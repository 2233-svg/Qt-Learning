# QGraphicsDropShadowEffect

> Qt 6.11.1 · Qt Widgets · 来自 `QGraphicsDropShadowEffect`

## 1. 先建立直觉

`QGraphicsDropShadowEffect` 给目标绘制结果加投影。它常用于让浮层、卡片、弹窗、场景节点看起来离背景更近或更高。

投影是视觉效果，不改变目标真实几何和点击区域。阴影看起来超出控件边界，但鼠标命中仍按原对象及其 item/widget 规则来。

## 2. 类说明

`QGraphicsDropShadowEffect` 继承自 `QGraphicsEffect`。核心属性是 `blurRadius`、`color`、`offset`。模糊半径决定阴影柔和程度，偏移决定阴影相对源对象的位置。

它会扩大有效绘制边界，因此 `boundingRectFor()` 会比源对象更大。若父控件或视图裁剪严格，阴影可能被切掉。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QGraphicsDropShadowEffect(QObject *)` | 创建投影效果。 |
| `setBlurRadius(qreal)` / `blurRadius()` | 设置或读取阴影模糊半径。 |
| `setColor(const QColor &)` / `color()` | 设置或读取阴影颜色。 |
| `setOffset(QPointF)` / `offset()` | 设置或读取阴影偏移。 |
| `setOffset(qreal dx, qreal dy)` | 坐标参数版本。 |
| `setXOffset(qreal)` / `xOffset()` | 单独设置或读取水平偏移。 |
| `setYOffset(qreal)` / `yOffset()` | 单独设置或读取垂直偏移。 |
| `boundingRectFor(QRectF)` | 返回包含阴影扩展后的边界。 |
| `blurRadiusChanged(qreal)` | 模糊半径变化时发出。 |
| `colorChanged(QColor)` | 阴影颜色变化时发出。 |
| `offsetChanged(QPointF)` | 偏移变化时发出。 |

## 4. 关键用法

```cpp
auto *shadow = new QGraphicsDropShadowEffect(panel);
shadow->setBlurRadius(24);
shadow->setOffset(0, 6);
shadow->setColor(QColor(0, 0, 0, 90));
panel->setGraphicsEffect(shadow);
```

在 graphics item 上同样适用：

```cpp
item->setGraphicsEffect(shadow);
```

## 5. 使用场景

适合弹窗、悬浮工具条、被选中节点、拖拽预览、卡片、上下文菜单式面板、画布中的浮动注释。

不适合给大量列表项或海量图元全部加阴影。那会产生大量离屏绘制和模糊计算。

## 6. 常见坑与经验

阴影被裁剪时，不一定是效果错了，可能是父控件、viewport 或 item 边界裁剪。需要给周围留空间或调整绘制结构。

偏移是屏幕视觉上的偏移，不是光照模型。统一应用里所有阴影方向，比每个控件随意设置更显专业。

透明阴影颜色通常比纯黑更自然。高 alpha 大阴影会让界面显脏。
