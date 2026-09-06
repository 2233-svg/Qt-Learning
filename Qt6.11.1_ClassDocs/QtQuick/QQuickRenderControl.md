# QQuickRenderControl

> Qt 6.11.1 · Qt Quick

## 1. 先建立直觉

**一句话定位：** `QQuickRenderControl` 是 QML 属性绑定与场景图机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Quick 面向 QML/场景图界面，提供可视项、动画、输入和高性能界面基础设施。

### 这是什么

`QQuickRenderControl` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QQuickRenderControl>`
- 继承自：QObject
- 直接派生类：未在类页中列出

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

### 公有函数

- `QQuickRenderControl(QObject *parent = nullptr)`
- `virtual ~QQuickRenderControl() override`
- `(since 6.0) void beginFrame()`
- `(since 6.6) QRhiCommandBuffer * commandBuffer() const`
- `(since 6.0) void endFrame()`
- `(since 6.0) bool initialize()`
- `void invalidate()`
- `void polishItems()`
- `void prepareThread(QThread *targetThread)`
- `void render()`
- `virtual QWindow * renderWindow(QPoint *offset)`
- `(since 6.6) QRhi * rhi() const`
- `(since 6.0) int samples() const`
- `(since 6.0) void setSamples(int sampleCount)`
- `bool sync()`
- `(since 6.0) QQuickWindow * window() const`

### 信号

- `void renderRequested()`
- `void sceneChanged()`

### 静态公有成员

- `QWindow * renderWindowFor(QQuickWindow *win, QPoint *offset = nullptr)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[explicit] QQuickRenderControl::QQuickRenderControl(QObject *parent = nullptr)`

**作用与语义：**

构造一个 QQuickRenderControl 对象，父对象为 `parent`。

### `[override virtual noexcept] QQuickRenderControl::~QQuickRenderControl()`

**作用与语义：**

销毁实例。释放所有场景图资源。

### `[since 6.0] void QQuickRenderControl::beginFrame()`

**作用与语义：**

指定图形帧的起始时间。调用 `sync()` 或 `render()` 必须用 benstartFrame() 和 `endFrame()` 的调用包围。
与早期仅支持OpenGL的Qt 5不同，使用其他图形API渲染需要更明确的帧起点和结束点。当手动通过`QQuickRenderControl`驱动渲染环时，现在由`QQuickRenderControl`用户指定这些点。
典型的更新步骤，包括将渲染初始化为现有纹理，可能如下。示例片段假设使用 Direct3D 11，但同样的概念也适用于其他图形 API。
注意：使用`software` Quick 适配时，无需也绝不调用该函数。
注意：内部 berentFrame() 和 `endFrame()` 分别调用 `beginOffscreenFrame()` 和 `endOffscreenFrame()`。这意味着调用该函数时，不能在`QRhi`上记录帧（无论是屏幕外帧还是基于交换链的帧）。

**官方示例：**

```cpp
 if (!m_quickInitialized) {
     m_quickWindow->setGraphicsDevice(QQuickGraphicsDevice::fromDeviceAndContext(m_engine->device(), m_engine->context()));

     if (!m_renderControl->initialize())
         qWarning("Failed to initialize redirected Qt Quick rendering");

     m_quickWindow->setRenderTarget(QQuickRenderTarget::fromNativeTexture({ quint64(m_res.texture), 0 },
                                                                          QSize(QML_WIDTH, QML_HEIGHT),
                                                                          SAMPLE_COUNT));

     m_quickInitialized = true;
 }

 m_renderControl->polishItems();

 m_renderControl->beginFrame();
 m_renderControl->sync();
 m_renderControl->render();
 m_renderControl->endFrame(); // Qt Quick's rendering commands are submitted to the device context here
