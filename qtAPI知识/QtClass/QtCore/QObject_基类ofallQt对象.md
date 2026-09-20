# Qt QObject 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QObject>`  
> 所属模块：`Qt6::Core`  
> 继承：无  
> 定位：Qt 对象模型的根基：生命周期、事件、信号槽、属性和元对象反射

## 1. QObject 到底解决什么问题

`QObject` 不是一个“带几个通用函数的基类”，而是一套对象模型。Qt 的很多高级能力都建立在它上面：

- **父子对象树**：父对象析构时自动删除子对象。
- **线程亲和性**：对象在哪个线程，决定 queued slot、定时器和事件在哪个线程执行。
- **信号槽**：对象之间不必互相持有调用细节，就能传递状态变化和请求。
- **事件分发**：定时器、用户事件、延迟删除和自定义事件都进入 `event()`。
- **元对象系统**：让 Qt 能发现类名、信号、槽、属性、枚举，并支持动态连接、QML 和设计器。

```text
QObject
├─ parent / children       生命周期树
├─ thread / moveToThread   线程亲和性
├─ connect / disconnect    信号槽连接
├─ event / eventFilter     事件分发
├─ property / Q_PROPERTY   属性系统
└─ Q_OBJECT / moc          元对象信息
```

如果一个类需要信号、槽、`deleteLater()`、属性、事件过滤器或父子所有权，它通常应该继承 `QObject`。如果只是一个值类型，例如坐标、颜色或配置结构，则不应为了“方便”继承它。

## 2. 构建和最小示例

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

最小的自定义对象：

```cpp
#include <QObject>

class Counter final : public QObject
{
    Q_OBJECT
    Q_PROPERTY(int value READ value WRITE setValue NOTIFY valueChanged)

public:
    explicit Counter(QObject *parent = nullptr)
        : QObject(parent)
    {
    }

    int value() const { return m_value; }

public slots:
    void setValue(int value)
    {
        if (m_value == value)
            return;
        m_value = value;
        emit valueChanged(m_value);
    }

signals:
    void valueChanged(int value);

private:
    int m_value = 0;
};
```

`Q_OBJECT` 不是可有可无的注释。它让 `moc` 为类生成元对象代码；没有它，信号槽、属性和 `qobject_cast` 等能力可能无法正确工作。使用 CMake 的 Qt 自动处理功能时，确认 `CMAKE_AUTOMOC` 已启用。

## 3. 父子对象：最常用的所有权模型

```cpp
auto *window = new QWidget;
auto *button = new QPushButton(window);
```

这里 `window` 是 `button` 的 parent。销毁 `window` 时，Qt 会销毁 `button`。父子关系解决的是 QObject 的对象所有权，不是普通 C++ 指针的所有权：

- parent 只能是 QObject。
- 一个 QObject 同时只有一个 parent。
- `setParent()` 会把对象从旧父对象移到新父对象。
- 有 parent 的对象不能直接 `moveToThread()`。
- parent 不会自动管理非 QObject 成员，也不会管理裸指针指向的外部对象。

```cpp
auto *child = new Worker;
child->setParent(owner);       // owner 现在负责销毁 child
child->setParent(nullptr);     // child 脱离 owner，所有权重新由调用者负责
```

如果已经使用 parent 管理对象，不要再对同一对象调用 `delete`，也不要把它交给另一个会删除它的智能指针。

## 4. 信号槽：通信而不是所有权

现代 Qt 代码优先使用类型安全连接：

```cpp
connect(source, &Source::valueChanged,
        target, &Target::setValue);

connect(source, &Source::finished,
        target, [target] {
            target->refresh();
        });
```

带 context 的 lambda 更安全：

```cpp
connect(source, &Source::finished, target, [target] {
    target->refresh();
});
```

当 `target` 被销毁时，连接会自动失效，lambda 不会再被调用。不要无 context 地捕获一个可能提前销毁的裸 `this`。

连接类型的核心差别：

