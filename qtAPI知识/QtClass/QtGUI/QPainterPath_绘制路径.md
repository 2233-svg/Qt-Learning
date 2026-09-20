# QPainterPath：把几何轮廓组织成可绘制、可命中的路径

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QPainterPath>`  
> CMake：`find_package(Qt6 REQUIRED COMPONENTS Gui)`，并链接 `Qt6::Gui`

`QPainterPath` 是二维矢量几何的容器。它记录直线、二次/三次贝塞尔曲线和若干子路径；随后可以交给 `QPainter::drawPath()` 绘制、交给 `QPainter::fillPath()` 填充，也能用来做命中测试、裁剪、布尔运算或生成笔画轮廓。

它是隐式共享的值类型：按值传递或复制通常很便宜，任意一个副本被修改时才分离底层数据。不要让多个线程并发修改同一个实例；构造完成、只读使用的独立副本则不依赖 GUI 对象，适合交给工作线程做纯几何计算。

## 它解决的问题

绘图 API 不应把一条复杂轮廓拆成很多互相依赖的临时坐标。`QPainterPath` 把“从哪里开始、接着连到哪里、哪些部分是闭合轮廓”保存为一个对象，因而特别适合：

- 自定义控件绘制圆角面板、图标、连接线、波形和不规则区域。
- 用 `contains()` 判断鼠标是否落在不规则按钮、地图区域或矢量图形内部。
- 用 `intersected()`、`united()`、`subtracted()` 合并、裁切或挖空填充区域。
- 配合 `QPainterPathStroker` 把一条中心线变成具有宽度、端点和连接样式的可填充轮廓。
- 从字体轮廓、SVG 风格曲线或手写轨迹生成 `QPolygonF`，再交给其他几何或渲染代码。

路径本身不保存画笔、画刷、变换或设备像素比。这些由 `QPainter`、`QPen`、`QBrush` 和 `QTransform` 决定；同一条路径可以在不同设备、不同样式下复用。

## 最小使用

```cpp
#include <QPainter>
#include <QPainterPath>

void BadgeWidget::paintEvent(QPaintEvent *)
{
    QPainterPath badge;
    badge.addRoundedRect(rect().adjusted(1, 1, -1, -1), 8, 8);

    QPainter painter(this);
    painter.setPen(Qt::NoPen);
    painter.setBrush(QColor("#1976d2"));
    painter.drawPath(badge);
}
```

`addRoundedRect()` 创建的是闭合子路径，所以既能描边也能填充。若仅调用 `moveTo()` 和 `lineTo()`，得到的是开放轮廓；描边通常符合预期，但填充、命中和布尔运算会按填充语义把开放部分视为隐式闭合。

## 路径模型：当前点与子路径

路径由一个或多个子路径组成。`moveTo()` 设定一个新子路径的起点，并隐式结束前一个子路径；它不会画出连接线。`lineTo()`、`quadTo()`、`cubicTo()`、`arcTo()` 都从当前点继续，调用后其终点成为新的当前点。

```cpp
QPainterPath path;
path.moveTo(20, 80);                 // 子路径 A 的起点
path.cubicTo(45, 10, 95, 10, 120, 80);
path.lineTo(20, 80);
path.closeSubpath();                 // 显式闭合 A

path.moveTo(150, 20);                // 开始子路径 B，不连接 A 和 B
path.lineTo(210, 80);
```

`closeSubpath()` 会添加一段回到子路径起点的直线（如有必要），然后关闭当前子路径。一个容易踩到的边界是：调用后当前点会变为 `(0, 0)`；要继续画新的独立轮廓，明确调用 `moveTo()`，不要依赖这个当前点。

`lineTo()` 在空路径上使用时，Qt 会先以 `(0, 0)` 作为起点。因此从任意位置开始画线，先调用 `moveTo()` 更清楚也更不易误判。

## 追加路径：`addPath()` 与 `connectPath()`

这两个函数名字相近，连接规则完全不同：

```cpp
QPainterPath outline;
outline.addRect(0, 0, 40, 40);

QPainterPath tail;
tail.moveTo(50, 20);
tail.lineTo(90, 20);

