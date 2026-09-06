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

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[alias] QShader::NativeResourceBindingMap`

**作用与语义：**

`QMap`<int、std：:p air<int、int>>的同义词。
`QRhi`假设的资源绑定模型基于SPIR-V。这意味着统一缓冲区、存储缓冲区、合并图像采样器和存储图像共享一个绑定点空间。`QShaderDescription`和`QRhiShaderResourceBinding`中的绑定编号预计与Vulkan兼容GLSL着色器的`binding`布局限定符相匹配。
除Vulkan外，图形API可能使用不完全兼容的资源绑定模型。SPIR-V翻译的着色器代码生成器可能因各种原因选择不考虑SPIR-V绑定限定条件。例如，SPIRV-Cross的Metal后端就是如此。此外，即使大多数情况下自动隐式转换（例如使用SPIR-V绑定点作为HLSL资源寄存器索引），分配资源绑定而不受SPIR-V绑定点限制，也能获得更好的结果。
因此，`QShader`可能会暴露一个额外的映射，描述给定SPIR-V绑定的原生绑定点。相关`QRhi`后端应自动使用该映射，视情况而定。值为对，因为组合图像采样器可能映射到两个本地资源（纹理和采样器），在某些着色语言中。此时第二个值指的是采样器。
注意：本地绑定可能为 -1，以防着色器中没有资源的激活绑定。（例如，声明了一个统一块，但着色器代码中未使用）映射始终完整，意味着所有声明的统一块、存储块、图像对象和合并采样器都有条目，但对于着色器函数中未实际引用的块，值为 -1。

### `[alias] QShader::SeparateToCombinedImageSamplerMappingList`

**作用与语义：**

`QList`的同义词<`QShader::SeparateToCombinedImageSamplerMapping`>。

### `enum class QShader::SerializedFormatVersion`

**作用与语义：**

描述序列化`QShader`时所需的输出格式。
`serialized()` `version`参数的默认值为 `Latest`。在绝大多数情况下，这已足够。只有当意图生成可被早期 Qt 版本加载的序列化数据时，才需要指定另一个值。例如，`qsb` 工具在给出 `--qsbversion` 命令行参数时使用这些枚举值。
注意：针对早期版本会使某些功能在生成的资产中失效。当该资产与指定的旧 Qt 版本一起使用时，这不会成为问题，因为该 Qt 版本不具备依赖于`QShader`中额外生成数据和序列化数据流的新特性，但如果生成的资产随后与较新的 Qt 版本一起使用，可能会成为问题。
- `QShader::SerializedFormatVersion::Latest`：`0`;当前的Qt版本
- `QShader::SerializedFormatVersion::Qt_6_5`：`1`;Qt 6.5
- `QShader::SerializedFormatVersion::Qt_6_4`：`2`;Qt 6.4

### `enum QShader::Source`

**作用与语义：**

描述条目包含哪种着色器代码。
- `QShader::SpirvShader`：`0`;SPIR-V
- `QShader::GlslShader`：`1`;GLSL
- `QShader::HlslShader`：`2`;HLSL
- `QShader::DxbcShader`：`3`;Direct3D 字节码（由 `fxc` 编译的 HLSL）
- `QShader::MslShader`：`4`;金属着色语言
- `QShader::DxilShader`：`5`;Direct3D 字节码（由 `dxc` 编译的 HLSL）
- `QShader::MetalLibShader`：`6`;预编译的金属字节码
- `QShader::WgslShader`：`7`;WGSL

### `enum QShader::Stage`

**作用与语义：**

描述着色器适合的图形流水线阶段。
- `QShader::VertexStage`：`0`;顶点着色器
- `QShader::TessellationControlStage`：`1`;镶嵌控制（船体）着色器
- `QShader::TessellationEvaluationStage`：`2`;镶嵌评估（域）着色器
- `QShader::GeometryStage`：`3`;几何着色器
- `QShader::FragmentStage`：`4`;片段（像素）着色器
- `QShader::ComputeStage`：`5`;计算着色器

### `enum QShader::Variant`

**作用与语义：**

描述条目包含哪种着色器代码。
- `QShader::StandardShader`：`0`;着色器代码的正常、未修改版本。
- `QShader::BatchableVertexShader`：`1`;顶点着色器重写，以适用于Qt Quick场景图批处理。
- `QShader::UInt16IndexedVertexAsComputeShader`：`2`;顶点着色器，设计用于带有镶嵌的Metal管道中，结合索引绘制调用，从uint16索引缓冲区获取索引数据。为支持金属镶嵌流水线，顶点着色器被转换为计算着色器，可能依赖于绘制调用中的索引缓冲区使用情况（例如着色器使用gl_VertexIndex），因此需要三种专用变体。
- `QShader::UInt32IndexedVertexAsComputeShader`：`3`;顶点着色器设计用于金属流水线，结合镶嵌和索引绘画调用，从uint32索引缓冲区获取索引数据。为了支持金属镶嵌流水线，顶点着色器被转换为计算着色器，可能依赖于绘制调用中的索引缓冲区使用情况（例如着色器使用gl_VertexIndex），因此需要三种专用变体。
- `QShader::NonIndexedVertexAsComputeShader`：`4`;顶点着色器，用于金属流水线中，结合镶嵌和非索引绘制调用。为了支持金属镶嵌流水线，顶点着色器被转换成计算着色器，可能依赖于绘制调用中的索引缓冲区使用情况（例如着色器使用gl_VertexIndex），因此需要三种专用变体。
- `QShader::HdrCapableFragmentShader (since Qt 6.10)`：`5`;一个重写的片段着色器，以支持Qt Quick场景图中的高动态范围渲染。

### `QShader::QShader()`

**作用与语义：**

构造一个新的、空的（因此无效）QShader 实例。

### `QShader::QShader(const QShader &other)`

**作用与语义：**

复制了`other`。

### `[noexcept, since 6.7] QShader::QShader(QShader &&other)`

**作用与语义：**

从`other`中构造出新的QShader。
注意：移出对象`other`处于部分成形状态，唯一有效的操作是销毁和赋予新值。

### `[noexcept] QShader::~QShader()`

**作用与语义：**

毁灭者。

### `QList<QShaderKey> QShader::availableShaders() const`

**作用与语义：**

返回可用的着色器版本列表。

### `QShaderDescription QShader::description() const`

**作用与语义：**

返回着色器的反射元数据。

### `[static] QShader QShader::fromSerialized(const QByteArray &data)`

**作用与语义：**

从给定的`data`创建一个新的`QShader`实例。
如果无法成功反序列化`data`，结果是默认构造`QShader`，`isValid()`返回`false`。
警告：着色器包，包括文件系统中的`.qsb`文件，被假定为可信内容。建议应用开发者在允许加载非应用用户提供内容前，仔细考虑潜在影响。

### `bool QShader::isValid() const`

**作用与语义：**

如果`QShader`包含至少一个着色器版本，则返回为真。

### `QShader::NativeResourceBindingMap QShader::nativeResourceBindingMap(const QShaderKey &key) const`

**作用与语义：**

返回`key`的本地绑定映射。如果没有可用的映射`key`，则映射为空的（例如，映射不适用于`key`描述的API和着色语言）。

### `QShader::NativeShaderInfo QShader::nativeShaderInfo(const QShaderKey &key) const`

**作用与语义：**

例如，返回本地着色器信息结构`key`体（如无`key`数据，则返回空对象，因为此类映射不适用于着色语言或着色器阶段。

### `void QShader::removeNativeShaderInfo(const QShaderKey &key)`

**作用与语义：**

移除了`key`的原生着色器信息。

### `void QShader::removeResourceBindingMap(const QShaderKey &key)`

**作用与语义：**

移除了`key`的原生资源绑定映射。

### `void QShader::removeSeparateToCombinedImageSamplerMappingList(const QShaderKey &key)`

**作用与语义：**

移除`key`的合成图像采样映射列表。

### `void QShader::removeShader(const QShaderKey &key)`

**作用与语义：**

移除给定`key`的源代码或二进制着色器代码。找不到时什么都不做。

### `QShader::SeparateToCombinedImageSamplerMappingList QShader::separateToCombinedImageSamplerMappingList(const QShaderKey &key) const`

**作用与语义：**

返回`key`的合成图像采样映射列表，或者如果没有可供 `key` 的数据，则返回空列表，例如因为此类映射不适用于着色语言。

### `QByteArray QShader::serialized(QShader::SerializedFormatVersion version = SerializedFormatVersion::Latest) const`

**作用与语义：**

返回`QShader`所保存的所有数据的串行化二进制版本，适合写入文件或其他I/O设备。
默认情况下，使用最新的序列化格式。使用`version`参数序列化以实现兼容的Qt版本。只有当确定生成的数据流必须与较旧的Qt版本兼容，但这会导致其与自该Qt版本以来引入的功能不兼容时，才应使用其他值（例如Qt 6.5的`Qt_6_5`）。

### `void QShader::setDescription(const QShaderDescription &desc)`

**作用与语义：**

将反射元数据设置为`desc`。

### `void QShader::setNativeShaderInfo(const QShaderKey &key, const QShader::NativeShaderInfo &info)`

**作用与语义：**

存储与`key`关联的本地着色器`info`。

### `void QShader::setResourceBindingMap(const QShaderKey &key, const QShader::NativeResourceBindingMap &map)`

**作用与语义：**

存储与`key`相关的本地资源绑定`map`。

### `void QShader::setSeparateToCombinedImageSamplerMappingList(const QShaderKey &key, const QShader::SeparateToCombinedImageSamplerMappingList &list)`

**作用与语义：**

存储与`key`关联的给定合并图像采样器映射的映射`list`。

### `void QShader::setShader(const QShaderKey &key, const QShaderCode &shader)`

**作用与语义：**

存储`key`指定着色器版本的源代码或二进制代码`shader`。

### `void QShader::setStage(QShader::Stage stage)`

**作用与语义：**

为`stage`设定流程。

### `QShaderCode QShader::shader(const QShaderKey &key) const`

**作用与语义：**

返回由`key`指定的特定着色器版本的源代码或二进制代码。

### `QShader::Stage QShader::stage() const`

**作用与语义：**

返回着色器本应使用的流水线阶段。

### `[noexcept, since 6.7] void QShader::swap(QShader &other)`

**作用与语义：**

将着色器与`other`交换。这个操作非常快，从未失败过。

### `[noexcept, since 6.7] QShader &QShader::operator=(QShader &&other)`

**作用与语义：**

Move-assign `other` 到这个`QShader`实例。
注意：移出对象 `other` 处于部分成形状态，唯一有效的操作是销毁和赋予新值。

### `QShader &QShader::operator=(const QShader &other)`

**作用与语义：**

为该对象分配`other`。

### `[noexcept] size_t qHash(const QShader &key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `[noexcept] bool operator!=(const QShader &lhs, const QShader &rhs)`

**作用与语义：**

如果两个 `QShader` 对象 `lhs` 和 `rhs` 中的值相等，则返回 `false`；否则返回 `true`。

### `[noexcept] bool operator==(const QShader &lhs, const QShader &rhs)`

**作用与语义：**

如果两个`QShader`对象`lhs`和`rhs`相等，返回`true`，意味着它们属于同一阶段，且有匹配的着色器源代码或二进制代码集合。

### `struct NativeShaderInfo`

**作用与语义：**

关于本地着色器代码的额外元数据。
描述本地着色器代码（如适用）的信息。对于某些着色器语言的特定着色器阶段，如果从SPIR-V翻译时需要在生成的着色器中引入额外的“神奇”输入、输出或资源，这一点尤为重要。这些添加可能依赖于原始源代码（即各种GLSL语言结构或内置内容的使用），因此如果某些功能被添加到生成的着色器代码中，需要动态地标示。
举例来说，考虑一个带有每个补丁（而非顶点）输出变量的镶嵌控制着色器。这被转换为Metal计算着色器输出（包括其他）到spvPatchOut缓冲区。但如果不使用每个补丁的输出变量，这个缓冲区根本不存在。着色器代码依赖于这种缓冲区，可以从该结构体中的数据看出。
注意：这是一个具有有限兼容性保证的RHI API，详情请参见 `QShader`。

### `struct SeparateToCombinedImageSamplerMapping`

**作用与语义：**

采样器制服的元数据映射。
描述了从传统合成图像采样器统一映射到独立纹理和采样器的绑定点。
例如，如果`combinedImageSampler`是`"_54"`，`textureBinding`是`1`，`samplerBinding`是`2`，这意味着GLSL着色器代码包含一个名为`_54`的`sampler2D`（或sampler3D等）统一码，对应原始着色器中的两个独立资源绑定（`1`和`2`）。
注意：这是一个具有有限兼容性保证的RHI API，详情请参见 `QShader`。

### `NativeResourceBindingMap`

**作用与语义：**

`QMap`<int、std：:p air<int、int>>的同义词。
`QRhi`假设的资源绑定模型基于SPIR-V。这意味着统一缓冲区、存储缓冲区、合并图像采样器和存储图像共享一个绑定点空间。`QShaderDescription`和`QRhiShaderResourceBinding`中的绑定编号预计与Vulkan兼容GLSL着色器的`binding`布局限定符相匹配。
除Vulkan外，图形API可能使用不完全兼容的资源绑定模型。SPIR-V翻译的着色器代码生成器可能因各种原因选择不考虑SPIR-V绑定限定条件。例如，SPIRV-Cross的Metal后端就是如此。此外，即使大多数情况下自动隐式转换（例如使用SPIR-V绑定点作为HLSL资源寄存器索引），分配资源绑定而不受SPIR-V绑定点限制，也能获得更好的结果。
因此，`QShader`可能会暴露一个额外的映射，描述给定SPIR-V绑定的原生绑定点。相关`QRhi`后端应自动使用该映射，视情况而定。值为对，因为组合图像采样器可能映射到两个本地资源（纹理和采样器），在某些着色语言中。此时第二个值指的是采样器。
注意：本地绑定可能为 -1，以防着色器中没有资源的激活绑定。（例如，声明了一个统一块，但着色器代码中未使用）映射始终完整，意味着所有声明的统一块、存储块、图像对象和合并采样器都有条目，但对于着色器函数中未实际引用的块，值为 -1。

### `SeparateToCombinedImageSamplerMappingList`

**作用与语义：**

`QList`的同义词<`QShader::SeparateToCombinedImageSamplerMapping`>。

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
