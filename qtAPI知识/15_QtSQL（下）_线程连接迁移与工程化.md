# Qt SQL（下）：线程连接、迁移与工程化

> 适用版本：Qt 6.11.1  
> 核心主题：连接线程归属、每线程连接、schema migration、SQLite 并发、连接池、测试与安全

上篇和中篇解决了查询及界面模型。本篇解决数据库代码进入真实项目后的生命周期问题。

## 1. 最重要的线程规则

数据库连接只能在创建它的线程中使用：

```text
线程 A 创建 connection A → 只在线程 A 查询
线程 B 创建 connection B → 只在线程 B 查询
```

复制 `QSqlDatabase` 句柄再传给线程 B，不会复制物理连接，也不会改变线程归属。

## 2. 推荐模式：在 Worker 所属线程创建连接

```cpp
class DatabaseWorker : public QObject
{
    Q_OBJECT

public slots:
    void initialize(QString databasePath)
    {
        m_connectionName = QStringLiteral("worker-%1")
            .arg(reinterpret_cast<quintptr>(QThread::currentThreadId()));

        QSqlDatabase db = QSqlDatabase::addDatabase(
            "QSQLITE", m_connectionName);
        db.setDatabaseName(databasePath);
        db.setConnectOptions("QSQLITE_BUSY_TIMEOUT=5000");

        if (!db.open())
            emit failed(db.lastError().text());
    }

    void loadNotes()
    {
        QSqlDatabase db = QSqlDatabase::database(m_connectionName);
        QSqlQuery query(db);
        query.prepare("SELECT id, title FROM note ORDER BY id");
        if (!query.exec()) {
            emit failed(query.lastError().text());
            return;
        }

        QList<NoteDto> notes;
        while (query.next())
            notes.push_back({query.value(0).toLongLong(),
                             query.value(1).toString()});
        emit notesLoaded(notes);
    }

signals:
    void notesLoaded(const QList<NoteDto> &notes);
    void failed(const QString &message);

private:
    QString m_connectionName;
};
```

建立线程：

```cpp
auto *thread = new QThread(&app);
auto *worker = new DatabaseWorker;
worker->moveToThread(thread);

QObject::connect(thread, &QThread::finished,
                 worker, &QObject::deleteLater);
thread->start();

QMetaObject::invokeMethod(worker, "initialize",
    Qt::QueuedConnection,
    Q_ARG(QString, databasePath));
```

连接在 queued slot 执行时创建，因此天然属于 worker 线程。DTO 通过 queued signal 传回 GUI；注册自定义跨线程元类型。

## 3. 关闭 Worker 连接

连接销毁顺序要明确：

```cpp
void DatabaseWorker::shutdown()
{
    const QString name = m_connectionName;
    {
        QSqlDatabase db = QSqlDatabase::database(name, false);
        db.close();
    }
    QSqlDatabase::removeDatabase(name);
    m_connectionName.clear();
}
```

调用 shutdown 前必须确保该线程内所有 `QSqlQuery` 已结束并销毁。shutdown 也应排队到 worker 线程，完成后再 `thread->quit()` / `wait()`。

不要在线程已经停止后从 GUI 线程取回并关闭它的连接。

## 4. `moveToThread()` 的使用边界

Qt 6.8+：

```cpp
const bool moved = db.moveToThread(targetThread);
```

只有没有 `QSqlQuery` 绑定到连接时才可能成功，且底层 driver 是 QObject，还受 QObject 移动规则约束。

大多数设计更清晰的做法仍是在目标线程创建和打开连接。`moveToThread()` 适合明确的所有权交接，不适合作为连接在线程间来回借用的机制。

## 5. 每线程连接工厂

连接名在整个进程注册表中必须唯一：

```cpp
QString connectionNameForCurrentThread()
{
    return QStringLiteral("db-%1")
        .arg(reinterpret_cast<quintptr>(QThread::currentThreadId()));
}

QSqlDatabase databaseForCurrentThread(const QString &path)
{
    const QString name = connectionNameForCurrentThread();
    if (QSqlDatabase::contains(name))
        return QSqlDatabase::database(name);

    QSqlDatabase db = QSqlDatabase::addDatabase("QSQLITE", name);
    db.setDatabaseName(path);
    if (!db.open())
        throw DatabaseError(db.lastError().text());
    return db;
}
```

线程 ID 可能被系统复用。长期线程池中还应结合应用生成的唯一序号，并在线程结束时移除注册连接。

## 6. 连接池的正确边界

连接池不能简单保存一组 `QSqlDatabase`，让任意线程取用。一个可行池必须保证：

- 连接只借给其归属线程；
- 每个借用者独占连接直到查询/事务结束；
- 超时后返回明确错误；
- 无活动 Query 才能回收或移动；
- 数据库客户端库允许相应并发模型；
- 连接断开后能重建并重新配置 session。

对于固定少量 worker，“每个 worker 一个长期连接”通常比通用连接池更简单可靠。

