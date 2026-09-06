# QIdentityProxyModel

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QIdentityProxyModel` 是 模型/视图协议 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QIdentityProxyModel` 是模型/视图体系中的数据模型类型，向视图提供索引、角色数据和结构变化通知。

**内部模型：** 视图不应该直接操作底层容器；它通过 QModelIndex 和 data roles 查询模型。模型必须准确维护索引有效性以及插入、删除、移动时的通知顺序。

**适用场景：** 需要把自定义数据接入 QListView、QTableView、QTreeView 或代理模型时使用。

**典型调用链：** 准备数据源 -> 实现/配置模型 -> 连接 view -> 通过 data/flags/setData 读写 -> 发出 dataChanged 或 begin/end 结构通知。

**先记住的坑：** 不要在 data() 中修改数据；不要返回过期索引；不要用全量 reset 代替精确结构通知，除非确实无法描述变化。

## 2. 依赖与对象关系

- 头文件：`#include <QIdentityProxyModel>`
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

### 公有函数

- `QIdentityProxyModel(QObject *parent = nullptr)`
- `virtual ~QIdentityProxyModel()`
- `(since 6.8) bool handleSourceDataChanges() const`
- `(since 6.8) bool handleSourceLayoutChanges() const`

### 重实现的公有函数

- `virtual int columnCount(const QModelIndex &parent = QModelIndex()) const override`
- `virtual bool dropMimeData(const QMimeData *data, Qt::DropAction action, int row, int column, const QModelIndex &parent) override`
- `virtual QVariant headerData(int section, Qt::Orientation orientation, int role = Qt::DisplayRole) const override`
- `virtual QModelIndex index(int row, int column, const QModelIndex &parent = QModelIndex()) const override`
- `virtual bool insertColumns(int column, int count, const QModelIndex &parent = QModelIndex()) override`
- `virtual bool insertRows(int row, int count, const QModelIndex &parent = QModelIndex()) override`
- `virtual QModelIndex mapFromSource(const QModelIndex &sourceIndex) const override`
- `virtual QItemSelection mapSelectionFromSource(const QItemSelection &selection) const override`
- `virtual QItemSelection mapSelectionToSource(const QItemSelection &selection) const override`
- `virtual QModelIndex mapToSource(const QModelIndex &proxyIndex) const override`
- `virtual QModelIndexList match(const QModelIndex &start, int role, const QVariant &value, int hits = 1, Qt::MatchFlags flags = Qt::MatchFlags(Qt::MatchStartsWith|Qt::MatchWrap)) const override`
- `virtual bool moveColumns(const QModelIndex &sourceParent, int sourceColumn, int count, const QModelIndex &destinationParent, int destinationChild) override`
- `virtual bool moveRows(const QModelIndex &sourceParent, int sourceRow, int count, const QModelIndex &destinationParent, int destinationChild) override`
- `virtual QModelIndex parent(const QModelIndex &child) const override`
- `virtual bool removeColumns(int column, int count, const QModelIndex &parent = QModelIndex()) override`
- `virtual bool removeRows(int row, int count, const QModelIndex &parent = QModelIndex()) override`
- `virtual int rowCount(const QModelIndex &parent = QModelIndex()) const override`
- `virtual void setSourceModel(QAbstractItemModel *newSourceModel) override`
- `virtual QModelIndex sibling(int row, int column, const QModelIndex &idx) const override`

### 保护函数

- `(since 6.8) void setHandleSourceDataChanges(bool b)`
- `(since 6.8) void setHandleSourceLayoutChanges(bool b)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[explicit] QIdentityProxyModel::QIdentityProxyModel(QObject *parent = nullptr)`

**作用与语义：**

构造与给定`parent`的恒等模型。

### `[virtual noexcept] QIdentityProxyModel::~QIdentityProxyModel()`

**作用与语义：**

摧毁了这种身份模型。

### `[override virtual] int QIdentityProxyModel::columnCount(const QModelIndex &parent = QModelIndex()) const`

**作用与语义：**

