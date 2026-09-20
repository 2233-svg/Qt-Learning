# QAbstractEventDispatcher 事件分发器深入笔记

> 适用版本：Qt 6，本文按 Qt 6.11.1 的接口说明  
> 头文件：`#include <QAbstractEventDispatcher>`  
> 所属模块：`Qt6::Core`  
> 继承关系：`QObject -> QAbstractEventDispatcher`

## 1. 先说结论：它到底负责什么

`QAbstractEventDispatcher` 是 Qt 事件循环背后的“接线层”。它不负责定义业务事件，而是负责把操作系统或外部事件源产生的事件取出来，再交给 Qt 的事件系统处理。

一个运行中的 Qt 线程，通常可以抽象成下面这条链：

```text
操作系统消息 / 定时器 / socket 可读写
                    ↓
        QAbstractEventDispatcher
                    ↓
      QCoreApplication / QApplication
                    ↓
        QObject::event() / 信号槽 / 定时器事件
```

它主要协调四类事情：

1. **事件循环**：等待事件、取出事件、分发事件。
2. **定时器**：登记定时器、取消定时器、查询剩余时间。
3. **socket notifier**：把文件描述符或 socket 的可读、可写、异常状态接入 Qt 事件循环。
4. **原生事件过滤**：在 Qt 把平台消息转换成 `QEvent` 之前，观察甚至拦截原生消息。

这也是一个抽象基类。Qt 在不同平台上会提供具体实现，例如 Windows、Linux、macOS 各自需要使用不同的系统等待机制。普通应用一般不会自己继承它；真正需要实现它的场景，通常是把 Qt 事件循环嵌入已有的事件循环，或者把某个外部事件系统接进 Qt。

## 2. 普通开发什么时候不应该直接使用它

如果你的需求只是下面这些，通常不需要直接操作 `QAbstractEventDispatcher`：

- 处理普通 GUI 和对象事件：使用 `QApplication`、`QObject`。
- 临时处理一批待处理事件：使用 `QCoreApplication::processEvents()`。
- 创建一个局部事件循环：使用 `QEventLoop`。
- 延迟执行或周期执行：使用 `QTimer`。
- 监听 socket 可读写：使用 `QSocketNotifier`、`QTcpSocket`。
- 监听 Windows/X11 等原生消息：使用 `QAbstractNativeEventFilter`。
- 在线程中运行事件循环：使用 `QThread::exec()`。

直接拿 dispatcher 做“手动事件循环”很容易把线程模型弄乱。例如，在 GUI 线程里反复调用底层 `processEvents()`，可能导致重入、对象状态被中途修改、用户输入在不合适的时机进入业务代码。能用更高层 API 表达的需求，应优先使用更高层 API。

## 3. 一个线程对应一个事件分发器

事件分发器和线程绑定。`QAbstractEventDispatcher::instance()` 默认查询当前线程的 dispatcher，也可以传入一个 `QThread *` 查询指定线程。

```cpp
QAbstractEventDispatcher *current =
    QAbstractEventDispatcher::instance();

QAbstractEventDispatcher *workerDispatcher =
    QAbstractEventDispatcher::instance(workerThread);
```

这里有几个重要边界：

- dispatcher 不是整个进程只有一个；有事件循环的线程可以拥有自己的 dispatcher。
- 对象的定时器和 socket notifier 必须在所属线程中工作。
- 在另一个线程里直接操作某个 dispatcher 的普通成员，通常是不安全的；只有文档明确标注线程安全的 `wakeUp()` 可以从其他线程唤醒它。
- `instance()` 返回的是线程当前使用的 dispatcher，不负责创建一个新的 dispatcher。

## 4. 自定义 dispatcher 的安装时机

如果确实要提供自己的事件分发器，必须在默认 dispatcher 被安装之前设置。Qt 文档给出的两个入口是：

```cpp
QCoreApplication::setEventDispatcher(dispatcher);
```

或者：

