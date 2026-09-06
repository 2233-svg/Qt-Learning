# QMainWindow

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QMainWindow` 是桌面应用主窗口框架，集中管理中央控件、菜单栏、工具栏、状态栏和停靠窗口。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QMainWindow` 是桌面应用主窗口框架，集中管理中央控件、菜单栏、工具栏、状态栏和停靠窗口。

**内部模型：** QMainWindow 有自己的特殊布局，中央区域只能通过 setCentralWidget 设置；工具栏和停靠窗口不是普通 layout 子项。把内容控件、命令 QAction 和窗口框架分开设计，后续扩展更稳定。

**适用场景：** 有菜单、工具栏、状态栏、多个编辑区或可停靠面板的桌面应用使用；只有一个简单控件的窗口可以直接用 QWidget。

**典型调用链：** 构造主窗口 -> 创建 QAction -> addMenu/addToolBar -> setCentralWidget -> addDockWidget -> statusBar()->showMessage -> saveState/restoreState。

**先记住的坑：** 不要给 QMainWindow 直接 setLayout；中央控件只能有一个；saveState/restoreState 要配合稳定的 objectName；工具栏和 dock 的所有权通常由主窗口接管。

## 2. 依赖与对象关系

- 头文件：`#include <QMainWindow>`
- 继承自：QWidget
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

QMainWindow 有自己的特殊布局，中央区域只能通过 setCentralWidget 设置；工具栏和停靠窗口不是普通 layout 子项。把内容控件、命令 QAction 和窗口框架分开设计，后续扩展更稳定。

### 状态、生命周期和线程

**生命周期：** 控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

**状态与结果：** 控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

**线程与事件循环：** 所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

## 3. 直接使用

有菜单、工具栏、状态栏、多个编辑区或可停靠面板的桌面应用使用；只有一个简单控件的窗口可以直接用 QWidget。 使用时通常按这个过程组织：构造主窗口 -> 创建 QAction -> addMenu/addToolBar -> setCentralWidget -> addDockWidget -> statusBar()->showMessage -> saveState/restoreState。

```cpp
#include <QApplication>
#include <QLabel>
#include <QMainWindow>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    QMainWindow window;
    window.setWindowTitle(QStringLiteral("Main Window"));
    window.setCentralWidget(new QLabel(QStringLiteral("Content"), &window));
    window.show();
    return app.exec();
}
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum DockOption { AnimatedDocks, AllowNestedDocks, AllowTabbedDocks, ForceTabbedDocks, VerticalTabs, GroupedDragging }`
- `flags DockOptions`

### 属性

- `animated : bool`
- `dockNestingEnabled : bool`
- `dockOptions : DockOptions`
- `documentMode : bool`
- `iconSize : QSize`
- `tabShape : QTabWidget::TabShape`
- `toolButtonStyle : Qt::ToolButtonStyle`
- `unifiedTitleAndToolBarOnMac : bool`

### 公有函数

- `QMainWindow(QWidget *parent = nullptr, Qt::WindowFlags flags = Qt::WindowFlags())`
- `virtual ~QMainWindow()`
- `void addDockWidget(Qt::DockWidgetArea area, QDockWidget *dockwidget)`
- `void addDockWidget(Qt::DockWidgetArea area, QDockWidget *dockwidget, Qt::Orientation orientation)`
- `void addToolBar(Qt::ToolBarArea area, QToolBar *toolbar)`
- `void addToolBar(QToolBar *toolbar)`
- `QToolBar * addToolBar(const QString &title)`
- `void addToolBarBreak(Qt::ToolBarArea area = Qt::TopToolBarArea)`
- `QWidget * centralWidget() const`
- `Qt::DockWidgetArea corner(Qt::Corner corner) const`
- `virtual QMenu * createPopupMenu()`
- `QMainWindow::DockOptions dockOptions() const`
- `Qt::DockWidgetArea dockWidgetArea(QDockWidget *dockwidget) const`
- `bool documentMode() const`
- `QSize iconSize() const`
- `void insertToolBar(QToolBar *before, QToolBar *toolbar)`
- `void insertToolBarBreak(QToolBar *before)`
- `bool isAnimated() const`
- `bool isDockNestingEnabled() const`
- `QMenuBar * menuBar() const`
- `QWidget * menuWidget() const`
- `void removeDockWidget(QDockWidget *dockwidget)`
- `void removeToolBar(QToolBar *toolbar)`
- `void removeToolBarBreak(QToolBar *before)`
- `void resizeDocks(const QList<QDockWidget *> &docks, const QList<int> &sizes, Qt::Orientation orientation)`
- `bool restoreDockWidget(QDockWidget *dockwidget)`
- `bool restoreState(const QByteArray &state, int version = 0)`
- `QByteArray saveState(int version = 0) const`
- `void setCentralWidget(QWidget *widget)`
- `void setCorner(Qt::Corner corner, Qt::DockWidgetArea area)`
- `void setDockOptions(QMainWindow::DockOptions options)`
- `void setDocumentMode(bool enabled)`
- `void setIconSize(const QSize &iconSize)`
- `void setMenuBar(QMenuBar *menuBar)`
- `void setMenuWidget(QWidget *menuBar)`
- `void setStatusBar(QStatusBar *statusbar)`
- `void setTabPosition(Qt::DockWidgetAreas areas, QTabWidget::TabPosition tabPosition)`
- `void setTabShape(QTabWidget::TabShape tabShape)`
- `void setToolButtonStyle(Qt::ToolButtonStyle toolButtonStyle)`
- `void splitDockWidget(QDockWidget *first, QDockWidget *second, Qt::Orientation orientation)`
- `QStatusBar * statusBar() const`
- `QTabWidget::TabPosition tabPosition(Qt::DockWidgetArea area) const`
- `QTabWidget::TabShape tabShape() const`
- `QList<QDockWidget *> tabifiedDockWidgets(QDockWidget *dockwidget) const`
- `void tabifyDockWidget(QDockWidget *first, QDockWidget *second)`
- `QWidget * takeCentralWidget()`
- `Qt::ToolBarArea toolBarArea(const QToolBar *toolbar) const`
- `bool toolBarBreak(QToolBar *toolbar) const`
- `Qt::ToolButtonStyle toolButtonStyle() const`
- `bool unifiedTitleAndToolBarOnMac() const`

