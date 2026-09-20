# Qt QObject 深入笔记（下）：信号、事件、线程与安全销毁

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QObject>`  
> 所属模块：`Qt6::Core`  
> 前篇：`QObject（上）_对象树元对象与属性.md`

上篇解决了 QObject 的身份和所有权。本篇继续处理它的动态行为：对象如何通信、事件如何被过滤、定时器依赖哪个事件循环、对象如何迁移线程，以及为什么跨线程销毁通常必须使用 `deleteLater()`。

## 1. 信号槽的基本模型

信号表示“某件事已经发生”，槽或可调用对象负责响应。发送者不需要知道有多少接收者：

```cpp
QObject::connect(button, &QPushButton::clicked,
                 controller, &Controller::submit);
```

连接成功返回 `QMetaObject::Connection`。一个信号可以连接多个槽，同一个槽也可接收多个信号。默认情况下，连接顺序决定同一线程直接调用槽的顺序，但业务代码不应依赖复杂连接图的隐式先后关系。

## 2. 推荐的类型安全 `connect`

### 2.1 成员信号到成员函数

```cpp
QMetaObject::Connection connection = QObject::connect(
    sender, &Sender::valueChanged,
    receiver, &Receiver::setValue);
```

编译器会检查信号参数是否能传给槽。槽参数可以少于信号参数：

```cpp
connect(slider, &QSlider::valueChanged,
        label, [label](int value) {
    label->setNum(value);
});
```

### 2.2 重载信号

```cpp
connect(comboBox,
        &QComboBox::currentIndexChanged,
        this,
        &Page::selectIndex);
```

若编译器无法判断重载，使用 `qOverload`：

```cpp
connect(spinBox,
        qOverload<int>(&QSpinBox::valueChanged),
        this,
        &Page::updateCount);
```

### 2.3 Lambda 一定要给 context

```cpp
connect(reply, &QNetworkReply::finished,
        page, [page, reply] {
    page->showData(reply->readAll());
});
```

这里 `page` 是 context：它销毁时连接自动断开，lambda 也会在 `page` 所属线程执行。省略 context 的三参数 lambda 连接只与 sender 生命周期绑定，捕获的页面可能先销毁，风险很高。

## 3. 旧式字符串连接

```cpp
connect(sender, SIGNAL(valueChanged(int)),
        receiver, SLOT(setValue(int)));
```

这种语法为了兼容旧代码仍存在，但参数拼写只能在运行时检查，重构工具也难以跟踪。新代码优先函数指针语法。只有接口在运行时才知道、需要按元对象动态连接时，才使用 `QMetaMethod` 或字符串形式。

## 4. 连接类型 `Qt::ConnectionType`

### 4.1 `AutoConnection`

默认类型。发射信号时，如果接收对象属于当前线程，就直接调用槽；否则将调用排入接收对象线程的事件队列。

判断依据是**发射信号时的当前线程与 receiver 的线程亲和性**，不是 sender 对象保存在哪个线程。

### 4.2 `DirectConnection`

```cpp
connect(sender, &Sender::ready,
        receiver, &Receiver::consume,
        Qt::DirectConnection);
```

槽在发射信号的线程立即执行。跨线程使用时，接收对象的成员函数会在错误线程运行，除非槽本身被严格设计为线程安全函数。

### 4.3 `QueuedConnection`

```cpp
connect(worker, &Worker::resultReady,
        window, &Window::showResult,
        Qt::QueuedConnection);
```

调用被封装为事件，随后在 receiver 所属线程的事件循环执行。参数类型必须可复制并被 Qt 元类型系统识别；自定义类型可用 `Q_DECLARE_METATYPE`，必要时调用 `qRegisterMetaType<T>()`。

### 4.4 `BlockingQueuedConnection`

发送线程会等待接收线程完成槽。若双方是同一线程会死锁；若两个线程互相阻塞调用也会死锁。只在边界非常清楚的同步桥接中使用，GUI 代码通常应避免。

### 4.5 `UniqueConnection` 与 `SingleShotConnection`

```cpp
connect(sender, &Sender::ready,
        receiver, &Receiver::consume,
        Qt::UniqueConnection);

connect(sender, &Sender::ready,
        receiver, &Receiver::consume,
        Qt::SingleShotConnection);
