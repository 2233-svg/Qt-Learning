# QPolygon

> Qt 6.11.1 · Qt GUI · 来自 `QPolygon`

## 1. 先建立直觉

`QPolygon` 是一串整数坐标 `QPoint` 组成的多边形。它既可以像列表一样保存点，也可以参与绘制、命中测试和多边形集合运算。相比 `QPolygonF`，它更贴近像素网格和整数几何；相比 `QPainterPath`，它只表达折线/多边形，不表达曲线。

它最常见于 `QPainter::drawPolygon()`、`drawPolyline()`、`QRegion` 转换、简单命中测试和整数坐标的 UI 几何计算。

## 2. 类说明

- 头文件：`#include <QPolygon>`
- CMake：`Qt6::Gui`
- 基类：`QList<QPoint>`
- 点类型：`QPoint`，整数坐标
- 浮点版本：`QPolygonF`

虽然 `QPolygon` 是点列表，但集合运算如 `intersected()`、`united()`、`subtracted()` 会把它作为面积处理；即使首尾没有相同点，也按隐式闭合多边形理解。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `QPolygon()` | 创建空多边形。 |
| `QPolygon(QList<QPoint>)` | 从点列表构造。 |
| `QPolygon(QRect, bool closed=false)` | 从矩形四角构造；`closed` 为真时额外加入起点作为第五点。 |
| `boundingRect()` | 返回所有点的整数包围矩形；空多边形返回空矩形。 |
| `containsPoint(point, fillRule)` | 按填充规则判断点是否在多边形面积内。 |
| `intersects(p)` | 判断两个多边形面积是否相交或包含。 |
| `intersected(p)` | 返回交集多边形。 |
| `united(p)` | 返回并集多边形。 |
| `subtracted(p)` | 返回从当前多边形中减去 `p` 的结果。 |
| `point(index)` / `point(index, &x, &y)` | 读取指定点。 |
| `setPoint(index, ...)` | 修改指定点。 |
| `setPoints(...)` | 以整数序列一次设置全部点。 |
| `putPoints(...)` | 从可变参数或另一个 polygon 复制部分点。 |
| `translate()` | 原地平移所有点。 |
| `translated()` | 返回平移后的副本。 |
| `toPolygonF()` | Qt 6.4 起转换为浮点多边形。 |
| `operator QVariant()` | 作为 Qt 属性或 QVariant 数据传递。 |

## 4. 关键用法

### 绘制整数多边形

```cpp
QPolygon arrow;
arrow << QPoint(0, 8) << QPoint(24, 8)
      << QPoint(24, 0) << QPoint(40, 16)
      << QPoint(24, 32) << QPoint(24, 24)
      << QPoint(0, 24);

painter.drawPolygon(arrow);
```

如果只是画轮廓折线，用 `drawPolyline()`；如果要填充面积，用 `drawPolygon()` 并关注 fill rule。

### 命中测试

```cpp
if (polygon.containsPoint(mousePos, Qt::OddEvenFill))
    activateShape();
```

`containsPoint()` 不要求你显式把首点追加到尾部。它按面积判断时会隐式闭合。

### 整数与浮点转换

```cpp
QPolygonF precise = polygon.toPolygonF();
```

从浮点转回整数会丢失小数精度；从整数转浮点则只是提升坐标类型。做旋转、缩放、抗锯齿几何时通常用 `QPolygonF` 更自然。

## 5. 使用场景

- 像素对齐的简单多边形绘制。
- 鼠标命中测试和不规则区域选择。
- 与 `QRegion`、整数矩形、栅格 UI 几何配合。
- 箭头、三角形、标签角标等简单图形。
- 需要集合运算但几何精度要求不高的区域处理。

## 6. 常见坑与经验

- **它继承自 `QList<QPoint>`，但不是普通业务列表。** 几何函数会按多边形面积解释点序。
- **集合运算隐式闭合。** 首尾不相等也会被当作闭合区域处理。
- **点顺序很重要。** 自交、多环、顺逆时针都会影响填充和运算结果。
- **整数坐标会截断精度。** 变换后的几何如果需要小数，先转 `QPolygonF`。
- **`QPolygon(QRect)` 的右下角语义要注意。** 它按矩形几何构造点，不一定等同于你手写的像素包含范围。
- **复杂曲线不要硬用 polygon。** 曲线、圆角、文字轮廓更适合 `QPainterPath`。

## 7. 知识点覆盖

- 整数点列表与多边形面积语义
- 绘制、命中测试和布尔集合运算
- 隐式闭合、填充规则和自交形状
- 与 `QPolygonF`、`QPainterPath`、`QRegion` 的取舍
- 批量设置点、局部复制点和平移几何
