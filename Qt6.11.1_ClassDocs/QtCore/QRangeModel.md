# QRangeModel

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QRangeModel` 是 模型/视图协议 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QRangeModel` 是模型/视图体系中的数据模型类型，向视图提供索引、角色数据和结构变化通知。

**内部模型：** 视图不应该直接操作底层容器；它通过 QModelIndex 和 data roles 查询模型。模型必须准确维护索引有效性以及插入、删除、移动时的通知顺序。

**适用场景：** 需要把自定义数据接入 QListView、QTableView、QTreeView 或代理模型时使用。

**典型调用链：** 准备数据源 -> 实现/配置模型 -> 连接 view -> 通过 data/flags/setData 读写 -> 发出 dataChanged 或 begin/end 结构通知。

**先记住的坑：** 不要在 data() 中修改数据；不要返回过期索引；不要用全量 reset 代替精确结构通知，除非确实无法描述变化。

## 2. 依赖与对象关系

- 头文件：`#include <QRangeModel>`
- 继承自：QAbstractItemModel
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

- `(since 6.11) struct ItemAccess`
- `(since 6.10) struct RowOptions`
- `(since 6.11) enum class AutoConnectPolicy { None, Full, OnRead }`
- `enum class RowCategory { Default, MultiRoleItem }`

### 属性

- `(since 6.11) autoConnectPolicy : AutoConnectPolicy`
- `roleNames : QHash<int, QByteArray>`

### 公有函数

- `QRangeModel(Range &&range, QObject *parent = nullptr)`
- `QRangeModel(Range &&range, Protocol &&protocol, QObject *parent = nullptr)`
- `virtual ~QRangeModel() override`
- `QRangeModel::AutoConnectPolicy autoConnectPolicy() const`
- `void resetRoleNames()`
- `void setAutoConnectPolicy(QRangeModel::AutoConnectPolicy policy)`
- `void setRoleNames(const QHash<int, QByteArray> &names)`

### 重实现的公有函数

- `virtual QModelIndex buddy(const QModelIndex &index) const override`
- `virtual bool canDropMimeData(const QMimeData *data, Qt::DropAction action, int row, int column, const QModelIndex &parent) const override`
- `virtual bool canFetchMore(const QModelIndex &parent) const override`
- `virtual bool clearItemData(const QModelIndex &index) override`
- `virtual int columnCount(const QModelIndex &parent = {}) const override`
- `virtual QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const override`
- `virtual bool dropMimeData(const QMimeData *data, Qt::DropAction action, int row, int column, const QModelIndex &parent) override`
- `virtual void fetchMore(const QModelIndex &parent) override`
- `virtual Qt::ItemFlags flags(const QModelIndex &index) const override`
- `virtual bool hasChildren(const QModelIndex &parent = QModelIndex()) const override`
- `virtual QVariant headerData(int section, Qt::Orientation orientation, int role = Qt::DisplayRole) const override`
- `virtual QModelIndex index(int row, int column, const QModelIndex &parent = {}) const override`
- `virtual bool insertColumns(int column, int count, const QModelIndex &parent = {}) override`
- `virtual bool insertRows(int row, int count, const QModelIndex &parent = {}) override`
- `virtual QMap<int, QVariant> itemData(const QModelIndex &index) const override`
- `virtual QModelIndexList match(const QModelIndex &start, int role, const QVariant &value, int hits, Qt::MatchFlags flags) const override`
- `virtual QMimeData * mimeData(const QModelIndexList &indexes) const override`
- `virtual QStringList mimeTypes() const override`
- `virtual bool moveColumns(const QModelIndex &sourceParent, int sourceColumn, int count, const QModelIndex &destinationParent, int destinationColumn) override`
- `virtual bool moveRows(const QModelIndex &sourceParent, int sourceRow, int count, const QModelIndex &destinationParent, int destinationRow) override`
- `virtual void multiData(const QModelIndex &index, QModelRoleDataSpan roleDataSpan) const override`
- `virtual QModelIndex parent(const QModelIndex &child) const override`
- `virtual bool removeColumns(int column, int count, const QModelIndex &parent = {}) override`
- `virtual bool removeRows(int row, int count, const QModelIndex &parent = {}) override`
- `virtual QHash<int, QByteArray> roleNames() const override`
- `virtual int rowCount(const QModelIndex &parent = {}) const override`
- `virtual bool setData(const QModelIndex &index, const QVariant &data, int role = Qt::EditRole) override`
- `virtual bool setHeaderData(int section, Qt::Orientation orientation, const QVariant &data, int role = Qt::EditRole) override`
- `virtual bool setItemData(const QModelIndex &index, const QMap<int, QVariant> &data) override`
- `virtual QModelIndex sibling(int row, int column, const QModelIndex &index) const override`
- `virtual void sort(int column, Qt::SortOrder order = Qt::AscendingOrder) override`
- `virtual QSize span(const QModelIndex &index) const override`
- `virtual Qt::DropActions supportedDragActions() const override`
- `virtual Qt::DropActions supportedDropActions() const override`

### 信号

- `void autoConnectPolicyChanged(QRangeModel::AutoConnectPolicy policy)`
- `void roleNamesChanged()`

### 重实现的保护函数

- `virtual bool event(QEvent *event) override`
- `virtual bool eventFilter(QObject *object, QEvent *event) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[since 6.11] enum class QRangeModel::AutoConnectPolicy`

**作用与语义：**

