# QSortFilterProxyModel

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QSortFilterProxyModel` 是 模型/视图协议 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QSortFilterProxyModel` 是模型/视图体系中的数据模型类型，向视图提供索引、角色数据和结构变化通知。

**内部模型：** 视图不应该直接操作底层容器；它通过 QModelIndex 和 data roles 查询模型。模型必须准确维护索引有效性以及插入、删除、移动时的通知顺序。

**适用场景：** 需要把自定义数据接入 QListView、QTableView、QTreeView 或代理模型时使用。

**典型调用链：** 准备数据源 -> 实现/配置模型 -> 连接 view -> 通过 data/flags/setData 读写 -> 发出 dataChanged 或 begin/end 结构通知。

**先记住的坑：** 不要在 data() 中修改数据；不要返回过期索引；不要用全量 reset 代替精确结构通知，除非确实无法描述变化。

## 2. 依赖与对象关系

- 头文件：`#include <QSortFilterProxyModel>`
- 继承自：QAbstractProxyModel
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
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

### 公有类型

- `(since 6.10) enum class Direction { Rows, Columns, Both }`
- `flags Directions`

### 属性

- `(since 6.0) autoAcceptChildRows : bool`
- `dynamicSortFilter : bool`
- `filterCaseSensitivity : Qt::CaseSensitivity`
- `filterKeyColumn : int`
- `filterRegularExpression : QRegularExpression`
- `filterRole : int`
- `isSortLocaleAware : bool`
- `recursiveFilteringEnabled : bool`
- `sortCaseSensitivity : Qt::CaseSensitivity`
- `sortRole : int`

### 公有函数

- `QSortFilterProxyModel(QObject *parent = nullptr)`
- `virtual ~QSortFilterProxyModel()`
- `bool autoAcceptChildRows() const`
- `QBindable<bool> bindableAutoAcceptChildRows()`
- `QBindable<bool> bindableDynamicSortFilter()`
- `QBindable<Qt::CaseSensitivity> bindableFilterCaseSensitivity()`
- `QBindable<int> bindableFilterKeyColumn()`
- `QBindable<QRegularExpression> bindableFilterRegularExpression()`
- `QBindable<int> bindableFilterRole()`
- `QBindable<bool> bindableIsSortLocaleAware()`
- `QBindable<bool> bindableRecursiveFilteringEnabled()`
- `QBindable<Qt::CaseSensitivity> bindableSortCaseSensitivity()`
- `QBindable<int> bindableSortRole()`
- `bool dynamicSortFilter() const`
- `Qt::CaseSensitivity filterCaseSensitivity() const`
- `int filterKeyColumn() const`
- `QRegularExpression filterRegularExpression() const`
- `int filterRole() const`
- `bool isRecursiveFilteringEnabled() const`
- `bool isSortLocaleAware() const`
- `void setAutoAcceptChildRows(bool accept)`
- `void setDynamicSortFilter(bool enable)`
- `void setFilterCaseSensitivity(Qt::CaseSensitivity cs)`
- `void setFilterKeyColumn(int column)`
- `void setFilterRole(int role)`
- `void setRecursiveFilteringEnabled(bool recursive)`
- `void setSortCaseSensitivity(Qt::CaseSensitivity cs)`
- `void setSortLocaleAware(bool on)`
- `void setSortRole(int role)`
- `Qt::CaseSensitivity sortCaseSensitivity() const`
- `int sortColumn() const`
- `Qt::SortOrder sortOrder() const`
- `int sortRole() const`

### 重实现的公有函数

- `virtual QModelIndex buddy(const QModelIndex &index) const override`
- `virtual bool canFetchMore(const QModelIndex &parent) const override`
- `virtual int columnCount(const QModelIndex &parent = QModelIndex()) const override`
- `virtual QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const override`
- `virtual bool dropMimeData(const QMimeData *data, Qt::DropAction action, int row, int column, const QModelIndex &parent) override`
- `virtual void fetchMore(const QModelIndex &parent) override`
- `virtual Qt::ItemFlags flags(const QModelIndex &index) const override`
- `virtual bool hasChildren(const QModelIndex &parent = QModelIndex()) const override`
- `virtual QVariant headerData(int section, Qt::Orientation orientation, int role = Qt::DisplayRole) const override`
- `virtual QModelIndex index(int row, int column, const QModelIndex &parent = QModelIndex()) const override`
- `virtual bool insertColumns(int column, int count, const QModelIndex &parent = QModelIndex()) override`
- `virtual bool insertRows(int row, int count, const QModelIndex &parent = QModelIndex()) override`
- `virtual QModelIndex mapFromSource(const QModelIndex &sourceIndex) const override`
- `virtual QItemSelection mapSelectionFromSource(const QItemSelection &sourceSelection) const override`
- `virtual QItemSelection mapSelectionToSource(const QItemSelection &proxySelection) const override`
- `virtual QModelIndex mapToSource(const QModelIndex &proxyIndex) const override`
- `virtual QModelIndexList match(const QModelIndex &start, int role, const QVariant &value, int hits = 1, Qt::MatchFlags flags = Qt::MatchFlags(Qt::MatchStartsWith|Qt::MatchWrap)) const override`
- `virtual QMimeData * mimeData(const QModelIndexList &indexes) const override`
- `virtual QStringList mimeTypes() const override`
- `virtual QModelIndex parent(const QModelIndex &child) const override`
- `virtual bool removeColumns(int column, int count, const QModelIndex &parent = QModelIndex()) override`
- `virtual bool removeRows(int row, int count, const QModelIndex &parent = QModelIndex()) override`
- `virtual int rowCount(const QModelIndex &parent = QModelIndex()) const override`
- `virtual bool setData(const QModelIndex &index, const QVariant &value, int role = Qt::EditRole) override`
- `virtual bool setHeaderData(int section, Qt::Orientation orientation, const QVariant &value, int role = Qt::EditRole) override`
- `virtual void setSourceModel(QAbstractItemModel *sourceModel) override`
- `virtual QModelIndex sibling(int row, int column, const QModelIndex &idx) const override`
- `virtual void sort(int column, Qt::SortOrder order = Qt::AscendingOrder) override`
- `virtual QSize span(const QModelIndex &index) const override`
- `virtual Qt::DropActions supportedDropActions() const override`

