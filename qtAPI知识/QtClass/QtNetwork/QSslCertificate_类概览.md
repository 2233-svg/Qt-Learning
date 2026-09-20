# QSslCertificate

> Qt 6.11.1 | Qt6::Network | `#include <QSslCertificate>`

## 类解决的问题

`QSslCertificate` 是 X.509 证书的 Qt 值类型包装。它把 PEM/DER 证书解析成可查询、可序列化、可参与证书链验证的对象，主要解决：

- 读取服务器、客户端或 CA 证书；
- 查询证书的主题、颁发者、序列号、有效期、SAN、公钥和扩展；
- 把证书重新导出为 PEM、DER 或可读文本；
- 从文件、设备、路径匹配结果中一次得到一张或多张证书；
- 使用 Qt 当前 SSL backend 验证证书链和主机名；
- 导入 PKCS#12 文件中的私钥、叶子证书和 CA 链。

它不是 TLS 连接，也不负责自动建立信任。证书对象只描述证书材料；真正建立连接时，还要交给 `QSslSocket` 或 `QSslConfiguration`，并由 backend 执行握手验证。

## 实际使用场景

### 1. 读取本地证书并配置服务端

```cpp
QFile certificateFile(QStringLiteral("server-chain.pem"));
if (!certificateFile.open(QIODevice::ReadOnly)) {
    return;
}

const QList<QSslCertificate> chain =
    QSslCertificate::fromDevice(&certificateFile, QSsl::Pem);
if (chain.isEmpty()) {
    return;
}

QSslConfiguration configuration =
    QSslConfiguration::defaultConfiguration();
configuration.setLocalCertificateChain(chain);
```

`fromDevice()` 会读取输入中的全部证书。服务端配置时通常把叶子证书放在列表第一项，后面依次放中间 CA。

### 2. 诊断主机名不匹配

```cpp
const QSslCertificate certificate = socket->peerCertificate();
const auto names = certificate.subjectAlternativeNames();

for (auto it = names.cbegin(); it != names.cend(); ++it) {
    qInfo() << it.key() << it.value();
}
```

主机名校验通常应依赖 Qt/backend 的验证结果；读取 SAN 适合做诊断、显示或排查证书部署问题。不能因为 Common Name 看起来正确，就跳过 SAN 和完整链验证。

### 3. 验证一条证书链

```cpp
const QList<QSslCertificate> chain = QSslCertificate::fromFile(
    QStringLiteral("peer-chain.pem"), QSsl::Pem);
const QList<QSslError> errors =
    QSslCertificate::verify(chain, QStringLiteral("api.example.com"));

for (const QSslError &error : errors) {
    qWarning() << error.error() << error.errorString();
}
```

验证结果由当前 Qt SSL backend、默认 CA 配置和传入主机名共同决定。离线验证和实际 socket 握手可能因为 backend、系统信任库或连接上下文不同而产生不同结果。

### 4. 从 PKCS#12 包中提取 TLS 材料

```cpp
QFile bundle(QStringLiteral("client.p12"));
if (!bundle.open(QIODevice::ReadOnly)) {
    return;
}

QSslKey privateKey;
QSslCertificate certificate;
QList<QSslCertificate> caCertificates;
if (!QSslCertificate::importPkcs12(&bundle, &privateKey, &certificate,
                                   &caCertificates,
                                   QByteArrayLiteral("password"))) {
    return;
}
```

`importPkcs12()` 输出的是私钥、叶子证书以及可选 CA 列表。输出参数必须指向可写对象；如果不需要 CA 链，可以传 `nullptr`。

## 构建与最小示例

```cmake
find_package(Qt6 REQUIRED COMPONENTS Network)
target_link_libraries(app PRIVATE Qt6::Network)
```

```cpp
#include <QFile>
#include <QSslCertificate>

const QList<QSslCertificate> certificates =
    QSslCertificate::fromFile(QStringLiteral("certificate.pem"));

for (const QSslCertificate &certificate : certificates) {
    if (!certificate.isNull()) {
        qInfo() << certificate.subjectDisplayName()
                << certificate.expiryDate();
    }
}
```

