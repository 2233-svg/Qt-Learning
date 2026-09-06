# QSGMaterialShader::RenderState

> Qt 6.11.1 · Qt Quick

## 1. 先建立直觉

**一句话定位：** `QSGMaterialShader::RenderState` 是 Qt Quick 场景图渲染类型，负责节点、材质、纹理、几何或渲染状态。

**模块背景：** Qt Quick 面向 QML/场景图界面，提供可视项、动画、输入和高性能界面基础设施。

### 这是什么

`QSGMaterialShader::RenderState` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QSGMaterialShader>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

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

- `enum DirtyState { DirtyMatrix, DirtyOpacity, DirtyCachedMaterialData, DirtyAll }`
- `flags DirtyStates`

### 公有函数

- `QMatrix4x4 combinedMatrix() const`
- `float determinant() const`
- `float devicePixelRatio() const`
- `QRect deviceRect() const`
- `QSGMaterialShader::RenderState::DirtyStates dirtyStates() const`
- `bool isMatrixDirty() const`
- `bool isOpacityDirty() const`
- `QMatrix4x4 modelViewMatrix() const`
- `float opacity() const`
- `QMatrix4x4 projectionMatrix() const`
- `QRhiResourceUpdateBatch * resourceUpdateBatch()`
- `QRhi * rhi()`
- `QByteArray * uniformData()`
- `QRect viewportRect() const`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 17 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum RenderState::DirtyStateflags RenderState::DirtyStates`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QSGMaterialShader::RenderState` 暴露的类型声明 `Dirty、Stateflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:DirtyStateflags RenderState::DirtyStates`。
- 属性名：`RenderState`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMatrix4x4 RenderState::combinedMatrix() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGMaterialShader::RenderState::combinedMatrix` 用于计算、查询或取得与“combined、Matrix”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMatrix4x4`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMatrix4x4`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `float RenderState::determinant() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGMaterialShader::RenderState::determinant` 用于计算、查询或取得与“determinant”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `float`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`float`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `float RenderState::devicePixelRatio() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGMaterialShader::RenderState::devicePixelRatio` 用于计算、查询或取得与“device、Pixel、Ratio”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `float`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`float`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRect RenderState::deviceRect() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGMaterialShader::RenderState::deviceRect` 用于计算、查询或取得与“device、Rect”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRect`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRect`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSGMaterialShader::RenderState::DirtyStates RenderState::dirtyStates() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGMaterialShader::RenderState::dirtyStates` 用于计算、查询或取得与“dirty、States”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSGMaterialShader::RenderState::DirtyStates`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSGMaterialShader::RenderState::DirtyStates`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool RenderState::isMatrixDirty() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isMatrixDirty`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool RenderState::isOpacityDirty() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isOpacityDirty`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMatrix4x4 RenderState::modelViewMatrix() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGMaterialShader::RenderState::modelViewMatrix` 用于计算、查询或取得与“model、View、Matrix”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMatrix4x4`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMatrix4x4`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `float RenderState::opacity() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGMaterialShader::RenderState::opacity` 用于计算、查询或取得与“opacity”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `float`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`float`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMatrix4x4 RenderState::projectionMatrix() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGMaterialShader::RenderState::projectionMatrix` 用于计算、查询或取得与“projection、Matrix”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMatrix4x4`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMatrix4x4`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhiResourceUpdateBatch *RenderState::resourceUpdateBatch()`

**API 类别：** 成员函数说明

**中文解读：** `QSGMaterialShader::RenderState::resourceUpdateBatch` 用于计算、查询或取得与“resource、更新、Batch”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRhiResourceUpdateBatch *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhiResourceUpdateBatch *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhi *RenderState::rhi()`

**API 类别：** 成员函数说明

**中文解读：** `QSGMaterialShader::RenderState::rhi` 用于计算、查询或取得与“rhi”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRhi *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhi *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray *RenderState::uniformData()`

**API 类别：** 成员函数说明

**中文解读：** `QSGMaterialShader::RenderState::uniformData` 用于计算、查询或取得与“uniform、数据访问”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QByteArray *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRect RenderState::viewportRect() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGMaterialShader::RenderState::viewportRect` 用于计算、查询或取得与“viewport、Rect”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRect`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRect`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum DirtyState { DirtyMatrix, DirtyOpacity, DirtyCachedMaterialData, DirtyAll }`

**API 类别：** 公有类型

**中文解读：** 这是 `QSGMaterialShader::RenderState` 暴露的类型声明 `Dirty、State`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags DirtyStates`

**API 类别：** 公有类型

**中文解读：** 这是 `QSGMaterialShader::RenderState` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

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

`QSGMaterialShader::RenderState` 所属机制类型：Qt Quick 场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