### 公有槽函数

- `void invalidate()`
- `void setFilterFixedString(const QString &pattern)`
- `void setFilterRegularExpression(const QString &pattern)`
- `void setFilterRegularExpression(const QRegularExpression &regularExpression)`
- `void setFilterWildcard(const QString &pattern)`

### 信号

- `(since 6.0) void autoAcceptChildRowsChanged(bool autoAcceptChildRows)`
- `void filterCaseSensitivityChanged(Qt::CaseSensitivity filterCaseSensitivity)`
- `void filterRoleChanged(int filterRole)`
- `void recursiveFilteringEnabledChanged(bool recursiveFilteringEnabled)`
- `void sortCaseSensitivityChanged(Qt::CaseSensitivity sortCaseSensitivity)`
- `void sortLocaleAwareChanged(bool sortLocaleAware)`
- `void sortRoleChanged(int sortRole)`

### 保护函数

- `(since 6.9) void beginFilterChange()`
- `(since 6.10) void endFilterChange(QSortFilterProxyModel::Directions directions = Direction::Both)`
- `virtual bool filterAcceptsColumn(int source_column, const QModelIndex &source_parent) const`
- `virtual bool filterAcceptsRow(int source_row, const QModelIndex &source_parent) const`
- `(since 6.0, until 6.13) void invalidateColumnsFilter()`
- `(until 6.13) void invalidateFilter()`
- `(since 6.0, until 6.13) void invalidateRowsFilter()`
- `virtual bool lessThan(const QModelIndex &source_left, const QModelIndex &source_right) const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[since 6.10] enum class QSortFilterProxyModel::Directionflags QSortFilterProxyModel::Directions`

**作用与语义：**

该枚举用于指定当滤波器参数变更时，自定义滤波器的适用方向。
- `QSortFilterProxyModel::Direction::Rows`：`0x01`;滤波器适用于`rows`
- `QSortFilterProxyModel::Direction::Columns`：`0x02`;滤波器适用于`columns`
- `QSortFilterProxyModel::Direction::Both`：`Rows | Columns`;过滤器适用于行和列
这个枚举是在Qt 6.10引入的。
Directions 类型是 QFlags 的 typedef<Direction>。它存储 Direction 值的 OR 组合。

### `[bindable, since 6.0] autoAcceptChildRows : bool`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
如果成立，代理模型不会过滤掉被接受行的子节点，即使这些子节点本身也会被过滤掉。
默认值为假。

**如何使用：** 调用 `autoAcceptChildRows()` 读取当前值；它不会修改应用状态。

### `[bindable] dynamicSortFilter : bool`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性适用于代理模型在源模型内容变化时是否动态排序和过滤。
注意，当dynamicSortFilter为真时，不应通过代理模型更新源模型。例如，如果你在`QComboBox`上设置代理模型，使用更新模型的函数，如`addItem()`，将无法如预期般工作。另一种方法是将dynamicSortFilter设为false，添加`QComboBox`项后调用`sort()`。
默认值为真。

**如何使用：** 调用 `dynamicSortFilter()` 读取当前值；它不会修改应用状态。

### `[bindable] filterCaseSensitivity : Qt::CaseSensitivity`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性表示了用于过滤源模型内容的`QRegularExpression`模式的大小写敏感性。
默认情况下，滤波器是区分大小写的。
注意：设置该属性会将新的大小写敏感性传播到`filterRegularExpression`属性，从而破坏其绑定。同样，显式设置`filterRegularExpression`会改变当前大小写敏感性，从而破坏其绑定。

**如何使用：** 调用 `filterCaseSensitivity()` 读取当前值；它不会修改应用状态。

### `[bindable] filterKeyColumn : int`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性包含用于过滤源模型内容的关键字的读取列。
默认值为0。如果值为-1，则所有列的键都会读取。

**如何使用：** 调用 `filterKeyColumn()` 读取当前值；它不会修改应用状态。

### `[bindable] filterRegularExpression : QRegularExpression`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性包含用于过滤源模型内容的`QRegularExpression`。
通过`QRegularExpression`重载设置该属性会覆盖当前`filterCaseSensitivity`。默认情况下，`QRegularExpression`是一个空字符串，所有内容都匹配。
如果没有设置`QRegularExpression`或字符串为空，源模型中的所有信息都会被接受。
注意：设置该属性会将新正则表达式的大小写敏感性传播到`filterCaseSensitivity`属性，从而破坏其绑定。同样，显式设置`filterCaseSensitivity`会改变当前正则表达式的大小写敏感性，从而破坏其绑定。

**如何使用：** 调用 `filterRegularExpression()` 读取当前值；它不会修改应用状态。

### `[bindable] filterRole : int`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性保留了用于查询源模型数据的项目角色，用于筛选项目时。
默认值是`Qt::DisplayRole`。

**如何使用：** 调用 `filterRole()` 读取当前值；它不会修改应用状态。

### `[bindable] isSortLocaleAware : bool`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性保留了用于排序时用于比较字符串的局部感知设置。
默认情况下，排序不具备本地感知能力。

**如何使用：** 调用 `isSortLocaleAware()` 读取当前值；它不会修改应用状态。

### `[bindable] recursiveFilteringEnabled : bool`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性决定是否将滤波器递归应用于子节点，对于任意匹配的子节点，其父节点也会被可见。
默认值为假。

**如何使用：** 调用 `recursiveFilteringEnabled()` 读取当前值；它不会修改应用状态。

### `[bindable] sortCaseSensitivity : Qt::CaseSensitivity`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性表示了用于排序时用于比较字符串的大小写敏感性设置。
默认情况下，排序是区分大小写的。

