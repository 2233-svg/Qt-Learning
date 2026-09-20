# Qt QShader：多后端着色器包与反射元数据

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QShader>`  
> RHI 头文件：`#include <rhi/qshader.h>`  
> 所属模块：`Qt6::Gui`  
> 继承：无  
> 类型定位：包含多种着色器版本和反射信息的值类型

## 1. 它解决什么问题

`QShader` 是 Qt Rendering Hardware Interface（RHI）使用的着色器包。一个 `QShader` 不只保存一份 GLSL 或 SPIR-V 文本，而是可以同时保存：

- 面向不同图形后端的着色器源代码或字节码；
- 每份代码对应的语言、版本和变体键；
- 着色器属于顶点、片段、计算等哪一个管线阶段；
- 顶点输入、输出、uniform block 和其他资源的反射描述；
- 原生资源绑定映射、独立纹理/采样器组合映射和其他后端附加信息；
- 可写入 `.qsb` 等二进制资源的序列化内容。

它解决的是“同一个 shader 资产如何在 Vulkan、OpenGL、Direct3D、Metal 和 WebGPU 等后端之间选择合适代码”的问题。应用通常在构建阶段用 `qsb` 生成 shader package，运行时读取并反序列化；RHI 再根据后端选择可用的 `QShaderKey`。

`QShader` 不是着色器编译器，也不是 GPU 上已经创建好的 shader module。它是 CPU 侧的值对象和资产容器。实际编译通常由 `qsb` 或 `QShaderBaker` 完成，实际 GPU 资源创建由 `QRhi` 和图形管线对象完成。

## 2. 兼容性与构建边界

### 2.1 这是有限兼容性的 RHI API

Qt 6.11.1 文档明确警告，`QRhi` 家族、`QShader` 和 `QShaderDescription` 没有源代码兼容性和二进制兼容性保证。应用只能把它们视为与编译时所用 Qt 版本绑定的 API；Qt 可能在小版本中进行源不兼容调整。

使用这组 API 时，应：

- 按当前 Qt 版本重新编译应用；
- 不把 `QShader` 作为跨版本公共 ABI 的参数类型；
- 不依赖其内部布局、序列化私有细节或私有头文件中的实现；
- 把 RHI 适配代码集中在较小的模块中。

### 2.2 CMake 和头文件

Qt 文档的基础头文件写法是：

```cpp
#include <QShader>
```

同时，文档提醒这组 RHI API 应链接 `Qt::GuiPrivate`，并使用带 `rhi` 前缀的头文件：

```cpp
#include <rhi/qshader.h>
```

CMake 示例：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui GuiPrivate)
target_link_libraries(mytarget PRIVATE Qt6::Gui Qt6::GuiPrivate)
```

qmake 工程至少使用：

```qmake
QT += gui
```

具体工程是否允许链接 `GuiPrivate`，还要结合 Qt 的部署策略和项目对有限兼容性 API 的接受程度。

## 3. 最小使用方式

### 3.1 从预编译 `.qsb` 资源读取

```cpp
#include <QFile>
#include <rhi/qshader.h>

QShader loadShaderPackage(const QString &path)
{
    QFile file(path);
    if (!file.open(QIODevice::ReadOnly))
        return {};

    QShader shader = QShader::fromSerialized(file.readAll());
    if (!shader.isValid())
        return {};

    return shader;
}
```

生产项目通常在构建阶段运行 `qsb`，把生成的二进制文件作为应用资源或随程序部署，而不是在每次启动时编译 shader。

### 3.2 手工建立一个简单的键值包

```cpp
#include <rhi/qshader.h>

