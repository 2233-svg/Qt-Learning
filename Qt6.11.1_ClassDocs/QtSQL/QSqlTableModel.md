# QSqlTableModel

> Qt 6.11.1 · Qt SQL

## 1. 先建立直觉

**一句话定位：** `QSqlTableModel` 是 Qt SQL 的“Sql表格模型”类型，参与数据库连接、SQL 执行、事务或结果模型。

**模块背景：** Qt SQL 提供数据库连接、查询、事务和 SQL 模型/视图集成。

### 这是什么

`QSqlTableModel` 是模型/视图体系中的数据模型类型，向视图提供索引、角色数据和结构变化通知。

**内部模型：** 视图不应该直接操作底层容器；它通过 QModelIndex 和 data roles 查询模型。模型必须准确维护索引有效性以及插入、删除、移动时的通知顺序。

**适用场景：** 需要把自定义数据接入 QListView、QTableView、QTreeView 或代理模型时使用。

**典型调用链：** 准备数据源 -> 实现/配置模型 -> 连接 view -> 通过 data/flags/setData 读写 -> 发出 dataChanged 或 begin/end 结构通知。

**先记住的坑：** 不要在 data() 中修改数据；不要返回过期索引；不要用全量 reset 代替精确结构通知，除非确实无法描述变化。

## 2. 依赖与对象关系

- 头文件：`#include <QSqlTableModel>`
- 继承自：QSqlQueryModel
- 直接派生类：QSqlRelationalTableModel

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Sql)
target_link_libraries(mytarget PRIVATE Qt6::Sql)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

视图不应该直接操作底层容器；它通过 QModelIndex 和 data roles 查询模型。模型必须准确维护索引有效性以及插入、删除、移动时的通知顺序。

### 状态、生命周期和线程

**生命周期：** 连接由连接名识别，查询和模型引用连接。关闭或移除连接前必须销毁仍引用它的 query、model 和 database 句柄；不同线程不要共用连接。

**状态与结果：** 区分连接是否打开、语句是否执行成功、游标是否定位在有效行、字段是否存在以及事务是否提交成功。`exec()` 成功不代表有结果行，`next()` 成功后才可以安全读取当前行。

**线程与事件循环：** Qt SQL 连接有线程归属，每个线程应建立自己的连接并使用唯一连接名；不要把一个线程创建的 QSqlDatabase 或 QSqlQuery 传到另一个线程继续使用。

## 3. 直接使用

需要把自定义数据接入 QListView、QTableView、QTreeView 或代理模型时使用。 使用时通常按这个过程组织：准备数据源 -> 实现/配置模型 -> 连接 view -> 通过 data/flags/setData 读写 -> 发出 dataChanged 或 begin/end 结构通知。

```cpp
QSqlQuery query(database);
query.prepare(QStringLiteral("SELECT name FROM users WHERE id = :id"));
query.bindValue(QStringLiteral(":id"), id);
if (query.exec()) {
    while (query.next()) {
        const QVariant value = query.value(0);
    }
}
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum EditStrategy { OnFieldChange, OnRowChange, OnManualSubmit }`

### 公有函数

- `QSqlTableModel(QObject *parent = nullptr, const QSqlDatabase &db = QSqlDatabase())`
- `virtual ~QSqlTableModel()`
- `QSqlDatabase database() const`
- `QSqlTableModel::EditStrategy editStrategy() const`
- `int fieldIndex(const QString &fieldName) const`
- `QString filter() const`
- `bool insertRecord(int row, const QSqlRecord &record)`
- `bool isDirty(const QModelIndex &index) const`
- `bool isDirty() const`
- `QSqlIndex primaryKey() const`
- `QSqlRecord record() const`
- `QSqlRecord record(int row) const`
- `virtual void revertRow(int row)`
- `virtual void setEditStrategy(QSqlTableModel::EditStrategy strategy)`
- `virtual void setFilter(const QString &filter)`
- `bool setRecord(int row, const QSqlRecord &values)`
- `virtual void setSort(int column, Qt::SortOrder order)`
- `virtual void setTable(const QString &tableName)`
- `QString tableName() const`

