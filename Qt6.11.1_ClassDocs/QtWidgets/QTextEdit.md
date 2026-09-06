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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 146 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QTextEdit::AutoFormattingFlagflags QTextEdit::AutoFormatting`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QTextEdit` 暴露的类型声明 `Auto、Formatting、Flagflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:AutoFormattingFlagflags QTextEdit::AutoFormatting`。
- 属性名：`QTextEdit`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `acceptRichText : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QTextEdit` 的配置属性。初始化或状态切换时通过 `setAcceptRichText(...)` 设置，之后用 `acceptRichText()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`acceptRichText`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `autoFormatting : AutoFormatting`

**API 类别：** 属性说明

**中文解读：** 这是 `QTextEdit` 的配置属性。初始化或状态切换时通过 `setAutoFormatting(...)` 设置，之后用 `autoFormatting()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`AutoFormatting`。
- 属性名：`autoFormatting`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `cursorWidth : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QTextEdit` 的配置属性。初始化或状态切换时通过 `setCursorWidth(...)` 设置，之后用 `cursorWidth()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`cursorWidth`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `document : QTextDocument*`

**API 类别：** 属性说明

**中文解读：** 这是 `QTextEdit` 的配置属性。初始化或状态切换时通过 `setDocument(...)` 设置，之后用 `document()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QTextDocument*`。
- 属性名：`document`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `documentTitle : QString`

**API 类别：** 属性说明

**中文解读：** 这是 `QTextEdit` 的配置属性。初始化或状态切换时通过 `setDocumentTitle(...)` 设置，之后用 `documentTitle()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QString`。
- 属性名：`documentTitle`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `html : QString`

**API 类别：** 属性说明

**中文解读：** 这是 `QTextEdit` 的配置属性。初始化或状态切换时通过 `setHtml(...)` 设置，之后用 `html()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QString`。
- 属性名：`html`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `lineWrapColumnOrWidth : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QTextEdit` 的配置属性。初始化或状态切换时通过 `setLineWrapColumnOrWidth(...)` 设置，之后用 `lineWrapColumnOrWidth()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`lineWrapColumnOrWidth`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `lineWrapMode : LineWrapMode`

**API 类别：** 属性说明

**中文解读：** 这是 `QTextEdit` 的配置属性。初始化或状态切换时通过 `setLineWrapMode(...)` 设置，之后用 `lineWrapMode()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`LineWrapMode`。
- 属性名：`lineWrapMode`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `markdown : QString`

**API 类别：** 属性说明

**中文解读：** 这是 `QTextEdit` 的配置属性。初始化或状态切换时通过 `setMarkdown(...)` 设置，之后用 `markdown()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QString`。
- 属性名：`markdown`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `overwriteMode : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QTextEdit` 的配置属性。初始化或状态切换时通过 `setOverwriteMode(...)` 设置，之后用 `overwriteMode()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`overwriteMode`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `placeholderText : QString`

**API 类别：** 属性说明

**中文解读：** 这是 `QTextEdit` 的配置属性。初始化或状态切换时通过 `setPlaceholderText(...)` 设置，之后用 `placeholderText()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QString`。
- 属性名：`placeholderText`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `plainText : QString`

**API 类别：** 属性说明

**中文解读：** 这是 `QTextEdit` 的配置属性。初始化或状态切换时通过 `setPlainText(...)` 设置，之后用 `plainText()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QString`。
- 属性名：`plainText`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `readOnly : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QTextEdit` 的配置属性。初始化或状态切换时通过 `setReadOnly(...)` 设置，之后用 `readOnly()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`readOnly`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `tabChangesFocus : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QTextEdit` 的配置属性。初始化或状态切换时通过 `setTabChangesFocus(...)` 设置，之后用 `tabChangesFocus()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`tabChangesFocus`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `tabStopDistance : qreal`

**API 类别：** 属性说明

