# QFontDatabase

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QFontDatabase` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QFontDatabase>`
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

- `enum SystemFont { GeneralFont, FixedFont, TitleFont, SmallestReadableFont }`
- `enum WritingSystem { Any, Latin, Greek, Cyrillic, Armenian, …, Nko }`

### 静态公有成员

- `(since 6.9) void addApplicationEmojiFontFamily(const QString &familyName)`
- `(since 6.8) void addApplicationFallbackFontFamily(QChar::Script script, const QString &familyName)`
- `int addApplicationFont(const QString &fileName)`
- `int addApplicationFontFromData(const QByteArray &fontData)`
- `(since 6.9) QStringList applicationEmojiFontFamilies()`
- `(since 6.8) QStringList applicationFallbackFontFamilies(QChar::Script script)`
- `QStringList applicationFontFamilies(int id)`
- `bool bold(const QString &family, const QString &style)`
- `QStringList families(QFontDatabase::WritingSystem writingSystem = Any)`
- `QFont font(const QString &family, const QString &style, int pointSize)`
- `bool isBitmapScalable(const QString &family, const QString &style = QString())`
- `bool isFixedPitch(const QString &family, const QString &style = QString())`
- `bool isPrivateFamily(const QString &family)`
- `bool isScalable(const QString &family, const QString &style = QString())`
- `bool isSmoothlyScalable(const QString &family, const QString &style = QString())`
- `bool italic(const QString &family, const QString &style)`
- `QList<int> pointSizes(const QString &family, const QString &styleName = QString())`
- `bool removeAllApplicationFonts()`
- `(since 6.9) bool removeApplicationEmojiFontFamily(const QString &familyName)`
- `(since 6.8) bool removeApplicationFallbackFontFamily(QChar::Script script, const QString &familyName)`
- `bool removeApplicationFont(int id)`
- `(since 6.9) void setApplicationEmojiFontFamilies(const QStringList &familyNames)`
- `(since 6.8) void setApplicationFallbackFontFamilies(QChar::Script script, const QStringList &familyNames)`
- `QList<int> smoothSizes(const QString &family, const QString &styleName)`
- `QList<int> standardSizes()`
- `QString styleString(const QFont &font)`
- `QString styleString(const QFontInfo &fontInfo)`
- `QStringList styles(const QString &family)`
- `QFont systemFont(QFontDatabase::SystemFont type)`
- `int weight(const QString &family, const QString &style)`
- `QString writingSystemName(QFontDatabase::WritingSystem writingSystem)`
- `QString writingSystemSample(QFontDatabase::WritingSystem writingSystem)`
- `QList<QFontDatabase::WritingSystem> writingSystems()`
- `QList<QFontDatabase::WritingSystem> writingSystems(const QString &family)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[static, since 6.9] void QFontDatabase::addApplicationEmojiFontFamily(const QString &familyName)`

**作用与语义：**

新增`familyName`作为应用定义的表情字体。
对于显示多色表情符号或表情符号序列，Qt 默认会优先使用系统默认的表情符号字体。有时应用程序可能想要覆盖默认字体，以实现特定的视觉风格或显示系统不支持的表情符号。

### `[static, since 6.8] void QFontDatabase::addApplicationFallbackFontFamily(QChar::Script script, const QString &familyName)`

**作用与语义：**

新增`familyName`作为应用定义的`script`备用字体。
当 Qt 遇到所选字体不支持的字符时，它会搜索备用字体列表以匹配它们。这确保即使主字体不支持，也能将多个脚本组合在一个字符串中。
备选字体列表基于字符串的文字以及其他条件，如系统语言。
虽然系统备份列表通常已足够，但在某些情况下，覆盖默认行为是有用的。其中一种情况是使用应用程序字体作为备份以确保跨平台一致性。
在另一种情况下，应用可能使用具有区域差异的脚本编写，并希望在多个区域以未翻译方式运行。在这种情况下，用与应用语言匹配的备份覆盖本地区域的备份可能很有用。
通过将`familyName`传递给 addApplicationFallbackFontFamily()，当匹配 `script` 缺失字符时，该族将成为首选族。`script`必须是有效脚本（`QChar::Script_Latin` 或更高）。当为同一脚本添加多个字体时，它们会按相反顺序优先排序，因此最后添加的字体族优先检查，依此类推。
注意：Qt的字体匹配算法考虑`QChar::Script_Common`（未确定的文字）和`QChar::Script_Latin`相同。为其中任一添加后备也会适用于另一方。

