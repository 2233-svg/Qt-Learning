# QPlainTextEdit

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QPlainTextEdit` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QPlainTextEdit` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QPlainTextEdit>`
- 继承自：QAbstractScrollArea
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

### 状态、生命周期和线程

**生命周期：** 控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

**状态与结果：** 控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

**线程与事件循环：** 所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

## 3. 直接使用

需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。 使用时通常按这个过程组织：创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum LineWrapMode { NoWrap, WidgetWidth }`

### 属性

- `backgroundVisible : bool`
- `blockCount : int`
- `centerOnScroll : bool`
- `cursorWidth : int`
- `documentTitle : QString`
- `lineWrapMode : LineWrapMode`
- `maximumBlockCount : int`
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

- `QPlainTextEdit(QWidget *parent = nullptr)`
- `QPlainTextEdit(const QString &text, QWidget *parent = nullptr)`
- `virtual ~QPlainTextEdit()`
- `QString anchorAt(const QPoint &pos) const`
- `bool backgroundVisible() const`
- `int blockCount() const`
- `bool canPaste() const`
- `bool centerOnScroll() const`
- `QMenu * createStandardContextMenu()`
- `QMenu * createStandardContextMenu(const QPoint &position)`
- `QTextCharFormat currentCharFormat() const`
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
- `bool isReadOnly() const`
- `bool isUndoRedoEnabled() const`
- `QPlainTextEdit::LineWrapMode lineWrapMode() const`
- `virtual QVariant loadResource(int type, const QUrl &name)`
- `int maximumBlockCount() const`
- `void mergeCurrentCharFormat(const QTextCharFormat &modifier)`
- `void moveCursor(QTextCursor::MoveOperation operation, QTextCursor::MoveMode mode = QTextCursor::MoveAnchor)`
- `bool overwriteMode() const`
- `QString placeholderText() const`
- `void print(QPagedPaintDevice *printer) const`
- `void setBackgroundVisible(bool visible)`
- `void setCenterOnScroll(bool enabled)`
- `void setCurrentCharFormat(const QTextCharFormat &format)`
- `void setCursorWidth(int width)`
- `void setDocument(QTextDocument *document)`
- `void setDocumentTitle(const QString &title)`
- `void setExtraSelections(const QList<QTextEdit::ExtraSelection> &selections)`
- `void setLineWrapMode(QPlainTextEdit::LineWrapMode mode)`
- `void setMaximumBlockCount(int maximum)`
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
- `QTextCursor textCursor() const`
- `Qt::TextInteractionFlags textInteractionFlags() const`
- `QString toPlainText() const`
- `QTextOption::WrapMode wordWrapMode() const`

### 重实现的公有函数

- `virtual QVariant inputMethodQuery(Qt::InputMethodQuery property) const override`

### 公有槽函数

- `void appendHtml(const QString &html)`
- `void appendPlainText(const QString &text)`
- `void centerCursor()`
- `void clear()`
- `void copy()`
- `void cut()`
- `void insertPlainText(const QString &text)`
- `void paste()`
- `void redo()`
- `void selectAll()`
- `void setPlainText(const QString &text)`
- `void undo()`
- `void zoomIn(int range = 1)`
- `void zoomOut(int range = 1)`

### 信号

- `void blockCountChanged(int newBlockCount)`
- `void copyAvailable(bool yes)`
- `void cursorPositionChanged()`
- `void modificationChanged(bool changed)`
- `void redoAvailable(bool available)`
- `void selectionChanged()`
- `void textChanged()`
- `void undoAvailable(bool available)`
- `void updateRequest(const QRect &rect, int dy)`

### 保护函数

