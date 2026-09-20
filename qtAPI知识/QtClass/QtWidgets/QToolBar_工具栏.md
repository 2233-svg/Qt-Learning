# Qt QToolBar 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QToolBar>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QWidget -> QToolBar`  
> 关键词：`QAction`、`QMainWindow`、停靠、浮动、`QWidgetAction`

## 1. 先说结论：QToolBar 是 QAction 的可停靠可视容器

`QToolBar` 是一条承载快捷命令的控件。它最适合放常用、即时、图标化的操作，例如新建、保存、撤销、缩放、运行或对齐。

工具栏的核心不是把一堆 `QPushButton` 横向塞在一起，而是把同一批 `QAction` 用另一种视觉入口展示出来：

```text
QAction
  ├─ 可加入 QMenu
  ├─ 可设置快捷键
  ├─ 可被代码 trigger()
  └─ 可加入 QToolBar，变成工具按钮
```

当它由 `QMainWindow` 管理时，工具栏还可以：

- 停靠到窗口的上、下、左、右区域；
- 在同一个停靠区中换到另一行；
- 在允许时由用户拖动到其他区域；
- 在允许时变为一个独立的浮动窗口；
- 通过 `QMainWindow::saveState()` 保存和恢复位置、换行与可见性。

它不负责：

- 定义业务命令本身，命令应放在 `QAction`；
- 为整个窗口手工排版，停靠布局应交给 `QMainWindow`；
- 表示复杂的属性面板，页面分组更适合 `QDockWidget`、侧栏或普通布局；
- 替代菜单。菜单适合完整命令集合，工具栏适合高频入口。

## 2. 最小可用写法：先有 QAction，再加入工具栏

```cpp
#include <QAction>
#include <QKeySequence>
#include <QMainWindow>
#include <QToolBar>

class MainWindow final : public QMainWindow
{
public:
    MainWindow()
    {
        auto *fileBar = addToolBar("文件");
        fileBar->setObjectName("fileToolBar");

        auto *openAction = new QAction("打开", this);
        openAction->setShortcut(QKeySequence::Open);
        connect(openAction, &QAction::triggered, this, &MainWindow::openFile);

        fileBar->addAction(openAction);
        fileBar->addSeparator();

        auto *saveAction = new QAction("保存", this);
        saveAction->setShortcut(QKeySequence::Save);
        connect(saveAction, &QAction::triggered, this, &MainWindow::saveFile);
        fileBar->addAction(saveAction);
    }

private:
    void openFile() {}
    void saveFile() {}
};
```

`QToolBar` 通过 `QWidget::addAction()` 继承来的 API 接收 `QAction`。将 action 同时加入菜单和工具栏，能保证文字、图标、快捷键、禁用状态与触发逻辑保持一致：

```cpp
fileMenu->addAction(openAction);
fileBar->addAction(openAction);
```

不要为菜单按钮和工具栏按钮各写一份点击逻辑。业务命令应集中在 action 的 `triggered` 信号或关联的槽函数中。

## 3. QMainWindow 停靠体系：区域、行和当前状态

`QMainWindow` 维护四个工具栏区域：

```text
                Qt::TopToolBarArea
    +---------------------------------------+
    | [文件] [编辑]                         |
    | [调试]          <- 第二条工具栏行      |
    +---+-------------------------------+---+
    |   |                               |   |
    | 左 |            centralWidget      | 右 |
    |   |                               |   |
    +---+-------------------------------+---+
                Qt::BottomToolBarArea
```

加入工具栏的常用方式：

```cpp
auto *editBar = new QToolBar("编辑", this);
editBar->setObjectName("editToolBar");
addToolBar(Qt::TopToolBarArea, editBar);

addToolBarBreak(Qt::TopToolBarArea);

auto *debugBar = new QToolBar("调试", this);
debugBar->setObjectName("debugToolBar");
addToolBar(Qt::TopToolBarArea, debugBar);
```

