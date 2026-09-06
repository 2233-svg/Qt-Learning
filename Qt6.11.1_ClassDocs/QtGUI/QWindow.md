# QWindow

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 底层窗口对象，负责窗口表面、屏幕、输入事件、可见性和窗口系统交互。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QWindow`：底层窗口对象，负责窗口表面、屏幕、输入事件、可见性和窗口系统交互。

**内部模型：** Widgets 通过父子控件树、布局系统、事件分发和重绘请求组成界面。控件的可见区域、sizeHint、sizePolicy、字体和平台 style 共同影响最终几何；用户输入先进入 Qt 事件系统，再由控件的事件函数、信号或快捷键处理。

**适用场景：** 创建 QApplication 后创建控件，设置 parent 或把控件加入布局，连接用户操作信号，再显示顶层窗口。复合界面用布局嵌套；控件尺寸异常时同时检查 sizePolicy、minimum/maximum size、layout stretch、margins 和 spacing。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要用固定坐标拼接响应式界面；不要给已经加入布局的控件反复 `setGeometry()`；不要在 `paintEvent()` 中修改业务状态；不要忘记窗口关闭、对象销毁和应用退出是三个不同事件。

## 2. 依赖与对象关系

- 头文件：`#include <QWindow>`
- 继承自：QObject、QSurface
- 直接派生类：QPaintDeviceWindow、QQuickWindow,、QVulkanWindow

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

Widgets 通过父子控件树、布局系统、事件分发和重绘请求组成界面。控件的可见区域、sizeHint、sizePolicy、字体和平台 style 共同影响最终几何；用户输入先进入 Qt 事件系统，再由控件的事件函数、信号或快捷键处理。

### 状态、生命周期和线程

**生命周期：** 控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

**状态与结果：** 控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

**线程与事件循环：** 所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

## 3. 直接使用

