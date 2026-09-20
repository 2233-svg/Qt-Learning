# Qt QRawFont 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QRawFont>`  
> 所属模块：`Qt6::Gui`  
> 继承：无  
> 定位：访问单个物理字体实例及其字形数据的低层值类型

## 1. 它解决什么问题

`QFont` 表示的是一个字体查询：应用提出“希望使用某个家族、样式、粗细和大小”，Qt 再根据平台字体库、字符集和字体回退机制选择实际字体。大多数用户界面只需要这种抽象，因此 `QFont` 通常更合适。

`QRawFont` 处理的是更低一层的问题：它代表某个具体物理字体在某个像素大小下的实例。应用可以从这个实例读取字体表、字形数量、字形轮廓、字形位图、字形 advance 和字体度量，也可以把字形索引与位置交给 `QGlyphRun` 和 `QPainter::drawGlyphRun()` 绘制。

因此，`QRawFont` 适用于“我必须知道 Qt 最终选中了哪一个物理字体，或者我必须直接操作 glyph index”的场景，而不是用于普通文本控件的字体设置。

## 2. 真实使用场景

### 2.1 自定义文本渲染和字形缓存

自定义排版引擎、代码编辑器、字幕渲染器或游戏文本系统可能需要缓存字形轮廓、alpha map 或 glyph advance。`QRawFont` 可以提供这些底层数据，`QGlyphRun` 则负责把字形索引和基线位置组织成可绘制的数据。

### 2.2 检查字体覆盖范围

字体选择器、文档导入工具或国际化检查工具可以使用 `supportsCharacter()` 检查某个物理字体是否有指定 Unicode 字符，也可以读取 `supportedWritingSystems()` 获取字体文件声明支持的书写系统。

### 2.3 读取 OpenType/TrueType 字体表

字体分析器、诊断工具和排版实验代码可以用 `fontTable()` 读取 `name`、`cmap`、`OS/2` 等 sfnt 表。返回的字节序遵循 sfnt 规范，是 Big Endian；这不是可以直接按本机整数布局强转的内存块。

### 2.4 复现 Qt 实际选择的字体

`QRawFont::fromFont()` 可以把 `QFont` 查询解析成 Qt 优先选择的物理字体，适合调试字体回退、查看最终家族和读取实际字形数据。但它可能比较昂贵，不应在每一帧或逐字符循环中调用。

## 3. 构建与包含

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

```cpp
#include <QRawFont>
```

qmake 工程使用：`QT += gui`。

如果 Qt 构建时禁用了 raw font 支持，相关 API 会被条件宏屏蔽；跨平台代码应确认目标 Qt 构建和后端是否提供该能力。Qt 6.11.1 文档明确列出的主要后端包括 Windows 的 GDI/DirectWrite、Linux 的 FreeType 以及 macOS 的 CoreText。

## 4. 最小可用示例

下面的例子把系统字体查询解析为物理字体，读取字符串对应的 cmap glyph index，再查询每个 glyph 的 advance。它适合说明 API 数据流；它没有实现完整文本 shaping。

```cpp
#include <QFontDatabase>
#include <QRawFont>
#include <QString>

QRawFont inspectSystemFont()
{
    const QFont query =
        QFontDatabase::systemFont(QFontDatabase::GeneralFont);
    return QRawFont::fromFont(query, QFontDatabase::Any);
}

void inspectText()
{
    const QRawFont font = inspectSystemFont();
    if (!font.isValid())
        return;

    const QString text = QStringLiteral("Qt");
    const QList<quint32> glyphIndexes = font.glyphIndexesForString(text);
    const QList<QPointF> advances =
        font.advancesForGlyphIndexes(glyphIndexes);

    Q_ASSERT(glyphIndexes.size() == advances.size());
    Q_ASSERT(font.glyphCount() == 0 || glyphIndexes.size() <= text.size());
}
```

这里的 `glyphIndexesForString()` 只按字体的 `cmap` 表把 Unicode 字符映射为 glyph index。它不会执行阿拉伯文、印度文字、连字、组合标记或 OpenType GPOS/GSUB 所需的完整 shaping。需要得到真正用于显示的字形序列和位置时，应使用 `QTextLayout`，再从 `glyphRuns()` 获取 `QGlyphRun`。

## 5. 建立正确的心智模型

### 5.1 `QFont` 是查询，`QRawFont` 是结果

`QFont` 可以描述一个并不存在于系统中的组合，例如某个家族、粗细和样式的请求。Qt 处理文本时可能选择另一个物理字体，甚至针对不同书写系统或字符使用回退字体。

`QRawFont` 表示一个具体的物理实例，包括：

- 实际家族名和样式名。
- 一个确定的像素大小。
- 一套底层 TrueType/OpenType 表。
- 根据该大小换算后的像素度量。
- 可用于 glyph 级绘制的字形数据。

