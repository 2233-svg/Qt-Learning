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

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QTextDocument::FindFlagflags QTextDocument::FindFlags`

**作用与语义：**

本枚举描述了`QTextDocument`查找函数可用的选项。这些选项可以从以下列表中进行或运算合成：
- `QTextDocument::FindBackward`：`0x00001`;向后搜索而非向前搜索。
- `QTextDocument::FindCaseSensitively`：`0x00002`;默认情况下，查找不区分大小写。指定此选项后，行为将变为大小写区分查找操作。
- `QTextDocument::FindWholeWords`：`0x00004`;使得查找匹配词仅为完整词。
FindFlags 类型是 QFlags 的 typedef<FindFlag>。它存储 FindFlag 值的 OR 组合。

### `enum QTextDocument::MarkdownFeatureflags QTextDocument::MarkdownFeatures`

**作用与语义：**

该枚举在读取或写入 Markdown 时选择支持的功能集。
- `QTextDocument::MarkdownNoHTML`：`0x0020 | 0x0040`;Markdown 文本中的任何 HTML 标签将被丢弃
- `QTextDocument::MarkdownDialectCommonMark`：`0`;仅限CommonMark标准化的功能
- `QTextDocument::MarkdownDialectGitHub`：`0x0004 | 0x0008 | 0x0400 | 0x0100 | 0x0200 | 0x0800 | 0x4000 | 0x100000`;大部分功能来自GitHub方言
具体来说，支持的 GitHub 方言子集包括 CommonMark 的所有内容，以及：
- 识别URL、www和电子邮件地址并将其转化为链接
- 划线
- 下划线（与斜体不同;在CommonMark中相同）
- 表格
- 任务列表
- 前言
“前置信息”通常是 YAML 格式的元数据。Qt 目前没有包含用于此的解析器;但你可以选择第三方解析器，调用 `QTextDocument::metaInformation()` 获取整个区块，并在 Qt 解析 Markdown 文件后调用自己的解析器。
注意：目前`toMarkdown()`的 Markdown 输出可能包含 GitHub 功能，即使你通过指定其他枚举值来禁用它们。这可能会在未来的 Qt 版本中得到修复。
MarkdownFeatures 类型是 QFlag 的 typedef<MarkdownFeature>。它存储 MarkdownFeatures 值的 OR 组合。

### `enum QTextDocument::MetaInformation`

**作用与语义：**

该枚举描述了可以添加到文档的不同类型的元信息。
- `QTextDocument::DocumentTitle`：`0`;文件标题。
- `QTextDocument::DocumentUrl`：`1`;文档的网址。`loadResource()`函数在加载相对资源时以该网址为基础。
- `QTextDocument::CssMedia`：`2`;当调用`setHtml()`时，该值用于从指定的CSS样式表中选择对应的“@media”规则（如有）。该枚举值在Qt 6.3中引入。
- `QTextDocument::FrontMatter`：`3`;该值用于选择头部材料，如果在解析源文件时提取了任何内容（目前仅限Markdown格式）。该枚举值在Qt 6.8中引入。

### `[alias, since 6.1] QTextDocument::ResourceProvider`

**作用与语义：**

std：：function<`QVariant`（const `QUrl`&）> 的别名类型。
这种类型防御是在Qt 6.1中引入的。

### `enum QTextDocument::ResourceType`

**作用与语义：**

该枚举描述了可通过`QTextDocument` `loadResource()`函数或`QTextBrowser::setSource()`加载的资源类型。
- `QTextDocument::UnknownResource`：`0`;不加载资源，或资源类型未知。
- `QTextDocument::HtmlResource`：`1`;该资源包含 HTML。
- `QTextDocument::ImageResource`：`2`;资源包含图像数据。目前支持的数据类型为`QMetaType::QPixmap`和`QMetaType::QImage`。如果对应变体类型为`QMetaType::QByteArray`，Qt尝试使用`QImage::loadFromData`加载图像。`QMetaType::QIcon`目前不支持。图标需要先转换为支持的类型之一，例如使用`QIcon::pixmap`。
- `QTextDocument::StyleSheetResource`：`3`;该资源包含CSS。
- `QTextDocument::MarkdownResource`：`4`;该资源包含Markdown。
- `QTextDocument::UserResource`：`100`;用户定义资源类型的第一个可用值。

### `baseUrl : QUrl`

**作用与语义：**

该属性包含用于解析文档中相对资源 URL 的基础 URL。
资源URL被解析为与基础URL目标相同的目录，意味着路径中最后一个“/”之后的任何部分将被忽略。
- `Base URL`：相对 URL;已解析的 URL
- `file:///path/to/content`：图片/logo.png;file:///path/to/images/logo.png
- `file:///path/to/content/`：图片/logo.png;file:///path/to/content/images/logo.png
- `file:///path/to/content/index.html`：图片/logo.png;file:///path/to/content/images/logo.png
- `file:///path/to/content/images/`：../images/logo.png;file:///path/to/content/images/logo.png

**如何使用：** 调用 `baseUrl()` 读取当前值；它不会修改应用状态。

### `[read-only] blockCount : int`

**作用与语义：**

该属性包含文档中的文本块数量。
在带有表格或框架的文档中，该属性的价值未定义。
默认情况下，如果定义，该属性的值为1。

**如何使用：** 调用 `blockCount()` 读取当前值；它不会修改应用状态。

### `defaultFont : QFont`

**作用与语义：**

该属性保留用于显示文档文本的默认字体。

**如何使用：** 调用 `defaultFont()` 读取当前值；它不会修改应用状态。

### `defaultStyleSheet : QString`

**作用与语义：**

默认样式表应用于文档中插入的所有新 HTML 格式文本，例如使用 `setHtml()` 或 `QTextCursor::insertHtml()`。
样式表需要符合 CSS 2.1 语法。
注意：更改默认样式表不会对文档的现有内容产生任何影响。

**如何使用：** 调用 `defaultStyleSheet()` 读取当前值；它不会修改应用状态。

### `defaultTextOption : QTextOption`

**作用与语义：**

