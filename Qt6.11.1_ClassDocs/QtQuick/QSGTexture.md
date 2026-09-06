# QSGTexture

> Qt 6.11.1 · Qt Quick

## 1. 先建立直觉

**一句话定位：** `QSGTexture` 是 Qt Quick 场景图渲染类型，负责节点、材质、纹理、几何或渲染状态。

**模块背景：** Qt Quick 面向 QML/场景图界面，提供可视项、动画、输入和高性能界面基础设施。

### 这是什么

`QSGTexture` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QSGTexture>`
- 继承自：QObject
- 直接派生类：QSGDynamicTexture

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Quick)
target_link_libraries(mytarget PRIVATE Qt6::Quick)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

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

- `enum AnisotropyLevel { AnisotropyNone, Anisotropy2x, Anisotropy4x, Anisotropy8x, Anisotropy16x }`
- `enum Filtering { None, Nearest, Linear }`
- `enum WrapMode { Repeat, ClampToEdge, MirroredRepeat }`

### 公有函数

- `QSGTexture()`
- `virtual ~QSGTexture() override`
- `QSGTexture::AnisotropyLevel anisotropyLevel() const`
- `(since 6.0) virtual void commitTextureOperations(QRhi *rhi, QRhiResourceUpdateBatch *resourceUpdates)`
- `virtual qint64 comparisonKey() const = 0`
- `QRectF convertToNormalizedSourceRect(const QRectF &rect) const`
- `QSGTexture::Filtering filtering() const`
- `virtual bool hasAlphaChannel() const = 0`
- `virtual bool hasMipmaps() const = 0`
- `QSGTexture::WrapMode horizontalWrapMode() const`
- `virtual bool isAtlasTexture() const`
- `QSGTexture::Filtering mipmapFiltering() const`
- `QNativeInterface * nativeInterface() const`
- `virtual QRectF normalizedTextureSubRect() const`
- `virtual QSGTexture * removedFromAtlas(QRhiResourceUpdateBatch *resourceUpdates = nullptr) const`
- `(since 6.0) virtual QRhiTexture * rhiTexture() const`
- `void setAnisotropyLevel(QSGTexture::AnisotropyLevel level)`
- `void setFiltering(QSGTexture::Filtering filter)`
- `void setHorizontalWrapMode(QSGTexture::WrapMode hwrap)`
- `void setMipmapFiltering(QSGTexture::Filtering filter)`
- `void setVerticalWrapMode(QSGTexture::WrapMode vwrap)`
- `virtual QSize textureSize() const = 0`
- `QSGTexture::WrapMode verticalWrapMode() const`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 26 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QSGTexture::AnisotropyLevel`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QSGTexture` 暴露的类型声明 `Anisotropy、Level`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:AnisotropyLevel`。
- 属性名：`QSGTexture`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QSGTexture::Filtering`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QSGTexture` 暴露的类型声明 `Filtering`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Filtering`。
- 属性名：`QSGTexture`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QSGTexture::WrapMode`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QSGTexture` 暴露的类型声明 `Wrap、模式`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:WrapMode`。
- 属性名：`QSGTexture`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSGTexture::QSGTexture()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSGTexture` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual noexcept] QSGTexture::~QSGTexture()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSGTexture` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSGTexture::AnisotropyLevel QSGTexture::anisotropyLevel() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGTexture::anisotropyLevel` 用于计算、查询或取得与“anisotropy、Level”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSGTexture::AnisotropyLevel`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSGTexture::AnisotropyLevel`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual, since 6.0] void QSGTexture::commitTextureOperations(QRhi *rhi, QRhiResourceUpdateBatch *resourceUpdates)`

**API 类别：** 成员函数说明

