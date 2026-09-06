# QQuickRenderTarget

> Qt 6.11.1 · Qt Quick

## 1. 先建立直觉

**一句话定位：** `QQuickRenderTarget` 是 QML 属性绑定与场景图机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Quick 面向 QML/场景图界面，提供可视项、动画、输入和高性能界面基础设施。

### 这是什么

`QQuickRenderTarget` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QQuickRenderTarget>`
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

- `(since 6.8) enum class Flag { MultisampleResolve }`
- `flags Flags`

### 公有函数

- `QQuickRenderTarget()`
- `~QQuickRenderTarget()`
- `(since 6.8) QRhiTexture * depthTexture() const`
- `(since 6.3) qreal devicePixelRatio() const`
- `bool isNull() const`
- `(since 6.4) bool mirrorVertically() const`
- `(since 6.8) void setDepthTexture(QRhiTexture *texture)`
- `(since 6.3) void setDevicePixelRatio(qreal ratio)`
- `(since 6.4) void setMirrorVertically(bool enable)`

### 静态公有成员

- `(since 6.4) QQuickRenderTarget fromD3D11Texture(void *texture, uint format, const QSize &pixelSize, int sampleCount = 1)`
- `QQuickRenderTarget fromD3D11Texture(void *texture, const QSize &pixelSize, int sampleCount = 1)`
- `(since 6.8) QQuickRenderTarget fromD3D11Texture(void *texture, uint format, QSize pixelSize, int sampleCount, QQuickRenderTarget::Flags flags)`
- `(since 6.6) QQuickRenderTarget fromD3D12Texture(void *texture, int resourceState, uint format, const QSize &pixelSize, int sampleCount = 1)`
- `(since 6.8) QQuickRenderTarget fromD3D12Texture(void *texture, int resourceState, uint format, uint viewFormat, QSize pixelSize, int sampleCount, int arraySize, QQuickRenderTarget::Flags flags)`
- `(since 6.4) QQuickRenderTarget fromMetalTexture(MTLTexture *texture, uint format, const QSize &pixelSize, int sampleCount = 1)`
- `QQuickRenderTarget fromMetalTexture(MTLTexture *texture, const QSize &pixelSize, int sampleCount = 1)`
- `(since 6.8) QQuickRenderTarget fromMetalTexture(MTLTexture *texture, uint format, uint viewFormat, QSize pixelSize, int sampleCount, int arraySize, QQuickRenderTarget::Flags flags)`
- `(since 6.2) QQuickRenderTarget fromOpenGLRenderBuffer(uint renderbufferId, const QSize &pixelSize, int sampleCount = 1)`
- `(since 6.4) QQuickRenderTarget fromOpenGLTexture(uint textureId, uint format, const QSize &pixelSize, int sampleCount = 1)`
- `QQuickRenderTarget fromOpenGLTexture(uint textureId, const QSize &pixelSize, int sampleCount = 1)`
- `(since 6.8) QQuickRenderTarget fromOpenGLTexture(uint textureId, uint format, QSize pixelSize, int sampleCount, int arraySize, QQuickRenderTarget::Flags flags)`
- `(since 6.4) QQuickRenderTarget fromPaintDevice(QPaintDevice *device)`
- `(since 6.6) QQuickRenderTarget fromRhiRenderTarget(QRhiRenderTarget *renderTarget)`
- `(since 6.4) QQuickRenderTarget fromVulkanImage(VkImage image, VkImageLayout layout, VkFormat format, const QSize &pixelSize, int sampleCount = 1)`
- `QQuickRenderTarget fromVulkanImage(VkImage image, VkImageLayout layout, const QSize &pixelSize, int sampleCount = 1)`
- `(since 6.8) QQuickRenderTarget fromVulkanImage(VkImage image, VkImageLayout layout, VkFormat format, VkFormat viewFormat, QSize pixelSize, int sampleCount, int arraySize, QQuickRenderTarget::Flags flags)`

### 相关非成员函数

- `bool operator!=(const QQuickRenderTarget &a, const QQuickRenderTarget &b)`
- `bool operator==(const QQuickRenderTarget &a, const QQuickRenderTarget &b)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 31 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `[since 6.8] enum class QQuickRenderTarget::Flagflags QQuickRenderTarget::Flags`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QQuickRenderTarget` 暴露的类型声明 `class`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Flagflags QQuickRenderTarget::Flags`。
- 属性名：`QQuickRenderTarget`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QQuickRenderTarget::QQuickRenderTarget()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QQuickRenderTarget` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QQuickRenderTarget::~QQuickRenderTarget()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QQuickRenderTarget` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.8] QRhiTexture *QQuickRenderTarget::depthTexture() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuickRenderTarget::depthTexture` 用于计算、查询或取得与“depth、Texture”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRhiTexture *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRhiTexture *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.3] qreal QQuickRenderTarget::devicePixelRatio() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuickRenderTarget::devicePixelRatio` 用于计算、查询或取得与“device、Pixel、Ratio”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.4] QQuickRenderTarget QQuickRenderTarget::fromD3D11Texture(void *texture, uint format, const QSize &pixelSize, int sampleCount = 1)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromD3D11Texture`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QQuickRenderTarget`。
- 参数 `texture`：类型为 `void *`。没有默认值，调用时必须提供。传入 `void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `format`：类型为 `uint`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `pixelSize`：类型为 `const QSize &`。没有默认值，调用时必须提供。传入 `const QSize &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sampleCount`：类型为 `int`。默认值为 `1`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QQuickRenderTarget QQuickRenderTarget::fromD3D11Texture(void *texture, const QSize &pixelSize, int sampleCount = 1)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromD3D11Texture`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QQuickRenderTarget`。
- 参数 `texture`：类型为 `void *`。没有默认值，调用时必须提供。传入 `void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pixelSize`：类型为 `const QSize &`。没有默认值，调用时必须提供。传入 `const QSize &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sampleCount`：类型为 `int`。默认值为 `1`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.8] QQuickRenderTarget QQuickRenderTarget::fromD3D11Texture(void *texture, uint format, QSize pixelSize, int sampleCount, QQuickRenderTarget::Flags flags)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromD3D11Texture`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QQuickRenderTarget`。
- 参数 `texture`：类型为 `void *`。没有默认值，调用时必须提供。传入 `void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `format`：类型为 `uint`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `pixelSize`：类型为 `QSize`。没有默认值，调用时必须提供。传入 `QSize` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sampleCount`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `flags`：类型为 `QQuickRenderTarget::Flags`。没有默认值，调用时必须提供。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.6] QQuickRenderTarget QQuickRenderTarget::fromD3D12Texture(void *texture, int resourceState, uint format, const QSize &pixelSize, int sampleCount = 1)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromD3D12Texture`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QQuickRenderTarget`。
- 参数 `texture`：类型为 `void *`。没有默认值，调用时必须提供。传入 `void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `resourceState`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `format`：类型为 `uint`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `pixelSize`：类型为 `const QSize &`。没有默认值，调用时必须提供。传入 `const QSize &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sampleCount`：类型为 `int`。默认值为 `1`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.8] QQuickRenderTarget QQuickRenderTarget::fromD3D12Texture(void *texture, int resourceState, uint format, uint viewFormat, QSize pixelSize, int sampleCount, int arraySize, QQuickRenderTarget::Flags flags)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromD3D12Texture`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QQuickRenderTarget`。
- 参数 `texture`：类型为 `void *`。没有默认值，调用时必须提供。传入 `void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `resourceState`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `format`：类型为 `uint`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `viewFormat`：类型为 `uint`。没有默认值，调用时必须提供。传入 `uint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pixelSize`：类型为 `QSize`。没有默认值，调用时必须提供。传入 `QSize` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sampleCount`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `arraySize`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `flags`：类型为 `QQuickRenderTarget::Flags`。没有默认值，调用时必须提供。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.4] QQuickRenderTarget QQuickRenderTarget::fromMetalTexture(MTLTexture *texture, uint format, const QSize &pixelSize, int sampleCount = 1)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromMetalTexture`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QQuickRenderTarget`。
- 参数 `texture`：类型为 `MTLTexture *`。没有默认值，调用时必须提供。传入 `MTLTexture *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `format`：类型为 `uint`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `pixelSize`：类型为 `const QSize &`。没有默认值，调用时必须提供。传入 `const QSize &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sampleCount`：类型为 `int`。默认值为 `1`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QQuickRenderTarget QQuickRenderTarget::fromMetalTexture(MTLTexture *texture, const QSize &pixelSize, int sampleCount = 1)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromMetalTexture`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QQuickRenderTarget`。
- 参数 `texture`：类型为 `MTLTexture *`。没有默认值，调用时必须提供。传入 `MTLTexture *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pixelSize`：类型为 `const QSize &`。没有默认值，调用时必须提供。传入 `const QSize &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sampleCount`：类型为 `int`。默认值为 `1`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.8] QQuickRenderTarget QQuickRenderTarget::fromMetalTexture(MTLTexture *texture, uint format, uint viewFormat, QSize pixelSize, int sampleCount, int arraySize, QQuickRenderTarget::Flags flags)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromMetalTexture`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QQuickRenderTarget`。
- 参数 `texture`：类型为 `MTLTexture *`。没有默认值，调用时必须提供。传入 `MTLTexture *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `format`：类型为 `uint`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `viewFormat`：类型为 `uint`。没有默认值，调用时必须提供。传入 `uint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pixelSize`：类型为 `QSize`。没有默认值，调用时必须提供。传入 `QSize` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sampleCount`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `arraySize`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `flags`：类型为 `QQuickRenderTarget::Flags`。没有默认值，调用时必须提供。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.2] QQuickRenderTarget QQuickRenderTarget::fromOpenGLRenderBuffer(uint renderbufferId, const QSize &pixelSize, int sampleCount = 1)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromOpenGLRenderBuffer`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QQuickRenderTarget`。
- 参数 `renderbufferId`：类型为 `uint`。没有默认值，调用时必须提供。传入 `uint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pixelSize`：类型为 `const QSize &`。没有默认值，调用时必须提供。传入 `const QSize &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sampleCount`：类型为 `int`。默认值为 `1`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.4] QQuickRenderTarget QQuickRenderTarget::fromOpenGLTexture(uint textureId, uint format, const QSize &pixelSize, int sampleCount = 1)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromOpenGLTexture`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QQuickRenderTarget`。
- 参数 `textureId`：类型为 `uint`。没有默认值，调用时必须提供。传入 `uint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `format`：类型为 `uint`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `pixelSize`：类型为 `const QSize &`。没有默认值，调用时必须提供。传入 `const QSize &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sampleCount`：类型为 `int`。默认值为 `1`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QQuickRenderTarget QQuickRenderTarget::fromOpenGLTexture(uint textureId, const QSize &pixelSize, int sampleCount = 1)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromOpenGLTexture`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QQuickRenderTarget`。
- 参数 `textureId`：类型为 `uint`。没有默认值，调用时必须提供。传入 `uint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pixelSize`：类型为 `const QSize &`。没有默认值，调用时必须提供。传入 `const QSize &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sampleCount`：类型为 `int`。默认值为 `1`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.8] QQuickRenderTarget QQuickRenderTarget::fromOpenGLTexture(uint textureId, uint format, QSize pixelSize, int sampleCount, int arraySize, QQuickRenderTarget::Flags flags)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromOpenGLTexture`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QQuickRenderTarget`。
- 参数 `textureId`：类型为 `uint`。没有默认值，调用时必须提供。传入 `uint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `format`：类型为 `uint`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `pixelSize`：类型为 `QSize`。没有默认值，调用时必须提供。传入 `QSize` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sampleCount`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `arraySize`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `flags`：类型为 `QQuickRenderTarget::Flags`。没有默认值，调用时必须提供。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.4] QQuickRenderTarget QQuickRenderTarget::fromPaintDevice(QPaintDevice *device)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromPaintDevice`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QQuickRenderTarget`。
- 参数 `device`：类型为 `QPaintDevice *`。没有默认值，调用时必须提供。QIODevice 或绘制设备。调用前要确认已经打开、支持所需模式，或处于合法绘制阶段。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.6] QQuickRenderTarget QQuickRenderTarget::fromRhiRenderTarget(QRhiRenderTarget *renderTarget)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromRhiRenderTarget`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QQuickRenderTarget`。
- 参数 `renderTarget`：类型为 `QRhiRenderTarget *`。没有默认值，调用时必须提供。传入 `QRhiRenderTarget *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.4] QQuickRenderTarget QQuickRenderTarget::fromVulkanImage(VkImage image, VkImageLayout layout, VkFormat format, const QSize &pixelSize, int sampleCount = 1)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromVulkanImage`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QQuickRenderTarget`。
- 参数 `image`：类型为 `VkImage`。没有默认值，调用时必须提供。传入 `VkImage` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `layout`：类型为 `VkImageLayout`。没有默认值，调用时必须提供。参与操作的布局对象。通常表示整个子布局的几何区域和所有权，不等于子布局里的某一个控件。
- 参数 `format`：类型为 `VkFormat`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `pixelSize`：类型为 `const QSize &`。没有默认值，调用时必须提供。传入 `const QSize &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sampleCount`：类型为 `int`。默认值为 `1`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QQuickRenderTarget QQuickRenderTarget::fromVulkanImage(VkImage image, VkImageLayout layout, const QSize &pixelSize, int sampleCount = 1)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromVulkanImage`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QQuickRenderTarget`。
- 参数 `image`：类型为 `VkImage`。没有默认值，调用时必须提供。传入 `VkImage` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `layout`：类型为 `VkImageLayout`。没有默认值，调用时必须提供。参与操作的布局对象。通常表示整个子布局的几何区域和所有权，不等于子布局里的某一个控件。
- 参数 `pixelSize`：类型为 `const QSize &`。没有默认值，调用时必须提供。传入 `const QSize &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sampleCount`：类型为 `int`。默认值为 `1`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.8] QQuickRenderTarget QQuickRenderTarget::fromVulkanImage(VkImage image, VkImageLayout layout, VkFormat format, VkFormat viewFormat, QSize pixelSize, int sampleCount, int arraySize, QQuickRenderTarget::Flags flags)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromVulkanImage`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QQuickRenderTarget`。
- 参数 `image`：类型为 `VkImage`。没有默认值，调用时必须提供。传入 `VkImage` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `layout`：类型为 `VkImageLayout`。没有默认值，调用时必须提供。参与操作的布局对象。通常表示整个子布局的几何区域和所有权，不等于子布局里的某一个控件。
- 参数 `format`：类型为 `VkFormat`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `viewFormat`：类型为 `VkFormat`。没有默认值，调用时必须提供。传入 `VkFormat` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pixelSize`：类型为 `QSize`。没有默认值，调用时必须提供。传入 `QSize` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sampleCount`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `arraySize`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `flags`：类型为 `QQuickRenderTarget::Flags`。没有默认值，调用时必须提供。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QQuickRenderTarget::isNull() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isNull`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.4] bool QQuickRenderTarget::mirrorVertically() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuickRenderTarget::mirrorVertically` 用于计算、查询或取得与“mirror、Vertically”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.8] void QQuickRenderTarget::setDepthTexture(QRhiTexture *texture)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setDepthTexture`。调用它会改变 `QQuickRenderTarget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `texture`：类型为 `QRhiTexture *`。没有默认值，调用时必须提供。传入 `QRhiTexture *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.3] void QQuickRenderTarget::setDevicePixelRatio(qreal ratio)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setDevicePixelRatio`。调用它会改变 `QQuickRenderTarget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `ratio`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.4] void QQuickRenderTarget::setMirrorVertically(bool enable)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setMirrorVertically`。调用它会改变 `QQuickRenderTarget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enable`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator!=(const QQuickRenderTarget &a, const QQuickRenderTarget &b)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QQuickRenderTarget` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `a`：类型为 `const QQuickRenderTarget &`。没有默认值，调用时必须提供。传入 `const QQuickRenderTarget &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `b`：类型为 `const QQuickRenderTarget &`。没有默认值，调用时必须提供。传入 `const QQuickRenderTarget &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator==(const QQuickRenderTarget &a, const QQuickRenderTarget &b)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QQuickRenderTarget` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `a`：类型为 `const QQuickRenderTarget &`。没有默认值，调用时必须提供。传入 `const QQuickRenderTarget &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `b`：类型为 `const QQuickRenderTarget &`。没有默认值，调用时必须提供。传入 `const QQuickRenderTarget &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.8) enum class Flag { MultisampleResolve }`

**API 类别：** 公有类型

**中文解读：** 这是 `QQuickRenderTarget` 暴露的类型声明 `class`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags Flags`

**API 类别：** 公有类型

**中文解读：** 这是 `QQuickRenderTarget` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

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

`QQuickRenderTarget` 所属机制类型：QML 属性绑定与场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