QShader makeShader()
{
    QShader shader;
    shader.setStage(QShader::VertexStage);

    QShaderVersion version(450);
    QShaderKey key(QShader::GlslShader, version);
    shader.setShader(key, QShaderCode(
        QByteArrayLiteral("#version 450\nvoid main() {}"),
        QByteArrayLiteral("main")));

    return shader;
}
```

这个示例只说明数据模型：`QShaderKey` 决定代码条目，`QShaderCode` 保存代码和入口点，`setStage()` 指定管线阶段。手工写入的 GLSL 不等于已经通过编译，也不一定包含 RHI 所需的全部反射信息；实际渲染资产应使用 `qsb` 或 `QShaderBaker` 生成。

### 3.3 交给 RHI 管线

RHI 图形管线或计算管线需要着色器时，通常直接传入对应的 `QShader`：

```cpp
QRhiGraphicsPipeline *pipeline = rhi->newGraphicsPipeline();
pipeline->setVertexShader(vertexShader);
pipeline->setFragmentShader(fragmentShader);
```

具体管线还必须设置顶点输入、资源绑定、渲染目标格式等其他信息。`QShader` 只提供 shader package 和反射数据，不会替你完成整个 pipeline 配置。

## 4. 核心使用模型

### 4.1 `QShaderKey` 是选择代码条目的完整键

一个 shader package 可以保存多份代码。查询时不能只传“GLSL”或“顶点阶段”，而要使用 `QShaderKey` 指定：

- `QShader::Source`：语言或二进制格式；
- `QShaderVersion`：语言版本以及例如 GLSL ES 标志；
- `QShader::Variant`：标准、可批处理或后端特殊变体。

`availableShaders()` 返回 package 中已有的键。应用通常先根据目标后端选择一个 key，再调用 `shader(key)`。如果 key 不存在，得到的 `QShaderCode::shader()` 为空，不能把它当作自动回退成功。

### 4.2 一个 package 包含多个“代码 + 元数据”层次

可以把结构理解成：

```text
QShader
  ├─ stage
  ├─ description
  ├─ QShaderKey -> QShaderCode
  ├─ QShaderKey -> NativeResourceBindingMap
  ├─ QShaderKey -> SeparateToCombinedImageSamplerMappingList
  └─ QShaderKey -> NativeShaderInfo
```

shader code 用 `QShaderKey` 索引；后端绑定映射和原生附加信息也按 key 存储。不要把某个 GLSL key 的后端映射无条件套到另一个版本、变体或语言上。

### 4.3 `Stage` 是整个 shader 的管线阶段

`stage()` 和 `setStage()` 作用于 `QShader` 包本身，而不是某个 `QShaderKey`。一个 package 内的不同代码版本应服务于同一个管线阶段；如果需要顶点和片段代码，应使用两个 `QShader`。

### 4.4 反射描述是资源布局协作的入口

`description()` 返回 `QShaderDescription`，其中包含 shader 输入、输出和 uniform block 等资源信息。应用或框架不知道 shader 预先布局时，可以使用反射信息生成顶点输入和资源绑定配置。

反射描述不等于运行时 GPU 验证。实际 pipeline 仍可能因为资源类型、格式、绑定数量或后端限制不匹配而创建失败。

### 4.5 值语义和隐式共享

`QShader` 使用类似 Qt Core 值类型的隐式共享机制，可以按值返回、复制和放入容器。调用 setter 时会自动 detach，使修改不会改变其他共享副本。

因此：

- 读取一个 `QShader` 的副本通常成本较低；
- 不要把“复制对象”误认为深拷贝后就能共享同一个可变状态；
- 修改副本后，原对象仍保持自己的数据；
- `detach()` 可以显式分离共享存储，但大多数代码不需要手动调用。

## 5. 生成与部署工作流

### 5.1 构建时用 `qsb`

推荐工作流是：

```text
shader source
    -> qsb / QShaderBaker
    -> 多种后端代码 + 反射元数据
    -> serialized QShader package
    -> 随应用部署
    -> fromSerialized()
    -> QRhi graphics/compute pipeline