### 重实现的公有函数

- `virtual void clear() override`
- `virtual bool clearItemData(const QModelIndex &index) override`
- `virtual QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const override`
- `virtual Qt::ItemFlags flags(const QModelIndex &index) const override`
- `virtual QVariant headerData(int section, Qt::Orientation orientation, int role = Qt::DisplayRole) const override`
- `virtual bool insertRows(int row, int count, const QModelIndex &parent = QModelIndex()) override`
- `virtual bool removeColumns(int column, int count, const QModelIndex &parent = QModelIndex()) override`
- `virtual bool removeRows(int row, int count, const QModelIndex &parent = QModelIndex()) override`
- `virtual int rowCount(const QModelIndex &parent = QModelIndex()) const override`
- `virtual bool setData(const QModelIndex &index, const QVariant &value, int role = Qt::EditRole) override`
- `virtual void sort(int column, Qt::SortOrder order) override`

### 公有槽函数

- `virtual void revert() override`
- `void revertAll()`
- `virtual bool select()`
- `virtual bool selectRow(int row)`
- `virtual bool submit() override`
- `bool submitAll()`

### 信号

- `void beforeDelete(int row)`
- `void beforeInsert(QSqlRecord &record)`
- `void beforeUpdate(int row, QSqlRecord &record)`
- `void primeInsert(int row, QSqlRecord &record)`

### 保护函数

- `virtual bool deleteRowFromTable(int row)`
- `virtual bool insertRowIntoTable(const QSqlRecord &values)`
- `virtual QString orderByClause() const`
- `QSqlRecord primaryValues(int row) const`
- `virtual QString selectStatement() const`
- `void setPrimaryKey(const QSqlIndex &key)`
- `virtual bool updateRowInTable(int row, const QSqlRecord &values)`

### 重实现的保护函数

- `virtual QModelIndex indexInQuery(const QModelIndex &item) const override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QSqlTableModel::EditStrategy`

**作用与语义：**

该枚举类型描述了编辑数据库中值时应选择的策略。
- `QSqlTableModel::OnFieldChange`：`0`;所有对模型的更改将立即应用到数据库中。
- `QSqlTableModel::OnRowChange`：`1`;当用户选择不同的行时，行的更改将被应用。
- `QSqlTableModel::OnManualSubmit`：`2`;所有变更都会缓存在模型中，直到调用`submitAll()`或`revertAll()`。
注意：为防止只插入部分初始化的行，`OnFieldChange`会像新插入行的 `OnRowChange` 一样表现。

### `[explicit] QSqlTableModel::QSqlTableModel(QObject *parent = nullptr, const QSqlDatabase &db = QSqlDatabase())`

**作用与语义：**

创建空的 QSqlTableModel，并将父节点设置为 `parent`，数据库连接设置为 `db`。如果`db`无效，将使用默认数据库连接。
默认的编辑策略是`OnRowChange`。

### `[virtual noexcept] QSqlTableModel::~QSqlTableModel()`

**作用与语义：**

摧毁该物体并释放所有分配的资源。

### `[signal] void QSqlTableModel::beforeDelete(int row)`

**作用与语义：**

该信号由`deleteRowFromTable()`在`row`从当前活跃数据库表中删除前发出。

### `[signal] void QSqlTableModel::beforeInsert(QSqlRecord &record)`

**作用与语义：**

该信号由`insertRowIntoTable()`在插入当前活跃数据库表的新行之前发出。即将插入的值存储在`record`中，插入前可以进行修改。

### `[signal] void QSqlTableModel::beforeUpdate(int row, QSqlRecord &record)`

**作用与语义：**

该信号由`updateRowInTable()`发出，随后`row`在当前活跃数据库表中更新，包含`record`的值。
注意，只有标记为生成的值才会被更新。生成的标志可以用`QSqlRecord::setGenerated()`设置，并用 `QSqlRecord::isGenerated()` 检查。

