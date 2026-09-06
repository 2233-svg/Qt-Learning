# QGlyphRun

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QGlyphRun` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QGlyphRun>`
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

- `enum GlyphRunFlag { Overline, Underline, StrikeOut, RightToLeft, SplitLigature }`
- `flags GlyphRunFlags`

### 公有函数

- `QGlyphRun()`
- `QGlyphRun(const QGlyphRun &other)`
- `~QGlyphRun()`
- `QRectF boundingRect() const`
- `void clear()`
- `QGlyphRun::GlyphRunFlags flags() const`
- `QList<quint32> glyphIndexes() const`
- `bool isEmpty() const`
- `bool isRightToLeft() const`
- `bool overline() const`
- `QList<QPointF> positions() const`
- `QRawFont rawFont() const`
- `void setBoundingRect(const QRectF &boundingRect)`
- `void setFlag(QGlyphRun::GlyphRunFlag flag, bool enabled = true)`
- `void setFlags(QGlyphRun::GlyphRunFlags flags)`
- `void setGlyphIndexes(const QList<quint32> &glyphIndexes)`
- `void setOverline(bool overline)`
- `void setPositions(const QList<QPointF> &positions)`
- `void setRawData(const quint32 *glyphIndexArray, const QPointF *glyphPositionArray, int size)`
- `void setRawFont(const QRawFont &rawFont)`
- `void setRightToLeft(bool rightToLeft)`
- `(since 6.5) void setSourceString(const QString &sourceString)`
- `void setStrikeOut(bool strikeOut)`
- `(since 6.5) void setStringIndexes(const QList<qsizetype> &stringIndexes)`
- `void setUnderline(bool underline)`
- `(since 6.5) QString sourceString() const`
- `bool strikeOut() const`
- `(since 6.5) QList<qsizetype> stringIndexes() const`
- `void swap(QGlyphRun &other)`
- `bool underline() const`
- `bool operator!=(const QGlyphRun &other) const`
- `QGlyphRun & operator=(const QGlyphRun &other)`
- `bool operator==(const QGlyphRun &other) const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QGlyphRun::GlyphRunFlagflags QGlyphRun::GlyphRunFlags`

**作用与语义：**

此枚举描述了修改字形运行在视觉布局中显示或行为方式的标志。生成字形运行的布局可以根据相关的内部数据设置这些标志，以保留呈现文本时所需的信息，以符合布局用户的预期。
- `QGlyphRun::Overline`: `0x01`; 表示字形应与上划线一起显示。
- `QGlyphRun::Underline`: `0x02`; 表示字形应与下划线一起显示。
- `QGlyphRun::StrikeOut`: `0x04`; 表示字形应被视觉上划掉。
- `QGlyphRun::RightToLeft`: `0x08`; 表示字形按从右到左的顺序排列。这可能会影响与字形运行相对的其他屏幕元素的位置，例如内联文本对象。
- `QGlyphRun::SplitLigature`: `0x10`; 表示字形运行拆分了连字字形。这意味着运行中包含了连字字形，但其所对应的字符仅是该连字的一部分。在这种情况下，可以使用字形运行的 `boundingRect()` 函数来获取对应字形运行所代表字符的区域。在可视化字形时，需要注意裁剪到此边界矩形以确保仅绘制连字的相应部分。特别是在从 `QTextLayout` 中为特定字符范围检索字形运行时，例如在检索 `QTextLayout` 的选中区域时，这种情况可能会发生。
GlyphRunFlags 类型是 QFlags<GlyphRunFlag> 的类型定义。它存储 GlyphRunFlag 值的 OR 组合。

### `QGlyphRun::QGlyphRun()`

**作用与语义：**

构造一个空的 QGlyphRun 对象。

### `QGlyphRun::QGlyphRun(const QGlyphRun &other)`

**作用与语义：**

构建一个QGlyphRun对象，该对象是`other`的复制品。

### `[noexcept] QGlyphRun::~QGlyphRun()`

**作用与语义：**

摧毁了`QGlyphRun`。

### `QRectF QGlyphRun::boundingRect() const`

**作用与语义：**

返回包含该`QGlyphRun`中所有字形的最小矩形。如果用`setBoundingRect()`设置了边界矩形，则返回该矩形。否则，边界矩形将根据字形运行中的字体度量计算。

### `void QGlyphRun::clear()`

**作用与语义：**

清除`QGlyphRun`对象中的所有数据。

### `QGlyphRun::GlyphRunFlags QGlyphRun::flags() const`

**作用与语义：**

返回本`QGlyphRun`设置的标志。

### `QList<quint32> QGlyphRun::glyphIndexes() const`

**作用与语义：**

返回该`QGlyphRun`对象的字形索引。

### `bool QGlyphRun::isEmpty() const`

**作用与语义：**