一个 `QRawFont` 不能代表一段文本所有字符的最终字体回退结果。文本可能包含多个 `QRawFont` 对应的 glyph run。

### 5.2 从文件/数据加载不会注册字体

通过文件名、`QByteArray`、`loadFromFile()` 或 `loadFromData()` 得到的字体只供这个 `QRawFont` 使用，不会加入 `QFontDatabase`，也不会自动成为普通 `QFont` 选择的一部分。如果需求是把字体安装或注册到应用字体数据库，应研究 `QFontDatabase` 的字体注册 API，而不是把 `QRawFont` 当作注册操作。

输入文件或数据必须包含 TrueType 或 OpenType 字体。加载后应立即检查 `isValid()`；文件不存在、数据格式不符合要求或后端无法处理时，不要继续把结果当作有效字体。

### 5.3 隐式共享不等于可以跨线程使用

`QRawFont` 是隐式共享值类型，复制对象通常成本较低；但 Qt 文档规定，`QRawFont` 被视为属于构造它的线程。无论对象是通过构造函数、`loadFromFile()`、`loadFromData()` 还是其它路径获得，都应在同一线程使用。不要把它移动到另一个线程后继续调用；需要在目标线程重新创建字体实例。

这条规则也影响缓存设计：跨线程传递字体文件字节或字体描述信息，在目标线程重建 `QRawFont`，比直接跨线程传递一个已经创建的 `QRawFont` 更稳妥。

## 6. 枚举和布局语义

### 6.1 `AntialiasingType`

该枚举只控制 `alphaMapForGlyph()` 的栅格化方式：

- `PixelAntialiasing`：按完整像素计算字形覆盖率，返回 `QImage::Format_Indexed8`，每个像素保存不透明度。
- `SubPixelAntialiasing`：分别计算红、绿、蓝子像素覆盖率，普通非彩色字体返回 `QImage::Format_RGB32`。

如果底层字体是彩色字体，返回图像会包含渲染后的彩色字形，此时 `antialiasingType` 会被忽略。

### 6.2 `LayoutFlag` 和 `LayoutFlags`

这些标志只告诉 `advancesForGlyphIndexes()` 如何计算 advance：

- `SeparateAdvances = 0`：每个 glyph 独立计算 advance，不应用相邻 glyph 的 kerning。
- `KernedAdvances = 1`：尝试使用字体 TrueType `KERN` 表中的相邻字距调整。
- `UseDesignMetrics = 2`：使用设计度量，而不是按绘制设备分辨率调整后的 hinting 度量；可以与前两个选项之一按位或组合。

`KernedAdvances` 不等于完整 OpenType shaping。现代字体中的 GPOS kerning、连字、上下文替换和复杂脚本处理仍应交给 `QTextLayout` 等排版 API。

## 7. 字形数据的典型流程

如果确实需要手工操作 glyph，可以按以下顺序组织：

1. 获得并验证一个 `QRawFont`。
2. 通过 `QTextLayout::glyphRuns()` 获取已经 shaping 的 `QGlyphRun`，或者在确认文本很简单时使用 `glyphIndexesForString()`。
3. 使用 `rawFont()`、`glyphIndexes()` 和 `positions()` 读取字形与位置。
4. 需要轮廓时调用 `pathForGlyph()`；需要位图时调用 `alphaMapForGlyph()`。
5. 需要绘制时，把 `QGlyphRun` 传给 `QPainter::drawGlyphRun()`，不要只凭 glyph index 猜测文本布局。

如果使用 `QTextLayout`：

```cpp
QTextLayout layout(QStringLiteral("office"), QFont(QStringLiteral("serif"), 24));
layout.beginLayout();
QTextLine line = layout.createLine();
line.setLineWidth(500);
layout.endLayout();

const QList<QGlyphRun> runs = layout.glyphRuns();
for (const QGlyphRun &run : runs) {
    const QRawFont rawFont = run.rawFont();
    const QList<quint32> glyphs = run.glyphIndexes();
    const QList<QPointF> positions = run.positions();
    // glyphs 和 positions 已经来自成形后的布局。
}
```

这里的 `QGlyphRun` 位置是每个 glyph 的基线位置，不是简单地把 advance 累加就一定能得到的结果。连字、双向文字、组合标记和上下文替换都可能让“字符数量、glyph 数量、位置数量”不再一一对应。

## 8. 度量、单位和有效性

### 8.1 像素单位与设计单位

`pixelSize()`、`ascent()`、`descent()`、`leading()`、`capHeight()`、`xHeight()`、字符宽度以及 glyph advance 等主要返回逻辑像素单位。`unitsPerEm()` 返回字体内部的设计单位数量，是把设计度量换算到像素度量时使用的基准。

