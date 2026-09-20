<!-- 依据 Qt 6.11.1 头文件 qgraphicsitem.h 整理。 -->

# QGraphicsPolygonItem 深入笔记

> 头文件：`#include <QGraphicsPolygonItem>`  
> 模块：`Qt6::Widgets`  
> 继承：`QGraphicsItem -> QAbstractGraphicsShapeItem -> QGraphicsPolygonItem`

## 1. 它解决什么问题

`QGraphicsPolygonItem` 用一串顶点构成可描边、可填充的闭合多边形。它适合矩形和椭圆无法准确表达的区域：箭头、菱形节点、六边形、地图区域、编辑器中的任意多边形选区。

```text
QPolygonF 顶点序列
  (x0, y0) -> (x1, y1) -> ... -> (xn, yn)
        ↓ 自动闭合
QGraphicsPolygonItem
  + pen / brush
  + fillRule
```

它的核心难点不是“如何传点”，而是三个边界：

1. `polygon` 的点属于图元本地坐标，而不是 scene 坐标。
2. 自交或嵌套轮廓时，`fillRule` 决定哪些区域算内部。
3. 改顶点会改变几何、命中区域和重绘范围，必须通过 `setPolygon()` 回写。

## 2. 最小使用路径

```cpp
#include <QGraphicsPolygonItem>

QPolygonF diamond;
diamond << QPointF(50, 0)
        << QPointF(100, 50)
        << QPointF(50, 100)
        << QPointF(0, 50);

auto *node = new QGraphicsPolygonItem(diamond);
node->setPen(QPen(QColor("#426d8d"), 2));
node->setBrush(QColor("#e6f3ff"));
node->setPos(200, 120);
scene->addItem(node);
```

`diamond` 描述的是局部菱形，`setPos(200, 120)` 决定它在 scene 中的位置。移动整个图元不要修改每个顶点；用 `setPos()` 才能保持局部几何、变换和子图元关系清晰。

## 3. `polygon()` 返回副本，编辑后必须回写

```cpp
QPolygonF points = node->polygon();
points[1].setX(120);
node->setPolygon(points);
```

`polygon()` 返回值，修改返回对象不会直接改变图元。顶点编辑器通常按这个过程工作：

1. 将鼠标 scene 坐标用 `mapFromScene()` 转成图元本地坐标。
2. 修改 `QPolygonF` 中对应顶点。
3. 调用 `setPolygon()` 回写。

```cpp
const QPointF local = node->mapFromScene(mouseScenePos);
QPolygonF points = node->polygon();
points[draggedIndex] = local;
node->setPolygon(points);
```

不要直接用 scene 坐标覆盖局部顶点，否则图元一旦移动、缩放或成为父图元的子项，顶点编辑就会发生偏移。

## 4. `fillRule`：自交区域到底算不算内部

多边形通常自动闭合。简单、不自交的多边形几乎不需要关心填充规则；一旦出现星形、8 字形或洞状轮廓，规则会决定 brush 填到哪里，也会影响 `shape()`、`contains()` 和碰撞结果。

默认规则是 `Qt::OddEvenFill`：

```cpp
node->setFillRule(Qt::OddEvenFill);
```

| 规则 | 内部判定 | 适合场景 |
| --- | --- | --- |
| `Qt::OddEvenFill` | 从点向外发射射线，与边相交次数为奇数则在内部。每穿过一层，内外状态翻转。 | 普通自交形状、带洞选区、无需控制顶点绕行方向的输入。 |
| `Qt::WindingFill` | 计算轮廓绕点的方向性次数，非零即在内部。 | 需要用顶点顺/逆时针方向表达“实心区域”与“洞”的矢量图形。 |

经验上，用户手绘出的复杂选择区域优先 `OddEvenFill`，因为每次穿越边界都自然切换内外。SVG、地图或布尔路径类数据若已有明确轮廓方向，`WindingFill` 更能保留其语义。

填充规则不是纯视觉选项。若用户点击“洞”中间仍选中了图元，先检查 `fillRule()` 和多边形是否自交，而不是只检查 brush。

## 5. pen、brush、边界和命中

```cpp
node->setPen(QPen(Qt::darkBlue, 4));
node->setBrush(QBrush(QColor("#d9efff")));
```

继承的 `QPen` 和 `QBrush` 控制边框与内部填充。粗 pen 会让实际可见范围大于顶点的最小外接矩形，因此：

- `polygon()`：原始本地顶点序列。
- `boundingRect()`：scene 索引和重绘用的保守范围。
- `shape()`：用于精确命中和碰撞的路径，包含多边形、填充规则和描边影响。
- `contains(point)`：判断**本地坐标**点是否命中。

```cpp
const bool hit = node->contains(node->mapFromScene(scenePoint));
```

不要用多边形的 `boundingRect()` 替代 `contains()` 做点击判断。三角形、菱形和凹多边形的矩形外接范围会包含大量实际不属于图元的区域。

## 6. 不要用它解决所有路径问题