该枚举定义了 `QRangeModel` 是否以及何时自动连接变换信号与模型`dataChanged()`信号的属性。只有与某个角色名称匹配的属性才会被连接。
- `QRangeModel::AutoConnectPolicy::None`：`0`;不会自动建立连接。
- `QRangeModel::AutoConnectPolicy::Full`：`1`;所有相关属性的信号都会自动连接，适用于所有`QObject`项。这包括`QObject`项添加到新插入的行和列。
- `QRangeModel::AutoConnectPolicy::OnRead`：`2`;相关属性的信号在模型首次读取该属性时连接起来。
创建自动连接的内存开销可能相当可观。全自动连接除了连接本身外，无需任何账务管理，但每个连接都占用内存，连接所有对象的所有属性可能成本很高，尤其是当只有部分对象的部分属性会改变时。
OnRead 连接策略不会连接到那些从未被读取的对象或属性（例如，从未在视图中渲染过），但记住已建立的连接需要一定的账务负担，并且内存随时间增长不可预测。例如，向下滚动一长串项目很容易产生成千上万的新连接。
这个枚举是在Qt 6.11引入的。

### `enum class QRangeModel::RowCategory`

**作用与语义：**

本列举说明了`QRangeModel`应如何呈现其所建造的系列元素。
- `QRangeModel::RowCategory::Default`：`0`;`QRangeModel`决定如何呈现行。
- `QRangeModel::RowCategory::MultiRoleItem`：`1`;`QRangeModel` 将带有元对象的物品呈现为多功能物品，同时在一维范围内使用时也是如此。
专门化你的类型的`RowOptions`模板，并添加一个包含该枚举值的公共成员变量`static constexpr auto rowCategory`。

### `[since 6.11] autoConnectPolicy : AutoConnectPolicy`

**作用与语义：**

当且当模型自动连接到属性时，通知发生变化。
如果`QRangeModel`运行在与其行或项类型相同类型的`QObject`子类的数据结构上，则可以自动将QObject的属性与`dataChanged()`信号连接起来。对于`QObject`行，对每列进行此操作，映射到`Qt::DisplayRole`属性。对于项目，则对与某个角色名称匹配的属性进行此操作。
默认情况下，该属性的值是`None`的，因此不会建立这样的连接。改变该属性的值总是会破坏所有现有的连接。
注意：如果`QRangeModel`操作的数据结构中的QObject被替换掉，连接不会被破坏或创建。

**如何使用：** 调用 `autoConnectPolicy()` 读取当前值；它不会修改应用状态。

### `roleNames : QHash<int, QByteArray>`

**作用与语义：**

该属性包含模型的角色名称。
如果该区间的所有列都属于同一类型，且该类型提供了元对象（即是小工具或`QObject`子类），那么该属性就包含该类型属性的名称，并将其映射到从`Qt::UserRole`开始`Qt::ItemDataRole`值的值。此外，角色“modelData”还提供对小工具或`QObject`实例的访问。
通过将该属性显式设置为非空映射来覆盖该默认行为。将该属性设置为空映射，或使用 resetRoleNames()，即可恢复默认行为。

**如何使用：** 调用 `roleNames()` 读取当前值；它不会修改应用状态。

### `[explicit] template < typename Range, typename Protocol, int = true > QRangeModel::QRangeModel(Range &&range, Protocol &&protocol, QObject *parent = nullptr)`

**作用与语义：**

构造一个`QRangeModel`实例，操作`range`中的数据。`range`必须是一个顺序范围，编译器通过参数相关查找找到`begin`和`end`重载，或者实现了`std::begin`和`std::end`。如果提供了`protocol`，模型将用协议实现表示该范围为树。模型实例成为`parent`的子。
`range`可以是指针或引用包装器，此时变异的模型API（如`setData()`或`insertRow()`）会修改被引用范围实例中的数据。如果`range`是一个值（或被移入模型），则连接到模型发出的信号，以响应数据的变化。
`QRangeModel`在构建过程中无法访问`range`。这使得在构造过程中，可以合法地将尚未完全构造的范围对象的指针或引用传递给该构造器，例如在子类QRangeModel时。
如果`range`被移入模型，那么模型销毁时，范围和所有数据都会被销毁。
注意：虽然模型在其他情况下不拥有距离对象的所有权，但一旦模型构建并传递给视图，你不得直接修改`range`。此类修改不会发出保持模型用户（其他模型或视图）与模型同步所需的信号，导致结果不一致、行为未定义和崩溃。使用`QRangeModelAdapter`安全地与底层范围交互，同时保持模型更新。

### `[override virtual noexcept] QRangeModel::~QRangeModel()`

**作用与语义：**

摧毁了`QRangeModel`。
模型构建的范围不被访问，只有当模型是从已搬入的范围构建时才会被销毁。

### `[override virtual] QModelIndex QRangeModel::buddy(const QModelIndex &index) const`

**作用与语义：**

重实现自：`QAbstractItemModel::buddy`（const QModelIndex & index） const.
返回由`index`表示的项目伙伴的模型索引。当用户想编辑某个项目时，视图会调用该函数检查是否应该编辑模型中的其他项目。然后，视图会利用伙伴项目返回的模型索引构建代理。
该功能的默认实现中，每个物品都是独立的伙伴。

### `[override virtual] bool QRangeModel::canDropMimeData(const QMimeData *data, Qt::DropAction action, int row, int column, const QModelIndex &parent) const`

**作用与语义：**

Reimplements： `QAbstractItemModel::canDropMimeData`（const QMimeData *data， Qt：:D ropAction action， int row， int column， const QModelIndex &parent） const.
返回`true`模型是否能接受`data`的删除。该默认实现仅检查`data` `mimeTypes()`列表中是否至少有一种格式，以及`action`是否在模型的`supportedDropActions()`中。
如果你想测试`data`是否能在`row`、`column`、`parent`时丢弃，可以用`action`重新实现这个函数。如果你不需要这个测试，就没必要重写这个函数。

### `[override virtual] bool QRangeModel::canFetchMore(const QModelIndex &parent) const`

**作用与语义：**

