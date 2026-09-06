# QItemSelectionModel

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QItemSelectionModel` 是 模型/视图协议 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QItemSelectionModel` 是模型/视图体系中的数据模型类型，向视图提供索引、角色数据和结构变化通知。

**内部模型：** 视图不应该直接操作底层容器；它通过 QModelIndex 和 data roles 查询模型。模型必须准确维护索引有效性以及插入、删除、移动时的通知顺序。

**适用场景：** 需要把自定义数据接入 QListView、QTableView、QTreeView 或代理模型时使用。

**典型调用链：** 准备数据源 -> 实现/配置模型 -> 连接 view -> 通过 data/flags/setData 读写 -> 发出 dataChanged 或 begin/end 结构通知。

**先记住的坑：** 不要在 data() 中修改数据；不要返回过期索引；不要用全量 reset 代替精确结构通知，除非确实无法描述变化。

## 2. 依赖与对象关系

- 头文件：`#include <QItemSelectionModel>`
- 继承自：QObject
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

- `enum SelectionFlag { NoUpdate, Clear, Select, Deselect, Toggle, …, ClearAndSelect }`
- `flags SelectionFlags`

### 属性

- `selectedIndexes : QModelIndexList`

### 公有函数

- `QItemSelectionModel(QAbstractItemModel *model = nullptr)`
- `QItemSelectionModel(QAbstractItemModel *model, QObject *parent)`
- `virtual ~QItemSelectionModel()`
- `QBindable<QAbstractItemModel *> bindableModel()`
- `bool columnIntersectsSelection(int column, const QModelIndex &parent = QModelIndex()) const`
- `QModelIndex currentIndex() const`
- `bool hasSelection() const`
- `bool isColumnSelected(int column, const QModelIndex &parent = QModelIndex()) const`
- `bool isRowSelected(int row, const QModelIndex &parent = QModelIndex()) const`
- `bool isSelected(const QModelIndex &index) const`
- `QAbstractItemModel * model()`
- `const QAbstractItemModel * model() const`
- `bool rowIntersectsSelection(int row, const QModelIndex &parent = QModelIndex()) const`
- `QModelIndexList selectedColumns(int row = 0) const`
- `QModelIndexList selectedIndexes() const`
- `QModelIndexList selectedRows(int column = 0) const`
- `const QItemSelection selection() const`
- `void setModel(QAbstractItemModel *model)`

### 公有槽函数

- `virtual void clear()`
- `virtual void clearCurrentIndex()`
- `void clearSelection()`
- `virtual void reset()`
- `virtual void select(const QItemSelection &selection, QItemSelectionModel::SelectionFlags command)`
- `virtual void select(const QModelIndex &index, QItemSelectionModel::SelectionFlags command)`
- `virtual void setCurrentIndex(const QModelIndex &index, QItemSelectionModel::SelectionFlags command)`

### 信号

- `void currentChanged(const QModelIndex &current, const QModelIndex &previous)`
- `void currentColumnChanged(const QModelIndex &current, const QModelIndex &previous)`
- `void currentRowChanged(const QModelIndex &current, const QModelIndex &previous)`
- `void modelChanged(QAbstractItemModel *model)`
- `void selectionChanged(const QItemSelection &selected, const QItemSelection &deselected)`

### 保护函数

- `void emitSelectionChanged(const QItemSelection &newSelection, const QItemSelection &oldSelection)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QItemSelectionModel::SelectionFlagflags QItemSelectionModel::SelectionFlags`

**作用与语义：**

本枚举描述了选择模型将如何更新。
- `QItemSelectionModel::NoUpdate`：`0x0000`;不进行选拔。
- `QItemSelectionModel::Clear`：`0x0001`;全部选拔将被清除。
- `QItemSelectionModel::Select`：`0x0002`;所有指定的索引都会被选中。
- `QItemSelectionModel::Deselect`：`0x0004`;所有指定的索引将被取消选择。
- `QItemSelectionModel::Toggle`：`0x0008`;所有指定的索引将根据其当前状态被选择或取消。
- `QItemSelectionModel::Current`：`0x0010`;当前选队将进行更新。
- `QItemSelectionModel::Rows`：`0x0020`;所有索引都将展开为跨行。
- `QItemSelectionModel::Columns`：`0x0040`;所有索引将扩展为跨列。
- `QItemSelectionModel::SelectCurrent`：`Select | Current`;为方便而提供选择和当前的组合。
- `QItemSelectionModel::ToggleCurrent`：`Toggle | Current`;结合了切换和电流，便于使用。
- `QItemSelectionModel::ClearAndSelect`：`Clear | Select`;为方便而提供，Clear和Select的组合。
SelectionFlags 类型是 QFlags 的 typedef<SelectionFlag>。它存储 SelectionFlag 值的 OR 组合。

