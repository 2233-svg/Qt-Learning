# QAbstractItemModel

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QAbstractItemModel` 定义模型/视图体系的数据协议：索引、层级、角色、编辑和结构变化通知都由它统一描述。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QAbstractItemModel` 定义模型/视图体系的数据协议：索引、层级、角色、编辑和结构变化通知都由它统一描述。

**内部模型：** view 不直接保存业务数据，而是通过 QModelIndex 向 model 查询 data。begin/endInsertRows、layoutChanged、dataChanged 等通知是保持 view 正确更新的协议，不是可有可无的刷新提示。

**适用场景：** 需要让 QListView/QTableView/QTreeView 展示自定义数据，或需要代理模型、排序过滤和编辑支持时继承它的合适子类。

**典型调用链：** 实现 rowCount/columnCount/index/parent/data -> 连接 view -> 在数据变化时发 dataChanged 或 begin/end 结构信号 -> 需要编辑时实现 flags/setData。

**先记住的坑：** 不要返回失效 QModelIndex；插入/删除必须成对 begin/end；区分 DisplayRole/EditRole；不要在 data() 中做昂贵或有副作用的工作。

## 2. 依赖与对象关系

- 头文件：`#include <QAbstractItemModel>`
- 继承自：QObject
- 直接派生类：QAbstractItemModelReplica、QAbstractListModel、QAbstractProxyModel、QAbstractTableModel、QConcatenateTablesProxyModel、QFileSystemModel、QHelpContentModel、QPdfBookmarkModel、QRangeModel,、QStandardItemModel

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

view 不直接保存业务数据，而是通过 QModelIndex 向 model 查询 data。begin/endInsertRows、layoutChanged、dataChanged 等通知是保持 view 正确更新的协议，不是可有可无的刷新提示。

### 状态、生命周期和线程

**生命周期：** 模型应比视图活得足够久，视图销毁时不会自动替业务容器释放资源。模型变化必须使用对应的 begin/end 协议或精确通知，不能只改容器后期待视图自行发现。取到的 QModelIndex 只在模型允许的生命周期内有效。

**状态与结果：** 区分当前索引、选择模型、编辑状态、数据角色和模型结构变化。`dataChanged` 表示已有项目的数据变化，行列插入/删除表示结构变化，`modelReset` 会让旧索引整体失效。

**线程与事件循环：** 模型通常在 GUI 线程被视图访问。后台线程不要直接修改正在显示的模型；应在正确线程汇总数据，再通过通知协议更新，或使用线程安全的数据交换层。

## 3. 直接使用

需要让 QListView/QTableView/QTreeView 展示自定义数据，或需要代理模型、排序过滤和编辑支持时继承它的合适子类。 使用时通常按这个过程组织：实现 rowCount/columnCount/index/parent/data -> 连接 view -> 在数据变化时发 dataChanged 或 begin/end 结构信号 -> 需要编辑时实现 flags/setData。

```cpp
class StringListModel final : public QAbstractListModel
{
public:
    int rowCount(const QModelIndex &parent = {}) const override;
    QVariant data(const QModelIndex &index, int role) const override;

private:
    QStringList values_;
};
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum class CheckIndexOption { NoOption, IndexIsValid, DoNotUseParent, ParentIsInvalid }`
- `flags CheckIndexOptions`
- `enum LayoutChangeHint { NoLayoutChangeHint, VerticalSortHint, HorizontalSortHint }`

### 公有函数

- `QAbstractItemModel(QObject *parent = nullptr)`
- `virtual ~QAbstractItemModel()`
- `virtual QModelIndex buddy(const QModelIndex &index) const`
- `virtual bool canDropMimeData(const QMimeData *data, Qt::DropAction action, int row, int column, const QModelIndex &parent) const`
- `virtual bool canFetchMore(const QModelIndex &parent) const`
- `bool checkIndex(const QModelIndex &index, QAbstractItemModel::CheckIndexOptions options = CheckIndexOption::NoOption) const`
- `(since 6.0) virtual bool clearItemData(const QModelIndex &index)`
- `virtual int columnCount(const QModelIndex &parent = QModelIndex()) const = 0`
- `virtual QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const = 0`
- `virtual bool dropMimeData(const QMimeData *data, Qt::DropAction action, int row, int column, const QModelIndex &parent)`
- `virtual void fetchMore(const QModelIndex &parent)`
- `virtual Qt::ItemFlags flags(const QModelIndex &index) const`
- `virtual bool hasChildren(const QModelIndex &parent = QModelIndex()) const`
- `bool hasIndex(int row, int column, const QModelIndex &parent = QModelIndex()) const`
- `virtual QVariant headerData(int section, Qt::Orientation orientation, int role = Qt::DisplayRole) const`
- `virtual QModelIndex index(int row, int column, const QModelIndex &parent = QModelIndex()) const = 0`
- `bool insertColumn(int column, const QModelIndex &parent = QModelIndex())`
- `virtual bool insertColumns(int column, int count, const QModelIndex &parent = QModelIndex())`
- `bool insertRow(int row, const QModelIndex &parent = QModelIndex())`
- `virtual bool insertRows(int row, int count, const QModelIndex &parent = QModelIndex())`
- `virtual QMap<int, QVariant> itemData(const QModelIndex &index) const`
- `virtual QModelIndexList match(const QModelIndex &start, int role, const QVariant &value, int hits = 1, Qt::MatchFlags flags = Qt::MatchFlags(Qt::MatchStartsWith|Qt::MatchWrap)) const`
- `virtual QMimeData * mimeData(const QModelIndexList &indexes) const`
- `virtual QStringList mimeTypes() const`
- `bool moveColumn(const QModelIndex &sourceParent, int sourceColumn, const QModelIndex &destinationParent, int destinationChild)`
- `virtual bool moveColumns(const QModelIndex &sourceParent, int sourceColumn, int count, const QModelIndex &destinationParent, int destinationChild)`
- `bool moveRow(const QModelIndex &sourceParent, int sourceRow, const QModelIndex &destinationParent, int destinationChild)`
- `virtual bool moveRows(const QModelIndex &sourceParent, int sourceRow, int count, const QModelIndex &destinationParent, int destinationChild)`
- `(since 6.0) virtual void multiData(const QModelIndex &index, QModelRoleDataSpan roleDataSpan) const`
- `virtual QModelIndex parent(const QModelIndex &index) const = 0`
- `bool removeColumn(int column, const QModelIndex &parent = QModelIndex())`
- `virtual bool removeColumns(int column, int count, const QModelIndex &parent = QModelIndex())`
- `bool removeRow(int row, const QModelIndex &parent = QModelIndex())`
- `virtual bool removeRows(int row, int count, const QModelIndex &parent = QModelIndex())`
- `virtual QHash<int, QByteArray> roleNames() const`
- `virtual int rowCount(const QModelIndex &parent = QModelIndex()) const = 0`
- `virtual bool setData(const QModelIndex &index, const QVariant &value, int role = Qt::EditRole)`
- `virtual bool setHeaderData(int section, Qt::Orientation orientation, const QVariant &value, int role = Qt::EditRole)`
- `virtual bool setItemData(const QModelIndex &index, const QMap<int, QVariant> &roles)`
- `virtual QModelIndex sibling(int row, int column, const QModelIndex &index) const`
- `virtual void sort(int column, Qt::SortOrder order = Qt::AscendingOrder)`
- `virtual QSize span(const QModelIndex &index) const`
- `virtual Qt::DropActions supportedDragActions() const`
- `virtual Qt::DropActions supportedDropActions() const`

### 公有槽函数

- `virtual void revert()`
- `virtual bool submit()`

### 信号

