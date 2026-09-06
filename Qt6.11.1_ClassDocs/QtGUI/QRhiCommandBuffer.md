# QRhiCommandBuffer

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QRhiCommandBuffer` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

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

- `enum BeginPassFlag { ExternalContent, DoNotTrackResourcesForCompute }`
- `flags BeginPassFlags`
- `DynamicOffset`
- `enum IndexFormat { IndexUInt16, IndexUInt32 }`
- `VertexInput`

### 公有函数

- `void beginComputePass(QRhiResourceUpdateBatch *resourceUpdates = nullptr, QRhiCommandBuffer::BeginPassFlags flags = {})`
- `void beginExternal()`
- `void beginPass(QRhiRenderTarget *rt, const QColor &colorClearValue, const QRhiDepthStencilClearValue &depthStencilClearValue, QRhiResourceUpdateBatch *resourceUpdates = nullptr, QRhiCommandBuffer::BeginPassFlags flags = {})`
- `void debugMarkBegin(const QByteArray &name)`
- `void debugMarkEnd()`
- `void debugMarkMsg(const QByteArray &msg)`
- `void dispatch(int x, int y, int z)`
- `void draw(quint32 vertexCount, quint32 instanceCount = 1, quint32 firstVertex = 0, quint32 firstInstance = 0)`
- `void drawIndexed(quint32 indexCount, quint32 instanceCount = 1, quint32 firstIndex = 0, qint32 vertexOffset = 0, quint32 firstInstance = 0)`
- `void endComputePass(QRhiResourceUpdateBatch *resourceUpdates = nullptr)`
- `void endExternal()`
- `void endPass(QRhiResourceUpdateBatch *resourceUpdates = nullptr)`
- `double lastCompletedGpuTime()`
- `const QRhiNativeHandles * nativeHandles()`
- `void resourceUpdate(QRhiResourceUpdateBatch *resourceUpdates)`
- `void setBlendConstants(const QColor &c)`
- `void setComputePipeline(QRhiComputePipeline *ps)`
- `void setGraphicsPipeline(QRhiGraphicsPipeline *ps)`
- `void setScissor(const QRhiScissor &scissor)`
- `void setShaderResources(QRhiShaderResourceBindings *srb = nullptr, int dynamicOffsetCount = 0, const QRhiCommandBuffer::DynamicOffset *dynamicOffsets = nullptr)`
- `(since 6.9) void setShadingRate(const QSize &coarsePixelSize)`
- `void setStencilRef(quint32 refValue)`
- `void setVertexInput(int startBinding, int bindingCount, const QRhiCommandBuffer::VertexInput *bindings, QRhiBuffer *indexBuf = nullptr, quint32 indexOffset = 0, QRhiCommandBuffer::IndexFormat indexFormat = IndexUInt16)`
- `void setViewport(const QRhiViewport &viewport)`

### 重实现的公有函数

- `virtual QRhiResource::Type resourceType() const override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QRhiCommandBuffer::BeginPassFlagflags QRhiCommandBuffer::BeginPassFlags`

**作用与语义：**

QRhi：：beginPass() 的标志值。
- `QRhiCommandBuffer::ExternalContent`：`0x01`;指定此过程将调用`QRhiCommandBuffer::beginExternal()`。某些后端，尤其是Vulkan，如果未设置该标志且`beginExternal()`仍被调用，将失败。
- `QRhiCommandBuffer::DoNotTrackResourcesForCompute`：`0x02`;规定如果跟踪的唯一目的是生成计算障碍，则无需追踪本次通道所用资源。意味着帧中没有计算通道。这是一个优化提示，某些后端，尤其是OpenGL，可能会考虑，允许它们跳过某些操作。当该标志被设置为帧中的渲染通道时，调用该帧中的`beginComputePass()`可能会导致意外行为，具体取决于渲染与计算通道之间的资源依赖关系。
BeginPassFlags 类型是 QFlags 的 typedef<BeginPassFlag>。它存储 BeginPassFlag 值的 OR 组合。

### `[alias] QRhiCommandBuffer::DynamicOffset`

**作用与语义：**

std：:p air<int， quint32> 的同义词。第一个条目是绑定，第二个是缓冲区中的偏移量。

### `enum QRhiCommandBuffer::IndexFormat`

**作用与语义：**

指定索引数据类型。
- `QRhiCommandBuffer::IndexUInt16`：`0`;无符号16位（quint16）
- `QRhiCommandBuffer::IndexUInt32`：`1`;无符号32位（quint32）

### `[alias] QRhiCommandBuffer::VertexInput`

**作用与语义：**

std：:p air<`QRhiBuffer` *， quint32> 的同义词。第二个条目是缓冲区中的偏移量，由第一个条目指定。

### `void QRhiCommandBuffer::beginComputePass(QRhiResourceUpdateBatch *resourceUpdates = nullptr, QRhiCommandBuffer::BeginPassFlags flags = {})`

**作用与语义：**

记录开始新的计算通道。
`resourceUpdates` 在非空时指定一个资源更新批处理，该批次将提交并释放。
注意：不要假设任何状态或资源绑定在每次传递之间依然存在。
注意：计算通行可以记录`setComputePipeline()`、`setShaderResources()`和`dispatch()`调用，而非图形调用。通用功能，如调试标记和 `beginExternal()`，渲染和计算通行均可使用。
注意：只有当`Compute`功能报告为支持时，计算才可用。
`flags`目前未被使用。

### `void QRhiCommandBuffer::beginExternal()`

**作用与语义：**

当前一个应用程序准备通过直接调用图形API函数将命令队列到当前传递的命令缓冲区时，被调用。
注意：只有在意图在`beginPass()`或`beginComputePass()`中提前声明时才可用。因此，只有在开始记录并指定`QRhiCommandBuffer::ExternalContent`时，才能调用此函数。
使用 Vulkan、Metal 或 Direct3D 12 时，可以通过 `nativeHandles()` 查询本地命令缓冲区或编码对象，并向它们排队命令。使用 OpenGL 或 Direct3D 11，可以从`QRhi::nativeHandles()`中获取（设备）上下文。但绝不能在不确保`QRhiCommandBuffer`状态保持最新的情况下进行。因此，必须将任何外部添加的命令记录封装在 beternal() 和 `endExternal()`之间。从概念上讲，这与 `QPainter` 的 `beginNativePainting()` 和 `endNativePainting()` 函数相同。
对于 OpenGL 来说，这个函数还有一个额外任务：确保上下文在当前线程上是最新的。
注意：一旦调用 berental()，在 `endExternal()` 之前，`QRhiCommandBuffer` 上不得调用其他特定的渲染传递函数（`set*` 或 `draw*`）。
警告：部分后端在 bestartExternal() - `endExternal()` 块内，可能会返回 `QRhiCommandBuffer::nativeHandles()` 的原生命令缓冲对象，该对象与主缓冲区不同。因此，在调用 bestartExternal() 后，重新查询本地命令缓冲区对象非常重要。实际上，例如在 Vulkan 中，外部记录的 Vulkan 命令会被放置在带有 VK_COMMAND_BUFFER_USAGE_RENDER_PASS_CONTINUE_BIT 的次级命令缓冲区上。`nativeHandles()` 在 begin/`endExternal` 之间调用时返回该次级命令缓冲区。

### `void QRhiCommandBuffer::beginPass(QRhiRenderTarget *rt, const QColor &colorClearValue, const QRhiDepthStencilClearValue &depthStencilClearValue, QRhiResourceUpdateBatch *resourceUpdates = nullptr, QRhiCommandBuffer::BeginPassFlags flags = {})`

**作用与语义：**

记录开始针对渲染目标的新渲染`rt`。
`resourceUpdates` 在非空时指定一个资源更新批处理，该批次将被提交并释放。
渲染目标的颜色和深度/模板缓冲区通常被清除。清除值在`colorClearValue`和`depthStencilClearValue`中指定。例外是渲染目标是用`QRhiTextureRenderTarget::PreserveColorContents`和/或`QRhiTextureRenderTarget::PreserveDepthStencilContents`创建的。此时清除值被忽略。
注意：启用保留的颜色或深度内容会根据底层硬件导致性能下降。采用平铺架构的移动显卡无需将之前的内容重新加载到切片缓冲区。同样，使用`QRhiTexture`作为深度缓冲区的`QRhiTextureRenderTarget`效率低于`QRhiRenderBuffer`，因为使用深度纹理时需要将数据写入其中，而渲染缓冲区则无需这样做（因为API不允许从渲染缓冲区读取采样）。
注意：不要假设任何状态或资源绑定在每次传递之间依然存在。
注意：`QRhiCommandBuffer`的`set`和`draw`函数只能在一次传递中调用。此外，除了`setGraphicsPipeline()`外，他们期望命令缓冲区中已经设置了流水线。根据后端不同，可能会出现未说明的问题。
如果`rt`是`QRhiTextureRenderTarget`，beginPass() 会检查从渲染目标引用的纹理和渲染缓冲对象是否是最新的。这类似于 `setShaderResources()` 对 `QRhiShaderResourceBindings` 的处理。如果任何附件自 `QRhiTextureRenderTarget::create()` 以来被重建，`rt` 会隐式调用 create()。因此，如果`rt`有`QRhiTexture`颜色附加 `texture`，且需要将纹理尺寸调整为不同，则以下方法是有效的：
`flags`允许控制某些高级功能。一个常用的标志是`ExternalContents`。每当该函数启动的通行中调用`beginExternal()`时，都应指定该标志。

**官方示例：**

```cpp
 QRhiTextureRenderTarget *rt = rhi->newTextureRenderTarget({ { texture } });
 rt->create();
 // ...
 texture->setPixelSize(new_size);
 texture->create();
 cb->beginPass(rt, colorClear, dsClear); // this is ok, no explicit rt->create() is required before
