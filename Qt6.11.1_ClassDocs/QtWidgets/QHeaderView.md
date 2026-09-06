# QHeaderView

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QHeaderView` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QHeaderView` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QHeaderView>`
- 继承自：QAbstractItemView
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

- `enum ResizeMode { Interactive, Fixed, Stretch, ResizeToContents, Custom }`

### 属性

- `cascadingSectionResizes : bool`
- `defaultAlignment : Qt::Alignment`
- `defaultSectionSize : int`
- `firstSectionMovable : bool`
- `highlightSections : bool`
- `maximumSectionSize : int`
- `minimumSectionSize : int`
- `sectionsClickable : bool`
- `sectionsMovable : bool`
- `showSortIndicator : bool`
- `(since 6.1) sortIndicatorClearable : bool`
- `stretchLastSection : bool`

### 公有函数

- `QHeaderView(Qt::Orientation orientation, QWidget *parent = nullptr)`
- `virtual ~QHeaderView()`
- `bool cascadingSectionResizes() const`
- `int count() const`
- `Qt::Alignment defaultAlignment() const`
- `int defaultSectionSize() const`
- `int hiddenSectionCount() const`
- `void hideSection(int logicalIndex)`
- `bool highlightSections() const`
- `bool isFirstSectionMovable() const`
- `bool isSectionHidden(int logicalIndex) const`
- `bool isSortIndicatorClearable() const`
- `bool isSortIndicatorShown() const`
- `int length() const`
- `int logicalIndex(int visualIndex) const`
- `int logicalIndexAt(const QPoint &pos) const`
- `int logicalIndexAt(int position) const`
- `int logicalIndexAt(int x, int y) const`
- `int maximumSectionSize() const`
- `int minimumSectionSize() const`
- `void moveSection(int from, int to)`
- `int offset() const`
- `Qt::Orientation orientation() const`
- `void resetDefaultSectionSize()`
- `int resizeContentsPrecision() const`
- `void resizeSection(int logicalIndex, int size)`
- `void resizeSections(QHeaderView::ResizeMode mode)`
- `bool restoreState(const QByteArray &state)`
- `QByteArray saveState() const`
- `int sectionPosition(int logicalIndex) const`
- `QHeaderView::ResizeMode sectionResizeMode(int logicalIndex) const`
- `int sectionSize(int logicalIndex) const`
- `int sectionSizeHint(int logicalIndex) const`
- `int sectionViewportPosition(int logicalIndex) const`
- `bool sectionsClickable() const`
- `bool sectionsHidden() const`
- `bool sectionsMovable() const`
- `bool sectionsMoved() const`
- `void setCascadingSectionResizes(bool enable)`
- `void setDefaultAlignment(Qt::Alignment alignment)`
- `void setDefaultSectionSize(int size)`
- `void setFirstSectionMovable(bool movable)`
- `void setHighlightSections(bool highlight)`
- `void setMaximumSectionSize(int size)`
- `void setMinimumSectionSize(int size)`
- `void setResizeContentsPrecision(int precision)`
- `void setSectionHidden(int logicalIndex, bool hide)`
- `void setSectionResizeMode(QHeaderView::ResizeMode mode)`
- `void setSectionResizeMode(int logicalIndex, QHeaderView::ResizeMode mode)`
- `void setSectionsClickable(bool clickable)`
- `void setSectionsMovable(bool movable)`
- `void setSortIndicator(int logicalIndex, Qt::SortOrder order)`
- `void setSortIndicatorClearable(bool clearable)`
- `void setSortIndicatorShown(bool show)`
- `void setStretchLastSection(bool stretch)`
- `void showSection(int logicalIndex)`
- `Qt::SortOrder sortIndicatorOrder() const`
- `int sortIndicatorSection() const`
- `bool stretchLastSection() const`
- `int stretchSectionCount() const`
- `void swapSections(int first, int second)`
- `int visualIndex(int logicalIndex) const`
- `int visualIndexAt(int position) const`

### 重实现的公有函数

- `virtual void reset() override`
- `virtual void setModel(QAbstractItemModel *model) override`
- `virtual void setVisible(bool v) override`
- `virtual QSize sizeHint() const override`

### 公有槽函数

- `void headerDataChanged(Qt::Orientation orientation, int logicalFirst, int logicalLast)`
- `void setOffset(int offset)`
- `void setOffsetToLastSection()`
- `void setOffsetToSectionPosition(int visualSectionNumber)`

### 信号

- `void geometriesChanged()`
- `void sectionClicked(int logicalIndex)`
- `void sectionCountChanged(int oldCount, int newCount)`
- `void sectionDoubleClicked(int logicalIndex)`
- `void sectionEntered(int logicalIndex)`
- `void sectionHandleDoubleClicked(int logicalIndex)`
- `void sectionMoved(int logicalIndex, int oldVisualIndex, int newVisualIndex)`
- `void sectionPressed(int logicalIndex)`
- `void sectionResized(int logicalIndex, int oldSize, int newSize)`
- `void sortIndicatorChanged(int logicalIndex, Qt::SortOrder order)`
- `void sortIndicatorClearableChanged(bool clearable)`

### 保护函数

- `virtual void initStyleOption(QStyleOptionHeader *option) const`
- `(since 6.0) virtual void initStyleOptionForIndex(QStyleOptionHeader *option, int logicalIndex) const`
- `virtual void paintSection(QPainter *painter, const QRect &rect, int logicalIndex) const`
- `virtual QSize sectionSizeFromContents(int logicalIndex) const`

### 重实现的保护函数

- `virtual void currentChanged(const QModelIndex &current, const QModelIndex &old) override`
- `virtual bool event(QEvent *e) override`
- `virtual int horizontalOffset() const override`
- `virtual void mouseDoubleClickEvent(QMouseEvent *e) override`
- `virtual void mouseMoveEvent(QMouseEvent *e) override`
- `virtual void mousePressEvent(QMouseEvent *e) override`
- `virtual void mouseReleaseEvent(QMouseEvent *e) override`
- `virtual void paintEvent(QPaintEvent *e) override`
- `virtual void setSelection(const QRect &rect, QItemSelectionModel::SelectionFlags flags) override`
- `virtual int verticalOffset() const override`
- `virtual bool viewportEvent(QEvent *e) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QHeaderView::ResizeMode`

**作用与语义：**

缩小模式指定了头部部分的行为。它可以在整个头视图上设置，也可以在单个部分上使用 `setSectionResizeMode()`。
- `QHeaderView::Interactive`：`0`;用户可以调整该节大小。该节也可以通过程序方式通过`resizeSection()`进行调整大小。节大小默认为`defaultSectionSize`。（参见`cascadingSectionResizes`。）
- `QHeaderView::Fixed`：`2`;用户无法调整该部分大小。该部分只能通过程序方式通过`resizeSection()`进行调整大小。部分大小默认为`defaultSectionSize`。
- `QHeaderView::Stretch`：`1`;`QHeaderView`会自动调整该部分大小以填满可用空间。用户或程序无法更改该区域的大小。
- `QHeaderView::ResizeToContents`：`3`;`QHeaderView` 会自动根据整列或整行的内容调整截面大小至最佳大小。大小不可由用户或程序更改。（该值于 4.2 版本引入）
以下数值已过时：
- `QHeaderView::Custom`：`Fixed`;改用固定。

### `cascadingSectionResizes : bool`

**作用与语义：**

该属性决定了当用户调整的区域达到最小大小后，交互式调整大小是否会级联到后续部分。
该特性仅影响以`Interactive`为缩放模式的部分。
默认值为假。

**如何使用：** 调用 `cascadingSectionResizes()` 读取当前值；它不会修改应用状态。

### `defaultAlignment : Qt::Alignment`

**作用与语义：**

该属性表示每个头部文本的默认对齐。

**如何使用：** 调用 `defaultAlignment()` 读取当前值；它不会修改应用状态。

### `defaultSectionSize : int`

**作用与语义：**

该属性保留了缩写前头部部分的默认大小。
该特性仅影响以`Interactive`或`Fixed`为缩放模式的部分。
默认情况下，该属性的值与样式相关。因此，当样式发生变化时，该属性会从中更新。调用 setDefaultSectionSize() 会停止更新，调用 resetDefaultSectionSize() 则会恢复默认行为。

**如何使用：** 调用 `defaultSectionSize()` 读取当前值；它不会修改应用状态。

### `firstSectionMovable : bool`

**作用与语义：**

该属性决定用户是否可以移动第一列。
该属性控制用户是否可以移动第一列。在`QTreeView`中，第一列保留树结构，因此默认不可移动，即使达到`setSectionsMovable`（真）之后也是如此。
例如，在没有树结构的平面列表的情况下，可以通过调用此方法使其再次可移动。在这种情况下，建议也调用 `QTreeView::setRootIsDecorated`（false）。
设置为true没有效果，除非同时调用`setSectionsMovable`（true）。

**如何使用：** 调用 `firstSectionMovable()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 treeView->setRootIsDecorated(false);
 treeView->header()->setFirstSectionMovable(true);