不要把 `unitsPerEm()` 当成当前字体的像素高度，也不要把已经是像素单位的 `ascent()` 再乘一次 `pixelSize()`。

### 8.2 全局度量不保证覆盖所有实际字形

`ascent()` 和 `descent()` 是字体度量，通常可用于行布局，但少数字体的极端重音或异国字符可能超出设计者提供的常规范围。需要确保某个具体 glyph 不被裁剪时，使用 `boundingRect(glyphIndex)` 检查实际轮廓边界。

`capHeight()` 指平直大写字母的高度，不应拿圆形或尖形大写字母的视觉外框直接验证它；`xHeight()` 也经常但不总是等于字符 `x` 的高度。

### 8.3 无效对象和 glyph index

默认构造的 `QRawFont` 无效。对无效对象读取字形、轮廓或位图没有有意义的结果：例如 `pathForGlyph()` 返回空路径，`alphaMapForGlyph()` 返回无效图像。进入字形查询前先检查 `isValid()`；Qt 6.11.1 可用 `glyphCount()` 检查 glyph index 是否落在 `[0, glyphCount())` 范围内。

## 9. 常见错误与排查

### 用 `QRawFont` 替代普通 `QFont`

如果只是给 `QPainter`、`QWidget` 或文本控件设置字体，使用 `QFont`。`QRawFont` 暴露的是底层字体文件和 glyph 数据，调用复杂、平台依赖更明显，而且不会自动完成字体回退。

### 把字符映射当作文本成形

`glyphIndexesForString()` 读取 `cmap` 映射，不会处理连字、重排、组合标记或复杂脚本。发现阿拉伯文、印地文、泰文、emoji 序列或带连字的拉丁文本显示异常时，先改用 `QTextLayout` 获取 glyph runs。

### 在高频路径调用 `fromFont()`

`fromFont()` 可能执行字体匹配，是潜在的昂贵操作。应在配置变化时缓存结果，而不是在每个字符、每一帧或每次绘制回调中重新解析。

### 忽略加载结果

`loadFromFile()` 和 `loadFromData()` 返回 `void`，成功与否要通过后续的 `isValid()` 判断。加载新字体会替换当前对象代表的字体；不要以为失败时旧字体一定仍然可用，应用逻辑应在加载后重新验证状态。

### 把 `fontTable()` 当作本机结构体

字体表是二进制协议数据，表名必须是四个字符，返回数据为 sfnt 规定的 Big Endian。解析时应按字体格式逐字段读取并做长度检查，不能直接把 `QByteArray::constData()` 转成任意本机结构体。

### 用 `supportedWritingSystems()` 判断单个字符

该列表来自字体文件中的 OS/2 表所声明的 Unicode 范围和代码页范围，并不能保证某个具体 Unicode 点一定有 glyph。需要判断单个字符时使用 `supportsCharacter(QChar)` 或 `supportsCharacter(uint)`.

## 10. 逐项 API 说明

### `QRawFont::QRawFont()`

**作用：** 构造一个无效的 `QRawFont`。

**适用场景：** 先声明对象，稍后通过 `loadFromFile()` 或 `loadFromData()` 填充；也可作为“尚未加载字体”的明确状态。

**边界：** 构造后必须通过 `isValid()` 判断是否可以读取字体信息。无效对象不要传给依赖实际字体的字形绘制流程。

### `QRawFont::QRawFont(const QByteArray &fontData, qreal pixelSize, QFont::HintingPreference hintingPreference = QFont::PreferDefaultHinting)`

**作用：** 从内存中的 TrueType/OpenType 数据构造指定像素大小和 hinting 偏好的物理字体实例。

**注意：**

- `fontData` 必须包含可识别的 TrueType 或 OpenType 字体数据。
- 该字体不会注册到 `QFontDatabase`。
- 构造线程成为该 `QRawFont` 的线程归属。
- 构造后检查 `isValid()`；文档没有把所有输入错误统一映射成可抛出的异常。

### `QRawFont::QRawFont(const QString &fileName, qreal pixelSize, QFont::HintingPreference hintingPreference = QFont::PreferDefaultHinting)`

**作用：** 从文件加载 TrueType/OpenType 字体，并创建指定像素大小的物理字体实例。

**注意：** 文件路径、文件权限、文件格式和目标平台字体后端都会影响结果。该操作不把字体注册到系统或 Qt 字体数据库，且对象不能直接跨线程使用。

### `QRawFont::QRawFont(const QRawFont &other)`

**作用：** 复制另一个 `QRawFont` 的值。

**语义：** `QRawFont` 是隐式共享类型，复制通常只复制共享数据句柄；但这不改变线程归属约束，也不意味着复制出的对象可安全送到任意线程。

