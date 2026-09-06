# QHttpHeaders

> Qt 6.11.1 · Qt Network

## 1. 先建立直觉

**一句话定位：** `QHttpHeaders` 是 Qt Network 的“HttpHeaders”类型，负责描述请求/地址/连接状态或承载异步网络数据。

**模块背景：** Qt Network 提供 TCP/UDP、HTTP、代理、DNS、SSL 和网络请求等异步网络能力。

### 这是什么

`QHttpHeaders` 是 异步网络机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 网络请求通常由管理器创建并调度，返回一个代表本次操作的 reply。连接建立、DNS、发送、接收和错误都是事件驱动的阶段；响应头、状态码、body 和传输错误分别表达不同层次的信息。

**适用场景：** 创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要把异步请求当同步函数；不要只检查 `error()` 而忽略 HTTP 状态码；不要在 readyRead 中假设一次就收到完整 body；不要在 GUI 线程用阻塞等待替代信号。

## 2. 依赖与对象关系

- 头文件：`#include <QHttpHeaders>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Network)
target_link_libraries(mytarget PRIVATE Qt6::Network)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

网络请求通常由管理器创建并调度，返回一个代表本次操作的 reply。连接建立、DNS、发送、接收和错误都是事件驱动的阶段；响应头、状态码、body 和传输错误分别表达不同层次的信息。

### 状态、生命周期和线程

**生命周期：** manager 必须在线程事件循环中存活到 reply 完成；reply 完成后读取结果并调用 `deleteLater()`，不能在信号触发前直接释放。请求对象是值类型，reply 才是带有异步状态和资源的对象。

**状态与结果：** 请求成功发出不等于 HTTP 成功，HTTP 状态码成功也不等于业务 JSON 有效。至少分别处理网络错误、HTTP 状态码、响应头、响应体解析和业务字段校验。上传/下载还要处理进度、分段读取和取消。

**线程与事件循环：** QNetworkAccessManager、QNetworkReply 和相关请求应在同一个有事件循环的线程使用。跨线程时把网络对象整体放到目标线程，通过信号传递结果，不要跨线程直接读写 reply。

## 3. 直接使用

创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum class WellKnownHeader { AIM, Accept, AcceptAdditions, AcceptCH, AcceptDatetime, …, ProtocolQuery }`

### 公有函数

- `QHttpHeaders()`
- `QHttpHeaders(const QHttpHeaders &other)`
- `QHttpHeaders(QHttpHeaders &&other)`
- `~QHttpHeaders()`
- `bool append(QAnyStringView name, QAnyStringView value)`
- `bool append(QHttpHeaders::WellKnownHeader name, QAnyStringView value)`
- `void clear()`
- `QByteArray combinedValue(QAnyStringView name) const`
- `QByteArray combinedValue(QHttpHeaders::WellKnownHeader name) const`
- `bool contains(QAnyStringView name) const`
- `bool contains(QHttpHeaders::WellKnownHeader name) const`
- `(since 6.10) std::optional<QDateTime> dateTimeValue(QAnyStringView name) const`
- `(since 6.10) std::optional<QDateTime> dateTimeValue(QHttpHeaders::WellKnownHeader name) const`
- `(since 6.10) std::optional<QDateTime> dateTimeValueAt(qsizetype i) const`
- `(since 6.10) std::optional<QList<QDateTime>> dateTimeValues(QAnyStringView name) const`
- `(since 6.10) std::optional<QList<QDateTime>> dateTimeValues(QHttpHeaders::WellKnownHeader name) const`
- `bool insert(qsizetype i, QAnyStringView name, QAnyStringView value)`
- `bool insert(qsizetype i, QHttpHeaders::WellKnownHeader name, QAnyStringView value)`
- `(since 6.10) std::optional<qint64> intValue(QAnyStringView name) const`
- `(since 6.10) std::optional<qint64> intValue(QHttpHeaders::WellKnownHeader name) const`
- `(since 6.10) std::optional<qint64> intValueAt(qsizetype i) const`
- `(since 6.10) std::optional<QList<qint64>> intValues(QAnyStringView name) const`
- `(since 6.10) std::optional<QList<qint64>> intValues(QHttpHeaders::WellKnownHeader name) const`
- `bool isEmpty() const`
- `QLatin1StringView nameAt(qsizetype i) const`
- `void removeAll(QAnyStringView name)`
- `void removeAll(QHttpHeaders::WellKnownHeader name)`
- `void removeAt(qsizetype i)`
- `bool replace(qsizetype i, QAnyStringView name, QAnyStringView newValue)`
- `bool replace(qsizetype i, QHttpHeaders::WellKnownHeader name, QAnyStringView newValue)`
- `(since 6.8) bool replaceOrAppend(QHttpHeaders::WellKnownHeader name, QAnyStringView newValue)`
- `bool replaceOrAppend(QAnyStringView name, QAnyStringView newValue)`
- `void reserve(qsizetype size)`
- `(since 6.10) void setDateTimeValue(QAnyStringView name, const QDateTime &dateTime)`
- `(since 6.10) void setDateTimeValue(QHttpHeaders::WellKnownHeader name, const QDateTime &dateTime)`
- `qsizetype size() const`
- `void swap(QHttpHeaders &other)`
- `QList<std::pair<QByteArray, QByteArray>> toListOfPairs() const`
- `QMultiHash<QByteArray, QByteArray> toMultiHash() const`
- `QMultiMap<QByteArray, QByteArray> toMultiMap() const`
- `QByteArrayView value(QAnyStringView name, QByteArrayView defaultValue = {}) const`
- `QByteArrayView value(QHttpHeaders::WellKnownHeader name, QByteArrayView defaultValue = {}) const`
- `QByteArrayView valueAt(qsizetype i) const`
- `QList<QByteArray> values(QAnyStringView name) const`
- `QList<QByteArray> values(QHttpHeaders::WellKnownHeader name) const`
- `QHttpHeaders & operator=(QHttpHeaders &&other)`
- `QHttpHeaders & operator=(const QHttpHeaders &other)`