```

### `highlightSections : bool`

**作用与语义：**

该属性决定是否高亮包含所选项目的章节。
默认情况下，该属性为`false`。

**如何使用：** 调用 `highlightSections()` 读取当前值；它不会修改应用状态。

### `maximumSectionSize : int`

**作用与语义：**

该属性包含了头部段的最大大小。
最大截面大小是允许的最大截面大小。该属性的默认值是1048575，这也是截面的最大可能大小。将最大值设为 -1 会将值重置为最大截面大小。
除了拉伸外，这一特性被所有缩放模式都遵守。

**如何使用：** 调用 `maximumSectionSize()` 读取当前值；它不会修改应用状态。

### `minimumSectionSize : int`

**作用与语义：**

该属性包含了头部段的最小大小。
最小节大小是允许的最小节大小。如果最小节大小设置为 -1，`QHeaderView`将使用字体度量大小。
所有缩放模式都尊重这一特性。

**如何使用：** 调用 `minimumSectionSize()` 读取当前值；它不会修改应用状态。

### `sectionsClickable : bool`

**作用与语义：**

如果头部可点击，则保持`true`;否则`false`。可点击头部可以设置，允许用户在视图中更改与头部相关的数据表示方式。

**如何使用：** 调用 `sectionsClickable()` 读取当前值；它不会修改应用状态。

### `sectionsMovable : bool`

**作用与语义：**

如果`sectionsMovable`为真，用户可以移动头部部分;否则它们会被固定在原位。
与`QTreeView`结合使用时，第一列默认不可移动（因为它包含树状结构）。你可以用`setFirstSectionMovable`（true）让它可移动。

**如何使用：** 调用 `sectionsMovable()` 读取当前值；它不会修改应用状态。

### `showSortIndicator : bool`

**作用与语义：**

该属性在排序指示器显示时成立。
默认情况下，该属性为`false`。

**如何使用：** 调用 `showSortIndicator()` 读取当前值；它不会修改应用状态。

### `[since 6.1] sortIndicatorClearable : bool`

**作用与语义：**

该属性决定排序指示器是否可以通过多次点击某一部分来清除。
该属性控制用户是否能通过多次点击该分段来移除该分段的排序指示。通常，点击某一分段只是改变该分段的排序顺序。将该属性设置为 true，排序指示器在交替升降后会被清除;这通常会恢复模型的原始排序。
将该属性设置为 true（除非 `sectionsClickable()` 也为真，否则无效（例如 `QTableView` 是某些视图的默认值，或者在使视图可排序时自动设置，例如调用 `QTreeView::setSortingEnabled`）。

**如何使用：** 调用 `sortIndicatorClearable()` 读取当前值；它不会修改应用状态。

### `stretchLastSection : bool`

**作用与语义：**

该属性是否满足头部最后可见部分是否占用所有可用空间。
默认值为假。
注意：`QTreeView`提供的水平首部配置中，此属性设置为 true，确保视图不会浪费其首部分配的空间。如果该值设为 true，该属性将覆盖头部最后一段的缩小模式。

**如何使用：** 调用 `stretchLastSection()` 读取当前值；它不会修改应用状态。

### `[explicit] QHeaderView::QHeaderView(Qt::Orientation orientation, QWidget *parent = nullptr)`

**作用与语义：**

创建一个新的通用头部，包含给定的`orientation`和`parent`。

### `[virtual noexcept] QHeaderView::~QHeaderView()`

**作用与语义：**

会毁掉头部。

### `int QHeaderView::count() const`

**作用与语义：**

返回头部中的分段数量。

### `[override virtual protected] void QHeaderView::currentChanged(const QModelIndex &current, const QModelIndex &old)`

**作用与语义：**

Reimpations： `QAbstractItemView::currentChanged`（const QModelIndex ¤t， const QModelIndex &previous）.
当新项目变成当前项目时，调用该槽位。之前的当前项目由`previous`索引指定，新项目由`current`索引指定。
如果你想知道物品的变化，请查看`dataChanged()`信号。

### `[override virtual protected] bool QHeaderView::event(QEvent *e)`

**作用与语义：**

重装：`QAbstractItemView::event`（QEvent *事件）。

### `[signal] void QHeaderView::geometriesChanged()`

**作用与语义：**

当头部几何形状发生变化时，该信号会发出。

### `[slot] void QHeaderView::headerDataChanged(Qt::Orientation orientation, int logicalFirst, int logicalLast)`

**作用与语义：**

更新更改后的头部部分，包含从`logicalFirst`到`logicalLast`包含的指定`orientation`。

### `int QHeaderView::hiddenSectionCount() const`

**作用与语义：**

返回被隐藏的头部部分数量。

### `void QHeaderView::hideSection(int logicalIndex)`

**作用与语义：**

隐藏`logicalIndex`指定的部分。

### `[override virtual protected] int QHeaderView::horizontalOffset() const`

**作用与语义：**

重装：`QAbstractItemView::horizontalOffset()` const.
返回头部的水平偏移量。垂直头部的偏移量为0。
返回视角的水平偏移。
在基类中，这是一个纯虚拟函数。

### `[virtual protected] void QHeaderView::initStyleOption(QStyleOptionHeader *option) const`

**作用与语义：**

用该 `QHeaderView` 的值初始化 `option`。该方法适用于子类需要`QStyleOptionHeader`但不想自己填写所有信息时。

### `[virtual protected, since 6.0] void QHeaderView::initStyleOptionForIndex(QStyleOptionHeader *option, int logicalIndex) const`

**作用与语义：**

初始化指定`logicalIndex`的样式`option`。该函数在调用`initStyleOption`后由默认实现调用`paintSection`。

### `bool QHeaderView::isSectionHidden(int logicalIndex) const`

**作用与语义：**

如果`logicalIndex`指定的部分对用户显式隐藏，返回 `true`;否则返回 `false`。

### `int QHeaderView::length() const`

**作用与语义：**

返回沿头部方向的长度。

### `int QHeaderView::logicalIndex(int visualIndex) const`

**作用与语义：**

返回该截面在给定`visualIndex`位置的逻辑索引，若`visualIndex` < 0或 `visualIndex` >= `QHeaderView::count()`则返回 -1。
请注意，`visualIndex`不会受到隐藏部分的影响。

### `int QHeaderView::logicalIndexAt(const QPoint &pos) const`

**作用与语义：**

返回`pos`中给定位置截面的逻辑索引。如果头是水平的，则使用x坐标，否则使用y坐标来查找逻辑索引。

### `int QHeaderView::logicalIndexAt(int position) const`

**作用与语义：**

返回视窗中覆盖给定`position`的部分。

### `int QHeaderView::logicalIndexAt(int x, int y) const`

**作用与语义：**

返回给定坐标处截面的逻辑索引。如果头部是水平的，则使用`x`，否则`y`用于查找逻辑索引。

### `[override virtual protected] void QHeaderView::mouseDoubleClickEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QAbstractItemView::mouseDoubleClickEvent`（QMouseEvent *event）。

### `[override virtual protected] void QHeaderView::mouseMoveEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QAbstractItemView::mouseMoveEvent`（QMouseEvent *event）。

### `[override virtual protected] void QHeaderView::mousePressEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QAbstractItemView::mousePressEvent`（QMouseEvent *event）。

### `[override virtual protected] void QHeaderView::mouseReleaseEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QAbstractItemView::mouseReleaseEvent`（QMouseEvent *event）。

### `void QHeaderView::moveSection(int from, int to)`

**作用与语义：**

将视觉索引`from`部分移动到视觉索引`to`。

### `int QHeaderView::offset() const`

**作用与语义：**

返回头部的偏移量：这是头部最左边（竖头最顶端）可见像素。

### `Qt::Orientation QHeaderView::orientation() const`

**作用与语义：**

返回头部的朝向。

### `[override virtual protected] void QHeaderView::paintEvent(QPaintEvent *e)`

**作用与语义：**

重实现自：`QAbstractScrollArea::paintEvent`（QPaintEvent *event）。

### `[virtual protected] void QHeaderView::paintSection(QPainter *painter, const QRect &rect, int logicalIndex) const`

**作用与语义：**

使用给定的`painter`和`rect`，绘制给定`logicalIndex`指定剖面。
通常，你不必调用这个函数。

### `[override virtual] void QHeaderView::reset()`

**作用与语义：**

重装：`QAbstractItemView::reset()`。
重置视图的内部状态。
警告：该函数将重置打开的编辑器、滚动条位置、选择等。现有的更改不会被提交。如果你想在重置视图时保存你的更改，可以重新实现这个函数，提交你的更改，然后调用该超类的实现。

### `int QHeaderView::resizeContentsPrecision() const`

**作用与语义：**

返回`QHeaderView`对`ResizeToContents`计算的精确度。

### `void QHeaderView::resizeSection(int logicalIndex, int size)`

**作用与语义：**

将`logicalIndex`指定截面调整为像素单位的 `size`。大小参数必须大于或等于零。但不建议使用大小为零。在这种情况下应使用`hideSection`。

### `[protected slot] void QHeaderView::resizeSections()`

**作用与语义：**

根据大小提示调整各部分的大小。通常，你不需要调用这个函数。
注意：该槽位已超载。连接该槽位：


使用 qOverload 连接：
connect（sender， &SenderClass：：signal，。
headerView， qOverload<>（&QHeaderView：：resizeSections））;

或者用lambda作为包装器：
connect（sender， &SenderClass：：signal，。
headerView， [receiver = headerView]() { receiver->resizeSections(); }）;


更多示例和方法，请参见连接超载槽位。

### `void QHeaderView::resizeSections(QHeaderView::ResizeMode mode)`

**作用与语义：**

根据给定的`mode`调整部分大小，忽略当前的缩放模式。

### `bool QHeaderView::restoreState(const QByteArray &state)`

**作用与语义：**

恢复该头部视图的 `state`。如果状态恢复，该函数返回 `true`;否则返回 false。

### `QByteArray QHeaderView::saveState() const`

**作用与语义：**

保存该头视图的当前状态。
要恢复保存状态，将返回值传递给`restoreState()`。

### `[signal] void QHeaderView::sectionClicked(int logicalIndex)`

**作用与语义：**

当点击某一部分时，该信号会发出。该部分的逻辑索引由`logicalIndex`指定。
注意，`sectionPressed`信号也会被发射。

### `[signal] void QHeaderView::sectionCountChanged(int oldCount, int newCount)`

**作用与语义：**

当节数变化时，即新增或删除节数时，会发出该信号。原始计数由`oldCount`指定，新计数由`newCount`表示。

### `[signal] void QHeaderView::sectionDoubleClicked(int logicalIndex)`

**作用与语义：**

该信号在双击某段时发出。该段的逻辑索引由`logicalIndex`指定。

### `[signal] void QHeaderView::sectionEntered(int logicalIndex)`

**作用与语义：**

当光标移动到该部分并按下鼠标左键时，该信号会发出。该部分的逻辑索引由`logicalIndex`指定。

### `[signal] void QHeaderView::sectionHandleDoubleClicked(int logicalIndex)`

**作用与语义：**

该信号在双击某段时发出。该段的逻辑索引由`logicalIndex`指定。

### `[signal] void QHeaderView::sectionMoved(int logicalIndex, int oldVisualIndex, int newVisualIndex)`

**作用与语义：**

当分段移动时，该信号会发出。分段的逻辑索引由`logicalIndex`指定，旧索引由`oldVisualIndex`表示，新索引位置由`newVisualIndex`指定。

### `int QHeaderView::sectionPosition(int logicalIndex) const`

**作用与语义：**

返回给定`logicalIndex`的部分位置，或如果该部分隐藏，则返回-1。位置以像素为单位，从第一个可见的项目左上角到带有`logicalIndex`的项目左上角。水平头条沿x轴，竖向头条沿y轴测量。

### `[signal] void QHeaderView::sectionPressed(int logicalIndex)`

**作用与语义：**

当按下某段时，该信号会发出。该段的逻辑索引由`logicalIndex`指定。

### `QHeaderView::ResizeMode QHeaderView::sectionResizeMode(int logicalIndex) const`

**作用与语义：**

返回适用于指定`logicalIndex`部分的缩放模式。

### `[signal] void QHeaderView::sectionResized(int logicalIndex, int oldSize, int newSize)`

**作用与语义：**

当截面大小调整时，该信号会发出。该段的逻辑编号由`logicalIndex`表示，旧尺寸由`oldSize`表示，新大小由 `newSize` 表示。

### `int QHeaderView::sectionSize(int logicalIndex) const`

**作用与语义：**

返回给定`logicalIndex`的宽度（垂直头部的高度）。

### `[virtual protected] QSize QHeaderView::sectionSizeFromContents(int logicalIndex) const`

**作用与语义：**

返回给定`logicalIndex`指定部分内容的大小。

### `int QHeaderView::sectionSizeHint(int logicalIndex) const`

**作用与语义：**

返回`logicalIndex`指定截面的合适大小提示。
`Qt::SizeHintRole`。

### `int QHeaderView::sectionViewportPosition(int logicalIndex) const`

**作用与语义：**

返回给定`logicalIndex`的截面视口位置。
如果该部分被隐藏，返回值未定义。

### `[protected slot] void QHeaderView::sectionsAboutToBeRemoved(const QModelIndex &parent, int logicalFirst, int logicalLast)`

**作用与语义：**

当部分从`parent`中移除时，称为该槽。`logicalFirst`和`logicalLast`表示部分被移除的位置。
如果只移除一个部分，则`logicalFirst`和`logicalLast`将是相同的。

### `bool QHeaderView::sectionsClickable() const`

**作用与语义：**

退货部分可点击。
注意：属性分区的获取函数可点击。

### `bool QHeaderView::sectionsHidden() const`

**作用与语义：**

如果头部中的部分被隐藏，返回`true`;否则返回 false;

### `[protected slot] void QHeaderView::sectionsInserted(const QModelIndex &parent, int logicalFirst, int logicalLast)`

**作用与语义：**

当`parent`插入节时，称为该槽位。`logicalFirst`和`logicalLast`标表示新部分插入的位置。
如果只插入一个部分，`logicalFirst`和`logicalLast`将是相同的。

### `bool QHeaderView::sectionsMovable() const`

**作用与语义：**

退货部分可移动。
注意：对于属性部分可移动的获取函数。

### `bool QHeaderView::sectionsMoved() const`

**作用与语义：**

如果头部中的部分被移动，返回`true`;否则返回false;

### `[override virtual] void QHeaderView::setModel(QAbstractItemModel *model)`

**作用与语义：**

重实现自：`QAbstractItemView::setModel`（QAbstractItemModel *model）。
将视图的`model`设定为呈现。
该函数将创建并设置新的选择模型，替换之前用`setSelectionModel()`设置的模型。不过，旧的选择模型不会被删除，因为它可能在多个视图之间共享。如果旧的选择模型不再需要，我们建议你删除它。这可以通过以下代码完成：
如果旧模型和旧选择模型都没有父模型，或者它们的父对象是长寿命对象，可能更倾向于调用它们的`deleteLater()`函数来显式删除它们。
视图不会拥有该模型的所有权，除非它是模型的父对象，因为模型可能在多个不同视图之间共享。

### `[slot] void QHeaderView::setOffset(int offset)`

**作用与语义：**

将头部的偏移设置为`offset`。

### `[slot] void QHeaderView::setOffsetToLastSection()`

**作用与语义：**

设置偏移量，使最后一段可见。

### `[slot] void QHeaderView::setOffsetToSectionPosition(int visualSectionNumber)`

**作用与语义：**

将偏移量设置为截面起点，位于给定`visualSectionNumber`。`visualSectionNumber` 是隐藏时实际可见的截面。不考虑截面。这不总是等同于`visualIndex()`。

### `void QHeaderView::setResizeContentsPrecision(int precision)`

**作用与语义：**

设置`QHeaderView`在使用`ResizeToContents`时应计算大小的精确度。较低的数值会提供较不准确但快速的自动缩放;较高的值则能提供更准确但速度较慢的调整。
`precision`数表示在计算首选尺寸时应考虑多少部分。
默认值是1000，这意味着自动调整尺寸的水平列在计算时最多会显示1000行。
特殊值0意味着它只查看可见区域。特殊值-1意味着查看所有元素。
该值用于`QTableView::sizeHintForColumn()`、`QTableView::sizeHintForRow()`和`QTreeView::sizeHintForColumn()`。重新实现这些函数可能会使该函数失去效果。

### `void QHeaderView::setSectionHidden(int logicalIndex, bool hide)`

**作用与语义：**

如果`hide`为真，则`logicalIndex`指定的截面被隐藏;否则该截面被显示。

### `void QHeaderView::setSectionResizeMode(QHeaderView::ResizeMode mode)`

**作用与语义：**

设定了如何将头部调整为给定`mode`描述大小的约束。

### `void QHeaderView::setSectionResizeMode(int logicalIndex, QHeaderView::ResizeMode mode)`

**作用与语义：**

设置了如何将头部中`logicalIndex`指定的部分调整为给定`mode`描述的部分的约束。逻辑索引应在调用该函数时存在。
注意：如果`stretchLastSection`属性设置为true，最后一节该设置将被忽略。这是`QTreeView`提供的水平头部的默认设置。

### `void QHeaderView::setSectionsClickable(bool clickable)`

**作用与语义：**

如果头部可点击，则保持`true`;否则`false`。可点击头部可以设置，允许用户在视图中更改与头部相关的数据表示方式。

**如何使用：** 调用 `setSectionsClickable(...)` 修改 `sectionsClickable`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QHeaderView::setSectionsMovable(bool movable)`

