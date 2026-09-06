# QTextLayout

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QTextLayout` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QTextLayout` 是 Qt Widgets 界面机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** Widgets 通过父子控件树、布局系统、事件分发和重绘请求组成界面。控件的可见区域、sizeHint、sizePolicy、字体和平台 style 共同影响最终几何；用户输入先进入 Qt 事件系统，再由控件的事件函数、信号或快捷键处理。

**适用场景：** 创建 QApplication 后创建控件，设置 parent 或把控件加入布局，连接用户操作信号，再显示顶层窗口。复合界面用布局嵌套；控件尺寸异常时同时检查 sizePolicy、minimum/maximum size、layout stretch、margins 和 spacing。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要用固定坐标拼接响应式界面；不要给已经加入布局的控件反复 `setGeometry()`；不要在 `paintEvent()` 中修改业务状态；不要忘记窗口关闭、对象销毁和应用退出是三个不同事件。

## 2. 依赖与对象关系

- 头文件：`#include <QTextLayout>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

Widgets 通过父子控件树、布局系统、事件分发和重绘请求组成界面。控件的可见区域、sizeHint、sizePolicy、字体和平台 style 共同影响最终几何；用户输入先进入 Qt 事件系统，再由控件的事件函数、信号或快捷键处理。

### 状态、生命周期和线程

**生命周期：** 控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

**状态与结果：** 控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

**线程与事件循环：** 所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

## 3. 直接使用

创建 QApplication 后创建控件，设置 parent 或把控件加入布局，连接用户操作信号，再显示顶层窗口。复合界面用布局嵌套；控件尺寸异常时同时检查 sizePolicy、minimum/maximum size、layout stretch、margins 和 spacing。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `struct FormatRange`
- `enum CursorMode { SkipCharacters, SkipWords }`
- `(since 6.5) enum GlyphRunRetrievalFlag { RetrieveGlyphIndexes, RetrieveGlyphPositions, RetrieveStringIndexes, RetrieveString, RetrieveAll }`
- `flags GlyphRunRetrievalFlags`

### 公有函数

- `QTextLayout()`
- `QTextLayout(const QString &text)`
- `QTextLayout(const QString &text, const QFont &font, const QPaintDevice *paintdevice = nullptr)`
- `~QTextLayout()`
- `void beginLayout()`
- `QRectF boundingRect() const`
- `bool cacheEnabled() const`
- `void clearFormats()`
- `void clearLayout()`
- `QTextLine createLine()`
- `Qt::CursorMoveStyle cursorMoveStyle() const`
- `void draw(QPainter *p, const QPointF &pos, const QList<QTextLayout::FormatRange> &selections = QList<FormatRange>(), const QRectF &clip = QRectF()) const`
- `void drawCursor(QPainter *painter, const QPointF &position, int cursorPosition, int width) const`
- `void drawCursor(QPainter *painter, const QPointF &position, int cursorPosition) const`
- `void endLayout()`
- `QFont font() const`
- `QList<QTextLayout::FormatRange> formats() const`
- `QList<QGlyphRun> glyphRuns(int from = -1, int length = -1) const`
- `(since 6.5) QList<QGlyphRun> glyphRuns(int from, int length, QTextLayout::GlyphRunRetrievalFlags retrievalFlags) const`
- `bool isValidCursorPosition(int pos) const`
- `int leftCursorPosition(int oldPos) const`
- `QTextLine lineAt(int i) const`
- `int lineCount() const`
- `QTextLine lineForTextPosition(int pos) const`
- `qreal maximumWidth() const`
- `qreal minimumWidth() const`
- `int nextCursorPosition(int oldPos, QTextLayout::CursorMode mode = SkipCharacters) const`
- `QPointF position() const`
- `int preeditAreaPosition() const`
- `QString preeditAreaText() const`
- `int previousCursorPosition(int oldPos, QTextLayout::CursorMode mode = SkipCharacters) const`
- `int rightCursorPosition(int oldPos) const`
- `void setCacheEnabled(bool enable)`
- `void setCursorMoveStyle(Qt::CursorMoveStyle style)`
- `void setFont(const QFont &font)`
- `void setFormats(const QList<QTextLayout::FormatRange> &formats)`
- `void setPosition(const QPointF &p)`
- `void setPreeditArea(int position, const QString &text)`
- `void setText(const QString &string)`
- `void setTextOption(const QTextOption &option)`
- `QString text() const`
- `const QTextOption & textOption() const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[since 6.5] enum QTextLayout::GlyphRunRetrievalFlagflags QTextLayout::GlyphRunRetrievalFlags`

**作用与语义：**

GlyphRunRetrievalFlag 指定了传递给 `glyphRuns()` 函数的标志，以决定哪些布局属性会被返回到`QGlyphRun`对象中。由于每个属性都会占用内存并可能需要额外分配，建议只请求你之后需要访问的属性。
- `QTextLayout::RetrieveGlyphIndexes`：`0x1`;检索字体中对应字形的索引。
- `QTextLayout::RetrieveGlyphPositions`：`0x2`;检索字形在布局中的相对位置。
- `QTextLayout::RetrieveStringIndexes`：`0x4`;检索原始字符串中对应每个字形的索引。
- `QTextLayout::RetrieveString`：`0x8`;从布局中检索原始源字符串。
- `QTextLayout::RetrieveAll`：`0xffff`;检索布局中所有可用的属性。
这个枚举是在Qt 6.5引入的。
GlyphRunRetrievalFlags 类型是 QFlags 的 typedef<GlyphRunRetrievalFlag>。它存储 GlyphRunRetrievalFlag 值的 OR 组合。

### `QTextLayout::QTextLayout()`

**作用与语义：**

构建一个空白的文本布局。

### `QTextLayout::QTextLayout(const QString &text)`

**作用与语义：**

构建文本布局以布局给定的`text`。

### `QTextLayout::QTextLayout(const QString &text, const QFont &font, const QPaintDevice *paintdevice = nullptr)`

**作用与语义：**

构建文本布局，以配置指定`font`的给定`text`。
所有的度量和布局计算都将基于绘画设备完成，`paintdevice`。如果`paintdevice` `nullptr`，计算将以屏幕指标进行。

### `[noexcept] QTextLayout::~QTextLayout()`

**作用与语义：**

破坏布局。

### `void QTextLayout::beginLayout()`

**作用与语义：**

开始布局流程。
警告：这将使布局失效，因此所有引用前述内容的现有`QTextLine`对象现在应被丢弃。

### `QRectF QTextLayout::boundingRect() const`

**作用与语义：**

包含布局中所有线条的最小矩形。

### `bool QTextLayout::cacheEnabled() const`

**作用与语义：**

如果缓存了完整的布局信息，返回`true`;否则返回`false`。

### `void QTextLayout::clearFormats()`

**作用与语义：**

清除文本布局支持的其他格式列表。

### `void QTextLayout::clearLayout()`

**作用与语义：**

清除布局中的行信息。调用该函数后，`lineCount()`返回0。
警告：这将使布局失效，因此所有涉及之前内容的现有`QTextLine`对象应被丢弃。

### `QTextLine QTextLayout::createLine()`

**作用与语义：**

如果有文本需要插入，则返回一行新的文本行以排版;否则返回无效的文本行。
文本布局创建一个新的行对象，从布局的最后一行开始，或者如果布局为空，则从起始点开始。布局维护一个内部光标，每行从光标位置开始填充文本，当调用`QTextLine::setLineWidth()`函数时。
一旦调用`QTextLine::setLineWidth()`，就可以创建新行并填充文本。重复此过程将布局出`QTextLayout`中包含的整个文本块。如果没有剩余文本可插入，返回的`QTextLine`将无效（isValid() 返回为 false）。

### `Qt::CursorMoveStyle QTextLayout::cursorMoveStyle() const`

**作用与语义：**

这个`QTextLayout`的光标移动风格。默认是`Qt::LogicalMoveStyle`。

### `void QTextLayout::draw(QPainter *p, const QPointF &pos, const QList<QTextLayout::FormatRange> &selections = QList<FormatRange>(), const QRectF &clip = QRectF()) const`

**作用与语义：**

在画家`p`绘制整个布局，位置由`pos`指定。渲染后的布局包含给定的`selections`，并在`clip`指定的矩形内裁剪。

### `void QTextLayout::drawCursor(QPainter *painter, const QPointF &position, int cursorPosition, int width) const`

**作用与语义：**

用当前笔和指定`width`在指定`position`上，使用指定的`painter`绘制文本光标。文本中对应的位置由`cursorPosition`指定。

### `void QTextLayout::drawCursor(QPainter *painter, const QPointF &position, int cursorPosition) const`

**作用与语义：**

用当前笔在给定`position`绘制文本光标，使用指定的`painter`。文本中对应的位置由`cursorPosition`指定。

### `void QTextLayout::endLayout()`

**作用与语义：**

布局流程就此结束。

### `QFont QTextLayout::font() const`

**作用与语义：**

返回当前用于布局的字体，或如果未设置，则返回默认字体。

### `QList<QTextLayout::FormatRange> QTextLayout::formats() const`

**作用与语义：**

返回文本布局支持的其他格式列表。

### `QList<QGlyphRun> QTextLayout::glyphRuns(int from = -1, int length = -1) const`

**作用与语义：**

返回所有对应于`length`字符的字形的字形索引和位置，这些符号从该`QTextLayout` `from`位置开始。这是一个昂贵的函数，不应在时间敏感的上下文中调用。
如果`from`小于零，则字形运行将从布局中的第一个字符开始。如果`length`小于零，则会从起始位置跨整个字符串。
注意：这等同于调用 glyphRuns（from， length， QTextLayout：：GlyphRunRetrievalFlag：：GlyphIndexes |QTextLayout：：GlyphRunRetrievalFlag：：GlyphPositions）。

### `[since 6.5] QList<QGlyphRun> QTextLayout::glyphRuns(int from, int length, QTextLayout::GlyphRunRetrievalFlags retrievalFlags) const`

**作用与语义：**

返回所有对应于`length`字符的字形索引和位置，这些字形从`QTextLayout`中`from`位置开始。这是一个昂贵的函数，不应在时间敏感的上下文中调用。
如果`from`小于零，则字形运行将从布局中的第一个字符开始。如果`length`小于零，则会从起始位置遍跨整个字符串。
`retrievalFlags`会指定将从布局中检索哪些`QGlyphRun`属性。为了最小化分配和内存消耗，应设置为只包含你之后需要访问的属性。

### `bool QTextLayout::isValidCursorPosition(int pos) const`

**作用与语义：**

如果位置`pos`是有效的光标位置，返回`true`。
在Unicode语境中，文本中的某些位置不是有效的光标位置，因为该位置位于Unicode代理或字素簇内。
字素簇是由两个或多个Unicode字符组成的序列，它们在屏幕上形成一个不可分割的实体。例如拉丁字母`Ä' can be represented in Unicode by two characters, `A'（0x41）和组合分位符（0x308）。文本光标只能有效地放置在这两个字符之前或之后，不能在它们之间，因为那样不合理。在印度语言中，每个音节都形成一个字素簇。

