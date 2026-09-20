# Qt QMutex：保护共享状态的互斥锁

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QMutex>`  
> 所属模块：`Qt6::Core`  
> 类型性质：不可复制的基础同步原语  
> 关联类型：`QMutexLocker`、`QRecursiveMutex`、`QDeadlineTimer`

## 1. 它解决什么问题

`QMutex` 保证同一时刻最多一个线程进入由它保护的临界区。它常用于保护多个线程共享的成员数据：

```cpp
class Counter
{
public:
    void increment()
    {
        QMutexLocker locker(&m_mutex);
        ++m_value;
    }

    int value() const
    {
        QMutexLocker locker(&m_mutex);
        return m_value;
    }

private:
    mutable QMutex m_mutex;
    int m_value = 0;
};
```

这里锁保护的是 `m_value` 的访问协议，不是对象本身的生命周期。所有读写路径都必须遵守同一把锁，否则仍然存在数据竞争。

适合场景：

- 保护共享容器、缓存和状态结构；
- 把多个字段的一次更新做成其他线程可观察的临界区；
- 保护非线程安全的第三方对象；
- 和 `QMutexLocker` 配合管理异常、早返回和多分支释放。

## 2. 它不是什么

`QMutex` 不是：

- 让任意 QObject 变成线程安全的开关；
- 事件循环或任务调度器；
- 读写锁；
- 自动解决死锁的工具；
- 保护没有使用它的代码路径的魔法屏障；
- 对象所有权或生命周期管理器。

锁只能建立使用同一把锁的线程之间的同步关系。对象析构、线程亲和性、信号重入和外部回调仍需单独设计。

## 3. 构建与最小示例

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QMutex>
#include <QMutexLocker>

class Cache
{
public:
    void put(QString key, QByteArray value)
    {
        QMutexLocker locker(&m_mutex);
        m_values.insert(std::move(key), std::move(value));
    }

    QByteArray get(const QString &key) const
    {
        QMutexLocker locker(&m_mutex);
        return m_values.value(key);
    }

private:
    mutable QMutex m_mutex;
    QHash<QString, QByteArray> m_values;
};
```

`QMutex` 默认构造为未锁定状态。它不需要手工初始化，也不能复制。

## 4. 基本锁语义

### 4.1 `lock()`：阻塞直到取得

```cpp
m_mutex.lock();
useSharedState();
m_mutex.unlock();
```

如果其他线程持有锁，`lock()` 会阻塞。手工配对容易因早返回或异常漏掉 `unlock()`，生产代码优先使用 `QMutexLocker`：

```cpp
QMutexLocker locker(&m_mutex);
useSharedState();
```

### 4.2 `unlock()`：释放当前线程持有的锁

只有成功取得锁的线程才能解锁。不能让线程 A 加锁、线程 B 解锁，也不能对未锁定的 mutex 调用 `unlock()`。违反这些前置条件会产生未定义行为或断言失败。

### 4.3 不递归

默认 `QMutex` 是非递归互斥锁。同一线程已经持有它时再次调用 `lock()`，通常会自我阻塞：

```cpp
mutex.lock();
mutex.lock(); // 错误设计：非递归锁会卡住
```

如果确实需要同一线程递归取得，使用 `QRecursiveMutex`，但优先先重新划分调用层次。递归锁只能改变重复加锁行为，不能修复锁顺序或重入导致的业务死锁。

## 5. 非阻塞和超时获取

### 5.1 `tryLock()`

```cpp
if (m_mutex.tryLock()) {
    useSharedState();
    m_mutex.unlock();
} else {
    deferOrRetry();
}
```

无参数版本立即尝试，成功返回 `true` 并由当前线程持有锁；失败返回 `false`，不会取得锁。

### 5.2 `tryLock(int timeout)`

```cpp
if (!m_mutex.tryLock(50))
    return false;

useSharedState();
m_mutex.unlock();
return true;
```

参数单位是毫秒。`0` 等价于不等待的尝试；正数最多等待指定时长；负值表示无限等待的兼容语义应谨慎使用，不要把负值当作“立即失败”的通用写法。

