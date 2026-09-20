# QSqlTableModel：一张数据库表的可编辑模型

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QSqlTableModel>`  
> 模块：`Qt6::Sql`  
> 继承：`QSqlQueryModel`  
> 相关类：`QSqlRelationalTableModel`、`QSqlRecord`、`QSqlIndex`、`QTableView`

## 它解决什么问题

`QSqlTableModel` 把**一张数据库表**映射为可供 Qt 模型/视图使用的二维模型，并把插入、修改、删除操作按选定策略写回数据库。

它建立在 `QSqlQueryModel` 之上，但能力边界不同：

```text
QSqlQueryModel
  任意 SELECT 结果，默认只读

QSqlTableModel
  单张表，负责生成 INSERT / UPDATE / DELETE，可编辑

QSqlRelationalTableModel
  单张表加外键显示值和关联编辑
```

这个类解决的是“让 `QTableView` 直接编辑一张表”的问题，而不是通用 ORM，也不是任意复杂 JOIN 的更新器。它依赖表元数据和主键定位记录，复杂多表业务规则通常更适合用明确的 `QSqlQuery` 命令实现。

## 使用场景

- 后台管理界面编辑一张实体表，例如员工、商品、配置项。
- 需要在表格中插入、修改、删除，并让模型决定何时提交。
- 用 `setFilter()`、`setSort()` 限制单表显示集合。

不适合：

- 直接编辑 JOIN、聚合或计算列的结果。
- 用外键 ID 展示人类可读名称，且希望编辑时自动显示下拉框。
- 需要跨多表保存并要求完整业务级事务编排的场景。

## 最小可编辑表格

```cpp
#include <QSqlTableModel>
#include <QTableView>

auto *model = new QSqlTableModel(parent, QSqlDatabase::database("app"));
model->setTable("employee");
model->setEditStrategy(QSqlTableModel::OnManualSubmit);
model->setFilter("active = 1");
model->setSort(model->fieldIndex("name"), Qt::AscendingOrder);

if (!model->select())
    qWarning() << model->lastError().text();

model->setHeaderData(1, Qt::Horizontal, tr("姓名"));
view->setModel(model);
view->hideColumn(model->fieldIndex("id"));
```

`setTable()` 只选择目标表，`setFilter()` 和 `setSort()` 只设置选取规则；调用 `select()` 后模型才按这些规则重新读库。

## 三种编辑策略是这类的核心

### `OnFieldChange`

每个字段修改都会尽快提交到数据库。适合简单、低风险、希望立即持久化的编辑，但失败后已提交改动不会自动回滚。新插入行为了避免写入半初始化数据，行为会退化为类似 `OnRowChange`。

### `OnRowChange`

用户切换到另一行时，提交当前行改动。这是默认策略。它把“一行”当作最小编辑单元，但不等于数据库事务。

### `OnManualSubmit`

所有插入、修改、删除先缓存到模型，直到 `submitAll()` 或 `revertAll()`。这是带“保存”“取消”按钮的表单最常用策略。

若要让多次提交在数据库层面原子化，应显式使用同一个 `QSqlDatabase` 的事务：

```cpp
QSqlDatabase db = model->database();

