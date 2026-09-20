# Qt QEvent 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QEvent>`  
> 所属模块：`Qt6::Core`  
> 类型性质：所有 Qt 事件的基类，具有接收状态和事件类型  
> 相关类型：`QObject`、`QCoreApplication`、`QEventLoop`、`QInputEvent`、`QPointerEvent`

## 1. 它解决什么问题

`QEvent` 是 Qt 事件系统里的基础对象。Qt 的事件循环从操作系统或应用内部取得事件，将其封装为 `QEvent` 的某个派生类，再交给目标 `QObject` 的 `event()` 或具体事件处理函数。

基类 `QEvent` 本身只保存两类核心信息：

1. `type()`：这是什么事件；
2. `accepted`：接收者是否接受这个事件。

鼠标位置、按键、窗口尺寸、定时器 ID、拖放数据等具体参数，都由派生类保存，例如 `QMouseEvent`、`QKeyEvent`、`QResizeEvent`、`QTimerEvent` 和 `QDropEvent`。

因此，`QEvent` 不是“业务数据对象”，也不是可以随意复制和长期保存的消息值类型。它通常只在事件分发和处理期间有效。

### 1.1 Qt 事件流

一个典型事件从产生到处理，大致经过：

```text
操作系统/Qt 内部/应用代码
        |
        v
创建某个 QEvent 派生对象
        |
        +--> QCoreApplication::sendEvent()   同步调用
        |
        +--> QCoreApplication::postEvent()   放入目标线程事件队列
                                      |
                                      v
                              QObject::event()
                                      |
                          具体 handler 或 eventFilter
```

系统产生的事件通常 `spontaneous() == true`。使用 `sendEvent()` 或 `postEvent()` 手动投递的事件通常为非 spontaneous 事件。

### 1.2 它不解决什么问题

- 不负责启动事件循环，事件循环由 `QCoreApplication::exec()` 等 API 驱动。
- 不决定事件应该发给哪个对象，目标由 `sendEvent()`、`postEvent()` 或 Qt 内部派发逻辑决定。
- 不提供通用的类型安全 payload；自定义事件需要派生类保存数据。
- 不拥有接收者对象，事件和接收者是两套生命周期。
- 不保证 `ignore()` 一定会传播到父对象；是否传播取决于具体事件类型和接收者的处理规则。

## 2. 实际使用场景

### 2.1 重写 `QObject::event()` 处理自定义事件

当一个对象需要接收跨函数、跨线程或异步排队的通知时，自定义 `QEvent` 比共享全局变量更清晰：

```cpp
class ReloadEvent final : public QEvent
{
public:
    static QEvent::Type eventType()
    {
        static const auto type = static_cast<QEvent::Type>(
            QEvent::registerEventType());
        return type;
    }

    explicit ReloadEvent(QString fileName)
        : QEvent(eventType()), m_fileName(std::move(fileName))
    {
    }

    const QString &fileName() const { return m_fileName; }

private:
    QString m_fileName;
};
```

接收者可以在 `event()` 中识别并处理：

```cpp
bool ConfigObject::event(QEvent *event)
{
    if (event->type() == ReloadEvent::eventType()) {
        auto *reload = static_cast<ReloadEvent *>(event);
        reloadFrom(reload->fileName());
        event->accept();
        return true;
    }

    return QObject::event(event);
}
```

### 2.2 跨线程排队通知

```cpp
QCoreApplication::postEvent(
    receiver,
    new ReloadEvent(QStringLiteral("settings.json")));
```

`postEvent()` 把事件交给 `receiver` 所在线程的事件队列，并在事件处理完成后负责删除事件对象。调用方不能在 `postEvent()` 后继续释放或复用这个裸指针。

接收者必须仍然存在，并且目标线程需要运行事件循环。若接收者被销毁，Qt 会移除发给它的已发布事件。

### 2.3 同步注入测试事件

`sendEvent()` 适合测试或明确需要同步处理的场景：

```cpp
ReloadEvent event(QStringLiteral("test.json"));
QCoreApplication::sendEvent(receiver, &event);
```

`sendEvent()` 不接管栈对象的所有权，调用返回时事件已经同步处理完毕。它会在当前调用线程中直接执行接收者的事件处理逻辑，因此不能用它替代跨线程的 queued 通知。

