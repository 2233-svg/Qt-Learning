# Qt QReadWriteLock 深入笔记：并发读、独占写、递归与饥饿控制

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QReadWriteLock>`  
> 所属模块：`Qt6::Core`  
> 定位：允许多个读者并发访问，但写者必须独占访问

`QReadWriteLock` 把临界区分为读模式和写模式。只读线程之间可以并发；任何写线程都必须等待所有读者和其他写者离开。它适合“读明显多于写、读临界区有实际耗时”的共享数据，并不保证一定比 QMutex 快。

## 1. CMake 与最小可用代码

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QHash>
#include <QReadLocker>
#include <QReadWriteLock>
#include <QWriteLocker>

class UserCache
{
public:
    QString find(int id) const
    {
        QReadLocker locker(&m_lock);
        return m_users.value(id);
    }

    void insert(int id, QString name)
    {
        QWriteLocker locker(&m_lock);
        m_users.insert(id, std::move(name));
    }

private:
    mutable QReadWriteLock m_lock;
    QHash<int, QString> m_users;
};
```

返回值使用副本，使调用者在读锁释放后仍可安全使用。不要返回容器元素引用或迭代器，让它们逃出锁的作用域。

## 2. 状态模型

```text
未锁定
├─ 多个 Reader 可同时进入：R1 + R2 + R3
└─ 一个 Writer 可独占进入：W

有 Reader 时：新 Writer 等待
有 Writer 时：所有 Reader 和其他 Writer 等待
```

读锁表示“本线程只观察受保护状态”。只要任何持有读锁的代码修改共享状态，就破坏了读者并发安全。

`mutable` cache、惰性初始化和访问计数虽然可能出现在 const 函数内，但仍是写入，应使用写锁，或改用独立同步机制。

## 3. 何时比 QMutex 合适

读写锁有更多状态管理成本。它通常在以下条件同时成立时才有优势：

- 读操作远多于写操作；
- 多线程确实会同时读取；
- 每次读取不是短到只访问一个整数；
- 读取不会修改内部缓存；
- 写锁不会被长期持有；
- 实际测量显示互斥锁已成为瓶颈。

若读操作很短，QMutex 的低开销可能更快；若写很多，读者仍频繁被阻塞；若数据本就可复制成不可变快照，消息传递可能更简单。

## 4. 构造与 `RecursionMode`

```cpp
QReadWriteLock lock; // 默认 NonRecursive
```

枚举：

```cpp
enum QReadWriteLock::RecursionMode {
    Recursive,
    NonRecursive
};
```

可显式启用递归：

```cpp
QReadWriteLock lock(QReadWriteLock::Recursive);
```

`NonRecursive` 下，同一线程只能取得一次该锁。`Recursive` 下，同线程可以用相同模式重复加锁，每次都必须有对应的 `unlock()`。

递归模式仍不允许改变锁类型：

```cpp
lock.lockForRead();
lock.lockForWrite(); // 不允许从读升级到写
```

```cpp
lock.lockForWrite();
lock.lockForRead();  // 不允许从写降级到读
```

即使启用了 Recursive，也只能 read -> read 或 write -> write。

## 5. `lockForRead()`

```cpp
lock.lockForRead();
Snapshot value = readSharedState();
lock.unlock();
```

若没有写者持锁，并且没有因公平策略应先运行的等待写者，读者可以取得锁。多个读者能并发运行。

优先使用 RAII：

```cpp
QReadLocker locker(&lock);
return makeSnapshot();
```

读锁内应避免：

- 修改受保护容器；
- 调用逻辑上 const、内部却写 cache 的函数；
- 长时间 I/O 或 sleep；
- 返回指向内部数据的引用、指针或迭代器；
- 调用未知回调，让其尝试写锁。

## 6. `lockForWrite()`

```cpp
lock.lockForWrite();
updateSharedState();
lock.unlock();
```

