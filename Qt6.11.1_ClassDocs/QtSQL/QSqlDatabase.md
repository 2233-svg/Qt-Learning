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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 50 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `[since 6.8] numericalPrecisionPolicy : QSql::NumericalPrecisionPolicy`

**API 类别：** 属性说明

**中文解读：** 这是 `QSqlDatabase` 的配置属性。初始化或状态切换时通过 `setNumericalPrecisionPolicy(...)` 设置，之后用 `NumericalPrecisionPolicy()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QSql::NumericalPrecisionPolicy`。
- 属性名：`numericalPrecisionPolicy`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSqlDatabase::QSqlDatabase()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSqlDatabase` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit protected] QSqlDatabase::QSqlDatabase(QSqlDriver *driver)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSqlDatabase` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `driver`：类型为 `QSqlDriver *`。没有默认值，调用时必须提供。传入 `QSqlDriver *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit protected] QSqlDatabase::QSqlDatabase(const QString &type)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSqlDatabase` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `type`：类型为 `const QString &`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSqlDatabase::QSqlDatabase(const QSqlDatabase &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSqlDatabase` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `const QSqlDatabase &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QSqlDatabase::~QSqlDatabase()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSqlDatabase` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QSqlDatabase QSqlDatabase::addDatabase(const QString &type, const QString &connectionName = defaultConnectionName())`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `addDatabase`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QSqlDatabase`。
- 参数 `type`：类型为 `const QString &`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。
- 参数 `connectionName`：类型为 `const QString &`。默认值为 `defaultConnectionName()`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QSqlDatabase QSqlDatabase::addDatabase(QSqlDriver *driver, const QString &connectionName = defaultConnectionName())`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `addDatabase`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QSqlDatabase`。
- 参数 `driver`：类型为 `QSqlDriver *`。没有默认值，调用时必须提供。传入 `QSqlDriver *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `connectionName`：类型为 `const QString &`。默认值为 `defaultConnectionName()`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QSqlDatabase QSqlDatabase::cloneDatabase(const QSqlDatabase &other, const QString &connectionName)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `cloneDatabase`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QSqlDatabase`。
- 参数 `other`：类型为 `const QSqlDatabase &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。
- 参数 `connectionName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QSqlDatabase QSqlDatabase::cloneDatabase(const QString &other, const QString &connectionName)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `cloneDatabase`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QSqlDatabase`。
- 参数 `other`：类型为 `const QString &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。
- 参数 `connectionName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSqlDatabase::close()`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `close`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QSqlDatabase::commit()`

**API 类别：** 成员函数说明

**中文解读：** `QSqlDatabase::commit` 用于计算、查询或取得与“提交”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QSqlDatabase::connectOptions() const`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `connectOptions`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QSqlDatabase::connectionName() const`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `connectionName`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QStringList QSqlDatabase::connectionNames()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `connectionNames`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QStringList`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] bool QSqlDatabase::contains(const QString &connectionName = defaultConnectionName())`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `contains`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数 `connectionName`：类型为 `const QString &`。默认值为 `defaultConnectionName()`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QSqlDatabase QSqlDatabase::database(const QString &connectionName = defaultConnectionName(), bool open = true)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `database`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QSqlDatabase`。
- 参数 `connectionName`：类型为 `const QString &`。默认值为 `defaultConnectionName()`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `open`：类型为 `bool`。默认值为 `true`。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QSqlDatabase::databaseName() const`

**API 类别：** 成员函数说明

**中文解读：** `QSqlDatabase::databaseName` 用于计算、查询或取得与“database、名称”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSqlDriver *QSqlDatabase::driver() const`

**API 类别：** 成员函数说明

**中文解读：** `QSqlDatabase::driver` 用于计算、查询或取得与“driver”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSqlDriver *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSqlDriver *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QSqlDatabase::driverName() const`

**API 类别：** 成员函数说明

**中文解读：** `QSqlDatabase::driverName` 用于计算、查询或取得与“driver、名称”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QStringList QSqlDatabase::drivers()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `drivers`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QStringList`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QSqlDatabase::hostName() const`

**API 类别：** 成员函数说明

**中文解读：** `QSqlDatabase::hostName` 用于计算、查询或取得与“host、名称”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] bool QSqlDatabase::isDriverAvailable(const QString &name)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `isDriverAvailable`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数 `name`：类型为 `const QString &`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QSqlDatabase::isOpen() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isOpen`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QSqlDatabase::isOpenError() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isOpenError`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QSqlDatabase::isValid() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isValid`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSqlError QSqlDatabase::lastError() const`

**API 类别：** 成员函数说明

