# QVulkanDeviceFunctions

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QVulkanDeviceFunctions` 是 Vulkan 动态函数解析机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QVulkanDeviceFunctions` 是 Vulkan 动态函数解析机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** Qt 不默认静态链接所有 Vulkan 函数，而是通过 `QVulkanInstance` 在运行时解析函数地址。实例级函数由 `QVulkanFunctions` 提供，设备级函数由与具体 `VkDevice` 关联的 `QVulkanDeviceFunctions` 提供。

**适用场景：** 创建并初始化 `QVulkanInstance`，把它绑定到窗口或渲染环境，通过 `functions()` 取得 instance 级函数，通过 `deviceFunctions(device)` 取得 device 级函数，检查返回状态后再调用。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要直接构造 `QVulkanFunctions`/`QVulkanDeviceFunctions`；不要把 instance 级和 device 级函数混用；不要假设扩展函数自动存在；不要忽略平台和驱动能力。

## 2. 依赖与对象关系

- 头文件：`#include <QVulkanDeviceFunctions>`
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

### 配套与继承 API

- `QVulkanDeviceFunctions *QVulkanInstance::deviceFunctions(VkDevice device)`
- `void QVulkanInstance::resetDeviceFunctions(VkDevice device)`
- `PFN_vkVoidFunction QVulkanDeviceFunctions::vkGetDeviceProcAddr(VkDevice device, const char *name)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 3 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `QVulkanDeviceFunctions *QVulkanInstance::deviceFunctions(VkDevice device)`

**API 类别：** 配套与继承 API

**中文解读：** `deviceFunctions` 属于 Vulkan 动态函数取得或调用过程。先保证 QVulkanInstance 有效、核心版本/扩展已启用，再区分实例级与设备级函数并检查 VkResult 或返回指针。

**签名拆解：**

- 返回值：`QVulkanDeviceFunctions *`。
- 参数 `device`：类型为 `VkDevice`。没有默认值，调用时必须提供。QIODevice 或绘制设备。调用前要确认已经打开、支持所需模式，或处于合法绘制阶段。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QVulkanInstance::resetDeviceFunctions(VkDevice device)`

**API 类别：** 配套与继承 API

**中文解读：** `resetDeviceFunctions` 属于 Vulkan 动态函数取得或调用过程。先保证 QVulkanInstance 有效、核心版本/扩展已启用，再区分实例级与设备级函数并检查 VkResult 或返回指针。

**签名拆解：**

- 返回值：`void`。
- 参数 `device`：类型为 `VkDevice`。没有默认值，调用时必须提供。QIODevice 或绘制设备。调用前要确认已经打开、支持所需模式，或处于合法绘制阶段。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `PFN_vkVoidFunction QVulkanDeviceFunctions::vkGetDeviceProcAddr(VkDevice device, const char *name)`

**API 类别：** 配套与继承 API

**中文解读：** `vkGetDeviceProcAddr` 属于 Vulkan 动态函数取得或调用过程。先保证 QVulkanInstance 有效、核心版本/扩展已启用，再区分实例级与设备级函数并检查 VkResult 或返回指针。

**签名拆解：**

- 返回值：`PFN_vkVoidFunction`。
- 参数 `device`：类型为 `VkDevice`。没有默认值，调用时必须提供。QIODevice 或绘制设备。调用前要确认已经打开、支持所需模式，或处于合法绘制阶段。
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

不要直接构造 `QVulkanFunctions`/`QVulkanDeviceFunctions`；不要把 instance 级和 device 级函数混用；不要假设扩展函数自动存在；不要忽略平台和驱动能力。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QVulkanDeviceFunctions` 所属机制类型：Vulkan 动态函数解析机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
