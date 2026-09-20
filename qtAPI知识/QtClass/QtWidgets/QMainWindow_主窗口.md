# Qt QMainWindow 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）  
> 头文件：`#include <QMainWindow>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QWidget -> QMainWindow`  
> 定位：带菜单、工具栏、停靠面板和状态栏的主窗口框架

## 1. QMainWindow 解决什么问题

`QMainWindow` 不是普通窗口的“加强版 QWidget”，而是一套现成的应用壳：

- 中间放工作区；
- 上面放菜单栏和工具栏；
- 四周放可停靠面板；
- 底部放状态栏；
- 允许把这些区域保存/恢复到上次布局。

典型场景就是编辑器、IDE、管理后台、调试工具、图形软件。  
如果你的窗口只有一块表单或一个内容区，直接用 `QWidget + QLayout` 更轻；如果你需要这些“壳层”，才该上 `QMainWindow`。

它自带内部布局，别再给它 `setLayout()`；正确做法是把内容分别放进中央区域、菜单栏、工具栏和停靠区域。

```text
QMainWindow
├─ menuBar / menuWidget
├─ toolbars
├─ dock widgets
├─ centralWidget
└─ statusBar
```

## 2. 最小可用示例

```cpp
#include <QApplication>
#include <QDockWidget>
#include <QLabel>
#include <QMainWindow>
#include <QStatusBar>
#include <QTextEdit>

class MainWindow final : public QMainWindow
{
public:
    MainWindow()
    {
        setWindowTitle(tr("示例主窗口"));

        auto *editor = new QTextEdit;
        setCentralWidget(editor);

        auto *dock = new QDockWidget(tr("项目"), this);
        dock->setObjectName("projectDock");
        dock->setWidget(new QLabel(tr("项目树")));
        addDockWidget(Qt::LeftDockWidgetArea, dock);

        statusBar()->showMessage(tr("就绪"));
    }
};
```

`QMainWindow` 构造后就是顶层窗口类型；传入 `parent` 主要是对象所有权和对象树关系，不会让它变成普通子控件。

## 3. 主窗口的四个核心区域

### 3.1 中央区域

```cpp
setCentralWidget(new QTextEdit);
```

中央区域是主窗口最重要的工作区。它可以是文本编辑器、视图、`QMdiArea`、自定义画布，甚至是另一个复杂容器。  
`setCentralWidget()` 会把旧中央控件替换掉，`takeCentralWidget()` 则把中央控件取走并把所有权交给调用方。

### 3.2 菜单栏

```cpp
menuBar()->addMenu(tr("&File"));
```

`menuBar()` 会在需要时懒创建一个 `QMenuBar`。如果你想用自定义菜单容器，不用 `QMenuBar` 本体，就改用 `setMenuWidget()`。

### 3.3 工具栏

```cpp
auto *tb = addToolBar(tr("Main"));
tb->addAction(tr("Refresh"));
```

工具栏适合高频操作。`QMainWindow` 负责工具栏区域的停靠、换行、拖拽和样式同步。

### 3.4 停靠面板

```cpp
auto *dock = new QDockWidget(tr("输出"), this);
dock->setWidget(new QTextEdit);
addDockWidget(Qt::BottomDockWidgetArea, dock);
```

停靠面板由 `QDockWidget` 提供，`QMainWindow` 只负责摆放和状态管理。  
如果要让两个 dock 并排或上下分开，用 `splitDockWidget()`；如果要标签化，用 `tabifyDockWidget()`。

## 4. DockOptions：主窗口的停靠行为总开关

`dockOptions()` 是主窗口停靠策略的总配置。默认值是 `AnimatedDocks | AllowTabbedDocks`。

