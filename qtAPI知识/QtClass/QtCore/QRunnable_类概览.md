# Qt QRunnable：提交给 QThreadPool 的任务对象

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QRunnable>`  
> 所属模块：`Qt6::Core`  
> 类型性质：不可复制的抽象任务基类  
> 关联类型：`QThreadPool`、`QFuture`、`QPromise`

## 1. 它解决什么问题

`QRunnable` 用一个对象表示“可以由 `QThreadPool` 在线程池工作线程执行的任务”。它本身不创建线程、不返回结果，也不提供事件循环；子类只需要实现 `run()`：

```cpp
class HashTask final : public QRunnable
{
public:
    explicit HashTask(QByteArray input)
        : m_input(std::move(input))
    {
    }

    void run() override
    {
        const QByteArray hash =
            QCryptographicHash::hash(m_input,
                                     QCryptographicHash::Sha256);
        saveHash(hash);
    }

private:
    QByteArray m_input;
};

QThreadPool::globalInstance()->start(new HashTask(data));
```

它适合：

- 没有返回值或自行回传结果的后台工作；
- 需要自定义任务对象状态、优先级或自定义 `run()` 的场景；
- 与 `QThreadPool::start(QRunnable *)`、`tryStart()`、`tryTake()` 协作；
- 希望显式控制任务对象自动删除策略的代码。

只有一个短 lambda 时，`QThreadPool::start(callable)` 通常更简洁；需要结果、进度、暂停、取消和异常传播时，优先考虑 `QPromise` / `QFuture` 或 Qt Concurrent。

## 2. 它不是什么

`QRunnable` 不是：

- `QObject`，没有 parent、信号槽、线程亲和性或 `deleteLater()`；
- 线程本身，也不是长期驻留的 worker；
- 线程安全容器；
- 自动取消机制；
- 结果、进度或异常的传输通道；
- 可重复安全地提交的通用任务对象。

`run()` 在某条线程池线程执行。任务不能直接操作 GUI，也不能假设自己每次都在同一条线程上运行。

## 3. 构建与最小示例

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QRunnable>
#include <QThreadPool>

class IndexTask final : public QRunnable
{
public:
    explicit IndexTask(QString path)
        : m_path(std::move(path))
    {
    }

    void run() override
    {
        indexFile(m_path);
    }

private:
    QString m_path;
};

QThreadPool::globalInstance()->start(new IndexTask(path));
```

上例使用默认自动删除。`start()` 成功提交后，不应再访问 `new IndexTask(...)` 得到的裸指针。

## 4. `run()` 的执行边界

### 4.1 在线程池线程执行

`QThreadPool` 选择何时、在哪条工作线程调用 `run()`。任务开始时间、工作线程身份和相邻任务顺序都不由 `QRunnable` 保证。

```cpp
void MyTask::run()
{
    // 这里不是 GUI 线程，除非调用者使用了特殊线程池环境。
    const Result result = calculate();
    deliverResultToOwnerThread(result);
}
```

返回 GUI 或 QObject 所属线程时，可使用 queued signal、`QMetaObject::invokeMethod()` 或 future/watcher 机制。不要从 `run()` 直接更新 `QWidget`。

### 4.2 `run()` 应有清晰的结束条件

线程池无法安全地强制终止任意正在运行的 C++ 代码。长任务应自己检查取消标志、分块处理，并尽快返回：

```cpp
void ImportTask::run()
{
    for (const Item &item : m_items) {
        if (m_cancelRequested.loadAcquire())
            return;
        importOne(item);
    }
}
```

不要在 `run()` 中无限阻塞，否则会占用池线程并让 `QThreadPool` 析构或 `waitForDone()` 长时间等待。

### 4.3 异常不能跨出任务边界

`run()` 里抛出的异常不应逃出线程池调用栈。自行捕获并转换为错误状态，或使用 `QPromise::setException()` 报告给关联 future。

## 5. auto-delete：谁销毁任务对象

### 5.1 默认开启

`QRunnable` 默认 `autoDelete() == true`。当线程池完成执行后，会按自动删除规则销毁 runnable：

```cpp
auto *task = new IndexTask(path);
QThreadPool::globalInstance()->start(task);

// 不要再访问 task；它可能已经运行并被删除。
```

自动删除最适合“一次提交、一次执行、任务对象只被线程池使用”的任务。

### 5.2 必须在提交前设置

