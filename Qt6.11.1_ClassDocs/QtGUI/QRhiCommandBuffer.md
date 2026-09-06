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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 33 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QRhiCommandBuffer::BeginPassFlagflags QRhiCommandBuffer::BeginPassFlags`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QRhiCommandBuffer` 暴露的类型声明 `起始位置、Pass、Flagflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:BeginPassFlagflags QRhiCommandBuffer::BeginPassFlags`。
- 属性名：`QRhiCommandBuffer`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[alias] QRhiCommandBuffer::DynamicOffset`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QRhiCommandBuffer` 的配置属性。初始化或状态切换时通过 `setDynamicOffset(...)` 设置，之后用 `DynamicOffset()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:DynamicOffset`。
- 属性名：`QRhiCommandBuffer`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QRhiCommandBuffer::IndexFormat`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QRhiCommandBuffer` 暴露的类型声明 `索引、格式化`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:IndexFormat`。
- 属性名：`QRhiCommandBuffer`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[alias] QRhiCommandBuffer::VertexInput`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QRhiCommandBuffer` 的配置属性。初始化或状态切换时通过 `setVertexInput(...)` 设置，之后用 `VertexInput()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:VertexInput`。
- 属性名：`QRhiCommandBuffer`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiCommandBuffer::beginComputePass(QRhiResourceUpdateBatch *resourceUpdates = nullptr, QRhiCommandBuffer::BeginPassFlags flags = {})`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `beginComputePass`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`void`。
- 参数 `resourceUpdates`：类型为 `QRhiResourceUpdateBatch *`。默认值为 `nullptr`。传入 `QRhiResourceUpdateBatch *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `flags`：类型为 `QRhiCommandBuffer::BeginPassFlags`。默认值为 `{}`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiCommandBuffer::beginExternal()`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `beginExternal`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiCommandBuffer::beginPass(QRhiRenderTarget *rt, const QColor &colorClearValue, const QRhiDepthStencilClearValue &depthStencilClearValue, QRhiResourceUpdateBatch *resourceUpdates = nullptr, QRhiCommandBuffer::BeginPassFlags flags = {})`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `beginPass`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`void`。
- 参数 `rt`：类型为 `QRhiRenderTarget *`。没有默认值，调用时必须提供。传入 `QRhiRenderTarget *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `colorClearValue`：类型为 `const QColor &`。没有默认值，调用时必须提供。传入 `const QColor &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `depthStencilClearValue`：类型为 `const QRhiDepthStencilClearValue &`。没有默认值，调用时必须提供。传入 `const QRhiDepthStencilClearValue &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `resourceUpdates`：类型为 `QRhiResourceUpdateBatch *`。默认值为 `nullptr`。传入 `QRhiResourceUpdateBatch *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `flags`：类型为 `QRhiCommandBuffer::BeginPassFlags`。默认值为 `{}`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiCommandBuffer::debugMarkBegin(const QByteArray &name)`

**API 类别：** 成员函数说明

**中文解读：** `QRhiCommandBuffer::debugMarkBegin` 用于执行与“调试输出、Mark、起始位置”相关的操作。调用时要先确认当前状态和 `name` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `name`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiCommandBuffer::debugMarkEnd()`

**API 类别：** 成员函数说明

**中文解读：** `QRhiCommandBuffer::debugMarkEnd` 用于执行与“调试输出、Mark、结束”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiCommandBuffer::debugMarkMsg(const QByteArray &msg)`

**API 类别：** 成员函数说明

**中文解读：** `QRhiCommandBuffer::debugMarkMsg` 用于执行与“调试输出、Mark、Msg”相关的操作。调用时要先确认当前状态和 `msg` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `msg`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiCommandBuffer::dispatch(int x, int y, int z)`

**API 类别：** 成员函数说明

**中文解读：** `QRhiCommandBuffer::dispatch` 用于执行与“dispatch”相关的操作。调用时要先确认当前状态和 `x`、`y`、`z` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `z`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiCommandBuffer::draw(quint32 vertexCount, quint32 instanceCount = 1, quint32 firstVertex = 0, quint32 firstInstance = 0)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QRhiCommandBuffer` 的核心操作 `draw`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `vertexCount`：类型为 `quint32`。没有默认值，调用时必须提供。传入 `quint32` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `instanceCount`：类型为 `quint32`。默认值为 `1`。传入 `quint32` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `firstVertex`：类型为 `quint32`。默认值为 `0`。传入 `quint32` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `firstInstance`：类型为 `quint32`。默认值为 `0`。传入 `quint32` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiCommandBuffer::drawIndexed(quint32 indexCount, quint32 instanceCount = 1, quint32 firstIndex = 0, qint32 vertexOffset = 0, quint32 firstInstance = 0)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QRhiCommandBuffer` 的核心操作 `drawIndexed`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `indexCount`：类型为 `quint32`。没有默认值，调用时必须提供。传入 `quint32` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `instanceCount`：类型为 `quint32`。默认值为 `1`。传入 `quint32` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `firstIndex`：类型为 `quint32`。默认值为 `0`。传入 `quint32` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `vertexOffset`：类型为 `qint32`。默认值为 `0`。传入 `qint32` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `firstInstance`：类型为 `quint32`。默认值为 `0`。传入 `quint32` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiCommandBuffer::endComputePass(QRhiResourceUpdateBatch *resourceUpdates = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `endComputePass`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数 `resourceUpdates`：类型为 `QRhiResourceUpdateBatch *`。默认值为 `nullptr`。传入 `QRhiResourceUpdateBatch *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiCommandBuffer::endExternal()`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `endExternal`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiCommandBuffer::endPass(QRhiResourceUpdateBatch *resourceUpdates = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `endPass`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数 `resourceUpdates`：类型为 `QRhiResourceUpdateBatch *`。默认值为 `nullptr`。传入 `QRhiResourceUpdateBatch *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `double QRhiCommandBuffer::lastCompletedGpuTime()`

