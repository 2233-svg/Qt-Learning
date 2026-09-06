# QSqlField

> Qt 6.11.1 · Qt SQL

## 1. 先建立直觉

**一句话定位：** `QSqlField` 是 Qt SQL 的“SqlField”类型，参与数据库连接、SQL 执行、事务或结果模型。

**模块背景：** Qt SQL 提供数据库连接、查询、事务和 SQL 模型/视图集成。

### 这是什么

`QSqlField` 是 Qt SQL 连接、查询与事务机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** Qt SQL 把驱动、连接、查询游标和模型分成不同对象。连接决定驱动和数据库会话，`QSqlQuery` 代表语句及其结果游标，事务把多条语句的提交边界固定下来，SQL 模型再把查询结果接到视图。

**适用场景：** 创建连接并检查 open，使用 prepare/bindValue 分离 SQL 结构和用户数据，执行后检查返回值和 lastError，遍历结果，必要时用 transaction/commit/rollback 包住一组操作。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要拼接用户输入形成 SQL；不要把 exec 成功当作有数据；不要在连接仍被引用时 removeDatabase；不要忽略驱动是否可用、字段类型转换和事务失败回滚。

## 2. 依赖与对象关系

- 头文件：`#include <QSqlField>`
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

### 公有类型

- `enum RequiredStatus { Required, Optional, Unknown }`

### 属性

- `(since 6.8) autoValue : bool`
- `(since 6.8) defaultValue : QVariant`
- `(since 6.8) generated : bool`
- `(since 6.8) length : int`
- `(since 6.8) metaType : QMetaType`
- `name : QString`
- `(since 6.8) precision : int`
- `(since 6.8) readOnly : bool`
- `(since 6.8) requiredStatus : RequiredStatus`
- `(since 6.8) tableName : QString`
- `(since 6.8) value : QVariant`

### 公有函数

- `(since 6.0) QSqlField(const QString &fieldName = QString(), QMetaType type = QMetaType(), const QString &table = QString())`
- `QSqlField(const QSqlField &other)`
- `~QSqlField()`
- `void clear()`
- `QVariant defaultValue() const`
- `bool isAutoValue() const`
- `bool isGenerated() const`
- `bool isNull() const`
- `bool isReadOnly() const`
- `bool isValid() const`
- `int length() const`
- `QMetaType metaType() const`
- `QString name() const`
- `int precision() const`
- `QSqlField::RequiredStatus requiredStatus() const`
- `void setAutoValue(bool autoVal)`
- `void setDefaultValue(const QVariant &value)`
- `void setGenerated(bool gen)`
- `void setLength(int fieldLength)`
- `void setMetaType(QMetaType type)`
- `void setName(const QString &name)`
- `void setPrecision(int precision)`
- `void setReadOnly(bool readOnly)`
- `void setRequired(bool required)`
- `void setRequiredStatus(QSqlField::RequiredStatus required)`
- `void setTableName(const QString &tableName)`
- `void setValue(const QVariant &value)`
- `(since 6.6) void swap(QSqlField &other)`
- `QString tableName() const`
- `QVariant value() const`
- `bool operator!=(const QSqlField &other) const`
- `QSqlField & operator=(const QSqlField &other)`
- `bool operator==(const QSqlField &other) const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QSqlField::RequiredStatus`

**作用与语义：**

指定该字段是必填还是可选。
- `QSqlField::Required`：`1`;插入记录时必须指定字段。
- `QSqlField::Optional`：`0`;插入记录时无需指定字段。
- `QSqlField::Unknown`：`-1`;数据库驱动程序无法判断该字段是必需的还是可选的。

### `[since 6.8] autoValue : bool`

**作用与语义：**

