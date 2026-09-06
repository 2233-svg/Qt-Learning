# QStandardItemModel

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QStandardItemModel` 是 模型/视图协议 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QStandardItemModel` 是模型/视图体系中的数据模型类型，向视图提供索引、角色数据和结构变化通知。

**内部模型：** 视图不应该直接操作底层容器；它通过 QModelIndex 和 data roles 查询模型。模型必须准确维护索引有效性以及插入、删除、移动时的通知顺序。

**适用场景：** 需要把自定义数据接入 QListView、QTableView、QTreeView 或代理模型时使用。

**典型调用链：** 准备数据源 -> 实现/配置模型 -> 连接 view -> 通过 data/flags/setData 读写 -> 发出 dataChanged 或 begin/end 结构通知。

**先记住的坑：** 不要在 data() 中修改数据；不要返回过期索引；不要用全量 reset 代替精确结构通知，除非确实无法描述变化。

## 2. 依赖与对象关系

- 头文件：`#include <QStandardItemModel>`
- 继承自：QAbstractItemModel
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

视图不应该直接操作底层容器；它通过 QModelIndex 和 data roles 查询模型。模型必须准确维护索引有效性以及插入、删除、移动时的通知顺序。

### 状态、生命周期和线程

**生命周期：** 模型应比视图活得足够久，视图销毁时不会自动替业务容器释放资源。模型变化必须使用对应的 begin/end 协议或精确通知，不能只改容器后期待视图自行发现。取到的 QModelIndex 只在模型允许的生命周期内有效。

**状态与结果：** 区分当前索引、选择模型、编辑状态、数据角色和模型结构变化。`dataChanged` 表示已有项目的数据变化，行列插入/删除表示结构变化，`modelReset` 会让旧索引整体失效。

**线程与事件循环：** 模型通常在 GUI 线程被视图访问。后台线程不要直接修改正在显示的模型；应在正确线程汇总数据，再通过通知协议更新，或使用线程安全的数据交换层。

## 3. 直接使用

需要把自定义数据接入 QListView、QTableView、QTreeView 或代理模型时使用。 使用时通常按这个过程组织：准备数据源 -> 实现/配置模型 -> 连接 view -> 通过 data/flags/setData 读写 -> 发出 dataChanged 或 begin/end 结构通知。

