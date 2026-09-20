# QSqlError
> Qt 6.11.1 · Qt SQL · 来自 `QSqlError`

## 1. 先建立直觉

`QSqlError` 是 Qt SQL 的错误信息容器。连接失败、SQL 语句失败、事务提交失败时，`QSqlDatabase::lastError()`、`QSqlQuery::lastError()`、SQL model 的 `lastError()` 都会返回它。

它把错误拆成几层：Qt/驱动文本、数据库服务器文本、错误类型、原生错误码。诊断时不要只看 `text()`，原生错误码经常更适合日志和排查。

## 2. 类说明

保留类说明：这些 API 来自 `QSqlError`，属于 Qt SQL 模块，用于保存数据库操作错误。

`QSqlError` 是可拷贝值类型，不会自动追踪后续错误。你拿到的是某一刻的错误快照。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `QSqlError(driverText, databaseText, type, nativeCode)` | 构造错误对象。 |
| `driverText()` | Qt SQL 驱动层描述。 |
| `databaseText()` | 数据库后端返回的描述。 |
| `nativeErrorCode()` | 数据库/驱动原生错误码。 |
| `type()` | 错误类别。 |
| `text()` | 合并后的可读错误文本。 |
| `isValid()` | 判断是否真的有错误。 |
| `swap()`、拷贝/移动/比较操作 | 值类型操作。 |
| `NoError` | 无错误。 |
| `ConnectionError` | 打开连接、认证、网络、驱动加载等连接错误。 |
| `StatementError` | SQL 语句、绑定、执行、游标相关错误。 |
| `TransactionError` | `transaction()`、`commit()`、`rollback()` 相关错误。 |
| `UnknownError` | 无法分类的错误。 |

## 4. 典型流程

```cpp
if (!query.exec()) {
    const QSqlError error = query.lastError();
    qWarning() << error.type()
               << error.nativeErrorCode()
               << error.text();
}
```

连接错误和语句错误要分开记录：

```cpp
if (!db.open())
    reportConnectionFailure(db.lastError());
else if (!query.exec())
    reportStatementFailure(query.lastError(), query.lastQuery());
```

## 5. 使用场景

| 场景 | 关注点 |
| --- | --- |
| 用户提示 | 用简洁业务文案，避免直接暴露密码、主机细节或 SQL。 |
| 开发日志 | 记录 `type()`、`nativeErrorCode()`、`driverText()`、`databaseText()`。 |
| 自动重试 | 只对明确可恢复的连接/锁等待类错误重试。 |
| SQL model 调试 | `model.lastError()` 常能解释为什么 `select()` 失败。 |

## 6. 常见坑与经验

`isValid()` 是判断有没有错误的入口。空的 `QSqlError` 不是失败，只是“当前没有错误信息”。

`text()` 适合快速日志，但结构化日志最好分开记录各字段。数据库原生错误码对 DBA 或生产排障更有价值。

错误对象不会自动清除数据库状态。处理错误后，你仍需要决定是否 rollback、finish query、close connection 或重建连接。

## 7. 知识点覆盖

- SQL 错误层次：驱动、数据库、类型、原生码。
- 连接错误、语句错误、事务错误的区分。
- 用户提示与开发日志的不同信息粒度。
- 错误快照和后续恢复动作。
