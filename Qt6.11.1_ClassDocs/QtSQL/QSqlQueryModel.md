# QSqlQueryModel

> Qt 6.11.1 · Qt SQL

## 1. 先建立直觉

**一句话定位：** `QSqlQueryModel` 是 Qt SQL 的“Sql查询模型”类型，参与数据库连接、SQL 执行、事务或结果模型。

**模块背景：** Qt SQL 提供数据库连接、查询、事务和 SQL 模型/视图集成。

### 这是什么

`QSqlQueryModel` 是模型/视图体系中的数据模型类型，向视图提供索引、角色数据和结构变化通知。

**内部模型：** 视图不应该直接操作底层容器；它通过 QModelIndex 和 data roles 查询模型。模型必须准确维护索引有效性以及插入、删除、移动时的通知顺序。

**适用场景：** 需要把自定义数据接入 QListView、QTableView、QTreeView 或代理模型时使用。

**典型调用链：** 准备数据源 -> 实现/配置模型 -> 连接 view -> 通过 data/flags/setData 读写 -> 发出 dataChanged 或 begin/end 结构通知。

**先记住的坑：** 不要在 data() 中修改数据；不要返回过期索引；不要用全量 reset 代替精确结构通知，除非确实无法描述变化。

## 2. 依赖与对象关系

- 头文件：`#include <QSqlQueryModel>`
- 继承自：QAbstractTableModel
- 直接派生类：QSqlTableModel

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Sql)
target_link_libraries(mytarget PRIVATE Qt6::Sql)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

视图不应该直接操作底层容器；它通过 QModelIndex 和 data roles 查询模型。模型必须准确维护索引有效性以及插入、删除、移动时的通知顺序。

### 状态、生命周期和线程

**生命周期：** 连接由连接名识别，查询和模型引用连接。关闭或移除连接前必须销毁仍引用它的 query、model 和 database 句柄；不同线程不要共用连接。

**状态与结果：** 区分连接是否打开、语句是否执行成功、游标是否定位在有效行、字段是否存在以及事务是否提交成功。`exec()` 成功不代表有结果行，`next()` 成功后才可以安全读取当前行。

**线程与事件循环：** Qt SQL 连接有线程归属，每个线程应建立自己的连接并使用唯一连接名；不要把一个线程创建的 QSqlDatabase 或 QSqlQuery 传到另一个线程继续使用。

## 3. 直接使用

需要把自定义数据接入 QListView、QTableView、QTreeView 或代理模型时使用。 使用时通常按这个过程组织：准备数据源 -> 实现/配置模型 -> 连接 view -> 通过 data/flags/setData 读写 -> 发出 dataChanged 或 begin/end 结构通知。

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

- `QSqlQueryModel(QObject *parent = nullptr)`
- `virtual ~QSqlQueryModel()`
- `virtual void clear()`
- `QSqlError lastError() const`
- `const QSqlQuery & query() const`
- `QSqlRecord record(int row) const`
- `QSqlRecord record() const`
- `(since 6.9) void refresh()`
- `(since 6.2) void setQuery(QSqlQuery &&query)`
- `void setQuery(const QString &query, const QSqlDatabase &db = QSqlDatabase())`

### 重实现的公有函数

- `virtual bool canFetchMore(const QModelIndex &parent = QModelIndex()) const override`
- `virtual int columnCount(const QModelIndex &index = QModelIndex()) const override`
- `virtual QVariant data(const QModelIndex &item, int role = Qt::DisplayRole) const override`
- `virtual void fetchMore(const QModelIndex &parent = QModelIndex()) override`
- `virtual QVariant headerData(int section, Qt::Orientation orientation, int role = Qt::DisplayRole) const override`
- `virtual bool insertColumns(int column, int count, const QModelIndex &parent = QModelIndex()) override`
- `virtual bool removeColumns(int column, int count, const QModelIndex &parent = QModelIndex()) override`
- `virtual QHash<int, QByteArray> roleNames() const override`
- `virtual int rowCount(const QModelIndex &parent = QModelIndex()) const override`
- `virtual bool setHeaderData(int section, Qt::Orientation orientation, const QVariant &value, int role = Qt::EditRole) override`

### 保护函数

- `virtual QModelIndex indexInQuery(const QModelIndex &item) const`
- `virtual void queryChange()`
- `void setLastError(const QSqlError &error)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[explicit] QSqlQueryModel::QSqlQueryModel(QObject *parent = nullptr)`