### 公有槽函数

- `void setAnimated(bool enabled)`
- `void setDockNestingEnabled(bool enabled)`
- `void setUnifiedTitleAndToolBarOnMac(bool set)`

### 信号

- `void iconSizeChanged(const QSize &iconSize)`
- `void tabifiedDockWidgetActivated(QDockWidget *dockWidget)`
- `void toolButtonStyleChanged(Qt::ToolButtonStyle toolButtonStyle)`

### 重实现的保护函数

- `virtual void contextMenuEvent(QContextMenuEvent *event) override`
- `virtual bool event(QEvent *event) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QMainWindow::DockOptionflags QMainWindow::DockOptions`

**作用与语义：**

该枚举包含指定`QMainWindow`对接行为的标志。
- `QMainWindow::AnimatedDocks`：`0x01`;与`animated`属性相同。
- `QMainWindow::AllowNestedDocks`：`0x02`;与`dockNestingEnabled`属性相同。
- `QMainWindow::AllowTabbedDocks`：`0x04`;用户可以将一个 dock 小部件“叠加”在另一个小部件之上。两个小部件叠加，并出现一个标签栏，用于选择哪个小部件可见。
- `QMainWindow::ForceTabbedDocks`：`0x08`;每个码头区域包含一组标签页码头组件。换句话说，码头组件不能在码头区域内相邻放置。如果设置了该选项，AllowNestedDocks 不会生效。
- `QMainWindow::VerticalTabs`：`0x10`;主窗口两侧的两个垂直插页区域垂直显示其标签。如果未设置此选项，所有插坞区域的标签页会显示在底部。这意味着允许TabbedDocks。参见`setTabPosition()`。
- `QMainWindow::GroupedDragging`：`0x20`;拖动dock标题栏时，所有与该标签绑定的标签页都会被拖动。这意味着AllowTabbedDocks。如果某些QDockWidget在允许区域有限制，则效果不佳。（该枚举值是在Qt 5.6中添加的。）
这些选项仅控制码头小部件在`QMainWindow`中如何被丢弃。它们不会重新排列码头控件以符合指定选项。因此，应在任何码头组件添加到主窗口之前设置。例外是 AnimatedDocks 和 VerticalTabs 选项，这些选项可以随时设置。
DockOptions 类型是 QFlags 的 typedef<DockOption>。它存储 DockOption 值的 OR 组合。

### `animated : bool`

**作用与语义：**

该属性决定了操作 dock 控件和工具栏是否会被动画化。
当停靠点小部件或工具栏被拖曳到主窗口上时，主窗口会调整其内容，指示如果停靠点小部件或工具栏被放下，将停靠在哪里。设置该属性后，`QMainWindow`会以平滑的动画移动其内容。清除该属性后，内容物会自动吸附到新位置。
默认情况下，该属性是设置的。如果主窗口中存在的控件在调整大小或重新绘制时较慢，可能会清除该属性。
设置此属性与使用 `setDockOptions()` 设置 `AnimatedDocks` 选项相同。

