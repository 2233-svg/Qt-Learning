# QModelRoleData
> Qt 6.11.1 · Qt Core · 来自 `QModelRoleData`

## 作用定位
`QModelRoleData` 将一个 role 编号和对应 `QVariant` 值打包，用于模型一次为同一索引填充多个角色数据。

## API 速查
| API | 是做什么的 |
|---|---|
| `role()` | 读取该数据项对应 role。|
| `data()` | 读取或写入该 role 的 QVariant 值。|
| `clearData()` | 清空当前保存的值。|

## 使用场景
模型重实现 `multiData()` 时，批量填充 DisplayRole、DecorationRole、UserRole 等多个角色，降低 view 多次回调成本。

## 常见坑与经验
- role 数字必须与模型 `roleNames()` 和 `data()` 语义一致。
- 缓存批量 role 数据时，要在模型变更后正确失效，避免显示旧状态。

## 知识点覆盖
模型 role、QVariant、批量数据提供、视图性能、缓存一致性。