- `QRectF blockBoundingGeometry(const QTextBlock &block) const`
- `QRectF blockBoundingRect(const QTextBlock &block) const`
- `virtual bool canInsertFromMimeData(const QMimeData *source) const`
- `QPointF contentOffset() const`
- `virtual QMimeData * createMimeDataFromSelection() const`
- `QTextBlock firstVisibleBlock() const`
- `QAbstractTextDocumentLayout::PaintContext getPaintContext() const`
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
- `virtual void paintEvent(QPaintEvent *e) override`
- `virtual void resizeEvent(QResizeEvent *e) override`
- `virtual void scrollContentsBy(int dx, int dy) override`
- `virtual void showEvent(QShowEvent *) override`
- `virtual void wheelEvent(QWheelEvent *e) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `backgroundVisible : bool`

**作用与语义：**

该属性决定调色板背景是否在文档区域外可见。
如果设置为 true，纯文本编辑会在未被文本文档覆盖的视口区域绘制调色板背景。否则，如果设置为 false，则不会。该功能使用户能够直观区分文档中用调色板底色绘制的区域，以及未被任何文档覆盖的空白区域。
默认是假的。

**如何使用：** 调用 `backgroundVisible()` 读取当前值；它不会修改应用状态。

### `[read-only] blockCount : int`

**作用与语义：**

该属性包含文档中的文本块数量。
默认情况下，在空文档中，该属性的值为1。

**如何使用：** 调用 `blockCount()` 读取当前值；它不会修改应用状态。

### `centerOnScroll : bool`

**作用与语义：**

该属性决定光标是否应置中于屏幕。
如果设置为 true，纯文本编辑会将文档垂直滚动，使光标在视口中心可见。这也允许文本编辑滚动到文档末尾以下。否则，如果设置为 false，纯文本编辑会尽可能少地滚动，以确保光标可见。同样的算法适用于通过 `appendPlainText()` 添加的任何新行。
默认是假的。

**如何使用：** 调用 `centerOnScroll()` 读取当前值；它不会修改应用状态。

### `cursorWidth : int`

**作用与语义：**

该属性指定光标的宽度（像素单位）。默认值为1。

**如何使用：** 调用 `cursorWidth()` 读取当前值；它不会修改应用状态。

### `documentTitle : QString`

**作用与语义：**

该属性包含从文本中解析出来的文档标题。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `documentTitle()` 读取当前值；它不会修改应用状态。

### `lineWrapMode : LineWrapMode`

**作用与语义：**

该属性表示了线环模式。
默认模式是`WidgetWidth`，使文字在文本编辑的右侧边缘被包裹。包裹发生在空白处，保持整词完整。如果你希望在单词内进行折叠，请使用`setWordWrapMode()`。

**如何使用：** 调用 `lineWrapMode()` 读取当前值；它不会修改应用状态。

### `maximumBlockCount : int`

**作用与语义：**

该属性限制了文档中块的限制。
指定文档可拥有的最大块数。如果文档中有更多带有该属性的块，则从文档开头移除块。
负值或零值表示文档可以包含无限数量的块。
默认值是0。
注意，设置该属性会立即将限制应用到文档内容上。设置该属性还会禁用撤销重做历史。

**如何使用：** 调用 `maximumBlockCount()` 读取当前值；它不会修改应用状态。

### `overwriteMode : bool`

**作用与语义：**

该属性决定了用户输入的文本是否会覆盖现有文本。
与许多文本编辑器一样，纯文本编辑器小部件可以配置为插入或覆盖用户输入的新文本。
如果`true`该属性，现有文本会逐字符被新文本覆盖;否则，文本会在光标位置插入，取代现有文本。
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

该属性获取并设置纯文本编辑器的内容。设置该属性后，之前的内容会被移除，撤销/重做历史也会被重置。`currentCharFormat()`也会被重置，除非`textCursor()`已经在文档开头。
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

规定标签在显示文本时应如何与用户输入交互。
如果标志中包含`Qt::LinksAccessibleByKeyboard`或`Qt::TextSelectableByKeyboard`，那么焦点策略也会自动设置为`Qt::ClickFocus`。
默认值取决于`QPlainTextEdit`是只读还是可编辑。

**如何使用：** 调用 `textInteractionFlags()` 读取当前值；它不会修改应用状态。

### `undoRedoEnabled : bool`

**作用与语义：**

该属性是否允许撤销和重做。
用户只有在该属性成立且存在可撤销（或重做）的操作时，才能撤销或重做操作。
默认情况下，该属性为`true`。

**如何使用：** 调用 `undoRedoEnabled()` 读取当前值；它不会修改应用状态。

### `wordWrapMode : QTextOption::WrapMode`

**作用与语义：**

该属性表示`QPlainTextEdit`在用单词包裹文本时所采用的模式。
默认情况下，该属性设置为`QTextOption::WrapAtWordBoundaryOrAnywhere`。

**如何使用：** 调用 `wordWrapMode()` 读取当前值；它不会修改应用状态。

### `[explicit] QPlainTextEdit::QPlainTextEdit(QWidget *parent = nullptr)`

**作用与语义：**

构造一个带有父 `parent` 的空 QPlainTextEdit。

### `[explicit] QPlainTextEdit::QPlainTextEdit(const QString &text, QWidget *parent = nullptr)`

**作用与语义：**

构建带有父 `parent`的 QPlainTextEdit。文本编辑将显示纯文本`text`。

### `[virtual noexcept] QPlainTextEdit::~QPlainTextEdit()`

**作用与语义：**

毁灭者。

### `QString QPlainTextEdit::anchorAt(const QPoint &pos) const`

**作用与语义：**

返回位置`pos`锚点的引用，如果该点没有锚点，则返回空字符串。

### `[slot] void QPlainTextEdit::appendHtml(const QString &html)`

**作用与语义：**

在文本编辑末尾附加一个带有`html`的新段落。
`appendPlainText()`。

### `[slot] void QPlainTextEdit::appendPlainText(const QString &text)`

**作用与语义：**

在文本编辑末尾附加一个带有`text`的新段落。

### `[protected] QRectF QPlainTextEdit::blockBoundingGeometry(const QTextBlock &block) const`

**作用与语义：**

返回内容坐标中的文本`block`边界矩形。用`contentOffset()`平移矩形以获得视口上的视觉坐标。

### `[protected] QRectF QPlainTextEdit::blockBoundingRect(const QTextBlock &block) const`

**作用与语义：**

返回文本在块自身坐标`block`的边界矩形。

### `[signal] void QPlainTextEdit::blockCountChanged(int newBlockCount)`

**作用与语义：**

每当区块计数变化时，该信号都会发出。新的区块计数会以`newBlockCount`传递。

### `[virtual protected] bool QPlainTextEdit::canInsertFromMimeData(const QMimeData *source) const`

**作用与语义：**

如果MIME数据对象的内容（由`source`指定的）可以被解码并插入文档，该函数会返回`true`。例如，当拖动操作中鼠标进入该控件时调用该功能，需要判断是否能接受拖动。

### `bool QPlainTextEdit::canPaste() const`

**作用与语义：**

返回是否可以将剪贴板的文本粘贴到文本编辑中。

### `[slot] void QPlainTextEdit::centerCursor()`

**作用与语义：**

滚动文档以使光标垂直居中。

### `[override virtual protected] void QPlainTextEdit::changeEvent(QEvent *e)`

**作用与语义：**

重实现自：`QFrame::changeEvent`（QEvent *ev）。

### `[slot] void QPlainTextEdit::clear()`

**作用与语义：**

删除文本编辑中的所有文本。
注释：
- 撤销/重做历史也会被清除。
- `currentCharFormat()` 会被重置，除非`textCursor()`已经在文档开头。

### `[protected] QPointF QPlainTextEdit::contentOffset() const`

**作用与语义：**

返回内容的视口坐标起点。
纯文本编辑内容的起点始终是第一个可见文本块的左上角。内容偏移量不同于（0,0）当文本被水平滚动，或第一个可见块部分滚动出屏幕时，即可见文本不以第一个可见块的第一行开始，或者第一个可见块是第一个块且编辑器显示边距时。

### `[override virtual protected] void QPlainTextEdit::contextMenuEvent(QContextMenuEvent *event)`

**作用与语义：**

重实现自：`QAbstractScrollArea::contextMenuEvent`（QContextMenuEvent *e）。
显示用`createStandardContextMenu()`创建的标准右键菜单。
如果你不希望文本编辑带有右键菜单，可以将其`contextMenuPolicy`设置为`Qt::NoContextMenu`。如果你想自定义右键菜单，请重新实现这个函数。如果你想扩展标准的右键菜单，重新实现这个功能，调用`createStandardContextMenu()`并扩展返回的菜单。
事件信息通过`event`对象传递。

**官方示例：**

```cpp
 void MyQPlainTextEdit::contextMenuEvent(QContextMenuEvent *event)
 {
     QMenu *menu = createStandardContextMenu();
     menu->addAction(tr("My Menu Item"));
     //...
     menu->exec(event->globalPos());
     delete menu;
 }