**中文解读：** `QSGTexture::commitTextureOperations` 用于执行与“提交、Texture、Operations”相关的操作。调用时要先确认当前状态和 `rhi`、`resourceUpdates` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `rhi`：类型为 `QRhi *`。没有默认值，调用时必须提供。传入 `QRhi *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `resourceUpdates`：类型为 `QRhiResourceUpdateBatch *`。没有默认值，调用时必须提供。传入 `QRhiResourceUpdateBatch *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] qint64 QSGTexture::comparisonKey() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGTexture::comparisonKey` 用于计算、查询或取得与“comparison、Key”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qint64`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qint64`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRectF QSGTexture::convertToNormalizedSourceRect(const QRectF &rect) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `convertToNormalizedSourceRect`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QRectF`。
- 参数 `rect`：类型为 `const QRectF &`。没有默认值，调用时必须提供。矩形区域；要确认坐标系、是否包含右下边界以及空矩形的语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSGTexture::Filtering QSGTexture::filtering() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGTexture::filtering` 用于计算、查询或取得与“filtering”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSGTexture::Filtering`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSGTexture::Filtering`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] bool QSGTexture::hasAlphaChannel() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `hasAlphaChannel`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] bool QSGTexture::hasMipmaps() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `hasMipmaps`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSGTexture::WrapMode QSGTexture::horizontalWrapMode() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGTexture::horizontalWrapMode` 用于计算、查询或取得与“水平、Wrap、模式”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSGTexture::WrapMode`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSGTexture::WrapMode`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] bool QSGTexture::isAtlasTexture() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isAtlasTexture`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSGTexture::Filtering QSGTexture::mipmapFiltering() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGTexture::mipmapFiltering` 用于计算、查询或取得与“mipmap、Filtering”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSGTexture::Filtering`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSGTexture::Filtering`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename QNativeInterface> QNativeInterface *QSGTexture::nativeInterface() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGTexture::nativeInterface` 用于计算、查询或取得与“native、Interface”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `template <typename QNativeInterface> QNativeInterface *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename QNativeInterface> QNativeInterface *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] QRectF QSGTexture::normalizedTextureSubRect() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGTexture::normalizedTextureSubRect` 用于计算、查询或取得与“normalized、Texture、Sub、Rect”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRectF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRectF`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] QSGTexture *QSGTexture::removedFromAtlas(QRhiResourceUpdateBatch *resourceUpdates = nullptr) const`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removedFromAtlas`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`QSGTexture *`。
- 参数 `resourceUpdates`：类型为 `QRhiResourceUpdateBatch *`。默认值为 `nullptr`。传入 `QRhiResourceUpdateBatch *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual, since 6.0] QRhiTexture *QSGTexture::rhiTexture() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGTexture::rhiTexture` 用于计算、查询或取得与“rhi、Texture”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRhiTexture *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhiTexture *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSGTexture::setAnisotropyLevel(QSGTexture::AnisotropyLevel level)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setAnisotropyLevel`。调用它会改变 `QSGTexture` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `level`：类型为 `QSGTexture::AnisotropyLevel`。没有默认值，调用时必须提供。传入 `QSGTexture::AnisotropyLevel` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSGTexture::setFiltering(QSGTexture::Filtering filter)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFiltering`。调用它会改变 `QSGTexture` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `filter`：类型为 `QSGTexture::Filtering`。没有默认值，调用时必须提供。过滤条件、匹配器或过滤标志；要确认它作用于显示结果、输入数据还是事件传播。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSGTexture::setHorizontalWrapMode(QSGTexture::WrapMode hwrap)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setHorizontalWrapMode`。调用它会改变 `QSGTexture` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `hwrap`：类型为 `QSGTexture::WrapMode`。没有默认值，调用时必须提供。传入 `QSGTexture::WrapMode` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSGTexture::setMipmapFiltering(QSGTexture::Filtering filter)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setMipmapFiltering`。调用它会改变 `QSGTexture` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `filter`：类型为 `QSGTexture::Filtering`。没有默认值，调用时必须提供。过滤条件、匹配器或过滤标志；要确认它作用于显示结果、输入数据还是事件传播。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSGTexture::setVerticalWrapMode(QSGTexture::WrapMode vwrap)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setVerticalWrapMode`。调用它会改变 `QSGTexture` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `vwrap`：类型为 `QSGTexture::WrapMode`。没有默认值，调用时必须提供。传入 `QSGTexture::WrapMode` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual] QSize QSGTexture::textureSize() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGTexture::textureSize` 用于计算、查询或取得与“texture、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSize`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSize`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSGTexture::WrapMode QSGTexture::verticalWrapMode() const`

**API 类别：** 成员函数说明

**中文解读：** `QSGTexture::verticalWrapMode` 用于计算、查询或取得与“垂直、Wrap、模式”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSGTexture::WrapMode`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSGTexture::WrapMode`。
- 参数：无。

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

`QSGTexture` 所属机制类型：Qt Quick 场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
