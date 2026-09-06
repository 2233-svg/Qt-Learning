# QRegularExpression

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 正则表达式模式对象，负责编译匹配规则并创建匹配结果。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QRegularExpression`：正则表达式模式对象，负责编译匹配规则并创建匹配结果。

**内部模型：** 这类类型通常可以按值传递、复制和返回。许多 Qt 容器、字符串和图像采用隐式共享：复制时共享数据，发生写操作时才 detach。这样便于 API 传值，但获取原始指针或长期持有引用时必须考虑对象修改和生命周期。

**适用场景：** 先确认值的有效性和表示格式，再调用查询、转换或修改 API；处理文本时区分 Unicode 和字节编码，处理图像时确认 format，处理 URL/路径时使用 Qt 的解析 API 而不是手写字符串规则。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要把空值当成业务成功；不要保存临时对象的内部指针；不要把 QString 当二进制缓冲区；不要假定隐式共享让并发写入自动安全。

## 2. 依赖与对象关系

- 头文件：`#include <QRegularExpression>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

这类类型通常可以按值传递、复制和返回。许多 Qt 容器、字符串和图像采用隐式共享：复制时共享数据，发生写操作时才 detach。这样便于 API 传值，但获取原始指针或长期持有引用时必须考虑对象修改和生命周期。

### 状态、生命周期和线程

**生命周期：** 值对象由作用域、容器或调用者管理，不使用 parent 和 deleteLater。跨线程传递副本通常比传递 QObject 安全，但共享数据在写入时仍可能发生复制，性能和内存峰值要结合数据规模判断。

**状态与结果：** 重点区分空值、无效值、默认值和已初始化值。例如空字符串、空 URL、null 图像和无效索引不一定表示同一件事；转换函数的失败结果要通过对应的状态查询确认。

**线程与事件循环：** 值类型本身通常可以复制后跨线程传递；不要把 data()/bits()/constData() 得到的指针当成跨线程长期有效的所有权。大对象频繁写入会触发 detach，应避免不必要的复制和格式转换。

## 3. 直接使用

