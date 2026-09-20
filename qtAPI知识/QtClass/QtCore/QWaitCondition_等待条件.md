# Qt QWaitCondition：用条件变量协调“状态何时成立”

`QWaitCondition` 是 Qt 的条件变量。它让一个线程在某个共享状态尚未满足时释放锁并休眠，另一个线程更新状态后唤醒等待者。它用于生产者/消费者队列、后台任务完成通知、资源池容量控制、线程退出协调等场景。

条件变量本身不保存“通知次数”或“事件已经发生”的状态。可靠代码必须另有一个受同一把锁保护的谓词，例如 `!queue.isEmpty()`、`stopped` 或 `available > 0`；等待方始终在 `while` 循环中检查谓词。

```cpp
#include <QMutex>
#include <QMutexLocker>
#include <QWaitCondition>

QMutex mutex;
QWaitCondition notEmpty;
QQueue<Job> jobs;
bool stopping = false;

bool takeJob(Job *out)
{
    QMutexLocker lock(&mutex);
    while (jobs.isEmpty() && !stopping)
        notEmpty.wait(&mutex);

    if (stopping)
        return false;

    *out = jobs.dequeue();
    return true;
}

void submit(Job job)
{
    QMutexLocker lock(&mutex);
    jobs.enqueue(std::move(job));
    notEmpty.wakeOne();
}
```

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QWaitCondition>`  
> CMake：`Qt6::Core`  
> 线程：所有成员函数线程安全；对象不可复制；本身没有 QObject 线程归属。

## 它解决什么问题

轮询共享状态会浪费 CPU：

```cpp
while (queue.isEmpty())
    QThread::msleep(1);
```

这种方式既不及时，也不能原子地处理“检查为空”和“开始等待”之间的竞态。若生产者恰好在检查后、休眠前写入并通知，消费者可能错过通知并无谓地睡很久。

`wait()` 的核心承诺是原子地完成：

1. 调用线程已经持有互斥量；
2. 释放该锁；
3. 进入条件变量的等待集合；
4. 被唤醒或超时后，重新以相同锁定状态拿回锁；
5. 返回给调用者。

因此生产者与消费者要用**同一把锁**保护共享谓词：消费者在锁内检查后等待，生产者在锁内改变谓词后唤醒。这样不会在“检查”和“入睡”之间丢失状态变化。

## 正确模型：谓词是事实，唤醒只是提醒

不要把 `wakeOne()` / `wakeAll()` 当成可累积的消息队列：

- 没有线程正在等待时，唤醒不会为将来的 `wait()` 留下一张“通知票”；
- `wakeOne()` 选中的线程由操作系统调度决定，不能指定哪一个；
- `wakeAll()` 唤醒后的线程还要竞争锁，且不保证唤醒顺序；
- 条件变量等待可能被非预期唤醒，或者唤醒后条件已被其他线程先消耗。

所以应写成：

```cpp
QMutexLocker lock(&mutex);
while (!ready && !cancelled) {
    if (!readyChanged.wait(&mutex, deadline))
        return false; // 超时后仍在锁内，可按业务再次检查状态
}

return ready;
```

不能写成：

```cpp
mutex.lock();
readyChanged.wait(&mutex);
useResource(); // 错：没有再次检查 ready
mutex.unlock();
```

`while` 既处理虚假/竞争性唤醒，也处理多个线程被唤醒后只有一个能取得资源的情况。谓词变量必须只在同一把锁保护下读写；否则 `QWaitCondition` 无法修复数据竞争。

## `wakeOne()` 还是 `wakeAll()`

当一次状态变化只增加一个可消费资源，例如队列新增一个任务、连接池归还一个连接，通常使用 `wakeOne()`：

```cpp
{
    QMutexLocker lock(&mutex);
    ++available;
    resourceAvailable.wakeOne();
}
```

当状态变化可能让多个线程都继续，例如停止标志变为真、应用即将退出、配置整体刷新时，使用 `wakeAll()`：

```cpp
{
    QMutexLocker lock(&mutex);
    stopping = true;
    changed.wakeAll();
}
```

`wakeAll()` 不是“让所有人立刻执行”。所有被唤醒的线程都要重新获得同一把锁，并重新检查谓词；如果只一个线程能消费状态，其余线程会继续等待。这种竞争会造成惊群，资源只有一个时优先用 `wakeOne()`。

是否一定要持锁调用 `wakeOne()` / `wakeAll()` 取决于更大的同步设计，但实务上推荐在更新谓词的同一临界区内唤醒：读者更容易看出状态和通知不可分离，也能避免不正确的“先通知、后更新”设计。真正的正确性条件是更新谓词和等待方检查谓词必须由同一把锁串行化。

## 等待锁和超时语义

`wait()` 有 `QMutex *` 与 `QReadWriteLock *` 两组重载。两者都要求锁由**当前调用线程**先成功锁定；返回时，锁已经恢复到调用前的锁定状态，调用者仍然在临界区内。

```cpp
QMutexLocker lock(&mutex);
const bool signaled = condition.wait(&mutex, QDeadlineTimer(500));
// mutex 此处仍被 lock 持有
```

建议优先使用 `QDeadlineTimer` 重载：

```cpp
const QDeadlineTimer deadline(1500); // 从现在起最多约 1.5 秒
while (!ready) {
    if (!condition.wait(&mutex, deadline))
        break;
}
```

它可表达一个绝对截止点，多个循环共用同一个 deadline 时不会因每轮重新计算超时而无限延长总等待。默认参数为 `QDeadlineTimer::Forever`，即永不超时，直到有唤醒发生。

`unsigned long time` 重载以毫秒表示相对等待时间，保留主要为了兼容旧调用。两种重载的返回值约定相同：被 `wakeOne()` / `wakeAll()` 唤醒返回 `true`，截止时间到达返回 `false`。返回 `true` **不等于谓词必然成立**，仍要在锁内重查。

### `QMutex` 的特殊限制

传给 `wait(QMutex *)` 的锁必须已锁定。若未锁定，行为未定义。若它是递归互斥量，`wait()` 会立即返回，不会形成真正等待；因此不要把递归 `QMutex` 用作等待条件的常规保护锁。

### `QReadWriteLock` 的特殊限制

传给 `wait(QReadWriteLock *)` 的锁也必须由当前线程持有。若锁根本未锁定，该重载会立即返回；若递归持有，Qt 无法正确完全释放它，文档明确不支持这种用法。对可等待谓词通常选普通 `QMutex` 最清晰；只有确实需要读写锁的共享读模型时再使用该重载。

## 一个有界队列的双条件示例

生产者既要等“有空位”，消费者又要等“有数据”，所以使用两个条件变量：

```cpp
class BoundedQueue
{
public:
    void push(QByteArray value)
    {
        QMutexLocker lock(&m_mutex);
        while (m_items.size() == m_capacity)
            m_notFull.wait(&m_mutex);

        m_items.append(std::move(value));
        m_notEmpty.wakeOne();
    }

