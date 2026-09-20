# Qt QRecursiveMutex 深入笔记：递归加锁、计数与重入边界

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QRecursiveMutex>`  
> 所属模块：`Qt6::Core`  
> 定位：允许同一线程重复取得同一把互斥锁

`QRecursiveMutex` 与 `QMutex` API 基本兼容，关键差异只有一个：当前持锁线程可以再次调用 `lock()`，不会把自己永久阻塞。内部会记录持有线程和递归层数；每次成功加锁都必须有一次对应解锁，计数归零后其他线程才能取得锁。

## 1. CMake 与最小可用代码

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QMutexLocker>
#include <QRecursiveMutex>

class Settings
{
public:
    void reset()
    {
        QMutexLocker locker(&m_mutex); // 第 1 层
        setValue("theme", "system");
        setValue("fontSize", 12);
    }

    void setValue(QString key, QVariant value)
    {
        QMutexLocker locker(&m_mutex); // 同一线程可进入第 2 层
        m_values.insert(std::move(key), std::move(value));
    }

private:
    QRecursiveMutex m_mutex;
    QHash<QString, QVariant> m_values;
};
```

这段代码可运行，但不一定是最佳设计。后文会把它改成普通 QMutex。

## 2. 递归锁的内部模型

普通 QMutex 的状态可近似理解为“未锁/已锁”。递归 mutex 还要记录持有者和深度：

```text
初始：owner = none, depth = 0

线程 A lock：   owner = A, depth = 1
线程 A lock：   owner = A, depth = 2
线程 B lock：   阻塞，因为 owner 是 A
线程 A unlock： owner = A, depth = 1
线程 A unlock： owner = none, depth = 0
线程 B：        现在才可能取得锁
```

“递归”指同一线程重复加锁，不是递归函数才可使用，也不是不同线程能共同持锁。其他线程仍然互斥。

## 3. 为什么同线程重复加锁有时会发生

最常见场景是一个已加锁的 public 函数调用另一个也会自行加锁的 public 函数：

```cpp
void Document::replaceAll(...)
{
    QMutexLocker locker(&m_mutex);
    remove(...); // remove() 也锁 m_mutex
    insert(...); // insert() 也锁 m_mutex
}
```

使用 QMutex 时会自死锁；QRecursiveMutex 允许嵌套调用。它能快速兼容既有 API，但代价是更高的构造和操作成本，也容易隐藏边界不清的调用结构。Qt 文档明确建议能用 QMutex 时优先使用 QMutex。

## 4. 优先方案：拆出已持锁实现

把公开入口和要求调用者已持锁的内部实现分开：

```cpp
class Settings
{
public:
    void reset()
    {
        QMutexLocker locker(&m_mutex);
        setValueLocked("theme", "system");
        setValueLocked("fontSize", 12);
    }

    void setValue(QString key, QVariant value)
    {
        QMutexLocker locker(&m_mutex);
        setValueLocked(std::move(key), std::move(value));
    }

private:
    void setValueLocked(QString key, QVariant value)
    {
        m_values.insert(std::move(key), std::move(value));
    }

    QMutex m_mutex;
    QHash<QString, QVariant> m_values;
};
```

常用命名包括 `fooLocked()`、`fooUnlocked()` 或带注释的 private helper。重要的是清楚说明前置条件，并确保这种 helper 不被未持锁路径调用。

这个结构的好处：

- 普通 QMutex 更轻量；
- 锁在哪一层取得一目了然；
- 不会因为深层函数偷偷重入而积累未知递归深度；
- 更容易审查临界区范围和回调风险；
- 更容易改用读写锁或消息传递。

## 5. `lock()` 和递归计数

```cpp
mutex.lock(); // depth + 1
mutex.lock(); // depth + 1

mutex.unlock(); // depth - 1，仍被当前线程持有
mutex.unlock(); // depth == 0，真正释放给其他线程
```

少一次 `unlock()` 不会只泄漏“一层小锁”，而是让其他线程永远无法取得它。多一次 `unlock()` 则对未锁 mutex 解锁，属于未定义行为。

因此更应该使用 RAII：

```cpp
void recurse(int depth)
{
    QMutexLocker locker(&m_mutex);
    if (depth > 0)
        recurse(depth - 1);
} // 每层 locker 精确对应一次 unlock
```

递归深度不应无界；锁允许重入不代表函数递归本身不会栈溢出。

## 6. `tryLock()` 与当前持有线程

### 6.1 截止时间版本（Qt 6.6）

```cpp
if (mutex.tryLock(QDeadlineTimer(200))) {
    performProtectedWork();
    mutex.unlock();
}
```

签名可写为：

```cpp
bool tryLock(QDeadlineTimer timeout = {});
```

