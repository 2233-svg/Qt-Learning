# Qt QEvent 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QEvent>`  
> 所属模块：`Qt6::Core`  
> 直接基类：无  
> 定位：所有 Qt 事件对象的基类，保存事件类型、接受状态和事件参数的多态接口

Qt 的事件系统把“某件事需要某个对象处理”表示为一个 `QEvent` 或其派生对象。事件可以来自操作系统，也可以由 Qt 或业务代码同步发送、异步投递。`QEvent` 本身只保存通用状态，鼠标、键盘、定时器、关闭、拖放等具体数据位于派生类。

## 1. 最小可用代码

### 1.1 CMake 配置

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

### 1.2 在 QObject 中处理事件

```cpp
#include <QCoreApplication>
#include <QEvent>
#include <QObject>

class Receiver final : public QObject
{
protected:
    bool event(QEvent *event) override
    {
        if (event->type() == QEvent::User) {
            qInfo() << "custom event received";
            return true;
        }
        return QObject::event(event);
    }
};

Receiver receiver;
QCoreApplication::postEvent(&receiver,
                            new QEvent(QEvent::User));
```

`postEvent()` 接管堆事件并稍后投递。未处理的事件必须交给基类 `event()`，否则 QObject 内建事件行为会被截断。

## 2. 事件传递链

```text
操作系统/Qt/业务代码
        │
        ├─ sendEvent：当前调用栈同步发送
        └─ postEvent：加入接收者线程的事件队列
                      │
                      ▼
          QCoreApplication::notify()
                      │
            应用级/对象级过滤器
                      │
                      ▼
               QObject::event()
                      │
       timerEvent/customEvent/Widget 专用处理器
```

事件最终在哪个线程处理，由接收 QObject 的线程亲和性和发送方式决定。`postEvent()` 是线程安全投递入口；事件处理函数本身仍在接收对象线程运行。

## 3. 构造、类型与析构

```cpp
QEvent event(QEvent::Type::User);
QEvent::Type type = event.type();
```

构造函数记录类型。`QEvent` 有虚析构函数，因此可以通过基类指针删除派生事件：

```cpp
QEvent *event = new MyEvent(...);
delete event;
```

由 `postEvent()` 投递后，所有权已经交给 Qt，调用者不得再删除或访问。

## 4. `QEvent::Type` 分类

`Type` 是一个很大的枚举。学习时按语义分组比背数值更重要。

### 4.1 对象与应用生命周期

常见类型：

```text
ChildAdded, ChildRemoved, ChildPolished
DeferredDelete, Destroy, DynamicPropertyChange
ThreadChange, ParentChange, ParentAboutToChange
ApplicationActivate, ApplicationDeactivate, ApplicationStateChange
Quit, Close, Show, Hide, ShowToParent, HideToParent
```

`DeferredDelete` 承载 `deleteLater()`；不要随意移除。`DynamicPropertyChange` 在动态属性改变时发送。`ThreadChange` 在对象线程亲和性即将变化时出现。

### 4.2 窗口和控件状态

```text
Move, Resize, Paint, UpdateRequest, Expose
WindowActivate, WindowDeactivate, WindowStateChange
FocusIn, FocusOut, FocusAboutToChange
EnabledChange, FontChange, PaletteChange, StyleChange
LayoutRequest, Polish, PolishRequest
ContentsRectChange, ReadOnlyChange, WindowTitleChange
```

这类事件多由 `QWidget`、`QWindow` 或平台集成处理。不要手工伪造 Paint/Resize 等事件来代替正确 API；例如更新 Widget 应调用 `update()`，由 Qt 安排绘制。

### 4.3 键盘、快捷键和输入法

```text
KeyPress, KeyRelease
Shortcut, ShortcutOverride
InputMethod, InputMethodQuery
KeyboardLayoutChange
```

`ShortcutOverride` 允许焦点对象先声明自己要处理按键；接受后快捷键不会抢先触发，按键继续作为普通事件交给对象。

### 4.4 鼠标、滚轮、触摸和指针

```text
MouseButtonPress, MouseButtonRelease, MouseButtonDblClick, MouseMove
HoverEnter, HoverMove, HoverLeave
Enter, Leave
Wheel
TouchBegin, TouchUpdate, TouchEnd, TouchCancel
TabletPress, TabletMove, TabletRelease
Pointer, NonClientAreaMouseMove/Press/Release/DoubleClick
```

Qt 6 统一了许多指针设备概念。具体数据应通过 `QPointerEvent`、`QSinglePointEvent`、`QMouseEvent`、`QTouchEvent` 等派生类型访问，不要按 Type 后做错误的 static_cast。

### 4.5 拖放、手势与上下文菜单