创建 QApplication 后创建控件，设置 parent 或把控件加入布局，连接用户操作信号，再显示顶层窗口。复合界面用布局嵌套；控件尺寸异常时同时检查 sizePolicy、minimum/maximum size、layout stretch、margins 和 spacing。 使用时通常按这个过程组织：构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum AncestorMode { ExcludeTransients, IncludeTransients }`
- `enum Visibility { Windowed, Minimized, Maximized, FullScreen, AutomaticVisibility, Hidden }`

### 属性

- `active : bool`
- `contentOrientation : Qt::ScreenOrientation`
- `flags : Qt::WindowFlags`
- `height : int`
- `maximumHeight : int`
- `maximumWidth : int`
- `minimumHeight : int`
- `minimumWidth : int`
- `modality : Qt::WindowModality`
- `opacity : qreal`
- `title : QString`
- `transientParent : QWindow*`
- `visibility : Visibility`
- `visible : bool`
- `width : int`
- `x : int`
- `y : int`

### 公有函数

- `QWindow(QScreen *targetScreen = nullptr)`
- `QWindow(QWindow *parent)`
- `virtual ~QWindow()`
- `QSize baseSize() const`
- `Qt::ScreenOrientation contentOrientation() const`
- `void create()`
- `QCursor cursor() const`
- `void destroy()`
- `qreal devicePixelRatio() const`
- `QString filePath() const`
- `Qt::WindowFlags flags() const`
- `virtual QObject * focusObject() const`
- `QRect frameGeometry() const`
- `QMargins frameMargins() const`
- `QPoint framePosition() const`
- `QRect geometry() const`
- `int height() const`
- `QIcon icon() const`
- `bool isActive() const`
- `bool isAncestorOf(const QWindow *child, QWindow::AncestorMode mode = IncludeTransients) const`
- `bool isExposed() const`
- `bool isModal() const`
- `bool isTopLevel() const`
- `bool isVisible() const`
- `(since 6.0) QPointF mapFromGlobal(const QPointF &pos) const`
- `QPoint mapFromGlobal(const QPoint &pos) const`
- `(since 6.0) QPointF mapToGlobal(const QPointF &pos) const`
- `QPoint mapToGlobal(const QPoint &pos) const`
- `QRegion mask() const`
- `int maximumHeight() const`
- `QSize maximumSize() const`
- `int maximumWidth() const`
- `int minimumHeight() const`
- `QSize minimumSize() const`
- `int minimumWidth() const`
- `Qt::WindowModality modality() const`
- `qreal opacity() const`
- `QWindow * parent(QWindow::AncestorMode mode = ExcludeTransients) const`
- `QPoint position() const`
- `void reportContentOrientationChange(Qt::ScreenOrientation orientation)`
- `QSurfaceFormat requestedFormat() const`
- `void resize(const QSize &newSize)`
- `void resize(int w, int h)`
- `(since 6.9) QMargins safeAreaMargins() const`
- `QScreen * screen() const`
- `void setBaseSize(const QSize &size)`
- `void setCursor(const QCursor &cursor)`
- `void setFilePath(const QString &filePath)`
- `void setFlag(Qt::WindowType flag, bool on = true)`
- `void setFlags(Qt::WindowFlags flags)`
- `void setFormat(const QSurfaceFormat &format)`
- `void setFramePosition(const QPoint &point)`
- `void setIcon(const QIcon &icon)`
- `bool setKeyboardGrabEnabled(bool grab)`
- `void setMask(const QRegion &region)`
- `void setMaximumSize(const QSize &size)`
- `void setMinimumSize(const QSize &size)`
- `void setModality(Qt::WindowModality modality)`
- `bool setMouseGrabEnabled(bool grab)`
- `void setOpacity(qreal level)`
- `void setParent(QWindow *parent)`
- `void setPosition(const QPoint &pt)`
- `void setPosition(int posx, int posy)`
- `void setScreen(QScreen *newScreen)`
- `void setSizeIncrement(const QSize &size)`
- `void setSurfaceType(QSurface::SurfaceType surfaceType)`
- `void setTransientParent(QWindow *parent)`
- `void setVisibility(QWindow::Visibility v)`
- `void setVulkanInstance(QVulkanInstance *instance)`
- `void setWindowState(Qt::WindowState state)`
- `void setWindowStates(Qt::WindowStates state)`
- `QSize sizeIncrement() const`
- `QString title() const`
- `QWindow * transientParent() const`
- `Qt::WindowType type() const`
- `void unsetCursor()`
- `QWindow::Visibility visibility() const`
- `QVulkanInstance * vulkanInstance() const`
- `int width() const`
- `WId winId() const`
- `Qt::WindowState windowState() const`
- `Qt::WindowStates windowStates() const`
- `int x() const`
- `int y() const`

### 重实现的公有函数

- `virtual QSurfaceFormat format() const override`
- `virtual QSize size() const override`
- `virtual QSurface::SurfaceType surfaceType() const override`

### 公有槽函数

- `void alert(int msec)`
- `bool close()`
- `void hide()`
- `void lower()`
- `void raise()`
- `void requestActivate()`
- `void requestUpdate()`
- `void setGeometry(const QRect &rect)`
- `void setGeometry(int posx, int posy, int w, int h)`
- `void setHeight(int arg)`
- `void setMaximumHeight(int h)`
- `void setMaximumWidth(int w)`
- `void setMinimumHeight(int h)`
- `void setMinimumWidth(int w)`
- `void setTitle(const QString &)`
- `void setVisible(bool visible)`
- `void setWidth(int arg)`
- `void setX(int arg)`
- `void setY(int arg)`
- `void show()`
- `void showFullScreen()`
- `void showMaximized()`
- `void showMinimized()`
- `void showNormal()`
- `bool startSystemMove()`
- `bool startSystemResize(Qt::Edges edges)`

### 信号

- `void activeChanged()`
- `void contentOrientationChanged(Qt::ScreenOrientation orientation)`
- `void flagsChanged(Qt::WindowFlags flags)`
- `void focusObjectChanged(QObject *object)`
- `void heightChanged(int arg)`
- `void maximumHeightChanged(int arg)`
- `void maximumWidthChanged(int arg)`
- `void minimumHeightChanged(int arg)`
- `void minimumWidthChanged(int arg)`
- `void modalityChanged(Qt::WindowModality modality)`
- `void opacityChanged(qreal opacity)`
- `(since 6.9) void safeAreaMarginsChanged(QMargins margins)`
- `void screenChanged(QScreen *screen)`
- `void transientParentChanged(QWindow *transientParent)`
- `void visibilityChanged(QWindow::Visibility visibility)`
- `void visibleChanged(bool arg)`
- `void widthChanged(int arg)`
- `void windowStateChanged(Qt::WindowState windowState)`
- `void windowTitleChanged(const QString &title)`
- `void xChanged(int arg)`
- `void yChanged(int arg)`

### 静态公有成员

- `QWindow * fromWinId(WId id)`

### 保护函数

- `virtual void closeEvent(QCloseEvent *ev)`
- `virtual void exposeEvent(QExposeEvent *ev)`
- `virtual void focusInEvent(QFocusEvent *ev)`
- `virtual void focusOutEvent(QFocusEvent *ev)`
- `virtual void hideEvent(QHideEvent *ev)`
- `virtual void keyPressEvent(QKeyEvent *ev)`
- `virtual void keyReleaseEvent(QKeyEvent *ev)`
- `virtual void mouseDoubleClickEvent(QMouseEvent *ev)`
- `virtual void mouseMoveEvent(QMouseEvent *ev)`
- `virtual void mousePressEvent(QMouseEvent *ev)`
- `virtual void mouseReleaseEvent(QMouseEvent *ev)`
- `virtual void moveEvent(QMoveEvent *ev)`
- `virtual bool nativeEvent(const QByteArray &eventType, void *message, qintptr *result)`
- `(since 6.0) virtual void paintEvent(QPaintEvent *ev)`
- `virtual void resizeEvent(QResizeEvent *ev)`
- `virtual void showEvent(QShowEvent *ev)`
- `virtual void tabletEvent(QTabletEvent *ev)`
- `virtual void touchEvent(QTouchEvent *ev)`
- `virtual void wheelEvent(QWheelEvent *ev)`

### 重实现的保护函数

- `virtual bool event(QEvent *ev) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QWindow::AncestorMode`

**作用与语义：**

此枚举用于控制是否应将临时父项视为祖先。
- `QWindow::ExcludeTransients`: `0`; 临时父项不被视为祖先。
- `QWindow::IncludeTransients`: `1`; 临时父项被视为祖先。

### `enum QWindow::Visibility`

**作用与语义：**

这个枚举描述了窗户占据或应占屏幕的哪个部分。
- `QWindow::Windowed`：`2`;窗口占据屏幕的一部分，但不一定覆盖整个屏幕。此状态仅发生在支持同时显示多个窗口的窗口系统中。在此状态下，用户可以手动移动和调整窗口大小，前提是窗口标志允许且窗口系统支持。
- `QWindow::Minimized`：`3`;根据窗口系统如何处理最小化窗口，窗口会被缩减为任务栏、底座、任务列表或桌面上的条目或图标。
- `QWindow::Maximized`：`4`;窗口占据整块屏幕，标题栏仍然可见。在大多数窗口系统中，点击工具栏的最大化按钮即可实现此状态。
- `QWindow::FullScreen`：`5`;窗口占据整块屏幕，不可调整大小，且没有标题栏。在某些不支持同时显示多个窗口的平台上，当窗口未被隐藏时，这可能是常见的可见性。
- `QWindow::AutomaticVisibility`：`1`;这意味着为窗口设定默认可见状态，根据平台不同，可能是全屏或窗口状态。它可以作为参数`setVisibility`，但永远不会从可视化访问器读取回来。
- `QWindow::Hidden`：`0`;窗口以任何方式不可见，但可能保留潜在可见性，通过设置自动可见性（AutomaticVisibility）可以恢复。

### `[read-only] active : bool`

**作用与语义：**

该属性表示窗口的活跃状态。

**如何使用：** 调用 `active()` 读取当前值；它不会修改应用状态。

### `contentOrientation : Qt::ScreenOrientation`

**作用与语义：**

此属性保存窗口内容的方向。
这是对窗口管理器的提示，以防它需要显示额外内容，如弹出窗口、对话框、状态栏或类似内容，相对于窗口的位置。
推荐的方向是 `QScreen::orientation()`，但应用程序不必支持所有可能的方向，因此可以选择忽略当前屏幕方向。
窗口与内容方向之间的差异决定了需要旋转内容的角度。`QScreen::angleBetween()`、`QScreen::transformBetween()` 和 `QScreen::mapBetween()` 可用于计算必要的变换。
默认值为 `Qt::PrimaryOrientation`。

**如何使用：** 调用 `contentOrientation()` 读取当前值；它不会修改应用状态。

### `flags : Qt::WindowFlags`

**作用与语义：**

该属性保留窗户的标志。
窗口标志控制窗口在窗口系统中的外观，无论是对话框、弹窗还是普通窗口，以及是否应该有标题栏等。
如果请求的标志无法满足，实际的窗口标志可能与 setFlags() 设置的标志不同。

**如何使用：** 调用 `flags()` 读取当前值；它不会修改应用状态。

### `height : int`

**作用与语义：**

该属性表示窗口几何形状的高度。

**如何使用：** 调用 `height()` 读取当前值；它不会修改应用状态。

### `maximumHeight : int`

**作用与语义：**

该属性表示了窗口几何的最大高度。

**如何使用：** 调用 `maximumHeight()` 读取当前值；它不会修改应用状态。

### `maximumWidth : int`

**作用与语义：**

该属性表示了窗口几何的最大宽度。

**如何使用：** 调用 `maximumWidth()` 读取当前值；它不会修改应用状态。

### `minimumHeight : int`

**作用与语义：**

该属性表示了窗口几何形状的最小高度。

**如何使用：** 调用 `minimumHeight()` 读取当前值；它不会修改应用状态。

### `minimumWidth : int`

**作用与语义：**

该属性表示窗口几何形状的最小宽度。

**如何使用：** 调用 `minimumWidth()` 读取当前值；它不会修改应用状态。

### `modality : Qt::WindowModality`

**作用与语义：**

该属性表示窗口的模态性。
模态窗口防止其他窗口接收输入事件。Qt 支持两种模态：`Qt::WindowModal` 和 `Qt::ApplicationModal`。
默认情况下，该属性为`Qt::NonModal`。

**如何使用：** 调用 `modality()` 读取当前值；它不会修改应用状态。

### `opacity : qreal`

**作用与语义：**

该属性决定了窗口系统中窗口的不透明度。
如果窗口系统支持窗口不透明度，可以用来淡入和淡出窗口，或使其半透明。
1.0及以上的数值被视为完全不透明，而0.0及以下的数值则被视为完全透明。介于两者的值代表两极之间的不同透明度水平。
默认值是1.0。

**如何使用：** 调用 `opacity()` 读取当前值；它不会修改应用状态。

### `title : QString`

**作用与语义：**

该属性在窗口系统中保留了窗口的标题。
窗口标题可能出现在窗口装饰的标题区域，具体取决于窗口系统和窗口标志。窗口系统也可能用它来识别其他上下文中的窗口，比如任务切换器中。

**如何使用：** 调用 `title()` 读取当前值；它不会修改应用状态。

### `transientParent : QWindow*`

**作用与语义：**

该属性包含该窗口作为瞬态弹出窗口的窗口。
这向窗口管理器提示该窗口是代表瞬态父窗口的对话框或弹窗。
为了使窗口默认置中于其瞬态`parent`之上，根据窗口管理器的不同，可能需要调用合适的`Qt::WindowType`（如`Qt::Dialog`）的`setFlags()`。

**如何使用：** 调用 `transientParent()` 读取当前值；它不会修改应用状态。

### `visibility : Visibility`

**作用与语义：**

该属性表示窗户的屏幕占用状态。
可见性是指窗口应以正常、最小化、最大化、全屏还是隐藏显示。
要将可见性设置为`AutomaticVisibility`意味着给窗口一个默认可见状态，这取决于平台，可能是全屏或窗口状态。读取可见性属性时，你总是得到实际状态，永远不会`AutomaticVisibility`。
默认值为隐藏。

**如何使用：** 调用 `visibility()` 读取当前值；它不会修改应用状态。

### `visible : bool`

**作用与语义：**

无论窗户是否可见，这一属性都成立。
该属性控制窗口在窗口系统中的可见性。
默认情况下，窗口不可见，你必须调用 setVisible（true）、`show()` 或类似的命令才能显示。
注意：隐藏窗口不会将该窗口从窗口系统中移除，只是隐藏它。在为全屏应用程序提供专用桌面的窗口系统（如macOS）中，隐藏全屏窗口不会移除该桌面，但保持空白。同一应用程序中的另一个窗口可能会显示全屏，并填满该桌面。使用`QWindow::close`完全移除窗口系统中的窗口。

**如何使用：** 调用 `visible()` 读取当前值；它不会修改应用状态。

### `width : int`

**作用与语义：**

该属性表示窗口几何形状的宽度。

**如何使用：** 调用 `width()` 读取当前值；它不会修改应用状态。

### `x : int`

**作用与语义：**

该属性表示窗口几何形状的 x 位置。

**如何使用：** 调用 `x()` 读取当前值；它不会修改应用状态。

### `y : int`

**作用与语义：**

该属性表示窗口几何形状的 y 位置。

**如何使用：** 调用 `y()` 读取当前值；它不会修改应用状态。

### `[explicit] QWindow::QWindow(QScreen *targetScreen = nullptr)`

**作用与语义：**

在`targetScreen`上创建一个窗口作为顶层。
直到调用`setVisible`（真）、`show()`或类似的条件时，窗口才会显示。

### `[explicit] QWindow::QWindow(QWindow *parent)`

**作用与语义：**

作为给定`parent`窗口的子窗口创建窗口。
窗口会嵌入父窗口内部，父窗口相对于父窗口的坐标。
屏幕是从父方继承的。

### `[virtual noexcept] QWindow::~QWindow()`

**作用与语义：**

把窗户都砸了。

### `[slot] void QWindow::alert(int msec)`

**作用与语义：**

该功能会显示`msec`毫秒的警报。如果`msec`是`0`（默认），则警报会无限期显示，直到窗口重新激活。该功能对当前的窗口没有影响。
在警报状态下，窗口表示需要关注，例如通过闪烁或跳动任务栏条目来表示。

### `QSize QWindow::baseSize() const`

**作用与语义：**

返回窗口的基础尺寸。

### `[slot] bool QWindow::close()`

**作用与语义：**

关上窗户。
这会关闭窗口，实际上调用`destroy()`，并可能导致应用程序退出。成功时返回`true`，如果有父窗口则返回为false（此时应关闭顶层窗口）。

### `[virtual protected] void QWindow::closeEvent(QCloseEvent *ev)`

**作用与语义：**

在处理接近事件（`ev`）时，可以覆盖此设置。
当窗口被请求关闭时，该函数被调用。如果你想阻止窗口关闭，可以在事件中调用`QEvent::ignore()`。

### `void QWindow::create()`

**作用与语义：**

分配与窗口相关平台资源。
此时，使用 `setFormat()` 设置的表面格式被解析为实际的原生表面。然而，窗口在调用 `setVisible()` 之前保持隐藏状态。
注意，通常不必直接调用该函数，因为它会被 `show()`、`setVisible()`、`winId()` 及其他需要访问平台资源的函数隐式调用。
如有必要，请打电话`destroy()`释放平台资源。

### `QCursor QWindow::cursor() const`

**作用与语义：**

该窗口的光标形状。

### `void QWindow::destroy()`

**作用与语义：**

释放与该窗口相关的本地平台资源。

### `qreal QWindow::devicePixelRatio() const`

**作用与语义：**

返回窗口的物理像素与设备无关像素的比例。该值取决于窗口所在的屏幕，且当窗口移动时可能会变化。
当设备像素比变化时，`QWindow`实例会收到类型为`QEvent::DevicePixelRatioChange`的事件。
常见数值为普通显示器的1.0和苹果“视网膜”显示器的2.0。
注意：对于没有平台窗口支持的窗口，即未调用`create()`，函数将退回到对应`QScreen`的设备像素比例。

### `[override virtual protected] bool QWindow::event(QEvent *ev)`

**作用与语义：**

重实现自：`QObject::event`（QEvent *e）。
覆盖此设置以处理发送到窗口的任何事件（`ev`）。如果事件被识别并处理，返回`true`。
如果你希望鼠标事件、键事件、调整大小事件等能像平常一样被派发，记得调用基础类版本。

### `[virtual protected] void QWindow::exposeEvent(QExposeEvent *ev)`

**作用与语义：**

当窗口在未暴露状态和暴露状态之间移动时，窗口系统会发送暴露事件（`ev`）。
一个暴露的窗口可能对用户可见。如果窗口被移出屏幕、被另一个窗口完全遮挡、被最小化或类似情况，可能会调用该函数，`isExposed()`值可能会变为false。你可以利用此事件限制昂贵操作，如动画，仅在窗口暴露时运行。
这个事件不应该用来绘画。要处理绘画工具，应该用`paintEvent()`。
每次窗口首次显示时，都会在曝光事件之前发送一个缩小事件。

### `QString QWindow::filePath() const`

**作用与语义：**

这个窗口所代表的文件名。

### `[virtual protected] void QWindow::focusInEvent(QFocusEvent *ev)`

**作用与语义：**

在事件中（`ev`）时，可以覆盖这个处理。
当窗口接收键盘聚焦时，事件中的焦点会被发送。

### `[virtual] QObject *QWindow::focusObject() const`

**作用与语义：**

返回将成为相关事件（如按键事件）最终接收者的`QObject`。

### `[signal] void QWindow::focusObjectChanged(QObject *object)`

**作用与语义：**

当与焦点相关的事件最终接收器切换为`object`时，该信号会发出。

### `[virtual protected] void QWindow::focusOutEvent(QFocusEvent *ev)`

**作用与语义：**

覆盖此功能以处理聚焦事件（`ev`）。
当窗口失去键盘焦点时，会发送聚焦外事件。

### `[override virtual] QSurfaceFormat QWindow::format() const`

**作用与语义：**

重装：`QSurface::format()` const.
返回该窗口的实际格式。
窗口创建后，该函数会返回窗口的实际表层格式。如果平台无法满足请求格式，表表格式可能与请求格式不同。它也可能是一个超集，例如某些缓冲区大小可能大于请求的。
注意：根据平台不同，该表面格式中的某些值可能仍包含请求的值，即已传递给`setFormat()`的值。典型例子包括OpenGL版本、配置文件和选项。这些选项可能不会在 `create()` 更新，因为它们是上下文特定的，且单个窗口可能在其生命周期内与多个上下文一起使用。查询这些值时，请使用`QOpenGLContext`的格式()来查询。
返回表面的格式。

### `QRect QWindow::frameGeometry() const`

**作用与语义：**

返回窗口的几何形状，包括窗框。
几何体与其屏幕的虚拟几何体（virtualGeometry()相关联。

### `QMargins QWindow::frameMargins() const`

**作用与语义：**

返回窗框周围的边距。

### `QPoint QWindow::framePosition() const`

**作用与语义：**

返回窗口左上角的位置，包括窗框。
这与 `frameGeometry()`.topLeft() 返回相同的值。

### `[static] QWindow *QWindow::fromWinId(WId id)`

**作用与语义：**

通过使用Qt下方的本地库创建的窗口，创建由其他进程创建的窗口的本地表示。
给定`id`本地窗口的句柄，该方法创建一个`QWindow`对象，用于调用`setParent()`和`setTransientParent()`等方法时表示该窗口。
在支持该方法的平台上，这可以用来嵌入`QWindow`到原生窗口中，或者嵌入本地窗口到`QWindow`中。
如果不支持外部窗口或嵌入本地窗口失败，该函数返回`nullptr`。
注意：所得`QWindow`不应用于操作底层原生窗口（除重新父级处理外），也不应用于观察原生窗口的状态变化。对此类操作的支持是偶然的，高度依赖平台且未经测试。

### `QRect QWindow::geometry() const`

**作用与语义：**

返回窗户几何形状，但不包括窗框。
几何体与其屏幕的虚拟几何体（virtualGeometry()相关联。

### `[slot] void QWindow::hide()`

**作用与语义：**

遮住窗户。
等同于调用`setVisible`（false）。

### `[virtual protected] void QWindow::hideEvent(QHideEvent *ev)`

**作用与语义：**

覆盖此功能以处理隐藏事件（`ev`）。
当窗口请求隐藏在窗口系统中时，调用该函数。

### `QIcon QWindow::icon() const`

**作用与语义：**

在窗口系统中返回窗口图标。

### `bool QWindow::isActive() const`

**作用与语义：**

该属性表示窗口的活跃状态。

**如何使用：** 调用 `isActive()` 读取当前值；它不会修改应用状态。

### `bool QWindow::isAncestorOf(const QWindow *child, QWindow::AncestorMode mode = IncludeTransients) const`

**作用与语义：**

如果窗口是给定`child`的祖先，返回`true`。如果`mode` `IncludeTransients`，则暂时父窗口也被视为祖先。

### `bool QWindow::isExposed() const`

**作用与语义：**

如果窗口系统中该窗口被暴露，则返回。
当窗口未被曝光时，应用程序会显示它，但窗口系统中仍然显示不出来，因此应用应尽量减少动画和其他图形活动。
每当该值变化时都会发送`exposeEvent()`。

### `bool QWindow::isModal() const`

**作用与语义：**

返回窗口是否为模态。
模态窗口防止其他窗口接收任何输入。

### `bool QWindow::isTopLevel() const`

**作用与语义：**

返回窗口是否为顶层，即没有父窗口。

### `[virtual protected] void QWindow::keyPressEvent(QKeyEvent *ev)`

**作用与语义：**

覆盖此功能以处理按键事件（`ev`）。

### `[virtual protected] void QWindow::keyReleaseEvent(QKeyEvent *ev)`

**作用与语义：**

覆盖此权限以处理密钥释放事件（`ev`）。

### `[slot] void QWindow::lower()`

**作用与语义：**

降低窗户系统的窗口。
有人请求将窗户降下，使其位于其他窗户下方。

### `[since 6.0] QPointF QWindow::mapFromGlobal(const QPointF &pos) const`

**作用与语义：**

将全局屏幕坐标`pos`转换为窗口坐标。

### `QPoint QWindow::mapFromGlobal(const QPoint &pos) const`

**作用与语义：**

将全局屏幕坐标`pos`转换为窗口坐标。

### `[since 6.0] QPointF QWindow::mapToGlobal(const QPointF &pos) const`

**作用与语义：**

将窗口坐标`pos`转换为全局屏幕坐标。例如，`mapToGlobal(QPointF(0,0))`给出窗口左上角像素的全局坐标。

### `QPoint QWindow::mapToGlobal(const QPoint &pos) const`

**作用与语义：**

将窗口坐标`pos`转换为全局屏幕坐标。例如，`mapToGlobal(QPointF(0,0))`给出窗口左上角像素的全局坐标。

### `QRegion QWindow::mask() const`

**作用与语义：**

返回窗户上的遮罩套装。
遮罩是向窗口系统发出的提示，表示应用程序不希望在指定区域外接收鼠标或触摸输入。

### `QSize QWindow::maximumSize() const`

**作用与语义：**

返回窗口的最大大小。

### `QSize QWindow::minimumSize() const`

**作用与语义：**

返回窗口的最小尺寸。

### `[signal] void QWindow::modalityChanged(Qt::WindowModality modality)`

**作用与语义：**

该属性表示窗口的模态性。
模态窗口防止其他窗口接收输入事件。Qt 支持两种模态：`Qt::WindowModal` 和 `Qt::ApplicationModal`。
默认情况下，该属性为`Qt::NonModal`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `modality` 的变化，不要把它当作普通函数主动调用。

### `[virtual protected] void QWindow::mouseDoubleClickEvent(QMouseEvent *ev)`

**作用与语义：**

可以覆盖它来处理鼠标双击事件（`ev`）。

### `[virtual protected] void QWindow::mouseMoveEvent(QMouseEvent *ev)`

**作用与语义：**

覆盖此功能以处理鼠标移动事件（`ev`）。

### `[virtual protected] void QWindow::mousePressEvent(QMouseEvent *ev)`

**作用与语义：**

覆盖此功能以处理鼠标按压事件（`ev`）。

### `[virtual protected] void QWindow::mouseReleaseEvent(QMouseEvent *ev)`

**作用与语义：**

覆盖此功能以处理鼠标释放事件（`ev`）。

### `[virtual protected] void QWindow::moveEvent(QMoveEvent *ev)`

**作用与语义：**

覆盖此权限以处理窗口移动事件（`ev`）。

### `[virtual protected] bool QWindow::nativeEvent(const QByteArray &eventType, void *message, qintptr *result)`

**作用与语义：**

覆盖此设置以处理平台相关事件。将获得`eventType`、`message`和`result`。
这可能会让你的申请变得不可携带。
只有当事件被处理时才应返回true。

### `[virtual protected, since 6.0] void QWindow::paintEvent(QPaintEvent *ev)`

**作用与语义：**

每当窗口某个区域需要重新绘制时，比如最初显示该窗户，或移动另一扇窗户导致部分窗户暴露，窗户系统都会发送绘画事件（`ev`）。
应用程序应根据绘制事件渲染到窗口，无论窗口的暴露状态如何。例如，可能会在窗口暴露前发送绘画事件，以准备向用户展示。

### `QWindow *QWindow::parent(QWindow::AncestorMode mode = ExcludeTransients) const`

**作用与语义：**

如果有的话，返回父窗口。
如果`mode`是`IncludeTransients`，则如果没有父节点，则返回瞬态父节点。
没有父窗口的窗口称为顶层窗口。

### `QPoint QWindow::position() const`

**作用与语义：**

返回桌面上窗口的位置，不包括任何窗口框。
注意：并非所有窗口系统都支持设置或查询顶层窗口位置。在此类系统中，程序移动窗口可能无效，且当前位置（如`QPoint(0, 0)`）可能会返回人工值。

### `[slot] void QWindow::raise()`

**作用与语义：**

把窗户系统里的窗户升高。
请求将窗户升高，使其高于其他窗户。

### `[slot] void QWindow::requestActivate()`

**作用与语义：**

请求窗口被激活，即接收键盘焦点。

### `[slot] void QWindow::requestUpdate()`

**作用与语义：**

安排`QEvent::UpdateRequest`活动送到这个窗口。
在支持此类操作的平台上，事件与显示垂直同步同步传递。否则，事件延迟最多为5毫秒。如果窗口相关屏幕报告的刷新率高于60 Hz，时间间隔会缩减至小于5的值。额外的时间是为了给事件循环留出一些空闲时间以收集系统事件，并可通过QT_QPA_UPDATE_IDLE_TIME环境变量覆盖。
在驾驶动画中，绘制完成后应调用一次该函数。多次调用该函数将导致窗口中传递一个事件。
`QWindow`子类应重新实现`event()`，拦截事件并调用应用的渲染代码，然后调用基类实现。
注意：子类对`event()`的重新实现必须调用基类实现，除非它绝对确定该事件不需要由基类处理。例如，该函数的默认实现依赖于`QEvent::Timer`事件。因此，过滤掉它们会破坏更新事件的传递。

### `QSurfaceFormat QWindow::requestedFormat() const`

**作用与语义：**

返回该窗口请求的表面格式。
如果平台实现不支持请求格式，则请求格式将与实际窗口格式不同。
这是与`setFormat()`的值。

### `void QWindow::resize(const QSize &newSize)`

**作用与语义：**

将窗户大小设置为`newSize`。

### `void QWindow::resize(int w, int h)`

**作用与语义：**

将窗户尺寸设置为由宽度、`w`和高度构成的`QSize` `h`。
关于交互式调整窗口大小，请参见 `startSystemResize()`。

### `[virtual protected] void QWindow::resizeEvent(QResizeEvent *ev)`

**作用与语义：**

覆盖此功能以处理调整大小事件（`ev`）。
每当窗口在窗口系统中被调整大小时，都会调用缩小事件，无论是直接通过窗口系统确认`setGeometry()`或`resize()`请求，还是通过用户手动调整窗口大小间接触发。

### `[since 6.9] QMargins QWindow::safeAreaMargins() const`

**作用与语义：**

返回窗户的安全区域边缘。
安全区域代表了窗口中可以安全放置内容的部分，不会被其他UI元素（如系统UI）遮挡或冲突。
边距相对于窗口内部几何形状表示，即`QRect`（0， 0， `width()`， `height()`）。

**官方示例：**

```cpp
 void PaintDeviceWindow::paintEvent(QPaintEvent *)
 {
     QPainter painter(this);
     QRect rect(0, 0, width(), height());
     painter.fillRect(rect, QGradient::SunnyMorning);
     painter.fillRect(rect - safeAreaMargins(), QGradient::DustyGrass);
 }