该属性表示默认文本选项将在文档中所有 `QTextLayout` 上设置。
当创建 `QTextBlock` 时，会在其 `QTextLayout` 上设置 defaultTextOption。这允许为文档设置全局属性，如默认的单词换行模式。

**如何使用：** 调用 `defaultTextOption()` 读取当前值；它不会修改应用状态。

### `documentMargin : qreal`

**作用与语义：**

文件周围的边距。默认是4。

**如何使用：** 调用 `documentMargin()` 读取当前值；它不会修改应用状态。

### `indentWidth : qreal`

**作用与语义：**

返回用于文本列表和文本块缩进的宽度。
`QTextListFormat` 和 `QTextBlockFormat` 的缩进属性指定了该值的倍数。默认缩进宽度为 40。

**如何使用：** 调用 `indentWidth()` 读取当前值；它不会修改应用状态。

### `[since 6.4] layoutEnabled : bool`

**作用与语义：**

该属性决定了每次变更后`QTextDocument`是否应重新计算布局。
如果该属性设置为 true，文档的任何更改都会触发布局，使一切正常运行，但需要时间。
临时禁用排版可以在进行多项修改（不仅是文本内容，还有默认字体、默认文本选项等）时节省时间，使文档在结尾只排版一次。例如，当文本宽度或页面大小尚未确定时，这非常有用。
默认情况下，该属性为`true`。

**如何使用：** 调用 `layoutEnabled()` 读取当前值；它不会修改应用状态。

### `maximumBlockCount : int`

**作用与语义：**

在文档中指定区块的限制。
指定文档可拥有的最大块数。如果文档中有更多带有该属性的块，则从文档开头移除块。
负值或零值表示文档可以包含无限数量的块。
默认值是0。
注意，设置此属性会立即将限制应用到文档内容上。
设置该属性还会禁用撤销重做历史。
在带有表格或框架的文档中，该属性未定义。

**如何使用：** 调用 `maximumBlockCount()` 读取当前值；它不会修改应用状态。

### `modified : bool`

**作用与语义：**

该属性决定文档是否被用户修改。
默认情况下，该属性为`false`。

**如何使用：** 调用 `modified()` 读取当前值；它不会修改应用状态。

### `pageSize : QSizeF`

**作用与语义：**

该属性包含用于排版的页面尺寸。
这些单位由底层的绘画设备决定。在绘制到屏幕上时，尺寸以逻辑像素为单位，在绘制到打印机时以点（1/72英寸）为单位。
默认情况下，对于新创建的空文档，该属性包含未定义的大小。

**如何使用：** 调用 `pageSize()` 读取当前值；它不会修改应用状态。

### `[read-only] size : QSizeF`

**作用与语义：**

该属性包含文档的实际大小。这相当于 `documentLayout()`->documentSize();
文档大小可以通过设置文本宽度或整页大小来更改。
注意宽度始终为 >= `pageSize()`。宽度()。
默认情况下，对于新创建的空文档，该属性包含一个配置相关的大小。

**如何使用：** 调用 `size()` 读取当前值；它不会修改应用状态。

### `textWidth : qreal`

**作用与语义：**

文本宽度指定文档中文本的首选宽度。如果文本（或内容本身）比指定宽度宽大，则被拆分成多行并垂直增长。如果文本无法分割成多行以符合指定宽度，则文本会变大，`size()`和`idealWidth()`属性会反映这一点。
如果文本宽度设置为 -1，则文本不会被拆分为多行，除非通过明确的换行或新段落强制执行。
默认值为-1。
设置文本宽度也会将页面高度设置为-1，导致文档连续地垂直增长或缩小。如果你想让文档布局将文本拆分成多个页面，就必须设置`pageSize`属性。

**如何使用：** 调用 `textWidth()` 读取当前值；它不会修改应用状态。

### `undoRedoEnabled : bool`

**作用与语义：**

该属性决定了本文档是否启用撤销/重做。
这默认为true。如果禁用，撤销堆栈会被清除，不会有任何物品被添加到中。

**如何使用：** 调用 `undoRedoEnabled()` 读取当前值；它不会修改应用状态。

### `useDesignMetrics : bool`

**作用与语义：**

该属性决定文档是否使用字体的设计指标来提升文本布局的准确性。
如果该属性设置为true，布局将使用设计度量。否则，将使用`QAbstractTextDocumentLayout::setPaintDevice()`上绘制设备的度量。
使用设计度量使布局的宽度不再依赖提示和像素四舍五入。这意味着所见即所得的文本布局成为可能，因为宽度基于绘图设备度量的线性扩展比平时更为线性。
默认情况下，该属性是`false`的。

**如何使用：** 调用 `useDesignMetrics()` 读取当前值；它不会修改应用状态。

### `[explicit] QTextDocument::QTextDocument(QObject *parent = nullptr)`

**作用与语义：**

构造一个包含给定`parent`的空 QTextDocument 。

### `[explicit] QTextDocument::QTextDocument(const QString &text, QObject *parent = nullptr)`

**作用与语义：**

构建包含指定普通（未格式化）`text`的QText文档，并带有给定的`parent`。

### `[virtual noexcept] QTextDocument::~QTextDocument()`

**作用与语义：**

销毁了文件。

### `void QTextDocument::addResource(int type, const QUrl &name, const QVariant &resource)`

**作用与语义：**

将资源`resource`添加到资源缓存中，使用`type`和`name`作为标识符。`type`应是`QTextDocument::ResourceType`的值。
例如，你可以添加一张图片作为资源，以便在文档中引用：
该图像可以通过 `QTextCursor` API 插入文档中：
或者，你也可以使用HTML `img`标签插入图片：

**官方示例：**

```cpp
     document->addResource(QTextDocument::ImageResource,
         QUrl("mydata://image.png"), QVariant(image));
```

### `void QTextDocument::adjustSize()`

**作用与语义：**

将文档调整到合理的大小。

### `QList<QTextFormat> QTextDocument::allFormats() const`

**作用与语义：**

返回文档中所有格式的文本格式列表。

### `int QTextDocument::availableRedoSteps() const`

**作用与语义：**

返回可用的重做步骤数量。

### `int QTextDocument::availableUndoSteps() const`