### 静态公有成员

- `QHttpHeaders fromListOfPairs(const QList<std::pair<QByteArray, QByteArray>> &headers)`
- `QHttpHeaders fromMultiHash(const QMultiHash<QByteArray, QByteArray> &headers)`
- `QHttpHeaders fromMultiMap(const QMultiMap<QByteArray, QByteArray> &headers)`
- `QByteArrayView wellKnownHeaderName(QHttpHeaders::WellKnownHeader name)`

### 相关非成员函数

- `QDebug operator<<(QDebug debug, const QHttpHeaders &headers)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum class QHttpHeaders::WellKnownHeader`

**作用与语义：**

根据IANA注册库，一些知名头部列表。
- `QHttpHeaders::WellKnownHeader::AIM`：`0`
- `QHttpHeaders::WellKnownHeader::Accept`：`1`
- `QHttpHeaders::WellKnownHeader::AcceptAdditions`：`2`
- `QHttpHeaders::WellKnownHeader::AcceptCH`：`3`
- `QHttpHeaders::WellKnownHeader::AcceptDatetime`：`4`
- `QHttpHeaders::WellKnownHeader::AcceptEncoding`：`5`
- `QHttpHeaders::WellKnownHeader::AcceptFeatures`：`6`
- `QHttpHeaders::WellKnownHeader::AcceptLanguage`：`7`
- `QHttpHeaders::WellKnownHeader::AcceptPatch`：`8`
- `QHttpHeaders::WellKnownHeader::AcceptPost`：`9`
- `QHttpHeaders::WellKnownHeader::AcceptRanges`：`10`
- `QHttpHeaders::WellKnownHeader::AcceptSignature`：`11`
- `QHttpHeaders::WellKnownHeader::AccessControlAllowCredentials`：`12`
- `QHttpHeaders::WellKnownHeader::AccessControlAllowHeaders`：`13`
- `QHttpHeaders::WellKnownHeader::AccessControlAllowMethods`：`14`
- `QHttpHeaders::WellKnownHeader::AccessControlAllowOrigin`：`15`
- `QHttpHeaders::WellKnownHeader::AccessControlExposeHeaders`：`16`
- `QHttpHeaders::WellKnownHeader::AccessControlMaxAge`：`17`
- `QHttpHeaders::WellKnownHeader::AccessControlRequestHeaders`：`18`
- `QHttpHeaders::WellKnownHeader::AccessControlRequestMethod`：`19`
- `QHttpHeaders::WellKnownHeader::Age`：`20`
- `QHttpHeaders::WellKnownHeader::Allow`：`21`
- `QHttpHeaders::WellKnownHeader::ALPN`：`22`
- `QHttpHeaders::WellKnownHeader::AltSvc`：`23`
- `QHttpHeaders::WellKnownHeader::AltUsed`：`24`
- `QHttpHeaders::WellKnownHeader::Alternates`：`25`
- `QHttpHeaders::WellKnownHeader::ApplyToRedirectRef`：`26`
- `QHttpHeaders::WellKnownHeader::AuthenticationControl`：`27`
- `QHttpHeaders::WellKnownHeader::AuthenticationInfo`：`28`
- `QHttpHeaders::WellKnownHeader::Authorization`：`29`
- `QHttpHeaders::WellKnownHeader::CacheControl`：`30`
- `QHttpHeaders::WellKnownHeader::CacheStatus`：`31`
- `QHttpHeaders::WellKnownHeader::CalManagedID`：`32`
- `QHttpHeaders::WellKnownHeader::CalDAVTimezones`：`33`
- `QHttpHeaders::WellKnownHeader::CapsuleProtocol`：`34`
- `QHttpHeaders::WellKnownHeader::CDNCacheControl`：`35`
- `QHttpHeaders::WellKnownHeader::CDNLoop`：`36`
- `QHttpHeaders::WellKnownHeader::CertNotAfter`：`37`
- `QHttpHeaders::WellKnownHeader::CertNotBefore`：`38`
- `QHttpHeaders::WellKnownHeader::ClearSiteData`：`39`
- `QHttpHeaders::WellKnownHeader::ClientCert`：`40`
- `QHttpHeaders::WellKnownHeader::ClientCertChain`：`41`
- `QHttpHeaders::WellKnownHeader::Close`：`42`
- `QHttpHeaders::WellKnownHeader::Connection`：`43`
- `QHttpHeaders::WellKnownHeader::ContentDigest`：`44`
- `QHttpHeaders::WellKnownHeader::ContentDisposition`：`45`
- `QHttpHeaders::WellKnownHeader::ContentEncoding`：`46`
- `QHttpHeaders::WellKnownHeader::ContentID`：`47`
- `QHttpHeaders::WellKnownHeader::ContentLanguage`：`48`
- `QHttpHeaders::WellKnownHeader::ContentLength`：`49`
- `QHttpHeaders::WellKnownHeader::ContentLocation`：`50`
- `QHttpHeaders::WellKnownHeader::ContentRange`：`51`
- `QHttpHeaders::WellKnownHeader::ContentSecurityPolicy`：`52`
- `QHttpHeaders::WellKnownHeader::ContentSecurityPolicyReportOnly`：`53`
- `QHttpHeaders::WellKnownHeader::ContentType`：`54`
- `QHttpHeaders::WellKnownHeader::Cookie`：`55`
- `QHttpHeaders::WellKnownHeader::CrossOriginEmbedderPolicy`：`56`
- `QHttpHeaders::WellKnownHeader::CrossOriginEmbedderPolicyReportOnly`：`57`
- `QHttpHeaders::WellKnownHeader::CrossOriginOpenerPolicy`：`58`
- `QHttpHeaders::WellKnownHeader::CrossOriginOpenerPolicyReportOnly`：`59`
- `QHttpHeaders::WellKnownHeader::CrossOriginResourcePolicy`：`60`
- `QHttpHeaders::WellKnownHeader::DASL`：`61`
- `QHttpHeaders::WellKnownHeader::Date`：`62`
- `QHttpHeaders::WellKnownHeader::DAV`：`63`
- `QHttpHeaders::WellKnownHeader::DeltaBase`：`64`
- `QHttpHeaders::WellKnownHeader::Depth`：`65`
- `QHttpHeaders::WellKnownHeader::Destination`：`66`
- `QHttpHeaders::WellKnownHeader::DifferentialID`：`67`
- `QHttpHeaders::WellKnownHeader::DPoP`：`68`
- `QHttpHeaders::WellKnownHeader::DPoPNonce`：`69`
- `QHttpHeaders::WellKnownHeader::EarlyData`：`70`
- `QHttpHeaders::WellKnownHeader::ETag`：`71`
- `QHttpHeaders::WellKnownHeader::Expect`：`72`
- `QHttpHeaders::WellKnownHeader::ExpectCT`：`73`
- `QHttpHeaders::WellKnownHeader::Expires`：`74`
- `QHttpHeaders::WellKnownHeader::Forwarded`：`75`
- `QHttpHeaders::WellKnownHeader::From`：`76`
- `QHttpHeaders::WellKnownHeader::Hobareg`：`77`
- `QHttpHeaders::WellKnownHeader::Host`：`78`
- `QHttpHeaders::WellKnownHeader::If`：`79`
- `QHttpHeaders::WellKnownHeader::IfMatch`：`80`
- `QHttpHeaders::WellKnownHeader::IfModifiedSince`：`81`
- `QHttpHeaders::WellKnownHeader::IfNoneMatch`：`82`
- `QHttpHeaders::WellKnownHeader::IfRange`：`83`
- `QHttpHeaders::WellKnownHeader::IfScheduleTagMatch`：`84`
- `QHttpHeaders::WellKnownHeader::IfUnmodifiedSince`：`85`
- `QHttpHeaders::WellKnownHeader::IM`：`86`
- `QHttpHeaders::WellKnownHeader::IncludeReferredTokenBindingID`：`87`
- `QHttpHeaders::WellKnownHeader::KeepAlive`：`88`
- `QHttpHeaders::WellKnownHeader::Label`：`89`
- `QHttpHeaders::WellKnownHeader::LastEventID`：`90`
- `QHttpHeaders::WellKnownHeader::LastModified`：`91`
- `QHttpHeaders::WellKnownHeader::Link`：`92`
- `QHttpHeaders::WellKnownHeader::Location`：`93`
- `QHttpHeaders::WellKnownHeader::LockToken`：`94`
- `QHttpHeaders::WellKnownHeader::MaxForwards`：`95`
- `QHttpHeaders::WellKnownHeader::MementoDatetime`：`96`
- `QHttpHeaders::WellKnownHeader::Meter`：`97`
- `QHttpHeaders::WellKnownHeader::MIMEVersion`：`98`
- `QHttpHeaders::WellKnownHeader::Negotiate`：`99`
- `QHttpHeaders::WellKnownHeader::NEL`：`100`
- `QHttpHeaders::WellKnownHeader::ODataEntityId`：`101`
- `QHttpHeaders::WellKnownHeader::ODataIsolation`：`102`
- `QHttpHeaders::WellKnownHeader::ODataMaxVersion`：`103`
- `QHttpHeaders::WellKnownHeader::ODataVersion`：`104`
- `QHttpHeaders::WellKnownHeader::OptionalWWWAuthenticate`：`105`
- `QHttpHeaders::WellKnownHeader::OrderingType`：`106`
- `QHttpHeaders::WellKnownHeader::Origin`：`107`
- `QHttpHeaders::WellKnownHeader::OriginAgentCluster`：`108`
- `QHttpHeaders::WellKnownHeader::OSCORE`：`109`
- `QHttpHeaders::WellKnownHeader::OSLCCoreVersion`：`110`
- `QHttpHeaders::WellKnownHeader::Overwrite`：`111`
- `QHttpHeaders::WellKnownHeader::PingFrom`：`112`
- `QHttpHeaders::WellKnownHeader::PingTo`：`113`
- `QHttpHeaders::WellKnownHeader::Position`：`114`
- `QHttpHeaders::WellKnownHeader::Prefer`：`115`
- `QHttpHeaders::WellKnownHeader::PreferenceApplied`：`116`
- `QHttpHeaders::WellKnownHeader::Priority`：`117`
- `QHttpHeaders::WellKnownHeader::ProxyAuthenticate`：`118`
- `QHttpHeaders::WellKnownHeader::ProxyAuthenticationInfo`：`119`
- `QHttpHeaders::WellKnownHeader::ProxyAuthorization`：`120`
- `QHttpHeaders::WellKnownHeader::ProxyStatus`：`121`
- `QHttpHeaders::WellKnownHeader::PublicKeyPins`：`122`
- `QHttpHeaders::WellKnownHeader::PublicKeyPinsReportOnly`：`123`
- `QHttpHeaders::WellKnownHeader::Range`：`124`
- `QHttpHeaders::WellKnownHeader::RedirectRef`：`125`
- `QHttpHeaders::WellKnownHeader::Referer`：`126`
- `QHttpHeaders::WellKnownHeader::Refresh`：`127`
- `QHttpHeaders::WellKnownHeader::ReplayNonce`：`128`
- `QHttpHeaders::WellKnownHeader::ReprDigest`：`129`
- `QHttpHeaders::WellKnownHeader::RetryAfter`：`130`
- `QHttpHeaders::WellKnownHeader::ScheduleReply`：`131`
- `QHttpHeaders::WellKnownHeader::ScheduleTag`：`132`
- `QHttpHeaders::WellKnownHeader::SecPurpose`：`133`
- `QHttpHeaders::WellKnownHeader::SecTokenBinding`：`134`
- `QHttpHeaders::WellKnownHeader::SecWebSocketAccept`：`135`
- `QHttpHeaders::WellKnownHeader::SecWebSocketExtensions`：`136`
- `QHttpHeaders::WellKnownHeader::SecWebSocketKey`：`137`
- `QHttpHeaders::WellKnownHeader::SecWebSocketProtocol`：`138`
- `QHttpHeaders::WellKnownHeader::SecWebSocketVersion`：`139`
- `QHttpHeaders::WellKnownHeader::Server`：`140`
- `QHttpHeaders::WellKnownHeader::ServerTiming`：`141`
- `QHttpHeaders::WellKnownHeader::SetCookie`：`142`
- `QHttpHeaders::WellKnownHeader::Signature`：`143`
- `QHttpHeaders::WellKnownHeader::SignatureInput`：`144`
- `QHttpHeaders::WellKnownHeader::SLUG`：`145`
- `QHttpHeaders::WellKnownHeader::SoapAction`：`146`
- `QHttpHeaders::WellKnownHeader::StatusURI`：`147`
- `QHttpHeaders::WellKnownHeader::StrictTransportSecurity`：`148`
- `QHttpHeaders::WellKnownHeader::Sunset`：`149`
- `QHttpHeaders::WellKnownHeader::SurrogateCapability`：`150`
- `QHttpHeaders::WellKnownHeader::SurrogateControl`：`151`
- `QHttpHeaders::WellKnownHeader::TCN`：`152`
- `QHttpHeaders::WellKnownHeader::TE`：`153`
- `QHttpHeaders::WellKnownHeader::Timeout`：`154`
- `QHttpHeaders::WellKnownHeader::Topic`：`155`
- `QHttpHeaders::WellKnownHeader::Traceparent`：`156`
- `QHttpHeaders::WellKnownHeader::Tracestate`：`157`
- `QHttpHeaders::WellKnownHeader::Trailer`：`158`
- `QHttpHeaders::WellKnownHeader::TransferEncoding`：`159`
- `QHttpHeaders::WellKnownHeader::TTL`：`160`
- `QHttpHeaders::WellKnownHeader::Upgrade`：`161`
- `QHttpHeaders::WellKnownHeader::Urgency`：`162`
- `QHttpHeaders::WellKnownHeader::UserAgent`：`163`
- `QHttpHeaders::WellKnownHeader::VariantVary`：`164`
- `QHttpHeaders::WellKnownHeader::Vary`：`165`
- `QHttpHeaders::WellKnownHeader::Via`：`166`
- `QHttpHeaders::WellKnownHeader::WantContentDigest`：`167`
- `QHttpHeaders::WellKnownHeader::WantReprDigest`：`168`
- `QHttpHeaders::WellKnownHeader::WWWAuthenticate`：`169`
- `QHttpHeaders::WellKnownHeader::XContentTypeOptions`：`170`
- `QHttpHeaders::WellKnownHeader::XFrameOptions`：`171`
- `QHttpHeaders::WellKnownHeader::AcceptCharset`：`172`
- `QHttpHeaders::WellKnownHeader::CPEPInfo`：`173`
- `QHttpHeaders::WellKnownHeader::Pragma`：`174`
- `QHttpHeaders::WellKnownHeader::ProtocolInfo`：`175`
- `QHttpHeaders::WellKnownHeader::ProtocolQuery`：`176`