```text
DragEnter, DragMove, DragLeave, Drop
Gesture, GestureOverride, NativeGesture
ContextMenu
ToolTip, WhatsThis, QueryWhatsThis
```

拖放事件通常需要接受合适的 proposed action，单纯返回 true 不等同于完成拖放协议。

### 4.6 定时器、进程与平台事件

```text
Timer, SockAct, SockClose
PlatformSurface, PlatformPanel
FileOpen
WinEventAct, MacSizeChange
ThemeChange, DevicePixelRatioChange, SafeAreaMarginsChange
```

部分类型只在特定平台或特定对象上出现。跨平台业务不要依赖某个平台事件必然存在。

### 4.7 自定义事件区间

```cpp
QEvent::User;    // 用户事件起点，通常为 1000
QEvent::MaxUser; // 用户事件上限，通常为 65535
```

不要硬编码枚举整数；使用命名常量或 `registerEventType()`。

## 5. 注册自定义事件类型

### 5.1 标准写法

```cpp
QEvent::Type resultEventType()
{
    static const int value = QEvent::registerEventType();
    return static_cast<QEvent::Type>(value);
}
```

`registerEventType(hint = -1)` 在线程安全的全局注册表中分配 `User..MaxUser` 范围内未使用的值。若传入可用 hint，会优先使用；冲突时分配别的值。没有可用值时返回 `-1`。

使用函数局部静态量避免多个翻译单元重复注册。不要在公共头文件中定义会产生多个不同 ID 的非 inline 全局初始化代码。

## 6. 自定义事件类

```cpp
class ResultEvent final : public QEvent
{
public:
    static Type staticType()
    {
        static const int id = registerEventType();
        return static_cast<Type>(id);
    }

    explicit ResultEvent(QString result)
        : QEvent(staticType()), m_result(std::move(result))
    {
    }

    const QString &result() const { return m_result; }

    QEvent *clone() const override
    {
        return new ResultEvent(*this);
    }

private:
    QString m_result;
};
```

事件数据应自包含。异步投递时不要保存指向调用方栈变量的引用。可复制 Qt 值类型、共享不可变数据或受控智能指针更安全。

## 7. `clone()`

```cpp
QEvent *copy = event->clone();
// 使用完由调用者 delete
delete copy;
```

`clone()` 返回当前事件的堆副本，调用者取得所有权。自定义派生类若增加数据，应重载 clone，否则通过基类克隆可能丢失派生状态或只得到基础事件语义。

克隆事件不表示重新产生一次操作系统输入，它只是复制事件对象的数据。

## 8. Accepted 状态

```cpp
event->accept();
event->ignore();

event->setAccepted(true);
const bool accepted = event->isAccepted();
```

`accept()` 等价于 `setAccepted(true)`，`ignore()` 等价于 false。该标志的具体含义由事件类型和接收框架决定：

- CloseEvent 接受通常允许关闭，忽略则阻止。
- Drag/Drop 接受表示支持相应动作。
- Pointer event 接受可能影响继续传播或抓取。
- 某些 Widget 输入事件忽略后会向父 Widget 传播。

事件初始 accepted 状态不要一概假设；不同派生类构造函数可能设置不同默认值。

### 8.1 accepted 与 `event()` 返回值不是一回事

```cpp
bool Widget::event(QEvent *event)
{
    event->accept(); // 改变事件自身状态
    return true;     // 告诉分发器：此对象已处理
}
```

二者经常相关但语义不同。重载具体事件处理器时按该事件协议设置 accept/ignore；重载总入口 `event()` 时按是否完成处理返回 bool。

### 8.2 指针事件的特殊行为

对 `QPointerEvent` 调用 accept 会隐式接受其携带的所有 `QEventPoint`。需要逐触点控制时，操作具体 point 的 accepted 状态，不要先接受整个事件。

## 9. 输入事件类别判断

Qt 6 提供无需逐个枚举 type 的快速判断：

```cpp
if (event->isInputEvent()) {
    auto *input = static_cast<QInputEvent *>(event);
}

if (event->isPointerEvent()) {
    auto *pointer = static_cast<QPointerEvent *>(event);
}

if (event->isSinglePointEvent()) {
    auto *single = static_cast<QSinglePointEvent *>(event);
}
```

- `isInputEvent()`：事件属于 `QInputEvent` 系列。
- `isPointerEvent()`：属于 `QPointerEvent` 系列。
- `isSinglePointEvent()`：属于单点指针事件系列。

这些判断比维护一长串鼠标/触摸枚举更能适应新设备类型。

## 10. `spontaneous()`

```cpp
if (event->spontaneous())
    qDebug() << "originated from the native event system";
```

由底层窗口系统产生并交给应用的事件通常是 spontaneous；通过 `sendEvent()`/`postEvent()` 手工发送的事件通常不是。