如果该值由数据库自动生成，例如自动递增主键值，则该值为`true`。
注意：在向数据库写入新记录时，`autoValue`字段只会保存记录提交数据库后产生的新值。使用ODBC驱动时，由于ODBC API的限制，`isAutoValue()`字段仅在执行`SELECT`查询获得的`QSqlRecord`生成的`QSqlField`中填充。它`false`指因`QSqlDatabase::record()`或`QSqlDatabase::primaryIndex()`返回的`QSqlRecord`而产生的`QSqlField`。

**如何使用：** 调用 `autoValue()` 读取当前值；它不会修改应用状态。

### `[since 6.8] defaultValue : QVariant`

**作用与语义：**

该属性表示该字段的默认值。只有部分数据库驱动程序支持该属性。目前支持的有 SQLite、PostgreSQL、Oracle 和 MySQL/MariaDB。

**如何使用：** 调用 `defaultValue()` 读取当前值；它不会修改应用状态。

### `[since 6.8] generated : bool`

**作用与语义：**

该属性表示生成状态。如果`generated` `false`，则该字段不会生成 SQL;否则，Qt 类如 `QSqlQueryModel` 和 `QSqlTableModel` 会为该字段生成 SQL。

**如何使用：** 调用 `generated()` 读取当前值；它不会修改应用状态。

### `[since 6.8] length : int`

**作用与语义：**

该属性表示场的长度。
如果值为负，表示数据库中无法获取该信息。对于字符串，这是字符串能包含的最大字符数;其他类型则含义各异。

**如何使用：** 调用 `length()` 读取当前值；它不会修改应用状态。

### `[since 6.8] metaType : QMetaType`

**作用与语义：**

该属性保存字段在数据库中存储的类型。注意实际值可能有不同的类型，过大无法存储在长整数或双数的数值通常以字符串形式存储，以防止精度损失。

**如何使用：** 调用 `metaType()` 读取当前值；它不会修改应用状态。

### `name : QString`

**作用与语义：**

该属性保存字段名称。它可以是列名或用户提供的别名。

**如何使用：** 调用 `name()` 读取当前值；它不会修改应用状态。

### `[since 6.8] precision : int`

**作用与语义：**

该属性表示场的精度;这仅对数值类型有意义。
如果返回的值为负，说明数据库中无法获得该信息。

**如何使用：** 调用 `precision()` 读取当前值；它不会修改应用状态。

### `[since 6.8] readOnly : bool`

**作用与语义：**

当该属性被`true`时，该`QSqlField`无法被修改。只读字段的值不能设置为`setValue()`，也不能用`clear()`清除为NULL。

**如何使用：** 调用 `readOnly()` 读取当前值；它不会修改应用状态。

### `[since 6.8] requiredStatus : RequiredStatus`

**作用与语义：**

该属性表示字段的 `RequiredStatus`。如果某个必填字段没有取值，`INSERT`将失败。

**如何使用：** 调用 `requiredStatus()` 读取当前值；它不会修改应用状态。

### `[since 6.8] tableName : QString`

**作用与语义：**

该属性包含字段的 tableName。
注意：使用QPSQL驱动时，由于libpq库的限制，`tableName()`字段不会被填充到由前向查询`QSqlQuery::record()`获得的`QSqlRecord`产生的`QSqlField`中。

**如何使用：** 调用 `tableName()` 读取当前值；它不会修改应用状态。

### `[since 6.8] value : QVariant`

**作用与语义：**

该地产将`value`作为`QVariant`。
将`value`设置为只读`QSqlField`是不操作。如果 `value` 的数据类型与字段当前的数据类型不同，会尝试将其转换为正确的类型。这会在赋值时保持字段的数据类型，例如将`QString`到整数数据类型。
要将值设置为NULL，请使用`clear()`。

**如何使用：** 调用 `value()` 读取当前值；它不会修改应用状态。

### `[explicit, since 6.0] QSqlField::QSqlField(const QString &fieldName = QString(), QMetaType type = QMetaType(), const QString &table = QString())`

**作用与语义：**

在`table`中构造一个称为`fieldName`的空域，类型为`type`。

### `QSqlField::QSqlField(const QSqlField &other)`