```

### `[signal, since 6.9] void QWindow::safeAreaMarginsChanged(QMargins margins)`

**作用与语义：**

当安全区边界变为`margins`时，该信号会发出。

### `QScreen *QWindow::screen() const`

**作用与语义：**

返回显示窗口的屏幕，若无窗口则返回空。
对于子窗口，返回对应顶层窗口的屏幕。

### `[signal] void QWindow::screenChanged(QScreen *screen)`

**作用与语义：**

当窗口`screen`发生变化时，该信号会发出，无论是通过显式设置`setScreen()`，还是当窗口屏幕被移除时自动触发。

### `void QWindow::setBaseSize(const QSize &size)`

**作用与语义：**

设置窗户的底`size`。
如果窗口定义了`sizeIncrement()`，则使用基准大小来计算合适的窗口大小。

### `void QWindow::setCursor(const QCursor &cursor)`

**作用与语义：**

为该窗口设置光标形状。
鼠标`cursor`在该窗口上方时会呈现此形状，除非设置覆盖光标。请参阅预定义光标对象列表，了解一系列有用的形状。
如果没有设置光标，或者调用`unsetCursor()`后，则使用父窗口的光标。
默认情况下，光标是`Qt::ArrowCursor`形状。
有些底层窗口实现如果光标离开窗口，即使鼠标被抓取，光标也会重置。如果你想为所有窗口设置光标，即使窗口外，也可以考虑`QGuiApplication::setOverrideCursor()`。

### `void QWindow::setFilePath(const QString &filePath)`

**作用与语义：**

设置该窗口所代表的文件名。
窗口系统可能会使用`filePath`来显示该窗口在磁贴栏中所代表的文档路径。

### `void QWindow::setFlag(Qt::WindowType flag, bool on = true)`

**作用与语义：**

如果 `on`为真，则将窗口标志`flag`;否则清除该标志。

### `void QWindow::setFormat(const QSurfaceFormat &format)`

**作用与语义：**

设定窗户表面`format`。
格式决定了诸如颜色深度、透明度、深度和模板缓冲区大小等属性。例如，给窗口提供透明背景（前提是窗口系统支持合成，且窗口中其他内容不会再次使窗口再次不透明）：
曲面格式将在`create()`函数中解析。调用该函数后再调用`create()`不会重新解析本地曲面的曲面格式。
当格式未通过该函数显式设置时，将使用`QSurfaceFormat::defaultFormat()`返回的格式。这意味着当有多个窗口时，单个调用该函数可以被一个调用替换，然后再创建一个窗口`QSurfaceFormat::setDefaultFormat()`。

**官方示例：**

```cpp
 QSurfaceFormat format;
 format.setAlphaBufferSize(8);
 window.setFormat(format);
