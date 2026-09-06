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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 69 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QTextCharFormat::FontPropertiesInheritanceBehavior`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QTextCharFormat` 暴露的类型声明 `字体、Properties、Inheritance、Behavior`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:FontPropertiesInheritanceBehavior`。
- 属性名：`QTextCharFormat`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QTextCharFormat::UnderlineStyle`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QTextCharFormat` 暴露的类型声明 `Underline、Style`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:UnderlineStyle`。
- 属性名：`QTextCharFormat`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QTextCharFormat::VerticalAlignment`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QTextCharFormat` 暴露的类型声明 `垂直、对齐方式`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:VerticalAlignment`。
- 属性名：`QTextCharFormat`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextCharFormat::QTextCharFormat()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextCharFormat` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QTextCharFormat::anchorHref() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCharFormat::anchorHref` 用于计算、查询或取得与“anchor、Href”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringList QTextCharFormat::anchorNames() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCharFormat::anchorNames` 用于计算、查询或取得与“anchor、Names”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QStringList`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStringList`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] qreal QTextCharFormat::baselineOffset() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCharFormat::baselineOffset` 用于计算、查询或取得与“baseline、Offset”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFont QTextCharFormat::font() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCharFormat::font` 用于计算、查询或取得与“字体”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QFont`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QFont`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFont::Capitalization QTextCharFormat::fontCapitalization() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCharFormat::fontCapitalization` 用于计算、查询或取得与“字体、Capitalization”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QFont::Capitalization`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QFont::Capitalization`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVariant QTextCharFormat::fontFamilies() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCharFormat::fontFamilies` 用于计算、查询或取得与“字体、Families”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QVariant`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVariant`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.11] QMap<QFont::Tag, quint32> QTextCharFormat::fontFeatures() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCharFormat::fontFeatures` 用于计算、查询或取得与“字体、Features”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMap<QFont::Tag, quint32>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMap<QFont::Tag, quint32>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QTextCharFormat::fontFixedPitch() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCharFormat::fontFixedPitch` 用于计算、查询或取得与“字体、Fixed、Pitch”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFont::HintingPreference QTextCharFormat::fontHintingPreference() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCharFormat::fontHintingPreference` 用于计算、查询或取得与“字体、Hinting、Preference”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QFont::HintingPreference`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QFont::HintingPreference`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QTextCharFormat::fontItalic() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCharFormat::fontItalic` 用于计算、查询或取得与“字体、Italic”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QTextCharFormat::fontKerning() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCharFormat::fontKerning` 用于计算、查询或取得与“字体、Kerning”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal QTextCharFormat::fontLetterSpacing() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCharFormat::fontLetterSpacing` 用于计算、查询或取得与“字体、Letter、Spacing”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFont::SpacingType QTextCharFormat::fontLetterSpacingType() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCharFormat::fontLetterSpacingType` 用于计算、查询或取得与“字体、Letter、Spacing、类型”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QFont::SpacingType`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QFont::SpacingType`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QTextCharFormat::fontOverline() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCharFormat::fontOverline` 用于计算、查询或取得与“字体、Overline”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal QTextCharFormat::fontPointSize() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCharFormat::fontPointSize` 用于计算、查询或取得与“字体、Point、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QTextCharFormat::fontStretch() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCharFormat::fontStretch` 用于计算、查询或取得与“字体、Stretch”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QTextCharFormat::fontStrikeOut() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCharFormat::fontStrikeOut` 用于计算、查询或取得与“字体、Strike、Out”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFont::StyleHint QTextCharFormat::fontStyleHint() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCharFormat::fontStyleHint` 用于计算、查询或取得与“字体、Style、Hint”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QFont::StyleHint`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QFont::StyleHint`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVariant QTextCharFormat::fontStyleName() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCharFormat::fontStyleName` 用于计算、查询或取得与“字体、Style、名称”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QVariant`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVariant`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFont::StyleStrategy QTextCharFormat::fontStyleStrategy() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCharFormat::fontStyleStrategy` 用于计算、查询或取得与“字体、Style、Strategy”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QFont::StyleStrategy`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QFont::StyleStrategy`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QTextCharFormat::fontUnderline() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCharFormat::fontUnderline` 用于计算、查询或取得与“字体、Underline”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.11] QMap<QFont::Tag, float> QTextCharFormat::fontVariableAxes() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCharFormat::fontVariableAxes` 用于计算、查询或取得与“字体、Variable、Axes”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMap<QFont::Tag, float>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMap<QFont::Tag, float>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QTextCharFormat::fontWeight() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCharFormat::fontWeight` 用于计算、查询或取得与“字体、Weight”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal QTextCharFormat::fontWordSpacing() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCharFormat::fontWordSpacing` 用于计算、查询或取得与“字体、Word、Spacing”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QTextCharFormat::isAnchor() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isAnchor`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QTextCharFormat::isValid() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isValid`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCharFormat::setAnchor(bool anchor)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setAnchor`。调用它会改变 `QTextCharFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `anchor`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCharFormat::setAnchorHref(const QString &value)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setAnchorHref`。调用它会改变 `QTextCharFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `value`：类型为 `const QString &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCharFormat::setAnchorNames(const QStringList &names)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setAnchorNames`。调用它会改变 `QTextCharFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `names`：类型为 `const QStringList &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] void QTextCharFormat::setBaselineOffset(qreal baseline)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setBaselineOffset`。调用它会改变 `QTextCharFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `baseline`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCharFormat::setFont(const QFont &font, QTextCharFormat::FontPropertiesInheritanceBehavior behavior = FontPropertiesAll)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFont`。调用它会改变 `QTextCharFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `font`：类型为 `const QFont &`。没有默认值，调用时必须提供。传入 `const QFont &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `behavior`：类型为 `QTextCharFormat::FontPropertiesInheritanceBehavior`。默认值为 `FontPropertiesAll`。传入 `QTextCharFormat::FontPropertiesInheritanceBehavior` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCharFormat::setFontCapitalization(QFont::Capitalization capitalization)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFontCapitalization`。调用它会改变 `QTextCharFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `capitalization`：类型为 `QFont::Capitalization`。没有默认值，调用时必须提供。传入 `QFont::Capitalization` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCharFormat::setFontFamilies(const QStringList &families)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFontFamilies`。调用它会改变 `QTextCharFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `families`：类型为 `const QStringList &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.11] void QTextCharFormat::setFontFeatures(const QMap<QFont::Tag, quint32> &fontFeatures)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFontFeatures`。调用它会改变 `QTextCharFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `fontFeatures`：类型为 `const QMap<QFont::Tag, quint32> &`。没有默认值，调用时必须提供。传入 `const QMap<QFont::Tag, quint32> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCharFormat::setFontFixedPitch(bool fixedPitch)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFontFixedPitch`。调用它会改变 `QTextCharFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `fixedPitch`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCharFormat::setFontHintingPreference(QFont::HintingPreference hintingPreference)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFontHintingPreference`。调用它会改变 `QTextCharFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `hintingPreference`：类型为 `QFont::HintingPreference`。没有默认值，调用时必须提供。传入 `QFont::HintingPreference` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCharFormat::setFontItalic(bool italic)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFontItalic`。调用它会改变 `QTextCharFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `italic`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCharFormat::setFontKerning(bool enable)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFontKerning`。调用它会改变 `QTextCharFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enable`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCharFormat::setFontLetterSpacing(qreal spacing)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFontLetterSpacing`。调用它会改变 `QTextCharFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `spacing`：类型为 `qreal`。没有默认值，调用时必须提供。相邻项目之间的间隔，通常以像素表示；它通常不等于外边距。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCharFormat::setFontLetterSpacingType(QFont::SpacingType letterSpacingType)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFontLetterSpacingType`。调用它会改变 `QTextCharFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `letterSpacingType`：类型为 `QFont::SpacingType`。没有默认值，调用时必须提供。传入 `QFont::SpacingType` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCharFormat::setFontOverline(bool overline)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFontOverline`。调用它会改变 `QTextCharFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `overline`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCharFormat::setFontPointSize(qreal size)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFontPointSize`。调用它会改变 `QTextCharFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `size`：类型为 `qreal`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCharFormat::setFontStretch(int factor)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFontStretch`。调用它会改变 `QTextCharFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `factor`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCharFormat::setFontStrikeOut(bool strikeOut)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFontStrikeOut`。调用它会改变 `QTextCharFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `strikeOut`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCharFormat::setFontStyleHint(QFont::StyleHint hint, QFont::StyleStrategy strategy = QFont::PreferDefault)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFontStyleHint`。调用它会改变 `QTextCharFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `hint`：类型为 `QFont::StyleHint`。没有默认值，调用时必须提供。传入 `QFont::StyleHint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `strategy`：类型为 `QFont::StyleStrategy`。默认值为 `QFont::PreferDefault`。传入 `QFont::StyleStrategy` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCharFormat::setFontStyleName(const QString &styleName)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFontStyleName`。调用它会改变 `QTextCharFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `styleName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCharFormat::setFontStyleStrategy(QFont::StyleStrategy strategy)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFontStyleStrategy`。调用它会改变 `QTextCharFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `strategy`：类型为 `QFont::StyleStrategy`。没有默认值，调用时必须提供。传入 `QFont::StyleStrategy` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCharFormat::setFontUnderline(bool underline)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFontUnderline`。调用它会改变 `QTextCharFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `underline`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.11] void QTextCharFormat::setFontVariableAxes(const QMap<QFont::Tag, float> &fontVariableAxes)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFontVariableAxes`。调用它会改变 `QTextCharFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `fontVariableAxes`：类型为 `const QMap<QFont::Tag, float> &`。没有默认值，调用时必须提供。传入 `const QMap<QFont::Tag, float> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCharFormat::setFontWeight(int weight)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFontWeight`。调用它会改变 `QTextCharFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `weight`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCharFormat::setFontWordSpacing(qreal spacing)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFontWordSpacing`。调用它会改变 `QTextCharFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `spacing`：类型为 `qreal`。没有默认值，调用时必须提供。相邻项目之间的间隔，通常以像素表示；它通常不等于外边距。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] void QTextCharFormat::setSubScriptBaseline(qreal baseline)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSubScriptBaseline`。调用它会改变 `QTextCharFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `baseline`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] void QTextCharFormat::setSuperScriptBaseline(qreal baseline)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSuperScriptBaseline`。调用它会改变 `QTextCharFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `baseline`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCharFormat::setTextOutline(const QPen &pen)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setTextOutline`。调用它会改变 `QTextCharFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `pen`：类型为 `const QPen &`。没有默认值，调用时必须提供。传入 `const QPen &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCharFormat::setToolTip(const QString &text)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setToolTip`。调用它会改变 `QTextCharFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCharFormat::setUnderlineColor(const QColor &color)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setUnderlineColor`。调用它会改变 `QTextCharFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `color`：类型为 `const QColor &`。没有默认值，调用时必须提供。传入 `const QColor &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCharFormat::setUnderlineStyle(QTextCharFormat::UnderlineStyle style)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setUnderlineStyle`。调用它会改变 `QTextCharFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `style`：类型为 `QTextCharFormat::UnderlineStyle`。没有默认值，调用时必须提供。传入 `QTextCharFormat::UnderlineStyle` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextCharFormat::setVerticalAlignment(QTextCharFormat::VerticalAlignment alignment)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setVerticalAlignment`。调用它会改变 `QTextCharFormat` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `alignment`：类型为 `QTextCharFormat::VerticalAlignment`。没有默认值，调用时必须提供。对齐标志的组合，例如 `Qt::AlignLeft | Qt::AlignVCenter`；它描述内容在已分配区域中的位置，不负责分配剩余空间。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] qreal QTextCharFormat::subScriptBaseline() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCharFormat::subScriptBaseline` 用于计算、查询或取得与“sub、Script、Baseline”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] qreal QTextCharFormat::superScriptBaseline() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCharFormat::superScriptBaseline` 用于计算、查询或取得与“super、Script、Baseline”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPen QTextCharFormat::textOutline() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCharFormat::textOutline` 用于计算、查询或取得与“文本、Outline”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPen`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPen`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QTextCharFormat::toolTip() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toolTip`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QColor QTextCharFormat::underlineColor() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCharFormat::underlineColor` 用于计算、查询或取得与“underline、Color”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QColor`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QColor`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextCharFormat::UnderlineStyle QTextCharFormat::underlineStyle() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCharFormat::underlineStyle` 用于计算、查询或取得与“underline、Style”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QTextCharFormat::UnderlineStyle`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextCharFormat::UnderlineStyle`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextCharFormat::VerticalAlignment QTextCharFormat::verticalAlignment() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextCharFormat::verticalAlignment` 用于计算、查询或取得与“垂直、对齐方式”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QTextCharFormat::VerticalAlignment`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextCharFormat::VerticalAlignment`。
- 参数：无。

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

`QTextCharFormat` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
