# QRawFont

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QRawFont` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QRawFont>`
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

- `enum AntialiasingType { PixelAntialiasing, SubPixelAntialiasing }`
- `enum LayoutFlag { SeparateAdvances, KernedAdvances, UseDesignMetrics }`
- `flags LayoutFlags`

### 公有函数

- `QRawFont()`
- `QRawFont(const QByteArray &fontData, qreal pixelSize, QFont::HintingPreference hintingPreference = QFont::PreferDefaultHinting)`
- `QRawFont(const QString &fileName, qreal pixelSize, QFont::HintingPreference hintingPreference = QFont::PreferDefaultHinting)`
- `QRawFont(const QRawFont &other)`
- `~QRawFont()`
- `QList<QPointF> advancesForGlyphIndexes(const QList<quint32> &glyphIndexes, QRawFont::LayoutFlags layoutFlags) const`
- `bool advancesForGlyphIndexes(const quint32 *glyphIndexes, QPointF *advances, int numGlyphs, QRawFont::LayoutFlags layoutFlags) const`
- `QList<QPointF> advancesForGlyphIndexes(const QList<quint32> &glyphIndexes) const`
- `bool advancesForGlyphIndexes(const quint32 *glyphIndexes, QPointF *advances, int numGlyphs) const`
- `QImage alphaMapForGlyph(quint32 glyphIndex, QRawFont::AntialiasingType antialiasingType = SubPixelAntialiasing, const QTransform &transform = QTransform()) const`
- `qreal ascent() const`
- `qreal averageCharWidth() const`
- `QRectF boundingRect(quint32 glyphIndex) const`
- `qreal capHeight() const`
- `qreal descent() const`
- `QString familyName() const`
- `(since 6.7) QByteArray fontTable(QFont::Tag tag) const`
- `QByteArray fontTable(const char *tag) const`
- `(since 6.11) quint32 glyphCount() const`
- `bool glyphIndexesForChars(const QChar *chars, int numChars, quint32 *glyphIndexes, int *numGlyphs) const`
- `QList<quint32> glyphIndexesForString(const QString &text) const`
- `(since 6.11) QString glyphName(quint32 glyphIndex) const`
- `QFont::HintingPreference hintingPreference() const`
- `bool isValid() const`
- `qreal leading() const`
- `qreal lineThickness() const`
- `void loadFromData(const QByteArray &fontData, qreal pixelSize, QFont::HintingPreference hintingPreference)`
- `void loadFromFile(const QString &fileName, qreal pixelSize, QFont::HintingPreference hintingPreference)`
- `qreal maxCharWidth() const`
- `QPainterPath pathForGlyph(quint32 glyphIndex) const`
- `qreal pixelSize() const`
- `void setPixelSize(qreal pixelSize)`
- `QFont::Style style() const`
- `QString styleName() const`
- `QList<QFontDatabase::WritingSystem> supportedWritingSystems() const`
- `bool supportsCharacter(QChar character) const`
- `bool supportsCharacter(uint ucs4) const`
- `void swap(QRawFont &other)`
- `qreal underlinePosition() const`
- `qreal unitsPerEm() const`
- `int weight() const`
- `qreal xHeight() const`
- `bool operator!=(const QRawFont &other) const`
- `QRawFont & operator=(const QRawFont &other)`
- `bool operator==(const QRawFont &other) const`

### 静态公有成员

- `QRawFont fromFont(const QFont &font, QFontDatabase::WritingSystem writingSystem = QFontDatabase::Any)`

### 相关非成员函数

- `size_t qHash(const QRawFont &key, size_t seed = 0)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QRawFont::AntialiasingType`

**作用与语义：**

这个枚举表示字形在函数`alphaMapForGlyph()`中光栅化的不同方式。
- `QRawFont::PixelAntialiasing`：`0`;通过测量该形状在整像素上的覆盖度来进行光栅化。返回的图像包含每个像素基于字形覆盖率的α值。
- `QRawFont::SubPixelAntialiasing`：`1`;通过测量每个子像素的覆盖率进行光栅化，分别返回每个像素的红、绿、蓝分量的单独α值。

