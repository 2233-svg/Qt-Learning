# QGlyphRun：已经完成排版的字形序列

> Qt 版本：6.11.1  
> 模块：`Qt6::Gui`  
> 头文件：`#include <QGlyphRun>`

## 它解决什么问题

界面最终绘制的不是 Unicode 字符，而是某个具体字体中的**字形索引**以及每个字形的**基线位置**。字符到字形的转换还可能包含字体回退、连字、组合附加符号、双向文本重排等步骤，因此字符与字形通常不是简单的一一对应关系。

`QGlyphRun` 保存排版完成后的一段结果：

- 使用哪个 `QRawFont`；
- 要绘制哪些 glyph；
- 每个 glyph 放在什么基线坐标；
- 该段是否从右向左、是否带下划线等绘制标志；
- 可选的源字符串和 glyph 到字符串索引的映射。

它适合处在“文本布局”和“底层绘制”之间。常规控件只需使用 `QPainter::drawText()`；只有需要检查、缓存或单独绘制排版结果时，才通常直接接触 `QGlyphRun`。

## 实际使用场景

- 从 `QTextLayout::glyphRuns()` 取得排版结果，逐段绘制或分析字体回退。
- 实现文本选区、命中测试、字形调试器和排版可视化工具。
- 将一段已经整形的文字交给 `QPainter::drawGlyphRun()` 绘制。
- 检查一个字符范围最终对应了哪些 glyph，处理连字被部分选中的情况。
- 在明确掌握字体和字形数据时，手工构造字形序列。

不适合用它替代完整的文本排版器。手工把 `QString` 的码点值塞进 `glyphIndexes()` 是错误的，因为 glyph index 只对指定的 `QRawFont` 有意义。

## 基本使用

通常让 `QTextLayout` 完成字符整形，再消费产生的字形序列：

```cpp
#include <QGlyphRun>
#include <QPainter>
#include <QTextLayout>

void drawShapedText(QPainter &painter, const QString &text,
                    const QFont &font, const QPointF &origin)
{
    QTextLayout layout(text, font);
    layout.beginLayout();
    QTextLine line = layout.createLine();
    line.setLineWidth(600.0);
    line.setPosition(QPointF(0, 0));
    layout.endLayout();

    for (const QGlyphRun &run : line.glyphRuns())
        painter.drawGlyphRun(origin, run);
}
```

传给 `drawGlyphRun()` 的点是附加到字形位置上的原点。`positions()` 中的每个点描述对应 glyph 的基线边缘位置，不是字符矩形的左上角。

## 字形、位置与字体必须匹配

一个可绘制的字形序列至少依赖三组相互匹配的数据：

1. `rawFont()` 指明 glyph index 所属的字体实例；
2. `glyphIndexes()` 给出该字体中的 glyph 编号；
3. `positions()` 给出每个 glyph 的位置。

字形和位置列表应逐项对应。`setGlyphIndexes()` 不验证索引是否确实存在于当前字体中，`setPositions()` 也不会替调用方修正数量不一致的问题。手工组装时，应先通过同一个 `QRawFont` 或排版结果获得合法 glyph，再保持两组数组长度一致。

`QGlyphRun` 是隐式共享值类型，复制通常很轻量；修改副本时会分离。它不拥有窗口、绘制设备或 `QPainter`。

## 源字符串映射不是一一对应

Qt 6.5 起，字形序列可以携带 `sourceString()` 和 `stringIndexes()`。后一列表的每个元素对应一个 glyph，值是该 glyph 在源字符串中的关联索引。

这个映射不能按“一 glyph 对一字符”理解：

- 多个字符形成一个连字时，字符串索引可能出现跳跃；
- 一个字符产生多个 glyph 时，索引可能重复；
- 没有请求布局器生成映射，或该 run 不是从字符串构造时，列表可能为空；
- 索引只有在同一份 `sourceString()` 的语境中才有意义。

因此它适合把 glyph 追溯到文本范围，但不能单独用来重建原始字符串。

## `SplitLigature` 与边界矩形

