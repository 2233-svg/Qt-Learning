# QSGTexture

> Qt 6.11.1 · Qt Quick

## 1. 先建立直觉

**一句话定位：** `QSGTexture` 是 Qt Quick 场景图渲染类型，负责节点、材质、纹理、几何或渲染状态。

**模块背景：** Qt Quick 面向 QML/场景图界面，提供可视项、动画、输入和高性能界面基础设施。

### 这是什么

`QSGTexture` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QSGTexture>`
- 继承自：QObject
- 直接派生类：QSGDynamicTexture

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Quick)
target_link_libraries(mytarget PRIVATE Qt6::Quick)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

### 状态、生命周期和线程

**生命周期：** 场景图节点和材质的有效期受窗口、组件和渲染阶段控制；纹理、材质和几何通常要在正确的 render context 中创建/释放。节点被删除或场景图失效后，底层 GPU 资源不能继续使用。

**状态与结果：** 区分 GUI/同步阶段、渲染阶段、节点 dirty 状态、纹理状态和后端能力。改变节点属性通常要标记更新，不能在错误阶段直接修改资源；材质是否可用还受默认后端限制。

**线程与事件循环：** QSG 类型经常运行在 render thread，不能从 GUI 线程或后台线程随意读写。通过 QQuickItem 的同步接口在规定阶段交换数据，避免跨线程共享 GPU 资源。

## 3. 直接使用

需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。 使用时通常按这个过程组织：注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum AnisotropyLevel { AnisotropyNone, Anisotropy2x, Anisotropy4x, Anisotropy8x, Anisotropy16x }`
- `enum Filtering { None, Nearest, Linear }`
- `enum WrapMode { Repeat, ClampToEdge, MirroredRepeat }`

### 公有函数

- `QSGTexture()`
- `virtual ~QSGTexture() override`
- `QSGTexture::AnisotropyLevel anisotropyLevel() const`
- `(since 6.0) virtual void commitTextureOperations(QRhi *rhi, QRhiResourceUpdateBatch *resourceUpdates)`
- `virtual qint64 comparisonKey() const = 0`
- `QRectF convertToNormalizedSourceRect(const QRectF &rect) const`
- `QSGTexture::Filtering filtering() const`
- `virtual bool hasAlphaChannel() const = 0`
- `virtual bool hasMipmaps() const = 0`
- `QSGTexture::WrapMode horizontalWrapMode() const`
- `virtual bool isAtlasTexture() const`
- `QSGTexture::Filtering mipmapFiltering() const`
- `QNativeInterface * nativeInterface() const`
- `virtual QRectF normalizedTextureSubRect() const`
- `virtual QSGTexture * removedFromAtlas(QRhiResourceUpdateBatch *resourceUpdates = nullptr) const`
- `(since 6.0) virtual QRhiTexture * rhiTexture() const`
- `void setAnisotropyLevel(QSGTexture::AnisotropyLevel level)`
- `void setFiltering(QSGTexture::Filtering filter)`
- `void setHorizontalWrapMode(QSGTexture::WrapMode hwrap)`
- `void setMipmapFiltering(QSGTexture::Filtering filter)`
- `void setVerticalWrapMode(QSGTexture::WrapMode vwrap)`
- `virtual QSize textureSize() const = 0`
- `QSGTexture::WrapMode verticalWrapMode() const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QSGTexture::AnisotropyLevel`

**作用与语义：**

指定当纹理未与屏幕对齐时，应采用的各向异性过滤水平。
- `QSGTexture::AnisotropyNone`：`0`;无各向异性过滤。
- `QSGTexture::Anisotropy2x`：`1`;2个各向异性滤波。
- `QSGTexture::Anisotropy4x`：`2`;4倍各向异性滤波。
- `QSGTexture::Anisotropy8x`：`3`;8倍各向异性滤波。
- `QSGTexture::Anisotropy16x`：`4`;16倍各向异性滤波。

### `enum QSGTexture::Filtering`

**作用与语义：**

规定当纹理坐标未对齐时，采样纹素应如何过滤。
- `QSGTexture::None`：`0`;不应进行过滤。该值仅与`setMipmapFiltering()`一起使用。
- `QSGTexture::Nearest`：`1`;采样返回最近的像素。
- `QSGTexture::Linear`：`2`;采样返回邻近纹素的线性插值。

