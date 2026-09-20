<!-- 依据 Qt 6.11.1 头文件 qgraphicsitem.h 整理。 -->

# QGraphicsPathItem 深入笔记

> 头文件：`#include <QGraphicsPathItem>`  
> 模块：`Qt6::Widgets`  
> 继承：`QGraphicsItem -> QAbstractGraphicsShapeItem -> QGraphicsPathItem`

## 1. 它解决什么问题

`QGraphicsPathItem` 用一个 `QPainterPath` 表示任意二维轮廓。相较于矩形、椭圆、多边形，它能同时表达直线、圆弧、二次/三次贝塞尔曲线、多个子路径和复杂填充区域。

它适合：

- 流程图中的圆角连线、箭头轮廓、避障路径。
- 矢量编辑器中的自由曲线、布尔轮廓、选区。
- 仪表盘弧线、地图边界、SVG 风格路径。
- 需要精确 shape/contains 的不规则可交互图元。

它不适合：

- 只有一条简单线段：`QGraphicsLineItem` 更轻。
- 只有矩形、圆或多边形：对应专用 item 语义更明确。
- 每帧重建极复杂路径的大规模动画：需要缓存、简化路径或改成专用自绘方案。

## 2. 从 `QPainterPath` 到场景图元

```cpp
#include <QGraphicsPathItem>
#include <QPainterPath>

QPainterPath outline;
outline.moveTo(0, 30);
outline.cubicTo(40, -10, 80, 70, 120, 30);
outline.lineTo(110, 55);
outline.lineTo(120, 30);
outline.lineTo(100, 20);
outline.closeSubpath();

auto *item = new QGraphicsPathItem(outline);
item->setPen(QPen(QColor("#3c6d95"), 2));
item->setBrush(QColor("#e5f2fb"));
item->setPos(180, 100);
scene->addItem(item);
```

`outline` 中的所有点是图元本地坐标；`setPos()` 决定整个路径放到 scene 的哪里。和其它 Graphics View item 一样，移动路径不要逐点加 scene 偏移，应移动图元本身。

若路径代表封闭区域，明确调用 `closeSubpath()`。这能让路径的轮廓、填充意图和描边终点保持一致；不要依赖不同绘制操作对“开放子路径填充”的隐式处理。

## 3. `path()` 返回副本，修改后必须 `setPath()`

```cpp
QPainterPath edited = item->path();
edited.lineTo(newLocalPoint);
item->setPath(edited);
```

`path()` 返回值对象，修改它不会自动更新 item。路径编辑器的一次顶点/控制点拖动通常是：

1. 把鼠标 scene 坐标用 `mapFromScene()` 转成本地坐标。
2. 在自己的路径模型中更新该控制点或子路径。
3. 构建或修改 `QPainterPath`。
4. 调用 `setPath()` 回写。

`setPath()` 可能改变 `boundingRect()`、`shape()`、场景索引和重绘区域。少量控制点的交互式编辑通常没问题；面对非常复杂路径时，避免在一次鼠标移动里重复构建大量中间路径或频繁执行昂贵布尔运算。

## 4. 路径命令的使用边界

```cpp
QPainterPath path;
path.moveTo(0, 0);
path.lineTo(80, 0);
path.quadTo(100, 0, 100, 20);
path.cubicTo(100, 45, 60, 60, 0, 40);
path.arcTo(QRectF(0, 0, 100, 100), 0, 90);
```

- `moveTo()`：开始新的子路径，不绘制连接段。
- `lineTo()`：添加直线段。
- `quadTo()` / `cubicTo()`：添加二次或三次贝塞尔曲线。
- `arcTo()`：添加椭圆弧。这里使用**普通度数**，不是 `QGraphicsEllipseItem` 的十六分之一度。
- `addPath()`：把另一个 path 的子路径合并进来。

路径的绘制笔触和命中范围仍受 `QPen` 影响。曲线视觉上很细时，默认 `shape()` 的可点击宽度可能太小；复杂交互图元可以单独重写 `shape()`，以更宽的 `QPainterPathStroker` 路径作为命中区域。

## 5. 填充规则决定复杂区域的内部语义

`QPainterPath` 自己带有 `fillRule`。当路径有自交、多个闭合子路径或洞时，它决定 brush 填充、`shape()` 和 `contains()` 的内部区域。

```cpp
QPainterPath path;
// 添加多个闭合子路径 ...
path.setFillRule(Qt::OddEvenFill);
item->setPath(path);
```

| 规则 | 内部判定 | 适合情况 |
| --- | --- | --- |
| `Qt::OddEvenFill` | 每穿过一次边界就切换内外。 | 用户画出的自交选区、普通洞状区域。 |
| `Qt::WindingFill` | 依据轮廓方向的绕数，非零即内部。 | SVG/地图等顶点方向本身有语义的路径。 |

不要只给 item 调 `setBrush()` 就假设洞会透明。洞是否被填充先由 `QPainterPath::fillRule()` 决定。

## 6. `boundingRect`、`shape`、`contains` 的分工