### `[override virtual] void QSqlTableModel::clear()`

**作用与语义：**

重装：`QSqlQueryModel::clear()`。
清除模型并释放任何获得的资源。

### `[override virtual] bool QSqlTableModel::clearItemData(const QModelIndex &index)`

**作用与语义：**

重装：`QAbstractItemModel::clearItemData`（const QModelIndex & index）。

### `[override virtual] QVariant QSqlTableModel::data(const QModelIndex &index, int role = Qt::DisplayRole) const`

**作用与语义：**

返回 `index` 在指定 `role` 下的数据。显示和编辑角色来自当前记录，其他角色按 `QSqlQueryModel`/`QAbstractItemModel` 规则处理；索引无效或角色不受支持时返回无效 `QVariant`。未提交的编辑会优先反映在返回值中。

### `QSqlDatabase QSqlTableModel::database() const`

**作用与语义：**

返回模型的数据库连接。

### `[virtual protected] bool QSqlTableModel::deleteRowFromTable(int row)`

**作用与语义：**

从当前活跃的数据库表中删除给定的`row`。
这是一种底层方法，直接运行在数据库上，不应直接调用。使用`removeRow()`或`removeRows()`删除数值。模型将根据其编辑策略决定何时修改数据库。
如果该行被删除，返回`true`;否则返回`false`。

### `QSqlTableModel::EditStrategy QSqlTableModel::editStrategy() const`

**作用与语义：**

返回当前的编辑策略。

### `int QSqlTableModel::fieldIndex(const QString &fieldName) const`

**作用与语义：**

返回场`fieldName`的索引，若模型中无对应字段则返回-1。

### `QString QSqlTableModel::filter() const`

**作用与语义：**

返回当前设置的过滤器。

### `[override virtual] Qt::ItemFlags QSqlTableModel::flags(const QModelIndex &index) const`

**作用与语义：**

重实现自：`QAbstractTableModel::flags`（const QModelIndex & index） const.

### `[override virtual] QVariant QSqlTableModel::headerData(int section, Qt::Orientation orientation, int role = Qt::DisplayRole) const`

**作用与语义：**

重实现自：`QSqlQueryModel::headerData`（int section， Qt：：Orientation orientation， int role） const.

### `[override virtual protected] QModelIndex QSqlTableModel::indexInQuery(const QModelIndex &item) const`

**作用与语义：**

重实现自：`QSqlQueryModel::indexInQuery`（const QModelIndex &item） const.
返回数据库结果集中给定`item`的索引。
如果没有插入、删除或移动列或行，返回值与 `item` 相同。
如果`item`超出边界或`item`未指向结果集中的某个值，则返回无效的模型索引。
返回数据库结果集中对模型中给定`item`值的索引。
如果没有插入、删除或移动任何列或行，返回值与 `item` 相同。
如果`item`超出边界或`item`未指向结果集中的某个值，则返回无效的模型索引。

### `bool QSqlTableModel::insertRecord(int row, const QSqlRecord &record)`

**作用与语义：**

将`record`插入位置`row`。如果`row`为负，记录将附加到末尾。调用`insertRows()`和`setRecord()`内部。
如果记录可以插入，返回`true`，否则返回假。
变更会立即提交以便进行`OnFieldChange`和`OnRowChange`。失败不会在模型中留下新行。

### `[virtual protected] bool QSqlTableModel::insertRowIntoTable(const QSqlRecord &values)`

**作用与语义：**

将`values`值插入当前活跃的数据库表中。
这是一种底层方法，直接运行在数据库上，不应直接调用。使用 `insertRow()` 和 `setData()` 插入数值。模型会根据其编辑策略决定何时修改数据库。
如果可以插入这些值，返回`true`，否则为假。错误信息可以通过 `lastError()` 检索。

### `[override virtual] bool QSqlTableModel::insertRows(int row, int count, const QModelIndex &parent = QModelIndex())`