### `[read-only] selectedIndexes : QModelIndexList`

**作用与语义：**

返回所有选中的模型项目索引列表。列表中无重复，且不排序。
注意：用于属性 selectIndex 的 Getter 函数。

**如何使用：** 调用 `selectedIndexes()` 读取当前值；它不会修改应用状态。

### `[explicit] QItemSelectionModel::QItemSelectionModel(QAbstractItemModel *model = nullptr)`

**作用与语义：**

构建一个针对指定题目`model`的选择模型。

### `[explicit] QItemSelectionModel::QItemSelectionModel(QAbstractItemModel *model, QObject *parent)`

**作用与语义：**

构建一个选择模型，对指定项目`model` `parent`操作。

### `[virtual noexcept] QItemSelectionModel::~QItemSelectionModel()`

**作用与语义：**

这破坏了选择模型。

### `[virtual slot] void QItemSelectionModel::clear()`

**作用与语义：**

清除选择模型。释放`selectionChanged()`和`currentChanged()`。

### `[virtual slot] void QItemSelectionModel::clearCurrentIndex()`

**作用与语义：**

清除当前索引。发出 `currentChanged()`。

### `[slot] void QItemSelectionModel::clearSelection()`

**作用与语义：**

清除选择模型中的选择。发出`selectionChanged()`。

### `[invokable] bool QItemSelectionModel::columnIntersectsSelection(int column, const QModelIndex &parent = QModelIndex()) const`

**作用与语义：**

退货`true`是否在`column`中选中了指定`parent`的物品。
注意：自第5.15卷起，`parent`的默认参数是空模型索引。
注意：该函数可通过元对象系统和QML调用。参见 `Q_INVOKABLE`。

### `[signal] void QItemSelectionModel::currentChanged(const QModelIndex &current, const QModelIndex &previous)`

**作用与语义：**

每当当前项目发生变化时，该信号都会发出。`previous`模型项目索引被`current`索引取代，作为当前项目。
注意，当项目模型重置时，该信号不会发出。

### `[signal] void QItemSelectionModel::currentColumnChanged(const QModelIndex &current, const QModelIndex &previous)`

**作用与语义：**

当`current`项发生变化且其列与当前`previous`项的列不同时，会发出该信号。
注意，当项目模型重置时，该信号不会发出。

### `QModelIndex QItemSelectionModel::currentIndex() const`

**作用与语义：**

返回当前项目的模型项索引，若无当前项则返回无效索引。

### `[signal] void QItemSelectionModel::currentRowChanged(const QModelIndex &current, const QModelIndex &previous)`

**作用与语义：**

当`current`项发生变化且其行与当前`previous`项的行不同时，该信号就会发出。
注意，当项目模型重置时，该信号不会发出。

### `[protected] void QItemSelectionModel::emitSelectionChanged(const QItemSelection &newSelection, const QItemSelection &oldSelection)`

**作用与语义：**

比较两个选择`newSelection`和 `oldSelection`，并与取消选中和被选中的项目`selectionChanged()`。

### `bool QItemSelectionModel::hasSelection() const`

**作用与语义：**

如果选择模型包含任何选中的项目，返回`true`，否则返回`false`。

### `[invokable] bool QItemSelectionModel::isColumnSelected(int column, const QModelIndex &parent = QModelIndex()) const`

**作用与语义：**

如果所有物品都被选中，`column`中所有物品并`parent`，退货`true`。
注意，这个函数通常比调用同一列所有项的 `isSelected()` 更快，且不可选择的项会被忽略。
注意：自Qt 5.15起，`parent`的默认参数是空模型索引。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[invokable] bool QItemSelectionModel::isRowSelected(int row, const QModelIndex &parent = QModelIndex()) const`

**作用与语义：**

如果所有物品都被选中并`parent` `row`，退货`true`。
注意，这个函数通常比对同一行中的所有项调用`isSelected()`更快，且不可选择项会被忽略。
注意：自第5.15量子起，`parent`的默认参数是空模型索引。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[invokable] bool QItemSelectionModel::isSelected(const QModelIndex &index) const`