```

### `void QRhiCommandBuffer::debugMarkBegin(const QByteArray &name)`

**作用与语义：**

在命令缓冲区上记录一个命名的调试组，并带有指定的`name`。这在图形调试工具如RenderDoc和XCode中有所体现。分组结束时用`debugMarkEnd()`表示。
注意：当`QRhi::DebugMarkers`不被支持或`QRhi::EnableDebugMarkers`未设置时，将被忽略。
注意：可以被叫在比赛框架内的任何位置，无论是在传球内还是外。

### `void QRhiCommandBuffer::debugMarkEnd()`

**作用与语义：**

记录调试组的结束。
注意：当`QRhi::DebugMarkers`不被支持或`QRhi::EnableDebugMarkers`未设置时，将被忽略。
注意：可以被叫在比赛框架内的任何位置，无论是在传球内还是外。

### `void QRhiCommandBuffer::debugMarkMsg(const QByteArray &msg)`

**作用与语义：**

在命令流中插入调试消息`msg`。
注意：当`QRhi::DebugMarkers`不被支持或`QRhi::EnableDebugMarkers`未设置时，将被忽略。
注意：在某些后端，debugMarkMsg() 只支持在通行内，且在通行外调用时会被忽略。在其他后端，则会记录在帧内的任何位置。

### `void QRhiCommandBuffer::dispatch(int x, int y, int z)`

**作用与语义：**

用于调度计算工作项目的记录，`x`、`y`和`z`指定对应维度中的本地工作组数量。
注意：该函数只能在计算通关内调用，即在 `beginComputePass()` 和 `endComputePass()` 调用之间调用。
注意：`x`、`y` 和 `z` 必须符合运行时底层图形 API 实现的限制。最大值通常为 65535。
注意：也要注意局部工作组大小的可能限制。这在着色器中有明确规定，例如：`layout(local_size_x = 16, local_size_y = 16) in;`。例如，OpenGL中单个本地工作组调用次数的最小值（`local_size_x`、`local_size_y`和`local_size_z`的乘积）是1024，而OpenGL ES（3.1）中，值可能低至128。这意味着上述示例可能被某些OpenGL ES实现拒绝，因为调用次数为256。

### `void QRhiCommandBuffer::draw(quint32 vertexCount, quint32 instanceCount = 1, quint32 firstVertex = 0, quint32 firstInstance = 0)`

**作用与语义：**

记录了一场无索引的平局。
顶点数在`vertexCount`中指定。对于实例绘制，`instanceCount`设置为非1的值。`firstVertex`是第一个要绘制顶点的索引。绘制多个实例时，第一个实例ID由`firstInstance`指定。
注意：`firstInstance`可能不被支持，当`QRhi::BaseInstance`功能被报告为不支持时，会被忽略。在这种情况下，第一实例 ID 始终为 0。目前 OpenGL 从未支持`QRhi::BaseInstance`，主要由于 OpenGL ES 的限制，因此便携应用不应被设计成依赖这一论点。
注意：需要访问当前顶点或实例索引的着色器必须使用 `gl_VertexIndex` 和 `gl_InstanceIndex`，即兼容 Vulkan 的内置变量，而非 `gl_VertexID` 和 `gl_InstanceID`。
注意：当`firstInstance`非零时，`gl_InstanceIndex`不会将基值包含在某些底层3D API中。这由`QRhi::InstanceIndexIncludesBaseInstance`特性表示。如果无法避免依赖基实例值，建议应用程序根据该功能报告的内容，以统一条件传递该值，并在着色器中添加`gl_InstanceIndex`。
注意：该函数只能在渲染通道内调用，即在`beginPass()`和`endPass()`调用之间调用。

### `void QRhiCommandBuffer::drawIndexed(quint32 indexCount, quint32 instanceCount = 1, quint32 firstIndex = 0, qint32 vertexOffset = 0, quint32 firstInstance = 0)`

**作用与语义：**

记录了一场索引平局。
顶点数在`indexCount`中指定。`firstIndex` 是基础索引。索引缓冲区的有效偏移量为 `indexOffset + firstIndex * n`，其中 `n` 根据索引元素类型为 2 或 4。`indexOffset` 在 `setVertexInput()` 中指定。
注意：索引缓冲区中的有效偏移量必须与某些后端（例如Metal）保持一致4字节。对于这些后端，`NonFourAlignedEffectiveIndexBufferOffset`功能将被报告为不支持。
`vertexOffset`（也称为`base vertex`）是一个带符号的值，在索引到顶点缓冲区前添加到元素索引中。但对此的支持并非总是可行，当特征`QRhi::BaseVertex`报告为不支持时，该值会被忽略。
对于实例绘图，`instanceCount`设置为除1以外的值。绘制多个实例时，第一个实例ID由`firstInstance`指定。
注意：`firstInstance`可能不被支持，当`QRhi::BaseInstance`功能被报告为不支持时会被忽略。在这种情况下，第一实例 ID 始终为 0。目前 OpenGL 不支持`QRhi::BaseInstance`，主要由于 OpenGL ES 的限制，因此便携应用不应被设计成依赖这一论点。
注意：需要访问当前顶点或实例索引的着色器必须使用`gl_VertexIndex`和`gl_InstanceIndex`，即Vulkan兼容的内置变量，而非`gl_VertexID`和`gl_InstanceID`。
注意：当`firstInstance`非零时，`gl_InstanceIndex`不会包含部分底层3D API中的基值。这由`QRhi::InstanceIndexIncludesBaseInstance`特性所指示。如果无法避免依赖基实例值，建议应用程序根据该特性报告的内容，以统一条件传递该值，并将其添加到着色器中的`gl_InstanceIndex`中。
注意：该函数只能在渲染过程中调用，即在`beginPass()`和`endPass()`调用之间调用。

### `void QRhiCommandBuffer::endComputePass(QRhiResourceUpdateBatch *resourceUpdates = nullptr)`

**作用与语义：**

记录结束当前计算通道。
`resourceUpdates` 在非空时指定一个资源更新批处理，该批次将提交并释放。

### `void QRhiCommandBuffer::endExternal()`

**作用与语义：**

一旦外部添加的命令被记录到命令缓冲区或上下文中，才能调用。
注意：调用该函数后，所有`QRhiCommandBuffer`状态必须被假定为无效。如果在外部命令后记录了更多绘图调用，则必须重新设置流水线、顶点和索引缓冲区及其他状态。

### `void QRhiCommandBuffer::endPass(QRhiResourceUpdateBatch *resourceUpdates = nullptr)`

**作用与语义：**

记录结束当前渲染通道。
`resourceUpdates` 在非空时指定一个资源更新批处理，该批次将被提交并释放。

### `double QRhiCommandBuffer::lastCompletedGpuTime()`

**作用与语义：**

返回创建`QRhi`时启用`QRhi::EnableTimestamps`时的最后可用时间戳（秒数）。该值表示GPU在最后完成帧期间经过的时间。
注意：当`QRhi::Timestamps`功能未被报告为支持，或未传递`QRhi::EnableTimestamps`给`QRhi::create()`时，不要期望结果为0。有例外，因为某些图形API（Metal）可以在无需额外操作（时间戳查询）的情况下提供时序，但便携应用应在知道需要时有意识地选择响应时间戳收集，并相应调用该函数。
在解读该值时必须谨慎，因为其精度和粒度通常不受 Qt 控制，且取决于底层图形 API 及其实现。特别是不建议比较不同图形 API 和硬件之间的值，甚至可能毫无意义。
当帧被记录为`beginFrame()`和`endFrame()`，即交换链时，时间值很可能异步出现。因此返回的值可能是0（例如，前1-2帧）或最后已知值，指的是之前某个帧。值 my 在某些情况下也会再次变为 0，例如调整窗口大小时。可以预期在 beginFrame() 中检索到最新的可用值，并在 beginFrame() 返回后通过该函数查询。
注意：不要假设该值指的是前一帧（`currently_recorded - 1`帧）。它也可能指`currently_recorded - 2`或 `currently_recorded - 3`。具体行为可能取决于图形 API 及其实现。
另一方面，对于屏幕外帧，返回的值一旦返回`endOffscreenFrame()`就会保持最新，因为屏幕外帧减少了GPU流水线，并等待命令完成。
注意：这意味着与交换链帧不同，屏幕外帧的返回值必然指向刚刚提交并完成的帧。（假设该函数在 endOffScreenFrame() 之后、但下一个 bestartOffScreenFrame()之前被调用）。
注意GPU频率缩放和GPU时钟变化的影响，具体取决于平台。例如，在Windows上，使用现代显卡，即使提交的帧负载相似或相同，返回的时序也可能在很大范围内变化。一般来说，这超出了Qt的控制和解决范围。然而，当环境变量`QT_D3D_STABLE_POWER_STATE`设置为非零值时，D3D12后端会自动调用ID3D12Device：：SetStablePowerState()。这能大大稳定结果。这对通过`QElapsedTimer`测量的CPU端时序也有不小影响，尤其是在涉及屏幕外帧时。
注意：不要也绝不要将应用程序带入生产环境`QT_D3D_STABLE_POWER_STATE`。详情请参见Windows API文档。

### `const QRhiNativeHandles *QRhiCommandBuffer::nativeHandles()`

**作用与语义：**

返回指向后端特定`QRhiNativeHandles`子类的指针，如`QRhiVulkanCommandBufferNativeHandles`。当暴露底层原生资源不被后端支持或不适用于后端时，返回的值会被`nullptr`。

### `[override virtual] QRhiResource::Type QRhiCommandBuffer::resourceType() const`

**作用与语义：**

重装：`QRhiResource::resourceType()` const.
返回资源类型。
返回资源类型。

### `void QRhiCommandBuffer::resourceUpdate(QRhiResourceUpdateBatch *resourceUpdates)`

**作用与语义：**

有时提交资源更新是必要的，或者更方便，无需开始渲染处理。用 `resourceUpdates` 调用该函数是将 `resourceUpdates` 传递给 `beginPass()` 调用（或 `endPass()`，通常是读回调用时的选择）。
注意：不能在传球内叫。

### `void QRhiCommandBuffer::setBlendConstants(const QColor &c)`

**作用与语义：**

记录将主动混合常数设置为`c`。
只有当绑定的流水线已设置`QRhiGraphicsPipeline::UsesBlendConstants`时才能调用。
注意：该函数只能在渲染通道内调用，即在`beginPass()`和`endPass()`调用之间调用。

### `void QRhiCommandBuffer::setComputePipeline(QRhiComputePipeline *ps)`

**作用与语义：**

建立新计算流水线的记录`ps`。
注意：必须在记录命令缓冲区`setShaderResources()`或`dispatch()`命令前调用此功能。
注意：`QRhi`会在一次传递中优化不必要的调用，因此应用程序方面无需过度优化以避免调用该函数。
注意：该函数只能在计算过程中调用，即在 `beginComputePass()` 和 `endComputePass()` 调用之间调用。

### `void QRhiCommandBuffer::setGraphicsPipeline(QRhiGraphicsPipeline *ps)`

**作用与语义：**

记录建立了新的图形流水线`ps`。
注意：必须在记录命令缓冲区上的其他`set`或`draw`命令前调用该函数。
注意：`QRhi`会在一次传递中优化不必要的调用，因此应用程序方面无需过度优化以避免调用该函数。
注意：该函数只能在渲染过程中调用，即在`beginPass()`和`endPass()`调用之间调用。
注意：新的图形流水线`ps`必须是有效的指针。
设置没有`UsesScissor`标志的图形流水线，要么会禁用剪刀（在适用时使用）的图形API，要么将剪刀矩形设置为与上次设置的视口一致（在图形API中剪刀几乎始终处于激活状态），以确保后端间行为一致`QRhi`。

### `void QRhiCommandBuffer::setScissor(const QRhiScissor &scissor)`

**作用与语义：**

记录中设定了激活剪刀矩形的规则，具体由`scissor`。
只有当绑定的流水线`UsesScissor`设置时，才能调用该函数。当该标志被设置在活动流水线上时，必须调用该函数，因为剪刀测试将被启用，因此必须提供剪刀矩形。
注意：`QRhi`假设使用OpenGL风格的视口坐标，意味着x和y位于左下角。
注意：该函数只能在渲染过程中调用，即在`beginPass()`和`endPass()`调用之间调用。

### `void QRhiCommandBuffer::setShaderResources(QRhiShaderResourceBindings *srb = nullptr, int dynamicOffsetCount = 0, const QRhiCommandBuffer::DynamicOffset *dynamicOffsets = nullptr)`

**作用与语义：**

绑定一组着色器资源的记录，如统一缓冲区或纹理，这些资源对一个或多个着色器阶段可见。
`srb`可以为空，此时使用当前图形或计算流水线的关联`QRhiShaderResourceBindings`。当`srb`为非空时，必须是`layout-compatible`的，意味着布局（绑定数量、每个绑定的类型和绑定编号）必须完全匹配调用流水线create（时关联的流水线）`QRhiShaderResourceBindings`。
在某些情况下，看似不必要的 setShaderResources() 调用是强制性的：在重建从 `srb` 引用的资源时，例如更改 `QRhiBuffer` 的大小后接一个 `QRhiBuffer::create()`，这里是相关本地对象（如 Vulkan 中的描述符集）更新为当前支持`QRhiBuffer`、`QRhiTexture`、`QRhiSampler` `srb` 对象的本地资源的地方。在这种情况下，即使 setShaderResources() `srb`与上次调用相同，也必须调用。
当 `srb` 不是空时，create() 中构建的 `QRhiShaderResourceBindings` 对象保证不会以任何形式被访问。事实上，即使在此时也不需要有效：在 create() 后销毁流水线关联的 srb，并在每个 setShaderResources() 调用中明确指定另一个布局兼容的 srb 是有效的。
`dynamicOffsets`允许通过`QRhiShaderResourceBinding::uniformBufferWithDynamicOffset()`为与`srb`关联的统一缓冲区指定缓冲区偏移量。这与`srb`本身提供偏移不同：动态偏移不需要为每个不同偏移量构建新`QRhiShaderResourceBindings`，可以避免写入底层描述符（如适用时带后端），因此可能更高效。`dynamicOffsets`的每个元素都是`binding` - `offset`对。`dynamicOffsetCount` 指定了`dynamicOffsets`中的元素数量。
注意：`dynamicOffsets` 中的所有偏移量必须与 `QRhi::ubufAlignment()` 返回的值对齐字节。
注意：部分后端可能会限制支持的动态偏移量数量。避免使用大于8的`dynamicOffsetCount`。
注意：`QRhi`会在一次传递中优化不必要的调用（考虑上述条件），因此应用程序无需过度优化以避免调用该函数。
注意：该函数只能在渲染或计算通道内调用，即在`beginPass()`与`endPass()`或 `beginComputePass()` 与 `endComputePass()` 之间调用。

### `[since 6.9] void QRhiCommandBuffer::setShadingRate(const QSize &coarsePixelSize)`

**作用与语义：**

将以下拉图调用的着色率设置为`coarsePixelSize`。
默认是1x1。
只有当`QRhi::VariableRateShading`功能被报告为支持且命令缓冲区绑定的`QRhiGraphicsPipeline`在创建时宣告`QRhiGraphicsPipeline::UsesShadingRate`时才有功能。
打电话`QRhi::supportedShadingRates()`查询给定样本数量支持的着色率。
当`QRhiShadingRateMap`和该函数同时使用时，每个图块使用较高的着色率。目前对组合器行为没有任何控制。

### `void QRhiCommandBuffer::setStencilRef(quint32 refValue)`

**作用与语义：**

记录将主动模板参考值设置为`refValue`。
只有当绑定的流水线已`QRhiGraphicsPipeline::UsesStencilRef` 时才能调用。
注意：该函数只能在渲染通道内调用，即在`beginPass()`和`endPass()`调用之间调用。

### `void QRhiCommandBuffer::setVertexInput(int startBinding, int bindingCount, const QRhiCommandBuffer::VertexInput *bindings, QRhiBuffer *indexBuf = nullptr, quint32 indexOffset = 0, QRhiCommandBuffer::IndexFormat indexFormat = IndexUInt16)`

**作用与语义：**

记录顶点输入绑定。
后续`drawIndexed()`命令使用的索引缓冲区由`indexBuf`、`indexOffset`和`indexFormat`指定。当不需要索引绘图时，`indexBuf`可设置为空。
顶点缓冲区绑定会被批量处理。`startBinding` 指定第一个绑定编号。记录的命令随后将每个缓冲区从`bindings`绑定到绑定点 `startBinding + i`，其中 `i` 是 `bindings` 中的索引。`bindings` 中的每个元素指定一个`QRhiBuffer`和一个偏移量。
注意：部分后端可能会限制顶点缓冲区绑定的数量。避免使用大于8的`bindingCount`。
大多数后端会自动忽略同一遍中多余的顶点输入和索引变化，因此应用程序无需过度优化以避免调用该函数。
注意：该函数只能在渲染通道内调用，即在`beginPass()`和`endPass()`调用之间调用。
举个简单的例子，举一个顶点着色器，有两个输入：
假设数据以交错格式提供，位置只使用2个浮点点数（即每个顶点5个浮点：x、y、r、g、b）。然后可以使用输入布局创建该着色器的`QRhiGraphicsPipeline`：
这里有一个缓冲区绑定（绑定编号0），有两个输入引用它。在记录通行时，一旦流水线设置好，顶点绑定可以像以下方式简单地指定，假设vbuf是包含所有交错位置颜色数据的那个`QRhiBuffer`：

**官方示例：**

```cpp
 layout(location = 0) in vec4 position;
 layout(location = 1) in vec3 color;
