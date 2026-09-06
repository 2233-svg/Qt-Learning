# QGraphicsAnchorLayout

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QGraphicsAnchorLayout` 是 布局管理机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QGraphicsAnchorLayout` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QGraphicsAnchorLayout>`
- 继承自：QGraphicsLayout
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

**生命周期：** 顶层布局可以在构造时绑定到 QWidget，也可以通过 `setLayout()` 安装；嵌套布局加入父布局后所有权交给父布局。布局析构不会自动销毁普通 QWidget，动态移除项目时要分别处理控件、子布局和 spacer。

**状态与结果：** 布局的项目索引会随着 add、insert、remove 和 takeAt 改变；索引既包括控件，也包括子布局、固定空白和 stretch。修改项目或尺寸参数后 Qt 会使布局失效并重新计算。

**线程与事件循环：** 布局只应在 GUI 线程操作，因为它直接改变 QWidget 几何和可见界面。布局系统不负责业务线程同步，也不会把手动的跨线程控件访问变安全。

## 3. 直接使用

需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。 使用时通常按这个过程组织：创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QGraphicsAnchorLayout(QGraphicsLayoutItem *parent = nullptr)`
- `virtual ~QGraphicsAnchorLayout()`
- `QGraphicsAnchor * addAnchor(QGraphicsLayoutItem *firstItem, Qt::AnchorPoint firstEdge, QGraphicsLayoutItem *secondItem, Qt::AnchorPoint secondEdge)`
- `void addAnchors(QGraphicsLayoutItem *firstItem, QGraphicsLayoutItem *secondItem, Qt::Orientations orientations = Qt::Horizontal | Qt::Vertical)`
- `void addCornerAnchors(QGraphicsLayoutItem *firstItem, Qt::Corner firstCorner, QGraphicsLayoutItem *secondItem, Qt::Corner secondCorner)`
- `QGraphicsAnchor * anchor(QGraphicsLayoutItem *firstItem, Qt::AnchorPoint firstEdge, QGraphicsLayoutItem *secondItem, Qt::AnchorPoint secondEdge)`
- `qreal horizontalSpacing() const`
- `void setHorizontalSpacing(qreal spacing)`
- `void setSpacing(qreal spacing)`
- `void setVerticalSpacing(qreal spacing)`
- `qreal verticalSpacing() const`

### 重实现的公有函数

- `virtual int count() const override`
- `virtual void invalidate() override`
- `virtual QGraphicsLayoutItem * itemAt(int index) const override`
- `virtual void removeAt(int index) override`
- `virtual void setGeometry(const QRectF &geom) override`

### 重实现的保护函数

- `virtual QSizeF sizeHint(Qt::SizeHint which, const QSizeF &constraint = QSizeF()) const override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QGraphicsAnchorLayout::QGraphicsAnchorLayout(QGraphicsLayoutItem *parent = nullptr)`

**作用与语义：**

构造一个QGraphicsAnchorLayout实例。`parent`传递给`QGraphicsLayout`的构造器。

### `[virtual noexcept] QGraphicsAnchorLayout::~QGraphicsAnchorLayout()`

**作用与语义：**

摧毁`QGraphicsAnchorLayout`物体。

### `QGraphicsAnchor *QGraphicsAnchorLayout::addAnchor(QGraphicsLayoutItem *firstItem, Qt::AnchorPoint firstEdge, QGraphicsLayoutItem *secondItem, Qt::AnchorPoint secondEdge)`

**作用与语义：**

在物品`firstItem`的边`firstEdge`和物品`secondItem`的边缘`secondEdge`之间创建一个锚点。锚点的间距从样式中取用。布局边和物品边缘之间的锚点大小为0。如果边界之间已有锚点，新的锚点将取代旧的。
如果`firstItem`和`secondItem`不属于布局，它们会自动添加到布局中。这意味着`count()`最多可以增加2。
锚点的间距取决于锚的类型。例如，从一个物品的右边到另一个物品的左边（或反之）锚点将使用默认的水平间距。同样的行为也适用于从底部到顶部的锚点，但它们会使用默认的垂直间距。对于所有其他锚点组合，间距为0。所有锚定函数都遵循此规则。
间距也可以通过`QGraphicsAnchor::setSpacing()`方法手动设置。
调用该函数，其中`firstItem`或`secondItem`是布局的祖先，则行为未定义。

### `void QGraphicsAnchorLayout::addAnchors(QGraphicsLayoutItem *firstItem, QGraphicsLayoutItem *secondItem, Qt::Orientations orientations = Qt::Horizontal | Qt::Vertical)`

**作用与语义：**

将`firstItem`的两条或四条边锚定为对应的`secondItem`边，使`firstItem`在`orientations`指定的维度内与`secondItem`大小相同。
例如，以下示例将两个物体的左右边锚定为其宽度：
这也可以通过以下代码行实现：

**官方示例：**

```cpp
 layout->addAnchor(b, Qt::AnchorLeft, c, Qt::AnchorLeft);
 layout->addAnchor(b, Qt::AnchorRight, c, Qt::AnchorRight);
```

### `void QGraphicsAnchorLayout::addCornerAnchors(QGraphicsLayoutItem *firstItem, Qt::Corner firstCorner, QGraphicsLayoutItem *secondItem, Qt::Corner secondCorner)`

**作用与语义：**