```cpp
workerThread->setEventDispatcher(dispatcher);
```

关键不在于“调用了设置函数”，而在于**调用得足够早**。如果线程已经创建并安装了默认事件分发器，再替换它，往往已经错过安装时机，也可能破坏线程已有的定时器和事件循环状态。

自定义 dispatcher 通常需要至少实现这些纯虚函数：

```cpp
bool processEvents(QEventLoop::ProcessEventsFlags flags) override;
void registerSocketNotifier(QSocketNotifier *notifier) override;
void unregisterSocketNotifier(QSocketNotifier *notifier) override;
void registerTimer(int timerId, qint64 interval,
                   Qt::TimerType timerType, QObject *object) override;
bool unregisterTimer(int timerId) override;
bool unregisterTimers(QObject *object) override;
QList<TimerInfo> registeredTimers(QObject *object) const override;
int remainingTime(int timerId) override;
void wakeUp() override;
void interrupt() override;
```

Qt 6.8 之后还需要关注 `Qt::TimerId` 和 `Duration` 版本的定时器虚函数。Qt 6 通过 `QAbstractEventDispatcherV2` 逐步承接了新接口，Qt 7 中 `QAbstractEventDispatcherV2` 会成为别名，旧的整数毫秒接口将不再是长期方向。

## 5. `processEvents()`：处理一批事件，不是永久循环

核心接口是：

```cpp
virtual bool processEvents(QEventLoop::ProcessEventsFlags flags) = 0;
```

它处理当前符合 `flags` 的待处理事件，直到当前没有更多可处理事件，然后返回：

- `true`：至少处理了一个事件。
- `false`：没有处理任何事件。

它**不会自己一直运行**。下面的代码只处理一批事件，然后继续执行后面的代码：

```cpp
const bool handled =
    QAbstractEventDispatcher::instance()->processEvents(
        QEventLoop::ExcludeUserInputEvents);
```

### 5.1 `WaitForMoreEvents` 的语义

如果传入 `QEventLoop::WaitForMoreEvents`：

- 已经有事件：先处理已有事件，然后返回。
- 当前没有事件：阻塞等待新的事件到来，处理后返回。

如果不传 `WaitForMoreEvents`，当前没有事件时会立即返回。这个区别决定了调用者是在“轮询”还是“等待”。

### 5.2 常见 flags 的用途

```cpp
QEventLoop::AllEvents
QEventLoop::ExcludeUserInputEvents
QEventLoop::ExcludeSocketNotifiers
QEventLoop::WaitForMoreEvents
```

- `AllEvents`：处理通常允许处理的事件。
- `ExcludeUserInputEvents`：暂时不让鼠标、键盘等用户输入进入，常用于长操作中更新进度，但它不是线程同步工具。
- `ExcludeSocketNotifiers`：暂时不处理 socket notifier 事件。
- `WaitForMoreEvents`：没有事件时等待，而不是立即返回。

不要把 `processEvents()` 当作“让界面不卡顿”的万能按钮。长时间循环里频繁调用它会引入重入：

```cpp
while (!finished) {
    doSmallPieceOfWork();
    QCoreApplication::processEvents();
}
```

在 `doSmallPieceOfWork()` 和下一次循环之间，按钮点击、定时器、销毁事件都可能执行。被调用的对象可能已经改变状态，甚至已经被删除。优先考虑把长任务移到工作线程，或者用异步分步任务代替手动泵事件。

## 6. `wakeUp()` 和 `interrupt()` 解决的是两个不同问题

### 6.1 `wakeUp()`：把正在等待的线程叫醒

```cpp
virtual void wakeUp() = 0;
```

如果事件循环当前正在系统等待函数中休眠，另一个线程可以调用 `wakeUp()` 让它尽快返回并重新检查事件。

```cpp
QMetaObject::invokeMethod(
    workerObject,
    &Worker::stop,
    Qt::QueuedConnection);

QAbstractEventDispatcher::instance(workerThread)->wakeUp();
```

