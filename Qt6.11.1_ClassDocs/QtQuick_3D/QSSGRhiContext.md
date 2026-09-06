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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 11 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `void QSSGRhiContext::checkAndAdjustForNPoT(QRhiTexture *texture, QSSGRhiSamplerDescription *samplerDescription)`

**API 类别：** 成员函数说明

**中文解读：** `QSSGRhiContext::checkAndAdjustForNPoT` 用于执行与“check、And、Adjust、For、N、Po、T”相关的操作。调用时要先确认当前状态和 `texture`、`samplerDescription` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `texture`：类型为 `QRhiTexture *`。没有默认值，调用时必须提供。传入 `QRhiTexture *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `samplerDescription`：类型为 `QSSGRhiSamplerDescription *`。没有默认值，调用时必须提供。传入 `QSSGRhiSamplerDescription *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhiCommandBuffer *QSSGRhiContext::commandBuffer() const`

**API 类别：** 成员函数说明

**中文解读：** `QSSGRhiContext::commandBuffer` 用于计算、查询或取得与“command、Buffer”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRhiCommandBuffer *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhiCommandBuffer *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhiCommandBuffer::BeginPassFlags QSSGRhiContext::commonPassFlags() const`

**API 类别：** 成员函数说明

**中文解读：** `QSSGRhiContext::commonPassFlags` 用于计算、查询或取得与“common、Pass、标志”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRhiCommandBuffer::BeginPassFlags`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhiCommandBuffer::BeginPassFlags`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhiTexture *QSSGRhiContext::dummyTexture(QRhiTexture::Flags flags, QRhiResourceUpdateBatch *rub, const QSize &size = QSize(64, 64), const QColor &fillColor = Qt::black, int arraySize = 0)`

**API 类别：** 成员函数说明

**中文解读：** `QSSGRhiContext::dummyTexture` 用于计算、查询或取得与“dummy、Texture”相关的操作。调用时要先确认当前状态和 `flags`、`rub`、`size`、`fillColor`、`arraySize` 的有效范围；返回类型是 `QRhiTexture *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhiTexture *`。
- 参数 `flags`：类型为 `QRhiTexture::Flags`。没有默认值，调用时必须提供。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。
- 参数 `rub`：类型为 `QRhiResourceUpdateBatch *`。没有默认值，调用时必须提供。传入 `QRhiResourceUpdateBatch *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `size`：类型为 `const QSize &`。默认值为 `QSize(64, 64)`。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。
- 参数 `fillColor`：类型为 `const QColor &`。默认值为 `Qt::black`。传入 `const QColor &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `arraySize`：类型为 `int`。默认值为 `0`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QSSGRhiContext::isValid() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isValid`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QSSGRhiContext::mainPassSampleCount() const`

**API 类别：** 成员函数说明

**中文解读：** `QSSGRhiContext::mainPassSampleCount` 用于计算、查询或取得与“main、Pass、Sample、数量统计”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QSSGRhiContext::mainPassViewCount() const`

**API 类别：** 成员函数说明

**中文解读：** `QSSGRhiContext::mainPassViewCount` 用于计算、查询或取得与“main、Pass、View、数量统计”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhiRenderPassDescriptor *QSSGRhiContext::mainRenderPassDescriptor() const`

**API 类别：** 成员函数说明

**中文解读：** `QSSGRhiContext::mainRenderPassDescriptor` 用于计算、查询或取得与“main、渲染、Pass、Descriptor”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRhiRenderPassDescriptor *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhiRenderPassDescriptor *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhiRenderTarget *QSSGRhiContext::renderTarget() const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSSGRhiContext` 的核心操作 `renderTarget`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`QRhiRenderTarget *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhi *QSSGRhiContext::rhi() const`

**API 类别：** 成员函数说明

**中文解读：** `QSSGRhiContext::rhi` 用于计算、查询或取得与“rhi”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRhi *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhi *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRhiSampler *QSSGRhiContext::sampler(const QSSGRhiSamplerDescription &samplerDescription)`

**API 类别：** 成员函数说明

**中文解读：** `QSSGRhiContext::sampler` 用于计算、查询或取得与“sampler”相关的操作。调用时要先确认当前状态和 `samplerDescription` 的有效范围；返回类型是 `QRhiSampler *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhiSampler *`。
- 参数 `samplerDescription`：类型为 `const QSSGRhiSamplerDescription &`。没有默认值，调用时必须提供。传入 `const QSSGRhiSamplerDescription &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

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

`QSSGRhiContext` 所属机制类型：QML 属性绑定与场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
