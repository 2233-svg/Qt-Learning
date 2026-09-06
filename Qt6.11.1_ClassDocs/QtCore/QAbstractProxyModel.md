# QAbstractProxyModel

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QAbstractProxyModel` 是 模型/视图协议 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QAbstractProxyModel` 是 Qt Core 中的抽象协议类型，通常通过具体子类、模型、插件或工厂来使用。

**内部模型：** 抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

**适用场景：** 当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。

**典型调用链：** 选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。

**先记住的坑：** 不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

## 2. 依赖与对象关系

- 头文件：`#include <QAbstractProxyModel>`
- 继承自：QAbstractItemModel
- 直接派生类：QIdentityProxyModel、QSortFilterProxyModel,、QTransposeProxyModel

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

### 状态、生命周期和线程

**生命周期：** 模型应比视图活得足够久，视图销毁时不会自动替业务容器释放资源。模型变化必须使用对应的 begin/end 协议或精确通知，不能只改容器后期待视图自行发现。取到的 QModelIndex 只在模型允许的生命周期内有效。

**状态与结果：** 区分当前索引、选择模型、编辑状态、数据角色和模型结构变化。`dataChanged` 表示已有项目的数据变化，行列插入/删除表示结构变化，`modelReset` 会让旧索引整体失效。

**线程与事件循环：** 模型通常在 GUI 线程被视图访问。后台线程不要直接修改正在显示的模型；应在正确线程汇总数据，再通过通知协议更新，或使用线程安全的数据交换层。

## 3. 直接使用

当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。 使用时通常按这个过程组织：选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。

