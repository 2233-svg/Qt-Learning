# QSqlQuery

> Qt 6.11.1 · Qt SQL

## 1. 先建立直觉

**一句话定位：** `QSqlQuery` 执行 SQL 语句、绑定参数、遍历结果并提供错误信息，是 Qt SQL 的直接查询接口。

**模块背景：** Qt SQL 提供数据库连接、查询、事务和 SQL 模型/视图集成。

### 这是什么

`QSqlQuery` 执行 SQL 语句、绑定参数、遍历结果并提供错误信息，是 Qt SQL 的直接查询接口。

**内部模型：** 一次 QSqlQuery 对应一次语句执行和结果游标；exec 后通过 next/first/last 移动游标，再通过 value 读取列。prepare/bindValue 能把数据和 SQL 结构分开。

**适用场景：** 需要精确 SQL、事务控制、批量操作或不适合直接用模型时使用。只查询表格展示时可考虑 QSqlQueryModel。

**典型调用链：** 构造 query(database) -> prepare -> bindValue -> exec -> next -> value -> lastError -> 结束时释放。

**先记住的坑：** 不要拼接用户输入形成 SQL；exec 成功不代表结果有行；列名和索引要核对；长事务会锁表或阻塞其他请求。

## 2. 依赖与对象关系

- 头文件：`#include <QSqlQuery>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Sql)
target_link_libraries(mytarget PRIVATE Qt6::Sql)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

一次 QSqlQuery 对应一次语句执行和结果游标；exec 后通过 next/first/last 移动游标，再通过 value 读取列。prepare/bindValue 能把数据和 SQL 结构分开。

### 状态、生命周期和线程

**生命周期：** 连接由连接名识别，查询和模型引用连接。关闭或移除连接前必须销毁仍引用它的 query、model 和 database 句柄；不同线程不要共用连接。

**状态与结果：** 区分连接是否打开、语句是否执行成功、游标是否定位在有效行、字段是否存在以及事务是否提交成功。`exec()` 成功不代表有结果行，`next()` 成功后才可以安全读取当前行。

**线程与事件循环：** Qt SQL 连接有线程归属，每个线程应建立自己的连接并使用唯一连接名；不要把一个线程创建的 QSqlDatabase 或 QSqlQuery 传到另一个线程继续使用。

## 3. 直接使用

需要精确 SQL、事务控制、批量操作或不适合直接用模型时使用。只查询表格展示时可考虑 QSqlQueryModel。 使用时通常按这个过程组织：构造 query(database) -> prepare -> bindValue -> exec -> next -> value -> lastError -> 结束时释放。

```cpp
#include <QSqlQuery>

