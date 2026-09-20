# QTextLine 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QTextLine>`  
> 所属模块：`Qt6::Gui`  
> 类型：由 `QTextLayout` 产生的轻量行句柄

## 1. 它解决什么问题

`QTextLine` 表示 `QTextLayout` 已经分出的一个视觉行。它提供行的几何、文本范围、绘制、x 坐标与光标位置互相映射，以及可选的字形运行访问。

它解决的是单段文本排版后“第 N 个视觉行在哪里、包含哪些字符、鼠标点在哪里应落到哪个光标位置”的问题。它不是字符串的行分割器：自动换行、双向文本、连字和字形边界都会让视觉行与简单换行符切分不同。

## 2. 从 `QTextLayout` 获得并配置

`QTextLine` 由 `QTextLayout::createLine()` 或 `lineAt()` 返回。默认构造对象无效；不要自己把它当作独立可布局对象。

```cpp
layout.beginLayout();
QTextLine line = layout.createLine();
if (line.isValid()) {
    line.setLineWidth(300);
    line.setPosition(QPointF(12, 0));
}
layout.endLayout();
```

`setLineWidth()` 是手工换行中的关键步骤：它给本行可用宽度，决定换行位置和对齐空间。`setNumColumns()` 以字符列数限制行，不等同于像素宽度；带 `alignmentWidth` 的重载提供用于对齐的宽度。二者通常选择其一作为主要约束，不要在不了解重新布局结果的情况下反复交替设置。

## 3. 坐标、光标与双向文本

`cursorToX()` 将文本位置映射为行内 x 坐标，`xToCursor()` 把 x 映射回文本位置。带 `int *cursorPos` 的 `cursorToX()` 会把传入位置修正为有效光标位置；需要拿到 Qt 的修正结果时必须使用该重载。

`Leading` 与 `Trailing` 指定在字形边缘取哪一侧。对普通从左到右文本它们常看似只是前后边界，但在 RTL、连字或复杂字形中差异很重要。

`CursorBetweenCharacters` 把点击位置解释为字符间的插入点；`CursorOnCharacter` 偏向命中字符。点击编辑器时通常使用前者。

## 4. 几何和文本范围

- `position()`、`x()`、`y()`：本行相对 layout 的放置位置；
- `rect()`：当前分配给本行的布局矩形；
- `width()`：当前设置的行宽；
- `naturalTextWidth()`：文字不受当前行宽约束时的自然宽度；
- `horizontalAdvance()`：排版运行的水平推进量；
- `textStart()`、`textLength()`：本行在 layout 文本中的起点和长度。

这些数值基于最近一次 layout。改变文本、字体、格式、选项，或调用 `clearLayout()` 后，旧行的几何和位置映射都不应继续使用。

## 5. 绘制、字形和线程

`draw()` 在给定 painter 和位置绘制该行；位置会与 line/layout 自身位置共同构成最终坐标。`glyphRuns()` 提取字形数据，适合自定义渲染或高级命中测试，但普通绘制不必先提取它。

行对象不拥有 layout；layout 销毁、清理或重新布局后，所有旧 `QTextLine` 句柄都应视为过期。不要跨线程并发访问同一 layout 和其行；绘制还必须遵守 painter 与目标设备的线程规则。

## API 速查表

| API | 用途与关键语义 | 边界、默认值或注意事项 |
| --- | --- | --- |
| `QTextLine()` | 创建无效行句柄。 | 只有 `QTextLayout` 产生的有效行才可布局和绘制。 |
| `isValid()` | 判断是否关联有效 layout 行。 | `createLine()` 用无效结果表示没有更多文本。 |
| `setLineWidth(qreal)` / `width()` | 设置或读取当前行宽约束。 | 影响换行与对齐；不等于自然文本宽度。 |
| `setNumColumns(int)` | 用字符列数设置行约束。 | 列不是像素，复杂文本的视觉宽度仍依字体而变。 |
| `setNumColumns(int, qreal alignmentWidth)` | 设置列数及对齐宽度。 | 用于列式排版；避免与不兼容的行宽策略混用。 |
| `setPosition()` / `position()` | 设置或读取行相对 layout 的位置。 | 不是屏幕全局坐标。 |
| `x()` / `y()` | 返回行位置的两个分量。 | 与 `position()` 对应。 |
| `rect()` | 返回本行的布局矩形。 | 几何依赖最近一次布局。 |
| `ascent()` / `descent()` / `height()` / `leading()` | 返回行的垂直度量。 | 用于堆叠行和基线计算，不是固定字体常量。 |
| `setLeadingIncluded()` / `leadingIncluded()` | 控制行高是否包含 leading。 | 会影响纵向累加和相邻行间距。 |
| `naturalTextWidth()` | 返回无宽度约束时的自然文字宽度。 | 可大于 `width()`。 |
| `horizontalAdvance()` | 返回文字水平推进量。 | 与自然边界和分配宽度并非总相同。 |
| `naturalTextRect()` | 返回文字自然边界矩形。 | 不包含任意额外行宽空白。 |
| `cursorToX(int *, Edge)` | 将位置映射为 x，并修正到有效光标位置。 | 指针必须有效；应读取写回后的修正位置。 |
| `cursorToX(int, Edge)` | 将位置映射为 x。 | 不向调用方返回位置修正结果。 |
| `xToCursor(qreal, CursorPosition)` | 将 x 映射为文本光标位置。 | `CursorBetweenCharacters` 适合插入点；BiDi 下不要自行用比例换算。 |
| `Edge::Leading` / `Trailing` | 指定字形的逻辑前沿或后沿。 | RTL、连字和复杂字形中两者可能显著不同。 |
| `CursorPosition::CursorBetweenCharacters` / `CursorOnCharacter` | 指定 x 命中的插入点或字符策略。 | 影响点击命中结果。 |
| `textStart()` / `textLength()` | 返回行在 layout 文本中的起点和长度。 | 是 layout 文本坐标，不是文档块号或字节偏移。 |
| `lineNumber()` | 返回此行的零起始行索引。 | 是 layout 内视觉行号，不是文档块号。 |
| `draw(QPainter *, const QPointF &)` | 绘制该行。 | painter 必须有效；不会替你完成布局。 |
| `glyphRuns(int, int)` | 取得范围的字形运行。 | 默认请求整行范围；提取成本高于直接 draw。 |
| `glyphRuns(int, int, GlyphRunRetrievalFlags)` | 按检索标志取得字形运行。 | Qt 6.5 起；仅在启用 raw font 支持时可用。 |

## 7. 记忆重点

`QTextLine` 是当前 `QTextLayout` 的一行视觉结果。先完成 layout，再用它做绘制和命中测试；位置是 layout 文本/局部坐标，双向文字则交给 `cursorToX()`、`xToCursor()` 和 `Leading` / `Trailing` 处理。
