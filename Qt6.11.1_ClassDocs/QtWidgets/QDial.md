# QDial

> Qt 6.11.1 · Qt Widgets · 来自 `QDial`

## 1. 先建立直觉

### 这是什么

`QDial` 是旋钮式数值控件。它继承 `QAbstractSlider` 的整数范围、value、tracking、步长和信号模型，但把线性轨道换成圆形或近圆形交互。

它适合模仿物理旋钮：音量、声像、亮度、角度、仪表参数。和 `QSlider` 相比，`QDial` 更节省线性空间，也更有“调节旋钮”的感受，但精确读数通常更弱，需要搭配 label 或数值控件。

### 适合使用的场景

- 音频、控制台、仪表盘风格的参数调节。
- 范围是循环或接近循环的值，例如角度。
- 需要紧凑地放置多个调节器。
- 需要刻度凹槽辅助感知范围。

### 不适合的场景

- 表单里精确输入数值，用 spin box。
- 普通线性参数调节，用 slider 更直观。
- 没有数值反馈时，不适合调关键参数。

## 2. 依赖与对象关系

- 头文件：`#include <QDial>`
- 模块：Qt Widgets
- CMake：`find_package(Qt6 REQUIRED COMPONENTS Widgets)`，并链接 `Qt6::Widgets`
- 继承自：`QAbstractSlider`
- 直接派生类：类页未列出

`QDial` 只新增旋钮相关 API：刻度凹槽、凹槽目标间距、是否显示凹槽、是否首尾环绕。范围、步长、value、tracking、反向控制等仍来自 `QAbstractSlider`。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `notchSize : int` | 当前刻度凹槽对应的值间隔，只读。 |
| `notchTarget : qreal` | 期望凹槽之间的像素距离。 |
| `notchesVisible : bool` | 是否显示旋钮周围刻度。 |
| `wrapping : bool` | 是否允许首尾相接环绕调节。 |
| `QDial(QWidget *parent)` | 创建旋钮控件。 |
| `~QDial()` | 销毁旋钮。 |
| `setNotchTarget(double)` | 设置刻度目标间距。 |
| `setNotchesVisible(bool)` | 显示或隐藏刻度凹槽。 |
| `setWrapping(bool)` | 开启或关闭环绕。 |
| `sizeHint()` / `minimumSizeHint()` | 返回推荐尺寸。 |
| `initStyleOption(QStyleOptionSlider *)` | 为绘制准备 style option。 |
| `sliderChange(SliderChange)` | 范围、值、步长变化时更新旋钮显示。 |
| `resizeEvent()` / `paintEvent()` | 处理尺寸和绘制。 |
| `mousePressEvent()` / `mouseMoveEvent()` / `mouseReleaseEvent()` | 处理旋钮拖动。 |
| `event()` | 通用事件入口。 |

## 4. API 逐项说明

### `notchSize`

当前刻度凹槽对应的值间隔。它不是像素，而是值域里的步距；Qt 会根据 `singleStep()`、范围和 `notchTarget` 推导出一个合适值。

读取它可以知道当前视觉刻度大约代表多少值。

### `notchTarget`

期望相邻凹槽之间的像素距离。默认值较小，实际凹槽间隔可能因控件大小、范围、style 和 single step 调整。

如果刻度太密或太稀，调整它比手动画刻度更稳。

### `notchesVisible`

控制是否显示旋钮周围刻度。刻度能帮助用户理解范围和步进，但也会增加视觉复杂度。

参数少、空间紧凑时可以关闭；需要精确感知范围时打开。

### `wrapping`

开启后，旋钮可以从最大值继续转到最小值，形成环绕。关闭时，表盘底部会留出断口，指示范围两端不相连。

角度、相位等循环量适合 wrapping；音量、亮度、数量通常不适合。

### 构造和析构

`QDial(QWidget *parent)` 创建旋钮，范围和默认值来自 `QAbstractSlider`。析构通常由父控件负责。

创建后应设置范围、步长、是否环绕以及是否显示刻度。

### `setNotchTarget()` / `setNotchesVisible()` / `setWrapping()`

分别控制刻度密度、刻度可见性和环绕行为。它们改变的是旋钮外观和交互边界，不改变 value 类型。

环绕开启时，用户可能从最大值一下跳到最小值；业务侧要确认这种跳变是否合理。

### `sizeHint()` / `minimumSizeHint()`

返回旋钮建议尺寸。旋钮需要足够的正方形空间，太窄会让拖动和刻度都难用。

布局中不要把 dial 拉成长条；如果空间是线性的，用 slider。

### `initStyleOption()`

填充 `QStyleOptionSlider`。自定义绘制时使用它，以保留范围、值、方向、tick/notch、启用状态等信息。

平台 style 对 dial 外观差异可能较大，定制时要测试目标系统。

### 事件、绘制和变化钩子

鼠标事件把圆周拖动转换为值变化；`resizeEvent()` 更新几何；`paintEvent()` 绘制旋钮；`sliderChange()` 响应范围和值变化。

普通业务代码通过 `valueChanged()` 连接即可，不需要重写这些底层函数。

## 5. 深入实践与常见坑

### 给旋钮配数值反馈

旋钮本身不易精确读数。关键参数旁边放 label、LCD、spin box 或 tooltip，用户会更有把握。

### wrapping 只给循环量

最大音量继续转到静音通常很危险；角度 359 到 0 则很自然。是否环绕要看物理含义。

### 多个旋钮要统一范围和刻度

音频面板里多个 dial 如果范围、步长、刻度密度不一致，会让用户很难形成肌肉记忆。