几个概念不要混淆：

| 概念 | API | 含义 |
| --- | --- | --- |
| 当前停靠位置 | `QMainWindow::toolBarArea(bar)` | 工具栏此刻在哪个区域；未加入时是 `Qt::NoToolBarArea`。 |
| 允许位置 | `QToolBar::allowedAreas()` | 用户可以拖到哪些区域的集合。 |
| 可移动 | `QToolBar::isMovable()` | 是否允许用户在工具栏区域之间拖动。 |
| 可浮动 | `QToolBar::isFloatable()` | 是否允许拖成独立窗口。 |
| 当前浮动 | `QToolBar::isFloating()` | 此刻是否已经是独立窗口。 |

## 4. `movable`、`floatable`、`floating`：三个经常混淆的属性

### 4.1 `movable`

`movable` 表示工具栏是否可以被用户拖到另一个工具栏区域。默认值是 `true`。

```cpp
toolBar->setMovable(false); // 固定在 QMainWindow 当前布局中
```

这不等于它永远不会移动。程序仍可调用 `QMainWindow::addToolBar()` 或 `insertToolBar()` 重排它；该属性限制的是用户交互拖动。

### 4.2 `floatable`

`floatable` 表示工具栏是否允许被用户拖成独立窗口。默认值是 `true`。

```cpp
toolBar->setFloatable(false);
```

`movable` 和 `floatable` 可分别配置。例如允许在顶部与底部之间移动，但不允许浮动：

```cpp
toolBar->setMovable(true);
toolBar->setFloatable(false);
toolBar->setAllowedAreas(
    Qt::TopToolBarArea | Qt::BottomToolBarArea);
```

### 4.3 `floating`

`floating` 是只读状态，表示工具栏当前是否已经成为独立窗口：

```cpp
if (toolBar->isFloating()) {
    // 工具栏当前脱离 QMainWindow 的停靠区。
}
```

`topLevelChanged(bool)` 会在这个状态改变时发出。参数为 `true` 表示现在浮动。

## 5. `allowedAreas` 是允许集合，不是当前位置

```cpp
toolBar->setAllowedAreas(
    Qt::TopToolBarArea | Qt::LeftToolBarArea);
```

这只说明用户允许把它停靠到顶部或左侧；不代表它马上移动到左侧，也不代表当前停靠位置一定在其中之一以外不会存在。

查询单一目标是否允许：

```cpp
if (toolBar->isAreaAllowed(Qt::LeftToolBarArea)) {
    // 左侧是允许的用户拖动目标。
}
```

`allowedAreas` 只有在工具栏属于 `QMainWindow` 的停靠框架时才有实际意义。普通地把工具栏放进 `QVBoxLayout`，它仍可显示内容，但没有主窗口的四区停靠行为。

## 6. QAction、separator 和嵌入 widget 的区别

### 6.1 添加 QAction

`QToolBar` 继承 `QWidget::addAction()`，加入后会创建对应的显示 widget，通常是 `QToolButton`：

```cpp
auto *undoAction = new QAction(QIcon(":/undo.svg"), "撤销", this);
toolBar->addAction(undoAction);
```

工具栏的 `toolButtonStyle`、`iconSize` 会应用到这种由 action 自动生成的工具按钮。

### 6.2 `addSeparator()`

```cpp
QAction *separator = toolBar->addSeparator();
```

分隔符也是一个 `QAction`，可以通过 `separator->setVisible(false)` 控制显示。它适合分隔命令组，不应用来制造大段空白；需要弹性空白时通常应使用专门的 `QWidgetAction` 或合理布局设计。

### 6.3 `addWidget()`

```cpp
auto *zoomBox = new QComboBox;
zoomBox->addItems({"50%", "100%", "200%"});
QAction *zoomWidgetAction = toolBar->addWidget(zoomBox);
```

