# QRhiTexture

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QRhiTexture` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

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

- `struct NativeTexture`
- `(since 6.8) struct ViewFormat`
- `enum Flag { RenderTarget, CubeMap, MipMapped, sRGB, UsedAsTransferSource, …, UsedAsShadingRateMap }`
- `flags Flags`
- `enum Format { UnknownFormat, RGBA8, BGRA8, R8, RG8, …, RGBA32SI }`

### 公有函数

- `int arrayRangeLength() const`
- `int arrayRangeStart() const`
- `int arraySize() const`
- `virtual bool create() = 0`
- `virtual bool createFrom(QRhiTexture::NativeTexture src)`
- `int depth() const`
- `QRhiTexture::Flags flags() const`
- `QRhiTexture::Format format() const`
- `virtual QRhiTexture::NativeTexture nativeTexture()`
- `QSize pixelSize() const`
- `(since 6.8) QRhiTexture::ViewFormat readViewFormat() const`
- `int sampleCount() const`
- `void setArrayRange(int startIndex, int count)`
- `void setArraySize(int arraySize)`
- `void setDepth(int depth)`
- `void setFlags(QRhiTexture::Flags f)`
- `void setFormat(QRhiTexture::Format fmt)`
- `virtual void setNativeLayout(int layout)`
- `void setPixelSize(const QSize &sz)`
- `(since 6.8) void setReadViewFormat(const QRhiTexture::ViewFormat &fmt)`
- `void setSampleCount(int s)`
- `(since 6.8) void setWriteViewFormat(const QRhiTexture::ViewFormat &fmt)`
- `(since 6.8) QRhiTexture::ViewFormat writeViewFormat() const`

### 重实现的公有函数

- `virtual QRhiResource::Type resourceType() const override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QRhiTexture::Flagflags QRhiTexture::Flags`

**作用与语义：**

用标志值来指定纹理的使用方式。如果不尊重`create()`之前设置的标志，并且试图以未事先声明的方式使用纹理，可能会导致不确定的行为或性能下降，具体取决于后端和底层图形API。
- `QRhiTexture::RenderTarget`：`1 << 0`;纹理将与`QRhiTextureRenderTarget`结合使用。
- `QRhiTexture::CubeMap`：`1 << 2`;纹理是立方体贴图。此类纹理有6个层，每个面分别为X、-X、Y、-Y、-Y、Z、-Z。Cubemap纹理不能多重采样。
- `QRhiTexture::MipMapped`：`1 << 3`;纹理具有多重映射。相应的多重输出计数自动计算，也可以通过`QRhi::mipLevelsForSize()`检索。多重采样的纹理图像必须在通过`QRhiResourceUpdateBatch::generateMips()`上传或生成的纹理中提供。多采样纹理不能有多重映射。
- `QRhiTexture::sRGB`：`1 << 4`;使用sRGB格式。
- `QRhiTexture::UsedAsTransferSource`：`1 << 5`;纹理作为纹理复制或读回的源，即纹理作为`QRhiResourceUpdateBatch::copyTexture()`或`QRhiResourceUpdateBatch::readBackTexture()`的来源。
- `QRhiTexture::UsedWithGenerateMips`：`1 << 6`;纹理将与`QRhiResourceUpdateBatch::generateMips()`一起使用。
- `QRhiTexture::UsedWithLoadStore`：`1 << 7`;纹理将用于图像加载/存储操作，例如计算着色器中。
- `QRhiTexture::UsedAsCompressedAtlas`：`1 << 8`;纹理采用压缩格式，子资源上传的尺寸可能与纹理大小不匹配。
- `QRhiTexture::ExternalOES`：`1 << 9`;纹理应使用GL_TEXTURE_EXTERNAL_OES目标和OpenGL。该标志在其他图形API中被忽略。
- `QRhiTexture::ThreeDimensional`：`1 << 10`;纹理是3D纹理。此类纹理应在`QRhi::newTexture()`重载时，除宽度和高度外，还取深度。3D纹理可以有mipmap，但不能是多重采样。在渲染或上传数据到3D纹理时，渲染目标的颜色附件或上传描述中指定的`layer`指的是范围内[0..depth-1]中的单个切片。底层图形API在运行时可能不支持3D纹理。支持通过`QRhi::ThreeDimensionalTextures`功能表示。
- `QRhiTexture::TextureRectangleGL`：`1 << 11`;纹理应在OpenGL中使用GL_TEXTURE_RECTANGLE目标。该标志在其他图形API中被忽略。与ExternalOES类似，该标志在处理平台API时非常有用，因为平台API中原生的OpenGL纹理对象被封装成`QRhiTexture`，且平台只能为非二维纹理目标提供纹理。
- `QRhiTexture::TextureArray`：`1 << 12`;纹理是一个纹理数组，即单个纹理对象，是同质的2D纹理数组。纹理数组是用`QRhi::newTextureArray()`创建的。底层图形API在运行时可能不支持纹理数组对象。支持由`QRhi::TextureArrays`功能表示。在渲染或上传数据到纹理数组时，渲染目标的颜色附件或上传描述中指定的`layer`会选择数组中的单个元素。
- `QRhiTexture::OneDimensional`：`1 << 13`;纹理是一维纹理。这类纹理可以通过将高度和深度分别传递给`QRhi::newTexture()`来创建。请注意，根据底层图形API的不同，一维纹理可能存在限制。例如，渲染到它们或使用基于mipmap滤波的滤波可能不被支持。这由`QRhi::OneDimensionalTextures`和 `QRhi::OneDimensionalTextureMipmaps`特征标志表示。
- `QRhiTexture::UsedAsShadingRateMap`：`1 << 14`
Flags 类型是 QFlags 的 typedef<Flag>。它存储 Flag 值的 OR 组合。

### `enum QRhiTexture::Format`

**作用与语义：**

指定纹理格式。另见`QRhi::isTextureFormatSupported()`，注意`QRhiTexture::sRGB`设置后`flags()`可以修改格式。
- `QRhiTexture::UnknownFormat`：`0`;不是一个有效的格式。此格式无法传递给`setFormat()`。
- `QRhiTexture::RGBA8`：`1`;四个分量，每个分量为无符号归一化8位。始终支持。（总共32位）
- `QRhiTexture::BGRA8`：`2`;四个组件，每个组件为无符号归一化的8位。（总共32位）
- `QRhiTexture::R8`：`3`;一个分量，无符号归一化的8位。（共8位）
- `QRhiTexture::RG8`：`4`;两个分量，无符号归一化的8位。（共16位）
- `QRhiTexture::R16`：`5`;一个分量，无符号归一化，16位。（共16位）
- `QRhiTexture::RG16`：`6`;两个分量，无符号归一化的16位。（总共32位）
- `QRhiTexture::RED_OR_ALPHA8`：`7`;要么与R8相同，要么是类似格式，但组件被混合为alpha，具体取决于`RedOrAlpha8IsRed`。（共8位）
- `QRhiTexture::RGBA16F`：`8`;四个组件，16位浮点。（总共64位）
- `QRhiTexture::RGBA32F`：`9`;四个组件，32位浮点数。（总共128位）
- `QRhiTexture::R16F`：`10`;一个分量，16位浮点点数。（总共16位）
- `QRhiTexture::R32F`：`11`;一个分量，32位浮点数。（总共32位）
- `QRhiTexture::RGB10A2`：`12`;四个分量，无符号归一化的10位R、G和B，2位alpha。这是一个打包格式，因此适用本地元序。注意没有BGR10A2。这是因为RGB10A2通过D3D映射到DXGI_FORMAT_R10G10B10A2_UNORM，MTLPixelFormatRGB10A2Unorm通过Metal映射到VK_FORMAT_A2B10G10R10_UNORM_PACK32，在OpenGL（ES）上映射GL_RGB10_A2/GL_RGB/GL_UNSIGNED_INT_2_10_10_10_REV。这是唯一普遍支持的RGB30选项。对应的`QImage`格式是`QImage::Format_BGR30`和`QImage::Format_A2BGR30_Premultiplied`。（总共32位）
- `QRhiTexture::D16`：`21`;16位深度（归一化无符号整数）
- `QRhiTexture::D24`：`22`;24位深度（归一化无符号整数）
- `QRhiTexture::D24S8`：`23`;24位深度（归一化无符号整数），8位模板
- `QRhiTexture::D32F`：`24`;32位深度（32位浮點）
- 4 `QRhiTexture::D32FS8 (since Qt 6.9)`：`25`;32位深度（32位浮点），8位模板，24位未使用（总共64位）
- `QRhiTexture::BC1`：`26`
- `QRhiTexture::BC2`：`27`
- `QRhiTexture::BC3`：`28`
- `QRhiTexture::BC4`：`29`
- `QRhiTexture::BC5`：`30`
- `QRhiTexture::BC6H`：`31`
- `QRhiTexture::BC7`：`32`
- `QRhiTexture::ETC2_RGB8`：`33`
- `QRhiTexture::ETC2_RGB8A1`：`34`
- `QRhiTexture::ETC2_RGBA8`：`35`
- `QRhiTexture::ASTC_4x4`：`36`
- `QRhiTexture::ASTC_5x4`：`37`
- `QRhiTexture::ASTC_5x5`：`38`
- `QRhiTexture::ASTC_6x5`：`39`
- `QRhiTexture::ASTC_6x6`：`40`
- `QRhiTexture::ASTC_8x5`：`41`
- `QRhiTexture::ASTC_8x6`：`42`
- `QRhiTexture::ASTC_8x8`：`43`
- `QRhiTexture::ASTC_10x5`：`44`
- `QRhiTexture::ASTC_10x6`：`45`
- `QRhiTexture::ASTC_10x8`：`46`
- `QRhiTexture::ASTC_10x10`：`47`
- `QRhiTexture::ASTC_12x10`：`48`
- `QRhiTexture::ASTC_12x12`：`49`
- `QRhiTexture::R8UI (since Qt 6.9)`：`17`;一个分量，无符号的8位。（共8位）
- `QRhiTexture::R32UI (since Qt 6.9)`：`18`;一个分量，无符号的32位。（总共32位）
- `QRhiTexture::RG32UI (since Qt 6.9)`：`19`;两个组件，无符号的32位。（共64位）
- `QRhiTexture::RGBA32UI (since Qt 6.9)`：`20`;四个组件，无符号32位。（总共128位）
- `QRhiTexture::R8SI (since Qt 6.10)`：`13`;一个分量，带符号的8位。（总共8位）
- `QRhiTexture::R32SI (since Qt 6.10)`：`14`;一个分量，带符号的32位。（总共32位）
- `QRhiTexture::RG32SI (since Qt 6.10)`：`15`;两个分量，带符号32位。（总共64位）
- `QRhiTexture::RGBA32SI (since Qt 6.10)`：`16`;四个分量，带符号32位。（总共128位）

### `int QRhiTexture::arrayRangeLength() const`

**作用与语义：**

调用`setArrayRange()`时返回暴露的数组范围大小。

### `int QRhiTexture::arrayRangeStart() const`

**作用与语义：**

调用`setArrayRange()`时返回第一个数组层。

### `int QRhiTexture::arraySize() const`

**作用与语义：**

返回纹理数组大小。

### `[pure virtual] bool QRhiTexture::create()`

**作用与语义：**

创建对应的本地图形资源。如果由于之前的 create() 存在资源且没有相应的`destroy()`，则 `destroy()` 会先隐式调用。
成功时返回`true`，`false`图形操作失败时返回。无论返回值如何，调用`destroy()`始终安全。

### `[virtual] bool QRhiTexture::createFrom(QRhiTexture::NativeTexture src)`

**作用与语义：**

类似于`create()`，但不会创建新的原生纹理。取而代之的是使用`src`指定的原生纹理资源。
这允许从外部图形引擎导入现有的原生纹理对象（该材质必须属于同一设备或共享上下文，具体取决于图形 API）。
如果指定的本地贴图对象已成功封装为非拥有`QRhiTexture`，则返回为真。
注意：`format()`、`pixelSize()`、`sampleCount()`和`flags()`仍需正确设置。将错误的尺寸和其他值传递给`QRhi::newTexture()`，然后再用createFrom()，期望仅凭本地纹理对象推断这些值，是错误的，会导致问题。
注意：`QRhiTexture`不拥有纹理对象的所有权。`destroy()`不会释放该对象或任何关联内存。
与此操作相反，即将`QRhiTexture`创建的原生纹理对象暴露给外部引擎，可以通过`nativeTexture()`实现。
注意：在导入3D纹理、纹理数组对象，或OpenGL ES中的外部纹理时，特别重要的是通过`setFlags()`设置对应的标志（`ThreeDimensional`、`TextureArray`、`ExternalOES`），然后再调用该函数。

### `int QRhiTexture::depth() const`

**作用与语义：**

返回3D纹理的深度。

### `QRhiTexture::Flags QRhiTexture::flags() const`

**作用与语义：**

返回纹理标志。

### `QRhiTexture::Format QRhiTexture::format() const`

**作用与语义：**

返回纹理格式。

### `[virtual] QRhiTexture::NativeTexture QRhiTexture::nativeTexture()`

**作用与语义：**

返回该纹理的底层原生资源。如果后端不支持暴露底层原生资源，返回值将为空。

### `QSize QRhiTexture::pixelSize() const`

**作用与语义：**

返回像素大小。

### `[since 6.8] QRhiTexture::ViewFormat QRhiTexture::readViewFormat() const`

**作用与语义：**

返回采样纹理时使用的视图格式。未调用时，视角格式被假定为与`format()`相同。

### `[override virtual] QRhiResource::Type QRhiTexture::resourceType() const`

**作用与语义：**

重装：`QRhiResource::resourceType()` const.
返回资源类型。
返回资源类型。

### `int QRhiTexture::sampleCount() const`

**作用与语义：**

返回采样计数。1表示没有多采样抗锯齿。

### `void QRhiTexture::setArrayRange(int startIndex, int count)`

**作用与语义：**

通常所有数组层都被暴露，着色器通过采样 `sampler2DArray` 时传递给 `texture()` GLSL 函数的第三个坐标选择该层。当`QRhi::TextureArrayRange`被报告为支持时，在请求`create()`或`createFrom()`只选择指定范围前调用 setArrayRange()，`count`从`startIndex`开始的元素。着色器逻辑可以基于此进行编写。

### `void QRhiTexture::setArraySize(int arraySize)`

**作用与语义：**

定格质感的`arraySize`。

### `void QRhiTexture::setDepth(int depth)`

**作用与语义：**

设置3D纹理的`depth`。

### `void QRhiTexture::setFlags(QRhiTexture::Flags f)`

**作用与语义：**

把纹理标记设置为`f`。

### `void QRhiTexture::setFormat(QRhiTexture::Format fmt)`

**作用与语义：**

将请求的纹理格式设置为`fmt`。
注意：值集仅在下一次调用`create()`时考虑，即底层图形资源被（重新）创建时。否则设置新值是徒劳的，必须避免，因为可能导致状态不一致。

### `[virtual] void QRhiTexture::setNativeLayout(int layout)`

**作用与语义：**

对于某些图形API，如Vulkan，在图像布局中需要特别注意直接使用图形API的自定义渲染代码。此功能允许在本地渲染命令后传达`QRhiTexture`背后的图像预期`layout`。
例如，考虑直接用Vulkan渲染到`QRhiTexture`的VkImage，代码块被`QRhiCommandBuffer::beginExternal()`和`QRhiCommandBuffer::endExternal()`包围，然后在基于`QRhi`的渲染通道中使用该图像进行纹理采样。为避免图像布局可能出现错误的过渡，该函数可用于指示在该代码块中记录的命令完成后图像布局。
调用该函数只有在`QRhiCommandBuffer::endExternal()`后且后续`QRhiCommandBuffer::beginPass()`之前才有意义。
该函数对底层图形API不暴露图像布局概念的`QRhi`后端无效。
注意：在Vulkan中，`layout`是`VkImageLayout`。而在Direct 3D 12中，`layout`是由`D3D12_RESOURCE_STATES`比特组成的值。

### `void QRhiTexture::setPixelSize(const QSize &sz)`

**作用与语义：**

将纹理大小（以像素为单位）设置为`sz`。
注意：值集仅在下一次调用`create()`时考虑，即底层图形资源被重新创建时。否则设置新值是徒劳的，必须避免，因为可能导致状态不一致。其他设置器同样如此。

### `[since 6.8] void QRhiTexture::setReadViewFormat(const QRhiTexture::ViewFormat &fmt)`

**作用与语义：**

将着色器资源视图格式（或用于采样纹理的视图格式）设置为`fmt`。默认情况下，纹理本身使用相同的格式（以及sRGB特性），在大多数情况下无需调用该函数。
只有当 `QRhi::TextureViewFormat` 功能被报告为支持时，才会考虑该设置。
注意：此功能旨在实现非sRGB和sRGB之间的“投射”，以便着色器读取执行或不执行隐式sRGB转换。其他类型的投射可能有效，也可能无效。

### `void QRhiTexture::setSampleCount(int s)`

**作用与语义：**

将样本计数设置为`s`。

### `[since 6.8] void QRhiTexture::setWriteViewFormat(const QRhiTexture::ViewFormat &fmt)`

**作用与语义：**

将渲染目标视图格式设置为`fmt`。默认情况下，与纹理本身使用相同的格式（以及sRGB特性），大多数情况下无需调用该函数。
提供写视图格式的一个常见应用场景是处理外部提供的纹理，这些贴图在我们控制之外使用带有3D API的sRGB格式，如Vulkan或Direct 3D，但渲染引擎已准备好在着色流水线末端处理线性化和sRGB转换。在这种情况下，渲染成此类纹理时需要的是一个具有相同但非sRGB格式的渲染目标视图（例如VkImageView）。（例如，如果从 OpenXR 实现中得到一个VK_FORMAT_R8G8B8A8_SRGB纹理，渲染时可能需要使用 VK_FORMAT_R8G8B8A8_UNORM 视图，如果渲染引擎的流水线需要;在此示例中，调用该函数的 `ViewFormat` 格式为 `QRhiTexture::RGBA8`，`srgb` 设置为 `false`）。
只有当`QRhi::TextureViewFormat`功能被报告为支持时，才会考虑该设置。
注意：此功能旨在实现非sRGB和sRGB之间的“投射”，以便着色器写入不执行或执行隐式sRGB转换。其他类型的投射可能有效，也可能无效。

### `[since 6.8] QRhiTexture::ViewFormat QRhiTexture::writeViewFormat() const`

**作用与语义：**

返回写入纹理时及与图像加载/存储时使用的视图格式。未调用时，视图格式被假定为与`format()`相同。

### `struct NativeTexture`

**作用与语义：**

包含关于纹理底层原生资源的信息。

### `(since 6.8) struct ViewFormat`

**作用与语义：**

指定从纹理读取或写入的视图格式。
注意：这是一个具有有限兼容性保证的RHI API，详情请参见 `QRhi`。

### `enum Flag { RenderTarget, CubeMap, MipMapped, sRGB, UsedAsTransferSource, …, UsedAsShadingRateMap }`

**作用与语义：**

用标志值来指定纹理的使用方式。如果不尊重`create()`之前设置的标志，并且试图以未事先声明的方式使用纹理，可能会导致不确定的行为或性能下降，具体取决于后端和底层图形API。
- `QRhiTexture::RenderTarget`：`1 << 0`;纹理将与`QRhiTextureRenderTarget`结合使用。
- `QRhiTexture::CubeMap`：`1 << 2`;纹理是立方体贴图。此类纹理有6个层，每个面分别为X、-X、Y、-Y、-Y、Z、-Z。Cubemap纹理不能多重采样。
- `QRhiTexture::MipMapped`：`1 << 3`;纹理具有多重映射。相应的多重输出计数自动计算，也可以通过`QRhi::mipLevelsForSize()`检索。多重采样的纹理图像必须在通过`QRhiResourceUpdateBatch::generateMips()`上传或生成的纹理中提供。多采样纹理不能有多重映射。
- `QRhiTexture::sRGB`：`1 << 4`;使用sRGB格式。
- `QRhiTexture::UsedAsTransferSource`：`1 << 5`;纹理作为纹理复制或读回的源，即纹理作为`QRhiResourceUpdateBatch::copyTexture()`或`QRhiResourceUpdateBatch::readBackTexture()`的来源。
- `QRhiTexture::UsedWithGenerateMips`：`1 << 6`;纹理将与`QRhiResourceUpdateBatch::generateMips()`一起使用。
- `QRhiTexture::UsedWithLoadStore`：`1 << 7`;纹理将用于图像加载/存储操作，例如计算着色器中。
- `QRhiTexture::UsedAsCompressedAtlas`：`1 << 8`;纹理采用压缩格式，子资源上传的尺寸可能与纹理大小不匹配。
- `QRhiTexture::ExternalOES`：`1 << 9`;纹理应使用GL_TEXTURE_EXTERNAL_OES目标和OpenGL。该标志在其他图形API中被忽略。
- `QRhiTexture::ThreeDimensional`：`1 << 10`;纹理是3D纹理。此类纹理应在`QRhi::newTexture()`重载时，除宽度和高度外，还取深度。3D纹理可以有mipmap，但不能是多重采样。在渲染或上传数据到3D纹理时，渲染目标的颜色附件或上传描述中指定的`layer`指的是范围内[0..depth-1]中的单个切片。底层图形API在运行时可能不支持3D纹理。支持通过`QRhi::ThreeDimensionalTextures`功能表示。
- `QRhiTexture::TextureRectangleGL`：`1 << 11`;纹理应在OpenGL中使用GL_TEXTURE_RECTANGLE目标。该标志在其他图形API中被忽略。与ExternalOES类似，该标志在处理平台API时非常有用，因为平台API中原生的OpenGL纹理对象被封装成`QRhiTexture`，且平台只能为非二维纹理目标提供纹理。
- `QRhiTexture::TextureArray`：`1 << 12`;纹理是一个纹理数组，即单个纹理对象，是同质的2D纹理数组。纹理数组是用`QRhi::newTextureArray()`创建的。底层图形API在运行时可能不支持纹理数组对象。支持由`QRhi::TextureArrays`功能表示。在渲染或上传数据到纹理数组时，渲染目标的颜色附件或上传描述中指定的`layer`会选择数组中的单个元素。
- `QRhiTexture::OneDimensional`：`1 << 13`;纹理是一维纹理。这类纹理可以通过将高度和深度分别传递给`QRhi::newTexture()`来创建。请注意，根据底层图形API的不同，一维纹理可能存在限制。例如，渲染到它们或使用基于mipmap滤波的滤波可能不被支持。这由`QRhi::OneDimensionalTextures`和 `QRhi::OneDimensionalTextureMipmaps`特征标志表示。
- `QRhiTexture::UsedAsShadingRateMap`：`1 << 14`
Flags 类型是 QFlags 的 typedef<Flag>。它存储 Flag 值的 OR 组合。

### `flags Flags`

**作用与语义：**

用标志值来指定纹理的使用方式。如果不尊重`create()`之前设置的标志，并且试图以未事先声明的方式使用纹理，可能会导致不确定的行为或性能下降，具体取决于后端和底层图形API。
- `QRhiTexture::RenderTarget`：`1 << 0`;纹理将与`QRhiTextureRenderTarget`结合使用。
- `QRhiTexture::CubeMap`：`1 << 2`;纹理是立方体贴图。此类纹理有6个层，每个面分别为X、-X、Y、-Y、-Y、Z、-Z。Cubemap纹理不能多重采样。
- `QRhiTexture::MipMapped`：`1 << 3`;纹理具有多重映射。相应的多重输出计数自动计算，也可以通过`QRhi::mipLevelsForSize()`检索。多重采样的纹理图像必须在通过`QRhiResourceUpdateBatch::generateMips()`上传或生成的纹理中提供。多采样纹理不能有多重映射。
- `QRhiTexture::sRGB`：`1 << 4`;使用sRGB格式。
- `QRhiTexture::UsedAsTransferSource`：`1 << 5`;纹理作为纹理复制或读回的源，即纹理作为`QRhiResourceUpdateBatch::copyTexture()`或`QRhiResourceUpdateBatch::readBackTexture()`的来源。
- `QRhiTexture::UsedWithGenerateMips`：`1 << 6`;纹理将与`QRhiResourceUpdateBatch::generateMips()`一起使用。
- `QRhiTexture::UsedWithLoadStore`：`1 << 7`;纹理将用于图像加载/存储操作，例如计算着色器中。
- `QRhiTexture::UsedAsCompressedAtlas`：`1 << 8`;纹理采用压缩格式，子资源上传的尺寸可能与纹理大小不匹配。
- `QRhiTexture::ExternalOES`：`1 << 9`;纹理应使用GL_TEXTURE_EXTERNAL_OES目标和OpenGL。该标志在其他图形API中被忽略。
- `QRhiTexture::ThreeDimensional`：`1 << 10`;纹理是3D纹理。此类纹理应在`QRhi::newTexture()`重载时，除宽度和高度外，还取深度。3D纹理可以有mipmap，但不能是多重采样。在渲染或上传数据到3D纹理时，渲染目标的颜色附件或上传描述中指定的`layer`指的是范围内[0..depth-1]中的单个切片。底层图形API在运行时可能不支持3D纹理。支持通过`QRhi::ThreeDimensionalTextures`功能表示。
- `QRhiTexture::TextureRectangleGL`：`1 << 11`;纹理应在OpenGL中使用GL_TEXTURE_RECTANGLE目标。该标志在其他图形API中被忽略。与ExternalOES类似，该标志在处理平台API时非常有用，因为平台API中原生的OpenGL纹理对象被封装成`QRhiTexture`，且平台只能为非二维纹理目标提供纹理。
- `QRhiTexture::TextureArray`：`1 << 12`;纹理是一个纹理数组，即单个纹理对象，是同质的2D纹理数组。纹理数组是用`QRhi::newTextureArray()`创建的。底层图形API在运行时可能不支持纹理数组对象。支持由`QRhi::TextureArrays`功能表示。在渲染或上传数据到纹理数组时，渲染目标的颜色附件或上传描述中指定的`layer`会选择数组中的单个元素。
- `QRhiTexture::OneDimensional`：`1 << 13`;纹理是一维纹理。这类纹理可以通过将高度和深度分别传递给`QRhi::newTexture()`来创建。请注意，根据底层图形API的不同，一维纹理可能存在限制。例如，渲染到它们或使用基于mipmap滤波的滤波可能不被支持。这由`QRhi::OneDimensionalTextures`和 `QRhi::OneDimensionalTextureMipmaps`特征标志表示。
- `QRhiTexture::UsedAsShadingRateMap`：`1 << 14`
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

`QRhiTexture` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
