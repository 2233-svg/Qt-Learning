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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 71 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `[alias, since 6.10] QRhi::AdapterList`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QRhi` 的配置属性。初始化或状态切换时通过 `setAdapterList(...)` 设置，之后用 `AdapterList()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:AdapterList`。
- 属性名：`QRhi`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QRhi::BeginFrameFlagflags QRhi::BeginFrameFlags`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QRhi` 暴露的类型声明 `起始位置、Frame、Flagflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:BeginFrameFlagflags QRhi::BeginFrameFlags`。
- 属性名：`QRhi`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QRhi::EndFrameFlagflags QRhi::EndFrameFlags`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QRhi` 暴露的类型声明 `结束、Frame、Flagflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:EndFrameFlagflags QRhi::EndFrameFlags`。
- 属性名：`QRhi`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QRhi::Feature`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QRhi` 暴露的类型声明 `Feature`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Feature`。
- 属性名：`QRhi`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QRhi::Flagflags QRhi::Flags`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QRhi` 暴露的类型声明 `Flagflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Flagflags QRhi::Flags`。
- 属性名：`QRhi`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QRhi::FrameOpResult`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QRhi` 暴露的类型声明 `Frame、Op、结果`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:FrameOpResult`。
- 属性名：`QRhi`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QRhi::Implementation`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QRhi` 暴露的类型声明 `Implementation`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Implementation`。
- 属性名：`QRhi`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QRhi::ResourceLimit`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QRhi` 暴露的类型声明 `Resource、Limit`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:ResourceLimit`。
- 属性名：`QRhi`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QRhi::~QRhi()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QRhi` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhi::addCleanupCallback(const QRhi::CleanupCallback &callback)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QRhi` 添加依赖、数据或子对象的 API `addCleanupCallback`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `callback`：类型为 `const QRhi::CleanupCallback &`。没有默认值，调用时必须提供。回调或函数对象。要确认可调用签名、捕获对象生命周期和执行线程，不要在回调中做长时间阻塞工作。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhi::addCleanupCallback(const void *key, const QRhi::CleanupCallback &callback)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QRhi` 添加依赖、数据或子对象的 API `addCleanupCallback`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `key`：类型为 `const void *`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `callback`：类型为 `const QRhi::CleanupCallback &`。没有默认值，调用时必须提供。回调或函数对象。要确认可调用签名、捕获对象生命周期和执行线程，不要在回调中做长时间阻塞工作。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhi::Implementation QRhi::backend() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhi::backend` 用于计算、查询或取得与“backend”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRhi::Implementation`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhi::Implementation`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const char *QRhi::backendName() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhi::backendName` 用于计算、查询或取得与“backend、名称”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const char *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const char *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] const char *QRhi::backendName(QRhi::Implementation impl)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `backendName`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`const char *`。
- 参数 `impl`：类型为 `QRhi::Implementation`。没有默认值，调用时必须提供。传入 `QRhi::Implementation` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhi::FrameOpResult QRhi::beginFrame(QRhiSwapChain *swapChain, QRhi::BeginFrameFlags flags = {})`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `beginFrame`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QRhi::FrameOpResult`。
- 参数 `swapChain`：类型为 `QRhiSwapChain *`。没有默认值，调用时必须提供。传入 `QRhiSwapChain *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `flags`：类型为 `QRhi::BeginFrameFlags`。默认值为 `{}`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhi::FrameOpResult QRhi::beginOffscreenFrame(QRhiCommandBuffer **cb, QRhi::BeginFrameFlags flags = {})`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `beginOffscreenFrame`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QRhi::FrameOpResult`。
- 参数 `cb`：类型为 `QRhiCommandBuffer **`。没有默认值，调用时必须提供。传入 `QRhiCommandBuffer **` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `flags`：类型为 `QRhi::BeginFrameFlags`。默认值为 `{}`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMatrix4x4 QRhi::clipSpaceCorrMatrix() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhi::clipSpaceCorrMatrix` 用于计算、查询或取得与“clip、Space、Corr、Matrix”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMatrix4x4`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMatrix4x4`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QRhi *QRhi::create(QRhi::Implementation impl, QRhiInitParams *params, QRhi::Flags flags, QRhiNativeHandles *importDevice, QRhiAdapter *adapter)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `create`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QRhi *`。
- 参数 `impl`：类型为 `QRhi::Implementation`。没有默认值，调用时必须提供。传入 `QRhi::Implementation` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `params`：类型为 `QRhiInitParams *`。没有默认值，调用时必须提供。传入 `QRhiInitParams *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `flags`：类型为 `QRhi::Flags`。没有默认值，调用时必须提供。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。
- 参数 `importDevice`：类型为 `QRhiNativeHandles *`。没有默认值，调用时必须提供。传入 `QRhiNativeHandles *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `adapter`：类型为 `QRhiAdapter *`。没有默认值，调用时必须提供。传入 `QRhiAdapter *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QRhi *QRhi::create(QRhi::Implementation impl, QRhiInitParams *params, QRhi::Flags flags = {}, QRhiNativeHandles *importDevice = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `create`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QRhi *`。
- 参数 `impl`：类型为 `QRhi::Implementation`。没有默认值，调用时必须提供。传入 `QRhi::Implementation` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `params`：类型为 `QRhiInitParams *`。没有默认值，调用时必须提供。传入 `QRhiInitParams *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `flags`：类型为 `QRhi::Flags`。默认值为 `{}`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。
- 参数 `importDevice`：类型为 `QRhiNativeHandles *`。默认值为 `nullptr`。传入 `QRhiNativeHandles *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QRhi::currentFrameSlot() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhi::currentFrameSlot` 用于计算、查询或取得与“当前、Frame、Slot”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhiDriverInfo QRhi::driverInfo() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhi::driverInfo` 用于计算、查询或取得与“driver、Info”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRhiDriverInfo`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhiDriverInfo`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhi::FrameOpResult QRhi::endFrame(QRhiSwapChain *swapChain, QRhi::EndFrameFlags flags = {})`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `endFrame`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`QRhi::FrameOpResult`。
- 参数 `swapChain`：类型为 `QRhiSwapChain *`。没有默认值，调用时必须提供。传入 `QRhiSwapChain *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `flags`：类型为 `QRhi::EndFrameFlags`。默认值为 `{}`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhi::FrameOpResult QRhi::endOffscreenFrame(QRhi::EndFrameFlags flags = {})`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `endOffscreenFrame`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`QRhi::FrameOpResult`。
- 参数 `flags`：类型为 `QRhi::EndFrameFlags`。默认值为 `{}`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.10] QRhi::AdapterList QRhi::enumerateAdapters(QRhi::Implementation impl, QRhiInitParams *params, QRhiNativeHandles *nativeHandles = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `enumerateAdapters`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QRhi::AdapterList`。
- 参数 `impl`：类型为 `QRhi::Implementation`。没有默认值，调用时必须提供。传入 `QRhi::Implementation` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `params`：类型为 `QRhiInitParams *`。没有默认值，调用时必须提供。传入 `QRhiInitParams *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `nativeHandles`：类型为 `QRhiNativeHandles *`。默认值为 `nullptr`。传入 `QRhiNativeHandles *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhi::FrameOpResult QRhi::finish()`

**API 类别：** 成员函数说明

**中文解读：** `QRhi::finish` 用于计算、查询或取得与“finish”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRhi::FrameOpResult`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhi::FrameOpResult`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QRhi::isClipDepthZeroToOne() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isClipDepthZeroToOne`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QRhi::isDeviceLost() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isDeviceLost`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QRhi::isFeatureSupported(QRhi::Feature feature) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isFeatureSupported`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `feature`：类型为 `QRhi::Feature`。没有默认值，调用时必须提供。传入 `QRhi::Feature` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QRhi::isRecordingFrame() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isRecordingFrame`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QRhi::isTextureFormatSupported(QRhiTexture::Format format, QRhiTexture::Flags flags = {}) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isTextureFormatSupported`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `format`：类型为 `QRhiTexture::Format`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `flags`：类型为 `QRhiTexture::Flags`。默认值为 `{}`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QRhi::isYUpInFramebuffer() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isYUpInFramebuffer`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QRhi::isYUpInNDC() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isYUpInNDC`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QRhi::makeThreadLocalNativeContextCurrent()`

**API 类别：** 成员函数说明

**中文解读：** `QRhi::makeThreadLocalNativeContextCurrent` 用于计算、查询或取得与“make、Thread、Local、Native、Context、当前”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] int QRhi::mipLevelsForSize(const QSize &size)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `mipLevelsForSize`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`int`。
- 参数 `size`：类型为 `const QSize &`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QRhiNativeHandles *QRhi::nativeHandles()`

**API 类别：** 成员函数说明

**中文解读：** `QRhi::nativeHandles` 用于计算、查询或取得与“native、Handles”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QRhiNativeHandles *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QRhiNativeHandles *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhiBuffer *QRhi::newBuffer(QRhiBuffer::Type type, QRhiBuffer::UsageFlags usage, quint32 size)`

