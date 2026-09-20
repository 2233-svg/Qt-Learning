# QSqlDriver：Qt SQL 驱动的抽象边界

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QSqlDriver>`  
> 模块：`Qt6::Sql`  
> 继承：`QObject`  
> 相关类：`QSqlDatabase`、`QSqlResult`、`QSqlDriverPlugin`

## 它解决什么问题

`QSqlDriver` 是 Qt SQL 与具体数据库客户端库之间的适配层。SQLite、PostgreSQL、MySQL、ODBC 等驱动都通过它把“打开连接、执行语句、报告能力、读取元数据、事务、事件通知”翻译成 Qt 的统一接口。

普通应用的正确入口是 `QSqlDatabase`：

```text
普通应用
QSqlDatabase -> QSqlQuery / SQL 模型

驱动开发
QSqlDatabase -> QSqlDriver -> QSqlResult -> 数据库客户端库
```

因此，`QSqlDriver` 不是应用层“更高级的数据库对象”。它是抽象基类，直接使用没有意义；只有在 Qt 没有现成驱动、需要包装专有数据库协议或维护驱动插件时，才需要派生它。

## 它和其他类怎样协作

- `QSqlDatabase` 保存驱动并调用它打开、关闭连接、查询元数据和开启事务。
- `QSqlDriver::createResult()` 为查询创建对应的 `QSqlResult`。
- `QSqlResult` 实现 SQL 语句执行、游标移动、绑定参数和字段取值等低层行为。
- `QSqlDriverPlugin` 让驱动可作为 Qt 插件按键名加载。

一个自定义驱动至少需要实现四个纯虚函数：

1. `open()`：连接数据库并正确维护打开状态和错误。
2. `close()`：释放底层连接与相关资源。
3. `createResult()`：创建与该驱动匹配的结果对象。
4. `hasFeature()`：准确报告实际支持的能力。

## 什么时候需要派生

确实需要的情形：

- 接入 Qt 没有提供驱动的数据库或专有数据服务。
- 封装现有 C/C++ 数据库客户端库，使其能被 `QSqlDatabase` 使用。
- 做数据库通知、专用元数据或 SQL 方言适配。

通常不需要的情形：

- 只是执行 SQL：使用 `QSqlQuery`。
- 只是开连接：使用 `QSqlDatabase`。
- 只是希望访问某个原生句柄：先确认现有驱动的 `handle()` 文档和生命周期，尽量避免绕过 Qt 层。

## 驱动实现的状态契约

`open()` 不是只返回 `true` 或 `false`。派生类应在成功时调用 `setOpen(true)`、清除打开错误状态，并在失败时设置精确的 `QSqlError`、调用 `setOpen(false)` 和 `setOpenError(true)`。`close()` 后应让打开状态与资源事实一致。

`hasFeature()` 也不是静态宣传页。有些能力取决于连接后的服务器版本、权限或连接选项，因此应在真实连接成功后才能可靠判断。错误报告和能力报告不准确，会让 `QSqlQuery`、模型以及业务层基于错误前提运行。

## SQL 生成、标识符和绑定值

`escapeIdentifier()` 和 `stripDelimiters()` 处理的是表名、列名等**标识符**；`formatValue()` 处理字段字面量。它们主要给驱动实现和框架内部 SQL 生成使用。

应用代码不要用 `formatValue()` 拼接不可信数据。普通参数化查询仍应使用 `QSqlQuery::prepare()` 与绑定值。标识符无法用绑定值表达时，也应从固定白名单中选择，并使用正确的驱动转义规则。

`sqlStatement()` 依据 `QSqlRecord` 和 `StatementType` 生成通用 SQL 片段。它对 `QSqlTableModel` 一类框架功能很重要，但不是业务代码的 SQL 构建器。

## 原生句柄和事件通知

`handle()` 用 `QVariant` 暴露可选的原生数据库句柄。它可能无效，也可能以驱动特定指针类型封装；连接关闭、重连或驱动销毁后都不能继续使用。除非现有驱动文档明确支持，否则不要依赖它。

若驱动支持 `EventNotifications`，可实现订阅接口，并在数据库事件到来时发射 `notification()`。订阅必须发生在连接打开之后，关闭连接时应自动取消订阅。

## API 速查表

`DriverFeature` 常用能力项：

- `Transactions`：支持事务。
- `QuerySize`：可报告查询总行数。
- `BLOB`、`Unicode`：支持二进制大对象和 Unicode。
- `PreparedQueries`、`NamedPlaceholders`、`PositionalPlaceholders`：预处理和占位符能力。
- `LastInsertId`、`BatchOperations`、`MultipleResultSets`、`CancelQuery`：执行扩展能力。
- `EventNotifications`：支持数据库事件通知。
- `FinishQuery`：能主动结束活动查询。

其余枚举：

- `IdentifierType`：`FieldName` 或 `TableName`，决定标识符转义语义。
- `NotificationSource`：`UnknownSource`、`SelfSource`、`OtherSource`，说明通知来源。
- `StatementType`：`WhereStatement`、`SelectStatement`、`UpdateStatement`、`InsertStatement`、`DeleteStatement`。

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QSqlDriver(QObject *parent)` | 构造驱动基类并设置 QObject 父对象。 | 仅派生类构造函数调用；普通应用不实例化驱动。 |
| 生命周期 | `~QSqlDriver()` | 销毁驱动对象。 | 确保底层连接和结果对象已按驱动约定释放。 |
| 必须实现 | `open(const QString &db, const QString &user, const QString &password, const QString &host, int port, const QString &options)` | 打开底层数据库连接。 | 纯虚函数；必须同步设置打开状态、打开错误和 `lastError`。 |
| 必须实现 | `close()` | 关闭底层连接并释放资源。 | 纯虚函数；关闭后不应保留可用的原生句柄或订阅。 |
| 必须实现 | `createResult()` | 创建与本驱动对应的 `QSqlResult`。 | 纯虚函数；结果对象要能正确回调该驱动。 |
| 必须实现 | `hasFeature(DriverFeature feature)` | 报告是否支持一项驱动能力。 | 纯虚函数；部分能力要等连接成功后才能准确判断。 |
| 事务 | `beginTransaction()` | 开始底层事务。 | 支持事务时重写并与 `Transactions` 特性保持一致。 |
| 事务 | `commitTransaction()` | 提交底层事务。 | 失败时设置可诊断的 `QSqlError`。 |
| 事务 | `rollbackTransaction()` | 回滚底层事务。 | 活动结果集可能被后端限制，需按客户端库规则处理。 |
| 连接信息 | `connectionName()` | 返回此驱动关联的 Qt 连接名。 | Qt 6.9 引入；连接名不是数据库名。 |
| 连接状态 | `isOpen()` | 返回驱动是否处于打开状态。 | 应由派生类通过 `setOpen()` 维护，不要只检查指针非空。 |
| 连接状态 | `isOpenError()` | 返回最近一次打开是否失败。 | 具体失败原因从 `lastError()` 取得。 |
| 连接状态 | `lastError()` | 返回驱动最近错误。 | 失败路径必须设置，避免上层只看到空错误。 |
| 连接状态 | `setOpen(bool open)` | 设置基类保存的打开状态。 | 受保护；在 `open()` 和 `close()` 实现中正确调用。 |
| 连接状态 | `setOpenError(bool error)` | 设置基类保存的打开错误状态。 | 受保护；成功重连时要清除旧错误状态。 |
| 连接状态 | `setLastError(const QSqlError &error)` | 设置驱动最近错误对象。 | 受保护；保留数据库错误码和客户端库信息。 |
| 数值精度 | `setNumericalPrecisionPolicy(QSql::NumericalPrecisionPolicy)` | 设置驱动默认数值精度策略。 | 新查询可能继承该策略；Qt 6.8 起也作为属性提供。 |
| 数值精度 | `numericalPrecisionPolicy()` | 返回当前驱动默认精度策略。 | 查询级策略可以覆盖该默认值。 |
| 标识符 | `escapeIdentifier(const QString &identifier, IdentifierType type)` | 为表名或字段名添加正确的数据库定界符。 | 只处理标识符，不是为数据值做防注入。 |
| 标识符 | `isIdentifierEscaped(const QString &identifier, IdentifierType type)` | 判断标识符是否已按本驱动规则定界。 | 用于驱动内部避免重复转义。 |
| 标识符 | `stripDelimiters(const QString &identifier, IdentifierType type)` | 去掉标识符的驱动专属定界符。 | 适合内部解析；不要假设所有后端使用同一种引号。 |
| 标识符 | `maximumIdentifierLength(IdentifierType type)` | 返回标识符允许的最大长度。 | Qt 6.0 引入；不同后端和对象类别可能不同。 |
| SQL 值 | `formatValue(const QSqlField &field, bool trimStrings)` | 按驱动方言格式化一个字段值。 | 用于驱动/框架 SQL 生成，业务查询仍优先绑定参数。 |
| SQL 生成 | `sqlStatement(StatementType type, const QString &tableName, const QSqlRecord &rec, bool preparedStatement)` | 根据记录生成通用 WHERE、SELECT、INSERT 等 SQL。 | 关注 `generated` 字段和是否生成占位符；通常仅供派生类使用。 |
| 原生访问 | `handle()` | 返回可选的驱动专属原生句柄。 | `QVariant` 类型和生命周期均依赖驱动；关闭或重连后可能失效。 |
| 元数据 | `tables(QSql::TableType tableType)` | 返回数据库中指定类型的表名。 | 默认实现可为空；派生类应按后端元数据 API 实现。 |
| 元数据 | `record(const QString &tableName)` | 返回表字段描述。 | 默认实现未必支持；用于 `QSqlDatabase::record()` 等上层 API。 |
| 元数据 | `primaryIndex(const QString &tableName)` | 返回表主键索引描述。 | 默认实现未必支持；影响 `QSqlTableModel` 的更新定位。 |
| 事件通知 | `subscribeToNotification(const QString &name)` | 订阅数据库事件。 | 连接必须已打开；仅在支持 `EventNotifications` 时实现。 |
| 事件通知 | `unsubscribeFromNotification(const QString &name)` | 取消订阅数据库事件。 | 关闭连接时应自动取消全部订阅。 |
| 事件通知 | `subscribedToNotifications()` | 返回当前已订阅事件名列表。 | 与订阅和取消订阅接口保持一致。 |
| 事件通知 | `notification(const QString &name, NotificationSource source, const QVariant &payload)` | 向上层发出数据库事件通知。 | 信号应在正确线程发射；载荷类型和来源要明确。 |

## 常见错误

- 业务代码直接依赖 `QSqlDriver`：应通过 `QSqlDatabase` 和 `QSqlQuery` 使用稳定公共接口。
- `hasFeature()` 无条件返回乐观值：上层会调用后端不支持的能力并得到难排查错误。
- `open()` 失败却未设置 `lastError()`、`setOpenError(true)`：用户只能得到空白失败信息。
- 把 `escapeIdentifier()` 当作字符串参数绑定：标识符转义和数据值绑定是两件事。
- 缓存 `handle()` 返回的原生指针：重连、关闭或驱动销毁后都可能悬空。
- 只实现订阅不实现取消订阅：连接关闭或重复连接时容易留下后端资源。