## 关键语义与边界

### null、invalid、blacklisted 不是同一个概念

默认构造或解析失败的对象是 null certificate，使用 `isNull()` 判断。证书内容存在但字段、签名或格式不符合要求时，可能是无效证书，具体问题通常要结合 `verify()` 或握手产生的 `QSslError` 判断。`isBlacklisted()` 则表示证书匹配 Qt/backend 的黑名单策略；它不是“对象为空”，也不是普通的链验证结果。

不要把 `!isNull()` 当成“证书可信”，也不要把 `isBlacklisted() == false` 当成“证书一定能用于当前主机”。

### 单对象构造只使用输入中的第一张证书

`QSslCertificate(QIODevice *)` 和 `QSslCertificate(QByteArray)` 面向单个对象。若输入包含多张 PEM/DER 证书，构造函数只使用第一张。需要取得全部证书时，使用 `fromDevice()` 或 `fromData()`，它们返回列表。

同理，`fromFile()` 适合读取一个普通文件中的全部证书，不会把路径当作通配符；需要路径匹配时使用 `fromPath()`。

### `fromFile()` 与 `fromPath()` 的职责不同

`fromFile()` 是 Qt 6.10 新增的普通文件读取 API。它只读取普通单文件；路径不存在、无法读取或不是普通文件时返回空列表。它不会递归目录，也不会展开通配符。

`fromPath()` 根据 `PatternSyntax` 解释路径：

- `FixedString`：把路径当作固定路径；
- `Wildcard`：使用通配符匹配；
- `RegularExpression`：使用正则表达式匹配。

匹配到多个文件时，返回列表的顺序不应被业务逻辑当成稳定排序；需要确定顺序时由应用自行排序或按证书属性排序。

### 证书链顺序和根 CA

传给 `verify()` 的链首必须是叶子证书，后面是它的中间证书。通常不需要把根 CA 放入列表；backend 会从默认 CA 配置或应用配置中寻找信任锚。把错误顺序的证书链传入验证函数，可能得到 `UnableToVerifyFirstCertificate` 等错误。

服务端发送的本地证书链也应遵循叶子证书在前、中间 CA 在后的顺序。根证书通常不应作为服务端发送链的一部分。

### `verify()` 不是“只检查签名”

`verify()` 可能检查证书链、有效期、用途、信任关系以及可选的主机名。传入 `hostName` 后，主机名匹配会成为验证的一部分。空主机名表示不执行这项主机名检查，但不代表关闭其他验证。

返回空列表通常表示没有发现错误；返回多个 `QSslError` 时应遍历全部错误。验证使用的 CA 和 backend 环境要与目标运行环境保持一致，不能只在开发机上验证一次后永久缓存结论。

### `subjectAlternativeNames()` 通常比 CN 更适合诊断主机名

现代 TLS 主机名验证主要依赖 Subject Alternative Name。`subjectAlternativeNames()` 返回按 `QSsl::AlternativeNameEntryType` 分类的多值映射，常见类型是 DNS 名称和 IP 地址。它可能为空，也可能包含多个名称。

应用若自行做主机名匹配，必须处理通配符规则、IDN、IP 地址与 DNS 名称的区别，并遵循目标安全策略。一般情况下应让 Qt/backend 执行验证，而不是用字符串包含关系替代它。

### 时间、序列号和指纹格式

- `effectiveDate()` 和 `expiryDate()` 返回证书声明的时间；null 或解析失败时可能返回无效的 `QDateTime`。
- `serialNumber()` 返回十六进制形式的序列号字符串，不要把它当作十进制整数。
- `digest()` 默认使用 `QCryptographicHash::Md5`。MD5 适合兼容旧系统或做非安全去重，不应作为现代安全身份指纹；需要指纹时显式选择 SHA-256 等更合适的算法。

### 主题和颁发者属性可能有多个值

