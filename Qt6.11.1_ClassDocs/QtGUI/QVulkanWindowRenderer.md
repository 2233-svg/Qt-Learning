# QVulkanWindowRenderer

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QVulkanWindowRenderer` 是 Vulkan 动态函数解析机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QVulkanWindowRenderer` 是 Vulkan 动态函数解析机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** Qt 不默认静态链接所有 Vulkan 函数，而是通过 `QVulkanInstance` 在运行时解析函数地址。实例级函数由 `QVulkanFunctions` 提供，设备级函数由与具体 `VkDevice` 关联的 `QVulkanDeviceFunctions` 提供。

**适用场景：** 创建并初始化 `QVulkanInstance`，把它绑定到窗口或渲染环境，通过 `functions()` 取得 instance 级函数，通过 `deviceFunctions(device)` 取得 device 级函数，检查返回状态后再调用。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要直接构造 `QVulkanFunctions`/`QVulkanDeviceFunctions`；不要把 instance 级和 device 级函数混用；不要假设扩展函数自动存在；不要忽略平台和驱动能力。

## 2. 依赖与对象关系

- 头文件：`#include <QVulkanWindowRenderer>`
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

### 公有函数

- `virtual ~QVulkanWindowRenderer()`
- `virtual void initResources()`
- `virtual void initSwapChainResources()`
- `virtual void logicalDeviceLost()`
- `virtual void physicalDeviceLost()`
- `virtual void preInitResources()`
- `virtual void releaseResources()`
- `virtual void releaseSwapChainResources()`
- `virtual void startNextFrame() = 0`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[virtual noexcept] QVulkanWindowRenderer::~QVulkanWindowRenderer()`

**作用与语义：**

虚拟毁灭者。

### `[virtual] void QVulkanWindowRenderer::initResources()`

**作用与语义：**

当需要创建渲染器的图形资源时，调用了这个虚拟函数。
根据`QVulkanWindow::PersistentResources`标志、设备丢失情况等，该功能在`QVulkanWindow`生命周期内可能被多次调用。但后续调用总是在调用`releaseResources()`之前。
像 device()、graphicsQueue() 和 graphicsCommandPool() 这样的访问器只保证在该函数内及之后返回有效值，直到调用 `releaseResources()`。
默认实现是空的。

### `[virtual] void QVulkanWindowRenderer::initSwapChainResources()`

**作用与语义：**

当可以执行与交换链、帧缓冲或渲染通行相关的初始化时，调用该虚拟函数。交换链及相关资源会被重置，然后在窗口调整大小事件时重新创建，因此对`initResources()`和`releaseResources()`的调用可以包含多次调用initSwapChainResources()以及中间`releaseSwapChainResources()`调用。
像 `QVulkanWindow::swapChainImageSize()` 这样的访问器只保证在函数内及之后返回有效值，直到调用 `releaseSwapChainResources()`。
这也是大小相关的计算（例如投影矩阵）应进行的地方，因为该函数在每次调整大小时都会被有效调用。
默认实现是空的。

### `[virtual] void QVulkanWindowRenderer::logicalDeviceLost()`

**作用与语义：**

当逻辑设备（VkDevice）丢失时调用该虚拟函数，意味着某些操作因`VK_ERROR_DEVICE_LOST`失败。
默认实现是空的。
通常不需要在此功能中执行特殊操作。`QVulkanWindow` 会自动释放所有资源（根据需要调用 `releaseSwapChainResources()` 和 `releaseResources()`），并尝试重新初始化，获取新的设备。当物理设备也丢失时，这种重新初始化尝试可能导致`physicalDeviceLost()`。

### `[virtual] void QVulkanWindowRenderer::physicalDeviceLost()`

**作用与语义：**

当物理设备丢失时调用了这个虚拟函数，意味着逻辑设备的创建随`VK_ERROR_DEVICE_LOST`失败。
默认实现是空的。
通常不需要在这个函数中执行特殊操作`QVulkanWindow`因为在一定时间后会自动重新尝试初始化。

### `[virtual] void QVulkanWindowRenderer::preInitResources()`

**作用与语义：**

这个虚拟函数是在图形初始化（即调用`initResources()`）即将开始之前调用的。
通常不需要重新实现此功能。但在某些情况下，涉及基于物理设备和表面的决策。这些决策通常无法在`QVulkanWindow`可见之前完成，因为此时Vulkan表面不可检索。
相反，应用程序可以重新实现该功能。这里`QVulkanWindow::physicalDevice()`和`QVulkanInstance::surfaceForWindow()`都可用，但尚未进行新的逻辑设备初始化。
默认实现是空的。

### `[virtual] void QVulkanWindowRenderer::releaseResources()`

**作用与语义：**

当渲染器需要释放图形资源时，调用该虚拟函数。
实现时必须准备调用该函数后，后续可能会有 `initResources()`。
`QVulkanWindow`负责在调用该功能前后等待设备空闲。
默认实现是空的。

### `[virtual] void QVulkanWindowRenderer::releaseSwapChainResources()`

**作用与语义：**

当需要释放交换链、帧缓冲或渲染通行相关资源时，调用该虚拟函数。
实现时必须准备，调用该函数后，可能会在后续时刻重新调用`initSwapChainResources()`。
`QVulkanWindow`负责在调用该功能前后等待设备空闲。
默认实现是空的。
注意：这是`QVulkanWindow`开始释放所有图形资源前最后一个操作的地方。因此，拥有异步、可能多线程`startNextFrame()`实现前必须执行阻塞等待和调用`QVulkanWindow::frameReady()`，以防有待处理的帧提交。

### `[pure virtual] void QVulkanWindowRenderer::startNextFrame()`

**作用与语义：**

当下一帧的绘制调用被添加到命令缓冲区时，调用了这个虚拟函数。
每次调用该函数后都必须调用`QVulkanWindow::frameReady()`。未按此操作将导致渲染循环停顿。调用也可以在从该函数返回后再进行。这意味着可以启动异步工作，只更新命令缓冲区并通知`QVulkanWindow`工作完成。
当调用该函数时，所有 Vulkan 资源都已初始化并准备好。当前的帧缓冲区和主命令缓冲区可以通过 `QVulkanWindow::currentFramebuffer()` 和 `QVulkanWindow::currentCommandBuffer()` 检索。逻辑设备和活跃图形队列可通过 `QVulkanWindow::device()` 和 `QVulkanWindow::graphicsQueue()` 访问。实现可以从 `QVulkanWindow::graphicsCommandPool()` 返回的池中创建额外的命令缓冲区。为了方便，主机可见索引和设备本地内存类型索引通过 `QVulkanWindow::hostVisibleMemoryIndex()` 和 `QVulkanWindow::deviceLocalMemoryIndex()` 公开。所有这些访问器都可以安全地从任何线程调用。

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

`QVulkanWindowRenderer` 所属机制类型：Vulkan 动态函数解析机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
