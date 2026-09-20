# QSqlResult 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QSqlResult>`  
> 所属模块：`Qt6::Sql`  
> 继承：无

## 它解决什么问题

`QSqlResult` 是 SQL driver 实现“一个查询结果集”的底层抽象。它负责保存已绑定参数、执行 SQL、定位当前行、读取当前行列值、维护错误和暴露少量后端能力。

普通应用几乎总是使用 `QSqlQuery`，因为 `QSqlQuery` 正是对具体 `QSqlResult` 实现的通用包装。只有在编写新的 `QSqlDriver` 时，才需要派生 `QSqlResult` 并实现其纯虚函数。

```text
应用代码: QSqlQuery
              |
driver 实现: QSqlResult 子类
              |
数据库客户端库或协议
```

## driver 实现需要保持的状态机

一个 result 至少维护四组状态：

- **活动状态**：是否有可读取的结果集；
- **当前行位置**：`BeforeFirstRow`、有效零基行、`AfterLastRow`；
- **查询状态**：原始查询、实际执行查询、是否为 SELECT、最后错误；
- **绑定状态**：位置或名字占位符、值以及 In、Out、InOut 类型。

派生类在 `fetch()`、`fetchFirst()`、`fetchLast()`、`fetchNext()`、`fetchPrevious()` 成功定位后必须调用 `setAt()`；执行或重置状态时应同步 `setActive()`、`setSelect()` 和 `setLastError()`。否则上层 `QSqlQuery` 的 `isValid()`、`at()`、`lastError()` 等行为会失真。

## forward-only 的关键边界

`setForwardOnly(true)` 会让 result 只允许向前读取，减少缓存内存。它必须在执行前设置；执行后切换可能产生未定义结果甚至崩溃。对于 PostgreSQL，forward-only 结果集导航期间不能在同一连接上执行其它 SQL，否则当前结果可能丢失。

forward-only 查询的错误不只在执行后检查，还要在持续 `fetchNext()` 或上层 `QSqlQuery::next()` 之后检查，因为后端可能在拉取后续数据时才报告错误。

## 底层 handle 不是稳定扩展点