默认构造的 QDeadlineTimer 已过期，所以无参数调用表现为立即尝试。若调用线程已经持有该递归锁，则能再次成功，递归计数加一，不需要等待。

### 6.2 毫秒版本

```cpp
bool acquired = mutex.tryLock(100);
```

最多等待指定毫秒。负值等价于 `lock()`，会一直等到能取得锁；0 表示立即尝试。成功一次就必须对应一次 `unlock()`，即使调用前当前线程已经持锁。

QRecursiveMutex 没有单独列出的 `tryLock()` 空参数旧式重载，但 `tryLock(QDeadlineTimer timeout = {})` 可以无参数调用。

## 7. 标准库兼容 API

### 7.1 立即尝试

```cpp
if (mutex.try_lock()) {
    update();
    mutex.unlock();
}
```

`try_lock()` 等价于无参数 `tryLock()`，用于标准库 Lockable 概念。

### 7.2 相对时间

```cpp
using namespace std::chrono_literals;

if (mutex.try_lock_for(50ms)) {
    update();
    mutex.unlock();
}
```

负 duration 表示立即 `try_lock()`，不同于 `tryLock(int)` 的负值无限等待。

### 7.3 绝对时间点

```cpp
auto until = std::chrono::steady_clock::now() + 50ms;
if (mutex.try_lock_until(until)) {
    update();
    mutex.unlock();
}
```

已过去的 time point 表示立即尝试。时间到达时返回 false；调度和系统等待精度意味着它不是硬实时截止保证。

### 7.4 标准 RAII

```cpp
std::lock_guard<QRecursiveMutex> guard(mutex);
update();
```

或：

```cpp
std::unique_lock<QRecursiveMutex> guard(mutex, std::defer_lock);
if (guard.try_lock_for(std::chrono::milliseconds(100)))
    update();
```

不要让两个 RAII 对象以为自己共同拥有同一次加锁。递归 mutex 会让这类错误暂时不显现，却仍可能造成计数不匹配。

## 8. 构造、析构和线程规则

```cpp
QRecursiveMutex mutex; // 初始未锁定，constexpr noexcept 构造
```

析构时仍被锁定可能导致未定义行为。必须先停止并等待所有访问线程，再销毁拥有 mutex 的对象。

`unlock()` 必须由当前持有线程调用。不能在线程 A 加锁后让线程 B 负责解锁。递归锁记录的是线程身份，不能作为跨线程“交接令牌”。需要许可计数或生产者/消费者协作时应使用 QSemaphore、QWaitCondition 或消息队列。

## 9. 递归锁不等于可重入代码

“锁可递归取得”只解决同一线程再次锁定的问题，不保证业务函数真正可重入。

```cpp
void Model::update()
{
    QMutexLocker locker(&m_mutex);
    m_updating = true;
    emit aboutToChange(); // direct 槽可能同步调用 update()
    mutateInternalState();
    m_updating = false;
}
```

QRecursiveMutex 让第二次 `update()` 通过，但此时第一次更新处于半完成状态。结果可能是状态损坏，而不是死锁。普通 QMutex 的死锁反而暴露了危险重入。

稳妥做法是：

- 持锁时不调用未知代码或发出可能 direct 回调的信号；
- 在锁内完成状态转换并复制通知数据；
- 解锁后再发信号；
- 若业务确实允许重入，明确设计状态机和每个中间状态的语义。

## 10. 递归锁也不能解决多锁死锁

```text
线程 A：持有 Recursive M1 -> 等 M2
线程 B：持有 Recursive M2 -> 等 M1
```

递归能力只针对“同一线程、同一把锁”，对两个线程形成的等待环毫无帮助。多锁仍要统一顺序，或用 `std::scoped_lock` 同时取得：

```cpp
std::scoped_lock guard(firstMutex, secondMutex);
updateBoth();
```

还要处理两个引用可能指向同一 mutex 的别名情况；不能把同一递归锁传两次并假设所有标准算法都按业务预期处理。

## 11. 合理使用场景

递归 mutex 可能合理的场景：

- 稳定的公开 API 之间必须互相调用，短期无法拆分内部实现；
- 第三方回调架构明确允许同线程同步回入，且业务中间状态已经设计为可重入；
- 递归数据结构算法在每层都必须调用同一个公开锁入口，重构成本明显更高；
- 兼容旧代码时先恢复正确性，再逐步收敛锁结构。

不合理的理由：

- “普通 QMutex 会卡住，所以换一个”；
- 不知道调用链上谁已经持锁；
- 用它掩盖持锁发信号造成的回调；
- 希望不同线程都能重复进入；
- 希望避免规划多把锁的顺序。

## 12. 与 QMutex 的选择