| 选项 | 是什么 | 适合什么场景 |
| --- | --- | --- |
| `AnimatedDocks` | 拖动停靠时做平滑动画。 | 大多数界面默认保留。 |
| `AllowNestedDocks` | 允许同一停靠区再分割出多层。 | 面板很多、需要自由排布时。 |
| `AllowTabbedDocks` | 允许把一个 dock 压到另一个 dock 上形成标签页。 | 多面板切换场景。 |
| `ForceTabbedDocks` | 每个停靠区只保留一组标签页，不允许并排。 | 想强制“一个区只是一叠标签”时。 |
| `VerticalTabs` | 左右两侧区域的标签竖排。 | 面板多且希望更节省横向空间。 |
| `GroupedDragging` | 拖动某个标签时，把同组标签一起拖走。 | 标签组稳定、规则简单时。 |

几个实际规则要记住：

- `AnimatedDocks` 等同于 `animated` 属性；
- `AllowNestedDocks` 等同于 `dockNestingEnabled`；
- `ForceTabbedDocks` 会让 `AllowNestedDocks` 失效；
- `VerticalTabs` 和 `GroupedDragging` 都隐含 `AllowTabbedDocks`；
- 这些选项更适合在添加 dock 之前设置，尤其是影响布局结构的选项。

## 5. 菜单栏、状态栏和自定义菜单

### 5.1 `menuBar()` / `setMenuBar()`

`menuBar()` 会在不存在时创建一个默认菜单栏。  
`setMenuBar()` 用你自己的 `QMenuBar` 替换它，`QMainWindow` 会接管所有权。

### 5.2 `menuWidget()` / `setMenuWidget()`

`menuWidget()` 返回当前菜单栏容器。  
`setMenuWidget()` 用于彻底替换成自定义 widget，不一定是 `QMenuBar`。

### 5.3 `statusBar()` / `setStatusBar()`

`statusBar()` 会懒创建一个空状态栏。  
`setStatusBar()` 则直接塞入你自己的 `QStatusBar`；传 `nullptr` 可以移除它。

### 5.4 `createPopupMenu()`

默认情况下，主窗口右键时会给出一个弹出菜单，里面通常是工具栏和停靠面板的可见性勾选项。  
如果你要一个更适合业务的“视图”菜单，就重写 `createPopupMenu()`。

## 6. 工具栏与停靠面板的排布

### 6.1 工具栏

```cpp
auto *fileBar = addToolBar(tr("File"));
addToolBar(Qt::TopToolBarArea, fileBar);
addToolBarBreak();
insertToolBarBreak(fileBar);
```

`addToolBar()` 把工具栏放进指定区域，默认放到顶部。  
`insertToolBar()` 是插到某个工具栏前面。  
`addToolBarBreak()` / `insertToolBarBreak()` 负责在同一区域里换行。

### 6.2 停靠面板

```cpp
addDockWidget(Qt::LeftDockWidgetArea, dock);
addDockWidget(Qt::LeftDockWidgetArea, dock, Qt::Vertical);
splitDockWidget(firstDock, secondDock, Qt::Horizontal);
tabifyDockWidget(firstDock, secondDock);
```

`addDockWidget(area, dock)` 是最常规的加入方式。  
带 `orientation` 的重载决定新 dock 进入该区域时是按横向还是纵向分割。  
`splitDockWidget()` 是在已有 dock 旁边再切一块。  
`tabifyDockWidget()` 是把第二个 dock 压到第一个 dock 上，形成标签页。

`dockWidgetArea(dock)` 可以查询一个 dock 当前在哪个区域；如果根本没加入主窗口，会返回 `Qt::NoDockWidgetArea`。  
`removeDockWidget()` 只会把 dock 从布局里拿掉并隐藏它，不会删除对象本身。  
`restoreDockWidget()` 则用于在 `restoreState()` 之后，给后来创建的 dock 补回原位置。

### 6.3 分隔与角落

```cpp
setCorner(Qt::TopLeftCorner, Qt::LeftDockWidgetArea);
```

`setCorner()` 决定四个角归哪个 dock 区域占用。  
`corner()` 用来反查这个设置。  
`isSeparator(const QPoint &pos)` 可理解为一个分隔条命中测试，常用于判断鼠标点到了主窗口布局里的分隔区域。