**作用与语义：**

重实现自：`QAbstractItemModel::insertRows`（整数行，整数计数，cont QModelIndex 和parent）。
在位置`row`插入`count`空行。注意，`parent`必然无效，因为该模型不支持父子关系。
对于编辑策略`OnFieldChange`和`OnRowChange`，一次只能插入一行，且模型中不得包含其他缓存变更。
每增加一行就会发出`primeInsert()`信号。如果你想用默认值初始化新行，可以连接到它。
无论采用何种编辑策略，都不会提交行。
如果参数超出边界或无法插入该行，返回`false`;否则返回`true`。

### `bool QSqlTableModel::isDirty(const QModelIndex &index) const`

**作用与语义：**

如果索引`index`的值是脏的，则返回`true`，否则为假。脏值是指模型中被修改但尚未写入数据库的值。
如果`index`无效或指向不存在的行，则返回假。

### `bool QSqlTableModel::isDirty() const`

**作用与语义：**

如果模型包含未提交到数据库的修改值，返回 会`true`，否则为假。

### `[virtual protected] QString QSqlTableModel::orderByClause() const`

**作用与语义：**

返回基于当前排序顺序的 SQL `ORDER BY` 子句。

### `QSqlIndex QSqlTableModel::primaryKey() const`

**作用与语义：**

返回当前表的主键，如果表未设置或没有主键，则返回空`QSqlIndex`。

### `[protected] QSqlRecord QSqlTableModel::primaryValues(int row) const`

**作用与语义：**

返回包含主键中字段的记录，该字段设置为`row`。如果没有定义主键，返回的记录将包含所有字段。

### `[signal] void QSqlTableModel::primeInsert(int row, QSqlRecord &record)`

**作用与语义：**

该信号由`insertRows()`发出，当插入当前活跃数据库表的指定`row`时。`record`参数可以写入（因为它是引用），例如用默认值填充某些字段并设置字段生成的标志。处理该信号时，不要尝试通过`setData()`或`setRecord()`等其他方式编辑记录。

### `QSqlRecord QSqlTableModel::record() const`

**作用与语义：**

它返回一个空记录，仅包含字段名称。该函数可用于检索记录的字段名称。

### `QSqlRecord QSqlTableModel::record(int row) const`

**作用与语义：**

在模型中返回`row`的记录。
如果`row`是有效行的索引，记录将被填充该行的值。
如果模型未初始化，将返回一个空记录。

### `[override virtual] bool QSqlTableModel::removeColumns(int column, int count, const QModelIndex &parent = QModelIndex())`

**作用与语义：**

重实现自：`QSqlQueryModel::removeColumns`（整数列，整数计数，cont QModelIndex 和父）。
从`parent`模型中移除`count`列，从索引`column`开始。
如果列被成功移除，则返回;否则返回`false`。

### `[override virtual] bool QSqlTableModel::removeRows(int row, int count, const QModelIndex &parent = QModelIndex())`

**作用与语义：**

重实现自：`QAbstractItemModel::removeRows`（整数行，整数计数，cont QModelIndex 和parent）。
移除从`row`开始的`count`行。由于该模型不支持层级结构，`parent`必须是无效的模型索引。
当编辑策略`OnManualSubmit`时，数据库中的行删除会被延迟，直到调用`submitAll()`。
对于`OnFieldChange`和`OnRowChange`，一次只能删除一行，且只有在没有其他行有缓存更改的情况下。删除请求立即提交到数据库。模型会保留一行作为成功删除的行，直到`select()`刷新。
删除失败后，该操作在模型中不会被恢复。应用程序可以重新提交或恢复。
已插入但尚未成功提交的待移除范围内的行会立即从模型中移除。
在数据库删除行之前，`beforeDelete()`信号会被发出。
如果行<0或行计数> `rowCount()`，则不执行任何操作，返回假。返回 `true` 如果所有行都可以被移除;否则返回 `false`。详细的数据库错误信息可以通过`lastError()`检索。

