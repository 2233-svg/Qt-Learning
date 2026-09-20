# Qt Core 进阶：线程与异步（中）——同步原语与线程池

> 适用版本：Qt 6.11.1  
> 所属模块：Qt Core  
> 核心类型：`QMutex`、`QMutexLocker`、`QReadWriteLock`、`QWaitCondition`、`QSemaphore`、`QThreadPool`、`QRunnable`  
> 前置知识：建议先阅读《07_QtCore进阶_线程与异步（上）_QThread与线程归属》。

## 1. 为什么“开了线程”还不够

多个线程只处理各自的数据时，问题通常不大。一旦它们共同读写同一份状态，就可能出现竞态条件。

```cpp
int counter = 0;

// 两个线程同时执行
++counter;
```

`++counter` 并不保证是一个不可分割的操作。它通常包含：

```text
读取 counter
加 1
写回 counter
```

两个线程可能都读到旧值 10，各自算出 11，再都写回 11。执行了两次递增，结果却只增加 1。

更严重的是，无同步的数据竞争在 C++ 内存模型中属于未定义行为。错误不只表现为“少加一次”，编译器优化后可能出现任何结果。

## 2. 先选择更简单的数据设计

同步工具并非第一选择。优先考虑减少共享状态：

1. 输入按值传入工作线程；
2. 每个线程只修改自己的局部数据；
3. 完成后通过信号传回不可变结果；
4. 由单一线程集中拥有和修改某个对象；
5. 只有无法避免的共享可变状态才加锁。

理想结构：

```text
主线程持有 Input
       │ 复制或移动
       ▼
工作线程独占自己的 Input，生成 Result
       │ 信号按值传回
       ▼
主线程接收并更新界面
```

这种消息传递模型更容易推理，也减少死锁风险。

## 3. 构建与头文件

本篇所有类型都属于 Qt Core。

### 3.1 CMake 配置

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

### 3.2 常用头文件

```cpp
#include <QMutex>
#include <QMutexLocker>
#include <QReadWriteLock>
#include <QReadLocker>
#include <QWriteLocker>
#include <QWaitCondition>
#include <QSemaphore>
#include <QThreadPool>
#include <QRunnable>
```

## 4. QMutex：一次只允许一个线程进入

互斥锁保护的是一条**访问规则**：凡是访问某组共享状态的代码，都必须先取得同一把锁。

```cpp
class Counter
{
public:
    void increment()
    {
        mutex_.lock();
        ++value_;
        mutex_.unlock();
    }

    int value() const
    {
        mutex_.lock();
        const int copy = value_;
        mutex_.unlock();
        return copy;
    }

private:
    mutable QMutex mutex_;
    int value_ = 0;
};
```

注意：读操作也要加锁。如果一个线程写、另一个线程无锁读，仍然存在数据竞争。

### 4.1 锁保护数据，不保护函数名字

下面仍然错误：

```cpp
void increment()
{
    QMutex localMutex; // 每次调用都是不同的锁
    QMutexLocker locker(&localMutex);
    ++sharedCounter;
}
```

所有参与者必须锁住同一个、生命周期覆盖共享数据的互斥量。因此通常把锁和数据放在同一个类中。

## 5. QMutexLocker：用作用域自动解锁

手动 `lock()` / `unlock()` 很容易在提前返回、异常或新增分支后漏掉解锁。应优先使用 RAII：

```cpp
void Account::deposit(qint64 amount)
{
    if (amount <= 0)
        return;

    QMutexLocker locker(&mutex_);
    balance_ += amount;
} // locker 析构，自动 unlock
```

它的好处不是少写一行代码，而是把“锁的持有期”绑定到 C++ 作用域。

### 5.1 缩小临界区

不要持锁执行耗时计算、磁盘访问或发出未知接收者的信号：

```cpp
Result Cache::lookup(const QString &key)
{
    Result result;
    {
        QMutexLocker locker(&mutex_);
        result = values_.value(key); // 只复制共享数据
    }

    result.prepareExpensivePreview(); // 解锁后再计算
    return result;
}
```

临界区越短，其他线程等待越少。

### 5.2 临时解锁与重新加锁

