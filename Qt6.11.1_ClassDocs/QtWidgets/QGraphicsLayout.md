# QGraphicsLayout

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QGraphicsLayout` 是 布局管理机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QGraphicsLayout` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QGraphicsLayout>`
- 继承自：QGraphicsLayoutItem
- 直接派生类：QGraphicsAnchorLayout、QGraphicsGridLayout,、QGraphicsLinearLayout

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

### 状态、生命周期和线程

**生命周期：** 顶层布局可以在构造时绑定到 QWidget，也可以通过 `setLayout()` 安装；嵌套布局加入父布局后所有权交给父布局。布局析构不会自动销毁普通 QWidget，动态移除项目时要分别处理控件、子布局和 spacer。

**状态与结果：** 布局的项目索引会随着 add、insert、remove 和 takeAt 改变；索引既包括控件，也包括子布局、固定空白和 stretch。修改项目或尺寸参数后 Qt 会使布局失效并重新计算。

**线程与事件循环：** 布局只应在 GUI 线程操作，因为它直接改变 QWidget 几何和可见界面。布局系统不负责业务线程同步，也不会把手动的跨线程控件访问变安全。

## 3. 直接使用

需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。 使用时通常按这个过程组织：创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QGraphicsLayout(QGraphicsLayoutItem *parent = nullptr)`
- `virtual ~QGraphicsLayout()`
- `void activate()`
- `virtual int count() const = 0`
- `virtual void invalidate()`
- `bool isActivated() const`
- `virtual QGraphicsLayoutItem * itemAt(int i) const = 0`
- `virtual void removeAt(int index) = 0`
- `void setContentsMargins(qreal left, qreal top, qreal right, qreal bottom)`
- `virtual void widgetEvent(QEvent *e)`

### 重实现的公有函数

- `virtual void getContentsMargins(qreal *left, qreal *top, qreal *right, qreal *bottom) const override`
- `virtual void updateGeometry() override`

### 保护函数

- `void addChildLayoutItem(QGraphicsLayoutItem *layoutItem)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QGraphicsLayout::QGraphicsLayout(QGraphicsLayoutItem *parent = nullptr)`

**作用与语义：**

构建一个QGraphicsLayout对象。
`parent` 传递给 `QGraphicsLayoutItem` 的构造函数，`QGraphicsLayoutItem` 的 isLayout 参数设为 true。
如果`parent`是`QGraphicsWidget`，布局会安装在该小部件上。（注意安装布局会删除旧的配置。）。

### `[virtual noexcept] QGraphicsLayout::~QGraphicsLayout()`

**作用与语义：**

摧毁`QGraphicsLayout`物体。

### `void QGraphicsLayout::activate()`

**作用与语义：**

激活布局，使布局中的所有物品立即重新排列。该功能基于调用`count()`和`itemAt()`，然后依次调用所有物品的 `setGeometry()`。激活后，布局将调整其几何体以符合父`contentsRect()`。父布局随后会使自身任何布局失效。
如果按顺序或递归方式调用，例如被调整大小的某个排列项调用，该函数将不做任何事。
请注意，该布局可免费使用几何缓存来优化此过程。要强制使任何此类缓存失效，可以在调用 activate() 之前调用 `invalidate()`。

### `[protected] void QGraphicsLayout::addChildLayoutItem(QGraphicsLayoutItem *layoutItem)`

**作用与语义：**

该功能是为自定义布局提供的便利功能，会浏览布局中的所有项目，并将其图形项目重新父级到布局最接近的`QGraphicsWidget`祖先。
如果`layoutItem`已经在不同的布局中，它将被从该布局中移除。
如果自定义布局需要特殊行为，可以忽略该函数，实现自己的行为。

### `[pure virtual] int QGraphicsLayout::count() const`

**作用与语义：**

这个纯虚拟函数必须在`QGraphicsLayout`子类中重新实现，以返回布局中的项目数量。
子职业可以自由决定如何存放这些物品。

### `[override virtual] void QGraphicsLayout::getContentsMargins(qreal *left, qreal *top, qreal *right, qreal *bottom) const`

**作用与语义：**

