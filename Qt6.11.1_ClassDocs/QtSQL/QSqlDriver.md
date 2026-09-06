# QSqlDriver

> Qt 6.11.1 · Qt SQL

## 1. 先建立直觉

**一句话定位：** `QSqlDriver` 是 Qt SQL 的“Sql驱动”类型，参与数据库连接、SQL 执行、事务或结果模型。

**模块背景：** Qt SQL 提供数据库连接、查询、事务和 SQL 模型/视图集成。

### 这是什么

`QSqlDriver` 是 Qt SQL 连接、查询与事务机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** Qt SQL 把驱动、连接、查询游标和模型分成不同对象。连接决定驱动和数据库会话，`QSqlQuery` 代表语句及其结果游标，事务把多条语句的提交边界固定下来，SQL 模型再把查询结果接到视图。

**适用场景：** 创建连接并检查 open，使用 prepare/bindValue 分离 SQL 结构和用户数据，执行后检查返回值和 lastError，遍历结果，必要时用 transaction/commit/rollback 包住一组操作。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要拼接用户输入形成 SQL；不要把 exec 成功当作有数据；不要在连接仍被引用时 removeDatabase；不要忽略驱动是否可用、字段类型转换和事务失败回滚。

## 2. 依赖与对象关系

- 头文件：`#include <QSqlDriver>`
- 继承自：QObject
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Sql)
target_link_libraries(mytarget PRIVATE Qt6::Sql)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

Qt SQL 把驱动、连接、查询游标和模型分成不同对象。连接决定驱动和数据库会话，`QSqlQuery` 代表语句及其结果游标，事务把多条语句的提交边界固定下来，SQL 模型再把查询结果接到视图。

### 状态、生命周期和线程

**生命周期：** 连接由连接名识别，查询和模型引用连接。关闭或移除连接前必须销毁仍引用它的 query、model 和 database 句柄；不同线程不要共用连接。

**状态与结果：** 区分连接是否打开、语句是否执行成功、游标是否定位在有效行、字段是否存在以及事务是否提交成功。`exec()` 成功不代表有结果行，`next()` 成功后才可以安全读取当前行。

**线程与事件循环：** Qt SQL 连接有线程归属，每个线程应建立自己的连接并使用唯一连接名；不要把一个线程创建的 QSqlDatabase 或 QSqlQuery 传到另一个线程继续使用。

## 3. 直接使用

创建连接并检查 open，使用 prepare/bindValue 分离 SQL 结构和用户数据，执行后检查返回值和 lastError，遍历结果，必要时用 transaction/commit/rollback 包住一组操作。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

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

- `enum DriverFeature { Transactions, QuerySize, BLOB, Unicode, PreparedQueries, …, CancelQuery }`
- `enum IdentifierType { FieldName, TableName }`
- `enum NotificationSource { UnknownSource, SelfSource, OtherSource }`
- `enum StatementType { WhereStatement, SelectStatement, UpdateStatement, InsertStatement, DeleteStatement }`

### 属性

- `(since 6.8) numericalPrecisionPolicy : QSql::NumericalPrecisionPolicy`

### 公有函数

- `QSqlDriver(QObject *parent = nullptr)`
- `virtual ~QSqlDriver()`
- `virtual bool beginTransaction()`
- `virtual void close() = 0`
- `virtual bool commitTransaction()`
- `(since 6.9) QString connectionName() const`
- `virtual QSqlResult * createResult() const = 0`
- `virtual QString escapeIdentifier(const QString &identifier, QSqlDriver::IdentifierType type) const`
- `virtual QString formatValue(const QSqlField &field, bool trimStrings = false) const`
- `virtual QVariant handle() const`
- `virtual bool hasFeature(QSqlDriver::DriverFeature feature) const = 0`
- `virtual bool isIdentifierEscaped(const QString &identifier, QSqlDriver::IdentifierType type) const`
- `virtual bool isOpen() const`
- `bool isOpenError() const`
- `QSqlError lastError() const`
- `(since 6.0) virtual int maximumIdentifierLength(QSqlDriver::IdentifierType type) const`
- `QSql::NumericalPrecisionPolicy numericalPrecisionPolicy() const`
- `virtual bool open(const QString &db, const QString &user = QString(), const QString &password = QString(), const QString &host = QString(), int port = -1, const QString &options = QString()) = 0`
- `virtual QSqlIndex primaryIndex(const QString &tableName) const`
- `virtual QSqlRecord record(const QString &tableName) const`
- `virtual bool rollbackTransaction()`
- `void setNumericalPrecisionPolicy(QSql::NumericalPrecisionPolicy precisionPolicy)`
- `virtual QString sqlStatement(QSqlDriver::StatementType type, const QString &tableName, const QSqlRecord &rec, bool preparedStatement) const`
- `virtual QString stripDelimiters(const QString &identifier, QSqlDriver::IdentifierType type) const`
- `virtual bool subscribeToNotification(const QString &name)`
- `virtual QStringList subscribedToNotifications() const`
- `virtual QStringList tables(QSql::TableType tableType) const`
- `virtual bool unsubscribeFromNotification(const QString &name)`