### `int QTextLayout::leftCursorPosition(int oldPos) const`

**作用与语义：**

返回`oldPos`左侧的光标位置，紧邻其侧。这取决于双向重排后字符的视觉位置。

### `QTextLine QTextLayout::lineAt(int i) const`

**作用与语义：**

返回该文本布局中的第`i`行文本。

### `int QTextLayout::lineCount() const`

**作用与语义：**

返回该文本布局中的行数。

### `QTextLine QTextLayout::lineForTextPosition(int pos) const`

**作用与语义：**

返回包含 `pos` 指定光标位置的行。

### `qreal QTextLayout::maximumWidth() const`

**作用与语义：**

布局可扩展的最大宽度;这基本上是整个文本的宽度。
警告：该函数仅在布局完成后返回有效值。

### `qreal QTextLayout::minimumWidth() const`

**作用与语义：**

布局所需的最小宽度。这是布局中最小且不可破坏子字符串的宽度。
警告：该函数仅在布局完成后返回有效值。

### `int QTextLayout::nextCursorPosition(int oldPos, QTextLayout::CursorMode mode = SkipCharacters) const`

**作用与语义：**

返回`oldPos`之后的下一个有效光标位置，且该位置符合给定的光标`mode`。返回`oldPos`，如果`oldPos`不是有效的光标位置。