**如何使用：** 调用 `animated()` 读取当前值；它不会修改应用状态。

### `dockNestingEnabled : bool`

**作用与语义：**

该属性决定码头是否可以嵌套。
如果该属性`false`，停靠区域只能包含一行（水平或垂直）的停靠组件。如果该属性`true`，则停靠小部件所占用的区域可以向任一方向分割，以容纳更多的停靠小部件。
Dock嵌套仅在包含大量Dock小部件的应用中才是必要的。它让用户在组织主窗口时有更大的自由。然而，当将Dock小部件拖到主窗口上时，Dock嵌套会导致行为更复杂（且不那么直观），因为放置的Dock小部件可以有更多方式放置在Dock区域。
设置该属性与使用 `setDockOptions()` 设置 `AllowNestedDocks` 选项相同。

**如何使用：** 调用 `dockNestingEnabled()` 读取当前值；它不会修改应用状态。

### `dockOptions : DockOptions`

**作用与语义：**

该属性具有`QMainWindow`的对接行为。
默认值为`AnimatedDocks` |`AllowTabbedDocks`。

**如何使用：** 调用 `dockOptions()` 读取当前值；它不会修改应用状态。

### `documentMode : bool`

**作用与语义：**

该属性是否将标签页 DockWidgets 的标签栏设置为文档模式。
默认是假的。

**如何使用：** 调用 `documentMode()` 读取当前值；它不会修改应用状态。

### `iconSize : QSize`

**作用与语义：**

主窗口中工具栏图标的大小。
默认是GUI样式的工具栏图标大小。请注意，所用图标必须至少达到这个大小，因为图标只是缩小了。

**如何使用：** 调用 `iconSize()` 读取当前值；它不会修改应用状态。

### `tabShape : QTabWidget::TabShape`

**作用与语义：**

该属性保留了用于标签式 Dock 控件的制表形状。
默认是`QTabWidget::Rounded`。

**如何使用：** 调用 `tabShape()` 读取当前值；它不会修改应用状态。

### `toolButtonStyle : Qt::ToolButtonStyle`

**作用与语义：**

工具栏按钮的样式。
为了让工具按钮的样式符合系统设置，请将该属性设置为`Qt::ToolButtonFollowStyle`。在 Unix 上，用户的设置将被使用桌面环境。在其他平台上，`Qt::ToolButtonFollowStyle` 仅指图标。
默认是`Qt::ToolButtonIconOnly`。

**如何使用：** 调用 `toolButtonStyle()` 读取当前值；它不会修改应用状态。

### `unifiedTitleAndToolBarOnMac : bool`

**作用与语义：**

该属性决定了窗口是否使用macOS统一的标题和工具栏外观。
注意，Qt 5 的实现相比 Qt 4 存在若干限制：
- 不支持在 Windows 中使用 OpenGL 内容。这包括 `QOpenGLWidget`。
- 使用可停靠或可移动工具栏可能导致涂装错误，不建议使用

**如何使用：** 调用 `unifiedTitleAndToolBarOnMac()` 读取当前值；它不会修改应用状态。

### `[explicit] QMainWindow::QMainWindow(QWidget *parent = nullptr, Qt::WindowFlags flags = Qt::WindowFlags())`

**作用与语义：**

构建一个包含给定`parent`和指定控件`flags`的QMainWindow。
QMainWindow 本身设置了`Qt::Window`标志，因此始终作为顶层控件创建。

### `[virtual noexcept] QMainWindow::~QMainWindow()`

**作用与语义：**

会破坏主窗户。

### `void QMainWindow::addDockWidget(Qt::DockWidgetArea area, QDockWidget *dockwidget)`

**作用与语义：**

将给定`dockwidget`加到指定的`area`上。

### `void QMainWindow::addDockWidget(Qt::DockWidgetArea area, QDockWidget *dockwidget, Qt::Orientation orientation)`

**作用与语义：**

在`orientation`指定方向上向给定`area`加`dockwidget`。

### `void QMainWindow::addToolBar(Qt::ToolBarArea area, QToolBar *toolbar)`

**作用与语义：**

将`toolbar`添加到主窗口的指定`area`中。`toolbar`放置在当前工具栏块的末尾（即行）。如果主窗口已经能`toolbar`，那么它只会将工具栏移动到`area`。

### `void QMainWindow::addToolBar(QToolBar *toolbar)`

**作用与语义：**

相当于调用 addToolBar（`Qt::TopToolBarArea`， `toolbar`）。

### `QToolBar *QMainWindow::addToolBar(const QString &title)`

**作用与语义：**

