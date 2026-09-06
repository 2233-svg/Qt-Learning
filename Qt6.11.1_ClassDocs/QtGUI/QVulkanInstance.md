# QVulkanInstance

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QVulkanInstance` 是 Vulkan 动态函数解析机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QVulkanInstance` 是 Vulkan 动态函数解析机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** Qt 不默认静态链接所有 Vulkan 函数，而是通过 `QVulkanInstance` 在运行时解析函数地址。实例级函数由 `QVulkanFunctions` 提供，设备级函数由与具体 `VkDevice` 关联的 `QVulkanDeviceFunctions` 提供。

**适用场景：** 创建并初始化 `QVulkanInstance`，把它绑定到窗口或渲染环境，通过 `functions()` 取得 instance 级函数，通过 `deviceFunctions(device)` 取得 device 级函数，检查返回状态后再调用。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要直接构造 `QVulkanFunctions`/`QVulkanDeviceFunctions`；不要把 instance 级和 device 级函数混用；不要假设扩展函数自动存在；不要忽略平台和驱动能力。

## 2. 依赖与对象关系

- 头文件：`#include <QVulkanInstance>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

Qt 不默认静态链接所有 Vulkan 函数，而是通过 `QVulkanInstance` 在运行时解析函数地址。实例级函数由 `QVulkanFunctions` 提供，设备级函数由与具体 `VkDevice` 关联的 `QVulkanDeviceFunctions` 提供。

### 状态、生命周期和线程

**生命周期：** 函数表依赖对应的 Vulkan instance/device 和有效的函数地址。不能直接构造某些函数表对象，也不能在 instance/device 销毁后继续调用；先完成初始化和设备选择，再取得正确层级的函数表。

**状态与结果：** 要区分 Vulkan loader 不存在、instance 未创建、device 未创建、函数版本/扩展不可用和调用本身返回错误。函数是否可调用还受 Vulkan 头文件版本、运行时驱动和启用扩展影响。

**线程与事件循环：** Vulkan 的线程规则由 Vulkan 对象和命令提交方式决定，Qt 的函数表只负责解析和转发，不替你同步设备访问。窗口/渲染对象还要遵守 Qt Quick 或 QWindow 的线程边界。

## 3. 直接使用

创建并初始化 `QVulkanInstance`，把它绑定到窗口或渲染环境，通过 `functions()` 取得 instance 级函数，通过 `deviceFunctions(device)` 取得 device 级函数，检查返回状态后再调用。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

```cpp
#include <QVulkanFunctions>
#include <QVulkanInstance>

QVulkanInstance instance;
if (instance.create()) {
    QVulkanFunctions *functions = instance.functions();
    // 只有在 instance 初始化完成且函数可用时调用函数表
}
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `DebugFilter`
- `(since 6.5) enum DebugMessageSeverityFlag { VerboseSeverity, InfoSeverity, WarningSeverity, ErrorSeverity }`
- `flags DebugMessageSeverityFlags`
- `(since 6.5) enum DebugMessageTypeFlag { GeneralMessage, ValidationMessage, PerformanceMessage }`
- `flags DebugMessageTypeFlags`
- `(since 6.5) DebugUtilsFilter`
- `enum Flag { NoDebugOutputRedirect, NoPortabilityDrivers }`
- `flags Flags`

### 公有函数

- `QVulkanInstance()`
- `~QVulkanInstance()`
- `QVersionNumber apiVersion() const`
- `(since 6.5) void clearDebugOutputFilters()`
- `bool create()`
- `void destroy()`
- `QVulkanDeviceFunctions * deviceFunctions(VkDevice device)`
- `VkResult errorCode() const`
- `QByteArrayList extensions() const`
- `QVulkanInstance::Flags flags() const`
- `QVulkanFunctions * functions() const`
- `PFN_vkVoidFunction getInstanceProcAddr(const char *name)`
- `(since 6.5) void installDebugOutputFilter(QVulkanInstance::DebugUtilsFilter filter)`
- `void installDebugOutputFilter(QVulkanInstance::DebugFilter filter)`
- `bool isValid() const`
- `QByteArrayList layers() const`
- `void presentAboutToBeQueued(QWindow *window)`
- `void presentQueued(QWindow *window)`
- `void removeDebugOutputFilter(QVulkanInstance::DebugFilter filter)`
- `void resetDeviceFunctions(VkDevice device)`
- `void setApiVersion(const QVersionNumber &vulkanVersion)`
- `void setExtensions(const QByteArrayList &extensions)`
- `void setFlags(QVulkanInstance::Flags flags)`
- `void setLayers(const QByteArrayList &layers)`
- `void setVkInstance(VkInstance existingVkInstance)`
- `QVersionNumber supportedApiVersion() const`
- `QVulkanInfoVector<QVulkanExtension> supportedExtensions() const`
- `QVulkanInfoVector<QVulkanLayer> supportedLayers() const`
- `bool supportsPresent(VkPhysicalDevice physicalDevice, uint32_t queueFamilyIndex, QWindow *window)`
- `VkInstance vkInstance() const`

