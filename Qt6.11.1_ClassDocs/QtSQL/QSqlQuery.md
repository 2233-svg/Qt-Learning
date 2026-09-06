# QSqlQuery

> Qt 6.11.1 · Qt SQL

## 1. 先建立直觉

**一句话定位：** `QSqlQuery` 执行 SQL 语句、绑定参数、遍历结果并提供错误信息，是 Qt SQL 的直接查询接口。

**模块背景：** Qt SQL 提供数据库连接、查询、事务和 SQL 模型/视图集成。

### 这是什么

`QSqlQuery` 执行 SQL 语句、绑定参数、遍历结果并提供错误信息，是 Qt SQL 的直接查询接口。

**内部模型：** 一次 QSqlQuery 对应一次语句执行和结果游标；exec 后通过 next/first/last 移动游标，再通过 value 读取列。prepare/bindValue 能把数据和 SQL 结构分开。

**适用场景：** 需要精确 SQL、事务控制、批量操作或不适合直接用模型时使用。只查询表格展示时可考虑 QSqlQueryModel。

**典型调用链：** 构造 query(database) -> prepare -> bindValue -> exec -> next -> value -> lastError -> 结束时释放。

**先记住的坑：** 不要拼接用户输入形成 SQL；exec 成功不代表结果有行；列名和索引要核对；长事务会锁表或阻塞其他请求。

## 2. 依赖与对象关系

- 头文件：`#include <QSqlQuery>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Sql)
target_link_libraries(mytarget PRIVATE Qt6::Sql)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

一次 QSqlQuery 对应一次语句执行和结果游标；exec 后通过 next/first/last 移动游标，再通过 value 读取列。prepare/bindValue 能把数据和 SQL 结构分开。

### 状态、生命周期和线程

**生命周期：** 连接由连接名识别，查询和模型引用连接。关闭或移除连接前必须销毁仍引用它的 query、model 和 database 句柄；不同线程不要共用连接。

**状态与结果：** 区分连接是否打开、语句是否执行成功、游标是否定位在有效行、字段是否存在以及事务是否提交成功。`exec()` 成功不代表有结果行，`next()` 成功后才可以安全读取当前行。

**线程与事件循环：** Qt SQL 连接有线程归属，每个线程应建立自己的连接并使用唯一连接名；不要把一个线程创建的 QSqlDatabase 或 QSqlQuery 传到另一个线程继续使用。

## 3. 直接使用

需要精确 SQL、事务控制、批量操作或不适合直接用模型时使用。只查询表格展示时可考虑 QSqlQueryModel。 使用时通常按这个过程组织：构造 query(database) -> prepare -> bindValue -> exec -> next -> value -> lastError -> 结束时释放。

```cpp
#include <QSqlQuery>

QSqlQuery query;
query.prepare(QStringLiteral("SELECT name FROM users WHERE id = :id"));
query.bindValue(QStringLiteral(":id"), userId);
if (query.exec() && query.next())
    const QString name = query.value(0).toString();
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum BatchExecutionMode { ValuesAsRows, ValuesAsColumns }`

### 属性

- `(since 6.8) forwardOnly : bool`
- `(since 6.8) numericalPrecisionPolicy : QSql::NumericalPrecisionPolicy`
- `(since 6.8) positionalBindingEnabled : bool`

### 公有函数

- `QSqlQuery(QSqlResult *result)`
- `QSqlQuery(const QSqlDatabase &db)`
- `QSqlQuery(const QString &query = QString(), const QSqlDatabase &db = QSqlDatabase())`
- `(since 6.2) QSqlQuery(QSqlQuery &&other)`
- `~QSqlQuery()`
- `void addBindValue(const QVariant &val, QSql::ParamType paramType = QSql::In)`
- `int at() const`
- `void bindValue(const QString &placeholder, const QVariant &val, QSql::ParamType paramType = QSql::In)`
- `void bindValue(int pos, const QVariant &val, QSql::ParamType paramType = QSql::In)`
- `QVariant boundValue(const QString &placeholder) const`
- `QVariant boundValue(int pos) const`
- `(since 6.6) QString boundValueName(int pos) const`
- `(since 6.6) QStringList boundValueNames() const`
- `(since 6.0) QVariantList boundValues() const`
- `void clear()`
- `const QSqlDriver * driver() const`
- `bool exec()`
- `bool exec(const QString &query)`
- `bool execBatch(QSqlQuery::BatchExecutionMode mode = ValuesAsRows)`
- `QString executedQuery() const`
- `void finish()`
- `bool first()`
- `bool isActive() const`
- `bool isForwardOnly() const`
- `bool isNull(int field) const`
- `bool isNull(QAnyStringView name) const`
- `(since 6.7) bool isPositionalBindingEnabled() const`
- `bool isSelect() const`
- `bool isValid() const`
- `bool last()`
- `QSqlError lastError() const`
- `QVariant lastInsertId() const`
- `QString lastQuery() const`
- `bool next()`
- `bool nextResult()`
- `int numRowsAffected() const`
- `QSql::NumericalPrecisionPolicy numericalPrecisionPolicy() const`
- `bool prepare(const QString &query)`
- `bool previous()`
- `QSqlRecord record() const`
- `const QSqlResult * result() const`
- `bool seek(int index, bool relative = false)`
- `void setForwardOnly(bool forward)`
- `void setNumericalPrecisionPolicy(QSql::NumericalPrecisionPolicy precisionPolicy)`
- `(since 6.7) void setPositionalBindingEnabled(bool enable)`
- `int size() const`
- `(since 6.2) void swap(QSqlQuery &other)`
- `QVariant value(int index) const`
- `QVariant value(QAnyStringView name) const`
- `(since 6.2) QSqlQuery & operator=(QSqlQuery &&other)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 54 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `[since 6.8] forwardOnly : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QSqlQuery` 的配置属性。初始化或状态切换时通过 `setForwardOnly(...)` 设置，之后用 `forwardOnly()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`forwardOnly`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.8] numericalPrecisionPolicy : QSql::NumericalPrecisionPolicy`

