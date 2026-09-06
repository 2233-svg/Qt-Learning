# QTextFormat

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是格式或能力描述类型，重点关注可用格式、属性查询和与实际数据对象之间的转换。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QTextFormat` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QTextFormat>`
- 继承自：未在类页中列出
- 直接派生类：QTextBlockFormat、QTextCharFormat、QTextFrameFormat,、QTextListFormat

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

- `enum FormatType { InvalidFormat, BlockFormat, CharFormat, ListFormat, FrameFormat, UserFormat }`
- `enum ObjectTypes { NoObject, ImageObject, TableObject, TableCellObject, UserObject }`
- `enum PageBreakFlag { PageBreak_Auto, PageBreak_AlwaysBefore, PageBreak_AlwaysAfter }`
- `flags PageBreakFlags`
- `enum Property { ObjectIndex, CssFloat, LayoutDirection, OutlinePen, ForegroundBrush, …, UserProperty }`

### 公有函数

- `QTextFormat()`
- `QTextFormat(int type)`
- `QTextFormat(const QTextFormat &other)`
- `~QTextFormat()`
- `QBrush background() const`
- `bool boolProperty(int propertyId) const`
- `QBrush brushProperty(int propertyId) const`
- `void clearBackground()`
- `void clearForeground()`
- `void clearProperty(int propertyId)`
- `QColor colorProperty(int propertyId) const`
- `qreal doubleProperty(int propertyId) const`
- `QBrush foreground() const`
- `bool hasProperty(int propertyId) const`
- `int intProperty(int propertyId) const`
- `bool isBlockFormat() const`
- `bool isCharFormat() const`
- `bool isEmpty() const`
- `bool isFrameFormat() const`
- `bool isImageFormat() const`
- `bool isListFormat() const`
- `bool isTableCellFormat() const`
- `bool isTableFormat() const`
- `bool isValid() const`
- `Qt::LayoutDirection layoutDirection() const`
- `QTextLength lengthProperty(int propertyId) const`
- `QList<QTextLength> lengthVectorProperty(int propertyId) const`
- `void merge(const QTextFormat &other)`
- `int objectIndex() const`
- `int objectType() const`
- `QPen penProperty(int propertyId) const`
- `QMap<int, QVariant> properties() const`
- `QVariant property(int propertyId) const`
- `int propertyCount() const`
- `void setBackground(const QBrush &brush)`
- `void setForeground(const QBrush &brush)`
- `void setLayoutDirection(Qt::LayoutDirection direction)`
- `void setObjectIndex(int index)`
- `void setObjectType(int type)`
- `void setProperty(int propertyId, const QList<QTextLength> &value)`
- `void setProperty(int propertyId, const QVariant &value)`
- `QString stringProperty(int propertyId) const`
- `void swap(QTextFormat &other)`
- `QTextBlockFormat toBlockFormat() const`
- `QTextCharFormat toCharFormat() const`
- `QTextFrameFormat toFrameFormat() const`
- `QTextImageFormat toImageFormat() const`
- `QTextListFormat toListFormat() const`
- `QTextTableCellFormat toTableCellFormat() const`
- `QTextTableFormat toTableFormat() const`
- `int type() const`
- `operator QVariant() const`
- `bool operator!=(const QTextFormat &other) const`
- `QTextFormat & operator=(const QTextFormat &other)`
- `bool operator==(const QTextFormat &other) const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QTextFormat::FormatType`

**作用与语义：**

这个枚举描述了`QTextFormat`对象正在格式化的文本项。
- `QTextFormat::InvalidFormat`：`-1`;由默认构造函数创建的无效格式
- `QTextFormat::BlockFormat`：`1`;对象格式化文本块
- `QTextFormat::CharFormat`：`2`;该对象格式化单个字符
- `QTextFormat::ListFormat`：`3`;对象格式化列表
- `QTextFormat::FrameFormat`：`5`;对象格式化帧
- `QTextFormat::UserFormat`：`100`

### `enum QTextFormat::ObjectTypes`

**作用与语义：**

这个枚举描述了该格式所关联的`QTextObject`类型。
- `QTextFormat::NoObject`：`0`
- `QTextFormat::ImageObject`：`1`
- `QTextFormat::TableObject`：`2`
- `QTextFormat::TableCellObject`：`3`
- `QTextFormat::UserObject`：`0x1000`;第一个可用于特定应用目的的对象。

