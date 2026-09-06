# QGraphicsLayoutItem

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QGraphicsLayoutItem` 是 图形场景与项目机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QGraphicsLayoutItem` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QGraphicsLayoutItem>`
- 继承自：未在类页中列出
- 直接派生类：QGraphicsLayout、QGraphicsWidget

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

### 状态、生命周期和线程

**生命周期：** 场景或父项目通常管理子项目，但视图只是观察者，不一定拥有场景。删除项目、改变父项目或切换场景时要确认索引、指针、选中状态和布局关系是否仍有效。

**状态与结果：** 区分局部坐标、场景坐标、视图/窗口坐标，区分选中、悬停、焦点、可见和碰撞状态。改变几何、变换或数据后通常请求更新，而不是手动强制调用绘制函数。

**线程与事件循环：** 图形对象通常只能在其所属 GUI/场景线程操作；后台线程负责数据准备，结果通过信号投递后再更新场景对象。

## 3. 直接使用

需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。 使用时通常按这个过程组织：创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QGraphicsLayoutItem(QGraphicsLayoutItem *parent = nullptr, bool isLayout = false)`
- `virtual ~QGraphicsLayoutItem()`
- `QRectF contentsRect() const`
- `QSizeF effectiveSizeHint(Qt::SizeHint which, const QSizeF &constraint = QSizeF()) const`
- `QRectF geometry() const`
- `virtual void getContentsMargins(qreal *left, qreal *top, qreal *right, qreal *bottom) const`
- `QGraphicsItem * graphicsItem() const`
- `(since 6.0) virtual bool isEmpty() const`
- `bool isLayout() const`
- `qreal maximumHeight() const`
- `QSizeF maximumSize() const`
- `qreal maximumWidth() const`
- `qreal minimumHeight() const`
- `QSizeF minimumSize() const`
- `qreal minimumWidth() const`
- `bool ownedByLayout() const`
- `QGraphicsLayoutItem * parentLayoutItem() const`
- `qreal preferredHeight() const`
- `QSizeF preferredSize() const`
- `qreal preferredWidth() const`
- `virtual void setGeometry(const QRectF &rect)`
- `void setMaximumHeight(qreal height)`
- `void setMaximumSize(const QSizeF &size)`
- `void setMaximumSize(qreal w, qreal h)`
- `void setMaximumWidth(qreal width)`
- `void setMinimumHeight(qreal height)`
- `void setMinimumSize(const QSizeF &size)`
- `void setMinimumSize(qreal w, qreal h)`
- `void setMinimumWidth(qreal width)`
- `void setParentLayoutItem(QGraphicsLayoutItem *parent)`
- `void setPreferredHeight(qreal height)`
- `void setPreferredSize(const QSizeF &size)`
- `void setPreferredSize(qreal w, qreal h)`
- `void setPreferredWidth(qreal width)`
- `void setSizePolicy(const QSizePolicy &policy)`
- `void setSizePolicy(QSizePolicy::Policy hPolicy, QSizePolicy::Policy vPolicy, QSizePolicy::ControlType controlType = QSizePolicy::DefaultType)`
- `QSizePolicy sizePolicy() const`
- `virtual void updateGeometry()`

### 保护函数