工具栏会接管传入 widget 的所有权。并且要注意两条规则：

1. 这不是自动生成的 action tool button，`toolButtonStyle` 不会作用于你手动加入的 `QToolButton`；
2. 控制这类 widget 的可见性应操作返回的 `QAction`，而不是直接 `show()` / `hide()` widget：

```cpp
zoomWidgetAction->setVisible(false);
```

若工具栏不是 `QMainWindow` 的子对象，空间不足时 extension popup 无法可靠容纳由 `addWidget()` 加入的 widget。需要可复用的嵌入式控件时，优先使用 `QWidgetAction`，让它按父容器创建 widget。

## 7. 工具栏过窄时发生什么

当工具栏无法容纳所有项目，Qt 会在尾部显示 extension button；用户点击后能从弹出菜单使用未放下的 action。

这解释了两个设计要求：

- 高优先级命令应排在前面；
- 不要将大量宽大的复杂控件直接放入工具栏。

只有纯 action 的工具栏最适合这种溢出机制。包含可编辑控件、复杂菜单或很多固定宽度 widget 时，需要实际缩放窗口测试。

## 8. 图标尺寸与工具按钮样式

### 8.1 `iconSize`

`iconSize` 是由 action 自动生成的工具按钮可使用图标的最大尺寸。默认值由当前 style 的 `QStyle::PM_ToolBarIconSize` 决定；小图标不会被强制放大。

```cpp
toolBar->setIconSize(QSize(24, 24));
```

不要用 `setFixedSize()` 强行调整每个内部按钮来控制图标，这会破坏平台 style 与高 DPI 适配。监听 `iconSizeChanged()` 可同步其他自定义控件。

### 8.2 `toolButtonStyle`

常见值包括：

```cpp
Qt::ToolButtonIconOnly
Qt::ToolButtonTextOnly
Qt::ToolButtonTextBesideIcon
Qt::ToolButtonTextUnderIcon
Qt::ToolButtonFollowStyle
```

默认是 `Qt::ToolButtonIconOnly`：

```cpp
toolBar->setToolButtonStyle(Qt::ToolButtonTextBesideIcon);
```

`Qt::ToolButtonFollowStyle` 在 Unix 上通常会遵循桌面环境设置；其他平台通常表现为 icon only。它只影响通过 `addAction()` 创建的工具按钮，不影响 `addWidget()` 手工塞入的 `QToolButton`。

## 9. `orientation`：由 QMainWindow 管理时不要直接设置

普通独立工具栏可以设置方向：

```cpp
toolBar->setOrientation(Qt::Vertical);
```

但当工具栏由 `QMainWindow` 管理时，不应靠该函数将工具栏“移动到另一边”。主窗口会根据停靠区决定工具栏方向；移动已停靠工具栏应使用：

```cpp
mainWindow->addToolBar(Qt::LeftToolBarArea, toolBar);
```

顶部和底部通常是水平，左侧和右侧通常是垂直。`orientationChanged()` 用于响应实际方向变化。

## 10. 查询某一个 action 的位置与对应 widget

```cpp
QAction *action = toolBar->actionAt(mouseEvent->position().toPoint());
if (action) {
    qDebug() << action->text();
}
```

两个 `actionAt()` 重载都返回命中 action；没有命中时返回 `nullptr`：

```cpp
toolBar->actionAt(QPoint(10, 10));
toolBar->actionAt(10, 10);
```

`actionGeometry(action)` 返回该 action 当前可见区域的局部矩形，适合定位动画、提示或测试：

```cpp
const QRect rect = toolBar->actionGeometry(saveAction);
```

`widgetForAction(action)` 返回工具栏中与 action 对应的 widget；action 不属于该工具栏时返回 `nullptr`。它可用于窄范围检查，但不要把内部生成的 `QToolButton` 当成稳定业务对象长期保存。

## 11. 显示、隐藏与上下文菜单

