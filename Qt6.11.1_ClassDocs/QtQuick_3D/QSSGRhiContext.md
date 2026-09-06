# QSSGRhiContext

> Qt 6.11.1 · Qt Quick 3D

## 1. 先建立直觉

**一句话定位：** `QSSGRhiContext` 是 QML 属性绑定与场景图机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Quick 3D 在 Qt Quick 中加入 3D 场景、相机、材质、模型和渲染能力。

### 这是什么

`QSSGRhiContext` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QSSGRhiContext>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

### 状态、生命周期和线程

**生命周期：** QML 引擎、上下文和对象所有权必须明确。由 QML 创建的对象通常由引擎管理；通过 context property 或 C++ 暴露的对象要决定由 C++ 持有还是转移给 QML，不能让绑定指向悬空对象。

**状态与结果：** 属性绑定和直接赋值不是一回事：直接给被绑定属性赋值通常会打破原有绑定。C++ 属性要有正确的 notify signal，QML 才能在数据变化时更新；信号参数和属性当前值要保持一致。

**线程与事件循环：** 大多数 QML 对象和 GUI 操作在 GUI 线程，场景图渲染还可能在 render thread。不要在渲染阶段调用 GUI 对象 API；后台数据通过线程安全的信号/槽边界送入 QML。

## 3. 直接使用

需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。 使用时通常按这个过程组织：注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `void checkAndAdjustForNPoT(QRhiTexture *texture, QSSGRhiSamplerDescription *samplerDescription)`
- `QRhiCommandBuffer * commandBuffer() const`
- `QRhiCommandBuffer::BeginPassFlags commonPassFlags() const`
- `QRhiTexture * dummyTexture(QRhiTexture::Flags flags, QRhiResourceUpdateBatch *rub, const QSize &size = QSize(64, 64), const QColor &fillColor = Qt::black, int arraySize = 0)`
- `bool isValid() const`
- `int mainPassSampleCount() const`
- `int mainPassViewCount() const`
- `QRhiRenderPassDescriptor * mainRenderPassDescriptor() const`
- `QRhiRenderTarget * renderTarget() const`
- `QRhi * rhi() const`
- `QRhiSampler * sampler(const QSSGRhiSamplerDescription &samplerDescription)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `void QSSGRhiContext::checkAndAdjustForNPoT(QRhiTexture *texture, QSSGRhiSamplerDescription *samplerDescription)`

**作用与语义：**

根据`texture`像素大小调整`samplerDescription`的平铺和过滤模式。
在大多数情况下，`samplerDescription`不会被更改。然而，在使用较旧的旧版3D API时，对于宽度或高度非幂的纹理，`QRhiSampler::Repeat`可能不支持平铺模式。
这一便利功能有助于创建稳健的应用程序，即使在运行时 OpenGL ES 2.0 或 WebGL 1 实现不支持 `QRhi::NPOTTextureRepeat` 等功能时，也能正常运行。

### `QRhiCommandBuffer *QSSGRhiContext::commandBuffer() const`

**作用与语义：**

返回当前帧的命令缓冲区，用于Qt Quick 3D渲染器。

### `QRhiCommandBuffer::BeginPassFlags QSSGRhiContext::commonPassFlags() const`

**作用与语义：**

退货 调用`QRhiCommandBuffer::beginPass()`时推荐的标志。

### `QRhiTexture *QSSGRhiContext::dummyTexture(QRhiTexture::Flags flags, QRhiResourceUpdateBatch *rub, const QSize &size = QSize(64, 64), const QColor &fillColor = Qt::black, int arraySize = 0)`

**作用与语义：**

返回一个纹理，其`flags`和像素`size`都符合指定。
这旨在高效访问填充给定`fillColor`的“虚拟”纹理，并在渲染堆栈的不同位置重复使用。
`rub`必须是有效的`QRhiResourceUpdateBatch`，因为如果找不到合适的缓存对象，该函数会创建新的纹理并为其生成内容。必要的上传操作随后会被排在该更新批次中。
当`arraySize`为2或更多时，返回一个二维纹理数组。
归还的贴图归 Qt Quick 3D 所有。

### `bool QSSGRhiContext::isValid() const`

**作用与语义：**

如果渲染器成功初始化，则返回 true。

### `int QSSGRhiContext::mainPassSampleCount() const`

**作用与语义：**

返回主渲染时使用的采样计数。

### `int QSSGRhiContext::mainPassViewCount() const`

**作用与语义：**

返回主渲染时使用的多视角计数。当使用多视角渲染时，这可能是2，或者1（无多视角）。

### `QRhiRenderPassDescriptor *QSSGRhiContext::mainRenderPassDescriptor() const`

**作用与语义：**

返回Qt Quick 3D渲染器主渲染通道所用的`QRhiRenderPassDescriptor`。

### `QRhiRenderTarget *QSSGRhiContext::renderTarget() const`

**作用与语义：**

返回 Qt Quick 3D 渲染器在当前帧中用于主渲染通道的渲染目标。
如果`View3D`使用非“屏幕外”的渲染模式，这实际上可以是交换链中的渲染目标。更常见的是，渲染目标指的是纹理（即`QRhiTextureRenderTarget`），例如因为renderMode是默认的屏幕外，或者因为使用了后期处理效果。

### `QRhi *QSSGRhiContext::rhi() const`

**作用与语义：**

返回 Qt Quick 3D 渲染器使用的`QRhi`对象。

### `QRhiSampler *QSSGRhiContext::sampler(const QSSGRhiSamplerDescription &samplerDescription)`

**作用与语义：**

返回一个采样器，包含`samplerDescription`中指定的滤波器和铺砖模式。
生成的`QRhiSampler`对象会被缓存并重复使用。因此，这是一种方便的方式，可以利用给定设置访问`QRhiSampler`，而无需频繁创建新的专用对象。
归还`QRhiSampler`的所有权仍归 Qt Quick 3D 所有。

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

`QSSGRhiContext` 所属机制类型：QML 属性绑定与场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