创建一个`QToolBar`对象，将其窗口标题设置为`title`，并将其插入顶部工具栏区域。

### `void QMainWindow::addToolBarBreak(Qt::ToolBarArea area = Qt::TopToolBarArea)`

**作用与语义：**

在所有其他存在的对象之后，给给定的`area`添加一个工具栏断开。

### `QWidget *QMainWindow::centralWidget() const`

**作用与语义：**

返回主窗口的中央控件。如果中央控件尚未设置，该函数返回`nullptr`。

### `[override virtual protected] void QMainWindow::contextMenuEvent(QContextMenuEvent *event)`

**作用与语义：**

重实现自：`QWidget::contextMenuEvent`（QContextMenuEvent *event）。
该事件处理程序用于事件`event`，可以在子类中重新实现，以接收控件上下文菜单事件。
当控件的 `contextMenuPolicy` `Qt::DefaultContextMenu`时调用处理器。
默认实现忽略上下文事件。详情请参见`QContextMenuEvent`文档。

### `Qt::DockWidgetArea QMainWindow::corner(Qt::Corner corner) const`

**作用与语义：**

返回占据指定`corner`的停靠坞小部件区域。

### `[virtual] QMenu *QMainWindow::createPopupMenu()`

**作用与语义：**

返回一个弹出菜单，包含主窗口中工具栏和停靠点小部件的可勾选条目。如果没有工具栏和停靠小部件，该函数返回`nullptr`。
默认情况下，当用户激活右键菜单时，通常通过右键点击工具栏或 Dock 小部件，主窗口调用此功能。
如果你想创建自定义弹窗菜单，可以重新实现这个功能，并返回新创建的弹窗菜单。弹窗菜单的所有权会转移给调用者。

### `Qt::DockWidgetArea QMainWindow::dockWidgetArea(QDockWidget *dockwidget) const`

**作用与语义：**

返回`dockwidget`的`Qt::DockWidgetArea`。如果主窗口中没有添加`dockwidget`，该函数返回`Qt::NoDockWidgetArea`。

### `[override virtual protected] bool QMainWindow::event(QEvent *event)`

**作用与语义：**

重实现自：`QWidget::event`（QEvent *事件）。

### `[signal] void QMainWindow::iconSizeChanged(const QSize &iconSize)`

**作用与语义：**

当窗口中图标的大小发生变化时，会发出该信号。新的图标大小会在`iconSize`中传递。
你可以将该信号连接到其他组件，以帮助保持应用外观的一致性。

### `void QMainWindow::insertToolBar(QToolBar *before, QToolBar *toolbar)`

**作用与语义：**

将`toolbar`插入`before`工具栏所在的区域，使其显示在其前方。例如，在正常的从左到右布局操作中，这意味着`toolbar`会出现在`before`指定的工具栏左侧的水平工具栏区域。

### `void QMainWindow::insertToolBarBreak(QToolBar *before)`

**作用与语义：**

在`before`指定的工具栏前插入一个工具栏断开。

### `QMenuBar *QMainWindow::menuBar() const`

**作用与语义：**

返回主窗口的菜单栏。如果菜单栏不存在，这个函数会创建并返回一个空菜单栏。
如果你想让 Mac 应用中的所有窗口共享一个菜单栏，不要用这个函数来创建它，因为这里创建的菜单栏会以该`QMainWindow`作为父。相反，你必须创建一个没有父的菜单栏，然后可以在所有 Mac 窗口之间共享。通过这种方式创建一个无父菜单栏：

**官方示例：**

```cpp
 QMenuBar *menuBar = new QMenuBar(nullptr);
```

### `QWidget *QMainWindow::menuWidget() const`

**作用与语义：**

返回主窗口的菜单栏。如果菜单栏尚未构建，该函数返回空值。

### `void QMainWindow::removeDockWidget(QDockWidget *dockwidget)`

**作用与语义：**

移除主窗口布局中的`dockwidget`并隐藏它。注意`dockwidget`没有被删除。

### `void QMainWindow::removeToolBar(QToolBar *toolbar)`

**作用与语义：**

移除主窗口布局中的`toolbar`并隐藏它。注意`toolbar`没有被删除。

### `void QMainWindow::removeToolBarBreak(QToolBar *before)`

**作用与语义：**

移除之前插入在`before`指定工具栏前的工具栏断裂点。

### `void QMainWindow::resizeDocks(const QList<QDockWidget *> &docks, const QList<int> &sizes, Qt::Orientation orientation)`

**作用与语义：**

