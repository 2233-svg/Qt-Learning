# QSqlResult

> Qt 6.11.1 · Qt SQL

## 1. 先建立直觉

**一句话定位：** `QSqlResult` 是 Qt SQL 的“SqlResult”类型，参与数据库连接、SQL 执行、事务或结果模型。

**模块背景：** Qt SQL 提供数据库连接、查询、事务和 SQL 模型/视图集成。

### 这是什么

`QSqlResult` 是 Qt SQL 连接、查询与事务机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** Qt SQL 把驱动、连接、查询游标和模型分成不同对象。连接决定驱动和数据库会话，`QSqlQuery` 代表语句及其结果游标，事务把多条语句的提交边界固定下来，SQL 模型再把查询结果接到视图。

**适用场景：** 创建连接并检查 open，使用 prepare/bindValue 分离 SQL 结构和用户数据，执行后检查返回值和 lastError，遍历结果，必要时用 transaction/commit/rollback 包住一组操作。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要拼接用户输入形成 SQL；不要把 exec 成功当作有数据；不要在连接仍被引用时 removeDatabase；不要忽略驱动是否可用、字段类型转换和事务失败回滚。

## 2. 依赖与对象关系

- 头文件：`#include <QSqlResult>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Sql)
target_link_libraries(mytarget PRIVATE Qt6::Sql)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

Qt SQL 把驱动、连接、查询游标和模型分成不同对象。连接决定驱动和数据库会话，`QSqlQuery` 代表语句及其结果游标，事务把多条语句的提交边界固定下来，SQL 模型再把查询结果接到视图。

### 状态、生命周期和线程

**生命周期：** 连接由连接名识别，查询和模型引用连接。关闭或移除连接前必须销毁仍引用它的 query、model 和 database 句柄；不同线程不要共用连接。

**状态与结果：** 区分连接是否打开、语句是否执行成功、游标是否定位在有效行、字段是否存在以及事务是否提交成功。`exec()` 成功不代表有结果行，`next()` 成功后才可以安全读取当前行。

**线程与事件循环：** Qt SQL 连接有线程归属，每个线程应建立自己的连接并使用唯一连接名；不要把一个线程创建的 QSqlDatabase 或 QSqlQuery 传到另一个线程继续使用。

## 3. 直接使用

创建连接并检查 open，使用 prepare/bindValue 分离 SQL 结构和用户数据，执行后检查返回值和 lastError，遍历结果，必要时用 transaction/commit/rollback 包住一组操作。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

```cpp
QSqlQuery query(database);
query.prepare(QStringLiteral("SELECT name FROM users WHERE id = :id"));
query.bindValue(QStringLiteral(":id"), id);
if (query.exec()) {
    while (query.next()) {
        const QVariant value = query.value(0);
    }
}
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `virtual ~QSqlResult()`
- `virtual QVariant handle() const`

### 保护函数

