# QRhi

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QRhi` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <rhi/qrhi.h>`
- 继承自：未在类页中列出
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

- `(since 6.10) AdapterList`
- `enum BeginFrameFlag { }`
- `flags BeginFrameFlags`
- `enum EndFrameFlag { SkipPresent }`
- `flags EndFrameFlags`
- `enum Feature { MultisampleTexture, MultisampleRenderBuffer, DebugMarkers, Timestamps, Instancing, …, DepthClamp }`
- `enum Flag { EnableDebugMarkers, EnableTimestamps, PreferSoftwareRenderer, EnablePipelineCacheDataSave, SuppressSmokeTestWarnings }`
- `flags Flags`
- `enum FrameOpResult { FrameOpSuccess, FrameOpError, FrameOpSwapChainOutOfDate, FrameOpDeviceLost }`
- `enum Implementation { Null, Vulkan, OpenGLES2, D3D11, D3D12, Metal }`
- `enum ResourceLimit { TextureSizeMin, TextureSizeMax, MaxColorAttachments, FramesInFlight, MaxAsyncReadbackFrames, …, ShadingRateImageTileSize }`

### 公有函数

- `~QRhi()`
- `void addCleanupCallback(const QRhi::CleanupCallback &callback)`
- `void addCleanupCallback(const void *key, const QRhi::CleanupCallback &callback)`
- `QRhi::Implementation backend() const`
- `const char * backendName() const`
- `QRhi::FrameOpResult beginFrame(QRhiSwapChain *swapChain, QRhi::BeginFrameFlags flags = {})`
- `QRhi::FrameOpResult beginOffscreenFrame(QRhiCommandBuffer **cb, QRhi::BeginFrameFlags flags = {})`
- `QMatrix4x4 clipSpaceCorrMatrix() const`
- `int currentFrameSlot() const`
- `QRhiDriverInfo driverInfo() const`
- `QRhi::FrameOpResult endFrame(QRhiSwapChain *swapChain, QRhi::EndFrameFlags flags = {})`
- `QRhi::FrameOpResult endOffscreenFrame(QRhi::EndFrameFlags flags = {})`
- `QRhi::FrameOpResult finish()`
- `bool isClipDepthZeroToOne() const`
- `bool isDeviceLost() const`
- `bool isFeatureSupported(QRhi::Feature feature) const`
- `bool isRecordingFrame() const`
- `bool isTextureFormatSupported(QRhiTexture::Format format, QRhiTexture::Flags flags = {}) const`
- `bool isYUpInFramebuffer() const`
- `bool isYUpInNDC() const`
- `bool makeThreadLocalNativeContextCurrent()`
- `const QRhiNativeHandles * nativeHandles()`
- `QRhiBuffer * newBuffer(QRhiBuffer::Type type, QRhiBuffer::UsageFlags usage, quint32 size)`
- `QRhiComputePipeline * newComputePipeline()`
- `QRhiGraphicsPipeline * newGraphicsPipeline()`
- `QRhiRenderBuffer * newRenderBuffer(QRhiRenderBuffer::Type type, const QSize &pixelSize, int sampleCount = 1, QRhiRenderBuffer::Flags flags = {}, QRhiTexture::Format backingFormatHint = QRhiTexture::UnknownFormat)`
- `QRhiSampler * newSampler(QRhiSampler::Filter magFilter, QRhiSampler::Filter minFilter, QRhiSampler::Filter mipmapMode, QRhiSampler::AddressMode addressU, QRhiSampler::AddressMode addressV, QRhiSampler::AddressMode addressW = QRhiSampler::Repeat)`
- `QRhiShaderResourceBindings * newShaderResourceBindings()`
- `(since 6.9) QRhiShadingRateMap * newShadingRateMap()`
- `QRhiSwapChain * newSwapChain()`
- `QRhiTexture * newTexture(QRhiTexture::Format format, const QSize &pixelSize, int sampleCount = 1, QRhiTexture::Flags flags = {})`
- `QRhiTexture * newTexture(QRhiTexture::Format format, int width, int height, int depth, int sampleCount = 1, QRhiTexture::Flags flags = {})`
- `QRhiTexture * newTextureArray(QRhiTexture::Format format, int arraySize, const QSize &pixelSize, int sampleCount = 1, QRhiTexture::Flags flags = {})`
- `QRhiTextureRenderTarget * newTextureRenderTarget(const QRhiTextureRenderTargetDescription &desc, QRhiTextureRenderTarget::Flags flags = {})`
- `QRhiResourceUpdateBatch * nextResourceUpdateBatch()`
- `QByteArray pipelineCacheData()`
- `void releaseCachedResources()`
- `void removeCleanupCallback(const void *key)`
- `int resourceLimit(QRhi::ResourceLimit limit) const`
- `void setPipelineCacheData(const QByteArray &data)`
- `(since 6.9) void setQueueSubmitParams(QRhiNativeHandles *params)`
- `QRhiStats statistics() const`
- `QList<int> supportedSampleCounts() const`
- `(since 6.9) QList<QSize> supportedShadingRates(int sampleCount) const`
- `QThread * thread() const`
- `int ubufAligned(int v) const`
- `int ubufAlignment() const`

### 静态公有成员

- `const char * backendName(QRhi::Implementation impl)`
- `QRhi * create(QRhi::Implementation impl, QRhiInitParams *params, QRhi::Flags flags, QRhiNativeHandles *importDevice, QRhiAdapter *adapter)`
- `QRhi * create(QRhi::Implementation impl, QRhiInitParams *params, QRhi::Flags flags = {}, QRhiNativeHandles *importDevice = nullptr)`
- `(since 6.10) QRhi::AdapterList enumerateAdapters(QRhi::Implementation impl, QRhiInitParams *params, QRhiNativeHandles *nativeHandles = nullptr)`
- `int mipLevelsForSize(const QSize &size)`
- `bool probe(QRhi::Implementation impl, QRhiInitParams *params)`
- `QSize sizeForMipLevel(int mipLevel, const QSize &baseLevelSize)`
- `QRhiSwapChainProxyData updateSwapChainProxyData(QRhi::Implementation impl, QWindow *window)`

### 相关非成员函数

