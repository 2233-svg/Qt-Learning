# QTextDocument

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QTextDocument` 是 Qt 对象机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QTextDocument` 是 Qt 对象机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

**适用场景：** 使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

## 2. 依赖与对象关系

- 头文件：`#include <QTextDocument>`
- 继承自：QObject
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

### 状态、生命周期和线程

**生命周期：** 先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

**状态与结果：** QObject 派生对象的状态通常通过属性、状态查询函数和信号变化共同表达。信号是通知，不是返回值；收到通知后应读取当前状态并处理异常路径，不能假设每个信号只会出现一次。

**线程与事件循环：** QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

## 3. 直接使用

使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum FindFlag { FindBackward, FindCaseSensitively, FindWholeWords }`
- `flags FindFlags`
- `enum MarkdownFeature { MarkdownNoHTML, MarkdownDialectCommonMark, MarkdownDialectGitHub }`
- `flags MarkdownFeatures`
- `enum MetaInformation { DocumentTitle, DocumentUrl, CssMedia, FrontMatter }`
- `(since 6.1) ResourceProvider`
- `enum ResourceType { UnknownResource, HtmlResource, ImageResource, StyleSheetResource, MarkdownResource, UserResource }`
- `enum Stacks { UndoStack, RedoStack, UndoAndRedoStacks }`

### 属性

- `baseUrl : QUrl`
- `blockCount : int`
- `defaultFont : QFont`
- `defaultStyleSheet : QString`
- `defaultTextOption : QTextOption`
- `documentMargin : qreal`
- `indentWidth : qreal`
- `(since 6.4) layoutEnabled : bool`
- `maximumBlockCount : int`
- `modified : bool`
- `pageSize : QSizeF`
- `size : QSizeF`
- `textWidth : qreal`
- `undoRedoEnabled : bool`
- `useDesignMetrics : bool`

### 公有函数

- `QTextDocument(QObject *parent = nullptr)`
- `QTextDocument(const QString &text, QObject *parent = nullptr)`
- `virtual ~QTextDocument()`
- `void addResource(int type, const QUrl &name, const QVariant &resource)`
- `void adjustSize()`
- `QList<QTextFormat> allFormats() const`
- `int availableRedoSteps() const`
- `int availableUndoSteps() const`
- `QUrl baseUrl() const`
- `(since 6.0) qreal baselineOffset() const`
- `QTextBlock begin() const`
- `int blockCount() const`
- `QChar characterAt(int pos) const`
- `int characterCount() const`
- `virtual void clear()`
- `void clearUndoRedoStacks(QTextDocument::Stacks stacksToClear = UndoAndRedoStacks)`
- `QTextDocument * clone(QObject *parent = nullptr) const`
- `Qt::CursorMoveStyle defaultCursorMoveStyle() const`
- `QFont defaultFont() const`
- `QString defaultStyleSheet() const`
- `QTextOption defaultTextOption() const`
- `QAbstractTextDocumentLayout * documentLayout() const`
- `qreal documentMargin() const`
- `void drawContents(QPainter *p, const QRectF &rect = QRectF())`
- `QTextBlock end() const`
- `QTextCursor find(const QRegularExpression &expr, const QTextCursor &cursor, QTextDocument::FindFlags options = FindFlags()) const`
- `QTextCursor find(const QRegularExpression &expr, int from = 0, QTextDocument::FindFlags options = FindFlags()) const`
- `QTextCursor find(const QString &subString, const QTextCursor &cursor, QTextDocument::FindFlags options = FindFlags()) const`
- `QTextCursor find(const QString &subString, int position = 0, QTextDocument::FindFlags options = FindFlags()) const`
- `QTextBlock findBlock(int pos) const`
- `QTextBlock findBlockByLineNumber(int lineNumber) const`
- `QTextBlock findBlockByNumber(int blockNumber) const`
- `QTextBlock firstBlock() const`
- `qreal idealWidth() const`
- `qreal indentWidth() const`
- `bool isEmpty() const`
- `bool isLayoutEnabled() const`
- `bool isModified() const`
- `bool isRedoAvailable() const`
- `bool isUndoAvailable() const`
- `bool isUndoRedoEnabled() const`
- `QTextBlock lastBlock() const`
- `int lineCount() const`
- `void markContentsDirty(int position, int length)`
- `int maximumBlockCount() const`
- `QString metaInformation(QTextDocument::MetaInformation info) const`
- `QTextObject * object(int objectIndex) const`
- `QTextObject * objectForFormat(const QTextFormat &f) const`
- `int pageCount() const`
- `QSizeF pageSize() const`
- `void print(QPagedPaintDevice *printer) const`
- `void redo(QTextCursor *cursor)`
- `QVariant resource(int type, const QUrl &name) const`
- `(since 6.1) QTextDocument::ResourceProvider resourceProvider() const`
- `int revision() const`
- `QTextFrame * rootFrame() const`
- `void setBaseUrl(const QUrl &url)`
- `(since 6.0) void setBaselineOffset(qreal baseline)`
- `void setDefaultCursorMoveStyle(Qt::CursorMoveStyle style)`
- `void setDefaultFont(const QFont &font)`
- `void setDefaultStyleSheet(const QString &sheet)`
- `void setDefaultTextOption(const QTextOption &option)`
- `void setDocumentLayout(QAbstractTextDocumentLayout *layout)`
- `void setDocumentMargin(qreal margin)`
- `void setHtml(const QString &html)`
- `void setIndentWidth(qreal width)`
- `void setLayoutEnabled(bool b)`
- `void setMarkdown(const QString &markdown, QTextDocument::MarkdownFeatures features = MarkdownDialectGitHub)`
- `void setMaximumBlockCount(int maximum)`
- `void setMetaInformation(QTextDocument::MetaInformation info, const QString &string)`
- `void setPageSize(const QSizeF &size)`
- `void setPlainText(const QString &text)`
- `(since 6.1) void setResourceProvider(const QTextDocument::ResourceProvider &provider)`
- `(since 6.0) void setSubScriptBaseline(qreal baseline)`
- `(since 6.0) void setSuperScriptBaseline(qreal baseline)`
- `void setTextWidth(qreal width)`
- `void setUndoRedoEnabled(bool enable)`
- `void setUseDesignMetrics(bool b)`
- `QSizeF size() const`
- `(since 6.0) qreal subScriptBaseline() const`
- `(since 6.0) qreal superScriptBaseline() const`
- `qreal textWidth() const`
- `QString toHtml() const`
- `QString toMarkdown(QTextDocument::MarkdownFeatures features = MarkdownDialectGitHub) const`
- `QString toPlainText() const`
- `QString toRawText() const`
- `void undo(QTextCursor *cursor)`
- `bool useDesignMetrics() const`

### 公有槽函数

- `void redo()`
- `void setModified(bool m = true)`
- `void undo()`

### 信号

- `void baseUrlChanged(const QUrl &url)`
- `void blockCountChanged(int newBlockCount)`
- `void contentsChange(int position, int charsRemoved, int charsAdded)`
- `void contentsChanged()`
- `void cursorPositionChanged(const QTextCursor &cursor)`
- `void documentLayoutChanged()`
- `void modificationChanged(bool changed)`
- `void redoAvailable(bool available)`
- `void undoAvailable(bool available)`
- `void undoCommandAdded()`

### 静态公有成员

- `(since 6.1) QTextDocument::ResourceProvider defaultResourceProvider()`
- `(since 6.1) void setDefaultResourceProvider(const QTextDocument::ResourceProvider &provider)`

### 保护函数

- `virtual QTextObject * createObject(const QTextFormat &format)`
- `virtual QVariant loadResource(int type, const QUrl &name)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 131 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QTextDocument::FindFlagflags QTextDocument::FindFlags`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QTextDocument` 暴露的类型声明 `查找、Flagflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:FindFlagflags QTextDocument::FindFlags`。
- 属性名：`QTextDocument`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QTextDocument::MarkdownFeatureflags QTextDocument::MarkdownFeatures`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QTextDocument` 暴露的类型声明 `Markdown、Featureflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:MarkdownFeatureflags QTextDocument::MarkdownFeatures`。
- 属性名：`QTextDocument`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QTextDocument::MetaInformation`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QTextDocument` 暴露的类型声明 `Meta、Information`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:MetaInformation`。
- 属性名：`QTextDocument`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[alias, since 6.1] QTextDocument::ResourceProvider`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QTextDocument` 的配置属性。初始化或状态切换时通过 `setResourceProvider(...)` 设置，之后用 `ResourceProvider()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:ResourceProvider`。
- 属性名：`QTextDocument`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QTextDocument::ResourceType`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QTextDocument` 暴露的类型声明 `Resource、类型`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:ResourceType`。
- 属性名：`QTextDocument`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `baseUrl : QUrl`