## 7. 状态保存与恢复

`saveState()` / `restoreState()` 是 QMainWindow 最值钱的地方之一。它们保存的不是窗口几何本身，而是工具栏和 dock 的布局状态，包括位置、大小、标签化和角落配置。

```cpp
settings.setValue("windowState", saveState(1));
restoreState(settings.value("windowState").toByteArray(), 1);
```

使用时注意：

- 每个 `QToolBar` 和 `QDockWidget` 都要有稳定唯一的 `objectName`；
- 保存和恢复时，dock/toolbar 的名字、数量和版本号要一致；
- `restoreState()` 返回 `false` 时，通常是版本不匹配或状态数据不合法；
- `restoreDockWidget()` 适合“状态先恢复，dock 后创建”的场景。

如果你还想恢复窗口位置和大小，配套用 `saveGeometry()` / `restoreGeometry()`，它们和 `saveState()` 不是一回事。

## 8. 什么时候用哪些属性

| 属性 / API | 是什么 | 典型用途 |
| --- | --- | --- |
| `animated` / `isAnimated()` / `setAnimated()` | 控制 dock 和工具栏拖动时是否动画。 | 界面拖动反馈。 |
| `dockNestingEnabled` / `isDockNestingEnabled()` / `setDockNestingEnabled()` | 控制是否允许多层分割停靠。 | 面板多的复杂工作台。 |
| `dockOptions()` / `setDockOptions()` | 一次设置整套停靠策略。 | 初始化主窗口布局规则。 |
| `documentMode` / `setDocumentMode()` | 让 tabified dock 看起来更像文档页。 | 编辑器、文档管理界面。 |
| `iconSize()` / `setIconSize()` | 读取或设置工具栏图标尺寸。 | 统一工具栏视觉密度。 |
| `tabShape()` / `setTabShape()` | 读取或设置 dock 标签形状。 | 调整标签外观风格。 |
| `toolButtonStyle()` / `setToolButtonStyle()` | 读取或设置工具栏按钮风格。 | 图标、文字、图文并列。 |
| `unifiedTitleAndToolBarOnMac()` / `setUnifiedTitleAndToolBarOnMac()` | macOS 上统一标题栏和工具栏。 | 仅 macOS，且要谨慎配合 dockable toolbar。 |

## 9. 选择和使用细节

### 9.1 `iconSize`

`iconSize()` 返回当前主窗口工具栏图标尺寸。  
`setIconSize()` 可以统一所有工具栏图标大小。Qt 只会把图标缩小到合适尺寸，尽量别拿很小的图标去硬撑大尺寸。

### 9.2 `tabShape`

`tabShape()` 和 `setTabShape()` 只影响 tabified dock 的标签形状。  
默认是 `QTabWidget::Rounded`。

### 9.3 `tabPosition`

`tabPosition(area)` 和 `setTabPosition(areas, pos)` 控制每个 dock 区域的标签位置。  
注意 `VerticalTabs` 会覆盖这里的设置。

### 9.4 `toolButtonStyle`

`toolButtonStyle()` / `setToolButtonStyle()` 控制工具栏按钮是只显示图标、只显示文字还是图文并排。  
如果想跟随系统风格，可以设为 `Qt::ToolButtonFollowStyle`。

### 9.5 `unifiedTitleAndToolBarOnMac`

这是 macOS 专用的窗口统一外观选项。  
只适合你真想要那种一体化标题栏时用，而且和可拖动/可停靠工具栏搭配时要更谨慎。