重实现自：`QAbstractItemModel::canFetchMore`（const QModelIndex &parent）const.
如果有更多数据可供 `parent`，返回`true`;否则返回 `false`。
默认实现总是返回`false`。
如果 canFetchMore() 返回 `true`，则应调用 `fetchMore()` 函数。这就是 `QAbstractItemView` 的行为，例如。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[override virtual] bool QRangeModel::clearItemData(const QModelIndex &index)`

**作用与语义：**

重现：`QAbstractItemModel::clearItemData`（const QModelIndex & index）。
将`index`区间存储的值替换为默认构造值。
对于运行在只读范围或实现C元组协议的行类型只读列的模型，该实现会立即返回`false`。
移除给定`index`中所有角色中存储的数据。如果成功返回`true`;否则返回`false`。如果数据被成功移除，应当发出`dataChanged()`信号。基类实现返回`false`。

### `[override virtual] int QRangeModel::columnCount(const QModelIndex &parent = {}) const`

**作用与语义：**

重实现自：`QAbstractItemModel::columnCount`（const QModelIndex 和 parent） const.
返回模型的列数。该函数对所有`parent`索引返回相同的值。
对于运行静态行类型的模型，返回的值在整个模型生命周期内始终相同。对于动态大小行类型的模型，模型返回第一行的项目数量，若模型没有行则返回0。
返回给定`parent`子节点的列数。
在大多数子类中，列数与`parent`无关。
注意：在实现基于表的模型时，当父模型有效时，columnCount() 应返回 0。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[override virtual] QVariant QRangeModel::data(const QModelIndex &index, int role = Qt::DisplayRole) const`

**作用与语义：**

重实现自：`QAbstractItemModel::data`（const QModelIndex & index， int role） const.
返回在给定`role`下存储的数据，且该值属于`index`所指范围内的值。
如果该索引的项类型是一个关联容器，从`int`、`Qt::ItemDataRole`或`QString`映射到`QVariant`，那么角色数据会在该容器中查找并返回。
如果该项目是小工具或`QObject`，则实现返回与`roleNames()`映射中`role`条目的属性值。
否则，实现返回由该项构造的 `QVariant` 通过 `QVariant::fromValue()` 对 `Qt::DisplayRole` 或 `Qt::EditRole`。对于其他角色，实现返回无效（默认构造）`QVariant`。
返回`index`所指项在指定`role`下存储的数据。
注意：如果你没有可返回的值，请返回一个无效（默认构造）的 `QVariant`。
注意：该函数可通过元对象系统和QML调用。参见 `Q_INVOKABLE`。

### `[override virtual] bool QRangeModel::dropMimeData(const QMimeData *data, Qt::DropAction action, int row, int column, const QModelIndex &parent)`

**作用与语义：**

Reimplementation s： `QAbstractItemModel::dropMimeData`（const QMimeData *data， Qt：:D ropAction action， int row， int column， const QModelIndex &parent）.
处理拖放操作提供的`data`，拖拽操作以给定`action`结束。
如果数据和动作由模型处理，返回`true`;否则返回`false`。
指定的`row`、`column`和`parent`表示操作结束时该项在模型中的位置。模型有责任在正确的位置完成动作。
例如，`QTreeView`中物品的投放动作可能导致新物品入，要么作为`row`、`column`和`parent`指定的物品的子项，要么作为该物品的兄弟姐妹。
当`row`和`column`为-1时，意味着丢弃的数据应被视为直接丢弃`parent`。通常这意味着将数据作为`parent`的子项附加。如果`row`和`column`大于或等于零，则表示丢弃发生在指定`parent`中指定的`row`和`column`之前。
调用`mimeTypes()`成员以获取可接受的MIME类型列表。该默认实现假设`mimeTypes()`的默认实现，返回单一默认MIME类型。如果你在自定义模型中重新实现`mimeTypes()`以返回多个MIME类型，必须重新实现该函数以利用它们。

### `[override virtual protected] bool QRangeModel::event(QEvent *event)`

**作用与语义：**

重实现自：`QObject::event`（QEvent *e）。
该虚拟函数接收对象事件，如果事件`e`被识别并处理，应返回真。
event() 函数可以重新实现，以自定义对象的行为。
确保你调用所有未处理的事件的父事件类实现。

### `[override virtual protected] bool QRangeModel::eventFilter(QObject *object, QEvent *event)`

**作用与语义：**

重实现自：`QObject::eventFilter`（QObject *已观看，QEvent *事件）。
如果该对象被安装为`watched`对象的事件过滤器，则过滤事件。
在你重新实现该函数时，如果你想过滤掉`event`，即停止进一步处理，返回 true;否则返回 false。
请注意，在上述示例中，未处理的事件会传递给基类的 eventFilter() 函数，因为基类可能为自身内部目的重新实现了 eventFilter()。
某些事件，如`QEvent::ShortcutOverride`，必须被明确接受（通过调用`accept()`来阻止传播）。
警告：如果你删除了该函数中的接收对象，请务必返回 true。否则，Qt 会将事件转发给已删除的对象，程序可能会崩溃。

### `[override virtual] void QRangeModel::fetchMore(const QModelIndex &parent)`

**作用与语义：**

