# QPolygonF

> Qt 6.11.1 · Qt GUI · 来自 `QPolygonF`

## 1. 先建立直觉

`QPolygonF` 是由 `QPointF` 组成的浮点多边形。它适合需要小数坐标、缩放旋转、抗锯齿绘制、精细命中测试的场景。和 `QPolygon` 一样，它本质上是点列表；和 `QPainterPath` 不同，它不表达曲线，只表达直线连接的多边形或折线。

当几何来自布局比例、动画插值、变换矩阵、缩放后的图形，优先用 `QPolygonF`。如果过早转成 `QPolygon`，小数会丢失，形状可能抖动、边缘不平滑，命中区域也会出现误差。

## 2. 类说明

- 头文件：`#include <QPolygonF>`
- CMake：`Qt6::Gui`
- 基类：`QList<QPointF>`
- 点类型：`QPointF`，浮点坐标
- 整数版本：`QPolygon`

`QPolygonF` 的集合运算同样把多边形视为面积，未显式闭合的点序也会被隐式闭合。`isClosed()` 只检查首尾点是否相等，不代表集合运算是否会把它当成闭合区域。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `QPolygonF()` | 创建空浮点多边形。 |
| `QPolygonF(QList<QPointF>)` | 从浮点点列表构造。 |
| `QPolygonF(QPolygon)` | 从整数多边形提升为浮点多边形。 |
| `QPolygonF(QRectF)` | 从浮点矩形构造闭合多边形。 |
| `boundingRect()` | 返回浮点包围矩形。 |
| `containsPoint(point, fillRule)` | 按填充规则判断点是否位于多边形面积内。 |
| `intersects(p)` | 判断两个多边形面积是否相交或包含。 |
| `intersected(p)` | 返回交集。 |
| `united(p)` | 返回并集。 |
| `subtracted(p)` | 返回当前多边形减去另一个多边形的结果。 |
| `isClosed()` | 判断首点和尾点是否相等。 |
| `translate()` | 原地平移所有点。 |
| `translated()` | 返回平移后的副本。 |
| `toPolygon()` | 转成整数 `QPolygon`，小数会被转换/舍入为整数点。 |
| `operator QVariant()` | 作为 Qt 属性或 QVariant 数据传递。 |

## 4. 关键用法

### 用浮点坐标绘制抗锯齿图形

```cpp
QPolygonF diamond;
diamond << QPointF(40.5, 0.5)
        << QPointF(80.5, 40.5)
        << QPointF(40.5, 80.5)
        << QPointF(0.5, 40.5);

painter.setRenderHint(QPainter::Antialiasing);
painter.drawPolygon(diamond);
```

浮点坐标让你可以精确控制亚像素位置。对于抗锯齿图形，这通常比整数坐标更可控。

### 变换后保持精度

```cpp
QPolygonF transformed = transform.map(originalPolygonF);
```

旋转、缩放、斜切都会产生小数坐标。用 `QPolygonF` 接住结果，能避免每一步都把误差量化到整数。

### 判断是否显式闭合

```cpp
if (!poly.isClosed())
    poly << poly.first();
```

这只是在点列表层面添加尾点。注意：`containsPoint()` 和集合运算即使在 `isClosed() == false` 时，也会把形状当作隐式闭合面积。

## 5. 使用场景

- 缩放/旋转/动画中的多边形几何。
- 抗锯齿绘制和高 DPI 下的亚像素定位。
- 图形编辑器里的节点、锚点、选择框。
- 从 `QPainterPath` 扁平化得到的多边形近似。
- 地图、图表、CAD 等需要浮点坐标的二维几何。

## 6. 常见坑与经验

- **`isClosed()` 不是面积判断开关。** 它只看首尾点是否相等，集合运算仍按闭合面积处理。
- **转成 `QPolygon` 会损失精度。** 尽量在最后一步、确实需要整数像素时再转换。
- **浮点比较要谨慎。** 首尾点因为计算误差可能视觉重合但 `isClosed()` 为 false。
- **复杂曲线仍然不适合 polygon。** 贝塞尔、圆角、文字轮廓用 `QPainterPath` 表达更自然。
- **点序影响填充结果。** 自交形状要明确 `OddEvenFill` 或 `WindingFill`。
- **集合运算结果可能改变点序和结构。** 不要依赖结果仍保持原来的顶点排列。

## 7. 知识点覆盖

- 浮点多边形与整数多边形的精度差异
- 亚像素绘制、高 DPI 和抗锯齿
- 显式闭合与隐式闭合面积语义
- 命中测试、布尔运算和填充规则
- 几何变换后的误差控制
- 与 `QPolygon`、`QPainterPath` 的选择边界
