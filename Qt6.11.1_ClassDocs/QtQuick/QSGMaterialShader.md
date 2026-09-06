# QSGMaterialShader

> Qt 6.11.1 · Qt Quick

## 1. 先建立直觉

**一句话定位：** `QSGMaterialShader` 是 Qt Quick 场景图渲染类型，负责节点、材质、纹理、几何或渲染状态。

**模块背景：** Qt Quick 面向 QML/场景图界面，提供可视项、动画、输入和高性能界面基础设施。

### 这是什么

`QSGMaterialShader` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QSGMaterialShader>`
- 继承自：未在类页中列出
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

- `struct GraphicsPipelineState`
- `class RenderState`
- `enum Flag { UpdatesGraphicsPipelineState }`
- `flags Flags`

### 公有函数

- `QSGMaterialShader()`
- `(since 6.4) int combinedImageSamplerCount(int binding) const`
- `QSGMaterialShader::Flags flags() const`
- `void setFlag(QSGMaterialShader::Flags flags, bool on = true)`
- `void setFlags(QSGMaterialShader::Flags flags)`
- `virtual bool updateGraphicsPipelineState(QSGMaterialShader::RenderState &state, QSGMaterialShader::GraphicsPipelineState *ps, QSGMaterial *newMaterial, QSGMaterial *oldMaterial)`
- `virtual void updateSampledImage(QSGMaterialShader::RenderState &state, int binding, QSGTexture **texture, QSGMaterial *newMaterial, QSGMaterial *oldMaterial)`
- `virtual bool updateUniformData(QSGMaterialShader::RenderState &state, QSGMaterial *newMaterial, QSGMaterial *oldMaterial)`

### 保护函数

- `void setShader(QSGMaterialShader::Stage stage, const QShader &shader)`
- `void setShaderFileName(QSGMaterialShader::Stage stage, const QString &filename)`
- `(since 6.8) void setShaderFileName(QSGMaterialShader::Stage stage, const QString &filename, int viewCount)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 16 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QSGMaterialShader::Flagflags QSGMaterialShader::Flags`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QSGMaterialShader` 暴露的类型声明 `Flagflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Flagflags QSGMaterialShader::Flags`。
- 属性名：`QSGMaterialShader`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSGMaterialShader::QSGMaterialShader()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSGMaterialShader` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.4] int QSGMaterialShader::combinedImageSamplerCount(int binding) const`

**API 类别：** 成员函数说明

**中文解读：** `QSGMaterialShader::combinedImageSamplerCount` 用于计算、查询或取得与“combined、Image、Sampler、数量统计”相关的操作。调用时要先确认当前状态和 `binding` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `binding`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSGMaterialShader::Flags QSGMaterialShader::flags() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGMaterialShader::flags` 用于计算、查询或取得与“标志”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSGMaterialShader::Flags`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSGMaterialShader::Flags`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSGMaterialShader::setFlag(QSGMaterialShader::Flags flags, bool on = true)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFlag`。调用它会改变 `QSGMaterialShader` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `flags`：类型为 `QSGMaterialShader::Flags`。没有默认值，调用时必须提供。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。
- 参数 `on`：类型为 `bool`。默认值为 `true`。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSGMaterialShader::setFlags(QSGMaterialShader::Flags flags)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFlags`。调用它会改变 `QSGMaterialShader` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `flags`：类型为 `QSGMaterialShader::Flags`。没有默认值，调用时必须提供。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] void QSGMaterialShader::setShader(QSGMaterialShader::Stage stage, const QShader &shader)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setShader`。调用它会改变 `QSGMaterialShader` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `stage`：类型为 `QSGMaterialShader::Stage`。没有默认值，调用时必须提供。传入 `QSGMaterialShader::Stage` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `shader`：类型为 `const QShader &`。没有默认值，调用时必须提供。传入 `const QShader &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] void QSGMaterialShader::setShaderFileName(QSGMaterialShader::Stage stage, const QString &filename)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setShaderFileName`。调用它会改变 `QSGMaterialShader` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `stage`：类型为 `QSGMaterialShader::Stage`。没有默认值，调用时必须提供。传入 `QSGMaterialShader::Stage` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `filename`：类型为 `const QString &`。没有默认值，调用时必须提供。文件名或路径。优先使用 Qt 的路径 API 拼接和规范化，不要手写平台分隔符。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected, since 6.8] void QSGMaterialShader::setShaderFileName(QSGMaterialShader::Stage stage, const QString &filename, int viewCount)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setShaderFileName`。调用它会改变 `QSGMaterialShader` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `stage`：类型为 `QSGMaterialShader::Stage`。没有默认值，调用时必须提供。传入 `QSGMaterialShader::Stage` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `filename`：类型为 `const QString &`。没有默认值，调用时必须提供。文件名或路径。优先使用 Qt 的路径 API 拼接和规范化，不要手写平台分隔符。
- 参数 `viewCount`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] bool QSGMaterialShader::updateGraphicsPipelineState(QSGMaterialShader::RenderState &state, QSGMaterialShader::GraphicsPipelineState *ps, QSGMaterial *newMaterial, QSGMaterial *oldMaterial)`

