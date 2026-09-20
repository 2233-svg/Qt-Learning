# QAbstractScrollArea

> Qt 6.11.1 · Qt Widgets · 来自 `QAbstractScrollArea`

## 1. 先建立直觉

`QAbstractScrollArea` 是所有“有视口和滚动条”的控件基类。`QTextEdit`、`QPlainTextEdit`、`QScrollArea`、`QAbstractItemView`、`QGraphicsView` 都建立在它的结构上：中间是 `viewport()`，边上是水平/垂直滚动条，角落和滚动条旁边还可以放辅助控件。

它通常不直接实例化。你继承它，是为了做自定义滚动视图；你学习它，是为了理解为什么很多控件的绘制、鼠标事件和坐标都发生在 viewport 上，而不是外层控件上。

## 2. 类说明

- 头文件：`#include <QAbstractScrollArea>`
- 模块：`Qt6::Widgets`
- 继承自：`QFrame`
- 直接派生类：`QAbstractItemView`、`QGraphicsView`、`QMdiArea`、`QPlainTextEdit`、`QScrollArea`、`QTextEdit`

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `setViewport()` / `viewport()` | 设置或读取实际显示内容的视口控件。 |
| `setupViewport()` | 子类化时初始化新视口。 |
| `horizontalScrollBar()` / `verticalScrollBar()` | 获取滚动条对象。 |
| `setHorizontalScrollBar()` / `setVerticalScrollBar()` | 替换滚动条。 |
| `setHorizontalScrollBarPolicy()` / `setVerticalScrollBarPolicy()` | 控制滚动条总是显示、按需显示或隐藏。 |
| `setSizeAdjustPolicy()` / `sizeAdjustPolicy()` | 控制滚动区域 size hint 是否随内容调整。 |
| `maximumViewportSize()` | 在没有滚动条时 viewport 可用最大尺寸。 |
| `setViewportMargins()` / `viewportMargins()` | 给 viewport 四周预留空间。 |
| `setCornerWidget()` / `cornerWidget()` | 设置两个滚动条交叉角落的控件。 |
| `addScrollBarWidget()` / `scrollBarWidgets()` | 在滚动条旁放按钮、标签等辅助控件。 |
| `scrollContentsBy(dx, dy)` | 滚动条移动后让子类滚动内容。 |
| `viewportEvent()` | 处理 viewport 上的事件。 |
| `viewportSizeHint()` | 返回 viewport 推荐尺寸。 |

## 4. 关键用法

### 事件和绘制多发生在 viewport

自定义滚动区域时，内容通常画在 `viewport()` 上。鼠标、拖放、右键菜单等事件也会被转发到 viewport 相关处理函数。很多坐标 bug 都来自把外层 frame 坐标当成 viewport 坐标。

### 滚动条只是状态，不是内容

子类要根据内容尺寸设置滚动条范围、页步长和值；滚动条值变化后，在 `scrollContentsBy()` 或相关事件中移动/重绘内容。不要直接调用 `scrollContentsBy()` 做程序滚动，应该设置滚动条值。

### viewport margins 用于固定边栏

行号栏、表头、角落按钮这类固定区域可以通过 `setViewportMargins()` 留空间，再把对应小控件放到边上。`QTableView`、`QPlainTextEdit` 行号栏等思路都离不开这个概念。

## 5. 常见坑与经验

- viewport 不是外层控件，绘制和命中测试要用对坐标系。
- 替换滚动条或 viewport 后要重新连接信号和初始化状态。
- `AdjustToContents` 可能导致布局反复计算，复杂内容要慎用。
- 滚动区域子类只能在 GUI 线程访问。
- 自定义滚动内容时，先设计内容尺寸模型，再设计滚动条范围。
