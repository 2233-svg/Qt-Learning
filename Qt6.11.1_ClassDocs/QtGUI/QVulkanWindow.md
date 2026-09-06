# QVulkanWindow

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QVulkanWindow` 是 Vulkan 动态函数解析机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QVulkanWindow` 是 Vulkan 动态函数解析机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** Qt 不默认静态链接所有 Vulkan 函数，而是通过 `QVulkanInstance` 在运行时解析函数地址。实例级函数由 `QVulkanFunctions` 提供，设备级函数由与具体 `VkDevice` 关联的 `QVulkanDeviceFunctions` 提供。

**适用场景：** 创建并初始化 `QVulkanInstance`，把它绑定到窗口或渲染环境，通过 `functions()` 取得 instance 级函数，通过 `deviceFunctions(device)` 取得 device 级函数，检查返回状态后再调用。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要直接构造 `QVulkanFunctions`/`QVulkanDeviceFunctions`；不要把 instance 级和 device 级函数混用；不要假设扩展函数自动存在；不要忽略平台和驱动能力。

## 2. 依赖与对象关系

- 头文件：`#include <QVulkanWindow>`
- 继承自：QWindow
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

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

- `(since 6.7) EnabledFeatures2Modifier`
- `EnabledFeaturesModifier`
- `enum Flag { PersistentResources }`
- `flags Flags`
- `QueueCreateInfoModifier`

### 公有函数

- `QVulkanWindow(QWindow *parent = nullptr)`
- `virtual ~QVulkanWindow()`
- `QList<VkPhysicalDeviceProperties> availablePhysicalDevices()`
- `QMatrix4x4 clipCorrectionMatrix()`
- `VkFormat colorFormat() const`
- `int concurrentFrameCount() const`
- `virtual QVulkanWindowRenderer * createRenderer()`
- `VkCommandBuffer currentCommandBuffer() const`
- `int currentFrame() const`
- `VkFramebuffer currentFramebuffer() const`
- `int currentSwapChainImageIndex() const`
- `VkRenderPass defaultRenderPass() const`
- `VkFormat depthStencilFormat() const`
- `VkImage depthStencilImage() const`
- `VkImageView depthStencilImageView() const`
- `VkDevice device() const`
- `uint32_t deviceLocalMemoryIndex() const`
- `QVulkanWindow::Flags flags() const`
- `void frameReady()`
- `QImage grab()`
- `VkCommandPool graphicsCommandPool() const`
- `VkQueue graphicsQueue() const`
- `uint32_t graphicsQueueFamilyIndex() const`
- `uint32_t hostVisibleMemoryIndex() const`
- `bool isValid() const`
- `VkImage msaaColorImage(int idx) const`
- `VkImageView msaaColorImageView(int idx) const`
- `VkPhysicalDevice physicalDevice() const`
- `const VkPhysicalDeviceProperties * physicalDeviceProperties() const`
- `VkSampleCountFlagBits sampleCountFlagBits() const`
- `void setDeviceExtensions(const QByteArrayList &extensions)`
- `(since 6.7) void setEnabledFeaturesModifier(const QVulkanWindow::EnabledFeaturesModifier &modifier)`
- `(since 6.7) void setEnabledFeaturesModifier(QVulkanWindow::EnabledFeatures2Modifier modifier)`
- `void setFlags(QVulkanWindow::Flags flags)`
- `void setPhysicalDeviceIndex(int idx)`
- `void setPreferredColorFormats(const QList<VkFormat> &formats)`
- `void setQueueCreateInfoModifier(const QVulkanWindow::QueueCreateInfoModifier &modifier)`
- `void setSampleCount(int sampleCount)`
- `QVulkanInfoVector<QVulkanExtension> supportedDeviceExtensions()`
- `QList<int> supportedSampleCounts()`
- `bool supportsGrab() const`
- `VkImage swapChainImage(int idx) const`
- `int swapChainImageCount() const`
- `QSize swapChainImageSize() const`
- `VkImageView swapChainImageView(int idx) const`

### 信号

- `void frameGrabbed(const QImage &image)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[since 6.7] QVulkanWindow::EnabledFeatures2Modifier`

**作用与语义：**

