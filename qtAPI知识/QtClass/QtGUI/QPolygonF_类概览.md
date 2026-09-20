# QPolygonF：保存浮点精度的顶点序列

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QPolygonF>`  
> 所属模块：`Qt6::Gui`

`QPolygonF` 是 `QList<QPointF>` 的几何专用类型。它保存一串浮点坐标，可作为折线顶点、填充多边形、绘图输入或几何运算结果。

它的本质仍是一个点列表：单独构造 `QPolygonF` 不会自动闭合，也不会自动把最后一个点连接到第一个点。是否把顶点解释为开放折线或封闭区域，由使用它的 API 决定。

## 它解决的问题

整数 `QPolygon` 适合像素级几何；当坐标来自缩放、旋转、动画、曲线离散化或高 DPI 布局时，浮点精度更合适：

- 使用 `QPainter::drawPolyline()` 绘制开放轨迹。
- 使用 `QPainter::drawPolygon()` 绘制填充区域。
- 保存图表曲线、手写路径和编辑器控制点。
- 在浮点坐标上做点包含、相交、并集和差集。
- 将 `QPainterPath` 或矢量数据转换成点序列交给网格、导出或自定义算法。

```cpp
QPolygonF triangle{
    QPointF(20.5, 10.0),
    QPointF(100.0, 30.25),
    QPointF(60.0, 90.75)
};

QPainter painter(this);
painter.setPen(QPen(Qt::darkBlue, 2));
painter.setBrush(QColor(30, 136, 229, 80));
painter.drawPolygon(triangle);
```

`drawPolygon()` 会按填充规则处理区域；`drawPolyline()` 只画开放线段，不填充。若需要明确表达闭合轮廓，可让首点和末点相同，并用 `isClosed()` 检查。

## 它是 `QList<QPointF>`，但不是路径

因为 `QPolygonF` 继承 `QList<QPointF>`，可以使用 `append()`、`prepend()`、`insert()`、`removeAt()`、`first()`、`last()`、索引访问和迭代器等列表操作。列表操作只修改顶点，不附带任何曲线、笔画、填充规则或子路径语义。

```cpp
QPolygonF path;
path << QPointF(0, 0)
     << QPointF(20.5, 12.0)
     << QPointF(50, 6);

for (const QPointF &point : path)
    qDebug() << point;
```

如果轮廓包含贝塞尔曲线、多个独立子路径或需要区分 `moveTo` 与 `lineTo`，应使用 `QPainterPath`。`QPolygonF` 只是折线顶点列表，无法保留曲线控制点和子路径边界。

## 闭合、填充与边界

`isClosed()` 的判断非常具体：非空且 `first() == last()`。它不执行几何近似比较，也不检查多边形是否自相交。

```cpp
QPolygonF polygon{
    {0, 0}, {100, 0}, {80, 60}, {0, 0}
};

if (polygon.isClosed())
    painter.drawPolygon(polygon, Qt::OddEvenFill);