先确认值的有效性和表示格式，再调用查询、转换或修改 API；处理文本时区分 Unicode 和字节编码，处理图像时确认 format，处理 URL/路径时使用 Qt 的解析 API 而不是手写字符串规则。 使用时通常按这个过程组织：构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum MatchOption { NoMatchOption, AnchoredMatchOption, AnchorAtOffsetMatchOption, DontCheckSubjectStringMatchOption }`
- `flags MatchOptions`
- `enum MatchType { NormalMatch, PartialPreferCompleteMatch, PartialPreferFirstMatch, NoMatch }`
- `enum PatternOption { NoPatternOption, CaseInsensitiveOption, DotMatchesEverythingOption, MultilineOption, ExtendedPatternSyntaxOption, …, UseUnicodePropertiesOption }`
- `flags PatternOptions`
- `(since 6.0) enum WildcardConversionOption { DefaultWildcardConversion, UnanchoredWildcardConversion, NonPathWildcardConversion }`
- `flags WildcardConversionOptions`

### 公有函数

- `QRegularExpression()`
- `QRegularExpression(const QString &pattern, QRegularExpression::PatternOptions options = NoPatternOption)`
- `QRegularExpression(const QRegularExpression &re)`
- `(since 6.1) QRegularExpression(QRegularExpression &&re)`
- `~QRegularExpression()`
- `int captureCount() const`
- `QString errorString() const`
- `QRegularExpressionMatchIterator globalMatch(const QString &subject, qsizetype offset = 0, QRegularExpression::MatchType matchType = NormalMatch, QRegularExpression::MatchOptions matchOptions = NoMatchOption) const`
- `(since 6.5) QRegularExpressionMatchIterator globalMatchView(QStringView subjectView, qsizetype offset = 0, QRegularExpression::MatchType matchType = NormalMatch, QRegularExpression::MatchOptions matchOptions = NoMatchOption) const`
- `bool isValid() const`
- `QRegularExpressionMatch match(const QString &subject, qsizetype offset = 0, QRegularExpression::MatchType matchType = NormalMatch, QRegularExpression::MatchOptions matchOptions = NoMatchOption) const`
- `(since 6.5) QRegularExpressionMatch matchView(QStringView subjectView, qsizetype offset = 0, QRegularExpression::MatchType matchType = NormalMatch, QRegularExpression::MatchOptions matchOptions = NoMatchOption) const`
- `QStringList namedCaptureGroups() const`
- `void optimize() const`
- `QString pattern() const`
- `qsizetype patternErrorOffset() const`
- `QRegularExpression::PatternOptions patternOptions() const`
- `void setPattern(const QString &pattern)`
- `void setPatternOptions(QRegularExpression::PatternOptions options)`
- `void swap(QRegularExpression &other)`
- `QRegularExpression & operator=(QRegularExpression &&re)`
- `QRegularExpression & operator=(const QRegularExpression &re)`

### 静态公有成员

- `QString anchoredPattern(QStringView expression)`
- `QString anchoredPattern(const QString &expression)`
- `QString escape(QStringView str)`
- `QString escape(const QString &str)`
- `(since 6.0) QRegularExpression fromWildcard(QStringView pattern, Qt::CaseSensitivity cs = Qt::CaseInsensitive, QRegularExpression::WildcardConversionOptions options = DefaultWildcardConversion)`
- `QString wildcardToRegularExpression(QStringView pattern, QRegularExpression::WildcardConversionOptions options = DefaultWildcardConversion)`
- `QString wildcardToRegularExpression(const QString &pattern, QRegularExpression::WildcardConversionOptions options = DefaultWildcardConversion)`

### 相关非成员函数

- `size_t qHash(const QRegularExpression &key, size_t seed = 0)`
- `bool operator!=(const QRegularExpression &lhs, const QRegularExpression &rhs)`
- `QDataStream & operator<<(QDataStream &out, const QRegularExpression &re)`
- `QDebug operator<<(QDebug debug, QRegularExpression::PatternOptions patternOptions)`
- `QDebug operator<<(QDebug debug, const QRegularExpression &re)`
- `bool operator==(const QRegularExpression &lhs, const QRegularExpression &rhs)`
- `QDataStream & operator>>(QDataStream &in, QRegularExpression &re)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QRegularExpression::MatchOptionflags QRegularExpression::MatchOptions`

**作用与语义：**

- `QRegularExpression::NoMatchOption`：`0x0000`;不设置匹配选项。
- `QRegularExpression::AnchoredMatchOption`：`AnchorAtOffsetMatchOption`;改用 AnchorAtOffsetMatchOption。
- `QRegularExpression::AnchorAtOffsetMatchOption`：`0x0001`;匹配被限制必须从传递给`match()`的偏移开始，才能成功，即使模式字符串中没有任何元字符锚定匹配。注意，通过该选项不会将匹配结束点锚定到主语的结尾;如果你想完全锚定正则表达式，可以使用`anchoredPattern()`。该枚举值在Qt 6.0中引入。
- `QRegularExpression::DontCheckSubjectStringMatchOption`：`0x0002`;在尝试匹配前，主旨字符串不会检查其 UTF-16 有效性。使用此选项时需极度谨慎，因为尝试匹配无效字符串可能导致程序崩溃和/或构成安全问题。该枚举值在 Qt 5.4 中引入。
MatchOptions 类型是 QFlags 的 typedef<MatchOption>。它存储 MatchOption 值的 OR 组合。

### `enum QRegularExpression::MatchType`

**作用与语义：**

MatchType 枚举定义了应针对主题字符串尝试匹配的类型。
- `QRegularExpression::NormalMatch`：`0`;正常匹配完成。
- `QRegularExpression::PartialPreferCompleteMatch`：`1`;模式字符串部分匹配主题字符串。如果发现部分匹配，则记录该匹配，并照常尝试其他匹配方案。如果找到完全匹配，则优先采用该匹配而非部分匹配;此时只报告完整匹配。如果找不到完全匹配（仅部分匹配），则报告部分匹配。
- `QRegularExpression::PartialPreferFirstMatch`：`2`;模式字符串部分与主语字符串匹配。如果发现部分匹配，则匹配停止并报告部分匹配。此时不尝试其他匹配方案（可能导致完全匹配）。此外，这种匹配类型假设主语字符串仅为更大文本的子字符串，且（在本文本中）主语字符串末尾之外还有其他字符。这可能导致令人惊讶的结果;更多细节请参见部分匹配部分的讨论。
- `QRegularExpression::NoMatch`：`3`;不进行匹配。该值由默认构造的构造`QRegularExpressionMatch`或`QRegularExpressionMatchIterator`返回为匹配类型。使用该匹配类型对用户来说并不太实用，因为从未发生匹配。该枚举值在第5.1个季度引入。

### `enum QRegularExpression::PatternOptionflags QRegularExpression::PatternOptions`

**作用与语义：**

PatternOption 枚举定义了模式字符串应如何解释的修饰符，从而定义模式与主题字符串匹配的方式。
- `QRegularExpression::NoPatternOption`：`0x0000`;不设置任何图案选项。
- `QRegularExpression::CaseInsensitiveOption`：`0x0001`;该模式应以不区分大小写的方式与主语字符串匹配。该选项对应于 Perl 正则表达式中的 /i 修饰符。
- `QRegularExpression::DotMatchesEverythingOption`：`0x0002`;模式字符串中的点元字符（`.`）允许匹配主语字符串中的任意字符，包括换行（通常点不匹配换行）。该选项对应于 Perl 正则表达式中的 `/s` 修饰符。
- `QRegularExpression::MultilineOption`：`0x0004`;模式字符串中的插入符（`^`）和美元元字符（`$`）分别允许在主题字符串中任何换行之后和之前，以及主题字符串的开头和末尾匹配。该选项对应于 Perl 正则表达式中的 `/m` 修饰符。
- `QRegularExpression::ExtendedPatternSyntaxOption`：`0x0008`;模式字符串中未转义且不属于字符类的空白部分将被忽略。此外，字符类外的未脱义升号（#）会导致后续所有字符（包括第一行）被忽略。这可用于提高模式字符串的可读性，并将注释放入正则表达式中;这在从文件加载或用户编写的模式字符串中尤为有用，因为在C代码中，字符串文字规则总能将注释置于模式字符串之外。该选项对应Perl正则表达式中的`/x`修饰符。
- `QRegularExpression::InvertedGreedinessOption`：`0x0010`;量词的贪婪程度是反转的：`*`、`+`、`?`、`{m,n}`等变得懒惰，而它们的懒惰版本（`*?`、`+?`、`??`、`{m,n}?`等）变得贪婪。在Perl正则表达式中没有类似的选项。
- `QRegularExpression::DontCaptureOption`：`0x0020`;非命名捕获群不捕获子串;命名捕获群仍然按预期工作，且对应整个匹配的隐式捕获组编号0也同样有效。Perl正则表达式中没有对此选项的对应。
- `QRegularExpression::UseUnicodePropertiesOption`：`0x0040`;`\w`、`\d`等字符类的含义，以及它们对应的字符（`\W`、`\D`等）的含义，从仅匹配ASCII字符改为匹配具有相应Unicode属性的任意字符。例如，`\d`被更改为匹配任何具有Unicode的Nd（十进制数字）属性的字符;`\w`匹配任何具有Unicode字母L（字母）或N（数字）属性的字符，加上下划线，依此类推。该选项对应于 Perl 正则表达式中的 `/u` 修饰符。
PatternOptions 类型是 QFlags 的 typedef<PatternOption>。它存储 PatternOption 值的 OR 组合。

### `[since 6.0] enum QRegularExpression::WildcardConversionOptionflags QRegularExpression::WildcardConversionOptions`

**作用与语义：**

WildcardConversionOption 枚举定义了将万用字块模式转换为正则表达式模式的方式修饰符。
- `QRegularExpression::DefaultWildcardConversion`：`0x0`;不设置转换选项。
- `QRegularExpression::UnanchoredWildcardConversion`：`0x1`;转换不会锚定模式。这允许部分字符串匹配百搭符表达式。
- `QRegularExpression::NonPathWildcardConversion (since Qt 6.6)`：`0x2`;转换时不会将模式解释为文件路径的滚动。
该枚举是在Qt 6.0中引入的。
WildcardConversionOptions 类型是 QFlags 的 typedef<WildcardConversionOption>。它存储 WildcardConversionOption 值的 OR 组合。

### `QRegularExpression::QRegularExpression()`

**作用与语义：**

构造一个带有空模式且无模式选项的QRegularExpression对象。

### `[explicit] QRegularExpression::QRegularExpression(const QString &pattern, QRegularExpression::PatternOptions options = NoPatternOption)`

**作用与语义：**

使用给定`pattern`作为模式，`options`作为模式选项，构建一个QRegularExpression对象。

### `[noexcept] QRegularExpression::QRegularExpression(const QRegularExpression &re)`

**作用与语义：**

构建一个QRegularExpression对象作为`re`的副本。

### `[constexpr noexcept, since 6.1] QRegularExpression::QRegularExpression(QRegularExpression &&re)`

**作用与语义：**

通过从 到 `re` 构建 QRegularExpression 对象。
注意，移出 QRegularExpression 只能被销毁或赋值。调用除析构函数或赋值算符外的其他函数效果尚无定义。

### `[noexcept] QRegularExpression::~QRegularExpression()`

**作用与语义：**

摧毁`QRegularExpression`物体。

### `[static] QString QRegularExpression::anchoredPattern(QStringView expression)`

**作用与语义：**

返回包裹在`\A`和`\z`锚之间的`expression`，用于精确匹配。

### `[static] QString QRegularExpression::anchoredPattern(const QString &expression)`

**作用与语义：**

返回包裹在`\A`和`\z`锚之间的`expression`，用于精确匹配。

### `int QRegularExpression::captureCount() const`

**作用与语义：**

返回模式字符串内捕获群的数量，若正则表达式无效则返回-1。
注意：隐式捕获群0未包含在返回的数字中。

### `QString QRegularExpression::errorString() const`

**作用与语义：**

返回检查正则表达式有效性时发现错误的文本描述，若未发现错误则返回“无错误”。

### `[static] QString QRegularExpression::escape(QStringView str)`

**作用与语义：**

转义 `str` 的所有字符，使其在用作正则表达式模式字符串时不再具有特殊含义，并返回转义字符串。例如：
这对于从任意字符串构建模式非常方便：
注意：该函数实现了Perl的引用元算法，并以反斜杠逃脱`str`中所有字符，除了`[A-Z]`、`[a-z]`和`[0-9]`范围内的字符，以及下划线（`_`）字符。Perl 唯一的区别是，字面上的 NUL `str` 中转义时，转义时序列为 `"\\0"`（反斜杠 `'0'`），而不是 `"\\\0"`（反斜杠`NUL`）。

**官方示例：**

```cpp
 QString escaped = QRegularExpression::escape("a(x) = f(x) + g(x)");
 // escaped == "a\\(x\\)\\ \\=\\ f\\(x\\)\\ \\+\\ g\\(x\\)"
