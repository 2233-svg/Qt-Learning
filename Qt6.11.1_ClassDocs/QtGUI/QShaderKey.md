# QShaderKey
> Qt 6.11.1 · Qt GUI · 来自 `QShaderKey`

## 1. 先建立直觉

`QShaderKey` 是从 `QShader` 包里定位某个具体 shader 版本的钥匙。它由三部分组成：代码来源格式、着色语言版本、变体。只说“我要 fragment shader”还不够；stage 存在 `QShader` 上，key 负责区分“GLSL 440 core 标准版”还是“MSL batchable 变体”等。

## 2. 类说明

- 头文件：`#include <QShaderKey>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 类型：值类型，可排序、可比较、可哈希
- 协作类：`QShader`、`QShaderVersion`、`QShaderCode`

它常作为 `QMap` 或 `QHash` 的 key。`operator<` 让它能稳定排序，便于序列化和调试输出。

## 3. API 速查

| API | 作用 |
| --- | --- |
| 默认构造 | 创建空 key，通常随后设置字段 |
| `QShaderKey(source, version, variant)` | 一次性指定格式、版本、变体 |
| `setSource()` / `source()` | 设置或读取 `QShader::Source` |
| `setSourceVersion()` / `sourceVersion()` | 设置或读取 `QShaderVersion` |
| `setSourceVariant()` / `sourceVariant()` | 设置或读取 `QShader::Variant` |
| `operator<` | 为 key 建立排序 |
| `operator==` / `operator!=` / `qHash()` | 比较与哈希 |

## 4. 关键用法

```cpp
QShaderKey glslKey(QShader::GlslShader,
                   QShaderVersion(440),
                   QShader::StandardShader);

QShaderCode glsl = shader.shader(glslKey);
```

OpenGL ES GLSL 需要版本标志：

```cpp
QShaderKey esKey(QShader::GlslShader,
                 QShaderVersion(300, QShaderVersion::GlslEs));
```

不要把 `QShaderVersion(300)` 和 `QShaderVersion(300, GlslEs)` 混为一谈；它们代表不同语言族。

## 5. 使用场景

- 查询 `QShader::availableShaders()` 后选择当前后端可用版本。
- 构建 shader 包时为每段代码建立索引。
- 删除某个后端版本或变体。
- 做 shader cache key 的一部分。

## 6. 常见坑与经验

- `sourceVariant()` 默认是 `StandardShader`，Qt Quick 或 HDR 场景需要的特殊变体不能省略。
- GLSL 版本数字不是 Qt 版本，也不是 OpenGL 运行时版本对象；它表示着色语言版本。
- key 不包含 stage；同一个 key 在不同 stage 的 `QShader` 上都有可能存在。
- 取 shader 前最好先看 `availableShaders()`，不要假设 `.qsb` 包含所有后端。

## 7. 知识点覆盖

本页覆盖：shader 版本定位、source/version/variant 三元组、GLSL ES 标志、排序和哈希、shader 包查询。
