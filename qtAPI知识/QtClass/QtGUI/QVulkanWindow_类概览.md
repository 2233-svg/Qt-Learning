# QVulkanWindow 深入笔记

> 适用版本：Qt 6.11.1
> 头文件：`#include <QVulkanWindow>`
> 所属模块：`Qt6::Gui`
> 继承：`QWindow -> QVulkanWindow`

## 它解决什么问题

`QVulkanWindow` 是 Qt 对常见 Vulkan 窗口渲染流程的高层封装。它继承自 `QWindow`，自动管理 Vulkan surface、物理设备、logical device、graphics queue、command pool、主 command buffer、depth-stencil 资源和 FIFO swapchain，并处理 resize、窗口暂时不可见、设备丢失和部分截图读回场景。

它解决的是“应用只想实现自己的绘制逻辑，却不想重复编写一整套窗口化 Vulkan 初始化和 swapchain 重建代码”的问题。应用通过 `createRenderer()` 返回 `QVulkanWindowRenderer`，在约定的回调里创建资源、录制命令并调用 `frameReady()`。

它不是所有 Vulkan 项目的万能窗口基类。需要复杂多窗口同步、特殊 surface、多个独立 swapchain、特殊 present 模式或完全自定义 device 创建流程时，仍可能需要直接继承 `QWindow`。

## 实际使用场景

- 编写一个带 Vulkan 画面的 Qt GUI 窗口。
- 用一套 renderer 回调管理长期 GPU 资源和 resize 相关资源。
- 使用 Qt 已准备好的当前 framebuffer、command buffer、graphics queue 和 swapchain image。
- 通过 `setSampleCount()`、`setPreferredColorFormats()` 配置 MSAA 和 sRGB。
- 用 `setEnabledFeaturesModifier()`、`setQueueCreateInfoModifier()` 补充 device feature 和 queue 创建策略。
- 用 `grab()` 做截图、自动化测试或 GPU 输出验证。

## 使用模型

先创建 `QGuiApplication` 和 `QVulkanInstance`，成功后把 instance 传给窗口的 `QWindow::setVulkanInstance()`。`QVulkanWindow` 构造时会把 surface 类型设成 `QSurface::VulkanSurface`；窗口第一次 expose 后才真正开始图形初始化。

窗口子类通常只需重写 `createRenderer()` 并返回一个 `QVulkanWindowRenderer`。窗口取得 renderer 的所有权，renderer 的生命周期跟随窗口。初始化前配置，例如 device extensions、物理设备索引、sample count、颜色格式和 feature modifier，都应在窗口显示前完成，最迟也要在 `preInitResources()` 阶段之前完成。

renderer 的回调分成三层：

- `preInitResources()`：物理设备和 surface 已可用，logical device 尚未完成，适合做二者联合决策。
- `initResources()` / `releaseResources()`：管理 device、graphics queue、command pool 以及不依赖 swapchain 尺寸的长期资源。
- `initSwapChainResources()` / `releaseSwapChainResources()`：管理 framebuffer、depth-stencil、MSAA、render pass 和尺寸相关资源，窗口 resize 时可能反复调用。
- `startNextFrame()`：向当前 command buffer 添加本帧命令；完成后必须让 `frameReady()` 恰好调用一次。

## 生命周期、所有权与线程边界

`QVulkanWindow` 在第一次 expose 后才会初始化 Vulkan 资源；`isValid()` 只有在 device 和 swapchain 都成功初始化后才返回 `true`。窗口变为不可见时，默认会释放图形资源并在重新可见时初始化；设置 `PersistentResources` 可以改变这个行为。

renderer 的回调默认在 GUI/main 线程执行，但 `startNextFrame()` 可以启动异步工作。当前 command buffer 等访问器在异步生成期间可以继续使用到 `frameReady()`；然而 `frameReady()` 本身必须在 GUI/main 线程调用，且每次 `startNextFrame()` 只能调用一次。

Qt 会在释放资源前后等待 device idle，但应用创建的额外 Vulkan 资源仍要由应用自己销毁。device lost 后，旧的 device、queue、command pool、pipeline、descriptor 和 image 都不能继续使用。

## 关键语义与边界

`currentCommandBuffer()`、`currentFramebuffer()`、`currentFrame()`、`currentSwapChainImageIndex()` 只在 `startNextFrame()` 到 `frameReady()` 之间有效。不要在普通 UI 事件、构造函数或资源释放之后缓存并调用这些句柄。