### `QRawFont::~QRawFont()`

**作用：** 销毁 `QRawFont` 值对象并释放其对共享字体数据的引用。

**注意：** 析构不会注销通过文件/数据加载的字体，因为该字体本来就没有注册到 `QFontDatabase`。不要在其它线程继续使用已销毁对象的副本或相关后端资源。

### `QList<QPointF> QRawFont::advancesForGlyphIndexes(const QList<quint32> &glyphIndexes) const`

**作用：** 返回 glyph 列表中每个 glyph 的独立 advance，结果单位为像素。

**边界：** 这是 `SeparateAdvances` 语义的便捷重载，不应用相邻字距调整。它不是文本总宽度的通用替代品，完整排版应使用 `QTextLayout` 或 `QFontMetricsF`。

### `QList<QPointF> QRawFont::advancesForGlyphIndexes(const QList<quint32> &glyphIndexes, QRawFont::LayoutFlags layoutFlags) const`

**作用：** 按 `layoutFlags` 计算并返回每个 glyph 的 advance。

**注意：** `KernedAdvances` 主要使用 TrueType `KERN` 表，不覆盖现代字体所有 GPOS/AAT 规则；`UseDesignMetrics` 可与其它选项组合。返回 advance 是从当前 glyph 位置到下一个 glyph 应放置位置的位移。

### `bool QRawFont::advancesForGlyphIndexes(const quint32 *glyphIndexes, QPointF *advances, int numGlyphs) const`

**作用：** 用指针数组批量计算独立 advance，结果写入调用方提供的 `advances` 数组。

**调用约束：**

- `glyphIndexes` 和 `advances` 都必须指向至少 `numGlyphs` 个元素。
- 调用方负责保证数组生命周期和可写性。
- `numGlyphs` 不应为负；对空数组应按项目需要单独处理。
- 返回值表示批量操作是否成功，不要只依赖输出数组内容。

### `bool QRawFont::advancesForGlyphIndexes(const quint32 *glyphIndexes, QPointF *advances, int numGlyphs, QRawFont::LayoutFlags layoutFlags) const`

**作用：** 指针数组版本的 advance 查询，可指定独立 advance、KERN 字距和设计度量选项。

**注意：** 数组长度、glyph index 有效性和线程归属都由调用方负责；需要完整 shaping 时不要把这个 API 当成排版引擎。

### `QImage QRawFont::alphaMapForGlyph(quint32 glyphIndex, QRawFont::AntialiasingType antialiasingType = SubPixelAntialiasing, const QTransform &transform = QTransform()) const`

**作用：** 按指定变换把 glyph 栅格化为图像。

**结果语义：**

- 无效字体返回无效 `QImage`。
- 普通字体使用 `PixelAntialiasing` 时通常得到 `Format_Indexed8` 不透明度图。
- 普通字体使用 `SubPixelAntialiasing` 时通常得到 `Format_RGB32` 子像素不透明度图。
- 彩色字体返回彩色 glyph 图像，并忽略 antialiasing 类型。
- `transform` 会影响栅格化结果，适合旋转、缩放等场景。

### `qreal QRawFont::ascent() const`

**作用：** 返回从基线到字体最高常规延伸位置的距离，单位为像素。

**边界：** 少数字体的极端字符可能超出该全局度量；需要具体 glyph 边界时使用 `boundingRect()`。

### `qreal QRawFont::averageCharWidth() const`

**作用：** 返回字体的平均字符宽度，单位为像素。

**注意：** 这是字体级估计值，不是任意字符串的实际排版宽度，也不包含复杂 shaping 后的上下文变化。

### `QRectF QRawFont::boundingRect(quint32 glyphIndex) const`

**作用：** 返回指定 glyph 轮廓的最小包围矩形。

**适用场景：** 绘制前做裁剪、碰撞或基线布局检查。调用前应验证字体有效和 glyph index 范围；矩形是 glyph 级结果，不等同于字符的 advance 范围。

### `qreal QRawFont::capHeight() const`

**作用：** 返回平直大写字母高出基线的高度，单位为像素。

**注意：** 它针对类似 H/I 的平直大写字母，圆形或尖形字母可能有 overshoot，不应据此推断所有大写 glyph 的外框高度。

### `qreal QRawFont::descent() const`

**作用：** 返回从基线到字体最低常规延伸位置的距离，单位为像素。

**边界：** 与 `ascent()` 一样，它是字体级度量，极少数实际 glyph 可能超出范围。

### `QString QRawFont::familyName() const`

**作用：** 返回这个物理字体实例的家族名。

**注意：** 这是实际字体信息，不是 `QFont` 查询中可能包含多个候选家族的列表。

### `[since 6.7] QByteArray QRawFont::fontTable(QFont::Tag tag) const`

