# QUrl

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** URL 值类型，负责地址解析、组件访问、编码、组合和规范化。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QUrl`：URL 值类型，负责地址解析、组件访问、编码、组合和规范化。

**内部模型：** 这类类型通常可以按值传递、复制和返回。许多 Qt 容器、字符串和图像采用隐式共享：复制时共享数据，发生写操作时才 detach。这样便于 API 传值，但获取原始指针或长期持有引用时必须考虑对象修改和生命周期。

**适用场景：** 先确认值的有效性和表示格式，再调用查询、转换或修改 API；处理文本时区分 Unicode 和字节编码，处理图像时确认 format，处理 URL/路径时使用 Qt 的解析 API 而不是手写字符串规则。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要把空值当成业务成功；不要保存临时对象的内部指针；不要把 QString 当二进制缓冲区；不要假定隐式共享让并发写入自动安全。

## 2. 依赖与对象关系

- 头文件：`#include <QUrl>`
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

- `(since 6.3) enum AceProcessingOption { IgnoreIDNWhitelist, AceTransitionalProcessing }`
- `flags AceProcessingOptions`
- `enum ComponentFormattingOption { PrettyDecoded, EncodeSpaces, EncodeUnicode, EncodeDelimiters, EncodeReserved, …, FullyDecoded }`
- `flags ComponentFormattingOptions`
- `flags FormattingOptions`
- `enum ParsingMode { TolerantMode, StrictMode, DecodedMode }`
- `enum UrlFormattingOption { None, RemoveScheme, RemovePassword, RemoveUserInfo, RemovePort, …, NormalizePathSegments }`
- `enum UserInputResolutionOption { DefaultResolution, AssumeLocalFile }`
- `flags UserInputResolutionOptions`

### 公有函数

- `QUrl()`
- `QUrl(const QString &url, QUrl::ParsingMode parsingMode = TolerantMode)`
- `QUrl(const QUrl &other)`
- `QUrl(QUrl &&other)`
- `~QUrl()`
- `QUrl adjusted(QUrl::FormattingOptions options) const`
- `QString authority(QUrl::ComponentFormattingOptions options = PrettyDecoded) const`
- `void clear()`
- `QString errorString() const`
- `QString fileName(QUrl::ComponentFormattingOptions options = FullyDecoded) const`
- `QString fragment(QUrl::ComponentFormattingOptions options = PrettyDecoded) const`
- `bool hasFragment() const`
- `bool hasQuery() const`
- `QString host(QUrl::ComponentFormattingOptions options = FullyDecoded) const`
- `bool isEmpty() const`
- `bool isLocalFile() const`
- `bool isParentOf(const QUrl &childUrl) const`
- `bool isRelative() const`
- `bool isValid() const`
- `bool matches(const QUrl &url, QUrl::FormattingOptions options) const`
- `QString password(QUrl::ComponentFormattingOptions options = FullyDecoded) const`
- `QString path(QUrl::ComponentFormattingOptions options = FullyDecoded) const`
- `int port(int defaultPort = -1) const`
- `QString query(QUrl::ComponentFormattingOptions options = PrettyDecoded) const`
- `QUrl resolved(const QUrl &relative) const`
- `QString scheme() const`
- `void setAuthority(const QString &authority, QUrl::ParsingMode mode = TolerantMode)`
- `void setFragment(const QString &fragment, QUrl::ParsingMode mode = TolerantMode)`
- `void setHost(const QString &host, QUrl::ParsingMode mode = DecodedMode)`
- `void setPassword(const QString &password, QUrl::ParsingMode mode = DecodedMode)`
- `void setPath(const QString &path, QUrl::ParsingMode mode = DecodedMode)`
- `void setPort(int port)`
- `void setQuery(const QString &query, QUrl::ParsingMode mode = TolerantMode)`
- `void setQuery(const QUrlQuery &query)`
- `void setScheme(const QString &scheme)`
- `void setUrl(const QString &url, QUrl::ParsingMode parsingMode = TolerantMode)`
- `void setUserInfo(const QString &userInfo, QUrl::ParsingMode mode = TolerantMode)`
- `void setUserName(const QString &userName, QUrl::ParsingMode mode = DecodedMode)`
- `void swap(QUrl &other)`
- `CFURLRef toCFURL() const`
- `QString toDisplayString(QUrl::FormattingOptions options = FormattingOptions(PrettyDecoded)) const`
- `QByteArray toEncoded(QUrl::FormattingOptions options = FullyEncoded) const`
- `QString toLocalFile() const`
- `NSURL * toNSURL() const`
- `QString toString(QUrl::FormattingOptions options = FormattingOptions(PrettyDecoded)) const`
- `QString url(QUrl::FormattingOptions options = FormattingOptions(PrettyDecoded)) const`
- `QString userInfo(QUrl::ComponentFormattingOptions options = PrettyDecoded) const`
- `QString userName(QUrl::ComponentFormattingOptions options = FullyDecoded) const`
- `QUrl & operator=(QUrl &&other)`
- `QUrl & operator=(const QString &url)`
- `QUrl & operator=(const QUrl &url)`

### 静态公有成员

- `(since 6.3) QString fromAce(const QByteArray &domain, QUrl::AceProcessingOptions options = {})`
- `QUrl fromCFURL(CFURLRef url)`
- `QUrl fromEncoded(QByteArrayView input, QUrl::ParsingMode mode = TolerantMode)`
- `QUrl fromLocalFile(const QString &localFile)`
- `QUrl fromNSURL(const NSURL *url)`
- `QString fromPercentEncoding(const QByteArray &input)`
- `QList<QUrl> fromStringList(const QStringList &urls, QUrl::ParsingMode mode = TolerantMode)`
- `QUrl fromUserInput(const QString &userInput, const QString &workingDirectory = QString(), QUrl::UserInputResolutionOptions options = DefaultResolution)`
- `QStringList idnWhitelist()`
- `void setIdnWhitelist(const QStringList &list)`
- `(since 6.3) QByteArray toAce(const QString &domain, QUrl::AceProcessingOptions options = {})`
- `QByteArray toPercentEncoding(const QString &input, const QByteArray &exclude = QByteArray(), const QByteArray &include = QByteArray())`
- `QStringList toStringList(const QList<QUrl> &urls, QUrl::FormattingOptions options = FormattingOptions(PrettyDecoded))`

### 相关非成员函数

- `bool operator!=(const QUrl &lhs, const QUrl &rhs)`
- `QDataStream & operator<<(QDataStream &out, const QUrl &url)`
- `bool operator==(const QUrl &lhs, const QUrl &rhs)`
- `QDataStream & operator>>(QDataStream &in, QUrl &url)`

### 公开宏

