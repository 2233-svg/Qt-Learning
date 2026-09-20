# Qt QShaderDescription::BuiltinVariable：内建变量反射记录

> 适用版本：Qt 6.11.1  
> 头文件：`#include <rhi/qshaderdescription.h>`  
> 所属模块：`Qt6::Gui`，RHI 相关 API 的兼容性保证有限  
> 定位：`QShaderDescription` 的嵌套聚合结构体，since Qt 6.6

## 1. 它解决什么问题

`QShaderDescription::BuiltinVariable` 描述 shader 使用的内建变量，例如顶点位置、顶点 ID、fragment 坐标、工作组 ID 和 tessellation 坐标。它把两个维度放在一条反射记录中：

- `type`：这个变量在 shader 规范中的内建语义；
- `varType`：该内建变量实际使用的 `VariableType`；
- `arrayDims`：变量是否是数组以及每一维大小。

它解决的是“识别 shader 的特殊内建接口”的问题。内建变量不是普通用户声明的 `location` 输入，因此不能用 `InOutVariable` 的 location 逻辑处理。

## 2. 结构定义与初始化

```cpp
struct BuiltinVariable {
    BuiltinType type;
    VariableType varType;
    QList<int> arrayDims;
};
```

该结构体的两个枚举字段没有类内默认初始化。应优先使用值初始化：

```cpp
QShaderDescription::BuiltinVariable builtin{};
```

这样 `type` 和 `varType` 会从零值开始，`arrayDims` 为空。直接写：

```cpp
QShaderDescription::BuiltinVariable builtin;
```

对于聚合中的枚举字段，不应依赖未初始化值。实际应用通常读取 `inputBuiltinVariables()` 或 `outputBuiltinVariables()`，不手工构造它。

## 3. 字段语义

| 字段 | 含义 | 关键边界 |
| --- | --- | --- |
| `type` | builtin 语义，如 `PositionBuiltin` | 不是普通 location，也不是变量数据类型 |
| `varType` | builtin 的实际变量类型 | 用于判断标量、向量、数组元素类型 |
| `arrayDims` | 数组维度 | 维度值为 0 时要按生成器的 runtime array 语义处理 |

`type` 与 `varType` 不能互换。例如 `PositionBuiltin` 表示位置语义，`Vec4` 才表示它的变量类型。

## 4. `BuiltinType` 语义速查

| 枚举值 | 语义 |
| --- | --- |
| `PositionBuiltin` | 顶点位置，如 `gl_Position` |
| `PointSizeBuiltin` | 点大小 |
| `ClipDistanceBuiltin` | clip distance |
| `CullDistanceBuiltin` | cull distance |
| `VertexIdBuiltin` | 顶点 ID |
| `InstanceIdBuiltin` | 实例 ID |
| `PrimitiveIdBuiltin` | 图元 ID |
| `InvocationIdBuiltin` | invocation ID |
| `LayerBuiltin` | layer |
| `ViewportIndexBuiltin` | viewport index |
| `TessLevelOuterBuiltin` | tessellation 外侧级别 |
| `TessLevelInnerBuiltin` | tessellation 内侧级别 |
| `TessCoordBuiltin` | tessellation 坐标 |
| `PatchVerticesBuiltin` | patch 顶点数 |
| `FragCoordBuiltin` | fragment 坐标 |
| `PointCoordBuiltin` | point 坐标 |
| `FrontFacingBuiltin` | 正面判断 |
| `SampleIdBuiltin` | sample ID |
| `SamplePositionBuiltin` | sample 位置 |
| `SampleMaskBuiltin` | sample mask |
| `FragDepthBuiltin` | fragment 深度 |
| `NumWorkGroupsBuiltin` | compute 工作组总数 |
| `WorkgroupSizeBuiltin` | compute 工作组尺寸 |
| `WorkgroupIdBuiltin` | 工作组 ID |
| `LocalInvocationIdBuiltin` | 工作组内 invocation ID |
| `GlobalInvocationIdBuiltin` | 全局 invocation ID |
| `LocalInvocationIndexBuiltin` | 工作组内线性 invocation 索引 |
| `VertexIndexBuiltin` | vertex index |
| `InstanceIndexBuiltin` | instance index |
| `ViewIndexBuiltin` | view index |