在图形初始化过程中调用的函数，用来更改被更改为 VkDeviceCreateInfo 的 VkPhysicalDeviceFeatures2。
默认情况下，`QVulkanWindow` 启用物理设备报告支持的所有 Vulkan 1.0 核心功能，但有某些例外。实际情况下，`robustBufferAccess` 总是被禁用，以避免意外的性能损失。
然而，在处理 Vulkan 1.1、1.2 或 1.3 功能和扩展时，这并不总是足够。因此才有了这种回调机制。如果运行时只有 Vulkan 1.0 相关，则改用 `setEnabledFeaturesModifier()`。
VkPhysicalDeviceFeatures2 引用传递给回调函数时，`sType` 设置，其余部分归零。函数可以根据需要将成员改为 true，或设置 `pNext` 链。
注意：在设置`pNext`链时，确保被引用的对象寿命足够长，例如将它们作为成员变量存储在`QVulkanWindow`子类中。
这种typedef是在Qt 6.7中引入的。

### `QVulkanWindow::EnabledFeaturesModifier`

**作用与语义：**

在图形初始化过程中调用的函数，用于修改创建 Vulkan 设备对象时传递的 VkPhysicalDeviceFeatures。
默认情况下，`QVulkanWindow`启用物理设备报告支持的所有Vulkan 1.0核心功能，但有某些例外。实际情况下，`robustBufferAccess`总是被禁用，以避免意外的性能损失。
传入的 VkPhysicalDeviceFeatures 引用在调用该函数时全部归零。函数可以根据需要更改成员。
注意：要控制Vulkan 1.1、1.2或1.3功能，请使用`EnabledFeatures2Modifier`。

### `enum QVulkanWindow::Flagflags QVulkanWindow::Flags`

**作用与语义：**

该枚举描述了可以传递给`setFlags()`的标志。
- `QVulkanWindow::PersistentResources`：`0x01`;确保当窗口不再暴露时，不会释放图形资源。默认行为是释放所有资源，等恢复可见时再初始化。
Flags 类型是 QFlags 的 typedef<Flag>。它存储 Flag 值的 OR 组合。

### `QVulkanWindow::QueueCreateInfoModifier`

**作用与语义：**

在图形初始化过程中调用的函数，用于添加需要创建的额外队列。
如果渲染器除了默认图形队列外还需要其他队列（例如传输队列），则设置。提供的队列族属性可用于选择额外队列的索引。渲染器随后可以在 initResources() 中请求实际队列。
注意：当请求额外的图形队列时，Qt 本身总是请求一个图形队列。你需要在 queueCreateInfo 中搜索相应的条目，并操作它以获得额外的队列。

### `[explicit] QVulkanWindow::QVulkanWindow(QWindow *parent = nullptr)`

**作用与语义：**

用给定的`parent`构造一个新的QVulkanWindow。
表面类型设置为`QSurface::VulkanSurface`。

### `[virtual noexcept] QVulkanWindow::~QVulkanWindow()`

**作用与语义：**

毁灭者。

### `QList<VkPhysicalDeviceProperties> QVulkanWindow::availablePhysicalDevices()`

**作用与语义：**

返回系统中支持的物理设备的属性列表。
注意：该函数可以在窗口可见之前调用。

### `QMatrix4x4 QVulkanWindow::clipCorrectionMatrix()`

**作用与语义：**

返回一个可用于纠正OpenGL与Vulkan坐标系统差异的`QMatrix4x4`。
通过预先将投影矩阵与该矩阵相乘，应用程序可以继续假设Y指向向上，并在视口中分别将minDepth和maxDepth设置为0和maxDepth，而无需对顶点Z位置做进一步修正。OpenGL应用中的几何体可以直接使用，假设光栅化状态与OpenGL剔除和前面设置相匹配。

### `VkFormat QVulkanWindow::colorFormat() const`

**作用与语义：**

返回交换链使用的颜色缓冲格式。
注意：从调用 `QVulkanWindowRenderer::initResources()` 到 `QVulkanWindowRenderer::releaseResources()` 期间，调用此函数才有效。

### `int QVulkanWindow::concurrentFrameCount() const`

**作用与语义：**

返回可能同时激活的帧数。
注意：`QVulkanWindow`的整个生命周期内，数值保持不变。

**官方示例：**

