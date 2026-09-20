# QGraphicsRectItem

> Qt 6.11.1 · Qt Widgets · 来自 `QGraphicsRectItem`

## 1. 先建立直觉

`QGraphicsRectItem` 是场景中的矩形图元。它适合画框、节点背景、选择区域、碰撞盒、可拖拽块等最基础的几何对象。

矩形的 `rect()` 是 item 自身坐标系里的形状，不等于 item 在场景中的位置。要移动它用 `setPos()`；要改变它内部矩形大小或局部坐标范围用 `setRect()`。

## 2. 类说明

`QGraphicsRectItem` 继承自 `QAbstractGraphicsShapeItem`，因此拥有 `pen` 和 `brush`。Qt 会根据矩形、画笔宽度和填充计算 `boundingRect()`、`shape()`、绘制与命中。

它是快速搭建图形界面的好材料，但如果节点要显示多段文本、端口和状态徽标，通常会把 rect item 作为背景，外面再组合其他 child items，或者写一个自定义 item。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QGraphicsRectItem(parent)` | 创建空矩形图元。 |
| `QGraphicsRectItem(QRectF, parent)` | 创建指定局部矩形的图元。 |
| `QGraphicsRectItem(x, y, w, h, parent)` | 用坐标和尺寸创建矩形。 |
| `setRect(const QRectF &)` / `rect()` | 设置或读取 item 局部坐标中的矩形。 |
| `setRect(x, y, w, h)` | 坐标参数版本。 |
| `setPen()` / `pen()` | 继承自 `QAbstractGraphicsShapeItem`，控制边框。 |
| `setBrush()` / `brush()` | 控制填充。 |
| `boundingRect()` | 返回含边框宽度的外接区域。 |
| `shape()` | 返回用于精确命中/碰撞的路径。 |
| `contains()` | 判断局部点是否命中矩形。 |
| `paint()` | 绘制矩形。 |
| `type()` | 返回 item 类型，便于 `qgraphicsitem_cast`。 |

## 4. 关键用法

```cpp
auto *rect = scene->addRect(QRectF(-50, -25, 100, 50),
                            QPen(Qt::black, 2),
                            QBrush(QColor("#e8f3ff")));
rect->setPos(200, 120);
rect->setFlag(QGraphicsItem::ItemIsMovable);
rect->setFlag(QGraphicsItem::ItemIsSelectable);
```

把矩形以原点为中心很适合节点和控制点；以左上角为 `(0, 0)` 则更像传统 UI 布局。一个项目里最好统一约定。

## 5. 使用场景

适合流程图节点背景、选区框、网格单元、图纸区域、拖拽占位、碰撞区域可视化、简单卡片形状。

如果需要圆角，`QGraphicsRectItem` 本身不提供圆角属性。可以继承自定义绘制，或使用 `QGraphicsPathItem` 绘制 rounded rect path。

## 6. 常见坑与经验

不要用 `setRect()` 移动 item，除非你确实要改变局部坐标。移动 item 应使用 `setPos()`。

修改 rect 会改变几何边界。Qt 的内置实现会处理；自定义类似类时要记住 `prepareGeometryChange()`。

pen 宽度会让实际绘制超出 `rect()` 本身，命中和 bounding rect 通常会把这部分纳入。
