# Qt QUrl：解析、组合和传递 URL，而不是把路径当字符串

`QUrl` 是 Qt Core 的 URL 值类型。它把一个地址拆成 scheme、authority、path、query、fragment 等有语义的组件，再负责 URI 百分号编码、Unicode 域名和相对地址解析。网络请求、打开文件、深链接、WebSocket 地址、富文本链接和跨平台文件 URL，都是它的典型使用位置。

它不是网络客户端，不会发起连接、判断服务器是否存在，也不是文件系统路径类。`QUrl` 只回答“这串内容能否表示一个 URL、各组件是什么、应如何编码/组合”；访问控制、协议白名单、文件路径规范化和网络错误处理必须由调用方完成。

```cpp
#include <QDebug>
#include <QUrl>

using namespace Qt::StringLiterals;

const QUrl apiUrl(u"https://api.example.com/v1/items?q=Qt 6"_s);
if (!apiUrl.isValid())
    qWarning().noquote() << apiUrl.errorString();

```

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QUrl>`  
> CMake：`Qt6::Core`  
> 线程：所有成员函数可重入；同一个可变 `QUrl` 实例仍不应在没有同步的情况下被多个线程同时读写。

## 它解决什么问题

手写 URL 字符串看似简单，却很容易把不同层次混在一起：

- 空格、`#`、`?`、`%` 什么时候是数据，什么时候是分隔符；
- `https://user:pass@host/path` 中真正的 host 是谁；
- `file:///...` 是本地文件 URL，`C:\...` 只是 Windows 路径；
- `../image.png` 必须相对某个 base URL 解析，不能靠字符串拼接；
- 域名可能是 Unicode，线上传输又要求 ASCII/Punycode；
- query 的键值、顺序和分隔规则需要独立处理。

`QUrl` 将前四类结构化问题集中处理，并提供明确的编码和格式化选项。query 项的增删、重复键和分隔符策略则属于 `QUrlQuery`，本页只说明 `QUrl::query()` 与 `setQuery()` 的边界。

## URL 组件与值语义

一个典型 URL 的结构如下：

```text
scheme://user:password@host:port/path?query#fragment
```

并非每个组件都必须出现。没有 scheme 的 URL 是相对 URL：

```cpp
Q_ASSERT(QUrl(u"images/logo.svg"_s).isRelative());
Q_ASSERT(!QUrl(u"file:images/logo.svg"_s).isRelative());
```

第二个例子虽然看起来也是相对路径，但它已有 `file` scheme，因此在 URL 语义上不再是相对 URL。这会直接影响 `resolved()`，是本类最常见的坑之一。

`QUrl` 是隐式共享的普通值类型：可以复制、移动、放入容器和跨函数传递，不具有 `QObject` 父子关系，也不需要事件循环。`detach()` / `isDetached()` 是隐式共享实现的低层接口；业务代码通常让写操作按需分离即可，不要为“优化”而随意调用 `detach()`。

构建配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

## 两条输入路径：协议文本与用户输入

### 已知是 URL：构造、`setUrl()` 或 `fromEncoded()`

当输入来自配置、协议、数据库或另一个 URL API，调用方已知道它是 URL 时，用 `QUrl(QString, mode)`、`setUrl()` 或 `fromEncoded()`：

```cpp
QUrl service;
service.setUrl(u"https://example.com/a%2Fb?sort=name"_s, QUrl::StrictMode);

const QUrl wireUrl = QUrl::fromEncoded(
    QByteArrayView("https://xn--bhler-kva.example.com/a%20b"),
    QUrl::StrictMode);
```

`QString` 输入是面向可读文本的 URL 表示；`fromEncoded()` 则接收线上传输用的字节表示。不要先对完整 URL 调用 `fromPercentEncoding()` 再交给构造函数，这会过早把 `%2F`、`%23` 等“数据中的保留字符”变回路径或 fragment 分隔符。

### 真的来自人：`fromUserInput()`

地址栏、文件选择框附加文本或命令面板允许用户输入 `example.com`、相对文件名、本地路径和完整 URL；此时可以使用启发式入口：

```cpp
const QUrl target = QUrl::fromUserInput(
    textFromAddressBar, QDir::currentPath());
```

它会尝试把不完整输入解释为 URL 或本地文件，适合“尽量帮用户猜对”的界面。`AssumeLocalFile` 可让歧义输入优先被解释为本地文件。

