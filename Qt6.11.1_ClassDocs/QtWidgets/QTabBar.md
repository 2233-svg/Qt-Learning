# QTabBar

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QTabBar` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QTabBar` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QTabBar>`
- 继承自：QWidget
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

- `enum ButtonPosition { LeftSide, RightSide }`
- `enum SelectionBehavior { SelectLeftTab, SelectRightTab, SelectPreviousTab }`
- `enum Shape { RoundedNorth, RoundedSouth, RoundedWest, RoundedEast, TriangularNorth, …, TriangularEast }`

### 属性

- `autoHide : bool`
- `changeCurrentOnDrag : bool`
- `count : int`
- `currentIndex : int`
- `documentMode : bool`
- `drawBase : bool`
- `elideMode : Qt::TextElideMode`
- `expanding : bool`
- `iconSize : QSize`
- `movable : bool`
- `selectionBehaviorOnRemove : SelectionBehavior`
- `shape : Shape`
- `tabsClosable : bool`
- `usesScrollButtons : bool`

### 公有函数

- `QTabBar(QWidget *parent = nullptr)`
- `virtual ~QTabBar()`
- `QString accessibleTabName(int index) const`
- `int addTab(const QString &text)`
- `int addTab(const QIcon &icon, const QString &text)`
- `bool autoHide() const`
- `bool changeCurrentOnDrag() const`
- `int count() const`
- `int currentIndex() const`
- `bool documentMode() const`
- `bool drawBase() const`
- `Qt::TextElideMode elideMode() const`
- `bool expanding() const`
- `QSize iconSize() const`
- `int insertTab(int index, const QString &text)`
- `int insertTab(int index, const QIcon &icon, const QString &text)`
- `bool isMovable() const`
- `bool isTabEnabled(int index) const`
- `bool isTabVisible(int index) const`
- `void moveTab(int from, int to)`
- `void removeTab(int index)`
- `QTabBar::SelectionBehavior selectionBehaviorOnRemove() const`
- `void setAccessibleTabName(int index, const QString &name)`
- `void setAutoHide(bool hide)`
- `void setChangeCurrentOnDrag(bool change)`
- `void setDocumentMode(bool set)`
- `void setDrawBase(bool drawTheBase)`
- `void setElideMode(Qt::TextElideMode mode)`
- `void setExpanding(bool enabled)`
- `void setIconSize(const QSize &size)`
- `void setMovable(bool movable)`
- `void setSelectionBehaviorOnRemove(QTabBar::SelectionBehavior behavior)`
- `void setShape(QTabBar::Shape shape)`
- `void setTabButton(int index, QTabBar::ButtonPosition position, QWidget *widget)`
- `void setTabData(int index, const QVariant &data)`
- `void setTabEnabled(int index, bool enabled)`
- `void setTabIcon(int index, const QIcon &icon)`
- `void setTabText(int index, const QString &text)`
- `void setTabTextColor(int index, const QColor &color)`
- `void setTabToolTip(int index, const QString &tip)`
- `void setTabVisible(int index, bool visible)`
- `void setTabWhatsThis(int index, const QString &text)`
- `void setTabsClosable(bool closable)`
- `void setUsesScrollButtons(bool useButtons)`
- `QTabBar::Shape shape() const`
- `int tabAt(const QPoint &position) const`
- `QWidget * tabButton(int index, QTabBar::ButtonPosition position) const`
- `QVariant tabData(int index) const`
- `QIcon tabIcon(int index) const`
- `QRect tabRect(int index) const`
- `QString tabText(int index) const`
- `QColor tabTextColor(int index) const`
- `QString tabToolTip(int index) const`
- `QString tabWhatsThis(int index) const`
- `bool tabsClosable() const`
- `bool usesScrollButtons() const`

### 重实现的公有函数

- `virtual QSize minimumSizeHint() const override`
- `virtual QSize sizeHint() const override`

### 公有槽函数

- `void setCurrentIndex(int index)`

### 信号

- `void currentChanged(int index)`
- `void tabBarClicked(int index)`
- `void tabBarDoubleClicked(int index)`
- `void tabCloseRequested(int index)`
- `void tabMoved(int from, int to)`

### 保护函数

- `virtual void initStyleOption(QStyleOptionTab *option, int tabIndex) const`
- `virtual QSize minimumTabSizeHint(int index) const`
- `virtual void tabInserted(int index)`
- `virtual void tabLayoutChange()`
- `virtual void tabRemoved(int index)`
- `virtual QSize tabSizeHint(int index) const`

### 重实现的保护函数

- `virtual void changeEvent(QEvent *event) override`
- `virtual bool event(QEvent *event) override`
- `virtual void hideEvent(QHideEvent *) override`
- `virtual void keyPressEvent(QKeyEvent *event) override`
- `virtual void mouseDoubleClickEvent(QMouseEvent *event) override`
- `virtual void mouseMoveEvent(QMouseEvent *event) override`
- `virtual void mousePressEvent(QMouseEvent *event) override`
- `virtual void mouseReleaseEvent(QMouseEvent *event) override`
- `virtual void paintEvent(QPaintEvent *) override`
- `virtual void resizeEvent(QResizeEvent *) override`
- `virtual void showEvent(QShowEvent *) override`
- `virtual void timerEvent(QTimerEvent *event) override`
- `virtual void wheelEvent(QWheelEvent *event) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QTabBar::ButtonPosition`

**作用与语义：**

该枚举类型列出了小部件在标签页上的位置。
- `QTabBar::LeftSide`：`0`;标签左侧。
- `QTabBar::RightSide`：`1`;标签右侧。

### `enum QTabBar::SelectionBehavior`

**作用与语义：**

此枚举类型列出了当移除一个标签页且被移除的标签页也是当前标签页时，`QTabBar` 的行为。
- `QTabBar::SelectLeftTab`: `0`；选择被移除标签页左侧的标签页。
- `QTabBar::SelectRightTab`: `1`；选择被移除标签页右侧的标签页。
- `QTabBar::SelectPreviousTab`: `2`；选择之前选择的标签页。

### `enum QTabBar::Shape`

**作用与语义：**

这个枚举类型列出了`QTabBar`支持的内置形状。请将这些视为提示，因为某些样式可能无法渲染部分形状。不过，应尊重位置。
- `QTabBar::RoundedNorth`：`0`;页面上方的正常圆润外观
- `QTabBar::RoundedSouth`：`1`;页面下方的正常圆润外观
- `QTabBar::RoundedWest`：`2`;页面左侧的正常圆润外观
- `QTabBar::RoundedEast`：`3`;右侧页面的正常圆润外观
- `QTabBar::TriangularNorth`：`4`;页面上方的三角形标签。
- `QTabBar::TriangularSouth`：`5`;例如，三角形标签页类似于Excel表格中使用的标签页
- `QTabBar::TriangularWest`：`6`;页面左侧的三角形标签。
- `QTabBar::TriangularEast`：`7`;页面右侧的三角形标签。

### `autoHide : bool`

**作用与语义：**

如果属实，当标签栏少于2个标签时会自动隐藏。
默认情况下，该属性为假。

**如何使用：** 调用 `autoHide()` 读取当前值；它不会修改应用状态。

### `changeCurrentOnDrag : bool`

**作用与语义：**

如果是这样，那么拖动标签栏时当前标签页会自动更换。
注意：你还应将acceptDrops属性设置为true，才能使此功能正常工作。
默认情况下，该属性为假。

**如何使用：** 调用 `changeCurrentOnDrag()` 读取当前值；它不会修改应用状态。

### `[read-only] count : int`

**作用与语义：**

该属性包含标签栏中的标签数量。

**如何使用：** 调用 `count()` 读取当前值；它不会修改应用状态。

### `currentIndex : int`

**作用与语义：**

该属性保留了标签栏可见标签的索引。
如果没有当前标签，当前索引为-1。

**如何使用：** 调用 `currentIndex()` 读取当前值；它不会修改应用状态。

### `documentMode : bool`

**作用与语义：**

无论制表栏是否以适合主窗口的模式渲染，该属性都适用。
这个属性被用作样式的提示，让它们以不同于标签控件中通常的样子绘制标签页。在macOS上，这看起来类似于Safari或Sierra的 Terminal.app 中的标签页。

**如何使用：** 调用 `documentMode()` 读取当前值；它不会修改应用状态。

### `drawBase : bool`

**作用与语义：**

定义了是否应该绘制其底部。
如果成立，则`QTabBar`根据样式重叠绘制基底。否则只绘制标签。

**如何使用：** 调用 `drawBase()` 读取当前值；它不会修改应用状态。

### `elideMode : Qt::TextElideMode`

**作用与语义：**

如何省略标签栏中的文字。
该属性控制在给定标签栏大小下空间不足时，如何省略项目。
默认情况下，数值取决于风格。

**如何使用：** 调用 `elideMode()` 读取当前值；它不会修改应用状态。

### `expanding : bool`

**作用与语义：**

当 是 expand（扩展）时`QTabBar`会扩展标签页以利用空位。
默认情况下，这个数值是真实的。

**如何使用：** 调用 `expanding()` 读取当前值；它不会修改应用状态。

### `iconSize : QSize`

**作用与语义：**

该属性保留了标签栏图标的大小。
默认值取决于样式。`iconSize` 是最大尺寸;图标较小的图标不会放大。

**如何使用：** 调用 `iconSize()` 读取当前值；它不会修改应用状态。

### `movable : bool`

**作用与语义：**

该属性决定用户是否能在标签栏区域内移动标签页。
默认情况下，该属性为`false`;

**如何使用：** 调用 `movable()` 读取当前值；它不会修改应用状态。

### `selectionBehaviorOnRemove : SelectionBehavior`

**作用与语义：**

如果被移除的标签页也是当前标签页，`removeTab`调用时哪个标签页应该设置为当前？
默认值是`SelectRightTab`。

**如何使用：** 调用 `selectionBehaviorOnRemove()` 读取当前值；它不会修改应用状态。

### `shape : Shape`

**作用与语义：**

该属性表示标签栏中标签的形状。
该属性的可能值由 Shape 枚举描述。

**如何使用：** 调用 `shape()` 读取当前值；它不会修改应用状态。

### `tabsClosable : bool`

**作用与语义：**

该属性决定了标签栏是否应该在每个标签页上放置关闭按钮。
当 tabsClosable 设置为 true 时，标签页左侧或右侧会出现关闭按钮，具体取决于样式。当按钮被直接点击，或在标签页任意位置收到鼠标中键点击时，信号`tabCloseRequested`会发出。
默认情况下，该值为假。

**如何使用：** 调用 `tabsClosable()` 读取当前值；它不会修改应用状态。

### `usesScrollButtons : bool`

**作用与语义：**

该属性决定了当标签栏有很多标签时，是否应该使用按钮来滚动标签页。
当标签栏中标签页数量过多，标签栏可以选择放大大小或添加按钮，方便你滚动切换标签页。
默认情况下，数值取决于风格。

**如何使用：** 调用 `usesScrollButtons()` 读取当前值；它不会修改应用状态。

### `[explicit] QTabBar::QTabBar(QWidget *parent = nullptr)`

**作用与语义：**

用给定的`parent`创建一个新的标签栏。

### `[virtual noexcept] QTabBar::~QTabBar()`

**作用与语义：**

标签栏会被破坏。

### `QString QTabBar::accessibleTabName(int index) const`

**作用与语义：**

返回位置`index`的标签页的可访问名，若`index`超出范围则返回空字符串。

### `int QTabBar::addTab(const QString &text)`

**作用与语义：**

添加一个带有文本`text`的新标签页。返回新标签页的索引。

### `int QTabBar::addTab(const QIcon &icon, const QString &text)`

**作用与语义：**

添加一个带有图标`icon`和文本`text`的新标签页。返回新标签页的索引。

### `[override virtual protected] void QTabBar::changeEvent(QEvent *event)`

**作用与语义：**

重装：`QWidget::changeEvent`（QEvent *事件）。
该事件处理程序可以重新实现以处理状态变化。
该事件中被更改的状态可以通过提供的`event`检索。
变更事件包括：`QEvent::ToolBarChange`、`QEvent::ActivationChange`、`QEvent::EnabledChange`、`QEvent::FontChange`、`QEvent::StyleChange`、`QEvent::PaletteChange`、`QEvent::WindowTitleChange`、`QEvent::IconTextChange`、`QEvent::ModifiedChange`、`QEvent::MouseTrackingChange`、`QEvent::ParentChange`、`QEvent::WindowStateChange`、`QEvent::LanguageChange`、`QEvent::LocaleChange`、`QEvent::LayoutDirectionChange`、`QEvent::ReadOnlyChange`。

### `[signal] void QTabBar::currentChanged(int index)`

**作用与语义：**

该属性保留了标签栏可见标签的索引。
如果没有当前标签，当前索引为-1。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `currentIndex` 的变化，不要把它当作普通函数主动调用。

### `[override virtual protected] bool QTabBar::event(QEvent *event)`

**作用与语义：**

重实现自：`QWidget::event`（QEvent *事件）。

### `[override virtual protected] void QTabBar::hideEvent(QHideEvent *)`

**作用与语义：**

重实现自：`QWidget::hideEvent`（QHideEvent *event）。
该事件处理程序可以在子类中重新实现，以接收控件隐藏事件。事件通过`event`参数传递。
隐藏事件会在小部件被隐藏后立即发送。
注意：当窗口系统改变其映射状态时，小部件会接收自发显示和隐藏事件，例如用户最小化窗口时自发隐藏事件，恢复窗口时自发显示事件。收到自发隐藏事件后，小部件仍被视为可见，意义`isVisible()`。

### `[virtual protected] void QTabBar::initStyleOption(QStyleOptionTab *option, int tabIndex) const`

**作用与语义：**

用`tabIndex`标签页的值初始化`option`。这种方法对需要一个`QStyleOptionTab`但不想自己填满所有信息的子类很有用。

### `int QTabBar::insertTab(int index, const QString &text)`

**作用与语义：**

在`index`位置插入带有文本`text`的新标签。如果`index`超出范围，则添加新标签。返回新标签的索引。

### `int QTabBar::insertTab(int index, const QIcon &icon, const QString &text)`

**作用与语义：**

插入一个带有图标`icon`和文本`text`的新标签页，位置`index`。如果`index`超出范围，则添加新标签。返回新标签的索引。
如果在调用该函数前`QTabBar`为空，插入的标签页将成为当前标签页。
在索引小于或等于当前索引处插入新标签会递增当前索引，但保留当前标签。

### `bool QTabBar::isTabEnabled(int index) const`

**作用与语义：**

如果位置`index`的标签页启用，返回`true`;否则返回`false`。

### `bool QTabBar::isTabVisible(int index) const`

**作用与语义：**

如果位置`index`的制表符可见，则返回真;否则返回假。

### `[override virtual protected] void QTabBar::keyPressEvent(QKeyEvent *event)`

**作用与语义：**

重实现自：`QWidget::keyPressEvent`（QKeyEvent *event）。
该事件处理程序用于事件`event`，可以在子类中重新实现，以接收该控件的按键事件。
一个小部件必须调用`setFocusPolicy()`先接受焦点，并且必须有焦点才能接收按键事件。
如果你重新实现这个处理器，如果你不对密钥进行操作，务必调用基类实现。
默认实现会关闭弹出小部件，如果用户按下`QKeySequence::Cancel`的按键序列（通常是 Escape 键）。否则事件会被忽略，以便小部件的父节点能够解释。
注意`QKeyEvent`以 isAccepted() == true 开头，所以你不需要调用 `QKeyEvent::accept()`——只要你对该键执行时不要调用基类实现即可。

### `[override virtual] QSize QTabBar::minimumSizeHint() const`

**作用与语义：**

重新实现属性的访问函数：`QWidget::minimumSizeHint`。

### `[virtual protected] QSize QTabBar::minimumTabSizeHint(int index) const`

**作用与语义：**

返回位置`index`的最小标签大小提示。

### `[override virtual protected] void QTabBar::mouseDoubleClickEvent(QMouseEvent *event)`

**作用与语义：**

重实现自：`QWidget::mouseDoubleClickEvent`（QMouseEvent *event）。
该事件处理程序用于事件`event`，可以在子类中重新实现，以接收小部件的鼠标双击事件。
默认实现调用`mousePressEvent()`。
注意：该小部件除了双击事件外，还会接收鼠标按键和鼠标释放事件。如果与该小部件重叠的其他小部件在新闻发布事件后消失，则该小部件只会接收双击事件。开发者有责任确保应用程序正确解读这些事件。

### `[override virtual protected] void QTabBar::mouseMoveEvent(QMouseEvent *event)`

**作用与语义：**

重实现自：`QWidget::mouseMoveEvent`（QMouseEvent *event）。
该事件处理程序用于事件`event`，可以重新实现为子类，以接收该小部件的鼠标移动事件。
如果关闭鼠标追踪，只有在鼠标移动过程中按下鼠标按钮时才会发生鼠标移动事件。如果开启鼠标追踪，即使未按键，鼠标移动事件也会发生。
`QMouseEvent::position()`报告鼠标光标相对于该小部件的位置。对于按下和释放事件，位置通常与最后一次鼠标移动事件的位置相同，但如果用户的手握手，可能会有所不同。这是底层窗口系统的功能，而非Qt。
如果你想在鼠标移动时立即显示提示（例如，获取鼠标坐标与`QMouseEvent::position()`并显示为提示），你必须先启用上述的鼠标追踪功能。然后，为了确保提示立即更新，你必须在鼠标移动事件（mouseMoveEvent）实现中调用`QToolTip::showText()`而不是`setToolTip()`。

### `[override virtual protected] void QTabBar::mousePressEvent(QMouseEvent *event)`

**作用与语义：**

重实现自：`QWidget::mousePressEvent`（QMouseEvent *event）。
该事件处理程序用于事件`event`，可以重新实现为子类，以接收该小部件的鼠标按键事件。
如果你在 mousePressEvent() 创建新控件，`mouseReleaseEvent()`可能不会出现在你预期的位置，这取决于底层窗口系统（或 X11 窗口管理器）、控件的位置，甚至可能还有其他因素。
默认实现实现了当你点击窗口外时关闭弹出小部件的功能。对于其他小部件类型，它没有任何作用。

### `[override virtual protected] void QTabBar::mouseReleaseEvent(QMouseEvent *event)`

**作用与语义：**

重实现自：`QWidget::mouseReleaseEvent`（QMouseEvent *event）。
该事件处理程序用于事件`event`，可以重新实现为子类，以接收该小部件的鼠标释放事件。

### `void QTabBar::moveTab(int from, int to)`

**作用与语义：**

将索引位置`from`的项目移动到索引位置`to`。

### `[override virtual protected] void QTabBar::paintEvent(QPaintEvent *)`

**作用与语义：**

重实现自：`QWidget::paintEvent`（QPaintEvent *event）。
该事件处理程序可以在子类中重新实现，以接收 `event` 传递的绘画事件。
绘图事件是请求重新绘制一个小部件的全部或部分。它可能由以下原因之一发生：
- `repaint()`或`update()`被援引，
- 小部件被遮挡，现已被发现，或
- 还有很多其他原因。
许多控件可以在被要求时重新绘制整个表面，但一些慢速控件需要通过仅绘制请求的区域来优化：`QPaintEvent::region()`。这种速度优化不会改变结果，因为在事件处理过程中绘制会被裁剪到该区域。例如，`QListView`和`QTableView`就是这样做的。
Qt 还试图通过将多个绘画事件合并为一个来加快绘画速度。当 `update()` 被多次调用或窗口系统发送多个绘画事件时，Qt 会将这些事件合并为一个区域更大的事件（参见 `QRegion::united()`）。`repaint()` 函数不支持这种优化，因此我们建议尽可能使用 `update()`。
当绘制事件发生时，更新区域通常已经被擦除，所以你是在小部件的背景上作画。
背景可以用`setBackgroundRole()`和`setPalette()`设置。
自 Qt 4.0 起，`QWidget` 会自动双缓冲绘制，因此无需在 paintEvent() 中编写双缓冲代码以避免闪烁。
注意：通常，你应避免在paintEvent()中调用`update()`或`repaint()`。例如，在paintEvent()中调用`update()`或`repaint()`会导致行为未定义;孩子可能会或不会获得绘画事件。
警告：如果你使用没有 Qt backingstore 的自定义绘图引擎，`Qt::WA_PaintOnScreen`必须设置。否则，`QWidget::paintEngine()` 永远不会被调用;Backingstore 将被使用。

### `void QTabBar::removeTab(int index)`

**作用与语义：**

移除位置`index`的标签。

### `[override virtual protected] void QTabBar::resizeEvent(QResizeEvent *)`

**作用与语义：**

重实现自：`QWidget::resizeEvent`（QResizeEvent *event）。
该事件处理程序可以在子类中重新实现，以接收通过 `event` 参数传递的控件调整大小事件。当调用 resizeEvent() 时，控件已经拥有新的几何体。旧的大小可以通过 `QResizeEvent::oldSize()` 访问。
控件会被擦除，并在处理调整尺寸事件后立即接收绘图事件。不需要（也不应该）在这个处理程序中进行绘图。

### `void QTabBar::setAccessibleTabName(int index, const QString &name)`

**作用与语义：**

将位置`index`标签的可访问名设置为`name`。

### `void QTabBar::setTabButton(int index, QTabBar::ButtonPosition position, QWidget *widget)`

**作用与语义：**

`widget`设置在标签`index`。小部件根据`position`放在左侧或右侧。
`position`中之前设置的任何小部件都被隐藏了。将`widget`设置为`nullptr`会隐藏当前小部件在`position`。
标签栏会拥有该小部件的所有权，因此当标签栏被销毁时，所有设置的小部件都会被标签栏删除，除非你在设置其他小部件（或`nullptr`）后单独重新子长该小部件。

### `void QTabBar::setTabData(int index, const QVariant &data)`

**作用与语义：**

将位置`index`的标签数据设置为`data`。

### `void QTabBar::setTabEnabled(int index, bool enabled)`

**作用与语义：**

如果`enabled`为真，则位置`index`的标签页被启用;否则位置`index`的项目被禁用。

### `void QTabBar::setTabIcon(int index, const QIcon &icon)`

**作用与语义：**

将位置`index`的标签图标设置为`icon`。

### `void QTabBar::setTabText(int index, const QString &text)`

**作用与语义：**

将位置`index`的标签文本设置为`text`。

### `void QTabBar::setTabTextColor(int index, const QColor &color)`

**作用与语义：**

将标签页中与指定`index`的文本颜色设置为指定的 `color`。
如果指定了无效颜色，标签页将使用`QTabBar`前景角色。

### `void QTabBar::setTabToolTip(int index, const QString &tip)`

**作用与语义：**

将标签在`index`位置的工具尖设为`tip`。

### `void QTabBar::setTabVisible(int index, bool visible)`

**作用与语义：**

如果`visible`成立，就让位置`index`的标签显示，否则隐藏。

### `void QTabBar::setTabWhatsThis(int index, const QString &text)`

**作用与语义：**

将标签页位置`index`的“这是什么”帮助文本设置为`text`。

### `[override virtual protected] void QTabBar::showEvent(QShowEvent *)`

**作用与语义：**

重实现自：`QWidget::showEvent`（QShowEvent *event）。
该事件处理程序可以在子类中重新实现，以接收传递给 `event` 参数的控件显示事件。
非自发的展示事件会在展示前立即发送到小部件。窗口的自发展示事件则在展示之后交付。
注意：当窗口系统改变其映射状态时，小部件会接收自发显示和隐藏事件，例如用户最小化窗口时自发隐藏事件，窗口恢复时自发显示事件。收到自发隐藏事件后，小部件仍被视为`isVisible()`可见。

### `[override virtual] QSize QTabBar::sizeHint() const`

**作用与语义：**

重新实现了属性的访问函数：`QWidget::sizeHint`。

### `int QTabBar::tabAt(const QPoint &position) const`

**作用与语义：**

返回覆盖`position`的标签的索引，若无覆盖`position`则返回-1;

### `[signal] void QTabBar::tabBarClicked(int index)`

**作用与语义：**

当用户点击`index`的标签页时，会发出该信号。
`index` 是点击的标签页的索引，或者如果光标下方没有标签页，则是 -1。

### `[signal] void QTabBar::tabBarDoubleClicked(int index)`

**作用与语义：**

当用户双击`index`的标签页时，会发出该信号。
`index`指点击的标签页，或者如果光标下方没有标签页，则表示-1。

### `QWidget *QTabBar::tabButton(int index, QTabBar::ButtonPosition position) const`

**作用与语义：**

返回小部件，设置一个`index`标签，如果没有设置，`position`或`nullptr`。

### `[signal] void QTabBar::tabCloseRequested(int index)`

**作用与语义：**

当点击标签页上的关闭按钮时，会发出这个信号。`index`是应该移除的索引。

### `QVariant QTabBar::tabData(int index) const`

**作用与语义：**

返回位置`index`的标签数据，若`index`超出范围则返回空变量。

### `QIcon QTabBar::tabIcon(int index) const`

**作用与语义：**

返回位置`index`的标签图标，如果超出`index`范围，则返回空图标。

### `[virtual protected] void QTabBar::tabInserted(int index)`

**作用与语义：**

在添加或插入新标签页到位置`index`后调用该虚拟处理器。

### `[virtual protected] void QTabBar::tabLayoutChange()`

**作用与语义：**

每当标签页布局发生变化时，都会调用这个虚拟处理程序。

### `[signal] void QTabBar::tabMoved(int from, int to)`

**作用与语义：**

当标签在索引位置`from`移动到索引位置`to`时发出该信号。
注意：当该信号从标签栏发出时，`QTabWidget`会自动移动页面。

### `QRect QTabBar::tabRect(int index) const`

**作用与语义：**

返回标签在`index`位置的视觉矩形，若`index`隐藏或超出范围则返回空矩形。

### `[virtual protected] void QTabBar::tabRemoved(int index)`

**作用与语义：**

该虚拟处理程序是在从`index`位置移除标签页后调用的。

### `[virtual protected] QSize QTabBar::tabSizeHint(int index) const`

**作用与语义：**

返回位置`index`的标签大小提示。

### `QString QTabBar::tabText(int index) const`

**作用与语义：**

返回位置`index`的制表符文本，若`index`超出范围则返回空字符串。

### `QColor QTabBar::tabTextColor(int index) const`

**作用与语义：**

返回带有指定`index`的标签页的文本颜色，如果`index`超出范围则返回无效颜色。

### `QString QTabBar::tabToolTip(int index) const`

**作用与语义：**

返回标签工具尖端，位置`index`，或者如果超出`index`范围，则返回空字符串。

### `QString QTabBar::tabWhatsThis(int index) const`

**作用与语义：**

返回标签页在位置`index`的“这是怎么回事”帮助文本，或者如果`index`超出范围，则返回空字符串。

### `[override virtual protected] void QTabBar::timerEvent(QTimerEvent *event)`

**作用与语义：**

重实现自：`QObject::timerEvent`（QTimerEvent *event）。

### `[override virtual protected] void QTabBar::wheelEvent(QWheelEvent *event)`

**作用与语义：**

重实现自：`QWidget::wheelEvent`（QWheelEvent *event）。
该事件处理程序用于事件`event`，可以在子类中重新实现，以接收该控件的轮事件。
如果你重新实现了这个处理程序，非常重要的是，如果你不处理事件，必须`ignore()`事件，这样小部件的父节点才能解释它。
默认实现会忽略该事件。

### `bool autoHide() const`

**作用与语义：**

如果属实，当标签栏少于2个标签时会自动隐藏。
默认情况下，该属性为假。

**如何使用：** 调用 `autoHide()` 读取当前值；它不会修改应用状态。

### `bool changeCurrentOnDrag() const`

**作用与语义：**

如果是这样，那么拖动标签栏时当前标签页会自动更换。
注意：你还应将acceptDrops属性设置为true，才能使此功能正常工作。
默认情况下，该属性为假。

**如何使用：** 调用 `changeCurrentOnDrag()` 读取当前值；它不会修改应用状态。

### `int count() const`

**作用与语义：**

该属性包含标签栏中的标签数量。

**如何使用：** 调用 `count()` 读取当前值；它不会修改应用状态。

### `int currentIndex() const`

**作用与语义：**

该属性保留了标签栏可见标签的索引。
如果没有当前标签，当前索引为-1。

**如何使用：** 调用 `currentIndex()` 读取当前值；它不会修改应用状态。

### `bool documentMode() const`

**作用与语义：**

无论制表栏是否以适合主窗口的模式渲染，该属性都适用。
这个属性被用作样式的提示，让它们以不同于标签控件中通常的样子绘制标签页。在macOS上，这看起来类似于Safari或Sierra的 Terminal.app 中的标签页。

**如何使用：** 调用 `documentMode()` 读取当前值；它不会修改应用状态。

### `bool drawBase() const`

**作用与语义：**

定义了是否应该绘制其底部。
如果成立，则`QTabBar`根据样式重叠绘制基底。否则只绘制标签。

**如何使用：** 调用 `drawBase()` 读取当前值；它不会修改应用状态。

### `Qt::TextElideMode elideMode() const`

**作用与语义：**

如何省略标签栏中的文字。
该属性控制在给定标签栏大小下空间不足时，如何省略项目。
默认情况下，数值取决于风格。

**如何使用：** 调用 `elideMode()` 读取当前值；它不会修改应用状态。

### `bool expanding() const`

**作用与语义：**

当 是 expand（扩展）时`QTabBar`会扩展标签页以利用空位。
默认情况下，这个数值是真实的。

**如何使用：** 调用 `expanding()` 读取当前值；它不会修改应用状态。

### `QSize iconSize() const`

**作用与语义：**

该属性保留了标签栏图标的大小。
默认值取决于样式。`iconSize` 是最大尺寸;图标较小的图标不会放大。

**如何使用：** 调用 `iconSize()` 读取当前值；它不会修改应用状态。

### `bool isMovable() const`

**作用与语义：**

该属性决定用户是否能在标签栏区域内移动标签页。
默认情况下，该属性为`false`;

**如何使用：** 调用 `isMovable()` 读取当前值；它不会修改应用状态。

### `QTabBar::SelectionBehavior selectionBehaviorOnRemove() const`

**作用与语义：**

如果被移除的标签页也是当前标签页，`removeTab`调用时哪个标签页应该设置为当前？
默认值是`SelectRightTab`。

**如何使用：** 调用 `selectionBehaviorOnRemove()` 读取当前值；它不会修改应用状态。

### `void setAutoHide(bool hide)`

**作用与语义：**

如果属实，当标签栏少于2个标签时会自动隐藏。
默认情况下，该属性为假。

**如何使用：** 调用 `setAutoHide(...)` 修改 `autoHide`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setChangeCurrentOnDrag(bool change)`