```

### `void QRhiCommandBuffer::setViewport(const QRhiViewport &viewport)`

**作用与语义：**

`viewport`中指定的活动视口矩形记录。
在底层图形API始终启用剪刀的后端，这个函数还会在激活`QRhiGraphicsPipeline`未设置时将剪刀设置为与视口匹配，`UsesScissor`。
注意：`QRhi`假设采用OpenGL风格的视口坐标，即x和y位于左下角。
注意：该函数只能在渲染通道内调用，即在`beginPass()`和`endPass()`调用之间调用。

### `enum BeginPassFlag { ExternalContent, DoNotTrackResourcesForCompute }`

**作用与语义：**

QRhi：：beginPass() 的标志值。
- `QRhiCommandBuffer::ExternalContent`：`0x01`;指定此过程将调用`QRhiCommandBuffer::beginExternal()`。某些后端，尤其是Vulkan，如果未设置该标志且`beginExternal()`仍被调用，将失败。
- `QRhiCommandBuffer::DoNotTrackResourcesForCompute`：`0x02`;规定如果跟踪的唯一目的是生成计算障碍，则无需追踪本次通道所用资源。意味着帧中没有计算通道。这是一个优化提示，某些后端，尤其是OpenGL，可能会考虑，允许它们跳过某些操作。当该标志被设置为帧中的渲染通道时，调用该帧中的`beginComputePass()`可能会导致意外行为，具体取决于渲染与计算通道之间的资源依赖关系。
BeginPassFlags 类型是 QFlags 的 typedef<BeginPassFlag>。它存储 BeginPassFlag 值的 OR 组合。

### `flags BeginPassFlags`

**作用与语义：**

QRhi：：beginPass() 的标志值。
- `QRhiCommandBuffer::ExternalContent`：`0x01`;指定此过程将调用`QRhiCommandBuffer::beginExternal()`。某些后端，尤其是Vulkan，如果未设置该标志且`beginExternal()`仍被调用，将失败。
- `QRhiCommandBuffer::DoNotTrackResourcesForCompute`：`0x02`;规定如果跟踪的唯一目的是生成计算障碍，则无需追踪本次通道所用资源。意味着帧中没有计算通道。这是一个优化提示，某些后端，尤其是OpenGL，可能会考虑，允许它们跳过某些操作。当该标志被设置为帧中的渲染通道时，调用该帧中的`beginComputePass()`可能会导致意外行为，具体取决于渲染与计算通道之间的资源依赖关系。
BeginPassFlags 类型是 QFlags 的 typedef<BeginPassFlag>。它存储 BeginPassFlag 值的 OR 组合。

### `DynamicOffset`

**作用与语义：**

std：:p air<int， quint32> 的同义词。第一个条目是绑定，第二个是缓冲区中的偏移量。

### `VertexInput`

**作用与语义：**

std：:p air<`QRhiBuffer` *， quint32> 的同义词。第二个条目是缓冲区中的偏移量，由第一个条目指定。

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

`QRhiCommandBuffer` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
