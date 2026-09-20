# QGraphicsPolygonItem

> Qt 6.11.1 · Qt Widgets · 来自 `QGraphicsPolygonItem`

## 1. 先建立直觉

`QGraphicsPolygonItem` 是场景中的多边形图元。它用 `QPolygonF` 保存一组顶点，再用 `pen` 画边、`brush` 填充内部。

它适合表达规则或不规则平面区域：三角形、箭头、热点区域、地图多边形、可选区块。比 path 简单，比 rect/ellipse 灵活。

## 2. 类说明

`QGraphicsPolygonItem` 继承自 `QAbstractGraphicsShapeItem`。多边形点坐标属于 item 局部坐标系，item 的位置和变换另由 `QGraphicsItem` 控制。

填充时会受 `fillRule()` 影响。自交多边形、带洞区域或复杂轮廓中，`OddEvenFill` 和 `WindingFill` 可能产生不同结果。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QGraphicsPolygonItem(parent)` | 创建空多边形图元。 |
| `QGraphicsPolygonItem(QPolygonF, parent)` | 创建指定顶点集合的多边形。 |
| `setPolygon(const QPolygonF &)` / `polygon()` | 设置或读取局部多边形点集。 |
| `setFillRule(Qt::FillRule)` / `fillRule()` | 设置或读取填充规则。 |
| `setPen()` / `pen()` | 控制边线。 |
| `setBrush()` / `brush()` | 控制填充。 |
| `boundingRect()` | 返回包含边线的外接矩形。 |
| `shape()` | 返回精确命中/碰撞形状。 |
| `contains()` | 判断点是否位于多边形区域。 |
| `paint()` | 绘制多边形。 |
| `type()` | 返回 item 类型。 |

## 4. 关键用法

```cpp
QPolygonF arrow;
arrow << QPointF(0, 0) << QPointF(80, 30)
      << QPointF(0, 60) << QPointF(18, 30);

auto *item = new QGraphicsPolygonItem(arrow);
item->setPen(QPen(Qt::black));
item->setBrush(QColor("#ffe08a"));
scene->addItem(item);
```

处理复杂自交形状时：

```cpp
item->setFillRule(Qt::WindingFill);
```

## 5. 使用场景

适合箭头、区域块、地图边界、流程图决策形状、雷达图片段、交互热区、可编辑顶点的轻量图元。

如果需要曲线、圆角或多个子路径，`QGraphicsPathItem` 更合适；如果只是矩形，`QGraphicsRectItem` 更轻。

## 6. 常见坑与经验

多边形不会自动闭合你的业务语义，但绘制填充时会按闭合轮廓处理。顶点顺序对自交和 winding 填充尤其重要。

顶点修改后索引和重绘都会受影响。频繁编辑顶点时，考虑是否需要自定义 item 优化 `shape()`。

多边形边缘可见但内部无填充时，命中体验可能和用户预期不同。空心区域是否可点，要按业务决定。