### `[static] int QFontDatabase::addApplicationFont(const QString &fileName)`

**作用与语义：**

从`fileName`指定的文件加载字体并向应用程序开放。返回一个 ID，可用于再次用 `removeApplicationFont()` 移除字体或检索字体中包含的族名列表。
如果字体无法加载，函数返回 -1。
目前仅支持TrueType字体、TrueType字体集合和OpenType字体。

### `[static] int QFontDatabase::addApplicationFontFromData(const QByteArray &fontData)`

**作用与语义：**

从`fontData`指定的二进制数据加载字体，并向应用程序开放。返回一个 ID，可用于再次用 `removeApplicationFont()` 移除字体或检索字体中包含的族名列表。
如果字体无法加载，函数返回 -1。
目前仅支持TrueType字体、TrueType字体集合和OpenType字体。

### `[static, since 6.9] QStringList QFontDatabase::applicationEmojiFontFamilies()`

**作用与语义：**

返回应用程序定义的表情符号字体家族列表。

### `[static, since 6.8] QStringList QFontDatabase::applicationFallbackFontFamilies(QChar::Script script)`

**作用与语义：**

返回由`addApplicationFallbackFontFamily()`函数之前添加用于`script`的应用定义的退回字体族列表。

### `[static] QStringList QFontDatabase::applicationFontFamilies(int id)`

**作用与语义：**

返回由`id`标识的给定应用字体的字体家族列表。

### `[static] bool QFontDatabase::bold(const QString &family, const QString &style)`

**作用与语义：**

如果带有家族 `family` 和样式 `style` 的字体加粗，返回 `true`;否则返回 `false`。

### `[static] QStringList QFontDatabase::families(QFontDatabase::WritingSystem writingSystem = Any)`

**作用与语义：**

返回支持该`writingSystem`的可用字体家族的排序列表。
如果一个家族存在于多个铸造厂，该字体的返回名称为“family [foundry]”。示例：“Times [Adobe]”、“Times [Cronyx]”、“Palatino”。

### `[static] QFont QFontDatabase::font(const QString &family, const QString &style, int pointSize)`

**作用与语义：**

返回一个具有族`family`、样式`style`和点大小`pointSize`的 `QFont` 对象。如果无法创建匹配的字体，则返回使用应用程序默认字体的 `QFont` 对象。

### `[static] bool QFontDatabase::isBitmapScalable(const QString &family, const QString &style = QString())`

**作用与语义：**

如果具有家族 `family` 和样式 `style` 的字体是可缩放的位图字体，返回 `true`;否则返回 `false`。缩放位图字体通常会产生不美观且几乎难以阅读的结果，因为字体的像素是按比例缩放的。如果需要缩放位图字体，最好将其缩放到`smoothSizes()`返回的固定大小之一。

### `[static] bool QFontDatabase::isFixedPitch(const QString &family, const QString &style = QString())`

**作用与语义：**

如果字体具有家族`family`和样式`style`是固定音高，则返回`true`;否则返回`false`。

### `[static] bool QFontDatabase::isPrivateFamily(const QString &family)`

**作用与语义：**

返回`true`当且仅当`family`字体家族是私有的。
例如，macOS 和 iOS 上就会出现这种情况，系统界面的字体对用户来说是无法访问的。为了完整起见，`QFontDatabase::families()` 返回所有字体家族，包括私有字体。如果你正在开发字体选择控制，应该使用这个功能来隐藏私有字体。