```cpp
// 视图通过 QModelIndex 和 role 查询模型。
const QVariant value = model->data(index, Qt::DisplayRole);
// 数据变化时由模型发出 dataChanged 或 begin/end 结构通知。
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 属性

- `sourceModel : QAbstractItemModel*`

### 公有函数

- `QAbstractProxyModel(QObject *parent = nullptr)`
- `virtual ~QAbstractProxyModel()`
- `QBindable<QAbstractItemModel *> bindableSourceModel()`
- `virtual QModelIndex mapFromSource(const QModelIndex &sourceIndex) const = 0`
- `virtual QItemSelection mapSelectionFromSource(const QItemSelection &sourceSelection) const`
- `virtual QItemSelection mapSelectionToSource(const QItemSelection &proxySelection) const`
- `virtual QModelIndex mapToSource(const QModelIndex &proxyIndex) const = 0`
- `virtual void setSourceModel(QAbstractItemModel *sourceModel)`
- `QAbstractItemModel * sourceModel() const`

### 重实现的公有函数

- `virtual QModelIndex buddy(const QModelIndex &index) const override`
- `virtual bool canDropMimeData(const QMimeData *data, Qt::DropAction action, int row, int column, const QModelIndex &parent) const override`
- `virtual bool canFetchMore(const QModelIndex &parent) const override`
- `(since 6.0) virtual bool clearItemData(const QModelIndex &index) override`
- `virtual QVariant data(const QModelIndex &proxyIndex, int role = Qt::DisplayRole) const override`
- `virtual bool dropMimeData(const QMimeData *data, Qt::DropAction action, int row, int column, const QModelIndex &parent) override`
- `virtual void fetchMore(const QModelIndex &parent) override`
- `virtual Qt::ItemFlags flags(const QModelIndex &index) const override`
- `virtual bool hasChildren(const QModelIndex &parent = QModelIndex()) const override`
- `virtual QVariant headerData(int section, Qt::Orientation orientation, int role = Qt::DisplayRole) const override`
- `virtual QMap<int, QVariant> itemData(const QModelIndex &proxyIndex) const override`
- `virtual QMimeData * mimeData(const QModelIndexList &indexes) const override`
- `virtual QStringList mimeTypes() const override`
- `virtual void revert() override`
- `virtual QHash<int, QByteArray> roleNames() const override`
- `virtual bool setData(const QModelIndex &index, const QVariant &value, int role = Qt::EditRole) override`
- `virtual bool setHeaderData(int section, Qt::Orientation orientation, const QVariant &value, int role = Qt::EditRole) override`
- `virtual bool setItemData(const QModelIndex &index, const QMap<int, QVariant> &roles) override`
- `virtual QModelIndex sibling(int row, int column, const QModelIndex &idx) const override`
- `virtual void sort(int column, Qt::SortOrder order = Qt::AscendingOrder) override`
- `virtual QSize span(const QModelIndex &index) const override`
- `virtual bool submit() override`
- `virtual Qt::DropActions supportedDragActions() const override`
- `virtual Qt::DropActions supportedDropActions() const override`

### 信号

- `void sourceModelChanged()`

### 保护函数

- `(since 6.2) QModelIndex createSourceIndex(int row, int col, void *internalPtr) const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[bindable] sourceModel : QAbstractItemModel*`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性表示该代理模型的源模型。
注意：这是一个私有信号。它可以用于信号连接，但用户不能发射。

**如何使用：** 调用 `sourceModel()` 读取当前值；它不会修改应用状态。

### `[explicit] QAbstractProxyModel::QAbstractProxyModel(QObject *parent = nullptr)`

**作用与语义：**

构造一个带有给定`parent`的代理模型。

### `[virtual noexcept] QAbstractProxyModel::~QAbstractProxyModel()`

**作用与语义：**

这会摧毁代理模型。

### `[override virtual] QModelIndex QAbstractProxyModel::buddy(const QModelIndex &index) const`

**作用与语义：**

重实现自：`QAbstractItemModel::buddy`（const QModelIndex & index） const.
返回由`index`表示的项目伙伴的模型索引。当用户想编辑某个项目时，视图会调用该函数检查是否应该编辑模型中的其他项目。然后，视图会利用伙伴项目返回的模型索引构建代理。
该功能的默认实现中，每个物品都是独立的伙伴。

### `[override virtual] bool QAbstractProxyModel::canDropMimeData(const QMimeData *data, Qt::DropAction action, int row, int column, const QModelIndex &parent) const`

**作用与语义：**

Reimplements： `QAbstractItemModel::canDropMimeData`（const QMimeData *data， Qt：:D ropAction action， int row， int column， const QModelIndex &parent） const.
返回`true`模型是否能接受`data`的删除。该默认实现仅检查`data` `mimeTypes()`列表中是否至少有一种格式，以及`action`是否在模型的`supportedDropActions()`中。
如果你想测试`data`是否能在`row`、`column`、`parent`时丢弃，可以用`action`重新实现这个函数。如果你不需要这个测试，就没必要重写这个函数。

### `[override virtual] bool QAbstractProxyModel::canFetchMore(const QModelIndex &parent) const`

**作用与语义：**

重实现自：`QAbstractItemModel::canFetchMore`（const QModelIndex &parent）const.
如果有更多数据可供 `parent`，返回`true`;否则返回 `false`。
默认实现总是返回`false`。
如果 canFetchMore() 返回 `true`，则应调用 `fetchMore()` 函数。这就是 `QAbstractItemView` 的行为，例如。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[override virtual, since 6.0] bool QAbstractProxyModel::clearItemData(const QModelIndex &index)`

**作用与语义：**

重实现自：`QAbstractItemModel::clearItemData`（const QModelIndex & index）。
移除给定`index`所有角色中存储的数据。成功返回`true`;否则返回`false`。如果数据被成功移除，应发出`dataChanged()`信号。基类实现返回`false`。

### `[protected, since 6.2] QModelIndex QAbstractProxyModel::createSourceIndex(int row, int col, void *internalPtr) const`

**作用与语义：**

相当于调用源模型上的 createIndex。
如果你的代理模型希望维护源模型中项目的父子关系，这种方法非常有用。在重新实现`mapToSource()`时，你可以调用该方法为源模型的行`row`和列`col`创建索引。
典型的用途是在重新实现`mapFromSource()`时保存来自源模型的内部指针并在重新实现`mapToSource()`时用与`internalPtr`相同的内部指针恢复原始源索引。

### `[override virtual] QVariant QAbstractProxyModel::data(const QModelIndex &proxyIndex, int role = Qt::DisplayRole) const`

**作用与语义：**