```cpp
     class Renderer {
         void startNextFrame();
         // ...

         VkDescriptorBufferInfo m_uniformBufInfo[QVulkanWindow::MAX_CONCURRENT_FRAME_COUNT];
         QVulkanWindow *m_window = nullptr;
     };

     void Renderer::startNextFrame()
     {
         const int count = m_window->concurrentFrameCount();
         // for (int i = 0; i < count; ++i)
             // m_uniformBufInfo[i] = ...
         // ...
     }
```

### `[virtual] QVulkanWindowRenderer *QVulkanWindow::createRenderer()`

**作用与语义：**

返回一个新的`QVulkanWindowRenderer`实例。
该虚拟函数在窗口生命周期内调用一次，即首次使其可见之后的某个时间点。
默认实现返回的是空，因此除了清除缓冲区外不会进行任何渲染。
窗口会获得返回的渲染器对象的所有权。

### `VkCommandBuffer QVulkanWindow::currentCommandBuffer() const`

**作用与语义：**

返回当前交换链帧的活动命令缓冲区。`QVulkanWindowRenderer::startNextFrame()`的实现预期会向该命令缓冲区添加命令。
注意：该函数只能在 startNextFrame() 内部调用，且在异步命令生成时，必须调用至 `frameReady()`。

### `int QVulkanWindow::currentFrame() const`

**作用与语义：**

返回当前帧索引，范围为[0， `concurrentFrameCount()` - 1]。
渲染器实现必须确保数据和其他动态资源在多个副本中均有统一，以防止帧N改变仍在活动帧N - 1， N - 2，N - `concurrentFrameCount()` 1。
为了避免依赖动态数组大小，应用程序在声明数组时可以使用`MAX_CONCURRENT_FRAME_COUNT`。这保证总是等于或大于`concurrentFrameCount()`返回的值。这些数组可以根据该函数返回的值进行索引。
注意：该函数只能在 startNextFrame() 内部调用，且在异步命令生成时，必须调用至 `frameReady()`。

**官方示例：**

```cpp
     class Renderer {
         void startNextFrame();
         // ...

         VkDescriptorBufferInfo m_uniformBufInfo[QVulkanWindow::MAX_CONCURRENT_FRAME_COUNT];
         QVulkanWindow *m_window = nullptr;
     };

     void Renderer::startNextFrame()
     {
         VkDescriptorBufferInfo &uniformBufInfo(m_uniformBufInfo[m_window->currentFrame()]);
         // ...
     }
```

### `VkFramebuffer QVulkanWindow::currentFramebuffer() const`

**作用与语义：**

使用默认渲染通道返回当前交换链图像的VkFramebuffer。
当不使用多重采样时，帧缓冲区有两个附件（颜色、深度模板），当`sampleCountFlagBits()`大于`VK_SAMPLE_COUNT_1_BIT`时，有三个附件（颜色解析、深度模板、多采样颜色）。渲染器必须考虑这一点，例如在提供清晰值时。
注意：如果应用程序提供自己的渲染通道而非返回的渲染通道，则无需使用该帧缓冲区`defaultRenderPass()`。
注意：该函数只能在 startNextFrame() 内部调用，且在异步命令生成时，必须调用至 `frameReady()`。

### `int QVulkanWindow::currentSwapChainImageIndex() const`

**作用与语义：**

返回当前交换链图像索引，范围为[0， `swapChainImageCount()` - 1]。
注意：该函数只能在 startNextFrame() 内调用，且在异步命令生成时，必须调用至 `frameReady()`。

### `VkRenderPass QVulkanWindow::defaultRenderPass() const`

**作用与语义：**

返回一个典型的渲染通道，包含一个子通道。
注意：应用程序不必使用该渲染通行。但随后，他们需确保当前的交换链和深度模板图像能够从`VK_IMAGE_LAYOUT_UNDEFINED`过渡到`VK_IMAGE_LAYOUT_PRESENT_SRC_KHR`，并通过应用程序的自定义渲染通行或通过其他方式`VK_IMAGE_LAYOUT_DEPTH_STENCIL_ATTACHMENT_OPTIMAL`。
注意：本次渲染过程中未启用模板读写功能。
注意：调用该函数仅从调用`QVulkanWindowRenderer::initResources()`到`QVulkanWindowRenderer::releaseResources()`有效。

### `VkFormat QVulkanWindow::depthStencilFormat() const`

**作用与语义：**

