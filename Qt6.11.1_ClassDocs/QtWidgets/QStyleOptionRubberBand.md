# QStyleOptionRubberBand

> Qt 6.11.1 · Qt Widgets · 来自 `QStyleOptionRubberBand`

## 1. 先建立直觉

`QStyleOptionRubberBand` 是 `QRubberBand` 绘制参数包。它告诉 style 当前橡皮筋是矩形还是线条，以及是否用不透明绘制。

橡皮筋常用于框选、拖拽预览、插入位置提示。

## 2. 类说明

`QStyleOptionRubberBand` 继承自 `QStyleOption`。主要字段是 `shape` 和 `opaque`。

style 使用它绘制 `QStyle::CE_RubberBand`，让临时选择框符合平台视觉。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `shape` | `QRubberBand::Line` 或 `QRubberBand::Rectangle`。 |
| `opaque` | 是否按不透明方式绘制。 |
| `rect` | 绘制区域。 |
| `QStyle::CE_RubberBand` | 绘制 rubber band 的 control。 |
| `QRubberBand` | 使用该 option 的控件。 |

## 4. 关键用法

```cpp
QStyleOptionRubberBand opt;
opt.initFrom(this);
opt.shape = QRubberBand::Rectangle;
opt.opaque = false;

QStylePainter p(this);
p.drawControl(QStyle::CE_RubberBand, opt);
```

## 5. 使用场景

适合自定义 rubber band、框选控件、截图范围选择、拖放位置提示。

普通框选直接用 `QRubberBand` 即可，不需要手动构造 option。

## 6. 常见坑与经验

橡皮筋是临时反馈，不应该承载最终选择状态。释放鼠标后要把结果同步到真正模型。

矩形和线条的视觉语义不同：矩形表示范围，线条表示位置。

在深浅主题中保持可见性很重要，优先交给 style 绘制。