QSqlQuery query;
query.prepare(QStringLiteral("SELECT name FROM users WHERE id = :id"));
query.bindValue(QStringLiteral(":id"), userId);
if (query.exec() && query.next())
    const QString name = query.value(0).toString();
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum BatchExecutionMode { ValuesAsRows, ValuesAsColumns }`

### 属性

- `(since 6.8) forwardOnly : bool`
- `(since 6.8) numericalPrecisionPolicy : QSql::NumericalPrecisionPolicy`
- `(since 6.8) positionalBindingEnabled : bool`

### 公有函数

- `QSqlQuery(QSqlResult *result)`
- `QSqlQuery(const QSqlDatabase &db)`
- `QSqlQuery(const QString &query = QString(), const QSqlDatabase &db = QSqlDatabase())`
- `(since 6.2) QSqlQuery(QSqlQuery &&other)`
- `~QSqlQuery()`
- `void addBindValue(const QVariant &val, QSql::ParamType paramType = QSql::In)`
- `int at() const`
- `void bindValue(const QString &placeholder, const QVariant &val, QSql::ParamType paramType = QSql::In)`
- `void bindValue(int pos, const QVariant &val, QSql::ParamType paramType = QSql::In)`
- `QVariant boundValue(const QString &placeholder) const`
- `QVariant boundValue(int pos) const`
- `(since 6.6) QString boundValueName(int pos) const`
- `(since 6.6) QStringList boundValueNames() const`
- `(since 6.0) QVariantList boundValues() const`
- `void clear()`
- `const QSqlDriver * driver() const`
- `bool exec()`
- `bool exec(const QString &query)`
- `bool execBatch(QSqlQuery::BatchExecutionMode mode = ValuesAsRows)`
- `QString executedQuery() const`
- `void finish()`
- `bool first()`
- `bool isActive() const`
- `bool isForwardOnly() const`
- `bool isNull(int field) const`
- `bool isNull(QAnyStringView name) const`
- `(since 6.7) bool isPositionalBindingEnabled() const`
- `bool isSelect() const`
- `bool isValid() const`
- `bool last()`
- `QSqlError lastError() const`
- `QVariant lastInsertId() const`
- `QString lastQuery() const`
- `bool next()`
- `bool nextResult()`
- `int numRowsAffected() const`
- `QSql::NumericalPrecisionPolicy numericalPrecisionPolicy() const`
- `bool prepare(const QString &query)`
- `bool previous()`
- `QSqlRecord record() const`
- `const QSqlResult * result() const`
- `bool seek(int index, bool relative = false)`
- `void setForwardOnly(bool forward)`
- `void setNumericalPrecisionPolicy(QSql::NumericalPrecisionPolicy precisionPolicy)`
- `(since 6.7) void setPositionalBindingEnabled(bool enable)`
- `int size() const`
- `(since 6.2) void swap(QSqlQuery &other)`
- `QVariant value(int index) const`
- `QVariant value(QAnyStringView name) const`
- `(since 6.2) QSqlQuery & operator=(QSqlQuery &&other)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[since 6.8] forwardOnly : bool`

**作用与语义：**

该属性仅满足前向模式。如果 `forward` 为真，则只允许 `next()` 和 `seek()` 值为正，用于导航结果。
仅前进模式（视驱动程序而定）可能更节省内存，因为不需要缓存结果。它也会提升某些数据库的性能。要实现这一点，你必须在准备或执行查询前调用`setForwardOnly()`。注意，接受查询和数据库的构造函数可能会执行查询。
仅前进模式默认关闭。
将只转发设置为假是对数据库引擎的建议，数据库引擎拥有最终决定结果集是仅转发还是可滚动的。`isForwardOnly()`总是返回结果集的正确状态。
注意：查询执行后调用`setForwardOnly`，最多会导致意外结果，最坏情况下会导致崩溃。
注意：为了确保仅转发查询成功完成，应用程序不仅应在执行查询后检查`lastError()`错误，也应在浏览查询结果后进行检查。
警告：PostgreSQL：在仅前向模式下浏览查询结果时，请不要在同一数据库连接上执行任何其他SQL命令。否则查询结果会丢失。

**如何使用：** 调用 `forwardOnly()` 读取当前值；它不会修改应用状态。

### `[since 6.8] numericalPrecisionPolicy : QSql::NumericalPrecisionPolicy`

**作用与语义：**

指示数据库驱动程序以`precisionPolicy`指定的精度返回数值。
例如，Oracle 驱动程序可以将数值以字符串形式检索，以防止精度损失。如果高精度无所谓，使用该方法通过绕过字符串转换来提高执行速度。
注意：不支持低精度取数值的驱动程序将忽略精度策略。您可以使用`QSqlDriver::hasFeature()`来了解驱动程序是否支持此功能。
注意：设置精度策略不会影响当前激活的查询。调用 `exec`（QString） 或 `prepare()` 以激活该策略。

**如何使用：** 调用 `numericalPrecisionPolicy()` 读取当前值；它不会修改应用状态。

### `[since 6.8] positionalBindingEnabled : bool`

**作用与语义：**

该属性根据`enable`启用或禁用该查询的位置`binding`（默认为`true`）。禁用位置绑定在查询本身包含“？”时非常有用，该“？”不应作为位置绑定参数处理，例如作为PostgreSQL数据库的JSON操作符。
当数据库原生支持带问号的位置绑定时，该属性无效（参见`QSqlDriver::PositionalPlaceholders`）。

**如何使用：** 调用 `positionalBindingEnabled()` 读取当前值；它不会修改应用状态。

### `[explicit] QSqlQuery::QSqlQuery(QSqlResult *result)`

**作用与语义：**

构建一个 QSqlQuery 对象，利用该`QSqlResult` `result`与数据库通信。

### `[explicit] QSqlQuery::QSqlQuery(const QSqlDatabase &db)`

**作用与语义：**

利用数据库`db`构建QSqlQuery对象。如果`db`无效，将使用应用的默认数据库。

### `[explicit] QSqlQuery::QSqlQuery(const QString &query = QString(), const QSqlDatabase &db = QSqlDatabase())`

**作用与语义：**

利用 SQL `query` 和数据库`db`构造 QSqlQuery 对象。如果未指定 `db` 或无效，则使用应用的默认数据库。如果 `query` 不是空字符串，则执行该字符串。

### `[noexcept, since 6.2] QSqlQuery::QSqlQuery(QSqlQuery &&other)`

**作用与语义：**

Move-构造一个QSqlQuery，`other`。

### `[noexcept] QSqlQuery::~QSqlQuery()`

**作用与语义：**

摧毁该物体并释放所有分配的资源。

### `void QSqlQuery::addBindValue(const QVariant &val, QSql::ParamType paramType = QSql::In)`

**作用与语义：**

使用位置值绑定时，将值 `val` 添加到值列表中。addBindValue() 调用的顺序决定了值在准备查询中绑定到哪个占位符。如果`paramType` `QSql::Out`或`QSql::InOut`，占位符将在`exec()`调用后被数据库中的数据覆盖。
绑定 NULL 值时，使用空`QVariant`;例如，绑定字符串时使用`QVariant(QMetaType::fromType<QString>())`。

### `int QSqlQuery::at() const`

**作用与语义：**

返回查询当前内部位置。第一个记录位于位置零。如果位置无效，函数返回`QSql::BeforeFirstRow`或`QSql::AfterLastRow`，这些都是特殊的负值。

### `void QSqlQuery::bindValue(const QString &placeholder, const QVariant &val, QSql::ParamType paramType = QSql::In)`

**作用与语义：**

将占位符`placeholder`设置为绑定到预备语句中的值 `val`。请注意，在指定占位符名称时必须包含占位标记（例如 `:`）。如果`paramType`是`QSql::Out`或`QSql::InOut`，占位符将在`exec()`调用后被数据库中的数据覆盖。此时，必须预先分配足够的空间来存储结果。
绑定 NULL 值时，使用空 `QVariant`;例如，绑定字符串时使用 `QVariant(QMetaType::fromType<QString>())`。

### `void QSqlQuery::bindValue(int pos, const QVariant &val, QSql::ParamType paramType = QSql::In)`

**作用与语义：**

将占位符设在 `pos` 的位置，使其绑定到预备语句中的值 `val`。字段编号从 0 开始。如果`paramType` `QSql::Out` 或 `QSql::InOut`，`exec()`调用后占位符将被数据库中的数据覆盖。

### `QVariant QSqlQuery::boundValue(const QString &placeholder) const`

**作用与语义：**

返回`placeholder`的值。

### `QVariant QSqlQuery::boundValue(int pos) const`

**作用与语义：**

返回位置`pos`的占位符值。

### `[since 6.6] QString QSqlQuery::boundValueName(int pos) const`

**作用与语义：**

返回位置`pos`的绑定值名称。
列表的顺序是按绑定顺序排列，无论使用命名还是位置绑定。

### `[since 6.6] QStringList QSqlQuery::boundValueNames() const`

**作用与语义：**

返回所有绑定值的名称。
列表的顺序是按绑定顺序排列，无论使用命名还是位置绑定。

### `[since 6.0] QVariantList QSqlQuery::boundValues() const`

**作用与语义：**

返回一组绑定值。
列表的顺序是按绑定顺序排列，无论使用命名还是位置绑定。
界限值可以通过以下方式进行考察：

**官方示例：**

```cpp
     const QVariantList list = query.boundValues();
     for (qsizetype i = 0; i < list.size(); ++i)
         qDebug() << i << ":" << list.at(i).toString();
