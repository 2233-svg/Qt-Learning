# QQuickWindow

> Qt 6.11.1 · Qt Quick

## 1. 先建立直觉

**一句话定位：** `QQuickWindow` 是 QML 属性绑定与场景图机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Quick 面向 QML/场景图界面，提供可视项、动画、输入和高性能界面基础设施。

### 这是什么

`QQuickWindow` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QQuickWindow>`
- 继承自：QWindow
- 直接派生类：QQuickView

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Quick)
target_link_libraries(mytarget PRIVATE Qt6::Quick)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

### 状态、生命周期和线程

**生命周期：** QML 引擎、上下文和对象所有权必须明确。由 QML 创建的对象通常由引擎管理；通过 context property 或 C++ 暴露的对象要决定由 C++ 持有还是转移给 QML，不能让绑定指向悬空对象。

**状态与结果：** 属性绑定和直接赋值不是一回事：直接给被绑定属性赋值通常会打破原有绑定。C++ 属性要有正确的 notify signal，QML 才能在数据变化时更新；信号参数和属性当前值要保持一致。

**线程与事件循环：** 大多数 QML 对象和 GUI 操作在 GUI 线程，场景图渲染还可能在 render thread。不要在渲染阶段调用 GUI 对象 API；后台数据通过线程安全的信号/槽边界送入 QML。

## 3. 直接使用

需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。 使用时通常按这个过程组织：注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

```cpp
// C++ 侧暴露属性/信号后，在 QML 中建立绑定。
// 变化时发出 notify signal，避免在绑定表达式中直接修改状态。
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `struct GraphicsStateInfo`
- `enum CreateTextureOption { TextureHasAlphaChannel, TextureHasMipmaps, TextureOwnsGLTexture, TextureCanUseAtlas, TextureIsOpaque }`
- `flags CreateTextureOptions`
- `enum RenderStage { BeforeSynchronizingStage, AfterSynchronizingStage, BeforeRenderingStage, AfterRenderingStage, AfterSwapStage, NoStage }`
- `enum SceneGraphError { ContextNotAvailable }`
- `enum TextRenderType { QtTextRendering, NativeTextRendering, CurveTextRendering }`

### 属性

- `activeFocusItem : QQuickItem*`
- `color : QColor`
- `contentItem : QQuickItem* const`
- `(since 6.11) devicePixelRatio : qreal`
- `transientParent : QWindow*`

### 公有函数

- `QQuickWindow(QQuickRenderControl *control)`
- `QQuickWindow(QWindow *parent = nullptr)`
- `virtual ~QQuickWindow() override`
- `QQuickItem * activeFocusItem() const`
- `void beginExternalCommands()`
- `QColor color() const`
- `QQuickItem * contentItem() const`
- `QSGImageNode * createImageNode() const`
- `QSGNinePatchNode * createNinePatchNode() const`
- `QSGRectangleNode * createRectangleNode() const`
- `(since 6.7) QSGTextNode * createTextNode() const`
- `QSGTexture * createTextureFromImage(const QImage &image, QQuickWindow::CreateTextureOptions options) const`
- `QSGTexture * createTextureFromImage(const QImage &image) const`
- `(since 6.6) QSGTexture * createTextureFromRhiTexture(QRhiTexture *texture, QQuickWindow::CreateTextureOptions options = {}) const`
- `qreal effectiveDevicePixelRatio() const`
- `void endExternalCommands()`
- `QImage grabWindow()`
- `(since 6.0) QQuickGraphicsConfiguration graphicsConfiguration() const`
- `(since 6.0) QQuickGraphicsDevice graphicsDevice() const`
- `const QQuickWindow::GraphicsStateInfo & graphicsStateInfo()`
- `QQmlIncubationController * incubationController() const`
- `bool isPersistentGraphics() const`
- `bool isPersistentSceneGraph() const`
- `bool isSceneGraphInitialized() const`
- `(since 6.0) QQuickRenderTarget renderTarget() const`
- `QSGRendererInterface * rendererInterface() const`
- `(since 6.6) QRhi * rhi() const`
- `void scheduleRenderJob(QRunnable *job, QQuickWindow::RenderStage stage)`
- `void setColor(const QColor &color)`
- `(since 6.0) void setGraphicsConfiguration(const QQuickGraphicsConfiguration &config)`
- `(since 6.0) void setGraphicsDevice(const QQuickGraphicsDevice &device)`
- `void setPersistentGraphics(bool persistent)`
- `void setPersistentSceneGraph(bool persistent)`
- `(since 6.0) void setRenderTarget(const QQuickRenderTarget &target)`
- `(since 6.6) QRhiSwapChain * swapChain() const`