- `(since 6.7) QRhiShaderResourceBindingSet`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[alias, since 6.10] QRhi::AdapterList`

**作用与语义：**

`QVector`<`QRhiAdapter`的同义词 *>。
这种类型防御是在Qt 6.10中引入的。

### `enum QRhi::BeginFrameFlagflags QRhi::BeginFrameFlags`

**作用与语义：**

`QRhi::beginFrame()`的旗标值。
BeginFrameFlags 类型是 QFlags 的 typedef<BeginFrameFlag>。它存储 BeginFrameFlag 值的 OR 组合。

### `enum QRhi::EndFrameFlagflags QRhi::EndFrameFlags`

**作用与语义：**

标志值`QRhi::endFrame()`。
- `QRhi::SkipPresent`：`1 << 0`;指定当前命令不排队或不调用swapBuffers。这样就不会显示任何图像。不建议生成多个帧，且所有帧都设置了该标志（除非用于基准测试——但请记住后端在等待命令完成而不呈现时行为可能不同，因此结果无法比较）
EndFrameFlags 类型是 QFlags 的 typedef<EndFrameFlag>。它存储 EndFrameFlag 值的 OR 组合。

### `enum QRhi::Feature`

**作用与语义：**

标记数值表示当前后端支持哪些功能。
- `QRhi::MultisampleTexture`：`1`;表示支持采样计数大于1的纹理。实际上，该功能将不支持3.1以上的OpenGL ES版本和3.0之前的OpenGL ES版本。
- `QRhi::MultisampleRenderBuffer`：`2`;表示支持采样计数大于1的渲染缓冲区。实际上，OpenGL ES 2.0不支持此功能，除非相关扩展存在，否则OpenGL 2.x也可能不支持此功能。
- `QRhi::DebugMarkers`：`3`;表示支持调试标记组（如同`QRhiCommandBuffer::debugMarkBegin()`）。
- `QRhi::Timestamps`：`4`;表示支持命令缓冲区时间戳。与`QRhiCommandBuffer::lastCompletedGpuTime()`相关。预计在Metal、Vulkan、Direct 3D 11和12以及3.3及以后版本的OpenGL上下文中支持此功能。然而，对于其中一些API，时间戳查询支持技术上是可选的，因此无法保证该功能在所有实现中都支持。
- `QRhi::Instancing`：`5`;表示支持实例化绘图。实际上，该功能在OpenGL ES 2.0和OpenGL 3.2及更早版本中将不被支持。
- `QRhi::CustomInstanceStepRate`：`6`;表示支持除1以外的实例步进率。实际上，OpenGL始终不支持此功能。此外，运行Vulkan 1.0而不VK_EXT_vertex_attribute_divisor也会导致该功能报告错误。
- `QRhi::PrimitiveRestart`：`7`;表示在遇到索引值为0xFFFF（`IndexUInt16`）或0xFFFFFFFF（`IndexUInt32`）时，至少在某些原始拓扑下，可以重新启动原语汇编。`QRhi`会尝试在所有后端启用此功能，但在某些情况下不会被支持。由于某些API中，原始重启固定索引始终处于开启状态，因此无法动态控制原语重启。应用程序必须假设，每当该功能被报告为支持时，上述索引值`may`根据拓扑结构被特别处理。只要该功能被报告为支持，原始重启在后端之间保证行为一致的唯一两种拓扑是`LineStrip`和`TriangleStrip`。
- `QRhi::NonDynamicUniformBuffers`：`8`;表示支持创建带有使用`UniformBuffer`和类型`Immutable`或`Static`的缓冲区。当被报告为不支持时，必须创建统一（常数）缓冲区作为`Dynamic`。（无论如何都推荐这样做）
- `QRhi::NonFourAlignedEffectiveIndexBufferOffset`：`9`;表示支持未对齐4字节的有效索引缓冲区偏移量（`indexOffset + firstIndex * indexComponentSize`）。不支持时，尝试发出非对齐有效偏移的`drawIndexed()`可能导致未指定行为。尤其适用于Metal，该系统将报告为不支持。
- `QRhi::NPOTTextureRepeat`：`10`;表示对于非二幂大小的纹理，支持`Repeat`包裹模式和mipmap过滤模式。实际上，只有在没有`GL_OES_texture_npot`的OpenGL ES 2.0实现时，这才可能为假。
- `QRhi::RedOrAlpha8IsRed`：`11`;表示`RED_OR_ALPHA8`格式映射为单组件8位`red`格式。除OpenGL使用OpenGL ES或非核心配置文件上下文外，所有后端均如此。`GL_ALPHA`采用单组件8位`alpha`格式。使用特殊纹理格式允许创建纹理的单一代码路径，实际格式由后端决定，同时功能标志可用于选择合适的着色器变体采样纹理。
- `QRhi::ElementIndexUint`：`12`;表示索引缓冲区支持32位无符号整数元素。实际上，除非运行在无必要扩展的普通OpenGL ES 2.0实现上，否则所有地方都成立。当错误时，索引缓冲区只支持16位无符号元素。
- `QRhi::Compute`：`13`;表示支持计算着色器、图像加载/存储和存储缓冲区。4.3 之前的 OpenGL 和 3.1 之前的 OpenGL ES 不支持计算。
- `QRhi::WideLines`：`14`;表示宽度非1的行被支持。当报告为不支持时，图形管道状态中设置的行宽会被忽略。在某些后端（如D3D11、D3D12、Metal）中，这总是可能为假。在Vulkan中，值取决于实现。在OpenGL中，在核心配置文件环境中不支持宽行。
- `QRhi::VertexShaderPointSize`：`15`;表示通过顶点着色器中通过`gl_PointSize`设置的光栅化点的大小被考虑在内。当报告为不支持时，不支持大小非1的点。在着色器中设置`gl_PointSize`仍然有效，但会被忽略。（例如，在生成HLSL时，该赋值会被无声地从生成的代码中移除）注意，一些API（Metal、Vulkan）要求在绘制点时在着色器中显式设置点大小，即使大小为1，因为它们并不会自动默认为1。
- `QRhi::BaseVertex`：`16`;表示`drawIndexed()`支持`vertexOffset`参数。当报告不支持时，索引绘制中的顶点偏移值将被忽略。实际上，该功能在低于3.2的OpenGL和OpenGL ES版本中不支持，以及在较旧的iOS设备上的Metal系统，包括iOS模拟器。
- `QRhi::BaseInstance`：`17`;表示实例化绘图命令支持`firstInstance`参数。当报告为不支持时，firstInstance 值被忽略，实例 ID 从零开始。实际上，该功能在较老的 iOS 设备上（包括 iOS 模拟器）及所有版本的 OpenGL 上将不支持。后者是因为 OpenGL ES 根本不支持基于基础实例的绘图调用。目前 `QRhi` 的 OpenGL 后端也未实现 OpenGL（非 ES）的功能，因为由于 GLES 的限制，便携应用实际上无法依赖非零的基础实例。如果应用程序仍然选择这样做，也应该知道 InstanceIndexIncludesBaseInstance 功能。
- `QRhi::TriangleFanTopology`：`18`;表示`QRhiGraphicsPipeline::setTopology()`支持`QRhiGraphicsPipeline::TriangleFan`。实际上，Metal 和 Direct 3D 11/12 将不支持此功能。
- `QRhi::ReadBackNonUniformBuffer`：`19`;表示对于使用方式不同的`QRhiBuffer`实例，支持读取缓冲区内容。实际上，OpenGL ES 2.0将不支持此功能。
- `QRhi::ReadBackNonBaseMipLevel`：`20`;表示在读取纹理内容时，支持指定除0以外的MIP级别。如果不支持，在`QRhiReadbackDescription`中指定非零级别会导致返回全零图像。实际上，OpenGL ES 2.0将不支持此功能。
- `QRhi::TexelFetch`：`21`;表示texelFetch()和textureLod()在着色器中可用。实际上，在OpenGL ES 2.0和OpenGL 2.x上下文中，由于GLSL 100 es及130之前版本不支持这些功能，因此该功能会被报告为不支持。
- `QRhi::RenderToNonBaseMipLevel`：`22`;表示在创建带有`QRhiTexture`作为颜色附件的`QRhiTextureRenderTarget`时，支持指定除0以外的MIP级别。如果不支持，`create()`在目标MIP级别不为零时会失败。实际上，OpenGL ES 2.0将不支持此功能。
- `QRhi::IntAttributes`：`23`;表示支持为着色器流水线指定带有符号和无符号整数类型的输入属性。不支持时，build() 会成功，但只显示警告信息，目标属性的值会被破坏。实际上，该功能在 OpenGL ES 2.0 和 OpenGL 2.x 中将不被支持。
- `QRhi::ScreenSpaceDerivatives`：`24`;表示着色器支持dFdx()、dFdy()和fwidth()等函数。实际上，没有GL_OES_standard_derivatives扩展的OpenGL ES 2.0将不支持此功能。
- `QRhi::ReadBackAnyTextureFormat`：`25`;表示回读纹理内容可以预期适用于任何`QRhiTexture::Format`。除OpenGL外的后端，预计该功能会返回true。当报告为false时（OpenGL通常会发生），只有`QRhiTexture::RGBA8`和`QRhiTexture::BGRA8`格式保证支持回读。此外，OpenGL支持（但不包括OpenGL ES），也支持读取每个组件1字节的格式`QRhiTexture::R8`和`QRhiTexture::RED_OR_ALPHA8`。读取浮点格式 `QRhiTexture::RGBA16F` 和 RGBA32F 也可能适用于 OpenGL，只要实现支持这些格式，但`QRhi`无法保证，正如该标志所示。
- `QRhi::PipelineCacheDataLoadSave`：`26`;表示 `pipelineCacheData()` 和 `setPipelineCacheData()` 函数是正常的。当不支持时，函数不会执行任何操作，检索的 blob 总是空的，因此在后续应用运行时，获取并重新加载流水线缓存内容不会带来任何好处。
- `QRhi::ImageDataStride`：`27`;表示支持在纹理上传中为原始图像数据指定自定义步幅（行长）。当不支持时（当底层API为OpenGL ES 2.0且不支持GL_UNPACK_ROW_LENGTH时），`QRhiTextureSubresourceUploadDescription::setDataStride()`不得使用。
- `QRhi::RenderBufferImport`：`28`;表示支持`QRhiRenderBuffer::createFrom()`。对于大多数图形API，这并不合理，因为`QRhiRenderBuffer`内部封装了纹理对象，就像 `QRhiTexture` 一样。然而，在 OpenGL 中，渲染缓冲对象作为 API 中的独立对象类型存在，在某些环境中（例如，可能希望将渲染缓冲对象与 EGLImage 对象关联）需要允许用 `QRhiRenderBuffer` 包裹现有的 OpenGL 渲染缓冲对象。
- `QRhi::ThreeDimensionalTextures`：`29`;表示支持3D纹理。实际上，该功能在低于3.0的OpenGL和OpenGL ES版本中将不被支持。
- `QRhi::RenderTo3DTextureSlice`：`30`;表示支持在3D纹理中渲染到切片。由于依赖VK_IMAGE_CREATE_2D_ARRAY_COMPATIBLE_BIT，Vulkan 1.0可能不支持此功能，而是Vulkan 1.1的功能。
- `QRhi::TextureArrays`：`31`;表示纹理数组被支持且`QRhi::newTextureArray()`功能正常。注意，即使不支持纹理数组，纹理数组仍然可用，因为它们是两个独立的功能。
- `QRhi::Tessellation`：`32`;表示支持镶嵌控制和评估阶段。当报告支持时，`QRhiGraphicsPipeline`的拓扑可设为`Patches`，控制点数量可通过`setPatchControlPointCount()`设置，`QRhiShaderStage`列表中可指定镶嵌控制和评估的着色器。镶嵌着色器在 API 间存在可移植性问题（例如，由于 HULL 着色器结构不同，将 GLSL/SPIR-V 转换为 HLSL 存在问题，而 Metal 则使用与其他平台略有不同的镶嵌流水线），因此即使所有底层 API 都实现了基本功能，仍可能出现意想不到的问题。尤其是对于 Direct 3D，必须在每个`QShader`中分别注入手写的 HLSL hull、领域着色器，分别用于镶嵌控制和评估阶段，因为 qsb 无法从 SPIR-V 生成这些着色器。请注意，应避免等值线镶嵌，因为并非所有后端都支持。后端之间可移植的最大补丁控制点数为 32。
- `QRhi::GeometryShader`：`33`;表示支持几何着色器阶段。支持时，可以在`QRhiShaderStage`列表中指定几何着色器。几何着色器在`QRhi`被视为实验性功能，预计仅支持Vulkan、Direct 3D 11和12、OpenGL（3.2）和OpenGL ES（3.2），前提是实现在运行时报告支持。从 Qt 6.11 开始，几何着色器会自动转换为 HLSL，因此不再需要注入手写的 HLSL 几何着色器（但请注意，不支持 gl_in 和 gl_in[0].gl_Position 等表达式;相反，将位置作为顶点着色器的输出变量传递）。Metal 不支持几何着色器。
- `QRhi::TextureArrayRange`: `34`；表示对于纹理数组，可以指定一个暴露给着色器的范围。通常所有数组层都是暴露的，由着色器选择层（通过采样 `sampler2DArray` 时传递给 texture() 的第三个坐标）。在支持的情况下，在 `building` 或 `importing` 之前调用 QRhiTexture::setArrayRangeStart() 和 QRhiTexture::setArrayRangeLength() 会对原生纹理产生影响，并只选择数组中指定的范围。这在特殊情况中是必要的，例如在使用加速视频解码和 Direct 3D 11 时，因为如果纹理数组上同时有 `D3D11_BIND_DECODER` 和 `D3D11_BIND_SHADER_RESOURCE`，只选择单个数组层时它才可用作着色器资源。请注意，所有这些仅在纹理用作 `QRhiShaderResourceBinding::SampledTexture` 或 `QRhiShaderResourceBinding::Texture` 着色器资源时适用，并且与图像加载/存储不兼容。此功能仅在某些后端可用，因为它并不适用于所有图形 API，并且本质上只是为特殊情况提供支持。实际上，该功能可预期在 Direct3D 11/12 和 Vulkan 上得到支持。
- `QRhi::NonFillPolygonMode`: `35`；表示支持为 `QRhiGraphicsPipeline` 设置默认 Fill 之外的 PolygonMode。将模式更改为 Line 的一个常见用例是获得线框渲染。然而，这并不是核心 OpenGL ES 功能，并且在 Vulkan 上是可选的，有些移动 GPU 可能也不提供该功能。
- `QRhi::OneDimensionalTextures`: `36`；表示支持 1D 纹理。实际上，这个功能在 OpenGL ES 上将不被支持。
- `QRhi::OneDimensionalTextureMipmaps`: `37`；表示支持生成 1D 纹理 mipmap。实际上，这个功能在不报告支持 OneDimensionalTextures、Metal 和 Direct 3D 12 的后端将不被支持。
- `QRhi::HalfAttributes`: `38`；表示支持为着色器管线指定半精度（16 位）浮点类型的输入属性。不支持时，build() 会成功，但会显示警告信息，并且目标属性的值将被破坏。实际上，这个功能在某些 OpenGL ES 2.0 和 OpenGL 2.x 实现中不被支持。请注意，虽然 Direct3D 11/12 支持半精度输入属性，但不支持 half3 类型。D3D 后端将 half3 属性作为 half4 传递。为确保跨平台兼容性，half3 输入应填充到 8 字节。
- `QRhi::RenderToOneDimensionalTexture`: `39`；表示支持 1D 纹理渲染目标。实际上，这个功能在不报告支持 OneDimensionalTextures 的后端和 Metal 上将不被支持。
- `QRhi::ThreeDimensionalTextureMipmaps`: `40`；表示支持生成 3D 纹理 mipmap。这通常从 Qt 6.10 开始被所有后端支持。
- `QRhi::MultiView`：`41`;表示支持多视角，参见例如支持VK_KHR_multiview。在没有`GL_OVR_multiview2`的OpenGL ES 2.0、Direct 3D 11和OpenGL（ES）实现中，该功能将不被支持。在Vulkan 1.1及以后版本，以及Direct 3D 12通常支持多视图。当报告为支持时，创建一个带有引用纹理数组且包含`multiViewCount`集的`QRhiColorAttachment`的`QRhiTextureRenderTarget`可以记录使用多视角渲染的渲染通道。此外，该渲染通道中使用的任何`QRhiGraphicsPipeline`必须设置相同的视图计数。注意，多视图仅与二维纹理数组结合使用。它不能用于将渲染优化为单个纹理（例如左右眼的两个）。相反，多视图渲染通道的目标始终是一个纹理数组，自动渲染到对应每个视图的图层（数组元素）。因此，这一特性也包含纹理数组。多视图渲染不支持与镶嵌或几何着色器结合使用。有关多视图渲染的更多细节，请参见 `QRhiColorAttachment::setMultiViewCount()`。该枚举值已在 Qt 6.7 中引入。
- `QRhi::TextureViewFormat`：`42`;表示在`QRhiTexture`上设置视图格式是有效的。当报告为支持时，设置读取（采样）或写入（渲染目标/图像加载-存储）视图模式会改变纹理的视图格式。不支持时，设置视图格式无影响。注意，Qt 对底层 3D API 及其实现中的格式兼容性或资源视图规则没有知识或控制权。传递不合适且不兼容的格式可能导致错误和未说明的行为。这主要是为了允许将“casting”渲染成用 sRGB 格式创建的纹理转为非 sRGB，以避免着色器写入时不想要的线性 >sRGB 转换。其他类型的casting可能有效，也可能无效，取决于底层API。目前已实现于 Vulkan 和 Direct 3D 12。在 D3D12 中，该功能仅在支持 `CastingFullyTypedFormatSupported` 时可用，详见 https://microsoft.github.io/DirectX-Specs/d3d/RelaxedCasting.html（并注意 `QRhi` 始终使用全类型格式的纹理）。该枚举值在 Qt 6.8 中引入。
- `QRhi::ResolveDepthStencil`：`43`;表示支持解析多采样深度或深度模板纹理。否则，设置深度解析纹理无效功能，必须避免。直接3D 11和12不支持解析深度/深度模板格式，因此此功能永远不会被支持。Vulkan 1.0没有API请求解析深度模板附件。因此，Vulkan仅支持该功能支持Vulkan 1.2及以上版本，以及在1.1实现中支持并配备相应扩展。此功能适用于极少数需要解析为非多重采样深度纹理的情况，例如渲染成OpenXR提供的深度纹理（XR_KHR_composition_layer_depth）。该枚举值在第6.8卷引入。
- `QRhi::VariableRateShading`：`44`;表示支持每绘图（每流水线）可变速率着色。当报告为支持时，`QRhiCommandBuffer::setShadingRate()`功能正常，并对`QRhiGraphicsPipeline`在其标志中声明`QRhiGraphicsPipeline::UsesShadingRate`的对象产生影响。调用`QRhi::supportedShadingRates()`确认支持哪些速率。（1x1始终支持，其他典型值有2x2、1x2、2x1、2x4、4x2、4x4）。假设运行时的实现和GPU支持VRS，该功能预计会被Direct 3D 12和Vulkan支持。该枚举值是在第6.9期引入的。
- `QRhi::VariableRateShadingMap`：`45`;表示基于图像的着色速率可以指定。“图像”不一定是纹理，它可能是原生的3D API对象，具体取决于运行时底层后端和图形API。实际上，该功能可以预期支持Direct 3D 12、Vulkan和Metal，前提是GPU足够现代以支持VRS。要检查是否支持D3D12/Vulkan风格的基于图像的VRS，请使用VariableRateShadingMapWithTexture。当该功能被报告为支持时，有两种可能：当 VariableRateShadingMapWithTexture 也为真时，`QRhiShadingRateMap` 通过 createFrom() 重载占用 `QRhiTexture` 参数，消耗`QRhiTexture`对象。当 VariableRateShadingMapWithTexture 为假时，`QRhiShadingRateMap` 会消耗其他类型的本地对象，例如在 Metal 中使用 MTLRasterizationRateMap。在这种情况下，使用 createFrom() 重载，取一个 NativeShadingRateMap。该枚举值在 Qt 6.9 中引入。
- `QRhi::VariableRateShadingMapWithTexture`：`46`;表示通过常规纹理支持基于图像的着色率指定。实际上，Direct 3D 12和Vulkan可能支持该功能。该枚举值已在Qt 6.9引入。
- `QRhi::PerRenderTargetBlending`：`47`;表示支持每个渲染目标混合，即MRT帧缓冲区中不同的渲染目标可以有不同的混合模式。实际上，除了OpenGL ES外，预计所有平台都支持该模式，OpenGL ES仅在GLES 3.2实现中支持。该枚举值于Qt 6.9引入。
- `QRhi::SampleVariables`：`48`;表示gl_SampleID、gl_SamplePosition、gl_SampleMaskIn和gl_SampleMask变量均可在片段着色器中使用。实际上，除了OpenGL ES外，预计该功能将支持所有平台，OpenGL ES仅在GLES 3.2实现中提供。该枚举值在Qt 6.9中引入。
- `QRhi::InstanceIndexIncludesBaseInstance`：`49`;表示`gl_InstanceIndex`包含基实例（绘图调用中的`firstInstance`参数）作为值。当该功能不支持但BaseInstance支持时，表示`gl_InstanceIndex`始终从0开始，而非基值。目前Direct 3D 11和12实际上是如此。在Vulkan和Metal中，该功能预计会被报告为始终支持。该枚举值在Qt 6.11中引入。
- `QRhi::DepthClamp`：`50`;表示支持启用深度钳。当报告为不支持时（如 OpenGL ES、3.2 之前未包含相关扩展的 OpenGL 版本以及 iOS 模拟器中的 Metal），调用 setDepthClamp() 并引用参数为 `true` 无效。该枚举值于 Qt 6.11 引入。

### `enum QRhi::Flagflags QRhi::Flags`

**作用与语义：**

描述需要启用哪些特殊功能。
- `QRhi::EnableDebugMarkers`：`1 << 0`;启用调试标记组。如果没有这个框架，调试功能如在外部GPU调试工具中显示调试组和自定义资源名称，将无法使用，`QRhiCommandBuffer::debugMarkBegin()`等功能将变得无运。避免在生产版本中启用，因为可能会带来小幅性能影响。当`QRhi::DebugMarkers`功能未被报告为支持时，该功能无效。
- `QRhi::EnableTimestamps`：`1 << 3`;启用 GPU 时间戳收集。未设置时，`QRhiCommandBuffer::lastCompletedGpuTime()` 总是返回 0。仅在需要时启用，因为根据底层图形 API 可能涉及少量额外工作（例如时间戳查询）。当 `QRhi::Timestamps` 功能未被报告为支持时，该功能无影响。
- `QRhi::PreferSoftwareRenderer`：`1 << 1`;表示后端应优先选择在CPU上用软件渲染的适配器或物理设备。例如，Direct3D通常会提供“基础渲染驱动程序”适配器，`DXGI_ADAPTER_FLAG_SOFTWARE`。设置该标志会要求后端选择该适配器，只要没有被其他后端特定方式强制使用。在Vulkan中，这对应于优先使用带有`VK_PHYSICAL_DEVICE_TYPE_CPU`的物理设备。当不可用或无法确定适配器/设备是否基于软件时，该标志被忽略。图形API中也可能忽略该标志，这些API没有枚举适配器/设备的概念和方式。
- `QRhi::EnablePipelineCacheDataSave`：`1 << 2`;在适用情况下，启用获取流水线缓存内容。未设置时，`pipelineCacheData()`始终返回空 blob。在不支持检索和恢复流水线缓存内容的后端，该标志无效，序列化缓存数据始终为空。该标志提供了选择加入机制，因为维护相关数据结构的成本对某些后端来说并不低。在 Vulkan 中，该功能直接映射到 VkPipelineCache、vkGetPipelineCacheData 和 VkPipelineCacheCreateInfo：:p InitialData。Direct3D 11 没有真正的 pipline 缓存，但 HLSL->DXBC 编译的结果会被存储，并可通过该机制进行序列化/反序列化。这使得未来在带有 HLSL 源代码而非离线预编译字节码的着色器应用中，可以跳过耗时的 D3DCompile() 缓存。如果大量 HLSL 源编译工作进行，这能大幅提升启动和加载时间。OpenGL 通过检索和加载着色器程序二进制文件（如果驱动程序支持）来模拟“流水线缓存”。OpenGL 还提供了额外的基于磁盘的缓存机制，用于 Qt 提供的着色器/程序二进制文件。一旦设置了该标志，写入这些机制可能会被禁用，因为将程序二进制文件存储到多个缓存中并不合理。
- `QRhi::SuppressSmokeTestWarnings`：`1 << 4`;表示在后端相关时，某些非致命`QRhi::create()`故障不应产生`qWarning()`调用。例如，在D3D11中，传递该标志会使许多因失败而出现的警告消息`QRhi::create()`转为分类调试打印，归入常用的`qt.rhi.general`日志分类。这可以被像 Qt Quick 这样的引擎使用，这些引擎具有备份逻辑，即它们会用不同的标志集（如 PreferSoftwareRenderer）重试调用 `create()`，以隐藏第一次尝试失败时输出的无条件警告`create()`。
Flags 类型是 QFlags 的 typedef<Flag>。它存储 Flag 值的 OR 组合。

### `enum QRhi::FrameOpResult`

**作用与语义：**

描述可能出现软失败的操作结果。
- `QRhi::FrameOpSuccess`：`0`;成功
- `QRhi::FrameOpError`：`1`;未说明错误
- `QRhi::FrameOpSwapChainOutOfDate`：`2`;交换链内部处于不一致状态。通过尝试以后重复操作（如`beginFrame()`）可以恢复。
- `QRhi::FrameOpDeviceLost`：`3`;图形设备丢失。通过释放并重新初始化所有由本地图形资源支持的对象，尝试重复操作（如`beginFrame()`）可恢复。参见 `isDeviceLost()`。

### `enum QRhi::Implementation`

**作用与语义：**

描述`QRhi`实例使用哪些图形API专用后端。
- `QRhi::Null`：`0`
- `QRhi::Vulkan`：`1`
- `QRhi::OpenGLES2`：`2`
- `QRhi::D3D11`：`3`
- `QRhi::D3D12`：`5`
- `QRhi::Metal`：`4`

### `enum QRhi::ResourceLimit`

**作用与语义：**

描述查询资源的限制。
- `QRhi::TextureSizeMin`：`1`;最小纹理宽度和高度。通常为1。最小纹理大小处理得很优雅，也就是说，尝试创建空大小的纹理会变成最小大小的纹理。
- `QRhi::TextureSizeMax`：`2`;最大纹理宽度和高度。这取决于图形API，有时也取决于平台或实现。通常值在4096到16384之间。尝试创建比这个更大的纹理通常会失败。
- `QRhi::MaxColorAttachments`：`3`;如果支持多个渲染目标，`QRhiTextureRenderTarget`的最大颜色附件数。不支持 MRT 时，数值为 1。否则通常为 8，但请注意 OpenGL 仅要求最低 4，这也是一些 OpenGL ES 实现提供的。
- `QRhi::FramesInFlight`：`4`;后端可以保持“飞行中”的帧数：对于像Vulkan或Metal这样的后端，在启动新帧时，`QRhi`负责在启动新帧时阻挡，并且发现CPU已经比GPU快`N - 1`帧（因为提交的命令缓冲区在帧编号`current` - `N`尚未完成）。N 是从这里返回的值，通常为 2。这对于直接与图形API集成渲染的应用程序可能相关，因为渲染代码可能希望对资源（如缓冲区）执行双重缓冲（如果值为2），类似于`QRhi`后端本身。当前帧槽索引（即0、1、..、N-1的值，然后环绕）可从`QRhi::currentFrameSlot()`中检索。对于后端，图形API对命令提交过程没有低级控制，该值为1。注意，即使该值为1，流水线仍可能发生（一些后端，如D3D11，设计为尝试实现此功能，例如通过使用统一缓冲区的更新策略，避免流水线停滞），但此时该值不受`QRhi`控制，因此API中未反映。
- `QRhi::MaxAsyncReadbackFrames`：`5`;在开始新帧时，异步纹理或缓冲区回读保证完成的数个`submitted`帧（包括包含回读的那一帧）。
- `QRhi::MaxThreadGroupsPerDimension`：`6`;可调度的最大计算工作/线程组数。实际上是`QRhiCommandBuffer::dispatch()`参数的最大值。通常为65535。
- `QRhi::MaxThreadsPerThreadGroup`：`7`;单个本地工作组中调用次数的最大值，或用其他术语表示，线程组中线程的最大线程数。实际上是计算着色器中`local_size_x`、`local_size_y`和`local_size_z`乘积的最大值。典型值为128、256、512、1024或1536。注意OpenGL ES和Vulkan都只指定128作为实现的最小要求限制。虽然在Vulkan中不常见，但一些针对移动/嵌入式设备的OpenGL ES 3.1实现仅支持规范规定的最小值。
- `QRhi::MaxThreadGroupX`：`8`;X维工作/线程组的最大大小。实际上是计算着色器中`local_size_x`的最大值。通常为256或1024。
- `QRhi::MaxThreadGroupY`：`9`;工作组/线程组在Y维的最大大小。实际上是计算着色器中`local_size_y`的最大值。通常为256或1024。
- `QRhi::MaxThreadGroupZ`：`10`;Z维工作组/线程组的最大大小。实际上是计算着色器中`local_size_z`的最大值。通常为64或256。
- `QRhi::TextureArraySizeMax`：`11`;纹理数组的最大大小。通常在256到2048之间。尝试创建包含更多元素的纹理数组很可能会失败。
- `QRhi::MaxUniformBufferRange`：`12`;从均匀缓冲区一次可以暴露到着色器的字节数。在OpenGL ES 2.0和3.0实现中，这个数值可能低至3584字节（224个四分量，每个分量向量32位）。其他地方通常为16384（1024 vec4s）或65536（4096 vec4s）。
- `QRhi::MaxVertexInputs`：`13`;顶点着色器输入属性的数量。`QRhiVertexInputAttribute`中的位置必须在范围`[0, MaxVertexInputs-1]`内。在OpenGL ES 2.0中，值最低可达8。其他地方，典型值为16、31或32。
- `QRhi::MaxVertexOutputs`：`14`;顶点着色器输出的最大数值（4个分量向量`out`变量）。OpenGL ES 2.0 的值可能低至 8，OpenGL ES 3.0 及部分 Metal 设备可达 15。其他地方，典型值为 32。
- `QRhi::ShadingRateImageTileSize`：`15`;着色率纹理的图块尺寸。如果不支持`QRhi::VariableRateShadingMapWithTexture`特性，则为0。否则，值为16，例如表示16x16的图块大小。（R8UI）着色率纹理中的每个字节定义了16x16像素图块的着色率。详情请参见`QRhiShadingRateMap`。

### `[noexcept] QRhi::~QRhi()`

**作用与语义：**

毁灭者。摧毁后端并释放资源。

### `void QRhi::addCleanupCallback(const QRhi::CleanupCallback &callback)`

**作用与语义：**

当`QRhi`被摧毁时，会注册一个`callback`。
回调运行时图形资源仍然可用，因此应用程序可以干净利落地释放属于`QRhi`的`QRhiResource`实例。这对于管理存储在`cache`类型对象中资源的生命周期特别有用，因为缓存中存放的是QRhiResources或包含QRhiResources的对象。

### `void QRhi::addCleanupCallback(const void *key, const QRhi::CleanupCallback &callback)`

**作用与语义：**

寄存器`callback`在`QRhi`被销毁时被调用。这种重载会使用一个不透明的指针`key`，用于确保给定回调只被注册（并被调用）一次。

### `QRhi::Implementation QRhi::backend() const`

**作用与语义：**

返回该`QRhi`的后端类型。

### `const char *QRhi::backendName() const`

**作用与语义：**

返回该`QRhi`的后端类型为字符串。

### `[static] const char *QRhi::backendName(QRhi::Implementation impl)`

**作用与语义：**

返回一个友好的后端`impl`名称，通常是正在使用的3D API名称。

### `QRhi::FrameOpResult QRhi::beginFrame(QRhiSwapChain *swapChain, QRhi::BeginFrameFlags flags = {})`

**作用与语义：**

启动一个新帧，目标是下一个可用的`swapChain`缓冲区。
帧由资源更新以及一个或多个渲染和计算遍组成。
`flags`可以表示某些特殊情况。
使用交换链渲染成`QWindow`的高级模式：
- 创建掉期链。
- 当表面尺寸与之前不同时调用`QRhiSwapChain::createOrResize()`。
- 打电话给`QRhiSwapChain::destroy()` `QPlatformSurfaceEvent::SurfaceAboutToBeDestroyed`。
- 那么在每个帧上：
beginFrame（sc）;
updates = nextResourceUpdateBatch();
更新->......
QRhiCommandBuffer *cb = sc->currentFrameCommandBuffer();
cb->beginPass（sc->currentFrameRenderTarget()， colorClear， dsClear， updates）;
...
cb->端传球();
......// 必要时再传。
endFrame（sc）;
成功时返回`QRhi::FrameOpSuccess`，失败时返回其他`QRhi::FrameOpResult`值。其中一些应被视为软性“稍后再试”的错误：当`QRhi::FrameOpSwapChainOutOfDate`返回时，交换链需要通过调用`QRhiSwapChain::createOrResize()`来调整或更新。应用程序随后应尝试生成新的帧。`QRhi::FrameOpDeviceLost`意味着图形设备丢失，但也可以通过释放所有资源，包括`QRhi`本身，然后重新创建所有资源来恢复。详见 `isDeviceLost()` 以获取进一步讨论。

### `QRhi::FrameOpResult QRhi::beginOffscreenFrame(QRhiCommandBuffer **cb, QRhi::BeginFrameFlags flags = {})`

**作用与语义：**

启动新的屏幕外帧。提供适合在`cb`中记录渲染命令的命令缓冲区。`flags`用于指示某些特殊情况，就像`beginFrame()`一样。
注意：存储在 *cb 的`QRhiCommandBuffer`不属于调用者所有。
不使用交换链渲染也是可能的。典型的用例是用于完全离屏的应用程序，例如通过渲染和读取生成图像序列，而无需显示窗口。
在屏幕应用中使用（如`beginFrame`、`endFrame`、beginOffscreenFrame、`endOffscreenFrame`、`beginFrame`等）也是可能的，但这会降低并行性，因此应很少使用。
屏幕外帧不允许CPU在GPU仍在处理前一帧时生成下一帧。这带来了一个副作用：如果回读被调度，结果在返回时保证`endOffscreenFrame()`可用。但针对交换链的帧则不然：GPU可能利用得更好，但处理读回操作需要应用程序更谨慎，因为`endFrame()`不像`endOffscreenFrame()`那样保证读取结果在该时可用。
不使用交换链渲染帧并读取帧内容的骨架可以如下：

**官方示例：**

```cpp
 QRhiReadbackResult rbResult;
 QRhiCommandBuffer *cb;
 rhi->beginOffscreenFrame(&cb);
 cb->beginPass(rt, colorClear, dsClear);
 // ...
 u = nextResourceUpdateBatch();
 u->readBackTexture(rb, &rbResult);
 cb->endPass(u);
 rhi->endOffscreenFrame();
 // image data available in rbResult
