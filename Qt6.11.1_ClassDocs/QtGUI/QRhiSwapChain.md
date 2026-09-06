# QRhiSwapChain

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QRhiSwapChain` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <rhi/qrhi.h>`
- 继承自：QRhiResource
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS GuiPrivate)
target_link_libraries(mytarget PRIVATE Qt6::GuiPrivate)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

### 状态、生命周期和线程

**生命周期：** 先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

**状态与结果：** 把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

**线程与事件循环：** 如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

## 3. 直接使用

围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum Flag { SurfaceHasPreMulAlpha, SurfaceHasNonPreMulAlpha, sRGB, UsedAsTransferSource, NoVSync, MinimalBufferCount }`
- `flags Flags`
- `enum Format { SDR, HDRExtendedSrgbLinear, HDR10, HDRExtendedDisplayP3Linear }`
- `enum StereoTargetBuffer { LeftBuffer, RightBuffer }`

### 公有函数

- `virtual bool createOrResize() = 0`
- `virtual QRhiCommandBuffer * currentFrameCommandBuffer() = 0`
- `virtual QRhiRenderTarget * currentFrameRenderTarget() = 0`
- `virtual QRhiRenderTarget * currentFrameRenderTarget(QRhiSwapChain::StereoTargetBuffer targetBuffer)`
- `QSize currentPixelSize() const`
- `QRhiRenderBuffer * depthStencil() const`
- `QRhiSwapChain::Flags flags() const`
- `QRhiSwapChain::Format format() const`
- `virtual QRhiSwapChainHdrInfo hdrInfo()`
- `virtual bool isFormatSupported(QRhiSwapChain::Format f) = 0`
- `virtual QRhiRenderPassDescriptor * newCompatibleRenderPassDescriptor() = 0`
- `QRhiSwapChainProxyData proxyData() const`
- `QRhiRenderPassDescriptor * renderPassDescriptor() const`
- `int sampleCount() const`
- `void setDepthStencil(QRhiRenderBuffer *ds)`
- `void setFlags(QRhiSwapChain::Flags f)`
- `void setFormat(QRhiSwapChain::Format f)`
- `void setProxyData(const QRhiSwapChainProxyData &d)`
- `void setRenderPassDescriptor(QRhiRenderPassDescriptor *desc)`
- `void setSampleCount(int samples)`
- `(since 6.9) void setShadingRateMap(QRhiShadingRateMap *map)`
- `void setWindow(QWindow *window)`
- `(since 6.9) QRhiShadingRateMap * shadingRateMap() const`
- `virtual QSize surfacePixelSize() = 0`
- `QWindow * window() const`

### 重实现的公有函数

- `virtual QRhiResource::Type resourceType() const override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QRhiSwapChain::Flagflags QRhiSwapChain::Flags`

**作用与语义：**

描述交换链属性的标志值。
- `QRhiSwapChain::SurfaceHasPreMulAlpha`：`1 << 0`;表示目标表面具有预乘 alpha 的透明性。例如，当目标`QWindow`启用 alpha 通道时，Qt Quick 就是用这个方式，因为场景图的 rendrerer 总是输出 alpha 乘以红、绿、蓝三色的片段。为确保各平台行为一致，每当交换链上设置该标志时，目标`QWindow`上始终将 `QSurfaceFormat::alphaBufferSize()` 设置为非零值。
- `QRhiSwapChain::SurfaceHasNonPreMulAlpha`：`1 << 1`;表示目标表面具有非预乘法alpha的透明性。请注意，如果系统合成器总是预期预乘法alpha的内容，某些系统可能不支持此功能。在这种情况下，使用该标志集的行为应等价于SurfaceHasPreMulAlpha。
- `QRhiSwapChain::sRGB`：`1 << 2`;请求为交换链的颜色缓冲区和/或渲染目标视图选择 sRGB 格式（如适用）。注意，这意味着所有针对该交换链的内容都会启用 sRGB 帧缓冲区更新和混合功能，且无法选择退出。对于 OpenGL，还应在`QWindow` `QSurfaceFormat`上设置 `sRGBColorSpace`。仅在交换链格式设置为 `QRhiSwapChain::SDR` 时才适用。
- `QRhiSwapChain::UsedAsTransferSource`：`1 << 3`;表示交换链将作为`QRhiResourceUpdateBatch::readBackTexture()`中回读的源。
- `QRhiSwapChain::NoVSync`：`1 << 4`;请求禁用等待垂直同步，同时避免限制渲染线程。该行为是后端特定的，仅适用于可控制的部分。有些人可能会完全忽略该请求。对于OpenGL，可以尝试通过`QSurfaceFormat::setSwapInterval()`将`QWindow`的交换间隔设置为0。
- `QRhiSwapChain::MinimalBufferCount`：`1 << 5`;创建交换链的请求，缓冲区数最小，实际上是2个，除非图形实现的最低缓冲数更高。仅适用于后端，且该控制可通过图形API实现，例如Vulkan。默认情况下，后端决定请求缓冲区数（实际上几乎总是2或3），这与应用程序无关。然而，例如在Vulkan上，后端通常偏好较高的缓冲区数（3），以避免移动设备上某些Vulkan实现出现异常性能问题。在某些平台上，强制减少缓冲区数（2）可能有益，因此该标志允许强制执行。注意，所有这些都不会影响保持在飞行中的帧数，因此CPU（`QRhi`）仍然会在最多比GPU领先`N - 1`帧时准备帧，即使交换链映像缓冲区计数大于`N`。（`N` = `QRhi::FramesInFlight`，通常为2）。
Flags 类型是 QFlags 的 typedef<Flag>。它存储 Flag 值的 OR 组合。

### `enum QRhiSwapChain::Format`

**作用与语义：**

描述掉期链格式。默认格式为SDR。
该枚举用于`isFormatSupported()`，提前检查平台及其窗口界面是否支持以该格式创建交换链，并与`setFormat()`配合，在首次调用`createOrResize()`前设置交换链中的请求格式。
- `QRhiSwapChain::SDR`：`0`;8位RGBA或BGRA，具体取决于后端和平台。特别是在OpenGL ES中，平台可能提供少于8位（例如由于EGL和`QSurfaceFormat`选择565或444格式——这超出`QRhi`控制范围）。标准动态范围。可与设置`QRhiSwapChain::sRGB`标志结合使用。
- `QRhiSwapChain::HDRExtendedSrgbLinear`：`1`;16位浮点RGBA，高动态范围，扩展线性sRGB（scRGB）色彩空间。这涉及Rec. 709原色（与SDR/sRGB相同）和线性色彩。窗口系统对显示的原生色彩空间（如HDR10）进行转换。在Windows上，这是系统合成器的标准色彩空间，也是桌面平台上HDR交换链的推荐格式。
- `QRhiSwapChain::HDR10`：`2`;10位无符号int RGB或BGR，2位alpha，高动态范围，HDR10（2020年修订）色彩空间，采用ST2084 PQ传递函数。
- `QRhiSwapChain::HDRExtendedDisplayP3Linear`：`3`;16位浮点RGBA，高动态范围，扩展线性显示P3色彩空间。iOS和VisionOS等平台上HDR的主要选择。

### `enum QRhiSwapChain::StereoTargetBuffer`

**作用与语义：**

选择用于立体交换链的回缓冲区。
- `QRhiSwapChain::LeftBuffer`：`0`
- `QRhiSwapChain::RightBuffer`：`1`

### `[pure virtual] bool QRhiSwapChain::createOrResize()`

**作用与语义：**

如果还没做，创建掉链，并调整掉链缓冲区大小以匹配当前目标曲面大小。每当目标曲面大小与之前不同时调用此值。
注意：只有在需要完全释放掉期链时才调用`destroy()`，通常是在`QPlatformSurfaceEvent::SurfaceAboutToBeDestroyed`时。要进行调整大小，只需调用createOrResize()。
成功时返回`true`，`false`图形操作失败时返回。无论返回值如何，调用`destroy()`始终是安全的。

### `[pure virtual] QRhiCommandBuffer *QRhiSwapChain::currentFrameCommandBuffer()`

**作用与语义：**

返回一个命令缓冲区，可以在`beginFrame`-`endFrame`块内记录渲染命令和资源更新，假设通过该交换链调用了beginFrame()。
注意：返回的对象在 endFrame() 之后也有效，直到下一个 beginFrame()，但返回的命令缓冲区不应用于记录任何命令。相反，它可以用于查询帧（或之前帧）收集的数据，例如调用 `lastCompletedGpuTime()`。
注意：该值不得在帧间缓存和重复使用。调用者不应在再次调用`beginFrame()`后保留返回对象。相反，应通过调用该函数再次查询命令缓冲对象。

### `[pure virtual] QRhiRenderTarget *QRhiSwapChain::currentFrameRenderTarget()`

**作用与语义：**

返回一个渲染目标，可用于与 beginPass() 一起使用，以渲染交换链当前的回缓冲区。仅在调用 bestartFrame() 的 `QRhi::beginFrame()` - `QRhi::endFrame()` 块内有效。
注意：该值不得在帧间缓存并重复使用。

### `[virtual] QRhiRenderTarget *QRhiSwapChain::currentFrameRenderTarget(QRhiSwapChain::StereoTargetBuffer targetBuffer)`

**作用与语义：**

返回一个渲染目标，可配合 beginPass() 来渲染到交换链的左侧或右侧后缓冲区。这种重载应仅用于立体渲染，即当关联`QWindow`有两个颜色缓冲区，分别对应一只眼睛，而非仅一个时。
当不支持立体渲染时，返回值将成为默认目标。除了 Metal，所有硬件后端都支持它，并且与 `QSurfaceFormat::StereoBuffers` 结合，前提是图形和显示驱动栈在运行时支持它。Metal 和 Null 后端会从这种重载中返回默认渲染目标。
注意：该值不得在帧间缓存并重复使用。

### `QSize QRhiSwapChain::currentPixelSize() const`

**作用与语义：**

返回掉频链最后成功构建的大小。利用此数据判断是否需要再次调用`createOrResize()`：如果`currentPixelSize() != surfacePixelSize()`，则需要调整掉链大小。
注意：典型的渲染逻辑会调用该函数，在准备新帧时获取输出大小，并基于该函数返回的大小进行基底相关计算（如视口）。
虽然在许多情况下，该值与`QWindow::size() * QWindow::devicePixelRatio()`相同，但依赖报告`QWindow`的大小并不保证在所有平台和图形API实现上都正确。因此，每当需要识别输出层或表面的尺寸（像素单位）时，强烈建议使用该函数。
这还带来了一个额外好处，就是在专用渲染线程中使用`QRhi`时避免了潜在的数据竞赛，因为无需调用`QWindow`函数，这些函数随后可能访问主线程更新的数据。

### `QRhiRenderBuffer *QRhiSwapChain::depthStencil() const`

**作用与语义：**

返回当前关联的深度模板渲染缓冲区。

### `QRhiSwapChain::Flags QRhiSwapChain::flags() const`

**作用与语义：**

返回当前设置的标志。

### `QRhiSwapChain::Format QRhiSwapChain::format() const`

**作用与语义：**

返回当前设定的格式。

### `[virtual] QRhiSwapChainHdrInfo QRhiSwapChain::hdrInfo()`

**作用与语义：**

返回相关显示器的HDR信息。
不要以为这是一项廉价操作。根据平台，该函数会对平台进行各种查询，可能会影响性能。
注意：只要窗口期未`set`，可以在`createOrResize()`前打电话。
注意：当前移动带有初始化交换链的窗口（HDR到HDR但特性不同，HDR到SDR等）时的处理尚未明确，且高度依赖窗口系统和合成器，且不同平台行为可能有所不同。目前`QRhi`仅保证hdrInfo()在`createOrResize()`时所属显示显示的有效数据（如有）返回有效数据。

### `[pure virtual] bool QRhiSwapChain::isFormatSupported(QRhiSwapChain::Format f)`

**作用与语义：**

如果支持给定的交换链格式 `f`，则返回为真。SDR 始终被支持。
注意：可以独立于`createOrResize()`调用，但`window()`必须已经设置好。未设置窗口调用可能会导致意外结果（任何HDR格式很可能为假），因为HDR格式支持通常绑定在交换链相关窗口所在的输出（屏幕）上。如果HDR格式的结果成立，那么只要窗口不被移动到其他屏幕，创建该格式的交换链通常会成功。
该函数的主要用途是在窗口设置后的第一个`createOrResize()`之前调用该函数。这使得`QRhi`后端能够执行平台或窗口系统特定的查询，以确定窗口（及其所在屏幕）是否能够以指定格式进行真正的HDR输出。
当格式被报告为支持时，调用`setFormat()`设置所需格式并调用`createOrResize()`。但要注意后果：成功申请HDR格式需要处理不同的色彩空间，可能需要对非HDR内容进行白位校正，调整色调映射方法，调整屏幕外渲染目标设置等。

### `[pure virtual] QRhiRenderPassDescriptor *QRhiSwapChain::newCompatibleRenderPassDescriptor()`

**作用与语义：**

返回一个新的 `QRhiRenderPassDescriptor`，它与此交换链兼容。 返回值有两种用途：可以传递给 `setRenderPassDescriptor()` 和 `QRhiGraphicsPipeline::setRenderPassDescriptor()`。渲染通道描述符描述了附件（颜色、深度/模板）以及可以由 `flags()` 影响的加载/存储行为。`QRhiGraphicsPipeline` 只能与具有 `compatible` `QRhiRenderPassDescriptor` 设置的交换链一起使用。

### `QRhiSwapChainProxyData QRhiSwapChain::proxyData() const`

**作用与语义：**

返回当前设置的代理数据。

### `QRhiRenderPassDescriptor *QRhiSwapChain::renderPassDescriptor() const`

**作用与语义：**

返回当前关联的 `QRhiRenderPassDescriptor` 对象。

### `[override virtual] QRhiResource::Type QRhiSwapChain::resourceType() const`

**作用与语义：**

重装：`QRhiResource::resourceType()` const.
返回资源类型。
返回资源类型。

### `int QRhiSwapChain::sampleCount() const`

**作用与语义：**

返回当前设置的采样计数。1表示没有多重采样抗锯齿。

### `void QRhiSwapChain::setDepthStencil(QRhiRenderBuffer *ds)`

**作用与语义：**

将渲染缓冲区设置为深度模板缓冲区`ds`。

### `void QRhiSwapChain::setFlags(QRhiSwapChain::Flags f)`

**作用与语义：**

这让标志变得很有点像`f`。

### `void QRhiSwapChain::setFormat(QRhiSwapChain::Format f)`

**作用与语义：**

定下了`f`的格式。
避免设置`isFormatSupported()`中报告为不支持的格式。请注意，对某一格式的支持可能取决于交换链相关窗口打开的屏幕。在某些平台，如Windows和macOS，HDR输出要正常工作，显示设置中必须启用HDR输出。
有关高动态范围输出的更多信息，请参见`isFormatSupported()`、`QRhiSwapChainHdrInfo`和`Format`。

### `void QRhiSwapChain::setProxyData(const QRhiSwapChainProxyData &d)`

**作用与语义：**

设置代理数据`d`。

### `void QRhiSwapChain::setRenderPassDescriptor(QRhiRenderPassDescriptor *desc)`

**作用与语义：**

与`QRhiRenderPassDescriptor` `desc`有关联。

### `void QRhiSwapChain::setSampleCount(int samples)`

**作用与语义：**

设定样本计数。`samples`常见的数值有1（无MSAA）、4（4×MSAA）或8×8（8×MSAA）。

### `[since 6.9] void QRhiSwapChain::setShadingRateMap(QRhiShadingRateMap *map)`

**作用与语义：**

与指定的`QRhiShadingRateMap` `map`关联。只有当`QRhi::VariableRateShadingMap`功能被报告为支持时，这才有效。
当也调用`QRhiCommandBuffer::setShadingRate()`时，每个瓦片使用较高的着色率。目前无法控制组合器行为。
注意：设置着色率映射意味着需要一个不同的新`QRhiRenderPassDescriptor`，且部分本地交换链对象必须重建。因此，如果交换链已经设置好，在setShadingRateMap()后立即调用`newCompatibleRenderPassDescriptor()`和`setRenderPassDescriptor()`。然后，`createOrResize()`也必须再次调用。这会产生滚动后果，例如图形管线：这些流程也需要与新`QRhiRenderPassDescriptor`关联并重建。请参阅`QRhiRenderPassDescriptor::serializedFormat()`，了解一些处理建议。记得也为它们设置`QRhiGraphicsPipeline::UsesShadingRate`标志。

### `void QRhiSwapChain::setWindow(QWindow *window)`

**作用与语义：**

设定`window`。

### `[since 6.9] QRhiShadingRateMap *QRhiSwapChain::shadingRateMap() const`

**作用与语义：**

返回当前设置的`QRhiShadingRateMap`。默认情况下，这是`nullptr`。

### `[pure virtual] QSize QRhiSwapChain::surfacePixelSize()`

**作用与语义：**

返回窗口对应的表面或层的大小。
警告：请勿以为这与`QWindow::size() * QWindow::devicePixelRatio()`相同。在某些图形API和窗口系统接口（例如Vulkan）中，理论上曲面的大小可能与相关窗口不同。为了支持这些情况，渲染逻辑必须始终基于`QRhiSwapChain`报告的大小进行尺寸衍生计算（如视口），而绝不能基于`QWindow`查询的大小。
注意：如果至少`window()`已设置，也可以在`createOrResize()`之前调用。结合`currentPixelSize()`可以检测交换链何时需要调整大小。但请注意，底层本地对象（表面、图层等）的大小是“活的”，因此每当调用该函数时，它返回底层实现报告的最新值，且不保证原子性。因此，强烈建议使用该函数来确定帧中使用的图形资源像素大小。应依赖 `currentPixelSize()`，它返回的大小是原子级的，且在`createOrResize()`调用之间不会变化。
注意：对于与交换链颜色缓冲区结合使用的深度模板缓冲区，强烈建议依赖 `QRhiRenderBuffer`：UsedWithSwapChainOnly 标志提供的自动大小和重建行为。避免仅仅通过该函数查询表面大小以获取可传递给`QRhiRenderBuffer::setPixelSize()`的大小，因为这会受到上述缺乏原子性的影响。

### `QWindow *QRhiSwapChain::window() const`

**作用与语义：**

返回当前设置的窗口。

### `enum Flag { SurfaceHasPreMulAlpha, SurfaceHasNonPreMulAlpha, sRGB, UsedAsTransferSource, NoVSync, MinimalBufferCount }`

**作用与语义：**

描述交换链属性的标志值。
- `QRhiSwapChain::SurfaceHasPreMulAlpha`：`1 << 0`;表示目标表面具有预乘 alpha 的透明性。例如，当目标`QWindow`启用 alpha 通道时，Qt Quick 就是用这个方式，因为场景图的 rendrerer 总是输出 alpha 乘以红、绿、蓝三色的片段。为确保各平台行为一致，每当交换链上设置该标志时，目标`QWindow`上始终将 `QSurfaceFormat::alphaBufferSize()` 设置为非零值。
- `QRhiSwapChain::SurfaceHasNonPreMulAlpha`：`1 << 1`;表示目标表面具有非预乘法alpha的透明性。请注意，如果系统合成器总是预期预乘法alpha的内容，某些系统可能不支持此功能。在这种情况下，使用该标志集的行为应等价于SurfaceHasPreMulAlpha。
- `QRhiSwapChain::sRGB`：`1 << 2`;请求为交换链的颜色缓冲区和/或渲染目标视图选择 sRGB 格式（如适用）。注意，这意味着所有针对该交换链的内容都会启用 sRGB 帧缓冲区更新和混合功能，且无法选择退出。对于 OpenGL，还应在`QWindow` `QSurfaceFormat`上设置 `sRGBColorSpace`。仅在交换链格式设置为 `QRhiSwapChain::SDR` 时才适用。
- `QRhiSwapChain::UsedAsTransferSource`：`1 << 3`;表示交换链将作为`QRhiResourceUpdateBatch::readBackTexture()`中回读的源。
- `QRhiSwapChain::NoVSync`：`1 << 4`;请求禁用等待垂直同步，同时避免限制渲染线程。该行为是后端特定的，仅适用于可控制的部分。有些人可能会完全忽略该请求。对于OpenGL，可以尝试通过`QSurfaceFormat::setSwapInterval()`将`QWindow`的交换间隔设置为0。
- `QRhiSwapChain::MinimalBufferCount`：`1 << 5`;创建交换链的请求，缓冲区数最小，实际上是2个，除非图形实现的最低缓冲数更高。仅适用于后端，且该控制可通过图形API实现，例如Vulkan。默认情况下，后端决定请求缓冲区数（实际上几乎总是2或3），这与应用程序无关。然而，例如在Vulkan上，后端通常偏好较高的缓冲区数（3），以避免移动设备上某些Vulkan实现出现异常性能问题。在某些平台上，强制减少缓冲区数（2）可能有益，因此该标志允许强制执行。注意，所有这些都不会影响保持在飞行中的帧数，因此CPU（`QRhi`）仍然会在最多比GPU领先`N - 1`帧时准备帧，即使交换链映像缓冲区计数大于`N`。（`N` = `QRhi::FramesInFlight`，通常为2）。
Flags 类型是 QFlags 的 typedef<Flag>。它存储 Flag 值的 OR 组合。

### `flags Flags`

**作用与语义：**

描述交换链属性的标志值。
- `QRhiSwapChain::SurfaceHasPreMulAlpha`：`1 << 0`;表示目标表面具有预乘 alpha 的透明性。例如，当目标`QWindow`启用 alpha 通道时，Qt Quick 就是用这个方式，因为场景图的 rendrerer 总是输出 alpha 乘以红、绿、蓝三色的片段。为确保各平台行为一致，每当交换链上设置该标志时，目标`QWindow`上始终将 `QSurfaceFormat::alphaBufferSize()` 设置为非零值。
- `QRhiSwapChain::SurfaceHasNonPreMulAlpha`：`1 << 1`;表示目标表面具有非预乘法alpha的透明性。请注意，如果系统合成器总是预期预乘法alpha的内容，某些系统可能不支持此功能。在这种情况下，使用该标志集的行为应等价于SurfaceHasPreMulAlpha。
- `QRhiSwapChain::sRGB`：`1 << 2`;请求为交换链的颜色缓冲区和/或渲染目标视图选择 sRGB 格式（如适用）。注意，这意味着所有针对该交换链的内容都会启用 sRGB 帧缓冲区更新和混合功能，且无法选择退出。对于 OpenGL，还应在`QWindow` `QSurfaceFormat`上设置 `sRGBColorSpace`。仅在交换链格式设置为 `QRhiSwapChain::SDR` 时才适用。
- `QRhiSwapChain::UsedAsTransferSource`：`1 << 3`;表示交换链将作为`QRhiResourceUpdateBatch::readBackTexture()`中回读的源。
- `QRhiSwapChain::NoVSync`：`1 << 4`;请求禁用等待垂直同步，同时避免限制渲染线程。该行为是后端特定的，仅适用于可控制的部分。有些人可能会完全忽略该请求。对于OpenGL，可以尝试通过`QSurfaceFormat::setSwapInterval()`将`QWindow`的交换间隔设置为0。
- `QRhiSwapChain::MinimalBufferCount`：`1 << 5`;创建交换链的请求，缓冲区数最小，实际上是2个，除非图形实现的最低缓冲数更高。仅适用于后端，且该控制可通过图形API实现，例如Vulkan。默认情况下，后端决定请求缓冲区数（实际上几乎总是2或3），这与应用程序无关。然而，例如在Vulkan上，后端通常偏好较高的缓冲区数（3），以避免移动设备上某些Vulkan实现出现异常性能问题。在某些平台上，强制减少缓冲区数（2）可能有益，因此该标志允许强制执行。注意，所有这些都不会影响保持在飞行中的帧数，因此CPU（`QRhi`）仍然会在最多比GPU领先`N - 1`帧时准备帧，即使交换链映像缓冲区计数大于`N`。（`N` = `QRhi::FramesInFlight`，通常为2）。
Flags 类型是 QFlags 的 typedef<Flag>。它存储 Flag 值的 OR 组合。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

### 状态和错误边界

把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

### 线程边界

如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

### 最容易出现的错误

不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QRhiSwapChain` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