**API 类别：** 成员函数说明

**中文解读：** `QSGMaterialShader::updateGraphicsPipelineState` 用于计算、查询或取得与“更新、Graphics、Pipeline、State”相关的操作。调用时要先确认当前状态和 `state`、`ps`、`newMaterial`、`oldMaterial` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `state`：类型为 `QSGMaterialShader::RenderState &`。没有默认值，调用时必须提供。状态值或状态对象；它描述调用时的阶段，不能把某个状态下有效的 API 用到其他阶段。
- 参数 `ps`：类型为 `QSGMaterialShader::GraphicsPipelineState *`。没有默认值，调用时必须提供。传入 `QSGMaterialShader::GraphicsPipelineState *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `newMaterial`：类型为 `QSGMaterial *`。没有默认值，调用时必须提供。传入 `QSGMaterial *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `oldMaterial`：类型为 `QSGMaterial *`。没有默认值，调用时必须提供。传入 `QSGMaterial *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] void QSGMaterialShader::updateSampledImage(QSGMaterialShader::RenderState &state, int binding, QSGTexture **texture, QSGMaterial *newMaterial, QSGMaterial *oldMaterial)`

**API 类别：** 成员函数说明

**中文解读：** `QSGMaterialShader::updateSampledImage` 用于执行与“更新、Sampled、Image”相关的操作。调用时要先确认当前状态和 `state`、`binding`、`texture`、`newMaterial`、`oldMaterial` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `state`：类型为 `QSGMaterialShader::RenderState &`。没有默认值，调用时必须提供。状态值或状态对象；它描述调用时的阶段，不能把某个状态下有效的 API 用到其他阶段。
- 参数 `binding`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `texture`：类型为 `QSGTexture **`。没有默认值，调用时必须提供。传入 `QSGTexture **` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `newMaterial`：类型为 `QSGMaterial *`。没有默认值，调用时必须提供。传入 `QSGMaterial *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `oldMaterial`：类型为 `QSGMaterial *`。没有默认值，调用时必须提供。传入 `QSGMaterial *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] bool QSGMaterialShader::updateUniformData(QSGMaterialShader::RenderState &state, QSGMaterial *newMaterial, QSGMaterial *oldMaterial)`

**API 类别：** 成员函数说明

**中文解读：** `QSGMaterialShader::updateUniformData` 用于计算、查询或取得与“更新、Uniform、数据访问”相关的操作。调用时要先确认当前状态和 `state`、`newMaterial`、`oldMaterial` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `state`：类型为 `QSGMaterialShader::RenderState &`。没有默认值，调用时必须提供。状态值或状态对象；它描述调用时的阶段，不能把某个状态下有效的 API 用到其他阶段。
- 参数 `newMaterial`：类型为 `QSGMaterial *`。没有默认值，调用时必须提供。传入 `QSGMaterial *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `oldMaterial`：类型为 `QSGMaterial *`。没有默认值，调用时必须提供。传入 `QSGMaterial *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `struct GraphicsPipelineState`

**API 类别：** 公有类型

**中文解读：** 这是 `QSGMaterialShader` 的 `Graphics、Pipeline、State` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `class RenderState`

**API 类别：** 公有类型

**中文解读：** 这是 `QSGMaterialShader` 暴露的类型声明 `渲染、State`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum Flag { UpdatesGraphicsPipelineState }`

**API 类别：** 公有类型

**中文解读：** 这是 `QSGMaterialShader` 暴露的类型声明 `Flag`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags Flags`

**API 类别：** 公有类型

**中文解读：** 这是 `QSGMaterialShader` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

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

`QSGMaterialShader` 所属机制类型：Qt Quick 场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
