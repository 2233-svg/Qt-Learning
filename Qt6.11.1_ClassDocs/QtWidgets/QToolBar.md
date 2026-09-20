# QToolBar

> Qt 6.11.1 · Qt Widgets · 来自 `QToolBar`

## 1. 先建立直觉

`QToolBar` 是放置高频命令的工具栏，通常位于 `QMainWindow` 顶部、侧边或可浮动窗口中。它最自然的内容是 `QAction`：打开、保存、撤销、搜索、运行等。

菜单适合完整命令结构，工具栏适合常用快捷操作。两者共享同一个 `QAction`，可以让快捷键、图标、启用状态、勾选状态保持一致。

## 2. 类说明

- 头文件：`#include <QToolBar>`
- 模块：`Qt6::Widgets`
- 继承自：`QWidget`
- 直接派生类：类页未列出

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

工具栏的可移动、可浮动、允许停靠区域等能力只有放入 `QMainWindow` 工具栏区域时才完整生效。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QToolBar(parent)` / `QToolBar(title, parent)` | 创建工具栏，标题用于主窗口右键菜单和浮动窗口。 |
| `addAction()` | 继承自 QWidget，添加 action 生成工具按钮。 |
| `addSeparator()` / `insertSeparator()` | 添加分隔符。 |
| `addWidget()` / `insertWidget()` | 在工具栏中放入自定义 QWidget。 |
| `widgetForAction()` | 根据 action 找到对应 widget。 |
| `actionAt()` | 根据坐标找 action。 |
| `clear()` | 清空工具栏 action。 |
| `setIconSize()` / `iconSize()` | 设置工具栏图标最大尺寸。 |
| `setToolButtonStyle()` / `toolButtonStyle()` | 图标、文字、文字在旁等显示方式。 |
| `setAllowedAreas()` / `allowedAreas()` | 设置可停靠区域。 |
| `isAreaAllowed()` | 判断某个区域是否允许。 |
| `setMovable()` / `isMovable()` | 是否允许用户移动工具栏。 |
| `setFloatable()` / `isFloatable()` | 是否允许拖成浮动窗口。 |
| `isFloating()` | 当前是否浮动。 |
| `setOrientation()` / `orientation()` | 设置方向；主窗口管理时通常不直接改。 |
| `toggleViewAction()` | 返回控制工具栏显示/隐藏的 action。 |
| `actionTriggered(action)` | 工具栏内 action 触发。 |
| `visibilityChanged()` / `topLevelChanged()` | 显示状态或浮动状态变化。 |
| `allowedAreasChanged()` / `movableChanged()` | 停靠策略变化。 |
| `iconSizeChanged()` / `toolButtonStyleChanged()` | 外观策略变化。 |

## 4. 关键用法

### 工具栏应该复用 QAction

不要为菜单和工具栏分别写两套槽。创建一个 `QAction`，设置文本、图标、快捷键、状态和 triggered 逻辑，然后同时加到菜单和工具栏。这样状态更新一次即可同步到所有入口。

### 自定义 widget 要克制

`addWidget()` 可以放搜索框、缩放下拉、模式切换等控件。过多复杂控件会让工具栏变成拥挤表单；复杂参数面板更适合 dock widget 或侧边栏。

### 主窗口负责停靠

工具栏放入 `QMainWindow::addToolBar()` 后，`allowedAreas`、`movable`、`floatable` 才有完整意义。用户布局可以配合 `QMainWindow::saveState()` / `restoreState()` 保存。

### 图标和文字策略影响可发现性

`ToolButtonIconOnly` 节省空间但依赖图标识别；`ToolButtonTextBesideIcon` 更适合新用户或专业工具中的关键动作。若想跟随系统偏好，用 `Qt::ToolButtonFollowStyle`。

## 5. 常见坑与经验

- `addWidget()` 返回的是一个 action，移除/隐藏时要操作这个 action。
- 自己创建的 widget 被加入工具栏后会重新设置 parent。
- `orientation` 在主窗口停靠时由区域决定，手动设置可能被覆盖。
- 没有文本或 tooltip 的图标按钮可发现性很差。
- 工具栏标题会出现在主窗口的工具栏管理菜单里，别留空或随便命名。
