# QVulkanInfoVector
> Qt 6.11.1 · Qt GUI · 来自 `QVulkanInfoVector`

## 1. 先建立直觉

`QVulkanInfoVector` 是 Qt 为 Vulkan 查询结构数组提供的便利容器。Vulkan 很多查询先要拿数量，再分配数组，再填结构；这个类型让 Qt API 返回层、扩展等信息时更顺手。

## 2. 类说明

- 头文件：`#include <QVulkanInfoVector>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 类型：模板容器风格辅助类型
- 协作类：`QVulkanInstance`

它主要出现在支持层、扩展列表等 Vulkan 信息查询中。

## 3. API 速查

| API | 作用 |
| --- | --- |
| 容器访问 | 保存 Vulkan info 结构数组 |
| `QVulkanInstance::supportedLayers()` | 返回可用 layer 信息 |
| `QVulkanInstance::supportedExtensions()` | 返回可用 extension 信息 |

## 4. 关键用法

```cpp
for (const auto &layer : QVulkanInstance::supportedLayers())
    qDebug() << layer.layerName;
```

字段来自 Vulkan 原生结构，比如 layer name、extension name、spec version 等。

## 5. 使用场景

- 枚举 validation layer。
- 检查 instance extension 是否可用。
- 诊断用户机器 Vulkan 环境。
- 创建 `QVulkanInstance` 前决定启用哪些 layer/extension。

## 6. 常见坑与经验

- 查询结果代表当前 loader 和平台环境，不代表所有 GPU device 能力。
- layer/extension 名称是字节字符串，比较时注意编码和精确名称。
- 启用不存在的 layer 或 extension 会导致 instance 创建失败。

## 7. 知识点覆盖

Vulkan layer、extension、loader 查询、创建前能力检查、信息结构数组。
