# QTextCursor 类笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QTextCursor>`  
> 所属模块：`Qt6::Gui`  
> 继承：无（隐式共享值类型）

## 1. 它解决什么问题

`QTextDocument` 保存的是一棵结构化富文本树：文档由块（block）组成，块中有字符格式、列表、表格、框架和图像对象。`QTextCursor` 是访问和修改这棵树的“编辑位置”对象。

它同时表示两件事：

- 一个当前位置 `position()`；
- 一个锚点 `anchor()`。当前位置与锚点不同，就形成选区。

因此它不是“字符串下标”那么简单。光标可以跨块移动、选择结构化内容、读取或修改格式、插入列表和表格，并把多次编辑合并成一次撤销命令。

典型使用场景包括：

- `QTextEdit` / `QPlainTextEdit` 的查找、替换、选中和格式化；
- 编辑器中按单词、行、块移动光标；
- 在光标处插入 HTML、Markdown、图片、表格或列表；
- 代码编辑器按块读取文本、给选区统一着色；
- 批量修改文档，同时让用户按一次撤销即可恢复。

`QTextCursor` 本身不拥有文档。它只是一个轻量的值对象，真正的文本和格式存放在关联的 `QTextDocument` 中。

## 2. 最小使用方式

```cpp
#include <QTextCursor>
#include <QTextDocument>

QTextDocument document;
document.setPlainText("one\ntwo\nthree");

QTextCursor cursor(&document);
cursor.movePosition(QTextCursor::Start);
cursor.movePosition(QTextCursor::NextWord, QTextCursor::KeepAnchor);

qDebug() << cursor.selectedText(); // "one"
cursor.insertText("ONE");           // 替换当前选区
```

使用编辑器控件时，通常复制控件的光标，修改后再写回去：

```cpp
QTextCursor cursor = editor->textCursor();
cursor.beginEditBlock();
cursor.select(QTextCursor::WordUnderCursor);
cursor.mergeCharFormat(emphasisFormat);
cursor.endEditBlock();
editor->setTextCursor(cursor);
```

## 3. 位置、锚点和选区

### 3.1 位置是文档中的字符位置

位置是插入点，范围通常是 `[0, document->characterCount()]`。它位于字符之间，而不是“指向一个字符”。`position()` 指向当前位置，`anchor()` 是选择起点；选区的实际范围应使用 `selectionStart()` 和 `selectionEnd()`，不要假定锚点总是小于当前位置。

文档内部的块分隔符也占用位置。`QTextBlock::position()` 给出块起点，块的末尾位置通常包括块分隔符所在的边界。对用户可见文本进行逐字符处理时，要区分 `selectedText()` 返回的段落分隔符（常见为 `QChar::ParagraphSeparator`）与普通换行字符串。

### 3.2 `MoveAnchor` 与 `KeepAnchor`

- `MoveAnchor`：移动后把锚点也放到新位置，原选区被清除；
- `KeepAnchor`：移动当前位置但保留锚点，用来扩展或收缩选区。

`setPosition()` 和 `movePosition()` 都支持这两种模式。一个常见的错误是先用 `KeepAnchor` 选中内容，之后继续移动却忘了恢复 `MoveAnchor`，导致后续输入替换了整段选区。

### 3.3 选区替换和选区删除

在有选区时：

- `insertText()` 会用新文本替换选区；
- `removeSelectedText()` 删除选区并把光标放在删除位置；
- `deleteChar()` 删除光标后的一个字符或对象；
- `deletePreviousChar()` 删除光标前的一个字符或对象。

这些操作会修改关联文档并进入文档的撤销栈，除非文档关闭了撤销或正在执行特殊的撤销/重做操作。

## 4. 移动语义和边界

`movePosition(operation, mode, n)` 会尝试重复执行移动操作 `n` 次，并返回是否成功完成请求。到达文档边界时，光标会停在边界，返回 `false`；不要把 `true` 理解为“移动了一个字符”，例如某些按块移动可能已经到达边界。

常用操作：

- `Start` / `End`：文档起点和文档终点；
- `StartOfBlock` / `EndOfBlock`：当前块起点和块末；
- `StartOfLine` / `EndOfLine`：当前视觉行的起止位置；
- `StartOfWord` / `EndOfWord`：当前单词的起止位置；
- `PreviousCharacter` / `NextCharacter`：按文本字符导航；
- `Left` / `Right`：按光标移动样式导航；
- `Up` / `Down`：保留水平视觉位置，移动到上一视觉行或下一视觉行；
- `PreviousBlock` / `NextBlock`：跨段落块移动；
- `PreviousWord` / `NextWord`：按单词边界移动；
- `WordLeft` / `WordRight`：按界面光标移动规则移动；
- `NextCell` / `PreviousCell`：在表格单元格之间移动；
- `NextRow` / `PreviousRow`：按表格行移动。