**中文解读：** 这是 `QTextEdit` 的配置属性。初始化或状态切换时通过 `setTabStopDistance(...)` 设置，之后用 `tabStopDistance()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`qreal`。
- 属性名：`tabStopDistance`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `textInteractionFlags : Qt::TextInteractionFlags`

**API 类别：** 属性说明

**中文解读：** 这是 `QTextEdit` 的配置属性。初始化或状态切换时通过 `setTextInteractionFlags(...)` 设置，之后用 `TextInteractionFlags()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`Qt::TextInteractionFlags`。
- 属性名：`textInteractionFlags`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `undoRedoEnabled : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QTextEdit` 的配置属性。初始化或状态切换时通过 `setUndoRedoEnabled(...)` 设置，之后用 `undoRedoEnabled()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`undoRedoEnabled`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `wordWrapMode : QTextOption::WrapMode`

**API 类别：** 属性说明

**中文解读：** 这是 `QTextEdit` 的配置属性。初始化或状态切换时通过 `setWrapMode(...)` 设置，之后用 `WrapMode()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QTextOption::WrapMode`。
- 属性名：`wordWrapMode`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QTextEdit::QTextEdit(QWidget *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextEdit` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `parent`：类型为 `QWidget *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QTextEdit::QTextEdit(const QString &text, QWidget *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextEdit` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。
- 参数 `parent`：类型为 `QWidget *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QTextEdit::~QTextEdit()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextEdit` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Qt::Alignment QTextEdit::alignment() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextEdit::alignment` 用于计算、查询或取得与“对齐方式”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `Qt::Alignment`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::Alignment`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QTextEdit::anchorAt(const QPoint &pos) const`

**API 类别：** 成员函数说明

**中文解读：** `QTextEdit::anchorAt` 用于计算、查询或取得与“anchor、按位置访问”相关的操作。调用时要先确认当前状态和 `pos` 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数 `pos`：类型为 `const QPoint &`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QTextEdit::append(const QString &text)`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `append`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] bool QTextEdit::canInsertFromMimeData(const QMimeData *source) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `canInsertFromMimeData`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `source`：类型为 `const QMimeData *`。没有默认值，调用时必须提供。源对象、源索引或源数据；它通常决定操作的输入，转换后要确认源的生命周期和线程归属。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QTextEdit::canPaste() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `canPaste`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QTextEdit::changeEvent(QEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** `QTextEdit::changeEvent` 用于执行与“change、Event”相关的操作。调用时要先确认当前状态和 `e` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `e`：类型为 `QEvent *`。没有默认值，调用时必须提供。传入 `QEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QTextEdit::clear()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `clear`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QTextEdit::contextMenuEvent(QContextMenuEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QTextEdit::contextMenuEvent` 用于执行与“context、Menu、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QContextMenuEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QTextEdit::copy()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `copy`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QTextEdit::copyAvailable(bool yes)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextEdit` 发出的通知信号 `copyAvailable`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `yes`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] QMimeData *QTextEdit::createMimeDataFromSelection() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextEdit::createMimeDataFromSelection` 用于计算、查询或取得与“创建、Mime、数据访问、转换进入、Selection”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMimeData *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMimeData *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMenu *QTextEdit::createStandardContextMenu()`

**API 类别：** 成员函数说明

**中文解读：** `QTextEdit::createStandardContextMenu` 用于计算、查询或取得与“创建、Standard、Context、Menu”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMenu *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMenu *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMenu *QTextEdit::createStandardContextMenu(const QPoint &position)`

**API 类别：** 成员函数说明

**中文解读：** `QTextEdit::createStandardContextMenu` 用于计算、查询或取得与“创建、Standard、Context、Menu”相关的操作。调用时要先确认当前状态和 `position` 的有效范围；返回类型是 `QMenu *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMenu *`。
- 参数 `position`：类型为 `const QPoint &`。没有默认值，调用时必须提供。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextCharFormat QTextEdit::currentCharFormat() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextEdit::currentCharFormat` 用于计算、查询或取得与“当前、Char、格式化”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QTextCharFormat`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextCharFormat`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QTextEdit::currentCharFormatChanged(const QTextCharFormat &f)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextEdit` 发出的通知信号 `currentCharFormatChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `f`：类型为 `const QTextCharFormat &`。没有默认值，调用时必须提供。传入 `const QTextCharFormat &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFont QTextEdit::currentFont() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextEdit::currentFont` 用于计算、查询或取得与“当前、字体”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QFont`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QFont`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextCursor QTextEdit::cursorForPosition(const QPoint &pos) const`

**API 类别：** 成员函数说明

**中文解读：** `QTextEdit::cursorForPosition` 用于计算、查询或取得与“cursor、For、Position”相关的操作。调用时要先确认当前状态和 `pos` 的有效范围；返回类型是 `QTextCursor`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextCursor`。
- 参数 `pos`：类型为 `const QPoint &`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QTextEdit::cursorPositionChanged()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextEdit` 发出的通知信号 `cursorPositionChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRect QTextEdit::cursorRect() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextEdit::cursorRect` 用于计算、查询或取得与“cursor、Rect”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRect`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRect`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRect QTextEdit::cursorRect(const QTextCursor &cursor) const`

**API 类别：** 成员函数说明

**中文解读：** `QTextEdit::cursorRect` 用于计算、查询或取得与“cursor、Rect”相关的操作。调用时要先确认当前状态和 `cursor` 的有效范围；返回类型是 `QRect`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRect`。
- 参数 `cursor`：类型为 `const QTextCursor &`。没有默认值，调用时必须提供。传入 `const QTextCursor &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QTextEdit::cut()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `cut`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QTextEdit::dragEnterEvent(QDragEnterEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** `QTextEdit::dragEnterEvent` 用于执行与“drag、Enter、Event”相关的操作。调用时要先确认当前状态和 `e` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `e`：类型为 `QDragEnterEvent *`。没有默认值，调用时必须提供。传入 `QDragEnterEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QTextEdit::dragLeaveEvent(QDragLeaveEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** `QTextEdit::dragLeaveEvent` 用于执行与“drag、Leave、Event”相关的操作。调用时要先确认当前状态和 `e` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `e`：类型为 `QDragLeaveEvent *`。没有默认值，调用时必须提供。传入 `QDragLeaveEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QTextEdit::dragMoveEvent(QDragMoveEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** `QTextEdit::dragMoveEvent` 用于执行与“drag、移动、Event”相关的操作。调用时要先确认当前状态和 `e` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `e`：类型为 `QDragMoveEvent *`。没有默认值，调用时必须提供。传入 `QDragMoveEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QTextEdit::dropEvent(QDropEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** `QTextEdit::dropEvent` 用于执行与“drop、Event”相关的操作。调用时要先确认当前状态和 `e` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `e`：类型为 `QDropEvent *`。没有默认值，调用时必须提供。传入 `QDropEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextEdit::ensureCursorVisible()`

**API 类别：** 成员函数说明

**中文解读：** `QTextEdit::ensureCursorVisible` 用于执行与“ensure、Cursor、可见状态”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QTextEdit::ExtraSelection> QTextEdit::extraSelections() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextEdit::extraSelections` 用于计算、查询或取得与“extra、Selections”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<QTextEdit::ExtraSelection>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QTextEdit::ExtraSelection>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QTextEdit::find(const QString &exp, QTextDocument::FindFlags options = QTextDocument::FindFlags())`

**API 类别：** 成员函数说明

**中文解读：** `QTextEdit::find` 用于计算、查询或取得与“查找”相关的操作。调用时要先确认当前状态和 `exp`、`options` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `exp`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `options`：类型为 `QTextDocument::FindFlags`。默认值为 `QTextDocument::FindFlags()`。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QTextEdit::find(const QRegularExpression &exp, QTextDocument::FindFlags options = QTextDocument::FindFlags())`

**API 类别：** 成员函数说明

**中文解读：** `QTextEdit::find` 用于计算、查询或取得与“查找”相关的操作。调用时要先确认当前状态和 `exp`、`options` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `exp`：类型为 `const QRegularExpression &`。没有默认值，调用时必须提供。传入 `const QRegularExpression &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `options`：类型为 `QTextDocument::FindFlags`。默认值为 `QTextDocument::FindFlags()`。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QTextEdit::focusInEvent(QFocusEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** `QTextEdit::focusInEvent` 用于执行与“focus、In、Event”相关的操作。调用时要先确认当前状态和 `e` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `e`：类型为 `QFocusEvent *`。没有默认值，调用时必须提供。传入 `QFocusEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] bool QTextEdit::focusNextPrevChild(bool next)`

**API 类别：** 成员函数说明

**中文解读：** `QTextEdit::focusNextPrevChild` 用于计算、查询或取得与“focus、移动到下一项、Prev、Child”相关的操作。调用时要先确认当前状态和 `next` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `next`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QTextEdit::focusOutEvent(QFocusEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** `QTextEdit::focusOutEvent` 用于执行与“focus、Out、Event”相关的操作。调用时要先确认当前状态和 `e` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `e`：类型为 `QFocusEvent *`。没有默认值，调用时必须提供。传入 `QFocusEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QTextEdit::fontFamily() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextEdit::fontFamily` 用于计算、查询或取得与“字体、Family”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QTextEdit::fontItalic() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextEdit::fontItalic` 用于计算、查询或取得与“字体、Italic”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal QTextEdit::fontPointSize() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextEdit::fontPointSize` 用于计算、查询或取得与“字体、Point、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QTextEdit::fontUnderline() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextEdit::fontUnderline` 用于计算、查询或取得与“字体、Underline”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QTextEdit::fontWeight() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextEdit::fontWeight` 用于计算、查询或取得与“字体、Weight”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QTextEdit::inputMethodEvent(QInputMethodEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** `QTextEdit::inputMethodEvent` 用于执行与“input、Method、Event”相关的操作。调用时要先确认当前状态和 `e` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `e`：类型为 `QInputMethodEvent *`。没有默认值，调用时必须提供。传入 `QInputMethodEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QVariant QTextEdit::inputMethodQuery(Qt::InputMethodQuery property) const`

**API 类别：** 成员函数说明

**中文解读：** `QTextEdit::inputMethodQuery` 用于计算、查询或取得与“input、Method、查询”相关的操作。调用时要先确认当前状态和 `property` 的有效范围；返回类型是 `QVariant`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVariant`。
- 参数 `property`：类型为 `Qt::InputMethodQuery`。没有默认值，调用时必须提供。传入 `Qt::InputMethodQuery` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QTextEdit::insertFromMimeData(const QMimeData *source)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QTextEdit` 添加依赖、数据或子对象的 API `insertFromMimeData`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `source`：类型为 `const QMimeData *`。没有默认值，调用时必须提供。源对象、源索引或源数据；它通常决定操作的输入，转换后要确认源的生命周期和线程归属。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QTextEdit::insertHtml(const QString &text)`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `insertHtml`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QTextEdit::insertPlainText(const QString &text)`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `insertPlainText`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QTextEdit::keyPressEvent(QKeyEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** `QTextEdit::keyPressEvent` 用于执行与“key、Press、Event”相关的操作。调用时要先确认当前状态和 `e` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `e`：类型为 `QKeyEvent *`。没有默认值，调用时必须提供。传入 `QKeyEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QTextEdit::keyReleaseEvent(QKeyEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** `QTextEdit::keyReleaseEvent` 用于执行与“key、释放、Event”相关的操作。调用时要先确认当前状态和 `e` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `e`：类型为 `QKeyEvent *`。没有默认值，调用时必须提供。传入 `QKeyEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual invokable] QVariant QTextEdit::loadResource(int type, const QUrl &name)`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `loadResource`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QVariant`。
- 参数 `type`：类型为 `int`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。
- 参数 `name`：类型为 `const QUrl &`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextEdit::mergeCurrentCharFormat(const QTextCharFormat &modifier)`

**API 类别：** 成员函数说明

**中文解读：** `QTextEdit::mergeCurrentCharFormat` 用于执行与“merge、当前、Char、格式化”相关的操作。调用时要先确认当前状态和 `modifier` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `modifier`：类型为 `const QTextCharFormat &`。没有默认值，调用时必须提供。传入 `const QTextCharFormat &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QTextEdit::mouseDoubleClickEvent(QMouseEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** `QTextEdit::mouseDoubleClickEvent` 用于执行与“mouse、Double、Click、Event”相关的操作。调用时要先确认当前状态和 `e` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `e`：类型为 `QMouseEvent *`。没有默认值，调用时必须提供。传入 `QMouseEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QTextEdit::mouseMoveEvent(QMouseEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** `QTextEdit::mouseMoveEvent` 用于执行与“mouse、移动、Event”相关的操作。调用时要先确认当前状态和 `e` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `e`：类型为 `QMouseEvent *`。没有默认值，调用时必须提供。传入 `QMouseEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QTextEdit::mousePressEvent(QMouseEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** `QTextEdit::mousePressEvent` 用于执行与“mouse、Press、Event”相关的操作。调用时要先确认当前状态和 `e` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `e`：类型为 `QMouseEvent *`。没有默认值，调用时必须提供。传入 `QMouseEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QTextEdit::mouseReleaseEvent(QMouseEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** `QTextEdit::mouseReleaseEvent` 用于执行与“mouse、释放、Event”相关的操作。调用时要先确认当前状态和 `e` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `e`：类型为 `QMouseEvent *`。没有默认值，调用时必须提供。传入 `QMouseEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextEdit::moveCursor(QTextCursor::MoveOperation operation, QTextCursor::MoveMode mode = QTextCursor::MoveAnchor)`

**API 类别：** 成员函数说明

**中文解读：** `QTextEdit::moveCursor` 用于执行与“移动、Cursor”相关的操作。调用时要先确认当前状态和 `operation`、`mode` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `operation`：类型为 `QTextCursor::MoveOperation`。没有默认值，调用时必须提供。传入 `QTextCursor::MoveOperation` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `mode`：类型为 `QTextCursor::MoveMode`。默认值为 `QTextCursor::MoveAnchor`。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QTextEdit::paintEvent(QPaintEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextEdit` 的核心操作 `paintEvent`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QPaintEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QTextEdit::paste()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `paste`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextEdit::print(QPagedPaintDevice *printer) const`

**API 类别：** 成员函数说明

**中文解读：** `QTextEdit::print` 用于执行与“print”相关的操作。调用时要先确认当前状态和 `printer` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `printer`：类型为 `QPagedPaintDevice *`。没有默认值，调用时必须提供。传入 `QPagedPaintDevice *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QTextEdit::redo()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `redo`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QTextEdit::redoAvailable(bool available)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextEdit` 发出的通知信号 `redoAvailable`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `available`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QTextEdit::resizeEvent(QResizeEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** `QTextEdit::resizeEvent` 用于执行与“调整尺寸、Event”相关的操作。调用时要先确认当前状态和 `e` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `e`：类型为 `QResizeEvent *`。没有默认值，调用时必须提供。传入 `QResizeEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QTextEdit::scrollContentsBy(int dx, int dy)`

**API 类别：** 成员函数说明

**中文解读：** `QTextEdit::scrollContentsBy` 用于执行与“scroll、Contents、By”相关的操作。调用时要先确认当前状态和 `dx`、`dy` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `dx`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `dy`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QTextEdit::scrollToAnchor(const QString &name)`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `scrollToAnchor`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `name`：类型为 `const QString &`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QTextEdit::selectAll()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `selectAll`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QTextEdit::selectionChanged()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextEdit` 发出的通知信号 `selectionChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QTextEdit::setAlignment(Qt::Alignment a)`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `setAlignment`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `a`：类型为 `Qt::Alignment`。没有默认值，调用时必须提供。传入 `Qt::Alignment` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextEdit::setCurrentCharFormat(const QTextCharFormat &format)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setCurrentCharFormat`。调用它会改变 `QTextEdit` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `format`：类型为 `const QTextCharFormat &`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QTextEdit::setCurrentFont(const QFont &f)`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `setCurrentFont`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `f`：类型为 `const QFont &`。没有默认值，调用时必须提供。传入 `const QFont &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextEdit::setExtraSelections(const QList<QTextEdit::ExtraSelection> &selections)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setExtraSelections`。调用它会改变 `QTextEdit` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `selections`：类型为 `const QList<QTextEdit::ExtraSelection> &`。没有默认值，调用时必须提供。传入 `const QList<QTextEdit::ExtraSelection> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QTextEdit::setFontFamily(const QString &fontFamily)`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `setFontFamily`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `fontFamily`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QTextEdit::setFontItalic(bool italic)`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `setFontItalic`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `italic`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QTextEdit::setFontPointSize(qreal s)`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `setFontPointSize`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `s`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QTextEdit::setFontUnderline(bool underline)`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `setFontUnderline`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `underline`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QTextEdit::setFontWeight(int weight)`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `setFontWeight`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `weight`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QTextEdit::setPlainText(const QString &text)`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `setPlainText`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QTextEdit::setText(const QString &text)`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `setText`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QTextEdit::setTextBackgroundColor(const QColor &c)`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `setTextBackgroundColor`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `c`：类型为 `const QColor &`。没有默认值，调用时必须提供。传入 `const QColor &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QTextEdit::setTextColor(const QColor &c)`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `setTextColor`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `c`：类型为 `const QColor &`。没有默认值，调用时必须提供。传入 `const QColor &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextEdit::setTextCursor(const QTextCursor &cursor)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setTextCursor`。调用它会改变 `QTextEdit` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `cursor`：类型为 `const QTextCursor &`。没有默认值，调用时必须提供。传入 `const QTextCursor &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QTextEdit::showEvent(QShowEvent *)`

**API 类别：** 成员函数说明

**中文解读：** `QTextEdit::showEvent` 用于执行与“显示、Event”相关的操作。调用时要先确认当前状态和 `QShowEvent *` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `QShowEvent *`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 通常在控件完成 parent、layout、属性和信号连接后调用；顶层窗口显示后由事件循环处理绘制和输入。

### `QColor QTextEdit::textBackgroundColor() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextEdit::textBackgroundColor` 用于计算、查询或取得与“文本、Background、Color”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QColor`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QColor`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QTextEdit::textChanged()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextEdit` 发出的通知信号 `textChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QColor QTextEdit::textColor() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextEdit::textColor` 用于计算、查询或取得与“文本、Color”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QColor`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QColor`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextCursor QTextEdit::textCursor() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextEdit::textCursor` 用于计算、查询或取得与“文本、Cursor”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QTextCursor`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextCursor`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QTextEdit::toPlainText() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toPlainText`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QTextEdit::undo()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `undo`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QTextEdit::undoAvailable(bool available)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextEdit` 发出的通知信号 `undoAvailable`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `available`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QTextEdit::wheelEvent(QWheelEvent *e)`

**API 类别：** 成员函数说明

**中文解读：** `QTextEdit::wheelEvent` 用于执行与“wheel、Event”相关的操作。调用时要先确认当前状态和 `e` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `e`：类型为 `QWheelEvent *`。没有默认值，调用时必须提供。传入 `QWheelEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QTextEdit::zoomIn(int range = 1)`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `zoomIn`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `range`：类型为 `int`。默认值为 `1`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QTextEdit::zoomOut(int range = 1)`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `zoomOut`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `range`：类型为 `int`。默认值为 `1`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `struct ExtraSelection`

**API 类别：** 公有类型

**中文解读：** 这是 `QTextEdit` 的 `Extra、Selection` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags AutoFormatting`

**API 类别：** 公有类型

**中文解读：** 这是 `QTextEdit` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum AutoFormattingFlag { AutoNone, AutoBulletList, AutoAll }`

**API 类别：** 公有类型

**中文解读：** 这是 `QTextEdit` 暴露的类型声明 `Auto、Formatting、Flag`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum LineWrapMode { NoWrap, WidgetWidth, FixedPixelWidth, FixedColumnWidth }`

**API 类别：** 公有类型

**中文解读：** 这是 `QTextEdit` 暴露的类型声明 `行、Wrap、模式`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool acceptRichText() const`

**API 类别：** 公有函数

**中文解读：** `QTextEdit::acceptRichText` 用于计算、查询或取得与“接受、Rich、文本”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextEdit::AutoFormatting autoFormatting() const`

**API 类别：** 公有函数

**中文解读：** `QTextEdit::autoFormatting` 用于计算、查询或取得与“auto、Formatting”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QTextEdit::AutoFormatting`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextEdit::AutoFormatting`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int cursorWidth() const`

**API 类别：** 公有函数

**中文解读：** `QTextEdit::cursorWidth` 用于计算、查询或取得与“cursor、宽度”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextDocument * document() const`

**API 类别：** 公有函数

**中文解读：** `QTextEdit::document` 用于计算、查询或取得与“document”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QTextDocument *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextDocument *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString documentTitle() const`

**API 类别：** 公有函数

**中文解读：** `QTextEdit::documentTitle` 用于计算、查询或取得与“document、Title”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool isReadOnly() const`

**API 类别：** 公有函数

**中文解读：** 这是查询 API `isReadOnly`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool isUndoRedoEnabled() const`

**API 类别：** 公有函数

**中文解读：** 这是查询 API `isUndoRedoEnabled`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int lineWrapColumnOrWidth() const`

**API 类别：** 公有函数

**中文解读：** `QTextEdit::lineWrapColumnOrWidth` 用于计算、查询或取得与“行、Wrap、列、Or、宽度”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextEdit::LineWrapMode lineWrapMode() const`

**API 类别：** 公有函数

**中文解读：** `QTextEdit::lineWrapMode` 用于计算、查询或取得与“行、Wrap、模式”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QTextEdit::LineWrapMode`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextEdit::LineWrapMode`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool overwriteMode() const`

**API 类别：** 公有函数

**中文解读：** `QTextEdit::overwriteMode` 用于计算、查询或取得与“overwrite、模式”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString placeholderText() const`

**API 类别：** 公有函数

**中文解读：** `QTextEdit::placeholderText` 用于计算、查询或取得与“placeholder、文本”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setAcceptRichText(bool accept)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setAcceptRichText`。调用它会改变 `QTextEdit` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `accept`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setAutoFormatting(QTextEdit::AutoFormatting features)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setAutoFormatting`。调用它会改变 `QTextEdit` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `features`：类型为 `QTextEdit::AutoFormatting`。没有默认值，调用时必须提供。传入 `QTextEdit::AutoFormatting` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setCursorWidth(int width)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setCursorWidth`。调用它会改变 `QTextEdit` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `width`：类型为 `int`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setDocument(QTextDocument *document)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setDocument`。调用它会改变 `QTextEdit` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `document`：类型为 `QTextDocument *`。没有默认值，调用时必须提供。传入 `QTextDocument *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setDocumentTitle(const QString &title)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setDocumentTitle`。调用它会改变 `QTextEdit` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `title`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setLineWrapColumnOrWidth(int w)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setLineWrapColumnOrWidth`。调用它会改变 `QTextEdit` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `w`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setLineWrapMode(QTextEdit::LineWrapMode mode)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setLineWrapMode`。调用它会改变 `QTextEdit` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `mode`：类型为 `QTextEdit::LineWrapMode`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setOverwriteMode(bool overwrite)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setOverwriteMode`。调用它会改变 `QTextEdit` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `overwrite`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setPlaceholderText(const QString &placeholderText)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setPlaceholderText`。调用它会改变 `QTextEdit` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `placeholderText`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setReadOnly(bool ro)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setReadOnly`。调用它会改变 `QTextEdit` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `ro`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setTabChangesFocus(bool b)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setTabChangesFocus`。调用它会改变 `QTextEdit` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `b`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setTabStopDistance(qreal distance)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setTabStopDistance`。调用它会改变 `QTextEdit` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `distance`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setTextInteractionFlags(Qt::TextInteractionFlags flags)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setTextInteractionFlags`。调用它会改变 `QTextEdit` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `flags`：类型为 `Qt::TextInteractionFlags`。没有默认值，调用时必须提供。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setUndoRedoEnabled(bool enable)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setUndoRedoEnabled`。调用它会改变 `QTextEdit` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enable`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setWordWrapMode(QTextOption::WrapMode policy)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setWordWrapMode`。调用它会改变 `QTextEdit` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `policy`：类型为 `QTextOption::WrapMode`。没有默认值，调用时必须提供。传入 `QTextOption::WrapMode` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool tabChangesFocus() const`

**API 类别：** 公有函数

**中文解读：** `QTextEdit::tabChangesFocus` 用于计算、查询或取得与“tab、Changes、Focus”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal tabStopDistance() const`

**API 类别：** 公有函数

**中文解读：** `QTextEdit::tabStopDistance` 用于计算、查询或取得与“tab、停止、Distance”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Qt::TextInteractionFlags textInteractionFlags() const`

**API 类别：** 公有函数

**中文解读：** `QTextEdit::textInteractionFlags` 用于计算、查询或取得与“文本、Interaction、标志”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `Qt::TextInteractionFlags`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::TextInteractionFlags`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString toHtml() const`

**API 类别：** 公有函数

**中文解读：** 这是转换/映射 API `toHtml`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString toMarkdown(QTextDocument::MarkdownFeatures features = QTextDocument::MarkdownDialectGitHub) const`

**API 类别：** 公有函数

**中文解读：** 这是转换/映射 API `toMarkdown`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QString`。
- 参数 `features`：类型为 `QTextDocument::MarkdownFeatures`。默认值为 `QTextDocument::MarkdownDialectGitHub`。传入 `QTextDocument::MarkdownFeatures` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextOption::WrapMode wordWrapMode() const`

**API 类别：** 公有函数

**中文解读：** `QTextEdit::wordWrapMode` 用于计算、查询或取得与“word、Wrap、模式”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QTextOption::WrapMode`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextOption::WrapMode`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setHtml(const QString &text)`

**API 类别：** 公有槽函数

**中文解读：** 这是可被信号连接或元对象调用的槽 `setHtml`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setMarkdown(const QString &markdown)`

**API 类别：** 公有槽函数

**中文解读：** 这是可被信号连接或元对象调用的槽 `setMarkdown`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `markdown`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

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
