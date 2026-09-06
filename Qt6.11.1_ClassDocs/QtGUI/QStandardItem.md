# QStandardItem

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QStandardItem` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QStandardItem>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

### 状态、生命周期和线程

**生命周期：** 先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

**状态与结果：** 把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

**线程与事件循环：** 如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

## 3. 直接使用

围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum ItemType { Type, UserType }`

### 公有函数

- `QStandardItem()`
- `QStandardItem(const QString &text)`
- `QStandardItem(const QIcon &icon, const QString &text)`
- `QStandardItem(int rows, int columns = 1)`
- `virtual ~QStandardItem()`
- `QString accessibleDescription() const`
- `QString accessibleText() const`
- `void appendColumn(const QList<QStandardItem *> &items)`
- `void appendRow(const QList<QStandardItem *> &items)`
- `void appendRow(QStandardItem *item)`
- `void appendRows(const QList<QStandardItem *> &items)`
- `QBrush background() const`
- `Qt::CheckState checkState() const`
- `QStandardItem * child(int row, int column = 0) const`
- `void clearData()`
- `virtual QStandardItem * clone() const`
- `int column() const`
- `int columnCount() const`
- `virtual QVariant data(int role = Qt::UserRole + 1) const`
- `Qt::ItemFlags flags() const`
- `QFont font() const`
- `QBrush foreground() const`
- `bool hasChildren() const`
- `QIcon icon() const`
- `QModelIndex index() const`
- `void insertColumn(int column, const QList<QStandardItem *> &items)`
- `void insertColumns(int column, int count)`
- `void insertRow(int row, const QList<QStandardItem *> &items)`
- `void insertRow(int row, QStandardItem *item)`
- `void insertRows(int row, const QList<QStandardItem *> &items)`
- `void insertRows(int row, int count)`
- `bool isAutoTristate() const`
- `bool isCheckable() const`
- `bool isDragEnabled() const`
- `bool isDropEnabled() const`
- `bool isEditable() const`
- `bool isEnabled() const`
- `bool isSelectable() const`
- `bool isUserTristate() const`
- `QStandardItemModel * model() const`
- `(since 6.0) virtual void multiData(QModelRoleDataSpan roleDataSpan) const`
- `QStandardItem * parent() const`
- `virtual void read(QDataStream &in)`
- `void removeColumn(int column)`
- `void removeColumns(int column, int count)`
- `void removeRow(int row)`
- `void removeRows(int row, int count)`
- `int row() const`
- `int rowCount() const`
- `void setAccessibleDescription(const QString &accessibleDescription)`
- `void setAccessibleText(const QString &accessibleText)`
- `void setAutoTristate(bool tristate)`
- `void setBackground(const QBrush &brush)`
- `void setCheckState(Qt::CheckState state)`
- `void setCheckable(bool checkable)`
- `void setChild(int row, int column, QStandardItem *item)`
- `void setChild(int row, QStandardItem *item)`
- `void setColumnCount(int columns)`
- `virtual void setData(const QVariant &value, int role = Qt::UserRole + 1)`
- `void setDragEnabled(bool dragEnabled)`
- `void setDropEnabled(bool dropEnabled)`
- `void setEditable(bool editable)`
- `void setEnabled(bool enabled)`
- `void setFlags(Qt::ItemFlags flags)`
- `void setFont(const QFont &font)`
- `void setForeground(const QBrush &brush)`
- `void setIcon(const QIcon &icon)`
- `void setRowCount(int rows)`
- `void setSelectable(bool selectable)`
- `void setSizeHint(const QSize &size)`
- `void setStatusTip(const QString &statusTip)`
- `void setText(const QString &text)`
- `void setTextAlignment(Qt::Alignment alignment)`
- `void setToolTip(const QString &toolTip)`
- `void setUserTristate(bool tristate)`
- `void setWhatsThis(const QString &whatsThis)`
- `QSize sizeHint() const`
- `void sortChildren(int column, Qt::SortOrder order = Qt::AscendingOrder)`
- `QString statusTip() const`
- `QStandardItem * takeChild(int row, int column = 0)`
- `QList<QStandardItem *> takeColumn(int column)`
- `QList<QStandardItem *> takeRow(int row)`
- `QString text() const`
- `Qt::Alignment textAlignment() const`
- `QString toolTip() const`
- `virtual int type() const`
- `QString whatsThis() const`
- `virtual void write(QDataStream &out) const`
- `virtual bool operator<(const QStandardItem &other) const`