**API 类别：** 成员函数说明

**中文解读：** `QRhi::newBuffer` 用于计算、查询或取得与“new、Buffer”相关的操作。调用时要先确认当前状态和 `type`、`usage`、`size` 的有效范围；返回类型是 `QRhiBuffer *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhiBuffer *`。
- 参数 `type`：类型为 `QRhiBuffer::Type`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。
- 参数 `usage`：类型为 `QRhiBuffer::UsageFlags`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `size`：类型为 `quint32`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhiComputePipeline *QRhi::newComputePipeline()`

**API 类别：** 成员函数说明

**中文解读：** `QRhi::newComputePipeline` 用于计算、查询或取得与“new、Compute、Pipeline”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRhiComputePipeline *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhiComputePipeline *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhiGraphicsPipeline *QRhi::newGraphicsPipeline()`

**API 类别：** 成员函数说明

**中文解读：** `QRhi::newGraphicsPipeline` 用于计算、查询或取得与“new、Graphics、Pipeline”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRhiGraphicsPipeline *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhiGraphicsPipeline *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhiRenderBuffer *QRhi::newRenderBuffer(QRhiRenderBuffer::Type type, const QSize &pixelSize, int sampleCount = 1, QRhiRenderBuffer::Flags flags = {}, QRhiTexture::Format backingFormatHint = QRhiTexture::UnknownFormat)`

**API 类别：** 成员函数说明

**中文解读：** `QRhi::newRenderBuffer` 用于计算、查询或取得与“new、渲染、Buffer”相关的操作。调用时要先确认当前状态和 `type`、`pixelSize`、`sampleCount`、`flags`、`backingFormatHint` 的有效范围；返回类型是 `QRhiRenderBuffer *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhiRenderBuffer *`。
- 参数 `type`：类型为 `QRhiRenderBuffer::Type`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。
- 参数 `pixelSize`：类型为 `const QSize &`。没有默认值，调用时必须提供。传入 `const QSize &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sampleCount`：类型为 `int`。默认值为 `1`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `flags`：类型为 `QRhiRenderBuffer::Flags`。默认值为 `{}`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。
- 参数 `backingFormatHint`：类型为 `QRhiTexture::Format`。默认值为 `QRhiTexture::UnknownFormat`。传入 `QRhiTexture::Format` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhiSampler *QRhi::newSampler(QRhiSampler::Filter magFilter, QRhiSampler::Filter minFilter, QRhiSampler::Filter mipmapMode, QRhiSampler::AddressMode addressU, QRhiSampler::AddressMode addressV, QRhiSampler::AddressMode addressW = QRhiSampler::Repeat)`