```

### `[slot] void QPlainTextEdit::copy()`

**作用与语义：**

将选中的文本复制到剪贴板上。

### `[signal] void QPlainTextEdit::copyAvailable(bool yes)`

**作用与语义：**

当文本编辑中选择或取消选择文本时，会发出该信号。
当选择文本时，该信号将以`yes`设置为true的状态发出。如果未选择文本或取消选择文本，则以`yes`为false的状态发出该信号。
如果`yes`为真，那么可以用`copy()`将选件复制到剪贴板。如果`yes`为假，则不`copy()`。

### `[virtual protected] QMimeData *QPlainTextEdit::createMimeDataFromSelection() const`

**作用与语义：**

该函数返回一个新的 MIME 数据对象，以表示文本编辑当前选择的内容。当需要将选区封装到新的 `QMimeData` 对象中时，调用该功能;例如，当开始拖放操作，或将数据复制到剪贴板时。
如果你重新实现这个函数，注意返回`QMimeData`对象的所有权会传递给调用者。通过`textCursor()`函数可以检索选择。

### `QMenu *QPlainTextEdit::createStandardContextMenu()`

**作用与语义：**

该功能创建标准的上下文菜单，用户用鼠标右键点击文本编辑时会显示。该功能由默认`contextMenuEvent()`处理程序调用。弹出菜单的所有权转移给调用者。
我们建议你改用createStandardContextMenu（`QPoint`）版本，它会启用与用户点击位置敏感的操作。

### `QMenu *QPlainTextEdit::createStandardContextMenu(const QPoint &position)`

**作用与语义：**

该功能创建标准的上下文菜单，用户用鼠标右键点击文本编辑时会显示。该功能从默认`contextMenuEvent()`处理程序调用，并获取鼠标点击所在的文档坐标`position`。这可以启用对用户点击位置敏感的操作。弹出菜单的所有权转移给调用者。

### `QTextCharFormat QPlainTextEdit::currentCharFormat() const`

**作用与语义：**

返回插入新文本时使用的字符格式。

### `QTextCursor QPlainTextEdit::cursorForPosition(const QPoint &pos) const`

**作用与语义：**

返回位置`pos`（视口坐标内）的`QTextCursor`。

### `[signal] void QPlainTextEdit::cursorPositionChanged()`

**作用与语义：**

每当光标位置变化时，都会发出该信号。

### `QRect QPlainTextEdit::cursorRect() const`

**作用与语义：**

返回一个矩形（以视口坐标表示），其中包含文本编辑的光标。

### `QRect QPlainTextEdit::cursorRect(const QTextCursor &cursor) const`

**作用与语义：**

返回一个包含`cursor`的矩形（以视口坐标为单位）。

### `[slot] void QPlainTextEdit::cut()`

**作用与语义：**

将选中的文本复制到剪贴板，并从文本编辑中删除。
如果没有被选中的文本，什么都不会发生。

### `QTextDocument *QPlainTextEdit::document() const`

**作用与语义：**

返回指向底层文档的指针。

### `[override virtual protected] void QPlainTextEdit::dragEnterEvent(QDragEnterEvent *e)`

**作用与语义：**

重实现自：`QAbstractScrollArea::dragEnterEvent`（QDragEnterEvent *event）。

### `[override virtual protected] void QPlainTextEdit::dragLeaveEvent(QDragLeaveEvent *e)`

**作用与语义：**

重实现自：`QAbstractScrollArea::dragLeaveEvent`（QDragLeaveEvent *event）。

### `[override virtual protected] void QPlainTextEdit::dragMoveEvent(QDragMoveEvent *e)`

**作用与语义：**

重实现自：`QAbstractScrollArea::dragMoveEvent`（QDragMoveEvent *event）。

### `[override virtual protected] void QPlainTextEdit::dropEvent(QDropEvent *e)`

**作用与语义：**

重实现自：`QAbstractScrollArea::dropEvent`（QDropEvent *事件）。

### `void QPlainTextEdit::ensureCursorVisible()`

**作用与语义：**

必要时通过滚动文本编辑确保光标可见。

### `QList<QTextEdit::ExtraSelection> QPlainTextEdit::extraSelections() const`

**作用与语义：**

回报之前设置的额外选择。

### `bool QPlainTextEdit::find(const QString &exp, QTextDocument::FindFlags options = QTextDocument::FindFlags())`

**作用与语义：**

使用给定的`options`查找字符串的下一次出现`exp`。如果找到`exp`，返回`true`，并更改光标选择匹配;否则返回`false`。

### `bool QPlainTextEdit::find(const QRegularExpression &exp, QTextDocument::FindFlags options = QTextDocument::FindFlags())`

**作用与语义：**

用给定的`options`找到下一个与正则表达式`exp`匹配的出现。
如果找到匹配并更改光标选择匹配，返回`true`;否则返回`false`。
警告：出于历史原因，`exp` 设置的大小写敏感性选项被忽略。相反，`options`用于判断搜索是否具有大小写敏感性。

### `[protected] QTextBlock QPlainTextEdit::firstVisibleBlock() const`

**作用与语义：**

返回第一个可见的方块。

### `[override virtual protected] void QPlainTextEdit::focusInEvent(QFocusEvent *e)`

**作用与语义：**

重实现自：`QWidget::focusInEvent`（QFocusEvent *event）。
该事件处理程序可以在子类中重新实现，以接收控件的键盘焦点事件（焦点接收）。事件通过`event`参数传递。
小部件通常必须`setFocusPolicy()`到非`Qt::NoFocus`的对象才能接收焦点事件。（注意，应用程序员可以调用任何小部件`setFocus()`，即使是那些通常不接受焦点的小部件。）。
默认实现会更新小部件（除非是没有指定`focusPolicy()`的窗口）。

### `[override virtual protected] bool QPlainTextEdit::focusNextPrevChild(bool next)`

**作用与语义：**

重构：`QWidget::focusNextPrevChild`（下一个布尔）。
根据 Tab 和 Shift Tab 找到一个新的控件来给键盘焦点，如果能找到新控件，则返回 `true`，找不到则返回 false。
如果`next`为真，该函数向前搜索;如果`next`为假，则向后搜索。
有时，你会想重新实现这个函数。例如，浏览器可能会重新实现它，将“当前活跃链接”向前或向后移动，只有当它到达“页面”的最后或第一个链接时才调用 focusNextPrevChild()。
子控件调用其父控件的 focusNextPrevChild()，但只有包含子控件的窗口决定将焦点重定向到哪里。通过重新实现该函数，你就能控制所有子控件的焦点遍历。

### `[override virtual protected] void QPlainTextEdit::focusOutEvent(QFocusEvent *e)`

**作用与语义：**

重现：`QWidget::focusOutEvent`（QFocusEvent *event）。
该事件处理程序可以在子类中重新实现，以接收控件的键盘焦点事件（焦点丢失）。事件通过`event`参数传递。
小部件通常必须`setFocusPolicy()`到非`Qt::NoFocus`的对象才能接收焦点事件。（注意，应用程序员可以调用任何小部件`setFocus()`，即使是那些通常不接受焦点的小部件。）。
默认实现会更新小部件（除非是没有指定`focusPolicy()`的窗口）。

### `[protected] QAbstractTextDocumentLayout::PaintContext QPlainTextEdit::getPaintContext() const`

**作用与语义：**

返回`viewport()`的绘画上下文，仅在重新实现`paintEvent()`时有用。

### `[override virtual protected] void QPlainTextEdit::inputMethodEvent(QInputMethodEvent *e)`

**作用与语义：**

重实现自：`QWidget::inputMethodEvent`（QInputMethodEvent *event）。
对于事件`event`，该事件处理程序可以被重新实现到子类中以接收输入法组合事件。当输入方法的状态发生变化时，调用该处理程序。
注意，在创建自定义文本编辑小部件时，必须明确设置`Qt::WA_InputMethodEnabled`窗口属性（使用`setAttribute()`函数），才能接收输入法事件。
默认实现调用 event->ignore()，拒绝输入法事件。详情请参见 `QInputMethodEvent` 文档。

### `[override virtual] QVariant QPlainTextEdit::inputMethodQuery(Qt::InputMethodQuery property) const`

**作用与语义：**

重实现自：`QWidget::inputMethodQuery`（Qt：：InputMethodQuery query） const.
该方法仅适用于输入控件。输入方法用于查询控件的一组属性，以支持复杂的输入法操作，以支持周围文本和重新转换。
`query` 指定查询的属性。

### `[virtual protected] void QPlainTextEdit::insertFromMimeData(const QMimeData *source)`

**作用与语义：**

该函数将由`source`指定的内容插入当前光标位置的文本编辑中。每当通过剪贴板粘贴操作插入文本，或文本编辑接受拖放操作数据时，都会调用该功能。

### `[slot] void QPlainTextEdit::insertPlainText(const QString &text)`

**作用与语义：**

方便的槽函数，可以插入当前光标位置的`text`。
它等价于。

**官方示例：**

```cpp
 edit->textCursor().insertText(text);
