# QStringListModel

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QStringListModel` 是 模型/视图协议 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QStringListModel` 是模型/视图体系中的数据模型类型，向视图提供索引、角色数据和结构变化通知。

**内部模型：** 视图不应该直接操作底层容器；它通过 QModelIndex 和 data roles 查询模型。模型必须准确维护索引有效性以及插入、删除、移动时的通知顺序。

**适用场景：** 需要把自定义数据接入 QListView、QTableView、QTreeView 或代理模型时使用。

**典型调用链：** 准备数据源 -> 实现/配置模型 -> 连接 view -> 通过 data/flags/setData 读写 -> 发出 dataChanged 或 begin/end 结构通知。

**先记住的坑：** 不要在 data() 中修改数据；不要返回过期索引；不要用全量 reset 代替精确结构通知，除非确实无法描述变化。

## 2. 依赖与对象关系

- 头文件：`#include <QStringListModel>`
- 继承自：QAbstractListModel
- 直接派生类：QHelpIndexModel

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

- `QStringListModel(QObject *parent = nullptr)`
- `QStringListModel(const QStringList &strings, QObject *parent = nullptr)`
- `void setStringList(const QStringList &strings)`
- `QStringList stringList() const`

### 重实现的公有函数

- `(since 6.0) virtual bool clearItemData(const QModelIndex &index) override`
- `virtual QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const override`
- `virtual Qt::ItemFlags flags(const QModelIndex &index) const override`
- `virtual bool insertRows(int row, int count, const QModelIndex &parent = QModelIndex()) override`
- `virtual QMap<int, QVariant> itemData(const QModelIndex &index) const override`
- `virtual bool moveRows(const QModelIndex &sourceParent, int sourceRow, int count, const QModelIndex &destinationParent, int destinationChild) override`
- `virtual bool removeRows(int row, int count, const QModelIndex &parent = QModelIndex()) override`
- `virtual int rowCount(const QModelIndex &parent = QModelIndex()) const override`
- `virtual bool setData(const QModelIndex &index, const QVariant &value, int role = Qt::EditRole) override`
- `virtual bool setItemData(const QModelIndex &index, const QMap<int, QVariant> &roles) override`
- `virtual QModelIndex sibling(int row, int column, const QModelIndex &idx) const override`
- `virtual void sort(int column, Qt::SortOrder order = Qt::AscendingOrder) override`
- `virtual Qt::DropActions supportedDropActions() const override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[explicit] QStringListModel::QStringListModel(QObject *parent = nullptr)`

**作用与语义：**

使用给定的 `parent` 构建一个字符串列表模型。

### `[explicit] QStringListModel::QStringListModel(const QStringList &strings, QObject *parent = nullptr)`

**作用与语义：**

构建一个字符串列表模型，包含指定的 `strings`，并使用给定的 `parent`。

### `[override virtual, since 6.0] bool QStringListModel::clearItemData(const QModelIndex &index)`

**作用与语义：**

重实现自：`QAbstractItemModel::clearItemData`（const QModelIndex & index）。
移除给定`index`所有角色中存储的数据。成功返回`true`;否则返回`false`。如果数据被成功移除，应发出`dataChanged()`信号。基类实现返回`false`。

### `[override virtual] QVariant QStringListModel::data(const QModelIndex &index, int role = Qt::DisplayRole) const`

**作用与语义：**

重实现自：`QAbstractItemModel::data`（const QModelIndex & index， int role） const.
返回指定`role`的数据，来自给定`index`的项目。
如果视图请求无效索引，则返回一个无效变体。
返回`index`所指项在给定`role`下存储的数据。
注意：如果你没有要返回的值，请返回一个无效（默认构造的）`QVariant`。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[override virtual] Qt::ItemFlags QStringListModel::flags(const QModelIndex &index) const`

**作用与语义：**

重实现自：`QAbstractListModel::flags`（const QModelIndex & index） const.
返回该物品的标志，并`index`。
有效项目已启用、可选、编辑、拖拽和拖拽。

### `[override virtual] bool QStringListModel::insertRows(int row, int count, const QModelIndex &parent = QModelIndex())`

**作用与语义：**

重实现自：`QAbstractItemModel::insertRows`（整数行，整数计数，条件QModelIndex和parent）。
从给定`row`开始插入`count`行。
行的`parent`索引是可选的，仅用于与`QAbstractItemModel`的一致性。默认情况下，会指定空索引，表示这些行入到模型的顶层。
如果插入成功，返回`true`。
注意：该函数的基类实现不做任何操作，返回`false`。
支持此功能的模型中，`count`行在给定`row`之前插入模型。新行中的项目将是`parent`模型索引所表示项的子节点。
如果`row`为0，则这些行会加在父行中已有的行之前。
如果`row` `rowCount()`，则这些行会附加到父节点中已有的行上。
如果`parent`没有子节点，则插入一列`count`行。
如果行成功插入，返回`true`;否则返回`false`。
如果你实现了自己的模型，如果你想支持插入，可以重新实现这个函数。或者，你也可以提供自己的 API 来修改数据。无论哪种情况，你都需要调用 `beginInsertRows()` 和 `endInsertRows()` 通知其他组件模型已经变更。
注意：该函数可以通过元对象系统和QML调用。参见 `Q_INVOKABLE`。

### `[override virtual] QMap<int, QVariant> QStringListModel::itemData(const QModelIndex &index) const`

**作用与语义：**

重实现自：`QAbstractItemModel::itemData`（const QModelIndex & index） const.
返回一个映射，包含模型中该项目在给定`index`处所有预定义角色的值。
如果你想将默认行为扩展到地图中包含自定义角色，可以重新实现这个函数。

### `[override virtual] bool QStringListModel::moveRows(const QModelIndex &sourceParent, int sourceRow, int count, const QModelIndex &destinationParent, int destinationChild)`

**作用与语义：**

重实现自：`QAbstractItemModel::moveRows`（const QModelIndex & sourceParent， int sourceRow， int count， const QModelIndex &destinationParent， int destinationChild）。
在支持此操作的模型中，将从父`sourceParent`下的给定`sourceRow`开始，`count`行移动到父`destinationParent`下行`destinationChild`。
如果行成功移动，返回`true`;否则返回`false`。
基类实现什么都不做，只返回`false`。
如果你实现了自己的模型，如果你想支持移动，可以重新实现这个函数。或者，你也可以提供自己的 API 来修改数据。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[override virtual] bool QStringListModel::removeRows(int row, int count, const QModelIndex &parent = QModelIndex())`