if (db.transaction() && model->submitAll()) {
    if (!db.commit())
        qWarning() << db.lastError().text();
} else {
    db.rollback();
    // OnManualSubmit 下失败的缓存仍在，可修正后重提，或调用 revertAll()。
}
```

`submitAll()` 在 `OnManualSubmit` 成功后会重新选取模型，视图当前选择可能丢失；失败时已提交的更改不会从缓存清除，这正好允许回滚后修正和重试。

## 主键、过滤和生成字段

### 主键决定如何定位更新与删除

调用 `setTable()` 时，模型会读取表主键。表没有可靠主键时，更新和删除可能无法精确定位目标行。用于编辑的表应声明稳定、唯一的主键。

### `setFilter()` 不是参数绑定接口

过滤字符串是 SQL 的 `WHERE` 子句内容，**不包含** `WHERE` 关键字，例如 `status = 'active'`。它会直接进入 SQL，绝不能把用户输入未经处理地拼进去。复杂或带参数的筛选，优先改用自己的 `QSqlQuery` 或严格白名单组装。

### `QSqlRecord::generated` 控制写回列

`setRecord()` 按字段名而不是字段位置映射。传入记录中 `generated == false` 的字段不会进入提交 SQL，可用于排除只读字段、数据库生成列或不想覆盖的列。

## 与视图、信号和代理的协作

视图修改单元格时会调用 `setData()`；模型按编辑策略立即写库或标记 dirty。调用 `insertRows()`、`insertRecord()`、`removeRows()` 只是先改变模型；什么时候提交取决于策略。

`primeInsert()` 在新行加入模型前发出，可为记录填默认值。`beforeInsert()`、`beforeUpdate()`、`beforeDelete()` 在实际 SQL 操作前发出，适合检查和补充即将写入的记录。它们不是跨线程通知，也不替代数据库约束。

外键可读名称和下拉编辑不属于本类；使用 `QSqlRelationalTableModel` 加 `QSqlRelationalDelegate`。

## API 速查表

`EditStrategy` 的取值：

- `OnFieldChange`：字段变更尽快写入；新插入行会按行提交。
- `OnRowChange`：切换行时提交当前行；这是默认策略。
- `OnManualSubmit`：缓存直到 `submitAll()` 或 `revertAll()`。

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QSqlTableModel(QObject *parent, const QSqlDatabase &db)` | 创建空的单表 SQL 模型。 | `db` 无效时使用默认连接；默认编辑策略是 `OnRowChange`。 |
| 生命周期 | `~QSqlTableModel()` | 销毁模型与其缓存。 | 视图仍在使用模型时不要提前删除。 |
| 表与连接 | `database()` | 返回模型使用的数据库连接句柄。 | 是共享句柄；可用它协调事务，但不要随意关闭连接。 |
| 表与连接 | `setTable(const QString &tableName)` | 设置要操作的单张表并读取元数据。 | 设置后调用 `select()`；编辑表应有可靠主键。 |
| 表与连接 | `tableName()` | 返回当前目标表名。 | 返回空字符串说明尚未设置表。 |
| 表与连接 | `primaryKey()` | 返回当前表的主键索引描述。 | 主键缺失会降低更新、删除的可靠性。 |
| 表与连接 | `fieldIndex(const QString &fieldName)` | 返回字段在模型中的列号。 | 找不到时返回负值；用于隐藏列和设置排序。 |
| 查询规则 | `setFilter(const QString &filter)` | 设置 SQL WHERE 条件内容。 | 不写 `WHERE`；不能把未验证的用户输入直接拼入。 |
| 查询规则 | `filter()` | 返回当前过滤字符串。 | 是 SQL 片段，不是已绑定参数对象。 |
| 查询规则 | `setSort(int column, Qt::SortOrder order)` | 设置下次选取使用的排序。 | 不会立刻刷新；之后调用 `select()`。 |
| 查询规则 | `sort(int column, Qt::SortOrder order)` | 设置排序并立即重新选取数据。 | 会改变当前模型内容和视图选择。 |
| 查询规则 | `select()` | 按表、过滤和排序重新从数据库填充模型。 | 返回 `false` 时检查 `lastError()`；会影响未提交缓存。 |
| 查询规则 | `selectRow(int row)` | 重新选取指定行。 | 用于刷新单行；行号须是当前模型有效行。 |
| 编辑策略 | `setEditStrategy(EditStrategy strategy)` | 设置修改何时写入数据库。 | 在用户编辑前设定，避免混淆已有 dirty 缓存。 |
| 编辑策略 | `editStrategy()` | 返回当前编辑策略。 | 据此决定使用 `submit()` 还是 `submitAll()`。 |
| 数据编辑 | `setData(const QModelIndex &index, const QVariant &value, int role)` | 修改一个模型单元格。 | 正常编辑使用 `Qt::EditRole`；最终提交时机由策略决定。 |
| 数据编辑 | `clearItemData(const QModelIndex &index)` | 清除索引处缓存的角色数据。 | Qt 6 的模型接口重实现；不是 SQL `NULL` 写入捷径。 |
| 数据编辑 | `setRecord(int row, const QSqlRecord &values)` | 按字段名批量设置某行字段值。 | `generated == false` 的字段不会写回数据库。 |
| 数据访问 | `data(const QModelIndex &index, int role)` | 返回指定单元格的角色数据。 | 自定义显示时优先使用代理或谨慎派生。 |
| 数据访问 | `record()` | 返回当前表的空记录模板和字段结构。 | 用它构造插入记录，不代表某一实际行。 |
| 数据访问 | `record(int row)` | 返回指定行的字段和值。 | 返回的是副本，直接修改它不会改模型。 |
| 数据访问 | `flags(const QModelIndex &index)` | 返回单元格可选、可编辑等标志。 | 可派生以限制只读列；不要只靠 UI 限制权限。 |
| 数据访问 | `headerData(int section, Qt::Orientation orientation, int role)` | 返回表头数据。 | 通过继承自模型的 `setHeaderData()` 可设置显示标题。 |
| 数据访问 | `rowCount(const QModelIndex &parent)` | 返回当前模型行数。 | 表格模型没有层级，`parent` 应无效。 |
| 插入 | `insertRows(int row, int count, const QModelIndex &parent)` | 在模型中插入指定数量的空行。 | 空行只进入模型缓存；填值和提交受策略控制。 |
| 插入 | `insertRecord(int row, const QSqlRecord &record)` | 在指定位置插入一条记录。 | 传 `row = -1` 可追加；字段生成标志影响提交列。 |
| 删除 | `removeRows(int row, int count, const QModelIndex &parent)` | 标记或执行连续多行删除。 | `OnManualSubmit` 下先缓存；提交前可 `revertAll()`。 |
| 提交与撤销 | `submit()` | 提交当前编辑行。 | 仅对 `OnFieldChange` 和 `OnRowChange` 有效；手动模式改用 `submitAll()`。 |
| 提交与撤销 | `submitAll()` | 提交所有待处理变更。 | 手动模式成功会重新选取，失败缓存保留以便修正重试。 |
| 提交与撤销 | `revert()` | 撤销当前编辑行的未提交修改。 | 对当前编辑上下文有效，不等于撤销全部缓存。 |
| 提交与撤销 | `revertRow(int row)` | 撤销指定行的未提交修改。 | 已经写入数据库的改动不能靠它撤销。 |
| 提交与撤销 | `revertAll()` | 丢弃模型内所有未提交修改。 | 只丢缓存；不会回滚此前已成功提交的数据。 |
| Dirty 状态 | `isDirty()` | 判断模型是否有未提交更改。 | 常用于保存按钮状态，但要同时处理提交错误。 |
| Dirty 状态 | `isDirty(const QModelIndex &index)` | 判断指定单元格是否有未提交更改。 | 只反映模型缓存，不反映其他连接的外部修改。 |
| 重置 | `clear()` | 清空表名、查询和模型内容。 | 不删除数据库表或数据。 |
| 列操作 | `removeColumns(int column, int count, const QModelIndex &parent)` | 从模型结果中移除列。 | 用于隐藏列；不会 ALTER TABLE。 |
| 派生钩子 | `selectStatement()` | 生成供 `select()` 使用的 SQL SELECT 语句。 | 仅供子类改写查询生成逻辑，不要在外部直接调用。 |
| 派生钩子 | `orderByClause()` | 生成排序 SQL 片段。 | 与 `setSort()` 协作；子类改写时注意标识符转义。 |
| 派生钩子 | `indexInQuery(const QModelIndex &item)` | 映射模型索引到实际查询索引。 | 添加、隐藏列的派生模型需要正确重写。 |
| 派生钩子 | `primaryValues(int row)` | 提取指定行主键字段值。 | 用于 UPDATE/DELETE 定位；只在派生实现中使用。 |
| 派生钩子 | `setPrimaryKey(const QSqlIndex &key)` | 设置模型用于定位记录的主键。 | `setTable()` 通常会自动设置；子类特殊化时使用。 |
| 派生钩子 | `insertRowIntoTable(const QSqlRecord &values)` | 直接执行底层 INSERT。 | 低层函数；外部应调用模型插入 API 让策略生效。 |
| 派生钩子 | `updateRowInTable(int row, const QSqlRecord &values)` | 直接执行底层 UPDATE。 | 不要绕过 `setData()` 和编辑策略。 |
| 派生钩子 | `deleteRowFromTable(int row)` | 直接执行底层 DELETE。 | 不要绕过 `removeRows()` 和提交流程。 |
| 写入信号 | `primeInsert(int row, QSqlRecord &record)` | 新记录加入模型前通知，可预填默认字段。 | 修改传入记录时只设置业务允许的默认值。 |
| 写入信号 | `beforeInsert(QSqlRecord &record)` | 实际 INSERT 前通知即将写入的记录。 | 可补充审计字段；数据库仍应保留约束。 |
| 写入信号 | `beforeUpdate(int row, QSqlRecord &record)` | 实际 UPDATE 前通知即将写入的记录。 | 不要在信号处理里递归修改同一模型。 |
| 写入信号 | `beforeDelete(int row)` | 实际 DELETE 前通知目标行。 | 行号基于当前模型；删除后不要继续使用它定位旧行。 |

## 最容易踩的坑

- 忘记调用 `select()`：设置表、过滤和排序后模型可能仍是空的或旧数据。
- 以为 `OnRowChange` 有事务语义：它只是提交时机，不保证多行原子性。
- 在 `OnManualSubmit` 中提交失败就立刻清空 UI：失败缓存仍在，应让用户修正或明确撤销。
- 直接把用户搜索文本塞进 `setFilter()`：这是 SQL 拼接风险。
- 对无主键表做编辑：模型难以精确更新和删除。
- 需要外键下拉框却仍使用 `QSqlTableModel`：换 `QSqlRelationalTableModel` 和 `QSqlRelationalDelegate`。
