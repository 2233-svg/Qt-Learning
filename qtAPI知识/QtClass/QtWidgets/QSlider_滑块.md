# Qt QSlider 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）  
> 头文件：`#include <QSlider>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QWidget -> QAbstractSlider -> QSlider`  
> 定位：让用户通过拖动手柄设置有界整数值的经典控件

## 1. QSlider 解决什么问题

`QSlider` 适合让用户连续地选择一个有限范围内的整数值，例如音量、缩放比例、透明度、播放进度或画笔大小。

```text
0        25        50        75       100
|---------|---------|---------|---------|
                    [====]
```

它与 `QSpinBox` 的取舍很简单：

- 值的趋势、相对位置比精确输入更重要，用 `QSlider`；
- 用户必须精确键入一个大范围数字，用 `QSpinBox`；
- 两者可绑定到同一个值，形成“拖动粗调 + 输入精调”。

真正的范围、value、tracking、single step、page step、键盘与信号都来自 `QAbstractSlider`。`QSlider` 自己新增的核心能力只有刻度的位置和间隔。

## 2. 最小可用示例：缩放控制

```cpp
auto *zoom = new QSlider(Qt::Horizontal);
zoom->setRange(25, 400);
zoom->setValue(100);
zoom->setSingleStep(5);
zoom->setPageStep(25);
zoom->setTickPosition(QSlider::TicksBelow);
zoom->setTickInterval(25);

connect(zoom, &QSlider::valueChanged, canvas,
        [canvas](int percent) {
            canvas->setZoom(percent / 100.0);
        });
```

`setValue(100)` 是逻辑缩放值 100%，不是 slider 在屏幕上的像素位置。若缩放重绘开销很大，可关闭 tracking，在 `sliderMoved()` 做轻量预览，松手后的 `valueChanged()` 再执行完整重算。

## 3. 刻度的两个维度

`tickPosition` 决定刻度画在滑槽哪边，`tickInterval` 决定相邻刻度差多少个**值单位**：

```cpp
slider->setTickPosition(QSlider::TicksBothSides);
slider->setTickInterval(10);
```

`tickInterval=10` 的意思是值每相差 10 放一个刻度，不是每隔 10 像素。范围从 0 到 100 时通常得到 0、10、20 ... 100 的刻度。

若 interval 为 `0`（默认），QSlider 会在 `singleStep` 与 `pageStep` 之间选择合适值。希望刻度表达固定业务档位时显式设置 interval；不需要刻度时保留默认 `NoTicks`，避免在窄 slider 上堆出无法阅读的短线。

| TickPosition | 水平 slider | 垂直 slider |
| --- | --- | --- |
| `NoTicks` | 不画刻度。 | 不画刻度。 |
| `TicksAbove` | 槽上方。 | 与 `TicksLeft` 同值，槽左侧。 |
| `TicksBelow` | 槽下方。 | 与 `TicksRight` 同值，槽右侧。 |
| `TicksBothSides` | 槽上下两侧。 | 槽左右两侧。 |
| `TicksLeft` | 不应作为水平语义使用。 | 槽左侧。 |
| `TicksRight` | 不应作为水平语义使用。 | 槽右侧。 |

刻度只是视觉提示，不会让 value 自动吸附到 tick interval。需要 5、10、15 这类离散档位时，在 `actionTriggered()` 里修正 `sliderPosition`，或用适当的 single step 与业务映射。

## 4. 鼠标、键盘和范围过大

QSlider 默认接受 Tab 焦点，并支持鼠标滚轮、方向键、PageUp/PageDown、Home、End。它只提供整数范围，范围很大时用户无法靠有限长度的滑槽精确拖到某个值。

经验上：

- 0 到 100、0 到 360、0 到几百：QSlider 很合适；
- 0 到几万：保留 slider 作为粗调，同时配合 `QSpinBox`；
- 无上限时间、文件偏移、海量行：更适合专门的滚动、文本或视图控件。