```cpp
// 视图通过 QModelIndex 和 role 查询模型。
const QVariant value = model->data(index, Qt::DisplayRole);
// 数据变化时由模型发出 dataChanged 或 begin/end 结构通知。
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 属性

- `sortRole : int`

### 公有函数

- `QStandardItemModel(QObject *parent = nullptr)`
- `QStandardItemModel(int rows, int columns, QObject *parent = nullptr)`
- `virtual ~QStandardItemModel()`
- `void appendColumn(const QList<QStandardItem *> &items)`
- `void appendRow(const QList<QStandardItem *> &items)`
- `void appendRow(QStandardItem *item)`
- `QBindable<int> bindableSortRole()`
- `void clear()`
- `QList<QStandardItem *> findItems(const QString &text, Qt::MatchFlags flags = Qt::MatchExactly, int column = 0) const`
- `QStandardItem * horizontalHeaderItem(int column) const`
- `QModelIndex indexFromItem(const QStandardItem *item) const`
- `void insertColumn(int column, const QList<QStandardItem *> &items)`
- `bool insertColumn(int column, const QModelIndex &parent = QModelIndex())`
- `void insertRow(int row, const QList<QStandardItem *> &items)`
- `bool insertRow(int row, const QModelIndex &parent = QModelIndex())`
- `void insertRow(int row, QStandardItem *item)`
- `QStandardItem * invisibleRootItem() const`
- `QStandardItem * item(int row, int column = 0) const`
- `QStandardItem * itemFromIndex(const QModelIndex &index) const`
- `const QStandardItem * itemPrototype() const`
- `void setColumnCount(int columns)`
- `void setHorizontalHeaderItem(int column, QStandardItem *item)`
- `void setHorizontalHeaderLabels(const QStringList &labels)`
- `void setItem(int row, int column, QStandardItem *item)`
- `void setItem(int row, QStandardItem *item)`
- `void setItemPrototype(const QStandardItem *item)`
- `void setItemRoleNames(const QHash<int, QByteArray> &roleNames)`
- `void setRowCount(int rows)`
- `void setSortRole(int role)`
- `void setVerticalHeaderItem(int row, QStandardItem *item)`
- `void setVerticalHeaderLabels(const QStringList &labels)`
- `int sortRole() const`
- `QList<QStandardItem *> takeColumn(int column)`
- `QStandardItem * takeHorizontalHeaderItem(int column)`
- `QStandardItem * takeItem(int row, int column = 0)`
- `QList<QStandardItem *> takeRow(int row)`
- `QStandardItem * takeVerticalHeaderItem(int row)`
- `QStandardItem * verticalHeaderItem(int row) const`

### 重实现的公有函数

- `virtual bool clearItemData(const QModelIndex &index) override`
- `virtual int columnCount(const QModelIndex &parent = QModelIndex()) const override`
- `virtual QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const override`
- `virtual bool dropMimeData(const QMimeData *data, Qt::DropAction action, int row, int column, const QModelIndex &parent) override`
- `virtual Qt::ItemFlags flags(const QModelIndex &index) const override`
- `virtual bool hasChildren(const QModelIndex &parent = QModelIndex()) const override`
- `virtual QVariant headerData(int section, Qt::Orientation orientation, int role = Qt::DisplayRole) const override`
- `virtual QModelIndex index(int row, int column, const QModelIndex &parent = QModelIndex()) const override`
- `virtual bool insertColumns(int column, int count, const QModelIndex &parent = QModelIndex()) override`
- `virtual bool insertRows(int row, int count, const QModelIndex &parent = QModelIndex()) override`
- `virtual QMap<int, QVariant> itemData(const QModelIndex &index) const override`
- `virtual QMimeData * mimeData(const QModelIndexList &indexes) const override`
- `virtual QStringList mimeTypes() const override`
- `virtual void multiData(const QModelIndex &index, QModelRoleDataSpan roleDataSpan) const override`
- `virtual QModelIndex parent(const QModelIndex &child) const override`
- `virtual bool removeColumns(int column, int count, const QModelIndex &parent = QModelIndex()) override`
- `virtual bool removeRows(int row, int count, const QModelIndex &parent = QModelIndex()) override`
- `virtual QHash<int, QByteArray> roleNames() const override`
- `virtual int rowCount(const QModelIndex &parent = QModelIndex()) const override`
- `virtual bool setData(const QModelIndex &index, const QVariant &value, int role = Qt::EditRole) override`
- `virtual bool setHeaderData(int section, Qt::Orientation orientation, const QVariant &value, int role = Qt::EditRole) override`
- `virtual bool setItemData(const QModelIndex &index, const QMap<int, QVariant> &roles) override`
- `virtual void sort(int column, Qt::SortOrder order = Qt::AscendingOrder) override`
- `virtual Qt::DropActions supportedDropActions() const override`

### 信号

- `void itemChanged(QStandardItem *item)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[bindable] sortRole : int`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性包含用于查询模型数据的项目角色，用于排序项目时查询数据。
默认值是`Qt::DisplayRole`。

**如何使用：** 调用 `sortRole()` 读取当前值；它不会修改应用状态。

### `[explicit] QStandardItemModel::QStandardItemModel(QObject *parent = nullptr)`

**作用与语义：**

用给定的 `parent` 构建一个新的物品模型。

### `QStandardItemModel::QStandardItemModel(int rows, int columns, QObject *parent = nullptr)`

**作用与语义：**

构建一个新的项目模型，初始有`rows`行和`columns`列，且`parent`。

### `[virtual noexcept] QStandardItemModel::~QStandardItemModel()`

**作用与语义：**

摧毁模型。模型销毁所有物品。

### `void QStandardItemModel::appendColumn(const QList<QStandardItem *> &items)`

**作用与语义：**

附加包含`items`的列。如有必要，行数增加至`items`大小。

### `void QStandardItemModel::appendRow(const QList<QStandardItem *> &items)`

**作用与语义：**

附加包含`items`的行。如有必要，列数增加至`items`大小。

### `void QStandardItemModel::appendRow(QStandardItem *item)`

**作用与语义：**

当构建只有一列的列表或树时，该函数提供了方便地添加单一新 `item` 的方法。

### `void QStandardItemModel::clear()`

**作用与语义：**

从模型中移除所有项目（包括头部项），并将行数和列数设为零。

### `[override virtual] bool QStandardItemModel::clearItemData(const QModelIndex &index)`

**作用与语义：**

重装：`QAbstractItemModel::clearItemData`（const QModelIndex & index）。

### `[override virtual] int QStandardItemModel::columnCount(const QModelIndex &parent = QModelIndex()) const`

**作用与语义：**

重实现自：`QAbstractItemModel::columnCount`（const QModelIndex &parent） const.

### `[override virtual] QVariant QStandardItemModel::data(const QModelIndex &index, int role = Qt::DisplayRole) const`

**作用与语义：**

重实现自：`QAbstractItemModel::data`（const QModelIndex & index， int role） const.

### `[override virtual] bool QStandardItemModel::dropMimeData(const QMimeData *data, Qt::DropAction action, int row, int column, const QModelIndex &parent)`

**作用与语义：**

把拖放数据 `data` 按 `action` 插入 `parent` 下的 `row`、`column` 位置，成功返回 `true`。`row` 或 `column` 为 -1 表示由模型选择合适位置；自定义 MIME 格式时应与 `mimeTypes()` 和 `mimeData()` 配套重实现。

### `QList<QStandardItem *> QStandardItemModel::findItems(const QString &text, Qt::MatchFlags flags = Qt::MatchExactly, int column = 0) const`

**作用与语义：**

返回与给定`text`匹配的物品列表，使用给定`flags`，在给定`column`中返回。

### `[override virtual] Qt::ItemFlags QStandardItemModel::flags(const QModelIndex &index) const`

**作用与语义：**

重实现自：`QAbstractItemModel::flags`（const QModelIndex & index） const.

### `[override virtual] bool QStandardItemModel::hasChildren(const QModelIndex &parent = QModelIndex()) const`

**作用与语义：**

重实现自：`QAbstractItemModel::hasChildren`（const QModelIndex & parent）const.

### `[override virtual] QVariant QStandardItemModel::headerData(int section, Qt::Orientation orientation, int role = Qt::DisplayRole) const`

**作用与语义：**

重实现自：`QAbstractItemModel::headerData`（int section，Qt：：Orientation orientation， int role）const.

### `QStandardItem *QStandardItemModel::horizontalHeaderItem(int column) const`

**作用与语义：**

如果设置了水平头部项，返回`column`的水平头项;否则返回`nullptr`。

### `[override virtual] QModelIndex QStandardItemModel::index(int row, int column, const QModelIndex &parent = QModelIndex()) const`

**作用与语义：**

重实现自：`QAbstractItemModel::index`（整数行，整数列，条件 QModelIndex 和父）const.

### `QModelIndex QStandardItemModel::indexFromItem(const QStandardItem *item) const`

**作用与语义：**

返回与给定`item`关联的`QModelIndex`。
当你想执行需要`QModelIndex`项的操作时，可以使用这个函数，比如`QAbstractItemView::scrollTo()`。`QStandardItem::index()`是出于方便而提供的;它等同于调用这个函数。

### `void QStandardItemModel::insertColumn(int column, const QList<QStandardItem *> &items)`

**作用与语义：**

在 `column` 插入一列，包含 `items`。如有必要，行数增加到 `items` 大小。

### `bool QStandardItemModel::insertColumn(int column, const QModelIndex &parent = QModelIndex())`

**作用与语义：**

在指定`parent`的子项中插入给定`column`前的单一列。如果插入该列，返回`true`;否则返回`false`。

### `[override virtual] bool QStandardItemModel::insertColumns(int column, int count, const QModelIndex &parent = QModelIndex())`

**作用与语义：**

重实现自：`QAbstractItemModel::insertColumns`（整数列，整数计数，条件QModelIndex和parent）。

### `void QStandardItemModel::insertRow(int row, const QList<QStandardItem *> &items)`

**作用与语义：**

在`row`插入包含`items`的行。如有必要，列数增加至`items`大小。

### `bool QStandardItemModel::insertRow(int row, const QModelIndex &parent = QModelIndex())`

**作用与语义：**

在指定`parent`的子项中插入给定`row`前的一行。如果插入该行，返回`true`;否则返回`false`。

### `void QStandardItemModel::insertRow(int row, QStandardItem *item)`

**作用与语义：**

在`row`插入一行包含`item`。
当构建只有一列的列表或树时，该函数提供了方便地添加单个新项的方式。

### `[override virtual] bool QStandardItemModel::insertRows(int row, int count, const QModelIndex &parent = QModelIndex())`

**作用与语义：**

重实现自：`QAbstractItemModel::insertRows`（整数行，整数计数，cont QModelIndex 和父）。

### `QStandardItem *QStandardItemModel::invisibleRootItem() const`

**作用与语义：**

返回模型的隐形根项。
隐形根项通过`QStandardItem` API访问模型的顶层项，使得能够以统一方式处理顶层项及其子项的函数成为可能;例如，涉及树模型的递归函数。
注意：调用从该函数检索的`QStandardItem`对象的 `index()` 是无效的。

### `QStandardItem *QStandardItemModel::item(int row, int column = 0) const`

**作用与语义：**

如果已设置，返回给定`row`和`column`的项目;否则返回`nullptr`。

### `[signal] void QStandardItemModel::itemChanged(QStandardItem *item)`

**作用与语义：**

每当`item`的数据发生变化时，该信号就会发出。

### `[override virtual] QMap<int, QVariant> QStandardItemModel::itemData(const QModelIndex &index) const`

**作用与语义：**

重实现自：`QAbstractItemModel::itemData`（const QModelIndex & index） const.

### `QStandardItem *QStandardItemModel::itemFromIndex(const QModelIndex &index) const`

**作用与语义：**

返回指向与给定`index`相关的`QStandardItem`的指针。
调用该函数通常是处理视图（如`QAbstractItemView::activated()`）基于`QModelIndex`信号的初始步骤。在你的槽中，调用itemFromIndex()，并以信号携带的`QModelIndex`作为参数，获取指向对应`QStandardItem`的指针。
注意，这个函数会懒惰地为索引创建一个项（使用`itemPrototype()`），并在父项的子表中设置，如果该索引中没有任何项。
如果`index`是无效索引，该函数返回`nullptr`。

### `const QStandardItem *QStandardItemModel::itemPrototype() const`

**作用与语义：**

返回模型使用的物品原型。模型在需要按需构建新物品时（例如，当视图或物品委托调用`setData()`时，将物品原型作为物品工厂使用）。

### `[override virtual] QMimeData *QStandardItemModel::mimeData(const QModelIndexList &indexes) const`

**作用与语义：**

重实现自：`QAbstractItemModel::mimeData`（const QModelIndexList & indexes） const.

### `[override virtual] QStringList QStandardItemModel::mimeTypes() const`

**作用与语义：**

重装：`QAbstractItemModel::mimeTypes()` const.

### `[override virtual] void QStandardItemModel::multiData(const QModelIndex &index, QModelRoleDataSpan roleDataSpan) const`

**作用与语义：**

一次读取 `index` 的多个角色并填入 `roleDataSpan`，避免逐个调用 `data()` 的开销。每个请求角色都应写回对应值；派生模型未处理的角色应交给基类实现。

### `[override virtual] QModelIndex QStandardItemModel::parent(const QModelIndex &child) const`

**作用与语义：**

重实现自：`QAbstractItemModel::parent`（const QModelIndex & index） const.

### `[override virtual] bool QStandardItemModel::removeColumns(int column, int count, const QModelIndex &parent = QModelIndex())`

**作用与语义：**

重实现自：`QAbstractItemModel::removeColumns`（整数列，整数计数，条件QModelIndex和parent）。

### `[override virtual] bool QStandardItemModel::removeRows(int row, int count, const QModelIndex &parent = QModelIndex())`

**作用与语义：**

重实现自：`QAbstractItemModel::removeRows`（整数行、整数计数、cont QModelIndex 和父）。

### `[override virtual] QHash<int, QByteArray> QStandardItemModel::roleNames() const`

**作用与语义：**

重实现自：`QAbstractItemModel::roleNames()` const.

### `[override virtual] int QStandardItemModel::rowCount(const QModelIndex &parent = QModelIndex()) const`

**作用与语义：**

重实现自：Const QModelIndex 和 parent const. `QAbstractItemModel::rowCount`（const QModelIndex & parent） const.

### `void QStandardItemModel::setColumnCount(int columns)`

**作用与语义：**

将该模型中的列数设为`columns`。如果小于`columnCount()`，则丢弃不需要列中的数据。

### `[override virtual] bool QStandardItemModel::setData(const QModelIndex &index, const QVariant &value, int role = Qt::EditRole)`

**作用与语义：**

重实现自：`QAbstractItemModel::setData`（const QModelIndex & index，const QVariant & value，int role）。

### `[override virtual] bool QStandardItemModel::setHeaderData(int section, Qt::Orientation orientation, const QVariant &value, int role = Qt::EditRole)`

**作用与语义：**

重实现自：`QAbstractItemModel::setHeaderData`（整数部分，Qt：：Orientation orientation，const QVariant & value，int role）。

### `void QStandardItemModel::setHorizontalHeaderItem(int column, QStandardItem *item)`

**作用与语义：**

将`column`的水平头项设置为`item`。模型对该项拥有权。如有必要，增加列数以适应该项。如果有，之前的头项（如果有的话）被删除。

### `void QStandardItemModel::setHorizontalHeaderLabels(const QStringList &labels)`

**作用与语义：**

使用`labels`设置水平头部标签。如有必要，列数增加至`labels`大小。

### `void QStandardItemModel::setItem(int row, int column, QStandardItem *item)`

**作用与语义：**

为给定`row`设置该项，并`column` `item`。模型对该项拥有权。如有必要，增加行数和列数以适应该项。如果有该位置的前一项（如果有的话）会被删除。

### `void QStandardItemModel::setItem(int row, QStandardItem *item)`

**作用与语义：**

为给定`row`设置该项，并`column` `item`。模型对该项拥有权。如有必要，增加行数和列数以适应该项。如果有该位置的前一项（如果有的话）会被删除。

### `[override virtual] bool QStandardItemModel::setItemData(const QModelIndex &index, const QMap<int, QVariant> &roles)`

**作用与语义：**

重实现自：`QAbstractItemModel::setItemData`（const QModelIndex & index， const QMap<int， QVariant> and roles）。

### `void QStandardItemModel::setItemPrototype(const QStandardItem *item)`

**作用与语义：**

将模型的项目原型设置为指定的`item`。模型拥有原型的所有权。
物品原型作为`QStandardItem`工厂，依赖`QStandardItem::clone()`函数。要提供自己的原型、子类`QStandardItem`，重现`QStandardItem::clone()`，并将原型设置为自定义类的实例。每当`QStandardItemModel`需要按需创建物品（例如视图或物品代理调用`setData()`）时，新物品将是你自定义类的实例。

### `void QStandardItemModel::setItemRoleNames(const QHash<int, QByteArray> &roleNames)`

**作用与语义：**

将物品角色名称设置为`roleNames`。

### `void QStandardItemModel::setRowCount(int rows)`

**作用与语义：**

将该模型中的行数设为`rows`。如果小于`rowCount()`，不需要的行数据将被丢弃。

### `void QStandardItemModel::setVerticalHeaderItem(int row, QStandardItem *item)`

**作用与语义：**

将`row`的垂直头项设置为`item`。模型对该项拥有所有权。如有必要，增加行数以适应该项。如果有之前的头部项，则被删除。

### `void QStandardItemModel::setVerticalHeaderLabels(const QStringList &labels)`

**作用与语义：**

使用`labels`设置垂直头部标签。如有必要，行数增加至`labels`大小。

### `[override virtual] void QStandardItemModel::sort(int column, Qt::SortOrder order = Qt::AscendingOrder)`

**作用与语义：**

重实现自：`QAbstractItemModel::sort`（整数列，Qt：：SortOrder order）。

### `[override virtual] Qt::DropActions QStandardItemModel::supportedDropActions() const`

**作用与语义：**

重装：`QAbstractItemModel::supportedDropActions()` const.
`QStandardItemModel`支持复制和移动。

### `QList<QStandardItem *> QStandardItemModel::takeColumn(int column)`

**作用与语义：**

移除给定`column`而不删除列项，返回指向已移除项的指针列表。模型释放了这些项的所有权。对于列中未被设置的项，列表中对应的指针将被`nullptr`。

### `QStandardItem *QStandardItemModel::takeHorizontalHeaderItem(int column)`

**作用与语义：**

在不删除`column`页首的水平头条项时移除，并返回指向该项的指针。模型释放了该项的所有权。

### `QStandardItem *QStandardItemModel::takeItem(int row, int column = 0)`

**作用与语义：**

在（`row`， `column`）处移除该物品而不删除它。模型释放该物品的所有权。

### `QList<QStandardItem *> QStandardItemModel::takeRow(int row)`

**作用与语义：**

移除给定`row`而不删除行中物品，并返回指向已移除物品的指针列表。模型释放了对该项的所有权。对于未被设置的行中物品，列表中对应的指针将被`nullptr`。

### `QStandardItem *QStandardItemModel::takeVerticalHeaderItem(int row)`

**作用与语义：**

在不删除该项目的情况下，将`row`处的垂直头项从头部移除，并返回指向该项的指针。模型释放了该项的所有权。

### `QStandardItem *QStandardItemModel::verticalHeaderItem(int row) const`

**作用与语义：**

如果设置了垂直头项，返回第`row`行的垂直头项;否则返回`nullptr`。

### `QBindable<int> bindableSortRole()`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性包含用于查询模型数据的项目角色，用于排序项目时查询数据。
默认值是`Qt::DisplayRole`。

**如何使用：** 调用 `bindableSortRole()` 取得 `sortRole` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `void setSortRole(int role)`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性包含用于查询模型数据的项目角色，用于排序项目时查询数据。
默认值是`Qt::DisplayRole`。

**如何使用：** 调用 `setSortRole(...)` 修改 `sortRole`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `int sortRole() const`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性包含用于查询模型数据的项目角色，用于排序项目时查询数据。
默认值是`Qt::DisplayRole`。

**如何使用：** 调用 `sortRole()` 读取当前值；它不会修改应用状态。

## 6. 深入实践与常见坑

### 生命周期和资源边界

模型应比视图活得足够久，视图销毁时不会自动替业务容器释放资源。模型变化必须使用对应的 begin/end 协议或精确通知，不能只改容器后期待视图自行发现。取到的 QModelIndex 只在模型允许的生命周期内有效。

### 状态和错误边界

区分当前索引、选择模型、编辑状态、数据角色和模型结构变化。`dataChanged` 表示已有项目的数据变化，行列插入/删除表示结构变化，`modelReset` 会让旧索引整体失效。

### 线程边界

模型通常在 GUI 线程被视图访问。后台线程不要直接修改正在显示的模型；应在正确线程汇总数据，再通过通知协议更新，或使用线程安全的数据交换层。

### 最容易出现的错误

不要在 data() 中修改数据；不要返回过期索引；不要用全量 reset 代替精确结构通知，除非确实无法描述变化。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QStandardItemModel` 所属机制类型：模型/视图协议。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
