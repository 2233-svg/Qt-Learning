# QDockWidget

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QDockWidget` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QDockWidget` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QDockWidget>`
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

- `enum DockWidgetFeature { DockWidgetClosable, DockWidgetMovable, DockWidgetFloatable, DockWidgetVerticalTitleBar, NoDockWidgetFeatures }`
- `flags DockWidgetFeatures`

### 属性

- `allowedAreas : Qt::DockWidgetAreas`
- `(since 6.9) dockLocation : Qt::DockWidgetArea`
- `features : DockWidgetFeatures`
- `floating : bool`
- `windowTitle : QString`

### 公有函数

- `QDockWidget(QWidget *parent = nullptr, Qt::WindowFlags flags = Qt::WindowFlags())`
- `QDockWidget(const QString &title, QWidget *parent = nullptr, Qt::WindowFlags flags = Qt::WindowFlags())`
- `virtual ~QDockWidget()`
- `Qt::DockWidgetAreas allowedAreas() const`
- `Qt::DockWidgetArea dockLocation() const`
- `QDockWidget::DockWidgetFeatures features() const`
- `bool isAreaAllowed(Qt::DockWidgetArea area) const`
- `bool isFloating() const`
- `void setAllowedAreas(Qt::DockWidgetAreas areas)`
- `(since 6.9) void setDockLocation(Qt::DockWidgetArea area)`
- `void setFeatures(QDockWidget::DockWidgetFeatures features)`
- `void setFloating(bool floating)`
- `void setTitleBarWidget(QWidget *widget)`
- `void setWidget(QWidget *widget)`
- `QWidget * titleBarWidget() const`
- `QAction * toggleViewAction() const`
- `QWidget * widget() const`

### 信号

- `void allowedAreasChanged(Qt::DockWidgetAreas allowedAreas)`
- `void dockLocationChanged(Qt::DockWidgetArea area)`
- `void featuresChanged(QDockWidget::DockWidgetFeatures features)`
- `void topLevelChanged(bool topLevel)`
- `void visibilityChanged(bool visible)`

### 保护函数

- `virtual void initStyleOption(QStyleOptionDockWidget *option) const`

### 重实现的保护函数

- `virtual void changeEvent(QEvent *event) override`
- `virtual void closeEvent(QCloseEvent *event) override`
- `virtual bool event(QEvent *event) override`
- `virtual void paintEvent(QPaintEvent *event) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QDockWidget::DockWidgetFeatureflags QDockWidget::DockWidgetFeatures`

**作用与语义：**

- `QDockWidget::DockWidgetClosable`：`0x01`;码头小部件可以关闭。
- `QDockWidget::DockWidgetMovable`：`0x02`;用户可以在多个停靠点之间移动码头组件。
- `QDockWidget::DockWidgetFloatable`：`0x04`;dock 小部件可以从主窗口分离，并作为独立窗口浮动。
- `QDockWidget::DockWidgetVerticalTitleBar`：`0x08`;底座小部件左侧显示一个竖直标题栏。这可以用来增加`QMainWindow`中的垂直空间。
- `QDockWidget::NoDockWidgetFeatures`：`0x00`;停靠坞小部件不能关闭、移动或浮动。
DockWidgetFeatures 类型是 QFlags 的 typedef<DockWidgetFeature>。它存储 DockWidgetFeature 值的 OR 组合。

### `allowedAreas : Qt::DockWidgetAreas`

**作用与语义：**

可放置Dock小部件的区域。
默认是`Qt::AllDockWidgetAreas`。

**如何使用：** 调用 `allowedAreas()` 读取当前值；它不会修改应用状态。

### `[since 6.9] dockLocation : Qt::DockWidgetArea`

**作用与语义：**

该属性保留当前的码头位置，如果该码头小部件是浮动的或没有主窗口父节点，则该属性表示 Qt：：NoDockLocation。

**如何使用：** 调用 `dockLocation()` 读取当前值；它不会修改应用状态。

### `features : DockWidgetFeatures`

**作用与语义：**

该属性决定了码头小部件是可移动、可闭合还是可浮动。
默认情况下，该属性设置为`DockWidgetClosable`、`DockWidgetMovable`和`DockWidgetFloatable`的组合。

**如何使用：** 调用 `features()` 读取当前值；它不会修改应用状态。

### `floating : bool`

**作用与语义：**

该属性决定dock小部件是否浮动。
浮动停靠小部件以单个独立窗口的形式呈现给用户，“位于”其父`QMainWindow`之上，而不是停靠在`QMainWindow`或分页插坞小部件组中。
浮动码头小部件可以单独定位和调整大小，无论是程序化还是鼠标操作。
默认情况下，该属性为`true`。
当该属性发生变化时，`topLevelChanged()`信号会被发射。

**如何使用：** 调用 `floating()` 读取当前值；它不会修改应用状态。

### `windowTitle : QString`

**作用与语义：**

该属性包含 dock 小部件标题（说明）。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `windowTitle()` 读取当前值；它不会修改应用状态。

### `[explicit] QDockWidget::QDockWidget(QWidget *parent = nullptr, Qt::WindowFlags flags = Qt::WindowFlags())`

**作用与语义：**

构建一个带有父`parent`和窗口标志的QDockWidget `flags`。Dock小部件将放置在左侧的Dock小部件区域。

### `[explicit] QDockWidget::QDockWidget(const QString &title, QWidget *parent = nullptr, Qt::WindowFlags flags = Qt::WindowFlags())`

**作用与语义：**

构建带有父 `parent` 和窗口标志的 QDockWidget `flags`。码头控件将放置在左侧码头控件区域。
窗口标题设置为`title`。当 QDockWidget 停靠和拔出时使用该标题。它也用于 `QMainWindow` 提供的上下文菜单中。

### `[virtual noexcept] QDockWidget::~QDockWidget()`

**作用与语义：**

摧毁了码头小部件。

### `[signal] void QDockWidget::allowedAreasChanged(Qt::DockWidgetAreas allowedAreas)`

**作用与语义：**

可放置Dock小部件的区域。
默认是`Qt::AllDockWidgetAreas`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `allowedAreas` 的变化，不要把它当作普通函数主动调用。

### `[override virtual protected] void QDockWidget::changeEvent(QEvent *event)`

**作用与语义：**

重装：`QWidget::changeEvent`（QEvent *事件）。
该事件处理程序可以重新实现以处理状态变化。
该事件中被更改的状态可以通过提供的`event`检索。
变更事件包括：`QEvent::ToolBarChange`、`QEvent::ActivationChange`、`QEvent::EnabledChange`、`QEvent::FontChange`、`QEvent::StyleChange`、`QEvent::PaletteChange`、`QEvent::WindowTitleChange`、`QEvent::IconTextChange`、`QEvent::ModifiedChange`、`QEvent::MouseTrackingChange`、`QEvent::ParentChange`、`QEvent::WindowStateChange`、`QEvent::LanguageChange`、`QEvent::LocaleChange`、`QEvent::LayoutDirectionChange`、`QEvent::ReadOnlyChange`。

### `[override virtual protected] void QDockWidget::closeEvent(QCloseEvent *event)`

**作用与语义：**

重实现自：`QWidget::closeEvent`（QCloseEvent *event）。
当 Qt 收到来自窗口系统顶层控件的窗口关闭请求时，该事件处理程序会以该`event`调用。
默认情况下，事件被接受，小部件关闭。你可以重新实现这个函数，改变小部件对窗口关闭请求的响应方式。例如，你可以通过调用所有事件的 `ignore()` 来阻止窗口关闭。
主窗口应用程序通常会重新实现该函数，以检查用户的工作是否已被保存，并在关闭前请求许可。

### `[signal] void QDockWidget::dockLocationChanged(Qt::DockWidgetArea area)`

**作用与语义：**

该属性保留当前的码头位置，如果该码头小部件是浮动的或没有主窗口父节点，则该属性表示 Qt：：NoDockLocation。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `dockLocation` 的变化，不要把它当作普通函数主动调用。

### `[override virtual protected] bool QDockWidget::event(QEvent *event)`

**作用与语义：**

重实现自：`QWidget::event`（QEvent *事件）。

### `[signal] void QDockWidget::featuresChanged(QDockWidget::DockWidgetFeatures features)`

**作用与语义：**

该属性决定了码头小部件是可移动、可闭合还是可浮动。
默认情况下，该属性设置为`DockWidgetClosable`、`DockWidgetMovable`和`DockWidgetFloatable`的组合。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `features` 的变化，不要把它当作普通函数主动调用。

### `[virtual protected] void QDockWidget::initStyleOption(QStyleOptionDockWidget *option) const`

**作用与语义：**

用这个`QDockWidget`的值初始化`option`。这种方法适用于子类需要`QStyleOptionDockWidget`但不想自己填满所有信息时。

### `bool QDockWidget::isAreaAllowed(Qt::DockWidgetArea area) const`

**作用与语义：**

如果该 dock 小部件能放置在给定的`area`中，返回`true`;否则返回`false`。

### `[override virtual protected] void QDockWidget::paintEvent(QPaintEvent *event)`

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

### `[since 6.9] void QDockWidget::setDockLocation(Qt::DockWidgetArea area)`

**作用与语义：**

该属性保留当前的码头位置，如果该码头小部件是浮动的或没有主窗口父节点，则该属性表示 Qt：：NoDockLocation。

**如何使用：** 调用 `setDockLocation(...)` 修改 `dockLocation`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QDockWidget::setTitleBarWidget(QWidget *widget)`