```

### `[override virtual protected] void QPlainTextEdit::keyPressEvent(QKeyEvent *e)`

**作用与语义：**

处理按键事件 `event`，默认实现负责纯文本输入、选择、删除和快捷键。子类可拦截自定义按键；不处理时必须调用基类实现，否则标准编辑或场景键盘操作会失效。

### `[override virtual protected] void QPlainTextEdit::keyReleaseEvent(QKeyEvent *e)`

**作用与语义：**

重实现自：`QWidget::keyReleaseEvent`（QKeyEvent *event）。
该事件处理程序用于事件`event`，可以在子类中重新实现，以接收该小部件的密钥释放事件。
小部件必须先接受焦点并拥有焦点，才能接收密钥释放事件。
如果你重新实现这个处理器，如果你不对密钥进行操作，务必调用基类实现。
默认实现忽略事件，以便小部件的父节点能够解释事件。
注意`QKeyEvent`以 isAccepted() == true开头，所以你不需要调用`QKeyEvent::accept()`——只要你对密钥操作时不要调用基类实现即可。

### `[virtual] QVariant QPlainTextEdit::loadResource(int type, const QUrl &name)`

**作用与语义：**

加载由给定`type`和`name`指定的资源。
该函数是`QTextDocument::loadResource()`的扩展。

### `void QPlainTextEdit::mergeCurrentCharFormat(const QTextCharFormat &modifier)`

**作用与语义：**

通过在编辑器光标上调用`QTextCursor::mergeCharFormat`，将`modifier`中指定的属性合并到当前字符格式中。如果编辑器有选区，则`modifier`的属性直接应用到该选区。

### `[signal] void QPlainTextEdit::modificationChanged(bool changed)`

**作用与语义：**

每当文档内容发生变化，影响修改状态时，就会发出该信号。如果`changed`为真，则说明文档已被修改;否则为假。
例如，在文档上调用 setModified（false） 然后插入文本，信号就会被发出。如果你撤销该操作，使文档恢复到原始未修改状态，信号就会再次发出。

### `[override virtual protected] void QPlainTextEdit::mouseDoubleClickEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QAbstractScrollArea::mouseDoubleClickEvent`（QMouseEvent *e）。

### `[override virtual protected] void QPlainTextEdit::mouseMoveEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QAbstractScrollArea::mouseMoveEvent`（QMouseEvent *e）。

### `[override virtual protected] void QPlainTextEdit::mousePressEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QAbstractScrollArea::mousePressEvent`（QMouseEvent *e）。

### `[override virtual protected] void QPlainTextEdit::mouseReleaseEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QAbstractScrollArea::mouseReleaseEvent`（QMouseEvent *e）。

### `void QPlainTextEdit::moveCursor(QTextCursor::MoveOperation operation, QTextCursor::MoveMode mode = QTextCursor::MoveAnchor)`

**作用与语义：**

通过执行指定`operation`移动光标。
如果`mode` `QTextCursor::KeepAnchor`，光标会选择它移动的文本。这与用户按住Shift键并用光标键移动光标时的效果相同。

### `[override virtual protected] void QPlainTextEdit::paintEvent(QPaintEvent *e)`

**作用与语义：**

重实现自：`QAbstractScrollArea::paintEvent`（QPaintEvent *event）。

### `[slot] void QPlainTextEdit::paste()`

**作用与语义：**

将剪贴板上的文本粘贴到当前光标位置的文本编辑中。
如果剪贴板里没有文字，什么都不会发生。
要改变该函数的行为，即修改`QPlainTextEdit`可粘贴的内容及其粘贴方式，需重新实现虚拟 `canInsertFromMimeData()` 并`insertFromMimeData()`函数。

### `void QPlainTextEdit::print(QPagedPaintDevice *printer) const`

**作用与语义：**

方便函数将文本编辑的文档打印到给定的 `printer`。这等同于直接调用文档上的打印方法，但该函数还支持 QPrinter：：Selection 作为打印范围。

### `[slot] void QPlainTextEdit::redo()`

**作用与语义：**

重新做上次的操作。
如果没有重做操作，即撤销/重做历史中没有重做步骤，则不会发生任何事。

### `[signal] void QPlainTextEdit::redoAvailable(bool available)`

**作用与语义：**

每当重做操作可用（`available`为真）或不可用（`available`为假）时，该信号就会发出。

### `[override virtual protected] void QPlainTextEdit::resizeEvent(QResizeEvent *e)`

**作用与语义：**

重实现自：`QAbstractScrollArea::resizeEvent`（QResizeEvent *event）。

### `[override virtual protected] void QPlainTextEdit::scrollContentsBy(int dx, int dy)`

**作用与语义：**

重实现自：`QAbstractScrollArea::scrollContentsBy`（智力 dx，智力 dy）。
当滚动条被移动`dx`、`dy`时调用，因此视口内容应相应滚动。
默认实现只需调用整个`viewport()`的`update()`，子类可以重新实现该处理程序以优化，或者像`QScrollArea`一样移动内容控件。参数`dx`和`dy`是为了方便，让类知道应该滚动多少（比如像素移动时很有用）。你也可以忽略这些值，直接滚动到滚动条指示的位置。
调用该函数进行程序滚动是错误，建议使用滚动条（例如直接调用`QScrollBar::setValue()`）。

### `[slot] void QPlainTextEdit::selectAll()`

**作用与语义：**

选择所有文本。

### `[signal] void QPlainTextEdit::selectionChanged()`

**作用与语义：**

每当选择发生变化时，该信号都会发出。

### `void QPlainTextEdit::setCurrentCharFormat(const QTextCharFormat &format)`

**作用与语义：**

通过在编辑器光标上调用 `QTextCursor::setCharFormat()`，设置插入新文本到 `format` 时使用的字符格式。如果编辑器有选区，则将 char 格式直接应用于该选区。

### `void QPlainTextEdit::setDocument(QTextDocument *document)`

**作用与语义：**

这`document`成为文本编辑器的新文档。
所提供文档的父`QObject`仍然是该对象的所有者。如果当前文档是文本编辑器的子文档，则该文档将被删除。
文档必须具有继承`QPlainTextDocumentLayout`的文档布局（参见 `QTextDocument::setDocumentLayout()`）。

### `void QPlainTextEdit::setExtraSelections(const QList<QTextEdit::ExtraSelection> &selections)`

**作用与语义：**

该功能允许临时用指定颜色标记文档中的某些区域，具体颜色为`selections`。例如，在编程编辑器中，用特定背景色标记整行文本以表示断点的存在。

### `[slot] void QPlainTextEdit::setPlainText(const QString &text)`

**作用与语义：**

该属性获取并设置纯文本编辑器的内容。设置该属性后，之前的内容会被移除，撤销/重做历史也会被重置。`currentCharFormat()`也会被重置，除非`textCursor()`已经在文档开头。
默认情况下，对于无内容的编辑器，该属性包含空字符串。

**如何使用：** 调用 `setPlainText(...)` 修改 `plainText`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QPlainTextEdit::setTextCursor(const QTextCursor &cursor)`