### 保护函数

- `QStandardItem(const QStandardItem &other)`
- `void emitDataChanged()`
- `QStandardItem & operator=(const QStandardItem &other)`

### 相关非成员函数

- `QDataStream & operator<<(QDataStream &out, const QStandardItem &item)`
- `QDataStream & operator>>(QDataStream &in, QStandardItem &item)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QStandardItem::ItemType`

**作用与语义：**

该枚举描述了用于描述标准项目的类型。
- `QStandardItem::Type`：`0`;标准物品的默认类型。
- `QStandardItem::UserType`：`1000`;自定义类型的最小值。低于 UserType 的值由 Qt 保留。
你可以在`QStandardItem`子类中定义新的用户类型，以确保自定义项目被特别处理;例如，在排序时。

### `QStandardItem::QStandardItem()`

**作用与语义：**

构造一个物品。

### `[explicit] QStandardItem::QStandardItem(const QString &text)`

**作用与语义：**

构造出具有给定`text`的物品。

### `QStandardItem::QStandardItem(const QIcon &icon, const QString &text)`

**作用与语义：**

构造出具有给定`icon`和`text`的物品。

### `[explicit] QStandardItem::QStandardItem(int rows, int columns = 1)`

**作用与语义：**

构造一个包含`rows`行和 `columns` 列子项的项目。

### `[protected] QStandardItem::QStandardItem(const QStandardItem &other)`

**作用与语义：**

构造`other`的副本。注意`model()`不会被复制。
这个函数在重新实现`clone()`时非常有用。

### `[virtual noexcept] QStandardItem::~QStandardItem()`

**作用与语义：**

摧毁了物品。这会导致物品的子嗣也被摧毁。

### `QString QStandardItem::accessibleDescription() const`

**作用与语义：**

返回该物品的可访问描述。
辅助技术（即无法使用传统交互方式的用户）使用无障碍描述。

### `QString QStandardItem::accessibleText() const`

**作用与语义：**

返回该项目可访问的文本。
辅助技术（即无法使用传统交互方式的用户）使用了可访问文本。

### `void QStandardItem::appendColumn(const QList<QStandardItem *> &items)`

**作用与语义：**

附加包含`items`的列。如有必要，行数增加至`items`大小。

### `void QStandardItem::appendRow(const QList<QStandardItem *> &items)`

**作用与语义：**

附加包含`items`的行。如有必要，列数增加至`items`大小。

### `void QStandardItem::appendRow(QStandardItem *item)`

**作用与语义：**

附加包含`item`的行。
当构建只有一列的列表或树时，该函数提供了方便地添加单个新项的方式。

### `void QStandardItem::appendRows(const QList<QStandardItem *> &items)`

**作用与语义：**

附加包含 `items` 的行。列数不会改变。

### `QBrush QStandardItem::background() const`

**作用与语义：**

返回用于渲染物品背景的画笔。

### `Qt::CheckState QStandardItem::checkState() const`

**作用与语义：**

返回已检查的物品状态。

### `QStandardItem *QStandardItem::child(int row, int column = 0) const`

**作用与语义：**

如果已设置子项，返回位于（`row`， `column`）的子项;否则返回`nullptr`。

### `void QStandardItem::clearData()`

**作用与语义：**

移除之前所有角色中的所有数据。

### `[virtual] QStandardItem *QStandardItem::clone() const`

**作用与语义：**

返回该物品的副本。该物品的子节点不会被复制。
在子类`QStandardItem`时，你可以重新实现这个函数，为`QStandardItemModel`提供一个工厂，用来按需创建新物品。

### `int QStandardItem::column() const`

**作用与语义：**

返回该项位于父表子表中的列，若无父项则返回-1。

### `int QStandardItem::columnCount() const`

**作用与语义：**

返回该项的子项列数。