- `QT_NO_URL_CAST_FROM_STRING`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[since 6.3] enum QUrl::AceProcessingOptionflags QUrl::AceProcessingOptions`

**作用与语义：**

ACE 处理选项控制 URL 如何转换为 ASCII 兼容编码以及如何从中转换回。
- `QUrl::IgnoreIDNWhitelist`：`0x1`；在将 URL 转换为 Unicode 时忽略 IDN 白名单。
- `QUrl::AceTransitionalProcessing`：`0x2`；使用 UTS #46 中描述的过渡处理。这允许更好地兼容 IDNA 2003 规范。
默认使用非过渡处理，并且仅允许 IDN 白名单列出的顶级域名内的 URL 包含非 ASCII 字符。
该枚举在 Qt 6.3 中引入。
AceProcessingOptions 类型是 QFlags<AceProcessingOption> 的 typedef。它存储 AceProcessingOption 值的按位或组合。

### `enum QUrl::ComponentFormattingOptionflags QUrl::ComponentFormattingOptions`

**作用与语义：**

组件格式选项定义了 URL 组成部分在以文本形式写出时的格式化方式。当它们在`toString()`和`toEncoded()`中使用时，可以与 `QUrl::FormattingOptions` 中的选项结合使用。
- `QUrl::PrettyDecoded`：`0x000000`;该组件以“漂亮的形式”返回，大部分百分比编码字符已解码。PrettyDecoded 的具体行为因组件而异，且可能在不同 Qt 版本中有所不同。这是默认状态。
- `QUrl::EncodeSpaces`：`0x100000`;保持空格字符的编码形式（“”）。
- `QUrl::EncodeUnicode`：`0x200000`;非美国ASCII字符保持其UTF-8百分点编码形式（例如，U 00E9代码点用“é”，拉丁字母小写字母E带尖音）。
- `QUrl::EncodeDelimiters`：`0x400000 | 0x800000`;保持某些分隔符的编码形式，如完整URL以文本表示时URL中出现的。分隔符会受到该选项变化的影响。该标志在`toString()`或`toEncoded()`中无效。
- `QUrl::EncodeReserved`：`0x1000000`;在编码形式中，保留规范中不允许的 US-ASCII 字符。这是 `toString()` 和 `toEncoded()` 的默认设置。
- `QUrl::DecodeReserved`：`0x2000000`;解码URL规范不允许出现在URL中的US-ASCII字符。这是单个组件获取者的默认设置。
- `QUrl::FullyEncoded`：`EncodeSpaces | EncodeUnicode | EncodeDelimiters | EncodeReserved`;保持所有字符正确编码的形式，因为该组件会作为URL的一部分出现。当与`toString()`一起使用时，这会产生一个完全符合规范的URL，完全符合`QString`的形式，结果与`toEncoded()`
- `QUrl::FullyDecoded`：`FullyEncoded | DecodeReserved | 0x4000000`;尽量解码尽可能多的部分。对于URL的各个组成部分，解码所有百分比编码序列，包括控制字符（U 0000到U 001F）和以百分比编码形式出现的UTF-8序列。使用此模式可能导致数据丢失，详见下文。
EncodeReserved 和 DecodeReserved 的值不应在同一次调用中同时使用。如果发生这种情况，行为是未定义的。它们作为独立值提供是因为“漂亮模式”在保留字符的行为在某些组件上不同，尤其是在完整 URL 上。
完全解码模式类似于Qt 4.x中返回`QString`的函数行为，每个字符都代表自己，且没有特殊含义。这对百分比字符（“%”）同样适用，应将其解释为字面意义的百分比，而非百分比编码序列的开头。在所有其他解码模式下，同一字符由序列“%”表示。
每当将用 QUrl：：FullyDecoded 获得的数据重新应用到`QUrl`时，必须注意使用`QUrl::DecodedMode`参数作为 setter（如 `setPath()` 和 `setUserName()`）。未这样做可能导致百分比字符（“%”）被重新解释为百分比编码序列的开头。
当URL的部分内容出现在非URL上下文时，该模式非常有用。例如，在FTP客户端应用中提取用户名、密码或文件路径时，应使用FullyDecoded模式。
此模式应谨慎使用，因为有两种情况在返回的 `QString` 中无法可靠表示。它们是：
- 非 UTF-8 序列：URL 可能包含不形成有效 UTF-8 序列的百分号编码字符序列。由于 URL 需要使用 UTF-8 解码，任何解码器失败都会导致 `QString` 在该序列存在的位置包含一个或多个替换字符。
- 编码分隔符：URL 也允许区分其字面形式的分隔符和百分号编码形式的等效分隔符。这在查询中最常见，但在 URL 的大多数部分都是允许的。
以下示例说明了该问题：
如果通过 HTTP GET 使用这两个 URL，Web 服务器的解释可能不同。第一种情况，它将解释为一个参数，键为 "q"，值为 "a =b&c"。第二种情况，它可能解释为两个参数，一个键为 "q"，值为 "a =b"，另一个键为 "c"，无值。
ComponentFormattingOptions 类型是 QFlags<ComponentFormattingOption> 的 typedef。它存储 ComponentFormattingOption 值的 OR 组合。

**官方示例：**

```cpp
 QUrl original("http://example.com/?q=a%2B%3Db%26c");
 QUrl copy(original);
 copy.setQuery(copy.query(QUrl::FullyDecoded), QUrl::DecodedMode);

 qDebug() << original.toString();   // prints: http://example.com/?q=a%2B%3Db%26c
 qDebug() << copy.toString();       // prints: http://example.com/?q=a+=b&c
```

### `enum QUrl::ParsingMode`

**作用与语义：**

解析模式控制`QUrl`解析字符串的方式。
- `QUrl::TolerantMode`：`0`;`QUrl`将尝试纠正URL中的一些常见错误。该模式有助于解析来自不严格符合标准的来源的URL。
- `QUrl::StrictMode`：`1`;仅接受有效的URL。此模式对一般URL验证非常有用。
- `QUrl::DecodedMode`：`2`;`QUrl` 会以完全解码的形式解释 URL 组件，其中百分比字符独立表示，而不是作为百分比编码序列的开头。该模式仅适用于设置 URL 组件的设置者;在`QUrl`构造器、`fromEncoded()` 或 `setUrl()` 中均不允许。有关该模式的更多信息，请参阅 `QUrl::FullyDecoded` 的文档。
在容忍模式中，解析器具有以下行为：
- 空格和 “ ”：未编码空格字符将被接受，并视为等价于 “ ”。
- 单个“%”字符：如果任何百分比字符“%”后面没有两个十六进制字符（例如“13% coverage.html”），解析器会假设输入未编码，并将所有“%”字符替换为“%”。
- 保留字符和非保留字符：编码URL应仅包含少数字符作为字面量;其他字符应为百分比编码。在宽容模式下，只要这些字符出现在URL中，则被接受：空格 / 双引号 / “<” / “>” / “” / “^” / “`" / "{" / "|" / "}" Those same characters can be decoded again by passing `QUrl：:D ecodeReserved` to `toString()` or `toEncoded()”。在单个组件的获取器中，这些字符通常以解码形式返回。
在严格模式下，如果发现解析错误，`isValid()` 返回 `false`，`errorString()` 返回描述错误的消息。如果检测到多个错误，报告哪个错误则未定义。
注意，容忍模式通常不足以解析用户输入，因为输入中往往包含比解析器能处理的错误和预期更多的内容。处理直接来自用户的数据——而非来自数据传输源（如其他程序）时，建议使用`fromUserInput()`。

### `enum QUrl::UrlFormattingOptionflags QUrl::FormattingOptions`

**作用与语义：**

格式选项定义了URL在以文本形式写出来时的格式化。
- `QUrl::None`：`0x0`;URL格式未变。
- `QUrl::RemoveScheme`：`0x1`;该方案从URL中移除。
- `QUrl::RemovePassword`：`0x2`;URL中的任何密码都会被移除。
- `QUrl::RemoveUserInfo`：`RemovePassword | 0x4`;URL中的任何用户信息都会被删除。
- `QUrl::RemovePort`：`0x8`;任何指定的端口都会从URL中移除。
- `QUrl::RemoveAuthority`：`RemoveUserInfo | RemovePort | 0x10`;移除用户名、密码、主机和端口。
- `QUrl::RemovePath`：`0x20`;URL路径被移除，只剩下方案、主机地址和端口（如存在）。
- `QUrl::RemoveQuery`：`0x40`;URL中带有“？”字符的查询部分被移除。
- `QUrl::RemoveFragment`：`0x80`;URL中的片段部分（包括“#”字符）被移除。
- `QUrl::RemoveFilename`：`0x800`;文件名（即路径中最后一个“/”之后的所有部分）被移除。尾部的“/”保留，除非设置了StripTrailingSlash。只有当RemovePath未被设置时才有效。
- `QUrl::PreferLocalFile`：`0x200`;如果 URL 是本地文件，且`isLocalFile()`中没有查询或片段，则返回本地文件路径。
- `QUrl::StripTrailingSlash`：`0x400`;如果有后斜杠，则从路径中移除。
- `QUrl::NormalizePathSegments`：`0x1000`;修改路径以去除冗余的目录分隔符，并解析“.”s 和 “..”尽可能多。对于非本地路径，相邻的斜杠会被保留。
请注意，Nameprep 中的大小写折叠规则（`QUrl`符合），要求主机名始终转换为小写，无论使用 Qt：：FormattingOptions 格式如何。
`QUrl::ComponentFormattingOptions`的选项也是可能的。
FormattingOptions 类型是 QFlags 的 typedef<UrlFormattingOption>。它存储 UrlFormattingOption 值的 OR 组合。

### `enum QUrl::UserInputResolutionOptionflags QUrl::UserInputResolutionOptions`

**作用与语义：**

用户输入解析选项定义了`fromUserInput()`应如何解释字符串，这些字符串可以是相对路径，也可以是HTTP URL的简短形式。例如，`file.pl`可以是本地文件或URL的 `http://file.pl`。
- `QUrl::DefaultResolution`：`0`;默认解析机制是检查`fromUserInput`工作目录中是否存在本地文件，并仅返回本地路径。否则假设为 URL。
- `QUrl::AssumeLocalFile`：`1`;该选项使`fromUserInput()`除非输入包含方案（如 `http://file.pl`），否则始终返回本地路径。这对文本编辑器等应用程序非常有用，因为它们能够在不存在文件时创建该路径。
UserInputResolutionOptions 类型是 QFlags 的 typedef<UserInputResolutionOption>。它存储 UserInputResolutionOption 值的 OR 组合。

### `QUrl::QUrl()`

**作用与语义：**

构造一个空的QUrl对象。