**作用与语义：**

设定可见`cursor`。

### `[override virtual protected] void QPlainTextEdit::showEvent(QShowEvent *)`

**作用与语义：**

重实现自：`QWidget::showEvent`（QShowEvent *event）。
该事件处理程序可以在子类中重新实现，以接收传递给 `event` 参数的控件显示事件。
非自发的展示事件会在展示前立即发送到小部件。窗口的自发展示事件则在展示之后交付。
注意：当窗口系统改变其映射状态时，小部件会接收自发显示和隐藏事件，例如用户最小化窗口时自发隐藏事件，窗口恢复时自发显示事件。收到自发隐藏事件后，小部件仍被视为`isVisible()`可见。

### `[signal] void QPlainTextEdit::textChanged()`

**作用与语义：**

该属性获取并设置纯文本编辑器的内容。设置该属性后，之前的内容会被移除，撤销/重做历史也会被重置。`currentCharFormat()`也会被重置，除非`textCursor()`已经在文档开头。
默认情况下，对于无内容的编辑器，该属性包含空字符串。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `plainText` 的变化，不要把它当作普通函数主动调用。

### `QTextCursor QPlainTextEdit::textCursor() const`

**作用与语义：**

返回代表当前可见光标的`QTextCursor`副本。注意，返回光标的变化不会影响`QPlainTextEdit`的光标;使用`setTextCursor()`来更新可见光标。

