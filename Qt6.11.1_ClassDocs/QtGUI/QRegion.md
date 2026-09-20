# QRegion

> Qt 6.11.1 · Qt GUI · 来自 `QRegion`

## 1. 先建立直觉

`QRegion` 表示屏幕/绘制中的一个离散区域，内部通常由一组不重叠的矩形拼成。它不是任意精度的矢量路径；如果你需要贝塞尔曲线、精细浮点几何或复杂填充轮廓，用 `QPainterPath`。如果你需要裁剪、脏区、窗口 mask、矩形集合运算，`QRegion` 很合适。

它常见于 GUI 系统的“哪些地方需要重绘”“哪些地方可点击/可见”“把这块区域裁剪掉”。区域越复杂，绘制和合成成本越高，所以 `QRegion` 的使用要在精确性和复杂度之间取舍。

## 2. 类说明

- 头文件：`#include <QRegion>`
- CMake：`Qt6::Gui`
- 类型性质：隐式共享值类型，可复制、可移动、可序列化
- 内部语义：由非重叠矩形集合表示的整数区域
- 常见协作类：`QPainter`、`QPaintEvent`、`QBitmap`、`QPolygon`、`QWidget`/`QWindow` mask

从 bitmap 或 polygon 构造 region 很方便，但可能产生大量小矩形。用于裁剪或窗口遮罩时，过度复杂的 region 会拖慢绘制。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `RegionType` | 构造矩形或椭圆区域：`Rectangle`、`Ellipse`。 |
| `QRegion()` | 创建空区域。 |
| `QRegion(QRect/int..., RegionType)` | 从矩形或椭圆创建区域。 |
| `QRegion(QPolygon, FillRule)` | 从多边形创建区域，按填充规则离散化。 |
| `QRegion(QBitmap)` | 从 bitmap 中的 `color1` 像素生成区域。 |
| `contains(QPoint/QRect)` | 判断点或矩形是否完全包含在区域中。 |
| `intersects(QRect/QRegion)` | 判断是否有重叠。 |
| `intersected()` / `operator&` | 求交集。 |
| `united()` / `operator|` / `operator+` | 求并集。 |
| `subtracted()` / `operator-` | 从当前区域减去另一区域。 |
| `xored()` / `operator^` | 求异或区域。 |
| `boundingRect()` | 返回包围整个区域的矩形。 |
| `rectCount()` | 返回内部矩形数量，可用来估算复杂度。 |
| `begin()` / `end()` / `rects()` | 遍历组成区域的非重叠矩形；`rects()` 为 Qt 6.8 起 API。 |
| `setRects(QSpan<const QRect>)` | Qt 6.8 起从矩形 span 设置区域。 |
| `translate()` / `translated()` | 原地或复制平移区域。 |
| `isEmpty()` / `isNull()` | 判断是否为空或 null 语义。 |
| `toHRGN()` / `fromHRGN()` | Windows 平台与 `HRGN` 互转。 |

## 4. 关键用法

### 裁剪绘制区域

```cpp
QRegion clip = QRegion(rect()).subtracted(sidebarRect);

QPainter p(this);
p.setClipRegion(clip);
drawMainContent(&p);
```

裁剪可以减少不该绘制的区域，也可以保护 UI 层级。但复杂 region 会增加后端处理成本。

### 处理重绘脏区

```cpp
void Widget::paintEvent(QPaintEvent *event)
{
    for (const QRect &r : event->region())
        repaintTile(r);
}
```

`QPaintEvent::region()` 通常告诉你这次需要重绘的区域。按 region 分块绘制可以避免整窗重画。

### 区域布尔运算

```cpp
QRegion visible = viewportRegion.intersected(contentRegion);
QRegion invalid = oldRegion.xored(newRegion);
```

`QRegion` 的优势就是集合运算。与 `QPolygon` / `QPainterPath` 不同，它的结果是离散矩形区域，更贴近绘制系统的脏区和 clip。

## 5. 使用场景

- `QPainter` 裁剪区域。
- QWidget 重绘脏区优化。
- 不规则窗口 mask 或 pixmap mask。
- 局部无效区域合并、相交、相减。
- 从位图或多边形生成可见/可点击区域。
- Windows 平台与 `HRGN` 互操作。

## 6. 常见坑与经验

- **region 是整数离散区域。** 它没有浮点精度，也不保存曲线语义。
- **复杂 region 可能很慢。** 从 bitmap 逐像素生成的区域可能包含大量矩形，裁剪和绘制成本明显增加。
- **`boundingRect()` 只是外框。** 它可能包含 region 外部的空洞，不可当成精确包含判断。
- **遍历得到的是矩形分解。** 矩形顺序和分解方式不应作为稳定业务语义依赖。
- **`contains(QRect)` 是完全包含。** 判断有无交集用 `intersects()`。
- **`isEmpty()` 与 `isNull()` 语义要区分。** 业务上通常更关心是否为空，但底层状态可能还有 null 概念。
- **窗口 mask 不等于透明绘制。** mask 影响可见/可交互区域，透明像素则是绘制内容的 alpha。

## 7. 知识点覆盖

- 矩形集合表示的离散区域模型
- 裁剪、脏区、窗口 mask 和位图 mask
- 区域并、交、差、异或运算
- 多边形/位图到区域的复杂度成本
- `boundingRect()`、`rectCount()`、矩形遍历和 Qt 6.8 `QSpan` API
- Windows `HRGN` 互操作边界
