<!-- 依据 Qt 6.11.1 头文件 qgraphicsitem.h 整理。 -->

# QGraphicsLineItem 深入笔记

> 头文件：`#include <QGraphicsLineItem>`  
> 模块：`Qt6::Widgets`  
> 继承：`QGraphicsItem -> QGraphicsLineItem`

## 1. 它解决什么问题

`QGraphicsLineItem` 表示场景中的一条直线段。它用本地 `QLineF` 保存两个端点，并用 `QPen` 定义颜色、宽度、虚线、端点和连接风格。

它适合：

- 流程图、节点图、连线编辑器中的连接线。
- 坐标轴、参考线、标尺刻度、十字准星。
- 拖拽中临时显示的连线或测量线。

它不适合：

- 折线、多段连线、贝塞尔曲线：使用 `QGraphicsPathItem`。
- 带箭头、标签、选中控点、避障路由的连线：通常用自定义 `QGraphicsObject`，线段只是其中一层。
- 无限延伸的网格线：按视图可见范围动态绘制或自定义 item，避免创建过多线段。

## 2. `line()` 与 `setPos()` 的职责

```cpp
auto *edge = new QGraphicsLineItem(0, 0, 120, 0);
edge->setPos(200, 80);
```

- `line()`：两个端点在**图元本地坐标系**中的位置。
- `setPos()`：整条线所在的父图元/scene 坐标位置。

连线编辑器中，若线的起点与终点本来就来自 scene 坐标，可直接把它们映射到 item 本地坐标，或让 item 固定在 `(0, 0)`。更常见、也更清楚的方式是把 item 原点放在起点：

```cpp
const QPointF start = sourceNode->scenePos();
const QPointF end = targetNode->scenePos();

edge->setPos(start);
edge->setLine(QLineF(QPointF(0, 0), end - start));
```

这样旋转、缩放、选择控点和子图元都围绕连接起点建立，维护起来比把所有 scene 坐标塞进 `setLine()` 更稳定。

## 3. 默认 pen 与缩放：最容易误判的地方

`QGraphicsLineItem` 的默认 pen 是黑色、宽度 `0` 的 pen。零宽 pen 是 cosmetic pen，会以 **1 个设备像素**绘制，不随 view 变换而变粗或变细。

```cpp
edge->setPen(QPen(Qt::black, 0)); // 1 设备像素，适合辅助线
edge->setPen(QPen(Qt::black, 2)); // 普通几何宽度，随 scene/view 缩放
```

选择策略时要有意识：

| 需求 | 合适 pen |
| --- | --- |
| 无论缩放都保持细、清晰的参考线 | 宽度 `0` 的 cosmetic pen |
| 线宽是场景几何的一部分，例如道路、流程边、测量结果 | 非零宽普通 pen |

非零宽 cosmetic pen 不受 `QGraphicsItem` 支持。不要用 `pen.setCosmetic(true)` 再设置大宽度来试图得到“始终 4 像素”的场景线；这种需求应放在视图前景绘制、忽略变换的专用 item，或重新设计交互层。

## 4. 命中区域不是数学上的一维线

线段没有面积，若按几何中心线做 hit test，用户几乎点不中。`QGraphicsLineItem::shape()` 会根据 pen 生成具有宽度的路径，`contains()` 也据此工作。

```cpp
edge->setPen(QPen(Qt::darkBlue, 8));
const bool hit = edge->contains(edge->mapFromScene(scenePoint));
```

这有一个交互设计问题：显示线宽和可点击线宽常常不应相同。若视觉上只想画 1 像素线，却希望用户容易点击，直接把 pen 加粗会改变画面。更合适的方式是：

- 为线创建一条透明、较粗的独立命中 item。
- 使用自定义图元，`paint()` 画细线、`shape()` 返回更宽的 stroker 路径。

`boundingRect()` 同样会纳入 pen 宽度，供 scene 做重绘和索引；不要以 `line().boundingRect()` 代替它。

## 5. 更新端点和样式

```cpp
edge->setLine(QLineF(source, target));

QPen pen(QColor("#4f77a0"));
pen.setWidthF(2.0);
pen.setStyle(Qt::DashLine);
pen.setCapStyle(Qt::RoundCap);
edge->setPen(pen);
```

`setLine()` 改变本地几何，`setPen()` 改变视觉和有效命中宽度。两者都会影响场景的重绘和索引范围，使用 setter 即可；不要在业务代码直接调用 `paint()` 或手动改 `boundingRect()`。

`QLineF` 是值类型，`line()` 返回副本。若要调整端点，需要修改副本再回写：

```cpp
QLineF current = edge->line();
current.setP2(newEnd);
edge->setLine(current);
```

## 6. 遮挡和类型