outline.addPath(tail);       // 追加为另一段路径，不额外连线
// outline.connectPath(tail); // 会从 outline 最后元素连到 tail 的第一元素
```

- `addPath()` 将传入路径作为闭合子路径追加到本路径。适合把多个独立图形放进同一填充或绘制对象。
- `connectPath()` 在本路径的当前末点和传入路径的首点之间补一条线，再追加传入路径。适合需要连续轮廓的拼接，但首尾位置不合适时会意外多出一条斜线。
- `addPolygon()` 添加的是**未闭合**子路径；若多边形必须成为填充区域，应自行 `closeSubpath()`，或改用闭合的 `addRect()` 等 API。
- `addRect()`、`addEllipse()`、`addRoundedRect()`、`addText()` 和 `addRegion()` 产生闭合子路径。

## 曲线与圆弧

`quadTo(control, end)` 添加二次贝塞尔曲线；`cubicTo(control1, control2, end)` 添加三次贝塞尔曲线。控制点通常不在曲线上，它们决定切线方向和曲率。

`arcMoveTo(rect, angle)` 只把当前点移到椭圆弧上对应的点；`arcTo(rect, startAngle, arcLength)` 则先从当前点连接到弧的起点，再追加椭圆弧。角度以度为单位，`0` 位于三点钟方向；正角度逆时针，负角度顺时针。

```cpp
QPainterPath sector;
sector.moveTo(60, 60);
sector.arcTo(QRectF(10, 10, 100, 100), 30, 280);
sector.closeSubpath(); // 扇形而非孤立弧线
```

若只想让下一段从弧线端点开始，又不希望从旧当前点画一条连接线，先用 `arcMoveTo()`。

## 填充规则与开放路径的边界

默认填充规则是 `Qt::OddEvenFill`：从点向外发射射线，边界交叉次数为奇数则在内部。这对“外圈减内孔”很直观。`Qt::WindingFill` 根据边缘方向累加绕行数，适用于依赖轮廓方向的复合形状。

```cpp
QPainterPath donut;
donut.setFillRule(Qt::OddEvenFill);
donut.addEllipse(QRectF(0, 0, 100, 100));
donut.addEllipse(QRectF(30, 30, 40, 40)); // 中心形成孔
```

`contains()`、`intersects()` 和路径布尔运算处理开放子路径时，会把它们当成隐式闭合的面积轮廓。不要把“描边看起来是一条折线”误认为它在几何测试中仍是没有面积的线；若需要按笔画宽度命中，应使用 `QPainterPathStroker::createStroke()` 生成笔画区域后测试。

## 命中、范围与布尔运算

`contains(point)` 测试点是否处在可填充区域内；`contains(rect)` 要求整个矩形在路径内；`intersects(rect)` 则只要矩形与路径有交集即可。针对两个路径，也有对应的 `contains(path)` 与 `intersects(path)`。

`boundingRect()` 给出路径的精确轴对齐外接矩形，必要时会计算曲线极值。`controlPointRect()` 只包围元素和贝塞尔控制点，是 `boundingRect()` 的超集，但计算明显更快。动画、视图裁剪的粗略过滤可先用 `controlPointRect()`；布局和精确碰撞边界用 `boundingRect()`。

```cpp
QPainterPath clipped = icon.intersected(clipArea);
QPainterPath merged  = left.united(right);
QPainterPath hole    = panel.subtracted(cutout);
```

布尔运算以填充区域为对象，可能将贝塞尔曲线扁平化为线段。`simplified()` 也会合并相交子路径、移除冗余边，并总是返回 `Qt::OddEvenFill` 路径。因此它适合为后续区域计算整理形状，却不应拿来保留原始曲线控制点或轮廓方向。

## 元素级编辑与调试

`elementCount()`、`elementAt()` 和 `setElementPositionAt()` 适合路径编辑器、节点调试器和少量局部调整。`Element` 公开 `x`、`y` 与 `type`，并提供类型判断函数。

曲线元素不能逐个当成独立顶点解释：

- `MoveToElement` 是新子路径起点。
- `LineToElement` 是线段终点。
- `CurveToElement` 是三次贝塞尔的第一个控制点。
- 后面必须紧跟两个 `CurveToDataElement`，分别表示第二个控制点和曲线终点。

因此移动一条三次曲线时，通常要作为连续的三个元素整体处理。`setElementPositionAt()` 只改坐标，不会自动保持切线连续、圆弧约束或其他编辑器语义。

## 长度、百分比和缓存

`length()` 返回近似路径长度；`percentAtLength(len)` 把长度位置换算为路径参数；`pointAtPercent(t)`、`angleAtPercent(t)`、`slopeAtPercent(t)` 查询位置、切线角度和斜率。

这里的 `t` 是路径参数，不是弧长比例。路径带有曲线时，`pointAtPercent(0.5)` 往往不在“走过一半距离”的位置。Qt 6.10 引入的 `trimmed(fromFraction, toFraction, offset)` 按长度线性解释 fraction，适合做描边生长、虚线风格的轮廓截取。

对同一路径反复查询长度和百分比时，可启用 Qt 6.10 的缓存：

```cpp
QPainterPath route = makeRoute();
route.setCachingEnabled(true);