`StartOfLine` 和 `EndOfLine` 依赖文档布局产生的视觉换行；没有合适布局或使用纯文本块模型时，不应把它们当成源文本中的 `\n`。`Left` / `Right` 还会受到 `QTextDocument::defaultCursorMoveStyle()` 与 `visualNavigation()` 影响。

`Up` / `Down` 使用 `verticalMovementX()` 保存垂直移动时的目标横坐标。编辑器实现中不要在每次按键前无条件重置这个值，否则连续上下移动会在长短不一的行之间横向漂移。

## 5. 格式 API 的实际差异

### 字符格式

`charFormat()` 返回当前位置适用的字符格式；有选区时，读取结果通常代表光标位置或选区相关的格式状态，不能用它判断选区内每个字符都完全相同。`setCharFormat()` 直接设置选区格式，`mergeCharFormat()` 只合并传入格式中已指定的属性。

### 块格式

`blockFormat()` 读取当前块的段落格式，例如对齐、缩进、段前段后间距。`setBlockFormat()` 直接设置覆盖，`mergeBlockFormat()` 只修改传入的字段。选区跨多个块时，块格式操作会作用于选区覆盖的块。

### 块字符格式

`blockCharFormat()`、`setBlockCharFormat()` 和 `mergeBlockCharFormat()` 用于块级默认字符格式。它们不是给每个已有字符逐一设置格式，而是影响块中没有显式字符格式的内容以及后续插入文本的格式。需要给已选文本着色时，应使用 `setCharFormat()` 或 `mergeCharFormat()`。

## 6. 结构化插入

- `insertBlock()` 插入段落分隔，重载允许同时指定块格式和块字符格式；
- `insertList()` 将当前块或当前选区纳入新列表；
- `createList()` 创建列表对象并把当前块纳入其中，适合从已有块建立列表；
- `insertTable()` 插入指定行列的表格。行数和列数应为正数，零或负数没有有意义的表格结构；
- `insertFrame()` 插入文本框架；
- `insertFragment()` 插入保留结构和格式的文档片段；
- `insertHtml()` 按 Qt 富文本 HTML 解析后插入；
- `insertMarkdown()` 按指定 Markdown 方言解析后插入，Qt 6.4 起提供；
- `insertImage()` 插入图片对象，图片实际数据通常通过文档资源系统解析。

插入结构对象后，返回的 `QTextList*`、`QTextTable*` 或 `QTextFrame*` 由文档管理，调用方不负责 `delete`。这些指针只在关联文档仍存活、对象尚未从文档结构中移除时有效。

`insertHtml()` 与 `insertMarkdown()` 不是通用浏览器或完整 Markdown 引擎。支持的标签、CSS、扩展语法和资源类型由 Qt 的富文本解析器决定；不可信输入仍需在业务层做安全过滤。

## 7. 编辑事务、撤销和光标跟随

`beginEditBlock()` 与 `endEditBlock()` 把一段连续编辑合并为一个撤销命令。它们应成对出现，即使中途发生逻辑分支，也应保证最终调用 `endEditBlock()`。

`joinPreviousEditBlock()` 把当前编辑加入前一个编辑块，适合把连续事件合并为一次用户可见操作。它不是“开始新事务”的替代品，调用前必须有可加入的前一编辑块。

`setKeepPositionOnInsert(true)` 控制在光标当前位置插入内容时，光标是否保持在插入内容之前。默认行为通常会让光标跟随插入内容移动；需要维护固定书签、语法标记或并行扫描位置时才启用它。它只影响插入位置的跟随策略，不会阻止文档修改。

`isCopyOf()` 用于判断两个光标是否仍共享同一内部光标数据。`QTextCursor` 是隐式共享类型，复制成本低；对其中一个光标修改时可能发生写时复制，因此不能用 `isCopyOf()` 判断两个光标在文档中的位置是否相等。位置排序和相等比较应使用 `==`、`<` 等运算符，并确保光标属于同一文档语境。

## 8. 无效光标、生命周期和线程边界