- `QSqlResult(const QSqlDriver *db)`
- `void addBindValue(const QVariant &val, QSql::ParamType paramType)`
- `int at() const`
- `virtual void bindValue(int index, const QVariant &val, QSql::ParamType paramType)`
- `virtual void bindValue(const QString &placeholder, const QVariant &val, QSql::ParamType paramType)`
- `QSql::ParamType bindValueType(int index) const`
- `QSql::ParamType bindValueType(const QString &placeholder) const`
- `QSqlResult::BindingSyntax bindingSyntax() const`
- `QVariant boundValue(int index) const`
- `QVariant boundValue(const QString &placeholder) const`
- `int boundValueCount() const`
- `QString boundValueName(int index) const`
- `QStringList boundValueNames() const`
- `QVariantList boundValues() const`
- `QVariantList & boundValues()`
- `void clear()`
- `virtual QVariant data(int index) = 0`
- `const QSqlDriver * driver() const`
- `virtual bool exec()`
- `QString executedQuery() const`
- `virtual bool fetch(int index) = 0`
- `virtual bool fetchFirst() = 0`
- `virtual bool fetchLast() = 0`
- `virtual bool fetchNext()`
- `virtual bool fetchPrevious()`
- `bool hasOutValues() const`
- `bool isActive() const`
- `bool isForwardOnly() const`
- `virtual bool isNull(int index) = 0`
- `bool isSelect() const`
- `bool isValid() const`
- `QSqlError lastError() const`
- `virtual QVariant lastInsertId() const`
- `QString lastQuery() const`
- `virtual int numRowsAffected() = 0`
- `virtual bool prepare(const QString &query)`
- `virtual QSqlRecord record() const`
- `virtual bool reset(const QString &query) = 0`
- `void resetBindCount()`
- `virtual bool savePrepare(const QString &query)`
- `virtual void setActive(bool active)`
- `virtual void setAt(int index)`
- `virtual void setForwardOnly(bool forward)`
- `virtual void setLastError(const QSqlError &error)`
- `virtual void setQuery(const QString &query)`
- `virtual void setSelect(bool select)`
- `virtual int size() = 0`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QSqlResult::BindingSyntax`

**作用与语义：**

该枚举类型指定了预备查询中用于占位符的不同语法。
- `QSqlResult::PositionalBinding`：`0`;使用ODBC风格的定位语法，占位符为“？”。
- `QSqlResult::NamedBinding`：`1`;使用带有命名占位符的 Oracle 风格语法（例如 “：id”）

### `[explicit protected] QSqlResult::QSqlResult(const QSqlDriver *db)`

**作用与语义：**

使用数据库驱动`db`创建QSqlResult。该对象被初始化为非活跃状态。

### `[virtual noexcept] QSqlResult::~QSqlResult()`

**作用与语义：**

摧毁该物体并释放所有分配的资源。

### `[protected] void QSqlResult::addBindValue(const QVariant &val, QSql::ParamType paramType)`

**作用与语义：**

将参数类型为`paramType`的值`val`绑定到当前记录（行）中下一个可用位置。

### `[protected] int QSqlResult::at() const`

**作用与语义：**

返回结果当前（基于零的）行位置。可能返回特殊值 `QSql::BeforeFirstRow` 或 `QSql::AfterLastRow`。

### `[virtual protected] void QSqlResult::bindValue(int index, const QVariant &val, QSql::ParamType paramType)`

**作用与语义：**

将参数类型`paramType`的值`val`绑定到当前记录（行）中的位置`index`。

### `[virtual protected] void QSqlResult::bindValue(const QString &placeholder, const QVariant &val, QSql::ParamType paramType)`

**作用与语义：**

将参数类型为`paramType`的值`val`绑定到当前记录（行）中的`placeholder`名称。
注意：绑定未定义的占位符会导致行为未定义。

### `[protected] QSql::ParamType QSqlResult::bindValueType(int index) const`

**作用与语义：**

返回位置`index`的值边界参数类型。

### `[protected] QSql::ParamType QSqlResult::bindValueType(const QString &placeholder) const`

**作用与语义：**

返回与给定`placeholder`名称绑定的值的参数类型。

### `[protected] QSqlResult::BindingSyntax QSqlResult::bindingSyntax() const`

**作用与语义：**

返回预备查询所使用的绑定语法。

### `[protected] QVariant QSqlResult::boundValue(int index) const`

**作用与语义：**

返回当前记录（行）中位置`index`的值界定。

### `[protected] QVariant QSqlResult::boundValue(const QString &placeholder) const`

**作用与语义：**

返回当前记录（行）中由给定`placeholder`名称所界定的值。

### `[protected] int QSqlResult::boundValueCount() const`

**作用与语义：**

返回结果中被绑定值的数量。

### `[protected] QString QSqlResult::boundValueName(int index) const`

**作用与语义：**

返回当前记录（行）中位置`index`的绑定值名称。

### `[protected] QStringList QSqlResult::boundValueNames() const`

**作用与语义：**

返回所有绑定值的名称。

### `[protected] QVariantList QSqlResult::boundValues() const`

**作用与语义：**

返回当前记录（行）结果的绑定值列表。

### `[protected] QVariantList &QSqlResult::boundValues()`

**作用与语义：**

返回对当前记录（行）结果绑定值列表的可变引用。

### `[protected] void QSqlResult::clear()`

**作用与语义：**

清除整个结果集并释放所有相关资源。

### `[pure virtual protected] QVariant QSqlResult::data(int index)`

**作用与语义：**

返回当前行字段`index`的数据作为`QVariant`。该函数仅在结果处于活跃状态且位于有效记录上且`index`非负时调用。派生类必须重新实现该函数，返回字段`index`值，若无法确定则返回QVariant()。

### `[protected] const QSqlDriver *QSqlResult::driver() const`

**作用与语义：**

返回与结果相关的驱动程序。这是传递给构造函数的对象。

### `[virtual protected] bool QSqlResult::exec()`

**作用与语义：**

执行查询，成功时返回true;否则返回false。

### `[protected] QString QSqlResult::executedQuery() const`

**作用与语义：**

返回实际执行的查询。这可能与传递的查询不同，例如如果绑定值用于预备查询，而底层数据库不支持预备查询。

### `[pure virtual protected] bool QSqlResult::fetch(int index)`

**作用与语义：**

将结果定位到任意（基于零的）行 `index`。
只有当结果处于活动状态时才调用该函数。派生类必须重新实现该函数并将结果定位到行 `index`，并以合适的值调用 `setAt()`。返回 true 表示成功，false 表示失败。

### `[pure virtual protected] bool QSqlResult::fetchFirst()`

**作用与语义：**

将结果定位到结果的第一条记录（第0行）。
只有当结果处于活动状态时才调用该函数。派生类必须重新实现该函数并将结果定位到第一个记录，并以合适的值调用`setAt()`。返回true表示成功，false表示失败。

### `[pure virtual protected] bool QSqlResult::fetchLast()`

**作用与语义：**

将结果定位到结果的最后一行记录。
只有当结果处于活动状态时才调用该函数。派生类必须重新实现该函数并将结果定位到最后一条记录，并以适当的值调用`setAt()`。返回true表示成功，false表示失败。

### `[virtual protected] bool QSqlResult::fetchNext()`

**作用与语义：**

将结果定位到结果中下一个可用的记录（行）。
只有当结果处于活动状态时，才调用该函数。默认实现调用`fetch()`下一个索引。派生类可以重新实现该函数，并以其他方式将结果定位到下一条记录，并以合适的值调用`setAt()`。返回 true 表示成功，false 表示失败。

### `[virtual protected] bool QSqlResult::fetchPrevious()`

**作用与语义：**

将结果定位到结果中之前的记录（行）。
该函数仅在结果处于活跃状态时被调用。默认实现调用`fetch()`前一个索引。派生类可以重新实现该函数，并以其他方式将结果定位到下一条记录，并以适当的值调用`setAt()`。返回true表示成功，false表示失败。

### `[virtual] QVariant QSqlResult::handle() const`

**作用与语义：**

返回该结果集的底层数据库句柄，包裹在`QVariant`中;如果没有句柄，则返回无效`QVariant`。
警告：使用时请极度谨慎，且仅在你知道自己在做什么的情况下使用。
警告：如果结果被修改（例如清除它），这里返回的句柄可能会变成过时指针。
警告：如果结果尚未执行，句柄可能为NULL。
警告：PostgreSQL：在仅转发模式下，调用 `fetch()`、`fetchFirst()`、`fetchLast()`、`fetchNext()`、`fetchPrevious()`、nextResult() 后，`QSqlResult` 的句柄可能会发生变化。
这里返回的句柄是数据库相关的，访问前应查询变体的类型名。
本示例检索了 sqlite 结果的句柄：
此摘要返回PostgreSQL或MySQL的句柄：

**官方示例：**

```cpp
 QSqlDatabase db = QSqlDatabase::database("sales");
 QSqlQuery query("SELECT NAME, DOB FROM EMPLOYEES", db);

 QVariant v = query.result()->handle();
 if (v.isValid() && qstrcmp(v.typeName(), "sqlite3_stmt*") == 0) {
     // v.data() returns a pointer to the handle
     sqlite3_stmt *handle = *static_cast<sqlite3_stmt **>(v.data());
     if (handle) {
         // ...
     }
 }
