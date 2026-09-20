# Qt QShaderDescription::BlockVariable：uniform/storage 成员布局

> 适用版本：Qt 6.11.1  
> 头文件：`#include <rhi/qshaderdescription.h>`  
> 所属模块：`Qt6::Gui`，RHI 相关 API 的兼容性保证有限  
> 定位：`QShaderDescription` 的嵌套聚合结构体，since Qt 6.6

## 1. 它解决什么问题

`QShaderDescription::BlockVariable` 描述 uniform block、storage block 或 push constant 中的一个成员。它把 shader 编译器计算出的成员布局暴露出来，包括：

- 名称和 `VariableType`；
- 相对所属 block 或 struct 起点的 `offset`；
- 已知大小 `size`；
- 数组维度和数组元素步长；
- 矩阵步长与主序；
- 嵌套结构体成员。

它解决的是“CPU 侧如何按 shader 的布局填充 buffer”以及“工具如何展示 shader 反射结构”的问题。它不是 C++ 结构体字段，也不是运行时 GPU buffer view。

## 2. 头文件和创建方式

```cpp
#include <rhi/qshaderdescription.h>
```

这是公开结构体，支持聚合初始化：

```cpp
QShaderDescription::BlockVariable member{
    QByteArrayLiteral("model"),
    QShaderDescription::Mat4,
    0,
    64,
    {},
    0,
    16,
    false,
    {}
};
```

实际应用通常读取 `QShaderDescription::UniformBlock::members`、`StorageBlock::members` 或 `PushConstantBlock::members`，而不是手工创建它。

## 3. 字段语义

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

| 字段 | 含义 | 边界 |
| --- | --- | --- |
| `name` | shader 成员名称 | 可能是变量名或匿名/生成器使用的名称，不是 C++ 标识符契约 |
| `type` | 成员类型 | `Struct` 时要递归读 `structMembers` |
| `offset` | 相对所属容器起点的字节偏移 | 是 shader 布局偏移，不等于 C++ `offsetof()` |
| `size` | 当前成员的已知大小 | 运行时数组等无法确定总长的成员可能为 `0` |
| `arrayDims` | 数组各维长度 | `0` 可表示运行时数组维度 |
| `arrayStride` | 相邻数组元素之间的步长 | 非数组或未提供时可能为 `0` |
| `matrixStride` | 矩阵行/列之间的步长 | 必须结合 `matrixIsRowMajor` 和类型解释 |
| `matrixIsRowMajor` | 是否 row-major | `false` 通常表示 column-major 语义 |
| `structMembers` | 嵌套 struct 成员 | 可能继续嵌套，读取时递归 |

头文件给出的默认值很重要：`type` 默认为 `Unknown`，数值字段默认为 `0`，数组列表为空，主序默认为 `false`。这表示“没有额外布局信息”时的默认状态，不代表一个实际 shader 成员必然位于 offset 0 或大小为 0。

## 4. 实际使用：递归打印布局

```cpp
void dumpMember(const QShaderDescription::BlockVariable &member,
                int depth = 0)
{
    const QByteArray indent(depth * 2, ' ');
    qDebug().noquote()
        << indent + member.name
        << "offset =" << member.offset
        << "size =" << member.size
        << "type =" << member.type
        << "arrayDims =" << member.arrayDims;

    if (member.type == QShaderDescription::Struct) {
        for (const auto &nested : member.structMembers)
            dumpMember(nested, depth + 1);
    }
}
```

如果成员位于 block 中，最终地址通常是：

```text
blockBase + member.offset
```

如果成员是嵌套 struct，则是：

```text
blockBase + outer.offset + inner.offset
```

数组元素还要加上 `index * arrayStride`；矩阵元素要结合 `matrixStride` 和主序计算。不要把 `size` 当成下一个成员的起始位置，padding 可能使二者不同。

## 5. 数组、矩阵和运行时数组

### 5.1 固定长度数组

固定长度数组通常在 `arrayDims` 中有正数维度，`arrayStride` 表示元素间距。数组的总占用不一定等于 `elementSize * count`，因为 shader 布局可能加入对齐和 padding。

