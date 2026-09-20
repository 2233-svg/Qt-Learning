# QSqlRelationalTableModel：让外键列显示为可读文本

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QSqlRelationalTableModel>`  
> 模块：`Qt6::Sql`  
> 继承：`QSqlTableModel`  
> 相关类：`QSqlRelation`、`QSqlRelationalDelegate`、`QSqlTableModel`

## 它解决什么问题

关系型数据库通常把外键保存为 ID，例如 `employee.city_id = 3`。ID 适合连接和约束，却不适合直接展示给用户。`QSqlRelationalTableModel` 在 `QSqlTableModel` 的单表编辑能力之上，为指定列配置 `QSqlRelation`：

```text
employee.city_id
  -> city.id
  -> city.name
```

这样视图可以显示 `"Shanghai"`，保存时仍写入对应的外键值。它不是通用的多表查询模型，而是“一个可编辑主表加若干查找表”的专门模型。

## 适用场景

- 员工表中的部门、城市、国家、状态等外键需要显示名称。
- 在 `QTableView` 中编辑外键，并希望得到下拉选择框。
- 主表仍是一张可更新的表，关联表只是用于查找与展示。

不适合：

- 任意 JOIN、聚合、多对多或复杂报表的更新。
- 主表没有主键的编辑场景。
- 希望由模型替代数据库的外键约束和参照完整性。

## 最小示例

```cpp
#include <QSqlRelationalDelegate>
#include <QSqlRelationalTableModel>
#include <QTableView>

auto *model = new QSqlRelationalTableModel(
    parent, QSqlDatabase::database("app"));

model->setTable("employee");
model->setRelation(
    model->fieldIndex("city_id"),
    QSqlRelation("city", "id", "name"));
model->setEditStrategy(QSqlTableModel::OnManualSubmit);

if (!model->select())
    qWarning() << model->lastError().text();

