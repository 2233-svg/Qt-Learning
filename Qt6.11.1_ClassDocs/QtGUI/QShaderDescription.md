# QShaderDescription

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QShaderDescription` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QShaderDescription>`
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

- `(since 6.6) struct BlockVariable`
- `(since 6.6) struct BuiltinVariable`
- `(since 6.6) struct InOutVariable`
- `(since 6.6) struct PushConstantBlock`
- `(since 6.6) struct StorageBlock`
- `(since 6.6) struct UniformBlock`
- `enum BuiltinType { PositionBuiltin, PointSizeBuiltin, ClipDistanceBuiltin, CullDistanceBuiltin, VertexIdBuiltin, …, ViewIndexBuiltin }`
- `enum ImageFlag { ReadOnlyImage, WriteOnlyImage }`
- `flags ImageFlags`
- `enum ImageFormat { ImageFormatUnknown, ImageFormatRgba32f, ImageFormatRgba16f, ImageFormatR32f, ImageFormatRgba8, …, ImageFormatR8ui }`
- `enum QualifierFlag { QualifierReadOnly, QualifierWriteOnly, QualifierCoherent, QualifierVolatile, QualifierRestrict }`
- `flags QualifierFlags`
- `enum TessellationMode { UnknownTessellationMode, TrianglesTessellationMode, QuadTessellationMode, IsolineTessellationMode }`
- `enum TessellationPartitioning { UnknownTessellationPartitioning, EqualTessellationPartitioning, FractionalEvenTessellationPartitioning, FractionalOddTessellationPartitioning }`
- `enum TessellationWindingOrder { UnknownTessellationWindingOrder, CwTessellationWindingOrder, CcwTessellationWindingOrder }`
- `enum VariableType { Unknown, Float, Vec2, Vec3, Vec4, …, Half4 }`

### 公有函数

- `QShaderDescription()`
- `QShaderDescription(const QShaderDescription &other)`
- `~QShaderDescription()`
- `QList<QShaderDescription::InOutVariable> combinedImageSamplers() const`
- `std::array<uint, 3> computeShaderLocalSize() const`
- `QList<QShaderDescription::BuiltinVariable> inputBuiltinVariables() const`
- `QList<QShaderDescription::InOutVariable> inputVariables() const`
- `bool isValid() const`
- `QList<QShaderDescription::BuiltinVariable> outputBuiltinVariables() const`
- `QList<QShaderDescription::InOutVariable> outputVariables() const`
- `QList<QShaderDescription::PushConstantBlock> pushConstantBlocks() const`
- `void serialize(QDataStream *stream, int version) const`
- `QList<QShaderDescription::StorageBlock> storageBlocks() const`
- `QList<QShaderDescription::InOutVariable> storageImages() const`
- `QShaderDescription::TessellationMode tessellationMode() const`
- `uint tessellationOutputVertexCount() const`
- `QShaderDescription::TessellationPartitioning tessellationPartitioning() const`
- `QShaderDescription::TessellationWindingOrder tessellationWindingOrder() const`
- `QByteArray toJson() const`
- `QList<QShaderDescription::UniformBlock> uniformBlocks() const`
- `QShaderDescription & operator=(const QShaderDescription &other)`

### 静态公有成员

- `QShaderDescription deserialize(QDataStream *stream, int version)`

### 相关非成员函数

- `bool operator==(const QShaderDescription &lhs, const QShaderDescription &rhs)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QShaderDescription::BuiltinType`

**作用与语义：**

