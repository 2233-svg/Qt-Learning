# QGraphicsLinearLayout

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QGraphicsLinearLayout` 是 布局管理机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QGraphicsLinearLayout` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QGraphicsLinearLayout>`
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

- `QGraphicsLinearLayout(QGraphicsLayoutItem *parent = nullptr)`
- `QGraphicsLinearLayout(Qt::Orientation orientation, QGraphicsLayoutItem *parent = nullptr)`
- `virtual ~QGraphicsLinearLayout()`
- `void addItem(QGraphicsLayoutItem *item)`
- `void addStretch(int stretch = 1)`
- `Qt::Alignment alignment(QGraphicsLayoutItem *item) const`
- `void insertItem(int index, QGraphicsLayoutItem *item)`
- `void insertStretch(int index, int stretch = 1)`
- `qreal itemSpacing(int index) const`
- `Qt::Orientation orientation() const`
- `void removeItem(QGraphicsLayoutItem *item)`
- `void setAlignment(QGraphicsLayoutItem *item, Qt::Alignment alignment)`
- `void setItemSpacing(int index, qreal spacing)`
- `void setOrientation(Qt::Orientation orientation)`
- `void setSpacing(qreal spacing)`
- `void setStretchFactor(QGraphicsLayoutItem *item, int stretch)`
- `qreal spacing() const`
- `int stretchFactor(QGraphicsLayoutItem *item) const`

### 重实现的公有函数

- `virtual int count() const override`
- `virtual void invalidate() override`
- `virtual QGraphicsLayoutItem * itemAt(int index) const override`
- `virtual void removeAt(int index) override`
- `virtual void setGeometry(const QRectF &rect) override`
- `virtual QSizeF sizeHint(Qt::SizeHint which, const QSizeF &constraint = QSizeF()) const override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QGraphicsLinearLayout::QGraphicsLinearLayout(QGraphicsLayoutItem *parent = nullptr)`

**作用与语义：**

用`Qt::Horizontal`方向构造一个QGraphicsLinearLayout实例。`parent`传递给`QGraphicsLayout`的构造函数。

### `QGraphicsLinearLayout::QGraphicsLinearLayout(Qt::Orientation orientation, QGraphicsLayoutItem *parent = nullptr)`

**作用与语义：**

构建一个QGraphicsLinearLayout实例。你可以传递布局的横向或竖向`orientation`，然后`parent`传递给`QGraphicsLayout`的构造器。

### `[virtual noexcept] QGraphicsLinearLayout::~QGraphicsLinearLayout()`

**作用与语义：**

摧毁`QGraphicsLinearLayout`物体。

### `void QGraphicsLinearLayout::addItem(QGraphicsLayoutItem *item)`

**作用与语义：**

该便利函数等价于调用 `insertItem`（-1， `item`）。

### `void QGraphicsLinearLayout::addStretch(int stretch = 1)`

**作用与语义：**

该便利函数等价于调用 `insertStretch`（-1， `stretch`）。

### `Qt::Alignment QGraphicsLinearLayout::alignment(QGraphicsLayoutItem *item) const`

**作用与语义：**

返回`item`的比对。默认比对是`Qt::AlignTop` |`Qt::AlignLeft`。
对齐决定了当布局空间超过小部件能占用时，物品在分配空间内的位置。

### `[override virtual] int QGraphicsLinearLayout::count() const`

**作用与语义：**

重装：`QGraphicsLayout::count()` const.
这个纯虚拟函数必须在`QGraphicsLayout`子类中重新实现，以返回布局中的项目数量。
子职业可以自由决定如何存放这些物品。

### `void QGraphicsLinearLayout::insertItem(int index, QGraphicsLayoutItem *item)`

**作用与语义：**

在布局中插入`item`，位于`index`，或当前处于`index`的任何物品之前。

### `void QGraphicsLinearLayout::insertStretch(int index, int stretch = 1)`

**作用与语义：**

在`index`或当前`index`的物品之前插入一段`stretch`。

### `[override virtual] void QGraphicsLinearLayout::invalidate()`

**作用与语义：**

重装：`QGraphicsLayout::invalidate()`。
清除布局中缓存的几何体和大小提示信息，并将`LayoutRequest`事件发布到受管理的父`QGraphicsLayoutItem`。

### `[override virtual] QGraphicsLayoutItem *QGraphicsLinearLayout::itemAt(int index) const`

**作用与语义：**

重实现自：`QGraphicsLayout::itemAt`（int i） const.
当从0开始迭代时，它会按可视化顺序返回这些项目。
该纯虚拟函数必须在 `QGraphicsLayout` 的子类中重新实现，以返回索引 `i` 的指针。重构可以假设 `i` 有效（即尊重 `count()` 的值）。与 `count()` 一起，它作为迭代布局中所有项的方式提供。
子类可以自由决定如何存储这些物品，视觉排列也不必通过该函数来体现。

### `qreal QGraphicsLinearLayout::itemSpacing(int index) const`

**作用与语义：**

在`index`时还原物品后方的间距。

### `Qt::Orientation QGraphicsLinearLayout::orientation() const`

**作用与语义：**

返回布局方向。

### `[override virtual] void QGraphicsLinearLayout::removeAt(int index)`

**作用与语义：**

重实现自：`QGraphicsLayout::removeAt`（整数索引）。
在`index`移除物品但不销毁物品。物品的所有权转移给调用者。
该纯虚拟函数必须在`QGraphicsLayout`的子类中重构以移除`index`处的项。重构可以假设`index`有效（即尊重`count()`值）。
实现必须确保被移除项的`parentLayoutItem()`不指向该布局，因为该项被视为已从布局层级中移除。
如果布局需要在不同应用程序间重复使用，我们建议布局删除该项目，但图形视图框架不依赖于此。
子职业可以自由决定如何存放这些物品。

### `void QGraphicsLinearLayout::removeItem(QGraphicsLayoutItem *item)`

**作用与语义：**

在不破坏布局的情况下移除`item`。`item`的所有权转移给调用者。

### `void QGraphicsLinearLayout::setAlignment(QGraphicsLayoutItem *item, Qt::Alignment alignment)`

**作用与语义：**

将`item`的对齐设置为`alignment`。如果`item`的对齐发生变化，该布局会自动失效。

### `[override virtual] void QGraphicsLinearLayout::setGeometry(const QRectF &rect)`

**作用与语义：**

重装：`QGraphicsLayoutItem::setGeometry`（const QRectF & rect）。
该虚拟函数将`QGraphicsLayoutItem`的几何体设置为 `rect`，即父坐标（例如，`rect` 的左上角等价于该物品在父坐标中的位置）。
你必须在`QGraphicsLayoutItem`的子类中重新实现该函数以接收几何更新。布局在进行重排时会调用该函数。
如果`rect`超出`minimumSize`和`maximumSize`的范围，则会调整到最接近的尺寸，使其在法律范围内。

### `void QGraphicsLinearLayout::setItemSpacing(int index, qreal spacing)`

**作用与语义：**

将物品后面的间距设为`index`到`spacing`。

### `void QGraphicsLinearLayout::setOrientation(Qt::Orientation orientation)`

**作用与语义：**

将布局方向改为`orientation`。更改布局方向会自动使布局失效。

### `void QGraphicsLinearLayout::setSpacing(qreal spacing)`

**作用与语义：**

将布局间距设置为`spacing`。间距指的是物品之间的垂直和水平距离。

### `void QGraphicsLinearLayout::setStretchFactor(QGraphicsLayoutItem *item, int stretch)`

**作用与语义：**

将`item`的拉伸因子设置为`stretch`。如果某个项目的拉伸因子发生变化，该函数将使布局失效。
将`stretch`设为0会移除物品的拉伸因子，实际上相当于将`stretch`设为1。

### `[override virtual] QSizeF QGraphicsLinearLayout::sizeHint(Qt::SizeHint which, const QSizeF &constraint = QSizeF()) const`

**作用与语义：**

重实现自：`QGraphicsLayoutItem::sizeHint`（Qt：：SizeHint which， const QSizeF & constraint） const.
该纯虚拟函数返回`QGraphicsLayoutItem` `which`的大小提示，利用`constraint`的宽度或高度来约束输出。
在`QGraphicsLayoutItem`的一个子类中重新实现这个函数，以提供物品所需的尺寸提示。

### `qreal QGraphicsLinearLayout::spacing() const`

**作用与语义：**

返回布局的间距。间距指的是物品之间的垂直和水平距离。

### `int QGraphicsLinearLayout::stretchFactor(QGraphicsLayoutItem *item) const`

**作用与语义：**

返回`item`的拉伸因子。默认的拉伸因子为0，意味着该物品没有分配的拉伸因子。

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

`QGraphicsLinearLayout` 所属机制类型：布局管理机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
