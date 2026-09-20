# QProgressBar

> Qt 6.11.1 · Qt Widgets · 来自 `QProgressBar`

## 1. 先建立直觉

### 这是什么

`QProgressBar` 是进度显示控件。它把一个整数范围里的当前值画成横向或纵向进度条，并可按格式显示百分比、当前值、总步数等文本。

它只负责“显示进度”，不负责运行任务、取消任务或调度线程。后台工作应通过信号把进度发回 GUI 线程，再调用 `setValue()` 更新。

### 适合使用的场景

- 文件处理、下载、导入、构建等确定总量的任务。
- 状态栏、对话框或面板中的进度反馈。
- 需要显示忙碌状态：把 minimum 和 maximum 都设为 0。
- 需要自定义进度文本格式。

### 不适合的场景

- 需要取消按钮和自动延迟显示时，用 `QProgressDialog`。
- 不知道总进度但只想显示“正在工作”，可用 busy progress 或动画指示。
- 不要在后台线程直接操作进度条。

## 2. 依赖与对象关系

- 头文件：`#include <QProgressBar>`
- 模块：Qt Widgets
- CMake：`find_package(Qt6 REQUIRED COMPONENTS Widgets)`，并链接 `Qt6::Widgets`
- 继承自：`QWidget`
- 直接派生类：类页未列出

进度条通常被其他容器持有，例如状态栏、工具面板、对话框。它没有自己的任务模型；你需要自己决定最大值、当前值和完成时机。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `enum Direction` | 垂直进度条文本方向。 |
| `minimum : int` / `maximum : int` | 进度范围；二者同为 0 时常表示忙碌模式。 |
| `value : int` | 当前进度值。 |
| `format : QString` | 文本格式，支持 `%p`、`%v`、`%m`。 |
| `text : QString` | 当前根据 format 生成的显示文本。 |
| `textVisible : bool` | 是否显示文本，style 可忽略。 |
| `alignment : Qt::Alignment` | 文本对齐。 |
| `orientation : Qt::Orientation` | 水平或垂直进度条。 |
| `textDirection : Direction` | 垂直进度条文本旋转方向。 |
| `invertedAppearance : bool` | 进度增长方向是否反转。 |
| `setRange(min, max)` | 一次设置范围。 |
| `setValue(int)` | 更新当前进度。 |
| `reset()` | 重置为无进度状态。 |
| `resetFormat()` | 恢复默认文本格式。 |
| `valueChanged(int)` | 当前值变化时发出。 |
| `sizeHint()` / `minimumSizeHint()` | 推荐尺寸。 |
| `initStyleOption(QStyleOptionProgressBar *)` | 为绘制准备 style option。 |
| `paintEvent()` / `event()` | 绘制和通用事件处理。 |

## 4. API 逐项说明

### `Direction` / `textDirection`

只影响垂直进度条的文本读取方向：从上到下或从下到上。水平进度条不受影响。

并非所有平台 style 都绘制垂直进度条文本，因此不要把关键进度信息只放在垂直条文字里。

### `minimum` / `maximum` / `setRange()`

范围决定百分比计算。默认通常是 0 到 100。`setRange(0, 0)` 常用于忙碌模式，表示任务正在运行但总量未知。

如果当前值超出新范围，进度条可能重置。更新范围时最好先确定任务总量，再开始发进度。

### `value` / `setValue()` / `valueChanged(int)`

`setValue()` 更新当前进度，值必须在范围内才有意义。变化时发出 `valueChanged(int)`。

进度更新不要过于频繁。高频任务可以按时间或百分比节流，否则 GUI 线程会被刷新拖慢。

### `format` / `text` / `resetFormat()`

`format` 控制文本，`%p` 是百分比，`%v` 是当前值，`%m` 是最大值。默认通常是 `%p%`。`text()` 返回实际生成的文本。

示例：`setFormat("%v / %m files")`。恢复默认用 `resetFormat()`。

### `textVisible` / `alignment`

`textVisible` 控制是否请求绘制文字，但 style 可以忽略。`alignment` 控制文字对齐。

如果文本很重要，建议旁边放独立 `QLabel`，不要完全依赖进度条内部文本。

### `orientation` / `invertedAppearance`

`orientation` 控制水平或垂直；`invertedAppearance` 让进度从相反方向增长，例如右到左。

右到左语言环境、特殊仪表布局可能需要反转，但普通进度条遵循平台默认即可。

### `reset()`

重置进度条，显示为尚未开始或无进度状态。它不取消任务，只改变控件状态。

任务失败、取消或准备复用进度条时可以调用。

### `sizeHint()` / `initStyleOption()` / `paintEvent()`

这些服务布局和绘制。自定义绘制时应使用 `QStyleOptionProgressBar`，保留平台主题、文本、方向和忙碌状态。

普通应用不需要重写绘制；改 format 和 style sheet 已能覆盖多数需求。

## 5. 深入实践与常见坑

### 忙碌模式不是 0%

`setRange(0, 0)` 通常显示忙碌动画，表示不知道总量。它不是“进度为零”。

### 后台线程只发信号

进度条是 QWidget，只能在 GUI 线程更新。worker 线程发 `progressChanged(int)`，连接到主线程里的 `setValue()`。

### 文本格式不要承载全部信息

有些 style 不显示文字。关键任务名、错误、速度、剩余时间最好放独立 label。