## API 速查表
### 10.1 公共类型

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型 | `DockOption` | 描述主窗口 dock 系统行为的单个选项。 | 单个枚举值通常不会单独存，用来组合成 `DockOptions`。 |
| 类型 | `DockOptions` | `DockOption` 的 flags 集合。 | 用 `|` 组合，用 `testFlag()` 或按位判断读取。 |
| 选项 | `AnimatedDocks` | 让 dock 和工具栏拖动、停靠时带动画。 | 默认常开；重绘压力大或调试布局时可以关闭。 |
| 选项 | `AllowNestedDocks` | 允许停靠区被继续分割成多层。 | 面板很多时有用；简单软件开太自由反而不好用。 |
| 选项 | `AllowTabbedDocks` | 允许多个 dock 叠成标签页。 | 属性、输出、搜索结果这类互斥查看面板很适合。 |
| 选项 | `ForceTabbedDocks` | 强制每个停靠区只采用标签堆叠。 | 会压住嵌套分割能力，适合想限制用户布局自由度的界面。 |
| 选项 | `VerticalTabs` | 左右 dock 区域的标签竖排。 | 隐含标签化；标签多时省横向空间。 |
| 选项 | `GroupedDragging` | 拖动标签化 dock 时连同同组标签一起移动。 | 标签组语义稳定时好用；复杂布局里要小心用户预期。 |

