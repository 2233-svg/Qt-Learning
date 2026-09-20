# QShaderBaker
> Qt 6.11.1 · Qt Shader Tools · 来自 `QShaderBaker`

## 1. 先建立直觉

`QShaderBaker` 是把 shader 源码“烘焙”为 `QShader` 的 C++ API。它和命令行工具 `qsb` 处理的是同一类问题：从一份 GLSL/HLSL/MSL 等输入出发，生成 Qt RHI 能按目标图形后端挑选的 shader 包。

要把它理解成“shader 打包器”，而不是运行时渲染对象。它不会画任何东西，也不会替你创建 pipeline；它的产物 `QShader` 才会被材质、效果、QRhi 或 Quick 场景图相关代码消费。

## 2. 类说明

`QShaderBaker` 是值语义风格的配置对象：先设置输入、目标语言/版本、变体、编译选项，再调用 `bake()` 得到 `QShader`。如果失败，通过 `errorMessage()` 取诊断文本。

它常出现在自定义构建工具、编辑器预览器、shader 热重载工具和需要在运行时生成 shader 的专业软件里。普通应用更推荐在构建阶段用 `qsb` 生成 `.qsb` 资源，启动时直接加载，避免把编译成本放到用户机器上。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `setSourceFileName(fileName)` | 从 shader 文件读取源代码，并让文件名进入错误信息。 |
| `setSourceFileName(fileName, stage)` | 指定 shader stage 的文件输入，适合非默认推断或多阶段处理。 |
| `setSourceString(source, stage, fileName)` | 从内存字符串提供 shader 源码，适合编辑器、测试、热重载。 |
| `setSourceDevice(device, stage, fileName)` | 从 `QIODevice` 读取源码，方便资源、网络缓存或自定义存储。 |
| `setGeneratedShaders(list)` | 声明要生成哪些目标源码/字节码和版本。 |
| `setGeneratedShaderVariants(variants)` | 生成标准、批处理顶点输入等变体。 |
| `setPreamble(bytes)` | 给源码前面注入宏或公共声明。 |
| `setPerTargetCompilation(bool)` | 对每个目标分别编译，使目标相关宏生效。 |
| `setBreakOnShaderTranslationError(bool)` | 某个目标翻译失败时是否立刻失败。 |
| `setSpirvOptions(options)` | 控制 SPIR-V 调试信息、剥离变量信息等。 |
| `setGlslOptions(options)` | 控制 GLSL 输出细节，例如 ES fragment 默认精度。 |
| `setMultiViewCount(count)` | 生成 multiview 相关 shader 代码。 |
| `setTessellationMode(mode)` | 指定曲面细分模式。 |
| `setTessellationOutputVertexCount(count)` | 指定 tessellation 输出顶点数。 |
| `setBatchableVertexShaderExtraInputLocation(location)` | 为可批处理顶点 shader 追加输入位置。 |
| `bake()` | 执行烘焙，返回 `QShader`。 |
| `errorMessage()` | 读取最近一次烘焙或配置产生的错误文本。 |
| `GeneratedShader` | 目标 shader 类型与版本的组合，通常是 `(QShader::Source, QShaderVersion)`。 |
| `SpirvOptions` | SPIR-V 输出选项集合。 |
| `GlslOptions` | GLSL 输出选项集合。 |

## 4. 典型流程

```cpp
QShaderBaker baker;
baker.setSourceFileName(u":/shaders/effect.vert"_s, QShader::VertexStage);
baker.setGeneratedShaders({
    { QShader::SpirvShader, QShaderVersion(100) },
    { QShader::GlslShader,  QShaderVersion(440) },
    { QShader::GlslShader,  QShaderVersion(300, QShaderVersion::GlslEs) }
});
baker.setGeneratedShaderVariants({ QShader::StandardShader });

QShader shader = baker.bake();
if (!shader.isValid())
    qWarning() << baker.errorMessage();
```

这里最关键的是“输入”和“输出目标”都要明确。只设置源文件但不声明生成目标，通常拿不到你想要的跨后端 shader 包。

## 5. 使用场景

| 场景 | 建议 |
| --- | --- |
| 应用固定 shader | 构建阶段用 `qsb`，把 `.qsb` 放进资源。 |
| shader 编辑器或材质编辑器 | 使用 `setSourceString()` 加 `bake()` 实时预览，但要把编译放在后台线程。 |
| 自动化资源流水线 | 用 `QShaderBaker` 写 C++ 打包工具，方便和 Qt 类型直接协作。 |
| 需要目标宏差异 | 开启 `setPerTargetCompilation(true)`，但要保证不同目标的接口描述兼容。 |
| 调试 shader 变量映射 | 先保留调试/变量信息，发布包再考虑剥离。 |

## 6. 常见坑与经验

`QShaderBaker` 的成本不低，尤其是多目标、多变体、多阶段时。图形界面里实时烘焙要放到工作线程，并设计节流；用户每敲一个字符就同步 `bake()`，体验会很差。

`setPerTargetCompilation(true)` 能让 `QSHADER_SPIRV`、`QSHADER_GLSL` 等目标宏参与编译，但别把这些宏误解成具体图形 API。它们描述的是输出语言/格式，不是 Vulkan、OpenGL、Metal 的运行时选择。

`QShaderBaker` 只负责产生 SPIR-V 和可读源码等 Qt shader 表示。面向 D3D 或 Metal 的更底层 native 产物通常由 `qsb` 的额外处理完成，不要假设 C++ API 覆盖命令行工具的每个发布流水线能力。

同一个 `QShader` 内不同目标最好保持一致的资源绑定、输入输出变量和反射描述。某个目标“能翻译过去”不代表整包在 Qt RHI 中就能被同一套材质代码安全消费。

## 7. 知识点覆盖

- Qt shader 包与 `QShader` 的关系。
- `qsb` 命令行流程和 `QShaderBaker` C++ API 的边界。
- shader stage、target source、`QShaderVersion`、variant 的组合方式。
- SPIR-V、GLSL/GLSL ES、多视图、tessellation 的配置入口。
- 编译诊断、错误文本、后台线程和编辑器热重载设计。