**作用与语义：**

如果是这样，那么拖动标签栏时当前标签页会自动更换。
注意：你还应将acceptDrops属性设置为true，才能使此功能正常工作。
默认情况下，该属性为假。

**如何使用：** 调用 `setChangeCurrentOnDrag(...)` 修改 `changeCurrentOnDrag`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setDocumentMode(bool set)`

**作用与语义：**

无论制表栏是否以适合主窗口的模式渲染，该属性都适用。
这个属性被用作样式的提示，让它们以不同于标签控件中通常的样子绘制标签页。在macOS上，这看起来类似于Safari或Sierra的 Terminal.app 中的标签页。

**如何使用：** 调用 `setDocumentMode(...)` 修改 `documentMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setDrawBase(bool drawTheBase)`

**作用与语义：**

定义了是否应该绘制其底部。
如果成立，则`QTabBar`根据样式重叠绘制基底。否则只绘制标签。

**如何使用：** 调用 `setDrawBase(...)` 修改 `drawBase`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setElideMode(Qt::TextElideMode mode)`

**作用与语义：**

如何省略标签栏中的文字。
该属性控制在给定标签栏大小下空间不足时，如何省略项目。
默认情况下，数值取决于风格。

**如何使用：** 调用 `setElideMode(...)` 修改 `elideMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setExpanding(bool enabled)`