### 2.4 事件过滤器

事件过滤器可以在目标对象的 `event()` 之前观察或拦截事件：

```cpp
bool Monitor::eventFilter(QObject *watched, QEvent *event)
{
    if (watched == target && event->type() == QEvent::KeyPress) {
        // 返回 true 表示过滤掉，不再交给 target 的后续处理
        return false;
    }

    return QObject::eventFilter(watched, event);
}
```

过滤器不应保存事件指针供稍后使用。事件通常只在当前调用栈内有效；需要保存信息时复制具体字段，而不是保存 `QEvent *`。

### 2.5 在标准事件处理器中决定接收或忽略

```cpp
void Editor::keyPressEvent(QKeyEvent *event)
{
    if (event->key() == Qt::Key_Escape) {
        cancelEditing();
        event->accept();
        return;
    }

    event->ignore();
}
```

`accept()` 表示当前接收者愿意处理该事件，`ignore()` 表示不接受。对于部分 QWidget 事件，忽略后可能继续交给父控件；这不是所有事件类别都共有的硬规则。

## 3. 构建与最小示例

`QEvent` 属于 Qt Core：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QEvent>

void inspect(QEvent *event)
{
    const QEvent::Type type = event->type();
    const bool accepted = event->isAccepted();
    const bool fromSystem = event->spontaneous();

    Q_UNUSED(type);
    Q_UNUSED(accepted);
    Q_UNUSED(fromSystem);
}
```

基类没有无参构造函数，必须在构造时指定 `QEvent::Type`。它也禁用了拷贝构造和拷贝赋值；需要多态复制时使用 Qt 6.0 起的 `clone()`。

## 4. 事件对象的生命周期和所有权

### 4.1 `sendEvent()` 不接管所有权

同步发送可以使用栈对象：

```cpp
QEvent event(QEvent::User);
QCoreApplication::sendEvent(receiver, &event);
```

调用结束后事件对象仍由调用者管理。接收者不能保存这个指针，除非调用者明确保证其生命周期覆盖保存期间，但通常不应这样设计。

### 4.2 `postEvent()` 接管事件对象

异步发布要求事件通常由堆上创建：

```cpp
QCoreApplication::postEvent(receiver, new QEvent(QEvent::User));
```

成功发布后，Qt 负责在事件处理后销毁它。不要：

- 在发布后手动 `delete`；
- 把同一个事件对象发布给多个目标；
- 在发布后修改事件对象；
- 让事件对象包含只在当前栈帧有效的引用。

如果接收者在事件处理前被销毁，Qt 会清理发给该接收者的已发布事件。

### 4.3 析构和已发布事件

`QEvent` 析构函数是虚函数。如果事件已经被 `postEvent()` 发布，析构时 Qt 会将它从待发布列表中移除。这不意味着调用者可以在发布后自行销毁事件；正常所有权仍由 Qt 管理。

### 4.4 不要跨事件回调保存裸指针

事件处理器返回后，事件可能马上被销毁。需要异步使用信息时：

```cpp
const QString path = static_cast<ReloadEvent *>(event)->fileName();
QTimer::singleShot(0, receiver, [path] {
    // 保存值，而不是保存 ReloadEvent *
});
```

如果需要把一个事件转交给另一个异步流程，优先复制它的业务字段，或使用 `clone()` 创建独立副本并明确谁负责删除。

## 5. accepted 状态的真实语义

### 5.1 默认值不能靠猜

Qt 文档说明，`QEvent` 构造后 accept flag 默认设为 `true`，但派生类构造函数可以把它清除。因此事件处理代码不能假设所有事件一开始都是 accepted。

```cpp
if (event->isAccepted()) {
    // 这里只能说明当前 flag 状态
}
```

这不等同于“事件已经被业务成功处理”。它只是 Qt 事件分发协议中的接收标志。

### 5.2 四个相关 API

```cpp
event->accept();              // setAccepted(true)
event->ignore();              // setAccepted(false)
event->setAccepted(false);
const bool ok = event->isAccepted();
```

`accept()` 和 `ignore()` 是最清晰的意图表达。需要统一设置状态时才直接调用 `setAccepted(bool)`。

### 5.3 忽略事件可能触发传播

对某些 QWidget 输入事件，接收者调用 `ignore()` 后，Qt 可能尝试将事件传给父控件或其他候选接收者。传播规则由具体事件和控件体系定义：

- 不要把 `ignore()` 当成“事件被删除”；
- 不要把 `accept()` 当成“事件一定不会继续经过其他内部逻辑”；
- 在自定义事件中，接收者通常用返回 `true` 表示已经处理。

### 5.4 Pointer event 的额外语义

Qt 文档特别指出，接受一个 `QPointerEvent` 会隐式接受它携带的所有 `QEventPoint`。因此处理多点触摸或指针事件时，还要阅读 `QPointerEvent`/`QEventPoint` 的接受状态规则，不能只看基类 flag。

## 6. `type()`、`spontaneous()` 和分类查询

### 6.1 `type()`

`type()` 返回构造时指定的 `QEvent::Type`。它用于在基类指针上分派到正确的派生类：

```cpp
switch (event->type()) {
case QEvent::Timer:
    // 通常交给 timerEvent() 或 QTimerEvent 处理
    break;
case QEvent::User:
    // 仅示例；生产代码通常使用 registerEventType()
    break;
default:
    break;
}
```

不要把所有事件都强制 `static_cast` 成某个派生类。只有确认 `type()` 对应的事件类型和类契约后，才可以进行安全的派生类转换。

### 6.2 `spontaneous()`

返回事件是否来自应用外部：

- 操作系统窗口系统产生的事件通常为 `true`；
- `sendEvent()`/`postEvent()` 手动发送的事件通常为 `false`；
- 它不是“是否异步”的标志；
- 它也不是“是否由用户操作触发”的完整判断。

例如，应用内部转发一个鼠标事件时，不能因为它包含鼠标数据就把它当成 spontaneous 系统输入。

### 6.3 `isInputEvent()`

Qt 6.0 起提供。若事件对象是 `QInputEvent` 或其派生类，返回 `true`。

它适合在通用过滤器中先做大类判断，但不能据此直接访问按键、鼠标或触摸字段：

```cpp
if (event->isInputEvent()) {
    // 仍需根据具体类型转换到 QKeyEvent/QPointerEvent 等
}
```

### 6.4 `isPointerEvent()`

Qt 6.0 起提供。若事件对象是 `QPointerEvent` 或其派生类，返回 `true`。它覆盖鼠标、触摸等指针事件体系，但不表示事件一定只有一个点。

### 6.5 `isSinglePointEvent()`

Qt 6.0 起提供。若事件对象是 `QSinglePointEvent` 的派生类，返回 `true`。这比 `isPointerEvent()` 更具体，适合需要单个 `QEventPoint` 语义的通用代码。

## 7. 自定义事件类型

### 7.1 使用 `registerEventType()`

不要随意写一个小于 `QEvent::User` 的整数作为应用事件类型。使用：

```cpp
const QEvent::Type type = static_cast<QEvent::Type>(
    QEvent::registerEventType());