### 重实现的公有函数

- `virtual QAccessibleInterface * accessibleRoot() const override`

### 公有槽函数

- `void releaseResources()`
- `void update()`

### 信号

- `void activeFocusItemChanged()`
- `void afterAnimating()`
- `(since 6.0) void afterFrameEnd()`
- `void afterRenderPassRecording()`
- `void afterRendering()`
- `void afterSynchronizing()`
- `(since 6.0) void beforeFrameBegin()`
- `void beforeRenderPassRecording()`
- `void beforeRendering()`
- `void beforeSynchronizing()`
- `void colorChanged(const QColor &)`
- `(since 6.11) void devicePixelRatioChanged()`
- `void frameSwapped()`
- `void sceneGraphAboutToStop()`
- `void sceneGraphError(QQuickWindow::SceneGraphError error, const QString &message)`
- `void sceneGraphInitialized()`
- `void sceneGraphInvalidated()`

### 静态公有成员

- `(since 6.0) QSGRendererInterface::GraphicsApi graphicsApi()`
- `bool hasDefaultAlphaBuffer()`
- `QString sceneGraphBackend()`
- `void setDefaultAlphaBuffer(bool useAlpha)`
- `(since 6.0) void setGraphicsApi(QSGRendererInterface::GraphicsApi api)`
- `void setSceneGraphBackend(const QString &backend)`
- `void setTextRenderType(QQuickWindow::TextRenderType renderType)`
- `QQuickWindow::TextRenderType textRenderType()`

### 重实现的保护函数

- `virtual void closeEvent(QCloseEvent *e) override`
- `virtual bool event(QEvent *event) override`
- `virtual void exposeEvent(QExposeEvent *) override`
- `virtual void focusInEvent(QFocusEvent *ev) override`
- `virtual void focusOutEvent(QFocusEvent *ev) override`
- `virtual void hideEvent(QHideEvent *) override`
- `virtual void keyPressEvent(QKeyEvent *e) override`
- `virtual void keyReleaseEvent(QKeyEvent *e) override`
- `virtual void mouseDoubleClickEvent(QMouseEvent *event) override`
- `virtual void mouseMoveEvent(QMouseEvent *event) override`
- `virtual void mousePressEvent(QMouseEvent *event) override`
- `virtual void mouseReleaseEvent(QMouseEvent *event) override`
- `virtual void resizeEvent(QResizeEvent *ev) override`
- `virtual void showEvent(QShowEvent *) override`
- `virtual void tabletEvent(QTabletEvent *event) override`
- `virtual void wheelEvent(QWheelEvent *event) override`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 91 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QQuickWindow::CreateTextureOptionflags QQuickWindow::CreateTextureOptions`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QQuickWindow` 暴露的类型声明 `创建、Texture、Optionflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:CreateTextureOptionflags QQuickWindow::CreateTextureOptions`。
- 属性名：`QQuickWindow`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QQuickWindow::RenderStage`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QQuickWindow` 暴露的类型声明 `渲染、Stage`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:RenderStage`。
- 属性名：`QQuickWindow`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QQuickWindow::SceneGraphError`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QQuickWindow` 暴露的类型声明 `Scene、Graph、错误`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:SceneGraphError`。
- 属性名：`QQuickWindow`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QQuickWindow::TextRenderType`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QQuickWindow` 暴露的类型声明 `文本、渲染、类型`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:TextRenderType`。
- 属性名：`QQuickWindow`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] activeFocusItem : QQuickItem*`