**作用与语义：**

当 是 expand（扩展）时`QTabBar`会扩展标签页以利用空位。
默认情况下，这个数值是真实的。

**如何使用：** 调用 `setExpanding(...)` 修改 `expanding`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setIconSize(const QSize &size)`

**作用与语义：**

该属性保留了标签栏图标的大小。
默认值取决于样式。`iconSize` 是最大尺寸;图标较小的图标不会放大。

**如何使用：** 调用 `setIconSize(...)` 修改 `iconSize`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMovable(bool movable)`

**作用与语义：**

该属性决定用户是否能在标签栏区域内移动标签页。
默认情况下，该属性为`false`;

**如何使用：** 调用 `setMovable(...)` 修改 `movable`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setSelectionBehaviorOnRemove(QTabBar::SelectionBehavior behavior)`

**作用与语义：**

如果被移除的标签页也是当前标签页，`removeTab`调用时哪个标签页应该设置为当前？
默认值是`SelectRightTab`。

**如何使用：** 调用 `setSelectionBehaviorOnRemove(...)` 修改 `selectionBehaviorOnRemove`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setShape(QTabBar::Shape shape)`

**作用与语义：**

该属性表示标签栏中标签的形状。
该属性的可能值由 Shape 枚举描述。

**如何使用：** 调用 `setShape(...)` 修改 `shape`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTabsClosable(bool closable)`

**作用与语义：**

该属性决定了标签栏是否应该在每个标签页上放置关闭按钮。
当 tabsClosable 设置为 true 时，标签页左侧或右侧会出现关闭按钮，具体取决于样式。当按钮被直接点击，或在标签页任意位置收到鼠标中键点击时，信号`tabCloseRequested`会发出。
默认情况下，该值为假。

**如何使用：** 调用 `setTabsClosable(...)` 修改 `tabsClosable`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setUsesScrollButtons(bool useButtons)`