### `[virtual] QVariant QStandardItem::data(int role = Qt::UserRole + 1) const`

**作用与语义：**

返回该项目在给定`role`中的数据，若无该角色数据则返回无效`QVariant`。
如果你重新实现这个函数，你的重实现应该调用你未处理的角色的基础实现，否则调用`flags()`、`isCheckable()`、`isEditable()`等标记将无法起作用。
注意：默认实现中，`Qt::EditRole` 和 `Qt::DisplayRole` 视为指的是相同的数据。

### `[protected] void QStandardItem::emitDataChanged()`

**作用与语义：**

使该物品关联的模型对该物品发出`dataChanged()`信号。
通常只有在你已经子类化`QStandardItem`并重新实现了`data()`和/或`setData()`时才需要调用这个函数。

### `Qt::ItemFlags QStandardItem::flags() const`

**作用与语义：**

返回该物品的标记。
物品标志决定了用户如何与该物品交互。
默认情况下，项目是启用的、可编辑、可选择、可勾选的，并且可以作为拖放操作的源和投放目标使用。

### `QFont QStandardItem::font() const`

**作用与语义：**

返回用于渲染该物品文本的字体。

### `QBrush QStandardItem::foreground() const`

**作用与语义：**

返回用于渲染物品前景（例如文本）的画笔。

### `bool QStandardItem::hasChildren() const`

**作用与语义：**

如果该项有子项，返回`true`;否则返回`false`。

### `QIcon QStandardItem::icon() const`

**作用与语义：**

返回物品图标。

### `QModelIndex QStandardItem::index() const`

**作用与语义：**

返回与该物品相关的`QModelIndex`。
当你需要在基于`QModelIndex`的API（例如`QAbstractItemView`）中调用项目功能时，你可以调用该函数获取对应项目在模型中位置的索引。
如果该项目未与模型关联，则返回无效`QModelIndex`。

### `void QStandardItem::insertColumn(int column, const QList<QStandardItem *> &items)`

**作用与语义：**

在 `column` 插入一列，包含 `items`。如有必要，行数增加到 `items` 大小。

### `void QStandardItem::insertColumns(int column, int count)`

**作用与语义：**

在第`column`列插入`count`列子项。

### `void QStandardItem::insertRow(int row, const QList<QStandardItem *> &items)`

**作用与语义：**

在`row`插入包含`items`的行。如有必要，列数增加至`items`大小。

### `void QStandardItem::insertRow(int row, QStandardItem *item)`

**作用与语义：**

在`row`插入一行包含`item`。
当构建只有一列的列表或树时，该函数提供了插入单一新项的便捷方式。

### `void QStandardItem::insertRows(int row, const QList<QStandardItem *> &items)`

**作用与语义：**

插入`items`在`row`。列数不会改变。

### `void QStandardItem::insertRows(int row, int count)`

**作用与语义：**

在第`row`行插入`count`行子项。

### `bool QStandardItem::isAutoTristate() const`

**作用与语义：**

返回该物品是否为三态且由`QTreeWidget`控制。
默认值为假。

### `bool QStandardItem::isCheckable() const`

**作用与语义：**

返回该项是否可被用户检查。
默认值为假。

### `bool QStandardItem::isDragEnabled() const`

**作用与语义：**

返回该物品是否支持拖曳。启用拖曳的物品可以被用户拖拽。
默认值为真。
注意，拖曳工作时必须在视图中启用拖拽;详见`QAbstractItemView::dragEnabled`。

### `bool QStandardItem::isDropEnabled() const`

**作用与语义：**

返回物品是否启用掉落。当物品被投放启用时，它可以作为掉落目标使用。
默认值为真。

### `bool QStandardItem::isEditable() const`

**作用与语义：**

返回该项目是否可以被用户编辑。
当某个项目可编辑（并且已启用）时，用户可以通过调用视图中的某个编辑触发器来编辑该项目;详见`QAbstractItemView::editTriggers`。
默认值为真。

### `bool QStandardItem::isEnabled() const`

**作用与语义：**

返回物品是否被启用。
当某个物品被启用时，用户可以与它进行交互。可能的交互类型由其他物品标志（如`isEditable()`和 `isSelectable()`）指定。
默认值为真。

