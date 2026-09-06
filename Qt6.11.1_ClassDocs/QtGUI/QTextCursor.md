# QTextCursor

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QTextCursor` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QTextCursor>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

### 状态、生命周期和线程

**生命周期：** 先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

**状态与结果：** 把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

**线程与事件循环：** 如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

## 3. 直接使用

围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum MoveMode { MoveAnchor, KeepAnchor }`
- `enum MoveOperation { NoMove, Start, StartOfLine, StartOfBlock, StartOfWord, …, PreviousRow }`
- `enum SelectionType { Document, BlockUnderCursor, LineUnderCursor, WordUnderCursor }`

### 公有函数

- `QTextCursor()`
- `QTextCursor(QTextDocument *document)`
- `QTextCursor(QTextFrame *frame)`
- `QTextCursor(const QTextBlock &block)`
- `QTextCursor(const QTextCursor &cursor)`
- `~QTextCursor()`
- `int anchor() const`
- `bool atBlockEnd() const`
- `bool atBlockStart() const`
- `bool atEnd() const`
- `bool atStart() const`
- `void beginEditBlock()`
- `QTextBlock block() const`
- `QTextCharFormat blockCharFormat() const`
- `QTextBlockFormat blockFormat() const`
- `int blockNumber() const`
- `QTextCharFormat charFormat() const`
- `void clearSelection()`
- `int columnNumber() const`
- `QTextList * createList(const QTextListFormat &format)`
- `QTextList * createList(QTextListFormat::Style style)`
- `QTextFrame * currentFrame() const`
- `QTextList * currentList() const`
- `QTextTable * currentTable() const`
- `void deleteChar()`
- `void deletePreviousChar()`
- `QTextDocument * document() const`
- `void endEditBlock()`
- `bool hasComplexSelection() const`
- `bool hasSelection() const`
- `void insertBlock()`
- `void insertBlock(const QTextBlockFormat &format)`
- `void insertBlock(const QTextBlockFormat &format, const QTextCharFormat &charFormat)`
- `void insertFragment(const QTextDocumentFragment &fragment)`
- `QTextFrame * insertFrame(const QTextFrameFormat &format)`
- `void insertHtml(const QString &html)`
- `void insertImage(const QTextImageFormat &format)`
- `void insertImage(const QString &name)`
- `void insertImage(const QImage &image, const QString &name = QString())`
- `void insertImage(const QTextImageFormat &format, QTextFrameFormat::Position alignment)`
- `QTextList * insertList(const QTextListFormat &format)`
- `QTextList * insertList(QTextListFormat::Style style)`
- `(since 6.4) void insertMarkdown(const QString &markdown, QTextDocument::MarkdownFeatures features = QTextDocument::MarkdownDialectGitHub)`
- `QTextTable * insertTable(int rows, int columns, const QTextTableFormat &format)`
- `QTextTable * insertTable(int rows, int columns)`
- `void insertText(const QString &text)`
- `void insertText(const QString &text, const QTextCharFormat &format)`
- `bool isCopyOf(const QTextCursor &other) const`
- `bool isNull() const`
- `void joinPreviousEditBlock()`
- `bool keepPositionOnInsert() const`
- `void mergeBlockCharFormat(const QTextCharFormat &modifier)`
- `void mergeBlockFormat(const QTextBlockFormat &modifier)`
- `void mergeCharFormat(const QTextCharFormat &modifier)`
- `bool movePosition(QTextCursor::MoveOperation operation, QTextCursor::MoveMode mode = MoveAnchor, int n = 1)`
- `int position() const`
- `int positionInBlock() const`
- `void removeSelectedText()`
- `void select(QTextCursor::SelectionType selection)`
- `void selectedTableCells(int *firstRow, int *numRows, int *firstColumn, int *numColumns) const`
- `QString selectedText() const`
- `QTextDocumentFragment selection() const`
- `int selectionEnd() const`
- `int selectionStart() const`
- `void setBlockCharFormat(const QTextCharFormat &format)`
- `void setBlockFormat(const QTextBlockFormat &format)`
- `void setCharFormat(const QTextCharFormat &format)`
- `void setKeepPositionOnInsert(bool b)`
- `void setPosition(int pos, QTextCursor::MoveMode m = MoveAnchor)`
- `void setVerticalMovementX(int x)`
- `void setVisualNavigation(bool b)`
- `void swap(QTextCursor &other)`
- `int verticalMovementX() const`
- `bool visualNavigation() const`
- `bool operator!=(const QTextCursor &other) const`
- `bool operator<(const QTextCursor &other) const`
- `bool operator<=(const QTextCursor &other) const`
- `QTextCursor & operator=(const QTextCursor &cursor)`
- `bool operator==(const QTextCursor &other) const`
- `bool operator>(const QTextCursor &other) const`
- `bool operator>=(const QTextCursor &other) const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QTextCursor::MoveMode`