```cpp
QMutexLocker locker(&mutex_);
prepareSharedState();

locker.unlock();
performSlowOperation();

locker.relock();
commitSharedState();
```

解锁期间共享状态可能已经变化，因此重新加锁后必须重新验证依赖的条件。

## 6. tryLock 与超时

不希望无限等待时可以尝试加锁：

Qt 6.11 的 `QMutexLocker` 没有“接管一把已锁互斥量”的构造参数。因此，`tryLock()` 成功后应明确配对 `unlock()`：

```cpp
if (mutex_.tryLock(100)) {
    updateState();
    mutex_.unlock();
}
```

Qt 6.6 起还可使用截止时间：

```cpp
if (mutex_.tryLock(QDeadlineTimer(100))) {
    updateState();
    mutex_.unlock();
}
```

需要手动解锁时，把受保护代码压缩到很小的区域，并避免中途 `return`。如果业务允许阻塞取得锁，则直接使用 `QMutexLocker`，让它负责完整的加锁和解锁过程。

## 7. 死锁如何产生

### 7.1 锁顺序相反

线程 A：

```cpp
lockA.lock();
lockB.lock();
```

线程 B：

```cpp
lockB.lock();
lockA.lock();
```

如果 A 拿到 A、B 拿到 B，它们将永久等待对方。

修复方法是定义全局一致的锁顺序，例如任何地方都先锁 A 再锁 B。

### 7.2 持锁发信号

```cpp
QMutexLocker locker(&mutex_);
emit stateChanged();
```

若直接连接的槽回调当前对象并尝试取得同一把非递归锁，就会自锁。稳妥做法：锁内只更新和复制状态，解锁后发信号。

```cpp
State copy;
{
    QMutexLocker locker(&mutex_);
    updateState();
    copy = state_;
}
emit stateChanged(copy);
```

### 7.3 锁内等待另一个线程

如果线程 A 持锁调用 `threadB.wait()`，而 B 结束前还需要同一把锁，两者也会死锁。等待线程结束前应释放与其工作相关的锁。

## 8. QRecursiveMutex：同一线程可重复取得

普通 `QMutex` 默认非递归，同一线程再次锁它会阻塞自己。`QRecursiveMutex` 允许同一线程多次加锁，并要求对应次数的解锁。

```cpp
QRecursiveMutex mutex_;
```

它偶尔用于无法轻易拆分、内部函数会再次进入同一锁的旧代码。但递归锁可能掩盖职责混乱和重入设计问题，而且通常开销更高。优先重构为：

```cpp
void update()
{
    QMutexLocker locker(&mutex_);
    updateUnlocked();
}

void updateUnlocked()
{
    // 要求调用方已经持锁
}
```

## 9. QReadWriteLock：多读单写

如果数据满足“读非常频繁、写较少、读取耗时不可忽略”，读写锁允许多个读线程同时进入，但写线程独占。

```cpp
class Dictionary
{
public:
    QString find(const QString &key) const
    {
        QReadLocker locker(&lock_);
        return words_.value(key);
    }

    void insert(const QString &key, const QString &value)
    {
        QWriteLocker locker(&lock_);
        words_.insert(key, value);
    }

private:
    mutable QReadWriteLock lock_;
    QHash<QString, QString> words_;
};
```

### 9.1 什么时候不值得用

- 临界区极短；
- 写入很多；
- 线程数量很少；
- 数据很小，直接复制快照更简单；
- 需要从读锁升级到写锁。

读写锁的管理成本可能高于普通互斥锁。没有测量证据时，先用 `QMutex`。

### 9.2 不要直接升级锁

持有读锁后再请求写锁可能死锁，因为写锁要等待所有读者退出，其中包括自己。应释放读锁，再取得写锁，并重新验证条件：

```cpp
{
    QReadLocker reader(&lock_);
    if (cache_.contains(key))
        return cache_.value(key);
}

QWriteLocker writer(&lock_);
if (!cache_.contains(key)) // 必须重新检查
    cache_.insert(key, createValue(key));
return cache_.value(key);
```

## 10. QWaitCondition：等待“状态成立”

条件变量用于线程等待某个由共享状态表示的条件，例如“队列非空”。它必须与互斥锁和谓词一起使用。

