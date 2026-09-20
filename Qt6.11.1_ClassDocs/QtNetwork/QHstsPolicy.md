# QHstsPolicy
> Qt 6.11.1 · Qt Network · 来自 `QHstsPolicy`

## 作用定位
`QHstsPolicy` 描述 HTTP Strict Transport Security 规则，将一个主机及可选子域强制升级为 HTTPS。

## API 速查
| API | 是做什么的 |
|---|---|
| `setHost()` | 设置适用主机。|
| `setExpiry()` | 设置策略到期时间。|
| `setIncludesSubDomains()` | 是否覆盖子域。|
| `isExpired()` | 判断策略是否过期。|

## 使用场景
检查或预加载高安全服务的 HSTS 策略。

## 常见坑与经验
- HSTS 是降低降级攻击的机制，不是证书校验的替代。
- 包含子域的策略配置错误可能让未部署 TLS 的子域不可访问。

## 知识点覆盖
HSTS、HTTPS 升级、子域、到期、降级攻击。
