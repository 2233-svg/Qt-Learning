# QMenuBar

> Qt 6.11.1 · Qt Widgets · 来自 `QMenuBar`

## 1. 先建立直觉

`QMenuBar` 是窗口顶部的菜单栏，承载 File、Edit、View、Help 这类顶层菜单。它本身也由 `QAction` 驱动：每个顶层菜单通过自己的 `menuAction()` 出现在菜单栏里。

在 `QMainWindow` 中通常不手动布局菜单栏，而是使用 `menuBar()` 或 `setMenuBar()`。在 macOS 等平台上，菜单栏可能变成系统原生菜单栏，而不是画在窗口内部。

## 2. 类说明

- 头文件：`#include <QMenuBar>`
- 模块：`Qt6::Widgets`
- 继承自：`QWidget`
- 直接派生类：类页未列出

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

菜单栏通常管理它通过 `addMenu(title)` 创建的菜单；如果传入已有 `QMenu *`，所有权规则要看 parent 和创建方式。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QMenuBar(parent)` | 创建菜单栏。 |
| `addMenu(menu)` | 添加已有菜单，返回该菜单的 action。 |
| `addMenu(title)` / `addMenu(icon, title)` | 创建并添加新菜单。 |
| `insertMenu(before, menu)` | 在指定 action 前插入菜单。 |
| `addSeparator()` / `insertSeparator()` | 添加顶层分隔符。 |
| `clear()` | 移除菜单栏所有 action。 |
| `actionAt()` / `actionGeometry()` | 根据坐标找 action 或获取 action 区域。 |
| `activeAction()` / `setActiveAction()` | 当前高亮顶层 action。 |
| `setCornerWidget()` / `cornerWidget()` | 在菜单栏角落放置小控件。 |
| `setDefaultUp()` / `isDefaultUp()` | 默认向上弹出菜单。 |
| `setNativeMenuBar()` / `isNativeMenuBar()` | 是否使用平台原生菜单栏。 |
| `toNSMenu()` | macOS 获取原生菜单对象。 |
| `triggered(action)` / `hovered(action)` | 顶层或菜单 action 被触发/悬停。 |
| `initStyleOption()` | 子类化绘制顶层菜单项时使用。 |

## 4. 关键用法

### 在 `QMainWindow` 中创建菜单

典型写法是：

```cpp
auto *fileMenu = menuBar()->addMenu(tr("&File"));
fileMenu->addAction(openAction);
fileMenu->addAction(saveAction);
```

`QAction` 可以同时加入菜单和工具栏，enabled/checked 状态会同步，这是 Qt action 系统的核心优势。

### 原生菜单栏影响位置和行为

在 macOS 上，菜单栏通常出现在屏幕顶部。`setNativeMenuBar(false)` 可以强制放在窗口内，但会违背平台习惯。跨平台应用通常接受原生行为，只在嵌入式、特殊窗口或自定义 shell 中关闭它。

### corner widget 要少用

`setCornerWidget()` 可放搜索框、状态按钮等小控件，但菜单栏主要是命令导航，不应变成复杂工具栏。常用工具更适合 `QToolBar`。

### 所有权和隐藏

`addMenu(title)` 创建的菜单由菜单栏管理；`addMenu(QMenu*)` 添加已有菜单时，菜单栏不一定拥有它。返回的 `QAction` 可用于隐藏、禁用或移动这个顶层菜单入口。

## 5. 常见坑与经验

- 菜单栏是顶层命令结构，不适合塞大量即时操作控件。
- 原生菜单栏下，菜单栏 widget 本身可能不占窗口内部高度。
- 顶层菜单项使用 `&File` 这类助记符时，要检查翻译后冲突。
- 动态菜单内容应放在菜单的 `aboutToShow()` 里构建，而不是每次主窗口状态变化都重建。
- 业务命令应集中在 `QAction`，菜单栏只负责组织。
