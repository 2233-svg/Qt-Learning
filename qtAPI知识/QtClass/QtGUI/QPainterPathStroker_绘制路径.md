# QPainterPathStroker：把路径描边转换为可填充轮廓

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QPainterPathStroker>`  
> CMake：`find_package(Qt6 REQUIRED COMPONENTS Gui)`，并链接 `Qt6::Gui`  
> 相关类型：`QPainterPath`、`QPen`、`QBrush`、`QPainter`

`QPainterPathStroker` 根据宽度、端点样式、连接样式、虚线模式和曲线离散精度，把一条 `QPainterPath` 的“描边”转换成另一个**可填充的路径**。它不是实际绘制器；`createStroke()` 只生成几何轮廓，之后可交给 `QPainter::fillPath()`、`contains()` 或路径布尔运算使用。

它适合将线条变成真实面积：例如扩大细线的命中区域、把笔划导出为矢量轮廓、制作描边文字或在没有原生 stroke 支持的后端中填充描边。

## 它解决的问题

`QPainter::strokePath(path, pen)` 会直接画出一条线，但不会提供线条所覆盖的几何区域。许多工作需要后者：

- 点击命中测试不能只判断鼠标是否恰好在线的数学中心线上；
- 矢量导出需要把“笔宽 4 的曲线”转换为多边形轮廓；
- 想对描边本身应用渐变、纹理、裁剪或路径布尔操作；
- 某些后端只支持填充路径，不支持原生笔划。

`QPainterPathStroker` 将中心路径两侧各扩展约一半宽度，并按端点、连接和虚线规则构造封闭路径。

## 实际使用场景

### 1. 为细线增加点击容差

```cpp
QPainterPath connection;
connection.moveTo(QPointF(40, 60));
connection.cubicTo(QPointF(160, 30), QPointF(240, 180), QPointF(360, 120));

QPainterPathStroker hitStroker;
hitStroker.setWidth(14.0);

const QPainterPath hitArea = hitStroker.createStroke(connection);
const bool selected = hitArea.contains(mousePosition);
```

视觉上可以仍用 2 px 的笔画线；命中测试另用 14 单位宽的轮廓。这样不会把交互容差与视觉样式绑死。

### 2. 将描边作为渐变填充的矢量形状

```cpp
QPainterPathStroker stroker;
stroker.setWidth(10.0);
stroker.setCapStyle(Qt::RoundCap);
stroker.setJoinStyle(Qt::RoundJoin);

const QPainterPath outline = stroker.createStroke(path);

QLinearGradient gradient(outline.boundingRect().topLeft(),
                         outline.boundingRect().bottomRight());
gradient.setColorAt(0.0, QColor("#27b5d6"));
gradient.setColorAt(1.0, QColor("#f1c744"));

painter.fillPath(outline, gradient);
```

此时渐变填充的是描边覆盖的面积，而不是原中心路径。它与 `strokePath()` 的笔样式绘制是两种不同工作流。

### 3. 将 `QPen` 样式迁移到轮廓生成器

```cpp
QPen pen(Qt::black, 5.0, Qt::DashDotLine,
         Qt::RoundCap, Qt::MiterJoin);
pen.setMiterLimit(3.0);

