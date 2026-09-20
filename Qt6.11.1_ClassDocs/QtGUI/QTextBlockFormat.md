# QTextBlockFormat
> Qt 6.11.1 · Qt GUI · 来自 `QTextBlockFormat`

## 1. 先建立直觉

`QTextBlockFormat` 描述段落块级格式：对齐、缩进、边距、行高、分页控制、文本方向、非断行等。它影响整个 `QTextBlock`，不是某几个字符。

通过 `QTextCursor::setBlockFormat()` 或 `mergeBlockFormat()` 应用。

## 2. 类说明

- 头文件：`#include <QTextBlockFormat>`
- CMake：`target_link_libraries(mytarget PRIVATE Qt6::Gui)`
- 继承：`QTextFormat`
- 协作类：`QTextBlock`、`QTextCursor`

字符外观用 `QTextCharFormat`，段落布局用 `QTextBlockFormat`。二者经常同时出现，但职责不同。

## 3. API 速查

| API | 作用 |
| --- | --- |
| `setAlignment()` / `alignment()` | 段落对齐 |
| `setTextIndent()` / `textIndent()` | 首行缩进 |
| `setIndent()` / `indent()` | 列表式缩进层级 |
| `setLeftMargin()` / `rightMargin()` 等 | 四边 margin |
| `setTopMargin()` / `bottomMargin()` | 段前段后间距 |
| `setLineHeight()` / `lineHeight()` | 行高规则和值 |
| `setHeadingLevel()` / `headingLevel()` | 标题级别 |
| `setPageBreakPolicy()` | 分页前后控制 |
| `setNonBreakableLines()` | 行内不自动换行 |
| `setLayoutDirection()` | 段落方向 LTR/RTL |
| `setMarker()` / `marker()` | 任务列表等 marker |
| `setTabPositions()` / `tabPositions()` | 段落 tab stops |

## 4. 关键用法

居中标题：

```cpp
QTextBlockFormat bf;
bf.setAlignment(Qt::AlignHCenter);
bf.setHeadingLevel(1);
cursor.mergeBlockFormat(bf);
```

设置段落间距：

```cpp
bf.setTopMargin(8);
bf.setBottomMargin(8);
```

## 5. 使用场景

- 段落对齐、首行缩进、引用块。
- Markdown/HTML 导入后的段落样式。
- 打印分页控制。
- 任务列表和标题结构。
- RTL 文本段落排版。

## 6. 常见坑与经验

- block format 应用于当前光标所在块或选区覆盖的所有块。
- `textIndent` 是首行缩进，`leftMargin` 是整个段落左边距，别混用。
- 行高策略要结合具体枚举理解，固定值和百分比效果不同。
- 标题级别是语义提示，不会自动给你设置字号和粗体，仍需字符格式或样式配合。

## 7. 知识点覆盖

本页覆盖：段落对齐、缩进、边距、行高、分页、RTL、标题级别、任务 marker。