内置变量类型。
- `QShaderDescription::PositionBuiltin`：`0`
- `QShaderDescription::PointSizeBuiltin`：`1`
- `QShaderDescription::ClipDistanceBuiltin`：`3`
- `QShaderDescription::CullDistanceBuiltin`：`4`
- `QShaderDescription::VertexIdBuiltin`：`5`
- `QShaderDescription::InstanceIdBuiltin`：`6`
- `QShaderDescription::PrimitiveIdBuiltin`：`7`
- `QShaderDescription::InvocationIdBuiltin`：`8`
- `QShaderDescription::LayerBuiltin`：`9`
- `QShaderDescription::ViewportIndexBuiltin`：`10`
- `QShaderDescription::TessLevelOuterBuiltin`：`11`
- `QShaderDescription::TessLevelInnerBuiltin`：`12`
- `QShaderDescription::TessCoordBuiltin`：`13`
- `QShaderDescription::PatchVerticesBuiltin`：`14`
- `QShaderDescription::FragCoordBuiltin`：`15`
- `QShaderDescription::PointCoordBuiltin`：`16`
- `QShaderDescription::FrontFacingBuiltin`：`17`
- `QShaderDescription::SampleIdBuiltin`：`18`
- `QShaderDescription::SamplePositionBuiltin`：`19`
- `QShaderDescription::SampleMaskBuiltin`：`20`
- `QShaderDescription::FragDepthBuiltin`：`22`
- `QShaderDescription::NumWorkGroupsBuiltin`：`24`
- `QShaderDescription::WorkgroupSizeBuiltin`：`25`
- `QShaderDescription::WorkgroupIdBuiltin`：`26`
- `QShaderDescription::LocalInvocationIdBuiltin`：`27`
- `QShaderDescription::GlobalInvocationIdBuiltin`：`28`
- `QShaderDescription::LocalInvocationIndexBuiltin`：`29`
- `QShaderDescription::VertexIndexBuiltin`：`42`
- `QShaderDescription::InstanceIndexBuiltin`：`43`
- `QShaderDescription::ViewIndexBuiltin`：`4440`

### `enum QShaderDescription::ImageFlagflags QShaderDescription::ImageFlags`

**作用与语义：**

图片标记。
- `QShaderDescription::ReadOnlyImage`：`1 << 0`
- `QShaderDescription::WriteOnlyImage`：`1 << 1`
ImageFlags 类型是 QFlags 的 typedef<ImageFlag>。它存储 ImageFlag 值的 OR 组合。

### `enum QShaderDescription::ImageFormat`

**作用与语义：**

图片格式。
- `QShaderDescription::ImageFormatUnknown`：`0`
- `QShaderDescription::ImageFormatRgba32f`：`1`
- `QShaderDescription::ImageFormatRgba16f`：`2`
- `QShaderDescription::ImageFormatR32f`：`3`
- `QShaderDescription::ImageFormatRgba8`：`4`
- `QShaderDescription::ImageFormatRgba8Snorm`：`5`
- `QShaderDescription::ImageFormatRg32f`：`6`
- `QShaderDescription::ImageFormatRg16f`：`7`
- `QShaderDescription::ImageFormatR11fG11fB10f`：`8`
- `QShaderDescription::ImageFormatR16f`：`9`
- `QShaderDescription::ImageFormatRgba16`：`10`
- `QShaderDescription::ImageFormatRgb10A2`：`11`
- `QShaderDescription::ImageFormatRg16`：`12`
- `QShaderDescription::ImageFormatRg8`：`13`
- `QShaderDescription::ImageFormatR16`：`14`
- `QShaderDescription::ImageFormatR8`：`15`
- `QShaderDescription::ImageFormatRgba16Snorm`：`16`
- `QShaderDescription::ImageFormatRg16Snorm`：`17`
- `QShaderDescription::ImageFormatRg8Snorm`：`18`
- `QShaderDescription::ImageFormatR16Snorm`：`19`
- `QShaderDescription::ImageFormatR8Snorm`：`20`
- `QShaderDescription::ImageFormatRgba32i`：`21`
- `QShaderDescription::ImageFormatRgba16i`：`22`
- `QShaderDescription::ImageFormatRgba8i`：`23`
- `QShaderDescription::ImageFormatR32i`：`24`
- `QShaderDescription::ImageFormatRg32i`：`25`
- `QShaderDescription::ImageFormatRg16i`：`26`
- `QShaderDescription::ImageFormatRg8i`：`27`
- `QShaderDescription::ImageFormatR16i`：`28`
- `QShaderDescription::ImageFormatR8i`：`29`
- `QShaderDescription::ImageFormatRgba32ui`：`30`
- `QShaderDescription::ImageFormatRgba16ui`：`31`
- `QShaderDescription::ImageFormatRgba8ui`：`32`
- `QShaderDescription::ImageFormatR32ui`：`33`
- `QShaderDescription::ImageFormatRgb10a2ui`：`34`
- `QShaderDescription::ImageFormatRg32ui`：`35`
- `QShaderDescription::ImageFormatRg16ui`：`36`
- `QShaderDescription::ImageFormatRg8ui`：`37`
- `QShaderDescription::ImageFormatR16ui`：`38`
- `QShaderDescription::ImageFormatR8ui`：`39`