### `[static] bool QFontDatabase::isScalable(const QString &family, const QString &style = QString())`

**作用与语义：**

如果具有家族 `family` 和样式 `style` 的字体可扩展，返回 `true`;否则返回 `false`。

### `[static] bool QFontDatabase::isSmoothlyScalable(const QString &family, const QString &style = QString())`

**作用与语义：**

如果具有家族 `family` 和样式 `style` 的字体可平滑缩放，返回 `true`;否则返回 `false`。如果该函数返回 `true`，可以安全地将该字体缩放到任意大小，且最终效果始终具有吸引力。

### `[static] bool QFontDatabase::italic(const QString &family, const QString &style)`

**作用与语义：**

如果具有家族 `family` 和样式 `style` 的字体为斜体，返回 `true`;否则返回 `false`。

### `[static] QList<int> QFontDatabase::pointSizes(const QString &family, const QString &styleName = QString())`

**作用与语义：**

返回具有家族 `family` 和样式`styleName`的字体可用点大小列表。列表可能是空的。

### `[static] bool QFontDatabase::removeAllApplicationFonts()`

**作用与语义：**

移除之前使用 `addApplicationFont()` 和 `addApplicationFontFromData()` 添加的所有本地应用字体。
如果字体卸载成功，返回`true`;否则返回`false`。

### `[static, since 6.9] bool QFontDatabase::removeApplicationEmojiFontFamily(const QString &familyName)`

**作用与语义：**

移除`familyName`从应用程序定义的表情符号字体列表中，前提是之前已随`addApplicationEmojiFontFamily()`添加。
如果姓氏在列表中，则返回 true;如果不在列表中，则返回 false。

### `[static, since 6.8] bool QFontDatabase::removeApplicationFallbackFontFamily(QChar::Script script, const QString &familyName)`

**作用与语义：**

只要`familyName`之前已随`addApplicationFallbackFontFamily()`添加，则从`script`的应用自定义备用字体列表中移除。
如果姓氏在列表中，则返回 true;如果不在列表中，则返回 false。

### `[static] bool QFontDatabase::removeApplicationFont(int id)`

**作用与语义：**

移除之前加载的应用程序字体，由`id`识别。如果字体卸载成功，返回`true`;否则返回`false`。

### `[static, since 6.9] void QFontDatabase::setApplicationEmojiFontFamilies(const QStringList &familyNames)`

**作用与语义：**

将应用程序定义的表情字体列表设置为`familyNames`。

### `[static, since 6.8] void QFontDatabase::setApplicationFallbackFontFamilies(QChar::Script script, const QStringList &familyNames)`

**作用与语义：**

设置应用程序定义的`script` to `familyNames` 的备用字体列表。
当 Qt 在 `script` 中遇到当前字体不支持的字符时，它会按`familyNames`的族顺序从头到尾检查，直到找到匹配的字符。更多详情请参见 `addApplicationFallbackFontFamily()`。
该函数覆盖当前应用程序定义的备用字体列表，用于`script`。

### `[static] QList<int> QFontDatabase::smoothSizes(const QString &family, const QString &styleName)`

**作用与语义：**

返回具有族`family`和样式`styleName`且外观吸引人的字体点大小。列表可能是空的。对于不可缩放字体和位图可扩展字体，该函数等价于`pointSizes()`。

### `[static] QList<int> QFontDatabase::standardSizes()`

**作用与语义：**

返回标准字体大小列表。

### `[static] QString QFontDatabase::styleString(const QFont &font)`

**作用与语义：**

返回描述 `font` 样式的字符串。例如，“粗体 斜体”、“粗体”、“斜体”或“常规”。可能返回空字符串。

### `[static] QString QFontDatabase::styleString(const QFontInfo &fontInfo)`

**作用与语义：**

返回描述 `fontInfo` 风格的字符串。例如，“加粗斜体”、“加粗”、“斜体”或“常规”。可能返回空字符串。