如果`QGlyphRun`中没有任何字形，返回`true`。

### `bool QGlyphRun::isRightToLeft() const`

**作用与语义：**

如果该`QGlyphRun`包含从右向左绘制的字形，返回`true`。

### `bool QGlyphRun::overline() const`

**作用与语义：**

退`true`是否应该用描边装饰来绘制这`QGlyphRun`。

### `QList<QPointF> QGlyphRun::positions() const`

**作用与语义：**

返回该字形索引集合中每个字形基线边的位置。

### `QRawFont QGlyphRun::rawFont() const`

**作用与语义：**

返回该`QGlyphRun`对象所选字体。

### `void QGlyphRun::setBoundingRect(const QRectF &boundingRect)`

**作用与语义：**

将该`QGlyphRun`中字形的边界矩形设置为`boundingRect`。除非该矩形为空，否则`boundingRect()`返回该矩形的边界矩形。
注意：除非你实现了文本形状，否则你不需要使用这个函数。它专门用于`QGlyphRun`应表示的面积小于其字形面积时。例如，如果通过调用`QTextLayout::glyphRuns()`检索字形，且指定范围只包含连字的一部分（即两个或多个字符合并为一个字形）。在这种情况下，边界矩形应仅包含连字字形中相应的部分，基于连字中字符的平均宽度计算。
为了支持这种情况（例如选段颜色应与主文本颜色不同），需要将绘画机构裁剪到从`boundingRect()`返回的矩形上，以避免绘制整个连字字形。

### `void QGlyphRun::setFlag(QGlyphRun::GlyphRunFlag flag, bool enabled = true)`

**作用与语义：**

如果`enabled`为真，则`flag`被启用;否则，该功能被禁用。

### `void QGlyphRun::setFlags(QGlyphRun::GlyphRunFlags flags)`

**作用与语义：**

这让本`QGlyphRun`的标志降为`flags`。

### `void QGlyphRun::setGlyphIndexes(const QList<quint32> &glyphIndexes)`

**作用与语义：**

将该`QGlyphRun`对象的字形索引设置为`glyphIndexes`。字形索引必须对所选字体有效。

### `void QGlyphRun::setOverline(bool overline)`

**作用与语义：**

如果`overline`正确，表示该`QGlyphRun`应涂有上线装饰。否则`QGlyphRun`应涂无上线装饰。

### `void QGlyphRun::setPositions(const QList<QPointF> &positions)`

**作用与语义：**

将该字形索引集中每个字形基线边缘的位置设置为`positions`。

### `void QGlyphRun::setRawData(const quint32 *glyphIndexArray, const QPointF *glyphPositionArray, int size)`

**作用与语义：**

设置该`QGlyphRun`的字形索引和位置，使用数组 `glyphIndexArray` 和 `glyphPositionArray` 中的前`size`元素。数据不会被复制。调用者必须保证只要该数组`QGlyphRun`及其副本存在，这些数组不会被删除。

### `void QGlyphRun::setRawFont(const QRawFont &rawFont)`

**作用与语义：**

设置查找指定`rawFont`字形索引的字体。

### `void QGlyphRun::setRightToLeft(bool rightToLeft)`

**作用与语义：**

表示该`QGlyphRun`包含的字形应从右向左排列（如果`rightToLeft`为真）。否则，字形的顺序被假定为从左到右。

### `[since 6.5] void QGlyphRun::setSourceString(const QString &sourceString)`

**作用与语义：**

将对应字形运行的字符串设置为`sourceString`。如果设置为，`stringIndexes()`返回的索引应当是该字符串的索引。

### `void QGlyphRun::setStrikeOut(bool strikeOut)`

**作用与语义：**

如果`strikeOut`属实，表示该`QGlyphRun`应涂有划线装饰。否则`QGlyphRun`应涂无划线装饰。

### `[since 6.5] void QGlyphRun::setStringIndexes(const QList<qsizetype> &stringIndexes)`

**作用与语义：**

将对应字形索引的字符串索引列表设置为`stringIndexes`。
有关本列表惯例的更多细节，请参见`stringIndexes()`。

### `void QGlyphRun::setUnderline(bool underline)`

**作用与语义：**

如果`underline`正确，表示该`QGlyphRun`应涂有下划线装饰。否则`QGlyphRun`应涂无下划线装饰。

### `[since 6.5] QString QGlyphRun::sourceString() const`

**作用与语义：**

如果字形运行是由字符串创建且该字符串是从布局中请求的，则返回对应字形运行的字符串。

### `bool QGlyphRun::strikeOut() const`

**作用与语义：**

退货`true`是否该用划线装饰涂上`QGlyphRun`。

### `[since 6.5] QList<qsizetype> QGlyphRun::stringIndexes() const`

**作用与语义：**

