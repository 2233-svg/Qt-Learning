# QTextLine
> Qt 6.11.1 · Qt GUI · 来自 `QTextLine`

## 1. 先建立直觉

`QTextLine` 是 `QTextLayout` 排版出来的一行。它知道这一行从文本哪个位置开始、长度是多少、宽高和基线在哪里，也能把 x 坐标换成字符位置。

它是布局结果的句柄，不是独立文本容器。

## 2. 类说明

- 头文件：`#include <QTextLine>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 类型：值类型，来自 `QTextLayout::createLine()` 或查询函数
- 协作类：`QTextLayout`

line 的几何信息只有在设置 line width 并完成布局后才有实际意义。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `isValid()` | 是否有效 |
| `setLineWidth()` / `width()` | 设置或读取行宽 |
| `setNumColumns()` / `numColumns()` | 按列数限制排版 |
| `setPosition()` / `position()` | 设置或读取行位置 |
| `textStart()` / `textLength()` | 行对应的文本范围 |
| `naturalTextWidth()` / `naturalTextRect()` | 不强制填满时的自然文本宽度和矩形 |
| `height()` / `ascent()` / `descent()` / `leading()` | 行高和字体度量 |
| `cursorToX()` / `xToCursor()` | 字符位置和 x 坐标互转 |
| `draw()` | 绘制该行 |
| `glyphRuns()` | 获取该行 glyph run |

## 4. 关键用法

鼠标点击定位：

```cpp
QTextLine line = layout.lineAt(lineIndex);
int pos = line.xToCursor(mouseX - line.position().x());
```

绘制单行：

```cpp
line.draw(&painter, origin);
```

`cursorToX()` 和 `xToCursor()` 会处理复杂脚本和双向文本，优先用它们而不是自己累加字符宽度。

## 5. 使用场景

- 自绘文本选择区域。
- 鼠标点击、拖拽选区命中测试。
- 行号编辑器计算每行高度。
- 对齐、截断、逐行绘制。
- 获取一行的 glyph 数据。

## 6. 常见坑与经验

- `textStart()` 是 layout 文本内的位置，不一定是文档全局位置。
- 行位置通常由你在排版循环中设置；不设置时几何可能都挤在原点。
- `naturalTextWidth()` 和 `width()` 不同，前者是内容需要的宽度，后者是布局给它的宽度。
- line 依附 layout，layout 改变后旧 line 要重新获取。

## 7. 知识点覆盖

本页覆盖：布局行、文本范围、行几何、基线度量、坐标和 cursor 转换、逐行绘制。