### `QUrl::QUrl(const QString &url, QUrl::ParsingMode parsingMode = TolerantMode)`

**作用与语义：**

通过解析`url`构造URL。注意，该构造器期望获得正确的URL或URL-Reference，不会尝试猜测意图。例如，以下声明：
将构造一个有效的URL，但可能不是预期的，因为缺少输入的`scheme()`部分。对于上述字符串，应用程序可能需要使用`fromUserInput()`。对于该构造器或`setUrl()`，可能就是预期的：
QUrl 会自动对所有不允许出现在 URL 中的字符进行百分比编码，并解码表示未保留字符（字母、数字、连字符、下划线、点和波浪号）的百分比编码序列。其他字符保持原始形式。
使用解析器模式`parsingMode`解析`url`。在`TolerantMode`（默认）中，QUrl 会纠正某些错误，尤其是存在一个百分比字符（'%'）后面没有两个十六进制数字，并且接受任意位置的字符。在 `StrictMode` 中，编码错误不被容忍，QUrl 还会检查某些禁止字符未编码的形式存在。如果在 `StrictMode` 中检测到错误，`isValid()` 将返回 false。在此语境下不允许使用解析模式`DecodedMode`。
要从编码字符串构造URL，你也可以使用`fromEncoded()`：
这两个函数是等价的，在Qt 5中，这两个函数都接受编码数据。通常，选择QUrl构造函数或`setUrl()`与`fromEncoded()`取决于源数据：构造函数和`setUrl()`取`QString`，而`fromEncoded`取`QByteArray`。

**官方示例：**

```cpp
 QUrl url("example.com");
```

### `[noexcept] QUrl::QUrl(const QUrl &other)`

**作用与语义：**

复制了`other`。

### `[noexcept] QUrl::QUrl(QUrl &&other)`

**作用与语义：**

Move构造一个QUrl实例，使其指向`other`指向的同一个对象。

### `[noexcept] QUrl::~QUrl()`

**作用与语义：**

Destructor;在对象被删除前立即调用。

### `QUrl QUrl::adjusted(QUrl::FormattingOptions options) const`

**作用与语义：**

返回调整后的URL。输出可通过传递带有`options`的标志进行自定义。
`QUrl::ComponentFormattingOption`的编码选项对这种方法来说不太合理，`QUrl::PreferLocalFile`也一样。
这总是等价于`QUrl`（URL.`toString`（选项））。

### `QString QUrl::authority(QUrl::ComponentFormattingOptions options = PrettyDecoded) const`

**作用与语义：**

如果URL被定义，则返回其权威;否则返回空字符串。
该函数返回一个明确的值，可能包含仍为百分方程编码的字符，以及一些无法在`QString`中以解码形式表示的控制序列。
`options`参数控制用户信息组件的格式化。该函数不允许使用`QUrl::FullyDecoded`值。如果需要获得完全解码的数据，分别调用`userName()`、`password()`、`host()`和`port()`。

### `void QUrl::clear()`

**作用与语义：**

重置`QUrl`的内容。调用该函数后，`QUrl`等于用默认空构造函数构造出来的。

### `QString QUrl::errorString() const`

**作用与语义：**

如果最后一次修改该`QUrl`对象的操作遇到解析错误，返回错误消息。如果未检测到错误，该函数返回空字符串，`isValid()`返回`true`。
该函数返回的错误信息具有技术属性，终端用户可能无法理解。它主要对试图理解`QUrl`不接受某些输入的开发者有帮助。

### `QString QUrl::fileName(QUrl::ComponentFormattingOptions options = FullyDecoded) const`

**作用与语义：**

返回文件名称，但不含目录路径。
注意，如果该`QUrl`对象的路径以斜杠结尾，文件名称视为空。
如果路径不包含斜杠，则完整返回为文件名。
`options`参数控制文件名组件的格式化。所有值都会产生明确无歧义的结果。使用`QUrl::FullyDecoded`，所有百分比编码序列都会被解码;否则，返回的值可能包含某些控制序列的百分比编码序列，这些序列在`QString`中无法以解码形式表示。

**官方示例：**

```cpp
 QUrl url("http://qt-project.org/support/file.html");
 // url.adjusted(RemoveFilename) == "http://qt-project.org/support/"
 // url.fileName() == "file.html"
```

### `QString QUrl::fragment(QUrl::ComponentFormattingOptions options = PrettyDecoded) const`

**作用与语义：**

返回URL的片段。要判断解析后的URL是否包含片段，请使用`hasFragment()`。
`options`参数控制片段组件的格式化。所有值均产生明确无歧义的结果。使用`QUrl::FullyDecoded`，所有百分比编码序列都被解码;否则，返回的值可能包含某些控制序列的百分比编码序列，这些序列在`QString`中无法以解码形式表示。
请注意，如果存在这些不可表示序列，可能会导致数据丢失`QUrl::FullyDecoded`。建议在非URL上下文中使用该值。

### `[static, since 6.3] QString QUrl::fromAce(const QByteArray &domain, QUrl::AceProcessingOptions options = {})`

**作用与语义：**

返回给定域名`domain`的Unicode形式，该格式编码为ASCII兼容编码（ACE）。输出可以通过传递带有`options`的标志来自定义。该函数的结果被视为等价于`domain`。
如果`domain`中的值无法编码，则会转换为`QString`并返回。
ASCII 兼容编码（ACE）由 RFC 3490、RFC 3491 和 RFC 3492 定义，并由 Unicode 技术标准 #46 更新。它是《应用中的国际化域名》（IDNA）规范的一部分，允许使用非美国 ASCII 字符（如 `"example.com"`）来编写域名。

### `[static] QUrl QUrl::fromCFURL(CFURLRef url)`

**作用与语义：**

构建包含CFURL副本的`QUrl` `url`。

### `[static] QUrl QUrl::fromEncoded(QByteArrayView input, QUrl::ParsingMode mode = TolerantMode)`

**作用与语义：**

解析`input`并返回相应的`QUrl`。`input`假设为编码形式，仅包含ASCII字符。
使用`mode`解析URL。有关该参数的更多信息请参见 `setUrl()`。在此语境下不允许`QUrl::DecodedMode`。
注意：在 6.7 之前的 Qt 版本中，这个函数用的是 `QByteArray`，而不是 `QByteArrayView`。如果你遇到编译错误，那是因为你的代码传递的对象是隐式可转换为 `QByteArray`，但不能`QByteArrayView`。将相应的参数包裹在 `QByteArray{~~~}` 中，使铸造显式化。这与旧版 Qt 版本兼容。

### `[static] QUrl QUrl::fromLocalFile(const QString &localFile)`

**作用与语义：**

返回`localFile`的`QUrl`表示，解释为本地文件。该函数接受用斜杠分隔的路径以及该平台的原生分隔符。
该功能还接受带有双斜杠（或反斜线）的路径，以表示远程文件，如“//servername/path/to/file.txt”。请注意，只有某些平台能用`QFile::open()`打开该文件。
空`localFile`会导致空的网址（自Qt 5.4起）。
在上面摘要的第一行中，文件URL是从本地的相对路径构建的。只有当有一个基础URL可以解析时，文件URL才有相对路径。例如：
要解决这样的URL，需要事先移除该方案：
因此，对于相对文件路径，最好使用相对 URL（即无方案）：

**官方示例：**

```cpp
 qDebug() << QUrl::fromLocalFile("file.txt");            // QUrl("file:file.txt")
 qDebug() << QUrl::fromLocalFile("/home/user/file.txt"); // QUrl("file:///home/user/file.txt")
 qDebug() << QUrl::fromLocalFile("file:file.txt");       // doesn't make sense; expects path, not url with scheme
```

### `[static] QUrl QUrl::fromNSURL(const NSURL *url)`

**作用与语义：**

构建包含NSURL副本的`QUrl` `url`。

### `[static] QString QUrl::fromPercentEncoding(const QByteArray &input)`

**作用与语义：**

返回解码后的`input`副本。`input`先从百分比编码解码，然后从UTF-8转换为Unicode。
注意：给定无效输入（例如包含序列“%G5”的字符串，这不是有效的十六进制数），输出也会无效。举例来说：“%G5”序列可以解码为“W”。

### `[static] QList<QUrl> QUrl::fromStringList(const QStringList &urls, QUrl::ParsingMode mode = TolerantMode)`

**作用与语义：**

将表示`urls`的字符串列表转换为URL列表，使用`QUrl`（str， `mode`）。注意，这意味着所有字符串必须是URL的，而非例如局部路径。

### `[static] QUrl QUrl::fromUserInput(const QString &userInput, const QString &workingDirectory = QString(), QUrl::UserInputResolutionOptions options = DefaultResolution)`

**作用与语义：**

