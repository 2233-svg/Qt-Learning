# QSslError

> Qt 6.11.1 | Qt6::Network | `#include <QSslError>`

## 类解决的问题

TLS 握手失败或证书校验不通过时，仅有一个“连接失败”状态通常不够排障。`QSslError` 是 Qt 对单个 SSL/TLS 错误的值对象描述，用来记录：

- 错误属于哪一类；
- Qt 提供的本地化短错误文本；
- 如果错误关联某张证书，具体是哪张证书。

它通常出现在 `QSslSocket::sslErrors()`、`QSslSocket::peerVerifyError()`、`QSslServer` 的相关信号和 `QSslCertificate::verify()` 返回值中。它是诊断数据，不是自动修复器；是否继续握手必须由应用根据错误类型、连接目标和信任策略决定。

## 实际使用场景

### 1. 记录证书校验失败原因

```cpp
connect(socket, &QSslSocket::sslErrors, this,
        [socket](const QList<QSslError> &errors) {
    for (const QSslError &error : errors) {
        qWarning() << error.error()
                   << error.errorString()
                   << error.certificate().subjectDisplayName();
    }
});
```

生产环境应避免把私密连接信息、完整证书内容或敏感主机信息无条件写入日志。

### 2. 只对明确允许的错误做策略判断

```cpp
connect(socket, &QSslSocket::sslErrors, this,
        [socket](const QList<QSslError> &errors) {
    const bool expectedForTest =
        errors.size() == 1
        && errors.front().error() == QSslError::SelfSignedCertificate;

    if (expectedForTest) {
        socket->ignoreSslErrors(errors);
    }
});
```

测试环境可以针对固定证书做例外；生产代码不应因为 `sslErrors()` 被触发就无条件调用 `ignoreSslErrors()`。

### 3. 结合证书对象做更深入检查

当 `certificate()` 非 null 时，可以读取主题、颁发者、有效期、SAN 和指纹；但这些信息只能帮助解释错误，不能绕过应用既定的信任策略。

## 构建与最小示例

```cmake
find_package(Qt6 REQUIRED COMPONENTS Network)
target_link_libraries(app PRIVATE Qt6::Network)
```

```cpp
#include <QSslError>

const QSslError error(QSslError::HostNameMismatch);
qInfo() << error.error() << error.errorString();
```

## 关键语义与边界

### 它是握手诊断值对象

`QSslError` 描述单个错误，不会主动改变 socket、证书链或验证模式。一个握手可能产生多个 `QSslError`，因此 `sslErrors()` 的参数是列表，处理时不要只读取第一项就丢弃其余诊断信息。

### 用 `error()` 做程序分支，用 `errorString()` 给人看

`error()` 返回稳定的枚举值，适合白名单、统计和控制流。`errorString()` 是短的本地化人类可读文本，可能随语言环境、Qt 版本或 backend 改变，不能拿来做精确逻辑判断。

### `certificate()` 可能是 null

证书链、签名、有效期或主机名相关错误通常可以关联证书，但 `NoSslSupport` 等错误可能没有具体证书。调用 `certificate()` 后先用 `isNull()` 判断，不能直接假设主题或序列号存在。

### 不要把错误枚举误认为都能安全忽略

`SelfSignedCertificate`、`CertificateExpired`、`HostNameMismatch`、`CertificateRevoked`、OCSP 错误等代表不同风险。是否允许继续连接是信任策略问题，不能通过“错误发生在测试机上”推导出生产环境也可以忽略。

### `NoPeerCertificate` 的含义取决于连接角色和配置

它表示没有收到对端证书，但客户端/服务端是否要求证书还取决于 `peerVerifyMode`、TLS 角色和 backend。处理时应同时查看 socket 的配置和实际连接方向，不要单凭错误名称推断完整原因。

### OCSP 错误属于证书状态检查路径

`OcspNoResponseFound`、`OcspMalformedResponse`、`OcspResponseExpired` 等错误与在线证书状态协议有关。它们不是普通的“证书格式错误”，应结合是否启用 OCSP stapling、服务端返回内容和应用的撤销策略排查。

### 生命周期、线程和比较

这是可重入的值对象，可放入 Qt 容器并跨函数传递。复制不会让错误继续监听 socket，也不会持有 socket 生命周期。比较运算适合比较错误值对象；不要把 `errorString()` 当成唯一标识。

## 常见误区

- 用 `errorString()` 判断错误类型：应使用 `error()`。
- 收到 `sslErrors()` 后无条件调用 `ignoreSslErrors()`：这会绕过证书验证。
- 假定每个错误都附带证书：先检查 `certificate().isNull()`。
- 把一组错误当成只有一个错误：应遍历完整列表。
- 看到 `SelfSignedCertificate` 就认为连接一定恶意：也可能是明确配置的内部 CA，但是否信任必须由策略决定。
- 把 `NoSslSupport` 当成证书错误：它通常说明当前环境没有可用 SSL 能力，应检查 backend、部署和构建配置。

## 错误枚举分组

### 证书链、签名和字段