返回深度模板缓冲区所使用的格式。
注意：调用该函数仅从调用`QVulkanWindowRenderer::initResources()`起有效，直到`QVulkanWindowRenderer::releaseResources()`。

### `VkImage QVulkanWindow::depthStencilImage() const`

**作用与语义：**

返回深度模板图像。
注意：调用该函数仅从调用`QVulkanWindowRenderer::initSwapChainResources()`到`QVulkanWindowRenderer::releaseSwapChainResources()`有效。

### `VkImageView QVulkanWindow::depthStencilImageView() const`

**作用与语义：**

返回深度模板图像视图。
注意：调用该函数仅从调用 `QVulkanWindowRenderer::initSwapChainResources()` 起有效至 `QVulkanWindowRenderer::releaseSwapChainResources()`。

### `VkDevice QVulkanWindow::device() const`

**作用与语义：**

返回激活逻辑设备。
注意：调用该函数仅从调用`QVulkanWindowRenderer::initResources()`到`QVulkanWindowRenderer::releaseResources()`有效。

### `uint32_t QVulkanWindow::deviceLocalMemoryIndex() const`

**作用与语义：**

返回适合通用使用的设备本地内存类型索引。
注意：调用该函数仅从调用`QVulkanWindowRenderer::initResources()`到`QVulkanWindowRenderer::releaseResources()`有效。
注意：不保证这种内存类型总是适用。正确的跨实现解决方案——尤其是设备本地镜像——是在检查`vkGetImageMemoryRequirements`返回的掩码后手动选择内存类型。

### `QVulkanWindow::Flags QVulkanWindow::flags() const`

**作用与语义：**

归还要求的标志。

### `[signal] void QVulkanWindow::frameGrabbed(const QImage &image)`

**作用与语义：**

当`image`准备好时，该信号会发出。

### `void QVulkanWindow::frameReady()`

**作用与语义：**

该函数必须在每次调用`QVulkanWindowRenderer::startNextFrame()`实现时被调用一次。在调用时，通过`currentCommandBuffer()`暴露的主命令缓冲区必须添加所有必要的渲染命令，因为该函数会触发提交命令并排队当前命令。
注意：该函数只能从GUI/主线程调用，`QVulkanWindowRenderer`的函数就是在那里调用的，`QVulkanWindow`实例也存在于此。

### `QImage QVulkanWindow::grab()`

**作用与语义：**

构建并渲染下一帧但不展示，然后对图像内容进行分块读回。
如果渲染器的`startNextFrame()`实现直接回调`frameReady()`，则返回图像。否则，返回的是未完成的图像，大小正确但内容尚未确定。在后一种情况下，内容将通过`frameGrabbed()`信号传递。
返回的`QImage`总是格式为`QImage::Format_RGBA8888`。如果`colorFormat()`是`VK_FORMAT_B8G8R8A8_UNORM`，红色和蓝色通道会自动交换，因为这种格式通常作为交换链色彩缓冲器的默认选择。对于其他颜色缓冲器格式，这个函数不会进行转换。
注意：当帧正在进行中（即应用程序尚未调用`frameReady()`）时不应调用此函数。
注意：由于额外的阻断读回，此功能可能成本较高。
注意：此功能目前需要交换链支持作为传输源（`VK_IMAGE_USAGE_TRANSFER_SRC_BIT`），否则将失败。

### `VkCommandPool QVulkanWindow::graphicsCommandPool() const`

**作用与语义：**

返回活跃的图形命令池。
注意：调用该函数仅从调用`QVulkanWindowRenderer::initResources()`到`QVulkanWindowRenderer::releaseResources()`有效。

### `VkQueue QVulkanWindow::graphicsQueue() const`

**作用与语义：**

返回当前的图形队列。
注意：调用该函数仅从调用`QVulkanWindowRenderer::initResources()`到`QVulkanWindowRenderer::releaseResources()`有效。

### `uint32_t QVulkanWindow::graphicsQueueFamilyIndex() const`

**作用与语义：**

返回活跃图形队列的家族索引。
注意：调用该函数仅从调用`QVulkanWindowRenderer::initResources()`到`QVulkanWindowRenderer::releaseResources()`为止有效。QVulkanWindowRenderer：：updateQueueCreateInfo() 的实现也可以调用该函数。

### `uint32_t QVulkanWindow::hostVisibleMemoryIndex() const`