### `QPointF QTextLayout::position() const`

**作用与语义：**

布局的全局位置。这与边界矩形和布局过程无关。

### `int QTextLayout::preeditAreaPosition() const`

**作用与语义：**

返回将在编辑前处理的文本布局中区域的位置。

### `QString QTextLayout::preeditAreaText() const`

**作用与语义：**

返回编辑前插入的文本。

### `int QTextLayout::previousCursorPosition(int oldPos, QTextLayout::CursorMode mode = SkipCharacters) const`

**作用与语义：**

返回`oldPos`之前第一个尊重给定光标`mode`的有效光标位置。返回`oldPos`值，如果`oldPos`不是有效的光标位置。

### `int QTextLayout::rightCursorPosition(int oldPos) const`

**作用与语义：**

返回光标位置在`oldPos`右侧，紧邻其侧。这取决于双向重排后字符的视觉位置。

### `void QTextLayout::setCacheEnabled(bool enable)`

**作用与语义：**

如果`enable`为真，则实现完整布局信息的缓存;否则禁用布局缓存。通常`QTextLayout`在调用`endLayout()`后丢弃大部分布局信息以减少内存消耗。但如果你想直接绘制排版文本，启用缓存可能会显著加快绘图速度。

### `void QTextLayout::setCursorMoveStyle(Qt::CursorMoveStyle style)`

