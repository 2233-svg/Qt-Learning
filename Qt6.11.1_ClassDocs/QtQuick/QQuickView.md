# QQuickView

> Qt 6.11.1 · Qt Quick

## 1. 先建立直觉

**一句话定位：** `QQuickView` 是 QML 属性绑定与场景图机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Quick 面向 QML/场景图界面，提供可视项、动画、输入和高性能界面基础设施。

### 这是什么

`QQuickView` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QQuickView>`
- 继承自：QQuickWindow
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Quick)
target_link_libraries(mytarget PRIVATE Qt6::Quick)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

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

- `QQuickView(QWindow *parent = nullptr)`
- `QQuickView(QQmlEngine *engine, QWindow *parent)`
- `QQuickView(const QUrl &source, QWindow *parent = nullptr)`
- `(since 6.7) QQuickView(QAnyStringView uri, QAnyStringView typeName, QWindow *parent = nullptr)`
- `virtual ~QQuickView() override`
- `QQmlEngine * engine() const`
- `QList<QQmlError> errors() const`
- `QSize initialSize() const`
- `QQuickView::ResizeMode resizeMode() const`
- `QQmlContext * rootContext() const`
- `QQuickItem * rootObject() const`
- `void setResizeMode(QQuickView::ResizeMode)`
- `QUrl source() const`
- `QQuickView::Status status() const`

### 公有槽函数

- `(since 6.7) void loadFromModule(QAnyStringView uri, QAnyStringView typeName)`
- `void setInitialProperties(const QVariantMap &initialProperties)`
- `void setSource(const QUrl &url)`

### 信号

- `void statusChanged(QQuickView::Status status)`

### 重实现的保护函数

- `virtual void keyPressEvent(QKeyEvent *e) override`
- `virtual void keyReleaseEvent(QKeyEvent *e) override`
- `virtual void mouseMoveEvent(QMouseEvent *e) override`
- `virtual void mousePressEvent(QMouseEvent *e) override`
- `virtual void mouseReleaseEvent(QMouseEvent *e) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QQuickView::ResizeMode`

**作用与语义：**

该枚举规定了如何调整视图大小。
- `QQuickView::SizeViewToRootObject`：`0`;视图在QML中随根项调整大小。
- `QQuickView::SizeRootObjectToView`：`1`;视图会自动将根项调整到视图大小。

### `enum QQuickView::Status`

**作用与语义：**

指定`QQuickView`的加载状态。
- `QQuickView::Null`：`0`;本`QQuickView`没有源集。
- `QQuickView::Ready`：`1`;本`QQuickView`已加载并创建了QML组件。
- `QQuickView::Loading`：`2`;该`QQuickView`正在加载网络数据。
- `QQuickView::Error`：`3`;发生一个或多个错误。调用`errors()`以获取错误列表。

### `resizeMode : ResizeMode`

**作用与语义：**

该属性决定视图是否应调整窗口内容大小。
如果该属性设置为`SizeViewToRootObject`（默认），视图会调整大小为QML根项的大小。
如果该属性设置为`SizeRootObjectToView`，视图会自动将根元素调整到视图大小。

**如何使用：** 调用 `resizeMode()` 读取当前值；它不会修改应用状态。

### `source : QUrl`

**作用与语义：**

该属性包含QML组件源的URL。
确保提供的URL完整且正确，特别是在从本地文件系统加载文件时使用`QUrl::fromLocalFile()`。
注意，设置源 URL 会导致 QML 组件实例化，即使 URL 与当前值保持不变。

**如何使用：** 调用 `source()` 读取当前值；它不会修改应用状态。

### `[read-only] status : Status`

**作用与语义：**

该组件当前的 `status`。

**如何使用：** 调用 `status()` 读取当前值；它不会修改应用状态。

### `[explicit] QQuickView::QQuickView(QWindow *parent = nullptr)`

**作用与语义：**

构造一个带有给定`parent`的QQuickView。`parent`的默认值为0。

### `QQuickView::QQuickView(QQmlEngine *engine, QWindow *parent)`

**作用与语义：**

构建一个带有QML的`engine`和`parent`的QQuickView。
注意：在这种情况下，QQuickView 不拥有给定的 `engine` 对象;销毁引擎是调用者的责任。如果在视图发布前删除`engine`，`status()` 将返回`QQuickView::Error`。

### `[explicit] QQuickView::QQuickView(const QUrl &source, QWindow *parent = nullptr)`

**作用与语义：**

构造一个QQuickView，包含给定的QML `source`和`parent`。`parent`的默认值为`nullptr`。

### `[explicit, since 6.7] QQuickView::QQuickView(QAnyStringView uri, QAnyStringView typeName, QWindow *parent = nullptr)`

**作用与语义：**

构造一个QQuickView，包含由`uri`和`typeName`指定的元素和父`parent`。`parent`的默认值是`nullptr`。

### `[override virtual noexcept] QQuickView::~QQuickView()`

**作用与语义：**

摧毁了`QQuickView`。

### `QQmlEngine *QQuickView::engine() const`

**作用与语义：**

返回用于实例化QML组件的`QQmlEngine`指针。

### `QList<QQmlError> QQuickView::errors() const`

**作用与语义：**

返回上次编译或创建操作中发生的错误列表。当状态不是错误时，返回一个空列表。

### `QSize QQuickView::initialSize() const`

**作用与语义：**

返回根对象的初始大小。
如果`resizeMode`是QQuickItem：：SizeRootObjectToView，根对象的大小会被调整为视图大小。initialSize包含根对象在调整大小前的大小。

### `[override virtual protected] void QQuickView::keyPressEvent(QKeyEvent *e)`

**作用与语义：**

窗口取得键盘焦点时，Qt 用该处理器把按键按下事件 `e` 送入 Qt Quick 焦点项和输入系统。子类只应拦截确实处理的按键并接受事件；未处理的情况要调用基类实现，否则 QML 项可能收不到键盘事件。

### `[override virtual protected] void QQuickView::keyReleaseEvent(QKeyEvent *e)`

**作用与语义：**

窗口取得键盘焦点时，Qt 用该处理器把按键释放事件 `e` 送入 Qt Quick 焦点项和输入系统。子类只应拦截确实处理的按键并接受事件；未处理的情况要调用基类实现，否则 QML 项可能收不到键盘事件。

### `[slot, since 6.7] void QQuickView::loadFromModule(QAnyStringView uri, QAnyStringView typeName)`

**作用与语义：**

加载由`uri`和`typeName`标识的QML组件。如果组件有QML文件支持，`source`会相应设置。对于`C++`中定义的类型，`source`为空。
如果在调用该方法之前设置了任何`source`，则该方法将被清除。
用相同的`uri`和`typeName`多次调用该方法，会导致QML组件被重新实例化。

### `[override virtual protected] void QQuickView::mouseMoveEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QQuickWindow::mouseMoveEvent`（QMouseEvent *event）。

### `[override virtual protected] void QQuickView::mousePressEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QQuickWindow::mousePressEvent`（QMouseEvent *event）。

### `[override virtual protected] void QQuickView::mouseReleaseEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QQuickWindow::mouseReleaseEvent`（QMouseEvent *event）。

### `QQmlContext *QQuickView::rootContext() const`

**作用与语义：**

该函数返回上下文层级的根节点。每个QML组件实例化在`QQmlContext`中。`QQmlContext`对于将数据传递给QML组件至关重要。在QML中，上下文按层级排列，该层级由`QQmlEngine`管理。

### `QQuickItem *QQuickView::rootObject() const`

**作用与语义：**

返回视图的根`item`。

### `[slot] void QQuickView::setInitialProperties(const QVariantMap &initialProperties)`

**作用与语义：**

设置调用`QQuickView::setSource()`后初始化QML组件的初始属性`initialProperties`。
注意：你只能用这个函数初始化顶层属性。
注意：该函数应始终在`setSource`之前调用，因为组件变`Ready`后该函数无效。

**官方示例：**

```cpp
     QScopedPointer<QQuickView> view { new QQuickView };
     view->setInitialProperties({"x, 100"}, {"width", 50});
     view->setSource(QUrl::fromLocalFile("myqmlfile.qml"));
     view->show();