这不是可信协议数据的解析器。下载器、OAuth 回调、插件 URI、策略文件或权限边界中的输入，不应依赖它猜测 scheme 或 host；应使用 `StrictMode` 解析，再逐项校验允许的 scheme、host、port、path 和是否含用户信息。

```cpp
bool isAllowedHttpsEndpoint(const QUrl &url)
{
    return url.isValid()
        && url.scheme() == u"https"_s
        && url.host() == u"api.example.com"_s
        && url.userInfo().isEmpty()
        && url.port(443) == 443;
}
```

`isValid()` 仅是 URL 结构/编码有效性检查，不表示 URL 可信、可访问、DNS 可解析，或路径不会越权。

## 解析模式：`%` 的含义不能猜

`ParsingMode` 控制字符串作为 URL 文本时的处理方式：

| 模式 | 适用输入 | 行为与边界 |
| --- | --- | --- |
| `TolerantMode` | 地址栏和宽松兼容场景 | 默认值。尽量接受字符并修正部分常见编码错误，例如孤立的 `%`。适合用户体验，不适合严格协议校验。 |
| `StrictMode` | 可信格式要求明确的 URL 文本 | 拒绝非法百分号编码和不允许以未编码形式出现的字符；出错后 `isValid()` 为 `false`，用 `errorString()` 诊断。 |
| `DecodedMode` | 单独设置“非 URL 来源”的组件值 | `%` 被视作普通数据，不能再表达百分号转义。只适用于支持它的 component setter，例如 `setPath()`、`setHost()`、`setUserName()`、`setPassword()`。 |

完整 URL 的构造函数和 `setUrl()` 不允许 `DecodedMode`，会给出运行时警告；完整 URL 中必须保留编码层次，避免 `?`、`#`、`/` 等字符的结构含义变得无法判定。`setAuthority()`、`setUserInfo()` 也不允许 `DecodedMode`，因为它们各自还要继续拆分子组件。

对来自密码框、文件名输入框等“明确不是 URL 文本”的单个字段，优先使用相应 setter 的默认 `DecodedMode`：

```cpp
QUrl url;
url.setScheme(u"https"_s);
url.setHost(u"example.com"_s);
url.setPath(u"/reports/July #1.pdf"_s); // '#' is data here
```

不要把 HTML 表单编码和 URL 百分号编码混为一谈。`QUrl` 不会把 `+` 自动解释为空格；若服务端采用 `application/x-www-form-urlencoded` 规则，应在请求业务层或 `QUrlQuery` 的专门规则中处理。

## 输出模式：显示、传输和取组件是三件事

`QUrl` 既要保留无歧义的 URL 结构，又要给人类显示可读文字，因此输出 API 的选项不能随意互换。

| 目标 | 推荐 API | 核心语义 |
| --- | --- | --- |
| 发送给网络层、保存为 URI 字节 | `toEncoded(QUrl::FullyEncoded)` | user info、path、fragment 先转 UTF-8，再对非 ASCII 字节和必要保留字符百分号编码；host 转为 Punycode。无效 URL 返回空 `QByteArray`。 |
| 一般调试或可再解析的文本 | `toString()` / `url()` | 默认 `PrettyDecoded`，可读但保持无歧义；`url()` 是 `toString()` 的同义 API。 |
| 给界面显示 | `toDisplayString()` | 始终隐含 `RemovePassword`，不会把密码回显。用户名、token query 等仍可能泄漏，日志也应按业务继续脱敏。 |
| 把单一组件交给非 URL 业务 | `path(FullyDecoded)`、`userName(FullyDecoded)` 等 | 可将百分号序列完全解码；对于无法用 `QString` 表示的字节可能有信息损失，不应再把结果当 URL 重新拼回去。 |

`PrettyDecoded` 是默认的折中表示：Qt 仅解码不引起 URL 歧义的内容。`FullyEncoded` 强制编码空间、Unicode、分隔符和保留字符。`FullyDecoded` 则是“离开 URL 世界、要得到业务文本”时的选项，**不允许传给** `toString()` / `url()`，因为完整 URL 一旦把保留字符全解码，就无法确认它原本是数据还是结构。

`authority()` 和 `userInfo()` 同样不允许 `FullyDecoded`，应改为分别读取 `userName()`、`password()`、`host()`、`port()`。这是 API 有意保留的无歧义边界。