### `enum QTextFormat::PageBreakFlagflags QTextFormat::PageBreakFlags`

**作用与语义：**

这个枚举描述了打印时分页的执行方式。它映射到对应的 css 属性。
- `QTextFormat::PageBreak_Auto`：`0`;分页点根据当前页面的可用空间自动确定
- `QTextFormat::PageBreak_AlwaysBefore`：`0x001`;页面总是在段落/表格之前被拆开
- `QTextFormat::PageBreak_AlwaysAfter`：`0x010`;总是在段落/表格之后开始新页面
PageBreakFlags 类型是 QFlags 的 typedef<PageBreakFlag>。它存储 PageBreakFlag 值的 OR 组合。

### `enum QTextFormat::Property`

**作用与语义：**

这个枚举描述了格式可以具备的不同属性。
- `QTextFormat::ObjectIndex`：`0x0`;格式化对象的索引。参见`objectIndex()`。
段落与字符属性。
- `QTextFormat::CssFloat`：`0x0800`;帧相对于周围文本的位置
- `QTextFormat::LayoutDirection`：`0x0801`;文档中文本的布局方向（`Qt::LayoutDirection`）。
- `QTextFormat::OutlinePen`：`0x810`
- `QTextFormat::ForegroundBrush`：`0x821`
- `QTextFormat::BackgroundBrush`：`0x820`
- `QTextFormat::BackgroundImageUrl`：`0x823`
段落属性。
- `QTextFormat::BlockAlignment`：`0x1010`
- `QTextFormat::BlockTopMargin`：`0x1030`
- `QTextFormat::BlockBottomMargin`：`0x1031`
- `QTextFormat::BlockLeftMargin`：`0x1032`
- `QTextFormat::BlockRightMargin`：`0x1033`
- `QTextFormat::TextIndent`：`0x1034`
- `QTextFormat::TabPositions`：`0x1035`;指定制表表位置。制表表位置是`QTextOption::Tab`的结构体，存储在`QList`中（内部，`QList`<`QVariant`>中）。
- `QTextFormat::BlockIndent`：`0x1040`
- `QTextFormat::LineHeight`：`0x1048`
- `QTextFormat::LineHeightType`：`0x1049`
- `QTextFormat::BlockNonBreakableLines`：`0x1050`
- `QTextFormat::BlockTrailingHorizontalRulerWidth`：`0x1060`;水平尺元素的宽度。
- `QTextFormat::HeadingLevel`：`0x1070`;标题的层级，例如1对应HTML的H1标签;否则为0。该枚举值已在Qt 5.12中添加。
- `QTextFormat::BlockCodeFence`：`0x1091`;在Markdown代码块周围“围栏”中使用的字符。如果代码块是缩进而非围栏，则该块不应具有此属性。该枚举值已在Qt 5.14中添加。
- `QTextFormat::BlockQuoteLevel`：`0x1080`;该块的嵌套引用深度为1，表示该块是顶层块引号。非块引号块不应具备此属性。该枚举值已在第5.14卷加入。
- `QTextFormat::BlockCodeLanguage`：`0x1090`;预格式化或代码块中的编程语言。不包含代码的块不应具备此属性。该枚举值在Qt 5.14中加入。
- `QTextFormat::BlockMarker`：`0x10A0`;与方块并列展示的装饰类型。该枚举值已在第5.14卷加入。
特征属性。
- `QTextFormat::FontFamily`：`0x2000`;e{此属性已被弃用。}请使用 QTextFormat：：FontFamilies。
- `QTextFormat::FontFamilies`：`0x1FE7`
- `QTextFormat::FontStyleName`：`0x1FE8`
- `QTextFormat::FontPointSize`：`0x2001`
- `QTextFormat::FontPixelSize`：`0x2009`
- `QTextFormat::FontSizeAdjustment`：`0x2002`;指定使用`FontPointSize`或`FontPixelSize`对基础字体大小添加整数调整。
- `QTextFormat::FontFixedPitch`：`0x2008`
- `QTextFormat::FontWeight`：`0x2003`
- `QTextFormat::FontItalic`：`0x2004`
- `QTextFormat::FontUnderline`：`0x2005`;该属性已被弃用。请使用 QTextFormat：：TextUnderlineStyle。
- `QTextFormat::FontOverline`：`0x2006`
- `QTextFormat::FontStrikeOut`：`0x2007`
- `QTextFormat::FontCapitalization`：`FirstFontProperty`;指定将应用于文本的大小写类型。
- `QTextFormat::FontLetterSpacingType`：`0x1FE9`;指定 FontLetterSpacing 属性的含义。默认为 `QFont::PercentageSpacing`。
- `QTextFormat::FontLetterSpacing`：`0x1FE1`;更改字体中单个字母之间的默认间距。值以百分比或绝对值表示，具体取决于 FontLetterSpacingType。默认值为 100%。
- `QTextFormat::FontWordSpacing`：`0x1FE2`;改变单词间的默认间距。正值使单词间距增加相应像素;负值减少字距。
- `QTextFormat::FontStretch`：`0x1FEA`;对应`QFont::Stretch`属性
- `QTextFormat::FontStyleHint`：`0x1FE3`;对应于`QFont::StyleHint`属性
- `QTextFormat::FontStyleStrategy`：`0x1FE4`;对应`QFont::StyleStrategy`属性
- `QTextFormat::FontKerning`：`0x1FE5`;指定字体是否启用了字距调整。
- `QTextFormat::FontHintingPreference`：`0x1FE6`;根据`QFont::HintingPreference`枚举的值控制提示的使用。
- `QTextFormat::FontFeatures`：`0x2010`;[自6.11起]为排版特征分配整数。更多信息请参见 `QFont::setFeature()`。
- `QTextFormat::FontVariableAxes`：`0x2011`;[自6.11起]将浮点数分配给可变字体中的可变轴。更多信息请参见 `QFont::setVariableAxis()`。
- `QTextFormat::TextUnderlineColor`：`0x2020`;指定绘制下划线、上线和划线的颜色。
- `QTextFormat::TextVerticalAlignment`：`0x2021`;根据枚举`QTextCharFormat::VerticalAlignment`值指定文本垂直对齐类型。
- `QTextFormat::TextOutline`：`0x2022`;指定用于绘制文本轮廓的`QPen`。
- `QTextFormat::TextUnderlineStyle`：`0x2023`;根据`QTextCharFormat::UnderlineStyle`枚举的值指定文本下划线样式。
- `QTextFormat::TextToolTip`：`0x2024`;指定文本片段时要显示的（可选）工具提示。
- `QTextFormat::TextSuperScriptBaseline`：`0x2025`;指定上标文本的基准（高度百分比）。
- `QTextFormat::TextSubScriptBaseline`：`0x2026`;指定下标文本的基线（以高度百分比计）。
- `QTextFormat::TextBaselineOffset`：`0x2027`;指定文本的基线（以高度百分比计）。正值则相应地向上移动;负值则向下移动。
- `QTextFormat::IsAnchor`：`0x2030`
- `QTextFormat::AnchorHref`：`0x2031`
- `QTextFormat::AnchorName`：`0x2032`
- `QTextFormat::ObjectType`：`0x2f00`
列表属性。
- `QTextFormat::ListStyle`：`0x3000`;指定列表中项的样式，由`QTextListFormat::Style`枚举的值描述。
- `QTextFormat::ListIndent`：`0x3001`;指定列表所使用的缩进量。
- `QTextFormat::ListNumberPrefix`：`0x3002`;定义数字列表中条目编号前的文本。
- `QTextFormat::ListNumberSuffix`：`0x3003`;定义数字列表中附加在条目编号后的文本。
- `QTextFormat::ListStart (since Qt 6.6)`：`0x3004`;定义列表的第一个值。
桌面与框架属性。
- `QTextFormat::FrameBorder`：`0x4000`
- `QTextFormat::FrameBorderBrush`：`0x4009`
- `QTextFormat::FrameBorderStyle`：`0x4010`;参见枚举`BorderStyle`。
- `QTextFormat::FrameBottomMargin`：`0x4006`
- `QTextFormat::FrameHeight`：`0x4004`
- `QTextFormat::FrameLeftMargin`：`0x4007`
- `QTextFormat::FrameMargin`：`0x4001`
- `QTextFormat::FramePadding`：`0x4002`
- `QTextFormat::FrameRightMargin`：`0x4008`
- `QTextFormat::FrameTopMargin`：`0x4005`
- `QTextFormat::FrameWidth`：`0x4003`
- `QTextFormat::TableCellSpacing`：`0x4102`
- `QTextFormat::TableCellPadding`：`0x4103`
- `QTextFormat::TableColumns`：`0x4100`
- `QTextFormat::TableColumnWidthConstraints`：`0x4101`
- `QTextFormat::TableHeaderRowCount`：`0x4104`
- `QTextFormat::TableBorderCollapse`：`0x4105`;指定`QTextTableFormat::borderCollapse`属性。
表单元特性。
- `QTextFormat::TableCellRowSpan`：`0x4810`
- `QTextFormat::TableCellColumnSpan`：`0x4811`
- `QTextFormat::TableCellLeftPadding`：`0x4814`
- `QTextFormat::TableCellRightPadding`：`0x4815`
- `QTextFormat::TableCellTopPadding`：`0x4812`
- `QTextFormat::TableCellBottomPadding`：`0x4813`
表单元属性，适用于启用`QTextTableFormat::borderCollapse`。
- `QTextFormat::TableCellTopBorder`：`0x4816`
- `QTextFormat::TableCellBottomBorder`：`0x4817`
- `QTextFormat::TableCellLeftBorder`：`0x4818`
- `QTextFormat::TableCellRightBorder`：`0x4819`
- `QTextFormat::TableCellTopBorderStyle`：`0x481a`
- `QTextFormat::TableCellBottomBorderStyle`：`0x481b`
- `QTextFormat::TableCellLeftBorderStyle`：`0x481c`
- `QTextFormat::TableCellRightBorderStyle`：`0x481d`
- `QTextFormat::TableCellTopBorderBrush`：`0x481e`
- `QTextFormat::TableCellBottomBorderBrush`：`0x481f`
- `QTextFormat::TableCellLeftBorderBrush`：`0x4820`
- `QTextFormat::TableCellRightBorderBrush`：`0x4821`
图像属性。
- `QTextFormat::ImageName`：`0x5000`;图片的文件名或来源。
- `QTextFormat::ImageTitle`：`0x5001`;HTML图片标签的标题属性，或Markdown图片链接中URL后面的引号字符串。该枚举值已在Qt 5.14中添加。
- `QTextFormat::ImageAltText`：`0x5002`;HTML图片标签的alt属性，或Markdown图片链接中的图片描述。该枚举值已在Qt 5.14中添加。
- `QTextFormat::ImageWidth`：`0x5010`
- `QTextFormat::ImageHeight`：`0x5011`
- `QTextFormat::ImageQuality`：`0x5014`
- `QTextFormat::ImageMaxWidth`：`0x5015`;这个枚举值是在第6.8季度添加的。
选择属性。
- `QTextFormat::FullWidthSelection`：`0x06000`;当设置为选区的 characterFormat 时，文本的全宽度将被选中。
分页特性。
- `QTextFormat::PageBreakPolicy`：`0x7000`;规定页面如何被拆分。参见`PageBreakFlag`枚举。
- `QTextFormat::UserProperty`：`0x100000`