### `bool QStandardItem::isSelectable() const`

**作用与语义：**

返回该项是否可被用户选择。
默认值为真。

### `bool QStandardItem::isUserTristate() const`

**作用与语义：**

返回该项是否为三态;即如果该项目可用三种独立状态检查，且用户可以循环所有三种状态。
默认值为假。

### `QStandardItemModel *QStandardItem::model() const`

**作用与语义：**

返回该物品所属的`QStandardItemModel`。
如果该项不是属于该模型的另一个项的子项，该函数返回`nullptr`。

### `[virtual, since 6.0] void QStandardItem::multiData(QModelRoleDataSpan roleDataSpan) const`

**作用与语义：**

用该项的数据填充`roleDataSpan`区间。
默认实现只需为该区间中的每个角色调用`data()`。

### `QStandardItem *QStandardItem::parent() const`

**作用与语义：**

返回该物品的父项，若没有父项则返回 `nullptr`。
注意：对于顶级项目，parent() 返回 `nullptr`。要接收顶级项目的父项目，请使用 `QStandardItemModel::invisibleRootItem()`。

### `[virtual] void QStandardItem::read(QDataStream &in)`

**作用与语义：**

读取流`in`中的项目。只读取该项目的数据和标志，不会读取子项目。

### `void QStandardItem::removeColumn(int column)`

**作用与语义：**

移除给定的`column`。列中原本的项目被删除。

### `void QStandardItem::removeColumns(int column, int count)`

**作用与语义：**

移除`count`列`column`的列。那些列中的项目被删除。

### `void QStandardItem::removeRow(int row)`

**作用与语义：**

移除给定的`row`。该行中的物品被删除。

### `void QStandardItem::removeRows(int row, int count)`

**作用与语义：**

移除`row`行的`count`行。那些行中的物品被删除。

### `int QStandardItem::row() const`

**作用与语义：**

返回该项位于父表子表中的行，若无父项则返回 -1。

### `int QStandardItem::rowCount() const`

**作用与语义：**

返回该项的子项行数。

### `void QStandardItem::setAccessibleDescription(const QString &accessibleDescription)`

**作用与语义：**

将该项的可访问描述设置为`accessibleDescription`指定的字符串。
辅助技术（即无法使用传统交互方式的用户）使用无障碍描述。

### `void QStandardItem::setAccessibleText(const QString &accessibleText)`

**作用与语义：**

将该项的可访问文本设置为`accessibleText`指定的字符串。
辅助技术（即无法使用传统交互方式的用户）使用了可访问文本。

### `void QStandardItem::setAutoTristate(bool tristate)`

**作用与语义：**

如果`tristate` `true`，确定该项为三态，并由`QTreeWidget`控制。这使得`QTreeWidget`中父项的状态能够自动管理（如果所有子节点都被检查，则检查为未检查;如果所有子节点都未检查，则为未检查;如果只有部分子节点被检查，则部分检查）。

### `void QStandardItem::setBackground(const QBrush &brush)`

**作用与语义：**

将物品的背景画笔设置为指定的`brush`。

### `void QStandardItem::setCheckState(Qt::CheckState state)`

**作用与语义：**

将该项的检查状态设置为`state`。

### `void QStandardItem::setCheckable(bool checkable)`

**作用与语义：**

设置该项是否可被用户检查。如果`checkable`为真，用户可以检查该项;否则，用户无法检查该项。
item delegate 会生成一个可勾选的项目，并在该项目文本旁边有一个复选框。

### `void QStandardItem::setChild(int row, int column, QStandardItem *item)`

**作用与语义：**

将子项（`row`， `column`）设置为`item`。该项（父项）拥有`item`的所有权。如有必要，行数和列数增加以适应该项。
注意：`item`传递`nullptr`会移除该物品。

### `void QStandardItem::setChild(int row, QStandardItem *item)`

**作用与语义：**

将孩子设定为`row`到`item`。

### `void QStandardItem::setColumnCount(int columns)`

**作用与语义：**

将子项列数设置为`columns`。如果小于`columnCount()`，则丢弃不需要列中的数据。

