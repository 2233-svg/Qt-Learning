# QGridLayout

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QGridLayout` 是 布局管理机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QGridLayout` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QGridLayout>`
- 继承自：QLayout
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

### 属性

- `horizontalSpacing : int`
- `verticalSpacing : int`

### 公有函数

- `QGridLayout(QWidget *parent = nullptr)`
- `virtual ~QGridLayout()`
- `void addItem(QLayoutItem *item, int row, int column, int rowSpan = 1, int columnSpan = 1, Qt::Alignment alignment = Qt::Alignment())`
- `void addLayout(QLayout *layout, int row, int column, Qt::Alignment alignment = Qt::Alignment())`
- `void addLayout(QLayout *layout, int row, int column, int rowSpan, int columnSpan, Qt::Alignment alignment = Qt::Alignment())`
- `void addWidget(QWidget *widget, int row, int column, Qt::Alignment alignment = Qt::Alignment())`
- `void addWidget(QWidget *widget, int fromRow, int fromColumn, int rowSpan, int columnSpan, Qt::Alignment alignment = Qt::Alignment())`
- `QRect cellRect(int row, int column) const`
- `int columnCount() const`
- `int columnMinimumWidth(int column) const`
- `int columnStretch(int column) const`
- `void getItemPosition(int index, int *row, int *column, int *rowSpan, int *columnSpan) const`
- `int horizontalSpacing() const`
- `QLayoutItem * itemAtPosition(int row, int column) const`
- `Qt::Corner originCorner() const`
- `int rowCount() const`
- `int rowMinimumHeight(int row) const`
- `int rowStretch(int row) const`
- `void setColumnMinimumWidth(int column, int minSize)`
- `void setColumnStretch(int column, int stretch)`
- `void setHorizontalSpacing(int spacing)`
- `void setOriginCorner(Qt::Corner corner)`
- `void setRowMinimumHeight(int row, int minSize)`
- `void setRowStretch(int row, int stretch)`
- `void setVerticalSpacing(int spacing)`
- `int verticalSpacing() const`

### 重实现的公有函数

- `virtual int count() const override`
- `virtual Qt::Orientations expandingDirections() const override`
- `virtual bool hasHeightForWidth() const override`
- `virtual int heightForWidth(int w) const override`
- `virtual void invalidate() override`
- `virtual QLayoutItem * itemAt(int index) const override`
- `virtual QSize maximumSize() const override`
- `virtual int minimumHeightForWidth(int w) const override`
- `virtual QSize minimumSize() const override`
- `virtual void setGeometry(const QRect &rect) override`
- `virtual void setSpacing(int spacing) override`
- `virtual QSize sizeHint() const override`
- `virtual int spacing() const override`
- `virtual QLayoutItem * takeAt(int index) override`

### 重实现的保护函数

- `virtual void addItem(QLayoutItem *item) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `horizontalSpacing : int`

**作用与语义：**

该属性决定了并排排列的元件之间的间距。
如果没有明确设置值，布局的水平间距将继承自父布局或父控件的样式设置。

**如何使用：** 调用 `horizontalSpacing()` 读取当前值；它不会修改应用状态。

### `verticalSpacing : int`

**作用与语义：**

该属性表示了叠加的控件之间的间距。
如果没有明确设置值，布局的垂直间距将继承自父布局或父控件的样式设置。

**如何使用：** 调用 `verticalSpacing()` 读取当前值；它不会修改应用状态。

### `[explicit] QGridLayout::QGridLayout(QWidget *parent = nullptr)`

**作用与语义：**

构建一个带有父控件 `parent` 的新 QGridLayout。该布局初始有一行一列，插入新项时会展开。
布局直接设置为`parent`的顶层布局。一个小部件只能有一个顶层布局。它由`QWidget::layout()`返回。
如果`parent` `nullptr`，你必须将这个网格布局插入另一个布局，或者用`QWidget::setLayout()`将其设置为小部件的布局。

### `[virtual noexcept] QGridLayout::~QGridLayout()`

**作用与语义：**

破坏网格布局。如果是顶层网格，几何管理会终止。
布局中的控件没有被破坏。

### `[override virtual protected] void QGridLayout::addItem(QLayoutItem *item)`

**作用与语义：**

重实现自：`QLayout::addItem`（QLayoutItem *item）。
在子职业中实现以添加`item`。添加方式因子职业而异。
该函数通常不会在应用代码中调用。要向布局添加小部件，使用`addWidget()`函数;要添加子布局，使用相关`QLayout`子类提供的addLayout()函数。
注意：`item`的所有权转移到了布局上，删除它由布局负责。

### `void QGridLayout::addItem(QLayoutItem *item, int row, int column, int rowSpan = 1, int columnSpan = 1, Qt::Alignment alignment = Qt::Alignment())`

**作用与语义：**

