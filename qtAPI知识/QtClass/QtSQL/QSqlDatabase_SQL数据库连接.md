# QSqlDatabase：SQL 连接的注册表入口

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QSqlDatabase>`  
> 模块：`Qt6::Sql`  
> 相关类：`QSqlDriver`、`QSqlQuery`、`QSqlTableModel`、`QSqlError`

## 它到底解决什么问题

`QSqlDatabase` 管理的是一个**具名数据库连接**。它负责选择驱动、保存连接参数、打开物理连接，并让 `QSqlQuery`、SQL 模型等对象能找到同一条连接。

它不是“数据库本身”，也不是独占连接对象。它是值类型句柄：同名连接被多个 `QSqlDatabase` 副本取得后，副本指向同一个底层连接；通过其中一个副本修改参数或关闭连接，会影响其余副本。

典型关系如下：

```text
QSqlDatabase("reporting")
  -> QSqlDriver
  -> 物理数据库连接
  -> QSqlQuery / QSqlQueryModel / QSqlTableModel
```

日常程序应通过 `QSqlDatabase` 使用数据库。只有编写数据库驱动时，才直接面对 `QSqlDriver`。

## 什么时候使用

- 应用启动时创建并配置 SQLite、MySQL、PostgreSQL、ODBC 等连接。
- 同一应用同时连接多个数据库，例如业务库、报表库和测试库。
- 为每个工作线程建立或克隆自己的连接。
- 在模型/视图程序中把特定连接显式传给 `QSqlTableModel`。

不适合把它当作长期成员变量随处保存。Qt 明确建议按需调用 `database(connectionName)` 取得句柄；若成员对象比 `QCoreApplication` 活得更久，关闭程序时可能出现未定义行为。

## 最小可用连接

```cmake
find_package(Qt6 REQUIRED COMPONENTS Sql)
target_link_libraries(mytarget PRIVATE Qt6::Sql)
```

```cpp
#include <QSqlDatabase>
#include <QSqlError>
#include <QDebug>

QSqlDatabase db = QSqlDatabase::addDatabase("QSQLITE", "app");
db.setDatabaseName("app.sqlite");

if (!db.open())
    qWarning() << db.lastError().text();
```

这里的 `"app"` 是**连接名**，`"app.sqlite"` 才是 SQLite 文件名。两者不能混为一谈。

## 连接模型与关键边界

### 1. 默认连接只是一个未命名的全局槽位

不传 `connectionName` 给 `addDatabase()`，创建的就是默认连接；之后不带连接名的 `database()`、`contains()` 等静态调用都会指向它。小型示例很方便，实际应用中建议为每个用途取唯一名称，避免组件互相覆盖默认连接。

再次以相同名称调用 `addDatabase()` 会替换旧连接。此时旧连接的所有已有句柄都会失效，因此不要用它“重新配置”一个仍被查询或模型使用的连接。

### 2. 一条连接只属于一个线程

连接只能由创建它的线程访问。工作线程需要自己的连接，而不是把主线程连接直接传过去。常用方式是在线程内调用 `addDatabase()`，或用 `cloneDatabase()` 复制参数后在目标线程打开。

Qt 6.8 起可调用 `moveToThread()` 移动连接与驱动的线程归属，但连接上不能还有绑定的 `QSqlQuery`；失败时返回 `false`。

### 3. `removeDatabase()` 的前提比 `close()` 严格

`close()` 只关闭物理连接，连接注册项和所有句柄仍存在。`removeDatabase(name)` 则从 Qt 的连接注册表删除该条目。

调用 `removeDatabase()` 前，必须让该连接的所有 `QSqlDatabase` 副本和 `QSqlQuery` 都先离开作用域或被重置；否则会产生 Qt 警告，并可能泄漏资源或留下无效结果集。

```cpp
{
    QSqlDatabase db = QSqlDatabase::database("app");
    QSqlQuery query(db);
    query.exec("SELECT 1");
} // db 和 query 均已销毁

QSqlDatabase::removeDatabase("app");
```

### 4. 事务要考虑活动的 SELECT

先用 `driver()->hasFeature(QSqlDriver::Transactions)` 确认能力，再调用 `transaction()`、`commit()` 或 `rollback()`。某些数据库在同一连接仍有活动的 `SELECT` 查询时无法提交或回滚；结束读取或调用 `QSqlQuery::finish()` 后再处理事务。

## 常用工作流

### 显式使用具名连接

```cpp
QSqlDatabase db = QSqlDatabase::addDatabase("QPSQL", "analytics");
db.setHostName("db.example.internal");
db.setDatabaseName("analytics");
db.setUserName("reader");
db.setPassword(password);