```

`UniqueConnection` 防止同一成员信号到同一成员槽的重复连接；它对 lambda、自由函数和 functor 的唯一性判断有限，不应依赖它为匿名可调用对象去重。`SingleShotConnection` 在第一次调用后自动断开。

标志可以与基本连接类型组合，具体写法以 `Qt::ConnectionType` 位标志规则为准。

## 5. 保存和断开连接

```cpp
QMetaObject::Connection c = connect(...);

if (!QObject::disconnect(c))
    qWarning() << "connection was already disconnected";
```

精确保存 connection handle 比“断开 sender 的所有连接”更安全。宽泛断开可能破坏其他模块或框架内部连接：

```cpp
// 谨慎：会断开 sender 到 receiver 的所有匹配连接
QObject::disconnect(sender, nullptr, receiver, nullptr);
```

对象销毁时相关连接会自动断开，但自动断开不能解决 lambda 捕获外部裸指针的问题；context 必须设置正确。

## 6. 信号阻塞

```cpp
const bool oldState = object->blockSignals(true);
updateManyProperties();
object->blockSignals(oldState);
```

更可靠的是 RAII：

```cpp
{
    QSignalBlocker blocker(object);
    updateManyProperties();
} // 自动恢复原状态
```

`signalsBlocked()` 查询当前状态。信号被阻塞时不会排队等待以后补发；它们直接被丢弃。`destroyed()` 即使在 signals blocked 状态下仍会发出。

不要用信号阻塞掩盖错误的数据依赖。若观察者必须得到最终状态，解除阻塞后显式发出一个批量更新或模型重置信号。

## 7. `sender()`、`receivers()` 与连接通知

### 7.1 `sender()` 和 `senderSignalIndex()`

```cpp
void Controller::handleAction()
{
    auto *action = qobject_cast<QAction *>(sender());
    if (!action)
        return;
}
```

`sender()` 只在由信号直接进入的槽调用期间有意义。嵌套信号、跨线程调用和后续异步回调会使它难以推理。优先使用 lambda 显式捕获必要身份。

### 7.2 `receivers()` 与 `isSignalConnected()`

这些受保护接口可用于避免昂贵的信号数据准备，但并发连接变化使结果只是瞬时快照：

```cpp
if (isSignalConnected(QMetaMethod::fromSignal(&Producer::heavyDataReady)))
    emit heavyDataReady(buildExpensivePayload());
```

检查后连接可能立即变化，不能把它用于正确性判断。

### 7.3 `connectNotify()` / `disconnectNotify()`

派生类可重载这两个函数观察某信号是否有监听者。它们可能在发起 connect/disconnect 的线程调用，并且 QObject 内部互斥量可能处于锁定状态；重载中不要再次调用可能锁定 QObject 的函数，也不要假设当前线程就是对象所属线程。

## 8. 事件入口 `event()`

所有发送给对象的事件先进入：

```cpp
bool MyObject::event(QEvent *event)
{
    if (event->type() == MyEventType) {
        handleMyEvent(static_cast<MyEvent *>(event));
        return true;
    }
    return QObject::event(event);
}
```

返回 `true` 表示事件已处理；返回 `false` 表示未处理。没有处理的类型必须交给基类，否则定时器、延迟删除等 QObject 内部事件可能失效。

## 9. 自定义事件

### 9.1 定义类型和事件

```cpp
class ResultEvent final : public QEvent
{
public:
    static QEvent::Type typeId()
    {
        static const int id = QEvent::registerEventType();
        return static_cast<QEvent::Type>(id);
    }

    explicit ResultEvent(QString value)
        : QEvent(typeId()), result(std::move(value)) {}

    QString result;
};
```

### 9.2 投递与处理

```cpp
QCoreApplication::postEvent(receiver,
                            new ResultEvent("done"));

void Receiver::customEvent(QEvent *event)
{
    if (event->type() == ResultEvent::typeId()) {
        auto *result = static_cast<ResultEvent *>(event);
        consume(result->result);
        return;
    }
    QObject::customEvent(event);
}
```

`postEvent()` 接管堆上事件的所有权并异步投递；`sendEvent()` 同步调用且不接管栈事件。不要把栈事件传给 `postEvent()`。

## 10. 事件过滤器

```cpp
watched->installEventFilter(filterObject);

