# QSSGRhiGraphicsPipelineState

> Qt 6.11.1 · Qt Quick 3D

## 1. 先建立直觉

**一句话定位：** `QSSGRhiGraphicsPipelineState` 是 QML 属性绑定与场景图机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Quick 3D 在 Qt Quick 中加入 3D 场景、相机、材质、模型和渲染能力。

### 这是什么

`QSSGRhiGraphicsPipelineState` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QSSGRhiGraphicsPipelineState>`
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

### 公有类型

- `enum class Flag { DepthTestEnabled, DepthWriteEnabled, BlendEnabled, UsesStencilRef, UsesScissor }`
- `flags Flags`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum class QSSGRhiGraphicsPipelineState::Flagflags QSSGRhiGraphicsPipelineState::Flags`

**作用与语义：**

- `QSSGRhiGraphicsPipelineState::Flag::DepthTestEnabled`: `0x1`
- `QSSGRhiGraphicsPipelineState::Flag::DepthWriteEnabled`: `0x2`
- `QSSGRhiGraphicsPipelineState::Flag::BlendEnabled`: `0x4`
- `QSSGRhiGraphicsPipelineState::Flag::UsesStencilRef`: `0x8`
- `QSSGRhiGraphicsPipelineState::Flag::UsesScissor`: `0x10`
Flags 类型是 QFlags<Flag> 的 typedef。它存储 Flag 值的按位或组合。

### `int QSSGRhiGraphicsPipelineState::colorAttachmentCount`

**作用与语义：**

颜色附件的数量。默认是1。

### `QRhiGraphicsPipeline::CullMode QSSGRhiGraphicsPipelineState::cullMode`

**作用与语义：**

指定剔除模式。

### `int QSSGRhiGraphicsPipelineState::depthBias`

**作用与语义：**

深度偏移。默认值为 0。

### `QRhiGraphicsPipeline::CompareOp QSSGRhiGraphicsPipelineState::depthFunc`

**作用与语义：**

深度比较函数。

### `float QSSGRhiGraphicsPipelineState::lineWidth`

**作用与语义：**

所用线宽。默认是1.0。
注意：对于1.0以外的数值，必须在运行时报告功能`QRhi::WideLines`支持。

### `QRhiGraphicsPipeline::PolygonMode QSSGRhiGraphicsPipelineState::polygonMode`

**作用与语义：**

多边形模式值。默认是`Fill`。

### `int QSSGRhiGraphicsPipelineState::samples`

**作用与语义：**

样本数量。
注意：采样计数为1意味着没有多重采样抗锯齿。

### `QRhiScissor QSSGRhiGraphicsPipelineState::scissor`

**作用与语义：**

剪刀，没错。
注意：仅在`UsesScissor`设置时使用。

### `float QSSGRhiGraphicsPipelineState::slopeScaledDepthBias`

**作用与语义：**

斜率缩放深度偏移。默认值为0。

### `QRhiGraphicsPipeline::StencilOpState QSSGRhiGraphicsPipelineState::stencilOpFrontState`

**作用与语义：**

描述模板操作状态。

### `quint32 QSSGRhiGraphicsPipelineState::stencilRef`

**作用与语义：**

活动模板参考值。 注意：只有在设置了 `UsesStencilRef` 时才使用。

### `quint32 QSSGRhiGraphicsPipelineState::stencilWriteMask`

**作用与语义：**

模板写入掩码值。默认值为`0xFF`。

### `std::array<QRhiGraphicsPipeline::TargetBlend, 8> QSSGRhiGraphicsPipelineState::targetBlend`

**作用与语义：**

一个颜色附件的混合状态。

### `QRhiViewport QSSGRhiGraphicsPipelineState::viewport`

**作用与语义：**

用于渲染的视口尺寸。

### `enum class Flag { DepthTestEnabled, DepthWriteEnabled, BlendEnabled, UsesStencilRef, UsesScissor }`

**作用与语义：**

- `QSSGRhiGraphicsPipelineState::Flag::DepthTestEnabled`: `0x1`
- `QSSGRhiGraphicsPipelineState::Flag::DepthWriteEnabled`: `0x2`
- `QSSGRhiGraphicsPipelineState::Flag::BlendEnabled`: `0x4`
- `QSSGRhiGraphicsPipelineState::Flag::UsesStencilRef`: `0x8`
- `QSSGRhiGraphicsPipelineState::Flag::UsesScissor`: `0x10`
Flags 类型是 QFlags<Flag> 的 typedef。它存储 Flag 值的按位或组合。

### `flags Flags`

**作用与语义：**

- `QSSGRhiGraphicsPipelineState::Flag::DepthTestEnabled`: `0x1`
- `QSSGRhiGraphicsPipelineState::Flag::DepthWriteEnabled`: `0x2`
- `QSSGRhiGraphicsPipelineState::Flag::BlendEnabled`: `0x4`
- `QSSGRhiGraphicsPipelineState::Flag::UsesStencilRef`: `0x8`
- `QSSGRhiGraphicsPipelineState::Flag::UsesScissor`: `0x10`
Flags 类型是 QFlags<Flag> 的 typedef。它存储 Flag 值的按位或组合。

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

`QSSGRhiGraphicsPipelineState` 所属机制类型：QML 属性绑定与场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
