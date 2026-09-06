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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 20 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QSGRenderNode::RenderingFlagflags QSGRenderNode::RenderingFlags`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QSGRenderNode` 暴露的类型声明 `Rendering、Flagflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:RenderingFlagflags QSGRenderNode::RenderingFlags`。
- 属性名：`QSGRenderNode`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QSGRenderNode::StateFlagflags QSGRenderNode::StateFlags`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QSGRenderNode` 暴露的类型声明 `State、Flagflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:StateFlagflags QSGRenderNode::StateFlags`。
- 属性名：`QSGRenderNode`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual noexcept] QSGRenderNode::~QSGRenderNode()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSGRenderNode` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] QSGRenderNode::StateFlags QSGRenderNode::changedStates() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGRenderNode::changedStates` 用于计算、查询或取得与“changed、States”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSGRenderNode::StateFlags`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSGRenderNode::StateFlags`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QSGClipNode *QSGRenderNode::clipList() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGRenderNode::clipList` 用于计算、查询或取得与“clip、List”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QSGClipNode *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QSGClipNode *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] QRhiCommandBuffer *QSGRenderNode::commandBuffer() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGRenderNode::commandBuffer` 用于计算、查询或取得与“command、Buffer”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRhiCommandBuffer *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhiCommandBuffer *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] QSGRenderNode::RenderingFlags QSGRenderNode::flags() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGRenderNode::flags` 用于计算、查询或取得与“标志”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSGRenderNode::RenderingFlags`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSGRenderNode::RenderingFlags`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal QSGRenderNode::inheritedOpacity() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGRenderNode::inheritedOpacity` 用于计算、查询或取得与“inherited、Opacity”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QMatrix4x4 *QSGRenderNode::matrix() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGRenderNode::matrix` 用于计算、查询或取得与“matrix”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QMatrix4x4 *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QMatrix4x4 *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual, since 6.0] void QSGRenderNode::prepare()`

**API 类别：** 成员函数说明

**中文解读：** `QSGRenderNode::prepare` 用于执行与“prepare”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.5] const QMatrix4x4 *QSGRenderNode::projectionMatrix() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGRenderNode::projectionMatrix` 用于计算、查询或取得与“projection、Matrix”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QMatrix4x4 *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QMatrix4x4 *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] QRectF QSGRenderNode::rect() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGRenderNode::rect` 用于计算、查询或取得与“rect”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRectF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRectF`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] void QSGRenderNode::releaseResources()`

**API 类别：** 成员函数说明

**中文解读：** `QSGRenderNode::releaseResources` 用于执行与“释放、Resources”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] void QSGRenderNode::render(const QSGRenderNode::RenderState *state)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSGRenderNode` 的核心操作 `render`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `state`：类型为 `const QSGRenderNode::RenderState *`。没有默认值，调用时必须提供。状态值或状态对象；它描述调用时的阶段，不能把某个状态下有效的 API 用到其他阶段。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] QRhiRenderTarget *QSGRenderNode::renderTarget() const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSGRenderNode` 的核心操作 `renderTarget`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`QRhiRenderTarget *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `struct RenderState`

**API 类别：** 公有类型

**中文解读：** 这是 `QSGRenderNode` 的 `渲染、State` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum RenderingFlag { BoundedRectRendering, DepthAwareRendering, OpaqueRendering, NoExternalRendering }`

**API 类别：** 公有类型

**中文解读：** 这是 `QSGRenderNode` 暴露的类型声明 `Rendering、Flag`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags RenderingFlags`

**API 类别：** 公有类型

**中文解读：** 这是 `QSGRenderNode` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum StateFlag { ViewportState, ScissorState, DepthState, StencilState, ColorState, …, RenderTargetState }`

**API 类别：** 公有类型

**中文解读：** 这是 `QSGRenderNode` 暴露的类型声明 `State、Flag`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags StateFlags`

**API 类别：** 公有类型

**中文解读：** 这是 `QSGRenderNode` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

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
