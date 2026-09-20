# QGraphicsPathItem

> Qt 6.11.1 · Qt Widgets · 来自 `QGraphicsPathItem`

## 1. 先建立直觉

`QGraphicsPathItem` 是场景中的任意路径图元。它用 `QPainterPath` 描述几何，可以包含直线、贝塞尔曲线、圆角矩形、闭合区域、复合轮廓。

当矩形、椭圆、多边形不够表达形状时，就轮到它出场。它是做流程图曲线连线、复杂图标、区域标注和自定义形状的常用工具。

## 2. 类说明

`QGraphicsPathItem` 继承自 `QAbstractGraphicsShapeItem`，所以路径可以有 `pen` 和 `brush`。开放路径主要靠 pen 绘制；闭合路径可以填充。

它的命中和碰撞由 path、fill rule、pen 宽度共同决定。路径越复杂，命中和重绘计算成本越高，大量路径图元需要关注性能。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QGraphicsPathItem(parent)` | 创建空路径图元。 |
| `QGraphicsPathItem(QPainterPath, parent)` | 创建指定路径图元。 |
| `setPath(const QPainterPath &)` / `path()` | 设置或读取 item 的局部路径。 |
| `setPen()` / `pen()` | 控制路径轮廓线。 |
| `setBrush()` / `brush()` | 控制闭合区域填充。 |
| `boundingRect()` | 返回包含路径和 pen 的外接区域。 |
| `shape()` | 返回用于精确命中/碰撞的路径形状。 |
| `contains()` | 判断点是否在路径形状内。 |
| `opaqueArea()` | 返回不透明区域，帮助绘制优化。 |
| `paint()` | 绘制路径。 |
| `type()` | 返回 item 类型。 |

## 4. 关键用法

```cpp
QPainterPath path;
path.moveTo(0, 0);
path.cubicTo(60, -40, 120, 40, 180, 0);

auto *edge = new QGraphicsPathItem(path);
edge->setPen(QPen(Qt::darkBlue, 2));
scene->addItem(edge);
```

圆角矩形也可以用 path 表达：

```cpp
QPainterPath bubble;
bubble.addRoundedRect(QRectF(0, 0, 160, 80), 8, 8);
item->setPath(bubble);
```

## 5. 使用场景

适合贝塞尔连线、自由曲线、圆角框、不规则按钮区域、标注云线、复杂图标、地图路径、可填充复杂区域。

如果只是简单直线或矩形，专用 item 更轻、更清楚。路径的灵活性不要变成所有图元都用它的理由。

## 6. 常见坑与经验

开放路径没有自然填充区域，`brush` 对它的效果取决于路径是否形成可填充轮廓。

路径变化会影响几何边界。频繁调用 `setPath()` 的动画场景要注意重绘成本和 scene 索引维护。

复杂连线通常需要扩大命中区域。可见路径可以很细，但用户可点击的 `shape()` 最好更宽。
