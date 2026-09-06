# QQuickRhiItemRenderer

> Qt 6.11.1 · Qt Quick

## 1. 先建立直觉

**一句话定位：** `QQuickRhiItemRenderer` 是 QML 属性绑定与场景图机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Quick 面向 QML/场景图界面，提供可视项、动画、输入和高性能界面基础设施。

### 这是什么

`QQuickRhiItemRenderer` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QQuickRhiItemRenderer>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Quick)
target_link_libraries(mytarget PRIVATE Qt6::Quick)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

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

- `QQuickRhiItemRenderer()`
- `virtual ~QQuickRhiItemRenderer()`

### 保护函数

- `QRhiTexture * colorTexture() const`
- `QRhiRenderBuffer * depthStencilBuffer() const`
- `virtual void initialize(QRhiCommandBuffer *cb) = 0`
- `QRhiRenderBuffer * msaaColorBuffer() const`
- `virtual void render(QRhiCommandBuffer *cb) = 0`
- `QRhiRenderTarget * renderTarget() const`
- `QRhiTexture * resolveTexture() const`
- `QRhi * rhi() const`
- `virtual void synchronize(QQuickRhiItem *item) = 0`
- `void update()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QQuickRhiItemRenderer::QQuickRhiItemRenderer()`

**作用与语义：**

构建一个新的渲染器。
当图形线程被阻塞时，该函数在渲染线程中调用。

### `[virtual noexcept] QQuickRhiItemRenderer::~QQuickRhiItemRenderer()`

**作用与语义：**

当`QQuickRhiItem`项的场景图资源清理完毕时，渲染器会自动被删除。
该函数在渲染线程中被调用。
在某些条件下，渲染器对象被销毁后再重新创建是正常且预期的。这是因为渲染器的生命周期实际上遵循底层场景图节点。例如，当将`QQuickRhiItem`对象的父节点设置为另一个`QQuickWindow`时，场景图节点都会被丢弃并因窗口变化而重新创建。这也涉及丢弃并创建新的`QQuickRhiItemRenderer`。
与`QRhiWidget`不同，`QQuickRhiItemRenderer`不需要为通过`QRhi`创建的图形资源实现额外的代码路径来释放（或提前释放）。只需释放解构器中的所有内容，或依赖智能指针即可。

### `[protected] QRhiTexture *QQuickRhiItemRenderer::colorTexture() const`

**作用与语义：**

返回纹理，作为该物品的颜色缓冲。
只能从`initialize()`和`render()`打电话。
与深度模板缓冲区和`QRhiRenderTarget`不同，这个纹理始终可用，由`QQuickRhiItem`管理，与`isAutoRenderTargetEnabled`的值无关。
注意：当`sampleCount`大于1且启用多采样抗锯齿时，返回值为`nullptr`。相反，通过调用`msaaColorBuffer()`查询`QRhiRenderBuffer`。
注意：背景纹理大小和采样数量也可以通过`renderTarget()`返回的`QRhiRenderTarget`查询。这比从`QRhiTexture`或 `QRhiRenderBuffer`查询更方便、更紧凑，因为无论是否使用多重采样，它都能正常工作。

### `[protected] QRhiRenderBuffer *QQuickRhiItemRenderer::depthStencilBuffer() const`

**作用与语义：**

返回用于物品渲染的深度模板缓冲区。
只能从`initialize()`和 `render()` 打电话。
仅在`isAutoRenderTargetEnabled` `true`时才可用。否则返回的值`nullptr`，需要重新实现`initialize()`来创建和管理深度模板缓冲区和`QRhiTextureRenderTarget`。

### `[pure virtual protected] void QQuickRhiItemRenderer::initialize(QRhiCommandBuffer *cb)`

**作用与语义：**

