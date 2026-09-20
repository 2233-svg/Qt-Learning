# QStyleOptionSpinBox

> Qt 6.11.1 · Qt Widgets · 来自 `QStyleOptionSpinBox`

## 1. 先建立直觉

`QStyleOptionSpinBox` 是 spin box 绘制参数包。它描述文本编辑框、上下按钮、frame，以及当前能否向上/向下 step。

SpinBox 是复杂控件，所以它继承自 `QStyleOptionComplex`，style 可以分别绘制和命中上按钮、下按钮、编辑区域。

## 2. 类说明

`QStyleOptionSpinBox` 主要用于 `QStyle::CC_SpinBox`。控件将是否有 frame、按钮符号、step enabled 状态等放入 option，style 负责按平台外观绘制。

它不保存数值本身，数值显示通常由内部 line edit 或控件文本负责。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `buttonSymbols` | 上下按钮显示样式，如箭头或无按钮。 |
| `stepEnabled` | 当前是否允许 step up/down。 |
| `frame` | 是否绘制边框。 |
| `subControls` | 要绘制的子控件集合。 |
| `activeSubControls` | 当前活动子控件。 |
| `QStyle::CC_SpinBox` | 绘制 spin box complex control。 |
| `QStyle::SC_SpinBoxUp` | 上按钮子控件。 |
| `QStyle::SC_SpinBoxDown` | 下按钮子控件。 |
| `QStyle::SC_SpinBoxEditField` | 编辑区域子控件。 |
| `QAbstractSpinBox::StepEnabled` | stepEnabled 的来源。 |

## 4. 关键用法

```cpp
QStyleOptionSpinBox opt;
opt.initFrom(this);
opt.frame = hasFrame();
opt.buttonSymbols = buttonSymbols();
opt.stepEnabled = stepEnabled();

QStylePainter p(this);
p.drawComplexControl(QStyle::CC_SpinBox, opt);
```

获取编辑区域：

```cpp
QRect editRect = style()->subControlRect(QStyle::CC_SpinBox, &opt,
                                         QStyle::SC_SpinBoxEditField, this);
```

## 5. 使用场景

适合自定义 spin box、时间/日期/数值编辑控件、style 实现、需要精确绘制上下按钮的复合控件。

普通使用 `QSpinBox`、`QDoubleSpinBox` 时不需要直接操作它。

## 6. 常见坑与经验

禁用 step up/down 不等于整个控件禁用。`stepEnabled` 应准确反映当前值是否到边界。

按钮区域由 style 决定。不要硬编码右侧 16 像素作为上下按钮，平台差异会打脸。

无 frame 或无按钮符号时，编辑区域会变化，布局和绘制都要使用 style 查询结果。
