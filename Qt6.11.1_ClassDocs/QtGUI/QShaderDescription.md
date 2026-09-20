# QShaderDescription
> Qt 6.11.1 · Qt GUI · 来自 `QShaderDescription`

## 1. 先建立直觉

`QShaderDescription` 是 shader 反射信息。它告诉你 shader 声明了哪些输入输出、uniform block、storage block、采样器、storage image、push constant，以及 compute/tessellation 相关元数据。

如果 `QShaderCode` 是机器要执行的代码，`QShaderDescription` 就是人和引擎用来正确绑定资源的说明书。

## 2. 类说明

- 头文件：`#include <QShaderDescription>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 类型：隐式共享值类型
- 协作类：`QShader`、`QRhiShaderResourceBinding`、shader 构建工具 `qsb`

Qt 6.6 起把多个反射结构体公开成具名类型，如 `UniformBlock`、`StorageBlock`、`InOutVariable`、`BlockVariable`、`BuiltinVariable`、`PushConstantBlock`。实际字段用于描述 binding、set、location、name、type、offset、size、array 维度等。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `isValid()` | 是否包含有效反射内容 |
| `inputVariables()` / `outputVariables()` | 普通输入输出变量，如 vertex attribute 和 fragment output |
| `inputBuiltinVariables()` / `outputBuiltinVariables()` | 内置变量，如 position、frag coord、vertex id |
| `uniformBlocks()` | uniform buffer block 列表 |
| `storageBlocks()` | SSBO/storage buffer block 列表 |
| `combinedImageSamplers()` | combined image sampler 资源 |
| `storageImages()` | image load/store 资源 |
| `pushConstantBlocks()` | push constant block 反射 |
| `computeShaderLocalSize()` | compute shader local size |
| `tessellationMode()` / `tessellationPartitioning()` / `tessellationWindingOrder()` | tessellation 元数据 |
| `tessellationOutputVertexCount()` | tessellation 输出顶点数 |
| `toJson()` | 导出 JSON，适合调试和工具链 |
| `serialize()` / `deserialize()` | 以 QSB 版本读写反射数据 |

## 4. 枚举速查

| 枚举 | 说明 |
| --- | --- |
| `VariableType` | 标量、向量、矩阵、sampler、image、struct、half 等变量类型 |
| `BuiltinType` | `PositionBuiltin`、`FragCoordBuiltin`、`VertexIndexBuiltin` 等内置变量 |
| `ImageFormat` | storage image 的格式，如 `ImageFormatRgba32f`、`ImageFormatR8ui` |
| `ImageFlags` | image 是否 read-only/write-only |
| `QualifierFlags` | `readonly`、`writeonly`、`coherent`、`volatile`、`restrict` 等限定 |
| `TessellationMode` | triangles、quad、isoline |
| `TessellationPartitioning` | equal、fractional even、fractional odd |
| `TessellationWindingOrder` | clockwise / counter-clockwise |

## 5. 关键用法

检查 uniform block：

```cpp
QShaderDescription desc = shader.description();
for (const auto &block : desc.uniformBlocks()) {
    qDebug() << block.blockName << block.binding << block.size;
}
```

检查 vertex 输入 location：

```cpp
for (const auto &v : desc.inputVariables())
    qDebug() << v.name << v.location << v.type;
```

这能帮助你确认 `QRhiVertexInputAttribute` 的 location、format 与 shader 是否一致，也能检查资源 binding 是否与 `QRhiShaderResourceBinding` 对齐。

## 6. 使用场景

- 自动生成 uniform buffer C++ 结构体或校验 offset。
- 根据 shader 反射创建资源绑定表。
- 调试 `.qsb` 包，输出 JSON 查看资源声明。
- 生成材质编辑器 UI，列出 shader 需要的纹理和常量。
- 校验 compute local size 和 dispatch 参数。

## 7. 常见坑与经验

- `pushConstantBlocks()` 有反射信息不代表 Qt RHI 就支持 push constants；Qt 文档提醒不要依赖它配合 RHI。
- storage block 的运行时数组最后一个成员大小可能未知，`knownSize` 不等于实际 buffer 总大小。
- combined sampler 在 GLSL/Vulkan 中常见，但 HLSL/Metal 可能拆成 texture 和 sampler，需结合 `QShader` 的 mapping。
- `isValid()` 只说明反射有内容，不说明 shader 一定能在当前 GPU 创建 pipeline。
- 反射里的 binding 通常遵循 SPIR-V/Vulkan 模型，跨后端原生 binding 要看 `QShader::nativeResourceBindingMap()`。

## 8. 知识点覆盖

本页覆盖：shader 反射、变量类型、uniform/storage block、sampler/image、内置变量、compute local size、tessellation 元数据、JSON 调试、资源绑定校验。
