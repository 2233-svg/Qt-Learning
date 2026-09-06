# QTextCharFormat

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是格式或能力描述类型，重点关注可用格式、属性查询和与实际数据对象之间的转换。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QTextCharFormat` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QTextCharFormat>`
- 继承自：QTextFormat
- 直接派生类：QTextImageFormat、QTextTableCellFormat

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

- `enum FontPropertiesInheritanceBehavior { FontPropertiesSpecifiedOnly, FontPropertiesAll }`
- `enum UnderlineStyle { NoUnderline, SingleUnderline, DashUnderline, DotLine, DashDotLine, …, SpellCheckUnderline }`
- `enum VerticalAlignment { AlignNormal, AlignSuperScript, AlignSubScript, AlignMiddle, AlignBottom, …, AlignBaseline }`

### 公有函数

- `QTextCharFormat()`
- `QString anchorHref() const`
- `QStringList anchorNames() const`
- `(since 6.0) qreal baselineOffset() const`
- `QFont font() const`
- `QFont::Capitalization fontCapitalization() const`
- `QVariant fontFamilies() const`
- `(since 6.11) QMap<QFont::Tag, quint32> fontFeatures() const`
- `bool fontFixedPitch() const`
- `QFont::HintingPreference fontHintingPreference() const`
- `bool fontItalic() const`
- `bool fontKerning() const`
- `qreal fontLetterSpacing() const`
- `QFont::SpacingType fontLetterSpacingType() const`
- `bool fontOverline() const`
- `qreal fontPointSize() const`
- `int fontStretch() const`
- `bool fontStrikeOut() const`
- `QFont::StyleHint fontStyleHint() const`
- `QVariant fontStyleName() const`
- `QFont::StyleStrategy fontStyleStrategy() const`
- `bool fontUnderline() const`
- `(since 6.11) QMap<QFont::Tag, float> fontVariableAxes() const`
- `int fontWeight() const`
- `qreal fontWordSpacing() const`
- `bool isAnchor() const`
- `bool isValid() const`
- `void setAnchor(bool anchor)`
- `void setAnchorHref(const QString &value)`
- `void setAnchorNames(const QStringList &names)`
- `(since 6.0) void setBaselineOffset(qreal baseline)`
- `void setFont(const QFont &font, QTextCharFormat::FontPropertiesInheritanceBehavior behavior = FontPropertiesAll)`
- `void setFontCapitalization(QFont::Capitalization capitalization)`
- `void setFontFamilies(const QStringList &families)`
- `(since 6.11) void setFontFeatures(const QMap<QFont::Tag, quint32> &fontFeatures)`
- `void setFontFixedPitch(bool fixedPitch)`
- `void setFontHintingPreference(QFont::HintingPreference hintingPreference)`
- `void setFontItalic(bool italic)`
- `void setFontKerning(bool enable)`
- `void setFontLetterSpacing(qreal spacing)`
- `void setFontLetterSpacingType(QFont::SpacingType letterSpacingType)`
- `void setFontOverline(bool overline)`
- `void setFontPointSize(qreal size)`
- `void setFontStretch(int factor)`
- `void setFontStrikeOut(bool strikeOut)`
- `void setFontStyleHint(QFont::StyleHint hint, QFont::StyleStrategy strategy = QFont::PreferDefault)`
- `void setFontStyleName(const QString &styleName)`
- `void setFontStyleStrategy(QFont::StyleStrategy strategy)`
- `void setFontUnderline(bool underline)`
- `(since 6.11) void setFontVariableAxes(const QMap<QFont::Tag, float> &fontVariableAxes)`
- `void setFontWeight(int weight)`
- `void setFontWordSpacing(qreal spacing)`
- `(since 6.0) void setSubScriptBaseline(qreal baseline)`
- `(since 6.0) void setSuperScriptBaseline(qreal baseline)`
- `void setTextOutline(const QPen &pen)`
- `void setToolTip(const QString &text)`
- `void setUnderlineColor(const QColor &color)`
- `void setUnderlineStyle(QTextCharFormat::UnderlineStyle style)`
- `void setVerticalAlignment(QTextCharFormat::VerticalAlignment alignment)`
- `(since 6.0) qreal subScriptBaseline() const`
- `(since 6.0) qreal superScriptBaseline() const`
- `QPen textOutline() const`
- `QString toolTip() const`
- `QColor underlineColor() const`
- `QTextCharFormat::UnderlineStyle underlineStyle() const`
- `QTextCharFormat::VerticalAlignment verticalAlignment() const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QTextCharFormat::FontPropertiesInheritanceBehavior`

