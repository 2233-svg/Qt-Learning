# QRhiShaderResourceBinding

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QRhiShaderResourceBinding` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

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

- `enum StageFlag { VertexStage, TessellationControlStage, TessellationEvaluationStage, FragmentStage, ComputeStage, GeometryStage }`
- `flags StageFlags`
- `enum Type { UniformBuffer, SampledTexture, Texture, Sampler, ImageLoad, …, BufferLoadStore }`

### 公有函数

- `bool isLayoutCompatible(const QRhiShaderResourceBinding &other) const`

### 静态公有成员

- `QRhiShaderResourceBinding bufferLoad(int binding, QRhiShaderResourceBinding::StageFlags stage, QRhiBuffer *buf)`
- `QRhiShaderResourceBinding bufferLoad(int binding, QRhiShaderResourceBinding::StageFlags stage, QRhiBuffer *buf, quint32 offset, quint32 size)`
- `QRhiShaderResourceBinding bufferLoadStore(int binding, QRhiShaderResourceBinding::StageFlags stage, QRhiBuffer *buf)`
- `QRhiShaderResourceBinding bufferLoadStore(int binding, QRhiShaderResourceBinding::StageFlags stage, QRhiBuffer *buf, quint32 offset, quint32 size)`
- `QRhiShaderResourceBinding bufferStore(int binding, QRhiShaderResourceBinding::StageFlags stage, QRhiBuffer *buf)`
- `QRhiShaderResourceBinding bufferStore(int binding, QRhiShaderResourceBinding::StageFlags stage, QRhiBuffer *buf, quint32 offset, quint32 size)`
- `QRhiShaderResourceBinding imageLoad(int binding, QRhiShaderResourceBinding::StageFlags stage, QRhiTexture *tex, int level)`
- `QRhiShaderResourceBinding imageLoadStore(int binding, QRhiShaderResourceBinding::StageFlags stage, QRhiTexture *tex, int level)`
- `QRhiShaderResourceBinding imageStore(int binding, QRhiShaderResourceBinding::StageFlags stage, QRhiTexture *tex, int level)`
- `QRhiShaderResourceBinding sampledTexture(int binding, QRhiShaderResourceBinding::StageFlags stage, QRhiTexture *tex, QRhiSampler *sampler)`
- `QRhiShaderResourceBinding sampledTextures(int binding, QRhiShaderResourceBinding::StageFlags stage, int count, const QRhiShaderResourceBinding::TextureAndSampler *texSamplers)`
- `QRhiShaderResourceBinding sampler(int binding, QRhiShaderResourceBinding::StageFlags stage, QRhiSampler *sampler)`
- `QRhiShaderResourceBinding texture(int binding, QRhiShaderResourceBinding::StageFlags stage, QRhiTexture *tex)`
- `QRhiShaderResourceBinding textures(int binding, QRhiShaderResourceBinding::StageFlags stage, int count, QRhiTexture **tex)`
- `QRhiShaderResourceBinding uniformBuffer(int binding, QRhiShaderResourceBinding::StageFlags stage, QRhiBuffer *buf)`
- `QRhiShaderResourceBinding uniformBuffer(int binding, QRhiShaderResourceBinding::StageFlags stage, QRhiBuffer *buf, quint32 offset, quint32 size)`
- `QRhiShaderResourceBinding uniformBufferWithDynamicOffset(int binding, QRhiShaderResourceBinding::StageFlags stage, QRhiBuffer *buf, quint32 size)`

### 相关非成员函数

- `size_t qHash(const QRhiShaderResourceBinding &key, size_t seed = 0)`
- `bool operator!=(const QRhiShaderResourceBinding &a, const QRhiShaderResourceBinding &b)`
- `bool operator==(const QRhiShaderResourceBinding &a, const QRhiShaderResourceBinding &b)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 25 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QRhiShaderResourceBinding::StageFlagflags QRhiShaderResourceBinding::StageFlags`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QRhiShaderResourceBinding` 暴露的类型声明 `Stage、Flagflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:StageFlagflags QRhiShaderResourceBinding::StageFlags`。
- 属性名：`QRhiShaderResourceBinding`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QRhiShaderResourceBinding::Type`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QRhiShaderResourceBinding` 暴露的类型声明 `类型`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Type`。
- 属性名：`QRhiShaderResourceBinding`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QRhiShaderResourceBinding QRhiShaderResourceBinding::bufferLoad(int binding, QRhiShaderResourceBinding::StageFlags stage, QRhiBuffer *buf)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `bufferLoad`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QRhiShaderResourceBinding`。
- 参数 `binding`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `stage`：类型为 `QRhiShaderResourceBinding::StageFlags`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `buf`：类型为 `QRhiBuffer *`。没有默认值，调用时必须提供。传入 `QRhiBuffer *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QRhiShaderResourceBinding QRhiShaderResourceBinding::bufferLoad(int binding, QRhiShaderResourceBinding::StageFlags stage, QRhiBuffer *buf, quint32 offset, quint32 size)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `bufferLoad`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QRhiShaderResourceBinding`。
- 参数 `binding`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `stage`：类型为 `QRhiShaderResourceBinding::StageFlags`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `buf`：类型为 `QRhiBuffer *`。没有默认值，调用时必须提供。传入 `QRhiBuffer *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `offset`：类型为 `quint32`。没有默认值，调用时必须提供。传入 `quint32` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `size`：类型为 `quint32`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QRhiShaderResourceBinding QRhiShaderResourceBinding::bufferLoadStore(int binding, QRhiShaderResourceBinding::StageFlags stage, QRhiBuffer *buf)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `bufferLoadStore`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QRhiShaderResourceBinding`。
- 参数 `binding`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `stage`：类型为 `QRhiShaderResourceBinding::StageFlags`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `buf`：类型为 `QRhiBuffer *`。没有默认值，调用时必须提供。传入 `QRhiBuffer *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QRhiShaderResourceBinding QRhiShaderResourceBinding::bufferLoadStore(int binding, QRhiShaderResourceBinding::StageFlags stage, QRhiBuffer *buf, quint32 offset, quint32 size)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `bufferLoadStore`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QRhiShaderResourceBinding`。
- 参数 `binding`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `stage`：类型为 `QRhiShaderResourceBinding::StageFlags`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `buf`：类型为 `QRhiBuffer *`。没有默认值，调用时必须提供。传入 `QRhiBuffer *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `offset`：类型为 `quint32`。没有默认值，调用时必须提供。传入 `quint32` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `size`：类型为 `quint32`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QRhiShaderResourceBinding QRhiShaderResourceBinding::bufferStore(int binding, QRhiShaderResourceBinding::StageFlags stage, QRhiBuffer *buf)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `bufferStore`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QRhiShaderResourceBinding`。
- 参数 `binding`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `stage`：类型为 `QRhiShaderResourceBinding::StageFlags`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `buf`：类型为 `QRhiBuffer *`。没有默认值，调用时必须提供。传入 `QRhiBuffer *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QRhiShaderResourceBinding QRhiShaderResourceBinding::bufferStore(int binding, QRhiShaderResourceBinding::StageFlags stage, QRhiBuffer *buf, quint32 offset, quint32 size)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `bufferStore`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QRhiShaderResourceBinding`。
- 参数 `binding`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `stage`：类型为 `QRhiShaderResourceBinding::StageFlags`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `buf`：类型为 `QRhiBuffer *`。没有默认值，调用时必须提供。传入 `QRhiBuffer *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `offset`：类型为 `quint32`。没有默认值，调用时必须提供。传入 `quint32` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `size`：类型为 `quint32`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QRhiShaderResourceBinding QRhiShaderResourceBinding::imageLoad(int binding, QRhiShaderResourceBinding::StageFlags stage, QRhiTexture *tex, int level)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `imageLoad`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QRhiShaderResourceBinding`。
- 参数 `binding`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `stage`：类型为 `QRhiShaderResourceBinding::StageFlags`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `tex`：类型为 `QRhiTexture *`。没有默认值，调用时必须提供。传入 `QRhiTexture *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `level`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QRhiShaderResourceBinding QRhiShaderResourceBinding::imageLoadStore(int binding, QRhiShaderResourceBinding::StageFlags stage, QRhiTexture *tex, int level)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `imageLoadStore`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QRhiShaderResourceBinding`。
- 参数 `binding`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `stage`：类型为 `QRhiShaderResourceBinding::StageFlags`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `tex`：类型为 `QRhiTexture *`。没有默认值，调用时必须提供。传入 `QRhiTexture *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `level`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QRhiShaderResourceBinding QRhiShaderResourceBinding::imageStore(int binding, QRhiShaderResourceBinding::StageFlags stage, QRhiTexture *tex, int level)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `imageStore`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QRhiShaderResourceBinding`。
- 参数 `binding`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `stage`：类型为 `QRhiShaderResourceBinding::StageFlags`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `tex`：类型为 `QRhiTexture *`。没有默认值，调用时必须提供。传入 `QRhiTexture *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `level`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QRhiShaderResourceBinding::isLayoutCompatible(const QRhiShaderResourceBinding &other) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isLayoutCompatible`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `other`：类型为 `const QRhiShaderResourceBinding &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QRhiShaderResourceBinding QRhiShaderResourceBinding::sampledTexture(int binding, QRhiShaderResourceBinding::StageFlags stage, QRhiTexture *tex, QRhiSampler *sampler)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `sampledTexture`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QRhiShaderResourceBinding`。
- 参数 `binding`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `stage`：类型为 `QRhiShaderResourceBinding::StageFlags`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `tex`：类型为 `QRhiTexture *`。没有默认值，调用时必须提供。传入 `QRhiTexture *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sampler`：类型为 `QRhiSampler *`。没有默认值，调用时必须提供。传入 `QRhiSampler *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QRhiShaderResourceBinding QRhiShaderResourceBinding::sampledTextures(int binding, QRhiShaderResourceBinding::StageFlags stage, int count, const QRhiShaderResourceBinding::TextureAndSampler *texSamplers)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `sampledTextures`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QRhiShaderResourceBinding`。
- 参数 `binding`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `stage`：类型为 `QRhiShaderResourceBinding::StageFlags`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `count`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `texSamplers`：类型为 `const QRhiShaderResourceBinding::TextureAndSampler *`。没有默认值，调用时必须提供。传入 `const QRhiShaderResourceBinding::TextureAndSampler *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QRhiShaderResourceBinding QRhiShaderResourceBinding::sampler(int binding, QRhiShaderResourceBinding::StageFlags stage, QRhiSampler *sampler)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `sampler`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QRhiShaderResourceBinding`。
- 参数 `binding`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `stage`：类型为 `QRhiShaderResourceBinding::StageFlags`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `sampler`：类型为 `QRhiSampler *`。没有默认值，调用时必须提供。传入 `QRhiSampler *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QRhiShaderResourceBinding QRhiShaderResourceBinding::texture(int binding, QRhiShaderResourceBinding::StageFlags stage, QRhiTexture *tex)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `texture`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QRhiShaderResourceBinding`。
- 参数 `binding`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `stage`：类型为 `QRhiShaderResourceBinding::StageFlags`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `tex`：类型为 `QRhiTexture *`。没有默认值，调用时必须提供。传入 `QRhiTexture *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QRhiShaderResourceBinding QRhiShaderResourceBinding::textures(int binding, QRhiShaderResourceBinding::StageFlags stage, int count, QRhiTexture **tex)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `textures`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QRhiShaderResourceBinding`。
- 参数 `binding`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `stage`：类型为 `QRhiShaderResourceBinding::StageFlags`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `count`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `tex`：类型为 `QRhiTexture **`。没有默认值，调用时必须提供。传入 `QRhiTexture **` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QRhiShaderResourceBinding QRhiShaderResourceBinding::uniformBuffer(int binding, QRhiShaderResourceBinding::StageFlags stage, QRhiBuffer *buf)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `uniformBuffer`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QRhiShaderResourceBinding`。
- 参数 `binding`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `stage`：类型为 `QRhiShaderResourceBinding::StageFlags`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `buf`：类型为 `QRhiBuffer *`。没有默认值，调用时必须提供。传入 `QRhiBuffer *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QRhiShaderResourceBinding QRhiShaderResourceBinding::uniformBuffer(int binding, QRhiShaderResourceBinding::StageFlags stage, QRhiBuffer *buf, quint32 offset, quint32 size)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `uniformBuffer`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QRhiShaderResourceBinding`。
- 参数 `binding`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `stage`：类型为 `QRhiShaderResourceBinding::StageFlags`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `buf`：类型为 `QRhiBuffer *`。没有默认值，调用时必须提供。传入 `QRhiBuffer *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `offset`：类型为 `quint32`。没有默认值，调用时必须提供。传入 `quint32` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `size`：类型为 `quint32`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QRhiShaderResourceBinding QRhiShaderResourceBinding::uniformBufferWithDynamicOffset(int binding, QRhiShaderResourceBinding::StageFlags stage, QRhiBuffer *buf, quint32 size)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `uniformBufferWithDynamicOffset`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QRhiShaderResourceBinding`。
- 参数 `binding`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `stage`：类型为 `QRhiShaderResourceBinding::StageFlags`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `buf`：类型为 `QRhiBuffer *`。没有默认值，调用时必须提供。传入 `QRhiBuffer *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `size`：类型为 `quint32`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] size_t qHash(const QRhiShaderResourceBinding &key, size_t seed = 0)`

**API 类别：** 相关非成员函数

**中文解读：** `QRhiShaderResourceBinding::qHash` 用于计算、查询或取得与“q、Hash”相关的操作。调用时要先确认当前状态和 `key`、`seed` 的有效范围；返回类型是 `size_t`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`size_t`。
- 参数 `key`：类型为 `const QRhiShaderResourceBinding &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `seed`：类型为 `size_t`。默认值为 `0`。传入 `size_t` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator!=(const QRhiShaderResourceBinding &a, const QRhiShaderResourceBinding &b)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QRhiShaderResourceBinding` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `a`：类型为 `const QRhiShaderResourceBinding &`。没有默认值，调用时必须提供。传入 `const QRhiShaderResourceBinding &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `b`：类型为 `const QRhiShaderResourceBinding &`。没有默认值，调用时必须提供。传入 `const QRhiShaderResourceBinding &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator==(const QRhiShaderResourceBinding &a, const QRhiShaderResourceBinding &b)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QRhiShaderResourceBinding` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `a`：类型为 `const QRhiShaderResourceBinding &`。没有默认值，调用时必须提供。传入 `const QRhiShaderResourceBinding &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `b`：类型为 `const QRhiShaderResourceBinding &`。没有默认值，调用时必须提供。传入 `const QRhiShaderResourceBinding &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum StageFlag { VertexStage, TessellationControlStage, TessellationEvaluationStage, FragmentStage, ComputeStage, GeometryStage }`

**API 类别：** 公有类型

**中文解读：** 这是 `QRhiShaderResourceBinding` 暴露的类型声明 `Stage、Flag`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags StageFlags`

**API 类别：** 公有类型

**中文解读：** 这是 `QRhiShaderResourceBinding` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

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

`QRhiShaderResourceBinding` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