### `enum QRawFont::LayoutFlagflags QRawFont::LayoutFlags`

**作用与语义：**

这个枚举告诉函数 `advancesForGlyphIndexes()` 如何计算前进量。
- `QRawFont::SeparateAdvances`: `0`; 将为每个字形单独计算前进量。
- `QRawFont::KernedAdvances`: `1`; 在相邻字形之间应用字距调整。请注意，目前不支持基于 OpenType GPOS 的字距调整。
- `QRawFont::UseDesignMetrics`: `2`; 使用设计指标而不是调整到绘图设备分辨率的提示指标。可以与上述任意选项进行或运算。
LayoutFlags 类型是 QFlags<LayoutFlag> 的一个 typedef。它存储 LayoutFlag 值的或组合。

### `QRawFont::QRawFont()`

**作用与语义：**

构造一个无效的QRawFont。

### `QRawFont::QRawFont(const QByteArray &fontData, qreal pixelSize, QFont::HintingPreference hintingPreference = QFont::PreferDefaultHinting)`

**作用与语义：**

构建一个QRawFont，表示所提供`fontData`中包含的字体，大小（像素`pixelSize`），并使用`hintingPreference`指定的提示偏好。
注意：数据必须包含 TrueType 或 OpenType 字体。

### `QRawFont::QRawFont(const QString &fileName, qreal pixelSize, QFont::HintingPreference hintingPreference = QFont::PreferDefaultHinting)`

**作用与语义：**

构建一个QRawFont，表示`fileName`引用的文件中字体，尺寸（像素）由`pixelSize`给出，并使用`hintingPreference`指定的提示偏好。
注意：所引用的文件必须包含 TrueType 或 OpenType 字体。

### `QRawFont::QRawFont(const QRawFont &other)`

**作用与语义：**

创建一个QRawFont，是`other`的复制品。

### `[noexcept] QRawFont::~QRawFont()`

**作用与语义：**

摧毁了`QRawFont`。

### `QList<QPointF> QRawFont::advancesForGlyphIndexes(const QList<quint32> &glyphIndexes, QRawFont::LayoutFlags layoutFlags) const`

**作用与语义：**

返回每个`glyphIndexes`的前进`QRawFont`像素单位。前进给出了从给定字形位置到下一个字形绘制位置的距离，使得两个字形看起来像是无间隔。进阶的计算方式由`layoutFlags`控制。
注意：当请求`KernedAdvances`时，该函数会从TrueType表`KERN`应用字距调整规则（如果字体中有相应功能）。在许多现代字体中，字距调整通过OpenType规则或AAT规则处理，这需要应用完整的形状步骤。要获得完整形状文本的结果，请使用`QTextLayout`。

### `bool QRawFont::advancesForGlyphIndexes(const quint32 *glyphIndexes, QPointF *advances, int numGlyphs, QRawFont::LayoutFlags layoutFlags) const`

**作用与语义：**

返回每个`QRawFont` `glyphIndexes`的前进，单位为像素单位。前进给出了从给定字形位置到下一个字形应绘制位置的距离，使两个字形看起来像是无间距。字形索引由数组给出`glyphIndexes`虽然结果通过`advances`返回，但两者都必须包含`numGlyphs`元素。前进的计算方式由`layoutFlags`控制。
注意：当请求`KernedAdvances`时，该函数会从字体中提供 TrueType 表 `KERN` 的字距调整规则（如果字体中有此功能）。在许多现代字体中，字距调整通过 OpenType 规则或 AAT 规则处理，这需要应用完整的塑形步骤。要获得完全整形文本的结果，请使用 `QTextLayout`。

