# Qt QShaderKey：多后端 shader 条目的精确索引

> 适用版本：Qt 6.11.1  
> 头文件：`#include <rhi/qshader.h>`  
> 所属模块：`Qt6::Gui`，RHI 相关 API 的兼容性保证有限  
> 继承：无  
> 类型定位：索引 `QShader` 内部代码条目的轻量值类型

## 1. 它解决什么问题

一个 `QShader` 可以包含多份代码：SPIR-V、GLSL、HLSL、MSL、DXIL、Metal library 或 WGSL，还可能有不同版本和 variant。`QShaderKey` 把选择维度组合为一个精确键：

```text
source + sourceVersion + sourceVariant
```

它解决的是“从一个多后端 shader package 中准确取出哪一份代码”的问题。它不是模糊搜索条件，不会自动匹配相近版本，也不会根据当前 QRhi 后端自动回退。

## 2. 构建与基本用法

```cpp
#include <rhi/qshader.h>

QShaderKey key(
    QShader::GlslShader,
    QShaderVersion(450),
    QShader::StandardShader);

QShaderCode code = shader.shader(key);
if (code.shader().isEmpty()) {
    // package 中没有这个精确 key
}
```

应用通常先读取 `shader.availableShaders()`，再根据后端和版本构造候选键。

## 3. 默认值

```cpp
QShaderKey key;
```

默认字段来自头文件：

- `source()`：`QShader::SpirvShader`；
- `sourceVersion()`：默认 `QShaderVersion`，版本为 `100`、flags 为空；
- `sourceVariant()`：`QShader::StandardShader`。

这不是“匹配任意 shader”的通配键。若 package 没有恰好是 SPIR-V/100/standard 的条目，查询仍然失败。

## 4. key 的三个维度

### 4.1 `source`

表示代码格式或语言，例如：

- `SpirvShader`；
- `GlslShader`；
- `HlslShader`；
- `DxbcShader`；
- `MslShader`；
- `DxilShader`；
- `MetalLibShader`；
- `WgslShader`。

它不是 shader stage。顶点、片段、计算阶段由 `QShader::stage()` 表示。

### 4.2 `sourceVersion`

这是 `QShaderVersion`，包含整数版本和 `GlslEs` flags。版本号相同但 GLSL ES 标志不同，得到的 key 也不同。

### 4.3 `sourceVariant`

表示代码变体，例如 `StandardShader`、`BatchableVertexShader` 或 Metal 专用 compute variant。特殊 variant 必须由生成器提供，不能只修改 key 的字段就把标准代码变成另一个变体。

## 5. 成员函数

### `QShaderKey::QShaderKey()`

constexpr、noexcept 默认构造。建立默认 key，不建立任何 `QShader` 条目。

### `QShaderKey::QShaderKey(QShader::Source s, const QShaderVersion &sver, QShader::Variant svar = QShader::StandardShader)`

用 source、版本和 variant 构造精确 key：

```cpp
QShaderKey spirv(
    QShader::SpirvShader,
    QShaderVersion(100));

QShaderKey es(
    QShader::GlslShader,
    QShaderVersion(300, QShaderVersion::GlslEs));
```

variant 默认是 `StandardShader`。构造不会检查 shader package 是否存在该条目，也不会编译或转换代码。

### `QShader::Source QShaderKey::source() const`

返回代码格式维度。

### `void QShaderKey::setSource(QShader::Source s)`

修改 source。它会改变 key 的值；若 key 已经作为 `QMap`、`QHash` 或 `QShader` 查询键使用，修改后应把它视为另一个 key。

### `QShaderVersion QShaderKey::sourceVersion() const`

返回版本对象的值副本，包括 version 和 flags。

### `void QShaderKey::setSourceVersion(const QShaderVersion &sver)`

替换版本维度。不会改变 `QShader` 中已经保存的代码，也不会自动选择相近版本。

### `QShader::Variant QShaderKey::sourceVariant() const`

返回 variant 维度。

### `void QShaderKey::setSourceVariant(QShader::Variant svar)`

替换 variant。只改变索引值，不生成对应代码。

## 6. 实际使用：选择代码和验证 fallback