### `QString QPlainTextEdit::toPlainText() const`

**作用与语义：**

该属性获取并设置纯文本编辑器的内容。设置该属性后，之前的内容会被移除，撤销/重做历史也会被重置。`currentCharFormat()`也会被重置，除非`textCursor()`已经在文档开头。
默认情况下，对于无内容的编辑器，该属性包含空字符串。

**如何使用：** 调用 `toPlainText()` 读取当前值；它不会修改应用状态。

### `[slot] void QPlainTextEdit::undo()`

**作用与语义：**

撤销上次的操作。
如果没有可撤销的操作，即撤销/重做历史中没有撤销步骤，则不会发生任何事。

### `[signal] void QPlainTextEdit::undoAvailable(bool available)`

**作用与语义：**

每当撤销操作可用（`available`为真）或不可用（`available`为假）时，该信号都会发出。

### `[signal] void QPlainTextEdit::updateRequest(const QRect &rect, int dy)`

**作用与语义：**

当文本文档需要更新指定`rect`时，该信号会发出。如果文本被滚动，`rect`会覆盖整个视口区域。如果文本是垂直滚动，`dy`会显示视口被滚动的像素数。
信号的目的是支持纯文本编辑子类中的额外控件，例如显示行号、断点或其他额外信息。

### `[override virtual protected] void QPlainTextEdit::wheelEvent(QWheelEvent *e)`