- `void columnsAboutToBeInserted(const QModelIndex &parent, int first, int last)`
- `void columnsAboutToBeMoved(const QModelIndex &sourceParent, int sourceStart, int sourceEnd, const QModelIndex &destinationParent, int destinationColumn)`
- `void columnsAboutToBeRemoved(const QModelIndex &parent, int first, int last)`
- `void columnsInserted(const QModelIndex &parent, int first, int last)`
- `void columnsMoved(const QModelIndex &sourceParent, int sourceStart, int sourceEnd, const QModelIndex &destinationParent, int destinationColumn)`
- `void columnsRemoved(const QModelIndex &parent, int first, int last)`
- `void dataChanged(const QModelIndex &topLeft, const QModelIndex &bottomRight, const QList<int> &roles = QList<int>())`
- `void headerDataChanged(Qt::Orientation orientation, int first, int last)`
- `void layoutAboutToBeChanged(const QList<QPersistentModelIndex> &parents = QList<QPersistentModelIndex>(), QAbstractItemModel::LayoutChangeHint hint = QAbstractItemModel::NoLayoutChangeHint)`
- `void layoutChanged(const QList<QPersistentModelIndex> &parents = QList<QPersistentModelIndex>(), QAbstractItemModel::LayoutChangeHint hint = QAbstractItemModel::NoLayoutChangeHint)`
- `void modelAboutToBeReset()`
- `void modelReset()`
- `void rowsAboutToBeInserted(const QModelIndex &parent, int start, int end)`
- `void rowsAboutToBeMoved(const QModelIndex &sourceParent, int sourceStart, int sourceEnd, const QModelIndex &destinationParent, int destinationRow)`
- `void rowsAboutToBeRemoved(const QModelIndex &parent, int first, int last)`
- `void rowsInserted(const QModelIndex &parent, int first, int last)`
- `void rowsMoved(const QModelIndex &sourceParent, int sourceStart, int sourceEnd, const QModelIndex &destinationParent, int destinationRow)`
- `void rowsRemoved(const QModelIndex &parent, int first, int last)`

### 保护函数

- `void beginInsertColumns(const QModelIndex &parent, int first, int last)`
- `void beginInsertRows(const QModelIndex &parent, int first, int last)`
- `bool beginMoveColumns(const QModelIndex &sourceParent, int sourceFirst, int sourceLast, const QModelIndex &destinationParent, int destinationChild)`
- `bool beginMoveRows(const QModelIndex &sourceParent, int sourceFirst, int sourceLast, const QModelIndex &destinationParent, int destinationChild)`
- `void beginRemoveColumns(const QModelIndex &parent, int first, int last)`
- `void beginRemoveRows(const QModelIndex &parent, int first, int last)`
- `void beginResetModel()`
- `void changePersistentIndex(const QModelIndex &from, const QModelIndex &to)`
- `void changePersistentIndexList(const QModelIndexList &from, const QModelIndexList &to)`
- `QModelIndex createIndex(int row, int column, const void *ptr = nullptr) const`
- `QModelIndex createIndex(int row, int column, quintptr id) const`
- `void endInsertColumns()`
- `void endInsertRows()`
- `void endMoveColumns()`
- `void endMoveRows()`
- `void endRemoveColumns()`
- `void endRemoveRows()`
- `void endResetModel()`
- `QModelIndexList persistentIndexList() const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum class QAbstractItemModel::CheckIndexOptionflags QAbstractItemModel::CheckIndexOptions`

**作用与语义：**

此枚举可用于控制`QAbstractItemModel::checkIndex()`执行的检查。
- `QAbstractItemModel::CheckIndexOption::NoOption`：`0x0000`；未指定任何检查选项。
- `QAbstractItemModel::CheckIndexOption::IndexIsValid`：`0x0001`；检查传递给`QAbstractItemModel::checkIndex()`的模型索引是否为有效的模型索引。
- `QAbstractItemModel::CheckIndexOption::DoNotUseParent`：`0x0002`；不会执行与使用传递给`QAbstractItemModel::checkIndex()`的索引的父项相关的任何检查。
- `QAbstractItemModel::CheckIndexOption::ParentIsInvalid`：`0x0004`；检查传递给`QAbstractItemModel::checkIndex()`的模型索引的父项是否为无效的模型索引。如果同时指定了此选项和DoNotUseParent，则忽略此选项。
CheckIndexOptions类型是QFlags<CheckIndexOption>的typedef。它存储CheckIndexOption值的或组合。

### `enum QAbstractItemModel::LayoutChangeHint`

**作用与语义：**

该枚举描述了模型布局的变化方式。
- `QAbstractItemModel::NoLayoutChangeHint`：`0`;没有提示。
- `QAbstractItemModel::VerticalSortHint`：`1`;行正在分类中。
- `QAbstractItemModel::HorizontalSortHint`：`2`;列正在排序中。
注意，VerticalSortHint 和 HorizontalSortHint 的含义是，项目在同一父节点内移动，而不是移动到模型中的另一个父节点，也没有被过滤或过滤。

### `[explicit] QAbstractItemModel::QAbstractItemModel(QObject *parent = nullptr)`

**作用与语义：**

构造一个抽象题目模型，并用给定的 `parent`。

### `[virtual noexcept] QAbstractItemModel::~QAbstractItemModel()`

**作用与语义：**

摧毁了抽象物品模型。

### `[protected] void QAbstractItemModel::beginInsertColumns(const QModelIndex &parent, int first, int last)`

**作用与语义：**

开始列插入操作。
在子类中重新实现`insertColumns()`时，必须调用该函数，然后再将数据插入模型底层数据存储。
`parent`索引对应新列插入的父索引;`first`和`last`是新列插入后所具有的列号。
- `Inserting columns`：指定你想插入模型中某项的列区间的首尾两列编号。例如，如图所示，我们在第4列前插入三列，`first`为4，`last`为6：

beginInsertColumns（父列，4,6）;

这会将三列新插入为第4、5和6列。
- `Appending columns`：要添加列，请在最后一列之后插入列。例如，如图所示，我们在一组六列现有列（以第5列结束）中附加三列，因此`first`为6，`last`为8：

beginInsertColumns（父列，6,8）;

这会将这两个新列附加为第6、7和8列。
注意：该函数会发出连接视图（或代理）必须处理的`columnsAboutToBeInserted()`信号，然后才插入数据。否则，视图可能会处于无效状态。

### `[protected] void QAbstractItemModel::beginInsertRows(const QModelIndex &parent, int first, int last)`

**作用与语义：**

开始行插入操作。
在子类中重新实现 `insertRows()` 时，必须在将数据插入模型的底层数据存储之前调用此函数。
`parent` 索引对应新行要插入的父项；`first` 和 `last` 是新行插入后将具有的行号。
- `Inserting rows`：指定要插入到模型中某个项的行范围的首行和末行。例如，如图所示，我们在第 2 行之前插入三行，因此 `first` 为 2，`last` 为 4：

beginInsertRows(parent, 2, 4);

这会将三行新行插入为第 2、3 和 4 行。
- `Appending rows`：要追加行，请将其插入到最后一行之后。例如，如图所示，我们向已有 4 行（最后一行为第 3 行）的集合追加两行，因此 `first` 为 4，`last` 为 5：

beginInsertRows(parent, 4, 5);

这会将两行新行追加为第 4 和 5 行。
注意：此函数会发射 `rowsAboutToBeInserted()` 信号，连接的视图（或代理）必须在数据插入之前处理该信号。否则，视图可能会处于无效状态。

### `[protected] bool QAbstractItemModel::beginMoveColumns(const QModelIndex &sourceParent, int sourceFirst, int sourceLast, const QModelIndex &destinationParent, int destinationChild)`

**作用与语义：**