**如何使用：** 调用 `sortCaseSensitivity()` 读取当前值；它不会修改应用状态。

### `[bindable] sortRole : int`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性包含用于查询源模型数据的项目角色，用于排序物品。
默认值是`Qt::DisplayRole`。

**如何使用：** 调用 `sortRole()` 读取当前值；它不会修改应用状态。

### `[explicit] QSortFilterProxyModel::QSortFilterProxyModel(QObject *parent = nullptr)`

**作用与语义：**

基于给定`parent`构造一个排序滤波器模型。

### `[virtual noexcept] QSortFilterProxyModel::~QSortFilterProxyModel()`

**作用与语义：**

破坏了这种排序过滤器模型。

### `[signal, since 6.0] void QSortFilterProxyModel::autoAcceptChildRowsChanged(bool autoAcceptChildRows)`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
如果成立，代理模型不会过滤掉被接受行的子节点，即使这些子节点本身也会被过滤掉。
默认值为假。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `autoAcceptChildRows` 的变化，不要把它当作普通函数主动调用。

### `[protected, since 6.9] void QSortFilterProxyModel::beginFilterChange()`

**作用与语义：**

准备更换滤网。
如果你正在实现自定义过滤（例如 `filterAcceptsRow()`），并且你的过滤参数即将被更改，应该调用这个函数。
一旦过滤器被更改，调用`endFilterChange()`，表示行过滤器时`Direction::Rows`，列过滤器时`Direction::Columns`，或者 `Direction::Columns`|`Direction::Rows`如果行和列都被过滤。

**官方示例：**

```cpp
 void MySortFilterProxyModel::setFilterMaximumDate(QDate date)
 {
     beginFilterChange();
     maxDate = date;
     endFilterChange(QSortFilterProxyModel::Direction::Rows);
 }
```

### `[override virtual] QModelIndex QSortFilterProxyModel::buddy(const QModelIndex &index) const`

**作用与语义：**

重实现自：`QAbstractProxyModel::buddy`（const QModelIndex & index） const.

### `[override virtual] bool QSortFilterProxyModel::canFetchMore(const QModelIndex &parent) const`

**作用与语义：**

重实现自：`QAbstractProxyModel::canFetchMore`（const QModelIndex &parent） const.

### `[override virtual] int QSortFilterProxyModel::columnCount(const QModelIndex &parent = QModelIndex()) const`

**作用与语义：**

重实现自：`QAbstractItemModel::columnCount`（const QModelIndex 和 parent） const.
返回给定`parent`子节点的列数。
在大多数子类中，列的数量与`parent`无关。
注意：在实现基于表的模型时，当父模型有效时，columnCount() 应返回 0。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[override virtual] QVariant QSortFilterProxyModel::data(const QModelIndex &index, int role = Qt::DisplayRole) const`

**作用与语义：**

重实现自：`QAbstractProxyModel::data`（const QModelIndex &proxyIndex， int role） const.

### `[override virtual] bool QSortFilterProxyModel::dropMimeData(const QMimeData *data, Qt::DropAction action, int row, int column, const QModelIndex &parent)`

**作用与语义：**

重实现自：`QAbstractProxyModel::dropMimeData`（const QMimeData *data， Qt：:D ropAction action， int row， int column， const QModelIndex &parent）.

### `[protected, since 6.10] void QSortFilterProxyModel::endFilterChange(QSortFilterProxyModel::Directions directions = Direction::Both)`

**作用与语义：**

在滤波参数变更后，当前的过滤无效。
如果你实现了自定义过滤（例如`filterAcceptsRow()`），且过滤器参数发生了变化，应调用这个函数。`directions`参数指定自定义过滤器是影响行、列还是两者。
当滤波器参数即将变更时调用`beginFilterChange()`，并在滤波器参数更改后调用该函数。调用时，`directions`设置为`Direction::Rows`用于行滤波器（即实现了`filterAcceptsRow()`），列滤波器`Direction::Columns`（即实现了`filterAcceptsColumn()`），如果两个滤波器函数都实现了，则`Direction::Both`。

### `[override virtual] void QSortFilterProxyModel::fetchMore(const QModelIndex &parent)`

**作用与语义：**

重实现自：`QAbstractProxyModel::fetchMore`（const QModelIndex & parent）。

### `[virtual protected] bool QSortFilterProxyModel::filterAcceptsColumn(int source_column, const QModelIndex &source_parent) const`

**作用与语义：**

如果列中由给定`source_column`和`source_parent`应包含在模型中，返回`true`;否则返回`false`。
注意：默认实现总是返回`true`。您必须重新实现该方法才能获得描述的行为。

### `[virtual protected] bool QSortFilterProxyModel::filterAcceptsRow(int source_row, const QModelIndex &source_parent) const`

**作用与语义：**

如果给定`source_row`和`source_parent`所示的行中的项目应包含在模型中，返回`true`;否则返回 false。
默认实现返回`true`，如果相关项所持有的值与过滤字符串、万用符字符串或正则表达式匹配。
注意：默认情况下，`Qt::DisplayRole`用于判断该行是否应被接受。这可以通过设置`filterRole`属性来更改。

### `[signal] void QSortFilterProxyModel::filterCaseSensitivityChanged(Qt::CaseSensitivity filterCaseSensitivity)`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性表示了用于过滤源模型内容的`QRegularExpression`模式的大小写敏感性。
默认情况下，滤波器是区分大小写的。
注意：设置该属性会将新的大小写敏感性传播到`filterRegularExpression`属性，从而破坏其绑定。同样，显式设置`filterRegularExpression`会改变当前大小写敏感性，从而破坏其绑定。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `filterCaseSensitivity` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QSortFilterProxyModel::filterRoleChanged(int filterRole)`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性保留了用于查询源模型数据的项目角色，用于筛选项目时。
默认值是`Qt::DisplayRole`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `filterRole` 的变化，不要把它当作普通函数主动调用。

### `[override virtual] Qt::ItemFlags QSortFilterProxyModel::flags(const QModelIndex &index) const`