重实现自：`QGraphicsLayoutItem::getContentsMargins`（qreal *左，qreal *top，qreal *right，qreal *bottom）const.
该虚拟函数为该`QGraphicsLayoutItem`提供`left`、`top`、`right`和`bottom`内容边距。默认实现假设所有目录余距均为0。参数指向存储在qreal中的值。如果任何指针被`nullptr`，该值不会被更新。

### `[virtual] void QGraphicsLayout::invalidate()`

**作用与语义：**

清除布局中缓存的几何体和尺寸提示信息，并将`LayoutRequest`事件发布到受管理的父`QGraphicsLayoutItem`。

### `bool QGraphicsLayout::isActivated() const`

**作用与语义：**

如果布局正在激活，返回`true`;否则返回`false`。如果布局正在激活，意味着它正在重新排列其项（即`activate()`函数已被调用，尚未返回）。

### `[pure virtual] QGraphicsLayoutItem *QGraphicsLayout::itemAt(int i) const`

**作用与语义：**

该纯虚拟函数必须在`QGraphicsLayout`的子类中重新实现，以返回索引`i`的项的指针。重构可以假设`i`有效（即尊重`count()`的值）。与`count()`一起，它作为迭代布局中所有项的方式提供。
子类可以自由决定如何存储这些物品，视觉排列也不必通过该函数来体现。

### `[pure virtual] void QGraphicsLayout::removeAt(int index)`

**作用与语义：**

该纯虚拟函数必须在`QGraphicsLayout`的子类中重新实现以移除`index`处的项。重实现可以假设`index`有效（即尊重`count()`值）。
实现必须确保被移除项的`parentLayoutItem()`不指向该布局，因为该项被视为已从布局层级中移除。
如果布局需要在不同应用程序间重复使用，我们建议布局删除该项目，但图形视图框架不依赖于此。
子职业可以自由决定如何存放这些物品。

### `void QGraphicsLayout::setContentsMargins(qreal left, qreal top, qreal right, qreal bottom)`

**作用与语义：**

将内容边距设置为`left`、`top`、`right`和`bottom`。顶层布局的默认内容边距取决于样式（通过查询pixelMetric中的`QStyle::PM_LayoutLeftMargin`、`QStyle::PM_LayoutTopMargin`、`QStyle::PM_LayoutRightMargin`和`QStyle::PM_LayoutBottomMargin`）。
子版面的默认边距是0。
更改目录边注会自动使布局失效。

### `[override virtual] void QGraphicsLayout::updateGeometry()`

**作用与语义：**

重装：`QGraphicsLayoutItem::updateGeometry()`。
这个虚拟函数会丢弃任何缓存的大小提示信息。如果你更改了`sizeHint()`函数的返回值，你应该始终调用这个函数。子类在重新实现该函数时必须始终调用基础实现。

### `[virtual] void QGraphicsLayout::widgetEvent(QEvent *e)`

**作用与语义：**

该虚拟事件处理程序接收管理组件的所有事件。`QGraphicsLayout`使用该事件处理程序监听与布局相关的事件，如几何变化、布局变化或布局方向变化。
`e`是事件的一个指示。
你可以重新实现这个事件处理程序，以跟踪类似事件，适用于你自己的自定义布局。

## 6. 深入实践与常见坑

### 生命周期和资源边界

顶层布局可以在构造时绑定到 QWidget，也可以通过 `setLayout()` 安装；嵌套布局加入父布局后所有权交给父布局。布局析构不会自动销毁普通 QWidget，动态移除项目时要分别处理控件、子布局和 spacer。

### 状态和错误边界

布局的项目索引会随着 add、insert、remove 和 takeAt 改变；索引既包括控件，也包括子布局、固定空白和 stretch。修改项目或尺寸参数后 Qt 会使布局失效并重新计算。

### 线程边界

布局只应在 GUI 线程操作，因为它直接改变 QWidget 几何和可见界面。布局系统不负责业务线程同步，也不会把手动的跨线程控件访问变安全。

### 最容易出现的错误

优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QGraphicsLayout` 所属机制类型：布局管理机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