除组合预设外，`ComponentFormattingOptions` 还提供 `EncodeSpaces`、`EncodeUnicode`、`EncodeDelimiters`、`EncodeReserved` 与 `DecodeReserved`，用于精细控制单个组件的序列化。`FormattingOptions` 可以再组合 `RemoveQuery`、`RemoveFragment` 等 URL 结构删除选项：

```cpp
const QUrl cacheKey = url.adjusted(
    QUrl::RemoveFragment | QUrl::NormalizePathSegments);

const QString origin = url.toString(
    QUrl::RemovePath | QUrl::RemoveQuery | QUrl::RemoveFragment);
```

`NormalizePathSegments` 只按 URL 规则处理 `.` 与 `..` 段，不会解析文件系统符号链接，也不等价于本地文件安全校验。

## 本地路径、`file:` URL 与相对解析

需要把本地路径交给 `QDesktopServices`、`QMediaPlayer`、网络 API 或 QML 时，使用 `fromLocalFile()`：

```cpp
const QString nativePath = QDir::cleanPath(
    QDir::home().filePath(u"Documents/report.pdf"_s));
const QUrl fileUrl = QUrl::fromLocalFile(nativePath);
```

它的参数必须是**路径**，不是已经带 `file:` 的 URL。绝对路径会生成类似 `file:///home/me/report.pdf` 的 URL；相对路径会生成 `file:report.pdf`。后者已有 scheme，不能直接作为 `resolved()` 的 relative 参数：

```cpp
QUrl base(u"file:/home/me/docs/"_s);
QUrl wrong = QUrl::fromLocalFile(u"report.pdf"_s);
Q_ASSERT(!wrong.isRelative());

QUrl relative(u"report.pdf"_s);
QUrl full = base.resolved(relative);
```

`toLocalFile()` 只对 `file` URL 有意义；普通相对 URL 没有 scheme 时返回空字符串。返回路径统一使用正斜杠；具有 host 的 file URL 会以 SMB/UNC 形式表示，例如 `//server/share/file.txt`。路径中若含非 UTF-8 的二进制百分号序列，`toLocalFile()` 的行为未定义，不要把它用于承载任意原始字节。

`isLocalFile()` 只识别 URL scheme，不验证文件存在，也不保证最终路径位于许可目录。若处理不可信的文件 URL，先转换到路径，再用操作系统或 `QFileInfo` 的规范化路径、符号链接策略和目录边界检查做授权。

## 相对 URL：用 `resolved()`，不要手工拼接

`resolved()` 按 URL 解析规则将相对 URL 合并到 base URL：

```cpp
const QUrl base(u"https://docs.example.com/guide/intro/"_s);
const QUrl target = base.resolved(QUrl(u"../assets/logo.svg"_s));
// https://docs.example.com/guide/assets/logo.svg
```

关键边界：

- `relative` 只要带 scheme，就被视为独立 URL；base 的 scheme、host、路径不会补进去。
- base 最后是否有 `/` 会改变最后一个路径段是“目录”还是“文件”的解释。
- `resolved()` 是 URL 层的点段合并，不进行 HTTP 重定向、不访问网络，也不做本地文件规范化。
- `isRelative()` 的定义只有“scheme 为空”，与“path 看起来相对”不是一回事。

`isParentOf()` 适合 URL 树状导航、资源浏览器等比较：它检查一个 URL 是否是另一个 URL 的父级。不要拿它作为沙箱安全判断，特别是 file URL 的符号链接、Windows 大小写/卷规则、编码别名和访问权限都不在这个比较的职责范围内。

## 组件构造：组合 API 方便，分量 API 更可控

`setAuthority()` 一次设置 username、password、host、port；`setUserInfo()` 一次设置 username 和 password。输入本身已经是完整 authority/userinfo URL 文本时很方便：

```cpp
QUrl url;
url.setScheme(u"https"_s);
url.setAuthority(u"alice:secret@example.com:8443"_s, QUrl::StrictMode);
url.setPath(u"/v1/status"_s);
```

但对独立业务字段，更稳妥的是分别调用 `setUserName()`、`setPassword()`、`setHost()`、`setPort()`。这样不会把字段里的 `@`、`:`、`/` 意外解释成 authority 分隔符。`setPort(-1)` 可移除显式端口；`port(defaultPort)` 在 URL 未显式带端口时返回调用方给出的默认值。

