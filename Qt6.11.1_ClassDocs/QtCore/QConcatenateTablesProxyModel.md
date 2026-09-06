# QConcatenateTablesProxyModel

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QConcatenateTablesProxyModel` 是 模型/视图协议 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QConcatenateTablesProxyModel` 是模型/视图体系中的数据模型类型，向视图提供索引、角色数据和结构变化通知。

**内部模型：** 视图不应该直接操作底层容器；它通过 QModelIndex 和 data roles 查询模型。模型必须准确维护索引有效性以及插入、删除、移动时的通知顺序。

**适用场景：** 需要把自定义数据接入 QListView、QTableView、QTreeView 或代理模型时使用。

**典型调用链：** 准备数据源 -> 实现/配置模型 -> 连接 view -> 通过 data/flags/setData 读写 -> 发出 dataChanged 或 begin/end 结构通知。

**先记住的坑：** 不要在 data() 中修改数据；不要返回过期索引；不要用全量 reset 代替精确结构通知，除非确实无法描述变化。

## 2. 依赖与对象关系

- 头文件：`#include <QConcatenateTablesProxyModel>`
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

### 公有函数

- `QConcatenateTablesProxyModel(QObject *parent = nullptr)`
- `virtual ~QConcatenateTablesProxyModel()`
- `void addSourceModel(QAbstractItemModel *sourceModel)`
- `QModelIndex mapFromSource(const QModelIndex &sourceIndex) const`
- `QModelIndex mapToSource(const QModelIndex &proxyIndex) const`
- `void removeSourceModel(QAbstractItemModel *sourceModel)`
- `QList<QAbstractItemModel *> sourceModels() const`

### 重实现的公有函数

- `virtual bool canDropMimeData(const QMimeData *data, Qt::DropAction action, int row, int column, const QModelIndex &parent) const override`
- `virtual int columnCount(const QModelIndex &parent = QModelIndex()) const override`
- `virtual QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const override`
- `virtual bool dropMimeData(const QMimeData *data, Qt::DropAction action, int row, int column, const QModelIndex &parent) override`
- `virtual Qt::ItemFlags flags(const QModelIndex &index) const override`
- `virtual QVariant headerData(int section, Qt::Orientation orientation, int role = Qt::DisplayRole) const override`
- `virtual QModelIndex index(int row, int column, const QModelIndex &parent = QModelIndex()) const override`
- `virtual QMap<int, QVariant> itemData(const QModelIndex &proxyIndex) const override`
- `virtual QMimeData * mimeData(const QModelIndexList &indexes) const override`
- `virtual QStringList mimeTypes() const override`
- `virtual QModelIndex parent(const QModelIndex &index) const override`
- `(since 6.9.0) virtual QHash<int, QByteArray> roleNames() const override`
- `virtual int rowCount(const QModelIndex &parent = QModelIndex()) const override`
- `virtual bool setData(const QModelIndex &index, const QVariant &value, int role = Qt::EditRole) override`
- `virtual bool setItemData(const QModelIndex &proxyIndex, const QMap<int, QVariant> &roles) override`
- `virtual QSize span(const QModelIndex &index) const override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[explicit] QConcatenateTablesProxyModel::QConcatenateTablesProxyModel(QObject *parent = nullptr)`

**作用与语义：**

构造一个连接行代理模型，`parent`。

### `[virtual noexcept] QConcatenateTablesProxyModel::~QConcatenateTablesProxyModel()`

**作用与语义：**

这破坏了代理模型。

### `void QConcatenateTablesProxyModel::addSourceModel(QAbstractItemModel *sourceModel)`

**作用与语义：**

在所有之前添加的源模型下方添加一个源模型`sourceModel`。
`sourceModel`的所有权不受此影响。
同一源模型不能重复添加。

### `[override virtual] bool QConcatenateTablesProxyModel::canDropMimeData(const QMimeData *data, Qt::DropAction action, int row, int column, const QModelIndex &parent) const`

**作用与语义：**

Reimplements： `QAbstractItemModel::canDropMimeData`（const QMimeData *data， Qt：:D ropAction action， int row， int column， const QModelIndex &parent） const.
返回`true`模型是否能接受`data`的删除。该默认实现仅检查`data` `mimeTypes()`列表中是否至少有一种格式，以及`action`是否在模型的`supportedDropActions()`中。
如果你想测试`data`是否能在`row`、`column`、`parent`时丢弃，可以用`action`重新实现这个函数。如果你不需要这个测试，就没必要重写这个函数。

### `[override virtual] int QConcatenateTablesProxyModel::columnCount(const QModelIndex &parent = QModelIndex()) const`

**作用与语义：**

