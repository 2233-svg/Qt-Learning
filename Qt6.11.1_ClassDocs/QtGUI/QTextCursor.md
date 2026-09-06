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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 84 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QTextCursor::MoveMode`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QTextCursor` 暴露的类型声明 `移动、模式`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:MoveMode`。
- 属性名：`QTextCursor`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QTextCursor::MoveOperation`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QTextCursor` 暴露的类型声明 `移动、Operation`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:MoveOperation`。
- 属性名：`QTextCursor`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QTextCursor::SelectionType`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QTextCursor` 暴露的类型声明 `Selection、类型`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:SelectionType`。
- 属性名：`QTextCursor`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextCursor::QTextCursor()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextCursor` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QTextCursor::QTextCursor(QTextDocument *document)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextCursor` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `document`：类型为 `QTextDocument *`。没有默认值，调用时必须提供。传入 `QTextDocument *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QTextCursor::QTextCursor(QTextFrame *frame)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextCursor` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `frame`：类型为 `QTextFrame *`。没有默认值，调用时必须提供。传入 `QTextFrame *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QTextCursor::QTextCursor(const QTextBlock &block)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextCursor` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `block`：类型为 `const QTextBlock &`。没有默认值，调用时必须提供。传入 `const QTextBlock &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextCursor::QTextCursor(const QTextCursor &cursor)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextCursor` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `cursor`：类型为 `const QTextCursor &`。没有默认值，调用时必须提供。传入 `const QTextCursor &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QTextCursor::~QTextCursor()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextCursor` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QTextCursor::anchor() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCursor::anchor` 用于计算、查询或取得与“anchor”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QTextCursor::atBlockEnd() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCursor::atBlockEnd` 用于计算、查询或取得与“按位置访问、阻塞或屏蔽、结束”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QTextCursor::atBlockStart() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCursor::atBlockStart` 用于计算、查询或取得与“按位置访问、阻塞或屏蔽、启动”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QTextCursor::atEnd() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCursor::atEnd` 用于计算、查询或取得与“按位置访问、结束”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QTextCursor::atStart() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCursor::atStart` 用于计算、查询或取得与“按位置访问、启动”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCursor::beginEditBlock()`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `beginEditBlock`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextBlock QTextCursor::block() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCursor::block` 用于计算、查询或取得与“阻塞或屏蔽”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QTextBlock`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextBlock`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextCharFormat QTextCursor::blockCharFormat() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCursor::blockCharFormat` 用于计算、查询或取得与“阻塞或屏蔽、Char、格式化”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QTextCharFormat`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextCharFormat`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextBlockFormat QTextCursor::blockFormat() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCursor::blockFormat` 用于计算、查询或取得与“阻塞或屏蔽、格式化”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QTextBlockFormat`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextBlockFormat`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QTextCursor::blockNumber() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCursor::blockNumber` 用于计算、查询或取得与“阻塞或屏蔽、Number”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextCharFormat QTextCursor::charFormat() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCursor::charFormat` 用于计算、查询或取得与“char、格式化”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QTextCharFormat`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextCharFormat`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCursor::clearSelection()`

**API 类别：** 成员函数说明

**中文解读：** `QTextCursor::clearSelection` 用于执行与“清空、Selection”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QTextCursor::columnNumber() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCursor::columnNumber` 用于计算、查询或取得与“列、Number”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextList *QTextCursor::createList(const QTextListFormat &format)`

**API 类别：** 成员函数说明

**中文解读：** `QTextCursor::createList` 用于计算、查询或取得与“创建、List”相关的操作。调用时要先确认当前状态和 `format` 的有效范围；返回类型是 `QTextList *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextList *`。
- 参数 `format`：类型为 `const QTextListFormat &`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextList *QTextCursor::createList(QTextListFormat::Style style)`

**API 类别：** 成员函数说明