```

### `QMatrix4x4 QRhi::clipSpaceCorrMatrix() const`

**作用与语义：**

返回一个矩阵，允许应用程序无论后端为何`QRhi`，都能持续使用面向OpenGL的顶点数据和透视投影矩阵（如`QMatrix4x4::perspective()`生成的）。
在典型渲染器中，一旦使用`this_matrix * mvp`而非仅`mvp`，即可使用顶点数据（Y上方和深度范围0-1的视口），而无需考虑运行时将使用哪个后端（以及图形API）。这样可以避免基于`isYUpInNDC()`和`isClipDepthZeroToOne()`的分支（尽管在实现某些高级图形技术时仍可能需要此类逻辑）。
请参阅本页，从瓦肯视角讨论该话题。

### `[static] QRhi *QRhi::create(QRhi::Implementation impl, QRhiInitParams *params, QRhi::Flags flags, QRhiNativeHandles *importDevice, QRhiAdapter *adapter)`

**作用与语义：**

返回一个新的`QRhi`实例，后端为由`impl`指定的图形API提供后端，并`flags`指定。如果函数失败，返回`nullptr`。
`params`必须指向`QRhiInitParams`的某个后端特定子类的实例，如`QRhiVulkanInitParams`、`QRhiMetalInitParams`、`QRhiD3D11InitParams`、`QRhiD3D12InitParams`、`QRhiGles2InitParams`。有关创建`QRhi`的示例，请参见这些类。
`QRhi` 设计上不实现任何后备逻辑：如果指定 API 无法初始化，create() 会失败，后端在调试输出中打印警告。不过，`QRhi` 的客户端，例如 Qt Quick，可能会提供额外逻辑，允许根据平台跳回与请求不同的 API。如果目的只是测试以后调用 create() 时初始化是否成功，最好使用 `probe()` 代替 create()，因为某些后端可以更轻量级地实现探测，而 create() 则会对基础设施进行完整初始化，如果该实例被立即丢弃`QRhi`则是浪费的。
`importDevice`允许使用已有的图形设备，而无需创建自己的图形设备`QRhi`。当非空时，该参数必须指向`QRhiNativeHandles`的某个子类实例：`QRhiVulkanNativeHandles`、`QRhiD3D11NativeHandles`、`QRhiD3D12NativeHandles`、`QRhiMetalNativeHandles`、`QRhiGles2NativeHandles`。具体细节和语义取决于backand及其底层图形API。
在`adapter`中指定`QRhiAdapter`提供了一种透明的跨API替代方案，替代通过`QRhiVulkanNativeHandles`传递`VkPhysicalDevice`或通过 `QRhiD3D12NativeHandles`传递适配器LUID。不对`adapter`的所有权。有关此方法的更多信息，请参见 `enumerateAdapters()`。
注意：`importDevice`和`adapter`不能同时指定。

### `[static] QRhi *QRhi::create(QRhi::Implementation impl, QRhiInitParams *params, QRhi::Flags flags = {}, QRhiNativeHandles *importDevice = nullptr)`

**作用与语义：**

相当于create（`impl`、`params`、`flags`、`importDevice`、`nullptr`）。

### `int QRhi::currentFrameSlot() const`

**作用与语义：**

在录制帧时返回当前帧槽索引。在当前帧外调用时（即`isRecordingFrame()` `false`时）未指定。
对于像Vulkan或Metal这样的后端，`QRhi`后端负责在开始新帧时阻挡，并且发现CPU已经比GPU快`FramesInFlight - 1`帧（因为提交的命令缓冲区在帧号`current` - `FramesInFlight`尚未完成）。
通常在帧间变化的资源（例如支持类型为`QRhiBuffer::Dynamic`的`QRhiBuffer`的原生缓冲对象）存在多个版本，因此每个帧在处理前一帧时提交的帧都能与自己的副本工作，从而避免在准备帧时暂停流水线。（GPU中可能仍在使用的资源内容不应被触动，但仅仅等待上一帧完成会降低GPU利用率，最终降低性能和效率。）。
从概念上讲，这在某种程度上类似于某些C容器和其他类型的写时复制方案。它也可能类似于OpenGL或Direct 3D 11实现对某些类型对象的内部表现。
实际上，这种双重（或三重）缓冲资源在 Vulkan、Metal 及类似`QRhi`后端通过固定数量的本地资源（如 VkBuffer）`slots`在`QRhiResource`后实现。然后可以通过一个帧槽索引来索引，索引为 0， 1， ..， `FramesInFlight`-1，然后环绕。
所有这些对`QRhi`用户来说都是透明的。然而，直接与图形API集成渲染的应用程序可能希望对自身图形资源进行类似的双重或三重缓冲。这最简单的实现方式是了解最大飞行中帧数（可通过`resourceLimit()`检索）和当前帧（槽）索引（由该函数返回）。

### `QRhiDriverInfo QRhi::driverInfo() const`

**作用与语义：**

返回该成功初始化实例所使用的图形设备的元数据`QRhi`。

### `QRhi::FrameOpResult QRhi::endFrame(QRhiSwapChain *swapChain, QRhi::EndFrameFlags flags = {})`

**作用与语义：**

结束、提交并呈现`swapChain`上一个`beginFrame()`开始的帧。
双重（或三重）缓冲由`QRhiSwapChain`和`QRhi`内部管理。
`flags` 也可以选择性地以某些方式改变行为。传递`QRhi::SkipPresent`可以跳过排队 Present 命令或调用 swapBuffers。
成功时返回`QRhi::FrameOpSuccess`，失败时返回`QRhi::FrameOpResult`值。其中一些应视为软性“稍后再试”的错误：当返回`QRhi::FrameOpSwapChainOutOfDate`时，交换链需要通过调用`QRhiSwapChain::createOrResize()`来调整或更新。应用程序随后应尝试生成新的帧。`QRhi::FrameOpDeviceLost`意味着图形设备丢失，但也可以通过释放所有资源，包括`QRhi`本身，然后重新创建所有资源来恢复。详见 `isDeviceLost()` 以获取进一步讨论。

### `QRhi::FrameOpResult QRhi::endOffscreenFrame(QRhi::EndFrameFlags flags = {})`

**作用与语义：**

结束，提交，等待画面外的画面。
`flags`目前未被使用。

### `[static, since 6.10] QRhi::AdapterList QRhi::enumerateAdapters(QRhi::Implementation impl, QRhiInitParams *params, QRhiNativeHandles *nativeHandles = nullptr)`

**作用与语义：**

返回存在的适配器（物理设备）列表，或在给定图形API无法提供此类控制时返回空列表。
在后端无法获得此类控制层级时，返回的列表总是空的。因此，列表空并不意味着系统中没有图形设备，而是无法进行细致的选择选择。
Direct 3D 11、Direct 3D 12 和 Vulkan 的后端预计将完全支持枚举适配器。其他则可能不支持。后端由 `impl` 指定。该函数返回的`QRhiAdapter`只能在具有相同`impl`的 `create()` 调用中使用。一些底层 API 可能存在进一步限制，尤其是 Vulkan，`QRhiAdapter` 指定为`QVulkanInstance`（`VkInstance`）。
调用者预期销毁列表中的`QRhiAdapter`对象。除了查询`info()`外，这些对象的唯一目的是传递给`create()`，或传递给更高层（如 Qt Quick）中的相应函数。
以下为 Vulkan 编写的摘要展示了如何枚举可用的物理设备并请求为所选设备创建`QRhi`。实际上，这相当于通过`QRhiVulkanNativeHandles`传递`VkPhysicalDevice`到 `create()`，但在应用端涉及的 API 代码较少：
由于某些底层图形API的设计，必须传递`params`。特别是在Vulkan中，必须提供`QVulkanInstance`，因为没有它无法枚举。后端专用`params`中的其他字段实际上不会被该函数使用。
`nativeHandles`为可选。指定时必须是有效的`QRhiD3D11NativeHandles`、`QRhiD3D12NativeHandles`或`QRhiVulkanNativeHandles`，类似于`create()`。但与`create()`不同，仅使用物理设备（Vulkan）或适配器LUID（D3D）字段，其他字段被忽略。这可以用来限制结果到给定的适配器。此时返回的列表将包含1个或0个元素。
注意，在前一段代码片段中，looksGood() 函数实现无法基于真实适配器/物理设备身份执行任何平台特定过滤，比如 Windows 上的适配器 LUID 或 Vulkan 中的 VkPhysicalDevice。这是因为 `QRhiDriverInfo` 不包含平台特定数据。相反，使用`nativeHandles` 来过滤结果，已在 enumerateAdapters()。 中。
以下两个片段，以Direct 3D 12为例，在实际操作中是等价的：

**官方示例：**

```cpp
 QRhiVulkanInitParams initParams;
 initParams.inst = &vulkanInstance;
 QRhi::AdapterList adapters = QRhi::enumerateAdapters(QRhi::Vulkan, &initParams);
 QRhiAdapter *chosenAdapter = nullptr;
 for (QRhiAdapter *adapter : adapters) {
     if (looksGood(adapter->info())) {
         chosenAdapter = adapter;
         break;
     }
 }
 QRhi *rhi = QRhi::create(QRhi::Vulkan, &initParams, {}, nullptr, chosenAdapter);
 qDeleteAll(adapters);