```

若首尾不同，`drawPolygon()` 在填充时仍会按多边形语义闭合最后一条边，但 `isClosed()` 会返回 `false`。因此“绘制时可填充”与“数据显式闭合”是两个概念。

`containsPoint(point, fillRule)` 按给定填充规则判断点是否在多边形区域内。自相交多边形的结果取决于 `Qt::OddEvenFill` 或 `Qt::WindingFill`；边界点的结果不应被当作跨平台精确几何契约来依赖，业务命中通常应加入容差或使用 stroked path。

`boundingRect()` 返回所有顶点的轴对齐包围矩形。它只反映顶点，当然不会包含任何不存在于顶点之间的曲线弯曲。

## 平移和一般变换

`translate()` 原地修改全部点，`translated()` 返回副本。两者只做平移，不做旋转、缩放或错切。

```cpp
const QPolygonF preview = polygon.translated(QPointF(12.5, 8.0));
polygon.translate(-12.5, -8.0);
```

对于一般二维变换，使用 `QTransform::map(polygon)`。如果同一个多边形需要在多个坐标系显示，优先保留原始顶点并生成变换副本，不要反复对同一对象做正向/逆向浮点变换，以免误差累积。

## 布尔运算的实际含义

`united()`、`intersected()` 和 `subtracted()` 以多边形填充区域为基础计算几何结果，返回新的 `QPolygonF`。输入最好是有效的封闭区域；开放折线、自相交轮廓、重复顶点和退化边会让结果难以解释。

结果可能包含多个轮廓或点顺序变化，不能假定返回值仍是单一、凸、按原顺序排列的多边形。需要表达孔洞和多个独立区域时，`QPainterPath` 或 `QRegion` 往往比单个 `QPolygonF` 更合适。

```cpp
QPolygonF visible = subject.intersected(viewportPolygon);
QPolygonF cut     = subject.subtracted(selectionHole);
```

若只需判断是否有交集，使用 `intersects()`，避免为了一个布尔结果创建完整结果多边形。

## 与整数 `QPolygon` 的转换

`QPolygonF(const QPolygon &)` 把整数点转换为浮点点；`toPolygon()` 则把浮点点转换回整数精度。转换回整数会发生舍入/截断造成的精度损失，不能用于要求可逆的几何编辑。

```cpp
QPolygon integerPolygon = polygon.toPolygon();
QPolygonF roundTrip(integerPolygon); // 可能已丢失小数坐标
```

使用 `QPolygonF` 作为内部模型、只在最终像素绘制或兼容旧接口时转换为 `QPolygon`，通常能减少累计误差。

## 生命周期、线程与性能

`QPolygonF` 是隐式共享值类型，复制和按值返回成本通常较低；写入共享副本时才分离。它不依赖 GUI 线程，可以在工作线程中做纯顶点计算，只要来源数据和目标对象没有并发读写冲突。

对大量点进行批量构建时，可利用 `QList` 的容量预留和连续批量操作。保存 `constData()` 返回的底层指针时，要注意任何可能改变列表的操作都可能使指针失效；更安全的做法是在一次调用期间直接传递它。

## 常见错误

- 认为创建 `QPolygonF` 会自动闭合：只有首尾相同才是 `isClosed()`。
- 用 `drawPolyline()` 期待填充：它只绘制开放折线。
- 用 `QPolygonF` 表示带曲线的路径：曲线会被迫离散成线段。
- 将 `toPolygon()` 当作无损转换：小数坐标会丢失。
- 对开放、自相交或退化多边形直接做布尔运算，却期待稳定的单轮廓结果。
- 反复原地平移、旋转、再逆变换，造成浮点误差累积。
- 保存 `constData()` 指针后继续修改顶点列表。

## API 速查表

### 构造与列表语义

| API | 语义与使用边界 |
| --- | --- |
| `QPolygonF()` | 构造空顶点列表；不自动闭合。 |
| `QPolygonF(QList<QPointF>)` | 从浮点点列表构造；点按原顺序保存。 |
| `QPolygonF(QPolygon)` | 将整数顶点转换为浮点顶点。 |
| `QPolygonF(QRectF)` | 用矩形的顶点构造多边形；用于表达矩形轮廓。 |
| `using QList<QPointF>` | 可使用 QList 的增删、索引、迭代、容量和数据访问 API；这些操作不创建路径语义。 |
| `swap(QPolygonF &)` | 高效交换两个顶点列表。 |
| `operator QVariant()` | 转换为 `QVariant`，用于通用属性/数据接口。 |

### 几何查询与变换

| API | 语义与使用边界 |
| --- | --- |
| `isClosed()` | 仅当非空且首尾点完全相等时为真；不检查自相交或有效性。 |
| `boundingRect()` | 返回所有顶点的浮点轴对齐包围盒。 |
| `containsPoint(point, fillRule)` | 按给定填充规则测试点是否在多边形区域内。 |
| `translate(offset)` / `translate(dx, dy)` | 原地平移所有顶点。 |
| `translated(offset)` / `translated(dx, dy)` | 返回平移副本，原多边形不变。 |
| `QTransform::map(QPolygonF)` | 执行旋转、缩放、错切等一般变换；应保留原始多边形减少误差。 |

### 布尔运算和精度转换

| API | 语义与使用边界 |
| --- | --- |
| `united(const QPolygonF &)` | 返回两个填充区域的并集；结果不保证单轮廓或原顶点顺序。 |
| `intersected(const QPolygonF &)` | 返回两个填充区域的交集；无交集时可能为空。 |
| `subtracted(const QPolygonF &)` | 返回本区域减去参数区域；输入最好为有效封闭轮廓。 |
| `intersects(const QPolygonF &)` | 只判断是否相交，不返回几何结果；适合快速过滤。 |
| `toPolygon()` | 转换为整数 `QPolygon`；会损失小数精度。 |

### 流和调试

| API | 语义与使用边界 |
| --- | --- |
| `QDataStream <<` / `>>` | 序列化/读取顶点列表；读取外部数据时检查流状态和点数上限。 |
| `QDebug <<` | 输出顶点列表调试信息。 |