**中文解读：** `QTextCursor::createList` 用于计算、查询或取得与“创建、List”相关的操作。调用时要先确认当前状态和 `style` 的有效范围；返回类型是 `QTextList *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextList *`。
- 参数 `style`：类型为 `QTextListFormat::Style`。没有默认值，调用时必须提供。传入 `QTextListFormat::Style` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextFrame *QTextCursor::currentFrame() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCursor::currentFrame` 用于计算、查询或取得与“当前、Frame”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QTextFrame *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextFrame *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextList *QTextCursor::currentList() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCursor::currentList` 用于计算、查询或取得与“当前、List”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QTextList *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextList *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextTable *QTextCursor::currentTable() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCursor::currentTable` 用于计算、查询或取得与“当前、Table”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QTextTable *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextTable *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCursor::deleteChar()`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `deleteChar`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCursor::deletePreviousChar()`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `deletePreviousChar`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextDocument *QTextCursor::document() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCursor::document` 用于计算、查询或取得与“document”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QTextDocument *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextDocument *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCursor::endEditBlock()`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `endEditBlock`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QTextCursor::hasComplexSelection() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `hasComplexSelection`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QTextCursor::hasSelection() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `hasSelection`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCursor::insertBlock()`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QTextCursor` 添加依赖、数据或子对象的 API `insertBlock`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCursor::insertBlock(const QTextBlockFormat &format)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QTextCursor` 添加依赖、数据或子对象的 API `insertBlock`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `format`：类型为 `const QTextBlockFormat &`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCursor::insertBlock(const QTextBlockFormat &format, const QTextCharFormat &charFormat)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QTextCursor` 添加依赖、数据或子对象的 API `insertBlock`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `format`：类型为 `const QTextBlockFormat &`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `charFormat`：类型为 `const QTextCharFormat &`。没有默认值，调用时必须提供。传入 `const QTextCharFormat &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCursor::insertFragment(const QTextDocumentFragment &fragment)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QTextCursor` 添加依赖、数据或子对象的 API `insertFragment`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `fragment`：类型为 `const QTextDocumentFragment &`。没有默认值，调用时必须提供。传入 `const QTextDocumentFragment &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextFrame *QTextCursor::insertFrame(const QTextFrameFormat &format)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QTextCursor` 添加依赖、数据或子对象的 API `insertFrame`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QTextFrame *`。
- 参数 `format`：类型为 `const QTextFrameFormat &`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCursor::insertHtml(const QString &html)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QTextCursor` 添加依赖、数据或子对象的 API `insertHtml`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `html`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCursor::insertImage(const QTextImageFormat &format)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QTextCursor` 添加依赖、数据或子对象的 API `insertImage`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `format`：类型为 `const QTextImageFormat &`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCursor::insertImage(const QString &name)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QTextCursor` 添加依赖、数据或子对象的 API `insertImage`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `name`：类型为 `const QString &`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCursor::insertImage(const QImage &image, const QString &name = QString())`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QTextCursor` 添加依赖、数据或子对象的 API `insertImage`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `image`：类型为 `const QImage &`。没有默认值，调用时必须提供。传入 `const QImage &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `name`：类型为 `const QString &`。默认值为 `QString()`。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCursor::insertImage(const QTextImageFormat &format, QTextFrameFormat::Position alignment)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QTextCursor` 添加依赖、数据或子对象的 API `insertImage`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `format`：类型为 `const QTextImageFormat &`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `alignment`：类型为 `QTextFrameFormat::Position`。没有默认值，调用时必须提供。对齐标志的组合，例如 `Qt::AlignLeft | Qt::AlignVCenter`；它描述内容在已分配区域中的位置，不负责分配剩余空间。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextList *QTextCursor::insertList(const QTextListFormat &format)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QTextCursor` 添加依赖、数据或子对象的 API `insertList`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QTextList *`。
- 参数 `format`：类型为 `const QTextListFormat &`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextList *QTextCursor::insertList(QTextListFormat::Style style)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QTextCursor` 添加依赖、数据或子对象的 API `insertList`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QTextList *`。
- 参数 `style`：类型为 `QTextListFormat::Style`。没有默认值，调用时必须提供。传入 `QTextListFormat::Style` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.4] void QTextCursor::insertMarkdown(const QString &markdown, QTextDocument::MarkdownFeatures features = QTextDocument::MarkdownDialectGitHub)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QTextCursor` 添加依赖、数据或子对象的 API `insertMarkdown`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `markdown`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `features`：类型为 `QTextDocument::MarkdownFeatures`。默认值为 `QTextDocument::MarkdownDialectGitHub`。传入 `QTextDocument::MarkdownFeatures` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextTable *QTextCursor::insertTable(int rows, int columns, const QTextTableFormat &format)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QTextCursor` 添加依赖、数据或子对象的 API `insertTable`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QTextTable *`。
- 参数 `rows`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `columns`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `format`：类型为 `const QTextTableFormat &`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextTable *QTextCursor::insertTable(int rows, int columns)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QTextCursor` 添加依赖、数据或子对象的 API `insertTable`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QTextTable *`。
- 参数 `rows`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `columns`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCursor::insertText(const QString &text)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QTextCursor` 添加依赖、数据或子对象的 API `insertText`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCursor::insertText(const QString &text, const QTextCharFormat &format)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QTextCursor` 添加依赖、数据或子对象的 API `insertText`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。
- 参数 `format`：类型为 `const QTextCharFormat &`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QTextCursor::isCopyOf(const QTextCursor &other) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isCopyOf`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `other`：类型为 `const QTextCursor &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QTextCursor::isNull() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isNull`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCursor::joinPreviousEditBlock()`

