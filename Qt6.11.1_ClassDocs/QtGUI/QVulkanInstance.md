# QVulkanInstance
> Qt 6.11.1 · Qt GUI · 来自 `QVulkanInstance`

## 1. 先建立直觉

`QVulkanInstance` 包装 Vulkan 的 `VkInstance`，并把它接入 Qt 的窗口系统。它负责启用 instance layer/extension、创建实例、加载函数表、为 `QWindow`/`QVulkanWindow` 提供 Vulkan surface 支持。

## 2. 类说明

- 头文件：`#include <QVulkanInstance>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 类型：Qt Vulkan instance 管理类
- 协作类：`QVulkanWindow`、`QVulkanFunctions`、`QVulkanDeviceFunctions`

必须在创建 Vulkan surface/window 前设置到 `QGuiApplication` 或相关窗口体系中。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `setLayers()` / `layers()` | 设置或读取启用的 instance layers |
| `setExtensions()` / `extensions()` | 设置或读取启用的 instance extensions |
| `setApiVersion()` / `apiVersion()` | Vulkan API 版本 |
| `create()` / `isValid()` | 创建实例并判断是否成功 |
| `destroy()` | 销毁实例 |
| `vkInstance()` | 取得原生 `VkInstance` |
| `functions()` | instance 级函数表 |
| `deviceFunctions(device)` | device 级函数表 |
| `getInstanceProcAddr()` | 原生函数加载入口 |
| `supportedLayers()` / `supportedExtensions()` | 查询 loader 支持项 |
| `supportsPresent()` | 查询物理设备/队列是否支持向窗口呈现 |
| `installDebugOutputFilter()` / `removeDebugOutputFilter()` | 安装 Vulkan debug 输出过滤 |

## 4. 关键用法

```cpp
QVulkanInstance inst;
inst.setLayers({"VK_LAYER_KHRONOS_validation"});
if (!inst.create())
    return;

QGuiApplication::setAttribute(Qt::AA_ShareOpenGLContexts); // 示例：按项目需要设置属性
window->setVulkanInstance(&inst);
```

实际启用 layers/extensions 前先用 `supportedLayers()`、`supportedExtensions()` 检查，避免用户机器缺少 validation layer 时直接失败。

## 5. 使用场景

- Qt 应用中初始化 Vulkan。
- 给 `QVulkanWindow` 提供 instance。
- 自定义 Vulkan renderer 与 Qt window surface 集成。
- 开启 validation layer 和 debug 输出。
- 查询平台呈现支持。

## 6. 常见坑与经验

- `create()` 前设置 layers/extensions；创建后再改不会影响已有 VkInstance。
- Qt/平台需要的 surface extension 通常由 Qt 协助处理，但自定义流程仍要确认扩展。
- validation layer 不是用户机器必有，发布版要优雅降级。
- `destroy()` 前确保所有依赖该 instance 的 Vulkan 对象和窗口已处理完。

## 7. 知识点覆盖

VkInstance、layer/extension、函数表、debug output、surface/present 支持、Qt 窗口集成。
