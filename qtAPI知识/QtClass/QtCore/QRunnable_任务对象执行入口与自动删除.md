# Qt QRunnable 深入笔记：任务对象、执行入口与自动删除

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QRunnable>`  
> 所属模块：`Qt6::Core`  
> 定位：封装一个可由 QThreadPool 执行的无返回值任务

`QRunnable` 是一个很小的抽象基类：核心只有纯虚函数 `run()` 和一个自动删除标志。它不创建线程，也不负责排队；`QThreadPool` 才负责选择工作线程、调度执行和按规则删除任务。

## 1. CMake 与最小可用代码

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

派生一个任务类：

```cpp
#include <QDebug>
#include <QRunnable>
#include <QThreadPool>

class PrintTask final : public QRunnable
{
public:
    explicit PrintTask(QString text) : m_text(std::move(text)) {}

    void run() override
    {
        qInfo() << m_text;
    }

private:
    QString m_text;
};

QThreadPool::globalInstance()->start(new PrintTask("hello"));
```

默认开启自动删除。`start()` 成功接收指针后，调用者不再删除或访问 `PrintTask`；线程池会在执行结束后清理它。

## 2. 类的本质：任务，不是线程

```text
QRunnable
├─ 保存一次任务需要的数据
└─ run()：任务入口

QThreadPool
├─ 等待队列
├─ 工作线程集合
├─ 调用 runnable->run()
└─ 按 autoDelete 决定是否 delete runnable
```

同一个 QRunnable 可能由任意一条池线程执行。创建 QRunnable 的线程与执行 `run()` 的线程通常不同；提交顺序也不等同于完成顺序。

QRunnable 不是 QObject：

- 没有 parent-child 所有权树；
- 没有 signals/slots；
- 没有线程亲和性；
- 不能调用 `moveToThread()`；
- 没有事件循环语义；
- 不能使用 `deleteLater()`。

这恰好使它成为轻量任务载体，但也意味着结果通知、取消和生命周期必须另外设计。

## 3. 构造、析构与 `run()`

公开接口的核心形态：

```cpp
QRunnable();                    // constexpr noexcept
virtual ~QRunnable();           // virtual noexcept
virtual void run() = 0;         // 纯虚函数
```

虚析构保证通过 `QRunnable *` 删除派生任务时能正确调用派生析构函数。

`run()` 在线程池选择的工作线程中同步执行。对线程池而言，函数返回就表示这一次执行完成。因此：

- 不要从 `run()` 返回后再让后台代码引用 `this`；默认情况下对象可能立刻被删除。
- 不要让 `run()` 抛出无人处理的异常；在线程入口传播未捕获异常通常会终止程序。应在任务边界捕获并转换为错误结果。
- `run()` 若永久阻塞，会永久占用一条池线程。
- `run()` 不会自动拥有 Qt 事件循环，不应依赖 queued slot 或 QTimer 来完成当前任务。

异常边界示例：

```cpp
void ImportTask::run()
{
    try {
        Result result = importFile(m_path);
        publishSuccess(std::move(result));
    } catch (const std::exception &e) {
        publishFailure(QString::fromUtf8(e.what()));
    } catch (...) {
        publishFailure("unknown import error");
    }
}
```

## 4. 自动删除：最关键的所有权规则

### 4.1 默认行为

```cpp
auto *task = new PrintTask("hello");
bool enabled = task->autoDelete(); // 默认 true
pool->start(task);                 // 成功提交后池接管
task = nullptr;                    // 最好立即放弃本地观察指针
```

默认 `autoDelete() == true`。QThreadPool 调用 `run()` 后自动 `delete` 任务。自动删除很适合 fire-and-forget 任务：没有外部指针，也没有单独回收步骤。

### 4.2 关闭自动删除

```cpp
auto *task = new ReusableTask(data);
task->setAutoDelete(false); // 必须在提交前
pool->start(task);

