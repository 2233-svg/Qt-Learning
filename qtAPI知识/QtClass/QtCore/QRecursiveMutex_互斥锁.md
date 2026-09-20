# Qt QRecursiveMutex：允许同一线程重复加锁的互斥量

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QRecursiveMutex>`  
> 所属模块：`Qt6::Core`  
> 类型性质：不可复制、不可移动的线程同步对象

## 1. 它解决什么问题

`QRecursiveMutex` 是一种允许递归取得的互斥量。持有它的线程可以再次调用 `lock()` 或成功调用 `tryLock()`，不会因为自己已经持锁而自我阻塞；其他线程仍然必须等待。

```cpp
QRecursiveMutex mutex;

mutex.lock();   // 深度 1
mutex.lock();   // 同一线程再次成功，深度 2
mutex.unlock(); // 深度 1
mutex.unlock(); // 深度 0，真正释放
```

它适合：

- 一个已持锁的公开函数会调用另一个也负责加锁的公开函数；
- 旧接口层次较深，暂时无法把“已持锁”前置条件统一下沉；
- 需要与 `QMutex` 相近的 API，但明确允许同线程重入。

它不是“更安全的 QMutex”。Qt 文档明确建议能使用普通 `QMutex` 时优先使用 `QMutex`，因为递归锁构造和操作成本更高，而且可能掩盖临界区设计问题。

## 2. 递归锁的状态模型

```text
初始：owner = none, depth = 0

线程 A lock       -> owner = A, depth = 1
线程 A 再次 lock  -> owner = A, depth = 2
线程 B lock       -> 阻塞
线程 A unlock     -> depth = 1，仍由 A 持有
线程 A unlock     -> depth = 0，B 才可能取得
```

递归计数是“成功加锁次数”与“解锁次数”的严格配对。少一次 `unlock()` 会让其他线程一直无法获得锁；多一次 `unlock()` 则属于错误使用。

## 3. 为什么会需要它

典型结构是多个公开成员都自行加锁：

```cpp
class Settings
{
public:
    void reset()
    {
        QMutexLocker locker(&m_mutex);
        setValue(QStringLiteral("theme"), QStringLiteral("system"));
    }

    void setValue(const QString &key, const QString &value)
    {
        QMutexLocker locker(&m_mutex);
        m_values.insert(key, value);
    }

private:
    QRecursiveMutex m_mutex;
    QHash<QString, QString> m_values;
};
```

`reset()` 调用 `setValue()` 时会在同一线程再次加锁。`QMutex` 会在这里自死锁，而 `QRecursiveMutex` 会增加递归深度。

更推荐的长期设计是拆出要求“调用者已经持锁”的 private helper，用普通 `QMutex`，让锁边界更明显：

```cpp
void reset()
{
    QMutexLocker locker(&m_mutex);
    setValueLocked(QStringLiteral("theme"), QStringLiteral("system"));
}
```

## 4. `lock()` 和 `unlock()`

```cpp
mutex.lock();
try {
    updateSharedState();
} catch (...) {
    mutex.unlock();
    throw;
}
mutex.unlock();
```

实际代码应优先使用 RAII：

```cpp
QMutexLocker locker(&mutex);
updateSharedState();
```

`lock()` 在其他线程持锁时阻塞，直到锁可用；同一线程重复调用会成功并增加递归深度。

`unlock()` 只能由当前持有线程调用，并且必须与成功的加锁次数对应。对未锁定的 mutex 解锁是未定义行为；错误线程解锁会产生错误。

## 5. `tryLock()` 的超时语义

### 5.1 `QDeadlineTimer` 版本

```cpp
if (mutex.tryLock(QDeadlineTimer(200))) {
    updateSharedState();
    mutex.unlock();
}
```

Qt 6.6 起提供：

```cpp
bool tryLock(QDeadlineTimer timeout = {});
```

它在截止时间到达前等待；成功返回 `true`，超时返回 `false`。默认构造的 `QDeadlineTimer` 可用于立即尝试。

当前线程已经持有锁时，调用仍会成功并增加递归深度。无论之前是否持有，都必须为这次成功调用再执行一次 `unlock()`。

### 5.2 毫秒版本

```cpp
bool acquired = mutex.tryLock(100);
```

最多等待 `timeout` 毫秒。`timeout == 0` 表示立即尝试；负值等价于 `lock()`，会一直等待。

### 5.3 标准库兼容版本

```cpp
if (mutex.try_lock()) {
    work();
    mutex.unlock();
}
```

`try_lock()` 等价于无参数 `tryLock()`，用于满足标准库 `Lockable` 风格接口。

```cpp
using namespace std::chrono_literals;

if (mutex.try_lock_for(50ms)) {
    work();
    mutex.unlock();
}