```

### `void QSqlQuery::clear()`

**作用与语义：**

清除结果集并释放查询持有的所有资源。将查询状态设置为非活跃状态。你几乎不需要调用这个函数。

### `const QSqlDriver *QSqlQuery::driver() const`

**作用与语义：**

返回与查询关联的数据库驱动。

### `bool QSqlQuery::exec()`

**作用与语义：**

执行事先准备好的SQL查询。如果查询成功执行，返回`true`;否则返回`false`。
注意，当调用exec()时，该查询的最后一个错误会被重置。

### `bool QSqlQuery::exec(const QString &query)`

**作用与语义：**

以`query`方式执行 SQL。如果查询成功，返回 `true`，并将查询状态设置为 `active`;否则返回 `false`。`query`字符串必须使用适合查询的 SQL 数据库的语法（例如标准 SQL）。
查询执行后，查询会被定位在无效记录上，必须先导航到有效记录后才能检索数据值（例如，使用`next()`）。
注意，当调用exec()时，该查询的最后一个错误会被重置。
对于 SQLite，查询字符串一次只能包含一个语句。如果给出多个语句，函数返回 `false`。

**官方示例：**

```cpp
     QSqlQuery query;
     query.exec("INSERT INTO employee (id, name, salary) "
                "VALUES (1001, 'Thad Beaumont', 65000)");