pool->waitForDone();        // 证明 run 已返回
consume(task->result());
delete task;
```

`setAutoDelete(false)` 把所有权留给应用，但不代表任务可在运行期间随意读取或删除。调用者仍必须建立“执行已结束”的同步关系。

### 4.3 提交后修改是未定义行为

```cpp
pool->start(task);
task->setAutoDelete(false); // 错误：提交后更改，未定义行为
```

线程池可能已读取标志、已经执行，甚至已经删除对象。auto-delete 是提交协议的一部分，必须先配置再提交。

### 4.4 所有权状态表

| 情况 | 提交前 | 提交成功后 | 执行完成后 |
|---|---|---|---|
| `autoDelete == true` | 调用者 | 线程池 | 已删除 |
| `autoDelete == false` | 调用者 | 仍由调用者持有，但不可提前删 | 调用者负责删除 |
| `tryStart()` 返回 false | 调用者 | 未提交 | 调用者负责删除/重试 |
| `tryTake()` 成功 | 原先在线程池队列 | 所有权交回调用者 | 调用者负责处理 |

“仍由调用者拥有”不等于“调用者可以不经同步地访问”。所有权回答谁删除，同步回答何时访问安全。

## 5. `QRunnable::create()`

可用静态模板把 callable 包装成一个 QRunnable：

```cpp
QRunnable *task = QRunnable::create([input] {
    process(input);
});

QThreadPool::globalInstance()->start(task);
```

返回的 Runnable 默认自动删除。Qt 6 的 callable 可以是 move-only 类型，因此可转移独占资源：

```cpp
auto payload = std::make_unique<Payload>();

QRunnable *task = QRunnable::create(
    [payload = std::move(payload)]() mutable {
        process(*payload);
    });

pool->start(task);
```

如果不需要拿到 QRunnable 指针，Qt 6 还允许直接 `pool->start(callable)`，通常更简洁。需要调用 `setAutoDelete(false)`、尝试从队列移除，或定义丰富任务类型时再显式创建 QRunnable。

## 6. 数据捕获与生命周期

### 6.1 按值保存输入

任务经常晚于提交函数返回，应把必要输入按值保存：

```cpp
class ParseTask final : public QRunnable
{
public:
    explicit ParseTask(QByteArray bytes)
        : m_bytes(std::move(bytes)) {}

    void run() override { parse(m_bytes); }

private:
    QByteArray m_bytes;
};
```

Qt 隐式共享值类型按值复制通常成本合理，写时才分离。不要保存对调用栈局部对象的引用或裸指针，除非外部协议能严格保证其生命周期。

### 6.2 捕获 QObject

QObject 可能在任务执行前销毁，而且不能因为指针有效就跨线程调用其任意方法。用 `QPointer` 检测生命周期，并把最终调用排回对象线程：

```cpp
QPointer<Receiver> receiver = m_receiver;

pool->start([receiver, input] {
    Result result = calculate(input);

    if (!receiver)
        return;

    QMetaObject::invokeMethod(
        receiver,
        [receiver, result = std::move(result)] {
            if (receiver)
                receiver->accept(result);
        },
        Qt::QueuedConnection);
});
```

queued lambda 必须有 context 对象，这样 Qt 能把它投递到正确线程，并在 context 销毁时避免调用。

## 7. 结果回传

QRunnable 的 `run()` 返回 `void`。常见方案有三类。

### 7.1 投递到接收 QObject

适合 UI 更新或少量结果，使用上一节的 `invokeMethod(..., Qt::QueuedConnection)`。

### 7.2 外部结果槽加同步

```cpp
struct SharedResult {
    QMutex mutex;
    std::optional<Result> value;
};
```

任务和调用者访问同一结果时必须由 mutex、原子操作或其他同步原语保护。仅仅等“一段时间”不构成同步。

### 7.3 使用 QPromise/QFuture

当需求包括返回值、异常、进度、多个结果、暂停或取消时，直接使用 `QPromise`、`QFuture`、`QFutureWatcher` 或 Qt Concurrent 通常更清楚。QRunnable 更接近底层执行单元。

## 8. 取消必须由任务协作

QRunnable 没有 `cancel()`。即使 `QThreadPool::clear()` 清掉待执行任务，也不能停止正在运行的 `run()`。

可用共享原子标志：

```cpp
struct CancelState {
    std::atomic_bool requested = false;
};

