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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 3 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `QVulkanFunctions *QVulkanInstance::functions() const`

**API 类别：** 配套与继承 API

**中文解读：** `functions` 属于 Vulkan 动态函数取得或调用过程。先保证 QVulkanInstance 有效、核心版本/扩展已启用，再区分实例级与设备级函数并检查 VkResult 或返回指针。

**签名拆解：**

- 返回值：`QVulkanFunctions *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `VkResult QVulkanFunctions::vkEnumeratePhysicalDevices(VkInstance instance, uint32_t *count, VkPhysicalDevice *devices)`

**API 类别：** 配套与继承 API

**中文解读：** `vkEnumeratePhysicalDevices` 属于 Vulkan 动态函数取得或调用过程。先保证 QVulkanInstance 有效、核心版本/扩展已启用，再区分实例级与设备级函数并检查 VkResult 或返回指针。

**签名拆解：**

- 返回值：`VkResult`。
- 参数 `instance`：类型为 `VkInstance`。没有默认值，调用时必须提供。传入 `VkInstance` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `uint32_t *`。没有默认值，调用时必须提供。传入 `uint32_t *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `devices`：类型为 `VkPhysicalDevice *`。没有默认值，调用时必须提供。传入 `VkPhysicalDevice *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `PFN_vkVoidFunction QVulkanInstance::getInstanceProcAddr(const char *name)`

**API 类别：** 配套与继承 API

**中文解读：** `getInstanceProcAddr` 属于 Vulkan 动态函数取得或调用过程。先保证 QVulkanInstance 有效、核心版本/扩展已启用，再区分实例级与设备级函数并检查 VkResult 或返回指针。

**签名拆解：**

- 返回值：`PFN_vkVoidFunction`。
- 参数 `name`：类型为 `const char *`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

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