### `QTextFormat::QTextFormat()`

**作用与语义：**

创建一个带有`InvalidFormat`的新文本格式。

### `[explicit] QTextFormat::QTextFormat(int type)`

**作用与语义：**

创建给定`type`的新文本格式。

### `QTextFormat::QTextFormat(const QTextFormat &other)`

**作用与语义：**

创建具有与`other`文本格式相同属性的新文本格式。

### `[noexcept] QTextFormat::~QTextFormat()`

**作用与语义：**

破坏了这种文本格式。

### `QBrush QTextFormat::background() const`

**作用与语义：**

返回用于绘制文档背景的画笔。

### `bool QTextFormat::boolProperty(int propertyId) const`

**作用与语义：**

返回`propertyId`指定属性的值。如果属性不是QTextFormat：：Bool类型，则返回false。

### `QBrush QTextFormat::brushProperty(int propertyId) const`

**作用与语义：**

返回由`propertyId`给出的属性值;如果属性不是`QMetaType::QBrush`类型，则返回`Qt::NoBrush`。

### `void QTextFormat::clearBackground()`

**作用与语义：**

清除用于绘制文档背景的画刷。将使用默认画刷。

### `void QTextFormat::clearForeground()`

**作用与语义：**

清除用于绘制文档前景的画刷。将使用默认画刷。