class ScanTask final : public QRunnable
{
public:
    ScanTask(QStringList files, std::shared_ptr<CancelState> cancel)
        : m_files(std::move(files)), m_cancel(std::move(cancel)) {}

    void run() override
    {
        for (const QString &file : m_files) {
            if (m_cancel->requested.load(std::memory_order_relaxed))
                return;
            scanOne(file);
        }
    }

private:
    QStringList m_files;
    std::shared_ptr<CancelState> m_cancel;
};
```

取消检查应放在一致状态边界。若任务阻塞在不可取消的系统调用中，标志不会使它自动醒来；需要选用超时 API 或关闭/唤醒相应资源。

## 9. 重复执行同一个对象

官方支持一种特殊方式：在 `run()` 内调用 `QThreadPool::tryStart(this)`，让同一个 Runnable 再执行一次。

```cpp
void BatchTask::run()
{
    processOneBatch();

    if (hasMoreBatches())
        QThreadPool::globalInstance()->tryStart(this);
}
```

若自动删除开启，对象会在最后一个 `run()` 执行退出后删除。但多个执行可能重叠，因此成员状态必须线程安全，`hasMoreBatches()` 也要能处理并发。

不要从外部对同一个自动删除对象多次调用 `start()`：

```cpp
pool->start(task);
pool->start(task); // 错误：可能一边执行/删除，一边再次使用
```

这会产生竞争。若确实需要多个相同任务，创建多个独立 Runnable；若需要一个可重用对象，关闭自动删除并建立严格的完成同步，但仍要防止并发 `run()`。

## 10. 从队列撤回任务

```cpp
task->setAutoDelete(false);
pool->start(task);