### `enum QShaderDescription::QualifierFlagflags QShaderDescription::QualifierFlags`

**作用与语义：**

资格赛标志。
- `QShaderDescription::QualifierReadOnly`：`1 << 0`
- `QShaderDescription::QualifierWriteOnly`：`1 << 1`
- `QShaderDescription::QualifierCoherent`：`1 << 2`
- `QShaderDescription::QualifierVolatile`：`1 << 3`
- `QShaderDescription::QualifierRestrict`：`1 << 4`
QualifierFlags 类型是 QFlags 的 typedef<QualifierFlag>。它存储 QualifierFlag 值的 OR 组合。

### `enum QShaderDescription::VariableType`

**作用与语义：**

表示变量或块成员的类型。
- `QShaderDescription::Unknown`：`0`
- `QShaderDescription::Float`：`1`
- `QShaderDescription::Vec2`：`2`
- `QShaderDescription::Vec3`：`3`
- `QShaderDescription::Vec4`：`4`
- `QShaderDescription::Mat2`：`5`
- `QShaderDescription::Mat2x3`：`6`
- `QShaderDescription::Mat2x4`：`7`
- `QShaderDescription::Mat3`：`8`
- `QShaderDescription::Mat3x2`：`9`
- `QShaderDescription::Mat3x4`：`10`
- `QShaderDescription::Mat4`：`11`
- `QShaderDescription::Mat4x2`：`12`
- `QShaderDescription::Mat4x3`：`13`
- `QShaderDescription::Int`：`14`
- `QShaderDescription::Int2`：`15`
- `QShaderDescription::Int3`：`16`
- `QShaderDescription::Int4`：`17`
- `QShaderDescription::Uint`：`18`
- `QShaderDescription::Uint2`：`19`
- `QShaderDescription::Uint3`：`20`
- `QShaderDescription::Uint4`：`21`
- `QShaderDescription::Bool`：`22`
- `QShaderDescription::Bool2`：`23`
- `QShaderDescription::Bool3`：`24`
- `QShaderDescription::Bool4`：`25`
- `QShaderDescription::Double`：`26`
- `QShaderDescription::Double2`：`27`
- `QShaderDescription::Double3`：`28`
- `QShaderDescription::Double4`：`29`
- `QShaderDescription::DMat2`：`30`
- `QShaderDescription::DMat2x3`：`31`
- `QShaderDescription::DMat2x4`：`32`
- `QShaderDescription::DMat3`：`33`
- `QShaderDescription::DMat3x2`：`34`
- `QShaderDescription::DMat3x4`：`35`
- `QShaderDescription::DMat4`：`36`
- `QShaderDescription::DMat4x2`：`37`
- `QShaderDescription::DMat4x3`：`38`
- `QShaderDescription::Sampler1D`：`39`
- `QShaderDescription::Sampler2D`：`40`
- `QShaderDescription::Sampler2DMS`：`41`
- `QShaderDescription::Sampler3D`：`42`
- `QShaderDescription::SamplerCube`：`43`
- `QShaderDescription::Sampler1DArray`：`44`
- `QShaderDescription::Sampler2DArray`：`45`
- `QShaderDescription::Sampler2DMSArray`：`46`
- `QShaderDescription::Sampler3DArray`：`47`
- `QShaderDescription::SamplerCubeArray`：`48`
- `QShaderDescription::SamplerRect`：`49`
- `QShaderDescription::SamplerBuffer`：`50`
- `QShaderDescription::SamplerExternalOES`：`51`
- `QShaderDescription::Sampler`：`52`;用于独立采样器。
- `QShaderDescription::Image1D`：`53`
- `QShaderDescription::Image2D`：`54`
- `QShaderDescription::Image2DMS`：`55`
- `QShaderDescription::Image3D`：`56`
- `QShaderDescription::ImageCube`：`57`
- `QShaderDescription::Image1DArray`：`58`
- `QShaderDescription::Image2DArray`：`59`
- `QShaderDescription::Image2DMSArray`：`60`
- `QShaderDescription::Image3DArray`：`61`
- `QShaderDescription::ImageCubeArray`：`62`
- `QShaderDescription::ImageRect`：`63`
- `QShaderDescription::ImageBuffer`：`64`
- `QShaderDescription::Struct`：`65`
- `QShaderDescription::Half`：`66`
- `QShaderDescription::Half2`：`67`
- `QShaderDescription::Half3`：`68`
- `QShaderDescription::Half4`：`69`