只有返回 `true` 时才有解锁责任。常见错误是忽略返回值后无条件 `unlock()`。

### 5.3 `tryLock(QDeadlineTimer)`

```cpp
const QDeadlineTimer deadline(200);
if (!m_mutex.tryLock(deadline))
    return false;

useSharedState();
m_mutex.unlock();
```

`QDeadlineTimer` 表示截止时间预算，而不是每次重试都重新开始的相对毫秒数。将同一个 deadline 传给多个阶段可以共享总等待预算：

```cpp
QDeadlineTimer deadline(200);
if (!first.tryLock(deadline))
    return false;
// ...
```

Qt 6.6 起提供该重载。默认构造的 `QDeadlineTimer` 表示已经到期的有限 deadline，不应误当成无限等待；需要无限等待时使用 `QDeadlineTimer::Forever`。

## 6. C++ Lockable 接口

`QMutex` 提供与标准库锁算法配合的接口：

```cpp
std::unique_lock<QMutex> lock(m_mutex);
std::scoped_lock lock2(m_mutex);
```

其中：

- `try_lock()` 等价于无参数 `tryLock()`；
- `try_lock_for(duration)` 按相对时长等待；
- `try_lock_until(timePoint)` 按时钟截止点等待；
- `lock()`、`unlock()` 满足基础 Lockable 契约。

使用标准库锁管理器时，仍需确认锁对象生命周期和锁顺序；接口兼容不代表死锁自动消失。

## 7. 临界区设计

### 7.1 只保护共享状态

```cpp
const QByteArray prepared = buildOutsideLock();
{
    QMutexLocker locker(&m_mutex);
    m_data = prepared;
}
emit dataChanged();
```

网络、磁盘、长计算、等待线程和用户回调尽量放到锁外。锁内发信号尤其要小心，因为槽可能重入当前对象、获取另一把锁或等待事件循环。

### 7.2 复制快照后解锁

```cpp
Snapshot Cache::snapshot() const
{
    QMutexLocker locker(&m_mutex);
    return Snapshot{m_values};
}
```

返回副本或隐式共享快照后，调用方在锁外继续处理，不要返回指向内部可变数据的裸引用。

### 7.3 所有路径使用同一把锁

只给写函数加锁、读函数不加锁并不能保证安全。`const` 查询函数也可能需要 `mutable QMutex`。

## 8. 生命周期和移动边界

`QMutex` 不可复制、不可移动。它通常作为拥有共享状态的对象成员：

```cpp
class Service
{
    QMutex m_mutex;
};
```

销毁 mutex 时，不能还有任何线程持有它或等待它。先停止工作线程、等待它们退出，再销毁包含 mutex 的对象。

不要把 `QMutex` 放在会被移动到其他地址、而其他线程仍持有其地址的对象中；mutex 地址应在并发协议中保持稳定。

## 9. 线程与内存可见性

成功的加锁和解锁建立相应的同步关系，使遵守同一锁协议的线程能够安全观察共享状态。它不会：

- 让未受保护的字段自动同步；
- 保护通过外部引用泄露的内部容器；
- 序列化 QObject 的任意方法；
- 允许跨线程直接调用 GUI 对象；
- 取消已经排队的信号或任务。

如果共享状态包含指针、引用或生命周期敏感对象，除了锁还要明确对象 owner 和销毁顺序。

## 10. 常见死锁来源

### 10.1 锁顺序反转

所有线程必须按同一顺序取得多把锁。`QMutexLocker` 只能自动释放，不能推导顺序。

### 10.2 持锁等待线程

线程 A 持锁等待线程 B；线程 B 需要同一把锁才能结束，会形成死锁。等待前先释放锁，或重新设计消息协议。

### 10.3 持锁发信号或回调

槽函数可能同步执行，也可能取得其他锁。先复制通知数据，解锁后再发信号或回调。

### 10.4 非递归锁重入

同一线程通过回调再次进入需要同一把锁的函数，会自己等待自己。减少锁内外部调用通常比改成递归锁更可靠。

## 11. 常见错误

### 11.1 忘记解锁