**作用与语义：**

设置一个任意`widget`作为 dock 小部件的标题栏。如果`widget` `nullptr`，之前在 Dock 小部件上设置的任何自定义标题栏小部件都会被移除但不会删除，默认标题栏将被使用。
如果设置了标题栏小部件，`QDockWidget`在浮动时不会使用原生窗口装饰。
以下是实现自定义标题栏的一些建议：
- 标题栏控件未明确处理的鼠标事件必须通过调用`QMouseEvent::ignore()`来忽略。这些事件随后传播到`QDockWidget`父节点，父节点按常规方式处理，拖动标题栏时移动，双击时停靠和脱离，等等。
- 当`DockWidgetVerticalTitleBar`设置为`QDockWidget`时，标题栏控件会相应地重新定位。在`resizeEvent()`中，标题栏应检查应采取的方向：
`QDockWidget` *dockWidget = qobject_cast<`QDockWidget`*>（parentWidget()）;
如果 （dockWidget->features() & `QDockWidget::DockWidgetVerticalTitleBar`） {。
我需要保持垂直。
} 否则 {。
我需要横着。
}。
- 标题栏小部件必须具有有效的`QWidget::sizeHint()`和 `QWidget::minimumSizeHint()`。这些功能应考虑标题栏当前的朝向。
- 无法从Dock小部件中移除标题栏。不过，通过设置默认构造`QWidget`作为标题栏小部件，可以实现类似效果。
如上所示`qobject_cast()`，标题栏小部件可以使用其父`QDockWidget`的完全访问权限。因此，它可以根据用户操作执行停靠和隐藏等操作。