**作用与语义：**

该枚举规定了`setFont()`函数在未设定字体属性下的行为。
- `QTextCharFormat::FontPropertiesSpecifiedOnly`：`0`;如果属性未被明确设置，不要更改文本格式的属性值。
- `QTextCharFormat::FontPropertiesAll`：`1`;如果某个属性未被明确设置，则用默认值覆盖文本格式的属性。

### `enum QTextCharFormat::UnderlineStyle`

**作用与语义：**

这个枚举描述了绘制下划线文字的不同方式。
- `QTextCharFormat::NoUnderline`：`0`;文字绘制时不加任何下划线装饰。
- `QTextCharFormat::SingleUnderline`：`1`;用`Qt::SolidLine`画线。
- `QTextCharFormat::DashUnderline`：`2`;划线使用`Qt::DashLine`绘制。
- `QTextCharFormat::DotLine`：`3`;点是用`Qt::DotLine`绘制的;
- `QTextCharFormat::DashDotLine`：`4`;用`Qt::DashDotLine`绘制破折号和点。
- `QTextCharFormat::DashDotDotLine`：`5`;下划线，使用`Qt::DashDotDotLine`绘制。
- `QTextCharFormat::WaveUnderline`：`6`;文本用波浪形线条划线。
- `QTextCharFormat::SpellCheckUnderline`：`7`;下划线根据QPlatformTheme的SpellCheckUnderlineStyle主题提示绘制。默认情况下，下划线映射为WaveUnderline，在macOS上映射为DotLine。

### `enum QTextCharFormat::VerticalAlignment`

**作用与语义：**

这个枚举描述了相邻字符垂直排列的方式。
- `QTextCharFormat::AlignNormal`：`0`;相邻字符按所用书写系统文本的标准方式排列。
- `QTextCharFormat::AlignSuperScript`：`1`;普通文本的字符置于基线之上。
- `QTextCharFormat::AlignSubScript`：`2`;普通文本的字符置于基线下方。
- `QTextCharFormat::AlignMiddle`：`3`;物体中心与基线垂直对齐。目前，这仅用于内联物体。
- `QTextCharFormat::AlignBottom`：`5`;物体的底边与基线垂直对齐。
- `QTextCharFormat::AlignTop`：`4`;物体的顶边与基线垂直对齐。
- `QTextCharFormat::AlignBaseline`：`6`;角色的基线线对齐。

### `QTextCharFormat::QTextCharFormat()`

**作用与语义：**

构建一个新的字符格式对象。

### `QString QTextCharFormat::anchorHref() const`

**作用与语义：**

返回文本格式的超文本链接，若未设置则返回空字符串。

### `QStringList QTextCharFormat::anchorNames() const`

**作用与语义：**

返回与该文本格式相关的锚点名称，若未设置锚点则返回空字符串列表。如果锚点名称已设置，采用此格式的文本可以作为超文本链接的目的地。

### `[since 6.0] qreal QTextCharFormat::baselineOffset() const`

**作用与语义：**

返回基线偏移的百分比。

### `QFont QTextCharFormat::font() const`

**作用与语义：**

返回该字符格式的字体。
该函数考虑格式的字体属性（如`fontWeight()`和`fontPointSize()`），并在默认字体之上解析，定义如下。如果格式是文档的一部分，则该字体为文档的默认字体。否则属性会在默认构造`QFont`上解析。
例如，如果该格式的字体大小未与默认字体更改，`fontPointSize()`返回0，而`font().pointSize()`返回绘画时使用的实际大小。