`hasQuery()` / `hasFragment()` 用于区分“组件不存在”和“组件存在但为空”的结构情况。构造 query 时优先创建 `QUrlQuery` 后 `setQuery(queryObject)`；仅在已有完整 query URL 文本时使用 `setQuery(QString, mode)`。

`fileName()` 只从 URL path 取最后一段，不访问文件系统，也不保证结果是平台意义上的文件名。

## 国际化域名与 IDN

URL 的 host 可以面向用户显示为 Unicode，例如 `bühler.example.com`，线上表示则使用 ACE/Punycode，例如 `xn--bhler-kva.example.com`。`toEncoded()` 已会完成 host 的 ACE 转换，绝大多数网络代码不必显式调用转换函数。

`toAce()` 与 `fromAce()` 适合确实需要单独处理**域名**的场景，例如域名审核器或协议适配器：

```cpp
const QByteArray ace = QUrl::toAce(u"bühler.example.com"_s);
const QString unicodeHost = QUrl::fromAce(ace);
```

二者自 Qt 6.3 起可带 `AceProcessingOptions`：

- `IgnoreIDNWhitelist`：忽略 Qt 的 IDN 白名单策略；
- `AceTransitionalProcessing`：请求 IDNA 的 transitional processing。

输入必须是域名，而不是含 scheme、端口或 IPv6 字面量的完整 host 字符串。`idnWhitelist()` / `setIdnWhitelist()` 读取和修改的是进程级 IDN 白名单策略；应用若确有修改需求，应在初始化阶段统一完成，避免不同模块对显示/转换策略产生不一致的预期。

安全审核时，不应仅根据用户可见的 Unicode 域名做许可判断。对 allowlist 使用 `url.host()` 提取结构化 host，并明确处理大小写、ACE/Unicode 形式和子域规则；`https://trusted.example@evil.example/` 的 host 是 `evil.example`。

## 有效性、比较、序列化与平台接口

解析或 setter 失败后可读取 `errorString()`，并在继续构造前 `clear()` 或重新 `setUrl()`。一个无效 `QUrl` 不应被继续当作“部分可用的地址”交给网络层。

`operator==` 比较 URL 的等价性；`matches(other, options)` 可在忽略某些组件后比较，常用于忽略 fragment 或 query 的缓存、导航逻辑：

```cpp
const bool sameDocument = left.matches(
    right, QUrl::RemoveFragment | QUrl::RemoveQuery);
```

这不是 URL 安全同源策略，也不会替代业务端口、host 和证书检查。`qHash()` 支持把 `QUrl` 放入 `QHash` / `QSet`；`QDataStream` 的 `<<` / `>>` 只用于双方约定了流版本的二进制数据，不能把它当作跨版本公开协议格式。

在 Apple 平台上，`fromCFURL()` / `toCFURL()` 和 `fromNSURL()` / `toNSURL()` 用于与 Core Foundation、Objective-C API 互转。`toCFURL()` 返回的对象由调用方负责释放；`toNSURL()` 返回 autoreleased 对象。这些 API 不会在非 Darwin 平台上提供。

## 常见错误

- 把本地路径直接传入 `QUrl(path)`。这只是在解析 URL 文本；要表示文件应使用 `fromLocalFile(path)`。
- 把 `fromUserInput()` 用作安全协议解析。它的目标是猜测用户意图，而不是拒绝歧义。
- 对完整 URL 手工 percent-decode 后再解析，导致 `%2F` 或 `%23` 改变组件边界。
- 将 `FullyDecoded` 用在 `toString()` 或 `userInfo()`。这些 API 明确禁止这种可能产生歧义的格式。
- 以为 `toDisplayString()` 就能安全写日志。它确实移除密码，但 query 中的 token、用户名和隐私路径仍可能存在。
- 以为 `isValid()` 意味着“可连接”“可信”或“文件可访问”。
- 把 `file:relative.txt` 当成 relative URL 交给 `resolved()`，结果 base URL 没有参与合并。
- 用字符串前缀、`isParentOf()` 或 `NormalizePathSegments` 实现本地文件授权。
- 把 Unicode 域名显示结果直接做许可比较，遗漏 Punycode、子域和 userinfo 欺骗。
- 对 query 手动拼接 `name=value`。有重复键、空值、保留字符或自定义分隔符时交给 `QUrlQuery`。