```

### `bool QSqlQuery::execBatch(QSqlQuery::BatchExecutionMode mode = ValuesAsRows)`

**作用与语义：**

批量执行事先准备好的SQL查询。所有绑定参数必须是变体列表。如果数据库不支持批处理，驱动将使用常规`exec()`调用来模拟。
如果查询成功执行，返回`true`;否则返回`false`。
上述示例在`myTable`中插入了四行新行：
要绑定 NULL 值，必须在绑定`QVariantList`中添加一个相关类型的 null 的 `QVariant`;例如，如果你使用字符串，应使用 `QVariant(QMetaType::fromType<QString>())`。
注意：每个绑定`QVariantList`必须包含相同数量的变体。
注意：列表中QVariant的类型不得更改。例如，`QVariantList`中不能混合整数和字符串变体。
`mode`参数表示绑定`QVariantList`将如何解释。如果`mode`是`ValuesAsRows`，`QVariantList`中的每个变体都会被解释为新行的值。`ValuesAsColumns`是Oracle驱动程序的一个特殊情况。在此模式下，`QVariantList`中的每个条目都被解释为存储过程中IN或OUT值的数组值。注意，这仅在IN或OUT值是仅由基本类型一列组成的表类型时有效，例如`TYPE myType IS TABLE OF VARCHAR(64) INDEX BY BINARY_INTEGER;`。

**官方示例：**

```cpp
 QSqlQuery q;
 q.prepare("insert into myTable values (?, ?)");

 QVariantList ints;
 ints << 1 << 2 << 3 << 4;
 q.addBindValue(ints);

 QVariantList names;
 names << "Harald" << "Boris" << "Trond" << QVariant(QMetaType::fromType<QString>());
 q.addBindValue(names);

 if (!q.execBatch())
     qDebug() << q.lastError();