将列表中的码头控件调整为列表`docks` `sizes`中对应的像素大小（像素单位）。如果`orientation` `Qt::Horizontal`，则调整宽度，否则调整码头控件的高度。尺寸会被调整，以保证最大和最小尺寸得到尊重，且`QMainWindow`本身不会被调整大小。任何额外或缺失的空间会根据尺寸的相对权重分配到各个控件之间。
如果蓝色和黄色小部件嵌套在同一层级，它们的大小会被调整，使得黄色小部件的大小是蓝色小部件的两倍。
如果某些控件被分组在标签页中，则每个组应指定一个控件。列表中未包含的小部件可能会修改以遵守约束。

**官方示例：**

```cpp
     resizeDocks({blueWidget, yellowWidget}, {20 , 40}, Qt::Horizontal);
```

### `bool QMainWindow::restoreDockWidget(QDockWidget *dockwidget)`

**作用与语义：**

如果状态在调用`restoreState()`后创建，则恢复`dockwidget`状态。如果状态恢复，返回`true`;否则返回`false`。

### `bool QMainWindow::restoreState(const QByteArray &state, int version = 0)`

**作用与语义：**

恢复该主窗口工具栏和 dockwidgets 的 `state`。还恢复角位设置。`version` 数值与 `state` 中存储的数值进行比较。如果不匹配，主窗口的状态保持不变，该函数返回 `false`;否则，状态恢复，该函数返回 `true`。
要恢复使用`QSettings`保存的几何体，可以使用以下代码：

**官方示例：**

```cpp
 void MainWindow::readSettings()
 {
     QSettings settings("MyCompany", "MyApp");
     restoreGeometry(settings.value("myWidget/geometry").toByteArray());
     restoreState(settings.value("myWidget/windowState").toByteArray());
 }
```

### `QByteArray QMainWindow::saveState(int version = 0) const`

**作用与语义：**

保存该主窗口工具栏和 dockwidgets 的当前状态。这包括可以用 `setCorner()` 设置的角落设置。`version` 编号作为数据的一部分存储。
`objectName`物业用于标识每个`QToolBar`和`QDockWidget`。你应确保每个`QToolBar`和添加`QDockWidget`的物业都是独一无二的`QMainWindow`。
要恢复保存状态，将返回值和`version`数传递给`restoreState()`。
为了在窗口关闭时保存几何体，你可以实现类似这样的关闭事件：

**官方示例：**

```cpp
 void MyMainWindow::closeEvent(QCloseEvent *event)
 {
     QSettings settings("MyCompany", "MyApp");
     settings.setValue("geometry", saveGeometry());
     settings.setValue("windowState", saveState());
     QMainWindow::closeEvent(event);
 }
```

### `void QMainWindow::setCentralWidget(QWidget *widget)`

**作用与语义：**

将给定`widget`设置为主窗口的中央控件。
注意：`QMainWindow`会接管`widget`指针的所有权，并在适当时间删除。

### `void QMainWindow::setCorner(Qt::Corner corner, Qt::DockWidgetArea area)`

**作用与语义：**

将给定的停靠坞小部件`area`占用指定的`corner`。

### `void QMainWindow::setMenuBar(QMenuBar *menuBar)`

**作用与语义：**

将主窗口的菜单栏设置为`menuBar`。
注意：`QMainWindow`会接管`menuBar`指针的所有权，并在适当时机删除。

### `void QMainWindow::setMenuWidget(QWidget *menuBar)`

**作用与语义：**

将主窗口的菜单栏设置为`menuBar`。
`QMainWindow`会接管`menuBar`指针，并在适当的时候删除它。

### `void QMainWindow::setStatusBar(QStatusBar *statusbar)`

**作用与语义：**

将主窗口的状态栏设置为`statusbar`。
将状态栏设置为`nullptr`会将其从主窗口移除。注意`QMainWindow`会获得`statusbar`指针的所有权，并在适当时间删除它。

### `void QMainWindow::setTabPosition(Qt::DockWidgetAreas areas, QTabWidget::TabPosition tabPosition)`

**作用与语义：**

将指定底座小部件的标签位置`areas`设置为指定的`tabPosition`。默认情况下，所有底座区域底部都会显示标签页。
注意：`VerticalTabs` 底座选项会覆盖该方法设置的标签位置。

### `void QMainWindow::splitDockWidget(QDockWidget *first, QDockWidget *second, Qt::Orientation orientation)`

**作用与语义：**

将`first`码头小部件覆盖的空间分成两部分，将`first`码头小部件移到第一部分，`second`码头小部件移到第二部分。
`orientation`规定了空间的划分方式：`Qt::Horizontal`分割时将第二个码头小部件置于第一个组件的右侧;`Qt::Vertical`分割时，第二个码头小部件位于第一个下方。
注意：如果`first`当前处于标签停靠区域，`second`将作为新标签添加，而非`first`的邻居。这是因为单个标签页只能包含一个扩展坞小部件。
注意：`Qt::LayoutDirection`会影响分割区域两部分中码头组件的顺序。当启用右向左布局方向时，码头组件的位置将被反向。