`subjectInfo()`、`issuerInfo()` 返回 `QStringList`，同一属性可能出现多次。枚举版适合读取 Qt 已知的标准属性；字节数组版适合读取特定 OID/属性名。`subjectInfoAttributes()` 和 `issuerInfoAttributes()` 可以发现证书实际包含的属性，再决定读取方式。

`subjectDisplayName()` 和 `issuerDisplayName()` 是便于展示的摘要，不应作为唯一身份判断，也不保证在所有证书上都有非空结果。

### 公钥和扩展的可用性受 SSL 构建影响

`publicKey()` 只有启用 SSL 支持时才可用。`extensions()` 返回证书扩展值对象列表，未知扩展也可能以通用形式保留；不能假设每个扩展都能被 Qt 解释成专用结构。

证书对象是隐式共享值类型，不拥有外部 `QIODevice`；从设备解析完成后，设备仍由调用方管理。复制证书不会复制文件、socket 或 backend 会话。

### PKCS#12 的设备和输出参数要求

`importPkcs12()` 要求 `QIODevice` 已打开且可读，并从当前设备位置读取。设备由调用方拥有；函数不会替应用打开或关闭它。成功时写入 key、叶子证书和可选 CA 链，失败时不要把输出对象当成有效认证材料。

PKCS#12 口令属于敏感数据。不要把口令、私钥或完整密钥包写入日志；读取后还应检查返回的 key 和 certificate 是否为 null。

### native handle 不适合作为跨平台业务数据

`handle()` 返回平台/backend 相关的原生证书句柄，仅适合与明确匹配的底层 API 配合。返回的句柄不转移所有权，也不保证跨平台、跨 backend 或跨 Qt 小版本具有相同语义。普通 Qt 应用应优先使用证书的 Qt API。

## 常见误区

- 用 `isNull() == false` 推断证书可信：它只说明对象有证书数据。
- 用单对象构造读取证书链：构造函数只取第一张，应使用 `fromData()`、`fromDevice()` 或 `fromFile()`。
- 把 `fromFile()` 当作通配符 API：路径匹配应使用 `fromPath()`。
- 把根 CA 塞到链首或把链顺序倒置：叶子证书应在首位，根 CA 通常由信任库提供。
- 只检查 Common Name，不检查 SAN：主机名诊断应优先查看 `subjectAlternativeNames()`，真正验证交给 backend。
- 用默认 `digest()` 作为安全指纹：默认是 MD5，应显式选择现代哈希算法。
- 看到 `verify()` 返回空列表就认为所有未来连接都可信：验证结果受 hostname、CA 配置、backend 和时间影响。
- 认为 `handle()` 是稳定的跨平台证书 ID：它只是底层互操作句柄。
- 忘记检查 `importPkcs12()` 的返回值和输出对象：失败时 key、证书或 CA 链不能直接使用。

## 逐项 API 说明

### 类型和构造

#### `enum SubjectInfo`

Qt 预定义的主题/颁发者属性类别，包括 `Organization`、`CommonName`、`LocalityName`、`OrganizationalUnitName`、`CountryName`、`StateOrProvinceName`、`DistinguishedNameQualifier`、`SerialNumber` 和 `EmailAddress`。它只覆盖 Qt 命名的常见属性；特殊属性可用字节数组 API 查询。

#### `enum class PatternSyntax`

指定 `fromPath()` 的路径解释方式：`RegularExpression`、`Wildcard` 或 `FixedString`。它只影响路径匹配，不影响证书解析格式。

#### `QSslCertificate(QIODevice *device, QSsl::EncodingFormat format = QSsl::Pem)`

从设备读取一张证书。设备必须提供可读内容；若内容包含多张证书，只取第一张。设备不由证书对象拥有或关闭。

#### `explicit QSslCertificate(const QByteArray &data = QByteArray(), QSsl::EncodingFormat format = QSsl::Pem)`

从字节数组解析一张证书。空数据或解析失败得到 null certificate；多证书输入只取第一张。

#### `QSslCertificate(const QSslCertificate &other)`

复制证书值对象。复制不会复制外部设备或 TLS 会话。

