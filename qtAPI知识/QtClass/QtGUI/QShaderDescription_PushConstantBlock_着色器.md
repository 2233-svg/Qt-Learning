# Qt QShaderDescription::PushConstantBlock：push constant 布局描述

> 适用版本：Qt 6.11.1  
> 头文件：`#include <rhi/qshaderdescription.h>`  
> 所属模块：`Qt6::Gui`，RHI 相关 API 的兼容性保证有限  
> 定位：`QShaderDescription` 的嵌套聚合结构体，since Qt 6.6

## 1. 它解决什么问题

`QShaderDescription::PushConstantBlock` 描述 shader 中的 push constant 区域：

- `name`：区域名称；
- `size`：已知布局大小；
- `members`：每个成员的 `BlockVariable` 布局。

它提供的是 shader 反射信息，用于检查 shader 接口和展示布局。它不是可直接写入的 CPU 缓冲区，也不意味着所有 QRhi 后端都暴露了同等的 push constant 更新能力。

## 2. 结构定义

```cpp
struct PushConstantBlock {
    QByteArray name;
    int size = 0;
    QList<BlockVariable> members;
};
```

字段默认值是有效的空状态：

- `name` 为空；
- `size` 为 `0`；
- `members` 为空。

实际应用通过 `QShaderDescription::pushConstantBlocks()` 读取：

```cpp
for (const auto &block : desc.pushConstantBlocks()) {
    qDebug() << block.name << block.size;
    for (const auto &member : block.members)
        qDebug() << member.name << member.offset << member.size;
}
```

## 3. 字段语义

| 字段 | 含义 | 边界 |
| --- | --- | --- |
| `name` | push constant block 名称 | 是 shader 侧名称 |
| `size` | push constant 布局的已知大小 | 不是 C++ `sizeof`，缺失信息时可能为 0 |
| `members` | 成员和递归布局 | 使用 `BlockVariable` 的 offset/stride/structMembers |

push constant 没有 `binding` 和 `descriptorSet` 字段。不要为它虚构一个普通 uniform buffer binding。

## 4. 实际使用场景

### 4.1 反射检查

工具可以使用 `name`、`size` 和成员列表生成布局面板、检查 shader 修改是否影响 push constant 接口，或在构建阶段报告成员 offset 变化。

### 4.2 判断是否需要替代方案

如果应用面向多个 QRhi 后端，应把 `pushConstantBlocks()` 当作“shader 需要这类接口”的证据，再检查目标 Qt/RHI 能力。如果运行时无法更新 push constant，可把 shader 改为使用 uniform block，并重新生成 shader package。

### 4.3 成员定位

成员地址按 block 起点加上 `BlockVariable::offset` 计算；嵌套 struct、数组和矩阵继续使用成员自身的 offset/stride。不能根据 `size` 连续拼接成员，因为布局可能有 padding。

## 5. 与 uniform/storage block 的区别

| 类型 | 绑定字段 | 典型用途 | 可移植性关注 |
| --- | --- | --- | --- |
| `UniformBlock` | `binding`、`descriptorSet` | 常量数据 | 通常有 QRhi buffer 资源路径 |
| `StorageBlock` | `binding`、`descriptorSet` | 可读写或大容量数据 | 关注 runtime array 和 qualifier |
| `PushConstantBlock` | 无普通 binding | 小量快速参数 | 需确认 QRhi/后端支持 |

三者的成员都使用 `BlockVariable`，但外层资源模型不同。

## 6. 常见误区

- 看到反射记录就直接调用不存在的通用 push constant API。
- 把 `size` 当成 C++ 结构体大小。
- 忽略成员 `offset`、数组 stride 和矩阵 stride。
- 给 push constant 分配 uniform block binding。
- 只检查 block 是否存在，不检查目标后端和 Qt 版本能力。
- 手工创建结构体后期待自动修改 `QShaderDescription`；它没有公开的 block setter。

## 7. 相关非成员运算符

### `bool operator==(const QShaderDescription::PushConstantBlock &, const QShaderDescription::PushConstantBlock &) noexcept`

比较名称、大小和成员布局值。适合缓存或测试，不表示运行时资源能在目标后端创建。

### `bool operator!=(const QShaderDescription::PushConstantBlock &, const QShaderDescription::PushConstantBlock &) noexcept`

返回相等比较的逻辑反值。

## API 速查表

| 类别 | API/字段 | 作用 | 关键边界 |
| --- | --- | --- | --- |
| 字段 | `name` | push constant 名称 | 不等于 binding 名称 |
| 字段 | `size` | 已知布局大小 | 不是 C++ `sizeof`；可能为 0 |
| 字段 | `members` | 成员布局列表 | 递归使用 `BlockVariable` |
| 查询 | `pushConstantBlocks()` | 获取 push constant 描述 | 反射存在不等于 QRhi 一定支持更新 |
| 比较 | `operator==` | 比较 block 描述 | 不是后端能力检查 |
| 比较 | `operator!=` | 相等比较的反值 | 仍是值比较 |

---

### 一句话总结

`PushConstantBlock` 描述 shader 侧 push constant 的名称、大小和成员布局；它能告诉你 shader 需要什么，却不能替你保证 QRhi 后端提供对应更新路径，跨后端使用时要准备 uniform block 等替代方案。
