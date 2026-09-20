# Qt QDockWidget 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）  
> 头文件：`#include <QDockWidget>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QWidget -> QDockWidget`  
> 常见搭档：`QMainWindow`、`QAction`

## 1. QDockWidget 解决什么问题

`QDockWidget` 是主窗口里的“可停靠面板容器”。它允许一个工具面板在主窗口边缘停靠、与其他面板标签化、拆成浮动窗口，也允许用户通过标题栏关闭或重新显示。

典型用途：

- 左侧项目树、右侧属性编辑器；
- 底部编译输出、日志和搜索结果；
- 可由用户自由布局的工具箱、监视器和调试面板。

它本身不是内容控件，而是一个带标题栏和停靠行为的外壳：

```text
QMainWindow
├─ centralWidget       中央工作区
├─ QDockWidget         停靠面板
│  └─ QWidget          真正的面板内容
└─ QToolBar / QMenu    操作入口
```

不要把需要停靠的内容直接 `addWidget()` 到 `QMainWindow`；应该先创建内容控件，再通过 `setWidget()` 放进 `QDockWidget`，最后调用 `QMainWindow::addDockWidget()`。

## 2. 最小可用示例

```cpp
#include <QDockWidget>
#include <QLabel>
#include <QMainWindow>

auto *dock = new QDockWidget(tr("项目"), mainWindow);
dock->setObjectName("projectDock"); // 状态保存/恢复需要稳定 objectName
dock->setAllowedAreas(Qt::LeftDockWidgetArea |
                      Qt::RightDockWidgetArea);
dock->setWidget(new QLabel(tr("项目树内容")));

mainWindow->addDockWidget(Qt::LeftDockWidgetArea, dock);
mainWindow->menuBar()->addAction(dock->toggleViewAction());
```

`QDockWidget` 需要放到 `QMainWindow` 的停靠区域中才会获得完整的拖拽和浮动行为。单独创建并 `show()` 只能得到一个普通顶层窗口式控件，不能替代主窗口的停靠管理。

## 3. `setWidget()`：容器和内容分工

`QDockWidget` 负责标题栏、关闭/浮动按钮和停靠状态；尺寸提示、最小尺寸、最大尺寸和布局应由传入的内容控件负责。

```cpp
auto *panel = new QWidget;
auto *layout = new QVBoxLayout(panel);
layout->addWidget(new QLabel(tr("日志")));
layout->addWidget(new QTextEdit);

auto *dock = new QDockWidget(tr("输出"), mainWindow);
dock->setObjectName("outputDock");
dock->setWidget(panel);
mainWindow->addDockWidget(Qt::BottomDockWidgetArea, dock);
```

要点：

- 先给内容控件设置布局，再调用 `setWidget()`；
- 如果 dock 已经可见，后来才设置内容控件，通常还需要对内容控件调用 `show()`；
- 尺寸约束尽量设置在内容控件上，不要把固定宽高写死在 `QDockWidget` 上。停靠和浮动时标题栏、边框尺寸不同；
- `setWidget(nullptr)` 可以移除内容，但不会替你定义“旧内容接下来由谁负责销毁”的业务语义。

## 4. 允许停靠的位置与当前位置

```cpp
dock->setAllowedAreas(Qt::LeftDockWidgetArea |
                      Qt::RightDockWidgetArea);

if (dock->isAreaAllowed(Qt::BottomDockWidgetArea)) {
    // 当前策略允许用户把面板拖到底部
}
```

`allowedAreas` 是“用户可以停靠到哪里”的限制，不是当前所在位置。Qt 6.9 起，`dockLocation` 表示当前停靠区域：

```cpp
Qt::DockWidgetArea area = dock->dockLocation();
dock->setDockLocation(Qt::RightDockWidgetArea);
dock->setDockLocation(Qt::NoDockLocation); // 等价于设为浮动
```

当面板浮动，或它没有属于某个 `QMainWindow` 时，`dockLocation()` 返回 `Qt::NoDockLocation`。调用 `setDockLocation()` 时，目标区域还必须在 `allowedAreas()` 中，否则不能把它当作任意区域强制使用。

## 5. floating、features 与标题栏

### 5.1 浮动状态

```cpp
dock->setFloating(true);  // 变成独立浮动窗口
dock->setFloating(false); // 回到主窗口的停靠布局
bool floating = dock->isFloating();
```

浮动窗口仍然是主窗口管理的 dock，不要把它当成完全独立的业务窗口。要观察状态变化，连接 `topLevelChanged(bool)`。

### 5.2 功能开关

```cpp
dock->setFeatures(QDockWidget::DockWidgetClosable |
                  QDockWidget::DockWidgetMovable |
                  QDockWidget::DockWidgetFloatable);
```

可以禁用关闭、拖动或浮动。例如一个必须始终存在的导航面板可以去掉 `DockWidgetClosable`；一个只允许停靠、不允许独立窗口的区域可以去掉 `DockWidgetFloatable`。

`DockWidgetVerticalTitleBar` 只控制标题栏方向，不代表面板内容也会自动旋转。判断位标志时用按位与：