### 10.1 生产者消费者模型

```cpp
class Queue
{
public:
    void push(QByteArray data)
    {
        {
            QMutexLocker locker(&mutex_);
            queue_.enqueue(std::move(data));
        }
        notEmpty_.wakeOne();
    }

    QByteArray pop()
    {
        QMutexLocker locker(&mutex_);

        while (queue_.isEmpty())
            notEmpty_.wait(locker.mutex());

        return queue_.dequeue();
    }

private:
    QMutex mutex_;
    QWaitCondition notEmpty_;
    QQueue<QByteArray> queue_;
};
```

`wait()` 会以原子方式释放互斥锁并休眠；被唤醒后，它会在返回前重新取得锁。因此生产者能在消费者睡眠期间取得锁并改变队列。

### 10.2 为什么必须用 while

不要写：

```cpp
if (queue_.isEmpty())
    notEmpty_.wait(&mutex_);
```

被唤醒不等于条件一定成立：

- 可能出现无理由唤醒；
- 多个消费者被唤醒后，另一个消费者先取走数据；
- 条件在重新获得锁之前再次变化。

所以标准模式永远是：

```cpp
while (!predicate)
    condition.wait(&mutex);
```

### 10.3 wakeOne 与 wakeAll

- `wakeOne()`：唤醒一个等待者，适合新增一个可消费资源；
- `wakeAll()`：唤醒全部等待者，适合全局状态变化或关闭通知。

唤醒只是通知线程重新竞争锁并检查谓词，不会把某个业务值直接传给它。

### 10.4 支持停止

无限等待的消费者还需要关闭状态：

```cpp
std::optional<QByteArray> pop()
{
    QMutexLocker locker(&mutex_);
    while (queue_.isEmpty() && !stopped_)
        notEmpty_.wait(locker.mutex());

    if (stopped_ && queue_.isEmpty())
        return std::nullopt;

    return queue_.dequeue();
}

void stop()
{
    {
        QMutexLocker locker(&mutex_);
        stopped_ = true;
    }
    notEmpty_.wakeAll();
}
```

仅修改 `stopped_` 而不 `wakeAll()`，已经睡眠的线程可能永远看不到停止状态。

## 11. QSemaphore：管理 N 份资源

互斥锁允许 1 个持有者，信号量允许最多 N 个许可同时被占用。

```cpp
QSemaphore slots(3); // 最多三个并发操作

void upload(const File &file)
{
    slots.acquire();
    sendFile(file);
    slots.release();
}
```

典型用途：

- 限制并发下载数；
- 表示缓冲区中的空槽或已填充槽；
- 管理固定数量的数据库连接；
- 对外部服务做并发限流。

### 11.1 RAII 封装许可

如果函数提前返回，手动 `release()` 容易遗漏。Qt 6.3 起可使用 `QSemaphoreReleaser`：

```cpp
slots.acquire();
QSemaphoreReleaser releaser(&slots);

if (!validate())
    return; // 自动 release

sendFile(file);
```

### 11.2 tryAcquire

```cpp
if (!slots.tryAcquire(1, 200)) {
    reportBusy();
    return;
}
QSemaphoreReleaser releaser(&slots);
```

它适合“资源繁忙时放弃或稍后重试”，而不是永久阻塞工作线程。

## 12. 原子变量：只解决很小的状态

`QAtomicInteger<T>`、`QAtomicPointer<T>` 或标准库 `std::atomic<T>` 适合计数器、布尔停止标记和指针交换等单变量原子操作。

```cpp
std::atomic_bool stopping = false;

// 控制线程
stopping.store(true);

// 工作线程
while (!stopping.load()) {
    processOneChunk();
}
```

原子变量不自动维护多个字段之间的不变量：

```cpp
std::atomic<int> count;
std::atomic<int> total;
```

即使两个字段各自原子，另一个线程仍可能看到“新 count + 旧 total”。需要一致快照时，使用同一把锁或把状态组织成不可变对象整体发布。

## 13. 内存可见性要点

互斥锁不仅防止同时进入，还建立线程间的内存同步关系。一个线程在解锁前完成的写入，随后取得同一把锁的线程能够正确观察到。

