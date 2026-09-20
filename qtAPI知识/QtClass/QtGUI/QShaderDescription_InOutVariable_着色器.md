# Qt QShaderDescription::InOutVariable：stage 接口与 image/sampler 资源记录

> 适用版本：Qt 6.11.1  
> 头文件：`#include <rhi/qshaderdescription.h>`  
> 所属模块：`Qt6::Gui`，RHI 相关 API 的兼容性保证有限  
> 定位：`QShaderDescription` 的嵌套聚合结构体，since Qt 6.6

## 1. 它解决什么问题

`QShaderDescription::InOutVariable` 是一个复用的反射记录，用于描述两类 shader 接口：

1. 普通 stage input/output 变量；
2. combined sampler、separate image、separate sampler 和 storage image 资源。

它把名称、类型、location、资源 binding、descriptor set、image format、读写 flags、数组维度和结构体成员放在一起。实际使用时，必须先知道该记录来自哪个列表，不能仅凭字段名称猜用途。

## 2. 结构定义与初始化

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

实际应用一般从以下 API 获得它：

```cpp
desc.inputVariables();
desc.outputVariables();
desc.combinedImageSamplers();
desc.separateImages();
desc.separateSamplers();
desc.storageImages();
```

## 3. 字段语义

| 字段 | 普通 stage input/output | image/sampler 资源 |
| --- | --- | --- |
| `name` | 输入或输出变量名 | shader 资源名 |
| `type` | 标量、向量、矩阵或 struct | sampler/image 类型 |
| `location` | stage interface location | 通常不适用，可能为 `-1` |
| `binding` | 通常不适用，可能为 `-1` | 资源 binding |
| `descriptorSet` | 通常不适用，可能为 `-1` | descriptor set |
| `imageFormat` | 通常为 `ImageFormatUnknown` | storage image 的格式要求 |
| `imageFlags` | 通常为空 | image 读写属性 |
| `arrayDims` | 输入/输出数组维度 | 资源数组维度 |
| `perPatch` | tessellation patch 级变量 | 通常为 `false` |
| `structMembers` | struct 输入/输出成员 | 结构化资源或变量的成员 |

`location`、`binding` 和 `descriptorSet` 是三个不同的编号空间：

- location 连接相邻 shader stage 或顶点输入；
- binding 标识资源绑定槽；
- descriptor set 标识资源集合。

## 4. 默认值的意义

- `type == Unknown`：类型没有反射到或记录为空；
- `location == -1`：没有可用 stage location；
- `binding == -1`：没有可用资源 binding；
- `descriptorSet == -1`：没有提供 descriptor set；
- `imageFormat == ImageFormatUnknown`：不是 storage image，或格式未知；
- `imageFlags` 为空：没有反射到 image 读写限定；
- `arrayDims` 为空：不是数组或数组维度未提供；
- `perPatch == false`：不是 patch 级变量，或未标记；
- `structMembers` 为空：不是结构体或没有成员记录。

负数不能转换成无符号 binding，也不能当作“自动分配”请求。应用应明确处理缺失信息。

## 5. 按来源列表解释记录

### 5.1 `inputVariables()` 和 `outputVariables()`

这些列表描述普通 stage interface。通常使用 `location` 配对相邻 shader stage，使用 `type`、`arrayDims` 和 `structMembers` 验证接口形状。

```cpp
for (const auto &variable : desc.inputVariables()) {
    if (variable.location < 0)
        continue;
    qDebug() << variable.location << variable.name << variable.type;
}
```

它不会自动检查两个 stage 的输入输出是否匹配，也不会根据 location 生成完整的 CPU vertex buffer 配置。

### 5.2 `combinedImageSamplers()`

记录 image 与 sampler 已组合的资源。通常重点是 `type`、`binding` 和 `descriptorSet`。它不表示应用可以忽略纹理格式、采样器状态或后端资源限制。

### 5.3 `separateImages()` 和 `separateSamplers()`

这两个列表把 image/texture 与 sampler 分开描述。不要只按同名变量自动配对；某些后端需要结合 `QShader` 中按 `QShaderKey` 保存的 separate-to-combined 映射。

### 5.4 `storageImages()`

storage image 除了类型和绑定外，还要读取：

- `imageFormat`；
- `imageFlags`；
- 数组维度；
- descriptor set。

storage image 的读写和格式都会影响实际 QRhi 资源及 pipeline 配置。

## 6. image flags

