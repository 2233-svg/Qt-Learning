# QAbstractListModel
> Qt 6.11.1 · Qt Core · 来自 `QAbstractListModel`

## 作用定位
`QAbstractListModel` 是单列列表模型的便利基类，减少实现普通列表时的列处理负担。

## API 速查
| API | 是做什么的 |
|---|---|
| `rowCount()` | 返回项目数量。|
| `data()` | 返回每行各 role 数据。|
| `roleNames()` | 为 QML 暴露自定义 role 名。|
| `setData()` | 实现可编辑列表。|
| `beginInsertRows()` / `endInsertRows()` | 通知列表插入。|

## 使用场景
QML `ListView` 的业务数据、简单设置列表、搜索结果。

## 常见坑与经验
- QML 的 delegate 通过 `roleNames()` 使用角色名；只返回数字 role 会让 QML 使用困难。
- 对现有数据改动用 `dataChanged()`，不要每次都 `beginResetModel()`。

## 知识点覆盖
列表模型、QML roles、增量更新、编辑、重置成本。