QPainterPathStroker stroker(pen);
const QPainterPath dashedOutline = stroker.createStroke(path);
```

传入 `QPen` 的构造函数适合让轮廓几何与已有的绘制笔设置保持一致；之后还可单独调整 stroker 的属性。

## 核心模型与边界

### 输出是“轮廓面积”，不是原路径的副本

`createStroke(path)` 返回一条新路径，表示输入路径若按当前描边参数绘制时所占的可填充面积。输出路径用于描边用途，Qt 文档明确提示不应把它当作原路径的普通替代品，否则可能得到意外行为。

生成的轮廓默认需要 `Qt::WindingFill` 填充规则，Qt 已为它设置该规则。不要把它随意改成 `OddEvenFill` 后期待所有自交、折返和虚线场景仍与 `QPen` 描边一致。

### 宽度是几何宽度

`setWidth(width)` 设置轮廓总宽度，结果大约从原路径中心线的每侧扩展 `width / 2`。它不是 `QPen` 的 cosmetic pen 概念：如果目标是“无论缩放如何都保持一个设备像素”的视觉线条，应让 `QPainter` / 设备处理 cosmetic pen；若目标是稳定的路径几何或命中区域，则为 stroker 设定明确的几何宽度。

### 端点和连接

端点样式控制开放子路径和每段虚线的两端：

- `Qt::FlatCap`：端点截在中心路径终点；
- `Qt::SquareCap`：端点沿路径方向延伸；
- `Qt::RoundCap`：端点为半圆。

连接样式控制折线和曲线片段交汇处：

- `Qt::BevelJoin`：切平尖角；
- `Qt::RoundJoin`：圆滑过渡；
- `Qt::MiterJoin`：尖角延长，受 miter limit 约束。

虚线开启时，每一个“有墨段”也会应用端点样式，因此圆端虚线的有效可见长度会与平端虚线不同。

### Miter limit 只作用于尖角连接

`miterLimit` 的单位是当前 `width` 的倍数，实际可延伸距离约为：

```text
miterLimit * width
```

它只在连接样式为 `Qt::MiterJoin` 时有效。尖角很小且 miter limit 很大时，轮廓可能产生长而尖的突出部分；图编辑器、路径命中测试和可视区域估算都应把它考虑进去。

### 虚线数组与 offset

`setDashPattern(const QList<qreal> &)` 中的元素依次表示：

```text
实线长度, 空白长度, 实线长度, 空白长度, ...
```

列表允许奇数个元素；循环重复时，最后一个元素会按第一个元素的长度扩展。`setDashOffset()` 改变图案沿路径的起始相位，适用于行军蚂蚁选区、流动连接线和同步的虚线动画。

虚线模式的尺度遵循 `QPen` 的虚线语义。若笔宽或路径变换会变化，不要把数组中的数值简单视为固定屏幕像素。

### 曲线阈值是精度与复杂度的权衡

stroker 需要把曲线处理为轮廓。`curveThreshold` 控制曲线扁平化粒度：

- 默认值为 `0.25`，通常已平衡质量和性能；
- 值更小，曲线外观更平滑，但生成路径会更复杂；
- 没有明显锯齿或几何误差时，不要为了“更精确”盲目降低阈值。

频繁编辑的大型曲线路径若每帧重新 `createStroke()`，小阈值会显著增加 CPU 与内存压力。应在参数或原路径改变后缓存结果，或在交互过程中采用更粗的预览。

### 生命周期与线程

`QPainterPathStroker` 是独立值对象，不依赖窗口、事件循环或 `QPainter` 活跃状态。`createStroke()` 返回独立的 `QPainterPath` 值。

不过，同一实例不应由多个线程同时修改；多线程生成轮廓时，每个线程使用独立 stroker 和独立路径数据。若路径来自仍在 GUI 线程编辑的模型，先复制稳定快照再交给后台计算。

## 关键 API 语义

### `createStroke()`

```cpp
QPainterPathStroker stroker;
stroker.setWidth(8.0);

const QPainterPath outline = stroker.createStroke(centerLine);
painter.fillPath(outline, Qt::red);
```

`createStroke()` 不会画到任何设备上，也不会修改传入路径。每次调用都按当前的宽度、cap、join、虚线、曲线阈值和 miter limit 生成新几何。

### 使用预定义或自定义虚线

```cpp
stroker.setDashPattern(Qt::DashLine);
stroker.setDashOffset(0.5);

stroker.setDashPattern({ 3.0, 1.0, 0.5, 1.0 });
```

`Qt::PenStyle` 重载适合常见线型。列表重载适合图纸规范、选区动画或有特定节奏的连接线。传入列表时应交替提供“实线、空白”；不要把它当成一组绝对坐标。

### 从 `QPen` 构造

```cpp
QPen pen(Qt::blue);
pen.setWidthF(3.5);
pen.setCapStyle(Qt::RoundCap);
pen.setJoinStyle(Qt::RoundJoin);

