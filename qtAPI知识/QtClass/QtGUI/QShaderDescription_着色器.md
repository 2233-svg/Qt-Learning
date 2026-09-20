# Qt QShaderDescription：着色器反射布局与资源元数据

> 适用版本：Qt 6.11.1  
> 头文件：`#include <rhi/qshaderdescription.h>`  
> 所属模块：`Qt6::Gui`，使用 RHI 相关能力时通常还要链接 `Qt6::GuiPrivate`  
> 继承：无  
> 类型定位：RHI 着色器反射描述的隐式共享值类型

## 1. 它解决什么问题

着色器源码或字节码只告诉 GPU 如何执行计算，并不方便应用直接回答这些问题：

- 顶点 shader 需要哪些输入变量，它们的 location 和类型是什么？
- fragment shader 输出了哪些变量？
- uniform block、storage block、push constant 的名字、binding、大小和成员偏移是什么？
- 某个资源是 combined sampler、独立 image、独立 sampler 还是 storage image？
- compute shader 的 `local_size_x/y/z` 是多少？
- tessellation shader 使用三角形、四边形还是 isoline，细分间距和绕序是什么？

`QShaderDescription` 就是这层“编译后反射信息”。`QShaderBaker` 或 `qsb` 生成 `QShader` 时会把描述放进 shader package，运行时由 `QShader::description()` 取出。它适合用来生成或校验顶点输入布局、资源绑定布局和部分管线配置。

它不是：

- shader 编译器；
- GPU 上的 descriptor set、uniform buffer 或 pipeline 对象；
- 可以凭空修改 shader 资源布局的编辑器；
- 对所有图形后端都保证完全一致的高层抽象。

反射结果描述的是生成器看到的 shader 接口。应用仍然要把它和 QRhi 的资源绑定、顶点输入、渲染目标格式及实际后端限制结合起来验证。

## 2. 兼容性、包含与构建

### 2.1 RHI API 的兼容性边界

`QShaderDescription` 位于 RHI 相关头文件中。Qt 对这组 API 的源代码和二进制兼容性保证有限，升级 Qt 小版本时也不应假设头文件布局、枚举数值以外的实现细节或序列化私有细节永远不变。

建议把依赖 `QShaderDescription` 的代码集中在渲染适配层，并与生成 shader package 所用的 Qt 版本一起测试。不要把它作为跨 Qt 版本插件 ABI 或跨进程协议的公共数据结构。

### 2.2 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui GuiPrivate)
target_link_libraries(mytarget PRIVATE Qt6::Gui Qt6::GuiPrivate)
```

```cpp
#include <rhi/qshaderdescription.h>
```

普通应用通常不直接构造反射记录，而是：

```cpp
QShader shader = QShader::fromSerialized(data);
if (!shader.isValid())
    return;

const QShaderDescription desc = shader.description();
```

`QShaderDescription` 是值类型，复制它不会复制 GPU 资源，也不会重新编译 shader。

## 3. 最小使用场景

下面的示例从 `QShader` 中读取顶点输入和 uniform block，展示最常见的消费方式：

```cpp
#include <QShader>
#include <QShaderDescription>
#include <QDebug>

void inspectShader(const QShader &shader)
{
    if (!shader.isValid())
        return;

    const QShaderDescription desc = shader.description();
    if (!desc.isValid())
        return;

    for (const auto &input : desc.inputVariables()) {
        qDebug() << input.name
                 << "type =" << input.type
                 << "location =" << input.location;
    }

    for (const auto &block : desc.uniformBlocks()) {
        qDebug() << "uniform block =" << block.blockName
                 << "binding =" << block.binding
                 << "set =" << block.descriptorSet
                 << "size =" << block.size;

        for (const auto &member : block.members)
            qDebug() << "  member =" << member.name
                     << "offset =" << member.offset
                     << "size =" << member.size;
    }
}
```

这里的 `offset`、`size` 和 `arrayStride` 是 shader 数据布局信息，不是 C++ 结构体的 `offsetof()` 结果。若 CPU 侧要填充 uniform buffer，应按照 shader 使用的布局规则和反射结果计算，并处理对齐与填充。

## 4. 核心使用模型

### 4.1 把它当成“只读反射快照”

普通应用最常见的流程是：

```text
qsb / QShaderBaker
    -> QShader package
    -> QShader::description()
    -> QShaderDescription
    -> 读取输入、资源和布局
    -> 创建 QRhi pipeline / resource bindings