### `[noexcept] QHttpHeaders::QHttpHeaders()`

**作用与语义：**

创建一个新的 QHttpHeaders 对象。

### `QHttpHeaders::QHttpHeaders(const QHttpHeaders &other)`

**作用与语义：**

创建`other`副本。

### `[constexpr noexcept] QHttpHeaders::QHttpHeaders(QHttpHeaders &&other)`

**作用与语义：**

从`other`中构造该对象，`empty`保持不变。

### `[noexcept] QHttpHeaders::~QHttpHeaders()`

**作用与语义：**

丢弃了头部对象。

### `bool QHttpHeaders::append(QAnyStringView name, QAnyStringView value)`

**作用与语义：**

在头部条目中附加 `name` 和 `value`，成功时返回 `true`。

### `bool QHttpHeaders::append(QHttpHeaders::WellKnownHeader name, QAnyStringView value)`

**作用与语义：**

注意：该函数会超载`QHttpHeaders::append`（QAnyStringView， QAnyStringView）。

### `void QHttpHeaders::clear()`

**作用与语义：**

清除所有头条目。

### `QByteArray QHttpHeaders::combinedValue(QAnyStringView name) const`

**作用与语义：**

返回逗号合并字符串中`name`的首部值。如果没有带有`name`的首部，返回`null` `QByteArray`。
注意：通过这种方式访问“Set-Cookie”头部的值可能无法按预期工作。这是HTTP RFC中的一个显著例外，其值不能以这种方式组合。建议选择`values()`。