**作用与语义：**

如果`sectionsMovable`为真，用户可以移动头部部分;否则它们会被固定在原位。
与`QTreeView`结合使用时，第一列默认不可移动（因为它包含树状结构）。你可以用`setFirstSectionMovable`（true）让它可移动。

**如何使用：** 调用 `setSectionsMovable(...)` 修改 `sectionsMovable`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `[override virtual protected] void QHeaderView::setSelection(const QRect &rect, QItemSelectionModel::SelectionFlags flags)`

**作用与语义：**

重实现自：`QAbstractItemView::setSelection`（const QRect &rect， QItemSelectionModel：：SelectionFlags flags）。
根据指定`flags`选择给定`rect`中的物品。
基础类实现什么都不做。
将选择`flags`应用到矩形内或被触及的物品，`rect`。
在实现自己的 itemview 时，setSelection 应调用 `selectionModel()`->select（selection， flags），其中 select 要么是空`QModelIndex`，要么是包含所有 `rect` 中物品的`QItemSelection`。

### `void QHeaderView::setSortIndicator(int logicalIndex, Qt::SortOrder order)`

**作用与语义：**

为`order`指定方向`logicalIndex`指定的部分设置排序指示器，并移除显示该分拣的其他部分的排序指示器。
`logicalIndex`可能为-1，此时不会显示排序指示，模型将恢复到自然的未排序顺序。注意，并非所有模型都支持此功能，甚至可能崩溃。