```

### `[static] QString QRegularExpression::escape(const QString &str)`

**作用与语义：**

转义 `str` 的所有字符，使其在用作正则表达式模式字符串时不再具有特殊含义，并返回转义字符串。例如：
这对于从任意字符串构建模式非常方便：
注意：该函数实现了Perl的引用元算法，并以反斜杠逃脱`str`中所有字符，除了`[A-Z]`、`[a-z]`和`[0-9]`范围内的字符，以及下划线（`_`）字符。Perl 唯一的区别是，字面上的 NUL `str` 中转义时，转义时序列为 `"\\0"`（反斜杠 `'0'`），而不是 `"\\\0"`（反斜杠`NUL`）。

**官方示例：**

```cpp
 QString escaped = QRegularExpression::escape("a(x) = f(x) + g(x)");
 // escaped == "a\\(x\\)\\ \\=\\ f\\(x\\)\\ \\+\\ g\\(x\\)"
```

### `[static, since 6.0] QRegularExpression QRegularExpression::fromWildcard(QStringView pattern, Qt::CaseSensitivity cs = Qt::CaseInsensitive, QRegularExpression::WildcardConversionOptions options = DefaultWildcardConversion)`

**作用与语义：**

返回球状模式的正则表达式`pattern`。如果`cs` `Qt::CaseSensitive`并根据`options`转换，正则表达式将不分大小写。
等价于。

**官方示例：**

```cpp
 auto reOptions = cs == Qt::CaseSensitive ? QRegularExpression::NoPatternOption :
                                            QRegularExpression::CaseInsensitiveOption;
 return QRegularExpression(wildcardToRegularExpression(str, options), reOptions);
