# Qt QEventLoop 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QEventLoop>`  
> 所属模块：`Qt6::Core`  
> 继承：`QObject -> QEventLoop`  
> 定位：在一个线程中临时运行或手动泵送 Qt 事件的局部事件循环

## 1. 它究竟解决什么问题

Qt 程序平时只有一个主循环：

```cpp
return QCoreApplication::exec();
```

主循环持续接收并分发定时器、socket、窗口、queued signal/slot、`postEvent()` 等事件。`QEventLoop` 提供的是同一套分发机制的局部入口：它可以在当前线程再运行一层事件循环，或者只处理一小批积压事件。

```text
QCoreApplication::exec()        主事件循环，通常贯穿整个程序
        |
        +-- QEventLoop::exec()  局部嵌套循环，只在当前作用域内运行
        |
        +-- processEvents()     不进入循环，只立即处理一批事件
```

它要解决的典型问题是：

- 在没有 `QCoreApplication::exec()` 的嵌入式宿主中，短暂交给 Qt 分发事件。
- 兼容旧的同步接口：等待一个本质异步的结果，但必须设置超时与取消出口。
- 框架级代码需要暂时处理当前线程的事件队列。

它不适合把异步 API 普遍改写成同步 API。局部事件循环运行期间，用户输入、定时器和其他槽仍会继续执行；这会带来重入、对象提前销毁和状态错序问题。应用业务优先保持异步。

## 2. 构建与最小示例

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

下面示例只演示 `exec()` 的退出机制。真实项目中，被等待的对象通常是网络回复、后台 Worker 或平台异步回调。

```cpp
#include <QCoreApplication>
#include <QEventLoop>
#include <QTimer>

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);

    QEventLoop loop;
    QTimer::singleShot(300, &loop, &QEventLoop::quit);

    const int result = loop.exec();
    qInfo() << "local loop exited with" << result;
    return 0;
}
```

`loop.exec()` 在调用它的线程中运行。该线程必须能够处理 Qt 事件；若这里阻塞在互斥锁、长计算或同步 I/O 上，`QEventLoop` 无法替你把事件“挤过去”。

## 3. `exec()`：局部事件循环的边界

```cpp
int QEventLoop::exec(QEventLoop::ProcessEventsFlags flags = AllEvents);
```

调用 `exec()` 后，函数不会立刻返回，而是反复分发当前线程事件，直到同一个 loop 收到：

- `quit()`，返回码为 `0`。
- `exit(code)`，返回传入的 `code`。
- 所在线程或循环被正常收尾。

```cpp
class LegacyFacade final : public QObject
{
    Q_OBJECT
public:
    QByteArray fetchSynchronously(AsyncClient *client, const QUrl &url)
    {
        QEventLoop loop;
        QTimer timeout;
        timeout.setSingleShot(true);

        QByteArray reply;
        bool timedOut = false;

        connect(client, &AsyncClient::finished, &loop,
                [&](const QByteArray &data) {
                    reply = data;
                    loop.quit();
                });
        connect(&timeout, &QTimer::timeout, &loop, [&] {
            timedOut = true;
            client->cancel();
            loop.exit(1);
        });

        client->get(url);
        timeout.start(5'000);

        if (loop.exec() != 0 || timedOut)
            return {};
        return reply;
    }
};
```

这类包装至少要具备三个条件：

1. 有成功、失败、超时和取消的退出路径。
2. loop、timeout 和连接的生命周期覆盖等待期。
3. 调用者能接受等待期间发生重入。

例如在按钮槽中调用同步包装，用户仍可能点击其他控件、触发第二次请求，甚至关闭当前页面。因此不能在进入 `exec()` 前把对象状态设为“永远不会再被调用”。

### 3.1 `isRunning()` 不能当并发同步原语

```cpp
if (loop.isRunning())
    loop.quit();
```

它只描述检查瞬间的状态，不保证下一行仍相同。跨线程协调不要靠轮询它；向 loop 所在线程发 queued signal/slot 或 `QMetaObject::invokeMethod()`。

