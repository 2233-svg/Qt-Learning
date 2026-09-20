# Qt QReadWriteLock：读多写少场景的读写锁

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QReadWriteLock>`  
> 所属模块：`Qt6::Core`  
> 类型性质：不可复制的读写同步原语  
> 关联类型：`QReadLocker`、`QWriteLocker`、`QDeadlineTimer`

## 1. 它解决什么问题

`QReadWriteLock` 把访问分成两类：

- 读锁：多个线程可以同时读取；
- 写锁：同一时刻只能有一个写者，且写入期间排斥读者。

它适合读操作远多于写操作、并且共享状态可以被清晰划分为“只读观察”和“独占更新”的场景：

```cpp
class Catalog
{
public:
    QString lookup(const QString &key) const
    {
        QReadLocker locker(&m_lock);
        return m_values.value(key);
    }

    void replace(QHash<QString, QString> values)
    {
        QWriteLocker locker(&m_lock);
        m_values = std::move(values);
    }

private:
    mutable QReadWriteLock m_lock;
    QHash<QString, QString> m_values;
};
```

如果读写比例接近、临界区很短，普通 `QMutex` 往往更简单。读写锁不是“更快”的通用替代品，它有额外的状态管理和等待调度成本。

## 2. 它不是什么

`QReadWriteLock` 不是：

- 数据副本或快照；
- 自动保护所有别名的线程安全容器；
- 读锁升级为写锁的事务工具；
- 解决锁顺序和死锁的工具；
- QObject 线程亲和性的替代品；
- 支持跨线程随意解锁的句柄。

所有访问共享状态的路径都必须遵守同一保护协议。锁对象销毁前，不能还有线程持有或等待它。

## 3. 构建与最小示例

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QReadLocker>
#include <QReadWriteLock>
#include <QWriteLocker>

class State
{
public:
    int value() const
    {
        QReadLocker locker(&m_lock);
        return m_value;
    }

    void setValue(int value)
    {
        QWriteLocker locker(&m_lock);
        m_value = value;
    }

private:
    mutable QReadWriteLock m_lock;
    int m_value = 0;
};
```

`QReadLocker` 和 `QWriteLocker` 会自动管理解锁。需要超时获取时，直接调用 `tryLockForRead()` 或 `tryLockForWrite()`，因为 locker 本身没有超时构造函数。

## 4. 两种锁的基本规则

### 4.1 读锁允许并发读

多个线程同时调用 `lockForRead()` 可以成功，只要没有写者持有写锁。读锁内只能访问按协议可并发读取的状态：

```cpp
lock.lockForRead();
const auto snapshot = data;
lock.unlock();
```

读锁不会复制 `data`，也不会保护没有使用这把锁的写操作。

### 4.2 写锁独占

`lockForWrite()` 成功后，其他读者和写者都必须等待。适合修改容器结构、替换多个相互依赖的字段，或提交一份已经在锁外准备好的快照。

### 4.3 解锁不区分读写模式

无论当前取得的是读锁还是写锁，都调用同一个 `unlock()`。必须由取得锁的线程释放，并且加锁和解锁次数要匹配。

## 5. 递归模式

构造函数默认使用 `NonRecursive`：

```cpp
QReadWriteLock lock; // NonRecursive
```

非递归模式下，同一线程重复取得同一把锁可能自我阻塞或违反前置条件。尤其不要在持有读锁时再请求写锁：

```cpp
lock.lockForRead();
lock.lockForWrite(); // 可能永远等不到自己释放读锁
```

`Recursive` 模式允许同一线程递归取得同一把锁，但每次成功加锁都必须对应一次 `unlock()`：

```cpp
QReadWriteLock lock(QReadWriteLock::Recursive);
lock.lockForWrite();
lock.lockForWrite();
lock.unlock();
lock.unlock();
```

递归模式仍不能把读锁安全升级为写锁，也不能解决多个锁之间的顺序反转。只有在确实需要递归调用结构时才选择它；优先通过重构减少隐式递归。

## 6. 阻塞、立即尝试和超时

### 6.1 `lockForRead()` / `lockForWrite()`

两个函数会阻塞直到取得对应类型的锁。构造 `QReadLocker` 或 `QWriteLocker` 也会发生同样的阻塞，因为 locker 构造时立即加锁。

### 6.2 无参数 `tryLockForRead()` / `tryLockForWrite()`

立即尝试，不等待：

```cpp
if (!lock.tryLockForRead())
    return false;

readSnapshot();
lock.unlock();
return true;
```

失败返回 `false` 且不持有锁；只有成功返回 `true` 才需要调用 `unlock()`。

### 6.3 `tryLockForRead(int)` / `tryLockForWrite(int)`

以毫秒为单位等待：

