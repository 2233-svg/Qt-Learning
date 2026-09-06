# QSqlDatabase

> Qt 6.11.1 · Qt SQL

## 1. 先建立直觉

**一句话定位：** `QSqlDatabase` 表示一个 Qt SQL 数据库连接配置和连接句柄，负责选择驱动、设置参数、打开和关闭连接。

**模块背景：** Qt SQL 提供数据库连接、查询、事务和 SQL 模型/视图集成。

### 这是什么

`QSqlDatabase` 表示一个 Qt SQL 数据库连接配置和连接句柄，负责选择驱动、设置参数、打开和关闭连接。

**内部模型：** Qt SQL 连接以 connectionName 标识并由 Qt 管理；QSqlDatabase 是隐式共享的值类，但连接真正的生命周期和线程归属必须明确。

**适用场景：** 应用需要连接 SQLite、MySQL、PostgreSQL 或其他 Qt SQL 驱动时使用。查询操作通过 QSqlQuery，模型展示通过 QSqlTableModel/QSqlQueryModel。

**典型调用链：** addDatabase(driver, name) -> setDatabaseName/credentials -> open -> transaction -> query/model -> commit/rollback -> close/removeDatabase。

**先记住的坑：** 每个线程应使用自己的连接；removeDatabase 前要销毁所有引用该连接的 QSqlDatabase/QSqlQuery；检查 open 和 lastError；用户输入必须使用绑定参数。

## 2. 依赖与对象关系

- 头文件：`#include <QSqlDatabase>`
- 继承自：QSqlDatabaseDefaultConnectionName
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Sql)
target_link_libraries(mytarget PRIVATE Qt6::Sql)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

Qt SQL 连接以 connectionName 标识并由 Qt 管理；QSqlDatabase 是隐式共享的值类，但连接真正的生命周期和线程归属必须明确。

### 状态、生命周期和线程

**生命周期：** 连接由连接名识别，查询和模型引用连接。关闭或移除连接前必须销毁仍引用它的 query、model 和 database 句柄；不同线程不要共用连接。

**状态与结果：** 区分连接是否打开、语句是否执行成功、游标是否定位在有效行、字段是否存在以及事务是否提交成功。`exec()` 成功不代表有结果行，`next()` 成功后才可以安全读取当前行。

**线程与事件循环：** Qt SQL 连接有线程归属，每个线程应建立自己的连接并使用唯一连接名；不要把一个线程创建的 QSqlDatabase 或 QSqlQuery 传到另一个线程继续使用。

## 3. 直接使用

应用需要连接 SQLite、MySQL、PostgreSQL 或其他 Qt SQL 驱动时使用。查询操作通过 QSqlQuery，模型展示通过 QSqlTableModel/QSqlQueryModel。 使用时通常按这个过程组织：addDatabase(driver, name) -> setDatabaseName/credentials -> open -> transaction -> query/model -> commit/rollback -> close/removeDatabase。

