<!-- 依据 Qt 6.11.1 头文件 qgraphicsitem.h 整理。 -->

# QGraphicsEllipseItem 深入笔记

> 头文件：`#include <QGraphicsEllipseItem>`  
> 模块：`Qt6::Widgets`  
> 继承：`QGraphicsItem -> QAbstractGraphicsShapeItem -> QGraphicsEllipseItem`

## 1. 它解决什么问题

`QGraphicsEllipseItem` 绘制椭圆、圆、圆弧、扇形和饼图切片。它用一个本地 `QRectF` 规定外接椭圆，再由 `startAngle` 和 `spanAngle` 决定是完整椭圆还是其中一段。

典型场景：

- 流程图中的圆形节点、状态灯、端点。
- 环形进度、扇形统计图、仪表盘刻度区域。
- 选区、圆形命中热区、雷达图标记。

它不适合：

- 任意复杂曲线：`QGraphicsPathItem` 更灵活。
- 圆角矩形：使用自定义路径或自绘 item。
- 高性能的大量点云圆标记：视数量和更新频率考虑批量自绘，避免每点一个独立 item。

## 2. 外接矩形和 scene 位置

```cpp
auto *indicator = new QGraphicsEllipseItem(0, 0, 32, 32);
indicator->setPos(200, 80);
```

和 `QGraphicsRectItem` 一样：

- `rect()` 是椭圆在**图元本地坐标**中的外接矩形。
- `setPos()` 是图元原点在父图元/scene 中的位置。

移动圆形应调用 `setPos()`，缩放或改变长短轴才调用 `setRect()`。把 scene 坐标写进 `setRect()` 会混淆图元的局部几何和场景摆放，后续旋转、缩放、子图元与命中换算都会变得难读。

拖拽生成的矩形仍要归一化：

```cpp
ellipse->setRect(QRectF(dragStart, dragCurrent).normalized());
```

负宽或负高的矩形不应传给图元依赖其绘制结果。

## 3. 完整椭圆、圆弧和扇形

`QGraphicsEllipseItem` 有三个互相关联的状态：

```cpp
ellipse->setRect(0, 0, 120, 120);
ellipse->setStartAngle(0);
ellipse->setSpanAngle(360 * 16);
```

- `rect`：外接椭圆的区域。
- `startAngle`：起始角。
- `spanAngle`：从起始角扫过的角度。

当 `spanAngle` 为完整圆时，得到完整椭圆；小于完整圆时，绘制的是一段椭圆弧和它与中心点围成的扇形区域。`Qt::NoBrush` 可将其表现为仅描边的圆弧；设置 brush 后内部扇形会被填充。

## 4. 角度单位：不是度，是十六分之一度

这组 API 使用 `int`，但单位是 **1/16 度**：

```text
90 度  = 90 * 16  = 1440
180 度 = 180 * 16 = 2880
360 度 = 360 * 16 = 5760
```

为了避免满篇魔法数字，建议封装一次：

```cpp
constexpr int angle16(qreal degrees)
{
    return qRound(degrees * 16.0);
}

ellipse->setStartAngle(angle16(-90.0));
ellipse->setSpanAngle(angle16(72.0));
```

角度约定：

- `0` 度在圆的 3 点钟方向。
- 正值逆时针扫过。
- 负值顺时针扫过。

所以常见“从 12 点钟开始的进度环”要从 `-90` 度开始：

```cpp
progressArc->setStartAngle(angle16(-90.0));
progressArc->setSpanAngle(angle16(360.0 * progress));
```

例如 `progress == 0.25` 时 span 为 `1440`，即从 12 点钟逆时针扫过四分之一圆。若设计期望顺时针增长，将 span 取负。

## 5. 画笔、填充和命中范围

`QGraphicsEllipseItem` 继承 `setPen()` 和 `setBrush()`：

```cpp
ellipse->setPen(QPen(QColor("#3578b8"), 3));
ellipse->setBrush(QColor("#dcefff"));
```

粗 pen 会扩展可见边缘，所以：

- `rect()` 只是原始椭圆区域。
- `boundingRect()` 是 scene 索引与重绘用的保守范围，会计入笔宽。
- `shape()` 给出更准确的命中/碰撞路径。
- `contains()` 接收图元**本地坐标**点。

scene 坐标点击测试需先映射：

```cpp
const bool hit = ellipse->contains(
    ellipse->mapFromScene(scenePoint));
```

仅用 `boundingRect().contains()` 会把椭圆四角也当成命中区域，做圆形按钮、地图标记或扇形图时尤其容易误判。

## 6. 饼图与进度环的设计选择

`QGraphicsEllipseItem` 的部分角度绘制天然是扇形，而不是“空心环”。要画进度环有两种常见做法：

1. `Qt::NoBrush` + 较粗 `QPen`：得到一段粗圆弧，适合进度环。
2. 绘制一个大扇形再叠加背景色的小圆：得到甜甜圈状的扇区，适合饼图。

当需要圆角线帽、渐变笔触、多个连续弧段或精确的环形命中区域时，`QPainterPath` 和自定义 `QGraphicsObject` 通常比拼多个椭圆 item 更好维护。