```text
path()          原始几何数据
boundingRect()  给 scene 的保守重绘/索引范围
shape()         精确命中和碰撞路径，含 pen 影响
contains()      判断一个本地点是否在 shape 内
```

粗 pen、曲线外凸和多子路径都会让 `boundingRect()` 大于简单的控制点范围。点击判断一定使用本地坐标：

```cpp
const QPointF local = item->mapFromScene(scenePoint);
if (item->contains(local)) {
    // 命中路径
}
```

`opaqueArea()` 与 `isObscuredBy()` 是 scene 遮挡优化接口，不应代替业务碰撞检测、路径相交或布尔运算。

## 7. 什么时候需要自定义 `QGraphicsObject`

`QGraphicsPathItem` 已提供一个完整路径和一套 pen/brush。以下情况可直接升级到自定义 item：

- 需要控制点、悬停手柄、路径标签和箭头作为子图元。
- 绘制很细、但命中必须很宽。
- path 改变需要驱动模型、撤销栈或信号。
- 需要分层缓存、渐变动画或定制选中状态。

此时常让 `QGraphicsObject` 持有 `QPainterPath`，自己实现 `boundingRect()`、`shape()`、`paint()`，并在路径改变前后遵守 `prepareGeometryChange()`。

## 8. 类型与扩展接口

`type()` 返回 `QGraphicsPathItem::Type`，值为 `2`。在 `QGraphicsItem *` 集合中需先比较 `type()`，再做 `static_cast`。

`supportsExtension()`、`setExtension()`、`extension()` 是受保护的 QGraphicsItem 框架扩展接口；标准路径项为了框架兼容性重写，普通应用不应直接调用。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型常量 | `QGraphicsPathItem::Type = 2` | 标识路径图元的运行时类型。 | 用 `type()` 确认后再 `static_cast`。 |
| 构造 | `explicit QGraphicsPathItem(QGraphicsItem *parent = nullptr)` | 创建空路径图元。 | 后续使用 `setPath()` 设置几何。 |
| 构造 | `explicit QGraphicsPathItem(const QPainterPath &path, QGraphicsItem *parent = nullptr)` | 用一个本地路径创建图元。 | 路径点是本地坐标，不是 scene 坐标。 |
| 析构 | `~QGraphicsPathItem()` | 销毁路径图元。 | 由 scene 或图元父子树处理所有权。 |
| 路径读取 | `QPainterPath path() const` | 返回当前路径。 | 返回副本，编辑后必须 `setPath()`。 |
| 路径设置 | `void setPath(const QPainterPath &path)` | 替换整个本地路径。 | 可能改变边界、命中和 scene 索引；复杂路径编辑勿无意义高频重建。 |
| 绘制边界 | `QRectF boundingRect() const` | 返回 scene 索引和重绘的保守范围。 | 粗 pen、曲线和外凸都会扩大范围。 |
| 命中 | `QPainterPath shape() const` | 返回精确命中和碰撞路径。 | 受 path、fillRule 和 pen 影响。 |
| 命中 | `bool contains(const QPointF &point) const` | 判断本地点是否命中路径。 | scene 点须先 `mapFromScene()`。 |
| 绘制 | `void paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget = nullptr)` | 按路径、pen 与 brush 绘制。 | 由 Graphics View 调用，不直接从业务代码调用。 |
| 遮挡优化 | `bool isObscuredBy(const QGraphicsItem *item) const` | 判断其它图元是否遮住本路径项。 | 不等于路径相交或碰撞检查。 |
| 遮挡优化 | `QPainterPath opaqueArea() const` | 返回已知完全不透明区域。 | 用于 scene 优化，不是点击区域。 |
| 类型查询 | `int type() const` | 返回 `QGraphicsPathItem::Type`。 | 用于异构图元集合的类型分派。 |
| 受保护扩展 | `bool supportsExtension(Extension extension) const` | 查询是否支持指定图元扩展。 | Qt 框架协议，普通应用不调用。 |
| 受保护扩展 | `void setExtension(Extension extension, const QVariant &variant)` | 写入扩展数据。 | 仅自定义图元框架扩展时使用。 |
| 受保护扩展 | `QVariant extension(const QVariant &variant) const` | 读取扩展数据。 | 参数和返回语义由具体扩展决定。 |

## 10. 排查清单

1. 改控制点没有更新：`path()` 返回副本，编辑后调用 `setPath()`。
2. 圆弧角度错了 16 倍：`QPainterPath::arcTo()` 使用普通度数，不乘 `16`。
3. 洞被填实或自交区域不对：检查 path 自身的 `fillRule()`。
4. 点中曲线很困难：用本地坐标 `contains()`；必要时用自定义 `shape()` 扩大交互带。
5. 拖动复杂路径卡顿：减少每次移动的路径重建和布尔计算，必要时在交互结束后再精化。

### 一句话总结

`QGraphicsPathItem` 把任意 `QPainterPath` 变成可绘制、可命中的 scene 图元；安全使用它的关键是路径始终保留在本地坐标、编辑后用 `setPath()` 回写、填充规则决定复杂区域语义，并分清路径 API 的普通角度与椭圆 item 的十六分之一度。