以下做法不可靠：

```cpp
bool ready = false;

// 线程 A
data = buildData();
ready = true;

// 线程 B
while (!ready) {}
use(data);
```

编译器和 CPU 可以重排或缓存普通变量访问。应使用锁、条件变量、原子变量，或者用排队信号槽传递结果。

## 14. QThreadPool：复用工作线程

为每个几毫秒的任务创建并销毁一个 `QThread` 成本较高。线程池维护一组可复用线程：

```text
任务提交 → 等待队列 → 空闲线程取任务 → 执行 → 线程回到池中
```

全局线程池：

```cpp
QThreadPool *pool = QThreadPool::globalInstance();
```

默认最大线程数通常来自 `QThread::idealThreadCount()`。

### 14.1 最小可用代码：提交 lambda

```cpp
#include <QCoreApplication>
#include <QDebug>
#include <QThread>
#include <QThreadPool>

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);

    QThreadPool::globalInstance()->start([] {
        qDebug() << "running in" << QThread::currentThread();
    });

    QThreadPool::globalInstance()->waitForDone();
    return 0;
}
```

这段代码演示任务提交，但 GUI 程序不要在按钮槽中调用 `waitForDone()`，否则仍会阻塞界面。

### 14.2 自定义线程池

```cpp
QThreadPool pool;
pool.setMaxThreadCount(4);
pool.setExpiryTimeout(30'000);
pool.start([] { processOne(); });
```

局部线程池析构前要确保任务已完成。长期服务通常把池作为拥有者对象的成员。

## 15. QRunnable：封装无返回值任务

```cpp
class ParseTask : public QRunnable
{
public:
    explicit ParseTask(QByteArray bytes)
        : bytes_(std::move(bytes)) {}

    void run() override
    {
        parse(bytes_);
    }

private:
    QByteArray bytes_;
};

QThreadPool::globalInstance()->start(new ParseTask(bytes));
```

`QRunnable::autoDelete()` 默认为 `true`，线程池在 `run()` 返回后自动删除任务对象。

### 15.1 所有权陷阱

```cpp
auto *task = new ParseTask(bytes);
pool.start(task);
// 默认情况下，此后不能再安全访问或 delete task
```

若调用 `setAutoDelete(false)`，则提交者负责在任务完全结束后删除。不要对开启自动删除的同一个 `QRunnable` 多次调用 `start()`，这会造成竞态。

### 15.2 QRunnable 不等于 QObject

`QRunnable` 本身没有信号槽。需要报告结果时，可选择：

- 让任务持有接收者的 `QPointer`，用 `invokeMethod()` 排队回传；
- 单独使用 `QObject` 结果通道；
- 改用返回 `QFuture` 的 Qt Concurrent；
- 只写入经过同步保护的结果存储。

不要从 `run()` 直接调用 GUI 方法。

## 16. 线程池的重要参数

### 16.1 maxThreadCount

```cpp
pool.setMaxThreadCount(4);
```

CPU 密集任务常以硬件并发数附近为起点。线程不是越多越快：过多线程会增加上下文切换和缓存竞争。

I/O 阻塞任务可能允许更多线程，但若底层 API 已提供异步方式，应优先使用异步 I/O，而不是用大量线程等待。

### 16.2 expiryTimeout

空闲线程默认在一段时间后退出，Qt 文档中的默认值为 30 秒：

```cpp
pool.setExpiryTimeout(60'000);
```

负值会禁用过期机制。长期保留很多空闲线程会占用系统资源，不应无依据设置。

### 16.3 priority

`start(runnable, priority)` 的优先级影响等待队列顺序，不代表已经执行的低优先级任务会被抢占。

### 16.4 tryStart

```cpp
if (!pool.tryStart([] { processNow(); })) {
    // 当前没有可用线程；决定排队、丢弃或稍后重试
}
```

`tryStart()` 不会像 `start()` 那样必然排入等待队列。

### 16.5 clear 与 cancel

`clear()` 只能移除尚未开始的可自动删除任务，不能停止正在执行的代码。已经运行的任务仍需要协作式取消设计。

## 17. 保留线程 reserveThread