```

### `QString QSqlQuery::executedQuery() const`

**作用与语义：**

返回上一次成功执行的查询。
在大多数情况下，该函数返回与`lastQuery()`相同的字符串。如果在不支持占位符的数据库系统上执行了带占位符的预备查询，则会模拟该查询的准备过程。原始查询中的占位符会被替换为其绑定值，形成新的查询。该函数返回修改后的查询。它主要用于调试目的。

### `void QSqlQuery::finish()`

**作用与语义：**

指示数据库驱动程序，在重新执行该查询之前，不会再从该查询获取数据。通常不需要调用该函数，但如果你打算以后重用该查询，调用它可能会帮助释放锁或光标等资源。
将查询设置为非活跃状态。绑定值保留其值。

### `bool QSqlQuery::first()`

**作用与语义：**

如果有，检索结果中的第一个记录，并将查询定位在检索到的记录上。注意，结果必须处于`active`状态，`isSelect()`在调用该函数前必须返回 true，否则它什么都不做并返回 false。如果成功，返回 `true`。如果失败，查询位置将被设置为无效位置，返回 false。

### `bool QSqlQuery::isActive() const`

**作用与语义：**

如果查询处于激活状态，返回`true`。活跃的 `QSqlQuery` 是指已经成功`exec()`但尚未完成的查询。当你完成一个活跃查询后，可以通过调用 `finish()` 或 `clear()` 使查询处于非活跃状态，或者删除`QSqlQuery`实例。
注意：特别值得关注的是作为`SELECT`语句的活跃查询。对于支持事务的数据库，作为`SELECT`语句的活跃查询可能导致`commit()`或`rollback()`失败，因此在提交或回滚之前，应利用上述方法使活跃`SELECT`语句查询非活跃。

### `bool QSqlQuery::isForwardOnly() const`

**作用与语义：**

该属性仅满足前向模式。如果 `forward` 为真，则只允许 `next()` 和 `seek()` 值为正，用于导航结果。
仅前进模式（视驱动程序而定）可能更节省内存，因为不需要缓存结果。它也会提升某些数据库的性能。要实现这一点，你必须在准备或执行查询前调用`setForwardOnly()`。注意，接受查询和数据库的构造函数可能会执行查询。
仅前进模式默认关闭。
将只转发设置为假是对数据库引擎的建议，数据库引擎拥有最终决定结果集是仅转发还是可滚动的。`isForwardOnly()`总是返回结果集的正确状态。
注意：查询执行后调用`setForwardOnly`，最多会导致意外结果，最坏情况下会导致崩溃。
注意：为了确保仅转发查询成功完成，应用程序不仅应在执行查询后检查`lastError()`错误，也应在浏览查询结果后进行检查。
警告：PostgreSQL：在仅前向模式下浏览查询结果时，请不要在同一数据库连接上执行任何其他SQL命令。否则查询结果会丢失。

**如何使用：** 调用 `isForwardOnly()` 读取当前值；它不会修改应用状态。

### `bool QSqlQuery::isNull(int field) const`

**作用与语义：**

返回 `true`如果查询不是 `active`、查询未定位在有效记录上、不存在此类`field`，或`field`为空;否则则`false`。注意，对于某些驱动程序，isNull() 直到尝试检索数据后才会返回准确信息。

### `bool QSqlQuery::isNull(QAnyStringView name) const`

**作用与语义：**

如果没有具有该`name`的字段，返回 `true`;否则返回对应字段索引的 isNull（int 索引）。
这种重载效率低于`isNull()`。
注意：在6.8之前的Qt版本中，该函数采用`QString`，而非`QAnyStringView`。

### `[since 6.7] bool QSqlQuery::isPositionalBindingEnabled() const`

**作用与语义：**

该属性根据`enable`启用或禁用该查询的位置`binding`（默认为`true`）。禁用位置绑定在查询本身包含“？”时非常有用，该“？”不应作为位置绑定参数处理，例如作为PostgreSQL数据库的JSON操作符。
当数据库原生支持带问号的位置绑定时，该属性无效（参见`QSqlDriver::PositionalPlaceholders`）。

**如何使用：** 调用 `isPositionalBindingEnabled()` 读取当前值；它不会修改应用状态。

### `bool QSqlQuery::isSelect() const`

**作用与语义：**

如果当前查询是`SELECT`语句，返回`true`;否则返回`false`。

### `bool QSqlQuery::isValid() const`

**作用与语义：**

如果查询当前位于有效记录上，返回`true`;否则返回`false`。

### `bool QSqlQuery::last()`

**作用与语义：**

检索结果中最后一条记录（如有），并将查询定位在检索记录上。注意，结果必须处于`active`状态，且`isSelect()`在调用该函数前必须返回true，否则将无所作为并返回false。如果成功，返回`true`。如果失败，查询位置将被设置为无效位置，返回false。

### `QSqlError QSqlQuery::lastError() const`

**作用与语义：**

返回关于该查询中最后一次出现错误（如有错误）的错误信息。

### `QVariant QSqlQuery::lastInsertId() const`

**作用与语义：**

如果数据库支持，返回最近插入行的对象 ID。如果查询未插入任何值或数据库未返回该 id，则返回无效`QVariant`。如果插入触及了多行，行为未定义。
对于MySQL数据库，行的自动递增字段将返回。
注意：为了使该函数在 PSQL 中工作，表必须包含 OID，而这些 OID 可能并非默认创建。请检查 `default_with_oids` 配置变量以确认。

### `QString QSqlQuery::lastQuery() const`

**作用与语义：**

返回当前查询的文本，若无当前查询文本则返回空字符串。

### `bool QSqlQuery::next()`

**作用与语义：**

如果有，检索结果中的下一条记录，并将查询定位在检索到的记录上。注意，结果必须处于`active`状态，且`isSelect()`在调用该函数前必须返回真，否则将无所作为并返回假。
适用以下规则：
- 如果结果目前位于第一条记录之前，例如查询刚执行后，则尝试检索第一条记录。
- 如果结果目前位于最后一条记录之后，则没有变化，返回假。
- 如果结果位于中间某处，则尝试检索下一条记录。
如果无法检索记录，结果会被放置在最后一条记录之后，返回false。如果记录被成功检索，则返回true。

### `bool QSqlQuery::nextResult()`

**作用与语义：**

丢弃当前结果集，如果有就导航到下一个。
一些数据库能够返回存储过程或SQL批处理（包含多个语句的查询字符串）的多个结果集。如果查询执行后有多个结果集可用，该函数可用于导航到下一个结果集。
如果有新的结果集，该函数将返回true。查询会被重新定位到新结果集中的无效记录，必须先导航到有效记录后才能检索数据值。如果没有新的结果集，函数返回`false`，查询被设置为非活跃状态。无论如何，旧的结果集将被丢弃。
当某个语句是非选择语句时，可能只能提供受影响行的计数，而不是结果集。
注意，某些数据库，如 Microsoft SQL Server，在处理多个结果集时要求不可滚动光标。有些数据库可能一次性执行所有语句，而有些则可能延迟执行，直到结果集被实际访问，且有些数据库可能对 SQL 批处理中使用的语句有限制。

### `int QSqlQuery::numRowsAffected() const`

**作用与语义：**

返回受结果SQL语句影响的行数，若无法确定则返回-1行。注意对于`SELECT`语句，值未定义;请使用`size()`。如果查询未`active`，返回-1。

### `QSql::NumericalPrecisionPolicy QSqlQuery::numericalPrecisionPolicy() const`

**作用与语义：**

返回 numicalPrecisionPolicy。
注意：属性 numericalPrecisionPolicy 的获取函数。

### `bool QSqlQuery::prepare(const QString &query)`

**作用与语义：**

准备SQL查询`query`执行。如果查询成功准备，返回`true`;否则返回`false`。
查询可以包含绑定值的占位符。支持Oracle风格的冒号名（例如`:surname`）和ODBC风格（`?`）占位符;但不能在同一查询中混合使用。示例请参见详细说明。
可移植性说明：有些数据库选择延迟准备查询，直到首次执行。在这种情况下，准备语法错误的查询成功，但每连续`exec()`都会失败。当数据库不直接支持命名占位符时，占位符只能包含范围为 [a-zA-Z0-9_] 的字符。
对于SQLite，查询字符串一次只能包含一个语句。如果给出多个语句，函数返回`false`。

**官方示例：**

```cpp
     QSqlQuery query;
     query.prepare("INSERT INTO person (id, forename, surname) "
                   "VALUES (:id, :forename, :surname)");
     query.bindValue(":id", 1001);
     query.bindValue(":forename", "Bart");
     query.bindValue(":surname", "Simpson");
     query.exec();
