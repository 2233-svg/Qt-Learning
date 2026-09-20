# QScrollBar

> Qt 6.11.1 · Qt Widgets · 来自 `QScrollBar`

## 1. 先建立直觉

### 这是什么

`QScrollBar` 是滚动条控件。它继承 `QAbstractSlider` 的整数范围模型，但它的语义不是“调一个参数”，而是“控制视口在更大内容中的位置”。`value` 通常表示当前滚动偏移，`pageStep` 通常表示一页可见内容大小。

大多数时候你不会手动创建滚动条，因为 `QScrollArea`、`QAbstractScrollArea`、各类视图已经内置了滚动条。只有在自定义视口、同步多个滚动位置或做特殊滚动控制时，才需要直接使用它。

### 适合使用的场景

- 自定义绘图区或画布需要手动控制可见区域。
- 多个视图需要共享或同步滚动位置。
- 需要单独放置滚动条，而不是使用 `QScrollArea` 默认布局。
- 需要扩展 Qt 6.10 起的标准滚动条右键菜单。

### 不适合的场景

- 普通内容滚动优先用 `QScrollArea` 或视图自带滚动条。
- 参数调节用 `QSlider` 或 `QDial`。
- 精确数值输入用 spin box。

## 2. 依赖与对象关系

- 头文件：`#include <QScrollBar>`
- 模块：Qt Widgets
- CMake：`find_package(Qt6 REQUIRED COMPONENTS Widgets)`，并链接 `Qt6::Widgets`
- 继承自：`QAbstractSlider`
- 直接派生类：类页未列出

`QScrollBar` 的范围、value、singleStep、pageStep、orientation、tracking、滚轮和键盘行为来自 `QAbstractSlider`。它自己主要提供滚动条外观、滚动条上下文菜单和平台 style 集成。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QScrollBar(QWidget *parent)` | 创建默认垂直滚动条。 |
| `QScrollBar(Qt::Orientation, QWidget *parent)` | 创建指定方向滚动条。 |
| `~QScrollBar()` | 销毁滚动条。 |
| `createStandardContextMenu(QPoint position)` | Qt 6.10 起创建标准右键菜单，所有权给调用方。 |
| `sizeHint() const` | 返回滚动条推荐尺寸。 |
| `initStyleOption(QStyleOptionSlider *)` | 为绘制准备滚动条 style option。 |
| `contextMenuEvent(QContextMenuEvent *)` | 默认显示标准右键菜单。 |
| `sliderChange(SliderChange)` | 响应范围、值、方向等变化并更新显示。 |
| `wheelEvent(QWheelEvent *)` | 把滚轮转换为滚动位置变化。 |
| `mousePressEvent()` / `mouseMoveEvent()` / `mouseReleaseEvent()` | 处理拖动滑块、点击轨道、按钮等交互。 |
| `paintEvent()` | 绘制滚动条各子控件。 |
| `hideEvent()` / `event()` | 处理隐藏和通用事件。 |

## 4. API 逐项说明

### 构造函数

`QScrollBar(QWidget *parent)` 创建默认垂直滚动条；`QScrollBar(Qt::Orientation, QWidget *parent)` 指定水平或垂直方向。

默认范围、步长、初始值来自 `QAbstractSlider`。实际用于滚动内容时，要根据内容总尺寸和视口尺寸设置范围与 page step。

### `~QScrollBar()`

销毁滚动条。若滚动条由滚动区域或父控件管理，通常无需手动删除。

自定义滚动条若和视口互相连接信号，销毁时 QObject 会断开连接，但外部裸指针仍需避免继续使用。

### `createStandardContextMenu(QPoint position)`

Qt 6.10 起提供。创建滚动条标准右键菜单，菜单所有权交给调用方。默认 `contextMenuEvent()` 会使用它。

想扩展菜单时，可以重写 `contextMenuEvent()`，调用这个函数拿到标准菜单，再追加动作。记得处理菜单生命周期，例如弹出后删除或设置 `WA_DeleteOnClose`。

### `contextMenuEvent(QContextMenuEvent *event)`

默认显示标准上下文菜单。若不想要滚动条右键菜单，可以设置 `contextMenuPolicy` 为 `Qt::NoContextMenu`。

某些平台或 style 会通过 style hint 影响菜单行为，定制时要测试目标平台。

### `initStyleOption(QStyleOptionSlider *option) const`

填充滚动条绘制需要的状态，包括方向、范围、当前位置、页面步长、子控件状态等。

自定义绘制滚动条时优先使用它和 `QStyle`，避免破坏平台外观。

### `sizeHint() const`

返回推荐尺寸。滚动条宽度/高度高度依赖平台 style 和方向。

不要用固定宽度假设所有平台滚动条都一样；现代桌面环境可能有覆盖式或较细的滚动条。

### `sliderChange(QAbstractSlider::SliderChange change)`

范围、值、方向或步长变化时调用。`QScrollBar` 用它更新自身显示。

自定义滚动条同步视口时，通常通过信号连接处理，不必重写这个函数。

### `wheelEvent(QWheelEvent *event)`

处理滚轮，让滚动条 value 改变。高精度触控板可能提供像素增量，传统鼠标滚轮提供角度增量；Qt 会在事件中区分。

如果你的滚动区域要支持平滑滚动或惯性滚动，可能要在视口层处理滚轮，而不是只改滚动条。

### 鼠标和绘制事件

鼠标事件处理拖动滑块、点击轨道、点击上下箭头等行为；绘制事件按 style 画出滚动条子控件。

滚动条交互是平台习惯很强的控件，除非确有必要，不要大幅改写鼠标行为。

## 5. 深入实践与常见坑

### pageStep 应该反映可见页面

滚动内容时，`pageStep` 通常设为视口大小。它会影响滑块长度，也影响 PageUp/PageDown 或点击轨道的移动距离。

### 范围不是内容总长度

常见滚动范围是 `0` 到 `contentSize - viewportSize`，而不是 `contentSize`。否则滚到末尾会露出空白。

### 优先使用现成滚动区域

`QAbstractScrollArea` 已经处理滚动条、视口、边框、角落控件和事件转发。只有自定义需求明确时才手写滚动条同步。