auto deadline = std::chrono::steady_clock::now() + 50ms;
if (mutex.try_lock_until(deadline)) {
    work();
    mutex.unlock();
}
```

`try_lock_for()` 的负 duration 表示立即尝试；`try_lock_until()` 已经过期的时间点也表示立即尝试。这与 `tryLock(int)` 的负值无限等待不同，不能混用记忆。

## 6. 递归不是业务重入许可

递归锁只允许同一线程再次取得锁，不代表对象可以在半更新状态中被重入：

```cpp
void update()
{
    QMutexLocker locker(&m_mutex);
    m_updating = true;
    emit aboutToChange(); // direct slot 可能同步重入 update()
    mutate();
    m_updating = false;
}
```

第二次 `update()` 可能顺利拿到递归锁，却看到 `m_updating == true` 的中间状态。应尽量：

- 持锁时不发出可能同步调用未知代码的信号；
- 在锁内完成状态转换，复制通知所需数据；
- 解锁后再发信号或执行用户回调；
- 对确实允许的重入建立明确状态机。

## 7. 生命周期和线程边界

`QRecursiveMutex` 初始未锁定。销毁仍被锁定的 mutex 可能导致未定义行为，因此析构拥有它的对象前必须：

1. 停止新的访问；
2. 等待正在运行的线程离开临界区；
3. 确认递归深度已经归零；
4. 再销毁 mutex。

它不具有 QObject 的线程亲和性，也不需要事件循环；但这不意味着可以让任意线程随意销毁或解锁。持有关系仍由线程身份约束。

## 8. 多锁和死锁

递归能力解决不了多锁等待环：

```text
线程 A：持有 M1，等待 M2
线程 B：持有 M2，等待 M1
```

多个锁仍应统一取得顺序，或使用适合的标准库多锁算法。持锁期间还应避免等待线程、阻塞 I/O、发信号和执行未知回调。

## 9. 常见错误

### 9.1 把它当作普通 QMutex 的无代价替代品

递归 mutex 更重。只有确实需要同线程嵌套加锁时才使用。

### 9.2 只解锁一次

每次成功 `lock()`、`tryLock()` 或 `try_lock*()` 都要对应一次 `unlock()`。

### 9.3 认为其他线程也能解锁

不能把锁交给另一个线程解锁。需要跨线程交接许可时使用信号量、消息队列或其他明确协议。

### 9.4 混淆不同超时 API 的负值

`tryLock(int)` 的负值表示无限等待；标准库兼容的 `try_lock_for()` 负 duration 表示立即尝试。

### 9.5 持锁发信号或调用回调

递归锁会让危险重入不再暴露为死锁，但对象状态仍可能被打断。

## 10. 逐项 API 语义

| API | 语义 | 边界 |
| --- | --- | --- |
| `QRecursiveMutex()` | 构造未锁定的递归 mutex。 | `constexpr noexcept`；不可复制移动。 |
| `~QRecursiveMutex()` | 销毁 mutex。 | 仍被锁定时可能是未定义行为。 |
| `void lock()` | 阻塞直到取得锁；同线程重复调用会增加深度。 | 每次成功调用都需一次 `unlock()`。 |
| `bool tryLock(QDeadlineTimer timeout = {})` | 在截止时间前尝试取得锁。 | Qt 6.6 起；当前线程重入也会成功。 |
| `bool tryLock(int timeout)` | 最多等待指定毫秒。 | 负值等价于无限等待。 |
| `bool try_lock()` | 标准库兼容的立即尝试。 | 成功后必须解锁。 |
| `bool try_lock_for(std::chrono::duration<Rep, Period> duration)` | 按相对 duration 尝试。 | 负 duration 表示立即尝试。 |
| `bool try_lock_until(std::chrono::time_point<Clock, Duration> timePoint)` | 按绝对时间点尝试。 | 已经过期表示立即尝试。 |
| `void unlock()` | 减少当前线程的递归深度；归零后释放。 | 必须由持有线程调用，次数必须匹配。 |

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QRecursiveMutex()` | 创建未锁定的递归互斥量。 | 不负责保护任何外部对象。 |
| 阻塞加锁 | `lock()` | 等待并取得锁。 | 同线程重入会增加深度。 |
| 有限等待 | `tryLock(int)` | 最多等待指定毫秒。 | 负值是无限等待。 |
| 截止时间 | `tryLock(QDeadlineTimer)` | 等到截止时间。 | Qt 6.6 起；成功后要解锁。 |
| 标准兼容 | `try_lock()` / `try_lock_for()` / `try_lock_until()` | 接入 C++ 标准库锁概念。 | 负值语义与 `tryLock(int)` 不同。 |
| 解锁 | `unlock()` | 释放一层递归深度。 | 加锁解锁必须严格配对。 |
| RAII | `QMutexLocker<QRecursiveMutex>` | 作用域管理加锁和解锁。 | 推荐用于异常安全。 |

---

### 一句话总结

`QRecursiveMutex` 允许同一线程重复取得同一把锁，但每一层成功加锁都必须对应解锁；它解决的是锁重入，不是业务状态重入或多锁死锁。