```

### `bool QSqlQuery::previous()`

**作用与语义：**

如果有，检索结果中的前一条记录，并将查询定位在检索到的记录上。注意，结果必须处于`active`状态，且`isSelect()`在调用该函数前必须返回true，否则它将无所作为并返回false。
适用以下规则：
- 如果结果当前位于第一条记录之前，则无变化，返回错误。
- 如果结果目前位于最后一条记录之后，则尝试检索最后一条记录。
- 如果结果介于中间，尝试检索上一条记录。
如果无法检索记录，结果会被放置在第一个记录之前，返回 false。如果记录被成功检索，则返回 true。

### `QSqlRecord QSqlQuery::record() const`

**作用与语义：**

返回包含当前查询字段信息的 `QSqlRecord`。如果查询指向有效行（`isValid()` 返回为真），记录将填充该行的值。当没有活动查询时返回空记录（`isActive()`返回 false）。
要从查询中获取值，应使用`value()`，因为它基于索引的查找更快。
在以下示例中，执行`SELECT * FROM`查询。由于列的顺序未定义，`QSqlRecord::indexOf()`用于获取列的索引。

**官方示例：**

```cpp
 QSqlQuery q("select * from employees");
 QSqlRecord rec = q.record();

 qDebug() << "Number of columns: " << rec.count();

 int nameCol = rec.indexOf("name"); // index of the field "name"
 while (q.next())
     qDebug() << q.value(nameCol).toString(); // output all names