## 4. `processEvents()`：能用，但要知道它打开了什么门

`processEvents()` 不像 `exec()` 那样持续运行。它立即处理当前线程的一批事件，然后返回：

```cpp
while (hasMoreChunks()) {
    processOneChunk();
    QCoreApplication::processEvents(QEventLoop::ExcludeUserInputEvents);
}
```

上面的写法看似能让界面“不卡”，但仍可能处理计时器、网络回调、延迟删除和其他业务槽。它无法让当前函数具备事务性，甚至 `ExcludeUserInputEvents` 也不等于“不会重入”。

对于业务代码，更可靠的改法是：

- 每次用 `QTimer::singleShot(0, ...)` 只安排一小块工作，让函数尽快返回。
- CPU 密集型任务放到 `QThread`、`QtConcurrent` 或任务线程池。
- 以状态机、信号和回调表达完成关系。

`processEvents()` 的合理使用场景主要是框架集成、测试、迁移旧代码时的极短事件泵；调用区域必须小，且能处理对象在期间变化或被删除。

### 4.1 三个重载的差别

```cpp
loop.processEvents(QEventLoop::AllEvents);
loop.processEvents(QEventLoop::AllEvents, 10);
loop.processEvents(QEventLoop::AllEvents,
                   QDeadlineTimer(std::chrono::milliseconds(10)));
```

- 不带时间限制的版本返回 `bool`，表示本次是否处理到了事件。
- `int maximumTime` 是兼容接口，表达“最多处理约多少毫秒”。
- `QDeadlineTimer` 版本适合新代码表达明确截止时间；它在调用期间也会继续处理新投递的事件。

时间上限仅限制这次泵事件的时间，不限制槽函数内部耗时，也不消除重入。

## 5. `ProcessEventsFlags`：筛选，不是隔离

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 事件筛选 | `AllEvents` | 允许处理正常可分发的事件；它是默认值。 | 默认不表示安全地处理“一切”；被调用的槽仍可能改动当前业务状态。 |
| 事件筛选 | `ExcludeUserInputEvents` | 暂时不分发鼠标、键盘等用户输入事件。 | 被排除的输入会留待之后处理；定时器、queued 调用等仍可造成重入。 |
| 事件筛选 | `ExcludeSocketNotifiers` | 暂时不分发 socket notifier 事件。 | 只适用于非常局部的底层控制；网络或管道事件会积压。 |
| 事件筛选 | `WaitForMoreEvents` | 当没有可处理事件时，让事件分发器等待下一件事件。 | 通常由 `exec()` 和底层集成使用；不要在持锁状态下用它等待。 |
| 内部标志 | `X11ExcludeTimers`、`EventLoopExec`、`DialogExec`、`ApplicationExec` | Qt 内部用于平台或不同层级循环的标志。 | 应用代码不要传这些实现细节；只使用公开的常规筛选语义。 |
| 标志组合 | `ProcessEventsFlags` | `ProcessEventsFlag` 的 `QFlags` 组合类型。 | 使用按位或组合，例如同时排除用户输入和 socket notifier；组合不是线程同步机制。 |

## 6. 退出、唤醒与线程边界

### 6.1 退出

```cpp
loop.quit();      // 等价于 exit(0)
loop.exit(42);    // 让 exec() 返回 42
```

`exit()` 会令正在运行的这个局部循环结束。若要从另一线程通知它，使用带上下文的 queued 调用：

```cpp
QMetaObject::invokeMethod(&loop, [&loop] {
    loop.quit();
}, Qt::QueuedConnection);
```

不要从其他线程直接依赖 `exit()` 改变 loop 状态，也不要让 lambda 捕获一个可能已经离开作用域的栈上 `QEventLoop`。

### 6.2 唤醒

```cpp
loop.wakeUp();
```

