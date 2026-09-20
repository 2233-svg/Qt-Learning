# QSqlRelation 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QSqlRelation>`  
> 所属模块：`Qt6::Sql`  
> 继承：无

## 它解决什么问题

`QSqlRelation` 描述一个外键列如何映射到另一张表的可读字段。它是 `QSqlRelationalTableModel` 的辅助值类型，用来解决“数据库保存 ID，但界面要显示名称”的常见问题。

例如订单表的 `customer_id` 保存客户主键，而客户表的 `name` 才应显示给用户：

```cpp
model.setRelation(
    customerIdColumn,
    QSqlRelation("customers", "id", "name"));
```

这里三个字符串分别是：

- `tableName`：被引用表，如 `customers`；
- `indexColumn`：被引用表中的键列，如 `id`；
- `displayColumn`：界面显示列，如 `name`。

`QSqlRelation` 不会创建数据库外键、不会验证 referential integrity，也不会执行 join。它只是给关系表模型一份“如何查找和显示关联值”的描述。

## 使用场景和边界

它只配合 `QSqlRelationalTableModel::setRelation()` 使用。模型会据此查询关联表，并通过 `QSqlRelationalDelegate` 把编辑器呈现成组合框等适当控件。

表名、键列和显示列都必须与实际数据库 schema 匹配。列名含义容易混淆：`indexColumn` 指的是**关联表中被当前外键引用的列**，不是当前主表外键列名；当前主表的列由 `setRelation(column, relation)` 的 `column` 参数指定。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QSqlRelation()` | 创建无效的关系描述。 | 三个列名查询都为空；使用前用 `isValid()` 判断。 |
| 构造 | `QSqlRelation(const QString &tableName, const QString &indexColumn, const QString &displayColumn)` | 创建关联表、键列和显示列明确的关系描述。 | 三个名字必须是关联表中的实际 SQL 标识，避免把主表外键列填进 indexColumn。 |
| 显示列 | `displayColumn() const` | 返回关联表中展示给用户的列名。 | 应选择可读且适合编辑器显示的字段，如名称而不是内部编码。 |
| 键列 | `indexColumn() const` | 返回关联表中被外键引用的键列名。 | 通常是关联表主键或唯一键。 |
| 有效性 | `isValid() const` | 判断关系描述是否有效。 | 默认构造对象无效，配置模型前应检查。 |
| 交换 | `swap(QSqlRelation &other)` | 高效且不会失败地交换两个关系描述。 | 用于值类型调整，无需深拷贝。 |
| 关联表 | `tableName() const` | 返回外键引用的表名。 | 这是目标表，不是设置 relation 的主表。 |

## 易错点

1. `QSqlRelation` 不会在数据库中创建外键约束。
2. `indexColumn` 属于目标关联表，而当前表的外键列由 `setRelation()` 第一个参数指定。
3. `displayColumn` 只影响模型的展示和编辑映射，不改变实际存储的外键值。
4. 默认构造关系无效，不能直接拿来配置模型。

### 一句话总结

`QSqlRelation` 是关系表模型的外键显示映射：数据库继续保存键值，UI 通过关联表的显示列呈现用户可读内容。