```

### `void QWindow::setFramePosition(const QPoint &point)`

**作用与语义：**

设置窗户（`point`）的左上角位置，包括窗框。
该位置相对于其屏幕的virtualGeometry()表示。

### `[slot] void QWindow::setGeometry(const QRect &rect)`

**作用与语义：**

将窗户的几何形状（窗框除外）设置为`rect`。
几何体与其屏幕的虚拟几何体（virtualGeometry()相关联。
注意：该槽位已超载。连接该槽位：


使用 qOverload 连接：
connect（sender， &SenderClass：：signal，。
window， qOverload（&QWindow：：setGeometry））;

或者用lambda作为包装器：
connect（sender， &SenderClass：：signal，。
window， [receiver = window]（const QRect &rect） { receiver->setGeometry（rect）; }）;


更多示例和方法，请参见连接超载槽位。

### `[slot] void QWindow::setGeometry(int posx, int posy, int w, int h)`

**作用与语义：**

将窗户的几何形状（不含窗框）设置为由`posx`、`posy`、`w`和`h`构成的矩形。
几何体与其屏幕的虚拟几何体（virtualGeometry()相关联。
注意：该槽位已超载。连接该槽位：


使用 qOverload 连接：
connect（sender， &SenderClass：：signal，。
window， qOverload（&QWindow：：setGeometry））;

或者用lambda作为包装器：
connect（sender， &SenderClass：：signal，。
窗口， [接收器 = 窗口]（int posx， int posy， int w， int h） { receiver->setGeometry（posx， posy， w， h）; }）;


更多示例和方法，请参见连接超载槽位。

### `void QWindow::setIcon(const QIcon &icon)`

**作用与语义：**

在窗口系统中设置窗口的 `icon`。
窗口图标可能被窗口系统用来装饰窗口，或者在任务切换器中使用。
注意：在macOS中，窗口标题栏图标用于表示文档的窗口，只有在设置了文件路径时才会显示。

### `bool QWindow::setKeyboardGrabEnabled(bool grab)`

**作用与语义：**

设置是否启用键盘抓取（`grab`）。
如果返回值为真，窗口会接收所有键事件，直到调用 setKeyboardGrabEnabled（false）;其他窗口则完全没有键事件。鼠标事件不受影响。如果你想抓取，可以用 `setMouseGrabEnabled()`。

### `void QWindow::setMask(const QRegion &region)`

**作用与语义：**

设置窗户的遮罩。
遮罩是向窗口系统发出的提示，表示应用程序不希望在给定`region`之外接收鼠标或触摸输入。
窗口管理器可以选择显示遮罩中未包含的窗口区域，因此应用程序负责清除遮罩以外的区域以实现透明。

### `void QWindow::setMaximumSize(const QSize &size)`

**作用与语义：**

设定窗口的最大大小。
这是给窗口管理器一个提示，防止调整大于指定`size`。

### `void QWindow::setMinimumSize(const QSize &size)`

**作用与语义：**

设定窗口的最小尺寸。
这是给窗口管理器一个提示，防止缩放低于指定`size`。

### `bool QWindow::setMouseGrabEnabled(bool grab)`

**作用与语义：**

设置是否启用鼠标抓取（`grab`）。
如果返回值为真，窗口会接收所有鼠标事件，直到调用 setMouseGrabEnabled（false）;其他窗口则完全没有鼠标事件。键盘事件不受影响。如果你想抓取，可以使用 `setKeyboardGrabEnabled()`。

### `void QWindow::setParent(QWindow *parent)`

**作用与语义：**

设置`parent`窗口。这会导致窗口系统管理窗口的剪辑，因此它会被剪辑到`parent`窗口。
将`parent`设置为`nullptr`会让窗口变成顶层窗口。
如果`parent`是`fromWinId()`创建的窗口，那么当前窗口会嵌入在`parent`中，前提是平台支持。

### `void QWindow::setPosition(const QPoint &pt)`

**作用与语义：**

将桌面窗口的位置设置为`pt`。
该位置相对于其屏幕的virtualGeometry()表示。
关于交互式移动窗口，请参见 `startSystemMove()`。关于交互式调整窗口大小，请参见 `startSystemResize()`。
注意：并非所有窗口系统都支持设置或查询顶层窗口位置。在此类系统中，程序移动窗口可能无效，且当前位置（如`QPoint(0, 0)`）可能会返回人工值。

### `void QWindow::setPosition(int posx, int posy)`

**作用与语义：**

把桌面窗口的位置设为`posx`，`posy`。
该位置相对于其屏幕的virtualGeometry()表示。

### `void QWindow::setScreen(QScreen *newScreen)`

**作用与语义：**

设置应显示窗口的屏幕。
如果窗口已经创建，它会在`newScreen`上重新创建。
注意：如果屏幕是多个屏幕组成的虚拟桌面的一部分，窗口不会自动移动到`newScreen`。要将窗口相对于屏幕放置，请使用屏幕的左上（TopLeft）位置。
这个功能只适用于顶层窗口。

### `void QWindow::setSizeIncrement(const QSize &size)`

**作用与语义：**

设置窗口的大小增量（`size`）。
当用户调整窗口大小时，尺寸会以`sizeIncrement()`为单位移动。`width()`水平像素和`sizeIncrement()`。`height()`像素垂直，`baseSize()`为基底。
默认情况下，该属性包含宽度和高度均为零的大小。
窗口系统可能不支持大小递增。

### `void QWindow::setSurfaceType(QSurface::SurfaceType surfaceType)`

**作用与语义：**

设定窗户的 `surfaceType`。
指定该窗口是用于带`QBackingStore`的栅格渲染，还是用于带`QOpenGLContext`的OpenGL渲染。
当`create()`函数创建原生曲面时，将使用该 `surfaceType`First 曲面。在创建原生曲面后调用该函数需要调用 `destroy()` 和 `create()` 来释放旧的原生曲面并创建新的。

### `void QWindow::setVulkanInstance(QVulkanInstance *instance)`

**作用与语义：**

将该窗口与指定的火神 `instance` 关联起来。
只要`QWindow`实例存在，`instance`就必须有效。

### `void QWindow::setWindowState(Qt::WindowState state)`

**作用与语义：**

设置窗口的屏幕占用状态。
窗口`state`表示窗口在窗口系统中是以最大化、最小、全屏还是正常状态出现。
枚举值`Qt::WindowActive`不是被接受的参数。

### `void QWindow::setWindowStates(Qt::WindowStates state)`

**作用与语义：**

设置窗口的屏幕占用状态。
窗口`state`表示该窗口在窗口系统中是否以最大化、最小化和/或全屏状态出现。
窗口可以处于多种状态的组合。例如，如果窗口既最小化又最大化，窗口会显示最小化，但点击任务栏条目后，窗口会恢复到最大化状态。
枚举值`Qt::WindowActive`不应被设置。

### `[slot] void QWindow::show()`

**作用与语义：**

可以看到窗户。
对于子窗口，这相当于调用`showNormal()`。否则，则相当于调用`showFullScreen()`、`showMaximized()`或`showNormal()`，具体取决于平台对窗口类型和标志的默认行为。

### `[virtual protected] void QWindow::showEvent(QShowEvent *ev)`

**作用与语义：**

覆盖此权限以处理展会事件（`ev`）。
当窗口请求显示时，调用该函数。
如果窗口系统成功显示窗口，随后会进行调整大小和曝光事件。

### `[slot] void QWindow::showFullScreen()`

**作用与语义：**

窗口显示为全屏。
等价于调用`setWindowStates`（`Qt::WindowFullScreen`）然后再调用`setVisible`（true）。
请参阅`QWidget::showFullScreen()`文档，了解平台特定的注意事项和限制。

### `[slot] void QWindow::showMaximized()`

**作用与语义：**

显示窗口是最大化的。
相当于调用`setWindowStates`（`Qt::WindowMaximized`）然后调用`setVisible`（true）。

### `[slot] void QWindow::showMinimized()`

**作用与语义：**

显示窗口已最小化。
等同于调用`setWindowStates`（`Qt::WindowMinimized`）然后再调用`setVisible`（true）。

### `[slot] void QWindow::showNormal()`

**作用与语义：**

显示窗口正常，即既未最大化、未最小化，也未全屏显示。
相当于先调用`setWindowStates`（`Qt::WindowNoState`）然后再调用`setVisible`（true）。

### `[override virtual] QSize QWindow::size() const`

**作用与语义：**

重实现自：`QSurface::size()` const.
返回窗户大小（不含任何窗框）。
返回表面的像素大小。

### `QSize QWindow::sizeIncrement() const`

**作用与语义：**

返回窗口的尺寸增量。

### `[slot] bool QWindow::startSystemMove()`

**作用与语义：**

启动系统特定的移动操作。
调用该操作会在支持该窗口的平台上启动交互式移动操作。实际行为可能因平台而异。通常，它会让窗口跟随鼠标光标移动，直到松开鼠标按钮。
在支持该功能的平台上，这种移动窗口的方法比`setPosition`更受青睐，因为它允许更原生地呈现移动窗口的外观和感觉，例如让窗口管理器将该窗口吸附到其他窗口，或者在拖动到屏幕边缘时通过动画进行特殊的平铺或调整大小。此外，在某些平台如Wayland上，`setPosition`不被支持，因此这是应用程序唯一能影响其位置的方式。
如果操作得到系统支持，则返回为真。

### `[slot] bool QWindow::startSystemResize(Qt::Edges edges)`

**作用与语义：**

启动系统特定的调整大小操作。
调用该操作会由支持该窗口的平台开始交互式的调整大小操作。实际行为可能因平台而异。通常，它会让窗口缩小使其边缘跟随鼠标光标。
在支持该方法的平台上，这种窗口大小调整方法比`setGeometry`更受青睐，因为它允许更原生的窗口大小调整，例如让窗口管理器将窗口与其他窗口吸附，或在拖动到屏幕边缘时通过动画实现特殊的大小调整行为。
`edges`应是单边，或两条相邻边（一个角）。不允许使用其他数值。
如果操作得到系统支持，则返回为真。

### `[override virtual] QSurface::SurfaceType QWindow::surfaceType() const`

**作用与语义：**

重实现自：`QSurface::surfaceType()` const.
返回窗口的表面类型。
返回表面类型。

### `[virtual protected] void QWindow::tabletEvent(QTabletEvent *ev)`

**作用与语义：**

通过覆盖该功能来处理平板按压、移动和释放事件（`ev`）。
近距离进入和离开事件不会发送到Windows，而是传递到应用实例。

### `[virtual protected] void QWindow::touchEvent(QTouchEvent *ev)`

**作用与语义：**

覆盖它以处理触摸事件（`ev`）。

### `Qt::WindowType QWindow::type() const`

**作用与语义：**

返回窗口类型。
这会返回表示窗口是对话框、提示、弹窗还是普通窗口等的部分。

### `void QWindow::unsetCursor()`

**作用与语义：**

恢复了该窗口的默认箭头光标。

### `QVulkanInstance *QWindow::vulkanInstance() const`

**作用与语义：**

如果设置了相关 Vulkan 实例，则返回;否则`nullptr`。

### `[virtual protected] void QWindow::wheelEvent(QWheelEvent *ev)`

**作用与语义：**

覆盖此功能以处理鼠标滚轮或其他滚轮事件（`ev`）。

### `WId QWindow::winId() const`

**作用与语义：**

返回窗口的平台ID。
注意：如果平台窗口尚未创建，该函数将使该函数被创建。如果平台窗口创建失败，返回 0。
对于该ID可能有用的平台，返回的值将唯一代表对应屏幕内的窗口。

### `Qt::WindowState QWindow::windowState() const`

**作用与语义：**

窗户的屏幕占用状态。

### `[signal] void QWindow::windowStateChanged(Qt::WindowState windowState)`

**作用与语义：**

当`windowState`发生变化时，该信号会通过显式设置`setWindowStates()`，或在用户点击标题栏按钮或其他方式时自动发出。

### `Qt::WindowStates QWindow::windowStates() const`

**作用与语义：**

窗户的屏幕占用状态。
窗口可以处于多种状态的组合。例如，如果窗口既最小化又最大化，窗口会显示最小化，但点击任务栏条目后，窗口会恢复到最大化状态。

### `Qt::ScreenOrientation contentOrientation() const`

**作用与语义：**

此属性保存窗口内容的方向。
这是对窗口管理器的提示，以防它需要显示额外内容，如弹出窗口、对话框、状态栏或类似内容，相对于窗口的位置。
推荐的方向是 `QScreen::orientation()`，但应用程序不必支持所有可能的方向，因此可以选择忽略当前屏幕方向。
窗口与内容方向之间的差异决定了需要旋转内容的角度。`QScreen::angleBetween()`、`QScreen::transformBetween()` 和 `QScreen::mapBetween()` 可用于计算必要的变换。
默认值为 `Qt::PrimaryOrientation`。

**如何使用：** 调用 `contentOrientation()` 读取当前值；它不会修改应用状态。

### `Qt::WindowFlags flags() const`

**作用与语义：**

该属性保留窗户的标志。
窗口标志控制窗口在窗口系统中的外观，无论是对话框、弹窗还是普通窗口，以及是否应该有标题栏等。
如果请求的标志无法满足，实际的窗口标志可能与 setFlags() 设置的标志不同。

**如何使用：** 调用 `flags()` 读取当前值；它不会修改应用状态。

### `int height() const`

**作用与语义：**

该属性表示窗口几何形状的高度。

**如何使用：** 调用 `height()` 读取当前值；它不会修改应用状态。

### `bool isVisible() const`

**作用与语义：**

无论窗户是否可见，这一属性都成立。
该属性控制窗口在窗口系统中的可见性。
默认情况下，窗口不可见，你必须调用 setVisible（true）、`show()` 或类似的命令才能显示。
注意：隐藏窗口不会将该窗口从窗口系统中移除，只是隐藏它。在为全屏应用程序提供专用桌面的窗口系统（如macOS）中，隐藏全屏窗口不会移除该桌面，但保持空白。同一应用程序中的另一个窗口可能会显示全屏，并填满该桌面。使用`QWindow::close`完全移除窗口系统中的窗口。

**如何使用：** 调用 `isVisible()` 读取当前值；它不会修改应用状态。

### `int maximumHeight() const`

**作用与语义：**

该属性表示了窗口几何的最大高度。

**如何使用：** 调用 `maximumHeight()` 读取当前值；它不会修改应用状态。

### `int maximumWidth() const`

**作用与语义：**

该属性表示了窗口几何的最大宽度。

**如何使用：** 调用 `maximumWidth()` 读取当前值；它不会修改应用状态。

### `int minimumHeight() const`

**作用与语义：**

该属性表示了窗口几何形状的最小高度。

**如何使用：** 调用 `minimumHeight()` 读取当前值；它不会修改应用状态。

### `int minimumWidth() const`

**作用与语义：**

该属性表示窗口几何形状的最小宽度。

**如何使用：** 调用 `minimumWidth()` 读取当前值；它不会修改应用状态。

### `Qt::WindowModality modality() const`

**作用与语义：**

该属性表示窗口的模态性。
模态窗口防止其他窗口接收输入事件。Qt 支持两种模态：`Qt::WindowModal` 和 `Qt::ApplicationModal`。
默认情况下，该属性为`Qt::NonModal`。

**如何使用：** 调用 `modality()` 读取当前值；它不会修改应用状态。

### `qreal opacity() const`

**作用与语义：**

该属性决定了窗口系统中窗口的不透明度。
如果窗口系统支持窗口不透明度，可以用来淡入和淡出窗口，或使其半透明。
1.0及以上的数值被视为完全不透明，而0.0及以下的数值则被视为完全透明。介于两者的值代表两极之间的不同透明度水平。
默认值是1.0。

**如何使用：** 调用 `opacity()` 读取当前值；它不会修改应用状态。

### `void reportContentOrientationChange(Qt::ScreenOrientation orientation)`

**作用与语义：**

此属性保存窗口内容的方向。
这是对窗口管理器的提示，以防它需要显示额外内容，如弹出窗口、对话框、状态栏或类似内容，相对于窗口的位置。
推荐的方向是 `QScreen::orientation()`，但应用程序不必支持所有可能的方向，因此可以选择忽略当前屏幕方向。
窗口与内容方向之间的差异决定了需要旋转内容的角度。`QScreen::angleBetween()`、`QScreen::transformBetween()` 和 `QScreen::mapBetween()` 可用于计算必要的变换。
默认值为 `Qt::PrimaryOrientation`。

**如何使用：** 调用 `reportContentOrientationChange()` 读取当前值；它不会修改应用状态。

### `void setFlags(Qt::WindowFlags flags)`

**作用与语义：**

该属性保留窗户的标志。
窗口标志控制窗口在窗口系统中的外观，无论是对话框、弹窗还是普通窗口，以及是否应该有标题栏等。
如果请求的标志无法满足，实际的窗口标志可能与 setFlags() 设置的标志不同。

**如何使用：** 调用 `setFlags(...)` 修改 `flags`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setModality(Qt::WindowModality modality)`