```cpp
auto *task = new IndexTask(path);
task->setAutoDelete(false);
pool->start(task);
```

提交给 `QThreadPool` 后再修改 `setAutoDelete()` 是未定义行为。所有权策略必须在 `start()`、`tryStart()` 或 `startOnReservedThread()` 之前确定。

### 5.3 关闭自动删除后由调用方负责

```cpp
auto *task = new IndexTask(path);
task->setAutoDelete(false);
pool->start(task);

pool->waitForDone();
delete task;
```

关闭 auto-delete 并不让任务可以随时安全销毁。调用方必须确认任务已经不在等待队列、也没有正在执行后，才能 `delete` 它。对正在运行的 runnable 直接删除是数据竞争和 use-after-free 风险。

### 5.4 `tryStart()` 的失败所有权

```cpp
auto *task = new IndexTask(path);
if (!pool->tryStart(task))
    delete task;
```

`tryStart(QRunnable *)` 返回 `false` 时任务没有进入线程池，所有权仍在调用方；返回 `true` 后则遵守 auto-delete 策略。Callable 重载会在失败时删除内部创建的 runnable。

## 6. 重复提交和自我重调度

不要从外部将同一个 auto-delete runnable 多次传给 `QThreadPool::start()`。多个执行实例可能竞态地结束并删除同一个对象。

Qt 支持一个 runnable 在自己的 `run()` 内使用 `tryStart(this)` 重新调度自己：

```cpp
void BatchTask::run()
{
    processOneBatch();
    if (hasMoreWork())
        QThreadPool::globalInstance()->tryStart(this);
}
```

这是一种高级模式。auto-delete 开启时，对象会在最后一次执行结束后删除；若多个 `run()` 可能并发访问同一对象，任务内部状态必须同步。普通周期任务通常更适合每轮创建新任务，或维护独立的共享状态。

## 7. 与 QThreadPool 队列 API 的关系

| API | `QRunnable` 在其中的角色 | 所有权重点 |
| --- | --- | --- |
| `start(runnable, priority)` | 启动或排队 | 成功提交后按 auto-delete 规则处理。 |
| `tryStart(runnable)` | 有即时容量才启动 | 失败时调用方仍拥有 runnable。 |
| `startOnReservedThread(runnable)` | 用预留容量运行 | 提交前仍必须确定 auto-delete。 |
| `clear()` | 移除尚未开始的任务 | 不影响已运行任务；auto-delete 待执行任务可被删除。 |
| `tryTake(runnable)` | 从队列尝试取回 | 成功后所有权回到调用方；通常只用于 `autoDelete == false`。 |

对自动删除任务调用 `tryTake()` 有 ABA 风险：任务地址可能已经被删除并被其他对象复用。需要撤回任务时，优先使用关闭 auto-delete 的明确所有权模型。

## 8. `QRunnable::create()`：用 callable 创建任务

```cpp
QRunnable *task = QRunnable::create([input = data] {
    process(input);
});

QThreadPool::globalInstance()->start(task);
```

`create()` 返回堆分配的 runnable，默认 auto-delete 为 true。它是 `QThreadPool::start(callable)` 的底层构件：

```cpp
pool->start([input = data] {
    process(input);
});
```

对于 `std::function` 或函数指针，空 callable 会被拒绝；`nullptr` 重载被显式删除。避免按引用捕获会在提交函数返回后消失的局部变量。

## 9. 生命周期与数据成员

任务对象的成员会在 `run()` 执行期间使用。提交前初始化完成后，除非明确同步，不要从提交线程继续修改这些成员：

```cpp
auto *task = new IndexTask(path);
pool->start(task);

// 错误：task 可能并行运行或已被 auto-delete。
// task->setPath(otherPath);
```

如果结果要存到任务对象中，auto-delete 通常不合适，因为调用方无法在任务结束后安全读取它。更好的方案：

- 将结果投递到接收对象所属线程；
- 使用 `QPromise` / `QFuture`；
- 使用受锁或原子保护的独立共享状态；
- 关闭 auto-delete，并建立明确的完成通知和回收顺序。

## 10. 常见使用场景

### 10.1 一次性 CPU 任务

```cpp
class ThumbnailTask final : public QRunnable
{
public:
    void run() override
    {
        const QImage thumbnail = buildThumbnail(m_source);
        postThumbnail(m_target, thumbnail);
    }

    QImage m_source;
    QPointer<Receiver> m_target;
};
```

