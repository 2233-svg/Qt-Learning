# QSslEllipticCurve
> Qt 6.11.1 · Qt Network · 来自 `QSslEllipticCurve`

## 作用定位
`QSslEllipticCurve` 描述 TLS 使用的椭圆曲线。

## API 速查
| API | 是做什么的 |
|---|---|
| `fromShortName()` | 按常用短名查曲线。|
| `fromLongName()` | 按长名查曲线。|
| `supportedCurves()` | 枚举后端支持曲线。|
| `id()` / `shortName()` | 查询标识。|

## 使用场景
TLS 诊断与合规配置。

## 常见坑与经验
- 支持曲线取决于 TLS 后端与平台，不能假设所有曲线都可用。

## 知识点覆盖
ECDH、椭圆曲线、TLS 后端、密码策略。