这些枚举值与 SPIR-V builtin 编号保持对应关系。应用代码应使用枚举名，不要依赖自定义的连续编号。

## 5. 实际使用场景

```cpp
void inspectBuiltins(const QShaderDescription &desc)
{
    for (const auto &builtin : desc.inputBuiltinVariables()) {
        qDebug() << "input builtin =" << builtin.type
                 << "variable type =" << builtin.varType
                 << "array dims =" << builtin.arrayDims;
    }

    for (const auto &builtin : desc.outputBuiltinVariables()) {
        if (builtin.type == QShaderDescription::PositionBuiltin)
            qDebug() << "shader writes position as" << builtin.varType;
    }
}
```

常见用途包括：

- 确认 vertex shader 是否写出 position；
- 检查 compute shader 是否使用工作组相关 builtin；
- 生成 shader 反射面板；
- 对 tessellation、multiview 或多重采样接口做能力检查。

## 6. 输入和输出方向

`BuiltinVariable` 自身没有 direction 字段。方向来自外层查询：

- `QShaderDescription::inputBuiltinVariables()`：输入侧 builtin；
- `QShaderDescription::outputBuiltinVariables()`：输出侧 builtin。

不要根据 builtin 名称猜输入输出。例如 `PositionBuiltin` 在某些阶段表现为输出，在其他阶段可能作为输入接口；应以所属列表和 shader stage 为准。

## 7. 常见误区

- 把 `type` 当成 `VariableType`：前者是语义，后者是数据类型。
- 给 builtin 分配普通 location：内建变量不通过普通 location 暴露。
- 假设每个 builtin 都能在所有 shader stage 使用：语义与阶段有关。
- 直接默认构造后读取字段：两个枚举字段没有类内默认值，应用应使用 `{}`。
- 只看 builtin 是否存在，不检查 `varType` 和数组维度：类型不匹配仍可能导致接口错误。
- 把 `BuiltinVariable` 当成可修改 shader 的对象：它只是反射值记录。

## 8. 相关非成员运算符

### `bool operator==(const QShaderDescription::BuiltinVariable &, const QShaderDescription::BuiltinVariable &) noexcept`

比较 `type`、`varType` 和 `arrayDims` 的值。适合测试反射缓存或比较两个 shader 描述，不表示两个 shader stage 的接口一定可连接。

### `bool operator!=(const QShaderDescription::BuiltinVariable &, const QShaderDescription::BuiltinVariable &) noexcept`

返回相等比较的逻辑反值。

## API 速查表

| 类别 | API/字段 | 作用 | 关键边界 |
| --- | --- | --- | --- |
| 字段 | `type` | 标识 builtin 语义 | 不是 location，也不是数据类型 |
| 字段 | `varType` | 标识 builtin 的实际类型 | 与 `type` 配合解释 |
| 字段 | `arrayDims` | 标识数组维度 | 不能忽略 0 维度的特殊语义 |
| 查询 | `inputBuiltinVariables()` | 从外层获取输入 builtin | 方向由列表决定 |
| 查询 | `outputBuiltinVariables()` | 从外层获取输出 builtin | 方向由列表决定 |
| 比较 | `operator==` | 比较 builtin 反射记录 | 不是 stage 兼容性检查 |
| 比较 | `operator!=` | 相等比较的反值 | 仍是值比较 |

---

### 一句话总结

`BuiltinVariable` 用 `type` 表达“哪个内建语义”，用 `varType` 表达“它是什么数据类型”，由输入/输出列表表达方向；它不使用普通 location，且应通过值初始化避免未初始化的枚举字段。
