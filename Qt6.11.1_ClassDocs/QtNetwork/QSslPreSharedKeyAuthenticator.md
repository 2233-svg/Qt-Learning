# QSslPreSharedKeyAuthenticator
> Qt 6.11.1 · Qt Network · 来自 `QSslPreSharedKeyAuthenticator`

## 作用定位
`QSslPreSharedKeyAuthenticator` 在 TLS-PSK 回调中交换身份提示和预共享密钥。

## API 速查
| API | 是做什么的 |
|---|---|
| `identityHint()` | 读取服务端身份提示。|
| `setIdentity()` | 设置客户端身份。|
| `setPreSharedKey()` | 设置密钥字节。|
| `maximumIdentityLength()` | 查询允许身份长度。|

## 使用场景
封闭设备网络使用预置密钥的 TLS 通信。

## 常见坑与经验
- PSK 的分发、轮换和泄露影响面必须在系统设计层解决；不适合把固定密钥写进客户端。

## 知识点覆盖
TLS-PSK、设备身份、密钥轮换、密钥管理。