重实现自：`QAbstractItemModel::columnCount`（const QModelIndex & parent） const.
该方法返回列数最少的源模型的列数。
返回给定`parent`子节点的列数。
在大多数子类中，列的数量与 `parent` 无关。
注意：在实现基于表的模型时，当父模型有效时，columnCount() 应返回 0。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[override virtual] QVariant QConcatenateTablesProxyModel::data(const QModelIndex &index, int role = Qt::DisplayRole) const`

**作用与语义：**

重构：`QAbstractItemModel::data`（const QModelIndex & index， int role） const.
返回`index`所指项在指定`role`下存储的数据。
注意：如果你没有可返回的值，请返回一个无效（默认构造）的 `QVariant`。
注意：该函数可通过元对象系统和QML调用。参见 `Q_INVOKABLE`。

### `[override virtual] bool QConcatenateTablesProxyModel::dropMimeData(const QMimeData *data, Qt::DropAction action, int row, int column, const QModelIndex &parent)`

**作用与语义：**

重实现自：`QAbstractItemModel::dropMimeData`（const QMimeData *data， Qt：:D ropAction action， int row， int column， const QModelIndex &parent）.
`QConcatenateTablesProxyModel`处理在物品之间以及最后一个项目之后的投放。在所有情况下，调用都会转发到底层的源模型。当丢入某个项目时，调用该项目的源模型。在物品之间投放时，调用紧邻放置位置下方的源模型。当在最后一个项目之后投放时，调用最后一个源模型。
处理拖拽操作提供的`data`，拖拽操作以给定`action`结束。
如果数据和动作由模型处理，返回`true`;否则返回`false`。
指定的`row`、`column`和`parent`表示操作结束时某项在模型中的位置。模型有责任在正确的位置完成动作。
例如，`QTreeView`中对物品的投放动作可能导致新物品入为`row`、`column`和`parent`指定的物品的子项，或作为该物品的兄弟姐妹。
当`row`和`column`为-1时，意味着丢弃的数据应直接在`parent`上被丢弃。通常这意味着将数据作为`parent`的子项附加。如果`row`和`column`大于或等于零，则表示丢弃发生在指定`row`和`column`之前，`parent`中。
调用`mimeTypes()`成员以获取可接受的MIME类型列表。该默认实现假设`mimeTypes()`的默认实现，返回单一默认MIME类型。如果你在自定义模型中重新实现`mimeTypes()`以返回多个MIME类型，必须重新实现该函数以利用它们。

### `[override virtual] Qt::ItemFlags QConcatenateTablesProxyModel::flags(const QModelIndex &index) const`

**作用与语义：**

重实现自：`QAbstractItemModel::flags`（const QModelIndex & index） const.
返回给定索引的标志。如果`index`有效，则该`index`的标志来自源模型。如果`index`无效（例如用于判断是否允许在视图中的空区域切换），则返回第一个模型的标志。
返回给定`index`的物品标记。
基类实现返回一组标志，使该项启用（`ItemIsEnabled`）并允许被选中（`ItemIsSelectable`）。
注意：该函数可通过元对象系统和QML调用。参见 `Q_INVOKABLE`。

### `[override virtual] QVariant QConcatenateTablesProxyModel::headerData(int section, Qt::Orientation orientation, int role = Qt::DisplayRole) const`

**作用与语义：**

重实现自：`QAbstractItemModel::headerData`（int section，Qt：：Orientation Orientation， int role）const.
该方法返回第一个源模型的水平头部数据，以及对应每行的源模型的垂直头部数据。
返回给定`role`和`section`的首部数据，并带有指定`orientation`。
对于水平头部，节号对应于列号。同样，对于竖向头部，节号对应行号。
注意：该函数可通过元对象系统和QML调用。参见 `Q_INVOKABLE`。

### `[override virtual] QModelIndex QConcatenateTablesProxyModel::index(int row, int column, const QModelIndex &parent = QModelIndex()) const`

**作用与语义：**

重实现自：`QAbstractItemModel::index`（整数行，整数列，cont QModelIndex 和parent）const.
返回由给定`row`、`column`和`parent`索引指定模型中项目的索引。
在子类中重新实现该函数时，调用 `createIndex()` 生成模型索引，其他组件可以用来引用模型中的项。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[override virtual] QMap<int, QVariant> QConcatenateTablesProxyModel::itemData(const QModelIndex &proxyIndex) const`

**作用与语义：**

重实现自：`QAbstractItemModel::itemData`（const QModelIndex & index） const.
返回一个映射，包含模型中该项目在给定`index`处所有预定义角色的值。
如果你想将默认行为扩展到地图中包含自定义角色，可以重新实现这个函数。

### `[invokable] QModelIndex QConcatenateTablesProxyModel::mapFromSource(const QModelIndex &sourceIndex) const`

**作用与语义：**

返回给定`sourceIndex`的代理索引，该索引可以来自任意源模型。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[invokable] QModelIndex QConcatenateTablesProxyModel::mapToSource(const QModelIndex &proxyIndex) const`

**作用与语义：**

返回给定`proxyIndex`的源索引。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[override virtual] QMimeData *QConcatenateTablesProxyModel::mimeData(const QModelIndexList &indexes) const`

**作用与语义：**