**中文解读：** `QSqlDatabase::lastError` 用于计算、查询或取得与“末项、错误”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSqlError`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSqlError`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.8] bool QSqlDatabase::moveToThread(QThread *targetThread)`

**API 类别：** 成员函数说明

**中文解读：** `QSqlDatabase::moveToThread` 用于计算、查询或取得与“移动、转换输出、Thread”相关的操作。调用时要先确认当前状态和 `targetThread` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `targetThread`：类型为 `QThread *`。没有默认值，调用时必须提供。传入 `QThread *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSql::NumericalPrecisionPolicy QSqlDatabase::numericalPrecisionPolicy() const`

**API 类别：** 成员函数说明

**中文解读：** `QSqlDatabase::numericalPrecisionPolicy` 用于计算、查询或取得与“numerical、Precision、Policy”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSql::NumericalPrecisionPolicy`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSql::NumericalPrecisionPolicy`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QSqlDatabase::open()`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `open`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QSqlDatabase::open(const QString &user, const QString &password)`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `open`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`bool`。
- 参数 `user`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `password`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QSqlDatabase::password() const`

**API 类别：** 成员函数说明

**中文解读：** `QSqlDatabase::password` 用于计算、查询或取得与“password”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QSqlDatabase::port() const`

**API 类别：** 成员函数说明

**中文解读：** `QSqlDatabase::port` 用于计算、查询或取得与“port”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSqlIndex QSqlDatabase::primaryIndex(const QString &tablename) const`

**API 类别：** 成员函数说明

**中文解读：** `QSqlDatabase::primaryIndex` 用于计算、查询或取得与“primary、索引”相关的操作。调用时要先确认当前状态和 `tablename` 的有效范围；返回类型是 `QSqlIndex`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSqlIndex`。
- 参数 `tablename`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSqlRecord QSqlDatabase::record(const QString &tablename) const`

**API 类别：** 成员函数说明

**中文解读：** `QSqlDatabase::record` 用于计算、查询或取得与“record”相关的操作。调用时要先确认当前状态和 `tablename` 的有效范围；返回类型是 `QSqlRecord`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSqlRecord`。
- 参数 `tablename`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] void QSqlDatabase::registerSqlDriver(const QString &name, QSqlDriverCreatorBase *creator)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `registerSqlDriver`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `name`：类型为 `const QString &`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。
- 参数 `creator`：类型为 `QSqlDriverCreatorBase *`。没有默认值，调用时必须提供。传入 `QSqlDriverCreatorBase *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] void QSqlDatabase::removeDatabase(const QString &connectionName)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `removeDatabase`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `connectionName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QSqlDatabase::rollback()`

**API 类别：** 成员函数说明

**中文解读：** `QSqlDatabase::rollback` 用于计算、查询或取得与“rollback”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSqlDatabase::setConnectOptions(const QString &options = QString())`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setConnectOptions`。调用它会改变 `QSqlDatabase` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `options`：类型为 `const QString &`。默认值为 `QString()`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSqlDatabase::setDatabaseName(const QString &name)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setDatabaseName`。调用它会改变 `QSqlDatabase` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `name`：类型为 `const QString &`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSqlDatabase::setHostName(const QString &host)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setHostName`。调用它会改变 `QSqlDatabase` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `host`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSqlDatabase::setNumericalPrecisionPolicy(QSql::NumericalPrecisionPolicy precisionPolicy)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setNumericalPrecisionPolicy`。调用它会改变 `QSqlDatabase` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `precisionPolicy`：类型为 `QSql::NumericalPrecisionPolicy`。没有默认值，调用时必须提供。传入 `QSql::NumericalPrecisionPolicy` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSqlDatabase::setPassword(const QString &password)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPassword`。调用它会改变 `QSqlDatabase` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `password`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSqlDatabase::setPort(int port)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPort`。调用它会改变 `QSqlDatabase` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `port`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSqlDatabase::setUserName(const QString &name)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setUserName`。调用它会改变 `QSqlDatabase` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `name`：类型为 `const QString &`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringList QSqlDatabase::tables(QSql::TableType type = QSql::Tables) const`

**API 类别：** 成员函数说明

**中文解读：** `QSqlDatabase::tables` 用于计算、查询或取得与“tables”相关的操作。调用时要先确认当前状态和 `type` 的有效范围；返回类型是 `QStringList`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStringList`。
- 参数 `type`：类型为 `QSql::TableType`。默认值为 `QSql::Tables`。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.8] QThread *QSqlDatabase::thread() const`

**API 类别：** 成员函数说明

**中文解读：** `QSqlDatabase::thread` 用于计算、查询或取得与“thread”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QThread *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QThread *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QSqlDatabase::transaction()`

**API 类别：** 成员函数说明

**中文解读：** `QSqlDatabase::transaction` 用于计算、查询或取得与“transaction”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QSqlDatabase::userName() const`

**API 类别：** 成员函数说明

**中文解读：** `QSqlDatabase::userName` 用于计算、查询或取得与“user、名称”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSqlDatabase &QSqlDatabase::operator=(const QSqlDatabase &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSqlDatabase` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QSqlDatabase &`。
- 参数 `other`：类型为 `const QSqlDatabase &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

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