### `QStatusBar *QMainWindow::statusBar() const`

**作用与语义：**

返回主窗口的状态栏。如果状态栏不存在，该函数会创建并返回一个空状态栏。

### `QTabWidget::TabPosition QMainWindow::tabPosition(Qt::DockWidgetArea area) const`

**作用与语义：**

返回`area`的制表位。
注意：底座`VerticalTabs`选项会覆盖该功能返回的标签位置。

### `[signal] void QMainWindow::tabifiedDockWidgetActivated(QDockWidget *dockWidget)`

**作用与语义：**

当通过选择标签激活tabified的Dock小部件时，会发出该信号。激活后的Dock小部件会在`dockWidget`传递。

### `QList<QDockWidget *> QMainWindow::tabifiedDockWidgets(QDockWidget *dockwidget) const`

**作用与语义：**

返回与`dockwidget`一起被tabify的Dock小部件。

### `void QMainWindow::tabifyDockWidget(QDockWidget *first, QDockWidget *second)`

**作用与语义：**

将`second` Dock 小部件移到`first` Dock 小部件上，在主窗口创建一个带标签的 Dock 区域。

### `QWidget *QMainWindow::takeCentralWidget()`

**作用与语义：**

移除主窗口中的中央小部件。
被移除的小部件的所有权会转移给调用者。

### `Qt::ToolBarArea QMainWindow::toolBarArea(const QToolBar *toolbar) const`

**作用与语义：**

返回`toolbar`的`Qt::ToolBarArea`。如果主窗口中未添加`toolbar`，该函数返回`Qt::NoToolBarArea`。

### `bool QMainWindow::toolBarBreak(QToolBar *toolbar) const`

**作用与语义：**

返回是否在`toolbar`之前有工具栏中断。

### `[signal] void QMainWindow::toolButtonStyleChanged(Qt::ToolButtonStyle toolButtonStyle)`

**作用与语义：**

当窗口中工具按钮的样式发生变化时，会发出该信号。新样式会在`toolButtonStyle`中传递。
你可以将该信号连接到其他组件，以帮助保持应用外观的一致性。

### `enum DockOption { AnimatedDocks, AllowNestedDocks, AllowTabbedDocks, ForceTabbedDocks, VerticalTabs, GroupedDragging }`

**作用与语义：**

该枚举包含指定`QMainWindow`对接行为的标志。
- `QMainWindow::AnimatedDocks`：`0x01`;与`animated`属性相同。
- `QMainWindow::AllowNestedDocks`：`0x02`;与`dockNestingEnabled`属性相同。
- `QMainWindow::AllowTabbedDocks`：`0x04`;用户可以将一个 dock 小部件“叠加”在另一个小部件之上。两个小部件叠加，并出现一个标签栏，用于选择哪个小部件可见。
- `QMainWindow::ForceTabbedDocks`：`0x08`;每个码头区域包含一组标签页码头组件。换句话说，码头组件不能在码头区域内相邻放置。如果设置了该选项，AllowNestedDocks 不会生效。
- `QMainWindow::VerticalTabs`：`0x10`;主窗口两侧的两个垂直插页区域垂直显示其标签。如果未设置此选项，所有插坞区域的标签页会显示在底部。这意味着允许TabbedDocks。参见`setTabPosition()`。
- `QMainWindow::GroupedDragging`：`0x20`;拖动dock标题栏时，所有与该标签绑定的标签页都会被拖动。这意味着AllowTabbedDocks。如果某些QDockWidget在允许区域有限制，则效果不佳。（该枚举值是在Qt 5.6中添加的。）
这些选项仅控制码头小部件在`QMainWindow`中如何被丢弃。它们不会重新排列码头控件以符合指定选项。因此，应在任何码头组件添加到主窗口之前设置。例外是 AnimatedDocks 和 VerticalTabs 选项，这些选项可以随时设置。
DockOptions 类型是 QFlags 的 typedef<DockOption>。它存储 DockOption 值的 OR 组合。

### `flags DockOptions`

**作用与语义：**