### 信号

- `void notification(const QString &name, QSqlDriver::NotificationSource source, const QVariant &payload)`

### 保护函数

- `virtual void setLastError(const QSqlError &error)`
- `virtual void setOpen(bool open)`
- `virtual void setOpenError(bool error)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QSqlDriver::DriverFeature`

**作用与语义：**

该枚举包含驱动程序可能支持的功能列表。使用`hasFeature()`查询某个功能是否被支持。部分功能依赖于数据库服务器，因此只有在成功通过`QSqlDatabase::open()`打开数据库连接后才能正确判断。
- `QSqlDriver::Transactions`：`0`;驱动程序是否支持SQL事务。
- `QSqlDriver::QuerySize`：`1`;数据库是否能够报告查询的大小。注意，有些数据库不支持返回查询的大小（即返回的行数），此时`QSqlQuery::size()`返回为-1。
- `QSqlDriver::BLOB`：`2`;驱动程序是否支持二进制大对象字段。
- `QSqlDriver::Unicode`：`3`;如果数据库服务器支持，驱动程序是否支持Unicode字符串。
- `QSqlDriver::PreparedQueries`：`4`;驱动程序是否支持预备查询执行。
- `QSqlDriver::NamedPlaceholders`：`5`;驱动程序是否支持使用命名占位符。
- `QSqlDriver::PositionalPlaceholders`：`6`;驱动程序是否支持使用位置占位符。
- `QSqlDriver::LastInsertId`：`7`;驱动程序是否支持返回最后被触碰行的ID。
- `QSqlDriver::BatchOperations`：`8`;驱动程序是否支持批处理操作，参见`QSqlQuery::execBatch()`
- `QSqlDriver::SimpleLocking`：`9`;驱动程序是否允许在表上设置写锁，而其他查询则有读取锁。
- `QSqlDriver::LowPrecisionNumbers`：`10`;驱动程序是否允许低精度获取数值。
- `QSqlDriver::EventNotifications`：`11`;驱动程序是否支持数据库事件通知。
- `QSqlDriver::FinishQuery`：`12`;驱动程序在调用`QSqlQuery::finish()`时是否能进行任何低层级资源清理。
- `QSqlDriver::MultipleResultSets`：`13`;驱动程序是否能访问从批处理语句或存储过程返回的多个结果集。
- `QSqlDriver::CancelQuery`：`14`;驱动程序是否允许取消正在进行的查询。
关于支持功能的更多信息可在 Qt SQL 驱动文档中找到。

### `enum QSqlDriver::IdentifierType`

**作用与语义：**

该枚举包含SQL标识符类型的列表。
- `QSqlDriver::FieldName`：`0`;一个SQL字段名称
- `QSqlDriver::TableName`：`1`;一个SQL表名称

### `enum QSqlDriver::NotificationSource`

**作用与语义：**

该枚举包含SQL通知源列表。
- `QSqlDriver::UnknownSource`：`0`;通知源未知
- `QSqlDriver::SelfSource`：`1`;通知源是该连接
- `QSqlDriver::OtherSource`：`2`;通知源是另一个连接

### `enum QSqlDriver::StatementType`

**作用与语义：**