**作用：** 按 `QFont::Tag` 读取底层 sfnt 字体表。

**结果与边界：**

- 表不存在时返回空 `QByteArray`。
- 返回字节序遵循 sfnt 规范，为 Big Endian。
- `QFont::Tag` 必须表达四字符表标签，例如 `QFont::Tag("name")`。
- API 从 Qt 6.7 开始提供。

### `QByteArray QRawFont::fontTable(const char *tag) const`

**作用：** 用四字符 C 字符串标签读取字体表。

**注意：** `tag` 必须是恰好四个字符的字符串，不是任意长度的表名；表不存在时返回空数组。解析返回数据时必须按字体表格式和 Big Endian 规则处理。

### `[static] QRawFont QRawFont::fromFont(const QFont &font, QFontDatabase::WritingSystem writingSystem = QFontDatabase::Any)`

**作用：** 根据 `QFont` 查询和指定书写系统，获取 Qt 将优先选择的物理字体。

**关键边界：**

- 这是静态工厂，不修改传入的 `QFont`。
- 该函数可能比较昂贵，不应放在性能敏感循环中。
- 返回的是一个书写系统对应的物理字体，不能保证覆盖输入文本的所有 Unicode 字符。
- 返回后仍应检查 `isValid()`。

### `[since 6.11] quint32 QRawFont::glyphCount() const`

**作用：** 返回该物理字体中的 glyph 数量。

**用途：** 在传给 `pathForGlyph()`、`alphaMapForGlyph()`、`boundingRect()` 或 `glyphName()` 前验证 glyph index 是否处于有效范围。

**版本：** 该函数从 Qt 6.11 开始提供。

### `bool QRawFont::glyphIndexesForChars(const QChar *chars, int numChars, quint32 *glyphIndexes, int *numGlyphs) const`

**作用：** 使用底层字体的 `cmap` 表，把一段 `QChar` 数组转换成 glyph index 数组。

**指针和容量规则：**

- `chars` 至少包含 `numChars` 个 `QChar`。
- `glyphIndexes` 的容量至少应为 `numChars`；如果转换仍需要更大容量，函数返回 `false`，并通过 `numGlyphs` 告知所需数量，以便调用方扩容后重试。
- `numGlyphs` 是输出参数，必须是有效的可写指针。
- 这是字符到 glyph 的映射，不执行完整 shaping。

### `QList<quint32> QRawFont::glyphIndexesForString(const QString &text) const`

**作用：** 使用字体 `cmap` 表把字符串转换成 glyph index 列表。

**关键边界：** 不处理会影响渲染的其它字体表和上下文规则。需要正确显示复杂脚本、连字或组合字符时，先用 `QTextLayout` 成形，再读取 `QGlyphRun`。

### `[since 6.11] QString QRawFont::glyphName(quint32 glyphIndex) const`

**作用：** 返回指定 glyph 的名称。

**注意：** 如果字体没有为该 glyph 提供显式名称，Qt 会根据 glyph index 合成一个名称；因此返回非空名称不一定代表字体文件中存在同名原始记录。该函数从 Qt 6.11 开始提供。

### `QFont::HintingPreference QRawFont::hintingPreference() const`

**作用：** 返回构造该 `QRawFont` 时使用的 hinting 偏好。

**注意：** 它反映字体实例的构造选项，不是动态修改底层平台字体后端的控制开关。

### `bool QRawFont::isValid() const`

**作用：** 判断当前 `QRawFont` 是否代表一个有效物理字体实例。

**使用习惯：** 默认构造、加载失败或不支持的字体后端都可能得到无效状态；在读取 glyph、度量和字体表之前先检查。

### `qreal QRawFont::leading() const`

**作用：** 返回字体的自然行间距，单位为像素。

**注意：** 它是字体提供的自然 inter-line spacing，不等于应用最终一定采用的段落行距。

### `qreal QRawFont::lineThickness() const`

**作用：** 返回与该字体文字一起绘制下划线、上划线等线条时建议使用的厚度。

**注意：** 这是度量建议值，不会自动绘制装饰线。

### `void QRawFont::loadFromData(const QByteArray &fontData, qreal pixelSize, QFont::HintingPreference hintingPreference)`

**作用：** 用内存中的 TrueType/OpenType 数据替换当前 `QRawFont`。

**边界：**

- 返回类型是 `void`，成功与否通过 `isValid()` 检查。
- 调用后当前对象代表新的字体，原先的字体状态不应继续假定存在。
- 字体不会注册到 `QFontDatabase`。
- 调用线程成为该对象后续使用的线程归属。

### `void QRawFont::loadFromFile(const QString &fileName, qreal pixelSize, QFont::HintingPreference hintingPreference)`