bool Filter::eventFilter(QObject *watched, QEvent *event)
{
    if (watched == lineEdit
        && event->type() == QEvent::KeyPress) {
        auto *key = static_cast<QKeyEvent *>(event);
        if (key->key() == Qt::Key_Escape) {
            lineEdit->clear();
            return true; // 停止继续传递
        }
    }
    return QObject::eventFilter(watched, event);
}
```

过滤器和被监视对象必须位于同一线程，否则过滤器不会被调用。后安装的过滤器通常先执行。返回 `true` 会吞掉事件；只观察不拦截时必须返回基类结果或 `false`。

删除被监视对象时要立即返回 `true`，避免 Qt 继续把同一个事件发送给已销毁对象：

```cpp
delete watched;
return true;
```

移除过滤器：

```cpp
watched->removeEventFilter(filterObject);
```

任一对象销毁后相关过滤关系会自动清理。

## 11. 子对象事件 `childEvent()`

父对象在子项加入、移除或状态变化时收到 `QChildEvent`：

```cpp
void Owner::childEvent(QChildEvent *event)
{
    if (event->added())
        qDebug() << "added:" << event->child();
    else if (event->removed())
        qDebug() << "removed:" << event->child();

    QObject::childEvent(event);
}
```

收到 ChildAdded 时子对象可能尚未构造完成，收到 ChildRemoved 时可能已经部分析构，不能在这里无条件向下转换并调用派生接口。

## 12. QObject 基础定时器

### 12.1 启动和处理

```cpp
class Poller : public QObject
{
public:
    using QObject::QObject;

    void start()
    {
        m_timerId = startTimer(std::chrono::seconds(1),
                               Qt::CoarseTimer);
    }

protected:
    void timerEvent(QTimerEvent *event) override
    {
        if (event->timerId() == m_timerId)
            poll();
        else
            QObject::timerEvent(event);
    }

private:
    int m_timerId = 0;
};
```

停止：

```cpp
killTimer(m_timerId);
m_timerId = 0;
```

Qt 6.8 起还有强类型 `Qt::TimerId` 相关重载。普通业务更适合 `QTimer`，因为它支持信号槽、single-shot 和属性；`startTimer()` 适合轻量底层对象。

定时器依赖对象所属线程的事件循环。必须在该线程启动和停止，回调也在该线程执行。

## 13. 线程亲和性 `thread()`

```cpp
QThread *ownerThread = object->thread();
```

线程亲和性表示 queued signal 和 posted event 将在哪个线程处理，不等于对象拥有一个专属线程。对象默认属于创建它的线程。

父子对象必须属于同一线程：

- `setParent()` 跨线程失败。
- 移动父对象会一起移动其子树。
- 有父对象的对象不能单独 `moveToThread()`。
- QObject 值成员若没有 parent，不会自动随外层对象迁移；需要明确设计。

## 14. `moveToThread()`

```cpp
auto *thread = new QThread;
auto *worker = new Worker;

worker->moveToThread(thread);
connect(thread, &QThread::started,
        worker, &Worker::startWork);
connect(thread, &QThread::finished,
        worker, &QObject::deleteLater);
thread->start();
```

Qt 6.7 起 `moveToThread()` 返回 `bool`，应检查失败：

```cpp
if (!worker->moveToThread(thread))
    qWarning() << "worker has a parent or migration is invalid";
```

一般只能从对象当前所属线程把它“推”到另一个线程；对象无亲和性时存在特殊的“拉入”规则。迁移不是任意线程都能安全调用的线程安全 API。

移动时对象的活动定时器会停止并在目标线程重新启动。频繁来回迁移可能不断推迟定时事件。

## 15. `delete` 与 `deleteLater()`

### 15.1 为什么需要延迟删除

直接删除正在处理事件、正在发信号或属于另一线程的 QObject 可能崩溃：

```cpp
object->deleteLater();
```

`deleteLater()` 向对象所属线程投递 DeferredDelete 事件，控制权返回事件循环后再销毁对象。它是跨线程请求销毁的标准方式。

### 15.2 事件循环边界

- 在主事件循环启动前调用：对象会在事件循环开始后删除。
- 主事件循环已经停止后调用：对象不会自动删除。
- 对象线程没有运行事件循环：通常在线程结束时清理，具体应配合 `QThread::finished`。
- 进入另一个嵌套事件循环不一定立即处理外层循环安排的 deferred delete；不要依赖嵌套循环作为销毁同步点。

不要在调用 `deleteLater()` 后继续解引用裸指针。使用 `QPointer` 观察对象是否已销毁：

```cpp
QPointer<Worker> safeWorker = worker;
worker->deleteLater();

if (safeWorker)
    qDebug() << "deletion is still pending";
