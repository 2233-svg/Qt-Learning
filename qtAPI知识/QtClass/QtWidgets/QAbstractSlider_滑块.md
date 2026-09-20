# Qt QAbstractSlider 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）  
> 头文件：`#include <QAbstractSlider>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QWidget -> QAbstractSlider`  
> 定位：为滑块、滚动条、旋钮提供统一的整数范围与交互状态模型

## 1. QAbstractSlider 解决什么问题

`QAbstractSlider` 把“用户在一个有界整数范围内移动位置”这件事抽象出来。`QSlider`、`QScrollBar`、`QDial` 都共享它的核心状态：

```text
minimum <= value <= maximum

singleStep  小步，例如方向键
pageStep    大步，例如 PageUp / PageDown
sliderPosition  拖动中的位置
tracking        是否拖动时立即提交 value
```

它在 C++ 层面不是纯抽象类，可以构造；但它没有为终端用户提供完整的可视交互外观，因此应用通常直接使用 `QSlider`、`QScrollBar`、`QDial`，或在自定义控件中继承它。

它解决的是“值、范围、输入动作和通知”的一致性，不解决具体外观。自定义控件需要自己把屏幕坐标映射到范围值，并绘制滑槽、手柄或刻度；Qt 提供 `QStyle::sliderValueFromPosition()`、`QStyle::sliderPositionFromValue()` 作为辅助。

## 2. 先掌握三个数：value、sliderPosition、tracking

这是最重要的关系：

```text
tracking = true（默认）
  拖动手柄
    sliderPosition 改变
    value 同步改变
    valueChanged(...) 持续发出

tracking = false
  拖动手柄
    sliderPosition 改变
    sliderMoved(...) 持续发出
    value 保持旧值
  松开手柄
    value 提交为 sliderPosition
    valueChanged(...) 发出
```

| 状态 | 表示什么 | 适合什么场景 |
| --- | --- | --- |
| `value` | 已提交的逻辑值。 | 改变音量、缩放比例、滚动位置等真实业务状态。 |
| `sliderPosition` | 手柄当前所在位置。 | 拖动预览、尚未提交的值。 |
| `tracking` | 拖动中是否立刻让 position 提交到 value。 | 实时预览设 `true`；昂贵计算、网络请求或重渲染设 `false`。 |

```cpp
slider->setTracking(false);

connect(slider, &QSlider::sliderMoved, this, [this](int position) {
    previewAt(position);     // 轻量预览
});
connect(slider, &QSlider::valueChanged, this, [this](int value) {
    commitExpensiveChange(value); // 松手后才执行
});
```

程序调用 `setValue()` 时，`value` 与 `sliderPosition` 都会更新；`tracking` 主要影响用户拖动期间的提交时机。

## 3. 范围和步长：它们不是同一件事

```cpp
slider->setRange(0, 100);
slider->setSingleStep(1);
slider->setPageStep(10);
slider->setValue(37);
```

- `minimum` / `maximum`：合法值边界。
- `singleStep`：小步，通常对应方向键或滚轮的一次操作。
- `pageStep`：大步，通常对应 PageUp / PageDown 或点击滑槽空白处。
- `value` 不要求是 step 的整数倍。`setValue(37)` 合法，即使 `singleStep` 是 10。

范围始终保持有效：

- 设置 `minimum` 时，必要的话 Qt 会同步调整 `maximum`，并把当前值夹到新范围；
- 设置 `maximum` 时，必要的话 Qt 会同步调整 `minimum`，并把当前值夹到新范围；
- `setRange(min, max)` 若 `max < min`，则 `min` 成为唯一合法值。

构造后的默认状态是：最小值 `0`、最大值 `99`、single step 为 `1`、page step 为 `10`、value 为 `0`；默认方向为 `Qt::Vertical`。

## 4. 输入方向与视觉方向不要混淆

```cpp
slider->setInvertedAppearance(true);
slider->setInvertedControls(true);
```