对某个字符范围调用 `QTextLayout::glyphRuns()` 时，范围可能只覆盖一个连字的一部分。此时 run 仍可能包含完整连字 glyph，但设置 `SplitLigature`，表示当前 run 只代表这个 glyph 覆盖的部分字符。

绘制这种 run 时必须裁剪到 `boundingRect()`：

```cpp
painter.save();
painter.setClipRect(run.boundingRect(), Qt::IntersectClip);
painter.drawGlyphRun(QPointF(0, 0), run);
painter.restore();
```

否则完整连字会被绘制出来，选区颜色或局部高亮可能越过目标范围。`setBoundingRect()` 可以提供显式边界；如果设置的是空矩形，`boundingRect()` 会退回计算 glyph 的实际包围区域。普通完整 run 通常无需手工设置边界。

## `setRawData()` 的借用生命周期

`setRawData()` 是避免容器复制的低层入口，但它**不会复制**两个数组：

```cpp
QVector<quint32> glyphs = obtainGlyphs();
QVector<QPointF> positions = obtainPositions();

QGlyphRun run;
run.setRawFont(rawFont);
run.setRawData(glyphs.constData(), positions.constData(), glyphs.size());
```

只要 `run` 或它的任意副本仍存在，两个数组就必须保持存活且内存地址稳定。局部数组离开作用域、`QVector` 扩容、清空或重新分配，都会让 run 内部的指针失效。无法严格控制生命周期时，应使用会保存列表值的 `setGlyphIndexes()` 和 `setPositions()`。

## 线程边界

`QGlyphRun` 本身可作为值传递，但其中的 `QRawFont` 被视为创建线程本地资源。把 run 移到另一个线程后，原 `QRawFont` 在目标线程不可用于 `QPainter` 绘制。

跨线程传递排版数据时，应在目标线程创建可用的 `QRawFont`，再通过 `setRawFont()` 替换。若 run 使用 `setRawData()` 借用了外部数组，还必须同时满足数组的跨线程访问和生命周期要求。通常更稳妥的做法是在负责绘制的线程完成字体资源创建和最终绘制。

## 标志语义

`GlyphRunFlags` 记录 run 的附加属性：

| 标志 | 含义 |
| --- | --- |
| `Overline` | 绘制上划线 |
| `Underline` | 绘制下划线 |
| `StrikeOut` | 绘制删除线 |
| `RightToLeft` | run 的方向为从右向左 |
| `SplitLigature` | run 只表示所含连字 glyph 的一部分，绘制时需要按边界裁剪 |

`setOverline()`、`setUnderline()`、`setStrikeOut()` 和 `setRightToLeft()` 是常用标志的便捷接口；`setFlag()` 修改单项，`setFlags()` 替换整组标志。

## 常见错误

- 把 Unicode 码点当成 glyph index。glyph index 必须来自当前 `QRawFont`。
- 字形数量与位置数量不一致，导致绘制结果缺失或错位。
- 忽略字体回退，假定整个字符串只对应用户指定的一个字体。
- 保存了 `setRawData()` 指向的临时数组或发生过扩容的容器。
- 跨线程复制 run 后直接绘制，没有在目标线程重建 `QRawFont`。
- 把 `stringIndexes()` 当作连续且唯一的字符编号。
- 对 `SplitLigature` 的 run 不做裁剪，造成局部选区绘制完整连字。
- 仅凭 `boundingRect()` 做字符级命中测试；精确文本命中通常仍应依赖 `QTextLayout`。

## API 速查表