### `QShaderDescription::QShaderDescription()`

**作用与语义：**

构建一个新的空 QShaderDescription。
注意：空意味着`isValid()`为新构建的实例返回`false`。

### `QShaderDescription::QShaderDescription(const QShaderDescription &other)`

**作用与语义：**

复制了`other`。

### `[noexcept] QShaderDescription::~QShaderDescription()`

**作用与语义：**

毁灭者。

### `QList<QShaderDescription::InOutVariable> QShaderDescription::combinedImageSamplers() const`

**作用与语义：**

返回合并图像采样器的列表。
以GLSL/Vulkan着色器为源，`layout(binding = 1) uniform sampler2D tex;`统一生成如下内容：（此处以文本JSON形式显示）。
这并不意味着其他语言版本的着色器也必须使用组合图像采样器，尤其是考虑到该概念可能并非处处存在。例如，HLSL 版本很可能仅使用分别为寄存器 t1 和 s1 的 Texture2D 和 SamplerState 对象。

**官方示例：**

```cpp
 "combinedImageSamplers": [
      {
          "binding": 1,
          "name": "tex",
          "set": 0,
          "type": "sampler2D"
      }
  ]
```

### `std::array<uint, 3> QShaderDescription::computeShaderLocalSize() const`

**作用与语义：**

返回计算着色器的局部大小。
例如，对于带有以下声明的计算着色器，函数返回 { 256， 16， 1}。

**官方示例：**

```cpp
 layout(local_size_x = 256, local_size_y = 16, local_size_z = 1) in;
```

### `[static] QShaderDescription QShaderDescription::deserialize(QDataStream *stream, int version)`

**作用与语义：**

返回从`stream`加载的新`QShaderDescription`。`version` 指定了 QSB 版本。

### `QList<QShaderDescription::BuiltinVariable> QShaderDescription::inputBuiltinVariables() const`

**作用与语义：**

返回用作输入的活动内置物列表。例如，一个晶面分析着色器读取gl_TessCoord和gl_Position的值时，这里会列出`TessCoordBuiltin`和`PositionBuiltin`。

### `QList<QShaderDescription::InOutVariable> QShaderDescription::inputVariables() const`

**作用与语义：**

返回输入变量列表。这包括顶点阶段的顶点输入（有时称为属性）以及其他阶段的输入（有时称为变量）。

### `bool QShaderDescription::isValid() const`

**作用与语义：**

如果`QShaderDescription`中至少包含一个变量和块列表中的一条，则返回为真。

### `QList<QShaderDescription::BuiltinVariable> QShaderDescription::outputBuiltinVariables() const`

**作用与语义：**

返回用作输入的活跃内置变量列表。例如，顶点着色器通常会内置`PositionBuiltin`作为输出。

### `QList<QShaderDescription::InOutVariable> QShaderDescription::outputVariables() const`

**作用与语义：**

返回输出变量列表。

### `QList<QShaderDescription::PushConstantBlock> QShaderDescription::pushConstantBlocks() const`

**作用与语义：**

返回推送常数块的列表。
注意：避免依赖推送常量块来搭配Qt渲染硬件接口使用，因为目前Qt硬件接口不支持。

### `void QShaderDescription::serialize(QDataStream *stream, int version) const`

**作用与语义：**

将此`QShaderDescription`序列化为`stream`。`version` 规定了 QSB 版本。

### `QList<QShaderDescription::StorageBlock> QShaderDescription::storageBlocks() const`

**作用与语义：**