| 属性 | 改变什么 | 对用户的影响 |
| --- | --- | --- |
| `invertedAppearance` | 最小值、最大值在控件上的视觉位置。 | 例如竖直滑块让最小值显示在顶部。 |
| `invertedControls` | 键盘和滚轮对 value 的增减方向。 | PageUp / 滚轮向上可改为向最小值移动。 |

两者相互独立。只想让竖直音量条“越往上越大”，通常先判断普通 appearance 是否已符合预期，再决定是否反转；不要为了反转键盘方向而误改 appearance。

对于 `QScrollBar`，很多 style 会忽略 `invertedAppearance` 的视觉效果；它主要对 `QSlider`、`QDial` 有意义。

## 5. SliderAction：用户到底触发了什么

滑块动作不是只有“值变了”。`SliderAction` 记录操作类别：

```cpp
slider->triggerAction(QAbstractSlider::SliderPageStepAdd);
```

| 动作 | 含义 | 常见来源 |
| --- | --- | --- |
| `SliderNoAction` | 无动作。 | 空状态或重复动作未设置。 |
| `SliderSingleStepAdd` | 向数值增大方向走一个小步。 | 方向键、滚轮。 |
| `SliderSingleStepSub` | 向数值减小方向走一个小步。 | 方向键、滚轮。 |
| `SliderPageStepAdd` | 向数值增大方向走一个大步。 | PageDown、点击滑槽空白区。 |
| `SliderPageStepSub` | 向数值减小方向走一个大步。 | PageUp、点击滑槽空白区。 |
| `SliderToMinimum` | 跳到最小值。 | Home 或程序控制。 |
| `SliderToMaximum` | 跳到最大值。 | End 或程序控制。 |
| `SliderMove` | 手柄被移动到某个位置。 | 鼠标拖动。 |

`actionTriggered(int action)` 的时序很特殊：信号发出时，`sliderPosition` 已按动作更新，但 `value` 尚未传播、`valueChanged()` 尚未发出、界面也还没更新。这使你可以在这个点修正动作结果：

```cpp
connect(slider, &QAbstractSlider::actionTriggered,
        slider, [slider](int action) {
    if (action == QAbstractSlider::SliderMove) {
        int snapped = (slider->sliderPosition() / 5) * 5;
        slider->setSliderPosition(snapped);
    }
});
```

这种方式适合拖动时吸附到 5 的倍数、时间轴刻度或离散档位。若只是响应最终业务值，监听 `valueChanged()` 更直接。

## 6. 信号如何选

| 信号 | 什么时候发出 | 应连接什么逻辑 |
| --- | --- | --- |
| `valueChanged(int value)` | 已提交 value 改变。 | 更新真实模型、保存配置、触发计算。 |
| `sliderMoved(int position)` | 手柄处于按下状态且发生移动，即使 tracking 关闭也发出。 | 轻量拖动预览。 |
| `sliderPressed()` | 用户按下手柄，或调用 `setSliderDown(true)`。 | 开始临时预览、显示浮层。 |
| `sliderReleased()` | 用户松开手柄，或调用 `setSliderDown(false)`。 | 结束预览、提交收尾操作。 |
| `rangeChanged(int min, int max)` | 合法范围改变。 | 刷新刻度、同步输入框限制。 |
| `actionTriggered(int action)` | 一个滑块动作被触发。 | 拦截并校正 step、吸附或特殊交互。 |

`sliderMoved()` 和 `valueChanged()` 不能互相替代：tracking 关闭时，前者在拖动中持续发出，后者通常在松手时才发出。

## 7. 自定义子类的状态钩子

`sliderDown` 通常由派生类在鼠标按下、释放时维护：

```cpp
setSliderDown(true);  // 同时发出 sliderPressed()
setSliderDown(false); // 同时发出 sliderReleased()
```

自动重复（例如长按按钮持续步进）由以下保护接口控制：

```cpp
setRepeatAction(SliderSingleStepAdd, 500, 50);
```

它表示等待 500 ms 后，每 50 ms 触发一次动作。不要在自动重复键事件期间修改 `singleStep`，Qt 文档将此行为定义为未定义。

当 range、方向、步长或 value 改变时，`sliderChange()` 会收到对应的 `SliderChange`：