`opaqueArea()` 与 `isObscuredBy()` 面向 scene 的遮挡优化，通常不用于业务碰撞判断。线条只有在 pen 和绘制结果足以形成不透明区域时才可能参与这类优化；不要将它们当成“线段相交”API。

`type()` 返回 `QGraphicsLineItem::Type`，值为 `6`。在异构图元集合中可先比较 `type()`，再安全地转换为 `QGraphicsLineItem *`。

受保护的 `supportsExtension()`、`setExtension()`、`extension()` 是 QGraphicsItem 框架扩展协议，标准直线项为兼容性重写；普通应用不应直接调用。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型常量 | `QGraphicsLineItem::Type = 6` | 标识直线图元的运行时类型。 | 先通过 `type()` 确认，再 `static_cast`。 |
| 构造 | `explicit QGraphicsLineItem(QGraphicsItem *parent = nullptr)` | 创建空直线图元。 | 后续用 `setLine()` 设置端点。 |
| 构造 | `explicit QGraphicsLineItem(const QLineF &line, QGraphicsItem *parent = nullptr)` | 用一条本地线段创建图元。 | 端点属于 item 本地坐标。 |
| 构造 | `explicit QGraphicsLineItem(qreal x1, qreal y1, qreal x2, qreal y2, QGraphicsItem *parent = nullptr)` | 用两个本地端点创建图元。 | scene 位置应通过 `setPos()` 管理。 |
| 析构 | `~QGraphicsLineItem()` | 销毁直线图元。 | 由 scene 或图元父子树统一管理。 |
| 线段读取 | `QLineF line() const` | 返回当前本地线段。 | 返回副本，修改后要 `setLine()` 回写。 |
| 线段设置 | `void setLine(const QLineF &line)` | 设置本地线段。 | 改端点，不等于移动整条线。 |
| 线段设置 | `void setLine(qreal x1, qreal y1, qreal x2, qreal y2)` | 用端点数值设置本地线段。 | 是 `QLineF` setter 的便捷重载。 |
| 画笔读取 | `QPen pen() const` | 返回当前画笔。 | 默认是宽度 `0` 的黑色 cosmetic pen。 |
| 画笔设置 | `void setPen(const QPen &pen)` | 设置颜色、宽度、线型与端点风格。 | 普通非零宽 pen 随缩放变化；非零 cosmetic pen 不受支持。 |
| 绘制边界 | `QRectF boundingRect() const` | 返回 scene 索引与重绘范围。 | 计入 pen 宽度，别用数学线段外接矩形替代。 |
| 命中 | `QPainterPath shape() const` | 返回按 pen 加宽后的命中路径。 | 用于碰撞和点击；视觉宽与点击宽可分离设计。 |
| 命中 | `bool contains(const QPointF &point) const` | 判断本地点是否命中线段区域。 | scene 坐标须先 `mapFromScene()`。 |
| 绘制 | `void paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget = nullptr)` | 按当前 pen 绘制线段。 | 由 Graphics View 调用，业务代码不直接调用。 |
| 遮挡优化 | `bool isObscuredBy(const QGraphicsItem *item) const` | 判断其它 item 是否遮住本线段。 | 不是线段相交 API。 |
| 遮挡优化 | `QPainterPath opaqueArea() const` | 返回完全不透明区域。 | 用于绘制优化，不用于点击。 |
| 类型查询 | `int type() const` | 返回 `QGraphicsLineItem::Type`。 | 用于异构图元集合的类型分派。 |
| 受保护扩展 | `bool supportsExtension(Extension extension) const` | 查询是否支持指定图元扩展。 | Qt 框架协议，普通应用不调用。 |
| 受保护扩展 | `void setExtension(Extension extension, const QVariant &variant)` | 写入扩展数据。 | 仅自定义图元框架扩展实现时使用。 |
| 受保护扩展 | `QVariant extension(const QVariant &variant) const` | 读取扩展数据。 | 参数与返回语义由具体扩展定义。 |

## 8. 排查清单

1. 放大后辅助线变粗/变细异常：检查是否应使用宽度 `0` 的 cosmetic pen。
2. 用户很难点中细线：显示宽度和命中宽度分离，别只靠 `contains()` 的默认细 pen。
3. 连线跟随节点时漂移：统一 scene 坐标与 item 本地坐标；常用“`pos = start`、line 从 `(0,0)` 指向 `end-start`”。
4. 更新了 `QLineF` 却没生效：`line()` 返回副本，需 `setLine()` 回写。
5. 想判断两条边相交：使用 `QLineF::intersects()`，不要使用 `isObscuredBy()`。

### 一句话总结

`QGraphicsLineItem` 用本地 `QLineF` 表示直线、用 `QPen` 定义视觉和命中厚度；最重要的选择是区分零宽 cosmetic 辅助线与随场景缩放的几何线，并为细线单独设计足够宽的交互命中区域。
