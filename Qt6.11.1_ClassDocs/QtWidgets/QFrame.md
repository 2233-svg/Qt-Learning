# QFrame

> Qt 6.11.1 · Qt Widgets · 来自 `QFrame`

## 1. 先建立直觉

### 这是什么

`QFrame` 是带边框/分隔线能力的基础控件。它继承 `QWidget`，本身不提供复杂交互，主要负责画一个框、面板、水平线或垂直线。许多控件继承它，是因为它们需要 frame 外观，例如 `QLabel`、`QStackedWidget`、`QAbstractScrollArea`。

`QFrame` 适合表达视觉层级，不适合承载业务状态。它和布局配合使用：布局决定子控件在哪，frame 决定外观边界是什么。

### 适合使用的场景

- 做水平/垂直分隔线。
- 给一块内容添加 `StyledPanel` 或 `Box` 边框。
- 作为自定义面板基类，保留平台 style 绘制。
- 需要统一控制 line width、shadow、frame shape。

### 不适合的场景

- 需要标题和可选启用/禁用整组内容，用 `QGroupBox`。
- 需要滚动内容，用 `QScrollArea` 或 `QAbstractScrollArea` 子类。
- 只是为了背景色，不一定需要 frame；普通 `QWidget` 加 palette/style sheet 可能更简单。

## 2. 依赖与对象关系

- 头文件：`#include <QFrame>`
- 模块：Qt Widgets
- CMake：`find_package(Qt6 REQUIRED COMPONENTS Widgets)`，并链接 `Qt6::Widgets`
- 继承自：`QWidget`
- 直接派生类：`QAbstractScrollArea`、`QLabel`、`QLCDNumber`、`QSplitter`、`QStackedWidget`、`QToolBox`

`QFrame` 的 frame 不等于 layout margin。边框会占据绘制和几何空间，布局的 contents margins 仍需单独设置。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `enum Shadow` | 边框阴影：平面、凸起、凹陷。 |
| `enum Shape` | 边框形状：无框、盒子、面板、分隔线等。 |
| `enum StyleMask` | 从 `frameStyle()` 中提取 shape/shadow 的掩码。 |
| `frameRect : QRect` | 边框绘制矩形。 |
| `frameShape : Shape` | 当前边框形状。 |
| `frameShadow : Shadow` | 当前阴影效果。 |
| `frameWidth : int` | 实际边框宽度，只读。 |
| `lineWidth : int` | 线宽。 |
| `midLineWidth : int` | 中线宽度，用于部分 3D 样式。 |
| `QFrame(QWidget *parent, Qt::WindowFlags f)` | 创建默认无框 frame。 |
| `frameStyle()` / `setFrameStyle(int)` | 一次读取或设置 shape + shadow。 |
| `setFrameShape()` / `setFrameShadow()` | 分别设置形状和阴影。 |
| `setFrameRect()` | 设置绘制边框的矩形。 |
| `sizeHint()` | 返回建议尺寸。 |
| `initStyleOption(QStyleOptionFrame *)` | 为自定义绘制准备 style option。 |
| `paintEvent()` / `event()` / `changeEvent()` | 绘制和响应 style、palette 等变化。 |

## 4. API 逐项说明

### `Shadow`

`Plain` 是平面线，`Raised` 看起来凸起，`Sunken` 看起来凹陷。现代界面中 3D 边框用得少，`StyledPanel` 加平台 style 往往更自然。

### `Shape`

`NoFrame` 不画边框；`Box` 画盒子；`Panel`/`StyledPanel` 画面板；`HLine`/`VLine` 是分隔线；`WinPanel` 是兼容旧 Windows 风格的形状。

实际项目里最常见的是 `StyledPanel`、`HLine`、`VLine`。分隔线用 frame 比自己画一条 label 背景更符合 style。

### `StyleMask`

用于从 `frameStyle()` 的整数里拆出 shape 和 shadow。普通代码更推荐直接用 `frameShape()`、`frameShadow()`。

只有处理旧代码或批量复制 frame style 时才常用它。

### `frameRect`

边框绘制的矩形，默认是整个控件区域。设置空矩形会回到控件矩形语义。

多数应用不需要手动设置；自定义绘制或特殊内容区域时才会碰它。

### `frameShape` / `frameShadow` / `frameStyle`

`frameStyle()` 把形状和阴影编码在一个整数里，`setFrameStyle()` 可以一次设置两者。分开读写时使用 `frameShape()`、`frameShadow()`。

示例：`setFrameStyle(QFrame::StyledPanel | QFrame::Sunken)`。

### `frameWidth` / `lineWidth` / `midLineWidth`

`lineWidth` 和 `midLineWidth` 是你设置的线宽参数，`frameWidth` 是根据 shape、shadow、style 最终算出的实际宽度。

布局计算时真正影响内容区域的是实际 frame width，而不是你想象中的某个固定像素。

### 构造和析构

构造函数默认 `NoFrame`，line width 为 1。析构通常由父控件负责。

如果你只是想用它当容器，记得设置 layout；`QFrame` 不会自动排列子控件。

### `initStyleOption()` / `paintEvent()`

`initStyleOption()` 填充 frame 绘制信息；`paintEvent()` 用 style 绘制 frame。

自定义 frame 子类时，优先让 style 画边框，然后只绘制你自己的内容。

## 5. 深入实践与常见坑

### QFrame 是视觉边界，不是语义分组

有标题、可勾选、启用禁用整组内容时，用 `QGroupBox`。只要一条线或面板边框时，用 `QFrame`。

### 分隔线也要交给布局

`HLine` 和 `VLine` 只是控件，仍然要加入布局。不要用绝对坐标画分割线。

### StyledPanel 通常比硬编码边框更好

它交给平台 style 决定外观，主题切换和跨平台效果更稳定。
