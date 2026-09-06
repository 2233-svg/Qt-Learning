# QListWidgetItem

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QListWidgetItem` 是 Qt 容器类型，负责保存一组元素，并提供插入、删除、查找、遍历和容量管理。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QListWidgetItem` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QListWidgetItem>`
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

**生命周期：** 容器自己管理元素存储，容器销毁后由它提供的迭代器、引用和 data 指针通常失效。修改容器可能重新分配或 detach，不能把元素地址和迭代器当成长期句柄。

**状态与结果：** 要区分空容器、容量、元素数量、查找失败和默认构造值。插入/删除可能改变索引和迭代器；关联容器还要考虑键唯一性、排序和查找复杂度。

**线程与事件循环：** 不同线程使用各自的容器副本通常安全；同一个容器一边读一边写仍需要同步，即使底层采用隐式共享也不会自动解决数据竞争。

## 3. 直接使用

需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。 使用时通常按这个过程组织：创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

```cpp
#include <QList>

QList<int> values{1, 2, 3};
values.append(4);
for (const int value : values) {
    // 使用 value
}
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum ItemType { Type, UserType }`

### 公有函数

- `QListWidgetItem(QListWidget *parent = nullptr, int type = Type)`
- `QListWidgetItem(const QString &text, QListWidget *parent = nullptr, int type = Type)`
- `QListWidgetItem(const QIcon &icon, const QString &text, QListWidget *parent = nullptr, int type = Type)`
- `QListWidgetItem(const QListWidgetItem &other)`
- `virtual ~QListWidgetItem()`
- `QBrush background() const`
- `Qt::CheckState checkState() const`
- `virtual QListWidgetItem * clone() const`
- `virtual QVariant data(int role) const`
- `Qt::ItemFlags flags() const`
- `QFont font() const`
- `QBrush foreground() const`
- `QIcon icon() const`
- `bool isHidden() const`
- `bool isSelected() const`
- `QListWidget * listWidget() const`
- `virtual void read(QDataStream &in)`
- `void setBackground(const QBrush &brush)`
- `void setCheckState(Qt::CheckState state)`
- `virtual void setData(int role, const QVariant &value)`
- `void setFlags(Qt::ItemFlags flags)`
- `void setFont(const QFont &font)`
- `void setForeground(const QBrush &brush)`
- `void setHidden(bool hide)`
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
- `QString text() const`
- `int textAlignment() const`
- `QString toolTip() const`
- `int type() const`
- `QString whatsThis() const`
- `virtual void write(QDataStream &out) const`
- `virtual bool operator<(const QListWidgetItem &other) const`
- `QListWidgetItem & operator=(const QListWidgetItem &other)`

### 相关非成员函数

- `QDataStream & operator<<(QDataStream &out, const QListWidgetItem &item)`
- `QDataStream & operator>>(QDataStream &in, QListWidgetItem &item)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QListWidgetItem::ItemType`

**作用与语义：**

该枚举描述了用于描述列表控件项的类型。
- `QListWidgetItem::Type`：`0`;列表小部件项的默认类型。
- `QListWidgetItem::UserType`：`1000`;自定义类型的最小值。低于 UserType 的值由 Qt 保留。
你可以在`QListWidgetItem`子类中定义新的用户类型，以确保自定义项目被特别对待。

### `[explicit] QListWidgetItem::QListWidgetItem(QListWidget *parent = nullptr, int type = Type)`

**作用与语义：**

用指定`parent`构造一个指定`type`的空列表控件项。如果未指定`parent`，则需要将该项插入带有`QListWidget::insertItem()`的列表控件中。
该构造器将该项插入到传给构造函数的父模型中。如果模型被排序，插入的行为是未确定的，因为模型会调用`'<'`算子方法，而此时尚未构造完成的项目。为避免未确定行为，我们建议不指定父节点，而使用`QListWidget::insertItem()`。

### `[explicit] QListWidgetItem::QListWidgetItem(const QString &text, QListWidget *parent = nullptr, int type = Type)`

**作用与语义：**

构造指定`type`的空列表控件项，使用给定的`text`和`parent`。如果未指定父节点，则需要将该项插入带有`QListWidget::insertItem()`的列表控件中。
该构造器将该项插入到传给构造器的父模型中。如果模型已排序，插入的行为未确定，因为模型会调用`'<'`算符方法，而此时尚未构造完成的。为避免未确定行为，我们建议不指定父节点，而使用`QListWidget::insertItem()`。

### `[explicit] QListWidgetItem::QListWidgetItem(const QIcon &icon, const QString &text, QListWidget *parent = nullptr, int type = Type)`

**作用与语义：**

构造指定`type`的空列表控件，使用给定的`icon`、`text`和`parent`。如果未指定父节点，则需要将该项插入带有`QListWidget::insertItem()`的列表控件中。
该构造器将该项插入传给构造函数的父模型中。如果模型被排序，插入的行为将未确定，因为模型会调用`'<'`算符方法，而此时尚未构造的项目。为避免未确定行为，我们建议不指定父节点，而使用`QListWidget::insertItem()`。

### `QListWidgetItem::QListWidgetItem(const QListWidgetItem &other)`

**作用与语义：**

构造`other`的副本。注意`type()`和`listWidget()`不被复制。
该函数在重新实现`clone()`时非常有用。

### `[virtual noexcept] QListWidgetItem::~QListWidgetItem()`

**作用与语义：**

销毁列表项目。

### `QBrush QListWidgetItem::background() const`

**作用与语义：**

返回用于显示列表项目背景的画笔。

### `Qt::CheckState QListWidgetItem::checkState() const`

**作用与语义：**

返回列表项的已检查状态（见 `Qt::CheckState`）。

### `[virtual] QListWidgetItem *QListWidgetItem::clone() const`

**作用与语义：**

创建该物品的精确复制品。

### `[virtual] QVariant QListWidgetItem::data(int role) const`

**作用与语义：**

返回给定`role`的物品数据。如果你需要额外角色或特殊行为，可以重新实现这个函数。

### `Qt::ItemFlags QListWidgetItem::flags() const`

**作用与语义：**

返回该物品的物品标志（见 `Qt::ItemFlags`）。

### `QFont QListWidgetItem::font() const`

**作用与语义：**

返回用于显示该列表条目文本的字体。

### `QBrush QListWidgetItem::foreground() const`

**作用与语义：**

返回用于显示列表项目前景（例如文本）的画刷。

### `QIcon QListWidgetItem::icon() const`

**作用与语义：**

返回列表项的图标。

### `bool QListWidgetItem::isHidden() const`

**作用与语义：**

如果物品被隐藏，返回`true`;否则返回`false`。

### `bool QListWidgetItem::isSelected() const`

**作用与语义：**

如果选中了该物品，返回`true`;否则返回`false`。

### `QListWidget *QListWidgetItem::listWidget() const`

**作用与语义：**

返回包含该项的列表控件。

### `[virtual] void QListWidgetItem::read(QDataStream &in)`

**作用与语义：**

读取直播`in`的物品。

### `void QListWidgetItem::setBackground(const QBrush &brush)`

**作用与语义：**

将列表项的背景画笔设置为给定的 `brush`。设置默认构造画笔会让视图使用样式中的默认颜色。

### `void QListWidgetItem::setCheckState(Qt::CheckState state)`

**作用与语义：**

将列表项的检查状态设置为`state`。

### `[virtual] void QListWidgetItem::setData(int role, const QVariant &value)`

**作用与语义：**

将给定`role`的数据设置为给定的`value`。如果你需要额外角色或特定角色的特殊行为，可以重新实现这个函数。
注意：默认实现中`Qt::EditRole`和 `Qt::DisplayRole` 视为相同的数据。

### `void QListWidgetItem::setFlags(Qt::ItemFlags flags)`

**作用与语义：**

将列表项目的物品标志设置为`flags`。

### `void QListWidgetItem::setFont(const QFont &font)`

**作用与语义：**

设置涂装时使用的字体为给定的`font`。

### `void QListWidgetItem::setForeground(const QBrush &brush)`

**作用与语义：**

将列表项目的前景画笔设置为给定的`brush`。设置默认构造画笔会让视图使用样式中的默认颜色。

### `void QListWidgetItem::setHidden(bool hide)`

**作用与语义：**

如果`hide`为真，则隐藏该物品;否则显示该物品。

### `void QListWidgetItem::setIcon(const QIcon &icon)`

**作用与语义：**

将列表项的图标设置为给定的`icon`。

### `void QListWidgetItem::setSelected(bool select)`

**作用与语义：**

将选中的状态设置为`select`。

### `void QListWidgetItem::setSizeHint(const QSize &size)`

**作用与语义：**

设置列表项的大小提示为`size`。如果未设置大小提示或`size`无效，项代理将根据项数据计算大小提示。

### `void QListWidgetItem::setStatusTip(const QString &statusTip)`

**作用与语义：**

将列表项目的状态提示设置为`statusTip`指定的文本。`QListWidget`鼠标追踪功能需要启用才能使此功能正常工作。

### `void QListWidgetItem::setText(const QString &text)`

**作用与语义：**

将列表控件项的文本设置为给定的 `text`。

### `[since 6.4] void QListWidgetItem::setTextAlignment(Qt::Alignment alignment)`

**作用与语义：**

将列表项的文本对齐设置为`alignment`。

### `void QListWidgetItem::setToolTip(const QString &toolTip)`

**作用与语义：**

将列表项的工具提示设置为`toolTip`指定的文本。

### `void QListWidgetItem::setWhatsThis(const QString &whatsThis)`

**作用与语义：**

将列表项目的“这是什么？”帮助设置为`whatsThis`指定的文本。

### `QSize QListWidgetItem::sizeHint() const`

**作用与语义：**

返回列表项的大小提示设置。

### `QString QListWidgetItem::statusTip() const`

**作用与语义：**

返回列表项的状态提示。

### `QString QListWidgetItem::text() const`

**作用与语义：**

返回列表项的文本。

### `int QListWidgetItem::textAlignment() const`

**作用与语义：**

返回列表项的文本对齐。
注意：该函数返回一个int，出于历史原因。在Qt 7中将被修正为返回`Qt::Alignment`。

### `QString QListWidgetItem::toolTip() const`

**作用与语义：**

返回列表项的工具提示。

### `int QListWidgetItem::type() const`

**作用与语义：**

返回传递给`QListWidgetItem`构造器的类型。

### `QString QListWidgetItem::whatsThis() const`

**作用与语义：**

返回列表项目的“这是什么？”帮助文本。

### `[virtual] void QListWidgetItem::write(QDataStream &out) const`

**作用与语义：**

写入该项目以流`out`。

### `[virtual] bool QListWidgetItem::operator<(const QListWidgetItem &other) const`

**作用与语义：**

如果该项的文本少于`other`项的文本，返回`true`;否则返回`false`。

### `QListWidgetItem &QListWidgetItem::operator=(const QListWidgetItem &other)`

**作用与语义：**

将`other`的数据和标志分配给该项。注意`type()`和`listWidget()`不会被复制。
该函数在重新实现`clone()`时非常有用。

### `QDataStream &operator<<(QDataStream &out, const QListWidgetItem &item)`

**作用与语义：**

写入列表控件项`item`以流`out`。
该操作员使用`QListWidgetItem::write()`。

### `QDataStream &operator>>(QDataStream &in, QListWidgetItem &item)`

**作用与语义：**

将 stream `in` 中的列表控件项读取到 `item`。
该操作员使用`QListWidgetItem::read()`。

## 6. 深入实践与常见坑

### 生命周期和资源边界

容器自己管理元素存储，容器销毁后由它提供的迭代器、引用和 data 指针通常失效。修改容器可能重新分配或 detach，不能把元素地址和迭代器当成长期句柄。

### 状态和错误边界

要区分空容器、容量、元素数量、查找失败和默认构造值。插入/删除可能改变索引和迭代器；关联容器还要考虑键唯一性、排序和查找复杂度。

### 线程边界

不同线程使用各自的容器副本通常安全；同一个容器一边读一边写仍需要同步，即使底层采用隐式共享也不会自动解决数据竞争。

### 最容易出现的错误

优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QListWidgetItem` 所属机制类型：Qt 容器与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
