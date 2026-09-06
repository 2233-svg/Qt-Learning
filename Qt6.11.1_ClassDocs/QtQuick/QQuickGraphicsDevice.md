# QQuickGraphicsDevice

> Qt 6.11.1 · Qt Quick

## 1. 先建立直觉

**一句话定位：** `QQuickGraphicsDevice` 是 QML 属性绑定与场景图机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Quick 面向 QML/场景图界面，提供可视项、动画、输入和高性能界面基础设施。

### 这是什么

`QQuickGraphicsDevice` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QQuickGraphicsDevice>`
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

### 公有函数

- `QQuickGraphicsDevice()`
- `~QQuickGraphicsDevice()`
- `bool isNull() const`

### 静态公有成员

- `QQuickGraphicsDevice fromAdapter(quint32 adapterLuidLow, qint32 adapterLuidHigh, int featureLevel = 0)`
- `QQuickGraphicsDevice fromDeviceAndCommandQueue(MTLDevice *device, MTLCommandQueue *commandQueue)`
- `QQuickGraphicsDevice fromDeviceAndContext(void *device, void *context)`
- `QQuickGraphicsDevice fromDeviceObjects(VkPhysicalDevice physicalDevice, VkDevice device, int queueFamilyIndex, int queueIndex = 0)`
- `QQuickGraphicsDevice fromOpenGLContext(QOpenGLContext *context)`
- `QQuickGraphicsDevice fromPhysicalDevice(VkPhysicalDevice physicalDevice)`
- `(since 6.6) QQuickGraphicsDevice fromRhi(QRhi *rhi)`
- `(since 6.10) QQuickGraphicsDevice fromRhiAdapter(QRhiAdapter *adapter)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 11 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `QQuickGraphicsDevice::QQuickGraphicsDevice()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QQuickGraphicsDevice` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QQuickGraphicsDevice::~QQuickGraphicsDevice()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QQuickGraphicsDevice` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QQuickGraphicsDevice QQuickGraphicsDevice::fromAdapter(quint32 adapterLuidLow, qint32 adapterLuidHigh, int featureLevel = 0)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromAdapter`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QQuickGraphicsDevice`。
- 参数 `adapterLuidLow`：类型为 `quint32`。没有默认值，调用时必须提供。传入 `quint32` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `adapterLuidHigh`：类型为 `qint32`。没有默认值，调用时必须提供。传入 `qint32` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `featureLevel`：类型为 `int`。默认值为 `0`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QQuickGraphicsDevice QQuickGraphicsDevice::fromDeviceAndCommandQueue(MTLDevice *device, MTLCommandQueue *commandQueue)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromDeviceAndCommandQueue`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QQuickGraphicsDevice`。
- 参数 `device`：类型为 `MTLDevice *`。没有默认值，调用时必须提供。QIODevice 或绘制设备。调用前要确认已经打开、支持所需模式，或处于合法绘制阶段。
- 参数 `commandQueue`：类型为 `MTLCommandQueue *`。没有默认值，调用时必须提供。传入 `MTLCommandQueue *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QQuickGraphicsDevice QQuickGraphicsDevice::fromDeviceAndContext(void *device, void *context)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromDeviceAndContext`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QQuickGraphicsDevice`。
- 参数 `device`：类型为 `void *`。没有默认值，调用时必须提供。QIODevice 或绘制设备。调用前要确认已经打开、支持所需模式，或处于合法绘制阶段。
- 参数 `context`：类型为 `void *`。没有默认值，调用时必须提供。上下文对象，用于限定回调连接的生命周期或解析/执行环境。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QQuickGraphicsDevice QQuickGraphicsDevice::fromDeviceObjects(VkPhysicalDevice physicalDevice, VkDevice device, int queueFamilyIndex, int queueIndex = 0)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromDeviceObjects`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QQuickGraphicsDevice`。
- 参数 `physicalDevice`：类型为 `VkPhysicalDevice`。没有默认值，调用时必须提供。传入 `VkPhysicalDevice` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `device`：类型为 `VkDevice`。没有默认值，调用时必须提供。QIODevice 或绘制设备。调用前要确认已经打开、支持所需模式，或处于合法绘制阶段。
- 参数 `queueFamilyIndex`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `queueIndex`：类型为 `int`。默认值为 `0`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QQuickGraphicsDevice QQuickGraphicsDevice::fromOpenGLContext(QOpenGLContext *context)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromOpenGLContext`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QQuickGraphicsDevice`。
- 参数 `context`：类型为 `QOpenGLContext *`。没有默认值，调用时必须提供。上下文对象，用于限定回调连接的生命周期或解析/执行环境。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QQuickGraphicsDevice QQuickGraphicsDevice::fromPhysicalDevice(VkPhysicalDevice physicalDevice)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromPhysicalDevice`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QQuickGraphicsDevice`。
- 参数 `physicalDevice`：类型为 `VkPhysicalDevice`。没有默认值，调用时必须提供。传入 `VkPhysicalDevice` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.6] QQuickGraphicsDevice QQuickGraphicsDevice::fromRhi(QRhi *rhi)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromRhi`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QQuickGraphicsDevice`。
- 参数 `rhi`：类型为 `QRhi *`。没有默认值，调用时必须提供。传入 `QRhi *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.10] QQuickGraphicsDevice QQuickGraphicsDevice::fromRhiAdapter(QRhiAdapter *adapter)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromRhiAdapter`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QQuickGraphicsDevice`。
- 参数 `adapter`：类型为 `QRhiAdapter *`。没有默认值，调用时必须提供。传入 `QRhiAdapter *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QQuickGraphicsDevice::isNull() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isNull`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
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

`QQuickGraphicsDevice` 所属机制类型：QML 属性绑定与场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
