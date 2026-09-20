# QSqlQuery：执行 SQL 并遍历结果集

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QSqlQuery>`  
> 模块：`Qt6::Sql`  
> 相关类：`QSqlDatabase`、`QSqlResult`、`QSqlRecord`、`QSqlError`

## 它解决什么问题

`QSqlQuery` 是 Qt SQL 的语句执行器和结果游标。它把一条 SQL 语句交给某个 `QSqlDatabase` 连接执行，并为 `SELECT` 的结果提供逐行访问能力。

它覆盖两类任务：

- 执行无结果集的语句，例如 `INSERT`、`UPDATE`、`DELETE`、DDL。
- 执行 `SELECT`，用游标在返回行之间移动并读取字段值。

`QSqlQuery` 不负责建立连接，不负责把结果显示为表格，也不负责自动把修改缓存后提交。连接属于 `QSqlDatabase`；表格展示用 `QSqlQueryModel`；单表编辑用 `QSqlTableModel`。

```text
QSqlDatabase
  -> QSqlQuery::prepare / exec
  -> QSqlResult（驱动层结果对象）
  -> next / value / record
```

## 什么时候选它

- 需要参数化插入、更新、删除或调用存储过程。
- 需要流式读取大结果集，不想一次塞进模型。
- 需要多结果集、受影响行数、最后插入 ID 等底层执行信息。
- 需要完全控制 SQL，而不是受单表模型的筛选和编辑策略约束。

如果只是把只读查询交给 `QTableView` 显示，优先考虑 `QSqlQueryModel`。如果是单表可编辑界面，优先考虑 `QSqlTableModel`。

## 最小示例：预处理与绑定

```cpp
#include <QSqlQuery>
#include <QSqlError>
#include <QDebug>

QSqlQuery query(QSqlDatabase::database("app"));
query.prepare(
    "INSERT INTO person (id, name, age) "
    "VALUES (:id, :name, :age)");
query.bindValue(":id", 42);
query.bindValue(":name", "Lin");
query.bindValue(":age", 20);

if (!query.exec())
    qWarning() << query.lastError().text();
```

绑定值用于**数据值**，不是 SQL 标识符。不能写成 `SELECT * FROM :table` 期待绑定表名；表名、列名、排序方向等 SQL 结构必须通过受控白名单生成，必要时使用驱动的 `escapeIdentifier()`。

## 先理解两个状态

### 执行状态：`isActive()`

SQL 成功执行后，查询通常处于 active 状态。失败则 inactive。再次执行任何 SQL 后，当前位置都会回到“无效记录”状态。

### 当前位置：`isValid()`

即使一个 `SELECT` 已经成功执行，刚执行完也还没有指向首行。先调用 `next()`、`first()`、`seek()` 等移动到一条实际记录，再用 `value()` 或 `record()` 读取数据。

```cpp
QSqlQuery query("SELECT id, name FROM person", db);
while (query.next()) {
    const int id = query.value(0).toInt();
    const QString name = query.value(1).toString();
}

if (query.lastError().isValid())
    qWarning() << query.lastError().text();
