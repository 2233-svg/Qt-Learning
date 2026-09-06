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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 8 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum class QSSGRenderHelpers::CreateFlagflags QSSGRenderHelpers::CreateFlags`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QSSGRenderHelpers` 暴露的类型声明 `class`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:CreateFlagflags QSSGRenderHelpers::CreateFlags`。
- 属性名：`QSSGRenderHelpers`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QSSGPrepResultId QSSGRenderHelpers::commit(const QSSGFrameData &frameData, QSSGPrepContextId prepId, QSSGRenderablesId renderablesId, float lodThreshold = 1.0f)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `commit`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QSSGPrepResultId`。
- 参数 `frameData`：类型为 `const QSSGFrameData &`。没有默认值，调用时必须提供。传入 `const QSSGFrameData &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `prepId`：类型为 `QSSGPrepContextId`。没有默认值，调用时必须提供。传入 `QSSGPrepContextId` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `renderablesId`：类型为 `QSSGRenderablesId`。没有默认值，调用时必须提供。传入 `QSSGRenderablesId` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `lodThreshold`：类型为 `float`。默认值为 `1.0f`。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QSSGRenderablesId QSSGRenderHelpers::createRenderables(const QSSGFrameData &frameData, QSSGPrepContextId prepId, const QSSGNodeIdList &nodes, QSSGRenderHelpers::CreateFlags flags = CreateFlag::None)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `createRenderables`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QSSGRenderablesId`。
- 参数 `frameData`：类型为 `const QSSGFrameData &`。没有默认值，调用时必须提供。传入 `const QSSGFrameData &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `prepId`：类型为 `QSSGPrepContextId`。没有默认值，调用时必须提供。传入 `QSSGPrepContextId` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `nodes`：类型为 `const QSSGNodeIdList &`。没有默认值，调用时必须提供。传入 `const QSSGNodeIdList &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `flags`：类型为 `QSSGRenderHelpers::CreateFlags`。默认值为 `CreateFlag::None`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QSSGPrepContextId QSSGRenderHelpers::prepareForRender(const QSSGFrameData &frameData, const QSSGRenderExtension &ext, QSSGCameraId cameraId, quint32 slot = 0)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `prepareForRender`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QSSGPrepContextId`。
- 参数 `frameData`：类型为 `const QSSGFrameData &`。没有默认值，调用时必须提供。传入 `const QSSGFrameData &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `ext`：类型为 `const QSSGRenderExtension &`。没有默认值，调用时必须提供。传入 `const QSSGRenderExtension &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cameraId`：类型为 `QSSGCameraId`。没有默认值，调用时必须提供。传入 `QSSGCameraId` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `slot`：类型为 `quint32`。默认值为 `0`。槽函数或回调。要确认签名、执行线程、上下文生命周期和是否可能阻塞。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] void QSSGRenderHelpers::prepareRenderables(const QSSGFrameData &frameData, QSSGPrepResultId prepId, QRhiRenderPassDescriptor *renderPassDescriptor, QSSGRhiGraphicsPipelineState &ps, QSSGRenderablesFilters filter = QSSGRenderablesFilter::All)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `prepareRenderables`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `frameData`：类型为 `const QSSGFrameData &`。没有默认值，调用时必须提供。传入 `const QSSGFrameData &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `prepId`：类型为 `QSSGPrepResultId`。没有默认值，调用时必须提供。传入 `QSSGPrepResultId` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `renderPassDescriptor`：类型为 `QRhiRenderPassDescriptor *`。没有默认值，调用时必须提供。传入 `QRhiRenderPassDescriptor *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `ps`：类型为 `QSSGRhiGraphicsPipelineState &`。没有默认值，调用时必须提供。传入 `QSSGRhiGraphicsPipelineState &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `filter`：类型为 `QSSGRenderablesFilters`。默认值为 `QSSGRenderablesFilter::All`。过滤条件、匹配器或过滤标志；要确认它作用于显示结果、输入数据还是事件传播。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] void QSSGRenderHelpers::renderRenderables(const QSSGFrameData &frameData, QSSGPrepResultId prepId)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `renderRenderables`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `frameData`：类型为 `const QSSGFrameData &`。没有默认值，调用时必须提供。传入 `const QSSGFrameData &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `prepId`：类型为 `QSSGPrepResultId`。没有默认值，调用时必须提供。传入 `QSSGPrepResultId` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum class CreateFlag { None, Recurse, Steal }`

**API 类别：** 公有类型

**中文解读：** 这是 `QSSGRenderHelpers` 暴露的类型声明 `class`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags CreateFlags`

**API 类别：** 公有类型

**中文解读：** 这是 `QSSGRenderHelpers` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

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