**作用与语义：**

重实现自：`QAbstractScrollArea::wheelEvent`（QWheelEvent *e）。

### `[slot] void QPlainTextEdit::zoomIn(int range = 1)`

**作用与语义：**

通过将基础字体大小`range`点放大，并将所有字体大小重新计算为新大小来放大文本。这不会改变任何图片的大小。

### `[slot] void QPlainTextEdit::zoomOut(int range = 1)`

**作用与语义：**

通过缩小基础字体大小`range`点，并重新计算所有字体大小为新大小来缩放文本。这不会改变任何图片的大小。

### `enum LineWrapMode { NoWrap, WidgetWidth }`

**作用与语义：**

控制纯文本编辑器的换行：`NoWrap` 保持逻辑行并允许水平滚动，`WidgetWidth` 按视口宽度折行。折行只改变显示，不会向文档插入换行符。

### `bool backgroundVisible() const`

**作用与语义：**

该属性决定调色板背景是否在文档区域外可见。
如果设置为 true，纯文本编辑会在未被文本文档覆盖的视口区域绘制调色板背景。否则，如果设置为 false，则不会。该功能使用户能够直观区分文档中用调色板底色绘制的区域，以及未被任何文档覆盖的空白区域。
默认是假的。

**如何使用：** 调用 `backgroundVisible()` 读取当前值；它不会修改应用状态。

### `int blockCount() const`

**作用与语义：**

该属性包含文档中的文本块数量。
默认情况下，在空文档中，该属性的值为1。

**如何使用：** 调用 `blockCount()` 读取当前值；它不会修改应用状态。

### `bool centerOnScroll() const`

**作用与语义：**

该属性决定光标是否应置中于屏幕。
如果设置为 true，纯文本编辑会将文档垂直滚动，使光标在视口中心可见。这也允许文本编辑滚动到文档末尾以下。否则，如果设置为 false，纯文本编辑会尽可能少地滚动，以确保光标可见。同样的算法适用于通过 `appendPlainText()` 添加的任何新行。
默认是假的。

**如何使用：** 调用 `centerOnScroll()` 读取当前值；它不会修改应用状态。

### `int cursorWidth() const`

**作用与语义：**

该属性指定光标的宽度（像素单位）。默认值为1。

**如何使用：** 调用 `cursorWidth()` 读取当前值；它不会修改应用状态。

### `QString documentTitle() const`

**作用与语义：**

该属性包含从文本中解析出来的文档标题。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `documentTitle()` 读取当前值；它不会修改应用状态。

### `bool isReadOnly() const`

**作用与语义：**

该属性决定文本编辑是否为只读。
在只读文本编辑中，用户只能浏览文本并选择文本;无法修改文本。
该属性的默认值为假。

**如何使用：** 调用 `isReadOnly()` 读取当前值；它不会修改应用状态。

### `bool isUndoRedoEnabled() const`

**作用与语义：**

该属性是否允许撤销和重做。
用户只有在该属性成立且存在可撤销（或重做）的操作时，才能撤销或重做操作。
默认情况下，该属性为`true`。

**如何使用：** 调用 `isUndoRedoEnabled()` 读取当前值；它不会修改应用状态。

### `QPlainTextEdit::LineWrapMode lineWrapMode() const`

**作用与语义：**

该属性表示了线环模式。
默认模式是`WidgetWidth`，使文字在文本编辑的右侧边缘被包裹。包裹发生在空白处，保持整词完整。如果你希望在单词内进行折叠，请使用`setWordWrapMode()`。

**如何使用：** 调用 `lineWrapMode()` 读取当前值；它不会修改应用状态。

### `int maximumBlockCount() const`

**作用与语义：**

该属性限制了文档中块的限制。
指定文档可拥有的最大块数。如果文档中有更多带有该属性的块，则从文档开头移除块。
负值或零值表示文档可以包含无限数量的块。
默认值是0。
注意，设置该属性会立即将限制应用到文档内容上。设置该属性还会禁用撤销重做历史。

**如何使用：** 调用 `maximumBlockCount()` 读取当前值；它不会修改应用状态。

### `bool overwriteMode() const`

**作用与语义：**

该属性决定了用户输入的文本是否会覆盖现有文本。
与许多文本编辑器一样，纯文本编辑器小部件可以配置为插入或覆盖用户输入的新文本。
如果`true`该属性，现有文本会逐字符被新文本覆盖;否则，文本会在光标位置插入，取代现有文本。
默认情况下，该属性为`false`（新文本不会覆盖现有文本）。