### `QFont::Capitalization QTextCharFormat::fontCapitalization() const`

**作用与语义：**

返回字体当前的大写类型。

### `QVariant QTextCharFormat::fontFamilies() const`

**作用与语义：**

返回文本格式的字体族。
注意：出于历史原因，该函数返回`QVariant`。将在Qt 7中修正为返回`QStringList`。该变体包含一个`QStringList`对象，可以通过调用`toStringList()`提取。

### `[since 6.11] QMap<QFont::Tag, quint32> QTextCharFormat::fontFeatures() const`

**作用与语义：**

获得文本格式字体的排版特征。

### `bool QTextCharFormat::fontFixedPitch() const`

**作用与语义：**

如果文本格式的字体是固定音高，返回`true`;否则返回`false`。

### `QFont::HintingPreference QTextCharFormat::fontHintingPreference() const`

**作用与语义：**

返回该文本格式的提示偏好设置。

### `bool QTextCharFormat::fontItalic() const`

**作用与语义：**

如果文本格式的字体为斜体，返回`true`;否则返回`false`。

### `bool QTextCharFormat::fontKerning() const`

**作用与语义：**

如果启用字体字距调整，返回`true`。

### `qreal QTextCharFormat::fontLetterSpacing() const`

**作用与语义：**

返回当前的字母间距。

### `QFont::SpacingType QTextCharFormat::fontLetterSpacingType() const`

**作用与语义：**

返回该格式的字母间距类型......

### `bool QTextCharFormat::fontOverline() const`

**作用与语义：**

如果文本格式的字体被划线，返回`true`;否则返回`false`。

### `qreal QTextCharFormat::fontPointSize() const`

**作用与语义：**

返回用于显示该格式文本的字体大小。

### `int QTextCharFormat::fontStretch() const`

**作用与语义：**

返回当前字体拉伸状态。

### `bool QTextCharFormat::fontStrikeOut() const`

**作用与语义：**

如果文本格式的字体被划去（有横线穿过），返回`true`;否则返回`false`。

### `QFont::StyleHint QTextCharFormat::fontStyleHint() const`

**作用与语义：**

返回字体样式提示。

### `QVariant QTextCharFormat::fontStyleName() const`

**作用与语义：**

返回文本格式的字体样式名称。
注意：该函数返回`QVariant`，出于历史原因。将在Qt 7中修正返回`QStringList`。该变体包含一个`QStringList`对象，可以通过调用`toStringList()`提取。

### `QFont::StyleStrategy QTextCharFormat::fontStyleStrategy() const`

**作用与语义：**

返回当前字体样式策略。

### `bool QTextCharFormat::fontUnderline() const`

**作用与语义：**

如果文本格式的字体被划线，返回`true`;否则返回`false`。

### `[since 6.11] QMap<QFont::Tag, float> QTextCharFormat::fontVariableAxes() const`

**作用与语义：**

获取文本格式字体的可变轴。

### `int QTextCharFormat::fontWeight() const`

**作用与语义：**

返回文本格式的字体粗细。

### `qreal QTextCharFormat::fontWordSpacing() const`

**作用与语义：**

返回当前的字间距值。

### `bool QTextCharFormat::isAnchor() const`

**作用与语义：**

如果文本格式为锚点，返回`true`;否则返回`false`。

### `bool QTextCharFormat::isValid() const`

**作用与语义：**

如果该字符格式有效，返回`true`;否则返回 false。

### `void QTextCharFormat::setAnchor(bool anchor)`

**作用与语义：**

如果`anchor`为真，采用此格式的文本代表锚点，格式化方式正确;否则文本格式正常。（锚点是通常以下划线且颜色不同于纯文本显示的超链接。）。
文本的渲染方式与格式是否定义有效锚点无关。使用`setAnchorHref()`，并可选`setAnchorNames()`创建超文本链接。

### `void QTextCharFormat::setAnchorHref(const QString &value)`