| 类型 | 执行位置 | 适用理解 | 常见使用场景 |
| --- | --- | --- | --- |
| `Qt::AutoConnection` | 同线程通常直接调用，跨线程通常排队 | 默认选择，按 sender/receiver 线程亲和性决定 | 大多数普通信号槽连接 |
| `Qt::DirectConnection` | 在发射信号的线程立即调用 | 必须确认接收对象和其状态允许被该线程直接访问 | 明确需要同步调用且线程边界已受控 |
| `Qt::QueuedConnection` | 排到接收对象所属线程的事件队列 | 跨线程更新 QObject 状态的常用方式，目标线程必须有事件循环 | Worker 与 GUI 或两个线程对象通信 |
| `Qt::BlockingQueuedConnection` | 发射线程阻塞到接收槽返回 | 同线程会死锁；跨线程也要防止接收槽反向等待发射线程 | 极少数需要同步握手的跨线程调用 |
| `Qt::UniqueConnection` | 避免重复建立同一个成员函数连接 | 对 lambda 不生效；不要把它当作业务去重机制 | 防止重复连接同一成员槽 |

信号槽不复制 QObject 的线程安全性。跨线程 queued 调用传递的参数必须能被 Qt 元类型系统处理；自定义类型需要 `Q_DECLARE_METATYPE` 和适当注册。

## 5. 线程亲和性：QObject 最容易被误解的部分

```cpp
worker->moveToThread(&thread);
```

线程亲和性决定：

- queued slot 在哪个线程执行。
- `QTimer` 的 timeout 在哪个线程产生。
- `deleteLater()` 投递到哪个事件队列。
- `event()` 收到的事件由哪个线程处理。

它不决定普通 C++ 成员函数的执行位置。直接调用：

```cpp
worker->doWork(); // 直接调用，在哪个线程调用就在哪个线程执行
```

跨线程应通过信号槽或 `QMetaObject::invokeMethod()`。移动对象前必须满足：

- 对象没有 parent。
- 调用 `moveToThread()` 的线程是对象当前所属线程。
- 目标线程对象仍然有效。
- 对象的 QObject 子对象一起满足迁移约束。

线程亲和性是事件调度边界，不是数据竞争保护。对普通成员的并发读写仍需互斥、原子变量、不可变消息或单线程归属。

## 6. 事件和事件过滤器

所有 QObject 都可能收到事件：

```cpp
bool Counter::event(QEvent *event)
{
    if (event->type() == QEvent::User + 1) {
        refresh();
        return true;
    }
    return QObject::event(event);
}
```

事件过滤器适合把观察逻辑放到另一个对象：

```cpp
class ShortcutFilter final : public QObject
{
protected:
    bool eventFilter(QObject *watched, QEvent *event) override
    {
        if (event->type() == QEvent::KeyPress) {
            // 只处理确实属于 watched 的事件
        }
        return QObject::eventFilter(watched, event);
    }
};

filter->installEventFilter(editor);
```

过滤器对象必须存活，并且通常要和被观察对象属于同一个线程。过滤器返回 `true` 表示事件已处理，不要忘记调用基类或返回 `false` 让事件继续传播。

## 7. 对象查找和 objectName

`objectName` 常用于调试、Qt Designer、测试和少量运行时查找：

```cpp
button->setObjectName("saveButton");
auto *saveButton = window->findChild<QPushButton *>("saveButton");
```

`findChild()` 默认递归查找子树；类型匹配由模板参数完成，名称匹配由 `objectName` 完成。它不是强类型依赖注入，也不应代替直接保存关键对象指针。大量调用会遍历对象树，性能敏感代码应缓存结果。

## 8. 动态属性和静态属性

静态属性使用 `Q_PROPERTY` 描述，适合需要 getter、setter、NOTIFY、绑定、QML 或设计器访问的状态：

```cpp
Q_PROPERTY(QString title READ title WRITE setTitle NOTIFY titleChanged)
```

动态属性不需要在类声明中预先定义：

```cpp
object->setProperty("sourceId", 42);
const QVariant value = object->property("sourceId");
```

动态属性适合少量扩展元数据，不适合替代正式的类接口。属性名拼写错误时，`setProperty()` 可能创建一个新的动态属性，问题不会在编译期暴露。

## 9. 延迟删除

```cpp
object->deleteLater();
```

它不是立即 `delete`，而是向对象所属线程投递 `DeferredDelete` 事件。事件循环运行后对象才会销毁。典型用法：

```cpp
connect(thread, &QThread::finished,
        worker, &QObject::deleteLater);
```

如果目标线程没有事件循环，或线程已经停止处理事件，延迟删除可能不会按预期发生。销毁跨线程对象时，要先设计停止、退出事件循环和等待顺序。