**作用与语义：**

重实现自：`QAbstractProxyModel::flags`（const QModelIndex & index） const.

### `[override virtual] bool QSortFilterProxyModel::hasChildren(const QModelIndex &parent = QModelIndex()) const`

**作用与语义：**

重实现自：`QAbstractProxyModel::hasChildren`（const QModelIndex 和 parent） const.

### `[override virtual] QVariant QSortFilterProxyModel::headerData(int section, Qt::Orientation orientation, int role = Qt::DisplayRole) const`

**作用与语义：**

重实现自：`QAbstractProxyModel::headerData`（整数节，Qt：：Orientation orientation， int role）const.

### `[override virtual] QModelIndex QSortFilterProxyModel::index(int row, int column, const QModelIndex &parent = QModelIndex()) const`

**作用与语义：**

重实现自：`QAbstractItemModel::index`（整数行，整数列，cont QModelIndex 和parent）const.
返回由给定`row`、`column`和`parent`索引指定模型中项目的索引。
在子类中重新实现该函数时，调用 `createIndex()` 生成模型索引，其他组件可以用来引用模型中的项。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[override virtual] bool QSortFilterProxyModel::insertColumns(int column, int count, const QModelIndex &parent = QModelIndex())`

**作用与语义：**

重实现自：`QAbstractItemModel::insertColumns`（整数列，整数计数，条件QModelIndex和parent）。
支持该方法的模型会在给定`column`之前插入`count`列。每个新列中的项都是`parent`模型索引所表示项的子项。
如果`column`为0，列会加在任何已有列之前。
如果`column`是`columnCount()`，则这些列会附加到任何已有的列上。
如果`parent`没有子节点，则插入一行，列`count`。
如果列成功插入，返回`true`;否则返回`false`。
基类实现什么都不做，返回`false`。
如果你实现了自己的模型，如果你想支持插入，可以重新实现这个函数。或者，你也可以提供自己的 API 来修改数据。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[override virtual] bool QSortFilterProxyModel::insertRows(int row, int count, const QModelIndex &parent = QModelIndex())`

**作用与语义：**

重实现自：`QAbstractItemModel::insertRows`（整数行，整数计数，cont QModelIndex 和父）。
注意：该函数的基类实现不做任何操作，返回`false`。
支持此操作的模型会在给定`row`之前插入`count`行。新行中的项将是`parent`模型索引所表示项的子项。
如果`row`为0，则这些行会在父行中的任何已有行之前加。
如果`row` `rowCount()`，则这些行会附加到父行中已有的行上。
如果`parent`没有子节点，则插入一列`count`行。
如果行成功插入，返回`true`;否则返回`false`。
如果你实现了自己的模型，如果你想支持插入，可以重新实现这个函数。或者，你也可以提供自己的 API 来修改数据。无论哪种情况，你都需要调用 `beginInsertRows()` 和 `endInsertRows()`，通知其他组件模型已更改。
注意：该函数可以通过元对象系统和QML调用。参见 `Q_INVOKABLE`。

### `[slot] void QSortFilterProxyModel::invalidate()`

**作用与语义：**

使当前的排序和过滤失效。

### `[protected, since 6.0, until 6.13] void QSortFilterProxyModel::invalidateColumnsFilter()`

**作用与语义：**

该函数计划在 6.13 版本中弃用。
改用`beginFilterChange()`和`endFilterChange`（`Direction::Rows`）。
使当前列的过滤失效。
如果你实现了自定义过滤（`filterAcceptsColumn()`），并且你的过滤参数发生了变化，应该调用这个函数。这和`invalidateFilter()`不同，它不会调用`filterAcceptsRow()`，只调用`filterAcceptsColumn()`。如果你想隐藏或显示行不变的列，可以用这个代替`invalidateFilter()`。
在滤波参数改变之前，先打电话给`beginFilterChange()`。

### `[protected, until 6.13] void QSortFilterProxyModel::invalidateFilter()`

**作用与语义：**

该函数计划在 6.13 版本中弃用。
改用`beginFilterChange()`和`endFilterChange()`。
使当前的过滤失效。
如果你实现了自定义过滤（例如 `filterAcceptsRow()`），并且滤波参数发生了变化，应该调用这个函数。
在滤网参数改变之前，先打电话给`beginFilterChange()`。

**官方示例：**

```cpp
 void MySortFilterProxyModel::setFilterMaximumDate(QDate date)
 {
     beginFilterChange();
     maxDate = date;
     endFilterChange(QSortFilterProxyModel::Direction::Rows);
 }
```

### `[protected, since 6.0, until 6.13] void QSortFilterProxyModel::invalidateRowsFilter()`

**作用与语义：**

该函数计划在 6.13 版本中弃用。
改用`beginFilterChange()`和`endFilterChange`（`Direction::Columns`）。
使当前行的过滤失效。
如果你实现了自定义过滤（通过 `filterAcceptsRow()`），并且你的过滤参数发生了变化，应该调用这个函数。这和 `invalidateFilter()` 不同，它不会调用 `filterAcceptsColumn()`，只调用 `filterAcceptsRow()`。如果你想隐藏或显示列不变的行，可以用这个代替 `invalidateFilter()`。
在你的过滤器参数改变之前，先打电话给`beginFilterChange()`。

### `[virtual protected] bool QSortFilterProxyModel::lessThan(const QModelIndex &source_left, const QModelIndex &source_right) const`

**作用与语义：**

如果给定索引`source_left`所引用的项值小于该索引`source_right`所引用项项的值，则返回`true`，否则返回`false`。
该函数作为排序时的<操作符，处理以下`QVariant`类型：
- `QMetaType::Int`
- `QMetaType::UInt`
- `QMetaType::LongLong`
- `QMetaType::ULongLong`
- `QMetaType::Float`
- `QMetaType::Double`
- `QMetaType::QChar`
- `QMetaType::QDate`
- `QMetaType::QTime`
- `QMetaType::QDateTime`
- `QMetaType::QString`
其他类型会用`QVariant::toString()`转换成`QString`。
`QString`的比较默认是区分大小写的;这可以通过`sortCaseSensitivity`属性进行更改。
默认情况下，比较时使用与 `QModelIndex`es 关联的 `Qt::DisplayRole`。这可以通过设置 `sortRole` 属性来更改。
注意：传递的索引对应源模型。

