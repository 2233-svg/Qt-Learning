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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 51 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QRawFont::AntialiasingType`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QRawFont` 暴露的类型声明 `Antialiasing、类型`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:AntialiasingType`。
- 属性名：`QRawFont`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QRawFont::LayoutFlagflags QRawFont::LayoutFlags`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QRawFont` 暴露的类型声明 `Layout、Flagflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:LayoutFlagflags QRawFont::LayoutFlags`。
- 属性名：`QRawFont`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRawFont::QRawFont()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QRawFont` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRawFont::QRawFont(const QByteArray &fontData, qreal pixelSize, QFont::HintingPreference hintingPreference = QFont::PreferDefaultHinting)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QRawFont` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `fontData`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `pixelSize`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `hintingPreference`：类型为 `QFont::HintingPreference`。默认值为 `QFont::PreferDefaultHinting`。传入 `QFont::HintingPreference` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRawFont::QRawFont(const QString &fileName, qreal pixelSize, QFont::HintingPreference hintingPreference = QFont::PreferDefaultHinting)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QRawFont` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `fileName`：类型为 `const QString &`。没有默认值，调用时必须提供。文件名或路径。优先使用 Qt 的路径 API 拼接和规范化，不要手写平台分隔符。
- 参数 `pixelSize`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `hintingPreference`：类型为 `QFont::HintingPreference`。默认值为 `QFont::PreferDefaultHinting`。传入 `QFont::HintingPreference` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRawFont::QRawFont(const QRawFont &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QRawFont` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `const QRawFont &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QRawFont::~QRawFont()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QRawFont` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QPointF> QRawFont::advancesForGlyphIndexes(const QList<quint32> &glyphIndexes, QRawFont::LayoutFlags layoutFlags) const`

**API 类别：** 成员函数说明

**中文解读：** `QRawFont::advancesForGlyphIndexes` 用于计算、查询或取得与“advances、For、Glyph、Indexes”相关的操作。调用时要先确认当前状态和 `glyphIndexes`、`layoutFlags` 的有效范围；返回类型是 `QList<QPointF>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QPointF>`。
- 参数 `glyphIndexes`：类型为 `const QList<quint32> &`。没有默认值，调用时必须提供。传入 `const QList<quint32> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `layoutFlags`：类型为 `QRawFont::LayoutFlags`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QRawFont::advancesForGlyphIndexes(const quint32 *glyphIndexes, QPointF *advances, int numGlyphs, QRawFont::LayoutFlags layoutFlags) const`

**API 类别：** 成员函数说明

**中文解读：** `QRawFont::advancesForGlyphIndexes` 用于计算、查询或取得与“advances、For、Glyph、Indexes”相关的操作。调用时要先确认当前状态和 `glyphIndexes`、`advances`、`numGlyphs`、`layoutFlags` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `glyphIndexes`：类型为 `const quint32 *`。没有默认值，调用时必须提供。传入 `const quint32 *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `advances`：类型为 `QPointF *`。没有默认值，调用时必须提供。传入 `QPointF *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `numGlyphs`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `layoutFlags`：类型为 `QRawFont::LayoutFlags`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QPointF> QRawFont::advancesForGlyphIndexes(const QList<quint32> &glyphIndexes) const`

**API 类别：** 成员函数说明

**中文解读：** `QRawFont::advancesForGlyphIndexes` 用于计算、查询或取得与“advances、For、Glyph、Indexes”相关的操作。调用时要先确认当前状态和 `glyphIndexes` 的有效范围；返回类型是 `QList<QPointF>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QPointF>`。
- 参数 `glyphIndexes`：类型为 `const QList<quint32> &`。没有默认值，调用时必须提供。传入 `const QList<quint32> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QRawFont::advancesForGlyphIndexes(const quint32 *glyphIndexes, QPointF *advances, int numGlyphs) const`

**API 类别：** 成员函数说明

**中文解读：** `QRawFont::advancesForGlyphIndexes` 用于计算、查询或取得与“advances、For、Glyph、Indexes”相关的操作。调用时要先确认当前状态和 `glyphIndexes`、`advances`、`numGlyphs` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `glyphIndexes`：类型为 `const quint32 *`。没有默认值，调用时必须提供。传入 `const quint32 *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `advances`：类型为 `QPointF *`。没有默认值，调用时必须提供。传入 `QPointF *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `numGlyphs`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QImage QRawFont::alphaMapForGlyph(quint32 glyphIndex, QRawFont::AntialiasingType antialiasingType = SubPixelAntialiasing, const QTransform &transform = QTransform()) const`

**API 类别：** 成员函数说明

**中文解读：** `QRawFont::alphaMapForGlyph` 用于计算、查询或取得与“alpha、映射、For、Glyph”相关的操作。调用时要先确认当前状态和 `glyphIndex`、`antialiasingType`、`transform` 的有效范围；返回类型是 `QImage`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QImage`。
- 参数 `glyphIndex`：类型为 `quint32`。没有默认值，调用时必须提供。传入 `quint32` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `antialiasingType`：类型为 `QRawFont::AntialiasingType`。默认值为 `SubPixelAntialiasing`。传入 `QRawFont::AntialiasingType` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `transform`：类型为 `const QTransform &`。默认值为 `QTransform()`。传入 `const QTransform &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal QRawFont::ascent() const`

**API 类别：** 成员函数说明

**中文解读：** `QRawFont::ascent` 用于计算、查询或取得与“ascent”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal QRawFont::averageCharWidth() const`

**API 类别：** 成员函数说明

**中文解读：** `QRawFont::averageCharWidth` 用于计算、查询或取得与“average、Char、宽度”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRectF QRawFont::boundingRect(quint32 glyphIndex) const`

**API 类别：** 成员函数说明

**中文解读：** `QRawFont::boundingRect` 用于计算、查询或取得与“bounding、Rect”相关的操作。调用时要先确认当前状态和 `glyphIndex` 的有效范围；返回类型是 `QRectF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRectF`。
- 参数 `glyphIndex`：类型为 `quint32`。没有默认值，调用时必须提供。传入 `quint32` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal QRawFont::capHeight() const`

**API 类别：** 成员函数说明

**中文解读：** `QRawFont::capHeight` 用于计算、查询或取得与“cap、高度”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal QRawFont::descent() const`

**API 类别：** 成员函数说明

**中文解读：** `QRawFont::descent` 用于计算、查询或取得与“descent”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QRawFont::familyName() const`

**API 类别：** 成员函数说明

**中文解读：** `QRawFont::familyName` 用于计算、查询或取得与“family、名称”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.7] QByteArray QRawFont::fontTable(QFont::Tag tag) const`

**API 类别：** 成员函数说明

**中文解读：** `QRawFont::fontTable` 用于计算、查询或取得与“字体、Table”相关的操作。调用时要先确认当前状态和 `tag` 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `tag`：类型为 `QFont::Tag`。没有默认值，调用时必须提供。传入 `QFont::Tag` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray QRawFont::fontTable(const char *tag) const`