```cpp
#include <QSqlDatabase>

QSqlDatabase database = QSqlDatabase::addDatabase("QSQLITE");
database.setDatabaseName("app.db");
if (!database.open())
    qWarning() << database.lastError();
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 属性

- `(since 6.8) numericalPrecisionPolicy : QSql::NumericalPrecisionPolicy`

### 公有函数

- `QSqlDatabase()`
- `QSqlDatabase(const QSqlDatabase &other)`
- `~QSqlDatabase()`
- `void close()`
- `bool commit()`
- `QString connectOptions() const`
- `QString connectionName() const`
- `QString databaseName() const`
- `QSqlDriver * driver() const`
- `QString driverName() const`
- `QString hostName() const`
- `bool isOpen() const`
- `bool isOpenError() const`
- `bool isValid() const`
- `QSqlError lastError() const`
- `(since 6.8) bool moveToThread(QThread *targetThread)`
- `QSql::NumericalPrecisionPolicy numericalPrecisionPolicy() const`
- `bool open()`
- `bool open(const QString &user, const QString &password)`
- `QString password() const`
- `int port() const`
- `QSqlIndex primaryIndex(const QString &tablename) const`
- `QSqlRecord record(const QString &tablename) const`
- `bool rollback()`
- `void setConnectOptions(const QString &options = QString())`
- `void setDatabaseName(const QString &name)`
- `void setHostName(const QString &host)`
- `void setNumericalPrecisionPolicy(QSql::NumericalPrecisionPolicy precisionPolicy)`
- `void setPassword(const QString &password)`
- `void setPort(int port)`
- `void setUserName(const QString &name)`
- `QStringList tables(QSql::TableType type = QSql::Tables) const`
- `(since 6.8) QThread * thread() const`
- `bool transaction()`
- `QString userName() const`
- `QSqlDatabase & operator=(const QSqlDatabase &other)`

### 静态公有成员

- `QSqlDatabase addDatabase(const QString &type, const QString &connectionName = defaultConnectionName())`
- `QSqlDatabase addDatabase(QSqlDriver *driver, const QString &connectionName = defaultConnectionName())`
- `QSqlDatabase cloneDatabase(const QSqlDatabase &other, const QString &connectionName)`
- `QSqlDatabase cloneDatabase(const QString &other, const QString &connectionName)`
- `QStringList connectionNames()`
- `bool contains(const QString &connectionName = defaultConnectionName())`
- `QSqlDatabase database(const QString &connectionName = defaultConnectionName(), bool open = true)`
- `QStringList drivers()`
- `bool isDriverAvailable(const QString &name)`
- `void registerSqlDriver(const QString &name, QSqlDriverCreatorBase *creator)`
- `void removeDatabase(const QString &connectionName)`

### 保护函数

- `QSqlDatabase(QSqlDriver *driver)`
- `QSqlDatabase(const QString &type)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[since 6.8] numericalPrecisionPolicy : QSql::NumericalPrecisionPolicy`

**作用与语义：**

该属性包含了在该数据库连接上创建的查询所使用的默认数值精度策略。
注意：不支持低精度取数值的驱动程序将忽略精度策略。你可以用`QSqlDriver::hasFeature()`来了解驱动程序是否支持此功能。
注意：将默认精度策略设置为`precisionPolicy`不会影响当前正在进行的任何查询。

**如何使用：** 调用 `numericalPrecisionPolicy()` 读取当前值；它不会修改应用状态。

### `QSqlDatabase::QSqlDatabase()`

**作用与语义：**

创建一个空的、无效的 QSqlDatabase 对象。使用 `addDatabase()`、`removeDatabase()` 和 `database()` 获取有效的 QSqlDatabase 对象。

### `[explicit protected] QSqlDatabase::QSqlDatabase(QSqlDriver *driver)`

**作用与语义：**

利用给定的`driver`创建数据库连接。

### `[explicit protected] QSqlDatabase::QSqlDatabase(const QString &type)`

**作用与语义：**

创建一个使用 `type` 所引用驱动的 QSqlDatabase 连接。如果未识别`type`，数据库连接将无功能。
目前可用的驱动类型有：
- `Driver Type`：描述
- `QDB2`：IBM DB2
- `QIBASE`：博兰洲际司机
- `QMYSQL`：MySQL 驱动
- `QOCI`：Oracle 调用接口驱动
- `QODBC`：ODBC 驱动（包含 Microsoft SQL Server）
- `QPSQL`：PostgreSQL 驱动
- `QSQLITE`：SQLite 版本 3 及以上
- `QMIMER`：Mimer SQL 11及以上
额外的第三方驱动，包括你自己的自定义驱动，都可以动态加载。

### `QSqlDatabase::QSqlDatabase(const QSqlDatabase &other)`

**作用与语义：**

创建`other`副本。

### `[noexcept] QSqlDatabase::~QSqlDatabase()`

**作用与语义：**

摧毁该物体并释放所有分配的资源。
注意：当最后一个连接被摧毁时，解构器隐式调用`close()`以释放数据库连接。

### `[static] QSqlDatabase QSqlDatabase::addDatabase(const QString &type, const QString &connectionName = defaultConnectionName())`

**作用与语义：**

使用驱动程序`type`和连接名称 `connectionName` 向数据库连接列表添加数据库。如果已经存在名为 `connectionName` 的数据库连接，该连接将被移除。
数据库连接由`connectionName`引用。新添加的数据库连接被返回。
如果`type`无法使用或无法加载，`isValid()`返回`false`。
如果未指定`connectionName`，新连接将成为应用程序的默认连接，后续调用`database()`但未包含连接名参数时，将返回默认连接。如果这里提供了`connectionName`，请使用 database（`connectionName`） 检索该连接。
警告：如果你添加了与现有连接名称相同的连接，新连接将替换旧连接。如果你多次调用该函数且未指定`connectionName`，默认连接将被替换。
在使用该连接之前，必须先初始化。例如，调用部分或全部`setDatabaseName()`、`setUserName()`、`setPassword()`、`setHostName()`、`setPort()`和`setConnectOptions()`，最后调用`open()`。
注意：该功能是线程安全的。

### `[static] QSqlDatabase QSqlDatabase::addDatabase(QSqlDriver *driver, const QString &connectionName = defaultConnectionName())`

**作用与语义：**

当你想用自己实例化的 `driver` 创建数据库连接时，这种重载非常有用。可能是你自己的数据库驱动，或者你只需要自己实例化一个 Qt 驱动。如果你这样做，建议你在应用程序中包含驱动代码。例如，你可以用自己的 QPSQL 驱动创建一个 PostgreSQL 连接，如下：
上述代码建立 PostgreSQL 连接并实例化 QPSQLDriver 对象。接着调用 addDatabase() 将连接添加到已知连接中，以便 Qt SQL 类使用。当驱动程序实例化连接句柄（或句柄集合）时，Qt 假设你已经打开了数据库连接。
注意：我们假设`qtdir`是 Qt 安装的目录。这会拉取使用 PostgreSQL 客户端库和实例化 QPSQLDriver 对象所需的代码，前提是你的 include 搜索路径中有 PostgreSQL 的头部。
记住，你必须将应用与数据库客户端库关联。确保客户端库在链接器的搜索路径中，并在`.pro`文件中添加类似这样的行：
所述方法适用于所有提供的驱动程序。唯一的区别在于驱动程序构造函数参数。以下是随Qt附带的驱动程序、其源代码文件及构造函数参数的表格：
- `Driver`：类名;构造函数参数;包含的文件
- `QPSQL`：QPSQLDriver;PGconn *连接;`qsql_psql.cpp`
- `QMYSQL`：QMYSQLDriver;MYSQL *连接;`qsql_mysql.cpp`
- `QOCI`：QOCIDriver;OCIEnv *环境，OCISvcCtx *服务上下文;`qsql_oci.cpp`
- `QODBC`：QODBCDriver;SQLHANDLE 环境，SQLHANDLE 连接;`qsql_odbc.cpp`
- `QDB2`：QDB2;SQLHANDLE 环境，SQLHANDLE 连接;`qsql_db2.cpp`
- `QSQLITE`：QSQLite驱动;sqlite *连接;`qsql_sqlite.cpp`
- `QMIMER`：QMimerSQLDriver;MimerSession *连接;`qsql_mimer.cpp`
- `QIBASE`：QIBaseDriver;isc_db_handle连接;`qsql_ibase.cpp`
警告：添加与现有连接名称相同的数据库连接，会导致现有连接被新的连接替换。
警告：SQL 框架会对`driver`拥有权。它不得被删除。要移除连接，请使用 `removeDatabase()`。

**官方示例：**

```cpp
 PGconn *con = PQconnectdb("host=server user=bart password=simpson dbname=springfield");
 QPSQLDriver *drv = new QPSQLDriver(con);
 QSqlDatabase db = QSqlDatabase::addDatabase(drv); // becomes the new default connection
 QSqlQuery query;
 query.exec("SELECT NAME, ID FROM STAFF");