```

类本身没有 `setInputVariables()`、`setUniformBlocks()` 之类的公开 setter。它主要是 Qt shader 工具链产生、应用读取的描述对象。公开的 `detach()` 只处理隐式共享存储的分离，不等于获得一个可通过普通公开属性编辑的 builder。

### 4.2 所有位置和 binding 都要按“可能缺失”处理

`InOutVariable` 的 `location`、`binding` 和 `descriptorSet` 默认是 `-1`。这通常表示 shader 或目标格式没有提供该装饰信息，不表示合法的 GPU binding 是负数。

同样，结构体字段中有一些可选反射信息默认是 `0`，例如：

- `BlockVariable::size`；
- `BlockVariable::arrayStride`；
- `BlockVariable::matrixStride`；
- `UniformBlock::size`；
- `StorageBlock::knownSize`；
- `StorageBlock::runtimeArrayStride`。

因此不能把 `0` 一概当作“空数据”或“一个字节”。对运行时数组尤其要区分：

- `arrayDims` 中的 `0` 可表示运行时数组维度；
- 运行时数组本身没有固定总大小，相关 `size` 可能为 `0`；
- `runtimeArrayStride` 表示相邻运行时数组元素的步长；
- `knownSize` 只覆盖运行时数组之前能够确定的部分。

### 4.3 反射记录按用途分组

可以把返回值分成几组：

| 分组 | 查询 API | 描述内容 |
| --- | --- | --- |
| stage interface | `inputVariables()`、`outputVariables()` | 普通输入/输出变量 |
| builtin interface | `inputBuiltinVariables()`、`outputBuiltinVariables()` | `gl_Position`、`gl_VertexID` 等内建变量 |
| buffer blocks | `uniformBlocks()`、`storageBlocks()`、`pushConstantBlocks()` | 缓冲区资源及成员布局 |
| image/sampler | `combinedImageSamplers()`、`separateImages()`、`separateSamplers()`、`storageImages()` | 纹理、采样器和 image 资源 |
| stage execution | `computeShaderLocalSize()`、tessellation 系列 API | 计算或细分阶段执行参数 |

同一个变量可能在不同后端生成路径中表现为不同的资源分类。应用不应只看变量名猜类型，应同时读取 `VariableType`、binding、descriptor set、image flags 和 image format。

### 4.4 结构体需要递归读取

`BlockVariable::structMembers` 和 `InOutVariable::structMembers` 都是嵌套成员列表。只有当 `type == Struct` 时，递归读取这些字段才有通常意义；对非结构体变量，列表通常为空。

数组和矩阵也不能只看顶层 `type`：

- `arrayDims` 给出数组维度；
- `arrayStride` 给出数组元素步长；
- `matrixStride` 给出矩阵列或行之间的步长；
- `matrixIsRowMajor` 说明矩阵的主序；
- `size` 是该层级可知的数据占用大小，运行时数组可能为 `0`。

## 5. 实际使用场景

### 5.1 从 shader 反射生成顶点输入

遍历 `inputVariables()`，按 `location` 和 `type` 建立 `QRhiVertexInputAttribute`。这是减少“shader 改了 location，但 C++ 仍使用旧编号”问题的一种方式。

反射结果仍不能替你决定 CPU 顶点缓冲的步长、绑定槽和数据是否真的按 shader 期望编码。对于矩阵、整数属性和归一化格式，要把 `VariableType` 映射到正确的 QRhi vertex attribute format。

### 5.2 生成 uniform buffer 的写入布局

读取 `uniformBlocks()` 后，可按 `members` 中的 `offset`、`size`、数组步长和矩阵步长填充 CPU 侧缓冲区。嵌套 `Struct` 必须递归计算字段地址。

不要按 C++ `struct` 的自然布局直接 `memcpy`，因为 GLSL/HLSL/MSL 的布局、对齐和矩阵主序可能不同。

### 5.3 检查资源绑定

读取 `uniformBlocks()`、`storageBlocks()` 和四类 image/sampler 列表，可以在创建 QRhi 资源绑定前检查：

- binding 是否存在；
- descriptor set 是否匹配；
- sampler 和 image 是否被拆分；
- storage image 是否要求读或写；
- image format 是否需要特定的存储格式。

`QShaderDescription` 只告诉你 shader 端的声明，不能保证运行时的 `QRhiTexture`、`QRhiSampler` 或 buffer 能力满足要求。

### 5.4 处理 compute shader

`computeShaderLocalSize()` 返回 shader 声明的 local workgroup size。它是每个 workgroup 的线程维度，不是整个 dispatch 的工作总量。调用 `QRhiCommandBuffer::dispatch()` 时，x、y、z 的 group 数仍由应用根据实际数据量计算。

返回值是 `std::array<uint, 3>`，默认数组为 `{0, 0, 0}`。零值表示没有可用的反射 local size，不应拿来作为实际 dispatch 的除数或合法工作组尺寸。

### 5.5 处理 tessellation shader

细分阶段可以读取：

- `tessellationMode()`：triangles、quads 或 isolines；
- `tessellationPartitioning()`：equal、fractional even 或 fractional odd；
- `tessellationWindingOrder()`：clockwise 或 counter-clockwise；
- `tessellationOutputVertexCount()`：细分控制阶段声明的输出顶点数。

这些值只描述 shader 的接口声明。是否能在目标 QRhi 后端启用 tessellation，还要检查后端能力和 pipeline 配置。

## 6. 成员类型

### 6.1 `VariableType`

`VariableType` 描述反射变量的基础类型、向量、矩阵、采样器、image、结构体或 half 类型。枚举顺序被头文件注释标记为不能重排；应用应使用枚举名而不是自行假设连续数值。

| 枚举值 | 含义 |
| --- | --- |
| `Unknown` | 未知或未提供类型 |
| `Float`、`Vec2`、`Vec3`、`Vec4` | `float` 及其向量 |
| `Mat2`、`Mat2x3`、`Mat2x4`、`Mat3`、`Mat3x2`、`Mat3x4`、`Mat4`、`Mat4x2`、`Mat4x3` | `float` 矩阵，命名中的列/行维度遵循 shader 工具链约定 |
| `Int`、`Int2`、`Int3`、`Int4` | `int` 及其向量 |
| `Uint`、`Uint2`、`Uint3`、`Uint4` | `uint` 及其向量 |
| `Bool`、`Bool2`、`Bool3`、`Bool4` | `bool` 及其向量 |
| `Double`、`Double2`、`Double3`、`Double4` | `double` 及其向量 |
| `DMat2`、`DMat2x3`、`DMat2x4`、`DMat3`、`DMat3x2`、`DMat3x4`、`DMat4`、`DMat4x2`、`DMat4x3` | `double` 矩阵 |
| `Sampler1D`、`Sampler2D`、`Sampler2DMS`、`Sampler3D`、`SamplerCube` | 基本 sampler 类型 |
| `Sampler1DArray`、`Sampler2DArray`、`Sampler2DMSArray`、`Sampler3DArray`、`SamplerCubeArray` | 数组或多层 sampler 类型 |
| `SamplerRect`、`SamplerBuffer`、`SamplerExternalOES`、`Sampler` | 矩形、buffer、外部 OES 和通用 sampler 类型 |
| `Image1D`、`Image2D`、`Image2DMS`、`Image3D`、`ImageCube` | 基本 image 类型 |
| `Image1DArray`、`Image2DArray`、`Image2DMSArray`、`Image3DArray`、`ImageCubeArray` | 数组或多层 image 类型 |
| `ImageRect`、`ImageBuffer` | 矩形和 buffer image 类型 |
| `Struct` | 结构体；详细字段在 `structMembers` 中 |
| `Half`、`Half2`、`Half3`、`Half4` | half 及其向量 |

这些类型只描述 shader 反射视角。比如 `Sampler2D` 不会直接告诉你应用必须创建哪一个具体的 `QRhiTexture` 格式；storage image 的格式还要结合 `ImageFormat`。

### 6.2 `ImageFormat`

`ImageFormat` 的数值与 SPIR-V 的 image format 对齐。它用于描述 storage image 的格式要求；普通 sampler 通常使用 `ImageFormatUnknown`。

| 枚举值 | 含义 |
| --- | --- |
| `ImageFormatUnknown` | 未知、未提供或不适用 |
| `ImageFormatRgba32f`、`ImageFormatRgba16f`、`ImageFormatR32f` | 浮点 RGBA、浮点 RGBA16、单通道 float |
| `ImageFormatRgba8`、`ImageFormatRgba8Snorm`、`ImageFormatRg8`、`ImageFormatR8` | 常规无符号或归一化 8 位格式 |
| `ImageFormatRg32f`、`ImageFormatRg16f`、`ImageFormatR11fG11fB10f`、`ImageFormatR16f` | 浮点双通道、特殊打包和单通道格式 |
| `ImageFormatRgba16`、`ImageFormatRgb10A2`、`ImageFormatRg16`、`ImageFormatR16` | 16 位和打包无符号格式 |
| `ImageFormatRgba16Snorm`、`ImageFormatRg16Snorm`、`ImageFormatRg8Snorm`、`ImageFormatR16Snorm`、`ImageFormatR8Snorm` | signed normalized 格式 |
| `ImageFormatRgba32i`、`ImageFormatRgba16i`、`ImageFormatRgba8i`、`ImageFormatR32i` | 有符号整数格式 |
| `ImageFormatRg32i`、`ImageFormatRg16i`、`ImageFormatRg8i`、`ImageFormatR16i`、`ImageFormatR8i` | 有符号整数双通道和单通道格式 |
| `ImageFormatRgba32ui`、`ImageFormatRgba16ui`、`ImageFormatRgba8ui`、`ImageFormatR32ui` | 无符号整数格式 |
| `ImageFormatRgb10a2ui`、`ImageFormatRg32ui`、`ImageFormatRg16ui`、`ImageFormatRg8ui`、`ImageFormatR16ui`、`ImageFormatR8ui` | 打包及无符号整数双通道、单通道格式 |

`ImageFormat` 只描述 shader 声明的 image format，不负责把它转换成 `QRhiTexture::Format`，也不保证所有 QRhi 后端支持每一种格式。

### 6.3 `ImageFlag` 和 `ImageFlags`

```cpp
enum ImageFlag {
    ReadOnlyImage = 1 << 0,
    WriteOnlyImage = 1 << 1
};
Q_DECLARE_FLAGS(ImageFlags, ImageFlag)
```

这是 flags 类型，不是互斥枚举。一个变量可以有多个 flag：

- `ReadOnlyImage`：shader 只读 image；
- `WriteOnlyImage`：shader 只写 image；
- 两者同时存在时，表示声明允许读写，实际含义仍需结合生成器和 shader 语言规则判断；
- 没有 flag 时，不能臆测为读写或只读。

### 6.4 `QualifierFlag` 和 `QualifierFlags`

```cpp
enum QualifierFlag {
    QualifierReadOnly = 1 << 0,
    QualifierWriteOnly = 1 << 1,
    QualifierCoherent = 1 << 2,
    QualifierVolatile = 1 << 3,
    QualifierRestrict = 1 << 4
};
Q_DECLARE_FLAGS(QualifierFlags, QualifierFlag)
```

这些 flags 位于 `StorageBlock::qualifierFlags`，描述 storage block 的 shader 限定符：

- `QualifierReadOnly`；
- `QualifierWriteOnly`；
- `QualifierCoherent`；
- `QualifierVolatile`；
- `QualifierRestrict`。

它们是声明元数据，不会自动替应用选择同步方式、内存屏障或 buffer 使用标志。

### 6.5 `BlockVariable`

```cpp
struct BlockVariable {
    QByteArray name;
    VariableType type = Unknown;
    int offset = 0;
    int size = 0;
    QList<int> arrayDims;
    int arrayStride = 0;
    int matrixStride = 0;
    bool matrixIsRowMajor = false;
    QList<BlockVariable> structMembers;
};
```

字段语义：

| 字段 | 作用 | 边界 |
| --- | --- | --- |
| `name` | 成员名 | 是 shader 侧名称，不是 C++ 字段名 |
| `type` | 成员类型 | `Struct` 时继续读取 `structMembers` |
| `offset` | 相对于所属 block 或 struct 起点的偏移 | 是 shader 布局偏移，不是 C++ `offsetof()` |
| `size` | 当前成员可知的占用大小 | 运行时数组等未知大小可能为 `0` |
| `arrayDims` | 数组各维长度 | `0` 可用于表示运行时数组维度 |
| `arrayStride` | 数组相邻元素步长 | 非数组或未提供时可能为 `0` |
| `matrixStride` | 矩阵行/列之间步长 | 需要结合主序和类型解释 |
| `matrixIsRowMajor` | 是否按 row-major 描述 | `false` 表示非 row-major，通常是 column-major |
| `structMembers` | 嵌套结构体成员 | 需要递归遍历 |

### 6.6 `InOutVariable`

```cpp
struct InOutVariable {
    QByteArray name;
    VariableType type = Unknown;
    int location = -1;
    int binding = -1;
    int descriptorSet = -1;
    ImageFormat imageFormat = ImageFormatUnknown;
    ImageFlags imageFlags;
    QList<int> arrayDims;
    bool perPatch = false;
    QList<BlockVariable> structMembers;
};
```

字段语义：

- `name`：普通输入/输出或 image/sampler 的 shader 名称；
- `type`：输入/输出类型或资源类型；
- `location`：stage interface location；没有 location 装饰或该资源不使用 location 时为 `-1`；
- `binding`：资源 binding；普通 stage input 往往不使用它，因此可能为 `-1`；
- `descriptorSet`：资源所在 descriptor set；未提供时为 `-1`；
- `imageFormat`：storage image 的格式，非 image 资源通常是 `ImageFormatUnknown`；
- `imageFlags`：storage image 的读写 flag；
- `arrayDims`：输入/输出或资源数组维度，运行时数组维度可能是 `0`；
- `perPatch`：tessellation 中该变量是否按 patch 传递；
- `structMembers`：当输入/输出变量是结构体时的成员列表。

不要把 `location`、`binding` 和 `descriptorSet` 混成同一个编号空间。location 是 stage interface，binding/set 是资源绑定。

### 6.7 `UniformBlock`

```cpp
struct UniformBlock {
    QByteArray blockName;
    QByteArray structName;
    int size = 0;
    int binding = -1;
    int descriptorSet = -1;
    QList<BlockVariable> members;
};
```

- `blockName`：shader 中 block 的名称；
- `structName`：头文件注释标为 instance name，实际表示实例名称相关字段；
- `size`：整个 uniform block 的已知大小；
- `binding`：uniform buffer binding；
- `descriptorSet`：descriptor set；
- `members`：block 成员及布局。

`size` 是 shader block 的布局大小，不应直接等价为 C++ `sizeof`。当成员有矩阵、数组或嵌套 struct 时，必须使用成员偏移和 stride。

### 6.8 `PushConstantBlock`

```cpp
struct PushConstantBlock {
    QByteArray name;
    int size = 0;
    QList<BlockVariable> members;
};
```

push constant 没有 `binding` 或 `descriptorSet` 字段，因为它是 shader 阶段可见的特殊小块。`name`、`size` 和 `members` 描述其名称、布局大小及成员。

Qt 文档对 QRhi 的 push constant 支持有明确限制：不能因为反射中存在 `pushConstantBlocks()` 就假设 QRhi 一定提供对应运行时上传 API。跨后端应用通常需要采用 uniform buffer 等可移植方案，或确认目标 Qt/RHI 版本和具体后端的支持状态。

### 6.9 `StorageBlock`

```cpp
struct StorageBlock {
    QByteArray blockName;
    QByteArray instanceName;
    int knownSize = 0;
    int binding = -1;
    int descriptorSet = -1;
    QList<BlockVariable> members;
    int runtimeArrayStride = 0;
    QualifierFlags qualifierFlags;
};
```

- `blockName`：storage block 名称；
- `instanceName`：block 实例名称；
- `knownSize`：不包含无法预先确定的运行时数组部分的已知大小；
- `binding`、`descriptorSet`：资源绑定位置；
- `members`：成员布局；
- `runtimeArrayStride`：运行时数组的元素步长；
- `qualifierFlags`：read-only、coherent 等 shader 限定符。

典型的 unsized SSBO 成员可以表现为：

```text
members[n].arrayDims == [0]
members[n].size == 0
storageBlock.runtimeArrayStride > 0
```

这不是错误，而是“前缀布局已知，尾部数组大小由实际 buffer 决定”的反射结果。

### 6.10 `BuiltinType` 和 `BuiltinVariable`

`BuiltinType` 的数值与 SPIR-V builtin 对齐。它描述的是内建变量的语义，不是普通用户变量的 location。

| 枚举值 | 典型 shader 内建语义 |
| --- | --- |
| `PositionBuiltin` | 顶点位置，如 `gl_Position` |
| `PointSizeBuiltin` | 点大小 |
| `ClipDistanceBuiltin`、`CullDistanceBuiltin` | 裁剪距离和剔除距离 |
| `VertexIdBuiltin`、`InstanceIdBuiltin` | 顶点和实例 ID |
| `PrimitiveIdBuiltin`、`InvocationIdBuiltin` | 图元和 invocation ID |
| `LayerBuiltin`、`ViewportIndexBuiltin` | layer 和 viewport index |
| `TessLevelOuterBuiltin`、`TessLevelInnerBuiltin` | tessellation 外侧和内侧级别 |
| `TessCoordBuiltin`、`PatchVerticesBuiltin` | tessellation 坐标和 patch 顶点数 |
| `FragCoordBuiltin`、`PointCoordBuiltin` | fragment 和 point 坐标 |
| `FrontFacingBuiltin` | 正面判断 |
| `SampleIdBuiltin`、`SamplePositionBuiltin`、`SampleMaskBuiltin` | 多重采样信息 |
| `FragDepthBuiltin` | fragment 深度 |
| `NumWorkGroupsBuiltin`、`WorkgroupSizeBuiltin` | compute 工作组总数和尺寸 |
| `WorkgroupIdBuiltin`、`LocalInvocationIdBuiltin`、`GlobalInvocationIdBuiltin` | compute 工作组和 invocation ID |
| `LocalInvocationIndexBuiltin` | compute 本地线性索引 |
| `VertexIndexBuiltin`、`InstanceIndexBuiltin` | vertex/instance index |
| `ViewIndexBuiltin` | view index |

```cpp
struct BuiltinVariable {
    BuiltinType type;
    VariableType varType;
    QList<int> arrayDims;
};
```

`type` 是 builtin 语义，`varType` 是它的实际变量类型，`arrayDims` 表示数组维度。builtin 变量没有普通 `location` 字段，应用应按 builtin 语义使用。

### 6.11 tessellation 枚举

```cpp
enum TessellationMode {
    UnknownTessellationMode,
    TrianglesTessellationMode,
    QuadTessellationMode,
    IsolineTessellationMode
};

