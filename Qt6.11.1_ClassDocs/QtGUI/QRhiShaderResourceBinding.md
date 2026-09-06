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

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QRhiShaderResourceBinding::StageFlagflags QRhiShaderResourceBinding::StageFlags`

**作用与语义：**

标志值用于指示着色器资源在哪些阶段中可见。
- `QRhiShaderResourceBinding::VertexStage`：`1 << 0`;顶点阶段
- `QRhiShaderResourceBinding::TessellationControlStage`：`1 << 1`;镶嵌控制（船体着色器）阶段
- `QRhiShaderResourceBinding::TessellationEvaluationStage`：`1 << 2`;镶嵌评估（领域着色器）阶段
- `QRhiShaderResourceBinding::FragmentStage`：`1 << 4`;片段（像素着色器）阶段
- `QRhiShaderResourceBinding::ComputeStage`：`1 << 5`;计算阶段
- `QRhiShaderResourceBinding::GeometryStage`：`1 << 3`;几何阶段
StageFlags 类型是 QFlags 的 typedef<StageFlag>。它存储 StageFlag 值的 OR 组合。

### `enum QRhiShaderResourceBinding::Type`

**作用与语义：**

指定绑定到绑定点的着色器资源类型。
- `QRhiShaderResourceBinding::UniformBuffer`：`0`;均匀缓冲
- `QRhiShaderResourceBinding::SampledTexture`：`1`;合成图像采样器（纹理和采样器对）。即使底层3D API关联的着色语言不支持该概念（如D3D和HLSL），仍支持该功能，因为着色器翻译层负责绑定点或着色器寄存器的适当转换和重新映射。
- `QRhiShaderResourceBinding::Texture`：`2`;纹理（独立）
- `QRhiShaderResourceBinding::Sampler`：`3`;采样器（独立）
- `QRhiShaderResourceBinding::ImageLoad`：`4`;图像加载（使用 GLSL 时，这映射为对暴露在着色器中的一个或所有图层的单一层级`imageLoad()`，以及作为图像对象暴露给着色器的纹理）
- `QRhiShaderResourceBinding::ImageStore`：`5`;图像存储（使用 GLSL 时，这映射为对暴露在着色器中作为图像对象的纹理进行单一层级的 `imageStore()` 或 imageAtomic*() 操作）
- `QRhiShaderResourceBinding::ImageLoadStore`：`6`;图像加载与存储
- `QRhiShaderResourceBinding::BufferLoad`：`7`;存储缓冲区负载（GLSL 映射为从着色器存储缓冲区读取）
- `QRhiShaderResourceBinding::BufferStore`：`8`;存储缓冲区存储（GLSL 映射写入着色器存储缓冲区）
- `QRhiShaderResourceBinding::BufferLoadStore`：`9`;存储缓冲区加载和存储

### `[static] QRhiShaderResourceBinding QRhiShaderResourceBinding::bufferLoad(int binding, QRhiShaderResourceBinding::StageFlags stage, QRhiBuffer *buf)`

**作用与语义：**

返回只读存储缓冲区的着色器资源绑定，具有给定的`binding`号和流水线`stage`。
注意：当`buf`不是空时，必须是用`QRhiBuffer::StorageBuffer`创建的。
注意：`buf`可以是空的。创建未指定资源的 `QRhiShaderResourceBindings` 是有效的，但此类对象不能与 `QRhiCommandBuffer::setShaderResources()` 一起使用。不过，它适合创建管道。这样的管道必须始终与另一个布局兼容的资源`QRhiShaderResourceBindings`一起使用，这些资源传递给`QRhiCommandBuffer::setShaderResources()`。
注意：缓冲区加载/存储仅保证在计算流水线内可用。虽然部分后端支持在图形流水线中使用这些资源，但并非普遍支持，即使支持，也可能在障碍和同步方面出现意想不到的问题。因此，避免将此类资源与计算以外的着色器一起使用。

### `[static] QRhiShaderResourceBinding QRhiShaderResourceBinding::bufferLoad(int binding, QRhiShaderResourceBinding::StageFlags stage, QRhiBuffer *buf, quint32 offset, quint32 size)`

**作用与语义：**

返回只读存储缓冲区的着色器资源绑定，`binding`号和流水线`stage`。该重载仅绑定区域，按照`offset`和`size`的规定。
注意：当`buf`不是空时，必须是用`QRhiBuffer::StorageBuffer`创建的。
注意：`buf`可以是空的。创建未指定资源的`QRhiShaderResourceBindings`是有效的，但此类对象不能与`QRhiCommandBuffer::setShaderResources()`一起使用。不过，它适合创建管道。因此，这样的管道必须始终与另一个布局兼容的资源`QRhiShaderResourceBindings`一起使用，这些资源已传递给`QRhiCommandBuffer::setShaderResources()`。
注意：缓冲区加载/存储仅保证在计算流水线内可用。虽然部分后端支持在图形流水线中使用这些资源，但并非普遍支持，即使支持，也可能在障碍和同步方面出现意想不到的问题。因此，避免将此类资源与计算以外的着色器一起使用。

### `[static] QRhiShaderResourceBinding QRhiShaderResourceBinding::bufferLoadStore(int binding, QRhiShaderResourceBinding::StageFlags stage, QRhiBuffer *buf)`

**作用与语义：**

返回给定`binding`号和流水线`stage`的着色器资源绑定，用于读写存储缓冲区。
注意：当`buf`不是空时，必须是用`QRhiBuffer::StorageBuffer`创建的。
注意：`buf`可以是空的。创建未指定资源的`QRhiShaderResourceBindings`是有效的，但此类对象不能用于`QRhiCommandBuffer::setShaderResources()`。不过，它适合创建管道。这样的管道必须始终与另一个布局兼容的资源`QRhiShaderResourceBindings`一起使用，这些资源已传递给`QRhiCommandBuffer::setShaderResources()`。
注意：缓冲区加载/存储仅保证在计算流水线内可用。虽然部分后端支持在图形流水线中使用这些资源，但并非普遍支持，即使支持，也可能在障碍和同步方面出现意想不到的问题。因此，避免将此类资源与计算以外的着色器一起使用。

### `[static] QRhiShaderResourceBinding QRhiShaderResourceBinding::bufferLoadStore(int binding, QRhiShaderResourceBinding::StageFlags stage, QRhiBuffer *buf, quint32 offset, quint32 size)`

**作用与语义：**

返回给定`binding`号和流水线`stage`的着色器资源绑定，用于读写存储缓冲区。该超载仅绑定区域，按照`offset`和`size`的规定。
注意：当`buf`不是空的，必须是用`QRhiBuffer::StorageBuffer`创建的。
注意：`buf`可以是空的。创建未指定资源的`QRhiShaderResourceBindings`是有效的，但此类对象不能与`QRhiCommandBuffer::setShaderResources()`一起使用。但它适合创建管道。这样的管道必须始终与另一个布局兼容的资源`QRhiShaderResourceBindings`一起使用，这些资源传递给`QRhiCommandBuffer::setShaderResources()`。
注意：缓冲区加载/存储仅保证在计算流水线内可用。虽然部分后端支持在图形流水线中使用这些资源，但并非普遍支持，即使支持，也可能在障碍和同步方面出现意想不到的问题。因此，避免将此类资源与计算以外的着色器一起使用。

### `[static] QRhiShaderResourceBinding QRhiShaderResourceBinding::bufferStore(int binding, QRhiShaderResourceBinding::StageFlags stage, QRhiBuffer *buf)`

**作用与语义：**

返回只写存储缓冲区的着色器资源绑定，包含给定的`binding`号和流水线`stage`。
注意：当`buf`不是空时，必须是用`QRhiBuffer::StorageBuffer`创建的。
注意：`buf`可以为空。创建未指定资源的`QRhiShaderResourceBindings`是有效的，但此类对象不能用于`QRhiCommandBuffer::setShaderResources()`。不过，它适合创建管道。这样的管道必须始终与另一个布局兼容的资源`QRhiShaderResourceBindings`一起使用，这些资源传递给`QRhiCommandBuffer::setShaderResources()`。
注意：缓冲区加载/存储仅保证在计算流水线内可用。虽然部分后端支持在图形流水线中使用这些资源，但并非普遍支持，即使支持，也可能在障碍和同步方面出现意想不到的问题。因此，避免将此类资源与计算以外的着色器一起使用。

### `[static] QRhiShaderResourceBinding QRhiShaderResourceBinding::bufferStore(int binding, QRhiShaderResourceBinding::StageFlags stage, QRhiBuffer *buf, quint32 offset, quint32 size)`

**作用与语义：**

返回只写存储缓冲区的着色器资源绑定，具有给定的`binding`号和流水线`stage`。该重载仅绑定一个区域，按照`offset`和`size`的规定。
注意：当`buf`不是空时，必须是用 `QRhiBuffer::StorageBuffer` 创建的。
注意：`buf`可以为空。创建未指定资源的`QRhiShaderResourceBindings`是有效的，但此类对象不能与`QRhiCommandBuffer::setShaderResources()`一起使用。不过，它适合创建管道。因此，这样的管道必须始终与另一个布局兼容的资源`QRhiShaderResourceBindings`一起使用，这些已传递给`QRhiCommandBuffer::setShaderResources()`。
注意：缓冲区加载/存储仅保证在计算流水线内可用。虽然部分后端支持在图形流水线中使用这些资源，但并非普遍支持，即使支持，也可能在障碍和同步方面出现意想不到的问题。因此，避免将此类资源与计算以外的着色器一起使用。

### `[static] QRhiShaderResourceBinding QRhiShaderResourceBinding::imageLoad(int binding, QRhiShaderResourceBinding::StageFlags stage, QRhiTexture *tex, int level)`

**作用与语义：**

返回只读存储图像的着色器资源绑定，具有给定的`binding`号和流水线`stage`。图像加载操作将访问指定`level`的所有层。（因此，如果纹理是立方体贴图，着色器必须使用imageCube而非image2D）。
注意：当`tex`不是空时，必须是用`QRhiTexture::UsedWithLoadStore`创建的。
注意：`tex`可以是空的。创建未指定资源的`QRhiShaderResourceBindings`是有效的，但此类对象不能与`QRhiCommandBuffer::setShaderResources()`一起使用。不过，它适合创建管道。这样的管道必须始终与另一个布局兼容的资源`QRhiShaderResourceBindings`一起使用，这些资源传递给`QRhiCommandBuffer::setShaderResources()`。
注意：图像加载/存储仅在计算和片段阶段可用。

### `[static] QRhiShaderResourceBinding QRhiShaderResourceBinding::imageLoadStore(int binding, QRhiShaderResourceBinding::StageFlags stage, QRhiTexture *tex, int level)`

**作用与语义：**

返回给定`binding`号和流水线`stage`的读写存储图像的着色器资源绑定。图像加载/存储操作将访问指定`level`的所有层。（因此，如果纹理是立方体贴图，着色器必须使用imageCube而非image2D）。
注意：当`tex`不是空的，必须是用`QRhiTexture::UsedWithLoadStore`创建的。
注意：`tex`可以是空的。创建未指定资源的`QRhiShaderResourceBindings`是有效的，但此类对象不能用于`QRhiCommandBuffer::setShaderResources()`。不过，它适合创建管道。这样的管道必须始终与另一个布局兼容的资源`QRhiShaderResourceBindings`一起使用，这些资源传递给`QRhiCommandBuffer::setShaderResources()`。
注意：图像加载/存储仅在计算和片段阶段可用。

### `[static] QRhiShaderResourceBinding QRhiShaderResourceBinding::imageStore(int binding, QRhiShaderResourceBinding::StageFlags stage, QRhiTexture *tex, int level)`

**作用与语义：**

返回只写存储图像的着色器资源绑定，具有给定的`binding`号和流水线`stage`。图像存储操作将访问指定`level`的所有层。（因此，如果纹理是立方体映射，着色器必须使用imageCube而非image2D）。
注意：当`tex`不是无效时，必须是用`QRhiTexture::UsedWithLoadStore`创建的。
注意：`tex`可以是空的。创建未指定资源的`QRhiShaderResourceBindings`是有效的，但此类对象不能用于`QRhiCommandBuffer::setShaderResources()`。不过，它适合创建管道。这样的管道必须始终与另一个布局兼容的资源`QRhiShaderResourceBindings`同时使用，这些资源已传递给`QRhiCommandBuffer::setShaderResources()`。
注意：图像加载/存储仅在计算和片段阶段可用。

### `bool QRhiShaderResourceBinding::isLayoutCompatible(const QRhiShaderResourceBinding &other) const`

**作用与语义：**

如果布局与`other`兼容，返回`true`。布局不包含实际资源（如缓冲区或纹理）及相关参数（如偏移量或大小）。
例如，下面的`a`和`b`不相等，但在布局上是兼容的：

**官方示例：**

```cpp
 auto a = QRhiShaderResourceBinding::uniformBuffer(0, QRhiShaderResourceBinding::VertexStage, buffer);
 auto b = QRhiShaderResourceBinding::uniformBuffer(0, QRhiShaderResourceBinding::VertexStage, someOtherBuffer, 256);