`wakeUp()` 是线程安全的，但它只负责唤醒，不负责告诉事件循环应该做什么，也不等价于投递一个 Qt 事件。实际通信仍应使用 queued signal、`QMetaObject::invokeMethod()` 或其他明确的线程通信方式。

### 6.2 `interrupt()`：让 `processEvents()` 尽快结束

```cpp
virtual void interrupt() = 0;
```

它用于打断当前的事件分发过程，让 `processEvents()` 尽快返回。它和 `wakeUp()` 的区别可以这样记：

- `wakeUp()` 的重点是“事件循环正在等待时，把它唤醒”。
- `interrupt()` 的重点是“事件循环正在处理事件时，请它尽快停止本轮处理”。

具体实现通常会同时处理“正在等待”和“正在处理”的状态，但语义上不要把两者混为一谈。自定义 dispatcher 时，必须让这两个请求具备可重复调用、可跨线程唤醒的合理行为。

## 7. `aboutToBlock()` 和 `awake()`：观察事件循环的睡眠边界

```cpp
void aboutToBlock();
void awake();
```

它们是信号，不是让你主动控制循环的函数：

- `aboutToBlock()`：事件循环准备调用一个可能阻塞的系统等待函数之前发出。
- `awake()`：事件循环从这个可能阻塞的函数返回后发出。

可以用它们做事件循环诊断或低频维护：

```cpp
auto *dispatcher = QAbstractEventDispatcher::instance();

QObject::connect(dispatcher,
                 &QAbstractEventDispatcher::aboutToBlock,
                 [] {
                     qDebug() << "event loop is about to block";
                 });

QObject::connect(dispatcher,
                 &QAbstractEventDispatcher::awake,
                 [] {
                     qDebug() << "event loop woke up";
                 });
```

这两个信号适合帮助回答“线程到底是在忙，还是在等待”这类问题，但不要把耗时工作放在连接槽里。`aboutToBlock()` 触发时，dispatcher 正准备进入等待；如果槽函数本身很慢，反而会改变事件循环的节奏。

## 8. 定时器：dispatcher 维护的是底层登记信息

应用层通常使用：

```cpp
QTimer timer;
timer.setInterval(1000);
timer.start();
```

或者：

```cpp
const Qt::TimerId id = object->startTimer(1000);
object->killTimer(id);
```

这些高层调用最终需要让所属线程的 dispatcher 登记一个定时器。dispatcher 关心的是：

- 定时器编号；
- 定时器间隔；
- `Qt::TimerType`；
- 定时器关联的 `QObject`；
- 下次到期还有多久。

### 8.1 `Duration` 和 Qt 6.8 新 API

```cpp
using Duration = std::chrono::nanoseconds;
```

`Duration` 是 dispatcher 使用的持续时间别名。Qt 6.11.1 中它是纳秒精度的 `std::chrono` duration，但代码应依赖这个别名，而不是把实现精度写死成某个具体类型。

Qt 6.8 引入了这些新方向的接口：

```cpp
Qt::TimerId registerTimer(Duration interval,
                           Qt::TimerType timerType,
                           QObject *object);

void registerTimer(Qt::TimerId timerId,
                   Duration interval,
                   Qt::TimerType timerType,
                   QObject *object);

bool unregisterTimer(Qt::TimerId timerId);
QList<TimerInfoV2> timersForObject(QObject *object) const;
Duration remainingTime(Qt::TimerId timerId) const;
```

相比旧接口，它们的变化有两个：

1. 定时器 ID 使用 `Qt::TimerId`，表达的是专门的定时器标识，而不是普通 `int`。
2. 时间间隔使用 `std::chrono` duration，避免所有接口都被“整数毫秒”限制。

### 8.2 旧接口为什么仍然存在

Qt 6 为了兼容已有代码，仍保留了：

