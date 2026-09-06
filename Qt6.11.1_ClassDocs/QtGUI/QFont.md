# QFont

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 字体描述类型，包含家族、大小、粗体、斜体等属性。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QFont`：字体描述类型，包含家族、大小、粗体、斜体等属性。

**内部模型：** 绘制对象维护一组状态：画笔、画刷、字体、变换、裁剪、合成模式和渲染提示。每次 draw 调用都会使用当前状态；坐标通常经过当前 transform 映射到目标设备。

**适用场景：** 开始绘制后配置必要状态，使用 save/restore 包围局部变换，按设备坐标绘制，结束时让上下文析构或调用 end。绘制文本和图片时同时考虑字体度量、devicePixelRatio、裁剪和性能。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要直接调用 paintEvent；不要在绘制函数里修改会再次触发绘制的状态；不要假定所有图像都是四字节像素；不要忘记 transform 会影响坐标和 boundingRect。

## 2. 依赖与对象关系

- 头文件：`#include <QFont>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

绘制对象维护一组状态：画笔、画刷、字体、变换、裁剪、合成模式和渲染提示。每次 draw 调用都会使用当前状态；坐标通常经过当前 transform 映射到目标设备。

### 状态、生命周期和线程

**生命周期：** 绘制上下文必须绑定有效的 paint device，并在合法的绘制阶段使用。QWidget 上通常只在 `paintEvent()` 内创建 painter；离屏图像、打印设备和 pixmap 则有各自的设备生命周期。

**状态与结果：** `save()`/`restore()` 用于隔离局部状态；改变坐标系、画笔或合成模式后要么恢复，要么明确后续绘制也需要该状态。重绘请求和真正绘制是两个阶段，业务状态变化应调用 `update()`。

**线程与事件循环：** 同一个 GUI 控件的绘制在 GUI 线程完成；离屏 QImage 可以按数据所有权在后台处理，但不要让后台线程直接绘制或访问正在显示的 QWidget/QPixmap 资源。

## 3. 直接使用

开始绘制后配置必要状态，使用 save/restore 包围局部变换，按设备坐标绘制，结束时让上下文析构或调用 end。绘制文本和图片时同时考虑字体度量、devicePixelRatio、裁剪和性能。 使用时通常按这个过程组织：构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