### `[override virtual] QModelIndex QSortFilterProxyModel::mapFromSource(const QModelIndex &sourceIndex) const`

**作用与语义：**

重实现自：`QAbstractProxyModel::mapFromSource`（const QModelIndex & sourceIndex） const.
返回给定源模型`sourceIndex`的`QSortFilterProxyModel`中的模型索引。
重新实现该函数，返回代理模型中对应源模型`sourceIndex`的模型索引。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[override virtual] QItemSelection QSortFilterProxyModel::mapSelectionFromSource(const QItemSelection &sourceSelection) const`

**作用与语义：**

Reimpments： `QAbstractProxyModel::mapSelectionFromSource`（const QItemSelection &sourceSelection） const.
返回从指定 `sourceSelection`映射的代理选择。
重新实现此方法，将源选择映射到代理选择。
注意：该函数可通过元对象系统和QML调用。参见 `Q_INVOKABLE`。

### `[override virtual] QItemSelection QSortFilterProxyModel::mapSelectionToSource(const QItemSelection &proxySelection) const`

**作用与语义：**

Reimpments： `QAbstractProxyModel::mapSelectionToSource`（const QItemSelection &proxySelection） const.
返回从指定`proxySelection`映射的源选择。
重新实现该方法，将代理选择映射到源选择。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[override virtual] QModelIndex QSortFilterProxyModel::mapToSource(const QModelIndex &proxyIndex) const`

**作用与语义：**

重实现自：`QAbstractProxyModel::mapToSource`（const QModelIndex & proxyIndex） const.
返回对应给定`proxyIndex`的源模型索引，该索引来自排序滤波器模型。
重新实现该函数，返回源模型中对应代理模型`proxyIndex`的模型索引。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[override virtual] QModelIndexList QSortFilterProxyModel::match(const QModelIndex &start, int role, const QVariant &value, int hits = 1, Qt::MatchFlags flags = Qt::MatchFlags(Qt::MatchStartsWith|Qt::MatchWrap)) const`

**作用与语义：**

重实现自：`QAbstractItemModel::match`（const QModelIndex &start， int role， const QVariant &value， int hits， Qt：：MatchFlags flags） const.
返回`start`索引列中存储在指定`value`下的数据与`role`匹配的项的索引列表。搜索的执行方式由给出的`flags`定义。返回的列表可能是空的。还请注意，如果使用代理模型，列表中结果的顺序可能与模型中的顺序不一致。结果的顺序不能被依赖。
搜索从`start`索引开始，持续直到匹配数据项数达到`hits`，搜索到达最后一行，或再次达到`start`——具体取决于`flags`中是否指定了`MatchWrap`。如果你想搜索所有匹配的项目，使用`hits` = -1。
默认情况下，该函数会对所有项目进行环绕、基于字符串的比较，搜索以`value`指定搜索词开头的项目。
注意：该函数的默认实现仅搜索列。重新实现该函数以包含不同的搜索行为。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[override virtual] QMimeData *QSortFilterProxyModel::mimeData(const QModelIndexList &indexes) const`

**作用与语义：**

重实现自：`QAbstractProxyModel::mimeData`（const QModelIndexList & indexes） const.

### `[override virtual] QStringList QSortFilterProxyModel::mimeTypes() const`

**作用与语义：**

重装：`QAbstractProxyModel::mimeTypes()` const.

### `[override virtual] QModelIndex QSortFilterProxyModel::parent(const QModelIndex &child) const`

**作用与语义：**

重实现自：`QAbstractItemModel::parent`（const QModelIndex & index） const.
返回模型项目的父项，并返回给定`index`。如果该项没有父项，则返回无效`QModelIndex`。
在暴露树状数据结构的模型中，一个常用的惯例是只有第一列的项有子节点。在这种情况下，在子类中重新实现该函数时，返回`QModelIndex`的列将为0。
在将该函数重新实现到子类中时，要注意避免调用`QModelIndex`成员函数，如`QModelIndex::parent()`，因为属于你模型的索引会直接调用你的实现，导致无限递归。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[signal] void QSortFilterProxyModel::recursiveFilteringEnabledChanged(bool recursiveFilteringEnabled)`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性决定是否将滤波器递归应用于子节点，对于任意匹配的子节点，其父节点也会被可见。
默认值为假。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `recursiveFilteringEnabled` 的变化，不要把它当作普通函数主动调用。

### `[override virtual] bool QSortFilterProxyModel::removeColumns(int column, int count, const QModelIndex &parent = QModelIndex())`

**作用与语义：**

重构：`QAbstractItemModel::removeColumns`（整数列，整数计数，函数QModelIndex 和parent）。
在支持此功能的模型中，会从模型中移除`count`列，起始于父 `parent` 下给定`column`。
如果列被成功移除，返回 返回`true`;否则返回 `false`。
基类实现什么都不做，只返回`false`。
如果你实现了自己的模型，如果你想支持删除，可以重新实现这个函数。或者，你也可以提供自己的 API 来修改数据。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[override virtual] bool QSortFilterProxyModel::removeRows(int row, int count, const QModelIndex &parent = QModelIndex())`

**作用与语义：**