### `QByteArray QHttpHeaders::combinedValue(QHttpHeaders::WellKnownHeader name) const`

**作用与语义：**

注意：该函数会超载 `QHttpHeaders::combinedValue`（QAnyStringView）。

### `bool QHttpHeaders::contains(QAnyStringView name) const`

**作用与语义：**

返回头部是否包含带有`name`的头部。

### `bool QHttpHeaders::contains(QHttpHeaders::WellKnownHeader name) const`

**作用与语义：**

注意：该函数会超载 QHttpHeaders：：has（QAnyStringView）。

### `[since 6.10] std::optional<QDateTime> QHttpHeaders::dateTimeValue(QAnyStringView name) const`

**作用与语义：**

将`name`的第一个找到的头值转换为`QDateTime`对象，遵循标准HTTP日期格式。如果头部不存在或包含无效`QDateTime`，返回`std::nullopt`。

### `[since 6.10] std::optional<QDateTime> QHttpHeaders::dateTimeValue(QHttpHeaders::WellKnownHeader name) const`

**作用与语义：**

注意：该函数会超载 `QHttpHeaders::dateTimeValue`（QAnyStringView）。

### `[since 6.10] std::optional<QDateTime> QHttpHeaders::dateTimeValueAt(qsizetype i) const`

**作用与语义：**