开始列移动操作。
在重构子类时，该方法简化了模型中的移动实体。该方法负责移动模型中的持久索引，否则你必须自己完成。使用 beginMoveColumns 和 `endMoveColumns` 是直接发出 `layoutAboutToBeChanged` 和 `layoutChanged` 以及 `changePersistentIndex` 的替代方案。
`sourceParent`索引对应列移动的父节点;`sourceFirst`和`sourceLast`分别是要移动列的第一个和最后一个列号。`destinationParent`索引对应这些列移动到的父节点。`destinationChild`是列将要移动到的列。也就是说，`sourceParent` 中第 `sourceFirst` 列的索引将变为 `destinationParent` 中的第 `destinationChild` 列，随后是所有其他至 `sourceLast` 列的索引。
然而，当同一父列（`sourceParent` 和 `destinationParent` 相等）向下移动列时，列会放在 `destinationChild` 索引之前。也就是说，如果你想把列 0 和 1 移动，使它们变成列 1 和 2，`destinationChild` 应该是 3。在这种情况下，源列 `i`（介于 `sourceFirst` 和 `sourceLast` 之间）的新索引等于 `(destinationChild-sourceLast-1+i)`。
注意，如果`sourceParent`和`destinationParent`相同，你必须确保`destinationChild`不在`sourceFirst`和`sourceLast` 1的范围内。你还必须确保不尝试将列移动到其自身的子列或祖先。如果任一条件成立，该方法返回`false`，此时应中止移动操作。

### `[protected] bool QAbstractItemModel::beginMoveRows(const QModelIndex &sourceParent, int sourceFirst, int sourceLast, const QModelIndex &destinationParent, int destinationChild)`

**作用与语义：**

开始行移动操作。
在重新实现子类时，该方法简化了模型中的移动实体。该方法负责移动模型中的持久索引，否则你必须自己完成。使用 bestartMoveRows 和 `endMoveRows` 是直接发出 `layoutAboutToBeChanged` 和 `layoutChanged` 以及 `changePersistentIndex` 的替代方案。
`sourceParent`索引对应行的父节点;`sourceFirst`和`sourceLast`分别是要移动行的第一个和最后一个行号。`destinationParent`索引对应这些行被移动到的父节点。`destinationChild`是行将要移动到的行。也就是说，`sourceParent`中第`sourceFirst`行的索引将变为`destinationParent`中的第`destinationChild`行，随后是所有至`sourceLast`行的索引。
然而，当同一父节点下移行（`sourceParent` 和 `destinationParent` 相等）时，行会放在 `destinationChild` 索引之前。也就是说，如果你想把第 0 行和第 1 行移动成第 1 和第 2 行，`destinationChild`应该是第 3 行。在这种情况下，源行 `i`（介于 `sourceFirst` 和 `sourceLast` 之间）的新索引等于 `(destinationChild-sourceLast-1+i)`。
注意，如果`sourceParent`和`destinationParent`相同，你必须确保`destinationChild`不在`sourceFirst`和`sourceLast` 1的范围内。你还必须确保不尝试将行移动到其自身的子行或祖先行。如果任一条件成立，该方法返回`false`，此时应中止移动操作。
- `Moving rows to another parent`：指定你想在模型中移动的源父节点行的首尾行数。还指定目标父节点中要移动的行。例如，如图所示，我们将源节点的第2行移到第4行，`sourceFirst`为2，`sourceLast`为4。我们将这些项移至目标节点第2行之上，`destinationChild`为2。

beginMoveRows（sourceParent， 2， 4， destinationParent， 2）;

这会将源端的三行第2、3、4行移动到目的地的第2、3和4行。其他受影响的兄弟姐妹也会相应地被移位。
- `Moving rows to append to another parent`：要将行附加到另一行，将其移至最后一行之后。例如，如图所示，我们将三行移动到6行的集合（以第5行结束），因此`destinationChild`为6：

beginMoveRows（sourceParent， 2， 4， destinationParent， 6）;

这会将目标行移动到目标父节点的末尾，分别为6、7和8。
- `Moving rows in the same parent up`：要在同一父节点内移动行，指定要移动到哪一行。例如，如图所示，我们将一个项目从第2行移动到第0行，因此`sourceFirst`和`sourceLast`为2，`destinationChild`为0。

beginMoveRows（parent， 2， 2， parent， 0）;

注意其他行可能会相应地被移位。还要注意，在同一父节点内移动物品时，不应尝试无效或无操作的移动。在上述例子中，项目2在移动前的第2行，因此不能移动到第2行（已经在第2行）或第3行（无操作，因为第3行意味着在第3行之上，也就是它已经在第3行之上）。
- `Moving rows in the same parent down`：要在同一父节点内移动行，指定要移动到哪行。例如，如图所示，我们将一个项目从第2行移到第4行，因此`sourceFirst`和`sourceLast`为2，`destinationChild`为4。

beginMoveRows（父列，2,2，父列4）;

注意其他行可能会相应地被移位。

### `[protected] void QAbstractItemModel::beginRemoveColumns(const QModelIndex &parent, int first, int last)`

**作用与语义：**

开始列移除操作。
在子类中重新实现 `removeColumns()` 时，必须在从模型的底层数据存储中删除数据之前调用此函数。
`parent` 索引对应要删除新列的父项；`first` 和 `last` 是要删除的首列和末列的列号。
- `Removing columns`：指定要从模型中的某个项中移除的列范围的首列和末列。例如，如图所示，我们移除第 4 列到第 6 列的三列，因此 `first` 为 4，`last` 为 6：

beginRemoveColumns(parent, 4, 6);
注意：此函数会发射 `columnsAboutToBeRemoved()` 信号，连接的视图（或代理）必须在数据被移除之前处理该信号。否则，视图可能会处于无效状态。

### `[protected] void QAbstractItemModel::beginRemoveRows(const QModelIndex &parent, int first, int last)`

**作用与语义：**

开始排间清除作业。
在子类中重新实现`removeRows()`时，必须调用该函数，然后再从模型底层数据存储中移除数据。
`parent`索引对应于移除新行的父索引;`first`和`last`分别是待移除行的行编号。
- `Removing rows`：指定你想从模型中移除的行的首尾两行数。例如，如图所示，我们将第2行的两行移除到第3行，因此`first`为2，`last`为3：

beginRemoveRows（父行，2,3）;
注意：该函数会发出连接视图（或代理）必须处理的`rowsAboutToBeRemoved()`信号，然后数据才会被移除。否则，视图可能会处于无效状态。

### `[protected] void QAbstractItemModel::beginResetModel()`

**作用与语义：**

开始模型重置操作。
重置操作会将模型重置为当前状态，并显示在任何附加的视图中。
注意：附加到此模型的任何视图也将被重置。
当模型被重置时，意味着模型以前报告的任何数据现在都是无效的，必须重新查询。这也意味着当前项和任何已选项将变为无效。
当模型的数据发生根本性变化时，有时直接调用此函数比发射 `dataChanged()` 来通知其他组件底层数据源或结构已更改更加简单。
在重置模型或代理模型的任何内部数据结构之前，必须调用此函数。
此函数会发射 `modelAboutToBeReset()` 信号。

### `[virtual] QModelIndex QAbstractItemModel::buddy(const QModelIndex &index) const`

**作用与语义：**

返回`index`所表示的项目伙伴的模型索引。当用户想编辑某个项目时，视图会调用该函数检查是否应该编辑模型中的其他项目。然后，视图会利用伙伴项目返回的模型索引构建代理。
该功能的默认实现中，每个物品都是独立的伙伴。

### `[virtual] bool QAbstractItemModel::canDropMimeData(const QMimeData *data, Qt::DropAction action, int row, int column, const QModelIndex &parent) const`

**作用与语义：**