| `SliderChange` | 表示什么 |
| --- | --- |
| `SliderRangeChange` | minimum / maximum 改变。 |
| `SliderOrientationChange` | 横向与纵向方向改变。 |
| `SliderStepsChange` | singleStep 或 pageStep 改变。 |
| `SliderValueChange` | 已提交 value 改变。 |

派生控件通常在 `sliderChange()` 中更新缓存、重算手柄几何或请求重绘；基类默认只更新显示。

## API 速查表
下表按 Qt 6.11.1 的 `qabstractslider.h` 直接声明整理。`QSlider`、`QScrollBar` 和 `QDial` 还会增加各自的外观或专用行为；这里先把共同的值模型、动作和通知讲完整。

### 8.1 构造、范围和值模型

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QAbstractSlider(QWidget *parent = nullptr)` | 创建一个提供整数范围和交互状态的滑块基类控件 | 可构造但没有具体滑槽外观；普通 UI 通常使用派生类 |
| 生命周期 | `~QAbstractSlider()` | 销毁滑块基类对象 | 遵循 QWidget 父子对象树 |
| 范围 | `setMinimum(int min)` | 设置合法最小值 | 必要时会调整最大值和当前值，调用后用 getter 读取最终状态 |
| 范围 | `minimum() const` | 读取合法最小值 | 与 `maximum()` 一起定义闭区间 |
| 范围 | `setMaximum(int max)` | 设置合法最大值 | 必要时会调整最小值和当前值 |
| 范围 | `maximum() const` | 读取合法最大值 | 不要把它当成像素长度 |
| 范围 | `setRange(int min, int max)` | 一次设置最小值和最大值 | `max < min` 时会形成只有 `min` 一个合法值的范围 |
| 值 | `setValue(int value)` | 设置已经提交的逻辑值 | 会夹到范围内，并同步 `sliderPosition`；与 tracking 无关 |
| 值 | `value() const` | 读取已经提交的逻辑值 | 业务模型通常监听和读取它 |
| 位置 | `setSliderPosition(int position)` | 设置手柄当前位置 | tracking 关闭时可只改变预览位置，不立即提交 value |
| 位置 | `sliderPosition() const` | 读取手柄当前位置 | 用户拖动期间可能与 `value()` 不同 |
| 步进 | `setSingleStep(int step)` | 设置方向键、滚轮等小步距离 | 它不是强制的值量化器，value 不要求是它的整数倍 |
| 步进 | `singleStep() const` | 读取小步距离 | 自动重复期间不要修改，避免未定义行为 |
| 步进 | `setPageStep(int step)` | 设置 Page 或轨道空白点击的大步距离 | 具体如何使用由派生控件和 style 共同决定 |
| 步进 | `pageStep() const` | 读取大步距离 | 滚动条常把它对应可见页长度 |

### 8.2 方向、跟踪和动作

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 方向 | `setOrientation(Qt::Orientation orientation)` | 设置横向或纵向方向 | 只传 `Qt::Horizontal` 或 `Qt::Vertical` |
| 方向 | `orientation() const` | 读取当前方向 | 默认方向是 `Qt::Vertical` |
| 跟踪 | `setTracking(bool enable)` | 设置拖动手柄时是否立即提交 value | 昂贵计算、网络操作或重渲染可设为 false |
| 跟踪 | `hasTracking() const` | 查询 tracking 状态 | getter 名称不是 `tracking()` |
| 按下状态 | `setSliderDown(bool down)` | 设置手柄是否处于按下状态 | 会触发 `sliderPressed()` / `sliderReleased()`；派生类实现鼠标交互时使用 |
| 按下状态 | `isSliderDown() const` | 查询手柄是否被按住 | 不等价于窗口是否有鼠标抓取 |
| 外观方向 | `setInvertedAppearance(bool on)` | 反转数值在控件视觉上的排列方向 | 不改变键盘和滚轮增减方向；部分 `QScrollBar` style 可能忽略视觉效果 |
| 外观方向 | `invertedAppearance() const` | 查询视觉方向是否反转 | 与 `invertedControls` 独立 |
| 控制方向 | `setInvertedControls(bool on)` | 反转键盘、滚轮等控制动作的增减语义 | 不改变手柄的视觉排列 |
| 控制方向 | `invertedControls() const` | 查询输入控制是否反转 | 不要用它代替 appearance 设置 |
| 动作 | `triggerAction(SliderAction action)` | 程序化触发标准滑块动作 | 可用于快捷键、自定义按钮或同步控件 |
| 动作枚举 | `SliderNoAction` | 表示没有滑块动作 | 不是一个会改变值的动作 |
| 动作枚举 | `SliderSingleStepAdd` / `SliderSingleStepSub` | 按小步增加或减少 | 方向键、滚轮常映射到它们 |
| 动作枚举 | `SliderPageStepAdd` / `SliderPageStepSub` | 按大步增加或减少 | Page 键或轨道空白点击常映射到它们 |
| 动作枚举 | `SliderToMinimum` / `SliderToMaximum` | 跳到范围端点 | Home、End 或程序控制可使用 |
| 动作枚举 | `SliderMove` | 表示手柄移动动作 | `actionTriggered()` 发出时可修正 `sliderPosition` |

### 8.3 信号

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 值通知 | `valueChanged(int value)` | 已提交 value 改变时发出 | 更新真实业务状态；tracking 关闭时通常在释放后才持续提交 |
| 拖动通知 | `sliderMoved(int position)` | 手柄被按住并移动时发出 | 即使 tracking 关闭也会发，适合轻量预览 |
| 拖动通知 | `sliderPressed()` | 手柄进入按下状态时发出 | 开始临时预览或显示浮层 |
| 拖动通知 | `sliderReleased()` | 手柄结束按下状态时发出 | 收尾或提交拖动交互 |
| 范围通知 | `rangeChanged(int min, int max)` | 合法范围改变时发出 | 同步刻度、输入框或范围标签 |
| 动作通知 | `actionTriggered(int action)` | 标准动作发生后、valueChanged 前发出 | 此时 `sliderPosition` 已更新，可做吸附和离散化 |

### 8.4 受保护扩展点和事件

这些函数主要给自定义滑块、滚动条或旋钮派生类使用。普通调用方应优先使用公共 setter、信号和现成派生控件。

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 自动重复 | `setRepeatAction(SliderAction action, int thresholdTime = 500, int repeatTime = 50)` | 配置延迟后反复触发某个动作 | 适合长按自定义步进按钮；与单步值修改的时序要分开 |
| 自动重复 | `repeatAction() const` | 读取当前自动重复动作 | 仅在派生类内部检查 |
| 状态变化 | `sliderChange(SliderChange change)` | 在范围、方向、步长或 value 改变时通知派生类 | 常用于重算手柄几何、缓存和请求重绘 |
| 变化枚举 | `SliderRangeChange` | 表示 minimum 或 maximum 改变 | 在 `sliderChange()` 中处理范围相关几何 |
| 变化枚举 | `SliderOrientationChange` | 表示方向改变 | 重新计算横纵向布局 |
| 变化枚举 | `SliderStepsChange` | 表示 singleStep 或 pageStep 改变 | 刻度或自动重复策略可能需要更新 |
| 变化枚举 | `SliderValueChange` | 表示已提交 value 改变 | 同步绘制位置或派生状态 |
| 事件 | `event(QEvent *e)` | 处理通用 QWidget 事件 | 重写时应把未处理事件交给基类 |
| 键盘 | `keyPressEvent(QKeyEvent *ev)` | 处理方向键、Page、Home、End 等滑块控制 | 保留标准键盘语义，除非实现完整替代行为 |
| 定时器 | `timerEvent(QTimerEvent *)` | 处理自动重复动作的定时器事件 | 通常由基类配合 `setRepeatAction()` 使用 |
| 滚轮 | `wheelEvent(QWheelEvent *e)` | 处理滚轮小步或大步变化 | 受 `invertedControls` 影响；需启用 wheel event 配置 |
| 状态 | `changeEvent(QEvent *e)` | 处理 style、字体、启用状态等变化 | 派生类扩展后通常仍调用基类 |
