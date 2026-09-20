# QFontMetricsF

> Qt 6.11.1 · Qt GUI · 来自 `QFontMetricsF`

## 1. 先建立直觉

`QFontMetricsF` 与 `QFontMetrics` 解决同一类问题，但把所有几何结果保留为 `qreal`。它适合缩放、旋转、PDF、矢量绘制和高 DPI 的连续坐标系，避免“每次测量先取整、累计后偏一像素”的小误差。

选择它的理由不是“浮点一定更精确”，而是你的后续几何本来就是浮点：例如文字与路径、`QTransform` 或 `QRectF` 相互计算。若最终控件尺寸和像素栅格就是整数，`QFontMetrics` 更直接。

## 2. 类说明

- 头文件：`#include <QFontMetricsF>`
- CMake：`target_link_libraries(app PRIVATE Qt6::Gui)`
- 类型：值类型，可由 `QFont`、`QPaintDevice`、`QFontMetrics` 或同类对象构造。
- 与 `QFontMetrics` 的函数族几乎一一对应，但返回 `qreal`、`QRectF`、`QSizeF`。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QFontMetricsF(font[, device])` | 创建与字体、设备匹配的浮点度量 |
| `QFontMetricsF(QFontMetrics)` | 将整数度量转换成浮点接口 |
| `ascent()` / `descent()` / `height()` | 浮点形式的基线与行高 |
| `leading()` / `lineSpacing()` | 浮点行间距与基线间距 |
| `capHeight()` / `xHeight()` | 大写高度与 x 高度，用于视觉几何 |
| `horizontalAdvance()` | 获取文本的逻辑前进距离 |
| `boundingRect()` | 获取文本墨迹的浮点包围框 |
| `tightBoundingRect()` | 获取较紧凑的墨迹框 |
| `boundingRect(rect, flags, text, ...)` | 测量指定浮点区域内的对齐、换行文字 |
| `size(flags, text, ...)` | 按文本标志返回 `QSizeF` |
| `elidedText(text, mode, width)` | 按浮点像素宽度生成省略文本 |
| `leftBearing()` / `rightBearing()` | 查询字形突出逻辑起止位置的距离 |
| `averageCharWidth()` / `maxWidth()` | 估算列宽或上限宽度 |
| `inFont()` / `inFontUcs4()` | 检查单个字符覆盖 |
| `overlinePos()` / `underlinePos()` / `strikeOutPos()` / `lineWidth()` | 以浮点坐标绘制文字装饰 |
| `fontDpi()` | 查询该度量依附设备的 DPI |
| `minLeftBearing()` / `minRightBearing()` | 获取字体全局最小 bearing，可能较慢 |
| `swap()` / 比较与赋值运算符 | 管理值对象 |

## 4. 关键用法

### 在缩放画布中对齐文字

```cpp
QFontMetricsF fm(painter.font());
const qreal baseline = target.center().y()
                     - (fm.ascent() + fm.descent()) / 2.0
                     + fm.ascent();
const qreal x = target.center().x()
              - fm.horizontalAdvance(label) / 2.0;
painter.drawText(QPointF(x, baseline), label);
```

这段代码以基线而不是 `boundingRect().top()` 居中。对包含不同字母、不同文字系统的文字，基线通常更稳定；如果你追求“视觉中心”而非排版中心，则可根据 `capHeight()` 或实际 `tightBoundingRect()` 进一步调整。

### 用同一规则测量并绘制多行文本

```cpp
QTextOption option(Qt::AlignLeft);
option.setWrapMode(QTextOption::WordWrap);

QFontMetricsF fm(font);
const QRectF needed = fm.boundingRect(text, option);
const QRectF box(0, 0, availableWidth, needed.height());

painter.drawText(box, text, option);
```

`QTextOption` 重载自 Qt 6.3 起提供，适合将换行模式、方向和对齐集中在一个对象中。`boundingRect()` 与 `drawText()` 要共享同一 `QTextOption`，否则不保证尺寸一致。

### 旋转文字前保留真实包围框

```cpp
const QRectF ink = fm.tightBoundingRect(text);
QTransform rotation;
rotation.rotate(-45.0);
const QRectF rotated = rotation.mapRect(ink);
```

`QRectF` 与 `QTransform` 组合时避免提前取整。最后真正需要像素区域，例如传给 `QRegion` 或图像分配时，再选择 `toAlignedRect()` 或明确的取整策略。

## 5. 使用场景

- `QGraphicsView`、自定义画布、缩放预览和矢量图导出。
- PDF/打印排版、页面网格、带旋转或变换的图表标签。
- 高 DPI 下反复累积的文本列宽、刻度、对齐辅助线。
- 需要与 `QRectF`、`QPointF`、`QPainterPath` 保持同一坐标域的自绘文字。

## 6. 常见坑与经验

- **浮点不会绕过字体栅格化。** 字体最终仍可能被平台按像素 hinting；`QFontMetricsF` 只是避免你的几何计算过早丢失小数。
- **不要每一步 `round()`。** 多列布局应累积 `qreal`，在输出边界统一取整，否则会出现间隔不均。
- **`boundingRect()` 与 `horizontalAdvance()` 的职责不同。** 前者是墨迹范围，后者是下一段内容的逻辑起点。
- **构造后不会追踪字体变化。** 改了 `QFont`、DPI 或绘制设备后，重建度量对象。
- **单字符测量不能实现编辑器。** 双向文本、组合字符、连字的插入位置要由 `QTextLayout` 或文本控件管理。
- **`QFontMetricsF(QFontMetrics)` 不会创造原始精度。** 若源对象已经按整数环境建立，它只是以浮点形式呈现已有数据。

## 7. 知识点覆盖

浮点几何、基线、缩放与变换、DPI、文本测量、换行规则一致性、advance 与 ink box、延迟取整、PDF/打印、复杂文本塑形。