当项目第一次初始化时，或者相关纹理的大小、格式或采样数发生变化时，或由于任何原因 `QRhi` 或纹理发生变化时，将调用此函数。此函数预期要维护（如果尚未创建则创建，如果大小已更改则调整并重建）渲染代码中 `render()` 使用的图形资源。
要查询 `QRhi`、`QRhiTexture` 及其他相关对象，请调用 `rhi()`、`colorTexture()`、`depthStencilBuffer()` 和 `renderTarget()`。
当项目大小发生变化时，`QRhi` 对象、颜色缓冲纹理和深度模板缓冲对象仍与之前是相同实例（因此 getter 返回相同指针），但颜色和深度/模板缓冲很可能已重建，这意味着 `size` 和底层原生纹理资源可能与上一次调用时不同。
重新实现时还应准备 `QRhi` 对象和颜色缓冲纹理在多次调用此函数之间可能会发生变化。例如，当项目重新设置父对象使其属于新的 `QQuickWindow` 时，此后调用此函数时，`QRhi` 及 `QQuickRhiItem` 管理的所有相关资源将是不同的实例。因此，重要的是先前由子类创建的所有现有 `QRhi` 资源必须销毁，因为它们属于先前的 `QRhi`，已经不应再使用。
当 `isAutoRenderTargetEnabled` 为 `true`（默认值）时，会自动创建并管理一个深度-模板 `QRhiRenderBuffer` 和与 `colorTexture()`（或 `msaaColorBuffer()`）及深度-模板缓冲相关联的 `QRhiTextureRenderTarget`。initialize() 和 `render()` 的重新实现可通过 `depthStencilBuffer()` 和 `renderTarget()` 查询这些对象。当 `isAutoRenderTargetEnabled` 设置为 `false` 时，这些对象将不再自动创建和管理。相反，由 initialize() 的实现来创建缓冲区并按需要设置渲染目标。当手动管理渲染目标的额外颜色或深度-模板附件时，其大小和采样数必须始终与 `colorTexture()`（或 `msaaColorBuffer()`）保持一致，否则可能会发生渲染或 3D API 验证错误。
子类创建的图形资源应在子类的析构函数实现中释放。
`cb` 是当前帧的 `QRhiCommandBuffer`。调用该函数时帧正在被记录，但没有处于活动的渲染通道中。提供命令缓冲区主要是为了允许入队资源更新，而无需延迟到 `render()`。
如果存在渲染线程，则此函数在渲染线程上调用。

### `[protected] QRhiRenderBuffer *QQuickRhiItemRenderer::msaaColorBuffer() const`

**作用与语义：**

返回作为该项目多重采样颜色缓冲区的渲染缓冲区。
只能在`initialize()`和`render()`中调用。
当`sampleCount`大于1，从而启用多重采样反采样时，返回的`QRhiRenderBuffer`采样计数匹配，并作为颜色缓冲区。用于渲染到该缓冲区的图形管线必须使用相同的采样计数创建，深度模板缓冲区的采样计数也必须匹配。多采样内容预计会被解析为从`resolveTexture()`返回的纹理中。当`isAutoRenderTargetEnabled` `true`时，`renderTarget()`会自动设置，方法是设置msaaColorBuffer()作为颜色附件0的`renderbuffer`，`resolveTexture()`作为`resolveTexture`。
当MSAA未被使用时，返回值`nullptr`。那就用`colorTexture()`吧。
根据底层的3D图形API，多采样纹理和采样计数大于1的彩色渲染缓冲区之间可能没有实际区别（`QRhi`可能两者都映射到同一原生资源类型）。不过，一些较早的API可能会区分纹理和渲染缓冲区。为了支持OpenGL ES 3.0，在多采样渲染缓冲区可用但多采样纹理不存在的情况下，`QQuickRhiItem`总是通过使用多采样`QRhiRenderBuffer`作为颜色附件来执行MSAA（从不使用多采样`QRhiTexture`）。
注意：背景纹理的大小和采样计数也可以通过`renderTarget()`返回的`QRhiRenderTarget`查询。这比从`QRhiTexture`或 `QRhiRenderBuffer`查询更方便、更简洁，因为无论是否使用多重采样都能正常工作。

