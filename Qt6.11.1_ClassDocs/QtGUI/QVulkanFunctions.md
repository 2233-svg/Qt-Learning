# QVulkanFunctions
> Qt 6.11.1 · Qt GUI · 来自 `QVulkanFunctions`

## 1. 先建立直觉

`QVulkanFunctions` 是 Qt 提供的 Vulkan instance 级函数表。它帮你拿到当前 `QVulkanInstance` 上可用的 Vulkan 函数指针，避免手动到处调用 `vkGetInstanceProcAddr`。

## 2. 类说明

- 头文件：`#include <QVulkanFunctions>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 获取方式：`QVulkanInstance::functions()`
- 协作类：`QVulkanInstance`、`QVulkanDeviceFunctions`

它主要面向 Vulkan 低层渲染代码。Qt 不隐藏 Vulkan 同步、内存和对象生命周期。

## 3. API 速查

| API | 作用 |
| --- | --- |
| Vulkan instance 函数包装 | 调用枚举物理设备、查询属性、创建 surface 相关对象等 instance 级函数 |
| `QVulkanInstance::functions()` | 取得与实例绑定的函数表 |

## 4. 关键用法

```cpp
QVulkanFunctions *f = inst.functions();
uint32_t count = 0;
f->vkEnumeratePhysicalDevices(inst.vkInstance(), &count, nullptr);
```

device 级函数应使用 `QVulkanDeviceFunctions`，不要混用层级。

## 5. 使用场景

- 枚举 physical device。
- 查询 Vulkan instance 级能力。
- 编写自定义 Vulkan 渲染器。
- 与 `QVulkanWindow` 以外的 Vulkan 初始化流程集成。

## 6. 常见坑与经验

- 必须在 `QVulkanInstance::create()` 成功后使用。
- Vulkan 函数层级严格，device 函数不要从 instance function table 里找。
- Qt 只是加载函数，不替你处理 VkResult、同步和销毁顺序。

## 7. 知识点覆盖

Vulkan instance 函数表、函数加载、VkInstance、低层渲染初始化、instance/device 分层。