**作用与语义：**

创建一个空的QSqlQueryModel，`parent`。

### `[virtual noexcept] QSqlQueryModel::~QSqlQueryModel()`

**作用与语义：**

摧毁该物体并释放所有分配的资源。

### `[override virtual] bool QSqlQueryModel::canFetchMore(const QModelIndex &parent = QModelIndex()) const`

**作用与语义：**

重实现自：`QAbstractItemModel::canFetchMore`（const QModelIndex & parent） const.
如果可以从数据库中读取更多行，返回`true`。这只影响那些不报告查询大小的数据库（见 `QSqlDriver::hasFeature()`）。
`parent`应该永远是无效`QModelIndex`。

### `[virtual] void QSqlQueryModel::clear()`

**作用与语义：**

清除模型并释放任何获得的资源。

### `[override virtual] int QSqlQueryModel::columnCount(const QModelIndex &index = QModelIndex()) const`

**作用与语义：**

重实现自：`QAbstractItemModel::columnCount`（const QModelIndex &parent） const.

### `[override virtual] QVariant QSqlQueryModel::data(const QModelIndex &item, int role = Qt::DisplayRole) const`

**作用与语义：**

重实现自：`QAbstractItemModel::data`（const QModelIndex & index， int role） const.
返回指定`item`和`role`的值。
如果`item`出界或发生错误，则返回无效`QVariant`。

### `[override virtual] void QSqlQueryModel::fetchMore(const QModelIndex &parent = QModelIndex())`

**作用与语义：**

重装：`QAbstractItemModel::fetchMore`（const QModelIndex 及父）。
从数据库中获取更多行。这只影响那些不报告查询大小的数据库（参见`QSqlDriver::hasFeature()`）。
为了强制获取整个结果集，可以使用以下方法：
`parent`应该永远是无效的`QModelIndex`。

**官方示例：**

```cpp
 while (myModel->canFetchMore())
     myModel->fetchMore();
```

### `[override virtual] QVariant QSqlQueryModel::headerData(int section, Qt::Orientation orientation, int role = Qt::DisplayRole) const`

**作用与语义：**

重实现自：`QAbstractItemModel::headerData`（int section，Qt：：Orientation orientation， int role）const.
返回指定`orientation`的`section`中给定`role`的头部数据。

### `[virtual protected] QModelIndex QSqlQueryModel::indexInQuery(const QModelIndex &item) const`

**作用与语义：**

返回数据库结果集中对模型中给定`item`的值索引。
如果没有插入、删除或移动列或行，返回值与 `item` 相同。
如果`item`超出边界或`item`未指向结果集中的某个值，则返回无效的模型索引。

### `[override virtual] bool QSqlQueryModel::insertColumns(int column, int count, const QModelIndex &parent = QModelIndex())`

**作用与语义：**

重构：`QAbstractItemModel::insertColumns`（整数列，整数计数，函数QModelIndex 和parent）。
在模型位置`column`插入`count`列。`parent`参数必须始终是无效`QModelIndex`，因为模型不支持父子关系。
如果`column`在界限内，返回`true`;否则返回`false`。
默认情况下，插入的列为空。要填充数据，请重新实现`data()`并单独处理插入的列：

**官方示例：**

```cpp
 QVariant MyModel::data(const QModelIndex &item, int role) const
 {
     if (item.column() == m_specialColumnNo) {
         // handle column separately
     }
     return QSqlQueryModel::data(item, role);
 }
```

### `QSqlError QSqlQueryModel::lastError() const`

**作用与语义：**

返回数据库上最后一次发生错误的信息。

### `const QSqlQuery &QSqlQueryModel::query() const`

**作用与语义：**

返回与该模型相关的const对象`QSqlQuery`引用。

### `[virtual protected] void QSqlQueryModel::queryChange()`

**作用与语义：**

每当查询发生变化时，这个虚拟函数都会被调用。默认实现不做任何操作。
`query()`返回新查询。

### `QSqlRecord QSqlQueryModel::record(int row) const`

**作用与语义：**

返回包含当前查询字段信息的记录。如果`row`是有效行的索引，记录将填充该行的值。
如果模型未初始化，将返回一个空记录。

