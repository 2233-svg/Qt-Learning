# QQuickPaintedItem

> Qt 6.11.1 · Qt Quick

## 1. 先建立直觉

**一句话定位：** `QQuickPaintedItem` 是 QML 属性绑定与场景图机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Quick 面向 QML/场景图界面，提供可视项、动画、输入和高性能界面基础设施。

### 这是什么

`QQuickPaintedItem` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QQuickPaintedItem>`
- 继承自：QQuickItem
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Quick)
target_link_libraries(mytarget PRIVATE Qt6::Quick)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

### 状态、生命周期和线程

**生命周期：** QML 引擎、上下文和对象所有权必须明确。由 QML 创建的对象通常由引擎管理；通过 context property 或 C++ 暴露的对象要决定由 C++ 持有还是转移给 QML，不能让绑定指向悬空对象。

**状态与结果：** 属性绑定和直接赋值不是一回事：直接给被绑定属性赋值通常会打破原有绑定。C++ 属性要有正确的 notify signal，QML 才能在数据变化时更新；信号参数和属性当前值要保持一致。

**线程与事件循环：** 大多数 QML 对象和 GUI 操作在 GUI 线程，场景图渲染还可能在 render thread。不要在渲染阶段调用 GUI 对象 API；后台数据通过线程安全的信号/槽边界送入 QML。

## 3. 直接使用

需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。 使用时通常按这个过程组织：注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

```cpp
// C++ 侧暴露属性/信号后，在 QML 中建立绑定。
// 变化时发出 notify signal，避免在绑定表达式中直接修改状态。
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum PerformanceHint { FastFBOResizing }`
- `flags PerformanceHints`
- `enum RenderTarget { Image, FramebufferObject, InvertedYFramebufferObject }`

### 属性

- `fillColor : QColor`
- `renderTarget : RenderTarget`
- `textureSize : QSize`

### 公有函数

- `QQuickPaintedItem(QQuickItem *parent = nullptr)`
- `virtual ~QQuickPaintedItem() override`
- `bool antialiasing() const`
- `QColor fillColor() const`
- `bool mipmap() const`
- `bool opaquePainting() const`
- `virtual void paint(QPainter *painter) = 0`
- `QQuickPaintedItem::PerformanceHints performanceHints() const`
- `QQuickPaintedItem::RenderTarget renderTarget() const`
- `void setAntialiasing(bool enable)`
- `void setFillColor(const QColor &)`
- `void setMipmap(bool enable)`
- `void setOpaquePainting(bool opaque)`
- `void setPerformanceHint(QQuickPaintedItem::PerformanceHint hint, bool enabled = true)`
- `void setPerformanceHints(QQuickPaintedItem::PerformanceHints hints)`
- `void setRenderTarget(QQuickPaintedItem::RenderTarget target)`
- `void setTextureSize(const QSize &size)`
- `QSize textureSize() const`
- `void update(const QRect &rect = QRect())`

### 重实现的公有函数

- `virtual bool isTextureProvider() const override`
- `virtual QSGTextureProvider * textureProvider() const override`

### 信号

- `void fillColorChanged()`
- `void renderTargetChanged()`
- `void textureSizeChanged()`

### 重实现的保护函数

- `virtual void itemChange(QQuickItem::ItemChange change, const QQuickItem::ItemChangeData &value) override`
- `virtual void releaseResources() override`
- `virtual QSGNode * updatePaintNode(QSGNode *oldNode, QQuickItem::UpdatePaintNodeData *data) override`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 34 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QQuickPaintedItem::PerformanceHintflags QQuickPaintedItem::PerformanceHints`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QQuickPaintedItem` 暴露的类型声明 `Performance、Hintflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:PerformanceHintflags QQuickPaintedItem::PerformanceHints`。
- 属性名：`QQuickPaintedItem`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QQuickPaintedItem::RenderTarget`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QQuickPaintedItem` 暴露的类型声明 `渲染、目标`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:RenderTarget`。
- 属性名：`QQuickPaintedItem`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `fillColor : QColor`

**API 类别：** 属性说明

**中文解读：** 这是 `QQuickPaintedItem` 的配置属性。初始化或状态切换时通过 `setFillColor(...)` 设置，之后用 `fillColor()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QColor`。
- 属性名：`fillColor`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `renderTarget : RenderTarget`

**API 类别：** 属性说明

