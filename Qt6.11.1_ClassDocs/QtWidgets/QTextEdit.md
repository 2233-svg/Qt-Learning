# QTextEdit

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** 多行富文本/纯文本编辑控件，负责文档编辑、光标、格式和滚动。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QTextEdit`：多行富文本/纯文本编辑控件，负责文档编辑、光标、格式和滚动。

**内部模型：** Widgets 通过父子控件树、布局系统、事件分发和重绘请求组成界面。控件的可见区域、sizeHint、sizePolicy、字体和平台 style 共同影响最终几何；用户输入先进入 Qt 事件系统，再由控件的事件函数、信号或快捷键处理。

**适用场景：** 创建 QApplication 后创建控件，设置 parent 或把控件加入布局，连接用户操作信号，再显示顶层窗口。复合界面用布局嵌套；控件尺寸异常时同时检查 sizePolicy、minimum/maximum size、layout stretch、margins 和 spacing。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要用固定坐标拼接响应式界面；不要给已经加入布局的控件反复 `setGeometry()`；不要在 `paintEvent()` 中修改业务状态；不要忘记窗口关闭、对象销毁和应用退出是三个不同事件。

## 2. 依赖与对象关系

- 头文件：`#include <QTextEdit>`
- 继承自：QAbstractScrollArea
- 直接派生类：QTextBrowser

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

Widgets 通过父子控件树、布局系统、事件分发和重绘请求组成界面。控件的可见区域、sizeHint、sizePolicy、字体和平台 style 共同影响最终几何；用户输入先进入 Qt 事件系统，再由控件的事件函数、信号或快捷键处理。

### 状态、生命周期和线程

**生命周期：** 控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

**状态与结果：** 控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

**线程与事件循环：** 所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

## 3. 直接使用

创建 QApplication 后创建控件，设置 parent 或把控件加入布局，连接用户操作信号，再显示顶层窗口。复合界面用布局嵌套；控件尺寸异常时同时检查 sizePolicy、minimum/maximum size、layout stretch、margins 和 spacing。 使用时通常按这个过程组织：构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `struct ExtraSelection`
- `flags AutoFormatting`
- `enum AutoFormattingFlag { AutoNone, AutoBulletList, AutoAll }`
- `enum LineWrapMode { NoWrap, WidgetWidth, FixedPixelWidth, FixedColumnWidth }`

### 属性

- `acceptRichText : bool`
- `autoFormatting : AutoFormatting`
- `cursorWidth : int`
- `document : QTextDocument*`
- `documentTitle : QString`
- `html : QString`
- `lineWrapColumnOrWidth : int`
- `lineWrapMode : LineWrapMode`
- `markdown : QString`
- `overwriteMode : bool`
- `placeholderText : QString`
- `plainText : QString`
- `readOnly : bool`
- `tabChangesFocus : bool`
- `tabStopDistance : qreal`
- `textInteractionFlags : Qt::TextInteractionFlags`
- `undoRedoEnabled : bool`
- `wordWrapMode : QTextOption::WrapMode`

### 公有函数

- `QTextEdit(QWidget *parent = nullptr)`
- `QTextEdit(const QString &text, QWidget *parent = nullptr)`
- `virtual ~QTextEdit()`
- `bool acceptRichText() const`
- `Qt::Alignment alignment() const`
- `QString anchorAt(const QPoint &pos) const`
- `QTextEdit::AutoFormatting autoFormatting() const`
- `bool canPaste() const`
- `QMenu * createStandardContextMenu()`
- `QMenu * createStandardContextMenu(const QPoint &position)`
- `QTextCharFormat currentCharFormat() const`
- `QFont currentFont() const`
- `QTextCursor cursorForPosition(const QPoint &pos) const`
- `QRect cursorRect() const`
- `QRect cursorRect(const QTextCursor &cursor) const`
- `int cursorWidth() const`
- `QTextDocument * document() const`
- `QString documentTitle() const`
- `void ensureCursorVisible()`
- `QList<QTextEdit::ExtraSelection> extraSelections() const`
- `bool find(const QString &exp, QTextDocument::FindFlags options = QTextDocument::FindFlags())`
- `bool find(const QRegularExpression &exp, QTextDocument::FindFlags options = QTextDocument::FindFlags())`
- `QString fontFamily() const`
- `bool fontItalic() const`
- `qreal fontPointSize() const`
- `bool fontUnderline() const`
- `int fontWeight() const`
- `bool isReadOnly() const`
- `bool isUndoRedoEnabled() const`
- `int lineWrapColumnOrWidth() const`
- `QTextEdit::LineWrapMode lineWrapMode() const`
- `virtual QVariant loadResource(int type, const QUrl &name)`
- `void mergeCurrentCharFormat(const QTextCharFormat &modifier)`
- `void moveCursor(QTextCursor::MoveOperation operation, QTextCursor::MoveMode mode = QTextCursor::MoveAnchor)`
- `bool overwriteMode() const`
- `QString placeholderText() const`
- `void print(QPagedPaintDevice *printer) const`
- `void setAcceptRichText(bool accept)`
- `void setAutoFormatting(QTextEdit::AutoFormatting features)`
- `void setCurrentCharFormat(const QTextCharFormat &format)`
- `void setCursorWidth(int width)`
- `void setDocument(QTextDocument *document)`
- `void setDocumentTitle(const QString &title)`
- `void setExtraSelections(const QList<QTextEdit::ExtraSelection> &selections)`
- `void setLineWrapColumnOrWidth(int w)`
- `void setLineWrapMode(QTextEdit::LineWrapMode mode)`
- `void setOverwriteMode(bool overwrite)`
- `void setPlaceholderText(const QString &placeholderText)`
- `void setReadOnly(bool ro)`
- `void setTabChangesFocus(bool b)`
- `void setTabStopDistance(qreal distance)`
- `void setTextCursor(const QTextCursor &cursor)`
- `void setTextInteractionFlags(Qt::TextInteractionFlags flags)`
- `void setUndoRedoEnabled(bool enable)`
- `void setWordWrapMode(QTextOption::WrapMode policy)`
- `bool tabChangesFocus() const`
- `qreal tabStopDistance() const`
- `QColor textBackgroundColor() const`
- `QColor textColor() const`
- `QTextCursor textCursor() const`
- `Qt::TextInteractionFlags textInteractionFlags() const`
- `QString toHtml() const`
- `QString toMarkdown(QTextDocument::MarkdownFeatures features = QTextDocument::MarkdownDialectGitHub) const`
- `QString toPlainText() const`
- `QTextOption::WrapMode wordWrapMode() const`

### 重实现的公有函数

- `virtual QVariant inputMethodQuery(Qt::InputMethodQuery property) const override`

### 公有槽函数

- `void append(const QString &text)`
- `void clear()`
- `void copy()`
- `void cut()`
- `void insertHtml(const QString &text)`
- `void insertPlainText(const QString &text)`
- `void paste()`
- `void redo()`
- `void scrollToAnchor(const QString &name)`
- `void selectAll()`
- `void setAlignment(Qt::Alignment a)`
- `void setCurrentFont(const QFont &f)`
- `void setFontFamily(const QString &fontFamily)`
- `void setFontItalic(bool italic)`
- `void setFontPointSize(qreal s)`
- `void setFontUnderline(bool underline)`
- `void setFontWeight(int weight)`
- `void setHtml(const QString &text)`
- `void setMarkdown(const QString &markdown)`
- `void setPlainText(const QString &text)`
- `void setText(const QString &text)`
- `void setTextBackgroundColor(const QColor &c)`
- `void setTextColor(const QColor &c)`
- `void undo()`
- `void zoomIn(int range = 1)`
- `void zoomOut(int range = 1)`