重实现自：`QAbstractItemModel::fetchMore`（const QModelIndex & parent）。
获取由`parent`索引指定的父项目的任何可用数据。
如果你是逐步填充模型，请重新实现。
默认实现什么都不做。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[override virtual] Qt::ItemFlags QRangeModel::flags(const QModelIndex &index) const`

**作用与语义：**

重实现自：`QAbstractItemModel::flags`（const QModelIndex & index） const.
返回给定`index`的物品标记。
实现返回一组标志组合，使该项（`ItemIsEnabled`）和允许被选择（`ItemIsSelectable`）。对于运行在可变数据范围内的模型，它还设置了允许该项可编辑的标志（`ItemIsEditable`）。
返回给定`index`的物品标记。
基类实现返回一组标志，使该项（`ItemIsEnabled`）和允许被选择（`ItemIsSelectable`）。
注意：该函数可通过元对象系统和QML调用。参见 `Q_INVOKABLE`。

### `[override virtual] bool QRangeModel::hasChildren(const QModelIndex &parent = QModelIndex()) const`

**作用与语义：**

重实现自：`QAbstractItemModel::hasChildren`（const QModelIndex &parent） const.
如果`parent`有子女，返回`true`;否则返回`false`。
用`rowCount()`检测父母的子女数量。
注意，如果同一索引的标志被设置`Qt::ItemNeverHasChildren`，报告某个特定索引 hasChildren 是未定义行为。
注意：该函数可以通过元对象系统和QML调用。参见 `Q_INVOKABLE`。

### `[override virtual] QVariant QRangeModel::headerData(int section, Qt::Orientation orientation, int role = Qt::DisplayRole) const`

**作用与语义：**

重实现自：`QAbstractItemModel::headerData`（int section， Qt：：Orientation orientation， int role） const.
返回给定`role`和`section`的首部数据，并带有指定`orientation`。
对于水平头部，节号对应于列号。同样，对于竖向头部，节号对应行号。
对于水平头部和`Qt::DisplayRole` `role`，使用数组作为行类型的范围操作的模型返回`section`。如果行类型是元组，则实现返回`section`的类型名称。对于是小工具或`QObject`类型的行，该函数返回`section`索引处属性的名称。
对于垂直头部，该函数总是返回默认实现的结果`QAbstractItemModel`。
返回给定`role`和`section`的数据，并在头部中返回指定`orientation`。
对于水平头部，节号对应于列号。同样，对于竖向头部，节号对应行号。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[override virtual] QModelIndex QRangeModel::index(int row, int column, const QModelIndex &parent = {}) const`

**作用与语义：**

重实现自：`QAbstractItemModel::index`（整数行，整数列，const QModelIndex 和parent）const.
返回模型项在`row`和`column`的索引`parent`。
传递有效的父节点会为操作列表和表范围的模型生成无效索引。
返回模型中由给定`row`、`column`和`parent`索引指定的项目索引。
在子类中重新实现该函数时，调用 `createIndex()` 生成模型索引，其他组件可以用来引用模型中的项。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[override virtual] bool QRangeModel::insertColumns(int column, int count, const QModelIndex &parent = {})`

**作用与语义：**

重实现自：`QAbstractItemModel::insertColumns`（整数列，整数计数，cont QModelIndex 和父）。
在`parent`区间的所有行中，插入`column`项前`count`空列。成功返回`true`;否则返回`false`。
注意：动态大小的行类型需要提供`insert(const_iterator, size_t, value_type)`成员函数。
对于只读范围或具有静态行类型（如元组、数组或结构体）的模型，该实现不做任何操作，立即返回`false`。树状模型总是如此。
支持此功能`count`模型，在给定`column`之前插入列。每个新列中的项都是`parent`模型索引所表示项的子项。
如果`column`为0，列会被加在已有列之前。
如果`column` `columnCount()`，列会附加到任何已有列上。
如果`parent`没有子节点，则插入一行`count`列。
如果列成功插入，返回`true`;否则返回`false`。
基类实现什么都不做，返回`false`。
如果你实现了自己的模型，如果你想支持插入，可以重新实现这个函数。或者，你也可以提供自己的 API 来修改数据。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[override virtual] bool QRangeModel::insertRows(int row, int count, const QModelIndex &parent = {})`

**作用与语义：**

重实现自：`QAbstractItemModel::insertRows`（整数行，整数计数，const QModelIndex 和父）。
在给定`row`之前`count`行插入`parent`的范围。成功时返回`true`;否则返回`false`。
注意：该范围需要动态大小并提供`insert(const_iterator, size_t, value_type)`成员功能。
对于只读或静态大小的模型（如数组），该实现不做任何操作，立即返回`false`。
注意：对于具有动态大小列类型的范围，列需要提供`resize(size_t)`成员函数。
注意：该函数的基类实现不做任何操作，返回`false`。
支持此操作的模型中，`count`行在给定`row`之前插入模型。新行中的项目将是`parent`模型索引所表示项的子节点。
如果`row`为0，则这些行会被加在父行中已有的行之前。
如果`row` `rowCount()`，则这些行会附加到父节点中已有的行上。
如果`parent`没有子节点，则插入一列`count`行。
如果行成功插入，返回`true`;否则返回`false`。
如果你实现了自己的模型，如果你想支持插入，可以重新实现这个函数。或者，你也可以提供自己的 API 来修改数据。无论哪种情况，你都需要调用 `beginInsertRows()` 和 `endInsertRows()` 通知其他组件模型发生了变化。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[override virtual] QMap<int, QVariant> QRangeModel::itemData(const QModelIndex &index) const`

**作用与语义：**

重实现自：`QAbstractItemModel::itemData`（const QModelIndex & index） const.
返回一个映射，包含模型中该项目在给定`index`处所有预定义角色的值。
如果该`index`的项目类型是一个关联容器，从`int`、`Qt::ItemDataRole`或`QString`映射到`QVariant`，那么该容器的数据会返回。
如果物品类型是小工具或`QObject`子类，则返回与角色名匹配的属性值。
如果该项目不是关联容器、小工具或`QObject`子类，则调用基类实现。
返回一个映射，包含模型中该项目在给定`index`处所有预定义角色的值。
如果你想将默认行为扩展到地图中包含自定义角色，可以重新实现这个函数。

### `[override virtual] QModelIndexList QRangeModel::match(const QModelIndex &start, int role, const QVariant &value, int hits, Qt::MatchFlags flags) const`

**作用与语义：**

重实现自：`QAbstractItemModel::match`（const QModelIndex &start， int role， const QVariant &value， int hits， Qt：：MatchFlags flags） const.
返回`start`索引列中存储在指定`value`下的数据与`role`匹配的项的索引列表。搜索的执行方式由给出的`flags`定义。返回的列表可能是空的。还请注意，如果使用代理模型，列表中结果的顺序可能与模型中的顺序不一致。结果的顺序不能被依赖。
搜索从`start`索引开始，持续直到匹配数据项数达到`hits`，搜索到达最后一行，或再次达到`start`——具体取决于`flags`中是否指定了`MatchWrap`。如果你想搜索所有匹配的项目，使用`hits` = -1。
默认情况下，该函数会对所有项目进行环绕、基于字符串的比较，搜索以`value`指定搜索词开头的项目。
注意：该函数的默认实现仅搜索列。重新实现该函数以包含不同的搜索行为。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[override virtual] QMimeData *QRangeModel::mimeData(const QModelIndexList &indexes) const`