**作用与语义：**

- `QTextCursor::MoveAnchor`: `0`; 将锚点移动到与光标相同的位置。
- `QTextCursor::KeepAnchor`: `1`; 保持锚点的位置不变。
如果 `anchor()` 保持在原地，而 `position()` 被移动，则中间的文本将被选中。

### `enum QTextCursor::MoveOperation`

**作用与语义：**

- `QTextCursor::NoMove`：`0`;保持光标原位
- `QTextCursor::Start`：`1`;移动到文档开头。
- `QTextCursor::StartOfLine`：`3`;移动到当前队列的起点。
- `QTextCursor::StartOfBlock`：`4`;移动到当前方块的起点。
- `QTextCursor::StartOfWord`：`5`;移动到当前单词的开头。
- `QTextCursor::PreviousBlock`：`6`;移动到上一个方块的起点。
- `QTextCursor::PreviousCharacter`：`7`;移动到前一个角色。
- `QTextCursor::PreviousWord`：`8`;移到上一个单词的开头。
- `QTextCursor::Up`：`2`;前进一行。
- `QTextCursor::Left`：`9`;向左移动一个角色。
- `QTextCursor::WordLeft`：`10`;向左移动一个单词。
- `QTextCursor::End`：`11`;移到文档末尾。
- `QTextCursor::EndOfLine`：`13`;移动到当前行的末尾。
- `QTextCursor::EndOfWord`：`14`;移动到当前单词的末尾。
- `QTextCursor::EndOfBlock`：`15`;移动到当前区块的末尾。
- `QTextCursor::NextBlock`：`16`;移动到下一个方块的起点。
- `QTextCursor::NextCharacter`：`17`;进入下一个角色。
- `QTextCursor::NextWord`：`18`;进入下一个单词。
- `QTextCursor::Down`：`12`;往前走一行。
- `QTextCursor::Right`：`19`;向右移动一个角色。
- `QTextCursor::WordRight`：`20`;向右移动一个字。
- `QTextCursor::NextCell`：`21`;移动到当前表中下一个表单元的开头。如果当前单元格是该行的最后一个单元格，光标将移动到下一行的第一个单元格。
- `QTextCursor::PreviousCell`：`22`;在当前表中移动到上一个表单元格的开头。如果当前单元格是该行的第一个单元格，光标将移动到上一行的最后一个单元格。
- `QTextCursor::NextRow`：`23`;移动到当前表下一行的第一个新单元格。
- `QTextCursor::PreviousRow`：`24`;移动到当前表格中上一行的最后一个单元格。

### `enum QTextCursor::SelectionType`

**作用与语义：**

该枚举描述了可以用`select()`函数应用的选择类型。
- `QTextCursor::Document`：`3`;选择整个文档。
- `QTextCursor::BlockUnderCursor`：`2`;选择光标下方的文本区块。
- `QTextCursor::LineUnderCursor`：`1`;选择光标下方的文本行。
- `QTextCursor::WordUnderCursor`：`0`;选择光标下方的单词。如果光标不位于可选字符串中，则不会选择任何文本。

