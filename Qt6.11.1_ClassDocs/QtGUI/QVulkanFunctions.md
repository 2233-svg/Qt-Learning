# QVulkanFunctions

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QVulkanFunctions` 是由 QVulkanInstance 提供的 Vulkan 实例级核心函数表，覆盖构建时 Vulkan 头文件允许的核心 1.0 到 1.3 API。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QVulkanFunctions` 是由 QVulkanInstance 提供的 Vulkan 实例级核心函数表，覆盖构建时 Vulkan 头文件允许的核心 1.0 到 1.3 API。

**内部模型：** Qt 运行时动态解析 Vulkan 函数，不直接链接全部入口。该对象不能自行构造；`QVulkanInstance::functions()` 返回实例级表，设备级命令必须从 `deviceFunctions(device)` 取得。扩展命令要通过 proc address 并先验证扩展已启用。

**适用场景：** 在 Qt 窗口/实例管理下直接调用 Vulkan 实例级核心命令时使用。

**典型调用链：** 配置 QVulkanInstance -> create/isValid -> functions -> 调用 vkEnumeratePhysicalDevices 等实例级命令 -> 检查 VkResult -> 销毁实例前停止使用函数表。

**先记住的坑：** 不能直接构造；不能混用实例级与设备级命令；构建机 Vulkan 头版本会影响可见原型；扩展函数不在核心表中自动提供。

## 2. 依赖与对象关系

- 头文件：`#include <QVulkanFunctions>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

Qt 运行时动态解析 Vulkan 函数，不直接链接全部入口。该对象不能自行构造；`QVulkanInstance::functions()` 返回实例级表，设备级命令必须从 `deviceFunctions(device)` 取得。扩展命令要通过 proc address 并先验证扩展已启用。

### 状态、生命周期和线程

**生命周期：** 函数表依赖对应的 Vulkan instance/device 和有效的函数地址。不能直接构造某些函数表对象，也不能在 instance/device 销毁后继续调用；先完成初始化和设备选择，再取得正确层级的函数表。

**状态与结果：** 要区分 Vulkan loader 不存在、instance 未创建、device 未创建、函数版本/扩展不可用和调用本身返回错误。函数是否可调用还受 Vulkan 头文件版本、运行时驱动和启用扩展影响。

**线程与事件循环：** Vulkan 的线程规则由 Vulkan 对象和命令提交方式决定，Qt 的函数表只负责解析和转发，不替你同步设备访问。窗口/渲染对象还要遵守 Qt Quick 或 QWindow 的线程边界。

## 3. 直接使用

在 Qt 窗口/实例管理下直接调用 Vulkan 实例级核心命令时使用。 使用时通常按这个过程组织：配置 QVulkanInstance -> create/isValid -> functions -> 调用 vkEnumeratePhysicalDevices 等实例级命令 -> 检查 VkResult -> 销毁实例前停止使用函数表。

```cpp
QVulkanFunctions *f = instance.functions();
uint32_t count = 0;
const VkResult result = f->vkEnumeratePhysicalDevices(
    instance.vkInstance(), &count, nullptr);
if (result != VK_SUCCESS) {
    // 处理 Vulkan 错误
}
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 配套与继承 API

- `QVulkanFunctions *QVulkanInstance::functions() const`
- `VkResult QVulkanFunctions::vkEnumeratePhysicalDevices(VkInstance instance, uint32_t *count, VkPhysicalDevice *devices)`
- `PFN_vkVoidFunction QVulkanInstance::getInstanceProcAddr(const char *name)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QVulkanFunctions *QVulkanInstance::functions() const`

**作用与语义：**

返回对应的`QVulkanFunctions`对象，该对象暴露核心 Vulkan 命令集，排除设备级功能，且保证跨平台功能。
注意：归还的物品由`QVulkanInstance`拥有和管理。请勿销毁或更改。
核心 Vulkan 1.0 API 中的函数将始终可用。对于更高版本的 Vulkan，如 1.1 和 1.2，`QVulkanFunctions` 对象也会尝试解析这些核心 API 函数，但如果运行时 Vulkan 实例实现不支持这些功能，调用任何不支持的函数会导致不确定的行为。此外，为了正确启用对 1.0 以上版本的支持，可能需要在 `create()` 前调用 `setApiVersion()` 来设置合适的实例 API 版本。要查询 Vulkan 实现的实例级版本，请调用 `supportedApiVersion()`。

### `VkResult QVulkanFunctions::vkEnumeratePhysicalDevices(VkInstance instance, uint32_t *count, VkPhysicalDevice *devices)`

**作用与语义：**

枚举 Vulkan 实例可见的物理设备。先把 `devices` 设为 `nullptr` 取得数量，再按 `count` 分配数组并再次调用；返回值是 `VkResult`，第二次调用仍应处理设备数变化导致的 `VK_INCOMPLETE`。

### `PFN_vkVoidFunction QVulkanInstance::getInstanceProcAddr(const char *name)`

**作用与语义：**

用给定的 `name` 解析 Vulkan 函数。
对于核心，Vulkan命令更倾向于使用可从`functions()`和`deviceFunctions()`检索的函数包装器。

## 6. 深入实践与常见坑

### 生命周期和资源边界

函数表依赖对应的 Vulkan instance/device 和有效的函数地址。不能直接构造某些函数表对象，也不能在 instance/device 销毁后继续调用；先完成初始化和设备选择，再取得正确层级的函数表。

### 状态和错误边界

要区分 Vulkan loader 不存在、instance 未创建、device 未创建、函数版本/扩展不可用和调用本身返回错误。函数是否可调用还受 Vulkan 头文件版本、运行时驱动和启用扩展影响。

### 线程边界

Vulkan 的线程规则由 Vulkan 对象和命令提交方式决定，Qt 的函数表只负责解析和转发，不替你同步设备访问。窗口/渲染对象还要遵守 Qt Quick 或 QWindow 的线程边界。

### 最容易出现的错误

不能直接构造；不能混用实例级与设备级命令；构建机 Vulkan 头版本会影响可见原型；扩展函数不在核心表中自动提供。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QVulkanFunctions` 所属机制类型：Vulkan 动态函数解析机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