**中文解读：** 这是 `QQuickPaintedItem` 的配置属性。初始化或状态切换时通过 `setRenderTarget(...)` 设置，之后用 `renderTarget()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`RenderTarget`。
- 属性名：`renderTarget`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `textureSize : QSize`

**API 类别：** 属性说明

**中文解读：** 这是 `QQuickPaintedItem` 的配置属性。初始化或状态切换时通过 `setTextureSize(...)` 设置，之后用 `textureSize()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QSize`。
- 属性名：`textureSize`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QQuickPaintedItem::QQuickPaintedItem(QQuickItem *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QQuickPaintedItem` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `parent`：类型为 `QQuickItem *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual noexcept] QQuickPaintedItem::~QQuickPaintedItem()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QQuickPaintedItem` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QQuickPaintedItem::antialiasing() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuickPaintedItem::antialiasing` 用于计算、查询或取得与“antialiasing”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QQuickPaintedItem::isTextureProvider() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isTextureProvider`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QQuickPaintedItem::itemChange(QQuickItem::ItemChange change, const QQuickItem::ItemChangeData &value)`

**API 类别：** 成员函数说明

**中文解读：** `QQuickPaintedItem::itemChange` 用于执行与“项目访问、Change”相关的操作。调用时要先确认当前状态和 `change`、`value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `change`：类型为 `QQuickItem::ItemChange`。没有默认值，调用时必须提供。传入 `QQuickItem::ItemChange` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const QQuickItem::ItemChangeData &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QQuickPaintedItem::mipmap() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuickPaintedItem::mipmap` 用于计算、查询或取得与“mipmap”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QQuickPaintedItem::opaquePainting() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuickPaintedItem::opaquePainting` 用于计算、查询或取得与“opaque、Painting”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] void QQuickPaintedItem::paint(QPainter *painter)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QQuickPaintedItem` 的核心操作 `paint`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `painter`：类型为 `QPainter *`。没有默认值，调用时必须提供。绘制上下文。要确认它已经绑定有效绘制设备，并处于允许绘制的阶段。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QQuickPaintedItem::PerformanceHints QQuickPaintedItem::performanceHints() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuickPaintedItem::performanceHints` 用于计算、查询或取得与“performance、Hints”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QQuickPaintedItem::PerformanceHints`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QQuickPaintedItem::PerformanceHints`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QQuickPaintedItem::releaseResources()`

**API 类别：** 成员函数说明

**中文解读：** `QQuickPaintedItem::releaseResources` 用于执行与“释放、Resources”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QQuickPaintedItem::setAntialiasing(bool enable)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setAntialiasing`。调用它会改变 `QQuickPaintedItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enable`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QQuickPaintedItem::setMipmap(bool enable)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setMipmap`。调用它会改变 `QQuickPaintedItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enable`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QQuickPaintedItem::setOpaquePainting(bool opaque)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setOpaquePainting`。调用它会改变 `QQuickPaintedItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `opaque`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QQuickPaintedItem::setPerformanceHint(QQuickPaintedItem::PerformanceHint hint, bool enabled = true)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPerformanceHint`。调用它会改变 `QQuickPaintedItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `hint`：类型为 `QQuickPaintedItem::PerformanceHint`。没有默认值，调用时必须提供。传入 `QQuickPaintedItem::PerformanceHint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `enabled`：类型为 `bool`。默认值为 `true`。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QQuickPaintedItem::setPerformanceHints(QQuickPaintedItem::PerformanceHints hints)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPerformanceHints`。调用它会改变 `QQuickPaintedItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `hints`：类型为 `QQuickPaintedItem::PerformanceHints`。没有默认值，调用时必须提供。传入 `QQuickPaintedItem::PerformanceHints` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QSGTextureProvider *QQuickPaintedItem::textureProvider() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuickPaintedItem::textureProvider` 用于计算、查询或取得与“texture、Provider”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSGTextureProvider *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSGTextureProvider *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QQuickPaintedItem::update(const QRect &rect = QRect())`

**API 类别：** 成员函数说明

**中文解读：** `QQuickPaintedItem::update` 用于执行与“更新”相关的操作。调用时要先确认当前状态和 `rect` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `rect`：类型为 `const QRect &`。默认值为 `QRect()`。矩形区域；要确认坐标系、是否包含右下边界以及空矩形的语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] QSGNode *QQuickPaintedItem::updatePaintNode(QSGNode *oldNode, QQuickItem::UpdatePaintNodeData *data)`

**API 类别：** 成员函数说明

**中文解读：** `QQuickPaintedItem::updatePaintNode` 用于计算、查询或取得与“更新、绘制、Node”相关的操作。调用时要先确认当前状态和 `oldNode`、`data` 的有效范围；返回类型是 `QSGNode *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSGNode *`。
- 参数 `oldNode`：类型为 `QSGNode *`。没有默认值，调用时必须提供。传入 `QSGNode *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `data`：类型为 `QQuickItem::UpdatePaintNodeData *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum PerformanceHint { FastFBOResizing }`

**API 类别：** 公有类型

**中文解读：** 这是 `QQuickPaintedItem` 暴露的类型声明 `Performance、Hint`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags PerformanceHints`

**API 类别：** 公有类型

**中文解读：** 这是 `QQuickPaintedItem` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QColor fillColor() const`

**API 类别：** 公有函数

**中文解读：** `QQuickPaintedItem::fillColor` 用于计算、查询或取得与“fill、Color”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QColor`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QColor`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QQuickPaintedItem::RenderTarget renderTarget() const`

**API 类别：** 公有函数

**中文解读：** 这是 `QQuickPaintedItem` 的核心操作 `renderTarget`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`QQuickPaintedItem::RenderTarget`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setFillColor(const QColor &)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setFillColor`。调用它会改变 `QQuickPaintedItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `const QColor &`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setRenderTarget(QQuickPaintedItem::RenderTarget target)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setRenderTarget`。调用它会改变 `QQuickPaintedItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `QQuickPaintedItem::RenderTarget`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setTextureSize(const QSize &size)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setTextureSize`。调用它会改变 `QQuickPaintedItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `size`：类型为 `const QSize &`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSize textureSize() const`

**API 类别：** 公有函数

**中文解读：** `QQuickPaintedItem::textureSize` 用于计算、查询或取得与“texture、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSize`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSize`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void fillColorChanged()`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `fillColorChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void renderTargetChanged()`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `renderTargetChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void textureSizeChanged()`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `textureSizeChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

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

`QQuickPaintedItem` 所属机制类型：QML 属性绑定与场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