优先使用 `QMutexLocker`。手工 `lock()` 只适合控制流极简单且有明确测试的底层代码。

### 11.2 `tryLock()` 失败后仍然解锁

只有返回 `true` 才持有锁。失败路径不能调用 `unlock()`。

### 11.3 复制 QMutex

复制被禁用。复制一个锁也无法复制它保护的同步关系。

### 11.4 把 QMutex 当作 QReadWriteLock

QMutex 不允许多个读者并发；需要读多写少时选择 `QReadWriteLock`。

### 11.5 在锁内执行慢操作

会放大阻塞、超时和死锁风险。尽量锁内提交快照或短更新。

### 11.6 让 mutex 在等待者仍存在时销毁

必须先停止和 join 工作线程，再销毁 mutex 所属对象。

## 12. 逐项 API 语义

### `QMutex()`

constexpr 默认构造未锁定的 mutex。它不分配业务数据，也不与任何线程绑定。

### `~QMutex()`

销毁 mutex。销毁时不能仍有线程持有或等待它；否则行为未定义。

### `lock()`

阻塞直到当前线程取得锁。成功后必须由同一线程调用 `unlock()`。

### `tryLock()`

立即尝试取得锁。成功返回 `true` 并取得锁，失败返回 `false` 且不持有锁。

### `tryLock(int timeout)`

最多等待指定毫秒数取得锁。成功后由调用线程负责 `unlock()`；超时返回 `false`。

### `tryLock(QDeadlineTimer timeout)`

Qt 6.6 起按截止时间预算尝试取得锁。支持共享一个绝对 deadline；只有成功才有解锁责任。

### `unlock()`

释放当前线程持有的锁。只能对已锁定且由当前线程拥有的 mutex 调用。

### `try_lock()`

C++ Lockable 兼容接口，语义等同于 `tryLock()`。

### `try_lock_for(std::chrono::duration)`

Qt 6.3 头文件提供的标准库风格相对时长接口，等待指定 duration 后返回是否取得锁。

### `try_lock_until(std::chrono::time_point)`

按给定时钟时间点尝试取得锁。时钟类型和 deadline 的转换应由标准库/Qt 语义一致地处理。

## API 速查表
| 类别 | API | 作用 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QMutex()` | 创建未锁定的互斥锁。 | 不可复制移动；销毁前必须没有持有者和等待者。 |
| 生命周期 | `~QMutex()` | 销毁互斥锁。 | 不能与其他线程对该锁的访问并发发生。 |
| 阻塞获取 | `lock()` | 阻塞直到取得锁。 | 可能无限等待；由同一线程负责 `unlock()`。 |
| 非阻塞获取 | `tryLock()` | 立即尝试取得锁。 | `false` 表示没有取得锁，失败路径不要解锁。 |
| 超时获取 | `tryLock(int timeout)` | 按毫秒等待取得锁。 | `0` 表示立即尝试；只有成功才需要解锁。 |
| 截止时间 | `tryLock(QDeadlineTimer)` | 按 deadline 预算等待。 | Qt 6.6 起；默认构造 deadline 不等于 Forever。 |
| 释放 | `unlock()` | 释放当前线程持有的锁。 | 不允许跨线程解锁或对未锁定 mutex 解锁。 |
| 标准库接口 | `try_lock()` | `tryLock()` 的 Lockable 兼容别名。 | 适合 `std::unique_lock` 等标准工具。 |
| 标准库接口 | `try_lock_for(duration)` | 按相对时长尝试加锁。 | Qt 6.3 起；仍需处理返回值和解锁责任。 |
| 标准库接口 | `try_lock_until(timePoint)` | 按时钟时间点尝试加锁。 | 时钟和截止点要与业务超时模型一致。 |

## 14. 一句话总结

`QMutex` 是不可复制的互斥同步原语：`lock()` 阻塞取得、`tryLock()` 返回是否成功、`unlock()` 必须由持有线程执行。真正用稳它，关键不在 API 数量，而在所有访问路径统一加锁、临界区短小、锁顺序固定、销毁前先让所有线程退出。