如果能推导出字符串，则返回用户提供的有效 URL `userInput`字符串。如果无法推断，则返回无效的 `QUrl()`。
这允许用户输入URL或本地文件路径，形式为普通字符串。该字符串可以手动输入位置栏、从剪贴板获取，或通过命令行参数传递。
当字符串还不是有效的 URL 时，会进行最佳猜测，并做出各种假设。
如果字符串对应系统中的有效文件路径，则会用`QUrl::fromLocalFile()`构建一个 file:// URL。
如果不是这样，会尝试将字符串转换为 http:// 或 ftp:// URL。如果字符串以“ftp”开头，则采用后者。结果随后通过`QUrl`的容忍解析器，在成功的情况下返回有效`QUrl`，或返回`QUrl()`。
- qt-project.org 变成 http://qt-project.org
- ftp.qt-project.org 变成 ftp://ftp.qt-project.org
- 主机名变 http://hostname
- /home/user/test.html 变为 file:///home/user/test.html
为了能够处理相对路径，该方法采用可选的`workingDirectory`路径。这在处理命令行参数时尤其有用。如果`workingDirectory`为空，则不会处理相对路径。
默认情况下，只有当文件实际存在于给定工作目录中时，输入字符串看起来像相对路径，才会被视为相对路径。如果应用程序能处理尚未存在的文件，它应该会在`options`中传递`AssumeLocalFile`该标志。

### `bool QUrl::hasFragment() const`

**作用与语义：**

如果该 URL 包含片段（即 # 在上面出现），返回 `true`。

### `bool QUrl::hasQuery() const`

**作用与语义：**

如果该URL包含查询（即？），返回`true`。

### `QString QUrl::host(QUrl::ComponentFormattingOptions options = FullyDecoded) const`

**作用与语义：**

如果URL被定义，返回该URL的主机;否则返回空字符串。
`options`参数控制主机名的格式化。`QUrl::EncodeUnicode`选项会使该函数返回ASCII兼容编码（ACE）形式的主机名，适用于非8位干净或需要遗留主机名的通道（如DNS请求或HTTP请求头）。如果不存在该标志，该函数会根据允许的顶级域名列表返回国际域名（IDN）的Unicode形式（参见`idnWhitelist()`）。
其他所有标志都被忽略。主机名不能包含控制字符或百分比字符，因此返回的值可以视为完全解码。

### `[static] QStringList QUrl::idnWhitelist()`

**作用与语义：**

返回当前允许组合中包含非ASCII字符的顶级域白名单。
有关该列表的理由，请参见`setIdnWhitelist()`。

### `bool QUrl::isEmpty() const`

**作用与语义：**

如果URL没有数据，返回`true`;否则返回`false`。

### `bool QUrl::isLocalFile() const`

**作用与语义：**

如果该 URL 指向本地文件路径，返回 `true`。如果方案是“file”，则该 URL 是本地文件路径。
注意，该函数将带有主机名的URL视为本地文件路径，即使最终的文件路径无法用`QFile::open()`打开。

### `bool QUrl::isParentOf(const QUrl &childUrl) const`

**作用与语义：**

如果该URL是`childUrl`的父网，返回`true`。如果两个网址共享相同的方案和权威，且该网址的路径是`childUrl`路径的父，`childUrl`是该网址的子网。

### `bool QUrl::isRelative() const`

**作用与语义：**

如果 URL 是相对的，则返回 `true`;否则返回 `false`。如果一个 URL 的方案未定义，则 URL 是相对引用;因此，该函数等价于调用 `scheme()`。`isEmpty()`。
相对参考定义见RFC 3986第4.2节。

### `bool QUrl::isValid() const`

**作用与语义：**

如果 URL 非空且有效，返回 `true`;否则返回 `false`。
该URL会经过一致性测试。URL的每一部分都必须符合URI标准的标准编码规则，才能报告该URL为有效。

**官方示例：**

```cpp
 bool checkUrl(const QUrl &url) {
     if (!url.isValid()) {
         qDebug("Invalid URL: %s", qUtf8Printable(url.toString()));
         return false;
     }

     return true;
 }
```

### `bool QUrl::matches(const QUrl &url, QUrl::FormattingOptions options) const`

**作用与语义：**

如果该URL和给定`url`相同，且对两者应用`options`，返回 `true`;否则返回 `false`。
这相当于调用两个URL的`adjusted`（选项）并比较结果的URL，但速度更快。

### `QString QUrl::password(QUrl::ComponentFormattingOptions options = FullyDecoded) const`

**作用与语义：**

如果 URL 已定义，则返回该 URL 的密码;否则返回空字符串。
`options`参数控制用户名组件的格式化。所有值都会产生明确的结果。使用`QUrl::FullyDecoded`时，所有百分比编码序列都会被解码;否则，返回的值可能包含某些控制序列的百分比编码序列，这些序列在`QString`中无法以解码形式表示。
请注意，如果存在这些不可表示的序列，可能会导致数据丢失`QUrl::FullyDecoded`。建议在结果将用于非URL上下文时使用该值，例如设置`QAuthenticator`或协商登录时。

### `QString QUrl::path(QUrl::ComponentFormattingOptions options = FullyDecoded) const`

**作用与语义：**

返回URL的路径。
`options`参数控制路径分量的格式化。所有值都会产生明确无歧义的结果。使用`QUrl::FullyDecoded`，所有百分比编码序列都被解码;否则，返回的值可能包含某些控制序列的百分比编码序列，这些序列在`QString`中无法以解码形式表示。
请注意，如果存在这些不可表示的序列，可能会导致数据丢失`QUrl::FullyDecoded`。建议在结果将用于非URL上下文（如发送到FTP服务器）时使用该值。
数据丢失的一个例子是，当你使用非Unicode的百分比编码序列并使用`FullyDecoded`（默认）：
在这个例子中，由于`%FF`无法转换，会有一定程度的数据丢失。
当路径包含子分界符（如`+`）时，也可能发生数据丢失：
其他解码示例：

**官方示例：**

```cpp
 qDebug() << QUrl("file:file.txt").path();                   // "file.txt"
 qDebug() << QUrl("/home/user/file.txt").path();             // "/home/user/file.txt"
 qDebug() << QUrl("http://www.example.com/test/123").path(); // "/test/123"
```

### `int QUrl::port(int defaultPort = -1) const`

**作用与语义：**

返回URL的端口，若端口未指定则返回`defaultPort`。

**官方示例：**

```cpp
 QTcpSocket sock;
 sock.connectToHost(url.host(), url.port(80));
```

### `QString QUrl::query(QUrl::ComponentFormattingOptions options = PrettyDecoded) const`

**作用与语义：**

如果存在查询字符串，返回 URL 的查询字符串;如果没有，返回空结果。要判断解析后的 URL 是否包含查询字符串，请使用 `hasQuery()`。
`options`参数控制查询组件的格式化。所有值都会产生明确无歧义的结果。使用`QUrl::FullyDecoded`时，所有百分比编码序列都会被解码;否则，返回的值可能包含某些控制序列的百分比编码序列，这些序列在`QString`中无法以解码形式表示。
请注意，不建议在查询中使用`QUrl::FullyDecoded`，因为查询通常包含应保持百分比编码的数据，包括使用“+”序列表示加号字符（' '）。

### `QUrl QUrl::resolved(const QUrl &relative) const`

**作用与语义：**

返回该 URL 与 `relative` 合并的结果。该 URL 作为基础，将 `relative` 转换为绝对 URL。
如果`relative`不是相对URL，该函数将直接返回`relative`。否则，两个URL的路径会合并，返回的新URL具有基础URL的格式和权威性，但路径是合并后的，如下示例所示：
调用 resolved() 时，带“..” 返回一个目录比原来高一级的`QUrl`。同样，调用 resolved() 时，用“../..” 从路径中移除两个层。如果 `relative` 是“/”，路径变为“/”。

**官方示例：**

```cpp
 QUrl baseUrl("http://qt.digia.com/Support/");
 QUrl relativeUrl("../Product/Library/");
 qDebug(qUtf8Printable(baseUrl.resolved(relativeUrl).toString()));
 // prints "http://qt.digia.com/Product/Library/"
```

### `QString QUrl::scheme() const`

**作用与语义：**

返回URL的方案。如果返回空字符串，表示方案未定义，URL为相对序列。
该方案只能包含 US-ASCII 字母或数字，这意味着不能包含任何需要编码的字符。此外，方案总是以小写形式返回。

### `void QUrl::setAuthority(const QString &authority, QUrl::ParsingMode mode = TolerantMode)`

**作用与语义：**