**作用与语义：**

返回可用的撤销步骤数。

### `[since 6.0] qreal QTextDocument::baselineOffset() const`

**作用与语义：**

返回文档布局中使用的基准偏移百分比。

### `QTextBlock QTextDocument::begin() const`

**作用与语义：**

返回文档的第一个文本块。

### `[signal] void QTextDocument::blockCountChanged(int newBlockCount)`

**作用与语义：**

当文档中文本块总数发生变化时，该信号会发出。`newBlockCount`传递的值即为新的总值。

### `QChar QTextDocument::characterAt(int pos) const`

**作用与语义：**

返回位置`pos`的字符，若位置超出范围则返回空字符。

### `int QTextDocument::characterCount() const`

**作用与语义：**

返回本文档的字符数。
注意：由于`QTextDocument`总是至少包含一个`QChar::ParagraphSeparator`，此方法至少返回1个。

### `[virtual] void QTextDocument::clear()`

**作用与语义：**

清除文档。

### `void QTextDocument::clearUndoRedoStacks(QTextDocument::Stacks stacksToClear = UndoAndRedoStacks)`

**作用与语义：**

清除`stacksToClear`指定的堆叠。
该方法清除撤销栈、重做栈或两者（默认）上的任何命令。如果命令被清除，会发出相应信号，`QTextDocument::undoAvailable()`或`QTextDocument::redoAvailable()`。

### `QTextDocument *QTextDocument::clone(QObject *parent = nullptr) const`

**作用与语义：**

创建一个新的`QTextDocument`，该是该文本文档的副本。`parent` 是返回文本文档的父文档。

### `[signal] void QTextDocument::contentsChange(int position, int charsRemoved, int charsAdded)`

**作用与语义：**

每当文档内容发生变化时，都会发出该信号;例如，当文本插入或删除，或格式调整时。
文件中会提供字符的`position`、删除字符数（`charsRemoved`）和新增字符数（`charsAdded`）的信息。
该信号在文档布局管理器收到变更通知之前就已发出。这个钩子允许你为文档实现语法高亮。

### `[signal] void QTextDocument::contentsChanged()`

**作用与语义：**

每当文档内容发生变化时，都会发出该信号;例如，当文本插入或删除，或格式调整时。

### `[virtual protected] QTextObject *QTextDocument::createObject(const QTextFormat &format)`

**作用与语义：**

创建并返回一个新的文档对象（`QTextObject`），基于给定的`format`。
QTextObjects 总是通过这种方法被创建，所以如果你在文档中使用自定义文本对象，必须重新实现它。

### `[signal] void QTextDocument::cursorPositionChanged(const QTextCursor &cursor)`

**作用与语义：**

每当光标位置因编辑操作而发生变化时，都会发出该信号。改变的光标会以`cursor`传递。如果文档与`QTextEdit`类一起使用，并且你需要在用方向键移动光标时获得信号，那么可以在`QTextEdit`中使用`cursorPositionChanged()`信号。

### `Qt::CursorMoveStyle QTextDocument::defaultCursorMoveStyle() const`

**作用与语义：**

默认光标移动风格被文档创建的所有对象`QTextCursor`使用。默认是`Qt::LogicalMoveStyle`。

### `QFont QTextDocument::defaultFont() const`

**作用与语义：**

返回文档布局中使用的默认字体。
注意：属性defaultFont的Getter函数。

### `[static, since 6.1] QTextDocument::ResourceProvider QTextDocument::defaultResourceProvider()`

**作用与语义：**

返回默认资源提供者。

### `QTextOption QTextDocument::defaultTextOption() const`

**作用与语义：**

文档中的所有 `QTextLayout` 对象都使用默认文本选项。这允许设置文档的全局属性，例如默认换行模式。
注意：获取属性 defaultTextOption 的 getter 函数。

### `QAbstractTextDocumentLayout *QTextDocument::documentLayout() const`

**作用与语义：**

返回本文档的文档布局。

### `[signal] void QTextDocument::documentLayoutChanged()`

**作用与语义：**

当设置新的文档布局时，会发出该信号。

### `void QTextDocument::drawContents(QPainter *p, const QRectF &rect = QRectF())`

**作用与语义：**

用画家`p`绘制文档内容，并裁剪到`rect`。如果`rect`是空矩形（默认），则文档绘制为未裁剪。

### `QTextBlock QTextDocument::end() const`

**作用与语义：**

该函数返回一个块，在迭代文档时测试文档结尾。
返回的块无效，代表文档中最后一个块之后的块。你可以用`lastBlock()`检索文档中最后一个有效块。

**官方示例：**

```cpp
 for (QTextBlock it = doc->begin(); it != doc->end(); it = it.next())
     std::cout << it.text().toStdString() << "\n";
```

### `QTextCursor QTextDocument::find(const QRegularExpression &expr, const QTextCursor &cursor, QTextDocument::FindFlags options = FindFlags()) const`

**作用与语义：**

找到文档中同一段落内与给定正则表达式`expr`匹配的下一个出现情况。
搜索从给定`cursor`的位置开始，除非搜索选项另有说明，否则会向前推进文档。`options`控制所执行的搜索类型。
如果找到匹配，返回带有匹配的光标;否则返回空光标。
如果给定`cursor`有选区，搜索在选区后开始;否则从光标位置开始。
默认情况下，搜索不区分大小写，可以匹配文档中任意文本。

### `QTextCursor QTextDocument::find(const QRegularExpression &expr, int from = 0, QTextDocument::FindFlags options = FindFlags()) const`

**作用与语义：**

在文档中同一段落内找到与给定正则表达式`expr`匹配的下一个出现。
搜索从给定的`from`位置开始，除非搜索选项另有说明，否则会向前推进文档。`options`控制所执行的搜索类型。
如果找到匹配，返回带有匹配的光标;否则返回空光标。
如果`from`位置为0（默认），搜索从文档开头开始;否则从指定位置开始。
警告：出于历史原因，`expr`设置的大小写敏感选项被忽略。取而代之的是，`options`用于判断搜索是否具有大小写敏感性。

