# QGraphicsGridLayout

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QGraphicsGridLayout` 是 布局管理机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QGraphicsGridLayout` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QGraphicsGridLayout>`
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

- `QGraphicsGridLayout(QGraphicsLayoutItem *parent = nullptr)`
- `virtual ~QGraphicsGridLayout()`
- `void addItem(QGraphicsLayoutItem *item, int row, int column, Qt::Alignment alignment = Qt::Alignment())`
- `void addItem(QGraphicsLayoutItem *item, int row, int column, int rowSpan, int columnSpan, Qt::Alignment alignment = Qt::Alignment())`
- `Qt::Alignment alignment(QGraphicsLayoutItem *item) const`
- `Qt::Alignment columnAlignment(int column) const`
- `int columnCount() const`
- `qreal columnMaximumWidth(int column) const`
- `qreal columnMinimumWidth(int column) const`
- `qreal columnPreferredWidth(int column) const`
- `qreal columnSpacing(int column) const`
- `int columnStretchFactor(int column) const`
- `qreal horizontalSpacing() const`
- `QGraphicsLayoutItem * itemAt(int row, int column) const`
- `void removeItem(QGraphicsLayoutItem *item)`
- `Qt::Alignment rowAlignment(int row) const`
- `int rowCount() const`
- `qreal rowMaximumHeight(int row) const`
- `qreal rowMinimumHeight(int row) const`
- `qreal rowPreferredHeight(int row) const`
- `qreal rowSpacing(int row) const`
- `int rowStretchFactor(int row) const`
- `void setAlignment(QGraphicsLayoutItem *item, Qt::Alignment alignment)`
- `void setColumnAlignment(int column, Qt::Alignment alignment)`
- `void setColumnFixedWidth(int column, qreal width)`
- `void setColumnMaximumWidth(int column, qreal width)`
- `void setColumnMinimumWidth(int column, qreal width)`
- `void setColumnPreferredWidth(int column, qreal width)`
- `void setColumnSpacing(int column, qreal spacing)`
- `void setColumnStretchFactor(int column, int stretch)`
- `void setHorizontalSpacing(qreal spacing)`
- `void setRowAlignment(int row, Qt::Alignment alignment)`
- `void setRowFixedHeight(int row, qreal height)`
- `void setRowMaximumHeight(int row, qreal height)`
- `void setRowMinimumHeight(int row, qreal height)`
- `void setRowPreferredHeight(int row, qreal height)`
- `void setRowSpacing(int row, qreal spacing)`
- `void setRowStretchFactor(int row, int stretch)`
- `void setSpacing(qreal spacing)`
- `void setVerticalSpacing(qreal spacing)`
- `qreal verticalSpacing() const`

### 重实现的公有函数

- `virtual int count() const override`
- `virtual void invalidate() override`
- `virtual QGraphicsLayoutItem * itemAt(int index) const override`
- `virtual void removeAt(int index) override`
- `virtual void setGeometry(const QRectF &rect) override`
- `virtual QSizeF sizeHint(Qt::SizeHint which, const QSizeF &constraint = QSizeF()) const override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QGraphicsGridLayout::QGraphicsGridLayout(QGraphicsLayoutItem *parent = nullptr)`

**作用与语义：**

构造一个QGraphicsGridLayout实例。`parent`传递给`QGraphicsLayout`的构造器。

### `[virtual noexcept] QGraphicsGridLayout::~QGraphicsGridLayout()`

**作用与语义：**

摧毁`QGraphicsGridLayout`物体。

### `void QGraphicsGridLayout::addItem(QGraphicsLayoutItem *item, int row, int column, Qt::Alignment alignment = Qt::Alignment())`

**作用与语义：**

在`row`和`column`的网格中增加`item`。你可以为`item`指定可选的`alignment`。

### `void QGraphicsGridLayout::addItem(QGraphicsLayoutItem *item, int row, int column, int rowSpan, int columnSpan, Qt::Alignment alignment = Qt::Alignment())`

**作用与语义：**

在`row`和 `column` 上给网格增加了`item`。你可以指定`rowSpan`和`columnSpan`，以及可选的`alignment`。

### `Qt::Alignment QGraphicsGridLayout::alignment(QGraphicsLayoutItem *item) const`

**作用与语义：**

返回`item`的对齐。

### `Qt::Alignment QGraphicsGridLayout::columnAlignment(int column) const`

**作用与语义：**

返回`column`的对齐。

### `int QGraphicsGridLayout::columnCount() const`

**作用与语义：**

返回网格布局中的列数。这总是比最后一列被布局项目占用的索引多一列（空列除末尾列外计入）。

### `qreal QGraphicsGridLayout::columnMaximumWidth(int column) const`

**作用与语义：**

返回`column`的最大宽度。

### `qreal QGraphicsGridLayout::columnMinimumWidth(int column) const`

**作用与语义：**

返回`column`最小宽度。

### `qreal QGraphicsGridLayout::columnPreferredWidth(int column) const`

**作用与语义：**

返回`column`的首选宽度。

### `qreal QGraphicsGridLayout::columnSpacing(int column) const`

**作用与语义：**

返回`column`列间距。

### `int QGraphicsGridLayout::columnStretchFactor(int column) const`

**作用与语义：**

`column`还原了拉伸因子。

### `[override virtual] int QGraphicsGridLayout::count() const`

**作用与语义：**

重装：`QGraphicsLayout::count()` const.
返回该网格布局中的布局项目数量。
该纯虚拟函数必须在`QGraphicsLayout`子类中重新实现，以返回布局中的项目数量。
子职业可以自由决定如何存放这些物品。

### `qreal QGraphicsGridLayout::horizontalSpacing() const`

**作用与语义：**

返回网格布局的默认水平间距。

### `[override virtual] void QGraphicsGridLayout::invalidate()`

**作用与语义：**

重装：`QGraphicsLayout::invalidate()`。
清除布局中缓存的几何体和大小提示信息，并将`LayoutRequest`事件发布到受管理的父`QGraphicsLayoutItem`。

### `[override virtual] QGraphicsLayoutItem *QGraphicsGridLayout::itemAt(int index) const`

**作用与语义：**

重实现自：`QGraphicsLayout::itemAt`（int i） const.
返回`index`的布局项，如果该索引中没有布局项，则返回`nullptr`。
该纯虚拟函数必须在 `QGraphicsLayout` 的子类中重新实现，以返回索引 `i` 的指针。重构可以假设 `i` 有效（即尊重 `count()` 的值）。与 `count()` 一起，它作为对布局中所有项进行迭代的方式提供。
子类可以自由决定如何存储这些物品，视觉排列也不必通过该函数来体现。

### `QGraphicsLayoutItem *QGraphicsGridLayout::itemAt(int row, int column) const`

**作用与语义：**

返回指向布局项（`row`， `column`）的指针。

### `[override virtual] void QGraphicsGridLayout::removeAt(int index)`

**作用与语义：**

重实现自：`QGraphicsLayout::removeAt`（整数索引）。
在`index`移除布局物品但不销毁它。物品的所有权转移给调用者。
这个纯虚拟函数必须在`QGraphicsLayout`的子类中重新实现，以移除`index`处的项。重实现可以假设`index`有效（即尊重`count()`的值）。
实现必须确保被移除项的`parentLayoutItem()`不指向该布局，因为该项被视为已从布局层级中移除。
如果布局需要在不同应用程序间重复使用，我们建议布局删除该项目，但图形视图框架不依赖于此。
子职业可以自由决定如何存放这些物品。

### `void QGraphicsGridLayout::removeItem(QGraphicsLayoutItem *item)`

**作用与语义：**

移除布局物品`item`但不破坏它。物品的所有权转移给调用者。

### `Qt::Alignment QGraphicsGridLayout::rowAlignment(int row) const`

**作用与语义：**

返回`row`的对齐。

### `int QGraphicsGridLayout::rowCount() const`

**作用与语义：**

返回网格布局中的行数。这总是比最后一行被布局项目占用的索引多一行（除末尾的空行外，所有空行都计入）。

### `qreal QGraphicsGridLayout::rowMaximumHeight(int row) const`

**作用与语义：**

返回行 `row` 的最大高度。

### `qreal QGraphicsGridLayout::rowMinimumHeight(int row) const`

**作用与语义：**

返回行的最小高度，`row`。

### `qreal QGraphicsGridLayout::rowPreferredHeight(int row) const`

**作用与语义：**

返回行的首选高度，`row`。

### `qreal QGraphicsGridLayout::rowSpacing(int row) const`

**作用与语义：**

返回行间距，换取`row`。

### `int QGraphicsGridLayout::rowStretchFactor(int row) const`

**作用与语义：**

可以恢复拉伸因子`row`。

### `void QGraphicsGridLayout::setAlignment(QGraphicsLayoutItem *item, Qt::Alignment alignment)`

**作用与语义：**

将`item`的对齐设置为`alignment`。

### `void QGraphicsGridLayout::setColumnAlignment(int column, Qt::Alignment alignment)`

**作用与语义：**

将`column`的对齐设置为`alignment`。

### `void QGraphicsGridLayout::setColumnFixedWidth(int column, qreal width)`

**作用与语义：**

将`column`的固定宽度设置为`width`。

### `void QGraphicsGridLayout::setColumnMaximumWidth(int column, qreal width)`

**作用与语义：**

将`column`的最大宽度设置为`width`。

### `void QGraphicsGridLayout::setColumnMinimumWidth(int column, qreal width)`

**作用与语义：**

设定`column`到`width`的最小宽度。

### `void QGraphicsGridLayout::setColumnPreferredWidth(int column, qreal width)`

**作用与语义：**

设置`column`的首选宽度`width`。

### `void QGraphicsGridLayout::setColumnSpacing(int column, qreal spacing)`

**作用与语义：**

把`column`间距设定为`spacing`。

### `void QGraphicsGridLayout::setColumnStretchFactor(int column, int stretch)`

**作用与语义：**

将`column`的拉伸因子设定为`stretch`。

### `[override virtual] void QGraphicsGridLayout::setGeometry(const QRectF &rect)`

**作用与语义：**

重装：`QGraphicsLayoutItem::setGeometry`（const QRectF & rect）。
将网格布局的边界几何设置为`rect`。
该虚拟函数将`QGraphicsLayoutItem`的几何形状设置为 `rect`，即父坐标（例如，`rect` 的左上角等价于该项在父坐标中的位置）。
你必须在`QGraphicsLayoutItem`的子类中重新实现该函数以接收几何更新。布局在进行重排时会调用该函数。
如果`rect`超出`minimumSize`和`maximumSize`的范围，则会调整到最接近的尺寸，使其在法律范围内。

### `void QGraphicsGridLayout::setHorizontalSpacing(qreal spacing)`

**作用与语义：**

将网格布局的默认水平间距设置为`spacing`。

### `void QGraphicsGridLayout::setRowAlignment(int row, Qt::Alignment alignment)`

**作用与语义：**

将`row`的对齐设置为`alignment`。

### `void QGraphicsGridLayout::setRowFixedHeight(int row, qreal height)`

**作用与语义：**

将行`row`的固定高度设置为`height`。

### `void QGraphicsGridLayout::setRowMaximumHeight(int row, qreal height)`

**作用与语义：**

将`row`行的最大高度设置为`height`。

### `void QGraphicsGridLayout::setRowMinimumHeight(int row, qreal height)`

**作用与语义：**

将行（`row`）的最小高度设置为`height`。

### `void QGraphicsGridLayout::setRowPreferredHeight(int row, qreal height)`

**作用与语义：**

将行`row`的首选高度设置为`height`。

### `void QGraphicsGridLayout::setRowSpacing(int row, qreal spacing)`

**作用与语义：**

将`row`间距设置为`spacing`。

### `void QGraphicsGridLayout::setRowStretchFactor(int row, int stretch)`

**作用与语义：**

将`row`的拉伸因子设定为`stretch`。

### `void QGraphicsGridLayout::setSpacing(qreal spacing)`

**作用与语义：**

将网格布局的默认间距（纵向和水平）设置为`spacing`。

### `void QGraphicsGridLayout::setVerticalSpacing(qreal spacing)`

**作用与语义：**

将网格布局的默认垂直间距设置为`spacing`。

### `[override virtual] QSizeF QGraphicsGridLayout::sizeHint(Qt::SizeHint which, const QSizeF &constraint = QSizeF()) const`

**作用与语义：**

重实现自：`QGraphicsLayoutItem::sizeHint`（Qt：：SizeHint which， const QSizeF & constraint） const.
该纯虚拟函数返回`QGraphicsLayoutItem` `which`的大小提示，利用`constraint`的宽度或高度来约束输出。
在`QGraphicsLayoutItem`的一个子类中重新实现这个函数，以提供物品所需的尺寸提示。

### `qreal QGraphicsGridLayout::verticalSpacing() const`

**作用与语义：**

返回网格布局的默认垂直间距。

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

`QGraphicsGridLayout` 所属机制类型：布局管理机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