### 5.2 运行时数组

当 `arrayDims` 某一维为 `0` 时，应把它视为运行时数组候选。此时：

- 总数组长度由实际 buffer 大小决定；
- `size` 可能为 `0`；
- 对 storage block，通常还要结合 `StorageBlock::runtimeArrayStride`；
- 不能通过 `arrayDims[0]` 计算出实际元素数量。

### 5.3 矩阵

矩阵有独立的元素步长。`matrixIsRowMajor == false` 通常对应 column-major，`true` 对应 row-major。CPU 侧不能只把矩阵看成连续的 `float` 数组后直接 `memcpy`，尤其是矩阵行列数不规则或布局含 padding 时。

## 6. 与其他类型的关系

`BlockVariable` 只描述成员，完整上下文来自外层结构：

| 外层类型 | `BlockVariable` 的作用 |
| --- | --- |
| `UniformBlock` | 描述 uniform buffer 的成员布局 |
| `StorageBlock` | 描述 SSBO 等 storage buffer 的成员布局 |
| `PushConstantBlock` | 描述 push constant 的成员布局 |
| `BlockVariable` | 通过 `structMembers` 递归描述嵌套 struct |

它与 `InOutVariable` 中的 `structMembers` 不同：后者描述 stage input/output 结构体的字段，不一定有 buffer offset；`BlockVariable` 的 `offset` 专门服务于 block 布局。

## 7. 常见误区

- 把 `offset` 当成 C++ `offsetof()`：C++ 对齐和 shader 对齐可能不同。
- 看到 `size == 0` 就认为成员为空：运行时数组和未提供布局信息都可能使用 0。
- 忽略 `arrayStride`：数组元素可能包含 padding。
- 忽略 `matrixStride`：矩阵的行列元素不一定紧密排列。
- 只读取一层 `structMembers`：结构体可以递归嵌套。
- 把 `arrayDims == [0]` 当成长度为零的数组：它更可能表示 runtime-sized array。
- 手工构造记录后期待 Qt 自动把它写回 `QShaderDescription`：公开 API 没有这种 setter 工作流。

## 8. 相关非成员运算符

### `bool operator==(const QShaderDescription::BlockVariable &, const QShaderDescription::BlockVariable &) noexcept`

按值比较两个成员描述，包括名称、类型、布局字段、数组信息和嵌套成员。它适合测试反射结果、比较缓存是否变化，不代表两个真实 GPU buffer 已经兼容。

### `bool operator!=(const QShaderDescription::BlockVariable &, const QShaderDescription::BlockVariable &) noexcept`

返回相等比较的逻辑反值。

## API 速查表

| 类别 | API/字段 | 作用 | 关键边界 |
| --- | --- | --- | --- |
| 字段 | `name` | shader 成员名 | 不是 C++ 字段名契约 |
| 字段 | `type` | 成员类型 | `Struct` 时递归读 `structMembers` |
| 字段 | `offset` | 相对容器起点偏移 | 不等于 C++ `offsetof()` |
| 字段 | `size` | 已知成员大小 | 运行时数组可能为 `0` |
| 字段 | `arrayDims` | 数组维度 | `0` 可能表示运行时维度 |
| 字段 | `arrayStride` | 数组元素步长 | 不能用元素 `size` 代替 |
| 字段 | `matrixStride` | 矩阵行/列步长 | 需结合主序解释 |
| 字段 | `matrixIsRowMajor` | 矩阵主序 | 影响 CPU 填充顺序 |
| 字段 | `structMembers` | 嵌套成员 | 应递归读取 |
| 比较 | `operator==` | 比较两个成员描述 | 是元数据比较，不是 GPU 兼容性证明 |
| 比较 | `operator!=` | 相等比较的反值 | 仍是值比较 |

---

### 一句话总结

`BlockVariable` 是 shader buffer 布局的递归节点：`offset`、`size`、数组 stride、矩阵 stride 和 `structMembers` 一起决定 CPU 侧如何定位成员；默认的 `0` 和空列表表示信息缺失或不适用，不能直接当成真实布局结论。