### `QTextCursor::QTextCursor()`

**作用与语义：**

构造一个空光标。

### `[explicit] QTextCursor::QTextCursor(QTextDocument *document)`

**作用与语义：**

构建一个指向`document`起点的光标。

### `[explicit] QTextCursor::QTextCursor(QTextFrame *frame)`

**作用与语义：**

构建一个指向`frame`起点的光标。

### `[explicit] QTextCursor::QTextCursor(const QTextBlock &block)`

**作用与语义：**

构建一个指向`block`起点的光标。

### `QTextCursor::QTextCursor(const QTextCursor &cursor)`

**作用与语义：**

构建一个新的光标，复制了`cursor`。

### `[noexcept] QTextCursor::~QTextCursor()`

**作用与语义：**

摧毁了`QTextCursor`。

### `int QTextCursor::anchor() const`

**作用与语义：**

返回锚点位置;这与`position()`相同，除非存在选择，此时`position()`标记选区的一端，anchor()标记另一端。就像光标位置一样，锚点位置位于字符之间。

### `bool QTextCursor::atBlockEnd() const`

**作用与语义：**

如果光标位于方块末尾，返回`true`;否则返回`false`。

### `bool QTextCursor::atBlockStart() const`

**作用与语义：**

如果光标位于块起点，返回`true`;否则返回`false`。

### `bool QTextCursor::atEnd() const`

**作用与语义：**

如果光标位于文档末尾，返回`true`;否则返回`false`。

### `bool QTextCursor::atStart() const`

**作用与语义：**

如果光标位于文档开头，返回`true`;否则返回`false`。

### `void QTextCursor::beginEditBlock()`

**作用与语义：**

表示文档上编辑操作块的开始，从撤销/重做视角应显示为单一操作。
调用撤销()会导致两个插入都被撤销，从而删除“World”和“Hello”。
可以嵌套调用以开始EditBlock和`endEditBlock`。最顶端的调用对决定撤销/重做操作的范围。

**官方示例：**

```cpp
 QTextCursor cursor(textDocument);
 cursor.beginEditBlock();
 cursor.insertText("Hello");
 cursor.insertText("World");
 cursor.endEditBlock();

 textDocument->undo();
```

### `QTextBlock QTextCursor::block() const`

**作用与语义：**

返回包含光标的方块。

### `QTextCharFormat QTextCursor::blockCharFormat() const`

**作用与语义：**

返回光标所在方块的方块字符格式。
块字符格式是用来插入空块开头文本的格式。

### `QTextBlockFormat QTextCursor::blockFormat() const`

**作用与语义：**

返回光标所在方块的块格式。

### `int QTextCursor::blockNumber() const`

**作用与语义：**

返回光标所在方块的编号，若光标无效则返回0。
注意，这个函数只在没有复杂对象（如表格或框架）的文档中才有意义。

### `QTextCharFormat QTextCursor::charFormat() const`

**作用与语义：**

返回光标`position()`前字符的格式。如果光标位于非空的文本块开头，则返回光标后紧接字符的格式。

### `void QTextCursor::clearSelection()`

**作用与语义：**

通过将锚点设置为光标位置来清除当前选择。
注意，它不会删除所选文本。

### `int QTextCursor::columnNumber() const`

**作用与语义：**

返回光标在其包含行内的位置。
注意，这是相对于换行行的列号，而不是相对于块（即段落）。
你可能更应该打电话给`positionInBlock()`。

### `QTextList *QTextCursor::createList(const QTextListFormat &format)`

**作用与语义：**

创建并返回一个包含给定`format`的新列表，并将当前段落的光标置于第一个列表项。

### `QTextList *QTextCursor::createList(QTextListFormat::Style style)`

**作用与语义：**

