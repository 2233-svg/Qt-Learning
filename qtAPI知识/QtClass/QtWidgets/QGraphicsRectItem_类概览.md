<!-- 依据 Qt 6.11.1 头文件 qgraphicsitem.h 整理。 -->

# QGraphicsRectItem 深入笔记

> 头文件：`#include <QGraphicsRectItem>`  
> 模块：`Qt6::Widgets`  
> 继承：`QGraphicsItem -> QAbstractGraphicsShapeItem -> QGraphicsRectItem`

## 1. 它解决什么问题

`QGraphicsRectItem` 是 Graphics View 中最直接的矩形图元。它用一个本地 `QRectF` 定义矩形轮廓，再继承 `QAbstractGraphicsShapeItem` 的 pen/brush 来绘制边框和填充。

它适合：

- 场景中的卡片背景、分组边框、选择区域。
- 流程图或节点图中的矩形节点。
- 编辑器中的拖拽框、对齐参考块、可点击热区。
- 快速验证坐标、层叠、选择和 scene 索引行为。

它不适合：

- 带圆角、阴影、文本、复杂交互状态的完整组件：通常使用自定义 `QGraphicsObject` 或由多个图元组合。
- 需要任意路径轮廓：使用 `QGraphicsPathItem`。
- 需要位图像素内容：使用 `QGraphicsPixmapItem`。

## 2. `rect()` 和 `setPos()` 管的不是同一件事

这是最容易写错的地方：

```cpp
auto *item = new QGraphicsRectItem(0, 0, 120, 48);
item->setPos(300, 160);
```

- `rect()`：矩形在**图元本地坐标系**中的几何。
- `pos()` / `setPos()`：图元原点在父图元或 scene 坐标系中的位置。

因此，移动整个矩形应该用 `setPos()`；改矩形自身宽高、局部起点才使用 `setRect()`。把场景位置直接塞进 `setRect(300, 160, ...)` 虽然看似能画到目标位置，却会让图元的本地 geometry、变换原点和子图元关系变得难以维护。

```text
rect():  局部轮廓             (0, 0, 120, 48)
pos():   图元放置位置          (300, 160)
scene 中最终位置：             (300, 160) 起的矩形
```

## 3. 创建和样式设置

```cpp
#include <QGraphicsRectItem>

auto *card = new QGraphicsRectItem(QRectF(0, 0, 160, 72));
card->setPen(QPen(QColor("#55708a"), 2.0));
card->setBrush(QColor("#eef7ff"));
card->setPos(40, 30);
card->setFlag(QGraphicsItem::ItemIsSelectable);
card->setFlag(QGraphicsItem::ItemIsMovable);
scene->addItem(card);
```

构造器有三种：

- 空构造：先创建，再用 `setRect()` 给几何。
- `QRectF` 构造：已有矩形对象时最清楚。
- `x, y, width, height` 构造：写固定数值时简短。

图元加入 `QGraphicsScene` 后，scene 会参与管理；若它有父图元，父图元析构会删除它。不要在 scene/父图元仍拥有图元时又交给其它智能指针重复管理。

## 4. 负宽高不是“反向拖拽”

`QGraphicsRectItem` 对负宽或负高的 `QRectF` 没有定义绘制行为。鼠标从右下往左上拖出选择框时，常会产生负尺寸，必须归一化：

```cpp
QRectF dragRect(startPoint, currentPoint);
selectionItem->setRect(dragRect.normalized());
```

不要依赖“本机上似乎还能画出来”的行为。归一化后，左上角总是较小坐标，宽高为非负值，也更符合后续 `contains()`、`boundingRect()` 和 scene 查询的预期。

## 5. pen 会让可见边界变大

`rect()` 是几何矩形，但 `boundingRect()` 是 scene 用来做索引和重绘判断的保守边界。粗 pen 绘制在矩形边缘附近，`boundingRect()` 会把相关笔宽纳入范围。

```cpp
card->setRect(0, 0, 100, 40);
card->setPen(QPen(Qt::black, 12));
```

此时不要假设 `boundingRect() == rect()`。同样地：

- `shape()` 返回更适合命中测试和碰撞检测的路径。
- `contains(point)` 判断一个**本地坐标**点是否落入有效形状。
- `opaqueArea()`、`isObscuredBy()` 服务于遮挡和绘制优化，不是应用层的碰撞算法。

需要判断场景坐标点时先转换：

```cpp
const QPointF localPoint = card->mapFromScene(scenePoint);
const bool hit = card->contains(localPoint);
```

## 6. `paint()` 不是你平常要调用的函数

`paint(QPainter *, ...)` 是 Graphics View 绘制阶段的虚函数。标准 `QGraphicsRectItem` 已实现它，会按当前 pen、brush 和 style option 绘制矩形。

正常项目改外观应调用 `setRect()`、`setPen()`、`setBrush()`，然后让 scene 自动安排重绘。不要在业务代码里直接调用 `paint()`；那会绕过场景的坐标、裁剪、缓存与更新流程。

