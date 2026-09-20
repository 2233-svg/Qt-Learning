# QSqlRelation
> Qt 6.11.1 · Qt SQL · 来自 `QSqlRelation`

## 1. 先建立直觉

`QSqlRelation` 描述一个外键列如何映射到另一张表的可读显示值。比如员工表 `city_id` 存整数，城市表 `id/name` 保存城市名；relation 就说明“用 city 表的 id 匹配，界面展示 name”。

它主要服务 `QSqlRelationalTableModel` 和 `QSqlRelationalDelegate`。

## 2. 类说明

保留类说明：这些 API 来自 `QSqlRelation`，属于 Qt SQL 模块，用于描述关系表、索引列和显示列。

它只是三段字符串的轻量值对象：关系表名、索引列、显示列。真正的 JOIN、查询和编辑由 relational table model 完成。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `QSqlRelation()` | 创建无效关系。 |
| `QSqlRelation(tableName, indexColumn, displayColumn)` | 创建外键关系描述。 |
| `tableName()` | 返回被关联的表。 |
| `indexColumn()` | 返回被关联表中用于匹配外键的列。 |
| `displayColumn()` | 返回向用户显示的列。 |
| `isValid()` | 判断三段信息是否构成有效关系。 |
| `swap()` | 值类型交换。 |

## 4. 典型流程

```cpp
auto *model = new QSqlRelationalTableModel(this, db);
model->setTable("employee");
model->setRelation(2, QSqlRelation("city", "id", "name"));
model->select();
```

第 2 列实际存 `city_id`，视图中显示城市名。配合 `QSqlRelationalDelegate`，编辑时通常出现下拉框。

## 5. 使用场景

| 场景 | 用法 |
| --- | --- |
| 外键显示名称 | 把 ID 列映射成名称列。 |
| 表格编辑外键 | 配合 relational delegate 显示候选值。 |
| 简单引用表 | 城市、部门、分类、状态码等字典表。 |

## 6. 常见坑与经验

relation 的列名是数据库列名，不是模型 header，也不是 SQL alias。写错不会在构造时失败，通常要到 `select()` 或显示时才暴露。

显示列不一定唯一。如果 displayColumn 有重复值，用户看到两个相同文本可能无法区分；字典表最好保证显示值唯一或用更清晰的组合字段。

复杂多表关系、额外过滤条件、联级加载通常超出 `QSqlRelation` 的舒适区。那时写自定义 SQL model 或代理模型更可控。

## 7. 知识点覆盖

- 外键列、关联表、索引列、显示列。
- `QSqlRelationalTableModel::setRelation()`。
- 字典表/引用表在 UI 中的显示和编辑。
- 简单关系模型的边界。