该枚举包含驱动程序可以创建的SQL语句（或子句）类型列表。
- `QSqlDriver::WhereStatement`：`0`;一个SQL `WHERE`语句（例如，`WHERE f = 5`）。
- `QSqlDriver::SelectStatement`：`1`;一个SQL `SELECT`语句（例如，`SELECT f FROM t`）。
- `QSqlDriver::UpdateStatement`：`2`;一个SQL `UPDATE`语句（例如，`UPDATE TABLE t set f = 1`）。
- `QSqlDriver::InsertStatement`：`3`;一个SQL `INSERT`语句（例如，`INSERT INTO t (f) values (1)`）。
- `QSqlDriver::DeleteStatement`：`4`;一个SQL `DELETE`语句（例如，`DELETE FROM t`）。

### `[since 6.8] numericalPrecisionPolicy : QSql::NumericalPrecisionPolicy`

**作用与语义：**

该属性包含数据库连接的精度策略。
注意：设置精度策略不会影响当前正在运行的任何查询。

**如何使用：** 调用 `numericalPrecisionPolicy()` 读取当前值；它不会修改应用状态。

### `[explicit] QSqlDriver::QSqlDriver(QObject *parent = nullptr)`

**作用与语义：**

用给定的`parent`构造一个新的驱动程序。

### `[virtual noexcept] QSqlDriver::~QSqlDriver()`

**作用与语义：**

摧毁该物体并释放所有分配的资源。

### `[virtual] bool QSqlDriver::beginTransaction()`

**作用与语义：**

调用该函数以启动事务。成功时返回true，否则返回false。默认实现不做任何操作，返回`false`。

### `[pure virtual] void QSqlDriver::close()`

**作用与语义：**

派生类必须重新实现这个纯虚拟函数以关闭数据库连接。成功时返回 true，失败时返回 false。

### `[virtual] bool QSqlDriver::commitTransaction()`

**作用与语义：**

该函数被调用以提交事务。如果成功，返回true，否则返回false。默认实现不做任何操作，返回`false`。

### `[since 6.9] QString QSqlDriver::connectionName() const`

**作用与语义：**

返回驱动创建时的数据库连接名称，并附`QSqlDatabase::addDatabase()`。

### `[pure virtual] QSqlResult *QSqlDriver::createResult() const`

**作用与语义：**

在数据库上创建一个空的 SQL 结果。派生类必须重新实现该函数，并返回一个适合其数据库的 `QSqlResult` 对象给调用者。

### `[virtual] QString QSqlDriver::escapeIdentifier(const QString &identifier, QSqlDriver::IdentifierType type) const`

**作用与语义：**

根据数据库规则返回转义的`identifier`。`identifier`可以是表名或字段名，具体取决于`type`。
默认实现什么都不做。

### `[virtual] QString QSqlDriver::formatValue(const QSqlField &field, bool trimStrings = false) const`

**作用与语义：**

返回数据库`field`值的字符串表示。例如，在构建INSERT和UPDATE语句时，会使用该字符串。
默认实现会根据以下规则返回以字符串格式化的值：
- 如果`field`为字符数据，值以单引号包裹返回，这适用于许多SQL数据库。任何嵌入的单引号字符都被转义（用两个单引号字符替代）。如果`trimStrings`为真（默认为假），则所有后置空白从字段中裁掉。
- 如果`field`是日期/时间数据，则该值以ISO格式并用单引号包围。如果日期/时间数据无效，则返回“NULL”。
- 如果`field`是`bytearray`数据，且驱动程序可以编辑二进制字段，则该值被格式化为十六进制字符串。
- 对于任何其他字段类型，调用 toString() 对其值进行调用，返回结果。

### `[virtual] QVariant QSqlDriver::handle() const`

**作用与语义：**

返回包裹在`QVariant`或无句柄时的无效变体包裹的低系列据库句柄。
警告：使用时请极度谨慎，且仅在你知道自己在做什么的情况下使用。
警告：这里返回的handle如果连接被修改（例如关闭连接），可能会变成过时指针。
警告：如果连接尚未打开，句柄可能为空。
这里返回的句柄是数据库相关的，访问前应查询变体的类型名。
本示例检索了与 sqlite 连接的句柄：
此摘要返回PostgreSQL或MySQL的句柄：

**官方示例：**

```cpp
 QSqlDatabase db = QSqlDatabase::database();
 QVariant v = db.driver()->handle();
 if (v.isValid() && (qstrcmp(v.typeName(), "sqlite3*") == 0)) {
     // v.data() returns a pointer to the handle
     sqlite3 *handle = *static_cast<sqlite3 **>(v.data());
     if (handle) {
         // ...
     }
 }
```

