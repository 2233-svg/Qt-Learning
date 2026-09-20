# Qt Core 基础：事件循环与事件系统

> 适用版本：Qt 6.11.1  
> 所属模块：Qt Core；GUI 事件还涉及 Qt GUI 和 Qt Widgets  
> 前置知识：`QObject`、信号与槽、C++ 虚函数

## 1. 为什么 Qt 应用需要事件循环

GUI 程序大部分时间不是按固定顺序连续计算，而是在等待：

- 用户按键或点击鼠标
- 窗口移动、缩放、显示或关闭
- 定时器到期
- 网络数据到达
- 线程发来排队信号
- 某个对象请求延迟删除

事件循环负责等待这些事件，并在事件到达时把它们分发给正确对象。

```text
操作系统 / Qt 内部 / 应用代码
              ↓
        事件队列与事件分发器
              ↓
        QCoreApplication::notify
              ↓
          QObject::event
              ↓
   具体处理函数或对象自己的 event 实现
```

典型入口：

```cpp
int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    MainWindow window;
    window.show();

    return app.exec();
}
```

`app.exec()` 启动主事件循环。它通常一直运行到应用调用 `quit()`、`exit()`，或最后一个窗口关闭并触发退出。

## 2. 事件循环不是 while(true)

可以用伪代码理解它：

```cpp
while (!shouldQuit) {
    waitForNativeOrPostedEvents();
    dispatchReadyEvents();
    processTimersAndQueuedCalls();
}
```

实际实现还涉及平台事件分发器、套接字通知、事件优先级、压缩和线程局部事件循环，远比普通无限循环复杂。

事件循环的关键性质：

1. 处理函数执行期间，同一线程通常不能处理下一个普通事件。
2. 处理函数返回后，控制权才交回事件循环。
3. 单次处理耗时过长会阻塞该线程的全部事件响应。
4. 每个运行事件循环的线程都有自己的事件队列和分发上下文。

## 3. QApplication、QGuiApplication、QCoreApplication

```text
QCoreApplication
  └─ QGuiApplication
       └─ QApplication
```

- `QCoreApplication`：无 GUI 的事件循环、应用信息、事件投递等。
- `QGuiApplication`：增加窗口系统、屏幕、字体、剪贴板等 GUI 基础。
- `QApplication`：增加 Qt Widgets 所需的样式和控件级行为。

一个进程通常只创建一个应用对象，而且应在创建其他依赖 Qt 应用环境的对象之前构造。

## 4. QEvent：事件是一个对象

Qt 中的事件继承自 `QEvent`。常见派生类型包括：

| 事件类 | 常见用途 |
|---|---|
| `QKeyEvent` | 键盘按下和释放 |
| `QMouseEvent` | 鼠标按键和移动 |
| `QWheelEvent` | 滚轮 |
| `QResizeEvent` | 控件或窗口尺寸改变 |
| `QMoveEvent` | 位置改变 |
| `QPaintEvent` | 请求重绘 |
| `QCloseEvent` | 请求关闭窗口 |
| `QTimerEvent` | 基础定时器到期 |
| `QChildEvent` | 子对象加入、移除或完善 |
| `QDynamicPropertyChangeEvent` | 动态属性改变 |

每个事件都有类型：

```cpp
QEvent::Type type = event->type();
```

一个事件类可以对应多个类型。例如 `QMouseEvent` 可表示按下、释放、双击和移动。

### 4.1 spontaneous

```cpp
bool fromWindowSystem = event->spontaneous();
```

由底层窗口系统产生的事件通常是 spontaneous；通过 `sendEvent()` 或 `postEvent()` 发送的事件不是。业务代码很少需要依赖这个标志。

## 5. 事件如何到达对象

Qt 将事件交给目标 `QObject` 的：

```cpp
bool QObject::event(QEvent *event);
```

对于 `QWidget`，`event()` 会根据类型继续分派到更具体的虚函数：

```text
QEvent::Paint       → paintEvent()
QEvent::Resize      → resizeEvent()
QEvent::MousePress  → mousePressEvent()
QEvent::KeyPress    → keyPressEvent()
QEvent::Close       → closeEvent()
```

因此，处理常见控件事件时通常重写专用函数，而不是写一个巨大的 `event()`。

## 6. 重写具体事件处理函数

```cpp
class ClickableWidget final : public QWidget
{
protected:
    void mousePressEvent(QMouseEvent *event) override
    {
        if (event->button() == Qt::LeftButton) {
            qDebug() << "left click at" << event->position();
            event->accept();
            return;
        }

        QWidget::mousePressEvent(event);
    }
};
```