### 静态公有成员

- `VkSurfaceKHR surfaceForWindow(QWindow *window)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QVulkanInstance::DebugFilter`

**作用与语义：**

用于调试过滤回调函数的Typedef，签名如下：
返回`true`会抑制该信息的印刷。
注意：从 Qt 6.5 开始，使用 `VK_EXT_debug_utils` 代替已废弃的 `VK_EXT_debug_report`。回调签名基于 VK_EXT_debug_report。因此，并非所有参数都有效。避免依赖除 `pMessage`、`messageCode` 和 `object` 以外的参数。希望访问 VK_EXT_debug_utils 中指定的所有回调数据的应用程序应迁移到 `DebugUtilsFilter`。

**官方示例：**

```cpp
 bool myDebugFilter(VkDebugReportFlagsEXT flags, VkDebugReportObjectTypeEXT objectType, uint64_t object,
                    size_t location, int32_t messageCode, const char *pLayerPrefix, const char *pMessage)
```

### `[since 6.5] enum QVulkanInstance::DebugMessageSeverityFlagflags QVulkanInstance::DebugMessageSeverityFlags`

**作用与语义：**

- `QVulkanInstance::VerboseSeverity`：`0x01`
- `QVulkanInstance::InfoSeverity`：`0x02`
- `QVulkanInstance::WarningSeverity`：`0x04`
- `QVulkanInstance::ErrorSeverity`：`0x08`
这个枚举是在Qt 6.5引入的。
DebugMessageSeverityFlags 类型是 QFlags 的 typedef<DebugMessageSeverityFlag>。它存储 DebugMessageSeverityFlag 值的 OR 组合。

### `[since 6.5] enum QVulkanInstance::DebugMessageTypeFlagflags QVulkanInstance::DebugMessageTypeFlags`

**作用与语义：**

- `QVulkanInstance::GeneralMessage`：`0x01`
- `QVulkanInstance::ValidationMessage`：`0x02`
- `QVulkanInstance::PerformanceMessage`：`0x04`
这个枚举是在Qt 6.5引入的。
DebugMessageTypeFlags 类型是 QFlags 的 typedef<DebugMessageTypeFlag>。它存储 DebugMessageTypeFlag 值的 OR 组合。

### `[alias, since 6.5] QVulkanInstance::DebugUtilsFilter`

**作用与语义：**

用于调试过滤回调函数的Typedef，签名如下：
`message`参数指向 VkDebugUtilsMessengerCallbackDataEXT 结构。详情请参阅 `VK_EXT_debug_utils` 文档。Qt 头不使用 real类型，以避免对 1.0 后 Vulkan 头部产生依赖。
返回`true`会抑制该信息的印刷。
这种类型防御是在Qt 6.5中引入的。

**官方示例：**

```cpp
 std::function<bool(DebugMessageSeverityFlags severity, DebugMessageTypeFlags type, const void *message)>;
```

### `enum QVulkanInstance::Flagflags QVulkanInstance::Flags`

**作用与语义：**

这个枚举描述了可以传递给`setFlags()`的标志。这些标志控制`create()`的行为。
- `QVulkanInstance::NoDebugOutputRedirect`：`0x01`;禁用 Vulkan 调试输出（`VK_EXT_debug_utils`）重定向到 `qDebug`。
- `QVulkanInstance::NoPortabilityDrivers (since Qt 6.5)`：`0x02`;禁用标记为Vulkan可携带性实体设备的枚举。
Flags 类型是 QFlags 的 typedef<Flag>。它存储 Flag 值的 OR 组合。

### `QVulkanInstance::QVulkanInstance()`

**作用与语义：**

构建一个新的实例。
注意：构造函数中不执行任何Vulkan初始化。

### `[noexcept] QVulkanInstance::~QVulkanInstance()`

**作用与语义：**

毁灭者。
注意：实例被摧毁后`vkInstance()`会`nullptr`回来。