将URL的权威设置为`authority`。
URL 的权威性是用户信息、主机名和端口的组合。所有这些元素都是可选的;因此，空的权威是有效的。
用户信息和主机之间用“@”分隔，主机和端口之间用“：”分隔。如果用户信息为空，必须省略“@”;但如果端口为空，允许出现零散的“：”。
以下示例展示了一个有效的权威字符串：
`authority`数据的解释方式`mode`如下：在`StrictMode`中，任何“%”字符后面必须紧跟两个十六进制字符，且某些字符（包括空格）不允许在未解码形式中出现。在`TolerantMode`（默认）中，所有字符都接受未解码形式，容忍解析器会纠正未跟随两个十六进制字符的“%”。
该函数不允许`mode`被`QUrl::DecodedMode`。要设置完全解码的数据，分别调用`setUserName()`、`setPassword()`、`setHost()`和`setPort()`。

### `void QUrl::setFragment(const QString &fragment, QUrl::ParsingMode mode = TolerantMode)`

**作用与语义：**

将URL的片段设置为`fragment`。片段是URL的最后一部分，用“#”表示，后面跟一串字符。它通常用于HTTP中引用页面上的某个链接或点：
该片段有时也被称为URL“引用”。
传递 QString() 参数（空`QString`）会取消该片段。传递 `QString`（“”）（空但非空`QString`）的参数会将片段设置为空字符串（就像原始 URL 只有一个“#”一样）。
`fragment`数据的解释方式`mode`：在`StrictMode`中，任何“%”字符后面必须紧跟两个十六进制字符，且部分字符（包括空格）不允许在未解码形式中出现。在`TolerantMode`未解码形式中，所有字符都被接受，容忍解析器会纠正未跟两个十六进制字符的“%”。在 `DecodedMode`中，“%”本身代表，编码字符不可行。
当从非URL的数据源设置片段，或通过调用`QUrl::FullyDecoded`格式选项的 Brot `fragment()` 获得片段时，应使用`QUrl::DecodedMode`。

### `void QUrl::setHost(const QString &host, QUrl::ParsingMode mode = DecodedMode)`

**作用与语义：**

将URL的主机设置为`host`。主机是权限的一部分。
`host`数据的解释方式`mode`：在`StrictMode`中，任何“%”字符后面必须紧跟两个十六进制字符，且某些字符（包括空格）不允许在未解码形式中出现。在`TolerantMode`未解码形式中，所有字符都被接受，容忍解析器会纠正未被两个十六进制字符跟进的“%”。在`DecodedMode`中，“%”本身代表，编码字符不可行。
请注意，在所有情况下，解析结果必须是符合 STD 3 规则的有效主机名，该规则已由国际化资源标识符规范（RFC 3987）修改。不允许使用无效主机名，否则会导致`isValid()`变假。

### `[static] void QUrl::setIdnWhitelist(const QStringList &list)`

**作用与语义：**

将允许在域中包含非ASCII字符的顶级域（TLD）白名单设置为`list`。
注意，如果你调用这个函数，需要在启动任何可能访问`idnWhitelist()`的线程之前先调用。
Qt默认包含支持国际化域名（IDN）的互联网顶级域名，并制定规则确保外观相似的字符之间不会存在欺骗（如拉丁小写字母`'a'`和西里尔字母对应字母，在大多数字体中视觉上相同）。
该列表会定期维护，因为注册商会发布新规则。
此功能为需要操作列表以添加或删除顶级域名的人提供。不建议为测试目的更改其值，因为这可能使用户面临安全风险。

### `void QUrl::setPassword(const QString &password, QUrl::ParsingMode mode = DecodedMode)`

**作用与语义：**

将URL密码设置为`password`。`password`是URL权威中用户信息元素的一部分，如`setUserInfo()`所述。
`password`数据的解释方式`mode`：在`StrictMode`中，任意“%”字符后面必须紧跟两个十六进制字符，且某些字符（包括空格）不允许以未解码形式出现。在`TolerantMode`未解码形式中，所有字符都被接受，容忍解析器会纠正未被两个十六进制字符跟进的“%”。在`DecodedMode`中，“%”本身代表，编码字符不可行。
当设置密码时应使用`QUrl::DecodedMode`，比如从非URL的数据源设置密码，比如显示给用户的密码对话框，或通过`QUrl::FullyDecoded`格式选项调用`password()`获得的密码。

### `void QUrl::setPath(const QString &path, QUrl::ParsingMode mode = DecodedMode)`

**作用与语义：**

将URL路径设置为`path`。路径是URL中权威之后但查询字符串之前的部分。
对于非层级方案，路径将是方案声明后的所有路径，如下例所示：
`path`数据的解释方式`mode`如下：在`StrictMode`中，任意“%”字符后面必须紧跟两个十六进制字符，且某些字符（包括空格）不允许在未解码形式中出现。在`TolerantMode`未解码形式中，所有字符都被接受，容忍解析器会纠正未跟两个十六进制字符的“%”。在`DecodedMode`中，“%”本身代表，编码字符不可行。
当从非 URL 的数据源设置路径时，应使用`QUrl::DecodedMode`，例如向用户展示的对话或通过使用 `QUrl::FullyDecoded` 格式选项调用 `path()` 获得的路径。

### `void QUrl::setPort(int port)`

**作用与语义：**

将URL的端口设置为`port`。端口是URL权威的一部分，如`setAuthority()`所述。
`port`必须在0到65535之间（含）。将端口设置为-1表示端口未指定。

### `void QUrl::setQuery(const QString &query, QUrl::ParsingMode mode = TolerantMode)`

**作用与语义：**

将URL的查询字符串设置为`query`。
如果你需要传递一个不符合键值模式的查询字符串，或者使用与`QUrl`建议不同的特殊字符编码方案，这个函数非常有用。
将 QString() 的值传递给 `query`（空`QString`）会完全重置查询。然而，传递 `QString`（“”）的值会将查询设置为空值，就像原始 URL 只有一个“？”一样。
`query`数据的解释方式`mode`：在`StrictMode`中，任何“%”字符后面必须紧跟两个十六进制字符，且某些字符（包括空格）不允许在未解码形式中出现。在`TolerantMode`未解码形式中，所有字符都被接受，容忍解析器会纠正未跟两个十六进制字符的“%”。在 `DecodedMode`中，“%”本身代表，编码字符不可行。
查询字符串通常包含百分比编码序列，因此不建议使用`DecodedMode`。需要注意的一个特殊序列是加号字符（“' '）。`QUrl`不会将空格转换为加号字符，尽管网页浏览器发布的HTML表单会转换。为了在查询中表示实际的加号字符，通常使用序列”+“。该函数在`TolerantMode`或`StrictMode`中保持”+“序列不变。

### `void QUrl::setQuery(const QUrlQuery &query)`

**作用与语义：**

将URL的查询字符串设置为`query`。
该函数从`QUrlQuery`对象和该`QUrl`对象上的集合重建查询字符串。该函数没有解析参数，因为`QUrlQuery`包含已解析的数据。

### `void QUrl::setScheme(const QString &scheme)`

**作用与语义：**

将URL的方案设置为`scheme`。由于方案只能包含ASCII字符，因此不对输入进行转换或解码。它还必须以ASCII字母开头。
该方案描述了URL的类型（或协议）。它在URL开头用一个或多个ASCII字符表示。
方案严格符合RFC 3986标准：`scheme = ALPHA *( ALPHA / DIGIT / "+" / "-" / "." )`。
以下示例展示了一个 URL 格式为“ftp”：
为了设置该方案，使用以下调用：
该方案也可以是空的，此时URL被解释为相对的。

**官方示例：**

```cpp
 QUrl url;
 url.setScheme("ftp");
```

### `void QUrl::setUrl(const QString &url, QUrl::ParsingMode parsingMode = TolerantMode)`

**作用与语义：**

解析`url`并将该对象设置为该值。`QUrl` 会自动对所有不允许出现在 URL 中的字符进行百分比编码，并解码表示未保留字符的百分比编码序列（字母、数字、连字符、下划线、点和波浪号）。其他字符保持原始形式。
使用解析器模式`parsingMode`解析`url`。在`TolerantMode`（默认）中，`QUrl`会纠正某些错误，尤其是存在一个百分比字符（'%'）后面没有两个十六进制数字，并且接受任意位置的字符。在 `StrictMode` 中，不允许编码错误，`QUrl`还会检查某些禁止字符未编码的形式存在。如果在`StrictMode`中检测到错误，`isValid()` 返回 false。在此语境下不允许使用解析模式`DecodedMode`，且会生成运行时警告。

### `void QUrl::setUserInfo(const QString &userInfo, QUrl::ParsingMode mode = TolerantMode)`

**作用与语义：**

