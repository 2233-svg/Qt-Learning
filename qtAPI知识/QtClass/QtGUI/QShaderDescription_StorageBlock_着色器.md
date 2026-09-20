# Qt QShaderDescription::StorageBlock：storage buffer 与运行时数组布局

> 适用版本：Qt 6.11.1  
> 头文件：`#include <rhi/qshaderdescription.h>`  
> 所属模块：`Qt6::Gui`，RHI 相关 API 的兼容性保证有限  
> 定位：`QShaderDescription` 的嵌套聚合结构体，since Qt 6.6

## 1. 它解决什么问题

`QShaderDescription::StorageBlock` 描述 shader 的 storage block，例如 GLSL 的 SSBO。相比 `UniformBlock`，它还需要表达：

- 可确定的前缀大小 `knownSize`；
- 运行时数组元素步长 `runtimeArrayStride`；
- shader 限定符 `qualifierFlags`；
- 资源 `binding` 和 `descriptorSet`；
- 成员的递归布局。

它解决的是“如何识别 storage buffer 的绑定和前缀布局，以及如何处理 unsized/runtime array”的问题。

## 2. 结构定义

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

实际应用从 `QShaderDescription::storageBlocks()` 读取，不需要手工创建：

```cpp
for (const auto &block : desc.storageBlocks()) {
    qDebug() << block.blockName
             << block.instanceName
             << "binding =" << block.binding
             << "set =" << block.descriptorSet
             << "knownSize =" << block.knownSize
             << "runtimeStride =" << block.runtimeArrayStride;
}
```

## 3. 字段语义

| 字段 | 含义 | 关键边界 |
| --- | --- | --- |
| `blockName` | storage block 名称 | shader 侧 block 名称 |
| `instanceName` | block 实例名称 | 可能为空，取决于 shader 声明 |
| `knownSize` | 已知的 block 前缀大小 | 不包含运行时数组无法确定的尾部 |
| `binding` | 资源 binding | 未提供时为 `-1` |
| `descriptorSet` | descriptor set | 未提供时为 `-1` |
| `members` | 成员布局 | 成员是递归的 `BlockVariable` |
| `runtimeArrayStride` | 运行时数组元素步长 | 没有 runtime array 或未知时可能为 `0` |
| `qualifierFlags` | storage block 限定符 | 不会自动实现同步和屏障 |

`knownSize` 不是实际 buffer 的完整字节数。应用创建 buffer 时，实际大小还要由数据量决定，并满足 shader 访问和后端限制。

## 4. 运行时数组的识别

典型的 unsized SSBO 成员可能表现为：

```text
member.arrayDims == [0]
member.size == 0
storageBlock.runtimeArrayStride > 0
```

解释方式是：

```text
固定前缀: [0, knownSize)
运行时数组第 i 项: arrayBase + i * runtimeArrayStride
实际元素数量: 由实际 buffer 大小和应用协议决定
```

不能把 `arrayDims[0] == 0` 当成“数组长度为 0”。它表示 shader 没有在编译时固定尾部数组长度。

## 5. `QualifierFlags`

```cpp
enum QualifierFlag {
    QualifierReadOnly = 1 << 0,
    QualifierWriteOnly = 1 << 1,
    QualifierCoherent = 1 << 2,
    QualifierVolatile = 1 << 3,
    QualifierRestrict = 1 << 4
};
```

这是可组合 flags：

```cpp
if (block.qualifierFlags.testFlag(QShaderDescription::QualifierReadOnly)) {
    // shader 声明为只读
}
```

各 flag 的含义：

- `QualifierReadOnly`：shader 侧只读；
- `QualifierWriteOnly`：shader 侧只写；
- `QualifierCoherent`：声明 coherent 访问语义；
- `QualifierVolatile`：声明 volatile 访问语义；
- `QualifierRestrict`：声明 restrict 访问语义。

反射只保存声明，不会自动替你插入 memory barrier、选择 buffer usage flag 或处理跨 dispatch 同步。

## 6. 与 `BlockVariable` 和 QRhi 的协作

`members` 中的每项都使用 `BlockVariable`：

- `offset` 用于定位 block 内成员；
- `arrayStride` 用于数组元素；
- `matrixStride` 和 `matrixIsRowMajor` 用于矩阵；
- `structMembers` 用于嵌套结构体。

资源绑定则使用 `binding` 与 `descriptorSet`。应用可据此创建或检查 QRhi resource binding，但仍需验证 buffer 的 usage、大小、访问权限以及目标后端能力。

## 7. 常见误区

- 把 `knownSize` 当成实际 SSBO 总大小：runtime array 尾部不在其中。
- 把 `runtimeArrayStride` 当成整个数组大小：它只是单个元素步长。
- 把 `arrayDims == [0]` 当成空数组。
- 把 `binding` 当成 vertex location。
- 看到 `QualifierCoherent` 就以为 Qt 自动处理同步。
- 忽略 `descriptorSet == -1` 的未提供语义。
- 直接把成员列表按 C++ struct 连续布局写入 buffer。
- 认为 storage block 一定是可写：还要读取 qualifier 和 shader 声明。

## 8. 相关非成员运算符

### `bool operator==(const QShaderDescription::StorageBlock &, const QShaderDescription::StorageBlock &) noexcept`

比较 block 名称、实例名、大小、绑定、成员、runtime stride 和 qualifier flags。适合测试反射变化，不代表两个 QRhi buffer 已经兼容。

### `bool operator!=(const QShaderDescription::StorageBlock &, const QShaderDescription::StorageBlock &) noexcept`

返回相等比较的逻辑反值。

## API 速查表

| 类别 | API/字段 | 作用 | 关键边界 |
| --- | --- | --- | --- |
| 字段 | `blockName` | storage block 名称 | shader 侧名称 |
| 字段 | `instanceName` | block 实例名称 | 可能为空 |
| 字段 | `knownSize` | 已知前缀大小 | 不含 runtime array 尾部 |
| 字段 | `binding` | 资源 binding | 缺失时为 `-1` |
| 字段 | `descriptorSet` | 资源 set | 缺失时为 `-1` |
| 字段 | `members` | 成员布局列表 | 使用 `BlockVariable` 递归解释 |
| 字段 | `runtimeArrayStride` | runtime array 单元素步长 | 不是整个数组大小 |
| 字段 | `qualifierFlags` | read/write/coherent 等限定符 | 不自动处理同步 |
| 查询 | `storageBlocks()` | 获取 storage block 列表 | 反射不等于 buffer 创建成功 |
| 比较 | `operator==` | 比较 block 描述 | 不是 QRhi 资源兼容性证明 |
| 比较 | `operator!=` | 相等比较的反值 | 仍是值比较 |

---

### 一句话总结

`StorageBlock` 的核心是“绑定 + 已知前缀 + runtime array stride + 递归成员布局”：`knownSize` 不包含无法预知的数组尾部，`qualifierFlags` 只是 shader 声明，实际 buffer 大小和同步仍由应用与后端负责。
