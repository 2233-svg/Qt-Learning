# QMessageAuthenticationCode
> Qt 6.11.1 · Qt Core · 来自 `QMessageAuthenticationCode`

## 作用定位
`QMessageAuthenticationCode` 计算 HMAC：使用共享密钥和哈希算法验证消息完整性与持钥方身份。

## API 速查
| API | 是做什么的 |
|---|---|
| 构造函数 `(algorithm, key)` | 选择哈希算法并设置密钥。|
| `setKey()` | 更换 HMAC 密钥。|
| `addData()` | 增量加入待认证消息。|
| `result()` | 取得认证码。|
| `reset()` | 复位计算状态。|
| `hash(message, key, algorithm)` | 一次性计算 HMAC。|

## 使用场景
验证 webhook、请求签名、设备消息完整性或带共享密钥的协议包。

## 常见坑与经验
- HMAC 只验证完整性与持钥身份，不提供加密保密性。
- 比较认证码时应使用常量时间比较，避免时序泄露。
- 密钥必须来自安全存储与轮换体系，不能硬编码到客户端二进制。
- 认证的原始字节序列必须明确，JSON 重新格式化后签名通常会改变。

## 知识点覆盖
HMAC、消息认证、密钥管理、常量时间比较、签名规范化、完整性。
