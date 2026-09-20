# QTextList 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QTextList>`  
> 所属模块：`Qt6::Gui`  
> 继承：`QTextBlockGroup`

## 1. 它解决什么问题

`QTextList` 是 `QTextDocument` 中一组块的列表对象。它把多个 `QTextBlock` 组织成项目符号或编号列表，并通过 `QTextListFormat` 决定项目符号样式、编号前后缀、缩进和起始编号。

它不是 `QList<QTextBlock>` 这样的值容器。列表对象属于文档结构；加入或移除项目改变的是块与列表的关系，块本身和其中的文本不会因为 `remove()` 而被删除。

实际场景：

- 富文本编辑器中创建、缩进、取消缩进项目列表；
- 报告生成器输出编号步骤或项目符号；
- 遍历已有文档，读取某个块在列表中的编号文字；
- 调整整份列表的样式、起始编号和逻辑缩进。

## 2. 创建、成员关系和编号

通常由 `QTextCursor` 创建列表：

```cpp
QTextListFormat format;
format.setStyle(QTextListFormat::ListDecimal);
format.setNumberPrefix("(");
format.setNumberSuffix(")");

QTextList *list = cursor.insertList(format);
```

`add(block)` 将一个同文档的块加入列表，`remove(block)` 解除该块与列表的关系，`removeItem(i)` 按项目索引解除关系。三者都不是删除文本 API；需要删除内容应通过 `QTextCursor` 修改文档。

`itemNumber(block)` 返回块在列表中的零起始项目索引；块不属于当前列表时应先按失败情形处理，而不要把返回值当有效编号。`itemText(block)` 返回布局用于显示的项目标签，例如 `1.`、`(a)` 或项目符号；它不是块正文。

## 3. 格式写回和边界

`format()` 返回 `QTextListFormat` 副本，修改后必须用 `setFormat()` 写回：

```cpp
QTextListFormat format = list->format();
format.setIndent(format.indent() + 1);
list->setFormat(format);
```

列表的 `indent` 是逻辑级别，不是直接以像素为单位的左边距；实际距离还受文档的 `indentWidth`、块格式、书写方向和布局影响。一个项目可能包含多个文本块或嵌套结构，因此不应仅靠 `count()` 推断正文行数。

## 4. 生命周期和线程

由 `QTextCursor::createList()`、`insertList()` 或文档解析得到的 `QTextList *` 由 `QTextDocument` 管理。不要手动删除它，也不要在文档清空、删除对应结构或析构后继续使用该指针。

列表、块和格式更新必须在文档所属线程完成；不要把 `QTextList *` 传给后台线程。后台分析应传递纯文本、格式副本或独立文档。

## API 速查表

| API | 用途与关键语义 | 边界、默认值或注意事项 |
| --- | --- | --- |
| `QTextList(QTextDocument *)` | 为文档构造列表对象。 | 常规代码由光标/文档创建；文档管理生命周期。 |
| `~QTextList()` | 销毁列表对象。 | 文档拥有的列表不由调用方删除。 |
| `count()` | 返回当前列表项目数。 | 是列表块项目数，不是视觉行数或字符数。 |
| `item(int i)` | 返回第 `i` 个项目块。 | 索引应在 `[0, count())`；越界结果不可作为有效块使用。 |
| `itemNumber(const QTextBlock &)` | 查询一个块的零起始项目索引。 | 块必须属于当前列表；不属于时按失败结果处理。 |
| `itemText(const QTextBlock &)` | 返回该块的列表标签文本。 | 例如编号或项目符号，不是项目正文。 |
| `add(const QTextBlock &block)` | 把块加入列表。 | 块应来自同一文档；不会复制或删除块文本。 |
| `remove(const QTextBlock &block)` | 从列表中移除指定块。 | 只解除列表关系，块仍留在文档。 |
| `removeItem(int i)` | 从列表中按索引移除项目。 | 不删除该项目的文本内容。 |
| `format()` | 返回列表格式副本。 | 修改副本不会回写列表。 |
| `setFormat(const QTextListFormat &)` | 更新列表格式。 | 影响整份列表的标签和缩进；会触发布局更新。 |

## 5. 记忆重点

`QTextList` 是文档结构对象，不是普通容器。移除项目不会删正文，编号是列表项目索引，格式修改要“取副本、改副本、再写回”，对象指针始终由文档拥有。