## 逐项 API 说明

### 构造、状态与解析

#### `QUrl()`、复制/移动构造和赋值

默认构造为空 URL；复制和移动只处理值语义，不产生网络或文件系统动作。`QT_NO_URL_CAST_FROM_STRING` 未定义时，`QString` 构造与赋值是隐式可用的，易把路径误当 URL；大型项目可定义该宏，让这类转换必须显式书写。

#### `setUrl()`、`fromEncoded()` 与 `fromStringList()`

前者处理 `QString` URL 文本，后两者分别处理已编码字节与批量转换。输入不是完整 URL、或者必须拒绝错误编码时使用 `StrictMode`。`setUrl()` 不允许 `DecodedMode`；失败后检查 `isValid()` 和 `errorString()`。

#### `isEmpty()`、`clear()`、`isValid()` 与 `errorString()`

空 URL 与无效 URL 是不同状态。`clear()` 使对象回到空状态；`isValid()` 只验证 URL 语法/编码；无效后先清空或重新解析，不要继续追加组件。

### 组件访问和设置

`authority` = userinfo + host + port；`userInfo` = username + 可选 password。组合 getter/setter 的 `DecodedMode` / `FullyDecoded` 限制，是为了不破坏其中分隔符的语义。单独访问 `userName()`、`password()`、`host()`、`path()` 才适合需要完全解码的非 URL 业务值。

`setScheme()` 可设为空，从而令 URL 变成相对 URL；`setPort(-1)` 清除端口。`query()` / `setQuery(QString)` 面对的是整体 query 文本，键值操作使用 `QUrlQuery`。

### 格式化、转换与比较

`toString()`、`url()`、`toDisplayString()` 都返回 `QString`，但它们的安全和可逆性不同；传输优先 `toEncoded()`。`adjusted()` 返回修改后的副本而不改变原 URL。`matches()` 的 options 是“忽略/调整哪些 URL 组件”，不包含网络或权限语义。

