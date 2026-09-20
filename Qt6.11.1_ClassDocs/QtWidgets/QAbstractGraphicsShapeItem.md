# QAbstractGraphicsShapeItem

> Qt 6.11.1 · Qt Widgets · 来自 `QAbstractGraphicsShapeItem`

## 1. 先建立直觉

`QAbstractGraphicsShapeItem` 是带画笔和画刷的图形 item 基类。矩形、椭圆、路径、多边形、简单文本这些“可用边线和填充来绘制”的 item 都从它继承。

它不是给你直接创建的常用图元，而是提供共同能力：`pen` 决定轮廓，`brush` 决定填充。真正的几何形状由具体子类决定。

## 2. 类说明

`QAbstractGraphicsShapeItem` 继承自 `QGraphicsItem`。它把 `QPen`、`QBrush` 管理从具体 shape item 中抽出来，并实现了与不透明区域相关的通用行为。

自定义 shape item 时，如果你的对象也符合“一个形状 + 轮廓 + 填充”的模式，继承它比直接继承 `QGraphicsItem` 少写不少基础代码。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `setPen(const QPen &)` / `pen()` | 设置或读取轮廓线。线宽会影响 `boundingRect()` 和命中区域。 |
| `setBrush(const QBrush &)` / `brush()` | 设置或读取填充。无填充可用 `Qt::NoBrush`。 |
| `isObscuredBy(const QGraphicsItem *)` | 判断当前图元是否被其他 item 遮挡。 |
| `opaqueArea()` | 返回不透明区域，帮助视图优化绘制。 |
| `QGraphicsRectItem` | 矩形具体实现。 |
| `QGraphicsEllipseItem` | 椭圆/扇形具体实现。 |
| `QGraphicsPathItem` | 任意 painter path 具体实现。 |
| `QGraphicsPolygonItem` | 多边形具体实现。 |
| `QGraphicsSimpleTextItem` | 简单文本具体实现。 |

## 4. 关键用法

```cpp
auto *rect = scene->addRect(QRectF(0, 0, 120, 60));
rect->setPen(QPen(Qt::darkBlue, 2));
rect->setBrush(QColor("#d8ecff"));
```

自定义 shape item 时，仍然要实现几何和绘制：

```cpp
class ShapeItem : public QAbstractGraphicsShapeItem {
public:
    QRectF boundingRect() const override;
    void paint(QPainter *, const QStyleOptionGraphicsItem *, QWidget *) override;
};
```

## 5. 使用场景

适合需要统一轮廓/填充配置的图元：流程图节点、标注框、状态区域、装饰形状、可选中几何对象。

如果 item 完全是图片、复杂控件或自定义 GPU 内容，这个基类的 pen/brush 模型可能不合适，直接继承 `QGraphicsItem` 或其他专用类更好。

## 6. 常见坑与经验

线宽会改变真实占用区域。自定义子类计算 `boundingRect()` 时要把 pen 宽度考虑进去，否则边线可能被裁剪。

`brush()` 是填充，不是背景。空心图形应显式用 `Qt::NoBrush`，不要靠透明颜色混过去。

继承这个类不免除 `prepareGeometryChange()` 的规则。形状边界变化前仍然要通知场景。
