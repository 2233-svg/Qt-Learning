# Qt QMutexLocker 深入笔记：RAII 锁管理、移动语义与条件等待

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QMutexLocker>`  
> 所属模块：`Qt6::Core`  
> 声明形式：`template <typename Mutex> class QMutexLocker`  
> 定位：在作用域内自动取得并释放 QMutex 或 QRecursiveMutex

`QMutexLocker` 把一次 mutex 所有权绑定到 C++ 对象生命周期：构造时加锁，析构时若仍持锁就解锁。这是 RAII（Resource Acquisition Is Initialization）在互斥锁上的应用，能覆盖普通返回、提前返回和异常退出。

## 1. CMake 与最小可用代码

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QMutex>
#include <QMutexLocker>

class Counter
{
public:
    void increment()
    {
        QMutexLocker locker(&m_mutex);
        ++m_value;
    } // 自动 unlock

    int value() const
    {
        QMutexLocker locker(&m_mutex);
        return m_value; // return 之前 locker 析构并解锁
    }

private:
    mutable QMutex m_mutex;
    int m_value = 0;
};
```

Qt 6 支持类模板实参推导，`QMutexLocker locker(&m_mutex)` 会推导为 `QMutexLocker<QMutex>`。也可以显式写出模板参数。

## 2. 为什么 RAII 比手工解锁可靠

手工代码必须照顾每一个出口：

```cpp
mutex.lock();

if (!validate()) {
    mutex.unlock();
    return false;
}

if (!commit()) {
    mutex.unlock();
    return false;
}

mutex.unlock();
return true;
```

使用 locker 后只有一个所有权对象：

```cpp
QMutexLocker locker(&mutex);

if (!validate())
    return false;

if (!commit())
    return false;

return true;
```

当栈展开时，局部对象总会析构。异常也同样适用：

```cpp
void Repository::update()
{
    QMutexLocker locker(&m_mutex);
    mutate(); // 即使抛异常，locker 析构仍会解锁
}
```

RAII 只保证锁的取得/释放成对，不保证临界区逻辑正确，也不能自动避免多锁死锁。

## 3. 构造函数与支持的 mutex

```cpp
QMutexLocker<QMutex> locker(&mutex);
QMutexLocker<QRecursiveMutex> recursiveLocker(&recursiveMutex);
```

模板参数需要提供兼容的 `lock()` 和 `unlock()`。最常见的是 QMutex 与 QRecursiveMutex。

构造函数立即调用传入 mutex 的 `lock()`，因此本身可能阻塞：

```cpp
QMutexLocker locker(&mutex); // 临界区从这一行开始
```

它没有超时构造函数。需要超时获取时，可先 `tryLock()`，然后使用支持 adopt-lock 的标准库 `std::unique_lock`，或用明确的 scope guard；不能在已手工加锁后再构造普通 QMutexLocker，否则会再次加锁。

## 4. 传入 `nullptr`

```cpp
QMutexLocker<QMutex> locker(nullptr);
```

传空指针时什么也不做，析构也不会解锁。这允许可选同步：

```cpp
QMutexLocker locker(threadSafe ? &m_mutex : nullptr);
performOperation();
```

但这种模式会让函数的线程安全属性依赖运行时条件，审查更困难。除非对象明确支持“外部已经串行化”的模式，否则不要为省一次锁引入可选 mutex。

```cpp
locker.mutex();    // nullptr
locker.isLocked(); // false，Qt 6.4 起
```

## 5. 析构行为

```cpp
{
    QMutexLocker locker(&mutex);
    update();
} // 若 locker 仍处于 locked 状态，此处自动 unlock
```

如果之前调用过 `locker.unlock()` 且没有 relock，析构时不会再次解锁。因此 locker 内部不仅保存 mutex 指针，也保存自己是否仍持锁的状态。

mutex 必须比 locker 活得更久：

