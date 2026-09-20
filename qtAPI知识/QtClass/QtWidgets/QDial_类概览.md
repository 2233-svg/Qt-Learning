# Qt QDial 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）  
> 头文件：`#include <QDial>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QWidget -> QAbstractSlider -> QDial`  
> 定位：以圆形旋钮交互控制有界整数值的控件

## 1. QDial 解决什么问题

`QDial` 与 `QSlider` 使用相同的值模型，但它把手柄移动呈现为旋钮转动。它特别适合：

- 角度、相位、色相等天然循环的值；
- 音频混音台的增益、声像、滤波参数；
- 工业设备或仪表盘式的紧凑方形控制区；
- 希望用户感知“转动”而不是“拖条”的参数。

```text
          0 / 360
             |
        .---------.
      /    50      \
     |       ^       |   <- 指针
      \             /
        '---------'
```

普通线性值（音量、缩放）并不必然要用旋钮。`QDial` 占用近似正方形空间，精确定位不如长 slider；范围较大、需要迅速定位时通常选 `QSlider` 或 `QSpinBox`。

## 2. wrapping：角度控制与普通旋钮的分界

```cpp
dial->setRange(0, 359);
dial->setWrapping(true);
```

`wrapping` 是 QDial 最有辨识度的属性：

| 设置 | 视觉和交互结果 | 适合场景 |
| --- | --- | --- |
| `false`（默认） | 底部留出缺口，指针只在上方大部分圆弧内活动；进入缺口时夹到 range 两端。 | 0 到 100 的普通参数。 |
| `true` | 没有端点缺口，指针可指向任意角度。 | 0 到 359 度、相位、循环选择。 |

`wrapping=true` 只改变旋钮对 range 两端的呈现与拖动路径，不会让 `value` 超出 `minimum` 到 `maximum`。如果业务上 `359` 后要回到 `0`，仍应明确按范围处理，并在模型层决定是否允许跨界连续编辑。

## 3. 刻度：notchTarget 与 notchSize 不是像素值的同义词

```cpp
dial->setNotchesVisible(true);
dial->setNotchTarget(5.0);
```

- `notchesVisible`：是否画一圈刻度。
- `notchTarget`：Qt 希望相邻刻度在屏幕上相距的目标像素数，默认约为 `3.7`。
- `notchSize`：实际相邻刻度间隔多少个**范围控制单位**，只读。

`notchSize` 不是像素。Qt 会根据控件尺寸、range 与 `singleStep()`，选择一个能使屏幕刻度间距接近 `notchTarget` 的 `singleStep` 倍数。空间不足时，它会跳过一些逻辑步长，尽量画出均匀且不拥挤的刻度。

因此，不能假设“每个 single step 都有一个刻度”。如果用户必须理解离散档位，除了 notch 还应配合数值标签、`QSpinBox` 或明确的单位说明。

## 4. 值模型仍来自 QAbstractSlider

```cpp
dial->setRange(-12, 12);
dial->setSingleStep(1);
dial->setPageStep(3);
dial->setTracking(false);
```

`QDial` 继承的语义不变：

- `value` 是已提交值；
- `sliderPosition` 是拖动中的指针位置；
- tracking 默认开启，拖动中连续发 `valueChanged()`；
- tracking 关闭时，拖动仍连续发 `sliderMoved()`，通常在鼠标释放后才提交 value；
- `sliderPressed()` / `sliderReleased()` 只覆盖鼠标按下、释放。键盘和滚轮也能改 value，但未必产生这两个信号。

音频或图像实时调参常保留 tracking；拖动一次会触发昂贵重新计算时可关闭 tracking，在 `sliderMoved()` 更新轻量预览、在 `valueChanged()` 做完整提交。

鼠标滚轮增量取 `wheelScrollLines * singleStep` 与 `pageStep` 中较小者，因此 page step 过小会限制一次滚轮的移动量。

## 5. 最小示例：角度控制

```cpp
auto *rotation = new QDial;
rotation->setRange(0, 359);
rotation->setWrapping(true);
rotation->setNotchesVisible(true);
rotation->setNotchTarget(6.0);
rotation->setSingleStep(5);

connect(rotation, &QDial::valueChanged, preview,
        [preview](int degrees) {
            preview->setRotation(degrees);
        });
```

若值代表完整角度而非离散档位，`singleStep=1` 可以保留精度；但 notch 实际间隔仍由 Qt 根据像素空间决定。对于 0 到 359 的旋钮，显示当前数值标签往往比试图画 360 根刻度更可用。