### `void QTextFormat::clearProperty(int propertyId)`

**作用与语义：**

清算由`propertyId`给定的属性价值。

### `QColor QTextFormat::colorProperty(int propertyId) const`

**作用与语义：**

返回由`propertyId`给定的属性值;如果该属性不是`QMetaType::QColor`类型，则返回无效颜色。

### `qreal QTextFormat::doubleProperty(int propertyId) const`

**作用与语义：**

返回`propertyId`指定属性的值。如果属性不是类型`QMetaType::Double`或`QMetaType::Float`类型，则返回0。

### `QBrush QTextFormat::foreground() const`

**作用与语义：**

返回用于渲染前景细节的画笔，如文本、框架轮廓和表格边框。

### `bool QTextFormat::hasProperty(int propertyId) const`

**作用与语义：**

如果文本格式具有与给定`propertyId`的属性，则返回`true`;否则返回`false`。

### `int QTextFormat::intProperty(int propertyId) const`

**作用与语义：**

返回`propertyId`指定属性的值。如果属性不是QTextFormat：：Integer类型，则返回0。

### `bool QTextFormat::isBlockFormat() const`

**作用与语义：**

如果此文本格式是 `BlockFormat`，则返回 `true`；否则返回 `false`。

### `bool QTextFormat::isCharFormat() const`

