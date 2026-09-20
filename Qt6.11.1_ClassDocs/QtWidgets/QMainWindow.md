# QMainWindow

> Qt 6.11.1 · Qt Widgets · 来自 `QMainWindow`

## 1. 先建立直觉

**一句话定位：** `QMainWindow` 是传统桌面应用的主窗口框架，专门管理中央内容区、菜单栏、工具栏、状态栏和可停靠面板。

### 这是什么

`QMainWindow` 不是“更大的 QWidget”，它有一套专用布局。主窗口中心只有一个 central widget；菜单栏、工具栏、状态栏和 dock widget 都放在主窗口预定义区域里，而不是通过 `setLayout()` 管理。

写主窗口时，最稳的结构是：业务内容放进 central widget，命令抽象成 `QAction`，菜单和工具栏复用这些 action，辅助面板用 `QDockWidget`，临时信息放状态栏。

### 适合使用的场景

- 带菜单、工具栏、状态栏的桌面软件。
- 文档编辑器、IDE、数据分析工具、图像工具等有中央工作区和侧边面板的应用。
- 需要停靠面板、标签化 dock、保存/恢复窗口布局。

### 不适合的场景

- 只有一个简单控件的窗口：直接用 QWidget。
- 表单式弹窗：用 QDialog。
- 想用普通 layout 任意摆放菜单栏/工具栏/dock：QMainWindow 已经有固定布局模型。

### 最小示例

```cpp
#include <QApplication>
#include <QLabel>
#include <QMainWindow>
#include <QMenuBar>
#include <QStatusBar>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QMainWindow window;
    window.setWindowTitle(QStringLiteral("Editor"));
    window.setCentralWidget(new QLabel(QStringLiteral("Document area"), &window));
    window.menuBar()->addMenu(QObject::tr("&File"));
    window.statusBar()->showMessage(QObject::tr("Ready"));
    window.resize(900, 600);
    window.show();

    return QApplication::exec();
}
```

**先记住的坑：** 不要对 QMainWindow 调用 `setLayout()`；central widget 只有一个；保存/恢复 dock 和 toolbar 状态前要给相关对象设置稳定 `objectName`；`removeDockWidget()` 和 `removeToolBar()` 只是从主窗口移除，不一定删除对象。

## 2. 依赖与对象关系

- 头文件：`#include <QMainWindow>`
- CMake：`find_package(Qt6 REQUIRED COMPONENTS Widgets)`，并链接 `Qt6::Widgets`
- 继承自：`QWidget`
- 协作类：`QAction`、`QMenuBar`、`QToolBar`、`QStatusBar`、`QDockWidget`

### 主窗口布局模型

主窗口由中央区域和四周框架区域组成。`setCentralWidget()` 管中央区域；`menuBar()`/`setMenuBar()` 管菜单栏；`addToolBar()` 管工具栏区域；`addDockWidget()` 管 dock 区域；`statusBar()` 管底部状态栏。它们不是普通子控件布局关系。

### 所有权

传给 `setCentralWidget()`、`setMenuBar()`、`setStatusBar()`、`addToolBar()`、`addDockWidget()` 的控件通常由主窗口接管或重新设置 parent。用 `takeCentralWidget()` 可以取回中央控件所有权；移除 toolbar/dock 后是否删除由你自己决定。

### 状态持久化

`saveState()` 保存 toolbar/dock 布局，`restoreState()` 恢复。它依赖每个 dock 和 toolbar 的 `objectName()`，所以这些名字必须稳定，不能每次启动随机生成。

## 3. API 速查