```

### `const QSqlResult *QSqlQuery::result() const`

**作用与语义：**

返回与查询相关的结果。

### `bool QSqlQuery::seek(int index, bool relative = false)`

**作用与语义：**

如果有，检索位置`index`的记录，并将查询定位在检索到的记录上。第一个记录位于位置0。注意查询必须处于`active`状态，且`isSelect()`必须返回true才能调用该函数。
如果`relative`为假（默认），则适用以下规则：
- 如果`index`为负，结果会被置于第一个记录之前，返回假。
- 否则，尝试移动到位置`index`的记录。如果无法检索位置`index`记录，则结果被定位在最后一条记录之后，返回false。如果记录成功检索，返回true。
如果`relative`为真，则适用以下规则：
- 如果结果目前位于第一条记录之前，且：
`index`为负或零，则无变化，返回假值。
`index`为正，尝试将结果定位在绝对位置`index` - 1，遵循上述非相对寻觅的相同规则。
- 如果结果目前位于最后记录之后，且：
`index`为正或为零，则无变化，返回假。
`index`为负，则尝试将结果定位为相较于最后记录的`index` 1相对位置，遵循以下规则。
- 如果结果目前位于中间某处，且相对偏移量`index`使结果低于零，则结果位于第一个记录之前，返回假。
- 否则，尝试移动到当前记录前`index`记录（或如果`index`为负，则移动到当前记录后方的`index`条记录）。如果偏移`index`的记录无法检索，则如果`index` >= 0，结果会被放在最后一条记录之后;如果`index`为负，则返回第一条记录之前），返回false。如果记录被成功检索，返回true。

### `void QSqlQuery::setForwardOnly(bool forward)`

**作用与语义：**

该属性仅满足前向模式。如果 `forward` 为真，则只允许 `next()` 和 `seek()` 值为正，用于导航结果。
仅前进模式（视驱动程序而定）可能更节省内存，因为不需要缓存结果。它也会提升某些数据库的性能。要实现这一点，你必须在准备或执行查询前调用`setForwardOnly()`。注意，接受查询和数据库的构造函数可能会执行查询。
仅前进模式默认关闭。
将只转发设置为假是对数据库引擎的建议，数据库引擎拥有最终决定结果集是仅转发还是可滚动的。`isForwardOnly()`总是返回结果集的正确状态。
注意：查询执行后调用`setForwardOnly`，最多会导致意外结果，最坏情况下会导致崩溃。
注意：为了确保仅转发查询成功完成，应用程序不仅应在执行查询后检查`lastError()`错误，也应在浏览查询结果后进行检查。
警告：PostgreSQL：在仅前向模式下浏览查询结果时，请不要在同一数据库连接上执行任何其他SQL命令。否则查询结果会丢失。

**如何使用：** 调用 `setForwardOnly(...)` 修改 `forwardOnly`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QSqlQuery::setNumericalPrecisionPolicy(QSql::NumericalPrecisionPolicy precisionPolicy)`

**作用与语义：**