**作用与语义：**

如果此文本格式是 `CharFormat`，则返回 `true`；否则返回 `false`。

### `bool QTextFormat::isEmpty() const`

**作用与语义：**

如果格式不存储任何属性，则返回 true;否则返回 false。

### `bool QTextFormat::isFrameFormat() const`

**作用与语义：**

如果此文本格式是 `FrameFormat`，则返回 `true`；否则返回 `false`。

### `bool QTextFormat::isImageFormat() const`

**作用与语义：**

如果此文本格式是图像格式，则返回 `true`；否则返回 `false`。

### `bool QTextFormat::isListFormat() const`

**作用与语义：**

如果此文本格式是 `ListFormat`，则返回 `true`；否则返回 `false`。

### `bool QTextFormat::isTableCellFormat() const`

**作用与语义：**

如果此文本格式是 `TableCellFormat`，则返回 `true`；否则返回 `false`。

### `bool QTextFormat::isTableFormat() const`

**作用与语义：**

如果此文本格式是 `TableFormat`，则返回 `true`；否则返回 `false`。

### `bool QTextFormat::isValid() const`

**作用与语义：**

如果格式有效（即不`InvalidFormat`），返回`true`;否则返回`false`。

### `Qt::LayoutDirection QTextFormat::layoutDirection() const`

**作用与语义：**

返回文档的布局方向。

### `QTextLength QTextFormat::lengthProperty(int propertyId) const`

**作用与语义：**

返回由`propertyId`给出的属性值。

### `QList<QTextLength> QTextFormat::lengthVectorProperty(int propertyId) const`

**作用与语义：**

返回由 `propertyId` 给定的属性值。如果该属性不是 QTextFormat：：LengthVector 类型，则返回一个空列表。

### `void QTextFormat::merge(const QTextFormat &other)`

**作用与语义：**

将`other`格式与此格式合并;若存在冲突，则优先使用`other`格式。

### `int QTextFormat::objectIndex() const`

**作用与语义：**

返回格式对象的索引，若格式对象无效则返回 -1。

### `int QTextFormat::objectType() const`

**作用与语义：**

返回文本格式的对象类型。

### `QPen QTextFormat::penProperty(int propertyId) const`

**作用与语义：**

返回由`propertyId`给出的属性值;如果属性不是`QMetaType::QPen`类型，则返回`Qt::NoPen`。

### `QMap<int, QVariant> QTextFormat::properties() const`

**作用与语义：**

返回包含该文本格式所有属性的映射。

### `QVariant QTextFormat::property(int propertyId) const`

**作用与语义：**

返回给定`propertyId`所指定的属性。

### `int QTextFormat::propertyCount() const`

**作用与语义：**

返回格式中存储的属性数量。

### `void QTextFormat::setBackground(const QBrush &brush)`