默认构造的光标是 null 光标：`isNull()` 为 `true`，没有关联文档。由无效文档、无效块或已失效结构得到的光标也不应继续执行编辑操作；先检查 `document()`、`isNull()` 和相关对象指针。

光标不拥有 `QTextDocument`。文档销毁后，光标不能再用于访问或修改内容，即使光标对象本身还在作用域中。文档编辑会调整活动光标的位置，但应用不应把位置整数长期缓存后直接复用；需要长期跟踪时保留 `QTextCursor`，或监听文档的 `contentsChange()`。

`QTextCursor` 是值类型，但它关联的是可变文档状态。不要在多个线程同时操作同一文档或其光标。后台线程若要处理文本，应在后台线程使用独立文档副本，完成后通过信号把结果交回 GUI 线程。

## 9. 常见使用片段

### 查找并替换

```cpp
QTextCursor cursor = document->find("TODO");
if (!cursor.isNull()) {
    cursor.insertText("DONE");
}
```

查找失败时返回的光标没有有效选区，不能仅用 `hasSelection()` 判断成功；应同时检查 `isNull()` 或 `document() != nullptr`。

### 给选区设置格式

```cpp
QTextCursor cursor = editor->textCursor();
if (cursor.hasSelection()) {
    QTextCharFormat format;
    format.setForeground(Qt::red);
    cursor.mergeCharFormat(format);
    editor->setTextCursor(cursor);
}
```

### 批量插入并合并撤销

```cpp
QTextCursor cursor(document);
cursor.movePosition(QTextCursor::End);
cursor.beginEditBlock();
cursor.insertText("first");
cursor.insertBlock();
cursor.insertText("second");
cursor.endEditBlock();
```

