# QSqlTableModel
> Qt 6.11.1 · Qt SQL · 来自 `QSqlTableModel`

## 1. 先建立直觉

`QSqlTableModel` 是一张数据库表的可编辑 Model/View 模型。你指定表名、过滤条件、排序方式，调用 `select()` 后，它把表数据暴露给 `QTableView`；用户编辑后，模型按编辑策略把改动提交回数据库。

它适合“单表 CRUD”。复杂 JOIN、聚合、虚拟列更适合 `QSqlQueryModel` 或自定义模型。

## 2. 类说明

保留类说明：这些 API 来自 `QSqlTableModel`，属于 Qt SQL 模块，用于把 SQL 表映射成可编辑表格模型。

`QSqlTableModel` 继承 `QSqlQueryModel`，再增加表名、主键、编辑策略、插入更新删除和提交回滚逻辑。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `QSqlTableModel(parent, db)` | 创建绑定指定数据库连接的表模型。 |
| `setTable(tableName)` / `tableName()` | 设置或读取数据库表名；不会自动取数，需 `select()`。 |
| `select()` / `selectRow(row)` | 执行查询并填充模型，或刷新某一行。 |
| `setFilter(filter)` / `filter()` | 设置 SQL WHERE 片段，不含 `WHERE`。 |
| `setSort(column, order)` / `sort()` | 设置或立即应用排序。 |
| `setEditStrategy()` / `editStrategy()` | 设置编辑提交策略。 |
| `OnFieldChange` | 单元格变化立即提交。 |
| `OnRowChange` | 离开行时提交该行。 |
| `OnManualSubmit` | 缓存修改，直到 `submitAll()`。 |
| `setData()` / `data()` / `flags()` | Model/View 编辑和显示接口。 |
| `insertRows()`、`insertRecord()`、`setRecord()` | 插入或设置整行记录。 |
| `removeRows()` | 删除行，提交时机取决于编辑策略。 |
| `submit()` / `submitAll()` | 提交当前或全部缓存修改。 |
| `revert()`、`revertRow()`、`revertAll()` | 撤销缓存修改。 |
| `isDirty(index)` / `isDirty()` | 判断是否有未提交修改。 |
| `record()` / `record(row)` | 获取空记录模板或某行记录。 |
| `fieldIndex(name)` | 根据字段名找列号。 |
| `primaryKey()` / `primaryValues(row)` | 获取主键结构或某行主键值。 |
| `beforeInsert`、`beforeUpdate`、`beforeDelete`、`primeInsert` | 提交前或插入初始化信号。 |
| `insertRowIntoTable()`、`updateRowInTable()`、`deleteRowFromTable()` | 底层数据库操作钩子，派生类可重写。 |

## 4. 典型流程

```cpp
auto *model = new QSqlTableModel(this, db);
model->setTable("employee");
model->setEditStrategy(QSqlTableModel::OnManualSubmit);
model->setFilter("active = 1");
model->setSort(model->fieldIndex("name"), Qt::AscendingOrder);
model->select();

view->setModel(model);
```

提交：

```cpp
if (!model->submitAll()) {
    qWarning() << model->lastError();
    model->revertAll();
}
```

## 5. 使用场景

| 场景 | 建议 |
| --- | --- |
| 后台管理表格 | `OnManualSubmit`，用户确认后统一提交。 |
| 小型设置表 | `OnFieldChange` 简洁，但失败反馈要明显。 |
| 主从表单 | 用过滤条件切换当前主记录相关子表。 |
| 插入行需要默认值 | 连接 `primeInsert` 填充记录。 |

## 6. 常见坑与经验

`setFilter()` 是 SQL 片段，不会自动参数绑定。不要把用户输入直接拼进去；需要安全过滤时用自定义查询模型或先严格转义/白名单。

`select()` 会丢弃未提交修改。刷新前先检查 `isDirty()`，否则用户编辑可能悄悄消失。

没有可靠主键的表不适合可编辑 table model。更新和删除需要定位真实行；主键缺失或重复会让提交行为不可预测。

`submitAll()` 失败后，缓存修改通常仍留在模型里。你可以修正错误后重提，或显式 `revertAll()`。

## 7. 知识点覆盖

- 单表 Model/View CRUD。
- 编辑策略、缓存修改、提交和撤销。
- 过滤、排序、主键和记录对象。
- 插入默认值、提交前信号和底层钩子。
- SQL 注入、刷新丢改和主键要求。
