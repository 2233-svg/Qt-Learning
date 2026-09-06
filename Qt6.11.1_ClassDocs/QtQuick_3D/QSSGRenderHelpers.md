# QSSGRenderHelpers

> Qt 6.11.1 · Qt Quick 3D

## 1. 先建立直觉

**一句话定位：** `QSSGRenderHelpers` 是 QML 属性绑定与场景图机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Quick 3D 在 Qt Quick 中加入 3D 场景、相机、材质、模型和渲染能力。

### 这是什么

`QSSGRenderHelpers` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QSSGRenderHelpers>`
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

- `enum class CreateFlag { None, Recurse, Steal }`
- `flags CreateFlags`

### 静态公有成员

- `QSSGPrepResultId commit(const QSSGFrameData &frameData, QSSGPrepContextId prepId, QSSGRenderablesId renderablesId, float lodThreshold = 1.0f)`
- `QSSGRenderablesId createRenderables(const QSSGFrameData &frameData, QSSGPrepContextId prepId, const QSSGNodeIdList &nodes, QSSGRenderHelpers::CreateFlags flags = CreateFlag::None)`
- `QSSGPrepContextId prepareForRender(const QSSGFrameData &frameData, const QSSGRenderExtension &ext, QSSGCameraId cameraId, quint32 slot = 0)`
- `void prepareRenderables(const QSSGFrameData &frameData, QSSGPrepResultId prepId, QRhiRenderPassDescriptor *renderPassDescriptor, QSSGRhiGraphicsPipelineState &ps, QSSGRenderablesFilters filter = QSSGRenderablesFilter::All)`
- `void renderRenderables(const QSSGFrameData &frameData, QSSGPrepResultId prepId)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum class QSSGRenderHelpers::CreateFlagflags QSSGRenderHelpers::CreateFlags`

**作用与语义：**

- `QSSGRenderHelpers::CreateFlag::None`: `0`；默认值。仅为指定的节点创建 Renderables
- `QSSGRenderHelpers::CreateFlag::Recurse`: `0x1`；为每个节点及其子节点创建 Renderables
- `QSSGRenderHelpers::CreateFlag::Steal`: `0x2`；从引擎获取 Renderables，并且不会被 `QtQuick3D` 渲染
注意：调用 `QSSGRenderHelpers::createRenderables()` 而未设置 {QSSGRenderHelpers::CreateFlag::Steal}{Steal} 标志意味着节点会被复制，并且 `QtQuick3D` 将像正常情况一样渲染它的节点副本。
CreateFlags 类型是 QFlags<CreateFlag> 的 typedef。它存储 CreateFlag 值的按位或组合。

### `[static] QSSGPrepResultId QSSGRenderHelpers::commit(const QSSGFrameData &frameData, QSSGPrepContextId prepId, QSSGRenderablesId renderablesId, float lodThreshold = 1.0f)`

**作用与语义：**

一旦对可渲染文件完成必要的更改，数据就可以标记为准备好提交渲染器。
返回 id 到准备结果。
`frameData`，`prepId`，`renderablesId`，`lodThreshold`。

### `[static] QSSGRenderablesId QSSGRenderHelpers::createRenderables(const QSSGFrameData &frameData, QSSGPrepContextId prepId, const QSSGNodeIdList &nodes, QSSGRenderHelpers::CreateFlags flags = CreateFlag::None)`

**作用与语义：**

获取一个节点 id 列表，创建可渲染的可渲染节点，渲染器可以进一步处理。如果列表中没有节点或没有可渲染节点，返回的 id 将无效。
默认情况下，该函数不会递归，且在列表中包含了`nodes`的子节点。通过在`flags`参数中传递`Recurse`标志，可以实现递归的启用。
返回一个id到已创建的可渲染文件。
`frameData`，`prepId`。

### `[static] QSSGPrepContextId QSSGRenderHelpers::prepareForRender(const QSSGFrameData &frameData, const QSSGRenderExtension &ext, QSSGCameraId cameraId, quint32 slot = 0)`

**作用与语义：**

prepareForRender() 创建上下文，用于收集和存储与该渲染扩展相关的渲染数据信息。
如果同一节点需要多次渲染但属性不同，例如不同的材质或相机，则需要新的上下文。为一个扩展创建多个上下文时可以使用`slot`参数。默认上下文在槽位0中创建。
将ID返回到准备上下文。
`frameData`，`ext`，`cameraId`。

### `[static] void QSSGRenderHelpers::prepareRenderables(const QSSGFrameData &frameData, QSSGPrepResultId prepId, QRhiRenderPassDescriptor *renderPassDescriptor, QSSGRhiGraphicsPipelineState &ps, QSSGRenderablesFilters filter = QSSGRenderablesFilter::All)`

**作用与语义：**

在调用`renderRenderables`之前，先准备好渲染所需的绘制调用数据。
返回 id 到准备结果。
`frameData`，`renderPassDescriptor`，`ps`，`prepId`，`filter`。

### `[static] void QSSGRenderHelpers::renderRenderables(const QSSGFrameData &frameData, QSSGPrepResultId prepId)`

**作用与语义：**

渲染可渲染的可渲染。
`frameData`，`prepId`。

### `enum class CreateFlag { None, Recurse, Steal }`

**作用与语义：**

- `QSSGRenderHelpers::CreateFlag::None`: `0`；默认值。仅为指定的节点创建 Renderables
- `QSSGRenderHelpers::CreateFlag::Recurse`: `0x1`；为每个节点及其子节点创建 Renderables
- `QSSGRenderHelpers::CreateFlag::Steal`: `0x2`；从引擎获取 Renderables，并且不会被 `QtQuick3D` 渲染
注意：调用 `QSSGRenderHelpers::createRenderables()` 而未设置 {QSSGRenderHelpers::CreateFlag::Steal}{Steal} 标志意味着节点会被复制，并且 `QtQuick3D` 将像正常情况一样渲染它的节点副本。
CreateFlags 类型是 QFlags<CreateFlag> 的 typedef。它存储 CreateFlag 值的按位或组合。

### `flags CreateFlags`

**作用与语义：**

- `QSSGRenderHelpers::CreateFlag::None`: `0`；默认值。仅为指定的节点创建 Renderables
- `QSSGRenderHelpers::CreateFlag::Recurse`: `0x1`；为每个节点及其子节点创建 Renderables
- `QSSGRenderHelpers::CreateFlag::Steal`: `0x2`；从引擎获取 Renderables，并且不会被 `QtQuick3D` 渲染
注意：调用 `QSSGRenderHelpers::createRenderables()` 而未设置 {QSSGRenderHelpers::CreateFlag::Steal}{Steal} 标志意味着节点会被复制，并且 `QtQuick3D` 将像正常情况一样渲染它的节点副本。
CreateFlags 类型是 QFlags<CreateFlag> 的 typedef。它存储 CreateFlag 值的按位或组合。

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

`QSSGRenderHelpers` 所属机制类型：QML 属性绑定与场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
