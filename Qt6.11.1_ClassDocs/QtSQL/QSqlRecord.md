# QSqlRecord

> Qt 6.11.1 · Qt SQL

## 1. 先建立直觉

**一句话定位：** `QSqlRecord` 是 Qt SQL 的“Sql记录”类型，参与数据库连接、SQL 执行、事务或结果模型。

**模块背景：** Qt SQL 提供数据库连接、查询、事务和 SQL 模型/视图集成。

### 这是什么

`QSqlRecord` 是 Qt SQL 连接、查询与事务机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** Qt SQL 把驱动、连接、查询游标和模型分成不同对象。连接决定驱动和数据库会话，`QSqlQuery` 代表语句及其结果游标，事务把多条语句的提交边界固定下来，SQL 模型再把查询结果接到视图。

**适用场景：** 创建连接并检查 open，使用 prepare/bindValue 分离 SQL 结构和用户数据，执行后检查返回值和 lastError，遍历结果，必要时用 transaction/commit/rollback 包住一组操作。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要拼接用户输入形成 SQL；不要把 exec 成功当作有数据；不要在连接仍被引用时 removeDatabase；不要忽略驱动是否可用、字段类型转换和事务失败回滚。

## 2. 依赖与对象关系

- 头文件：`#include <QSqlRecord>`
- 继承自：未在类页中列出
- 直接派生类：QSqlIndex

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

- `QSqlRecord()`
- `QSqlRecord(const QSqlRecord &other)`
- `(since 6.6) QSqlRecord(QSqlRecord &&other)`
- `~QSqlRecord()`
- `void append(const QSqlField &field)`
- `void clear()`
- `void clearValues()`
- `bool contains(QAnyStringView name) const`
- `int count() const`
- `QSqlField field(int index) const`
- `QSqlField field(QAnyStringView name) const`
- `QString fieldName(int index) const`
- `int indexOf(QAnyStringView name) const`
- `void insert(int pos, const QSqlField &field)`
- `bool isEmpty() const`
- `bool isGenerated(int index) const`
- `bool isGenerated(QAnyStringView name) const`
- `bool isNull(int index) const`
- `bool isNull(QAnyStringView name) const`
- `QSqlRecord keyValues(const QSqlRecord &keyFields) const`
- `void remove(int pos)`
- `void replace(int pos, const QSqlField &field)`
- `void setGenerated(QAnyStringView name, bool generated)`
- `void setGenerated(int index, bool generated)`
- `void setNull(int index)`
- `void setNull(QAnyStringView name)`
- `void setValue(int index, const QVariant &val)`
- `void setValue(QAnyStringView name, const QVariant &val)`
- `(since 6.6) void swap(QSqlRecord &other)`
- `QVariant value(int index) const`
- `QVariant value(QAnyStringView name) const`
- `bool operator!=(const QSqlRecord &other) const`
- `(since 6.6) QSqlRecord & operator=(QSqlRecord &&other)`
- `QSqlRecord & operator=(const QSqlRecord &other)`
- `bool operator==(const QSqlRecord &other) const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QSqlRecord::QSqlRecord()`

**作用与语义：**

构建一个空白记录。

### `QSqlRecord::QSqlRecord(const QSqlRecord &other)`

**作用与语义：**

构建了一份`other`的复制品。
QSqlRecord 是隐式共享的。这意味着你可以在常数时间内复制记录。

### `[constexpr noexcept, since 6.6] QSqlRecord::QSqlRecord(QSqlRecord &&other)`

**作用与语义：**

从`other`移动构建新的QSqlRecord。
注意：移出对象 `other` 处于部分成形状态，唯一有效的操作是销毁和赋值。

### `[noexcept] QSqlRecord::~QSqlRecord()`

**作用与语义：**

摧毁该物体并释放所有分配的资源。

### `void QSqlRecord::append(const QSqlField &field)`

**作用与语义：**

请在记录末尾附上字段`field`副本。

### `void QSqlRecord::clear()`

**作用与语义：**

移除记录中的所有字段。

### `void QSqlRecord::clearValues()`

**作用与语义：**

清除记录中所有字段的值，并将每个字段设为空。

### `bool QSqlRecord::contains(QAnyStringView name) const`

**作用与语义：**

如果记录中存在称为`name`的字段，返回`true`;否则返回`false`。
注意：在6.8之前的Qt版本中，该功能采用了`QString`，而非取`QAnyStringView`。

### `int QSqlRecord::count() const`

**作用与语义：**

返回记录中的字段数量。

### `QSqlField QSqlRecord::field(int index) const`

**作用与语义：**

返回位置`index`的字段。如果`index`超出范围，函数返回默认构造值。

### `QSqlField QSqlRecord::field(QAnyStringView name) const`

**作用与语义：**

返回名为 `name` 的字段。如果找不到称为 `name` 的字段，函数返回一个默认构造的值。
注意：在6.8之前的Qt版本中，该功能采用`QString`，而非取`QAnyStringView`。

### `QString QSqlRecord::fieldName(int index) const`

**作用与语义：**

返回位置`index`的字段名称。如果字段不存在，则返回空字符串。

### `int QSqlRecord::indexOf(QAnyStringView name) const`