创建并返回一个包含给定`style`的新列表，使光标当前段落成为第一个列表项。
所使用的样式由`QTextListFormat::Style`枚举定义。

### `QTextFrame *QTextCursor::currentFrame() const`

**作用与语义：**

返回当前帧的指针。如果光标无效，返回`nullptr`。

### `QTextList *QTextCursor::currentList() const`

**作用与语义：**

如果光标`position()`在属于列表的块内，则返回当前列表;否则返回`nullptr`。

### `QTextTable *QTextCursor::currentTable() const`

**作用与语义：**

如果光标`position()`在属于该表的块内，则返回当前表的指针;否则返回`nullptr`。

### `void QTextCursor::deleteChar()`

**作用与语义：**

如果没有被选中的文本，则删除当前光标位置的字符;否则，删除所选文本。

### `void QTextCursor::deletePreviousChar()`

**作用与语义：**

如果没有选中的文本，则删除当前光标位置之前的字符;否则，删除所选文本。

### `QTextDocument *QTextCursor::document() const`

**作用与语义：**

返回该光标关联的文档。

### `void QTextCursor::endEditBlock()`

**作用与语义：**

表示文档上应作为单一操作从撤销/重做视角显示的编辑操作块结束。

### `bool QTextCursor::hasComplexSelection() const`

**作用与语义：**

如果光标包含的选择不是单纯从`selectionStart()`到`selectionEnd()`的范围，返回`true`;否则返回`false`。
复选区是指跨越表中至少两个单元格的选区;其范围由`selectedTableCells()`指定。

### `bool QTextCursor::hasSelection() const`

**作用与语义：**

如果光标包含选择，返回`true`;否则返回`false`。

### `void QTextCursor::insertBlock()`

**作用与语义：**

在光标`position()`插入一个新的空块，并带有当前`blockFormat()`和`charFormat()`。

### `void QTextCursor::insertBlock(const QTextBlockFormat &format)`

**作用与语义：**

在光标`position()`插入一个新的空块，块格式为`format`，当前`charFormat()`为块字符格式。

### `void QTextCursor::insertBlock(const QTextBlockFormat &format, const QTextCharFormat &charFormat)`

**作用与语义：**

在光标`position()`插入一个新的空块，块格式为`format`，`charFormat`为块字符格式。

### `void QTextCursor::insertFragment(const QTextDocumentFragment &fragment)`

**作用与语义：**

在当前`position()`插入文本`fragment`。

### `QTextFrame *QTextCursor::insertFrame(const QTextFrameFormat &format)`

**作用与语义：**

在当前光标`position()`插入一个具有给定`format`的帧，将光标`position()`入帧内，返回帧。
如果光标保留一个选区，整个选区会被移动到画面内。

### `void QTextCursor::insertHtml(const QString &html)`

**作用与语义：**

在当前`position()`插入文本`html`。文本被解释为HTML格式。
注意：当该函数与样式表一起使用时，样式表只会应用到文档当前的块。要在整个文档中应用样式表，请使用`QTextDocument::setDefaultStyleSheet()`。

### `void QTextCursor::insertImage(const QTextImageFormat &format)`

**作用与语义：**

插入由`format`定义的图像在当前`position()`。

### `void QTextCursor::insertImage(const QString &name)`

**作用与语义：**

方便地将给定`name`图像插入当前`position()`。

**官方示例：**

```cpp
 QImage img;
 textDocument->addResource(QTextDocument::ImageResource, QUrl("myimage"), img);
 cursor.insertImage("myimage");
```

### `void QTextCursor::insertImage(const QImage &image, const QString &name = QString())`

**作用与语义：**

方便插入给定`image`，当前`position()`可选`name`。

### `void QTextCursor::insertImage(const QTextImageFormat &format, QTextFrameFormat::Position alignment)`

**作用与语义：**

将给定`format`定义的图像插入光标当前位置和指定`alignment`。