**API 类别：** 成员函数说明

**中文解读：** `QRhi::newSampler` 用于计算、查询或取得与“new、Sampler”相关的操作。调用时要先确认当前状态和 `magFilter`、`minFilter`、`mipmapMode`、`addressU`、`addressV`、`addressW` 的有效范围；返回类型是 `QRhiSampler *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhiSampler *`。
- 参数 `magFilter`：类型为 `QRhiSampler::Filter`。没有默认值，调用时必须提供。传入 `QRhiSampler::Filter` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `minFilter`：类型为 `QRhiSampler::Filter`。没有默认值，调用时必须提供。传入 `QRhiSampler::Filter` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `mipmapMode`：类型为 `QRhiSampler::Filter`。没有默认值，调用时必须提供。传入 `QRhiSampler::Filter` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `addressU`：类型为 `QRhiSampler::AddressMode`。没有默认值，调用时必须提供。传入 `QRhiSampler::AddressMode` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `addressV`：类型为 `QRhiSampler::AddressMode`。没有默认值，调用时必须提供。传入 `QRhiSampler::AddressMode` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `addressW`：类型为 `QRhiSampler::AddressMode`。默认值为 `QRhiSampler::Repeat`。传入 `QRhiSampler::AddressMode` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhiShaderResourceBindings *QRhi::newShaderResourceBindings()`

**API 类别：** 成员函数说明

**中文解读：** `QRhi::newShaderResourceBindings` 用于计算、查询或取得与“new、Shader、Resource、Bindings”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRhiShaderResourceBindings *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhiShaderResourceBindings *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.9] QRhiShadingRateMap *QRhi::newShadingRateMap()`