- `UnableToGetIssuerCertificate`
- `UnableToDecryptCertificateSignature`
- `UnableToDecodeIssuerPublicKey`
- `CertificateSignatureFailed`
- `UnableToGetLocalIssuerCertificate`
- `UnableToVerifyFirstCertificate`
- `SubjectIssuerMismatch`
- `AuthorityIssuerSerialNumberMismatch`
- `InvalidNotBeforeField`
- `InvalidNotAfterField`
- `PathLengthExceeded`

### 有效期、信任和用途

- `CertificateNotYetValid`
- `CertificateExpired`
- `SelfSignedCertificate`
- `SelfSignedCertificateInChain`
- `CertificateRevoked`
- `InvalidCaCertificate`
- `InvalidPurpose`
- `CertificateUntrusted`
- `CertificateRejected`
- `NoPeerCertificate`
- `HostNameMismatch`
- `CertificateBlacklisted`
- `CertificateStatusUnknown`

### 环境和 OCSP

- `NoSslSupport`
- `OcspNoResponseFound`
- `OcspMalformedRequest`
- `OcspMalformedResponse`
- `OcspInternalError`
- `OcspTryLater`
- `OcspSigRequred`
- `OcspUnauthorized`
- `OcspResponseCannotBeTrusted`
- `OcspResponseCertIdUnknown`
- `OcspResponseExpired`
- `OcspStatusUnknown`

`NoError` 表示没有错误；`UnspecifiedError` 的数值为 `-1`，表示未指定错误。`OcspSigRequred` 是 Qt 6.11.1 头文件中的拼写，代码中应使用 Qt 实际声明的枚举名。

## 逐项 API 说明

### 构造、赋值和交换

#### `QSslError()`

构造“无错误”的对象，并带有默认的 null certificate。

#### `explicit QSslError(QSslError::SslError error)`

构造指定类型的错误，不关联证书。

#### `QSslError(QSslError::SslError error, const QSslCertificate &certificate)`

构造指定类型并关联指定证书的错误。证书参数是值对象，不会把证书的所有权转移给错误对象。

#### `QSslError(const QSslError &other)`

复制错误对象。

#### `QSslError &operator=(const QSslError &other)`

复制赋值，替换当前错误。

#### `QSslError &operator=(QSslError &&other) noexcept`

移动赋值，转移值对象状态。

#### `~QSslError()`

销毁错误对象，不影响产生该错误的 socket 或证书。

#### `void swap(QSslError &other) noexcept`

交换两个错误对象，操作快速且不抛异常。

### 查询

#### `QSslError::SslError error() const`

返回错误枚举。程序分支、过滤和统计应使用此函数。

#### `QString errorString() const`

返回短的本地化人类可读文本。适合 UI 和诊断日志，不适合作为持久化协议字段或逻辑键。

#### `QSslCertificate certificate() const`

返回关联证书；若该错误不针对具体证书，则返回 null certificate。

### 比较

#### `bool operator==(const QSslError &other) const`

比较两个错误对象是否相等，适合测试预期错误或去重。

#### `bool operator!=(const QSslError &other) const`

返回 `operator==` 的反结果。

## API 速查表

| 类别 | API | 语义 | 边界与注意事项 |
| --- | --- | --- | --- |
| 枚举 | `enum SslError` | 描述 TLS 握手中可识别的错误类型。 | 用枚举做逻辑判断，不要解析错误字符串。 |
| 构造 | `QSslError()` | 构造 `NoError` 和 null certificate。 | 只是值对象，不会连接或修复 socket。 |
| 构造 | `explicit QSslError(SslError error)` | 构造指定错误。 | 不关联证书。 |
| 构造 | `QSslError(SslError error, const QSslCertificate &certificate)` | 构造错误并关联证书。 | 证书仍是值对象，不转移所有权。 |
| 构造 | `QSslError(const QSslError &other)` | 复制错误。 | 不复制 socket 生命周期。 |
| 赋值 | `QSslError &operator=(const QSslError &other)` | 复制赋值。 | 覆盖当前错误。 |
| 赋值 | `QSslError &operator=(QSslError &&other) noexcept` | 移动赋值。 | 转移值对象状态。 |
| 析构 | `~QSslError()` | 销毁错误值对象。 | 不影响 socket 或证书。 |
| 交换 | `void swap(QSslError &other) noexcept` | 交换两个错误。 | 快速且不抛异常。 |
| 查询 | `SslError error() const` | 返回错误枚举。 | 适合程序分支、统计和过滤。 |
| 查询 | `QString errorString() const` | 返回本地化短文本。 | 不稳定，不应作为逻辑键。 |
| 查询 | `QSslCertificate certificate() const` | 返回关联证书。 | 没有关联证书时返回 null certificate。 |
| 比较 | `bool operator==(const QSslError &other) const` | 判断两个错误相等。 | 可用于白名单或测试。 |
| 比较 | `bool operator!=(const QSslError &other) const` | 判断两个错误不同。 | 与 `operator==` 相反。 |

## 一句话总结

`QSslError` 是 TLS 失败原因的结构化诊断值：用 `error()` 控制逻辑，用 `errorString()` 面向人，用 `certificate()` 追踪具体证书，并把“是否忽略”留给明确的信任策略。