### `QList<QPointF> QRawFont::advancesForGlyphIndexes(const QList<quint32> &glyphIndexes) const`

**作用与语义：**

返回每个`glyphIndexes`的`QRawFont`的提前，单位为像素。这些推进给出了从给定字形位置到下一个字形应绘制位置的距离，使得看起来两个字形之间没有间隔。每个字形的前进是单独计算的。

### `bool QRawFont::advancesForGlyphIndexes(const quint32 *glyphIndexes, QPointF *advances, int numGlyphs) const`

**作用与语义：**

返回每个`glyphIndexes`的 `QRawFont` 的进度（像素单位）。前进给出了从给定字形位置到下一个字形绘制位置的距离，使两个字形看起来像是无间距。字形索引由数组给出`glyphIndexes`虽然结果通过 `advances` 返回，但两者都必须包含`numGlyphs`元素。每个字形的前进分别计算。

### `QImage QRawFont::alphaMapForGlyph(quint32 glyphIndex, QRawFont::AntialiasingType antialiasingType = SubPixelAntialiasing, const QTransform &transform = QTransform()) const`

**作用与语义：**

该函数返回底层字体中给定`glyphIndex`的字形光栅化图像，使用指定的`transform`。如果`QRawFont`无效，该函数将返回无效`QImage`。
如果字体是彩色字体，那么生成的图像将包含当前像素大小的渲染字形。在这种情况下，`antialiasingType`将被忽略。
否则，如果`antialiasingType`设置为`QRawFont::SubPixelAntialiasing`，则生成的图像将处于`QImage::Format_RGB32`，每个像素的RGB值将代表该像素在光栅化中的子像素不透明度。否则，图像将采用`QImage::Format_Indexed8`格式，每个像素包含光栅化中该像素的不透明度。

### `qreal QRawFont::ascent() const`

**作用与语义：**

返回该`QRawFont`的上升，单位为像素单位。
字体的上升是指从基线到字符最高位置的距离。实际上，一些字体设计师会打破这一规则，例如当他们在一个字符上加多个重音符号，或为了适应异国语言中的特殊字符时，因此（虽然罕见）这个值可能会过小。

### `qreal QRawFont::averageCharWidth() const`

**作用与语义：**

返回该`QRawFont`的平均字符宽度（像素单位）。

### `QRectF QRawFont::boundingRect(quint32 glyphIndex) const`

**作用与语义：**

返回包含给定`glyphIndex`字形的最小矩形。

### `qreal QRawFont::capHeight() const`

**作用与语义：**

返回该`QRawFont`的电容高度，单位为像素单位。
字体的大写高度是指大写字母高于基线的高度。它具体指的是扁平的大写字母（如H或I）的高度，与圆头字母如O或尖头字母（如A）相对，后者可能显示超升。

### `qreal QRawFont::descent() const`

**作用与语义：**

返回该`QRawFont`的下降，单位为像素单位。
下降是指从基线到字符延伸到最低点的距离。实际上，一些字体设计师会打破这一规则，例如为了适应异国语言中的特殊字符，因此（虽然罕见）这个值可能过小。

### `QString QRawFont::familyName() const`

**作用与语义：**

还原了这个`QRawFont`的姓氏。

### `[since 6.7] QByteArray QRawFont::fontTable(QFont::Tag tag) const`

**作用与语义：**

从底层物理字体中检索`tag`指定的sfnt表，若未发现空字节数组则检索。返回的字体表的字节顺序为大端序，符合sfnt格式的规定。

### `QByteArray QRawFont::fontTable(const char *tag) const`

**作用与语义：**

名称必须是四字符字符串。
注意：该函数会超载 `fontTable`（QFont：：Tag）。

### `[static] QRawFont QRawFont::fromFont(const QFont &font, QFontDatabase::WritingSystem writingSystem = QFontDatabase::Any)`

**作用与语义：**