### `QTextList *QTextCursor::insertList(const QTextListFormat &format)`

**作用与语义：**

在当前位置插入一个新块，并将其作为新创建列表的第一个项，并以给定`format`。返回已创建的列表。

### `QTextList *QTextCursor::insertList(QTextListFormat::Style style)`

**作用与语义：**

在当前位置插入一个新块，并将其作为新创建列表的第一个项，并以给定`style`。返回已创建的列表。

### `[since 6.4] void QTextCursor::insertMarkdown(const QString &markdown, QTextDocument::MarkdownFeatures features = QTextDocument::MarkdownDialectGitHub)`

**作用与语义：**

在当前`position()`插入`markdown`文本，并使用指定的Markdown `features`。默认是GitHub方言。

### `QTextTable *QTextCursor::insertTable(int rows, int columns, const QTextTableFormat &format)`

**作用与语义：**

创建一个新表，指定`format`中`rows`和`columns`数量，插入文档当前光标`position()`，返回表对象。光标移至第一个单元格的开头。
表格中必须至少有一行和一列。

### `QTextTable *QTextCursor::insertTable(int rows, int columns)`

**作用与语义：**

创建一个新表，包含给定数量的`rows`和`columns`，插入到文档当前光标`position()`，返回表对象。光标被移动到第一个单元格的开头。
表格中必须至少有一行和一列。

### `void QTextCursor::insertText(const QString &text)`

**作用与语义：**

在当前位置插入`text`，使用当前字符格式。
如果存在选择，该选择会被删除并替换为`text`，例如：
这会清除所有现有的选择，选择光标处的单词（即从前`position()`开始），并用“Hello World”替换该选项。
插入文本中的任何 ASCII 换行字符（\n）都被转换为 Unicode 区块分隔符，对应`insertBlock()`调用。

**官方示例：**

```cpp
 cursor.clearSelection();
 cursor.movePosition(QTextCursor::NextWord, QTextCursor::KeepAnchor);
 cursor.insertText("Hello World");
```

### `void QTextCursor::insertText(const QString &text, const QTextCharFormat &format)`

**作用与语义：**

插入`text`在当前位置，`format`。

### `bool QTextCursor::isCopyOf(const QTextCursor &other) const`

**作用与语义：**

返回`true`如果该光标和`other`彼此是复制品，即其中一个作为另一个的复制品创建，且自此未曾移动。这比等式更为严格。

### `bool QTextCursor::isNull() const`

**作用与语义：**

如果光标为空，返回`true`;否则返回`false`。空光标由默认构造函数创建。

### `void QTextCursor::joinPreviousEditBlock()`

**作用与语义：**

类似`beginEditBlock()`表示编辑操作块的开始，这些操作应作为撤销/重做的单一操作出现。但与`beginEditBlock()`不同的是，它不会启动新块，而是反转之前对`endEditBlock()`的调用，因此后续操作成为之前创建的编辑块的一部分。
调用撤销()会导致所有三个插入都被撤销。

**官方示例：**

```cpp
 QTextCursor cursor(textDocument);
 cursor.beginEditBlock();
 cursor.insertText("Hello");
 cursor.insertText("World");
 cursor.endEditBlock();

 // ...

 cursor.joinPreviousEditBlock();
 cursor.insertText("Hey");
 cursor.endEditBlock();

 textDocument->undo();
```

### `bool QTextCursor::keepPositionOnInsert() const`

**作用与语义：**

返回在插入文本时光标是否应保持当前位置。
默认是假的;

### `void QTextCursor::mergeBlockCharFormat(const QTextCharFormat &modifier)`

**作用与语义：**

修改当前块（或所有包含在选择中的块）的块字符格式，并按照`modifier`指定的块格式。

### `void QTextCursor::mergeBlockFormat(const QTextBlockFormat &modifier)`

**作用与语义：**