```

### `[static] QSqlDatabase QSqlDatabase::cloneDatabase(const QSqlDatabase &other, const QString &connectionName)`

**作用与语义：**

克隆数据库连接`other`并存储为`connectionName`。原始数据库的所有设置，如`databaseName()`、`hostName()`等，都会被复制过来。如果`other`是无效数据库，则无效。返回新创建的数据库连接。
注意：新连接尚未开启。使用新连接前，您必须先联系`open()`。
注意：该函数是重入函数。

### `[static] QSqlDatabase QSqlDatabase::cloneDatabase(const QString &other, const QString &connectionName)`

**作用与语义：**

克隆数据库连接 `other`并存储为 `connectionName`。原始数据库中的所有设置，例如 `databaseName()`、`hostName()` 等，都会被复制到此中。如果`other`是无效数据库，则无效。返回新创建的数据库连接。
注意：新连接尚未开通。使用新连接前，您必须先调用`open()`。
这种重载在将另一个线程中的数据库克隆到由`other`表示的数据库使用的线程时非常有用。

### `void QSqlDatabase::close()`

**作用与语义：**

关闭数据库连接，释放所有已获得的资源，并使所有与数据库共用的现有`QSqlQuery`对象失效。
这也会影响该`QSqlDatabase`对象的副本。

### `bool QSqlDatabase::commit()`

**作用与语义：**

如果驱动程序支持事务且已启动`transaction()`，则向数据库提交事务。如果操作成功，返回`true`。否则返回`false`。
注意：对于某些数据库，如果数据库有活跃查询`SELECT`，提交会失败并返回`false`。在提交前先`inactive`查询。
请致电`lastError()`获取有关错误的信息。

### `QString QSqlDatabase::connectOptions() const`

**作用与语义：**

返回用于该连接的连接选项字符串。字符串可能是空的。

### `QString QSqlDatabase::connectionName() const`

**作用与语义：**

返回连接名，可能为空。
注意：连接名称不是数据库名称。

### `[static] QStringList QSqlDatabase::connectionNames()`

**作用与语义：**

返回包含所有连接名称的列表。
注意：该功能是线程安全的。

### `[static] bool QSqlDatabase::contains(const QString &connectionName = defaultConnectionName())`

**作用与语义：**

如果数据库连接列表包含`connectionName`，返回`true`;否则返回`false`。
注意：该功能是线程安全的。

### `[static] QSqlDatabase QSqlDatabase::database(const QString &connectionName = defaultConnectionName(), bool open = true)`

**作用与语义：**

返回名为`connectionName`的数据库连接。数据库连接必须是之前随`addDatabase()`添加的。如果`open`为真（默认），且数据库连接尚未打开，现在就打开连接。如果未指定`connectionName`，则使用默认连接。如果数据库列表中不存在`connectionName`，则返回无效连接。
注意：该功能是线程安全的。

### `QString QSqlDatabase::databaseName() const`

**作用与语义：**

返回连接的数据库名称，可能为空。
注意：数据库名称不是连接名称。

### `QSqlDriver *QSqlDatabase::driver() const`

**作用与语义：**

返回用于访问数据库连接的数据库驱动程序。

### `QString QSqlDatabase::driverName() const`

**作用与语义：**

返回连接的驱动程序名称。

### `[static] QStringList QSqlDatabase::drivers()`

**作用与语义：**

返回所有可用数据库驱动程序的列表。

### `QString QSqlDatabase::hostName() const`

**作用与语义：**

返回连接的主机名;可能是空的。

### `[static] bool QSqlDatabase::isDriverAvailable(const QString &name)`

**作用与语义：**

如果有名为`name`的司机可用，则返回`true`;否则返回`false`。

### `bool QSqlDatabase::isOpen() const`

**作用与语义：**

如果数据库连接当前开放，返回`true`;否则返回`false`。

### `bool QSqlDatabase::isOpenError() const`

**作用与语义：**

如果数据库连接中出现错误，返回`true`;否则返回`false`。错误信息可以通过`lastError()`函数检索。

### `bool QSqlDatabase::isValid() const`

**作用与语义：**

如果 `QSqlDatabase` 有有效的驱动程序，则返回 `true`。

**官方示例：**

```cpp
 QSqlDatabase db;
 qDebug() << db.isValid();    // Returns false

 db = QSqlDatabase::database("sales");
 qDebug() << db.isValid();    // Returns \c true if "sales" connection exists

 QSqlDatabase::removeDatabase("sales");
 qDebug() << db.isValid();    // Returns false