返回 返回`true`模型是否能接受`data`的删除。该默认实现仅检查`data` 是否在`mimeTypes()`列表中至少有一个格式，以及`action`是否在模型的`supportedDropActions()`中。
如果你想测试`data`是否能在`row`、`column`、`parent`时用`action`丢弃，可以在自定义模型中重新实现这个函数。如果你不需要这个测试，也没必要重新实现这个函数。

### `[virtual invokable] bool QAbstractItemModel::canFetchMore(const QModelIndex &parent) const`

**作用与语义：**

如果有更多可用数据，返回`true` `parent`;否则返回`false`。
默认实现总是返回`false`。
如果 canFetchMore() 返回 `true`，则应调用 `fetchMore()` 函数。这就是 `QAbstractItemView` 的行为。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[protected] void QAbstractItemModel::changePersistentIndex(const QModelIndex &from, const QModelIndex &to)`

**作用与语义：**

将等于给定`from`模型指数的`QPersistentModelIndex`转换为给定的`to`模型指数。
如果没有找到等于给定`from`模型指数的持久模型索引，则不会有任何变化。

### `[protected] void QAbstractItemModel::changePersistentIndexList(const QModelIndexList &from, const QModelIndexList &to)`

**作用与语义：**

将与给定`from`模型索引列表中索引相等的{`QPersistentModelIndex`}e转换为给定的`to`模型索引列表。
如果找不到等于给定`from`模型索引列表中索引的持久模型索引，则不会有任何更改。

### `bool QAbstractItemModel::checkIndex(const QModelIndex &index, QAbstractItemModel::CheckIndexOptions options = CheckIndexOption::NoOption) const`

**作用与语义：**

该函数检查`index`是否是该模型的合法模型索引。合法模型索引要么是无效模型索引，要么是满足以下条件的有效模型索引：
- 指数模型为`this`;
- 索引行大于或等于零;
- 索引的行数小于索引父节点的行数;
- 索引的列大于或等于零;
- 索引的列数小于索引父列的列数。
`options`论证可能会改变部分这些检查。如果`options`包含`IndexIsValid`，那么`index`必须是有效的索引;这在重现如期望有效索引的`data()`或 `setData()` 等函数时非常有用。
如果`options`包含`DoNotUseParent`，则省略调用`parent()`的检查;这使得从`parent()`重实现中调用该函数（否则将导致无休止递归和崩溃）。
如果`options`不包含`DoNotUseParent`，而包含`ParentIsInvalid`，则会进行额外检查：检查父索引是否有效。这在实现平面模型如列表或表时非常有用，因为没有模型索引应有有效的父索引。
如果所有检查都成功，该函数返回真，否则返回假。这使得该函数可以在`Q_ASSERT`及类似的调试机制中使用。如果某个检查失败，`qt.core.qabstractitemmodel.checkindex`日志类别会打印警告消息，其中包含一些可能对调试失败有用的信息。
注意：该函数是用于实现你自己项目模型的调试辅助工具。在开发复杂模型以及构建复杂模型层级结构（例如使用代理模型）时，调用此函数非常有用，以便发现与错误模型索引（如上定义）意外传递到某些`QAbstractItemModel` API相关的错误。
警告：请注意，向项目模型传递非法索引属于未定义行为，因此应用程序必须避免这样做，且不应依赖物品模型可能采用的任何“防御性”程序来优雅处理非法索引。

### `[virtual, since 6.0] bool QAbstractItemModel::clearItemData(const QModelIndex &index)`

**作用与语义：**

移除给定`index`所有角色中存储的数据。如果成功返回`true`;否则返回`false`。如果数据被成功移除，应发出`dataChanged()`信号。基类实现返回`false`。

### `[pure virtual invokable] int QAbstractItemModel::columnCount(const QModelIndex &parent = QModelIndex()) const`

**作用与语义：**

返回给定`parent`子节点的列数。
在大多数子类中，列的数量与`parent`无关。
注意：在实现基于表的模型时，当父模型有效时，columnCount() 应返回 0。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

**官方示例：**

```cpp
 int MyModel::columnCount(const QModelIndex &parent) const
 {
     Q_UNUSED(parent);
     return 3;
 }
```

### `[private signal] void QAbstractItemModel::columnsAboutToBeInserted(const QModelIndex &parent, int first, int last)`

**作用与语义：**

该信号在插入列入模型前发出。新项目将位于 `first` 和 `last` 之间，位于给定的 `parent` 项目下方。
注意：连接到该信号的组件会用它来适应模型尺寸的变化。它只能由`QAbstractItemModel`实现发出，不能在子类代码中显式发出。
注意：这是一个私有信号。它可以用于信号连接，但用户不能发射。

### `[private signal] void QAbstractItemModel::columnsAboutToBeMoved(const QModelIndex &sourceParent, int sourceStart, int sourceEnd, const QModelIndex &destinationParent, int destinationColumn)`

**作用与语义：**

该信号在模型内列移动前发出。将被移动的项目是介于`sourceStart`和`sourceEnd`之间，包含在给定`sourceParent`项下的物品。它们将从列`destinationColumn`开始移动到`destinationParent`。
注意：连接到该信号的组件会用它来适应模型尺寸的变化。该信号只能由`QAbstractItemModel`实现发出，不能在子类代码中显式发射。
注意：这是一个私有信号。它可以用于信号连接，但用户不能发射。

### `[private signal] void QAbstractItemModel::columnsAboutToBeRemoved(const QModelIndex &parent, int first, int last)`

**作用与语义：**

该信号在模型列被移除前发出。要移除的项目是`first`到`last`之间，包含在给定`parent`项下的。
注意：连接到该信号的组件会用它来适应模型尺寸的变化。它只能通过`QAbstractItemModel`实现发出，不能在子类代码中显式发射。
注意：这是一个私有信号。它可以用于信号连接，但用户不能发射。

### `[private signal] void QAbstractItemModel::columnsInserted(const QModelIndex &parent, int first, int last)`

**作用与语义：**

该信号是在模型插入列后发出的。新增的项目是介于`first`到`last`包含在内的，属于给定的`parent`项。
注意：连接到该信号的组件会用它来适应模型尺寸的变化。它只能由`QAbstractItemModel`实现发出，不能在子类代码中显式发射。
注意：这是一个私有信号。它可以用于信号连接，但用户不能发射。

### `[private signal] void QAbstractItemModel::columnsMoved(const QModelIndex &sourceParent, int sourceStart, int sourceEnd, const QModelIndex &destinationParent, int destinationColumn)`

**作用与语义：**

该信号是在模型内列移动后发出的。`sourceStart`到`sourceEnd`之间的项目，在给定`sourceParent`项下已移动到`destinationParent`，从列`destinationColumn`开始。
注意：连接到该信号的组件使用该信号来适应模型尺寸的变化。该信号只能由`QAbstractItemModel`实现发出，不能在子类代码中显式发射。
注意：这是一个私有信号。它可以用于信号连接，但用户不能发射。

### `[private signal] void QAbstractItemModel::columnsRemoved(const QModelIndex &parent, int first, int last)`

**作用与语义：**

该信号是在模型中移除列后发出的。被移除的项目包括在`first`到`last`之间，包含在给定`parent`项下的项目。
注意：连接到该信号的组件会用它来适应模型尺寸的变化。它只能通过`QAbstractItemModel`实现发射，不能在子类代码中显式发射。
注意：这是一个私有信号。它可以用于信号连接，但用户不能发射。

### `[protected] QModelIndex QAbstractItemModel::createIndex(int row, int column, const void *ptr = nullptr) const`

**作用与语义：**

为给定`row`和`column`创建模型索引，内部指针`ptr`。
使用`QSortFilterProxyModel`时，其索引有自己的内部指针。不建议在模型外部访问该内部指针。改用`data()`函数。
该函数提供了一个一致的接口，模型子类必须使用以创建模型索引。

### `[protected] QModelIndex QAbstractItemModel::createIndex(int row, int column, quintptr id) const`

**作用与语义：**

为给定`row`和`column`创建模型索引，内部标识符为`id`。
该函数提供了一个一致的接口，模型子类必须使用以创建模型索引。

### `[pure virtual invokable] QVariant QAbstractItemModel::data(const QModelIndex &index, int role = Qt::DisplayRole) const`

**作用与语义：**

返回`index`所指项在指定`role`下存储的数据。
注意：如果您没有可返回的值，请返回一个无效（默认构造）的 `QVariant`。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[signal] void QAbstractItemModel::dataChanged(const QModelIndex &topLeft, const QModelIndex &bottomRight, const QList<int> &roles = QList<int>())`

