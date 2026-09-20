# QPen

> Qt 6.11.1 · Qt GUI · 来自 `QPen`

## 1. 先建立直觉

`QPen` 描述如何描绘路径轮廓：颜色或画刷、线宽、实线/虚线、端点样式、折角连接方式和 miter 限制。它决定的是路径“边缘长什么样”，不是路径内部填充。

一支 pen 不只是“颜色加宽度”。放大画布后线是否变粗、虚线是否按宽度同比例放大、尖角是否拉出长刺、线段末端是否圆润，都由 `QPen` 的具体设置决定。

## 2. 类说明

`QPen` 是值类型，常配合 `QPainter::setPen()`、`drawLine()`、`drawPath()`、`drawRect()` 使用。它内部用一个 `QBrush` 填充笔触，因此描边也可以是渐变或纹理，而不只是一种纯色。

类说明只用于表明这些 API 来自 `QPen`：填充属性由 `QBrush` 表达，路径几何由 `QPainterPath` 或图元提供，实际坐标缩放由 painter transform 决定。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QPen()` | 构造默认黑色、宽 1、实线的画笔。 |
| `QPen(color)` | 构造指定颜色的实线画笔。 |
| `QPen(style)` | 构造指定线型的黑色画笔。 |
| `QPen(brush, width, style, cap, join)` | 完整构造画笔，支持渐变/纹理描边。 |
| `brush()` / `setBrush()` | 查询或设置笔触填充画刷。 |
| `color()` / `setColor()` | 查询或设置纯色描边颜色。 |
| `width()` / `widthF()` | 查询整数或浮点逻辑线宽。 |
| `setWidth()` / `setWidthF()` | 设置逻辑线宽；0 表示 cosmetic pen。 |
| `isCosmetic()` / `setCosmetic()` | 查询或设置是否保持设备像素宽度。 |
| `style()` / `setStyle()` | 查询或设置 Solid、Dash、Dot、DashDot、CustomDash 等线型。 |
| `dashPattern()` / `setDashPattern()` | 查询或设置自定义虚线与间隙序列。 |
| `dashOffset()` / `setDashOffset()` | 查询或设置虚线图案起始偏移，可用于流动动画。 |
| `capStyle()` / `setCapStyle()` | 设置线段端点为 Flat、Square、Round。 |
| `joinStyle()` / `setJoinStyle()` | 设置折角为 Miter、Bevel、Round。 |
| `miterLimit()` / `setMiterLimit()` | 限制 MiterJoin 尖角最大伸出长度。 |
| `isSolid()` | 判断是否为实线。 |
| `swap(other)` | 高效交换画笔。 |
| `operator==` / `operator!=` | 比较画笔配置。 |

## 4. 关键用法

### 普通逻辑线宽随缩放变化

```cpp
QPen pen(QColor("#0f172a"));
pen.setWidthF(2.0);
painter.setPen(pen);

painter.scale(2.0, 2.0);
painter.drawLine(QPointF(0, 0), QPointF(80, 0));
```

这类非 cosmetic pen 会随 painter 的缩放放大。它适合 CAD、矢量图、流程图等“线条属于场景”的绘制。

### cosmetic pen 保持屏幕像素宽度

```cpp
QPen gridPen(QColor(100, 116, 139, 120));
gridPen.setWidth(0);
gridPen.setCosmetic(true);
painter.setPen(gridPen);
```

cosmetic pen 无论缩放多少，视觉上通常保持约一个设备像素宽，适合辅助网格、选择框、参考线。它不适合需要随导出比例或打印比例变粗的正式图形。

### 用 cap 和 join 控制线条风格

```cpp
QPen stroke(QColor("#2563eb"), 8);
stroke.setCapStyle(Qt::RoundCap);
stroke.setJoinStyle(Qt::RoundJoin);
painter.setPen(stroke);
painter.drawPath(path);
```

RoundCap 让线段末端圆润，RoundJoin 让折角平滑，常用于手写笔迹、地图路径和圆角图标。SquareCap 会比终点多延长半个线宽，做精确对齐时要算进去。

### 自定义虚线按“笔宽单位”定义

```cpp
QPen dashed(QColor("#334155"), 2.0);
dashed.setDashPattern({3.0, 1.5});
dashed.setDashOffset(m_dashPhase);
painter.setPen(dashed);
```

这里 3.0 和 1.5 是笔宽倍数，不是固定屏幕像素。线宽从 2 变为 4 时，虚线和间隙都会放大两倍。动画虚线时只更新 `dashOffset()` 即可。

### MiterJoin 要设置合理上限

```cpp
pen.setJoinStyle(Qt::MiterJoin);
pen.setMiterLimit(3.0);
```

尖锐夹角下 miter 会拉得很长。miter limit 超出后 Qt 会退化处理，避免出现针刺般的长角。地图、折线图、机械图纸应根据线宽和角度验证视觉效果。

## 5. 使用场景

`QPen` 适合图形轮廓、连接线、图表曲线、选区边框、手写轨迹、CAD 辅助线、地图路径、虚线边界、网格、标尺和打印输出。

渐变 `QBrush` 作为 pen 适合光谱曲线、热度描边或装饰线，但高对比数据图形通常使用稳定纯色更易读。

## 6. 常见坑与经验

不要把线宽 0 理解为“不画线”。它表示 cosmetic pen，通常仍会绘制一设备像素宽的线。

不要把 dash pattern 写成奇数项、负数或零值。应使用偶数个正数，交替表示实线段和间隙。

不要忘记 cap 会改变可见长度。FlatCap、SquareCap、RoundCap 在线端视觉范围不同。

不要在缩放场景里无意使用 cosmetic pen。导出高分辨率图片或打印时，它的固定像素宽度可能显得过细。

不要只调颜色不调 join。复杂折线的锯齿、尖刺、交汇不自然，往往是 join/miter 而不是抗锯齿的问题。

不要假设 `setStyle()` 会保留虚线 offset。切换 style 时虚线相关状态可能重置，动画逻辑要重新设置。

## 7. 知识点覆盖

学习 `QPen` 应覆盖逻辑线宽、浮点线宽、cosmetic pen、实线与虚线、dash pattern、dash offset、cap、join、miter limit、渐变描边、缩放与打印、路径轮廓质量。