将URL的用户信息设置为`userInfo`。用户信息是URL权威性的可选部分，详见`setAuthority()`。
用户信息由用户名和可选的密码组成，中间用“：”分隔。如果密码为空，则必须省略冒号。以下示例展示了一个有效的用户信息字符串：
`userInfo`数据的解释方式`mode`：在`StrictMode`中，任何“%”字符后面必须紧跟两个十六进制字符，且某些字符（包括空格）不允许在未解码形式中出现。在`TolerantMode`（默认）中，所有字符都接受未解码形式，容忍解析器会纠正未跟随两个十六进制字符的“%”。
该函数不允许`mode` `QUrl::DecodedMode`。要设置完全解码的数据，分别调用`setUserName()`和`setPassword()`。

### `void QUrl::setUserName(const QString &userName, QUrl::ParsingMode mode = DecodedMode)`

**作用与语义：**

将URL的用户名设置为`userName`。`userName`是URL权威中用户信息元素的一部分，如`setUserInfo()`所述。
`userName`数据的解释方式`mode`如下：在`StrictMode`中，任何“%”字符后面必须紧跟两个十六进制字符，且某些字符（包括空格）在未解码形式中不被允许。在`TolerantMode`（默认）中，所有字符都接受未解码形式，容忍解析器会纠正未跟两个十六进制字符的“%”。在`DecodedMode`中，“%”本身代表，编码字符不存在。
当从非URL的数据源设置用户名时，应使用`QUrl::DecodedMode`，例如向用户显示的密码对话框，或通过`QUrl::FullyDecoded`格式选项调用`userName()`获得的用户名。

### `[noexcept] void QUrl::swap(QUrl &other)`

**作用与语义：**

将该URL与`other`交换。此操作非常快速且从未失败。

### `[static, since 6.3] QByteArray QUrl::toAce(const QString &domain, QUrl::AceProcessingOptions options = {})`

**作用与语义：**

返回给定域名的ASCII兼容编码 `domain`。输出可以通过传递带有`options`的标志来自定义。该函数的结果被视为等价于`domain`。
ASCII兼容编码（ACE）由RFC 3490、RFC 3491和RFC 3492定义，并由Unicode技术标准#46更新。它是国际化域名应用规范（IDNA）的一部分，允许使用非美国ASCII字符编写域名（如`"example.com"`）。
如果`domain`不是有效的主机名，该函数会返回空的`QByteArray`。特别注意，IPv6文字不是有效的域名。

### `CFURLRef QUrl::toCFURL() const`

**作用与语义：**

从`QUrl`创建CFURL。
调用者拥有CFURL并负责释放。

### `QString QUrl::toDisplayString(QUrl::FormattingOptions options = FormattingOptions(PrettyDecoded)) const`

**作用与语义：**

返回一个可显示的 URL 字符串表示。输出可以通过传递带有 `options` 的标志来自定义。`RemovePassword` 选项始终启用，因为密码不应向用户显示。
默认选项中，产生的`QString`可以以后传回给`QUrl`，但最初存在的任何密码都会丢失。

### `QByteArray QUrl::toEncoded(QUrl::FormattingOptions options = FullyEncoded) const`

**作用与语义：**

如果 URL 有效，返回编码后的 URL;否则返回空 `QByteArray`。输出可以通过传递带有 `options` 的标志来自定义。
用户信息、路径和片段均转换为 UTF-8，所有非 ASCII 字符则被编码为百分比。主机名则使用 Punycode 编码。

### `QString QUrl::toLocalFile() const`

**作用与语义：**

返回该URL的路径格式化为本地文件路径。返回的路径将使用斜杠，即使最初是反斜杠创建的。
如果该URL包含非空主机名，则以SMB网络中常见的形式编码为返回值（例如，“//servername/path/to/file.txt”）。
注意：如果该URL的路径成分包含非UTF-8二进制序列（如），该函数的行为未定义。

**官方示例：**

```cpp
 qDebug() << QUrl("file:file.txt").toLocalFile();            // "file.txt"
 qDebug() << QUrl("file:/home/user/file.txt").toLocalFile(); // "/home/user/file.txt"
 qDebug() << QUrl("file.txt").toLocalFile();                 // ""; wasn't a local file as it had no scheme
```

### `NSURL *QUrl::toNSURL() const`

**作用与语义：**

从`QUrl`创建NSURL。
NSURL是自动发布的。

### `[static] QByteArray QUrl::toPercentEncoding(const QString &input, const QByteArray &exclude = QByteArray(), const QByteArray &include = QByteArray())`

**作用与语义：**

返回编码后的`input`副本。`input`首先转换为UTF-8，所有不在未保留组中的ASCII字符均为百分比编码。为防止字符被百分比编码，传给`exclude`。为强制字符为百分比编码，则传给`include`。
无保留定义为：`ALPHA / DIGIT / "-" / "." / "_" / "~"`。

**官方示例：**

```cpp
 QByteArray ba = QUrl::toPercentEncoding("{a fishy string?}", "{}", "s");
 qDebug(ba.constData());
 // prints "{a fi%73hy %73tring%3F}"
```

### `QString QUrl::toString(QUrl::FormattingOptions options = FormattingOptions(PrettyDecoded)) const`

**作用与语义：**

返回URL的字符串表示。输出可以通过传递带有`options`的标志来自定义。该函数不允许选项`QUrl::FullyDecoded`，因为会产生歧义数据。
默认格式选项是`PrettyDecoded`。

### `[static] QStringList QUrl::toStringList(const QList<QUrl> &urls, QUrl::FormattingOptions options = FormattingOptions(PrettyDecoded))`

**作用与语义：**

将`urls`列表转换为`QString`对象列表，使用`toString`（`options`）。

### `QString QUrl::url(QUrl::FormattingOptions options = FormattingOptions(PrettyDecoded)) const`

**作用与语义：**

返回 URL 的字符串表示。输出可以通过传递带有 `options` 的标志来自定义。该函数不允许选项 `QUrl::FullyDecoded`，因为这会产生歧义数据。
所得`QString`可以以后传回给`QUrl`。
`toString`（选项）的同义词。

### `QString QUrl::userInfo(QUrl::ComponentFormattingOptions options = PrettyDecoded) const`

**作用与语义：**

返回URL的用户信息，如果用户信息未定义，则返回空字符串。
该函数返回一个明确的值，可能包含仍以百分比编码的字符，以及一些无法在`QString`中以解码形式表示的控制序列。
`options`参数控制用户信息组件的格式化。该函数不允许使用`QUrl::FullyDecoded`值。如果你需要获得完全解码的数据，分别调用`userName()`和`password()`。

### `QString QUrl::userName(QUrl::ComponentFormattingOptions options = FullyDecoded) const`

**作用与语义：**

如果URL被定义，返回用户名;否则返回空字符串。
`options`参数控制用户名组件的格式化。所有值都会产生明确无歧义的结果。使用`QUrl::FullyDecoded`，所有百分比编码序列都会被解码;否则，返回的值可能包含某些控制序列的百分比编码序列，这些序列在`QString`中无法以解码形式表示。
请注意，如果存在这些不可表示的序列，`QUrl::FullyDecoded`可能导致数据丢失。建议在非URL上下文中使用该值，如设置`QAuthenticator`或协商登录时。

### `[noexcept] QUrl &QUrl::operator=(QUrl &&other)`

**作用与语义：**

Move-assign `other`到该`QUrl`实例。

### `QUrl &QUrl::operator=(const QString &url)`

**作用与语义：**

将指定的`url`分配给该对象。
当`QT_NO_URL_CAST_FROM_STRING`宏定义时，该操作符不可用。

### `[noexcept] QUrl &QUrl::operator=(const QUrl &url)`

**作用与语义：**

将指定`url`分配给该对象。

### `[noexcept] bool operator!=(const QUrl &lhs, const QUrl &rhs)`

**作用与语义：**

如果 `lhs` 和 `rhs` 的 URL 不相等，则返回 `true`；否则返回 `false`。

### `QDataStream &operator<<(QDataStream &out, const QUrl &url)`

**作用与语义：**

向流`out`写入 URL `url`，并返回流的引用。

### `[noexcept] bool operator==(const QUrl &lhs, const QUrl &rhs)`

**作用与语义：**

如果 `lhs` 和 `rhs` URL 等效，则返回 `true`；否则返回 `false`。

### `QDataStream &operator>>(QDataStream &in, QUrl &url)`

**作用与语义：**

从流的`in`读取`url`的网址，并返回流的引用。

### `QT_NO_URL_CAST_FROM_STRING`

**作用与语义：**

禁用自动从`QString`（或字符*）转换为`QUrl`。
当你有很多文件名用`QString`的代码，想转换成`QUrl`以实现网络透明时，用这个定义编译代码非常有用。在任何使用`QUrl`的代码中，它可以帮助避免漏`QUrl::resolved()`调用，以及`QString` `QUrl`转换的其他误用。
例如，如果你有这样的代码。
你可以将其重写为。