### `void QDockWidget::setWidget(QWidget *widget)`

**作用与语义：**

将Dock小部件设置为`widget`。
如果添加`widget`时dock小部件可见，必须明确`show()`。
注意，在调用该函数之前，必须先添加`widget`布局;否则，`widget`将不可见。

### `QWidget *QDockWidget::titleBarWidget() const`

**作用与语义：**

返回`QDockWidget`上设置的自定义标题栏控件，如果没有设置自定义标题栏，则返回`nullptr`。

### `QAction *QDockWidget::toggleViewAction() const`

**作用与语义：**

返回一个可勾选的操作，可以添加到菜单和工具栏，方便用户显示或关闭该 dock 小部件。
动作的文本被设置为 dock 小部件的窗口标题。
`QAction`对象归`QDockWidget`所有。当`QDockWidget`被销毁时，该对象将被自动删除。
注意：该动作不能用来程序化显示或隐藏dock小部件。请使用`visible`属性。

### `[signal] void QDockWidget::topLevelChanged(bool topLevel)`

**作用与语义：**

该属性决定dock小部件是否浮动。
浮动停靠小部件以单个独立窗口的形式呈现给用户，“位于”其父`QMainWindow`之上，而不是停靠在`QMainWindow`或分页插坞小部件组中。
浮动码头小部件可以单独定位和调整大小，无论是程序化还是鼠标操作。
默认情况下，该属性为`true`。
当该属性发生变化时，`topLevelChanged()`信号会被发射。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `floating` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QDockWidget::visibilityChanged(bool visible)`

**作用与语义：**

当底座小部件变为`visible`（或不可见）时，会发出该信号。当小部件被隐藏或显示，以及当小部件停靠在标签页的底座区域并选择或取消时，都会触发。
注意：信号可能与`QWidget::isVisible()`不同。如果某个底座小部件被最小化或固定化并关联到未选中或非激活标签页，就会发生这种情况。

### `QWidget *QDockWidget::widget() const`

**作用与语义：**

返回 dock 控件的控件。如果控件尚未设置，该函数返回零。

### `enum DockWidgetFeature { DockWidgetClosable, DockWidgetMovable, DockWidgetFloatable, DockWidgetVerticalTitleBar, NoDockWidgetFeatures }`

**作用与语义：**

- `QDockWidget::DockWidgetClosable`：`0x01`;码头小部件可以关闭。
- `QDockWidget::DockWidgetMovable`：`0x02`;用户可以在多个停靠点之间移动码头组件。
- `QDockWidget::DockWidgetFloatable`：`0x04`;dock 小部件可以从主窗口分离，并作为独立窗口浮动。
- `QDockWidget::DockWidgetVerticalTitleBar`：`0x08`;底座小部件左侧显示一个竖直标题栏。这可以用来增加`QMainWindow`中的垂直空间。
- `QDockWidget::NoDockWidgetFeatures`：`0x00`;停靠坞小部件不能关闭、移动或浮动。
DockWidgetFeatures 类型是 QFlags 的 typedef<DockWidgetFeature>。它存储 DockWidgetFeature 值的 OR 组合。

### `flags DockWidgetFeatures`

**作用与语义：**

- `QDockWidget::DockWidgetClosable`：`0x01`;码头小部件可以关闭。
- `QDockWidget::DockWidgetMovable`：`0x02`;用户可以在多个停靠点之间移动码头组件。
- `QDockWidget::DockWidgetFloatable`：`0x04`;dock 小部件可以从主窗口分离，并作为独立窗口浮动。
- `QDockWidget::DockWidgetVerticalTitleBar`：`0x08`;底座小部件左侧显示一个竖直标题栏。这可以用来增加`QMainWindow`中的垂直空间。
- `QDockWidget::NoDockWidgetFeatures`：`0x00`;停靠坞小部件不能关闭、移动或浮动。
DockWidgetFeatures 类型是 QFlags 的 typedef<DockWidgetFeature>。它存储 DockWidgetFeature 值的 OR 组合。

### `Qt::DockWidgetAreas allowedAreas() const`

**作用与语义：**

可放置Dock小部件的区域。
默认是`Qt::AllDockWidgetAreas`。

**如何使用：** 调用 `allowedAreas()` 读取当前值；它不会修改应用状态。

### `Qt::DockWidgetArea dockLocation() const`

**作用与语义：**

该属性保留当前的码头位置，如果该码头小部件是浮动的或没有主窗口父节点，则该属性表示 Qt：：NoDockLocation。

**如何使用：** 调用 `dockLocation()` 读取当前值；它不会修改应用状态。

### `QDockWidget::DockWidgetFeatures features() const`

**作用与语义：**

该属性决定了码头小部件是可移动、可闭合还是可浮动。
默认情况下，该属性设置为`DockWidgetClosable`、`DockWidgetMovable`和`DockWidgetFloatable`的组合。

**如何使用：** 调用 `features()` 读取当前值；它不会修改应用状态。

### `bool isFloating() const`

**作用与语义：**

该属性决定dock小部件是否浮动。
浮动停靠小部件以单个独立窗口的形式呈现给用户，“位于”其父`QMainWindow`之上，而不是停靠在`QMainWindow`或分页插坞小部件组中。
浮动码头小部件可以单独定位和调整大小，无论是程序化还是鼠标操作。
默认情况下，该属性为`true`。
当该属性发生变化时，`topLevelChanged()`信号会被发射。

**如何使用：** 调用 `isFloating()` 读取当前值；它不会修改应用状态。

### `void setAllowedAreas(Qt::DockWidgetAreas areas)`

**作用与语义：**

可放置Dock小部件的区域。
默认是`Qt::AllDockWidgetAreas`。

**如何使用：** 调用 `setAllowedAreas(...)` 修改 `allowedAreas`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setFeatures(QDockWidget::DockWidgetFeatures features)`

**作用与语义：**

该属性决定了码头小部件是可移动、可闭合还是可浮动。
默认情况下，该属性设置为`DockWidgetClosable`、`DockWidgetMovable`和`DockWidgetFloatable`的组合。

**如何使用：** 调用 `setFeatures(...)` 修改 `features`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setFloating(bool floating)`

**作用与语义：**

该属性决定dock小部件是否浮动。
浮动停靠小部件以单个独立窗口的形式呈现给用户，“位于”其父`QMainWindow`之上，而不是停靠在`QMainWindow`或分页插坞小部件组中。
浮动码头小部件可以单独定位和调整大小，无论是程序化还是鼠标操作。
默认情况下，该属性为`true`。
当该属性发生变化时，`topLevelChanged()`信号会被发射。

**如何使用：** 调用 `setFloating(...)` 修改 `floating`；传入的新值会成为后续查询和相关界面行为所使用的值。

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

`QDockWidget` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