**作用与语义：**

该属性表示窗口的模态性。
模态窗口防止其他窗口接收输入事件。Qt 支持两种模态：`Qt::WindowModal` 和 `Qt::ApplicationModal`。
默认情况下，该属性为`Qt::NonModal`。

**如何使用：** 调用 `setModality(...)` 修改 `modality`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setOpacity(qreal level)`

**作用与语义：**

该属性决定了窗口系统中窗口的不透明度。
如果窗口系统支持窗口不透明度，可以用来淡入和淡出窗口，或使其半透明。
1.0及以上的数值被视为完全不透明，而0.0及以下的数值则被视为完全透明。介于两者的值代表两极之间的不同透明度水平。
默认值是1.0。

**如何使用：** 调用 `setOpacity(...)` 修改 `opacity`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTransientParent(QWindow *parent)`

**作用与语义：**

该属性包含该窗口作为瞬态弹出窗口的窗口。
这向窗口管理器提示该窗口是代表瞬态父窗口的对话框或弹窗。
为了使窗口默认置中于其瞬态`parent`之上，根据窗口管理器的不同，可能需要调用合适的`Qt::WindowType`（如`Qt::Dialog`）的`setFlags()`。

**如何使用：** 调用 `setTransientParent(...)` 修改 `transientParent`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setVisibility(QWindow::Visibility v)`

**作用与语义：**

该属性表示窗户的屏幕占用状态。
可见性是指窗口应以正常、最小化、最大化、全屏还是隐藏显示。
要将可见性设置为`AutomaticVisibility`意味着给窗口一个默认可见状态，这取决于平台，可能是全屏或窗口状态。读取可见性属性时，你总是得到实际状态，永远不会`AutomaticVisibility`。
默认值为隐藏。

**如何使用：** 调用 `setVisibility(...)` 修改 `visibility`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QString title() const`