```

## 16. `destroyed()` 信号

```cpp
connect(object, &QObject::destroyed,
        owner, [owner](QObject *dead) {
    owner->removeReference(dead);
});
```

`destroyed(QObject *)` 在对象析构过程中发出，即使信号被阻塞也会发出。接收者只能把参数作为身份标识，不应调用其虚函数或读取派生类状态。

Qt 容器持有裸 QObject 指针时，使用该信号移除条目，或直接存 `QPointer<T>` 让指针在销毁后自动变空。

## 17. 翻译函数 `tr()`

```cpp
setErrorString(tr("Connection failed"));
```

`tr(sourceText, disambiguation, n)` 使用当前类的元对象名称作为翻译上下文：

```cpp
label->setText(tr("%n file(s)", nullptr, count));
```

动态切换语言后，已经计算出的 QString 不会自动更新；Widgets 应处理 `QEvent::LanguageChange`，QML 引擎应重新翻译绑定。

## 18. 综合工作对象模式

```cpp
class Worker final : public QObject
{
    Q_OBJECT
public slots:
    void process(Request request)
    {
        if (m_stopping)
            return;
        emit resultReady(calculate(request));
    }

    void stop() { m_stopping = true; }

signals:
    void resultReady(Result result);

private:
    bool m_stopping = false;
};

auto *thread = new QThread(qApp);
auto *worker = new Worker;
worker->moveToThread(thread);

connect(controller, &Controller::requestReady,
        worker, &Worker::process);
connect(worker, &Worker::resultReady,
        controller, &Controller::acceptResult);
connect(thread, &QThread::finished,
        worker, &QObject::deleteLater);
connect(thread, &QThread::finished,
        thread, &QObject::deleteLater);

