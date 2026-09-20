# QVulkanInstance 深入笔记

> 适用版本：Qt 6.11.1
> 头文件：`#include <QVulkanInstance>`
> 所属模块：`Qt6::Gui`
> 继承：无

## 它解决什么问题

`QVulkanInstance` 是 Qt 对 Vulkan instance 和 Vulkan loader 的跨平台封装。它负责在运行时加载 Vulkan 库、查询 instance 层和扩展、创建或接管 `VkInstance`，并为 Qt 的 `QWindow`、`QVulkanFunctions`、`QVulkanDeviceFunctions` 提供共同的入口。

它解决的是 Vulkan 初始化中最靠前、也最容易被平台差异污染的一层：应用不需要自己处理每个平台的 Vulkan loader 名称、surface 创建细节和 instance 级函数解析，就可以把一个 `QWindow` 关联到可用的 Vulkan instance。

`QVulkanInstance` 不是 logical device，也不是渲染上下文。它不负责创建 swapchain、command buffer 或 graphics pipeline；这些工作要么由应用自己完成，要么交给 `QVulkanWindow`。

## 实际使用场景

- 创建一个供多个 Vulkan 窗口使用的应用级 `VkInstance`。
- 在创建 instance 前检查验证层、调试层和平台 WSI 扩展。
- 把已有渲染引擎创建的 `VkInstance` 交给 Qt，使 Qt 窗口使用外部 Vulkan 初始化。
- 取得 instance 级核心函数、device 级函数，以及窗口的原生 `VkSurfaceKHR`。
- 安装 Vulkan debug message 过滤器，把验证层噪声压掉或按类别筛选。

## 使用模型

典型顺序是：先创建 `QGuiApplication`，再创建 `QVulkanInstance`，按需要调用 `setLayers()`、`setExtensions()`、`setApiVersion()`、`setFlags()`，最后调用 `create()`。创建成功后，把它传给每一个 Vulkan 窗口的 `QWindow::setVulkanInstance()`。

`QVulkanInstance` 的构造函数不会立即加载 Vulkan 或创建 `VkInstance`。真正初始化发生在 `create()`。这允许把实例作为 `main()` 中的普通成员变量保存，并把初始化失败作为可处理的运行时情况。

`supportedLayers()` 和 `supportedExtensions()` 可以在 `create()` 之前调用；它们会触发 Vulkan 库加载，用来决定哪些层和扩展值得请求。请求了但当前环境不支持的层或扩展会被忽略，所以 `create()` 成功后应再通过 `layers()`、`extensions()` 检查实际启用结果。

默认情况下 Qt 创建并拥有底层 `VkInstance`。如果调用 `setVkInstance()` 传入已有句柄，Qt 只接管访问，不拥有也不销毁这个句柄；外部创建者必须保证必要的 `VK_KHR_surface`、平台 WSI 扩展以及需要时的 `VK_EXT_debug_utils` 已经启用。

## 生命周期、所有权与线程边界

一个 `QVulkanInstance` 通常贯穿整个 GUI 应用生命周期。`create()` 成功后，`vkInstance()`、`functions()` 和由它创建的 device 函数表才有可用的底层环境；调用 `destroy()` 后对象仍可复用，但此前取得的函数表指针和 Vulkan 句柄都应视为失效。

`functions()` 返回的 `QVulkanFunctions *` 和 `deviceFunctions()` 返回的 `QVulkanDeviceFunctions *` 都由 `QVulkanInstance` 管理，应用不能删除、修改或长期跨 instance 生命周期保存它们。logical device 销毁后，要调用 `resetDeviceFunctions(device)` 通知 Qt 清除对应缓存。

创建 Vulkan 窗口时，Qt 平台插件参与 surface 创建，平台本身不一定支持 Vulkan；这时 `create()` 可能失败。失败后用 `errorCode()` 获取 Vulkan 错误，并把 Vulkan 不可用当作正常降级路径。

## 关键语义与边界

`setApiVersion()` 设置的是应用请求的 Vulkan API 版本，不是强行把物理设备升级到该版本。对于 1.1、1.2、1.3 等高版本命令，还要同时检查运行时物理设备的 API 版本；函数表能解析出声明并不意味着当前设备可以安全调用。

`surfaceForWindow()` 可能在第一次调用时创建平台 surface，后续调用通常返回同一个句柄。`supportsPresent()` 同时封装通用的 surface 支持查询和平台特有的 presentation 支持查询，适合选择能同时承担图形和 present 的 queue family。