**API 类别：** 成员函数说明

**中文解读：** `QTextCursor::joinPreviousEditBlock` 用于执行与“join、Previous、Edit、阻塞或屏蔽”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QTextCursor::keepPositionOnInsert() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCursor::keepPositionOnInsert` 用于计算、查询或取得与“keep、Position、On、插入”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCursor::mergeBlockCharFormat(const QTextCharFormat &modifier)`

**API 类别：** 成员函数说明

**中文解读：** `QTextCursor::mergeBlockCharFormat` 用于执行与“merge、阻塞或屏蔽、Char、格式化”相关的操作。调用时要先确认当前状态和 `modifier` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `modifier`：类型为 `const QTextCharFormat &`。没有默认值，调用时必须提供。传入 `const QTextCharFormat &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCursor::mergeBlockFormat(const QTextBlockFormat &modifier)`

**API 类别：** 成员函数说明

**中文解读：** `QTextCursor::mergeBlockFormat` 用于执行与“merge、阻塞或屏蔽、格式化”相关的操作。调用时要先确认当前状态和 `modifier` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `modifier`：类型为 `const QTextBlockFormat &`。没有默认值，调用时必须提供。传入 `const QTextBlockFormat &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCursor::mergeCharFormat(const QTextCharFormat &modifier)`

**API 类别：** 成员函数说明

**中文解读：** `QTextCursor::mergeCharFormat` 用于执行与“merge、Char、格式化”相关的操作。调用时要先确认当前状态和 `modifier` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `modifier`：类型为 `const QTextCharFormat &`。没有默认值，调用时必须提供。传入 `const QTextCharFormat &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QTextCursor::movePosition(QTextCursor::MoveOperation operation, QTextCursor::MoveMode mode = MoveAnchor, int n = 1)`

**API 类别：** 成员函数说明