```

### `QRhi::FrameOpResult QRhi::finish()`

**作用与语义：**

等待图形队列中的任何工作（如适用）完成，然后执行所有延迟操作，如完成读回和资源释放。可以在帧内外调用，但不能在传递中调用。帧内表示提交命令缓冲区上的任何工作。
注意：请避免使用该函数。在交换链框架中，需要在固定点等待结果时，可能需要使用该功能。

### `bool QRhi::isClipDepthZeroToOne() const`

**作用与语义：**

如果底层图形API在剪辑空间中使用深度范围[0， 1]，返回`true`。
实际上，这`false`仅适用于 OpenGL，因为 OpenGL 使用投影后的深度范围 [-1， 1]。（不要与由 glDepthRange() 控制的 NDC 到窗口映射混淆，后者使用 [0， 1] 范围，除非被 `QRhiViewport` 覆盖）在某些 OpenGL 版本中可以使用 glClipControl() 来更改此功能，但 OpenGL `QRhi` 后端不使用该函数，因为 OpenGL ES 或 4.5 以下版本中不支持该功能。
注意：`clipSpaceCorrMatrix()`在返回的矩阵中包含相应的调整。因此，许多`QRhi`用户无需采取其他措施，除了预先将投影矩阵与`clipSpaceCorrMatrix()`相乘即可。然而，某些图形技术，如某些类型的阴影映射，涉及在着色器中处理和输出深度值。这些需要查询并考虑该函数的值。

### `bool QRhi::isDeviceLost() const`

**作用与语义：**

如果图形设备丢失，则返回为真。
设备的丢失通常在`beginFrame()`、`endFrame()`或`QRhiSwapChain::createOrResize()`中被检测，具体取决于后端和底层的原生API。最常见的是`endFrame()`，因为呈现就是在该处进行。在某些后端`QRhiSwapChain::createOrResize()`也可能因设备丢失而失败。因此，这个功能作为一种通用方式，用来检查设备丢失是否被之前的操作检测到。
设备丢失后，不应再通过`QRhi`进行操作。相反，应释放所有`QRhi`资源，然后销毁`QRhi`。然后可以尝试创建新的`QRhi`。如果成功，所有图形资源必须重新初始化。如果失败，则可以反复尝试。
虽然简单的应用程序可能选择不在意设备丢失，但在常用的桌面平台上，设备丢失可能因多种原因发生，包括物理断开显卡连接、禁用设备或驱动程序、卸载或升级显卡驱动，或因错误导致显卡设备重置。其中一些情况也可能发生在完全正常的情况下，例如在Qt应用运行时，将显卡驱动升级到新版本是常见的任务。用户很可能期望应用程序能够存活下来，即使应用正在使用OpenGL或Direct3D等API。
Qt基于`QRhi`构建的自有框架，如Qt Quick，预计在设备丢失发生时能够处理并采取适当措施。如果图形资源的数据（如纹理和缓冲区）仍然存在于CPU端，那么在应用层面可能完全察觉不到此类事件，因为图形资源可以无缝地重新初始化。然而，直接与`QRhi`合作的应用和库应准备自行检查和处理设备丢失情况。
注意：使用 OpenGL，应用程序可能需要通过在`QOpenGLContext`上设置 `QSurfaceFormat::ResetNotification` 来选择上下文重置通知。这通常通过在 `QRhiGles2InitParams::format` 中启用该标志来实现。但请注意，即使未设置该标志，某些系统仍可能触发上下文重置情况。

### `bool QRhi::isFeatureSupported(QRhi::Feature feature) const`

**作用与语义：**

如果支持指定`feature`，返回`true`。

### `bool QRhi::isRecordingFrame() const`

**作用与语义：**

当存在活跃帧时，返回为真，意味着存在一个`beginFrame()`（或`beginOffscreenFrame()`）但尚未对应的`endFrame()`（或`endOffscreenFrame()`）。

### `bool QRhi::isTextureFormatSupported(QRhiTexture::Format format, QRhiTexture::Flags flags = {}) const`

**作用与语义：**

如果支持`flags`修改的指定纹理，返回`format`返回`true`。
该查询支持无压缩和压缩格式。

### `bool QRhi::isYUpInFramebuffer() const`

**作用与语义：**

如果底层图形API在帧缓冲区和图片中Y轴指向上方，返回`true`。
实际上，这`true`适用于OpenGL。

### `bool QRhi::isYUpInNDC() const`

**作用与语义：**

如果底层图形API的Y轴指向其归一化设备坐标系的Y轴指向上方，返回`true`。
实际上，这`false`仅适用于瓦尔坎。
注意：`clipSpaceCorrMatrix()`返回矩阵中包含相应的调整（使Y点向上）。

### `bool QRhi::makeThreadLocalNativeContextCurrent()`

**作用与语义：**

使用 OpenGL 时，这使得 OpenGL 上下文在当前线程上保持最新状态。该函数对其他后端没有影响。
调用该函数通常在 Qt 框架代码中相关，因为需要确保应用程序提供的外部 OpenGL 代码在直接使用 OpenGL 的情况下仍能像以前一样运行，只要`QRhi`使用 OpenGL 后端。
失败时返回 false，类似于 `QOpenGLContext::makeCurrent()`。操作失败时，可以调用 `isDeviceLost()` 来判断上下文丢失情况。这种检查等同于通过`QOpenGLContext::isValid()`检查。

### `[static] int QRhi::mipLevelsForSize(const QSize &size)`

**作用与语义：**

返回给定`size`的MIP级别数量。

### `const QRhiNativeHandles *QRhi::nativeHandles()`

**作用与语义：**

返回指向后端特定设备、上下文及类似概念的本地对象集合的指针。
可根据情况选角为`QRhiVulkanNativeHandles`、`QRhiD3D11NativeHandles`、`QRhiD3D12NativeHandles`、`QRhiGles2NativeHandles`或`QRhiMetalNativeHandles`。
注意：无论是返回指针还是任何本地对象，都不会转让所有权。

### `QRhiBuffer *QRhi::newBuffer(QRhiBuffer::Type type, QRhiBuffer::UsageFlags usage, quint32 size)`

**作用与语义：**

返回一个包含指定`type`、`usage`和`size`的新缓冲区。
注意：部分`usage`和`type`组合可能并非所有后端都支持。请参见 `UsageFlags` 和功能标志。
注意：后端可以选择分配大于`size`的缓冲区。这对应用程序透明，因此对`size`值没有特殊限制。`QRhiBuffer::size()`总是会报告`size`请求的值。

### `QRhiComputePipeline *QRhi::newComputePipeline()`

**作用与语义：**

返回一个新的计算流水线资源。
注意：只有当`Compute`功能被报告为支持时，计算才可用。

### `QRhiGraphicsPipeline *QRhi::newGraphicsPipeline()`

**作用与语义：**

返回一个新的图形管道资源。

### `QRhiRenderBuffer *QRhi::newRenderBuffer(QRhiRenderBuffer::Type type, const QSize &pixelSize, int sampleCount = 1, QRhiRenderBuffer::Flags flags = {}, QRhiTexture::Format backingFormatHint = QRhiTexture::UnknownFormat)`

**作用与语义：**

返回一个新的渲染缓冲区，包含指定的`type`、`pixelSize`、`sampleCount`和`flags`。
当`backingFormatHint`设置为非`QRhiTexture::UnknownFormat`的纹理格式时，后端可以用它来决定渲染缓冲区背后的存储格式。
注意：`backingFormatHint`通常在涉及多采样和浮点纹理格式时变得相关：渲染成多采样`QRhiRenderBuffer`再解析为非 RGBA8 `QRhiTexture`意味着（在某些图形 API 下）支持`QRhiRenderBuffer`的存储使用匹配的非 RGBA8 格式。这意味着传递类似 `QRhiTexture::RGBA32F` 格式很重要，因为后端通常默认选择 `QRhiTexture::RGBA8`，但后来在尝试在`QRhiTextureRenderTarget`的颜色附件中设置 RGBA8->RGBA32F 多采样解析时会出问题。

### `QRhiSampler *QRhi::newSampler(QRhiSampler::Filter magFilter, QRhiSampler::Filter minFilter, QRhiSampler::Filter mipmapMode, QRhiSampler::AddressMode addressU, QRhiSampler::AddressMode addressV, QRhiSampler::AddressMode addressW = QRhiSampler::Repeat)`

**作用与语义：**

返回一个新的采样器，包含指定的放大滤镜`magFilter`、压缩滤波器`minFilter`、多频映射模式`mipmapMode`以及寻址（环绕）模式`addressU`、`addressV`和`addressW`。
注意：将`mipmapMode`设置为非`None`值意味着所有相关MIP级别的图像将通过纹理上传或调用该采样器所用纹理的`generateMips()`提供。尝试使用采样器时，纹理中没有所有相关MIP级别数据，会导致渲染错误，具体行为取决于底层图形API。

### `QRhiShaderResourceBindings *QRhi::newShaderResourceBindings()`

**作用与语义：**

返回一个新的着色器资源绑定集合资源。

### `[since 6.9] QRhiShadingRateMap *QRhi::newShadingRateMap()`

**作用与语义：**

返回一个新的着色率地图对象。

### `QRhiSwapChain *QRhi::newSwapChain()`

**作用与语义：**

退回一条新的掉期链。

### `QRhiTexture *QRhi::newTexture(QRhiTexture::Format format, const QSize &pixelSize, int sampleCount = 1, QRhiTexture::Flags flags = {})`

**作用与语义：**

返回一个新的1D或2D纹理，具有指定的`format`、`pixelSize`、`sampleCount`和`flags`。
一维纹理数组必须在`flags`中设置`QRhiTexture::OneDimensional`。如果`pixelSize`高度为0，该函数会隐式设置该标志。
注意：`format` 指定了请求的内部和外部格式，意味着上传到纹理的数据必须兼容，而原生纹理内部可以使用该格式（但不保证，至少在 OpenGL 的情况下）。
注意：只有当`OneDimensionalTextures`功能在运行时报告支持时，1D纹理才有功能。此外，1D纹理上的mipmap只有在`OneDimensionalTextureMipmaps`功能在运行时被报告时才有功能。

### `QRhiTexture *QRhi::newTexture(QRhiTexture::Format format, int width, int height, int depth, int sampleCount = 1, QRhiTexture::Flags flags = {})`

**作用与语义：**

返回一个新的1D、2D或3D纹理，包含指定的`format`、`width`、`height`、`depth`、`sampleCount`和`flags`。
这种重载适用于3D纹理，因为它允许指定`depth`。3D纹理必须在`flags`中设置`QRhiTexture::ThreeDimensional`，但使用该超载时可以省略，因为当`depth`大于0时，标志是隐式设置的。对于1D、2D和立方体纹理，`depth`应设为0。
一维纹理必须`QRhiTexture::OneDimensional` 设置在`flags`。如果 `height` 和 `depth` 都是 0，这个重载会隐式设置该标志。
注意：3D贴图只有在运行时`ThreeDimensionalTextures`功能被报告为支持时才可使用。
注意：1D纹理只有在`OneDimensionalTextures`功能在运行时报告支持时才有功能。此外，1D纹理上的mipmap只有在运行时报告`OneDimensionalTextureMipmaps`特征时才有功能。

### `QRhiTexture *QRhi::newTextureArray(QRhiTexture::Format format, int arraySize, const QSize &pixelSize, int sampleCount = 1, QRhiTexture::Flags flags = {})`

**作用与语义：**

返回一个新的1D或2D纹理数组，包含指定的`format`、`arraySize`、`pixelSize`、`sampleCount`和`flags`。
该函数隐式地将`QRhiTexture::TextureArray`置于`flags`中。
一维纹理数组必须`QRhiTexture::OneDimensional` 在`flags`中设置。如果`pixelSize`高度为0，该函数会隐式设置该标志。
注意：不要将纹理数组与纹理的数组混淆。该函数创建的`QRhiTexture`可用于着色器中的1D或2D数组采样器，例如：`layout(binding = 1) uniform sampler2DArray texArr;`。纹理数组指通过`QRhiShaderResourceBinding::sampledTextures()`和>计数1暴露给着色器的贴图列表，并在着色器中声明，例如：`layout(binding = 1) uniform sampler2D textures[4];`。
注意：只有当`TextureArrays`功能在运行时报告为支持时，此功能才有效。
注意：1D纹理只有在`OneDimensionalTextures`功能在运行时报告支持时才有功能。此外，1D纹理上的mipmap只有在`OneDimensionalTextureMipmaps`功能在运行时报告时才有功能。

### `QRhiTextureRenderTarget *QRhi::newTextureRenderTarget(const QRhiTextureRenderTargetDescription &desc, QRhiTextureRenderTarget::Flags flags = {})`

**作用与语义：**

返回一个新的纹理渲染目标，颜色和深度/模板附件均在`desc`中提供，并带有指定的`flags`。

### `QRhiResourceUpdateBatch *QRhi::nextResourceUpdateBatch()`

**作用与语义：**

返回一个可用的空批次，可以记录复制类型的操作。
注意：返回值不属于调用者所有，且绝不能销毁。批处理通过传递给`QRhiCommandBuffer::beginPass()`、`QRhiCommandBuffer::endPass()`或`QRhiCommandBuffer::resourceUpdate()`，或调用`QRhiResourceUpdateBatch::release()`返回池以供重复使用。
注意：可以调用外部`beginFrame()` - `endFrame()` 因为批处理实例只是单独收集数据，不执行任何操作。
由于不绑定被录制的帧，以下序列是有效的，例如：
警告：每个`QRhi`最大批次数为64个。当达到此限制时，函数将返回空值，直到有批次返回到池中。

**官方示例：**

```cpp
 rhi->beginFrame(swapchain);
 QRhiResourceUpdateBatch *u = rhi->nextResourceUpdateBatch();
 u->uploadStaticBuffer(buf, data);
 // ... do not commit the batch
 rhi->endFrame();
 // u stays valid (assuming buf stays valid as well)
 rhi->beginFrame(swapchain);
 swapchain->currentFrameCommandBuffer()->resourceUpdate(u);
 // ... draw with buf
 rhi->endFrame();