重实现自：`QAbstractItemModel::removeRows`（整数行，整数计数，函数QModelIndex 和父）。
在支持此功能的模型中，会从模型中移除父`parent`下以给定`row`为起始的`count`行。
如果行被成功移除，返回`true`;否则返回`false`。
基类实现什么都不做，只返回`false`。
如果你实现了自己的模型，如果你想支持删除，可以重新实现这个函数。或者，你也可以提供自己的 API 来修改数据。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[override virtual] int QSortFilterProxyModel::rowCount(const QModelIndex &parent = QModelIndex()) const`

**作用与语义：**

重实现自：`QAbstractItemModel::rowCount`（const QModelIndex & parent）const.
返回给定`parent`下的行数。当父节点有效时，表示 rowCount 返回的是父节点的子节点数。
注意：在实现基于表的模型时，当父模型有效时，rowCount() 应返回 0。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[override virtual] bool QSortFilterProxyModel::setData(const QModelIndex &index, const QVariant &value, int role = Qt::EditRole)`

**作用与语义：**

重实现自：`QAbstractProxyModel::setData`（const QModelIndex & index，const QVariant & value，int role）。

### `[slot] void QSortFilterProxyModel::setFilterFixedString(const QString &pattern)`

**作用与语义：**

将用于过滤源模型内容的固定字符串设置为给定`pattern`。
该方法会重置正则表达式选项，但尊重大小写区分。
注意：调用此方法会更新正则表达式，从而破坏`filterRegularExpression`的绑定。但对`filterCaseSensitivity`绑定没有影响。

### `[slot] void QSortFilterProxyModel::setFilterRegularExpression(const QString &pattern)`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性包含用于过滤源模型内容的`QRegularExpression`。
通过`QRegularExpression`重载设置该属性会覆盖当前`filterCaseSensitivity`。默认情况下，`QRegularExpression`是一个空字符串，所有内容都匹配。
如果没有设置`QRegularExpression`或字符串为空，源模型中的所有信息都会被接受。
注意：设置该属性会将新正则表达式的大小写敏感性传播到`filterCaseSensitivity`属性，从而破坏其绑定。同样，显式设置`filterCaseSensitivity`会改变当前正则表达式的大小写敏感性，从而破坏其绑定。

**如何使用：** 调用 `setFilterRegularExpression(...)` 修改 `filterRegularExpression`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `[slot] void QSortFilterProxyModel::setFilterWildcard(const QString &pattern)`

**作用与语义：**

将用于过滤源模型内容的万用符表达式设置为给定的`pattern`。
该方法会重置正则表达式选项，但尊重大小写区分。
注意：调用该方法会更新正则表达式，从而破坏`filterRegularExpression`的绑定。但对`filterCaseSensitivity`绑定没有影响。

### `[override virtual] bool QSortFilterProxyModel::setHeaderData(int section, Qt::Orientation orientation, const QVariant &value, int role = Qt::EditRole)`

**作用与语义：**

重实现自：`QAbstractProxyModel::setHeaderData`（整数部分，Qt：：Orientation orientation，const QVariant & value，整数角色）。

### `[override virtual] void QSortFilterProxyModel::setSourceModel(QAbstractItemModel *sourceModel)`

**作用与语义：**

重实现自：`QAbstractProxyModel::setSourceModel`（QAbstractItemModel *sourceModel）。
注意：此特性支持`QProperty`绑定。
该属性表示该代理模型的源模型。
注意：这是一个私有信号。它可以用于信号连接，但用户不能发射。

### `[override virtual] QModelIndex QSortFilterProxyModel::sibling(int row, int column, const QModelIndex &idx) const`

**作用与语义：**

重实现自：`QAbstractProxyModel::sibling`（int 行，int column，const QModelIndex &idx） const.

### `[override virtual] void QSortFilterProxyModel::sort(int column, Qt::SortOrder order = Qt::AscendingOrder)`

**作用与语义：**

重实现自：`QAbstractProxyModel::sort`（整数列，Qt：：排序顺序）。
按给定`order`中的`column`排序模型。如果排序`column`小于零，模型将按给定`order`中的源模型行排序。

### `[signal] void QSortFilterProxyModel::sortCaseSensitivityChanged(Qt::CaseSensitivity sortCaseSensitivity)`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性表示了用于排序时用于比较字符串的大小写敏感性设置。
默认情况下，排序是区分大小写的。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `sortCaseSensitivity` 的变化，不要把它当作普通函数主动调用。

### `int QSortFilterProxyModel::sortColumn() const`

**作用与语义：**

返回当前用于排序的列。
返回最近使用的排序列。默认值为 -1，意味着该代理模型不进行排序。

### `[signal] void QSortFilterProxyModel::sortLocaleAwareChanged(bool sortLocaleAware)`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性保留了用于排序时用于比较字符串的局部感知设置。
默认情况下，排序不具备本地感知能力。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `isSortLocaleAware` 的变化，不要把它当作普通函数主动调用。

### `Qt::SortOrder QSortFilterProxyModel::sortOrder() const`

**作用与语义：**

返回当前用于排序的顺序。
这会返回最近使用的排序顺序。默认值是`Qt::AscendingOrder`。

### `[signal] void QSortFilterProxyModel::sortRoleChanged(int sortRole)`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性包含用于查询源模型数据的项目角色，用于排序物品。
默认值是`Qt::DisplayRole`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `sortRole` 的变化，不要把它当作普通函数主动调用。

### `[override virtual] QSize QSortFilterProxyModel::span(const QModelIndex &index) const`

**作用与语义：**

重实现自：`QAbstractProxyModel::span`（const QModelIndex & index） const.

### `[override virtual] Qt::DropActions QSortFilterProxyModel::supportedDropActions() const`

**作用与语义：**

重装：`QAbstractProxyModel::supportedDropActions()` const.

### `(since 6.10) enum class Direction { Rows, Columns, Both }`

**作用与语义：**

该枚举用于指定当滤波器参数变更时，自定义滤波器的适用方向。
- `QSortFilterProxyModel::Direction::Rows`：`0x01`;滤波器适用于`rows`
- `QSortFilterProxyModel::Direction::Columns`：`0x02`;滤波器适用于`columns`
- `QSortFilterProxyModel::Direction::Both`：`Rows | Columns`;过滤器适用于行和列
这个枚举是在Qt 6.10引入的。
Directions 类型是 QFlags 的 typedef<Direction>。它存储 Direction 值的 OR 组合。