**API 类别：** 属性说明

**中文解读：** 这是 `QSqlQuery` 的配置属性。初始化或状态切换时通过 `setNumericalPrecisionPolicy(...)` 设置，之后用 `NumericalPrecisionPolicy()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QSql::NumericalPrecisionPolicy`。
- 属性名：`numericalPrecisionPolicy`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.8] positionalBindingEnabled : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QSqlQuery` 的配置属性。初始化或状态切换时通过 `setPositionalBindingEnabled(...)` 设置，之后用 `positionalBindingEnabled()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`positionalBindingEnabled`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QSqlQuery::QSqlQuery(QSqlResult *result)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSqlQuery` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `result`：类型为 `QSqlResult *`。没有默认值，调用时必须提供。传入 `QSqlResult *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QSqlQuery::QSqlQuery(const QSqlDatabase &db)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSqlQuery` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `db`：类型为 `const QSqlDatabase &`。没有默认值，调用时必须提供。传入 `const QSqlDatabase &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QSqlQuery::QSqlQuery(const QString &query = QString(), const QSqlDatabase &db = QSqlDatabase())`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSqlQuery` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `query`：类型为 `const QString &`。默认值为 `QString()`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `db`：类型为 `const QSqlDatabase &`。默认值为 `QSqlDatabase()`。传入 `const QSqlDatabase &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept, since 6.2] QSqlQuery::QSqlQuery(QSqlQuery &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSqlQuery` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `QSqlQuery &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QSqlQuery::~QSqlQuery()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSqlQuery` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSqlQuery::addBindValue(const QVariant &val, QSql::ParamType paramType = QSql::In)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QSqlQuery` 添加依赖、数据或子对象的 API `addBindValue`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `val`：类型为 `const QVariant &`。没有默认值，调用时必须提供。传入 `const QVariant &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `paramType`：类型为 `QSql::ParamType`。默认值为 `QSql::In`。传入 `QSql::ParamType` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QSqlQuery::at() const`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `at`，用于取得 `QSqlQuery` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSqlQuery::bindValue(const QString &placeholder, const QVariant &val, QSql::ParamType paramType = QSql::In)`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `bindValue`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`void`。
- 参数 `placeholder`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `val`：类型为 `const QVariant &`。没有默认值，调用时必须提供。传入 `const QVariant &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `paramType`：类型为 `QSql::ParamType`。默认值为 `QSql::In`。传入 `QSql::ParamType` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSqlQuery::bindValue(int pos, const QVariant &val, QSql::ParamType paramType = QSql::In)`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `bindValue`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`void`。
- 参数 `pos`：类型为 `int`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。
- 参数 `val`：类型为 `const QVariant &`。没有默认值，调用时必须提供。传入 `const QVariant &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `paramType`：类型为 `QSql::ParamType`。默认值为 `QSql::In`。传入 `QSql::ParamType` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVariant QSqlQuery::boundValue(const QString &placeholder) const`

**API 类别：** 成员函数说明

**中文解读：** `QSqlQuery::boundValue` 用于计算、查询或取得与“bound、值访问”相关的操作。调用时要先确认当前状态和 `placeholder` 的有效范围；返回类型是 `QVariant`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVariant`。
- 参数 `placeholder`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVariant QSqlQuery::boundValue(int pos) const`

**API 类别：** 成员函数说明