### `QVersionNumber QVulkanInstance::apiVersion() const`

**作用与语义：**

返回请求的 Vulkan API 版本，应用程序预期运行时会返回，或者如果未调用`setApiVersion()`版本号，则返回空版本号`create()`。

### `[since 6.5] void QVulkanInstance::clearDebugOutputFilters()`

**作用与语义：**

移除`installDebugOutputFilter()`之前安装的所有滤网功能。
注意：该函数可以在`create()`之前调用。

### `bool QVulkanInstance::create()`

**作用与语义：**

初始化 Vulkan 库并创建新实例或采用已有的 Vulkan 实例。
成功时返回 true，错误时返回 false，或不支持 Vulkan 时返回。
成功后，指向该`QVulkanInstance`的指针可以通过`vkInstance()`恢复。
只要该`QVulkanInstance`存在，Vulkan实例和库就会使用，或者直到调用`destroy()`为止。
默认情况下，VkInstance 是用 VK_INSTANCE_CREATE_ENUMERATE_PORTABILITY_BIT_KHR 设置的标志创建的。这意味着 Vulkan 可移植性物理设备也会被枚举。如果不希望这样，可以设置 `NoPortabilityDrivers` 标志。

### `void QVulkanInstance::destroy()`

**作用与语义：**

销毁底层平台实例，从而摧毁Vk实例（当被拥有时）。`QVulkanInstance`对象仍可通过再次调用`create()`重用。

### `QVulkanDeviceFunctions *QVulkanInstance::deviceFunctions(VkDevice device)`

**作用与语义：**

返回暴露设备级核心 Vulkan 命令集的 `QVulkanDeviceFunctions` 对象，且保证跨平台功能正常。
注意：返回对象中的 Vulkan 函数只能以 `device` 或 `device` 的子对象（VkQueue、VkCommandBuffer）作为首参数调用。这是因为这些函数通过 vkGetDeviceProcAddr 解析，以避免内部调度的潜在开销。
注意：归还物品归`QVulkanInstance`所有和管理。请勿销毁或更改。
注意：该对象是缓存的，因此再次用相同`device`调用该函数是一种廉价操作。然而，当设备被摧毁时，应用程序需通过调用`resetDeviceFunctions()`通知`QVulkanInstance`。
核心 Vulkan 1.0 API 的功能将始终可用。对于更高版本的 Vulkan，如 1.1 和 1.2，`QVulkanDeviceFunctions` 对象会尝试解析这些核心 API 函数，但如果运行时 Vulkan 物理设备不支持这些功能，调用任何不支持函数会导致未指定行为。为了正确启用对 1.0 以上版本的支持，可能需要在 `create()` 前调用 `setApiVersion()` 来设置合适的实例 API 版本。此外，应用程序还应在 VkPhysicalDeviceProperties 中检查物理设备的 `apiVersion`。

### `VkResult QVulkanInstance::errorCode() const`

**作用与语义：**

在未成功`create()`后返回Vulkan错误代码，`VK_SUCCESS`其他情况。
该值通常是 vkCreateInstance() 的返回值（创建新 Vulkan 实例而非采用现有实例时），但如果平台插件不支持 Vulkan，也可能`VK_NOT_READY`。

### `QByteArrayList QVulkanInstance::extensions() const`

**作用与语义：**

如果调用`create()`且成功，则返回启用的实例扩展。否则返回请求的扩展。

### `QVulkanInstance::Flags QVulkanInstance::flags() const`

**作用与语义：**

返回请求的标志。

### `QVulkanFunctions *QVulkanInstance::functions() const`

**作用与语义：**

返回对应的`QVulkanFunctions`对象，该对象暴露核心 Vulkan 命令集，排除设备级功能，且保证跨平台功能。
注意：归还的物品由`QVulkanInstance`拥有和管理。请勿销毁或更改。
核心 Vulkan 1.0 API 中的函数将始终可用。对于更高版本的 Vulkan，如 1.1 和 1.2，`QVulkanFunctions` 对象也会尝试解析这些核心 API 函数，但如果运行时 Vulkan 实例实现不支持这些功能，调用任何不支持的函数会导致不确定的行为。此外，为了正确启用对 1.0 以上版本的支持，可能需要在 `create()` 前调用 `setApiVersion()` 来设置合适的实例 API 版本。要查询 Vulkan 实现的实例级版本，请调用 `supportedApiVersion()`。

### `PFN_vkVoidFunction QVulkanInstance::getInstanceProcAddr(const char *name)`

