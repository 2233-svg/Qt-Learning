# QDnsTlsAssociationRecord：表示 DNS TLSA/DANE 证书关联记录

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDnsTlsAssociationRecord>`  
> 所属模块：`Qt6::Network`  
> 类型性质：隐式共享值类型，由 `QDnsLookup` 返回  
> 引入版本：Qt 6.8

## 它解决什么问题

TLSA 记录把 DNS 名称与某个 TLS 证书或公钥材料关联，用于 DANE 场景。`QDnsTlsAssociationRecord` 保存一条 TLSA 应答的：

- 证书使用方式 `usage()`；
- 要匹配完整证书还是 SPKI 的 `selector()`；
- 原文、SHA-256 或 SHA-512 匹配方式 `matchType()`；
- 二进制关联数据 `value()`；
- 记录名称和 TTL。

它只描述 DNS 中返回的 TLSA 数据。它不验证 DNSSEC、不读取 socket 的对端证书、不比较证书摘要，也不会自动改变 `QSslSocket` 的证书验证策略。

## 实际使用场景

```cpp
QDnsLookup lookup(QDnsLookup::TLSA, u"_443._tcp.example.test"_s);

connect(&lookup, &QDnsLookup::finished, this, [&lookup] {
    if (lookup.error() != QDnsLookup::NoError)
        return;

    for (const QDnsTlsAssociationRecord &record
         : lookup.tlsAssociationRecords()) {
        qDebug() << record.name()
                 << int(record.usage())
                 << int(record.selector())
                 << int(record.matchType())
                 << record.value().toHex();
    }
});

