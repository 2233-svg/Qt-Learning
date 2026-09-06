# QShader

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QShader` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QShader>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
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

- `struct NativeShaderInfo`
- `struct SeparateToCombinedImageSamplerMapping`
- `NativeResourceBindingMap`
- `SeparateToCombinedImageSamplerMappingList`
- `enum class SerializedFormatVersion { Latest, Qt_6_5, Qt_6_4 }`
- `enum Source { SpirvShader, GlslShader, HlslShader, DxbcShader, MslShader, …, WgslShader }`
- `enum Stage { VertexStage, TessellationControlStage, TessellationEvaluationStage, GeometryStage, FragmentStage, ComputeStage }`
- `enum Variant { StandardShader, BatchableVertexShader, UInt16IndexedVertexAsComputeShader, UInt32IndexedVertexAsComputeShader, NonIndexedVertexAsComputeShader, HdrCapableFragmentShader }`

### 公有函数

- `QShader()`
- `QShader(const QShader &other)`
- `(since 6.7) QShader(QShader &&other)`
- `~QShader()`
- `QList<QShaderKey> availableShaders() const`
- `QShaderDescription description() const`
- `bool isValid() const`
- `QShader::NativeResourceBindingMap nativeResourceBindingMap(const QShaderKey &key) const`
- `QShader::NativeShaderInfo nativeShaderInfo(const QShaderKey &key) const`
- `void removeNativeShaderInfo(const QShaderKey &key)`
- `void removeResourceBindingMap(const QShaderKey &key)`
- `void removeSeparateToCombinedImageSamplerMappingList(const QShaderKey &key)`
- `void removeShader(const QShaderKey &key)`
- `QShader::SeparateToCombinedImageSamplerMappingList separateToCombinedImageSamplerMappingList(const QShaderKey &key) const`
- `QByteArray serialized(QShader::SerializedFormatVersion version = SerializedFormatVersion::Latest) const`
- `void setDescription(const QShaderDescription &desc)`
- `void setNativeShaderInfo(const QShaderKey &key, const QShader::NativeShaderInfo &info)`
- `void setResourceBindingMap(const QShaderKey &key, const QShader::NativeResourceBindingMap &map)`
- `void setSeparateToCombinedImageSamplerMappingList(const QShaderKey &key, const QShader::SeparateToCombinedImageSamplerMappingList &list)`
- `void setShader(const QShaderKey &key, const QShaderCode &shader)`
- `void setStage(QShader::Stage stage)`
- `QShaderCode shader(const QShaderKey &key) const`
- `QShader::Stage stage() const`
- `(since 6.7) void swap(QShader &other)`
- `(since 6.7) QShader & operator=(QShader &&other)`
- `QShader & operator=(const QShader &other)`

### 静态公有成员

- `QShader fromSerialized(const QByteArray &data)`

### 相关非成员函数

- `size_t qHash(const QShader &key, size_t seed = 0)`
- `bool operator!=(const QShader &lhs, const QShader &rhs)`
- `bool operator==(const QShader &lhs, const QShader &rhs)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 40 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `[alias] QShader::NativeResourceBindingMap`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QShader` 的配置属性。初始化或状态切换时通过 `setNativeResourceBindingMap(...)` 设置，之后用 `NativeResourceBindingMap()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:NativeResourceBindingMap`。
- 属性名：`QShader`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[alias] QShader::SeparateToCombinedImageSamplerMappingList`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QShader` 的配置属性。初始化或状态切换时通过 `setSeparateToCombinedImageSamplerMappingList(...)` 设置，之后用 `SeparateToCombinedImageSamplerMappingList()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:SeparateToCombinedImageSamplerMappingList`。
- 属性名：`QShader`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum class QShader::SerializedFormatVersion`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QShader` 暴露的类型声明 `class`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:SerializedFormatVersion`。
- 属性名：`QShader`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QShader::Source`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QShader` 暴露的类型声明 `来源`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Source`。
- 属性名：`QShader`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QShader::Stage`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QShader` 暴露的类型声明 `Stage`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Stage`。
- 属性名：`QShader`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QShader::Variant`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QShader` 暴露的类型声明 `Variant`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Variant`。
- 属性名：`QShader`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QShader::QShader()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QShader` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QShader::QShader(const QShader &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QShader` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `const QShader &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept, since 6.7] QShader::QShader(QShader &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QShader` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `QShader &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QShader::~QShader()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QShader` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QShaderKey> QShader::availableShaders() const`

**API 类别：** 成员函数说明

**中文解读：** `QShader::availableShaders` 用于计算、查询或取得与“可用量、Shaders”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<QShaderKey>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QShaderKey>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QShaderDescription QShader::description() const`

**API 类别：** 成员函数说明

**中文解读：** `QShader::description` 用于计算、查询或取得与“description”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QShaderDescription`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QShaderDescription`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QShader QShader::fromSerialized(const QByteArray &data)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromSerialized`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QShader`。
- 参数 `data`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QShader::isValid() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isValid`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QShader::NativeResourceBindingMap QShader::nativeResourceBindingMap(const QShaderKey &key) const`

**API 类别：** 成员函数说明

**中文解读：** `QShader::nativeResourceBindingMap` 用于计算、查询或取得与“native、Resource、Binding、映射”相关的操作。调用时要先确认当前状态和 `key` 的有效范围；返回类型是 `QShader::NativeResourceBindingMap`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QShader::NativeResourceBindingMap`。
- 参数 `key`：类型为 `const QShaderKey &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QShader::NativeShaderInfo QShader::nativeShaderInfo(const QShaderKey &key) const`

**API 类别：** 成员函数说明

**中文解读：** `QShader::nativeShaderInfo` 用于计算、查询或取得与“native、Shader、Info”相关的操作。调用时要先确认当前状态和 `key` 的有效范围；返回类型是 `QShader::NativeShaderInfo`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QShader::NativeShaderInfo`。
- 参数 `key`：类型为 `const QShaderKey &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QShader::removeNativeShaderInfo(const QShaderKey &key)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeNativeShaderInfo`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数 `key`：类型为 `const QShaderKey &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QShader::removeResourceBindingMap(const QShaderKey &key)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeResourceBindingMap`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数 `key`：类型为 `const QShaderKey &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QShader::removeSeparateToCombinedImageSamplerMappingList(const QShaderKey &key)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeSeparateToCombinedImageSamplerMappingList`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数 `key`：类型为 `const QShaderKey &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QShader::removeShader(const QShaderKey &key)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeShader`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数 `key`：类型为 `const QShaderKey &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QShader::SeparateToCombinedImageSamplerMappingList QShader::separateToCombinedImageSamplerMappingList(const QShaderKey &key) const`

**API 类别：** 成员函数说明

**中文解读：** `QShader::separateToCombinedImageSamplerMappingList` 用于计算、查询或取得与“separate、转换输出、Combined、Image、Sampler、Mapping、List”相关的操作。调用时要先确认当前状态和 `key` 的有效范围；返回类型是 `QShader::SeparateToCombinedImageSamplerMappingList`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QShader::SeparateToCombinedImageSamplerMappingList`。
- 参数 `key`：类型为 `const QShaderKey &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray QShader::serialized(QShader::SerializedFormatVersion version = SerializedFormatVersion::Latest) const`

**API 类别：** 成员函数说明

**中文解读：** `QShader::serialized` 用于计算、查询或取得与“serialized”相关的操作。调用时要先确认当前状态和 `version` 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `version`：类型为 `QShader::SerializedFormatVersion`。默认值为 `SerializedFormatVersion::Latest`。传入 `QShader::SerializedFormatVersion` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QShader::setDescription(const QShaderDescription &desc)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setDescription`。调用它会改变 `QShader` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `desc`：类型为 `const QShaderDescription &`。没有默认值，调用时必须提供。传入 `const QShaderDescription &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QShader::setNativeShaderInfo(const QShaderKey &key, const QShader::NativeShaderInfo &info)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setNativeShaderInfo`。调用它会改变 `QShader` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `key`：类型为 `const QShaderKey &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `info`：类型为 `const QShader::NativeShaderInfo &`。没有默认值，调用时必须提供。传入 `const QShader::NativeShaderInfo &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QShader::setResourceBindingMap(const QShaderKey &key, const QShader::NativeResourceBindingMap &map)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setResourceBindingMap`。调用它会改变 `QShader` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `key`：类型为 `const QShaderKey &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `map`：类型为 `const QShader::NativeResourceBindingMap &`。没有默认值，调用时必须提供。传入 `const QShader::NativeResourceBindingMap &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QShader::setSeparateToCombinedImageSamplerMappingList(const QShaderKey &key, const QShader::SeparateToCombinedImageSamplerMappingList &list)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSeparateToCombinedImageSamplerMappingList`。调用它会改变 `QShader` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `key`：类型为 `const QShaderKey &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `list`：类型为 `const QShader::SeparateToCombinedImageSamplerMappingList &`。没有默认值，调用时必须提供。传入 `const QShader::SeparateToCombinedImageSamplerMappingList &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QShader::setShader(const QShaderKey &key, const QShaderCode &shader)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setShader`。调用它会改变 `QShader` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `key`：类型为 `const QShaderKey &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `shader`：类型为 `const QShaderCode &`。没有默认值，调用时必须提供。传入 `const QShaderCode &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QShader::setStage(QShader::Stage stage)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setStage`。调用它会改变 `QShader` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `stage`：类型为 `QShader::Stage`。没有默认值，调用时必须提供。传入 `QShader::Stage` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QShaderCode QShader::shader(const QShaderKey &key) const`

**API 类别：** 成员函数说明

**中文解读：** `QShader::shader` 用于计算、查询或取得与“shader”相关的操作。调用时要先确认当前状态和 `key` 的有效范围；返回类型是 `QShaderCode`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QShaderCode`。
- 参数 `key`：类型为 `const QShaderKey &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QShader::Stage QShader::stage() const`

**API 类别：** 成员函数说明

**中文解读：** `QShader::stage` 用于计算、查询或取得与“stage”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QShader::Stage`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QShader::Stage`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept, since 6.7] void QShader::swap(QShader &other)`

**API 类别：** 成员函数说明

**中文解读：** `QShader::swap` 用于执行与“swap”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `other`：类型为 `QShader &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept, since 6.7] QShader &QShader::operator=(QShader &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QShader` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QShader &`。
- 参数 `other`：类型为 `QShader &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QShader &QShader::operator=(const QShader &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QShader` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QShader &`。
- 参数 `other`：类型为 `const QShader &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] size_t qHash(const QShader &key, size_t seed = 0)`

**API 类别：** 相关非成员函数

**中文解读：** `QShader::qHash` 用于计算、查询或取得与“q、Hash”相关的操作。调用时要先确认当前状态和 `key`、`seed` 的有效范围；返回类型是 `size_t`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`size_t`。
- 参数 `key`：类型为 `const QShader &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `seed`：类型为 `size_t`。默认值为 `0`。传入 `size_t` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator!=(const QShader &lhs, const QShader &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QShader` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QShader &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QShader &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator==(const QShader &lhs, const QShader &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QShader` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QShader &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QShader &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `struct NativeShaderInfo`

**API 类别：** 公有类型

**中文解读：** 这是 `QShader` 的 `Native、Shader、Info` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `struct SeparateToCombinedImageSamplerMapping`

**API 类别：** 公有类型

**中文解读：** 这是 `QShader` 的 `Separate、转换输出、Combined、Image、Sampler、Mapping` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `NativeResourceBindingMap`

**API 类别：** 公有类型

**中文解读：** 这是 `QShader` 的 `Native、Resource、Binding、映射` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `SeparateToCombinedImageSamplerMappingList`

**API 类别：** 公有类型

**中文解读：** 这是 `QShader` 的 `Separate、转换输出、Combined、Image、Sampler、Mapping、List` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

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

`QShader` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