`initResources()` 中有效的 `device()`、`graphicsQueue()`、`graphicsCommandPool()`、`colorFormat()` 等访问器，会在 `releaseResources()` 后失效。`initSwapChainResources()` 中有效的 swapchain image、image view、depth-stencil、MSAA 和 `swapChainImageSize()`，会在 `releaseSwapChainResources()` 后失效。

`swapChainImageSize()` 应作为渲染尺寸的唯一依据。高 DPI 或平台 surface capability 可能使它和 `QWindow::size() * devicePixelRatio()` 存在一像素差异，viewport、projection 和 framebuffer 相关计算应使用 Vulkan 报告的尺寸。

`setSampleCount()` 不会像 `QSurfaceFormat::setSamples()` 那样自动退回较低采样数。先读 `supportedSampleCounts()`；如果请求值不支持，Qt 会警告并禁用多重采样。启用 MSAA 后，默认 framebuffer 会包含 resolve 和 multisample 相关附件，clear value 数量也要相应处理。

`grab()` 是阻塞读回，开销较大，只在 `supportsGrab()` 为 `true` 且当前没有进行中的 frame 时调用。同步 renderer 会直接返回完整图像；异步 renderer 可能先返回只有尺寸的图像，最终内容通过 `frameGrabbed()` 提供。

## 常见误区

- 在窗口显示后才设置 device extension、物理设备索引或 sample count，配置已经不再生效。
- 忘记给每个 `startNextFrame()` 配对调用一次 `frameReady()`，渲染循环会停住。
- 把 resize 相关对象放在 `initResources()`，窗口变化后继续使用旧 framebuffer 或 projection。
- 用 `QWindow::size()` 代替 `swapChainImageSize()`，在高 DPI 平台造成 viewport 越界。
- 请求不支持的 sample count 却期待 Qt 自动降级。
- 把 `QVector3D::project()` 的坐标系修正和 `clipCorrectionMatrix()` 的职责混在一起；后者是投影矩阵配套修正。
- 在 frame 进行中调用 `grab()`，或在不支持 transfer source 的 swapchain 上强行截图。
- 在 feature modifier 中把 `pNext` 指向临时局部变量，回调结束后结构链已经悬空。

## API 速查表

