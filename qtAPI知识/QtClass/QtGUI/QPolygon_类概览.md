# QPolygon：保存整数像素坐标的顶点序列

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QPolygon>`  
> 所属模块：`Qt6::Gui`

`QPolygon` 是 `QList<QPoint>` 的几何专用类型，用整数坐标保存多边形顶点。它适合像素对齐的绘制、窗口区域、简单填充几何和与旧版 Qt API 的互操作。

它仍然只是一个点列表：不会自动闭合、不会保存曲线，也不会记录填充规则。`QPainter::drawPolygon()` 会将顶点按多边形解释并在绘制/填充时闭合；`QPainter::drawPolyline()` 则把同一批点当作开放折线。

## 它解决的问题

当几何天然以设备像素或整数网格表达时，`QPolygon` 能避免不必要的浮点转换：

- 绘制像素对齐的多边形和折线。
- 表达窗口区域、裁剪轮廓和简单整数几何。
- 从矩形快速构造四点或五点闭合轮廓。
- 用 `setPoints()` / `putPoints()` 批量填充顶点。
- 在需要浮点变换前后与 `QPolygonF` 转换。

```cpp
QPolygon polygon;
polygon << QPoint(10, 10)
        << QPoint(120, 20)
        << QPoint(80, 90);

QPainter painter(this);
painter.setPen(QPen(Qt::darkGreen, 1));
painter.setBrush(QColor(76, 175, 80, 90));
painter.drawPolygon(polygon);
```

## 与 `QPolygonF` 和 `QPainterPath` 的选择

- 需要整数像素、快速列表操作和老接口兼容时，使用 `QPolygon`。
- 需要小数坐标、缩放/旋转后保留精度时，使用 `QPolygonF`。
- 需要贝塞尔曲线、多个子路径、路径采样或复杂填充时，使用 `QPainterPath`。

`QPolygon` 继承 `QList<QPoint>`，因此可以使用列表的增删、索引和迭代 API。它不提供 `QPainterPath` 的当前点状态，也不能表示一条曲线或多个有独立起点的子路径。

## 从矩形构造：`closed` 的准确含义

```cpp
QRect rect(10, 20, 100, 60);
QPolygon open(rect);          // 4 个顺时针顶点
QPolygon closed(rect, true);  // 5 个顶点，最后重复 topLeft()
```

当 `closed` 为 `false` 时，结果只包含矩形的四个角；当为 `true` 时，会追加矩形左上角作为第五个点。注意 `QRect` 的右下坐标是 `x + width`、`y + height`，不是把宽高直接当成最后一个坐标。

`closed` 只是数据中是否重复首点。即使没有重复首点，`drawPolygon()` 和多边形区域运算仍会在语义上补齐最后一条边。

## 顶点批量 API

### `setPoint()` 与 `point()`

`setPoint(index, ...)` 修改已有索引位置，不负责把多边形扩展到该索引。索引必须对应已经存在的点；需要扩容时先构造指定大小、调用 `resize()`，或使用 `setPoints()` / `putPoints()`。

`point(index, x, y)` 会把坐标写入有效的输出指针；传入空指针时对应坐标不输出。`point(index)` 返回一个 `QPoint` 副本。

### `setPoints()`

`setPoints(nPoints, points)` 和可变参数重载会把 polygon 调整为恰好 `nPoints` 个点后填充。指针重载要求至少有 `2 * nPoints` 个连续整数；可变参数重载要求后续整数严格按 x、y 成对提供。

```cpp
const int coordinates[] = {10, 20, 80, 20, 50, 70};
QPolygon polygon;
polygon.setPoints(3, coordinates);
```

可变参数接口缺乏编译期长度检查，现代代码通常优先使用 `QList<QPoint>` 初始化或指针数组重载。

### `putPoints()`

`putPoints(index, nPoints, ...)` 从指定索引开始覆盖/追加点，若 `index + nPoints` 超过当前大小则自动扩容。另一个重载从已有 `QPolygon` 的 `fromIndex` 开始复制。

```cpp
QPolygon polygon(1);
polygon[0] = QPoint(4, 5);
polygon.putPoints(1, 2, 6, 7, 8, 9);
```

源 polygon 与目标 polygon 发生别名时，不要依赖复杂的重叠复制行为；需要可靠结果时先复制源数据。`index`、`nPoints`、`fromIndex` 传入负值或使范围失效时，调用方不应期待有效几何结果。

## 区域判断和布尔运算

`containsPoint(point, fillRule)` 按指定填充规则判断点是否在多边形内部。`united()`、`intersected()`、`subtracted()` 把多边形当作面积，而不是只处理边界线；非闭合 polygon 会被隐式闭合。

```cpp
if (polygon.containsPoint(cursorPos, Qt::OddEvenFill))
    setHovered(true);