### `[override virtual] void QHeaderView::setVisible(bool v)`

**作用与语义：**

重新实现了属性的访问函数：`QWidget::visible`。

### `void QHeaderView::showSection(int logicalIndex)`

**作用与语义：**

显示`logicalIndex`指定的部分。

### `[override virtual] QSize QHeaderView::sizeHint() const`

**作用与语义：**

重装：`QAbstractScrollArea::sizeHint()` const.
返回该头部的适当大小提示。

### `[signal] void QHeaderView::sortIndicatorChanged(int logicalIndex, Qt::SortOrder order)`

**作用与语义：**

当包含排序指示器的部分或指示的顺序发生变化时，该信号会发出。该段的逻辑索引由`logicalIndex`指定，排序顺序由`order`指定。

### `Qt::SortOrder QHeaderView::sortIndicatorOrder() const`

**作用与语义：**

返回排序指示器的顺序。如果没有哪个部分有排序指示器，则该函数的返回值未定义。

### `int QHeaderView::sortIndicatorSection() const`

**作用与语义：**

返回带有排序指示器的部分的逻辑索引。默认情况下，这是第0节。

### `int QHeaderView::stretchSectionCount() const`

**作用与语义：**

返回设置为缩放模式拉伸的截面数量。在视图中，可以用来判断视图几何形状变化时是否需要调整截面大小。