### `[override virtual slot] void QSqlTableModel::revert()`

**作用与语义：**

重装：`QAbstractItemModel::revert()`。
当用户取消当前行编辑时，项目代理调用了这个重新实现的槽位。
如果模型的策略设置为`OnRowChange`或`OnFieldChange`，则会回退这些更改。对`OnManualSubmit`策略没有任何作用。
用`revertAll()`回退`OnManualSubmit`策略的所有待处理变更，或用`revertRow()`回退特定行。

### `[slot] void QSqlTableModel::revertAll()`

**作用与语义：**

还原所有待处理的变更。

### `[virtual] void QSqlTableModel::revertRow(int row)`

**作用与语义：**

还原指定`row`的所有更改。

### `[override virtual] int QSqlTableModel::rowCount(const QModelIndex &parent = QModelIndex()) const`

**作用与语义：**

重实现自：`QSqlQueryModel::rowCount`（const QModelIndex &parent）const.

### `[virtual slot] bool QSqlTableModel::select()`

**作用与语义：**

用通过`setTable()`设置的表中的数据填充模型，使用指定的过滤器和排序条件，成功时返回`true`;否则返回`false`。
注意：调用 select() 将恢复所有未提交的更改并删除已插入的列。

### `[virtual slot] bool QSqlTableModel::selectRow(int row)`

**作用与语义：**

在模型中刷新时，`row`数据库表中的行值与主键值匹配。没有主键时，所有列值必须匹配。如果找不到匹配的行，模型将显示空行。
成功时返回`true`;否则返回`false`。

### `[virtual protected] QString QSqlTableModel::selectStatement() const`

**作用与语义：**

返回内部用于填充模型的 SQL `SELECT` 语句。该语句包含过滤器和 `ORDER BY` 子句。

### `[override virtual] bool QSqlTableModel::setData(const QModelIndex &index, const QVariant &value, int role = Qt::EditRole)`

**作用与语义：**

重实现自：`QAbstractItemModel::setData`（const QModelIndex & index，const QVariant & value，int role）。
将角色`role`的项目数据设置为`value` `index`。
对于编辑策略`OnFieldChange`，只有当没有其他索引缓存变更时，索引才可以接收变更。变更会立即提交。然而，尚未插入数据库的行可以自由更改，且不会自动提交。提交的变更失败时不会被恢复。
对于`OnRowChange`，只有当没有其他行有缓存变更时，索引才可以接收变更。变更不会自动提交。
如果`value`等于当前值，返回`true`。但该值不会提交到数据库。
返回`true`值是否可以设置或假，例如`index`超出边界。
如果角色不`Qt::EditRole`，返回`false`。要设置除 EditRole 以外的角色数据，可以使用自定义代理模型或子类 `QSqlTableModel`。

### `[virtual] void QSqlTableModel::setEditStrategy(QSqlTableModel::EditStrategy strategy)`

**作用与语义：**

将数据库中编辑数值的策略设置为`strategy`。
这样可以回退所有待处理的变更。

### `[virtual] void QSqlTableModel::setFilter(const QString &filter)`

**作用与语义：**

将电流滤波器设置为`filter`。
过滤器是一个没有关键词`WHERE`的SQL `WHERE`子句（例如，`name='Josephine')`）。
如果模型已经被数据库填充，模型会用新的筛选器重新选择该模型。否则，下次调用`select()`时会应用该筛选器。

### `[protected] void QSqlTableModel::setPrimaryKey(const QSqlIndex &key)`

**作用与语义：**

保护方法允许子类将主键设置为`key`。
通常，每当你打电话`setTable()`时，主索引会自动设置。

### `bool QSqlTableModel::setRecord(int row, const QSqlRecord &values)`

**作用与语义：**