### 信号

- `void copyAvailable(bool yes)`
- `void currentCharFormatChanged(const QTextCharFormat &f)`
- `void cursorPositionChanged()`
- `void redoAvailable(bool available)`
- `void selectionChanged()`
- `void textChanged()`
- `void undoAvailable(bool available)`

### 保护函数

- `virtual bool canInsertFromMimeData(const QMimeData *source) const`
- `virtual QMimeData * createMimeDataFromSelection() const`
- `virtual void insertFromMimeData(const QMimeData *source)`

### 重实现的保护函数

- `virtual void changeEvent(QEvent *e) override`
- `virtual void contextMenuEvent(QContextMenuEvent *event) override`
- `virtual void dragEnterEvent(QDragEnterEvent *e) override`
- `virtual void dragLeaveEvent(QDragLeaveEvent *e) override`
- `virtual void dragMoveEvent(QDragMoveEvent *e) override`
- `virtual void dropEvent(QDropEvent *e) override`
- `virtual void focusInEvent(QFocusEvent *e) override`
- `virtual bool focusNextPrevChild(bool next) override`
- `virtual void focusOutEvent(QFocusEvent *e) override`
- `virtual void inputMethodEvent(QInputMethodEvent *e) override`
- `virtual void keyPressEvent(QKeyEvent *e) override`
- `virtual void keyReleaseEvent(QKeyEvent *e) override`
- `virtual void mouseDoubleClickEvent(QMouseEvent *e) override`
- `virtual void mouseMoveEvent(QMouseEvent *e) override`
- `virtual void mousePressEvent(QMouseEvent *e) override`
- `virtual void mouseReleaseEvent(QMouseEvent *e) override`
- `virtual void paintEvent(QPaintEvent *event) override`
- `virtual void resizeEvent(QResizeEvent *e) override`
- `virtual void scrollContentsBy(int dx, int dy) override`
- `virtual void showEvent(QShowEvent *) override`
- `virtual void wheelEvent(QWheelEvent *e) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QTextEdit::AutoFormattingFlagflags QTextEdit::AutoFormatting`

**作用与语义：**

- `QTextEdit::AutoNone`：`0`;不要做任何自动格式化。
- `QTextEdit::AutoBulletList`：`0x00000001`;自动创建项目符号列表（例如，当用户在最左侧列输入星号（*'）或在现有列表项中按回车时）。
- `QTextEdit::AutoAll`：`0xffffffff`;应用所有自动格式化。目前仅支持自动项目符号列表。
AutoFormatting 类型是 QFlags 的 typedef<AutoFormattingFlag>。它存储 AutoFormattingFlag 值的 OR 组合。

### `acceptRichText : bool`

**作用与语义：**

该属性决定文本编辑是否接受用户的富文本插入。
当该属性设置为虚假文本时，编辑只接受用户的纯文本输入。例如通过剪贴板或拖放。
该房产的默认情况是真实的。

**如何使用：** 调用 `acceptRichText()` 读取当前值；它不会修改应用状态。

### `autoFormatting : AutoFormatting`

**作用与语义：**

该属性包含启用的自动格式化功能集合。
该值可以是`AutoFormattingFlag`枚举中任意组合的值。默认值为`AutoNone`。选择`AutoAll`以启用所有自动格式化。
目前，唯一提供的自动格式化功能是`AutoBulletList`;未来版本的Qt可能会提供更多功能。

**如何使用：** 调用 `autoFormatting()` 读取当前值；它不会修改应用状态。

### `cursorWidth : int`

**作用与语义：**

该属性指定光标的宽度（像素单位）。默认值为1。

**如何使用：** 调用 `cursorWidth()` 读取当前值；它不会修改应用状态。

### `document : QTextDocument*`

**作用与语义：**

此属性保存文本编辑器的基础文档。
注意：除非编辑器是文档的父对象，否则编辑器不会接管文档的所有权。所提供文档的父对象仍然是该对象的所有者。如果之前分配的文档是编辑器的子对象，则该文档将被删除。

**如何使用：** 调用 `document()` 读取当前值；它不会修改应用状态。

### `documentTitle : QString`

**作用与语义：**

该属性包含从文本中解析出来的文档标题。
默认情况下，对于新创建的空文档，该属性包含空字符串。

**如何使用：** 调用 `documentTitle()` 读取当前值；它不会修改应用状态。

### `html : QString`

**作用与语义：**

该属性为文本编辑提供了HTML接口。
toHtml() 返回文本编辑的文本，表示为 html。
setHtml() 会更改文本编辑的文本。之前的文本会被删除，撤销/重做历史也会被清除。输入文本被解释为 HTML 格式的富文本。`currentCharFormat()`也会被重置，除非`textCursor()`已经在文档开头。
注意：调用者有责任确保在创建包含HTML的`QString`并传递给setHtml()时，文本正确解码。
默认情况下，对于新创建的空白文档，该属性包含描述无正文的 HTML 4.0 文档的文本。

**如何使用：** 调用 `html()` 读取当前值；它不会修改应用状态。

### `lineWrapColumnOrWidth : int`

**作用与语义：**

此属性保存文本换行的位置（以像素或字符列为单位，取决于换行模式）。
如果换行模式是 `FixedPixelWidth`，则值为从文本编辑左边缘开始换行的像素数。如果换行模式是 `FixedColumnWidth`，则值为从文本编辑左边缘开始换行的字符列号。
默认情况下，此属性包含值 0。

**如何使用：** 调用 `lineWrapColumnOrWidth()` 读取当前值；它不会修改应用状态。

### `lineWrapMode : LineWrapMode`

**作用与语义：**

该属性表示了线环模式。
默认模式是`WidgetWidth`，这会导致文字在文本编辑的右侧边缘被包裹。包裹发生在空白处，保持整词完整。如果你希望在单词内进行折叠，可以使用`setWordWrapMode()`。如果你设置了`FixedPixelWidth`或`FixedColumnWidth`的包裹模式，也应该调用你想要的宽度的`setLineWrapColumnOrWidth()`。

**如何使用：** 调用 `lineWrapMode()` 读取当前值；它不会修改应用状态。

### `markdown : QString`

**作用与语义：**

该属性为文本编辑文本提供了Markdown接口。
`toMarkdown()`将文本编辑文本返回为“纯”Markdown，没有任何嵌入的HTML格式。`QTextDocument`支持的一些功能（如特定颜色和命名字体）无法用“纯”Markdown表达，因此会被省略。
`setMarkdown()`会修改文本编辑的文本。任何之前的文本都会被删除，撤销/重做历史也会被清除。输入文本被解读为Markdown格式的富文本。
对`markdown`字符串中包含的HTML的解析处理方式与`setHtml`相同;但不支持HTML块内的Markdown格式化。
解析器的一些功能可以通过`features`参数启用或禁用：
- `MarkdownNoHTML`：Markdown 文本中的任何 HTML 标签将被丢弃
- `MarkdownDialectCommonMark`：解析器仅支持CommonMark标准化的功能
- `MarkdownDialectGitHub`：解析器支持GitHub方言
默认是`MarkdownDialectGitHub`。

**如何使用：** 调用 `markdown()` 读取当前值；它不会修改应用状态。

### `overwriteMode : bool`

**作用与语义：**

该属性决定了用户输入的文本是否会覆盖现有文本。
与许多文本编辑器一样，文本编辑器小部件可以配置为插入或覆盖用户输入的新文本。
如果`true`该属性，现有文本会被新文本逐字符覆盖;否则，文本会插入光标位置，取代现有文本。
默认情况下，该属性为`false`（新文本不会覆盖现有文本）。

