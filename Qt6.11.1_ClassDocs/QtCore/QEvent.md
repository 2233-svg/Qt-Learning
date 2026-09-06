# QEvent

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QEvent` 是 Qt 的值类型，围绕“事件”保存可复制的数据，并提供查询、转换或修改 API。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QEvent` 是事件或输入数据对象，描述 Qt 在事件分发过程中传递的状态。

**内部模型：** 事件对象通常由 Qt 创建并只在处理函数调用期间有效；重点是读取类型、接受/忽略事件，并决定是否交给基类继续处理。

**适用场景：** 重实现 QWidget/QWindow/对象的事件处理函数，或在事件过滤器中区分输入行为时使用。

**典型调用链：** Qt 创建事件 -> event/eventFilter 收到 -> 检查字段和 modifiers -> accept/ignore -> 必要时调用基类实现。

**先记住的坑：** 不要保存短生命周期事件指针；不要无条件吞掉事件；坐标系、设备像素比和键盘自动重复都要按事件类型处理。

## 2. 依赖与对象关系

- 头文件：`#include <QEvent>`
- 继承自：未在类页中列出
- 直接派生类：QActionEvent、QChildEvent、QChildWindowEvent、QCloseEvent、QDragLeaveEvent、QDropEvent、QDynamicPropertyChangeEvent、QExposeEvent、QFileOpenEvent、QFocusEvent、QGestureEvent、QGraphicsSceneEvent、QHelpEvent、QHideEvent、QIconDragEvent、QInputEvent、QInputMethodEvent、QInputMethodQueryEvent、QMoveEvent、QPaintEvent、QPlatformSurfaceEvent、QResizeEvent、QScrollEvent、QScrollPrepareEvent、QShortcutEvent、QShowEvent、QStateMachine::SignalEvent、QStateMachine::WrappedEvent、QStatusTipEvent、QTimerEvent、QWhatsThisClickedEvent,、QWindowStateChangeEvent

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

事件对象通常由 Qt 创建并只在处理函数调用期间有效；重点是读取类型、接受/忽略事件，并决定是否交给基类继续处理。

### 状态、生命周期和线程

**生命周期：** 值对象由作用域、容器或调用者管理，不使用 parent 和 deleteLater。跨线程传递副本通常比传递 QObject 安全，但共享数据在写入时仍可能发生复制，性能和内存峰值要结合数据规模判断。

**状态与结果：** 重点区分空值、无效值、默认值和已初始化值。例如空字符串、空 URL、null 图像和无效索引不一定表示同一件事；转换函数的失败结果要通过对应的状态查询确认。

**线程与事件循环：** 值类型本身通常可以复制后跨线程传递；不要把 data()/bits()/constData() 得到的指针当成跨线程长期有效的所有权。大对象频繁写入会触发 detach，应避免不必要的复制和格式转换。

## 3. 直接使用