```cpp
QMutexLocker<QMutex> *bad;
{
    QMutex mutex;
    bad = new QMutexLocker(&mutex);
} // mutex 已销毁，bad 保存悬空指针
delete bad; // 错误
```

正常的局部声明顺序自然满足：mutex 是类成员，locker 是成员函数局部变量。

## 6. `unlock()` 与 `relock()`

### 6.1 暂时释放

```cpp
QMutexLocker locker(&m_mutex);
Snapshot snapshot = makeSnapshotLocked();

locker.unlock();
performSlowIo(snapshot);

locker.relock();
mergeResultLocked(snapshot);
```

`unlock()` 释放关联 mutex，并把 locker 标记为未持锁；`relock()` 再次调用 mutex 的 `lock()`，可能阻塞。

释放期间，共享状态可能已被其他线程修改。因此 relock 后不能沿用旧假设：

```cpp
QMutexLocker locker(&m_mutex);
int version = m_version;
locker.unlock();

Result result = calculate();

locker.relock();
if (m_version != version)
    return; // 旧计算基础已失效
m_result = std::move(result);
```

### 6.2 更清晰的嵌套作用域

若后面无需重新加锁，优先缩小 scope：

```cpp
Snapshot snapshot;
{
    QMutexLocker locker(&m_mutex);
    snapshot = makeSnapshotLocked();
}

performSlowIo(snapshot);
```

这使“当前是否持锁”可由花括号直接看出。unlock/relock 适合必须把同一个 locker 传给条件等待或一个连续算法的情况。

### 6.3 非法状态操作

不要在已经 unlock 的 locker 上再次 unlock，也不要在仍 locked 时调用 relock；它们会把底层 mutex 带入错误操作或自死锁。可用 `isLocked()` 做断言，但更应让控制流本身清晰。

## 7. `isLocked()`（Qt 6.4）

```cpp
QMutexLocker locker(&mutex);
Q_ASSERT(locker.isLocked());

locker.unlock();
Q_ASSERT(!locker.isLocked());
```

它报告“这个 locker 当前是否管理着一次锁定”，不是查询 mutex 是否被任意线程锁住。mutex 通常也不提供可靠的全局 `isLocked()`，因为查询结果会立刻过时。

move 之后，源 locker 不再管理 mutex，`isLocked()` 返回 false。

## 8. `mutex()`

```cpp
QMutex *ptr = locker.mutex();
```

返回构造时关联的 mutex 指针。主要用途是传给需要原始 mutex 的 API，典型代表 QWaitCondition：

```cpp
QMutexLocker locker(&m_mutex);

while (m_queue.isEmpty() && !m_stopping)
    m_notEmpty.wait(locker.mutex());

if (!m_queue.isEmpty())
    consume(m_queue.dequeue());
```

`wait()` 会原子地释放 mutex 并让线程休眠；被唤醒后，在返回前重新取得同一 mutex。对调用者而言，`wait()` 返回时 locker 仍然处于持锁状态。

必须用 `while` 重查条件，而不是 `if`：唤醒可能是伪唤醒，条件也可能先被其他线程消耗。

不要把 `mutex()` 返回的指针保存到超过 locker 或底层 mutex 生命周期的位置。它不转移所有权。

## 9. 移动构造（Qt 6.4）

```cpp
QMutexLocker<QMutex> first(&mutex);
QMutexLocker<QMutex> second(std::move(first));

Q_ASSERT(!first.isLocked());
Q_ASSERT(second.isLocked());
```

移动会把 mutex 指针和 locked/unlocked 状态转给目标。源对象变成不管理任何 mutex 的状态，析构时不会解锁。

这允许从工厂函数返回 locker：

```cpp
QMutexLocker<QMutex> State::lock()
{
    return QMutexLocker<QMutex>(&m_mutex);
}
```

但把锁所有权隐藏在返回值中容易扩大临界区，API 必须明确说明调用者得到的是一个活动锁。

QMutexLocker 不可复制。若能复制，两份对象都会认为自己应解锁同一次所有权，必然出错。

