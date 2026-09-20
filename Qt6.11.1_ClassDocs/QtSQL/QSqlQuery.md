# QSqlQuery
> Qt 6.11.1 · Qt SQL · 来自 `QSqlQuery`

## 1. 先建立直觉

`QSqlQuery` 是执行 SQL 语句和读取结果集的对象。它可以执行一次性 SQL，也可以 `prepare()` 后绑定参数，执行 `SELECT`、`INSERT`、`UPDATE`、存储过程或批处理。

记住一句话：`exec()` 成功只表示语句执行成功，不表示一定有结果行。读取结果必须先让游标定位到有效行，例如调用 `next()`。

## 2. 类说明

保留类说明：这些 API 来自 `QSqlQuery`，属于 Qt SQL 模块，用于准备、执行 SQL 并遍历结果。

`QSqlQuery` 依附某个数据库连接。默认构造或只传 SQL 字符串时会使用默认连接；大型程序建议显式传 `QSqlDatabase`，避免无意使用错误连接。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `QSqlQuery(db)` / `QSqlQuery(query, db)` | 在指定连接上创建 query，可立即执行 SQL。 |
| `prepare(sql)` | 预编译/准备 SQL，推荐配合绑定参数。 |
| `bindValue(name/index, value, type)` | 按命名或位置占位符绑定值。 |
| `addBindValue(value, type)` | 按顺序追加绑定值。 |
| `boundValue()`、`boundValues()`、`boundValueName()` | 调试和检查已绑定参数。 |
| `exec()` / `exec(sql)` | 执行已准备或临时 SQL。 |
| `execBatch()` | 批量执行绑定值列表。 |
| `next()`、`previous()`、`first()`、`last()`、`seek()` | 移动结果游标。 |
| `value(index/name)` | 读取当前行字段值。 |
| `isNull(index/name)` | 判断当前行字段是否为 SQL NULL。 |
| `record()` | 返回结果字段元数据。 |
| `size()` | 返回结果行数；驱动不支持时为 -1。 |
| `numRowsAffected()` | 返回受影响行数。 |
| `lastInsertId()` | 返回插入后的自增 ID，取决于驱动支持。 |
| `lastError()` | 获取查询级错误。 |
| `lastQuery()` / `executedQuery()` | 查看原始 SQL 或带绑定处理后的 SQL。 |
| `isActive()`、`isValid()`、`isSelect()` | 查询执行状态、游标状态和语句类型。 |
| `setForwardOnly()` / `isForwardOnly()` | 优化只向前读取的大结果集。 |
| `finish()` / `clear()` | 释放结果集资源或清空 query 状态。 |
| `nextResult()` | 访问存储过程/批处理的多个结果集。 |

## 4. 典型流程

```cpp
QSqlQuery query(db);
query.prepare("SELECT name, email FROM user WHERE id = :id");
query.bindValue(":id", userId);

if (!query.exec()) {
    qWarning() << query.lastError().text();
    return;
}

if (query.next()) {
    const QString name = query.value("name").toString();
}
```

批量插入：

```cpp
QSqlQuery q(db);
q.prepare("INSERT INTO log(message, level) VALUES (?, ?)");
q.addBindValue(messages);
q.addBindValue(levels);
if (!q.execBatch())
    qWarning() << q.lastError();
```

## 5. 使用场景

| 场景 | 建议 |
| --- | --- |
| 用户输入参与 SQL | 必须使用 `prepare()` + `bindValue()`，不要拼字符串。 |
| 大结果集导出 | `setForwardOnly(true)`，逐行 `next()` 处理。 |
| 插入后拿主键 | 检查 `lastInsertId()` 是否有效，兼容不同驱动。 |
| 存储过程或多结果集 | 使用 `nextResult()` 并分别读取每个结果。 |
| 调试 SQL | 输出 `lastError()`、`lastQuery()`、绑定值。 |

## 6. 常见坑与经验

不要混用命名占位符和位置占位符，尤其跨驱动时更容易出问题。选一种风格，项目内保持一致。

`value()` 只能在有效当前行上读取。刚 `exec()` 完、`next()` 之前，或 `next()` 已经返回 false 后，读取值都不可靠。

`size()` 并不总可信。很多数据库游标不会提前知道总行数，返回 -1 是正常行为；需要总数时写 `COUNT(*)`。

`QSqlQuery` 活着时可能占用数据库游标或锁。事务内长时间持有未 finish 的 SELECT，可能影响后续提交或写入。

## 7. 知识点覆盖

- SQL 准备、绑定参数和执行。
- 结果游标、当前行和字段读取。
- 查询错误、受影响行数、自增 ID。
- forward-only、大结果集和资源释放。
- 批处理、多结果集和驱动差异。