重构：`QAbstractItemModel::data`（const QModelIndex & index， int role） const.
返回`index`所指项在指定`role`下存储的数据。
注意：如果你没有可返回的值，请返回一个无效（默认构造）的 `QVariant`。
注意：该函数可通过元对象系统和QML调用。参见 `Q_INVOKABLE`。

### `[override virtual] bool QAbstractProxyModel::dropMimeData(const QMimeData *data, Qt::DropAction action, int row, int column, const QModelIndex &parent)`

**作用与语义：**

Reimplementation s： `QAbstractItemModel::dropMimeData`（const QMimeData *data， Qt：:D ropAction action， int row， int column， const QModelIndex &parent）.
处理拖放操作提供的`data`，拖拽操作以给定`action`结束。
如果数据和动作由模型处理，返回`true`;否则返回`false`。
指定的`row`、`column`和`parent`表示操作结束时该项在模型中的位置。模型有责任在正确的位置完成动作。
例如，`QTreeView`中物品的投放动作可能导致新物品入，要么作为`row`、`column`和`parent`指定的物品的子项，要么作为该物品的兄弟姐妹。
当`row`和`column`为-1时，意味着丢弃的数据应被视为直接丢弃`parent`。通常这意味着将数据作为`parent`的子项附加。如果`row`和`column`大于或等于零，则表示丢弃发生在指定`parent`中指定的`row`和`column`之前。
调用`mimeTypes()`成员以获取可接受的MIME类型列表。该默认实现假设`mimeTypes()`的默认实现，返回单一默认MIME类型。如果你在自定义模型中重新实现`mimeTypes()`以返回多个MIME类型，必须重新实现该函数以利用它们。

### `[override virtual] void QAbstractProxyModel::fetchMore(const QModelIndex &parent)`

**作用与语义：**

重实现自：`QAbstractItemModel::fetchMore`（const QModelIndex & parent）。
获取由`parent`索引指定的父项目的任何可用数据。
如果你是逐步填充模型，请重新实现。
默认实现什么都不做。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[override virtual] Qt::ItemFlags QAbstractProxyModel::flags(const QModelIndex &index) const`

**作用与语义：**

重实现自：`QAbstractItemModel::flags`（const QModelIndex & index） const.
返回给定`index`的物品标志。
基类实现返回一组标志组合，使该项（`ItemIsEnabled`）启用并允许选择（`ItemIsSelectable`）。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[override virtual] bool QAbstractProxyModel::hasChildren(const QModelIndex &parent = QModelIndex()) const`

**作用与语义：**

重实现自：`QAbstractItemModel::hasChildren`（const QModelIndex &parent） const.
如果`parent`有子女，返回`true`;否则返回`false`。
用`rowCount()`检测父母的子女数量。
注意，如果同一索引的标志被设置`Qt::ItemNeverHasChildren`，报告某个特定索引 hasChildren 是未定义行为。
注意：该函数可以通过元对象系统和QML调用。参见 `Q_INVOKABLE`。

### `[override virtual] QVariant QAbstractProxyModel::headerData(int section, Qt::Orientation orientation, int role = Qt::DisplayRole) const`

**作用与语义：**

重实现自：`QAbstractItemModel::headerData`（整数节，Qt：：Orientation orientation， int role）const.
返回给定`role`和`section`的头部数据，并带有指定`orientation`。
对于水平头部，节号对应于列号。同样，对于竖向头部，节号对应行号。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[override virtual] QMap<int, QVariant> QAbstractProxyModel::itemData(const QModelIndex &proxyIndex) const`

**作用与语义：**

重实现自：`QAbstractItemModel::itemData`（const QModelIndex & index） const.
返回一个映射，包含模型中该项目在给定`index`处所有预定义角色的值。
如果你想将默认行为扩展到地图中包含自定义角色，可以重新实现这个函数。

### `[pure virtual invokable] QModelIndex QAbstractProxyModel::mapFromSource(const QModelIndex &sourceIndex) const`

**作用与语义：**

重新实现该函数，返回代理模型中对应源模型`sourceIndex`的模型索引。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[virtual invokable] QItemSelection QAbstractProxyModel::mapSelectionFromSource(const QItemSelection &sourceSelection) const`

**作用与语义：**