原则：

- 完全替换父类行为时，可以不调用父类实现。
- 只处理部分情况时，把未处理情况交回父类。
- 不确定父类是否具有重要默认行为时，优先调用父类实现。

忘记调用父类可能破坏焦点、快捷键、拖放、选择和控件状态等默认行为。

## 7. 重写 event()

没有合适的专用处理函数，或需要在统一入口截获事件时，可以重写 `event()`：

```cpp
bool Editor::event(QEvent *event)
{
    if (event->type() == QEvent::KeyPress) {
        auto *keyEvent = static_cast<QKeyEvent *>(event);

        if (keyEvent->key() == Qt::Key_Tab) {
            insertTabCharacter();
            return true;
        }
    }

    return QWidget::event(event);
}
```

`true` 表示事件已被识别并处理；未处理事件应交给父类 `event()`。

### 7.1 返回值与 accept 标志不是同一个概念

需要区分：

- `event()` / `eventFilter()` 的 `bool` 返回值：是否继续分发。
- `QEvent::accept()` / `ignore()`：设置事件的 accepted 状态。

具体事件是否向父控件传播、是否触发默认行为，取决于该事件类型和接收类的规则。不能把所有事件都简单理解为“accept 就停止冒泡”。

## 8. 事件过滤器

事件过滤器可以在目标对象之前观察或拦截事件。

### 8.1 安装过滤器

```cpp
target->installEventFilter(filterObject);
```

过滤器类重写：

```cpp
bool Filter::eventFilter(QObject *watched, QEvent *event)
{
    if (watched == target_ && event->type() == QEvent::KeyPress) {
        auto *keyEvent = static_cast<QKeyEvent *>(event);

        if (keyEvent->key() == Qt::Key_Escape) {
            cancelOperation();
            return true; // 拦截，不再交给目标对象
        }
    }

    return QObject::eventFilter(watched, event);
}
```

含义：

- 返回 `true`：事件被过滤掉，目标对象和后续过滤器不再处理。
- 返回 `false`：允许继续传递。

未处理分支调用父类实现更稳妥，因为父类也可能实现了自己的过滤逻辑。

### 8.2 多个过滤器的顺序

同一目标安装多个事件过滤器时，最后安装的过滤器通常最先执行。不要让业务正确性依赖复杂的过滤器安装顺序。

### 8.3 过滤器与目标必须同线程

过滤对象与被观察对象必须具有相同线程归属。它们后来被移动到不同线程时，过滤器不会工作；重新处于同一线程后才可继续工作。

### 8.4 在过滤器中删除目标对象

如果在 `eventFilter()` 中删除了被观察对象，必须返回 `true`：

```cpp
bool Filter::eventFilter(QObject *watched, QEvent *event)
{
    if (shouldRemove(watched, event)) {
        delete watched;
        return true;
    }

    return false;
}
```

如果删除后返回 `false`，Qt 会继续把当前事件发送给已经销毁的对象，导致崩溃。实际项目通常更适合 `deleteLater()`，但仍要正确停止当前分发。

### 8.5 移除过滤器

```cpp
target->removeEventFilter(filterObject);
```

即使正在执行过滤逻辑，也允许移除过滤器。

## 9. 应用级全局事件过滤器

```cpp
app.installEventFilter(globalFilter);
```

这样可以观察应用中所有对象的事件，适用于：

- 自动化输入记录
- 全局空闲检测
- 特殊无障碍或输入策略
- 定向诊断

但全局过滤器会经过大量事件，可能增加所有事件分发的成本，也容易产生过度耦合。能在具体控件或局部容器处理时，不要使用全局过滤器。

## 10. sendEvent()：同步发送

```cpp
QEvent event(MyEventType);
const bool handled = QCoreApplication::sendEvent(receiver, &event);
```

特点：

- 立即调用事件过滤器和接收对象。
- 函数返回时处理已经结束。
- 可以使用栈上的事件对象。
- 返回值反映 `notify()` 的处理结果。

调用关系近似：

```text
sendEvent()
  → notify()
    → eventFilter()
      → receiver->event()
```

同步发送会在当前调用栈重入接收对象。若接收对象正在修改状态，重入可能破坏不变量。

## 11. postEvent()：异步投递

```cpp
QCoreApplication::postEvent(receiver,
                            new QEvent(MyEventType));
```

特点：