```

### `QSqlError QSqlDatabase::lastError() const`

**作用与语义：**

返回数据库上最后一次发生错误的信息。
与单个查询相关的失败由`QSqlQuery::lastError()`报告。

### `[since 6.8] bool QSqlDatabase::moveToThread(QThread *targetThread)`

**作用与语义：**

改变`QSqlDatabase`及其相关驱动的线程亲和力。该函数成功时返回`true`。事件处理将在`targetThread`中继续。
在此操作过程中，你必须确保该实例没有绑定`QSqlQuery`，否则`QSqlDatabase`不会被移动到给定线程，函数返回`false`。
由于关联驱动源自`QObject`，所有将 `QObject` 移动到另一个线程的约束也适用于该函数。

### `QSql::NumericalPrecisionPolicy QSqlDatabase::numericalPrecisionPolicy() const`

**作用与语义：**

返回 numicalPrecisionPolicy。
注意：属性 numericalPrecisionPolicy 的获取函数。

### `bool QSqlDatabase::open()`

**作用与语义：**

使用当前连接值打开数据库连接。成功时返回`true`;否则返回`false`。错误信息可以通过`lastError()`检索。

### `bool QSqlDatabase::open(const QString &user, const QString &password)`

**作用与语义：**

使用给定的`user`名和`password`打开数据库连接。成功时返回`true`;否则返回`false`。错误信息可以通过`lastError()`函数检索。
该函数不存储所获得的密码。相反，密码会直接传递给驱动程序以打开连接，然后将其丢弃。

### `QString QSqlDatabase::password() const`

**作用与语义：**

返回连接的密码。如果密码未设置`setPassword()`，且密码是在 `open()` 调用中提供的，或未使用密码，则返回空字符串。

### `int QSqlDatabase::port() const`

**作用与语义：**

返回连接的端口号。如果端口号未设置，该值为未定义。

### `QSqlIndex QSqlDatabase::primaryIndex(const QString &tablename) const`

**作用与语义：**

返回表`tablename`的主索引。如果不存在主索引，则返回空`QSqlIndex`。
注意：如果创建时表格未被引用，某些驱动程序（如 QPSQL 驱动程序）可能需要你用小写字母传递`tablename`。更多信息请参见 Qt SQL 驱动文档。

### `QSqlRecord QSqlDatabase::record(const QString &tablename) const`

**作用与语义：**

返回一个包含表（或视图）中所有字段名称的`QSqlRecord`，称为 `tablename`。字段在记录中的出现顺序未定义。如果不存在这样的表（或视图），则返回一个空记录。
注意：某些驱动程序，如 QPSQL 驱动，如果创建时表未引用，可能需要你用小写传递`tablename`。更多信息请参见 Qt SQL 驱动文档。

### `[static] void QSqlDatabase::registerSqlDriver(const QString &name, QSqlDriverCreatorBase *creator)`

**作用与语义：**

这个函数在SQL框架内注册了一个新的SQL驱动，称为`name`。如果你有自定义SQL驱动，不想编译成插件，这非常有用。
`QSqlDatabase`会拥有`creator`指针的所有权，所以你不能自己删除它。

**官方示例：**

```cpp
 QSqlDatabase::registerSqlDriver("MYDRIVER", new QSqlDriverCreator<QSqlDriver>);
 QVERIFY(QSqlDatabase::drivers().contains("MYDRIVER"));
 QSqlDatabase db = QSqlDatabase::addDatabase("MYDRIVER");
 QVERIFY(db.isValid());