**API 类别：** 属性说明

**中文解读：** 这是 `QTextDocument` 的配置属性。初始化或状态切换时通过 `setBaseUrl(...)` 设置，之后用 `baseUrl()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QUrl`。
- 属性名：`baseUrl`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] blockCount : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QTextDocument` 的状态/能力属性。通常通过 `blockCount()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`blockCount`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `defaultFont : QFont`

**API 类别：** 属性说明

**中文解读：** 这是 `QTextDocument` 的配置属性。初始化或状态切换时通过 `setDefaultFont(...)` 设置，之后用 `defaultFont()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QFont`。
- 属性名：`defaultFont`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `defaultStyleSheet : QString`

**API 类别：** 属性说明

**中文解读：** 这是 `QTextDocument` 的配置属性。初始化或状态切换时通过 `setDefaultStyleSheet(...)` 设置，之后用 `defaultStyleSheet()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QString`。
- 属性名：`defaultStyleSheet`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `defaultTextOption : QTextOption`

**API 类别：** 属性说明

**中文解读：** 这是 `QTextDocument` 的配置属性。初始化或状态切换时通过 `setDefaultTextOption(...)` 设置，之后用 `defaultTextOption()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QTextOption`。
- 属性名：`defaultTextOption`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `documentMargin : qreal`