## 10. 元对象宏应该怎么选

- `Q_OBJECT`：QObject 派生类需要信号、槽、属性、动态元对象能力时使用。
- `Q_PROPERTY`：声明可反射、可绑定的属性。
- `Q_INVOKABLE`：把成员函数注册到元对象系统，可被 `invokeMethod()`、QML 等调用。
- `Q_ENUM`：让类内枚举进入元对象系统。
- `Q_FLAG`：让位标志枚举进入元对象系统。
- `Q_GADGET`：值类型不继承 QObject，但需要枚举、静态属性或元对象信息时使用。
- `Q_NAMESPACE`：为命名空间提供元对象和枚举反射能力。

宏必须放在正确的类或命名空间上下文中；它们不是运行时函数，不能用来替代普通 C++ 继承关系。

## 11. 常见误区

### 把 parent 当作线程归属

parent 只负责对象树所有权。线程归属由对象当前线程决定；有 parent 的对象不能直接迁移。

### 以为 queued connection 会自动创建线程

queued connection 只是把调用排到接收对象所属线程的事件队列。目标线程必须有正在运行的事件循环。

### 在跨线程对象上直接调用普通成员函数

直接调用不会自动排队，容易同时访问同一状态。用 queued signal/slot 或 `invokeMethod()`。

### 在析构函数中调用 `deleteLater()`

析构已经开始时，对象不能再依赖自己的事件循环完成删除。析构阶段应直接释放当前对象拥有的同步资源。

### 只凭 `sender()` 判断业务来源

`sender()` 只在槽被调用期间有意义，连接关系复杂或跨线程时可读性很差。更可靠的接口是显式传递来源 ID 或上下文数据。

### 动态属性拼写错误

