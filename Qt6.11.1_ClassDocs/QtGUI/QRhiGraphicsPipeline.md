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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 76 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QRhiGraphicsPipeline::BlendFactor`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QRhiGraphicsPipeline` 暴露的类型声明 `Blend、Factor`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:BlendFactor`。
- 属性名：`QRhiGraphicsPipeline`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QRhiGraphicsPipeline::BlendOp`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QRhiGraphicsPipeline` 暴露的类型声明 `Blend、Op`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:BlendOp`。
- 属性名：`QRhiGraphicsPipeline`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QRhiGraphicsPipeline::ColorMaskComponentflags QRhiGraphicsPipeline::ColorMask`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QRhiGraphicsPipeline` 暴露的类型声明 `Color、Mask、Componentflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:ColorMaskComponentflags QRhiGraphicsPipeline::ColorMask`。
- 属性名：`QRhiGraphicsPipeline`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QRhiGraphicsPipeline::CompareOp`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QRhiGraphicsPipeline` 暴露的类型声明 `比较、Op`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:CompareOp`。
- 属性名：`QRhiGraphicsPipeline`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QRhiGraphicsPipeline::CullMode`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QRhiGraphicsPipeline` 暴露的类型声明 `Cull、模式`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:CullMode`。
- 属性名：`QRhiGraphicsPipeline`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QRhiGraphicsPipeline::Flagflags QRhiGraphicsPipeline::Flags`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QRhiGraphicsPipeline` 暴露的类型声明 `Flagflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Flagflags QRhiGraphicsPipeline::Flags`。
- 属性名：`QRhiGraphicsPipeline`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QRhiGraphicsPipeline::FrontFace`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QRhiGraphicsPipeline` 暴露的类型声明 `开头、Face`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:FrontFace`。
- 属性名：`QRhiGraphicsPipeline`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QRhiGraphicsPipeline::PolygonMode`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QRhiGraphicsPipeline` 暴露的类型声明 `Polygon、模式`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:PolygonMode`。
- 属性名：`QRhiGraphicsPipeline`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QRhiGraphicsPipeline::StencilOp`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QRhiGraphicsPipeline` 暴露的类型声明 `Stencil、Op`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:StencilOp`。
- 属性名：`QRhiGraphicsPipeline`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QRhiGraphicsPipeline::Topology`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QRhiGraphicsPipeline` 暴露的类型声明 `Topology`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Topology`。
- 属性名：`QRhiGraphicsPipeline`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QRhiShaderStage *QRhiGraphicsPipeline::cbeginShaderStages() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhiGraphicsPipeline::cbeginShaderStages` 用于计算、查询或取得与“cbegin、Shader、Stages”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QRhiShaderStage *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QRhiShaderStage *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QRhiGraphicsPipeline::TargetBlend *QRhiGraphicsPipeline::cbeginTargetBlends() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhiGraphicsPipeline::cbeginTargetBlends` 用于计算、查询或取得与“cbegin、目标、Blends”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QRhiGraphicsPipeline::TargetBlend *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QRhiGraphicsPipeline::TargetBlend *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QRhiShaderStage *QRhiGraphicsPipeline::cendShaderStages() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhiGraphicsPipeline::cendShaderStages` 用于计算、查询或取得与“cend、Shader、Stages”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QRhiShaderStage *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QRhiShaderStage *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QRhiGraphicsPipeline::TargetBlend *QRhiGraphicsPipeline::cendTargetBlends() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhiGraphicsPipeline::cendTargetBlends` 用于计算、查询或取得与“cend、目标、Blends”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QRhiGraphicsPipeline::TargetBlend *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QRhiGraphicsPipeline::TargetBlend *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] bool QRhiGraphicsPipeline::create()`

**API 类别：** 成员函数说明

**中文解读：** `QRhiGraphicsPipeline::create` 用于计算、查询或取得与“创建”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhiGraphicsPipeline::CullMode QRhiGraphicsPipeline::cullMode() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhiGraphicsPipeline::cullMode` 用于计算、查询或取得与“cull、模式”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRhiGraphicsPipeline::CullMode`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhiGraphicsPipeline::CullMode`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QRhiGraphicsPipeline::depthBias() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhiGraphicsPipeline::depthBias` 用于计算、查询或取得与“depth、Bias”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhiGraphicsPipeline::CompareOp QRhiGraphicsPipeline::depthOp() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhiGraphicsPipeline::depthOp` 用于计算、查询或取得与“depth、Op”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRhiGraphicsPipeline::CompareOp`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhiGraphicsPipeline::CompareOp`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhiGraphicsPipeline::Flags QRhiGraphicsPipeline::flags() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhiGraphicsPipeline::flags` 用于计算、查询或取得与“标志”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRhiGraphicsPipeline::Flags`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhiGraphicsPipeline::Flags`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhiGraphicsPipeline::FrontFace QRhiGraphicsPipeline::frontFace() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhiGraphicsPipeline::frontFace` 用于计算、查询或取得与“开头、Face”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRhiGraphicsPipeline::FrontFace`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhiGraphicsPipeline::FrontFace`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.11] bool QRhiGraphicsPipeline::hasDepthClamp() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `hasDepthClamp`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QRhiGraphicsPipeline::hasDepthTest() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `hasDepthTest`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QRhiGraphicsPipeline::hasDepthWrite() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `hasDepthWrite`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QRhiGraphicsPipeline::hasStencilTest() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `hasStencilTest`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `float QRhiGraphicsPipeline::lineWidth() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhiGraphicsPipeline::lineWidth` 用于计算、查询或取得与“行、宽度”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `float`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`float`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.7] int QRhiGraphicsPipeline::multiViewCount() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhiGraphicsPipeline::multiViewCount` 用于计算、查询或取得与“multi、View、数量统计”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QRhiGraphicsPipeline::patchControlPointCount() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhiGraphicsPipeline::patchControlPointCount` 用于计算、查询或取得与“patch、Control、Point、数量统计”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhiGraphicsPipeline::PolygonMode QRhiGraphicsPipeline::polygonMode() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhiGraphicsPipeline::polygonMode` 用于计算、查询或取得与“polygon、模式”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRhiGraphicsPipeline::PolygonMode`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhiGraphicsPipeline::PolygonMode`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhiRenderPassDescriptor *QRhiGraphicsPipeline::renderPassDescriptor() const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QRhiGraphicsPipeline` 的核心操作 `renderPassDescriptor`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`QRhiRenderPassDescriptor *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QRhiResource::Type QRhiGraphicsPipeline::resourceType() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhiGraphicsPipeline::resourceType` 用于计算、查询或取得与“resource、类型”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRhiResource::Type`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhiResource::Type`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QRhiGraphicsPipeline::sampleCount() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhiGraphicsPipeline::sampleCount` 用于计算、查询或取得与“sample、数量统计”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiGraphicsPipeline::setCullMode(QRhiGraphicsPipeline::CullMode mode)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setCullMode`。调用它会改变 `QRhiGraphicsPipeline` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `mode`：类型为 `QRhiGraphicsPipeline::CullMode`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiGraphicsPipeline::setDepthBias(int bias)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setDepthBias`。调用它会改变 `QRhiGraphicsPipeline` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `bias`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.11] void QRhiGraphicsPipeline::setDepthClamp(bool enable)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setDepthClamp`。调用它会改变 `QRhiGraphicsPipeline` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enable`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiGraphicsPipeline::setDepthOp(QRhiGraphicsPipeline::CompareOp op)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setDepthOp`。调用它会改变 `QRhiGraphicsPipeline` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `op`：类型为 `QRhiGraphicsPipeline::CompareOp`。没有默认值，调用时必须提供。传入 `QRhiGraphicsPipeline::CompareOp` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiGraphicsPipeline::setDepthTest(bool enable)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setDepthTest`。调用它会改变 `QRhiGraphicsPipeline` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enable`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiGraphicsPipeline::setDepthWrite(bool enable)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setDepthWrite`。调用它会改变 `QRhiGraphicsPipeline` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enable`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiGraphicsPipeline::setFlags(QRhiGraphicsPipeline::Flags f)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFlags`。调用它会改变 `QRhiGraphicsPipeline` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `f`：类型为 `QRhiGraphicsPipeline::Flags`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiGraphicsPipeline::setFrontFace(QRhiGraphicsPipeline::FrontFace f)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFrontFace`。调用它会改变 `QRhiGraphicsPipeline` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `f`：类型为 `QRhiGraphicsPipeline::FrontFace`。没有默认值，调用时必须提供。传入 `QRhiGraphicsPipeline::FrontFace` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiGraphicsPipeline::setLineWidth(float width)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setLineWidth`。调用它会改变 `QRhiGraphicsPipeline` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `width`：类型为 `float`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.7] void QRhiGraphicsPipeline::setMultiViewCount(int count)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setMultiViewCount`。调用它会改变 `QRhiGraphicsPipeline` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `count`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiGraphicsPipeline::setPatchControlPointCount(int count)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPatchControlPointCount`。调用它会改变 `QRhiGraphicsPipeline` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `count`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiGraphicsPipeline::setPolygonMode(QRhiGraphicsPipeline::PolygonMode mode)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPolygonMode`。调用它会改变 `QRhiGraphicsPipeline` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `mode`：类型为 `QRhiGraphicsPipeline::PolygonMode`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiGraphicsPipeline::setRenderPassDescriptor(QRhiRenderPassDescriptor *desc)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setRenderPassDescriptor`。调用它会改变 `QRhiGraphicsPipeline` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `desc`：类型为 `QRhiRenderPassDescriptor *`。没有默认值，调用时必须提供。传入 `QRhiRenderPassDescriptor *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiGraphicsPipeline::setSampleCount(int s)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSampleCount`。调用它会改变 `QRhiGraphicsPipeline` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `s`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiGraphicsPipeline::setShaderResourceBindings(QRhiShaderResourceBindings *srb)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setShaderResourceBindings`。调用它会改变 `QRhiGraphicsPipeline` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `srb`：类型为 `QRhiShaderResourceBindings *`。没有默认值，调用时必须提供。传入 `QRhiShaderResourceBindings *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiGraphicsPipeline::setShaderStages(std::initializer_list<QRhiShaderStage> list)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setShaderStages`。调用它会改变 `QRhiGraphicsPipeline` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `list`：类型为 `std::initializer_list<QRhiShaderStage>`。没有默认值，调用时必须提供。传入 `std::initializer_list<QRhiShaderStage>` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename InputIterator> void QRhiGraphicsPipeline::setShaderStages(InputIterator first, InputIterator last)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setShaderStages`。调用它会改变 `QRhiGraphicsPipeline` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`template <typename InputIterator> void`。
- 参数 `first`：类型为 `InputIterator`。没有默认值，调用时必须提供。传入 `InputIterator` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `last`：类型为 `InputIterator`。没有默认值，调用时必须提供。传入 `InputIterator` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiGraphicsPipeline::setSlopeScaledDepthBias(float bias)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSlopeScaledDepthBias`。调用它会改变 `QRhiGraphicsPipeline` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `bias`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiGraphicsPipeline::setStencilBack(const QRhiGraphicsPipeline::StencilOpState &state)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setStencilBack`。调用它会改变 `QRhiGraphicsPipeline` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `state`：类型为 `const QRhiGraphicsPipeline::StencilOpState &`。没有默认值，调用时必须提供。状态值或状态对象；它描述调用时的阶段，不能把某个状态下有效的 API 用到其他阶段。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiGraphicsPipeline::setStencilFront(const QRhiGraphicsPipeline::StencilOpState &state)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setStencilFront`。调用它会改变 `QRhiGraphicsPipeline` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `state`：类型为 `const QRhiGraphicsPipeline::StencilOpState &`。没有默认值，调用时必须提供。状态值或状态对象；它描述调用时的阶段，不能把某个状态下有效的 API 用到其他阶段。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiGraphicsPipeline::setStencilReadMask(quint32 mask)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setStencilReadMask`。调用它会改变 `QRhiGraphicsPipeline` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `mask`：类型为 `quint32`。没有默认值，调用时必须提供。传入 `quint32` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiGraphicsPipeline::setStencilTest(bool enable)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setStencilTest`。调用它会改变 `QRhiGraphicsPipeline` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enable`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiGraphicsPipeline::setStencilWriteMask(quint32 mask)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setStencilWriteMask`。调用它会改变 `QRhiGraphicsPipeline` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `mask`：类型为 `quint32`。没有默认值，调用时必须提供。传入 `quint32` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiGraphicsPipeline::setTargetBlends(std::initializer_list<QRhiGraphicsPipeline::TargetBlend> list)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setTargetBlends`。调用它会改变 `QRhiGraphicsPipeline` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `list`：类型为 `std::initializer_list<QRhiGraphicsPipeline::TargetBlend>`。没有默认值，调用时必须提供。传入 `std::initializer_list<QRhiGraphicsPipeline::TargetBlend>` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename InputIterator> void QRhiGraphicsPipeline::setTargetBlends(InputIterator first, InputIterator last)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setTargetBlends`。调用它会改变 `QRhiGraphicsPipeline` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`template <typename InputIterator> void`。
- 参数 `first`：类型为 `InputIterator`。没有默认值，调用时必须提供。传入 `InputIterator` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `last`：类型为 `InputIterator`。没有默认值，调用时必须提供。传入 `InputIterator` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiGraphicsPipeline::setTopology(QRhiGraphicsPipeline::Topology t)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setTopology`。调用它会改变 `QRhiGraphicsPipeline` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `t`：类型为 `QRhiGraphicsPipeline::Topology`。没有默认值，调用时必须提供。传入 `QRhiGraphicsPipeline::Topology` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiGraphicsPipeline::setVertexInputLayout(const QRhiVertexInputLayout &layout)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setVertexInputLayout`。调用它会改变 `QRhiGraphicsPipeline` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `layout`：类型为 `const QRhiVertexInputLayout &`。没有默认值，调用时必须提供。参与操作的布局对象。通常表示整个子布局的几何区域和所有权，不等于子布局里的某一个控件。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhiShaderResourceBindings *QRhiGraphicsPipeline::shaderResourceBindings() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhiGraphicsPipeline::shaderResourceBindings` 用于计算、查询或取得与“shader、Resource、Bindings”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRhiShaderResourceBindings *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhiShaderResourceBindings *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QRhiShaderStage *QRhiGraphicsPipeline::shaderStageAt(qsizetype index) const`