重实现自：`QAbstractItemModel::columnCount`（const QModelIndex 和 parent） const.
返回给定`parent`子节点的列数。
在大多数子类中，列的数量与`parent`无关。
注意：在实现基于表的模型时，当父模型有效时，columnCount() 应返回 0。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[override virtual] bool QIdentityProxyModel::dropMimeData(const QMimeData *data, Qt::DropAction action, int row, int column, const QModelIndex &parent)`

**作用与语义：**

重实现自：`QAbstractProxyModel::dropMimeData`（const QMimeData *data， Qt：:D ropAction action， int row， int column， const QModelIndex &parent）.

### `[since 6.8] bool QIdentityProxyModel::handleSourceDataChanges() const`

**作用与语义：**

如果该代理模型处理源模型数据变更，返回`true`;否则返回`false`。

### `[since 6.8] bool QIdentityProxyModel::handleSourceLayoutChanges() const`

**作用与语义：**

如果该代理模型处理源模型布局的变更，返回`true`，否则返回`false`。

### `[override virtual] QVariant QIdentityProxyModel::headerData(int section, Qt::Orientation orientation, int role = Qt::DisplayRole) const`

**作用与语义：**

重实现自：`QAbstractProxyModel::headerData`（整数节，Qt：：Orientation orientation， int role）const.

### `[override virtual] QModelIndex QIdentityProxyModel::index(int row, int column, const QModelIndex &parent = QModelIndex()) const`

**作用与语义：**

重实现自：`QAbstractItemModel::index`（整数行，整数列，cont QModelIndex 和parent）const.
返回由给定`row`、`column`和`parent`索引指定模型中项目的索引。
在子类中重新实现该函数时，调用 `createIndex()` 生成模型索引，其他组件可以用来引用模型中的项。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[override virtual] bool QIdentityProxyModel::insertColumns(int column, int count, const QModelIndex &parent = QModelIndex())`

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

### `[override virtual] bool QIdentityProxyModel::insertRows(int row, int count, const QModelIndex &parent = QModelIndex())`

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

### `[override virtual] QModelIndex QIdentityProxyModel::mapFromSource(const QModelIndex &sourceIndex) const`

**作用与语义：**

重实现自：`QAbstractProxyModel::mapFromSource`（const QModelIndex & sourceIndex） const.
重新实现该函数，返回代理模型中对应源模型`sourceIndex`的模型索引。
注意：该函数可通过元对象系统和QML调用。参见 `Q_INVOKABLE`。

### `[override virtual] QItemSelection QIdentityProxyModel::mapSelectionFromSource(const QItemSelection &selection) const`

**作用与语义：**

Reimpments： `QAbstractProxyModel::mapSelectionFromSource`（const QItemSelection &sourceSelection） const.
返回从指定 `sourceSelection`映射的代理选择。
重新实现此方法，将源选择映射到代理选择。
注意：该函数可通过元对象系统和QML调用。参见 `Q_INVOKABLE`。

### `[override virtual] QItemSelection QIdentityProxyModel::mapSelectionToSource(const QItemSelection &selection) const`

**作用与语义：**

Reimpments： `QAbstractProxyModel::mapSelectionToSource`（const QItemSelection &proxySelection） const.
返回从指定`proxySelection`映射的源选择。
重新实现该方法，将代理选择映射到源选择。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[override virtual] QModelIndex QIdentityProxyModel::mapToSource(const QModelIndex &proxyIndex) const`

**作用与语义：**

重实现自：`QAbstractProxyModel::mapToSource`（const QModelIndex & proxyIndex） const.
重新实现该函数，返回源模型中的模型索引，对应代理模型中的`proxyIndex`。
注意：该函数可通过元对象系统和QML调用。参见 `Q_INVOKABLE`。

### `[override virtual] QModelIndexList QIdentityProxyModel::match(const QModelIndex &start, int role, const QVariant &value, int hits = 1, Qt::MatchFlags flags = Qt::MatchFlags(Qt::MatchStartsWith|Qt::MatchWrap)) const`

**作用与语义：**

重实现自：`QAbstractItemModel::match`（const QModelIndex &start， int role， const QVariant &value， int hits， Qt：：MatchFlags flags） const.
返回`start`索引列中存储在指定`value`下的数据与`role`匹配的项的索引列表。搜索的执行方式由给出的`flags`定义。返回的列表可能是空的。还请注意，如果使用代理模型，列表中结果的顺序可能与模型中的顺序不一致。结果的顺序不能被依赖。
搜索从`start`索引开始，持续直到匹配数据项数达到`hits`，搜索到达最后一行，或再次达到`start`——具体取决于`flags`中是否指定了`MatchWrap`。如果你想搜索所有匹配的项目，使用`hits` = -1。
默认情况下，该函数会对所有项目进行环绕、基于字符串的比较，搜索以`value`指定搜索词开头的项目。
注意：该函数的默认实现仅搜索列。重新实现该函数以包含不同的搜索行为。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[override virtual] bool QIdentityProxyModel::moveColumns(const QModelIndex &sourceParent, int sourceColumn, int count, const QModelIndex &destinationParent, int destinationChild)`

**作用与语义：**

重实现自：`QAbstractItemModel::moveColumns`（const QModelIndex & sourceParent， int sourceColumn， int count， const QModelIndex &destinationParent， int destinationChild）。
在支持该支持的模型中，从父`sourceParent`下`count`列开始，从给定`sourceColumn`开始，移动到父`destinationParent`下列`destinationChild`。
如果列成功移动，返回`true`;否则返回`false`。
基类实现什么都不做，返回`false`。
如果你实现了自己的模型，如果你想支持移动，可以重新实现这个函数。或者，你也可以提供自己的 API 来修改数据。
注意：该函数可通过元对象系统和QML调用。参见 `Q_INVOKABLE`。