```

### `[static] QRhiShaderResourceBinding QRhiShaderResourceBinding::sampledTexture(int binding, QRhiShaderResourceBinding::StageFlags stage, QRhiTexture *tex, QRhiSampler *sampler)`

**作用与语义：**

返回给定的绑定编号、流水线阶段、纹理和采样器（由`binding`、`stage`、`tex`、`sampler` 指定）的着色器资源绑定。
注意：该函数等价于调用`sampledTextures()`，`count`为1。
注意：`tex` 和 `sampler` 可以为空。创建未指定资源的 `QRhiShaderResourceBindings` 是有效的，但此类对象不能用于 `QRhiCommandBuffer::setShaderResources()`。不过，它适合创建管道。这样的管道必须始终与另一个布局兼容的资源`QRhiShaderResourceBindings`一起使用，这些资源传递给`QRhiCommandBuffer::setShaderResources()`。
注意：着色器可能不能消耗超过16个纹理/采样器，具体取决于底层图形API。在渲染器设计中必须牢记这一硬性限制。这不适用于只占用单一绑定点（着色器寄存器）且可能包含256-2048个纹理的纹理数组，具体取决于底层图形API。纹理数组（见`sampledTextures()`）在这方面与使用相同数量的单个纹理没有区别。

### `[static] QRhiShaderResourceBinding QRhiShaderResourceBinding::sampledTextures(int binding, QRhiShaderResourceBinding::StageFlags stage, int count, const QRhiShaderResourceBinding::TextureAndSampler *texSamplers)`

**作用与语义：**

返回给定绑定编号、流水线阶段以及由`binding`、`stage`、`count`和`texSamplers`指定的纹理采样器对数组的着色器资源绑定。
注意：`count`必须至少为1，且不得大于16。
注意：当`count`为1时，该函数等价于`sampledTexture()`。
当涉及组合图像采样器数组时，该函数尤为重要。例如，在GLSL中`layout(binding = 5) uniform sampler2D shadowMaps[8];`声明一个组合图像采样器的数组。应用程序随后需要为绑定点5提供一个`QRhiShaderResourceBinding`，通过调用该函数，`count`设为8，并为数组中的每个元素提供有效的纹理和采样器来设置。
警告：数组的所有元素都必须指定。上述示例中，唯一有效且可移植的方法是调用该函数，`count`为8。此外，所有`QRhiTexture`和`QRhiSampler`实例都必须有效，这意味着nullptr不被接受。这是因为一些底层API，如Vulkan，要求描述符数组中的每个元素都有一个有效的图像和采样器对象。如果某些数组元素不相关（因为着色器无法访问），建议应用程序提供“虚拟”采样器和纹理。
注意：`texSamplers`可以为空。创建未指定资源的`QRhiShaderResourceBindings`是有效的，但此类对象不能用于`QRhiCommandBuffer::setShaderResources()`。不过，它适合创建管道。这样的管道必须始终与另一个布局兼容的资源`QRhiShaderResourceBindings`一起使用，这些资源传递给`QRhiCommandBuffer::setShaderResources()`。

### `[static] QRhiShaderResourceBinding QRhiShaderResourceBinding::sampler(int binding, QRhiShaderResourceBinding::StageFlags stage, QRhiSampler *sampler)`

**作用与语义：**

返回给定绑定号、流水线阶段和采样器（由`binding`、`stage`、`sampler`指定的着色器资源绑定。
注意：`sampler`可以为空。创建未指定资源的`QRhiShaderResourceBindings`是有效的，但此类对象不能与`QRhiCommandBuffer::setShaderResources()`一起使用。不过，它适合创建管道。因此，这样的管道必须始终与另一个布局兼容的资源`QRhiShaderResourceBindings`与传`QRhiCommandBuffer::setShaderResources()`一起使用。
不支持多个独立采样器的数组。
这为独立的采样器对象创建了绑定，而`sampledTexture()`则适合组合图像采样器。在兼容Vulkan的GLSL代码中，单独的采样器被声明为`sampler`，而不是`sampler2D`：`layout(binding = 2) uniform sampler samp;`。
既有`texture2D`和`sampler`，就可以一起使用来采样质感：`fragColor = texture(sampler2D(tex, samp), texcoord);`。
注意：着色器可能无法消耗超过16个采样器，具体取决于底层图形API。在渲染器设计中必须牢记这一硬性限制。

### `[static] QRhiShaderResourceBinding QRhiShaderResourceBinding::texture(int binding, QRhiShaderResourceBinding::StageFlags stage, QRhiTexture *tex)`

**作用与语义：**

返回给定的绑定编号、流水线阶段和纹理的着色器资源绑定，这些绑定由`binding`、`stage`、`tex` 规定。
注意：该函数等价于调用`count`为1的`textures()`。
注意：`tex`可以是空的。创建未指定资源的`QRhiShaderResourceBindings`是有效的，但此类对象不能用于`QRhiCommandBuffer::setShaderResources()`。不过，它适合创建管道。这样的管道必须始终与另一个布局兼容的资源`QRhiShaderResourceBindings`一起使用，这些资源传递给`QRhiCommandBuffer::setShaderResources()`。
这为独立的纹理（图像）对象创建绑定，而`sampledTexture()`适合组合图像采样器。在兼容Vulkan的GLSL代码中，单独纹理声明为`texture2D`，而不是`sampler2D`：`layout(binding = 1) uniform texture2D tex;`。
注意：着色器可能无法消耗超过16个纹理，具体取决于底层图形API。在渲染器设计中必须牢记这一硬性限制。这不适用于那些只消耗单一绑定点（着色器寄存器）且可能包含256-2048个纹理的纹理数组，具体取决于底层图形API。纹理数组（见`sampledTextures()`）在这方面与使用相同数量的单个纹理没有区别。

### `[static] QRhiShaderResourceBinding QRhiShaderResourceBinding::textures(int binding, QRhiShaderResourceBinding::StageFlags stage, int count, QRhiTexture **tex)`

**作用与语义：**

返回给定绑定号、流水线阶段以及由`binding`、`stage`、`count`和`tex`指定（独立）纹理数组的着色器资源绑定。
注意：`count`必须至少为1，且不得大于16。
注意：当`count`为1时，该函数等价于`texture()`。
警告：阵列中的所有元素必须指定。
注意：`tex`可以为空。创建未指定资源的`QRhiShaderResourceBindings`是有效的，但此类对象不能用于`QRhiCommandBuffer::setShaderResources()`。不过，它适合创建管道。因此，这样的管道必须始终与另一个布局兼容的资源`QRhiShaderResourceBindings`一起使用，这些资源传递给`QRhiCommandBuffer::setShaderResources()`。

### `[static] QRhiShaderResourceBinding QRhiShaderResourceBinding::uniformBuffer(int binding, QRhiShaderResourceBinding::StageFlags stage, QRhiBuffer *buf)`

**作用与语义：**

返回给定绑定号、流水线阶段和缓冲区的着色器资源绑定，这些绑定点由`binding`、`stage`和`buf`指定的。
注意：当`buf`不是空的，必须是用`QRhiBuffer::UniformBuffer`创建的。
注意：`buf`可以是空的。创建未指定资源的`QRhiShaderResourceBindings`是有效的，但此类对象不能用于`QRhiCommandBuffer::setShaderResources()`。不过，它适合创建管道。这样的管道必须始终与另一个布局兼容的资源`QRhiShaderResourceBindings`一起使用，这些资源传递给`QRhiCommandBuffer::setShaderResources()`。
注意：如果`buf`大小超过`QRhi::MaxUniformBufferRange`报告的限制，可能会出现意外错误。

### `[static] QRhiShaderResourceBinding QRhiShaderResourceBinding::uniformBuffer(int binding, QRhiShaderResourceBinding::StageFlags stage, QRhiBuffer *buf, quint32 offset, quint32 size)`

**作用与语义：**

返回给定绑定号、流水线阶段和缓冲区的着色器资源绑定，由`binding`、`stage`和`buf`指定的。该超载仅绑定`offset`和`size`指定区域。
注意：用户需确保偏移量对齐于`QRhi::ubufAlignment()`。
注意：`size`必须大于0。
注意：当`buf`不是空时，必须用`QRhiBuffer::UniformBuffer`创建。
注意：`buf`可以为空。创建未指定资源的`QRhiShaderResourceBindings`是有效的，但此类对象不能用于`QRhiCommandBuffer::setShaderResources()`。不过，它适合创建管道。这样的管道必须始终与另一个布局兼容的资源`QRhiShaderResourceBindings`同时使用，这些资源传递给`QRhiCommandBuffer::setShaderResources()`。
注意：如果`size`超过`QRhi::MaxUniformBufferRange`报告的限制，可能会发生意外错误。

### `[static] QRhiShaderResourceBinding QRhiShaderResourceBinding::uniformBufferWithDynamicOffset(int binding, QRhiShaderResourceBinding::StageFlags stage, QRhiBuffer *buf, quint32 size)`

**作用与语义：**

返回给定的绑定编号、流水线阶段和由`binding`、`stage`和`buf`指定缓冲区的着色器资源绑定。假设均匀缓冲区具有动态偏移。动态偏移可以在`QRhiCommandBuffer::setShaderResources()`中指定，从而允许使用不同的偏移值而无需为缓冲区创建新的绑定。绑定区域的大小由`size`指定。与非动态偏移一样，`offset + size`不能超过`buf`的大小。
注意：当`buf`不是无效时，必须是用`QRhiBuffer::UniformBuffer`创建的。
注意：`buf`可以是空的。创建未指定资源的`QRhiShaderResourceBindings`是有效的，但此类对象不能与`QRhiCommandBuffer::setShaderResources()`一起使用。不过，它适合创建管道。这样的管道必须始终与另一个布局兼容的资源`QRhiShaderResourceBindings`一起使用，这些资源传递给`QRhiCommandBuffer::setShaderResources()`。
注意：如果`size`超过`QRhi::MaxUniformBufferRange`报告的限制，可能会发生意外错误。

### `[noexcept] size_t qHash(const QRhiShaderResourceBinding &key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `[noexcept] bool operator!=(const QRhiShaderResourceBinding &a, const QRhiShaderResourceBinding &b)`

**作用与语义：**

如果两个 `QRhiShaderResourceBinding` 对象 `a` 和 `b` 中的所有绑定都相等，则返回 `false`；否则返回 `true`。

### `[noexcept] bool operator==(const QRhiShaderResourceBinding &a, const QRhiShaderResourceBinding &b)`

**作用与语义：**

如果两个`QRhiShaderResourceBinding`对象的内容相等，`a`和`b`的内容相等，返回`true`。这包括资源（缓冲区、纹理）和相关参数（偏移量、大小）。仅比较布局（绑定点、流水线阶段、资源类型）时，请使用`isLayoutCompatible()`。

### `enum StageFlag { VertexStage, TessellationControlStage, TessellationEvaluationStage, FragmentStage, ComputeStage, GeometryStage }`

**作用与语义：**

标志值用于指示着色器资源在哪些阶段中可见。
- `QRhiShaderResourceBinding::VertexStage`：`1 << 0`;顶点阶段
- `QRhiShaderResourceBinding::TessellationControlStage`：`1 << 1`;镶嵌控制（船体着色器）阶段
- `QRhiShaderResourceBinding::TessellationEvaluationStage`：`1 << 2`;镶嵌评估（领域着色器）阶段
- `QRhiShaderResourceBinding::FragmentStage`：`1 << 4`;片段（像素着色器）阶段
- `QRhiShaderResourceBinding::ComputeStage`：`1 << 5`;计算阶段
- `QRhiShaderResourceBinding::GeometryStage`：`1 << 3`;几何阶段
StageFlags 类型是 QFlags 的 typedef<StageFlag>。它存储 StageFlag 值的 OR 组合。

### `flags StageFlags`

**作用与语义：**

标志值用于指示着色器资源在哪些阶段中可见。
- `QRhiShaderResourceBinding::VertexStage`：`1 << 0`;顶点阶段
- `QRhiShaderResourceBinding::TessellationControlStage`：`1 << 1`;镶嵌控制（船体着色器）阶段
- `QRhiShaderResourceBinding::TessellationEvaluationStage`：`1 << 2`;镶嵌评估（领域着色器）阶段
- `QRhiShaderResourceBinding::FragmentStage`：`1 << 4`;片段（像素着色器）阶段
- `QRhiShaderResourceBinding::ComputeStage`：`1 << 5`;计算阶段
- `QRhiShaderResourceBinding::GeometryStage`：`1 << 3`;几何阶段
StageFlags 类型是 QFlags 的 typedef<StageFlag>。它存储 StageFlag 值的 OR 组合。

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
