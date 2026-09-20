# Qt QShader::SeparateToCombinedImageSamplerMapping：纹理与采样器合并映射

> 适用版本：Qt 6.11.1  
> 头文件：`#include <rhi/qshader.h>`  
> 所属模块：`Qt6::Gui` / RHI  
> 归属类型：`QShader::SeparateToCombinedImageSamplerMapping`  
> 继承：无  
> 类型定位：后端资源绑定转换的值结构体

## 1. 它解决什么问题

`QShader::SeparateToCombinedImageSamplerMapping` 描述一条纹理资源映射：原始 shader 把 texture 和 sampler 作为两个独立资源绑定，而某个目标语言或图形 API 的 shader 代码需要把它们表示成一个 combined image sampler。

一个映射条目包含：

- 生成后的 combined sampler 名称；
- 原始 shader 中 texture 的 binding；
- 原始 shader 中 sampler 的 binding。

例如：

```text
combinedSamplerName = "_54"
textureBinding      = 1
samplerBinding     = 2
```

表示生成的 GLSL 代码中有一个名为 `_54` 的 `sampler2D` 或 `sampler3D` uniform，它对应原始 shader 中 binding `1` 的 texture 和 binding `2` 的 sampler。

这个结构体不创建纹理、不创建采样器、不修改 `QRhiShaderResourceBinding`，也不执行 shader 翻译。它只是 `QShader` 生成和后端消费之间的一条元数据记录，通常以 `QShader::SeparateToCombinedImageSamplerMappingList` 的形式按 `QShaderKey` 保存。

## 2. 构建与包含

该结构体定义在 `QShader` 的 RHI 头文件中：

```cpp
#include <rhi/qshader.h>
```

RHI API 的兼容性边界同样适用于本类型：

- 没有源代码兼容性保证；
- 没有二进制兼容性保证；
- CMake 通常需要链接 `Qt::GuiPrivate`；
- 不应把该结构体暴露在跨 Qt 小版本的公共 ABI 中。

CMake：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui GuiPrivate)
target_link_libraries(mytarget PRIVATE Qt6::Gui Qt6::GuiPrivate)
```

## 3. 最小使用方式

### 3.1 构造一个映射条目

这是一个聚合结构体，没有公开构造函数。应使用值初始化，确保整数成员有确定值：

```cpp
QShader::SeparateToCombinedImageSamplerMapping mapping{};
mapping.combinedSamplerName = QByteArrayLiteral("_54");
mapping.textureBinding = 1;
mapping.samplerBinding = 2;
```

也可以使用聚合初始化：

```cpp
QShader::SeparateToCombinedImageSamplerMapping mapping{
    QByteArrayLiteral("_54"),
    1,
    2
};
```

### 3.2 放入 `QShader`

```cpp
QShader::SeparateToCombinedImageSamplerMappingList mappings;
mappings.append(mapping);

shader.setSeparateToCombinedImageSamplerMappingList(key, mappings);

const auto stored =
    shader.separateToCombinedImageSamplerMappingList(key);
```

`key` 必须是与这些映射对应的 shader 代码的精确 `QShaderKey`。GLSL、MSL 或其他版本的代码可能有不同的 binding 和名称，不能把一条记录无条件复用于所有 key。

## 4. 核心使用模型

### 4.1 三个字段是一条完整关系

一个条目不是“combined sampler 名称列表”，而是名称与两个原始 binding 的三元关系：

```text
原始 texture binding + 原始 sampler binding
                     -> 生成的 combined sampler name