### `QTextCursor QTextDocument::find(const QString &subString, const QTextCursor &cursor, QTextDocument::FindFlags options = FindFlags()) const`

**作用与语义：**

查找该字符串`subString`在文档中的下一次出现。搜索从给定`cursor`的位置开始，除非搜索选项另有说明，否则会在文档中向前推进。`options`控制所执行的搜索类型。
如果找到匹配，返回一个光标`subString`;否则返回空光标。
如果给定`cursor`有选择，搜索在选择后开始;否则从光标位置开始。
默认情况下，搜索不区分大小写，可以匹配文档中任意文本。

### `QTextCursor QTextDocument::find(const QString &subString, int position = 0, QTextDocument::FindFlags options = FindFlags()) const`

**作用与语义：**

查找该字符串在文档中出现的下一次`subString`。搜索从给定的`position`开始，除非搜索选项中另有说明，否则将向前推进文档。`options`控制所执行的搜索类型。
如果找到匹配，返回一个包含匹配`subString`光标;否则返回空光标。
如果`position`为0（默认值），搜索从文档开头开始;否则从指定位置开始。

### `QTextBlock QTextDocument::findBlock(int pos) const`

**作用与语义：**

返回包含第`pos`个字符的文本块。

### `QTextBlock QTextDocument::findBlockByLineNumber(int lineNumber) const`

**作用与语义：**

返回包含指定`lineNumber`的文本块。

### `QTextBlock QTextDocument::findBlockByNumber(int blockNumber) const`

**作用与语义：**

返回带有指定`blockNumber`的文本块。

### `QTextBlock QTextDocument::firstBlock() const`

**作用与语义：**

返回文档的第一个文本块。

### `qreal QTextDocument::idealWidth() const`

**作用与语义：**

返回文本文档的理想宽度。理想宽度是文档实际使用的宽度，未考虑可选的对齐。它总是 <= `size()`.width()。

### `bool QTextDocument::isEmpty() const`

**作用与语义：**

如果文档为空，返回`true`;否则返回`false`。

### `bool QTextDocument::isRedoAvailable() const`

**作用与语义：**

如果可以重做，返回`true`;否则返回`false`。

### `bool QTextDocument::isUndoAvailable() const`

**作用与语义：**

如果可以撤销，返回`true`;否则返回`false`。

### `QTextBlock QTextDocument::lastBlock() const`

**作用与语义：**

返回文档的最后（有效）文本块。

### `int QTextDocument::lineCount() const`

**作用与语义：**

返回本文档的行数（如果布局支持）。否则，这与块数相同。

### `[virtual protected invokable] QVariant QTextDocument::loadResource(int type, const QUrl &name)`

**作用与语义：**

从给定`name`的资源加载指定`type`的数据。
富文本引擎调用该函数，用于请求`QTextDocument`未直接存储但仍与其关联的数据。例如，图像通过`QTextImageFormat`对象的名称属性间接引用。
当Qt调用时，`type`是`QTextDocument::ResourceType`的值之一。
如果`QTextDocument`是`QObject`的子对象，且具有可调用的loadResource方法，如`QTextEdit`、`QTextBrowser`或`QTextDocument`本身，那么默认实现会尝试从父节点获取数据。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `void QTextDocument::markContentsDirty(int position, int length)`

**作用与语义：**

将指定`position`和`length`指定的内容标记为“脏”，告知文档需要重新排版。

### `QString QTextDocument::metaInformation(QTextDocument::MetaInformation info) const`

**作用与语义：**

返回`info`指定类型的文档元信息。

### `[signal] void QTextDocument::modificationChanged(bool changed)`

**作用与语义：**

每当文档内容发生变化，影响修改状态时，该信号就会发出。如果`changed`为真，则说明文档已被修改;否则为假。
例如，调用文档中的`setModified`（false）然后插入文本，信号就会被发出。如果你撤销该操作，使文档恢复到原始未修改状态，信号就会再次发出。

### `QTextObject *QTextDocument::object(int objectIndex) const`

**作用与语义：**

返回与给定`objectIndex`关联的文本对象。

### `QTextObject *QTextDocument::objectForFormat(const QTextFormat &f) const`

**作用与语义：**

返回与格式关联的文本对象`f`。

### `int QTextDocument::pageCount() const`

**作用与语义：**

返回本文档的页数。

### `void QTextDocument::print(QPagedPaintDevice *printer) const`

**作用与语义：**

将文档打印到指定`printer`。`QPagedPaintDevice`必须先设置好才能使用此功能。
这只是方便地将整份文档打印到打印机上的方法。
如果文档已经在`pageSize()`属性中按指定高度分页，则按原样打印。
如果文档没有分页，比如用于`QTextEdit`的文档，则会创建一份临时副本，并根据绘画设备的 paperRect() 大小将副本拆分成多个页面。默认情况下，文档内容周围会设置 2 厘米的页边距。此外，当前页码会印在每页底部。

### `void QTextDocument::redo(QTextCursor *cursor)`

**作用与语义：**

如果可以重做，可以重新做一次编辑操作。
提供的`cursor`位于重新进行版面操作地点的末端。

### `[slot] void QTextDocument::redo()`

**作用与语义：**

如果可以重做，可以重新做一次编辑操作。
注意：该槽位已超载。连接该槽位：


使用 qOverload 连接：
connect（sender， &SenderClass：：signal，。
textDocument， qOverload<>（&QTextDocument：：redo））;

或者用lambda作为包装器：
connect（sender， &SenderClass：：signal，。
textDocument， [接收器 = textDocument]() { receiver->redo(); }）;


更多示例和方法，请参见连接超载槽位。

### `[signal] void QTextDocument::redoAvailable(bool available)`

**作用与语义：**

每当重做操作可用（`available`为真）或不可用（`available`为假）时，该信号就会发出。

### `QVariant QTextDocument::resource(int type, const QUrl &name) const`

**作用与语义：**