```cpp
if (dock->features() & QDockWidget::DockWidgetVerticalTitleBar) {
    // 标题栏按垂直停靠样式处理
}
```

### 5.3 自定义标题栏

```cpp
auto *titleBar = new QWidget;
auto *titleLayout = new QHBoxLayout(titleBar);
titleLayout->addWidget(new QLabel(tr("属性")));
titleLayout->addStretch();

dock->setTitleBarWidget(titleBar);
```

传入 `nullptr` 会移除自定义标题栏并恢复默认标题栏，但被移除的 widget 不会自动删除。自定义标题栏还意味着浮动时不会使用原生窗口装饰，因此关闭、浮动和拖动按钮通常要由自己的标题栏实现或明确保留替代入口。

## 6. 用 `toggleViewAction()` 接入菜单

```cpp
viewMenu->addAction(projectDock->toggleViewAction());
```

这个函数返回一个由 `QDockWidget` 所有的可勾选 `QAction`。它的文本会跟随 dock 的窗口标题，勾选状态表示面板是否可见，适合直接放入“视图”菜单或工具栏。

它的职责是给用户一个显示/隐藏入口，不是让程序执行显示/隐藏。程序主动控制可见性应使用：

```cpp
dock->setVisible(true);
dock->hide();
dock->show();
```

不要删除 `toggleViewAction()` 返回的 action，也不要把它保存成一个脱离 dock 生命周期的独立对象。

## 7. 保存和恢复主窗口布局

`QDockWidget` 的停靠位置、浮动状态、标签化关系等通常由 `QMainWindow::saveState()` 保存，而不是由 dock 自己单独保存：

```cpp
settings.setValue("windowState", mainWindow->saveState(1));
```

恢复时：

```cpp
mainWindow->restoreState(
    settings.value("windowState").toByteArray(), 1);
```

要让恢复可靠：

- 每个 dock 使用稳定且唯一的 `objectName`；
- 保存和恢复时创建的 dock 集合、objectName 和版本号保持一致；
- 改变布局结构后递增 `version`，避免旧状态误套到新布局；
- `restoreState()` 必须在相关 dock 已创建并加入主窗口之后调用；
- `restoreState()` 返回 `false` 时检查状态数据是否为空、版本是否匹配以及 objectName 是否变化。

## API 速查表
### 8.1 类型与构造

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型 | `DockWidgetFeature` | 表示 dock 可用功能的单个枚举位。 | 单个位通常组合成 `DockWidgetFeatures` 使用。 |
| 功能位 | `DockWidgetClosable` | 允许用户关闭 dock。 | 关闭只是隐藏，仍可通过 `toggleViewAction()` 或代码重新显示。 |
| 功能位 | `DockWidgetMovable` | 允许用户拖动 dock 改变停靠位置。 | 取消后用户不能拖，程序仍可调用主窗口 API 调整位置。 |
| 功能位 | `DockWidgetFloatable` | 允许用户把 dock 拆成浮动窗口。 | 浮动仍属于 dock 系统，不等于独立业务对话框。 |
| 功能位 | `DockWidgetVerticalTitleBar` | 使用垂直标题栏样式。 | 只影响标题栏方向，不会旋转内容控件。 |
| 功能位 | `DockWidgetFeatureMask` | 公开功能位的掩码。 | 一般只在过滤或调试 flags 时碰到。 |
| 功能位 | `NoDockWidgetFeatures` | 禁用关闭、移动、浮动等用户操作。 | 适合必须固定存在的面板。 |
| 功能位 | `Reserved` | Qt 内部保留位。 | 不要在业务代码里依赖它。 |
| 类型 | `DockWidgetFeatures` | 多个 `DockWidgetFeature` 的 flags 集合。 | 用 `|` 组合，用 `&` 或 `testFlag()` 判断。 |
| 构造 | `QDockWidget(QWidget *parent = nullptr, Qt::WindowFlags flags = {})` | 创建无标题 dock 容器。 | 后续用 `setWindowTitle()` 设置标题；一般以 `QMainWindow` 为父对象。 |
| 构造 | `QDockWidget(const QString &title, QWidget *parent = nullptr, Qt::WindowFlags flags = {})` | 创建带标题的 dock 容器。 | 标题会影响默认标题栏和 `toggleViewAction()` 的文本。 |
| 析构 | `~QDockWidget()` | 销毁 dock 及其子对象。 | 内容控件若已设为子对象，通常会一起释放。 |