```

### `QRegularExpressionMatchIterator QRegularExpression::globalMatch(const QString &subject, qsizetype offset = 0, QRegularExpression::MatchType matchType = NormalMatch, QRegularExpression::MatchOptions matchOptions = NoMatchOption) const`

**作用与语义：**

尝试对正则表达式与给定`subject`字符串进行全局匹配，从主体内`offset`位置开始，使用类型匹配`matchType`并尊重给定`matchOptions`。
返回的`QRegularExpressionMatchIterator`会排在第一场比赛结果之前（如果有的话）。

### `[since 6.5] QRegularExpressionMatchIterator QRegularExpression::globalMatchView(QStringView subjectView, qsizetype offset = 0, QRegularExpression::MatchType matchType = NormalMatch, QRegularExpression::MatchOptions matchOptions = NoMatchOption) const`

**作用与语义：**

尝试将正则表达式与给定的`subjectView`字符串视图进行全局匹配，从主体内`offset`位置开始，使用类型为`matchType`的匹配并尊重给定的`matchOptions`。
返回的`QRegularExpressionMatchIterator`会排在第一场比赛结果（如有）之前。
注意：只要有`QRegularExpressionMatchIterator`或`QRegularExpressionMatch`对象使用，`subjectView`引用的数据必须保持有效。

### `bool QRegularExpression::isValid() const`

**作用与语义：**

如果正则表达式是有效的正则表达式（即无语法错误等），否则返回`true`。使用`errorString()`获取错误的文本描述。

### `QRegularExpressionMatch QRegularExpression::match(const QString &subject, qsizetype offset = 0, QRegularExpression::MatchType matchType = NormalMatch, QRegularExpression::MatchOptions matchOptions = NoMatchOption) const`

**作用与语义：**

尝试将正则表达式与给定的`subject`字符串匹配，从主语内部`offset`位置开始，使用类型匹配`matchType`并尊重给定`matchOptions`。
返回的`QRegularExpressionMatch`对象包含匹配结果。

### `[since 6.5] QRegularExpressionMatch QRegularExpression::matchView(QStringView subjectView, qsizetype offset = 0, QRegularExpression::MatchType matchType = NormalMatch, QRegularExpression::MatchOptions matchOptions = NoMatchOption) const`

**作用与语义：**

尝试将正则表达式与给定的`subjectView`字符串视图匹配，从主体内`offset`位置开始，使用类型`matchType`匹配并尊重给定`matchOptions`。
返回的`QRegularExpressionMatch`对象包含匹配结果。
注意：只要有`QRegularExpressionMatch`对象使用，`subjectView`所引用的数据必须保持有效。

### `QStringList QRegularExpression::namedCaptureGroups() const`

**作用与语义：**

返回`captureCount()` 1元素列表，包含模式字符串中命名捕获群的名称。列表排序为：列表中位置`i`的元素（如果有名称）为第`i`捕获群的名称，若该捕获群无名则为空字符串。
例如，给定正则表达式。
namedCaptureGroups() 将返回以下列表：
这对应于捕获组#0（对应整场比赛）没有名称，捕获组#1名为“Day”，捕获组#2名为“Month”，依此类推。
如果正则表达式无效，则返回一个空列表。

**官方示例：**

```cpp
     (?<day>\d\d)-(?<month>\d\d)-(?<year>\d\d\d\d) (\w+) (?<name>\w+)