```cpp
int registerTimer(qint64 interval,
                  Qt::TimerType timerType,
                  QObject *object);

virtual void registerTimer(int timerId,
                           qint64 interval,
                           Qt::TimerType timerType,
                           QObject *object) = 0;

virtual bool unregisterTimer(int timerId) = 0;
virtual QList<TimerInfo> registeredTimers(QObject *object) const = 0;
virtual int remainingTime(int timerId) = 0;
```

其中返回 `int` 的 `registerTimer(qint64, ...)` 已被标记为过时，文档明确建议新代码改用 `Duration` 重载，并说明旧接口将在 Qt 7 移除。

如果你正在实现一个自定义 dispatcher，不要只实现能通过当前版本编译的旧接口；应同时检查 Qt 6.8+ 的 `QAbstractEventDispatcherV2` 设计，确保未来迁移不会把时间精度和 ID 类型重新压回整数。

### 8.3 `remainingTime()` 的特殊返回值

旧接口返回毫秒：

```cpp
int remainingTime(int timerId);
```

新接口返回 `Duration`：

```cpp
Duration remainingTime(Qt::TimerId timerId) const;
```

两者都表达相同的状态：

- 定时器不存在或未激活：旧接口返回 `-1`，新接口返回负 duration。
- 定时器已经到期但事件还没有被处理：返回 `0`。
- 仍未到期：返回剩余时间。

因此不能把返回值简单理解成“永远大于等于零的时间”。判断定时器是否存在时，应先处理负值；判断是否已经到期时，应单独检查零值。

## 9. `TimerInfo` 和 `TimerInfoV2`

### 9.1 旧的 `TimerInfo`

```cpp
struct TimerInfo {
    int timerId;
    int interval;
    Qt::TimerType timerType;
};
```

它描述一个对象关联的定时器，但 ID 和 interval 都是旧的整数形式。`TimerInfo` 在 Qt 6.8 已被标记为过时，主要用于维持 Qt 6 旧代码的兼容性。

### 9.2 `TimerInfoV2`

```cpp
struct TimerInfoV2 {
    Duration interval;
    Qt::TimerId timerId;
    Qt::TimerType timerType;
};
```

`TimerInfoV2` 的三个字段分别表示：

- `interval`：定时器周期或登记时使用的间隔。
- `timerId`：活动定时器的唯一 ID。
- `timerType`：定时器类型，例如粗略、精确或非常粗略的调度策略。

使用 `timersForObject(object)` 查询时，返回的是该对象当前登记的定时器列表。它适合诊断“这个对象到底启动了哪些底层定时器”，不适合替代业务层自己的定时器状态管理。

## 10. socket notifier：把外部 I/O 接进事件循环

抽象接口提供：

```cpp
virtual void registerSocketNotifier(QSocketNotifier *notifier) = 0;
virtual void unregisterSocketNotifier(QSocketNotifier *notifier) = 0;
```

`QSocketNotifier` 代表一个 socket 或文件描述符的 I/O 状态。当它可读、可写或发生异常时，dispatcher 需要让 Qt 收到相应事件。

自定义 dispatcher 的典型任务是把 `QSocketNotifier` 转换成外部事件库的监听对象：

```text
QSocketNotifier
       ↓ registerSocketNotifier()
外部 event loop 的 read/write watcher
       ↓
外部 loop 报告就绪
       ↓
发送 Qt 的 socket notifier 事件
```

注销时要反向解除外部 watcher。Qt 文档特别要求 `unregisterSocketNotifier()` 的重实现调用基类实现；不能只删除外部事件库中的监听，却跳过 Qt 内部的注销逻辑。

如果你只是使用网络模块，应该直接使用 `QTcpSocket`、`QUdpSocket`、`QNetworkAccessManager` 等高层 API，而不是自己调用这两个注册函数。

## 11. 原生事件过滤：Qt 事件之前的最后一道观察点

相关 API：