**作用与语义：**

该属性在窗口系统中保留了窗口的标题。
窗口标题可能出现在窗口装饰的标题区域，具体取决于窗口系统和窗口标志。窗口系统也可能用它来识别其他上下文中的窗口，比如任务切换器中。

**如何使用：** 调用 `title()` 读取当前值；它不会修改应用状态。

### `QWindow * transientParent() const`

**作用与语义：**

该属性包含该窗口作为瞬态弹出窗口的窗口。
这向窗口管理器提示该窗口是代表瞬态父窗口的对话框或弹窗。
为了使窗口默认置中于其瞬态`parent`之上，根据窗口管理器的不同，可能需要调用合适的`Qt::WindowType`（如`Qt::Dialog`）的`setFlags()`。

**如何使用：** 调用 `transientParent()` 读取当前值；它不会修改应用状态。

### `QWindow::Visibility visibility() const`

**作用与语义：**

该属性表示窗户的屏幕占用状态。
可见性是指窗口应以正常、最小化、最大化、全屏还是隐藏显示。
要将可见性设置为`AutomaticVisibility`意味着给窗口一个默认可见状态，这取决于平台，可能是全屏或窗口状态。读取可见性属性时，你总是得到实际状态，永远不会`AutomaticVisibility`。
默认值为隐藏。