**作用与语义：**

返回记录中称为`name`的字段的位置，若找不到则返回-1。字段名称不区分大小写。如果多个字段匹配，返回第一个字段。
注意：在6.8之前的Qt版本中，该函数采用`QString`，而非`QAnyStringView`。

### `void QSqlRecord::insert(int pos, const QSqlField &field)`

**作用与语义：**

将字段`field`插入记录中位置`pos`。

### `bool QSqlRecord::isEmpty() const`

**作用与语义：**

如果记录中没有字段，返回`true`;否则返回`false`。

### `bool QSqlRecord::isGenerated(int index) const`

**作用与语义：**

如果记录在位置`index`有字段并且需要生成该字段（默认），返回`true`;否则返回`false`。

### `bool QSqlRecord::isGenerated(QAnyStringView name) const`

**作用与语义：**

如果记录中有名为`name`的字段且需要生成该字段（默认），返回`true`;否则返回`false`。
注意：在6.8之前的Qt版本中，该功能采用了`QString`，而非`QAnyStringView`。

### `bool QSqlRecord::isNull(int index) const`

**作用与语义：**

如果场`index`为空或位置`index`无场，返回`true`;否则返回`false`。

### `bool QSqlRecord::isNull(QAnyStringView name) const`

**作用与语义：**

如果称为`name`的字段为空或不存在称为`name`的字段，返回`true`;否则返回`false`。
注意：在6.8之前的Qt版本中，这个功能是`QString`的，而不是`QAnyStringView`。

### `QSqlRecord QSqlRecord::keyValues(const QSqlRecord &keyFields) const`

**作用与语义：**

返回包含`keyFields`字段的记录，设置为字段名称匹配的值。

### `void QSqlRecord::remove(int pos)`

**作用与语义：**

移除位置`pos`的场。如果`pos`超出范围，什么都不会发生。

### `void QSqlRecord::replace(int pos, const QSqlField &field)`

**作用与语义：**

将位置`pos`的场替换为给定的`field`。如果`pos`超出范围，则不会发生任何事。

### `void QSqlRecord::setGenerated(QAnyStringView name, bool generated)`

**作用与语义：**

将称为 `name` 的字段生成的标志设置为 `generated`。如果字段不存在，则不会发生任何事。例如，只有将 `generated` 设置为 true（true）的字段才会被包含在 `QSqlQueryModel` 生成的 SQL 中。
注意：在6.8之前的Qt版本中，该函数采用`QString`，而非取`QAnyStringView`。

### `void QSqlRecord::setGenerated(int index, bool generated)`

**作用与语义：**

将字段`index`生成的标志设置为`generated`。

### `void QSqlRecord::setNull(int index)`

**作用与语义：**

将场`index`的值设为空。如果场不存在，则不会发生任何事。

### `void QSqlRecord::setNull(QAnyStringView name)`

**作用与语义：**

将称为 `name` 的字段值设置为空值。如果字段不存在，则不会发生任何事。
注意：在6.8之前的Qt版本中，该功能采用了`QString`，而非`QAnyStringView`。

### `void QSqlRecord::setValue(int index, const QVariant &val)`

**作用与语义：**

将位置`index`的场值设为`val`。如果场不存在，则不会发生任何事。

### `void QSqlRecord::setValue(QAnyStringView name, const QVariant &val)`

**作用与语义：**

将称为`name`的场的值设为`val`。如果该场不存在，则不会发生任何事。
注意：在6.8之前的Qt版本中，该函数采用`QString`，而非取`QAnyStringView`。

### `[noexcept, since 6.6] void QSqlRecord::swap(QSqlRecord &other)`

**作用与语义：**

将该SQL记录与`other`交换。此操作非常快速且从未失败。

### `QVariant QSqlRecord::value(int index) const`

**作用与语义：**

返回记录中位置`index`的字段值。如果`index`超出边界，则返回无效`QVariant`。

### `QVariant QSqlRecord::value(QAnyStringView name) const`

**作用与语义：**

返回记录中称为 `name` 的字段值。如果字段 `name` 不存在，则返回无效变体。注意：在 6.8 之前的 Qt 版本中，该函数取用 `QString`，而非 `QAnyStringView`。

### `bool QSqlRecord::operator!=(const QSqlRecord &other) const`

**作用与语义：**

如果该对象与`other`不相同，返回`true`;否则返回`false`。

### `[noexcept, since 6.6] QSqlRecord &QSqlRecord::operator=(QSqlRecord &&other)`

**作用与语义：**

Move-assign `other` 到该`QSqlRecord`实例。
注意：移出对象 `other` 处于部分成形状态，唯一有效的操作是销毁和赋值。

### `QSqlRecord &QSqlRecord::operator=(const QSqlRecord &other)`

**作用与语义：**

将纪录定为`other`。
`QSqlRecord`是隐式共享的。这意味着你可以在恒定时间内复制记录。

### `bool QSqlRecord::operator==(const QSqlRecord &other) const`

**作用与语义：**

如果该对象与`other`相同（即字段相同且顺序相同），返回 `true`;否则返回 `false`。

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

`QSqlRecord` 所属机制类型：Qt SQL 连接、查询与事务机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
