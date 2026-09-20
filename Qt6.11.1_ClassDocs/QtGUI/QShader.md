# QShader
> Qt 6.11.1 · Qt GUI · 来自 `QShader`

## 1. 先建立直觉

`QShader` 是 Qt shader 包的内存表示。一个 `QShader` 可以同时保存同一着色器的多个后端版本，例如 SPIR-V、GLSL、HLSL、MSL、DXIL、WGSL，并带有反射信息、入口点、本地资源绑定映射等元数据。

它常见于 Qt 的 RHI、Qt Quick scene graph、`qsb` 生成的 `.qsb` 文件加载，以及需要跨图形 API 分发 shader 的工具链。

## 2. 类说明

- 头文件：`#include <QShader>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 类型：隐式共享值类型，可复制，可移动
- 协作类：`QShaderKey`、`QShaderCode`、`QShaderVersion`、`QShaderDescription`

`QShader` 不是运行时编译器。实际项目通常用 `qsb` 预生成 shader 包，运行时用 `fromSerialized()` 读取，再按当前后端选取合适的 `QShaderCode`。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `fromSerialized(data)` | 从 `.qsb` 二进制数据恢复 `QShader` |
| `serialized(version)` | 把 shader 包序列化，适合写文件或资源 |
| `isValid()` | 是否至少包含一个 shader 版本 |
| `setStage()` / `stage()` | 设置或读取 vertex/fragment/compute 等阶段 |
| `setShader(key, code)` / `shader(key)` | 按 `QShaderKey` 存取某个后端版本 |
| `availableShaders()` | 列出包里已有的所有 key |
| `setDescription()` / `description()` | 设置或读取反射信息 |
| `setResourceBindingMap()` / `nativeResourceBindingMap()` | 保存 SPIR-V binding 到后端原生 binding 的映射 |
| `setNativeShaderInfo()` / `nativeShaderInfo()` | 保存 Metal 等后端需要的额外信息 |
| `setSeparateToCombinedImageSamplerMappingList()` | 记录独立 texture/sampler 与 combined sampler 的映射 |
| `removeShader()` 等 remove 函数 | 删除指定 key 下的代码或元数据 |
| `swap()` | 快速交换两个 shader 包 |

## 4. 枚举速查

| 枚举 | 用途 |
| --- | --- |
| `Source` | 代码格式：`SpirvShader`、`GlslShader`、`HlslShader`、`DxbcShader`、`MslShader`、`DxilShader`、`MetalLibShader`、`WgslShader` |
| `Stage` | 管线阶段：vertex、tess control/eval、geometry、fragment、compute |
| `Variant` | 同一 shader 的特殊变体，如 Qt Quick batchable vertex、HDR fragment、Metal tessellation 相关 compute 变体 |
| `SerializedFormatVersion` | 序列化兼容版本；默认 `Latest` |

## 5. 关键用法

从资源加载 `.qsb`：

```cpp
QFile f(":/shaders/color.frag.qsb");
f.open(QIODevice::ReadOnly);
QShader shader = QShader::fromSerialized(f.readAll());
if (!shader.isValid())
    return;
```

根据后端取特定版本：

```cpp
QShaderKey key(QShader::SpirvShader, QShaderVersion(100));
QShaderCode code = shader.shader(key);
```

通常不建议业务代码手工拼完整 `QShader` 包；更稳的做法是把 GLSL/Vulkan 源交给 `qsb`，让工具生成 SPIR-V、目标语言、反射和绑定映射。

## 6. 使用场景

- Qt Quick 自定义材质或 scene graph 节点使用 `.qsb`。
- RHI 渲染器在不同图形 API 后端加载同一个逻辑 shader。
- 构建工具或资源管线检查 shader 包内容。
- 根据 `QShaderDescription` 自动生成 uniform buffer 布局或调试信息。
- 做向旧 Qt 版本兼容的 shader 资产输出。

## 7. 常见坑与经验

- `.qsb` 应视为可信资产，不要随便加载用户提供的 shader 包；反序列化不是沙盒。
- `SerializedFormatVersion` 选旧版本会丢失新 Qt 引入的元数据，除非确实要兼容旧运行时。
- `QShaderKey` 必须把 source、version、variant 都匹配上；取不到代码时返回空 `QShaderCode`。
- SPIR-V 的 binding 模型与 Metal/HLSL 不完全一致，后端需要 binding map 辅助，别自己假设所有语言资源编号相同。
- move 之后的 `QShader` 只适合销毁或重新赋值，不要继续读取。

## 8. 知识点覆盖

本页覆盖：qsb 资产、跨后端 shader 包、shader stage/source/variant、反射信息、资源绑定映射、序列化兼容、安全边界。