**如何使用：** 调用 `visibility()` 读取当前值；它不会修改应用状态。

### `int width() const`

**作用与语义：**

该属性表示窗口几何形状的宽度。

**如何使用：** 调用 `width()` 读取当前值；它不会修改应用状态。

### `int x() const`

**作用与语义：**

该属性表示窗口几何形状的 x 位置。

**如何使用：** 调用 `x()` 读取当前值；它不会修改应用状态。

### `int y() const`

**作用与语义：**

该属性表示窗口几何形状的 y 位置。

**如何使用：** 调用 `y()` 读取当前值；它不会修改应用状态。

### `void setHeight(int arg)`

**作用与语义：**

该属性表示窗口几何形状的高度。

**如何使用：** 调用 `setHeight(...)` 修改 `height`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMaximumHeight(int h)`

**作用与语义：**

该属性表示了窗口几何的最大高度。

**如何使用：** 调用 `setMaximumHeight(...)` 修改 `maximumHeight`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMaximumWidth(int w)`

**作用与语义：**

该属性表示了窗口几何的最大宽度。

**如何使用：** 调用 `setMaximumWidth(...)` 修改 `maximumWidth`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMinimumHeight(int h)`

**作用与语义：**

该属性表示了窗口几何形状的最小高度。

**如何使用：** 调用 `setMinimumHeight(...)` 修改 `minimumHeight`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMinimumWidth(int w)`