**作用与语义：**

将视觉光标移动样式设置为给定的`style`。如果`QTextLayout`有文档支持，你可以忽略它，使用`QTextDocument`中的选项，这个选项适用于像`QLineEdit`或自定义小部件那样没有`QTextDocument`的自定义小部件。默认值是`Qt::LogicalMoveStyle`。

### `void QTextLayout::setFont(const QFont &font)`

**作用与语义：**

将布局的字体设置为给定的`font`。该布局失效，必须重新排版。

### `void QTextLayout::setFormats(const QList<QTextLayout::FormatRange> &formats)`

**作用与语义：**

将文本布局支持的额外格式设置为`formats`。格式在预编辑区域文本存在后应用。

### `void QTextLayout::setPosition(const QPointF &p)`

**作用与语义：**

将文本布局移动到点 `p`。

### `void QTextLayout::setPreeditArea(int position, const QString &text)`

**作用与语义：**

在编辑前设置该区域的布局`position`和`text`。布局失效，必须重新布局。

### `void QTextLayout::setText(const QString &string)`

**作用与语义：**

将布局文本设置为给定的`string`。布局失效，必须重新排版。
请注意，当将该`QTextLayout`作为`QTextDocument`的一部分使用时，这种方法不会有效果。

### `void QTextLayout::setTextOption(const QTextOption &option)`

**作用与语义：**

将控制布局过程的文本选项结构设置为给定的 `option`。

### `QString QTextLayout::text() const`

**作用与语义：**

返回版面文本。

### `const QTextOption &QTextLayout::textOption() const`

**作用与语义：**

返回当前用于控制布局过程的文本选项。

### `struct FormatRange`

**作用与语义：**

QTextLayout::FormatRange 结构用于在文本布局内容的指定区域应用额外的格式信息。

### `enum CursorMode { SkipCharacters, SkipWords }`

**作用与语义：**

控制光标移动的粒度：`SkipCharacters` 按字符位置移动，`SkipWords` 按单词边界移动。把它传给 `nextCursorPosition()` 或 `previousCursorPosition()`，Qt 会同时遵守双向文本和合法字形边界。

### `(since 6.5) enum GlyphRunRetrievalFlag { RetrieveGlyphIndexes, RetrieveGlyphPositions, RetrieveStringIndexes, RetrieveString, RetrieveAll }`

**作用与语义：**

GlyphRunRetrievalFlag 指定了传递给 `glyphRuns()` 函数的标志，以决定哪些布局属性会被返回到`QGlyphRun`对象中。由于每个属性都会占用内存并可能需要额外分配，建议只请求你之后需要访问的属性。
- `QTextLayout::RetrieveGlyphIndexes`：`0x1`;检索字体中对应字形的索引。
- `QTextLayout::RetrieveGlyphPositions`：`0x2`;检索字形在布局中的相对位置。
- `QTextLayout::RetrieveStringIndexes`：`0x4`;检索原始字符串中对应每个字形的索引。
- `QTextLayout::RetrieveString`：`0x8`;从布局中检索原始源字符串。
- `QTextLayout::RetrieveAll`：`0xffff`;检索布局中所有可用的属性。
这个枚举是在Qt 6.5引入的。
GlyphRunRetrievalFlags 类型是 QFlags 的 typedef<GlyphRunRetrievalFlag>。它存储 GlyphRunRetrievalFlag 值的 OR 组合。

### `flags GlyphRunRetrievalFlags`

**作用与语义：**

GlyphRunRetrievalFlag 指定了传递给 `glyphRuns()` 函数的标志，以决定哪些布局属性会被返回到`QGlyphRun`对象中。由于每个属性都会占用内存并可能需要额外分配，建议只请求你之后需要访问的属性。
- `QTextLayout::RetrieveGlyphIndexes`：`0x1`;检索字体中对应字形的索引。
- `QTextLayout::RetrieveGlyphPositions`：`0x2`;检索字形在布局中的相对位置。
- `QTextLayout::RetrieveStringIndexes`：`0x4`;检索原始字符串中对应每个字形的索引。
- `QTextLayout::RetrieveString`：`0x8`;从布局中检索原始源字符串。
- `QTextLayout::RetrieveAll`：`0xffff`;检索布局中所有可用的属性。
这个枚举是在Qt 6.5引入的。
GlyphRunRetrievalFlags 类型是 QFlags 的 typedef<GlyphRunRetrievalFlag>。它存储 GlyphRunRetrievalFlag 值的 OR 组合。

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

`QTextLayout` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
