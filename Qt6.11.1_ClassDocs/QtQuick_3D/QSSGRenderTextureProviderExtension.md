# QSSGRenderTextureProviderExtension

> Qt 6.11.1 · Qt Quick 3D

## 1. 先建立直觉

**一句话定位：** `QSSGRenderTextureProviderExtension` 是 QML 属性绑定与场景图机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Quick 3D 在 Qt Quick 中加入 3D 场景、相机、材质、模型和渲染能力。

### 这是什么

`QSSGRenderTextureProviderExtension` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QSSGRenderTextureProviderExtension>`
- 继承自：QSSGRenderExtension
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

### 配套与继承 API

- `virtual QSSGRenderExtension::RenderMode QSSGRenderExtension::mode() const`
- `virtual bool QSSGRenderExtension::prepareData(QSSGFrameData &data)`
- `virtual void QSSGRenderExtension::prepareRender(QSSGFrameData &data)`
- `virtual void QSSGRenderExtension::render(QSSGFrameData &data)`
- `virtual void QSSGRenderExtension::resetForFrame()`
- `virtual QSSGRenderExtension::RenderStage QSSGRenderExtension::stage() const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `virtual QSSGRenderExtension::RenderMode QSSGRenderExtension::mode() const`

**作用与语义：**

返回该扩展所使用的渲染模式。

### `virtual bool QSSGRenderExtension::prepareData(QSSGFrameData &data)`

**作用与语义：**

在收集场景`data`之后调用，但在当前帧中尚未完成任何渲染数据或渲染之前。
返回脏状态。如果有脏数据需要渲染，返回`true`。
注意：在准备和渲染阶段，引擎创建/收集的大部分数据是每帧的，应在下一帧开始时释放或假定发布。

### `virtual void QSSGRenderExtension::prepareRender(QSSGFrameData &data)`

**作用与语义：**

准备渲染数据。构建并收集渲染所需的`data`。在此之前安排的任何渲染扩展都已处理完毕。此外;任何模式`RenderMode::Standalone`的渲染扩展如果成功，将已全部完成。
注意：在准备和渲染阶段，引擎创建/收集的大部分数据是每帧的，应在下一帧开始时释放或假定发布。

### `virtual void QSSGRenderExtension::render(QSSGFrameData &data)`

**作用与语义：**

记录渲染通道。根据扩展`mode`该函数将在帧的准备或渲染阶段调用。
使用`data`获取渲染上下文，从中查询活动`QRhi`对象。

### `virtual void QSSGRenderExtension::resetForFrame()`

**作用与语义：**

每次新帧开始时调用。此时应清除前一帧的数据。

### `virtual QSSGRenderExtension::RenderStage QSSGRenderExtension::stage() const`

**作用与语义：**

返回 该渲染扩展将被使用的阶段。

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

`QSSGRenderTextureProviderExtension` 所属机制类型：QML 属性绑定与场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
