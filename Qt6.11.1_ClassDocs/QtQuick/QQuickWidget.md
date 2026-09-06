# QQuickWidget

> Qt 6.11.1 · Qt Quick

## 1. 先建立直觉

**一句话定位：** `QQuickWidget` 是 QML 属性绑定与场景图机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Quick 面向 QML/场景图界面，提供可视项、动画、输入和高性能界面基础设施。

### 这是什么

`QQuickWidget` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QQuickWidget>`
- 继承自：QWidget
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS QuickWidgets)
target_link_libraries(mytarget PRIVATE Qt6::QuickWidgets)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

### 状态、生命周期和线程

**生命周期：** QML 引擎、上下文和对象所有权必须明确。由 QML 创建的对象通常由引擎管理；通过 context property 或 C++ 暴露的对象要决定由 C++ 持有还是转移给 QML，不能让绑定指向悬空对象。

**状态与结果：** 属性绑定和直接赋值不是一回事：直接给被绑定属性赋值通常会打破原有绑定。C++ 属性要有正确的 notify signal，QML 才能在数据变化时更新；信号参数和属性当前值要保持一致。

**线程与事件循环：** 大多数 QML 对象和 GUI 操作在 GUI 线程，场景图渲染还可能在 render thread。不要在渲染阶段调用 GUI 对象 API；后台数据通过线程安全的信号/槽边界送入 QML。

## 3. 直接使用

需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。 使用时通常按这个过程组织：创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

```cpp
// C++ 侧暴露属性/信号后，在 QML 中建立绑定。
// 变化时发出 notify signal，避免在绑定表达式中直接修改状态。
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum ResizeMode { SizeViewToRootObject, SizeRootObjectToView }`
- `enum Status { Null, Ready, Loading, Error }`

### 属性

- `resizeMode : ResizeMode`
- `source : QUrl`
- `status : Status`

### 公有函数

- `QQuickWidget(QWidget *parent = nullptr)`
- `QQuickWidget(QQmlEngine *engine, QWidget *parent)`
- `QQuickWidget(const QUrl &source, QWidget *parent = nullptr)`
- `(since 6.9) QQuickWidget(QAnyStringView uri, QAnyStringView typeName, QWidget *parent = nullptr)`
- `virtual ~QQuickWidget() override`
- `QQmlEngine * engine() const`
- `QList<QQmlError> errors() const`
- `QSurfaceFormat format() const`
- `QImage grabFramebuffer() const`
- `QSize initialSize() const`
- `QQuickWindow * quickWindow() const`
- `QQuickWidget::ResizeMode resizeMode() const`
- `QQmlContext * rootContext() const`
- `QQuickItem * rootObject() const`
- `void setClearColor(const QColor &color)`
- `void setFormat(const QSurfaceFormat &format)`
- `void setResizeMode(QQuickWidget::ResizeMode)`
- `QUrl source() const`
- `QQuickWidget::Status status() const`

### 公有槽函数

- `(since 6.9) void loadFromModule(QAnyStringView uri, QAnyStringView typeName)`
- `(since 6.9) void setInitialProperties(const QVariantMap &initialProperties)`
- `void setSource(const QUrl &url)`

### 信号

- `void sceneGraphError(QQuickWindow::SceneGraphError error, const QString &message)`
- `void statusChanged(QQuickWidget::Status status)`

### 重实现的保护函数

- `virtual void dragEnterEvent(QDragEnterEvent *e) override`
- `virtual void dragLeaveEvent(QDragLeaveEvent *e) override`
- `virtual void dragMoveEvent(QDragMoveEvent *e) override`
- `virtual void dropEvent(QDropEvent *e) override`
- `virtual bool event(QEvent *e) override`
- `virtual void focusInEvent(QFocusEvent *event) override`
- `virtual bool focusNextPrevChild(bool next) override`
- `virtual void focusOutEvent(QFocusEvent *event) override`
- `virtual void hideEvent(QHideEvent *) override`
- `virtual void keyPressEvent(QKeyEvent *e) override`
- `virtual void keyReleaseEvent(QKeyEvent *e) override`
- `virtual void mouseDoubleClickEvent(QMouseEvent *e) override`
- `virtual void mouseMoveEvent(QMouseEvent *e) override`
- `virtual void mousePressEvent(QMouseEvent *e) override`
- `virtual void mouseReleaseEvent(QMouseEvent *e) override`
- `virtual void paintEvent(QPaintEvent *event) override`
- `virtual void showEvent(QShowEvent *) override`
- `virtual void wheelEvent(QWheelEvent *e) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QQuickWidget::ResizeMode`

**作用与语义：**

该枚举规定了如何调整视图大小。
- `QQuickWidget::SizeViewToRootObject`：`0`;视图在QML中以根项进行调整大小。
- `QQuickWidget::SizeRootObjectToView`：`1`;视图会自动将根元素调整为视图大小。

### `enum QQuickWidget::Status`

**作用与语义：**

指定`QQuickWidget`的加载状态。
- `QQuickWidget::Null`：`0`;本`QQuickWidget`没有源集。
- `QQuickWidget::Ready`：`1`;该`QQuickWidget`已加载并创建了QML组件。
- `QQuickWidget::Loading`：`2`;该`QQuickWidget`正在加载网络数据。
- `QQuickWidget::Error`：`3`;发生一个或多个错误。调用`errors()`以获取错误列表。

### `resizeMode : ResizeMode`

**作用与语义：**

决定视图是否应该调整窗口内容大小。
如果该属性设置为`SizeViewToRootObject`（默认），视图会调整大小为QML根项的大小。
如果该属性设置为`SizeRootObjectToView`，视图会自动将根项调整到视图大小。
无论如何，视图的 sizeHint 都是根项的初始大小。但请注意，由于 QML 可能动态加载，大小可能会变化。

**如何使用：** 调用 `resizeMode()` 读取当前值；它不会修改应用状态。

### `source : QUrl`

**作用与语义：**

该属性包含QML组件源的URL。
确保提供的URL完整且正确，特别是在从本地文件系统加载文件时使用`QUrl::fromLocalFile()`。
注意：设置源 URL 会导致 QML 组件实例化，即使 URL 与当前值保持不变。

**如何使用：** 调用 `source()` 读取当前值；它不会修改应用状态。

### `[read-only] status : Status`

**作用与语义：**

该组件当前的 `status`。

**如何使用：** 调用 `status()` 读取当前值；它不会修改应用状态。

### `[explicit] QQuickWidget::QQuickWidget(QWidget *parent = nullptr)`

**作用与语义：**

构建一个带有默认QML引擎的QQuickWidget，作为`parent`的子节点。
`parent`的默认值是`nullptr`。

### `QQuickWidget::QQuickWidget(QQmlEngine *engine, QWidget *parent)`

**作用与语义：**

构造一个QQuickWidget，`engine`为`parent`的子节点。
注意：QQuickWidget 不拥有给定的 `engine` 对象;销毁引擎是调用者的责任。如果在视图出现前删除`engine`，`status()` 将返回 `QQuickWidget::Error`。

### `[explicit] QQuickWidget::QQuickWidget(const QUrl &source, QWidget *parent = nullptr)`

**作用与语义：**

构建一个带有默认QML引擎的QQuickWidget，并作为`parent`的子节点`source`给定的QML。
`parent`的默认值是`nullptr`。

### `[explicit, since 6.9] QQuickWidget::QQuickWidget(QAnyStringView uri, QAnyStringView typeName, QWidget *parent = nullptr)`

**作用与语义：**

构造一个QQuickWidget，包含由`uri`和`typeName`指定的元素，以及父`parent`。`parent`的默认值是`nullptr`。

### `[override virtual noexcept] QQuickWidget::~QQuickWidget()`

**作用与语义：**

摧毁了`QQuickWidget`。

### `[override virtual protected] void QQuickWidget::dragEnterEvent(QDragEnterEvent *e)`

**作用与语义：**

重实现自：`QWidget::dragEnterEvent`（QDragEnterEvent *event）。

### `[override virtual protected] void QQuickWidget::dragLeaveEvent(QDragLeaveEvent *e)`

**作用与语义：**

重实现自：`QWidget::dragLeaveEvent`（QDragLeaveEvent *event）。

### `[override virtual protected] void QQuickWidget::dragMoveEvent(QDragMoveEvent *e)`

**作用与语义：**

重实现自：`QWidget::dragMoveEvent`（QDragMoveEvent *event）。

### `[override virtual protected] void QQuickWidget::dropEvent(QDropEvent *e)`

**作用与语义：**

重实现自：`QWidget::dropEvent`（QDropEvent *event）。

### `QQmlEngine *QQuickWidget::engine() const`

**作用与语义：**

返回用于实例化QML组件的`QQmlEngine`指针。

### `QList<QQmlError> QQuickWidget::errors() const`

**作用与语义：**

返回上次编译或创建操作中发生的错误列表。当状态未`Error`时，返回一个空列表。

### `[override virtual protected] bool QQuickWidget::event(QEvent *e)`

**作用与语义：**

重实现自：`QWidget::event`（QEvent *事件）。

### `[override virtual protected] void QQuickWidget::focusInEvent(QFocusEvent *event)`

**作用与语义：**

重实现自：`QWidget::focusInEvent`（QFocusEvent *事件）。

### `[override virtual protected] bool QQuickWidget::focusNextPrevChild(bool next)`

**作用与语义：**

重装：`QWidget::focusNextPrevChild`（下一个布尔）。

### `[override virtual protected] void QQuickWidget::focusOutEvent(QFocusEvent *event)`

**作用与语义：**

重实现自：`QWidget::focusOutEvent`（QFocusEvent *event）。

### `QSurfaceFormat QQuickWidget::format() const`

**作用与语义：**

返回实际的表面格式。
如果小部件尚未显示，则返回请求的格式。

### `QImage QQuickWidget::grabFramebuffer() const`

**作用与语义：**

渲染一帧并读取成图像。
注意：这是一项可能昂贵的操作。

### `[override virtual protected] void QQuickWidget::hideEvent(QHideEvent *)`

**作用与语义：**

重实现自：`QWidget::hideEvent`（QHideEvent *event）。

### `QSize QQuickWidget::initialSize() const`

**作用与语义：**

返回根对象的初始大小。
如果`resizeMode` `SizeRootObjectToView`，根对象将被调整为视图大小。该函数返回根对象在调整大小前的大小。

### `[override virtual protected] void QQuickWidget::keyPressEvent(QKeyEvent *e)`

**作用与语义：**

重实现自：`QWidget::keyPressEvent`（QKeyEvent *event）。

### `[override virtual protected] void QQuickWidget::keyReleaseEvent(QKeyEvent *e)`

**作用与语义：**

重实现自：`QWidget::keyReleaseEvent`（QKeyEvent *event）。

### `[slot, since 6.9] void QQuickWidget::loadFromModule(QAnyStringView uri, QAnyStringView typeName)`

**作用与语义：**

加载由`uri`和`typeName`标识的QML组件。如果组件有QML文件支持，`source`会相应设置。对于`C++`中定义的类型，`source`为空。
如果在调用该方法之前设置了任何`source`，则该方法将被清除。
用相同的`uri`和`typeName`多次调用该方法，会导致QML组件被重新实例化。

### `[override virtual protected] void QQuickWidget::mouseDoubleClickEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QWidget::mouseDoubleClickEvent`（QMouseEvent *event）。

### `[override virtual protected] void QQuickWidget::mouseMoveEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QWidget::mouseMoveEvent`（QMouseEvent *event）。

### `[override virtual protected] void QQuickWidget::mousePressEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QWidget::mousePressEvent`（QMouseEvent *event）。

### `[override virtual protected] void QQuickWidget::mouseReleaseEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QWidget::mouseReleaseEvent`（QMouseEvent *event）。

### `[override virtual protected] void QQuickWidget::paintEvent(QPaintEvent *event)`

**作用与语义：**

重实现自：`QWidget::paintEvent`（QPaintEvent *event）。

### `QQuickWindow *QQuickWidget::quickWindow() const`

**作用与语义：**

返回该控件用于驱动 Qt Quick 渲染的屏幕外`QQuickWindow`。如果你想使用目前未被 `QQuickWidget` 暴露的 `QQuickWindow` API，例如连接 `QQuickWindow::beforeRendering()` 信号以在 Qt Quick 自身渲染下方绘制原生 OpenGL 内容，这非常有用。
警告：使用该函数的返回值请谨慎。特别是，切勿尝试展示`QQuickWindow`，使用其他仅支持`QWindow`的 API 时务必非常小心。
警告：在`QQuickWidget`的生命周期内，尤其是当小部件被移动到其他`QQuickWindow`时，屏幕外窗口可能会被删除（并重新创建）。如果你需要知道窗口何时被替换，请连接到其`destroyed()`信号。

### `QQmlContext *QQuickWidget::rootContext() const`

**作用与语义：**

该函数返回上下文层级的根节点。每个QML组件实例化在`QQmlContext`中。`QQmlContext`对于将数据传递给QML组件至关重要。在QML中，上下文按层级排列，该层级由`QQmlEngine`管理。

### `QQuickItem *QQuickWidget::rootObject() const`

**作用与语义：**

返回视图的根 `item`。当 `setSource()` 未被调用、调用时带有损坏的 `QtQuick` 代码，或根项未定义时，可以被 `nullptr`。

### `[signal] void QQuickWidget::sceneGraphError(QQuickWindow::SceneGraphError error, const QString &message)`

**作用与语义：**

当场景图初始化过程中出现`error`时，该信号会发出。
如果应用程序希望以自定义方式处理错误，比如OpenGL上下文创建失败，应连接到该信号。当没有槽函数连接到信号时，行为会不同：快速会打印`message`，或显示消息框，然后终止应用程序。
该信号将从图形界面线程中发出。

### `void QQuickWidget::setClearColor(const QColor &color)`

**作用与语义：**

设置透明的`color`。默认情况下，这是不透明的颜色。
要获得半透明`QQuickWidget`，调用该函数，将`color`设为`Qt::transparent`，在顶层窗口设置`Qt::WA_TranslucentBackground`小部件属性，并通过 `setFormat()` 请求 alpha 通道。

### `void QQuickWidget::setFormat(const QSurfaceFormat &format)`

**作用与语义：**

为该小部件所使用的上下文和屏幕外表面设置表面`format`。
当需要请求某个 OpenGL 版本或配置文件的上下文时，调用此函数。深度、模板和 alpha 缓冲区的大小会自动处理，无需显式请求。

### `[slot, since 6.9] void QQuickWidget::setInitialProperties(const QVariantMap &initialProperties)`

**作用与语义：**

设置调用`QQuickWidget::setSource()`后初始化QML组件的初始属性`initialProperties`。
注意：你只能用这个函数初始化顶层属性。
注意：该函数应始终在`setSource`之前调用，因为组件变`Ready`后该函数无效。

### `[slot] void QQuickWidget::setSource(const QUrl &url)`

**作用与语义：**

该属性包含QML组件源的URL。
确保提供的URL完整且正确，特别是在从本地文件系统加载文件时使用`QUrl::fromLocalFile()`。
注意：设置源 URL 会导致 QML 组件实例化，即使 URL 与当前值保持不变。

**如何使用：** 调用 `setSource(...)` 修改 `source`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `[override virtual protected] void QQuickWidget::showEvent(QShowEvent *)`

**作用与语义：**

重实现自：`QWidget::showEvent`（QShowEvent *event）。

### `QUrl QQuickWidget::source() const`

**作用与语义：**

如果设置了，返回源 URL。
注意：属性来源的获取函数。

### `[signal] void QQuickWidget::statusChanged(QQuickWidget::Status status)`

**作用与语义：**

该组件当前的 `status`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `status` 的变化，不要把它当作普通函数主动调用。

### `[override virtual protected] void QQuickWidget::wheelEvent(QWheelEvent *e)`

**作用与语义：**

重实现自：`QWidget::wheelEvent`（QWheelEvent *event）。

### `QQuickWidget::ResizeMode resizeMode() const`

**作用与语义：**

决定视图是否应该调整窗口内容大小。
如果该属性设置为`SizeViewToRootObject`（默认），视图会调整大小为QML根项的大小。
如果该属性设置为`SizeRootObjectToView`，视图会自动将根项调整到视图大小。
无论如何，视图的 sizeHint 都是根项的初始大小。但请注意，由于 QML 可能动态加载，大小可能会变化。

**如何使用：** 调用 `resizeMode()` 读取当前值；它不会修改应用状态。

### `void setResizeMode(QQuickWidget::ResizeMode)`

**作用与语义：**

决定视图是否应该调整窗口内容大小。
如果该属性设置为`SizeViewToRootObject`（默认），视图会调整大小为QML根项的大小。
如果该属性设置为`SizeRootObjectToView`，视图会自动将根项调整到视图大小。
无论如何，视图的 sizeHint 都是根项的初始大小。但请注意，由于 QML 可能动态加载，大小可能会变化。

**如何使用：** 调用 `setResizeMode(...)` 修改 `resizeMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QQuickWidget::Status status() const`

**作用与语义：**

该组件当前的 `status`。

**如何使用：** 调用 `status()` 读取当前值；它不会修改应用状态。

## 6. 深入实践与常见坑

### 生命周期和资源边界

QML 引擎、上下文和对象所有权必须明确。由 QML 创建的对象通常由引擎管理；通过 context property 或 C++ 暴露的对象要决定由 C++ 持有还是转移给 QML，不能让绑定指向悬空对象。

### 状态和错误边界

属性绑定和直接赋值不是一回事：直接给被绑定属性赋值通常会打破原有绑定。C++ 属性要有正确的 notify signal，QML 才能在数据变化时更新；信号参数和属性当前值要保持一致。

### 线程边界

大多数 QML 对象和 GUI 操作在 GUI 线程，场景图渲染还可能在 render thread。不要在渲染阶段调用 GUI 对象 API；后台数据通过线程安全的信号/槽边界送入 QML。

### 最容易出现的错误

优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QQuickWidget` 所属机制类型：QML 属性绑定与场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