**作用与语义：**

将文本格式的超文本链接设置为给定的`value`。这通常是像“http://example.com/index.html”这样的URL。
锚点会显示`value`作为其显示文本;如果你想显示不同的文本，请调用`setAnchorNames()`。
要将文本格式化为超文本链接，请使用`setAnchor()`。

### `void QTextCharFormat::setAnchorNames(const QStringList &names)`

**作用与语义：**

设置文本格式的锚`names`。为了使锚点作为超链接工作，目标必须用`setAnchorHref()`设置，锚点必须用`setAnchor()`启用。

### `[since 6.0] void QTextCharFormat::setBaselineOffset(qreal baseline)`

**作用与语义：**

将文本的基线（高度百分比）设置为`baseline`。正值则将文本向上移动相应百分比;负值则向下移动。默认值为0。

### `void QTextCharFormat::setFont(const QFont &font, QTextCharFormat::FontPropertiesInheritanceBehavior behavior = FontPropertiesAll)`

**作用与语义：**

设定文本格式的 `font`。
如果`behavior`为`QTextCharFormat::FontPropertiesAll`，未显式设置的字体属性会被处理为默认值;如果`behavior` `QTextCharFormat::FontPropertiesSpecifiedOnly`，则未显式设置的字体属性被忽略，相应属性值保持不变。

### `void QTextCharFormat::setFontCapitalization(QFont::Capitalization capitalization)`

**作用与语义：**

将该字体中出现的文本大小写设置为`capitalization`。
字体的大小写使文本以选定的大小写模式出现。

### `void QTextCharFormat::setFontFamilies(const QStringList &families)`

**作用与语义：**

设置文本格式的字体`families`。

### `[since 6.11] void QTextCharFormat::setFontFeatures(const QMap<QFont::Tag, quint32> &fontFeatures)`

**作用与语义：**

将文本格式字体的排版特征设置为`fontFeatures`。

### `void QTextCharFormat::setFontFixedPitch(bool fixedPitch)`

**作用与语义：**

如果`fixedPitch`为真，则将文本格式的字体设置为固定音高;否则使用非固定音高字体。

### `void QTextCharFormat::setFontHintingPreference(QFont::HintingPreference hintingPreference)`

**作用与语义：**

设置文本格式字体的提示偏好为`hintingPreference`。

### `void QTextCharFormat::setFontItalic(bool italic)`

**作用与语义：**

如果`italic`为真，则将文本格式的字体设置为斜体;否则字体将为非斜体。

### `void QTextCharFormat::setFontKerning(bool enable)`

**作用与语义：**

如果`enable`为真，则启用字体字距调整;否则禁用。
启用字距调整时，字形度量不再相符，即使是拉丁文本也是如此。换句话说，宽度（'a'）宽度（'b'）等于宽度（“ab”）的假设不一定成立。

### `void QTextCharFormat::setFontLetterSpacing(qreal spacing)`

**作用与语义：**

将该格式的字母间距设置为给定的`spacing`。该值的含义取决于字体和字母间距类型。
对于百分比间距，值为100表示默认间距;值为200则使字母所占空间翻倍。

### `void QTextCharFormat::setFontLetterSpacingType(QFont::SpacingType letterSpacingType)`

**作用与语义：**

将该格式的字母间距类型设置为`letterSpacingType`。

### `void QTextCharFormat::setFontOverline(bool overline)`

**作用与语义：**

如果`overline`为真，则将文本格式的字体设置为加划线;否则字体显示为非划线。

### `void QTextCharFormat::setFontPointSize(qreal size)`

**作用与语义：**

设置文本格式的字体`size`。

### `void QTextCharFormat::setFontStretch(int factor)`

**作用与语义：**

它会把字体的拉伸因子设为`factor`。
拉伸因子通过倍率改变字体中所有字符的宽度。例如，将`factor`设为150，字体中所有字符宽度增加1.5倍（即150%）。默认拉伸因子为100。最小拉伸因子为1，最大拉伸因子为4000。
拉伸因子仅应用于轮廓字体。位图字体忽略拉伸因子。

