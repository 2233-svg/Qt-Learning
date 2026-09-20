# QSslConfiguration
> Qt 6.11.1 · Qt Network · 来自 `QSslConfiguration`

## 作用定位
`QSslConfiguration` 是 TLS 会话的值类型配置，控制协议、证书、私钥、CA、密码套件与 OCSP。

## API 速查
| API | 是做什么的 |
|---|---|
| `defaultConfiguration()` | 读取默认 TLS 设置。|
| `setProtocol()` | 限制允许协议版本。|
| `setCaCertificates()` | 设置受信任 CA。|
| `setLocalCertificate()` / `setPrivateKey()` | 设置客户端/服务端身份。|
| `setCiphers()` | 限制密码套件。|
| `setOcspStaplingEnabled()` | 配置 OCSP stapling。|

## 使用场景
企业私有 CA、mTLS 客户端、受控 TLS 合规策略。

## 常见坑与经验
- 从系统默认配置大幅删改可能造成兼容性或安全退化；变更需测试真实服务端。

## 知识点覆盖
TLS 配置、CA、mTLS、协议版本、密码套件、OCSP。