返回指定`type`的数据，并由给定`name`返回资源。
富文本引擎调用该函数，以请求那些不直接由`QTextDocument`存储但仍与之关联的数据。例如，图像通过`QTextImageFormat`对象的名称属性间接引用。
资源缓存在文档内部。如果缓存中找不到资源，调用`loadResource`尝试加载该资源。`loadResource`应使用`addResource`将该资源添加到缓存中。
如果`loadResource`未加载资源，则调用`resourceProvider`，最后是`defaultResourceProvider`，前提是设置。注意，提供者的结果不会自动添加到缓存中。

### `[since 6.1] QTextDocument::ResourceProvider QTextDocument::resourceProvider() const`

**作用与语义：**

返回本文本文档的资源提供者。

### `int QTextDocument::revision() const`

**作用与语义：**

如果启用撤销，返回文档的版本。
当未被修改的文档被编辑时，修订量必定会增加。

### `QTextFrame *QTextDocument::rootFrame() const`

**作用与语义：**

返回文档的根框架。

### `[since 6.0] void QTextDocument::setBaselineOffset(qreal baseline)`

**作用与语义：**

将基准行设置为字体高度的百分比，用于文档布局`baseline`。默认值为0。正值会按相应比例向上移动;负值则向下移动。

### `void QTextDocument::setDefaultCursorMoveStyle(Qt::CursorMoveStyle style)`

**作用与语义：**

设置默认光标移动风格为给定的`style`。

### `void QTextDocument::setDefaultFont(const QFont &font)`

**作用与语义：**

该属性保留用于显示文档文本的默认字体。

**如何使用：** 调用 `setDefaultFont(...)` 修改 `defaultFont`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `[static, since 6.1] void QTextDocument::setDefaultResourceProvider(const QTextDocument::ResourceProvider &provider)`

**作用与语义：**

将默认资源提供者设置为`provider`。
所有没有明确设置提供者的 QTextDocuments 都会使用默认提供者。

### `void QTextDocument::setDefaultTextOption(const QTextOption &option)`

**作用与语义：**

该属性表示默认文本选项将在文档中所有 `QTextLayout` 上设置。
当创建 `QTextBlock` 时，会在其 `QTextLayout` 上设置 defaultTextOption。这允许为文档设置全局属性，如默认的单词换行模式。

**如何使用：** 调用 `setDefaultTextOption(...)` 修改 `defaultTextOption`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QTextDocument::setDocumentLayout(QAbstractTextDocumentLayout *layout)`

**作用与语义：**

设置文档使用给定的`layout`。之前的布局被删除。

### `void QTextDocument::setHtml(const QString &html)`

**作用与语义：**

用`html`字符串中指定的HTML格式文本替换文档的全部内容。调用该函数时，撤销/重做历史会被重置。
尽可能尊重HTML格式;例如，“<b>加粗</b>文本”会生成第一个单词带有粗体字重的文本，使其看起来加粗：“加粗文本”。
要选择除默认“屏幕”规则外的CSS媒体规则，使用`setMetaInformation()`，“`CssMedia`”作为“信息”参数。
注意：当创建包含HTML的`QString`并传递给setHtml()时，调用者有责任确保文本正确解码。

### `void QTextDocument::setIndentWidth(qreal width)`

**作用与语义：**

返回用于文本列表和文本块缩进的宽度。
`QTextListFormat` 和 `QTextBlockFormat` 的缩进属性指定了该值的倍数。默认缩进宽度为 40。

**如何使用：** 调用 `setIndentWidth(...)` 修改 `indentWidth`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QTextDocument::setMarkdown(const QString &markdown, QTextDocument::MarkdownFeatures features = MarkdownDialectGitHub)`

**作用与语义：**

用`markdown`字符串中给定的Markdown格式文本替换文档的全部内容，并支持相应`features`。默认情况下，包含所有支持的GitHub风格Markdown功能;通过 Pass `MarkdownDialectCommonMark` 进行更基础的解析。
尽可能尊重Markdown格式;例如，“加粗*文本”会生成第一个单词带有字体粗重的文本，使其看起来更突出。
`markdown`字符串中包含的HTML的解析方式与`setHtml`相同;但不支持HTML块内的Markdown格式化。
解析器的某些功能可以通过`features`参数启用或禁用。默认是`MarkdownDialectGitHub`。
当调用该函数时，撤销/重做历史会被重置。

### `void QTextDocument::setMetaInformation(QTextDocument::MetaInformation info, const QString &string)`

**作用与语义：**

将文档中由`info`指定类型的元信息设置为给定的`string`。

### `void QTextDocument::setPlainText(const QString &text)`

**作用与语义：**

用给定的明`text`替换文档的全部内容。调用该函数时，撤销/重做历史会被重置。

### `[since 6.1] void QTextDocument::setResourceProvider(const QTextDocument::ResourceProvider &provider)`

**作用与语义：**

将文本文档资源提供者设置为`provider`。

### `[since 6.0] void QTextDocument::setSubScriptBaseline(qreal baseline)`

**作用与语义：**

将默认下标的基准行设置为字体高度的百分比，用于文档布局`baseline`。默认值为16.67%（高度的1/6）。

### `[since 6.0] void QTextDocument::setSuperScriptBaseline(qreal baseline)`

**作用与语义：**

将默认上标的基准行设置为字体高度的百分比，用于文档布局`baseline`。默认值为50%（高度的一半）。

### `[since 6.0] qreal QTextDocument::subScriptBaseline() const`

**作用与语义：**

返回上标的基行，表示文档布局中使用的字体高度百分比。

### `[since 6.0] qreal QTextDocument::superScriptBaseline() const`

**作用与语义：**

返回上标的基行，表示文档布局中使用的字体高度百分比。

### `QString QTextDocument::toHtml() const`

**作用与语义：**

返回包含文档HTML表示的字符串。
文档内容指定其编码为 UTF-8。如果你以后将返回的 HTML 字符串转换为字节数组以便通过网络传输或保存到磁盘时，应使用 `QString::toUtf8()` 将字符串转换为 `QByteArray`。

### `QString QTextDocument::toMarkdown(QTextDocument::MarkdownFeatures features = MarkdownDialectGitHub) const`

**作用与语义：**

返回包含文档Markdown表示的字符串，包含给定`features`，或如果写入失败则返回空字符串。

### `QString QTextDocument::toPlainText() const`