### `void QTextCharFormat::setFontStrikeOut(bool strikeOut)`

**作用与语义：**

如果`strikeOut`为真，则将文本格式的字体设置为启用划号（并有横线穿过）;否则则不划号显示。

### `void QTextCharFormat::setFontStyleHint(QFont::StyleHint hint, QFont::StyleStrategy strategy = QFont::PreferDefault)`

**作用与语义：**

设置字体样式`hint`和`strategy`。
Qt 在 X11 上不支持样式提示，因为这些信息不由窗口系统提供。

### `void QTextCharFormat::setFontStyleName(const QString &styleName)`

**作用与语义：**

设置文本格式的字体`styleName`。

### `void QTextCharFormat::setFontStyleStrategy(QFont::StyleStrategy strategy)`

**作用与语义：**

设定字体样式`strategy`。

### `void QTextCharFormat::setFontUnderline(bool underline)`

**作用与语义：**

如果`underline`为真，则将文本格式的字体设置为下划线;否则显示为非下划线。

### `[since 6.11] void QTextCharFormat::setFontVariableAxes(const QMap<QFont::Tag, float> &fontVariableAxes)`

**作用与语义：**

将文本格式字体的可变轴设置为`fontVariableAxes`。

### `void QTextCharFormat::setFontWeight(int weight)`

**作用与语义：**

将文本格式的字体粗细设置为`weight`。

### `void QTextCharFormat::setFontWordSpacing(qreal spacing)`

**作用与语义：**

将该格式的字间距设置为给定的像素`spacing`。

### `[since 6.0] void QTextCharFormat::setSubScriptBaseline(qreal baseline)`

**作用与语义：**

将下标的基准行设置为字体高度的百分比为`baseline`。默认值为16.67%（高度的1/6）。

### `[since 6.0] void QTextCharFormat::setSuperScriptBaseline(qreal baseline)`

**作用与语义：**

将上标的基准行设置为字体高度的百分比，设置为`baseline`。默认值为50%（高度的一半）。

### `void QTextCharFormat::setTextOutline(const QPen &pen)`

**作用与语义：**

设置用于绘制角色轮廓的钢笔到指定`pen`。

### `void QTextCharFormat::setToolTip(const QString &text)`

**作用与语义：**

将文本片段的工具提示设置为给定的 `text`。

### `void QTextCharFormat::setUnderlineColor(const QColor &color)`

**作用与语义：**

将用于在该格式中字符上划下线、上划线和划线的颜色设置为指定的`color`。

### `void QTextCharFormat::setUnderlineStyle(QTextCharFormat::UnderlineStyle style)`

**作用与语义：**

将文本下划线的样式设置为`style`。

### `void QTextCharFormat::setVerticalAlignment(QTextCharFormat::VerticalAlignment alignment)`

**作用与语义：**

将该格式字符所用的垂直对齐设置为指定的`alignment`。

### `[since 6.0] qreal QTextCharFormat::subScriptBaseline() const`

**作用与语义：**

返回下标的基线，表示字体高度的百分比。

### `[since 6.0] qreal QTextCharFormat::superScriptBaseline() const`

**作用与语义：**

返回上标的基线，表示字体高度的百分比。

### `QPen QTextCharFormat::textOutline() const`

**作用与语义：**

返回用于绘制该格式字符轮廓的钢笔。

### `QString QTextCharFormat::toolTip() const`

**作用与语义：**

返回显示的提示，显示一段文本。

### `QColor QTextCharFormat::underlineColor() const`

**作用与语义：**

返回用于在该格式中为字符绘制下划线、划线和划线的颜色。

### `QTextCharFormat::UnderlineStyle QTextCharFormat::underlineStyle() const`

**作用与语义：**

恢复了对文本划线的风格。

### `QTextCharFormat::VerticalAlignment QTextCharFormat::verticalAlignment() const`

**作用与语义：**

返回该格式字符所使用的垂直对齐。

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

`QTextCharFormat` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