```

### `[protected] bool QSqlResult::hasOutValues() const`

**作用与语义：**

如果查询的绑定值中至少有一个是`QSql::Out`或`QSql::InOut`，则返回`true`;否则返回`false`。

### `[protected] bool QSqlResult::isActive() const`

**作用与语义：**

如果结果有需要检索的记录，返回`true`;否则返回`false`。

### `[protected] bool QSqlResult::isForwardOnly() const`

**作用与语义：**

如果只能向前滚动结果集，返回`true`;否则返回`false`。

### `[pure virtual protected] bool QSqlResult::isNull(int index)`

**作用与语义：**

如果当前行中位置`index`的字段为空，返回`true`;否则返回`false`。

### `[protected] bool QSqlResult::isSelect() const`

**作用与语义：**

如果当前结果来自`SELECT`语句，返回`true`;否则返回`false`。

### `[protected] bool QSqlResult::isValid() const`

**作用与语义：**

如果结果位于有效记录上（即结果不在第一条记录之前或之后），返回`true`;否则返回`false`。

### `[protected] QSqlError QSqlResult::lastError() const`

**作用与语义：**

返回与结果相关的最后一个错误。

### `[virtual protected] QVariant QSqlResult::lastInsertId() const`

**作用与语义：**

如果数据库支持，则返回最近插入行的对象ID。如果查询未插入任何值或数据库未返回ID，则返回无效`QVariant`。如果插入触及了多行，行为未定义。
注意，对于 Oracle 数据库，行的 ROWID 会返回，而对于 MySQL 数据库，行的自动递增字段会返回。

### `[protected] QString QSqlResult::lastQuery() const`

**作用与语义：**

返回当前的SQL查询文本，或者如果没有空字符串则返回。

### `[pure virtual protected] int QSqlResult::numRowsAffected()`

**作用与语义：**

返回上次执行查询影响的行数，若无法确定或查询为`SELECT`语句，则返回-1行。

### `[virtual protected] bool QSqlResult::prepare(const QString &query)`

**作用与语义：**

准备给定的`query`以供执行;查询通常会使用占位符，以便反复执行。如果查询成功准备，返回真;否则返回`false`。

### `[virtual protected] QSqlRecord QSqlResult::record() const`

**作用与语义：**

如果查询处于活动状态，返回当前记录；否则返回空的 `QSqlRecord`。
默认实现总是返回空的 `QSqlRecord`。

### `[pure virtual protected] bool QSqlResult::reset(const QString &query)`

**作用与语义：**

设置结果后用SQL语句`query`进行后续数据检索。
派生类必须重新实现该函数并将`query`应用到数据库中。该函数仅在结果被设置为非活跃状态且位于新结果第一条记录之前后调用。如果查询成功且准备使用，派生类应返回true，否则返回false。

### `[protected] void QSqlResult::resetBindCount()`

**作用与语义：**

重置绑定参数的数量。

### `[virtual protected] bool QSqlResult::savePrepare(const QString &query)`

**作用与语义：**

准备给定的`query`，尽可能利用底层数据库功能。如果查询成功准备，返回`true`;否则返回`false`。
注意：该方法应称为“safePrepare()”。

### `[virtual protected] void QSqlResult::setActive(bool active)`

**作用与语义：**

该函数用于派生类将内部激活状态设置为`active`。

### `[virtual protected] void QSqlResult::setAt(int index)`

**作用与语义：**

该函数用于派生类将内部（零为基础）行位置设置为`index`。

### `[virtual protected] void QSqlResult::setForwardOnly(bool forward)`

**作用与语义：**

将仅前进模式设置为`forward`。如果`forward`为真，则仅允许`fetchNext()`用于搜索结果。仅前进模式所需的内存大大减少，因为无需缓存结果。默认情况下，此功能被禁用。
将只转发设置为假是向数据库引擎的建议，数据库引擎拥有最终决定结果集是仅转发还是可滚动的。`isForwardOnly()`总是返回结果集的正确状态。
注意：查询执行后调用 setForwardOnly 充其量会导致意外结果，最坏情况下会崩溃。
注意：为了确保仅转发查询成功完成，应用程序不仅应在执行查询后检查`lastError()`错误，也应在浏览查询结果后进行检查。
警告：PostgreSQL：在仅前向模式下浏览查询结果时，请不要在同一数据库连接上执行任何其他SQL命令。否则查询结果会丢失。

### `[virtual protected] void QSqlResult::setLastError(const QSqlError &error)`

**作用与语义：**

该函数用于派生类将最后错误设为`error`。

### `[virtual protected] void QSqlResult::setQuery(const QString &query)`

**作用与语义：**

将当前查询设置为`query`。您必须调用`reset()`才能在数据库中执行查询。

### `[virtual protected] void QSqlResult::setSelect(bool select)`

**作用与语义：**

该函数用于导出类，用以指示当前语句是否为 SQL `SELECT`语句。如果语句是 `SELECT` 语句，`select` 参数应为真;否则应为假。

### `[pure virtual protected] int QSqlResult::size()`

**作用与语义：**

返回`SELECT`结果的大小，如果无法确定或查询不是`SELECT`语句，则返回-1。

## 6. 深入实践与常见坑

### 生命周期和资源边界

连接由连接名识别，查询和模型引用连接。关闭或移除连接前必须销毁仍引用它的 query、model 和 database 句柄；不同线程不要共用连接。

### 状态和错误边界

区分连接是否打开、语句是否执行成功、游标是否定位在有效行、字段是否存在以及事务是否提交成功。`exec()` 成功不代表有结果行，`next()` 成功后才可以安全读取当前行。

### 线程边界

Qt SQL 连接有线程归属，每个线程应建立自己的连接并使用唯一连接名；不要把一个线程创建的 QSqlDatabase 或 QSqlQuery 传到另一个线程继续使用。

### 最容易出现的错误

不要拼接用户输入形成 SQL；不要把 exec 成功当作有数据；不要在连接仍被引用时 removeDatabase；不要忽略驱动是否可用、字段类型转换和事务失败回滚。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QSqlResult` 所属机制类型：Qt SQL 连接、查询与事务机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