**API 类别：** 属性说明

**中文解读：** 这是 `QTextDocument` 的配置属性。初始化或状态切换时通过 `setDocumentMargin(...)` 设置，之后用 `documentMargin()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`qreal`。
- 属性名：`documentMargin`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `indentWidth : qreal`

**API 类别：** 属性说明

**中文解读：** 这是 `QTextDocument` 的配置属性。初始化或状态切换时通过 `setIndentWidth(...)` 设置，之后用 `indentWidth()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`qreal`。
- 属性名：`indentWidth`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.4] layoutEnabled : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QTextDocument` 的配置属性。初始化或状态切换时通过 `setLayoutEnabled(...)` 设置，之后用 `layoutEnabled()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`layoutEnabled`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `maximumBlockCount : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QTextDocument` 的配置属性。初始化或状态切换时通过 `setMaximumBlockCount(...)` 设置，之后用 `maximumBlockCount()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`maximumBlockCount`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `modified : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QTextDocument` 的配置属性。初始化或状态切换时通过 `setModified(...)` 设置，之后用 `modified()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`modified`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `pageSize : QSizeF`

**API 类别：** 属性说明

**中文解读：** 这是 `QTextDocument` 的配置属性。初始化或状态切换时通过 `setPageSize(...)` 设置，之后用 `pageSize()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QSizeF`。
- 属性名：`pageSize`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] size : QSizeF`

**API 类别：** 属性说明

**中文解读：** 这是 `QTextDocument` 的状态/能力属性。通常通过 `size()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`QSizeF`。
- 属性名：`size`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `textWidth : qreal`

**API 类别：** 属性说明

**中文解读：** 这是 `QTextDocument` 的配置属性。初始化或状态切换时通过 `setTextWidth(...)` 设置，之后用 `textWidth()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`qreal`。
- 属性名：`textWidth`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `undoRedoEnabled : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QTextDocument` 的配置属性。初始化或状态切换时通过 `setUndoRedoEnabled(...)` 设置，之后用 `undoRedoEnabled()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`undoRedoEnabled`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `useDesignMetrics : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QTextDocument` 的配置属性。初始化或状态切换时通过 `setUseDesignMetrics(...)` 设置，之后用 `useDesignMetrics()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`useDesignMetrics`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QTextDocument::QTextDocument(QObject *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextDocument` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `parent`：类型为 `QObject *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QTextDocument::QTextDocument(const QString &text, QObject *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextDocument` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。
- 参数 `parent`：类型为 `QObject *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QTextDocument::~QTextDocument()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextDocument` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextDocument::addResource(int type, const QUrl &name, const QVariant &resource)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QTextDocument` 添加依赖、数据或子对象的 API `addResource`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `type`：类型为 `int`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。
- 参数 `name`：类型为 `const QUrl &`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。
- 参数 `resource`：类型为 `const QVariant &`。没有默认值，调用时必须提供。传入 `const QVariant &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextDocument::adjustSize()`

**API 类别：** 成员函数说明

**中文解读：** `QTextDocument::adjustSize` 用于执行与“adjust、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QTextFormat> QTextDocument::allFormats() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextDocument::allFormats` 用于计算、查询或取得与“all、Formats”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<QTextFormat>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QTextFormat>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QTextDocument::availableRedoSteps() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextDocument::availableRedoSteps` 用于计算、查询或取得与“可用量、重做、Steps”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QTextDocument::availableUndoSteps() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextDocument::availableUndoSteps` 用于计算、查询或取得与“可用量、撤销、Steps”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] qreal QTextDocument::baselineOffset() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextDocument::baselineOffset` 用于计算、查询或取得与“baseline、Offset”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextBlock QTextDocument::begin() const`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `begin`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QTextBlock`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QTextDocument::blockCountChanged(int newBlockCount)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextDocument` 发出的通知信号 `blockCountChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `newBlockCount`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QChar QTextDocument::characterAt(int pos) const`