```cpp
void installNativeEventFilter(QAbstractNativeEventFilter *filterObj);
void removeNativeEventFilter(QAbstractNativeEventFilter *filterObj);
bool filterNativeEvent(const QByteArray &eventType,
                       void *message,
                       qintptr *result);
```

### 11.1 安装过滤器

```cpp
class NativeFilter : public QAbstractNativeEventFilter
{
public:
    bool nativeEventFilter(const QByteArray &eventType,
                           void *message,
                           qintptr *result) override
    {
        Q_UNUSED(result);
        qDebug() << eventType << message;
        return false;
    }
};

NativeFilter filter;
QAbstractEventDispatcher::instance()
    ->installNativeEventFilter(&filter);
```

过滤器接收的是平台原生消息，而不是已经转换好的 `QEvent`。多个过滤器同时存在时，后安装的过滤器先被调用。

过滤器返回：

- `true`：消息已被过滤，停止继续处理。
- `false`：允许后续过滤器和 Qt 的正常处理继续进行。

过滤器对象必须在它被使用期间保持有效。dispatcher 不会替你取得过滤器的所有权；dispatcher 销毁时会移除过滤器，但过滤器自己的生命周期仍由创建者负责。

### 11.2 `filterNativeEvent()` 的职责

如果你实现自定义 dispatcher，必须对从系统收到的**所有**原生消息调用 `filterNativeEvent()`。这样，应用安装的 `QAbstractNativeEventFilter` 才不会因为换了 dispatcher 而失效。

参数中的 `eventType` 和 `message` 是平台相关的：

- Windows 通常是 `MSG` 等原生消息数据。
- X11、Wayland、macOS 等平台的消息结构不同。
- `result` 只在 Windows 上使用，对应 Windows 消息处理中的 `LRESULT`。

如果需求可以通过 `QObject::installEventFilter()` 完成，优先使用后者，因为它跨平台且工作在 Qt 事件层；只有必须观察平台消息、窗口创建、系统快捷键或原生协议时，才进入 native event filter。

## 12. 生命周期钩子：`startingUp()` 与 `closingDown()`

```cpp
virtual void startingUp();
virtual void closingDown();
```

这两个函数是 dispatcher 的生命周期扩展点：

- `startingUp()`：事件循环相关基础设施开始使用时调用。
- `closingDown()`：事件分发器即将停止使用时调用。

默认实现可以不做任何事情。自定义 dispatcher 如果需要初始化或释放外部事件循环资源，可以重写它们，但必须把资源状态和 Qt 线程生命周期对齐，避免在 dispatcher 已经关闭后仍向 Qt 投递事件。

它们不是普通业务对象的“启动/关闭信号”，不能用来替代 `QThread::started`、`QThread::finished` 或应用级初始化流程。

## 13. 一个更合理的自定义 dispatcher 设计轮廓

假设已有一个外部事件库，想让 Qt 对象和外部事件在同一个线程里协同工作，设计时通常需要明确以下几件事：

```text
1. 外部等待函数在哪里调用？
2. Qt 事件和外部事件谁先处理？
3. 外部线程如何唤醒 Qt 所在线程？
4. Qt 定时器如何映射到外部 timer watcher？
5. QSocketNotifier 如何映射到外部 I/O watcher？
6. interrupt() 如何让本轮 processEvents() 返回？
7. native event filter 是否对所有平台消息都调用？
```

`processEvents(flags)` 可以采用类似这样的流程：

```text
检查 interrupt 标志
    ↓
处理已经到达的 Qt/外部事件
    ↓
处理允许的定时器和 socket notifier
    ↓
如果没有更多事件：
    ├─ 没有 WaitForMoreEvents：立即返回
    └─ 有 WaitForMoreEvents：发出 aboutToBlock，进入等待
                              ↓
                          被事件或 wakeUp 唤醒
                              ↓
                          发出 awake，继续处理
```

这只是行为轮廓，不是可直接复制的实现。真正的 dispatcher 还需要处理线程安全、事件优先级、重复唤醒、对象销毁、定时器漂移和平台消息的所有权等问题。