#### `QSslCertificate(QSslCertificate &&other) noexcept`

移动构造证书值对象。移动后的源对象只应析构或重新赋值。

#### `~QSslCertificate()`

销毁证书对象。Qt 释放其内部共享数据，不影响外部设备或证书文件。

#### `QSslCertificate &operator=(const QSslCertificate &other)`

复制赋值，替换当前证书。

#### `QSslCertificate &operator=(QSslCertificate &&other) noexcept`

移动赋值，转移证书值对象状态。

#### `void swap(QSslCertificate &other) noexcept`

交换两个证书对象，适合在不复制底层共享数据的情况下交换值。

### 状态和证书属性

#### `bool isNull() const`

判断对象是否为 null certificate。默认构造、空数据、解析失败或 `clear()` 后为 true；false 不能单独证明证书可信。

#### `bool isBlacklisted() const`

判断证书是否匹配 Qt/backend 的黑名单。它是额外的黑名单状态，不等于 null，也不替代完整链验证。

#### `bool isSelfSigned() const`

判断证书是否为自签名。自签名只描述签名者与主题关系，不等于不安全；内部 CA、测试证书或根 CA 都可能是自签名。

#### `void clear()`

清空证书，使对象恢复为 null certificate。

#### `QByteArray version() const`

返回证书版本字段的字节表示。它描述 X.509 版本，不是 Qt 或 TLS 版本。

#### `QByteArray serialNumber() const`

返回证书序列号的十六进制字符串。它是证书字段，不是全局唯一且可信的业务用户 ID。

#### `QByteArray digest(QCryptographicHash::Algorithm algorithm = QCryptographicHash::Md5) const`

返回证书编码数据的摘要。默认算法是 MD5；安全指纹应显式选择合适的强哈希算法。null certificate 不应被当作有效指纹。

#### `QStringList issuerInfo(SubjectInfo info) const`

返回颁发者指定标准属性的所有值。一个属性可能有多个值。

#### `QStringList issuerInfo(const QByteArray &attribute) const`

按字节属性标识查询颁发者字段，适合 Qt 枚举未覆盖的属性或明确的 OID/名称。

#### `QStringList subjectInfo(SubjectInfo info) const`

返回主题指定标准属性的所有值。

#### `QStringList subjectInfo(const QByteArray &attribute) const`

按字节属性标识查询主题字段。不要假设返回列表只有一个元素。

#### `QString issuerDisplayName() const`

返回便于显示的颁发者名称摘要。它可能为空或受证书内容影响，不应作为严格匹配键。

#### `QString subjectDisplayName() const`

返回便于显示的主题名称摘要。需要精确读取字段时使用 `subjectInfo()`。

#### `QList<QByteArray> subjectInfoAttributes() const`

返回证书主题中实际存在的属性标识列表。可用来发现非标准属性。

#### `QList<QByteArray> issuerInfoAttributes() const`

返回颁发者中实际存在的属性标识列表。

#### `QMultiMap<QSsl::AlternativeNameEntryType, QString> subjectAlternativeNames() const`

返回 Subject Alternative Name 中的 DNS 名称、IP 地址等条目。一个类型可有多个值；主机名验证不应由简单字符串比较自行替代。

#### `QDateTime effectiveDate() const`

返回证书的生效时间。字段缺失或证书无效时应检查返回的 `QDateTime` 是否有效。

#### `QDateTime expiryDate() const`

返回证书的到期时间。它适合显示和提前告警，但不能代替完整验证。

#### `QSslKey publicKey() const`

返回证书携带的公钥。仅在启用 SSL 支持时可用；证书 null 或解析失败时不要假设返回有效 key。

#### `QList<QSslCertificateExtension> extensions() const`

返回证书扩展列表。未知扩展可能仍存在，但应用必须根据扩展对象和 OID 判断是否能安全解释。

### 序列化和原生互操作

#### `QByteArray toPem() const`

以 PEM 编码导出证书。空证书不能导出可用证书材料。

#### `QByteArray toDer() const`