**作用与语义：**

每当现有项目中的数据发生变化时，该信号都会发出。
如果这些项属于同一父项，受影响的就是介于`topLeft`到`bottomRight`之间的。如果这些项没有相同的父项，则行为未定义。
在重新实现`setData()`函数时，必须显式地发出该信号。
可选的`roles`参数可用于指定实际被修改的数据角色。角色参数中的向量为空表示所有角色都应被视为修改。角色参数中元素的顺序无关紧要。

### `[virtual] bool QAbstractItemModel::dropMimeData(const QMimeData *data, Qt::DropAction action, int row, int column, const QModelIndex &parent)`

**作用与语义：**

处理拖放操作提供的 `data`，拖放操作以给定的 `action` 结束。
如果数据和动作由模型处理，返回`true`;否则返回`false`。
指定的`row`、`column`和`parent`表示操作结束时某项在模型中的位置。模型有责任在正确位置完成操作。
例如，`QTreeView`中物品的掉落动作可能导致新物品入为`row`、`column`和`parent`指定的物品的子项，或作为该物品的兄弟项目插入。
当`row`和`column`都为-1时，意味着丢弃的数据应直接被视为`parent`上的丢弃。通常这意味着将数据作为`parent`的子项附加。如果`row`和`column`大于或等于零，则表示丢弃发生在指定`row`之前，`column`在指定`parent`中。
调用`mimeTypes()`成员以获取可接受的MIME类型列表。该默认实现假设`mimeTypes()`的默认实现，返回单一默认MIME类型。如果你在自定义模型中重新实现`mimeTypes()`以返回多个MIME类型，必须重新实现该函数以利用它们。

### `[protected] void QAbstractItemModel::endInsertColumns()`

**作用与语义：**

结束列插入操作。
在子类中重新实现`insertColumns()`时，必须在将数据插入模型底层数据存储后调用该函数。

### `[protected] void QAbstractItemModel::endInsertRows()`

**作用与语义：**

结束行插入操作。
在子类中重新实现`insertRows()`时，必须在将数据插入模型底层数据存储后调用该函数。

### `[protected] void QAbstractItemModel::endMoveColumns()`

**作用与语义：**

结束列移动操作。
实现子类时，必须在移动模型底层数据存储数据后调用该函数。

### `[protected] void QAbstractItemModel::endMoveRows()`

**作用与语义：**

结束了一次行移动操作。
实现子类时，必须在移动模型底层数据存储数据后调用该函数。

### `[protected] void QAbstractItemModel::endRemoveColumns()`

**作用与语义：**

结束了一次柱子移除操作。
在子类中重新实现`removeColumns()`时，必须在移除模型底层数据存储中的数据后调用该函数。

### `[protected] void QAbstractItemModel::endRemoveRows()`

**作用与语义：**

结束了一排的移除操作。
在子类中重新实现`removeRows()`时，必须在从模型底层数据存储中移除数据后调用该函数。

### `[protected] void QAbstractItemModel::endResetModel()`

**作用与语义：**

完成模型复位操作。
你必须在重置模型或代理模型中的任何内部数据结构后调用该函数。
该功能会发出信号`modelReset()`。

### `[virtual invokable] void QAbstractItemModel::fetchMore(const QModelIndex &parent)`

**作用与语义：**

获取`parent`索引指定的父项目的任何可用数据。
如果你是逐步填充模型，请重新实现。
默认实现什么都不做。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[virtual invokable] Qt::ItemFlags QAbstractItemModel::flags(const QModelIndex &index) const`

**作用与语义：**

返回给定`index`的物品标志。
基类实现返回一组标志，使该项（`ItemIsEnabled`）启用，允许选择（`ItemIsSelectable`）。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[virtual invokable] bool QAbstractItemModel::hasChildren(const QModelIndex &parent = QModelIndex()) const`

**作用与语义：**

如果`parent`有子女，返回`true`;否则返回`false`。
用`rowCount()`来了解父母的子女数量。
注意，如果同一索引的标志被设置`Qt::ItemNeverHasChildren`，报告某个索引有 hasChildren 是未定义行为。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[invokable] bool QAbstractItemModel::hasIndex(int row, int column, const QModelIndex &parent = QModelIndex()) const`

**作用与语义：**

如果模型返回有效的`QModelIndex`，则返回`true` `row`，`column` `parent`，否则返回`false`。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[virtual invokable] QVariant QAbstractItemModel::headerData(int section, Qt::Orientation orientation, int role = Qt::DisplayRole) const`

**作用与语义：**

返回给定`role`和`section`的数据，并在头部中返回指定`orientation`。
对于水平头部，节号对应于列号。同样，对于竖向头部，节号对应行号。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[signal] void QAbstractItemModel::headerDataChanged(Qt::Orientation orientation, int first, int last)`

**作用与语义：**

每当头部发生变化时，该信号都会发出。`orientation`表示横向还是竖向头部发生了变化。头部中从`first`到`last`的部分需要更新。
在重新实现`setHeaderData()`函数时，必须显式地发出该信号。
如果你改变列数或行数，则不需要发出该信号，但可以使用开始/结束函数（详见`QAbstractItemModel`类描述中的子类部分）。

### `[pure virtual invokable] QModelIndex QAbstractItemModel::index(int row, int column, const QModelIndex &parent = QModelIndex()) const`

**作用与语义：**

返回由给定`row`、`column`和`parent`索引指定的模型中项目的索引。
在子类中重新实现该函数时，调用 `createIndex()` 生成模型索引，其他组件可以用来引用模型中的项目。
注意：该函数可通过元对象系统和QML调用。参见 `Q_INVOKABLE`。

### `[invokable] bool QAbstractItemModel::insertColumn(int column, const QModelIndex &parent = QModelIndex())`

**作用与语义：**

在指定`parent`的子项中，在给定`column`前插入一列。
如果插入了列，返回`true`;否则返回`false`。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[virtual invokable] bool QAbstractItemModel::insertColumns(int column, int count, const QModelIndex &parent = QModelIndex())`

**作用与语义：**

在支持该方法的模型中，`count`在给定`column`之前插入新列。每个新列中的项都是`parent`模型索引所表示项的子项。
如果`column`为0，列会被加在已有列之前。
如果`column` `columnCount()`，则这些列会附加到任何已有的列上。
如果`parent`没有子节点，则插入一行`count`列。
如果列成功插入，返回`true`;否则返回`false`。
基类实现什么都不做，只返回`false`。
如果你实现了自己的模型，如果你想支持插入，可以重新实现这个函数。或者，你也可以提供自己的 API 来修改数据。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[invokable] bool QAbstractItemModel::insertRow(int row, const QModelIndex &parent = QModelIndex())`

**作用与语义：**

在指定`parent`的子项中，在给定`row`前插入一行。
注意：该函数调用虚拟方法`insertRows`。
插入行时返回`true`;否则返回`false`。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[virtual invokable] bool QAbstractItemModel::insertRows(int row, int count, const QModelIndex &parent = QModelIndex())`

**作用与语义：**