**作用与语义：**

返回适合通用使用的主机可见内存类型索引。
返回的内存类型既可视又连贯。此外，如果可能，它还会被缓存。
注意：调用此函数仅从调用`QVulkanWindowRenderer::initResources()`到`QVulkanWindowRenderer::releaseResources()`有效。

### `bool QVulkanWindow::isValid() const`

**作用与语义：**

如果该窗口成功初始化了所有 Vulkan 资源，包括交换链，则返回 true。
注意：窗口可见后，初始化发生在第一次曝光事件时。

### `VkImage QVulkanWindow::msaaColorImage(int idx) const`

**作用与语义：**

返回指定的多重采样彩色图像，若未使用多采样则返回`VK_NULL_HANDLE`。
`idx`必须处于[0， `swapChainImageCount()` - 1]范围内。
注意：调用该函数仅从调用`QVulkanWindowRenderer::initSwapChainResources()`到`QVulkanWindowRenderer::releaseSwapChainResources()`有效。

### `VkImageView QVulkanWindow::msaaColorImageView(int idx) const`

**作用与语义：**

返回指定的多重采样彩色图像视图，若未使用多重采样则返回`VK_NULL_HANDLE`。
`idx`必须处于[0， `swapChainImageCount()` - 1]范围内。
注意：调用该函数仅从调用`QVulkanWindowRenderer::initSwapChainResources()`起有效直到`QVulkanWindowRenderer::releaseSwapChainResources()`。

### `VkPhysicalDevice QVulkanWindow::physicalDevice() const`

**作用与语义：**

退回了激活的物理设备。
注意：调用该函数仅从调用`QVulkanWindowRenderer::preInitResources()`起有效至`QVulkanWindowRenderer::releaseResources()`。

### `const VkPhysicalDeviceProperties *QVulkanWindow::physicalDeviceProperties() const`

**作用与语义：**

返回一个指向活动物理设备的属性的指针。
注意：调用该函数仅从调用`QVulkanWindowRenderer::preInitResources()`到`QVulkanWindowRenderer::releaseResources()`有效。

### `VkSampleCountFlagBits QVulkanWindow::sampleCountFlagBits() const`

**作用与语义：**

返回当前的采样计数为`VkSampleCountFlagBits`值。
当针对默认渲染目标时，`VkPipelineMultisampleStateCreateInfo`的`rasterizationSamples`字段必须设置为该值。

### `void QVulkanWindow::setDeviceExtensions(const QByteArrayList &extensions)`

**作用与语义：**

设置启用设备`extensions`列表。
不支持的扩展则被忽略。
掉电链扩展总是会自动添加，无需包含在列表中。
注意：该函数必须在窗口显示前或最迟在`QVulkanWindowRenderer::preInitResources()`时调用，若之后调用则无效。

### `[since 6.7] void QVulkanWindow::setEnabledFeaturesModifier(const QVulkanWindow::EnabledFeaturesModifier &modifier)`

**作用与语义：**

设置启用的设备功能修改功能`modifier`。
注意：要控制Vulkan 1.1、1.2或1.3功能，请使用重载`EnabledFeatures2Modifier`。
注意：`modifier` 传递给回调函数，所有成员都设为 false。函数可以根据需要更改成员。

### `[since 6.7] void QVulkanWindow::setEnabledFeaturesModifier(QVulkanWindow::EnabledFeatures2Modifier modifier)`

**作用与语义：**

设置启用的设备功能修改功能`modifier`。

### `void QVulkanWindow::setFlags(QVulkanWindow::Flags flags)`

**作用与语义：**

根据提供的`flags`配置行为。
注意：该函数必须在窗口显示前或最迟在`QVulkanWindowRenderer::preInitResources()`时调用，若之后调用则无效。

### `void QVulkanWindow::setPhysicalDeviceIndex(int idx)`

**作用与语义：**

请求使用带有索引`idx`的物理设备。索引对应于从`availablePhysicalDevices()`返回的列表。
默认情况下，使用第一个物理设备。
注意：该函数必须在窗口显示前或最迟在`QVulkanWindowRenderer::preInitResources()`时调用，若之后调用则无效。

### `void QVulkanWindow::setPreferredColorFormats(const QList<VkFormat> &formats)`

**作用与语义：**