**作用与语义：**

重实现自：`QAbstractItemModel::mimeData`（const QModelIndexList & indexes） const.
返回一个对象，包含对应指定`indexes`列表的序列化数据项。描述编码数据的格式来源于`mimeTypes()`函数。该默认实现使用`mimeTypes()`默认实现返回的默认MIME类型。如果你在自定义模型中重新实现`mimeTypes()`以返回更多MIME类型，请重新实现该函数以利用这些类型。
如果`indexes`列表为空，或没有支持的MIME类型，则返回`nullptr`而非序列化的空列表。

### `[override virtual] QStringList QRangeModel::mimeTypes() const`

**作用与语义：**

重实现自：`QAbstractItemModel::mimeTypes()` const.
返回允许的 MIME 类型列表。默认情况下，内置模型和视图使用内部 MIME 类型：`application/x-qabstractitemmodeldatalist`。
在自定义模型中实现拖放支持时，如果你返回的数据格式不是默认的内部 MIME 类型，请重新实现这个函数，返回你的 MIME 类型列表。
如果你在自定义模型中重新实现该函数，也必须重新实现调用它的成员函数：`mimeData()` 和 `dropMimeData()`。

### `[override virtual] bool QRangeModel::moveColumns(const QModelIndex &sourceParent, int sourceColumn, int count, const QModelIndex &destinationParent, int destinationColumn)`

**作用与语义：**

重实现自：`QAbstractItemModel::moveColumns`（const QModelIndex & sourceParent， int sourceColumn， int count， const QModelIndex & destinationParent， int destinationChild）。
从父`sourceParent`下`sourceColumn` `count`列开始的列移动到父`destinationParent`下的列`destinationColumn`。
如果列成功移动，返回`true`;否则返回`false`。
支持该功能`count`模型，将父`sourceParent`下的列`sourceColumn`移动到父`destinationParent`下的列`destinationChild`。
如果列成功移动，返回`true`;否则返回`false`。
基类实现什么都不做，返回`false`。
如果你实现了自己的模型，如果你想支持移动，可以重新实现这个函数。或者，你也可以提供自己的 API 来修改数据。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[override virtual] bool QRangeModel::moveRows(const QModelIndex &sourceParent, int sourceRow, int count, const QModelIndex &destinationParent, int destinationRow)`

**作用与语义：**

重实现自：`QAbstractItemModel::moveRows`（const QModelIndex & sourceParent， int sourceRow， int count， const QModelIndex & destinationParent， int destinationChild）。
从父`sourceParent`下`count`行，从给定`sourceRow`开始，行`destinationRow`到父`destinationParent`下。
如果行成功移动，返回`true`;否则返回`false`。
支持此操作的模型中，将从父`sourceParent`下的给定`sourceRow`行`count`移至父`destinationParent`下的行`destinationChild`。
如果行成功移动，返回`true`;否则返回`false`。
基类实现什么都不做，返回`false`。
如果你实现了自己的模型，如果你想支持移动，可以重新实现这个函数。或者，你也可以提供自己的 API 来修改数据。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[override virtual] void QRangeModel::multiData(const QModelIndex &index, QModelRoleDataSpan roleDataSpan) const`

**作用与语义：**

Reimpations： `QAbstractItemModel::multiData`（const QModelIndex &index， QModelRoleDataSpan roleDataSpan） const.
用所需数据填充给定`index`的`roleDataSpan`。
默认实现会对该区间中的每个角色调用 `data()`。子类可以重新实现该函数，以更高效地向视图提供数据：
在上面的摘要中，`index`整个调用都是相同的。这意味着访问必要的数据结构以获取`index`的信息只能做一次（将相关代码从循环中抬出）。
鼓励使用`QModelRoleData::setData()`或类似的`QVariant::setValue()`，而不是单独构造`QVariant`并使用纯赋值算符;这是因为前者允许重复使用已分配给`QModelRoleData` `QVariant`对象的内存，而后者总是分配新变体然后销毁旧的。
注意，视图可能调用了 multiData()，其间隔在之前调用中已被使用，因此可能已经包含部分数据。因此，如果模型无法返回给定角色的数据，必须清除对应`QModelRoleData`对象中的数据。这可以通过调用 `QModelRoleData::clearData()`，或者类似地设置默认构造`QVariant`来实现，依此类推。未清除数据会导致视图误以为“旧”数据应用于相应角色。
最后，为了避免代码重复，子类也可能决定用 multiData() 来重新实现`data()`，通过提供一个仅包含一个元素的张成：
注意：模型不得修改跨内角色或重组跨度元素。这样做会导致行为未定义。
注意：将无效模型索引传递给该函数是违法的。