const qreal half = route.percentAtLength(route.length() * 0.5);
const QPointF marker = route.pointAtPercent(half);
```

缓存默认关闭，开启会占用额外内存；一次性查询或频繁改动路径时通常没有收益。任意修改路径后，先前计算结果不应继续假定有效。

## 多边形转换与绘制

`toSubpathPolygons()` 为每个子路径生成一个多边形，适合保留子路径边界。`toFillPolygon()` / `toFillPolygons()` 为填充而重绕子路径，可能插入额外连接线；返回的边不能当作原路径的逐段忠实表示。带 `QTransform` 的重载会先在给定变换下转换，曲线扁平化精度也会随变换而变化。

若只是绘制，直接传给 `QPainter` 保留的信息最多：

```cpp
QPainter painter(this);
painter.setRenderHint(QPainter::Antialiasing);
painter.setPen(QPen(Qt::black, 3, Qt::SolidLine, Qt::RoundCap, Qt::RoundJoin));
painter.setBrush(QColor(255, 193, 7, 120));
painter.drawPath(path);
```

## 生命周期、性能和常见错误

- `reserve(n)` 仅预留元素容量，不改变路径内容；批量构建大量点时可减少扩容。`capacity()` 用于观察当前容量，不是元素数，元素数用 `elementCount()`。
- `clear()` 清空所有元素。清空后不要继续使用旧的元素索引。
- `translated()` 返回新路径；`translate()` 原地修改。共享副本上调用原地函数会触发分离。
- `toReversed()` 返回一个元素顺序反转的新路径；它不是针对每个图形语义的“镜像”操作。需要坐标变换时使用 `QTransform`。
- `operator+` / `+=` 对应路径连接语义，`operator|` / `|=` 为并集，`operator&` / `&=` 为交集，`operator-` / `-=` 为差集。为了可读性，业务代码中优先使用命名成员函数。
- 通过 `QDataStream` 读入路径时，把输入当作不可信数据；流状态失败时不要使用结果路径。跨进程或长期持久化格式更宜明确版本与校验，而非把 Qt 私有二进制布局当协议。

## API 速查表

| API | 语义与使用边界 |
| --- | --- |
| `QPainterPath()` | 构造空路径，当前点为 `(0, 0)`。 |
| `QPainterPath(startPoint)` | 构造并以 `startPoint` 作为第一个子路径起点。 |
| 拷贝/移动构造、赋值、`swap()` | 值语义；拷贝隐式共享，修改时分离。移动后只保留目标对象可用性假设。 |
| `clear()` | 删除全部元素和子路径。 |
| `reserve(int size)` | 预留元素容量；适合大量连续构建，不改变 `elementCount()`。 |
| `capacity()` | 返回已分配的元素容量，不等于实际元素数。 |
| `closeSubpath()` | 连接回当前子路径起点并关闭它；调用后当前点为 `(0, 0)`。 |
| `moveTo(QPointF)` / `moveTo(x, y)` | 开始新子路径，不绘制连接线，并隐式结束旧子路径。 |
| `lineTo(QPointF)` / `lineTo(x, y)` | 从当前点添加直线；空路径会以 `(0, 0)` 为起点。 |
| `arcMoveTo(QRectF, angle)` / 坐标重载 | 仅把当前点移动到椭圆弧对应位置。 |
| `arcTo(QRectF, startAngle, arcLength)` / 坐标重载 | 从当前点连到弧起点后添加弧；角度单位为度，正向逆时针。 |
| `cubicTo(c1, c2, end)` / 坐标重载 | 添加三次贝塞尔曲线；两个控制点不一定落在曲线上。 |
| `quadTo(control, end)` / 坐标重载 | 添加二次贝塞尔曲线。 |
| `currentPosition()` | 返回当前点；闭合子路径后为 `(0, 0)`。 |
| `addRect(QRectF)` / 坐标重载 | 添加闭合矩形子路径。 |
| `addEllipse(QRectF)` / 坐标重载 / 中心半径重载 | 添加闭合椭圆子路径。 |
| `addRoundedRect(QRectF, xRadius, yRadius, mode)` / 坐标重载 | 添加闭合圆角矩形；`mode` 决定半径按绝对值还是相对尺寸解释。 |
| `addPolygon(QPolygonF)` | 追加未闭合多边形子路径；需要面积语义时显式闭合。 |
| `addText(QPointF, QFont, QString)` / 坐标重载 | 把字形轮廓追加为闭合子路径；它不是文本布局 API，复杂排版使用 `QTextLayout` 等。 |
| `addPath(const QPainterPath &)` | 追加传入路径而不额外画连接线。 |
| `addRegion(const QRegion &)` | 把整数像素区域追加为闭合路径；适合与 `QRegion` 互操作，曲线信息不会存在。 |
| `connectPath(const QPainterPath &)` | 先连接本路径末点和传入路径首点，再追加；注意潜在的意外斜线。 |
| `contains(QPointF)` | 判断点是否在填充区域内。 |
| `contains(QRectF)` | 仅当整个矩形包含在路径中时为真。 |
| `intersects(QRectF)` | 路径与矩形有任意交集即为真。 |
| `translate(dx, dy)` / `translate(offset)` | 原地平移路径，会修改对象。 |
| `translated(dx, dy)` / `translated(offset)` | 返回平移后的新路径，原路径不变。 |
| `boundingRect()` | 精确轴对齐包围盒；曲线极值会参与计算。 |
| `controlPointRect()` | 控制点包围盒，可能比精确边界大但通常更快。 |
| `fillRule()` | 返回当前填充规则，默认 `Qt::OddEvenFill`。 |
| `setFillRule(Qt::FillRule)` | 设为奇偶或绕数填充；会改变填充、命中和布尔计算语义。 |
| `isEmpty()` | 没有元素时为真；它不是“路径是否有可见面积”的判断。 |
| `toReversed()` | 返回元素顺序反转的新路径。 |
| `toSubpathPolygons(transform)` | 分别输出子路径的扁平化多边形。 |
| `toFillPolygons(transform)` | 输出适合填充的重绕多边形；可能产生额外边。 |
| `toFillPolygon(transform)` | 输出单个适合填充的重绕多边形；同样不保证还原原路径轮廓。 |
| `elementCount()` | 返回元素数；一条三次曲线占三个连续元素。 |
| `elementAt(int i)` | 返回第 `i` 个元素；索引必须在 `[0, elementCount())` 内。 |
| `setElementPositionAt(int i, x, y)` | 修改元素坐标；不维护曲线切线或其他高层约束。 |
| `isCachingEnabled()` | 查询长度/百分比查询缓存是否开启（Qt 6.10 起）。 |
| `setCachingEnabled(bool)` | 开关长度相关缓存；重复查询更快，内存占用更高（Qt 6.10 起）。 |
| `length()` | 计算近似总长度；曲线结果受扁平化和数值计算影响。 |
| `percentAtLength(qreal len)` | 将长度位置映射到路径参数；长度超界时按实现边界处理，调用方应先钳制。 |
| `pointAtPercent(qreal t)` | 返回参数 `t` 处位置；曲线时 `t` 不按弧长均匀。 |
| `angleAtPercent(qreal t)` | 返回该处切线角度，单位为度。 |
| `slopeAtPercent(qreal t)` | 返回该处切线斜率；垂直切线等情形应避免依赖有限数值。 |
| `trimmed(fromFraction, toFraction, offset)` | 按长度比例截取新路径，可附加循环偏移（Qt 6.10 起）。 |
| `intersects(const QPainterPath &)` | 判断两个路径的填充区域是否相交。 |
| `contains(const QPainterPath &)` | 判断传入路径填充区域是否完全被本路径包含。 |
| `united(const QPainterPath &)` | 返回两个填充区域并集；可能扁平化曲线。 |
| `intersected(const QPainterPath &)` | 返回两个填充区域交集；可能扁平化曲线。 |
| `subtracted(const QPainterPath &)` | 返回本路径减去参数路径后的区域；可能扁平化曲线。 |
| `simplified()` | 合并相交子路径并移除冗余边；结果填充规则恒为 `OddEvenFill`。 |
| `operator==` / `operator!=` | 比较路径内容是否相等；不应用作几何近似相等测试。 |
| `operator&` / `&=` | 交集及原地交集，等价于 `intersected()`。 |
| `operator\|` / `\|=` | 并集及原地并集，等价于 `united()`。 |
| `operator+` / `+=` | 路径连接及原地连接，等价于连接语义，不等价于区域并集。 |
| `operator-` / `-=` | 差集及原地差集，等价于 `subtracted()`。 |
| `operator*(QPainterPath, QTransform)` | 返回变换后的路径，等价于由 `QTransform` 映射。 |
| `QDataStream <<` / `>>` | 写入或读取路径；读取外部数据后必须检查流状态和数据规模。 |
| `QDebug <<` | 输出调试表示；仅在未禁用调试流时可用。 |

### `QPainterPath::Element`

| API | 语义与使用边界 |
| --- | --- |
| `x`、`y`、`type` | 元素的公开坐标和类型；曲线的三个连续元素要作为整体解释。 |
| `isMoveTo()` / `isLineTo()` / `isCurveTo()` | 快速判断主要元素类别；`CurveToDataElement` 不会被 `isCurveTo()` 识别。 |
| `operator QPointF()` | 将元素坐标转换成 `QPointF`，不保留元素类型。 |
| `operator==` / `operator!=` | 比较类型和模糊相等的坐标。 |

### `QPainterPath::ElementType`

| 枚举值 | 含义 |
| --- | --- |
| `MoveToElement` | 子路径起点。 |
| `LineToElement` | 直线终点。 |
| `CurveToElement` | 三次贝塞尔第一个控制点。 |
| `CurveToDataElement` | 紧随 `CurveToElement` 的第二控制点或曲线终点。 |