### `[pure virtual] bool QSqlDriver::hasFeature(QSqlDriver::DriverFeature feature) const`

**作用与语义：**

如果驱动支持功能`feature`，返回`true`;否则返回`false`。
请注意，有些数据库需要先`open()`才能确定这一点。

### `[virtual] bool QSqlDriver::isIdentifierEscaped(const QString &identifier, QSqlDriver::IdentifierType type) const`

**作用与语义：**

返回`identifier`是否符合数据库规则的转义。`identifier`可以是表名或字段名，取决于`type`。
如果你想在`QSqlDriver`子类中实现自己的实现，可以重新实现这个函数，。

### `[virtual] bool QSqlDriver::isOpen() const`

**作用与语义：**

如果数据库连接是开放的，返回`true`;否则返回 false。

### `bool QSqlDriver::isOpenError() const`

**作用与语义：**

如果打开数据库连接时出现错误，返回`true`;否则返回`false`。

### `QSqlError QSqlDriver::lastError() const`

**作用与语义：**

返回一个`QSqlError`对象，包含数据库上最后一次错误的信息。

### `[virtual, since 6.0] int QSqlDriver::maximumIdentifierLength(QSqlDriver::IdentifierType type) const`

**作用与语义：**

根据数据库设置返回标识符的最大长度`type`。如果数据库中没有最大值，则默认返回INT_MAX。

### `[signal] void QSqlDriver::notification(const QString &name, QSqlDriver::NotificationSource source, const QVariant &payload)`

**作用与语义：**

当数据库发布事件通知，司机订阅该通知时，该信号会发出。`name`标识事件通知，`source`指示信号源，`payload`存储可随通知一同提供的额外数据。

### `QSql::NumericalPrecisionPolicy QSqlDriver::numericalPrecisionPolicy() const`

**作用与语义：**

返回 numicalPrecisionPolicy。
注意：属性 numericalPrecisionPolicy 的获取函数。

### `[pure virtual] bool QSqlDriver::open(const QString &db, const QString &user = QString(), const QString &password = QString(), const QString &host = QString(), int port = -1, const QString &options = QString())`

**作用与语义：**

派生类必须重新实现这个纯虚拟函数，在数据库`db`上开启数据库连接，使用用户名`user`、密码`password`、主机`host`、端口`port`和连接选项`options`。
函数成功时必须返回真，失败时返回假。

### `[virtual] QSqlIndex QSqlDriver::primaryIndex(const QString &tableName) const`

**作用与语义：**

返回表`tableName`的主索引。如果表没有主索引，返回空的`QSqlIndex`。默认实现返回的是空索引。

### `[virtual] QSqlRecord QSqlDriver::record(const QString &tableName) const`

**作用与语义：**

返回一个`QSqlRecord`，包含表`tableName`字段的名称。如果不存在此类表，则返回空记录。默认实现返回空记录。

### `[virtual] bool QSqlDriver::rollbackTransaction()`

**作用与语义：**

调用该函数用于回滚事务。如果成功，返回 true，否则返回 false。默认实现不做任何操作，返回 `false`。

### `[virtual protected] void QSqlDriver::setLastError(const QSqlError &error)`

**作用与语义：**

该函数用于设定数据库中最后一次错误（`error`）的值。

### `void QSqlDriver::setNumericalPrecisionPolicy(QSql::NumericalPrecisionPolicy precisionPolicy)`

**作用与语义：**

该属性包含数据库连接的精度策略。
注意：设置精度策略不会影响当前正在运行的任何查询。

**如何使用：** 调用 `setNumericalPrecisionPolicy(...)` 修改 `numericalPrecisionPolicy`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `[virtual protected] void QSqlDriver::setOpen(bool open)`

**作用与语义：**

该函数将数据库的开放状态设置为`open`。派生类可以使用该函数报告`open()`的状态。

### `[virtual protected] void QSqlDriver::setOpenError(bool error)`

**作用与语义：**

该函数将数据库的开放错误状态设置为`error`。派生类可以使用该函数报告`open()`的状态。注意，如果 `error`为真，数据库的开放状态将设置为关闭（即返回`isOpen()`返回`false`）。

