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

### 静态公有成员

- `const int MAX_CONCURRENT_FRAME_COUNT`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 57 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `[since 6.7] QVulkanWindow::EnabledFeatures2Modifier`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QVulkanWindow` 的配置属性。初始化或状态切换时通过 `setEnabledFeatures2Modifier(...)` 设置，之后用 `EnabledFeatures2Modifier()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:EnabledFeatures2Modifier`。
- 属性名：`QVulkanWindow`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVulkanWindow::EnabledFeaturesModifier`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QVulkanWindow` 的配置属性。初始化或状态切换时通过 `setEnabledFeaturesModifier(...)` 设置，之后用 `EnabledFeaturesModifier()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:EnabledFeaturesModifier`。
- 属性名：`QVulkanWindow`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QVulkanWindow::Flagflags QVulkanWindow::Flags`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QVulkanWindow` 暴露的类型声明 `Flagflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Flagflags QVulkanWindow::Flags`。
- 属性名：`QVulkanWindow`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVulkanWindow::QueueCreateInfoModifier`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QVulkanWindow` 的配置属性。初始化或状态切换时通过 `setQueueCreateInfoModifier(...)` 设置，之后用 `QueueCreateInfoModifier()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:QueueCreateInfoModifier`。
- 属性名：`QVulkanWindow`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QVulkanWindow::QVulkanWindow(QWindow *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QVulkanWindow` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `parent`：类型为 `QWindow *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QVulkanWindow::~QVulkanWindow()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QVulkanWindow` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<VkPhysicalDeviceProperties> QVulkanWindow::availablePhysicalDevices()`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanWindow::availablePhysicalDevices` 用于计算、查询或取得与“可用量、Physical、Devices”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<VkPhysicalDeviceProperties>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<VkPhysicalDeviceProperties>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMatrix4x4 QVulkanWindow::clipCorrectionMatrix()`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanWindow::clipCorrectionMatrix` 用于计算、查询或取得与“clip、Correction、Matrix”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMatrix4x4`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMatrix4x4`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `VkFormat QVulkanWindow::colorFormat() const`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanWindow::colorFormat` 用于计算、查询或取得与“color、格式化”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `VkFormat`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`VkFormat`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QVulkanWindow::concurrentFrameCount() const`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanWindow::concurrentFrameCount` 用于计算、查询或取得与“concurrent、Frame、数量统计”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] QVulkanWindowRenderer *QVulkanWindow::createRenderer()`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanWindow::createRenderer` 用于计算、查询或取得与“创建、Renderer”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QVulkanWindowRenderer *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVulkanWindowRenderer *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `VkCommandBuffer QVulkanWindow::currentCommandBuffer() const`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanWindow::currentCommandBuffer` 用于计算、查询或取得与“当前、Command、Buffer”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `VkCommandBuffer`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`VkCommandBuffer`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QVulkanWindow::currentFrame() const`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanWindow::currentFrame` 用于计算、查询或取得与“当前、Frame”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `VkFramebuffer QVulkanWindow::currentFramebuffer() const`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanWindow::currentFramebuffer` 用于计算、查询或取得与“当前、Framebuffer”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `VkFramebuffer`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`VkFramebuffer`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QVulkanWindow::currentSwapChainImageIndex() const`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanWindow::currentSwapChainImageIndex` 用于计算、查询或取得与“当前、Swap、Chain、Image、索引”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `VkRenderPass QVulkanWindow::defaultRenderPass() const`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanWindow::defaultRenderPass` 用于计算、查询或取得与“default、渲染、Pass”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `VkRenderPass`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`VkRenderPass`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `VkFormat QVulkanWindow::depthStencilFormat() const`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanWindow::depthStencilFormat` 用于计算、查询或取得与“depth、Stencil、格式化”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `VkFormat`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`VkFormat`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `VkImage QVulkanWindow::depthStencilImage() const`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanWindow::depthStencilImage` 用于计算、查询或取得与“depth、Stencil、Image”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `VkImage`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`VkImage`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `VkImageView QVulkanWindow::depthStencilImageView() const`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanWindow::depthStencilImageView` 用于计算、查询或取得与“depth、Stencil、Image、View”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `VkImageView`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`VkImageView`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `VkDevice QVulkanWindow::device() const`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanWindow::device` 用于计算、查询或取得与“device”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `VkDevice`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`VkDevice`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `uint32_t QVulkanWindow::deviceLocalMemoryIndex() const`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanWindow::deviceLocalMemoryIndex` 用于计算、查询或取得与“device、Local、Memory、索引”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `uint32_t`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`uint32_t`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVulkanWindow::Flags QVulkanWindow::flags() const`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanWindow::flags` 用于计算、查询或取得与“标志”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QVulkanWindow::Flags`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVulkanWindow::Flags`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QVulkanWindow::frameGrabbed(const QImage &image)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QVulkanWindow` 发出的通知信号 `frameGrabbed`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `image`：类型为 `const QImage &`。没有默认值，调用时必须提供。传入 `const QImage &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QVulkanWindow::frameReady()`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanWindow::frameReady` 用于执行与“frame、Ready”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QImage QVulkanWindow::grab()`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanWindow::grab` 用于计算、查询或取得与“抓取”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QImage`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QImage`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `VkCommandPool QVulkanWindow::graphicsCommandPool() const`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanWindow::graphicsCommandPool` 用于计算、查询或取得与“graphics、Command、Pool”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `VkCommandPool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`VkCommandPool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `VkQueue QVulkanWindow::graphicsQueue() const`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanWindow::graphicsQueue` 用于计算、查询或取得与“graphics、Queue”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `VkQueue`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`VkQueue`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `uint32_t QVulkanWindow::graphicsQueueFamilyIndex() const`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanWindow::graphicsQueueFamilyIndex` 用于计算、查询或取得与“graphics、Queue、Family、索引”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `uint32_t`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`uint32_t`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `uint32_t QVulkanWindow::hostVisibleMemoryIndex() const`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanWindow::hostVisibleMemoryIndex` 用于计算、查询或取得与“host、可见状态、Memory、索引”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `uint32_t`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`uint32_t`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QVulkanWindow::isValid() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isValid`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `VkImage QVulkanWindow::msaaColorImage(int idx) const`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanWindow::msaaColorImage` 用于计算、查询或取得与“msaa、Color、Image”相关的操作。调用时要先确认当前状态和 `idx` 的有效范围；返回类型是 `VkImage`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`VkImage`。
- 参数 `idx`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `VkImageView QVulkanWindow::msaaColorImageView(int idx) const`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanWindow::msaaColorImageView` 用于计算、查询或取得与“msaa、Color、Image、View”相关的操作。调用时要先确认当前状态和 `idx` 的有效范围；返回类型是 `VkImageView`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`VkImageView`。
- 参数 `idx`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `VkPhysicalDevice QVulkanWindow::physicalDevice() const`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanWindow::physicalDevice` 用于计算、查询或取得与“physical、Device”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `VkPhysicalDevice`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`VkPhysicalDevice`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const VkPhysicalDeviceProperties *QVulkanWindow::physicalDeviceProperties() const`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanWindow::physicalDeviceProperties` 用于计算、查询或取得与“physical、Device、Properties”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const VkPhysicalDeviceProperties *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const VkPhysicalDeviceProperties *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `VkSampleCountFlagBits QVulkanWindow::sampleCountFlagBits() const`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanWindow::sampleCountFlagBits` 用于计算、查询或取得与“sample、数量统计、Flag、Bits”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `VkSampleCountFlagBits`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`VkSampleCountFlagBits`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QVulkanWindow::setDeviceExtensions(const QByteArrayList &extensions)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setDeviceExtensions`。调用它会改变 `QVulkanWindow` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `extensions`：类型为 `const QByteArrayList &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.7] void QVulkanWindow::setEnabledFeaturesModifier(const QVulkanWindow::EnabledFeaturesModifier &modifier)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setEnabledFeaturesModifier`。调用它会改变 `QVulkanWindow` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `modifier`：类型为 `const QVulkanWindow::EnabledFeaturesModifier &`。没有默认值，调用时必须提供。传入 `const QVulkanWindow::EnabledFeaturesModifier &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.7] void QVulkanWindow::setEnabledFeaturesModifier(QVulkanWindow::EnabledFeatures2Modifier modifier)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setEnabledFeaturesModifier`。调用它会改变 `QVulkanWindow` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `modifier`：类型为 `QVulkanWindow::EnabledFeatures2Modifier`。没有默认值，调用时必须提供。传入 `QVulkanWindow::EnabledFeatures2Modifier` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QVulkanWindow::setFlags(QVulkanWindow::Flags flags)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFlags`。调用它会改变 `QVulkanWindow` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `flags`：类型为 `QVulkanWindow::Flags`。没有默认值，调用时必须提供。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QVulkanWindow::setPhysicalDeviceIndex(int idx)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPhysicalDeviceIndex`。调用它会改变 `QVulkanWindow` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `idx`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QVulkanWindow::setPreferredColorFormats(const QList<VkFormat> &formats)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPreferredColorFormats`。调用它会改变 `QVulkanWindow` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `formats`：类型为 `const QList<VkFormat> &`。没有默认值，调用时必须提供。传入 `const QList<VkFormat> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QVulkanWindow::setQueueCreateInfoModifier(const QVulkanWindow::QueueCreateInfoModifier &modifier)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setQueueCreateInfoModifier`。调用它会改变 `QVulkanWindow` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `modifier`：类型为 `const QVulkanWindow::QueueCreateInfoModifier &`。没有默认值，调用时必须提供。传入 `const QVulkanWindow::QueueCreateInfoModifier &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QVulkanWindow::setSampleCount(int sampleCount)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSampleCount`。调用它会改变 `QVulkanWindow` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `sampleCount`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVulkanInfoVector<QVulkanExtension> QVulkanWindow::supportedDeviceExtensions()`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanWindow::supportedDeviceExtensions` 用于计算、查询或取得与“supported、Device、Extensions”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QVulkanInfoVector<QVulkanExtension>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVulkanInfoVector<QVulkanExtension>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<int> QVulkanWindow::supportedSampleCounts()`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanWindow::supportedSampleCounts` 用于计算、查询或取得与“supported、Sample、Counts”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<int>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<int>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QVulkanWindow::supportsGrab() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `supportsGrab`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `VkImage QVulkanWindow::swapChainImage(int idx) const`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanWindow::swapChainImage` 用于计算、查询或取得与“swap、Chain、Image”相关的操作。调用时要先确认当前状态和 `idx` 的有效范围；返回类型是 `VkImage`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`VkImage`。
- 参数 `idx`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QVulkanWindow::swapChainImageCount() const`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanWindow::swapChainImageCount` 用于计算、查询或取得与“swap、Chain、Image、数量统计”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSize QVulkanWindow::swapChainImageSize() const`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanWindow::swapChainImageSize` 用于计算、查询或取得与“swap、Chain、Image、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSize`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSize`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `VkImageView QVulkanWindow::swapChainImageView(int idx) const`

**API 类别：** 成员函数说明

**中文解读：** `QVulkanWindow::swapChainImageView` 用于计算、查询或取得与“swap、Chain、Image、View”相关的操作。调用时要先确认当前状态和 `idx` 的有效范围；返回类型是 `VkImageView`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`VkImageView`。
- 参数 `idx`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const int QVulkanWindow::MAX_CONCURRENT_FRAME_COUNT`