修改当前块（或所有包含在选择中的块）的块格式，并按照`modifier`指定的块格式。

### `void QTextCursor::mergeCharFormat(const QTextCharFormat &modifier)`

**作用与语义：**

将光标当前字符格式与格式`modifier`描述的属性合并。如果光标有选择，该函数将`modifier`中设置的所有属性应用到所有包含该选择的字符格式上。

### `bool QTextCursor::movePosition(QTextCursor::MoveOperation operation, QTextCursor::MoveMode mode = MoveAnchor, int n = 1)`

**作用与语义：**

通过执行指定`operation` `n`次、指定`mode`移动光标，如果所有操作成功返回`true`;否则返回`false`。
例如，如果该函数反复使用来寻找下一个单词的结尾，最终在到达文档末尾时会失败。
默认情况下，移动操作只执行一次（`n` = 1）。
如果`mode` `KeepAnchor`，光标会选择它移动的文本。这与用户按住Shift键并用光标键移动光标时的效果相同。

### `int QTextCursor::position() const`

**作用与语义：**

返回文档中光标的绝对位置。光标位于字符之间。
注意：此处的“字符”指的是`QChar`对象串，即16位Unicode字符，位置被视为该字符串的索引。这不一定对应书写系统中的单个字素，因为单个字素可能由多个Unicode字符表示，例如代理对、语言连字或变音符号。

### `int QTextCursor::positionInBlock() const`

**作用与语义：**

返回光标在方块中的相对位置。光标位于字符之间。
这相当于`position() - block().position()`。
注意：此处的“字符”指的是`QChar`对象串，即16位Unicode字符，位置被视为该字符串的索引。这不一定对应书写系统中的单个字素，因为单个字素可能由多个Unicode字符表示，例如代理对、语言连字或变音符号。

### `void QTextCursor::removeSelectedText()`

**作用与语义：**

如果存在选择，其内容会被删除;否则则无效。

### `void QTextCursor::select(QTextCursor::SelectionType selection)`

**作用与语义：**

根据给定的文字选择文档中的文本`selection`。

### `void QTextCursor::selectedTableCells(int *firstRow, int *numRows, int *firstColumn, int *numColumns) const`

**作用与语义：**

如果选择跨越表单元格，`firstRow`填充选区中第一行的编号，`firstColumn` 选区第一列的编号，`numRows` 和 `numColumns` 填充选区中的行和列数。如果选区不跨越任何表单元格，结果无害但未定义。

### `QString QTextCursor::selectedText() const`

**作用与语义：**

返回当前选择的文本（可能是空的）。这只返回文本，没有富文本格式信息。如果你想要文档片段（即格式化富文本），请使用`selection()`。
注意：如果从编辑器获得的选区跨行，文本将包含 Unicode U 2029 段分隔符，而非换行`\n`字符。使用`QString::replace()`将这些字符替换为换行。

### `QTextDocumentFragment QTextCursor::selection() const`

**作用与语义：**

返回当前选择（可能是空的）及其所有格式信息。如果你只想要选中的文本（即纯文本），可以用`selectedText()`。
注意：与`QTextDocumentFragment::toPlainText()`不同，`selectedText()`可能包含特殊的Unicode字符，如`QChar::ParagraphSeparator`。

### `int QTextCursor::selectionEnd() const`

**作用与语义：**

如果光标没有选择，则返回选择的末尾或`position()`。

### `int QTextCursor::selectionStart() const`

**作用与语义：**

如果光标没有选择，则返回选择的起点或`position()`。

### `void QTextCursor::setBlockCharFormat(const QTextCharFormat &format)`

**作用与语义：**

将当前块（或所有包含在选择中的块）的块字符格式设置为`format`。

### `void QTextCursor::setBlockFormat(const QTextBlockFormat &format)`

**作用与语义：**

将当前块（或所有包含在选择中的块）的块格式设置为`format`。

### `void QTextCursor::setCharFormat(const QTextCharFormat &format)`