**作用与语义：**

用给定的 `name` 解析 Vulkan 函数。
对于核心，Vulkan命令更倾向于使用可从`functions()`和`deviceFunctions()`检索的函数包装器。

### `[since 6.5] void QVulkanInstance::installDebugOutputFilter(QVulkanInstance::DebugUtilsFilter filter)`

**作用与语义：**

安装一个`filter`函数，每个 Vulkan 调试消息都会调用。当回调返回 `true` 时，消息被停止（过滤掉），不会出现在调试输出中。
注意：过滤只有在`NoDebugOutputRedirect`未`set`时才有效。安装过滤器在其他情况下没有效果。
注意：该函数可以在 `create()` 之前调用。

### `void QVulkanInstance::installDebugOutputFilter(QVulkanInstance::DebugFilter filter)`

**作用与语义：**

安装一个`filter`函数，每个 Vulkan 调试消息都会调用。当回调返回 `true` 时，消息被停止（过滤掉），不会出现在调试输出中。
注意：过滤只有在`NoDebugOutputRedirect`未`set`时才有效。安装过滤器在其他情况下没有效果。
注意：该函数可以在 `create()` 之前调用。

### `bool QVulkanInstance::isValid() const`

**作用与语义：**

如果`create()`成功且实例有效，则返回为真。

### `QByteArrayList QVulkanInstance::layers() const`

**作用与语义：**

如果调用`create()`且成功，则返回启用的实例层。否则返回请求的层。

### `void QVulkanInstance::presentAboutToBeQueued(QWindow *window)`

**作用与语义：**

该函数应由应用程序的渲染器调用，然后排队当前操作以获得`window`。
虽然在某些平台上这不允许操作，但有些平台可能会执行窗口系统相关的同步。例如，在Wayland上，这会增加发送wl_surface.帧请求，以防止驱动在最小化窗口时阻塞。

### `void QVulkanInstance::presentQueued(QWindow *window)`

**作用与语义：**

该函数应由应用程序渲染器在排队完成当前操作后调用`window`。
虽然在某些平台上这会是无操作操作，但有些平台可能会执行依赖窗口系统的同步。例如，在X11上，这会更新`_NET_WM_SYNC_REQUEST_COUNTER`。

### `void QVulkanInstance::removeDebugOutputFilter(QVulkanInstance::DebugFilter filter)`

**作用与语义：**

移除`installDebugOutputFilter()`之前安装的`filter`功能。
注意：该函数可以在`create()`之前调用。

### `void QVulkanInstance::resetDeviceFunctions(VkDevice device)`

**作用与语义：**

使给定`device`的`QVulkanDeviceFunctions`对象失效并销毁。
当调用`deviceFunctions()`的VkDevice在应用计划继续运行时被销毁，可能在后续创建新的逻辑Vulkan设备时，必须调用该函数。
在销毁`QVulkanInstance`之前无需调用，因为清理工作会自动完成。

### `void QVulkanInstance::setApiVersion(const QVersionNumber &vulkanVersion)`

**作用与语义：**

指定应用程序设计使用的最高 Vulkan API 版本。
默认情况下，`vulkanVersion`是0，映射到Vulkan 1.0。
注意：该函数只能在`create()`之前调用，之后调用则无效。
注意：注意 Vulkan 1.1 改变了 Vulkan API 版本字段的行为。在 Vulkan 1.0 中，指定不支持的`vulkanVersion`会导致`VK_ERROR_INCOMPATIBLE_DRIVER` `create()`失败，这是规范要求的。从 Vulkan 1.1 开始，规范禁止此操作，驱动程序必须接受任何版本且不会失败实例创建。
建议应用开发者熟悉 Vulkan 规范中的 `apiVersion` 说明。

### `void QVulkanInstance::setExtensions(const QByteArrayList &extensions)`

**作用与语义：**

指定需要启用的额外实例`extensions`列表。也可以安全地指定不支持的扩展，因为运行时这些扩展不支持时会被忽略。
注意：Qt 要求的与表面相关的扩展（例如 `VK_KHR_win32_surface`）始终会自动添加，无需在此列表中包含。
注意：除非设置`NoPortabilityDrivers`标志，否则`VK_KHR_portability_enumeration`会自动添加。该值是在第6.5个Qt中引入的。
注意：该函数只能在`create()`之前调用，若在后调用则无效。

### `void QVulkanInstance::setFlags(QVulkanInstance::Flags flags)`

**作用与语义：**