注意：该函数的基类实现不做任何操作，返回`false`。
支持此操作的模型中，`count`行在给定`row`之前插入模型。新行中的项目将是`parent`模型索引所表示项的子节点。
如果`row`为0，则这些行会被置于父行中已有的行之前。
如果`row` `rowCount()`，则这些行会附加到父节点中已有的行上。
如果`parent`没有子节点，则插入一列`count`行。
如果行成功插入，返回`true`;否则返回`false`。
如果你实现了自己的模型，如果你想支持插入，可以重新实现这个函数。或者，你也可以提供自己的 API 来修改数据。无论哪种情况，你都需要调用 `beginInsertRows()` 和 `endInsertRows()`，通知其他组件模型发生了变化。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[virtual] QMap<int, QVariant> QAbstractItemModel::itemData(const QModelIndex &index) const`

**作用与语义：**

返回一个映射，包含模型中所有预定义角色的值，该项目在给定`index`。
如果你想将默认行为扩展到地图中包含自定义角色，可以重新实现这个函数。

### `[signal] void QAbstractItemModel::layoutAboutToBeChanged(const QList<QPersistentModelIndex> &parents = QList<QPersistentModelIndex>(), QAbstractItemModel::LayoutChangeHint hint = QAbstractItemModel::NoLayoutChangeHint)`

**作用与语义：**

该信号在模型布局变更前发出。连接到该信号的组件利用它来适应模型布局的变化。
子类在发出 layoutAboutToBeChanged() 后应更新任何持久模型索引。
可选的`parents`参数用于更具体地通知模型布局的哪些部分正在发生变化。空列表表示整个模型布局发生了变化。`parents`列表中元素的顺序并不重要。可选的`hint`参数用于提示模型重新布局时发生的情况。

### `[signal] void QAbstractItemModel::layoutChanged(const QList<QPersistentModelIndex> &parents = QList<QPersistentModelIndex>(), QAbstractItemModel::LayoutChangeHint hint = QAbstractItemModel::NoLayoutChangeHint)`

**作用与语义：**

每当模型暴露的物品布局发生变化时，都会发出该信号;例如，当模型被排序时。当视图接收到该信号时，应更新物品布局以反映这一变化。
在子类 `QAbstractItemModel` 或 `QAbstractProxyModel` 时，确保在更改项目顺序或数据结构之前先发出 `layoutAboutToBeChanged()`，并在更改布局后 exupd()。
可选的`parents`参数用于更具体地通知模型布局的哪些部分正在发生变化。空列表表示整个模型布局发生了变化。`parents`列表中元素的顺序并不重要。可选的`hint`参数用于在模型重新布局时提供提示。
子类应在发送 layoutChanged() 之前更新任何持久模型索引。换句话说，当结构发生变化时：
- 发射`layoutAboutToBeChanged`
- 记住将要改变的`QModelIndex`
- 更新您的内部数据
- 叫来`changePersistentIndex()`
- 发射布局已更改

### `[virtual invokable] QModelIndexList QAbstractItemModel::match(const QModelIndex &start, int role, const QVariant &value, int hits = 1, Qt::MatchFlags flags = Qt::MatchFlags(Qt::MatchStartsWith|Qt::MatchWrap)) const`

**作用与语义：**

返回`start`索引列中存储在指定`role`下的数据与指定`value`匹配的项索引列表。搜索方式由给出的`flags`定义。返回的列表可能是空的。还请注意，如果使用代理模型，列表中结果的顺序可能与模型中的顺序不一致。结果的顺序不可依赖。
搜索从`start`索引开始，持续直到匹配数据项数等于`hits`，搜索到达最后一行，或再次达到`start`——具体取决于`flags`中是否指定`MatchWrap`。如果你想搜索所有匹配的项目，使用`hits` = -1。
默认情况下，该函数会对所有项目进行环绕、基于字符串的比较，搜索以`value`指定搜索词开头的项目。
注意：该函数的默认实现仅搜索列。重新实现该函数以包含不同的搜索行为。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[virtual] QMimeData *QAbstractItemModel::mimeData(const QModelIndexList &indexes) const`

**作用与语义：**

返回一个包含序列化数据项的对象，对应指定`indexes`列表。描述编码数据的格式来自`mimeTypes()`函数。该默认实现使用`mimeTypes()`默认实现返回的默认MIME类型。如果你在自定义模型中重新实现`mimeTypes()`以返回更多MIME类型，请重新实现该函数以利用这些类型。
如果`indexes`列表为空，或没有支持的MIME类型，则返回`nullptr`而非序列化的空列表。

### `[virtual] QStringList QAbstractItemModel::mimeTypes() const`

**作用与语义：**

返回允许的 MIME 类型列表。默认情况下，内置模型和视图使用内部 MIME 类型：`application/x-qabstractitemmodeldatalist`。
在自定义模型中实现拖放支持时，如果你返回的数据格式不是默认的内部 MIME 类型，请重新实现这个函数，返回你的 MIME 类型列表。
如果你在自定义模型中重新实现该函数，也必须重新实现调用它的成员函数：`mimeData()` 和 `dropMimeData()`。

### `[private signal] void QAbstractItemModel::modelAboutToBeReset()`

**作用与语义：**

该信号在调用`beginResetModel()`时发出，模型内部状态（例如持久模型索引）尚未失效。
注意：这是一个私有信号。它可以用于信号连接，但用户不能发射。

### `[private signal] void QAbstractItemModel::modelReset()`

**作用与语义：**

当`endResetModel()`被调用时，该信号会在模型内部状态（例如持久模型索引）失效后发出。
注意，如果模型被重置，应视为之前从该模型中检索的所有信息无效。这包括但不限于`rowCount()`和`columnCount()`、`flags()`、通过`data()`检索的数据以及`roleNames()`。
注意：这是一个私有信号。它可以用于信号连接，但用户不能发射。

### `[invokable] bool QAbstractItemModel::moveColumn(const QModelIndex &sourceParent, int sourceColumn, const QModelIndex &destinationParent, int destinationChild)`

**作用与语义：**

支持这个功能的型号，`sourceColumn`从`sourceParent`提升到`destinationChild`不到`destinationParent`。
如果列成功移动，返回`true`;否则返回`false`。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[virtual invokable] bool QAbstractItemModel::moveColumns(const QModelIndex &sourceParent, int sourceColumn, int count, const QModelIndex &destinationParent, int destinationChild)`

**作用与语义：**

在支持此方法的模型中，将`count`列从父`sourceParent`下的给定`sourceColumn`移动到父`destinationParent`下的第`destinationChild`列。
如果列成功移动，返回`true`;否则返回`false`。
基类实现什么都不做，只返回`false`。
如果你实现了自己的模型，如果你想支持移动，可以重新实现这个函数。或者，你也可以提供自己的 API 来修改数据。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[invokable] bool QAbstractItemModel::moveRow(const QModelIndex &sourceParent, int sourceRow, const QModelIndex &destinationParent, int destinationChild)`

**作用与语义：**

支持这种功能的模型，`sourceRow`从`sourceParent`提升到`destinationChild` `destinationParent`。
如果行成功移动，返回`true`;否则返回`false`。
注意：该函数可以通过元对象系统和QML调用。参见 `Q_INVOKABLE`。

### `[virtual invokable] bool QAbstractItemModel::moveRows(const QModelIndex &sourceParent, int sourceRow, int count, const QModelIndex &destinationParent, int destinationChild)`

**作用与语义：**

支持此操作的模型`count`从父`sourceParent`下的给定`sourceRow`行移动到父`destinationParent`下的行`destinationChild`。
如果行成功移动，返回`true`;否则返回`false`。
基类实现什么都不做，返回`false`。
如果你实现了自己的模型，如果你想支持移动，可以重新实现这个函数。或者，你也可以提供自己的 API 来修改数据。
注意：该函数可通过元对象系统和QML调用。参见 `Q_INVOKABLE`。