| API | 用途速查 |
|---|---|
| `DockOption` / `DockOptions` | 控制 dock 是否动画、嵌套、标签化、强制标签化、垂直标签和分组拖动。 |
| `animated` / `setAnimated()` | 控制 dock 和 toolbar 拖动时是否使用动画。 |
| `dockNestingEnabled` / `setDockNestingEnabled()` | 是否允许 dock 区域再分割嵌套。 |
| `dockOptions` / `setDockOptions()` | 一次性设置 dock 行为组合。 |
| `documentMode` / `setDocumentMode()` | 让标签化 dock 使用文档模式外观。 |
| `iconSize` / `setIconSize()` / `iconSizeChanged()` | 控制主窗口工具栏图标尺寸。 |
| `tabShape` / `setTabShape()` | 控制 dock 标签页形状。 |
| `toolButtonStyle` / `setToolButtonStyle()` | 控制工具栏按钮图标/文字显示方式。 |
| `unifiedTitleAndToolBarOnMac` | macOS 上是否尝试统一标题栏和工具栏。 |
| `setCentralWidget()` / `centralWidget()` / `takeCentralWidget()` | 设置、读取、取出唯一中央控件。 |
| `menuBar()` / `setMenuBar()` / `menuWidget()` / `setMenuWidget()` | 管理主窗口菜单栏或自定义菜单控件。 |
| `statusBar()` / `setStatusBar()` | 管理状态栏。 |
| `addToolBar()` / `insertToolBar()` / `removeToolBar()` | 添加、插入、移除工具栏。 |
| `addToolBarBreak()` / `insertToolBarBreak()` / `removeToolBarBreak()` / `toolBarBreak()` | 管理工具栏换行分隔。 |
| `toolBarArea()` | 查询工具栏所在区域。 |
| `addDockWidget()` / `removeDockWidget()` / `dockWidgetArea()` | 添加、移除、查询 dock 面板位置。 |
| `splitDockWidget()` / `tabifyDockWidget()` / `tabifiedDockWidgets()` | 分割或标签化 dock 面板。 |
| `resizeDocks()` | 按方向调整一组 dock 的尺寸比例。 |
| `setCorner()` / `corner()` | 决定四个角落归哪个 dock 区域使用。 |
| `setTabPosition()` / `tabPosition()` | 设置指定 dock 区域的标签位置。 |
| `saveState()` / `restoreState()` / `restoreDockWidget()` | 保存、恢复主窗口 dock/toolbar 布局。 |
| `createPopupMenu()` / `contextMenuEvent()` | 生成或处理 toolbar/dock 显示开关菜单。 |
| `tabifiedDockWidgetActivated()` | 标签化 dock 当前页变化时发出。 |

## 4. API 逐项说明

### `DockOption` / `DockOptions`

`DockOption` 是 dock 行为开关，`DockOptions` 是它们的 flags 组合。`AnimatedDocks` 控制动画，`AllowNestedDocks` 允许区域分割，`AllowTabbedDocks` 允许标签化，`ForceTabbedDocks` 强制每个区域标签化，`VerticalTabs` 让侧边区域标签竖排，`GroupedDragging` 拖动一个标签时带着同组标签一起移动。除动画和垂直标签外，大多数选项最好在添加 dock 前设置。

### `animated : bool`

控制拖动 dock 或 toolbar 时是否有动画反馈。界面复杂、重绘慢或远程桌面场景可以关闭，减少拖动卡顿。它等价于 `dockOptions` 中的 `AnimatedDocks`。

### `dockNestingEnabled : bool`

控制 dock 区域是否可以嵌套分割。面板很多的 IDE 类应用适合打开；普通应用打开后会增加放置复杂度，用户不一定容易理解。

### `dockOptions : DockOptions`

集中配置 dock 行为。默认通常包含动画和标签化 dock。要稳定控制布局能力，建议在创建/添加所有 dock 前一次性设置。

### `documentMode : bool`

控制标签化 dock 的标签栏是否采用文档模式外观。它主要影响视觉风格，不改变 dock 的结构语义。

### `iconSize : QSize`

主窗口工具栏默认图标尺寸。设置后会影响主窗口管理的工具栏，并发出 `iconSizeChanged()`。如果单个 toolbar 需要例外，可在 toolbar 自身设置。

### `tabShape : QTabWidget::TabShape`

设置 dock 标签页形状。它影响标签化 dock 的外观，通常和平台风格保持一致即可。

### `toolButtonStyle : Qt::ToolButtonStyle`

控制工具栏按钮显示图标、文字或二者。桌面应用常用 `Qt::ToolButtonIconOnly` 或 `Qt::ToolButtonTextUnderIcon`。变化会发出 `toolButtonStyleChanged()`。

### `unifiedTitleAndToolBarOnMac : bool`

macOS 专用外观选项，尝试把标题栏和工具栏统一。只在 macOS 上有意义，且取决于平台风格和窗口配置。

### `QMainWindow(QWidget *parent, Qt::WindowFlags flags)`

创建主窗口。它可以有 QObject/QWidget parent，但常见主窗口通常是顶层窗口。`flags` 控制平台窗口类型和装饰。

### `~QMainWindow()`

销毁主窗口和由它拥有的菜单栏、状态栏、工具栏、dock、central widget 等子对象。退出时不要让后台任务继续回调已销毁窗口。

### `setCentralWidget(QWidget *widget)` / `centralWidget()` / `takeCentralWidget()`

中央控件是主窗口的主要内容区，只能有一个。复杂内容应先放进一个容器 QWidget，再把容器设为 central widget。`takeCentralWidget()` 会把当前中央控件从主窗口移走并交还给调用者，适合动态替换工作区。

### `menuBar()` / `setMenuBar()` / `setMenuWidget()`

`menuBar()` 懒创建并返回默认菜单栏；`setMenuBar()` 安装自定义 `QMenuBar`；`setMenuWidget()` 可以放任意 QWidget 作为菜单栏区域。标准桌面应用优先用 `menuBar()` 加菜单和 QAction。