```cpp
void Widget::paintEvent(QPaintEvent *)
{
    QPainter painter(this);
    painter.save();
    // 设置画笔、画刷、字体或变换后进行绘制
    painter.restore();
}
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `(since 6.7) struct Tag`
- `enum Capitalization { MixedCase, AllUppercase, AllLowercase, SmallCaps, Capitalize }`
- `enum HintingPreference { PreferDefaultHinting, PreferNoHinting, PreferVerticalHinting, PreferFullHinting }`
- `enum SpacingType { PercentageSpacing, AbsoluteSpacing }`
- `enum Stretch { AnyStretch, UltraCondensed, ExtraCondensed, Condensed, SemiCondensed, …, UltraExpanded }`
- `enum Style { StyleNormal, StyleItalic, StyleOblique }`
- `enum StyleHint { AnyStyle, SansSerif, Helvetica, Serif, Times, …, System }`
- `enum StyleStrategy { PreferDefault, PreferBitmap, PreferDevice, PreferOutline, ForceOutline, …, PreferQuality }`
- `enum Weight { Thin, ExtraLight, Light, Normal, Medium, …, Black }`

### 公有函数

- `QFont()`
- `QFont(const QFont &font, const QPaintDevice *pd)`
- `QFont(const QString &family, int pointSize = -1, int weight = -1, bool italic = false)`
- `QFont(const QStringList &families, int pointSize = -1, int weight = -1, bool italic = false)`
- `QFont(const QFont &font)`
- `~QFont()`
- `bool bold() const`
- `QFont::Capitalization capitalization() const`
- `(since 6.7) void clearFeatures()`
- `(since 6.7) void clearVariableAxes()`
- `QString defaultFamily() const`
- `bool exactMatch() const`
- `QStringList families() const`
- `QString family() const`
- `(since 6.7) QList<QFont::Tag> featureTags() const`
- `(since 6.7) quint32 featureValue(QFont::Tag tag) const`
- `bool fixedPitch() const`
- `bool fromString(const QString &descrip)`
- `QFont::HintingPreference hintingPreference() const`
- `bool isCopyOf(const QFont &f) const`
- `(since 6.7) bool isFeatureSet(QFont::Tag tag) const`
- `(since 6.7) bool isVariableAxisSet(QFont::Tag tag) const`
- `bool italic() const`
- `bool kerning() const`
- `QString key() const`
- `qreal letterSpacing() const`
- `QFont::SpacingType letterSpacingType() const`
- `bool overline() const`
- `int pixelSize() const`
- `int pointSize() const`
- `qreal pointSizeF() const`
- `QFont resolve(const QFont &other) const`
- `void setBold(bool enable)`
- `void setCapitalization(QFont::Capitalization caps)`
- `void setFamilies(const QStringList &families)`
- `void setFamily(const QString &family)`
- `(since 6.7) void setFeature(QFont::Tag tag, quint32 value)`
- `void setFixedPitch(bool enable)`
- `void setHintingPreference(QFont::HintingPreference hintingPreference)`
- `void setItalic(bool enable)`
- `void setKerning(bool enable)`
- `void setLetterSpacing(QFont::SpacingType type, qreal spacing)`
- `void setOverline(bool enable)`
- `void setPixelSize(int pixelSize)`
- `void setPointSize(int pointSize)`
- `void setPointSizeF(qreal pointSize)`
- `void setStretch(int factor)`
- `void setStrikeOut(bool enable)`
- `void setStyle(QFont::Style style)`
- `void setStyleHint(QFont::StyleHint hint, QFont::StyleStrategy strategy = PreferDefault)`
- `void setStyleName(const QString &styleName)`
- `void setStyleStrategy(QFont::StyleStrategy s)`
- `void setUnderline(bool enable)`
- `(since 6.7) void setVariableAxis(QFont::Tag tag, float value)`
- `void setWeight(QFont::Weight weight)`
- `void setWordSpacing(qreal spacing)`
- `int stretch() const`
- `bool strikeOut() const`
- `QFont::Style style() const`
- `QFont::StyleHint styleHint() const`
- `QString styleName() const`
- `QFont::StyleStrategy styleStrategy() const`
- `void swap(QFont &other)`
- `QString toString() const`
- `bool underline() const`
- `(since 6.7) void unsetFeature(QFont::Tag tag)`
- `(since 6.7) void unsetVariableAxis(QFont::Tag tag)`
- `(since 6.7) QList<QFont::Tag> variableAxisTags() const`
- `(since 6.7) float variableAxisValue(QFont::Tag tag) const`
- `QFont::Weight weight() const`
- `qreal wordSpacing() const`
- `operator QVariant() const`
- `bool operator!=(const QFont &f) const`
- `bool operator<(const QFont &f) const`
- `QFont & operator=(QFont &&other)`
- `QFont & operator=(const QFont &font)`
- `bool operator==(const QFont &f) const`

### 静态公有成员

- `void insertSubstitution(const QString &familyName, const QString &substituteName)`
- `void insertSubstitutions(const QString &familyName, const QStringList &substituteNames)`
- `void removeSubstitutions(const QString &familyName)`
- `QString substitute(const QString &familyName)`
- `QStringList substitutes(const QString &familyName)`
- `QStringList substitutions()`

### 相关非成员函数

- `size_t qHash(const QFont &key, size_t seed = 0)`
- `QDataStream & operator<<(QDataStream &s, const QFont &font)`
- `QDataStream & operator>>(QDataStream &s, QFont &font)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QFont::Capitalization`

**作用与语义：**

适用于该字体的文本渲染选项。
- `QFont::MixedCase`：`0`;这是正常的文本渲染选项，不应用大写变化。
- `QFont::AllUppercase`：`1`;这会将文本全部大写字母渲染。
- `QFont::AllLowercase`：`2`;这会将文本全部改为小写字母。
- `QFont::SmallCaps`：`3`;这会将文本改为小写字体。
- `QFont::Capitalize`：`4`;这会将每个单词的第一个字符作为大写字母来表示。

### `enum QFont::HintingPreference`

**作用与语义：**

这个枚举描述了可以应用于字形的不同提示等级，以在像素密度可能需要的显示屏上提高可读性。
- `QFont::PreferDefaultHinting`: `0`; 使用目标平台的默认提示等级。
- `QFont::PreferNoHinting`: `1`; 如果可能，在渲染文本时不对字形轮廓进行提示。文本布局将保持排版准确且可缩放，使用与打印时相同的度量。
- `QFont::PreferVerticalHinting`: `2`; 如果可能，渲染文本时不应用水平提示，但在垂直方向上将字形对齐到像素网格。对于像素密度过低而无法准确呈现字形的显示屏，文本将显得更清晰。但由于字形的水平度量未进行提示，文本布局可以缩放到更高密度的设备（例如打印机）而不影响行间断等细节。
- `QFont::PreferFullHinting`: `3`; 如果可能，渲染文本时在水平和垂直方向都使用提示。文本将被调整以优化目标设备上的可读性，但由于度量依赖于文本的目标大小，字形位置、换行和其他排版细节不会缩放，这意味着在不同像素密度的设备上，文本布局可能看起来不同。
请注意，此枚举仅描述偏好，因为并非所有 Qt 支持的平台都支持完整范围的提示等级。下表列出了在选定目标平台上给定提示偏好的效果。
- ``: PreferDefaultHinting; PreferNoHinting; PreferVerticalHinting; PreferFullHinting
- `Windows and DirectWrite enabled in Qt`: 完全提示; 垂直提示; 垂直提示; 完全提示
- `FreeType`: 操作系统设置; 不提示; 垂直提示（轻度）; 完全提示
- `Cocoa on macOS`: 不提示; 不提示; 不提示; 不提示

### `enum QFont::Stretch`

**作用与语义：**

遵循CSS命名规范的预定义拉伸值。值越高，文本拉伸越多。
- `QFont::AnyStretch (since Qt 5.8)`：`0`;0 接受任何用其他`QFont`属性匹配的拉伸
- `QFont::UltraCondensed`：`50`;50
- `QFont::ExtraCondensed`：`62`;62
- `QFont::Condensed`：`75`;75
- `QFont::SemiCondensed`：`87`;87
- `QFont::Unstretched`：`100`;100
- `QFont::SemiExpanded`：`112`;112
- `QFont::Expanded`：`125`;125
- `QFont::ExtraExpanded`：`150`;150
- `QFont::UltraExpanded`：`200`;200

### `enum QFont::Style`

**作用与语义：**

本枚举描述了用于显示文本的不同字形样式。
- `QFont::StyleNormal`：`0`;无样式文本中使用的普通字形。
- `QFont::StyleItalic`：`1`;专为表示斜体文本设计的斜体字形。
- `QFont::StyleOblique`：`2`;带有斜体外观的字形，通常基于未样式化的字形，但未经过微调以表示斜体文本。

### `enum QFont::StyleHint`

**作用与语义：**

样式提示被字体匹配算法用于在选定字体族不可用时找到合适的默认族。
- `QFont::AnyStyle`：`5`;由字体匹配算法选择族。这是默认。
- `QFont::SansSerif`：`Helvetica`;字体匹配器偏好无衬线字体。
- `QFont::Helvetica`：`0`;是`SansSerif`的同义词。
- `QFont::Serif`：`Times`;字体匹配器偏好衬线字体。
- `QFont::Times`：`1`;是`Serif`的同义词。
- `QFont::TypeWriter`：`Courier`;字体匹配器偏好固定音高字体。
- `QFont::Courier`：`2`;`TypeWriter`的同义词。
- `QFont::OldEnglish`：`3`;字体匹配器偏好装饰性字体。
- `QFont::Decorative`：`OldEnglish`;是`OldEnglish`的同义词。
- `QFont::Monospace`：`7`;字体匹配器偏好映射到 CSS 通用字体家族“单空间”的字体。
- `QFont::Fantasy`：`8`;字体匹配器偏好映射到 CSS 通用字体家族“幻想”字体。
- `QFont::Cursive`：`6`;字体匹配器偏好映射到 CSS 通用字体家族“连笔体”的字体。
- `QFont::System`：`4`;字体匹配器偏好系统字体。

### `enum QFont::StyleStrategy`

**作用与语义：**

样式策略告诉字体匹配算法应使用哪种字体，以找到合适的默认字体族。
以下策略可供选择：
- `QFont::PreferDefault`：`0x0001`;默认样式策略。它不偏好任何类型的字体。
- `QFont::PreferBitmap`：`0x0002`;偏好位图字体（而非轮廓字体）。
- `QFont::PreferDevice`：`0x0004`;偏好设备字体。
- `QFont::PreferOutline`：`0x0008`;偏好轮廓字体（而非位图字体）。
- `QFont::ForceOutline`：`0x0010`;强制使用轮廓字体。
- `QFont::NoAntialias`：`0x0100`;不要对字体进行抗锯齿。
- `QFont::NoSubpixelAntialias`：`0x0800`;尽量避免字体上的子像素抗锯齿。
- `QFont::PreferAntialias`：`0x0080`;如果可能，则采用抗锯齿。
- `QFont::ContextFontMerging (since Qt 6.8)`：`0x2000`;如果所选字体不含某个字符，Qt会自动选择一个外观相似且包含该字符的备用字体。默认情况下，这会以字符为单位进行。这意味着在某些罕见情况下，即使同一文字体，也可能使用多个字体来表示同一字符串。设置`ContextFontMerging`会尝试找到与输入字符串最大子集匹配的备回字体。对于缺少字形的字符串，这会更昂贵，但可能带来更一致的结果。如果设置了`NoFontMerging`，则`ContextFontMerging`不会有影响。
- `QFont::PreferTypoLineMetrics (since Qt 6.8)`：`0x4000`;出于兼容性考虑，OpenType 字体包含两组竞争的垂直行度量，分别提供字体的 4 `ascent`、`descent` 和 `leading`。这些指标通常被称为 win（Windows）度量和错别字（排版）度量。虽然规范建议使用 `typo` 度量来控制行距，但许多应用程序更倾向于使用`win`度量，除非字体的 fsSelection 字段中设置了 `USE_TYPO_METRICS` 标志。出于向后兼容性的原因，Qt 应用同样如此。对于设置 `USE_TYPO_METRICS` 标志以表示 `typo` 指标有效性的字体来说，这个问题不存在;对于 `win` 指标和 `typo` 指标匹配的字体也不是问题。然而，对于某些字体，`win` 指标可能大于理想行距，`USE_TYPO_METRICS` 标志可能会因误置而被取消。对于此类字体，设置 `PreferTypoLineMetrics` 可能带来更好的效果。
- `QFont::NoFontMerging`：`0x8000`;如果为某书写系统选择的字体不包含被要求绘制的字符，Qt会自动选择一个外观相似且包含该字符的字体。NoFontMerge标志会禁用该功能。请注意，启用该标志并不会阻止Qt在所选字体不支持文本书写系统时自动选择合适的字体。
- `QFont::PreferNoShaping`：`0x1000`;有时，字体会对一组字符应用复杂规则以正确显示它们。在某些书写系统中，如婆罗米字母，为了使文本可读，这是必要的，但在例如拉丁字母中，这只是一个装饰性特征。PreferNoShaping 标志会在不需要时禁用所有此类功能，这在大多数情况下会提升性能（自第5.10个Q以来）。
这些中的任何一个都可以用以下之一的标志进行运筹码：
- `QFont::PreferMatch`：`0x0020`;偏好完全匹配。字体匹配器会尝试使用指定的精确字体大小。
- `QFont::PreferQuality`：`0x0040`;偏好最优质的字体。字体匹配器将使用字体支持的最接近标准点大小。

### `enum QFont::Weight`

**作用与语义：**

Qt使用1到1000的权重刻度，兼容OpenType。1的权重表示薄，1000则极为黑色。
该枚举包含预定义的字体权重：
- `QFont::Thin`：`100`;100
- `QFont::ExtraLight`：`200`;200
- `QFont::Light`：`300`;300
- `QFont::Normal`：`400`;400
- `QFont::Medium`：`500`;500
- `QFont::DemiBold`：`600`;600
- `QFont::Bold`：`700`;700
- `QFont::ExtraBold`：`800`;800
- `QFont::Black`：`900`;900

### `QFont::QFont()`

**作用与语义：**

构建一个使用应用程序默认字体的字体对象。

### `QFont::QFont(const QFont &font, const QPaintDevice *pd)`

**作用与语义：**

从`font`构建字体用于绘画设备`pd`。

### `QFont::QFont(const QString &family, int pointSize = -1, int weight = -1, bool italic = false)`

**作用与语义：**

构建具有指定`family`、`pointSize`、`weight`和 `italic`设置的字体对象。
如果`pointSize`为零或负数，字体点数设置为系统相关的默认值。通常为12点。
`family`名称也可以选择性地包含铸造厂名称，例如“Helvetica [Cronyx]”。如果`family`来自多个铸造厂且未指定铸造厂，则选择任意代工厂。如果该代字厂不可用，则通过字体匹配算法设置代字厂。
这样会将族字符串分割为逗号，并用结果列表调用`setFamilies()`。要保留带有逗号的字体，请使用取`QStringList`的构造器。

### `[explicit] QFont::QFont(const QStringList &families, int pointSize = -1, int weight = -1, bool italic = false)`

**作用与语义：**

构建具有指定 `families`、`pointSize`、`weight` 和 `italic` 设置的字体对象。
如果`pointSize`为零或负数，字体点大小将设置为系统相关的默认值。通常为12个点。
`families` 中的每个族名条目还可以选择包含铸造厂名称，例如“Helvetica [Cronyx]”。如果该族群来自多个铸造厂且未指定铸造厂，则选择任意铸造厂。如果族群不可用，则通过字体匹配算法设置一个族。

### `QFont::QFont(const QFont &font)`

**作用与语义：**

构建了一种仿`font`字体。

### `[noexcept] QFont::~QFont()`

**作用与语义：**

销毁字体对象并释放所有分配的资源。

### `bool QFont::bold() const`

**作用与语义：**

如果 `weight()` 大于 `QFont::Medium`，则返回`true`;否则返回 `false`。

### `QFont::Capitalization QFont::capitalization() const`

**作用与语义：**

返回字体当前的大写类型。

### `[since 6.7] void QFont::clearFeatures()`

**作用与语义：**

清除`QFont`上之前设置的功能。
有关字体功能的更多细节，请参见 `setFeature()`。

### `[since 6.7] void QFont::clearVariableAxes()`

**作用与语义：**

清除`QFont`上之前设置的可变轴值。
关于变轴的更多细节请参见`setVariableAxis()`。

### `QString QFont::defaultFamily() const`

**作用与语义：**

返回对应当前风格提示的家族姓氏。

### `bool QFont::exactMatch() const`

**作用与语义：**

如果有与该字体设置完全匹配的窗口系统字体，返回`true`。

### `QStringList QFont::families() const`

**作用与语义：**

返回请求的字体族名，即上次`setFamilies()`调用或通过构造函数设置的名称。否则返回空列表。

### `QString QFont::family() const`

**作用与语义：**

返回请求的字体族名。这始终与`families()`调用中的第一个条目相同。

### `[since 6.7] QList<QFont::Tag> QFont::featureTags() const`

**作用与语义：**

返回当前该`QFont`上所有字体功能的标签列表。
有关字体功能的更多细节，请参见`setFeature()`。

### `[since 6.7] quint32 QFont::featureValue(QFont::Tag tag) const`

**作用与语义：**

返回特定特征`tag`的值。如果标签未被设置，则返回为0。
有关字体功能的更多细节，请参见`setFeature()`。

### `bool QFont::fixedPitch() const`

**作用与语义：**

如果已设定固定音高，返回`true`;否则返回`false`。

### `bool QFont::fromString(const QString &descrip)`

**作用与语义：**

将该字体设置为与描述`descrip`匹配。描述是字体属性的逗号分隔列表，由`toString()`返回。

### `QFont::HintingPreference QFont::hintingPreference() const`

**作用与语义：**

返回当前用该字体渲染的字形的首选提示层级。

### `[static] void QFont::insertSubstitution(const QString &familyName, const QString &substituteName)`

**作用与语义：**

将`substituteName`插入到族`familyName`的替换表中。
替换字体后，通过销毁并重新创建所有`QFont`对象来触发字体更新。

### `[static] void QFont::insertSubstitutions(const QString &familyName, const QStringList &substituteNames)`

**作用与语义：**

将`substituteNames`族列表插入`familyName`的替换列表。
替换字体后，通过销毁并重新创建所有`QFont`对象来触发字体更新。

### `bool QFont::isCopyOf(const QFont &f) const`

**作用与语义：**

如果该字体和`f`是彼此的复制品，即其中一个是作为另一个的复制品创建的，且此后未被修改，返回`true`。这比相等更严格。

### `[since 6.7] bool QFont::isFeatureSet(QFont::Tag tag) const`

**作用与语义：**

如果`tag`给出的特征在`QFont`上设置了某个值，则返回真;否则返回假。
有关字体功能的更多细节，请参见`setFeature()`。

### `[since 6.7] bool QFont::isVariableAxisSet(QFont::Tag tag) const`

**作用与语义：**

如果变量轴的值在`tag` `QFont`上被设置，则返回真，否则返回虚假。
有关字体变量轴的更多细节，请参见 `setVariableAxis()`。

### `bool QFont::italic() const`

**作用与语义：**

如果字体`style()`不`true`，返回`QFont::StyleNormal`。

### `bool QFont::kerning() const`

**作用与语义：**

返回`true`在使用该字体绘制文本时是否应使用字距调整。

### `QString QFont::key() const`

**作用与语义：**

返回字体键，字体的文本表示。它通常用作字体缓存或字典的键。

### `qreal QFont::letterSpacing() const`

**作用与语义：**

返回字体的字母间距。

### `QFont::SpacingType QFont::letterSpacingType() const`

**作用与语义：**

返回用于字母间距的间距类型。

### `bool QFont::overline() const`

**作用与语义：**

如果已设置划线，返回`true`;否则返回`false`。

### `int QFont::pixelSize() const`

**作用与语义：**

如果字体设置为 `setPixelSize()`，则返回字体的像素大小。如果设置为 `setPointSize()` 或 `setPointSizeF()`，则返回 -1。

### `int QFont::pointSize() const`

**作用与语义：**

返回字体的点大小。如果字体大小以像素为单位，返回 -1。

### `qreal QFont::pointSizeF() const`

**作用与语义：**

返回字体的点大小。如果字体大小以像素为单位，返回 -1。

### `[static] void QFont::removeSubstitutions(const QString &familyName)`

**作用与语义：**

去除了所有`familyName`的替代。

### `QFont QFont::resolve(const QFont &other) const`

**作用与语义：**

返回一个新`QFont`，该包含从`other`复制过但之前未在该字体上设置过的属性。

### `void QFont::setBold(bool enable)`

**作用与语义：**

如果 `enable` 为真，则字体权重为 `QFont::Bold`;否则权重为 `QFont::Normal`。
要控制更细致的胆量，请使用`setWeight()`。
注意：如果设置了`styleName()`，该值可能会被忽略;如果平台支持，字体会被人工加粗。

### `void QFont::setCapitalization(QFont::Capitalization caps)`

**作用与语义：**

将该字体中的文本大写设置为`caps`。
字体的大小写使文本以选定的大小写模式出现。

### `void QFont::setFamilies(const QStringList &families)`

**作用与语义：**

列出字体的族名列表。名称不区分大小写，可能包含铸字厂名称。`families`年中的第一个族将作为字体的主族。
`families` 中的每个家族名称条目还可以选择包含一个铸造厂名称，例如“Helvetica [Cronyx]”。如果该家族来自多个铸造厂且未指定铸造厂，则选择任意铸造厂。如果无法使用该家族，则通过字体匹配算法设置一个代字厂。

### `void QFont::setFamily(const QString &family)`

**作用与语义：**

确定字体的族名。名称不区分大小写，可能包含铸字厂名称。
`family`名称也可以选择性地包含铸造厂名称，例如“Helvetica [Cronyx]”。如果`family`来自多个铸造厂且未指定铸造厂，则选择任意铸造厂。如果族群不可用，则通过字体匹配算法设置族。

### `[since 6.7] void QFont::setFeature(QFont::Tag tag, quint32 value)`

**作用与语义：**

在调整文本时，对`tag`指定的排版功能应用整数值。这为字体塑造过程提供了高级访问权限，并可用于支持API未涵盖的字体功能。
该功能由一个`tag`指定，通常由字体功能图中的四个字符特征名称编码而成。
这个`value`与标签一起传递的整数在大多数情况下代表一个布尔值：值为零表示该功能被禁用，非零值表示该功能已被启用。然而，对于某些字体特性，它可能有其他解释。例如，当应用于`salt`功能时，该值是一个索引，用于指定可使用样式的替代方案。
例如，`frac`字体功能会将用斜杠分隔的对角分数（如`1/2`）转换为不同的表示方式。通常这会将整个分数烘焙成单一字符宽度（如`½`）。
如果字体支持`frac`功能，可以通过在字体功能映射中设置`features["frac"] = 1`来启用。
注意：默认情况下，Qt 会根据其他字体属性启用或禁用某些字体功能。特别是，`kern` 功能会根据`QFont`的`kerning()`属性启用或禁用。此外，所有连字功能（`liga`、`clig`、`dlig`、`hlig`）如果应用`letterSpacing()`也会被禁用，但仅限于那些连字只是装饰性的书写系统。对于需要连字的书写系统，功能将保持默认状态。使用setFeature()及相关函数设置的值会覆盖默认行为。例如，如果功能“字距”设置为1，那么字距调整总是被启用，无论字距调整属性是否设为false。同样，如果设置为0，字距调整总是被禁用。要将字体特性重置为默认行为，可以使用`unsetFeature()`取消设置。

### `void QFont::setFixedPitch(bool enable)`

**作用与语义：**

如果`enable`为真，则将固定音高设为 ;否则将固定音高关闭。

### `void QFont::setHintingPreference(QFont::HintingPreference hintingPreference)`

**作用与语义：**

将字形提示级别的偏好设置为`hintingPreference`。这是对底层字体渲染系统使用一定程度提示的提示，且各平台支持各异。详情请参见文档中的表格`QFont::HintingPreference`。
默认的提示偏好是`QFont::PreferDefaultHinting`。

### `void QFont::setItalic(bool enable)`

**作用与语义：**

如果 `enable`为真，则将字体的 `style()` 设置为 `QFont::StyleItalic`;否则样式设为 `QFont::StyleNormal`。
注意：如果`styleName()`设置，该值可以忽略;如果平台支持，字体可能会倾斜，而不是选择设计的斜体字体变体。

### `void QFont::setKerning(bool enable)`

**作用与语义：**

如果`enable`为真，则启用字距调整;否则禁用字距。默认情况下，字距调整是启用的。
启用字距调整时，字形度量不再相符，即使是拉丁文本也是如此。换句话说，宽度（'a'）宽度（'b'）等于宽度（“ab”）的假设不一定成立。

### `void QFont::setLetterSpacing(QFont::SpacingType type, qreal spacing)`

**作用与语义：**

将字体的字母间距设置为`spacing`，间距类型设置为`type`。
字母间距会改变字体中单个字母之间的默认间距。字母间距可以根据所选的间距类型，按字符宽度百分比或像素单位调整为更小或更大。

### `void QFont::setOverline(bool enable)`

**作用与语义：**

如果`enable`为真，则使上划线 为 ;否则 使上划线关闭。

### `void QFont::setPixelSize(int pixelSize)`

**作用与语义：**

将字体大小设置为`pixelSize`像素，最大大小为无符号的16位整数。
使用此函数使字体依赖设备。使用`setPointSize()`或`setPointSizeF()`以设备无关的方式设置字体大小。

### `void QFont::setPointSize(int pointSize)`

**作用与语义：**

将点大小设为`pointSize`。点大小必须大于零。

### `void QFont::setPointSizeF(qreal pointSize)`

**作用与语义：**

将点大小设为`pointSize`。点大小必须大于零。要求的精度可能并非所有平台都能实现。

### `void QFont::setStretch(int factor)`

**作用与语义：**

它设定了字体的拉伸系数。
拉伸系数匹配字体的浓缩或扩展版本，或者应用拉伸变换，使字体中所有字符的宽度变化`factor`%。例如，将`factor`设为150，字体中所有字符宽度增加1.5倍（即150%）。最小拉伸因子为1，最大拉伸因子为4000。默认拉伸因子为`AnyStretch`，接受任何拉伸因子，且不对字体施加任何变换。
拉伸因子仅应用于轮廓字体。位图字体忽略拉伸因子。
注意：当匹配带有原生非默认拉伸因子的字体时，请求100的拉伸会将其拉伸回中宽字体。

### `void QFont::setStrikeOut(bool enable)`

**作用与语义：**

如果`enable`为真，则三振出局为开;否则置三振出局。

### `void QFont::setStyle(QFont::Style style)`

**作用与语义：**

将字体样式设置为`style`。

### `void QFont::setStyleHint(QFont::StyleHint hint, QFont::StyleStrategy strategy = PreferDefault)`

**作用与语义：**

将风格提示和策略分别设定为`hint`和`strategy`。
如果这些提示没有明确设置，风格提示会默认为`AnyStyle`，风格策略则会变成`PreferDefault`。
Qt 在 X11 上不支持样式提示，因为这些信息不由窗口系统提供。

### `void QFont::setStyleName(const QString &styleName)`

**作用与语义：**

将字体样式名称设置为`styleName`。设置后，其他样式属性如`style()`和`weight()`将被忽略用于字体匹配，尽管如果平台的字体引擎支持，这些属性可能会在之后进行模拟。
由于人工模拟样式质量较低，且缺乏完整的跨平台支持，不建议同时使用样式名称匹配和样式匹配属性。

### `void QFont::setStyleStrategy(QFont::StyleStrategy s)`

**作用与语义：**

将字体的样式策略设置为`s`。

### `void QFont::setUnderline(bool enable)`

**作用与语义：**

如果`enable`为真，则下划线开启;否则下划线关闭。

### `[since 6.7] void QFont::setVariableAxis(QFont::Tag tag, float value)`

**作用与语义：**

对应于`tag`的可变轴施加`value`。
可变字体提供了一种方式，可以在同一字体文件中存储多个变体（具有不同的粗细、宽度或样式）。这些变体以浮点值的形式给出，用于预定义的一组参数，称为“可变轴”。特定实例通常由字体设计者命名，在 Qt 中，这些实例可以通过 `setStyleName()` 选择，就像传统的子家族一样。
在某些情况下，为不同轴提供任意值也很有用。例如，如果字体有常规和粗体子家族，你可能需要在它们之间加一个权重。你可以手动请求，提供字体中“wght”轴的自定义值。
如果字体支持“wght”轴且给定值在其定义范围内，则会提供对应权重550.0的字体。
许多字体提供的标准轴线有几种，如“wght”（粗细）、“wdth”（宽度）“ital”（斜体）和“opsz”（光学尺寸）。它们各自在字体本身中定义了独立范围。例如，“wght”可能跨度为100到900（`QFont::Thin`到`QFont::Black`），而“ital”可以从0到1（从非斜体到完全斜体）。
字体也可以选择定义自定义轴;唯一的限制是名称必须满足`QFont::Tag`（四个拉丁字母-1字符序列）的要求。
默认情况下，不设置可变轴。
注意：在Windows上，如果使用可选的GDI字体后端，则不支持可变轴。

**官方示例：**

```cpp
 QFont font;
 font.setVariableAxis("wght", (QFont::Normal + QFont::Bold) / 2.0f);