**API 类别：** 成员函数说明

**中文解读：** `QTextDocument::characterAt` 用于计算、查询或取得与“character、按位置访问”相关的操作。调用时要先确认当前状态和 `pos` 的有效范围；返回类型是 `QChar`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QChar`。
- 参数 `pos`：类型为 `int`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QTextDocument::characterCount() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextDocument::characterCount` 用于计算、查询或取得与“character、数量统计”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] void QTextDocument::clear()`

**API 类别：** 成员函数说明

**中文解读：** 这是状态清理或重置 API `clear`。调用后原有数据、索引、缓存或绑定可能失效；使用前先确认它影响的是当前对象、子对象还是底层共享资源，之后重新检查状态。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextDocument::clearUndoRedoStacks(QTextDocument::Stacks stacksToClear = UndoAndRedoStacks)`

**API 类别：** 成员函数说明

**中文解读：** `QTextDocument::clearUndoRedoStacks` 用于执行与“清空、撤销、重做、Stacks”相关的操作。调用时要先确认当前状态和 `stacksToClear` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `stacksToClear`：类型为 `QTextDocument::Stacks`。默认值为 `UndoAndRedoStacks`。传入 `QTextDocument::Stacks` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextDocument *QTextDocument::clone(QObject *parent = nullptr) const`

**API 类别：** 成员函数说明

**中文解读：** `QTextDocument::clone` 用于计算、查询或取得与“clone”相关的操作。调用时要先确认当前状态和 `parent` 的有效范围；返回类型是 `QTextDocument *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextDocument *`。
- 参数 `parent`：类型为 `QObject *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QTextDocument::contentsChange(int position, int charsRemoved, int charsAdded)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextDocument` 发出的通知信号 `contentsChange`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `position`：类型为 `int`。没有默认值，调用时必须提供。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。
- 参数 `charsRemoved`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `charsAdded`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QTextDocument::contentsChanged()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextDocument` 发出的通知信号 `contentsChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] QTextObject *QTextDocument::createObject(const QTextFormat &format)`

**API 类别：** 成员函数说明

**中文解读：** `QTextDocument::createObject` 用于计算、查询或取得与“创建、Object”相关的操作。调用时要先确认当前状态和 `format` 的有效范围；返回类型是 `QTextObject *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextObject *`。
- 参数 `format`：类型为 `const QTextFormat &`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QTextDocument::cursorPositionChanged(const QTextCursor &cursor)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextDocument` 发出的通知信号 `cursorPositionChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `cursor`：类型为 `const QTextCursor &`。没有默认值，调用时必须提供。传入 `const QTextCursor &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Qt::CursorMoveStyle QTextDocument::defaultCursorMoveStyle() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextDocument::defaultCursorMoveStyle` 用于计算、查询或取得与“default、Cursor、移动、Style”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `Qt::CursorMoveStyle`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::CursorMoveStyle`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFont QTextDocument::defaultFont() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextDocument::defaultFont` 用于计算、查询或取得与“default、字体”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QFont`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QFont`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.1] QTextDocument::ResourceProvider QTextDocument::defaultResourceProvider()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `defaultResourceProvider`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QTextDocument::ResourceProvider`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextOption QTextDocument::defaultTextOption() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextDocument::defaultTextOption` 用于计算、查询或取得与“default、文本、Option”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QTextOption`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextOption`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QAbstractTextDocumentLayout *QTextDocument::documentLayout() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextDocument::documentLayout` 用于计算、查询或取得与“document、Layout”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QAbstractTextDocumentLayout *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAbstractTextDocumentLayout *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QTextDocument::documentLayoutChanged()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextDocument` 发出的通知信号 `documentLayoutChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextDocument::drawContents(QPainter *p, const QRectF &rect = QRectF())`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextDocument` 的核心操作 `drawContents`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `p`：类型为 `QPainter *`。没有默认值，调用时必须提供。传入 `QPainter *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `rect`：类型为 `const QRectF &`。默认值为 `QRectF()`。矩形区域；要确认坐标系、是否包含右下边界以及空矩形的语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextBlock QTextDocument::end() const`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `end`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`QTextBlock`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextCursor QTextDocument::find(const QRegularExpression &expr, const QTextCursor &cursor, QTextDocument::FindFlags options = FindFlags()) const`

