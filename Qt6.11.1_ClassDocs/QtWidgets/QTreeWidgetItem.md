# QTreeWidgetItem

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QTreeWidgetItem` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QTreeWidgetItem` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QTreeWidgetItem>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

### 状态、生命周期和线程

**生命周期：** 控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

**状态与结果：** 控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

**线程与事件循环：** 所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

## 3. 直接使用

需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。 使用时通常按这个过程组织：创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum ChildIndicatorPolicy { ShowIndicator, DontShowIndicator, DontShowIndicatorWhenChildless }`
- `enum ItemType { Type, UserType }`

### 公有函数

- `QTreeWidgetItem(int type = Type)`
- `QTreeWidgetItem(QTreeWidget *parent, int type = Type)`
- `QTreeWidgetItem(QTreeWidgetItem *parent, int type = Type)`
- `QTreeWidgetItem(const QStringList &strings, int type = Type)`
- `QTreeWidgetItem(QTreeWidget *parent, QTreeWidgetItem *preceding, int type = Type)`
- `QTreeWidgetItem(QTreeWidget *parent, const QStringList &strings, int type = Type)`
- `QTreeWidgetItem(QTreeWidgetItem *parent, QTreeWidgetItem *preceding, int type = Type)`
- `QTreeWidgetItem(QTreeWidgetItem *parent, const QStringList &strings, int type = Type)`
- `QTreeWidgetItem(const QTreeWidgetItem &other)`
- `virtual ~QTreeWidgetItem()`
- `void addChild(QTreeWidgetItem *child)`
- `void addChildren(const QList<QTreeWidgetItem *> &children)`
- `QBrush background(int column) const`
- `Qt::CheckState checkState(int column) const`
- `QTreeWidgetItem * child(int index) const`
- `int childCount() const`
- `QTreeWidgetItem::ChildIndicatorPolicy childIndicatorPolicy() const`
- `virtual QTreeWidgetItem * clone() const`
- `int columnCount() const`
- `virtual QVariant data(int column, int role) const`
- `Qt::ItemFlags flags() const`
- `QFont font(int column) const`
- `QBrush foreground(int column) const`
- `QIcon icon(int column) const`
- `int indexOfChild(QTreeWidgetItem *child) const`
- `void insertChild(int index, QTreeWidgetItem *child)`
- `void insertChildren(int index, const QList<QTreeWidgetItem *> &children)`
- `bool isDisabled() const`
- `bool isExpanded() const`
- `bool isFirstColumnSpanned() const`
- `bool isHidden() const`
- `bool isSelected() const`
- `QTreeWidgetItem * parent() const`
- `virtual void read(QDataStream &in)`
- `void removeChild(QTreeWidgetItem *child)`
- `void setBackground(int column, const QBrush &brush)`
- `void setCheckState(int column, Qt::CheckState state)`
- `void setChildIndicatorPolicy(QTreeWidgetItem::ChildIndicatorPolicy policy)`
- `virtual void setData(int column, int role, const QVariant &value)`
- `void setDisabled(bool disabled)`
- `void setExpanded(bool expand)`
- `void setFirstColumnSpanned(bool span)`
- `void setFlags(Qt::ItemFlags flags)`
- `void setFont(int column, const QFont &font)`
- `void setForeground(int column, const QBrush &brush)`
- `void setHidden(bool hide)`
- `void setIcon(int column, const QIcon &icon)`
- `void setSelected(bool select)`
- `void setSizeHint(int column, const QSize &size)`
- `void setStatusTip(int column, const QString &statusTip)`
- `void setText(int column, const QString &text)`
- `(since 6.4) void setTextAlignment(int column, Qt::Alignment alignment)`
- `void setToolTip(int column, const QString &toolTip)`
- `void setWhatsThis(int column, const QString &whatsThis)`
- `QSize sizeHint(int column) const`
- `void sortChildren(int column, Qt::SortOrder order)`
- `QString statusTip(int column) const`
- `QTreeWidgetItem * takeChild(int index)`
- `QList<QTreeWidgetItem *> takeChildren()`
- `QString text(int column) const`
- `int textAlignment(int column) const`
- `QString toolTip(int column) const`
- `QTreeWidget * treeWidget() const`
- `int type() const`
- `QString whatsThis(int column) const`
- `virtual void write(QDataStream &out) const`
- `virtual bool operator<(const QTreeWidgetItem &other) const`
- `QTreeWidgetItem & operator=(const QTreeWidgetItem &other)`

### 保护函数

- `void emitDataChanged()`

### 相关非成员函数

- `QDataStream & operator<<(QDataStream &out, const QTreeWidgetItem &item)`
- `QDataStream & operator>>(QDataStream &in, QTreeWidgetItem &item)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QTreeWidgetItem::ItemType`

**作用与语义：**

该枚举描述了用于描述树控件项目的类型。
- `QTreeWidgetItem::Type`：`0`;树状控件项目的默认类型。
- `QTreeWidgetItem::UserType`：`1000`;自定义类型的最小值。低于 UserType 的值由 Qt 保留。
你可以在`QTreeWidgetItem`子类中定义新的用户类型，以确保自定义项目被特别对待;例如，在排序物品时。

### `[explicit] QTreeWidgetItem::QTreeWidgetItem(int type = Type)`

**作用与语义：**

构造指定`type`的树控件项。该项必须插入树控件中。

### `[explicit] QTreeWidgetItem::QTreeWidgetItem(QTreeWidget *parent, int type = Type)`

**作用与语义：**

构造指定`type`的树控件项，并将其附加到给定`parent`中的项上。

### `[explicit] QTreeWidgetItem::QTreeWidgetItem(QTreeWidgetItem *parent, int type = Type)`

**作用与语义：**

构建一个树状控件项并将其附加到给定的`parent`上。

### `[explicit] QTreeWidgetItem::QTreeWidgetItem(const QStringList &strings, int type = Type)`

**作用与语义：**

构建指定`type`的树状控件项。该项必须插入树状控件中。给定的`strings`列表将设置为该项中每一列的条目文本。

### `QTreeWidgetItem::QTreeWidgetItem(QTreeWidget *parent, QTreeWidgetItem *preceding, int type = Type)`

**作用与语义：**

构造指定`type`的树控件项，并在`preceding`项之后插入给定`parent`。

### `QTreeWidgetItem::QTreeWidgetItem(QTreeWidget *parent, const QStringList &strings, int type = Type)`

**作用与语义：**

构建指定`type`的树状控件项，并将其附加到给定`parent`中的项上。给定的`strings`列表将被设置为该项中每一列的条目文本。

### `QTreeWidgetItem::QTreeWidgetItem(QTreeWidgetItem *parent, QTreeWidgetItem *preceding, int type = Type)`

**作用与语义：**

构造指定`type`的树控件项，插入在`preceding`子项之后的`parent`中。

### `QTreeWidgetItem::QTreeWidgetItem(QTreeWidgetItem *parent, const QStringList &strings, int type = Type)`

**作用与语义：**

构建一个树控件项并将其附加到给定的`parent`上。给定的`strings`列表将被设置为该项中每一列的条目文本。

### `QTreeWidgetItem::QTreeWidgetItem(const QTreeWidgetItem &other)`

**作用与语义：**

构造`other`的副本。注意`type()`和`treeWidget()`不被复制。
该函数在重新实现`clone()`时非常有用。

### `[virtual noexcept] QTreeWidgetItem::~QTreeWidgetItem()`

**作用与语义：**

摧毁这个树小部件。
该项目将从已添加的`QTreeWidget`中移除。这使得随时删除物品是安全的。

### `void QTreeWidgetItem::addChild(QTreeWidgetItem *child)`

**作用与语义：**

将`child`项附加到子项列表中。

### `void QTreeWidgetItem::addChildren(const QList<QTreeWidgetItem *> &children)`

**作用与语义：**

附加给定的`children`列表。

### `QBrush QTreeWidgetItem::background(int column) const`

**作用与语义：**

返回用于渲染指定`column`背景的画笔。

### `Qt::CheckState QTreeWidgetItem::checkState(int column) const`

**作用与语义：**

返回给定`column`标签的检查状态。

### `QTreeWidgetItem *QTreeWidgetItem::child(int index) const`

**作用与语义：**

在该项子节点列表中的指定`index`返回该项目。

### `int QTreeWidgetItem::childCount() const`

**作用与语义：**

返回子项目的数量。

### `QTreeWidgetItem::ChildIndicatorPolicy QTreeWidgetItem::childIndicatorPolicy() const`

**作用与语义：**

返回项目指示策略。该策略决定树枝展开/折叠指示器何时显示。

### `[virtual] QTreeWidgetItem *QTreeWidgetItem::clone() const`

**作用与语义：**

创建该物品及其子节点的深度副本。

### `int QTreeWidgetItem::columnCount() const`

**作用与语义：**

返回该项的列数。

### `[virtual] QVariant QTreeWidgetItem::data(int column, int role) const`

**作用与语义：**

返回该物品的`column`和`role`值。

### `[protected] void QTreeWidgetItem::emitDataChanged()`

**作用与语义：**

使与该物品相关的模型对该物品发出`dataChanged()`信号。
通常只有在你已经子类化`QTreeWidgetItem`并重新实现了`data()`和/或`setData()`时才需要调用这个函数。

### `Qt::ItemFlags QTreeWidgetItem::flags() const`

**作用与语义：**

返回用于描述该项目的标志。这些标志决定该项目是否可以被检查、编辑和选择。
标志的默认值为 `Qt::ItemIsSelectable` |`Qt::ItemIsUserCheckable` |`Qt::ItemIsEnabled` |`Qt::ItemIsDragEnabled` |`Qt::ItemIsDropEnabled`。

### `QFont QTreeWidgetItem::font(int column) const`

**作用与语义：**

返回用于指定`column`渲染文本的字体。

### `QBrush QTreeWidgetItem::foreground(int column) const`

**作用与语义：**

返回用于渲染指定`column`前景（例如文本）的画笔。设置默认构造画笔将允许视图使用样式中的默认颜色。

### `QIcon QTreeWidgetItem::icon(int column) const`

**作用与语义：**

返回指定`column`中显示的图标。

### `int QTreeWidgetItem::indexOfChild(QTreeWidgetItem *child) const`

**作用与语义：**

返回该项子项列表中给定`child`的索引。

### `void QTreeWidgetItem::insertChild(int index, QTreeWidgetItem *child)`

**作用与语义：**

在子项列表中插入`index`的`child`项。
如果孩子已经被植入了其他地方，就不会再入。

### `void QTreeWidgetItem::insertChildren(int index, const QList<QTreeWidgetItem *> &children)`

**作用与语义：**

将给定的`children`列表插入到`index` 的子项列表中。
已经植入过其他地方的孩子不会被植入。

### `bool QTreeWidgetItem::isDisabled() const`

**作用与语义：**

如果物品被禁用，返回`true`;否则返回`false`。

### `bool QTreeWidgetItem::isExpanded() const`

**作用与语义：**

如果物品被扩展，返回`true`，否则返回 `false`。

### `bool QTreeWidgetItem::isFirstColumnSpanned() const`

**作用与语义：**

如果该项跨越了一行中的所有列，返回`true`;否则返回`false`。

### `bool QTreeWidgetItem::isHidden() const`

**作用与语义：**

如果物品被隐藏，会`true`返回;否则返回`false`。

### `bool QTreeWidgetItem::isSelected() const`

**作用与语义：**

如果选中了该物品，返回`true`，否则返回`false`。

### `QTreeWidgetItem *QTreeWidgetItem::parent() const`

**作用与语义：**

返回该物品的父节点。

### `[virtual] void QTreeWidgetItem::read(QDataStream &in)`

**作用与语义：**

读取流`in`中的项目。这只会将数据读入单个项目。

### `void QTreeWidgetItem::removeChild(QTreeWidgetItem *child)`

**作用与语义：**

移除`child`指示的物品。移除的物品不会被删除。

### `void QTreeWidgetItem::setBackground(int column, const QBrush &brush)`

**作用与语义：**

将标签在指定`column`的背景画笔设置为指定的`brush`。设置默认构造画笔后，视图可以使用样式中的默认颜色。
注意：如果 Qt 样式表与 setBackground() 在同一小部件上使用，且设置冲突时样式表将优先。

### `void QTreeWidgetItem::setCheckState(int column, Qt::CheckState state)`

**作用与语义：**

将该项目在给定`column`检查状态设置为`state`。

### `void QTreeWidgetItem::setChildIndicatorPolicy(QTreeWidgetItem::ChildIndicatorPolicy policy)`

**作用与语义：**

设置项目指示器`policy`。该策略决定树枝扩展/折叠指示器何时显示。默认值为`DontShowIndicatorWhenChildless`。

### `[virtual] void QTreeWidgetItem::setData(int column, int role, const QVariant &value)`

**作用与语义：**

设定物品`column`值，`role`给定`value`。
`role`描述了`value`指定的数据类型，并由`Qt::ItemDataRole`枚举定义。
注意：默认实现中，`Qt::EditRole` 和 `Qt::DisplayRole` 视为指的是相同的数据。

### `void QTreeWidgetItem::setDisabled(bool disabled)`

**作用与语义：**

如果`disabled`为真，则禁用该项;否则启用该项。

### `void QTreeWidgetItem::setExpanded(bool expand)`

**作用与语义：**

如果`expand`为真，则展开该项，否则将该项折叠。
警告：必须先将`QTreeWidgetItem`添加到`QTreeWidget`中，才能调用此函数。

### `void QTreeWidgetItem::setFirstColumnSpanned(bool span)`

**作用与语义：**

如果 `span`为真，则设置第一部分跨越所有列;否则显示所有项目部分。

### `void QTreeWidgetItem::setFlags(Qt::ItemFlags flags)`

**作用与语义：**

将该物品的标志设置为给定的`flags`。这些标志决定了该物品是否可以被选择或修改。这通常用于禁用某个物品。

### `void QTreeWidgetItem::setFont(int column, const QFont &font)`

**作用与语义：**

将用于显示给定`column`文本的字体设置为给定的`font`。

### `void QTreeWidgetItem::setForeground(int column, const QBrush &brush)`

**作用与语义：**

将标签在指定`column`中的前景画笔设置为指定的`brush`。

### `void QTreeWidgetItem::setHidden(bool hide)`

**作用与语义：**

如果`hide`为真，则隐藏该物品，否则显示该物品。
注意：如果该项当前不在视图中，调用该函数无效。特别是，调用`setHidden(true)`项后才添加到视图，才会出现可见的项。

### `void QTreeWidgetItem::setIcon(int column, const QIcon &icon)`

**作用与语义：**

将显示在指定`column`中的图标设置为`icon`。

### `void QTreeWidgetItem::setSelected(bool select)`

**作用与语义：**

将选中的状态设置为`select`。

### `void QTreeWidgetItem::setSizeHint(int column, const QSize &size)`

**作用与语义：**

将给定`column`中树项目的大小提示设置为`size`。如果未设置大小提示或`size`无效，项目代理将根据项目数据计算大小提示。

### `void QTreeWidgetItem::setStatusTip(int column, const QString &statusTip)`

**作用与语义：**

将给定`column`的状态提示设置为指定`statusTip`。`QTreeWidget`鼠标追踪功能需要启用才能使此功能正常工作。

### `void QTreeWidgetItem::setText(int column, const QString &text)`

**作用与语义：**

将文本设置为在给定`column`中显示给定`text`。

### `[since 6.4] void QTreeWidgetItem::setTextAlignment(int column, Qt::Alignment alignment)`

**作用与语义：**

将给定`column`标签的文本对齐设置为指定的`alignment`。

### `void QTreeWidgetItem::setToolTip(int column, const QString &toolTip)`

**作用与语义：**

将该`column`的工具提示设置为`toolTip`。

### `void QTreeWidgetItem::setWhatsThis(int column, const QString &whatsThis)`

**作用与语义：**

将“这是什么？”帮助设置给给定`column`的`whatsThis`。

### `QSize QTreeWidgetItem::sizeHint(int column) const`

**作用与语义：**

返回给定`column`中树状物的大小提示集（见`QSize`）。

### `void QTreeWidgetItem::sortChildren(int column, Qt::SortOrder order)`

**作用与语义：**

用给定`order`对该`column`中的值排序该项的子节点。
注意：如果该物品没有关联到`QTreeWidget`，这个功能就没有任何作用。

### `QString QTreeWidgetItem::statusTip(int column) const`

**作用与语义：**

返回给定`column`内容的状态提示。

### `QTreeWidgetItem *QTreeWidgetItem::takeChild(int index)`

**作用与语义：**

`index`移除该物品并返回，否则返回0。

### `QList<QTreeWidgetItem *> QTreeWidgetItem::takeChildren()`

**作用与语义：**

移除子列表并返回，否则返回空列表。

### `QString QTreeWidgetItem::text(int column) const`

**作用与语义：**

返回指定`column`的文本。

### `int QTreeWidgetItem::textAlignment(int column) const`

**作用与语义：**

返回给定`column`标签的文本对齐。
注意：出于历史原因，该函数返回一个 int。它将在Qt 7 中被纠正为返回 `Qt::Alignment`。

### `QString QTreeWidgetItem::toolTip(int column) const`

**作用与语义：**

返回给定`column`的工具提示。

### `QTreeWidget *QTreeWidgetItem::treeWidget() const`

**作用与语义：**

返回包含该项目的树状控件。

### `int QTreeWidgetItem::type() const`

**作用与语义：**

返回传递给`QTreeWidgetItem`构造器的类型。

### `QString QTreeWidgetItem::whatsThis(int column) const`

**作用与语义：**

返回“这是什么？”帮助，针对给定`column`的内容。

### `[virtual] void QTreeWidgetItem::write(QDataStream &out) const`

**作用与语义：**

将该项目写入流`out`。这只写入一个单一项目的数据。

### `[virtual] bool QTreeWidgetItem::operator<(const QTreeWidgetItem &other) const`

**作用与语义：**

如果该项的文本少于`other`项的文本，则返回`true`，否则返回`false`。

### `QTreeWidgetItem &QTreeWidgetItem::operator=(const QTreeWidgetItem &other)`

**作用与语义：**

将`other`的数据和标志分配给该项。注意`type()`和`treeWidget()`不会被复制。
这个函数在重新实现`clone()`时非常有用。

### `QDataStream &operator<<(QDataStream &out, const QTreeWidgetItem &item)`

**作用与语义：**

写入树状控件的项`item`流式`out`。
该算符使用`QTreeWidgetItem::write()`。

### `QDataStream &operator>>(QDataStream &in, QTreeWidgetItem &item)`

**作用与语义：**

将 stream `in` 中的树状控件项目读取到 `item`。
该操作员使用`QTreeWidgetItem::read()`。

### `enum ChildIndicatorPolicy { ShowIndicator, DontShowIndicator, DontShowIndicatorWhenChildless }`

**作用与语义：**

- `QTreeWidgetItem::ShowIndicator`：`0`;即使没有子，该物品也会显示展开和折叠的控制。
- `QTreeWidgetItem::DontShowIndicator`：`1`;即使有子节点，扩展和收缩的控制也永远不会显示。如果节点被强制打开，用户将无法展开或折叠该项目。
- `QTreeWidgetItem::DontShowIndicatorWhenChildless`：`2`;如果物品包含子节点，将显示展开和折叠的控制项。

## 6. 深入实践与常见坑

### 生命周期和资源边界

控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

### 状态和错误边界

控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

### 线程边界

所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

### 最容易出现的错误

优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QTreeWidgetItem` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