`QGraphicsPolygonItem` 只有一条多边形轮廓。以下需求更适合 `QGraphicsPathItem`：

- 圆弧、贝塞尔曲线、多个子路径。
- 需要精确控制闭合方式和复杂布尔路径。
- 从 SVG path 或 `QPainterPath` 直接导入几何。

若只是展示大量静态区域，也应评估单个 item 数量和 scene 索引开销；数据量很大时，批量绘制到一个自定义 item 往往更高效。

## 7. 类型和框架接口

`type()` 返回 `QGraphicsPolygonItem::Type`，值为 `5`。在异构 `QGraphicsItem *` 集合中确认类型后才可使用 `static_cast`。

`paint()`、`boundingRect()`、`shape()`、`contains()` 属于场景绘制与命中流程。`isObscuredBy()`、`opaqueArea()` 用于遮挡优化；`supportsExtension()`、`setExtension()`、`extension()` 是框架扩展协议，普通项目不直接调用。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型常量 | `QGraphicsPolygonItem::Type = 5` | 标识多边形图元的运行时类型。 | 用 `type()` 确认后再进行 `static_cast`。 |
| 构造 | `explicit QGraphicsPolygonItem(QGraphicsItem *parent = nullptr)` | 创建空多边形图元。 | 后续使用 `setPolygon()` 赋予顶点。 |
| 构造 | `explicit QGraphicsPolygonItem(const QPolygonF &polygon, QGraphicsItem *parent = nullptr)` | 以顶点序列创建多边形图元。 | 顶点是图元本地坐标，不是 scene 坐标。 |
| 析构 | `~QGraphicsPolygonItem()` | 销毁多边形图元。 | 由图元父子树或 scene 生命周期处理。 |
| 顶点读取 | `QPolygonF polygon() const` | 返回当前的本地顶点序列。 | 返回副本，改完必须 `setPolygon()` 回写。 |
| 顶点设置 | `void setPolygon(const QPolygonF &polygon)` | 替换整个本地顶点序列。 | 编辑顶点时先把鼠标 scene 坐标映射到本地坐标。 |
| 填充规则 | `Qt::FillRule fillRule() const` | 返回当前内部区域判定规则。 | 自交或洞状轮廓时会影响绘制、命中和碰撞。 |
| 填充规则 | `void setFillRule(Qt::FillRule rule)` | 设置奇偶或绕数填充规则。 | 默认 `OddEvenFill`；矢量轮廓方向有语义时考虑 `WindingFill`。 |
| 绘制边界 | `QRectF boundingRect() const` | 返回 scene 索引和重绘使用的范围。 | 粗 pen 会扩大结果，且通常比真正多边形宽松。 |
| 命中 | `QPainterPath shape() const` | 返回精确命中和碰撞路径。 | 同时受 polygon、fillRule 与 pen 影响。 |
| 命中 | `bool contains(const QPointF &point) const` | 判断本地点是否命中多边形。 | scene 坐标须先 `mapFromScene()`。 |
| 绘制 | `void paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget = nullptr)` | 按 polygon、pen、brush 和 fillRule 绘制。 | 由 Graphics View 调用，业务代码不直接调用。 |
| 遮挡优化 | `bool isObscuredBy(const QGraphicsItem *item) const` | 判断其它图元是否遮住本图元。 | 不是多边形相交/碰撞 API。 |
| 遮挡优化 | `QPainterPath opaqueArea() const` | 返回已知完全不透明区域。 | 用于 scene 绘制优化，不是命中区域。 |
| 类型查询 | `int type() const` | 返回 `QGraphicsPolygonItem::Type`。 | 用于异构图元集合的类型分派。 |
| 受保护扩展 | `bool supportsExtension(Extension extension) const` | 查询是否支持指定图元扩展。 | Qt 框架协议，普通应用不调用。 |
| 受保护扩展 | `void setExtension(Extension extension, const QVariant &variant)` | 写入扩展数据。 | 仅自定义框架扩展实现时使用。 |
| 受保护扩展 | `QVariant extension(const QVariant &variant) const` | 读取扩展数据。 | 参数与返回语义由具体扩展决定。 |

## 9. 排查清单

1. 拖动顶点时位置漂移：将 scene 鼠标坐标先 `mapFromScene()`，再更新 `QPolygonF`。
2. 修改顶点没有任何效果：`polygon()` 返回副本，必须调用 `setPolygon()` 回写。
3. 自交星形/洞填充不对：检查 `fillRule()`，分别尝试奇偶与绕数规则。
4. 点击外接矩形角落仍命中：使用 `contains()` / `shape()`，不要以 `boundingRect()` 做精确判断。
5. 多边形越来越复杂：改用 `QGraphicsPathItem` 或一个自定义批量绘制图元。

### 一句话总结

`QGraphicsPolygonItem` 用局部 `QPolygonF` 定义闭合区域，用 `fillRule` 决定复杂轮廓的内部语义；顶点编辑必须在本地坐标中完成并通过 `setPolygon()` 回写，精确命中则依赖 `shape()` 而不是外接矩形。
