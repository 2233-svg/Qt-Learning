# QSqlRelationalTableModel

> Qt 6.11.1 · Qt SQL

## 1. 先建立直觉

**一句话定位：** `QSqlRelationalTableModel` 是 Qt SQL 的“SqlRelational表格模型”类型，参与数据库连接、SQL 执行、事务或结果模型。

**模块背景：** Qt SQL 提供数据库连接、查询、事务和 SQL 模型/视图集成。

### 这是什么

`QSqlRelationalTableModel` 是模型/视图体系中的数据模型类型，向视图提供索引、角色数据和结构变化通知。

**内部模型：** 视图不应该直接操作底层容器；它通过 QModelIndex 和 data roles 查询模型。模型必须准确维护索引有效性以及插入、删除、移动时的通知顺序。

**适用场景：** 需要把自定义数据接入 QListView、QTableView、QTreeView 或代理模型时使用。

**典型调用链：** 准备数据源 -> 实现/配置模型 -> 连接 view -> 通过 data/flags/setData 读写 -> 发出 dataChanged 或 begin/end 结构通知。

**先记住的坑：** 不要在 data() 中修改数据；不要返回过期索引；不要用全量 reset 代替精确结构通知，除非确实无法描述变化。

## 2. 依赖与对象关系

- 头文件：`#include <QSqlRelationalTableModel>`
- 继承自：QSqlTableModel
- 直接派生类：未在类页中列出

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

- `enum JoinMode { InnerJoin, LeftJoin }`

### 公有函数

- `QSqlRelationalTableModel(QObject *parent = nullptr, const QSqlDatabase &db = QSqlDatabase())`
- `virtual ~QSqlRelationalTableModel()`
- `QSqlRelation relation(int column) const`
- `virtual QSqlTableModel * relationModel(int column) const`
- `void setJoinMode(QSqlRelationalTableModel::JoinMode joinMode)`
- `virtual void setRelation(int column, const QSqlRelation &relation)`

### 重实现的公有函数

- `virtual void clear() override`
- `virtual QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const override`
- `virtual bool removeColumns(int column, int count, const QModelIndex &parent = QModelIndex()) override`
- `virtual bool select() override`
- `virtual bool setData(const QModelIndex &index, const QVariant &value, int role = Qt::EditRole) override`
- `virtual void setTable(const QString &table) override`

### 公有槽函数

- `virtual void revertRow(int row) override`

### 重实现的保护函数

- `virtual bool insertRowIntoTable(const QSqlRecord &values) override`
- `virtual QString orderByClause() const override`
- `virtual QString selectStatement() const override`
- `virtual bool updateRowInTable(int row, const QSqlRecord &values) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QSqlRelationalTableModel::JoinMode`

**作用与语义：**

- `QSqlRelationalTableModel::InnerJoin`：`0`;- 内连接模式，当两个表至少有一个匹配时返回行。
- `QSqlRelationalTableModel::LeftJoin`：`1`;- 左连接模式，返回左表（table_name1）的所有行，即使右表（table_name2）中没有匹配。

### `[explicit] QSqlRelationalTableModel::QSqlRelationalTableModel(QObject *parent = nullptr, const QSqlDatabase &db = QSqlDatabase())`

**作用与语义：**

创建一个空的 QSqlRelationalTableModel，并将父节点设置为 `parent`，数据库连接设置为 `db`。如果`db`无效，则使用默认数据库连接。

### `[virtual noexcept] QSqlRelationalTableModel::~QSqlRelationalTableModel()`

**作用与语义：**

摧毁该物体并释放所有分配的资源。

### `[override virtual] void QSqlRelationalTableModel::clear()`

**作用与语义：**

重装：`QSqlTableModel::clear()`。

### `[override virtual] QVariant QSqlRelationalTableModel::data(const QModelIndex &index, int role = Qt::DisplayRole) const`

**作用与语义：**

重实现自：`QSqlTableModel::data`（const QModelIndex & index， int role） const.

### `[override virtual protected] bool QSqlRelationalTableModel::insertRowIntoTable(const QSqlRecord &values)`

**作用与语义：**

重实现自：`QSqlTableModel::insertRowIntoTable`（const QSqlRecord & values）。
将`values`值插入当前活跃的数据库表中。
这是一种底层方法，直接运行在数据库上，不应直接调用。使用`insertRow()`和`setData()`插入数值。模型会根据其编辑策略决定何时修改数据库。
如果可以插入这些值，返回`true`，否则为假。错误信息可以通过 `lastError()` 检索。

