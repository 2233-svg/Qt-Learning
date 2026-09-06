# QTableWidgetItem

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QTableWidgetItem` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QTableWidgetItem` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QTableWidgetItem>`
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

- `enum ItemType { Type, UserType }`

### 公有函数

- `QTableWidgetItem(int type = Type)`
- `QTableWidgetItem(const QString &text, int type = Type)`
- `QTableWidgetItem(const QIcon &icon, const QString &text, int type = Type)`
- `QTableWidgetItem(const QTableWidgetItem &other)`
- `virtual ~QTableWidgetItem()`
- `QBrush background() const`
- `Qt::CheckState checkState() const`
- `virtual QTableWidgetItem * clone() const`
- `int column() const`
- `virtual QVariant data(int role) const`
- `Qt::ItemFlags flags() const`
- `QFont font() const`
- `QBrush foreground() const`
- `QIcon icon() const`
- `bool isSelected() const`
- `virtual void read(QDataStream &in)`
- `int row() const`
- `void setBackground(const QBrush &brush)`
- `void setCheckState(Qt::CheckState state)`
- `virtual void setData(int role, const QVariant &value)`
- `void setFlags(Qt::ItemFlags flags)`
- `void setFont(const QFont &font)`
- `void setForeground(const QBrush &brush)`
- `void setIcon(const QIcon &icon)`
- `void setSelected(bool select)`
- `void setSizeHint(const QSize &size)`
- `void setStatusTip(const QString &statusTip)`
- `void setText(const QString &text)`
- `(since 6.4) void setTextAlignment(Qt::Alignment alignment)`
- `void setToolTip(const QString &toolTip)`
- `void setWhatsThis(const QString &whatsThis)`
- `QSize sizeHint() const`
- `QString statusTip() const`
- `QTableWidget * tableWidget() const`
- `QString text() const`
- `int textAlignment() const`
- `QString toolTip() const`
- `int type() const`
- `QString whatsThis() const`
- `virtual void write(QDataStream &out) const`
- `virtual bool operator<(const QTableWidgetItem &other) const`
- `QTableWidgetItem & operator=(const QTableWidgetItem &other)`

### 相关非成员函数

- `QDataStream & operator<<(QDataStream &out, const QTableWidgetItem &item)`
- `QDataStream & operator>>(QDataStream &in, QTableWidgetItem &item)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QTableWidgetItem::ItemType`

**作用与语义：**

该枚举描述了用于描述表控件项的类型。
- `QTableWidgetItem::Type`：`0`;表格控件的默认类型。
- `QTableWidgetItem::UserType`：`1000`;自定义类型的最小值。低于 UserType 的值由 Qt 保留。
你可以在`QTableWidgetItem`子类中定义新的用户类型，以确保自定义物品能被特别对待。

### `[explicit] QTableWidgetItem::QTableWidgetItem(int type = Type)`

**作用与语义：**

构造指定`type`中不属于任何表的表项。

### `[explicit] QTableWidgetItem::QTableWidgetItem(const QString &text, int type = Type)`

**作用与语义：**

用给定的`text`构造一个表项。

### `[explicit] QTableWidgetItem::QTableWidgetItem(const QIcon &icon, const QString &text, int type = Type)`

**作用与语义：**

构造一个具有给定`icon`和`text`的表项。

### `QTableWidgetItem::QTableWidgetItem(const QTableWidgetItem &other)`

**作用与语义：**

构造`other`的副本。注意`type()`和`tableWidget()`未被复制。
该函数在重新实现`clone()`时非常有用。

### `[virtual noexcept] QTableWidgetItem::~QTableWidgetItem()`

**作用与语义：**

会摧毁桌面物品。

### `QBrush QTableWidgetItem::background() const`

**作用与语义：**

返回用于渲染物品背景的画笔。

### `Qt::CheckState QTableWidgetItem::checkState() const`

**作用与语义：**

返回表格项的检查状态。

### `[virtual] QTableWidgetItem *QTableWidgetItem::clone() const`

**作用与语义：**

创建该物品的副本。

### `int QTableWidgetItem::column() const`

**作用与语义：**

返回表中项的列。如果项不在表中，该函数返回 -1。

### `[virtual] QVariant QTableWidgetItem::data(int role) const`

**作用与语义：**

返回给定`role`的物品数据。

### `Qt::ItemFlags QTableWidgetItem::flags() const`

**作用与语义：**

返回用于描述该项目的标志。这些标志决定该项目是否可以被检查、编辑和选择。

### `QFont QTableWidgetItem::font() const`

**作用与语义：**

返回用于渲染该物品文本的字体。

### `QBrush QTableWidgetItem::foreground() const`

**作用与语义：**

返回用于渲染物品前景（例如文本）的画笔。

### `QIcon QTableWidgetItem::icon() const`

**作用与语义：**

返回物品图标。

### `bool QTableWidgetItem::isSelected() const`

**作用与语义：**

如果选中了该物品，返回`true`，否则返回`false`。

### `[virtual] void QTableWidgetItem::read(QDataStream &in)`

**作用与语义：**

读取直播`in`的物品。

### `int QTableWidgetItem::row() const`

**作用与语义：**

返回表中该项的行。如果该项不在表中，该函数返回 -1。

### `void QTableWidgetItem::setBackground(const QBrush &brush)`

**作用与语义：**

将物品的背景画笔设置为指定的`brush`。设置默认构造画笔会让视图使用样式中的默认颜色。

### `void QTableWidgetItem::setCheckState(Qt::CheckState state)`

**作用与语义：**

将表项的检查状态设置为`state`。

### `[virtual] void QTableWidgetItem::setData(int role, const QVariant &value)`

**作用与语义：**

将该物品在给定`role`中的数据设置为指定的`value`。
注意：默认实现将`Qt::EditRole`和`Qt::DisplayRole`视为指代相同的数据。

### `void QTableWidgetItem::setFlags(Qt::ItemFlags flags)`

**作用与语义：**

将该物品的标志设置为给定的`flags`。这些标志决定了该物品是否可以被选择或修改。

### `void QTableWidgetItem::setFont(const QFont &font)`

**作用与语义：**

设置用于显示物品文本的字体为给定的`font`。

### `void QTableWidgetItem::setForeground(const QBrush &brush)`

**作用与语义：**

将物品的前景画笔设置为指定的`brush`。设置默认构造画笔会让视图使用样式中的默认颜色。

### `void QTableWidgetItem::setIcon(const QIcon &icon)`

**作用与语义：**

将物品图标设置为指定的 `icon`。

### `void QTableWidgetItem::setSelected(bool select)`

**作用与语义：**

将选中的状态设置为`select`。

### `void QTableWidgetItem::setSizeHint(const QSize &size)`

**作用与语义：**

设置表项的大小提示为`size`。如果未设置大小提示或`size`无效，项代理将根据项数据计算大小提示。

### `void QTableWidgetItem::setStatusTip(const QString &statusTip)`

**作用与语义：**

将表格项目的状态提示设置为`statusTip`指定的文本。`QTableWidget`鼠标追踪功能需要启用才能使此功能正常工作。

### `void QTableWidgetItem::setText(const QString &text)`

**作用与语义：**

将物品文本设置为指定的`text`。

### `[since 6.4] void QTableWidgetItem::setTextAlignment(Qt::Alignment alignment)`

**作用与语义：**

将该项目文本的文本对齐设置为指定的`alignment`。

### `void QTableWidgetItem::setToolTip(const QString &toolTip)`

**作用与语义：**

将物品的工具提示设置为`toolTip`指定的字符串。

### `void QTableWidgetItem::setWhatsThis(const QString &whatsThis)`

**作用与语义：**

将物品的“这是什么？”帮助设置为`whatsThis`指定的字符串。

### `QSize QTableWidgetItem::sizeHint() const`

**作用与语义：**

返回该桌面物品的尺寸提示设置。

### `QString QTableWidgetItem::statusTip() const`

**作用与语义：**

返回该物品的状态提示。

### `QTableWidget *QTableWidgetItem::tableWidget() const`

**作用与语义：**

返回包含该项的表小部件。

### `QString QTableWidgetItem::text() const`

**作用与语义：**

返回商品的文本。

### `int QTableWidgetItem::textAlignment() const`

**作用与语义：**

返回该项文本的文本对齐。
注意：出于历史原因，该函数返回一个智力。将在第7问答中修正为返回`Qt::Alignment`。

### `QString QTableWidgetItem::toolTip() const`

**作用与语义：**

返回物品的工具提示。

### `int QTableWidgetItem::type() const`

**作用与语义：**

返回传递给`QTableWidgetItem`构造器的类型。

### `QString QTableWidgetItem::whatsThis() const`

**作用与语义：**

还给物品的“这是什么？”帮助。

### `[virtual] void QTableWidgetItem::write(QDataStream &out) const`

**作用与语义：**

写入该项目以流`out`。

### `[virtual] bool QTableWidgetItem::operator<(const QTableWidgetItem &other) const`

**作用与语义：**

如果该项小于`other`项，则返回`true`;否则返回false。

### `QTableWidgetItem &QTableWidgetItem::operator=(const QTableWidgetItem &other)`

**作用与语义：**

将`other`的数据和标志分配给该项。注意`type()`和`tableWidget()`不会被复制。
该函数在重新实现`clone()`时非常有用。

### `QDataStream &operator<<(QDataStream &out, const QTableWidgetItem &item)`

**作用与语义：**

写入表控件的项目`item`流式`out`。
该操作员使用`QTableWidgetItem::write()`。

### `QDataStream &operator>>(QDataStream &in, QTableWidgetItem &item)`

**作用与语义：**

将 stream `in` 中的表格控件项目读取到 `item`。
该操作员使用`QTableWidgetItem::read()`。

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

`QTableWidgetItem` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
