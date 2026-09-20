# QFontMetrics

`QFontMetrics` 计算指定字体在指定设备上的字符与字符串尺寸，但它把所有结果四舍五入为整数像素。现代高 DPI、缩放和复杂文本布局通常应优先使用 `QFontMetricsF`；本类适合最终 API 需要 `int` / `QRect` / `QSize` 时使用。

- 头文件：`#include <QFontMetrics>`
- 模块：`Qt6::Gui`
- 类型特性：隐式共享的值类型；构造后是度量快照
- 关键边界：字体或绘制器之后改变时，既有对象不会更新

## 它解决的问题

文字的墨迹边界、笔画出界和下一字符的起点不是同一件事。`QFontMetrics` 提供三类度量：

| 需求 | 典型 API | 说明 |
| --- | --- | --- |
| 行距和基线 | `ascent()`、`descent()`、`lineSpacing()` | 安排多行文本 |
| 连续排版宽度 | `horizontalAdvance()` | 下一段文字应开始的位置 |
| 像素覆盖范围 | `boundingRect()`、`tightBoundingRect()` | 裁剪、命中/背景、离屏图像尺寸 |

不要用 `boundingRect(text).width()` 代替 `horizontalAdvance(text)`。斜体的左侧外伸、右侧 overhang 和字形组合都会让墨迹宽度不同于推进宽度。

## 实际场景

**自绘控件截断文字。**

```cpp
const QFontMetrics fm(font());
const QString label = fm.elidedText(title, Qt::ElideRight, availableWidth);
painter.drawText(rect, Qt::AlignVCenter, label);
```

**计算自绘行高。** `height()` 固定为 `ascent() + descent()`；如果希望两行之间加上字体建议的额外间距，用 `lineSpacing()`，它还包含 `leading()`。

**为复杂布局留空间。** `boundingRect(rect, flags, text, ...)` 会把换行、对齐和 tab 等绘制语义纳入计算；若文本有精确的方向、换行策略和 tab 设置，使用 Qt 6.3 起接收 `QTextOption` 的重载更清晰。

## 设备和精度边界

仅传 `QFont` 构造时，得到的是屏幕兼容度量；传入 `QPaintDevice` 时度量与该设备关联。打印机字体只用第一种构造时，Qt 可能改用最近的屏幕字体，结果可能不准确。对 `QPainter`，`painter.fontMetrics()` 是当前绘制器的度量快照。

本类会把分数度量取整，累计后可能出现一两个像素的错位。对高 DPI、动画、文本编辑器、对齐表格和自定义渲染，优先 `QFontMetricsF`，最后一步再按绘制需求取整。

`minLeftBearing()`、`minRightBearing()`、`maxWidth()` 要扫描字体字形集合，字体大时很慢，不应放在每帧绘制或模型 `data()` 中。

## API 速查表

### 构造、复制与字体级度量

| API | 语义 | 使用时重点注意 |
| --- | --- | --- |
| `QFontMetrics(font)` | 构造屏幕兼容字体的度量快照。 | 之后改变 `font` 不会刷新；打印机字体可能不准。 |
| `QFontMetrics(font, paintDevice)` | 构造与指定设备匹配的度量快照。 | 设备必须在构造时有效；打印/高 DPI 选此重载。 |
| 复制构造、`operator=`、移动赋值、`swap()` | 复制、赋值或交换快照。 | 不触发新的匹配或测量。 |
| `ascent()` | 基线以上的最大高度。 | 文本原点在基线时通常用 `y - ascent()` 得到行顶。 |
| `descent()` | 基线以下的最大高度。 | `height() == ascent() + descent()`。 |
| `height()` | 字体高度，不含额外 leading。 | 单行行框常用。 |
| `leading()` | 建议的额外行间距。 | 可为零。 |
| `lineSpacing()` | `height() + leading()`。 | 多行基线距离通常用它。 |
| `capHeight()` | 大写字母顶部到基线的高度。 | 适合图标与全大写标签的视觉对齐。 |
| `xHeight()` | 小写 x 的高度。 | 不等同于字号。 |
| `averageCharWidth()` | 平均字符宽度估计。 | 不能精确替代字符串宽度。 |
| `maxWidth()` | 任意字形的最大宽度。 | 可能慢；不等同于字符串最大推进宽度。 |
| `minLeftBearing()` / `minRightBearing()` | 全字体最小左右 side bearing。 | 可能慢；用于防止斜体等字形裁剪。 |
| `fontDpi()` | 此度量使用的字体 DPI。 | 用于诊断，不要用常数假定屏幕 DPI。 |
| `underlinePos()` / `overlinePos()` / `strikeOutPos()` / `lineWidth()` | 装饰线的位置和建议线宽。 | 为相对基线的字体度量，绘制时结合文本原点。 |

