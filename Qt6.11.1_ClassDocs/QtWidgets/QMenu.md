# QMenu

> Qt 6.11.1 · Qt Widgets · 来自 `QMenu`

## 1. 先建立直觉

`QMenu` 是一组 `QAction` 的弹出式容器。它可以作为菜单栏下拉菜单、右键上下文菜单、工具按钮下拉菜单、系统托盘菜单或子菜单使用。

真正的命令通常写在 `QAction` 里：文本、图标、快捷键、enabled、checked、triggered。`QMenu` 负责展示、分组、弹出位置、悬停和触发信号。把命令放在 action 里，可以让同一个命令同时出现在菜单和工具栏。

## 2. 类说明

- 头文件：`#include <QMenu>`
- 模块：`Qt6::Widgets`
- 继承自：`QWidget`
- 直接派生类：类页未列出

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

弹出菜单视觉上是顶层窗口，但作为 QObject 仍可由 parent 管理生命周期。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QMenu(parent)` / `QMenu(title, parent)` | 创建菜单。 |
| `addAction()` | 继承自 QWidget，添加命令 action。 |
| `addMenu()` / `insertMenu()` | 添加或插入子菜单。 |
| `addSeparator()` / `insertSeparator()` | 添加分隔符。 |
| `addSection()` / `insertSection()` | 添加带文本的分组标题。 |
| `clear()` | 清空菜单 action。 |
| `isEmpty()` | 判断菜单是否没有可用 action。 |
| `exec()` | 同步弹出菜单并返回用户选中的 action。 |
| `popup()` | 异步弹出菜单。 |
| `actionAt()` / `actionGeometry()` | 根据坐标查询 action 或 action 区域。 |
| `activeAction()` / `setActiveAction()` | 当前高亮 action。 |
| `setDefaultAction()` / `defaultAction()` | 设置默认 action，常用于强调主要命令。 |
| `menuAction()` | 返回代表此菜单的 action，用于菜单栏或子菜单。 |
| `menuInAction()` | 从 action 反查对应菜单。 |
| `setTitle()` / `title()` | 菜单标题，同时影响 `menuAction()` 文本。 |
| `setIcon()` / `icon()` | 菜单图标，同时影响 `menuAction()` 图标。 |
| `setSeparatorsCollapsible()` | 是否折叠连续或首尾分隔符。 |
| `setToolTipsVisible()` | 菜单项是否显示 tooltip。 |
| `setTearOffEnabled()` | 是否允许撕下菜单成为独立窗口。 |
| `showTearOffMenu()` / `hideTearOffMenu()` | 显示或隐藏撕下菜单。 |
| `setAsDockMenu()` | macOS 上设置为 Dock 菜单。 |
| `toNSMenu()` | macOS 获取原生 `NSMenu`。 |
| `aboutToShow()` / `aboutToHide()` | 菜单显示/隐藏前信号。 |
| `triggered(action)` / `hovered(action)` | 用户触发或悬停 action。 |
| `initStyleOption()` | 子类化绘制菜单项前初始化样式选项。 |

## 4. 关键用法

### 动态菜单在 `aboutToShow()` 里构建

最近文件、打开方式、设备列表这类内容会变化的菜单，适合在 `aboutToShow()` 中清空并重建。这样菜单平时不维护过期状态，打开时才读取最新数据。

### `exec()` 和 `popup()` 的选择

`exec()` 会启动局部事件循环并返回选中的 action，适合同步上下文菜单。`popup()` 立即返回，用户选择通过 `triggered()` 或 action 自己的信号处理。复杂应用更偏向异步，避免嵌套事件循环带来的状态问题。

### 分隔符和 section 用来组织命令

`addSeparator()` 分组但不说明含义；`addSection()` 可显示组名。菜单不应太长，频繁使用的命令应放到工具栏或主界面，低频命令再放菜单。

### 自定义控件谨慎放进菜单

需要在菜单里放 slider、搜索框等控件时通常用 `QWidgetAction`。但菜单天然是短暂停留的命令面板，复杂交互更适合弹出面板或对话框。

## 5. 常见坑与经验

- 菜单显示命令，不要把业务逻辑写死在菜单类里，放到 `QAction` 更可复用。
- `exec()` 的返回 action 可能为空，用户可能取消菜单。
- 上下文菜单位置通常要把局部坐标转成全局坐标。
- 连续分隔符默认会折叠，动态菜单里不用太害怕多加一个 separator。
- tear-off 菜单是传统桌面特性，现代界面里少用。