```

自相交、多重轮廓、重复点和退化边会让区域结果依赖填充规则和几何算法。需要可靠孔洞、多轮廓或曲线边界时，考虑 `QPainterPath`。

`intersects()` 只报告是否有交集，包含边界接触、包含关系等情况；它不返回相交区域。若只做快速过滤，应优先使用它和 `boundingRect()`。

## 平移、一般变换与精度

`translate()` 原地移动所有整数点，`translated()` 返回副本。旋转、缩放和错切应使用 `QTransform::map()`：

```cpp
QTransform transform;
transform.translate(50, 50);
transform.rotate(15);
const QPolygonF transformed = transform.map(polygon.toPolygonF());
```

将整数 polygon 直接转换到 `QPolygonF` 后再变换，能避免中间结果过早舍入。`toPolygonF()` 从 Qt 6.4 起提供；反向 `QPolygonF::toPolygon()` 会损失小数精度。

## 生命周期、线程与性能

`QPolygon` 是隐式共享值类型，复制和按值返回通常便宜；修改共享副本时分离。它不依赖 GUI 线程，可以在线程中处理独立的点列表。

若用 `constData()` 把点数组交给底层函数，调用期间不要改变 polygon；任何可能重分配的列表操作都可能使指针失效。`QPainter` 的批量绘制重载应在调用点直接传入 polygon。

## 常见错误

- 认为四点矩形 polygon 的最后一点会自动回到首点：只有 `QPolygon(rect, true)` 才显式重复首点。
- 把 `setPoint()` 当成自动扩容接口：越界索引不应使用。
- `setPoints()` 的 `nPoints` 与实际整数数组数量不匹配。
- 可变参数 API 漏传一个坐标，导致未定义的读取行为。
- 用整数 polygon 做连续旋转动画，导致每帧舍入和抖动。
- 把非闭合 polygon 的布尔结果当成无面积折线结果。
- 只设置 `QPolygon` 后用 `drawPolyline()`，却期待有填充。

## API 速查表

### 构造与列表

| API | 语义与使用边界 |
| --- | --- |
| `QPolygon()` | 构造空整数顶点列表。 |
| `QPolygon(QList<QPoint>)` | 从整数点列表构造；顺序按输入保留。 |
| `QPolygon(QRect, bool closed)` | 从矩形构造四点轮廓；`closed=true` 时追加首点成为第五点。 |
| `QPolygon(int nPoints, const int *points)` | 从连续 x、y 整数数组构造；数组至少包含 `2 * nPoints` 个整数。 |
| `using QList<QPoint>` | 可用 QList 的增删、索引、迭代、容量和数据访问 API。 |
| `swap(QPolygon &)` | 快速交换两个 polygon。 |
| `operator QVariant()` | 转换为 `QVariant`。 |

### 顶点访问和批量填充

| API | 语义与使用边界 |
| --- | --- |
| `point(index)` | 返回索引处的 `QPoint` 副本；索引必须有效。 |
| `point(index, x, y)` | 将坐标写入有效的 x/y 输出指针；可分别传空指针忽略某一坐标。 |
| `setPoint(index, x, y)` / `setPoint(index, QPoint)` | 修改已有索引的点；不会为越界索引自动扩容。 |
| `setPoints(nPoints, const int *points)` | 调整大小并从连续整数数组填充所有点。 |
| `setPoints(nPoints, firstx, firsty, ...)` | 调整大小并从 x/y 可变参数填充；调用方负责参数数量和类型。 |
| `putPoints(index, nPoints, firstx, firsty, ...)` | 从目标索引开始写入点，必要时扩容；整数按 x/y 成对提供。 |
| `putPoints(index, nPoints, fromPolygon, fromIndex)` | 从另一个 polygon 复制指定数量的点，必要时扩容。 |

### 几何操作

| API | 语义与使用边界 |
| --- | --- |
| `boundingRect()` | 返回顶点的整数轴对齐包围盒；空 polygon 返回空矩形。 |
| `containsPoint(point, fillRule)` | 按奇偶或绕数规则判断点是否在区域内。 |
| `intersects(polygon)` | 判断两个 polygon 是否有交集、包含或被包含关系。 |
| `united(polygon)` | 返回两个填充区域的并集；非闭合输入按隐式闭合处理。 |
| `intersected(polygon)` | 返回两个填充区域的交集。 |
| `subtracted(polygon)` | 返回本区域减去参数区域的结果。 |
| `translate(dx, dy)` / `translate(offset)` | 原地平移所有点。 |
| `translated(dx, dy)` / `translated(offset)` | 返回平移副本。 |
| `toPolygonF()` | 转换为浮点 `QPolygonF`；Qt 6.4 起，适合后续一般变换。 |
| `QTransform::map(QPolygon)` | 执行旋转、缩放、错切等一般变换；结果类型取决于重载。 |

### 流和调试

| API | 语义与使用边界 |
| --- | --- |
| `QDataStream <<` / `>>` | 序列化/读取点列表；读取外部数据时检查流状态和点数上限。 |
| `QDebug <<` | 输出调试表示。 |