- `void setGraphicsItem(QGraphicsItem *item)`
- `void setOwnedByLayout(bool ownership)`
- `virtual QSizeF sizeHint(Qt::SizeHint which, const QSizeF &constraint = QSizeF()) const = 0`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QGraphicsLayoutItem::QGraphicsLayoutItem(QGraphicsLayoutItem *parent = nullptr, bool isLayout = false)`

**作用与语义：**

构造 QGraphicsLayoutItem 对象。`parent` 成为该对象的父对象。如果 `isLayout` 为真，则该项为 layout，否则 `isLayout` 为假。

### `[virtual noexcept] QGraphicsLayoutItem::~QGraphicsLayoutItem()`

**作用与语义：**

摧毁`QGraphicsLayoutItem`物体。

### `QRectF QGraphicsLayoutItem::contentsRect() const`

**作用与语义：**

返回本地坐标中的内容。
contents rect 定义了相关布局在排列子项时所使用的子矩形。该函数是一个便利功能，通过内容边距调整物品的 `geometry()`。注意 `getContentsMargins()` 是一个虚拟函数，你可以重新实现以返回物品的内容页余。

### `QSizeF QGraphicsLayoutItem::effectiveSizeHint(Qt::SizeHint which, const QSizeF &constraint = QSizeF()) const`

**作用与语义：**

返回该`QGraphicsLayoutItem`的有效尺寸提示。
`which` 就是所涉及的大小提示。`constraint` 是一个可选参数，在计算有效大小提示时定义了一个特殊的约束。默认情况下，`constraint` 是 `QSizeF`（-1， -1），这意味着大小提示没有约束。
如果你想指定小部件的尺寸提示，可以`constraint`提供固定尺寸。这对只能垂直或水平增长的小部件很有用，需要将宽度或高度设置为特殊值。
例如，一个文本段落项如果能放入200列宽度内，可能会垂直增长。你可以通过`QSizeF`（200， -1）作为约束，以获得合适的最小、首选和最大高度）。
你可以通过在`QGraphicsLayoutItem`子类中重新实现`sizeHint()`，或者调用以下函数之一来调整有效大小提示：`setMinimumSize()`、`setPreferredSize`或`setMaximumSize()`（或两者的组合）。
该函数缓存每个大小提示，并保证每个`which`值`sizeHint()`仅调用一次——除非未指定`constraint`且已调用`updateGeometry()`。

### `QRectF QGraphicsLayoutItem::geometry() const`

**作用与语义：**

返回该项目的几何形状（例如位置和大小）作为`QRectF`。该函数等价于 `QRectF`（pos()， size()）。

### `[virtual] void QGraphicsLayoutItem::getContentsMargins(qreal *left, qreal *top, qreal *right, qreal *bottom) const`

**作用与语义：**

该虚拟函数为该`QGraphicsLayoutItem`提供`left`、`top`、`right`和`bottom`内容边距。默认实现假设所有内容边距均为0。参数指向存储在qreal中的值。如果任何指针被`nullptr`，该值不会更新。

### `QGraphicsItem *QGraphicsLayoutItem::graphicsItem() const`

**作用与语义：**

返回该布局项所代表的`QGraphicsItem`。对于`QGraphicsWidget`，它会返回自身。对于自定义物品，它可以返回汇总后的值。

### `[virtual, since 6.0] bool QGraphicsLayoutItem::isEmpty() const`

**作用与语义：**

如果该项目为空，也就是说它是否没有内容且不应占用任何空间，返回`true`。
默认实现如果该项被隐藏，`true`返回为真，除非其大小策略将 retainSizeWhenHidden 设置为 `true`。

### `bool QGraphicsLayoutItem::isLayout() const`

**作用与语义：**

如果该`QGraphicsLayoutItem`是布局（例如，被一个对象继承，该对象排列其他`QGraphicsLayoutItem`对象），返回`true`;否则返回`false`。

### `qreal QGraphicsLayoutItem::maximumHeight() const`

**作用与语义：**

返回最大高度。

### `QSizeF QGraphicsLayoutItem::maximumSize() const`

**作用与语义：**

返回最大尺寸。

### `qreal QGraphicsLayoutItem::maximumWidth() const`

**作用与语义：**

返回最大宽度。

### `qreal QGraphicsLayoutItem::minimumHeight() const`

**作用与语义：**

返回最低高度。

### `QSizeF QGraphicsLayoutItem::minimumSize() const`

**作用与语义：**

退回最小尺寸。

### `qreal QGraphicsLayoutItem::minimumWidth() const`

**作用与语义：**

返回最小宽度。

### `bool QGraphicsLayoutItem::ownedByLayout() const`

**作用与语义：**

返回布局是否应该在其结构函数中删除该项。如果为真，则布局会删除它。如果为假，则假设有其他对象拥有该项的所有权，布局不会删除该项。
如果该物品同时继承了`QGraphicsItem`和 `QGraphicsLayoutItem`（如`QGraphicsWidget`所做），那么该物品实际上属于两个所有权层级。该属性决定了布局在销毁时应如何处理其子项目。对于`QGraphicsWidget`而言，更倾向于在删除布局时不要删除其子项（因为它们也是图形项层级的一部分）。
默认情况下，该值在`QGraphicsLayoutItem`中初始化为false，但`QGraphicsLayout`覆盖以返回true。这是因为`QGraphicsLayout`通常不属于`QGraphicsItem`层级，因此父布局应将其删除。子类可以通过调用`setOwnedByLayout`（true）来覆盖该默认行为。

### `QGraphicsLayoutItem *QGraphicsLayoutItem::parentLayoutItem() const`

**作用与语义：**

返回该`QGraphicsLayoutItem`的父，若无父类或父级未继承`QGraphicsLayoutItem`则返回`nullptr`（`QGraphicsLayoutItem`常通过多重继承与`QObject`派生类使用）。

### `qreal QGraphicsLayoutItem::preferredHeight() const`

**作用与语义：**

返回首选高度。

### `QSizeF QGraphicsLayoutItem::preferredSize() const`

**作用与语义：**

退回首选尺寸。

### `qreal QGraphicsLayoutItem::preferredWidth() const`

**作用与语义：**

返回首选宽度。

### `[virtual] void QGraphicsLayoutItem::setGeometry(const QRectF &rect)`

**作用与语义：**

该虚函数将`QGraphicsLayoutItem`的几何形状设置为`rect`，即父坐标（例如，`rect`的左上角等价于该物品在父坐标中的位置）。
你必须在`QGraphicsLayoutItem`的子类中重新实现这个函数，才能接收几何更新。布局在进行重排时会调用这个函数。
如果`rect`超出`minimumSize`和`maximumSize`的范围，则会调整到最接近的尺寸，使其在法律范围内。

### `[protected] void QGraphicsLayoutItem::setGraphicsItem(QGraphicsItem *item)`

**作用与语义：**

如果`QGraphicsLayoutItem`代表`QGraphicsItem`，并且想利用`QGraphicsLayout`的自动重父功能，应该设置这个值。注意，如果你删除`item`但不删除布局项，你需要调用setGraphicsItem（`nullptr`），以避免出现悬挂指针。

### `void QGraphicsLayoutItem::setMaximumHeight(qreal height)`

**作用与语义：**

将最大高度设置为`height`。

### `void QGraphicsLayoutItem::setMaximumSize(const QSizeF &size)`

**作用与语义：**

将最大大小设置为`size`。该属性覆盖`Qt::MaximumSize`的`sizeHint()`，并确保`effectiveSizeHint()`永远不会返回大于`size`的大小。要解除最大大小，请使用无效大小。

### `void QGraphicsLayoutItem::setMaximumSize(qreal w, qreal h)`

**作用与语义：**

这个便捷函数等同于调用 setMaximumSize(`QSizeF`(`w`, `h`))。

### `void QGraphicsLayoutItem::setMaximumWidth(qreal width)`

**作用与语义：**

将最大宽度设置为`width`。

### `void QGraphicsLayoutItem::setMinimumHeight(qreal height)`

**作用与语义：**

将最低高度设置为`height`。

### `void QGraphicsLayoutItem::setMinimumSize(const QSizeF &size)`

**作用与语义：**

将最小大小设置为`size`。该属性覆盖`sizeHint()` `Qt::MinimumSize`，并确保`effectiveSizeHint()`永远不会返回小于`size`的大小。为了解除最小大小，请使用无效大小。

### `void QGraphicsLayoutItem::setMinimumSize(qreal w, qreal h)`

**作用与语义：**

这个便捷函数等同于调用 setMinimumSize(`QSizeF`(`w`, `h`))。

### `void QGraphicsLayoutItem::setMinimumWidth(qreal width)`

**作用与语义：**

将最小宽度设置为`width`。

### `[protected] void QGraphicsLayoutItem::setOwnedByLayout(bool ownership)`

**作用与语义：**

设置布局是否应该在其结构器中删除该项。`ownership`必须为真，布局才能删除它。

### `void QGraphicsLayoutItem::setParentLayoutItem(QGraphicsLayoutItem *parent)`

**作用与语义：**

将该`QGraphicsLayoutItem`的父节点设置为`parent`。

### `void QGraphicsLayoutItem::setPreferredHeight(qreal height)`

**作用与语义：**

将首选高度设置为`height`。

### `void QGraphicsLayoutItem::setPreferredSize(const QSizeF &size)`

**作用与语义：**

将首选大小设置为`size`。该属性覆盖`Qt::PreferredSize`的`sizeHint()`，并提供`effectiveSizeHint()`的默认值。要取消首选大小，请使用无效大小。

### `void QGraphicsLayoutItem::setPreferredSize(qreal w, qreal h)`

**作用与语义：**

这个便捷函数等同于调用 setPreferredSize(`QSizeF`(`w`, `h`))。

### `void QGraphicsLayoutItem::setPreferredWidth(qreal width)`

**作用与语义：**

将首选宽度设置为`width`。

### `void QGraphicsLayoutItem::setSizePolicy(const QSizePolicy &policy)`

**作用与语义：**

将尺寸策略设置为`policy`。尺寸策略描述了在布局中，物品应如何横向和纵向增长。
`QGraphicsLayoutItem` 的默认大小策略是 （`QSizePolicy::Fixed`， `QSizePolicy::Fixed`， `QSizePolicy::DefaultType`），但子类通常会更改默认值。例如，`QGraphicsWidget` 默认为 （`QSizePolicy::Preferred`， `QSizePolicy::Preferred`， `QSizePolicy::DefaultType`）。

### `void QGraphicsLayoutItem::setSizePolicy(QSizePolicy::Policy hPolicy, QSizePolicy::Policy vPolicy, QSizePolicy::ControlType controlType = QSizePolicy::DefaultType)`

**作用与语义：**

该函数等同于调用 setSizePolicy（`QSizePolicy`（`hPolicy`， `vPolicy`， `controlType`））。

### `[pure virtual protected] QSizeF QGraphicsLayoutItem::sizeHint(Qt::SizeHint which, const QSizeF &constraint = QSizeF()) const`

**作用与语义：**

该纯虚拟函数返回`QGraphicsLayoutItem` `which`的大小提示，利用`constraint`的宽度或高度来约束输出。
在`QGraphicsLayoutItem`的一个子类中重新实现这个函数，以提供物品所需的尺寸提示。

### `QSizePolicy QGraphicsLayoutItem::sizePolicy() const`

**作用与语义：**

恢复当前的尺寸政策。

### `[virtual] void QGraphicsLayoutItem::updateGeometry()`

**作用与语义：**

该虚拟函数会丢弃任何缓存大小提示信息。如果你更改了`sizeHint()`函数的返回值，应始终调用该函数。子类在重新实现该函数时必须始终调用基础实现。

## 6. 深入实践与常见坑

### 生命周期和资源边界

场景或父项目通常管理子项目，但视图只是观察者，不一定拥有场景。删除项目、改变父项目或切换场景时要确认索引、指针、选中状态和布局关系是否仍有效。

### 状态和错误边界

区分局部坐标、场景坐标、视图/窗口坐标，区分选中、悬停、焦点、可见和碰撞状态。改变几何、变换或数据后通常请求更新，而不是手动强制调用绘制函数。

### 线程边界

图形对象通常只能在其所属 GUI/场景线程操作；后台线程负责数据准备，结果通过信号投递后再更新场景对象。

### 最容易出现的错误

优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QGraphicsLayoutItem` 所属机制类型：图形场景与项目机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