### `enum QSGTexture::WrapMode`

**作用与语义：**

指定采样器应如何处理纹理坐标。
- `QSGTexture::Repeat`：`0`;仅使用纹理坐标的分数部分，导致大于1和低于0的值重复出现。
- `QSGTexture::ClampToEdge`：`1`;大于1的数值被夹为1，低于0的数值被夹为0。
- `QSGTexture::MirroredRepeat`：`2`;当纹理坐标为偶数时，仅使用小数部分。当为奇数时，纹理坐标设置为`1 - fractional part`。该值在Qt 5.10中引入。

### `QSGTexture::QSGTexture()`

**作用与语义：**

构造QSGTexture基类。

### `[override virtual noexcept] QSGTexture::~QSGTexture()`

**作用与语义：**

摧毁了`QSGTexture`。

### `QSGTexture::AnisotropyLevel QSGTexture::anisotropyLevel() const`

**作用与语义：**

返回用于过滤该纹理的各向异性水平。

### `[virtual, since 6.0] void QSGTexture::commitTextureOperations(QRhi *rhi, QRhiResourceUpdateBatch *resourceUpdates)`

**作用与语义：**

调用该函数将图像上传操作排队到`resourceUpdates`，以防有待处理操作。当没有新数据（例如，自上次调用该函数以来没有setImage()时，该函数不做任何操作。
涉及`rhi`纹理的材质通常会从`updateSampledImage()`实现中调用该函数，通常没有任何条件，从`QSGMaterialShader::RenderState`传递`state.rhi()`和`state.resourceUpdateBatch()`。
警告：该函数只能从渲染线程中调用。

### `[pure virtual] qint64 QSGTexture::comparisonKey() const`

**作用与语义：**

返回一个适合比较纹理的键。通常用于`QSGMaterial::compare()`实现。
仅仅比较`QSGTexture`指针并不总是足够，因为两个引用同一原生纹理对象的`QSGTexture`实例也应被视为相等。因此需要这个函数。
如果目前还没有图形资源（原生纹理对象），该函数的实现通常不会创建，也不应生成。
没有原生纹理对象的`QSGTexture`通常不等于其他`QSGTexture`，因此返回值必须相应设计。有例外，特别是当使用图集（多个纹理共享同一个图集纹理时），这就由子类实现根据情况处理。
警告：该函数只能从渲染线程中调用。

### `QRectF QSGTexture::convertToNormalizedSourceRect(const QRectF &rect) const`

**作用与语义：**

返回`rect`转换为归一化坐标。

### `QSGTexture::Filtering QSGTexture::filtering() const`

**作用与语义：**

返回用于该纹理的采样模式。

### `[pure virtual] bool QSGTexture::hasAlphaChannel() const`

**作用与语义：**

如果纹理数据包含alpha通道，则返回为true。

### `[pure virtual] bool QSGTexture::hasMipmaps() const`

**作用与语义：**

如果纹理数据包含 mipmap 级别，则返回为真。

### `QSGTexture::WrapMode QSGTexture::horizontalWrapMode() const`

**作用与语义：**

返回用于该纹理的水平包裹模式。

### `[virtual] bool QSGTexture::isAtlasTexture() const`

**作用与语义：**

无论该纹理是否属于图谱，都会返回。
默认实现会返回false。

### `QSGTexture::Filtering QSGTexture::mipmapFiltering() const`

**作用与语义：**

返回从该纹理采样时是否应使用多重映射。

### `template <typename QNativeInterface> QNativeInterface *QSGTexture::nativeInterface() const`

**作用与语义：**

返回给定类型的原生纹理接口。
该功能提供访问`QSGTexture`平台特定功能，具体内容在`QNativeInterface`命名空间中声明：
- `QNativeInterface::QSGD3D11Texture`：提供访问并支持采用 Direct3D 11 纹理对象
- `QNativeInterface::QSGD3D12Texture`：提供访问并支持采用Direct3D 12纹理对象
- `QNativeInterface::QSGMetalTexture`：提供访问并支持采用金属纹理对象
- `QNativeInterface::QSGOpenGLTexture`：提供访问并支持采用 OpenGL 纹理对象
- `QNativeInterface::QSGVulkanTexture`：提供访问并支持采用 Vulkan 图像对象
这允许访问底层的原生纹理对象，例如用OpenGL访问`GLuint`纹理ID，或用Vulkan访问`VkImage`句柄。
如果请求的接口不可用，则返回`nullptr`。