**官方示例：**

```cpp
 url = filename; // probably not what you want
```

### `(since 6.3) enum AceProcessingOption { IgnoreIDNWhitelist, AceTransitionalProcessing }`

**作用与语义：**

ACE 处理选项控制 URL 如何转换为 ASCII 兼容编码以及如何从中转换回。
- `QUrl::IgnoreIDNWhitelist`：`0x1`；在将 URL 转换为 Unicode 时忽略 IDN 白名单。
- `QUrl::AceTransitionalProcessing`：`0x2`；使用 UTS #46 中描述的过渡处理。这允许更好地兼容 IDNA 2003 规范。
默认使用非过渡处理，并且仅允许 IDN 白名单列出的顶级域名内的 URL 包含非 ASCII 字符。
该枚举在 Qt 6.3 中引入。
AceProcessingOptions 类型是 QFlags<AceProcessingOption> 的 typedef。它存储 AceProcessingOption 值的按位或组合。

### `flags AceProcessingOptions`

**作用与语义：**

ACE 处理选项控制 URL 如何转换为 ASCII 兼容编码以及如何从中转换回。
- `QUrl::IgnoreIDNWhitelist`：`0x1`；在将 URL 转换为 Unicode 时忽略 IDN 白名单。
- `QUrl::AceTransitionalProcessing`：`0x2`；使用 UTS #46 中描述的过渡处理。这允许更好地兼容 IDNA 2003 规范。
默认使用非过渡处理，并且仅允许 IDN 白名单列出的顶级域名内的 URL 包含非 ASCII 字符。
该枚举在 Qt 6.3 中引入。
AceProcessingOptions 类型是 QFlags<AceProcessingOption> 的 typedef。它存储 AceProcessingOption 值的按位或组合。

### `enum ComponentFormattingOption { PrettyDecoded, EncodeSpaces, EncodeUnicode, EncodeDelimiters, EncodeReserved, …, FullyDecoded }`

**作用与语义：**

组件格式选项定义了 URL 组成部分在以文本形式写出时的格式化方式。当它们在`toString()`和`toEncoded()`中使用时，可以与 `QUrl::FormattingOptions` 中的选项结合使用。
- `QUrl::PrettyDecoded`：`0x000000`;该组件以“漂亮的形式”返回，大部分百分比编码字符已解码。PrettyDecoded 的具体行为因组件而异，且可能在不同 Qt 版本中有所不同。这是默认状态。
- `QUrl::EncodeSpaces`：`0x100000`;保持空格字符的编码形式（“”）。
- `QUrl::EncodeUnicode`：`0x200000`;非美国ASCII字符保持其UTF-8百分点编码形式（例如，U 00E9代码点用“é”，拉丁字母小写字母E带尖音）。
- `QUrl::EncodeDelimiters`：`0x400000 | 0x800000`;保持某些分隔符的编码形式，如完整URL以文本表示时URL中出现的。分隔符会受到该选项变化的影响。该标志在`toString()`或`toEncoded()`中无效。
- `QUrl::EncodeReserved`：`0x1000000`;在编码形式中，保留规范中不允许的 US-ASCII 字符。这是 `toString()` 和 `toEncoded()` 的默认设置。
- `QUrl::DecodeReserved`：`0x2000000`;解码URL规范不允许出现在URL中的US-ASCII字符。这是单个组件获取者的默认设置。
- `QUrl::FullyEncoded`：`EncodeSpaces | EncodeUnicode | EncodeDelimiters | EncodeReserved`;保持所有字符正确编码的形式，因为该组件会作为URL的一部分出现。当与`toString()`一起使用时，这会产生一个完全符合规范的URL，完全符合`QString`的形式，结果与`toEncoded()`
- `QUrl::FullyDecoded`：`FullyEncoded | DecodeReserved | 0x4000000`;尽量解码尽可能多的部分。对于URL的各个组成部分，解码所有百分比编码序列，包括控制字符（U 0000到U 001F）和以百分比编码形式出现的UTF-8序列。使用此模式可能导致数据丢失，详见下文。
EncodeReserved 和 DecodeReserved 的值不应在同一次调用中同时使用。如果发生这种情况，行为是未定义的。它们作为独立值提供是因为“漂亮模式”在保留字符的行为在某些组件上不同，尤其是在完整 URL 上。
完全解码模式类似于Qt 4.x中返回`QString`的函数行为，每个字符都代表自己，且没有特殊含义。这对百分比字符（“%”）同样适用，应将其解释为字面意义的百分比，而非百分比编码序列的开头。在所有其他解码模式下，同一字符由序列“%”表示。
每当将用 QUrl：：FullyDecoded 获得的数据重新应用到`QUrl`时，必须注意使用`QUrl::DecodedMode`参数作为 setter（如 `setPath()` 和 `setUserName()`）。未这样做可能导致百分比字符（“%”）被重新解释为百分比编码序列的开头。
当URL的部分内容出现在非URL上下文时，该模式非常有用。例如，在FTP客户端应用中提取用户名、密码或文件路径时，应使用FullyDecoded模式。
此模式应谨慎使用，因为有两种情况在返回的 `QString` 中无法可靠表示。它们是：
- 非 UTF-8 序列：URL 可能包含不形成有效 UTF-8 序列的百分号编码字符序列。由于 URL 需要使用 UTF-8 解码，任何解码器失败都会导致 `QString` 在该序列存在的位置包含一个或多个替换字符。
- 编码分隔符：URL 也允许区分其字面形式的分隔符和百分号编码形式的等效分隔符。这在查询中最常见，但在 URL 的大多数部分都是允许的。
以下示例说明了该问题：
如果通过 HTTP GET 使用这两个 URL，Web 服务器的解释可能不同。第一种情况，它将解释为一个参数，键为 "q"，值为 "a =b&c"。第二种情况，它可能解释为两个参数，一个键为 "q"，值为 "a =b"，另一个键为 "c"，无值。
ComponentFormattingOptions 类型是 QFlags<ComponentFormattingOption> 的 typedef。它存储 ComponentFormattingOption 值的 OR 组合。

**官方示例：**

```cpp
 QUrl original("http://example.com/?q=a%2B%3Db%26c");
 QUrl copy(original);
 copy.setQuery(copy.query(QUrl::FullyDecoded), QUrl::DecodedMode);

 qDebug() << original.toString();   // prints: http://example.com/?q=a%2B%3Db%26c
 qDebug() << copy.toString();       // prints: http://example.com/?q=a+=b&c
```

### `flags ComponentFormattingOptions`

**作用与语义：**