将索引`i`的头值转换为符合标准HTTP日期格式的`QDateTime`对象。索引`i`必须有效。

### `[since 6.10] std::optional<QList<QDateTime>> QHttpHeaders::dateTimeValues(QAnyStringView name) const`

**作用与语义：**

返回 `name` 的所有头部值，包含一个包含 `QDateTime` 对象的列表，遵循标准的 HTTP 日期格式。如果找不到有效的日期-时间值，返回 `std::nullopt`。

### `[since 6.10] std::optional<QList<QDateTime>> QHttpHeaders::dateTimeValues(QHttpHeaders::WellKnownHeader name) const`

**作用与语义：**

注意：该函数会超载 `QHttpHeaders::dateTimeValues`（QAnyStringView）。

### `[static] QHttpHeaders QHttpHeaders::fromListOfPairs(const QList<std::pair<QByteArray, QByteArray>> &headers)`

**作用与语义：**

创建一个新的`QHttpHeaders`对象，填充`headers`。

### `[static] QHttpHeaders QHttpHeaders::fromMultiHash(const QMultiHash<QByteArray, QByteArray> &headers)`

**作用与语义：**

创建一个新的`QHttpHeaders`对象，填充`headers`。

### `[static] QHttpHeaders QHttpHeaders::fromMultiMap(const QMultiMap<QByteArray, QByteArray> &headers)`