## 10. 移动赋值（Qt 6.4）

```cpp
QMutexLocker<QMutex> first(&mutexA);
QMutexLocker<QMutex> second(&mutexB);

second = std::move(first);
```

若 `second` 原先持锁，移动赋值先释放它管理的 `mutexB`，再接管 `first` 的 mutex 和状态。赋值后 first 不再管理任何 mutex。

移动赋值可能在并发协议中改变锁释放顺序，不应为了“少写一个变量”随意使用。让 locker 保持短生命周期通常更容易审查。

## 11. `swap()`（Qt 6.4）

```cpp
first.swap(second);
```

交换两个 locker 的 mutex 指针和锁定状态，操作很快且不失败。它不会额外 lock 或 unlock。

`swap()` 主要服务泛型代码和移动实现。业务代码中频繁交换锁拥有者会使锁顺序难以理解；应有明确理由和注释。

## 12. 条件变量中的标准模式

生产者：

```cpp
void Queue::push(Item item)
{
    {
        QMutexLocker locker(&m_mutex);
        m_items.enqueue(std::move(item));
    }
    m_notEmpty.wakeOne();
}
```

消费者：

```cpp
std::optional<Item> Queue::take(QDeadlineTimer deadline)
{
    QMutexLocker locker(&m_mutex);

    while (m_items.isEmpty() && !m_closed) {
        if (!m_notEmpty.wait(locker.mutex(), deadline))
            return std::nullopt;
    }

    if (m_items.isEmpty())
        return std::nullopt;

    return m_items.dequeue();
}
```

判断条件和进入等待必须使用同一 mutex，QWaitCondition 才能原子释放锁并避免“检查为空后、真正睡眠前恰好错过通知”的丢失唤醒。

## 13. 与标准库锁包装器比较

| 包装器 | 主要能力 |
|---|---|
| `QMutexLocker<Mutex>` | Qt 风格，支持 unlock/relock、mutex 指针、移动 |
| `std::lock_guard<Mutex>` | 最简单的整段作用域锁，不能主动 unlock |
| `std::unique_lock<Mutex>` | 延迟、尝试、超时、adopt、移动，状态更丰富 |
| `std::scoped_lock<...>` | 一次管理一把或多把锁，适合避免多锁顺序问题 |

QMutex 兼容标准 Lockable 接口，因此这些标准包装器可以直接使用。QWaitCondition 需要 QMutex 指针时，QMutexLocker 更自然；超时取得锁或多锁时，标准包装器可能更合适。

## 14. 常见错误

### 错误 1：构造 locker 前已经手工加锁

```cpp
mutex.lock();
QMutexLocker locker(&mutex); // QMutex 自死锁
```

QMutexLocker 没有 adopt-lock 构造语义。让它从一开始负责取得锁，或使用 `std::unique_lock(..., std::adopt_lock)` 接管既有锁。

### 错误 2：手工解锁底层 mutex

```cpp
QMutexLocker locker(&mutex);
mutex.unlock(); // locker 仍以为自己持锁，析构会再次 unlock
```

需要提前释放时调用 `locker.unlock()`，让包装器状态同步变化。

### 错误 3：locker 生命周期大于 mutex

析构时会访问悬空 mutex 指针。底层 mutex 必须先构造、后销毁。

### 错误 4：unlock 后继续依赖旧状态

其他线程可能在空窗期修改数据。relock 后重新验证版本、条件和迭代器。

### 错误 5：把 `isLocked()` 当成全局查询

它只说明该 locker 自己的状态，不说明其他 locker 或线程。

### 错误 6：持锁发信号或调用未知回调

RAII 不会防止重入和锁顺序反转。锁内只做受控、短小的状态操作，通知通常放在解锁之后。