### `[virtual] void QStandardItem::setData(const QVariant &value, int role = Qt::UserRole + 1)`

**作用与语义：**

将该物品在给定`role`中的数据设置为指定的`value`。
如果你对`QStandardItem`子类并重新实现该函数，你的重实现应当：
- 如果您未调用 setData() 的基础实现，则调用 `emitDataChanged()`。这将确保例如使用该模型的视图会被通知更改
- 调用你未处理的角色的基础实现，否则设置标志，例如调用`setFlags()`、`setCheckable()`、`setEditable()`等，将无法实现。
注意：默认实现中，`Qt::EditRole` 和 `Qt::DisplayRole` 视为指的是相同的数据。

### `void QStandardItem::setDragEnabled(bool dragEnabled)`

**作用与语义：**

设置该项目是否支持拖曳。如果`dragEnabled`为真，用户可以拖动该项目;否则，用户无法拖动该项目。
注意，你还需要确保视图中启用了物品拖拽功能;详见 `QAbstractItemView::dragEnabled`。

### `void QStandardItem::setDropEnabled(bool dropEnabled)`

**作用与语义：**

设置该物品是否允许掉落。如果`dropEnabled`为真，该物品可以作为掉落目标使用;否则，不能。
注意，你还需要确保视图中启用了投放;参见`QWidget::acceptDrops()`;并且模型支持所需的投放动作;详见`QAbstractItemModel::supportedDropActions()`。

### `void QStandardItem::setEditable(bool editable)`

**作用与语义：**

设置该项是否可编辑。如果`editable`为真，用户可以编辑该项;否则，用户无法编辑该项。
用户如何编辑视图中的项目由视图的编辑触发器决定;详见`QAbstractItemView::editTriggers`。

### `void QStandardItem::setEnabled(bool enabled)`

**作用与语义：**

设置该项是否被启用。如果`enabled`为真，则该项已启用，意味着用户可以与该项互动;如果`enabled`为假，则用户无法与该项交互。
该标志优先于其他物品标志;例如，如果某个物品未被启用，用户无法选择该物品，即使已设置`Qt::ItemIsSelectable`标志。

### `void QStandardItem::setFlags(Qt::ItemFlags flags)`

**作用与语义：**

将该物品的标记设置为`flags`。
物品标志决定用户如何与该物品交互。这通常用于禁用物品。

### `void QStandardItem::setFont(const QFont &font)`

**作用与语义：**

设置用于显示物品文本的字体为给定的`font`。

### `void QStandardItem::setForeground(const QBrush &brush)`

**作用与语义：**

将用于显示物品前景（例如文本）的画笔设置为给定的`brush`。

### `void QStandardItem::setIcon(const QIcon &icon)`

**作用与语义：**

将物品图标设置为指定的 `icon`。

### `void QStandardItem::setRowCount(int rows)`

**作用与语义：**

将子项行数设为`rows`。如果小于`rowCount()`，则丢弃不需要行中的数据。

### `void QStandardItem::setSelectable(bool selectable)`

**作用与语义：**

决定该项是否可被选择。如果`selectable`为真，用户可以选择该项;否则，用户无法选择该项。
你可以通过操作它们的视图属性来控制选择行为和模式;参见`QAbstractItemView::selectionMode`和`QAbstractItemView::selectionBehavior`。

### `void QStandardItem::setSizeHint(const QSize &size)`

**作用与语义：**

设置该项的大小提示为`size`。如果没有设置大小提示，项目代理将根据项目数据计算大小提示。

### `void QStandardItem::setStatusTip(const QString &statusTip)`

**作用与语义：**

将项目的状态提示设置为`statusTip`指定的字符串。

### `void QStandardItem::setText(const QString &text)`

**作用与语义：**

将物品文本设置为指定的`text`。

### `void QStandardItem::setTextAlignment(Qt::Alignment alignment)`

**作用与语义：**

将该项目文本的文本对齐设置为指定的`alignment`。

### `void QStandardItem::setToolTip(const QString &toolTip)`

**作用与语义：**

将物品的工具提示设置为`toolTip`指定的字符串。