设定掉期链的首选`formats`。
默认情况下，不会设置应用首选格式。在这种情况下，会使用表面的首选格式，或者如果没有该格式，则`VK_FORMAT_B8G8R8A8_UNORM`。
`formats`中的列表是有序的。如果不支持第一种格式，将考虑第二种格式，依此类推。当列表中不支持任何格式时，行为与默认情况下相同。
初始化后要查询实际格式，请调用`colorFormat()`。
注意：该函数必须在窗口显现前或最迟在`QVulkanWindowRenderer::preInitResources()`时调用，若之后调用则无效。
注意：重新实现`QVulkanWindowRenderer::preInitResources()`允许动态检查支持格式列表，如有需要。该曲面可通过 QVulkanInstace：：surfaceForWindow() 检索，同时该函数仍可安全调用以影响初始化的后期阶段。

### `void QVulkanWindow::setQueueCreateInfoModifier(const QVulkanWindow::QueueCreateInfoModifier &modifier)`

**作用与语义：**

设置队列创建信息修改函数`modifier`。

### `void QVulkanWindow::setSampleCount(int sampleCount)`

**作用与语义：**

请求对给定`sampleCount`进行多重采样抗锯齿。有效值为1、2、4、8......直到物理设备支持的最大值为止。
当采样计数大于1时，`QVulkanWindow`会创建一个多采样色彩缓冲区，而不是简单地针对交换链的图像。多采样缓冲区中的渲染会在每帧结束时被解析到非多采样缓冲区。
如需查看支持的样本计数列表，请致电`supportedSampleCounts()`。
在设置渲染流水线时，调用 `sampleCountFlagBits()` 查询激活采样计数作为`VkSampleCountFlagBits`值。
注意：该函数必须在窗口显现前或最迟在`QVulkanWindowRenderer::preInitResources()`时调用，若之后调用则无效。

### `QVulkanInfoVector<QVulkanExtension> QVulkanWindow::supportedDeviceExtensions()`

**作用与语义：**

返回由`setPhysicalDeviceIndex()`选择的物理设备创建的逻辑设备支持的扩展列表。
注意：该函数可以在窗口可见之前调用。

### `QList<int> QVulkanWindow::supportedSampleCounts()`

**作用与语义：**

使用`setPhysicalDeviceIndex()`选择的物理设备时，返回支持的样本计数集合，作为排序列表。
默认情况下`QVulkanWindow`使用采样计数为1。通过调用与该函数返回的集合不同的值（2、4、8、......）的 `setSampleCount()`，可以请求多采样抗锯齿。
注意：该函数可以在窗口可见之前调用。

### `bool QVulkanWindow::supportsGrab() const`

**作用与语义：**

如果交换链支持作为传输源使用，则返回为真，意味着`grab()`是可运行的。
注意：调用此函数仅从调用`QVulkanWindowRenderer::initSwapChainResources()`起有效至`QVulkanWindowRenderer::releaseSwapChainResources()`。

### `VkImage QVulkanWindow::swapChainImage(int idx) const`

**作用与语义：**

返回指定的交换链映像。
`idx`必须处于[0， `swapChainImageCount()` - 1]范围内。
注意：调用该函数仅从调用`QVulkanWindowRenderer::initSwapChainResources()`起有效至`QVulkanWindowRenderer::releaseSwapChainResources()`。

### `int QVulkanWindow::swapChainImageCount() const`

**作用与语义：**

返回交换链中的图片数量。
注意：在提供自定义渲染通道和帧缓冲区时，访问此文件是必要的。帧缓冲区针对当前交换链图像，因此应用程序必须提供多个帧缓冲区。
注意：调用该函数仅从调用`QVulkanWindowRenderer::initSwapChainResources()`到`QVulkanWindowRenderer::releaseSwapChainResources()`有效。

### `QSize QVulkanWindow::swapChainImageSize() const`

**作用与语义：**