根据提供的 `flags`配置`create()`的行为。
注意：该函数只能在`create()`之前调用，之后调用则无效。

### `void QVulkanInstance::setLayers(const QByteArrayList &layers)`

**作用与语义：**

指定启用实例`layers`列表。也可以安全地指定不支持层，因为运行时不支持时这些层会被忽略。
注意：该函数只能在`create()`之前调用，之后调用则无效。

### `void QVulkanInstance::setVkInstance(VkInstance existingVkInstance)`

**作用与语义：**

让`QVulkanInstance`采用已有的 VkInstance 句柄，而不是创建一个新的。
注意：`existingVkInstance`必须至少启用`VK_KHR_surface`并启用相应的 WSI 专用 `VK_KHR_*_surface`扩展。为确保调试输出重定向功能正常，还需要`VK_EXT_debug_utils`。
注意：该函数只能在 `create()` 之前调用，之后调用则无效。

### `QVersionNumber QVulkanInstance::supportedApiVersion() const`

**作用与语义：**

返回由 Vulkan 实现支持的实例级功能版本。
实际上，这要么是vkEnumerateInstanceVersion返回的值（如果该函数可用，Vulkan 1.1及更新版本），要么是1.0。
希望根据运行时可用的 Vulkan 版本分支其 Vulkan 功能和 API 使用情况的应用程序，可以用该函数确定在调用 `create()` 前传入哪个版本给`setApiVersion()`。
注意：该函数可以在`create()`之前调用。

### `QVulkanInfoVector<QVulkanExtension> QVulkanInstance::supportedExtensions() const`

**作用与语义：**

返回支持的实例级扩展列表。
注意：该函数可以在`create()`之前调用。

### `QVulkanInfoVector<QVulkanLayer> QVulkanInstance::supportedLayers() const`

**作用与语义：**

返回支持的实例级层列表。
注意：该函数可以在 `create()` 之前调用。

### `bool QVulkanInstance::supportsPresent(VkPhysicalDevice physicalDevice, uint32_t queueFamilyIndex, QWindow *window)`

**作用与语义：**

如果队列家族中`queueFamilyIndex` `physicalDevice`支持向`window`呈现，则返回为真。
在检查某台 Vulkan 设备的队列时调用该函数，以决定哪个队列可用于演示。

### `[static] VkSurfaceKHR QVulkanInstance::surfaceForWindow(QWindow *window)`

**作用与语义：**

创建或检索给定`window`已有的`VkSurfaceKHR`柄。
失败时返回Vulkan表面手柄或0。

### `VkInstance QVulkanInstance::vkInstance() const`

**作用与语义：**

返回 VkInstance 处理`QVulkanInstance`包裹，或者如果尚未成功调用`create()`且未通过 `setVkInstance()` 提供现有实例，则返回 `nullptr`。

### `DebugFilter`

**作用与语义：**

用于调试过滤回调函数的Typedef，签名如下：
返回`true`会抑制该信息的印刷。
注意：从 Qt 6.5 开始，使用 `VK_EXT_debug_utils` 代替已废弃的 `VK_EXT_debug_report`。回调签名基于 VK_EXT_debug_report。因此，并非所有参数都有效。避免依赖除 `pMessage`、`messageCode` 和 `object` 以外的参数。希望访问 VK_EXT_debug_utils 中指定的所有回调数据的应用程序应迁移到 `DebugUtilsFilter`。

**官方示例：**

```cpp
 bool myDebugFilter(VkDebugReportFlagsEXT flags, VkDebugReportObjectTypeEXT objectType, uint64_t object,
                    size_t location, int32_t messageCode, const char *pLayerPrefix, const char *pMessage)
```

### `(since 6.5) enum DebugMessageSeverityFlag { VerboseSeverity, InfoSeverity, WarningSeverity, ErrorSeverity }`

**作用与语义：**

- `QVulkanInstance::VerboseSeverity`：`0x01`
- `QVulkanInstance::InfoSeverity`：`0x02`
- `QVulkanInstance::WarningSeverity`：`0x04`
- `QVulkanInstance::ErrorSeverity`：`0x08`
这个枚举是在Qt 6.5引入的。
DebugMessageSeverityFlags 类型是 QFlags 的 typedef<DebugMessageSeverityFlag>。它存储 DebugMessageSeverityFlag 值的 OR 组合。

### `flags DebugMessageSeverityFlags`

**作用与语义：**