### `QSqlRecord QSqlQueryModel::record() const`

**作用与语义：**

返回一个包含当前查询字段信息的空记录。
如果模型未初始化，将返回一个空记录。

### `[since 6.9] void QSqlQueryModel::refresh()`

**作用与语义：**

重新执行当前查询以从同一数据库连接获取数据。
注意：当查询包含绑定值时，`refresh()`不适用。

### `[override virtual] bool QSqlQueryModel::removeColumns(int column, int count, const QModelIndex &parent = QModelIndex())`

**作用与语义：**

重实现自：`QAbstractItemModel::removeColumns`（整数列，整数计数，条件QModelIndex和parent）。
从模型`column`位置开始移除`count`列。`parent`参数必须始终是无效的`QModelIndex`，因为模型不支持父子关系。
移除柱子实际上可以隐藏它们。它不会影响底层`QSqlQuery`。
如果列被移除，返回`true`;否则返回`false`。

### `[override virtual] QHash<int, QByteArray> QSqlQueryModel::roleNames() const`

**作用与语义：**

重实现自：`QAbstractItemModel::roleNames()` const.
返回模特的角色名。
Qt只为`QSqlQueryModel`定义了一个角色：
- `Qt Role`：QML角色名称
- `Qt::DisplayRole`：展示

### `[override virtual] int QSqlQueryModel::rowCount(const QModelIndex &parent = QModelIndex()) const`

**作用与语义：**

重实现自：`QAbstractItemModel::rowCount`（const QModelIndex & parent） const.
如果数据库支持返回查询大小（见 `QSqlDriver::hasFeature()`），则返回当前查询的行数。否则，返回客户端当前缓存的行数。
`parent`应该永远是无效`QModelIndex`。

### `[override virtual] bool QSqlQueryModel::setHeaderData(int section, Qt::Orientation orientation, const QVariant &value, int role = Qt::EditRole)`

**作用与语义：**

重实现自：`QAbstractItemModel::setHeaderData`（整数部分，Qt：：Orientation orientation，const QVariant & value，整数角色）。
将指定`role`水平头的标题设置为`value`。如果模型用于视图显示数据（例如，`QTableView`），这非常有用。
如果`orientation` `Qt::Horizontal`且`section`指向有效切段，返回`true`;否则返回false。
注意，由于模型是只读的，该函数不能用于修改数据库中的值。

### `[protected] void QSqlQueryModel::setLastError(const QSqlError &error)`

**作用与语义：**

受保护函数允许派生类将数据库上最后一次错误的值设置为`error`。

### `[since 6.2] void QSqlQueryModel::setQuery(QSqlQuery &&query)`

**作用与语义：**

重置模型，并将数据提供者设置为给定的`query`。注意查询必须是主动的，且不得是isForwardOnly()。
如果查询设置错误，`lastError()` 可以用来检索冗长信息。
注意：调用 setQuery() 会移除所有插入的列。

### `void QSqlQueryModel::setQuery(const QString &query, const QSqlDatabase &db = QSqlDatabase())`

**作用与语义：**

执行给定数据库连接`db`的查询`query`。如果未指定数据库（或数据库无效），则使用默认连接。
如果查询设置有错误，`lastError()` 可以用来检索冗长信息。

**官方示例：**

```cpp
 QSqlQueryModel model;
 model.setQuery("select * from MyTable");
 if (model.lastError().isValid())
     qDebug() << model.lastError();
```

## 6. 深入实践与常见坑

### 生命周期和资源边界

连接由连接名识别，查询和模型引用连接。关闭或移除连接前必须销毁仍引用它的 query、model 和 database 句柄；不同线程不要共用连接。

### 状态和错误边界

区分连接是否打开、语句是否执行成功、游标是否定位在有效行、字段是否存在以及事务是否提交成功。`exec()` 成功不代表有结果行，`next()` 成功后才可以安全读取当前行。

### 线程边界

Qt SQL 连接有线程归属，每个线程应建立自己的连接并使用唯一连接名；不要把一个线程创建的 QSqlDatabase 或 QSqlQuery 传到另一个线程继续使用。

### 最容易出现的错误

不要在 data() 中修改数据；不要返回过期索引；不要用全量 reset 代替精确结构通知，除非确实无法描述变化。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QSqlQueryModel` 所属机制类型：Qt SQL 连接、查询与事务机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