### `void QHeaderView::swapSections(int first, int second)`

**作用与语义：**

将视觉索引`first`的部分与视觉索引`second`的部分交换。

### `[override virtual protected] int QHeaderView::verticalOffset() const`

**作用与语义：**

重装：`QAbstractItemView::verticalOffset()` const.
返回头部的垂直偏移量。对于水平头部，这个值为0。
返回视图的垂直偏移量。
在基类中，这是一个纯虚拟函数。

### `[override virtual protected] bool QHeaderView::viewportEvent(QEvent *e)`

**作用与语义：**

重装：`QAbstractItemView::viewportEvent`（QEvent *事件）。

### `int QHeaderView::visualIndex(int logicalIndex) const`

**作用与语义：**

返回由给定`logicalIndex`指定截面的视觉索引位置，否则返回-1。
隐藏部分仍然有有效的视觉索引。

### `int QHeaderView::visualIndexAt(int position) const`

**作用与语义：**

返回覆盖视口中给定`position`的区域的视觉索引。

### `bool cascadingSectionResizes() const`

**作用与语义：**

该属性决定了当用户调整的区域达到最小大小后，交互式调整大小是否会级联到后续部分。
该特性仅影响以`Interactive`为缩放模式的部分。
默认值为假。

**如何使用：** 调用 `cascadingSectionResizes()` 读取当前值；它不会修改应用状态。