Qt 默认把 Vulkan debug output 重定向到 `qDebug()`。`NoDebugOutputRedirect` 必须在 `create()` 前设置；过滤器只有在重定向开启时才有效。Qt 6.5 起优先使用 `DebugUtilsFilter`，旧的 `DebugFilter` 基于已弃用的 debug report 回调，能获得的参数不如新接口完整。

`presentAboutToBeQueued()` 和 `presentQueued()` 是给自定义 renderer 使用的平台同步钩子，必须围绕实际的 present 提交调用成对使用。在某些平台上它们是空操作，在 Wayland 或 X11 等平台上可能影响窗口系统同步。

## 常见误区

- 以为构造 `QVulkanInstance` 就已经创建了 Vulkan instance；真正初始化要到 `create()`。
- 不检查 `supportedLayers()`/`supportedExtensions()`，把验证层或 WSI 扩展是否存在想当然。
- `create()` 成功后仍用 `layers()` 的请求列表判断实际启用情况；应读取成功后的实际列表。
- 把 `functions()` 或 `deviceFunctions()` 返回对象当成应用拥有的对象并手动删除。
- 传入外部 `VkInstance` 后忘记由外部创建者启用 Qt 所需的 surface 扩展。
- 在 `VkDevice` 销毁后不调用 `resetDeviceFunctions()`，之后又用同一设备句柄创建新设备。
- 把 `NoPortabilityDrivers` 当成“禁用所有非原生设备”；它只控制标记为 Vulkan Portability 的物理设备枚举。

## API 速查表

