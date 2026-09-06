# QSGRenderNode

> Qt 6.11.1 · Qt Quick

## 1. 先建立直觉

**一句话定位：** `QSGRenderNode` 是 Qt Quick 场景图渲染类型，负责节点、材质、纹理、几何或渲染状态。

**模块背景：** Qt Quick 面向 QML/场景图界面，提供可视项、动画、输入和高性能界面基础设施。

### 这是什么

`QSGRenderNode` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QSGRenderNode>`
- 继承自：QSGNode
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

**生命周期：** 场景图节点和材质的有效期受窗口、组件和渲染阶段控制；纹理、材质和几何通常要在正确的 render context 中创建/释放。节点被删除或场景图失效后，底层 GPU 资源不能继续使用。

**状态与结果：** 区分 GUI/同步阶段、渲染阶段、节点 dirty 状态、纹理状态和后端能力。改变节点属性通常要标记更新，不能在错误阶段直接修改资源；材质是否可用还受默认后端限制。

**线程与事件循环：** QSG 类型经常运行在 render thread，不能从 GUI 线程或后台线程随意读写。通过 QQuickItem 的同步接口在规定阶段交换数据，避免跨线程共享 GPU 资源。

## 3. 直接使用

需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。 使用时通常按这个过程组织：注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `struct RenderState`
- `enum RenderingFlag { BoundedRectRendering, DepthAwareRendering, OpaqueRendering, NoExternalRendering }`
- `flags RenderingFlags`
- `enum StateFlag { ViewportState, ScissorState, DepthState, StencilState, ColorState, …, RenderTargetState }`
- `flags StateFlags`

### 公有函数

- `virtual ~QSGRenderNode() override`
- `virtual QSGRenderNode::StateFlags changedStates() const`
- `const QSGClipNode * clipList() const`
- `(since 6.6) QRhiCommandBuffer * commandBuffer() const`
- `virtual QSGRenderNode::RenderingFlags flags() const`
- `qreal inheritedOpacity() const`
- `const QMatrix4x4 * matrix() const`
- `(since 6.0) virtual void prepare()`
- `(since 6.5) const QMatrix4x4 * projectionMatrix() const`
- `virtual QRectF rect() const`
- `virtual void releaseResources()`
- `virtual void render(const QSGRenderNode::RenderState *state) = 0`
- `(since 6.6) QRhiRenderTarget * renderTarget() const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QSGRenderNode::RenderingFlagflags QSGRenderNode::RenderingFlags`

**作用与语义：**

`flags()`返回的位掩码可能值。
- `QSGRenderNode::BoundedRectRendering`：`0x01`;表示`render()`的实现不会渲染超出`rect()`项目坐标报告的区域。这类节点实现可以带来更高效的渲染，具体取决于场景图后端。例如，当场景中所有渲染节点都设置了该标志时，`software`后端可以继续使用更优的部分更新路径。
- `QSGRenderNode::DepthAwareRendering`：`0x02`;表示`render()`的实现符合场景图预期，仅生成场景坐标中的Z值为0，然后通过从`RenderState::projectionMatrix()`和`matrix()`检索的矩阵进行转换，详见`render()`注释。此类节点实现可提升渲染效率，具体取决于场景图后端。例如，当场景中所有渲染节点都设置该标志时，批处理的OpenGL渲染器仍可继续使用更优路径。
- `QSGRenderNode::OpaqueRendering`：`0x04`;表示`render()`的实现会写出`rect()`报告的整个区域的不透明像素。默认情况下，渲染器必须假设`render()`也能输出半透明或完全透明的像素。设置该标志在某些情况下可以提升性能。
- `QSGRenderNode::NoExternalRendering`：`0x08`;表示`prepare()`和`render()`的实现仅使用`QRhi`族API，而非直接调用OpenGL、Vulkan或Metal等3D API。
RenderingFlags 类型是 QFlags 的 typedef<RenderingFlag>。它存储 RenderingFlag 值的 OR 组合。

### `enum QSGRenderNode::StateFlagflags QSGRenderNode::StateFlags`

**作用与语义：**

该枚举包含了从`changedStates()`返回的位掩码中可能使用的值。
- `QSGRenderNode::ViewportState`：`0x40`;视窗
- `QSGRenderNode::ScissorState`：`0x04`;开启剪刀测试的状态，剪刀矩形
- `QSGRenderNode::DepthState`：`0x01`;该值在第6量子中无影响。
- `QSGRenderNode::StencilState`：`0x02`;该值在第6量子中无效。
- `QSGRenderNode::ColorState`：`0x08`;该值在第6量子中无影响。
- `QSGRenderNode::BlendState`：`0x10`;该值在第6量子中无效。
- `QSGRenderNode::CullState`：`0x20`;该值在第6量子中无效。
- `QSGRenderNode::RenderTargetState`：`0x80`;该值在第6量子中无影响。
StateFlags 类型是 QFlags 的 typedef<StateFlag>。它存储 StateFlag 值的 OR 组合。

### `[override virtual noexcept] QSGRenderNode::~QSGRenderNode()`

**作用与语义：**

解构渲染节点。派生类预计会执行类似这里`releaseResources()`的清理。
对于`QRhi`和资源如`QRhiBuffer`、`QRhiTexture`、`QRhiGraphicsPipeline`等，使用智能指针（如std：：unique_ptr）通常是个好习惯，这通常可以避免实现结构化器，并使源代码更紧凑。不过请记住，实现`releaseResources()`（unique_ptrs上可能包含多个reset()调用，仍然很重要。

### `[virtual] QSGRenderNode::StateFlags QSGRenderNode::changedStates() const`

**作用与语义：**

该函数应返回一个遮罩，每个位代表由`render()`函数改变的图形状态。
注意：在Qt 6和基于`QRhi`的渲染中，唯一相关的值是`ViewportState`和`ScissorState`。其他值可以返回，但实际中会忽略。
- `ViewportState`：视口
- `ScissorState`：启用剪刀测试的状态，剪刀矩形
- `DepthState`：该值在第6量子无影响。
- `StencilState`：该值在第6量子中无影响。
- `ColorState`：该值在Qt 6中无影响。
- `BlendState`：该值在Qt 6中无影响。
- `CullState`：该值在第6量子中无影响。
- `RenderTargetState`：该值在Qt 6中无影响。
注意：`software`后端会暴露其`QPainter`，并在调用`render()`前后保存和恢复。因此，无需报告这里的任何状态变化。
默认实现返回0，意味着`render()`中没有发生任何相关状态的更改。
注意：该函数可在`render()`之前调用。

### `const QSGClipNode *QSGRenderNode::clipList() const`

**作用与语义：**

返回当前的剪辑列表。

### `[since 6.6] QRhiCommandBuffer *QSGRenderNode::commandBuffer() const`

**作用与语义：**

返回当前的命令缓冲区。

### `[virtual] QSGRenderNode::RenderingFlags QSGRenderNode::flags() const`

**作用与语义：**

返回描述该渲染节点行为的标志。
默认实现返回 0。

### `qreal QSGRenderNode::inheritedOpacity() const`

**作用与语义：**

返回当前有效不透明度。

### `const QMatrix4x4 *QSGRenderNode::matrix() const`

**作用与语义：**

返回当前模型视图矩阵的指针。

### `[virtual, since 6.0] void QSGRenderNode::prepare()`

**作用与语义：**

在帧准备阶段调用。每次调用`render()`前都会调用该函数。
与`render()`不同，该函数在场景图开始在底层命令缓冲区记录当前帧的渲染通道之前就被调用。这在使用图形 API（如 Vulkan）进行渲染时非常有用，因为需要在渲染通道前记录复制类操作。
默认实现是空的。
在实现使用`QRhi`渲染的`QSGRenderNode`时，通过`QQuickWindow::rhi()`查询`QQuickWindow`中的`QRhi`对象。要获得提交工作的`QRhiCommandBuffer`，请调用`commandBuffer()`。如需查询当前渲染目标的信息，请调用`renderTarget()`。详情请参见{Scene Graph - Custom QSGRenderNode}示例。

### `[since 6.5] const QMatrix4x4 *QSGRenderNode::projectionMatrix() const`

**作用与语义：**

返回指向当前投影矩阵的指针。
`render()`这与从`RenderState::projectionMatrix()`返回的矩阵相同。这个getter的存在是为了让`prepare()`也能查询投影矩阵。
使用现代图形 API 或 Qt 自身的图形抽象层时，很可能会想将`*projectionMatrix() * *matrix()`加载到统一缓冲区。不过这需要在渲染过程之外完成，`prepare()`。这就是为什么两个矩阵都可以直接从`QSGRenderNode`查询，无论是在`prepare()`还是在`render()`中。

### `[virtual] QRectF QSGRenderNode::rect() const`

**作用与语义：**

返回`render()`接触区域的物品坐标边界矩形。该值仅在包含`BoundedRectRendering`时使用，否则忽略`flags()`。
在`software`后端，将矩形与`BoundedRectRendering`结合报告尤其重要，否则场景中有渲染节点会触发全屏更新，跳过所有部分更新优化。
对于覆盖对应`QQuickItem`全部区域的渲染节点，返回值为 （0， 0， item->width()， item->height()）。
注意：节点也可以自由渲染超出物品宽度和高度所指定的边界，因为场景图节点不受`QQuickItem`几何体限制，只要该函数正确报告这一点。

### `[virtual] void QSGRenderNode::releaseResources()`

**作用与语义：**

当该节点必须立即释放所有自定义图形资源时，调用了该函数。如果该节点没有通过正在使用的图形 API 直接分配图形资源（缓冲区、纹理、渲染目标、围栏等），这里就无需处理。
未能释放所有自定义资源可能导致某些系统在图形设备丢失场景中出现错误行为，因为后续的图形系统初始化可能失败。
注意：一些场景图后端可能选择不调用该函数。因此，预期`QSGRenderNode`实现会在其解构器和 releaseResources() 中同时执行清理。
与解构函数不同，期望在调用 releaseResources() 后调用 `render()` 重新初始化所有所需资源。
使用 OpenGL 时，场景图的 OpenGL 上下文在调用 destructor 和该函数时都是最新的。

### `[pure virtual] void QSGRenderNode::render(const QSGRenderNode::RenderState *state)`

**作用与语义：**

该函数由渲染器调用，应通过`QRhi`或直接通过底层图形API（OpenGL、Direct3D等）直接调用命令来绘制该节点。
有效不透明度可以通过`inheritedOpacity()`恢复。
投影矩阵通过`state`获得，而模型-视图矩阵则可用`matrix()`取。合并矩阵即投影矩阵乘以模型-视图矩阵。投影矩阵确保场景中物品的正确堆叠。
使用提供的矩阵时，顶点数据的坐标系遵循通常的`QQuickItem`约定：左上为（0， 0），右下为对应`QQuickItem`的宽度()和高度()减一。例如，假设每个顶点坐标布局为两浮点（x-y），覆盖物体一半的三角形可以用逆时针方向指定为（宽度-1，高度-1）、（0,0）、（0，高度-1）。
注意：`QSGRenderNode` 是作为实现自定义 2D 或 2.5D Qt 快速项目的一种方式提供。它并非用于将真正的 3D 内容集成到 Qt 快速场景中。这种使用场景更适合其他集成自定义渲染的方法。
注意：`QSGRenderNode` 的表现明显优于基于纹理的方法（如 `QQuickRhiItem`），尤其是在片段处理能力有限的系统中。这是因为它避免了先渲染到纹理再绘制纹理四边形。相反，`QSGRenderNode`允许记录与场景图其他命令一致的绘制调用，避免额外的渲染目标以及可能昂贵的纹理和混合。
在调用函数之前，先计算剪辑信息。希望考虑剪裁的实现可以根据`state`中的信息设置剪刀或模板。模板缓冲区填充了必要的剪辑形状，但模板测试的实现取决于实现。
一些场景图后端，尤其是软件，不使用剪刀或模板。在那里，剪辑区域作为普通`QRegion`提供。
在实现使用`QRhi`渲染的`QSGRenderNode`时，通过`QQuickWindow::rhi()`查询`QQuickWindow`中的`QRhi`对象。要获得提交工作的`QRhiCommandBuffer`，请调用`commandBuffer()`。要查询关于当前渲染目标的信息，请调用`renderTarget()`。详情请参见{Scene Graph - Custom QSGRenderNode}示例。
在Qt 6及其基于`QRhi`的场景图渲染器中，调用该函数时不应对激活状态（OpenGL）做任何假设，即使使用OpenGL。调用该函数时，也不应假设命令列表/缓冲区绑定的流水线和动态状态。
注意：深度写入应被禁用。启用深度写入可能导致意想不到的结果，这取决于所使用的场景图后端和场景内容，因此需谨慎处理。
注意：在第6问中，`changedStates()`使用有限。更多信息请参见文档`changedStates()`。
对于某些图形API，包括直接使用`QRhi`时，可能需要额外重新实现`prepare()`，或者连接`QQuickWindow::beforeRendering()`信号。这些操作是在命令缓冲区录制渲染通道开始前调用/发出的（Vulkan的vkCmdBeginRenderPass，金属的경우 通过MTLRenderCommandEncoder开始编码）。在render()中无法通过此类API进行复制操作。相反，这些操作可以在`prepare()`或连接的foreRendering槽（使用DirectConnection）中完成。

### `[since 6.6] QRhiRenderTarget *QSGRenderNode::renderTarget() const`

**作用与语义：**

返回当前渲染目标。
这主要用于使 `prepare()` 和 `render()` 的实现能够使用 `QRhi` 访问 `QRhiRenderTarget` 的 `renderPassDescriptor` 或像素大小。
要构建 `QRhiGraphicsPipeline`，这意味着必须提供 `QRhiRenderPassDescriptor`，可从渲染目标查询 renderPassDescriptor。然而，需要注意的是，自定义 `QQuickItem` 和 `QSGRenderNode` 生命周期内渲染目标可能会变化。例如，考虑动态在该项目或其祖先上设置 `layer.enabled: true` 时会发生什么：这会触发渲染到纹理，而不是直接渲染到窗口，这意味着从那时起 `QSGRenderNode` 将使用不同的渲染目标。新的渲染目标可能会有不同的像素格式，这可能会导致已构建的图形管线不兼容。这可以通过以下逻辑来处理：

**官方示例：**

```cpp
 if (m_pipeline && renderTarget()->renderPassDescriptor()->serializedFormat() != m_renderPassFormat) {
     delete m_pipeline;
     m_pipeline = nullptr;
 }
 if (!m_pipeline) {
     // Build a new QRhiGraphicsPipeline.
     // ...
     // Store the serialized format for fast and simple comparisons later on.
     m_renderPassFormat = renderTarget()->renderPassDescriptor()->serializedFormat();
 }