```cpp
if (!lock.tryLockForWrite(50))
    return false;

update();
lock.unlock();
```

`0` 表示立即尝试；正值表示最多等待指定时长；负值的“无限等待”兼容语义不要作为普通业务输入，业务接口应明确区分阻塞、立即失败和有限超时。

### 6.4 `QDeadlineTimer` 重载

Qt 6.6 起支持按截止时间预算等待：

```cpp
const QDeadlineTimer deadline(200);
if (!lock.tryLockForRead(deadline))
    return false;

readSnapshot();
lock.unlock();
```

一个 deadline 可以在多个阶段共享总等待预算。默认构造的 `QDeadlineTimer` 是已经到期的有限 deadline，通常表现为不等待；需要无限等待时使用 `QDeadlineTimer::Forever`。

## 7. 读写锁升级和降级

`QReadWriteLock` 没有把当前读锁原子升级为写锁的公开操作。错误的升级方式：

```cpp
lock.lockForRead();
if (needsChange())
    lock.lockForWrite(); // 读锁仍在，可能自我阻塞
```

安全但非原子的流程是：

```cpp
lock.lockForRead();
const bool change = needsChange();
lock.unlock();

if (change) {
    lock.lockForWrite();
    if (needsChange()) // 释放读锁期间必须重新检查
        applyChange();
    lock.unlock();
}
```

如果检查和修改必须不可分割，应从一开始使用写锁，或重新设计数据结构和提交协议。

写锁降级为读锁也没有原子操作。应在写锁内复制需要的快照，释放写锁后在锁外使用快照；不要依赖短暂同时持有两种锁来实现降级。

## 8. 读者、写者和公平性

锁的调度由 Qt 和操作系统实现决定。业务代码不应依赖某个固定的先来先服务顺序，也不应把它当作实时公平队列。

长时间读临界区会阻塞写者；长时间写临界区会阻塞所有读者。读多写少并不意味着可以让读锁覆盖磁盘 I/O、网络请求、用户回调或大量计算。

把共享数据复制到局部快照后尽快解锁，通常比在锁内完成完整业务流程更稳定。

## 9. 临界区与死锁设计

### 9.1 锁内只做短状态访问

```cpp
const auto next = buildIndexOutsideLock();
{
    QWriteLocker locker(&m_lock);
    m_index = next;
}
emit indexChanged();
```

信号、插件回调和用户函数尽量放在锁外，避免同步槽重入并再次请求同一把锁。

### 9.2 固定多锁顺序

同时使用多把锁时，所有线程必须按同一顺序获取。读写锁的读/写模式不能消除锁顺序反转。

### 9.3 不要持锁等待依赖当前锁的线程

如果线程 A 持写锁等待线程 B，而 B 需要取得同一把锁才能结束，就会形成死锁。等待前先释放锁，或使用消息传递。

## 10. 生命周期、不可复制和线程边界

`QReadWriteLock` 不可复制。它通常作为共享状态 owner 的成员，并且地址在并发协议中保持稳定。

销毁顺序必须是：

1. 停止新任务进入；
2. 让所有工作线程结束对共享状态的访问；
3. 等待持锁线程退出；
4. 最后销毁包含 `QReadWriteLock` 的对象。

锁本身不绑定 QObject 线程，也不允许跨线程解锁。它能同步数据访问，但不能让跨线程 GUI 调用合法。

## 11. `QBasicReadWriteLock` 和标准库兼容接口

Qt 6.11.1 的 `QReadWriteLock` 继承轻量的 `QBasicReadWriteLock`，因此还提供标准读写锁风格的名称：

```cpp
lock.lock();          // 等价于 lockForWrite()
lock.lock_shared();   // 等价于 lockForRead()
lock.try_lock();      // 尝试写锁
lock.try_lock_shared(); // 尝试读锁
lock.unlock_shared(); // 释放读锁
```

这些接口适合与部分标准库泛型代码配合，但 `std::unique_lock` 只表达独占锁，不能自动表达共享读锁。Qt 自己的 `QReadLocker` / `QWriteLocker` 通常更直观。

## 12. 常见错误

### 12.1 只给写路径加锁

读路径绕过同一把锁仍然会和写线程产生数据竞争。所有访问路径都要统一。

### 12.2 读锁内申请写锁

这是典型的自我阻塞。先释放读锁，再重新检查并取得写锁，或直接使用写锁。

### 12.3 读锁内返回内部引用

locker 返回后读锁已经释放，内部引用可能马上被写线程修改。优先返回值或共享快照。

### 12.4 误以为 Recursive 解决死锁

递归模式只处理同一线程重复取得同一把锁的部分情况，不处理锁顺序反转、线程等待和外部回调重入。

### 12.5 忽略 tryLock 返回值

失败时没有锁，不能无条件调用 `unlock()`。成功路径要保证恰好释放一次。

