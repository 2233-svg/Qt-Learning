# QSqlDatabase
> Qt 6.11.1 · Qt SQL · 来自 `QSqlDatabase`

## 1. 先建立直觉

`QSqlDatabase` 是 Qt SQL 的连接句柄。它不表示某张表，也不直接保存查询结果；它表示“用哪个驱动、哪个连接名、哪些连接参数，连到哪一个数据库会话”。

最关键的概念是连接名。Qt 在进程内维护一张连接表，`addDatabase()` 把连接放进去，`database(name)` 按名字取回，`removeDatabase(name)` 移除。默认连接只是没有显式命名时使用的那一项，不是全局魔法。

## 2. 类说明

保留类说明：这些 API 来自 `QSqlDatabase`，属于 Qt SQL 模块，用于管理数据库驱动、连接参数、事务和连接级元数据。

`QSqlDatabase` 是值对象式句柄，拷贝它不会复制一个新的物理连接，而是引用同一个连接条目。关闭或移除连接前，必须确保相关 `QSqlQuery`、SQL model 和其它句柄都已经销毁或脱离。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `addDatabase(type, connectionName)` | 创建并注册连接，驱动如 `QSQLITE`、`QMYSQL`、`QPSQL`。 |
| `addDatabase(QSqlDriver *, connectionName)` | 使用已有底层驱动对象注册连接。 |
| `database(connectionName, open)` | 取回连接；`open=true` 时会尝试自动打开。 |
| `removeDatabase(connectionName)` | 从连接表移除连接；移除前不能还有活跃引用。 |
| `cloneDatabase(other, connectionName)` | 复制连接参数到新连接名，但新连接未打开。 |
| `contains()` / `connectionNames()` | 检查连接是否存在、列出连接名。 |
| `drivers()` / `isDriverAvailable()` | 查询可用 SQL 驱动。 |
| `registerSqlDriver()` | 注册自定义驱动创建器。 |
| `setDatabaseName()`、`setHostName()`、`setPort()` | 设置数据库、主机、端口；通常必须在 `open()` 前。 |
| `setUserName()`、`setPassword()`、`open(user, password)` | 设置认证信息；避免长期保存明文密码时用 `open(user, password)`。 |
| `setConnectOptions()` / `connectOptions()` | 设置驱动特定选项，如 SSL、ODBC 参数。 |
| `open()` / `close()` | 打开或关闭连接。 |
| `isOpen()`、`isOpenError()`、`isValid()` | 读取连接状态。 |
| `lastError()` | 读取最近连接级错误。 |
| `transaction()`、`commit()`、`rollback()` | 控制事务。 |
| `driver()`、`driverName()` | 访问底层 SQL driver 信息。 |
| `tables()`、`record(table)`、`primaryIndex(table)` | 查询数据库元数据。 |
| `setNumericalPrecisionPolicy()` / `numericalPrecisionPolicy()` | 控制数值读取精度策略。 |
| `moveToThread()` / `thread()` | Qt 6.8 起移动或查询连接所属线程。 |

## 4. 典型流程

```cpp
QSqlDatabase db = QSqlDatabase::addDatabase("QSQLITE", "app");
db.setDatabaseName("app.db");
if (!db.open()) {
    qWarning() << db.lastError().text();
    return;
}

QSqlQuery query(db);
query.exec("CREATE TABLE IF NOT EXISTS note(id INTEGER PRIMARY KEY, text TEXT)");
```

事务写法：

```cpp
if (!db.transaction())
    return;

if (!saveA(db) || !saveB(db)) {
    db.rollback();
    return;
}
if (!db.commit())
    qWarning() << db.lastError();
```

## 5. 使用场景

| 场景 | 关注点 |
| --- | --- |
| SQLite 本地存储 | `QSQLITE`、数据库文件路径、事务批量写入。 |
| 客户端连接 MySQL/PostgreSQL | 驱动部署、主机端口、SSL、连接失败诊断。 |
| 多数据库或多租户 | 显式连接名，避免覆盖默认连接。 |
| 多线程数据库访问 | 每个线程自己的连接；不要跨线程共用 query/model。 |
| SQL model 展示 | model 构造时传入正确 `QSqlDatabase`。 |

## 6. 常见坑与经验

不要反复 `addDatabase()` 不带连接名。这样会不断替换默认连接，旧 query/model 还活着时会留下难查的问题。

`removeDatabase()` 前要让所有引用该连接的 `QSqlDatabase` 句柄、`QSqlQuery`、`QSqlQueryModel`、`QSqlTableModel` 都离开作用域。否则 Qt 会警告连接仍在使用，后续行为也容易悬空。

连接参数大多要在 `open()` 前设置。连接已经打开后改 databaseName、host、connectOptions 通常不会影响当前物理连接，应该 close 后重新 open。

事务支持取决于驱动和数据库引擎。SQLite、MySQL 的不同存储引擎、ODBC 后端行为都可能不同；提交失败时不要假设数据已经完整写入。

## 7. 知识点覆盖

- 连接名、默认连接和连接表。
- 驱动选择、驱动部署和自定义驱动注册。
- 连接参数、打开/关闭、错误读取。
- 事务边界和失败回滚。
- 连接线程归属和 SQL model/query 生命周期。