**API 类别：** 成员函数说明

**中文解读：** `QTextDocument::find` 用于计算、查询或取得与“查找”相关的操作。调用时要先确认当前状态和 `expr`、`cursor`、`options` 的有效范围；返回类型是 `QTextCursor`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextCursor`。
- 参数 `expr`：类型为 `const QRegularExpression &`。没有默认值，调用时必须提供。传入 `const QRegularExpression &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cursor`：类型为 `const QTextCursor &`。没有默认值，调用时必须提供。传入 `const QTextCursor &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `options`：类型为 `QTextDocument::FindFlags`。默认值为 `FindFlags()`。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextCursor QTextDocument::find(const QRegularExpression &expr, int from = 0, QTextDocument::FindFlags options = FindFlags()) const`

**API 类别：** 成员函数说明

**中文解读：** `QTextDocument::find` 用于计算、查询或取得与“查找”相关的操作。调用时要先确认当前状态和 `expr`、`from`、`options` 的有效范围；返回类型是 `QTextCursor`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextCursor`。
- 参数 `expr`：类型为 `const QRegularExpression &`。没有默认值，调用时必须提供。传入 `const QRegularExpression &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `from`：类型为 `int`。默认值为 `0`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `options`：类型为 `QTextDocument::FindFlags`。默认值为 `FindFlags()`。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextCursor QTextDocument::find(const QString &subString, const QTextCursor &cursor, QTextDocument::FindFlags options = FindFlags()) const`

**API 类别：** 成员函数说明

**中文解读：** `QTextDocument::find` 用于计算、查询或取得与“查找”相关的操作。调用时要先确认当前状态和 `subString`、`cursor`、`options` 的有效范围；返回类型是 `QTextCursor`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextCursor`。
- 参数 `subString`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `cursor`：类型为 `const QTextCursor &`。没有默认值，调用时必须提供。传入 `const QTextCursor &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `options`：类型为 `QTextDocument::FindFlags`。默认值为 `FindFlags()`。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextCursor QTextDocument::find(const QString &subString, int position = 0, QTextDocument::FindFlags options = FindFlags()) const`

**API 类别：** 成员函数说明

**中文解读：** `QTextDocument::find` 用于计算、查询或取得与“查找”相关的操作。调用时要先确认当前状态和 `subString`、`position`、`options` 的有效范围；返回类型是 `QTextCursor`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextCursor`。
- 参数 `subString`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `position`：类型为 `int`。默认值为 `0`。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。
- 参数 `options`：类型为 `QTextDocument::FindFlags`。默认值为 `FindFlags()`。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextBlock QTextDocument::findBlock(int pos) const`

**API 类别：** 成员函数说明

**中文解读：** `QTextDocument::findBlock` 用于计算、查询或取得与“查找、阻塞或屏蔽”相关的操作。调用时要先确认当前状态和 `pos` 的有效范围；返回类型是 `QTextBlock`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextBlock`。
- 参数 `pos`：类型为 `int`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextBlock QTextDocument::findBlockByLineNumber(int lineNumber) const`

**API 类别：** 成员函数说明

**中文解读：** `QTextDocument::findBlockByLineNumber` 用于计算、查询或取得与“查找、阻塞或屏蔽、By、行、Number”相关的操作。调用时要先确认当前状态和 `lineNumber` 的有效范围；返回类型是 `QTextBlock`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextBlock`。
- 参数 `lineNumber`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextBlock QTextDocument::findBlockByNumber(int blockNumber) const`

**API 类别：** 成员函数说明

**中文解读：** `QTextDocument::findBlockByNumber` 用于计算、查询或取得与“查找、阻塞或屏蔽、By、Number”相关的操作。调用时要先确认当前状态和 `blockNumber` 的有效范围；返回类型是 `QTextBlock`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextBlock`。
- 参数 `blockNumber`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextBlock QTextDocument::firstBlock() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextDocument::firstBlock` 用于计算、查询或取得与“首项、阻塞或屏蔽”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QTextBlock`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextBlock`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal QTextDocument::idealWidth() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextDocument::idealWidth` 用于计算、查询或取得与“ideal、宽度”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QTextDocument::isEmpty() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isEmpty`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QTextDocument::isRedoAvailable() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isRedoAvailable`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QTextDocument::isUndoAvailable() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isUndoAvailable`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextBlock QTextDocument::lastBlock() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextDocument::lastBlock` 用于计算、查询或取得与“末项、阻塞或屏蔽”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QTextBlock`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextBlock`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QTextDocument::lineCount() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextDocument::lineCount` 用于计算、查询或取得与“行、数量统计”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected invokable] QVariant QTextDocument::loadResource(int type, const QUrl &name)`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `loadResource`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QVariant`。
- 参数 `type`：类型为 `int`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。
- 参数 `name`：类型为 `const QUrl &`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextDocument::markContentsDirty(int position, int length)`