**API 类别：** 成员函数说明

**中文解读：** `QRhi::newShadingRateMap` 用于计算、查询或取得与“new、Shading、Rate、映射”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRhiShadingRateMap *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhiShadingRateMap *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhiSwapChain *QRhi::newSwapChain()`

**API 类别：** 成员函数说明

**中文解读：** `QRhi::newSwapChain` 用于计算、查询或取得与“new、Swap、Chain”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRhiSwapChain *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhiSwapChain *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhiTexture *QRhi::newTexture(QRhiTexture::Format format, const QSize &pixelSize, int sampleCount = 1, QRhiTexture::Flags flags = {})`

**API 类别：** 成员函数说明

**中文解读：** `QRhi::newTexture` 用于计算、查询或取得与“new、Texture”相关的操作。调用时要先确认当前状态和 `format`、`pixelSize`、`sampleCount`、`flags` 的有效范围；返回类型是 `QRhiTexture *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhiTexture *`。
- 参数 `format`：类型为 `QRhiTexture::Format`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `pixelSize`：类型为 `const QSize &`。没有默认值，调用时必须提供。传入 `const QSize &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sampleCount`：类型为 `int`。默认值为 `1`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `flags`：类型为 `QRhiTexture::Flags`。默认值为 `{}`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhiTexture *QRhi::newTexture(QRhiTexture::Format format, int width, int height, int depth, int sampleCount = 1, QRhiTexture::Flags flags = {})`

**API 类别：** 成员函数说明

**中文解读：** `QRhi::newTexture` 用于计算、查询或取得与“new、Texture”相关的操作。调用时要先确认当前状态和 `format`、`width`、`height`、`depth`、`sampleCount`、`flags` 的有效范围；返回类型是 `QRhiTexture *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhiTexture *`。
- 参数 `format`：类型为 `QRhiTexture::Format`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `width`：类型为 `int`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `int`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `depth`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sampleCount`：类型为 `int`。默认值为 `1`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `flags`：类型为 `QRhiTexture::Flags`。默认值为 `{}`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhiTexture *QRhi::newTextureArray(QRhiTexture::Format format, int arraySize, const QSize &pixelSize, int sampleCount = 1, QRhiTexture::Flags flags = {})`

**API 类别：** 成员函数说明

**中文解读：** `QRhi::newTextureArray` 用于计算、查询或取得与“new、Texture、Array”相关的操作。调用时要先确认当前状态和 `format`、`arraySize`、`pixelSize`、`sampleCount`、`flags` 的有效范围；返回类型是 `QRhiTexture *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhiTexture *`。
- 参数 `format`：类型为 `QRhiTexture::Format`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `arraySize`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pixelSize`：类型为 `const QSize &`。没有默认值，调用时必须提供。传入 `const QSize &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sampleCount`：类型为 `int`。默认值为 `1`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `flags`：类型为 `QRhiTexture::Flags`。默认值为 `{}`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhiTextureRenderTarget *QRhi::newTextureRenderTarget(const QRhiTextureRenderTargetDescription &desc, QRhiTextureRenderTarget::Flags flags = {})`

**API 类别：** 成员函数说明

**中文解读：** `QRhi::newTextureRenderTarget` 用于计算、查询或取得与“new、Texture、渲染、目标”相关的操作。调用时要先确认当前状态和 `desc`、`flags` 的有效范围；返回类型是 `QRhiTextureRenderTarget *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhiTextureRenderTarget *`。
- 参数 `desc`：类型为 `const QRhiTextureRenderTargetDescription &`。没有默认值，调用时必须提供。传入 `const QRhiTextureRenderTargetDescription &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `flags`：类型为 `QRhiTextureRenderTarget::Flags`。默认值为 `{}`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhiResourceUpdateBatch *QRhi::nextResourceUpdateBatch()`

**API 类别：** 成员函数说明

**中文解读：** `QRhi::nextResourceUpdateBatch` 用于计算、查询或取得与“移动到下一项、Resource、更新、Batch”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRhiResourceUpdateBatch *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhiResourceUpdateBatch *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray QRhi::pipelineCacheData()`

**API 类别：** 成员函数说明

**中文解读：** `QRhi::pipelineCacheData` 用于计算、查询或取得与“pipeline、Cache、数据访问”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] bool QRhi::probe(QRhi::Implementation impl, QRhiInitParams *params)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `probe`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数 `impl`：类型为 `QRhi::Implementation`。没有默认值，调用时必须提供。传入 `QRhi::Implementation` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `params`：类型为 `QRhiInitParams *`。没有默认值，调用时必须提供。传入 `QRhiInitParams *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhi::releaseCachedResources()`