**如何使用：** 调用 `overwriteMode()` 读取当前值；它不会修改应用状态。

### `placeholderText : QString`

**作用与语义：**

该属性包含编辑器占位文本。
设置该属性后，只要`document()`为空，编辑器就会显示一个灰色的占位文本。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `placeholderText()` 读取当前值；它不会修改应用状态。

### `plainText : QString`

**作用与语义：**

该属性将文本编辑器的内容保持为纯文本。
设置属性时，之前的内容会被删除，撤销/重做历史也会被重置。`currentCharFormat()`也会被重置，除非`textCursor()`已经在文档开头。
如果文本编辑有其他内容类型，调用`toPlainText()`时不会被纯文本替代。唯一的例外是非间隔空间nbsp;，它会转换成标准空间。
默认情况下，对于无内容的编辑器，该属性包含空字符串。

**如何使用：** 调用 `plainText()` 读取当前值；它不会修改应用状态。

### `readOnly : bool`

**作用与语义：**

该属性决定文本编辑是否为只读。
在只读文本编辑中，用户只能浏览文本并选择文本;无法修改文本。
该属性的默认值为假。

**如何使用：** 调用 `readOnly()` 读取当前值；它不会修改应用状态。

### `tabChangesFocus : bool`

**作用与语义：**

无论Tab键改变焦点还是被接受为输入，这一属性都成立。
在某些情况下，文本编辑不应允许用户使用Tab键输入计表器或更改缩进，因为这会破坏焦点链。默认为false。

**如何使用：** 调用 `tabChangesFocus()` 读取当前值；它不会修改应用状态。

### `tabStopDistance : qreal`

**作用与语义：**

该属性表示制表停止距离（像素单位）。
默认情况下，该属性包含80像素的值。
不要设置小于`QChar::VisualTabCharacter`字符`horizontalAdvance()`的值，否则制表符字符将被不完全绘制。

**如何使用：** 调用 `tabStopDistance()` 读取当前值；它不会修改应用状态。

### `textInteractionFlags : Qt::TextInteractionFlags`

**作用与语义：**

指定小部件应如何与用户输入交互。
默认值取决于`QTextEdit`是只读还是可编辑，以及它是`QTextBrowser`还是不是。

**如何使用：** 调用 `textInteractionFlags()` 读取当前值；它不会修改应用状态。

### `undoRedoEnabled : bool`

**作用与语义：**

该属性在启用撤销和重做时均适用。
用户只有在该属性成立且存在可撤销（或重做）的操作时，才能撤销或重做操作。

**如何使用：** 调用 `undoRedoEnabled()` 读取当前值；它不会修改应用状态。

### `wordWrapMode : QTextOption::WrapMode`

**作用与语义：**

该属性表示`QTextEdit`在用单词包裹文本时所采用的模式。
默认情况下，该属性设置为`QTextOption::WrapAtWordBoundaryOrAnywhere`。

**如何使用：** 调用 `wordWrapMode()` 读取当前值；它不会修改应用状态。

### `[explicit] QTextEdit::QTextEdit(QWidget *parent = nullptr)`

**作用与语义：**

构造一个带有父 `parent` 的空 QTextEdit。

### `[explicit] QTextEdit::QTextEdit(const QString &text, QWidget *parent = nullptr)`

**作用与语义：**

构建带有父`parent`的QTextEdit。文本编辑将显示文本`text`。文本被解释为html。

### `[virtual noexcept] QTextEdit::~QTextEdit()`

**作用与语义：**

毁灭者。

### `Qt::Alignment QTextEdit::alignment() const`

**作用与语义：**

返回当前段落的对齐。

### `QString QTextEdit::anchorAt(const QPoint &pos) const`

**作用与语义：**

返回位置`pos`锚点的引用，如果该点没有锚点，则返回空字符串。

### `[slot] void QTextEdit::append(const QString &text)`

**作用与语义：**

在文本编辑末尾添加一个带有`text`的新段落。
注意：新增的段落将采用当前段落相同的字符格式和块格式，由光标位置决定。

### `[virtual protected] bool QTextEdit::canInsertFromMimeData(const QMimeData *source) const`

**作用与语义：**

该函数返回`true`，如果 MIME 数据对象的内容（由 `source` 指定）可以解码并插入文档中。例如，当拖动操作时鼠标进入该控件时调用该功能，需要判断是否能接受拖放操作。
重新实现该功能，以启用对额外 MIME 类型的拖放支持。

### `bool QTextEdit::canPaste() const`

**作用与语义：**

返回是否可以将剪贴板的文本粘贴到文本编辑中。

### `[override virtual protected] void QTextEdit::changeEvent(QEvent *e)`

**作用与语义：**

重实现自：`QFrame::changeEvent`（QEvent *ev）。

### `[slot] void QTextEdit::clear()`

**作用与语义：**

删除文本编辑中的所有文本。
注释：
- 撤销/重做历史也会被清除。
- `currentCharFormat()` 会被重置，除非`textCursor()`已经在文档开头。

### `[override virtual protected] void QTextEdit::contextMenuEvent(QContextMenuEvent *event)`

**作用与语义：**

重实现自：`QAbstractScrollArea::contextMenuEvent`（QContextMenuEvent *e）。
显示用`createStandardContextMenu()`创建的标准右键菜单。
如果你不希望文本编辑带有右键菜单，可以将其`contextMenuPolicy`设置为`Qt::NoContextMenu`。如果你想自定义右键菜单，请重新实现这个函数。如果你想扩展标准的右键菜单，重新实现这个功能，调用`createStandardContextMenu()`并扩展返回的菜单。
事件信息通过`event`对象传递。

**官方示例：**

```cpp
 void MyTextEdit::contextMenuEvent(QContextMenuEvent *event)
 {
     QMenu *menu = createStandardContextMenu();
     menu->addAction(tr("My Menu Item"));
     //...
     menu->exec(event->globalPos());
     delete menu;
 }
```

### `[slot] void QTextEdit::copy()`

**作用与语义：**

将选中的文本复制到剪贴板上。

### `[signal] void QTextEdit::copyAvailable(bool yes)`

**作用与语义：**

当文本编辑中选择或取消选择文本时，会发出该信号。
当选择文本时，该信号将以`yes`设置为true的状态发出。如果未选择文本或取消选择文本，则以`yes`为false的状态发出该信号。
如果`yes`为真，那么可以用`copy()`将选件复制到剪贴板。如果`yes`为假，则不`copy()`。

### `[virtual protected] QMimeData *QTextEdit::createMimeDataFromSelection() const`

**作用与语义：**

该函数返回一个新的 MIME 数据对象，以表示文本编辑当前选择的内容。当需要将选区封装到新的 `QMimeData` 对象中时，调用该功能;例如，当开始拖放操作，或将数据复制到剪贴板时。
如果你重新实现这个函数，注意返回`QMimeData`对象的所有权会传递给调用者。通过`textCursor()`函数可以检索选择。

### `QMenu *QTextEdit::createStandardContextMenu()`

**作用与语义：**

该功能创建标准的上下文菜单，用户用鼠标右键点击文本编辑时会显示。该功能由默认`contextMenuEvent()`处理程序调用。弹出菜单的所有权转移给调用者。
我们建议你改用createStandardContextMenu（`QPoint`）版本，它会启用与用户点击位置敏感的操作。

### `QMenu *QTextEdit::createStandardContextMenu(const QPoint &position)`

**作用与语义：**

