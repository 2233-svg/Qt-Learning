# Qt QTextEdit::ExtraSelection 深入笔记

> 适用版本：Qt 6.11.1
> 所属模块：`Qt6::Widgets`
> 位置：`QTextEdit` 的辅助结构体
> 常见搭档：`QTextEdit::setExtraSelections()`、`QTextCursor`、`QTextCharFormat`

## 1. 它解决什么问题

`QTextEdit::ExtraSelection` 不是独立控件，而是一个“额外高亮描述”。它告诉 `QTextEdit`：

- 哪个光标范围要被标出来；
- 用什么格式覆盖显示；
- 这份高亮只是一层叠加，不是真的改文档内容。

它最常见的用途是：

- 搜索命中高亮；
- 当前行高亮；
- 错误位置标记；
- 选区外的临时视觉提示。

这类高亮的特点是“只是显示层”，所以它比直接修改文档内容更安全，也更容易撤销。

## 2. 最小可用代码

```cpp
#include <QTextEdit>
#include <QTextCursor>
#include <QTextCharFormat>

QTextEdit::ExtraSelection makeSelection(QTextEdit *edit)
{
    QTextEdit::ExtraSelection sel;
    sel.cursor = edit->textCursor();
    sel.format.setBackground(Qt::yellow);
    sel.format.setForeground(Qt::black);
    return sel;
}
```

然后把它交给：

```cpp
edit->setExtraSelections({makeSelection(edit)});
```

## 3. 两个字段分别做什么

### 3.1 `cursor`

`cursor` 决定高亮范围。它不是“当前编辑光标”的别名，而是一个可以独立描述范围的 `QTextCursor`。

你可以让它选中：

- 一整段文本；
- 一个词；
- 多个字符；
- 甚至空位置，用来标记插入点。

### 3.2 `format`

`format` 决定高亮的样式。它通常用 `QTextCharFormat` 设置背景色、前景色、下划线等属性。

常见组合是：

```cpp
sel.format.setBackground(QColor("#fff59d"));
sel.format.setProperty(QTextFormat::FullWidthSelection, true);
```

## 4. 适合什么场景

- 搜索功能把所有命中项临时标黄；
- 当前行左侧高亮；
- 拼写检查或语法检查提示；
- 代码编辑器里显示临时警告区域。

如果你只是想改正文内容，就不该用它；那种情况应该直接改文档或使用 `QTextCursor` 编辑文本。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 成员 | `cursor` | 记录要高亮的文本范围。 | 范围可以是选区，也可以是插入点。 |
| 成员 | `format` | 记录覆盖显示的格式。 | 常用背景色、前景色和附加属性。 |
| 用法 | `QTextEdit::setExtraSelections(const QList<ExtraSelection> &selections)` | 把额外高亮列表交给文本编辑器。 | 这是它真正的落点。 |
| 用法 | `QTextEdit::extraSelections() const` | 读取当前额外高亮。 | 适合调试和同步界面状态。 |

### 一句话总结

`QTextEdit::ExtraSelection` 是富文本编辑器的“临时高亮层描述”，用来标记范围和格式，而不是修改正文。