**API 类别：** 成员函数说明

**中文解读：** `QTextDocument::markContentsDirty` 用于执行与“mark、Contents、Dirty”相关的操作。调用时要先确认当前状态和 `position`、`length` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `position`：类型为 `int`。没有默认值，调用时必须提供。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。
- 参数 `length`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QTextDocument::metaInformation(QTextDocument::MetaInformation info) const`

**API 类别：** 成员函数说明

**中文解读：** `QTextDocument::metaInformation` 用于计算、查询或取得与“meta、Information”相关的操作。调用时要先确认当前状态和 `info` 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数 `info`：类型为 `QTextDocument::MetaInformation`。没有默认值，调用时必须提供。传入 `QTextDocument::MetaInformation` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QTextDocument::modificationChanged(bool changed)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextDocument` 发出的通知信号 `modificationChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `changed`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextObject *QTextDocument::object(int objectIndex) const`

**API 类别：** 成员函数说明

**中文解读：** `QTextDocument::object` 用于计算、查询或取得与“object”相关的操作。调用时要先确认当前状态和 `objectIndex` 的有效范围；返回类型是 `QTextObject *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextObject *`。
- 参数 `objectIndex`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextObject *QTextDocument::objectForFormat(const QTextFormat &f) const`

**API 类别：** 成员函数说明

**中文解读：** `QTextDocument::objectForFormat` 用于计算、查询或取得与“object、For、格式化”相关的操作。调用时要先确认当前状态和 `f` 的有效范围；返回类型是 `QTextObject *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextObject *`。
- 参数 `f`：类型为 `const QTextFormat &`。没有默认值，调用时必须提供。传入 `const QTextFormat &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QTextDocument::pageCount() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextDocument::pageCount` 用于计算、查询或取得与“page、数量统计”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextDocument::print(QPagedPaintDevice *printer) const`

**API 类别：** 成员函数说明

**中文解读：** `QTextDocument::print` 用于执行与“print”相关的操作。调用时要先确认当前状态和 `printer` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `printer`：类型为 `QPagedPaintDevice *`。没有默认值，调用时必须提供。传入 `QPagedPaintDevice *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextDocument::redo(QTextCursor *cursor)`

**API 类别：** 成员函数说明