### `[virtual, since 6.0] void QAbstractItemModel::multiData(const QModelIndex &index, QModelRoleDataSpan roleDataSpan) const`

**作用与语义：**

用所需数据填充给`roleDataSpan`，针对给定`index`。
默认实现会对该区间中的每个角色调用 `data()`。子类可以重新实现该函数，以更高效地向视图提供数据：
在上面的摘要中，`index`对整个调用都是相同的。这意味着访问必要的数据结构以获取`index`信息只能做一次（将相关代码从循环中提起）。
鼓励使用`QModelRoleData::setData()`或类似的`QVariant::setValue()`，而不是单独构造`QVariant`并使用纯赋值算符;这是因为前者允许重复使用存储在`QModelRoleData`中的`QVariant`对象已分配的内存，而后者总是分配新变体，然后销毁旧变体。
注意，视图可能调用了 multiData()，其间隔在之前调用中已被使用，因此可能已经包含部分数据。因此，如果模型无法返回给定角色的数据，则必须清除对应`QModelRoleData`对象中的数据。这可以通过调用 `QModelRoleData::clearData()`，或者设置默认构造`QVariant`等方式实现。未清除数据会导致视图误以为“旧”数据应用于相应角色。
最后，为了避免代码重复，子类也可能决定用multiData()重新实现`data()`，通过仅提供一个元素的张成：
注意：模型不得修改跨内角色或重组跨度元素。这样做会导致行为未定义。
注意：将无效模型索引传递给该函数是违法的。

**官方示例：**

```cpp
 void MyModel::multiData(const QModelIndex &index, QModelRoleDataSpan roleDataSpan) const
 {
     for (QModelRoleData &roleData : roleDataSpan) {
         int role = roleData.role();

         // ... obtain the data for index and role ...

         roleData.setData(result);
     }
 }
```

### `[pure virtual invokable] QModelIndex QAbstractItemModel::parent(const QModelIndex &index) const`

**作用与语义：**

返回模型项目的父项，并返回给定`index`。如果该项没有父项，则返回无效`QModelIndex`。
在暴露树状数据结构的模型中，一个常见的惯例是只有第一列的项有子节点。在这种情况下，在子类中重新实现该函数时，返回`QModelIndex`的列将为0。
在子类中重新实现该函数时，要注意避免调用`QModelIndex`成员函数，如`QModelIndex::parent()`，因为属于你模型的索引只会调用你的实现，导致无限递归。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[protected] QModelIndexList QAbstractItemModel::persistentIndexList() const`

**作用与语义：**

返回模型中作为持久索引存储的索引列表。

### `[invokable] bool QAbstractItemModel::removeColumn(int column, const QModelIndex &parent = QModelIndex())`

**作用与语义：**

从指定`parent`的子项中移除给定的`column`。
如果列被移除，返回`true`;否则返回`false`。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[virtual invokable] bool QAbstractItemModel::removeColumns(int column, int count, const QModelIndex &parent = QModelIndex())`

**作用与语义：**

在支持此功能`count`模型中，移除父`parent`下以给定`column`为起始的列。
如果列被成功移除，返回`true`;否则返回`false`。
基类实现什么都不做，返回`false`。
如果你实现了自己的模型，如果你想支持删除，可以重新实现这个函数。或者，你也可以提供自己的 API 来修改数据。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[invokable] bool QAbstractItemModel::removeRow(int row, const QModelIndex &parent = QModelIndex())`

**作用与语义：**

从指定`parent`的子项中移除给定的`row`。
如果该行被移除，返回`true`;否则返回`false`。
这是一个调用`removeRows()`的便利函数。`removeRows()`的`QAbstractItemModel`实现不做任何事。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[virtual invokable] bool QAbstractItemModel::removeRows(int row, int count, const QModelIndex &parent = QModelIndex())`

**作用与语义：**

在支持该支持的模型中，会从模型中移除从父 `parent`下以给定`row`为起始的`count`行。
如果行被成功移除，返回`true`;否则返回`false`。
基类实现什么都不做，只返回`false`。
如果你实现了自己的模型，如果你想支持删除，可以重新实现这个函数。或者，你也可以提供自己的 API 来修改数据。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[virtual protected slot] void QAbstractItemModel::resetInternalData()`

**作用与语义：**

该槽位在模型内部数据被清除、重置时被调用。
该槽位提供了具体代理模型子类的便利性，例如维护额外数据的`QSortFilterProxyModel`子类。
注意：由于错误，该槽位在Qt 5.0中缺失。

**官方示例：**

```cpp
 class CustomDataProxy : public QSortFilterProxyModel
 {
     Q_OBJECT
 public:
     CustomDataProxy(QObject *parent)
       : QSortFilterProxyModel(parent)
     {
     }

     //...

     QVariant data(const QModelIndex &index, int role) const override
     {
         if (role != Qt::BackgroundRole)
             return QSortFilterProxyModel::data(index, role);

         if (m_customData.contains(index.row()))
             return m_customData.value(index.row());
         return QSortFilterProxyModel::data(index, role);
     }

 private slots:
     void resetInternalData()
     {
         m_customData.clear();
     }

 private:
   QHash<int, QVariant> m_customData;
 };
```

### `[virtual slot] void QAbstractItemModel::revert()`

**作用与语义：**

让模型知道应丢弃缓存信息。该函数通常用于行编辑。

### `[virtual] QHash<int, QByteArray> QAbstractItemModel::roleNames() const`

**作用与语义：**

返回模特的角色名。
Qt 默认设置的角色名称如下：
- `Qt Role`：QML角色名称
- `Qt::DisplayRole`：显示
- `Qt::DecorationRole`：装饰
- `Qt::EditRole`：编辑
- `Qt::ToolTipRole`：工具提示
- `Qt::StatusTipRole`：statusTip
- `Qt::WhatsThisRole`：这是什么

### `[pure virtual invokable] int QAbstractItemModel::rowCount(const QModelIndex &parent = QModelIndex()) const`

**作用与语义：**

返回给定`parent`下的行数。当父单位有效时，表示 rowCount 返回的是父节点的子节点数。
注意：在实现基于表的模型时，当父模型有效时，rowCount() 应返回 0。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[private signal] void QAbstractItemModel::rowsAboutToBeInserted(const QModelIndex &parent, int start, int end)`

**作用与语义：**

该信号在插入行前发出。新项目将位于`start`和`end`之间，位于给定的`parent`项下方。
注意：连接到该信号的组件会用它来适应模型尺寸的变化。它只能由`QAbstractItemModel`实现发出，不能在子类代码中显式发射。
注意：这是一个私有信号。它可以用于信号连接，但用户不能发射。

### `[private signal] void QAbstractItemModel::rowsAboutToBeMoved(const QModelIndex &sourceParent, int sourceStart, int sourceEnd, const QModelIndex &destinationParent, int destinationRow)`

**作用与语义：**

该信号在模型内移动行之前发出。将被移动的项目是介于`sourceStart`到`sourceEnd`之间，包含在给定`sourceParent`项下的物品。它们会从第`destinationRow`行开始移动到`destinationParent`。
注意：连接到该信号的组件使用该信号来适应模型尺寸的变化。该信号只能由`QAbstractItemModel`实现发出，不能在子类代码中显式发射。
注意：这是一个私有信号。它可以用于信号连接，但用户不能发射。

### `[private signal] void QAbstractItemModel::rowsAboutToBeRemoved(const QModelIndex &parent, int first, int last)`

**作用与语义：**

该信号在模型移除行之前发出。将被移除的项目是`first`到`last`包含在该`parent`项下的项目。
注意：连接到该信号的组件会用它来适应模型尺寸的变化。它只能通过`QAbstractItemModel`实现发出，不能在子类代码中显式发射。
注意：这是一个私有信号。它可以用于信号连接，但用户不能发射。