当线程池外部发生了一个它看不见的阻塞操作，可临时告诉线程池有容量被占用：

```cpp
pool.reserveThread();
performExternalBlockingWork();
pool.releaseThread();
```

这会影响活动线程计数。忘记 `releaseThread()` 会让池长期错误估计容量。

Qt 6.3 起 `startOnReservedThread()` 可让任务使用预留线程。普通业务很少需要它，不要把它当作任务固定绑定到某个特定线程的机制。

## 18. 线程池任务的对象生命周期

lambda 捕获同样需要审查：

```cpp
void Controller::start()
{
    QString local = makeText();
    QThreadPool::globalInstance()->start([&local] {
        process(local); // 危险：start() 返回后 local 被销毁
    });
}
```

改为按值捕获：

```cpp
QThreadPool::globalInstance()->start([text = std::move(local)] {
    process(text);
});
```

捕获 `this` 也有风险，因为拥有者可能先于任务销毁。可复制任务所需数据，或使用 `QPointer` 在回传前检查 QObject 是否仍存在。

```cpp
QPointer<Controller> guard(this);
QThreadPool::globalInstance()->start([guard] {
    Result result = calculate();
    if (!guard)
        return;

    QMetaObject::invokeMethod(guard, [guard, result] {
        if (guard)
            guard->accept(result);
    });
});
```

## 19. 任务粒度与性能

把一百万个整数分别包装成一百万个任务，调度成本可能超过计算本身。合理任务粒度应让单个任务有足够工作量，同时保留并行度。

```text
粒度过细：队列、调度、同步成本占主导
粒度适中：核心保持忙碌，管理成本可控
粒度过粗：某个慢任务拖住整体，核心利用不足
```

可把输入分块，例如每个任务处理几千或几万个元素，再通过测量调整。

## 20. 不要让同一个池发生“池内等待”

假设线程池最大线程数是 4，4 个任务都运行后各自提交子任务，并同步等待子任务完成。子任务没有空闲线程可运行，于是形成线程池饥饿死锁。

```text
4 个父任务占满池
每个父任务等待子任务
子任务都在队列里，没有线程可执行
```

修复方向：

- 不在池任务中同步等待同池子任务；
- 用连续任务或异步完成通知；
- 合并任务；
- 对确有隔离需求的工作使用独立线程池。

## 21. 如何选择同步工具

| 问题 | 工具 |
|---|---|
| 一次只允许一个线程访问状态 | `QMutex` + `QMutexLocker` |
| 读多写少，允许并发读 | `QReadWriteLock` |
| 等待某个共享条件成立 | `QWaitCondition` + `QMutex` |
| 限制 N 个并发资源 | `QSemaphore` |
| 单个计数或停止标记 | `std::atomic` / Qt 原子类型 |
| 大量短小、独立、无返回值任务 | `QThreadPool` / `QRunnable` |
| 希望异步取得结果 | Qt Concurrent + `QFuture` |

## 22. 常见错误

### 22.1 只有写者加锁

无锁读取与加锁写入仍然竞争。所有访问同一状态的路径必须遵守同一同步协议。

### 22.2 锁与数据生命周期不一致

局部锁保护不了全局数据。把锁和受保护的数据封装到同一类。

### 22.3 锁住后调用外部代码

虚函数、回调、信号接收者可能重入或取得其他锁。锁内避免调用行为未知的代码。

### 22.4 用 if 等待条件

条件变量被唤醒后必须在锁内重新检查谓词，所以使用 `while`。

### 22.5 把线程池当无限队列

生产速度持续高于消费速度时，等待任务会占用大量内存。需要背压、队列上限或拒绝策略。

### 22.6 以为 clear 能停止运行任务

`QThreadPool::clear()` 只影响尚未启动的部分任务。运行中的任务必须自己响应取消。

### 22.7 在线程池任务中使用线程局部对象假设

池线程会复用，同一任务的后续运行不保证落在相同线程。不要依赖“上次在该线程保存的状态”，除非明确管理线程局部存储及其清理。

## 23. 调试并发问题

建议日志至少包含：

```cpp
qDebug() << "object thread:" << object->thread()
         << "current thread:" << QThread::currentThread()
         << "task:" << taskId;
```

