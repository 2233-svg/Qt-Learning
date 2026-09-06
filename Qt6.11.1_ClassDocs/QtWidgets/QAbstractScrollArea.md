# QAbstractScrollArea

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QAbstractScrollArea` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QAbstractScrollArea` 是 Qt Widgets 中的抽象协议类型，通常通过具体子类、模型、插件或工厂来使用。

**内部模型：** 抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

**适用场景：** 当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。

**典型调用链：** 选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。

**先记住的坑：** 不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

## 2. 依赖与对象关系

- 头文件：`#include <QAbstractScrollArea>`
- 继承自：QFrame
- 直接派生类：QAbstractItemView、QGraphicsView、QMdiArea、QPlainTextEdit、QScrollArea,、QTextEdit

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

### 状态、生命周期和线程

**生命周期：** 控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

**状态与结果：** 控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

**线程与事件循环：** 所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

## 3. 直接使用

当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。 使用时通常按这个过程组织：选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum SizeAdjustPolicy { AdjustIgnored, AdjustToContents, AdjustToContentsOnFirstShow }`

### 属性

- `horizontalScrollBarPolicy : Qt::ScrollBarPolicy`
- `sizeAdjustPolicy : SizeAdjustPolicy`
- `verticalScrollBarPolicy : Qt::ScrollBarPolicy`

### 公有函数

- `QAbstractScrollArea(QWidget *parent = nullptr)`
- `virtual ~QAbstractScrollArea()`
- `void addScrollBarWidget(QWidget *widget, Qt::Alignment alignment)`
- `QWidget * cornerWidget() const`
- `QScrollBar * horizontalScrollBar() const`
- `Qt::ScrollBarPolicy horizontalScrollBarPolicy() const`
- `QSize maximumViewportSize() const`
- `QWidgetList scrollBarWidgets(Qt::Alignment alignment)`
- `void setCornerWidget(QWidget *widget)`
- `void setHorizontalScrollBar(QScrollBar *scrollBar)`
- `void setHorizontalScrollBarPolicy(Qt::ScrollBarPolicy)`
- `void setSizeAdjustPolicy(QAbstractScrollArea::SizeAdjustPolicy policy)`
- `void setVerticalScrollBar(QScrollBar *scrollBar)`
- `void setVerticalScrollBarPolicy(Qt::ScrollBarPolicy)`
- `void setViewport(QWidget *widget)`
- `virtual void setupViewport(QWidget *viewport)`
- `QAbstractScrollArea::SizeAdjustPolicy sizeAdjustPolicy() const`
- `QScrollBar * verticalScrollBar() const`
- `Qt::ScrollBarPolicy verticalScrollBarPolicy() const`
- `QWidget * viewport() const`

### 重实现的公有函数

- `virtual QSize minimumSizeHint() const override`
- `virtual QSize sizeHint() const override`

### 保护函数

- `virtual void scrollContentsBy(int dx, int dy)`
- `void setViewportMargins(const QMargins &margins)`
- `void setViewportMargins(int left, int top, int right, int bottom)`
- `virtual bool viewportEvent(QEvent *event)`
- `QMargins viewportMargins() const`
- `virtual QSize viewportSizeHint() const`

### 重实现的保护函数

- `virtual void contextMenuEvent(QContextMenuEvent *e) override`
- `virtual void dragEnterEvent(QDragEnterEvent *event) override`
- `virtual void dragLeaveEvent(QDragLeaveEvent *event) override`
- `virtual void dragMoveEvent(QDragMoveEvent *event) override`
- `virtual void dropEvent(QDropEvent *event) override`
- `virtual bool event(QEvent *event) override`
- `virtual void keyPressEvent(QKeyEvent *e) override`
- `virtual void mouseDoubleClickEvent(QMouseEvent *e) override`
- `virtual void mouseMoveEvent(QMouseEvent *e) override`
- `virtual void mousePressEvent(QMouseEvent *e) override`
- `virtual void mouseReleaseEvent(QMouseEvent *e) override`
- `virtual void paintEvent(QPaintEvent *event) override`
- `virtual void resizeEvent(QResizeEvent *event) override`
- `virtual void wheelEvent(QWheelEvent *e) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QAbstractScrollArea::SizeAdjustPolicy`

**作用与语义：**

该枚举规定了当视口大小变化时，`QAbstractScrollArea`的尺寸提示应如何调整。
- `QAbstractScrollArea::AdjustIgnored`：`0`;滚动区域将保持之前的行为，不会进行任何调整。
- `QAbstractScrollArea::AdjustToContents`：`2`;滚动区域始终会根据视口调整
- `QAbstractScrollArea::AdjustToContentsOnFirstShow`：`1`;滚动区域在首次显示时会调整为其视口。

### `horizontalScrollBarPolicy : Qt::ScrollBarPolicy`

**作用与语义：**

此属性保存水平滚动条的策略。
默认策略是 `Qt::ScrollBarAsNeeded`。

**如何使用：** 调用 `horizontalScrollBarPolicy()` 读取当前值；它不会修改应用状态。

### `sizeAdjustPolicy : SizeAdjustPolicy`

**作用与语义：**

此属性保存描述当视口大小变化时滚动区域如何变化的策略。
默认策略是 `QAbstractScrollArea::AdjustIgnored`。更改此属性可能实际上会调整滚动区域的大小。

**如何使用：** 调用 `sizeAdjustPolicy()` 读取当前值；它不会修改应用状态。

### `verticalScrollBarPolicy : Qt::ScrollBarPolicy`

**作用与语义：**

此属性保存垂直滚动条的策略。
默认策略是 `Qt::ScrollBarAsNeeded`。

**如何使用：** 调用 `verticalScrollBarPolicy()` 读取当前值；它不会修改应用状态。

### `[explicit] QAbstractScrollArea::QAbstractScrollArea(QWidget *parent = nullptr)`

**作用与语义：**

搭建了一个视窗。
`parent`参数被发送给`QWidget`构造器。

### `[virtual noexcept] QAbstractScrollArea::~QAbstractScrollArea()`

**作用与语义：**

毁掉了视窗。

### `void QAbstractScrollArea::addScrollBarWidget(QWidget *widget, Qt::Alignment alignment)`

**作用与语义：**

在`alignment`指定的位置添加`widget`滚动条小部件。
滚动条控件显示在水平或垂直滚动条旁边，可以放置在其任一侧。如果你希望滚动条控件始终可见，请将相应滚动条的滚动条Policy设置为`AlwaysOn`。
`alignment`必须是Qt：：alignleft和`Qt::AlignRight`之一，后者映射到水平滚动条，或者映射到垂直滚动条的`Qt::AlignTop`和`Qt::AlignBottom`。
滚动条小部件可以通过重新父级或删除小部件来移除。也可以用`QWidget::hide()`隐藏小部件。
滚动条小部件将根据当前样式调整大小以适应滚动条几何形状。以下描述了横向滚动条小部件的情形：
小部件的高度将设置为与滚动条的高度相匹配。要控制小部件的宽度，可以使用`QWidget::setMinimumWidth`和`QWidget::setMaximumWidth`，或者实现`QWidget::sizeHint()`并设置水平大小策略。如果你想要一个方形小部件，可以调用`QStyle::pixelMetric`（`QStyle::PM_ScrollBarExtent`）并将宽度设置为这个值。

### `[override virtual protected] void QAbstractScrollArea::contextMenuEvent(QContextMenuEvent *e)`

**作用与语义：**

重实现自：`QWidget::contextMenuEvent`（QContextMenuEvent *event）。
该事件处理程序可以在子类中重新实现，以接收`viewport()`控件的上下文菜单事件。事件会以`e`传递。
该事件处理程序用于事件`event`，可以重新实现为子类以接收控件上下文菜单事件。
当控件的 `contextMenuPolicy` `Qt::DefaultContextMenu`时调用处理器。
默认实现忽略上下文事件。详情请参见`QContextMenuEvent`文档。

### `QWidget *QAbstractScrollArea::cornerWidget() const`

**作用与语义：**

返回两个滚动条之间角落的小部件。
默认情况下，没有角落小部件。

### `[override virtual protected] void QAbstractScrollArea::dragEnterEvent(QDragEnterEvent *event)`

**作用与语义：**

重实现自：`QWidget::dragEnterEvent`（QDragEnterEvent *event）。
该事件处理程序可以被重新实现为子类，以接收`event`传递的拖入事件，用于`viewport()`小部件。
当拖拽进行中且鼠标进入该控件时，调用该事件处理程序。事件通过`event`参数传递。
如果事件被忽略，小部件将不会接收任何拖动动作事件。
请参阅拖放文档，了解如何在申请中提供拖放功能的概览。

### `[override virtual protected] void QAbstractScrollArea::dragLeaveEvent(QDragLeaveEvent *event)`

**作用与语义：**

重实现自：`QWidget::dragLeaveEvent`（QDragLeaveEvent *event）。
该事件处理程序可以被重新实现为子类，以接收`event`传递的拖曳离开事件，用于`viewport()`小部件。
当拖拽进行且鼠标离开该控件时，调用该事件处理程序。事件通过`event`参数传递。
请参阅拖放文档，了解如何在申请中提供拖放功能的概览。

### `[override virtual protected] void QAbstractScrollArea::dragMoveEvent(QDragMoveEvent *event)`

**作用与语义：**

重实现自：`QWidget::dragMoveEvent`（QDragMoveEvent *event）。
该事件处理程序可以被重新实现到子类中，以接收`viewport()` widget 的拖动移动事件（在 `event` 中传递）。
当拖拽正在进行中，且发生以下任一条件时，会调用该事件处理程序：光标进入该控件、光标在控件内移动，或在控件拥有焦点时按下键盘上的修饰键。事件通过`event`参数传递。
请参阅拖放文档，了解如何在申请中提供拖放功能的概览。

### `[override virtual protected] void QAbstractScrollArea::dropEvent(QDropEvent *event)`

**作用与语义：**

重实现自：`QWidget::dropEvent`（QDropEvent *event）。
该事件处理程序可以在子类中重新实现，以接收`viewport()`小部件的 drop 事件（`event`传递）。
当拖拽该控件被调用时，该事件处理程序被调用。事件通过`event`参数传递。
请参阅拖放文档，了解如何在申请中提供拖放功能的概览。

### `[override virtual protected] bool QAbstractScrollArea::event(QEvent *event)`

**作用与语义：**

重实现自：`QFrame::event`（QEvent *e）。
这是`QAbstractScrollArea`小部件的主事件处理程序（不是滚动区域`viewport()`）。指定的`event`是一个通用事件对象，根据类型可能需要转换为相应的类。

### `QScrollBar *QAbstractScrollArea::horizontalScrollBar() const`

**作用与语义：**

返回横向滚动条。

### `[override virtual protected] void QAbstractScrollArea::keyPressEvent(QKeyEvent *e)`

**作用与语义：**

重实现自：`QWidget::keyPressEvent`（QKeyEvent *event）。
当按键发生时，该函数会在按键事件`e`时调用。它处理 PageUp、PageDown、Up、Down、Left、Right 四个键，忽略所有其他按键操作。
该事件处理程序用于事件`event`，可以在子类中重新实现，以接收该小部件的按键事件。
小部件必须调用`setFocusPolicy()`先接受焦点，并且必须拥有焦点才能接收按键事件。
如果你重新实现这个处理器，如果你不对密钥进行操作，务必调用基类实现。
默认实现会关闭弹出式小部件，如果用户按下`QKeySequence::Cancel`的按键序列（通常是Escape键）。否则事件会被忽略，以便小部件的父节点能够解释。
注意`QKeyEvent`以 isAccepted() == true() 开头，所以你不需要调用 `QKeyEvent::accept()`——只要你对密钥执行时不要调用基类实现即可。

### `QSize QAbstractScrollArea::maximumViewportSize() const`

**作用与语义：**

返回视口大小，就像滚动条没有有效的滚动范围一样。

### `[override virtual] QSize QAbstractScrollArea::minimumSizeHint() const`

**作用与语义：**

重新实现属性的访问函数：`QWidget::minimumSizeHint`。

### `[override virtual protected] void QAbstractScrollArea::mouseDoubleClickEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QWidget::mouseDoubleClickEvent`（QMouseEvent *event）。
该事件处理程序可以被重新实现为子类，以接收`viewport()` widget 的鼠标双击事件。事件会在`e`传递。
该事件处理程序用于事件`event`，可以重新实现为子类，以接收该小部件的鼠标双击事件。
默认实现调用`mousePressEvent()`。
注意：该小部件除了双击事件外，还会接收鼠标按键和鼠标释放事件。如果与该小部件重叠的其他小部件在新闻发布事件后消失，则该小部件只会接收双击事件。开发者有责任确保应用程序正确解读这些事件。

### `[override virtual protected] void QAbstractScrollArea::mouseMoveEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QWidget::mouseMoveEvent`（QMouseEvent *event）。
该事件处理程序可以被重新实现为子类，以接收`viewport()`小部件的鼠标移动事件。事件会在`e`传递。
该事件处理程序用于事件`event`，可以在子类中重新实现，以接收该小部件的鼠标移动事件。
如果关闭鼠标追踪，只有在鼠标移动过程中按下鼠标按钮时才会发生鼠标移动事件。如果开启鼠标追踪，即使未按键，鼠标移动事件也会发生。
`QMouseEvent::position()` 报告鼠标光标相对于该小部件的位置。对于按下和释放事件，位置通常与最后一次鼠标移动事件的位置相同，但如果用户握手，位置可能会有所不同。这是底层窗口系统的功能，而非 Qt。
如果你想在鼠标移动时立即显示提示（例如，获取鼠标坐标与`QMouseEvent::position()`并以提示形式显示），你必须先启用上述描述的鼠标追踪功能。然后，为了确保提示立即更新，你必须在鼠标MoveEvent()实现中调用`QToolTip::showText()`而不是`setToolTip()`。

### `[override virtual protected] void QAbstractScrollArea::mousePressEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QWidget::mousePressEvent`（QMouseEvent *event）。
该事件处理程序可以被重新实现为子类，以接收`viewport()`小部件的鼠标按键事件。事件会在`e`中传递。
默认实现调用`QWidget::mousePressEvent()`，用于默认弹出处理。
该事件处理程序用于事件`event`，可以在子类中重新实现，以接收该控件的鼠标按键事件。
如果你在 mousePressEvent() 创建新控件，`mouseReleaseEvent()`可能不会到达你预期的位置，这取决于底层窗口系统（或 X11 窗口管理器）、控件的位置，甚至可能还有其他因素。
默认实现实现了当你点击窗口外时关闭弹出小部件的功能。对于其他小部件类型，它没有任何作用。

### `[override virtual protected] void QAbstractScrollArea::mouseReleaseEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QWidget::mouseReleaseEvent`（QMouseEvent *event）。
该事件处理程序可以被重新实现为子类，以接收`viewport()`小部件的鼠标释放事件。事件会在`e`传递。
该事件处理程序用于事件`event`，可以在子类中重新实现，以接收该控件的鼠标释放事件。

### `[override virtual protected] void QAbstractScrollArea::paintEvent(QPaintEvent *event)`

**作用与语义：**

重实现自：`QFrame::paintEvent`（QPaintEvent *）。
该事件处理程序可以被重新实现为子类，以接收 `viewport()` 控件的绘画事件（在 `event` 中传递）。
注意：如果你创建`QPainter`，它必须在`viewport()`上操作。

### `[override virtual protected] void QAbstractScrollArea::resizeEvent(QResizeEvent *event)`

**作用与语义：**

重实现自：`QWidget::resizeEvent`（QResizeEvent *event）。
该事件处理程序可以在子类中重新实现，以接收`viewport()`小部件的调整大小事件（传递在`event`中）。
当调用 resizeEvent() 时，视口已经拥有新的几何体：新大小可通过 `QResizeEvent::size()` 函数访问，旧大小可通过 `QResizeEvent::oldSize()` 访问。
该事件处理程序可在子类中重新实现，以接收 `event` 参数中传递的控件调整大小事件。当调用 resizeEvent() 时，控件已有新的几何体。旧尺寸可通过 `QResizeEvent::oldSize()` 访问。
控件会被擦除，并在处理调整尺寸事件后立即接收绘图事件。不需要（也不应该）在这个处理程序中进行绘图。

### `QWidgetList QAbstractScrollArea::scrollBarWidgets(Qt::Alignment alignment)`

**作用与语义：**

返回当前设置的滚动条控件列表。`alignment`可以是四个位置标志的任意组合。

### `[virtual protected] void QAbstractScrollArea::scrollContentsBy(int dx, int dy)`

**作用与语义：**

当滚动条被`dx`、`dy`移动时调用了这个虚拟处理程序，因此应相应地滚动视口的内容。
默认实现只需调用整个`viewport()`的`update()`，子类可以重新实现该处理程序以优化，或者像`QScrollArea`一样移动内容控件。参数`dx`和`dy`是为了方便，让类知道应该滚动多少（比如像素移动时很有用）。你也可以忽略这些值，直接滚动到滚动条指示的位置。
调用该函数以进行程序滚动是错误的，建议使用滚动条（例如直接调用`QScrollBar::setValue()`）。

### `void QAbstractScrollArea::setCornerWidget(QWidget *widget)`

**作用与语义：**

将两个滚动条之间角落的小部件设置为`widget`。
你可能还需要至少将其中一个滚动条模式设置为`AlwaysOn`。
经过`nullptr`时，角落里没有小部件。
之前的角落小部件都被隐藏了。
你可以在不同时间调用 setCornerWidget()，使用相同的 widget。
当滚动区域被销毁时，所有设置在这里设置的小部件都会被删除，除非你在设置其他角落小部件（或`nullptr`）后单独重新子护该小部件。
任何新设置的小部件都应该没有当前的父组件。
默认情况下，没有角落小部件。

### `void QAbstractScrollArea::setHorizontalScrollBar(QScrollBar *scrollBar)`

**作用与语义：**

用`scrollBar`替换现有的横向滚动条，并将所有原滚动条的滑块属性设置到新的滚动条上。随后，原滚动条被删除。
`QAbstractScrollArea`默认已经提供水平和垂直滚动条。你可以调用这个功能，用自定义的滚动条替换默认的水平滚动条。

### `void QAbstractScrollArea::setVerticalScrollBar(QScrollBar *scrollBar)`

**作用与语义：**

用`scrollBar`替换现有的垂直滚动条，并将所有原滚动条的滑块属性设置到新的滚动条上。随后，原滚动条被删除。
`QAbstractScrollArea`默认已经提供了垂直和水平滚动条。你可以调用这个函数，用你自己的自定义滚动条替换默认的垂直滚动条。

### `void QAbstractScrollArea::setViewport(QWidget *widget)`

**作用与语义：**

将视口设置为给定的`widget`。`QAbstractScrollArea`将拥有给定的`widget`。
如果`widget` `nullptr`，`QAbstractScrollArea`会为视口分配一个新的`QWidget`实例。

### `[protected] void QAbstractScrollArea::setViewportMargins(const QMargins &margins)`

**作用与语义：**

在滚动区域周围`margins`集合。这对于像电子表格中行和列“锁定”的应用非常有用。边际空间留空;将小部件放在未使用的区域。
默认情况下，所有边距都是零。

### `[protected] void QAbstractScrollArea::setViewportMargins(int left, int top, int right, int bottom)`

**作用与语义：**

将滚动区域周围的边距设置为`left`、`top`、`right`和`bottom`。这对于像电子表格中行列“锁定”的应用非常有用。边际空白保持空白;将小部件放入未使用的区域。
注意，该函数经常被`QTreeView`和 `QTableView`调用，因此边距必须由`QAbstractScrollArea`子类实现。此外，如果子类要用于项目视图，不应调用该函数。
默认情况下，所有边距都是零。

### `[virtual] void QAbstractScrollArea::setupViewport(QWidget *viewport)`

**作用与语义：**

`QAbstractScrollArea`在调用`setViewport`（`viewport`）后调用该槽。在`QAbstractScrollArea`的子类中重构该函数，以在使用前初始化新`viewport`。

### `[override virtual] QSize QAbstractScrollArea::sizeHint() const`

**作用与语义：**

重装：`QFrame::sizeHint()` const.
返回滚动区域的 sizeHint 属性。大小通过使用 `viewportSizeHint()` 加上一些额外的滚动条空间（如有需要）确定。
重新实现属性的访问函数：`QWidget::sizeHint`。

### `QScrollBar *QAbstractScrollArea::verticalScrollBar() const`

**作用与语义：**

返回垂直滚动条。

### `QWidget *QAbstractScrollArea::viewport() const`

**作用与语义：**

返回视口小部件。
使用`QScrollArea::widget()`函数检索视口控件的内容。

### `[virtual protected] bool QAbstractScrollArea::viewportEvent(QEvent *event)`

**作用与语义：**

滚动区域（`viewport()` 小部件）的主事件处理程序。它处理指定的`event`，子类可以调用以提供合理的默认行为。
返回`true`表示事件系统事件已处理，无需进一步处理;否则返回`false`表示事件应继续传播。
你可以在子类中重新实现这个函数，但我们建议使用专门的事件处理程序。
视口事件的专用处理程序有：`paintEvent()`、`mousePressEvent()`、`mouseReleaseEvent()`、`mouseDoubleClickEvent()`、`mouseMoveEvent()`、`wheelEvent()`、`dragEnterEvent()`、`dragMoveEvent()`、`dragLeaveEvent()`、`dropEvent()`、`contextMenuEvent()`和`resizeEvent()`。

### `[protected] QMargins QAbstractScrollArea::viewportMargins() const`

**作用与语义：**

返回滚动区域周围的边距。默认情况下，所有边距都是零。

### `[virtual protected] QSize QAbstractScrollArea::viewportSizeHint() const`

**作用与语义：**

返回视口推荐大小。默认实现返回`viewport()`->`sizeHint()`。注意大小仅为视口大小，没有可见滚动条。

### `[override virtual protected] void QAbstractScrollArea::wheelEvent(QWheelEvent *e)`

**作用与语义：**

重实现自：`QWidget::wheelEvent`（QWheelEvent *event）。
该事件处理程序可以在子类中重新实现，以接收`viewport()`小部件的轮子事件。事件会在`e`传递。
该事件处理程序用于事件`event`，可以在子类中重新实现，以接收该控件的轮事件。
如果你重新实现了这个处理程序，非常重要的是，如果你不处理该事件，`ignore()`事件，这样小部件的父节点才能解释它。
默认实现会忽略该事件。

### `Qt::ScrollBarPolicy horizontalScrollBarPolicy() const`

**作用与语义：**

此属性保存水平滚动条的策略。
默认策略是 `Qt::ScrollBarAsNeeded`。

**如何使用：** 调用 `horizontalScrollBarPolicy()` 读取当前值；它不会修改应用状态。

### `void setHorizontalScrollBarPolicy(Qt::ScrollBarPolicy)`

**作用与语义：**

此属性保存水平滚动条的策略。
默认策略是 `Qt::ScrollBarAsNeeded`。

**如何使用：** 调用 `setHorizontalScrollBarPolicy(...)` 修改 `horizontalScrollBarPolicy`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setSizeAdjustPolicy(QAbstractScrollArea::SizeAdjustPolicy policy)`