该功能创建标准的上下文菜单，用户用鼠标右键点击文本编辑时会显示。该功能从默认`contextMenuEvent()`处理程序调用，并获取鼠标点击所在的文档坐标`position`。这可以启用对用户点击位置敏感的操作。弹出菜单的所有权转移给调用者。

### `QTextCharFormat QTextEdit::currentCharFormat() const`

**作用与语义：**

返回插入新文本时使用的字符格式。

### `[signal] void QTextEdit::currentCharFormatChanged(const QTextCharFormat &f)`

**作用与语义：**

当当前字符格式发生变化时，例如光标位置的变化，会发出该信号。
新赛制是`f`。

### `QFont QTextEdit::currentFont() const`

**作用与语义：**

返回当前格式的字体。

### `QTextCursor QTextEdit::cursorForPosition(const QPoint &pos) const`

**作用与语义：**

返回位置`pos`（视口坐标内）的`QTextCursor`。

### `[signal] void QTextEdit::cursorPositionChanged()`

**作用与语义：**

每当光标位置变化时，都会发出该信号。

### `QRect QTextEdit::cursorRect() const`

**作用与语义：**

返回一个矩形（以视口坐标表示），其中包含文本编辑的光标。

### `QRect QTextEdit::cursorRect(const QTextCursor &cursor) const`

**作用与语义：**

返回一个包含`cursor`的矩形（以视口坐标为单位）。

### `[slot] void QTextEdit::cut()`

**作用与语义：**

将选中的文本复制到剪贴板，并从文本编辑中删除。
如果没有被选中的文本，什么都不会发生。

### `[override virtual protected] void QTextEdit::dragEnterEvent(QDragEnterEvent *e)`

**作用与语义：**

重实现自：`QAbstractScrollArea::dragEnterEvent`（QDragEnterEvent *event）。

### `[override virtual protected] void QTextEdit::dragLeaveEvent(QDragLeaveEvent *e)`

**作用与语义：**

重实现自：`QAbstractScrollArea::dragLeaveEvent`（QDragLeaveEvent *event）。

### `[override virtual protected] void QTextEdit::dragMoveEvent(QDragMoveEvent *e)`

**作用与语义：**

重实现自：`QAbstractScrollArea::dragMoveEvent`（QDragMoveEvent *event）。

### `[override virtual protected] void QTextEdit::dropEvent(QDropEvent *e)`

**作用与语义：**

重实现自：`QAbstractScrollArea::dropEvent`（QDropEvent *事件）。

### `void QTextEdit::ensureCursorVisible()`

**作用与语义：**

必要时通过滚动文本编辑确保光标可见。

### `QList<QTextEdit::ExtraSelection> QTextEdit::extraSelections() const`

**作用与语义：**

回报之前设置的额外选择。

### `bool QTextEdit::find(const QString &exp, QTextDocument::FindFlags options = QTextDocument::FindFlags())`

**作用与语义：**

使用给定的`options`查找字符串的下一次出现`exp`。如果找到`exp`，返回`true`，并更改光标选择匹配;否则返回`false`。

### `bool QTextEdit::find(const QRegularExpression &exp, QTextDocument::FindFlags options = QTextDocument::FindFlags())`

**作用与语义：**

用给定的`options`找到下一个与正则表达式`exp`匹配的出现。
如果找到匹配并更改光标选择匹配，返回`true`;否则返回`false`。
警告：出于历史原因，`exp` 设置的大小写敏感性选项被忽略。相反，`options`用于判断搜索是否具有大小写敏感性。

### `[override virtual protected] void QTextEdit::focusInEvent(QFocusEvent *e)`

**作用与语义：**

重实现自：`QWidget::focusInEvent`（QFocusEvent *event）。
该事件处理程序可以在子类中重新实现，以接收控件的键盘焦点事件（焦点接收）。事件通过`event`参数传递。
小部件通常必须`setFocusPolicy()`到非`Qt::NoFocus`的对象才能接收焦点事件。（注意，应用程序员可以调用任何小部件`setFocus()`，即使是那些通常不接受焦点的小部件。）。
默认实现会更新小部件（除非是没有指定`focusPolicy()`的窗口）。

### `[override virtual protected] bool QTextEdit::focusNextPrevChild(bool next)`

**作用与语义：**

重构：`QWidget::focusNextPrevChild`（下一个布尔）。
根据 Tab 和 Shift Tab 找到一个新的控件来给键盘焦点，如果能找到新控件，则返回 `true`，找不到则返回 false。
如果`next`为真，该函数向前搜索;如果`next`为假，则向后搜索。
有时，你会想重新实现这个函数。例如，浏览器可能会重新实现它，将“当前活跃链接”向前或向后移动，只有当它到达“页面”的最后或第一个链接时才调用 focusNextPrevChild()。
子控件调用其父控件的 focusNextPrevChild()，但只有包含子控件的窗口决定将焦点重定向到哪里。通过重新实现该函数，你就能控制所有子控件的焦点遍历。

### `[override virtual protected] void QTextEdit::focusOutEvent(QFocusEvent *e)`

**作用与语义：**

重现：`QWidget::focusOutEvent`（QFocusEvent *event）。
该事件处理程序可以在子类中重新实现，以接收控件的键盘焦点事件（焦点丢失）。事件通过`event`参数传递。
小部件通常必须`setFocusPolicy()`到非`Qt::NoFocus`的对象才能接收焦点事件。（注意，应用程序员可以调用任何小部件`setFocus()`，即使是那些通常不接受焦点的小部件。）。
默认实现会更新小部件（除非是没有指定`focusPolicy()`的窗口）。

### `QString QTextEdit::fontFamily() const`

**作用与语义：**

返回当前格式的字体家族。

### `bool QTextEdit::fontItalic() const`

**作用与语义：**

如果当前格式的字体为斜体，返回`true`;否则返回 false。

### `qreal QTextEdit::fontPointSize() const`

**作用与语义：**

返回当前格式字体的点大小。

### `bool QTextEdit::fontUnderline() const`

**作用与语义：**

如果当前格式的字体被划线，返回`true`;否则返回 false。

### `int QTextEdit::fontWeight() const`

**作用与语义：**

返回当前格式的字体粗细。

### `[override virtual protected] void QTextEdit::inputMethodEvent(QInputMethodEvent *e)`

**作用与语义：**

重实现自：`QWidget::inputMethodEvent`（QInputMethodEvent *event）。
对于事件`event`，该事件处理程序可以被重新实现到子类中以接收输入法组合事件。当输入方法的状态发生变化时，调用该处理程序。
注意，在创建自定义文本编辑小部件时，必须明确设置`Qt::WA_InputMethodEnabled`窗口属性（使用`setAttribute()`函数），才能接收输入法事件。
默认实现调用 event->ignore()，拒绝输入法事件。详情请参见 `QInputMethodEvent` 文档。

### `[override virtual] QVariant QTextEdit::inputMethodQuery(Qt::InputMethodQuery property) const`

**作用与语义：**

重实现自：`QWidget::inputMethodQuery`（Qt：：InputMethodQuery query） const.
该方法仅适用于输入控件。输入方法用于查询控件的一组属性，以支持复杂的输入法操作，以支持周围文本和重新转换。
`query` 指定查询的属性。

### `[virtual protected] void QTextEdit::insertFromMimeData(const QMimeData *source)`

**作用与语义：**

该函数将由`source`指定的MIME数据对象内容插入当前光标位置的文本编辑中。每当通过剪贴板粘贴操作插入文本，或文本编辑接受拖拽操作的数据时，都会调用该功能。
重新实现该功能，以启用对额外 MIME 类型的拖放支持。