在`firstItem`和`secondItem`之间创建两个锚点，分别由角点`firstCorner`和`secondCorner`，一个用于水平边，另一个用于垂直边。
这是一个方便函数，因为锚定角可以表示为锚定两条边。例如：
这也可以通过以下代码行实现：
如果边对之间已经存在锚点，则该锚点将被该函数指定的锚点所替代。
如果`firstItem`和`secondItem`不属于布局，它们会自动添加到布局中。这意味着`count()`最多可以增加2个。

**官方示例：**

```cpp
 layout->addAnchor(a, Qt::AnchorTop, layout, Qt::AnchorTop);
 layout->addAnchor(a, Qt::AnchorLeft, layout, Qt::AnchorLeft);
```

### `QGraphicsAnchor *QGraphicsAnchorLayout::anchor(QGraphicsLayoutItem *firstItem, Qt::AnchorPoint firstEdge, QGraphicsLayoutItem *secondItem, Qt::AnchorPoint secondEdge)`

**作用与语义：**

返回由`firstItem`和`firstEdge`以及`secondItem`和`secondEdge`定义的锚点之间的锚点。如果没有这样的锚点，函数返回0。

### `[override virtual] int QGraphicsAnchorLayout::count() const`

**作用与语义：**

重装：`QGraphicsLayout::count()` const.
这个纯虚拟函数必须在`QGraphicsLayout`子类中重新实现，以返回布局中的项目数量。
子职业可以自由决定如何存放这些物品。

### `qreal QGraphicsAnchorLayout::horizontalSpacing() const`

**作用与语义：**

返回锚点布局的默认水平间距。

### `[override virtual] void QGraphicsAnchorLayout::invalidate()`

**作用与语义：**

重装：`QGraphicsLayout::invalidate()`。
清除布局中缓存的几何体和大小提示信息，并将`LayoutRequest`事件发布到受管理的父`QGraphicsLayoutItem`。

### `[override virtual] QGraphicsLayoutItem *QGraphicsAnchorLayout::itemAt(int index) const`

**作用与语义：**

重实现自：`QGraphicsLayout::itemAt`（int i） const.
这个纯虚拟函数必须在`QGraphicsLayout`的子类中重新实现，以返回索引`i`的项的指针。重构可以假设`i`有效（即尊重`count()`的值）。与`count()`一起，它作为迭代布局中所有项的方式提供。
子类可以自由决定如何存储这些物品，视觉排列也不必通过该函数来体现。

### `[override virtual] void QGraphicsAnchorLayout::removeAt(int index)`

**作用与语义：**

重实现自：`QGraphicsLayout::removeAt`（整数索引）。
在`index`移除布局物品而不破坏它。物品的所有权转移给调用者。
移除物品也会移除与之相关的锚点。
必须在`QGraphicsLayout`的子类中重构该项，以移除`index`的项。重构可以假设`index`有效（即尊重`count()`的值）。
实现必须确保被移除项的`parentLayoutItem()`不指向该布局，因为该项被视为已从布局层级中移除。
如果布局需要在不同应用程序间重复使用，我们建议布局删除该项目，但图形视图框架不依赖于此。
子职业可以自由决定如何存放这些物品。

### `[override virtual] void QGraphicsAnchorLayout::setGeometry(const QRectF &geom)`

**作用与语义：**

重装：`QGraphicsLayoutItem::setGeometry`（const QRectF & rect）。
该虚拟函数将`QGraphicsLayoutItem`的几何体设置为 `rect`，即父坐标（例如，`rect` 的左上角等价于该物品在父坐标中的位置）。
你必须在`QGraphicsLayoutItem`的子类中重新实现该函数以接收几何更新。布局在进行重排时会调用该函数。
如果`rect`超出`minimumSize`和`maximumSize`的范围，则会调整到最接近的尺寸，使其在法律范围内。

### `void QGraphicsAnchorLayout::setHorizontalSpacing(qreal spacing)`

**作用与语义：**

将锚点布局的默认水平间距设置为`spacing`。

### `void QGraphicsAnchorLayout::setSpacing(qreal spacing)`

**作用与语义：**

将锚点布局的默认水平和默认垂直间距设置为`spacing`。
如果一个物品锚定时没有与锚点关联的间距，则会使用默认的间距。
`QGraphicsAnchorLayout`不支持负距。设置负值会取消之前的间距，使布局使用当前控件样式提供的间距。

### `void QGraphicsAnchorLayout::setVerticalSpacing(qreal spacing)`

**作用与语义：**

将锚点布局的默认垂直间距设置为`spacing`。

### `[override virtual protected] QSizeF QGraphicsAnchorLayout::sizeHint(Qt::SizeHint which, const QSizeF &constraint = QSizeF()) const`

**作用与语义：**

重实现自：`QGraphicsLayoutItem::sizeHint`（Qt：：SizeHint which， const QSizeF & constraint） const.
该纯虚拟函数返回`QGraphicsLayoutItem` `which`的大小提示，利用`constraint`的宽度或高度来约束输出。
在`QGraphicsLayoutItem`的一个子类中重新实现这个函数，以提供物品所需的尺寸提示。

### `qreal QGraphicsAnchorLayout::verticalSpacing() const`

**作用与语义：**

返回锚点布局的默认垂直间距。

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

`QGraphicsAnchorLayout` 所属机制类型：布局管理机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
