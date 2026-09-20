# QStyleOptionSizeGrip

> Qt 6.11.1 · Qt Widgets · 来自 `QStyleOptionSizeGrip`

## 1. 先建立直觉

`QStyleOptionSizeGrip` 是尺寸抓手绘制参数包。`QSizeGrip` 需要告诉 style 自己位于窗口哪个角，style 才能按正确方向画斜线或抓手纹理。

它描述的是 resize corner 的外观，不负责真正调整窗口大小。

## 2. 类说明

`QStyleOptionSizeGrip` 继承自 `QStyleOption`，主要字段是 `corner`。

在 RTL 布局或不同平台窗口装饰中，size grip 可能出现在不同角落，不能只按右下角硬画。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `corner` | 抓手所在角：TopLeft、TopRight、BottomLeft、BottomRight。 |
| `rect` | 抓手绘制区域。 |
| `QStyle::CE_SizeGrip` | 绘制 size grip 的 control。 |
| `QSizeGrip` | 使用该 option 的控件。 |

## 4. 关键用法

```cpp
QStyleOptionSizeGrip opt;
opt.initFrom(this);
opt.corner = Qt::BottomRightCorner;

QStylePainter p(this);
p.drawControl(QStyle::CE_SizeGrip, opt);
```

## 5. 使用场景

适合自定义 size grip、无边框窗口 resize corner、状态栏右下角抓手。

普通窗口可直接使用 `QSizeGrip` 或 `QStatusBar::setSizeGripEnabled()`。

## 6. 常见坑与经验

corner 影响纹理方向。硬画右下角在 RTL 或特殊布局里会显得反。

固定大小窗口不应显示 size grip，否则用户会以为可以调整大小。

抓手的可点击区域可以比视觉纹理略大，提升可用性。