| 类别 | API | 语义与边界 |
| --- | --- | --- |
| 类型 | `GlyphRunFlag` | 单项绘制或方向标志：`Overline`、`Underline`、`StrikeOut`、`RightToLeft`、`SplitLigature`。 |
| 类型 | `GlyphRunFlags` | `QFlags<GlyphRunFlag>` 组合类型。 |
| 构造 | `QGlyphRun()` | 构造空 run。 |
| 构造 | `QGlyphRun(const QGlyphRun &other)` | 隐式共享复制；若借用 raw data，副本也延长了调用方必须保证的数组有效期。 |
| 析构 | `~QGlyphRun()` | 释放自身共享状态；不销毁外部绘制器，借用数组也不会由它释放。 |
| 交换 | `swap(QGlyphRun &other) noexcept` | 常量时间交换内部共享状态。 |
| 字体 | `rawFont() const` | 返回当前 `QRawFont`；字体与 glyph index 必须匹配，并受创建线程限制。 |
| 字体 | `setRawFont(const QRawFont &rawFont)` | 设置 glyph 所属字体；不会重新整形或验证已有 glyph。 |
| 原始数据 | `setRawData(const quint32 *glyphIndexArray, const QPointF *glyphPositionArray, int size)` | 借用前 `size` 项，不复制；两个数组必须在 run 及其所有副本存续期间保持有效。 |
| 字形 | `glyphIndexes() const` | 返回 glyph 索引列表；索引只对 `rawFont()` 有意义。 |
| 字形 | `setGlyphIndexes(const QList<quint32> &glyphIndexes)` | 设置索引列表；调用方负责保证索引合法并与位置逐项对应。 |
| 位置 | `positions() const` | 返回各 glyph 的基线位置列表。 |
| 位置 | `setPositions(const QList<QPointF> &positions)` | 设置位置列表；不会自动补齐、排序或匹配 glyph 数量。 |
| 状态 | `clear()` | 清空 run 的内容和关联状态，使其回到空状态。 |
| 状态 | `isEmpty() const` | 判断 run 是否没有可用字形数据。 |
| 标志 | `setOverline(bool overline)` | 开关 `Overline`。 |
| 标志 | `overline() const` | 查询是否带上划线标志。 |
| 标志 | `setUnderline(bool underline)` | 开关 `Underline`。 |
| 标志 | `underline() const` | 查询是否带下划线标志。 |
| 标志 | `setStrikeOut(bool strikeOut)` | 开关 `StrikeOut`。 |
| 标志 | `strikeOut() const` | 查询是否带删除线标志。 |
| 标志 | `setRightToLeft(bool on)` | 开关 `RightToLeft`；它描述方向，不执行双向算法或重新排列 glyph。 |
| 标志 | `isRightToLeft() const` | 查询 run 是否标记为从右向左。 |
| 标志 | `setFlag(GlyphRunFlag flag, bool enabled = true)` | 修改一个标志，不影响其他标志。 |
| 标志 | `setFlags(GlyphRunFlags flags)` | 用给定组合替换全部标志。 |
| 标志 | `flags() const` | 返回全部标志。 |
| 边界 | `setBoundingRect(const QRectF &boundingRect)` | 设置显式边界；空矩形会让查询退回 glyph 的计算边界。主要用于部分连字等特殊范围。 |
| 边界 | `boundingRect() const` | 返回显式边界，未设置有效边界时计算 glyph 包围区域；`SplitLigature` 绘制应以它裁剪。 |
| 文本映射 | `stringIndexes() const` | Qt 6.5 起。返回每个 glyph 对应的字符串索引；可能为空、重复或跳跃。 |
| 文本映射 | `setStringIndexes(const QList<qsizetype> &stringIndexes)` | Qt 6.5 起。设置 glyph 到源字符串的映射；应与 glyph 列表逐项对应。 |
| 文本映射 | `setSourceString(const QString &sourceString)` | Qt 6.5 起。保存映射所引用的源字符串，不会据此重新整形 glyph。 |
| 文本映射 | `sourceString() const` | Qt 6.5 起。返回可选源字符串。 |
| 比较 | `operator==(const QGlyphRun &other) const` | 比较字形列表、位置和字体等 run 状态；不是视觉近似比较。 |
| 比较 | `operator!=(const QGlyphRun &other) const` | `operator==` 的逻辑取反。 |
| 赋值 | `operator=(const QGlyphRun &other)` | 隐式共享复制赋值；同样遵守借用数组和字体线程边界。 |

## 相关类

- `QTextLayout`、`QTextLine`：执行文本布局并产生 glyph runs。
- `QTextFragment`：可从富文本片段取得对应 glyph runs。
- `QRawFont`：提供具体字体中的字形访问能力。
- `QPainter::drawGlyphRun()`：绘制已经排版好的字形序列。

`QGlyphRun` 的核心不是“存一段文字”，而是保存一段文字经过字体选择与排版后得到的可绘制结果。
