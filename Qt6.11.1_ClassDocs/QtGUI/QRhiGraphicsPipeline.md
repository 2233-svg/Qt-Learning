# QRhiGraphicsPipeline

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QRhiGraphicsPipeline` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

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

- `(since 6.6) struct StencilOpState`
- `(since 6.6) struct TargetBlend`
- `enum BlendFactor { Zero, One, SrcColor, OneMinusSrcColor, DstColor, …, OneMinusSrc1Alpha }`
- `enum BlendOp { Add, Subtract, ReverseSubtract, Min, Max }`
- `flags ColorMask`
- `enum ColorMaskComponent { R, G, B, A }`
- `enum CompareOp { Never, Less, Equal, LessOrEqual, Greater, …, Always }`
- `enum CullMode { None, Front, Back }`
- `enum Flag { UsesBlendConstants, UsesStencilRef, UsesScissor, CompileShadersWithDebugInfo, UsesShadingRate }`
- `flags Flags`
- `enum FrontFace { CCW, CW }`
- `enum PolygonMode { Fill, Line }`
- `enum StencilOp { StencilZero, Keep, Replace, IncrementAndClamp, DecrementAndClamp, …, DecrementAndWrap }`
- `enum Topology { Triangles, TriangleStrip, TriangleFan, Lines, LineStrip, …, Patches }`

### 公有函数

- `const QRhiShaderStage * cbeginShaderStages() const`
- `const QRhiGraphicsPipeline::TargetBlend * cbeginTargetBlends() const`
- `const QRhiShaderStage * cendShaderStages() const`
- `const QRhiGraphicsPipeline::TargetBlend * cendTargetBlends() const`
- `virtual bool create() = 0`
- `QRhiGraphicsPipeline::CullMode cullMode() const`
- `int depthBias() const`
- `QRhiGraphicsPipeline::CompareOp depthOp() const`
- `QRhiGraphicsPipeline::Flags flags() const`
- `QRhiGraphicsPipeline::FrontFace frontFace() const`
- `(since 6.11) bool hasDepthClamp() const`
- `bool hasDepthTest() const`
- `bool hasDepthWrite() const`
- `bool hasStencilTest() const`
- `float lineWidth() const`
- `(since 6.7) int multiViewCount() const`
- `int patchControlPointCount() const`
- `QRhiGraphicsPipeline::PolygonMode polygonMode() const`
- `QRhiRenderPassDescriptor * renderPassDescriptor() const`
- `int sampleCount() const`
- `void setCullMode(QRhiGraphicsPipeline::CullMode mode)`
- `void setDepthBias(int bias)`
- `(since 6.11) void setDepthClamp(bool enable)`
- `void setDepthOp(QRhiGraphicsPipeline::CompareOp op)`
- `void setDepthTest(bool enable)`
- `void setDepthWrite(bool enable)`
- `void setFlags(QRhiGraphicsPipeline::Flags f)`
- `void setFrontFace(QRhiGraphicsPipeline::FrontFace f)`
- `void setLineWidth(float width)`
- `(since 6.7) void setMultiViewCount(int count)`
- `void setPatchControlPointCount(int count)`
- `void setPolygonMode(QRhiGraphicsPipeline::PolygonMode mode)`
- `void setRenderPassDescriptor(QRhiRenderPassDescriptor *desc)`
- `void setSampleCount(int s)`
- `void setShaderResourceBindings(QRhiShaderResourceBindings *srb)`
- `void setShaderStages(std::initializer_list<QRhiShaderStage> list)`
- `void setShaderStages(InputIterator first, InputIterator last)`
- `void setSlopeScaledDepthBias(float bias)`
- `void setStencilBack(const QRhiGraphicsPipeline::StencilOpState &state)`
- `void setStencilFront(const QRhiGraphicsPipeline::StencilOpState &state)`
- `void setStencilReadMask(quint32 mask)`
- `void setStencilTest(bool enable)`
- `void setStencilWriteMask(quint32 mask)`
- `void setTargetBlends(std::initializer_list<QRhiGraphicsPipeline::TargetBlend> list)`
- `void setTargetBlends(InputIterator first, InputIterator last)`
- `void setTopology(QRhiGraphicsPipeline::Topology t)`
- `void setVertexInputLayout(const QRhiVertexInputLayout &layout)`
- `QRhiShaderResourceBindings * shaderResourceBindings() const`
- `const QRhiShaderStage * shaderStageAt(qsizetype index) const`
- `qsizetype shaderStageCount() const`
- `float slopeScaledDepthBias() const`
- `QRhiGraphicsPipeline::StencilOpState stencilBack() const`
- `QRhiGraphicsPipeline::StencilOpState stencilFront() const`
- `quint32 stencilReadMask() const`
- `quint32 stencilWriteMask() const`
- `const QRhiGraphicsPipeline::TargetBlend * targetBlendAt(qsizetype index) const`
- `qsizetype targetBlendCount() const`
- `QRhiGraphicsPipeline::Topology topology() const`
- `QRhiVertexInputLayout vertexInputLayout() const`

### 重实现的公有函数

- `virtual QRhiResource::Type resourceType() const override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QRhiGraphicsPipeline::BlendFactor`

**作用与语义：**

指定混合因子。
- `QRhiGraphicsPipeline::Zero`：`0`
- `QRhiGraphicsPipeline::One`：`1`
- `QRhiGraphicsPipeline::SrcColor`：`2`
- `QRhiGraphicsPipeline::OneMinusSrcColor`：`3`
- `QRhiGraphicsPipeline::DstColor`：`4`
- `QRhiGraphicsPipeline::OneMinusDstColor`：`5`
- `QRhiGraphicsPipeline::SrcAlpha`：`6`
- `QRhiGraphicsPipeline::OneMinusSrcAlpha`：`7`
- `QRhiGraphicsPipeline::DstAlpha`：`8`
- `QRhiGraphicsPipeline::OneMinusDstAlpha`：`9`
- `QRhiGraphicsPipeline::ConstantColor`：`10`
- `QRhiGraphicsPipeline::OneMinusConstantColor`：`11`
- `QRhiGraphicsPipeline::ConstantAlpha`：`12`
- `QRhiGraphicsPipeline::OneMinusConstantAlpha`：`13`
- `QRhiGraphicsPipeline::SrcAlphaSaturate`：`14`
- `QRhiGraphicsPipeline::Src1Color`：`15`
- `QRhiGraphicsPipeline::OneMinusSrc1Color`：`16`
- `QRhiGraphicsPipeline::Src1Alpha`：`17`
- `QRhiGraphicsPipeline::OneMinusSrc1Alpha`：`18`

### `enum QRhiGraphicsPipeline::BlendOp`

**作用与语义：**

指定混合操作。
- `QRhiGraphicsPipeline::Add`：`0`
- `QRhiGraphicsPipeline::Subtract`：`1`
- `QRhiGraphicsPipeline::ReverseSubtract`：`2`
- `QRhiGraphicsPipeline::Min`：`3`
- `QRhiGraphicsPipeline::Max`：`4`

### `enum QRhiGraphicsPipeline::ColorMaskComponentflags QRhiGraphicsPipeline::ColorMask`

**作用与语义：**

用于指定颜色写入遮罩的标志值。
- `QRhiGraphicsPipeline::R`：`1 << 0`
- `QRhiGraphicsPipeline::G`：`1 << 1`
- `QRhiGraphicsPipeline::B`：`1 << 2`
- `QRhiGraphicsPipeline::A`：`1 << 3`
ColorMask类型是QFlags的typedef<ColorMaskComponent>。它存储ColorMaskComponent值的或组合。

### `enum QRhiGraphicsPipeline::CompareOp`

**作用与语义：**

指定深度或模板比较函数。
- `QRhiGraphicsPipeline::Never`：`0`
- `QRhiGraphicsPipeline::Less`：`1`;（默认深度）
- `QRhiGraphicsPipeline::Equal`：`2`
- `QRhiGraphicsPipeline::LessOrEqual`：`3`
- `QRhiGraphicsPipeline::Greater`：`4`
- `QRhiGraphicsPipeline::NotEqual`：`5`
- `QRhiGraphicsPipeline::GreaterOrEqual`：`6`
- `QRhiGraphicsPipeline::Always`：`7`;（模板默认）

### `enum QRhiGraphicsPipeline::CullMode`

**作用与语义：**

指定剔除模式。
- 无`QRhiGraphicsPipeline::None`：`0`;无剔除（默认）
- `QRhiGraphicsPipeline::Front`：`1`;切割前面
- `QRhiGraphicsPipeline::Back`：`2`;剔除背面

### `enum QRhiGraphicsPipeline::Flagflags QRhiGraphicsPipeline::Flags`

**作用与语义：**

用于描述管道动态状态的标志值，以及其他选项。视口始终是动态的。
- `QRhiGraphicsPipeline::UsesBlendConstants`：`1 << 0`;表示通过`QRhiCommandBuffer::setBlendConstants()`设置混合颜色常数
- `QRhiGraphicsPipeline::UsesStencilRef`：`1 << 1`;表示模板参考值将通过`QRhiCommandBuffer::setStencilRef()`设置
- `QRhiGraphicsPipeline::UsesScissor`：`1 << 2`;表示通过`QRhiCommandBuffer::setScissor()`设置剪刀矩形
- `QRhiGraphicsPipeline::CompileShadersWithDebugInfo`：`1 << 3`;启用调试信息的着色器编译请求。这仅在涉及源代码的运行时着色器编译，且底层基础设施支持时才相关。具体例子中，这与Vulkan和SPIR-V无关，因为GLSL到SPIR-V的编译并非运行时完成。另一方面，考虑Direct3D和HLSL，这里有多种选项：当`QShader`包附带预编译字节码（`DXBC`）时，需通过生成`.qsb`文件的工具请求调试信息，类似于Vulkan和SPIR-V的情况。然而，当 HLSL 源代码存在于预或运行时生成的 `QShader` 包中时，编译的第一阶段（从 HLSL 源代码到中间格式）也会在运行时进行，并考虑该标志。调试信息尤其重要于像 RenderDoc 这样的工具，因为它允许在调查流水线和执行顶点或片段着色器调试时看到原始源代码。
- `QRhiGraphicsPipeline::UsesShadingRate`：`1 << 4`;表示每个绘制（每个流水线）着色率值将通过`QRhiCommandBuffer::setShadingRate()`设定。不指定该标志但仍然调用 setShadingRate() 可能会导致根据底层图形 API 的不同而出现不同且意想不到的结果。
Flags 类型是 QFlags 的 typedef<Flag>。它存储 Flag 值的 OR 组合。

### `enum QRhiGraphicsPipeline::FrontFace`

**作用与语义：**

规定前面绕制顺序。
- `QRhiGraphicsPipeline::CCW`：`0`;逆时针（默认）
- `QRhiGraphicsPipeline::CW`：`1`;顺时针

### `enum QRhiGraphicsPipeline::PolygonMode`

**作用与语义：**

指定多边形光栅化模式。
多边形模式（金属中的三角形填充模式，D3D中的填充模式）指定了光栅化多边形时所使用的填充模式。多边形可以绘制为实体（填充），也可以绘制为线状网格（线）。
非填充多边形模式的支持是可选的，`QRhi::NonFillPolygonMode`功能表示。在OpenGL ES和部分Vulkan实现中，该功能很可能会被报告为不支持，这意味着除了填充外，无法使用其他值。
- `QRhiGraphicsPipeline::Fill`：`0`;多边形内部填充（默认）
- `QRhiGraphicsPipeline::Line`：`1`;多边形的边界边以线段形式绘制。

### `enum QRhiGraphicsPipeline::StencilOp`

**作用与语义：**

指定模板操作。
- `QRhiGraphicsPipeline::StencilZero`: `0`
- `QRhiGraphicsPipeline::Keep`: `1`；（默认）
- `QRhiGraphicsPipeline::Replace`: `2`
- `QRhiGraphicsPipeline::IncrementAndClamp`: `3`
- `QRhiGraphicsPipeline::DecrementAndClamp`: `4`
- `QRhiGraphicsPipeline::Invert`: `5`
- `QRhiGraphicsPipeline::IncrementAndWrap`: `6`
- `QRhiGraphicsPipeline::DecrementAndWrap`: `7`

### `enum QRhiGraphicsPipeline::Topology`

**作用与语义：**

指定原始拓扑。
- `QRhiGraphicsPipeline::Triangles`：`0`;（默认）
- `QRhiGraphicsPipeline::TriangleStrip`：`1`
- `QRhiGraphicsPipeline::TriangleFan`：`2`;（仅在支持`QRhi::TriangleFanTopology`时使用）
- `QRhiGraphicsPipeline::Lines`：`3`
- `QRhiGraphicsPipeline::LineStrip`：`4`
- `QRhiGraphicsPipeline::Points`：`5`
- `QRhiGraphicsPipeline::Patches`：`6`;（仅在支持`QRhi::Tessellation`且需要流水线中存在镶嵌阶段时才可用）

### `const QRhiShaderStage *QRhiGraphicsPipeline::cbeginShaderStages() const`

**作用与语义：**

返回一个 cont 迭代器，指向着色器阶段列表中的第一个项目。

### `const QRhiGraphicsPipeline::TargetBlend *QRhiGraphicsPipeline::cbeginTargetBlends() const`

**作用与语义：**

返回一个const迭代器，指向渲染目标混合设置列表中的第一个项目。

### `const QRhiShaderStage *QRhiGraphicsPipeline::cendShaderStages() const`

**作用与语义：**

返回一个const迭代器，指向着色器阶段列表中最后一项之后。

### `const QRhiGraphicsPipeline::TargetBlend *QRhiGraphicsPipeline::cendTargetBlends() const`

**作用与语义：**

返回一个const迭代器，指向渲染目标混合设置列表中最后一个项目之后。

### `[pure virtual] bool QRhiGraphicsPipeline::create()`

**作用与语义：**

创建对应的本地图形资源。如果由于之前的 create() 已有资源存在且没有相应的 `destroy()`，那么 `destroy()` 会先隐式调用。
成功时返回`true`，`false`图形操作失败时返回。无论返回值如何，调用`destroy()`始终安全。
注意：这可能是一个昂贵的操作，具体取决于底层的图形API，尤其是在着色器从源码或中间字节码格式编译/优化到GPU自身指令集时。在适用的情况下，`QRhi`后端会自动设置相关的非持久化设施以加速此过程，例如Vulkan后端会自动创建`VkPipelineCache`以提升应用生命周期内的数据重用。
注意：驱动程序还可能采用各种持久（基于磁盘）的缓存策略来处理着色器和流水线数据，这些数据对 Qt 来说是隐藏的，也不在 Qt 控制范围内。在某些情况下，根据图形 API 和`QRhi`后端，`QRhi` 内部有手动管理此类缓存的功能，允许检索可序列化的 blob，并在应用的未来运行中重新加载，以确保更快的流水线创建速度。详情请参见`QRhi::pipelineCacheData()`和 `QRhi::setPipelineCacheData()`。还需要注意的是，当处理由更高级别Qt框架管理的`QRhi`实例时，例如`QQuickWindow`默认使用基于磁盘的流水线缓存（该缓存是除任何驱动程序缓存外的）。

### `QRhiGraphicsPipeline::CullMode QRhiGraphicsPipeline::cullMode() const`

**作用与语义：**

返回当前设置的面部剔除模式。

### `int QRhiGraphicsPipeline::depthBias() const`

**作用与语义：**

返回当前设置的深度偏差。

### `QRhiGraphicsPipeline::CompareOp QRhiGraphicsPipeline::depthOp() const`

**作用与语义：**

返回深度比较函数。

### `QRhiGraphicsPipeline::Flags QRhiGraphicsPipeline::flags() const`

**作用与语义：**

返回当前设置的标志。

### `QRhiGraphicsPipeline::FrontFace QRhiGraphicsPipeline::frontFace() const`

**作用与语义：**

返回当前设定的前脸模式。

### `[since 6.11] bool QRhiGraphicsPipeline::hasDepthClamp() const`

**作用与语义：**

如果启用深度钳，则返回true。

### `bool QRhiGraphicsPipeline::hasDepthTest() const`

**作用与语义：**

如果启用深度测试，则返回为真。

### `bool QRhiGraphicsPipeline::hasDepthWrite() const`

**作用与语义：**

如果启用深度写入，则返回真值。

### `bool QRhiGraphicsPipeline::hasStencilTest() const`

**作用与语义：**

如果启用模板测试，则返回为真。

### `float QRhiGraphicsPipeline::lineWidth() const`

**作用与语义：**

返回当前设置的线宽。默认值是1.0f。

### `[since 6.7] int QRhiGraphicsPipeline::multiViewCount() const`

**作用与语义：**

返回观看次数。默认值为0，表示没有多视图渲染。

### `int QRhiGraphicsPipeline::patchControlPointCount() const`

**作用与语义：**

返回当前设置的补丁控制点数。

### `QRhiGraphicsPipeline::PolygonMode QRhiGraphicsPipeline::polygonMode() const`

**作用与语义：**

返回多边形模式。

### `QRhiRenderPassDescriptor *QRhiGraphicsPipeline::renderPassDescriptor() const`

**作用与语义：**

返回当前设定的`QRhiRenderPassDescriptor`。

### `[override virtual] QRhiResource::Type QRhiGraphicsPipeline::resourceType() const`

**作用与语义：**

重装：`QRhiResource::resourceType()` const.
返回资源类型。
返回资源类型。

### `int QRhiGraphicsPipeline::sampleCount() const`

**作用与语义：**

返回当前设置的采样计数。1表示没有多重采样抗锯齿。

### `void QRhiGraphicsPipeline::setCullMode(QRhiGraphicsPipeline::CullMode mode)`

**作用与语义：**

设置指定的面剔除`mode`。

### `void QRhiGraphicsPipeline::setDepthBias(int bias)`

**作用与语义：**

设置深度`bias`。默认值为0。

### `[since 6.11] void QRhiGraphicsPipeline::setDepthClamp(bool enable)`

**作用与语义：**

当`enable`为真时启用深度截获。启用深度截获时，原本会被近距离或远剪裁平面裁剪的图元被光栅化，其深度值被钳为深度范围。禁用（默认情况下）时，这些图元会被裁剪。
注意：当`QRhi::DepthClamp`功能被报告为不支持时，该设置将被忽略。

### `void QRhiGraphicsPipeline::setDepthOp(QRhiGraphicsPipeline::CompareOp op)`

**作用与语义：**

设置深度比较函数`op`。

### `void QRhiGraphicsPipeline::setDepthTest(bool enable)`

**作用与语义：**

根据`enable`启用或禁用深度测试。深度测试和写出深度数据默认被禁用。

### `void QRhiGraphicsPipeline::setDepthWrite(bool enable)`

**作用与语义：**

根据`enable`控制深度数据写入深度缓冲区。默认情况下，该功能被禁用。深度写入通常与深度测试一起启用。
注意：未启用深度测试而启用深度写入可能无法达到预期结果，应避免。

### `void QRhiGraphicsPipeline::setFlags(QRhiGraphicsPipeline::Flags f)`

**作用与语义：**

这让标志变得很有点像`f`。

### `void QRhiGraphicsPipeline::setFrontFace(QRhiGraphicsPipeline::FrontFace f)`

**作用与语义：**

设置前脸模式`f`。

### `void QRhiGraphicsPipeline::setLineWidth(float width)`

**作用与语义：**

设置行 `width`。如果运行时`QRhi::WideLines`特性被报告为不支持，则忽略除 1.0f 以外的数值。

### `[since 6.7] void QRhiGraphicsPipeline::setMultiViewCount(int count)`

**作用与语义：**

设置视图`count`用于多视图渲染。默认值为0，表示没有多视图渲染。`count`必须达到2或以上才能触发多视图渲染。
多视图仅在多视图功能被报告为支持时才可用。渲染目标必须是二维纹理数组，渲染目标的颜色附件必须有相同的`count`设置。
关于多视角渲染的更多细节，请参见 `QRhiColorAttachment::setMultiViewCount()`。

### `void QRhiGraphicsPipeline::setPatchControlPointCount(int count)`

**作用与语义：**

将补丁控制点数设置为`count`。默认值为3。仅在拓扑设置为`Patches`时使用此值。

### `void QRhiGraphicsPipeline::setPolygonMode(QRhiGraphicsPipeline::PolygonMode mode)`

**作用与语义：**

设置多边形`mode`。默认是填充。

### `void QRhiGraphicsPipeline::setRenderPassDescriptor(QRhiRenderPassDescriptor *desc)`

**作用与语义：**

与指定的`QRhiRenderPassDescriptor` `desc`合作。

### `void QRhiGraphicsPipeline::setSampleCount(int s)`

**作用与语义：**

设置采样计数。`s`的典型值为1、4或8。流水线必须始终与渲染目标兼容，即采样计数必须匹配。

### `void QRhiGraphicsPipeline::setShaderResourceBindings(QRhiShaderResourceBindings *srb)`

**作用与语义：**

与`srb`关联描述资源绑定布局及资源本身（`QRhiBuffer`、`QRhiTexture`）。后者是可选的，因为在创建管道时只有布局重要。因此，这里传递的`srb`可以保持实际缓冲区或纹理对象未指定（`nullptr`），只要在记录绘制调用前有另一个`layout-compatible` `QRhiShaderResourceBindings`通过`setShaderResources()`绑定。

### `void QRhiGraphicsPipeline::setShaderStages(std::initializer_list<QRhiShaderStage> list)`

**作用与语义：**

设置着色器阶段的 `list`。

### `template <typename InputIterator> void QRhiGraphicsPipeline::setShaderStages(InputIterator first, InputIterator last)`

**作用与语义：**

从迭代器`first`和`last`中设置着色器阶段的列表。

### `void QRhiGraphicsPipeline::setSlopeScaledDepthBias(float bias)`

**作用与语义：**

设置斜率缩放深度`bias`。默认值为0。

### `void QRhiGraphicsPipeline::setStencilBack(const QRhiGraphicsPipeline::StencilOpState &state)`

**作用与语义：**

设置反面模板测试`state`。

### `void QRhiGraphicsPipeline::setStencilFront(const QRhiGraphicsPipeline::StencilOpState &state)`

**作用与语义：**

设置前脸的模板测试`state`。

### `void QRhiGraphicsPipeline::setStencilReadMask(quint32 mask)`

**作用与语义：**

设置模板读取`mask`。默认值为0xFF。

### `void QRhiGraphicsPipeline::setStencilTest(bool enable)`

**作用与语义：**

根据`enable`启用或禁用模板测试。默认情况下，该功能被禁用。

### `void QRhiGraphicsPipeline::setStencilWriteMask(quint32 mask)`

**作用与语义：**

设置模板写入`mask`。默认值为0xFF。

### `void QRhiGraphicsPipeline::setTargetBlends(std::initializer_list<QRhiGraphicsPipeline::TargetBlend> list)`

**作用与语义：**

设置渲染目标混合设置的 `list`。这是一个列表，因为当使用多个渲染目标（即一个`QRhiTextureRenderTarget`有多个`QRhiColorAttachment`时），每个渲染目标（颜色附件）都需要有`TargetBlend`结构。
默认情况下，有一个默认构造的 `TargetBlend`。

### `template <typename InputIterator> void QRhiGraphicsPipeline::setTargetBlends(InputIterator first, InputIterator last)`

**作用与语义：**

它会从迭代器`first`和`last`中设置渲染目标混合设置列表。

### `void QRhiGraphicsPipeline::setTopology(QRhiGraphicsPipeline::Topology t)`

**作用与语义：**

将原始拓扑设定为`t`。

### `void QRhiGraphicsPipeline::setVertexInputLayout(const QRhiVertexInputLayout &layout)`

**作用与语义：**

指定顶点输入 `layout`。

### `QRhiShaderResourceBindings *QRhiGraphicsPipeline::shaderResourceBindings() const`

**作用与语义：**

返回当前关联的`QRhiShaderResourceBindings`对象。

### `const QRhiShaderStage *QRhiGraphicsPipeline::shaderStageAt(qsizetype index) const`

**作用与语义：**

在指定 `index` 返回着色器阶段。

### `qsizetype QRhiGraphicsPipeline::shaderStageCount() const`

**作用与语义：**

返回该管线中的着色器阶段数量。

### `float QRhiGraphicsPipeline::slopeScaledDepthBias() const`

**作用与语义：**

返回当前设置的斜率缩放深度偏差。

### `QRhiGraphicsPipeline::StencilOpState QRhiGraphicsPipeline::stencilBack() const`

**作用与语义：**

返回当前模板测试状态的背面。

### `QRhiGraphicsPipeline::StencilOpState QRhiGraphicsPipeline::stencilFront() const`

**作用与语义：**

返回当前模板测试状态的正面。

### `quint32 QRhiGraphicsPipeline::stencilReadMask() const`

**作用与语义：**

返回当前模板读掩码。

### `quint32 QRhiGraphicsPipeline::stencilWriteMask() const`

**作用与语义：**

返回当前的模板写掩码。

### `const QRhiGraphicsPipeline::TargetBlend *QRhiGraphicsPipeline::targetBlendAt(qsizetype index) const`

**作用与语义：**

在指定`index`返回渲染目标混合设置。

### `qsizetype QRhiGraphicsPipeline::targetBlendCount() const`

**作用与语义：**

返回渲染目标混合设置的数量。

### `QRhiGraphicsPipeline::Topology QRhiGraphicsPipeline::topology() const`

**作用与语义：**

返回当前设定的原始拓扑。

### `QRhiVertexInputLayout QRhiGraphicsPipeline::vertexInputLayout() const`

**作用与语义：**

返回当前设置的顶点输入布局规范。

### `(since 6.6) struct StencilOpState`

**作用与语义：**

描述模板操作状态。
默认构造的模板操作状态包含以下集合：
- `failOp` - `Keep`
- `depthFailOp` - `Keep`
- `passOp` - `Keep`
- `compareOp` `Always`
注意：这是一个具有有限兼容性保证的RHI API，详情请参见 `QRhi`。

### `(since 6.6) struct TargetBlend`

**作用与语义：**

描述单色附件的混合状态。
默认设置为色彩写入，禁用混合。混合值默认设置为预乘 alpha（1、`OneMinusSrcAlpha`、1、`OneMinusSrcAlpha`）。这意味着要获得 Qt Quick 使用的 alpha 混合模式，只需将 `enable` 标志设置为 true，同时保持其他值为默认即可。
注意：这是一个具有有限兼容性保证的RHI API，详情请参见 `QRhi`。

### `flags ColorMask`

**作用与语义：**

用于指定颜色写入遮罩的标志值。
- `QRhiGraphicsPipeline::R`：`1 << 0`
- `QRhiGraphicsPipeline::G`：`1 << 1`
- `QRhiGraphicsPipeline::B`：`1 << 2`
- `QRhiGraphicsPipeline::A`：`1 << 3`
ColorMask类型是QFlags的typedef<ColorMaskComponent>。它存储ColorMaskComponent值的或组合。

### `enum ColorMaskComponent { R, G, B, A }`

**作用与语义：**

用于指定颜色写入遮罩的标志值。
- `QRhiGraphicsPipeline::R`：`1 << 0`
- `QRhiGraphicsPipeline::G`：`1 << 1`
- `QRhiGraphicsPipeline::B`：`1 << 2`
- `QRhiGraphicsPipeline::A`：`1 << 3`
ColorMask类型是QFlags的typedef<ColorMaskComponent>。它存储ColorMaskComponent值的或组合。

### `enum Flag { UsesBlendConstants, UsesStencilRef, UsesScissor, CompileShadersWithDebugInfo, UsesShadingRate }`

**作用与语义：**

用于描述管道动态状态的标志值，以及其他选项。视口始终是动态的。
- `QRhiGraphicsPipeline::UsesBlendConstants`：`1 << 0`;表示通过`QRhiCommandBuffer::setBlendConstants()`设置混合颜色常数
- `QRhiGraphicsPipeline::UsesStencilRef`：`1 << 1`;表示模板参考值将通过`QRhiCommandBuffer::setStencilRef()`设置
- `QRhiGraphicsPipeline::UsesScissor`：`1 << 2`;表示通过`QRhiCommandBuffer::setScissor()`设置剪刀矩形
- `QRhiGraphicsPipeline::CompileShadersWithDebugInfo`：`1 << 3`;启用调试信息的着色器编译请求。这仅在涉及源代码的运行时着色器编译，且底层基础设施支持时才相关。具体例子中，这与Vulkan和SPIR-V无关，因为GLSL到SPIR-V的编译并非运行时完成。另一方面，考虑Direct3D和HLSL，这里有多种选项：当`QShader`包附带预编译字节码（`DXBC`）时，需通过生成`.qsb`文件的工具请求调试信息，类似于Vulkan和SPIR-V的情况。然而，当 HLSL 源代码存在于预或运行时生成的 `QShader` 包中时，编译的第一阶段（从 HLSL 源代码到中间格式）也会在运行时进行，并考虑该标志。调试信息尤其重要于像 RenderDoc 这样的工具，因为它允许在调查流水线和执行顶点或片段着色器调试时看到原始源代码。
- `QRhiGraphicsPipeline::UsesShadingRate`：`1 << 4`;表示每个绘制（每个流水线）着色率值将通过`QRhiCommandBuffer::setShadingRate()`设定。不指定该标志但仍然调用 setShadingRate() 可能会导致根据底层图形 API 的不同而出现不同且意想不到的结果。
Flags 类型是 QFlags 的 typedef<Flag>。它存储 Flag 值的 OR 组合。

### `flags Flags`

**作用与语义：**

用于描述管道动态状态的标志值，以及其他选项。视口始终是动态的。
- `QRhiGraphicsPipeline::UsesBlendConstants`：`1 << 0`;表示通过`QRhiCommandBuffer::setBlendConstants()`设置混合颜色常数
- `QRhiGraphicsPipeline::UsesStencilRef`：`1 << 1`;表示模板参考值将通过`QRhiCommandBuffer::setStencilRef()`设置
- `QRhiGraphicsPipeline::UsesScissor`：`1 << 2`;表示通过`QRhiCommandBuffer::setScissor()`设置剪刀矩形
- `QRhiGraphicsPipeline::CompileShadersWithDebugInfo`：`1 << 3`;启用调试信息的着色器编译请求。这仅在涉及源代码的运行时着色器编译，且底层基础设施支持时才相关。具体例子中，这与Vulkan和SPIR-V无关，因为GLSL到SPIR-V的编译并非运行时完成。另一方面，考虑Direct3D和HLSL，这里有多种选项：当`QShader`包附带预编译字节码（`DXBC`）时，需通过生成`.qsb`文件的工具请求调试信息，类似于Vulkan和SPIR-V的情况。然而，当 HLSL 源代码存在于预或运行时生成的 `QShader` 包中时，编译的第一阶段（从 HLSL 源代码到中间格式）也会在运行时进行，并考虑该标志。调试信息尤其重要于像 RenderDoc 这样的工具，因为它允许在调查流水线和执行顶点或片段着色器调试时看到原始源代码。
- `QRhiGraphicsPipeline::UsesShadingRate`：`1 << 4`;表示每个绘制（每个流水线）着色率值将通过`QRhiCommandBuffer::setShadingRate()`设定。不指定该标志但仍然调用 setShadingRate() 可能会导致根据底层图形 API 的不同而出现不同且意想不到的结果。
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

`QRhiGraphicsPipeline` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
