# QSqlError 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QSqlError>`  
> 所属模块：`Qt6::Sql`  
> 继承：无

## 它解决什么问题

`QSqlError` 是 Qt SQL 的错误值对象。数据库操作失败时，`QSqlDatabase::lastError()`、`QSqlQuery::lastError()` 等接口会返回它，用来同时保存 Qt driver 层信息、数据库原生错误信息和原生错误码。

```cpp
QSqlQuery query(db);
if (!query.exec("INSERT INTO users(name) VALUES ('Ada')")) {
    const QSqlError error = query.lastError();
    qWarning() << error.type()
               << error.nativeErrorCode()
               << error.text();
}
```

它解决的是“错误来源不同、格式不同”的问题：

- `driverText()`：Qt SQL driver 报告的文字；
- `databaseText()`：数据库服务器或数据库库报告的文字；
- `nativeErrorCode()`：具体数据库的错误码；
- `type()`：连接、SQL 语句、事务等错误类别；
- `text()`：前两类文字拼接后的便利展示。

## 如何记录和判断错误

业务代码不要只记录 `text()`。它适合日志展示，但跨数据库分析或针对性处理时，应同时保留 `type()` 和 `nativeErrorCode()`。例如唯一键冲突、断线、权限不足在不同数据库中的文本语言不同，但原生错误码和错误类型更适合建立可控的处理策略。

`isValid()` 用于判断对象中是否真的存在错误。它不表示“数据库连接现在一定可用”，也不表示错误已经恢复；只是说明此错误对象是否携带错误状态。

## 值类型与比较语义

`QSqlError` 是值类型，支持拷贝、移动和 `swap()`。比较运算符比较的是 `type()` 与 `nativeErrorCode()`，不是完整错误文本。因此两条不同描述文字但具有相同错误类别和原生码的错误可能被视为相等。

移动后的对象处于部分形成状态，只能销毁或重新赋值，不能继续读取其文本或类型。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型 | `enum ErrorType` | 描述错误发生的上下文类别。 | 用于区分连接、语句、事务等失败；原生错误码仍需结合数据库判断。 |
| 枚举值 | `NoError` | 表示没有 SQL 错误。 | 与 `isValid()` 一起判断，避免把默认对象当失败。 |
| 枚举值 | `ConnectionError` | 表示打开或使用连接时失败。 | 常需要重连或提示网络、凭据、服务状态问题。 |
| 枚举值 | `StatementError` | 表示 SQL 语句执行失败。 | 记录 SQL 上下文和绑定参数，但注意不要泄露敏感数据。 |
| 枚举值 | `TransactionError` | 表示事务操作失败。 | 回滚、连接状态和数据库事务规则都应重新确认。 |
| 枚举值 | `UnknownError` | 表示无法归类的错误。 | 保留完整 driver、database 文本和原生码以便排查。 |
| 构造 | `QSqlError(const QString &driverText = {}, const QString &databaseText = {}, ErrorType type = NoError, const QString &nativeErrorCode = {})` | 从各类错误信息构造错误对象。 | 通常由 Qt 返回；自定义 driver 构造时应分别填入不同来源的信息。 |
| 构造 | `QSqlError(const QSqlError &other)` | 拷贝错误对象。 | 值类型，可安全保存到日志、结果对象或跨层返回。 |
| 构造 | `QSqlError(QSqlError &&other)` | 移动构造错误对象。 | 被移动对象只能销毁或重新赋值。 |
| 析构 | `~QSqlError()` | 销毁错误对象。 | 普通值语义，无需手工管理资源。 |
| 数据库文本 | `databaseText() const` | 返回数据库报告的错误文字。 | 内容依数据库产品、驱动和语言环境而变化，可能为空。 |
| driver 文本 | `driverText() const` | 返回 Qt driver 报告的错误文字。 | 可能为空；与数据库文本并非互相替代。 |
| 有效性 | `isValid() const` | 判断错误对象是否表示已设置的错误。 | 只判断对象状态，不等价于连接是否已经恢复。 |
| 原生错误码 | `nativeErrorCode() const` | 返回数据库原生错误码。 | 有些 driver 可能用分号连接多个错误码；不要假设单一整数。 |
| 交换 | `swap(QSqlError &other)` | 高效且不会失败地交换两个错误对象。 | 用于需要避免额外拷贝的值对象处理。 |
| 汇总文本 | `text() const` | 将 driver 文本和数据库文本拼接为便于展示的字符串。 | 适合日志，不要只靠它做程序分支。 |
| 错误类型 | `type() const` | 返回错误类型。 | 某些不确定情况可能无法可靠确定具体类型。 |
| 不等比较 | `operator!=(const QSqlError &other) const` | 比较类型和原生错误码是否不同。 | 不比较完整错误文字。 |
| 移动赋值 | `operator=(QSqlError &&other)` | 以移动方式替换当前错误。 | 源对象移动后只可销毁或重新赋值。 |
| 拷贝赋值 | `operator=(const QSqlError &other)` | 以另一错误值替换当前错误。 | 适合保存最后错误快照。 |
| 相等比较 | `operator==(const QSqlError &other) const` | 比较类型和原生错误码是否相同。 | 相同不保证所有文字描述相同。 |

## 易错点

1. `text()` 适合给人看，程序处理优先结合 `type()` 和 `nativeErrorCode()`。
2. `databaseText()` 与 `driverText()` 都可能为空，不能只取其中一个。
3. `isValid()` 不等于连接处于健康状态。
4. 不能读取移动后 `QSqlError` 的内容。

### 一句话总结

`QSqlError` 是 Qt SQL 的分层错误快照：它同时保留 driver、数据库、原生码和错误类型，适合把用户提示与可分析的错误处理分开。