```

缺少任意一个字段，后端就无法知道生成后的 sampler 对应哪些原始资源。不要只修改名称而保留旧 binding，也不要把 texture binding 当成 combined sampler 的 binding。

### 4.2 `combinedSamplerName` 是生成代码中的名称

该字段是 `QByteArray`，保存目标 shader 代码中 combined sampler uniform 的名称。Qt 文档示例使用 `_54`，但名称格式由 shader 转换器决定，不应假设所有生成器都采用相同前缀或编号策略。

它不是原始 shader 中 texture 的变量名，也不是 `QRhiShaderResourceBinding` 的整数 binding。调试时应把它与实际生成的 shader 源码或反射信息对照。

### 4.3 `textureBinding` 和 `samplerBinding` 是原始独立绑定

这两个整数分别指向原始 shader 中的 texture 和 sampler 资源。它们不是数组索引，也不是结构体成员偏移，具体 binding 空间仍受 shader 生成器和 RHI 的资源绑定模型约束。

不要把两个值合并成一个整数，也不要在应用层重新排序后再期待 Qt 自动修正。条目应原样来自生成器，或者由掌握目标后端约定的工具代码创建。

### 4.4 列表按 `QShaderKey` 保存

`QShader` 使用 `SeparateToCombinedImageSamplerMappingList`，即：

```cpp
QList<QShader::SeparateToCombinedImageSamplerMapping>
```

该列表按 `QShaderKey` 关联到某一份 shader 代码。查询不到或当前语言不需要 separate-to-combined 转换时，`QShader::separateToCombinedImageSamplerMappingList(key)` 返回空列表。

## 5. 实际使用场景

### 5.1 GLSL separate texture/sampler 到 combined sampler

某些 shader 语言和后端允许把 texture 与 sampler 分开声明，而生成后的 GLSL 需要使用 `sampler2D`、`sampler3D` 等 combined 类型。转换器可以用该列表告诉运行时每个 combined sampler对应的原始资源。

### 5.2 预编译 `.qsb` 资产

通常由 `qsb` 或 `QShaderBaker` 生成并写入 `.qsb` package。应用通过 `QShader::fromSerialized()` 读取整个 package，不必手工逐条重建映射。

### 5.3 shader package 检查工具

shader 工具可以把列表显示为：

```text
生成名称   原始 texture binding   原始 sampler binding
_54        1                      2
```

这适合排查资源绑定不一致，但显示时应注明它是特定 key 的后端映射，而不是全局资源表。

### 5.4 自定义 shader 生成流水线

自定义生成器在明确掌握目标 Qt 版本、shader 语言和 RHI 后端约定时，可以手工设置映射列表。生成器必须同时保证 shader code、入口点、反射描述、binding map 和本列表保持一致。

## 6. 生命周期、所有权和线程

### 6.1 轻量值结构体

该类型不继承 `QObject`，不拥有 texture、sampler、GPU module 或外部内存。可以按值复制、放进 `QList`，也可以作为 `QShader` setter 的参数。

### 6.2 默认初始化的整数边界

头文件只声明三个公开数据成员，没有用户声明的构造函数或默认成员初始值。下面的普通默认初始化不应读取：

```cpp
QShader::SeparateToCombinedImageSamplerMapping value; // int 成员未初始化
```

需要确定的空记录时使用：

```cpp
QShader::SeparateToCombinedImageSamplerMapping value{};
```

但值初始化得到的 binding 为 `0`，这只是确定的数值，不代表 binding `0` 在你的 shader 中一定有效。

### 6.3 `QShader` 返回的是列表值

`QShader::separateToCombinedImageSamplerMappingList()` 返回一个列表值。修改查询结果不会自动修改原 package：

```cpp
auto list = shader.separateToCombinedImageSamplerMappingList(key);
list[0].textureBinding = 4;
shader.setSeparateToCombinedImageSamplerMappingList(key, list);
```

修改后必须显式写回 `QShader`。

### 6.4 线程边界来自 RHI 使用者

结构体和列表本身可以按值在线程之间传递，但完整 `QShader` package 的更新以及 QRhi pipeline 替换仍要遵守渲染线程和帧生命周期约束。不要在渲染线程正在读取 package 时从另一个线程直接写入同一对象。

## 7. 与相关类型的边界

### 7.1 与 `QShaderKey`

`QShaderKey` 决定这条 mapping 属于哪一份 source、版本和 variant。key 不同，代码中的 combined sampler 名称和原始 binding 都可能不同。

### 7.2 与 `QShaderCode`

`QShaderCode` 保存实际源代码或字节码以及入口点；本结构体只保存转换关系。它不能单独说明 shader 是否有效或是否能被后端编译。

### 7.3 与 `NativeResourceBindingMap`

`NativeResourceBindingMap` 描述另一类资源 binding 映射；本结构体专门描述 separate texture/sampler 合并。两者可能同时存在，不能用其中一个替代另一个。

### 7.4 与 `QRhiShaderResourceBinding`

`QRhiShaderResourceBinding` 描述运行时要绑定的纹理、采样器、buffer 和 binding。mapping 只告诉生成器或后端如何理解 shader 代码中的资源关系，不会创建或绑定实际资源。

### 7.5 与 `QShaderDescription`

反射描述提供资源和接口信息；mapping 提供某些语言转换过程所需的额外关联。调试 binding 时通常要同时查看两者和最终生成的 shader 代码。

## 8. 常见误区与排查顺序

### 8.1 把 `combinedSamplerName` 当成 binding

它是生成后的变量名称，不是整数 binding。需要 binding 时查看对应的 binding map、反射数据和目标 API 规则。

### 8.2 交换 texture 和 sampler binding

`textureBinding` 与 `samplerBinding` 有明确角色。交换它们会让生成的 combined sampler 绑定到错误资源，通常表现为采样器类型错误、纹理内容异常或 pipeline 验证失败。

### 8.3 手工使用 `0` 作为“无效 binding”

结构体没有定义无效 binding 常量。`0` 可能是一个合法 binding，也可能只是值初始化结果。缺少映射应使用空列表或不写入条目，而不是创建一条全零记录。

### 8.4 一条记录复用到所有 shader key

不同 source、版本和 variant 的生成代码可能有不同名称和 binding。映射始终按 key 保存，使用前确认 key 完全匹配。

### 8.5 修改返回列表却不写回

查询函数返回列表值。修改局部列表不会影响 `QShader`，必须调用对应 setter。

### 8.6 认为它会自动完成 shader 翻译

该结构体只是转换元数据。它不会把 `texture2D` 变成 `sampler2D`，也不会重新编译或生成代码。

### 8.7 认为列表顺序就是资源 binding 顺序

Qt 文档只定义列表包含映射条目，没有保证列表顺序具有额外的排序协议。按字段查找和比较，不要把列表位置当作固定资源编号。

### 8.8 跨 Qt 版本解析字段语义

QShader/RHI API 没有源和二进制兼容保证。即使三个字段的数据类型不变，也不要把某版本生成的内部约定当作跨版本 ABI。

## 9. 逐项 API 说明

### 数据成员

#### `QByteArray QShader::SeparateToCombinedImageSamplerMapping::combinedSamplerName`

保存生成后的 combined image sampler 名称，例如 `_54`。它对应目标 shader 代码中的 `sampler2D`、`sampler3D` 等 combined sampler uniform。

该字段不是原始 texture 变量名，不是整数 binding，也没有统一的命名格式。默认构造或值初始化时为空。

#### `int QShader::SeparateToCombinedImageSamplerMapping::textureBinding`

保存原始 shader 中 texture 资源的 binding。它与 `samplerBinding` 一起确定 combined sampler 对应的两份原始资源。

头文件没有为该字段提供默认成员初始值。使用聚合对象时应值初始化或显式赋值；`0` 不是 Qt 定义的无效值。

#### `int QShader::SeparateToCombinedImageSamplerMapping::samplerBinding`

保存原始 shader 中 sampler 资源的 binding。它与 `textureBinding` 的角色不同，不能交换。

该字段也没有默认成员初始值。它的有效范围和 binding 空间由实际 shader 生成器和后端约定决定。

### 相关列表与 `QShader` API

#### `using QShader::SeparateToCombinedImageSamplerMappingList = QList<SeparateToCombinedImageSamplerMapping>`

定义映射条目的 Qt 列表类型。列表按 `QShaderKey` 保存在 `QShader` 中；没有适用映射时返回空列表。

#### `QShader::SeparateToCombinedImageSamplerMappingList QShader::separateToCombinedImageSamplerMappingList(const QShaderKey &key) const`

读取指定 shader key 的映射列表。返回空列表表示没有数据或该语言、阶段、后端不需要这类转换，不一定表示 shader 无效。

#### `void QShader::setSeparateToCombinedImageSamplerMappingList(const QShaderKey &key, const QShader::SeparateToCombinedImageSamplerMappingList &list)`

把映射列表写入指定 key。setter 修改的是 `QShader` package，调用方应让列表与该 key 的 code、反射和其他 binding 元数据一致。

#### `void QShader::removeSeparateToCombinedImageSamplerMappingList(const QShaderKey &key)`

删除指定 key 的映射列表。它不会删除对应 shader code、`NativeResourceBindingMap` 或 `NativeShaderInfo`。

## API 速查表

| 类别 | API | 作用 | 关键边界 |
| --- | --- | --- | --- |
| 字段 | `QByteArray combinedSamplerName` | 保存生成后的 combined sampler 名称 | 是变量名，不是 binding；名称格式由生成器决定 |
| 字段 | `int textureBinding` | 保存原始 texture 绑定 | `0` 可能合法；必须与实际 shader binding 约定一致 |
| 字段 | `int samplerBinding` | 保存原始 sampler 绑定 | 不能与 texture binding 交换；无默认成员初值 |
| 值初始化 | `Mapping mapping{}` | 创建字段有确定初值的空结构 | 整数为 `0` 不代表有效资源映射 |
| 列表 | `SeparateToCombinedImageSamplerMappingList` | 映射条目的 `QList` 别名 | 列表按 `QShaderKey` 保存；空列表可能是合法状态 |
| 查询 | `QShader::separateToCombinedImageSamplerMappingList(const QShaderKey &) const` | 读取指定 key 的映射 | 不支持或无数据时返回空列表 |
| 写入 | `QShader::setSeparateToCombinedImageSamplerMappingList(const QShaderKey &, const SeparateToCombinedImageSamplerMappingList &)` | 写入指定 key 的映射 | 修改查询副本不会自动写回；必须调用 setter |
| 删除 | `QShader::removeSeparateToCombinedImageSamplerMappingList(const QShaderKey &)` | 删除指定 key 的映射 | 不影响 shader code、binding map 或 native info |
| 相关 | `QShaderKey` | 指定 source、版本和 variant | 映射只对精确 key 生效，不能跨 key 复用 |
| 相关 | `QShaderCode` | 保存实际源代码或字节码 | 映射不负责翻译、编译或校验代码 |
| 相关 | `NativeResourceBindingMap` | 保存另一类后端 binding 映射 | 不能替代 separate-to-combined 关系 |
| 相关 | `QShaderDescription` | 描述资源和接口反射信息 | 应与映射和生成后的 shader 一起核对 |
| 相关 | `QRhiShaderResourceBinding` | 描述实际运行时资源绑定 | 映射不会创建纹理、采样器或 GPU 资源 |
| 兼容性 | RHI API | 提供 Qt shader 后端转换数据 | 无源/二进制兼容保证，应锁定 Qt 版本 |

---

### 一句话总结

`QShader::SeparateToCombinedImageSamplerMapping` 用三个字段表达“原始 texture binding + 原始 sampler binding -> 生成后的 combined sampler 名称”；它是按 `QShaderKey` 保存的后端元数据，不是实际资源或编译器，使用时要值初始化结构体、保持字段角色和 key 精确匹配，并通过 `QShader` setter 显式写回。