### `[override virtual protected] QString QSqlRelationalTableModel::orderByClause() const`

**作用与语义：**

重实现自：`QSqlTableModel::orderByClause()` const.
返回基于当前排序顺序的 SQL `ORDER BY` 子句。

### `QSqlRelation QSqlRelationalTableModel::relation(int column) const`

**作用与语义：**

返回列 `column` 的关系，若未设置关系则返回无效关系。

### `[virtual] QSqlTableModel *QSqlRelationalTableModel::relationModel(int column) const`

**作用与语义：**

返回一个`QSqlTableModel`对象，用于访问`column`为外键的表;如果给定`column`没有关系，则返回`nullptr`。
返回的对象归`QSqlRelationalTableModel`所有。

### `[override virtual] bool QSqlRelationalTableModel::removeColumns(int column, int count, const QModelIndex &parent = QModelIndex())`

**作用与语义：**

重实现自：`QSqlTableModel::removeColumns`（整数列，整数计数，cont QModelIndex 和父）。

### `[override virtual slot] void QSqlRelationalTableModel::revertRow(int row)`

**作用与语义：**

重装：`QSqlTableModel::revertRow`（int row）。
回撤指定`row`的所有更改。

### `[override virtual] bool QSqlRelationalTableModel::select()`

**作用与语义：**

重实现自：`QSqlTableModel::select()`。
用通过 `setTable()` 设置的表中的数据填充模型，使用指定的滤波器和排序条件，成功时返回 `true`;否则返回 `false`。
注意：调用 select() 将恢复所有未提交的更改并删除已插入的列。

### `[override virtual protected] QString QSqlRelationalTableModel::selectStatement() const`

**作用与语义：**

重装：`QSqlTableModel::selectStatement()` const.
返回内部用于填充模型的SQL `SELECT`语句。该语句包含过滤器和`ORDER BY`子句。

### `[override virtual] bool QSqlRelationalTableModel::setData(const QModelIndex &index, const QVariant &value, int role = Qt::EditRole)`

**作用与语义：**

重实现自：`QSqlTableModel::setData`（const QModelIndex & index， const QVariant & value， int role）。
将指定`index`设置到给定`value`的项目中该`role`的数据。根据编辑策略，该值可能一次性应用到数据库，也可以缓存到模型中。
返回`true`值是否可以被设置，或错误时为假（例如，如果`index`超出界限）。
对于关系列，`value`必须是索引，而非显示值。如果给定了索引，它也必须存在于被引用的表中，否则函数返回`false`。如果传递的是QVariant()而不是索引，索引将被清除。

### `void QSqlRelationalTableModel::setJoinMode(QSqlRelationalTableModel::JoinMode joinMode)`

**作用与语义：**

设置SQL的`joinMode`显示或隐藏带有NULL外键的行。在`InnerJoin`模式（默认）中，这些行不会显示：如果你想显示它们，可以使用`LeftJoin`模式。

### `[virtual] void QSqlRelationalTableModel::setRelation(int column, const QSqlRelation &relation)`

**作用与语义：**

设指定的`column`由`relation`指定为外部索引。
setRelation() 调用指定表`employee`中的第 2 列是一个外键，映射到表 `city` 的字段`id`，视图应向用户展示`city`的`name`字段。
注意：表的主键可能不包含与其他表的关系。

**官方示例：**

```cpp
     model->setTable("employee");

     model->setRelation(2, QSqlRelation("city", "id", "name"));
```

### `[override virtual] void QSqlRelationalTableModel::setTable(const QString &table)`

**作用与语义：**

重实现自：`QSqlTableModel::setTable`（const QString &tableName）。
将模型运行的数据库表设置为`tableName`。不从表中选择数据，但获取字段信息。
要用表的数据填充模型，请调用`select()`。
错误信息可以通过`lastError()`检索。

### `[override virtual protected] bool QSqlRelationalTableModel::updateRowInTable(int row, const QSqlRecord &values)`

**作用与语义：**

重实现自：`QSqlTableModel::updateRowInTable`（整数行，cont QSqlRecord & values）。
用指定的`values`更新当前活跃数据库表中的给定`row`。如果成功返回`true`;否则返回`false`。
这是一种直接在数据库上运行的低级方法，不应直接调用。使用`setData()`来更新数值。模型会根据其编辑策略决定何时修改数据库。
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

`QSqlRelationalTableModel` 所属机制类型：Qt SQL 连接、查询与事务机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