排查顺序：

1. 明确每份共享数据的所有访问点；
2. 确认这些访问是否使用同一同步规则；
3. 列出所有锁的取得顺序；
4. 检查持锁期间是否等待线程、发信号或调用外部代码；
5. 检查任务、捕获数据和接收对象的生命周期；
6. 在支持的平台使用 ThreadSanitizer 等数据竞争检测工具；
7. 不要用增加 `sleep()` 隐藏时序问题。

并发错误通常受时序影响，“加日志后不复现”不代表问题消失。

## 24. API 速查表

| API | 用途 | 注意点 |
|---|---|---|
| `QMutex::lock()` | 阻塞取得互斥锁 | 必须配对解锁 |
| `QMutex::tryLock()` | 非阻塞或限时尝试 | 失败时不能访问受保护状态 |
| `QMutexLocker` | 作用域锁 | 优先于手动解锁 |
| `QReadLocker` | 取得读锁 | 不可直接升级为写锁 |
| `QWriteLocker` | 取得写锁 | 写者独占 |
| `QWaitCondition::wait()` | 释放锁并等待 | 放在谓词 `while` 中 |
| `wakeOne()` | 唤醒一个等待者 | 被唤醒后仍需竞争锁 |
| `wakeAll()` | 唤醒所有等待者 | 适合停止或全局变化 |
| `QSemaphore::acquire(n)` | 取得 n 个许可 | 可能阻塞 |
| `QSemaphoreReleaser` | 自动归还许可 | 防止提前返回泄漏许可 |
| `QThreadPool::start()` | 提交任务 | 可能排队 |
| `QThreadPool::tryStart()` | 有空闲线程才启动 | 失败时由调用方决定策略 |
| `QThreadPool::clear()` | 清理未启动任务 | 不停止运行中任务 |
| `QRunnable::setAutoDelete()` | 设置任务所有权 | 提交前确定，避免竞态 |

## 25. 自测题

### 题 1：读操作为什么也要锁

一个线程加锁写 `QList`，另一个线程只读取且不加锁，是否安全？

<details>
<summary>答案</summary>

不安全。读写同时发生仍是数据竞争，读取还可能撞上容器重分配或内部状态修改。读写双方必须遵守同一同步协议。

</details>

### 题 2：条件变量为何使用 while

`wakeOne()` 已经发出通知，消费者为什么还要检查队列是否为空？

<details>
<summary>答案</summary>

唤醒不保证业务谓词仍成立。可能无理由唤醒，也可能其他消费者先取得锁并消费数据。线程重新持锁后必须重新验证条件。

</details>

### 题 3：何时用信号量

需要限制最多 4 个并发上传，应使用互斥锁还是初始值为 4 的信号量？

<details>
<summary>答案</summary>

信号量。互斥锁只允许一个持有者，信号量可以表达固定数量的并发许可。

</details>

### 题 4：线程池为何会饥饿死锁

所有池线程都被父任务占用，而父任务同步等待提交到同一池的子任务，会发生什么？

<details>
<summary>答案</summary>

子任务没有线程可以执行，父任务又不退出释放线程，形成饥饿死锁。应改成异步连续任务、合并任务或使用隔离资源。

</details>

### 题 5：autoDelete 的含义

`QRunnable` 默认提交给线程池后由谁删除？

<details>
<summary>答案</summary>

默认 `autoDelete` 为 true，线程池在任务完成后删除它。提交者不能再按普通自有裸指针使用或重复删除该对象。

</details>

## 26. 本篇总结

并发正确性建立在明确规则上，而不是建立在“这次运行没出错”上：

1. 尽量通过消息传递和数据独占减少共享状态。
2. 共享可变数据的所有访问者必须遵守同一把锁或同一种原子协议。
3. 使用 RAII 管理锁和信号量许可，并尽量缩短临界区。
4. 条件变量等待的是受锁保护的谓词，通知只是促使线程重新检查。
5. 线程池适合大量独立短任务，但仍需处理返回结果、取消、背压和生命周期。

下一篇将把任务执行与结果管理连接起来，讲清 Qt Concurrent、`QFuture`、`QFutureWatcher`、连续任务、异常传播和 `QPromise`。
