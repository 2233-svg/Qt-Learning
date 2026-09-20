# QNetworkCookie
> Qt 6.11.1 · Qt Network · 来自 `QNetworkCookie`

## 作用定位
`QNetworkCookie` 表示一个 HTTP cookie，包括名称、值、域、路径、过期、Secure、HttpOnly 与 SameSite 属性。

## API 速查
| API | 是做什么的 |
|---|---|
| `parseCookies()` | 解析 Set-Cookie 头。|
| `toRawForm()` | 序列化为 HTTP 头文本。|
| `setDomain()` / `setPath()` | 设置作用域。|
| `setExpirationDate()` | 设置过期时间。|
| `setSecure()` | 限制仅 HTTPS 发送。|
| `setHttpOnly()` | 禁止脚本层访问。|
| `setSameSitePolicy()` | 设置跨站发送策略。|

## 使用场景
检查服务器下发 cookie，或实现持久 cookie jar。

## 常见坑与经验
- 不要把 session cookie 明文写入日志或不加密的配置文件。
- Domain/Path/SameSite 配错会造成“登录偶尔失效”，不是 Qt 自动修复的问题。

## 知识点覆盖
Cookie、作用域、Secure、HttpOnly、SameSite、会话安全。