```

### `[static] void QSqlDatabase::removeDatabase(const QString &connectionName)`

**作用与语义：**

将数据库连接`connectionName`从数据库连接列表中移除。
警告：调用该函数时，数据库连接不应有未开查询，否则将发生资源泄漏。
正确的做法是：
要移除默认连接，该连接可能是通过调用`addDatabase()`未指定连接名称创建的，您可以通过调用`database()`返回的数据库中的 `connectionName()` 来获取默认连接名称。注意，如果没有创建默认数据库，将返回无效数据库。
注意：该功能是线程安全的。

**官方示例：**

```cpp
 // WRONG
 QSqlDatabase db = QSqlDatabase::database("sales");
 QSqlQuery query("SELECT NAME, DOB FROM EMPLOYEES", db);
 QSqlDatabase::removeDatabase("sales"); // will output a warning
 // "db" is now a dangling invalid database connection,
 // "query" contains an invalid result set
```

### `bool QSqlDatabase::rollback()`

**作用与语义：**

如果驱动程序支持事务且已启动`transaction()`，则回滚数据库中的事务。返回`true`操作是否成功。否则返回`false`。
注意：对于某些数据库，如果数据库中有活跃查询进行`SELECT`，回滚会失败并返回`false`。在回滚前先`inactive`查询。
请致电`lastError()`获取有关错误的信息。

### `void QSqlDatabase::setConnectOptions(const QString &options = QString())`

**作用与语义：**

设置数据库特定的`options`。必须在打开连接前完成，否则无效。另一种可能是关闭连接，调用QSqlDatabase：：setConnectOptions()，然后再次`open()`连接。
`options`字符串的格式是用分号分隔的选项名称列表或option=value对。选项取决于所使用的数据库客户端，并在SQL数据库驱动程序页面中描述了每个插件。
示例：
请参阅客户端库文档以获取关于不同选项的更多信息。

**官方示例：**

```cpp
 db.setConnectOptions("SSL_KEY=client-key.pem;SSL_CERT=client-cert.pem;SSL_CA=ca-cert.pem;CLIENT_IGNORE_SPACE=1"); // use an SSL connection to the server
 if (!db.open()) {
     db.setConnectOptions(); // clears the connect option string
     // ...
 }
 // ...
 // PostgreSQL connection
 db.setConnectOptions("requiressl=1"); // enable PostgreSQL SSL connections
 if (!db.open()) {
     db.setConnectOptions(); // clear options
     // ...
 }
 // ...
 // ODBC connection
 db.setConnectOptions("SQL_ATTR_ACCESS_MODE=SQL_MODE_READ_ONLY;SQL_ATTR_TRACE=SQL_OPT_TRACE_ON"); // set ODBC options
 if (!db.open()) {
     db.setConnectOptions(); // don't try to set this option
     // ...
 }
 }
