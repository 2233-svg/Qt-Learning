# QDnsTlsAssociationRecord
> Qt 6.11.1 · Qt Network · 来自 `QDnsTlsAssociationRecord`

## 作用定位
`QDnsTlsAssociationRecord` 表示 TLSA/DANE 记录，携带 TLS 证书或公钥关联信息。

## API 速查
| API | 是做什么的 |
|---|---|
| `certificateUsage()` | 说明关联的证书使用方式。|
| `selector()` | 选择整张证书或公钥信息。|
| `matchingType()` | 说明原始或哈希匹配方式。|
| `value()` | 返回关联数据。|
| `timeToLive()` | 返回 TTL。|

## 使用场景
支持 DNSSEC/DANE 的邮件或专用服务验证链。

## 常见坑与经验
- TLSA 的安全价值依赖 DNSSEC 验证；普通未验证 DNS 查询不能提供同等级信任。
- 它不是替代通用 HTTPS 证书校验的简单开关。

## 知识点覆盖
TLSA、DANE、DNSSEC、证书关联、信任链。