```

### `void QFont::setWeight(QFont::Weight weight)`

**作用与语义：**

将字体权重设置为`weight`，使用枚举定义的比例`QFont::Weight`。
注意：如果`styleName()`设置，字体选择时可能会忽略该值。

### `void QFont::setWordSpacing(qreal spacing)`

**作用与语义：**

将字体的字距设置为`spacing`。
单词间距会改变单词间的默认间距。正值则使单词间距增加相应的像素数，负值则相应减少单词间距。
词间距不适用于书写系统，因为单个单词之间没有留白。

### `int QFont::stretch() const`

**作用与语义：**

它会返回字体的拉伸因子。

### `bool QFont::strikeOut() const`

**作用与语义：**

如果已设定三振，则回`true`;否则回`false`。

### `QFont::Style QFont::style() const`

**作用与语义：**

返回字体样式。

### `QFont::StyleHint QFont::styleHint() const`

**作用与语义：**

还给`StyleHint`。
样式提示影响字体匹配算法。有关可用提示列表，请参见 `QFont::StyleHint`。

### `QString QFont::styleName() const`

**作用与语义：**

返回请求的字体样式名称。这可以用来匹配不规则样式的字体（这些样式无法在其他样式属性中规范化）。

### `QFont::StyleStrategy QFont::styleStrategy() const`

**作用与语义：**

还给`StyleStrategy`。
样式策略会影响字体匹配算法。有关可用策略列表，请参见 `QFont::StyleStrategy`。

### `[static] QString QFont::substitute(const QString &familyName)`

**作用与语义：**

每当指定`familyName`时返回第一个家族姓氏。查询不区分大小写。
如果没有替代的 `familyName`，则返回`familyName`。
要获取替换列表，请使用`substitutes()`。

### `[static] QStringList QFont::substitutes(const QString &familyName)`

**作用与语义：**

返回一份家族姓氏列表，每当指定`familyName`时使用。查询不区分大小写。
如果没有替换 `familyName`，则返回一个空列表。

### `[static] QStringList QFont::substitutions()`

**作用与语义：**

返回排序的替换姓氏列表。

### `[noexcept] void QFont::swap(QFont &other)`

**作用与语义：**

将该字体实例与`other`交换。此操作非常快速且从未失败。

### `QString QFont::toString() const`

**作用与语义：**

返回字体描述。描述是一份逗号分隔的属性列表，非常适合`QSettings`中使用，包含以下内容：
- 字体家族
- 点数大小
- 像素尺寸
- 风格提示
- 字体粗细
- 字体样式
- 下划线
- 三振出局
- 固定音距
- 永远为0
- 大小写
- 字母间距
- 词间距
- 拉伸
- 风格策略
- 字体样式
- 字体特征
- 可变轴

### `bool QFont::underline() const`

**作用与语义：**

如果下划线设置，返回`true`;否则返回`false`。

### `[since 6.7] void QFont::unsetFeature(QFont::Tag tag)`

**作用与语义：**

从明确启用/禁用功能的映射中撤销`tag`。
注意：即使此前未添加该功能，这也会标记字体功能映射为本`QFont`修改，因此在与其他字体解析时，该映射将优先。
取消`QFont`上的现有功能会恢复默认状态。
有关字体功能的更多细节，请参见`setFeature()`。

### `[since 6.7] void QFont::unsetVariableAxis(QFont::Tag tag)`

**作用与语义：**

重置由`tag`给出的先前设定的可变轴值。
注意：如果此标签之前没有给出任何值，`QFont`在与其他`QFont`值解析时仍会将变量轴视为设定值。

### `[since 6.7] QList<QFont::Tag> QFont::variableAxisTags() const`

**作用与语义：**

返回当前该`QFont`上所有变量轴的标签列表。
关于变轴的更多细节，请参见 `setVariableAxis()`。

### `[since 6.7] float QFont::variableAxisValue(QFont::Tag tag) const`

**作用与语义：**

返回特定变量轴的值`tag`。如果标签未被设置，则返回0.0。
关于可变轴的更多细节，请参见`setVariableAxis()`。

### `QFont::Weight QFont::weight() const`

**作用与语义：**

返回字体权重，使用与`QFont::Weight`枚举相同的刻度。

### `qreal QFont::wordSpacing() const`

**作用与语义：**

返回字体的字距。

### `QFont::operator QVariant() const`

**作用与语义：**

将字体返回为`QVariant`。

### `bool QFont::operator!=(const QFont &f) const`

**作用与语义：**

如果字体与`f`不同，返回`true`;否则返回`false`。
如果两个QFont的字体属性不同，则被视为不同。

### `bool QFont::operator<(const QFont &f) const`

**作用与语义：**

提供了该字体与字体`f`的任意比较。唯一保证`false`的是，如果两个字体相等，且 （f1 < f2） == ！（f2 < f1） 如果字体不相等。
该函数在某些情况下非常有用，例如你想在`QMap`中使用`QFont`对象作为键。

### `[noexcept] QFont &QFont::operator=(QFont &&other)`

**作用与语义：**

Move-assign `other`到该`QFont`实例。

### `QFont &QFont::operator=(const QFont &font)`

**作用与语义：**

为该字体分配`font`并返回引用。

### `bool QFont::operator==(const QFont &f) const`

**作用与语义：**

如果该字体等于 `f`，则返回 `true`;否则返回 false。
如果两个QFont的字体属性相等，则视为相等。

### `[noexcept] size_t qHash(const QFont &key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `QDataStream &operator<<(QDataStream &s, const QFont &font)`

**作用与语义：**

将字体`font`写入数据流`s`。（`toString()`写入文本流。）。

### `QDataStream &operator>>(QDataStream &s, QFont &font)`

**作用与语义：**

从数据流中读取字体`font` `s`。（`fromString()`从文本流读取。）。

### `(since 6.7) struct Tag`

**作用与语义：**

QFont::Tag 类型提供访问高级字体功能的能力。
`QFont` 在文本排版时提供访问高级功能的能力。功能由标签定义，可以表示为四字符字符串或 32 位整数值。此类型以类型安全的方式表示这样的标签。它可以从四字符 8 位字符串字面值或对应的 32 位整数值构造。使用更短或更长的字符串字面值将导致编译时错误。
命名构造函数允许从 32 位整数或字符串值创建标签，如果输入无效，将返回 `std::nullopt`。

**官方示例：**

```cpp
 QFont font;
 // Correct
 font.setFeature("frac");

 // Wrong - won't compile
 font.setFeature("fraction");

 // Wrong - will produce runtime warning and fail
 font.setFeature(u"fraction"_s);
```

### `enum SpacingType { PercentageSpacing, AbsoluteSpacing }`

**作用与语义：**

- `QFont::PercentageSpacing`：`0`;值为100时保持间距不变;值为200时，字符后方的间距增加到字符本身的宽度。
- `QFont::AbsoluteSpacing`：`1`;正值使字母间距增加相应像素;负值则减少间距。

## 6. 深入实践与常见坑

### 生命周期和资源边界

绘制上下文必须绑定有效的 paint device，并在合法的绘制阶段使用。QWidget 上通常只在 `paintEvent()` 内创建 painter；离屏图像、打印设备和 pixmap 则有各自的设备生命周期。

### 状态和错误边界

`save()`/`restore()` 用于隔离局部状态；改变坐标系、画笔或合成模式后要么恢复，要么明确后续绘制也需要该状态。重绘请求和真正绘制是两个阶段，业务状态变化应调用 `update()`。

### 线程边界

同一个 GUI 控件的绘制在 GUI 线程完成；离屏 QImage 可以按数据所有权在后台处理，但不要让后台线程直接绘制或访问正在显示的 QWidget/QPixmap 资源。

### 最容易出现的错误

不要直接调用 paintEvent；不要在绘制函数里修改会再次触发绘制的状态；不要假定所有图像都是四字节像素；不要忘记 transform 会影响坐标和 boundingRect。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QFont` 所属机制类型：二维绘制状态机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