enum TessellationWindingOrder {
    UnknownTessellationWindingOrder,
    CwTessellationWindingOrder,
    CcwTessellationWindingOrder
};

enum TessellationPartitioning {
    UnknownTessellationPartitioning,
    EqualTessellationPartitioning,
    FractionalEvenTessellationPartitioning,
    FractionalOddTessellationPartitioning
};
```

`Unknown...` 是“没有反射到该声明或当前阶段不适用”，不是一个可直接传给 pipeline 的有效 tessellation 配置。

## 7. 序列化与诊断

### 7.1 `toJson()`

```cpp
QByteArray json = desc.toJson();
```

`toJson()` 返回描述对象的 JSON 表示，适合日志、调试工具、反射检查器和问题报告。它是诊断输出，不应当被当作跨版本稳定的应用协议。JSON 字段名称和格式属于 Qt 实现的一部分，升级 Qt 后应重新验证。

### 7.2 `serialize()` 和 `deserialize()`

```cpp
QByteArray serializeDescription(const QShaderDescription &desc)
{
    QByteArray bytes;
    QBuffer buffer(&bytes);
    buffer.open(QIODevice::WriteOnly);
    QDataStream stream(&buffer);
    desc.serialize(&stream, 1);
    return bytes;
}

QShaderDescription readDescription(const QByteArray &bytes)
{
    QBuffer buffer;
    buffer.setData(bytes);
    buffer.open(QIODevice::ReadOnly);
    QDataStream stream(&buffer);
    return QShaderDescription::deserialize(&stream, 1);
}
```

注意：

- `stream` 必须指向处于正确读写状态的 `QDataStream`；
- `version` 是 Qt shader 反射序列化格式的版本参数，不是 GLSL、SPIR-V 或 shader stage 版本；
- 反序列化从 stream 的当前位置读取；
- 数据损坏、版本不匹配或流读取失败时，应检查返回对象的 `isValid()`；
- 若只是为了日志或人工查看，优先使用 `toJson()`；
- 若要持久化，优先让 `QShader` 的 package 序列化统一管理 shader code 和 description，避免单独维护容易失配的描述文件。

不要把任意外部字节流直接当作可信 shader 资产。shader package 和反射二进制都应有来源、版本和大小控制。

## 8. 生命周期、拷贝和线程

`QShaderDescription` 不继承 `QObject`，也不拥有 GPU 资源。它采用隐式共享风格的内部数据：

- 默认构造创建空描述；
- 复制和按值返回通常成本较低；
- `detach()` 可强制分离共享数据；
- 析构只释放描述对象自身的共享存储；
- 销毁描述不会影响 `QShader` 或 QRhi pipeline。

隐式共享不是“同一个实例可以并发写”。多个线程读取独立副本通常适合；如果一个线程通过内部工具路径修改描述，而另一个线程同时读取同一对象，仍需要外部同步。

普通应用通常只读取 `QShader::description()` 返回的对象，不应依赖私有头文件 `qshaderdescription_p.h` 来改写内部列表。私有头文件没有公共兼容性承诺。

## 9. 常见误区与排查顺序

### 9.1 把 `isValid()` 当成“所有布局都完整”

`isValid()` 只表示描述对象包含可用反射信息。它不保证每个变量都有 location，不保证每个资源都有 binding，不保证所有 block 的大小都非零，也不保证目标后端支持该接口。

### 9.2 用变量名代替资源分类

名称叫 `texture` 的变量可能是 combined sampler、separate image 或 storage image。应根据返回列表和 `VariableType` 判断，不要根据名字猜。

### 9.3 把 `binding` 和 `location` 混用

顶点输入/输出使用 location，buffer 和 image/sampler 资源使用 binding 与 descriptor set。它们属于不同的接口空间。

### 9.4 忽略 `descriptorSet == -1`

某些 shader、语言或生成路径没有显式 descriptor set。负值表示“未提供”，不是应该转换成一个很大的无符号数。

### 9.5 把 `size == 0` 当成空 block

`size == 0` 也可能表示布局大小未知，尤其是运行时数组。对 storage block 应同时看 `knownSize`、成员的 `arrayDims` 和 `runtimeArrayStride`。

### 9.6 只读取一层 `structMembers`

结构体可以嵌套，数组元素也可能是结构体。布局工具必须递归处理成员，并在每一层加上父成员的 offset。

### 9.7 只按 `VariableType` 创建 storage image

storage image 还需要看 `imageFormat` 和 `imageFlags`。只检查 `Image2D` 而忽略格式和读写能力，可能在资源创建或 pipeline 验证时失败。

### 9.8 把 compute local size 当 dispatch 数量

local size 是一个 workgroup 内的 invocation 数。dispatch 的 group 数由应用数据规模决定，二者不能直接互换。

### 9.9 认为 push constant 一定可移植

反射可以描述 push constant，但目标 QRhi 后端和 Qt 版本未必提供对等的运行时更新路径。跨后端代码应准备 uniform buffer 等替代方式。

### 9.10 把 `toJson()` 当稳定格式

JSON 输出适合诊断，不适合作为跨 Qt 版本持久化协议。若必须存储，应由应用定义自己的版本化格式，并把需要的字段明确复制出来。

### 9.11 直接信任外部序列化数据

反序列化失败要检查 `isValid()`，外部输入还要限制文件大小、来源和版本。反射描述本身虽不是 GPU 资源，但它通常来自 shader package，不能跳过应用的资产信任边界。

## 10. 逐项 API 说明

### 构造、共享和状态

#### `QShaderDescription::QShaderDescription()`

创建空的反射描述。默认内部列表为空，local size 为 `{0, 0, 0}`，tessellation 相关枚举为 `Unknown...`，输出顶点数为 `0`。空对象通常不具备可用反射信息，应先检查 `isValid()`。

#### `QShaderDescription::QShaderDescription(const QShaderDescription &other)`

复制描述对象。它复制值语义，底层数据可隐式共享；后续分离不会改变源对象的逻辑内容。

#### `QShaderDescription &QShaderDescription::operator=(const QShaderDescription &other)`

复制赋值。赋值后目标对象包含源描述的逻辑快照，不会关联任何 GPU 资源。

#### `QShaderDescription::~QShaderDescription()`

销毁描述对象及其共享数据引用。不会销毁 shader、buffer、pipeline 或其他 QRhi 资源。

#### `void QShaderDescription::detach()`

强制当前对象从共享数据中分离。它是共享存储控制 API，不会从 shader 文本重新生成反射，也不提供公开的逐字段 setter。普通只读代码通常不需要调用。

#### `bool QShaderDescription::isValid() const`

判断描述是否包含可用反射数据。它不是完整性、后端兼容性或 pipeline 创建成功的保证。对默认对象、解析失败对象或没有有效反射记录的对象，应按 `false` 处理。

### 序列化

#### `void QShaderDescription::serialize(QDataStream *stream, int version) const`

把描述写入给定的 `QDataStream`。stream 必须可写，version 必须与读取方约定一致。它只序列化描述，不会自动写入对应的 shader code；生产资产更适合序列化完整 `QShader` package。

#### `QByteArray QShaderDescription::toJson() const`

返回描述的 JSON 诊断表示。适合日志和工具展示；不保证是跨 Qt 版本稳定的持久化协议。

#### `[static] QShaderDescription QShaderDescription::deserialize(QDataStream *stream, int version)`

从 stream 的当前位置读取描述并返回值对象。流损坏、版本错误或读取失败时，调用方应检查返回值的 `isValid()`，不要只检查返回对象是否成功构造。

### 普通输入和输出

#### `QList<QShaderDescription::InOutVariable> QShaderDescription::inputVariables() const`

返回普通 stage input 变量列表。使用 `location` 建立输入布局，使用 `type`、`arrayDims` 和 `structMembers` 解释数据形状。没有显式 location 的变量可能返回 `-1`。

#### `QList<QShaderDescription::InOutVariable> QShaderDescription::outputVariables() const`

返回普通 stage output 变量列表。它可用于检查相邻 shader stage 的接口，但不会替你验证两个 stage 的 location、类型和数组维度是否完全匹配。

#### `QList<QShaderDescription::BuiltinVariable> QShaderDescription::inputBuiltinVariables() const`

返回输入侧 builtin 变量。使用 `BuiltinType` 判断语义，使用 `varType` 和 `arrayDims` 判断实际类型和维度；不要把 builtin 当作普通 location 输入。

#### `QList<QShaderDescription::BuiltinVariable> QShaderDescription::outputBuiltinVariables() const`

返回输出侧 builtin 变量。它常用于检查 position、frag depth、tessellation 或 compute 相关内建接口是否存在。

### Buffer blocks

#### `QList<QShaderDescription::UniformBlock> QShaderDescription::uniformBlocks() const`

返回 uniform block 列表。每一项包含 block 名称、实例名、大小、binding、descriptor set 和递归成员布局。`size` 与成员 offset 应用于 CPU 侧缓冲填充，但不能直接替代后端对齐规则的验证。

#### `QList<QShaderDescription::PushConstantBlock> QShaderDescription::pushConstantBlocks() const`

返回 push constant block 列表。它描述 shader 侧布局，不表示当前 QRhi 后端一定可更新该资源。跨后端使用前应检查 Qt 和后端能力。

#### `QList<QShaderDescription::StorageBlock> QShaderDescription::storageBlocks() const`

返回 storage block 列表。重点读取 `knownSize`、`runtimeArrayStride`、`qualifierFlags` 和成员的 `arrayDims`。运行时数组的总长度由实际 buffer 大小决定。

### Image 和 sampler

#### `QList<QShaderDescription::InOutVariable> QShaderDescription::combinedImageSamplers() const`

返回同时包含 image 与 sampler 语义的 combined sampler 资源。资源 binding 和 descriptor set 从 `InOutVariable` 读取。

#### `QList<QShaderDescription::InOutVariable> QShaderDescription::separateImages() const`

返回独立 image/texture 资源。它们可能需要和 `separateSamplers()` 中的 sampler 分别绑定，具体合并方式取决于目标 shader 语言、生成器和后端。

#### `QList<QShaderDescription::InOutVariable> QShaderDescription::separateSamplers() const`

返回独立 sampler 资源。不能假设它们和同名 image 自动配对；如果 shader package 还保存了 separate-to-combined 映射，应按对应 `QShaderKey` 读取映射。

#### `QList<QShaderDescription::InOutVariable> QShaderDescription::storageImages() const`

返回 storage image 资源。除 `type`、binding 和 descriptor set 外，还要检查 `imageFormat` 与 `imageFlags`，因为 storage image 的格式和读写能力会影响实际资源配置。

### Compute 和 tessellation

#### `std::array<uint, 3> QShaderDescription::computeShaderLocalSize() const`

返回 compute shader 的 local workgroup 尺寸，顺序是 x、y、z。默认或未提供时可能为 `{0, 0, 0}`；它不是 dispatch group 数，也不能直接作为除数。

#### `uint QShaderDescription::tessellationOutputVertexCount() const`

返回 tessellation control shader 声明的每个 patch 输出顶点数。没有该声明或当前阶段不适用时为 `0`，不能据此推导任意后端的最大支持值。

#### `QShaderDescription::TessellationMode QShaderDescription::tessellationMode() const`

返回细分模式：triangles、quads 或 isolines。`UnknownTessellationMode` 表示未知或不适用。

#### `QShaderDescription::TessellationWindingOrder QShaderDescription::tessellationWindingOrder() const`

返回细分生成图元的绕序：clockwise 或 counter-clockwise。未知时返回 `UnknownTessellationWindingOrder`。

#### `QShaderDescription::TessellationPartitioning QShaderDescription::tessellationPartitioning() const`

返回细分间距策略：equal、fractional even 或 fractional odd。未知时返回 `UnknownTessellationPartitioning`。

### 相关非成员运算符

#### `bool operator==(const QShaderDescription &lhs, const QShaderDescription &rhs) noexcept`

比较两个描述对象的值内容，包括反射列表和 stage execution 元数据。相等只表示描述数据相等，不表示对应 shader code、后端资源或 pipeline 也相等。

#### `bool operator!=(const QShaderDescription &lhs, const QShaderDescription &rhs) noexcept`

返回 `operator==` 的逻辑反值，属于头文件中的便捷内联运算符。

## API 速查表

| 类别 | API | 作用 | 关键边界 |
| --- | --- | --- | --- |
| 构造 | `QShaderDescription()` | 创建空反射描述 | 默认通常无有效反射；local size 为零数组 |
| 构造 | `QShaderDescription(const QShaderDescription &other)` | 复制描述 | 值语义和隐式共享；不复制 GPU 资源 |
| 赋值 | `operator=(const QShaderDescription &other)` | 复制赋值 | 目标变成源描述的逻辑副本 |
| 析构 | `~QShaderDescription()` | 销毁描述对象 | 不影响 QShader 或 QRhi 资源 |
| 共享 | `detach()` | 强制分离共享存储 | 不会重新生成反射，也不是公开 builder |
| 状态 | `isValid() const` | 判断是否含可用反射 | 不保证字段完整或后端兼容 |
| 序列化 | `serialize(QDataStream *, int)` | 写出描述 | stream、version 必须与读取方匹配 |
| 诊断 | `toJson() const` | 导出 JSON | 适合诊断，不是稳定跨版本协议 |
| 反序列化 | `deserialize(QDataStream *, int)` | 读取描述 | 失败后检查 `isValid()` |
| 输入 | `inputVariables() const` | 查询普通输入变量 | location 可能为 `-1` |
| 输出 | `outputVariables() const` | 查询普通输出变量 | 不自动验证相邻 stage 接口 |
| builtin | `inputBuiltinVariables() const` | 查询输入 builtin | 用 `BuiltinType`，不是 location |
| builtin | `outputBuiltinVariables() const` | 查询输出 builtin | 用 `BuiltinType`，不是 location |
| block | `uniformBlocks() const` | 查询 uniform block 布局 | size/offset 按 shader 布局解释 |
| block | `pushConstantBlocks() const` | 查询 push constant 布局 | 反射存在不等于 QRhi 一定支持更新 |
| block | `storageBlocks() const` | 查询 storage block 布局 | 关注 knownSize 和 runtimeArrayStride |
| 资源 | `combinedImageSamplers() const` | 查询 combined sampler | binding/set 仍需按资源配置验证 |
| 资源 | `separateImages() const` | 查询独立 image | 不自动和 sampler 配对 |
| 资源 | `separateSamplers() const` | 查询独立 sampler | 不自动和 image 配对 |
| 资源 | `storageImages() const` | 查询 storage image | 还要检查 imageFormat 和 imageFlags |
| compute | `computeShaderLocalSize() const` | 查询 local workgroup 尺寸 | 不是 dispatch group 数；零值表示未提供 |
| tessellation | `tessellationOutputVertexCount() const` | 查询 patch 输出顶点数 | 未提供时为 `0` |
| tessellation | `tessellationMode() const` | 查询 triangles/quads/isoline | `Unknown` 表示未知或不适用 |
| tessellation | `tessellationWindingOrder() const` | 查询 cw/ccw | `Unknown` 表示未知或不适用 |
| tessellation | `tessellationPartitioning() const` | 查询 equal/fractional 策略 | `Unknown` 表示未知或不适用 |
| 类型 | `VariableType` | 描述变量、矩阵、资源或 struct 类型 | 使用枚举名，不假设可重排数值 |
| 类型 | `ImageFormat` | 描述 storage image 格式 | 不直接等价于 QRhi texture format |
| flags | `ImageFlags` | 描述 image 读写属性 | 是组合 flags，不是互斥 enum |
| flags | `QualifierFlags` | 描述 storage block 限定符 | 不自动实现同步和屏障 |
| 结构体 | `BlockVariable` | 描述 block 成员和递归布局 | offset/stride 是 shader 布局；数组 0 可能是运行时维度 |
| 结构体 | `InOutVariable` | 描述输入、输出和 image/sampler 资源 | location、binding、set 是不同编号空间 |
| 结构体 | `UniformBlock` | 描述 uniform block | size 不是 C++ `sizeof` |
| 结构体 | `PushConstantBlock` | 描述 push constant | 需检查 QRhi/后端实际支持 |
| 结构体 | `StorageBlock` | 描述 SSBO 等 storage block | knownSize 不含运行时数组尾部 |
| 结构体 | `BuiltinVariable` | 描述 builtin 语义和类型 | builtin 不使用普通 location |
| 比较 | `operator==(const QShaderDescription &, const QShaderDescription &) noexcept` | 比较反射值内容 | 不证明 shader/pipeline 兼容 |
| 比较 | `operator!=(const QShaderDescription &, const QShaderDescription &) noexcept` | 相等比较的反值 | 仍是值比较 |

---

### 一句话总结

`QShaderDescription` 是 shader package 的反射布局快照：它把 stage 输入输出、builtin、buffer block、image/sampler 资源和 compute/tessellation 元数据暴露给应用。使用时先检查 `isValid()`，再按不同资源分组读取；对 `-1`、`0`、运行时数组、矩阵 stride 和有限 RHI 兼容性保持谨慎，不能把反射结果直接当成已经验证成功的 GPU pipeline。