指示数据库驱动程序以`precisionPolicy`指定的精度返回数值。
例如，Oracle 驱动程序可以将数值以字符串形式检索，以防止精度损失。如果高精度无所谓，使用该方法通过绕过字符串转换来提高执行速度。
注意：不支持低精度取数值的驱动程序将忽略精度策略。您可以使用`QSqlDriver::hasFeature()`来了解驱动程序是否支持此功能。
注意：设置精度策略不会影响当前激活的查询。调用 `exec`（QString） 或 `prepare()` 以激活该策略。

**如何使用：** 调用 `setNumericalPrecisionPolicy(...)` 修改 `numericalPrecisionPolicy`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `[since 6.7] void QSqlQuery::setPositionalBindingEnabled(bool enable)`

**作用与语义：**

该属性根据`enable`启用或禁用该查询的位置`binding`（默认为`true`）。禁用位置绑定在查询本身包含“？”时非常有用，该“？”不应作为位置绑定参数处理，例如作为PostgreSQL数据库的JSON操作符。
当数据库原生支持带问号的位置绑定时，该属性无效（参见`QSqlDriver::PositionalPlaceholders`）。

**如何使用：** 调用 `setPositionalBindingEnabled(...)` 修改 `positionalBindingEnabled`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `int QSqlQuery::size() const`

**作用与语义：**

返回结果大小（返回行数），如果无法确定大小或数据库不支持查询大小的报告，则返回 -1。注意，对于非`SELECT`语句（`isSelect()`返回 `false`），size() 返回 -1。如果查询未激活（`isActive()` 返回 `false`），则返回 -1。
要确定非`SELECT`语句影响的行数，请使用`numRowsAffected()`。

### `[noexcept, since 6.2] void QSqlQuery::swap(QSqlQuery &other)`

**作用与语义：**

将该查询与`other`交换。该操作非常快且从未失败。

### `QVariant QSqlQuery::value(int index) const`

**作用与语义：**

返回当前记录中的字段`index`值。
字段从左到右编号，使用`SELECT`语句的文本，例如在。
字段0为`forename`，字段1为`surname`。不建议使用`SELECT *`，因为查询字段的顺序未定义。
如果字段`index`不存在、查询处于非活动状态，或查询位于无效记录上，则返回无效`QVariant`。

**官方示例：**

```cpp
 SELECT forename, surname FROM people;
```

### `QVariant QSqlQuery::value(QAnyStringView name) const`

**作用与语义：**

返回当前记录中称为 `name` 的字段的值。如果字段 `name` 不存在，则返回无效变体。这种超载效率低于 `value()` 注意：在 6.8 之前的 Qt 版本中，该函数使用 `QString`，而非`QAnyStringView`。

### `[noexcept, since 6.2] QSqlQuery &QSqlQuery::operator=(QSqlQuery &&other)`

**作用与语义：**

Move-assign `other`该对象。

### `enum BatchExecutionMode { ValuesAsRows, ValuesAsColumns }`

**作用与语义：**

- `QSqlQuery::ValuesAsRows`：`0`;- 更新多行。将`QVariantList`中的每个条目视为更新下一行的值。
- `QSqlQuery::ValuesAsColumns`：`1`;- 更新一行。将`QVariantList`中的每个条目视为数组类型的单一值。

## 6. 深入实践与常见坑

### 生命周期和资源边界

连接由连接名识别，查询和模型引用连接。关闭或移除连接前必须销毁仍引用它的 query、model 和 database 句柄；不同线程不要共用连接。

### 状态和错误边界

区分连接是否打开、语句是否执行成功、游标是否定位在有效行、字段是否存在以及事务是否提交成功。`exec()` 成功不代表有结果行，`next()` 成功后才可以安全读取当前行。

### 线程边界

Qt SQL 连接有线程归属，每个线程应建立自己的连接并使用唯一连接名；不要把一个线程创建的 QSqlDatabase 或 QSqlQuery 传到另一个线程继续使用。

### 最容易出现的错误

不要拼接用户输入形成 SQL；exec 成功不代表结果有行；列名和索引要核对；长事务会锁表或阻塞其他请求。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QSqlQuery` 所属机制类型：Qt SQL 连接、查询与事务机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