```

### `[slot] void QQuickView::setSource(const QUrl &url)`

**作用与语义：**

该属性包含QML组件源的URL。
确保提供的URL完整且正确，特别是在从本地文件系统加载文件时使用`QUrl::fromLocalFile()`。
注意，设置源 URL 会导致 QML 组件实例化，即使 URL 与当前值保持不变。

**如何使用：** 调用 `setSource(...)` 修改 `source`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QUrl QQuickView::source() const`

**作用与语义：**

如果设置了，返回源 URL。
注意：属性来源的获取函数。

### `[signal] void QQuickView::statusChanged(QQuickView::Status status)`

**作用与语义：**

该组件当前的 `status`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `status` 的变化，不要把它当作普通函数主动调用。

### `QQuickView::ResizeMode resizeMode() const`

**作用与语义：**

该属性决定视图是否应调整窗口内容大小。
如果该属性设置为`SizeViewToRootObject`（默认），视图会调整大小为QML根项的大小。
如果该属性设置为`SizeRootObjectToView`，视图会自动将根元素调整到视图大小。

**如何使用：** 调用 `resizeMode()` 读取当前值；它不会修改应用状态。

### `void setResizeMode(QQuickView::ResizeMode)`

**作用与语义：**

该属性决定视图是否应调整窗口内容大小。
如果该属性设置为`SizeViewToRootObject`（默认），视图会调整大小为QML根项的大小。
如果该属性设置为`SizeRootObjectToView`，视图会自动将根元素调整到视图大小。

**如何使用：** 调用 `setResizeMode(...)` 修改 `resizeMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QQuickView::Status status() const`

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

`QQuickView` 所属机制类型：QML 属性绑定与场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