QPainterPathStroker stroker(pen);
```

构造时复制 `QPen` 的相关描边参数。之后修改原 `pen` 不会回写到既有 stroker；需要新的样式时重新设置 stroker 或重新构造它。

## 常见错误

### 把轮廓当作原路径做任意几何操作

生成路径是为“描边面积”服务的，含有描边展开和可能的自交细节。需要编辑原曲线、计算中心线长度或保存语义化矢量数据时，保留原 `QPainterPath`，把轮廓视为派生产物。

### 忽略输出的 `WindingFill`

用输出路径填充时，保持 `Qt::WindingFill`。随意改成奇偶填充可能使自交、复合路径或虚线轮廓出现孔洞或填充不一致。

### `MiterJoin` 配合过大的 miter limit

锐角折线会生成极长尖刺，既影响视觉也扩大命中区域。对用户可编辑的路径，设定合理上限，或在锐角场景选择 `BevelJoin` / `RoundJoin`。

### 每次鼠标移动都生成高精度轮廓

这会让路径编辑器在复杂曲线上卡顿。交互中使用较宽松阈值或缓存，停止拖动后再生成最终精度的结果。

## API 速查表

| API | 说明 | 使用时重点 |
| --- | --- | --- |
| `QPainterPathStroker()` | 创建具有默认描边参数的 stroker。 | 随后显式设置 `width`、cap、join 等关键视觉参数。 |
| `QPainterPathStroker(const QPen &pen)` | 从 `QPen` 复制描边相关设置创建 stroker。 | 适合与现有 `QPainter` 笔样式对齐；之后与原 `QPen` 相互独立。 |
| `~QPainterPathStroker()` | 销毁 stroker。 | 不管理输入路径或 `createStroke()` 返回的路径。 |
| `createStroke(const QPainterPath &path) const` | 生成输入路径的可填充描边轮廓。 | 输出用于 outline / hit-test / fill；保留其 winding fill 规则。 |
| `setWidth(qreal width)` | 设置生成轮廓的总几何宽度。 | 轮廓约向中心线两侧各扩展一半宽度；不等同 cosmetic pen。 |
| `width() const` | 返回当前轮廓宽度。 | 用于计算包围范围和 miter 实际上限。 |
| `setCapStyle(Qt::PenCapStyle style)` | 设置开放路径和虚线段的端点形状。 | 每个虚线实段同样受 cap 影响。 |
| `capStyle() const` | 返回当前端点样式。 | 常见选择：`FlatCap`、`SquareCap`、`RoundCap`。 |
| `setJoinStyle(Qt::PenJoinStyle style)` | 设置拐点连接形状。 | `MiterJoin` 才受 miter limit 影响。 |
| `joinStyle() const` | 返回当前连接样式。 | 尖角路径常选 `RoundJoin` 或受控 `MiterJoin`。 |
| `setMiterLimit(qreal limit)` | 设置 miter 可延伸的宽度倍数。 | 实际量级约为 `limit * width`，仅用于 `MiterJoin`。 |
| `miterLimit() const` | 返回当前 miter limit。 | 调整宽度后要重新评估尖刺范围。 |
| `setDashPattern(Qt::PenStyle style)` | 采用 Qt 预定义虚线样式。 | 适合 `DashLine`、`DotLine`、`DashDotLine` 等。 |
| `setDashPattern(const QList<qreal> &pattern)` | 设置自定义实线/空白交替数组。 | 奇数长度列表会扩展末项；按 `QPen` 虚线尺度解释。 |
| `dashPattern() const` | 返回当前虚线数组。 | 用于保存和调试当前描边配置。 |
| `setDashOffset(qreal offset)` | 设置虚线图案沿路径的相位偏移。 | 用于动画时逐步改变 offset，而不是重建图案。 |
| `dashOffset() const` | 返回当前虚线偏移。 | 与 `dashPattern()` 配合读取。 |
| `setCurveThreshold(qreal threshold)` | 设置曲线扁平化阈值。 | 默认 `0.25` 通常合适；降低值会提高曲线平滑度和几何复杂度。 |
| `curveThreshold() const` | 返回当前曲线阈值。 | 排查曲线描边质量和性能时读取。 |

## 与相邻类型的分工

| 需求 | 推荐类型 |
| --- | --- |
| 保存、编辑中心线和闭合图形 | `QPainterPath` |
| 直接画出笔划 | `QPainter::strokePath()` 或 `QPainter::drawPath()` + `QPen` |
| 把笔划变成可填充几何 | `QPainterPathStroker::createStroke()` |
| 设置普通描边的颜色、宽度、cap、join、虚线 | `QPen` |
| 填充生成的轮廓 | `QPainter::fillPath()` + `QBrush` |

一句话记忆：`QPainterPathStroker` 不画线，它把“怎样画这条线”的笔样式转换成“这条线实际覆盖了哪些面积”的路径。