基于`font`查询获取物理表示。返回的物理字体是Qt优先显示选定`writingSystem`文本的字体。
警告：该函数可能成本较高，不应在性能敏感代码中调用。

### `[since 6.11] quint32 QRawFont::glyphCount() const`

**作用与语义：**

返回该`QRawFont`中的符文数量。

### `bool QRawFont::glyphIndexesForChars(const QChar *chars, int numChars, quint32 *glyphIndexes, int *numGlyphs) const`

**作用与语义：**

利用底层字体中的 CMAP 表将一串 Unicode 点转换为字形索引。该函数的工作原理与 `glyphIndexesForString()` 类似，但它接收一个数组（`chars`），结果会返回`glyphIndexes`，但数组和字形数量会在 `numGlyphs` 中设置。数组的大小`glyphIndexes`至少要`numChars`，如果还不够，这个函数会返回 false，然后你可以根据 `numGlyphs` 返回的大小调整 `glyphIndexes`。

### `QList<quint32> QRawFont::glyphIndexesForString(const QString &text) const`

**作用与语义：**

利用底层字体中的 CMAP 表将 `text` 给出的 Unicode 点串转换为字形索引，并返回包含结果的列表。
注意，如果字体中存在其他影响文本形状的表格，返回的字形索引无法正确表示文本的渲染。要获得正确形状的文本，您可以使用`QTextLayout`布局和塑造文本，然后调用 QTextLayout：：glyphs() 获取字形索引列表和`QRawFont`对。

### `[since 6.11] QString QRawFont::glyphName(quint32 glyphIndex) const`

**作用与语义：**

返回给定`glyphIndex`的名称。
如果字体中没有明确名称，则根据字形索引合成名称。

### `QFont::HintingPreference QRawFont::hintingPreference() const`

**作用与语义：**

返回用于构造该`QRawFont`的提示偏好。

### `bool QRawFont::isValid() const`

**作用与语义：**

如果 `QRawFont` 有效，则返回 `true`，否则返回 false。

### `qreal QRawFont::leading() const`

**作用与语义：**

返回该`QRawFont`的前导像素单位。
这就是自然的行间距。

### `qreal QRawFont::lineThickness() const`

**作用与语义：**

返回绘制线条（下划线、划线等）的粗细，同时返回用该字体绘制的文字。

### `void QRawFont::loadFromData(const QByteArray &fontData, qreal pixelSize, QFont::HintingPreference hintingPreference)`

**作用与语义：**

用`fontData` `pixelSize`给出的尺寸（像素）的字体替换当前`QRawFont`，并使用`hintingPreference`指定的提示偏好。
`fontData`必须包含TrueType或OpenType字体。

### `void QRawFont::loadFromFile(const QString &fileName, qreal pixelSize, QFont::HintingPreference hintingPreference)`

**作用与语义：**

用`fileName`引用的文件内容替换当前`QRawFont`，文件大小（以像素计）由`pixelSize`给出，并使用`hintingPreference`指定的提示偏好。
文件必须引用 TrueType 或 OpenType 字体。

### `qreal QRawFont::maxCharWidth() const`

**作用与语义：**

返回字体中最宽字符的宽度。

### `QPainterPath QRawFont::pathForGlyph(quint32 glyphIndex) const`

**作用与语义：**

如果该`QRawFont`有效，该函数返回底层字体某一`glyphIndex`的字形形状。否则，返回空`QPainterPath`。
归还的符文永远不会被暗示。

### `qreal QRawFont::pixelSize() const`

**作用与语义：**

返回该`QRawFont`设定的像素大小。像素大小影响字形的光栅化方式、`pathForGlyph()`返回的字形大小，并用于将内部度量从设计单元转换为逻辑像素单元。

### `void QRawFont::setPixelSize(qreal pixelSize)`

**作用与语义：**

将该字体渲染的像素大小设置为`pixelSize`。

### `QFont::Style QRawFont::style() const`

**作用与语义：**

回归了本`QRawFont`的风格。

