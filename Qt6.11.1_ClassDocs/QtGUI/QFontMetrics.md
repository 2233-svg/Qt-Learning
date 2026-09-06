# QFontMetrics

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 字体度量工具，负责计算文字宽度、高度、基线和换行所需空间。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QFontMetrics`：字体度量工具，负责计算文字宽度、高度、基线和换行所需空间。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QFontMetrics>`
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

围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。 使用时通常按这个过程组织：构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QFontMetrics(const QFont &font)`
- `QFontMetrics(const QFont &font, const QPaintDevice *paintdevice)`
- `QFontMetrics(const QFontMetrics &fm)`
- `~QFontMetrics()`
- `int ascent() const`
- `int averageCharWidth() const`
- `QRect boundingRect(QChar ch) const`
- `QRect boundingRect(const QString &text) const`
- `(since 6.3) QRect boundingRect(const QString &text, const QTextOption &option) const`
- `QRect boundingRect(const QRect &rect, int flags, const QString &text, int tabStops = 0, int *tabArray = nullptr) const`
- `QRect boundingRect(int x, int y, int width, int height, int flags, const QString &text, int tabStops = 0, int *tabArray = nullptr) const`
- `int capHeight() const`
- `int descent() const`
- `QString elidedText(const QString &text, Qt::TextElideMode mode, int width, int flags = 0) const`
- `qreal fontDpi() const`
- `int height() const`
- `(since 6.3) int horizontalAdvance(const QString &text, const QTextOption &option) const`
- `int horizontalAdvance(const QString &text, int len = -1) const`
- `int horizontalAdvance(QChar ch) const`
- `bool inFont(QChar ch) const`
- `bool inFontUcs4(uint ucs4) const`
- `int leading() const`
- `int leftBearing(QChar ch) const`
- `int lineSpacing() const`
- `int lineWidth() const`
- `int maxWidth() const`
- `int minLeftBearing() const`
- `int minRightBearing() const`
- `int overlinePos() const`
- `int rightBearing(QChar ch) const`
- `QSize size(int flags, const QString &text, int tabStops = 0, int *tabArray = nullptr) const`
- `int strikeOutPos() const`
- `void swap(QFontMetrics &other)`
- `QRect tightBoundingRect(const QString &text) const`
- `(since 6.3) QRect tightBoundingRect(const QString &text, const QTextOption &option) const`
- `int underlinePos() const`
- `int xHeight() const`
- `bool operator!=(const QFontMetrics &other) const`
- `QFontMetrics & operator=(QFontMetrics &&other)`
- `QFontMetrics & operator=(const QFontMetrics &fm)`
- `bool operator==(const QFontMetrics &other) const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[explicit] QFontMetrics::QFontMetrics(const QFont &font)`

**作用与语义：**

为`font`构建字体度量对象。
字体度量将兼容用于创建`font`的绘图设备。
font metrics 对象保存在构建函数中传递的字体信息，若字体属性后来更改，则不更新。
使用 QFontMetrics（const `QFont` &， `QPaintDevice` *） 获取与特定绘图设备兼容的字体指标。

### `QFontMetrics::QFontMetrics(const QFont &font, const QPaintDevice *paintdevice)`

**作用与语义：**

构建一个字体度量对象用于`font`和`paintdevice`。
字体度量会与通过的 paintDevice 兼容。如果`paintdevice`是`nullptr`的，度量系统将与屏幕兼容，也就是说，这些度量是用该字体在`widgets`或`pixmaps`上绘制文字时获得的，而不是在`QPicture`或`QPrinter`上。
font metrics 对象保存在构建函数中传递的字体信息，若字体属性后来更改，则不更新。

### `QFontMetrics::QFontMetrics(const QFontMetrics &fm)`

**作用与语义：**

构建了`fm`的复制品。

### `[noexcept] QFontMetrics::~QFontMetrics()`

**作用与语义：**

销毁字体度量对象并释放所有分配的资源。

### `int QFontMetrics::ascent() const`

**作用与语义：**

返回洗礼盆的上升。
字体的上升是指从基线到字符延伸到最高位置的距离。实际上，一些字体设计师会打破这一规则，例如当他们在一个字符上加多个重音符号，或为了容纳某个字符时，因此（虽然罕见）这个数值可能会过小。

### `int QFontMetrics::averageCharWidth() const`

**作用与语义：**

返回字体中字形的平均宽度。

### `QRect QFontMetrics::boundingRect(QChar ch) const`

**作用与语义：**

如果在坐标系原点绘制字符`ch`，返回被墨水覆盖的矩形。
注意，边界矩形可能向（0， 0）左侧延伸（例如斜体字体），且文本输出可能覆盖边界矩形中的所有像素。对于空格字符，矩形通常为空。
注意，矩形通常同时延伸到基线的上下。
警告：返回矩形的宽度并非字符的前置宽度。请使用boundingRect（const `QString` &） 或 `horizontalAdvance()`。

### `QRect QFontMetrics::boundingRect(const QString &text) const`

**作用与语义：**

返回由 `text` 指定字符串中字符的边界矩形。边界矩形总是至少覆盖文本在绘制时将覆盖的像素集合。
注意，边界矩形可能向（0， 0）左侧延伸，例如斜体字体，且返回矩形的宽度可能与`horizontalAdvance()`方法返回的宽度不同。
如果你想知道弦的前进宽度（以便将一组弦并排排列），可以用`horizontalAdvance()`。
换行字符被当作普通字符处理，而不是换行符。
边界矩形的高度至少与`height()`返回的值相当。

### `[since 6.3] QRect QFontMetrics::boundingRect(const QString &text, const QTextOption &option) const`

**作用与语义：**

返回由`text` `option`布局的字符串中字符的边界矩形。边界矩形总是至少覆盖文本在（0， 0）处绘制时将覆盖的像素集合。
注意，边界矩形可能向（0， 0）左侧延伸，例如斜体字体，且返回矩形的宽度可能与`horizontalAdvance()`方法返回的宽度不同。
如果你想知道弦的前进宽度（以便将一组弦线并排排列），可以用`horizontalAdvance()`。
换行字符被当作普通字符处理，而不是换行符。
包围矩形的高度至少与`height()`返回的值相当。

### `QRect QFontMetrics::boundingRect(const QRect &rect, int flags, const QString &text, int tabStops = 0, int *tabArray = nullptr) const`

**作用与语义：**

返回由 `text` 指定字符串中字符的边界矩形，即文本在绘制时覆盖的像素集合。绘图及边界矩形受限于矩形`rect`。
`flags`参数是以下标志的逐位或：
- `Qt::AlignLeft` 向左边界对齐，阿拉伯语和希伯来语则向右对齐。
- `Qt::AlignRight` 与右边边界对齐，阿拉伯语和希伯来语则向左。
- `Qt::AlignJustify`产生对齐文本。
- `Qt::AlignHCenter`水平对齐为中心。
- `Qt::AlignTop`对齐于顶部边框。
- `Qt::AlignBottom`对齐于底部边框。
- `Qt::AlignVCenter`垂直居中对齐
- `Qt::AlignCenter` （== `Qt::AlignHCenter | Qt::AlignVCenter`）
- `Qt::TextSingleLine` 忽略文本中的换行字符。
- `Qt::TextExpandTabs` 扩展制表表（见下文）
- `Qt::TextShowMnemonic`将“&x”解释为x;即下划线。
- `Qt::TextWordWrap`将文本拆分以适应矩形。
`Qt::Horizontal`对齐默认为`Qt::AlignLeft`，垂直对齐默认为`Qt::AlignTop`。
如果设置多个水平或多个垂直对齐标志，则最终的对齐是未定义的。
如果`Qt::TextExpandTabs`设在`flags`中，则：如果`tabArray`非空，则指定制表符的0端像素位置序列;如果`tabStops`非零，则用作制表表间距（以像素计）。
注意，边界矩形可以向（0， 0）左侧延伸，例如斜体字体，且文本输出可能覆盖边界矩形中的所有像素。
换行字符以换行符的形式处理。
尽管实际字符高度不同，“是”和“是”这两个边界矩形的高度是相同的。
该函数返回的边界矩形比更简单的 boundingRect() 函数计算的矩形略大。该函数使用多行文本正确对齐所需的最大左侧和 `right` 字体方位。此外，fontHeight() 和 `lineSpacing()` 用于计算高度，而非单个字符高度。

### `QRect QFontMetrics::boundingRect(int x, int y, int width, int height, int flags, const QString &text, int tabStops = 0, int *tabArray = nullptr) const`

**作用与语义：**

返回由`x`坐标、`width`和`height`指定`y`矩形内给定`text`的边界矩形。
如果`Qt::TextExpandTabs`设为`flags`且`tabArray`非空，则指定制表符的像素位置序列为0端;否则，如果`tabStops`非零，则用作制表符间距（以像素计）。

### `int QFontMetrics::capHeight() const`

**作用与语义：**

返回字体的大小写高度。
字体的大写高度是指大写字母高于基线的高度。它具体指的是扁平的大写字母（如H或I）的高度，与圆头字母如O或尖头字母（如A）相对，后者可能显示超升。

### `int QFontMetrics::descent() const`

**作用与语义：**

返回洗礼盆的下降。
下降是指从基线到最低点字符延伸到的距离。实际上，一些字体设计师会打破这一规则，例如为了适应某个字符，因此虽然很少见，但这个值可能会太小。

### `QString QFontMetrics::elidedText(const QString &text, Qt::TextElideMode mode, int width, int flags = 0) const`

**作用与语义：**

如果字符串`text`宽于`width`，则返回字符串的省略版本（即字符串中带有“...”）。否则，返回原始字符串。
`mode`参数指定文本是左侧省略（例如，“...tech”），在中间（例如，“Tr......”ch“），还是在右侧（例如，”Trol...“）。
`width`以像素为单位，而非字符。
`flags`参数是可选的，目前只支持`Qt::TextShowMnemonic`作为值。
省号跟随`layoutdirection`。例如，如果`mode`是`Qt::ElideLeft`，则从右到左的排版中，省号会在文本的右侧;如果`mode` `Qt::ElideRight`，则在左侧。

### `qreal QFontMetrics::fontDpi() const`

**作用与语义：**

返回字体DPI。

### `int QFontMetrics::height() const`

**作用与语义：**

返回字体高度。
这总是等于`ascent()` `descent()`。

### `[since 6.3] int QFontMetrics::horizontalAdvance(const QString &text, const QTextOption &option) const`

**作用与语义：**

返回使用`option`布局的`text`水平像素数。
前进是指在`text`之后绘制下一个字符所需的适当距离。

### `int QFontMetrics::horizontalAdvance(const QString &text, int len = -1) const`

**作用与语义：**

返回`text`前`len`字符的水平前进像素。如果`len`为负（默认），则使用整个字符串。即使`len`明显较短，也会分析整个`text`长度。
这是画`text`后下一个字符的合适距离。

### `int QFontMetrics::horizontalAdvance(QChar ch) const`

**作用与语义：**

返回字符`ch`的水平前进（像素单位）。这是一个适合在`ch`之后绘制下一个字符的距离。
图中描述了一些度量。中央的深色矩形覆盖每个字符的逻辑水平Advance()。外侧浅色矩形覆盖每个字符的正`leftBearing()`和`rightBearing()`。注意该字体中“f”的进位都是负的，而“o”的方位都是正的。
警告：该函数会因处理字符串时出现的阿拉伯字符或非空格标记产生错误结果，因为处理字符串时标记的字形形状和位置无法考虑。在实现交互式文本控件时，请使用`QTextLayout`。

### `bool QFontMetrics::inFont(QChar ch) const`

**作用与语义：**

如果字符 `ch` 在字体中是有效字符，则返回 `true`；否则返回 `false`。

### `bool QFontMetrics::inFontUcs4(uint ucs4) const`

**作用与语义：**

如果用 UCS-4/UTF-32 编码的字符`ucs4`字体中有效字符，返回 `true`;否则返回 `false`。

### `int QFontMetrics::leading() const`

**作用与语义：**

返回字体的前导。
这就是自然的行间距。

### `int QFontMetrics::leftBearing(QChar ch) const`

**作用与语义：**

返回字体中左侧的字符`ch`。
左方位角是字符最左端像素与字符逻辑原点的向右距离。如果字符的像素向逻辑原点左侧延伸，则该值为负数。
该指标的图形描述请参见 `horizontalAdvance()`。

### `int QFontMetrics::lineSpacing() const`

**作用与语义：**

返回从一个基线到下一个基线的距离。
这个值总是等于`leading()` `height()`。

### `int QFontMetrics::lineWidth() const`

**作用与语义：**

返回下划线和划线线的宽度，并根据字体点大小进行调整。

### `int QFontMetrics::maxWidth() const`

**作用与语义：**

返回字体中最宽字符的宽度。

### `int QFontMetrics::minLeftBearing() const`

**作用与语义：**

返回字体的最小左方位。
这是字体中最小的`leftBearing`（字符）。
注意，如果字体较大，这个功能可能会非常慢。

### `int QFontMetrics::minRightBearing() const`

**作用与语义：**

返回字体的最小右方位。
这是字体中最小的 `rightBearing`（char）。
注意，如果字体较大，这个功能可能会非常慢。

### `int QFontMetrics::overlinePos() const`

**作用与语义：**

返回从基线到应绘制上线的距离。

### `int QFontMetrics::rightBearing(QChar ch) const`

**作用与语义：**

返回字体中正确的字符方位`ch`。
右方位角是字符最右边像素与后一个字符逻辑原点的向左距离。如果字符的像素延伸到字符`horizontalAdvance()`的右侧，则该值为负。
该指标的图解描述请参见 `horizontalAdvance()`。

### `QSize QFontMetrics::size(int flags, const QString &text, int tabStops = 0, int *tabArray = nullptr) const`

**作用与语义：**

返回像素大小为`text`。
`flags`论元是以下标志的逐位或：
- `Qt::TextSingleLine` 忽略换行字符。
- `Qt::TextExpandTabs` 扩展制表表（见下文）
- `Qt::TextShowMnemonic`将“&x”解释为x;即下划线。
- `Qt::TextWordWrap` 将文本拆分以适应矩形。
如果`Qt::TextExpandTabs`设在`flags`，则：如果`tabArray`非空，则指定制表符的0终止像素位置序列;否则如果`tabStops`非零，则用作制表表符间距（以像素为单位）。
换行字符以换行符的形式处理。
尽管实际字符高度不同，“是”和“是”这两个边界矩形的高度是相同的。

### `int QFontMetrics::strikeOutPos() const`

**作用与语义：**

返回从基线到三振线应画的距离。

### `[noexcept] void QFontMetrics::swap(QFontMetrics &other)`

**作用与语义：**

将该字体度量实例与`other`交换。此操作非常快且从未失败。

### `QRect QFontMetrics::tightBoundingRect(const QString &text) const`

**作用与语义：**

返回一个紧密的边界矩形，围绕字符串中由`text`指定的字符。边界矩形总是至少覆盖文本在（0， 0）绘制时将覆盖的像素集合。
注意，边界矩形可能向（0， 0）左侧延伸，例如斜体字体，且返回矩形的宽度可能与`horizontalAdvance()`方法返回的宽度不同。
如果你想知道弦的前进宽度（以便将一组弦并排排列），可以用`horizontalAdvance()`。
换行字符被当作普通字符处理，而不是换行符。

### `[since 6.3] QRect QFontMetrics::tightBoundingRect(const QString &text, const QTextOption &option) const`

**作用与语义：**

返回一个紧密的边界矩形，围绕字符串中由`text`用`option`布局的字符。边界矩形总是至少覆盖文本在绘制时将覆盖的像素集合。
注意，边界矩形可能向（0， 0）左侧延伸，例如斜体字体，且返回矩形的宽度可能与`horizontalAdvance()`方法返回的宽度不同。
如果你想知道弦的提前宽度（以便将一组弦排列在一起），可以用`horizontalAdvance()`。
换行字符被当作普通字符处理，而不是换行符。

### `int QFontMetrics::underlinePos() const`

**作用与语义：**

返回从基线到应画下划线的距离。

### `int QFontMetrics::xHeight() const`

**作用与语义：**

返回字体的“x”高度。这通常但不总是等同于字符“x”的高度。

### `bool QFontMetrics::operator!=(const QFontMetrics &other) const`

**作用与语义：**

如果 不等于 `other` 该对象，返回 `true`;否则返回 `false`。
如果两种字体指标由相同`QFont`构建且所用的绘图设备被认为兼容，则视为等同。

### `[noexcept] QFontMetrics &QFontMetrics::operator=(QFontMetrics &&other)`

**作用与语义：**

Move-assign `other` 到该`QFontMetrics`实例。

### `QFontMetrics &QFontMetrics::operator=(const QFontMetrics &fm)`

**作用与语义：**

分配字体度量 `fm`。

### `bool QFontMetrics::operator==(const QFontMetrics &other) const`

**作用与语义：**

如果`other`等于该对象，则返回`true`;否则返回`false`。
如果两种字体度量由相同`QFont`构建且所用的绘图设备被认为兼容，则视为平等。

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

`QFontMetrics` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
