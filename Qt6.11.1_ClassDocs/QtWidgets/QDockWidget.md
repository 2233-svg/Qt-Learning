# QDockWidget

> Qt 6.11.1 · Qt Widgets · 来自 `QDockWidget`

## 1. 先建立直觉

`QDockWidget` 是 `QMainWindow` 里的可停靠面板：项目树、属性检查器、日志输出、图层面板、工具设置、调试窗口都常用它承载。它外层负责标题栏、关闭、浮动、拖动和停靠位置，内部真正内容由 `setWidget()` 设置。

它不是普通布局容器。只有放进 `QMainWindow` 的 dock 区域后，停靠、分割、标签化、浮动和状态保存才完整生效。

## 2. 类说明

- 头文件：`#include <QDockWidget>`
- 模块：`Qt6::Widgets`
- 继承自：`QWidget`
- 直接派生类：类页未列出

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

内容控件通过 `setWidget()` 放入 dock；主窗口通过 `addDockWidget()`、`splitDockWidget()`、`tabifyDockWidget()` 管理布局。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QDockWidget(parent, flags)` / `QDockWidget(title, parent, flags)` | 创建停靠面板。 |
| `setWidget()` / `widget()` | 设置或读取内部内容控件。 |
| `setTitleBarWidget()` / `titleBarWidget()` | 替换标题栏控件。 |
| `setFeatures()` / `features()` | 控制是否可关闭、移动、浮动、竖直标题栏。 |
| `setAllowedAreas()` / `allowedAreas()` | 限制可停靠区域。 |
| `isAreaAllowed()` | 查询某区域是否允许停靠。 |
| `setFloating()` / `isFloating()` | 设置或查询是否浮动为独立窗口。 |
| `setDockLocation()` / `dockLocation()` | Qt 6.9 起设置或读取当前停靠区域。 |
| `toggleViewAction()` | 返回控制 dock 显示/隐藏的 action。 |
| `allowedAreasChanged()` | 可停靠区域变化。 |
| `featuresChanged()` | 功能开关变化。 |
| `topLevelChanged()` | 浮动状态变化。 |
| `visibilityChanged()` | 可见性变化。 |
| `dockLocationChanged()` | 停靠位置变化。 |
| `initStyleOption()` | 子类化绘制 dock 外框/标题时初始化样式选项。 |

## 4. 关键用法

### dock 外壳和内容控件分离

`QDockWidget` 本身只是一层可停靠外壳。把真正 UI 放进一个普通 QWidget，再 `dock->setWidget(panel)`。不要直接给 dock 设置布局再塞控件，这会和它内部标题栏/框架结构冲突。

### 让用户找回面板

`toggleViewAction()` 很重要。把它加入 View 菜单后，用户关闭 dock 还能重新打开。专业桌面应用通常都会有“视图/面板”菜单集中管理 dock 显示。

### features 控制自由度

属性面板可以可关闭、可移动、可浮动；核心导航面板可能只允许移动但不允许关闭；关键监控面板可禁用浮动。`DockWidgetVerticalTitleBar` 可节省横向空间，但不是所有界面都适合。

### 保存布局用主窗口

dock 的位置、大小、标签化关系通常通过 `QMainWindow::saveState()` / `restoreState()` 保存，而不是单独保存每个 dock。恢复前要先创建所有 dock，并设置稳定 objectName。

## 5. 常见坑与经验

- `setWidget()` 的内容控件会被 dock 重新设为子对象。
- 关闭 dock 通常只是隐藏，不代表销毁内容。
- 自定义标题栏后，要自己考虑关闭、浮动、拖动等交互是否还清楚。
- `dockLocation` 对浮动或未放进主窗口的 dock 可能是无停靠位置。
- 没有稳定 `objectName` 时，主窗口状态恢复很容易失败。
