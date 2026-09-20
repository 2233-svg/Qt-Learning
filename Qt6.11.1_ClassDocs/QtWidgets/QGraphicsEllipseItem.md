# QGraphicsEllipseItem

> Qt 6.11.1 · Qt Widgets · 来自 `QGraphicsEllipseItem`

## 1. 先建立直觉

`QGraphicsEllipseItem` 是场景中的椭圆图元。它可以画完整圆/椭圆，也可以通过起始角和跨度角画弧形或扇形。

它的几何基础仍然是一个局部 `QRectF`：椭圆被内切在这个矩形里。移动图元用 `setPos()`，改变椭圆大小用 `setRect()`。

## 2. 类说明

`QGraphicsEllipseItem` 继承自 `QAbstractGraphicsShapeItem`，所以用 `pen` 画边，用 `brush` 填充。`startAngle` 和 `spanAngle` 采用 Qt 绘图系统的角度单位：一度的 1/16。

完整椭圆常用于节点、端口、控制点；弧段和扇形适合仪表、占比、范围标记。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QGraphicsEllipseItem(parent)` | 创建空椭圆图元。 |
| `QGraphicsEllipseItem(QRectF, parent)` | 创建指定外接矩形的椭圆。 |
| `setRect(const QRectF &)` / `rect()` | 设置或读取椭圆外接矩形。 |
| `setStartAngle(int)` / `startAngle()` | 设置或读取起始角，单位是 1/16 度。 |
| `setSpanAngle(int)` / `spanAngle()` | 设置或读取跨度角，单位是 1/16 度。 |
| `setPen()` / `setBrush()` | 设置边线和填充。 |
| `boundingRect()` | 返回包含边线的外接区域。 |
| `shape()` | 返回用于命中/碰撞的真实形状。 |
| `contains()` | 判断点是否在椭圆或扇形内。 |
| `paint()` | 绘制椭圆/弧段/扇形。 |
| `type()` | 返回 item 类型。 |

## 4. 关键用法

```cpp
auto *dot = scene->addEllipse(QRectF(-6, -6, 12, 12),
                              QPen(Qt::darkGreen),
                              QBrush(Qt::green));
dot->setPos(portPosition);
```

绘制 90 度扇形：

```cpp
auto *pie = new QGraphicsEllipseItem(QRectF(-40, -40, 80, 80));
pie->setStartAngle(0 * 16);
pie->setSpanAngle(90 * 16);
scene->addItem(pie);
```

## 5. 使用场景

适合端口、节点、控制点、选择手柄、状态灯、圆形按钮视觉、简单仪表弧线、占比扇形、地图点位。

如果需要复杂曲线、圆角组合或不规则区域，`QGraphicsPathItem` 更灵活。

## 6. 常见坑与经验

角度单位不是度，而是 1/16 度。写 `90` 只会得到 5.625 度，常见正确写法是 `90 * 16`。

`rect()` 是外接矩形，不是场景位置。移动用 `setPos()`，否则局部坐标会变得难以维护。

非常小的椭圆在缩放后命中可能不舒服。交互控制点可以用更大的 `shape()` 或自定义 item 增加点击热区。