它只表示来源类别，不是安全凭证。不能据此认定事件来自可信用户，也不能用它阻止自动化测试或安全攻击。

## 11. 同步 `sendEvent()`

```cpp
ResultEvent event("ready");
const bool handled = QCoreApplication::sendEvent(receiver, &event);
qDebug() << handled << event.isAccepted();
```

特点：

- 当前调用栈立即分发。
- 通常应在 receiver 所属线程调用。
- 调用者保留事件所有权，栈对象可用。
- 接收函数可在返回前修改 accepted 和事件数据。
- 会产生重入，receiver 可能在处理期间间接删除对象。

不要在持有不允许重入的互斥锁时同步发送复杂事件。

## 12. 异步 `postEvent()`

```cpp
QCoreApplication::postEvent(
    receiver,
    new ResultEvent("ready"),
    Qt::NormalEventPriority);
```

特点：

- 线程安全地加入 receiver 所在线程队列。
- Qt 接管事件指针并最终删除。
- 调用后不能再读取 event 或 accepted 状态。
- receiver 必须在处理时仍存活；QObject 析构会移除其待处理事件。
- 需要 receiver 所在线程有活跃事件循环才能及时处理。

优先级较大的 posted event 先处理；相同优先级保持投递顺序。不要把所有业务事件设为高优先级，否则定时器、UI 和清理事件可能饥饿。

## 13. 事件过滤

事件过滤器看到的是同一个事件对象：

```cpp
bool Filter::eventFilter(QObject *watched, QEvent *event)
{
    if (event->type() == ResultEvent::staticType()) {
        auto *result = static_cast<ResultEvent *>(event);
        inspect(result->result());
        return false; // 继续交给 watched
    }
    return QObject::eventFilter(watched, event);
}
```

返回 true 会停止后续过滤器和目标对象处理。过滤器若删除 `watched`，必须返回 true。

## 14. 事件压缩与频率

Qt 可能对某些框架事件进行合并，例如连续更新/绘制请求；平台也可能压缩鼠标移动。不要假设每次状态变化都对应一个独立事件，也不要通过统计 Paint/Move 事件数量推断业务次数。

自定义事件若高频产生，应在业务层做合并：对象只保留最新状态，并用一个“待处理”标志避免队列堆积。

```cpp
if (!m_updatePending) {
    m_updatePending = true;
    QCoreApplication::postEvent(this, new UpdateEvent);
}
```

处理时清除标志并读取最新状态。

## 15. 事件对象中的指针生命周期

某些事件保存外部对象指针或临时视图。事件只保证在分发期间的数据有效性，不应把 `QEvent *` 保存到异步回调中：

```cpp
bool Receiver::event(QEvent *event)
{
    // 错误：lambda 执行时 event 已销毁
    QTimer::singleShot(0, [event] { use(event); });
    return true;
}
```

需要异步处理时立即复制必要值，而不是保存事件地址。

## 16. 测试事件

单元测试可用 `sendEvent()` 验证同步处理：

```cpp
ResultEvent event("ok");
QVERIFY(QCoreApplication::sendEvent(&receiver, &event));
QCOMPARE(receiver.lastResult(), QString("ok"));
```

测试队列行为则使用 `postEvent()` 并让事件循环推进：

```cpp
QCoreApplication::postEvent(&receiver, new ResultEvent("ok"));
QTRY_COMPARE(receiver.lastResult(), QString("ok"));
```

键鼠 GUI 测试优先使用 QTest 的输入模拟 API，它会构造正确的专用事件和坐标，而不是手写不完整的 `QMouseEvent`。

## 17. 常见误区

### 用 `QEvent::User + n` 在多个模块各自硬编码

不同插件可能使用同一个值。统一注册或调用 `registerEventType()`。

### 把栈事件传给 `postEvent()`

Qt 会尝试删除它，导致未定义行为。posted event 必须 `new`，投递后归 Qt。

### 处理事件后仍调用基类

若已经完全消费自定义事件，再调用基类可能导致重复或意外处理。处理完成直接返回 true；未处理才调用基类。

### 只调用 accept 却从 `event()` 返回 false

accepted 和处理返回值属于不同层面。按具体事件协议和总入口约定分别设置。

### 保存事件指针到以后

事件通常在分发结束后销毁。只复制需要的数据。