重实现 QWidget/QWindow/对象的事件处理函数，或在事件过滤器中区分输入行为时使用。 使用时通常按这个过程组织：Qt 创建事件 -> event/eventFilter 收到 -> 检查字段和 modifiers -> accept/ignore -> 必要时调用基类实现。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum Type { None, ActionAdded, ActionChanged, ActionRemoved, ActivationChange, …, MaxUser }`

### 属性

- `accepted : bool`

### 公有函数

- `QEvent(QEvent::Type type)`
- `virtual ~QEvent()`
- `void accept()`
- `(since 6.0) virtual QEvent * clone() const`
- `void ignore()`
- `bool isAccepted() const`
- `(since 6.0) bool isInputEvent() const`
- `(since 6.0) bool isPointerEvent() const`
- `(since 6.0) bool isSinglePointEvent() const`
- `virtual void setAccepted(bool accepted)`
- `bool spontaneous() const`
- `QEvent::Type type() const`

### 静态公有成员

- `int registerEventType(int hint = -1)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QEvent::Type`

**作用与语义：**

该枚举类型定义了 Qt 中的有效事件类型。事件类型及每种类型的专用类如下：
- `QEvent::None`：`0`;不是事件。
- `QEvent::ActionAdded`：`114`;新增了一个动作（`QActionEvent`）。
- `QEvent::ActionChanged`：`113`;动作被更改（`QActionEvent`）。
- `QEvent::ActionRemoved`：`115`;一个动作已被移除（`QActionEvent`）。
- `QEvent::ActivationChange`：`99`;小部件的顶层窗口激活状态发生变化。
- `QEvent::ApplicationActivate`：`121`;该枚举已被弃用。请使用ApplicationStateChange。
- `QEvent::ApplicationActivated`：`ApplicationActivate`;该枚举已被弃用。请使用 ApplicationStateChange。
- `QEvent::ApplicationDeactivate`：`122`;该枚举已被弃用。请使用ApplicationStateChange。
- `QEvent::ApplicationFontChange`：`36`;默认应用字体发生了变化。
- `QEvent::ApplicationLayoutDirectionChange`：`37`;默认应用布局方向已更改。
- `QEvent::ApplicationPaletteChange`：`38`;默认应用调色板已更改。
- `QEvent::ApplicationStateChange`：`214`;申请状态发生变化。
- `QEvent::ApplicationWindowIconChange`：`35`;应用程序图标发生了变化。
- `QEvent::ChildAdded`：`68`;一个对象得到一个子节点（`QChildEvent`）。
- `QEvent::ChildPolished`：`69`;一个小部件子被抛光（`QChildEvent`）。
- `QEvent::ChildRemoved`：`71`;物体失去一个子（`QChildEvent`）。
- `QEvent::ChildWindowAdded (since Qt 6.7)`：`223`;在窗口中添加了一个子窗口。
- `QEvent::ChildWindowRemoved (since Qt 6.7)`：`224`;窗户上的子窗被移除。
- `QEvent::Clipboard`：`40`;剪贴板内容已更改。
- `QEvent::Close`：`19`;小工具关闭（`QCloseEvent`）。
- `QEvent::CloseSoftwareInputPanel`：`200`;一个小部件想要关闭软件输入面板（SIP）。
- `QEvent::ContentsRectChange`：`178`;小部件内容的边界rect发生变化。
- `QEvent::ContextMenu`：`82`;上下文弹出菜单（`QContextMenuEvent`）。
- `QEvent::CursorChange`：`183`;控件的光标发生变化。
- `QEvent::DeferredDelete`：`52`;该对象在清理完成后将被删除（QDeferredDeleteEvent）
- `QEvent::DevicePixelRatioChange (since Qt 6.6)`：`222`;该小部件或窗口底层存储的 devicePixelRatio 发生了变化。
- `QEvent::DragEnter`：`60`;光标在拖拽操作（`QDragEnterEvent`）中进入小部件。
- `QEvent::DragLeave`：`62`;光标在拖拽操作（`QDragLeaveEvent`）中离开小部件。
- `QEvent::DragMove`：`61`;正在进行拖拽操作（`QDragMoveEvent`）。
- `QEvent::Drop`：`63`;完成拖放操作（`QDropEvent`）。
- `QEvent::DynamicPropertyChange`：`170`;对象中添加、更改或移除动态属性。
- `QEvent::EnabledChange`：`98`;控件的启用状态发生了变化。
- `QEvent::Enter`：`10`;鼠标进入控件边界（`QEnterEvent`）。
- `QEvent::EnterEditFocus`：`150`;编辑小部件获得编辑焦点。`QT_KEYPAD_NAVIGATION`必须被定义。
- `QEvent::EnterWhatsThisMode`：`124`;当应用程序进入“这是什么？”模式时，发送到顶层控件。
- `QEvent::Expose`：`206`;当窗口的屏幕内容失效并需要从备份存储中清除时，发送到窗口。
- `QEvent::FileOpen`：`116`;文件开放请求（`QFileOpenEvent`）。
- `QEvent::FocusIn`：`8`;控件或窗口获得键盘焦点（`QFocusEvent`）。
- `QEvent::FocusOut`：`9`;控件或窗口失去键盘焦点（`QFocusEvent`）。
- `QEvent::FocusAboutToChange`：`23`;控件或窗口焦点即将更改（`QFocusEvent`）
- `QEvent::FontChange`：`97`;小部件的字体发生了变化。
- `QEvent::Gesture`：`198`;触发了一个手势（`QGestureEvent`）。
- `QEvent::GestureOverride`：`202`;触发了手势覆盖（`QGestureEvent`）。
- `QEvent::GrabKeyboard`：`188`;物品获得键盘抓取（仅限`QGraphicsItem`）。
- `QEvent::GrabMouse`：`186`;物品获得鼠标抓取（仅限`QGraphicsItem`）。
- `QEvent::GraphicsSceneContextMenu`：`159`;图形场景（`QGraphicsSceneContextMenuEvent`）上的上下文弹窗菜单。
- `QEvent::GraphicsSceneDragEnter`：`164`;光标在拖拽操作（`QGraphicsSceneDragDropEvent`）中进入图形场景。
- `QEvent::GraphicsSceneDragLeave`：`166`;在拖拽操作（`QGraphicsSceneDragDropEvent`）期间，光标会离开图形场景。
- `QEvent::GraphicsSceneDragMove`：`165`;场景（`QGraphicsSceneDragDropEvent`）正在进行拖拽操作。
- `QEvent::GraphicsSceneDrop`：`167`;在场景（`QGraphicsSceneDragDropEvent`）上完成拖放操作。
- `QEvent::GraphicsSceneHelp`：`163`;用户请求图形场景（`QHelpEvent`）的帮助。
- `QEvent::GraphicsSceneHoverEnter`：`160`;鼠标光标进入图形场景中的悬浮物品（`QGraphicsSceneHoverEvent`）。
- `QEvent::GraphicsSceneHoverLeave`：`162`;鼠标光标在图形场景中停留一个悬浮物品（`QGraphicsSceneHoverEvent`）。
- `QEvent::GraphicsSceneHoverMove`：`161`;鼠标光标在图形场景（`QGraphicsSceneHoverEvent`）中的悬浮物体内移动。
- `QEvent::GraphicsSceneMouseDoubleClick`：`158`;在图形场景（`QGraphicsSceneMouseEvent`）中再次按鼠标（双击）。
- `QEvent::GraphicsSceneMouseMove`：`155`;在图形场景中移动鼠标（`QGraphicsSceneMouseEvent`）。
- `QEvent::GraphicsSceneMousePress`：`156`;图形场景中的鼠标按压（`QGraphicsSceneMouseEvent`）。
- `QEvent::GraphicsSceneMouseRelease`：`157`;图形场景中的鼠标释放（`QGraphicsSceneMouseEvent`）。
- `QEvent::GraphicsSceneMove`：`182`;小部件被移动（`QGraphicsSceneMoveEvent`）。
- `QEvent::GraphicsSceneResize`：`181`;小部件大小调整（`QGraphicsSceneResizeEvent`）。
- `QEvent::GraphicsSceneWheel`：`168`;在图形场景中滚动的鼠标轮（`QGraphicsSceneWheelEvent`）。
- `QEvent::GraphicsSceneLeave`：`220`;光标离开一个图形场景（`QGraphicsSceneWheelEvent`）。
- `QEvent::Hide`：`18`;小部件被隐藏（`QHideEvent`）。
- `QEvent::HideToParent`：`27`;一个子控件被隐藏了。
- `QEvent::HoverEnter`：`127`;鼠标光标进入一个悬浮小部件（`QHoverEvent`）。
- `QEvent::HoverLeave`：`128`;鼠标光标留下一个悬浮小部件（`QHoverEvent`）。
- `QEvent::HoverMove`：`129`;鼠标光标在悬浮小部件（`QHoverEvent`）内移动。
- `QEvent::IconDrag`：`96`;窗户的主图标被拖走了（`QIconDragEvent`）。
- `QEvent::IconTextChange`：`101`;小部件的图标文本已更改。（已弃用）
- `QEvent::InputMethod`：`83`;正在使用输入法（`QInputMethodEvent`）。
- `QEvent::InputMethodQuery`：`207`;输入法查询事件（`QInputMethodQueryEvent`）
- `QEvent::KeyboardLayoutChange`：`169`;键盘布局发生了变化。
- `QEvent::KeyPress`：`6`;按键（`QKeyEvent`）。
- `QEvent::KeyRelease`：`7`;密钥释放（`QKeyEvent`）。
- `QEvent::LanguageChange`：`89`;应用翻译发生了变化。
- `QEvent::LayoutDirectionChange`：`90`;布局方向发生了变化。
- `QEvent::LayoutRequest`：`76`;小部件布局需要重新设计。
- `QEvent::Leave`：`11`;鼠标离开控件的边界。
- `QEvent::LeaveEditFocus`：`151`;编辑小部件在编辑时失去焦点。QT_KEYPAD_NAVIGATION必须被定义。
- `QEvent::LeaveWhatsThisMode`：`125`;当应用程序离开“这是什么？”模式时，发送到顶层控件。
- `QEvent::LocaleChange`：`88`;系统所在地发生变化。
- `QEvent::NonClientAreaMouseButtonDblClick`：`176`;客户端区域外发生了鼠标双击（`QMouseEvent`）。
- `QEvent::NonClientAreaMouseButtonPress`：`174`;鼠标按键发生在客户端区域（`QMouseEvent`）之外。
- `QEvent::NonClientAreaMouseButtonRelease`：`175`;鼠标按键释放发生在客户端区域外（`QMouseEvent`）。
- `QEvent::NonClientAreaMouseMove`：`173`;鼠标移动发生在客户端区域（`QMouseEvent`）之外。
- `QEvent::MacSizeChange`：`177`;用户更改了他的控件大小（仅限macOS）。
- `QEvent::MetaCall`：`43`;通过`QMetaObject::invokeMethod()`进行异步方法调用。
- `QEvent::ModifiedChange`：`102`;控件的修改状态已更改。
- `QEvent::MouseButtonDblClick`：`4`;再次按键（`QMouseEvent`）。
- `QEvent::MouseButtonPress`：`2`;鼠标压制机（`QMouseEvent`）。
- `QEvent::MouseButtonRelease`：`3`;老鼠释放（`QMouseEvent`）。
- `QEvent::MouseMove`：`5`;鼠标移动（`QMouseEvent`）。
- `QEvent::MouseTrackingChange`：`109`;鼠标追踪状态发生变化。
- `QEvent::Move`：`13`;小部件位置发生变化（`QMoveEvent`）。
- `QEvent::NativeGesture`：`197`;系统检测到一个手势（`QNativeGestureEvent`）。
- `QEvent::OrientationChange`：`208`;屏幕的方向会发生变化（QScreenOrientationChangeEvent）。
- `QEvent::Paint`：`12`;屏幕更新必要（`QPaintEvent`）。
- `QEvent::PaletteChange`：`39`;控件的调色板发生了变化。
- `QEvent::ParentAboutToChange`：`131`;对象父节点即将更改。仅发送给某些对象类型，如`QWidget`。
- `QEvent::ParentChange`：`21`;对象父节点发生了变化。仅发送给某些对象类型，如`QWidget`。
- `QEvent::ParentWindowAboutToChange (since Qt 6.7)`：`225`;父窗口即将变换。
- `QEvent::ParentWindowChange (since Qt 6.7)`：`226`;父窗口发生了变化。
- `QEvent::PlatformPanel`：`212`;已请求设立平台专属小组。
- `QEvent::PlatformSurface`：`217`;已创建或即将被摧毁的原生平台表面（`QPlatformSurfaceEvent`）。
- `QEvent::Polish`：`75`;小部件经过抛光。
- `QEvent::PolishRequest`：`74`;小部件应被抛光。
- `QEvent::QueryWhatsThis`：`123`;如果小部件有“这是什么？”帮助（`QHelpEvent`），应接受该事件。
- `QEvent::Quit`：`20`;应用已退出。
- `QEvent::ReadOnlyChange (since Qt 5.4)`：`106`;小部件的只读状态发生了变化。
- `QEvent::RequestSoftwareInputPanel`：`199`;一个小部件想要打开软件输入面板（SIP）。
- `QEvent::Resize`：`14`;小部件大小发生变化（`QResizeEvent`）。
- `QEvent::ScrollPrepare`：`204`;物体需要填写其几何信息（`QScrollPrepareEvent`）。
- `QEvent::Scroll`：`205`;物体需要滚动到指定位置（`QScrollEvent`）。
- `QEvent::Shortcut`：`117`;子键用于快捷键操作（`QShortcutEvent`）。
- `QEvent::ShortcutOverride`：`51`;子键操作，用于覆盖快捷键操作（`QKeyEvent`）。当快捷方式即将触发时，`ShortcutOverride`会发送到当前窗口。这允许客户端（例如控件）通过接受事件来表示他们将自行处理该快捷方式。如果快捷键覆盖被接受，事件将作为正常按键传递给焦点控件。否则，如果存在快捷方式动作，则触发该动作。
- `QEvent::Show`：`17`;小部件显示在屏幕上（`QShowEvent`）。
- `QEvent::ShowToParent`：`26`;已展示一个子控件。
- `QEvent::SockAct`：`50`;套接字激活，用于实现`QSocketNotifier`。
- `QEvent::StateMachineSignal`：`192`;传递给状态机（`QStateMachine::SignalEvent`）的信号。
- `QEvent::StateMachineWrapped`：`193`;该事件是另一个事件（`QStateMachine::WrappedEvent`）的包装器，即包含另一个事件()。
- `QEvent::StatusTip`：`112`;请求状态提示（`QStatusTipEvent`）。
- `QEvent::StyleChange`：`100`;小部件的样式已更改。
- `QEvent::TabletMove`：`87`;Wacom绘板移动（`QTabletEvent`）。
- `QEvent::TabletPress`：`92`;Wacom平板印刷机（`QTabletEvent`）。
- `QEvent::TabletRelease`：`93`;Wacom绘图板发行（`QTabletEvent`年）。
- `QEvent::TabletEnterProximity`：`171`;Wacom绘图板进入接近事件（`QTabletEvent`），发送到`QApplication`。
- `QEvent::TabletLeaveProximity`：`172`;Wacom绘图板离场事件（`QTabletEvent`），发送到`QApplication`。
- `QEvent::TabletTrackingChange (since Qt 5.9)`：`219`;Wacom绘图板的追踪状态发生了变化。
- `QEvent::ThreadChange`：`22`;该对象被移动到另一个线程。这是上一个线程中发送给该对象的最后一个事件。详见`QObject::moveToThread()`。
- `QEvent::Timer`：`1`;常规计时器事件（`QTimerEvent`）。
- `QEvent::ToolBarChange`：`120`;macOS上工具栏按钮被切换。
- `QEvent::ToolTip`：`110`;请求提供提示（`QHelpEvent`）。
- `QEvent::ToolTipChange`：`184`;小部件的工具提示发生了变化。
- `QEvent::TouchBegin`：`194`;触摸屏或触控板事件序列的开始（`QTouchEvent`）。
- `QEvent::TouchCancel`：`209`;取消触碰事件序列（`QTouchEvent`）。
- `QEvent::TouchEnd`：`196`;触控事件序列结束（`QTouchEvent`）。
- `QEvent::TouchUpdate`：`195`;触摸屏事件（`QTouchEvent`）。
- `QEvent::UngrabKeyboard`：`189`;物品失去键盘抓取（仅`QGraphicsItem`）。
- `QEvent::UngrabMouse`：`187`;物品失去鼠标抓取（`QGraphicsItem`，`QQuickItem`）。
- `QEvent::UpdateLater`：`78`;该小部件应排队等待以后重新涂装。
- `QEvent::UpdateRequest`：`77`;小部件应重新涂装。
- `QEvent::WhatsThis`：`111`;小部件应显示“这是什么？”帮助（`QHelpEvent`）。
- `QEvent::WhatsThisClicked`：`118`;点击了一个小部件“这是什么？”帮助中的链接。
- `QEvent::Wheel`：`31`;滚鼠轮（`QWheelEvent`）。
- `QEvent::WinEventAct`：`132`;发生了Windows特定的激活事件。
- `QEvent::WindowActivate`：`24`;窗口已启动。
- `QEvent::WindowBlocked`：`103`;窗口被模态对话框屏蔽。
- `QEvent::WindowDeactivate`：`25`;窗口已被关闭。
- `QEvent::WindowIconChange`：`34`;窗口图标发生变化。
- `QEvent::WindowStateChange`：`105`;窗口状态（最小化、最大化或全屏）发生变化（`QWindowStateChangeEvent`）。
- `QEvent::WindowTitleChange`：`33`;窗户标题已更改。
- `QEvent::WindowUnblocked`：`104`;在模态对话结束后窗口会被解除阻塞。
- `QEvent::WinIdChange`：`203`;该本地控件的窗口系统标识符已更改。
- `QEvent::ZOrderChange`：`126`;小部件的 z 顺序发生了变化。该事件从未发送到顶层窗口。
- `QEvent::SafeAreaMarginsChange (since Qt 6.9)`：`227`;窗口的安全区域边界发生变化。
用户事件的值应介于`User`到`MaxUser`之间：
- `QEvent::User`：`1000`;用户定义事件。
- `QEvent::MaxUser`：`65535`;最后用户事件ID。
为了方便起见，您可以使用`registerEventType()`功能注册并保留一个自定义事件类型。这样做可以避免误用应用中已在其他地方使用的自定义事件类型。

### `accepted : bool`

**作用与语义：**

该属性包含事件对象的accept标志。
设置accept参数表示事件接收方需要该事件。不需要的事件可能会传播到父控件。默认情况下，isAccepted() 设置为true，但不要依赖它，因为子类可能会在其构造函数中选择清除该参数。
为了方便，接受标志也可以设置为`accept()`，并以`ignore()`清除。
注意：接受`QPointerEvent`隐含`accepts`该事件所承载的所有`points`。

**如何使用：** 调用 `accepted()` 读取当前值；它不会修改应用状态。

### `[explicit] QEvent::QEvent(QEvent::Type type)`

**作用与语义：**

构造类型为`type`的事件对象。

### `[virtual noexcept] QEvent::~QEvent()`

**作用与语义：**

销毁该事件。如果是`posted`，将从待发布事件列表中移除。

### `void QEvent::accept()`

**作用与语义：**

设置事件对象的accept标志，相当于调用`setAccepted`（true）。
设置接受参数表示事件接收方需要该事件。不需要的事件可能会传播到父组件。

### `[virtual, since 6.0] QEvent *QEvent::clone() const`

**作用与语义：**

创建并返回该事件的完全相同的副本。

### `void QEvent::ignore()`

**作用与语义：**

清除事件对象的accept标志参数，相当于调用`setAccepted`（false）。
清除accept参数表示事件接收方不希望该事件。不需要的事件可能会传播到父控件。

### `[noexcept, since 6.0] bool QEvent::isInputEvent() const`

**作用与语义：**

如果事件对象是`QInputEvent`还是其子类，返回`true`。

### `[noexcept, since 6.0] bool QEvent::isPointerEvent() const`

**作用与语义：**

如果事件对象是`QPointerEvent`还是其子类，返回`true`。

### `[noexcept, since 6.0] bool QEvent::isSinglePointEvent() const`

**作用与语义：**

如果事件对象是`QSinglePointEvent`的子类，返回`true`。

### `[static noexcept] int QEvent::registerEventType(int hint = -1)`

**作用与语义：**

注册并返回自定义事件类型。如果提供的`hint`可用，将被使用;否则返回的值介于`QEvent::User`到`QEvent::MaxUser`之间，且尚未注册。如果`hint`值不在`QEvent::User`和`QEvent::MaxUser`之间，则被忽略。
如果所有可用值都已取用或程序正在关闭，返回 -1。
注意：该功能是线程安全的。

### `bool QEvent::spontaneous() const`

**作用与语义：**

如果事件起源于应用程序外部（系统事件），返回`true`;否则返回`false`。

### `QEvent::Type QEvent::type() const`

**作用与语义：**

返回事件类型。

### `bool isAccepted() const`

**作用与语义：**

该属性包含事件对象的accept标志。
设置accept参数表示事件接收方需要该事件。不需要的事件可能会传播到父控件。默认情况下，isAccepted() 设置为true，但不要依赖它，因为子类可能会在其构造函数中选择清除该参数。
为了方便，接受标志也可以设置为`accept()`，并以`ignore()`清除。
注意：接受`QPointerEvent`隐含`accepts`该事件所承载的所有`points`。

**如何使用：** 调用 `isAccepted()` 读取当前值；它不会修改应用状态。

### `virtual void setAccepted(bool accepted)`

**作用与语义：**

该属性包含事件对象的accept标志。
设置accept参数表示事件接收方需要该事件。不需要的事件可能会传播到父控件。默认情况下，isAccepted() 设置为true，但不要依赖它，因为子类可能会在其构造函数中选择清除该参数。
为了方便，接受标志也可以设置为`accept()`，并以`ignore()`清除。
注意：接受`QPointerEvent`隐含`accepts`该事件所承载的所有`points`。

**如何使用：** 调用 `setAccepted(...)` 修改 `accepted`；传入的新值会成为后续查询和相关界面行为所使用的值。

## 6. 深入实践与常见坑

### 生命周期和资源边界

值对象由作用域、容器或调用者管理，不使用 parent 和 deleteLater。跨线程传递副本通常比传递 QObject 安全，但共享数据在写入时仍可能发生复制，性能和内存峰值要结合数据规模判断。

### 状态和错误边界

重点区分空值、无效值、默认值和已初始化值。例如空字符串、空 URL、null 图像和无效索引不一定表示同一件事；转换函数的失败结果要通过对应的状态查询确认。

### 线程边界

值类型本身通常可以复制后跨线程传递；不要把 data()/bits()/constData() 得到的指针当成跨线程长期有效的所有权。大对象频繁写入会触发 detach，应避免不必要的复制和格式转换。

### 最容易出现的错误

不要保存短生命周期事件指针；不要无条件吞掉事件；坐标系、设备像素比和键盘自动重复都要按事件类型处理。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QEvent` 所属机制类型：Qt 值类型与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