**作用与语义：**

创建一个新的`QHttpHeaders`对象，填充`headers`。

### `bool QHttpHeaders::insert(qsizetype i, QAnyStringView name, QAnyStringView value)`

**作用与语义：**

在索引`i`插入一个头部条目，`name`和`value`。索引必须有效（参见`size()`）。返回插入是否成功。

### `bool QHttpHeaders::insert(qsizetype i, QHttpHeaders::WellKnownHeader name, QAnyStringView value)`

**作用与语义：**

注意：该函数会超载 `QHttpHeaders::insert`（qsizetype， QAnyStringView， QAnyStringView）。

### `[noexcept, since 6.10] std::optional<qint64> QHttpHeaders::intValue(QAnyStringView name) const`

**作用与语义：**

返回第一个有效头部的值，`name`解释为64位整数。如果头部不存在或无法解析为整数，返回`std::nullopt`。

### `[noexcept, since 6.10] std::optional<qint64> QHttpHeaders::intValue(QHttpHeaders::WellKnownHeader name) const`

**作用与语义：**

注意：该函数会超载 `QHttpHeaders::intValue`（QAnyStringView）。

### `[noexcept, since 6.10] std::optional<qint64> QHttpHeaders::intValueAt(qsizetype i) const`

**作用与语义：**