该枚举包含指定`QMainWindow`对接行为的标志。
- `QMainWindow::AnimatedDocks`：`0x01`;与`animated`属性相同。
- `QMainWindow::AllowNestedDocks`：`0x02`;与`dockNestingEnabled`属性相同。
- `QMainWindow::AllowTabbedDocks`：`0x04`;用户可以将一个 dock 小部件“叠加”在另一个小部件之上。两个小部件叠加，并出现一个标签栏，用于选择哪个小部件可见。
- `QMainWindow::ForceTabbedDocks`：`0x08`;每个码头区域包含一组标签页码头组件。换句话说，码头组件不能在码头区域内相邻放置。如果设置了该选项，AllowNestedDocks 不会生效。
- `QMainWindow::VerticalTabs`：`0x10`;主窗口两侧的两个垂直插页区域垂直显示其标签。如果未设置此选项，所有插坞区域的标签页会显示在底部。这意味着允许TabbedDocks。参见`setTabPosition()`。
- `QMainWindow::GroupedDragging`：`0x20`;拖动dock标题栏时，所有与该标签绑定的标签页都会被拖动。这意味着AllowTabbedDocks。如果某些QDockWidget在允许区域有限制，则效果不佳。（该枚举值是在Qt 5.6中添加的。）
这些选项仅控制码头小部件在`QMainWindow`中如何被丢弃。它们不会重新排列码头控件以符合指定选项。因此，应在任何码头组件添加到主窗口之前设置。例外是 AnimatedDocks 和 VerticalTabs 选项，这些选项可以随时设置。
DockOptions 类型是 QFlags 的 typedef<DockOption>。它存储 DockOption 值的 OR 组合。

### `QMainWindow::DockOptions dockOptions() const`

**作用与语义：**

该属性具有`QMainWindow`的对接行为。
默认值为`AnimatedDocks` |`AllowTabbedDocks`。

**如何使用：** 调用 `dockOptions()` 读取当前值；它不会修改应用状态。

### `bool documentMode() const`

**作用与语义：**

该属性是否将标签页 DockWidgets 的标签栏设置为文档模式。
默认是假的。

**如何使用：** 调用 `documentMode()` 读取当前值；它不会修改应用状态。

### `QSize iconSize() const`

**作用与语义：**

主窗口中工具栏图标的大小。
默认是GUI样式的工具栏图标大小。请注意，所用图标必须至少达到这个大小，因为图标只是缩小了。

**如何使用：** 调用 `iconSize()` 读取当前值；它不会修改应用状态。

### `bool isAnimated() const`

**作用与语义：**

该属性决定了操作 dock 控件和工具栏是否会被动画化。
当停靠点小部件或工具栏被拖曳到主窗口上时，主窗口会调整其内容，指示如果停靠点小部件或工具栏被放下，将停靠在哪里。设置该属性后，`QMainWindow`会以平滑的动画移动其内容。清除该属性后，内容物会自动吸附到新位置。
默认情况下，该属性是设置的。如果主窗口中存在的控件在调整大小或重新绘制时较慢，可能会清除该属性。
设置此属性与使用 `setDockOptions()` 设置 `AnimatedDocks` 选项相同。

**如何使用：** 调用 `isAnimated()` 读取当前值；它不会修改应用状态。

### `bool isDockNestingEnabled() const`

**作用与语义：**

该属性决定码头是否可以嵌套。
如果该属性`false`，停靠区域只能包含一行（水平或垂直）的停靠组件。如果该属性`true`，则停靠小部件所占用的区域可以向任一方向分割，以容纳更多的停靠小部件。
Dock嵌套仅在包含大量Dock小部件的应用中才是必要的。它让用户在组织主窗口时有更大的自由。然而，当将Dock小部件拖到主窗口上时，Dock嵌套会导致行为更复杂（且不那么直观），因为放置的Dock小部件可以有更多方式放置在Dock区域。
设置该属性与使用 `setDockOptions()` 设置 `AllowNestedDocks` 选项相同。

**如何使用：** 调用 `isDockNestingEnabled()` 读取当前值；它不会修改应用状态。

### `void setDockOptions(QMainWindow::DockOptions options)`

**作用与语义：**

该属性具有`QMainWindow`的对接行为。
默认值为`AnimatedDocks` |`AllowTabbedDocks`。

**如何使用：** 调用 `setDockOptions(...)` 修改 `dockOptions`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setDocumentMode(bool enabled)`

**作用与语义：**

该属性是否将标签页 DockWidgets 的标签栏设置为文档模式。
默认是假的。

**如何使用：** 调用 `setDocumentMode(...)` 修改 `documentMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setIconSize(const QSize &iconSize)`

**作用与语义：**

主窗口中工具栏图标的大小。
默认是GUI样式的工具栏图标大小。请注意，所用图标必须至少达到这个大小，因为图标只是缩小了。

**如何使用：** 调用 `setIconSize(...)` 修改 `iconSize`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTabShape(QTabWidget::TabShape tabShape)`

**作用与语义：**