**API 类别：** 成员函数说明

**中文解读：** `QRhiGraphicsPipeline::shaderStageAt` 用于计算、查询或取得与“shader、Stage、按位置访问”相关的操作。调用时要先确认当前状态和 `index` 的有效范围；返回类型是 `const QRhiShaderStage *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QRhiShaderStage *`。
- 参数 `index`：类型为 `qsizetype`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qsizetype QRhiGraphicsPipeline::shaderStageCount() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhiGraphicsPipeline::shaderStageCount` 用于计算、查询或取得与“shader、Stage、数量统计”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `float QRhiGraphicsPipeline::slopeScaledDepthBias() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhiGraphicsPipeline::slopeScaledDepthBias` 用于计算、查询或取得与“slope、Scaled、Depth、Bias”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `float`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`float`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhiGraphicsPipeline::StencilOpState QRhiGraphicsPipeline::stencilBack() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhiGraphicsPipeline::stencilBack` 用于计算、查询或取得与“stencil、末尾”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRhiGraphicsPipeline::StencilOpState`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhiGraphicsPipeline::StencilOpState`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhiGraphicsPipeline::StencilOpState QRhiGraphicsPipeline::stencilFront() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhiGraphicsPipeline::stencilFront` 用于计算、查询或取得与“stencil、开头”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRhiGraphicsPipeline::StencilOpState`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhiGraphicsPipeline::StencilOpState`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `quint32 QRhiGraphicsPipeline::stencilReadMask() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhiGraphicsPipeline::stencilReadMask` 用于计算、查询或取得与“stencil、读取、Mask”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `quint32`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`quint32`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `quint32 QRhiGraphicsPipeline::stencilWriteMask() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhiGraphicsPipeline::stencilWriteMask` 用于计算、查询或取得与“stencil、写入、Mask”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `quint32`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`quint32`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QRhiGraphicsPipeline::TargetBlend *QRhiGraphicsPipeline::targetBlendAt(qsizetype index) const`