**作用：** 用文件中的 TrueType/OpenType 字体替换当前对象。

**边界：** 文件无法读取或格式不受支持时要重新检查 `isValid()`；这不是注册字体 API，也不保证应用中的 `QFont` 查询会找到该字体。

### `qreal QRawFont::maxCharWidth() const`

**作用：** 返回字体中最宽字符的宽度，单位为像素。

**注意：** 这是字体度量，不应当作某个具体 glyph 的轮廓宽度；字形外框和 advance 还应分别参考 `boundingRect()` 与 `advancesForGlyphIndexes()`。

### `QPainterPath QRawFont::pathForGlyph(quint32 glyphIndex) const`

**作用：** 返回指定 glyph 的矢量轮廓。

**结果语义：**

- 字体无效时返回空 `QPainterPath`。
- 返回的 glyph 始终是 unhinted 轮廓。
- 轮廓适合缩放、变换、路径布尔运算和自定义绘制，但不等于经过屏幕 hinting 后的实际像素结果。

### `qreal QRawFont::pixelSize() const`

**作用：** 返回当前字体实例的像素大小。

**影响：** 它影响 glyph 栅格化、`pathForGlyph()` 返回的轮廓大小，以及设计单位度量到逻辑像素的换算。

### `void QRawFont::setPixelSize(qreal pixelSize)`

**作用：** 设置后续渲染使用的像素大小。

**注意：** 修改后字体度量、glyph 路径和 alpha map 的结果都会随之变化；如果应用缓存了这些结果，应在尺寸变化时使缓存失效。应用应自行校验传入的尺寸，文档没有为所有非正常数值定义统一的业务语义。

### `QFont::Style QRawFont::style() const`

**作用：** 返回物理字体的样式枚举，例如正常、斜体或倾斜体。

**注意：** 这是字体实例报告的实际样式，不是对 glyph 轮廓进行后处理倾斜的操作。

### `QString QRawFont::styleName() const`

**作用：** 返回物理字体的样式名称。

**注意：** 名称来自字体实际信息，不能假设所有平台、字体文件和语言环境使用相同字符串。

### `QList<QFontDatabase::WritingSystem> QRawFont::supportedWritingSystems() const`

**作用：** 返回字体文件声明支持的书写系统列表。

**边界：** 列表依赖字体 OS/2 表中的 Unicode 范围和代码页范围；它不能保证某个具体 Unicode 点存在 glyph，单字符判断应使用 `supportsCharacter()`。

### `bool QRawFont::supportsCharacter(QChar character) const`

**作用：** 判断字体是否有与给定 `QChar` 对应的 glyph。

**注意：** 对 BMP 字符可以使用此重载；需要表达完整 UCS-4 代码点时使用 `supportsCharacter(uint)`，不要把代理项当作独立的 Unicode 字符判断。

### `bool QRawFont::supportsCharacter(uint ucs4) const`

**作用：** 判断字体是否有与给定 UCS-4 编码字符对应的 glyph。

**适用场景：** 检查 BMP 之外的 Unicode 字符，尤其是使用代理项表示的字符或较大的 Unicode 代码点。

### `void QRawFont::swap(QRawFont &other) noexcept`

**作用：** 交换两个 `QRawFont` 的值。

**语义：** 操作非常快且不会失败，适合实现高效的临时对象提交或容器重排；交换不会把对象变成可跨线程使用。

### `qreal QRawFont::underlinePosition() const`

**作用：** 返回相对于基线、用于在文字下方绘制下划线的位置，单位为像素。

**注意：** 返回的是位置建议，不会自动绘制下划线；实际装饰还应结合 `lineThickness()` 和应用的文本布局。

### `qreal QRawFont::unitsPerEm() const`

**作用：** 返回字体 em 方框使用的设计单位数量。

**注意：** 这是内部设计单位，不是像素值；它与 `pixelSize()` 一起用于把字体表中的设计度量换算为逻辑像素。

### `int QRawFont::weight() const`

**作用：** 返回物理字体的粗细值，语义与 `QFont::Weight` 对应。

**注意：** 返回的是字体实例报告的粗细，不会自动修改字体或模拟加粗。

### `qreal QRawFont::xHeight() const`

**作用：** 返回字体的 x-height，单位为像素。

**注意：** 它经常但不总是等于字符 `x` 的高度；不要用单个字形的视觉测量替代字体提供的度量。

### `bool QRawFont::operator==(const QRawFont &other) const`

**作用：** 比较两个 `QRawFont` 值是否相等。

**使用场景：** 判断字体状态是否变化，以决定是否重建 glyph 或度量缓存。比较值相等不表示两个对象必须拥有独立的底层数据，它们可能共享同一份隐式共享存储。

### `bool QRawFont::operator!=(const QRawFont &other) const`