**作用与语义：**

复制了`other`。

### `[noexcept] QSqlField::~QSqlField()`

**作用与语义：**

摧毁该物体并释放所有分配的资源。

### `void QSqlField::clear()`

**作用与语义：**

清除字段的值并将其设置为NULL。如果字段是只读，则不会发生任何事。

### `QVariant QSqlField::defaultValue() const`

**作用与语义：**

设置 defaultValue 的值。
注意：属性defaultValue使用Getter函数。

### `bool QSqlField::isAutoValue() const`

**作用与语义：**

如果该值由数据库自动生成，例如自动递增主键值，则该值为`true`。
注意：在向数据库写入新记录时，`autoValue`字段只会保存记录提交数据库后产生的新值。使用ODBC驱动时，由于ODBC API的限制，`isAutoValue()`字段仅在执行`SELECT`查询获得的`QSqlRecord`生成的`QSqlField`中填充。它`false`指因`QSqlDatabase::record()`或`QSqlDatabase::primaryIndex()`返回的`QSqlRecord`而产生的`QSqlField`。

**如何使用：** 调用 `isAutoValue()` 读取当前值；它不会修改应用状态。

### `bool QSqlField::isGenerated() const`

**作用与语义：**

该属性表示生成状态。如果`generated` `false`，则该字段不会生成 SQL;否则，Qt 类如 `QSqlQueryModel` 和 `QSqlTableModel` 会为该字段生成 SQL。

**如何使用：** 调用 `isGenerated()` 读取当前值；它不会修改应用状态。

### `bool QSqlField::isNull() const`

**作用与语义：**

如果字段值为NULL，返回`true`;否则返回false。

### `bool QSqlField::isReadOnly() const`

**作用与语义：**

当该属性被`true`时，该`QSqlField`无法被修改。只读字段的值不能设置为`setValue()`，也不能用`clear()`清除为NULL。

**如何使用：** 调用 `isReadOnly()` 读取当前值；它不会修改应用状态。

### `bool QSqlField::isValid() const`

**作用与语义：**

如果字段的变体类型有效，返回`true`;否则返回`false`。

### `int QSqlField::length() const`

**作用与语义：**

返回长度值。
注意：属性长度的获取函数。

### `QMetaType QSqlField::metaType() const`

**作用与语义：**

返回 metaType 的值。
注意：属性metaType的Getter函数。

### `QString QSqlField::name() const`

**作用与语义：**

返回 name 的值。
注意：物业名称的获取函数。

### `int QSqlField::precision() const`

**作用与语义：**

返回精度值。
注意：获取函数以获得属性精度。

### `QSqlField::RequiredStatus QSqlField::requiredStatus() const`

**作用与语义：**

返回 requiredStatus 的值。
注意：property的获取函数为 requiredStatus。

### `void QSqlField::setAutoValue(bool autoVal)`

**作用与语义：**

如果该值由数据库自动生成，例如自动递增主键值，则该值为`true`。
注意：在向数据库写入新记录时，`autoValue`字段只会保存记录提交数据库后产生的新值。使用ODBC驱动时，由于ODBC API的限制，`isAutoValue()`字段仅在执行`SELECT`查询获得的`QSqlRecord`生成的`QSqlField`中填充。它`false`指因`QSqlDatabase::record()`或`QSqlDatabase::primaryIndex()`返回的`QSqlRecord`而产生的`QSqlField`。

**如何使用：** 调用 `setAutoValue(...)` 修改 `autoValue`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QSqlField::setDefaultValue(const QVariant &value)`

**作用与语义：**

该属性表示该字段的默认值。只有部分数据库驱动程序支持该属性。目前支持的有 SQLite、PostgreSQL、Oracle 和 MySQL/MariaDB。

**如何使用：** 调用 `setDefaultValue(...)` 修改 `defaultValue`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QSqlField::setGenerated(bool gen)`

**作用与语义：**