返回着色器存储块列表。
例如，使用 GLSL/Vulkan 着色器作为源代码时，声明。
生成以下内容：（此处以文本JSON形式显示）。
注意：存储块中最后一个成员的大小未定义。该大小显示为`size` 0，数组维度为`[0]`。存储块的 `knownSize` 排除最后一个成员的大小，因为该大小仅在运行时已知。对于未定义数组大小的最后一个成员，数组项之间的字节步幅为 `runtimeArrayStride`。该值根据指定的缓冲区内存布局标准（std140， std430）规则确定。
注意：SSBO不适用于某些图形API，如OpenGL 2.x或3.1之前的OpenGL ES。

**官方示例：**

```cpp
 struct Stuff {
     vec2 a;
     vec2 b;
 };
 layout(std140, binding = 0) buffer StuffSsbo {
     vec4 whatever;
     Stuff stuff[];
 } buf;
```

### `QList<QShaderDescription::InOutVariable> QShaderDescription::storageImages() const`

**作用与语义：**

返回图像变量列表。
这些问题很可能出现在计算着色器中。例如，`layout (binding = 0, rgba8) uniform readonly image2D inputImage;`生成以下内容：（此处以文本JSON形式显示）。
注意：独立的图像对象与某些图形API（如3.1之前的OpenGL 2.x或OpenGL ES）不兼容。

**官方示例：**

```cpp
 "storageImages": [
      {
          "binding": 0,
          "imageFormat": "rgba8",
          "name": "inputImage",
          "set": 0,
          "type": "image2D"
      }
  ]
```

### `QShaderDescription::TessellationMode QShaderDescription::tessellationMode() const`

**作用与语义：**

返回镶嵌控制或评估着色器的镶嵌执行模式。
未设置时返回的值为`UnknownTessellationMode`。
例如，对于带有以下声明的镶嵌评估着色器，函数返回`TrianglesTessellationMode`。

**官方示例：**

```cpp
 layout(triangles) in;
```

### `uint QShaderDescription::tessellationOutputVertexCount() const`

**作用与语义：**

返回输出顶点的数量。
例如，对于带有以下声明的镶嵌控制着色器，函数返回3。

**官方示例：**

```cpp
 layout(vertices = 3) out;
```

### `QShaderDescription::TessellationPartitioning QShaderDescription::tessellationPartitioning() const`

**作用与语义：**

返回镶嵌控制或评估着色器的镶嵌分区模式。
未设置时返回的值为`UnknownTessellationPartitioning`。
例如，对于带有以下声明的镶嵌评估着色器，函数返回`FractionalOddTessellationPartitioning`。

**官方示例：**

```cpp
 layout(triangles, fractional_odd_spacing, ccw) in;
```

### `QShaderDescription::TessellationWindingOrder QShaderDescription::tessellationWindingOrder() const`

**作用与语义：**

返回镶嵌控制或评估着色器的镶嵌绕线顺序。
未设置时返回的值为`UnknownTessellationWindingOrder`。
例如，对于带有以下声明的镶嵌评估着色器，函数返回`CcwTessellationWindingOrder`。

**官方示例：**

```cpp
 layout(triangles, fractional_odd_spacing, ccw) in;
```

### `QByteArray QShaderDescription::toJson() const`

**作用与语义：**

返回序列化的JSON文本版本。
注意：JSON文本没有提供反序列化方法。

### `QList<QShaderDescription::UniformBlock> QShaderDescription::uniformBlocks() const`

**作用与语义：**

返回均匀块列表。

### `QShaderDescription &QShaderDescription::operator=(const QShaderDescription &other)`

**作用与语义：**

为该对象分配`other`。

### `[noexcept] bool operator==(const QShaderDescription &lhs, const QShaderDescription &rhs)`

**作用与语义：**

如果两个`QShaderDescription`对象相等，返回`true` `lhs` 和 `rhs`。

### `(since 6.6) struct BlockVariable`

**作用与语义：**

描述均匀或推常数块的成员。
注意：这是一个具有有限兼容性保证的RHI API，详情请参见 `QShaderDescription`。

### `(since 6.6) struct BuiltinVariable`

**作用与语义：**

描述一个内置变量。
注意：这是一个具有有限兼容性保证的RHI API，详情请参见 `QShaderDescription`。

### `(since 6.6) struct InOutVariable`

**作用与语义：**

描述着色器中的输入或输出变量。
注意：这是一个具有有限兼容性保证的RHI API，详情请参见 `QShaderDescription`。