```

### `void QRegularExpression::optimize() const`

**作用与语义：**

立即编译模式，包括 JIT 编译（如果启用 JIT）以实现优化。

### `QString QRegularExpression::pattern() const`

**作用与语义：**

返回正则表达式的模式字符串。

### `qsizetype QRegularExpression::patternErrorOffset() const`

**作用与语义：**

返回模式字符串内的偏移量，该偏移量在检查正则表达式有效性时发现错误。如果未发现错误，则返回-1。

### `QRegularExpression::PatternOptions QRegularExpression::patternOptions() const`

**作用与语义：**

返回正则表达式的模式选项。

### `void QRegularExpression::setPattern(const QString &pattern)`

**作用与语义：**

将正规表达式的模式字符串设置为`pattern`。模式选项保持不变。

### `void QRegularExpression::setPatternOptions(QRegularExpression::PatternOptions options)`

**作用与语义：**

将给定`options`设为正则表达式的模式选项。模式字符串保持不变。

### `[noexcept] void QRegularExpression::swap(QRegularExpression &other)`

**作用与语义：**

将正则表达式与`other`互换。该操作非常快速且从未失败。

### `[static] QString QRegularExpression::wildcardToRegularExpression(QStringView pattern, QRegularExpression::WildcardConversionOptions options = DefaultWildcardConversion)`

**作用与语义：**

返回给定球状`pattern`的正则表达式表示。
有两种转换方式可选，一种针对文件路径混合，另一种则更通用。
默认情况下，该转换针对的是文件路径分隔符，这意味着路径分隔符会获得特殊处理。这意味着它不仅仅是从“*”到“.*”等的基本转换。
更通用的球状变换可以通过在转换`options`中传递`NonPathWildcardConversion`实现。
该实现紧密遵循球状图案的万用符定义：
- `c`：任何字符都表示自己，且不包括下面提到的字符。因此，c 与字符 c 匹配。
- `?`：匹配任意单个字符，除非选择了路径分隔符（如果文件选择了路径大块化）。它与完整正则表达式中的 b{.} 相同。
- `*`：匹配任意字符的零个或多个，除非路径分隔符（如果文件选择了路径大块化）。它与完整正规表达式中的 .* 相同。
- `[abc]`：匹配括号中给出的字符。
- `[a-c]`：匹配括号中所示范围中的一个字符。
- `[!abc]`：匹配一个未在括号中给出的字符。它与完整正规表达式中的[^abc]相同。
- `[!a-c]`：匹配一个不属于括号中范围的字符。它与完整正规表达式中的[^a-c]相同。
注意：出于历史原因，反斜杠（\）字符在此语境中不是转义字符。为了匹配某个特殊字符，请将其置于方括号内（例如`[?]`）。
关于该实施的更多信息可见：
- 维基百科球体条目
- `man 7 glob`
默认情况下，返回的正则表达式是完全锚定的。换句话说，无需对结果再次调用`anchoredPattern()`。要得到一个未锚定的正则表达式，在转换`options`中传递`UnanchoredWildcardConversion`。

**官方示例：**

```cpp
 QString wildcard = QRegularExpression::wildcardToRegularExpression("*.jpeg");
 // Will match files with names like:
 //    foo.jpeg
 //    f_o_o.jpeg
 //    föö.jpeg