- 事件进入接收对象所属线程的队列。
- 当前函数立即返回。
- 稍后由事件循环分发。
- 事件必须在堆上创建。
- Qt 接管已投递事件的所有权并负责删除。

不要这样写：

```cpp
QEvent event(MyEventType);
QCoreApplication::postEvent(receiver, &event); // 错误：栈对象会提前失效
```

也不要在投递后手动删除：

```cpp
auto *event = new QEvent(MyEventType);
QCoreApplication::postEvent(receiver, event);
delete event; // 错误：所有权已经交给 Qt
```

### 11.1 事件优先级

`postEvent()` 可指定优先级。优先级高的事件先处理，相同优先级保持投递顺序。除非确有调度需求，不要滥用优先级制造隐蔽依赖。

### 11.2 事件压缩

Qt 会对某些高频事件进行合并，例如绘制和尺寸变化。`QWidget::update()` 请求稍后重绘，多个请求可能合并，从而减少闪烁和重复工作。

## 12. sendEvent 与 postEvent 对比

| 特征 | `sendEvent()` | `postEvent()` |
|---|---|---|
| 执行时间 | 当前调用栈立即执行 | 稍后由事件循环执行 |
| 事件对象 | 可放在栈上 | 必须动态分配 |
| 所有权 | 调用者保留 | Qt 接管 |
| 是否可能重入 | 是，立即重入 | 稍后执行，仍可能产生逻辑重入 |
| 线程用途 | 受同步调用线程约束 | 可投递到对象所属线程 |
| 返回处理结果 | 可以 | 不可以立即获得 |

## 13. 自定义事件

信号适合广播状态变化，自定义事件适合把一个事件对象投递给特定接收者，或接入现有事件过滤和分发体系。

### 13.1 注册事件类型

```cpp
const QEvent::Type DataReadyEventType =
    static_cast<QEvent::Type>(QEvent::registerEventType());
```

用户事件范围是 `QEvent::User` 到 `QEvent::MaxUser`。使用 `registerEventType()` 可以避免不同组件意外复用同一个编号。

### 13.2 定义事件类

```cpp
class DataReadyEvent final : public QEvent
{
public:
    explicit DataReadyEvent(QString data)
        : QEvent(DataReadyEventType)
        , data_(std::move(data))
    {
    }

    const QString &data() const
    {
        return data_;
    }

private:
    QString data_;
};
```

### 13.3 接收事件

```cpp
bool Receiver::event(QEvent *event)
{
    if (event->type() == DataReadyEventType) {
        auto *dataEvent = static_cast<DataReadyEvent *>(event);
        process(dataEvent->data());
        return true;
    }

    return QObject::event(event);
}
```

### 13.4 投递事件

```cpp
QCoreApplication::postEvent(
    receiver,
    new DataReadyEvent(QStringLiteral("payload")));
```

跨线程投递前要保证 `receiver` 在投递与处理期间有效。Qt 会在接收对象销毁时移除发给它的已投递事件，但并发代码仍需设计清晰的关闭顺序。

## 14. 信号与事件的区别

| 问题 | 信号与槽 | 事件 |
|---|---|---|
| 通信关系 | 一个发送者可有多个接收者 | 通常投递给一个目标对象 |
| 接收者是否预先连接 | 需要连接 | 目标实现 `event()` 即可 |
| 数据表达 | 函数参数 | 事件对象及其派生字段 |
| 拦截机制 | 连接和断开 | 事件过滤器 |
| 常见用途 | 状态通知、组件通信 | 输入、窗口、定时、底层分发 |

事件常常最终导致信号。例如按钮先收到鼠标事件，内部更新按下状态，随后发出 `clicked()` 信号。应用层通常监听信号，自定义控件或输入行为才更常直接处理事件。

## 15. 定时器与事件循环

`QTimer` 依赖所属线程的事件循环：

```cpp
QTimer timer;
timer.setInterval(1000);

QObject::connect(&timer, &QTimer::timeout, [] {
    qDebug() << "tick";
});

timer.start();
```

定时器表示“时间到达后尽快通知”，不是硬实时保证。如果事件循环正忙，`timeout()` 会延后。

零间隔定时器会尽快执行，但与其他事件的相对顺序没有严格保证。大量工作应拆分或移到工作线程，不要用零间隔定时器无限占用事件循环。

## 16. 排队信号也是事件循环的一部分

跨线程 `QueuedConnection` 不会直接调用槽。Qt 把元调用封装并投递到接收对象线程：

```text
工作线程 emit resultReady(data)
            ↓
接收线程事件队列
            ↓
接收线程事件循环
            ↓
GUI 对象的槽函数
```