```

`isActive()` 表示语句执行状态，`isValid()` 表示当前是否真的指向一行；二者不能互相替代。

## 参数绑定的四个重点

### 1. 在 `prepare()` 后、`exec()` 前绑定

可使用命名占位符 `:name`，也可使用位置占位符 `?`。同一条语句应坚持一种风格，保证参数顺序清晰。

```cpp
query.prepare("UPDATE person SET name = ? WHERE id = ?");
query.addBindValue("Mira");
query.addBindValue(42);
query.exec();
```

### 2. 输出参数不是普通输入参数

存储过程可以为绑定值指定 `QSql::In`、`Out` 或 `InOut`。执行后应通过 `boundValue()` 读取输出参数，并确认目标驱动支持此用法。

### 3. `execBatch()` 的数据布局要与模式对应

默认 `ValuesAsRows` 表示每个绑定位置对应一个值列表，每一轮从每个列表取同一索引的值；`ValuesAsColumns` 是面向数组参数的另一种布局。批处理支持与具体驱动有关。

### 4. PostgreSQL 的 `?` 需要额外留意

PostgreSQL 的 JSON 等操作符也会使用问号。Qt 6.7 的 `setPositionalBindingEnabled(false)` 可关闭 Qt 对 `?` 的位置绑定解析，但只在驱动原生支持位置绑定时才有意义。

## 前向模式并非只是性能开关

`setForwardOnly(true)` 必须在 `prepare()` 或执行之前调用。它可能减少缓存和内存使用，但结果只能向前移动：`next()` 和正向 `seek()` 可用，`previous()`、`first()`、`last()` 等随机访问不应依赖。

执行后再改变前向模式可能得到不可预测结果，甚至崩溃。并且前向查询的错误可能在读取过程中才显现，所以不只要在 `exec()` 后检查 `lastError()`，循环结束后也要再检查一次。

## 事务与活动查询

某些驱动在活动的 `SELECT` 还没有结束时，不允许同一连接 `commit()` 或 `rollback()`。读取完成后可调用 `finish()` 释放结果资源，或让查询对象销毁，然后再处理事务。

## API 速查表

`BatchExecutionMode` 的取值：

- `ValuesAsRows`：每个占位符绑定一个列表，每一轮取各列表的同位置元素。
- `ValuesAsColumns`：把每个绑定值视为一行中的列值，适合特定数组参数布局。

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QSqlQuery(QSqlResult *result)` | 用指定驱动结果对象构造查询。 | 驱动实现层使用；`result` 的所有权和生命周期须遵循 Qt 驱动约定。 |
| 构造 | `QSqlQuery(const QSqlDatabase &db)` | 创建绑定到指定连接的空查询。 | 推荐显式传入具名连接，避免误用默认连接。 |
| 构造 | `QSqlQuery(const QString &query, const QSqlDatabase &db)` | 构造时立即执行 SQL。 | 不能在构造后再设置前向模式；失败要检查 `lastError()`。 |
| 构造 | `QSqlQuery(QSqlQuery &&other)` | 移动构造查询。 | Qt 6.2 引入；移动后不要再依赖源对象的状态。 |
| 生命周期 | `~QSqlQuery()` | 销毁查询及其结果资源。 | 若事务受活动查询阻塞，可显式 `finish()` 提前结束。 |
| 生命周期 | `operator=(QSqlQuery &&other)` | 移动赋值查询状态。 | 目标查询原有的执行状态会被替换。 |
| 生命周期 | `swap(QSqlQuery &other)` | 快速交换两个查询的内部状态。 | Qt 6.2 引入；适合资源转移，不改变连接本身。 |
| 执行 | `prepare(const QString &query)` | 准备一条可绑定参数的 SQL。 | 先确认返回值；只给数据值使用占位符。 |
| 执行 | `exec()` | 执行已准备的语句及当前绑定值。 | 每次执行后都检查返回值和 `lastError()`。 |
| 执行 | `exec(const QString &query)` | 直接执行一条 SQL 字符串。 | 外部输入不要用拼接 SQL；优先 `prepare()` 加绑定。 |
| 执行 | `execBatch(BatchExecutionMode mode)` | 按多个绑定值批量执行已准备语句。 | 参数列表长度和布局必须一致；先确认驱动的批处理能力。 |
| 执行 | `clear()` | 清除查询、结果集和绑定值。 | 之后需要重新 `prepare()` 或 `exec()`。 |
| 执行 | `finish()` | 让查询变为 inactive 并释放结果资源。 | 读取完大结果或提交事务前很有用。 |
| 执行信息 | `lastQuery()` | 返回最后一次准备或执行的原始 SQL。 | 预处理语句通常仍保留占位符。 |
| 执行信息 | `executedQuery()` | 返回驱动实际执行的 SQL 表示。 | 某些驱动会改写或模拟预处理，不能把它当安全审计原文。 |
| 执行信息 | `lastError()` | 返回最近一次查询错误。 | 前向读取时循环结束后也应检查。 |
| 执行信息 | `lastInsertId()` | 返回最近一次插入生成的 ID。 | 并非所有驱动或表结构都支持；无效 `QVariant` 表示不可用。 |
| 执行信息 | `numRowsAffected()` | 返回非 SELECT 语句影响的行数。 | 驱动不能报告时值可能是 `-1`。 |
| 执行信息 | `size()` | 返回 SELECT 的总行数。 | 只有驱动支持 `QuerySize` 时可靠；否则返回 `-1`。 |
| 执行信息 | `nextResult()` | 切换到下一结果集。 | 仅对存储过程或多语句且驱动支持多结果集时有意义。 |
| 绑定参数 | `addBindValue(const QVariant &val, QSql::ParamType type)` | 按下一个位置追加绑定值。 | 顺序必须与 `?` 占位符一致。 |
| 绑定参数 | `bindValue(int pos, const QVariant &val, QSql::ParamType type)` | 按位置绑定一个值。 | 位置从 `0` 开始。 |
| 绑定参数 | `bindValue(const QString &placeholder, const QVariant &val, QSql::ParamType type)` | 按命名占位符绑定一个值。 | 通常使用带 `:` 的占位符名，例如 `:id`。 |
| 绑定参数 | `boundValue(int pos)` | 读取指定位置的绑定值。 | 输出参数应在成功执行后读取。 |
| 绑定参数 | `boundValue(const QString &placeholder)` | 读取指定名称的绑定值。 | 名称需与准备时使用的占位符一致。 |
| 绑定参数 | `boundValues()` | 返回全部绑定值。 | 用于诊断时注意不要泄漏密码等敏感数据。 |
| 绑定参数 | `boundValueName(int pos)` | 返回某位置绑定值的名称。 | Qt 6.6 引入；位置无效时结果为空。 |
| 绑定参数 | `boundValueNames()` | 返回所有命名绑定值的名称。 | Qt 6.6 引入；位置占位符未必有名称。 |
| 位置绑定 | `setPositionalBindingEnabled(bool enable)` | 控制 Qt 是否把 `?` 解析为位置占位符。 | Qt 6.7 引入；处理 PostgreSQL 问号运算符时使用。 |
| 位置绑定 | `isPositionalBindingEnabled()` | 返回位置绑定解析是否启用。 | Qt 6.7 引入；不是所有驱动都受此设置影响。 |
| 数值精度 | `setNumericalPrecisionPolicy(QSql::NumericalPrecisionPolicy)` | 设置本查询读取数值字段的精度策略。 | 会覆盖连接级策略；金融数据应明确选择。 |
| 数值精度 | `numericalPrecisionPolicy()` | 返回当前查询精度策略。 | 未单独设置时通常继承连接策略。 |
| 前向模式 | `setForwardOnly(bool forward)` | 设置结果集是否只允许向前遍历。 | 必须在 `prepare()` 或执行前调用。 |
| 前向模式 | `isForwardOnly()` | 返回结果集实际是否为前向模式。 | 数据库可决定是否采用；以这个返回值为准。 |
| 游标状态 | `isActive()` | 判断最近执行是否成功且结果仍活动。 | active 不等于已指向有效记录。 |
| 游标状态 | `isSelect()` | 判断当前语句是否返回结果集。 | 导航函数应只用于活动的 SELECT。 |
| 游标状态 | `isValid()` | 判断当前游标是否指向一条实际记录。 | 读取 `value()` 前应保证为 `true`。 |
| 游标状态 | `at()` | 返回当前行索引或特殊位置标识。 | 首行索引为 `0`；不要用它替代 `isValid()`。 |
| 导航 | `next()` | 移到下一条记录。 | 最常用的逐行读取方式；返回 `false` 后检查错误。 |
| 导航 | `previous()` | 移到上一条记录。 | 前向模式不支持；要求活动 SELECT。 |
| 导航 | `first()` | 移到第一条记录。 | 需要可滚动结果集；空结果返回 `false`。 |
| 导航 | `last()` | 移到最后一条记录。 | 可能触发读取完整结果；前向模式不能用。 |
| 导航 | `seek(int index, bool relative)` | 绝对或相对移动到指定记录。 | 前向模式只能安全地正向移动。 |
| 读取结果 | `value(int index)` | 读取当前行中按列索引定位的字段值。 | 索引读取比按名称快；先确保 `isValid()`。 |
| 读取结果 | `value(QAnyStringView name)` | 读取当前行中按字段名定位的值。 | Qt 6.8 起参数为 `QAnyStringView`；按名查找较慢。 |
| 读取结果 | `isNull(int field)` | 判断当前行指定列是否为 SQL NULL。 | 不要用 `QVariant` 的转换结果推断 NULL。 |
| 读取结果 | `isNull(QAnyStringView name)` | 判断当前行指定字段名是否为 SQL NULL。 | 字段不存在时要结合记录结构判断。 |
| 读取结果 | `record()` | 返回当前查询的字段信息及当前行值。 | 只需取值时优先 `value(index)`，速度更好。 |
| 底层访问 | `driver()` | 返回本查询使用的驱动指针。 | 指针不由查询拥有；普通程序很少需要它。 |
| 底层访问 | `result()` | 返回底层 `QSqlResult` 指针。 | 驱动或诊断场景使用，不要依赖具体派生类型。 |

## 常见错误

- `exec()` 成功后立刻 `value(0)`：还没移动到第一行，应先 `next()`。
- 用字符串拼接用户输入：值应使用 `prepare()` 和 `bindValue()`。
- 执行后才调用 `setForwardOnly(true)`：这是未定义风险，不是可选优化。
- 认为 `size()` 一定返回行数：许多驱动会返回 `-1`。
- 事务提交失败只盯着连接：检查是否有仍 active 的 `SELECT` 查询。
