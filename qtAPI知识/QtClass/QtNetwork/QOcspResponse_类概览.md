# QOcspResponse：TLS 握手中携带的证书吊销状态

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QOcspResponse>`  
> CMake：`Qt6::Network`，且 Qt 构建须启用 SSL  
> 类型：隐式共享值类型

## 它解决什么问题

`QOcspResponse` 表示客户端在 TLS 握手期间通过 OCSP stapling 从服务器收到的一条证书吊销状态响应。它把响应所针对的证书、签名响应的证书、证书状态和吊销原因以可检查的值对象形式提供出来。

它不是 OCSP 请求器，也不能由应用手工填充真实响应。应用需要先在 `QSslConfiguration` 中启用 OCSP stapling，再从已握手的 `QSslSocket::ocspResponses()` 读取结果。

## 实际使用场景

- 安全诊断工具检查服务器在 TLS 握手中实际 stapled 的 OCSP 状态。
- 对高安全连接记录证书的 `Good`、`Revoked` 或 `Unknown` 结果和吊销原因。
- 测试 TLS 服务是否配置了可用的 OCSP stapling。

它适合观测和附加策略判断，不应单独替代完整 TLS 证书链验证、主机名验证、有效期验证或应用自身的信任策略。

## 获取方式

先在连接前开启 stapling；握手完成后读取响应：

```cpp
#include <QSslConfiguration>
#include <QSslSocket>

QSslConfiguration configuration = QSslConfiguration::defaultConfiguration();
configuration.setOcspStaplingEnabled(true);

QSslSocket socket;
socket.setSslConfiguration(configuration);

QObject::connect(&socket, &QSslSocket::encrypted, &socket, [&socket] {
    for (const QOcspResponse &response : socket.ocspResponses()) {
        qDebug() << response.certificateStatus()
                 << response.revocationReason();
    }
});

socket.connectToHostEncrypted(QStringLiteral("api.example.com"), 443);
```

即使调用了 `setOcspStaplingEnabled(true)`，结果列表也可能为空：TLS 后端需要支持 OCSP、服务器需要发送响应，而且 Qt 必须收到可确定的响应。`QSslSocket::ocspResponses()` 在未收到响应或没有明确响应时返回空列表。

## 关键语义与边界

### `Good` 不是“完整证书验证通过”

| 状态 | 含义 |
| --- | --- |
| `Good` | 响应称证书未被吊销；但这不必然证明证书曾被签发，也不保证响应产生时刻处于证书有效期内。 |
| `Revoked` | 证书已被永久或临时吊销（例如 hold）。 |
| `Unknown` | responder 不知道所查询的证书。默认构造对象也为此状态。 |

因此“有一条 `Good` 响应”不能替代对 `QSslSocket` 握手错误、对端证书、主机名和系统信任链的检查。应先完成正常 TLS 验证，再将 OCSP 结果作为额外信号。

### 吊销原因只解释 Revoked

`revocationReason()` 采用 RFC 5280 的原因枚举：`KeyCompromise`、`CACompromise`、`AffiliationChanged`、`Superseded`、`CessationOfOperation`、`CertificateHold`、`RemoveFromCRL` 等。没有吊销原因时为 `None`，默认构造对象也是 `None`。

只有 `certificateStatus() == Revoked` 时，原因通常才有实际解释价值；不要把 `None` 当作“明确未吊销”的结论。

### subject 与 responder 不同

`subject()` 返回这条 OCSP 响应所针对的证书；`responder()` 返回用于签名该 OCSP 响应的证书。二者常常不同。审计时应分别记录，不能把 responder 当作服务器 leaf certificate。

### 平台和后端能力

该类要求 Qt 具备 SSL 功能，OCSP stapling 还依赖当前 TLS 后端的能力。可通过 `QSslSocket` 的支持特性了解 OCSP 可用性。跨平台安全策略不能假设所有部署环境都会返回 OCSP 响应，应将“无响应”设计为明确可处理的状态。

### 值语义与哈希

`QOcspResponse` 是可复制、可移动的隐式共享值类型，适合保存在 `QList` 或用 `qHash()` 放入哈希容器。相等比较要求它们针对同一 subject、由同一 responder 签名，并且证书状态和吊销原因相同。

## 常见误区

- **调用 `ocspResponses()` 前未启用 stapling**：通常不会得到可用结果。
- **空列表等于“证书未吊销”**：空列表只是没有收到明确响应。
- **`Good` 等于 TLS 全面安全**：它不涵盖证书签发、时间有效性、主机名和信任链的全部问题。
- **把 `responder()` 当作服务端证书**：实际目标证书是 `subject()`。
- **只在 `Unknown` 时看 `revocationReason()`**：原因主要对 `Revoked` 有解释意义。

## API 速查表

| 类别 | API | 语义与注意点 |
| --- | --- | --- |
| 状态枚举 | `QOcspCertificateStatus::Good` | 声称未吊销；不等同完整证书有效性或信任验证。 |
| 状态枚举 | `QOcspCertificateStatus::Revoked` | 已永久或临时吊销。 |
| 状态枚举 | `QOcspCertificateStatus::Unknown` | responder 不认识该证书；默认构造状态。 |
| 原因枚举 | `QOcspRevocationReason::None` | 没有吊销原因；默认值，不代表已验证未吊销。 |
| 原因枚举 | `Unspecified`、`KeyCompromise`、`CACompromise`、`AffiliationChanged`、`Superseded`、`CessationOfOperation`、`CertificateHold`、`RemoveFromCRL` | RFC 5280 吊销原因；主要在状态为 `Revoked` 时解释为何吊销。 |
| 构造 | `QOcspResponse()` | 创建 `Unknown` / `None` 的默认响应。 |
| 值语义 | 拷贝构造、移动构造、拷贝/移动赋值、`swap(other)` | 隐式共享值操作，不执行网络访问。 |
| 析构 | `~QOcspResponse()` | 普通值类型析构。 |
| 查询 | `certificateStatus()` | 返回 Good、Revoked 或 Unknown。 |
| 查询 | `revocationReason()` | 返回吊销原因；结合 Revoked 状态解释。 |
| 查询 | `subject()` | 返回该响应针对的证书。 |
| 查询 | `responder()` | 返回签名 OCSP 响应的证书。 |
| 比较 | `operator==(lhs, rhs)` / `operator!=(lhs, rhs)` | 比较 subject、responder、状态和吊销原因。 |
| 哈希 | `qHash(response, seed)` | 用于哈希容器的散列函数。 |

## 相关类型

- `QSslConfiguration::setOcspStaplingEnabled()`：在握手前请求 OCSP stapling。
- `QSslSocket::ocspResponses()`：握手后取得 `QList<QOcspResponse>`。
- `QSslCertificate`：`subject()` 和 `responder()` 的返回类型。