**API 类别：** 成员函数说明

**中文解读：** `QRawFont::fontTable` 用于计算、查询或取得与“字体、Table”相关的操作。调用时要先确认当前状态和 `tag` 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `tag`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QRawFont QRawFont::fromFont(const QFont &font, QFontDatabase::WritingSystem writingSystem = QFontDatabase::Any)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromFont`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QRawFont`。
- 参数 `font`：类型为 `const QFont &`。没有默认值，调用时必须提供。传入 `const QFont &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `writingSystem`：类型为 `QFontDatabase::WritingSystem`。默认值为 `QFontDatabase::Any`。传入 `QFontDatabase::WritingSystem` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.11] quint32 QRawFont::glyphCount() const`

**API 类别：** 成员函数说明

**中文解读：** `QRawFont::glyphCount` 用于计算、查询或取得与“glyph、数量统计”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `quint32`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`quint32`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QRawFont::glyphIndexesForChars(const QChar *chars, int numChars, quint32 *glyphIndexes, int *numGlyphs) const`

**API 类别：** 成员函数说明

**中文解读：** `QRawFont::glyphIndexesForChars` 用于计算、查询或取得与“glyph、Indexes、For、Chars”相关的操作。调用时要先确认当前状态和 `chars`、`numChars`、`glyphIndexes`、`numGlyphs` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `chars`：类型为 `const QChar *`。没有默认值，调用时必须提供。传入 `const QChar *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `numChars`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `glyphIndexes`：类型为 `quint32 *`。没有默认值，调用时必须提供。传入 `quint32 *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `numGlyphs`：类型为 `int *`。没有默认值，调用时必须提供。传入 `int *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<quint32> QRawFont::glyphIndexesForString(const QString &text) const`

**API 类别：** 成员函数说明

**中文解读：** `QRawFont::glyphIndexesForString` 用于计算、查询或取得与“glyph、Indexes、For、字符串”相关的操作。调用时要先确认当前状态和 `text` 的有效范围；返回类型是 `QList<quint32>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<quint32>`。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.11] QString QRawFont::glyphName(quint32 glyphIndex) const`

**API 类别：** 成员函数说明

**中文解读：** `QRawFont::glyphName` 用于计算、查询或取得与“glyph、名称”相关的操作。调用时要先确认当前状态和 `glyphIndex` 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数 `glyphIndex`：类型为 `quint32`。没有默认值，调用时必须提供。传入 `quint32` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFont::HintingPreference QRawFont::hintingPreference() const`

**API 类别：** 成员函数说明

**中文解读：** `QRawFont::hintingPreference` 用于计算、查询或取得与“hinting、Preference”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QFont::HintingPreference`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QFont::HintingPreference`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QRawFont::isValid() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isValid`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal QRawFont::leading() const`

**API 类别：** 成员函数说明

**中文解读：** `QRawFont::leading` 用于计算、查询或取得与“leading”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal QRawFont::lineThickness() const`

**API 类别：** 成员函数说明