**作用与语义：**

该属性决定了当标签栏有很多标签时，是否应该使用按钮来滚动标签页。
当标签栏中标签页数量过多，标签栏可以选择放大大小或添加按钮，方便你滚动切换标签页。
默认情况下，数值取决于风格。

**如何使用：** 调用 `setUsesScrollButtons(...)` 修改 `usesScrollButtons`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QTabBar::Shape shape() const`

**作用与语义：**

该属性表示标签栏中标签的形状。
该属性的可能值由 Shape 枚举描述。

**如何使用：** 调用 `shape()` 读取当前值；它不会修改应用状态。

### `bool tabsClosable() const`

**作用与语义：**

该属性决定了标签栏是否应该在每个标签页上放置关闭按钮。
当 tabsClosable 设置为 true 时，标签页左侧或右侧会出现关闭按钮，具体取决于样式。当按钮被直接点击，或在标签页任意位置收到鼠标中键点击时，信号`tabCloseRequested`会发出。
默认情况下，该值为假。

**如何使用：** 调用 `tabsClosable()` 读取当前值；它不会修改应用状态。

### `bool usesScrollButtons() const`

**作用与语义：**

该属性决定了当标签栏有很多标签时，是否应该使用按钮来滚动标签页。
当标签栏中标签页数量过多，标签栏可以选择放大大小或添加按钮，方便你滚动切换标签页。
默认情况下，数值取决于风格。

**如何使用：** 调用 `usesScrollButtons()` 读取当前值；它不会修改应用状态。

### `void setCurrentIndex(int index)`

**作用与语义：**

该属性保留了标签栏可见标签的索引。
如果没有当前标签，当前索引为-1。

**如何使用：** 调用 `setCurrentIndex(...)` 修改 `currentIndex`；传入的新值会成为后续查询和相关界面行为所使用的值。

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

`QTabBar` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
