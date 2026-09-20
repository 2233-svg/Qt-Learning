# QStyleOptionFrame

> Qt 6.11.1 · Qt Widgets · 来自 `QStyleOptionFrame`

## 1. 先建立直觉

`QStyleOptionFrame` 是边框类控件的绘制参数包。`QFrame`、输入框外框、面板边界等都需要告诉 style：边框形状、阴影、线宽和内容区域。

它解决的是“这个框应该按当前平台怎样画”，而不是管理控件内容。

## 2. 类说明

`QStyleOptionFrame` 继承自 `QStyleOption`。它包含 `lineWidth`、`midLineWidth`、`frameShape`、`features` 等字段。

style 使用它绘制 `PE_Frame`、`PE_FrameLineEdit`、`PE_FrameGroupBox` 等 primitive 或 control 的边框部分。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `lineWidth` | 主边框宽度。 |
| `midLineWidth` | 中线宽度，常用于 raised/sunken 效果。 |
| `frameShape` | frame 形状，如 box、panel、styled panel。 |
| `features` | frame 特性标志。 |
| `QFrame::frameShape()` | 常作为 frameShape 来源。 |
| `QFrame::lineWidth()` | 常作为 lineWidth 来源。 |
| `QStyle::PE_Frame` | 通用 frame primitive。 |
| `QStyle::PE_FrameLineEdit` | line edit 边框。 |

## 4. 关键用法

```cpp
QStyleOptionFrame opt;
opt.initFrom(this);
opt.lineWidth = lineWidth();
opt.midLineWidth = midLineWidth();
opt.frameShape = frameShape();

QPainter p(this);
style()->drawPrimitive(QStyle::PE_Frame, &opt, &p, this);
```

## 5. 使用场景

适合自定义 frame、输入区域边框、面板边界、style 实现、需要平台一致边框的控件。

普通 `QFrame` 使用者不需要直接创建它，控件内部会处理。

## 6. 常见坑与经验

边框宽度会影响内容区域。绘制和布局都要考虑 frame width，否则文字可能贴边或被压住。

不同 style 对 frameShape 的解释可能不同。不要指望所有平台画出完全一样的凹凸感。

只想画一条分隔线时，`QFrame` 的 HLine/VLine 通常比自定义绘制更简单。