### `[slot] void QTextEdit::insertHtml(const QString &text)`

**作用与语义：**

方便的槽函数，插入假设为HTML格式的`text`，位于当前光标位置。
它等价于：
注意：当该函数与样式表一起使用时，样式表只会应用到文档当前的块。要在整个文档中应用样式表，请使用`QTextDocument::setDefaultStyleSheet()`。

**官方示例：**

```cpp
 edit->textCursor().insertHtml(fragment);
```

### `[slot] void QTextEdit::insertPlainText(const QString &text)`

**作用与语义：**

方便的槽函数，可以插入当前光标位置的`text`。
它等价于。

**官方示例：**

```cpp
 edit->textCursor().insertText(text);
```

### `[override virtual protected] void QTextEdit::keyPressEvent(QKeyEvent *e)`

**作用与语义：**

处理按键事件 `event`，默认实现负责富文本输入、选择、删除和快捷键。子类可拦截自定义按键；不处理时必须调用基类实现，否则标准编辑或场景键盘操作会失效。

### `[override virtual protected] void QTextEdit::keyReleaseEvent(QKeyEvent *e)`

**作用与语义：**

重实现自：`QWidget::keyReleaseEvent`（QKeyEvent *event）。
该事件处理程序用于事件`event`，可以在子类中重新实现，以接收该小部件的密钥释放事件。
小部件必须先接受焦点并拥有焦点，才能接收密钥释放事件。
如果你重新实现这个处理器，如果你不对密钥进行操作，务必调用基类实现。
默认实现忽略事件，以便小部件的父节点能够解释事件。
注意`QKeyEvent`以 isAccepted() == true开头，所以你不需要调用`QKeyEvent::accept()`——只要你对密钥操作时不要调用基类实现即可。

### `[virtual invokable] QVariant QTextEdit::loadResource(int type, const QUrl &name)`

**作用与语义：**

加载由给定`type`和`name`指定的资源。
该函数是`QTextDocument::loadResource()`的扩展。
注意：该函数可通过元对象系统和QML调用。参见 `Q_INVOKABLE`。

### `void QTextEdit::mergeCurrentCharFormat(const QTextCharFormat &modifier)`

**作用与语义：**

通过在编辑器光标上调用`QTextCursor::mergeCharFormat`，将`modifier`中指定的属性合并到当前字符格式中。如果编辑器有选区，则`modifier`的属性直接应用到该选区。

### `[override virtual protected] void QTextEdit::mouseDoubleClickEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QAbstractScrollArea::mouseDoubleClickEvent`（QMouseEvent *e）。

### `[override virtual protected] void QTextEdit::mouseMoveEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QAbstractScrollArea::mouseMoveEvent`（QMouseEvent *e）。

### `[override virtual protected] void QTextEdit::mousePressEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QAbstractScrollArea::mousePressEvent`（QMouseEvent *e）。

### `[override virtual protected] void QTextEdit::mouseReleaseEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QAbstractScrollArea::mouseReleaseEvent`（QMouseEvent *e）。

### `void QTextEdit::moveCursor(QTextCursor::MoveOperation operation, QTextCursor::MoveMode mode = QTextCursor::MoveAnchor)`

**作用与语义：**

通过执行指定`operation`移动光标。
如果`mode` `QTextCursor::KeepAnchor`，光标会选择它移动的文本。这与用户按住Shift键并用光标键移动光标时的效果相同。

### `[override virtual protected] void QTextEdit::paintEvent(QPaintEvent *event)`

**作用与语义：**

重实现自：`QAbstractScrollArea::paintEvent`（QPaintEvent *event）。
该事件处理程序可以在子类中重新实现，以接收 `event` 传递的绘画事件。通常不需要在 `QTextEdit` 的子类中重新实现该函数。
注意：如果你创建`QPainter`，它必须在`viewport()`上操作。
警告：在该函数的重新实现中，底层文本文档不得被修改。

### `[slot] void QTextEdit::paste()`

**作用与语义：**

将剪贴板上的文本粘贴到当前光标位置的文本编辑中。
如果剪贴板里没有文字，什么都不会发生。
要改变该函数的行为，即修改可粘贴`QTextEdit`的内容和粘贴方式，需要重新实现虚拟`canInsertFromMimeData()`和`insertFromMimeData()`函数。

### `void QTextEdit::print(QPagedPaintDevice *printer) const`

**作用与语义：**

方便函数将文本编辑的文档打印到给定的 `printer`。这等同于直接调用文档上的打印方法，但该函数还支持 QPrinter：：Selection 作为打印范围。

### `[slot] void QTextEdit::redo()`

**作用与语义：**

重新做上次的操作。
如果没有重做操作，即撤销/重做历史中没有重做步骤，则不会发生任何事。

### `[signal] void QTextEdit::redoAvailable(bool available)`

**作用与语义：**

每当重做操作可用（`available`为真）或不可用（`available`为假）时，该信号就会发出。

### `[override virtual protected] void QTextEdit::resizeEvent(QResizeEvent *e)`

**作用与语义：**

重实现自：`QAbstractScrollArea::resizeEvent`（QResizeEvent *event）。

### `[override virtual protected] void QTextEdit::scrollContentsBy(int dx, int dy)`

**作用与语义：**

重实现自：`QAbstractScrollArea::scrollContentsBy`（智力 dx，智力 dy）。
当滚动条被移动`dx`、`dy`时调用，因此视口内容应相应滚动。
默认实现只需调用整个`viewport()`的`update()`，子类可以重新实现该处理程序以优化，或者像`QScrollArea`一样移动内容控件。参数`dx`和`dy`是为了方便，让类知道应该滚动多少（比如像素移动时很有用）。你也可以忽略这些值，直接滚动到滚动条指示的位置。
调用该函数进行程序滚动是错误，建议使用滚动条（例如直接调用`QScrollBar::setValue()`）。

### `[slot] void QTextEdit::scrollToAnchor(const QString &name)`

**作用与语义：**

滚动文本编辑，使给定`name`锚点可见;如果`name`是空的、已经可见的，或者找不到，则不做任何操作。

### `[slot] void QTextEdit::selectAll()`

**作用与语义：**

选择所有文本。

### `[signal] void QTextEdit::selectionChanged()`

**作用与语义：**

每当选择发生变化时，该信号都会发出。

### `[slot] void QTextEdit::setAlignment(Qt::Alignment a)`

**作用与语义：**

将当前段落的对齐设置为`a`。有效的对齐有`Qt::AlignLeft`、`Qt::AlignRight`、`Qt::AlignJustify`和`Qt::AlignCenter`（水平居中）。

### `void QTextEdit::setCurrentCharFormat(const QTextCharFormat &format)`

**作用与语义：**

通过在编辑器光标上调用 `QTextCursor::setCharFormat()`，设置插入新文本到 `format` 时使用的字符格式。如果编辑器有选区，则将 char 格式直接应用于该选区。

### `[slot] void QTextEdit::setCurrentFont(const QFont &f)`

**作用与语义：**

将当前格式的字体设置为`f`。

### `void QTextEdit::setExtraSelections(const QList<QTextEdit::ExtraSelection> &selections)`

**作用与语义：**

该功能允许临时用指定颜色标记文档中的某些区域，具体颜色为`selections`。例如，在编程编辑器中，用特定背景色标记整行文本以表示断点的存在。

### `[slot] void QTextEdit::setFontFamily(const QString &fontFamily)`

**作用与语义：**

将当前格式的字体家族设置为`fontFamily`。

### `[slot] void QTextEdit::setFontItalic(bool italic)`

**作用与语义：**