```

生成的 package 应与运行时使用的 Qt 版本和目标后端策略一起测试。`SerializedFormatVersion::Latest` 默认面向当前 Qt 版本。

### 5.2 运行时用 `QShaderBaker`

运行时编译适合用户提供 shader、动态生成 shader 或开发工具，但它是昂贵操作，可能涉及 shader 编译器、文件和平台工具。普通应用启动路径不应把大量 shader 编译放在首帧之前。

### 5.3 序列化数据视为可信资产

Qt 文档警告，shader package，包括文件系统中的 `.qsb` 文件，被假设为可信内容。不要未经安全评估就允许用户上传任意 shader package 并调用 `fromSerialized()`。加载外部 shader 资产时，应限制来源、验证版本和大小，并结合平台图形驱动的安全模型评估风险。

## 6. 成员类型语义

### 6.1 `Source`

`Source` 描述 `QShaderCode` 中 `QByteArray` 的语言或字节码类型：

- `SpirvShader`：SPIR-V；
- `GlslShader`：GLSL；
- `HlslShader`：HLSL；
- `DxbcShader`：由 `fxc` 编译的 Direct3D 字节码；
- `MslShader`：Metal Shading Language；
- `DxilShader`：由 `dxc` 编译的 Direct3D 字节码；
- `MetalLibShader`：预编译 Metal 字节码；
- `WgslShader`：WebGPU Shading Language。

它描述代码内容，不自动验证 `QByteArray` 是否真的符合该类型。键、版本和实际字节码必须由生成工具保持一致。

### 6.2 `Stage`

`Stage` 描述 shader 适用的图形管线阶段：

- `VertexStage`：顶点；
- `TessellationControlStage`：细分控制，也称 hull；
- `TessellationEvaluationStage`：细分求值，也称 domain；
- `GeometryStage`：几何；
- `FragmentStage`：片段，也称 pixel；
- `ComputeStage`：计算。

它不是 `QShaderKey` 的一部分。把 fragment shader 设置成 `VertexStage` 不会自动转换代码，只会产生错误的 package 元数据。

### 6.3 `Variant`

`Variant` 用于同一管线阶段的特殊版本：

- `StandardShader`：普通、未修改的 shader；
- `BatchableVertexShader`：为 Qt Quick 场景图批处理重写的顶点 shader；
- `UInt16IndexedVertexAsComputeShader`：Metal 细分场景中，使用 `uint16` index buffer 的顶点 shader 计算变体；
- `UInt32IndexedVertexAsComputeShader`：Metal 细分场景中，使用 `uint32` index buffer 的顶点 shader 计算变体；
- `NonIndexedVertexAsComputeShader`：Metal 细分场景中，使用非索引 draw 的顶点 shader 计算变体；
- `HdrCapableFragmentShader`：Qt 6.10 起提供、为 Qt Quick HDR 渲染重写的片段 shader。

后面三个 Metal 变体不是“把任意顶点 shader 改成 compute shader”的通用工具，而是特定生成管线使用的预生成版本。

### 6.4 `SerializedFormatVersion`

该枚举控制 `serialized()` 的二进制格式目标：

- `Latest`：当前 Qt 版本，默认值；
- `Qt_6_5`：面向 Qt 6.5；
- `Qt_6_4`：面向 Qt 6.4。

只有确实需要旧 Qt 版本读取时才应选择旧格式。旧格式会牺牲较新版本引入的功能；反过来，针对旧版本生成的 asset 在新 Qt 中也可能缺少新功能所需的附加数据。

### 6.5 `NativeResourceBindingMap`

这是：

```cpp
using NativeResourceBindingMap = QMap<int, std::pair<int, int>>;
```

RHI 的资源绑定模型以 SPIR-V 为基础，uniform buffer、storage buffer、combined image sampler 和 storage image 共享一个 binding point 空间。该映射按 `QShaderKey` 保存通用 binding 到后端原生绑定信息的关系。

如果某个 key 不需要映射或没有可用映射，查询返回空 map。不要把空 map 解释成“所有绑定都确定无需调整”，而应结合目标后端和生成器的约定判断。

### 6.6 `SeparateToCombinedImageSamplerMappingList`

这是：

```cpp
using SeparateToCombinedImageSamplerMappingList =
    QList<SeparateToCombinedImageSamplerMapping>;
```

它描述某些后端把独立 texture 和 sampler 组合成 combined image sampler 时所需的映射。列表按 shader key 保存；不适用时返回空列表。结构体字段在 `QShader_SeparateToCombinedImageSamplerMapping_图像.md` 中单独展开。

### 6.7 `NativeShaderInfo`

`NativeShaderInfo` 为某个 shader key 保存后端附加信息，包括 `flags` 和 `extraBufferBindings`。没有对应数据时，`nativeShaderInfo()` 返回空对象。它是生成器和后端之间的附加协作数据，不应被当作通用 shader 反射替代品。

## 7. 实际使用场景

### 7.1 为 QRhi 提供跨后端 shader

使用 `qsb` 生成包含 SPIR-V、GLSL、HLSL、MSL、DXIL 或 WGSL 的 package，运行时根据 QRhi 后端选择合适 key。这是 `QShader` 最典型的用途。

### 7.2 从反射信息创建资源布局

当框架不知道 shader 的输入和 uniform block 布局时，可读取 `QShaderDescription`，再生成顶点输入和资源绑定。这样 shader 资产和管线配置可以减少手写重复信息，但仍需检查生成的布局是否符合后端要求。

### 7.3 为同一 shader 保存不同版本

OpenGL ES、桌面 GLSL、HLSL 和 WGSL 可能使用不同版本或入口约定。用 `QShaderVersion` 和 `QShaderKey` 区分这些版本，不要把版本号藏在字符串文件名中后再靠调用方猜测。

### 7.4 使用 Qt Quick 专用变体

Qt Quick 场景图批处理或 HDR 渲染可能需要 `BatchableVertexShader` 或 `HdrCapableFragmentShader`。这些变体应由 Qt 的 shader 工具链生成并按明确 key 查询，不应手工把标准 shader 标记成特殊变体。

### 7.5 运行时 shader 工具

编辑器、材质预览器或用户脚本工具可以调用 `QShaderBaker` 生成 `QShader`，然后通过 `serialized()` 导出。工具链应把编译错误、目标版本、后端列表和生成的反射信息一并展示给用户。

## 8. 生命周期、所有权和线程

### 8.1 纯值对象，不拥有 GPU shader module

`QShader` 不继承 `QObject`，不拥有窗口、RHI 或 GPU 资源。销毁一个 `QShader` 不会销毁已经由 QRhi 管线创建的底层 shader module，也不会通知任何渲染线程。

### 8.2 隐式共享不等于任意线程并发写

独立的 `QShader` 副本可以按值在工作线程之间传递。多个线程同时修改同一个实例仍然需要外部同步；更清晰的做法是在线程之间传递不可变副本，完成生成后再把结果交给渲染线程。

`QShader` 的值操作本身不要求 GUI 事件循环，但 QRhi 对象和图形资源有各自的线程和帧生命周期要求。不要因为 shader package 是值类型，就在任意线程直接修改或提交正在使用的 QRhi pipeline。

### 8.3 setter 触发分离

`setStage()`、`setDescription()`、`setShader()` 和各种附加映射 setter 会修改对象。由于隐式共享，它们会在必要时 detach。若多个大 package 共享同一底层数据，第一次修改可能产生分离和内存开销。

### 8.4 序列化数据的所有权

`serialized()` 返回自己的 `QByteArray` 值。读取文件时，`fromSerialized()` 会解析输入并建立 `QShader` 数据，不要求调用方长期保留原始文件缓冲区。

## 9. 查询、修改与删除的键语义

### 9.1 先构造精确 key

```cpp
QShaderKey key(QShader::SpirvShader,
               QShaderVersion(100),
               QShader::StandardShader);