## API 速查表
| API | 用途与关键语义 | 边界、默认值或注意事项 |
| --- | --- | --- |
| `QTextCursor()` | 创建 null 光标。 | 没有关联文档，先用 `isNull()` 判断。 |
| `QTextCursor(QTextDocument *document)` | 创建关联文档的光标，初始在文档起点。 | 不取得文档所有权；传入 `nullptr` 得到无效语境。 |
| `QTextCursor(QTextFrame *frame)` | 创建框架内容范围内的光标。 | 框架必须属于仍存活的文档；不拥有框架。 |
| `QTextCursor(const QTextBlock &block)` | 创建位于块起点的光标。 | 块无效时不能进行有效编辑。 |
| `QTextCursor(const QTextCursor &cursor)` | 复制光标状态。 | 值语义、隐式共享；不复制文档。 |
| `operator=(const QTextCursor &other)` | 赋值光标状态。 | 目标光标改为指向同一文档语境的位置。 |
| `~QTextCursor()` | 释放光标自身的共享数据。 | 不销毁关联文档或结构对象。 |
| `swap(QTextCursor &other)` | 交换两个光标状态。 | `noexcept`；不修改文档内容。 |
| `isNull()` | 判断是否没有有效内部光标。 | null 光标不可用于正常编辑。 |
| `setPosition(int pos, MoveMode mode = MoveAnchor)` | 设置当前位置。 | `pos` 受文档有效位置范围约束；`MoveAnchor` 会清除选区，`KeepAnchor` 保留锚点。 |
| `position()` | 返回当前位置。 | 是插入点，不是“当前字符编号”。 |
| `positionInBlock()` | 返回当前位置相对当前块起点的偏移。 | 无效光标时不要把结果当作有效列号。 |
| `anchor()` | 返回选区锚点。 | 与当前位置不同才表示有选区。 |
| `insertText(const QString &text)` | 在当前位置插入文本，或替换选区。 | 空字符串不产生可见文本；会参与撤销。 |
| `insertText(const QString &, const QTextCharFormat &format)` | 以指定字符格式插入或替换文本。 | 只影响插入文本，不等同于给后续整块设置默认格式。 |
| `movePosition(MoveOperation op, MoveMode mode = MoveAnchor, int n = 1)` | 按字符、单词、块、行或表格结构移动。 | 到边界返回 `false`；`n` 表示重复次数，视觉行操作依赖布局。 |
| `visualNavigation()` | 查询是否按视觉顺序导航。 | 影响双向文本中的左右移动语义。 |
| `setVisualNavigation(bool b)` | 设置左右导航是否按视觉方向。 | 只改变导航规则，不改变文本顺序。 |
| `setVerticalMovementX(int x)` | 设置上下移动时保存的目标横坐标。 | 通常由编辑器维护；不应每次按键都重置。 |
| `verticalMovementX()` | 读取上下移动的目标横坐标。 | 主要用于连续 `Up` / `Down`。 |
| `setKeepPositionOnInsert(bool b)` | 设置插入发生在光标处时是否保持原位置。 | 默认值由 Qt 光标状态初始化；只影响位置跟随。 |
| `keepPositionOnInsert()` | 查询插入位置跟随策略。 | 适合书签或扫描光标场景。 |
| `deleteChar()` | 删除光标后的字符、对象或选区相关内容。 | 在文档末尾通常无内容可删；组合字符边界要按 Qt 文本位置处理。 |
| `deletePreviousChar()` | 删除光标前的字符、对象或选区相关内容。 | 在文档起点无内容可删。 |
| `select(SelectionType selection)` | 选择当前单词、视觉行、块或整个文档。 | `LineUnderCursor` 依赖布局；`Document` 会覆盖整个文档。 |
| `hasSelection()` | 判断是否存在普通线性选区。 | 选区为空时为 `false`。 |
| `hasComplexSelection()` | 判断是否存在表格等复杂结构选区。 | 复杂选区不应只按连续字符串处理。 |
| `removeSelectedText()` | 删除当前选区。 | 删除后光标落在选区起点，撤销记录由文档管理。 |
| `clearSelection()` | 清除选区并保留当前位置。 | 等价于让锚点回到当前位置。 |
| `selectionStart()` | 返回选区较小的位置。 | 无选区时通常等于当前位置。 |
| `selectionEnd()` | 返回选区较大的位置。 | 无选区时通常等于当前位置。 |
| `selectedText()` | 返回选区纯文本。 | 段落分隔可能以 `QChar::ParagraphSeparator` 表示；不会保留格式。 |
| `selection()` | 返回保留格式和结构的 `QTextDocumentFragment`。 | 片段是值对象；资源仍按文档资源机制解析。 |
| `selectedTableCells(...)` | 输出表格选区的首行、行数、首列、列数。 | 输出指针必须非空；普通线性选区不应当作表格矩形。 |
| `block()` | 返回当前位置所在的 `QTextBlock`。 | 当前位置在块分隔边界时要结合实际块位置判断。 |
| `charFormat()` | 读取当前位置的字符格式。 | 混合选区不能据此推断所有字符格式一致。 |
| `setCharFormat(const QTextCharFormat &format)` | 直接设置选区或当前位置字符格式。 | 覆盖对应格式属性；给新文本指定格式可用 `insertText` 重载。 |
| `mergeCharFormat(const QTextCharFormat &modifier)` | 将已指定的字符格式属性合并到选区。 | 未指定属性保持不变，适合加粗、改颜色等局部操作。 |
| `blockFormat()` | 读取当前块的段落格式。 | 选区跨块时读取的是当前光标所在块。 |
| `setBlockFormat(const QTextBlockFormat &format)` | 设置选区覆盖块的段落格式。 | 会替换相关块格式；跨块时应确认范围。 |
| `mergeBlockFormat(const QTextBlockFormat &modifier)` | 合并选区覆盖块的段落格式。 | 未指定属性保持原值。 |
| `blockCharFormat()` | 读取当前块的默认字符格式。 | 不等于每个已有字符的实际格式。 |
| `setBlockCharFormat(const QTextCharFormat &format)` | 设置选区覆盖块的默认字符格式。 | 主要影响块默认值和后续输入。 |
| `mergeBlockCharFormat(const QTextCharFormat &modifier)` | 合并块默认字符格式。 | 需要给已有文本着色时使用字符格式 API。 |
| `atBlockStart()` | 判断是否在块起点。 | 视觉行起点和块起点不是同一概念。 |
| `atBlockEnd()` | 判断是否在块末。 | 块分隔符边界要结合 `positionInBlock()` 理解。 |
| `atStart()` | 判断是否在文档起点。 | 无效光标不应视为有效文档起点。 |
| `atEnd()` | 判断是否在文档终点。 | 文档终点是可插入位置，不代表最后一个可见字符。 |
| `insertBlock()` | 插入一个新块。 | 当前选区会被替换；新块使用当前格式上下文。 |
| `insertBlock(const QTextBlockFormat &format)` | 插入带块格式的新块。 | 块格式控制对齐、缩进、间距等段落属性。 |
| `insertBlock(const QTextBlockFormat &, const QTextCharFormat &)` | 同时指定块格式和块默认字符格式。 | 适合程序化生成段落。 |
| `insertList(const QTextListFormat &format)` | 将当前位置或选区创建为指定格式的列表。 | 返回文档拥有的 `QTextList*`。 |
| `insertList(QTextListFormat::Style style)` | 用列表样式创建列表。 | 样式只决定编号/项目符号等列表表现。 |
| `createList(const QTextListFormat &format)` | 从当前块创建列表对象。 | 与 `insertList` 的具体适用范围不同，确认当前块是否已在列表中。 |
| `createList(QTextListFormat::Style style)` | 用样式创建列表。 | 返回指针不由调用方释放。 |
| `currentList()` | 返回当前位置所属列表。 | 不在列表中返回 `nullptr`。 |
| `insertTable(int rows, int cols)` | 插入指定行列的表格。 | 行列应为正数；返回文档拥有的 `QTextTable*`。 |
| `insertTable(int rows, int cols, const QTextTableFormat &format)` | 插入带表格格式的表格。 | 格式控制边框、间距、宽度和对齐等布局属性。 |
| `currentTable()` | 返回当前位置所属表格。 | 不在表格中返回 `nullptr`。 |
| `insertFrame(const QTextFrameFormat &format)` | 插入文本框架并返回它。 | 框架由文档管理；格式中的边距、边框和位置影响布局。 |
| `currentFrame()` | 返回当前位置所在的最内层框架。 | 根框架和普通框架要区分；无效光标返回空指针。 |
| `insertFragment(const QTextDocumentFragment &fragment)` | 插入保留格式的文档片段。 | 目标选区会被替换；片段不拥有原文档。 |
| `insertHtml(const QString &html)` | 解析 Qt 支持的富文本 HTML 并插入。 | 不是完整浏览器 HTML；资源和 CSS 支持受 Qt 富文本实现限制。 |
| `insertMarkdown(const QString &, QTextDocument::MarkdownFeatures features = MarkdownDialectGitHub)` | 解析 Markdown 并插入。 | Qt 6.4 起；方言和 HTML 支持由 `features` 决定。 |
| `insertImage(const QTextImageFormat &format)` | 按图像格式插入图像对象。 | `name` 通常用于从文档资源系统查找图像。 |
| `insertImage(const QTextImageFormat &, QTextFrameFormat::Position alignment)` | 插入带浮动/定位方式的图像。 | 对齐属于框架位置语义，不能只靠字符对齐理解。 |
| `insertImage(const QString &name)` | 按资源名称插入图像。 | 文档必须能通过资源 provider 或 `addResource()` 找到资源。 |
| `insertImage(const QImage &, const QString &name = QString())` | 把 `QImage` 作为资源并插入。 | 空名称由 Qt 生成或使用内部资源；需要跨文档保存时应规划资源名。 |
| `beginEditBlock()` | 开始合并撤销的编辑块。 | 必须和 `endEditBlock()` 配对。 |
| `joinPreviousEditBlock()` | 将编辑加入上一个编辑块。 | 只有存在可连接的前一编辑块时才有意义。 |
| `endEditBlock()` | 结束当前编辑块。 | 忘记调用会破坏预期的撤销粒度。 |
| `operator==` / `operator!=` | 比较两个光标是否表示相同位置和选区状态。 | 两个光标应属于相同文档语境；不等同于 `isCopyOf()`。 |
| `operator<` / `operator<=` / `operator>` / `operator>=` | 按文档位置比较光标。 | 只适合可比较的同一文档光标；选区锚点不会改变当前位置排序的基本用途。 |
| `isCopyOf(const QTextCursor &other)` | 判断内部光标数据是否仍为同一份共享副本。 | 写时复制后可能变为 `false`；不要用它判断位置相等。 |
| `blockNumber()` | 返回当前块编号。 | 通常从零开始；无效光标返回无效值，不能当作正常块号。 |
| `columnNumber()` | 返回当前块中的列位置。 | 对制表符、复杂脚本和视觉布局，不一定等于像素列或屏幕列。 |
| `document()` | 返回关联文档。 | 光标不拥有文档；无效光标返回 `nullptr`。 |

## 11. 记忆重点

把 `QTextCursor` 记成“文档上的可编辑范围”最实用：先确认它关联哪个文档，再用位置/锚点构造选区，最后选择文本 API、格式 API 或结构 API。凡是涉及撤销粒度、视觉行、表格单元格和资源的代码，都应显式处理相应边界，而不要把它退化成普通 `QString` 下标。
