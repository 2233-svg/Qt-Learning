# QSsl：TLS、证书和密钥共用枚举

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QSsl>`  
> 所属模块：`Qt6::Network`  
> 类型性质：命名空间，定义 TLS 相关的枚举和标志

## 它解决什么问题

`QSsl` 集中定义 `QSslSocket`、`QSslConfiguration`、`QSslKey`、`QSslCertificate`、`QDtls` 等 TLS 类共用的枚举：密钥类型、编码格式、协议选择、实现能力和可选行为。

它不是 TLS 连接对象，不会发起握手、加载证书或验证服务器。实际网络连接由 `QSslSocket` 或高层网络类完成，具体配置通常写入 `QSslConfiguration`。

## 实际使用场景

- 为 `QSslSocket` 或 `QSslConfiguration` 选择 TLS/DTLS 协议范围。
- 指定证书和密钥文件采用 PEM 还是 DER 编码。
- 读取证书 Subject Alternative Name 的条目类型。
- 在运行时根据后端是否支持 ALPN、OCSP、PSK、会话票据或 TLS alerts 调整功能。
- 针对确有兼容性问题的旧服务器关闭某项 TLS 扩展。

协议和选项只是请求或描述。最终可用能力取决于平台 TLS 后端及其版本，应结合 `QSslSocket::supportsSsl()`、`implementedClasses()`、`supportedFeatures()` 等实际查询结果处理。

## 密钥与证书枚举

### `KeyType`

| 枚举值 | 含义 |
| --- | --- |
| `PrivateKey` | 私钥 |
| `PublicKey` | 公钥 |

它用于构造或解析 `QSslKey`。私钥属于敏感材料，枚举本身不提供安全存储或清零保证。

### `EncodingFormat`

| 枚举值 | 含义 |
| --- | --- |
| `Pem` | Base64 文本封装的 PEM 格式 |
| `Der` | 二进制 ASN.1 DER 格式 |

编码格式不等于密钥算法。一个 RSA、EC 或其它类型的键都可能以 PEM 或 DER 表示。

### `KeyAlgorithm`

| 枚举值 | 含义 |
| --- | --- |
| `Opaque` | 由外部提供者作为黑盒使用的密钥 |
| `Rsa` | RSA |
| `Dsa` | DSA |
| `Ec` | 椭圆曲线密钥 |
| `Dh` | Diffie-Hellman |
| `MlDsa` | ML-DSA |

枚举只描述类型，不表示当前后端一定能加载、签名或协商该算法。

### `AlternativeNameEntryType`

| 枚举值 | 含义 |
| --- | --- |
| `EmailEntry` | 证书适用的邮箱地址 |
| `DnsEntry` | DNS 主机名，可能包含通配符 |
| `IpAddressEntry` | IP 地址 |

使用 SAN 校验时，应将条目类型与待验证目标匹配。不能把 DNS 名称按 IP 地址规则比较，也不能自行把通配符规则扩展到不受协议允许的形式。

## 协议枚举：`SslProtocol`

新代码优先使用现代协议下限：

| 用途 | 推荐枚举 | 边界 |
| --- | --- | --- |
| TLS 至少 1.2 | `TlsV1_2OrLater` | Qt 6.3 起替代旧 TLS 1.0/1.1 选项 |
| TLS 1.2 | `TlsV1_2` | 固定为 TLS 1.2 |
| TLS 1.3 | `TlsV1_3` | 固定为 TLS 1.3 |
| TLS 至少 1.3 | `TlsV1_3OrLater` | 取决于后端实际支持 |
| DTLS 1.2 | `DtlsV1_2` | 用于数据报 TLS |
| DTLS 至少 1.2 | `DtlsV1_2OrLater` | 取决于后端实际支持 |
| 后端安全默认集合 | `SecureProtocols` | 默认策略，不应被理解为固定版本号 |
| 后端支持的任意协议 | `AnyProtocol` | 只适用于 `QSslSocket`，不宜作为安全策略 |
| 未知 | `UnknownProtocol` | 不能确定协议时的结果值 |

`TlsV1_0`、`TlsV1_1`、`TlsV1_0OrLater`、`TlsV1_1OrLater`、`DtlsV1_0` 和 `DtlsV1_0OrLater` 在 Qt 6.3 已弃用。不要为“兼容”而降低协议下限，除非有明确的风险接受和隔离策略。

## `SslOption`：只在必要时关闭特性

`SslOptions` 是 `QFlags<QSsl::SslOption>`，可以按位组合。它们主要用于处理已知的服务端兼容性问题，而不是常规性能开关。

| 选项 | 作用与边界 |
| --- | --- |
| `SslOptionDisableEmptyFragments` | 禁用空片段插入；默认已启用，旧服务器可能受影响。 |
| `SslOptionDisableSessionTickets` | 禁用会话票据；可能增加连接建立成本。 |
| `SslOptionDisableCompression` | 禁用 TLS 压缩；默认已启用，避免 CRIME 风险。 |
| `SslOptionDisableServerNameIndication` | 禁用 SNI；虚拟主机通常会因此选择错误证书。 |
| `SslOptionDisableLegacyRenegotiation` | 禁用旧式不安全重新协商；默认已启用。 |
| `SslOptionDisableSessionSharing` | 禁用通过 session ID 共享会话。 |
| `SslOptionDisableSessionPersistence` | 禁用会话票据 ASN.1 持久化；默认已启用以降低内存使用。 |
| `SslOptionDisableServerCipherPreference` | 服务器端不按服务器偏好选密码套件；仅服务器 socket 且 OpenSSL 后端支持。 |

这些选项能否生效依赖 TLS 后端版本。修改默认值前应先证明问题来自具体扩展，并做协议、证书、SNI 和会话恢复回归测试。

## 后端能力与 TLS alerts

### `ImplementedClass`

该枚举列出后端是否实现 `QSslKey`、`QSslCertificate`、`QSslSocket`、Diffie-Hellman、椭圆曲线、DTLS 和 DTLS cookie 验证器等类。公开头文件存在不等于所有后端都有可运行实现。

### `SupportedFeature`

可查询的能力包括：

- `CertificateVerification`
- `ClientSideAlpn`
- `ServerSideAlpn`
- `Ocsp`
- `Psk`
- `SessionTicket`
- `Alerts`

功能开关应按此结果降级或报告不可用，而不是在运行时静默假定后端支持。

### `AlertLevel` 与 `AlertType`

`AlertLevel` 是 `Warning`、`Fatal`、`Unknown`。`Fatal` 表示底层后端会正确终止连接，应用应转入失败处理，不应继续复用该 socket。

`AlertType` 包含标准 TLS alert 代码，如 `CloseNotify`、`HandshakeFailure`、`BadCertificate`、`CertificateExpired`、`UnknownCa`、`ProtocolVersion`、`NoApplicationProtocol` 等。它是协议诊断信息，不是可据此忽略证书错误的授权依据。

## 常见误区

- 把 `QSsl` 当作可以创建 TLS 连接的对象。
- 使用 `AnyProtocol` 代替明确的最低协议要求。
- 为了连接旧服务端盲目关闭 SNI、证书校验相关行为或安全默认选项。
- 把 PEM/DER 编码格式误认为 RSA/EC 等密钥算法。
- 只看枚举是否存在，不检查 TLS 后端的实际实现和支持能力。
- 收到 TLS alert 后继续向同一连接写入业务数据。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 命名空间 | `QSsl` | 放置 TLS 共用枚举。 | 本身不建立连接。 |
| 密钥 | `KeyType` | 区分 `PrivateKey` 和 `PublicKey`。 | 私钥生命周期和存储由应用负责。 |
| 编码 | `EncodingFormat` | 选择 `Pem` 或 `Der`。 | 与密钥算法无关。 |
| 算法 | `KeyAlgorithm` | 描述 Opaque、RSA、DSA、EC、DH、ML-DSA。 | 后端可能不支持。 |
| 证书 | `AlternativeNameEntryType` | 区分邮箱、DNS、IP SAN 条目。 | 比较规则必须按条目类型执行。 |
| 协议 | `SslProtocol` | 选择 TLS/DTLS 协议策略。 | 新代码优先 TLS/DTLS 1.2 及以上。 |
| 协议 | `TlsV1_2OrLater` | 请求 TLS 1.2 或更高版本。 | 受 TLS 后端支持限制。 |
| 协议 | `TlsV1_3` / `TlsV1_3OrLater` | 请求 TLS 1.3 或更高版本。 | 后端或服务端不支持时需处理失败。 |
| 协议 | `DtlsV1_2` / `DtlsV1_2OrLater` | 请求 DTLS 1.2。 | 仅适用于 DTLS 场景。 |
| 协议 | 旧 TLS/DTLS 1.0/1.1 枚举 | 旧协议版本选择。 | Qt 6.3 已弃用。 |
| 选项 | `SslOption` / `SslOptions` | 以位标志调整 TLS 扩展行为。 | 只针对已证实的兼容性问题使用。 |
| 能力 | `ImplementedClass` | 描述后端实现了哪些 TLS 类。 | 公开 API 存在不代表可用。 |
| 能力 | `SupportedFeature` | 描述后端支持哪些 TLS 特性。 | 在启用 ALPN、OCSP、PSK 等前检查。 |
| alerts | `AlertLevel` | 描述告警严重度。 | `Fatal` 后应停止使用连接。 |
| alerts | `AlertType` | 描述标准 TLS alert 代码。 | 用于诊断，不用于绕过安全验证。 |

### 一句话总结

`QSsl` 提供 TLS 配置和诊断的共同词汇；安全策略必须同时考虑协议下限、证书验证和底层 TLS 后端能力。