`toggleViewAction()` 返回一个可勾选 action，触发时显示或隐藏该工具栏：

```cpp
QAction *showFileBar = fileBar->toggleViewAction();
viewMenu->addAction(showFileBar);
```

它的文本来自 `QToolBar::windowTitle()`，因此构造时有意义的标题很重要：

```cpp
auto *fileBar = new QToolBar("文件", this);
```

当工具栏显示或隐藏时，`visibilityChanged(bool)` 发出；不应只监听 `QWidget::showEvent()`，因为可见性也可能由 toggle action 或主窗口状态恢复造成。

`QMainWindow` 的默认上下文菜单会聚合工具栏的 toggle actions。对用户可定制的主窗口，这是比自己维护一堆“显示工具栏”复选项更稳定的做法。

## 12. 保存和恢复布局：objectName 不是装饰

想让用户下次启动时保留工具栏位置、换行和显示状态：

```cpp
void MainWindow::writeSettings()
{
    QSettings settings("ExampleOrg", "Editor");
    settings.setValue("window/geometry", saveGeometry());
    settings.setValue("window/state", saveState(1));
}

void MainWindow::readSettings()
{
    QSettings settings("ExampleOrg", "Editor");
    restoreGeometry(settings.value("window/geometry").toByteArray());
    restoreState(settings.value("window/state").toByteArray(), 1);
}
```

所有参与保存的 `QToolBar` 都必须有唯一且稳定的 `objectName`：

```cpp
fileBar->setObjectName("fileToolBar");
editBar->setObjectName("editToolBar");
```

`saveState()` 用 `objectName` 识别各工具栏。没有设置或名称重复时，恢复布局会变得不可靠。`saveState(version)` 与 `restoreState(state, version)` 的版本号必须匹配，否则恢复失败且不改变现有主窗口状态。

## 13. 生命周期、所有权与线程

- `QToolBar` 是 `QWidget`，应在 GUI 线程创建、修改和销毁；
- 传给 `QMainWindow::addToolBar()` 的工具栏由主窗口管理其布局，但不应据此假设可随意手工删除；通常让 Qt 父子对象链负责销毁；
- `addWidget(widget)` 后，工具栏接管 widget 所有权；
- `QAction` 可以由主窗口或工具栏以外的对象拥有，并同时加入多个界面入口；
- `clear()` 只从工具栏移除所有 actions，不等于删除那些 `QAction` 对象；
- 工具栏析构时会销毁其子 widget，但 action 的实际销毁仍取决于它的 QObject 父对象。

一个稳妥的所有权模型是：`QMainWindow` 作为工具栏和共享 actions 的父对象；需要被多个窗口共享的 actions，则由更高层的命令对象拥有。

## 14. 常见误区与排查

### 14.1 直接给工具栏塞一堆 QPushButton

可以做到，但会丢掉 action 的快捷键、菜单复用、统一启用状态和溢出处理。高频命令应优先建成 `QAction`。

### 14.2 `addWidget()` 后直接 `widget->hide()`

这不会按工具栏 action 布局预期工作。保存 `addWidget()` 返回的 action，并调用 `action->setVisible(false)`。

### 14.3 使用 `setOrientation()` 移动已经停靠的工具栏

方向不是停靠命令。被 `QMainWindow` 管理时，要使用 `addToolBar(area, bar)` 或 `insertToolBar()`。

### 14.4 允许范围和当前区域混为一谈

`allowedAreas()` 是可去位置的集合；当前区域使用 `QMainWindow::toolBarArea()` 查询。

### 14.5 保存状态却没有设置唯一 objectName

布局恢复依赖每条工具栏稳定唯一的 `objectName`。这是恢复失败最常见的原因之一。

### 14.6 期待 `toolButtonStyle` 改变手动 addWidget 的 QToolButton

属性只影响 action 自动生成的工具按钮。手动加入的 widget 由你自己负责配置。