重实现自：`QAbstractItemModel::mimeData`（const QModelIndexList & indexes） const.
调用会被转发到`indexes`列表中第一个索引的源模型。
重要提示：请注意，该代理只支持拖拽单行。如果调用来自多行索引，它会断言，因为该代理模型无法通用实现来自不同源模型的行。`QMimeData`中的每个数据都需要合并，这取决于数据类型。如果你想支持拖拽多行，可以在子类中重新实现此方法。
返回一个对象，包含对应指定列表的序列化数据项`indexes`。描述编码数据的格式来源于`mimeTypes()`函数。该默认实现使用`mimeTypes()`默认实现返回的默认MIME类型。如果您在自定义模型中重新实现`mimeTypes()`以返回更多MIME类型，请重新实现该函数以利用这些类型。
如果 Lists of `indexes` 是空的，或者没有支持 MIME 类型的 MIME，则返回 `nullptr` 而不是序列化的空列表。

### `[override virtual] QStringList QConcatenateTablesProxyModel::mimeTypes() const`

**作用与语义：**

重装：`QAbstractItemModel::mimeTypes()` const.
该方法返回第一个源模型的哑剧类型。
返回允许的MIME类型列表。默认情况下，内置模型和视图使用内部MIME类型：`application/x-qabstractitemmodeldatalist`。
在自定义模型中实现拖放支持时，如果你返回的数据格式不是默认的内部 MIME 类型，请重新实现这个函数，返回你的 MIME 类型列表。
如果你在自定义模型中重新实现该函数，也必须重新实现调用它的成员函数：`mimeData()` 和 `dropMimeData()`。

### `[override virtual] QModelIndex QConcatenateTablesProxyModel::parent(const QModelIndex &index) const`

**作用与语义：**

重实现自：`QAbstractItemModel::parent`（const QModelIndex & index） const.
返回模型项目的父项，并返回给定`index`。如果该项没有父项，则返回无效`QModelIndex`。
在暴露树状数据结构的模型中，一个常用的惯例是只有第一列的项有子节点。在这种情况下，在子类中重新实现该函数时，返回`QModelIndex`的列将为0。
在将该函数重新实现到子类中时，要注意避免调用`QModelIndex`成员函数，如`QModelIndex::parent()`，因为属于你模型的索引会直接调用你的实现，导致无限递归。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `void QConcatenateTablesProxyModel::removeSourceModel(QAbstractItemModel *sourceModel)`

**作用与语义：**

移除之前添加到该代理中的源模型`sourceModel`。
`sourceModel`的所有权不受此影响。

### `[override virtual, since 6.9.0] QHash<int, QByteArray> QConcatenateTablesProxyModel::roleNames() const`

**作用与语义：**

重装：`QAbstractItemModel::roleNames()` const.
返回底层模型 roleNames() 的并集。
如果源模型将不同名称关联到同一角色，最后源模型中使用的名称会覆盖早期模型中使用的名称。
返回模特的角色名。
Qt 默认设置的角色名称如下：
- `Qt Role`：QML角色名称
- `Qt::DisplayRole`：展示
- `Qt::DecorationRole`：装饰
- `Qt::EditRole`：编辑
- `Qt::ToolTipRole`：工具提示
- `Qt::StatusTipRole`：statusTip
- `Qt::WhatsThisRole`：这是什么

### `[override virtual] int QConcatenateTablesProxyModel::rowCount(const QModelIndex &parent = QModelIndex()) const`

**作用与语义：**

重实现自：`QAbstractItemModel::rowCount`（const QModelIndex & parent）const.
返回给定`parent`下的行数。当父节点有效时，表示 rowCount 返回的是父节点的子节点数。
注意：在实现基于表的模型时，当父模型有效时，rowCount() 应返回 0。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[override virtual] bool QConcatenateTablesProxyModel::setData(const QModelIndex &index, const QVariant &value, int role = Qt::EditRole)`

**作用与语义：**

重实现自：`QAbstractItemModel::setData`（const QModelIndex & index， const QVariant & value， int role）。
将`index`项的 `role` 数据设置为 `value`。
成功时返回`true`;成功时返回`false`。
如果数据成功设置，`dataChanged()`信号应会发出。
基类实现返回`false`。该函数和`data()`必须重新实现以适应可编辑模型。
注意：该函数可通过元对象系统和QML调用。参见 `Q_INVOKABLE`。

### `[override virtual] bool QConcatenateTablesProxyModel::setItemData(const QModelIndex &proxyIndex, const QMap<int, QVariant> &roles)`

**作用与语义：**

重实现自：`QAbstractItemModel::setItemData`（const QModelIndex & index， const QMap<int， QVariant> and roles）。
将`index`项的角色数据设置为每个`Qt::ItemDataRole`的对应值`roles`。
成功时返回`true`;否则返回`false`。
不在`roles`中的角色不会被修改。

### `QList<QAbstractItemModel *> QConcatenateTablesProxyModel::sourceModels() const`

**作用与语义：**

返回作为该代理模型源模型添加的模型列表。

### `[override virtual] QSize QConcatenateTablesProxyModel::span(const QModelIndex &index) const`

**作用与语义：**

重实现自：`QAbstractItemModel::span`（const QModelIndex & index） const.
返回由`index`表示的项的行和列跨。
注：目前不使用跨度。

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

`QConcatenateTablesProxyModel` 所属机制类型：模型/视图协议。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