以 DER 编码导出证书。适合需要二进制 ASN.1 表示的文件、协议或指纹输入。

#### `QString toText() const`

返回适合人阅读的证书文本摘要。它用于诊断和展示，不应作为稳定的机器解析格式。

#### `Qt::HANDLE handle() const`

返回 backend/platform 相关的原生证书句柄。返回值不转移所有权，也不保证跨平台稳定。

### 静态读取和验证

#### `static QList<QSslCertificate> fromPath(const QString &path, QSsl::EncodingFormat format = QSsl::Pem, PatternSyntax syntax = PatternSyntax::FixedString)`

按指定语法解释路径并解析匹配文件中的全部证书。`FixedString` 不展开通配符；需要匹配多个文件时选择 `Wildcard` 或 `RegularExpression`。结果为空表示没有可解析证书，不应只看路径是否存在。

#### `static QList<QSslCertificate> fromDevice(QIODevice *device, QSsl::EncodingFormat format = QSsl::Pem)`

从可读设备解析全部证书。读取从设备当前状态和位置开始；设备所有权、打开和关闭由调用方负责。

#### `static QList<QSslCertificate> fromData(const QByteArray &data, QSsl::EncodingFormat format = QSsl::Pem)`

从字节数组解析全部证书。与单对象构造不同，它不会只保留第一张。

#### `static QList<QSslCertificate> fromFile(const QString &filePath, QSsl::EncodingFormat format = QSsl::Pem)`

从普通单文件解析全部证书。Qt 6.10 起提供；非普通文件、不可读文件或不存在文件返回空列表，不承担通配符匹配职责。

#### `static QList<QSslError> verify(const QList<QSslCertificate> &certificateChain, const QString &hostName = QString())`

使用当前 SSL backend 验证证书链；链首应为叶子证书，`hostName` 非空时还执行主机名校验。返回空列表表示没有报告错误，否则返回全部 `QSslError`。验证依赖 CA 配置和 backend。

#### `static bool importPkcs12(QIODevice *device, QSslKey *key, QSslCertificate *cert, QList<QSslCertificate> *caCertificates = nullptr, const QByteArray &passPhrase = QByteArray())`

从已打开、可读的 PKCS#12 设备中导入私钥、叶子证书和可选 CA 链。设备当前位置会影响读取；输出指针必须有效，除非对应参数允许为 `nullptr`。成功后仍应检查 key/cert 的 `isNull()`。

### 比较和哈希

#### `bool operator==(const QSslCertificate &other) const`

比较两个证书值对象是否相等，适合值比较和测试，不表示证书被信任或适用于某个主机。

#### `bool operator!=(const QSslCertificate &other) const`

返回不相等比较结果。

#### `size_t qHash(const QSslCertificate &key, size_t seed = 0) noexcept`

为证书提供 Qt 哈希支持，可用于 `QHash`。哈希可用于容器索引，不应被当作安全指纹或唯一身份。

## API 速查表