组件格式选项定义了 URL 组成部分在以文本形式写出时的格式化方式。当它们在`toString()`和`toEncoded()`中使用时，可以与 `QUrl::FormattingOptions` 中的选项结合使用。
- `QUrl::PrettyDecoded`：`0x000000`;该组件以“漂亮的形式”返回，大部分百分比编码字符已解码。PrettyDecoded 的具体行为因组件而异，且可能在不同 Qt 版本中有所不同。这是默认状态。
- `QUrl::EncodeSpaces`：`0x100000`;保持空格字符的编码形式（“”）。
- `QUrl::EncodeUnicode`：`0x200000`;非美国ASCII字符保持其UTF-8百分点编码形式（例如，U 00E9代码点用“é”，拉丁字母小写字母E带尖音）。
- `QUrl::EncodeDelimiters`：`0x400000 | 0x800000`;保持某些分隔符的编码形式，如完整URL以文本表示时URL中出现的。分隔符会受到该选项变化的影响。该标志在`toString()`或`toEncoded()`中无效。
- `QUrl::EncodeReserved`：`0x1000000`;在编码形式中，保留规范中不允许的 US-ASCII 字符。这是 `toString()` 和 `toEncoded()` 的默认设置。
- `QUrl::DecodeReserved`：`0x2000000`;解码URL规范不允许出现在URL中的US-ASCII字符。这是单个组件获取者的默认设置。
- `QUrl::FullyEncoded`：`EncodeSpaces | EncodeUnicode | EncodeDelimiters | EncodeReserved`;保持所有字符正确编码的形式，因为该组件会作为URL的一部分出现。当与`toString()`一起使用时，这会产生一个完全符合规范的URL，完全符合`QString`的形式，结果与`toEncoded()`
- `QUrl::FullyDecoded`：`FullyEncoded | DecodeReserved | 0x4000000`;尽量解码尽可能多的部分。对于URL的各个组成部分，解码所有百分比编码序列，包括控制字符（U 0000到U 001F）和以百分比编码形式出现的UTF-8序列。使用此模式可能导致数据丢失，详见下文。
EncodeReserved 和 DecodeReserved 的值不应在同一次调用中同时使用。如果发生这种情况，行为是未定义的。它们作为独立值提供是因为“漂亮模式”在保留字符的行为在某些组件上不同，尤其是在完整 URL 上。
完全解码模式类似于Qt 4.x中返回`QString`的函数行为，每个字符都代表自己，且没有特殊含义。这对百分比字符（“%”）同样适用，应将其解释为字面意义的百分比，而非百分比编码序列的开头。在所有其他解码模式下，同一字符由序列“%”表示。
每当将用 QUrl：：FullyDecoded 获得的数据重新应用到`QUrl`时，必须注意使用`QUrl::DecodedMode`参数作为 setter（如 `setPath()` 和 `setUserName()`）。未这样做可能导致百分比字符（“%”）被重新解释为百分比编码序列的开头。
当URL的部分内容出现在非URL上下文时，该模式非常有用。例如，在FTP客户端应用中提取用户名、密码或文件路径时，应使用FullyDecoded模式。
此模式应谨慎使用，因为有两种情况在返回的 `QString` 中无法可靠表示。它们是：
- 非 UTF-8 序列：URL 可能包含不形成有效 UTF-8 序列的百分号编码字符序列。由于 URL 需要使用 UTF-8 解码，任何解码器失败都会导致 `QString` 在该序列存在的位置包含一个或多个替换字符。
- 编码分隔符：URL 也允许区分其字面形式的分隔符和百分号编码形式的等效分隔符。这在查询中最常见，但在 URL 的大多数部分都是允许的。
以下示例说明了该问题：
如果通过 HTTP GET 使用这两个 URL，Web 服务器的解释可能不同。第一种情况，它将解释为一个参数，键为 "q"，值为 "a =b&c"。第二种情况，它可能解释为两个参数，一个键为 "q"，值为 "a =b"，另一个键为 "c"，无值。
ComponentFormattingOptions 类型是 QFlags<ComponentFormattingOption> 的 typedef。它存储 ComponentFormattingOption 值的 OR 组合。

**官方示例：**

```cpp
 QUrl original("http://example.com/?q=a%2B%3Db%26c");
 QUrl copy(original);
 copy.setQuery(copy.query(QUrl::FullyDecoded), QUrl::DecodedMode);

 qDebug() << original.toString();   // prints: http://example.com/?q=a%2B%3Db%26c
 qDebug() << copy.toString();       // prints: http://example.com/?q=a+=b&c
```

### `flags FormattingOptions`

**作用与语义：**

格式选项定义了URL在以文本形式写出来时的格式化。
- `QUrl::None`：`0x0`;URL格式未变。
- `QUrl::RemoveScheme`：`0x1`;该方案从URL中移除。
- `QUrl::RemovePassword`：`0x2`;URL中的任何密码都会被移除。
- `QUrl::RemoveUserInfo`：`RemovePassword | 0x4`;URL中的任何用户信息都会被删除。
- `QUrl::RemovePort`：`0x8`;任何指定的端口都会从URL中移除。
- `QUrl::RemoveAuthority`：`RemoveUserInfo | RemovePort | 0x10`;移除用户名、密码、主机和端口。
- `QUrl::RemovePath`：`0x20`;URL路径被移除，只剩下方案、主机地址和端口（如存在）。
- `QUrl::RemoveQuery`：`0x40`;URL中带有“？”字符的查询部分被移除。
- `QUrl::RemoveFragment`：`0x80`;URL中的片段部分（包括“#”字符）被移除。
- `QUrl::RemoveFilename`：`0x800`;文件名（即路径中最后一个“/”之后的所有部分）被移除。尾部的“/”保留，除非设置了StripTrailingSlash。只有当RemovePath未被设置时才有效。
- `QUrl::PreferLocalFile`：`0x200`;如果 URL 是本地文件，且`isLocalFile()`中没有查询或片段，则返回本地文件路径。
- `QUrl::StripTrailingSlash`：`0x400`;如果有后斜杠，则从路径中移除。
- `QUrl::NormalizePathSegments`：`0x1000`;修改路径以去除冗余的目录分隔符，并解析“.”s 和 “..”尽可能多。对于非本地路径，相邻的斜杠会被保留。
请注意，Nameprep 中的大小写折叠规则（`QUrl`符合），要求主机名始终转换为小写，无论使用 Qt：：FormattingOptions 格式如何。
`QUrl::ComponentFormattingOptions`的选项也是可能的。
FormattingOptions 类型是 QFlags 的 typedef<UrlFormattingOption>。它存储 UrlFormattingOption 值的 OR 组合。

### `enum UrlFormattingOption { None, RemoveScheme, RemovePassword, RemoveUserInfo, RemovePort, …, NormalizePathSegments }`

**作用与语义：**

格式选项定义了URL在以文本形式写出来时的格式化。
- `QUrl::None`：`0x0`;URL格式未变。
- `QUrl::RemoveScheme`：`0x1`;该方案从URL中移除。
- `QUrl::RemovePassword`：`0x2`;URL中的任何密码都会被移除。
- `QUrl::RemoveUserInfo`：`RemovePassword | 0x4`;URL中的任何用户信息都会被删除。
- `QUrl::RemovePort`：`0x8`;任何指定的端口都会从URL中移除。
- `QUrl::RemoveAuthority`：`RemoveUserInfo | RemovePort | 0x10`;移除用户名、密码、主机和端口。
- `QUrl::RemovePath`：`0x20`;URL路径被移除，只剩下方案、主机地址和端口（如存在）。
- `QUrl::RemoveQuery`：`0x40`;URL中带有“？”字符的查询部分被移除。
- `QUrl::RemoveFragment`：`0x80`;URL中的片段部分（包括“#”字符）被移除。
- `QUrl::RemoveFilename`：`0x800`;文件名（即路径中最后一个“/”之后的所有部分）被移除。尾部的“/”保留，除非设置了StripTrailingSlash。只有当RemovePath未被设置时才有效。
- `QUrl::PreferLocalFile`：`0x200`;如果 URL 是本地文件，且`isLocalFile()`中没有查询或片段，则返回本地文件路径。
- `QUrl::StripTrailingSlash`：`0x400`;如果有后斜杠，则从路径中移除。
- `QUrl::NormalizePathSegments`：`0x1000`;修改路径以去除冗余的目录分隔符，并解析“.”s 和 “..”尽可能多。对于非本地路径，相邻的斜杠会被保留。
请注意，Nameprep 中的大小写折叠规则（`QUrl`符合），要求主机名始终转换为小写，无论使用 Qt：：FormattingOptions 格式如何。
`QUrl::ComponentFormattingOptions`的选项也是可能的。
FormattingOptions 类型是 QFlags 的 typedef<UrlFormattingOption>。它存储 UrlFormattingOption 值的 OR 组合。

### `enum UserInputResolutionOption { DefaultResolution, AssumeLocalFile }`

**作用与语义：**

用户输入解析选项定义了`fromUserInput()`应如何解释字符串，这些字符串可以是相对路径，也可以是HTTP URL的简短形式。例如，`file.pl`可以是本地文件或URL的 `http://file.pl`。
- `QUrl::DefaultResolution`：`0`;默认解析机制是检查`fromUserInput`工作目录中是否存在本地文件，并仅返回本地路径。否则假设为 URL。
- `QUrl::AssumeLocalFile`：`1`;该选项使`fromUserInput()`除非输入包含方案（如 `http://file.pl`），否则始终返回本地路径。这对文本编辑器等应用程序非常有用，因为它们能够在不存在文件时创建该路径。
UserInputResolutionOptions 类型是 QFlags 的 typedef<UserInputResolutionOption>。它存储 UserInputResolutionOption 值的 OR 组合。

### `flags UserInputResolutionOptions`

**作用与语义：**

用户输入解析选项定义了`fromUserInput()`应如何解释字符串，这些字符串可以是相对路径，也可以是HTTP URL的简短形式。例如，`file.pl`可以是本地文件或URL的 `http://file.pl`。
- `QUrl::DefaultResolution`：`0`;默认解析机制是检查`fromUserInput`工作目录中是否存在本地文件，并仅返回本地路径。否则假设为 URL。
- `QUrl::AssumeLocalFile`：`1`;该选项使`fromUserInput()`除非输入包含方案（如 `http://file.pl`），否则始终返回本地路径。这对文本编辑器等应用程序非常有用，因为它们能够在不存在文件时创建该路径。
UserInputResolutionOptions 类型是 QFlags 的 typedef<UserInputResolutionOption>。它存储 UserInputResolutionOption 值的 OR 组合。

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

`QUrl` 所属机制类型：Qt 值类型与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