### `[static] QStringList QFontDatabase::styles(const QString &family)`

**作用与语义：**

返回该字体家族可用的样式列表`family`。一些示例样式：“Light”、“Light Italic”、“Brun”、“Oblique”、“Demi”。该列表可能是空白的。

### `[static] QFont QFontDatabase::systemFont(QFontDatabase::SystemFont type)`

**作用与语义：**

返回最适合特定`type`的字体，确保与系统的外观和感觉完美集成。

### `[static] int QFontDatabase::weight(const QString &family, const QString &style)`

**作用与语义：**

返回具有家族`family`和样式`style`的字体权重。如果没有此类家族和样式组合，返回为-1。

### `[static] QString QFontDatabase::writingSystemName(QFontDatabase::WritingSystem writingSystem)`

**作用与语义：**

返回`writingSystem`的名称（例如用于在对话框中显示给用户）。

### `[static] QString QFontDatabase::writingSystemSample(QFontDatabase::WritingSystem writingSystem)`

**作用与语义：**

返回包含`writingSystem`示例字符的字符串。

### `[static] QList<QFontDatabase::WritingSystem> QFontDatabase::writingSystems()`

**作用与语义：**

返回一个排序的可用书写系统列表。这是根据系统上所有已安装字体的信息生成的列表。

### `[static] QList<QFontDatabase::WritingSystem> QFontDatabase::writingSystems(const QString &family)`

**作用与语义：**

返回给定字体支持的书写系统排序列表`family`。

### `enum SystemFont { GeneralFont, FixedFont, TitleFont, SmallestReadableFont }`

**作用与语义：**

- `QFontDatabase::GeneralFont`：`0`;默认系统字体。
- `QFontDatabase::FixedFont`：`1`;系统推荐的固定字体。
- `QFontDatabase::TitleFont`：`2`;系统标准字体用于标题。
- `QFontDatabase::SmallestReadableFont`：`3`;最小的系统可读字体。

### `enum WritingSystem { Any, Latin, Greek, Cyrillic, Armenian, …, Nko }`

**作用与语义：**

- `QFontDatabase::Any`：`0`
- `QFontDatabase::Latin`：`1`
- `QFontDatabase::Greek`：`2`
- `QFontDatabase::Cyrillic`：`3`
- `QFontDatabase::Armenian`：`4`
- `QFontDatabase::Hebrew`：`5`
- `QFontDatabase::Arabic`：`6`
- `QFontDatabase::Syriac`：`7`
- `QFontDatabase::Thaana`：`8`
- `QFontDatabase::Devanagari`：`9`
- `QFontDatabase::Bengali`：`10`
- `QFontDatabase::Gurmukhi`：`11`
- `QFontDatabase::Gujarati`：`12`
- `QFontDatabase::Oriya`：`13`
- `QFontDatabase::Tamil`：`14`
- `QFontDatabase::Telugu`：`15`
- `QFontDatabase::Kannada`：`16`
- `QFontDatabase::Malayalam`：`17`
- `QFontDatabase::Sinhala`：`18`
- `QFontDatabase::Thai`：`19`
- `QFontDatabase::Lao`：`20`
- `QFontDatabase::Tibetan`：`21`
- `QFontDatabase::Myanmar`：`22`
- `QFontDatabase::Georgian`：`23`
- `QFontDatabase::Khmer`：`24`
- `QFontDatabase::SimplifiedChinese`：`25`
- `QFontDatabase::TraditionalChinese`：`26`
- `QFontDatabase::Japanese`：`27`
- `QFontDatabase::Korean`：`28`
- `QFontDatabase::Vietnamese`：`29`
- `QFontDatabase::Symbol`：`30`
- `QFontDatabase::Other`：`Symbol`;（与符号相同）
- `QFontDatabase::Ogham`：`31`
- `QFontDatabase::Runic`：`32`
- `QFontDatabase::Nko`：`33`

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

`QFontDatabase` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
