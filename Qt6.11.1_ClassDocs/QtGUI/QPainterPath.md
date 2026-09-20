# QPainterPath

> Qt 6.11.1 · Qt GUI · 来自 `QPainterPath`

## 1. 先建立直觉

`QPainterPath` 是 Qt 的二维矢量路径容器。它把移动、直线、二次/三次贝塞尔曲线、闭合子路径、文字轮廓、矩形、椭圆等图形统一成一串路径元素。`QPainter` 可以直接 `drawPath()`，也可以用它做命中测试、布尔运算、路径动画、裁剪和复杂填充。

把它看成“比 `QPolygonF` 更有表达力、比 `QPainter` 状态更持久”的几何对象。`QPainter` 负责把当前状态画出来，`QPainterPath` 负责描述形状本身。

## 2. 类说明

- 头文件：`#include <QPainterPath>`
- CMake：`Qt6::Gui`
- 内部元素：`MoveToElement`、`LineToElement`、`CurveToElement`、`CurveToDataElement`
- 类型性质：隐式共享值类型，Qt 6.10 起支持移动构造和路径长度缓存控制
- 常见协作类：`QPainter`、`QPainterPathStroker`、`QTransform`、`QRegion`、`QPolygonF`

`QPainterPath` 可以包含多个子路径。`moveTo()` 会开始新子路径，`closeSubpath()` 会把当前子路径闭合，`connectPath()` 则会尝试用线段把两个路径连接起来。填充效果由 `fillRule()` 决定，常见选择是奇偶填充和 winding 填充。

## 3. API 速查

| API 族 | 作用 |
| --- | --- |
| `QPainterPath()` / `QPainterPath(startPoint)` | 创建空路径，或从指定起点开始。 |
| `moveTo()` / `lineTo()` | 移动当前点，或添加直线段。 |
| `quadTo()` / `cubicTo()` | 添加二次/三次贝塞尔曲线。 |
| `arcMoveTo()` / `arcTo()` | 按椭圆矩形和角度移动或添加弧线。 |
| `closeSubpath()` | 闭合当前子路径，并把当前位置回到子路径起点。 |
| `addRect()` / `addEllipse()` / `addRoundedRect()` | 追加常见闭合形状。 |
| `addPolygon()` / `addRegion()` / `addText()` | 把多边形、区域或文字轮廓加入路径。 |
| `addPath()` / `connectPath()` | 合并路径；前者追加子路径，后者可连接当前位置。 |
| `currentPosition()` | 查询当前绘制位置。 |
| `elementCount()` / `elementAt()` | 读取底层路径元素，适合编辑器和导出器。 |
| `setElementPositionAt()` | 修改指定元素坐标。 |
| `boundingRect()` | 返回紧贴绘制结果的边界矩形。 |
| `controlPointRect()` | 返回控制点边界，计算更快但可能更松。 |
| `contains()` / `intersects()` | 对点、矩形或路径做命中和相交判断。 |
| `united()` / `intersected()` / `subtracted()` | 路径布尔运算；运算结果按填充区域理解。 |
| `operator+` / `operator|` / `operator&` / `operator-` | 对追加、并、交、差的运算符写法。 |
| `length()` / `pointAtPercent()` / `angleAtPercent()` | 沿路径取长度、点和方向，用于路径动画。 |
| `percentAtLength()` / `trimmed()` | 按长度映射百分比；Qt 6.10 起可截取路径片段。 |
| `toFillPolygon(s)` / `toSubpathPolygons()` | 将路径扁平化为多边形，常用于低层几何或调试。 |
| `translate()` / `translated()` | 原地或复制后平移路径。 |
| `setFillRule()` / `fillRule()` | 控制重叠区域如何填充。 |
| `reserve()` / `capacity()` | 为大量元素预分配空间。 |
| `setCachingEnabled()` | Qt 6.10 起控制长度等计算的缓存。 |

## 4. 关键用法

### 构造可填充的复杂图形

```cpp
QPainterPath badge;
badge.addRoundedRect(QRectF(0, 0, 160, 64), 12, 12);
badge.moveTo(20, 64);
badge.lineTo(32, 82);
badge.lineTo(44, 64);
badge.closeSubpath();

painter.setBrush(QColor("#2f80ed"));
painter.setPen(Qt::NoPen);
painter.drawPath(badge);
```

路径本身只保存几何。颜色、线宽、抗锯齿和透明度由绘制时的 `QPainter` 状态决定。

### 用路径做命中测试

```cpp
if (shape.contains(mousePosition))
    setHovered(true);
```

对不规则图形，`contains()` 比用矩形包围盒判断更准确。注意它按填充区域判断，因此 `fillRule()` 会影响结果。

### 路径动画：沿曲线移动

```cpp
const qreal t = progress; // 0.0 到 1.0
const QPointF pos = path.pointAtPercent(t);
const qreal angle = path.angleAtPercent(t);
```

`pointAtPercent()` 的参数不是严格的“长度比例线性参数”直觉，复杂曲线下速度可能不完全均匀。需要更接近按长度匀速时，可用 `length()` 和 `percentAtLength()` 做映射。

### 布尔运算做遮罩和组合

```cpp
QPainterPath ring = outer.subtracted(inner);
QPainterPath clipped = ring.intersected(viewportPath);
```

布尔运算把路径当成填充区域处理，不是单纯处理轮廓线。如果你想对线条本身做区域运算，先用 `QPainterPathStroker` 把线条转换为可填充轮廓。

## 5. 使用场景

- 自定义控件：圆角标签、仪表盘、气泡、复杂按钮外形。
- 矢量图形：图标、路径动画、可缩放插画。
- 文本轮廓：`addText()` 后做渐变填充、描边或几何变形。
- 命中检测：不规则可点击区域、图形编辑器对象选择。
- 裁剪和遮罩：用路径限制绘制区域或生成 alpha mask。
- 几何运算：合并、相交、相减复杂区域。

## 6. 常见坑与经验

- **路径不是画笔状态。** 同一个路径可以被不同 pen/brush 画出完全不同效果。
- **`addPolygon()` 不会自动闭合。** 如果需要最后一点连回第一点，调用 `closeSubpath()`。
- **`boundingRect()` 和 `controlPointRect()` 不同。** 前者更贴近实际曲线边界，后者基于控制点通常更快但更大。
- **布尔运算看填充区域。** 线段本身没有面积；想处理描边区域要先 stroker。
- **便利形状会展开成路径元素。** 添加矩形或文字后，底层只剩 move/line/curve 元素，不保留原始高层类型。
- **路径长度计算可能有成本。** 对频繁动画的复杂路径，Qt 6.10 起可考虑开启缓存，但修改路径后要意识到缓存会更新。
- **填充规则影响命中和绘制。** 自交路径、洞、重叠子路径尤其要明确使用 `OddEvenFill` 还是 `WindingFill`。

## 7. 知识点覆盖

- 子路径、当前点、闭合路径和连接路径
- 贝塞尔曲线、圆弧、文字轮廓和便利形状的统一表达
- 路径元素遍历与路径编辑器实现
- 填充规则、命中测试、包围盒和控制点边界
- 路径布尔运算、描边区域转换和裁剪
- 路径长度采样、动画、截取和缓存策略