`wakeUp()` 让可能正因 `WaitForMoreEvents` 或事件分发器等待而休眠的 loop 重新检查队列。常规程序几乎不需要手动调用；投递事件、启动定时器和 queued connection 已经会按正常路径唤醒事件分发器。

### 6.3 `event()`

```cpp
bool event(QEvent *event) override;
```

这是 `QObject` 事件分发链的一部分，由 Qt 内部调度 `QEventLoop` 的生命周期。普通项目不应为了控制循环而重写它；优先连接完成信号并调用 `quit()` 或 `exit()`。

## 7. 常见误区

### 把局部循环当成等待锁

`exec()` 会分发事件，不会等待某个 mutex 条件。持锁进入局部循环时，回调可能又需要同一把锁，造成死锁或状态损坏。

### 用 `processEvents()` 修复长耗时任务

它只能暂时让消息得到分发，不能让算法更快，也不会保护对象生命周期。分块、异步或工作线程才是长期方案。

### 在析构函数中嵌套 `exec()`

对象销毁阶段再处理任意事件非常危险：外部回调可能访问半销毁对象。析构应尽量同步、短小，不应等待新的异步结果。

### 忘记超时

任何把异步结果同步等待的封装都必须有超时、取消或应用关闭出口；否则服务器、设备或逻辑缺陷会永久卡住调用线程。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QEventLoop(QObject *parent = nullptr)` | 创建一个可在所属线程中运行的局部事件循环对象。 | parent 负责对象销毁，但 loop 通常是临时栈对象；不要让异步回调保留其失效地址。 |
| 析构 | `~QEventLoop()` | 销毁局部事件循环对象。 | 必须先让相关等待完成或取消；不要在析构中再进入事件循环。 |
| 局部循环 | `exec(ProcessEventsFlags flags = AllEvents)` | 进入局部循环，直到 `quit()` 或 `exit()`，并返回退出码。 | 会允许当前线程其他事件和槽继续执行；业务代码需评估重入和可重入调用。 |
| 状态 | `isRunning() const` | 查询该 loop 此刻是否正在运行。 | 只是一瞬间状态，不能替代跨线程同步或“只执行一次”保护。 |
| 处理事件 | `processEvents(ProcessEventsFlags flags = AllEvents)` | 立即处理一批可分发事件，并返回本次是否处理到事件。 | 不会持续等待；调用期间仍可能重入并改变对象图。 |
| 处理事件 | `processEvents(ProcessEventsFlags flags, int maximumTime)` | 在最多约指定毫秒内处理事件。 | 是兼容重载；时间限制不限制槽函数执行时间，也不会带来逻辑隔离。 |
| 处理事件 | `processEvents(ProcessEventsFlags flags, QDeadlineTimer deadline)` | 在给定 deadline 前处理事件。 | Qt 6.7 起可用；会处理调用期间新投递的事件，重入范围可能比旧重载更大。 |
| 退出 | `exit(int returnCode = 0)` | 请求当前局部循环退出，并让 `exec()` 返回指定值。 | 从其他线程应通过 queued invocation 发起；确保 loop 在回调执行时仍存活。 |
| 退出 | `quit()` | 请求当前局部循环以返回码 `0` 退出。 | 是 `exit(0)` 的便捷形式；不会终止线程，也不会取消正在运行的槽函数。 |
| 唤醒 | `wakeUp()` | 唤醒可能处于等待状态的事件循环。 | 主要供事件循环或底层集成使用；正常应用通常无需直接调用。 |
| 事件入口 | `event(QEvent *event)` | 处理 `QEventLoop` 自身收到的 Qt 事件。 | 框架调用的扩展点；普通业务不要重写它来模拟退出或调度。 |

---

### 一句话总结

`QEventLoop` 能让当前线程临时处理 Qt 事件，但它不是“安全等待”工具：`exec()` 会打开重入入口，`processEvents()` 也不会隔离业务状态。只在框架集成或确有兼容需求时使用，并始终设计明确的退出、超时、取消和生命周期边界。