```

### `QByteArray QRhi::pipelineCacheData()`

**作用与语义：**

返回一个二进制数据块，包含从`QRhiGraphicsPipeline`收集的数据，并在该`QRhi`的生命周期内成功创建`QRhiComputePipeline`。
通过保存缓存数据，然后在后续运行中重新加载缓存数据，可以减少流水线和着色器创建时间。缓存及其序列化版本具体包含什么内容并未明确说明，始终取决于所用后端，且在某些情况下还取决于图形API的具体实现。
当`PipelineCacheDataLoadSave`被报告为无支撑时，返回的`QByteArray`为空。
当调用`create()`时未指定`EnablePipelineCacheDataSave`标志，返回的`QByteArray`可能为空，即使支持`PipelineCacheDataLoadSave`功能。
当返回的数据非空时，它总是针对Qt版本和`QRhi`后端。此外，在某些情况下，图形设备和所用驱动版本存在强烈依赖关系。`QRhi`负责添加适当的头部和保护措施，确保数据始终安全传递给`setPipelineCacheData()`，因此尝试从另一个版本驱动运行中加载数据时，可以安全优雅地处理。
注意：调用`releaseCachedResources()`可能会根据后端而清除收集的流水线数据。随后调用该函数可能无法返回任何数据。
有关该功能详情，请参见`EnablePipelineCacheDataSave`。
注意：尽量减少对该函数的调用次数。检索 blob 并不总是一项便宜的操作，因此该函数应仅以较低频率调用，理想情况下只调用一次，例如在关闭应用程序时。

### `[static] bool QRhi::probe(QRhi::Implementation impl, QRhiInitParams *params)`

**作用与语义：**

如果`create()`在调用给定`impl`和`params`时，可以预期成功，则返回为真。
对于某些后端来说，这相当于调用`create()`，检查返回值，然后销毁所得`QRhi`。
对于其他平台，尤其是 Metal，可能有特定的探测实现，允许以更轻量级的方式测试，同时不会在调试输出中出现故障警告。

### `void QRhi::releaseCachedResources()`

**作用与语义：**

尝试释放后端缓存中的资源。这可以包括CPU和GPU资源。只有可以自动重建的内存和资源才在作用域内。例如，如果后端`QRhiGraphicsPipeline`实现维护着色器编译结果的缓存，调用该函数会导致该缓存被清空，从而可能释放内存和图形资源。
在资源受限的环境中调用该函数是合理的，因为在一定程度上需要确保最小的资源使用，但牺牲了性能。

### `void QRhi::removeCleanupCallback(const void *key)`

**作用与语义：**

取消与`key`的回调。如果没有`key`注册清理回调，该函数则无效。没有密钥注册的回调无法移除。

### `int QRhi::resourceLimit(QRhi::ResourceLimit limit) const`

**作用与语义：**

返回指定资源`limit`的值。
这些值在初始化时预期会被后端查询，这意味着调用该函数是轻量操作。

### `void QRhi::setPipelineCacheData(const QByteArray &data)`

**作用与语义：**

在适用时，`data`加载到管道缓存中。
当`PipelineCacheDataLoadSave`被报告为不支持时，该函数可以安全调用，但不会产生任何影响。
`pipelineCacheData()`返回的blob总是针对Qt版本、`QRhi`后端，有时也针对图形设备和特定版本的图形驱动。`QRhi`负责添加适当的头部和保护措施，确保数据始终能安全传递到该函数。如果存在不匹配，例如驱动程序已升级到新版本，或数据来自其他`QRhi`后端，会打印警告，`data`则被安全忽略。
在 Vulkan 中，该缓存直接映射到 VkPipelineCache。调用该函数会创建一个新的 Vulkan 流水线缓存对象，其初始数据来源于 `data`。随后所有后续创建的 `QRhiGraphicsPipeline` 和 `QRhiComputePipeline` 对象都会使用该流水线缓存对象，从而可能加速流水线的创建。
对于其他API来说，没有真正的流水线缓存，但它们可能会提供来自着色器编译（D3D）或程序二进制（OpenGL）的字节码缓存。在运行时大量从源代码编译着色器的应用中，如果“流水线缓存”是用该函数预种的，后续运行中可以带来显著提升。
注意：`QRhi`无法保证`data`会影响流水线和着色器创建性能。对于像Vulkan这样的API，驱动程序可以决定`data`是否被用于某种目的，或者是否被忽略。
有关该功能的更多信息，请参见`EnablePipelineCacheDataSave`。
注意：`QRhi`提供的该机制独立于驱动程序自身的内部缓存机制（如果有的话）。这意味着，根据图形API及其实现，获取和重新加载`data`的具体效果无法预测。如果Qt控制之外的其他缓存机制已经激活，性能提升可能根本看不到。
注意：尽量减少对该函数的调用次数。加载blob并不总是一项廉价操作，因此该函数应仅以较低频率调用，理想情况下只调用一次，例如启动应用程序时。
警告：串行化的流水线缓存数据被假定为可信内容。Qt 对`data`中包含的头部和元数据进行稳健的解析，但建议应用开发者切勿传递来自不受信任来源的数据。

### `[since 6.9] void QRhi::setQueueSubmitParams(QRhiNativeHandles *params)`

**作用与语义：**

在后端和图形API的情况下，该函数允许为下一次向图形命令队列提交命令提供额外参数。
特别是在 Vulkan 中，这允许传递一份 Vulkan 信号量对象列表，供 `vkQueueSubmit()` 信号并等待。`params` 必须是`QRhiVulkanQueueSubmitParams`。这在某些高级用例中尤为重要，例如执行原生 Vulkan 调用时，需要等待并信号应用程序自定义 Vulkan 渲染或计算代码管理的 Vk。此外，这也允许在下一`vkQueuePresentKHR()`指定额外的信号量等待。
注意：该功能仅影响下一次队列提交，该提交时间为`endFrame()`、`endOffscreenFrame()`或`finish()`。当前队列在`endFrame()`中进行。
在许多其他后端中，这个函数的实现是无运操作的。

### `[static] QSize QRhi::sizeForMipLevel(int mipLevel, const QSize &baseLevelSize)`

**作用与语义：**

返回给定`mipLevel`的纹理图像尺寸，基于`baseLevelSize`中给出的0级尺寸计算得出。

### `QRhiStats QRhi::statistics() const`

**作用与语义：**

收集并返回有关图形资源的时间和分配统计数据。
关于内存分配的数据仅在某些后端可用，而这些操作由 Qt 控制。在图形 API 中，如果没有对资源内存分配的底层控制，这永远不会被支持，结果中所有相关字段均为 0。
特别是在Vulkan中，这些值始终有效，并且会从底层的内存分配库中查询。这有助于了解活动缓冲区和纹理的内存需求。
Direct 3D 12 也是如此。除了内存分配库的统计数据外，这里的结果还包括一个 `totalUsageBytes` 字段，报告总大小，包括不受内存分配库控制的额外资源（如交换链缓冲区、描述符堆等），这些数据由 DXGI 报告。
这些值对应于所有类型的内存组合。（例如，如果是独立GPU的话，是视频系统）。
大多数后端都能获得额外数据，比如图形和计算流水线创建所花费的总时间（毫秒计）（通常涉及着色器编译或缓存查找，以及可能昂贵的处理）。
注意：如管道创建等操作的经过时间可能受多种因素影响。不同后端不应对结果进行比较，因为“管道”的概念以及在调用`QRhiGraphicsPipeline::create()`时实际操作的具体过程，在图形API及其实现之间差异很大。
注意：此外，许多驱动程序可能会为着色器、程序、流水线采用各种缓存策略。（独立于Qt自身的类似功能，如`setPipelineCacheData()`或OpenGL专用程序二进制磁盘缓存。）由于此类内部行为对API客户端透明，Qt和`QRhi`对缓存的具体缓存策略、持久性、缓存数据失效等既不了解也不控制。在读取时序时，如流水线创建所花费的时间，应考虑驱动程序级缓存机制的潜在存在及未说明行为。

### `QList<int> QRhi::supportedSampleCounts() const`

**作用与语义：**

返回支持的样本计数列表。
一个典型的例子是 （1， 2， 4， 8）。
有些后端支持的数值列表是预先固定的，而有些则通过（物理）设备属性指示运行时支持的内容。

### `[since 6.9] QList<QSize> QRhi::supportedShadingRates(int sampleCount) const`

**作用与语义：**

返回 指定`sampleCount`支持的变量着色率列表。
1x1始终支持。

### `QThread *QRhi::thread() const`

**作用与语义：**

返回`QRhi`所在的帖子`initialized`。

### `int QRhi::ubufAligned(int v) const`

**作用与语义：**

返回与`ubufAlignment()`给出的均匀缓冲区对齐`v`值（通常是偏移量）。

### `int QRhi::ubufAlignment() const`

**作用与语义：**

返回最小均匀缓冲区偏移对齐（字节单位）。通常为256。
尝试绑定一个偏移量不对齐的均匀缓冲区，会导致失败，具体取决于后端和底层的图形 API 。

### `[static] QRhiSwapChainProxyData QRhi::updateSwapChainProxyData(QRhi::Implementation impl, QWindow *window)`

**作用与语义：**

生成并返回一个包含`impl`指定后端和图形API特有的不透明数据的`QRhiSwapChainProxyData`结构体。`window`是交换链的目标`QWindow`。
返回的结构体可以传递给`QRhiSwapChain::setProxyData()`。这在线程渲染系统中很合理：这个静态函数预期在主线程（GUI）上调用，不同于所有`QRhi`操作，然后传输到与`QRhi`和`QRhiSwapChain`工作的线程，再传递给交换链。这使得可以进行仅安全调用主线程的原生平台查询，例如从NSView查询CAMetalLayer，然后将数据传递给渲染线程上的`QRhiSwapChain`。以Metal为例，在专用渲染线程上访问view.layer会在Xcode线程检查器中发出警告。通过数据代理机制，可以避免这种情况。
当线程不涉及时，无需生成和传递`QRhiSwapChainProxyData`：后端保证能够自行查询所需内容，如果所有内容都存在主线（GUI）线程，这就足够了。
注意：`impl`应与创建`QRhi`时的材料相匹配。例如，在非苹果平台上用`QRhi::Metal`调用不会产生任何有用的数据。

### `[alias, since 6.7] QRhiShaderResourceBindingSet`

**作用与语义：**

`QRhiShaderResourceBindings`的同义词。
这种typedef是在Qt 6.7中引入的。

### `(since 6.10) AdapterList`

**作用与语义：**

`QVector`<`QRhiAdapter`的同义词 *>。
这种类型防御是在Qt 6.10中引入的。

### `enum BeginFrameFlag { }`

**作用与语义：**

`QRhi::beginFrame()`的旗标值。
BeginFrameFlags 类型是 QFlags 的 typedef<BeginFrameFlag>。它存储 BeginFrameFlag 值的 OR 组合。

### `flags BeginFrameFlags`

**作用与语义：**

`QRhi::beginFrame()`的旗标值。
BeginFrameFlags 类型是 QFlags 的 typedef<BeginFrameFlag>。它存储 BeginFrameFlag 值的 OR 组合。

### `enum EndFrameFlag { SkipPresent }`

**作用与语义：**

标志值`QRhi::endFrame()`。
- `QRhi::SkipPresent`：`1 << 0`;指定当前命令不排队或不调用swapBuffers。这样就不会显示任何图像。不建议生成多个帧，且所有帧都设置了该标志（除非用于基准测试——但请记住后端在等待命令完成而不呈现时行为可能不同，因此结果无法比较）
EndFrameFlags 类型是 QFlags 的 typedef<EndFrameFlag>。它存储 EndFrameFlag 值的 OR 组合。

### `flags EndFrameFlags`

**作用与语义：**

标志值`QRhi::endFrame()`。
- `QRhi::SkipPresent`：`1 << 0`;指定当前命令不排队或不调用swapBuffers。这样就不会显示任何图像。不建议生成多个帧，且所有帧都设置了该标志（除非用于基准测试——但请记住后端在等待命令完成而不呈现时行为可能不同，因此结果无法比较）
EndFrameFlags 类型是 QFlags 的 typedef<EndFrameFlag>。它存储 EndFrameFlag 值的 OR 组合。

### `enum Flag { EnableDebugMarkers, EnableTimestamps, PreferSoftwareRenderer, EnablePipelineCacheDataSave, SuppressSmokeTestWarnings }`

**作用与语义：**

描述需要启用哪些特殊功能。
- `QRhi::EnableDebugMarkers`：`1 << 0`;启用调试标记组。如果没有这个框架，调试功能如在外部GPU调试工具中显示调试组和自定义资源名称，将无法使用，`QRhiCommandBuffer::debugMarkBegin()`等功能将变得无运。避免在生产版本中启用，因为可能会带来小幅性能影响。当`QRhi::DebugMarkers`功能未被报告为支持时，该功能无效。
- `QRhi::EnableTimestamps`：`1 << 3`;启用 GPU 时间戳收集。未设置时，`QRhiCommandBuffer::lastCompletedGpuTime()` 总是返回 0。仅在需要时启用，因为根据底层图形 API 可能涉及少量额外工作（例如时间戳查询）。当 `QRhi::Timestamps` 功能未被报告为支持时，该功能无影响。
- `QRhi::PreferSoftwareRenderer`：`1 << 1`;表示后端应优先选择在CPU上用软件渲染的适配器或物理设备。例如，Direct3D通常会提供“基础渲染驱动程序”适配器，`DXGI_ADAPTER_FLAG_SOFTWARE`。设置该标志会要求后端选择该适配器，只要没有被其他后端特定方式强制使用。在Vulkan中，这对应于优先使用带有`VK_PHYSICAL_DEVICE_TYPE_CPU`的物理设备。当不可用或无法确定适配器/设备是否基于软件时，该标志被忽略。图形API中也可能忽略该标志，这些API没有枚举适配器/设备的概念和方式。
- `QRhi::EnablePipelineCacheDataSave`：`1 << 2`;在适用情况下，启用获取流水线缓存内容。未设置时，`pipelineCacheData()`始终返回空 blob。在不支持检索和恢复流水线缓存内容的后端，该标志无效，序列化缓存数据始终为空。该标志提供了选择加入机制，因为维护相关数据结构的成本对某些后端来说并不低。在 Vulkan 中，该功能直接映射到 VkPipelineCache、vkGetPipelineCacheData 和 VkPipelineCacheCreateInfo：:p InitialData。Direct3D 11 没有真正的 pipline 缓存，但 HLSL->DXBC 编译的结果会被存储，并可通过该机制进行序列化/反序列化。这使得未来在带有 HLSL 源代码而非离线预编译字节码的着色器应用中，可以跳过耗时的 D3DCompile() 缓存。如果大量 HLSL 源编译工作进行，这能大幅提升启动和加载时间。OpenGL 通过检索和加载着色器程序二进制文件（如果驱动程序支持）来模拟“流水线缓存”。OpenGL 还提供了额外的基于磁盘的缓存机制，用于 Qt 提供的着色器/程序二进制文件。一旦设置了该标志，写入这些机制可能会被禁用，因为将程序二进制文件存储到多个缓存中并不合理。
- `QRhi::SuppressSmokeTestWarnings`：`1 << 4`;表示在后端相关时，某些非致命`QRhi::create()`故障不应产生`qWarning()`调用。例如，在D3D11中，传递该标志会使许多因失败而出现的警告消息`QRhi::create()`转为分类调试打印，归入常用的`qt.rhi.general`日志分类。这可以被像 Qt Quick 这样的引擎使用，这些引擎具有备份逻辑，即它们会用不同的标志集（如 PreferSoftwareRenderer）重试调用 `create()`，以隐藏第一次尝试失败时输出的无条件警告`create()`。
Flags 类型是 QFlags 的 typedef<Flag>。它存储 Flag 值的 OR 组合。

### `flags Flags`

**作用与语义：**

描述需要启用哪些特殊功能。
- `QRhi::EnableDebugMarkers`：`1 << 0`;启用调试标记组。如果没有这个框架，调试功能如在外部GPU调试工具中显示调试组和自定义资源名称，将无法使用，`QRhiCommandBuffer::debugMarkBegin()`等功能将变得无运。避免在生产版本中启用，因为可能会带来小幅性能影响。当`QRhi::DebugMarkers`功能未被报告为支持时，该功能无效。
- `QRhi::EnableTimestamps`：`1 << 3`;启用 GPU 时间戳收集。未设置时，`QRhiCommandBuffer::lastCompletedGpuTime()` 总是返回 0。仅在需要时启用，因为根据底层图形 API 可能涉及少量额外工作（例如时间戳查询）。当 `QRhi::Timestamps` 功能未被报告为支持时，该功能无影响。
- `QRhi::PreferSoftwareRenderer`：`1 << 1`;表示后端应优先选择在CPU上用软件渲染的适配器或物理设备。例如，Direct3D通常会提供“基础渲染驱动程序”适配器，`DXGI_ADAPTER_FLAG_SOFTWARE`。设置该标志会要求后端选择该适配器，只要没有被其他后端特定方式强制使用。在Vulkan中，这对应于优先使用带有`VK_PHYSICAL_DEVICE_TYPE_CPU`的物理设备。当不可用或无法确定适配器/设备是否基于软件时，该标志被忽略。图形API中也可能忽略该标志，这些API没有枚举适配器/设备的概念和方式。
- `QRhi::EnablePipelineCacheDataSave`：`1 << 2`;在适用情况下，启用获取流水线缓存内容。未设置时，`pipelineCacheData()`始终返回空 blob。在不支持检索和恢复流水线缓存内容的后端，该标志无效，序列化缓存数据始终为空。该标志提供了选择加入机制，因为维护相关数据结构的成本对某些后端来说并不低。在 Vulkan 中，该功能直接映射到 VkPipelineCache、vkGetPipelineCacheData 和 VkPipelineCacheCreateInfo：:p InitialData。Direct3D 11 没有真正的 pipline 缓存，但 HLSL->DXBC 编译的结果会被存储，并可通过该机制进行序列化/反序列化。这使得未来在带有 HLSL 源代码而非离线预编译字节码的着色器应用中，可以跳过耗时的 D3DCompile() 缓存。如果大量 HLSL 源编译工作进行，这能大幅提升启动和加载时间。OpenGL 通过检索和加载着色器程序二进制文件（如果驱动程序支持）来模拟“流水线缓存”。OpenGL 还提供了额外的基于磁盘的缓存机制，用于 Qt 提供的着色器/程序二进制文件。一旦设置了该标志，写入这些机制可能会被禁用，因为将程序二进制文件存储到多个缓存中并不合理。
- `QRhi::SuppressSmokeTestWarnings`：`1 << 4`;表示在后端相关时，某些非致命`QRhi::create()`故障不应产生`qWarning()`调用。例如，在D3D11中，传递该标志会使许多因失败而出现的警告消息`QRhi::create()`转为分类调试打印，归入常用的`qt.rhi.general`日志分类。这可以被像 Qt Quick 这样的引擎使用，这些引擎具有备份逻辑，即它们会用不同的标志集（如 PreferSoftwareRenderer）重试调用 `create()`，以隐藏第一次尝试失败时输出的无条件警告`create()`。
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

`QRhi` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