### `[pure virtual protected] void QQuickRhiItemRenderer::render(QRhiCommandBuffer *cb)`

**作用与语义：**

当需要更新后端颜色缓冲区内容时调用。 在此函数被调用之前，`initialize()` 至少会被调用一次。 要请求更新，请在从 QML 或在主/GUI 线程的 C 代码（例如在属性设置器中）调用时，使用 `QQuickItem::update()`，或者在 `QQuickRhiItemRenderer` 回调中调用时使用 `update()`。 在 render() 中调用 `QQuickRhiItemRenderer` 的 `update()` 将导致持续触发更新。 `cb` 是当前帧的 `QRhiCommandBuffer`。 该函数在记录帧时被调用，但没有活动的渲染通道。 如果存在渲染线程，则此函数在渲染线程上调用。

### `[protected] QRhiRenderTarget *QQuickRhiItemRenderer::renderTarget() const`

**作用与语义：**

返回必须在`render()`重实现中与`QRhiCommandBuffer::beginPass()`一起使用的渲染目标对象。
只能从`initialize()`和`render()`调用。
仅在`isAutoRenderTargetEnabled` `true`时可用。否则返回的值将被`nullptr`，需要重新实现`initialize()`来创建和管理深度模板缓冲区和`QRhiTextureRenderTarget`。
创建图形流水线时需要`QRhiRenderPassDescriptor`。可以通过调用 `renderPassDescriptor()` 从返回的`QRhiTextureRenderTarget`中查询。
注意：返回的`QRhiTextureRenderTarget`总是报告`devicePixelRatio()` `1`。这是因为只有交换链和相关窗口有设备像素比例的概念，而非纹理，且这里的渲染目标总是指纹理。如果屏幕上的缩放因子对渲染有关联，请通过物品的`window()->effectiveDevicePixelRatio()`在`synchronize()`中查询并存储。这样做时，始终优先使用`effectiveDevicePixelRatio()`而非基类的`devicePixelRatio()`。

### `[protected] QRhiTexture *QQuickRhiItemRenderer::resolveTexture() const`

**作用与语义：**

返回非多采样纹理，多采样内容被解析为该纹理。
当未启用多重采样抗锯齿时，结果会被`nullptr`。
只能从`initialize()`和 `render()` 打电话。
启用MSAA时，该纹理会被物品底层场景图节点在Qt Quick主渲染过程中纹理四边形时使用。然而，`QQuickRhiItemRenderer`的渲染必须针对`msaaColorBuffer()`返回的（多重采样）`QRhiRenderBuffer`。当`isAutoRenderTargetEnabled`被`true`时，这由`renderTarget()`返回的`QRhiRenderTarget`处理。否则，子类代码需正确配置带有色彩缓冲和解析纹理的渲染目标对象。

### `[protected] QRhi *QQuickRhiItemRenderer::rhi() const`

**作用与语义：**

返回当前`QRhi`对象。
只能从`initialize()`和 `render()` 打电话。

### `[pure virtual protected] void QQuickRhiItemRenderer::synchronize(QQuickRhiItem *item)`

**作用与语义：**

该函数在渲染线程（如果有）调用，而主线程/图形界面线程被阻塞。它从`item`的同步步骤调用，允许读写属于主线程和渲染线程的数据。通常，存储在`QQuickRhiItem`中的属性值会复制到`QQuickRhiItemRenderer`中，以便渲染线程和主线程并行工作后可以安全地读取`render()`。

### `[protected] void QQuickRhiItemRenderer::update()`

**作用与语义：**

当需要更新离屏颜色缓冲区的内容时调用此函数。（即请求再次调用 `render()`；调用将在稍后进行，并且更新通常限于演示速率）可以在 `render()` 中调用此函数以安排更新。注意：此函数应在渲染器内部使用。要在 GUI 线程上更新项，请使用 `QQuickRhiItem::update()`。

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

`QQuickRhiItemRenderer` 所属机制类型：QML 属性绑定与场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