```

### `[static] QString QRegularExpression::wildcardToRegularExpression(const QString &pattern, QRegularExpression::WildcardConversionOptions options = DefaultWildcardConversion)`

**作用与语义：**

返回给定球状`pattern`的正则表达式表示。
有两种转换方式可选，一种针对文件路径混合，另一种则更通用。
默认情况下，该转换针对的是文件路径分隔符，这意味着路径分隔符会获得特殊处理。这意味着它不仅仅是从“*”到“.*”等的基本转换。
更通用的球状变换可以通过在转换`options`中传递`NonPathWildcardConversion`实现。
该实现紧密遵循球状图案的万用符定义：
- `c`：任何字符都表示自己，且不包括下面提到的字符。因此，c 与字符 c 匹配。
- `?`：匹配任意单个字符，除非选择了路径分隔符（如果文件选择了路径大块化）。它与完整正则表达式中的 b{.} 相同。
- `*`：匹配任意字符的零个或多个，除非路径分隔符（如果文件选择了路径大块化）。它与完整正规表达式中的 .* 相同。
- `[abc]`：匹配括号中给出的字符。
- `[a-c]`：匹配括号中所示范围中的一个字符。
- `[!abc]`：匹配一个未在括号中给出的字符。它与完整正规表达式中的[^abc]相同。
- `[!a-c]`：匹配一个不属于括号中范围的字符。它与完整正规表达式中的[^a-c]相同。
注意：出于历史原因，反斜杠（\）字符在此语境中不是转义字符。为了匹配某个特殊字符，请将其置于方括号内（例如`[?]`）。
关于该实施的更多信息可见：
- 维基百科球体条目
- `man 7 glob`
默认情况下，返回的正则表达式是完全锚定的。换句话说，无需对结果再次调用`anchoredPattern()`。要得到一个未锚定的正则表达式，在转换`options`中传递`UnanchoredWildcardConversion`。

**官方示例：**

```cpp
 QString wildcard = QRegularExpression::wildcardToRegularExpression("*.jpeg");
 // Will match files with names like:
 //    foo.jpeg
 //    f_o_o.jpeg
 //    föö.jpeg
