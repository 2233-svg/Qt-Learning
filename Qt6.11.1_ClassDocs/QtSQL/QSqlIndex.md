# QSqlIndex

> Qt 6.11.1 · Qt SQL

## 1. 先建立直觉

**一句话定位：** `QSqlIndex` 是 Qt SQL 的“SqlIndex”类型，参与数据库连接、SQL 执行、事务或结果模型。

**模块背景：** Qt SQL 提供数据库连接、查询、事务和 SQL 模型/视图集成。

### 这是什么

`QSqlIndex` 是 Qt SQL 连接、查询与事务机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** Qt SQL 把驱动、连接、查询游标和模型分成不同对象。连接决定驱动和数据库会话，`QSqlQuery` 代表语句及其结果游标，事务把多条语句的提交边界固定下来，SQL 模型再把查询结果接到视图。

**适用场景：** 创建连接并检查 open，使用 prepare/bindValue 分离 SQL 结构和用户数据，执行后检查返回值和 lastError，遍历结果，必要时用 transaction/commit/rollback 包住一组操作。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要拼接用户输入形成 SQL；不要把 exec 成功当作有数据；不要在连接仍被引用时 removeDatabase；不要忽略驱动是否可用、字段类型转换和事务失败回滚。

## 2. 依赖与对象关系

- 头文件：`#include <QSqlIndex>`
- 继承自：QSqlRecord
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

### 属性

- `(since 6.8) cursorName : QString`
- `(since 6.8) name : QString`

### 公有函数

- `QSqlIndex(const QString &cursorname = QString(), const QString &name = QString())`
- `QSqlIndex(const QSqlIndex &other)`
- `(since 6.6) QSqlIndex(QSqlIndex &&other)`
- `~QSqlIndex()`
- `void append(const QSqlField &field)`
- `void append(const QSqlField &field, bool desc)`
- `QString cursorName() const`
- `bool isDescending(int i) const`
- `QString name() const`
- `void setCursorName(const QString &cursorName)`
- `void setDescending(int i, bool desc)`
- `void setName(const QString &name)`
- `(since 6.6) QSqlIndex & operator=(QSqlIndex &&other)`
- `QSqlIndex & operator=(const QSqlIndex &other)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[since 6.8] cursorName : QString`

**作用与语义：**

该属性保存索引关联的光标名称。

**如何使用：** 调用 `cursorName()` 读取当前值；它不会修改应用状态。

### `[since 6.8] name : QString`

**作用与语义：**

该属性保存索引名称。

**如何使用：** 调用 `name()` 读取当前值；它不会修改应用状态。

### `[explicit] QSqlIndex::QSqlIndex(const QString &cursorname = QString(), const QString &name = QString())`

**作用与语义：**

利用光标名`cursorname`和索引名`name`构建空索引。

### `QSqlIndex::QSqlIndex(const QSqlIndex &other)`

**作用与语义：**

复制了`other`。

### `[noexcept, since 6.6] QSqlIndex::QSqlIndex(QSqlIndex &&other)`

**作用与语义：**

从`other`移动构建新的QSqlIndex。
注意：移除对象 `other` 处于部分成形状态，唯一有效的操作是销毁和赋予新值。

### `[noexcept] QSqlIndex::~QSqlIndex()`

**作用与语义：**

摧毁该物体并释放所有分配的资源。

### `void QSqlIndex::append(const QSqlField &field)`

**作用与语义：**

将字段`field`附加到索引字段列表中。字段以升序排序附加。

### `void QSqlIndex::append(const QSqlField &field, bool desc)`

**作用与语义：**

将字段`field`附加到索引字段列表中。字段以升排序顺序附加，除非`desc`为真。

### `QString QSqlIndex::cursorName() const`

**作用与语义：**

返回光标Name。
注意：属性游标Name的获取函数。

### `bool QSqlIndex::isDescending(int i) const`

**作用与语义：**

如果索引中的字段`i`按降序排序，返回 `true`;否则返回 `false`。

### `QString QSqlIndex::name() const`

**作用与语义：**

还原了名字。
注意：物业名称的获取函数。

### `void QSqlIndex::setCursorName(const QString &cursorName)`

**作用与语义：**

该属性保存索引关联的光标名称。

**如何使用：** 调用 `setCursorName(...)` 修改 `cursorName`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QSqlIndex::setDescending(int i, bool desc)`

**作用与语义：**

如果`desc`为真，字段`i`按降序排序。否则，字段`i`按默认顺序从高到低排序。如果该字段不存在，则不会发生任何事。

### `void QSqlIndex::setName(const QString &name)`

**作用与语义：**

该属性保存索引名称。

**如何使用：** 调用 `setName(...)` 修改 `name`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `[noexcept, since 6.6] QSqlIndex &QSqlIndex::operator=(QSqlIndex &&other)`

**作用与语义：**

Move-assign `other`到该`QSqlIndex`实例。
注意：移出对象 `other` 处于部分成形状态，唯一有效的操作是销毁和赋值。

### `QSqlIndex &QSqlIndex::operator=(const QSqlIndex &other)`

**作用与语义：**

将索引设为`other`。

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

`QSqlIndex` 所属机制类型：Qt SQL 连接、查询与事务机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
