# Qt QMutex 深入笔记：互斥保护、超时锁与死锁规避

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QMutex>`  
> 所属模块：`Qt6::Core`  
> 定位：让同一时刻最多一个线程进入受保护的临界区

`QMutex` 是非递归互斥锁。它的真正用途不是“保护某一行代码”，而是保护一组共享状态及其不变量：线程取得锁后才能观察或修改这组状态，释放锁前必须重新建立有效状态。

## 1. CMake 与最小可用代码

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

推荐通过 `QMutexLocker` 使用 RAII：

```cpp
#include <QMutex>
#include <QMutexLocker>
#include <QStringList>

class MessageStore
{
public:
    void append(QString message)
    {
        QMutexLocker locker(&m_mutex);
        m_messages.append(std::move(message));
    }

    QStringList snapshot() const
    {
        QMutexLocker locker(&m_mutex);
        return m_messages;
    }

private:
    mutable QMutex m_mutex;
    QStringList m_messages;
};
```

锁与被保护数据属于同一个对象，成员函数返回时 locker 自动解锁，即使中途 `return` 或抛异常也不会漏掉。

## 2. 互斥锁到底保证什么

假设两个字段必须满足 `available + borrowed == total`。只给某一个整数做原子操作无法保护这个跨字段关系：

```cpp
void Inventory::borrowOne()
{
    QMutexLocker locker(&m_mutex);

    if (m_available == 0)
        return;

    --m_available;
    ++m_borrowed;
    // 离开临界区时整体不变量仍成立。
}
```

同一把 mutex 形成同步关系：一个线程在解锁前完成的写入，对随后成功锁住同一 mutex 的线程可见。但前提是所有访问路径都遵守同一协议。某个“只读”函数若不加锁，仍会与写线程产生数据竞争。

```text
线程 A：lock -> 修改共享状态 -> unlock
                                  |
                                  | 同步/可见性
                                  v
线程 B：                       lock -> 读取新状态 -> unlock
```

mutex 不会自动识别要保护的数据，也不会阻止绕过锁的代码访问它。

## 3. 构造与生命周期

```cpp
QMutex mutex; // 初始为未锁定
```

QMutex 构造和销毁开销很低；无竞争时不会为锁动态分配内存，因此把锁作为业务类成员是正常做法。

它不可复制。锁的生命周期必须覆盖所有可能访问它的线程，也必须覆盖被保护状态的生命周期。

销毁仍处于锁定状态的 QMutex 可能导致未定义行为：

```cpp
// 错误模型：后台线程仍在 lock/unlock，拥有 mutex 的对象先析构。
delete sharedState;
```

对象析构前先停止并等待所有使用者，而不是试图在析构函数中“抢最后一次锁”解决生命周期竞态。

## 4. `lock()` 与 `unlock()`

```cpp
m_mutex.lock();
updateState();
m_mutex.unlock();
```

`lock()` 在锁空闲时取得所有权；若其他线程持有，就阻塞到锁可用。`unlock()` 必须由取得锁的同一线程调用。

以下行为错误：

- 未持锁却调用 `unlock()`：未定义行为；
- 在线程 A 加锁、线程 B 解锁：错误；
- 同一线程对非递归 QMutex 连续 `lock()`：自死锁；
- mutex 仍锁定时将其销毁：可能是未定义行为。

手工 lock/unlock 容易在提前返回处遗漏：

```cpp
m_mutex.lock();
if (!isValid())
    return; // 错误：永远没有 unlock
m_mutex.unlock();
```

除非必须与特殊 API 交互，否则使用 QMutexLocker 或标准库 lock guard。

## 5. `tryLock()` 三种 Qt 风格接口

### 5.1 立即尝试

```cpp
if (m_mutex.tryLock()) {
    inspectState();
    m_mutex.unlock();
} else {
    skipOptionalWork();
}
```

锁空闲就返回 true 并取得锁，否则立即返回 false。成功后必须解锁。

### 5.2 毫秒超时

```cpp
if (m_mutex.tryLock(100)) {
    updateState();
    m_mutex.unlock();
}
```

最多等待 `timeout` 毫秒。负数有特殊含义：等价于 `lock()`，即无限等待；0 等价于立即尝试。

### 5.3 绝对截止时间（Qt 6.6）

```cpp
QDeadlineTimer deadline(500);