```

### `[noexcept] QRegularExpression &QRegularExpression::operator=(QRegularExpression &&re)`

**作用与语义：**

Move-assign 正则表达式 `re` 给该对象，并返回结果的引用。模式和模式选项都会被复制。
注意，移出`QRegularExpression`只能被销毁或分配到。调用除解构器或赋值运算符外的其他函数效果尚无定义。

### `[noexcept] QRegularExpression &QRegularExpression::operator=(const QRegularExpression &re)`

**作用与语义：**

将正则表达式`re`赋入该对象，并返回对副本的引用。模式和模式选项都被复制。

### `[noexcept] size_t qHash(const QRegularExpression &key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `[noexcept] bool operator!=(const QRegularExpression &lhs, const QRegularExpression &rhs)`

**作用与语义：**

如果`lhs`正则表达式与`rhs`不同，返回`true`;否则返回为假。

### `QDataStream &operator<<(QDataStream &out, const QRegularExpression &re)`

**作用与语义：**

写入正则表达式`re`流`out`。

### `QDebug operator<<(QDebug debug, QRegularExpression::PatternOptions patternOptions)`

**作用与语义：**

将模式选项`patternOptions`写入调试对象`debug`以便调试。

### `QDebug operator<<(QDebug debug, const QRegularExpression &re)`

**作用与语义：**

将正规表达式`re`写入调试对象`debug`以便调试。

### `[noexcept] bool operator==(const QRegularExpression &lhs, const QRegularExpression &rhs)`

**作用与语义：**

如果`lhs`正则表达式等于`rhs`，则返回`true`;否则返回假。如果两个`QRegularExpression`对象具有相同的模式字符串和相同的模式选项，则它们相等。

### `QDataStream &operator>>(QDataStream &in, QRegularExpression &re)`

**作用与语义：**

将流`in`的正则表达式读取到`re`。

### `enum MatchOption { NoMatchOption, AnchoredMatchOption, AnchorAtOffsetMatchOption, DontCheckSubjectStringMatchOption }`

**作用与语义：**

- `QRegularExpression::NoMatchOption`：`0x0000`;不设置匹配选项。
- `QRegularExpression::AnchoredMatchOption`：`AnchorAtOffsetMatchOption`;改用 AnchorAtOffsetMatchOption。
- `QRegularExpression::AnchorAtOffsetMatchOption`：`0x0001`;匹配被限制必须从传递给`match()`的偏移开始，才能成功，即使模式字符串中没有任何元字符锚定匹配。注意，通过该选项不会将匹配结束点锚定到主语的结尾;如果你想完全锚定正则表达式，可以使用`anchoredPattern()`。该枚举值在Qt 6.0中引入。
- `QRegularExpression::DontCheckSubjectStringMatchOption`：`0x0002`;在尝试匹配前，主旨字符串不会检查其 UTF-16 有效性。使用此选项时需极度谨慎，因为尝试匹配无效字符串可能导致程序崩溃和/或构成安全问题。该枚举值在 Qt 5.4 中引入。
MatchOptions 类型是 QFlags 的 typedef<MatchOption>。它存储 MatchOption 值的 OR 组合。

### `flags MatchOptions`

**作用与语义：**

- `QRegularExpression::NoMatchOption`：`0x0000`;不设置匹配选项。
- `QRegularExpression::AnchoredMatchOption`：`AnchorAtOffsetMatchOption`;改用 AnchorAtOffsetMatchOption。
- `QRegularExpression::AnchorAtOffsetMatchOption`：`0x0001`;匹配被限制必须从传递给`match()`的偏移开始，才能成功，即使模式字符串中没有任何元字符锚定匹配。注意，通过该选项不会将匹配结束点锚定到主语的结尾;如果你想完全锚定正则表达式，可以使用`anchoredPattern()`。该枚举值在Qt 6.0中引入。
- `QRegularExpression::DontCheckSubjectStringMatchOption`：`0x0002`;在尝试匹配前，主旨字符串不会检查其 UTF-16 有效性。使用此选项时需极度谨慎，因为尝试匹配无效字符串可能导致程序崩溃和/或构成安全问题。该枚举值在 Qt 5.4 中引入。
MatchOptions 类型是 QFlags 的 typedef<MatchOption>。它存储 MatchOption 值的 OR 组合。

### `enum PatternOption { NoPatternOption, CaseInsensitiveOption, DotMatchesEverythingOption, MultilineOption, ExtendedPatternSyntaxOption, …, UseUnicodePropertiesOption }`

**作用与语义：**

PatternOption 枚举定义了模式字符串应如何解释的修饰符，从而定义模式与主题字符串匹配的方式。
- `QRegularExpression::NoPatternOption`：`0x0000`;不设置任何图案选项。
- `QRegularExpression::CaseInsensitiveOption`：`0x0001`;该模式应以不区分大小写的方式与主语字符串匹配。该选项对应于 Perl 正则表达式中的 /i 修饰符。
- `QRegularExpression::DotMatchesEverythingOption`：`0x0002`;模式字符串中的点元字符（`.`）允许匹配主语字符串中的任意字符，包括换行（通常点不匹配换行）。该选项对应于 Perl 正则表达式中的 `/s` 修饰符。
- `QRegularExpression::MultilineOption`：`0x0004`;模式字符串中的插入符（`^`）和美元元字符（`$`）分别允许在主题字符串中任何换行之后和之前，以及主题字符串的开头和末尾匹配。该选项对应于 Perl 正则表达式中的 `/m` 修饰符。
- `QRegularExpression::ExtendedPatternSyntaxOption`：`0x0008`;模式字符串中未转义且不属于字符类的空白部分将被忽略。此外，字符类外的未脱义升号（#）会导致后续所有字符（包括第一行）被忽略。这可用于提高模式字符串的可读性，并将注释放入正则表达式中;这在从文件加载或用户编写的模式字符串中尤为有用，因为在C代码中，字符串文字规则总能将注释置于模式字符串之外。该选项对应Perl正则表达式中的`/x`修饰符。
- `QRegularExpression::InvertedGreedinessOption`：`0x0010`;量词的贪婪程度是反转的：`*`、`+`、`?`、`{m,n}`等变得懒惰，而它们的懒惰版本（`*?`、`+?`、`??`、`{m,n}?`等）变得贪婪。在Perl正则表达式中没有类似的选项。
- `QRegularExpression::DontCaptureOption`：`0x0020`;非命名捕获群不捕获子串;命名捕获群仍然按预期工作，且对应整个匹配的隐式捕获组编号0也同样有效。Perl正则表达式中没有对此选项的对应。
- `QRegularExpression::UseUnicodePropertiesOption`：`0x0040`;`\w`、`\d`等字符类的含义，以及它们对应的字符（`\W`、`\D`等）的含义，从仅匹配ASCII字符改为匹配具有相应Unicode属性的任意字符。例如，`\d`被更改为匹配任何具有Unicode的Nd（十进制数字）属性的字符;`\w`匹配任何具有Unicode字母L（字母）或N（数字）属性的字符，加上下划线，依此类推。该选项对应于 Perl 正则表达式中的 `/u` 修饰符。
PatternOptions 类型是 QFlags 的 typedef<PatternOption>。它存储 PatternOption 值的 OR 组合。

### `flags PatternOptions`

**作用与语义：**

PatternOption 枚举定义了模式字符串应如何解释的修饰符，从而定义模式与主题字符串匹配的方式。
- `QRegularExpression::NoPatternOption`：`0x0000`;不设置任何图案选项。
- `QRegularExpression::CaseInsensitiveOption`：`0x0001`;该模式应以不区分大小写的方式与主语字符串匹配。该选项对应于 Perl 正则表达式中的 /i 修饰符。
- `QRegularExpression::DotMatchesEverythingOption`：`0x0002`;模式字符串中的点元字符（`.`）允许匹配主语字符串中的任意字符，包括换行（通常点不匹配换行）。该选项对应于 Perl 正则表达式中的 `/s` 修饰符。
- `QRegularExpression::MultilineOption`：`0x0004`;模式字符串中的插入符（`^`）和美元元字符（`$`）分别允许在主题字符串中任何换行之后和之前，以及主题字符串的开头和末尾匹配。该选项对应于 Perl 正则表达式中的 `/m` 修饰符。
- `QRegularExpression::ExtendedPatternSyntaxOption`：`0x0008`;模式字符串中未转义且不属于字符类的空白部分将被忽略。此外，字符类外的未脱义升号（#）会导致后续所有字符（包括第一行）被忽略。这可用于提高模式字符串的可读性，并将注释放入正则表达式中;这在从文件加载或用户编写的模式字符串中尤为有用，因为在C代码中，字符串文字规则总能将注释置于模式字符串之外。该选项对应Perl正则表达式中的`/x`修饰符。
- `QRegularExpression::InvertedGreedinessOption`：`0x0010`;量词的贪婪程度是反转的：`*`、`+`、`?`、`{m,n}`等变得懒惰，而它们的懒惰版本（`*?`、`+?`、`??`、`{m,n}?`等）变得贪婪。在Perl正则表达式中没有类似的选项。
- `QRegularExpression::DontCaptureOption`：`0x0020`;非命名捕获群不捕获子串;命名捕获群仍然按预期工作，且对应整个匹配的隐式捕获组编号0也同样有效。Perl正则表达式中没有对此选项的对应。
- `QRegularExpression::UseUnicodePropertiesOption`：`0x0040`;`\w`、`\d`等字符类的含义，以及它们对应的字符（`\W`、`\D`等）的含义，从仅匹配ASCII字符改为匹配具有相应Unicode属性的任意字符。例如，`\d`被更改为匹配任何具有Unicode的Nd（十进制数字）属性的字符;`\w`匹配任何具有Unicode字母L（字母）或N（数字）属性的字符，加上下划线，依此类推。该选项对应于 Perl 正则表达式中的 `/u` 修饰符。
PatternOptions 类型是 QFlags 的 typedef<PatternOption>。它存储 PatternOption 值的 OR 组合。

### `(since 6.0) enum WildcardConversionOption { DefaultWildcardConversion, UnanchoredWildcardConversion, NonPathWildcardConversion }`

**作用与语义：**

WildcardConversionOption 枚举定义了将万用字块模式转换为正则表达式模式的方式修饰符。
- `QRegularExpression::DefaultWildcardConversion`：`0x0`;不设置转换选项。
- `QRegularExpression::UnanchoredWildcardConversion`：`0x1`;转换不会锚定模式。这允许部分字符串匹配百搭符表达式。
- `QRegularExpression::NonPathWildcardConversion (since Qt 6.6)`：`0x2`;转换时不会将模式解释为文件路径的滚动。
该枚举是在Qt 6.0中引入的。
WildcardConversionOptions 类型是 QFlags 的 typedef<WildcardConversionOption>。它存储 WildcardConversionOption 值的 OR 组合。

### `flags WildcardConversionOptions`

**作用与语义：**

WildcardConversionOption 枚举定义了将万用字块模式转换为正则表达式模式的方式修饰符。
- `QRegularExpression::DefaultWildcardConversion`：`0x0`;不设置转换选项。
- `QRegularExpression::UnanchoredWildcardConversion`：`0x1`;转换不会锚定模式。这允许部分字符串匹配百搭符表达式。
- `QRegularExpression::NonPathWildcardConversion (since Qt 6.6)`：`0x2`;转换时不会将模式解释为文件路径的滚动。
该枚举是在Qt 6.0中引入的。
WildcardConversionOptions 类型是 QFlags 的 typedef<WildcardConversionOption>。它存储 WildcardConversionOption 值的 OR 组合。

## 6. 深入实践与常见坑

### 生命周期和资源边界

值对象由作用域、容器或调用者管理，不使用 parent 和 deleteLater。跨线程传递副本通常比传递 QObject 安全，但共享数据在写入时仍可能发生复制，性能和内存峰值要结合数据规模判断。

### 状态和错误边界

重点区分空值、无效值、默认值和已初始化值。例如空字符串、空 URL、null 图像和无效索引不一定表示同一件事；转换函数的失败结果要通过对应的状态查询确认。

### 线程边界

值类型本身通常可以复制后跨线程传递；不要把 data()/bits()/constData() 得到的指针当成跨线程长期有效的所有权。大对象频繁写入会触发 detach，应避免不必要的复制和格式转换。

### 最容易出现的错误

不要把空值当成业务成功；不要保存临时对象的内部指针；不要把 QString 当二进制缓冲区；不要假定隐式共享让并发写入自动安全。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QRegularExpression` 所属机制类型：Qt 值类型与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
