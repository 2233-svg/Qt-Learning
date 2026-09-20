# QSqlRelationalTableModel
> Qt 6.11.1 · Qt SQL · 来自 `QSqlRelationalTableModel`

## 1. 先建立直觉

`QSqlRelationalTableModel` 是带外键显示能力的 `QSqlTableModel`。它让主表里存的外键 ID，在视图里显示成关联表里的可读文本；编辑时配合 `QSqlRelationalDelegate` 可以用下拉框选择关联值。

它解决的是“单表编辑 + 简单外键字典显示”，不是通用 ORM。

## 2. 类说明

保留类说明：这些 API 来自 `QSqlRelationalTableModel`，属于 Qt SQL 模块，用于把外键列映射到关联表显示列。

它通过 `setRelation(column, QSqlRelation(...))` 定义关系，并在 `select()` 时生成带 JOIN 的查询。更新时仍然写回主表外键值。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `QSqlRelationalTableModel(parent, db)` | 创建关系表模型。 |
| `setRelation(column, relation)` | 把某列定义为外键关系。 |
| `relation(column)` | 查询某列关系描述。 |
| `relationModel(column)` | 返回某列关联表的模型，常给 delegate 下拉框使用。 |
| `setJoinMode(InnerJoin/LeftJoin)` | 控制关联查询使用内连接或左连接。 |
| `setTable()` / `select()` | 继承并重写，关系变化后重新生成查询。 |
| `data()` / `setData()` | 显示关联列文本，编辑时处理外键值。 |
| `clear()`、`removeColumns()`、`revertRow()` | 维护关系模型状态。 |
| `selectStatement()`、`orderByClause()` | 生成带关系的 SQL，可在派生类中定制。 |
| `insertRowIntoTable()`、`updateRowInTable()` | 写回主表时使用。 |
| `JoinMode::InnerJoin` | 没有关联记录的主表行会被过滤掉。 |
| `JoinMode::LeftJoin` | 保留主表行，关联不存在时显示为空。 |

## 4. 典型流程

```cpp
auto *model = new QSqlRelationalTableModel(this, db);
model->setTable("employee");
model->setRelation(model->fieldIndex("city_id"),
                   QSqlRelation("city", "id", "name"));
model->setJoinMode(QSqlRelationalTableModel::LeftJoin);
model->select();

view->setModel(model);
view->setItemDelegate(new QSqlRelationalDelegate(view));
```

## 5. 使用场景

| 场景 | 为什么适合 |
| --- | --- |
| 字典表外键 | 状态、城市、部门、分类等 ID 显示成名称。 |
| 简单后台管理 | 视图编辑主表，同时用下拉框选择外键。 |
| 避免手写常见 JOIN | 关系规则简单时快速生成。 |

## 6. 常见坑与经验

`InnerJoin` 会隐藏没有匹配外键的主表行。很多人以为数据丢了，其实是 JOIN 模式过滤了；外键允许为空或引用表不完整时，用 `LeftJoin` 更符合维护界面预期。

关系列显示的是 displayColumn，不是原始外键值。需要取真实 ID 时，要理解模型角色和 relationModel 的映射，不要直接把显示文本当主键。

多级关系、组合外键、带条件的字典表、权限过滤等复杂场景会让 relational model 很别扭。此时写自定义 `QSqlQueryModel` 或业务模型更清楚。

## 7. 知识点覆盖

- 外键列到显示列的映射。
- `QSqlRelation`、relation model 和 delegate 配合。
- JOIN 模式对行可见性的影响。
- 关系模型的编辑写回边界。