返回交换链的图像大小。
这通常与窗口大小相符，但如果`vkGetPhysicalDeviceSurfaceCapabilitiesKHR`报告的是固定大小，也可能有所不同。
此外，在某些平台上观察到，在高DPI缩放激活时，Vulkan报告的表面尺寸会不同，这意味着`QWindow`报告的`size()`与`devicePixelRatio()`相较于此处返回的值少或多1像素，推测是由于四舍五入的差异。渲染代码应当意识到这一点，任何相关的渲染逻辑都必须基于此处返回的值，而绝不能基于`QWindow`报告的尺寸。无论理论上哪个像素大小正确，Vulkan渲染都必须仅依赖于Vulkan API报告的表面尺寸。否则，例如在设置视口时，可能会出现验证错误，因为应用程序提供的值可能从Vulkan的视角中变得超出界限。
注意：调用该函数仅从调用`QVulkanWindowRenderer::initSwapChainResources()`起有效至`QVulkanWindowRenderer::releaseSwapChainResources()`。

### `VkImageView QVulkanWindow::swapChainImageView(int idx) const`

**作用与语义：**

返回指定的交换链状图像视图。
`idx`必须处于[0， `swapChainImageCount()` - 1]范围内。
注意：调用该函数仅从调用`QVulkanWindowRenderer::initSwapChainResources()`到`QVulkanWindowRenderer::releaseSwapChainResources()`有效。

### `const int QVulkanWindow::MAX_CONCURRENT_FRAME_COUNT`

**作用与语义：**

该变量保持一个恒定值，且总是等于或大于最大值`concurrentFrameCount()`。

### `(since 6.7) EnabledFeatures2Modifier`

**作用与语义：**

在图形初始化过程中调用的函数，用来更改被更改为 VkDeviceCreateInfo 的 VkPhysicalDeviceFeatures2。
默认情况下，`QVulkanWindow` 启用物理设备报告支持的所有 Vulkan 1.0 核心功能，但有某些例外。实际情况下，`robustBufferAccess` 总是被禁用，以避免意外的性能损失。
然而，在处理 Vulkan 1.1、1.2 或 1.3 功能和扩展时，这并不总是足够。因此才有了这种回调机制。如果运行时只有 Vulkan 1.0 相关，则改用 `setEnabledFeaturesModifier()`。
VkPhysicalDeviceFeatures2 引用传递给回调函数时，`sType` 设置，其余部分归零。函数可以根据需要将成员改为 true，或设置 `pNext` 链。
注意：在设置`pNext`链时，确保被引用的对象寿命足够长，例如将它们作为成员变量存储在`QVulkanWindow`子类中。
这种typedef是在Qt 6.7中引入的。

### `EnabledFeaturesModifier`

**作用与语义：**

在图形初始化过程中调用的函数，用于修改创建 Vulkan 设备对象时传递的 VkPhysicalDeviceFeatures。
默认情况下，`QVulkanWindow`启用物理设备报告支持的所有Vulkan 1.0核心功能，但有某些例外。实际情况下，`robustBufferAccess`总是被禁用，以避免意外的性能损失。
传入的 VkPhysicalDeviceFeatures 引用在调用该函数时全部归零。函数可以根据需要更改成员。
注意：要控制Vulkan 1.1、1.2或1.3功能，请使用`EnabledFeatures2Modifier`。

### `enum Flag { PersistentResources }`

**作用与语义：**

该枚举描述了可以传递给`setFlags()`的标志。
- `QVulkanWindow::PersistentResources`：`0x01`;确保当窗口不再暴露时，不会释放图形资源。默认行为是释放所有资源，等恢复可见时再初始化。
Flags 类型是 QFlags 的 typedef<Flag>。它存储 Flag 值的 OR 组合。

### `flags Flags`

**作用与语义：**

该枚举描述了可以传递给`setFlags()`的标志。
- `QVulkanWindow::PersistentResources`：`0x01`;确保当窗口不再暴露时，不会释放图形资源。默认行为是释放所有资源，等恢复可见时再初始化。
Flags 类型是 QFlags 的 typedef<Flag>。它存储 Flag 值的 OR 组合。

### `QueueCreateInfoModifier`

**作用与语义：**

在图形初始化过程中调用的函数，用于添加需要创建的额外队列。
如果渲染器除了默认图形队列外还需要其他队列（例如传输队列），则设置。提供的队列族属性可用于选择额外队列的索引。渲染器随后可以在 initResources() 中请求实际队列。
注意：当请求额外的图形队列时，Qt 本身总是请求一个图形队列。你需要在 queueCreateInfo 中搜索相应的条目，并操作它以获得额外的队列。

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

`QVulkanWindow` 所属机制类型：Vulkan 动态函数解析机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
