# QTextCharFormat
> Qt 6.11.1 · Qt GUI · 来自 `QTextCharFormat`

## 1. 先建立直觉

`QTextCharFormat` 描述一段字符的外观和语义：字体、字号、颜色、背景、下划线、锚点链接、上下标、字距、工具提示、对象类型等。

它作用在字符范围上，通常通过 `QTextCursor::setCharFormat()` 或 `mergeCharFormat()` 应用。

## 2. 类说明

- 头文件：`#include <QTextCharFormat>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 继承：`QTextFormat`
- 协作类：`QTextCursor`、`QTextFragment`、`QTextLayout::FormatRange`

字符格式不控制段落缩进、行距、列表编号或表格边框；那些分别属于 block/list/table/frame 格式。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `setFont()` / `font()` | 整体字体 |
| `setFontFamily()` / `fontFamilies()` | 字体族 |
| `setFontPointSize()` / `fontPointSize()` | 字号 |
| `setFontWeight()` / `fontWeight()` | 字重 |
| `setFontItalic()` / `fontItalic()` | 斜体 |
| `setFontUnderline()` / `fontUnderline()` | 下划线 |
| `setUnderlineStyle()` / `underlineStyle()` | 下划线样式 |
| `setUnderlineColor()` / `underlineColor()` | 下划线颜色 |
| `setForeground()` / `foreground()` | 文字颜色画刷 |
| `setBackground()` / `background()` | 背景画刷 |
| `setVerticalAlignment()` | 上标、下标、基线等 |
| `setAnchor()` / `isAnchor()` | 标记为链接锚点 |
| `setAnchorHref()` / `anchorHref()` | 链接地址 |
| `setAnchorNames()` / `anchorNames()` | 锚点名称 |
| `setToolTip()` / `toolTip()` | 悬停提示 |
| `setTextOutline()` / `textOutline()` | 文本描边 |
| `setObjectType()` | 插入自定义 inline object |

## 4. 关键用法

给选区加链接：

```cpp
QTextCharFormat link;
link.setAnchor(true);
link.setAnchorHref("https://example.com");
link.setForeground(Qt::blue);
link.setFontUnderline(true);
cursor.mergeCharFormat(link);
```

插入上标：

```cpp
QTextCharFormat sup;
sup.setVerticalAlignment(QTextCharFormat::AlignSuperScript);
cursor.insertText("2", sup);
```

## 5. 使用场景

- 富文本编辑器工具栏：字体、颜色、粗体、斜体。
- 链接、脚注、上标下标。
- 语法高亮中的 token 着色。
- 自定义 inline object 占位。
- 搜索命中或诊断高亮。

## 6. 常见坑与经验

- 工具栏按钮推荐用 `mergeCharFormat()`，否则可能覆盖用户已有字体属性。
- `setFont()` 会设置一组字体属性；只想改字号或粗体时用单项 setter。
- 链接不仅是蓝色下划线，必须 `setAnchor(true)` 和 href 才有语义。
- 语法高亮设置的格式是显示层，不等同于修改文档存储的富文本格式。

## 7. 知识点覆盖

本页覆盖：字符外观、链接语义、上下标、文本描边、格式合并、语法高亮与文档格式区别。