**API 类别：** 属性说明

**中文解读：** 这是 `QQuickWindow` 的状态/能力属性。通常通过 `activeFocusItem()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`QQuickItem*`。
- 属性名：`activeFocusItem`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `color : QColor`

**API 类别：** 属性说明

**中文解读：** 这是 `QQuickWindow` 的配置属性。初始化或状态切换时通过 `setColor(...)` 设置，之后用 `color()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QColor`。
- 属性名：`color`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] contentItem : QQuickItem* const`

**API 类别：** 属性说明

**中文解读：** 这是 `QQuickWindow` 的状态/能力属性。通常通过 `contentItem()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`QQuickItem* const`。
- 属性名：`contentItem`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only, since 6.11] devicePixelRatio : qreal`

**API 类别：** 属性说明

**中文解读：** 这是 `QQuickWindow` 的状态/能力属性。通常通过 `devicePixelRatio()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`qreal`。
- 属性名：`devicePixelRatio`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `transientParent : QWindow*`

**API 类别：** 属性说明

**中文解读：** 这是 `QQuickWindow` 的配置属性。初始化或状态切换时通过 `setTransientParent(...)` 设置，之后用 `transientParent()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QWindow*`。
- 属性名：`transientParent`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QQuickWindow::QQuickWindow(QQuickRenderControl *control)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QQuickWindow` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `control`：类型为 `QQuickRenderControl *`。没有默认值，调用时必须提供。传入 `QQuickRenderControl *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QQuickWindow::QQuickWindow(QWindow *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QQuickWindow` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `parent`：类型为 `QWindow *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual noexcept] QQuickWindow::~QQuickWindow()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QQuickWindow` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QAccessibleInterface *QQuickWindow::accessibleRoot() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuickWindow::accessibleRoot` 用于计算、查询或取得与“accessible、Root”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QAccessibleInterface *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAccessibleInterface *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QQuickWindow::afterAnimating()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QQuickWindow` 发出的通知信号 `afterAnimating`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal, since 6.0] void QQuickWindow::afterFrameEnd()`

**API 类别：** 成员函数说明

**中文解读：** `QQuickWindow::afterFrameEnd` 用于执行与“after、Frame、结束”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QQuickWindow::afterRenderPassRecording()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QQuickWindow` 发出的通知信号 `afterRenderPassRecording`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QQuickWindow::afterRendering()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QQuickWindow` 发出的通知信号 `afterRendering`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QQuickWindow::afterSynchronizing()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QQuickWindow` 发出的通知信号 `afterSynchronizing`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal, since 6.0] void QQuickWindow::beforeFrameBegin()`

**API 类别：** 成员函数说明

**中文解读：** `QQuickWindow::beforeFrameBegin` 用于执行与“before、Frame、起始位置”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QQuickWindow::beforeRenderPassRecording()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QQuickWindow` 发出的通知信号 `beforeRenderPassRecording`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QQuickWindow::beforeRendering()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QQuickWindow` 发出的通知信号 `beforeRendering`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QQuickWindow::beforeSynchronizing()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QQuickWindow` 发出的通知信号 `beforeSynchronizing`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QQuickWindow::beginExternalCommands()`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `beginExternalCommands`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QQuickWindow::closeEvent(QCloseEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `closeEvent`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数 `e`：类型为 `QCloseEvent *`。没有默认值，调用时必须提供。传入 `QCloseEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSGImageNode *QQuickWindow::createImageNode() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuickWindow::createImageNode` 用于计算、查询或取得与“创建、Image、Node”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSGImageNode *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSGImageNode *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSGNinePatchNode *QQuickWindow::createNinePatchNode() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuickWindow::createNinePatchNode` 用于计算、查询或取得与“创建、Nine、Patch、Node”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSGNinePatchNode *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSGNinePatchNode *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSGRectangleNode *QQuickWindow::createRectangleNode() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuickWindow::createRectangleNode` 用于计算、查询或取得与“创建、Rectangle、Node”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSGRectangleNode *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSGRectangleNode *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.7] QSGTextNode *QQuickWindow::createTextNode() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuickWindow::createTextNode` 用于计算、查询或取得与“创建、文本、Node”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSGTextNode *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSGTextNode *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSGTexture *QQuickWindow::createTextureFromImage(const QImage &image, QQuickWindow::CreateTextureOptions options) const`

**API 类别：** 成员函数说明

**中文解读：** `QQuickWindow::createTextureFromImage` 用于计算、查询或取得与“创建、Texture、转换进入、Image”相关的操作。调用时要先确认当前状态和 `image`、`options` 的有效范围；返回类型是 `QSGTexture *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSGTexture *`。
- 参数 `image`：类型为 `const QImage &`。没有默认值，调用时必须提供。传入 `const QImage &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `options`：类型为 `QQuickWindow::CreateTextureOptions`。没有默认值，调用时必须提供。传入 `QQuickWindow::CreateTextureOptions` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSGTexture *QQuickWindow::createTextureFromImage(const QImage &image) const`

**API 类别：** 成员函数说明

**中文解读：** `QQuickWindow::createTextureFromImage` 用于计算、查询或取得与“创建、Texture、转换进入、Image”相关的操作。调用时要先确认当前状态和 `image` 的有效范围；返回类型是 `QSGTexture *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSGTexture *`。
- 参数 `image`：类型为 `const QImage &`。没有默认值，调用时必须提供。传入 `const QImage &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] QSGTexture *QQuickWindow::createTextureFromRhiTexture(QRhiTexture *texture, QQuickWindow::CreateTextureOptions options = {}) const`

**API 类别：** 成员函数说明

**中文解读：** `QQuickWindow::createTextureFromRhiTexture` 用于计算、查询或取得与“创建、Texture、转换进入、Rhi、Texture”相关的操作。调用时要先确认当前状态和 `texture`、`options` 的有效范围；返回类型是 `QSGTexture *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSGTexture *`。
- 参数 `texture`：类型为 `QRhiTexture *`。没有默认值，调用时必须提供。传入 `QRhiTexture *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `options`：类型为 `QQuickWindow::CreateTextureOptions`。默认值为 `{}`。传入 `QQuickWindow::CreateTextureOptions` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal, since 6.11] void QQuickWindow::devicePixelRatioChanged()`

**API 类别：** 成员函数说明

**中文解读：** 这是状态变化通知 `devicePixelRatioChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal QQuickWindow::effectiveDevicePixelRatio() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuickWindow::effectiveDevicePixelRatio` 用于计算、查询或取得与“effective、Device、Pixel、Ratio”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QQuickWindow::endExternalCommands()`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `endExternalCommands`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] bool QQuickWindow::event(QEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QQuickWindow::event` 用于计算、查询或取得与“event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `event`：类型为 `QEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QQuickWindow::exposeEvent(QExposeEvent *)`

**API 类别：** 成员函数说明

**中文解读：** `QQuickWindow::exposeEvent` 用于执行与“expose、Event”相关的操作。调用时要先确认当前状态和 `QExposeEvent *` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `QExposeEvent *`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QQuickWindow::focusInEvent(QFocusEvent *ev)`

**API 类别：** 成员函数说明

**中文解读：** `QQuickWindow::focusInEvent` 用于执行与“focus、In、Event”相关的操作。调用时要先确认当前状态和 `ev` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `ev`：类型为 `QFocusEvent *`。没有默认值，调用时必须提供。传入 `QFocusEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QQuickWindow::focusOutEvent(QFocusEvent *ev)`

**API 类别：** 成员函数说明

**中文解读：** `QQuickWindow::focusOutEvent` 用于执行与“focus、Out、Event”相关的操作。调用时要先确认当前状态和 `ev` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `ev`：类型为 `QFocusEvent *`。没有默认值，调用时必须提供。传入 `QFocusEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QQuickWindow::frameSwapped()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QQuickWindow` 发出的通知信号 `frameSwapped`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QImage QQuickWindow::grabWindow()`

**API 类别：** 成员函数说明

**中文解读：** `QQuickWindow::grabWindow` 用于计算、查询或取得与“抓取、Window”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QImage`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QImage`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.0] QSGRendererInterface::GraphicsApi QQuickWindow::graphicsApi()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `graphicsApi`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QSGRendererInterface::GraphicsApi`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] QQuickGraphicsConfiguration QQuickWindow::graphicsConfiguration() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuickWindow::graphicsConfiguration` 用于计算、查询或取得与“graphics、Configuration”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QQuickGraphicsConfiguration`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QQuickGraphicsConfiguration`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] QQuickGraphicsDevice QQuickWindow::graphicsDevice() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuickWindow::graphicsDevice` 用于计算、查询或取得与“graphics、Device”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QQuickGraphicsDevice`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QQuickGraphicsDevice`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QQuickWindow::GraphicsStateInfo &QQuickWindow::graphicsStateInfo()`

**API 类别：** 成员函数说明

**中文解读：** `QQuickWindow::graphicsStateInfo` 用于计算、查询或取得与“graphics、State、Info”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QQuickWindow::GraphicsStateInfo &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QQuickWindow::GraphicsStateInfo &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] bool QQuickWindow::hasDefaultAlphaBuffer()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `hasDefaultAlphaBuffer`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QQuickWindow::hideEvent(QHideEvent *)`