## API 速查表

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `QUrl()` | 创建空 URL | 空不等于无效；无 I/O。 |
| `QUrl(const QString &, ParsingMode)` | 解析完整 URL 文本 | 默认宽松；完整 URL 不允许 `DecodedMode`。 |
| `QUrl(const QUrl &)` / `QUrl(QUrl &&)` | 复制或移动值 | 隐式共享值类型，无 QObject 生命周期。 |
| `operator=(const QUrl &)` / `operator=(QUrl &&)` | 赋值 URL | 只改变本对象的值。 |
| `operator=(const QString &)` | 解析并赋值字符串 | 定义 `QT_NO_URL_CAST_FROM_STRING` 后不可用。 |
| `clear()` | 清空 URL | 用于放弃无效或旧状态。 |
| `isEmpty()` | 判断是否为空 | 不等于 `isValid()`。 |
| `isValid()` | 判断 URL 语法/编码是否有效 | 不验证可达性、权限或可信度。 |
| `errorString()` | 返回最近的解析错误说明 | 在 `isValid()==false` 后用于诊断。 |
| `setUrl(const QString &, ParsingMode)` | 解析并整体替换 URL | `StrictMode` 适合协议输入；不支持 `DecodedMode`。 |
| `fromEncoded(QByteArrayView, ParsingMode)` | 从已编码字节构造 | 用于 wire-format URL；不要预先全量 decode。 |
| `fromStringList(QStringList, ParsingMode)` | 批量解析字符串 | 每一项按同一模式转换。 |
| `fromUserInput(input, workingDirectory, options)` | 猜测用户输入的 URL/文件 | 仅用于人机输入；不是安全解析器。 |
| `DefaultResolution` | 默认用户输入解析策略 | 按 Qt 启发式识别 URL 或本地文件。 |
| `AssumeLocalFile` | 用户输入优先按本地文件解释 | 处理歧义地址栏输入时使用。 |
| `TolerantMode` | 宽松解析 | 修正部分错误；不可作为严格验证。 |
| `StrictMode` | 严格解析 | 非法 `%` 编码或未编码禁用字符会使 URL 无效。 |
| `DecodedMode` | 接收已解码的组件数据 | `%` 是字面数据；只用于支持它的组件 setter。 |
| `scheme()` / `setScheme()` | 读取/设置 scheme | 空 scheme 即相对 URL。 |
| `authority()` / `setAuthority()` | 读取/设置 userinfo、host、port | 是复合字段；不允许 fully decoded 结果/输入模式。 |
| `userInfo()` / `setUserInfo()` | 读取/设置 username 与 password | `FullyDecoded` / `DecodedMode` 不允许；需要时分别处理两项。 |
| `userName()` / `setUserName()` | 读取/设置用户名 | 默认可完全解码；适合从非 URL 表单字段设置。 |
| `password()` / `setPassword()` | 读取/设置密码 | 不要用 `toString()` 写日志；显示接口会移除密码。 |
| `host()` / `setHost()` | 读取/设置 host | 做 allowlist 时比较此结构化值，不要解析 display string。 |
| `port(defaultPort)` / `setPort(int)` | 读取/设置端口 | 未显式端口返回 `defaultPort`；`-1` 清除显式端口。 |
| `path()` / `setPath()` | 读取/设置 URL path | `FullyDecoded` 结果不应直接重新拼 URL。 |
| `fileName()` | 返回 path 最后一个段 | 不访问文件系统，也不检查文件存在。 |
| `hasQuery()` / `query()` | 判断/读取整体 query | 区分缺失与空 query；键值操作见 `QUrlQuery`。 |
| `setQuery(const QString &, ParsingMode)` | 设置整体 query 文本 | 仅适合已有 query URL 文本。 |
| `setQuery(const QUrlQuery &)` | 设置结构化 query | 日常添加/删除 query 项的推荐入口。 |
| `hasFragment()` / `fragment()` / `setFragment()` | 操作 fragment | fragment 不会发送到 HTTP 服务器。 |
| `isRelative()` | 判断 scheme 是否为空 | `file:foo` 不相对，即使其 path 看起来相对。 |
| `resolved(const QUrl &)` | 基于当前 URL 解析相对 URL | 参数带 scheme 时 base 不参与合并；注意 base 尾部 `/`。 |
| `isParentOf(const QUrl &)` | 判断 URL 层级父子关系 | 适合导航，不可替代文件系统授权检查。 |
| `isLocalFile()` | 判断是否为 `file` URL | 不检查存在性、权限或目录边界。 |
| `fromLocalFile(const QString &)` | 从本地路径生成 file URL | 参数是路径不是 URL；相对路径产物已有 `file:` scheme。 |
| `toLocalFile()` | 将 file URL 转成本地路径 | 非 file URL 返回空；使用正斜杠，UNC host 会保留。 |
| `adjusted(FormattingOptions)` | 返回格式调整后的副本 | 不修改原对象；可移除 query/fragment、规范点段等。 |
| `matches(const QUrl &, FormattingOptions)` | 在指定调整选项下比较 URL | 可忽略组件；不是同源或权限安全检查。 |
| `toString(FormattingOptions)` / `url()` | 输出字符串形式 | `url()` 是同义 API；不允许 `FullyDecoded`。 |
| `toDisplayString(FormattingOptions)` | 输出面向人的地址 | 总是移除 password；其余敏感组件仍需业务脱敏。 |
| `toEncoded(FormattingOptions)` | 输出编码 URL 字节 | 默认 `FullyEncoded`；无效 URL 返回空字节数组。 |
| `PrettyDecoded` | 可读且无歧义的默认组件格式 | 不等同于完全解码。 |
| `FullyEncoded` | 完整 URI 编码格式 | 适合传输与稳定序列化。 |
| `FullyDecoded` | 完整解码单一组件 | 仅给非 URL 业务文本；会破坏完整 URL 的可判定性。 |
| `ComponentFormattingOption(s)` | 指定单个 URL 组件的输出编码 | 用于 `host()`、`path()` 等组件 getter；部分复合 getter 禁止 `FullyDecoded`。 |
| `UrlFormattingOption` / `FormattingOptions` | 指定完整 URL 的调整和输出规则 | 可与组件格式位组合，用于 `toString()`、`adjusted()`、`matches()` 等。 |
| `EncodeSpaces` / `EncodeUnicode` | 强制编码空格/Unicode | 用于精细控制组件输出。 |
| `EncodeDelimiters` / `EncodeReserved` | 强制编码分隔符/保留字符 | 保持数据不被误解为 URL 结构。 |
| `DecodeReserved` | 解码保留字符 | 仅在确认不会造成组件歧义时使用。 |
| `None` | 不应用 URL 删除类格式选项 | 可与组件格式选项组合。 |
| `RemoveScheme` / `RemoveAuthority` / `RemovePath` | 输出时移除对应结构 | 只影响返回表示或 `adjusted()` 副本。 |
| `RemovePassword` / `RemoveUserInfo` / `RemovePort` | 输出时移除敏感/连接信息 | `toDisplayString()` 总是启用 `RemovePassword`。 |
| `RemoveQuery` / `RemoveFragment` | 输出时移除 query/fragment | 常用于比较或缓存键；注意语义可能改变。 |
| `PreferLocalFile` | 格式化时优先本地文件路径 | 仅在适合本机呈现时使用。 |
| `StripTrailingSlash` / `RemoveFilename` | 删除末尾 `/` 或最后一个 path 段 | 只处理 URL 结构，不访问文件系统。 |
| `NormalizePathSegments` | 规范化 `.` / `..` path 段 | 不解析符号链接，不能用于越权防护。 |
| `toPercentEncoding(input, exclude, include)` | 对任意文本做百分号编码 | 不是完整 URL 解析器；输入先转 UTF-8。 |
| `fromPercentEncoding(bytes)` | 解码百分号字节 | 仅用于确定的单独数据，不要提前 decode 完整 URL。 |
| `toAce(domain, options)` | Unicode 域名转 ACE/Punycode | Qt 6.3 起；参数必须是域名，不是完整 URL/IPv6 literal。 |
| `fromAce(domain, options)` | ACE/Punycode 域名转 Unicode | Qt 6.3 起；显示/比较时注意 IDN 安全边界。 |
| `IgnoreIDNWhitelist` | 忽略 Qt IDN 白名单策略 | 仅在明确知道转换策略后使用。 |
| `AceTransitionalProcessing` | 启用 transitional IDNA 处理 | 仅用于需要兼容该 IDNA 策略的协议场景。 |
| `AceProcessingOption(s)` | 控制 ACE/IDN 转换策略 | 仅用于 `toAce()` / `fromAce()`；Qt 6.3 起可用。 |
| `UserInputResolutionOption(s)` | 控制 `fromUserInput()` 的歧义处理 | 当前公开选项为默认策略和 `AssumeLocalFile`。 |
| `idnWhitelist()` / `setIdnWhitelist()` | 获取/设置 IDN 白名单 | 进程级策略；应在初始化阶段集中设置。 |
| `toStringList(QList<QUrl>, options)` | 批量格式化 URL | 每项等价于使用 `toString(options)`。 |
| `detach()` / `isDetached()` | 管理/检查隐式共享数据 | 低层性能接口，正常值语义代码通常不需要。 |
| `swap(QUrl &)` | 常数时间交换两个 URL | 不解析、不访问网络。 |
| `qHash(const QUrl &, seed)` | 生成哈希值 | 用于 `QHash`、`QSet`。 |
| `operator==` / `operator!=` | 比较 URL 等价性 | 需要忽略组件时用 `matches()`。 |
| `operator<<(QDataStream &, const QUrl &)` | 写入二进制流 | 双方应约定 `QDataStream` 版本。 |
| `operator>>(QDataStream &, QUrl &)` | 从二进制流读取 URL | 不把 Qt 私有流格式当公开互操作协议。 |
| `fromCFURL()` / `toCFURL()` | 与 Core Foundation URL 转换 | 仅 Darwin；`toCFURL()` 返回值由调用方释放。 |
| `fromNSURL()` / `toNSURL()` | 与 Objective-C `NSURL` 转换 | 仅 Darwin；`toNSURL()` 返回 autoreleased 对象。 |
| `QT_NO_URL_CAST_FROM_STRING` | 禁用 `QString` 到 `QUrl` 自动转换 | 推荐用于迁移路径/URL 混用严重的项目。 |

---

### 一句话总结

`QUrl` 管的是 URL 结构和编码，不管网络可信度或文件权限：已知协议文本用严格解析，用户输入才用启发式解析；传输用 `toEncoded()`，显示用 `toDisplayString()`，本地路径用 `fromLocalFile()`，相对地址用 `resolved()`。