`imageFlags` 的类型是 `QShaderDescription::ImageFlags`：

```cpp
enum ImageFlag {
    ReadOnlyImage = 1 << 0,
    WriteOnlyImage = 1 << 1
};
```

这是可组合 flags，不是互斥枚举。使用时可以写：

```cpp
if (variable.imageFlags.testFlag(QShaderDescription::ReadOnlyImage)) {
    // shader 只读 image
}
```

没有 flag 时不要自动推断访问权限。两个 flag 同时存在时，仍应以生成器和 shader 语言规则为准。

## 7. `perPatch`、数组和 struct

`perPatch` 主要服务 tessellation stage interface。它表示变量按 patch 传递，而不是按每个 tessellated vertex 传递。它只在相应阶段和变量声明中有意义。

数组变量通过 `arrayDims` 描述。结构体变量通常用 `type == Struct`，并在 `structMembers` 中保存字段。与 block 成员不同，stage interface 的结构体字段不一定有 buffer offset；不要把它们当成 `BlockVariable` 的布局记录。

## 8. 常见误区

- 把所有记录都当成 vertex input：资源列表中的 `binding` 与 stage input 的 `location` 完全不同。
- 把 `binding == -1` 转成无符号整数：这会制造巨大且错误的 binding。
- 忽略 `descriptorSet`：跨资源集合后端时可能导致绑定到错误 set。
- 只看 `type` 不看 `imageFormat` 和 `imageFlags`：storage image 配置会不完整。
- 把 separate image 和 sampler 按名字强行配对：应使用生成器提供的映射。
- 把 `perPatch` 忽略：tessellation 输入输出接口可能因此不匹配。
- 直接默认构造后把 `imageFlags` 当成已确定权限：默认记录不是有效反射。
- 认为结构体成员一定有 offset：只有 block 布局中的 `BlockVariable` 才提供那种偏移语义。

## 9. 相关非成员运算符

### `bool operator==(const QShaderDescription::InOutVariable &, const QShaderDescription::InOutVariable &) noexcept`

比较完整记录的值，包括名称、类型、位置、资源绑定、格式、flags、数组、patch 属性和结构体成员。它适合反射缓存比较，不是运行时资源兼容性证明。

### `bool operator!=(const QShaderDescription::InOutVariable &, const QShaderDescription::InOutVariable &) noexcept`

返回相等比较的逻辑反值。

## API 速查表

| 类别 | API/字段 | 作用 | 关键边界 |
| --- | --- | --- | --- |
| 字段 | `name` | 变量或资源名称 | 不能单独决定资源类别 |
| 字段 | `type` | 变量或资源类型 | 与来源列表一起解释 |
| 字段 | `location` | stage interface location | 缺失时为 `-1` |
| 字段 | `binding` | 资源 binding | 与 location 不同；缺失时为 `-1` |
| 字段 | `descriptorSet` | 资源 descriptor set | 缺失时为 `-1` |
| 字段 | `imageFormat` | storage image 格式 | 非 image 通常为 Unknown |
| 字段 | `imageFlags` | image 读写 flags | 是组合 flags |
| 字段 | `arrayDims` | 数组维度 | 可能包含运行时维度 0 |
| 字段 | `perPatch` | 是否按 patch 传递 | 主要用于 tessellation |
| 字段 | `structMembers` | 结构体成员 | 不等同于 block offset 布局 |
| 查询 | `inputVariables()` | 获取输入记录 | location 可能缺失 |
| 查询 | `outputVariables()` | 获取输出记录 | 不自动验证 stage 匹配 |
| 查询 | `combinedImageSamplers()` | 获取组合 sampler | 仍要配置实际纹理/采样器 |
| 查询 | `separateImages()` | 获取独立 image | 不自动和 sampler 配对 |
| 查询 | `separateSamplers()` | 获取独立 sampler | 需要结合后端映射 |
| 查询 | `storageImages()` | 获取 storage image | 必须看格式和访问 flags |
| 比较 | `operator==` | 比较记录值内容 | 不是 GPU 兼容性检查 |
| 比较 | `operator!=` | 相等比较的反值 | 仍是值比较 |

---

### 一句话总结

`InOutVariable` 是一个按来源列表解释的通用反射记录：普通输入输出看 `location`，资源看 `binding`/`descriptorSet`，storage image 还要看格式和读写 flags；`-1` 表示信息未提供，不能当作有效编号。