该属性保留了用于标签式 Dock 控件的制表形状。
默认是`QTabWidget::Rounded`。

**如何使用：** 调用 `setTabShape(...)` 修改 `tabShape`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setToolButtonStyle(Qt::ToolButtonStyle toolButtonStyle)`

**作用与语义：**

工具栏按钮的样式。
为了让工具按钮的样式符合系统设置，请将该属性设置为`Qt::ToolButtonFollowStyle`。在 Unix 上，用户的设置将被使用桌面环境。在其他平台上，`Qt::ToolButtonFollowStyle` 仅指图标。
默认是`Qt::ToolButtonIconOnly`。

**如何使用：** 调用 `setToolButtonStyle(...)` 修改 `toolButtonStyle`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QTabWidget::TabShape tabShape() const`

**作用与语义：**

该属性保留了用于标签式 Dock 控件的制表形状。
默认是`QTabWidget::Rounded`。

**如何使用：** 调用 `tabShape()` 读取当前值；它不会修改应用状态。

### `Qt::ToolButtonStyle toolButtonStyle() const`

**作用与语义：**

工具栏按钮的样式。
为了让工具按钮的样式符合系统设置，请将该属性设置为`Qt::ToolButtonFollowStyle`。在 Unix 上，用户的设置将被使用桌面环境。在其他平台上，`Qt::ToolButtonFollowStyle` 仅指图标。
默认是`Qt::ToolButtonIconOnly`。

**如何使用：** 调用 `toolButtonStyle()` 读取当前值；它不会修改应用状态。

### `bool unifiedTitleAndToolBarOnMac() const`

**作用与语义：**

该属性决定了窗口是否使用macOS统一的标题和工具栏外观。
注意，Qt 5 的实现相比 Qt 4 存在若干限制：
- 不支持在 Windows 中使用 OpenGL 内容。这包括 `QOpenGLWidget`。
- 使用可停靠或可移动工具栏可能导致涂装错误，不建议使用

**如何使用：** 调用 `unifiedTitleAndToolBarOnMac()` 读取当前值；它不会修改应用状态。

### `void setAnimated(bool enabled)`

**作用与语义：**

该属性决定了操作 dock 控件和工具栏是否会被动画化。
当停靠点小部件或工具栏被拖曳到主窗口上时，主窗口会调整其内容，指示如果停靠点小部件或工具栏被放下，将停靠在哪里。设置该属性后，`QMainWindow`会以平滑的动画移动其内容。清除该属性后，内容物会自动吸附到新位置。
默认情况下，该属性是设置的。如果主窗口中存在的控件在调整大小或重新绘制时较慢，可能会清除该属性。
设置此属性与使用 `setDockOptions()` 设置 `AnimatedDocks` 选项相同。

**如何使用：** 调用 `setAnimated(...)` 修改 `animated`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setDockNestingEnabled(bool enabled)`

**作用与语义：**

该属性决定码头是否可以嵌套。
如果该属性`false`，停靠区域只能包含一行（水平或垂直）的停靠组件。如果该属性`true`，则停靠小部件所占用的区域可以向任一方向分割，以容纳更多的停靠小部件。
Dock嵌套仅在包含大量Dock小部件的应用中才是必要的。它让用户在组织主窗口时有更大的自由。然而，当将Dock小部件拖到主窗口上时，Dock嵌套会导致行为更复杂（且不那么直观），因为放置的Dock小部件可以有更多方式放置在Dock区域。
设置该属性与使用 `setDockOptions()` 设置 `AllowNestedDocks` 选项相同。

**如何使用：** 调用 `setDockNestingEnabled(...)` 修改 `dockNestingEnabled`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setUnifiedTitleAndToolBarOnMac(bool set)`

**作用与语义：**

该属性决定了窗口是否使用macOS统一的标题和工具栏外观。
注意，Qt 5 的实现相比 Qt 4 存在若干限制：
- 不支持在 Windows 中使用 OpenGL 内容。这包括 `QOpenGLWidget`。
- 使用可停靠或可移动工具栏可能导致涂装错误，不建议使用

**如何使用：** 调用 `setUnifiedTitleAndToolBarOnMac(...)` 修改 `unifiedTitleAndToolBarOnMac`；传入的新值会成为后续查询和相关界面行为所使用的值。

## 6. 深入实践与常见坑

### 生命周期和资源边界

控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

### 状态和错误边界

控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

### 线程边界

所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

### 最容易出现的错误

不要给 QMainWindow 直接 setLayout；中央控件只能有一个；saveState/restoreState 要配合稳定的 objectName；工具栏和 dock 的所有权通常由主窗口接管。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QMainWindow` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