### `void QStandardItem::setUserTristate(bool tristate)`

**作用与语义：**

设定该项是否为三态，并由用户控制。如果`tristate`为真，用户可以循环经历三个独立状态;否则，该项可检查为两个状态。（注意，这也要求该项可检验;详见 `isCheckable()`。）。

### `void QStandardItem::setWhatsThis(const QString &whatsThis)`

**作用与语义：**

将物品的“这是什么？”帮助设置为`whatsThis`指定的字符串。

### `QSize QStandardItem::sizeHint() const`

**作用与语义：**

返回该物品的尺寸提示，若未设置大小提示则返回无效`QSize`。
如果没有设置大小提示，项目代理将根据项目数据计算大小提示。

### `void QStandardItem::sortChildren(int column, Qt::SortOrder order = Qt::AscendingOrder)`

**作用与语义：**

用给定`order`按给定`column`中的值对该项的子节点进行排序。
注意：该函数是递归的，因此它会排序该项的子节点、其子节点等。

### `QString QStandardItem::statusTip() const`

**作用与语义：**

返回该物品的状态提示。

### `QStandardItem *QStandardItem::takeChild(int row, int column = 0)`

**作用与语义：**

在不删除（`row`， `column`）的子项时移除，并返回指向该项的指针。如果给定位置没有子项，该函数返回`nullptr`。
注意，这个函数与`takeRow()`和`takeColumn()`不同，不影响子表的维度。

### `QList<QStandardItem *> QStandardItem::takeColumn(int column)`

**作用与语义：**

在不删除列项的情况下移除`column`，并返回指向已移除项的指针列表。对于列中尚未设置的项，列表中对应的指针将被`nullptr`。

### `QList<QStandardItem *> QStandardItem::takeRow(int row)`

**作用与语义：**

移除`row`而不删除行项，返回指向已移除项的指针列表。对于未设置的行中项，列表中对应的指针将被`nullptr`。

### `QString QStandardItem::text() const`

**作用与语义：**

返回该项目的文本。这是在视图中呈现给用户的文本。

### `Qt::Alignment QStandardItem::textAlignment() const`

**作用与语义：**

返回该项文本的文本对齐。

### `QString QStandardItem::toolTip() const`

**作用与语义：**

返回物品的工具提示。

### `[virtual] int QStandardItem::type() const`

**作用与语义：**

返回该项的类型。该类型用于区分自定义项和基类。在子类`QStandardItem`时，应重新实现该函数，并返回一个大于或等于`UserType`的新值。

### `QString QStandardItem::whatsThis() const`

**作用与语义：**

还给物品的“这是什么？”帮助。

### `[virtual] void QStandardItem::write(QDataStream &out) const`

**作用与语义：**

将项目写入流`out`。只写入该项目的数据和标志，不写子项目。

### `[virtual] bool QStandardItem::operator<(const QStandardItem &other) const`

**作用与语义：**

如果该项小于`other`，返回`true`;否则返回`false`。
默认实现使用该项目的排序角色数据（见`QStandardItemModel::sortRole`）进行比较，前提是该项目属于某个模型;否则，则使用该项目的 `Qt::DisplayRole` （`text()`） 数据进行比较。
`sortChildren()`和`QStandardItemModel::sort()`在排序物品时使用这个函数。如果你想要自定义排序，可以子类`QStandardItem`并重新实现这个函数。

### `[protected] QStandardItem &QStandardItem::operator=(const QStandardItem &other)`

**作用与语义：**

将`other`的数据和标志分配给该项。注意`type()`和`model()`不会被复制。
这个函数在重新实现`clone()`时非常有用。

### `QDataStream &operator<<(QDataStream &out, const QStandardItem &item)`

**作用与语义：**

写入流媒体`QStandardItem` `item` `out`。
该操作员使用`QStandardItem::write()`。

### `QDataStream &operator>>(QDataStream &in, QStandardItem &item)`

**作用与语义：**

读取流`in`的`QStandardItem`到`item`。
该操作员使用`QStandardItem::read()`。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

### 状态和错误边界

把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

### 线程边界

如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

### 最容易出现的错误

不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QStandardItem` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