### 10.2 构造、属性与基础访问器

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QMainWindow(QWidget *parent = nullptr, Qt::WindowFlags flags = {})` | 创建一个带中央区、菜单栏、工具栏、dock 区和状态栏的主窗口框架。 | 不要给它直接 `setLayout()`；内容要放进专门区域。 |
| 析构 | `~QMainWindow()` | 销毁主窗口和父子对象树里的子对象。 | 中央控件、工具栏、状态栏等被接管后通常由主窗口释放。 |
| 工具栏属性 | `iconSize() const` / `setIconSize(const QSize &iconSize)` | 读取或统一设置工具栏图标尺寸。 | Qt 会按样式处理缩放，最好提供足够清晰的图标资源。 |
| 工具栏属性 | `toolButtonStyle() const` / `setToolButtonStyle(Qt::ToolButtonStyle toolButtonStyle)` | 读取或统一设置工具栏按钮显示方式。 | 可控制只图标、只文字、文字在旁边或跟随系统。 |
| 停靠属性 | `isAnimated() const` / `setAnimated(bool enabled)` | 读取或设置 dock/toolbar 停靠动画。 | 等同于 `AnimatedDocks` 选项的便捷接口。 |
| 停靠属性 | `isDockNestingEnabled() const` / `setDockNestingEnabled(bool enabled)` | 读取或设置是否允许多层嵌套停靠。 | 等同于 `AllowNestedDocks`；和 `ForceTabbedDocks` 同时使用时要注意优先级。 |
| 标签属性 | `documentMode() const` / `setDocumentMode(bool enabled)` | 让标签化 dock 使用更接近文档页的外观。 | 常见于 IDE 和编辑器风格界面。 |
| 标签属性 | `tabShape() const` / `setTabShape(QTabWidget::TabShape tabShape)` | 读取或设置 dock 标签形状。 | 只影响 tabified dock 的标签，不影响中央区普通 `QTabWidget`。 |
| 标签属性 | `tabPosition(Qt::DockWidgetArea area) const` / `setTabPosition(Qt::DockWidgetAreas areas, QTabWidget::TabPosition tabPosition)` | 查询或设置各 dock 区域的标签位置。 | `VerticalTabs` 会覆盖左右区域的常规标签位置设置。 |
| 停靠策略 | `dockOptions() const` / `setDockOptions(DockOptions options)` | 读取或设置整套 dock 行为策略。 | 影响布局结构的选项最好在添加 dock 之前设置。 |
| macOS 外观 | `unifiedTitleAndToolBarOnMac() const` / `setUnifiedTitleAndToolBarOnMac(bool set)` | 控制 macOS 上标题栏和工具栏一体化显示。 | 平台相关；可停靠工具栏下要多测试外观与拖拽。 |

### 10.3 菜单、状态栏和中央区域

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 菜单栏 | `menuBar() const` | 返回菜单栏；没有时自动创建默认 `QMenuBar`。 | 最常用入口，适合普通桌面应用菜单。 |
| 菜单栏 | `setMenuBar(QMenuBar *menubar)` | 替换主窗口菜单栏。 | 主窗口接管所有权；别再把同一个菜单栏塞给别处。 |
| 菜单容器 | `menuWidget() const` | 返回当前菜单区域的 widget。 | 可能是 `QMenuBar`，也可能是自定义 widget。 |
| 菜单容器 | `setMenuWidget(QWidget *menubar)` | 用任意 widget 替换菜单区域。 | 适合自定义标题/菜单区域，但会放弃标准菜单栏的一些平台行为。 |
| 状态栏 | `statusBar() const` | 返回状态栏；没有时自动创建空 `QStatusBar`。 | 适合显示就绪状态、临时提示、坐标等低频信息。 |
| 状态栏 | `setStatusBar(QStatusBar *statusbar)` | 设置或替换状态栏。 | 主窗口接管所有权；传空可移除状态栏。 |
| 中央区 | `centralWidget() const` | 返回当前中央工作区控件。 | 没有设置时返回空指针。 |
| 中央区 | `setCentralWidget(QWidget *widget)` | 设置主窗口中间的核心工作区。 | 主窗口接管所有权；旧中央控件会被替换。 |
| 中央区 | `takeCentralWidget()` | 从主窗口取走中央控件并返回指针。 | 所有权交还调用者，之后要自己决定复用或删除。 |

### 10.4 工具栏、停靠面板和区域管理

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 工具栏 | `addToolBar(Qt::ToolBarArea area, QToolBar *toolbar)` | 把已有工具栏加入指定区域。 | 如果工具栏已在主窗口中，会移动到新区域。 |
| 工具栏 | `addToolBar(QToolBar *toolbar)` | 把已有工具栏加入默认顶部区域。 | 适合常规主工具栏。 |
| 工具栏 | `addToolBar(const QString &title)` | 创建一个工具栏，设置标题并加入顶部区域。 | 返回的 `QToolBar` 由主窗口托管，可继续添加 action。 |
| 工具栏 | `insertToolBar(QToolBar *before, QToolBar *toolbar)` | 把工具栏插到另一个工具栏前。 | 两者都应属于同一个主窗口工具栏系统。 |
| 工具栏 | `removeToolBar(QToolBar *toolbar)` | 从主窗口工具栏布局中移除并隐藏。 | 不会删除对象，后续可重新添加。 |
| 工具栏换行 | `addToolBarBreak(Qt::ToolBarArea area = Qt::TopToolBarArea)` | 在指定工具栏区域增加一个换行断点。 | 适合把同一区域的工具栏分成多行。 |
| 工具栏换行 | `insertToolBarBreak(QToolBar *before)` | 在指定工具栏前插入换行断点。 | 调整已有工具栏排列时使用。 |
| 工具栏换行 | `removeToolBarBreak(QToolBar *before)` | 移除某工具栏前的换行断点。 | 只影响布局，不影响工具栏对象本身。 |
| 工具栏查询 | `toolBarArea(const QToolBar *toolbar) const` | 查询工具栏当前所在区域。 | 未加入主窗口时通常返回 `Qt::NoToolBarArea`。 |
| 工具栏查询 | `toolBarBreak(QToolBar *toolbar) const` | 判断该工具栏前是否存在换行。 | 保存或诊断工具栏排列时有用。 |
| Dock 添加 | `addDockWidget(Qt::DockWidgetArea area, QDockWidget *dockwidget)` | 把 dock 面板加入指定停靠区域。 | dock 必须是 `QDockWidget`，真实内容放在 dock 内部。 |
| Dock 添加 | `addDockWidget(Qt::DockWidgetArea area, QDockWidget *dockwidget, Qt::Orientation orientation)` | 加入 dock，并指定与同区已有 dock 的分割方向。 | 适合初始化时精确控制面板横向/纵向排列。 |
| Dock 排布 | `splitDockWidget(QDockWidget *first, QDockWidget *second, Qt::Orientation orientation)` | 把 `second` 放到 `first` 旁边并分割区域。 | `first` 必须已经在主窗口中；标签化状态会影响实际结果。 |
| Dock 排布 | `tabifyDockWidget(QDockWidget *first, QDockWidget *second)` | 把第二个 dock 叠到第一个 dock 上形成标签组。 | 两个 dock 都应由同一主窗口管理。 |
| Dock 查询 | `tabifiedDockWidgets(QDockWidget *dockwidget) const` | 返回和指定 dock 同组的其他标签化 dock。 | 只对已经标签化的 dock 有意义。 |
| Dock 移除 | `removeDockWidget(QDockWidget *dockwidget)` | 从主窗口布局移除 dock 并隐藏。 | 不删除对象，常用于临时隐藏或转移面板。 |
| Dock 恢复 | `restoreDockWidget(QDockWidget *dockwidget)` | 将后来创建的 dock 放回保存状态里的位置。 | 通常在 `restoreState()` 后动态补建 dock 时使用。 |
| Dock 查询 | `dockWidgetArea(QDockWidget *dockwidget) const` | 查询 dock 当前停靠在哪个区域。 | 没加入主窗口时返回 `Qt::NoDockWidgetArea`。 |
| Dock 尺寸 | `resizeDocks(const QList<QDockWidget *> &docks, const QList<int> &sizes, Qt::Orientation orientation)` | 批量调整一组 dock 的相对尺寸。 | 尺寸是同一方向上的目标分配，最终会受最小尺寸约束。 |
| 角落 | `setCorner(Qt::Corner corner, Qt::DockWidgetArea area)` | 设置主窗口四个角落归哪个 dock 区域占用。 | 左上、右上、左下、右下会影响 dock 区域交界处的布局。 |
| 角落 | `corner(Qt::Corner corner) const` | 查询某个角落当前归属区域。 | 调试复杂 dock 排布时很有用。 |
| 命中测试 | `isSeparator(const QPoint &pos) const` | 判断位置是否落在主窗口布局分隔条上。 | 做自定义交互或调试鼠标区域时才会用到。 |

### 10.5 状态保存、弹出菜单和信号

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 状态保存 | `saveState(int version = 0) const` | 保存工具栏和 dock 的布局状态。 | 依赖 `QToolBar/QDockWidget` 稳定唯一的 `objectName`。 |
| 状态恢复 | `restoreState(const QByteArray &state, int version = 0)` | 恢复之前保存的主窗口布局状态。 | 版本不匹配或数据无效会返回 `false`。 |
| 右键菜单 | `createPopupMenu()` | 创建主窗口默认弹出菜单。 | 默认通常包含工具栏和 dock 的显示隐藏项；可重写成业务菜单。 |
| 信号 | `iconSizeChanged(const QSize &iconSize)` | 工具栏图标尺寸变化时发出。 | 用来同步自定义工具区或设置界面。 |
| 信号 | `toolButtonStyleChanged(Qt::ToolButtonStyle toolButtonStyle)` | 工具栏按钮样式变化时发出。 | 适合把全局显示风格同步给外部按钮。 |
| 信号 | `tabifiedDockWidgetActivated(QDockWidget *dockWidget)` | 标签化 dock 中某个面板被激活时发出。 | 用于更新属性面板、菜单勾选或状态提示。 |

### 10.6 受保护函数

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 事件 | `contextMenuEvent(QContextMenuEvent *event)` | 处理主窗口右键菜单事件。 | 默认会走 `createPopupMenu()`；重写时要决定是否保留默认视图菜单。 |
| 事件 | `event(QEvent *event)` | 主窗口事件总入口。 | 只有处理特殊事件或平台行为时才建议重写。 |

---

### 一句话总结

`QMainWindow` 是主窗口壳层：中央区放工作内容，四周放菜单、工具栏、dock 和状态栏；`dockOptions` 决定停靠规则，`saveState()/restoreState()` 负责记住布局，`QDockWidget` 和 `QToolBar` 才是它真正承载的对象。
