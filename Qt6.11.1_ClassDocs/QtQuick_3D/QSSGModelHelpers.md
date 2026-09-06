# QSSGModelHelpers

> Qt 6.11.1 · Qt Quick 3D

## 1. 先建立直觉

**一句话定位：** `QSSGModelHelpers` 是 QML 属性绑定与场景图机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Quick 3D 在 Qt Quick 中加入 3D 场景、相机、材质、模型和渲染能力。

### 这是什么

`QSSGModelHelpers` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QSSGModelHelpers>`
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

### 静态公有成员

- `float getGlobalOpacity(const QSSGFrameData &frameData, QSSGNodeId model)`
- `float getGlobalOpacity(const QSSGFrameData &frameData, QSSGNodeId model, QSSGPrepContextId prepId)`
- `QMatrix4x4 getGlobalTransform(const QSSGFrameData &frameData, QSSGNodeId model, QSSGPrepContextId prepId = {})`
- `float getLocalOpacity(const QSSGFrameData &frameData, QSSGNodeId model)`
- `QMatrix4x4 getLocalTransform(const QSSGFrameData &frameData, QSSGNodeId model)`
- `void setGlobalOpacity(const QSSGFrameData &frameData, QSSGRenderablesId renderablesId, QSSGNodeId model, float opacity)`
- `void setGlobalTransform(const QSSGFrameData &frameData, QSSGRenderablesId renderablesId, QSSGNodeId model, const QMatrix4x4 &transform)`
- `void setModelMaterials(const QSSGFrameData &frameData, QSSGRenderablesId renderablesId, QSSGModelHelpers::MaterialList materials)`
- `void setModelMaterials(const QSSGFrameData &frameData, QSSGRenderablesId renderablesId, QSSGNodeId model, QSSGModelHelpers::MaterialList materials)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 9 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `[static] float QSSGModelHelpers::getGlobalOpacity(const QSSGFrameData &frameData, QSSGNodeId model)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `getGlobalOpacity`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`float`。
- 参数 `frameData`：类型为 `const QSSGFrameData &`。没有默认值，调用时必须提供。传入 `const QSSGFrameData &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `model`：类型为 `QSSGNodeId`。没有默认值，调用时必须提供。数据模型对象。要确认模型生命周期、线程归属、索引有效期和变化通知协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] float QSSGModelHelpers::getGlobalOpacity(const QSSGFrameData &frameData, QSSGNodeId model, QSSGPrepContextId prepId)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `getGlobalOpacity`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`float`。
- 参数 `frameData`：类型为 `const QSSGFrameData &`。没有默认值，调用时必须提供。传入 `const QSSGFrameData &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `model`：类型为 `QSSGNodeId`。没有默认值，调用时必须提供。数据模型对象。要确认模型生命周期、线程归属、索引有效期和变化通知协议。
- 参数 `prepId`：类型为 `QSSGPrepContextId`。没有默认值，调用时必须提供。传入 `QSSGPrepContextId` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QMatrix4x4 QSSGModelHelpers::getGlobalTransform(const QSSGFrameData &frameData, QSSGNodeId model, QSSGPrepContextId prepId = {})`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `getGlobalTransform`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QMatrix4x4`。
- 参数 `frameData`：类型为 `const QSSGFrameData &`。没有默认值，调用时必须提供。传入 `const QSSGFrameData &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `model`：类型为 `QSSGNodeId`。没有默认值，调用时必须提供。数据模型对象。要确认模型生命周期、线程归属、索引有效期和变化通知协议。
- 参数 `prepId`：类型为 `QSSGPrepContextId`。默认值为 `{}`。传入 `QSSGPrepContextId` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] float QSSGModelHelpers::getLocalOpacity(const QSSGFrameData &frameData, QSSGNodeId model)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `getLocalOpacity`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`float`。
- 参数 `frameData`：类型为 `const QSSGFrameData &`。没有默认值，调用时必须提供。传入 `const QSSGFrameData &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `model`：类型为 `QSSGNodeId`。没有默认值，调用时必须提供。数据模型对象。要确认模型生命周期、线程归属、索引有效期和变化通知协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QMatrix4x4 QSSGModelHelpers::getLocalTransform(const QSSGFrameData &frameData, QSSGNodeId model)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `getLocalTransform`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QMatrix4x4`。
- 参数 `frameData`：类型为 `const QSSGFrameData &`。没有默认值，调用时必须提供。传入 `const QSSGFrameData &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `model`：类型为 `QSSGNodeId`。没有默认值，调用时必须提供。数据模型对象。要确认模型生命周期、线程归属、索引有效期和变化通知协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] void QSSGModelHelpers::setGlobalOpacity(const QSSGFrameData &frameData, QSSGRenderablesId renderablesId, QSSGNodeId model, float opacity)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `setGlobalOpacity`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `frameData`：类型为 `const QSSGFrameData &`。没有默认值，调用时必须提供。传入 `const QSSGFrameData &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `renderablesId`：类型为 `QSSGRenderablesId`。没有默认值，调用时必须提供。传入 `QSSGRenderablesId` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `model`：类型为 `QSSGNodeId`。没有默认值，调用时必须提供。数据模型对象。要确认模型生命周期、线程归属、索引有效期和变化通知协议。
- 参数 `opacity`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] void QSSGModelHelpers::setGlobalTransform(const QSSGFrameData &frameData, QSSGRenderablesId renderablesId, QSSGNodeId model, const QMatrix4x4 &transform)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `setGlobalTransform`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `frameData`：类型为 `const QSSGFrameData &`。没有默认值，调用时必须提供。传入 `const QSSGFrameData &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `renderablesId`：类型为 `QSSGRenderablesId`。没有默认值，调用时必须提供。传入 `QSSGRenderablesId` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `model`：类型为 `QSSGNodeId`。没有默认值，调用时必须提供。数据模型对象。要确认模型生命周期、线程归属、索引有效期和变化通知协议。
- 参数 `transform`：类型为 `const QMatrix4x4 &`。没有默认值，调用时必须提供。传入 `const QMatrix4x4 &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] void QSSGModelHelpers::setModelMaterials(const QSSGFrameData &frameData, QSSGRenderablesId renderablesId, QSSGModelHelpers::MaterialList materials)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `setModelMaterials`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `frameData`：类型为 `const QSSGFrameData &`。没有默认值，调用时必须提供。传入 `const QSSGFrameData &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `renderablesId`：类型为 `QSSGRenderablesId`。没有默认值，调用时必须提供。传入 `QSSGRenderablesId` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `materials`：类型为 `QSSGModelHelpers::MaterialList`。没有默认值，调用时必须提供。传入 `QSSGModelHelpers::MaterialList` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] void QSSGModelHelpers::setModelMaterials(const QSSGFrameData &frameData, QSSGRenderablesId renderablesId, QSSGNodeId model, QSSGModelHelpers::MaterialList materials)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `setModelMaterials`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `frameData`：类型为 `const QSSGFrameData &`。没有默认值，调用时必须提供。传入 `const QSSGFrameData &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `renderablesId`：类型为 `QSSGRenderablesId`。没有默认值，调用时必须提供。传入 `QSSGRenderablesId` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `model`：类型为 `QSSGNodeId`。没有默认值，调用时必须提供。数据模型对象。要确认模型生命周期、线程归属、索引有效期和变化通知协议。
- 参数 `materials`：类型为 `QSSGModelHelpers::MaterialList`。没有默认值，调用时必须提供。传入 `QSSGModelHelpers::MaterialList` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

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

`QSSGModelHelpers` 所属机制类型：QML 属性绑定与场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
