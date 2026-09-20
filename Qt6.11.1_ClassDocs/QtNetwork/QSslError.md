# QSslError
> Qt 6.11.1 · Qt Network · 来自 `QSslError`

## 作用定位
`QSslError` 描述 TLS 证书校验或握手中的一个具体错误。

## API 速查
| API | 是做什么的 |
|---|---|
| `error()` | 返回错误枚举。|
| `certificate()` | 返回相关证书。|
| `errorString()` | 返回诊断文字。|

## 使用场景
记录连接失败的证书链问题并提示用户/运维修复。

## 常见坑与经验
- 生产环境不应以 `ignoreSslErrors()` 绕过错误；应修复主机名、时间、CA 或链配置。

## 知识点覆盖
TLS 校验、证书链、主机名、错误诊断、安全默认值。