```

### `[since 6.6] QRhiCommandBuffer *QQuickRenderControl::commandBuffer() const`

**作用与语义：**

返回当前的命令缓冲区。
一旦调用`beginFrame()`，会自动设置`QRhiCommandBuffer`。这就是 Qt 快速场景图使用的命令缓冲区，但在某些情况下，应用程序也可能想查询它，例如发送资源更新（例如纹理回读）。
返回的命令缓冲区引用应仅在`beginFrame()`和`endFrame()`之间使用。有特定例外，例如在`endFrame()`后、下一个`beginFrame()`之前调用命令缓冲区上的`lastCompletedGpuTime()`是有效的。
注意：该函数不适用，使用Qt Quick的`software`适配时返回空函数。

### `[since 6.0] void QQuickRenderControl::endFrame()`

**作用与语义：**

指定图形帧的结尾。调用`sync()`或`render()`必须通过调用`beginFrame()`和endFrame()来包裹。
当调用该函数时，场景图中排队的任何图形命令都会提交到上下文队列或命令队列中，视情况而定。
注意：使用`software` Quick 适配时，无需也绝不调用该函数。

### `[since 6.0] bool QQuickRenderControl::initialize()`

**作用与语义：**

初始化场景图资源。当使用 Vulkan、Metal、OpenGL 或 Direct3D 等图形 API 进行 Qt Quick 渲染时，调用该函数时`QQuickRenderControl`会设置合适的渲染引擎。只要`QQuickRenderControl`存在，这个渲染基础设施就存在。
要控制 Qt Quick 使用哪些图形 API，请用 `QSGRendererInterface`：GraphicsApi 常量调用 `QQuickWindow::setGraphicsApi()`。必须在调用该函数之前完成此操作。
为了防止场景图创建自己的设备和上下文对象，请指定合适的`QQuickGraphicsDevice`，通过调用`QQuickWindow::setGraphicsDevice()`来包裹现有图形对象。
要配置启用哪些设备扩展（例如Vulkan），请在此功能之前调用`QQuickWindow::setGraphicsConfiguration()`。
注意：使用Vulkan时，`QQuickRenderControl`不会自动创建`QVulkanInstance`。相反，应用程序负责创建合适的`QVulkanInstance`并将其与`QQuickWindow`关联。在初始化`QVulkanInstance`之前，强烈建议通过调用静态函数`QQuickGraphicsConfiguration::preferredInstanceExtensions()`查询Qt Quick所需的实例扩展列表，并将返回的列表传递给`QVulkanInstance::setExtensions()`。
成功时回报`true`，`false`其他情况。
注意：使用`software` Qt Quick 适配时，无需也绝不调用该函数。
默认的 Qt Quick 适配功能会创建新的 `QRhi` 对象，类似于未使用 `QQuickRenderControl` 时的屏幕`QQuickWindow`。要让新的 `QRhi` 对象采用某些现有设备或上下文资源（例如使用现有 `QOpenGLContext` 而非创建新资源），如上所述使用 `QQuickWindow::setGraphicsDevice()`。当应用程序希望让 Qt Quick 渲染使用已有的 `QRhi` 对象时，也可以通过 `QQuickGraphicsDevice::fromRhi()` 实现。当这样的`QQuickGraphicsDevice`被设置，引用已存在的`QRhi`时，initialize()中不会创建新的专用`QRhi`对象。

### `void QQuickRenderControl::invalidate()`

**作用与语义：**

停止渲染，释放资源。
这相当于真实`QQuickWindow`窗户被隐藏时的清理操作。
该函数由解构函数调用。因此通常不需要直接调用它。
一旦调用了 invalidate()，可以通过再次调用 `initialize()` 来重用`QQuickRenderControl`实例。
注意：该函数不考虑 QQuickWindow：:p ersistentSceneGraph() 或 QQuickWindow：:p ersistentGraphics()这意味着上下文特定的资源始终会被释放。

### `void QQuickRenderControl::polishItems()`

**作用与语义：**

该函数应尽快调用，直到`sync()`。在线程场景中，渲染可以与该函数并行进行。

### `void QQuickRenderControl::prepareThread(QThread *targetThread)`

**作用与语义：**

准备在GUI线程外渲染Qt Quick场景。
`targetThread` 指定了同步和渲染将进行的线程。在单一线程场景中无需调用该函数。

### `void QQuickRenderControl::render()`

**作用与语义：**

用当前上下文渲染场景图。

### `[signal] void QQuickRenderControl::renderRequested()`

**作用与语义：**

当需要渲染场景图时，会发出该信号。无需调用`sync()`。
注意：避免在该信号发出时直接触发渲染。相反，建议通过使用定时器等方式来延迟渲染。这将带来更好的性能。

### `[virtual] QWindow *QQuickRenderControl::renderWindow(QPoint *offset)`

**作用与语义：**

在子类中重新实现，返回该渲染控件渲染的真实窗口。
如果`offset`非空，则设置为窗口内控件的偏移量。
注意：虽然不是强制的，但重新实现此功能对于支持不同设备像素比例的多屏幕以及正确定位从QML打开的弹窗至关重要。因此强烈建议将其分成子类。

### `[static] QWindow *QQuickRenderControl::renderWindowFor(QQuickWindow *win, QPoint *offset = nullptr)`

**作用与语义：**

返回渲染时`win`的真实窗口（如果有的话）。
如果`offset`非空，则将其设置为窗口内渲染的偏移量。

### `[since 6.6] QRhi *QQuickRenderControl::rhi() const`

**作用与语义：**

返回该`QQuickRenderControl`关联的`QRhi`。
注意：`QRhi`仅在`initialize()`成功完成时存在。在此之前返回值为空。
注意：该函数不适用，使用Qt Quick的`software`适配时返回空值。

### `[since 6.0] int QQuickRenderControl::samples() const`

**作用与语义：**

返回当前采样计数。1或0表示不进行多重采样。

### `[signal] void QQuickRenderControl::sceneChanged()`

**作用与语义：**

当场景图更新时会发出该信号，意味着需要调用`polishItems()`和`sync()`。如果`sync()`返回为真，则需要调用`render()`。
注意：避免在发出该信号时直接触发抛光、同步和渲染。相反，建议通过使用定时器等方式延迟。这将带来更好的性能。

### `[since 6.0] void QQuickRenderControl::setSamples(int sampleCount)`

**作用与语义：**

设置用于多重采样的采样数量。当`sampleCount`为0或1时，多重采样被禁用。
注意：该函数总是与多采样渲染目标结合使用，这意味着`sampleCount`必须匹配传递给QQuickRenderTarget：：fromNativeTexture()的采样计数，而QQuickRenderTarget：：fromNativeTexture()又必须与原生纹理的采样计数匹配。

### `bool QQuickRenderControl::sync()`

**作用与语义：**

该函数用于同步QML场景与渲染场景图。
如果使用专用渲染线程，应在此调用期间阻塞GUI线程。
如果同步改变了场景图，则返回为真。

### `[since 6.0] QQuickWindow *QQuickRenderControl::window() const`

**作用与语义：**

返回该`QQuickRenderControl`关联的`QQuickWindow`。
注意：在构造`QQuickWindow`时，`QQuickRenderControl`会关联到一个`QQuickWindow`。该函数的返回值在此之前为零。

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

`QQuickRenderControl` 所属机制类型：QML 属性绑定与场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