写锁要求完全独占：已有任意读锁或写锁时都会等待。在默认非递归模式下，当前线程自己已有读/写锁也会阻塞。

```cpp
QWriteLocker locker(&lock);
updateSharedState();
```

写临界区应保持短小。可先在锁外完成纯计算，再在锁内验证版本并提交结果：

```cpp
Result result = expensiveCalculation(input);

{
    QWriteLocker locker(&m_lock);
    if (m_version != expectedVersion)
        return false;
    m_result = std::move(result);
    ++m_version;
}
```

## 7. 写者优先与饥饿控制

如果读请求持续不断，朴素读写锁可能让写者永远等不到“读者数量变成零”。QReadWriteLock 为等待写者提供优先：

- 一旦有写者阻塞等待，后来的读者不会继续成功插队，即使当前只是其他读者持锁；
- 当前由写者持锁时，另一个等待写者优先于同时等待的读者。

这避免写者无限饥饿，但意味着读请求延迟可能因写者队列增大。Qt 没有承诺严格 FIFO 次序，业务不能依赖某个等待者精确排第几。

## 8. `tryLockForRead()`

### 8.1 毫秒超时

```cpp
if (lock.tryLockForRead(20)) {
    Snapshot s = readState();
    lock.unlock();
}
```

最多等待 `timeout` 毫秒。负数等价于 `lockForRead()`，即无限等待；0 表示立即尝试。只有返回 true 才需要解锁。

### 8.2 截止时间（Qt 6.6）

```cpp
if (lock.tryLockForRead(QDeadlineTimer(100))) {
    Snapshot s = readState();
    lock.unlock();
}
```

签名的 deadline 参数默认 `{}`，所以也可无参数立即尝试：

```cpp
bool acquired = lock.tryLockForRead();
```

QDeadlineTimer 适合把同一个总时间预算传给多步操作，避免每一步重新获得完整超时。

## 9. `tryLockForWrite()`

### 9.1 毫秒超时

```cpp
if (lock.tryLockForWrite(50)) {
    updateState();
    lock.unlock();
} else {
    deferUpdate();
}
```

负 timeout 无限等待，0 立即尝试。超时返回 false 只表示没有取得锁，不会取消其他线程或预留未来写权限。

### 9.2 截止时间（Qt 6.6）

```cpp
QDeadlineTimer deadline(250);
if (!lock.tryLockForWrite(deadline))
    return false;

updateState();
lock.unlock();
```

无参数 `tryLockForWrite()` 使用默认过期 deadline，可立即尝试。

手工成功路径容易漏解锁。QReadLocker/QWriteLocker 没有 adopt-lock 构造函数；如果需要超时 + RAII，可在成功后使用 scope guard，或封装一个明确拥有已取得锁的辅助类型。

## 10. `unlock()`

同一个接口释放读锁或写锁，QReadWriteLock 根据当前线程的持有状态处理：

```cpp
lock.lockForRead();
lock.unlock();

lock.lockForWrite();
lock.unlock();
```

对未锁定的 QReadWriteLock 调用 `unlock()` 是错误，Qt 文档明确指出会导致程序终止。成功的每次 `lock...` / `tryLock...` 都必须恰好对应一次 unlock。

锁对象必须比所有使用者活得久；析构前应停止并等待访问线程。

## 11. 不支持原子升级与降级

### 11.1 升级陷阱

```cpp
QReadLocker readLocker(&m_lock);
if (!contains(key)) {
    QWriteLocker writeLocker(&m_lock); // 当前读锁未释放，自死锁
    insert(key);
}
```

正确做法是释放读锁，再取写锁，并重新检查条件：

```cpp
{
    QReadLocker readLocker(&m_lock);
    if (m_data.contains(key))
        return m_data.value(key);
}

QWriteLocker writeLocker(&m_lock);
if (!m_data.contains(key)) // 必须重查，空窗期可能已有线程插入
    m_data.insert(key, createValue(key));
return m_data.value(key);
```