### `(since 6.6) struct PushConstantBlock`

**作用与语义：**

描述了推送恒定阻挡。
注意：这是一个具有有限兼容性保证的RHI API，详情请参见 `QShaderDescription`。

### `(since 6.6) struct StorageBlock`

**作用与语义：**

描述一个着色器存储块。
注意：这是一个具有有限兼容性保证的RHI API，详情请参见 `QShaderDescription`。

### `(since 6.6) struct UniformBlock`

**作用与语义：**

描述均匀的块状结构。
注意：当转换为不支持统一块的着色语言（如GLSL 120或GLSL/ES 100）时，结构体中的统一块被普通统一块替代。结构体名称，以及由块成员生成的统一前缀，由`structName`给出。
注意：这是一个具有有限兼容性保证的RHI API，详情请参见 `QShaderDescription`。

### `enum ImageFlag { ReadOnlyImage, WriteOnlyImage }`

**作用与语义：**

图片标记。
- `QShaderDescription::ReadOnlyImage`：`1 << 0`
- `QShaderDescription::WriteOnlyImage`：`1 << 1`
ImageFlags 类型是 QFlags 的 typedef<ImageFlag>。它存储 ImageFlag 值的 OR 组合。

### `flags ImageFlags`

**作用与语义：**

图片标记。
- `QShaderDescription::ReadOnlyImage`：`1 << 0`
- `QShaderDescription::WriteOnlyImage`：`1 << 1`
ImageFlags 类型是 QFlags 的 typedef<ImageFlag>。它存储 ImageFlag 值的 OR 组合。

### `enum QualifierFlag { QualifierReadOnly, QualifierWriteOnly, QualifierCoherent, QualifierVolatile, QualifierRestrict }`

**作用与语义：**

资格赛标志。
- `QShaderDescription::QualifierReadOnly`：`1 << 0`
- `QShaderDescription::QualifierWriteOnly`：`1 << 1`
- `QShaderDescription::QualifierCoherent`：`1 << 2`
- `QShaderDescription::QualifierVolatile`：`1 << 3`
- `QShaderDescription::QualifierRestrict`：`1 << 4`
QualifierFlags 类型是 QFlags 的 typedef<QualifierFlag>。它存储 QualifierFlag 值的 OR 组合。

### `flags QualifierFlags`

**作用与语义：**

资格赛标志。
- `QShaderDescription::QualifierReadOnly`：`1 << 0`
- `QShaderDescription::QualifierWriteOnly`：`1 << 1`
- `QShaderDescription::QualifierCoherent`：`1 << 2`
- `QShaderDescription::QualifierVolatile`：`1 << 3`
- `QShaderDescription::QualifierRestrict`：`1 << 4`
QualifierFlags 类型是 QFlags 的 typedef<QualifierFlag>。它存储 QualifierFlag 值的 OR 组合。

### `enum TessellationMode { UnknownTessellationMode, TrianglesTessellationMode, QuadTessellationMode, IsolineTessellationMode }`

**作用与语义：**

指定细分着色器生成图元的形状：`UnknownTessellationMode` 表示未知，`TrianglesTessellationMode` 生成三角形，`QuadTessellationMode` 生成四边形，`IsolineTessellationMode` 生成等值线。读取反射信息后应先排除未知值。

### `enum TessellationPartitioning { UnknownTessellationPartitioning, EqualTessellationPartitioning, FractionalEvenTessellationPartitioning, FractionalOddTessellationPartitioning }`

**作用与语义：**

指定细分级别如何取整和分割：`EqualTessellationPartitioning` 使用等距整数分割，`FractionalEvenTessellationPartitioning` 和 `FractionalOddTessellationPartitioning` 分别使用偶数、奇数分数分割；`UnknownTessellationPartitioning` 表示着色器未提供可识别模式。

### `enum TessellationWindingOrder { UnknownTessellationWindingOrder, CwTessellationWindingOrder, CcwTessellationWindingOrder }`

**作用与语义：**

指定细分后图元的顶点绕序。`CwTessellationWindingOrder` 为顺时针，`CcwTessellationWindingOrder` 为逆时针，`UnknownTessellationWindingOrder` 表示未知；绕序会影响正反面判断和背面剔除。

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

`QShaderDescription` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