## 7. GUI Model 与后台查询

`QSqlQueryModel` / `QSqlTableModel` 继承 Item Model。接到 View 后通常位于 GUI 线程，不应从 worker 线程直接调用 `setQuery()`、`select()` 或改数据。

两种路线：

```text
小型本地库：GUI 线程使用 SQL Model，确保查询足够快

大型/远程查询：Worker 线程 QSqlQuery
             → 转成 QList<Dto>
             → queued signal 到 GUI
             → 自定义 ItemModel 应用结果
```

不能把 worker 的活动 `QSqlQuery` 移交给 GUI Model，它仍绑定于原连接和线程。

## 8. Schema migration 的目标

迁移让任意已发布旧版本数据库按确定路径升级到当前 schema：

```text
空数据库 → v1 → v2 → v3
已有 v1 ─────→ v2 → v3
已有 v2 ──────────→ v3
```

每一步需要：唯一版本号、可重复测试的 SQL、事务边界、错误报告和备份/恢复策略。

## 9. SQLite `user_version` 最小迁移器

```cpp
int schemaVersion(QSqlDatabase db)
{
    QSqlQuery query(db);
    if (!query.exec("PRAGMA user_version") || !query.next())
        throw DatabaseError(query.lastError().text());
    return query.value(0).toInt();
}

bool migrateToV2(QSqlDatabase db)
{
    if (!db.transaction())
        return false;

    QSqlQuery query(db);
    const bool ok = query.exec(
        "ALTER TABLE note ADD COLUMN archived INTEGER NOT NULL DEFAULT 0")
        && query.exec("CREATE INDEX idx_note_archived ON note(archived)")
        && query.exec("PRAGMA user_version = 2");

    if (ok && db.commit())
        return true;

    db.rollback();
    return false;
}
```

启动时循环应用 `current + 1` 的迁移，直到目标版本。版本号只能在该步所有改变成功后更新，并与 schema 改变处于同一事务。

### 9.1 并非所有数据库 DDL 都可事务回滚

服务端数据库应使用独立 `schema_migrations` 表及其官方迁移语义。某些 DDL 会隐式提交，必须针对真实数据库测试失败恢复。

### 9.2 不要启动时静默破坏性迁移

删列、重写大表、改变类型可能耗时并丢数据。应先复制/回填、验证，再在后续版本删除旧结构；桌面应用还要处理磁盘不足和中途断电。

## 10. SQLite 连接级配置

常见配置：

```cpp
QSqlQuery query(db);
query.exec("PRAGMA foreign_keys = ON");
query.exec("PRAGMA journal_mode = WAL");
query.exec("PRAGMA busy_timeout = 5000");
```

- 外键检查需要按连接启用并验证结果。
- WAL 改善读写并发，但仍只有一个 writer，且有额外文件与检查点语义。
- busy timeout 让锁暂时冲突时等待，不解决长事务。
- PRAGMA 支持随 SQLite 构建和版本变化，每条都检查返回。

同一文件的每个新连接都要应用所需连接级设置。

### 10.1 内存数据库与多连接

普通 `:memory:` 属于单个连接。创建第二连接会得到另一个空数据库。测试多连接行为应使用临时文件，或明确使用受支持的 SQLite URI 共享内存模式。

## 11. 锁和事务长度

保持写事务短小：

```text
事务前：完成网络请求、用户确认和大计算
事务内：读取必要状态、执行写语句、校验、提交
事务后：发 UI 通知和执行非数据库副作用
```

不要打开事务后等待对话框或网络结果。长事务增加锁冲突，还可能让用户离开时留下难以管理的状态。

数据库提交与发送网络消息无法由普通 SQL 事务原子覆盖。需要 outbox、幂等键或补偿流程，而不是假设两者能同时回滚。

## 12. 乐观并发控制

多人或多线程可能同时编辑同一行。只按 id 更新会静默覆盖：

```sql
UPDATE note
SET title = :title, version = version + 1
WHERE id = :id AND version = :expectedVersion
```

然后检查：

```cpp
if (query.numRowsAffected() == 0)
    return Conflict;
```

冲突后由业务决定刷新、合并或提示用户。时间戳也可作为版本，但整数 revision 通常更清晰。

## 13. 数据库文件和凭据安全

- 数据库路径使用 `QStandardPaths::AppDataLocation`，不要依赖工作目录。
- 文件权限按平台收紧；SQLite 默认不是加密数据库。
- 密码/token 使用系统安全存储，不放在 QSettings 明文中。
- 日志不输出密码、完整连接串和敏感字段。
- 本地加密需要支持的加密数据库构建，并管理密钥生命周期。
- 服务端连接必须配置 TLS 并验证证书，具体选项依赖驱动。

参数绑定防 SQL 注入，不会自动提供磁盘加密、权限控制或敏感字段脱敏。

## 14. 备份与恢复