### `[override virtual] QModelIndex QRangeModel::parent(const QModelIndex &child) const`

**作用与语义：**

重实现自：`QAbstractItemModel::parent`（const QModelIndex & index） const.
返回`child`索引处的项目的父节点。
对于在列表和表范围内操作的模型，该函数总是生成无效索引。对于模型在树上的操作，该函数返回由树遍历协议的父()实现返回的行项索引。
返回带有给定`index`的模型项目的父项。如果该项没有父项，则返回无效`QModelIndex`。
在暴露树状数据结构的模型中，一个常见的惯例是只有第一列的项有子。在这种情况下，在子类中重新实现该函数时，返回`QModelIndex`的列将为0。
在子类中重新实现该函数时，注意避免调用`QModelIndex`成员函数，如`QModelIndex::parent()`，因为属于你模型的索引会直接调用你的实现，导致无限递归。
注意：该函数可通过元对象系统和QML调用。参见 `Q_INVOKABLE`。

### `[override virtual] bool QRangeModel::removeColumns(int column, int count, const QModelIndex &parent = {})`

**作用与语义：**

重构：`QAbstractItemModel::removeColumns`（整数列，整数计数，const QModelIndex 和父）。
在`parent`范围内的所有行中，从`column`项中移除`count`列。如果成功返回`true`，否则返回`false`。
注意：动态大小的行类型需要提供`erase(const_iterator, size_t)`成员函数。
对于只读范围或具有静态行类型（如元组、数组或结构体）的模型，该实现不做任何操作，立即返回`false`。树模型总是如此。
在支持此功能的模型中，会从父`parent`下移除以给定`column`开头的`count`列。
如果列被成功移除，返回`true`;否则返回`false`。
基类实现什么都不做，只返回`false`。
如果你实现了自己的模型，如果你想支持删除，可以重新实现这个函数。或者，你也可以提供自己的 API 来修改数据。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[override virtual] bool QRangeModel::removeRows(int row, int count, const QModelIndex &parent = {})`

**作用与语义：**

重实现自：`QAbstractItemModel::removeRows`（整数行，整数计数，cont QModelIndex 和父）。
从`parent`点的范围内移除`count`行，从给定的`row`开始。成功时返回`true`，否则返回`false`。
注意：该范围需要动态大小并提供`erase(const_iterator, size_t)`成员功能。
对于只读或静态大小的模型（如数组），该实现不做任何操作，立即返回`false`。
在支持此功能的模型中，会从父`parent`下移除从给定`row`开始的`count`行。
如果行被成功移除，返回`true`;否则返回`false`。
基类实现什么都不做，只返回`false`。
如果你实现了自己的模型，如果你想支持删除，可以重新实现这个函数。或者，你也可以提供自己的 API 来修改数据。
注意：该函数可以通过元对象系统和QML调用。参见 `Q_INVOKABLE`。

### `[override virtual protected slot] void QRangeModel::resetInternalData()`

**作用与语义：**

重装：`QAbstractItemModel::resetInternalData()`。
该槽位在模型内部数据被清除、重置时被调用。
该槽位提供了具体代理模型子类的便利，例如维护额外数据的`QSortFilterProxyModel`子类。
注意：由于错误，该槽位在Qt 5.0中缺失。

### `[override virtual] QHash<int, QByteArray> QRangeModel::roleNames() const`

**作用与语义：**

重装：`QAbstractItemModel::roleNames()` const.
注意：在`QRangeModel`子类中覆盖该函数是可能的，但可能会破坏该属性的行为。
注意：属性角色Names的获取函数。
返回模特的角色名。
Qt 默认设置的角色名称如下：
- `Qt Role`：QML角色名称
- `Qt::DisplayRole`：显示
- `Qt::DecorationRole`：装饰
- `Qt::EditRole`：编辑
- `Qt::ToolTipRole`：工具提示
- `Qt::StatusTipRole`：statusTip
- `Qt::WhatsThisRole`：这是什么

### `[override virtual] int QRangeModel::rowCount(const QModelIndex &parent = {}) const`

**作用与语义：**

重实现自：`QAbstractItemModel::rowCount`（const QModelIndex & parent） const.
返回给定`parent`下的行数。这是无效`parent`索引根范围中的项数。
如果`parent`索引有效，则对于操作列表和表范围的模型，该函数总是返回0。对于树，则返回树遍历协议中childRows()实现返回的范围大小。
返回给定`parent`下的行数。当父节点有效时，表示 rowCount 返回的是父节点的子节点数。
注意：在实现基于表的模型时，当父模型有效时，rowCount() 应返回 0。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[override virtual] bool QRangeModel::setData(const QModelIndex &index, const QVariant &data, int role = Qt::EditRole)`

**作用与语义：**

重实现自：`QAbstractItemModel::setData`（const QModelIndex & index， const QVariant & value， int role）。
将`index`项的 `role` 数据设置为 `data`。
如果该`index`的项目类型是一个关联容器，从`int`、`Qt::ItemDataRole`或`QString`映射到`QVariant`，那么`data`会存储在该容器中，按`role`指定的键。
如果该项是小工具或`QObject`，则`data`写入该项的属性，与`roleNames()`映射中的`role`条目相符。函数返回`true`是否找到了属性，如果`data`存储了可转换为所需类型的值，否则返回`false`。
否则，该实现将 in in 的 `data` 值赋予 `Qt::DisplayRole` 和 `Qt::EditRole` 范围内`index`的项，并返回 `true`。对于其他角色，实现返回 `false`。
对于在只读区间或实现C元组协议的行类型中只读列操作的模型，该实现会立即返回`false`。
将`index`项的`role`数据设置为`value`。
成功时返回`true`;成功时返回`false`。
如果数据成功设置，`dataChanged()`信号应当发出。
基类实现返回`false`。该函数和`data()`必须重新实现以适应可编辑模型。
注意：该函数可通过元对象系统和QML调用。参见 `Q_INVOKABLE`。