若想改变矩形画法，例如圆角、状态图标、悬停纹理，通常从 `QGraphicsObject` 或 `QGraphicsItem` 编写自己的 `paint()` 更合适。不要修改标准类的内部扩展接口。

## 7. 类型识别和扩展接口

`type()` 返回 `QGraphicsRectItem::Type`，其值为 `3`。在一组 `QGraphicsItem *` 中需要区分运行时类型时可用：

```cpp
if (item->type() == QGraphicsRectItem::Type) {
    auto *rectItem = static_cast<QGraphicsRectItem *>(item);
    // 仅在 type 已确认后使用 static_cast。
}
```

`supportsExtension()`、`setExtension()`、`extension()` 是 QGraphicsItem 的受保护扩展协议，标准矩形项为框架兼容性重写。普通应用不应调用或依赖它们；若自己的派生图元需要支持某种框架扩展，才研究这组 API。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型常量 | `QGraphicsRectItem::Type = 3` | 标识矩形图元的运行时类型。 | 与 `type()` 配合后才能安全 `static_cast`。 |
| 构造 | `explicit QGraphicsRectItem(QGraphicsItem *parent = nullptr)` | 创建尚未设定矩形的图元。 | 后续必须用 `setRect()` 设置有效几何。 |
| 构造 | `explicit QGraphicsRectItem(const QRectF &rect, QGraphicsItem *parent = nullptr)` | 用 `QRectF` 创建矩形图元。 | 传入前确保 `rect.normalized()`，避免负宽高。 |
| 构造 | `explicit QGraphicsRectItem(qreal x, qreal y, qreal w, qreal h, QGraphicsItem *parent = nullptr)` | 用局部坐标和尺寸创建矩形。 | `x/y` 是本地起点，不是 scene 位置。 |
| 析构 | `~QGraphicsRectItem()` | 销毁矩形图元。 | 由父图元或 scene 逻辑统一处理所有权。 |
| 几何 | `QRectF rect() const` | 返回矩形的本地几何。 | 不等于 `pos()`，也不一定等于 `boundingRect()`。 |
| 几何 | `void setRect(const QRectF &rect)` | 设置本地矩形几何。 | 负宽高前先 `normalized()`；移动整体用 `setPos()`。 |
| 几何 | `void setRect(qreal x, qreal y, qreal w, qreal h)` | 用数值设置本地矩形几何。 | 是 `QRectF` setter 的便捷重载。 |
| 绘制边界 | `QRectF boundingRect() const` | 返回用于 scene 索引和重绘的外接范围。 | 粗 pen 会使结果大于 `rect()`。 |
| 命中 | `QPainterPath shape() const` | 返回精确形状路径。 | 用于碰撞和点击；坐标是图元本地坐标。 |
| 命中 | `bool contains(const QPointF &point) const` | 判断本地点是否在有效形状内。 | scene 点须先 `mapFromScene()`。 |
| 绘制 | `void paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget = nullptr)` | 按 pen/brush 绘制矩形。 | 由 Graphics View 调用，业务代码不要直接调用。 |
| 遮挡优化 | `bool isObscuredBy(const QGraphicsItem *item) const` | 判断其它图元是否遮住本矩形。 | 服务于绘制优化，不等同于相交检测。 |
| 遮挡优化 | `QPainterPath opaqueArea() const` | 返回确定不透明的区域。 | 不是鼠标命中 API。 |
| 类型查询 | `int type() const` | 返回 `QGraphicsRectItem::Type`。 | 用于异构 item 容器中的类型分派。 |
| 受保护扩展 | `bool supportsExtension(Extension extension) const` | 查询是否支持指定 QGraphicsItem 扩展。 | 框架协议；普通应用不直接使用。 |
| 受保护扩展 | `void setExtension(Extension extension, const QVariant &variant)` | 写入指定扩展数据。 | 仅自定义图元实现框架扩展时使用。 |
| 受保护扩展 | `QVariant extension(const QVariant &variant) const` | 读取扩展数据。 | 参数/返回约定由具体扩展决定。 |

## 9. 排查清单

1. 矩形位置不对：确认是 `setPos()` 还是 `setRect()` 的职责用反了。
2. 拖拽选择框不显示或错乱：把拖拽产生的 `QRectF` 调用 `normalized()`。
3. 粗边被裁掉或场景查询不完整：用 `boundingRect()` 理解有效范围，别只看 `rect()`。
4. scene 点判断命中失败：先从 scene 坐标映射到 item 本地坐标。
5. 想要圆角矩形：不要滥用 `setRect()`；改用自定义 `paint()` 或专用路径图元。

### 一句话总结

`QGraphicsRectItem` 用本地 `rect` 描述矩形，用 `pos` 把矩形放进场景；安全使用的关键是归一化拖拽矩形、理解 pen 扩大的有效边界，并把命中测试放在本地坐标系中处理。