返回索引`i`处解释为64位整数的头部值。索引`i`必须有效。

### `[since 6.10] std::optional<QList<qint64>> QHttpHeaders::intValues(QAnyStringView name) const`

**作用与语义：**

返回在列表中`name`解释为64位整数的头部值。如果头部不存在或无法作为整数解析，则返回`std::nullopt`。

### `[since 6.10] std::optional<QList<qint64>> QHttpHeaders::intValues(QHttpHeaders::WellKnownHeader name) const`

**作用与语义：**

注意：该函数会超载 `QHttpHeaders::intValues`（QAnyStringView）。

### `[noexcept] bool QHttpHeaders::isEmpty() const`

**作用与语义：**

如果头部大小为0，返回`true`;否则返回`false`。

### `[noexcept] QLatin1StringView QHttpHeaders::nameAt(qsizetype i) const`

**作用与语义：**

返回索引`i`的头部名称。索引`i`必须有效（见`size()`）。
头部名称不区分大小写，返回的名称为小写。

### `void QHttpHeaders::removeAll(QAnyStringView name)`

**作用与语义：**

去除头部`name`。

### `void QHttpHeaders::removeAll(QHttpHeaders::WellKnownHeader name)`

**作用与语义：**

注意：该函数会超载 `QHttpHeaders::removeAll`（QAnyStringView）。

### `void QHttpHeaders::removeAt(qsizetype i)`

**作用与语义：**

移除索引`i`的头部。索引`i`必须有效（见 `size()`）。

### `bool QHttpHeaders::replace(qsizetype i, QAnyStringView name, QAnyStringView newValue)`

**作用与语义：**

将索引`i`的头部条目替换为`name`和`newValue`。索引必须有效（见 `size()`）。返回替换是否成功。

### `bool QHttpHeaders::replace(qsizetype i, QHttpHeaders::WellKnownHeader name, QAnyStringView newValue)`

**作用与语义：**

注意：该函数会超载 `QHttpHeaders::replace`（qsizetype， QAnyStringView， QAnyStringView）。

### `[since 6.8] bool QHttpHeaders::replaceOrAppend(QHttpHeaders::WellKnownHeader name, QAnyStringView newValue)`

**作用与语义：**

如果`QHttpHeaders`已经包含`name`，则用`newValue`替换其值，并移除可能的额外`name`条目。如果`name`不存在，则添加新条目。成功时返回`true`。
该函数是一种方便的方法，用于设置唯一`name` ： `newValue` 头部。对于大多数头部，相对顺序无关紧要，这使得如果已有条目存在，便于重复使用。

### `bool QHttpHeaders::replaceOrAppend(QAnyStringView name, QAnyStringView newValue)`

**作用与语义：**

注意：该函数会超载 QHttpHeaders：：replaceOrAppend（WellKnownHeader， QAnyStringView）。

### `void QHttpHeaders::reserve(qsizetype size)`

**作用与语义：**

尝试为至少`size`个头部条目分配内存。
如果你提前知道有多少个头部条目，可以调用该函数以防止重分配和内存碎片化。

### `[since 6.10] void QHttpHeaders::setDateTimeValue(QAnyStringView name, const QDateTime &dateTime)`

**作用与语义：**