**API 类别：** 成员函数说明

**中文解读：** `QRhiCommandBuffer::lastCompletedGpuTime` 用于计算、查询或取得与“末项、Completed、Gpu、时间”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `double`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`double`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QRhiNativeHandles *QRhiCommandBuffer::nativeHandles()`

**API 类别：** 成员函数说明

**中文解读：** `QRhiCommandBuffer::nativeHandles` 用于计算、查询或取得与“native、Handles”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QRhiNativeHandles *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QRhiNativeHandles *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QRhiResource::Type QRhiCommandBuffer::resourceType() const`

**API 类别：** 成员函数说明

**中文解读：** `QRhiCommandBuffer::resourceType` 用于计算、查询或取得与“resource、类型”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRhiResource::Type`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhiResource::Type`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiCommandBuffer::resourceUpdate(QRhiResourceUpdateBatch *resourceUpdates)`

**API 类别：** 成员函数说明

**中文解读：** `QRhiCommandBuffer::resourceUpdate` 用于执行与“resource、更新”相关的操作。调用时要先确认当前状态和 `resourceUpdates` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `resourceUpdates`：类型为 `QRhiResourceUpdateBatch *`。没有默认值，调用时必须提供。传入 `QRhiResourceUpdateBatch *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiCommandBuffer::setBlendConstants(const QColor &c)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setBlendConstants`。调用它会改变 `QRhiCommandBuffer` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `c`：类型为 `const QColor &`。没有默认值，调用时必须提供。传入 `const QColor &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiCommandBuffer::setComputePipeline(QRhiComputePipeline *ps)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setComputePipeline`。调用它会改变 `QRhiCommandBuffer` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `ps`：类型为 `QRhiComputePipeline *`。没有默认值，调用时必须提供。传入 `QRhiComputePipeline *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiCommandBuffer::setGraphicsPipeline(QRhiGraphicsPipeline *ps)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setGraphicsPipeline`。调用它会改变 `QRhiCommandBuffer` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `ps`：类型为 `QRhiGraphicsPipeline *`。没有默认值，调用时必须提供。传入 `QRhiGraphicsPipeline *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiCommandBuffer::setScissor(const QRhiScissor &scissor)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setScissor`。调用它会改变 `QRhiCommandBuffer` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `scissor`：类型为 `const QRhiScissor &`。没有默认值，调用时必须提供。传入 `const QRhiScissor &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiCommandBuffer::setShaderResources(QRhiShaderResourceBindings *srb = nullptr, int dynamicOffsetCount = 0, const QRhiCommandBuffer::DynamicOffset *dynamicOffsets = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setShaderResources`。调用它会改变 `QRhiCommandBuffer` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `srb`：类型为 `QRhiShaderResourceBindings *`。默认值为 `nullptr`。传入 `QRhiShaderResourceBindings *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `dynamicOffsetCount`：类型为 `int`。默认值为 `0`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `dynamicOffsets`：类型为 `const QRhiCommandBuffer::DynamicOffset *`。默认值为 `nullptr`。传入 `const QRhiCommandBuffer::DynamicOffset *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.9] void QRhiCommandBuffer::setShadingRate(const QSize &coarsePixelSize)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setShadingRate`。调用它会改变 `QRhiCommandBuffer` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `coarsePixelSize`：类型为 `const QSize &`。没有默认值，调用时必须提供。传入 `const QSize &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiCommandBuffer::setStencilRef(quint32 refValue)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setStencilRef`。调用它会改变 `QRhiCommandBuffer` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `refValue`：类型为 `quint32`。没有默认值，调用时必须提供。传入 `quint32` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiCommandBuffer::setVertexInput(int startBinding, int bindingCount, const QRhiCommandBuffer::VertexInput *bindings, QRhiBuffer *indexBuf = nullptr, quint32 indexOffset = 0, QRhiCommandBuffer::IndexFormat indexFormat = IndexUInt16)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setVertexInput`。调用它会改变 `QRhiCommandBuffer` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `startBinding`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `bindingCount`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `bindings`：类型为 `const QRhiCommandBuffer::VertexInput *`。没有默认值，调用时必须提供。传入 `const QRhiCommandBuffer::VertexInput *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `indexBuf`：类型为 `QRhiBuffer *`。默认值为 `nullptr`。传入 `QRhiBuffer *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `indexOffset`：类型为 `quint32`。默认值为 `0`。传入 `quint32` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `indexFormat`：类型为 `QRhiCommandBuffer::IndexFormat`。默认值为 `IndexUInt16`。传入 `QRhiCommandBuffer::IndexFormat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRhiCommandBuffer::setViewport(const QRhiViewport &viewport)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setViewport`。调用它会改变 `QRhiCommandBuffer` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `viewport`：类型为 `const QRhiViewport &`。没有默认值，调用时必须提供。传入 `const QRhiViewport &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum BeginPassFlag { ExternalContent, DoNotTrackResourcesForCompute }`

**API 类别：** 公有类型

**中文解读：** 这是 `QRhiCommandBuffer` 暴露的类型声明 `起始位置、Pass、Flag`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags BeginPassFlags`

**API 类别：** 公有类型

**中文解读：** 这是 `QRhiCommandBuffer` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `DynamicOffset`

**API 类别：** 公有类型

**中文解读：** 这是 `QRhiCommandBuffer` 的 `Dynamic、Offset` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `VertexInput`

**API 类别：** 公有类型

**中文解读：** 这是 `QRhiCommandBuffer` 的 `Vertex、Input` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

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

`QRhiCommandBuffer` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