返回从指定`sourceSelection`映射的代理选择。
重新实现此方法，将源选择映射到代理选择。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[virtual invokable] QItemSelection QAbstractProxyModel::mapSelectionToSource(const QItemSelection &proxySelection) const`

**作用与语义：**

返回从指定`proxySelection`映射的源选择。
重新实现该方法，将代理选择映射到源选择。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[pure virtual invokable] QModelIndex QAbstractProxyModel::mapToSource(const QModelIndex &proxyIndex) const`

**作用与语义：**

重新实现该函数，返回源模型中对应代理模型`proxyIndex`的模型索引。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[override virtual] QMimeData *QAbstractProxyModel::mimeData(const QModelIndexList &indexes) const`

**作用与语义：**

重实现自：`QAbstractItemModel::mimeData`（const QModelIndexList & indexes） const.
返回一个对象，包含对应指定`indexes`列表的序列化数据项。描述编码数据的格式来源于`mimeTypes()`函数。该默认实现使用`mimeTypes()`默认实现返回的默认MIME类型。如果你在自定义模型中重新实现`mimeTypes()`以返回更多MIME类型，请重新实现该函数以利用这些类型。
如果`indexes`列表为空，或没有支持的MIME类型，则返回`nullptr`而非序列化的空列表。

### `[override virtual] QStringList QAbstractProxyModel::mimeTypes() const`

**作用与语义：**

重实现自：`QAbstractItemModel::mimeTypes()` const.
返回允许的 MIME 类型列表。默认情况下，内置模型和视图使用内部 MIME 类型：`application/x-qabstractitemmodeldatalist`。
在自定义模型中实现拖放支持时，如果你返回的数据格式不是默认的内部 MIME 类型，请重新实现这个函数，返回你的 MIME 类型列表。
如果你在自定义模型中重新实现该函数，也必须重新实现调用它的成员函数：`mimeData()` 和 `dropMimeData()`。

### `[override virtual] void QAbstractProxyModel::revert()`

**作用与语义：**

重装：`QAbstractItemModel::revert()`。
让模型知道应丢弃缓存信息。该函数通常用于行编辑。

### `[override virtual] QHash<int, QByteArray> QAbstractProxyModel::roleNames() const`

**作用与语义：**

重装：`QAbstractItemModel::roleNames()` const.
返回模特的角色名。
Qt 默认设置的角色名称如下：
- `Qt Role`：QML角色名称
- `Qt::DisplayRole`：展示
- `Qt::DecorationRole`：装饰
- `Qt::EditRole`：编辑
- `Qt::ToolTipRole`：工具提示
- `Qt::StatusTipRole`：statusTip
- `Qt::WhatsThisRole`：这是什么

### `[override virtual] bool QAbstractProxyModel::setData(const QModelIndex &index, const QVariant &value, int role = Qt::EditRole)`

**作用与语义：**

重实现自：`QAbstractItemModel::setData`（const QModelIndex & index， const QVariant & value， int role）。
将`index`项的 `role` 数据设置为 `value`。
成功时返回`true`;成功时返回`false`。
如果数据成功设置，`dataChanged()`信号应会发出。
基类实现返回`false`。该函数和`data()`必须重新实现以适应可编辑模型。
注意：该函数可通过元对象系统和QML调用。参见 `Q_INVOKABLE`。

### `[override virtual] bool QAbstractProxyModel::setHeaderData(int section, Qt::Orientation orientation, const QVariant &value, int role = Qt::EditRole)`

**作用与语义：**

重实现自：`QAbstractItemModel::setHeaderData`（整数部分，Qt：：Orientation orientation，const QVariant &value，int role）。
在头部设置给定`role`和`section`数据，并指定`orientation`到所提供`value`。
如果头部数据更新，返回`true`;否则返回`false`。
在重新实现该功能时，必须显式地发出`headerDataChanged()`信号。

### `[override virtual] bool QAbstractProxyModel::setItemData(const QModelIndex &index, const QMap<int, QVariant> &roles)`

**作用与语义：**

重实现自：`QAbstractItemModel::setItemData`（const QModelIndex & index， const QMap<int， QVariant> and roles）。
将`index`项的角色数据设置为每个`Qt::ItemDataRole`的对应值`roles`。
成功时返回`true`;否则返回`false`。
不在`roles`中的角色不会被修改。

### `[virtual] void QAbstractProxyModel::setSourceModel(QAbstractItemModel *sourceModel)`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性表示该代理模型的源模型。
注意：这是一个私有信号。它可以用于信号连接，但用户不能发射。

**如何使用：** 调用 `setSourceModel(...)` 修改 `sourceModel`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `[override virtual] QModelIndex QAbstractProxyModel::sibling(int row, int column, const QModelIndex &idx) const`

**作用与语义：**

重构：`QAbstractItemModel::sibling`（整数行，整数列，const QModelIndex & index）const.
`row`时退回兄弟姐妹，`index` `column`物品，或者如果该地点没有兄弟姐妹，则`QModelIndex`无效。
sibling() 只是一个方便函数，它会找到该项的父项，并用它检索指定`row`和`column`中子项的索引。
该方法可选择性地覆盖以实现特定优化。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[override virtual] void QAbstractProxyModel::sort(int column, Qt::SortOrder order = Qt::AscendingOrder)`

