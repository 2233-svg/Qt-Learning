# QGraphicsItem

> Qt 6.11.1 · Qt Widgets · 来自 `QGraphicsItem`

## 1. 先建立直觉

`QGraphicsItem` 是 Graphics View 场景里的基础图元。场景中的矩形、线、图片、文本、节点、端口、连线、控制柄，本质上都可以是 item。

它不是 `QWidget`，没有 QObject 的信号槽，也不参与 widget layout。它生活在 `QGraphicsScene` 的坐标世界里，由 `QGraphicsView` 显示；它的核心职责是：告诉 Qt 自己占多大、怎么画、怎样响应事件。

## 2. 类说明

自定义 item 最少要实现两个函数：`boundingRect()` 和 `paint()`。`boundingRect()` 必须准确包含绘制区域，Qt 用它做重绘裁剪、命中、索引和更新；`paint()` 负责实际绘制。

复杂 item 还会实现 `shape()` 做精确命中，设置 flags 支持选择/移动/焦点，重写鼠标键盘事件处理交互，使用父子 item 组合成节点、标签、端口等结构。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `boundingRect()` | 必须实现，返回 item 绘制和重绘的外接矩形。 |
| `paint(QPainter *, QStyleOptionGraphicsItem *, QWidget *)` | 必须实现，绘制 item。 |
| `shape()` | 返回精确形状，用于命中和碰撞，默认基于 bounding rect。 |
| `contains()` | 判断点是否在 item 内。 |
| `setPos()` / `pos()` | 设置或读取父坐标系中的位置。 |
| `scenePos()` | 读取场景坐标位置。 |
| `setRotation()` / `setScale()` / `setTransform()` | 设置旋转、缩放或完整变换。 |
| `mapToScene()` / `mapFromScene()` | 在 item、父 item、scene 坐标之间转换。 |
| `setParentItem()` / `parentItem()` | 建立 item 层级关系。 |
| `childItems()` | 返回子 item。 |
| `setZValue()` / `zValue()` | 控制叠放顺序。 |
| `setFlags()` / `setFlag()` | 启用可移动、可选择、可聚焦等行为。 |
| `setSelected()` / `isSelected()` | 设置或读取选中状态。 |
| `setVisible()` / `isVisible()` | 控制可见性。 |
| `update()` | 请求重绘 item 区域。 |
| `prepareGeometryChange()` | 在改变 `boundingRect()` 前必须调用。 |
| `collidesWithItem()` / `collidingItems()` | 做碰撞检测。 |
| `itemChange()` | 监听位置、选择、父子、场景等状态变化。 |

## 4. 关键用法

```cpp
class NodeItem : public QGraphicsItem {
public:
    QRectF boundingRect() const override
    {
        return QRectF(-60, -30, 120, 60);
    }

    void paint(QPainter *p, const QStyleOptionGraphicsItem *, QWidget *) override
    {
        p->setBrush(isSelected() ? QColor("#ffd66b") : QColor("#f4f4f4"));
        p->drawRoundedRect(boundingRect(), 6, 6);
    }
};
```

让 item 可拖拽和可选择：

```cpp
item->setFlags(QGraphicsItem::ItemIsMovable |
               QGraphicsItem::ItemIsSelectable |
               QGraphicsItem::ItemSendsGeometryChanges);
```

改变影响边界的尺寸前：

```cpp
prepareGeometryChange();
width = newWidth;
update();
```

## 5. 使用场景

适合自定义节点、连线、图标、控制点、标注框、流程图块、游戏编辑器元素、地图要素、测量标记、交互式图形对象。

如果图形对象需要信号槽、属性系统或动画属性，考虑继承 `QGraphicsObject`；如果要嵌入真正的 QWidget，看 `QGraphicsProxyWidget`，但不要滥用。

## 6. 常见坑与经验

`boundingRect()` 不能随便写大。过大导致重绘区域大、命中不准、性能差；过小会绘制残影或裁剪掉边缘。

改变几何边界前必须调用 `prepareGeometryChange()`。这是 Graphics View 新手最常踩的坑。

item 坐标默认以自身原点为中心或左上取决于你怎么设计。统一约定很重要，尤其是连线和端口需要频繁坐标映射时。
