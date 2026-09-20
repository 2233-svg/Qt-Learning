# Qt SQL（上）：数据库连接、查询与事务

> 适用版本：Qt 6.11.1  
> 核心类型：`QSqlDatabase`、`QSqlQuery`、`QSqlError`、`QSqlRecord`、`QSqlDriver`

Qt SQL 提供统一 C++ 接口，真正能力仍由 SQLite、PostgreSQL、MySQL、ODBC 等驱动和数据库决定。

```text
QSqlDatabase：命名连接和事务
       ↓
QSqlQuery：准备、绑定、执行、遍历结果
       ↓
QSqlDriver：底层驱动能力与差异
```

## 1. 构建配置

```cmake
find_package(Qt6 REQUIRED COMPONENTS Sql)
target_link_libraries(mytarget PRIVATE Qt6::Sql)
```

SQLite 驱动通常作为 Qt 插件部署。编译时找到 Qt SQL 不代表运行时一定能加载 `QSQLITE`。

```cpp
qDebug() << QSqlDatabase::drivers();
qDebug() << QSqlDatabase::isDriverAvailable("QSQLITE");
```

## 2. 最小可用 SQLite 示例

```cpp
#include <QCoreApplication>
#include <QDebug>
#include <QSqlDatabase>
#include <QSqlError>
#include <QSqlQuery>

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);

    QSqlDatabase db = QSqlDatabase::addDatabase("QSQLITE");
    db.setDatabaseName("notes.db");

    if (!db.open()) {
        qCritical() << db.lastError().text();
        return 1;
    }

    QSqlQuery query(db);
    if (!query.exec(
            "CREATE TABLE IF NOT EXISTS note ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "title TEXT NOT NULL)")) {
        qCritical() << query.lastError().text();
        return 1;
    }

    query.prepare("INSERT INTO note(title) VALUES(:title)");
    query.bindValue(":title", QStringLiteral("学习 Qt SQL"));
    if (!query.exec()) {
        qCritical() << query.lastError().text();
        return 1;
    }

    if (!query.exec("SELECT id, title FROM note ORDER BY id")) {
        qCritical() << query.lastError().text();
        return 1;
    }

    while (query.next())
        qDebug() << query.value(0).toLongLong()
                 << query.value(1).toString();

    return 0;
}
```

SQLite 的数据库名是文件路径；`":memory:"` 创建仅存在于当前连接生命周期内的内存数据库。

## 3. 连接名称不是数据库名称

```cpp
QSqlDatabase db = QSqlDatabase::addDatabase(
    "QSQLITE", "application-main");
db.setDatabaseName(databasePath);
```

- `application-main` 是 Qt 连接注册表中的唯一名字。
- `databasePath` 是 SQLite 文件；服务端数据库则是库名。
- 同一数据库可以有多个独立连接。

取回连接：

```cpp
QSqlDatabase db = QSqlDatabase::database("application-main");
```

不传连接名会使用默认连接。小程序方便，大型程序中显式命名能避免库和测试互相替换默认连接。

### 3.1 QSqlDatabase 是共享连接句柄

它是值类型，但复制不会复制物理连接；多个副本指向注册表中的同一命名连接。修改一个副本的连接配置会影响同一连接的其他副本。

需要独立连接可用 `cloneDatabase()`，但克隆后仍需在正确线程打开。

## 4. 正确移除连接

`removeDatabase()` 要求所有引用该连接的 `QSqlDatabase` 和 `QSqlQuery` 已销毁：

```cpp
void runTask()
{
    const QString name = QStringLiteral("temporary");
    {
        QSqlDatabase db = QSqlDatabase::addDatabase("QSQLITE", name);
        db.setDatabaseName(":memory:");
        db.open();

        QSqlQuery query(db);
        query.exec("SELECT 1");
    } // query 和 db 句柄先离开作用域

    QSqlDatabase::removeDatabase(name);
}
```

仍有引用时移除会产生警告并使现有查询失效。`close()` 关闭物理连接，`removeDatabase()` 才从 Qt 注册表移除名字。

不要让 `QSqlDatabase` 成为比 `QCoreApplication` 更晚析构的全局/静态对象。

## 5. 打开不同数据库

SQLite：

```cpp
db.setDatabaseName(QDir(appDataDir).filePath("app.sqlite"));
db.open();
```

PostgreSQL 等服务端连接：

```cpp
QSqlDatabase db = QSqlDatabase::addDatabase("QPSQL", "main");
db.setHostName("db.example.com");
db.setPort(5432);
db.setDatabaseName("appdb");
db.setUserName(userName);
db.setPassword(password);
db.setConnectOptions("connect_timeout=5");
db.open();
```

连接选项语法由驱动决定。密码不要硬编码或输出日志。连接失败同时记录 `driverText()`、`databaseText()` 和 `nativeErrorCode()`，对用户只显示适当信息。

