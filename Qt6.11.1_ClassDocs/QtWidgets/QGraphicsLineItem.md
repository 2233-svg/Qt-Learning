# QGraphicsLineItem

> Qt 6.11.1 · Qt Widgets · 来自 `QGraphicsLineItem`

## 1. 先建立直觉

`QGraphicsLineItem` 是场景中的直线段图元。它用一个 `QLineF` 描述起点和终点，用 `QPen` 描述颜色、宽度、虚线、端点和连接样式。

它适合画简单连接线、参考线、测量线、坐标轴、分隔线。复杂折线、曲线、箭头、可编辑路径通常更适合 `QGraphicsPathItem` 或自定义 item。

## 2. 类说明

`QGraphicsLineItem` 继承自 `QGraphicsItem`。它没有 brush，因为线没有填充区域。它的 `shape()` 会考虑 pen 宽度，所以粗线和细线的命中区域不同。

和其他 item 一样，`line()` 是局部坐标中的线段；item 的场景位置、旋转、缩放仍由 `QGraphicsItem` 的变换系统控制。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QGraphicsLineItem(parent)` | 创建空线段图元。 |
| `QGraphicsLineItem(QLineF, parent)` | 创建指定线段。 |
| `QGraphicsLineItem(x1, y1, x2, y2, parent)` | 用坐标创建线段。 |
| `setLine(const QLineF &)` / `line()` | 设置或读取局部坐标中的线段。 |
| `setLine(x1, y1, x2, y2)` | 坐标参数版本。 |
| `setPen(const QPen &)` / `pen()` | 设置或读取线条样式。 |
| `boundingRect()` | 返回包含 pen 宽度的外接区域。 |
| `shape()` | 返回用于命中和碰撞的线条轮廓。 |
| `contains()` | 判断点是否命中线条。 |
| `paint()` | 绘制线条。 |
| `type()` | 返回 item 类型。 |

## 4. 关键用法

```cpp
auto *line = scene->addLine(QLineF(0, 0, 120, 40),
                            QPen(Qt::darkGray, 2, Qt::DashLine));
line->setFlag(QGraphicsItem::ItemIsSelectable);
```

连接两个 item 时，通常把端点换算到共同坐标系：

```cpp
const QPointF a = source->scenePos();
const QPointF b = target->scenePos();
line->setLine(QLineF(line->mapFromScene(a), line->mapFromScene(b)));
```

## 5. 使用场景

适合简单连线、参考线、标尺、坐标轴、流程图初版连接、拖拽预览线、调试碰撞边界。

如果线需要箭头、可点击热区明显大于可见线宽、自动绕障碍、端点吸附或多段路径，建议自定义 item 或使用 `QGraphicsPathItem`。

## 6. 常见坑与经验

细线很难点击。可以把可见 pen 保持 1 像素，但自定义 `shape()` 扩大命中区域，用户体验会好很多。

不要在大量连线中每帧重建 item。更新已有 `QGraphicsLineItem::setLine()` 通常更便宜。

线段端点的坐标属于 item 局部坐标。父子 item 或 scene 坐标混用时，先明确映射方向。