| API | 作用 | 重点注意 |
| --- | --- | --- |
| `[since 6.7] using EnabledFeatures2Modifier` | 在创建设备时修改 `VkPhysicalDeviceFeatures2`，可设置新版本 feature 和 `pNext` 链。 | 被引用的扩展结构必须活得足够久；不要指向临时变量。 |
| `using EnabledFeaturesModifier` | 在创建设备时修改 Vulkan 1.0 的 `VkPhysicalDeviceFeatures`。 | 回调收到的结构初始为零；控制 1.1+ feature 应使用 `EnabledFeatures2Modifier`。 |
| `enum Flag` / `Flags` | 控制窗口资源策略。 | 使用 `QFlags` 组合标志。 |
| `QVulkanWindow::PersistentResources` | 窗口不可见时保留图形资源。 | 默认会释放并在重新可见时重建；保留资源会增加占用。 |
| `using QueueCreateInfoModifier` | 在 device 初始化时追加或修改 queue create info。 | Qt 始终会请求 graphics queue；追加 graphics queue 时要检查已有条目。 |
| `[explicit] QVulkanWindow(QWindow *parent = nullptr)` | 构造 Vulkan 窗口并把 surface 类型设为 Vulkan surface。 | 仍需关联有效的 `QVulkanInstance`，并在 GUI 应用中使用。 |
| `[virtual noexcept] ~QVulkanWindow()` | 销毁窗口及 Qt 管理的 Vulkan 资源和 renderer。 | 应确保应用自有资源已在 renderer 释放回调中清理。 |
| `QList<VkPhysicalDeviceProperties> availablePhysicalDevices()` | 返回系统可用物理设备的属性列表。 | 可在窗口显示前调用；索引对应 `setPhysicalDeviceIndex()`。 |
| `QMatrix4x4 clipCorrectionMatrix()` | 返回把常见 OpenGL 投影约定修正为 Vulkan clip 空间的矩阵。 | 预乘 projection matrix；Vulkan 的 Y 方向和深度范围与 OpenGL 不同。 |
| `VkFormat colorFormat() const` | 返回当前 swapchain 使用的颜色格式。 | 只在 `initResources()` 到 `releaseResources()` 期间有效。 |
| `int concurrentFrameCount() const` | 返回可能同时处于活动状态的帧数量。 | 动态 uniform 等资源应按帧复制；值在窗口生命周期内固定。 |
| `[virtual] QVulkanWindowRenderer *createRenderer()` | 创建并返回窗口使用的 renderer。 | 默认返回空，不绘制应用内容；窗口取得返回对象所有权，通常只调用一次。 |
| `VkCommandBuffer currentCommandBuffer() const` | 返回当前 swapchain frame 的主 command buffer。 | 只能在 `startNextFrame()` 到 `frameReady()` 之间使用。 |
| `int currentFrame() const` | 返回当前帧槽位，范围为 `[0, concurrentFrameCount() - 1]`。 | 用它索引每帧 uniform 等动态资源；可用 `MAX_CONCURRENT_FRAME_COUNT` 静态分配数组。 |
| `VkFramebuffer currentFramebuffer() const` | 返回当前 swapchain image 对应的默认 framebuffer。 | 只在当前 frame 期间有效；MSAA 开启时附件数量不同。 |
| `int currentSwapChainImageIndex() const` | 返回当前 swapchain image 索引。 | 只在当前 frame 期间有效，范围为 `[0, swapChainImageCount() - 1]`。 |
| `VkRenderPass defaultRenderPass() const` | 返回 Qt 提供的典型单 subpass render pass。 | 不使用它时，应用必须自己处理 swapchain/depth image layout 转换。 |
| `VkFormat depthStencilFormat() const` | 返回 depth-stencil buffer 格式。 | 只在 `initResources()` 到 `releaseResources()` 期间有效。 |
| `VkImage depthStencilImage() const` | 返回窗口管理的 depth-stencil image。 | 只在 `initSwapChainResources()` 到 `releaseSwapChainResources()` 期间有效。 |
| `VkImageView depthStencilImageView() const` | 返回窗口管理的 depth-stencil image view。 | 只在 swapchain 资源生命周期内有效。 |
| `VkDevice device() const` | 返回当前 logical device。 | 只在 `initResources()` 到 `releaseResources()` 期间有效；device lost 后失效。 |
| `uint32_t deviceLocalMemoryIndex() const` | 返回一个通常适合 device-local 分配的 memory type index。 | 只是便利值，不保证适合所有 image；严谨分配仍应根据 memory requirements 自行选择。 |
| `Flags flags() const` | 返回请求的窗口资源标志。 | 读取的是配置值，不是当前资源是否已保留的诊断结果。 |
| `[signal] void frameGrabbed(const QImage &image)` | 异步截图读回完成时发出。 | 只有异步 `grab()` 需要依赖它；连接对象要保证生命周期。 |
| `void frameReady()` | 告知窗口当前 frame 的 command buffer 已准备好，可以提交和 present。 | 每次 `startNextFrame()` 必须恰好调用一次；只能在 GUI/main 线程调用。 |
| `QImage grab()` | 渲染下一帧并把颜色 buffer 阻塞读回为图像。 | 需要 `supportsGrab()`；不能在 frame 进行中调用，且可能非常慢。 |
| `VkCommandPool graphicsCommandPool() const` | 返回当前 graphics command pool。 | 只在 `initResources()` 到 `releaseResources()` 期间有效。 |
| `VkQueue graphicsQueue() const` | 返回当前 graphics queue。 | 只在资源初始化生命周期内有效；不要在 device 销毁后使用。 |
| `uint32_t graphicsQueueFamilyIndex() const` | 返回当前 graphics queue 所属 family 索引。 | 只在初始化资源期间有效；用于 queue family 相关配置。 |
| `uint32_t hostVisibleMemoryIndex() const` | 返回一个 host-visible 且 coherent 的便利 memory type index，可能同时 cached。 | 只是通用便利值；特殊资源应根据 requirements 自行选择。 |
| `bool isValid() const` | 判断窗口是否已成功初始化包括 swapchain 在内的 Vulkan 资源。 | 初始化发生在首次 expose 后；未显示或初始化失败时为假。 |
| `VkImage msaaColorImage(int idx) const` | 返回指定 swapchain 槽位的 multisample color image。 | 未启用 MSAA 时返回 `VK_NULL_HANDLE`；索引和生命周期都必须合法。 |
| `VkImageView msaaColorImageView(int idx) const` | 返回指定 swapchain 槽位的 multisample color image view。 | 未启用 MSAA 时返回 `VK_NULL_HANDLE`；只在 swapchain 资源生命周期内有效。 |
| `VkPhysicalDevice physicalDevice() const` | 返回当前选中的物理设备。 | 从 `preInitResources()` 开始到 `releaseResources()` 有效。 |
| `const VkPhysicalDeviceProperties *physicalDeviceProperties() const` | 返回当前物理设备属性指针。 | 指针由窗口内部管理；只在初始化阶段有效，不要跨资源重建保存。 |
| `VkSampleCountFlagBits sampleCountFlagBits() const` | 返回实际使用的 Vulkan sample count。 | 创建 pipeline 的 multisample state 时应使用该值。 |
| `void setDeviceExtensions(const QByteArrayList &extensions)` | 请求启用 device extensions。 | 应在窗口显示前设置；不支持的扩展会被忽略，swapchain 扩展自动添加。 |
| `[since 6.7] void setEnabledFeaturesModifier(const EnabledFeaturesModifier &modifier)` | 设置 Vulkan 1.0 feature 修改回调。 | 配置必须在 device 初始化前完成；回调中的设置必须确实被物理设备支持。 |
| `[since 6.7] void setEnabledFeaturesModifier(EnabledFeatures2Modifier modifier)` | 设置 Vulkan 1.1+ `VkPhysicalDeviceFeatures2` 修改回调。 | `pNext` 链对象必须保持有效到 device 创建完成。 |
| `void setFlags(Flags flags)` | 设置窗口资源策略。 | 典型地在窗口显示前调用；`PersistentResources` 会改变不可见时的释放行为。 |
| `void setPhysicalDeviceIndex(int idx)` | 请求使用 `availablePhysicalDevices()` 中指定索引的物理设备。 | 默认使用第一个；必须在显示前或最迟 `preInitResources()` 前调用，之后无效。 |
| `void setPreferredColorFormats(const QList<VkFormat> &formats)` | 按优先顺序请求 swapchain 颜色格式。 | 只是偏好，最终格式用 `colorFormat()` 查询；适合请求 sRGB。 |
| `void setQueueCreateInfoModifier(const QueueCreateInfoModifier &modifier)` | 修改创建 logical device 时的 queue create info。 | 用于追加 transfer 等 queue；Qt 自己仍会请求 graphics queue。 |
| `void setSampleCount(int sampleCount)` | 请求多重采样级别。 | 只接受设备支持的值；不支持时不自动降级，而是禁用 MSAA。 |
| `QVulkanInfoVector<QVulkanExtension> supportedDeviceExtensions()` | 查询当前物理设备支持的 device extensions。 | 适合初始化前检查；只表示支持，不表示已启用。 |
| `QList<int> supportedSampleCounts()` | 返回设备和窗口路径支持的 sample count 集合。 | 先查询再传给 `setSampleCount()`，不要依赖自动 fallback。 |
| `bool supportsGrab() const` | 判断 swapchain 是否支持 transfer source，从而能否使用 `grab()`。 | 只在 swapchain 资源生命周期内有效。 |
| `VkImage swapChainImage(int idx) const` | 返回指定索引的 swapchain image。 | 索引范围为 `[0, swapChainImageCount() - 1]`；只在 swapchain 资源生命周期内有效。 |
| `int swapChainImageCount() const` | 返回 swapchain image 数量。 | 作为 image、view、MSAA 数组索引范围的依据。 |
| `QSize swapChainImageSize() const` | 返回 Vulkan 报告的 swapchain image 尺寸。 | 渲染应使用它而非简单的 window size；高 DPI 下可能有差异。 |
| `VkImageView swapChainImageView(int idx) const` | 返回指定索引的 swapchain image view。 | 索引和生命周期必须合法。 |
| `const int MAX_CONCURRENT_FRAME_COUNT` | 提供不小于 `concurrentFrameCount()` 的静态最大帧数。 | 用于声明固定大小的每帧资源数组，实际访问仍按 `currentFrame()`。 |

## 一句话总结

`QVulkanWindow` 把 Vulkan 窗口生命周期整理成几个明确回调：初始化资源、重建 swapchain、录制当前帧，并用一次且仅一次的 `frameReady()` 推动提交。