从释放读锁到取得写锁之间不是原子升级，任何状态都可能变化。

### 11.2 降级

写锁也不能在保持连续所有权的同时转成读锁。释放写锁再取得读锁之间同样存在空窗。需要连续观察时，在写锁内复制快照，然后释放锁使用快照。

## 12. 递归模式的细节

```cpp
QReadWriteLock lock(QReadWriteLock::Recursive);

lock.lockForRead();
lock.lockForRead();
lock.unlock();
lock.unlock();
```

递归读锁和递归写锁都按调用次数计数。少解锁一次，其他模式的等待者就可能永久阻塞。

递归模式解决的是同一线程、同一种锁模式的嵌套调用，不解决：

- read -> write 升级；
- write -> read 降级；
- 不同线程之间的锁交接；
- 多把锁顺序反转；
- 持锁回调看到半完成状态。

与 QRecursiveMutex 相同，优先拆出 `fooLocked()` 私有实现，让 public 入口只加锁一次。

## 13. 安全返回数据

错误：

```cpp
const Value &Cache::find(Key key) const
{
    QReadLocker locker(&m_lock);
    return m_data[key]; // 返回后锁释放，引用可能失效
}
```

返回副本：

```cpp
std::optional<Value> Cache::find(Key key) const
{
    QReadLocker locker(&m_lock);
    auto it = m_data.constFind(key);
    if (it == m_data.cend())
        return std::nullopt;
    return *it;
}
```

对于大对象，可使用不可变共享快照（例如 `std::shared_ptr<const Data>`），在写锁内替换快照指针，让读者在锁外安全消费自己的共享引用。

## 14. 与 QWaitCondition 的关系

QWaitCondition 可以等待 QReadWriteLock，但传入时必须不是递归锁；若递归锁被持有，wait 会立即返回。条件等待的状态协议通常使用 QMutex 更直观。

等待期间 QWaitCondition 会释放锁并在返回前重新取得。若使用读写锁，需要明确当前持有模式和被保护条件，避免多个读者都在等待一个只有写者能改变的条件时形成复杂调度。

## 15. 性能测量

读写锁提高的是“读临界区可重叠程度”，不是让单次读更便宜。测量时关注：

- 读/写比例；
- 临界区持续时间；
- 同时读线程数量；
- 写者等待时长；
- cache line 和共享容器本身的扩展性；
- 锁外计算是否还能进一步增加；
- 是否因写者优先导致尾部读延迟。

如果一个简单 QMutex 已足够快，它通常更容易推理和维护。

## 16. 常见错误

### 错误 1：const 函数一律使用读锁

逻辑 const 函数可能更新 cache、统计或惰性字段。只要修改受保护状态就需要写锁或独立同步。

### 错误 2：在读锁内尝试写锁

QReadWriteLock 不支持升级，Recursive 模式也不支持。释放、重取并重新验证条件。

### 错误 3：返回内部引用或迭代器

锁释放后写线程可使它失效。返回值快照或不可变共享对象。

### 错误 4：认为读写锁必然比 mutex 快

短读、频繁写、低并发时管理成本可能更高。以基准测量决定。

### 错误 5：递归模式混合 read/write

递归只允许相同模式重复取得，不能转换锁类型。

### 错误 6：持锁调用未知代码

回调可能再次加锁或形成跨对象锁环。锁内只操作明确受控的数据。

