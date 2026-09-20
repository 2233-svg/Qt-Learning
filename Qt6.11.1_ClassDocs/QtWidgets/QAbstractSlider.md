# QAbstractSlider

> Qt 6.11.1 · Qt Widgets · 来自 `QAbstractSlider`

## 1. 先建立直觉

### 这是什么

`QAbstractSlider` 是 Qt Widgets 中“范围内整数位置控件”的基类。`QSlider`、`QScrollBar`、`QDial` 都使用同一套模型：有最小值、最大值、当前值、小步长、大步长、方向、拖动中的临时位置，以及一组用户动作信号。

它不只是“滑块”。更准确地说，它定义了一个可用键盘、鼠标、滚轮和重复动作改变的整数范围状态机。具体子类决定这个状态机长成水平滑条、滚动条还是旋钮。

### 适合使用的场景

- 理解 slider、scrollbar、dial 的共同值模型。
- 自定义一种基于整数范围的交互控件。
- 需要区分拖动中的 `sliderPosition` 和已经提交的 `value`。
- 需要控制 tracking、反向外观、反向控制、重复动作。

### 不适合的场景

- 用户需要输入精确数值时，用 `QSpinBox` 或 `QLineEdit`。
- 需要浮点范围时，用整数映射或专门控件，不要假设 slider 支持 double。
- 数据列表滚动通常直接使用视图自带滚动条，不需要手动创建。

## 2. 依赖与对象关系

- 头文件：`#include <QAbstractSlider>`
- 模块：Qt Widgets
- CMake：`find_package(Qt6 REQUIRED COMPONENTS Widgets)`，并链接 `Qt6::Widgets`
- 继承自：`QWidget`
- 直接派生类：`QDial`、`QScrollBar`、`QSlider`

### 值、位置和跟踪

`value` 是已提交的当前值。`sliderPosition` 是滑块手柄当前所在位置；拖动时它可以先变化。`tracking` 决定拖动过程中是否立即把 position 同步成 value 并发出 `valueChanged()`。

关闭 tracking 时，用户拖动中可以看到手柄移动，但真正的值通常到释放时才更新。这对昂贵预览非常有用。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `enum SliderAction` | 抽象动作：单步增减、页步增减、到最小/最大、移动。 |
| `minimum : int` / `maximum : int` | 有效整数范围。 |
| `value : int` | 已提交当前值。 |
| `sliderPosition : int` | 手柄当前位置，拖动时可先于 value 变化。 |
| `tracking : bool` | 拖动中是否实时发出值变化。 |
| `singleStep : int` | 方向键、滚轮等小步变化量。 |
| `pageStep : int` | PageUp/PageDown 或轨道点击的大步变化量。 |
| `orientation : Qt::Orientation` | 水平或垂直方向。 |
| `invertedAppearance : bool` | 是否反转最小/最大值的视觉位置。 |
| `invertedControls : bool` | 是否反转滚轮和键盘方向。 |
| `sliderDown : bool` | 手柄是否正被按下。 |
| `setRange(min, max)` | 一次设置范围。 |
| `setValue(int)` | 设置当前值并限制在范围内。 |
| `setSliderPosition(int)` | 设置手柄位置。 |
| `triggerAction(SliderAction)` | 程序化触发滑块动作。 |
| `setRepeatAction(action, threshold, repeat)` | 设置按住后重复触发的动作。 |
| `repeatAction() const` | 返回当前重复动作。 |
| `valueChanged(int)` | 当前值变化时发出。 |
| `sliderMoved(int)` | 用户拖动手柄时发出位置。 |
| `sliderPressed()` / `sliderReleased()` | 手柄按下和释放。 |
| `rangeChanged(int, int)` | 范围变化时发出。 |
| `actionTriggered(int)` | 抽象动作触发后、value 同步前发出。 |
| `sliderChange(SliderChange)` | 子类响应范围、步长、值、方向变化的钩子。 |
| `keyPressEvent()` / `wheelEvent()` / `timerEvent()` | 键盘、滚轮、重复动作处理。 |

## 4. API 逐项说明