```

### `void QSqlDatabase::setDatabaseName(const QString &name)`

**作用与语义：**

将连接的数据库名称设置为`name`。要生效，必须在连接`opened`之前设置数据库名称。或者，你可以`close()`连接，设置数据库名称，然后再次调用`open()`。
注意：数据库名称不是连接名称。连接名称必须在连接对象创建时传递给`addDatabase()`。
对于QSLITE驱动，如果数据库名称不存在，除非设置了QSQLITE_OPEN_READONLY选项，否则它会帮你创建文件。
此外，`name` 可以设置为 `":memory:"`，这会创建一个临时数据库，仅在应用的生命周期内可用。
对于QOCI（Oracle）驱动程序，数据库名称是TNS服务名称。
对于 QODBC 驱动程序，`name`可以是 DSN、DSN 文件名（此时文件必须有 `.dsn` 扩展名）或连接字符串。
例如，Microsoft Access 用户可以使用以下连接字符串直接打开 `.mdb` 文件，而无需在 ODBC 管理器中创建 DSN 条目：
没有默认值。

**官方示例：**

```cpp
 // ...
 QSqlDatabase db = QSqlDatabase::addDatabase("QODBC");
 db.setDatabaseName("DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};FIL={MS Access};DBQ=myaccessfile.mdb");
 if (db.open()) {
     // success!
 }
 // ...