if (!db.open()) {
    qWarning() << db.lastError().databaseText()
               << db.lastError().driverText();
    return;
}

QSqlQuery query(db);
query.exec("SELECT count(*) FROM events");
```

### 在线程中克隆配置

```cpp
const auto workerDb =
    QSqlDatabase::cloneDatabase("analytics", "analytics-worker");

// 在 workerDb 所属线程中打开并使用它。
if (!workerDb.open())
    qWarning() << workerDb.lastError().text();
```

`cloneDatabase()` 复制连接参数和驱动类型，但新连接仍需 `open()`；它不是共享同一条底层连接的快捷方式。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造与复制 | `QSqlDatabase()` | 创建无效的数据库句柄。 | 它本身不创建连接；先 `addDatabase()` 或 `database()`。 |
| 构造与复制 | `QSqlDatabase(const QSqlDatabase &other)` | 复制另一个连接句柄。 | 副本共享同一底层连接和配置。 |
| 构造与复制 | `operator=(const QSqlDatabase &other)` | 让当前句柄改指向另一个连接。 | 赋值不会复制物理连接；旧引用关系会改变。 |
| 构造与复制 | `~QSqlDatabase()` | 释放当前句柄引用。 | 析构不等于删除具名连接注册项。 |
| 受保护构造 | `QSqlDatabase(QSqlDriver *driver)` | 用自定义驱动创建连接对象。 | 驱动编写或注册场景使用，普通应用不用。 |
| 受保护构造 | `QSqlDatabase(const QString &type)` | 按驱动类型构造内部连接对象。 | 由 Qt 连接管理机制使用。 |
| 注册连接 | `addDatabase(const QString &type, const QString &connectionName)` | 按驱动键创建并注册一个连接。 | 同名会替换旧连接；生产代码建议总是给唯一名称。 |
| 注册连接 | `addDatabase(QSqlDriver *driver, const QString &connectionName)` | 注册调用方提供的驱动实例。 | 连接接管 `driver` 所有权，调用方不能再删除它。 |
| 克隆连接 | `cloneDatabase(const QSqlDatabase &other, const QString &connectionName)` | 按已有句柄的参数创建独立连接配置。 | 新连接未打开，常用于每线程一连接。 |
| 克隆连接 | `cloneDatabase(const QString &other, const QString &connectionName)` | 按已有连接名克隆连接配置。 | 源连接必须存在；目标名必须避免冲突。 |
| 取得连接 | `database(const QString &connectionName, bool open)` | 按名称取得已注册连接的句柄。 | 默认会尝试打开；返回的是共享连接句柄。 |
| 取得连接 | `contains(const QString &connectionName)` | 判断指定连接名是否已注册。 | 只说明注册项存在，不代表已打开或可用。 |
| 取得连接 | `connectionNames()` | 列出当前所有连接名。 | 用于诊断和关闭清理，别把列表当线程同步机制。 |
| 取得连接 | `connectionName()` | 返回当前句柄关联的连接名。 | 无效句柄返回值没有可用连接语义。 |
| 驱动发现 | `drivers()` | 列出 Qt 当前可用的 SQL 驱动键。 | 驱动插件缺失时列表中不会出现对应键。 |
| 驱动发现 | `isDriverAvailable(const QString &name)` | 判断某个驱动键是否可用。 | 在 `addDatabase()` 前检查，可输出更清楚的部署错误。 |
| 驱动信息 | `driver()` | 返回底层 `QSqlDriver` 指针。 | 指针由连接拥有；普通查询优先通过高层 API 完成。 |
| 驱动信息 | `driverName()` | 返回创建连接时指定的驱动键。 | 它是 Qt 驱动名，不一定等于数据库品牌字符串。 |
| 配置 | `setDatabaseName(const QString &name)` | 设置数据库名、文件名、DSN 或连接串。 | 具体含义随驱动变化；它不是连接名。 |
| 配置 | `databaseName()` | 读取数据库名配置。 | 只是配置值，不表示连接一定已经打开。 |
| 配置 | `setHostName(const QString &host)` | 设置服务器主机名。 | SQLite 等嵌入式驱动通常不需要它。 |
| 配置 | `hostName()` | 读取服务器主机名配置。 | 空字符串可能是合法配置。 |
| 配置 | `setPort(int port)` | 设置服务器端口。 | `-1` 表示由驱动使用默认端口。 |
| 配置 | `port()` | 读取端口配置。 | 不能由此判断实际已连接端口。 |
| 配置 | `setUserName(const QString &name)` | 设置认证用户名。 | 生产环境避免把凭据写死在源码。 |
| 配置 | `userName()` | 读取用户名配置。 | 用户名可为空，具体取决于驱动。 |
| 配置 | `setPassword(const QString &password)` | 设置连接密码。 | 尽量缩短明文凭据在内存中的存活时间。 |
| 配置 | `password()` | 读取密码配置。 | 不要记录到日志或显示给用户。 |
| 配置 | `setConnectOptions(const QString &options)` | 设置驱动专属连接选项。 | 选项通常应在 `open()` 前设置；传空字符串可清空。 |
| 配置 | `connectOptions()` | 返回当前连接选项字符串。 | 语法完全依赖具体驱动。 |
| 数值精度 | `setNumericalPrecisionPolicy(QSql::NumericalPrecisionPolicy)` | 设置本连接查询的数值精度策略。 | 会被新建查询继承；高精度金额要选对策略。 |
| 数值精度 | `numericalPrecisionPolicy()` | 返回连接的数值精度策略。 | 查询自身设置可覆盖连接级默认值。 |
| 打开与关闭 | `open()` | 使用已配置参数建立物理连接。 | 失败后立即检查 `lastError()`。 |
| 打开与关闭 | `open(const QString &user, const QString &password)` | 用临时用户名和密码打开连接。 | 不会替代所有永久配置项；仍需数据库名等参数。 |
| 打开与关闭 | `close()` | 关闭物理连接。 | 不删除注册项；已有查询和模型的可用性要自行管理。 |
| 状态与错误 | `isOpen()` | 判断连接是否已打开。 | 打开并不自动说明每条 SQL 都会成功。 |
| 状态与错误 | `isOpenError()` | 判断最近一次打开是否出错。 | 获取错误细节仍应使用 `lastError()`。 |
| 状态与错误 | `isValid()` | 判断句柄是否指向有效连接。 | 有效不等于已打开。 |
| 状态与错误 | `lastError()` | 返回最近一次数据库或驱动错误。 | 每次失败路径都应记录 `databaseText()` 和 `driverText()`。 |
| 元数据 | `tables(QSql::TableType type)` | 列出表、视图或系统表名称。 | 先确保连接已经打开；结果依赖权限和驱动实现。 |
| 元数据 | `record(const QString &tableName)` | 读取表字段的 `QSqlRecord` 描述。 | 是元数据快照，不会让模型自动同步。 |
| 元数据 | `primaryIndex(const QString &tableName)` | 读取表主键索引信息。 | 没有主键或驱动不支持时结果可能为空。 |
| 事务 | `transaction()` | 开始数据库事务。 | 先确认驱动支持事务；成功后必须提交或回滚。 |
| 事务 | `commit()` | 提交当前事务。 | 活动 SELECT 可能让部分数据库提交失败。 |
| 事务 | `rollback()` | 回滚当前事务。 | 同样可能受活动查询限制；失败时检查错误。 |
| 线程 | `thread()` | 返回连接和驱动当前所属线程。 | Qt 6.8 引入；用于诊断线程归属。 |
| 线程 | `moveToThread(QThread *targetThread)` | 把连接和驱动移到目标线程。 | 不能有绑定的 `QSqlQuery`；失败会返回 `false`。 |
| 注册扩展 | `registerSqlDriver(const QString &name, QSqlDriverCreatorBase *creator)` | 注册自定义 SQL 驱动创建器。 | Qt 接管 `creator` 所有权；属于驱动开发场景。 |
| 删除连接 | `removeDatabase(const QString &connectionName)` | 从全局注册表移除具名连接。 | 先销毁所有 `QSqlDatabase` 副本和活动查询，否则资源泄漏。 |

## 最容易踩的坑

- 把数据库名当连接名：`setDatabaseName()` 不能修改连接注册名。
- 多个模块都偷偷使用默认连接：后创建者可能替换前一个连接。
- 跨线程传递同一条连接：每个线程应独立创建或克隆连接。
- `removeDatabase()` 时局部 `QSqlDatabase db` 仍在作用域内：先让所有句柄和查询销毁。
- 事务失败只看布尔值：应同时检查 `lastError()`，并确认是否仍有活动查询。