**中文解读：** `QTextCursor::movePosition` 用于计算、查询或取得与“移动、Position”相关的操作。调用时要先确认当前状态和 `operation`、`mode`、`n` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `operation`：类型为 `QTextCursor::MoveOperation`。没有默认值，调用时必须提供。传入 `QTextCursor::MoveOperation` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `mode`：类型为 `QTextCursor::MoveMode`。默认值为 `MoveAnchor`。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。
- 参数 `n`：类型为 `int`。默认值为 `1`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QTextCursor::position() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCursor::position` 用于计算、查询或取得与“position”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QTextCursor::positionInBlock() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCursor::positionInBlock` 用于计算、查询或取得与“position、In、阻塞或屏蔽”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCursor::removeSelectedText()`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeSelectedText`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCursor::select(QTextCursor::SelectionType selection)`

**API 类别：** 成员函数说明

**中文解读：** `QTextCursor::select` 用于执行与“select”相关的操作。调用时要先确认当前状态和 `selection` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `selection`：类型为 `QTextCursor::SelectionType`。没有默认值，调用时必须提供。传入 `QTextCursor::SelectionType` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCursor::selectedTableCells(int *firstRow, int *numRows, int *firstColumn, int *numColumns) const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCursor::selectedTableCells` 用于执行与“selected、Table、Cells”相关的操作。调用时要先确认当前状态和 `firstRow`、`numRows`、`firstColumn`、`numColumns` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `firstRow`：类型为 `int *`。没有默认值，调用时必须提供。传入 `int *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `numRows`：类型为 `int *`。没有默认值，调用时必须提供。传入 `int *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `firstColumn`：类型为 `int *`。没有默认值，调用时必须提供。传入 `int *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `numColumns`：类型为 `int *`。没有默认值，调用时必须提供。传入 `int *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QTextCursor::selectedText() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCursor::selectedText` 用于计算、查询或取得与“selected、文本”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextDocumentFragment QTextCursor::selection() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCursor::selection` 用于计算、查询或取得与“selection”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QTextDocumentFragment`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextDocumentFragment`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QTextCursor::selectionEnd() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCursor::selectionEnd` 用于计算、查询或取得与“selection、结束”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QTextCursor::selectionStart() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCursor::selectionStart` 用于计算、查询或取得与“selection、启动”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCursor::setBlockCharFormat(const QTextCharFormat &format)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setBlockCharFormat`。调用它会改变 `QTextCursor` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `format`：类型为 `const QTextCharFormat &`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCursor::setBlockFormat(const QTextBlockFormat &format)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setBlockFormat`。调用它会改变 `QTextCursor` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `format`：类型为 `const QTextBlockFormat &`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCursor::setCharFormat(const QTextCharFormat &format)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setCharFormat`。调用它会改变 `QTextCursor` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `format`：类型为 `const QTextCharFormat &`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCursor::setKeepPositionOnInsert(bool b)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setKeepPositionOnInsert`。调用它会改变 `QTextCursor` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `b`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCursor::setPosition(int pos, QTextCursor::MoveMode m = MoveAnchor)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPosition`。调用它会改变 `QTextCursor` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `pos`：类型为 `int`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。
- 参数 `m`：类型为 `QTextCursor::MoveMode`。默认值为 `MoveAnchor`。传入 `QTextCursor::MoveMode` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCursor::setVerticalMovementX(int x)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setVerticalMovementX`。调用它会改变 `QTextCursor` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCursor::setVisualNavigation(bool b)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setVisualNavigation`。调用它会改变 `QTextCursor` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `b`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] void QTextCursor::swap(QTextCursor &other)`

**API 类别：** 成员函数说明

**中文解读：** `QTextCursor::swap` 用于执行与“swap”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `other`：类型为 `QTextCursor &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QTextCursor::verticalMovementX() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCursor::verticalMovementX` 用于计算、查询或取得与“垂直、Movement、X”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QTextCursor::visualNavigation() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCursor::visualNavigation` 用于计算、查询或取得与“visual、Navigation”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QTextCursor::operator!=(const QTextCursor &other) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextCursor` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `other`：类型为 `const QTextCursor &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QTextCursor::operator<(const QTextCursor &other) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextCursor` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `other`：类型为 `const QTextCursor &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QTextCursor::operator<=(const QTextCursor &other) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextCursor` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `other`：类型为 `const QTextCursor &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextCursor &QTextCursor::operator=(const QTextCursor &cursor)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextCursor` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QTextCursor &`。
- 参数 `cursor`：类型为 `const QTextCursor &`。没有默认值，调用时必须提供。传入 `const QTextCursor &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QTextCursor::operator==(const QTextCursor &other) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextCursor` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `other`：类型为 `const QTextCursor &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QTextCursor::operator>(const QTextCursor &other) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextCursor` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `other`：类型为 `const QTextCursor &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QTextCursor::operator>=(const QTextCursor &other) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextCursor` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `other`：类型为 `const QTextCursor &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

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