## 7. 类型与框架接口

`type()` 返回 `QGraphicsEllipseItem::Type`，其值为 `4`。它用于在 `QGraphicsItem *` 集合中识别椭圆图元：

```cpp
if (item->type() == QGraphicsEllipseItem::Type) {
    auto *ellipse = static_cast<QGraphicsEllipseItem *>(item);
}
```

`paint()`、`boundingRect()`、`shape()`、`contains()` 由 Graphics View 调用。`isObscuredBy()` 与 `opaqueArea()` 服务遮挡优化；三项受保护 `Extension` API 是框架扩展协议，普通应用不直接调用。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型常量 | `QGraphicsEllipseItem::Type = 4` | 标识椭圆图元的运行时类型。 | 用 `type()` 确认后再 `static_cast`。 |
| 构造 | `explicit QGraphicsEllipseItem(QGraphicsItem *parent = nullptr)` | 创建未设置外接矩形的椭圆图元。 | 后续用 `setRect()` 指定本地几何。 |
| 构造 | `explicit QGraphicsEllipseItem(const QRectF &rect, QGraphicsItem *parent = nullptr)` | 用外接矩形创建椭圆。 | 传入前归一化，避免负宽高。 |
| 构造 | `explicit QGraphicsEllipseItem(qreal x, qreal y, qreal w, qreal h, QGraphicsItem *parent = nullptr)` | 用本地坐标和尺寸创建椭圆。 | `x/y` 不是 scene 位置。 |
| 析构 | `~QGraphicsEllipseItem()` | 销毁椭圆图元。 | 由图元父子树或 scene 生命周期处理。 |
| 几何 | `QRectF rect() const` | 返回本地外接矩形。 | 不等于 `pos()` 或 `boundingRect()`。 |
| 几何 | `void setRect(const QRectF &rect)` | 设置本地外接矩形。 | 拖拽矩形先 `normalized()`；移动用 `setPos()`。 |
| 几何 | `void setRect(qreal x, qreal y, qreal w, qreal h)` | 用数值设置本地外接矩形。 | 是 `QRectF` setter 的便捷重载。 |
| 角度 | `int startAngle() const` | 返回起始角，单位为 1/16 度。 | `0` 在 3 点钟方向。 |
| 角度 | `void setStartAngle(int angle)` | 设置起始角。 | 使用 `degrees * 16`，12 点钟起点常用 `-90 * 16`。 |
| 角度 | `int spanAngle() const` | 返回扫过角度，单位为 1/16 度。 | 正值逆时针，负值顺时针。 |
| 角度 | `void setSpanAngle(int angle)` | 设置扫过角度。 | 完整圆为 `5760`；用符号控制方向。 |
| 绘制边界 | `QRectF boundingRect() const` | 返回 scene 索引和重绘所用范围。 | 粗 pen 会使结果大于 `rect()`。 |
| 命中 | `QPainterPath shape() const` | 返回椭圆/扇形的精确路径。 | 适合碰撞与命中，坐标为图元本地坐标。 |
| 命中 | `bool contains(const QPointF &point) const` | 判断本地点是否落入有效形状。 | scene 点先 `mapFromScene()`；不要用外接矩形代替。 |
| 绘制 | `void paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget = nullptr)` | 按矩形、角度、pen 和 brush 绘制。 | 由场景调用，业务代码不直接调用。 |
| 遮挡优化 | `bool isObscuredBy(const QGraphicsItem *item) const` | 判断其它图元是否遮住本椭圆。 | 不是碰撞或相交查询 API。 |
| 遮挡优化 | `QPainterPath opaqueArea() const` | 返回完全不透明区域。 | 用于 scene 绘制优化，不是命中区域。 |
| 类型查询 | `int type() const` | 返回 `QGraphicsEllipseItem::Type`。 | 用于异构图元集合的类型分派。 |
| 受保护扩展 | `bool supportsExtension(Extension extension) const` | 查询是否支持指定图元扩展。 | Qt 框架协议，普通应用不调用。 |
| 受保护扩展 | `void setExtension(Extension extension, const QVariant &variant)` | 写入扩展数据。 | 仅自定义图元框架扩展时使用。 |
| 受保护扩展 | `QVariant extension(const QVariant &variant) const` | 读取扩展数据。 | 参数和返回约定由具体扩展决定。 |

## 9. 排查清单

1. 圆弧方向反了：记住正值逆时针，顺时针 span 要取负。
2. 仪表盘从 3 点钟开始：将 `startAngle` 设为 `-90 * 16`。
3. 角度看起来小了 16 倍：API 参数不是度，必须乘以 `16`。
4. 圆形按钮四角也能点中：用 `contains()` / `shape()`，不要只查 `boundingRect()`。
5. 想画空心环却得到实心扇形：使用 `Qt::NoBrush` 配合粗 pen，或用路径实现环形区域。

### 一句话总结

`QGraphicsEllipseItem` 用本地外接矩形定义椭圆，用十六分之一度的起始角和跨度定义圆弧或扇形；准确使用它的关键是分清 `rect` 与 `pos`、记住 3 点钟起点和角度方向，并用精确 `shape` 处理圆形命中。