如果`italic`为真，则将当前格式设置为斜体;否则将当前格式设置为非斜体。

### `[slot] void QTextEdit::setFontPointSize(qreal s)`

**作用与语义：**

将当前格式的点大小设置为`s`。
注意，如果`s`为零或负，则该函数的行为未被定义。

### `[slot] void QTextEdit::setFontUnderline(bool underline)`

**作用与语义：**

如果`underline`为真，则将当前格式设置为下划线;否则将当前格式设置为无下划线。

### `[slot] void QTextEdit::setFontWeight(int weight)`

**作用与语义：**

将当前格式的字体权重设置为给定的 `weight`，其中所用值位于`QFont::Weight`枚举定义的范围内。

### `[slot] void QTextEdit::setPlainText(const QString &text)`

**作用与语义：**

该属性将文本编辑器的内容保持为纯文本。
设置属性时，之前的内容会被删除，撤销/重做历史也会被重置。`currentCharFormat()`也会被重置，除非`textCursor()`已经在文档开头。
如果文本编辑有其他内容类型，调用`toPlainText()`时不会被纯文本替代。唯一的例外是非间隔空间nbsp;，它会转换成标准空间。
默认情况下，对于无内容的编辑器，该属性包含空字符串。

**如何使用：** 调用 `setPlainText(...)` 修改 `plainText`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `[slot] void QTextEdit::setText(const QString &text)`

**作用与语义：**

设置文本编辑的 `text`。文本可以是纯文本或 HTML，文本编辑会尝试猜测正确的格式。
直接使用`setHtml()`或`setPlainText()`，避免文本编辑的猜测。

### `[slot] void QTextEdit::setTextBackgroundColor(const QColor &c)`

**作用与语义：**

将当前格式的文本背景颜色设置为`c`。

### `[slot] void QTextEdit::setTextColor(const QColor &c)`

**作用与语义：**

将当前格式的文本颜色设置为`c`。

### `void QTextEdit::setTextCursor(const QTextCursor &cursor)`

**作用与语义：**

设定可见`cursor`。

### `[override virtual protected] void QTextEdit::showEvent(QShowEvent *)`

**作用与语义：**

重实现自：`QWidget::showEvent`（QShowEvent *event）。
该事件处理程序可以在子类中重新实现，以接收传递给 `event` 参数的控件显示事件。
非自发的展示事件会在展示前立即发送到小部件。窗口的自发展示事件则在展示之后交付。
注意：当窗口系统改变其映射状态时，小部件会接收自发显示和隐藏事件，例如用户最小化窗口时自发隐藏事件，窗口恢复时自发显示事件。收到自发隐藏事件后，小部件仍被视为`isVisible()`可见。

### `QColor QTextEdit::textBackgroundColor() const`

**作用与语义：**

返回当前格式的文本背景色。

### `[signal] void QTextEdit::textChanged()`

**作用与语义：**

该属性为文本编辑提供了HTML接口。
toHtml() 返回文本编辑的文本，表示为 html。
setHtml() 会更改文本编辑的文本。之前的文本会被删除，撤销/重做历史也会被清除。输入文本被解释为 HTML 格式的富文本。`currentCharFormat()`也会被重置，除非`textCursor()`已经在文档开头。
注意：调用者有责任确保在创建包含HTML的`QString`并传递给setHtml()时，文本正确解码。
默认情况下，对于新创建的空白文档，该属性包含描述无正文的 HTML 4.0 文档的文本。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `html` 的变化，不要把它当作普通函数主动调用。

### `QColor QTextEdit::textColor() const`

**作用与语义：**

返回当前格式的文本颜色。

### `QTextCursor QTextEdit::textCursor() const`

**作用与语义：**

返回代表当前可见光标的`QTextCursor`副本。注意，返回光标的变化不会影响`QTextEdit`的光标;使用`setTextCursor()`来更新可见光标。

### `QString QTextEdit::toPlainText() const`

**作用与语义：**

该属性将文本编辑器的内容保持为纯文本。
设置属性时，之前的内容会被删除，撤销/重做历史也会被重置。`currentCharFormat()`也会被重置，除非`textCursor()`已经在文档开头。
如果文本编辑有其他内容类型，调用`toPlainText()`时不会被纯文本替代。唯一的例外是非间隔空间nbsp;，它会转换成标准空间。
默认情况下，对于无内容的编辑器，该属性包含空字符串。

**如何使用：** 调用 `toPlainText()` 读取当前值；它不会修改应用状态。

### `[slot] void QTextEdit::undo()`

**作用与语义：**

撤销上次的操作。
如果没有可撤销的操作，即撤销/重做历史中没有撤销步骤，则不会发生任何事。

### `[signal] void QTextEdit::undoAvailable(bool available)`

**作用与语义：**

每当撤销操作可用（`available`为真）或不可用（`available`为假）时，该信号都会发出。

### `[override virtual protected] void QTextEdit::wheelEvent(QWheelEvent *e)`

**作用与语义：**

重实现自：`QAbstractScrollArea::wheelEvent`（QWheelEvent *e）。

### `[slot] void QTextEdit::zoomIn(int range = 1)`

**作用与语义：**

通过将基础字体大小`range`点放大，并将所有字体大小重新计算为新大小来放大文本。这不会改变任何图片的大小。

### `[slot] void QTextEdit::zoomOut(int range = 1)`

**作用与语义：**

通过缩小基础字体大小`range`点，并重新计算所有字体大小为新大小来缩放文本。这不会改变任何图片的大小。

### `struct ExtraSelection`

**作用与语义：**

QTextEdit::ExtraSelection 结构提供了一种方法，用于为文档中的给定选择指定字符格式。

### `flags AutoFormatting`

**作用与语义：**

- `QTextEdit::AutoNone`：`0`;不要做任何自动格式化。
- `QTextEdit::AutoBulletList`：`0x00000001`;自动创建项目符号列表（例如，当用户在最左侧列输入星号（*'）或在现有列表项中按回车时）。
- `QTextEdit::AutoAll`：`0xffffffff`;应用所有自动格式化。目前仅支持自动项目符号列表。
AutoFormatting 类型是 QFlags 的 typedef<AutoFormattingFlag>。它存储 AutoFormattingFlag 值的 OR 组合。

### `enum AutoFormattingFlag { AutoNone, AutoBulletList, AutoAll }`

**作用与语义：**

- `QTextEdit::AutoNone`：`0`;不要做任何自动格式化。
- `QTextEdit::AutoBulletList`：`0x00000001`;自动创建项目符号列表（例如，当用户在最左侧列输入星号（*'）或在现有列表项中按回车时）。
- `QTextEdit::AutoAll`：`0xffffffff`;应用所有自动格式化。目前仅支持自动项目符号列表。
AutoFormatting 类型是 QFlags 的 typedef<AutoFormattingFlag>。它存储 AutoFormattingFlag 值的 OR 组合。

### `enum LineWrapMode { NoWrap, WidgetWidth, FixedPixelWidth, FixedColumnWidth }`

**作用与语义：**

控制富文本编辑器的视觉换行：不换行、按控件宽度、固定像素宽度或固定列数换行。固定模式还需用 `setLineWrapColumnOrWidth()` 给出宽度；换行只影响布局，不会改写文档内容。

### `bool acceptRichText() const`

**作用与语义：**

该属性决定文本编辑是否接受用户的富文本插入。
当该属性设置为虚假文本时，编辑只接受用户的纯文本输入。例如通过剪贴板或拖放。
该房产的默认情况是真实的。

**如何使用：** 调用 `acceptRichText()` 读取当前值；它不会修改应用状态。