### `[override virtual] bool QRangeModel::setHeaderData(int section, Qt::Orientation orientation, const QVariant &data, int role = Qt::EditRole)`

**作用与语义：**

重实现自：`QAbstractItemModel::setHeaderData`（整数部分，Qt：：Orientation orientation，const QVariant &value，int role）。
在头部设置给定`role`和`section`数据，并指定`orientation`到所提供`value`。
如果头部数据更新，返回`true`;否则返回`false`。
在重新实现该功能时，必须显式地发出`headerDataChanged()`信号。

### `[override virtual] bool QRangeModel::setItemData(const QModelIndex &index, const QMap<int, QVariant> &data)`

**作用与语义：**

重实现自：`QAbstractItemModel::setItemData`（const QModelIndex & index， const QMap<int， QVariant> and roles）。
如果该`index`的项目类型是一个关联容器，从`int`或`Qt::ItemDataRole`映射到`QVariant`，那么`data`中的条目会存储在该容器中。如果关联容器从`QString`映射到`QVariant`，那么只有`data`中那些在角色名表中有映射的值才会被存储。
如果物品类型是小工具或`QObject`子类，那么与角色名匹配的属性会被设置为`data`中对应的值。
`data`中没有条目的角色不被修改。
对于可复制的项目类型，该实现为事务性，如果`data`的所有条目都能存储，则返回 true。如果任何条目无法更新，则原始容器不被修改，函数返回 false。
如果该项不是关联容器、小工具或`QObject`子类，则调用基类实现，该实现为`data`中的每个条目调用`setData()`。
将`index`项的角色数据设置为每个`Qt::ItemDataRole`的对应值`roles`。
成功时返回`true`;否则返回`false`。
未在`roles`中的角色不会被修改。

### `[override virtual] QModelIndex QRangeModel::sibling(int row, int column, const QModelIndex &index) const`

**作用与语义：**

重实现自：`QAbstractItemModel::sibling`（整数行，整数列，cont QModelIndex & index）const.
`row`时退还兄弟姐妹，`index` `column`物品，或者如果该地点没有兄弟姐妹，则`QModelIndex`无效。
这种实现比通过`index`的 `parent()` 快得多。
`row`时退回兄弟姐妹，`index`时`column`物品，或者如果该地点没有兄弟姐妹，则`QModelIndex`无效。
sibling() 只是一个方便函数，它会找到该项的父项，并用它检索指定`row`和`column`子项的索引。
该方法可选择性地覆盖以实现特定优化。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[override virtual] void QRangeModel::sort(int column, Qt::SortOrder order = Qt::AscendingOrder)`

**作用与语义：**

重实现自：`QAbstractItemModel::sort`（整数列，Qt：：SortOrder）。
按给定`order`中的`column`排序模型。
基础类实现什么都不做。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[override virtual] QSize QRangeModel::span(const QModelIndex &index) const`

**作用与语义：**

重实现自：`QAbstractItemModel::span`（const QModelIndex & index） const.
返回由`index`表示的项的行和列跨。
注：目前不使用跨度。

### `[override virtual] Qt::DropActions QRangeModel::supportedDragActions() const`

**作用与语义：**

重装：`QAbstractItemModel::supportedDragActions()` const.
返回该模型中数据支持的动作。
默认实现返回`supportedDropActions()`。如果你希望支持更多操作，可以重新实现这个函数。
当发生拖拽时，`QAbstractItemView::startDrag()` 默认使用支持的DragActions()。

### `[override virtual] Qt::DropActions QRangeModel::supportedDropActions() const`

**作用与语义：**

重实现自：`QAbstractItemModel::supportedDropActions()` const.
返回该模型支持的投放动作。
默认实现返回`Qt::CopyAction`。如果你希望支持额外操作，请重新实现这个函数。你还必须重新实现`dropMimeData()`函数以处理这些额外的操作。

### `(since 6.11) struct ItemAccess`

**作用与语义：**

ItemAccess 模板提供了一个自定义点，用于控制 QRangeModel 如何访问各个项目的角色数据。
针对数据结构中使用的类型对该模板进行专门化，并实现 `readRole()` 和 `writeRole()` 成员以访问类型的特定角色数据。
此类型的专门化将优先于任何预定义行为。不要对非自有类型专门化此模板。对 ItemAccess 专门化的类型将被隐式解释为多角色项。

**官方示例：**

```cpp
 template <>
 struct QRangeModel::ItemAccess<ItemType>
 {
     static QVariant readRole(const ItemType &item, int role)
     {
         switch (role) {
             // ...
         }
         return {};
     }

     static bool writeRole(ItemType &item, const QVariant &data, int role)
     {
         bool ok = false;
         switch (role) {
             // ...
         }

         return ok;
     }
 };
```

### `(since 6.10) struct RowOptions`

**作用与语义：**

RowOptions 模板提供了一个自定义点，用于控制 QRangeModel 如何表示作为行的类型。
将该模板专门化为你范围内使用的类型，并添加相关成员。
- `Member`：价值观
- `static constexpr `RowCategory` rowCategory`：`RowCategory`

**官方示例：**

```cpp
 class ColorEntry
 {
     Q_GADGET
     Q_PROPERTY(QString display MEMBER m_colorName)
     Q_PROPERTY(QColor decoration READ decoration)
     Q_PROPERTY(QString toolTip READ toolTip)
 public:
     ...
 };
 template <>
 struct QRangeModel::RowOptions<ColorEntry>
 {
     static constexpr auto rowCategory = QRangeModel::RowCategory::MultiRoleItem;
 };
```

### `QRangeModel(Range &&range, QObject *parent = nullptr)`