## API 速查表
### 5.1 QSlider 自有 API

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QSlider(QWidget *parent = nullptr)` | 创建一个滑块控件 | 默认方向来自 Qt 实现的控件默认值；业务界面通常显式使用带 `orientation` 的构造函数 |
| 构造 | `QSlider(Qt::Orientation orientation, QWidget *parent = nullptr)` | 创建水平或垂直滑块 | 只应传 `Qt::Horizontal` 或 `Qt::Vertical`；方向决定布局占位和刻度语义 |
| 生命周期 | `~QSlider()` | 销毁滑块控件 | 生命周期通常交给父 widget 或布局中的父对象 |
| 刻度 | `tickPosition() const` | 读取刻度画在滑槽哪一侧 | 默认 `NoTicks`；水平和垂直方向对同一枚举值的视觉含义不同 |
| 刻度 | `setTickPosition(TickPosition position)` | 设置刻度位置 | 水平常用 `TicksBelow`，垂直常用 `TicksRight`；空间紧张时保留无刻度更清爽 |
| 刻度 | `tickInterval() const` | 读取相邻刻度相差多少个值单位 | 返回值不是像素距离，也不表示手柄吸附间隔 |
| 刻度 | `setTickInterval(int interval)` | 设置刻度的值间隔 | `0` 表示 Qt 在 `singleStep()` 和 `pageStep()` 之间自动选择；离散业务档位仍需单独校验 |
| 尺寸 | `minimumSizeHint() const` | 返回最小推荐尺寸 | 方向、刻度位置和平台样式会影响最小空间 |
| 尺寸 | `sizeHint() const` | 返回推荐尺寸 | 交给外层 layout 协商；范围大小本身不会让控件自动变长 |
| 样式 | `initStyleOption(QStyleOptionSlider *option) const` | 填充当前 slider 的样式参数 | 自定义派生控件想沿用平台样式绘制时使用 |
| 事件 | `event(QEvent *event)` | 处理通用事件入口 | 普通业务代码不直接调用，派生类重写时要保留父类语义 |
| 事件 | `mousePressEvent(QMouseEvent *event)` | 处理滑槽或手柄按下 | 自定义点击跳转、吸附等交互时要小心别破坏拖动开始状态 |
| 事件 | `mouseMoveEvent(QMouseEvent *event)` | 处理手柄拖动 | 通常由基类更新 `sliderPosition`；`tracking` 决定是否同步提交到 `value` |
| 事件 | `mouseReleaseEvent(QMouseEvent *event)` | 处理拖动结束 | 影响 `sliderReleased()` 以及 `tracking=false` 时的最终提交时机 |
| 绘制 | `paintEvent(QPaintEvent *event)` | 绘制滑槽、手柄和刻度 | 自定义外观优先借助 `QStyle` 或样式表，避免硬编码平台细节 |

### 5.2 继承自 QAbstractSlider 的常用 API

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 范围 | `minimum() const` / `setMinimum(int)` | 读取或设置最小合法值 | 设置范围端点会约束当前 `value` 和 `sliderPosition` |
| 范围 | `maximum() const` / `setMaximum(int)` | 读取或设置最大合法值 | 范围越大，有限长度滑槽上的精确拖动越困难 |
| 范围 | `setRange(int min, int max)` | 一次设置合法整数范围 | 初始化时优先用它保证上下界一致 |
| 值 | `value() const` / `setValue(int value)` | 读取或设置已提交值 | 用 `valueChanged(int)` 接收业务更新；它不是像素位置 |
| 位置 | `sliderPosition() const` / `setSliderPosition(int position)` | 读取或设置拖动中的手柄位置 | `tracking=false` 时可能暂时不同于 `value()`，适合预览 |
| 步长 | `singleStep() const` / `setSingleStep(int step)` | 设置方向键、滚轮等小步长 | 表示细调单位，也会影响自动刻度间隔 |
| 步长 | `pageStep() const` / `setPageStep(int step)` | 设置 PageUp/PageDown 大步长 | 适合粗调；也参与 `tickInterval=0` 时的自动选择 |
| 提交策略 | `hasTracking() const` / `setTracking(bool enable)` | 控制拖动时是否持续提交 `value` | 实时预览保留开启；昂贵重算可关闭，释放后再提交 |
| 方向 | `orientation() const` / `setOrientation(Qt::Orientation)` | 查询或设置滑块方向 | 改方向会影响布局尺寸、键盘方向和刻度显示位置 |
| 方向 | `invertedAppearance() const` / `setInvertedAppearance(bool)` | 反转最小值和最大值的视觉方向 | 常用于垂直音量杆或符合领域习惯的坐标方向 |
| 方向 | `invertedControls() const` / `setInvertedControls(bool)` | 反转键盘、滚轮的增减方向 | 不改变刻度绘制位置，要和视觉反转分开判断 |
| 信号 | `sliderMoved(int position)` | 拖动过程中位置变化时发出 | `tracking=false` 时常用它更新轻量预览 |
| 信号 | `sliderPressed()` / `sliderReleased()` | 鼠标拖动开始和结束时发出 | 键盘、滚轮改值不保证产生这两个信号 |
| 信号 | `valueChanged(int value)` | 已提交值变化时发出 | 更新模型、标签、画布等正式业务状态 |
| 信号 | `actionTriggered(int action)` | 标准滑块动作发生后发出 | 需要吸附到离散档位时可在这里修正 `sliderPosition` |

### 5.3 TickPosition 枚举速查

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 枚举值 | `NoTicks` | 不显示刻度 | 默认选择，适合紧凑连续调节 |
| 枚举值 | `TicksAbove` | 水平滑槽上方显示刻度 | 垂直方向下它与 `TicksLeft` 是同一个数值 |
| 枚举值 | `TicksBelow` | 水平滑槽下方显示刻度 | 垂直方向下它与 `TicksRight` 是同一个数值 |
| 枚举值 | `TicksBothSides` | 滑槽两侧都显示刻度 | 需要更明显标尺且空间充足时使用 |
| 枚举值 | `TicksLeft` | 垂直滑槽左侧显示刻度 | 是 `TicksAbove` 的别名，不应在水平语义里强行使用 |
| 枚举值 | `TicksRight` | 垂直滑槽右侧显示刻度 | 是 `TicksBelow` 的别名，垂直 slider 常用 |