该属性表示生成状态。如果`generated` `false`，则该字段不会生成 SQL;否则，Qt 类如 `QSqlQueryModel` 和 `QSqlTableModel` 会为该字段生成 SQL。

**如何使用：** 调用 `setGenerated(...)` 修改 `generated`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QSqlField::setLength(int fieldLength)`

**作用与语义：**

该属性表示场的长度。
如果值为负，表示数据库中无法获取该信息。对于字符串，这是字符串能包含的最大字符数;其他类型则含义各异。

**如何使用：** 调用 `setLength(...)` 修改 `length`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QSqlField::setMetaType(QMetaType type)`

**作用与语义：**

该属性保存字段在数据库中存储的类型。注意实际值可能有不同的类型，过大无法存储在长整数或双数的数值通常以字符串形式存储，以防止精度损失。

**如何使用：** 调用 `setMetaType(...)` 修改 `metaType`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QSqlField::setName(const QString &name)`

**作用与语义：**

该属性保存字段名称。它可以是列名或用户提供的别名。

**如何使用：** 调用 `setName(...)` 修改 `name`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QSqlField::setPrecision(int precision)`

**作用与语义：**

该属性表示场的精度;这仅对数值类型有意义。
如果返回的值为负，说明数据库中无法获得该信息。

**如何使用：** 调用 `setPrecision(...)` 修改 `precision`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QSqlField::setReadOnly(bool readOnly)`

**作用与语义：**

当该属性被`true`时，该`QSqlField`无法被修改。只读字段的值不能设置为`setValue()`，也不能用`clear()`清除为NULL。

**如何使用：** 调用 `setReadOnly(...)` 修改 `readOnly`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QSqlField::setRequired(bool required)`

**作用与语义：**

如果该项为真，则将该字段的所需状态设置为`Required` `required`;否则将该字段设为`Optional`。

### `void QSqlField::setRequiredStatus(QSqlField::RequiredStatus required)`

**作用与语义：**

该属性表示字段的 `RequiredStatus`。如果某个必填字段没有取值，`INSERT`将失败。

**如何使用：** 调用 `setRequiredStatus(...)` 修改 `requiredStatus`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QSqlField::setTableName(const QString &tableName)`

**作用与语义：**

该属性包含字段的 tableName。
注意：使用QPSQL驱动时，由于libpq库的限制，`tableName()`字段不会被填充到由前向查询`QSqlQuery::record()`获得的`QSqlRecord`产生的`QSqlField`中。

**如何使用：** 调用 `setTableName(...)` 修改 `tableName`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QSqlField::setValue(const QVariant &value)`

**作用与语义：**

该地产将`value`作为`QVariant`。
将`value`设置为只读`QSqlField`是不操作。如果 `value` 的数据类型与字段当前的数据类型不同，会尝试将其转换为正确的类型。这会在赋值时保持字段的数据类型，例如将`QString`到整数数据类型。
要将值设置为NULL，请使用`clear()`。

**如何使用：** 调用 `setValue(...)` 修改 `value`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `[noexcept, since 6.6] void QSqlField::swap(QSqlField &other)`

**作用与语义：**

将该字段与`other`交换。这个操作非常快，且从未失败。

### `QString QSqlField::tableName() const`

**作用与语义：**

返回 tableName。
注意：属性tableName的Getter函数。

### `QVariant QSqlField::value() const`

**作用与语义：**

返回价值的值。
注意：房产价值的获取函数。

### `bool QSqlField::operator!=(const QSqlField &other) const`

**作用与语义：**

如果场不等于`other`，则返回`true`;否则返回假。

### `QSqlField &QSqlField::operator=(const QSqlField &other)`

**作用与语义：**

将场设为`other`。

### `bool QSqlField::operator==(const QSqlField &other) const`

**作用与语义：**

如果场等于 `other`，则返回 `true`;否则返回 false。

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

`QSqlField` 所属机制类型：Qt SQL 连接、查询与事务机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