**如何使用：** 调用 `overwriteMode()` 读取当前值；它不会修改应用状态。

### `QString placeholderText() const`

**作用与语义：**

该属性包含编辑器占位文本。
设置该属性后，只要`document()`为空，编辑器就会显示一个灰色的占位文本。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `placeholderText()` 读取当前值；它不会修改应用状态。

### `void setBackgroundVisible(bool visible)`

**作用与语义：**

该属性决定调色板背景是否在文档区域外可见。
如果设置为 true，纯文本编辑会在未被文本文档覆盖的视口区域绘制调色板背景。否则，如果设置为 false，则不会。该功能使用户能够直观区分文档中用调色板底色绘制的区域，以及未被任何文档覆盖的空白区域。
默认是假的。

**如何使用：** 调用 `setBackgroundVisible(...)` 修改 `backgroundVisible`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setCenterOnScroll(bool enabled)`

**作用与语义：**

该属性决定光标是否应置中于屏幕。
如果设置为 true，纯文本编辑会将文档垂直滚动，使光标在视口中心可见。这也允许文本编辑滚动到文档末尾以下。否则，如果设置为 false，纯文本编辑会尽可能少地滚动，以确保光标可见。同样的算法适用于通过 `appendPlainText()` 添加的任何新行。
默认是假的。

**如何使用：** 调用 `setCenterOnScroll(...)` 修改 `centerOnScroll`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setCursorWidth(int width)`

**作用与语义：**

该属性指定光标的宽度（像素单位）。默认值为1。

**如何使用：** 调用 `setCursorWidth(...)` 修改 `cursorWidth`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setDocumentTitle(const QString &title)`

**作用与语义：**

该属性包含从文本中解析出来的文档标题。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `setDocumentTitle(...)` 修改 `documentTitle`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setLineWrapMode(QPlainTextEdit::LineWrapMode mode)`

**作用与语义：**

该属性表示了线环模式。
默认模式是`WidgetWidth`，使文字在文本编辑的右侧边缘被包裹。包裹发生在空白处，保持整词完整。如果你希望在单词内进行折叠，请使用`setWordWrapMode()`。

**如何使用：** 调用 `setLineWrapMode(...)` 修改 `lineWrapMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMaximumBlockCount(int maximum)`

**作用与语义：**

该属性限制了文档中块的限制。
指定文档可拥有的最大块数。如果文档中有更多带有该属性的块，则从文档开头移除块。
负值或零值表示文档可以包含无限数量的块。
默认值是0。
注意，设置该属性会立即将限制应用到文档内容上。设置该属性还会禁用撤销重做历史。

**如何使用：** 调用 `setMaximumBlockCount(...)` 修改 `maximumBlockCount`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setOverwriteMode(bool overwrite)`

**作用与语义：**

该属性决定了用户输入的文本是否会覆盖现有文本。
与许多文本编辑器一样，纯文本编辑器小部件可以配置为插入或覆盖用户输入的新文本。
如果`true`该属性，现有文本会逐字符被新文本覆盖;否则，文本会在光标位置插入，取代现有文本。
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

规定标签在显示文本时应如何与用户输入交互。
如果标志中包含`Qt::LinksAccessibleByKeyboard`或`Qt::TextSelectableByKeyboard`，那么焦点策略也会自动设置为`Qt::ClickFocus`。
默认值取决于`QPlainTextEdit`是只读还是可编辑。

**如何使用：** 调用 `setTextInteractionFlags(...)` 修改 `textInteractionFlags`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setUndoRedoEnabled(bool enable)`

**作用与语义：**

该属性是否允许撤销和重做。
用户只有在该属性成立且存在可撤销（或重做）的操作时，才能撤销或重做操作。
默认情况下，该属性为`true`。

**如何使用：** 调用 `setUndoRedoEnabled(...)` 修改 `undoRedoEnabled`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setWordWrapMode(QTextOption::WrapMode policy)`

**作用与语义：**

该属性表示`QPlainTextEdit`在用单词包裹文本时所采用的模式。
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

规定标签在显示文本时应如何与用户输入交互。
如果标志中包含`Qt::LinksAccessibleByKeyboard`或`Qt::TextSelectableByKeyboard`，那么焦点策略也会自动设置为`Qt::ClickFocus`。
默认值取决于`QPlainTextEdit`是只读还是可编辑。

**如何使用：** 调用 `textInteractionFlags()` 读取当前值；它不会修改应用状态。

### `QTextOption::WrapMode wordWrapMode() const`

**作用与语义：**

该属性表示`QPlainTextEdit`在用单词包裹文本时所采用的模式。
默认情况下，该属性设置为`QTextOption::WrapAtWordBoundaryOrAnywhere`。

**如何使用：** 调用 `wordWrapMode()` 读取当前值；它不会修改应用状态。

## 6. 深入实践与常见坑

### 生命周期和资源边界

控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

### 状态和错误边界

控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

### 线程边界

所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

### 最容易出现的错误

优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QPlainTextEdit` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
