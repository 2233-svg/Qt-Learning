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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 47 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `[since 6.5] enum QTextLayout::GlyphRunRetrievalFlagflags QTextLayout::GlyphRunRetrievalFlags`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QTextLayout` 暴露的类型声明 `Glyph、运行、Retrieval、Flagflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:GlyphRunRetrievalFlagflags QTextLayout::GlyphRunRetrievalFlags`。
- 属性名：`QTextLayout`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextLayout::QTextLayout()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextLayout` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextLayout::QTextLayout(const QString &text)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextLayout` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextLayout::QTextLayout(const QString &text, const QFont &font, const QPaintDevice *paintdevice = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextLayout` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。
- 参数 `font`：类型为 `const QFont &`。没有默认值，调用时必须提供。传入 `const QFont &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `paintdevice`：类型为 `const QPaintDevice *`。默认值为 `nullptr`。传入 `const QPaintDevice *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QTextLayout::~QTextLayout()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextLayout` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextLayout::beginLayout()`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `beginLayout`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRectF QTextLayout::boundingRect() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextLayout::boundingRect` 用于计算、查询或取得与“bounding、Rect”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRectF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRectF`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QTextLayout::cacheEnabled() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextLayout::cacheEnabled` 用于计算、查询或取得与“cache、启用状态”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextLayout::clearFormats()`

**API 类别：** 成员函数说明

**中文解读：** `QTextLayout::clearFormats` 用于执行与“清空、Formats”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextLayout::clearLayout()`

**API 类别：** 成员函数说明

**中文解读：** `QTextLayout::clearLayout` 用于执行与“清空、Layout”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextLine QTextLayout::createLine()`

**API 类别：** 成员函数说明

**中文解读：** `QTextLayout::createLine` 用于计算、查询或取得与“创建、行”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QTextLine`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextLine`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Qt::CursorMoveStyle QTextLayout::cursorMoveStyle() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextLayout::cursorMoveStyle` 用于计算、查询或取得与“cursor、移动、Style”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `Qt::CursorMoveStyle`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::CursorMoveStyle`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextLayout::draw(QPainter *p, const QPointF &pos, const QList<QTextLayout::FormatRange> &selections = QList<FormatRange>(), const QRectF &clip = QRectF()) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextLayout` 的核心操作 `draw`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `p`：类型为 `QPainter *`。没有默认值，调用时必须提供。传入 `QPainter *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pos`：类型为 `const QPointF &`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。
- 参数 `selections`：类型为 `const QList<QTextLayout::FormatRange> &`。默认值为 `QList<FormatRange>()`。传入 `const QList<QTextLayout::FormatRange> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `clip`：类型为 `const QRectF &`。默认值为 `QRectF()`。传入 `const QRectF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextLayout::drawCursor(QPainter *painter, const QPointF &position, int cursorPosition, int width) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextLayout` 的核心操作 `drawCursor`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `painter`：类型为 `QPainter *`。没有默认值，调用时必须提供。绘制上下文。要确认它已经绑定有效绘制设备，并处于允许绘制的阶段。
- 参数 `position`：类型为 `const QPointF &`。没有默认值，调用时必须提供。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。
- 参数 `cursorPosition`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `width`：类型为 `int`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextLayout::drawCursor(QPainter *painter, const QPointF &position, int cursorPosition) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextLayout` 的核心操作 `drawCursor`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `painter`：类型为 `QPainter *`。没有默认值，调用时必须提供。绘制上下文。要确认它已经绑定有效绘制设备，并处于允许绘制的阶段。
- 参数 `position`：类型为 `const QPointF &`。没有默认值，调用时必须提供。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。
- 参数 `cursorPosition`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextLayout::endLayout()`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `endLayout`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFont QTextLayout::font() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextLayout::font` 用于计算、查询或取得与“字体”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QFont`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QFont`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QTextLayout::FormatRange> QTextLayout::formats() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `formats`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QList<QTextLayout::FormatRange>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QGlyphRun> QTextLayout::glyphRuns(int from = -1, int length = -1) const`

**API 类别：** 成员函数说明

**中文解读：** `QTextLayout::glyphRuns` 用于计算、查询或取得与“glyph、Runs”相关的操作。调用时要先确认当前状态和 `from`、`length` 的有效范围；返回类型是 `QList<QGlyphRun>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QGlyphRun>`。
- 参数 `from`：类型为 `int`。默认值为 `-1`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `length`：类型为 `int`。默认值为 `-1`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.5] QList<QGlyphRun> QTextLayout::glyphRuns(int from, int length, QTextLayout::GlyphRunRetrievalFlags retrievalFlags) const`

**API 类别：** 成员函数说明

**中文解读：** `QTextLayout::glyphRuns` 用于计算、查询或取得与“glyph、Runs”相关的操作。调用时要先确认当前状态和 `from`、`length`、`retrievalFlags` 的有效范围；返回类型是 `QList<QGlyphRun>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QGlyphRun>`。
- 参数 `from`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `length`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `retrievalFlags`：类型为 `QTextLayout::GlyphRunRetrievalFlags`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QTextLayout::isValidCursorPosition(int pos) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isValidCursorPosition`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `pos`：类型为 `int`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QTextLayout::leftCursorPosition(int oldPos) const`

**API 类别：** 成员函数说明

**中文解读：** `QTextLayout::leftCursorPosition` 用于计算、查询或取得与“左侧、Cursor、Position”相关的操作。调用时要先确认当前状态和 `oldPos` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `oldPos`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextLine QTextLayout::lineAt(int i) const`