### `QString QRawFont::styleName() const`

**作用与语义：**

恢复了本`QRawFont`的样式名称。

### `QList<QFontDatabase::WritingSystem> QRawFont::supportedWritingSystems() const`

**作用与语义：**

返回字体文件中设计者提供的信息支持的书写系统列表。请注意，这并不保证支持字体中的某个特定 Unicode 点。您可以使用`supportsCharacter()`检查对单个特定字符的支持。
注意：该列表基于字体OS/2表中设置的Unicode范围和代码页范围确定，且底层字体文件中必须有此类表。

### `bool QRawFont::supportsCharacter(QChar character) const`

**作用与语义：**

如果字体的字形对应给定`character`，返回`true`。

### `bool QRawFont::supportsCharacter(uint ucs4) const`

**作用与语义：**

如果字体的字形对应于UCS-4编码的字符`ucs4`，返回`true`。

### `[noexcept] void QRawFont::swap(QRawFont &other)`

**作用与语义：**

将原始字体替换为`other`。这个操作非常快，从未失败过。

### `qreal QRawFont::underlinePosition() const`

**作用与语义：**

返回从基线开始绘制下划线的位置，用于在用该字体渲染的文本下方绘制下划线。

### `qreal QRawFont::unitsPerEm() const`

**作用与语义：**

返回设计单元数量定义了该`QRawFont`的电磁矩形的宽度和高度。该数值与像素大小一起用于将设计度量转换为像素单位，因为内部指标在设计单位中指定，像素大小表示1电磁尺（像素单位）。

### `int QRawFont::weight() const`

**作用与语义：**

还原了这`QRawFont`的重量。

### `qreal QRawFont::xHeight() const`

**作用与语义：**

返回该`QRawFont`的xHeight（像素单位）。
这通常但不总是等同于字符“x”的高度。

### `bool QRawFont::operator!=(const QRawFont &other) const`

**作用与语义：**

如果`QRawFont`不等于`other`，则返回`true`。否则，返回`false`。

### `QRawFont &QRawFont::operator=(const QRawFont &other)`

**作用与语义：**

分配`other`到这个`QRawFont`。

### `bool QRawFont::operator==(const QRawFont &other) const`

**作用与语义：**

如果该`QRawFont`等于`other`，则返回`true`。否则返回`false`。

### `[noexcept] size_t qHash(const QRawFont &key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `enum LayoutFlag { SeparateAdvances, KernedAdvances, UseDesignMetrics }`

**作用与语义：**

这个枚举告诉函数 `advancesForGlyphIndexes()` 如何计算前进量。
- `QRawFont::SeparateAdvances`: `0`; 将为每个字形单独计算前进量。
- `QRawFont::KernedAdvances`: `1`; 在相邻字形之间应用字距调整。请注意，目前不支持基于 OpenType GPOS 的字距调整。
- `QRawFont::UseDesignMetrics`: `2`; 使用设计指标而不是调整到绘图设备分辨率的提示指标。可以与上述任意选项进行或运算。
LayoutFlags 类型是 QFlags<LayoutFlag> 的一个 typedef。它存储 LayoutFlag 值的或组合。

### `flags LayoutFlags`

**作用与语义：**

这个枚举告诉函数 `advancesForGlyphIndexes()` 如何计算前进量。
- `QRawFont::SeparateAdvances`: `0`; 将为每个字形单独计算前进量。
- `QRawFont::KernedAdvances`: `1`; 在相邻字形之间应用字距调整。请注意，目前不支持基于 OpenType GPOS 的字距调整。
- `QRawFont::UseDesignMetrics`: `2`; 使用设计指标而不是调整到绘图设备分辨率的提示指标。可以与上述任意选项进行或运算。
LayoutFlags 类型是 QFlags<LayoutFlag> 的一个 typedef。它存储 LayoutFlag 值的或组合。

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

`QRawFont` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