## 6. QSqlError

```cpp
const QSqlError error = query.lastError();
qWarning() << error.type()
           << error.driverText()
           << error.databaseText()
           << error.nativeErrorCode();
```

错误来源可能是连接、语句、事务或未知错误。原生错误码与文案依赖数据库，不能跨驱动只靠字符串匹配实现业务分支。

## 7. 准备语句与参数绑定

```cpp
QSqlQuery query(db);
query.prepare(R"SQL(
    SELECT id, title
    FROM note
    WHERE title LIKE :pattern
      AND id > :minimumId
    ORDER BY id
)SQL");
query.bindValue(":pattern", "%" + keyword + "%");
query.bindValue(":minimumId", minimumId);

if (!query.exec())
    qWarning() << query.lastError();
```

绑定参数用于数据值，避免 SQL 注入并让驱动处理类型和转义。

### 7.1 不能绑定表名和列名

占位符只代表值：

```sql
SELECT * FROM note WHERE title = :title
```

不能写：

```sql
SELECT :column FROM :table
```

动态标识符必须从程序白名单选择，再由驱动 `escapeIdentifier()` 处理。绝不能把用户输入直接拼成表名、排序列或 SQL 片段。

### 7.2 命名和位置占位符

```cpp
query.prepare("INSERT INTO note(title) VALUES(?)");
query.addBindValue(title);
```

不要在同一语句混用两种形式。不同驱动对占位符语法支持有差异，查询 `QSqlDriver::PreparedQueries` 能力，并在目标数据库测试。

## 8. NULL、空字符串与无效 QVariant

数据库 NULL 不等于空字符串或数值 0：

```cpp
const QVariant value = query.value("nickname");
if (value.isNull())
    qDebug() << "数据库 NULL";
else
    qDebug() << value.toString();
```

写入 NULL：

```cpp
query.bindValue(":nickname", QVariant(QMetaType::fromType<QString>()));
```

业务结构应明确哪些字段可空。把所有 NULL 默默转成空值会丢失语义。

## 9. 执行与遍历

`exec()` 成功后，SELECT 查询通常位于第一条记录之前：

```cpp
while (query.next()) {
    const qint64 id = query.value("id").toLongLong();
    const QString title = query.value("title").toString();
}
```

常见定位 API：`first()`、`last()`、`previous()`、`seek()`。并非所有驱动都支持可滚动结果集。

大结果集只向前遍历时，在 prepare/exec 前设置：

```cpp
query.setForwardOnly(true);
```

这可能显著降低内存，但之后不能随意向后定位。Qt 6.8+ 可检查 `isForwardOnly()`。

### 9.1 不依赖 size()

许多驱动对 SELECT 的 `QSqlQuery::size()` 返回 `-1`。需要数量时执行明确的 `COUNT(*)`，或遍历时计数。

### 9.2 受影响行数和自增 ID

```cpp
if (query.exec()) {
    qDebug() << query.numRowsAffected();
    qDebug() << query.lastInsertId();
}
```

两者的支持和准确性依赖驱动。不要把 `lastInsertId()` 当成跨数据库通用协议；PostgreSQL 常通过 `RETURNING` 更明确地取得新 ID。

## 10. 批量执行

```cpp
QSqlQuery query(db);
query.prepare("INSERT INTO note(title) VALUES(?)");
query.addBindValue(QStringList{"A", "B", "C"});

if (!query.execBatch())
    qWarning() << query.lastError();
```

批量能力、数组绑定和返回行为依赖驱动。大量写入还应放在事务中，否则每条自动提交会非常慢。

## 11. 事务

```cpp
if (!db.transaction()) {
    qWarning() << db.lastError();
    return false;
}

QSqlQuery query(db); // 事务开始后再创建查询
bool ok = query.prepare("UPDATE account SET balance=balance+:d WHERE id=:id");

if (ok) {
    query.bindValue(":d", -amount);
    query.bindValue(":id", fromId);
    ok = query.exec();
}
if (ok) {
    query.bindValue(":d", amount);
    query.bindValue(":id", toId);
    ok = query.exec();
}

if (ok)
    ok = db.commit();
else
    db.rollback();

if (!ok) {
    db.rollback(); // commit 失败时也尝试回滚
    qWarning() << db.lastError();
}
return ok;
```

事务应在创建相关 Query 之前开始。提交本身也可能失败，例如连接断开或约束延迟检查失败。

### 11.1 驱动能力

```cpp
if (!db.driver()->hasFeature(QSqlDriver::Transactions))
    qWarning() << "驱动不支持事务";
```

数据库还可能隐式提交 DDL。事务隔离级别、保存点和锁行为都由数据库/驱动决定，不能只凭 Qt API 假设一致。

### 11.2 RAII 事务守卫思路

