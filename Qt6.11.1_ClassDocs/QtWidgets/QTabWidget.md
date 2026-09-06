# QTabWidget

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QTabWidget` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QTabWidget` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QTabWidget>`
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

- `enum TabPosition { North, South, West, East }`
- `enum TabShape { Rounded, Triangular }`

### 属性

- `count : int`
- `currentIndex : int`
- `documentMode : bool`
- `elideMode : Qt::TextElideMode`
- `iconSize : QSize`
- `movable : bool`
- `tabBarAutoHide : bool`
- `tabPosition : TabPosition`
- `tabShape : TabShape`
- `tabsClosable : bool`
- `usesScrollButtons : bool`

### 公有函数

- `QTabWidget(QWidget *parent = nullptr)`
- `virtual ~QTabWidget()`
- `int addTab(QWidget *page, const QString &label)`
- `int addTab(QWidget *page, const QIcon &icon, const QString &label)`
- `void clear()`
- `QWidget * cornerWidget(Qt::Corner corner = Qt::TopRightCorner) const`
- `int count() const`
- `int currentIndex() const`
- `QWidget * currentWidget() const`
- `bool documentMode() const`
- `Qt::TextElideMode elideMode() const`
- `QSize iconSize() const`
- `int indexOf(const QWidget *w) const`
- `int insertTab(int index, QWidget *page, const QString &label)`
- `int insertTab(int index, QWidget *page, const QIcon &icon, const QString &label)`
- `bool isMovable() const`
- `bool isTabEnabled(int index) const`
- `bool isTabVisible(int index) const`
- `void removeTab(int index)`
- `void setCornerWidget(QWidget *widget, Qt::Corner corner = Qt::TopRightCorner)`
- `void setDocumentMode(bool set)`
- `void setElideMode(Qt::TextElideMode mode)`
- `void setIconSize(const QSize &size)`
- `void setMovable(bool movable)`
- `void setTabBarAutoHide(bool enabled)`
- `void setTabEnabled(int index, bool enable)`
- `void setTabIcon(int index, const QIcon &icon)`
- `void setTabPosition(QTabWidget::TabPosition position)`
- `void setTabShape(QTabWidget::TabShape s)`
- `void setTabText(int index, const QString &label)`
- `void setTabToolTip(int index, const QString &tip)`
- `void setTabVisible(int index, bool visible)`
- `void setTabWhatsThis(int index, const QString &text)`
- `void setTabsClosable(bool closeable)`
- `void setUsesScrollButtons(bool useButtons)`
- `QTabBar * tabBar() const`
- `bool tabBarAutoHide() const`
- `QIcon tabIcon(int index) const`
- `QTabWidget::TabPosition tabPosition() const`
- `QTabWidget::TabShape tabShape() const`
- `QString tabText(int index) const`
- `QString tabToolTip(int index) const`
- `QString tabWhatsThis(int index) const`
- `bool tabsClosable() const`
- `bool usesScrollButtons() const`
- `QWidget * widget(int index) const`

### 重实现的公有函数

- `virtual bool hasHeightForWidth() const override`
- `virtual int heightForWidth(int width) const override`
- `virtual QSize minimumSizeHint() const override`
- `virtual QSize sizeHint() const override`

### 公有槽函数

- `void setCurrentIndex(int index)`
- `void setCurrentWidget(QWidget *widget)`

### 信号

- `void currentChanged(int index)`
- `void tabBarClicked(int index)`
- `void tabBarDoubleClicked(int index)`
- `void tabCloseRequested(int index)`

### 保护函数

- `virtual void initStyleOption(QStyleOptionTabWidgetFrame *option) const`
- `void setTabBar(QTabBar *tb)`
- `virtual void tabInserted(int index)`
- `virtual void tabRemoved(int index)`

### 重实现的保护函数

- `virtual void changeEvent(QEvent *ev) override`
- `virtual bool event(QEvent *ev) override`
- `virtual void keyPressEvent(QKeyEvent *e) override`
- `virtual void paintEvent(QPaintEvent *event) override`
- `virtual void resizeEvent(QResizeEvent *e) override`
- `virtual void showEvent(QShowEvent *) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QTabWidget::TabPosition`

**作用与语义：**

该枚举类型定义了`QTabWidget`绘制制表列的位置：
- `QTabWidget::North`：`0`;标签画在页面上方。
- `QTabWidget::South`：`1`;标签画在页面下方。
- `QTabWidget::West`：`2`;标签画在页面左侧。
- `QTabWidget::East`：`3`;标签画在页面右侧。

### `enum QTabWidget::TabShape`

**作用与语义：**

这个枚举类型定义了标签的形状：
- `QTabWidget::Rounded`：`0`;标签采用圆润的外观。这是默认形状。
- `QTabWidget::Triangular`：`1`;标签呈三角形。

### `[read-only] count : int`

**作用与语义：**

该属性包含标签栏中的标签数量。
默认情况下，该属性的值为0。

**如何使用：** 调用 `count()` 读取当前值；它不会修改应用状态。

### `currentIndex : int`

**作用与语义：**

该属性表示当前标签页的索引位置。
如果没有当前控件，当前索引为-1。
默认情况下，该属性包含 -1，因为控件中最初没有标签页。

**如何使用：** 调用 `currentIndex()` 读取当前值；它不会修改应用状态。

### `documentMode : bool`

**作用与语义：**

该属性适用于标签小部件是否以适合文档页面的模式渲染。这与macOS上的文档模式相同。
当该属性被设置时，制表小部件框不会被渲染。该模式适合显示文档类页面，页面覆盖了大部分标签小部件区域。

**如何使用：** 调用 `documentMode()` 读取当前值；它不会修改应用状态。

### `elideMode : Qt::TextElideMode`

**作用与语义：**

如何省略标签栏中的文字。
该属性控制在给定标签栏大小下空间不足时，如何省略项目。
默认情况下，数值取决于风格。

**如何使用：** 调用 `elideMode()` 读取当前值；它不会修改应用状态。

### `iconSize : QSize`

**作用与语义：**

该属性保留了标签栏图标的大小。
默认值取决于样式。这是图标的最大尺寸。图标大小较小时不会放大。

**如何使用：** 调用 `iconSize()` 读取当前值；它不会修改应用状态。

### `movable : bool`

**作用与语义：**

该属性决定用户是否能在标签栏区域内移动标签页。
默认情况下，该属性为`false`;

**如何使用：** 调用 `movable()` 读取当前值；它不会修改应用状态。

### `tabBarAutoHide : bool`

**作用与语义：**

如果属实，当标签栏少于2个标签时会自动隐藏。
默认情况下，该属性为假。

**如何使用：** 调用 `tabBarAutoHide()` 读取当前值；它不会修改应用状态。

### `tabPosition : TabPosition`

**作用与语义：**

此属性保存此标签部件中标签的位置。
此属性的可能值由 `TabPosition` 枚举描述。
默认情况下，此属性设置为 `North`。

**如何使用：** 调用 `tabPosition()` 读取当前值；它不会修改应用状态。

### `tabShape : TabShape`

**作用与语义：**

该属性表示了该标签组件中标签的形状。
该属性的可能值有`QTabWidget::Rounded`（默认）或`QTabWidget::Triangular`。

**如何使用：** 调用 `tabShape()` 读取当前值；它不会修改应用状态。

### `tabsClosable : bool`

**作用与语义：**

该属性适用于是否自动在每个标签上添加关闭按钮。

**如何使用：** 调用 `tabsClosable()` 读取当前值；它不会修改应用状态。

### `usesScrollButtons : bool`

**作用与语义：**

该属性决定了当标签栏有很多标签时，是否应该使用按钮来滚动标签页。
当标签栏中标签页数量过多，标签栏可以选择放大大小或添加按钮，方便你滚动切换标签页。
默认情况下，数值取决于风格。

**如何使用：** 调用 `usesScrollButtons()` 读取当前值；它不会修改应用状态。

### `[explicit] QTabWidget::QTabWidget(QWidget *parent = nullptr)`

**作用与语义：**

构建带有父`parent`的标签小部件。

### `[virtual noexcept] QTabWidget::~QTabWidget()`

**作用与语义：**

会破坏标签小部件。

### `int QTabWidget::addTab(QWidget *page, const QString &label)`

**作用与语义：**

在标签组件中添加一个包含指定`page`和`label`的标签页，并在标签栏中返回该标签页的索引。`page`的所有权传递给`QTabWidget`。
如果标签`label`包含&符号，字母后面的字母作为标签的快捷方式，例如标签为“Bro&wse”，Alt W就成为快捷键，将焦点移到该标签上。
注意：如果你在 `show()` 后调用 addTab()，布局系统会尝试根据控件层级的变化调整，可能导致闪烁。为防止这种情况，你可以在更改前将 `QWidget::updatesEnabled` 属性设置为 false;记得在更改完成后将属性设置为 true，使控件再次接收绘图事件。

### `int QTabWidget::addTab(QWidget *page, const QIcon &icon, const QString &label)`

**作用与语义：**

将带有指定`page`、`icon`和`label`的标签添加到标签小部件，并在标签栏中返回该标签的索引。`page`的所有权传递给`QTabWidget`。
该函数与 addTab()相同，但增加了一个`icon`。

### `[override virtual protected] void QTabWidget::changeEvent(QEvent *ev)`

**作用与语义：**

重装：`QWidget::changeEvent`（QEvent *事件）。
该事件处理程序可以重新实现以处理状态变化。
该事件中被更改的状态可以通过提供的`event`检索。
变更事件包括：`QEvent::ToolBarChange`、`QEvent::ActivationChange`、`QEvent::EnabledChange`、`QEvent::FontChange`、`QEvent::StyleChange`、`QEvent::PaletteChange`、`QEvent::WindowTitleChange`、`QEvent::IconTextChange`、`QEvent::ModifiedChange`、`QEvent::MouseTrackingChange`、`QEvent::ParentChange`、`QEvent::WindowStateChange`、`QEvent::LanguageChange`、`QEvent::LocaleChange`、`QEvent::LayoutDirectionChange`、`QEvent::ReadOnlyChange`。

### `void QTabWidget::clear()`

**作用与语义：**

删除所有页面，但不删除它们。调用该函数相当于调用`removeTab()`直到标签控件为空。

### `QWidget *QTabWidget::cornerWidget(Qt::Corner corner = Qt::TopRightCorner) const`

**作用与语义：**

返回标签控件或`nullptr` `corner`中显示的控件。

### `[signal] void QTabWidget::currentChanged(int index)`

**作用与语义：**

该属性表示当前标签页的索引位置。
如果没有当前控件，当前索引为-1。
默认情况下，该属性包含 -1，因为控件中最初没有标签页。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `currentIndex` 的变化，不要把它当作普通函数主动调用。

### `QWidget *QTabWidget::currentWidget() const`

**作用与语义：**

返回当前由制表表对话框显示的页面指针。制表表对话框尽力确保该值永远不会是0（但如果你足够努力，它确实可能为0）。

### `[override virtual protected] bool QTabWidget::event(QEvent *ev)`

**作用与语义：**

重实现自：`QWidget::event`（QEvent *事件）。

### `[override virtual] bool QTabWidget::hasHeightForWidth() const`

**作用与语义：**

重装：`QWidget::hasHeightForWidth()` const.
如果小部件的首选高度取决于宽度，则返回`true`;否则返回`false`。

### `[override virtual] int QTabWidget::heightForWidth(int width) const`

**作用与语义：**

重实现自：`QWidget::heightForWidth`（内性 w） const.
返回该小部件的首选高度，基于宽度`w`。
如果该控件有布局，默认实现返回该布局的首选高度。如果没有布局，默认实现返回 -1，表示首选高度不依赖于宽度。

### `int QTabWidget::indexOf(const QWidget *w) const`

**作用与语义：**

返回小部件所占用页面的索引位置，`w`，如果找不到小部件则返回 -1。

### `[virtual protected] void QTabWidget::initStyleOption(QStyleOptionTabWidgetFrame *option) const`

**作用与语义：**

用这个`QTabWidget`的值初始化`option`。这种方法适用于子类需要一个`QStyleOptionTabWidgetFrame`但不想自己填写所有信息时。

### `int QTabWidget::insertTab(int index, QWidget *page, const QString &label)`

**作用与语义：**

在指定`index`插入带有指定`label`和`page`的标签页到标签小部件中，并在标签栏返回插入标签的索引。`page`的所有权传递给`QTabWidget`。
标签显示在标签页中，外观可能因标签小部件的配置而有所不同。
如果制表`label`包含和号符号，则用和号后面的字母作为制表表的快捷方式，例如标签为“Bro&wse”，则小号W成为快捷键，将焦点移到该制表符上。
如果`index`超出范围，则直接附加制表符。否则则插入指定位置。
如果在调用该函数前`QTabWidget`为空，新页面将成为当前页面。在索引大小于或等于当前索引处插入新标签页，会递增当前索引，但保留当前页面。
注意：如果你在`show()`后调用 insertTab()，布局系统会尝试调整控件层级的变化，可能导致闪烁。为防止这种情况，你可以在更改前将 `QWidget::updatesEnabled` 属性设置为 false;记得在更改完成后将属性设置为 true，使控件再次接收绘图事件。

### `int QTabWidget::insertTab(int index, QWidget *page, const QIcon &icon, const QString &label)`

**作用与语义：**

在指定`index`插入带有指定`label`、`page`和`icon`的标签页，并在标签栏返回插入标签的索引。`page`的所有权传递给`QTabWidget`。
该函数与 insertTab()相同，但增加了一个`icon`。

### `bool QTabWidget::isTabEnabled(int index) const`

**作用与语义：**

如果页面在位置`index`启用，返回`true`;否则返回`false`。

### `bool QTabWidget::isTabVisible(int index) const`

**作用与语义：**

如果位置`index`的页面可见，则返回真;否则返回假。

### `[override virtual protected] void QTabWidget::keyPressEvent(QKeyEvent *e)`

**作用与语义：**

重实现自：`QWidget::keyPressEvent`（QKeyEvent *event）。
该事件处理程序用于事件`event`，可以在子类中重新实现，以接收该控件的按键事件。
一个小部件必须调用`setFocusPolicy()`先接受焦点，并且必须有焦点才能接收按键事件。
如果你重新实现这个处理器，如果你不对密钥进行操作，务必调用基类实现。
默认实现会关闭弹出小部件，如果用户按下`QKeySequence::Cancel`的按键序列（通常是 Escape 键）。否则事件会被忽略，以便小部件的父节点能够解释。
注意`QKeyEvent`以 isAccepted() == true 开头，所以你不需要调用 `QKeyEvent::accept()`——只要你对该键执行时不要调用基类实现即可。

### `[override virtual] QSize QTabWidget::minimumSizeHint() const`

**作用与语义：**

重新实现了属性的访问函数：`QWidget::minimumSizeHint`。
返回标签小部件的合适最小大小。

### `[override virtual protected] void QTabWidget::paintEvent(QPaintEvent *event)`

**作用与语义：**

重实现自：`QWidget::paintEvent`（QPaintEvent *event）。
根据绘图`event`，绘制标签小部件的标签栏。
该事件处理程序可以在子类中重新实现，以接收 `event` 传递的绘画事件。
绘图事件是请求重新绘制一个小部件的全部或部分。它可能由以下原因之一发生：
- `repaint()`或`update()`被援引，
- 小部件被遮挡，现已被发现，或
- 还有很多其他原因。
许多控件在被要求时可以直接重新绘制整个表面，但一些速度较慢的控件需要通过只绘制请求的区域来优化：`QPaintEvent::region()`。这种速度优化不会改变结果，因为在事件处理过程中绘制会被裁剪到该区域。例如，`QListView`和`QTableView`就是这么做的。
Qt 还试图通过将多个绘画事件合并为一个来加快绘画速度。当 `update()` 被多次调用或窗口系统发送多个绘画事件时，Qt 会将这些事件合并为一个区域更大的事件（参见 `QRegion::united()`）。`repaint()` 函数不支持这种优化，因此我们建议尽可能使用 `update()`。
当绘制事件发生时，更新区域通常已经被擦除，所以你是在小部件的背景上作画。
背景可以用`setBackgroundRole()`和`setPalette()`设置。
自 Qt 4.0 起，`QWidget` 会自动对绘画进行双缓冲，因此无需在 paintEvent() 中编写双重缓冲代码以避免闪烁。
注意：通常，你应避免在 paintEvent() 中调用 `update()` 或 `repaint()`。例如，在 paintEvent() 中调用 Children `update()` 或 `repaint()` 会导致行为不明确;孩子可能会也可能不会获得 paint 事件。
警告：如果你使用没有 Qt backingstore 的自定义 paint 引擎，`Qt::WA_PaintOnScreen` 必须设置。否则，`QWidget::paintEngine()` 永远不会被调用;Backingstore 将被使用。

### `void QTabWidget::removeTab(int index)`

**作用与语义：**

从该控件堆栈中移除位置`index`的标签。页面控件本身并未被删除。

### `[override virtual protected] void QTabWidget::resizeEvent(QResizeEvent *e)`

**作用与语义：**

重实现自：`QWidget::resizeEvent`（QResizeEvent *event）。
该事件处理程序可以在子类中重新实现，以接收通过 `event` 参数传递的控件调整大小事件。当调用 resizeEvent() 时，控件已经拥有新的几何体。旧的大小可以通过 `QResizeEvent::oldSize()` 访问。
控件会被擦除，并在处理调整尺寸事件后立即接收绘图事件。不需要（也不应该）在这个处理程序中进行绘图。

### `void QTabWidget::setCornerWidget(QWidget *widget, Qt::Corner corner = Qt::TopRightCorner)`

**作用与语义：**

将给定的`widget`设置为在标签控件指定的`corner`中显示。控件的几何形状基于控件的`sizeHint()`和`style()`确定。
只使用`corner`的水平部分。
经过`nullptr`时，角落里没有小部件。
任何之前设置的角落控件都被隐藏了。
当标签小部件被销毁时，所有设置在这里设置的小部件都会被删除，除非你在设置其他角落小部件（或`nullptr`）后单独重新父级该小部件。
注意：角落小部件设计用于`North`和`South`制表位置;其他方向已知无法正常工作。

### `[slot] void QTabWidget::setCurrentWidget(QWidget *widget)`

**作用与语义：**

`widget`当前的小部件。使用的`widget`必须是该标签小部件中的页面。

### `[protected] void QTabWidget::setTabBar(QTabBar *tb)`

**作用与语义：**

用标签栏`tb`替换对话的`QTabBar`标题。注意，必须在添加任何标签之前调用，否则行为未定义。

### `void QTabWidget::setTabEnabled(int index, bool enable)`

**作用与语义：**

如果`enable`为真，则位置`index`的页面被启用;否则位置`index`的页面被禁用。页面的标签符会被适当重新绘制。
`QTabWidget`内部使用`QWidget::setEnabled()`，而不是单独使用标志。
请注意，即使是禁用的标签页/页面也可能被看到。如果页面已经可见，`QTabWidget`不会隐藏它;如果所有页面都被禁用，`QTabWidget`会显示其中一个页面。

### `void QTabWidget::setTabIcon(int index, const QIcon &icon)`

**作用与语义：**

将标签的 `icon` 设置在位置 `index`。

### `void QTabWidget::setTabText(int index, const QString &label)`

**作用与语义：**

在位置`index`的标签页定义了新的`label`。
如果提供的文本包含一个&字符（'&'），会自动为其创建一个快捷方式。紧跟在'&'之后的字符将作为快捷键使用。任何之前的快捷方式都会被覆盖，或者如果文本中没有定义快捷方式，则会被清除。详情请参见`QShortcut`文档（要显示实际的&&，请使用'&&'）。

### `void QTabWidget::setTabToolTip(int index, const QString &tip)`

**作用与语义：**

将页面位置`index`的制表工具提示设置为`tip`。

### `void QTabWidget::setTabVisible(int index, bool visible)`

**作用与语义：**

如果`visible`为真，位置`index`的页面是可见的;否则位置`index`的页面是隐藏的。页面的标签会相应地重新绘制。

### `void QTabWidget::setTabWhatsThis(int index, const QString &text)`

**作用与语义：**

将页面位置`index`的“这是怎么回事”帮助文本设置为`text`。

### `[override virtual protected] void QTabWidget::showEvent(QShowEvent *)`

**作用与语义：**

重实现自：`QWidget::showEvent`（QShowEvent *event）。
该事件处理程序可以在子类中重新实现，以接收传递给 `event` 参数的控件显示事件。
非自发的展示事件会在展示前立即发送到小部件。窗口的自发展示事件则在展示之后交付。
注意：当窗口系统改变其映射状态时，小部件会接收自发显示和隐藏事件，例如用户最小化窗口时自发隐藏事件，窗口恢复时自发显示事件。收到自发隐藏事件后，小部件仍被视为`isVisible()`可见。

### `[override virtual] QSize QTabWidget::sizeHint() const`

**作用与语义：**

重新实现了属性的访问函数：`QWidget::sizeHint`。

### `QTabBar *QTabWidget::tabBar() const`

**作用与语义：**

返回当前`QTabBar`。

### `[signal] void QTabWidget::tabBarClicked(int index)`

**作用与语义：**

当用户点击`index`的标签页时，会发出该信号。
`index`指点击的标签，或者如果光标下方没有标签，则表示-1。

### `[signal] void QTabWidget::tabBarDoubleClicked(int index)`

**作用与语义：**

当用户在`index`双击标签页时，会发出该信号。
`index` 是点击的标签的索引，或者如果光标下方没有标签，则是 -1。

### `[signal] void QTabWidget::tabCloseRequested(int index)`

**作用与语义：**

当点击标签页上的关闭按钮时，会发出这个信号。`index`是应该移除的索引。

### `QIcon QTabWidget::tabIcon(int index) const`

**作用与语义：**

返回页面`index`位置标签的图标。

### `[virtual protected] void QTabWidget::tabInserted(int index)`

**作用与语义：**

在添加或插入新标签页到位置`index`后调用该虚拟处理器。

### `[virtual protected] void QTabWidget::tabRemoved(int index)`

**作用与语义：**

该虚拟处理程序是在从`index`位置移除标签页后调用的。

### `QString QTabWidget::tabText(int index) const`

**作用与语义：**

返回页面位置`index`标签的标签文本。

### `QString QTabWidget::tabToolTip(int index) const`

**作用与语义：**

返回页面位置`index`的标签工具提示，若未设置工具提示则返回空字符串。

### `QString QTabWidget::tabWhatsThis(int index) const`

**作用与语义：**

返回页面位置`index`的“What's This help”文本，若未设置帮助文本则返回空字符串。

### `QWidget *QTabWidget::widget(int index) const`

**作用与语义：**

如果`index`超出范围，则返回索引`index`或`nullptr`的标签页。

### `int count() const`

**作用与语义：**

该属性包含标签栏中的标签数量。
默认情况下，该属性的值为0。

**如何使用：** 调用 `count()` 读取当前值；它不会修改应用状态。

### `int currentIndex() const`

**作用与语义：**

该属性表示当前标签页的索引位置。
如果没有当前控件，当前索引为-1。
默认情况下，该属性包含 -1，因为控件中最初没有标签页。

**如何使用：** 调用 `currentIndex()` 读取当前值；它不会修改应用状态。

### `bool documentMode() const`

**作用与语义：**

该属性适用于标签小部件是否以适合文档页面的模式渲染。这与macOS上的文档模式相同。
当该属性被设置时，制表小部件框不会被渲染。该模式适合显示文档类页面，页面覆盖了大部分标签小部件区域。

**如何使用：** 调用 `documentMode()` 读取当前值；它不会修改应用状态。

### `Qt::TextElideMode elideMode() const`

**作用与语义：**

如何省略标签栏中的文字。
该属性控制在给定标签栏大小下空间不足时，如何省略项目。
默认情况下，数值取决于风格。

**如何使用：** 调用 `elideMode()` 读取当前值；它不会修改应用状态。

### `QSize iconSize() const`

**作用与语义：**

该属性保留了标签栏图标的大小。
默认值取决于样式。这是图标的最大尺寸。图标大小较小时不会放大。

**如何使用：** 调用 `iconSize()` 读取当前值；它不会修改应用状态。

### `bool isMovable() const`

**作用与语义：**

该属性决定用户是否能在标签栏区域内移动标签页。
默认情况下，该属性为`false`;

**如何使用：** 调用 `isMovable()` 读取当前值；它不会修改应用状态。

### `void setDocumentMode(bool set)`

**作用与语义：**

该属性适用于标签小部件是否以适合文档页面的模式渲染。这与macOS上的文档模式相同。
当该属性被设置时，制表小部件框不会被渲染。该模式适合显示文档类页面，页面覆盖了大部分标签小部件区域。

**如何使用：** 调用 `setDocumentMode(...)` 修改 `documentMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setElideMode(Qt::TextElideMode mode)`

**作用与语义：**

如何省略标签栏中的文字。
该属性控制在给定标签栏大小下空间不足时，如何省略项目。
默认情况下，数值取决于风格。

**如何使用：** 调用 `setElideMode(...)` 修改 `elideMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setIconSize(const QSize &size)`

**作用与语义：**

该属性保留了标签栏图标的大小。
默认值取决于样式。这是图标的最大尺寸。图标大小较小时不会放大。

**如何使用：** 调用 `setIconSize(...)` 修改 `iconSize`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMovable(bool movable)`