### 12.6 把公平性当作业务保证

不要依赖读者或写者必然按某种顺序获得锁。需要严格排队时使用显式队列或消息协议。

## 13. 逐项 API 语义

### `QReadWriteLock(RecursionMode recursionMode = NonRecursive)`

创建读写锁。默认非递归；传入 `Recursive` 后，同一线程可以递归取得锁，但每次成功加锁都必须对应一次 `unlock()`。

### `~QReadWriteLock()`

销毁读写锁。销毁时不能有线程持有或等待该锁。

### `lockForRead()`

阻塞直到取得读锁。多个读者可并发；写者持有时会等待。

### `lockForWrite()`

阻塞直到取得独占写锁。取得后排斥所有通过同一锁协议进行的读写操作。

### `tryLockForRead()`

不等待地尝试读锁。成功返回 `true`，失败返回 `false`。

### `tryLockForWrite()`

不等待地尝试写锁。成功返回 `true`，失败返回 `false`。

### `tryLockForRead(int timeout)`

按毫秒等待读锁。只有成功才需要 `unlock()`。

### `tryLockForWrite(int timeout)`

按毫秒等待写锁。只有成功才需要 `unlock()`。

### `tryLockForRead(QDeadlineTimer timeout)`

Qt 6.6 起按截止时间预算尝试取得读锁。已到期的 deadline 通常立即失败。

### `tryLockForWrite(QDeadlineTimer timeout)`

Qt 6.6 起按截止时间预算尝试取得写锁。已到期的 deadline 通常立即失败。

### `unlock()`

释放当前线程通过该锁取得的读锁或写锁。加锁和解锁次数必须匹配，不能跨线程解锁。

### `lock()`

继承的标准库兼容名称，等价于 `lockForWrite()`。

### `lock_shared()`

继承的标准库兼容名称，等价于 `lockForRead()`。

### `try_lock()`

继承的标准库兼容名称，立即尝试取得写锁。

### `try_lock_shared()`

继承的标准库兼容名称，立即尝试取得读锁。

### `unlock_shared()`

继承的标准库兼容名称，释放当前读锁；使用时仍遵守同一线程和匹配次数规则。

## API 速查表
| 类别 | API | 作用 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QReadWriteLock(RecursionMode = NonRecursive)` | 创建读写锁并选择是否允许递归。 | 默认非递归；递归模式也不能解决读转写和多锁死锁。 |
| 生命周期 | `~QReadWriteLock()` | 销毁读写锁。 | 销毁前必须没有持有者和等待者。 |
| 读锁 | `lockForRead()` | 阻塞取得共享读锁。 | 多读者可并发；写者持有时等待。 |
| 写锁 | `lockForWrite()` | 阻塞取得独占写锁。 | 排斥读者和其他写者；构造 `QWriteLocker` 也会阻塞。 |
| 立即读锁 | `tryLockForRead()` | 不等待尝试读锁。 | 失败不持锁，不能无条件解锁。 |
| 立即写锁 | `tryLockForWrite()` | 不等待尝试写锁。 | 失败不持锁，成功后必须解锁。 |
| 超时读锁 | `tryLockForRead(int)` | 按毫秒等待读锁。 | `0` 立即尝试；处理返回值和释放责任。 |
| 超时写锁 | `tryLockForWrite(int)` | 按毫秒等待写锁。 | 读多写少不代表写锁可以覆盖慢操作。 |
| 截止读锁 | `tryLockForRead(QDeadlineTimer)` | 按 deadline 预算等待读锁。 | Qt 6.6 起；默认构造 deadline 通常表示已到期。 |
| 截止写锁 | `tryLockForWrite(QDeadlineTimer)` | 按 deadline 预算等待写锁。 | Qt 6.6 起；需要无限等待时用 `QDeadlineTimer::Forever`。 |
| 释放 | `unlock()` | 释放当前线程持有的读锁或写锁。 | 不能跨线程解锁；递归加锁要对应多次解锁。 |
| 标准接口 | `lock()` / `lock_shared()` | 分别映射写锁和读锁。 | 便于泛型代码，语义仍由读写锁规则约束。 |
| 标准接口 | `try_lock()` / `try_lock_shared()` | 分别立即尝试写锁和读锁。 | 返回 `false` 时不持锁。 |
| 标准接口 | `unlock_shared()` | 释放共享读锁。 | 只释放当前线程已取得的读锁。 |

## 15. 一句话总结

`QReadWriteLock` 用共享读锁和独占写锁解决读多写少的同步问题：先统一所有访问路径的保护协议，再选择阻塞或 tryLock 超时接口；不要在读锁内升级写锁、不要让锁跨越慢回调和线程等待，也不要把递归模式当成死锁修复器。