生产代码可封装守卫：构造时 `transaction()`，显式 `commit()` 后标记成功，析构时若未提交则 `rollback()`。但析构函数不能可靠报告 rollback 错误，关键路径仍要显式检查。

## 12. 查询生命周期

`QSqlQuery` 仍活动时可能占用服务器 cursor 或阻碍某些数据库提交/关闭：

```cpp
query.finish();
```

它释放当前结果集资源，但保留查询对象以便重用。离开作用域也会清理。

不要在遍历同一 Query 时对它重新 `exec()`；新执行会替换当前结果集。嵌套查询使用另一个 `QSqlQuery`，并确认驱动支持同一连接上同时活动的多个结果集。

## 13. SQL 可移植性边界

Qt 统一连接和结果接口，不统一 SQL 方言：

| 差异 | 示例 |
|---|---|
| 自增主键 | SQLite AUTOINCREMENT、PostgreSQL identity/sequence |
| 分页 | LIMIT/OFFSET、FETCH FIRST |
| UPSERT | 各数据库语法不同 |
| 布尔/日期类型 | 存储和转换不同 |
| 标识符大小写 | 引号和折叠规则不同 |
| RETURNING | 支持范围不同 |
| DDL 事务 | 数据库行为不同 |

如果产品只支持一个数据库，就明确测试该方言；若声称跨库，建立每种驱动的自动化集成测试。

## 14. 常见错误

### 14.1 拼接用户输入

SQL 注入不仅来自 WHERE 值，也来自排序字段、LIMIT 和表名。值使用绑定，标识符使用白名单。

### 14.2 忽略每次返回值

`open()`、`prepare()`、`exec()`、`transaction()`、`commit()` 都可能失败。成功路径不能掩盖前一步错误。

### 14.3 removeDatabase 时 Query 仍存在

会警告且行为失效。用嵌套作用域先销毁所有句柄。

### 14.4 把连接复制当成连接池

复制 `QSqlDatabase` 只是共享同一命名连接，不会得到独立物理连接。

### 14.5 用 size() 判断 SELECT 行数

不少驱动返回 -1。使用 COUNT 或遍历。

### 14.6 把 NULL 当空字符串

会丢失业务语义并影响筛选、唯一约束和更新判断。

## 15. API 速查

| API | 用途 |
|---|---|
| `addDatabase()` | 注册命名连接 |
| `database()` | 获取现有连接句柄 |
| `removeDatabase()` | 无引用后移除连接 |
| `open()` / `close()` | 打开/关闭物理连接 |
| `prepare()` | 准备带占位符语句 |
| `bindValue()` / `addBindValue()` | 绑定值 |
| `exec()` / `execBatch()` | 执行单条/批量语句 |
| `next()` / `value()` | 遍历和读取结果 |
| `setForwardOnly()` | 优化只向前的大结果集 |
| `numRowsAffected()` | 非 SELECT 影响行数 |
| `lastInsertId()` | 驱动支持时取得新 ID |
| `finish()` | 释放活动结果集资源 |
| `transaction()` / `commit()` / `rollback()` | 事务边界 |
| `lastError()` | 获取结构化 SQL 错误 |

## 16. 自测题

1. 连接名与数据库名有什么区别？
2. 复制 QSqlDatabase 会创建新物理连接吗？
3. 为什么 removeDatabase 前要销毁 Query 和连接句柄？
4. 绑定参数能否代表表名？
5. SELECT 后为什么先调用 next()？
6. 为什么不能依赖 query.size()？
7. 事务应在创建相关 Query 前还是后开始？
8. commit 是否一定成功？
9. setForwardOnly 应在何时设置？
10. Qt SQL 是否统一了所有数据库 SQL 方言？

## 17. 参考答案

1. 连接名是 Qt 注册表中的身份；数据库名/路径是后端实际目标。
2. 不会，副本共享同一命名连接。
3. 活动引用会让移除操作警告并使查询失效。
4. 不能，占位符只代表数据值；标识符必须白名单选择并正确转义。
5. 执行后游标位于第一条之前，`next()` 才移动到有效记录。
6. 许多驱动对 SELECT 返回 -1；应 COUNT 或遍历。
7. 之前。
8. 不一定，连接或延迟约束等问题可使提交失败。
9. prepare/exec 之前。
10. 没有，Qt 统一 C++ 接口，方言和数据库行为仍不同。

## 18. 本篇结论

```text
显式命名并打开正确线程中的连接
  → prepare + bind 数据值
  → 检查每一步结果和 QSqlError
  → 流式遍历结果，不假设 size()
  → 多步写操作用事务，并检查 commit
  → Query/连接句柄销毁后再 removeDatabase
```

下篇继续讲线程与每线程连接、迁移和连接池边界，以及 `QSqlQueryModel`、`QSqlTableModel`、`QSqlRelationalTableModel` 如何接入 Model/View。