**API 类别：** 成员函数说明

**中文解读：** `QQuickWindow::hideEvent` 用于执行与“隐藏、Event”相关的操作。调用时要先确认当前状态和 `QHideEvent *` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `QHideEvent *`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QQmlIncubationController *QQuickWindow::incubationController() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuickWindow::incubationController` 用于计算、查询或取得与“incubation、Controller”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QQmlIncubationController *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QQmlIncubationController *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QQuickWindow::isPersistentGraphics() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isPersistentGraphics`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QQuickWindow::isPersistentSceneGraph() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isPersistentSceneGraph`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QQuickWindow::isSceneGraphInitialized() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isSceneGraphInitialized`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QQuickWindow::keyPressEvent(QKeyEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** `QQuickWindow::keyPressEvent` 用于执行与“key、Press、Event”相关的操作。调用时要先确认当前状态和 `e` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `e`：类型为 `QKeyEvent *`。没有默认值，调用时必须提供。传入 `QKeyEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QQuickWindow::keyReleaseEvent(QKeyEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** `QQuickWindow::keyReleaseEvent` 用于执行与“key、释放、Event”相关的操作。调用时要先确认当前状态和 `e` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `e`：类型为 `QKeyEvent *`。没有默认值，调用时必须提供。传入 `QKeyEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QQuickWindow::mouseDoubleClickEvent(QMouseEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QQuickWindow::mouseDoubleClickEvent` 用于执行与“mouse、Double、Click、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QMouseEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QQuickWindow::mouseMoveEvent(QMouseEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QQuickWindow::mouseMoveEvent` 用于执行与“mouse、移动、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QMouseEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QQuickWindow::mousePressEvent(QMouseEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QQuickWindow::mousePressEvent` 用于执行与“mouse、Press、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QMouseEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QQuickWindow::mouseReleaseEvent(QMouseEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QQuickWindow::mouseReleaseEvent` 用于执行与“mouse、释放、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QMouseEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QQuickWindow::releaseResources()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `releaseResources`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] QQuickRenderTarget QQuickWindow::renderTarget() const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QQuickWindow` 的核心操作 `renderTarget`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`QQuickRenderTarget`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSGRendererInterface *QQuickWindow::rendererInterface() const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QQuickWindow` 的核心操作 `rendererInterface`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`QSGRendererInterface *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QQuickWindow::resizeEvent(QResizeEvent *ev)`

**API 类别：** 成员函数说明

**中文解读：** `QQuickWindow::resizeEvent` 用于执行与“调整尺寸、Event”相关的操作。调用时要先确认当前状态和 `ev` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `ev`：类型为 `QResizeEvent *`。没有默认值，调用时必须提供。传入 `QResizeEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] QRhi *QQuickWindow::rhi() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuickWindow::rhi` 用于计算、查询或取得与“rhi”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRhi *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhi *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QQuickWindow::sceneGraphAboutToStop()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QQuickWindow` 发出的通知信号 `sceneGraphAboutToStop`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QQuickWindow::sceneGraphBackend()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `sceneGraphBackend`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QQuickWindow::sceneGraphError(QQuickWindow::SceneGraphError error, const QString &message)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QQuickWindow` 发出的通知信号 `sceneGraphError`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `error`：类型为 `QQuickWindow::SceneGraphError`。没有默认值，调用时必须提供。错误输出对象或错误状态。解析/执行后要检查它，而不能只看主返回值。
- 参数 `message`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QQuickWindow::sceneGraphInitialized()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QQuickWindow` 发出的通知信号 `sceneGraphInitialized`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QQuickWindow::sceneGraphInvalidated()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QQuickWindow` 发出的通知信号 `sceneGraphInvalidated`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QQuickWindow::scheduleRenderJob(QRunnable *job, QQuickWindow::RenderStage stage)`

**API 类别：** 成员函数说明

**中文解读：** `QQuickWindow::scheduleRenderJob` 用于执行与“schedule、渲染、Job”相关的操作。调用时要先确认当前状态和 `job`、`stage` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `job`：类型为 `QRunnable *`。没有默认值，调用时必须提供。传入 `QRunnable *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `stage`：类型为 `QQuickWindow::RenderStage`。没有默认值，调用时必须提供。传入 `QQuickWindow::RenderStage` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] void QQuickWindow::setDefaultAlphaBuffer(bool useAlpha)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `setDefaultAlphaBuffer`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `useAlpha`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.0] void QQuickWindow::setGraphicsApi(QSGRendererInterface::GraphicsApi api)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `setGraphicsApi`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `api`：类型为 `QSGRendererInterface::GraphicsApi`。没有默认值，调用时必须提供。传入 `QSGRendererInterface::GraphicsApi` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] void QQuickWindow::setGraphicsConfiguration(const QQuickGraphicsConfiguration &config)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setGraphicsConfiguration`。调用它会改变 `QQuickWindow` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `config`：类型为 `const QQuickGraphicsConfiguration &`。没有默认值，调用时必须提供。传入 `const QQuickGraphicsConfiguration &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] void QQuickWindow::setGraphicsDevice(const QQuickGraphicsDevice &device)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setGraphicsDevice`。调用它会改变 `QQuickWindow` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `device`：类型为 `const QQuickGraphicsDevice &`。没有默认值，调用时必须提供。QIODevice 或绘制设备。调用前要确认已经打开、支持所需模式，或处于合法绘制阶段。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QQuickWindow::setPersistentGraphics(bool persistent)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPersistentGraphics`。调用它会改变 `QQuickWindow` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `persistent`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QQuickWindow::setPersistentSceneGraph(bool persistent)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPersistentSceneGraph`。调用它会改变 `QQuickWindow` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `persistent`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] void QQuickWindow::setRenderTarget(const QQuickRenderTarget &target)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setRenderTarget`。调用它会改变 `QQuickWindow` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `const QQuickRenderTarget &`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] void QQuickWindow::setSceneGraphBackend(const QString &backend)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `setSceneGraphBackend`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `backend`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] void QQuickWindow::setTextRenderType(QQuickWindow::TextRenderType renderType)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `setTextRenderType`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `renderType`：类型为 `QQuickWindow::TextRenderType`。没有默认值，调用时必须提供。传入 `QQuickWindow::TextRenderType` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QQuickWindow::showEvent(QShowEvent *)`

**API 类别：** 成员函数说明

**中文解读：** `QQuickWindow::showEvent` 用于执行与“显示、Event”相关的操作。调用时要先确认当前状态和 `QShowEvent *` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `QShowEvent *`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] QRhiSwapChain *QQuickWindow::swapChain() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuickWindow::swapChain` 用于计算、查询或取得与“swap、Chain”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRhiSwapChain *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhiSwapChain *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QQuickWindow::tabletEvent(QTabletEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QQuickWindow::tabletEvent` 用于执行与“tablet、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QTabletEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QQuickWindow::TextRenderType QQuickWindow::textRenderType()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `textRenderType`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QQuickWindow::TextRenderType`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QQuickWindow::update()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `update`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QQuickWindow::wheelEvent(QWheelEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QQuickWindow::wheelEvent` 用于执行与“wheel、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QWheelEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `struct GraphicsStateInfo`

**API 类别：** 公有类型

**中文解读：** 这是 `QQuickWindow` 的 `Graphics、State、Info` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum CreateTextureOption { TextureHasAlphaChannel, TextureHasMipmaps, TextureOwnsGLTexture, TextureCanUseAtlas, TextureIsOpaque }`

**API 类别：** 公有类型

**中文解读：** 这是 `QQuickWindow` 暴露的类型声明 `创建、Texture、Option`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags CreateTextureOptions`

**API 类别：** 公有类型

**中文解读：** 这是 `QQuickWindow` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QQuickItem * activeFocusItem() const`

**API 类别：** 公有函数

**中文解读：** `QQuickWindow::activeFocusItem` 用于计算、查询或取得与“活动状态、Focus、项目访问”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QQuickItem *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QQuickItem *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QColor color() const`

**API 类别：** 公有函数

**中文解读：** `QQuickWindow::color` 用于计算、查询或取得与“color”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QColor`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QColor`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QQuickItem * contentItem() const`

**API 类别：** 公有函数

**中文解读：** `QQuickWindow::contentItem` 用于计算、查询或取得与“content、项目访问”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QQuickItem *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QQuickItem *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setColor(const QColor &color)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setColor`。调用它会改变 `QQuickWindow` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `color`：类型为 `const QColor &`。没有默认值，调用时必须提供。传入 `const QColor &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void activeFocusItemChanged()`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `activeFocusItemChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void colorChanged(const QColor &)`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `colorChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `const QColor &`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

## 6. 深入实践与常见坑

### 生命周期和资源边界

QML 引擎、上下文和对象所有权必须明确。由 QML 创建的对象通常由引擎管理；通过 context property 或 C++ 暴露的对象要决定由 C++ 持有还是转移给 QML，不能让绑定指向悬空对象。

### 状态和错误边界

属性绑定和直接赋值不是一回事：直接给被绑定属性赋值通常会打破原有绑定。C++ 属性要有正确的 notify signal，QML 才能在数据变化时更新；信号参数和属性当前值要保持一致。

### 线程边界

大多数 QML 对象和 GUI 操作在 GUI 线程，场景图渲染还可能在 render thread。不要在渲染阶段调用 GUI 对象 API；后台数据通过线程安全的信号/槽边界送入 QML。

### 最容易出现的错误

不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QQuickWindow` 所属机制类型：QML 属性绑定与场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