**作用与语义：**

如果选择给定的模型项目`index`，返回`true`。
注意：该函数可通过元对象系统和QML调用。参见 `Q_INVOKABLE`。

### `QAbstractItemModel *QItemSelectionModel::model()`

**作用与语义：**

返回由选择模型操作的项目模型。

### `const QAbstractItemModel *QItemSelectionModel::model() const`

**作用与语义：**

返回由选择模型操作的项目模型。

### `[signal] void QItemSelectionModel::modelChanged(QAbstractItemModel *model)`

**作用与语义：**

当`model`成功设置`setModel()`时，该信号会发出。

### `[virtual slot] void QItemSelectionModel::reset()`

**作用与语义：**

清除选择模型。不发出任何信号。

### `[invokable] bool QItemSelectionModel::rowIntersectsSelection(int row, const QModelIndex &parent = QModelIndex()) const`

**作用与语义：**

如果在`row`中选中了与给定`parent`的物品，返回时`true`。
注意：自第5.15Q以来，`parent`的默认参数是空模型索引。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[virtual slot] void QItemSelectionModel::select(const QItemSelection &selection, QItemSelectionModel::SelectionFlags command)`

**作用与语义：**

使用指定`command`选择`selection`物品，并发射`selectionChanged()`。
注意：该槽位已超载。连接该槽位：


使用 qOverload 连接：
connect（sender， &SenderClass：：signal，。
itemSelectionModel， qOverload（&QItemSelectionModel：：select））;

或者用lambda作为包装器：
connect（sender， &SenderClass：：signal，。
itemSelectionModel， [receiver = itemSelectionModel]（const QItemSelection &selection， QItemSelectionModel：：SelectionFlags command） { receiver->select（selection， command）; }）;


更多示例和方法，请参见连接超载槽位。

### `[virtual slot] void QItemSelectionModel::select(const QModelIndex &index, QItemSelectionModel::SelectionFlags command)`

**作用与语义：**

使用指定`command`选择模型项`index`，并发射`selectionChanged()`。
注意：该槽位已超载。连接该槽位：


使用 qOverload 连接：
connect（sender， &SenderClass：：signal，。
itemSelectionModel， qOverload（&QItemSelectionModel：：select））;

或者用lambda作为包装器：
connect（sender， &SenderClass：：signal，。
itemSelectionModel， [receiver = itemSelectionModel]（const QModelIndex &index， QItemSelectionModel：：SelectionFlags command） { receiver->select（index， command）; }）;


更多示例和方法，请参见连接超载槽位。

### `[invokable] QModelIndexList QItemSelectionModel::selectedColumns(int row = 0) const`

**作用与语义：**

返回给定`row`中所有行都被选中的列索引。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `QModelIndexList QItemSelectionModel::selectedIndexes() const`

**作用与语义：**

返回所有选中的模型项目索引列表。列表中无重复，且不排序。
注意：用于属性 selectIndex 的 Getter 函数。

### `[invokable] QModelIndexList QItemSelectionModel::selectedRows(int column = 0) const`

**作用与语义：**

返回给定`column`中所有列被选中的行索引。
注意：该函数可通过元对象系统和QML调用。参见 `Q_INVOKABLE`。

### `const QItemSelection QItemSelectionModel::selection() const`

**作用与语义：**

返回存储在选择模型中的选择范围。

### `[signal] void QItemSelectionModel::selectionChanged(const QItemSelection &selected, const QItemSelection &deselected)`

**作用与语义：**

每当选择发生变化时，该信号都会发出。选择的变化表示为`deselected`项的选择和`selected`项的选题。
注意当前索引的变化与选择无关。还要注意，当项目模型重置时，该信号不会发出。
保持被选中但索引变化的项目不包含在`selected`和`deselected`中。因此，如果所选项目的索引发生变化，该信号可能同时`selected`和`deselected`均为空。
注意：不允许在直接连接到该信号的槽内修改模型（例如调用setData()）。该信号可能在模型被修改过程中发出，例如在移除行或列时，或模型重置时。在此类时刻尝试进行额外更改可能导致行为不明确。特别是，嵌套修改可能会破坏内部状态，例如`QSortFilterProxyModel`维护的映射结构。
注意：属性`selectedIndexes`的通知信号。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `selectedIndexes` 的变化，不要把它当作普通函数主动调用。

### `[virtual slot] void QItemSelectionModel::setCurrentIndex(const QModelIndex &index, QItemSelectionModel::SelectionFlags command)`

**作用与语义：**

将模型物品`index`为当前物品，并发射`currentChanged()`。当前物品用于键盘导航和焦点指示;它独立于任何选择的物品，尽管所选物品也可以是当前物品。
根据指定的`command`，`index`也可以成为当前选择的一部分。

### `void QItemSelectionModel::setModel(QAbstractItemModel *model)`

**作用与语义：**

将模型设置为`model`。`modelChanged()`信号将被发射。

### `enum SelectionFlag { NoUpdate, Clear, Select, Deselect, Toggle, …, ClearAndSelect }`

**作用与语义：**

本枚举描述了选择模型将如何更新。
- `QItemSelectionModel::NoUpdate`：`0x0000`;不进行选拔。
- `QItemSelectionModel::Clear`：`0x0001`;全部选拔将被清除。
- `QItemSelectionModel::Select`：`0x0002`;所有指定的索引都会被选中。
- `QItemSelectionModel::Deselect`：`0x0004`;所有指定的索引将被取消选择。
- `QItemSelectionModel::Toggle`：`0x0008`;所有指定的索引将根据其当前状态被选择或取消。
- `QItemSelectionModel::Current`：`0x0010`;当前选队将进行更新。
- `QItemSelectionModel::Rows`：`0x0020`;所有索引都将展开为跨行。
- `QItemSelectionModel::Columns`：`0x0040`;所有索引将扩展为跨列。
- `QItemSelectionModel::SelectCurrent`：`Select | Current`;为方便而提供选择和当前的组合。
- `QItemSelectionModel::ToggleCurrent`：`Toggle | Current`;结合了切换和电流，便于使用。
- `QItemSelectionModel::ClearAndSelect`：`Clear | Select`;为方便而提供，Clear和Select的组合。
SelectionFlags 类型是 QFlags 的 typedef<SelectionFlag>。它存储 SelectionFlag 值的 OR 组合。

### `flags SelectionFlags`

**作用与语义：**

本枚举描述了选择模型将如何更新。
- `QItemSelectionModel::NoUpdate`：`0x0000`;不进行选拔。
- `QItemSelectionModel::Clear`：`0x0001`;全部选拔将被清除。
- `QItemSelectionModel::Select`：`0x0002`;所有指定的索引都会被选中。
- `QItemSelectionModel::Deselect`：`0x0004`;所有指定的索引将被取消选择。
- `QItemSelectionModel::Toggle`：`0x0008`;所有指定的索引将根据其当前状态被选择或取消。
- `QItemSelectionModel::Current`：`0x0010`;当前选队将进行更新。
- `QItemSelectionModel::Rows`：`0x0020`;所有索引都将展开为跨行。
- `QItemSelectionModel::Columns`：`0x0040`;所有索引将扩展为跨列。
- `QItemSelectionModel::SelectCurrent`：`Select | Current`;为方便而提供选择和当前的组合。
- `QItemSelectionModel::ToggleCurrent`：`Toggle | Current`;结合了切换和电流，便于使用。
- `QItemSelectionModel::ClearAndSelect`：`Clear | Select`;为方便而提供，Clear和Select的组合。
SelectionFlags 类型是 QFlags 的 typedef<SelectionFlag>。它存储 SelectionFlag 值的 OR 组合。

### `QBindable<QAbstractItemModel *> bindableModel()`

**作用与语义：**

返回 `model` 属性的 `QBindable<QAbstractItemModel *>` 包装，供 Qt 属性绑定系统跟踪选择模型所关联的数据模型。只想取得当前模型时调用 `model()`；只有需要建立或检查属性绑定时才使用该接口。

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

`QItemSelectionModel` 所属机制类型：模型/视图协议。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
