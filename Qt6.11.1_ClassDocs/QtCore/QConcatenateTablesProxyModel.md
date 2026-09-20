# QConcatenateTablesProxyModel
> Qt 6.11.1 · Qt Core · 来自 `QConcatenateTablesProxyModel`

## 作用定位
`QConcatenateTablesProxyModel` 将多个结构相同的表模型按行纵向拼接为一个代理模型，统一提供给单个 view。

## API 速查
| API | 是做什么的 |
|---|---|
| `addSourceModel()` | 在末尾加入一个源表模型。|
| `removeSourceModel()` | 移除指定源模型。|
| `sourceModels()` | 读取当前源模型列表。|
| `mapToSource()` | 将拼接后索引映射回原模型。|
| `mapFromSource()` | 将原模型索引映射到拼接模型。|
| `sourceModel()` | 兼容代理模型接口，通常不表示唯一源。|

## 使用场景
把不同数据源但列结构相同的日志、查询结果或分区表显示在同一个 `QTableView` 中。

## 常见坑与经验
- 所有源模型应具有一致列数、列顺序和 role 语义；代理不会替你语义对齐。
- 编辑或选择操作要通过映射回具体源模型，不能假定拼接行号就是源行号。

## 知识点覆盖
表代理、模型拼接、索引映射、列契约、多数据源视图。