## API 速查表
### 6.1 QDial 自有属性、构造与绘制接口

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QDial(QWidget *parent = nullptr)` | 创建圆形旋钮控件 | 值模型来自 `QAbstractSlider`，默认范围是 `0..99`；创建后通常设置 range、步长和是否环绕 |
| 生命周期 | `~QDial()` | 销毁旋钮控件 | 由父对象管理时无需手动释放 |
| 环绕 | `wrapping() const` | 查询旋钮是否使用无缺口环绕显示 | 默认 `false`；适合判断当前旋钮是普通有端点参数还是循环参数 |
| 环绕 | `setWrapping(bool on)` | 设置旋钮是否环绕 | 角度、相位、色相这类循环值常设为 `true`；它不改变 `minimum()` / `maximum()` 的合法范围 |
| 刻度 | `notchesVisible() const` | 查询是否绘制刻度线 | 默认 `false`；小控件或大范围值上刻度可能反而干扰阅读 |
| 刻度 | `setNotchesVisible(bool visible)` | 显示或隐藏旋钮刻度 | 刻度只是视觉辅助，不能替代数值标签或离散档位校验 |
| 刻度 | `notchTarget() const` | 读取相邻刻度的目标屏幕间距 | 单位接近像素，是布局和绘制参考，不是业务值间隔 |
| 刻度 | `setNotchTarget(double target)` | 设置相邻刻度希望保持的屏幕间距 | 默认约 `3.7`；Qt 会根据控件尺寸和步长折算实际刻度间隔 |
| 刻度 | `notchSize() const` | 读取实际相邻刻度之间相隔多少个值单位 | 只读，通常是 `singleStep()` 的倍数；不要假设每个 single step 都画一根刻度 |
| 尺寸 | `minimumSizeHint() const` | 返回旋钮最小推荐尺寸 | 旋钮需要接近正方形空间，过窄会让指针和刻度难读 |
| 尺寸 | `sizeHint() const` | 返回旋钮推荐尺寸 | 交给外层 layout 协商；必要时用布局约束保持正方形感 |
| 样式 | `initStyleOption(QStyleOptionSlider *option) const` | 填充当前旋钮的样式参数 | 自定义派生类想沿用平台样式绘制时使用 |
| 事件 | `event(QEvent *event)` | 处理通用事件入口 | 普通业务代码不直接调用，派生类重写时要尊重父类处理 |
| 事件 | `mousePressEvent(QMouseEvent *event)` | 处理鼠标按下旋钮 | 关联拖动开始和 `sliderPressed()` 语义 |
| 事件 | `mouseMoveEvent(QMouseEvent *event)` | 处理鼠标拖动旋钮 | 更新 `sliderPosition`；`tracking` 决定是否同步提交到 `value` |
| 事件 | `mouseReleaseEvent(QMouseEvent *event)` | 处理鼠标释放旋钮 | `tracking=false` 时通常在释放后才提交最终值 |
| 绘制 | `paintEvent(QPaintEvent *event)` | 绘制旋钮、指针和刻度 | 定制外观时优先考虑 `QStyle`，避免硬编码破坏平台一致性 |
| 布局 | `resizeEvent(QResizeEvent *event)` | 控件尺寸变化后更新内部几何 | 影响刻度密度、指针位置和可用圆弧 |
| 变化通知 | `sliderChange(SliderChange change)` | range、步长、值等滑块状态变化时被调用 | 派生控件可在这里同步缓存或触发重绘 |

### 6.2 继承自 QAbstractSlider 的关键 API

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 范围 | `setRange(int min, int max)` | 设置旋钮合法整数范围 | 角度常用 `0..359`；范围本身不因为 `wrapping=true` 而变成无限循环 |
| 值 | `value() const` / `setValue(int value)` | 读取或设置已提交值 | 业务状态通常跟随 `valueChanged(int)`，不要把拖动中的预览值误当最终提交 |
| 位置 | `sliderPosition() const` / `setSliderPosition(int)` | 读取或设置拖动中的指针位置 | `tracking=false` 时它可能暂时不同于 `value()` |
| 步长 | `singleStep() const` / `setSingleStep(int step)` | 设置方向键、滚轮的小步长 | 也参与 `notchSize()` 的计算，影响刻度稀疏程度 |
| 步长 | `pageStep() const` / `setPageStep(int step)` | 设置 PageUp/PageDown 大步长 | 鼠标滚轮一次移动量也会受到 page step 限制 |
| 提交策略 | `hasTracking() const` / `setTracking(bool enable)` | 控制拖动过程中是否持续提交 `value` | 实时音频/图像参数可开启；昂贵计算可关闭，在释放后提交 |
| 方向 | `invertedAppearance() const` / `setInvertedAppearance(bool)` | 反转值在旋钮上的视觉方向 | 它改变显示方向，不等同于反转键盘和滚轮控制 |
| 方向 | `invertedControls() const` / `setInvertedControls(bool)` | 反转键盘、滚轮的增减方向 | 不直接改变指针绘制方向，要和 `invertedAppearance` 分开设计 |
| 信号 | `sliderMoved(int position)` | 拖动过程中位置变化时发出 | `tracking=false` 时可用它做轻量预览 |
| 信号 | `sliderPressed()` / `sliderReleased()` | 鼠标拖动开始和结束时发出 | 键盘、滚轮改值不保证产生这两个信号 |
| 信号 | `valueChanged(int value)` | 已提交值变化时发出 | 保存模型、更新正式预览、触发业务联动的核心信号 |
| 信号 | `actionTriggered(int action)` | 标准滑块动作发生后发出 | 需要吸附到离散档位时，可在这里调整 `sliderPosition` |