if (m_mutex.tryLock(deadline)) {
    updateState();
    m_mutex.unlock();
}
```

截止时间适合把同一总预算传过多层调用：

```cpp
bool Service::complete(QDeadlineTimer deadline)
{
    if (!firstMutex.tryLock(deadline))
        return false;
    std::unique_lock<QMutex> firstGuard(firstMutex, std::adopt_lock);

    return secondStage(deadline); // 继续消耗同一总预算
}
```

`std::adopt_lock` 表示当前线程已经成功取得锁，由 `unique_lock` 接管后续解锁。关键思想是不要在每层重新获得“完整 500 ms”。

## 6. 标准库兼容接口

QMutex 满足标准库 Lockable 相关接口，可与 C++ 锁工具组合。

### 6.1 `try_lock()`

```cpp
bool acquired = mutex.try_lock();
```

等价于 `tryLock()`。QMutex 本身已有 `lock()` 和 `unlock()`，所以可用于 `std::lock_guard`：

```cpp
std::lock_guard<QMutex> guard(mutex);
updateState();
```

### 6.2 `try_lock_for()`

```cpp
using namespace std::chrono_literals;

if (mutex.try_lock_for(50ms)) {
    updateState();
    mutex.unlock();
}
```

等待指定 duration。负 duration 等价于立即 `try_lock()`，这一点与 `tryLock(int)` 的负数表示无限等待不同。

### 6.3 `try_lock_until()`

```cpp
auto deadline = std::chrono::steady_clock::now() + 50ms;
if (mutex.try_lock_until(deadline)) {
    updateState();
    mutex.unlock();
}
```

等待到指定 time point。已过去的时间点等价于立即尝试，同样不同于负数毫秒的 Qt 旧式接口。

### 6.4 用 `std::unique_lock`

```cpp
std::unique_lock<QMutex> lock(mutex, std::defer_lock);
if (lock.try_lock_for(std::chrono::milliseconds(100)))
    updateState();
```

`unique_lock` 适合延迟加锁、条件加锁或与多个标准库锁协作。团队应统一风格，避免同一作用域同时用手工 unlock 和 RAII 对同一所有权负责。

## 7. QMutex 是非递归锁

```cpp
void Cache::outer()
{
    QMutexLocker locker(&m_mutex);
    inner();
}

void Cache::inner()
{
    QMutexLocker locker(&m_mutex); // 同一线程再次获取，死锁
}
```

更好的修正通常是拆出要求“调用者已持锁”的私有函数：

```cpp
void Cache::outer()
{
    QMutexLocker locker(&m_mutex);
    innerLocked();
}

void Cache::inner()
{
    QMutexLocker locker(&m_mutex);
    innerLocked();
}

void Cache::innerLocked()
{
    // 约定调用者已持有 m_mutex。
}
```

`QRecursiveMutex` 允许同线程重复加锁，但可能掩盖调用层次和所有权设计问题，开销也更高。只有接口确实无法避免重入时才采用。

## 8. 临界区应该保护什么

### 8.1 保护不变量

把必须一致变化的数据放在同一临界区：

```cpp
QMutexLocker locker(&m_mutex);
account.balance -= amount;
ledger.append(Transaction{-amount});
```

若中途释放锁，其他线程可能看到余额已变但流水尚未记录的非法中间状态。

### 8.2 缩短锁内耗时

先在锁外完成昂贵计算，再短暂提交：

```cpp
Result calculated = expensivePureCalculation(input);