## API 速查表
读写锁最容易被误用的地方是把“读多写少”当成充分理由。查表前先确定读操作是否真的不改共享状态、是否需要安全快照，以及是否会发生读锁到写锁的升级；后两者往往决定该不该使用 `QReadWriteLock`。

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举 | `enum RecursionMode { NonRecursive, Recursive }` | 选择同一线程是否可以以相同模式重复取得锁。 | 默认 `NonRecursive`；递归模式不能把读锁升级成写锁，也不能把写锁降级成读锁。 |
| 构造 | `QReadWriteLock(RecursionMode recursionMode = NonRecursive)` | 创建读写锁并确定递归策略。 | 模式在构造时决定；锁对象必须覆盖所有访问线程的生命周期。 |
| 析构 | `~QReadWriteLock()` | 销毁读写锁。 | 必须先停止并等待所有访问者，且不能仍有读锁/写锁持有；否则行为未定义。 |
| 阻塞读锁 | `lockForRead()` | 阻塞直到取得共享读锁。 | 多个读者可以并发；已有等待写者时新读者可能被挡住，避免写者饥饿。 |
| 阻塞写锁 | `lockForWrite()` | 阻塞直到取得独占写锁。 | 必须等所有读者和写者离开；持锁期间应只做短小状态提交。 |
| 立即读尝试 | `tryLockForRead()` | 立即尝试取得读锁，失败马上返回 false。 | 只有返回 true 才需要 `unlock()`；适合不愿阻塞的可选读取。 |
| 毫秒读尝试 | `tryLockForRead(int timeout)` | 最多等待指定毫秒取得读锁。 | `timeout < 0` 表示无限等待，`0` 表示立即尝试；这是 Qt 风格的负值语义。 |
| deadline 读尝试 | `tryLockForRead(QDeadlineTimer timeout)` | 在绝对截止时间前尝试取得读锁。 | 默认构造 deadline 已过期，所以无参数调用表现为立即尝试；适合跨多步共享总预算。 |
| 立即写尝试 | `tryLockForWrite()` | 立即尝试取得独占写锁。 | 失败不代表未来不会成功，只表示这次没有取得；不要继续修改共享状态。 |
| 毫秒写尝试 | `tryLockForWrite(int timeout)` | 最多等待指定毫秒取得写锁。 | 负值无限等待、0 立即尝试；返回 true 后必须恰好 unlock 一次。 |
| deadline 写尝试 | `tryLockForWrite(QDeadlineTimer timeout)` | 在绝对截止时间前尝试取得写锁。 | deadline 贯穿调用链时不要每层重置；默认 deadline 表示立即尝试。 |
| 解锁 | `unlock()` | 释放当前线程持有的读锁或写锁。 | 每次成功 lock/tryLock 都必须对应一次；未锁定时调用是错误，Qt 文档要求避免。 |
| 标准读写接口 | `lock()` / `lock_shared()` / `try_lock()` / `try_lock_shared()` | 提供标准库 `shared_mutex` 风格的兼容入口。 | `lock()` 等价写锁，`lock_shared()` 等价读锁；使用标准包装器时保持同一所有权协议。 |
| 标准解锁 | `unlock_shared()` | 释放标准库语义下的共享读锁。 | 和 `unlock()` 一样必须由正确的持有线程调用。 |
| RAII 读锁 | `QReadLocker` | 作用域内自动取得/释放读锁。 | 没有超时构造；需要限时先用 tryLock，再使用明确的 scope guard。 |
| RAII 写锁 | `QWriteLocker` | 作用域内自动取得/释放写锁。 | 不提供事务回滚，也没有读写升级能力。 |

## 18. 总结

1. QReadWriteLock 允许并发读，但写操作必须独占。
2. 只有在读多写少、读临界区足够大且存在真实并发时，它才可能优于 QMutex。
3. Qt 优先已等待的写者，避免持续新读者让写者永久饥饿。
4. 读锁内不能修改共享状态，逻辑 const 也要检查隐式写入。
5. 不支持读写锁原子升级或降级，释放后重取必须重新验证状态。
6. Recursive 仅允许同线程以相同模式重复取得，并要求等次数解锁。
7. 截止时间重载适合共享总预算，旧式负毫秒表示无限等待。
8. 返回共享数据应使用副本或不可变快照，不让引用、指针和迭代器逃出锁。
9. 优先使用 QReadLocker/QWriteLocker 管理普通加锁路径。
10. 锁选择应依据测量与不变量复杂度，而不是只依据“读操作看起来很多”。
