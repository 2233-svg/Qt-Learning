# QStyleOptionSlider

> Qt 6.11.1 · Qt Widgets · 来自 `QStyleOptionSlider`

## 1. 先建立直觉

`QStyleOptionSlider` 是滑块类范围控件的绘制参数包。`QSlider`、`QScrollBar`、`QDial` 这类控件都需要向 style 描述最小值、最大值、当前位置、方向、刻度和是否倒置。

它继承自 `QStyleOptionComplex`，因为滑块控件往往有 groove、handle、add/sub page 等子区域。

## 2. 类说明

`QStyleOptionSlider` 不保存业务模型，只保存一次绘制/命中所需状态。style 使用它绘制 `CC_Slider`、`CC_ScrollBar`、`CC_Dial` 等 complex control。

范围值和像素位置之间的转换应交给 style 相关工具和控件逻辑处理，不要在绘制里随意硬算。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `minimum` / `maximum` | 范围上下限。 |
| `sliderPosition` | 滑块位置，通常是拖动中的即时位置。 |
| `sliderValue` | 当前实际值。 |
| `singleStep` / `pageStep` | 单步和页步长。 |
| `orientation` | 水平或垂直。 |
| `upsideDown` | 值增长方向是否反转。 |
| `tickPosition` / `tickInterval` | 刻度显示位置和间隔。 |
| `dialWrapping` | dial 是否首尾相接。 |
| `notchTarget` | dial notch 目标密度。 |
| `subControls` / `activeSubControls` | 复杂控件子区域和当前活动区域。 |
| `QStyle::CC_Slider` | 绘制 slider。 |
| `QStyle::CC_ScrollBar` | 绘制 scrollbar。 |
| `QStyle::CC_Dial` | 绘制 dial。 |

## 4. 关键用法

```cpp
QStyleOptionSlider opt;
opt.initFrom(this);
opt.orientation = Qt::Horizontal;
opt.minimum = minimum();
opt.maximum = maximum();
opt.sliderPosition = sliderPosition();
opt.sliderValue = value();
opt.singleStep = singleStep();
opt.pageStep = pageStep();

QStylePainter p(this);
p.drawComplexControl(QStyle::CC_Slider, opt);
```

命中 handle：

```cpp
auto hit = style()->hitTestComplexControl(QStyle::CC_Slider, &opt, pos, this);
```

## 5. 使用场景

适合自定义范围控件、style 实现、需要平台一致滑块外观的控件、delegate 中绘制进度/滑块交互。

普通业务只用 `QSlider` / `QScrollBar` API 即可。

## 6. 常见坑与经验

`sliderPosition` 和 `sliderValue` 可能不同。拖动但尚未提交时尤其要区分。

RTL、垂直方向、`invertedAppearance` 都会影响增长方向，别只按从左到右硬算。

handle 命中区域由 style 决定，用 `hitTestComplexControl()` 比自己猜矩形可靠。