### `QTextEdit::AutoFormatting autoFormatting() const`

**作用与语义：**

该属性包含启用的自动格式化功能集合。
该值可以是`AutoFormattingFlag`枚举中任意组合的值。默认值为`AutoNone`。选择`AutoAll`以启用所有自动格式化。
目前，唯一提供的自动格式化功能是`AutoBulletList`;未来版本的Qt可能会提供更多功能。

**如何使用：** 调用 `autoFormatting()` 读取当前值；它不会修改应用状态。

### `int cursorWidth() const`

**作用与语义：**

该属性指定光标的宽度（像素单位）。默认值为1。

**如何使用：** 调用 `cursorWidth()` 读取当前值；它不会修改应用状态。

### `QTextDocument * document() const`

**作用与语义：**

此属性保存文本编辑器的基础文档。
注意：除非编辑器是文档的父对象，否则编辑器不会接管文档的所有权。所提供文档的父对象仍然是该对象的所有者。如果之前分配的文档是编辑器的子对象，则该文档将被删除。

**如何使用：** 调用 `document()` 读取当前值；它不会修改应用状态。

### `QString documentTitle() const`

**作用与语义：**

该属性包含从文本中解析出来的文档标题。
默认情况下，对于新创建的空文档，该属性包含空字符串。

**如何使用：** 调用 `documentTitle()` 读取当前值；它不会修改应用状态。

### `bool isReadOnly() const`

**作用与语义：**

该属性决定文本编辑是否为只读。
在只读文本编辑中，用户只能浏览文本并选择文本;无法修改文本。
该属性的默认值为假。

**如何使用：** 调用 `isReadOnly()` 读取当前值；它不会修改应用状态。

### `bool isUndoRedoEnabled() const`

**作用与语义：**

该属性在启用撤销和重做时均适用。
用户只有在该属性成立且存在可撤销（或重做）的操作时，才能撤销或重做操作。

**如何使用：** 调用 `isUndoRedoEnabled()` 读取当前值；它不会修改应用状态。

### `int lineWrapColumnOrWidth() const`

**作用与语义：**

此属性保存文本换行的位置（以像素或字符列为单位，取决于换行模式）。
如果换行模式是 `FixedPixelWidth`，则值为从文本编辑左边缘开始换行的像素数。如果换行模式是 `FixedColumnWidth`，则值为从文本编辑左边缘开始换行的字符列号。
默认情况下，此属性包含值 0。

**如何使用：** 调用 `lineWrapColumnOrWidth()` 读取当前值；它不会修改应用状态。

### `QTextEdit::LineWrapMode lineWrapMode() const`

**作用与语义：**

该属性表示了线环模式。
默认模式是`WidgetWidth`，这会导致文字在文本编辑的右侧边缘被包裹。包裹发生在空白处，保持整词完整。如果你希望在单词内进行折叠，可以使用`setWordWrapMode()`。如果你设置了`FixedPixelWidth`或`FixedColumnWidth`的包裹模式，也应该调用你想要的宽度的`setLineWrapColumnOrWidth()`。

**如何使用：** 调用 `lineWrapMode()` 读取当前值；它不会修改应用状态。

### `bool overwriteMode() const`

**作用与语义：**

该属性决定了用户输入的文本是否会覆盖现有文本。
与许多文本编辑器一样，文本编辑器小部件可以配置为插入或覆盖用户输入的新文本。
如果`true`该属性，现有文本会被新文本逐字符覆盖;否则，文本会插入光标位置，取代现有文本。
默认情况下，该属性为`false`（新文本不会覆盖现有文本）。

**如何使用：** 调用 `overwriteMode()` 读取当前值；它不会修改应用状态。

### `QString placeholderText() const`

**作用与语义：**

该属性包含编辑器占位文本。
设置该属性后，只要`document()`为空，编辑器就会显示一个灰色的占位文本。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `placeholderText()` 读取当前值；它不会修改应用状态。

### `void setAcceptRichText(bool accept)`

**作用与语义：**

该属性决定文本编辑是否接受用户的富文本插入。
当该属性设置为虚假文本时，编辑只接受用户的纯文本输入。例如通过剪贴板或拖放。
该房产的默认情况是真实的。

**如何使用：** 调用 `setAcceptRichText(...)` 修改 `acceptRichText`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setAutoFormatting(QTextEdit::AutoFormatting features)`

**作用与语义：**

该属性包含启用的自动格式化功能集合。
该值可以是`AutoFormattingFlag`枚举中任意组合的值。默认值为`AutoNone`。选择`AutoAll`以启用所有自动格式化。
目前，唯一提供的自动格式化功能是`AutoBulletList`;未来版本的Qt可能会提供更多功能。

**如何使用：** 调用 `setAutoFormatting(...)` 修改 `autoFormatting`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setCursorWidth(int width)`

**作用与语义：**

该属性指定光标的宽度（像素单位）。默认值为1。

**如何使用：** 调用 `setCursorWidth(...)` 修改 `cursorWidth`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setDocument(QTextDocument *document)`

**作用与语义：**

此属性保存文本编辑器的基础文档。
注意：除非编辑器是文档的父对象，否则编辑器不会接管文档的所有权。所提供文档的父对象仍然是该对象的所有者。如果之前分配的文档是编辑器的子对象，则该文档将被删除。

**如何使用：** 调用 `setDocument(...)` 修改 `document`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setDocumentTitle(const QString &title)`

**作用与语义：**

该属性包含从文本中解析出来的文档标题。
默认情况下，对于新创建的空文档，该属性包含空字符串。

**如何使用：** 调用 `setDocumentTitle(...)` 修改 `documentTitle`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setLineWrapColumnOrWidth(int w)`

**作用与语义：**

此属性保存文本换行的位置（以像素或字符列为单位，取决于换行模式）。
如果换行模式是 `FixedPixelWidth`，则值为从文本编辑左边缘开始换行的像素数。如果换行模式是 `FixedColumnWidth`，则值为从文本编辑左边缘开始换行的字符列号。
默认情况下，此属性包含值 0。

**如何使用：** 调用 `setLineWrapColumnOrWidth(...)` 修改 `lineWrapColumnOrWidth`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setLineWrapMode(QTextEdit::LineWrapMode mode)`

**作用与语义：**

该属性表示了线环模式。
默认模式是`WidgetWidth`，这会导致文字在文本编辑的右侧边缘被包裹。包裹发生在空白处，保持整词完整。如果你希望在单词内进行折叠，可以使用`setWordWrapMode()`。如果你设置了`FixedPixelWidth`或`FixedColumnWidth`的包裹模式，也应该调用你想要的宽度的`setLineWrapColumnOrWidth()`。

**如何使用：** 调用 `setLineWrapMode(...)` 修改 `lineWrapMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setOverwriteMode(bool overwrite)`

**作用与语义：**

该属性决定了用户输入的文本是否会覆盖现有文本。
与许多文本编辑器一样，文本编辑器小部件可以配置为插入或覆盖用户输入的新文本。
如果`true`该属性，现有文本会被新文本逐字符覆盖;否则，文本会插入光标位置，取代现有文本。
默认情况下，该属性为`false`（新文本不会覆盖现有文本）。

**如何使用：** 调用 `setOverwriteMode(...)` 修改 `overwriteMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setPlaceholderText(const QString &placeholderText)`

**作用与语义：**

该属性包含编辑器占位文本。
设置该属性后，只要`document()`为空，编辑器就会显示一个灰色的占位文本。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `setPlaceholderText(...)` 修改 `placeholderText`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setReadOnly(bool ro)`

**作用与语义：**

该属性决定文本编辑是否为只读。
在只读文本编辑中，用户只能浏览文本并选择文本;无法修改文本。
该属性的默认值为假。

**如何使用：** 调用 `setReadOnly(...)` 修改 `readOnly`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTabChangesFocus(bool b)`