### `Qt::Alignment defaultAlignment() const`

**作用与语义：**

该属性表示每个头部文本的默认对齐。

**如何使用：** 调用 `defaultAlignment()` 读取当前值；它不会修改应用状态。

### `int defaultSectionSize() const`

**作用与语义：**

该属性保留了缩写前头部部分的默认大小。
该特性仅影响以`Interactive`或`Fixed`为缩放模式的部分。
默认情况下，该属性的值与样式相关。因此，当样式发生变化时，该属性会从中更新。调用 setDefaultSectionSize() 会停止更新，调用 resetDefaultSectionSize() 则会恢复默认行为。

**如何使用：** 调用 `defaultSectionSize()` 读取当前值；它不会修改应用状态。

### `bool highlightSections() const`

**作用与语义：**

该属性决定是否高亮包含所选项目的章节。
默认情况下，该属性为`false`。

**如何使用：** 调用 `highlightSections()` 读取当前值；它不会修改应用状态。

### `bool isFirstSectionMovable() const`

**作用与语义：**

该属性决定用户是否可以移动第一列。
该属性控制用户是否可以移动第一列。在`QTreeView`中，第一列保留树结构，因此默认不可移动，即使达到`setSectionsMovable`（真）之后也是如此。
例如，在没有树结构的平面列表的情况下，可以通过调用此方法使其再次可移动。在这种情况下，建议也调用 `QTreeView::setRootIsDecorated`（false）。
设置为true没有效果，除非同时调用`setSectionsMovable`（true）。

