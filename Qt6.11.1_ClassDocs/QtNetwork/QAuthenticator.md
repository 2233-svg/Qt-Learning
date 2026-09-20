# QAuthenticator
> Qt 6.11.1 · Qt Network · 来自 `QAuthenticator`

## 作用定位
`QAuthenticator` 在网络或代理认证回调中承载认证方案、用户名、密码和选项。

## API 速查
| API | 是做什么的 |
|---|---|
| `setUser()` / `setPassword()` | 提供用户名密码。|
| `realm()` | 读取认证域。|
| `method()` | 查询 Basic、Digest、NTLM 等方式。|
| `option()` / `setOption()` | 处理认证扩展选项。|

## 使用场景
连接 `QNetworkAccessManager::authenticationRequired` 或 `proxyAuthenticationRequired`，按域名从安全凭据库取值。

## 常见坑与经验
- 回调中只填凭据，不要异步等待 UI；需要交互认证时预先设计请求队列。
- Basic 认证不是加密，必须经 HTTPS 使用。

## 知识点覆盖
HTTP 认证、代理认证、realm、凭据管理、Basic/Digest、安全。
