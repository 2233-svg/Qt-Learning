# QTextLayout
> Qt 6.11.1 · Qt GUI · 来自 `QTextLayout`

## 1. 先建立直觉

`QTextLayout` 是低层文本排版对象。它把一段字符串按字体、方向、换行宽度、格式范围排成一组 `QTextLine`，并能绘制、命中测试、处理光标位置。

`QTextDocument` 会为每个 block 使用布局；你也可以直接用它做自绘控件中的轻量文本排版。

## 2. 类说明

- 头文件：`#include <QTextLayout>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 类型：可独立使用的布局对象
- 协作类：`QTextLine`、`QTextOption`、`QPainter`、`QGlyphRun`

典型流程是 `beginLayout()`，循环 `createLine()`、设置 line width 和 position，最后 `endLayout()`。

## 3. API 速查

| API | 作用 |
| --- | --- |
| 构造函数 | 用文本、字体、paint device 创建布局 |
| `setText()` / `text()` | 设置或读取排版文本 |
| `setFont()` / `font()` | 默认字体 |
| `setTextOption()` / `textOption()` | 换行、对齐、方向、tab 等选项 |
| `setFormats()` / `formats()` | 设置格式范围 |
| `beginLayout()` / `createLine()` / `endLayout()` | 执行排版 |
| `lineAt()` / `lineForTextPosition()` / `lineCount()` | 查询布局行 |
| `draw()` | 绘制文本 |
| `drawCursor()` | 绘制光标 |
| `hitTest()` | 坐标到字符位置 |
| `glyphRuns()` | 获取 glyph run，适合高级绘制 |
| `minimumWidth()` / `maximumWidth()` | 排版宽度参考 |
| `boundingRect()` | 布局边界 |

## 4. 关键用法

```cpp
QTextLayout layout(text, font);
layout.beginLayout();
qreal y = 0;
while (true) {
    QTextLine line = layout.createLine();
    if (!line.isValid())
        break;
    line.setLineWidth(width);
    line.setPosition(QPointF(0, y));
    y += line.height();
}
layout.endLayout();
layout.draw(&painter, QPointF(0, 0));
```

格式范围使用 `QTextLayout::FormatRange`，适合自绘代码编辑器、搜索命中高亮等场景。

## 5. 使用场景

- 自绘控件排版多行文本。
- 代码编辑器自定义绘制行内容。
- 命中测试，鼠标坐标转字符位置。
- 获取 glyph run 做高级 OpenGL/RHI 文本渲染。
- 不需要完整 `QTextDocument` 的轻量富格式文本。

## 6. 常见坑与经验

- 修改文本、字体、格式或选项后要重新 layout。
- 必须 `beginLayout()` 和 `endLayout()` 成对使用。
- `QTextLayout` 只排一段文本，不提供文档级 frame/list/table。
- `hitTest()` 的坐标是布局局部坐标。
- 复杂脚本、双向文本、emoji 不要手写字符宽度，交给 layout。

## 7. 知识点覆盖

本页覆盖：低层文本排版、行创建、格式范围、绘制、命中测试、glyph run、双向文本基础。