lookup.lookup();
```

TLSA 查询名通常由端口、传输协议和服务主机组成，例如 `_443._tcp.example.test`。具体命名、证书选择、验证步骤和失败策略必须遵守所实现协议的 DANE 规范。

## 三个控制字段必须组合理解

### `CertificateUsage`

| 值 | 别名 | 含义 |
| --- | --- | --- |
| `CertificateAuthorityConstrait` | `PKIX_TA` | 关联一个必须出现在链中且仍通过 PKIX 验证的 CA。 |
| `ServiceCertificateConstraint` | `PKIX_EE` | 关联服务端终端证书，且仍通过 PKIX 验证。 |
| `TrustAnchorAssertion` | `DANE_TA` | 指定 DANE 信任锚，用于验证服务端证书链。 |
| `DomainIssuedCertificate` | `DANE_EE` | 指定必须匹配的服务端终端证书，不执行 PKIX 验证。 |
| `PrivateUse` | `PrivCert` | 私有用途，没有标准解释。 |

第一个枚举名的 `Constrait` 拼写来自 Qt 公共 API，不能在代码中自行改成 `Constraint`。`DANE_EE` 等模式涉及不同的 PKIX 处理要求，不应只凭一个枚举值就决定绕过或放宽常规证书校验。

### `Selector`

| 值 | 别名 | 选择的数据 |
| --- | --- | --- |
| `FullCertificate` | `Cert` | DER 形式的完整证书 |
| `SubjectPublicKeyInfo` | `SPKI` | 证书的 SubjectPublicKeyInfo 结构 |
| `PrivateUse` | `PrivSel` | 私有用途 |

### `MatchingType`

| 值 | 含义 |
| --- | --- |
| `Exact` | `value()` 是被选择数据的原始二进制内容 |
| `Sha256` | `value()` 是被选择数据的 SHA-256 二进制摘要 |
| `Sha512` | `value()` 是被选择数据的 SHA-512 二进制摘要 |
| `PrivateUse` / `PrivMatch` | 私有用途 |

这三组字段共同决定 `value()` 的解释。不能把任何 `value()` 都当作 PEM 文本、十六进制字符串或完整证书。

## `value()` 的二进制边界

`value()` 返回 `QByteArray`，始终应按二进制数据处理：

- `Exact` 时可能是完整证书或 SPKI 的 DER 字节；
- `Sha256`、`Sha512` 时是摘要原始字节，不是 `toHex()` 后的 ASCII；
- 日志可使用 `toHex()`，但比较前不能把一方当原始字节、另一方当十六进制文本；
- 长度和匹配过程应符合 selector 与 matching type 的组合。

该类不公开 setter，不能用它手工生成 TLSA 记录。应用从 `QDnsLookup::tlsAssociationRecords()` 读取后，应以自己的协议验证器或已实现的 DANE 逻辑消费。

## DNS 真实性、TLS 验证和缓存

DNS 查询成功并不自动说明 TLSA 数据可以被当作信任依据。使用 DANE 前，调用方应明确处理 DNS 响应真实性，例如评估 `QDnsLookup::isAuthenticData()` 及底层 resolver/部署能力，并遵守所采用规范的 DNSSEC 要求。

同样，TLSA 记录不替代 TCP/DTLS 连接、主机名处理、证书链读取和握手错误处理。不要把 `DomainIssuedCertificate` 等值当作可以在没有完整验证流程时直接忽略 TLS 错误的开关。

`timeToLive()` 为秒单位 DNS 缓存期限。自建缓存应以响应到达时间计算过期，并在安全策略、DNS 真实性或记录变化时重新评估。

## 生命周期与线程

`QDnsTlsAssociationRecord` 是隐式共享值类型。默认构造为空记录；有效数据通常在 `QDnsLookup::finished()` 后从 `tlsAssociationRecords()` 取得。

异步任务或缓存需要保留结果时，按值复制记录。不要保存查询结果列表元素的引用，也不要假定下一次 `lookup()` 后旧列表仍代表当前 DNS 状态。

## 逐项 API 说明

### `QDnsTlsAssociationRecord()`

创建空 TLSA 记录。没有公开 setter，业务有效记录来自 DNS 查询。

### `QDnsTlsAssociationRecord(const QDnsTlsAssociationRecord &other)`

复制记录。类型采用隐式共享，复制不会发起 DNS 查询或证书验证。

### `CertificateUsage usage() const`

返回证书使用方式。它决定 DANE 和 PKIX 验证关系，必须结合协议规范处理。

### `Selector selector() const`

返回关联数据针对完整证书还是 SPKI。它决定从对端证书中取哪一段二进制数据。

### `MatchingType matchType() const`

返回直接比较、SHA-256、SHA-512 或私有匹配方式。它决定 `value()` 的字节含义。

### `QByteArray value() const`

返回关联二进制数据。不是自动解码的 PEM、文本或十六进制字符串。

### `QString name() const` / `quint32 timeToLive() const`

返回记录所有者名称和缓存 TTL 秒数。TTL 不是 TLS 会话时间或证书到期时间。

### `void swap(QDnsTlsAssociationRecord &other) noexcept`

交换两个本地记录值，不影响 DNS 或 TLS 状态。

### 复制/移动 `operator=`

替换当前记录。移动后源对象只保证可析构或重新赋值。

## 常见误区

- 查询到 TLSA 就直接把它当作可信验证结论。
- 不检查 DNS 响应真实性或 DNSSEC 部署条件。
- 把 `value()` 当成 PEM 文本或十六进制字符串。
- 忽略 usage、selector、matchType 必须组合解释。
- 把 TTL 当作证书有效期或 TLS 会话生命周期。
- 用 `DANE_EE` 等枚举直接绕过独立的 TLS 错误处理。
- 默认构造记录后期待可以设置 TLSA 字段。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QDnsTlsAssociationRecord()` | 创建空 TLSA 记录。 | 有效数据来自 `QDnsLookup::TLSA`。 |
| 构造 | `QDnsTlsAssociationRecord(const QDnsTlsAssociationRecord &)` | 复制记录。 | 隐式共享，不验证证书。 |
| 枚举 | `CertificateUsage` | 描述 DANE/PKIX 使用方式。 | 结合规范和 DNS 真实性处理。 |
| 枚举 | `Selector` | 选择完整证书或 SPKI。 | 决定待比较的二进制材料。 |
| 枚举 | `MatchingType` | 选择直接、SHA-256 或 SHA-512 匹配。 | 决定 `value()` 的字节解释。 |
| 字段 | `CertificateUsage usage() const` | 返回使用方式。 | 不能单独据此绕过 TLS 验证。 |
| 字段 | `Selector selector() const` | 返回选择器。 | `Cert`/`SPKI` 是别名。 |
| 字段 | `MatchingType matchType() const` | 返回匹配方式。 | 摘要值是二进制，不是 hex 文本。 |
| 字段 | `QByteArray value() const` | 返回 TLSA 关联数据。 | 组合三项控制字段解释。 |
| 字段 | `QString name() const` | 返回记录所有者名称。 | 通常包含服务端口和传输标签。 |
| 缓存 | `quint32 timeToLive() const` | 返回 TTL 秒数。 | 不是证书有效期。 |
| 工具 | `void swap(QDnsTlsAssociationRecord &)` | 交换两个记录值。 | 不影响 DNS/TLS 状态。 |
| 赋值 | 复制/移动 `operator=` | 替换当前记录。 | 移动后不依赖源内容。 |

### 一句话总结

`QDnsTlsAssociationRecord` 只是 TLSA 的结构化 DNS 数据；它能提供 DANE 比较所需字段，但不能替代 DNS 真实性检查或完整 TLS 验证流程。
