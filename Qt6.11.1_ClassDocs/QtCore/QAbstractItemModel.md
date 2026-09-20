# QAbstractItemModel
> Qt 6.11.1 · Qt Core · 来自 `QAbstractItemModel`

## 作用定位
`QAbstractItemModel` 是 Qt Model/View 数据模型的核心接口。它用 `QModelIndex` 表示二维或树形位置，并用 roles 提供显示、编辑、排序等不同数据视图。

## API 速查
| API | 是做什么的 |
|---|---|
| `index()` / `parent()` | 建立模型索引和树父子关系。|
| `rowCount()` / `columnCount()` | 报告结构大小。|
| `data()` | 按索引和 role 返回数据。|
| `setData()` | 写入可编辑数据并发出变化通知。|
| `headerData()` | 返回表头数据。|
| `flags()` | 声明选择、编辑、拖放能力。|
| `beginInsertRows()` / `endInsertRows()` | 正确通知行插入。|
| `dataChanged()` | 通知既有单元格的数据或角色改变。|

## 使用场景
为 `QTableView`、`QTreeView`、QML view 或代理模型暴露业务数据。所有结构变更必须包在对应 begin/end 调用之间。

## 常见坑与经验
- `QModelIndex` 不应长期当作稳定 ID 保存；重排/重置后可能失效，需使用 `QPersistentModelIndex` 或业务键。
- `dataChanged()` 的索引范围和 roles 要准确，范围过大造成无谓刷新，遗漏则界面不更新。
- begin/end 中间不得让 view 看到未完成状态。

## 知识点覆盖
Model/View、QModelIndex、roles、树模型、变更通知、持久索引、数据绑定。