将头部名称`name`设置为`dateTime`，遵循标准的HTTP IMF-fixdate格式。如果头部不存在，则添加一个新的头部。

### `[since 6.10] void QHttpHeaders::setDateTimeValue(QHttpHeaders::WellKnownHeader name, const QDateTime &dateTime)`

**作用与语义：**

注意：该函数会超载 QHttpHeaders：：setDateTimeValue（QAnyStringView）。

### `[noexcept] qsizetype QHttpHeaders::size() const`

**作用与语义：**

返回头部条目数量。

### `[noexcept] void QHttpHeaders::swap(QHttpHeaders &other)`

**作用与语义：**

将`QHttpHeaders`与`other`交换。此操作非常快速且从未失效。

### `QList<std::pair<QByteArray, QByteArray>> QHttpHeaders::toListOfPairs() const`

**作用与语义：**

返回头部条目，作为（名称、值）对的列表。头部名称不区分大小写，返回的名称为小写。

### `QMultiHash<QByteArray, QByteArray> QHttpHeaders::toMultiHash() const`

**作用与语义：**

返回头部条目，作为从名称到值的哈希值。头部名称不区分大小写，返回的名称为小写。

### `QMultiMap<QByteArray, QByteArray> QHttpHeaders::toMultiMap() const`

**作用与语义：**

返回头部条目，作为名称到值的映射。头部名称不区分大小写，返回的名称为小写。

### `[noexcept] QByteArrayView QHttpHeaders::value(QAnyStringView name, QByteArrayView defaultValue = {}) const`

**作用与语义：**

返回（第一个）头部的值，`name`，如果不存在则返回`defaultValue`。

### `[noexcept] QByteArrayView QHttpHeaders::value(QHttpHeaders::WellKnownHeader name, QByteArrayView defaultValue = {}) const`

**作用与语义：**

注意：该函数会超载 `QHttpHeaders::value`（QAnyStringView， QByteArrayView）。

### `[noexcept] QByteArrayView QHttpHeaders::valueAt(qsizetype i) const`

**作用与语义：**

返回索引`i`的头部值。索引`i`必须有效（见`size()`）。

### `QList<QByteArray> QHttpHeaders::values(QAnyStringView name) const`

**作用与语义：**

返回列表中`name`的首部值。如果没有带有`name`的头部，返回一个空列表。

### `QList<QByteArray> QHttpHeaders::values(QHttpHeaders::WellKnownHeader name) const`

**作用与语义：**

注意：该函数会超载 `QHttpHeaders::values`（QAnyStringView）。

### `[static noexcept] QByteArrayView QHttpHeaders::wellKnownHeaderName(QHttpHeaders::WellKnownHeader name)`

**作用与语义：**

返回与所提供`name`对应的视图的头部名称。

### `[noexcept] QHttpHeaders &QHttpHeaders::operator=(QHttpHeaders &&other)`

**作用与语义：**

Move-assign `other`并返回该对象的引用。
`other`会被留在`empty`。

### `QHttpHeaders &QHttpHeaders::operator=(const QHttpHeaders &other)`

**作用与语义：**

分配`other`的内容并返回该对象的引用。

### `QDebug operator<<(QDebug debug, const QHttpHeaders &headers)`

**作用与语义：**

把`headers`写入`debug`流。

## 6. 深入实践与常见坑

### 生命周期和资源边界

manager 必须在线程事件循环中存活到 reply 完成；reply 完成后读取结果并调用 `deleteLater()`，不能在信号触发前直接释放。请求对象是值类型，reply 才是带有异步状态和资源的对象。

### 状态和错误边界

请求成功发出不等于 HTTP 成功，HTTP 状态码成功也不等于业务 JSON 有效。至少分别处理网络错误、HTTP 状态码、响应头、响应体解析和业务字段校验。上传/下载还要处理进度、分段读取和取消。

### 线程边界

QNetworkAccessManager、QNetworkReply 和相关请求应在同一个有事件循环的线程使用。跨线程时把网络对象整体放到目标线程，通过信号传递结果，不要跨线程直接读写 reply。

### 最容易出现的错误

不要把异步请求当同步函数；不要只检查 `error()` 而忽略 HTTP 状态码；不要在 readyRead 中假设一次就收到完整 body；不要在 GUI 线程用阻塞等待替代信号。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QHttpHeaders` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