```cpp
QList<QShaderKey> keys = shader.availableShaders();

const QList<QShaderKey> candidates = {
    QShaderKey(QShader::SpirvShader, QShaderVersion(100)),
    QShaderKey(QShader::GlslShader, QShaderVersion(450)),
    QShaderKey(QShader::GlslShader,
               QShaderVersion(300, QShaderVersion::GlslEs))
};

for (const QShaderKey &candidate : candidates) {
    if (!keys.contains(candidate))
        continue;

    const QShaderCode code = shader.shader(candidate);
    if (!code.shader().isEmpty()) {
        // 选择后还要结合 QRhi 后端和 stage 使用。
        break;
    }
}
```

`availableShaders()` 只报告 package 中已有的精确键，不定义优先级。应用应根据 QRhi 后端、版本支持和部署策略决定候选顺序。

## 7. 比较、排序和哈希

### `operator==` / `operator!=`

按 source、sourceVersion 和 sourceVariant 比较。版本号和 `GlslEs` flags 任一不同，key 就不同。

### `operator<`

为有序容器提供严格弱序，适合 `QMap<QShaderKey, ...>`。不要把排序结果解释成 shader 后端优先级。

### `qHash`

允许把 key 放入 `QHash` 或 `QSet`。哈希是进程内容器索引工具，不是稳定文件 ID，也不是安全指纹。

## 8. 与 `QShader` 的边界

`QShaderKey` 只描述“找哪一条”，不保存：

- shader code；
- shader entry point；
- shader stage；
- 反射 description；
- native binding map。

这些数据由 `QShader`、`QShaderCode` 和其他类型分别保存。删除某个 key 的 shader code 也不应被理解为自动清理该 key 上的全部附加数据，具体要看 `QShader` 的删除 API 语义。

## 9. 常见误区

- 把默认构造 key 当作 wildcard。
- 只用 source 查找，忽略版本和 variant。
- 把 source 当成 vertex/fragment stage。
- 用 `operator<` 选择“最新”或“最兼容” shader。
- 只改 variant 字段伪造 batchable 或 Metal compute shader。
- 认为 key 构造会验证 package 中是否存在代码。
- 修改已经作为容器 key 使用的对象后继续依赖旧索引。
- 用 `qHash` 结果做跨版本资产指纹。

## API 速查表
| 类别 | API | 作用 | 关键边界 |
| --- | --- | --- | --- |
| 构造 | `QShaderKey()` | 创建默认 key | 默认是 SPIR-V/版本 100/standard，不是通配符 |
| 构造 | `QShaderKey(Source, const QShaderVersion &, Variant)` | 创建精确 key | 不检查 package，不编译代码 |
| 查询 | `source() const` | 读取代码格式 | 不是 shader stage |
| 修改 | `setSource(Source)` | 设置代码格式 | 会使 key 变成另一个值 |
| 查询 | `sourceVersion() const` | 读取版本和 flags | ES 标志也属于 key |
| 修改 | `setSourceVersion(const QShaderVersion &)` | 设置版本维度 | 不自动 fallback |
| 查询 | `sourceVariant() const` | 读取代码变体 | 不是 stage |
| 修改 | `setSourceVariant(Variant)` | 设置变体维度 | 不会生成特殊代码 |
| 查询 | `QShader::availableShaders()` | 获取 package 中已有 key | 顺序不是优先级 |
| 查询 | `QShader::shader(const QShaderKey &)` | 按精确 key 取代码 | 缺失时为空，不自动匹配 |
| 比较 | `operator==` | 比较三个 key 维度 | 不是代码内容比较 |
| 比较 | `operator!=` | 相等比较的反值 | 仍是值比较 |
| 排序 | `operator<` | 支持有序容器 | 不是兼容性排序 |
| 哈希 | `qHash(const QShaderKey &, size_t)` | 支持 QHash/QSet | 不是稳定资产 ID |

---

### 一句话总结

`QShaderKey` 是 `QShader` 多后端代码的精确索引，必须同时匹配 source、`QShaderVersion` 和 variant；默认 key 不是通配符，列表顺序和 `<` 排序也都不能替应用做后端优先级或版本回退决策。