```

`registerEventType()` 会在 `QEvent::User` 到 `QEvent::MaxUser` 范围内保留一个尚未使用的类型。它是线程安全的。

### 7.2 hint 的规则

```cpp
const int hint = 1200;
const int id = QEvent::registerEventType(hint);
```

- hint 在 `User..MaxUser` 范围内且尚未被占用时，Qt 尽量使用它；
- hint 不在合法范围内时会被忽略；
- hint 已被占用时，Qt 会分配另一个可用 ID；
- 所有可用 ID 都被占用，或程序正在关闭时返回 `-1`。

因此调用方必须处理失败情况，不要无条件把 `-1` 转成自定义 `Type` 后继续使用。

### 7.3 建议的自定义事件写法

```cpp
class RefreshEvent final : public QEvent
{
public:
    static QEvent::Type typeId()
    {
        static const int id = QEvent::registerEventType();
        return static_cast<QEvent::Type>(id);
    }

    RefreshEvent() : QEvent(typeId()) {}

    RefreshEvent(const RefreshEvent &other)
        : QEvent(typeId()), m_reason(other.m_reason)
    {
        setAccepted(other.isAccepted());
    }

    QEvent *clone() const override
    {
        return new RefreshEvent(*this);
    }

    QString reason() const { return m_reason; }

private:
    QString m_reason;
};
```

静态局部变量保证同一进程内这个事件类只注册一次。不要在每次构造事件时重新调用 `registerEventType()`，否则同一个类的事件实例会拥有不同类型。

### 7.4 `User` 和 `MaxUser`

- `QEvent::User` 是用户自定义事件范围的第一个 ID；
- `QEvent::MaxUser` 是最后一个 ID；
- 它们是范围边界，不是“通用自定义事件类型”；
- 多个模块直接使用 `QEvent::User` 会产生类型冲突。

## 8. `QEvent::Type` 如何分类

`Type` 有很多值，实际编码时重点是识别事件族，而不是记住整数：

| 类别 | 常见类型 | 通常对应的派生类或处理点 |
|---|---|---|
| 基础/无效 | `None` | 不是有效业务事件 |
| 定时器 | `Timer` | `QTimerEvent::timerId()`、`QObject::timerEvent()` |
| 键盘 | `KeyPress`、`KeyRelease`、`Shortcut`、`ShortcutOverride` | `QKeyEvent`、`QShortcutEvent` |
| 鼠标/指针 | `MouseButtonPress`、`MouseButtonRelease`、`MouseButtonDblClick`、`MouseMove` | `QMouseEvent`/指针事件体系 |
| 焦点 | `FocusIn`、`FocusOut`、`FocusAboutToChange` | `QFocusEvent` |
| 控件生命周期 | `Create`、`Destroy`、`Show`、`Hide`、`Close`、`Move`、`Resize` | `QShowEvent`、`QHideEvent`、`QCloseEvent`、`QMoveEvent`、`QResizeEvent` |
| 绘制/刷新 | `Paint`、`UpdateRequest`、`UpdateLater`、`Expose` | `QPaintEvent`、窗口/平台绘制机制 |
| 父子对象 | `ChildAdded`、`ChildPolished`、`ChildRemoved`、`ParentChange`、`ParentAboutToChange` | `QChildEvent`、`QObject`/`QWidget` |
| 拖放 | `DragEnter`、`DragMove`、`DragLeave`、`Drop` | `QDragEnterEvent`、`QDragMoveEvent`、`QDragLeaveEvent`、`QDropEvent` |
| 输入法 | `InputMethod`、`InputMethodQuery` | `QInputMethodEvent`、`QInputMethodQueryEvent` |
| 触摸/手势 | `TouchBegin`、`TouchUpdate`、`TouchEnd`、`TouchCancel`、`Gesture`、`GestureOverride`、`NativeGesture` | `QTouchEvent`、`QGestureEvent` |
| 平台/窗口 | `WindowActivate`、`WindowDeactivate`、`WindowStateChange`、`PlatformSurface`、`DevicePixelRatioChange` | `QWindow`/平台事件 |
| 应用状态 | `ApplicationStateChange`、`ApplicationFontChange`、`ApplicationPaletteChange`、`LanguageChange`、`LocaleChange` | `QCoreApplication`、`QApplication` |
| 延迟删除/元调用 | `DeferredDelete`、`MetaCall` | Qt 内部事件机制 |
| 图形场景 | `GraphicsSceneMouseMove`、`GraphicsSceneMousePress`、`GraphicsSceneHoverMove`、`GraphicsSceneDrop` 等 | `QGraphicsSceneEvent` 派生类 |
| Qt 6.7 窗口关系 | `ChildWindowAdded`、`ChildWindowRemoved`、`ParentWindowAboutToChange`、`ParentWindowChange` | Qt 6.7 起 |
| Qt 6.9 安全区 | `SafeAreaMarginsChange` | Qt 6.9 起 |
| 应用自定义 | `User..MaxUser` | `registerEventType()` |

### 8.1 容易误用的枚举项

- `ApplicationActivate`、`ApplicationActivated`、`ApplicationDeactivate` 等旧应用激活枚举已弃用语义，现代代码优先关注 `ApplicationStateChange`。
- `ThreadChange`、`DeferredDelete`、`MetaCall`、`PlatformSurface` 等事件通常由 Qt 内部或对象生命周期机制产生，不应随意手动伪造。
- `None` 表示无效事件类型，不适合投递给接收者。
- 枚举的整数值用于 ABI/内部识别，不应作为跨 Qt 版本的持久化协议编号。

## 9. 派生 QEvent 时的设计边界

### 9.1 禁止复制不是偶然限制

`QEvent` 禁用拷贝构造和拷贝赋值。事件可能处于已发布、已接受或由事件循环管理的状态，复制一个基类对象并不能自动复制其派生类 payload、所有权和队列状态。

需要复制时：

- 自己的派生事件提供明确的复制构造或字段复制；
- 或调用虚函数 `clone()`；
- 复制结果的所有权由调用者明确管理。

### 9.2 覆盖 `clone()`

Qt 6.0 起可以为自定义事件实现 `clone()`。由于 `QEvent` 基类禁用了拷贝构造，派生类必须自己复制 payload 和接收状态，不能直接依赖编译器生成的拷贝构造：

```cpp
RefreshEvent(const RefreshEvent &other)
    : QEvent(typeId()), m_reason(other.m_reason)
{
    setAccepted(other.isAccepted());
}

