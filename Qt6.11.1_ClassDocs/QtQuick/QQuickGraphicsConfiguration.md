# QQuickGraphicsConfiguration

> Qt 6.11.1 · Qt Quick

## 1. 先建立直觉

**一句话定位：** `QQuickGraphicsConfiguration` 是 QML 属性绑定与场景图机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Quick 面向 QML/场景图界面，提供可视项、动画、输入和高性能界面基础设施。

### 这是什么

`QQuickGraphicsConfiguration` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QQuickGraphicsConfiguration>`
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

- `QQuickGraphicsConfiguration()`
- `~QQuickGraphicsConfiguration()`
- `QByteArrayList deviceExtensions() const`
- `(since 6.5) bool isAutomaticPipelineCacheEnabled() const`
- `bool isDebugLayerEnabled() const`
- `bool isDebugMarkersEnabled() const`
- `bool isDepthBufferEnabledFor2D() const`
- `QString pipelineCacheLoadFile() const`
- `QString pipelineCacheSaveFile() const`
- `bool prefersSoftwareDevice() const`
- `(since 6.5) void setAutomaticPipelineCache(bool enable)`
- `(since 6.5) void setDebugLayer(bool enable)`
- `(since 6.5) void setDebugMarkers(bool enable)`
- `void setDepthBufferFor2D(bool enable)`
- `void setDeviceExtensions(const QByteArrayList &extensions)`
- `(since 6.5) void setPipelineCacheLoadFile(const QString &filename)`
- `(since 6.5) void setPipelineCacheSaveFile(const QString &filename)`
- `(since 6.5) void setPreferSoftwareDevice(bool enable)`
- `(since 6.6) void setTimestamps(bool enable)`
- `(since 6.6) bool timestampsEnabled() const`

### 静态公有成员

- `(since 6.1) QByteArrayList preferredInstanceExtensions()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QQuickGraphicsConfiguration::QQuickGraphicsConfiguration()`

**作用与语义：**

构建默认的QQuickGraphicsConfiguration，未指定场景图需要考虑的任何额外设置。

### `[noexcept] QQuickGraphicsConfiguration::~QQuickGraphicsConfiguration()`

**作用与语义：**

毁灭者。

### `QByteArrayList QQuickGraphicsConfiguration::deviceExtensions() const`

**作用与语义：**

返回请求的额外设备扩展列表。

### `[since 6.5] bool QQuickGraphicsConfiguration::isAutomaticPipelineCacheEnabled() const`

**作用与语义：**

如果启用了自动流水线缓存，则返回为true。
默认情况下，除非设置了某些应用属性或环境变量，否则这是正确的。更多信息请参见自动流水线缓存。

### `bool QQuickGraphicsConfiguration::isDebugLayerEnabled() const`

**作用与语义：**

如果要启用调试/验证层，则返回为真。
默认情况下，该值为假。

### `bool QQuickGraphicsConfiguration::isDebugMarkersEnabled() const`

**作用与语义：**

如果启用了调试标记，则返回为真。
默认情况下，该值为假。

### `bool QQuickGraphicsConfiguration::isDepthBufferEnabledFor2D() const`

**作用与语义：**

如果对2D内容启用深度缓冲使用，则返回为真。
默认情况下，该值为真，除非`QSG_NO_DEPTH_BUFFER`环境变量被设置。

### `QString QQuickGraphicsConfiguration::pipelineCacheLoadFile() const`

**作用与语义：**

返回当前设置的文件名以加载流水线缓存。
默认情况下，该值是一个空字符串。

### `QString QQuickGraphicsConfiguration::pipelineCacheSaveFile() const`

**作用与语义：**

返回当前设置的文件名，用于存储流水线缓存。
默认情况下，该值是一个空字符串。

### `[static, since 6.1] QByteArrayList QQuickGraphicsConfiguration::preferredInstanceExtensions()`

**作用与语义：**

返回 Qt Quick 偏好在 VkInstance 上启用的 Vulkan 实例扩展列表。
在大多数情况下，Qt Quick负责创建`QVulkanInstance`。那么这个函数就不相关了。另一方面，当使用`QQuickRenderControl`与基于Vulkan的渲染结合时，应用程序负责创建`QVulkanInstance`并将其与（屏幕外的）`QQuickWindow`关联。在这种情况下，应用通常会查询启用实例扩展列表，并将其传递给`QVulkanInstance::setExtensions()`，然后再调用`QVulkanInstance::create()`。

### `bool QQuickGraphicsConfiguration::prefersSoftwareDevice() const`

**作用与语义：**

如果优先考虑基于光栅器的软件图形设备，则返回为真。
默认情况下，该值为假。

### `[since 6.5] void QQuickGraphicsConfiguration::setAutomaticPipelineCache(bool enable)`

**作用与语义：**

根据`enable`调整自动流水线缓存的使用情况。
默认值为真，除非设置了某些应用属性或环境变量。更多信息请参见自动管道缓存。

### `[since 6.5] void QQuickGraphicsConfiguration::setDebugLayer(bool enable)`

**作用与语义：**

启用图形API实现的调试或验证层（如有）。
实际上，Vulkan 和 Direct 3D 11 支持此功能，前提是安装并运行时已提供必要的支持（验证层、Windows SDK）。当`enable`成立时，Qt 会尝试在 VkInstance 上启用标准验证层，或在图形设备上设置 `D3D11_CREATE_DEVICE_DEBUG`。
对于macOS上的Metal，启动应用前请将环境变量设为`METAL_DEVICE_WRAPPER_TYPE=1`。
将`enable`设为真调用该函数，等价于将环境变量`QSG_RHI_DEBUG_LAYER`设置为非零值。
默认值为假。
注意：启用调试层或验证层可能会带来不小的性能影响。强烈建议在启用该标志的情况下将应用交付生产环境。
注意：由于底层图形API设计的不同，该设置不总是每个`QQuickWindow`单独设置，尽管每个`QQuickWindow`都有自己的`QQuickGraphicsConfiguration`。特别是在Vulkan中，实例对象（VkInstance）只被创建一次，之后应用中所有窗口都会使用。因此，启用验证层会影响所有窗口。这也意味着，尝试通过仅在其他窗口开始渲染后才显示的窗口来启用验证，对Vulkan没有影响。其他API，如D3D11，则将调试层概念作为每个设备（ID3D11Device）设置，因此它是基于真正的每个窗口进行控制（假设场景图渲染循环为每个`QQuickWindow`使用专用的图形设备/上下文）。

### `[since 6.5] void QQuickGraphicsConfiguration::setDebugMarkers(bool enable)`

**作用与语义：**

在适用的情况下，`enable`控制将调试标记和对象名称插入图形命令流中。
一些框架，如 Qt Quick 3D，能够为它们创建的图形对象（缓冲区、纹理）标注名称，并指示命令缓冲区中渲染的起点和结束点。这些内容随后通过 RenderDoc 或 XCode 等工具制作的帧捕获数据可见。
预计支持该接口的图形API有Vulkan（如果有VK_EXT_debug_utils）、Direct 3D 11和Metal。
将 `enable` 设为 true 调用该函数，等同于将环境变量 `QSG_RHI_PROFILE` 设置为非零值。
默认值为假。
注意：启用调试标记可能会影响性能。不建议在启用该标志的情况下将应用程序交付生产环境。

### `void QQuickGraphicsConfiguration::setDepthBufferFor2D(bool enable)`

**作用与语义：**

将2D内容的深度缓冲区使用设置为`enable`。禁用后，Qt Quick场景图永远不会写入深度缓冲区。
默认情况下，除非`QSG_NO_DEPTH_BUFFER`环境变量被设置，否则该值为真。
默认值为真是绝大多数场景的最优设置。禁用深度缓冲区使用会降低场景图批处理的效率。
不过，在某些情况下，允许写入深度缓冲区的2D内容并不理想。可以考虑将3D场景作为“叠加层”叠加在2D场景之上，通过Qt Quick 3D使用`View3D`渲染，`renderMode`设置为`Overlay`。在这种情况下，深度缓冲区被2D内容填充可能会导致意想不到的结果。这是因为2D场景图渲染器生成和处理深度值的方式不一定与3D场景的工作方式兼容。这可能导致深度值冲突、碰撞和意外的深度测试失败。因此，这里的稳健方法是调用该函数，`enable`设为false，并禁用`QQuickWindow`中二维内容的深度缓冲写入。
注意：该标志与设置`QSG_NO_DEPTH_BUFFER`环境变量不完全相同。该标志不控制深度模板缓冲区的存在。它对渲染流水线相当相关。要强制完全不添加深度/模板附件，设置 `QSG_NO_DEPTH_BUFFER` 和 `QSG_NO_STENCIL_BUFFER`。但请注意，这样的`QQuickWindow`及其中的任何 Item 图层可能会与某些操作模式的 `View3D` Item 不兼容，因为 3D 内容需要深度缓冲。调用该函数总是安全的，但可能导致资源（如深度缓冲区）被创建，尽管它们未被主动使用。

### `void QQuickGraphicsConfiguration::setDeviceExtensions(const QByteArrayList &extensions)`

**作用与语义：**

设置图形设备上需要启用的额外`extensions`列表（例如`VkDevice`）。
当使用图形API渲染时，如果该概念不适用，`extensions`会被忽略。
注意：列表中指定了额外的扩展。Qt Quick 总是启用场景图所需的扩展。

### `[since 6.5] void QQuickGraphicsConfiguration::setPipelineCacheLoadFile(const QString &filename)`

**作用与语义：**

设置 `filename` 是`QQuickWindow`期望从哪里加载其图形/计算流水线缓存的初始内容。默认值为空，意味着流水线缓存加载被禁用。
有关流水线缓存的讨论，请参见“流水线缓存保存与加载”。
持续存储流水线缓存可以提升应用未来的运行性能，因为可以避免昂贵的着色器编译和流水线构建步骤。
文件内容的加载时间并未定义，除此之外，它会在`QQuickWindow`场景图初始化的某个时刻发生。因此，文件在调用该函数后必须继续存在。`QQuickGraphicsConfiguration`仅存储文件名，无法单独执行任何实际的I/O和图形操作。真正的工作将在后续进行，可能是在另一个线程上。
当运行图形 API 时，无法或不支持获取和重新加载流水线缓存（或着色器/程序二进制文件），调用该函数无效。
调用该函数大体等同于将环境变量 `QSG_RHI_PIPELINE_CACHE_LOAD` 设置为 `filename`，但有一个重要区别：该函数仅控制关联`QQuickWindow`的流水线缓存存储。因此，拥有多个`QQuickWindow`或`QQuickView`实例的应用程序可以通过专门为每个窗口存储和重新加载缓存内容。环境变量不允许这样做。
注意：如果文件中的数据在运行时与图形设备和驱动版本不匹配，内容将被忽略，应用程序会被透明地忽略。这适用于许多图形API，必要的检查由Qt负责。也有例外，最显著的是Direct 3D 11，其中“流水线缓存”仅用于存储运行时HLSL->DXBC编译的结果，因此设备和厂商都无关。
警告：串行化的流水线缓存数据被假定为可信内容。建议应用开发者切勿从不受信任的来源传递数据。

### `[since 6.5] void QQuickGraphicsConfiguration::setPipelineCacheSaveFile(const QString &filename)`

**作用与语义：**

设置`QQuickWindow`预期存储图形/计算流水线缓存内容的`filename`。默认值为空，意味着流水线缓存加载被禁用。
有关流水线缓存的讨论，请参见“流水线缓存保存与加载”。
持续存储流水线缓存可以提升应用未来的运行性能，因为可以避免昂贵的着色器编译和流水线构建步骤。
文件的写入时间尚未明确。由于关闭窗口，通常在撕毁场景图时会发生。因此，应用程序不应在`QQuickWindow`完全销毁前假设文件可用。`QQuickGraphicsConfiguration`仅存储文件名，本身不执行任何实际的I/O和图形操作。
当使用图形 API 运行时，获取流水线缓存（或着色器/程序二进制文件）不适用或不支持，调用该函数无效。
调用该函数大多等同于将环境变量 `QSG_RHI_PIPELINE_CACHE_SAVE` 设置为 `filename`，但有一个重要区别：该函数仅控制关联`QQuickWindow`的流水线缓存存储。因此，拥有多个`QQuickWindow`或`QQuickView`实例的应用程序可以通过专门为每个窗口存储并随后重新加载缓存内容。环境变量不允许这样做。

### `[since 6.5] void QQuickGraphicsConfiguration::setPreferSoftwareDevice(bool enable)`

**作用与语义：**

请求选择使用软件光栅化的适配器或物理设备。仅在底层 API 支持枚举适配器（例如 Direct 3D 或 Vulkan）时适用，否则忽略。
如果图形API实现中没有此类图形适配器或物理设备，则请求被忽略。对于直接3D，可以预期始终有基于WARP的光栅器可用。而对于Vulkan，只有当Mesa的`lavapipe`或其他物理设备报告`VK_PHYSICAL_DEVICE_TYPE_CPU`可用时，标志才会生效。
调用该函数时`enable`设为真，相当于将环境变量`QSG_RHI_PREFER_SOFTWARE_RENDERER`设置为非零值。
默认值为假。

### `[since 6.6] void QQuickGraphicsConfiguration::setTimestamps(bool enable)`

**作用与语义：**

启用后，GPU 时序数据会从支持该功能的平台和 3D API 上的命令缓冲区收集。这些数据随后会打印到渲染日志中，渲染器日志可以通过`QSG_RENDER_TIMING`环境变量或日志类别（如 `qt.scenegraph.time.renderloop`）启用，也可以对其他模块（如 Qt Quick 3D 的`DebugView`项）显示。
默认情况下，此功能被禁用，因为收集数据可能需要额外工作，例如根据底层图形API在命令流中插入时间戳查询。启用时，要么调用该函数，`enable`设为true，要么将`QSG_RHI_PROFILE`环境变量设置为非零值。
预计支持此类的图形 API，包括 Direct 3D 11、Direct 3D 12、Vulkan（只要底层 Vulkan 实现支持时间戳查询）、Metal 以及带有核心或兼容性配置文件的 OpenGL，适用于版本 3.3 或更新。OpenGL ES 不支持时间戳。

### `[since 6.6] bool QQuickGraphicsConfiguration::timestampsEnabled() const`

**作用与语义：**

如果启用了 GPU 时序收集，则返回为真。
默认情况下，该值为假。

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

`QQuickGraphicsConfiguration` 所属机制类型：QML 属性绑定与场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