thread->start();
```

`Worker` 的槽在其线程事件循环执行；结果通过 queued connection 回到 controller 线程。关闭时先让 worker 停止接收新工作，再调用 `thread->quit()` 和合理的等待策略。

## 19. 常见误区

### “用了信号槽就是线程安全”

只有 queued delivery 把执行切到 receiver 线程。DirectConnection 或没有 context 的 lambda 仍可能在发送线程运行，共享数据仍需同步。

### “parent 会自动把对象移到自己的线程”

跨线程设置 parent 会失败。先在正确线程创建对象，或无 parent 状态下合法迁移，再建立父子关系。

### “disconnect 后排队调用一定消失”

已经进入事件队列的 queued call 可能仍会执行。槽中还要检查对象状态、请求代次或取消标记。

### “deleteLater 立刻把指针变空”

它只是安排未来销毁。裸指针不会自动清空，使用 `QPointer` 或明确状态。

### “事件过滤器返回 true 更保险”

返回 true 会吞掉事件，控件默认行为可能全部失效。仅在已经完整处理并明确阻止后续传递时返回 true。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 信号槽连接 | `connect(...)`：函数指针到成员函数 | 建立编译期类型安全的信号到槽连接，并返回 `QMetaObject::Connection` | 信号和槽的参数在编译期检查；重载信号可用 `qOverload` 明确选择 |
| 信号槽连接 | `connect(...)`：带 context 的 lambda/functor | 把可调用对象接到信号上，并让 context 管理连接生命周期和执行线程 | 捕获 `this` 或其他 QObject 时优先提供 context；context 销毁后不会再调用 lambda |
| 信号槽连接 | `connect(...)`：`QMetaMethod` 或字符串重载 | 在运行时按元对象信息建立连接 | 字符串形式缺少编译期检查；只有动态接口或旧代码兼容时才使用 |
| 信号槽连接 | `Qt::ConnectionType` | 指定连接采用直接调用、事件队列、阻塞队列、唯一连接或单次连接等策略 | `AutoConnection` 依据发射时线程与 receiver 亲和性决定；`BlockingQueuedConnection` 同线程会死锁 |
| 信号槽连接 | `QMetaObject::Connection` | 表示一次具体连接的句柄，可保存并精确断开 | 句柄本身不保证连接仍然存在；对象销毁或已断开后再操作要接受失败结果 |
| 信号槽连接 | `disconnect(...)` | 断开指定连接、指定对象间的连接或全部匹配连接 | 优先断开保存的 connection handle；宽泛断开可能误伤其他模块和框架连接 |
| 信号控制 | `blockSignals(bool)` | 暂时禁止对象发出普通信号，并返回之前的阻塞状态 | 被阻塞的信号不会缓存补发；`destroyed()` 即使阻塞也会发出，复杂批量更新更适合 `QSignalBlocker` |
| 信号控制 | `signalsBlocked()` | 查询当前是否处于信号阻塞状态 | 只是瞬时状态，不能作为并发同步或业务状态机依据 |
| 信号诊断 | `sender()` / `senderSignalIndex()` | 在槽执行期间获取当前信号发送者及信号索引 | 只适合直接信号调用场景；跨线程、嵌套信号和异步逻辑中不要依赖隐式 sender 身份 |
| 信号诊断 | `receivers(const char *)` / `isSignalConnected(QMetaMethod)` | 估算某个信号当前是否有接收者 | 结果可能随时变化，只能用于省略昂贵准备，不能用于并发正确性判断 |
| 连接通知 | `connectNotify()` / `disconnectNotify()` | 在派生类中观察某个信号何时建立或断开连接 | 回调可能来自发起连接的线程，且 QObject 内部锁可能已持有；不要在其中调用会再次锁 QObject 的操作 |
| 事件分发 | `event(QEvent *)` | 接收并分派发给对象的各种事件，是 QObject 事件处理总入口 | 自定义处理后返回 `true`；未处理事件应交给基类，否则定时器和延迟删除等行为可能失效 |
| 事件分发 | `customEvent(QEvent *)` | 处理未被更具体接口消费的自定义事件 | 事件通常由 `QCoreApplication::postEvent()` 异步投递；不要把栈事件交给 `postEvent()` |
| 事件过滤 | `installEventFilter(QObject *)` | 让过滤器在被监视对象处理事件前观察或拦截事件 | 过滤器和被监视对象必须在同一线程；返回 `true` 会阻止后续默认处理 |
| 事件过滤 | `removeEventFilter(QObject *)` | 移除已经安装的事件过滤器 | 对象销毁时相关过滤关系会自动清理；被监视对象被删除时过滤器应立即停止继续处理 |
| 子对象事件 | `childEvent(QChildEvent *)` | 观察子对象加入、移除或状态变化 | `ChildAdded` 时子对象可能尚未构造完成，`ChildRemoved` 时可能已开始析构，不能无条件调用派生接口 |
| 基础定时器 | `startTimer(int, Qt::TimerType)` / `startTimer(std::chrono::milliseconds, Qt::TimerType)` | 向对象所属线程注册低层定时器，并返回 timer ID | 必须在对象所属线程启动；回调依赖该线程事件循环，普通业务优先使用 `QTimer` |
| 基础定时器 | `killTimer(int)` / `killTimer(Qt::TimerId)` | 停止由 `startTimer()` 注册的定时器 | 只会停止对应 ID；应在正确线程调用并在停止后清理本地 ID |
| 基础定时器 | `timerEvent(QTimerEvent *)` | 接收基础定时器到期事件的虚函数入口 | 覆盖后要按 ID 区分多个定时器；不认识的事件交给基类 |
| 线程亲和性 | `thread()` | 返回对象的线程亲和性，即 queued 调用和 posted event 的处理线程 | 它不是“当前正在执行的线程”，也不表示对象拥有一条专属线程 |
| 线程亲和性 | `moveToThread(QThread *)` | 把对象及其 QObject 子树迁移到目标线程 | 有 parent 时不能单独迁移；通常必须从对象当前线程发起，并检查 Qt 6.7 起的 `bool` 返回值 |
| 生命周期 | `deleteLater()` | 向对象所属线程安排一次延迟销毁 | 依赖事件循环处理 DeferredDelete；调用后不要继续解引用裸指针，必要时使用 `QPointer` |
| 生命周期 | `destroyed(QObject *)` | 在对象析构过程中通知外部清理引用或记录身份 | 对象已经进入销毁流程，不要在接收槽中调用其业务接口或读取派生类状态 |
| 国际化 | `tr(const char *, const char *, int)` | 按当前类元对象上下文查找翻译文本，并支持复数形式 | 已生成的 `QString` 不会因语言切换自动更新；界面需响应语言变化重新取文案 |

---

### 一句话总结

`QObject` 把身份、所有权、通信、事件和线程归属绑定在同一个对象上：用 parent 管生命周期，用带 context 的类型安全连接通信，用事件循环承载 queued 调用与定时器，用 `moveToThread()` 管亲和性，并用 `deleteLater()` 在正确线程安全收尾。