### `[private signal] void QAbstractItemModel::rowsInserted(const QModelIndex &parent, int first, int last)`

**作用与语义：**

该信号是在模型中插入行后发出的。新项目包括在`first`到`last`之间，包含在给定`parent`项下的项目。
注意：连接到该信号的组件会用它来适应模型尺寸的变化。它只能由`QAbstractItemModel`实现发出，不能在子类代码中显式发射。
注意：这是一个私有信号。它可以用于信号连接，但用户不能发射。

### `[private signal] void QAbstractItemModel::rowsMoved(const QModelIndex &sourceParent, int sourceStart, int sourceEnd, const QModelIndex &destinationParent, int destinationRow)`

**作用与语义：**

该信号是在模型内行移动后发出的。`sourceStart`到`sourceEnd`之间的项目，在给定`sourceParent`项下被移至`destinationParent`，从`destinationRow`行开始。
注意：连接到该信号的组件会用它来适应模型尺寸的变化。它只能由`QAbstractItemModel`实现发射，不能在子类代码中显式发射。
注意：这是一个私有信号。它可以用于信号连接，但用户不能发射。

### `[private signal] void QAbstractItemModel::rowsRemoved(const QModelIndex &parent, int first, int last)`

**作用与语义：**

该信号是在模型中移除行后发出的。被移除的项目包括在`first`到`last`之间的项目，包含在给定`parent`项下。
注意：连接到该信号的组件会用它来适应模型尺寸的变化。它只能由`QAbstractItemModel`实现发出，不能在子类代码中显式发射。
注意：这是一个私有信号。它可以用于信号连接，但用户不能发射。

### `[virtual invokable] bool QAbstractItemModel::setData(const QModelIndex &index, const QVariant &value, int role = Qt::EditRole)`

**作用与语义：**

将`index`处物品的 `role` 数据设置为 `value`。
成功时返回`true`;否则返回`false`。
如果数据设置成功，应发出`dataChanged()`信号。
基类实现返回`false`。该函数和`data()`必须重新实现以适应可编辑模型。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[virtual] bool QAbstractItemModel::setHeaderData(int section, Qt::Orientation orientation, const QVariant &value, int role = Qt::EditRole)`

**作用与语义：**

在头部设置给定`role`和`section`数据，并指定`orientation`到所提供`value`。
如果头部数据更新，返回`true`;否则返回`false`。
在重新实现此功能时，必须显式地发出`headerDataChanged()`信号。

### `[virtual] bool QAbstractItemModel::setItemData(const QModelIndex &index, const QMap<int, QVariant> &roles)`

**作用与语义：**

将`index`项的角色数据设置为每个`Qt::ItemDataRole`的 `roles` 关联值。
成功时返回`true`;若成功则返回`false`。
未在 `roles` 中的职位不会被修改。

### `[virtual invokable] QModelIndex QAbstractItemModel::sibling(int row, int column, const QModelIndex &index) const`

**作用与语义：**

`row`退还兄弟姐妹，`index` `column`物品，或者如果该地点没有兄弟姐妹，则`QModelIndex`无效。
sibling() 只是一个方便函数，用来查找该项的父项，并用它检索指定`row`和`column`子项的索引。
该方法可选择性地覆盖以实现特定优化。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[virtual invokable] void QAbstractItemModel::sort(int column, Qt::SortOrder order = Qt::AscendingOrder)`

**作用与语义：**

按给定`order`中的`column`排序模型。
基础类实现什么都不做。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[virtual] QSize QAbstractItemModel::span(const QModelIndex &index) const`

**作用与语义：**

返回由`index`表示的项的行和列跨。
注：目前不使用跨度。

### `[virtual slot] bool QAbstractItemModel::submit()`

**作用与语义：**

让模型知道应将缓存信息提交到永久存储。该功能通常用于行编辑。
如果没有错误，返回`true`;否则返回`false`。

### `[virtual] Qt::DropActions QAbstractItemModel::supportedDragActions() const`

**作用与语义：**

返回该模型中数据支持的动作。
默认实现返回`supportedDropActions()`。如果你希望支持更多操作，可以重新实现这个函数。
当发生拖拽时，`QAbstractItemView::startDrag()` 默认使用 supportedDragActions() 作为值。

### `[virtual] Qt::DropActions QAbstractItemModel::supportedDropActions() const`

**作用与语义：**

返回该模型支持的投放动作。
默认实现返回`Qt::CopyAction`。如果你希望支持额外的操作，请重新实现这个函数。你还必须重新实现`dropMimeData()`函数来处理这些额外的操作。

### `enum class CheckIndexOption { NoOption, IndexIsValid, DoNotUseParent, ParentIsInvalid }`

**作用与语义：**

此枚举可用于控制`QAbstractItemModel::checkIndex()`执行的检查。
- `QAbstractItemModel::CheckIndexOption::NoOption`：`0x0000`；未指定任何检查选项。
- `QAbstractItemModel::CheckIndexOption::IndexIsValid`：`0x0001`；检查传递给`QAbstractItemModel::checkIndex()`的模型索引是否为有效的模型索引。
- `QAbstractItemModel::CheckIndexOption::DoNotUseParent`：`0x0002`；不会执行与使用传递给`QAbstractItemModel::checkIndex()`的索引的父项相关的任何检查。
- `QAbstractItemModel::CheckIndexOption::ParentIsInvalid`：`0x0004`；检查传递给`QAbstractItemModel::checkIndex()`的模型索引的父项是否为无效的模型索引。如果同时指定了此选项和DoNotUseParent，则忽略此选项。
CheckIndexOptions类型是QFlags<CheckIndexOption>的typedef。它存储CheckIndexOption值的或组合。

### `flags CheckIndexOptions`

**作用与语义：**

此枚举可用于控制`QAbstractItemModel::checkIndex()`执行的检查。
- `QAbstractItemModel::CheckIndexOption::NoOption`：`0x0000`；未指定任何检查选项。
- `QAbstractItemModel::CheckIndexOption::IndexIsValid`：`0x0001`；检查传递给`QAbstractItemModel::checkIndex()`的模型索引是否为有效的模型索引。
- `QAbstractItemModel::CheckIndexOption::DoNotUseParent`：`0x0002`；不会执行与使用传递给`QAbstractItemModel::checkIndex()`的索引的父项相关的任何检查。
- `QAbstractItemModel::CheckIndexOption::ParentIsInvalid`：`0x0004`；检查传递给`QAbstractItemModel::checkIndex()`的模型索引的父项是否为无效的模型索引。如果同时指定了此选项和DoNotUseParent，则忽略此选项。
CheckIndexOptions类型是QFlags<CheckIndexOption>的typedef。它存储CheckIndexOption值的或组合。

## 6. 深入实践与常见坑

### 生命周期和资源边界

模型应比视图活得足够久，视图销毁时不会自动替业务容器释放资源。模型变化必须使用对应的 begin/end 协议或精确通知，不能只改容器后期待视图自行发现。取到的 QModelIndex 只在模型允许的生命周期内有效。

### 状态和错误边界

区分当前索引、选择模型、编辑状态、数据角色和模型结构变化。`dataChanged` 表示已有项目的数据变化，行列插入/删除表示结构变化，`modelReset` 会让旧索引整体失效。

### 线程边界

模型通常在 GUI 线程被视图访问。后台线程不要直接修改正在显示的模型；应在正确线程汇总数据，再通过通知协议更新，或使用线程安全的数据交换层。

### 最容易出现的错误

不要返回失效 QModelIndex；插入/删除必须成对 begin/end；区分 DisplayRole/EditRole；不要在 data() 中做昂贵或有副作用的工作。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QAbstractItemModel` 所属机制类型：模型/视图协议。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
