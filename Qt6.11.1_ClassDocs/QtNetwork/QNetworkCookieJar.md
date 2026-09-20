# QNetworkCookieJar
> Qt 6.11.1 · Qt Network · 来自 `QNetworkCookieJar`

## 作用定位
`QNetworkCookieJar` 管理 `QNetworkAccessManager` 的 cookie 存取与 URL 匹配规则。

## API 速查
| API | 是做什么的 |
|---|---|
| `cookiesForUrl()` | 返回某请求应携带的 cookie。|
| `setCookiesFromUrl()` | 接收响应下发 cookie。|
| `insertCookie()` / `deleteCookie()` | 手动管理一个 cookie。|
| `allCookies()` / `setAllCookies()` | 读取或替换 jar 内容。|

## 使用场景
子类化实现跨启动持久会话，或对第三方登录域施加额外 cookie 策略。

## 常见坑与经验
- jar 安装给 manager 后归 manager 所有。
- 持久化前过滤 session、过期和安全属性；不要把所有 cookie 无差别保存。

## 知识点覆盖
Cookie jar、URL 匹配、持久会话、所有权、安全存储。
