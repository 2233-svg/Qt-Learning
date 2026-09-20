# Qt QAbstractTextDocumentLayout::Selection 深入笔记

> 适用版本：Qt 6.11.1  
> 所属类：`QAbstractTextDocumentLayout`  
> 定义位置：`#include <QAbstractTextDocumentLayout>`  
> 定位：描述一次绘制中的临时文本选区和覆盖格式

## 1. 它解决什么问题

`QAbstractTextDocumentLayout::Selection` 用一个小型值对象描述“哪些文档字符在本次绘制中应该以什么附加格式显示”。它主要服务于：

- 编辑器当前选区；
- 查找结果高亮；
- 拼写错误或诊断范围；
- 临时搜索匹配；
- 只在预览中显示的注释范围。

它不是 `QTextCursor` 的替代品，也不是永久格式操作。把 `Selection` 放进 `PaintContext::selections` 后，布局只在本次 `draw()` 中叠加 `format`；不会把格式写回 `QTextDocument`。

## 2. 最小使用方式

```cpp
QTextCursor cursor(document);
cursor.setPosition(start);
cursor.setPosition(end, QTextCursor::KeepAnchor);

QAbstractTextDocumentLayout::Selection selection;
selection.cursor = cursor;
selection.format.setBackground(QColor("#fff3a3"));
selection.format.setForeground(Qt::black);

QAbstractTextDocumentLayout::PaintContext context;
context.selections.append(selection);
layout->draw(painter, context);
```

创建范围时通常要使用 `QTextCursor::KeepAnchor`。如果两次 `setPosition()` 都使用默认的 `MoveAnchor`，cursor 最终只有一个插入位置，不会形成选区。

## 3. 数据与所有权

`Selection` 是可复制的值类型，内部的 `QTextCursor` 和 `QTextCharFormat` 也按值语义传递。它不拥有 `QTextDocument`：cursor 仍然关联某个文档，而文档必须在布局绘制期间保持有效。

这意味着：

- 复制 `Selection` 不会复制整个文档；
- 销毁文档后，旧 selection 不能继续用于布局；
- selection 不会自动跟踪业务模型中的“搜索结果”变化；
- 文档编辑后，应用应重新计算范围或让 cursor 按 Qt 的 cursor 语义更新；
- selection 的格式只用于当前绘制，不会修改 cursor 覆盖文本的永久字符格式。

## 4. 成员逐项说明

### `QTextCursor cursor`

指定选区覆盖的文档范围。布局通常读取 `selection.cursor.selectionStart()` 和 `selection.cursor.selectionEnd()`，再把字符位置映射到行和 glyph。

边界：

- 空 cursor 或没有选区时，范围可能为空；
- `selectionStart()` 与 `selectionEnd()` 是文档字符位置，不是像素；
- cursor 必须关联正在布局的同一个 `QTextDocument`，否则位置没有可解释意义；
- 选区结束位置通常是半开区间语义，布局应按 QTextCursor 的范围规则处理；
- 文档变化后，旧 cursor 的范围可能改变，不能把它当成永久坐标。

如果选区是从用户选择复制出来的，通常直接保存该 cursor 的值即可；如果选区来自整数位置，优先构造一个明确关联文档的 cursor。

### `QTextCharFormat format`

指定覆盖到该选区上的字符格式。常用属性包括背景、前景、字体、下划线和波浪线。

默认构造的 `QTextCharFormat` 没有业务格式。文档头文件把它作为值成员，不会自动填入某个“选中颜色”。调用者应显式设置需要的属性：

```cpp
selection.format.clearForeground();
selection.format.setBackground(palette.highlight());
selection.format.setForeground(palette.highlightedText().color());
```

只设置需要改变的属性通常更稳妥。若把一个完整的文档字符格式复制进来，可能意外覆盖原文的字体、字号、语言或脚本属性，具体叠加优先级由布局实现决定。

## 5. 多个选区与重叠

一个 `PaintContext` 可以携带多个 `Selection`。它们可以来自不同用途，例如一个是系统选区，一个是查找命中高亮。

重叠时要注意：

- Qt 抽象接口没有规定所有布局都采用同样的合并顺序；
- 背景、前景、字体和装饰线可能分别有不同的叠加结果；
- 如果两个 selection 关联不同文档，布局无法正确解释它们；
- 大量碎片化 selection 会增加布局和绘制成本，应尽量合并相邻范围。

需要稳定视觉结果时，应用应在传入前先按文档位置排序、合并可合并范围，并明确哪一种高亮优先。

## 6. 与永久格式的区别

永久格式通过 `QTextCursor::mergeCharFormat()`、`setCharFormat()` 等编辑 API 写进文档；`Selection::format` 只是绘制覆盖层：

```cpp
// 永久修改文档：
QTextCursor edit(document);
edit.setPosition(start);
edit.setPosition(end, QTextCursor::KeepAnchor);
edit.mergeCharFormat(permanentFormat);

// 只在本次绘制中高亮：
QAbstractTextDocumentLayout::Selection overlay;
overlay.cursor = edit;
overlay.format.setBackground(Qt::yellow);
```

如果搜索结果、拼写检查或诊断标记需要随文档编辑实时变化，应由应用维护范围更新策略，而不是指望 `Selection` 自己成为持久标记。

## API 速查表

| 成员 | 类型 | 作用 | 默认/边界 |
| --- | --- | --- | --- |
| 构造 | `Selection` | 创建一个临时选区描述。 | 成员为默认构造的 cursor 和 format。 |
| 范围 | `cursor` | 指定被覆盖的文档字符范围。 | 通常用 `KeepAnchor` 建立范围；不是像素坐标。 |
| 样式 | `format` | 指定本次绘制的字符格式覆盖层。 | 不写回文档；只设置所需属性更安全。 |

### 一句话总结

`Selection` 是绘制时的临时高亮描述：`cursor` 决定范围，`format` 决定覆盖样式；它不拥有文档、不保存永久格式，文档变化或多选区重叠时都需要应用明确管理。
