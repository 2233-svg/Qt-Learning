# QFontMetrics

> Qt 6.11.1 · Qt GUI · 来自 `QFontMetrics`

## 1. 先建立直觉

`QFontMetrics` 回答的是“按这个字体画出来，需要多少**整数像素**”。它不画文字，也不决定文字如何断行；它提供文字的前进距离、墨迹边界、基线和装饰线位置，供控件尺寸、手工绘制和省略文本使用。

最常见的混淆是把 `boundingRect().width()` 当作文本宽度。边界矩形描述墨迹会覆盖哪里；`horizontalAdvance()` 描述下一段文字应该从哪里开始。斜体的突出部分、负 bearing 和悬挂标点会让两者不同。

## 2. 类说明

- 头文件：`#include <QFontMetrics>`
- CMake：`target_link_libraries(app PRIVATE Qt6::Gui)`
- 类型：值类型。构造时固定字体和可选 `QPaintDevice`，随后字体变化不会反映到该对象。
- 需要亚像素精度时用 `QFontMetricsF`；交互式复杂文本、光标位置、双向文字和逐行排版用 `QTextLayout`。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QFontMetrics(font[, device])` | 创建与屏幕或指定绘制设备兼容的度量快照 |
| `ascent()` / `descent()` / `height()` | 获取基线上方、下方与基本行高 |
| `leading()` / `lineSpacing()` | 获取字体建议的额外行距和基线到基线距离 |
| `capHeight()` / `xHeight()` | 获取大写高度、x 高度，用于视觉对齐 |
| `horizontalAdvance(text)` | 计算排完文本后的笔位置，适合横向布局 |
| `boundingRect(text)` | 计算墨迹可能覆盖的矩形，适合裁剪与重绘区域 |
| `tightBoundingRect(text)` | 取得更紧的实际墨迹包围框 |
| `boundingRect(rect, flags, text, ...)` | 按对齐、换行、制表符规则测量多行文本 |
| `size(flags, text, ...)` | 返回按文本标志布局后的尺寸 |
| `elidedText(text, mode, width)` | 按像素宽度插入省略号 |
| `leftBearing()` / `rightBearing()` | 查询单字形越出其逻辑宽度的部分 |
| `averageCharWidth()` / `maxWidth()` | 粗略估算列宽或缓冲区，不保证等宽 |
| `inFont()` / `inFontUcs4()` | 检查单个 Unicode 字符能否由当前字体覆盖 |
| `underlinePos()` / `overlinePos()` / `strikeOutPos()` / `lineWidth()` | 手绘文本装饰线时使用 |
| `fontDpi()` | 取得计算该度量时的 DPI |
| `minLeftBearing()` / `minRightBearing()` | 取得全字体最小边距，可能较慢 |
| `swap()` / 比较与赋值运算符 | 值对象管理与比较 |

## 4. 关键用法

### 为自绘标签预留正确宽度

```cpp
QFontMetrics fm(font());
const QString title = fm.elidedText(documentName,
                                    Qt::ElideMiddle,
                                    availableWidth);
painter.drawText(x, baseline, title);
```

`elidedText()` 的 `width` 是像素宽度，不能传字符数。文件名、路径和标识符通常应使用 `Qt::ElideMiddle`，这样两端的关键信息都能保留。

### 区分排版宽度与墨迹范围

```cpp
QFontMetrics fm(font);
const int advance = fm.horizontalAdvance(text);
const QRect ink = fm.tightBoundingRect(text);

// 横向排列用 advance；为绘制内容建立裁剪/背景区域时关注 ink。
painter.drawText(origin, text);
nextOrigin.setX(origin.x() + advance);
```

`horizontalAdvance()` 会进行文本塑形，因此字符串中阿拉伯文、连字和组合音标仍应整段测量。不要逐个字符相加；开启 kerning 时，即使拉丁文本也不满足 `width("a") + width("b") == width("ab")`。

### 在给定矩形中测量自动换行文本

```cpp
const int flags = Qt::AlignLeft | Qt::AlignTop | Qt::TextWordWrap;
QRect used = fm.boundingRect(contentRect, flags, description);
painter.drawText(contentRect, flags, description);
```

测量和绘制必须使用同一组 `flags`、同一个矩形和同一种制表符规则。否则计算出的高度看似正确，却会在绘制时多出一行或发生裁切。

### 用基线建立多行文字

```cpp
int y = top + fm.ascent();
for (const QString &line : lines) {
    painter.drawText(left, y, line);
    y += fm.lineSpacing();
}
```

`height()` 是 `ascent() + descent()`；`lineSpacing()` 还包含 `leading()`，用于相邻基线的自然距离。

## 5. 使用场景

- 自绘控件的 `sizeHint()`、表头、徽标、工具栏文字与省略策略。
- 日志、代码、监控面板中按基线对齐多段文本。
- 富文本之外的简单多行说明文字布局。
- 根据字体覆盖情况选择 emoji、图标字体或回退字形。
- 手工绘制下划线、删除线，以及检查斜体是否超出背景区域。

## 6. 常见坑与经验

- **度量对象会过期。** 改变 `QWidget::font()`、屏幕 DPI 或 painter 的字体后，重新取得 `fontMetrics()` 或重建 `QFontMetrics`。
- **设备会改变结果。** 打印机、`QImage` 和屏幕的 DPI 可能不同；针对输出设备构造 `QFontMetrics(font, device)`，或从 painter 获取。
- **`boundingRect()` 并非“前进宽度”。** 它可能从原点左侧开始，也可能比 `horizontalAdvance()` 宽或窄。
- **`tightBoundingRect()` 不适合行布局。** 它紧贴墨迹，空白、上行和下行空间不足；文本行高仍优先用 `lineSpacing()`。
- **`minLeftBearing()` 与 `minRightBearing()` 可能昂贵。** 它们可能遍历字形；在绘制循环中缓存结果。
- **`QChar` 不是所有 Unicode 字符。** 非 BMP 码点应使用 `inFontUcs4()`；完整字符串的回退与塑形则不能仅凭它判断。
- **复杂编辑器别手写测量。** `horizontalAdvance(QChar)` 对阿拉伯文、组合标记等并不适合光标和选区；使用 `QTextLayout`。

## 7. 知识点覆盖

整数像素度量、基线、行距、advance 与 ink box、字形 bearing、文本省略、对齐与换行标志、DPI、Unicode 覆盖、文本塑形、绘制设备一致性。
