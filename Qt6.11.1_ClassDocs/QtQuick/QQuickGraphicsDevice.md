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

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QQuickGraphicsDevice::QQuickGraphicsDevice()`

**作用与语义：**

构建一个默认的 QQuickGraphicsDevice，不引用任何本地对象。

### `[noexcept] QQuickGraphicsDevice::~QQuickGraphicsDevice()`

**作用与语义：**

毁灭者。

### `[static] QQuickGraphicsDevice QQuickGraphicsDevice::fromAdapter(quint32 adapterLuidLow, qint32 adapterLuidHigh, int featureLevel = 0)`

**作用与语义：**

返回一个新`QQuickGraphicsDevice`，描述了DXGI适配器和D3D功能等级。
该出厂功能适用于 Direct3D 11 和 12，尤其是与 OpenXR 结合使用。`adapterLuidLow` 和 `adapterLuidHigh` 共同指定 LUID，而 featureLevel 指定 `D3D_FEATURE_LEVEL_` 值。如果不指定，`featureLevel` 可设置为 0，此时将使用场景图的默认值。
注意：使用 Direct 3D 12 `featureLevel` 指定传递给 D3D12CreateDevice()的 `minimum` 功能层级。

### `[static] QQuickGraphicsDevice QQuickGraphicsDevice::fromDeviceAndCommandQueue(MTLDevice *device, MTLCommandQueue *commandQueue)`

**作用与语义：**

返回一个新的`QQuickGraphicsDevice`，引用已有的`device`和`commandQueue`对象。
这种工厂功能适用于金属。
注意：生成的 `QQuickGraphicsDevice` 不拥有任何本地资源，仅包含引用。调用者有责任确保本地资源持续存在直到必要。

### `[static] QQuickGraphicsDevice QQuickGraphicsDevice::fromDeviceAndContext(void *device, void *context)`

**作用与语义：**

返回一个新的`QQuickGraphicsDevice`，引用本地设备和上下文对象。
该工厂功能适用于Direct3D 11。`device`预计为`ID3D11Device*`，`context`为`ID3D11DeviceContext*`。
它也支持 Direct 3D 12，如果运行时使用的 3D API 是 Direct 3D 12。使用 D3D12 时，`context` 未被使用，可以设置为空。`device` 预计会是 `ID3D12Device*`。
注意：最终的`QQuickGraphicsDevice`不拥有任何本地资源，仅包含引用。调用者有责任确保本地资源持续存在直到必要。

### `[static] QQuickGraphicsDevice QQuickGraphicsDevice::fromDeviceObjects(VkPhysicalDevice physicalDevice, VkDevice device, int queueFamilyIndex, int queueIndex = 0)`

**作用与语义：**

返回一个新的`QQuickGraphicsDevice`引用已有的`device`对象。
该工厂函数适用于Vulkan。必须始终提供`physicalDevice`、`device`和`queueFamilyIndex`。`queueIndex`是可选的，因为默认值0通常合适。
注意：最终`QQuickGraphicsDevice`不拥有任何本地资源，仅包含引用。调用者有责任确保本地资源在必要时间内持续存在。

### `[static] QQuickGraphicsDevice QQuickGraphicsDevice::fromOpenGLContext(QOpenGLContext *context)`

**作用与语义：**

返回一个引用现有OpenGL的新`QQuickGraphicsDevice` `context`。
该出厂功能适用于 OpenGL。
注意：确保`context`与`QQuickWindow`兼容且可用由调用者负责。相关`QSurfaceFormat`中平台特定的不匹配，或因尝试在多个线程中使用`context`而导致的线程问题，则由调用者自行避免。

### `[static] QQuickGraphicsDevice QQuickGraphicsDevice::fromPhysicalDevice(VkPhysicalDevice physicalDevice)`

**作用与语义：**

返回一个引用现有`physicalDevice`的新`QQuickGraphicsDevice`。
该出厂功能适用于 Vulkan，尤其适合与 OpenXR 结合使用。
注意：最终`QQuickGraphicsDevice`不拥有任何本地资源，仅包含引用。调用者有责任确保本地资源持续存在，直到必要时间为止。

### `[static, since 6.6] QQuickGraphicsDevice QQuickGraphicsDevice::fromRhi(QRhi *rhi)`

**作用与语义：**

返回一个引用现有`rhi`对象的新`QQuickGraphicsDevice`。
注意：与`fromOpenGLContext()`类似，调用者必须谨慎只共享已知兼容的QQuickWindows之间的`QRhi`（以及底层图形上下文或设备），不得违反底层图形API在线程、像素格式等方面的规则。

### `[static, since 6.10] QQuickGraphicsDevice QQuickGraphicsDevice::fromRhiAdapter(QRhiAdapter *adapter)`

**作用与语义：**

返回一个引用现有`adapter` `QRhiAdapter`对象的新`QQuickGraphicsDevice`。
不适用于`QRhi`后端和图形API，因为`QRhiAdapter`没有真正的实现。
相当于Direct 3D的 `fromAdapter()`，以及 Vulkan 的`fromPhysicalDevice()`。
注意：所有权不被`adapter`夺取，且至少必须在场景图启动前保持有效，这很可能发生在相关`QQuickWindow`暴露时。

### `bool QQuickGraphicsDevice::isNull() const`

**作用与语义：**

如果这是一个默认构造图形设备且不引用任何本地对象，则返回为真。

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