**作用与语义：**

设置用来绘制文档背景的画笔，`brush`指定。

### `void QTextFormat::setForeground(const QBrush &brush)`

**作用与语义：**

将前景画笔设置为指定的`brush`。前景画笔主要用于渲染文本。

### `void QTextFormat::setLayoutDirection(Qt::LayoutDirection direction)`

**作用与语义：**

将文档的布局方向设置为指定的`direction`。

### `void QTextFormat::setObjectIndex(int index)`

**作用与语义：**

设置格式对象的对象`index`。

### `void QTextFormat::setObjectType(int type)`

**作用与语义：**

将文本格式的对象类型设置为`type`。

### `void QTextFormat::setProperty(int propertyId, const QList<QTextLength> &value)`

**作用与语义：**

将`propertyId`所给出属性的值设为`value`。

### `void QTextFormat::setProperty(int propertyId, const QVariant &value)`

**作用与语义：**

将`propertyId`指定的属性设置为给定的`value`。

### `QString QTextFormat::stringProperty(int propertyId) const`

**作用与语义：**

返回由`propertyId`给出的属性值;如果属性不是`QMetaType::QString`类型，则返回空字符串。

### `void QTextFormat::swap(QTextFormat &other)`

**作用与语义：**

将文本格式替换为`other`。此操作非常快速且从未失败。

### `QTextBlockFormat QTextFormat::toBlockFormat() const`

**作用与语义：**

返回该格式为块格式。

### `QTextCharFormat QTextFormat::toCharFormat() const`

**作用与语义：**

返回该格式为字符格式。

### `QTextFrameFormat QTextFormat::toFrameFormat() const`

**作用与语义：**

返回该格式为帧格式。

### `QTextImageFormat QTextFormat::toImageFormat() const`

**作用与语义：**

返回该格式为图像格式。

### `QTextListFormat QTextFormat::toListFormat() const`

**作用与语义：**

返回该格式为列表格式。

### `QTextTableCellFormat QTextFormat::toTableCellFormat() const`

**作用与语义：**

返回该格式为表单元格格式。

### `QTextTableFormat QTextFormat::toTableFormat() const`

**作用与语义：**

返回该格式为表格格式。

### `int QTextFormat::type() const`

**作用与语义：**

返回此格式的类型。

### `QTextFormat::operator QVariant() const`

**作用与语义：**

返回文本格式为`QVariant`。

### `bool QTextFormat::operator!=(const QTextFormat &other) const`

**作用与语义：**

如果此文本格式与 `other` 文本格式不同，则返回 `true`。

### `QTextFormat &QTextFormat::operator=(const QTextFormat &other)`

**作用与语义：**

将`other`文本格式分配给该文本格式，并返回该文本格式的引用。

### `bool QTextFormat::operator==(const QTextFormat &other) const`

**作用与语义：**

如果此文本格式与 `other` 文本格式相同，则返回 `true`。

### `enum PageBreakFlag { PageBreak_Auto, PageBreak_AlwaysBefore, PageBreak_AlwaysAfter }`

**作用与语义：**

这个枚举描述了打印时分页的执行方式。它映射到对应的 css 属性。
- `QTextFormat::PageBreak_Auto`：`0`;分页点根据当前页面的可用空间自动确定
- `QTextFormat::PageBreak_AlwaysBefore`：`0x001`;页面总是在段落/表格之前被拆开
- `QTextFormat::PageBreak_AlwaysAfter`：`0x010`;总是在段落/表格之后开始新页面
PageBreakFlags 类型是 QFlags 的 typedef<PageBreakFlag>。它存储 PageBreakFlag 值的 OR 组合。

### `flags PageBreakFlags`

**作用与语义：**

这个枚举描述了打印时分页的执行方式。它映射到对应的 css 属性。
- `QTextFormat::PageBreak_Auto`：`0`;分页点根据当前页面的可用空间自动确定
- `QTextFormat::PageBreak_AlwaysBefore`：`0x001`;页面总是在段落/表格之前被拆开
- `QTextFormat::PageBreak_AlwaysAfter`：`0x010`;总是在段落/表格之后开始新页面
PageBreakFlags 类型是 QFlags 的 typedef<PageBreakFlag>。它存储 PageBreakFlag 值的 OR 组合。

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

`QTextFormat` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
