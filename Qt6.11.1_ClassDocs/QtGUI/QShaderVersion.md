# QShaderVersion
> Qt 6.11.1 · Qt GUI · 来自 `QShaderVersion`

## 1. 先建立直觉

`QShaderVersion` 描述着色语言版本，以及它是否属于 GLSL ES。它通常作为 `QShaderKey` 的一部分，用来区分同一种 source 下的不同语言目标。

## 2. 类说明

- 头文件：`#include <QShaderVersion>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 类型：值类型，可比较、可排序
- 协作类：`QShaderKey`

版本号的解释取决于 shader source。对 GLSL 来说，`440` 表示 `#version 440`，`300 + GlslEs` 表示 `#version 300 es`。

## 3. API 速查

| API | 作用 |
| --- | --- |
| 默认构造 | 创建默认版本对象 |
| `QShaderVersion(v, flags)` | 指定版本号和标志 |
| `setVersion()` / `version()` | 设置或读取版本数字 |
| `setFlags()` / `flags()` | 设置或读取标志 |
| `GlslEs` | 表示 GLSL ES 语言族 |
| `operator<` / `operator==` / `operator!=` | 排序和比较 |

## 4. 关键用法

```cpp
QShaderVersion desktop440(440);
QShaderVersion es300(300, QShaderVersion::GlslEs);
```

两者都可能用于 `QShader::GlslShader`，但它们不是同一种 shader。桌面 GLSL 和 GLSL ES 的语法、内置支持和平台目标不同。

## 5. 使用场景

- 选择合适的 GLSL 输出版本。
- 区分 OpenGL 桌面与 OpenGL ES shader。
- 参与 `QShaderKey` 的排序、查找和序列化。
- 构建工具生成多目标 shader 包。

## 6. 常见坑与经验

- `version()` 返回整数，不带 `#version` 字符串里的 `es`，`es` 在 flags。
- 对 SPIR-V、DXIL、MetalLib 等二进制目标，版本语义可能不像 GLSL 那样直观，通常按工具链生成的 key 使用即可。
- 默认构造的版本对象不代表“当前平台最佳版本”，不要拿它做自动选择。

## 7. 知识点覆盖

本页覆盖：着色语言版本、GLSL ES 标志、`QShaderKey` 组合、版本比较、跨后端 shader 目标选择。
