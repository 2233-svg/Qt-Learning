# QSslCertificate
> Qt 6.11.1 · Qt Network · 来自 `QSslCertificate`

## 作用定位
`QSslCertificate` 表示 X.509 证书，提供主题、签发者、有效期、扩展、公钥和序列化访问。

## API 速查
| API | 是做什么的 |
|---|---|
| `fromData()` / `fromPath()` | 从 PEM/DER 数据或文件读取证书。|
| `subjectInfo()` / `issuerInfo()` | 读取主体和签发者字段。|
| `effectiveDate()` / `expiryDate()` | 读取有效期。|
| `publicKey()` | 取得证书公钥。|
| `extensions()` | 读取 X.509 扩展。|
| `verify()` | 验证证书链与主机名相关问题。|

## 使用场景
检查企业证书、加载客户端证书、展示连接安全详情。

## 常见坑与经验
- 仅查看 CN 不够，主机名验证应依赖 SAN 与完整链校验。

## 知识点覆盖
X.509、证书链、SAN、有效期、公钥、PEM/DER。