**API 类别：** 成员函数说明

**中文解读：** `QTextLayout::lineAt` 用于计算、查询或取得与“行、按位置访问”相关的操作。调用时要先确认当前状态和 `i` 的有效范围；返回类型是 `QTextLine`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextLine`。
- 参数 `i`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QTextLayout::lineCount() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextLayout::lineCount` 用于计算、查询或取得与“行、数量统计”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextLine QTextLayout::lineForTextPosition(int pos) const`

**API 类别：** 成员函数说明

**中文解读：** `QTextLayout::lineForTextPosition` 用于计算、查询或取得与“行、For、文本、Position”相关的操作。调用时要先确认当前状态和 `pos` 的有效范围；返回类型是 `QTextLine`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextLine`。
- 参数 `pos`：类型为 `int`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal QTextLayout::maximumWidth() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextLayout::maximumWidth` 用于计算、查询或取得与“最大值、宽度”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal QTextLayout::minimumWidth() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextLayout::minimumWidth` 用于计算、查询或取得与“最小值、宽度”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QTextLayout::nextCursorPosition(int oldPos, QTextLayout::CursorMode mode = SkipCharacters) const`

**API 类别：** 成员函数说明

**中文解读：** `QTextLayout::nextCursorPosition` 用于计算、查询或取得与“移动到下一项、Cursor、Position”相关的操作。调用时要先确认当前状态和 `oldPos`、`mode` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `oldPos`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `mode`：类型为 `QTextLayout::CursorMode`。默认值为 `SkipCharacters`。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPointF QTextLayout::position() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextLayout::position` 用于计算、查询或取得与“position”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPointF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPointF`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QTextLayout::preeditAreaPosition() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextLayout::preeditAreaPosition` 用于计算、查询或取得与“preedit、Area、Position”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QTextLayout::preeditAreaText() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextLayout::preeditAreaText` 用于计算、查询或取得与“preedit、Area、文本”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QTextLayout::previousCursorPosition(int oldPos, QTextLayout::CursorMode mode = SkipCharacters) const`

**API 类别：** 成员函数说明

**中文解读：** `QTextLayout::previousCursorPosition` 用于计算、查询或取得与“previous、Cursor、Position”相关的操作。调用时要先确认当前状态和 `oldPos`、`mode` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `oldPos`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `mode`：类型为 `QTextLayout::CursorMode`。默认值为 `SkipCharacters`。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QTextLayout::rightCursorPosition(int oldPos) const`

**API 类别：** 成员函数说明

**中文解读：** `QTextLayout::rightCursorPosition` 用于计算、查询或取得与“右侧、Cursor、Position”相关的操作。调用时要先确认当前状态和 `oldPos` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `oldPos`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextLayout::setCacheEnabled(bool enable)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setCacheEnabled`。调用它会改变 `QTextLayout` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enable`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextLayout::setCursorMoveStyle(Qt::CursorMoveStyle style)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setCursorMoveStyle`。调用它会改变 `QTextLayout` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `style`：类型为 `Qt::CursorMoveStyle`。没有默认值，调用时必须提供。传入 `Qt::CursorMoveStyle` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextLayout::setFont(const QFont &font)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFont`。调用它会改变 `QTextLayout` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `font`：类型为 `const QFont &`。没有默认值，调用时必须提供。传入 `const QFont &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextLayout::setFormats(const QList<QTextLayout::FormatRange> &formats)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFormats`。调用它会改变 `QTextLayout` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `formats`：类型为 `const QList<QTextLayout::FormatRange> &`。没有默认值，调用时必须提供。传入 `const QList<QTextLayout::FormatRange> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextLayout::setPosition(const QPointF &p)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPosition`。调用它会改变 `QTextLayout` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `p`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextLayout::setPreeditArea(int position, const QString &text)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPreeditArea`。调用它会改变 `QTextLayout` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `position`：类型为 `int`。没有默认值，调用时必须提供。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextLayout::setText(const QString &string)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setText`。调用它会改变 `QTextLayout` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `string`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextLayout::setTextOption(const QTextOption &option)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setTextOption`。调用它会改变 `QTextLayout` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `option`：类型为 `const QTextOption &`。没有默认值，调用时必须提供。选项或绘制/行为配置对象；调用前确认其中的状态、矩形和样式信息已经初始化。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QTextLayout::text() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextLayout::text` 用于计算、查询或取得与“文本”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QTextOption &QTextLayout::textOption() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextLayout::textOption` 用于计算、查询或取得与“文本、Option”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QTextOption &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QTextOption &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `struct FormatRange`

**API 类别：** 公有类型

**中文解读：** 这是 `QTextLayout` 的 `格式化、Range` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum CursorMode { SkipCharacters, SkipWords }`

**API 类别：** 公有类型

**中文解读：** 这是 `QTextLayout` 暴露的类型声明 `Cursor、模式`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.5) enum GlyphRunRetrievalFlag { RetrieveGlyphIndexes, RetrieveGlyphPositions, RetrieveStringIndexes, RetrieveString, RetrieveAll }`

**API 类别：** 公有类型

**中文解读：** 这是 `QTextLayout` 暴露的类型声明 `Glyph、运行、Retrieval、Flag`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags GlyphRunRetrievalFlags`

**API 类别：** 公有类型

**中文解读：** 这是 `QTextLayout` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

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

`QTextLayout` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