### 8.2 内容、停靠和窗口状态

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 内容 | `widget() const` | 返回 dock 里面真正承载业务 UI 的内容控件。 | 没设置内容时返回空指针。 |
| 内容 | `setWidget(QWidget *widget)` | 把业务控件放进 dock 容器。 | 内容控件应先建好布局；尺寸策略主要写在内容控件上。 |
| 功能 | `features() const` | 读取当前功能位集合。 | 用来判断是否允许关闭、移动、浮动或垂直标题栏。 |
| 功能 | `setFeatures(DockWidgetFeatures features)` | 设置用户可操作的 dock 功能。 | 修改后发 `featuresChanged()`；它控制用户操作，不代表程序完全不能改。 |
| 浮动 | `isFloating() const` | 判断 dock 当前是否以浮动窗口显示。 | 比检查 window flags 更直观。 |
| 浮动 | `setFloating(bool floating)` | 在浮动和停靠状态之间切换。 | 需要 dock 已经归 `QMainWindow` 管理，行为才完整。 |
| 停靠限制 | `allowedAreas() const` | 返回允许停靠到哪些区域。 | 这是允许范围，不是当前位置。 |
| 停靠限制 | `setAllowedAreas(Qt::DockWidgetAreas areas)` | 限制用户可把 dock 拖到哪些区域。 | 例如只允许左侧和右侧，避免面板跑到不合适的位置。 |
| 停靠限制 | `isAreaAllowed(Qt::DockWidgetArea area) const` | 判断指定区域是否被允许。 | 是内联便捷判断，等价于检查 `allowedAreas()` flags。 |
| 当前位置 | `dockLocation() const` | 返回当前停靠区域。 | Qt 6.9 起；浮动或不在主窗口里时返回 `Qt::NoDockLocation`。 |
| 当前位置 | `setDockLocation(Qt::DockWidgetArea area)` | 程序主动把 dock 放到某个区域。 | `NoDockLocation` 表示浮动；目标区域应符合 `allowedAreas()`。 |
| 标题栏 | `titleBarWidget() const` | 返回自定义标题栏控件。 | 没有自定义标题栏时返回空指针。 |
| 标题栏 | `setTitleBarWidget(QWidget *widget)` | 替换默认 dock 标题栏。 | 传空恢复默认；被替换掉的旧标题栏不会自动删除。 |
| 显示入口 | `toggleViewAction() const` | 返回控制该 dock 显示/隐藏的可勾选 action。 | 适合放进“视图”菜单；action 由 dock 拥有，别手动删除。 |

### 8.3 信号

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 信号 | `featuresChanged(DockWidgetFeatures features)` | dock 功能位变化时发出。 | 设置面板、菜单勾选状态可据此同步。 |
| 信号 | `topLevelChanged(bool topLevel)` | dock 浮动状态变化时发出。 | `true` 表示成为浮动窗口，`false` 表示回到主窗口停靠布局。 |
| 信号 | `allowedAreasChanged(Qt::DockWidgetAreas allowedAreas)` | 允许停靠区域变化时发出。 | 可用于同步用户偏好或提示文本。 |
| 信号 | `visibilityChanged(bool visible)` | dock 可见性变化时发出。 | Qt 注释里提示未来可能弱化；新代码也可考虑 `showEvent/hideEvent`。 |
| 信号 | `dockLocationChanged(Qt::DockWidgetArea area)` | 当前停靠区域变化时发出。 | Qt 6.9 起；适合记录布局或更新状态栏位置提示。 |

### 8.4 保护扩展点

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 事件 | `changeEvent(QEvent *event)` | 处理语言、字体、样式等变化。 | 重写时通常先或后调用基类，避免标题栏状态不同步。 |
| 事件 | `closeEvent(QCloseEvent *event)` | 处理用户关闭 dock 的事件。 | 关闭通常意味着隐藏；需要阻止关闭或保存状态时重写。 |
| 绘制 | `paintEvent(QPaintEvent *event)` | 绘制 dock 外观。 | 普通样式调整优先用 style 或自定义标题栏，别轻易全手绘。 |
| 事件 | `event(QEvent *event)` | dock 的统一事件入口。 | 只有处理特殊平台事件或标题栏行为时才建议重写。 |
| 样式支持 | `initStyleOption(QStyleOptionDockWidget *option) const` | 用当前 dock 状态填充样式选项。 | 自定义绘制时调用它，避免遗漏浮动、可关闭、标题等状态。 |

## 9. 常见误区

### 9.1 把尺寸约束写在 dock 上

停靠状态和浮动状态的装饰尺寸不同。固定 `QDockWidget` 的尺寸会让某一种状态下的布局失真；应让内容 widget 提供 `sizeHint()`、`minimumSize` 和 `QSizePolicy`。

### 9.2 以为 `setWidget()` 会自动把内容显示出来

内容 widget 如果是后来加入的，dock 已经可见时要确认内容本身已经 `show()`；内容 widget 的布局也应在 `setWidget()` 前准备好。

### 9.3 误删 `toggleViewAction()`

这个 action 的所有权属于 dock。菜单只引用它，不负责删除它。

### 9.4 用 `windowTitle` 代替 `objectName`

标题是给用户看的，可能被翻译或动态修改；布局保存恢复依赖稳定的 `objectName`，两者用途不同。

### 9.5 把浮动 dock 当成普通对话框

浮动只是 dock 的一种显示状态。真正需要独立任务流程、确认按钮和模态行为时，应使用 `QDialog`；需要可重排工具面板时才用 `QDockWidget`。

---

### 一句话总结

`QDockWidget` 是 `QMainWindow` 中可停靠、可浮动、可标签化的面板外壳：用 `setWidget()` 放入内容，用 `allowedAreas/features` 控制用户操作，用 `toggleViewAction()` 接入视图菜单，用稳定 `objectName` 配合 `saveState()/restoreState()` 保存布局。
