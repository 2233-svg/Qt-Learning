# QSqlResult
> Qt 6.11.1 · Qt SQL · 来自 `QSqlResult`

## 1. 先建立直觉

`QSqlResult` 是 `QSqlQuery` 背后的结果集抽象。应用代码通常用 `QSqlQuery`，而 driver 实现者要实现 `QSqlResult`：执行 SQL、绑定参数、移动游标、读取列值、报告行数和错误。

它是 Qt SQL driver 开发的核心类之一。

## 2. 类说明

保留类说明：这些 API 来自 `QSqlResult`，属于 Qt SQL 模块，用于抽象 SQL 语句执行结果和游标。

多数函数是 protected，因为它们服务 `QSqlQuery` 与驱动内部协作。公开 API 只有析构和 `handle()` 这类少数入口。

## 3. API 速查

| API | 用来做什么 |
| --- | --- |
| `QSqlResult(driver)` | 由 driver 创建 result，绑定所属驱动。 |
| `reset(query)` | 执行原始 SQL，派生类必须实现。 |
| `prepare(query)` / `savePrepare(query)` | 准备 SQL，支持驱动原生或模拟预处理。 |
| `exec()` | 执行已准备语句。 |
| `bindValue()`、`addBindValue()` | 保存绑定参数。 |
| `boundValue*()`、`boundValues()` | 查询绑定参数和参数名。 |
| `BindingSyntax` | 位置绑定 `?` 或命名绑定 `:name`。 |
| `fetch(index)`、`fetchFirst()`、`fetchLast()`、`fetchNext()`、`fetchPrevious()` | 移动结果游标。 |
| `data(index)` | 返回当前行指定列值。 |
| `isNull(index)` | 判断当前列是否 SQL NULL。 |
| `record()` | 返回结果字段结构。 |
| `size()` | 返回结果行数；不支持时可返回 -1。 |
| `numRowsAffected()` | 返回受影响行数。 |
| `lastInsertId()` | 返回最后插入 ID。 |
| `lastError()` / `setLastError()` | 读取或设置结果级错误。 |
| `isActive()`、`isValid()`、`isSelect()` | 查询结果状态。 |
| `setActive()`、`setAt()`、`setSelect()`、`setQuery()` | 派生类维护状态。 |
| `setForwardOnly()` / `isForwardOnly()` | 控制单向游标模式。 |
| `clear()` | 清除绑定和值状态。 |
| `handle()` | 返回底层语句句柄，依驱动而定。 |

## 4. Driver 实现视角

一个 driver 的 `createResult()` 通常返回自定义 result：

```cpp
QSqlResult *MyDriver::createResult() const
{
    return new MyResult(this);
}
```

`MyResult` 至少要实现执行、取值、游标移动、行数和 NULL 判断。`QSqlQuery::next()` 最终会落到 result 的 fetch 逻辑。

## 5. 使用场景

| 场景 | 是否直接接触 |
| --- | --- |
| 普通查询 | 不直接接触，用 `QSqlQuery`。 |
| 调试底层语句句柄 | 可通过 `query.result()->handle()`，但要小心生命周期。 |
| 实现自定义 SQL driver | 必须实现 result 派生类。 |
| 支持存储过程 OUT 参数 | 需要正确处理绑定参数类型和 out values。 |

## 6. 常见坑与经验

`handle()` 返回的原生语句句柄只在 result 活着且底层语句未重置时可靠。query 重新执行、finish、clear 或连接关闭后，句柄可能失效。

forward-only 模式能降低内存和后端游标压力，但会限制随机访问。模型类通常需要非 forward-only 查询。

绑定参数的语法和驱动能力密切相关。没有原生 prepared query 的后端可能由 Qt 做模拟替换，转义和类型转换就更要谨慎。

## 7. 知识点覆盖

- `QSqlQuery` 与 `QSqlResult` 的内部关系。
- SQL 执行、预处理、绑定参数和游标移动。
- result 状态、错误、行数和字段记录。
- 自定义 driver 中 result 的实现责任。
- 原生语句句柄和 forward-only 模式。