**如何使用：** 调用 `isFirstSectionMovable()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 treeView->setRootIsDecorated(false);
 treeView->header()->setFirstSectionMovable(true);
```

### `bool isSortIndicatorClearable() const`

**作用与语义：**

该属性决定排序指示器是否可以通过多次点击某一部分来清除。
该属性控制用户是否能通过多次点击该分段来移除该分段的排序指示。通常，点击某一分段只是改变该分段的排序顺序。将该属性设置为 true，排序指示器在交替升降后会被清除;这通常会恢复模型的原始排序。
将该属性设置为 true（除非 `sectionsClickable()` 也为真，否则无效（例如 `QTableView` 是某些视图的默认值，或者在使视图可排序时自动设置，例如调用 `QTreeView::setSortingEnabled`）。

**如何使用：** 调用 `isSortIndicatorClearable()` 读取当前值；它不会修改应用状态。

### `bool isSortIndicatorShown() const`

**作用与语义：**

该属性在排序指示器显示时成立。
默认情况下，该属性为`false`。

**如何使用：** 调用 `isSortIndicatorShown()` 读取当前值；它不会修改应用状态。

### `int maximumSectionSize() const`

**作用与语义：**

该属性包含了头部段的最大大小。
最大截面大小是允许的最大截面大小。该属性的默认值是1048575，这也是截面的最大可能大小。将最大值设为 -1 会将值重置为最大截面大小。
除了拉伸外，这一特性被所有缩放模式都遵守。

**如何使用：** 调用 `maximumSectionSize()` 读取当前值；它不会修改应用状态。

### `int minimumSectionSize() const`

**作用与语义：**

该属性包含了头部段的最小大小。
最小节大小是允许的最小节大小。如果最小节大小设置为 -1，`QHeaderView`将使用字体度量大小。
所有缩放模式都尊重这一特性。

**如何使用：** 调用 `minimumSectionSize()` 读取当前值；它不会修改应用状态。

### `void resetDefaultSectionSize()`

**作用与语义：**

该属性保留了缩写前头部部分的默认大小。
该特性仅影响以`Interactive`或`Fixed`为缩放模式的部分。
默认情况下，该属性的值与样式相关。因此，当样式发生变化时，该属性会从中更新。调用 setDefaultSectionSize() 会停止更新，调用 resetDefaultSectionSize() 则会恢复默认行为。

**如何使用：** 调用 `resetDefaultSectionSize()` 撤销对 `defaultSectionSize` 的显式覆盖，让它重新采用继承值或默认值。

### `void setCascadingSectionResizes(bool enable)`

**作用与语义：**

该属性决定了当用户调整的区域达到最小大小后，交互式调整大小是否会级联到后续部分。
该特性仅影响以`Interactive`为缩放模式的部分。
默认值为假。

**如何使用：** 调用 `setCascadingSectionResizes(...)` 修改 `cascadingSectionResizes`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setDefaultAlignment(Qt::Alignment alignment)`

**作用与语义：**

该属性表示每个头部文本的默认对齐。

**如何使用：** 调用 `setDefaultAlignment(...)` 修改 `defaultAlignment`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setDefaultSectionSize(int size)`