```

### `struct RenderState`

**作用与语义：**

提供关于投影矩阵和裁剪的信息。
渲染状态包含渲染器在调用场景图后端命令时的信息。

### `enum RenderingFlag { BoundedRectRendering, DepthAwareRendering, OpaqueRendering, NoExternalRendering }`

**作用与语义：**

`flags()`返回的位掩码可能值。
- `QSGRenderNode::BoundedRectRendering`：`0x01`;表示`render()`的实现不会渲染超出`rect()`项目坐标报告的区域。这类节点实现可以带来更高效的渲染，具体取决于场景图后端。例如，当场景中所有渲染节点都设置了该标志时，`software`后端可以继续使用更优的部分更新路径。
- `QSGRenderNode::DepthAwareRendering`：`0x02`;表示`render()`的实现符合场景图预期，仅生成场景坐标中的Z值为0，然后通过从`RenderState::projectionMatrix()`和`matrix()`检索的矩阵进行转换，详见`render()`注释。此类节点实现可提升渲染效率，具体取决于场景图后端。例如，当场景中所有渲染节点都设置该标志时，批处理的OpenGL渲染器仍可继续使用更优路径。
- `QSGRenderNode::OpaqueRendering`：`0x04`;表示`render()`的实现会写出`rect()`报告的整个区域的不透明像素。默认情况下，渲染器必须假设`render()`也能输出半透明或完全透明的像素。设置该标志在某些情况下可以提升性能。
- `QSGRenderNode::NoExternalRendering`：`0x08`;表示`prepare()`和`render()`的实现仅使用`QRhi`族API，而非直接调用OpenGL、Vulkan或Metal等3D API。
RenderingFlags 类型是 QFlags 的 typedef<RenderingFlag>。它存储 RenderingFlag 值的 OR 组合。

### `flags RenderingFlags`

**作用与语义：**

`flags()`返回的位掩码可能值。
- `QSGRenderNode::BoundedRectRendering`：`0x01`;表示`render()`的实现不会渲染超出`rect()`项目坐标报告的区域。这类节点实现可以带来更高效的渲染，具体取决于场景图后端。例如，当场景中所有渲染节点都设置了该标志时，`software`后端可以继续使用更优的部分更新路径。
- `QSGRenderNode::DepthAwareRendering`：`0x02`;表示`render()`的实现符合场景图预期，仅生成场景坐标中的Z值为0，然后通过从`RenderState::projectionMatrix()`和`matrix()`检索的矩阵进行转换，详见`render()`注释。此类节点实现可提升渲染效率，具体取决于场景图后端。例如，当场景中所有渲染节点都设置该标志时，批处理的OpenGL渲染器仍可继续使用更优路径。
- `QSGRenderNode::OpaqueRendering`：`0x04`;表示`render()`的实现会写出`rect()`报告的整个区域的不透明像素。默认情况下，渲染器必须假设`render()`也能输出半透明或完全透明的像素。设置该标志在某些情况下可以提升性能。
- `QSGRenderNode::NoExternalRendering`：`0x08`;表示`prepare()`和`render()`的实现仅使用`QRhi`族API，而非直接调用OpenGL、Vulkan或Metal等3D API。
RenderingFlags 类型是 QFlags 的 typedef<RenderingFlag>。它存储 RenderingFlag 值的 OR 组合。

### `enum StateFlag { ViewportState, ScissorState, DepthState, StencilState, ColorState, …, RenderTargetState }`

**作用与语义：**

该枚举包含了从`changedStates()`返回的位掩码中可能使用的值。
- `QSGRenderNode::ViewportState`：`0x40`;视窗
- `QSGRenderNode::ScissorState`：`0x04`;开启剪刀测试的状态，剪刀矩形
- `QSGRenderNode::DepthState`：`0x01`;该值在第6量子中无影响。
- `QSGRenderNode::StencilState`：`0x02`;该值在第6量子中无效。
- `QSGRenderNode::ColorState`：`0x08`;该值在第6量子中无影响。
- `QSGRenderNode::BlendState`：`0x10`;该值在第6量子中无效。
- `QSGRenderNode::CullState`：`0x20`;该值在第6量子中无效。
- `QSGRenderNode::RenderTargetState`：`0x80`;该值在第6量子中无影响。
StateFlags 类型是 QFlags 的 typedef<StateFlag>。它存储 StateFlag 值的 OR 组合。

### `flags StateFlags`

**作用与语义：**

该枚举包含了从`changedStates()`返回的位掩码中可能使用的值。
- `QSGRenderNode::ViewportState`：`0x40`;视窗
- `QSGRenderNode::ScissorState`：`0x04`;开启剪刀测试的状态，剪刀矩形
- `QSGRenderNode::DepthState`：`0x01`;该值在第6量子中无影响。
- `QSGRenderNode::StencilState`：`0x02`;该值在第6量子中无效。
- `QSGRenderNode::ColorState`：`0x08`;该值在第6量子中无影响。
- `QSGRenderNode::BlendState`：`0x10`;该值在第6量子中无效。
- `QSGRenderNode::CullState`：`0x20`;该值在第6量子中无效。
- `QSGRenderNode::RenderTargetState`：`0x80`;该值在第6量子中无影响。
StateFlags 类型是 QFlags 的 typedef<StateFlag>。它存储 StateFlag 值的 OR 组合。

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

`QSGRenderNode` 所属机制类型：Qt Quick 场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
