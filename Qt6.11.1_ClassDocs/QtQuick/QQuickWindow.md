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

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QQuickWindow::CreateTextureOptionflags QQuickWindow::CreateTextureOptions`

**作用与语义：**

CreateTextureOption 枚举用于自定义纹理的封装方式。
- `QQuickWindow::TextureHasAlphaChannel`: `0x0001`；纹理具有 alpha 通道，并应使用混合方式绘制。
- `QQuickWindow::TextureHasMipmaps`: `0x0002`；纹理具有 mipmap，可以在启用 mipmapping 的情况下绘制。
- `QQuickWindow::TextureOwnsGLTexture`: `0x0004`；从 Qt 6.0 起，此标志在实际中不使用并被忽略。原生图形资源的所有权无法转移到封装的 `QSGTexture`，因为 Qt Quick 可能没有关于如何释放此类对象及其关联内存的必要详细信息。
- `QQuickWindow::TextureCanUseAtlas`: `0x0008`；图像可以上传到纹理图集。
- `QQuickWindow::TextureIsOpaque`: `0x0010`；纹理在 `QSGTexture::hasAlphaChannel()` 返回 false，并且不会进行混合。此标志在 Qt 5.6 中添加。
CreateTextureOptions 类型是 QFlags<CreateTextureOption> 的 typedef。它存储 CreateTextureOption 值的按位或组合。

### `enum QQuickWindow::RenderStage`

**作用与语义：**

- `QQuickWindow::BeforeSynchronizingStage`：`0`;在同步之前。
- `QQuickWindow::AfterSynchronizingStage`：`1`;同步后。
- `QQuickWindow::BeforeRenderingStage`：`2`;渲染前。
- `QQuickWindow::AfterRenderingStage`：`3`;渲染后。
- `QQuickWindow::AfterSwapStage`：`4`;帧交换后。
- `QQuickWindow::NoStage`：`5`;越快越好。该数值是在第5.6季度加的。

### `enum QQuickWindow::SceneGraphError`

**作用与语义：**

该枚举描述了`sceneGraphError()`信号中的误差。
- `QQuickWindow::ContextNotAvailable`：`1`;图形上下文创建失败。这通常意味着没有找到合适的OpenGL实现，例如因为未安装图形驱动程序，因此不支持OpenGL 2。在使用OpenGL ES的移动和嵌入式板上，这种错误很可能表明窗口系统集成存在问题，甚至可能是Qt配置错误。

### `enum QQuickWindow::TextRenderType`

**作用与语义：**

该枚举描述了 Qt Quick 中文本类元素的默认渲染类型（`Text`、`TextInput` 等）。
如果你希望文本在目标平台上看起来像原生，且不需要诸如文本转换等高级功能，请选择 NativeTextRendering。将这些功能与 NativeTextRendering 渲染类型结合使用，会导致效果较差，有时甚至出现像素化。
`QtTextRendering`和`CurveTextRendering`都是硬件加速技术。`QtTextRendering`速度更快，但占用更多内存，且在大尺寸时会出现渲染伪影。`CurveTextRendering`应作为替代方案，适用于`QtTextRendering`无法获得良好视觉效果或优先减少图形内存消耗的情况。
- `QQuickWindow::QtTextRendering`：`0`;使用 Qt 自己的光栅化算法。
- `QQuickWindow::NativeTextRendering`：`1`;使用操作系统的原生光栅化器来处理文本。
- `QQuickWindow::CurveTextRendering`：`2`;文本通过直接运行在图形硬件上的曲线光栅器渲染。（于 Qt 6.7.0 引入。）

### `[read-only] activeFocusItem : QQuickItem*`

**作用与语义：**

该属性包含当前具有主动焦点的物品;若没有当前焦点的物品则`null`。

**如何使用：** 调用 `activeFocusItem()` 读取当前值；它不会修改应用状态。

### `color : QColor`

**作用与语义：**

该属性保留用于清除每帧开始时颜色缓冲区的颜色。
默认情况下，透明色是白色。

**如何使用：** 调用 `color()` 读取当前值；它不会修改应用状态。

### `[read-only] contentItem : QQuickItem* const`

**作用与语义：**

该属性包含场景的不可见根元素。
一个`QQuickWindow`总是有一个包含其所有内容的不可见根项。要将物品添加到该窗口，请将这些项重新为 contentItem 或场景中的现有项。

**如何使用：** 调用 `contentItem()` 读取当前值；它不会修改应用状态。

### `[read-only, since 6.11] devicePixelRatio : qreal`

**作用与语义：**

返回窗口的物理像素与设备无关像素的比例。该值取决于窗口所在的屏幕，且当窗口移动时可能会变化。

**如何使用：** 调用 `devicePixelRatio()` 读取当前值；它不会修改应用状态。

### `transientParent : QWindow*`

**作用与语义：**

该属性包含该窗口作为瞬态弹出窗口的窗口。
这向窗口管理器提示该窗口是代表瞬态父窗口的对话框或弹窗，可以是任何类型的`QWindow`。
为了使窗口默认置中于其瞬态父节点之上，根据窗口管理器的不同，可能还需要用合适的`Qt::WindowType`（如`Qt::Dialog`）设置`flags`属性。

**如何使用：** 调用 `transientParent()` 读取当前值；它不会修改应用状态。

### `[explicit] QQuickWindow::QQuickWindow(QQuickRenderControl *control)`

**作用与语义：**

构建一个窗口用于显示QML场景，渲染由`control`对象控制。更多信息请参阅`QQuickRenderControl`的文档。

### `[explicit] QQuickWindow::QQuickWindow(QWindow *parent = nullptr)`

**作用与语义：**

构建一个窗口用于显示带有父窗口`parent`的QML场景。

### `[override virtual noexcept] QQuickWindow::~QQuickWindow()`

**作用与语义：**

把窗户都砸了。

### `[override virtual] QAccessibleInterface *QQuickWindow::accessibleRoot() const`

**作用与语义：**

返回该窗口的无障碍界面，若无法创建该接口则返回0。

### `[signal] void QQuickWindow::afterAnimating()`

**作用与语义：**

该信号在图形界面线程上发出，然后请求渲染线程执行场景图同步。
与其他类似信号不同，该信号是在图形界面线程中发出，而非渲染线程。它可用于同步外部动画系统与QML内容。同时，这意味着该信号不适合触发图形操作。

### `[signal, since 6.0] void QQuickWindow::afterFrameEnd()`

**作用与语义：**

当场景图提交一帧时，该信号会发出。该信号在所有相关信号（如`afterRendering()`）之后发出。它是场景图渲染线程渲染帧时发出的最后一个信号。
注意：与`frameSwapped()`不同，当Qt Quick输出通过`QQuickRenderControl`重定向时，该信号也必然会发出。
警告：此信号来自场景图渲染线程。如果您的槽函数函数需要在执行继续前完成，必须确保连接是直接的（详见`Qt::ConnectionType`）。

### `[signal] void QQuickWindow::afterRenderPassRecording()`

**作用与语义：**

该信号是在场景图录制主渲染通道命令后发出的，但该通道尚未在命令缓冲区上最终完成。
该信号比`afterRendering()`更早发出，确保不仅帧，连场景图主渲染通道的录制过程仍然活跃。这使得插入命令无需生成完整的独立渲染通道（通常会清除附加图像）。本地图形对象可以通过`QSGRendererInterface`查询。
注意：资源更新（上传、复制）通常不能在渲染通道内排队。因此，更复杂的用户渲染需要同时连接`beforeRendering()`和该信号。
警告：此信号来自场景图渲染线程。如果您的槽函数函数需要在执行继续前完成，必须确保连接是直接的（见`Qt::ConnectionType`）。

### `[signal] void QQuickWindow::afterRendering()`

**作用与语义：**

信号是在场景图将其命令添加到尚未提交到图形队列的命令缓冲区后发出的。如有需要，连接该信号的槽函数可以先通过`QSGRendererInterface`查询本地资源，如命令缓冲区。但请注意，渲染通道（或多个通道）此时已经被记录，无法在场景图通道中添加更多命令。相反，使用`afterRenderPassRecording()`来实现。因此，该信号在Qt 6中的作用有限，不同于Qt 5。相反，通常是`beforeRendering()`与`beforeRenderPassRecording()`，或`beforeRendering()`与`afterRenderPassRecording()`的结合，用于实现自定义渲染的底层或叠加。
警告：此信号来自场景图渲染线程。如果您的槽函数函数需要在执行继续前完成，必须确保连接是直接的（见 `Qt::ConnectionType`）。
注意：使用OpenGL时，请注意设置OpenGL 3.x或4.x的特定状态，并在从连接槽返回时保持这些状态为启用或设置为非默认值，可能会干扰场景图的渲染。场景图用于渲染的`QOpenGLContext`在信号发出时会被绑定。

### `[signal] void QQuickWindow::afterSynchronizing()`

**作用与语义：**

该信号是在场景图与QML状态同步后发出的。
该信号可用于调用`QQuickItem::updatePaintNode()`后进行准备工作，前提是GUI线程仍处于锁定状态。
使用 OpenGL 时，场景图用于渲染的 `QOpenGLContext` 此时会被绑定。
警告：此信号来自场景图渲染线程。如果您的槽函数函数需要在执行继续前完成，必须确保连接是直接的（见`Qt::ConnectionType`）。
警告：使用OpenGL时，请注意设置OpenGL 3.x或4.x的特定状态，并在从连接槽返回时保持这些状态为启用或设置为非默认值，可能会干扰场景图的渲染。

### `[signal, since 6.0] void QQuickWindow::beforeFrameBegin()`

**作用与语义：**

该信号在场景图开始准备帧之前发出。该信号位于`beforeSynchronizing()`或`beforeRendering()`等信号之前。这是场景图渲染线程在准备新帧时发出的最早信号。
该信号对于需要执行某些操作（如资源清理）的低级图形框架尤为重要，而此时 Qt Quick 尚未通过底层渲染接口 API 启动新帧录制。
警告：此信号来自场景图渲染线程。如果你的槽函数函数需要在执行继续前完成，必须确保连接是直接的（见`Qt::ConnectionType`）。

### `[signal] void QQuickWindow::beforeRenderPassRecording()`

**作用与语义：**

该信号在场景图开始录制主渲染通道命令之前发出。（图层有自己的通道，在该信号发出时已完全记录。）信号发出时，渲染通道已在命令缓冲区激活。
该信号比 `beforeRendering()` 晚发出，确保不仅画面，连场景图主渲染通道的录制都处于激活状态。这使得插入命令无需生成完整的独立渲染通道（通常会清除附加图像）。原生图形对象可以通过`QSGRendererInterface`查询。
注意：资源更新（上传、复制）通常不能在渲染通道内排队。因此，更复杂的用户渲染需要同时连接`beforeRendering()`和该信号。
警告：此信号来自场景图渲染线程。如果你的槽函数函数需要在执行继续前完成，必须确保连接是直接的（见 `Qt::ConnectionType`）。

### `[signal] void QQuickWindow::beforeRendering()`

**作用与语义：**

该信号是在帧准备完成后发出的，这意味着在录制模式下（如适用）会有一个命令缓冲区。如有需要，连接到该信号的槽函数函数可以通过`QSGRendererInterface`查询本地资源，类似之前的命令。但请注意，此时主渲染流程的录制尚未开始，且无法在该过程中添加命令。启动一次传输意味着清除颜色、深度和模板缓冲区，因此仅仅连接该信号无法实现底层渲染。而是连接到`beforeRenderPassRecording()`。然而，如果需要记录复制类命令，连接该信号仍然很重要，因为这些命令无法被排在渲染通道中。
警告：此信号来自场景图渲染线程。如果您的槽函数函数需要在执行继续前完成，必须确保连接是直接的（见`Qt::ConnectionType`）。
注意：使用 OpenGL 时，注意设置 OpenGL 3.x 或 4.x 的特定状态，并在从连接槽返回时保持启用或设置为非默认值，可能会干扰场景图的渲染。场景图用于渲染的`QOpenGLContext`在信号发出时会被绑定。

### `[signal] void QQuickWindow::beforeSynchronizing()`

**作用与语义：**

该信号在场景图与QML状态同步之前发出。
即使信号来自场景图渲染线程，GUI线程仍会被阻挡，就像`QQuickItem::updatePaintNode()`一样。因此，访问连接`Qt::DirectConnection`的槽函数或λ线程数据是安全的。
该信号可用于调用`QQuickItem::updatePaintNode()`前所需的任何准备工作。
使用OpenGL时，场景图用于渲染的`QOpenGLContext`此时会被绑定。
警告：此信号来自场景图渲染线程。如果您的槽函数函数需要在执行继续前完成，必须确保连接是直接的（参见`Qt::ConnectionType`）。
警告：使用OpenGL时，请注意设置OpenGL 3.x或4.x的特定状态，并在从连接槽返回时保持这些状态为启用或设置为非默认值，可能会干扰场景图的渲染。

### `void QQuickWindow::beginExternalCommands()`

**作用与语义：**

当将原始图形（OpenGL、Vulkan、Metal 等）命令与场景图渲染混合时，必须先调用该函数，然后再向场景图用于渲染主渲染通道的命令缓冲区发送命令。这是为了避免重叠状态。
实际上，该功能通常通过连接到`beforeRenderPassRecording()`或`afterRenderPassRecording()`信号的槽函数调用。
在向应用程序自身的命令缓冲区（例如由应用程序创建和管理的 VkCommandBuffer 或 MTLCommandBuffer MTLRenderCommandEncoder，而非从场景图中检索）时，无需调用该函数。在图形 API（如 OpenGL、Direct 3D 11）中，beginExternalCommands() 和 `endExternalCommands()` 共同替代了 Qt 5 resetOpenGLState() 函数。
在`QSGRenderNode`的`render()`实现中，调用该函数和`endExternalCommands()`是不必要的，因为场景图对渲染节点隐式执行必要的步骤。
本地图形对象（如图形设备、命令缓冲区或编码器）可通过`QSGRendererInterface::getResource()`访问。
警告：请注意，`QSGRendererInterface::CommandListResource` 可能在 bestartExternalCommands() - `endExternalCommands()` 之间返回不同的对象。当底层实现提供了专门的次级命令缓冲区用于在渲染过程中记录外部图形命令时，这种情况就会发生。因此，调用该函数后请务必查询 CommandListResource。不要尝试重用之前查询中的对象。
注意：当场景图使用OpenGL时，请注意上下文中的OpenGL状态可以有任意设置，而该函数不会将状态重置回默认状态。

### `[override virtual protected] void QQuickWindow::closeEvent(QCloseEvent *e)`

**作用与语义：**

重实现自：`QWindow::closeEvent`（QCloseEvent *ev）。

### `QSGImageNode *QQuickWindow::createImageNode() const`

**作用与语义：**

创建一个简单的图像节点。当场景图未初始化时，返回值为空。
这是一种交叉后端替代方案，不用直接构建`QSGSimpleTextureNode`。

### `QSGNinePatchNode *QQuickWindow::createNinePatchNode() const`

**作用与语义：**

创建一个九个补丁节点。当场景图未初始化时，返回值为空。

### `QSGRectangleNode *QQuickWindow::createRectangleNode() const`

**作用与语义：**

创建一个简单的矩形节点。当场景图未初始化时，返回值为空。
这是一种跨后端替代方案，不用直接构建`QSGSimpleRectNode`。

### `[since 6.7] QSGTextNode *QQuickWindow::createTextNode() const`

**作用与语义：**

创建文本节点。当场景图未初始化时，返回值为空。

### `QSGTexture *QQuickWindow::createTextureFromImage(const QImage &image, QQuickWindow::CreateTextureOptions options) const`

**作用与语义：**

从提供的`image`创建新的`QSGTexture`。如果图像有α通道，对应的纹理也会有α通道。
函数调用者负责删除返回的纹理。底层的原生纹理对象随后连同`QSGTexture`一起被销毁。
当`options`包含`TextureCanUseAtlas`时，引擎可能会将图像放入纹理图集。图集中的纹理需要依赖 `QSGTexture::normalizedTextureSubRect()` 来提供几何体，不支持`QSGTexture::Repeat`。`CreateTextureOption` 中的其他值被忽略。
当 `options` 包含 `TextureIsOpaque` 时，引擎会生成一个 RGB 纹理，但该纹理返回 false `QSGTexture::hasAlphaChannel()`。不透明纹理在大多数情况下渲染速度更快。当该标志未设置时，纹理将根据图像格式拥有 alpha 通道。
当`options`包含`TextureHasMipmaps`时，引擎会创建一个纹理，可以使用mipmap过滤。多重映射纹理不能出现在图集中。
在`options`中设置`TextureHasAlphaChannel`对此功能没有任何作用，因为默认默认是Alpha通道和混合。要选择退出，请设置`TextureIsOpaque`。
当场景图使用 OpenGL 时，返回的纹理将使用 `GL_TEXTURE_2D` 作为纹理目标，`GL_RGBA` 作为内部格式。而其他图形 API 通常纹理格式`RGBA8`。重新实现 `QSGTexture` 以创建参数不同纹理。
警告：如果场景图尚未初始化，该函数将返回0。
警告：返回的纹理不是由场景图管理的内存，必须由渲染线程调用者显式删除。这可以通过从`QSGNode`解构器中删除纹理，或者在纹理已经与渲染线程有亲和力的情况下使用`deleteLater()`实现。
该函数可以从主线程和渲染线程调用。

### `QSGTexture *QQuickWindow::createTextureFromImage(const QImage &image) const`

**作用与语义：**

从提供的`image`创建新的`QSGTexture`。如果图像有α通道，对应的纹理也会有α通道。
函数调用者负责删除返回的纹理。底层的原生纹理对象随后连同`QSGTexture`一起被销毁。
当`options`包含`TextureCanUseAtlas`时，引擎可能会将图像放入纹理图集。图集中的纹理需要依赖 `QSGTexture::normalizedTextureSubRect()` 来提供几何体，不支持`QSGTexture::Repeat`。`CreateTextureOption` 中的其他值被忽略。
当 `options` 包含 `TextureIsOpaque` 时，引擎会生成一个 RGB 纹理，但该纹理返回 false `QSGTexture::hasAlphaChannel()`。不透明纹理在大多数情况下渲染速度更快。当该标志未设置时，纹理将根据图像格式拥有 alpha 通道。
当`options`包含`TextureHasMipmaps`时，引擎会创建一个纹理，可以使用mipmap过滤。多重映射纹理不能出现在图集中。
在`options`中设置`TextureHasAlphaChannel`对此功能没有任何作用，因为默认默认是Alpha通道和混合。要选择退出，请设置`TextureIsOpaque`。
当场景图使用 OpenGL 时，返回的纹理将使用 `GL_TEXTURE_2D` 作为纹理目标，`GL_RGBA` 作为内部格式。而其他图形 API 通常纹理格式`RGBA8`。重新实现 `QSGTexture` 以创建参数不同纹理。
警告：如果场景图尚未初始化，该函数将返回0。
警告：返回的纹理不是由场景图管理的内存，必须由渲染线程调用者显式删除。这可以通过从`QSGNode`解构器中删除纹理，或者在纹理已经与渲染线程有亲和力的情况下使用`deleteLater()`实现。
该函数可以从主线程和渲染线程调用。

### `[since 6.6] QSGTexture *QQuickWindow::createTextureFromRhiTexture(QRhiTexture *texture, QQuickWindow::CreateTextureOptions options = {}) const`

**作用与语义：**

用提供的`texture`创建新的`QSGTexture`。
使用`options`来自定义纹理属性。该函数只考虑`TextureHasAlphaChannel`标志。设置后，场景图渲染器始终将生成的`QSGTexture`视为需要混合。对于完全不透明的纹理，不设置标志可以节省渲染时进行 alpha 混合的成本。标志与`QRhiTexture`的 `format` 没有直接对应，也就是说，在采用常用纹理格式（如常用`QRhiTexture::RGBA8`）时不设置标志是完全正常的。
多点映射不由`options`控制，因为 `texture` Mipmap 已经创建了，并且内置了是否有 mipmap。
归还的`QSGTexture`拥有`QRhiTexture`，意味着`texture`与归还的`QSGTexture`一起被销毁。
如果`texture`拥有其底层的本地图形资源（OpenGL纹理对象、Vulkan图像等），这取决于`QRhiTexture`的创建方式（`QRhiTexture::create()`或`QRhiTexture::createFrom()`），而该函数不会控制或更改。
注意：只有当场景图已经初始化并使用默认的基于`QRhi`的自适应时，这才有效。否则返回值`nullptr`。
注意：该函数只能在场景图渲染线程中调用。

### `[signal, since 6.11] void QQuickWindow::devicePixelRatioChanged()`

**作用与语义：**

返回窗口的物理像素与设备无关像素的比例。该值取决于窗口所在的屏幕，且当窗口移动时可能会变化。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `devicePixelRatio` 的变化，不要把它当作普通函数主动调用。

### `qreal QQuickWindow::effectiveDevicePixelRatio() const`

**作用与语义：**

返回窗口的物理像素与设备无关像素的比例。该值取决于窗口所在的屏幕，且当窗口移动时可能会变化。

**如何使用：** 调用 `effectiveDevicePixelRatio()` 读取当前值；它不会修改应用状态。

### `void QQuickWindow::endExternalCommands()`

**作用与语义：**

当将原始图形（OpenGL、Vulkan、Metal 等）命令与场景图渲染混合使用时，必须在将命令录入场景图渲染主渲染通道的命令缓冲区后调用该函数。这是为了避免卡顿状态。
实际上，该功能通常通过连接到`beforeRenderPassRecording()`或`afterRenderPassRecording()`信号的槽函数调用。
在将命令记录到应用程序自身的命令缓冲区（例如应用程序创建和管理的 VkCommandBuffer 或 MTLCommandBuffer MTLRenderCommandEncoder，而非从场景图中检索）时，无需调用该函数。在图形 API 中，若没有暴露本地命令缓冲区概念（如 OpenGL、Direct 3D 11），`beginExternalCommands()` 和 endExternalCommands() 共同替代了 Qt 5 resetOpenGLState() 函数。
在`QSGRenderNode`的`render()`实现中，调用该函数和 `beginExternalCommands()` 并非必需，因为场景图隐式执行渲染节点所需的步骤。

### `[override virtual protected] bool QQuickWindow::event(QEvent *event)`

**作用与语义：**

重实现自：`QWindow::event`（QEvent *ev）。

### `[override virtual protected] void QQuickWindow::exposeEvent(QExposeEvent *)`

**作用与语义：**

重实现自：`QWindow::exposeEvent`（QExposeEvent *ev）。

### `[override virtual protected] void QQuickWindow::focusInEvent(QFocusEvent *ev)`

**作用与语义：**

重实现自：`QWindow::focusInEvent`（QFocusEvent *ev）。

### `[override virtual protected] void QQuickWindow::focusOutEvent(QFocusEvent *ev)`

**作用与语义：**

重实现自：`QWindow::focusOutEvent`（QFocusEvent *ev）。

### `[signal] void QQuickWindow::frameSwapped()`

**作用与语义：**

当帧被排队等待呈现时，该信号会发出。在启用垂直同步时，在连续动画场景中，每个垂直同步间隔最多发出一次信号。
该信号将由场景图渲染线程发出。

### `QImage QQuickWindow::grabWindow()`

**作用与语义：**

抓取窗口内容并以图像形式返回。
当窗口不可见时，可以调用 grabWindow() 函数。这要求窗口`created`且大小有效，且同一进程中没有其他 `QQuickWindow` 实例在渲染。
注意：当该窗口与`QQuickRenderControl`结合使用时，该函数的结果是空的图像，除非`software`后端正在使用。这是因为当通过`QQuickRenderControl`和`setRenderTarget()`将输出重定向到应用管理的图形资源（如纹理）时，应用程序更适合管理和执行最终的回读操作，因为它本身就完全控制了该资源。
警告：调用该函数会导致性能问题。
警告：该函数只能从GUI线程中调用。

### `[static, since 6.0] QSGRendererInterface::GraphicsApi QQuickWindow::graphicsApi()`

**作用与语义：**

返回如果场景图在此时初始化时将使用的图形API。
查询场景图所用API的标准方式是在场景图初始化后使用`QSGRendererInterface::graphicsApi()`，例如在`sceneGraphInitialized()`信号发出时或之后。在这种情况下，可以得到真实的结果，因为这样就知道所有初始化都是用该图形API正确完成的。
这并不总是方便的。如果应用需要搭建外部框架，或者需要以依赖场景图内置API选择逻辑的方式处理`setGraphicsDevice()`，那么推迟这些操作直到`QQuickWindow`可见或调用`QQuickRenderControl::initialize()`之后，并不总是可行的。
因此，这个静态函数作为`setGraphicsApi()`的对应物提供：它可以随时调用，结果反映了如果场景图在调用点被初始化时会选择的 API。
注意：该静态函数仅在主线（GUI）线程中调用。在渲染时查询 API，请使用 `QSGRendererInterface`，因为该对象存在渲染线程中。
注意：该函数不考虑场景图后端。

### `[since 6.0] QQuickGraphicsConfiguration QQuickWindow::graphicsConfiguration() const`

**作用与语义：**

返回传递给`setGraphicsConfiguration()`的`QQuickGraphicsConfiguration`，或者返回默认构造的。

### `[since 6.0] QQuickGraphicsDevice QQuickWindow::graphicsDevice() const`

**作用与语义：**

返回传递给`setGraphicsDevice()`的`QQuickGraphicsDevice`，或默认构造的。

### `const QQuickWindow::GraphicsStateInfo &QQuickWindow::graphicsStateInfo()`

**作用与语义：**

返回一个描述RHI内部状态的`GraphicsStateInfo`结构体引用，特别是后端的双缓冲或三缓冲状态（如Vulkan或Metal集成）。当底层图形API是Vulkan或Metal，且外部渲染代码希望对自身经常变化的资源（如均匀缓冲区）进行双缓冲或三缓冲时，这尤为重要，以避免流水线停滞。

### `[static] bool QQuickWindow::hasDefaultAlphaBuffer()`

**作用与语义：**

返回是否在新创建的窗口中使用 alpha 透明度。

### `[override virtual protected] void QQuickWindow::hideEvent(QHideEvent *)`

**作用与语义：**

重实现自：`QWindow::hideEvent`（QHideEvent *ev）。

### `QQmlIncubationController *QQuickWindow::incubationController() const`

**作用与语义：**

返回一个孵化控制器，在该窗口内在帧间拼接孵化。`QQuickView`会自动帮你安装这个控制器，否则你需要用`QQmlEngine::setIncubationController()`自己安装。
控制器归窗口所有，删除窗口时控制器会被销毁。

### `bool QQuickWindow::isPersistentGraphics() const`

**作用与语义：**

是否能在`QQuickWindow`生命周期内释放关键图形资源。
注意：这只是提示，不保证会被考虑。

### `bool QQuickWindow::isPersistentSceneGraph() const`

**作用与语义：**

返回场景图节点和资源是否能在该`QQuickWindow`生命周期内释放。
注意：这是一个提示。这种情况发生的时间和方式取决于具体的实现方式。

### `bool QQuickWindow::isSceneGraphInitialized() const`

**作用与语义：**

如果场景图已被初始化，则返回为真;否则返回为假。

### `[override virtual protected] void QQuickWindow::keyPressEvent(QKeyEvent *e)`

**作用与语义：**

窗口取得键盘焦点时，Qt 用该处理器把按键按下事件 `e` 送入 Qt Quick 焦点项和输入系统。子类只应拦截确实处理的按键并接受事件；未处理的情况要调用基类实现，否则 QML 项可能收不到键盘事件。

### `[override virtual protected] void QQuickWindow::keyReleaseEvent(QKeyEvent *e)`

**作用与语义：**

窗口取得键盘焦点时，Qt 用该处理器把按键释放事件 `e` 送入 Qt Quick 焦点项和输入系统。子类只应拦截确实处理的按键并接受事件；未处理的情况要调用基类实现，否则 QML 项可能收不到键盘事件。

### `[override virtual protected] void QQuickWindow::mouseDoubleClickEvent(QMouseEvent *event)`

**作用与语义：**

重实现自：`QWindow::mouseDoubleClickEvent`（QMouseEvent *ev）。

### `[override virtual protected] void QQuickWindow::mouseMoveEvent(QMouseEvent *event)`

**作用与语义：**

重实现自：`QWindow::mouseMoveEvent`（QMouseEvent *ev）。

### `[override virtual protected] void QQuickWindow::mousePressEvent(QMouseEvent *event)`

**作用与语义：**

重实现自：`QWindow::mousePressEvent`（QMouseEvent *ev）。

### `[override virtual protected] void QQuickWindow::mouseReleaseEvent(QMouseEvent *event)`

**作用与语义：**

重实现自：`QWindow::mouseReleaseEvent`（QMouseEvent *ev）。

### `[slot] void QQuickWindow::releaseResources()`

**作用与语义：**

该函数尝试释放当前由 QML 场景中持有的冗余资源。
调用该函数会请求场景图释放缓存的图形资源，如图形流水线对象、着色器程序或图像数据。
此外，根据所使用的渲染循环，该功能还可能导致场景图和所有与窗口相关的渲染资源被释放。如果发生这种情况，`sceneGraphInvalidated()`信号会被发出，允许用户清理自己的图形资源。如果应用程序无法处理清理，`setPersistentGraphics()`和`setPersistentSceneGraph()`函数可以用来防止这种情况发生，但代价是内存占用增加。
注意：缓存的图形资源（如图形管道或着色器程序）的发布不依赖于持久性提示。这些提示的释放无论持久图形和场景图提示的值如何，都会发生。
注意：该函数与`QQuickItem::releaseResources()`虚拟函数无关。

### `[since 6.0] QQuickRenderTarget QQuickWindow::renderTarget() const`

**作用与语义：**

返回传递给`setRenderTarget()`的`QQuickRenderTarget`，或默认构造的。

### `QSGRendererInterface *QQuickWindow::rendererInterface() const`

**作用与语义：**

返回当前渲染器接口。该值始终有效，且永远不会为空值。
注意：该函数可以在构建`QQuickWindow`后随时调用，即使`isSceneGraphInitialized()`仍为虚假。然而，某些渲染器接口函数，特别是`QSGRendererInterface::getResource()`，在场景图上线运行前无法正常工作。而后端查询，如`QSGRendererInterface::graphicsApi()`或`QSGRendererInterface::shaderType()`，则始终是可运行的。
注意：返回指针的所有权仍归 Qt。返回的实例可能在不同 `QQuickWindow` 实例之间共享，取决于所使用的场景图后端。因此，应用程序应为每个`QQuickWindow`查询接口对象，而不是重复使用已查询的指针。

### `[override virtual protected] void QQuickWindow::resizeEvent(QResizeEvent *ev)`

**作用与语义：**

窗口尺寸改变时接收 `ev`，并让 Qt Quick 场景和内容项按新尺寸更新。子类可在这里同步自定义资源，但应调用基类实现，且不要在事件处理中执行耗时布局或渲染。

### `[since 6.6] QRhi *QQuickWindow::rhi() const`

**作用与语义：**

返回该窗口用于渲染的 `QRhi` 对象。
仅在窗口使用 Qt 的 3D API 和着色语言抽象时才可用，这意味着使用`software`适配时结果总是空的。
结果仅在渲染初始化时有效，这由`sceneGraphInitialized()`信号的发射表示。在此之前，返回的值为空值。在常规的屏幕上`QQuickWindow`场景图初始化通常发生在原生窗口首次曝光（显示）时。使用`QQuickRenderControl`时，初始化是在显式`initialize()`调用中完成。
实际上，该函数是通过`QSGRendererInterface`查询`QRhi`的快捷方式。

### `[signal] void QQuickWindow::sceneGraphAboutToStop()`

**作用与语义：**

当场景图即将停止渲染时，这个信号会在渲染线程上发出。这通常是因为窗口被隐藏了。
应用程序可以使用该信号释放资源，但应准备快速重新实现。场景图和图形上下文目前不会发布。
警告：此信号来自场景图渲染线程。如果你的槽函数函数需要在执行继续前完成，必须确保连接是直接的（见`Qt::ConnectionType`）。
警告：请非常确保sceneGraphAboutToStop()的信号处理程序保持图形上下文与输入信号处理时的状态相同。未能做到这一点可能导致场景无法正常渲染。

### `[static] QString QQuickWindow::sceneGraphBackend()`

**作用与语义：**

返回请求的Qt Quick场景图后端。
注意：该函数的返回值可能因后续调用`setSceneGraphBackend()`而过时，直到应用程序中的第一个`QQuickWindow`被构建完成。
注意：该值仅反映`QT_QUICK_BACKEND`环境变量中的请求，前提是构建`QQuickWindow`。

### `[signal] void QQuickWindow::sceneGraphError(QQuickWindow::SceneGraphError error, const QString &message)`

**作用与语义：**

当场景图初始化过程中出现`error`时，该信号会发出。
如果应用程序希望以自定义方式处理错误，比如图形上下文创建失败，应连接到该信号。当没有槽函数连接到该信号时，行为会有所不同：快速会打印`message`或显示消息框，然后终止应用程序。
该信号将从图形界面线程中发出。

### `[signal] void QQuickWindow::sceneGraphInitialized()`

**作用与语义：**

当场景图初始化时，该信号会发出。
该信号将由场景图渲染线程发出。

### `[signal] void QQuickWindow::sceneGraphInvalidated()`

**作用与语义：**

当场景图失效时，该信号会发出。
该信号意味着所使用的图形渲染上下文已被无效化，所有与该上下文相关的用户资源应被释放。
在使用 OpenGL 渲染时，调用该函数时该窗口的 `QOpenGLContext` 会被绑定。唯一的例外是当原生 OpenGL 在 Qt 控制之外被破坏时，例如通过 EGL_CONTEXT_LOST。
该信号将由场景图渲染线程发出。

### `void QQuickWindow::scheduleRenderJob(QRunnable *job, QQuickWindow::RenderStage stage)`

**作用与语义：**

当该窗口的渲染达到给定`stage`时，调度`job`运行。
这比“一次性”任务中等效信号`QQuickWindow`方便。
窗口会对`job`拥有权，并在工作完成后删除它。
如果渲染在`job`运行前就被关闭，作业将被运行后作为场景图清理的一部分删除。如果窗口从未显示，且在`QQuickWindow`被销毁前没有渲染，所有待处理的作业都会被销毁，且不会调用它们的run()方法。
如果渲染是在不同的线程上进行的，那么工作也会在渲染线程上完成。
如果`stage` `NoStage`，`job`会在渲染线程不忙于渲染帧时尽早执行。如果窗口未被暴露且不可渲染，在作业发布或处理时，作业会被删除且不执行run()方法。如果使用非线程渲染器，作业的run()方法同步执行。使用OpenGL渲染时，OpenGL上下文会在执行任何作业（包括`NoStage`作业）前切换为渲染器的上下文。
注意：该函数不会触发渲染;针对`NoStage`以外的任何阶段的作业都会被存储，直到渲染在其他地方被触发。要强制作业提前运行，请调用`QQuickWindow::update()`;

### `[static] void QQuickWindow::setDefaultAlphaBuffer(bool useAlpha)`

**作用与语义：**

`useAlpha` 规定是否在新创建的窗口上使用 alpha 透明度。
在任何期望创建半透明窗口的应用程序中，在创建第一个`QQuickWindow`之前，必须先将此设置为 true。默认值为 false。

### `[static, since 6.0] void QQuickWindow::setGraphicsApi(QSGRendererInterface::GraphicsApi api)`

**作用与语义：**

请求指定的图形 `api`。
当使用内置默认图形适配时，`api` 指定场景图应使用哪个图形 API（OpenGL、Vulkan、Metal 或 Direct3D）进行渲染。此外，`software` 后端也内置，可通过将 `api` 设置为 `QSGRendererInterface::Software` 来请求。
与只能用来请求特定后端（内置或作为动态加载插件安装）的 `setSceneGraphBackend()` 不同，该功能与更高层次的图形 API 概念相配合。它涵盖了随 Qt Quick 自带的后端，因此在`QSGRendererInterface::GraphicsApi`枚举中有相应的值。
当该函数完全未被调用，且对应的环境变量`QSG_RHI_BACKEND`也未被设置时，场景图将根据平台选择所用图形API。
该函数在仅准备用特定API渲染的应用程序中尤为重要。例如，如果应用程序原生渲染OpenGL或Vulkan，则会确保Qt Quick也使用OpenGL或Vulkan进行渲染。此类应用应在其main()函数中早期调用该函数。
注意：函数调用必须在构建应用程序中的第一个`QQuickWindow`之前完成。图形API之后不能更改。
注意：与`QQuickRenderControl`结合使用时，此规则会有所放宽：可以更改图形API，但前提是所有现有`QQuickRenderControl`和`QQuickWindow`实例均已被销毁。
要查询场景图使用的图形API来渲染，`QSGRendererInterface::graphicsApi()`场景图初始化后，通常在窗口首次可见时或调用`QQuickRenderControl::initialize()`时进行。
要切换回默认行为，即场景图根据平台和其他条件选择图形API，请将`api`设为`QSGRendererInterface::Unknown`。

### `[since 6.0] void QQuickWindow::setGraphicsConfiguration(const QQuickGraphicsConfiguration &config)`

**作用与语义：**

设置该窗口的图形配置。`config`包含场景图在初始化底层图形设备和上下文时可能考虑的各种设置。
此类额外配置，例如指定为Vulkan启用哪些设备扩展，在集成依赖某些扩展的原生图形渲染代码时变得重要且必不可少。与外部3D或VR引擎（如OpenXR）集成时，情况同样如此。
注意：在采用现有图形设备时，`setGraphicsDevice()`忽略了该配置，因为场景图无法控制这些对象的实际构建。
`QQuickGraphicsConfiguration`实例是隐式共享的，可复制，并且可以通过值传递。
警告：在`QQuickWindow`上设置`QQuickGraphicsConfiguration`必须足够早，在该窗口的场景图首次初始化之前。对于屏幕窗口，这意味着调用必须在调用`QQuickWindow`或`QQuickView`调用`show()`之前完成。在`QQuickRenderControl`中，配置必须在调用`initialize()`之前完成。

### `[since 6.0] void QQuickWindow::setGraphicsDevice(const QQuickGraphicsDevice &device)`

**作用与语义：**

为该窗口设置图形设备对象。场景图将使用现有设备、物理设备及`device`指定的其他对象，而非创建新的对象。
该函数常与 `QQuickRenderControl` 和 `setRenderTarget()` 结合使用，以将 Qt 快速渲染重定向到纹理中。
默认构造`QQuickGraphicsDevice`不会以任何方式改变默认行为。一旦通过`QQuickGraphicsDevice`工厂函数（如`QQuickGraphicsDevice::fromDeviceObjects()`）创建的`device`传递入去，且场景图使用匹配的图形API（例如fromDeviceObjects()，即Vulkan），场景图将使用`QQuickGraphicsDevice`封装的现有设备对象（如Vulkan的`VkPhysicalDevice`、`VkDevice`和图形队列族索引）。这使得可以使用同一设备，从而在 Qt Quick 和原生渲染引擎之间共享资源，如缓冲区和纹理。
警告：该函数只能在初始化场景图之前调用，之后调用则无效。实际上，通常意味着在`QQuickRenderControl::initialize()`之前调用。
举例来说，这次使用 Direct3D 的典型应用预期如下：
使用该函数的关键在于确保资源或资源的句柄，如上述示例中的`texture`，同时被外部渲染引擎和场景图渲染器看到并可用。这需要使用相同的图形设备（或使用 OpenGL，OpenGL 上下文）。
`QQuickGraphicsDevice`实例是隐式共享的，可复制，并且可以通过值传递。它们不拥有相关的本地对象（例如示例中的ID3D11Device）。
注意：使用`QQuickRenderControl`并不总是意味着必须调用该函数。当不需要采用现有设备或上下文时，不应调用该函数，场景图会像启用屏幕`QQuickWindow`一样，正常初始化自己的设备和上下文。

**官方示例：**

```cpp
 // native graphics resources set up by a custom D3D rendering engine
 ID3D11Device *device;
 ID3D11DeviceContext *context;
 ID3D11Texture2D *texture;
 ...
 // now to redirect Qt Quick content into 'texture' we could do the following:
 QQuickRenderControl *renderControl = new QQuickRenderControl;
 QQuickWindow *window = new QQuickWindow(renderControl); // this window will never be shown on-screen
 ...
 window->setGraphicsDevice(QQuickGraphicsDevice::fromDeviceAndContext(device, context));
 renderControl->initialize();
 window->setRenderTarget(QQuickRenderTarget::fromD3D11Texture(texture, textureSize);
 ...
```

### `void QQuickWindow::setPersistentGraphics(bool persistent)`

**作用与语义：**

设置是否应保留图形资源（图形设备或上下文、交换链、缓冲区、纹理）至`persistent`。默认值为真。
当调用`releaseResources()`，或者窗口被隐藏（更具体地说，无法渲染）时，一些渲染循环有可能释放所有（而不仅仅是缓存的）图形资源。这可以暂时释放内存，但也意味着渲染引擎在窗口需要再次渲染时，必须对资源进行全面且可能代价高昂的重新初始化。
注意：窗口不可渲染的规则是针对平台和窗口管理器的。
注意：所有图形资源在最后一个`QQuickWindow`被删除时都会释放，无论该设置如何。
注意：这只是提示，不保证会被考虑。
注意：此提示不适用于缓存资源，缓存资源相对便宜，后者易于放弃后再重新创建。因此，调用`releaseResources()`通常会导致释放这些资源，无论提示值如何。

### `void QQuickWindow::setPersistentSceneGraph(bool persistent)`

**作用与语义：**

设置场景图节点和资源是否`persistent`。持久性表示节点和资源无法释放。默认值为`true`。
当调用`releaseResources()`时，当窗口被隐藏（更具体地说，无法渲染），一些渲染循环可以释放场景图节点和相关图形资源。这暂时释放了内存，但也意味着下次窗口渲染时需要重建场景图。
注意：窗口不可渲染的规则是针对平台和窗口管理器的。
注意：无论设置如何，场景图节点和资源在最后一个`QQuickWindow`被删除时都会被释放。
注意：这只是提示，不保证会被考虑。

### `[since 6.0] void QQuickWindow::setRenderTarget(const QQuickRenderTarget &target)`

**作用与语义：**

将该窗口的渲染目标设置为`target`。
`QQuickRenderTarget`作为可渲染的本地对象（最常见的是二维纹理）及其相关元数据（如像素大小）的不透明句柄。
默认构造`QQuickRenderTarget`意味着没有重定向。而通过静态`QQuickRenderTarget`工厂函数创建的有效`target`，则允许重定向Qt Quick场景的渲染：它不再针对与窗口关联的表面的颜色缓冲区，而是针对`target`中指定的纹理或其他图形对象。
例如，假设场景图使用Vulkan进行渲染，可以将其输出重定向到`VkImage`。对于像Vulkan这样的图形API，也必须提供图像布局。`QQuickRenderTarget`实例是隐式共享的，且可复制，且可以通过值传递。但它们不拥有相关的本地对象（例如示例中的VkImage）。
该功能常与`QQuickRenderControl`和隐形`QQuickWindow`结合使用，以将 Qt Quick 内容渲染成纹理，而无需为该`QQuickWindow`创建屏幕原生窗口。
当目标或相关数据（如大小）发生变化时，调用该函数并添加新`QQuickRenderTarget`。构建`QQuickRenderTarget`实例并调用该函数成本较低，但需要注意，设置新的`target`时使用不同的本地对象或其他数据，可能会导致场景图即将渲染下一帧时出现昂贵的初始化步骤。因此，只有在必要时才更改目标。
注意：窗口不拥有`target`中引用的任何本地对象。
注意：调用者有责任确保`target`中提到的本地对象对场景图渲染器同样有效。例如，对于Vulkan、Metal和Direct3D，这意味着纹理或图像是在场景图内部使用的同一图形设备上创建的。因此，当涉及在已有设备或上下文上创建的纹理对象时，该功能通常与`setGraphicsDevice()`结合使用。
注意：在相关图形API中，应用程序必须关注场景图执行的图像布局转换。例如，一旦通过调用该函数将VkImage关联到场景图，其布局在渲染帧时会切换为`VK_IMAGE_LAYOUT_COLOR_ATTACHMENT_OPTIMAL`。
警告：该函数只能从执行渲染的线程中调用。

**官方示例：**

```cpp
 QQuickRenderTarget rt = QQuickRenderTarget::fromVulkanImage(vulkanImage, VK_IMAGE_LAYOUT_PREINITIALIZED, pixelSize);
 quickWindow->setRenderTarget(rt);
```

### `[static] void QQuickWindow::setSceneGraphBackend(const QString &backend)`

**作用与语义：**

请求Qt Quick场景图`backend`。后端可以内置，也可以以动态加载插件的形式安装。
注意：调用函数必须在构建应用程序中的第一个`QQuickWindow`之前完成。之后不能更改。
有关后端列表的更多信息，请参见“在您的应用程序中切换适配”。如果`backend`无效或发生错误，请求将被忽略。
注意：调用该函数等同于设置`QT_QUICK_BACKEND`或`QMLSCENE_DEVICE`环境变量。不过，在生成其他进程的应用中使用该 API 更安全，无需担心环境继承问题。

### `[static] void QQuickWindow::setTextRenderType(QQuickWindow::TextRenderType renderType)`

**作用与语义：**

将Qt Quick中文本类元素的默认渲染类型设置为`renderType`。
注意：设置渲染类型只会影响之后创建的元素;现有元素的渲染类型不会被修改。

### `[override virtual protected] void QQuickWindow::showEvent(QShowEvent *)`

**作用与语义：**

重实现自：`QWindow::showEvent`（QShowEvent *ev）。

### `[since 6.6] QRhiSwapChain *QQuickWindow::swapChain() const`

**作用与语义：**

返回该窗口使用的`QRhiSwapChain`（如果有的话）。
注意：只有由标准渲染循环支持的屏幕窗口（如`basic`或`threaded`）才会有交换链。否则返回的值为空。例如，当窗口与`QQuickRenderControl`一起使用时，结果总是空的。

### `[override virtual protected] void QQuickWindow::tabletEvent(QTabletEvent *event)`

**作用与语义：**

重实现自：`QWindow::tabletEvent`（QTabletEvent *ev）。

### `[static] QQuickWindow::TextRenderType QQuickWindow::textRenderType()`

**作用与语义：**

返回 Qt Quick 中类似文本元素的渲染类型。默认是 `QQuickWindow::QtTextRendering`。

### `[slot] void QQuickWindow::update()`

**作用与语义：**

安排窗口渲染另一帧。
调用 QQuickWindow：：update() 与 `QQuickItem::update()` 不同，它总是触发重绘，无论底层场景图是否发生变化。

### `[override virtual protected] void QQuickWindow::wheelEvent(QWheelEvent *event)`

**作用与语义：**

接收窗口上的滚轮事件，并按指针位置把它分派给 Qt Quick 项和输入处理器。子类处理后应接受事件；未处理时调用基类，使 Flickable、WheelHandler 等 QML 组件仍能响应。

### `struct GraphicsStateInfo`

**作用与语义：**

描述 restartExternalCommands() 调用时 RHI 的一些图形状态。

### `enum CreateTextureOption { TextureHasAlphaChannel, TextureHasMipmaps, TextureOwnsGLTexture, TextureCanUseAtlas, TextureIsOpaque }`

**作用与语义：**

CreateTextureOption 枚举用于自定义纹理的封装方式。
- `QQuickWindow::TextureHasAlphaChannel`: `0x0001`；纹理具有 alpha 通道，并应使用混合方式绘制。
- `QQuickWindow::TextureHasMipmaps`: `0x0002`；纹理具有 mipmap，可以在启用 mipmapping 的情况下绘制。
- `QQuickWindow::TextureOwnsGLTexture`: `0x0004`；从 Qt 6.0 起，此标志在实际中不使用并被忽略。原生图形资源的所有权无法转移到封装的 `QSGTexture`，因为 Qt Quick 可能没有关于如何释放此类对象及其关联内存的必要详细信息。
- `QQuickWindow::TextureCanUseAtlas`: `0x0008`；图像可以上传到纹理图集。
- `QQuickWindow::TextureIsOpaque`: `0x0010`；纹理在 `QSGTexture::hasAlphaChannel()` 返回 false，并且不会进行混合。此标志在 Qt 5.6 中添加。
CreateTextureOptions 类型是 QFlags<CreateTextureOption> 的 typedef。它存储 CreateTextureOption 值的按位或组合。

### `flags CreateTextureOptions`

**作用与语义：**

CreateTextureOption 枚举用于自定义纹理的封装方式。
- `QQuickWindow::TextureHasAlphaChannel`: `0x0001`；纹理具有 alpha 通道，并应使用混合方式绘制。
- `QQuickWindow::TextureHasMipmaps`: `0x0002`；纹理具有 mipmap，可以在启用 mipmapping 的情况下绘制。
- `QQuickWindow::TextureOwnsGLTexture`: `0x0004`；从 Qt 6.0 起，此标志在实际中不使用并被忽略。原生图形资源的所有权无法转移到封装的 `QSGTexture`，因为 Qt Quick 可能没有关于如何释放此类对象及其关联内存的必要详细信息。
- `QQuickWindow::TextureCanUseAtlas`: `0x0008`；图像可以上传到纹理图集。
- `QQuickWindow::TextureIsOpaque`: `0x0010`；纹理在 `QSGTexture::hasAlphaChannel()` 返回 false，并且不会进行混合。此标志在 Qt 5.6 中添加。
CreateTextureOptions 类型是 QFlags<CreateTextureOption> 的 typedef。它存储 CreateTextureOption 值的按位或组合。

### `QQuickItem * activeFocusItem() const`

**作用与语义：**

该属性包含当前具有主动焦点的物品;若没有当前焦点的物品则`null`。

**如何使用：** 调用 `activeFocusItem()` 读取当前值；它不会修改应用状态。

### `QColor color() const`

**作用与语义：**

该属性保留用于清除每帧开始时颜色缓冲区的颜色。
默认情况下，透明色是白色。

**如何使用：** 调用 `color()` 读取当前值；它不会修改应用状态。

### `QQuickItem * contentItem() const`

**作用与语义：**

该属性包含场景的不可见根元素。
一个`QQuickWindow`总是有一个包含其所有内容的不可见根项。要将物品添加到该窗口，请将这些项重新为 contentItem 或场景中的现有项。

**如何使用：** 调用 `contentItem()` 读取当前值；它不会修改应用状态。

### `void setColor(const QColor &color)`

**作用与语义：**

该属性保留用于清除每帧开始时颜色缓冲区的颜色。
默认情况下，透明色是白色。

**如何使用：** 调用 `setColor(...)` 修改 `color`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void activeFocusItemChanged()`

**作用与语义：**

该属性包含当前具有主动焦点的物品;若没有当前焦点的物品则`null`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `activeFocusItem` 的变化，不要把它当作普通函数主动调用。

### `void colorChanged(const QColor &)`

**作用与语义：**

该属性保留用于清除每帧开始时颜色缓冲区的颜色。
默认情况下，透明色是白色。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `color` 的变化，不要把它当作普通函数主动调用。

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