**API 类别：** Member Variable Documentation

**中文解读：** 这是 `QVulkanWindow` 的配置属性。初始化或状态切换时通过 `setMAX_CONCURRENT_FRAME_COUNT(...)` 设置，之后用 `MAX_CONCURRENT_FRAME_COUNT()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:MAX_CONCURRENT_FRAME_COUNT`。
- 属性名：`QVulkanWindow`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.7) EnabledFeatures2Modifier`

**API 类别：** 公有类型

**中文解读：** 这是 `QVulkanWindow` 的 `启用状态、Features、2、Modifier` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `EnabledFeaturesModifier`

**API 类别：** 公有类型

**中文解读：** 这是 `QVulkanWindow` 的 `启用状态、Features、Modifier` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum Flag { PersistentResources }`

**API 类别：** 公有类型

**中文解读：** 这是 `QVulkanWindow` 暴露的类型声明 `Flag`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags Flags`

**API 类别：** 公有类型

**中文解读：** 这是 `QVulkanWindow` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QueueCreateInfoModifier`

**API 类别：** 公有类型

**中文解读：** 这是 `QVulkanWindow` 的 `Queue、创建、Info、Modifier` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const int MAX_CONCURRENT_FRAME_COUNT`

**API 类别：** 静态公有成员

**中文解读：** 这是静态工具 API `const`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

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