### 字符、字符串与矩形

| API | 语义 | 使用时重点注意 |
| --- | --- | --- |
| `inFont(QChar)` | 判断 BMP 字符是否在字体中。 | 只接收单个 UTF-16 单元，非 BMP 用 `inFontUcs4()`。 |
| `inFontUcs4(uint)` | 判断 Unicode 码点是否可用。 | 结果不等价于复杂脚本整段 shaping 能力。 |
| `leftBearing(ch)` / `rightBearing(ch)` | 返回字符相对推进框的左右空白，可能为负。 | 处理斜体外伸和裁剪。 |
| `horizontalAdvance(QChar)` | 返回字符的推进宽度。 | 不是 `boundingRect(ch).width()`。 |
| `horizontalAdvance(text, len)` | 返回前 `len` 个字符的推进宽度。 | `len < 0` 为全文；即使 `len` 很短，Qt 仍会分析整段文本以正确处理 shaping。 |
| `horizontalAdvance(text, option)` | 按 `QTextOption` 布局返回推进宽度。 | Qt 6.3；方向/文本选项影响结果。 |
| `boundingRect(QChar)` | 返回单字符在原点绘制时的墨迹矩形。 | 空格通常为空；宽度不能用于推进。 |
| `boundingRect(text)` | 返回文本墨迹边界。 | 宽度可能与推进不同；换行符按普通字符处理。 |
| `boundingRect(text, option)` | 按 `QTextOption` 返回文本边界。 | Qt 6.3；复杂文字/方向优先使用。 |
| `boundingRect(rect, flags, text, tabStops, tabArray)` | 计算在给定矩形与 `drawText` flags 下的布局边界。 | `tabArray` 是旧接口；新代码优先 `QTextOption`/布局类。 |
| `boundingRect(x, y, w, h, flags, text, ...)` | 上一 API 的坐标参数便利重载。 | 本质同上。 |
| `size(flags, text, tabStops, tabArray)` | 返回上述 flags 布局的尺寸。 | 等价于只取边界大小的便利入口。 |
| `tightBoundingRect(text)` | 返回更紧的文本墨迹边界。 | 不含排版推进空白；换行不解释为换行。 |
| `tightBoundingRect(text, option)` | 按 `QTextOption` 返回紧边界。 | Qt 6.3。 |
| `elidedText(text, mode, width, flags)` | 在像素宽度不足时插入省略号。 | 宽度单位是像素；`flags` 目前主要支持 `Qt::TextShowMnemonic`；省略位置受 RTL 方向影响。 |
| `operator==` / `!=` | 比较两个度量快照。 | 比较其内部字体状态，不是比较某段文本测量结果。 |

## 易错点

1. 给固定宽度列做累加时使用整数度量。分数 advance 在多列后会造成可见漂移，使用 `QFontMetricsF`。
2. 忽略负 bearing。只按 `horizontalAdvance()` 建图可能裁掉斜体字形左/右边缘。
3. 用 `tightBoundingRect()` 计算多行文本高度。它不把 `\n` 当作换行；使用绘制矩形重载或 `QTextLayout`。
4. 在性能热路径调用 `minLeftBearing()`、`minRightBearing()`、`maxWidth()`。