### `[virtual] QString QSqlDriver::sqlStatement(QSqlDriver::StatementType type, const QString &tableName, const QSqlRecord &rec, bool preparedStatement) const`

**作用与语义：**

返回表 `type` 类型 `tableName` 的 SQL 语句，`rec` 的值。如果 `preparedStatement`为真，该字符串将包含占位符而非值。
每个`rec`字段生成的标志决定该字段是否包含在生成语句中。
该方法可用于操作表，无需担心依赖数据库的SQL方言。对于未准备的语句，值将被正确转义。
在 WHERE 语句中，`rec` 的每个非空字段指定了一个与字段值相等的过滤条件，或者如果准备好了，则指定占位符。然而，无论是否准备好，空字段都指定条件为 IS NULL，且从不引入占位符。应用程序在执行过程中不得尝试绑定空字段的数据。如果需要占位符，字段必须设置为某个非空值。此外，由于非空字段指定了等价条件，而 SQL NULL 不等于任何东西，甚至不等于它自身，通常将空字段绑定到占位符上并不实用。

### `[virtual] QString QSqlDriver::stripDelimiters(const QString &identifier, QSqlDriver::IdentifierType type) const`

**作用与语义：**

返回去除前置和后尾分隔符的`identifier`，`identifier`可以是表名或字段名，取决于`type`。如果`identifier`没有前置和后置分隔符字符，则返回`identifier`，无需修改。
如果你想在`QSqlDriver`子类中提供自己的实现，可以重新实现这个函数，。

### `[virtual] bool QSqlDriver::subscribeToNotification(const QString &name)`

**作用与语义：**

该函数用于订阅数据库中的事件通知。`name` 用于识别事件通知。
如果成功，返回真，否则返回假。
调用该函数时，数据库必须处于打开状态。当通过调用关闭数据库时`close()`所有已订阅的事件通知都会自动取消订阅。注意，在已打开的数据库上调用`open()`可能会隐式地导致调用`close()`，从而导致驱动程序取消所有事件通知。
当数据库发布由`name`识别的事件通知时，`notification()`信号会被发出。
如果你想在自己的`QSqlDriver`子类中提供事件通知支持，请重新实现这个函数，。

### `[virtual] QStringList QSqlDriver::subscribedToNotifications() const`

**作用与语义：**

返回当前订阅的事件通知名称列表。
如果你想在自己的 `QSqlDriver` 子类中提供事件通知支持，请重新实现这个函数，。

### `[virtual] QStringList QSqlDriver::tables(QSql::TableType tableType) const`

**作用与语义：**

返回数据库中表名称的列表。默认实现返回一个空列表。
`tableType`参数描述应返回哪些类型的表。由于二进制兼容性，字符串包含枚举QSql：：TableTypes的值作为文本。空字符串应视为`QSql::Tables`以实现向后兼容。

### `[virtual] bool QSqlDriver::unsubscribeFromNotification(const QString &name)`

**作用与语义：**

该函数用于取消数据库中的事件通知。`name` 用于识别事件通知。
如果成功，返回真，否则返回假。
调用该函数时，数据库必须处于打开状态。所有订阅的事件通知在调用`close()`函数时自动取消订阅。
调用该函数后，当数据库发布由`name`识别的事件通知时，`notification()`信号将不再发出。
如果你想在自己的`QSqlDriver`子类中提供事件通知支持，请重新实现这个函数，。

## 6. 深入实践与常见坑

### 生命周期和资源边界

连接由连接名识别，查询和模型引用连接。关闭或移除连接前必须销毁仍引用它的 query、model 和 database 句柄；不同线程不要共用连接。

### 状态和错误边界

区分连接是否打开、语句是否执行成功、游标是否定位在有效行、字段是否存在以及事务是否提交成功。`exec()` 成功不代表有结果行，`next()` 成功后才可以安全读取当前行。

### 线程边界

Qt SQL 连接有线程归属，每个线程应建立自己的连接并使用唯一连接名；不要把一个线程创建的 QSqlDatabase 或 QSqlQuery 传到另一个线程继续使用。

### 最容易出现的错误

不要拼接用户输入形成 SQL；不要把 exec 成功当作有数据；不要在连接仍被引用时 removeDatabase；不要忽略驱动是否可用、字段类型转换和事务失败回滚。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QSqlDriver` 所属机制类型：Qt SQL 连接、查询与事务机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