QEvent *clone() const override
{
    return new RefreshEvent(*this);
}
```

这不会解除 `QEvent` 基类的拷贝禁用。若事件含有资源句柄、QObject 指针或引用，应定义“克隆后共享还是独立”的语义。

调用方必须释放返回的堆对象：

```cpp
std::unique_ptr<QEvent> copy(event->clone());
```

对已经发布到事件队列的事件不要随意调用 `clone()` 再重新发布，除非派生类明确支持这种用法。

### 9.3 受保护的分类构造器

Qt 6.11 头文件提供了供 Qt 派生类使用的受保护构造路径：

```cpp
QEvent(Type, InputEventTag);
QEvent(Type, PointerEventTag);
QEvent(Type, SinglePointEventTag);
```

它们用于让 Qt 的输入事件层设置 `isInputEvent()`、`isPointerEvent()` 和 `isSinglePointEvent()` 标志。普通业务自定义事件通常只调用公开的 `QEvent(Type)` 构造函数，不应自行伪造这些 tag。

## 10. API 逐项说明

### 10.1 `QEvent::Type`

事件类型枚举。常见值包括 `Timer`、`MouseButtonPress`、`KeyPress`、`Paint`、`Resize`、`Close`、`DeferredDelete`、`TouchBegin`、`ApplicationStateChange`、`User` 和 `MaxUser`。

使用时优先比较命名枚举，不要比较裸整数。具体事件参数必须转到与类型匹配的派生类。

### 10.2 `accepted : bool`

事件的接收标志属性：

- 读取函数：`isAccepted()`；
- 写入函数：`setAccepted(bool)`；
- 便捷写入：`accept()`、`ignore()`；
- `QPointerEvent` 被接受时，其携带的点也会被隐式接受。

默认状态通常为 accepted，但派生类可以在构造函数中清除它。

### 10.3 `explicit QEvent(QEvent::Type type)`

构造指定类型的基类事件。没有默认构造函数。

`type` 应是已定义的 Qt 类型，或通过 `registerEventType()` 分配的自定义类型。不要把未注册的随意整数当成跨模块稳定事件类型。

### 10.4 `virtual ~QEvent() noexcept`

虚析构函数，保证通过 `QEvent *` 删除派生事件时正确调用派生类析构。若事件已经发布，析构时会从待发布列表中移除。

正常情况下，已发布事件由 Qt 删除，不由发布者手动删除。

### 10.5 `void accept()`

把 accept flag 设为 `true`，等同于 `setAccepted(true)`。它表示当前接收者愿意接受事件，不表示业务操作一定成功。

### 10.6 `void ignore()`

把 accept flag 清为 `false`，等同于 `setAccepted(false)`。某些 QWidget 事件会因此继续尝试传播给父控件或其他处理者。

### 10.7 `bool isAccepted() const`

返回当前 accept flag。它只反映事件对象当前状态，不报告事件是否被某个 handler 调用过。

### 10.8 `virtual void setAccepted(bool accepted)`

设置 accept flag。它是虚函数，派生事件可以在需要时扩展设置行为，但普通处理代码优先使用 `accept()` 和 `ignore()` 表达意图。

### 10.9 `QEvent *clone() const`

Qt 6.0 起的虚函数，创建并返回当前事件的独立副本。调用者拥有返回的堆对象，必须负责释放。

如果派生类没有正确覆盖，得到的副本可能只具有基类语义；需要完整复制 payload 时应检查具体派生类的 `clone()` 实现。

### 10.10 `bool isInputEvent() const noexcept`

Qt 6.0 起，判断对象是否属于 `QInputEvent` 体系。返回 `true` 时仍需进一步判断具体输入类别。

### 10.11 `bool isPointerEvent() const noexcept`

Qt 6.0 起，判断对象是否属于 `QPointerEvent` 体系。可用于通用指针事件过滤，但不能替代具体类型转换。

### 10.12 `bool isSinglePointEvent() const noexcept`

Qt 6.0 起，判断对象是否属于 `QSinglePointEvent` 体系。它表示事件使用单点语义，不等同于“所有输入事件”。

### 10.13 `static int registerEventType(int hint = -1) noexcept`

注册并返回一个自定义事件类型：

- 合法 hint 是 `QEvent::User` 到 `QEvent::MaxUser`；
- 合法且未占用的 hint 会尽量被采用；
- hint 不合法或已占用时，Qt 选择其他可用值；
- 无可用值或程序关闭时返回 `-1`；
- 函数线程安全。

应该在类型级别缓存注册结果，不要每次构造事件时重复注册。

### 10.14 `bool spontaneous() const`

判断事件是否来自应用外部系统。它不是同步/异步标志，也不是完整的用户输入判断。

### 10.15 `QEvent::Type type() const`

返回事件类型。它是从 `QEvent *` 判断具体派生类和分派逻辑的首要入口。

## 11. 常见误区和排查顺序

### 11.1 发布后又 delete

如果使用了 `postEvent(receiver, event)`, 成功发布后不要手动删除 `event`。它的生命周期由 Qt 事件队列管理。

### 11.2 把 `sendEvent()` 当成跨线程队列

`sendEvent()` 是同步调用，接收者的处理代码会立即在当前线程执行。跨线程通知应使用 `postEvent()`，并确保接收者线程有事件循环。

### 11.3 保存事件指针

事件处理返回后，事件可能已经被销毁。保存具体字段或调用 `clone()`，不要把 `QEvent *` 放入成员变量等待下次使用。

### 11.4 使用裸整数自定义类型

直接写 `static_cast<QEvent::Type>(1001)` 会和其他模块或库冲突。使用 `registerEventType()` 并缓存结果。

### 11.5 误解 `accepted`

`isAccepted() == true` 不等于“业务处理成功”；`ignore()` 也不一定表示事件会被丢弃。查清具体事件类和接收者的传播规则。

### 11.6 错误地转换派生类

先检查 `type()` 或分类 API，再转换到 `QKeyEvent`、`QMouseEvent`、`QTimerEvent` 等派生类。不要把任意事件都转换成同一个派生类。

### 11.7 忽略线程归属

`postEvent()` 将事件投递到接收者所属线程的队列。对象移动线程、对象销毁或目标线程停止事件循环时，事件的处理时机都会变化。

## API 速查表
### 12.1 类型、状态和构造

| API | 作用 | 关键边界 |
|---|---|---|
| `QEvent::Type` | 标识事件类别 | 用命名枚举比较，不依赖裸整数 |
| `QEvent::None` | 无效事件类型 | 不要作为正常业务事件投递 |
| `QEvent::User` | 自定义事件 ID 起点 | 不要直接占用，调用注册函数 |
| `QEvent::MaxUser` | 自定义事件 ID 终点 | 注册失败时可能无可用 ID |
| `accepted : bool` | 记录接收标志 | 默认通常为 true，派生类可清除 |
| `QEvent(type)` | 构造指定类型事件 | 无默认构造；类型需合法 |
| `~QEvent()` | 虚析构事件 | 已发布事件由 Qt 管理生命周期 |
| `QEvent` copy | 拷贝构造/赋值被禁用 | 需要复制使用 `clone()` 或自定义字段复制 |

### 12.2 接收状态

| API | 作用 | 关键边界 |
|---|---|---|
| `accept()` | 设置 accepted 为 true | 表示愿意接收，不等于业务成功 |
| `ignore()` | 设置 accepted 为 false | 某些 QWidget 事件可能继续传播 |
| `isAccepted()` | 读取接收标志 | 只反映当前状态 |
| `setAccepted(bool)` | 直接设置接收标志 | 虚函数；普通代码优先用 accept/ignore |

### 12.3 分类和来源

| API | 作用 | 关键边界 |
|---|---|---|
| `type()` | 读取事件类型 | 决定是否可转换到某个派生类 |
| `spontaneous()` | 判断是否来自应用外部 | 不是同步/异步标志 |
| `isInputEvent()` | 判断是否为 `QInputEvent` 派生类 | Qt 6.0；仍需确认具体输入类型 |
| `isPointerEvent()` | 判断是否为 `QPointerEvent` 派生类 | Qt 6.0；不表示单点 |
| `isSinglePointEvent()` | 判断是否为 `QSinglePointEvent` 派生类 | Qt 6.0；更具体的输入分类 |
| `clone()` | 创建独立事件副本 | Qt 6.0；返回堆对象由调用者释放 |

### 12.4 自定义事件

| API | 作用 | 关键边界 |
|---|---|---|
| `registerEventType()` | 注册自定义事件类型 | 线程安全；失败返回 `-1` |
| `registerEventType(hint)` | 尝试申请指定 ID | hint 必须在 `User..MaxUser`，且不保证一定采用 |
| `QEvent::User..MaxUser` | 自定义类型可用范围 | 应通过注册函数分配 |
| `QCoreApplication::sendEvent()` | 同步发送事件 | 不接管所有权；当前线程立即执行 |
| `QCoreApplication::postEvent()` | 异步发布事件 | 通常接管堆对象；发往接收者所属线程 |

### 12.5 常见 `Type` 家族

| 家族 | 代表项 | 典型用途 |
|---|---|---|
| 键盘/快捷键 | `KeyPress`、`KeyRelease`、`ShortcutOverride`、`Shortcut` | 键盘输入和快捷键抢占 |
| 鼠标/指针 | `MouseButtonPress`、`MouseMove`、`MouseButtonRelease` | 鼠标和指针交互 |
| 焦点 | `FocusIn`、`FocusOut`、`FocusAboutToChange` | 键盘焦点切换 |
| 窗口/控件 | `Show`、`Hide`、`Move`、`Resize`、`Close` | 控件生命周期和几何变化 |
| 绘制/刷新 | `Paint`、`UpdateRequest`、`UpdateLater`、`Expose` | 重绘和平台表面更新 |
| 定时器 | `Timer` | `QTimerEvent`/`timerEvent()` |
| 拖放 | `DragEnter`、`DragMove`、`DragLeave`、`Drop` | 拖放协议 |
| 触摸/手势 | `TouchBegin`、`TouchUpdate`、`TouchEnd`、`TouchCancel`、`Gesture` | 多点触摸和手势 |
| 对象关系 | `ChildAdded`、`ChildRemoved`、`ParentChange`、`ThreadChange` | QObject/QWidget 生命周期 |
| 应用状态 | `ApplicationStateChange`、`LanguageChange`、`LocaleChange` | 应用环境变化 |
| 延迟/内部 | `DeferredDelete`、`MetaCall` | Qt 内部调度 |
| 窗口关系 | `ChildWindowAdded`、`ParentWindowChange` | Qt 6.7 起的窗口关系变化 |
| 安全区域 | `SafeAreaMarginsChange` | Qt 6.9 起 |

## 13. 选型结论

把 `QEvent` 理解成“由事件循环短暂持有、由接收者处理、带类型和接收状态的多态事件对象”最准确：

- 普通业务通知需要排队时，派生 `QEvent` 并用 `registerEventType()`；
- 同步测试用 `sendEvent()`，异步跨线程通知用 `postEvent()`；
- 发布后遵守 Qt 的事件所有权，不要手动释放；
- `type()` 用来识别事件族，`isInputEvent()` 等 API 用来做粗粒度分类；
- `accept()`/`ignore()` 是事件传播协议，不是业务成功/失败返回值；
- 事件处理结束后不要保存裸指针，需要延迟使用时复制字段或明确调用 `clone()`。