**作用：** 判断两个 `QRawFont` 值是否不相等。

**注意：** 与 `operator==` 保持逻辑互补，适合在字体配置变化检测中使用。

### `QRawFont &QRawFont::operator=(const QRawFont &other)`

**作用：** 把 `other` 的字体值赋给当前对象。

**语义：** 赋值使用隐式共享值语义，当前对象原有的字体引用会被替换。线程归属约束仍然有效，不能用赋值把一个字体安全地“搬”到另一个线程。

### `size_t qHash(const QRawFont &key, size_t seed = 0) noexcept`

**作用：** 为 `QRawFont` 生成哈希值，以便用作 `QHash`/`QSet` 的键。

**注意：** 相等的 `QRawFont` 必须产生一致的哈希语义；如果缓存还依赖 glyph index、像素位置、变换或 shaping 状态，这些信息必须作为额外的缓存键组成部分。

## API 速查表

| 类别 | API | 解决什么问题 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QRawFont::QRawFont()` | 创建无效字体占位对象 | 使用前检查 `isValid()` |
| 构造 | `QRawFont::QRawFont(const QByteArray &fontData, qreal pixelSize, QFont::HintingPreference hintingPreference = QFont::PreferDefaultHinting)` | 从内存 TrueType/OpenType 数据创建物理字体实例 | 不注册字体；数据格式、像素大小和构造线程都重要 |
| 构造 | `QRawFont::QRawFont(const QString &fileName, qreal pixelSize, QFont::HintingPreference hintingPreference = QFont::PreferDefaultHinting)` | 从字体文件创建物理字体实例 | 文件必须是受支持的 TrueType/OpenType 字体；不注册到字体数据库 |
| 构造 | `QRawFont::QRawFont(const QRawFont &other)` | 复制字体值 | 隐式共享但仍按构造线程使用 |
| 析构 | `QRawFont::~QRawFont()` | 销毁字体值对象 | 不要在对象销毁后继续使用相关数据 |
| Advance | `QList<QPointF> advancesForGlyphIndexes(const QList<quint32> &glyphIndexes)` | 获取每个 glyph 的独立 advance | 默认是 `SeparateAdvances`，不是完整文本宽度 |
| Advance | `QList<QPointF> advancesForGlyphIndexes(const QList<quint32> &, LayoutFlags)` | 按布局标志计算 glyph advance | `KernedAdvances` 只覆盖有限的 KERN 规则；复杂 shaping 用 `QTextLayout` |
| Advance | `bool advancesForGlyphIndexes(const quint32 *, QPointF *, int)` | 用数组高效批量获取独立 advance | 两个数组至少有 `numGlyphs` 个元素，检查返回值 |
| Advance | `bool advancesForGlyphIndexes(const quint32 *, QPointF *, int, LayoutFlags)` | 用数组批量获取带布局选项的 advance | 指针容量、glyph index 和线程归属由调用方保证 |
| 栅格化 | `QImage alphaMapForGlyph(quint32, AntialiasingType, const QTransform &)` | 获取 glyph 的栅格图像 | 无效字体返回无效图像；彩色字体忽略抗锯齿类型 |
| 度量 | `qreal ascent()` | 获取字体上升部距离 | 字体级度量，极端 glyph 可能超出 |
| 度量 | `qreal averageCharWidth()` | 获取平均字符宽度 | 只是估计值，不是字符串实际排版宽度 |
| 几何 | `QRectF boundingRect(quint32 glyphIndex)` | 获取 glyph 的最小包围矩形 | 先验证 glyph index；不等于 advance 范围 |
| 度量 | `qreal capHeight()` | 获取平直大写字母高度 | 圆形/尖形字母可能有 overshoot |
| 度量 | `qreal descent()` | 获取字体下降部距离 | 字体级度量，极端 glyph 可能超出 |
| 元数据 | `QString familyName()` | 获取实际物理字体家族名 | 不等于 `QFont` 查询中的候选家族列表 |
| 字体表 | `[since 6.7] QByteArray fontTable(QFont::Tag tag)` | 按强类型标签读取 sfnt 表 | 不存在时为空；返回数据为 Big Endian |
| 字体表 | `QByteArray fontTable(const char *tag)` | 按四字符 C 字符串读取 sfnt 表 | 标签必须恰好四个字符，解析需做长度检查 |
| 工厂 | `[static] QRawFont fromFont(const QFont &, QFontDatabase::WritingSystem)` | 把字体查询解析为物理字体 | 可能昂贵；只代表一个选择结果，检查有效性 |
| 字形信息 | `[since 6.11] quint32 glyphCount()` | 获取字体中的 glyph 数量 | 用于验证 glyph index；Qt 6.11 新增 |
| 字符映射 | `bool glyphIndexesForChars(const QChar *, int, quint32 *, int *)` | 用数组把字符映射为 glyph index | `glyphIndexes` 可能需要扩容；`numGlyphs` 是输出参数；不做 shaping |
| 字符映射 | `QList<quint32> glyphIndexesForString(const QString &)` | 把字符串映射为 glyph index 列表 | 只使用 cmap；复杂文本使用 `QTextLayout` |
| 字形信息 | `[since 6.11] QString glyphName(quint32 glyphIndex)` | 获取 glyph 名称 | 没有显式名称时可能合成名称；Qt 6.11 新增 |
| 配置查询 | `QFont::HintingPreference hintingPreference()` | 查询构造字体时的 hinting 偏好 | 是实例信息，不是动态后端控制器 |
| 有效性 | `bool isValid()` | 检查字体是否有效 | 默认构造、加载失败后都必须先检查 |
| 度量 | `qreal leading()` | 获取自然行间距 | 不等于应用最终采用的段落行距 |
| 度量 | `qreal lineThickness()` | 获取文字装饰线建议厚度 | 只返回度量，不自动绘制装饰线 |
| 加载 | `void loadFromData(const QByteArray &, qreal, QFont::HintingPreference)` | 用内存数据替换当前字体 | 返回 `void`，加载后检查 `isValid()`；不注册字体 |
| 加载 | `void loadFromFile(const QString &, qreal, QFont::HintingPreference)` | 用文件内容替换当前字体 | 文件错误不会通过返回值报告；加载后重新验证 |
| 度量 | `qreal maxCharWidth()` | 获取最宽字符宽度 | 不等于具体 glyph 轮廓宽度或 advance |
| 轮廓 | `QPainterPath pathForGlyph(quint32 glyphIndex)` | 获取 glyph 的矢量轮廓 | 无效字体返回空路径；轮廓始终 unhinted |
| 配置查询 | `qreal pixelSize()` | 查询当前字体像素大小 | 影响路径、栅格化和设计度量换算 |
| 配置 | `void setPixelSize(qreal pixelSize)` | 修改字体像素大小 | 修改后应使路径、alpha map 和度量缓存失效 |
| 元数据 | `QFont::Style style()` | 查询实际字体样式 | 不会模拟斜体或改变 glyph |
| 元数据 | `QString styleName()` | 查询实际样式名称 | 字符串由字体文件/平台提供，不应硬编码比较 |
| 覆盖范围 | `QList<QFontDatabase::WritingSystem> supportedWritingSystems()` | 获取字体声明支持的书写系统 | 不能保证某个具体 Unicode 点有 glyph |
| 覆盖范围 | `bool supportsCharacter(QChar character)` | 检查一个 `QChar` 字符是否有 glyph | 完整 UCS-4 代码点使用 `uint` 重载 |
| 覆盖范围 | `bool supportsCharacter(uint ucs4)` | 检查 UCS-4 字符是否有 glyph | 适用于 BMP 之外的代码点 |
| 值操作 | `void swap(QRawFont &other) noexcept` | 高效交换两个字体值 | 快速且不失败；不改变线程约束 |
| 度量 | `qreal underlinePosition()` | 获取下划线相对基线的位置 | 只返回位置建议，不自动绘制 |
| 度量 | `qreal unitsPerEm()` | 获取字体 em 方框的设计单位数 | 是设计单位，不是像素；用于换算 |
| 元数据 | `int weight()` | 查询物理字体粗细 | 不会模拟加粗 |
| 度量 | `qreal xHeight()` | 获取字体 x-height | 不保证等于字符 `x` 的视觉高度 |
| 比较 | `bool operator==(const QRawFont &other)` | 比较字体值是否相等 | 可用于缓存失效判断；底层数据可能隐式共享 |
| 比较 | `bool operator!=(const QRawFont &other)` | 比较字体值是否不相等 | 与相等运算保持互补 |
| 赋值 | `QRawFont &operator=(const QRawFont &other)` | 替换当前字体值 | 不改变线程归属规则，不能借此跨线程迁移 |
| 哈希 | `size_t qHash(const QRawFont &key, size_t seed = 0) noexcept` | 用于 `QHash`/`QSet` 的键 | 其它 shaping、位置和变换信息需另行纳入缓存键 |

---

### 一句话总结

`QRawFont` 是访问具体物理字体和 glyph 数据的低层工具：用 `fromFont()` 或文件/数据加载得到有效实例，用 `glyphIndexesForString()` 做简单 cmap 查询，用 `QTextLayout` 获取复杂文本的真实 shaping，再结合 `QGlyphRun`、`pathForGlyph()`、`alphaMapForGlyph()` 和字体度量完成自定义渲染；普通字体设置仍应优先使用 `QFont`。