因此接收线程没有运行事件循环时，排队槽不会正常得到执行。这也是事件循环与信号槽不能割裂学习的原因。

## 17. deleteLater 与 DeferredDelete

`QObject::deleteLater()` 会安排 `QEvent::DeferredDelete`：

```cpp
object->deleteLater();
```

对象不是立即删除，而是在控制权返回合适的事件循环后销毁。这避免在对象自己的事件或信号调用栈中直接析构。

如果主事件循环已经停止，之后调用 `deleteLater()` 不会再由主循环处理。关闭程序时应设计清晰的销毁顺序，不要把退出后的清理全部寄托在延迟删除上。

## 18. processEvents 为什么要谨慎

```cpp
QCoreApplication::processEvents();
```

它会在当前代码尚未返回时主动处理一批事件。看似能让长循环中的界面“保持响应”，却可能带来：

- 当前函数被用户操作重入
- 对象在当前代码继续使用前被关闭或删除
- 状态只更新一半时触发其他槽
- 难以预测的事件顺序
- `DeferredDelete` 等处理与正常主循环不同

危险模式：

```cpp
for (int i = 0; i < hugeCount; ++i) {
    doOneStep(i);
    QCoreApplication::processEvents();
}
```

更好的方向：

- 把计算放到工作线程或 `QtConcurrent`。
- 使用真正异步的网络、文件或进程 API。
- 用定时器把任务拆成小批次，并让每批自然返回事件循环。

只有在明确理解重入和生命周期后，才应在有限、受控的场景调用 `processEvents()`。

## 19. 局部与嵌套事件循环

`QEventLoop` 可以启动局部事件循环：

```cpp
QEventLoop loop;

connect(worker, &Worker::finished,
        &loop, &QEventLoop::quit);

loop.exec();
```

它会阻塞当前函数，但继续处理当前线程的事件。问题在于调用栈尚未返回，外部事件却能再次进入相关对象，形成重入。

模态对话框、部分同步包装和旧式 API 可能使用嵌套循环。新业务代码优先保持异步，通过信号延续流程，而不是把异步操作包装成同步等待。

## 20. 退出事件循环

### 20.1 quit

```cpp
QCoreApplication::quit();
```

请求应用以返回码 0 退出主事件循环。它是线程安全的槽，适合连接信号。

### 20.2 exit

```cpp
QCoreApplication::exit(2);
```

指定返回码退出。它应从主线程调用；跨线程通常发送信号连接到 `quit()` 或主线程槽更合适。

### 20.3 连接退出信号

```cpp
QObject::connect(&app, &QCoreApplication::aboutToQuit, [] {
    qDebug() << "application is about to quit";
});
```

`aboutToQuit` 适合最后阶段通知，但不应把可能长时间阻塞或依赖新异步事件的工作放在这里。

## 21. 完整示例：自定义事件的同步与异步发送

```cpp
#include <QCoreApplication>
#include <QDebug>
#include <QEvent>
#include <QObject>
#include <QString>
#include <utility>

const QEvent::Type MessageEventType =
    static_cast<QEvent::Type>(QEvent::registerEventType());

class MessageEvent final : public QEvent
{
public:
    explicit MessageEvent(QString message)
        : QEvent(MessageEventType)
        , message_(std::move(message))
    {
    }

    const QString &message() const { return message_; }

private:
    QString message_;
};

class Receiver final : public QObject
{
protected:
    bool event(QEvent *event) override
    {
        if (event->type() == MessageEventType) {
            const auto *messageEvent =
                static_cast<MessageEvent *>(event);
            qDebug() << messageEvent->message();
            return true;
        }

        return QObject::event(event);
    }
};

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);
    Receiver receiver;

    MessageEvent immediate(QStringLiteral("sendEvent: 立即处理"));
    QCoreApplication::sendEvent(&receiver, &immediate);

    QCoreApplication::postEvent(
        &receiver,
        new MessageEvent(QStringLiteral("postEvent: 稍后处理")));

    QCoreApplication::postEvent(
        &app,
        new QEvent(QEvent::Quit));

    return app.exec();
}
```

预期顺序：

1. `sendEvent` 的消息在进入 `app.exec()` 前立即输出。
2. `postEvent` 的消息进入队列。
3. 主事件循环启动后处理消息事件。
4. 随后处理退出事件并结束程序。

## 22. 常见错误

### 22.1 事件函数不返回

