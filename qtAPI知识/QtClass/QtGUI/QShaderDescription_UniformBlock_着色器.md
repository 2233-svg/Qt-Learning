# Qt QShaderDescription::UniformBlock：uniform buffer 布局描述

> 适用版本：Qt 6.11.1  
> 头文件：`#include <rhi/qshaderdescription.h>`  
> 所属模块：`Qt6::Gui`，RHI 相关 API 的兼容性保证有限  
> 定位：`QShaderDescription` 的嵌套聚合结构体，since Qt 6.6

## 1. 它解决什么问题

`QShaderDescription::UniformBlock` 描述 shader 使用的 uniform block，包括名称、实例相关名称、布局大小、资源绑定和递归成员。它让应用能够：

- 找出 shader 需要哪些 uniform buffer；
- 确认 binding 和 descriptor set；
- 按反射 offset 填充 CPU 侧 buffer；
- 在 shader 变更后检查布局是否变化。

它不是实际的 `QRhiBuffer`，也不会替应用创建 resource binding。

## 2. 结构定义

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

头文件中 `structName` 字段旁有 `// instanceName` 注释。阅读和跨语言工具中应把它理解为 block 实例名称相关字段，不要把它误认为 C++ 的类型名。

## 3. 字段语义

| 字段 | 含义 | 边界 |
| --- | --- | --- |
| `blockName` | uniform block 名称 | shader 侧 block 名 |
| `structName` | 实例名称相关字段 | 头文件注释标为 instanceName，可能为空 |
| `size` | block 布局大小 | 不等于 C++ `sizeof` |
| `binding` | uniform buffer binding | 未提供时为 `-1` |
| `descriptorSet` | descriptor set | 未提供时为 `-1` |
| `members` | block 成员和布局 | 使用 `BlockVariable` 递归读取 |

默认对象的 `size == 0`、binding/set 为 `-1`、members 为空。它表示空记录或未提供信息，不代表一个可直接绑定的零大小 uniform buffer。

## 4. 实际使用场景

### 4.1 列出 shader 资源

```cpp
for (const auto &block : desc.uniformBlocks()) {
    qDebug() << "block =" << block.blockName
             << "instance =" << block.structName
             << "binding =" << block.binding
             << "set =" << block.descriptorSet
             << "size =" << block.size;
}
```

### 4.2 按反射布局写入 buffer

成员地址通常是：

```text
bufferBase + member.offset
```

嵌套结构体、数组和矩阵还要递归加上父 offset 并使用各自 stride。`size` 只能作为该层级布局大小参考，不能用来推导每个成员连续排列。

### 4.3 创建 QRhi 资源绑定前检查

应用可以用 `binding` 和 `descriptorSet` 检查 `QRhiShaderResourceBinding` 的布局，用 `size` 检查 buffer 容量。但 shader 反射不会自动验证：

- 实际 buffer 的 usage；
- 动态 offset 是否满足对齐；
- 后端允许的 uniform buffer 范围；
- CPU 侧编码的类型和矩阵主序。

## 5. 布局字段的正确解释

`members` 中的 `BlockVariable` 需要按以下顺序处理：

1. 先加父成员的 `offset`；
2. 如果有数组，用 `arrayStride` 定位元素；
3. 如果有矩阵，用 `matrixStride` 和 `matrixIsRowMajor` 定位行列；
4. 如果 `type == Struct`，递归处理 `structMembers`；
5. 使用 shader 的类型和布局规则处理对齐，而不是直接依赖 C++ 自然布局。

`arrayDims` 中出现 `0` 时，可能是 runtime array，uniform block 一般不应依赖这种布局；如果出现，应按生成器和目标语言规则核对，不要直接计算固定长度。

## 6. 与其他 block 类型的区别

| 类型 | 主要特征 |
| --- | --- |
| `UniformBlock` | 绑定 uniform buffer，通常保存只读常量数据 |
| `StorageBlock` | 有 `knownSize`、runtime array stride 和 qualifier flags |
| `PushConstantBlock` | 没有普通 binding/set 字段，后端支持需单独确认 |

三者都使用 `BlockVariable` 表示成员，但外层资源语义不同。

## 7. 常见误区

- 把 `blockName`、`structName` 和 C++ 类型名混为一谈。
- 把 `size` 当成 C++ `sizeof`。
- 把 binding 和 descriptor set 合成一个整数。
- 忽略成员 padding、矩阵 stride 和数组 stride。
- 只按 block 名匹配资源，不检查 binding/set。
- 把空 block 记录的默认值当成真实 shader 布局。
- 修改 `UniformBlock` 结构体后期待原 `QShaderDescription` 自动更新。

## 8. 相关非成员运算符

### `bool operator==(const QShaderDescription::UniformBlock &, const QShaderDescription::UniformBlock &) noexcept`

比较 block 的名称、大小、绑定、descriptor set 和成员列表。它适合检查反射缓存或测试生成结果，不表示实际 uniform buffer 已经满足后端约束。

### `bool operator!=(const QShaderDescription::UniformBlock &, const QShaderDescription::UniformBlock &) noexcept`

返回相等比较的逻辑反值。

## API 速查表

| 类别 | API/字段 | 作用 | 关键边界 |
| --- | --- | --- | --- |
| 字段 | `blockName` | uniform block 名称 | shader 侧名称 |
| 字段 | `structName` | 实例名称相关字段 | 头文件注释标为 instanceName |
| 字段 | `size` | block 布局大小 | 不等于 C++ `sizeof` |
| 字段 | `binding` | uniform buffer binding | 缺失时为 `-1` |
| 字段 | `descriptorSet` | descriptor set | 缺失时为 `-1` |
| 字段 | `members` | 成员布局列表 | 递归使用 `BlockVariable` |
| 查询 | `uniformBlocks()` | 获取 uniform block 列表 | 反射不替代 QRhi 资源验证 |
| 比较 | `operator==` | 比较 block 值内容 | 不是 buffer 兼容性证明 |
| 比较 | `operator!=` | 相等比较的反值 | 仍是值比较 |

---

### 一句话总结

`UniformBlock` 是 shader uniform buffer 的反射入口：用 `binding`/`descriptorSet` 找资源，用 `members` 的 offset 和 stride 填充数据；`size` 是 shader 布局大小，不是 C++ `sizeof`，默认的 `-1` 和 `0` 必须按“未提供”处理。