**中文解读：** `QTextDocument::redo` 用于执行与“重做”相关的操作。调用时要先确认当前状态和 `cursor` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `cursor`：类型为 `QTextCursor *`。没有默认值，调用时必须提供。传入 `QTextCursor *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QTextDocument::redo()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `redo`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QTextDocument::redoAvailable(bool available)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextDocument` 发出的通知信号 `redoAvailable`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `available`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVariant QTextDocument::resource(int type, const QUrl &name) const`

**API 类别：** 成员函数说明

**中文解读：** `QTextDocument::resource` 用于计算、查询或取得与“resource”相关的操作。调用时要先确认当前状态和 `type`、`name` 的有效范围；返回类型是 `QVariant`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVariant`。
- 参数 `type`：类型为 `int`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。
- 参数 `name`：类型为 `const QUrl &`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.1] QTextDocument::ResourceProvider QTextDocument::resourceProvider() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextDocument::resourceProvider` 用于计算、查询或取得与“resource、Provider”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QTextDocument::ResourceProvider`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextDocument::ResourceProvider`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QTextDocument::revision() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextDocument::revision` 用于计算、查询或取得与“revision”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextFrame *QTextDocument::rootFrame() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextDocument::rootFrame` 用于计算、查询或取得与“root、Frame”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QTextFrame *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextFrame *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] void QTextDocument::setBaselineOffset(qreal baseline)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setBaselineOffset`。调用它会改变 `QTextDocument` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `baseline`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextDocument::setDefaultCursorMoveStyle(Qt::CursorMoveStyle style)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setDefaultCursorMoveStyle`。调用它会改变 `QTextDocument` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `style`：类型为 `Qt::CursorMoveStyle`。没有默认值，调用时必须提供。传入 `Qt::CursorMoveStyle` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextDocument::setDefaultFont(const QFont &font)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setDefaultFont`。调用它会改变 `QTextDocument` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `font`：类型为 `const QFont &`。没有默认值，调用时必须提供。传入 `const QFont &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.1] void QTextDocument::setDefaultResourceProvider(const QTextDocument::ResourceProvider &provider)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `setDefaultResourceProvider`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `provider`：类型为 `const QTextDocument::ResourceProvider &`。没有默认值，调用时必须提供。传入 `const QTextDocument::ResourceProvider &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextDocument::setDefaultTextOption(const QTextOption &option)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setDefaultTextOption`。调用它会改变 `QTextDocument` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `option`：类型为 `const QTextOption &`。没有默认值，调用时必须提供。选项或绘制/行为配置对象；调用前确认其中的状态、矩形和样式信息已经初始化。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextDocument::setDocumentLayout(QAbstractTextDocumentLayout *layout)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setDocumentLayout`。调用它会改变 `QTextDocument` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `layout`：类型为 `QAbstractTextDocumentLayout *`。没有默认值，调用时必须提供。参与操作的布局对象。通常表示整个子布局的几何区域和所有权，不等于子布局里的某一个控件。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextDocument::setHtml(const QString &html)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setHtml`。调用它会改变 `QTextDocument` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `html`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextDocument::setIndentWidth(qreal width)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setIndentWidth`。调用它会改变 `QTextDocument` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `width`：类型为 `qreal`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextDocument::setMarkdown(const QString &markdown, QTextDocument::MarkdownFeatures features = MarkdownDialectGitHub)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setMarkdown`。调用它会改变 `QTextDocument` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `markdown`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `features`：类型为 `QTextDocument::MarkdownFeatures`。默认值为 `MarkdownDialectGitHub`。传入 `QTextDocument::MarkdownFeatures` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextDocument::setMetaInformation(QTextDocument::MetaInformation info, const QString &string)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setMetaInformation`。调用它会改变 `QTextDocument` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `info`：类型为 `QTextDocument::MetaInformation`。没有默认值，调用时必须提供。传入 `QTextDocument::MetaInformation` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `string`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextDocument::setPlainText(const QString &text)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPlainText`。调用它会改变 `QTextDocument` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.1] void QTextDocument::setResourceProvider(const QTextDocument::ResourceProvider &provider)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setResourceProvider`。调用它会改变 `QTextDocument` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `provider`：类型为 `const QTextDocument::ResourceProvider &`。没有默认值，调用时必须提供。传入 `const QTextDocument::ResourceProvider &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] void QTextDocument::setSubScriptBaseline(qreal baseline)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSubScriptBaseline`。调用它会改变 `QTextDocument` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `baseline`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] void QTextDocument::setSuperScriptBaseline(qreal baseline)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSuperScriptBaseline`。调用它会改变 `QTextDocument` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `baseline`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] qreal QTextDocument::subScriptBaseline() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextDocument::subScriptBaseline` 用于计算、查询或取得与“sub、Script、Baseline”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] qreal QTextDocument::superScriptBaseline() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextDocument::superScriptBaseline` 用于计算、查询或取得与“super、Script、Baseline”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QTextDocument::toHtml() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toHtml`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QTextDocument::toMarkdown(QTextDocument::MarkdownFeatures features = MarkdownDialectGitHub) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toMarkdown`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QString`。
- 参数 `features`：类型为 `QTextDocument::MarkdownFeatures`。默认值为 `MarkdownDialectGitHub`。传入 `QTextDocument::MarkdownFeatures` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QTextDocument::toPlainText() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toPlainText`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QTextDocument::toRawText() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toRawText`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextDocument::undo(QTextCursor *cursor)`

**API 类别：** 成员函数说明

**中文解读：** `QTextDocument::undo` 用于执行与“撤销”相关的操作。调用时要先确认当前状态和 `cursor` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `cursor`：类型为 `QTextCursor *`。没有默认值，调用时必须提供。传入 `QTextCursor *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QTextDocument::undo()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `undo`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QTextDocument::undoAvailable(bool available)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextDocument` 发出的通知信号 `undoAvailable`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `available`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QTextDocument::undoCommandAdded()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextDocument` 发出的通知信号 `undoCommandAdded`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum FindFlag { FindBackward, FindCaseSensitively, FindWholeWords }`

**API 类别：** 公有类型

**中文解读：** 这是 `QTextDocument` 暴露的类型声明 `查找、Flag`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags FindFlags`

**API 类别：** 公有类型

**中文解读：** 这是 `QTextDocument` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum MarkdownFeature { MarkdownNoHTML, MarkdownDialectCommonMark, MarkdownDialectGitHub }`

**API 类别：** 公有类型

**中文解读：** 这是 `QTextDocument` 暴露的类型声明 `Markdown、Feature`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags MarkdownFeatures`