**中文解读：** `QSqlQuery::boundValue` 用于计算、查询或取得与“bound、值访问”相关的操作。调用时要先确认当前状态和 `pos` 的有效范围；返回类型是 `QVariant`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVariant`。
- 参数 `pos`：类型为 `int`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] QString QSqlQuery::boundValueName(int pos) const`

**API 类别：** 成员函数说明

**中文解读：** `QSqlQuery::boundValueName` 用于计算、查询或取得与“bound、值访问、名称”相关的操作。调用时要先确认当前状态和 `pos` 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数 `pos`：类型为 `int`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] QStringList QSqlQuery::boundValueNames() const`

**API 类别：** 成员函数说明

**中文解读：** `QSqlQuery::boundValueNames` 用于计算、查询或取得与“bound、值访问、Names”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QStringList`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStringList`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] QVariantList QSqlQuery::boundValues() const`

**API 类别：** 成员函数说明

**中文解读：** `QSqlQuery::boundValues` 用于计算、查询或取得与“bound、Values”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QVariantList`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVariantList`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSqlQuery::clear()`

**API 类别：** 成员函数说明

**中文解读：** 这是状态清理或重置 API `clear`。调用后原有数据、索引、缓存或绑定可能失效；使用前先确认它影响的是当前对象、子对象还是底层共享资源，之后重新检查状态。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QSqlDriver *QSqlQuery::driver() const`

**API 类别：** 成员函数说明

**中文解读：** `QSqlQuery::driver` 用于计算、查询或取得与“driver”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QSqlDriver *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QSqlDriver *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QSqlQuery::exec()`

**API 类别：** 成员函数说明

**中文解读：** `QSqlQuery::exec` 用于计算、查询或取得与“执行”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 执行后要结合 `lastError()`、`next()`、事务状态和字段读取判断结果，不能只看 bool。

### `bool QSqlQuery::exec(const QString &query)`

**API 类别：** 成员函数说明

**中文解读：** `QSqlQuery::exec` 用于计算、查询或取得与“执行”相关的操作。调用时要先确认当前状态和 `query` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `query`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 执行后要结合 `lastError()`、`next()`、事务状态和字段读取判断结果，不能只看 bool。

### `bool QSqlQuery::execBatch(QSqlQuery::BatchExecutionMode mode = ValuesAsRows)`

**API 类别：** 成员函数说明

**中文解读：** `QSqlQuery::execBatch` 用于计算、查询或取得与“执行、Batch”相关的操作。调用时要先确认当前状态和 `mode` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `mode`：类型为 `QSqlQuery::BatchExecutionMode`。默认值为 `ValuesAsRows`。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 执行后要结合 `lastError()`、`next()`、事务状态和字段读取判断结果，不能只看 bool。

### `QString QSqlQuery::executedQuery() const`

**API 类别：** 成员函数说明

**中文解读：** `QSqlQuery::executedQuery` 用于计算、查询或取得与“executed、查询”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 执行后要结合 `lastError()`、`next()`、事务状态和字段读取判断结果，不能只看 bool。

### `void QSqlQuery::finish()`

**API 类别：** 成员函数说明

**中文解读：** `QSqlQuery::finish` 用于执行与“finish”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QSqlQuery::first()`

**API 类别：** 成员函数说明

**中文解读：** `QSqlQuery::first` 用于计算、查询或取得与“首项”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QSqlQuery::isActive() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isActive`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QSqlQuery::isForwardOnly() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isForwardOnly`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QSqlQuery::isNull(int field) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isNull`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `field`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QSqlQuery::isNull(QAnyStringView name) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isNull`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `name`：类型为 `QAnyStringView`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.7] bool QSqlQuery::isPositionalBindingEnabled() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isPositionalBindingEnabled`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QSqlQuery::isSelect() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isSelect`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QSqlQuery::isValid() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isValid`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QSqlQuery::last()`

**API 类别：** 成员函数说明

**中文解读：** `QSqlQuery::last` 用于计算、查询或取得与“末项”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSqlError QSqlQuery::lastError() const`

**API 类别：** 成员函数说明

**中文解读：** `QSqlQuery::lastError` 用于计算、查询或取得与“末项、错误”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSqlError`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSqlError`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVariant QSqlQuery::lastInsertId() const`

**API 类别：** 成员函数说明

**中文解读：** `QSqlQuery::lastInsertId` 用于计算、查询或取得与“末项、插入、Id”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QVariant`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVariant`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QSqlQuery::lastQuery() const`

**API 类别：** 成员函数说明

**中文解读：** `QSqlQuery::lastQuery` 用于计算、查询或取得与“末项、查询”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QSqlQuery::next()`

**API 类别：** 成员函数说明

**中文解读：** `QSqlQuery::next` 用于计算、查询或取得与“移动到下一项”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 移动到有效结果行后才能用 `value()` 读取字段；遍历结束后不要继续读取当前行。