## 14. 常见误区

### 14.1 把 dispatcher 当成业务事件队列

dispatcher 管的是线程级事件机制，不是给业务代码存放任务的容器。业务任务应通过 queued signal、`invokeMethod()`、线程池或任务框架投递。

### 14.2 从任意线程调用普通 dispatcher API

`wakeUp()` 明确是线程安全的；其他函数不要默认线程安全。尤其是定时器和 socket notifier，它们必须在对象所属线程的事件循环上下文中操作。

### 14.3 用 `processEvents()` 代替正确的异步设计

手动泵事件可能暂时让界面继续刷新，但会让函数执行期间发生重入。长期任务应优先移出 GUI 线程，而不是在 GUI 线程里不断嵌套事件处理。

### 14.4 只实现旧的整数定时器接口

Qt 6.8 已经提供 `Duration`、`Qt::TimerId` 和 `TimerInfoV2`。如果自定义 dispatcher 只围绕 `int` 和毫秒设计，后续迁移到 Qt 7 时需要重新调整接口和内部数据结构。

### 14.5 自定义 dispatcher 忘记调用 `filterNativeEvent()`

这样会导致应用安装的 `QAbstractNativeEventFilter` 在你的 dispatcher 下失效，问题通常只在特定平台或特定窗口消息下暴露。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型别名 | `using Duration = std::chrono::nanoseconds` | 表示 dispatcher 定时器使用的持续时间类型 | 通过 `Duration` 使用时间，不要把未来精度写死成整数毫秒 |
| 类型 | `TimerInfo` | 描述旧式定时器的 ID、毫秒间隔和定时器类型 | Qt 6.8 已过时，旧代码兼容用，新代码优先 `TimerInfoV2` |
| 类型 | `TimerInfoV2` | 描述新式定时器的 `Qt::TimerId`、`Duration` 间隔和类型 | 用于 `timersForObject()`，字段是公开成员 |
| 构造函数 | `QAbstractEventDispatcher(QObject *parent = nullptr)` | 构造一个事件分发器基类对象 | 通常由具体平台实现或自定义子类调用，不能直接实例化抽象类 |
| 析构函数 | `~QAbstractEventDispatcher()` | 销毁事件分发器 | 应通过基类指针多态销毁，子类资源应在子类析构阶段释放 |
| 静态查询 | `instance(QThread *thread = nullptr)` | 获取当前线程或指定线程的 dispatcher | 不创建对象；跨线程查询不等于可以跨线程操作 |
| 核心虚函数 | `processEvents(QEventLoop::ProcessEventsFlags flags)` | 处理符合 flags 的待处理事件 | 处理完当前批次就返回；`WaitForMoreEvents` 才会在无事件时等待 |
| socket 虚函数 | `registerSocketNotifier(QSocketNotifier *notifier)` | 把 socket notifier 注册到事件分发器 | 自定义 dispatcher 要映射到外部 I/O 等待机制 |
| socket 虚函数 | `unregisterSocketNotifier(QSocketNotifier *notifier)` | 从事件分发器移除 socket notifier | 重实现必须调用基类实现 |
| 新式定时器 | `registerTimer(Duration interval, Qt::TimerType timerType, QObject *object)` | 创建并登记一个定时器，返回 `Qt::TimerId` | Qt 6.8 引入；新代码优先使用 |
| 新式定时器虚函数 | `registerTimer(Qt::TimerId timerId, Duration interval, Qt::TimerType timerType, QObject *object)` | 按指定 ID 登记定时器 | 主要给 dispatcher 实现使用，ID、对象和线程必须对应 |
| 旧式定时器 | `registerTimer(qint64 interval, Qt::TimerType timerType, QObject *object)` | 以毫秒间隔创建定时器并返回整数 ID | 已过时，Qt 7 迁移到 `Duration` 重载 |
| 旧式定时器虚函数 | `registerTimer(int timerId, qint64 interval, Qt::TimerType timerType, QObject *object)` | 按指定整数 ID 登记旧式定时器 | 自定义旧版兼容实现需要提供，长期代码应同步支持新式接口 |
| 取消定时器 | `unregisterTimer(Qt::TimerId timerId)` | 取消指定新式定时器，成功返回 `true` | Qt 6.8 引入；只能在正确的线程上下文中使用 |
| 取消定时器 | `unregisterTimer(int timerId)` | 取消指定旧式整数定时器 | 旧接口，返回 `false` 表示没有成功取消 |
| 批量取消 | `unregisterTimers(QObject *object)` | 移除某个对象关联的全部定时器 | 返回值表示是否全部成功移除，不是“对象是否存在” |
| 查询旧定时器 | `registeredTimers(QObject *object) const` | 返回对象的 `TimerInfo` 列表 | 旧 API；查询的是登记信息，不是业务层 timer 状态 |
| 查询新定时器 | `timersForObject(QObject *object) const` | 返回对象的 `TimerInfoV2` 列表 | Qt 6.8 引入，适合新代码和诊断工具 |
| 查询剩余时间 | `remainingTime(int timerId)` | 查询旧式定时器剩余毫秒数 | 不存在返回 `-1`，已到期返回 `0` |
| 查询剩余时间 | `remainingTime(Qt::TimerId timerId) const` | 查询新式定时器剩余 duration | 不存在返回负 duration，已到期返回零 duration |
| 线程唤醒 | `wakeUp()` | 唤醒正在等待的事件循环 | 明确线程安全；只负责唤醒，不负责投递业务任务 |
| 中断分发 | `interrupt()` | 请求当前事件分发尽快结束 `processEvents()` | 是“结束本轮分发”的请求，不等同于停止线程 |
| 生命周期 | `startingUp()` | 在 dispatcher 开始服务事件循环时提供初始化钩子 | 默认实现通常为空，不是业务启动信号 |
| 生命周期 | `closingDown()` | 在 dispatcher 关闭前提供清理钩子 | 外部事件源、watcher 和唤醒资源要与它同步释放 |
| 原生过滤 | `installNativeEventFilter(QAbstractNativeEventFilter *filterObj)` | 安装接收应用原生消息的过滤器 | 后安装的过滤器先执行；dispatcher 不接管过滤器所有权 |
| 原生过滤 | `removeNativeEventFilter(QAbstractNativeEventFilter *filter)` | 移除已安装的原生事件过滤器 | 未安装时请求会被忽略，过滤器回调期间移除也是允许的 |
| 原生过滤 | `filterNativeEvent(const QByteArray &eventType, void *message, qintptr *result)` | 将原生消息交给已安装过滤器并决定是否继续处理 | 自定义 dispatcher 必须对所有系统消息调用；参数平台相关 |
| 信号 | `aboutToBlock()` | 事件循环即将进入可能阻塞的等待前发出 | 适合诊断或轻量维护，不要执行耗时操作 |
| 信号 | `awake()` | 事件循环从可能阻塞的等待返回后发出 | 可观察唤醒频率，与 `aboutToBlock()` 成对使用 |

## 16. 最后记住这条分层关系

大多数 Qt 程序只需要使用：

```text
QTimer / QSocketNotifier / QEventLoop / QCoreApplication
```

只有在下面这个边界上，才需要直接研究 `QAbstractEventDispatcher`：

```text
你不只是想使用 Qt 的事件循环，
而是要改变 Qt 事件循环如何等待、如何接入外部事件源、
或者如何把平台消息交给 Qt。
```

因此，学习这个类的重点不是记住每个函数名，而是理解“事件从哪里来、在哪里等待、谁负责唤醒、什么时候停止分发，以及定时器和 socket 如何归属于线程”。这些关系正确以后，API 才不会变成一堆孤立的虚函数。