**作用与语义：**

重实现自：`QAbstractItemModel::removeRows`（整数行，整数计数，条件QModelIndex和parent）。
从给定`row`开始，从模型中移除`count`行。
行的`parent`索引是可选的，仅用于与`QAbstractItemModel`的一致性。默认情况下，会指定空索引，表示模型顶层的行被移除。
如果移除行成功，退货`true`。
在支持此功能的模型中，会从模型中移除从父 `parent` 下以给定`row`开始的`count`行。
如果行被成功移除，返回`true`;否则返回`false`。
基类实现什么都不做，返回`false`。
如果你实现了自己的模型，如果你想支持删除，可以重新实现这个函数。或者，你也可以提供自己的 API 来修改数据。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[override virtual] int QStringListModel::rowCount(const QModelIndex &parent = QModelIndex()) const`

**作用与语义：**

重实现自：`QAbstractItemModel::rowCount`（const QModelIndex &parent）const.
返回模型中的行数。该值对应于模型内部字符串列表中的项数。
可选的`parent`参数在大多数用于指定要计数行父节点的模型中存在。由于如果指定了有效的父节点，则该列表是一个列表，结果总是0。
返回给定`parent`下的行数。当父节点有效时，表示 rowCount 返回的是父节点的子节点数。
注意：在实现基于表的模型时，当父模型有效时，rowCount() 应返回 0。
注意：该函数可通过元对象系统和QML调用。参见 `Q_INVOKABLE`。

### `[override virtual] bool QStringListModel::setData(const QModelIndex &index, const QVariant &value, int role = Qt::EditRole)`

**作用与语义：**

重实现自：`QAbstractItemModel::setData`（const QModelIndex & index， const QVariant & value， int role）。
将项目中指定`role`的数据，模型中给定的`index`，设置为提供的`value`。
如果物品发生变化，`dataChanged()`信号会被发射。发出`dataChanged()`信号后返回`true`。
将`index`项的 `role` 数据设置为 `value`。
成功时返回`true`;否则返回`false`。
如果数据成功设置，`dataChanged()`信号应会发出。
基类实现返回`false`。该函数和`data()`必须为可编辑模型重新实现。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[override virtual] bool QStringListModel::setItemData(const QModelIndex &index, const QMap<int, QVariant> &roles)`

**作用与语义：**

重实现自：`QAbstractItemModel::setItemData`（const QModelIndex & index， const QMap<int， QVariant> and roles）。
如果`roles`同时包含`Qt::DisplayRole`和`Qt::EditRole`，则后者优先。
将`index`项的角色数据设置为每个`Qt::ItemDataRole`的对应值`roles`。
成功时返回`true`;否则返回`false`。
未在`roles`中的角色不会被修改。

### `void QStringListModel::setStringList(const QStringList &strings)`

**作用与语义：**

将模型内部字符串列表设置为`strings`。模型会通知任何附加视图其底层数据发生变化。

### `[override virtual] QModelIndex QStringListModel::sibling(int row, int column, const QModelIndex &idx) const`

**作用与语义：**

重实现自：`QAbstractListModel::sibling`（int row， int column， const QModelIndex &idx） const.

### `[override virtual] void QStringListModel::sort(int column, Qt::SortOrder order = Qt::AscendingOrder)`

**作用与语义：**

重实现自：`QAbstractItemModel::sort`（整数列，Qt：：SortOrder）。
按给定`order`中的`column`排序模型。
基础类实现什么都不做。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `QStringList QStringListModel::stringList() const`

**作用与语义：**

返回模型用来存储数据的字符串列表。

### `[override virtual] Qt::DropActions QStringListModel::supportedDropActions() const`

**作用与语义：**

重实现自：`QAbstractItemModel::supportedDropActions()` const.
返回该模型支持的投放动作。
默认实现返回`Qt::CopyAction`。如果你希望支持额外操作，请重新实现这个函数。你还必须重新实现`dropMimeData()`函数以处理这些额外的操作。

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

`QStringListModel` 所属机制类型：模型/视图协议。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