### `flags Directions`

**作用与语义：**

该枚举用于指定当滤波器参数变更时，自定义滤波器的适用方向。
- `QSortFilterProxyModel::Direction::Rows`：`0x01`;滤波器适用于`rows`
- `QSortFilterProxyModel::Direction::Columns`：`0x02`;滤波器适用于`columns`
- `QSortFilterProxyModel::Direction::Both`：`Rows | Columns`;过滤器适用于行和列
这个枚举是在Qt 6.10引入的。
Directions 类型是 QFlags 的 typedef<Direction>。它存储 Direction 值的 OR 组合。

### `bool autoAcceptChildRows() const`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
如果成立，代理模型不会过滤掉被接受行的子节点，即使这些子节点本身也会被过滤掉。
默认值为假。

**如何使用：** 调用 `autoAcceptChildRows()` 读取当前值；它不会修改应用状态。

### `QBindable<bool> bindableAutoAcceptChildRows()`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
如果成立，代理模型不会过滤掉被接受行的子节点，即使这些子节点本身也会被过滤掉。
默认值为假。

**如何使用：** 调用 `bindableAutoAcceptChildRows()` 取得 `autoAcceptChildRows` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `QBindable<bool> bindableDynamicSortFilter()`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性适用于代理模型在源模型内容变化时是否动态排序和过滤。
注意，当dynamicSortFilter为真时，不应通过代理模型更新源模型。例如，如果你在`QComboBox`上设置代理模型，使用更新模型的函数，如`addItem()`，将无法如预期般工作。另一种方法是将dynamicSortFilter设为false，添加`QComboBox`项后调用`sort()`。
默认值为真。

**如何使用：** 调用 `bindableDynamicSortFilter()` 取得 `dynamicSortFilter` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `QBindable<Qt::CaseSensitivity> bindableFilterCaseSensitivity()`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性表示了用于过滤源模型内容的`QRegularExpression`模式的大小写敏感性。
默认情况下，滤波器是区分大小写的。
注意：设置该属性会将新的大小写敏感性传播到`filterRegularExpression`属性，从而破坏其绑定。同样，显式设置`filterRegularExpression`会改变当前大小写敏感性，从而破坏其绑定。

**如何使用：** 调用 `bindableFilterCaseSensitivity()` 取得 `filterCaseSensitivity` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `QBindable<int> bindableFilterKeyColumn()`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性包含用于过滤源模型内容的关键字的读取列。
默认值为0。如果值为-1，则所有列的键都会读取。

**如何使用：** 调用 `bindableFilterKeyColumn()` 取得 `filterKeyColumn` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `QBindable<QRegularExpression> bindableFilterRegularExpression()`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性包含用于过滤源模型内容的`QRegularExpression`。
通过`QRegularExpression`重载设置该属性会覆盖当前`filterCaseSensitivity`。默认情况下，`QRegularExpression`是一个空字符串，所有内容都匹配。
如果没有设置`QRegularExpression`或字符串为空，源模型中的所有信息都会被接受。
注意：设置该属性会将新正则表达式的大小写敏感性传播到`filterCaseSensitivity`属性，从而破坏其绑定。同样，显式设置`filterCaseSensitivity`会改变当前正则表达式的大小写敏感性，从而破坏其绑定。

**如何使用：** 调用 `bindableFilterRegularExpression()` 取得 `filterRegularExpression` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `QBindable<int> bindableFilterRole()`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性保留了用于查询源模型数据的项目角色，用于筛选项目时。
默认值是`Qt::DisplayRole`。

**如何使用：** 调用 `bindableFilterRole()` 取得 `filterRole` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `QBindable<bool> bindableIsSortLocaleAware()`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性保留了用于排序时用于比较字符串的局部感知设置。
默认情况下，排序不具备本地感知能力。

**如何使用：** 调用 `bindableIsSortLocaleAware()` 取得 `isSortLocaleAware` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `QBindable<bool> bindableRecursiveFilteringEnabled()`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性决定是否将滤波器递归应用于子节点，对于任意匹配的子节点，其父节点也会被可见。
默认值为假。

**如何使用：** 调用 `bindableRecursiveFilteringEnabled()` 取得 `recursiveFilteringEnabled` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `QBindable<Qt::CaseSensitivity> bindableSortCaseSensitivity()`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性表示了用于排序时用于比较字符串的大小写敏感性设置。
默认情况下，排序是区分大小写的。

**如何使用：** 调用 `bindableSortCaseSensitivity()` 取得 `sortCaseSensitivity` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `QBindable<int> bindableSortRole()`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性包含用于查询源模型数据的项目角色，用于排序物品。
默认值是`Qt::DisplayRole`。

**如何使用：** 调用 `bindableSortRole()` 取得 `sortRole` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `bool dynamicSortFilter() const`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性适用于代理模型在源模型内容变化时是否动态排序和过滤。
注意，当dynamicSortFilter为真时，不应通过代理模型更新源模型。例如，如果你在`QComboBox`上设置代理模型，使用更新模型的函数，如`addItem()`，将无法如预期般工作。另一种方法是将dynamicSortFilter设为false，添加`QComboBox`项后调用`sort()`。
默认值为真。

**如何使用：** 调用 `dynamicSortFilter()` 读取当前值；它不会修改应用状态。

### `Qt::CaseSensitivity filterCaseSensitivity() const`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性表示了用于过滤源模型内容的`QRegularExpression`模式的大小写敏感性。
默认情况下，滤波器是区分大小写的。
注意：设置该属性会将新的大小写敏感性传播到`filterRegularExpression`属性，从而破坏其绑定。同样，显式设置`filterRegularExpression`会改变当前大小写敏感性，从而破坏其绑定。

**如何使用：** 调用 `filterCaseSensitivity()` 读取当前值；它不会修改应用状态。

### `int filterKeyColumn() const`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性包含用于过滤源模型内容的关键字的读取列。
默认值为0。如果值为-1，则所有列的键都会读取。