{
    QMutexLocker locker(&m_mutex);
    m_latest = std::move(calculated);
    ++m_version;
}
```

不要在持锁时做网络请求、磁盘 I/O、长时间计算、sleep 或阻塞式跨线程调用。它们扩大争用，也容易把外部依赖引入死锁环。

### 8.3 不要在持锁时发出未知回调

```cpp
QMutexLocker locker(&m_mutex);
emit changed(); // direct 槽可能同步回调当前对象并再次取锁
```

通常先复制通知所需数据，解锁，再发信号：

```cpp
Snapshot snapshot;
{
    QMutexLocker locker(&m_mutex);
    updateLocked();
    snapshot = makeSnapshotLocked();
}
emit changed(snapshot);
```

信号连接类型可能随对象线程归属变化；不能假设它永远 queued。

## 9. 多把锁与死锁

经典锁顺序反转：

```text
线程 A：锁住 M1 -> 等待 M2
线程 B：锁住 M2 -> 等待 M1
```

解决方式是定义全局一致顺序：永远先 M1 后 M2。对于标准库兼容锁，可使用 `std::scoped_lock` 一次取得多把锁：

```cpp
std::scoped_lock guard(first.mutex, second.mutex);
transferLocked(first, second, amount);
```

若两个参数可能引用同一对象，要先处理自转账等别名情况，否则相当于对同一非递归锁加两次。

超时锁能让调用最终返回，但不能自动修复不一致的锁顺序。它通常是故障控制措施，不应成为死锁设计的遮盖物。

## 10. 可变 mutex 与 const 接口

读取逻辑状态的 const 函数仍需同步：

```cpp
class Counter
{
public:
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

`mutable` 表示锁不属于对象对外可观察的业务状态。它不是允许 const 函数随意修改业务数据的借口。

不要返回受锁保护数据的引用：

```cpp
const QStringList &messages() const; // 返回后锁已释放，引用可能被并发修改
```

返回快照或提供在锁内执行的受控操作。

## 11. Mutex 与其他同步工具

| 需求 | 工具 |
|---|---|
| 独占保护一组可变状态 | `QMutex` |
| 同一线程必须递归获取 | `QRecursiveMutex`，先审视设计 |
| 自动作用域解锁 | `QMutexLocker` |
| 读多写少、允许并发读 | `QReadWriteLock` |
| 等待“状态变为真” | `QWaitCondition + QMutex` |
| 计数型资源许可 | `QSemaphore` |
| 单个简单数值/标志 | `std::atomic`，前提是不涉及复合不变量 |
| QObject 跨线程传递命令 | queued signal/slot |

mutex 提供互斥，不提供条件等待。轮询“加锁、检查、解锁、sleep”应改为 QWaitCondition，避免延迟和无谓唤醒。

## 12. 性能与公平性

QMutex 针对无竞争路径优化，无竞争时不会动态分配。但锁是否“轻量”不意味着可以忽视设计：

- 竞争会引起线程休眠、唤醒和上下文切换；
- 热点全局锁会串行化所有任务；
- cache line 在核心间移动也有成本；
- Qt 不承诺严格 FIFO 公平性，不能依赖等待最久者必定先取得锁；
- 高频 tryLock 自旋会浪费 CPU 并可能使持锁线程更难获得调度。

优化前先测量。拆锁会增加不变量复杂度和多锁死锁风险；有时复制不可变快照或通过消息传递消除共享写状态更简单。

## 13. 常见错误

### 错误 1：只有写操作加锁

无锁读取与加锁写入仍是数据竞争。所有访问路径必须使用同一同步协议。

### 错误 2：锁是函数局部变量

```cpp
void append()
{
    QMutex mutex; // 每次调用各有一把锁，线程之间互不排斥
    QMutexLocker locker(&mutex);
    sharedList.append(value);
}
```

锁必须由访问者共享，通常与共享数据同生命周期。

### 错误 3：复制指针后解锁，误以为对象安全

锁内取得裸指针不保证解锁后目标仍存活。应复制值、使用共享所有权，或让后续操作仍处于明确的生命周期协议中。

### 错误 4：用 mutex 让 QObject 变得可跨线程随意调用

mutex 能保护业务数据，却不会改变 QObject 的线程亲和性规则。Timer、socket、GUI 和事件相关成员仍只能在所属线程操作。

### 错误 5：持锁等待另一个线程结束

若目标线程退出前也需要同一把锁，就会死锁。发出停止请求后先释放业务锁，再 `wait()`。

### 错误 6：忽略 tryLock 返回值

```cpp
mutex.tryLock(10);
update(); // 可能根本没取得锁
mutex.unlock();
```

只有返回 true 才拥有锁并有义务解锁。

## API 速查表
`QMutex` 的 API 很少，但每个调用都带着线程间协议：先决定保护哪组不变量，再选择阻塞、限时尝试或标准库适配接口。表中尤其要注意超时值的语义和“谁加锁谁解锁”的所有权边界。

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 生命周期 | `QMutex()` | 构造一把初始未锁定的非递归互斥锁。 | 适合作为受保护数据的成员；不可复制，也不应临时创建来保护共享状态。 |
| 生命周期 | `~QMutex()` | 销毁 mutex。 | 销毁时必须没有线程持有或等待使用它；锁定状态销毁可能导致未定义行为。 |
| 阻塞加锁 | `lock()` | 无限等待直到当前线程取得锁。 | `QMutex` 非递归，同一线程重复 `lock()` 会自死锁；优先用 `QMutexLocker` 管理。 |
| 解锁 | `unlock()` | 释放当前线程持有的锁。 | 必须由成功取得锁的同一线程调用；未持锁解锁是错误行为。 |
| 立即尝试 | `tryLock()` | 锁空闲则立即取得，忙时立即返回 false。 | 返回 true 后才拥有锁并必须解锁；不要忽略返回值继续访问共享数据。 |
| 毫秒超时 | `tryLock(int timeout)` | 最多等待指定毫秒取得锁。 | `timeout < 0` 等价于无限等待，`0` 等价于立即尝试；这是 Qt 风格语义。 |
| 截止时间 | `tryLock(QDeadlineTimer timeout)` | 在同一个绝对截止点前尝试取得锁。 | 适合把总时间预算贯穿多层调用；不要每层重新构造完整 timeout。 |
| 标准接口 | `try_lock()` | 标准库 Lockable 风格的立即尝试。 | 等价于 `tryLock()`，用于 `std::unique_lock` 等标准工具。 |
| 标准接口 | `try_lock_for(std::chrono::duration duration)` | 在相对 chrono duration 内尝试取得锁。 | 负 duration 表示立即尝试，不同于 `tryLock(int)` 的负数无限等待。 |
| 标准接口 | `try_lock_until(std::chrono::time_point timePoint)` | 尝试等待到指定 chrono 时间点。 | 已过去的 time point 等价于立即尝试；真实等待精度受系统调度影响。 |
| RAII 搭档 | `QMutexLocker<QMutex>` | 作用域内自动加锁、退出时自动解锁。 | 最常用；能避免提前 return、异常路径漏掉 `unlock()`。 |
| 标准 RAII | `std::lock_guard` / `std::unique_lock` / `std::scoped_lock` | 用标准库包装器管理 `QMutex`。 | 多锁、延迟加锁或 adopt-lock 需求时更合适；同一锁所有权不要混用多个包装器。 |

## 15. 总结

1. QMutex 保护的是共享状态的不变量，所有读写路径都必须遵守同一协议。
2. 成功加锁与随后解锁建立线程间的互斥和可见性关系。
3. 优先用 QMutexLocker 或标准库 RAII 锁，避免提前返回和异常导致漏解锁。
4. QMutex 非递归；重复加锁通常提示函数分层或锁职责需要重构。
5. Qt 的负毫秒超时表示无限等待，而标准库负 duration 表示立即尝试。
6. 持锁期间避免 I/O、sleep、跨线程阻塞调用和未知回调。
7. 多锁代码必须采用一致顺序，必要时使用 `std::scoped_lock`。
8. 不要返回受保护对象的裸引用或指针，让访问逃离锁的生命周期。
9. mutex 不能改变 QObject 的线程亲和性，也不能代替对象生命周期管理。
10. 线程退出协议必须先避免持有其所需的锁，再等待线程完成。