### `[virtual] QRectF QSGTexture::normalizedTextureSubRect() const`

**作用与语义：**

返回`textureSize()`内的矩形，该纹理在归一化坐标下表示。
默认实现返回位置为0， 0的rect，宽度和高度均为1。

### `[virtual] QSGTexture *QSGTexture::removedFromAtlas(QRhiResourceUpdateBatch *resourceUpdates = nullptr) const`

**作用与语义：**

该函数返回当前纹理的副本，从其图集中移除。
当前纹理保持不变，因此纹理坐标无需更新。
从图集中移除纹理主要适用于将其传递给操作纹理坐标0-1的着色器，而不是图集内部纹理子rect。
如果纹理不属于纹理图集，该函数返回为0。
建议实现该函数时多次调用返回同一实例，以限制内存使用。
`resourceUpdates` 是一个可选的资源更新批次，纹理操作（如有）会被排队。Material 可以从 `QSGMaterialShader::RenderState` 获取实例。当 null 时，removedFromAtlas() 实现会创建自己的批次并立即提交。但当指定有效实例时，该函数不会提交更新批次。
警告：该函数只能从渲染线程中调用。

### `[virtual, since 6.0] QRhiTexture *QSGTexture::rhiTexture() const`

**作用与语义：**

返回该`QRhiTexture` `QSGTexture`，若无则返回空（可能是内部尚未创建有效纹理，或该概念不适用于当前场景图后端）。
如果没有新 Null `QRhiTexture`，这个函数不应该创建。在这种情况下，它应该返回 null。渲染器的期望是，null 纹理会导致使用透明的虚拟纹理。
警告：该函数只能从渲染线程中调用。

### `void QSGTexture::setAnisotropyLevel(QSGTexture::AnisotropyLevel level)`

**作用与语义：**

将各向异性过滤设置为`level`。默认值为`QSGTexture::AnisotropyNone`，意味着不启用各向异性过滤。
注意：根据所使用的图形 API，请求可能会被忽略。运行时并不保证支持各向异性过滤。

### `void QSGTexture::setFiltering(QSGTexture::Filtering filter)`

**作用与语义：**

将采样模式设置为`filter`。

### `void QSGTexture::setHorizontalWrapMode(QSGTexture::WrapMode hwrap)`

**作用与语义：**

将水平包裹模式设置为`hwrap`。

### `void QSGTexture::setMipmapFiltering(QSGTexture::Filtering filter)`

**作用与语义：**

将mipmap采样模式设置为`filter`。
设置 mipmap 过滤没有效果，只要纹理没有 mipmaps。

### `void QSGTexture::setVerticalWrapMode(QSGTexture::WrapMode vwrap)`

**作用与语义：**

将垂直包裹模式设置为`vwrap`。

### `[pure virtual] QSize QSGTexture::textureSize() const`

**作用与语义：**

返回纹理的像素大小。

### `QSGTexture::WrapMode QSGTexture::verticalWrapMode() const`

**作用与语义：**

返回用于该纹理的垂直包裹模式。

## 6. 深入实践与常见坑

### 生命周期和资源边界

场景图节点和材质的有效期受窗口、组件和渲染阶段控制；纹理、材质和几何通常要在正确的 render context 中创建/释放。节点被删除或场景图失效后，底层 GPU 资源不能继续使用。

### 状态和错误边界

区分 GUI/同步阶段、渲染阶段、节点 dirty 状态、纹理状态和后端能力。改变节点属性通常要标记更新，不能在错误阶段直接修改资源；材质是否可用还受默认后端限制。

### 线程边界

QSG 类型经常运行在 render thread，不能从 GUI 线程或后台线程随意读写。通过 QQuickItem 的同步接口在规定阶段交换数据，避免跨线程共享 GPU 资源。

### 最容易出现的错误

不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QSGTexture` 所属机制类型：Qt Quick 场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
