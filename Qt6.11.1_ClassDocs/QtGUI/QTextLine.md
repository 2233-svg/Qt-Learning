# QTextLine

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QTextLine` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QTextLine>`
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

- `enum CursorPosition { CursorBetweenCharacters, CursorOnCharacter }`
- `enum Edge { Leading, Trailing }`

### 公有函数

- `QTextLine()`
- `qreal ascent() const`
- `qreal cursorToX(int *cursorPos, QTextLine::Edge edge = Leading) const`
- `qreal cursorToX(int cursorPos, QTextLine::Edge edge = Leading) const`
- `qreal descent() const`
- `void draw(QPainter *painter, const QPointF &position) const`
- `(since 6.5) QList<QGlyphRun> glyphRuns(int from, int length, QTextLayout::GlyphRunRetrievalFlags retrievalFlags) const`
- `QList<QGlyphRun> glyphRuns(int from = -1, int length = -1) const`
- `qreal height() const`
- `qreal horizontalAdvance() const`
- `bool isValid() const`
- `qreal leading() const`
- `bool leadingIncluded() const`
- `int lineNumber() const`
- `QRectF naturalTextRect() const`
- `qreal naturalTextWidth() const`
- `QPointF position() const`
- `QRectF rect() const`
- `void setLeadingIncluded(bool included)`
- `void setLineWidth(qreal width)`
- `void setNumColumns(int numColumns)`
- `void setNumColumns(int numColumns, qreal alignmentWidth)`
- `void setPosition(const QPointF &pos)`
- `int textLength() const`
- `int textStart() const`
- `qreal width() const`
- `qreal x() const`
- `int xToCursor(qreal x, QTextLine::CursorPosition cpos = CursorBetweenCharacters) const`
- `qreal y() const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QTextLine::QTextLine()`

**作用与语义：**

生成一条无效的行。

### `qreal QTextLine::ascent() const`

**作用与语义：**

返回线路的上升。

### `qreal QTextLine::cursorToX(int *cursorPos, QTextLine::Edge edge = Leading) const`

**作用与语义：**

将光标位置`cursorPos`转换为线内对应的x位置，考虑`edge`。
如果`cursorPos`不是有效的光标位置，则会使用最近的有效光标位置，并`cursorPos`修改为指向该有效光标位置。

### `qreal QTextLine::cursorToX(int cursorPos, QTextLine::Edge edge = Leading) const`

**作用与语义：**

将光标位置`cursorPos`转换为线内对应的x位置，考虑`edge`。
如果`cursorPos`不是有效的光标位置，则会使用最近的有效光标位置，并`cursorPos`修改为指向该有效光标位置。

### `qreal QTextLine::descent() const`

**作用与语义：**

返回线路下降。

### `void QTextLine::draw(QPainter *painter, const QPointF &position) const`

**作用与语义：**

在指定`position`处在给定`painter`上画一条线。

### `[since 6.5] QList<QGlyphRun> QTextLine::glyphRuns(int from, int length, QTextLayout::GlyphRunRetrievalFlags retrievalFlags) const`

**作用与语义：**

返回本`QTextLine`中所有字形的字形索引和位置，适用于由`from`和`length`定义的字符。`from`索引相对于包含`QTextLayout`文本开头，且该范围必须在`QTextLine`范围内，由函数`textStart()`和`textLength()`给出。
`retrievalFlags`指定将从布局中检索哪些`QGlyphRun`属性。为了最小化分配和内存消耗，应设置为只包含你之后需要访问的属性。
如果`from`为负，则默认为`textStart()`;如果`length`为负，则默认返回值为`textLength()`。

### `QList<QGlyphRun> QTextLine::glyphRuns(int from = -1, int length = -1) const`

**作用与语义：**

返回本`QTextLine`中所有字形的字形索引和位置，涵盖由`from`和`length`定义的范围内的字符。`from`索引相对于包含`QTextLayout`文本开头，且该范围必须在函数`textStart()`和`textLength()`给出的`QTextLine`范围内。
如果`from`为负，则默认为`textStart()`;如果`length`为负，则默认返回值为`textLength()`。
注意：这等同于调用 glyphRuns（from， length， QTextLayout：：GlyphRunRetrievalFlag：：GlyphIndexes |QTextLayout：：GlyphRunRetrievalFlag：：GlyphPositions）。