**作用与语义：**

该属性表示窗口几何形状的最小宽度。

**如何使用：** 调用 `setMinimumWidth(...)` 修改 `minimumWidth`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTitle(const QString &)`

**作用与语义：**

该属性在窗口系统中保留了窗口的标题。
窗口标题可能出现在窗口装饰的标题区域，具体取决于窗口系统和窗口标志。窗口系统也可能用它来识别其他上下文中的窗口，比如任务切换器中。

**如何使用：** 调用 `setTitle(...)` 修改 `title`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setVisible(bool visible)`

**作用与语义：**

无论窗户是否可见，这一属性都成立。
该属性控制窗口在窗口系统中的可见性。
默认情况下，窗口不可见，你必须调用 setVisible（true）、`show()` 或类似的命令才能显示。
注意：隐藏窗口不会将该窗口从窗口系统中移除，只是隐藏它。在为全屏应用程序提供专用桌面的窗口系统（如macOS）中，隐藏全屏窗口不会移除该桌面，但保持空白。同一应用程序中的另一个窗口可能会显示全屏，并填满该桌面。使用`QWindow::close`完全移除窗口系统中的窗口。

**如何使用：** 调用 `setVisible(...)` 修改 `visible`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setWidth(int arg)`

**作用与语义：**

该属性表示窗口几何形状的宽度。

**如何使用：** 调用 `setWidth(...)` 修改 `width`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setX(int arg)`

**作用与语义：**

该属性表示窗口几何形状的 x 位置。

**如何使用：** 调用 `setX(...)` 修改 `x`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setY(int arg)`

**作用与语义：**

该属性表示窗口几何形状的 y 位置。

**如何使用：** 调用 `setY(...)` 修改 `y`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void activeChanged()`

**作用与语义：**

该属性表示窗口的活跃状态。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `active` 的变化，不要把它当作普通函数主动调用。

### `void contentOrientationChanged(Qt::ScreenOrientation orientation)`

**作用与语义：**

此属性保存窗口内容的方向。
这是对窗口管理器的提示，以防它需要显示额外内容，如弹出窗口、对话框、状态栏或类似内容，相对于窗口的位置。
推荐的方向是 `QScreen::orientation()`，但应用程序不必支持所有可能的方向，因此可以选择忽略当前屏幕方向。
窗口与内容方向之间的差异决定了需要旋转内容的角度。`QScreen::angleBetween()`、`QScreen::transformBetween()` 和 `QScreen::mapBetween()` 可用于计算必要的变换。
默认值为 `Qt::PrimaryOrientation`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `contentOrientation` 的变化，不要把它当作普通函数主动调用。

### `void flagsChanged(Qt::WindowFlags flags)`

**作用与语义：**

该属性保留窗户的标志。
窗口标志控制窗口在窗口系统中的外观，无论是对话框、弹窗还是普通窗口，以及是否应该有标题栏等。
如果请求的标志无法满足，实际的窗口标志可能与 setFlags() 设置的标志不同。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `flags` 的变化，不要把它当作普通函数主动调用。

### `void heightChanged(int arg)`

**作用与语义：**

该属性表示窗口几何形状的高度。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `height` 的变化，不要把它当作普通函数主动调用。

### `void maximumHeightChanged(int arg)`

**作用与语义：**

该属性表示了窗口几何的最大高度。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `maximumHeight` 的变化，不要把它当作普通函数主动调用。

### `void maximumWidthChanged(int arg)`

**作用与语义：**

该属性表示了窗口几何的最大宽度。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `maximumWidth` 的变化，不要把它当作普通函数主动调用。

### `void minimumHeightChanged(int arg)`

**作用与语义：**

该属性表示了窗口几何形状的最小高度。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `minimumHeight` 的变化，不要把它当作普通函数主动调用。

### `void minimumWidthChanged(int arg)`

**作用与语义：**

该属性表示窗口几何形状的最小宽度。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `minimumWidth` 的变化，不要把它当作普通函数主动调用。

### `void opacityChanged(qreal opacity)`

**作用与语义：**

该属性决定了窗口系统中窗口的不透明度。
如果窗口系统支持窗口不透明度，可以用来淡入和淡出窗口，或使其半透明。
1.0及以上的数值被视为完全不透明，而0.0及以下的数值则被视为完全透明。介于两者的值代表两极之间的不同透明度水平。
默认值是1.0。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `opacity` 的变化，不要把它当作普通函数主动调用。

### `void transientParentChanged(QWindow *transientParent)`

**作用与语义：**

该属性包含该窗口作为瞬态弹出窗口的窗口。
这向窗口管理器提示该窗口是代表瞬态父窗口的对话框或弹窗。
为了使窗口默认置中于其瞬态`parent`之上，根据窗口管理器的不同，可能需要调用合适的`Qt::WindowType`（如`Qt::Dialog`）的`setFlags()`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `transientParent` 的变化，不要把它当作普通函数主动调用。

### `void visibilityChanged(QWindow::Visibility visibility)`

**作用与语义：**

该属性表示窗户的屏幕占用状态。
可见性是指窗口应以正常、最小化、最大化、全屏还是隐藏显示。
要将可见性设置为`AutomaticVisibility`意味着给窗口一个默认可见状态，这取决于平台，可能是全屏或窗口状态。读取可见性属性时，你总是得到实际状态，永远不会`AutomaticVisibility`。
默认值为隐藏。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `visibility` 的变化，不要把它当作普通函数主动调用。

### `void visibleChanged(bool arg)`

**作用与语义：**

无论窗户是否可见，这一属性都成立。
该属性控制窗口在窗口系统中的可见性。
默认情况下，窗口不可见，你必须调用 setVisible（true）、`show()` 或类似的命令才能显示。
注意：隐藏窗口不会将该窗口从窗口系统中移除，只是隐藏它。在为全屏应用程序提供专用桌面的窗口系统（如macOS）中，隐藏全屏窗口不会移除该桌面，但保持空白。同一应用程序中的另一个窗口可能会显示全屏，并填满该桌面。使用`QWindow::close`完全移除窗口系统中的窗口。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `visible` 的变化，不要把它当作普通函数主动调用。

### `void widthChanged(int arg)`

**作用与语义：**

该属性表示窗口几何形状的宽度。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `width` 的变化，不要把它当作普通函数主动调用。

### `void windowTitleChanged(const QString &title)`

**作用与语义：**

该属性在窗口系统中保留了窗口的标题。
窗口标题可能出现在窗口装饰的标题区域，具体取决于窗口系统和窗口标志。窗口系统也可能用它来识别其他上下文中的窗口，比如任务切换器中。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `title` 的变化，不要把它当作普通函数主动调用。

### `void xChanged(int arg)`

**作用与语义：**

该属性表示窗口几何形状的 x 位置。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `x` 的变化，不要把它当作普通函数主动调用。

### `void yChanged(int arg)`

**作用与语义：**

该属性表示窗口几何形状的 y 位置。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `y` 的变化，不要把它当作普通函数主动调用。

## 6. 深入实践与常见坑

### 生命周期和资源边界

控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

### 状态和错误边界

控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

### 线程边界

所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

### 最容易出现的错误

不要用固定坐标拼接响应式界面；不要给已经加入布局的控件反复 `setGeometry()`；不要在 `paintEvent()` 中修改业务状态；不要忘记窗口关闭、对象销毁和应用退出是三个不同事件。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QWindow` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