**中文解读：** `QRawFont::lineThickness` 用于计算、查询或取得与“行、Thickness”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRawFont::loadFromData(const QByteArray &fontData, qreal pixelSize, QFont::HintingPreference hintingPreference)`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `loadFromData`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`void`。
- 参数 `fontData`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `pixelSize`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `hintingPreference`：类型为 `QFont::HintingPreference`。没有默认值，调用时必须提供。传入 `QFont::HintingPreference` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRawFont::loadFromFile(const QString &fileName, qreal pixelSize, QFont::HintingPreference hintingPreference)`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `loadFromFile`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`void`。
- 参数 `fileName`：类型为 `const QString &`。没有默认值，调用时必须提供。文件名或路径。优先使用 Qt 的路径 API 拼接和规范化，不要手写平台分隔符。
- 参数 `pixelSize`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `hintingPreference`：类型为 `QFont::HintingPreference`。没有默认值，调用时必须提供。传入 `QFont::HintingPreference` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal QRawFont::maxCharWidth() const`

**API 类别：** 成员函数说明

**中文解读：** `QRawFont::maxCharWidth` 用于计算、查询或取得与“max、Char、宽度”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPainterPath QRawFont::pathForGlyph(quint32 glyphIndex) const`

**API 类别：** 成员函数说明

**中文解读：** `QRawFont::pathForGlyph` 用于计算、查询或取得与“path、For、Glyph”相关的操作。调用时要先确认当前状态和 `glyphIndex` 的有效范围；返回类型是 `QPainterPath`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPainterPath`。
- 参数 `glyphIndex`：类型为 `quint32`。没有默认值，调用时必须提供。传入 `quint32` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal QRawFont::pixelSize() const`

**API 类别：** 成员函数说明

**中文解读：** `QRawFont::pixelSize` 用于计算、查询或取得与“pixel、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRawFont::setPixelSize(qreal pixelSize)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPixelSize`。调用它会改变 `QRawFont` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `pixelSize`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFont::Style QRawFont::style() const`

**API 类别：** 成员函数说明

**中文解读：** `QRawFont::style` 用于计算、查询或取得与“style”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QFont::Style`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QFont::Style`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QRawFont::styleName() const`

**API 类别：** 成员函数说明

**中文解读：** `QRawFont::styleName` 用于计算、查询或取得与“style、名称”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QFontDatabase::WritingSystem> QRawFont::supportedWritingSystems() const`

**API 类别：** 成员函数说明

**中文解读：** `QRawFont::supportedWritingSystems` 用于计算、查询或取得与“supported、Writing、Systems”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<QFontDatabase::WritingSystem>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QFontDatabase::WritingSystem>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QRawFont::supportsCharacter(QChar character) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `supportsCharacter`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `character`：类型为 `QChar`。没有默认值，调用时必须提供。传入 `QChar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QRawFont::supportsCharacter(uint ucs4) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `supportsCharacter`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `ucs4`：类型为 `uint`。没有默认值，调用时必须提供。传入 `uint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] void QRawFont::swap(QRawFont &other)`

**API 类别：** 成员函数说明

**中文解读：** `QRawFont::swap` 用于执行与“swap”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `other`：类型为 `QRawFont &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal QRawFont::underlinePosition() const`

**API 类别：** 成员函数说明

**中文解读：** `QRawFont::underlinePosition` 用于计算、查询或取得与“underline、Position”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal QRawFont::unitsPerEm() const`

**API 类别：** 成员函数说明

**中文解读：** `QRawFont::unitsPerEm` 用于计算、查询或取得与“units、Per、Em”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QRawFont::weight() const`

**API 类别：** 成员函数说明

**中文解读：** `QRawFont::weight` 用于计算、查询或取得与“weight”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal QRawFont::xHeight() const`

**API 类别：** 成员函数说明

**中文解读：** `QRawFont::xHeight` 用于计算、查询或取得与“x、高度”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QRawFont::operator!=(const QRawFont &other) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QRawFont` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `other`：类型为 `const QRawFont &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRawFont &QRawFont::operator=(const QRawFont &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QRawFont` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QRawFont &`。
- 参数 `other`：类型为 `const QRawFont &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QRawFont::operator==(const QRawFont &other) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QRawFont` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `other`：类型为 `const QRawFont &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] size_t qHash(const QRawFont &key, size_t seed = 0)`

**API 类别：** 相关非成员函数

**中文解读：** `QRawFont::qHash` 用于计算、查询或取得与“q、Hash”相关的操作。调用时要先确认当前状态和 `key`、`seed` 的有效范围；返回类型是 `size_t`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`size_t`。
- 参数 `key`：类型为 `const QRawFont &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `seed`：类型为 `size_t`。默认值为 `0`。传入 `size_t` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum LayoutFlag { SeparateAdvances, KernedAdvances, UseDesignMetrics }`

**API 类别：** 公有类型

**中文解读：** 这是 `QRawFont` 暴露的类型声明 `Layout、Flag`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags LayoutFlags`

**API 类别：** 公有类型

**中文解读：** 这是 `QRawFont` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

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

`QRawFont` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