**作用与语义：**

将光标当前字符格式设置为给定的`format`。如果光标有选择，则将给定的`format`应用到当前选择上。

### `void QTextCursor::setKeepPositionOnInsert(bool b)`

**作用与语义：**

定义了当文本插入到当前位置时，光标是否应保持当前位置。
如果`b`为真，光标在光标位置插入文本时，光标保持当前位置。如果`b`为假，光标随插入文本移动。
默认是假的。
注意，当文本插入于当前光标位置之前时，光标总是移动;当文本插入于当前光标位置之后时，光标始终保持其位置。

### `void QTextCursor::setPosition(int pos, QTextCursor::MoveMode m = MoveAnchor)`

**作用与语义：**

将光标移动到文档中的绝对位置，使用`pos`指定的`m`指定的`MoveMode`。光标位于字符之间。
注意：此处的“字符”指的是`QChar`对象串，即16位Unicode字符，`pos`被视为该字符串的索引。这不一定对应书写系统中的单个字素，因为单个字素可能由多个Unicode字符表示，例如代理对、语言连字或变音符号。如需更通用的文档导航方式，可以使用`movePosition()`，它会尊重文本中的实际字素边界。

### `void QTextCursor::setVerticalMovementX(int x)`

**作用与语义：**

将垂直光标移动的视觉x位置设置为`x`。
当光标水平移动时，垂直移动的 x 位置会自动清除，垂直移动时保持不变。该机制允许光标沿视觉上直线上下移动，字体比例一致，并能轻柔地“跳跃”在短线上。
值为-1表示没有预定义的x位置。当光标下次上下移动时，该位置会自动设置。

### `void QTextCursor::setVisualNavigation(bool b)`

**作用与语义：**

将视觉导航设置为`b`。
可视化导航意味着跳过隐藏的文本段落。默认是false。

### `[noexcept] void QTextCursor::swap(QTextCursor &other)`

**作用与语义：**

将文本光标实例与`other`交换。该操作非常快速且从未失败。

### `int QTextCursor::verticalMovementX() const`

**作用与语义：**

返回垂直光标移动的视觉 x 位置。
值为-1表示没有预定义的x位置。当光标下次上下移动时，该位置会自动设置。

### `bool QTextCursor::visualNavigation() const`

**作用与语义：**

如果光标进行视觉导航，返回`true`;否则返回`false`。
可视化导航意味着跳过隐藏的文本段落。默认是false。

### `bool QTextCursor::operator!=(const QTextCursor &other) const`

**作用与语义：**

如果`other`光标在文档中与该光标不同的位置，返回`true`;否则返回`false`。

### `bool QTextCursor::operator<(const QTextCursor &other) const`

**作用与语义：**

如果`other`光标位置在文档中比该光标晚，返回`true`;否则返回`false`。

### `bool QTextCursor::operator<=(const QTextCursor &other) const`

**作用与语义：**

如果`other`光标位置较晚或与该光标在文档中相同位置，返回`true`;否则返回false。

### `QTextCursor &QTextCursor::operator=(const QTextCursor &cursor)`

**作用与语义：**

复制`cursor`并将其分配给该`QTextCursor`。注意`QTextCursor`是一个隐式共享类。

### `bool QTextCursor::operator==(const QTextCursor &other) const`

**作用与语义：**

如果`other`光标与该光标在文档中的位置相同，返回`true`;否则返回`false`。

### `bool QTextCursor::operator>(const QTextCursor &other) const`

**作用与语义：**

如果`other`光标的位置比该光标更早，返回`true`;否则返回`false`。

### `bool QTextCursor::operator>=(const QTextCursor &other) const`

**作用与语义：**

如果`other`光标位于文档中与该光标位置相同或更早的位置，返回`true`;否则返回 false。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

### 状态和错误边界

把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

### 线程边界

如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

### 最容易出现的错误

不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QTextCursor` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
