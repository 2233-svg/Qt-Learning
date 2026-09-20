# QOcspResponse
> Qt 6.11.1 · Qt Network · 来自 `QOcspResponse`

## 作用定位
`QOcspResponse` 表示证书在线状态协议响应，用于得知证书是否被吊销或状态未知。

## API 速查
| API | 是做什么的 |
|---|---|
| `certificateStatus()` | 读取 good、revoked、unknown 等状态。|
| `responder()` | 查询响应者信息。|
| `revocationTime()` | 证书吊销时读取时间。|

## 使用场景
高级 TLS 诊断与严格证书状态策略。

## 常见坑与经验
- OCSP 不可达与“证书有效”不是同义；失败策略须明确。

## 知识点覆盖
OCSP、证书吊销、状态验证、失败策略。