在位置`row`、`column`处添加`item`，跨越`rowSpan`行和`columnSpan`列，并根据`alignment`对齐。如果`rowSpan`和/或`columnSpan`为-1，则该项将分别延伸至底部和/或右边。布局负责`item`的所有权。
警告：请勿使用此功能添加子布局或子控件项。请使用`addLayout()`或`addWidget()`。

### `void QGridLayout::addLayout(QLayout *layout, int row, int column, Qt::Alignment alignment = Qt::Alignment())`

**作用与语义：**

将`layout`放置在网格中的位置（`row`，`column`）。左上角的位置是（0,0）。
对齐由`alignment`指定。默认对齐为0，意味着小部件填满整个单元格。
非零对齐表示布局不应膨胀以填满可用空间，而是应根据`sizeHint()`进行尺寸调整。
`layout`成为网格布局的子体。

### `void QGridLayout::addLayout(QLayout *layout, int row, int column, int rowSpan, int columnSpan, Qt::Alignment alignment = Qt::Alignment())`

**作用与语义：**

该版本将布局`layout`添加到单元格网格中，跨越多行/多列。单元格从`row`开始，且`column`跨越`rowSpan`行和`columnSpan`列。
如果`rowSpan`和/或`columnSpan`为-1，则布局将分别延伸到底部和/或右边。

### `void QGridLayout::addWidget(QWidget *widget, int row, int column, Qt::Alignment alignment = Qt::Alignment())`

**作用与语义：**

将给定的`widget`添加到格子网格中，`row`， `column`。左上角的位置默认为 （0， 0）。
对齐由`alignment`指定。默认对齐为0，意味着小部件填满整个单元格。

### `void QGridLayout::addWidget(QWidget *widget, int fromRow, int fromColumn, int rowSpan, int columnSpan, Qt::Alignment alignment = Qt::Alignment())`

**作用与语义：**

该版本将给定的`widget`添加到单元格网格中，跨越多行/多列。单元格从`fromRow`开始，且跨`fromColumn`行`rowSpan`行和`columnSpan`列。`widget`将拥有给定的`alignment`。
如果`rowSpan`和/或`columnSpan`为-1，那么小部件将分别延伸到底部和/或右边。

### `QRect QGridLayout::cellRect(int row, int column) const`

**作用与语义：**

返回网格中行为`row`、列为`column`的单元格几何形状。如果`row`或`column`位于网格之外，则返回无效矩形。
警告：在当前版本的 Qt 中，该函数在调用 `setGeometry()` 之前不会返回有效结果，即在`parentWidget()`可见之后。

### `int QGridLayout::columnCount() const`

**作用与语义：**

返回该网格中的列数。

### `int QGridLayout::columnMinimumWidth(int column) const`

**作用与语义：**

返回第`column`列的列间距。

### `int QGridLayout::columnStretch(int column) const`

**作用与语义：**

返回第4列的拉伸因子`column`。

### `[override virtual] int QGridLayout::count() const`

**作用与语义：**

重装：`QLayout::count()` const.
必须在子类中实现，以返回布局中的物品数量。

### `[override virtual] Qt::Orientations QGridLayout::expandingDirections() const`

**作用与语义：**

重装：`QLayout::expandingDirections()` const.

### `void QGridLayout::getItemPosition(int index, int *row, int *column, int *rowSpan, int *columnSpan) const`

**作用与语义：**

返回带有给定`index`的物品位置信息。
作为`row`和`column`传递的变量会根据该项目在布局中的位置更新，`rowSpan`和`columnSpan`变量则根据该项目的垂直和水平跨度更新。

### `[override virtual] bool QGridLayout::hasHeightForWidth() const`

**作用与语义：**

重装：`QLayoutItem::hasHeightForWidth()` const.
如果该布局的首选高度取决于宽度，则返回`true`;否则返回`false`。默认实现返回false。
在支持宽度高度的布局管理器中重新实现这个功能。

### `[override virtual] int QGridLayout::heightForWidth(int w) const`

**作用与语义：**

重装：`QLayoutItem::heightForWidth`（int） const.
返回该布局项的首选高度，基于宽度，但默认实现中未使用宽度。
默认实现返回 -1，表示首选高度与项目宽度无关。使用函数 `hasHeightForWidth()` 通常比调用该函数并测试 -1 快得多。
在支持宽度高度的布局管理器中重新实现该函数。典型的实现如下：
强烈建议缓存;没有缓存，布局将耗费指数级时间。

### `[override virtual] void QGridLayout::invalidate()`

**作用与语义：**

重装：`QLayout::invalidate()`。

### `[override virtual] QLayoutItem *QGridLayout::itemAt(int index) const`

**作用与语义：**

重实现自：`QLayout::itemAt`（int index）const.
必须在子类中实现以返回`index`的布局项。如果没有这样的项，函数必须返回`nullptr`。项编号从0依次排列。如果一个项被删除，其他项将被重新编号。
该函数可用于遍历布局。以下代码将为小部件布局结构中的每个布局项绘制一个矩形。

### `QLayoutItem *QGridLayout::itemAtPosition(int row, int column) const`

**作用与语义：**