`values`应用于模型中的`row`。源场和目标场按场名映射，而非记录中的位置。
请注意，`values`中生成的标志被保留，以确定提交到数据库时是否使用相应字段。默认情况下，该标志对`QSqlRecord`中的所有字段都设置为`true`。你必须将标志设置为`false`，`values`中的任意值都使用`setGenerated`（false），才能将更改保存回数据库。
对于编辑策略`OnFieldChange`和`OnRowChange`，只有当没有其他行有缓存变更时，行才可以接收变更。变更会立即提交。提交的变更失败时不会被恢复。
如果所有值都可以设置，则返回`true`;否则返回false。

### `[virtual] void QSqlTableModel::setSort(int column, Qt::SortOrder order)`

**作用与语义：**

将`column`的排序顺序设置为`order`。这不会影响当前数据，要用新的排序顺序刷新数据，请调用`select()`。

### `[virtual] void QSqlTableModel::setTable(const QString &tableName)`

**作用与语义：**

将模型运行的数据库表设置为`tableName`。不从表中选择数据，而是获取其字段信息。
要将表中的数据填充模型，请调用`select()`。
错误信息可以通过`lastError()`检索。

### `[override virtual] void QSqlTableModel::sort(int column, Qt::SortOrder order)`

**作用与语义：**

重实现自：`QAbstractItemModel::sort`（整数列，Qt：：排序顺序）。
按`column`排序和排序顺序`order`排序。这会立即选择数据，使用 `setSort()` 设置排序顺序，而不填充模型数据。

### `[override virtual slot] bool QSqlTableModel::submit()`

**作用与语义：**

重装：`QAbstractItemModel::submit()`。
当用户停止编辑当前行时，项目代理调用了这个重新实现的槽位。
如果模型的策略设置为`OnRowChange`或`OnFieldChange`，则提交当前编辑的行。对`OnManualSubmit`策略没有任何作用。
使用`submitAll()`提交所有待处理的`OnManualSubmit`策略变更。
成功时返回`true`;否则返回`false`。使用`lastError()`查询详细错误信息。
不会自动重新填充模型。提交的行在成功后会从数据库中刷新。

### `[slot] bool QSqlTableModel::submitAll()`

**作用与语义：**

提交所有待处理的变更，成功后`true`返回。错误时`false`返回，详细信息可通过`lastError()`获得。
`OnManualSubmit`，成功后模型将重新填充。任何呈现该模型的视图将失去其选择。
注意：在`OnManualSubmit`模式下，已提交的更改在 submitAll() 失败时不会从缓存中清除。这使得交易可以回滚并重新提交，而不会丢失数据。

### `QString QSqlTableModel::tableName() const`

**作用与语义：**

返回当前选择的表名称。

### `[virtual protected] bool QSqlTableModel::updateRowInTable(int row, const QSqlRecord &values)`

**作用与语义：**

用指定的`values`更新当前活跃数据库表中的指定`row`。如果成功返回`true`;否则返回`false`。
这是一种底层方法，直接运行在数据库上，不应直接调用。使用`setData()`来更新数值。模型会根据其编辑策略决定何时修改数据库。
注意，只有设置了生成标志的值才会被更新。生成标志可以用`QSqlRecord::setGenerated()`设置并用`QSqlRecord::isGenerated()`测试。

## 6. 深入实践与常见坑

### 生命周期和资源边界

连接由连接名识别，查询和模型引用连接。关闭或移除连接前必须销毁仍引用它的 query、model 和 database 句柄；不同线程不要共用连接。

### 状态和错误边界

区分连接是否打开、语句是否执行成功、游标是否定位在有效行、字段是否存在以及事务是否提交成功。`exec()` 成功不代表有结果行，`next()` 成功后才可以安全读取当前行。

### 线程边界

Qt SQL 连接有线程归属，每个线程应建立自己的连接并使用唯一连接名；不要把一个线程创建的 QSqlDatabase 或 QSqlQuery 传到另一个线程继续使用。

### 最容易出现的错误

不要在 data() 中修改数据；不要返回过期索引；不要用全量 reset 代替精确结构通知，除非确实无法描述变化。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QSqlTableModel` 所属机制类型：Qt SQL 连接、查询与事务机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