QShaderCode code = shader.shader(key);
if (code.shader().isEmpty()) {
    // 该精确 key 没有代码。
}
```

默认构造的 `QShaderKey` 有自己的默认 source、version 和 variant；不要把它当成“匹配任意 shader”的通配符。

### 9.2 `availableShaders()` 不给出后端优先级

它返回可用 key 的列表，不定义应用应该优先选择哪一个，也不保证列表顺序是稳定的后端优先级。选择策略应由 QRhi 后端、版本兼容性和应用的 fallback 顺序决定。

### 9.3 删除只影响一个 key 的一类数据

`removeShader(key)` 只删除该 key 的代码；`removeResourceBindingMap(key)`、`removeSeparateToCombinedImageSamplerMappingList(key)` 和 `removeNativeShaderInfo(key)` 分别删除该 key 的对应附加数据。删除 shader code 不应被误解成自动删除其他附加映射。

如果最终 package 需要序列化，应在删除后重新检查 `availableShaders()`、反射和附加数据是否仍然相互一致。

## 10. 常见误区与排查顺序

### 10.1 把 `QShader` 当成编译器

`QShader` 只保存代码和元数据。输入一个 GLSL 字符串不会自动生成 SPIR-V、HLSL 或反射信息；使用 `qsb` 或 `QShaderBaker` 完成编译和转换。

### 10.2 直接依赖稳定 ABI

RHI API 没有源和二进制兼容保证。不要在插件 ABI、跨进程协议或独立 SDK 的公共头文件中暴露 `QShader`，也不要跨 Qt 小版本复用未经重新生成的私有对象假设。

### 10.3 只保存一份后端代码

某个后端能运行不代表其他后端也能运行。使用 `availableShaders()` 检查 package 是否包含目标 key，并为缺失代码提供明确错误或 fallback。

### 10.4 把 `QShaderKey` 的 `Source` 当成 shader 阶段

`Source` 是语言或字节码格式；`Stage` 才是 vertex、fragment、compute 等管线阶段。两者是不同维度，不能互换。

### 10.5 忽略入口点

`QShaderCode` 还包含 `entryPoint()`。某些语言和生成路径依赖入口点名称；只检查 `shader()` 非空而忽略入口点，可能导致后端创建失败。

### 10.6 用标准变体代替特殊变体

`BatchableVertexShader`、Metal compute 变体和 HDR 片段变体有特定生成语义。不要仅修改 `QShaderKey` 的 variant 字段来伪造它们。

### 10.7 旧序列化格式没有代价

使用 `Qt_6_4` 或 `Qt_6_5` 是为了旧 Qt 读取，会让新功能所需的数据无法写入或不可用。只有部署目标明确需要旧版本时才指定旧格式。

### 10.8 把反射信息当作最终验证

`QShaderDescription` 帮助发现资源和输入，但不保证你的顶点布局、资源绑定、纹理格式和渲染目标在具体后端一定匹配。仍需让 pipeline 创建和实际绘制通过验证。

### 10.9 加载不可信 `.qsb`

Qt 文档把 shader package 视为可信内容。不要把用户上传的任意 `.qsb` 当普通图片或文本处理；应在产品层面限制来源和能力。

### 10.10 用 `QShader` 替代窗口或 GPU 线程同步

它是 CPU 值对象，不是线程同步工具。更新 shader package 后，仍需由渲染线程按 QRhi 的资源替换和帧生命周期规则重新创建 pipeline。

## 11. 逐项 API 说明

### 成员类型

#### `enum QShader::Source`

标识 `QShaderCode` 中保存的源代码或字节码种类：

| 枚举值 | 数值 | 含义 |
| --- | ---: | --- |
| `SpirvShader` | `0` | SPIR-V |
| `GlslShader` | `1` | GLSL |
| `HlslShader` | `2` | HLSL |
| `DxbcShader` | `3` | `fxc` 生成的 Direct3D 字节码 |
| `MslShader` | `4` | Metal Shading Language |
| `DxilShader` | `5` | `dxc` 生成的 Direct3D 字节码 |
| `MetalLibShader` | `6` | 预编译 Metal 字节码 |
| `WgslShader` | `7` | WGSL |

#### `enum QShader::Stage`

标识 shader 所属管线阶段：

| 枚举值 | 数值 | 含义 |
| --- | ---: | --- |
| `VertexStage` | `0` | 顶点 shader |
| `TessellationControlStage` | `1` | 细分控制或 hull shader |
| `TessellationEvaluationStage` | `2` | 细分求值或 domain shader |
| `GeometryStage` | `3` | 几何 shader |
| `FragmentStage` | `4` | 片段或 pixel shader |
| `ComputeStage` | `5` | 计算 shader |

#### `enum QShader::Variant`

标识同一阶段的代码变体：

| 枚举值 | 数值 | 含义 |
| --- | ---: | --- |
| `StandardShader` | `0` | 普通未修改版本 |
| `BatchableVertexShader` | `1` | 适合 Qt Quick 场景图批处理的顶点版本 |
| `UInt16IndexedVertexAsComputeShader` | `2` | Metal 细分和 `uint16` 索引 draw 的顶点计算版本 |
| `UInt32IndexedVertexAsComputeShader` | `3` | Metal 细分和 `uint32` 索引 draw 的顶点计算版本 |
| `NonIndexedVertexAsComputeShader` | `4` | Metal 细分和非索引 draw 的顶点计算版本 |
| `HdrCapableFragmentShader` | `5` | Qt 6.10 起的 HDR 能力片段版本 |

#### `enum class QShader::SerializedFormatVersion`

指定序列化格式的目标 Qt 版本：

| 枚举值 | 数值 | 含义 |
| --- | ---: | --- |
| `SerializedFormatVersion::Latest` | `0` | 当前 Qt 版本，默认值 |
| `SerializedFormatVersion::Qt_6_5` | `1` | 面向 Qt 6.5 的格式 |
| `SerializedFormatVersion::Qt_6_4` | `2` | 面向 Qt 6.4 的格式 |

### 类型别名和结构

#### `[alias] QShader::NativeResourceBindingMap`

等价于 `QMap<int, std::pair<int, int>>`。它按 `QShaderKey` 保存通用 binding 到原生绑定数据的映射。空 map 表示该 key 没有可用映射或该映射不适用。

#### `[alias] QShader::SeparateToCombinedImageSamplerMappingList`

等价于 `QList<QShader::SeparateToCombinedImageSamplerMapping>`。它按 key 保存独立纹理和采样器合并时的附加映射，未提供时返回空列表。

#### `struct QShader::SeparateToCombinedImageSamplerMapping`

该结构体包含：

- `QByteArray combinedSamplerName`：组合后的 sampler 名称；
- `int textureBinding`：纹理绑定；
- `int samplerBinding`：采样器绑定。

它用于后端需要把 separate image 和 sampler 组合成一个资源时的映射，字段的实际使用取决于目标语言和生成器。

#### `struct QShader::NativeShaderInfo`

该结构体包含：

- `int flags`：后端附加标志；
- `QMap<int, int> extraBufferBindings`：额外 buffer 绑定。

没有对应 key 的信息时，`nativeShaderInfo()` 返回默认构造的空对象。

### 构造、赋值与共享

#### `QShader::QShader()`

默认构造一个 shader package。默认对象没有可用 shader 数据，通常 `isValid()` 为 `false`。需要使用前应通过反序列化、生成器或 setter 填充有效内容，并按实际流程验证。

#### `QShader::QShader(const QShader &other)`

复制一个 shader package。复制采用隐式共享，初始时可以共享底层数据；之后任一副本通过 setter 修改时会自动分离。

#### `[noexcept, since 6.7] QShader::QShader(QShader &&other)`

移动构造一个 shader package。它转移内部共享数据，适合从工厂、容器或函数返回值构造对象。移动后的 `other` 仍是有效的 C++ 对象，但不要依赖其中原有 shader 内容。

#### `QShader &QShader::operator=(const QShader &other)`

复制赋值 shader package。它遵循隐式共享值语义，赋值后两个对象逻辑上包含相同数据。

#### `[noexcept, since 6.7] QShader &QShader::operator=(QShader &&other)`

移动赋值 shader package。适合转移临时对象或工厂结果；移动后不要继续依赖源对象原有内容。

#### `[noexcept] QShader::~QShader()`

销毁值对象及其共享数据引用。它不会销毁 QRhi 中已经创建的 GPU shader 资源。

#### `[noexcept, since 6.7] void QShader::swap(QShader &other)`

交换两个 shader package 的内部数据。它不执行 shader 编译、不合并 package，也不改变两个对象之外的管线资源。

#### `void QShader::detach()`

强制当前对象与隐式共享存储分离。通常 setter 已经会隐式 detach，只有需要明确控制分离时才手动调用。该 API 属于有限兼容性的 RHI 接口，不应依赖其内部实现成本。

### 有效性与阶段

#### `bool QShader::isValid() const`

判断 shader package 是否有效。反序列化失败时，`fromSerialized()` 返回的默认对象会使它返回 `false`。它是 package 层面的快速检查，不替代具体后端 pipeline 创建验证。

#### `QShader::Stage QShader::stage() const`

返回 package 的管线阶段。它应与 shader code 和生成器的实际阶段一致。

#### `void QShader::setStage(QShader::Stage stage)`

设置 package 的管线阶段。它只修改元数据，不把 shader 代码转换到另一个阶段，也不会验证代码内容是否真的符合新阶段。

### 反射描述

#### `QShaderDescription QShader::description() const`

返回 shader 的反射元数据，包含输入、输出、uniform block 等资源描述。返回的是值对象副本，适合读取和传递给布局生成逻辑。

#### `void QShader::setDescription(const QShaderDescription &desc)`

设置 shader 的反射元数据。调用方负责确保描述与实际 shader 代码一致；Qt 不会根据 `desc` 自动修改或重新编译代码。

### shader 代码查询与修改

#### `QList<QShaderKey> QShader::availableShaders() const`

返回 package 中可用 shader 版本的 key 列表。列表只说明哪些精确 key 存在，不提供后端优先级，也不保证顺序可用于持久化协议。

#### `QShaderCode QShader::shader(const QShaderKey &key) const`

返回指定 key 的 shader code。key 不存在或对应代码为空时，返回的 `QShaderCode::shader()` 为空。查询不会自动选择相近版本、语言或变体。

#### `void QShader::setShader(const QShaderKey &key, const QShaderCode &shader)`

按 key 写入或替换 shader code。它只修改指定 key 的代码条目，不自动生成其他后端版本，不自动更新反射描述，也不自动调整附加映射。

#### `void QShader::removeShader(const QShaderKey &key)`

删除指定 key 的 shader code。它不会自动删除该 key 的资源绑定映射、组合 sampler 映射或 native shader info；删除后如需保持 package 完整，应分别清理不再需要的附加数据。

### 序列化

#### `QByteArray QShader::serialized(QShader::SerializedFormatVersion version = SerializedFormatVersion::Latest) const`

把 package 中的全部数据序列化为二进制 `QByteArray`，适合写入文件或其他 I/O 设备。默认使用当前 Qt 的 `Latest` 格式。

指定旧版本格式只适合明确需要旧 Qt 读取的部署场景；旧格式可能丢失新版本功能所需的数据。序列化结果应当与目标 Qt 版本、shader 生成工具和部署资产一起测试。

#### `[static] QShader QShader::fromSerialized(const QByteArray &data)`

从二进制数据反序列化 shader package。数据解析失败时返回默认构造的 `QShader`，其 `isValid()` 为 `false`。输入 package 被 Qt 文档视为可信内容，不能无审查加载不可信用户数据。

### 原生资源绑定和附加信息

#### `QShader::NativeResourceBindingMap QShader::nativeResourceBindingMap(const QShaderKey &key) const`

返回指定 key 的原生资源绑定映射。没有映射，或该语言和后端不适用时返回空 map。它是按 key 存储的附加信息，不能跨 key 盲目复用。

#### `void QShader::setResourceBindingMap(const QShaderKey &key, const QShader::NativeResourceBindingMap &map)`

设置指定 key 的原生资源绑定映射。调用方应使用生成器或目标后端约定的 binding 数据，不能只根据整数编号自行猜测 pair 中两个值的含义。

#### `void QShader::removeResourceBindingMap(const QShaderKey &key)`

删除指定 key 的原生资源绑定映射。它只影响 binding map，不删除 shader code 或其他 native 附加信息。

#### `QShader::SeparateToCombinedImageSamplerMappingList QShader::separateToCombinedImageSamplerMappingList(const QShaderKey &key) const`

返回指定 key 的独立 texture/sampler 到 combined sampler 的映射列表。该语言或后端不需要映射时返回空列表。

#### `void QShader::setSeparateToCombinedImageSamplerMappingList(const QShaderKey &key, const QShader::SeparateToCombinedImageSamplerMappingList &list)`

设置指定 key 的 combined image sampler 映射列表。列表内容应与该 key 的代码和资源布局一致，Qt 不会自动从 shader 文本推断或修正它。

#### `void QShader::removeSeparateToCombinedImageSamplerMappingList(const QShaderKey &key)`

删除指定 key 的 combined image sampler 映射列表。不会删除 shader code 或 binding map。

#### `QShader::NativeShaderInfo QShader::nativeShaderInfo(const QShaderKey &key) const`

返回指定 key 的原生 shader 附加信息。没有数据或该后端、语言、阶段不适用时返回默认空对象。

#### `void QShader::setNativeShaderInfo(const QShaderKey &key, const QShader::NativeShaderInfo &info)`

设置指定 key 的原生 shader 附加信息，包括 flags 和额外 buffer 绑定。应使用生成器和后端约定的值，避免手工构造不一致的元数据。

#### `void QShader::removeNativeShaderInfo(const QShaderKey &key)`

删除指定 key 的原生 shader 附加信息。它不影响 shader code、反射描述或其他类型的映射。

### 相关非成员

#### `[noexcept] bool operator==(const QShader &lhs, const QShader &rhs)`

比较两个 `QShader` 是否相等。Qt 文档将其定义为两个对象属于同一阶段，并且具有匹配的 shader 源代码或二进制代码集合。不要把相等判断当作 GPU 资源兼容性或 pipeline 可创建性的证明。

#### `[noexcept] bool operator!=(const QShader &lhs, const QShader &rhs)`

返回 `operator==` 的反值。它是头文件中的便捷内联运算符。

#### `[noexcept] size_t qHash(const QShader &key, size_t seed = 0)`

为 `QShader` 提供哈希值，可用于 `QHash` 和 `QSet`。哈希适合进程内容器索引，不应被当作稳定的文件 ID、跨进程指纹或安全校验值。

## API 速查表

| 类别 | API | 作用 | 关键边界 |
| --- | --- | --- | --- |
| 枚举 | `enum Source` | 标识 shader 源代码或字节码格式 | 不会验证 `QByteArray` 真的是该格式 |
| 枚举 | `enum Stage` | 标识 vertex、fragment、compute 等管线阶段 | 不属于 key；设置阶段不会转换代码 |
| 枚举 | `enum Variant` | 标识标准、批处理、Metal 特殊或 HDR 变体 | 不能只改 key 字段伪造特殊变体 |
| 枚举 | `SerializedFormatVersion` | 指定序列化目标 Qt 版本 | 旧格式会牺牲新功能数据 |
| 别名 | `NativeResourceBindingMap` | `QMap<int, std::pair<int, int>>` 的原生绑定映射 | 按 key 存储；空 map 表示没有适用映射 |
| 别名 | `SeparateToCombinedImageSamplerMappingList` | combined sampler 映射结构体列表 | 按 key 存储；不适用时为空 |
| 结构体 | `SeparateToCombinedImageSamplerMapping` | 保存组合 sampler 名称和 texture/sampler binding | 必须与对应代码和生成器约定一致 |
| 结构体 | `NativeShaderInfo` | 保存 flags 和额外 buffer bindings | 没有数据时查询返回空对象 |
| 构造 | `QShader()` | 创建默认 shader package | 默认对象通常无有效 shader；应检查 `isValid()` |
| 构造 | `QShader(const QShader &other)` | 复制 shader package | 隐式共享；后续写入会分离 |
| 构造 | `QShader(QShader &&other)` | 移动构造 shader package | since 6.7；移动后不要依赖源对象内容 |
| 生命周期 | `~QShader()` | 销毁值对象 | 不会销毁 QRhi 已创建的 GPU shader 资源 |
| 赋值 | `operator=(const QShader &other)` | 复制赋值 | 保持值语义和隐式共享 |
| 赋值 | `operator=(QShader &&other)` | 移动赋值 | since 6.7；源对象内容不再可依赖 |
| 工具 | `swap(QShader &other)` | 交换两个 package | 不编译、不合并、不改变 GPU pipeline |
| 工具 | `detach()` | 强制与共享存储分离 | setter 通常已隐式 detach；一般不需手动调用 |
| 状态 | `isValid() const` | 判断 package 是否有效 | 不能替代具体后端 pipeline 验证 |
| 阶段 | `stage() const` | 读取管线阶段 | 应与实际 shader 代码阶段一致 |
| 阶段 | `setStage(Stage stage)` | 设置管线阶段元数据 | 不会把代码转换到新阶段 |
| 反射 | `description() const` | 获取输入、输出和资源反射描述 | 反射不等于后端 pipeline 验证 |
| 反射 | `setDescription(const QShaderDescription &desc)` | 设置反射描述 | 不会自动修改或编译 shader code |
| 查询 | `availableShaders() const` | 获取所有可用 `QShaderKey` | 不提供优先级，不应依赖列表顺序 |
| 查询 | `shader(const QShaderKey &key) const` | 按精确 key 获取代码 | 缺失 key 时返回空 code，不自动 fallback |
| 写入 | `setShader(const QShaderKey &, const QShaderCode &)` | 写入或替换一个代码条目 | 不自动生成其他语言或更新反射 |
| 删除 | `removeShader(const QShaderKey &)` | 删除一个 key 的代码 | 不自动删除该 key 的其他附加信息 |
| 序列化 | `serialized(SerializedFormatVersion version = Latest) const` | 导出全部 package 数据 | 默认当前版本；外部加载资产要考虑可信性 |
| 反序列化 | `fromSerialized(const QByteArray &data)` | 从二进制恢复 package | 失败返回无效默认对象 |
| 绑定 | `nativeResourceBindingMap(const QShaderKey &) const` | 查询原生资源 binding 映射 | 不适用时为空，不能跨 key 复用 |
| 绑定 | `setResourceBindingMap(const QShaderKey &, const NativeResourceBindingMap &)` | 写入原生 binding 映射 | pair 含义由后端/生成器约定 |
| 删除 | `removeResourceBindingMap(const QShaderKey &)` | 删除一个 key 的 binding map | 不影响 code、反射和其他映射 |
| sampler | `separateToCombinedImageSamplerMappingList(const QShaderKey &) const` | 查询 separate 到 combined sampler 映射 | 不适用时为空 |
| sampler | `setSeparateToCombinedImageSamplerMappingList(const QShaderKey &, const SeparateToCombinedImageSamplerMappingList &)` | 写入 sampler 合并映射 | 必须与该 key 的资源布局一致 |
| 删除 | `removeSeparateToCombinedImageSamplerMappingList(const QShaderKey &)` | 删除一个 key 的 sampler 映射 | 不影响其他附加数据 |
| 原生信息 | `nativeShaderInfo(const QShaderKey &) const` | 查询后端附加 shader 信息 | 无数据时返回空对象 |
| 原生信息 | `setNativeShaderInfo(const QShaderKey &, const NativeShaderInfo &)` | 写入 flags 和额外 buffer 绑定 | 应使用生成器/后端约定值 |
| 删除 | `removeNativeShaderInfo(const QShaderKey &)` | 删除一个 key 的原生附加信息 | 不影响 shader code 和反射 |
| 比较 | `operator==(const QShader &, const QShader &)` | 比较阶段和 shader code 集合 | 相等不表示 GPU pipeline 一定兼容 |
| 比较 | `operator!=(const QShader &, const QShader &)` | `operator==` 的反值 | 仍是值对象比较，不是 GPU 状态比较 |
| 哈希 | `qHash(const QShader &, size_t seed = 0)` | 用作 `QHash`/`QSet` 的 key | 不应当作稳定文件 ID 或安全指纹 |
| 工具链 | `qsb` | 构建时生成多后端 shader package | 推荐用于生产资产；与 Qt 版本和目标后端一起测试 |
| 工具链 | `QShaderBaker` | 运行时或工具中生成 QShader | 编译开销高，适合动态 shader 场景 |
| RHI | `QRhiGraphicsPipeline::setVertexShader()` | 为图形管线设置顶点 shader | 仍需配置顶点输入、资源和渲染目标 |
| RHI | `QRhiGraphicsPipeline::setFragmentShader()` | 为图形管线设置片段 shader | shader package 不等于已创建的 GPU 资源 |

---

### 一句话总结

`QShader` 是一个按 `QShaderKey` 保存多后端代码、反射描述和原生附加映射的隐式共享值类型：生产环境通常用 `qsb` 生成并通过 `fromSerialized()` 加载，运行时用 `availableShaders()` 和精确 key 选择代码；使用时要同时尊重 RHI 的有限兼容性、旧序列化格式的功能代价以及外部 shader package 的可信边界。