**作用与语义：**

无论Tab键改变焦点还是被接受为输入，这一属性都成立。
在某些情况下，文本编辑不应允许用户使用Tab键输入计表器或更改缩进，因为这会破坏焦点链。默认为false。

**如何使用：** 调用 `setTabChangesFocus(...)` 修改 `tabChangesFocus`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTabStopDistance(qreal distance)`

**作用与语义：**

该属性表示制表停止距离（像素单位）。
默认情况下，该属性包含80像素的值。
不要设置小于`QChar::VisualTabCharacter`字符`horizontalAdvance()`的值，否则制表符字符将被不完全绘制。

**如何使用：** 调用 `setTabStopDistance(...)` 修改 `tabStopDistance`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTextInteractionFlags(Qt::TextInteractionFlags flags)`

**作用与语义：**

指定小部件应如何与用户输入交互。
默认值取决于`QTextEdit`是只读还是可编辑，以及它是`QTextBrowser`还是不是。

**如何使用：** 调用 `setTextInteractionFlags(...)` 修改 `textInteractionFlags`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setUndoRedoEnabled(bool enable)`

**作用与语义：**

该属性在启用撤销和重做时均适用。
用户只有在该属性成立且存在可撤销（或重做）的操作时，才能撤销或重做操作。

**如何使用：** 调用 `setUndoRedoEnabled(...)` 修改 `undoRedoEnabled`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setWordWrapMode(QTextOption::WrapMode policy)`

**作用与语义：**

该属性表示`QTextEdit`在用单词包裹文本时所采用的模式。
默认情况下，该属性设置为`QTextOption::WrapAtWordBoundaryOrAnywhere`。

**如何使用：** 调用 `setWordWrapMode(...)` 修改 `wordWrapMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `bool tabChangesFocus() const`

**作用与语义：**

无论Tab键改变焦点还是被接受为输入，这一属性都成立。
在某些情况下，文本编辑不应允许用户使用Tab键输入计表器或更改缩进，因为这会破坏焦点链。默认为false。

**如何使用：** 调用 `tabChangesFocus()` 读取当前值；它不会修改应用状态。

### `qreal tabStopDistance() const`

**作用与语义：**

该属性表示制表停止距离（像素单位）。
默认情况下，该属性包含80像素的值。
不要设置小于`QChar::VisualTabCharacter`字符`horizontalAdvance()`的值，否则制表符字符将被不完全绘制。

**如何使用：** 调用 `tabStopDistance()` 读取当前值；它不会修改应用状态。

### `Qt::TextInteractionFlags textInteractionFlags() const`

**作用与语义：**

指定小部件应如何与用户输入交互。
默认值取决于`QTextEdit`是只读还是可编辑，以及它是`QTextBrowser`还是不是。

**如何使用：** 调用 `textInteractionFlags()` 读取当前值；它不会修改应用状态。

### `QString toHtml() const`

**作用与语义：**

该属性为文本编辑提供了HTML接口。
toHtml() 返回文本编辑的文本，表示为 html。
setHtml() 会更改文本编辑的文本。之前的文本会被删除，撤销/重做历史也会被清除。输入文本被解释为 HTML 格式的富文本。`currentCharFormat()`也会被重置，除非`textCursor()`已经在文档开头。
注意：调用者有责任确保在创建包含HTML的`QString`并传递给setHtml()时，文本正确解码。
默认情况下，对于新创建的空白文档，该属性包含描述无正文的 HTML 4.0 文档的文本。

**如何使用：** 调用 `toHtml()` 读取当前值；它不会修改应用状态。

### `QString toMarkdown(QTextDocument::MarkdownFeatures features = QTextDocument::MarkdownDialectGitHub) const`

**作用与语义：**

该属性为文本编辑文本提供了Markdown接口。
`toMarkdown()`将文本编辑文本返回为“纯”Markdown，没有任何嵌入的HTML格式。`QTextDocument`支持的一些功能（如特定颜色和命名字体）无法用“纯”Markdown表达，因此会被省略。
`setMarkdown()`会修改文本编辑的文本。任何之前的文本都会被删除，撤销/重做历史也会被清除。输入文本被解读为Markdown格式的富文本。
对`markdown`字符串中包含的HTML的解析处理方式与`setHtml`相同;但不支持HTML块内的Markdown格式化。
解析器的一些功能可以通过`features`参数启用或禁用：
- `MarkdownNoHTML`：Markdown 文本中的任何 HTML 标签将被丢弃
- `MarkdownDialectCommonMark`：解析器仅支持CommonMark标准化的功能
- `MarkdownDialectGitHub`：解析器支持GitHub方言
默认是`MarkdownDialectGitHub`。

**如何使用：** 调用 `toMarkdown()` 读取当前值；它不会修改应用状态。

### `QTextOption::WrapMode wordWrapMode() const`

**作用与语义：**

该属性表示`QTextEdit`在用单词包裹文本时所采用的模式。
默认情况下，该属性设置为`QTextOption::WrapAtWordBoundaryOrAnywhere`。

**如何使用：** 调用 `wordWrapMode()` 读取当前值；它不会修改应用状态。

### `void setHtml(const QString &text)`

**作用与语义：**

该属性为文本编辑提供了HTML接口。
toHtml() 返回文本编辑的文本，表示为 html。
setHtml() 会更改文本编辑的文本。之前的文本会被删除，撤销/重做历史也会被清除。输入文本被解释为 HTML 格式的富文本。`currentCharFormat()`也会被重置，除非`textCursor()`已经在文档开头。
注意：调用者有责任确保在创建包含HTML的`QString`并传递给setHtml()时，文本正确解码。
默认情况下，对于新创建的空白文档，该属性包含描述无正文的 HTML 4.0 文档的文本。

**如何使用：** 调用 `setHtml(...)` 修改 `html`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMarkdown(const QString &markdown)`

**作用与语义：**

该属性为文本编辑文本提供了Markdown接口。
`toMarkdown()`将文本编辑文本返回为“纯”Markdown，没有任何嵌入的HTML格式。`QTextDocument`支持的一些功能（如特定颜色和命名字体）无法用“纯”Markdown表达，因此会被省略。
`setMarkdown()`会修改文本编辑的文本。任何之前的文本都会被删除，撤销/重做历史也会被清除。输入文本被解读为Markdown格式的富文本。
对`markdown`字符串中包含的HTML的解析处理方式与`setHtml`相同;但不支持HTML块内的Markdown格式化。
解析器的一些功能可以通过`features`参数启用或禁用：
- `MarkdownNoHTML`：Markdown 文本中的任何 HTML 标签将被丢弃
- `MarkdownDialectCommonMark`：解析器仅支持CommonMark标准化的功能
- `MarkdownDialectGitHub`：解析器支持GitHub方言
默认是`MarkdownDialectGitHub`。

**如何使用：** 调用 `setMarkdown(...)` 修改 `markdown`；传入的新值会成为后续查询和相关界面行为所使用的值。

## 6. 深入实践与常见坑

### 生命周期和资源边界

控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

### 状态和错误边界

控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

### 线程边界

所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

### 最容易出现的错误

不要用固定坐标拼接响应式界面；不要给已经加入布局的控件反复 `setGeometry()`；不要在 `paintEvent()` 中修改业务状态；不要忘记窗口关闭、对象销毁和应用退出是三个不同事件。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QTextEdit` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
