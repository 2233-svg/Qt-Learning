# QRhiShaderStage

> Qt 6.11.1 · Qt GUI Private · 来自 `QRhiShaderStage`

## 1. 先建立直觉

`QRhiShaderStage` 是“某个 pipeline 阶段使用哪份 `QShader`”的描述对象。图形 pipeline 通常包含 Vertex 和 Fragment；计算 pipeline 只包含 Compute；几何、细分阶段则需要对应后端 feature 支持。

`QShader` 是多后端 shader 包，可能包含 SPIR-V、MSL、HLSL、GLSL 等代码以及不同 variant。`QRhiShaderStage` 负责说明这份 shader 包用于哪个阶段，并选择哪个 `QShader::Variant`。

## 2. 类说明

- 头文件：`#include <rhi/qrhi.h>`
- CMake：`Qt6::GuiPrivate`
- 类型性质：值类型，可比较、可哈希
- 使用入口：`QRhiGraphicsPipeline::setShaderStages()`、`QRhiComputePipeline::setShaderStage()`
- 核心字段：stage type、`QShader`、shader variant

stage type 必须和 shader 本身内容匹配。把 fragment shader 放进 vertex stage 不会变成自动转换，而是 pipeline 创建失败或后端错误。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `Type::Vertex` | 顶点阶段。 |
| `Type::Fragment` | 片段/像素阶段。 |
| `Type::Compute` | 计算阶段，需要 `QRhi::Compute`。 |
| `Type::Geometry` | 几何阶段，需要 `QRhi::GeometryShader`。 |
| `Type::TessellationControl` / `TessellationEvaluation` | 细分控制/评估阶段，需要 `QRhi::Tessellation`。 |
| `QRhiShaderStage(type, shader, variant)` | 构造阶段描述。 |
| `setType()` / `type()` | 设置/读取阶段类型。 |
| `setShader()` / `shader()` | 设置/读取 `QShader`。 |
| `setShaderVariant()` / `shaderVariant()` | 设置/读取 shader variant。 |
| `operator==` / `qHash()` | 用于比较和缓存键。 |

## 4. 关键用法

```cpp
ps->setShaderStages({
    QRhiShaderStage(QRhiShaderStage::Vertex, vertexShader),
    QRhiShaderStage(QRhiShaderStage::Fragment, fragmentShader)
});
```

compute pipeline 则只能设置 compute stage：

```cpp
computePs->setShaderStage(
    QRhiShaderStage(QRhiShaderStage::Compute, computeShader));
```

## 5. 使用场景

- 图形 pipeline 中组织 vertex/fragment shader。
- compute pipeline 中指定 compute shader。
- 根据材质/宏/变体选择不同 `QShader::Variant`。
- pipeline cache key 中包含 shader stage 信息。
- 在支持的后端上启用 geometry/tessellation shader。

## 6. 常见坑与经验

- **stage type 要和 shader 匹配。** `QShader` 包里必须有对应阶段和后端可用代码。
- **高级阶段先查 feature。** Geometry、Tessellation、Compute 都不是所有后端都支持。
- **variant 不是运行时 uniform。** 它通常代表编译/打包时准备的 shader 变体。
- **空 QShader 不能创建有效 pipeline。** 默认构造 stage 只适合作占位。
- **跨后端要依赖 qsb 产物。** 不要假设某一种 shader 源码能被所有后端运行时编译。

## 7. 知识点覆盖

- RHI shader stage 与 `QShader` 包
- graphics/compute pipeline 的 shader 组织
- shader variant、feature 查询和高级阶段
- pipeline cache 中 shader stage 的身份