目标对象可能提前销毁时，回传前检查 `QPointer`，并通过 queued 调用回到目标线程。

### 10.2 需要携带复杂输入状态

```cpp
class ExportTask final : public QRunnable
{
public:
    ExportTask(ExportPlan plan, QSharedPointer<CancelFlag> cancel)
        : m_plan(std::move(plan)), m_cancel(std::move(cancel))
    {
    }

    void run() override
    {
        exportPlan(m_plan, *m_cancel);
    }

private:
    ExportPlan m_plan;
    QSharedPointer<CancelFlag> m_cancel;
};
```

任务输入应通过值、不可变快照或拥有关系明确的共享状态传入。

## 11. 常见错误

### 11.1 把 QRunnable 当 QObject

它没有 parent、信号和 `deleteLater()`。需要 QObject 线程亲和性和事件循环时，使用 Worker QObject + QThread。

### 11.2 auto-delete 任务提交后继续访问

线程池可能立刻运行并删除任务。提交成功后将原指针视为不可访问。

### 11.3 提交后修改 auto-delete

这是未定义行为。提交前决定所有权。

### 11.4 把同一个 auto-delete task 外部多次提交

会产生删除竞态。创建独立任务或使用受同步保护的重调度设计。

### 11.5 在 run() 中操作 GUI

池线程不是 GUI 线程。通过 queued 调用回传结果。

### 11.6 按引用捕获短生命周期变量

callable 可能稍后才执行。按值捕获或使用明确共享所有权。

### 11.7 以为 clear() 会取消正在运行任务

它只移除等待队列。运行中的代码需要协作式取消。

## 12. 逐项 API 语义

### `QRunnable()`

构造任务基类，默认 `autoDelete` 为 `true`。它不提交任务、不启动线程。

### `~QRunnable()`

虚析构函数，允许线程池通过基类指针正确销毁派生任务。析构时不自动停止其他正在运行的同一对象任务。

### `run()`

纯虚函数。`QThreadPool` 在工作线程调用它；实现必须定义任务完成、取消检查、错误处理和跨线程结果回传策略。

### `autoDelete() const`

查询任务完成后线程池是否自动删除它。返回值应在提交前决定，提交后只读地理解，不要修改。

### `setAutoDelete(bool autoDelete)`

设置自动删除策略。必须在提交到线程池前调用；提交后修改是未定义行为。

### `create(Callable &&functionToRun)`

静态工厂，创建包装 callable 的 `QRunnable *`。返回对象默认自动删除；空 `std::function` 或空函数指针不可作为有效任务。

## API 速查表
| 类别 | API | 作用 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QRunnable()` | 创建默认 auto-delete 的任务基类。 | 不提交、不启动；派生类必须实现 `run()`。 |
| 生命周期 | `~QRunnable()` | 虚析构任务对象。 | 不会自动终止并发运行的同一对象任务。 |
| 执行 | `run()` | 在线程池线程执行任务主体。 | 纯虚；不能直接操作 GUI；异常不应逃出。 |
| 所有权查询 | `autoDelete()` | 查询池完成后是否自动删除任务。 | 默认 `true`；提交成功后不要继续依赖裸指针。 |
| 所有权设置 | `setAutoDelete(bool)` | 设置任务是否由线程池自动删除。 | 必须在 `start()` / `tryStart()` 前调用。 |
| 工厂 | `QRunnable::create(Callable &&)` | 将 callable 包装成堆分配 runnable。 | 默认 auto-delete；捕获数据必须覆盖异步执行期。 |
| 协作 | `QThreadPool::start(QRunnable *)` | 启动或排队任务。 | auto-delete 任务提交后不可访问。 |
| 协作 | `QThreadPool::tryStart(QRunnable *)` | 有即时容量才运行任务。 | 返回 `false` 时调用者仍拥有 runnable。 |
| 协作 | `QThreadPool::tryTake(QRunnable *)` | 尝试从等待队列取回任务。 | 通常只对关闭 auto-delete 的任务使用，避免 ABA 风险。 |

## 14. 一句话总结

`QRunnable` 是线程池任务的最小对象接口：`run()` 在不固定的池线程运行，默认由池自动删除。提交前确定 auto-delete，提交后不再碰原指针；长任务自行协作取消，结果通过 queued 回传或 QPromise/QFuture 交给调用方。