**作用与语义：**

该属性保留了缩写前头部部分的默认大小。
该特性仅影响以`Interactive`或`Fixed`为缩放模式的部分。
默认情况下，该属性的值与样式相关。因此，当样式发生变化时，该属性会从中更新。调用 setDefaultSectionSize() 会停止更新，调用 resetDefaultSectionSize() 则会恢复默认行为。

**如何使用：** 调用 `setDefaultSectionSize(...)` 修改 `defaultSectionSize`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setFirstSectionMovable(bool movable)`

**作用与语义：**

该属性决定用户是否可以移动第一列。
该属性控制用户是否可以移动第一列。在`QTreeView`中，第一列保留树结构，因此默认不可移动，即使达到`setSectionsMovable`（真）之后也是如此。
例如，在没有树结构的平面列表的情况下，可以通过调用此方法使其再次可移动。在这种情况下，建议也调用 `QTreeView::setRootIsDecorated`（false）。
设置为true没有效果，除非同时调用`setSectionsMovable`（true）。

**如何使用：** 调用 `setFirstSectionMovable(...)` 修改 `firstSectionMovable`；传入的新值会成为后续查询和相关界面行为所使用的值。

**官方示例：**

```cpp
 treeView->setRootIsDecorated(false);
 treeView->header()->setFirstSectionMovable(true);
```

### `void setHighlightSections(bool highlight)`

**作用与语义：**

该属性决定是否高亮包含所选项目的章节。
默认情况下，该属性为`false`。

**如何使用：** 调用 `setHighlightSections(...)` 修改 `highlightSections`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMaximumSectionSize(int size)`

**作用与语义：**

该属性包含了头部段的最大大小。
最大截面大小是允许的最大截面大小。该属性的默认值是1048575，这也是截面的最大可能大小。将最大值设为 -1 会将值重置为最大截面大小。
除了拉伸外，这一特性被所有缩放模式都遵守。

**如何使用：** 调用 `setMaximumSectionSize(...)` 修改 `maximumSectionSize`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMinimumSectionSize(int size)`

**作用与语义：**

该属性包含了头部段的最小大小。
最小节大小是允许的最小节大小。如果最小节大小设置为 -1，`QHeaderView`将使用字体度量大小。
所有缩放模式都尊重这一特性。

**如何使用：** 调用 `setMinimumSectionSize(...)` 修改 `minimumSectionSize`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setSortIndicatorClearable(bool clearable)`

**作用与语义：**

该属性决定排序指示器是否可以通过多次点击某一部分来清除。
该属性控制用户是否能通过多次点击该分段来移除该分段的排序指示。通常，点击某一分段只是改变该分段的排序顺序。将该属性设置为 true，排序指示器在交替升降后会被清除;这通常会恢复模型的原始排序。
将该属性设置为 true（除非 `sectionsClickable()` 也为真，否则无效（例如 `QTableView` 是某些视图的默认值，或者在使视图可排序时自动设置，例如调用 `QTreeView::setSortingEnabled`）。

**如何使用：** 调用 `setSortIndicatorClearable(...)` 修改 `sortIndicatorClearable`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setSortIndicatorShown(bool show)`

**作用与语义：**

该属性在排序指示器显示时成立。
默认情况下，该属性为`false`。

**如何使用：** 调用 `setSortIndicatorShown(...)` 修改 `showSortIndicator`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setStretchLastSection(bool stretch)`

**作用与语义：**

该属性是否满足头部最后可见部分是否占用所有可用空间。
默认值为假。
注意：`QTreeView`提供的水平首部配置中，此属性设置为 true，确保视图不会浪费其首部分配的空间。如果该值设为 true，该属性将覆盖头部最后一段的缩小模式。

**如何使用：** 调用 `setStretchLastSection(...)` 修改 `stretchLastSection`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `bool stretchLastSection() const`

**作用与语义：**

该属性是否满足头部最后可见部分是否占用所有可用空间。
默认值为假。
注意：`QTreeView`提供的水平首部配置中，此属性设置为 true，确保视图不会浪费其首部分配的空间。如果该值设为 true，该属性将覆盖头部最后一段的缩小模式。

**如何使用：** 调用 `stretchLastSection()` 读取当前值；它不会修改应用状态。

### `void sortIndicatorClearableChanged(bool clearable)`

**作用与语义：**

该属性决定排序指示器是否可以通过多次点击某一部分来清除。
该属性控制用户是否能通过多次点击该分段来移除该分段的排序指示。通常，点击某一分段只是改变该分段的排序顺序。将该属性设置为 true，排序指示器在交替升降后会被清除;这通常会恢复模型的原始排序。
将该属性设置为 true（除非 `sectionsClickable()` 也为真，否则无效（例如 `QTableView` 是某些视图的默认值，或者在使视图可排序时自动设置，例如调用 `QTreeView::setSortingEnabled`）。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `sortIndicatorClearable` 的变化，不要把它当作普通函数主动调用。

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

`QHeaderView` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
