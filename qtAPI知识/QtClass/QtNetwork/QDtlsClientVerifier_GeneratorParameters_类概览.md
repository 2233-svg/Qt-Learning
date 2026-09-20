# QDtlsClientVerifier::GeneratorParameters：DTLS cookie 生成参数

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDtlsClientVerifier>`  
> CMake：`find_package(Qt6 REQUIRED COMPONENTS Network)`，并链接 `Qt6::Network`  
> 类型：值类型结构体

## 它解决什么问题

`QDtlsClientVerifier::GeneratorParameters` 把生成 DTLS cookie 所需的两个输入封装在一起：哈希算法 `hash` 和服务端 secret `secret`。它是传给 `QDtlsClientVerifier::setCookieGeneratorParameters()` 与 `QDtls::setCookieGeneratorParameters()` 的配置值。

cookie 验证的目的不是加密业务数据，而是在服务端开始消耗会话和握手资源之前，确认请求发起者确实能接收返回到其 UDP 地址和端口的响应。这个结构体让 verifier 与后续 `QDtls` 会话使用一致的 cookie 计算规则。

## 实际使用场景

- 服务启动时从密码学安全随机源生成 secret，配置到全局 verifier 和所有服务端 `QDtls` 会话。
- 按安全策略轮换 secret，使过旧的 cookie 失效。
- 显式选择后端支持的哈希算法，并把配置封装为可传递的值对象。

它不持有密钥生命周期策略，也不会自动轮换 secret；secret 的生成、保存、发布和轮换均由应用负责。

## 正确配置

```cpp
QByteArray secret = loadCryptographicallySecureSecret();
QDtlsClientVerifier::GeneratorParameters params(
    QCryptographicHash::Sha256, secret);

if (!verifier.setCookieGeneratorParameters(params))
    qFatal("DTLS cookie secret must not be empty");

// 为通过 verifier 的客户端建立服务端 QDtls 前：
dtls.setCookieGeneratorParameters(params);
```

同一条服务端验证路径中，verifier 和对应 `QDtls` 必须使用相同参数。若两边的 secret 或哈希算法不同，verifier 验证过的 ClientHello 仍可能被后续 `QDtls` 的 cookie 检查拒绝。

## 关键语义与边界

- 默认构造得到 `Sha1` 和空 `secret`。这是“待填充”的值，不是可直接安装的安全配置。
- `QDtlsClientVerifier::setCookieGeneratorParameters()` 把空 secret 视为无效，返回 `false`，且不会替换当前配置。
- 哈希算法不是 secret 的替代品。即使算法强，固定、可预测或泄露的 secret 仍会削弱 cookie 防护。
- secret 应是密码学安全随机字节序列，不能由域名、端口、当前时间或普通 `qrand()` 推导。
- 轮换 secret 会使旧 cookie 失效。生产服务端若需要平滑轮换，应在应用层设计短暂的双 secret 验证窗口或重试策略；这个结构体和 Qt API 不保存历史 secret。
- 该结构体按值传递，复制它也会复制 secret。避免在日志、调试输出、崩溃报告或不受保护的配置文件中泄露它。

## API 速查表

| 类别 | API | 语义与使用重点 |
| --- | --- | --- |
| 构造 | `GeneratorParameters()` | 默认 `hash` 为 `QCryptographicHash::Sha1`，`secret` 为空；不能直接作为有效 verifier 配置。 |
| 构造 | `GeneratorParameters(QCryptographicHash::Algorithm algorithm, const QByteArray &secret)` | 以指定 hash 和 secret 构造；调用设置函数前仍需确认 secret 非空且安全生成。 |
| 数据成员 | `QCryptographicHash::Algorithm hash` | 生成 cookie 时使用的哈希算法；verifier 与服务端 `QDtls` 必须一致。 |
| 数据成员 | `QByteArray secret` | cookie 的服务端秘密字节串；不可为空，必须保密、随机并按策略轮换。 |
| 协作 API | `QDtlsClientVerifier::setCookieGeneratorParameters()` | 安装 verifier 的 cookie 参数；空 secret 会失败。 |
| 协作 API | `QDtls::setCookieGeneratorParameters()` | 为服务端 DTLS 会话安装同一套参数；必须在握手前调用。 |

## 一句话总结

`GeneratorParameters` 是 DTLS cookie 的 hash 与 secret 配置载体；真正的安全性取决于 secret 的随机性、保密性、轮换策略，以及 verifier 与 `QDtls` 是否严格保持一致。
