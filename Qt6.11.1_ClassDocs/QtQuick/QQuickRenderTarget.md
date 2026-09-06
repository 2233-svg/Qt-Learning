# QQuickRenderTarget

> Qt 6.11.1 · Qt Quick

## 1. 先建立直觉

**一句话定位：** `QQuickRenderTarget` 是 QML 属性绑定与场景图机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Quick 面向 QML/场景图界面，提供可视项、动画、输入和高性能界面基础设施。

### 这是什么

`QQuickRenderTarget` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QQuickRenderTarget>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Quick)
target_link_libraries(mytarget PRIVATE Qt6::Quick)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

### 状态、生命周期和线程

**生命周期：** QML 引擎、上下文和对象所有权必须明确。由 QML 创建的对象通常由引擎管理；通过 context property 或 C++ 暴露的对象要决定由 C++ 持有还是转移给 QML，不能让绑定指向悬空对象。

**状态与结果：** 属性绑定和直接赋值不是一回事：直接给被绑定属性赋值通常会打破原有绑定。C++ 属性要有正确的 notify signal，QML 才能在数据变化时更新；信号参数和属性当前值要保持一致。

**线程与事件循环：** 大多数 QML 对象和 GUI 操作在 GUI 线程，场景图渲染还可能在 render thread。不要在渲染阶段调用 GUI 对象 API；后台数据通过线程安全的信号/槽边界送入 QML。

## 3. 直接使用

需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。 使用时通常按这个过程组织：注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