`handle()` 返回数据库相关的原生 result handle，并以 QVariant 封装。它可能无效、为空、在 clear 或 fetch 后失效，且类型依数据库而不同。只有已经确切了解 driver 的原生 API 和 QVariant 类型名时才使用；正常业务代码不要依赖它。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型 | `enum BindingSyntax` | 表示 prepared query 的占位符风格。 | driver 需与自身支持的 `?` 或命名占位符语法一致。 |
| 枚举值 | `PositionalBinding` | 使用位置占位符绑定。 | 参数次序必须与 SQL 占位符次序一致。 |
| 枚举值 | `NamedBinding` | 使用命名占位符绑定。 | 名称必须是已定义占位符，否则行为未定义。 |
| 构造 | `QSqlResult(const QSqlDriver *db)` | 用关联 driver 创建处于非活动状态的 result。 | 受保护；driver 指针必须在 result 生命周期内有效。 |
| 析构 | `~QSqlResult()` | 销毁 result 并释放资源。 | driver 和 result 的所有权由具体 driver 实现协调。 |
| 追加绑定 | `addBindValue(const QVariant &val, QSql::ParamType paramType)` | 将值绑定到下一可用位置。 | 受保护辅助函数；位置由内部绑定计数决定。 |
| 当前行位置 | `at() const` | 返回当前零基行位置或前首行、后末行特殊值。 | 仅用于 driver 实现；有效行还需结合 `isValid()`。 |
| 按位置绑定 | `bindValue(int index, const QVariant &val, QSql::ParamType paramType)` | 将参数绑定到指定位置。 | 下标和参数类型必须与后端 prepared statement 一致。 |
| 按名称绑定 | `bindValue(const QString &placeholder, const QVariant &val, QSql::ParamType paramType)` | 将参数绑定到指定命名占位符。 | 未定义占位符的绑定行为未定义。 |
| 查询绑定类型 | `bindValueType(int index) const` | 返回指定位置参数的 In、Out、InOut 类型。 | 越界处理由实现方保持一致。 |
| 查询绑定类型 | `bindValueType(const QString &placeholder) const` | 返回指定命名参数的类型。 | 名称必须和绑定语法、占位符表一致。 |
| 绑定语法 | `bindingSyntax() const` | 返回当前 prepared query 使用的绑定语法。 | 上层绑定逻辑与 driver 支持的语法必须匹配。 |
| 取绑定值 | `boundValue(int index) const` | 返回指定位置已绑定的值。 | 是绑定快照，不代表数据库最终类型转换结果。 |
| 取绑定值 | `boundValue(const QString &placeholder) const` | 返回指定名称已绑定的值。 | 名称找不到时不能当作有效空值处理。 |
| 绑定数量 | `boundValueCount() const` | 返回当前绑定参数数量。 | 用于实现方验证参数计数。 |
| 绑定名称 | `boundValueName(int index) const` | 返回指定位置绑定参数名。 | 位置绑定时名称可能为空或由实现定义。 |
| 全部绑定名称 | `boundValueNames() const` | 返回全部已绑定参数名称。 | 用于诊断和 driver 实现，不应记录敏感参数到普通日志。 |
| 全部绑定值 | `boundValues() const` | 返回绑定值列表只读副本。 | 可能含密码等敏感数据，调试输出须脱敏。 |
| 可变绑定列表 | `boundValues()` | 返回绑定值列表的可变引用。 | 仅派生实现内部使用，修改后需保持计数和名称映射一致。 |
| 清理结果 | `clear()` | 清空结果集并释放关联资源。 | 调用后原生 handle、当前行和数据都可能失效。 |
| 读取列数据 | `data(int index)` | 返回当前有效行指定列的 QVariant 数据。 | 纯虚；仅在活动、有效行和非负索引条件下被调用。 |
| 关联 driver | `driver() const` | 返回构造时关联的 driver。 | 非拥有指针；不能在 result 存活期间提前销毁 driver。 |
| 执行 | `exec()` | 执行已准备的查询并返回是否成功。 | 默认或派生实现应正确设置活动状态和最后错误。 |
| 实际执行 SQL | `executedQuery() const` | 返回后端实际执行的 SQL。 | 对不支持原生 prepared query 的后端，可能与原始查询不同。 |
| 任意定位 | `fetch(int index)` | 定位到指定零基行。 | 纯虚；成功后必须调用 `setAt()`。 |
| 定位首行 | `fetchFirst()` | 定位到第一行。 | 纯虚；活动结果为空时返回 false 并更新位置。 |
| 定位末行 | `fetchLast()` | 定位到最后一行。 | 纯虚；forward-only 后端通常无法高效或无法支持。 |
| 定位下一行 | `fetchNext()` | 定位到下一可用行。 | 默认可基于 fetch 实现；forward-only 只允许此方向。 |
| 定位上一行 | `fetchPrevious()` | 定位到上一行。 | forward-only 模式下不允许；派生类需正确处理边界。 |
| 原生句柄 | `handle() const` | 返回封装在 QVariant 中的数据库原生 result handle。 | 高风险且可能失效；先核对 QVariant 类型，普通业务代码避免使用。 |
| 输出参数 | `hasOutValues() const` | 判断是否存在 Out 或 InOut 绑定参数。 | 用于存储过程等 driver 支持场景。 |
| 活动状态 | `isActive() const` | 判断是否有可取回的结果。 | 活动不等于当前行有效，仍需 `isValid()`。 |
| 前向状态 | `isForwardOnly() const` | 判断结果是否只能前向导航。 | 查询执行前设置；后端可最终决定是否强制前向。 |
| 当前列 NULL | `isNull(int index)` | 判断当前行指定列是否为 NULL。 | 纯虚；只能在有效当前行读取。 |
| 是否 SELECT | `isSelect() const` | 判断当前语句是否 SELECT。 | 影响 size 和受影响行数等语义。 |
| 当前行有效性 | `isValid() const` | 判断当前位置是否为有效记录行。 | BeforeFirstRow 和 AfterLastRow 都为 false。 |
| 最后错误 | `lastError() const` | 返回此 result 的最后 SQL 错误。 | forward-only 查询还应在导航过程中检查。 |
| 最后插入 ID | `lastInsertId() const` | 返回最近插入行 ID，或无效 QVariant。 | 多行插入行为未定义；各数据库返回类型可能不同。 |
| 原始查询 | `lastQuery() const` | 返回当前 SQL 文本。 | 不同于 `executedQuery()` 可能替换绑定参数后的实际 SQL。 |
| 受影响行数 | `numRowsAffected()` | 返回最近查询影响行数，未知或 SELECT 为 -1。 | 纯虚；不要用它代替 SELECT 总行数。 |
| 准备查询 | `prepare(const QString &query)` | 准备带占位符的 SQL 以便重复执行。 | 返回 false 时通过 lastError 报告；可按后端重写。 |
| 当前记录结构 | `record() const` | 返回活动查询的当前 record 元数据。 | 默认实现为空；driver 应在需要时提供字段信息。 |
| 重置并执行 | `reset(const QString &query)` | 将 result 设为新 SQL 并准备数据读取。 | 纯虚；执行前应置非活动并定位到前首行，成功后更新状态。 |
| 重置绑定计数 | `resetBindCount()` | 重置追加绑定所使用的参数计数。 | 重新准备或重用 result 时保持绑定状态一致。 |
| 安全准备 | `savePrepare(const QString &query)` | 尽量利用后端 prepared statement 功能准备 SQL。 | 名称历史拼写为 savePrepare；通常由 driver 处理回退策略。 |
| 设置活动状态 | `setActive(bool active)` | 设置 result 内部活动标记。 | 派生类执行成功、失败、clear 时都要同步更新。 |
| 设置当前位置 | `setAt(int index)` | 设置当前零基行位置。 | 所有 fetch 实现必须维护，确保上层导航一致。 |
| 设置前向模式 | `setForwardOnly(bool forward)` | 请求前向只读或可滚动结果。 | 必须在执行前调用；PostgreSQL forward-only 期间不可在同连接执行其它 SQL。 |
| 设置最后错误 | `setLastError(const QSqlError &error)` | 更新 result 的最后错误。 | 失败路径应保留 driver 文本、数据库文本和原生码。 |
| 设置查询文本 | `setQuery(const QString &query)` | 设置当前查询文本但不执行。 | 之后必须调用 reset 才会真正执行。 |
| 设置 SELECT 标记 | `setSelect(bool select)` | 标记当前语句是否为 SELECT。 | 用于上层正确解释 size 与受影响行数。 |
| 结果大小 | `size()` | 返回 SELECT 结果行数，未知或非 SELECT 为 -1。 | 纯虚；forward-only 或流式后端通常无法预先给出大小。 |

## 易错点

1. 应用代码用 `QSqlQuery`，不要直接派生或操作 `QSqlResult`。
2. 每个 fetch 成功或失败路径都要维护 `setAt()`，否则上层游标状态错误。
3. `isActive()` 不表示当前行有效，读取数据前还需确认 `isValid()`。
4. `setForwardOnly()` 必须在执行前调用，且 PostgreSQL 有同连接命令限制。
5. `handle()` 是 driver 私有原生对象，可能在 clear 或导航后失效。

### 一句话总结

`QSqlResult` 是 SQL driver 的查询结果状态机：它实现绑定、执行、游标导航和数据读取，应用层通过 `QSqlQuery` 间接使用它。