- `QVulkanInstance::VerboseSeverity`：`0x01`
- `QVulkanInstance::InfoSeverity`：`0x02`
- `QVulkanInstance::WarningSeverity`：`0x04`
- `QVulkanInstance::ErrorSeverity`：`0x08`
这个枚举是在Qt 6.5引入的。
DebugMessageSeverityFlags 类型是 QFlags 的 typedef<DebugMessageSeverityFlag>。它存储 DebugMessageSeverityFlag 值的 OR 组合。

### `(since 6.5) enum DebugMessageTypeFlag { GeneralMessage, ValidationMessage, PerformanceMessage }`

**作用与语义：**

- `QVulkanInstance::GeneralMessage`：`0x01`
- `QVulkanInstance::ValidationMessage`：`0x02`
- `QVulkanInstance::PerformanceMessage`：`0x04`
这个枚举是在Qt 6.5引入的。
DebugMessageTypeFlags 类型是 QFlags 的 typedef<DebugMessageTypeFlag>。它存储 DebugMessageTypeFlag 值的 OR 组合。

### `flags DebugMessageTypeFlags`

**作用与语义：**

- `QVulkanInstance::GeneralMessage`：`0x01`
- `QVulkanInstance::ValidationMessage`：`0x02`
- `QVulkanInstance::PerformanceMessage`：`0x04`
这个枚举是在Qt 6.5引入的。
DebugMessageTypeFlags 类型是 QFlags 的 typedef<DebugMessageTypeFlag>。它存储 DebugMessageTypeFlag 值的 OR 组合。

### `(since 6.5) DebugUtilsFilter`

**作用与语义：**

用于调试过滤回调函数的Typedef，签名如下：
`message`参数指向 VkDebugUtilsMessengerCallbackDataEXT 结构。详情请参阅 `VK_EXT_debug_utils` 文档。Qt 头不使用 real类型，以避免对 1.0 后 Vulkan 头部产生依赖。
返回`true`会抑制该信息的印刷。
这种类型防御是在Qt 6.5中引入的。

**官方示例：**

```cpp
 std::function<bool(DebugMessageSeverityFlags severity, DebugMessageTypeFlags type, const void *message)>;
```

### `enum Flag { NoDebugOutputRedirect, NoPortabilityDrivers }`

**作用与语义：**

这个枚举描述了可以传递给`setFlags()`的标志。这些标志控制`create()`的行为。
- `QVulkanInstance::NoDebugOutputRedirect`：`0x01`;禁用 Vulkan 调试输出（`VK_EXT_debug_utils`）重定向到 `qDebug`。
- `QVulkanInstance::NoPortabilityDrivers (since Qt 6.5)`：`0x02`;禁用标记为Vulkan可携带性实体设备的枚举。
Flags 类型是 QFlags 的 typedef<Flag>。它存储 Flag 值的 OR 组合。

### `flags Flags`

**作用与语义：**

这个枚举描述了可以传递给`setFlags()`的标志。这些标志控制`create()`的行为。
- `QVulkanInstance::NoDebugOutputRedirect`：`0x01`;禁用 Vulkan 调试输出（`VK_EXT_debug_utils`）重定向到 `qDebug`。
- `QVulkanInstance::NoPortabilityDrivers (since Qt 6.5)`：`0x02`;禁用标记为Vulkan可携带性实体设备的枚举。
Flags 类型是 QFlags 的 typedef<Flag>。它存储 Flag 值的 OR 组合。

## 6. 深入实践与常见坑

### 生命周期和资源边界

函数表依赖对应的 Vulkan instance/device 和有效的函数地址。不能直接构造某些函数表对象，也不能在 instance/device 销毁后继续调用；先完成初始化和设备选择，再取得正确层级的函数表。

### 状态和错误边界

要区分 Vulkan loader 不存在、instance 未创建、device 未创建、函数版本/扩展不可用和调用本身返回错误。函数是否可调用还受 Vulkan 头文件版本、运行时驱动和启用扩展影响。

### 线程边界

Vulkan 的线程规则由 Vulkan 对象和命令提交方式决定，Qt 的函数表只负责解析和转发，不替你同步设备访问。窗口/渲染对象还要遵守 Qt Quick 或 QWindow 的线程边界。

### 最容易出现的错误

不要直接构造 `QVulkanFunctions`/`QVulkanDeviceFunctions`；不要把 instance 级和 device 级函数混用；不要假设扩展函数自动存在；不要忽略平台和驱动能力。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QVulkanInstance` 所属机制类型：Vulkan 动态函数解析机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