**作用与语义：**

此属性保存描述当视口大小变化时滚动区域如何变化的策略。
默认策略是 `QAbstractScrollArea::AdjustIgnored`。更改此属性可能实际上会调整滚动区域的大小。

**如何使用：** 调用 `setSizeAdjustPolicy(...)` 修改 `sizeAdjustPolicy`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setVerticalScrollBarPolicy(Qt::ScrollBarPolicy)`

**作用与语义：**

此属性保存垂直滚动条的策略。
默认策略是 `Qt::ScrollBarAsNeeded`。

**如何使用：** 调用 `setVerticalScrollBarPolicy(...)` 修改 `verticalScrollBarPolicy`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QAbstractScrollArea::SizeAdjustPolicy sizeAdjustPolicy() const`

**作用与语义：**

此属性保存描述当视口大小变化时滚动区域如何变化的策略。
默认策略是 `QAbstractScrollArea::AdjustIgnored`。更改此属性可能实际上会调整滚动区域的大小。

**如何使用：** 调用 `sizeAdjustPolicy()` 读取当前值；它不会修改应用状态。

### `Qt::ScrollBarPolicy verticalScrollBarPolicy() const`

**作用与语义：**

此属性保存垂直滚动条的策略。
默认策略是 `Qt::ScrollBarAsNeeded`。

**如何使用：** 调用 `verticalScrollBarPolicy()` 读取当前值；它不会修改应用状态。

## 6. 深入实践与常见坑

### 生命周期和资源边界

控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

### 状态和错误边界

控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

### 线程边界

所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

### 最容易出现的错误

不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QAbstractScrollArea` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