`setProperty("titel", ...)` 可能悄悄创建错误属性。正式状态优先用 `Q_PROPERTY` 和编译器可检查的 setter。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QObject(QObject *parent = nullptr)` | 创建 QObject，并可立即加入 parent 的对象树。 | parent 获得销毁责任；QObject 不可复制，不能按值传递。 |
| 析构 | `~QObject()` | 销毁对象并断开连接、销毁 QObject 子对象。 | 不要和 parent 管理、智能指针或其他所有权重复删除。 |
| 属性 | `objectName()` | 读取对象名称。 | 名称主要服务于调试、设计器和查找，不保证唯一。 |
| 属性 | `setObjectName(const QString &)` | 设置对象名称。 | 修改会发出 `objectNameChanged`；名称不是对象所有权或类型信息。 |
| 属性 | `setObjectName(QAnyStringView)` | 用轻量字符串视图设置对象名称。 | Qt 6.4 起可用；传入的临时视图只在调用期间有效。 |
| 属性 | `bindableObjectName()` | 返回 objectName 的可绑定属性接口。 | 用于 Qt 属性绑定，不要用绑定绕过线程归属规则。 |
| 类型查询 | `isWidgetType()` | 判断对象是否为 QWidget 类型。 | 这是 Qt 内部类型标记，不等同于 C++ 的任意继承判断。 |
| 类型查询 | `isWindowType()` | 判断对象是否为窗口类型。 | 适合诊断和框架判断；不能代替具体窗口 API。 |
| 类型查询 | `isQuickItemType()` | 判断对象是否为 Qt Quick item 类型。 | Qt 6.4 起可用；不要用它代替 `qobject_cast` 的具体类型检查。 |
| 类型查询 | `isQmlExposed()` | 查询对象是否被 QML 暴露。 | Qt 6.11 起可用；暴露状态由 QML/框架管理。 |
| 信号控制 | `signalsBlocked()` | 查询当前对象是否屏蔽信号。 | 只影响该对象发出的信号，不影响事件、槽直接调用或其他对象。 |
| 信号控制 | `blockSignals(bool)` | 暂时阻止或恢复对象发出的信号，并返回旧状态。 | 适合短作用域；`destroyed()` 即使信号被屏蔽也会发出。 |
| 线程 | `thread()` | 返回对象当前的线程亲和性。 | 返回指针不转移所有权；空线程通常表示对象正在销毁或状态异常。 |
| 线程 | `moveToThread(QThread *)` | 将对象及 QObject 子对象迁移到目标线程。 | 对象不能有 parent，调用者需是当前线程；不会自动保护普通成员数据。 |
| 定时器 | `startTimer(int, Qt::TimerType)` | 为对象注册底层定时器，返回 timer ID。 | 必须在对象所属线程调用；需要重写 `timerEvent()` 才直接使用。 |
| 定时器 | `startTimer(std::chrono::nanoseconds, Qt::TimerType)` | 用 chrono 时长注册底层定时器。 | Qt 6.8 起使用强类型时长；仍依赖所属线程事件循环。 |
| 定时器 | `killTimer(int)` | 停止指定的旧式 timer ID。 | 只能停止属于该对象的 timer；不要使用已重启后的旧 ID。 |
| 定时器 | `killTimer(Qt::TimerId)` | 停止强类型 Qt timer ID。 | Qt 6.8 起可用；调用线程和对象线程必须正确。 |
| 查找 | `findChild<T>(QAnyStringView, FindChildOptions)` | 按类型和名称递归查找第一个子对象。 | 找不到返回空指针；查找结果不拥有对象，关键对象应缓存。 |
| 查找 | `findChild<T>(FindChildOptions)` | 按类型查找第一个子对象，不限制名称。 | Qt 6.7 起提供；同类型多个对象时结果依赖对象树顺序。 |
| 查找 | `findChildren<T>(QAnyStringView, FindChildOptions)` | 按类型和名称递归查找全部子对象。 | 返回列表不拥有对象；大对象树频繁调用会有遍历成本。 |
| 查找 | `findChildren<T>(FindChildOptions)` | 按类型查找全部子对象，不限制名称。 | Qt 6.3 起提供；明确使用 `FindDirectChildrenOnly` 可避免递归。 |
| 查找 | `findChildren<T>(QRegularExpression, FindChildOptions)` | 按类型和 objectName 正则查找全部子对象。 | 正则匹配增加复杂度；不要把它当作高频查询索引。 |
| 对象树 | `children()` | 返回直接子对象列表。 | 列表引用属于 QObject 内部；不要长期保存并假设顺序不变。 |
| 对象树 | `setParent(QObject *)` | 改变对象的父对象和所有权归属。 | 新 parent 必须兼容线程亲和性；设置 parent 不会复制对象。 |
| 事件 | `event(QEvent *)` | QObject 处理自身事件的总入口。 | 重写时未处理的事件应交给基类；不要在这里执行长时间工作。 |
| 事件 | `eventFilter(QObject *, QEvent *)` | 处理被安装过滤器对象观察到的事件。 | 返回 true 会截断事件；过滤器与被观察对象通常必须同线程。 |
| 过滤器 | `installEventFilter(QObject *)` | 给对象安装另一个 QObject 作为事件过滤器。 | 过滤器对象必须存活且线程兼容；安装顺序会影响多个过滤器。 |
| 过滤器 | `removeEventFilter(QObject *)` | 移除已安装的事件过滤器。 | 对象销毁会自动移除连接，但主动移除能缩小观察范围。 |
| 连接 | `connect(sender, signal, receiver, method, type)` | 建立信号到成员槽或信号的连接。 | 新代码优先指针语法；确认连接类型、参数兼容性和对象生命周期。 |
| 连接 | `connect(sender, QMetaMethod, receiver, QMetaMethod, type)` | 用运行时元方法建立连接。 | 适合反射或插件边界；编译器无法替你检查签名。 |
| 连接 | `connect(sender, signal, functor)` | 把信号连接到无 context 的 functor。 | 默认是直接连接并以 sender 作为上下文；lambda 捕获外部对象要谨慎。 |
| 连接 | `connect(sender, signal, context, functor, type)` | 把信号连接到受 context 生命周期保护的 functor。 | 推荐形式；context 销毁后连接自动失效。 |
| 连接 | `connect(sender, signal, receiver, method, type)` | 用成员函数指针建立类型安全的信号槽连接。 | 重载信号要用 `qOverload` 或 lambda 明确选择。 |
| 断开 | `disconnect(connection)` | 按连接句柄断开一条连接。 | 句柄失效或已断开时返回 false；保存句柄比按字符串全局断开更安全。 |
| 断开 | `disconnect(sender, signal, receiver, method)` | 按发送者、信号、接收者和方法匹配断开。 | 过滤条件越宽，误断开的风险越大。 |
| 断开 | `disconnect(sender, QMetaMethod, receiver, QMetaMethod)` | 用元方法匹配断开连接。 | 适合反射代码；必须保证元方法来自正确的类。 |
| 断开 | `disconnect(sender, signal, receiver, method)` | 用成员函数指针断开类型安全连接。 | lambda 连接不能靠成员函数指针重建匹配，优先保存连接句柄。 |
| 断开 | `disconnect(signal, receiver, method) const` | 从当前对象出发匹配并断开连接。 | 默认参数很宽，谨慎使用无条件断开。 |
| 诊断 | `dumpObjectTree()` | 输出对象及其子对象树。 | 主要用于调试；对象名称和 parent 关系应先设置清楚。 |
| 诊断 | `dumpObjectInfo()` | 输出对象的元对象和连接相关诊断信息。 | 调试辅助，不是稳定的程序接口。 |
| 动态属性 | `setProperty(const char *, const QVariant &)` | 设置静态或动态属性。 | 拼写错误可能创建新的动态属性；正式状态优先用 Q_PROPERTY。 |
| 动态属性 | `setProperty(const char *, QVariant &&)` | 移动一个 QVariant 设置属性。 | Qt 6.6 起可用；仍需确认属性名和类型。 |
| 动态属性 | `property(const char *)` | 读取静态或动态属性值。 | 未知属性返回无效 QVariant；要检查 `isValid()` 和类型。 |
| 动态属性 | `dynamicPropertyNames()` | 返回当前动态属性名称。 | 不包含所有静态 Q_PROPERTY；列表是状态快照。 |
| 信号 | `destroyed(QObject *)` | 对象即将销毁时发出的信号。 | 不能被 `blockSignals()` 屏蔽；不要在槽中访问已销毁对象状态。 |
| 信号 | `objectNameChanged(QString)` | objectName 改变时发出的通知信号。 | 只在名称实际改变时关心刷新逻辑，避免无意义回写。 |
| 对象树 | `parent()` | 返回当前父对象。 | 不转移所有权；对象可能在异步回调期间已被销毁，必要时使用 `QPointer`。 |
| 类型 | `inherits(const char *)` | 按元对象类名判断继承关系。 | 依赖 Q_OBJECT 元对象；新代码通常优先 `qobject_cast`。 |
| 生命周期 | `deleteLater()` | 向对象所属线程投递延迟删除请求。 | 依赖事件循环；不能把它当作立即销毁，也不要再使用待删除对象。 |
| 槽扩展 | `sender()` | 在当前槽调用期间返回发送信号的对象。 | 只适合短暂诊断；不要用它构造隐式业务依赖。 |
| 槽扩展 | `senderSignalIndex()` | 返回当前 sender 发出信号在元对象中的索引。 | 只在槽调用期间有意义；重载和继承会使代码难读。 |
| 槽扩展 | `receivers(const char *)` | 查询指定信号当前连接数量。 | 受保护函数；数量可能随时变化，不能作为同步判断。 |
| 槽扩展 | `isSignalConnected(QMetaMethod)` | 查询某个信号是否有连接。 | 受保护函数；可用于昂贵信号的优化，但不能替代正确发信号。 |
| 事件扩展 | `timerEvent(QTimerEvent *)` | 处理 `startTimer()` 注册的低层定时器事件。 | 处理完应快速返回；不用底层 timer 时优先使用 QTimer。 |
| 事件扩展 | `childEvent(QChildEvent *)` | 观察子对象添加、移除或对象树变化。 | 事件到达时子对象状态可能尚未完全配置，不要过早使用业务状态。 |
| 事件扩展 | `customEvent(QEvent *)` | 处理自定义事件类型。 | 自定义事件通常通过 `postEvent()` 投递；明确事件类型和所有权。 |
| 连接扩展 | `connectNotify(QMetaMethod)` | 在某个信号首次建立连接等场景通知派生类。 | 受保护虚函数；不要在其中调用可能再次触发连接操作的 QObject API。 |
| 连接扩展 | `disconnectNotify(QMetaMethod)` | 在信号连接被移除时通知派生类。 | 受保护虚函数；线程调用上下文和锁规则要按 QObject 文档处理。 |
| 翻译 | `tr(const char *, const char *, int)` | 按类上下文查找可翻译字符串。 | 源文本要稳定；复数文本正确传入 n；结果不适合作为持久化键。 |
| 宏 | `Q_OBJECT` | 为 QObject 派生类启用元对象、信号槽和属性能力。 | 需要 moc；类声明位置和构建系统必须正确。 |
| 宏 | `Q_PROPERTY(...)` | 声明可反射、可通知或可绑定的属性。 | READ、WRITE、NOTIFY、BINDABLE 等字段要与实际成员契约一致。 |
| 宏 | `Q_INVOKABLE` | 把成员函数注册为可通过元对象调用的函数。 | 参数必须是 Qt 元类型可处理的形式；不是线程安全声明。 |
| 宏 | `Q_SIGNAL` / `Q_SIGNALS` | 声明信号或信号区域。 | 信号由对象发出，不应在外部直接调用信号实现。 |
| 宏 | `Q_SLOT` / `Q_SLOTS` | 声明槽或槽区域。 | 槽可以被信号、元对象或普通代码调用，线程语义取决于调用方式。 |
| 宏 | `Q_EMIT` | 标记信号发射位置。 | 它主要是可读性宏，不会自动改变线程或连接类型。 |
| 宏 | `Q_ENUM` | 将类内枚举注册到元对象系统。 | 枚举必须属于包含 Q_OBJECT 或 Q_GADGET 的类。 |
| 宏 | `Q_FLAG` | 将位标志枚举注册到元对象系统。 | 枚举值要按位定义；注册不会自动验证组合合法性。 |
| 宏 | `Q_ENUM_NS` | 将命名空间枚举注册到命名空间元对象。 | 命名空间必须使用 Q_NAMESPACE。 |
| 宏 | `Q_FLAG_NS` | 将命名空间位标志注册到命名空间元对象。 | 与 Q_FLAG 相同，需注意组合值语义。 |
| 宏 | `Q_NAMESPACE` | 为命名空间生成元对象信息。 | 适合无 QObject 实例的枚举反射和 QML 暴露。 |
| 宏 | `Q_NAMESPACE_EXPORT(EXPORT_MACRO)` | 为导出库的命名空间元对象指定导出宏。 | 跨动态库使用时导出宏必须正确。 |
| 宏 | `Q_GADGET` | 为值类型启用轻量元对象能力。 | 不提供 parent、事件循环或信号槽；不要把它当 QObject。 |
| 宏 | `Q_GADGET_EXPORT(EXPORT_MACRO)` | 为导出库的 gadget 元对象指定导出宏。 | Qt 6.3 起可用；检查动态库符号导出。 |
| 宏 | `Q_CLASSINFO(Name, Value)` | 向元对象添加自定义类信息。 | 适合插件、设计器或反射元数据，不会自动生成运行时行为。 |
| 宏 | `Q_INTERFACES(...)` | 声明 QObject 实现的接口以支持元对象查询。 | 接口还要配合 `Q_DECLARE_INTERFACE`；它不是 C++ 多态继承替代品。 |
| 宏 | `Q_REVISION` | 为属性、信号或方法声明版本修订号。 | 主要用于 QML/元对象版本控制，必须与暴露策略一致。 |
| 宏 | `Q_MOC_INCLUDE` | 指示 moc 生成代码需要包含的头文件。 | Qt 6 起用于解决前置声明和 moc 解析边界。 |
| 宏 | `Q_SET_OBJECT_NAME(Object)` | 在调试构建中按变量名设置 QObject 名称的辅助宏。 | 只适合诊断便利，不能依赖它提供稳定业务名称。 |
| 编译开关 | `QT_NO_CONTEXTLESS_CONNECT` | 禁用无 context 的 functor 连接重载。 | 推荐在大型项目中启用，迫使连接代码明确生命周期上下文。 |
| 编译开关 | `QT_NO_NARROWING_CONVERSIONS_IN_CONNECT` | 禁止连接参数发生窄化转换。 | 有助于在编译期发现信号槽参数精度损失。 |

---

### 一句话总结

`QObject` 的核心不是“所有 Qt 类的父类”这句口号，而是对象树、事件循环、线程亲和性、信号槽和元对象系统的共同契约。先把对象归属和执行线程想清楚，再使用 `connect()`、`moveToThread()`、`deleteLater()` 和属性系统，Qt 的大多数行为就会变得可预测。