## API 速查表
### 15.1 构造、内容和查询

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QToolBar(QWidget *parent = nullptr)` | 创建空工具栏 | 传入 `parent` 建立 QObject 所有权 |
| 构造 | `QToolBar(const QString &title, QWidget *parent = nullptr)` | 创建带窗口标题的工具栏 | `title` 会用于 `toggleViewAction()` 和主窗口上下文菜单 |
| 生命周期 | `~QToolBar()` | 销毁工具栏 | 子 widget 随父对象链销毁；共享 action 的寿命由其 parent 决定 |
| 命令 | `addAction(...)` | 把 action 加到工具栏末尾 | 日常添加命令的首选 API |
| 命令 | `insertAction(before, action)` | 在指定 action 前插入 action | `before` 不在工具栏中时按 QWidget action 规则处理 |
| 分隔 | `addSeparator()` | 在末尾加入分隔 action | 返回的 `QAction` 可控制 separator 可见性 |
| 分隔 | `insertSeparator(before)` | 在 `before` 对应项目之前插入 separator | 用于维护命令组顺序 |
| 嵌入 | `addWidget(widget)` | 在末尾加入一个 widget，并返回其包装 action | 工具栏接管 widget；可见性操作返回 action |
| 嵌入 | `insertWidget(before, widget)` | 在指定 action 前加入 widget | 适合插入搜索框、组合框等小控件 |
| 清空 | `clear()` | 从工具栏移除全部 actions | 不会自动销毁那些 action 对象 |
| 查询 | `actionAt(const QPoint &p)` | 返回局部坐标命中的 action | 无命中返回 `nullptr` |
| 查询 | `actionAt(int x, int y)` | `QPoint` 重载的便捷形式 | 坐标相对于 toolbar 本身 |
| 几何 | `actionGeometry(action)` | 返回 action 当前局部几何 | 不属于工具栏或不可见时不要假设矩形有效 |
| 查询 | `widgetForAction(action)` | 返回当前工具栏为 action 使用的 widget | 无对应项返回 `nullptr`；不要长期依赖内部 widget |
| 显示控制 | `toggleViewAction()` | 返回显示/隐藏当前工具栏的可勾选 action | 加入“视图”菜单或依赖 QMainWindow 默认上下文菜单 |

### 15.2 停靠和属性 API

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 可移动 | `setMovable(bool)` / `isMovable()` | 设置或查询用户能否在工具栏区域间拖动 | 默认可移动；不限制程序重排 |
| 可浮动 | `setFloatable(bool)` / `isFloatable()` | 设置或查询是否可拖成独立窗口 | 默认可浮动；与 movable 不同 |
| 浮动状态 | `isFloating()` | 查询当前是否独立浮动 | 只读；状态变化监听 `topLevelChanged` |
| 区域 | `setAllowedAreas(Qt::ToolBarAreas)` | 设置用户允许停靠的区域集合 | 仅 QMainWindow 停靠场景有意义 |
| 区域 | `allowedAreas()` | 获取允许区域集合 | 不是当前位置 |
| 区域 | `isAreaAllowed(Qt::ToolBarArea)` | 查询某单一目标区域是否允许 | 快速判断 `allowedAreas` 的成员关系 |
| 方向 | `setOrientation(Qt::Orientation)` | 设置独立工具栏方向 | QMainWindow 管理时通过停靠区移动，不要靠它 |
| 方向 | `orientation()` | 获取当前方向 | 顶/底常为 Horizontal，左/右常为 Vertical |
| 图标 | `setIconSize(const QSize &)` / `iconSize()` | 设置或获取 action 工具按钮图标最大尺寸 | 默认取 `PM_ToolBarIconSize`；小图不会被放大 |
| 按钮样式 | `setToolButtonStyle(Qt::ToolButtonStyle)` / `toolButtonStyle()` | 设置或获取 action 工具按钮的显示风格 | 不影响 `addWidget()` 加入的自定义 QToolButton |

### 15.3 信号

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 信号 | `actionTriggered(QAction *action)` | 工具栏中的 action 被触发 | 记录、统一命令跟踪；action 也可能从其他入口触发 |
| 信号 | `movableChanged(bool)` | 可移动属性变化 | 同步自定义停靠 UI |
| 信号 | `allowedAreasChanged(Qt::ToolBarAreas)` | 允许区域集合变化 | 更新限制提示或配置界面 |
| 信号 | `orientationChanged(Qt::Orientation)` | 实际方向变化 | 更新嵌入 widget 的紧凑布局 |
| 信号 | `iconSizeChanged(const QSize &)` | 图标最大尺寸变化 | 同步自定义工具栏 widget |
| 信号 | `toolButtonStyleChanged(Qt::ToolButtonStyle)` | action 工具按钮风格变化 | 同步外部定制按钮表现 |
| 信号 | `topLevelChanged(bool topLevel)` | 浮动状态变化 | 保存或响应浮动窗口状态 |
| 信号 | `visibilityChanged(bool visible)` | 工具栏显示或隐藏 | 更新菜单勾选和业务偏好 |

### 15.4 受保护扩展点

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 事件 | `actionEvent(QActionEvent *)` | 响应 action 被加入、移除或改变 | 重写时先理解 QWidget action 事件链 |
| 事件 | `changeEvent(QEvent *)` | 响应语言、风格、字体等状态变化 | 自定义缓存要在对应事件后失效 |
| 事件 | `event(QEvent *)` | 通用事件分派入口 | 能用具体事件处理时不要滥用 |
| 绘制 | `paintEvent(QPaintEvent *)` | 绘制工具栏容器 | 通常交由 style；外观定制优先 `QProxyStyle` |
| 样式 | `initStyleOption(QStyleOptionToolBar *) const` | 用真实工具栏状态填充 style option | 子类/自定义 style 调试入口；不属于普通业务 API |

### 15.5 与 QMainWindow 协作的关键 API

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 停靠 | `QMainWindow::addToolBar(area, bar)` | 将工具栏停靠到指定区域 | 主窗口负责布局 |
| 停靠 | `QMainWindow::addToolBar(title)` | 创建并加入一条工具栏 | 仍应设置唯一 `objectName` 以支持状态恢复 |
| 停靠 | `QMainWindow::insertToolBar(before, bar)` | 在同一行中调整工具栏顺序 | `before` 应是已加入主窗口的工具栏 |
| 换行 | `QMainWindow::addToolBarBreak(area)` | 在区域中开始新的一条工具栏行 | 用于明确的两行布局 |
| 换行 | `QMainWindow::insertToolBarBreak(before)` | 在某工具栏前插入换行 | 调整现有工具栏行 |
| 移除 | `QMainWindow::removeToolBar(bar)` | 从主窗口停靠布局中移除 | 不删除 toolbar 对象 |
| 查询 | `QMainWindow::toolBarArea(bar)` | 查询当前停靠区 | 未加入时返回 `Qt::NoToolBarArea` |
| 查询 | `QMainWindow::toolBarBreak(bar)` | 查询 toolbar 前是否有换行 | 用于检查/恢复自定义布局 |
| 状态保存 | `QMainWindow::saveState(version)` | 保存工具栏和 dock widget 布局 | 依赖每项唯一 `objectName` |
| 状态恢复 | `QMainWindow::restoreState(state, version)` | 恢复保存的布局 | version 不匹配时返回 `false` 并保持现状 |

---

### 一句话总结

`QToolBar` 是用 `QAction` 组织高频命令的可视容器。把命令定义在 action 中，再由 `QMainWindow` 管理工具栏的停靠、移动、浮动和状态恢复；只有嵌入控件时才使用 `addWidget()`，并通过返回的 action 控制它的可见性。