**API 类别：** 公有类型

**中文解读：** 这是 `QTextDocument` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.1) ResourceProvider`

**API 类别：** 公有类型

**中文解读：** 这是 `QTextDocument` 的 `Resource、Provider` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum Stacks { UndoStack, RedoStack, UndoAndRedoStacks }`

**API 类别：** 公有类型

**中文解读：** 这是 `QTextDocument` 暴露的类型声明 `Stacks`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QUrl baseUrl() const`

**API 类别：** 公有函数

**中文解读：** `QTextDocument::baseUrl` 用于计算、查询或取得与“base、Url”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QUrl`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QUrl`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int blockCount() const`

**API 类别：** 公有函数

**中文解读：** `QTextDocument::blockCount` 用于计算、查询或取得与“阻塞或屏蔽、数量统计”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString defaultStyleSheet() const`

**API 类别：** 公有函数

**中文解读：** `QTextDocument::defaultStyleSheet` 用于计算、查询或取得与“default、Style、Sheet”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal documentMargin() const`

**API 类别：** 公有函数

**中文解读：** `QTextDocument::documentMargin` 用于计算、查询或取得与“document、Margin”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal indentWidth() const`

**API 类别：** 公有函数

**中文解读：** `QTextDocument::indentWidth` 用于计算、查询或取得与“indent、宽度”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool isLayoutEnabled() const`

**API 类别：** 公有函数

**中文解读：** 这是查询 API `isLayoutEnabled`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool isModified() const`

**API 类别：** 公有函数

**中文解读：** 这是查询 API `isModified`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

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

### `int maximumBlockCount() const`

**API 类别：** 公有函数

**中文解读：** `QTextDocument::maximumBlockCount` 用于计算、查询或取得与“最大值、阻塞或屏蔽、数量统计”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSizeF pageSize() const`

**API 类别：** 公有函数

**中文解读：** `QTextDocument::pageSize` 用于计算、查询或取得与“page、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSizeF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSizeF`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setBaseUrl(const QUrl &url)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setBaseUrl`。调用它会改变 `QTextDocument` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `url`：类型为 `const QUrl &`。没有默认值，调用时必须提供。资源地址。要确认 scheme、编码、相对路径、重定向和是否包含敏感信息。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setDefaultStyleSheet(const QString &sheet)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setDefaultStyleSheet`。调用它会改变 `QTextDocument` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `sheet`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setDocumentMargin(qreal margin)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setDocumentMargin`。调用它会改变 `QTextDocument` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `margin`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setLayoutEnabled(bool b)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setLayoutEnabled`。调用它会改变 `QTextDocument` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `b`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setMaximumBlockCount(int maximum)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setMaximumBlockCount`。调用它会改变 `QTextDocument` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `maximum`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setPageSize(const QSizeF &size)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setPageSize`。调用它会改变 `QTextDocument` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `size`：类型为 `const QSizeF &`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setTextWidth(qreal width)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setTextWidth`。调用它会改变 `QTextDocument` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `width`：类型为 `qreal`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setUndoRedoEnabled(bool enable)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setUndoRedoEnabled`。调用它会改变 `QTextDocument` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enable`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setUseDesignMetrics(bool b)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setUseDesignMetrics`。调用它会改变 `QTextDocument` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `b`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSizeF size() const`

**API 类别：** 公有函数

**中文解读：** 这是尺寸/数量查询 API `size`，返回 `QTextDocument` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`QSizeF`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal textWidth() const`

**API 类别：** 公有函数

**中文解读：** `QTextDocument::textWidth` 用于计算、查询或取得与“文本、宽度”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool useDesignMetrics() const`

**API 类别：** 公有函数

**中文解读：** `QTextDocument::useDesignMetrics` 用于计算、查询或取得与“use、Design、Metrics”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setModified(bool m = true)`

**API 类别：** 公有槽函数

**中文解读：** 这是可被信号连接或元对象调用的槽 `setModified`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `m`：类型为 `bool`。默认值为 `true`。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void baseUrlChanged(const QUrl &url)`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `baseUrlChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `url`：类型为 `const QUrl &`。没有默认值，调用时必须提供。资源地址。要确认 scheme、编码、相对路径、重定向和是否包含敏感信息。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

### 状态和错误边界

QObject 派生对象的状态通常通过属性、状态查询函数和信号变化共同表达。信号是通知，不是返回值；收到通知后应读取当前状态并处理异常路径，不能假设每个信号只会出现一次。

### 线程边界

QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

### 最容易出现的错误

不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QTextDocument` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