### `statusBar()` / `setStatusBar()`

`statusBar()` 懒创建状态栏。短消息用 `showMessage()`，常驻状态控件可加到 status bar。`setStatusBar()` 用于替换成自定义状态栏对象。

### `addToolBar()` / `insertToolBar()` / `removeToolBar()`

工具栏承载 QAction，是菜单命令的可视快捷入口。`addToolBar()` 可指定区域或直接追加；`insertToolBar()` 插到已有 toolbar 前；`removeToolBar()` 只从主窗口拿掉，不等于删除对象。

### `addToolBarBreak()` / `insertToolBarBreak()` / `removeToolBarBreak()` / `toolBarBreak()`

这些 API 控制工具栏区域换行。工具栏很多时可以把它们分行显示。过度依赖固定换行会降低不同屏幕尺寸下的适应性。

### `toolBarArea(const QToolBar *toolbar)`

查询工具栏当前所在区域。保存自定义设置或根据位置更新 UI 时有用。

### `addDockWidget()` / `removeDockWidget()` / `dockWidgetArea()`

Dock 面板用于属性面板、项目树、日志窗口、搜索结果等辅助区域。`addDockWidget()` 把 dock 放到指定区域；带 orientation 的重载控制与已有 dock 的分割方向；`removeDockWidget()` 只是移除。`dockWidgetArea()` 查询当前位置。

### `splitDockWidget()` / `tabifyDockWidget()` / `tabifiedDockWidgets()`

`splitDockWidget()` 把两个 dock 分割并排；`tabifyDockWidget()` 把第二个 dock 标签化到第一个 dock 所在组；`tabifiedDockWidgets()` 查询同一标签组中的其他 dock。IDE 类布局常用这些 API 设置初始工作区。

### `resizeDocks()`

按水平或垂直方向调整一组 dock 的尺寸。传入的 sizes 是相对权重，Qt 会受最小尺寸和可用空间约束。适合恢复用户布局后的微调。

### `setCorner()` / `corner()`

四个角落会同时接触两个 dock 区域，`setCorner()` 决定角落属于哪一侧。侧边栏和底部面板同时存在时，这会影响可用空间分配。

### `setTabPosition()` / `tabPosition()`

设置某些 dock 区域标签页出现的位置。侧边 dock 可用左右标签，底部 dock 可用上下标签。视觉上要考虑平台习惯和可读性。

### `saveState(int version)` / `restoreState(const QByteArray &state, int version)`

保存和恢复 toolbar/dock 布局。`version` 是你自己的布局版本号；改变 dock 结构或 objectName 后应升级版本或处理恢复失败。恢复前要先创建并命名所有相关 toolbar/dock。

### `restoreDockWidget(QDockWidget *dockwidget)`

在主窗口状态已经恢复后，把稍后创建的 dock 放回保存状态中的位置。插件式界面很有用。前提仍然是 objectName 稳定。

### `createPopupMenu()` / `contextMenuEvent()`

默认右键主窗口 toolbar/dock 区域时，会生成一个可勾选显示隐藏 toolbar/dock 的菜单。重写 `createPopupMenu()` 可以定制这个菜单；重写 `contextMenuEvent()` 则能完全改右键行为。

### `event(QEvent *event)`

处理主窗口内部事件。通常不用重写；如果重写，不处理的事件交给基类，避免破坏 dock、toolbar、菜单等框架行为。

### `iconSizeChanged()` / `toolButtonStyleChanged()`

当主窗口工具栏图标尺寸或工具按钮样式变化时发出。自定义工具栏或外部设置页可连接它同步显示。

### `tabifiedDockWidgetActivated(QDockWidget *dockWidget)`

标签化 dock 当前页变化时发出。可用来更新属性面板状态、懒加载 dock 内容或记录用户最近使用的面板。

## 5. 深入实践与常见坑

### 不要 setLayout

`QMainWindow` 已经有自己的内部布局。应用内容放到 central widget，central widget 内部再用普通布局。

### QAction 是命令中心

菜单项、工具栏按钮和快捷键应尽量共享同一个 QAction。这样启用状态、文本、图标、快捷键和 triggered 逻辑只维护一份。

### objectName 决定恢复质量

`saveState()` 依靠 toolbar/dock 的 `objectName()` 匹配对象。名字变了，恢复就会失败或错位。用户配置版本升级时要认真处理。

### Dock 能力不要一次全开

嵌套、标签化、分组拖动都很强，但也会增加用户理解成本。普通应用通常允许标签化就够了；IDE 类应用才需要更复杂的 dock 自由度。

### 主窗口只是壳

不要把所有业务逻辑都塞进 QMainWindow 子类。主窗口负责装配 action、菜单、工具栏和页面；文档状态、数据加载、模型和命令逻辑应拆到独立对象。