```cpp
// C++ 侧暴露属性/信号后，在 QML 中建立绑定。
// 变化时发出 notify signal，避免在绑定表达式中直接修改状态。
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `(since 6.8) enum class Flag { MultisampleResolve }`
- `flags Flags`

### 公有函数

- `QQuickRenderTarget()`
- `~QQuickRenderTarget()`
- `(since 6.8) QRhiTexture * depthTexture() const`
- `(since 6.3) qreal devicePixelRatio() const`
- `bool isNull() const`
- `(since 6.4) bool mirrorVertically() const`
- `(since 6.8) void setDepthTexture(QRhiTexture *texture)`
- `(since 6.3) void setDevicePixelRatio(qreal ratio)`
- `(since 6.4) void setMirrorVertically(bool enable)`

### 静态公有成员

- `(since 6.4) QQuickRenderTarget fromD3D11Texture(void *texture, uint format, const QSize &pixelSize, int sampleCount = 1)`
- `QQuickRenderTarget fromD3D11Texture(void *texture, const QSize &pixelSize, int sampleCount = 1)`
- `(since 6.8) QQuickRenderTarget fromD3D11Texture(void *texture, uint format, QSize pixelSize, int sampleCount, QQuickRenderTarget::Flags flags)`
- `(since 6.6) QQuickRenderTarget fromD3D12Texture(void *texture, int resourceState, uint format, const QSize &pixelSize, int sampleCount = 1)`
- `(since 6.8) QQuickRenderTarget fromD3D12Texture(void *texture, int resourceState, uint format, uint viewFormat, QSize pixelSize, int sampleCount, int arraySize, QQuickRenderTarget::Flags flags)`
- `(since 6.4) QQuickRenderTarget fromMetalTexture(MTLTexture *texture, uint format, const QSize &pixelSize, int sampleCount = 1)`
- `QQuickRenderTarget fromMetalTexture(MTLTexture *texture, const QSize &pixelSize, int sampleCount = 1)`
- `(since 6.8) QQuickRenderTarget fromMetalTexture(MTLTexture *texture, uint format, uint viewFormat, QSize pixelSize, int sampleCount, int arraySize, QQuickRenderTarget::Flags flags)`
- `(since 6.2) QQuickRenderTarget fromOpenGLRenderBuffer(uint renderbufferId, const QSize &pixelSize, int sampleCount = 1)`
- `(since 6.4) QQuickRenderTarget fromOpenGLTexture(uint textureId, uint format, const QSize &pixelSize, int sampleCount = 1)`
- `QQuickRenderTarget fromOpenGLTexture(uint textureId, const QSize &pixelSize, int sampleCount = 1)`
- `(since 6.8) QQuickRenderTarget fromOpenGLTexture(uint textureId, uint format, QSize pixelSize, int sampleCount, int arraySize, QQuickRenderTarget::Flags flags)`
- `(since 6.4) QQuickRenderTarget fromPaintDevice(QPaintDevice *device)`
- `(since 6.6) QQuickRenderTarget fromRhiRenderTarget(QRhiRenderTarget *renderTarget)`
- `(since 6.4) QQuickRenderTarget fromVulkanImage(VkImage image, VkImageLayout layout, VkFormat format, const QSize &pixelSize, int sampleCount = 1)`
- `QQuickRenderTarget fromVulkanImage(VkImage image, VkImageLayout layout, const QSize &pixelSize, int sampleCount = 1)`
- `(since 6.8) QQuickRenderTarget fromVulkanImage(VkImage image, VkImageLayout layout, VkFormat format, VkFormat viewFormat, QSize pixelSize, int sampleCount, int arraySize, QQuickRenderTarget::Flags flags)`

### 相关非成员函数

- `bool operator!=(const QQuickRenderTarget &a, const QQuickRenderTarget &b)`
- `bool operator==(const QQuickRenderTarget &a, const QQuickRenderTarget &b)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[since 6.8] enum class QQuickRenderTarget::Flagflags QQuickRenderTarget::Flags`

**作用与语义：**

静态`QQuickRenderTarget`构造函数的标志。
- `QQuickRenderTarget::Flag::MultisampleResolve`：`0x01`;表示`sampleCount`参数不是所提供纹理的采样数（且纹理仍非多重采样纹理），而是多采样抗锯齿所需的采样。触发自动创建和管理中间多采样纹理（或纹理数组）作为颜色缓冲区，对应用程序透明。采样在渲染结束时自动解析为提供的纹理。当该标志未被设置且`sampleCount`参数大于1时，表示提供的纹理是多重采样的。当`sampleCount`为1时，该标志无效（表明不涉及多重采样）。
这个枚举是在Qt 6.8引入的。
Flags 类型是 QFlags 的 typedef<Flag>。它存储 Flag 值的 OR 组合。

### `QQuickRenderTarget::QQuickRenderTarget()`

**作用与语义：**

构建一个默认的QQuickRenderTarget，不引用任何本地对象。

### `[noexcept] QQuickRenderTarget::~QQuickRenderTarget()`

**作用与语义：**

毁灭者。

### `[since 6.8] QRhiTexture *QQuickRenderTarget::depthTexture() const`

**作用与语义：**

返回当前设置的深度纹理，或者在大多数情况下返回`nullptr`。
只有在调用`setDepthTexture()`时，该值才非空。

### `[since 6.3] qreal QQuickRenderTarget::devicePixelRatio() const`

**作用与语义：**

返回渲染目标的设备像素比。这是设备像素与设备无关像素之间的比值。
默认的设备像素比是1.0。

### `[static, since 6.4] QQuickRenderTarget QQuickRenderTarget::fromD3D11Texture(void *texture, uint format, const QSize &pixelSize, int sampleCount = 1)`

**作用与语义：**

返回一个新的 `QQuickRenderTarget`，该对象引用由 `texture` 指定的 D3D11 纹理对象。
`format` 指定纹理的 DXGI_FORMAT。只能使用 Qt 渲染基础设施支持的纹理格式。
`pixelSize` 指定图像的大小，以像素为单位。目前仅支持 2D 纹理。
`sampleCount` 指定采样数量。0 或 1 表示不多重采样，而像 4 或 8 这样的值表示原生对象是多重采样纹理。
该纹理用作 Qt Quick 场景图使用的渲染目标的第一个颜色附件。如适用，将自动创建并使用深度模板缓冲区。
注意：生成的 `QQuickRenderTarget` 不拥有任何原生资源，它仅包含引用以及相关的大小和采样数元数据。调用者有责任确保原生资源在必要时存在。

### `[static] QQuickRenderTarget QQuickRenderTarget::fromD3D11Texture(void *texture, const QSize &pixelSize, int sampleCount = 1)`

**作用与语义：**

返回一个新的 `QQuickRenderTarget`，该对象引用由 `texture` 指定的 D3D11 纹理对象。该纹理被假定为具有 DXGI_FORMAT_R8G8B8A8_UNORM 格式。
`pixelSize` 指定图像的大小，以像素为单位。目前仅支持 2D 纹理。
`sampleCount` 指定采样数量。0 或 1 表示不多重采样，而像 4 或 8 这样的值表示原生对象是多重采样纹理。
该纹理用作 Qt Quick 场景图使用的渲染目标的第一个颜色附件。如适用，将自动创建并使用深度模板缓冲区。
注意：生成的 `QQuickRenderTarget` 不拥有任何原生资源，它仅包含引用以及相关的大小和采样数元数据。调用者有责任确保原生资源在必要时存在。

### `[static, since 6.8] QQuickRenderTarget QQuickRenderTarget::fromD3D11Texture(void *texture, uint format, QSize pixelSize, int sampleCount, QQuickRenderTarget::Flags flags)`

**作用与语义：**

返回一个新的`QQuickRenderTarget`，引用由`texture`指定的D3D11纹理对象。
`format` 指定了纹理的 Tyty DXGI_FORMAT。只应使用 Qt 渲染基础设施支持的纹理格式。
`pixelSize` 表示图像的大小，单位为像素。目前仅支持 2D 纹理。
`sampleCount` 指定采样数量。0 或 1 表示不进行多重采样，而 4 或 8 表示原生对象为多采样纹理，除非`flags`包含 `MultisampleResolve`。此时，`texture` 被假定为非多采样的二维纹理，`sampleCount`定义所需的采样数量。最终的`QQuickRenderTarget`将使用中间自动生成的多采样纹理作为颜色附加，并将采样解析为`texture`。这是当原生纹理尚未多采样时，执行 MSAA 的推荐方法。
纹理作为 Qt Quick 场景图渲染目标的第一个颜色附加。如果适用，深度模板缓冲区会自动创建并使用。当颜色缓冲区为多重采样时，深度模板缓冲区也会自动为多重采样。
注意：生成的`QQuickRenderTarget`不拥有任何本地资源，仅包含引用及相关大小和样本数的元数据。调用者有责任确保本地资源在必要时间内持续存在。

### `[static, since 6.6] QQuickRenderTarget QQuickRenderTarget::fromD3D12Texture(void *texture, int resourceState, uint format, const QSize &pixelSize, int sampleCount = 1)`

**作用与语义：**

返回一个新的`QQuickRenderTarget`，引用由`texture`指定的D3D12纹理对象。
`resourceState`必须有一个有效的位掩码，位来自D3D12_RESOURCE_STATES，指定资源当前状态。
`format` 指定纹理的 DXGI_FORMAT 1。仅应使用 Qt 渲染基础设施支持的纹理格式。
`pixelSize` 指定图像的像素大小。目前仅支持 2D 纹理。
`sampleCount` 指定采样数量。0 或 1 表示不进行多重采样，而像 4 或 8 这样的值表示本地对象是多采样纹理。
纹理作为 Qt Quick 场景图渲染目标的第一个颜色附加。如适用，深度模板缓冲区会自动创建并使用。
注意：最终`QQuickRenderTarget`不拥有任何本地资源，仅包含引用及相关大小和样本数的元数据。调用者有责任确保本地资源持续存在直到必要。

### `[static, since 6.8] QQuickRenderTarget QQuickRenderTarget::fromD3D12Texture(void *texture, int resourceState, uint format, uint viewFormat, QSize pixelSize, int sampleCount, int arraySize, QQuickRenderTarget::Flags flags)`

**作用与语义：**

返回一个新的`QQuickRenderTarget`，引用由`texture`指定的D3D12二维纹理或二维纹理数组对象。
`resourceState`必须有一个有效的位掩码，包含D3D12_RESOURCE_STATES位，指定资源当前状态。
`format` 指定纹理的 DXGI_FORMAT。仅应使用 Qt 渲染基础设施支持的纹理格式。
`viewFormat` 是渲染目标视图（RTV）使用的DXGI_FORMAT。通常与 `format` 相同。只有在驱动支持宽松格式投射时才能正常工作，否则该参数会被忽略。实际上，预计 Windows 10 1703 及以后版本应始终支持。
`pixelSize` 指定图像的大小，单位为像素。目前仅支持 2D 纹理和 2D 纹理数组。
`sampleCount` 指定采样数量。0 或 1 表示不进行多重采样，而像 4 或 8 这样的值表示该对象是多采样纹理，除非 `flags` 包含 `MultisampleResolve`。此时，`texture` 被假定为非多采样的二维纹理或二维纹理数组，`sampleCount` 定义了所需的采样数。生成的 `QQuickRenderTarget` 会使用中间自动生成的多采样纹理（或纹理数组）作为颜色附加，并将采样解析为`texture`。这是当原生 D3D12 纹理尚未多采样时，执行 MSAA 的推荐方法。
数组元素（图层）的数量以`arraySize`表示。当大于1时，表示多视图渲染（视图实例化），这在VR/AR中尤为重要。`arraySize`是视图数量，通常为`2`。有关在Qt Quick场景图中启用多视图渲染的详细信息，请参见 `QSGMaterial::viewCount()`。
纹理作为 Qt Quick 场景图渲染目标的第一个颜色附加。如果适用，深度模板缓冲区会自动创建并使用。当颜色缓冲区为多采样时，深度模板缓冲区也会自动为多重采样。对于多视图渲染，深度模板纹理会自动组成与匹配`arraySize`的数组。
注意：最终`QQuickRenderTarget`不拥有任何本地资源，仅包含引用及相关大小和样本数的元数据。调用者有责任确保本地资源在必要时间内持续存在。

### `[static, since 6.4] QQuickRenderTarget QQuickRenderTarget::fromMetalTexture(MTLTexture *texture, uint format, const QSize &pixelSize, int sampleCount = 1)`

**作用与语义：**

返回一个新的`QQuickRenderTarget`，引用由`texture`指定的金属纹理对象。
`format` 指定了纹理的 MTLPixelFormat。仅应使用 Qt 渲染基础设施支持的纹理格式。
`pixelSize` 指定图像的大小，单位为像素。目前仅支持 2D 纹理。
`sampleCount` 指定采样数量。0 或 1 表示不进行多重采样，而 4 或 8 表示原生对象是多采样纹理。
纹理作为 Qt Quick 场景图渲染目标的第一个颜色附加。如适用，深度模板缓冲区会自动创建并使用。
注意：最终的`QQuickRenderTarget`不拥有任何原生资源，仅包含引用及相关大小和样本数的元数据。调用者有责任确保本地资源持续存在直到必要。

### `[static] QQuickRenderTarget QQuickRenderTarget::fromMetalTexture(MTLTexture *texture, const QSize &pixelSize, int sampleCount = 1)`

**作用与语义：**

返回一个新的 `QQuickRenderTarget`，它引用由 `texture` 指定的 Metal 纹理对象。该纹理假定格式为 MTLPixelFormatRGBA8Unorm。
`pixelSize` 指定图像的尺寸，以像素为单位。目前仅支持 2D 纹理。
`sampleCount` 指定样本数量。0 或 1 表示不进行多重采样，而像 4 或 8 这样的值表示原生对象是多重采样纹理。
该纹理被用作 Qt Quick 场景图使用的渲染目标的第一个颜色附件。深度模板缓冲区（如适用）会被自动创建和使用。
注意：生成的 `QQuickRenderTarget` 不拥有任何原生资源，它仅包含引用及尺寸和样本数量的相关元数据。调用者有责任确保原生资源在必要的时间内存在。

### `[static, since 6.8] QQuickRenderTarget QQuickRenderTarget::fromMetalTexture(MTLTexture *texture, uint format, uint viewFormat, QSize pixelSize, int sampleCount, int arraySize, QQuickRenderTarget::Flags flags)`

**作用与语义：**

返回一个新的`QQuickRenderTarget`，引用`texture`中给出的金属二维纹理或二维纹理数组。
`format`指定了纹理的MTLPixel格式。仅应使用Qt渲染基础设施支持的纹理格式。
`viewFormat`通常与`format`值相同。在某些情况下，例如渲染为`_SRGB`格式的纹理时，且不需要在着色器写入时隐式线性>sRGB转换，值可能会不同。但请注意，当运行时`QRhi`报告`QRhi::TextureViewFormat`功能不支持时，Qt可能会忽略该值。
`pixelSize` 指定图像的像素大小。目前仅支持二维纹理和二维纹理数组。
`sampleCount` 指定采样数量。0 或 1 表示不进行多重采样，而 4 或 8 等值表示原生对象是多采样纹理，除非`flags`包含 `MultisampleResolve`。此时，`texture` 被假设为非多采样的二维纹理或二维纹理数组，`sampleCount` 定义所需的采样数量。最终的`QQuickRenderTarget`将使用中间自动生成的多采样纹理（或纹理数组）作为颜色附加，并将采样解析为`texture`。这是当原生金属纹理尚未多采样时，执行MSAA的推荐方法。
数组元素（图层）的数量以`arraySize`表示。当数值大于1时，表示多视角渲染，这在VR/AR中尤为重要。`arraySize`是视角数量，通常为`2`。有关在Qt Quick场景图中启用多视角渲染的详细信息，请参见 `QSGMaterial::viewCount()`。
纹理作为 Qt Quick 场景图渲染目标的第一个颜色附加。如果适用，深度模板缓冲区会自动创建并使用。当颜色缓冲区为多重采样时，深度模板缓冲区也会自动为多重采样。对于多视图渲染，深度模板纹理会自动组成与匹配`arraySize`的数组。
注意：最终`QQuickRenderTarget`不拥有任何本地资源，仅包含引用及相关大小和样本数的元数据。调用者有责任确保本地资源在必要时间内持续存在。

### `[static, since 6.2] QQuickRenderTarget QQuickRenderTarget::fromOpenGLRenderBuffer(uint renderbufferId, const QSize &pixelSize, int sampleCount = 1)`

**作用与语义：**

返回一个新的`QQuickRenderTarget`，引用由`renderbufferId`指定的OpenGL渲染缓冲对象。
渲染缓冲区将作为内部帧缓冲对象的颜色附件。该功能旨在支持应用程序创建的渲染缓冲区，这些缓冲区下方有外部缓冲区，例如 EGLImageKHR。一旦应用程序调用了 glEGLImageTargetRenderbufferStorageOES，渲染缓冲区就可以传递给该函数。
`pixelSize` 指定图像的大小，单位为像素。
`sampleCount` 指定采样数量。0 或 1 表示不进行多重采样，而 4 或 8 表示本地对象是多采样渲染缓冲区。
注意：最终`QQuickRenderTarget`不拥有任何本地资源，仅包含引用及相关大小和样本数的元数据。调用者有责任确保本地资源在必要时间内持续存在。

### `[static, since 6.4] QQuickRenderTarget QQuickRenderTarget::fromOpenGLTexture(uint textureId, uint format, const QSize &pixelSize, int sampleCount = 1)`

**作用与语义：**

返回一个新的`QQuickRenderTarget`，引用由`textureId`指定的OpenGL纹理对象。
`format` 指定了纹理的原生内部格式。仅应使用 Qt 渲染基础设施支持的纹理格式。
`pixelSize` 指定图像的大小，单位为像素。目前仅支持 2D 纹理。
`sampleCount` 表示采样数量。0 或 1 表示不进行多重采样，而 4 或 8 这样的值表示该对象是多采样纹理。
纹理作为 Qt Quick 场景图渲染目标的第一个颜色附加。如适用，深度模板缓冲区会自动创建并使用。
OpenGL 对象名 `textureId` 必须是 Qt 快速场景图渲染上下文中的有效名称。
注意：生成的`QQuickRenderTarget`不拥有任何本地资源，仅包含引用及相关大小和样本数量的元数据。调用者有责任确保本地资源在必要时间内持续存在。

### `[static] QQuickRenderTarget QQuickRenderTarget::fromOpenGLTexture(uint textureId, const QSize &pixelSize, int sampleCount = 1)`

**作用与语义：**

返回一个新的`QQuickRenderTarget`，引用由`textureId`指定的OpenGL纹理对象。该纹理假设格式为GL_RGBA（GL_RGBA8）。
`pixelSize` 指定图像的大小，单位为像素。目前仅支持 2D 纹理。
`sampleCount` 指定采样数量。0 或 1 表示不进行多重采样，而 4 或 8 表示本地对象是多采样纹理。
纹理作为 Qt Quick 场景图渲染目标的第一个颜色附加。如适用，深度模板缓冲区会自动创建并使用。
OpenGL 对象名 `textureId` 必须在 Qt Quick 场景图所使用的渲染上下文中是有效名称。
注意：最终的`QQuickRenderTarget`不拥有任何原生资源，仅包含引用及相关大小和样本数的元数据。调用者有责任确保本地资源持续存在直到必要。

### `[static, since 6.8] QQuickRenderTarget QQuickRenderTarget::fromOpenGLTexture(uint textureId, uint format, QSize pixelSize, int sampleCount, int arraySize, QQuickRenderTarget::Flags flags)`

**作用与语义：**

返回引用 `textureId` 指定的 OpenGL 2D 纹理或纹理数组对象的新`QQuickRenderTarget`。
`format` 指定了纹理的原生内部格式。仅应使用 Qt 渲染基础设施支持的纹理格式。
`pixelSize` 指定图像的像素大小。目前仅支持 2D 纹理和 2D 纹理数组。
`sampleCount` 指定采样数量。0 或 1 表示不进行多重采样，而 4 或 8 表示原生对象是多采样纹理，除非 `flags` 包含 `MultisampleResolve`。此时，`textureId` 被假定为非多采样的二维纹理或二维纹理数组，`sampleCount` 定义了所需的采样数。最终的`QQuickRenderTarget`将使用中间自动生成的多采样纹理（或纹理数组）作为颜色附加，并将采样分解为`textureId`。这是当原生 OpenGL 纹理尚未多采样时，执行 MSAA 的推荐方法。
当`arraySize`大于1时，意味着多视角渲染（GL_OVR_multiview、`QRhiColorAttachment::setMultiViewCount()`），这在VR/AR中尤为重要。此时`arraySize`为视角数量，通常为`2`。有关在Qt Quick场景图中启用多视角渲染的详细信息，请参见 `QSGMaterial::viewCount()`。
如果适用，深度模板缓冲区会自动创建并使用。当颜色缓冲区为多重采样时，深度模板缓冲区也会自动为多重采样。对于多视图渲染，深度模板纹理会自动组成数组，`arraySize`匹配。
OpenGL 对象名 `textureId` 必须是 Qt Quick 场景图渲染上下文中的有效二维纹理名称。当 `arraySize` 大于 1 时，`textureId` 必须是有效的二维纹理数组名称。
注意：最终`QQuickRenderTarget`不拥有任何本地资源，仅包含引用及相关大小和样本数的元数据。调用方有责任确保本地资源在必要时间内持续存在。
注意：该超载的实现与 OpenGL ES 2.0 或 3.0 不兼容，至少需要 OpenGL ES 3.1。（桌面端则需 OpenGL 3.0）。

### `[static, since 6.4] QQuickRenderTarget QQuickRenderTarget::fromPaintDevice(QPaintDevice *device)`

**作用与语义：**

返回一个新的`QQuickRenderTarget`，引用由`device`指定的绘画设备对象。
这种将渲染重定向到`QPaintDevice`的选项仅在运行 Qt Quick `software` 后端时才可用。
注意：`QQuickRenderTarget`不承担`device`所有权，调用者有责任确保该物体在必要时间内持续存在。

### `[static, since 6.6] QQuickRenderTarget QQuickRenderTarget::fromRhiRenderTarget(QRhiRenderTarget *renderTarget)`

**作用与语义：**

返回一个引用现有`renderTarget`的新`QQuickRenderTarget`。
`renderTarget`大多数情况下会是一个`QRhiTextureRenderTarget`，允许将Qt Quick场景的渲染直接导入`QRhiTexture`。
注意：最终的`QQuickRenderTarget`不拥有`renderTarget`及任何底层原生资源，仅包含引用及相关大小和样本数量的元数据。调用者有责任确保被引用资源持续存在，直到必要时间为止。

### `[static, since 6.4] QQuickRenderTarget QQuickRenderTarget::fromVulkanImage(VkImage image, VkImageLayout layout, VkFormat format, const QSize &pixelSize, int sampleCount = 1)`

**作用与语义：**

返回一个新的 `QQuickRenderTarget`，它引用由 `image` 指定的 Vulkan 图像对象。图像的当前 `layout` 也必须提供。
`format` 指定图像的 VkFormat。仅应使用 Qt 渲染基础设施支持的图像格式。
`pixelSize` 指定图像的尺寸，以像素为单位。目前仅支持 2D 纹理。
`sampleCount` 指定样本数量。0 或 1 表示不进行多重采样，而像 4 或 8 这样的值表示原生对象是多重采样纹理。
该图像被用作 Qt Quick 场景图使用的渲染目标的第一个颜色附件。深度模板缓冲区（如适用）会被自动创建和使用。
注意：生成的 `QQuickRenderTarget` 不拥有任何原生资源，它仅包含引用及尺寸和样本数量的相关元数据。调用者有责任确保原生资源在必要的时间内存在。

### `[static] QQuickRenderTarget QQuickRenderTarget::fromVulkanImage(VkImage image, VkImageLayout layout, const QSize &pixelSize, int sampleCount = 1)`

**作用与语义：**

返回一个新的`QQuickRenderTarget`，引用由`image`指定的Vulkan图像对象。假设该图像格式为VK_FORMAT_R8G8B8A8_UNORM。
`pixelSize` 指定图像的大小，单位为像素。目前仅支持 2D 纹理。
`sampleCount` 指定采样数量。0 或 1 表示不进行多重采样，而 4 或 8 表示本地对象是多采样纹理。
纹理作为 Qt Quick 场景图渲染目标的第一个颜色附加。如适用，深度模板缓冲区会自动创建并使用。
注意：最终`QQuickRenderTarget`不拥有任何本地资源，仅包含引用及相关大小和样本数的元数据。调用者有责任确保本地资源在必要时间内持续存在。

### `[static, since 6.8] QQuickRenderTarget QQuickRenderTarget::fromVulkanImage(VkImage image, VkImageLayout layout, VkFormat format, VkFormat viewFormat, QSize pixelSize, int sampleCount, int arraySize, QQuickRenderTarget::Flags flags)`

**作用与语义：**

返回一个新的`QQuickRenderTarget`，引用由`image`指定的Vulkan图像对象。还必须提供当前图像的当前`layout`。图像必须是2D纹理或2D纹理数组。
`format` 指定了图像的 VkFormat。仅应使用 Qt 渲染基础设施支持的图像格式。
`viewFormat`通常与`format`值相同。在某些情况下，比如渲染为`_SRGB`格式的纹理时，且不需要在着色器写入时隐式线性>sRGB转换，值可能会不同。（例如，`format`为`VK_FORMAT_R8G8B8A8_SRGB`，`viewFormat`为`VK_FORMAT_R8G8B8A8_UNORM`）。
`pixelSize` 指定图像的大小，单位为像素。目前仅支持 2D 纹理。
`sampleCount` 指定采样数量。0 或 1 表示不进行多重采样，而 4 或 8 表示原生对象是多采样纹理，除非 `flags` 包含 `MultisampleResolve`。此时，`image` 被假定为非多采样的二维纹理或二维纹理数组，`sampleCount`定义了所需的采样数量。最终的`QQuickRenderTarget`将使用中间自动生成的多采样纹理（或纹理数组）作为颜色附加，并将采样解析为`image`。这是当原生Vulkan图像尚未多采样时，执行MSAA的推荐方法。
数组元素（图层）的数量以`arraySize`表示。当数组大于1时，表示多视角渲染（VK_KHR_multiview），这在VR/AR中尤为重要。`arraySize`表示视图数量，通常为`2`。有关在Qt Quick场景图中启用多视图渲染的详细信息，请参见 `QSGMaterial::viewCount()`。
纹理作为 Qt Quick 场景图渲染目标的第一个颜色附加。深度模板缓冲区（如适用）会自动创建并使用。当颜色缓冲区为多重采样时，深度模板缓冲区也会自动为多重采样。对于多视图渲染，深度模板纹理会自动组成数组，`arraySize`匹配。
注意：生成的`QQuickRenderTarget`不拥有任何本地资源，仅包含引用及相关大小和样本数的元数据。调用者有责任确保本地资源在必要时间内持续存在。

### `bool QQuickRenderTarget::isNull() const`

**作用与语义：**

如果该 `QQuickRenderTarget` 是默认构造的，且不引用本地对象，则返回为真。

### `[since 6.4] bool QQuickRenderTarget::mirrorVertically() const`

**作用与语义：**

返回 返回渲染目标是否垂直镜像。
默认值是`false`。

### `[since 6.8] void QQuickRenderTarget::setDepthTexture(QRhiTexture *texture)`

**作用与语义：**

使用给定`texture`作为深度或深度模板缓冲区的请求。不对`texture`所有权。
只有在相关时才会考虑请求。例如，调用该函数对`fromRhiRenderTarget()`、`fromPaintDevice()`或 `fromOpenGLRenderBuffer()` 没有影响。
通常深度模板缓冲区是自动创建的，对`QQuickRenderTarget`用户透明。因此，在大多数情况下使用`QQuickRenderTarget`时无需调用该函数。但在特殊情况下，能够提供纹理来渲染深度（或深度和模板）数据变得至关重要，而不是让 Qt Quick 自行创建中间纹理或缓冲区。一个例子是 OpenXR 及其扩展如 XR_KHR_composition_layer_depth。为了“提交深度缓冲区”给 XR 合成器，实际上必须从 OpenXR（来自 XrSwapchain）中获取已创建的深度（深度模板）纹理，并以此作为深度数据的渲染目标。没有这个函数，这是不可能实现的。
注意：`texture`始终预期为非多重采样的2D纹理或纹理数组（用于多视图）。如果涉及MSAA，采样在渲染结束时会被解析为`texture`，无论是否设置了`MultisampleResolve`标志。MSAA仅在底层3D API支持深度（深度模板）纹理时支持，且该支持并非普遍可用。详情请参见相关的QRhi功能标志。当不支持该标志且请求多重采样并结合自定义深度纹理时，渲染过程中不会触碰`texture`，并会打印警告。
注意：在 OpenGL 和 OpenGL ES 中，使用 depth textures 在 OpenGL ES 2.0 上不可用，且至少需要 OpenGL ES 3.0。没有至少 OpenGL ES 3.1 或桌面版 OpenGL 3.0，则无法支持多重采样（MSAA）。

### `[since 6.3] void QQuickRenderTarget::setDevicePixelRatio(qreal ratio)`

**作用与语义：**

将该渲染目标的设备像素比设置为`ratio`。这是设备像素与设备无关像素之间的比值。
注意，如果重新实现`QQuickRenderControl::renderWindow()`返回有效`QWindow`，指定的设备像素比率值将被忽略。

### `[since 6.4] void QQuickRenderTarget::setMirrorVertically(bool enable)`

**作用与语义：**

绘制时渲染目标内容的尺寸应垂直镜像到`enable`。这便于轻松集成不符合标准期望的第三方渲染代码。
注意：使用`software`后端时不应使用此函数。

### `[noexcept] bool operator!=(const QQuickRenderTarget &a, const QQuickRenderTarget &b)`

**作用与语义：**

如果`a`和`b`指的是不同的本地对象集，或者相关数据（大小、样本数）不匹配，则返回为真。

### `[noexcept] bool operator==(const QQuickRenderTarget &a, const QQuickRenderTarget &b)`

**作用与语义：**

如果`a`和`b`引用相同的本地对象集合且关联数据（大小、样本数）相匹配，则返回为真。

### `(since 6.8) enum class Flag { MultisampleResolve }`

**作用与语义：**

静态`QQuickRenderTarget`构造函数的标志。
- `QQuickRenderTarget::Flag::MultisampleResolve`：`0x01`;表示`sampleCount`参数不是所提供纹理的采样数（且纹理仍非多重采样纹理），而是多采样抗锯齿所需的采样。触发自动创建和管理中间多采样纹理（或纹理数组）作为颜色缓冲区，对应用程序透明。采样在渲染结束时自动解析为提供的纹理。当该标志未被设置且`sampleCount`参数大于1时，表示提供的纹理是多重采样的。当`sampleCount`为1时，该标志无效（表明不涉及多重采样）。
这个枚举是在Qt 6.8引入的。
Flags 类型是 QFlags 的 typedef<Flag>。它存储 Flag 值的 OR 组合。

### `flags Flags`

**作用与语义：**

静态`QQuickRenderTarget`构造函数的标志。
- `QQuickRenderTarget::Flag::MultisampleResolve`：`0x01`;表示`sampleCount`参数不是所提供纹理的采样数（且纹理仍非多重采样纹理），而是多采样抗锯齿所需的采样。触发自动创建和管理中间多采样纹理（或纹理数组）作为颜色缓冲区，对应用程序透明。采样在渲染结束时自动解析为提供的纹理。当该标志未被设置且`sampleCount`参数大于1时，表示提供的纹理是多重采样的。当`sampleCount`为1时，该标志无效（表明不涉及多重采样）。
这个枚举是在Qt 6.8引入的。
Flags 类型是 QFlags 的 typedef<Flag>。它存储 Flag 值的 OR 组合。

## 6. 深入实践与常见坑

### 生命周期和资源边界

QML 引擎、上下文和对象所有权必须明确。由 QML 创建的对象通常由引擎管理；通过 context property 或 C++ 暴露的对象要决定由 C++ 持有还是转移给 QML，不能让绑定指向悬空对象。

### 状态和错误边界

属性绑定和直接赋值不是一回事：直接给被绑定属性赋值通常会打破原有绑定。C++ 属性要有正确的 notify signal，QML 才能在数据变化时更新；信号参数和属性当前值要保持一致。

### 线程边界

大多数 QML 对象和 GUI 操作在 GUI 线程，场景图渲染还可能在 render thread。不要在渲染阶段调用 GUI 对象 API；后台数据通过线程安全的信号/槽边界送入 QML。

### 最容易出现的错误

不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QQuickRenderTarget` 所属机制类型：QML 属性绑定与场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