**如何使用：** 调用 `filterKeyColumn()` 读取当前值；它不会修改应用状态。

### `QRegularExpression filterRegularExpression() const`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性包含用于过滤源模型内容的`QRegularExpression`。
通过`QRegularExpression`重载设置该属性会覆盖当前`filterCaseSensitivity`。默认情况下，`QRegularExpression`是一个空字符串，所有内容都匹配。
如果没有设置`QRegularExpression`或字符串为空，源模型中的所有信息都会被接受。
注意：设置该属性会将新正则表达式的大小写敏感性传播到`filterCaseSensitivity`属性，从而破坏其绑定。同样，显式设置`filterCaseSensitivity`会改变当前正则表达式的大小写敏感性，从而破坏其绑定。

**如何使用：** 调用 `filterRegularExpression()` 读取当前值；它不会修改应用状态。

### `int filterRole() const`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性保留了用于查询源模型数据的项目角色，用于筛选项目时。
默认值是`Qt::DisplayRole`。

**如何使用：** 调用 `filterRole()` 读取当前值；它不会修改应用状态。

### `bool isRecursiveFilteringEnabled() const`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性决定是否将滤波器递归应用于子节点，对于任意匹配的子节点，其父节点也会被可见。
默认值为假。

**如何使用：** 调用 `isRecursiveFilteringEnabled()` 读取当前值；它不会修改应用状态。

### `bool isSortLocaleAware() const`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性保留了用于排序时用于比较字符串的局部感知设置。
默认情况下，排序不具备本地感知能力。

**如何使用：** 调用 `isSortLocaleAware()` 读取当前值；它不会修改应用状态。

### `void setAutoAcceptChildRows(bool accept)`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
如果成立，代理模型不会过滤掉被接受行的子节点，即使这些子节点本身也会被过滤掉。
默认值为假。

**如何使用：** 调用 `setAutoAcceptChildRows(...)` 修改 `autoAcceptChildRows`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setDynamicSortFilter(bool enable)`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性适用于代理模型在源模型内容变化时是否动态排序和过滤。
注意，当dynamicSortFilter为真时，不应通过代理模型更新源模型。例如，如果你在`QComboBox`上设置代理模型，使用更新模型的函数，如`addItem()`，将无法如预期般工作。另一种方法是将dynamicSortFilter设为false，添加`QComboBox`项后调用`sort()`。
默认值为真。

**如何使用：** 调用 `setDynamicSortFilter(...)` 修改 `dynamicSortFilter`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setFilterCaseSensitivity(Qt::CaseSensitivity cs)`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性表示了用于过滤源模型内容的`QRegularExpression`模式的大小写敏感性。
默认情况下，滤波器是区分大小写的。
注意：设置该属性会将新的大小写敏感性传播到`filterRegularExpression`属性，从而破坏其绑定。同样，显式设置`filterRegularExpression`会改变当前大小写敏感性，从而破坏其绑定。

**如何使用：** 调用 `setFilterCaseSensitivity(...)` 修改 `filterCaseSensitivity`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setFilterKeyColumn(int column)`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性包含用于过滤源模型内容的关键字的读取列。
默认值为0。如果值为-1，则所有列的键都会读取。

**如何使用：** 调用 `setFilterKeyColumn(...)` 修改 `filterKeyColumn`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setFilterRole(int role)`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性保留了用于查询源模型数据的项目角色，用于筛选项目时。
默认值是`Qt::DisplayRole`。

**如何使用：** 调用 `setFilterRole(...)` 修改 `filterRole`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setRecursiveFilteringEnabled(bool recursive)`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性决定是否将滤波器递归应用于子节点，对于任意匹配的子节点，其父节点也会被可见。
默认值为假。

**如何使用：** 调用 `setRecursiveFilteringEnabled(...)` 修改 `recursiveFilteringEnabled`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setSortCaseSensitivity(Qt::CaseSensitivity cs)`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性表示了用于排序时用于比较字符串的大小写敏感性设置。
默认情况下，排序是区分大小写的。

**如何使用：** 调用 `setSortCaseSensitivity(...)` 修改 `sortCaseSensitivity`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setSortLocaleAware(bool on)`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性保留了用于排序时用于比较字符串的局部感知设置。
默认情况下，排序不具备本地感知能力。

**如何使用：** 调用 `setSortLocaleAware(...)` 修改 `isSortLocaleAware`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setSortRole(int role)`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性包含用于查询源模型数据的项目角色，用于排序物品。
默认值是`Qt::DisplayRole`。

**如何使用：** 调用 `setSortRole(...)` 修改 `sortRole`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `Qt::CaseSensitivity sortCaseSensitivity() const`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性表示了用于排序时用于比较字符串的大小写敏感性设置。
默认情况下，排序是区分大小写的。

**如何使用：** 调用 `sortCaseSensitivity()` 读取当前值；它不会修改应用状态。

### `int sortRole() const`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性包含用于查询源模型数据的项目角色，用于排序物品。
默认值是`Qt::DisplayRole`。

**如何使用：** 调用 `sortRole()` 读取当前值；它不会修改应用状态。

### `void setFilterRegularExpression(const QRegularExpression &regularExpression)`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性包含用于过滤源模型内容的`QRegularExpression`。
通过`QRegularExpression`重载设置该属性会覆盖当前`filterCaseSensitivity`。默认情况下，`QRegularExpression`是一个空字符串，所有内容都匹配。
如果没有设置`QRegularExpression`或字符串为空，源模型中的所有信息都会被接受。
注意：设置该属性会将新正则表达式的大小写敏感性传播到`filterCaseSensitivity`属性，从而破坏其绑定。同样，显式设置`filterCaseSensitivity`会改变当前正则表达式的大小写敏感性，从而破坏其绑定。

**如何使用：** 调用 `setFilterRegularExpression(...)` 修改 `filterRegularExpression`；传入的新值会成为后续查询和相关界面行为所使用的值。

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

`QSortFilterProxyModel` 所属机制类型：模型/视图协议。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