### `[override virtual] bool QIdentityProxyModel::moveRows(const QModelIndex &sourceParent, int sourceRow, int count, const QModelIndex &destinationParent, int destinationChild)`

**作用与语义：**

重实现自：`QAbstractItemModel::moveRows`（const QModelIndex & sourceParent， int sourceRow， int count， const QModelIndex &destinationParent， int destinationChild）。
在支持此操作的模型中，将从父`sourceParent`下的给定`sourceRow`开始，`count`行移动到父`destinationParent`下行`destinationChild`。
如果行成功移动，返回`true`;否则返回`false`。
基类实现什么都不做，只返回`false`。
如果你实现了自己的模型，如果你想支持移动，可以重新实现这个函数。或者，你也可以提供自己的 API 来修改数据。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[override virtual] QModelIndex QIdentityProxyModel::parent(const QModelIndex &child) const`

**作用与语义：**

重实现自：`QAbstractItemModel::parent`（const QModelIndex & index） const.
返回模型项目的父项，并返回给定`index`。如果该项没有父项，则返回无效`QModelIndex`。
在暴露树状数据结构的模型中，一个常用的惯例是只有第一列的项有子节点。在这种情况下，在子类中重新实现该函数时，返回`QModelIndex`的列将为0。
在将该函数重新实现到子类中时，要注意避免调用`QModelIndex`成员函数，如`QModelIndex::parent()`，因为属于你模型的索引会直接调用你的实现，导致无限递归。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[override virtual] bool QIdentityProxyModel::removeColumns(int column, int count, const QModelIndex &parent = QModelIndex())`

**作用与语义：**

重构：`QAbstractItemModel::removeColumns`（整数列，整数计数，函数QModelIndex 和parent）。
在支持此功能的模型中，会从模型中移除`count`列，起始于父 `parent` 下给定`column`。
如果列被成功移除，返回 返回`true`;否则返回 `false`。
基类实现什么都不做，只返回`false`。
如果你实现了自己的模型，如果你想支持删除，可以重新实现这个函数。或者，你也可以提供自己的 API 来修改数据。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[override virtual] bool QIdentityProxyModel::removeRows(int row, int count, const QModelIndex &parent = QModelIndex())`

**作用与语义：**

重实现自：`QAbstractItemModel::removeRows`（整数行，整数计数，函数QModelIndex 和父）。
在支持此功能的模型中，会从模型中移除父`parent`下以给定`row`为起始的`count`行。
如果行被成功移除，返回`true`;否则返回`false`。
基类实现什么都不做，只返回`false`。
如果你实现了自己的模型，如果你想支持删除，可以重新实现这个函数。或者，你也可以提供自己的 API 来修改数据。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[override virtual] int QIdentityProxyModel::rowCount(const QModelIndex &parent = QModelIndex()) const`

**作用与语义：**

重实现自：`QAbstractItemModel::rowCount`（const QModelIndex & parent）const.
返回给定`parent`下的行数。当父节点有效时，表示 rowCount 返回的是父节点的子节点数。
注意：在实现基于表的模型时，当父模型有效时，rowCount() 应返回 0。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[protected, since 6.8] void QIdentityProxyModel::setHandleSourceDataChanges(bool b)`

**作用与语义：**

如果`b` `true`，该代理模型将处理源模型数据的变更（通过连接`QAbstractItemModel::dataChanged`信号）。
默认情况下，这个代理模型会处理源模型的数据变更。
在 `QIdentityProxyModel` 的子类中，如果你需要专门处理源模型数据的变更，将此设置为 `false` 可能很有用。
注意：调用此方法仅在调用`setSourceModel()`后才会生效。

### `[protected, since 6.8] void QIdentityProxyModel::setHandleSourceLayoutChanges(bool b)`

**作用与语义：**

如果`b` `true`，该代理模型将处理源模型布局的变更（通过连接`QAbstractItemModel::layoutAboutToBeChanged`和`QAbstractItemModel::layoutChanged`信号）。
默认情况下，这个代理模型会处理源模型布局的更改。
在 `QIdentityProxyModel` 的子类中，如果你需要特别处理源模型布局的更改，将此设置为 `false` 可能很有用。
注意：调用此方法仅在调用`setSourceModel()`后才会生效。

### `[override virtual] void QIdentityProxyModel::setSourceModel(QAbstractItemModel *newSourceModel)`

**作用与语义：**

重实现自：`QAbstractProxyModel::setSourceModel`（QAbstractItemModel *sourceModel）。
注意：此特性支持`QProperty`绑定。
该属性表示该代理模型的源模型。
注意：这是一个私有信号。它可以用于信号连接，但用户不能发射。

### `[override virtual] QModelIndex QIdentityProxyModel::sibling(int row, int column, const QModelIndex &idx) const`

**作用与语义：**

重实现自：`QAbstractProxyModel::sibling`（int 行，int column，const QModelIndex &idx） const.

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

`QIdentityProxyModel` 所属机制类型：模型/视图协议。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