if (pool->tryTake(task)) {
    // 尚未执行，所有权明确回到这里。
    delete task;
}
```

`tryTake()` 只能撤回尚未开始的任务。返回 false 时，任务可能已经运行、已经完成，或不在该池中。

对于自动删除任务，按地址调用 `tryTake()` 有 ABA 风险：原任务可能已执行和释放，同一地址被分配给新任务，最终撤回错误对象。因此只对 `autoDelete() == false` 的 Runnable 使用 `tryTake()`。

## 11. 任务内部是否能使用 QObject

可以在 `run()` 内创建局部 QObject，只要它及其子对象在 `run()` 返回前于同一线程销毁：

```cpp
void NetworkLikeTask::run()
{
    QLocalObject helper; // 构造、使用、销毁都在当前池线程
    helper.performSynchronousOperation();
}
```

但不要把该对象留到 `run()` 返回之后，也不要假设池线程会持续处理它的事件。需要 QTimer、异步 socket 或 queued slot 的长期服务时，使用有事件循环的 QThread + Worker。

线程池线程会被复用，所以也不要擅自长期更改线程名称、优先级、事件分发器或全局线程状态；这会污染后续任务的执行环境。

## 12. 任务粒度与资源策略

一次 QRunnable 太小，入队、唤醒和同步开销可能超过实际工作；太大则降低公平性、延长取消响应并造成队头阻塞。

可以批处理：

```cpp
void BatchTask::run()
{
    for (qsizetype i = begin; i < end; ++i)
        process(items[i]);
}
```

合理批次应通过测量决定。CPU 密集任务通常按核心数控制并发；阻塞 I/O 不应无上限塞满全局池；持有数据库连接、文件描述符等稀缺资源的任务还要遵守对应资源池的上限。

## 13. 常见错误

### 错误 1：栈上对象开启自动删除

```cpp
PrintTask task("hello");
pool->start(&task); // 错误：池可能 delete 栈地址，且 task 可能提前离开作用域
```

默认自动删除任务必须动态分配，或直接提交 callable。栈对象只有在关闭自动删除并严格等待完成时才可能安全，但这种写法脆弱，不推荐。

### 错误 2：把 QRunnable 当 QObject

QRunnable 没有线程归属与信号槽。需要信号时可以让任务类多重继承 `QObject, QRunnable`，但所有权和线程归属会变复杂；通常让任务向独立接收 QObject queued 投递更清晰。

### 错误 3：提交后读取任务成员

自动删除时可能悬空；关闭自动删除时也可能与 `run()` 并发形成数据竞争。先建立完成同步，再读取。

### 错误 4：任务直接操作 GUI

`run()` 位于池线程，QWidget 只能在 GUI 线程访问。把纯数据结果投递回 GUI。

### 错误 5：将 `clear()` 当作强制取消

它只移除未开始项。运行中 Runnable 必须自己响应取消。

### 错误 6：在全局池运行无限等待任务

这会占住共享容量，拖慢 Qt Concurrent 和其他模块。使用异步 I/O、专用 QThread，或至少隔离到容量受控的私有池。

## API 速查表
`QRunnable` 的 API 很短，真正需要查清的是所有权：任务交给线程池后，是否开启自动删除、是否还可能被重复启动、以及结果和取消状态由谁保存。先弄清这三件事，再写 `run()`。

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造与类型 | `QRunnable()` | 构造一个可交给 `QThreadPool` 执行的任务基类对象 | 它不是 `QObject`，没有 parent、信号槽、线程亲和性或事件循环；默认开启自动删除 |
| 构造与类型 | `virtual ~QRunnable()` | 通过 `QRunnable *` 多态销毁派生任务 | 自动删除开启时通常由线程池在 `run()` 返回后调用；关闭自动删除则由任务拥有者负责 |
| 执行入口 | `virtual void run() = 0` | 定义任务真正执行的代码，线程池会在工作线程调用它 | 无返回值且可能在任意池线程运行；不要依赖固定线程身份，也不要让异常逃出任务边界 |
| 所有权 | `autoDelete() const` | 查询任务完成后是否由线程池自动删除 | 只表示删除策略，不表示任务已经完成，也不提供成员访问同步 |
| 所有权 | `setAutoDelete(bool)` | 设置任务完成后的删除策略 | 必须在提交给线程池前设置；提交后修改属于未定义行为 |
| 工厂方法 | `QRunnable::create(Callable &&)` | 把一个可调用对象包装成 `QRunnable` 指针，省去手写派生类 | 返回对象通常默认自动删除；捕获的资源必须覆盖任务实际执行时间，支持 move-only callable 的版本要注意所有权转移 |
| 调度配合 | `QThreadPool::start(QRunnable *)` | 把任务放入线程池等待执行或立即执行 | 提交成功后，自动删除任务的原始指针不可再访问；关闭自动删除也必须等 `run()` 完成后再读写成员 |
| 调度配合 | `QThreadPool::tryStart(QRunnable *)` | 线程池有可用线程时尝试启动任务，否则返回失败 | 返回失败时任务仍由调用者处理；不要把同一个自动删除对象从外部重复提交 |
| 调度配合 | `QThreadPool::tryTake(QRunnable *)` | 尝试从等待队列撤回尚未开始的任务 | 只对关闭自动删除的任务使用；自动删除任务按地址撤回可能产生 ABA 风险 |
| 调度配合 | `QThreadPool::clear()` | 清除线程池中尚未开始的任务 | 不能停止已经进入 `run()` 的任务；运行中取消必须由任务自己协作响应 |

## 15. 总结

1. QRunnable 是任务对象，不是线程，也不是 QObject。
2. QThreadPool 负责调度并调用 `run()`；任务不能依赖固定线程身份。
3. 默认 auto-delete 开启，提交成功后不要再访问或删除原指针。
4. 关闭自动删除只改变所有权，不自动提供完成同步或线程安全。
5. auto-delete 标志必须在提交前确定，提交后修改属于未定义行为。
6. `QRunnable::create()` 可把 callable 包装成任务；简单场景可直接提交 callable。
7. 结果应通过 queued 投递、受同步保护的状态或 Future/Promise 回传。
8. 已运行任务只能协作式取消，阻塞点还必须能够超时或被唤醒。
9. 不要从外部重复 start 同一个自动删除对象；必要时创建独立任务实例。
10. 使用 `tryTake()` 撤回任务时关闭自动删除，避免 ABA 地址复用风险。