| 维度 | QMutex | QRecursiveMutex |
|---|---|---|
| 同线程重复 lock | 自死锁 | 成功并增加深度 |
| 其他线程访问 | 互斥 | 互斥 |
| 构造和操作成本 | 更低 | 明显更高 |
| 暴露意外重入 | 容易通过死锁暴露 | 可能掩盖问题 |
| 默认选择 | 是 | 否，确有递归需求才用 |
| QMutexLocker 支持 | 支持 | 支持 |
| 标准 Lockable API | 支持 | 支持 |

性能不是唯一原因。普通锁迫使代码明确持锁边界，通常更利于长期维护。

## 13. 常见错误

### 错误 1：加锁两次，只解锁一次

其他线程会永久等待。每次成功 lock/tryLock 都必须独立配对 unlock，使用 RAII 自动管理。

### 错误 2：认为递归锁允许另一线程解锁

它只允许持锁线程重复获取，解锁仍必须由持有线程执行。

### 错误 3：持锁发出同步回调

递归锁避免了自死锁，却可能让回调观察半完成状态。先完成状态、解锁，再通知。

### 错误 4：用递归锁修复锁顺序反转

线程间的多锁等待环仍然存在。建立全局锁顺序。

### 错误 5：析构时仍有递归层数

只要 depth 不为 0，mutex 就仍处于锁定状态。析构可能产生未定义行为。

### 错误 6：负超时语义混淆

`tryLock(-1)` 无限等待，`try_lock_for(-1ms)` 立即尝试。跨两套 API 时必须显式处理输入。

## API 速查表
递归锁解决的是“同一线程因调用链重入而再次请求同一把锁”，不是一般性的并发正确性方案。每次成功加锁都必须有一次对应解锁；查表时要特别分清递归层数、超时尝试和跨线程所有权。

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 生命周期 | `QRecursiveMutex()` | 构造一把初始未锁定的递归互斥锁。 | 比 `QMutex` 成本更高；只有确实需要同线程重复进入时使用。 |
| 生命周期 | `~QRecursiveMutex()` | 销毁递归互斥锁。 | 析构前递归深度必须为 0，且没有其他线程仍可能访问它。 |
| 阻塞加锁 | `lock()` | 取得锁；若当前线程已持有，则递归深度加一。 | 每次成功调用都必须对应一次 `unlock()`；递归能力不表示业务状态可安全重入。 |
| 解锁 | `unlock()` | 释放一层递归持有。 | 只有深度归零时才真正让其他线程进入；必须由持有线程调用。 |
| deadline 尝试 | `tryLock(QDeadlineTimer timeout = {})` | 在截止时间前尝试取得锁。 | 当前线程已持锁时会再次成功并增加深度；默认过期 deadline 表示立即尝试。 |
| 毫秒尝试 | `tryLock(int timeout)` | 最多等待指定毫秒取得锁。 | `timeout < 0` 表示无限等待；成功后即使原本已持锁，也要多解锁一次。 |
| 标准接口 | `try_lock()` | 标准库 Lockable 风格的立即尝试。 | 等价于无参数 `tryLock()`；成功后可交给标准 RAII 管理。 |
| 标准接口 | `try_lock_for(std::chrono::duration duration)` | 在相对 chrono duration 内尝试取得锁。 | 负 duration 表示立即尝试，不同于 `tryLock(int)` 的负数无限等待。 |
| 标准接口 | `try_lock_until(std::chrono::time_point timePoint)` | 尝试等待到指定 chrono 时间点。 | 已过去的时间点表示立即尝试；不是硬实时截止保证。 |
| RAII 搭档 | `QMutexLocker<QRecursiveMutex>` | 用作用域对象配对递归 lock/unlock。 | 每层递归调用各自拥有一个 locker，可避免少解锁导致深度泄漏。 |
| 设计取舍 | 与 `QMutex` 对比 | 解决同线程重复请求同一锁时的自死锁。 | 不能解决多锁顺序反转、跨线程解锁、持锁回调看到半完成状态等问题。 |

## 15. 总结

1. QRecursiveMutex 允许同一持锁线程重复 lock，并用递归深度记录未完成的解锁次数。
2. 每次成功加锁都必须有一次解锁，只有深度归零其他线程才能进入。
3. 它的构造与操作明显比 QMutex 昂贵，普通 QMutex 应是默认选择。
4. public 函数互调时，优先拆出要求已持锁的 private helper。
5. 锁可递归不等于业务代码可重入；半完成状态仍可能被同步回调破坏。
6. 它不能解决不同线程、不同锁之间的等待环。
7. Qt 毫秒负超时与标准 chrono 负时长的语义相反。
8. QMutexLocker 和标准库 RAII 都可管理它，能避免递归计数失配。
9. 不能跨线程解锁，也不能在仍被持有时销毁。
10. 采用递归锁时应记录具体原因，避免它成为模糊锁边界的长期掩护。