```

### `void QSqlDatabase::setHostName(const QString &host)`

**作用与语义：**

将连接的主机名设置为`host`。要生效，必须在连接`opened`之前设置好主机名。或者，你可以`close()`连接，设置主机名，然后再次调用`open()`。
没有默认值。

### `void QSqlDatabase::setNumericalPrecisionPolicy(QSql::NumericalPrecisionPolicy precisionPolicy)`

**作用与语义：**

该属性包含了在该数据库连接上创建的查询所使用的默认数值精度策略。
注意：不支持低精度取数值的驱动程序将忽略精度策略。你可以用`QSqlDriver::hasFeature()`来了解驱动程序是否支持此功能。
注意：将默认精度策略设置为`precisionPolicy`不会影响当前正在进行的任何查询。

**如何使用：** 调用 `setNumericalPrecisionPolicy(...)` 修改 `numericalPrecisionPolicy`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QSqlDatabase::setPassword(const QString &password)`

**作用与语义：**

将连接密码设置为`password`。要生效，密码必须在连接`opened`之前设置好。或者，你可以`close()`连接，设置密码，然后再次调用`open()`。
没有默认值。
警告：该函数将密码以明文形式存储在 Qt 中。请使用以密码为参数的 `open()` 调用以避免此行为。

### `void QSqlDatabase::setPort(int port)`

**作用与语义：**

将连接的端口号设置为`port`。要生效，端口号必须在连接`opened`之前设置好。或者，你也可以`close()`连接，设置端口号，然后再次调用`open()`......
没有默认值。

### `void QSqlDatabase::setUserName(const QString &name)`

**作用与语义：**

将连接的用户名设置为`name`。要生效，必须在连接`opened`之前设置好用户名。或者，你可以`close()`连接，设置用户名，然后再次调用`open()`。
没有默认值。

### `QStringList QSqlDatabase::tables(QSql::TableType type = QSql::Tables) const`

**作用与语义：**

返回数据库的表、系统表和视图列表，按照参数`type`指定。

### `[since 6.8] QThread *QSqlDatabase::thread() const`

**作用与语义：**

返回指向关联的`QThread`实例的指针。

### `bool QSqlDatabase::transaction()`

**作用与语义：**

如果驱动程序支持事务，则在数据库上启动事务。如果操作成功，返回`true`。否则返回`false`。

### `QString QSqlDatabase::userName() const`

**作用与语义：**

返回连接的用户名;可能是空的。

### `QSqlDatabase &QSqlDatabase::operator=(const QSqlDatabase &other)`

**作用与语义：**

为该对象分配`other`。

## 6. 深入实践与常见坑

### 生命周期和资源边界

连接由连接名识别，查询和模型引用连接。关闭或移除连接前必须销毁仍引用它的 query、model 和 database 句柄；不同线程不要共用连接。

### 状态和错误边界

区分连接是否打开、语句是否执行成功、游标是否定位在有效行、字段是否存在以及事务是否提交成功。`exec()` 成功不代表有结果行，`next()` 成功后才可以安全读取当前行。

### 线程边界

Qt SQL 连接有线程归属，每个线程应建立自己的连接并使用唯一连接名；不要把一个线程创建的 QSqlDatabase 或 QSqlQuery 传到另一个线程继续使用。

### 最容易出现的错误

每个线程应使用自己的连接；removeDatabase 前要销毁所有引用该连接的 QSqlDatabase/QSqlQuery；检查 open 和 lastError；用户输入必须使用绑定参数。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QSqlDatabase` 所属机制类型：Qt SQL 连接、查询与事务机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