### `qreal QTextLine::height() const`

**作用与语义：**

返回行的高度。如果不包含前导，这等于`ascent()` `descent()`。如果包含前导，则等于`ascent()` `descent()` `leading()`。

### `qreal QTextLine::horizontalAdvance() const`

**作用与语义：**

返回文本的水平推进。文本的推进是指从其位置到自然绘制的下一个位置的距离。
通过将提前部分加到文本行的位置，并以此作为第二行文本行的位置，你可以将两行并排放置，中间没有空隙。

### `bool QTextLine::isValid() const`

**作用与语义：**

如果此文本行有效，则返回 `true`；否则返回 `false`。

### `qreal QTextLine::leading() const`

**作用与语义：**

返回线路的前导。

### `bool QTextLine::leadingIncluded() const`

**作用与语义：**

如果线高度包含正前导，返回`true`;否则返回`false`。
默认情况下，前导不包含在内。

### `int QTextLine::lineNumber() const`

**作用与语义：**

返回文本引擎中行的位置。

### `QRectF QTextLine::naturalTextRect() const`

**作用与语义：**

返回被该直线覆盖的矩形。

### `qreal QTextLine::naturalTextWidth() const`

**作用与语义：**

返回文本占据的行宽。这始终是<=对`width()`，是layout()在不改变换行位置的情况下可使用的最小宽度。

### `QPointF QTextLine::position() const`

**作用与语义：**

返回该行相对于文本布局的位置。

### `QRectF QTextLine::rect() const`

**作用与语义：**

返回线的边界矩形。

### `void QTextLine::setLeadingIncluded(bool included)`

**作用与语义：**

如果`included`为真，则包含正向向直线高度;否则不包含前导。
默认情况下，前导不包含在内。
注意负导引被忽略，必须在代码中通过让行重叠来处理。

### `void QTextLine::setLineWidth(qreal width)`

**作用与语义：**

用给定的 `width` 布局该行。从起始位置开始，用能放入行中的字符填充。如果文本无法在行末拆分，则会在下一个空白或文字末尾填充额外的字符。

### `void QTextLine::setNumColumns(int numColumns)`

**作用与语义：**

布局行。行从起始位置填充`numColumns`指定的字符数。如果文本无法分割至`numColumns`字符，则该行将被填充至下一个空白或文本末尾的字符数。

### `void QTextLine::setNumColumns(int numColumns, qreal alignmentWidth)`

**作用与语义：**

排版行。行从起始位置填充`numColumns`指定的字符。如果文本无法分割至`numColumns`字符，则该行将被填充到下一个空白或文字末尾的字符。提供的`alignmentWidth`作为对齐的参考宽度。

### `void QTextLine::setPosition(const QPointF &pos)`

**作用与语义：**

将线移至位置`pos`。

### `int QTextLine::textLength() const`

**作用与语义：**

返回该行文本的长度。

### `int QTextLine::textStart() const`

**作用与语义：**

返回从传递到`QTextLayout`的字符串起始点的行起点。

### `qreal QTextLine::width() const`

**作用与语义：**

返回由 layout() 函数指定的行宽。

### `qreal QTextLine::x() const`

**作用与语义：**

返回该行的 x 位置。

### `int QTextLine::xToCursor(qreal x, QTextLine::CursorPosition cpos = CursorBetweenCharacters) const`

**作用与语义：**

根据光标位置类型，将x坐标`x`转换为最接近的匹配光标位置，`cpos`。注意，结果光标位置包含可能的预编辑区域文本。

### `qreal QTextLine::y() const`

**作用与语义：**

返回线的 y 位置。

### `enum CursorPosition { CursorBetweenCharacters, CursorOnCharacter }`

**作用与语义：**

控制 `cursorToX()` 如何解释光标位置：`CursorBetweenCharacters` 把位置视为字符间隙，`CursorOnCharacter` 把位置视为字符本身。处理文本插入光标通常使用前者。

### `enum Edge { Leading, Trailing }`

**作用与语义：**

指定文本行的逻辑边缘：`Leading` 是按文字方向开始的一侧，`Trailing` 是结束的一侧。它不是固定的左/右；在从右到左文本中两者方向会相反。

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

`QTextLine` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
