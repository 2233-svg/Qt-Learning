# QSslCertificateExtension
> Qt 6.11.1 · Qt Network · 来自 `QSslCertificateExtension`

## 作用定位
`QSslCertificateExtension` 表示 X.509 的单个扩展，如 Key Usage、Basic Constraints、Subject Alternative Name。

## API 速查
| API | 是做什么的 |
|---|---|
| `oid()` | 读取扩展对象标识。|
| `value()` | 读取扩展值。|
| `isCritical()` | 判断扩展是否为关键扩展。|
| `isSupported()` | 判断 Qt 是否能解释该扩展。|

## 使用场景
审查 CA 属性、SAN 或密钥用途。

## 常见坑与经验
- 未识别的关键扩展不应被当作可忽略信息。

## 知识点覆盖
X.509 扩展、OID、Key Usage、SAN、关键扩展。