**API 类别：** 成员函数说明

**中文解读：** `QRhi::releaseCachedResources` 用于执行与“释放、Cached、Resources”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhi::removeCleanupCallback(const void *key)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeCleanupCallback`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数 `key`：类型为 `const void *`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QRhi::resourceLimit(QRhi::ResourceLimit limit) const`

**API 类别：** 成员函数说明

**中文解读：** `QRhi::resourceLimit` 用于计算、查询或取得与“resource、Limit”相关的操作。调用时要先确认当前状态和 `limit` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `limit`：类型为 `QRhi::ResourceLimit`。没有默认值，调用时必须提供。传入 `QRhi::ResourceLimit` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhi::setPipelineCacheData(const QByteArray &data)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPipelineCacheData`。调用它会改变 `QRhi` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `data`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.9] void QRhi::setQueueSubmitParams(QRhiNativeHandles *params)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setQueueSubmitParams`。调用它会改变 `QRhi` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `params`：类型为 `QRhiNativeHandles *`。没有默认值，调用时必须提供。传入 `QRhiNativeHandles *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QSize QRhi::sizeForMipLevel(int mipLevel, const QSize &baseLevelSize)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `sizeForMipLevel`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QSize`。
- 参数 `mipLevel`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `baseLevelSize`：类型为 `const QSize &`。没有默认值，调用时必须提供。传入 `const QSize &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhiStats QRhi::statistics() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhi::statistics` 用于计算、查询或取得与“statistics”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRhiStats`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhiStats`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<int> QRhi::supportedSampleCounts() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhi::supportedSampleCounts` 用于计算、查询或取得与“supported、Sample、Counts”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<int>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<int>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.9] QList<QSize> QRhi::supportedShadingRates(int sampleCount) const`

**API 类别：** 成员函数说明

**中文解读：** `QRhi::supportedShadingRates` 用于计算、查询或取得与“supported、Shading、Rates”相关的操作。调用时要先确认当前状态和 `sampleCount` 的有效范围；返回类型是 `QList<QSize>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QSize>`。
- 参数 `sampleCount`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QThread *QRhi::thread() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhi::thread` 用于计算、查询或取得与“thread”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QThread *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QThread *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QRhi::ubufAligned(int v) const`

**API 类别：** 成员函数说明

**中文解读：** `QRhi::ubufAligned` 用于计算、查询或取得与“ubuf、Aligned”相关的操作。调用时要先确认当前状态和 `v` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `v`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QRhi::ubufAlignment() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhi::ubufAlignment` 用于计算、查询或取得与“ubuf、对齐方式”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QRhiSwapChainProxyData QRhi::updateSwapChainProxyData(QRhi::Implementation impl, QWindow *window)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `updateSwapChainProxyData`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QRhiSwapChainProxyData`。
- 参数 `impl`：类型为 `QRhi::Implementation`。没有默认值，调用时必须提供。传入 `QRhi::Implementation` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `window`：类型为 `QWindow *`。没有默认值，调用时必须提供。传入 `QWindow *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[alias, since 6.7] QRhiShaderResourceBindingSet`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QRhi` 的 `Q、Rhi、Shader、Resource、Binding、设置` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.10) AdapterList`

**API 类别：** 公有类型

**中文解读：** 这是 `QRhi` 的 `Adapter、List` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum BeginFrameFlag { }`

**API 类别：** 公有类型

**中文解读：** 这是 `QRhi` 暴露的类型声明 `起始位置、Frame、Flag`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags BeginFrameFlags`

**API 类别：** 公有类型

**中文解读：** 这是 `QRhi` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum EndFrameFlag { SkipPresent }`

**API 类别：** 公有类型

**中文解读：** 这是 `QRhi` 暴露的类型声明 `结束、Frame、Flag`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags EndFrameFlags`

**API 类别：** 公有类型

**中文解读：** 这是 `QRhi` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum Flag { EnableDebugMarkers, EnableTimestamps, PreferSoftwareRenderer, EnablePipelineCacheDataSave, SuppressSmokeTestWarnings }`

**API 类别：** 公有类型

**中文解读：** 这是 `QRhi` 暴露的类型声明 `Flag`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags Flags`

**API 类别：** 公有类型

**中文解读：** 这是 `QRhi` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

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