**作用与语义：**

构造一个`QRangeModel`实例，操作`range`中的数据。`range`必须是一个顺序范围，编译器通过参数相关查找找到`begin`和`end`重载，或者实现了`std::begin`和`std::end`。如果提供了`protocol`，模型将用协议实现表示该范围为树。模型实例成为`parent`的子。
`range`可以是指针或引用包装器，此时变异的模型API（如`setData()`或`insertRow()`）会修改被引用范围实例中的数据。如果`range`是一个值（或被移入模型），则连接到模型发出的信号，以响应数据的变化。
`QRangeModel`在构建过程中无法访问`range`。这使得在构造过程中，可以合法地将尚未完全构造的范围对象的指针或引用传递给该构造器，例如在子类QRangeModel时。
如果`range`被移入模型，那么模型销毁时，范围和所有数据都会被销毁。
注意：虽然模型在其他情况下不拥有距离对象的所有权，但一旦模型构建并传递给视图，你不得直接修改`range`。此类修改不会发出保持模型用户（其他模型或视图）与模型同步所需的信号，导致结果不一致、行为未定义和崩溃。使用`QRangeModelAdapter`安全地与底层范围交互，同时保持模型更新。

### `QRangeModel::AutoConnectPolicy autoConnectPolicy() const`

**作用与语义：**

当且当模型自动连接到属性时，通知发生变化。
如果`QRangeModel`运行在与其行或项类型相同类型的`QObject`子类的数据结构上，则可以自动将QObject的属性与`dataChanged()`信号连接起来。对于`QObject`行，对每列进行此操作，映射到`Qt::DisplayRole`属性。对于项目，则对与某个角色名称匹配的属性进行此操作。
默认情况下，该属性的值是`None`的，因此不会建立这样的连接。改变该属性的值总是会破坏所有现有的连接。
注意：如果`QRangeModel`操作的数据结构中的QObject被替换掉，连接不会被破坏或创建。

**如何使用：** 调用 `autoConnectPolicy()` 读取当前值；它不会修改应用状态。

### `void resetRoleNames()`

**作用与语义：**

该属性包含模型的角色名称。
如果该区间的所有列都属于同一类型，且该类型提供了元对象（即是小工具或`QObject`子类），那么该属性就包含该类型属性的名称，并将其映射到从`Qt::UserRole`开始`Qt::ItemDataRole`值的值。此外，角色“modelData”还提供对小工具或`QObject`实例的访问。
通过将该属性显式设置为非空映射来覆盖该默认行为。将该属性设置为空映射，或使用 resetRoleNames()，即可恢复默认行为。

**如何使用：** 调用 `resetRoleNames()` 撤销对 `roleNames` 的显式覆盖，让它重新采用继承值或默认值。

### `void setAutoConnectPolicy(QRangeModel::AutoConnectPolicy policy)`

**作用与语义：**

当且当模型自动连接到属性时，通知发生变化。
如果`QRangeModel`运行在与其行或项类型相同类型的`QObject`子类的数据结构上，则可以自动将QObject的属性与`dataChanged()`信号连接起来。对于`QObject`行，对每列进行此操作，映射到`Qt::DisplayRole`属性。对于项目，则对与某个角色名称匹配的属性进行此操作。
默认情况下，该属性的值是`None`的，因此不会建立这样的连接。改变该属性的值总是会破坏所有现有的连接。
注意：如果`QRangeModel`操作的数据结构中的QObject被替换掉，连接不会被破坏或创建。

**如何使用：** 调用 `setAutoConnectPolicy(...)` 修改 `autoConnectPolicy`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setRoleNames(const QHash<int, QByteArray> &names)`

**作用与语义：**

该属性包含模型的角色名称。
如果该区间的所有列都属于同一类型，且该类型提供了元对象（即是小工具或`QObject`子类），那么该属性就包含该类型属性的名称，并将其映射到从`Qt::UserRole`开始`Qt::ItemDataRole`值的值。此外，角色“modelData”还提供对小工具或`QObject`实例的访问。
通过将该属性显式设置为非空映射来覆盖该默认行为。将该属性设置为空映射，或使用 resetRoleNames()，即可恢复默认行为。

**如何使用：** 调用 `setRoleNames(...)` 修改 `roleNames`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void autoConnectPolicyChanged(QRangeModel::AutoConnectPolicy policy)`

**作用与语义：**

当且当模型自动连接到属性时，通知发生变化。
如果`QRangeModel`运行在与其行或项类型相同类型的`QObject`子类的数据结构上，则可以自动将QObject的属性与`dataChanged()`信号连接起来。对于`QObject`行，对每列进行此操作，映射到`Qt::DisplayRole`属性。对于项目，则对与某个角色名称匹配的属性进行此操作。
默认情况下，该属性的值是`None`的，因此不会建立这样的连接。改变该属性的值总是会破坏所有现有的连接。
注意：如果`QRangeModel`操作的数据结构中的QObject被替换掉，连接不会被破坏或创建。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `autoConnectPolicy` 的变化，不要把它当作普通函数主动调用。

### `void roleNamesChanged()`

**作用与语义：**

该属性包含模型的角色名称。
如果该区间的所有列都属于同一类型，且该类型提供了元对象（即是小工具或`QObject`子类），那么该属性就包含该类型属性的名称，并将其映射到从`Qt::UserRole`开始`Qt::ItemDataRole`值的值。此外，角色“modelData”还提供对小工具或`QObject`实例的访问。
通过将该属性显式设置为非空映射来覆盖该默认行为。将该属性设置为空映射，或使用 resetRoleNames()，即可恢复默认行为。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `roleNames` 的变化，不要把它当作普通函数主动调用。

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

`QRangeModel` 所属机制类型：模型/视图协议。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