| API | 作用 | 重点注意 |
| --- | --- | --- |
| `using DebugFilter` | 定义旧版 Vulkan debug report 过滤回调类型。返回 `true` 可抑制消息。 | Qt 6.5 起优先使用 `DebugUtilsFilter`；旧回调的部分参数可能不可用。 |
| `enum DebugMessageSeverityFlag` / `DebugMessageSeverityFlags` | 表示 debug utils 消息严重级别：verbose、info、warning、error。 | Qt 6.5 引入；flags 是多个级别的 OR 组合。 |
| `enum DebugMessageTypeFlag` / `DebugMessageTypeFlags` | 表示 general、validation、performance 消息类别。 | Qt 6.5 引入；flags 可组合。 |
| `using DebugUtilsFilter` | 定义新版 debug utils 过滤器回调。 | 回调收到严重级别、消息类型和 `VkDebugUtilsMessengerCallbackDataEXT` 语义的指针；返回 `true` 抑制输出。 |
| `enum Flag` / `Flags` | 控制 instance 创建行为的选项集合。 | 使用 `QFlags` 组合标志。 |
| `QVulkanInstance::NoDebugOutputRedirect` | 禁止 Qt 把 Vulkan debug output 重定向到 `qDebug()`。 | 必须在 `create()` 前设置；设置后过滤器也不会生效。 |
| `QVulkanInstance::NoPortabilityDrivers` | 禁止枚举被标记为 Vulkan Portability 的物理设备。 | Qt 6.5 引入；只影响物理设备枚举。 |
| `QVulkanInstance::QVulkanInstance()` | 构造一个尚未初始化的 Qt Vulkan instance 对象。 | 构造函数不加载 Vulkan，也不创建 `VkInstance`。 |
| `[noexcept] ~QVulkanInstance()` | 销毁包装对象和 Qt 自己拥有的底层 instance。 | 外部传入的 `VkInstance` 不由 Qt 销毁。 |
| `QVersionNumber apiVersion() const` | 返回应用通过 `setApiVersion()` 请求的 API 版本。 | 未设置时返回空版本号；这是请求值，不是运行时实际支持值。 |
| `[since 6.5] void clearDebugOutputFilters()` | 移除之前安装的所有 debug utils 过滤器。 | 可在 `create()` 前调用；只影响 Qt 的过滤器列表。 |
| `bool create()` | 加载 Vulkan 并创建新 `VkInstance`，或采用 `setVkInstance()` 提供的句柄。 | 失败返回 `false`；平台不支持 Vulkan 时也可能失败。 |
| `void destroy()` | 销毁底层 instance；若是外部句柄则只解除 Qt 的使用。 | 对象本身仍可再次 `create()`；旧句柄和函数表不能继续使用。 |
| `QVulkanDeviceFunctions *deviceFunctions(VkDevice device)` | 返回绑定到指定 `VkDevice` 的 device 级核心函数表。 | 返回对象由 Qt 拥有；只能把该 device 或其子对象作为命令的首参数。 |
| `VkResult errorCode() const` | 返回最近一次失败 `create()` 的 Vulkan 错误码。 | 成功时返回 `VK_SUCCESS`；平台插件不支持时也可能是 `VK_NOT_READY`。 |
| `QByteArrayList extensions() const` | 返回请求或实际启用的 instance extensions。 | `create()` 成功后是实际启用列表，之前是请求列表。 |
| `Flags flags() const` | 返回当前请求的创建标志。 | 返回的是 `setFlags()` 设置的值。 |
| `QVulkanFunctions *functions() const` | 返回 instance 级核心 Vulkan 函数表。 | 由 Qt 管理；高于 1.0 的命令仍要检查 API 版本。 |
| `PFN_vkVoidFunction getInstanceProcAddr(const char *name)` | 按名称解析 Vulkan instance 级函数地址。 | 核心命令优先使用 `functions()`；扩展命令要确认扩展已启用。 |
| `[since 6.5] void installDebugOutputFilter(DebugUtilsFilter filter)` | 安装新版 debug utils 消息过滤器。 | 必须保证回调捕获对象的生命周期足够长；返回 `true` 会抑制输出。 |
| `void installDebugOutputFilter(DebugFilter filter)` | 安装旧版 debug report 过滤器。 | 旧接口信息不完整；需要完整 debug utils 数据时使用新版重载。 |
| `bool isValid() const` | 判断 Qt 是否当前持有有效的 Vulkan instance。 | `destroy()` 后为假；不能只用对象是否构造来判断。 |
| `QByteArrayList layers() const` | 返回请求或实际启用的 instance layers。 | `create()` 成功后读取实际启用结果；不支持的请求会被忽略。 |
| `void presentAboutToBeQueued(QWindow *window)` | 在自定义 renderer 排队 present 前通知 Qt。 | 与 `presentQueued()` 成对使用，服务于平台窗口同步。 |
| `void presentQueued(QWindow *window)` | 在自定义 renderer 排队 present 后通知 Qt。 | 必须对应之前的 `presentAboutToBeQueued()`。 |
| `void removeDebugOutputFilter(DebugFilter filter)` | 移除之前安装的旧版 debug report 过滤器。 | 仅针对 `DebugFilter`；新版过滤器使用 `clearDebugOutputFilters()` 统一清除。 |
| `void resetDeviceFunctions(VkDevice device)` | 清除指定 logical device 的函数表缓存。 | 应在应用销毁该 `VkDevice` 后调用。 |
| `void setApiVersion(const QVersionNumber &vulkanVersion)` | 设置创建 instance 时请求的 Vulkan API 版本。 | 要在 `create()` 前设置；还要检查物理设备运行时版本。 |
| `void setExtensions(const QByteArrayList &extensions)` | 设置要请求启用的 instance extensions。 | 应在 `create()` 前设置；不支持项会被忽略。 |
| `void setFlags(Flags flags)` | 设置 instance 创建行为标志。 | 典型地在 `create()` 前设置。 |
| `void setLayers(const QByteArrayList &layers)` | 设置要请求启用的 instance layers。 | 验证层名称必须精确；不支持的层会被忽略。 |
| `void setVkInstance(VkInstance existingVkInstance)` | 让 Qt 采用已有的 `VkInstance` 而不再创建新的。 | Qt 不拥有、不销毁该句柄；外部 instance 必须已启用 Qt 所需扩展。 |
| `QVersionNumber supportedApiVersion() const` | 查询 Vulkan 实现支持的 instance 级 API 版本。 | 可用于 `create()` 前决策；不要和 `apiVersion()` 的请求值混淆。 |
| `QVulkanInfoVector<QVulkanExtension> supportedExtensions() const` | 查询系统可用的 instance extension。 | 可在 `create()` 前调用；只表示支持，不表示已启用。 |
| `QVulkanInfoVector<QVulkanLayer> supportedLayers() const` | 查询系统可用的 instance layer。 | 可在 `create()` 前调用；适合决定是否请求验证层。 |
| `bool supportsPresent(VkPhysicalDevice physicalDevice, uint32_t queueFamilyIndex, QWindow *window)` | 判断某物理设备的 queue family 能否向指定窗口 present。 | 选择 graphics/present queue 时调用；需要有效窗口和物理设备。 |
| `[static] VkSurfaceKHR surfaceForWindow(QWindow *window)` | 为窗口创建或取得平台原生 Vulkan surface。 | 失败返回 `0`；第一次调用可能触发平台资源创建。 |
| `VkInstance vkInstance() const` | 返回 Qt 包装或采用的原生 `VkInstance` 句柄。 | `destroy()` 后返回空句柄；不转移所有权。 |

## 一句话总结

`QVulkanInstance` 管理 Vulkan 初始化的根：先在 `create()` 前做版本、layer、extension 配置，再把有效 instance 交给窗口和函数表使用。