**作用与语义：**

该属性决定用户是否能在标签栏区域内移动标签页。
默认情况下，该属性为`false`;

**如何使用：** 调用 `setMovable(...)` 修改 `movable`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTabBarAutoHide(bool enabled)`

**作用与语义：**

如果属实，当标签栏少于2个标签时会自动隐藏。
默认情况下，该属性为假。

**如何使用：** 调用 `setTabBarAutoHide(...)` 修改 `tabBarAutoHide`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTabPosition(QTabWidget::TabPosition position)`

**作用与语义：**

此属性保存此标签部件中标签的位置。
此属性的可能值由 `TabPosition` 枚举描述。
默认情况下，此属性设置为 `North`。

**如何使用：** 调用 `setTabPosition(...)` 修改 `tabPosition`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTabShape(QTabWidget::TabShape s)`

**作用与语义：**

该属性表示了该标签组件中标签的形状。
该属性的可能值有`QTabWidget::Rounded`（默认）或`QTabWidget::Triangular`。

**如何使用：** 调用 `setTabShape(...)` 修改 `tabShape`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTabsClosable(bool closeable)`

**作用与语义：**

该属性适用于是否自动在每个标签上添加关闭按钮。

**如何使用：** 调用 `setTabsClosable(...)` 修改 `tabsClosable`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setUsesScrollButtons(bool useButtons)`

**作用与语义：**

该属性决定了当标签栏有很多标签时，是否应该使用按钮来滚动标签页。
当标签栏中标签页数量过多，标签栏可以选择放大大小或添加按钮，方便你滚动切换标签页。
默认情况下，数值取决于风格。

**如何使用：** 调用 `setUsesScrollButtons(...)` 修改 `usesScrollButtons`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `bool tabBarAutoHide() const`

**作用与语义：**

如果属实，当标签栏少于2个标签时会自动隐藏。
默认情况下，该属性为假。

**如何使用：** 调用 `tabBarAutoHide()` 读取当前值；它不会修改应用状态。

### `QTabWidget::TabPosition tabPosition() const`

**作用与语义：**

此属性保存此标签部件中标签的位置。
此属性的可能值由 `TabPosition` 枚举描述。
默认情况下，此属性设置为 `North`。

**如何使用：** 调用 `tabPosition()` 读取当前值；它不会修改应用状态。

### `QTabWidget::TabShape tabShape() const`

**作用与语义：**

该属性表示了该标签组件中标签的形状。
该属性的可能值有`QTabWidget::Rounded`（默认）或`QTabWidget::Triangular`。

**如何使用：** 调用 `tabShape()` 读取当前值；它不会修改应用状态。

### `bool tabsClosable() const`

**作用与语义：**

该属性适用于是否自动在每个标签上添加关闭按钮。

**如何使用：** 调用 `tabsClosable()` 读取当前值；它不会修改应用状态。

### `bool usesScrollButtons() const`

**作用与语义：**

该属性决定了当标签栏有很多标签时，是否应该使用按钮来滚动标签页。
当标签栏中标签页数量过多，标签栏可以选择放大大小或添加按钮，方便你滚动切换标签页。
默认情况下，数值取决于风格。

**如何使用：** 调用 `usesScrollButtons()` 读取当前值；它不会修改应用状态。

### `void setCurrentIndex(int index)`

**作用与语义：**

该属性表示当前标签页的索引位置。
如果没有当前控件，当前索引为-1。
默认情况下，该属性包含 -1，因为控件中最初没有标签页。

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

`QTabWidget` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