### `bool QSqlQuery::nextResult()`

**API 类别：** 成员函数说明

**中文解读：** `QSqlQuery::nextResult` 用于计算、查询或取得与“移动到下一项、结果”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 移动到有效结果行后才能用 `value()` 读取字段；遍历结束后不要继续读取当前行。

### `int QSqlQuery::numRowsAffected() const`

**API 类别：** 成员函数说明

**中文解读：** `QSqlQuery::numRowsAffected` 用于计算、查询或取得与“num、行、Affected”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSql::NumericalPrecisionPolicy QSqlQuery::numericalPrecisionPolicy() const`

**API 类别：** 成员函数说明

**中文解读：** `QSqlQuery::numericalPrecisionPolicy` 用于计算、查询或取得与“numerical、Precision、Policy”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSql::NumericalPrecisionPolicy`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSql::NumericalPrecisionPolicy`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QSqlQuery::prepare(const QString &query)`

**API 类别：** 成员函数说明

**中文解读：** `QSqlQuery::prepare` 用于计算、查询或取得与“prepare”相关的操作。调用时要先确认当前状态和 `query` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `query`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 通常接 `bindValue()` 后再 `exec()`，不要拼接用户输入。

### `bool QSqlQuery::previous()`

**API 类别：** 成员函数说明

**中文解读：** `QSqlQuery::previous` 用于计算、查询或取得与“previous”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSqlRecord QSqlQuery::record() const`

**API 类别：** 成员函数说明

**中文解读：** `QSqlQuery::record` 用于计算、查询或取得与“record”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSqlRecord`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSqlRecord`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QSqlResult *QSqlQuery::result() const`

**API 类别：** 成员函数说明

**中文解读：** `QSqlQuery::result` 用于计算、查询或取得与“结果”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QSqlResult *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QSqlResult *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QSqlQuery::seek(int index, bool relative = false)`

**API 类别：** 成员函数说明

**中文解读：** `QSqlQuery::seek` 用于计算、查询或取得与“定位”相关的操作。调用时要先确认当前状态和 `index`、`relative` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `relative`：类型为 `bool`。默认值为 `false`。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSqlQuery::setForwardOnly(bool forward)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setForwardOnly`。调用它会改变 `QSqlQuery` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `forward`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSqlQuery::setNumericalPrecisionPolicy(QSql::NumericalPrecisionPolicy precisionPolicy)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setNumericalPrecisionPolicy`。调用它会改变 `QSqlQuery` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `precisionPolicy`：类型为 `QSql::NumericalPrecisionPolicy`。没有默认值，调用时必须提供。传入 `QSql::NumericalPrecisionPolicy` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.7] void QSqlQuery::setPositionalBindingEnabled(bool enable)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPositionalBindingEnabled`。调用它会改变 `QSqlQuery` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enable`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QSqlQuery::size() const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `size`，返回 `QSqlQuery` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept, since 6.2] void QSqlQuery::swap(QSqlQuery &other)`

**API 类别：** 成员函数说明

**中文解读：** `QSqlQuery::swap` 用于执行与“swap”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `other`：类型为 `QSqlQuery &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVariant QSqlQuery::value(int index) const`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `value`，用于取得 `QSqlQuery` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`QVariant`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVariant QSqlQuery::value(QAnyStringView name) const`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `value`，用于取得 `QSqlQuery` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`QVariant`。
- 参数 `name`：类型为 `QAnyStringView`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept, since 6.2] QSqlQuery &QSqlQuery::operator=(QSqlQuery &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSqlQuery` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QSqlQuery &`。
- 参数 `other`：类型为 `QSqlQuery &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum BatchExecutionMode { ValuesAsRows, ValuesAsColumns }`

**API 类别：** 公有类型

**中文解读：** 这是 `QSqlQuery` 暴露的类型声明 `Batch、Execution、模式`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

## 6. 深入实践与常见坑

### 生命周期和资源边界

连接由连接名识别，查询和模型引用连接。关闭或移除连接前必须销毁仍引用它的 query、model 和 database 句柄；不同线程不要共用连接。

### 状态和错误边界

区分连接是否打开、语句是否执行成功、游标是否定位在有效行、字段是否存在以及事务是否提交成功。`exec()` 成功不代表有结果行，`next()` 成功后才可以安全读取当前行。

### 线程边界

Qt SQL 连接有线程归属，每个线程应建立自己的连接并使用唯一连接名；不要把一个线程创建的 QSqlDatabase 或 QSqlQuery 传到另一个线程继续使用。

### 最容易出现的错误

不要拼接用户输入形成 SQL；exec 成功不代表结果有行；列名和索引要核对；长事务会锁表或阻塞其他请求。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QSqlQuery` 所属机制类型：Qt SQL 连接、查询与事务机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