复制正在写入的 SQLite 主文件不一定构成一致备份，尤其启用 WAL 时。优先使用 SQLite backup API、驱动支持或先建立一致快照。

恢复流程也必须测试：

```text
识别备份版本 → 校验完整性 → 原子替换/导入 → 执行迁移 → 再次校验
```

只有“生成过备份文件”而没有演练恢复，不足以证明可恢复。

## 15. 测试矩阵

### 15.1 每个测试独立数据库

```cpp
QTemporaryDir dir;
const QString path = dir.filePath("test.sqlite");
const QString connection = QUuid::createUuid().toString();
```

测试结束先销毁 Query/句柄，再 removeDatabase。不要共享一个全局测试库，让执行顺序决定结果。

### 15.2 必测行为

- 从空库建立当前 schema；
- 从每个已发布版本逐步迁移；
- 迁移中间失败可恢复；
- 唯一、外键、非空约束；
- 事务提交和回滚；
- 并发更新冲突；
- 锁等待与超时；
- 多线程连接隔离；
- NULL、Unicode、时区、最大整数；
- 驱动缺失和连接断开。

SQLite 单元测试不能证明 PostgreSQL/MySQL 行为。支持哪些生产驱动，就为哪些驱动运行集成测试。

## 16. 监控与诊断

建议记录：

```text
操作名、耗时、影响行数、错误类型、原生错误码、连接角色、迁移版本
```

不要默认记录完整 SQL 和绑定值。SQL 可能暴露结构，绑定值可能含个人信息。

慢查询应在数据库侧结合 EXPLAIN、索引统计和锁等待分析。只在 Qt 层测总耗时无法区分网络、排队、锁和执行计划问题。

## 17. 常见错误

### 17.1 把主线程连接传给 worker

违反连接线程规则。worker 自己创建命名连接。

### 17.2 线程退出后再清连接

连接应在线程仍运行时关闭、移除，再退出线程。

### 17.3 每个任务创建连接却从不 remove

注册表和数据库资源不断增长。要么每 worker 长期复用，要么完整清理。

### 17.4 只测最新 schema

老用户数据库升级路径未被验证。每个已发布版本都应作为迁移起点。

### 17.5 长事务中等待网络

锁被无谓持有，失败边界跨系统且无法原子回滚。

### 17.6 SQLite 开 WAL 就认为可以并行写

WAL 改善读写并发，不会变成多个同时 writer。

## 18. API 与原则速查

| 项目 | 要点 |
|---|---|
| 每线程连接 | 在线程内创建、打开、查询、关闭 |
| `moveToThread()` | Qt 6.8+，无绑定 Query 才可移动 |
| DTO 跨线程 | 传值，不传 Query/连接 |
| connection name | 进程内唯一，并在结束时移除 |
| schema version | 与迁移变更原子提交 |
| SQLite foreign keys | 每连接启用并检查 |
| WAL | 改善读写，不提供多 writer |
| busy timeout | 缓解短暂锁冲突，不替代短事务 |
| 乐观锁 | id + version 条件更新并检查影响行数 |
| 测试 | 每生产驱动执行真实集成测试 |

## 19. 自测题

1. 能否复制 GUI 线程的 QSqlDatabase 给 worker 使用？
2. 为什么优先在目标线程创建连接？
3. moveToThread 在什么情况下会失败？
4. worker 查询结果应以什么形式回 GUI？
5. SQLite user_version 何时更新？
6. foreign_keys PRAGMA 是否只需全应用执行一次？
7. WAL 是否允许多个并行 writer？
8. 为什么事务内不应等待网络？
9. 乐观锁如何发现数据已被别人修改？
10. 为什么 SQLite 测试不能证明 PostgreSQL 正确？

## 20. 参考答案

1. 不能；副本仍代表原线程创建的同一连接。
2. 线程归属天然正确，避免移动驱动及活动 Query 的复杂限制。
3. 有 QSqlQuery 绑定，或不满足 QObject 线程移动约束时。
4. 转为不依赖连接的 DTO/值对象，通过 queued signal 传递。
5. 该版本全部 schema 变更成功后，并与其处于同一事务。
6. 不是；它是连接级设置，每个新连接都要配置。
7. 不能，SQLite 仍只有一个 writer。
8. 会延长锁占用，而且数据库事务无法回滚外部网络副作用。
9. UPDATE 同时匹配 id 和预期 version，并检查影响行数是否为 0。
10. 驱动、SQL 方言、事务、类型和并发行为都不同。

## 21. 本篇结论

```text
连接属于创建线程
  → 每个 worker 拥有独立命名连接
  → Query 不跨线程，结果转换为 DTO
  → 迁移按版本、事务和恢复策略执行
  → SQLite 每连接配置，保持短事务
  → 多用户写入用版本字段发现冲突
  → 每种生产数据库运行集成测试
```

数据库工程化的重点不是隐藏 SQL，而是让连接、线程、事务、迁移、并发和恢复边界都能被证明正确。