    QByteArray pop()
    {
        QMutexLocker lock(&m_mutex);
        while (m_items.isEmpty())
            m_notEmpty.wait(&m_mutex);

        QByteArray value = std::move(m_items.front());
        m_items.pop_front();
        m_notFull.wakeOne();
        return value;
    }

private:
    QMutex m_mutex;
    QWaitCondition m_notEmpty;
    QWaitCondition m_notFull;
    QList<QByteArray> m_items;
    qsizetype m_capacity = 64;
};
```

生产和消费实际实现还应定义关闭语义。比如析构或 `close()` 中设置 `m_closed = true` 并 `wakeAll()`，然后让两侧的 while 条件包含 `!m_closed`；否则线程可能永远停在 `wait()`。

## 生命周期和线程边界

`QWaitCondition` 可以被多个线程同时调用，所有函数线程安全。它不是 `QObject`，不需要事件循环，也不可复制。对象的生命周期必须覆盖所有可能在其上等待或唤醒的线程：销毁前先让工作线程退出并 `join()` / `wait()`，不能在其他线程仍可能调用 `wait()`、`wakeOne()` 或 `wakeAll()` 时析构条件变量。

条件变量不会管理它所接收的 `QMutex` / `QReadWriteLock`，调用方必须保证锁对象也在等待期内有效。退出路径要特别小心：先在锁内设置停止谓词，再 `wakeAll()`，最后等待线程结束。

## API 速查表

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `QWaitCondition()` | 创建条件变量 | 初始没有已保存的通知；需要独立谓词记录状态。 |
| `~QWaitCondition()` | 销毁条件变量 | 先确保没有线程仍可能等待或访问它。 |
| `wait(QMutex *, QDeadlineTimer)` | 释放已锁定 mutex 并等待 | 互斥量必须由当前线程锁定；原子释放/等待，返回前重新锁定。唤醒为 `true`，超时为 `false`。 |
| `wait(QReadWriteLock *, QDeadlineTimer)` | 释放已锁定读写锁并等待 | 锁未锁定会立即返回；递归锁定不支持正确释放。 |
| `wait(QMutex *, unsigned long msecs)` | 按相对毫秒等待 mutex 条件 | 旧式相对超时入口；优先用可复用绝对 deadline。 |
| `wait(QReadWriteLock *, unsigned long msecs)` | 按相对毫秒等待读写锁条件 | 同样恢复原锁定状态；遵守读写锁非递归前置条件。 |
| `wakeOne()` | 唤醒一个等待线程 | 具体线程和恢复顺序不可预测；资源只增加一个时常用。 |
| `wakeAll()` | 唤醒全部等待线程 | 被唤醒者仍竞争锁并重查谓词；用于关闭/全局状态变化。 |
| `notify_one()` | STL 命名的单线程通知 | 等价于 `wakeOne()`。 |
| `notify_all()` | STL 命名的全体通知 | 等价于 `wakeAll()`。 |

---

### 一句话总结

`QWaitCondition` 不是事件计数器，而是“在锁保护的谓词尚不成立时原子释放锁并等待”的工具；用 `while (predicate 不成立) wait()`，更新谓词后再唤醒，才能避免丢通知、竞争唤醒和死锁。