如果字形运行由字符串构成且已从布局请求字符串索引，则返回对应每个字形索引的字符串索引。此时返回的向量长度对应于 `glyphIndexes()` 的长度。其他情况下，该向量为空。
由于单个字形可能对应源字符串中的多个字符，字符串索引列表中可能存在空缺。例如，如果字符串“first”被包含字符对“fi”连字的字体处理，那么五字符字符串将生成一个仅包含四个字形的字形连续。此时字形索引可能是（1， 2， 3， 4）（四个任意字形索引），而字符串索引为（0， 2， 3， 4）。字形按字符串的逻辑顺序排列，因此推测第一个字形跨字符0和1。
反之，单个字符也可能生成多个字形，此时字符串索引列表中会出现重复条目。
字符串索引对应于字符串，可通过`sourceString()`选择性地获得。

### `[noexcept] void QGlyphRun::swap(QGlyphRun &other)`

**作用与语义：**

将这个字形运行实例与`other`交换。这个操作非常快，从未失败过。

### `bool QGlyphRun::underline() const`

**作用与语义：**

退货`true`是否需要用底线装饰来涂装这`QGlyphRun`。

### `bool QGlyphRun::operator!=(const QGlyphRun &other) const`

**作用与语义：**

将 `other` 与此 `QGlyphRun` 对象进行比较。如果字符索引列表、位置列表或字体有任何不同，则返回 `true`，否则返回 `false`。

### `QGlyphRun &QGlyphRun::operator=(const QGlyphRun &other)`

**作用与语义：**

为该`QGlyphRun`对象分配`other`。

### `bool QGlyphRun::operator==(const QGlyphRun &other) const`

**作用与语义：**

将 `other` 与此 `QGlyphRun` 对象进行比较。如果字形索引列表、位置列表和字体都相等，则返回 `true`，否则返回 `false`。

### `enum GlyphRunFlag { Overline, Underline, StrikeOut, RightToLeft, SplitLigature }`

**作用与语义：**

此枚举描述了修改字形运行在视觉布局中显示或行为方式的标志。生成字形运行的布局可以根据相关的内部数据设置这些标志，以保留呈现文本时所需的信息，以符合布局用户的预期。
- `QGlyphRun::Overline`: `0x01`; 表示字形应与上划线一起显示。
- `QGlyphRun::Underline`: `0x02`; 表示字形应与下划线一起显示。
- `QGlyphRun::StrikeOut`: `0x04`; 表示字形应被视觉上划掉。
- `QGlyphRun::RightToLeft`: `0x08`; 表示字形按从右到左的顺序排列。这可能会影响与字形运行相对的其他屏幕元素的位置，例如内联文本对象。
- `QGlyphRun::SplitLigature`: `0x10`; 表示字形运行拆分了连字字形。这意味着运行中包含了连字字形，但其所对应的字符仅是该连字的一部分。在这种情况下，可以使用字形运行的 `boundingRect()` 函数来获取对应字形运行所代表字符的区域。在可视化字形时，需要注意裁剪到此边界矩形以确保仅绘制连字的相应部分。特别是在从 `QTextLayout` 中为特定字符范围检索字形运行时，例如在检索 `QTextLayout` 的选中区域时，这种情况可能会发生。
GlyphRunFlags 类型是 QFlags<GlyphRunFlag> 的类型定义。它存储 GlyphRunFlag 值的 OR 组合。

### `flags GlyphRunFlags`

**作用与语义：**

此枚举描述了修改字形运行在视觉布局中显示或行为方式的标志。生成字形运行的布局可以根据相关的内部数据设置这些标志，以保留呈现文本时所需的信息，以符合布局用户的预期。
- `QGlyphRun::Overline`: `0x01`; 表示字形应与上划线一起显示。
- `QGlyphRun::Underline`: `0x02`; 表示字形应与下划线一起显示。
- `QGlyphRun::StrikeOut`: `0x04`; 表示字形应被视觉上划掉。
- `QGlyphRun::RightToLeft`: `0x08`; 表示字形按从右到左的顺序排列。这可能会影响与字形运行相对的其他屏幕元素的位置，例如内联文本对象。
- `QGlyphRun::SplitLigature`: `0x10`; 表示字形运行拆分了连字字形。这意味着运行中包含了连字字形，但其所对应的字符仅是该连字的一部分。在这种情况下，可以使用字形运行的 `boundingRect()` 函数来获取对应字形运行所代表字符的区域。在可视化字形时，需要注意裁剪到此边界矩形以确保仅绘制连字的相应部分。特别是在从 `QTextLayout` 中为特定字符范围检索字形运行时，例如在检索 `QTextLayout` 的选中区域时，这种情况可能会发生。
GlyphRunFlags 类型是 QFlags<GlyphRunFlag> 的类型定义。它存储 GlyphRunFlag 值的 OR 组合。

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

`QGlyphRun` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
