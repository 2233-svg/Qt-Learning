# QSqlDriver
> Qt 6.11.1 · Qt SQL · 来自 `QSqlDriver`

## 1. 先建立直觉

`QSqlDriver` 是 Qt SQL 驱动抽象层。`QSqlDatabase` 面向应用提供连接 API，背后真正负责和 SQLite、PostgreSQL、MySQL、ODBC 等后端通信的是 driver。

普通业务代码很少直接调用它；你会在检查驱动能力、访问原生句柄、实现自定义驱动或数据库通知时接触它。

## 2. 类说明

保留类说明：这些 API 来自 `QSqlDriver`，属于 Qt SQL 模块，用于抽象数据库后端能力、连接、事务、语句生成和通知。

它继承 `QObject`，派生驱动必须实现 `open()`、`close()`、`createResult()`、`hasFeature()` 等核心虚函数。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `open(db, user, password, host, port, options)` | 打开底层数据库连接。 |
| `close()` | 关闭底层连接。 |
| `isOpen()` / `isOpenError()` | 查询连接状态。 |
| `lastError()` / `setLastError()` | 读取或设置驱动级错误。 |
| `beginTransaction()` / `commitTransaction()` / `rollbackTransaction()` | 事务钩子。 |
| `createResult()` | 创建 `QSqlResult`，供 `QSqlQuery` 执行语句。 |
| `hasFeature(feature)` | 查询事务、BLOB、预处理、批处理、通知等能力。 |
| `tables(type)` / `record(table)` / `primaryIndex(table)` | 查询数据库元数据。 |
| `escapeIdentifier()` / `stripDelimiters()` / `isIdentifierEscaped()` | 处理表名、字段名引用。 |
| `formatValue(field, trim)` | 把字段值格式化成 SQL 字面量。 |
| `sqlStatement(type, table, record, prepared)` | 根据 record 生成 SELECT/INSERT/UPDATE/DELETE 片段。 |
| `handle()` | 返回底层原生连接句柄，类型依驱动而定。 |
| `subscribeToNotification()` / `unsubscribeFromNotification()` | 订阅数据库通知。 |
| `notification(name, source, payload)` | 数据库事件通知信号。 |
| `setNumericalPrecisionPolicy()` / `numericalPrecisionPolicy()` | 数值精度策略。 |
| `connectionName()` | Qt 6.9 起查询所属连接名。 |
| `maximumIdentifierLength()` | 查询表名/字段名最大长度。 |

## 4. DriverFeature 速查

| Feature | 说明 |
| --- | --- |
| `Transactions` | 支持事务。 |
| `QuerySize` | 能报告结果行数。 |
| `BLOB` | 支持二进制大对象。 |
| `Unicode` | 支持 Unicode 字符串。 |
| `PreparedQueries` | 支持预处理语句。 |
| `NamedPlaceholders` / `PositionalPlaceholders` | 支持命名或位置占位符。 |
| `LastInsertId` | 能返回最后插入 ID。 |
| `BatchOperations` | 支持批处理。 |
| `EventNotifications` | 支持数据库通知。 |
| `MultipleResultSets` | 支持多个结果集。 |
| `CancelQuery` | 支持取消正在执行的查询。 |

## 5. 使用场景

| 场景 | 用法 |
| --- | --- |
| 写跨数据库代码 | 先用 `hasFeature()` 判断能力，再选择策略。 |
| 访问数据库原生 API | `handle()` 取底层连接，但要严控生命周期。 |
| 自定义 Qt SQL 驱动 | 派生 `QSqlDriver` 并配套 `QSqlResult`。 |
| PostgreSQL LISTEN/NOTIFY 等通知 | 使用通知订阅 API，前提是驱动支持。 |

## 6. 常见坑与经验

不要在业务层大量依赖 `handle()`。原生句柄类型、生命周期和线程规则都由驱动决定；连接关闭或重连后，旧句柄可能立即失效。

`hasFeature()` 是跨驱动代码的事实入口。不要因为 SQLite 支持某行为，就假设 ODBC、MySQL、PostgreSQL 都一样。

`formatValue()` 和 `sqlStatement()` 是驱动辅助，不是用户输入安全的替代品。外部输入仍应走 prepared query 和绑定参数。

数据库通知不是所有驱动都支持，也不是通用消息队列。断线重连、事务提交时机、payload 格式都要按数据库后端测试。

## 7. 知识点覆盖

- Qt SQL driver 与 database/query/result 的分层。
- 驱动能力探测和跨数据库差异。
- 标识符转义、SQL 语句辅助生成和元数据查询。
- 原生句柄、数据库通知和自定义驱动实现。