`event()` 和 `eventFilter()` 必须在所有路径返回明确布尔值，否则产生未定义行为。

### 22.2 拦截了不该拦截的事件

过滤器无条件返回 `true` 会让目标对象失去大量默认行为。只消费真正处理的事件。

### 22.3 未处理事件不调用父类

这可能破坏控件内部状态、焦点、绘制和输入行为。

### 22.4 把栈事件交给 postEvent

`postEvent()` 接管事件，必须传入动态分配对象。栈事件只能用于同步 `sendEvent()` 等不会跨越其生命周期的调用。

### 22.5 postEvent 后继续修改事件

所有权转移后，调用方不应再访问事件指针。

### 22.6 在事件处理中执行耗时操作

处理函数不返回，事件循环就无法继续。将耗时任务异步化。

### 22.7 用 processEvents 掩盖架构问题

界面暂时能动不代表状态安全。优先拆分任务或使用线程。

### 22.8 滥用嵌套事件循环

同步等待异步结果会制造重入。优先用信号、future 或状态机延续流程。

## 23. API 速查

| API | 作用 | 关键点 |
|---|---|---|
| `QCoreApplication::exec()` | 启动主事件循环 | 通常在 `main()` 末尾调用 |
| `QCoreApplication::quit()` | 请求正常退出 | 返回码 0 |
| `QCoreApplication::exit(code)` | 指定返回码退出 | 优先在主线程调用 |
| `QObject::event()` | 对象通用事件入口 | 未处理时调用父类 |
| `QObject::eventFilter()` | 在目标前观察事件 | true 表示停止传递 |
| `installEventFilter()` | 安装过滤器 | 过滤器与目标需同线程 |
| `removeEventFilter()` | 移除过滤器 | 激活期间也可移除 |
| `QEvent::type()` | 查询事件类型 | 再转换到正确派生类型 |
| `accept()` / `ignore()` | 修改 accepted 状态 | 具体语义依事件类型而定 |
| `sendEvent()` | 同步发送事件 | 调用者保留所有权 |
| `postEvent()` | 异步投递事件 | Qt 接管堆事件 |
| `registerEventType()` | 注册自定义类型编号 | 避免编号冲突 |
| `QEventLoop::exec()` | 启动局部事件循环 | 注意重入 |
| `QEventLoop::quit()` | 退出局部循环 | 常连接完成信号 |
| `processEvents()` | 主动处理部分事件 | 谨慎使用 |
| `deleteLater()` | 安排延迟删除事件 | 依赖事件循环 |

## 24. 自测题

1. 为什么耗时槽会让整个窗口失去响应？
2. `QObject::event()` 与 `mousePressEvent()` 是什么关系？
3. 事件过滤器返回 `true` 表示什么？
4. `sendEvent()` 与 `postEvent()` 的事件所有权有何区别？
5. 为什么不能把栈上的事件传给 `postEvent()`？
6. 排队信号为什么依赖接收线程的事件循环？
7. 为什么 `processEvents()` 可能造成重入？
8. 自定义事件编号为什么推荐通过 `registerEventType()` 获取？
9. 在事件过滤器里删除目标对象后为什么必须返回 `true`？
10. 信号与事件分别更适合什么通信方式？

### 参考答案

1. 槽未返回时 GUI 线程无法回到事件循环处理绘制和输入。
2. `event()` 是通用入口，`QWidget::event()` 按类型分派到具体虚函数。
3. 当前事件被消费，不再交给后续过滤器和目标对象。
4. 同步发送由调用者保留所有权；异步投递后 Qt 接管所有权。
5. 函数返回后栈对象失效，但事件可能尚未处理。
6. 槽调用被包装成事件，需要该线程取出并分发。
7. 当前函数尚未结束，处理其他事件可能再次调用当前对象并改变其状态或生命周期。
8. 避免不同组件使用相同用户事件编号。
9. 返回 false 会继续向已经删除的目标发送当前事件。
10. 信号适合低耦合的一对多状态通知；事件适合向特定对象投递并接入过滤/分发体系。

---

## 总结

Qt 的事件循环是定时器、窗口输入、排队信号、异步通知和延迟删除共同依赖的运行基础。事件首先进入队列或同步发送，再经过应用分发、事件过滤器和对象的 `event()`，最终到达具体处理函数。掌握事件系统的关键不只是会重写一个鼠标函数，而是理解同步与异步、事件所有权、对象线程归属、处理函数返回时机和重入风险。只要 GUI 线程能迅速返回事件循环，Qt 应用才会持续保持响应。