### `SliderAction`

表示用户或程序触发的抽象动作：小步加、小步减、大步加、大步减、到最小、到最大、移动等。它比鼠标或键盘事件更高一层。

连接 `actionTriggered(int)` 可以在 value 真正传播前调整 `sliderPosition`，适合做吸附、跳格或自定义步进。

### `minimum` / `maximum` / `setRange()`

定义整数范围。设置一端时 Qt 会保持范围有效，并把当前值压回范围内。`setRange()` 更适合初始化或整体更新。

默认常见范围是 0 到 99。使用前要设置成业务范围，否则 UI 会给用户错误边界。

### `value`

已提交当前值。程序调用 `setValue()` 会限制到范围内，并在变化时发出 `valueChanged(int)`。

如果你要响应真实业务变化，优先监听 `valueChanged()`，而不是 `sliderMoved()`。

### `sliderPosition`

手柄当前位置。tracking 开启时通常等于 value；tracking 关闭时，拖动过程中它可能只是临时位置。

需要在拖动时显示预览数值但不提交时，使用 `sliderMoved(int)` 或 `sliderPosition()`。

### `tracking`

决定拖动中是否实时更新 value。默认通常开启。

图像滤镜、昂贵计算、远程请求类场景建议关闭 tracking，然后在 `sliderReleased()` 或 `valueChanged()` 最终触发时处理。

### `singleStep` / `pageStep`

`singleStep` 是小步变化，常对应方向键或滚轮；`pageStep` 是大步变化，常对应 PageUp/PageDown 或点击轨道。

对滑块来说，page step 也影响用户感觉“点一下轨道跳多少”。它应和范围尺度相匹配。

### `orientation`

控制水平或垂直布局。子类外观和 size hint 会随方向改变。

不要用旋转变换模拟方向，直接设置 orientation 更符合 style 和辅助功能。

### `invertedAppearance` / `invertedControls`

`invertedAppearance` 反转值在视觉上的方向；`invertedControls` 反转键盘/滚轮控制方向。二者可以独立设置。

音频、亮度这类通常最小在左/下，最大在右/上；某些坐标轴、滚动语义可能需要反转。

### `sliderDown`

表示手柄是否正被按住。程序调用 `setSliderDown()` 会发出 pressed/released 信号。

普通代码很少主动设置它；它更多用于自定义控件同步内部状态。

### `triggerAction()` / `setRepeatAction()` / `repeatAction()`

`triggerAction()` 以统一方式触发滑块动作。`setRepeatAction()` 设置按住后重复触发的动作及时间参数，`repeatAction()` 读取当前重复动作。

这些 API 常用于子类实现按钮按住、轨道按住等行为。

### 信号组

`valueChanged()` 表示值提交变化；`sliderMoved()` 表示用户拖动位置；`sliderPressed()` / `sliderReleased()` 表示拖动生命周期；`rangeChanged()` 表示边界变化；`actionTriggered()` 表示某个动作刚触发。

不要把所有逻辑都连到 `valueChanged()`。预览、提交、日志、边界同步应该选不同信号。

### `sliderChange(SliderChange change)`

子类钩子，用来响应范围、方向、步长、值变化。默认通常只是更新显示。

自定义 slider 外观时，重写它比在多个 setter 后手动刷新更集中。

### 事件函数

键盘、滚轮和定时器事件负责把用户输入变成 slider action。`wheelEvent()` 在表单里尤其容易误触，必要时可在具体子类中过滤。

重写事件时，未处理的情况交给基类，保留键盘可访问性和平台习惯。

## 5. 深入实践与常见坑

### tracking 是性能开关

实时拖动滤镜或音量很自然；实时触发网络请求或大图重算就很危险。关闭 tracking 可以让用户拖动顺滑，释放后再提交。

### slider 只有整数

浮点值要映射。例如 0.0 到 1.0 可以映射到 0 到 1000，再除以 1000。文档里要写清楚映射精度。

### 外观反转和控制反转不是一回事

只反转视觉不一定反转键盘/滚轮。坐标类控件要同时考虑用户看到的方向和操作方向。