**作用与语义：**

返回文档中的纯文本。如果你需要格式信息，可以用`QTextCursor`。
该函数返回与`toRawText()`相同，但会用ASCII替代部分Unicode字符。特别是，无间断空格（U 00A0）被普通空格（U 0020）取代，段落分隔符（U 2029）和行分隔符（U 2028）被换行符（U 000A）取代。如果你需要文档的精确内容，可以用`toRawText()`。
注意：嵌入对象，如图像，由Unicode值U FFFC（对象替换字符）表示。

### `QString QTextDocument::toRawText() const`

**作用与语义：**

返回文档中的原始文本，但没有任何格式信息。如果你需要格式信息，可以用`QTextCursor`。

### `void QTextDocument::undo(QTextCursor *cursor)`

**作用与语义：**

如果有撤销功能，则撤销文档上最后一次编辑操作。提供的`cursor`位于编辑操作撤销位置的末尾。
详情请参见 Qt Undo 框架文档。

### `[slot] void QTextDocument::undo()`

**作用与语义：**

注意：该槽位已超载。连接该槽位：


使用 qOverload 连接：
connect（sender， &SenderClass：：signal，。
textDocument， qOverload<>（&QTextDocument：：undo））;

或者用lambda作为包装器：
connect（sender， &SenderClass：：signal，。
textDocument， [接收器 = textDocument]() { receiver->undo(); }）;


更多示例和方法，请参见连接超载槽位。

### `[signal] void QTextDocument::undoAvailable(bool available)`

**作用与语义：**

每当撤销操作可用（`available`为真）或不可用（`available`为假）时，该信号就会发出。
详情请参见 Qt Undo 框架文档。

### `[signal] void QTextDocument::undoCommandAdded()`

**作用与语义：**

每当`QTextDocument`中新增一个撤销级别时，都会发出该信号。

### `enum FindFlag { FindBackward, FindCaseSensitively, FindWholeWords }`

**作用与语义：**

本枚举描述了`QTextDocument`查找函数可用的选项。这些选项可以从以下列表中进行或运算合成：
- `QTextDocument::FindBackward`：`0x00001`;向后搜索而非向前搜索。
- `QTextDocument::FindCaseSensitively`：`0x00002`;默认情况下，查找不区分大小写。指定此选项后，行为将变为大小写区分查找操作。
- `QTextDocument::FindWholeWords`：`0x00004`;使得查找匹配词仅为完整词。
FindFlags 类型是 QFlags 的 typedef<FindFlag>。它存储 FindFlag 值的 OR 组合。

### `flags FindFlags`

**作用与语义：**

本枚举描述了`QTextDocument`查找函数可用的选项。这些选项可以从以下列表中进行或运算合成：
- `QTextDocument::FindBackward`：`0x00001`;向后搜索而非向前搜索。
- `QTextDocument::FindCaseSensitively`：`0x00002`;默认情况下，查找不区分大小写。指定此选项后，行为将变为大小写区分查找操作。
- `QTextDocument::FindWholeWords`：`0x00004`;使得查找匹配词仅为完整词。
FindFlags 类型是 QFlags 的 typedef<FindFlag>。它存储 FindFlag 值的 OR 组合。

### `enum MarkdownFeature { MarkdownNoHTML, MarkdownDialectCommonMark, MarkdownDialectGitHub }`

**作用与语义：**

该枚举在读取或写入 Markdown 时选择支持的功能集。
- `QTextDocument::MarkdownNoHTML`：`0x0020 | 0x0040`;Markdown 文本中的任何 HTML 标签将被丢弃
- `QTextDocument::MarkdownDialectCommonMark`：`0`;仅限CommonMark标准化的功能
- `QTextDocument::MarkdownDialectGitHub`：`0x0004 | 0x0008 | 0x0400 | 0x0100 | 0x0200 | 0x0800 | 0x4000 | 0x100000`;大部分功能来自GitHub方言
具体来说，支持的 GitHub 方言子集包括 CommonMark 的所有内容，以及：
- 识别URL、www和电子邮件地址并将其转化为链接
- 划线
- 下划线（与斜体不同;在CommonMark中相同）
- 表格
- 任务列表
- 前言
“前置信息”通常是 YAML 格式的元数据。Qt 目前没有包含用于此的解析器;但你可以选择第三方解析器，调用 `QTextDocument::metaInformation()` 获取整个区块，并在 Qt 解析 Markdown 文件后调用自己的解析器。
注意：目前`toMarkdown()`的 Markdown 输出可能包含 GitHub 功能，即使你通过指定其他枚举值来禁用它们。这可能会在未来的 Qt 版本中得到修复。
MarkdownFeatures 类型是 QFlag 的 typedef<MarkdownFeature>。它存储 MarkdownFeatures 值的 OR 组合。

### `flags MarkdownFeatures`

**作用与语义：**

该枚举在读取或写入 Markdown 时选择支持的功能集。
- `QTextDocument::MarkdownNoHTML`：`0x0020 | 0x0040`;Markdown 文本中的任何 HTML 标签将被丢弃
- `QTextDocument::MarkdownDialectCommonMark`：`0`;仅限CommonMark标准化的功能
- `QTextDocument::MarkdownDialectGitHub`：`0x0004 | 0x0008 | 0x0400 | 0x0100 | 0x0200 | 0x0800 | 0x4000 | 0x100000`;大部分功能来自GitHub方言
具体来说，支持的 GitHub 方言子集包括 CommonMark 的所有内容，以及：
- 识别URL、www和电子邮件地址并将其转化为链接
- 划线
- 下划线（与斜体不同;在CommonMark中相同）
- 表格
- 任务列表
- 前言
“前置信息”通常是 YAML 格式的元数据。Qt 目前没有包含用于此的解析器;但你可以选择第三方解析器，调用 `QTextDocument::metaInformation()` 获取整个区块，并在 Qt 解析 Markdown 文件后调用自己的解析器。
注意：目前`toMarkdown()`的 Markdown 输出可能包含 GitHub 功能，即使你通过指定其他枚举值来禁用它们。这可能会在未来的 Qt 版本中得到修复。
MarkdownFeatures 类型是 QFlag 的 typedef<MarkdownFeature>。它存储 MarkdownFeatures 值的 OR 组合。