## API 速查表
### 18.1 构造、类型和生命周期

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QEvent(QEvent::Type type)` | 创建一个带通用类型信息的基础事件对象。 | 鼠标、键盘、定时器等专用数据应使用对应派生事件；基础事件本身不携带这些参数。 |
| 析构 | `~QEvent()` | 销毁事件对象，允许通过基类指针安全析构派生事件。 | `postEvent()` 投递后的事件由 Qt 删除；调用方不能重复删除。 |
| 类型 | `type()` | 返回事件的 `QEvent::Type`。 | 用枚举比较，不要硬编码整数；确认类型后再转换到匹配的派生类。 |
| 来源 | `spontaneous()` | 判断事件是否由底层系统自发产生。 | 不是可信用户输入证明，也不能作为安全边界或反自动化机制。 |
| 克隆 | `clone()` | 创建当前事件的堆副本。 | 返回副本的所有权给调用者；自定义派生事件增加数据时应重写。 |

### 18.2 类型注册和事件分类

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 自定义类型 | `registerEventType(int hint = -1)` | 在线程安全的全局表中分配 `User..MaxUser` 范围内的未使用事件类型。 | hint 冲突时会分配其他值；没有可用值返回 `-1`，应缓存注册结果并处理失败。 |
| 类型范围 | `QEvent::User` / `QEvent::MaxUser` | 表示应用自定义事件类型的起止范围。 | 不要在多个模块里直接使用 `User + n` 硬编码，插件之间可能冲突。 |
| 输入分类 | `isInputEvent()` | 判断事件是否属于 `QInputEvent` 家族。 | 返回 true 后才能按匹配层级转换；具体数据仍要使用正确派生类型。 |
| 指针分类 | `isPointerEvent()` | 判断事件是否属于 `QPointerEvent` 家族。 | 适合统一处理鼠标、触摸等指针事件；不要把它直接当单点事件使用。 |
| 单点分类 | `isSinglePointEvent()` | 判断事件是否属于 `QSinglePointEvent` 家族。 | 只有返回 true 后才适合访问单点坐标等专用接口。 |
| 事件枚举 | `QEvent::Type` | 为 Qt 内建事件和用户事件提供语义分类。 | 跨平台代码只依赖稳定语义；部分平台事件只在特定平台或对象上出现。 |

### 18.3 接受状态

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 接受 | `accept()` | 把事件的 accepted 状态设为 true。 | 这是事件协议状态，不等于 `event()` 返回 true；效果由具体事件协议决定。 |
| 忽略 | `ignore()` | 把事件的 accepted 状态设为 false。 | 某些 Widget 输入事件会因此继续向父对象传播；不要假设所有事件都相同。 |
| 显式设置 | `setAccepted(bool accepted)` | 直接设置 accepted 标志。 | `QPointerEvent` 的 accepted 可能影响其携带的 points；需要逐点控制时使用 point API。 |
| 查询 | `isAccepted()` | 查询事件当前 accepted 状态。 | 初始值可能由具体派生事件构造函数决定；不能和分发返回值混为一谈。 |
| 分发结果 | `QObject::event(QEvent *)` / `QCoreApplication::sendEvent()` 返回值 | 表示目标对象是否报告自己处理了事件。 | 返回值与 accepted 是两个层次；总入口按是否处理返回，具体事件按协议设置状态。 |

### 18.4 同步发送、异步投递和扩展

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 同步分发 | `QCoreApplication::sendEvent(QObject *receiver, QEvent *event)` | 在当前调用栈中立即把事件交给 receiver。 | 调用者拥有事件对象；可能发生重入，通常应在 receiver 所属线程调用。 |
| 异步投递 | `QCoreApplication::postEvent(QObject *receiver, QEvent *event, int priority = Qt::NormalEventPriority)` | 把事件排入 receiver 所在线程的事件队列。 | event 必须是堆对象；投递后所有权归 Qt，不能继续访问或删除。 |
| 事件过滤 | `QObject::installEventFilter()` / `eventFilter()` | 在目标对象收到事件前观察或拦截同一个事件对象。 | 过滤器返回 true 会停止后续处理；删除 watched 后必须返回 true。 |
| 事件入口 | `QObject::event(QEvent *event)` | 目标对象处理事件的总入口。 | 未处理的事件交给基类；完全消费自定义事件后直接返回 true。 |
| 事件数据 | 具体派生事件类 | 携带鼠标、键盘、定时器、拖放等专用参数。 | 先判断类型或分类，再使用匹配的派生类接口，不要错误 `static_cast`。 |
| 异步数据 | 自定义事件中的值类型数据 | 让 posted event 在投递后仍自包含。 | 不要保存调用方栈变量引用或把 `QEvent *` 保存到稍后执行的 lambda 中；异步场景复制必要数据。 |

---

### 一句话总结

`QEvent` 是 Qt 事件传递的多态载体：用 `Type` 区分语义，用 accepted 表达具体协议状态，用 `sendEvent()` 同步调用、`postEvent()` 安全排队，自定义事件则通过全局注册类型和自包含数据避免冲突与悬空引用。