**作用与语义：**

重实现自：`QAbstractItemModel::sort`（整数列，Qt：：SortOrder）。
按给定`order`中的`column`排序模型。
基础类实现什么都不做。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `QAbstractItemModel *QAbstractProxyModel::sourceModel() const`

**作用与语义：**

返回包含代理模型可用数据的模型。
注意：属性sourceModel的获取函数。

### `[override virtual] QSize QAbstractProxyModel::span(const QModelIndex &index) const`

**作用与语义：**

重实现自：`QAbstractItemModel::span`（const QModelIndex & index） const.
返回由`index`表示的项的行和列跨。
注：目前不使用跨度。

### `[override virtual] bool QAbstractProxyModel::submit()`

**作用与语义：**

重装：`QAbstractItemModel::submit()`。
让模型知道应将缓存信息提交到永久存储。该功能通常用于行编辑。
如果没有错误，返回`true`;否则返回`false`。

### `[override virtual] Qt::DropActions QAbstractProxyModel::supportedDragActions() const`

**作用与语义：**

重装：`QAbstractItemModel::supportedDragActions()` const.
返回该模型中数据支持的动作。
默认实现返回`supportedDropActions()`。如果你希望支持更多操作，可以重新实现这个函数。
当发生拖拽时，`QAbstractItemView::startDrag()` 默认使用支持的DragActions()。

### `[override virtual] Qt::DropActions QAbstractProxyModel::supportedDropActions() const`

**作用与语义：**

重实现自：`QAbstractItemModel::supportedDropActions()` const.
返回该模型支持的投放动作。
默认实现返回`Qt::CopyAction`。如果你希望支持额外操作，请重新实现这个函数。你还必须重新实现`dropMimeData()`函数以处理这些额外的操作。

### `QBindable<QAbstractItemModel *> bindableSourceModel()`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性表示该代理模型的源模型。
注意：这是一个私有信号。它可以用于信号连接，但用户不能发射。

**如何使用：** 调用 `bindableSourceModel()` 取得 `sourceModel` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `void sourceModelChanged()`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性表示该代理模型的源模型。
注意：这是一个私有信号。它可以用于信号连接，但用户不能发射。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `sourceModel` 的变化，不要把它当作普通函数主动调用。

## 6. 深入实践与常见坑

### 生命周期和资源边界

模型应比视图活得足够久，视图销毁时不会自动替业务容器释放资源。模型变化必须使用对应的 begin/end 协议或精确通知，不能只改容器后期待视图自行发现。取到的 QModelIndex 只在模型允许的生命周期内有效。

### 状态和错误边界

区分当前索引、选择模型、编辑状态、数据角色和模型结构变化。`dataChanged` 表示已有项目的数据变化，行列插入/删除表示结构变化，`modelReset` 会让旧索引整体失效。

### 线程边界

模型通常在 GUI 线程被视图访问。后台线程不要直接修改正在显示的模型；应在正确线程汇总数据，再通过通知协议更新，或使用线程安全的数据交换层。

### 最容易出现的错误

不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QAbstractProxyModel` 所属机制类型：模型/视图协议。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