### `(since 6.1) ResourceProvider`

**作用与语义：**

std：：function<`QVariant`（const `QUrl`&）> 的别名类型。
这种类型防御是在Qt 6.1中引入的。

### `enum Stacks { UndoStack, RedoStack, UndoAndRedoStacks }`

**作用与语义：**

- `QTextDocument::UndoStack`：`0x01`;撤销堆栈。
- `QTextDocument::RedoStack`：`0x02`;重做堆栈。
- `QTextDocument::UndoAndRedoStacks`：`UndoStack | RedoStack`;撤销和重做堆栈。

### `QUrl baseUrl() const`

**作用与语义：**

该属性包含用于解析文档中相对资源 URL 的基础 URL。
资源URL被解析为与基础URL目标相同的目录，意味着路径中最后一个“/”之后的任何部分将被忽略。
- `Base URL`：相对 URL;已解析的 URL
- `file:///path/to/content`：图片/logo.png;file:///path/to/images/logo.png
- `file:///path/to/content/`：图片/logo.png;file:///path/to/content/images/logo.png
- `file:///path/to/content/index.html`：图片/logo.png;file:///path/to/content/images/logo.png
- `file:///path/to/content/images/`：../images/logo.png;file:///path/to/content/images/logo.png

**如何使用：** 调用 `baseUrl()` 读取当前值；它不会修改应用状态。

### `int blockCount() const`

**作用与语义：**

该属性包含文档中的文本块数量。
在带有表格或框架的文档中，该属性的价值未定义。
默认情况下，如果定义，该属性的值为1。

**如何使用：** 调用 `blockCount()` 读取当前值；它不会修改应用状态。

### `QString defaultStyleSheet() const`

**作用与语义：**

默认样式表应用于文档中插入的所有新 HTML 格式文本，例如使用 `setHtml()` 或 `QTextCursor::insertHtml()`。
样式表需要符合 CSS 2.1 语法。
注意：更改默认样式表不会对文档的现有内容产生任何影响。

**如何使用：** 调用 `defaultStyleSheet()` 读取当前值；它不会修改应用状态。

### `qreal documentMargin() const`

**作用与语义：**

文件周围的边距。默认是4。

**如何使用：** 调用 `documentMargin()` 读取当前值；它不会修改应用状态。

### `qreal indentWidth() const`

**作用与语义：**

返回用于文本列表和文本块缩进的宽度。
`QTextListFormat` 和 `QTextBlockFormat` 的缩进属性指定了该值的倍数。默认缩进宽度为 40。

**如何使用：** 调用 `indentWidth()` 读取当前值；它不会修改应用状态。

### `bool isLayoutEnabled() const`

**作用与语义：**

该属性决定了每次变更后`QTextDocument`是否应重新计算布局。
如果该属性设置为 true，文档的任何更改都会触发布局，使一切正常运行，但需要时间。
临时禁用排版可以在进行多项修改（不仅是文本内容，还有默认字体、默认文本选项等）时节省时间，使文档在结尾只排版一次。例如，当文本宽度或页面大小尚未确定时，这非常有用。
默认情况下，该属性为`true`。

**如何使用：** 调用 `isLayoutEnabled()` 读取当前值；它不会修改应用状态。

### `bool isModified() const`

**作用与语义：**

该属性决定文档是否被用户修改。
默认情况下，该属性为`false`。

**如何使用：** 调用 `isModified()` 读取当前值；它不会修改应用状态。

### `bool isUndoRedoEnabled() const`

**作用与语义：**

该属性决定了本文档是否启用撤销/重做。
这默认为true。如果禁用，撤销堆栈会被清除，不会有任何物品被添加到中。

**如何使用：** 调用 `isUndoRedoEnabled()` 读取当前值；它不会修改应用状态。

### `int maximumBlockCount() const`

**作用与语义：**

在文档中指定区块的限制。
指定文档可拥有的最大块数。如果文档中有更多带有该属性的块，则从文档开头移除块。
负值或零值表示文档可以包含无限数量的块。
默认值是0。
注意，设置此属性会立即将限制应用到文档内容上。
设置该属性还会禁用撤销重做历史。
在带有表格或框架的文档中，该属性未定义。

**如何使用：** 调用 `maximumBlockCount()` 读取当前值；它不会修改应用状态。

### `QSizeF pageSize() const`

**作用与语义：**

该属性包含用于排版的页面尺寸。
这些单位由底层的绘画设备决定。在绘制到屏幕上时，尺寸以逻辑像素为单位，在绘制到打印机时以点（1/72英寸）为单位。
默认情况下，对于新创建的空文档，该属性包含未定义的大小。

**如何使用：** 调用 `pageSize()` 读取当前值；它不会修改应用状态。

### `void setBaseUrl(const QUrl &url)`

**作用与语义：**

该属性包含用于解析文档中相对资源 URL 的基础 URL。
资源URL被解析为与基础URL目标相同的目录，意味着路径中最后一个“/”之后的任何部分将被忽略。
- `Base URL`：相对 URL;已解析的 URL
- `file:///path/to/content`：图片/logo.png;file:///path/to/images/logo.png
- `file:///path/to/content/`：图片/logo.png;file:///path/to/content/images/logo.png
- `file:///path/to/content/index.html`：图片/logo.png;file:///path/to/content/images/logo.png
- `file:///path/to/content/images/`：../images/logo.png;file:///path/to/content/images/logo.png

**如何使用：** 调用 `setBaseUrl(...)` 修改 `baseUrl`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setDefaultStyleSheet(const QString &sheet)`

**作用与语义：**

默认样式表应用于文档中插入的所有新 HTML 格式文本，例如使用 `setHtml()` 或 `QTextCursor::insertHtml()`。
样式表需要符合 CSS 2.1 语法。
注意：更改默认样式表不会对文档的现有内容产生任何影响。

**如何使用：** 调用 `setDefaultStyleSheet(...)` 修改 `defaultStyleSheet`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setDocumentMargin(qreal margin)`