view->setModel(model);
view->setItemDelegate(new QSqlRelationalDelegate(view));
```

`QSqlRelation("city", "id", "name")` 的三个参数依次是：

1. 引用表名 `city`。
2. 引用表中与主表外键匹配的索引列 `id`。
3. 视图应显示给用户的文本列 `name`。

`setRelation()` 中的列号是**主表模型列号**。应先 `setTable()`，再用 `fieldIndex("city_id")` 获取列号，避免硬编码位置随表结构变化而错位。

## 显示值、保存值与代理

模型的显示数据来自关联表的 display column，数据库中主表存的却还是 index column 的外键值。因此用户在界面里看到名称，不等于 `record(row)` 中该列一定能直接作为名称使用；写回、筛选和取原始外键时要先确认所处 API 的语义。

仅设置关系不会让默认代理自动变成下拉框。可编辑的 `QTableView` 通常还需要 `QSqlRelationalDelegate`，它会使用关联模型创建组合框，让用户在显示名称中选择，然后将对应关系写回主表。

使用 `setData()` 直接改关联列时，应使用 `Qt::EditRole`；不要把 `DisplayRole` 当作写入协议。

## 默认 `InnerJoin` 可能让行“消失”

默认连接模式是 `InnerJoin`。当外键为 `NULL` 时，对应主表行不会出现在模型中。若业务需要保留这些行，例如“尚未分配城市的员工”，应在 `select()` 前调用：

```cpp
model->setJoinMode(QSqlRelationalTableModel::LeftJoin);
```

`LeftJoin` 解决的是显示 `NULL` 外键行的问题，不会替你修复无效外键。引用表不存在对应行时，参照完整性仍应该由数据库约束和业务逻辑保证。

## 关系表名称与列名冲突

多个关系的 display column 可能都叫 `name`，也可能与主表字段重名。此类重复发生时，模型会对结果列起别名；`QSqlRecord::fieldName()` 因而可能返回别名，而 `QSqlRelation::displayColumn()` 仍返回原始显示列名。

引用表在生成 SQL 时也会使用类似 `relTblAl_2` 的别名。需要对关联显示列做 `setFilter()` 时，使用模型生成的关联表别名，而不要假设引用表原名能直接用于 WHERE 条件。

## 与 `QSqlTableModel` 的继承边界

`QSqlRelationalTableModel` 继承了单表模型的编辑策略、`submitAll()`、`revertAll()`、过滤、排序、插入和删除 API。那些行为仍然针对**主表**。关联表模型只作为查询和编辑选择来源，不是调用方拥有的独立数据模型。

主表必须声明主键，且主键本身不能是一个关联列。否则模型无法稳定地为更新与删除定位记录。

## API 速查表

`JoinMode` 的取值：

- `InnerJoin`：默认值；不显示外键为 `NULL` 的主表行。
- `LeftJoin`：保留外键为 `NULL` 的主表行。

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QSqlRelationalTableModel(QObject *parent, const QSqlDatabase &db)` | 创建空的关联表模型。 | `db` 无效时使用默认连接；实际项目推荐传具名连接。 |
| 生命周期 | `~QSqlRelationalTableModel()` | 销毁模型及其内部关联模型。 | `relationModel()` 返回的对象会随主模型失效。 |
| 关系配置 | `setRelation(int column, const QSqlRelation &relation)` | 把主表指定列配置为外键关系。 | 先 `setTable()`；主表主键列不能配置关系。 |
| 关系配置 | `relation(int column)` | 返回指定主表列的关系描述。 | 无关系或列无效时返回无效 `QSqlRelation`。 |
| 关系配置 | `relationModel(int column)` | 返回关联表对应的 `QSqlTableModel`。 | 返回指针由本模型拥有，不能删除，也不应长期脱离主模型保存。 |
| 连接方式 | `setJoinMode(JoinMode joinMode)` | 设置关联查询使用内连接还是左连接。 | 默认内连接隐藏 NULL 外键行；应在 `select()` 前设置。 |
| 查询与重置 | `select()` | 按关系配置生成连接查询并重新填充模型。 | 设置表、关系、连接方式后调用；失败检查 `lastError()`。 |
| 查询与重置 | `setTable(const QString &table)` | 设置主表并重置表相关元数据。 | 改主表后重新设置关系并 `select()`，不要沿用旧列号假设。 |
| 查询与重置 | `clear()` | 清空主表、关系与当前查询结果。 | 只重置模型，不会删除数据库任何表或数据。 |
| 模型数据 | `data(const QModelIndex &index, int role)` | 返回转换后的显示数据与标准模型角色数据。 | 显示值可能来自关联表，不要混同于存储的外键值。 |
| 模型数据 | `setData(const QModelIndex &index, const QVariant &value, int role)` | 修改主表字段或关联字段。 | 关联字段写入使用 `Qt::EditRole`；提交时机沿用基类编辑策略。 |
| 模型结构 | `removeColumns(int column, int count, const QModelIndex &parent)` | 移除模型可见列。 | 只影响模型视图，并会同步维护关系元数据。 |
| 撤销 | `revertRow(int row)` | 撤销指定主表行的未提交改动。 | 会同时恢复关联展示状态；已提交数据不受影响。 |
| 派生钩子 | `selectStatement()` | 生成带关系 JOIN 的 SELECT 语句。 | 仅供子类特殊化；别在外部调用或拼接 SQL。 |
| 派生钩子 | `orderByClause()` | 生成关联查询的 ORDER BY 片段。 | 重写时要处理别名和标识符转义。 |
| 派生钩子 | `insertRowIntoTable(const QSqlRecord &values)` | 直接向主表执行 INSERT。 | 底层实现点；正常代码走 `insertRecord()` 和编辑策略。 |
| 派生钩子 | `updateRowInTable(int row, const QSqlRecord &values)` | 直接更新主表一行。 | 不要绕过模型的缓存、信号和提交控制。 |

## 常见错误

- 只调用 `setRelation()`，却没有安装 `QSqlRelationalDelegate`：可编辑界面不会自然出现好用的下拉选择。
- 关系列号写死为 `2`、`3`：字段顺序变更后会错误关联，改用 `fieldIndex()`。
- 默认 `InnerJoin` 下发现 NULL 外键记录“不见了”：明确选择 `LeftJoin`。
- 将关系表返回的 `QSqlTableModel *` 手动删除：它属于 `QSqlRelationalTableModel`。
- 以为它会保证参照完整性：数据库仍应声明外键约束，应用也应处理不存在的引用记录。
- 用原始 display column 名做复杂过滤：遇到重名时模型会别名化，需按生成的别名理解查询。