## API 速查表
`QMutexLocker` 的重点不是“替 mutex 写几个转发函数”，而是让临界区和 C++ 作用域绑定。查表时优先确认 locker 当前是否持锁、底层锁是否仍存活，以及临时 `unlock()` 后由谁负责恢复保护。

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 模板 | `template <typename Mutex> class QMutexLocker` | 为兼容 `lock()`/`unlock()` 的 mutex 类型提供 RAII 锁管理。 | 最常见模板参数是 `QMutex` 和 `QRecursiveMutex`；它不是独立同步原语。 |
| 构造 | `QMutexLocker(Mutex *mutex)` | 构造时立即对传入 mutex 调用 `lock()`。 | 构造本身可能阻塞；传 `nullptr` 时不加锁、不解锁。 |
| 析构 | `~QMutexLocker()` | 析构时如果仍持锁就自动解锁。 | 底层 mutex 必须比 locker 活得久；不要手工操作底层 mutex 破坏 locker 状态。 |
| 移动构造 | `QMutexLocker(QMutexLocker &&other)` | 接管另一个 locker 的 mutex 指针和持锁状态。 | 源 locker 变为空且不再解锁；Qt 6.4 起支持。 |
| 移动赋值 | `operator=(QMutexLocker &&other)` | 释放目标原先持有的锁，再接管源 locker 状态。 | 会改变目标旧锁释放时机；不要为简短写法让锁顺序变得难审查。 |
| 禁止复制 | `Q_DISABLE_COPY(QMutexLocker)` | 禁止复制锁所有权对象。 | 复制会导致多个对象以为自己负责同一次 unlock，因此被禁止。 |
| 提前释放 | `unlock()` | 释放当前 locker 管理的锁，并把内部状态改为未持锁。 | 需要提前解锁时调用它，不要直接调用 `mutex->unlock()`。 |
| 重新加锁 | `relock()` | 对关联 mutex 再次调用 `lock()`，恢复持锁状态。 | 只能在已 unlock 状态使用；空窗期内共享状态可能已变化，需重新验证条件。 |
| 状态查询 | `isLocked()` | 查询这个 locker 当前是否持有锁。 | 只描述 locker 自己的状态，不是 mutex 的全局“是否被任意线程锁住”。 |
| 底层指针 | `mutex()` | 返回 locker 关联的 mutex 指针。 | 不转移所有权；常用于 `QWaitCondition::wait(locker.mutex())`。 |
| 交换 | `swap(QMutexLocker &other)` | 交换两个 locker 的底层指针和持锁状态。 | 不额外 lock/unlock；业务代码频繁交换锁拥有者会降低可读性。 |
| 条件等待 | 与 `QWaitCondition::wait()` 配合 | 让条件等待原子释放 mutex 并在返回前重新加锁。 | wait 后要用 `while` 重查条件；locker 返回时仍表示持锁状态。 |
| 取舍 | 与 `std::unique_lock` 对比 | Qt 风格更适合 QWaitCondition，标准库更适合超时/adopt/multi-lock。 | QMutexLocker 没有 adopt-lock 和超时构造；已手工加锁后不要再构造普通 locker。 |

## 16. 总结

1. QMutexLocker 用 RAII 保证每次取得的锁在所有退出路径上释放。
2. 构造时立即加锁，析构时只在仍持锁的情况下解锁。
3. Qt 6 可自动推导 QMutex 或 QRecursiveMutex 模板参数。
4. 传 nullptr 会得到不管理锁的 locker，但可选同步应谨慎使用。
5. 提前释放必须调用 locker 自己的 `unlock()`，随后可用 `relock()`。
6. 解锁空窗期后原有条件可能失效，重新加锁必须重新验证。
7. `mutex()` 主要用于 QWaitCondition；wait 返回时锁已重新取得。
8. Qt 6.4 起 locker 可移动、查询状态和 swap，源对象移动后不再持锁。
9. QMutexLocker 没有 adopt-lock 或超时构造，相关需求可使用标准库包装器。
10. RAII 解决的是成对释放，不会自动解决临界区过大、危险回调或多锁死锁。