**作用与语义：**

文件周围的边距。默认是4。

**如何使用：** 调用 `setDocumentMargin(...)` 修改 `documentMargin`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setLayoutEnabled(bool b)`

**作用与语义：**

该属性决定了每次变更后`QTextDocument`是否应重新计算布局。
如果该属性设置为 true，文档的任何更改都会触发布局，使一切正常运行，但需要时间。
临时禁用排版可以在进行多项修改（不仅是文本内容，还有默认字体、默认文本选项等）时节省时间，使文档在结尾只排版一次。例如，当文本宽度或页面大小尚未确定时，这非常有用。
默认情况下，该属性为`true`。

**如何使用：** 调用 `setLayoutEnabled(...)` 修改 `layoutEnabled`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMaximumBlockCount(int maximum)`

**作用与语义：**

在文档中指定区块的限制。
指定文档可拥有的最大块数。如果文档中有更多带有该属性的块，则从文档开头移除块。
负值或零值表示文档可以包含无限数量的块。
默认值是0。
注意，设置此属性会立即将限制应用到文档内容上。
设置该属性还会禁用撤销重做历史。
在带有表格或框架的文档中，该属性未定义。

**如何使用：** 调用 `setMaximumBlockCount(...)` 修改 `maximumBlockCount`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setPageSize(const QSizeF &size)`

**作用与语义：**

该属性包含用于排版的页面尺寸。
这些单位由底层的绘画设备决定。在绘制到屏幕上时，尺寸以逻辑像素为单位，在绘制到打印机时以点（1/72英寸）为单位。
默认情况下，对于新创建的空文档，该属性包含未定义的大小。

**如何使用：** 调用 `setPageSize(...)` 修改 `pageSize`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTextWidth(qreal width)`

**作用与语义：**

文本宽度指定文档中文本的首选宽度。如果文本（或内容本身）比指定宽度宽大，则被拆分成多行并垂直增长。如果文本无法分割成多行以符合指定宽度，则文本会变大，`size()`和`idealWidth()`属性会反映这一点。
如果文本宽度设置为 -1，则文本不会被拆分为多行，除非通过明确的换行或新段落强制执行。
默认值为-1。
设置文本宽度也会将页面高度设置为-1，导致文档连续地垂直增长或缩小。如果你想让文档布局将文本拆分成多个页面，就必须设置`pageSize`属性。

**如何使用：** 调用 `setTextWidth(...)` 修改 `textWidth`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setUndoRedoEnabled(bool enable)`

**作用与语义：**

该属性决定了本文档是否启用撤销/重做。
这默认为true。如果禁用，撤销堆栈会被清除，不会有任何物品被添加到中。

**如何使用：** 调用 `setUndoRedoEnabled(...)` 修改 `undoRedoEnabled`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setUseDesignMetrics(bool b)`

**作用与语义：**

该属性决定文档是否使用字体的设计指标来提升文本布局的准确性。
如果该属性设置为true，布局将使用设计度量。否则，将使用`QAbstractTextDocumentLayout::setPaintDevice()`上绘制设备的度量。
使用设计度量使布局的宽度不再依赖提示和像素四舍五入。这意味着所见即所得的文本布局成为可能，因为宽度基于绘图设备度量的线性扩展比平时更为线性。
默认情况下，该属性是`false`的。

**如何使用：** 调用 `setUseDesignMetrics(...)` 修改 `useDesignMetrics`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QSizeF size() const`

**作用与语义：**

该属性包含文档的实际大小。这相当于 `documentLayout()`->documentSize();
文档大小可以通过设置文本宽度或整页大小来更改。
注意宽度始终为 >= `pageSize()`。宽度()。
默认情况下，对于新创建的空文档，该属性包含一个配置相关的大小。

**如何使用：** 调用 `size()` 读取当前值；它不会修改应用状态。

### `qreal textWidth() const`

**作用与语义：**

文本宽度指定文档中文本的首选宽度。如果文本（或内容本身）比指定宽度宽大，则被拆分成多行并垂直增长。如果文本无法分割成多行以符合指定宽度，则文本会变大，`size()`和`idealWidth()`属性会反映这一点。
如果文本宽度设置为 -1，则文本不会被拆分为多行，除非通过明确的换行或新段落强制执行。
默认值为-1。
设置文本宽度也会将页面高度设置为-1，导致文档连续地垂直增长或缩小。如果你想让文档布局将文本拆分成多个页面，就必须设置`pageSize`属性。

**如何使用：** 调用 `textWidth()` 读取当前值；它不会修改应用状态。

### `bool useDesignMetrics() const`

**作用与语义：**

该属性决定文档是否使用字体的设计指标来提升文本布局的准确性。
如果该属性设置为true，布局将使用设计度量。否则，将使用`QAbstractTextDocumentLayout::setPaintDevice()`上绘制设备的度量。
使用设计度量使布局的宽度不再依赖提示和像素四舍五入。这意味着所见即所得的文本布局成为可能，因为宽度基于绘图设备度量的线性扩展比平时更为线性。
默认情况下，该属性是`false`的。

**如何使用：** 调用 `useDesignMetrics()` 读取当前值；它不会修改应用状态。

### `void setModified(bool m = true)`

**作用与语义：**

该属性决定文档是否被用户修改。
默认情况下，该属性为`false`。

**如何使用：** 调用 `setModified(...)` 修改 `modified`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void baseUrlChanged(const QUrl &url)`

**作用与语义：**

该属性包含用于解析文档中相对资源 URL 的基础 URL。
资源URL被解析为与基础URL目标相同的目录，意味着路径中最后一个“/”之后的任何部分将被忽略。
- `Base URL`：相对 URL;已解析的 URL
- `file:///path/to/content`：图片/logo.png;file:///path/to/images/logo.png
- `file:///path/to/content/`：图片/logo.png;file:///path/to/content/images/logo.png
- `file:///path/to/content/index.html`：图片/logo.png;file:///path/to/content/images/logo.png
- `file:///path/to/content/images/`：../images/logo.png;file:///path/to/content/images/logo.png

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `baseUrl` 的变化，不要把它当作普通函数主动调用。

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
