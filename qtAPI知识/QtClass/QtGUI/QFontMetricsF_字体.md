# QFontMetricsF

`QFontMetricsF` 为给定 `QFont` 和输出设备提供浮点字体度量。它是 `QFontMetrics` 的高精度版本，也是自定义排版、高 DPI 界面和打印布局的默认选择。

- 头文件：`#include <QFontMetricsF>`
- 模块：`Qt6::Gui`
- 类型特性：隐式共享的可复制值类型；结果是构造时快照
- 与 `QFontMetrics` 的差异：返回 `qreal`、`QRectF`、`QSizeF`，不在每个 API 调用时提前取整

## 它解决的问题

文本布局依赖连续距离：字形推进宽度可以是 7.25 px，基线和装饰线也可能落在分数坐标。若过早取整，单个字看似无差别，长文本、多列表格或缩放动画却会积累错位。`QFontMetricsF` 保留实际度量，直到绘制或像素对齐的最后一步才取整。

```cpp
QFontMetricsF fm(painter.font(), painter.device());
const qreal advance = fm.horizontalAdvance(text);
const QRectF ink = fm.tightBoundingRect(text);
```

`advance` 是后续文字应开始的水平位置；`ink` 是覆盖像素的紧边界。两者服务于不同问题，不能互换。

## 实际场景

**精确对齐图标和文字。** 使用 `ascent()`、`capHeight()` 或 `xHeight()` 计算视觉中心，避免仅按 `QRectF::center()` 对齐造成上下晃动。

**自定义文本布局。** 将连续片段的 `horizontalAdvance()` 相加，最后使用 `QPointF` / `QRectF` 绘制，避免每段都转整数。

**打印和多屏缩放。** 用 `QFontMetricsF(font, paintDevice)` 对目标 `QPrinter`、`QImage` 或绘制器设备测量；不要复用屏幕度量去安排打印版式。

## 生命周期、性能与复杂文本

对象不跟随 `QFont` 或 `QPainter` 更新。改变字号、设备 DPI、字距、变量轴或绘制器字体后，应重新创建 `QFontMetricsF`。

字符串的 `horizontalAdvance(text, length)` 即使只请求前几个字符，也可能检查整段，以保证阿拉伯文、天城文、连字等 shaping 的正确性。需要对长文本做大量局部测量时，考虑 `QTextLayout` / `QTextLine` 复用布局结果。

`minLeftBearing()`、`minRightBearing()` 和 `maxWidth()` 需要扫描字形集合，可能很慢；把它们放在初始化或缓存计算中。

## API 速查表

### 构造、复制与基础纵向度量

| API | 语义 | 使用时重点注意 |
| --- | --- | --- |
| `QFontMetricsF(font)` | 创建屏幕兼容度量快照。 | 对打印机字体可能使用最近屏幕字体；打印选设备重载。 |
| `QFontMetricsF(font, paintDevice)` | 创建匹配指定设备的度量快照。 | 屏幕、图片和打印机可得不同 DPI 结果。 |
| `QFontMetricsF(QFontMetrics)` | 从整数度量构造浮点度量。 | 不能恢复已经损失的整数精度；优先直接从 `QFont` 构造。 |
| 复制构造、`operator=`、移动赋值、`swap()` | 复制、赋值或交换快照。 | 不重新测量或更新字体状态。 |
| `ascent()` / `descent()` | 返回基线上方/下方的浮点高度。 | `height()` 恒等于二者之和。 |
| `height()` | 返回字形行框高度，不含 leading。 | 单行最小布局高度常用。 |
| `leading()` / `lineSpacing()` | 返回额外行距及推荐基线间距。 | 多行正文按 `lineSpacing()` 递增基线。 |
| `capHeight()` / `xHeight()` | 返回大写高度和小写 x 高度。 | 用于视觉对齐，不等同于点大小。 |
| `averageCharWidth()` | 返回平均字符宽度估计。 | 不是任何具体字符串的精确宽度。 |
| `maxWidth()` | 返回字体中最宽字形的宽度。 | 可能慢，且不是文本推进宽度。 |
| `minLeftBearing()` / `minRightBearing()` | 返回全字体最小左右 bearing。 | 可能慢；用于预留字形外伸空间。 |
| `fontDpi()` | 返回度量关联的字体 DPI。 | 诊断设备依赖时使用。 |
| `underlinePos()` / `overlinePos()` / `strikeOutPos()` / `lineWidth()` | 返回装饰线位置与建议厚度。 | 均为相对基线的浮点度量。 |

### 字符覆盖、推进与边界

| API | 语义 | 使用时重点注意 |
| --- | --- | --- |
| `inFont(QChar)` | 查询单个 BMP 字符是否在字体中。 | 非 BMP 码点使用 `inFontUcs4()`。 |
| `inFontUcs4(uint)` | 查询 Unicode 码点覆盖。 | 不等同于整段复杂文本必然用该字体渲染。 |
| `leftBearing(ch)` / `rightBearing(ch)` | 返回字符两侧的 bearing，可为负。 | 斜体/花体边缘裁剪时必须考虑。 |
| `horizontalAdvance(QChar)` | 返回单字符推进距离。 | 与其墨迹宽度不同。 |
| `horizontalAdvance(text, length)` | 返回前 `length` 个字符的推进距离。 | `length < 0` 测全文；完整字符串仍会参与 shaping 分析。 |
| `horizontalAdvance(text, textOption)` | 以 `QTextOption` 指定方向等布局规则测推进。 | Qt 6.3；复杂脚本优先这一重载。 |
| `boundingRect(QChar)` | 返回字符在基线最左点附近的墨迹矩形。 | 可越过 x=0，也可跨越基线上下。 |
| `boundingRect(text)` | 返回文本的墨迹边界。 | 宽度不保证等于 advance；`\n` 作为普通字符处理。 |
| `boundingRect(text, textOption)` | 按 `QTextOption` 返回文本边界。 | Qt 6.3；适合需要明确文本方向的测量。 |
| `boundingRect(rect, flags, text, tabStops, tabArray)` | 模拟矩形 `drawText` 的布局边界。 | tab 参数属旧式接口；复杂布局考虑 `QTextLayout`。 |
| `size(flags, text, tabStops, tabArray)` | 返回上述 flags 布局尺寸。 | 只需要宽高时使用。 |
| `tightBoundingRect(text)` | 返回紧贴墨迹的边界。 | 不能用于连续文本的下一起点。 |
| `tightBoundingRect(text, textOption)` | 按 `QTextOption` 返回紧边界。 | Qt 6.3。 |
| `elidedText(text, mode, width, flags)` | 在浮点像素宽度内生成省略文本。 | 宽度单位仍为像素；RTL 会镜像省略号的视觉方向。 |
| `operator==` / `!=` | 比较度量对象状态。 | 不是比较某次文本布局结果。 |

## 易错点

1. 计算出 `QRectF` 后马上逐项 `toRect()`。这会失去使用本类的意义；仅在最终像素 API 必需时取整。
2. 在 `QPainter` 更换字体或目标设备后继续用原度量。重新构造快照。
3. 用 `tightBoundingRect()` 处理换行文本。它不会将 `\n` 解释成布局换行。
4. 误将 `inFont()` 当成 fallback 后仍能显示的判断。它询问当前字体本身，不描述 Qt 回退链。