**API 类别：** 成员函数说明

**中文解读：** `QRhiGraphicsPipeline::targetBlendAt` 用于计算、查询或取得与“目标、Blend、按位置访问”相关的操作。调用时要先确认当前状态和 `index` 的有效范围；返回类型是 `const QRhiGraphicsPipeline::TargetBlend *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QRhiGraphicsPipeline::TargetBlend *`。
- 参数 `index`：类型为 `qsizetype`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qsizetype QRhiGraphicsPipeline::targetBlendCount() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhiGraphicsPipeline::targetBlendCount` 用于计算、查询或取得与“目标、Blend、数量统计”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhiGraphicsPipeline::Topology QRhiGraphicsPipeline::topology() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `topology`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QRhiGraphicsPipeline::Topology`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhiVertexInputLayout QRhiGraphicsPipeline::vertexInputLayout() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhiGraphicsPipeline::vertexInputLayout` 用于计算、查询或取得与“vertex、Input、Layout”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRhiVertexInputLayout`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhiVertexInputLayout`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.6) struct StencilOpState`

**API 类别：** 公有类型

**中文解读：** 这是 `QRhiGraphicsPipeline` 的 `Stencil、Op、State` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.6) struct TargetBlend`

**API 类别：** 公有类型

**中文解读：** 这是 `QRhiGraphicsPipeline` 的 `目标、Blend` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags ColorMask`

**API 类别：** 公有类型

**中文解读：** 这是 `QRhiGraphicsPipeline` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum ColorMaskComponent { R, G, B, A }`

**API 类别：** 公有类型

**中文解读：** 这是 `QRhiGraphicsPipeline` 暴露的类型声明 `Color、Mask、Component`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum Flag { UsesBlendConstants, UsesStencilRef, UsesScissor, CompileShadersWithDebugInfo, UsesShadingRate }`

**API 类别：** 公有类型

**中文解读：** 这是 `QRhiGraphicsPipeline` 暴露的类型声明 `Flag`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags Flags`

**API 类别：** 公有类型

**中文解读：** 这是 `QRhiGraphicsPipeline` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

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

`QRhiGraphicsPipeline` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