| 类别 | API | 语义 | 边界与注意事项 |
| --- | --- | --- | --- |
| 类型 | `SubjectInfo` | Qt 预定义主题/颁发者属性枚举。 | 特殊属性使用字节数组重载。 |
| 类型 | `PatternSyntax` | `fromPath()` 的路径匹配语法。 | 不影响 PEM/DER 解析。 |
| 构造 | `QSslCertificate(QIODevice *, EncodingFormat)` | 从设备读取第一张证书。 | 设备由调用方拥有；多证书用 `fromDevice()`。 |
| 构造 | `QSslCertificate(QByteArray, EncodingFormat)` | 从数据解析第一张证书。 | 空数据或失败得到 null。 |
| 构造 | 拷贝/移动构造 | 复制或移动证书值。 | 不复制外部设备或 TLS 会话。 |
| 生命周期 | `~QSslCertificate()` | 销毁证书对象。 | 不影响外部文件和设备。 |
| 赋值 | `operator=(const QSslCertificate &)` | 复制赋值。 | 覆盖当前对象。 |
| 赋值 | `operator=(QSslCertificate &&)` | 移动赋值。 | 移动源只应析构或重新赋值。 |
| 交换 | `swap(QSslCertificate &)` | 交换两个证书。 | 快速且不抛异常。 |
| 状态 | `isNull()` | 判断是否为空证书。 | 不代表可信性。 |
| 状态 | `isBlacklisted()` | 判断是否被黑名单匹配。 | 不替代链验证。 |
| 状态 | `isSelfSigned()` | 判断是否自签名。 | 自签名不等于一定不安全。 |
| 状态 | `clear()` | 清空证书。 | 恢复 null 状态。 |
| 属性 | `version()` | 获取 X.509 版本。 | 不是 Qt/TLS 版本。 |
| 属性 | `serialNumber()` | 获取十六进制序列号。 | 不要当十进制或业务 ID。 |
| 属性 | `digest(Algorithm)` | 获取证书摘要。 | 默认 MD5，不应作为现代安全指纹。 |
| 属性 | `issuerInfo(...)` | 查询颁发者属性。 | 结果是 `QStringList`，可能多值。 |
| 属性 | `subjectInfo(...)` | 查询主题属性。 | 支持枚举和字节数组重载。 |
| 属性 | `issuerDisplayName()` | 获取颁发者展示摘要。 | 适合显示，不适合严格身份判断。 |
| 属性 | `subjectDisplayName()` | 获取主题展示摘要。 | 可能为空。 |
| 属性 | `subjectInfoAttributes()` | 列出主题属性标识。 | 可发现非标准属性。 |
| 属性 | `issuerInfoAttributes()` | 列出颁发者属性标识。 | 可发现非标准属性。 |
| SAN | `subjectAlternativeNames()` | 获取 SAN 多值映射。 | 主机名验证不要用简单字符串替代。 |
| 时间 | `effectiveDate()` | 获取生效时间。 | 需检查 `QDateTime` 有效性。 |
| 时间 | `expiryDate()` | 获取到期时间。 | 只能作为有效期信息。 |
| 密钥 | `publicKey()` | 获取证书公钥。 | 受 SSL 构建和证书解析影响。 |
| 扩展 | `extensions()` | 获取 X.509 扩展。 | 未知扩展不一定有专用解释。 |
| 导出 | `toPem()` | 导出 PEM。 | null 对象不能产生可用证书。 |
| 导出 | `toDer()` | 导出 DER。 | 二进制编码，不含信任语义。 |
| 导出 | `toText()` | 导出可读文本。 | 不要当稳定机器格式。 |
| 原生 | `handle()` | 获取 native 句柄。 | 平台/backend 相关，不转移所有权。 |
| 读取 | `fromPath(...)` | 按路径语法读取匹配文件中的全部证书。 | 语法必须与实际路径意图匹配。 |
| 读取 | `fromDevice(...)` | 从设备读取全部证书。 | 设备需可读，位置会影响结果。 |
| 读取 | `fromData(...)` | 从数据读取全部证书。 | 与单对象构造区别在于返回全部。 |
| 读取 | `fromFile(...)` | 从普通文件读取全部证书。 | Qt 6.10 起；不展开通配符。 |
| 验证 | `verify(chain, hostName)` | 验证证书链和可选主机名。 | 叶子在首位；根 CA 通常由信任库提供。 |
| 导入 | `importPkcs12(...)` | 导入私钥、叶子证书和可选 CA 链。 | 设备须已打开可读；检查返回值和输出。 |
| 比较 | `operator==` / `operator!=` | 比较证书值。 | 不表示可信或主机适配。 |
| 哈希 | `qHash(...)` | 为 `QHash` 提供哈希。 | 不是安全指纹。 |

## 一句话总结

`QSslCertificate` 是 X.509 证书材料的 Qt 值类型：单对象构造只取第一张，批量读取用 `fromData()`/`fromDevice()`/`fromFile()`，验证时让叶子证书位于链首并结合 hostname、CA 和 backend 判断，`isNull()` 更不能被误当成“是否可信”。