返回占用单元格的布局项（`row`，`column`），如果单元格为空则返回`nullptr`。

### `[override virtual] QSize QGridLayout::maximumSize() const`

**作用与语义：**

重装：`QLayout::maximumSize()` const.

### `[override virtual] int QGridLayout::minimumHeightForWidth(int w) const`

**作用与语义：**

重实现自：`QLayoutItem::minimumHeightForWidth`（内性 w） const.
返回该控件在给定宽度下所需的最小高度，`w`。默认实现则返回 `heightForWidth`（`w`）。

### `[override virtual] QSize QGridLayout::minimumSize() const`

**作用与语义：**

重装：`QLayout::minimumSize()` const.

### `Qt::Corner QGridLayout::originCorner() const`

**作用与语义：**

返回用于网格原点的角，即位置（0， 0）。

### `int QGridLayout::rowCount() const`

**作用与语义：**

返回该网格中的行数。

### `int QGridLayout::rowMinimumHeight(int row) const`

**作用与语义：**

返回第`row`行设置的最小宽度。

### `int QGridLayout::rowStretch(int row) const`

**作用与语义：**

返回第`row`行的拉伸因子。

### `void QGridLayout::setColumnMinimumWidth(int column, int minSize)`

**作用与语义：**

将列`column`的最小宽度设置为`minSize`像素。

### `void QGridLayout::setColumnStretch(int column, int stretch)`

**作用与语义：**

将第`column`列的拉伸因子设为`stretch`。第一列为0。
拉伸因子相对于该网格中的其他列。拉伸因子较高的列占据更多可用空间。
默认的拉伸因子为0。如果拉伸因子为0且表中其他列无法增长，该列仍可能增长。
另一种方法是用带`QSpacerItem`的`addItem()`增加间距。

### `[override virtual] void QGridLayout::setGeometry(const QRect &rect)`

**作用与语义：**

重装：`QLayout::setGeometry`（const QRect & r）。

### `void QGridLayout::setOriginCorner(Qt::Corner corner)`

**作用与语义：**

将网格的原点角，即位置（0， 0）设置为`corner`。

### `void QGridLayout::setRowMinimumHeight(int row, int minSize)`

**作用与语义：**

将`row`行的最小高度设置为`minSize`像素。

### `void QGridLayout::setRowStretch(int row, int stretch)`

**作用与语义：**

将第`row`行的拉伸因子设置为`stretch`。第一行为0。
拉伸因子相对于该网格中其他行的比例。拉伸因子较高的行占据的可用空间更多。
默认的拉伸因子为0。如果拉伸因子为0且表中其他行无法增长，该行仍可能增长。

### `[override virtual] void QGridLayout::setSpacing(int spacing)`

**作用与语义：**

重新实现了属性的访问函数：`QLayout::spacing`。
该函数将垂直和水平间距设置为`spacing`。

### `[override virtual] QSize QGridLayout::sizeHint() const`

**作用与语义：**

重装：`QLayoutItem::sizeHint()` const.
在子类中实现，以返回该物品的首选大小。

### `[override virtual] int QGridLayout::spacing() const`

**作用与语义：**

重新实现了属性的访问函数：`QLayout::spacing`。
如果垂直间距等于水平间距，该函数返回该值;否则返回-1。

### `[override virtual] QLayoutItem *QGridLayout::takeAt(int index)`

**作用与语义：**

重实现自：`QLayout::takeAt`（整数索引）。
必须在子类中实现，以从布局中移除`index`的布局项并返回该项。如果没有这样的项，函数必须什么都不做，返回0。项编号从0开始依次编号。如果一个项被移除，其他项将被重新编号。
以下代码片段展示了一种安全移除所有布局物品的方法：

### `int horizontalSpacing() const`

**作用与语义：**

该属性决定了并排排列的元件之间的间距。
如果没有明确设置值，布局的水平间距将继承自父布局或父控件的样式设置。

**如何使用：** 调用 `horizontalSpacing()` 读取当前值；它不会修改应用状态。

### `void setHorizontalSpacing(int spacing)`

**作用与语义：**

该属性决定了并排排列的元件之间的间距。
如果没有明确设置值，布局的水平间距将继承自父布局或父控件的样式设置。

**如何使用：** 调用 `setHorizontalSpacing(...)` 修改 `horizontalSpacing`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setVerticalSpacing(int spacing)`

**作用与语义：**

该属性表示了叠加的控件之间的间距。
如果没有明确设置值，布局的垂直间距将继承自父布局或父控件的样式设置。

**如何使用：** 调用 `setVerticalSpacing(...)` 修改 `verticalSpacing`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `int verticalSpacing() const`

**作用与语义：**

该属性表示了叠加的控件之间的间距。
如果没有明确设置值，布局的垂直间距将继承自父布局或父控件的样式设置。

**如何使用：** 调用 `verticalSpacing()` 读取当前值；它不会修改应用状态。

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

`QGridLayout` 所属机制类型：布局管理机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
