# QNetworkRequest
> Qt 6.11.1 · Qt Network · 来自 `QNetworkRequest`

## 作用定位
`QNetworkRequest` 是一次 HTTP 请求的值类型描述，保存 URL、请求头、属性、重定向策略和传输设置；实际 I/O 由 `QNetworkAccessManager` 进行。

## API 速查
| API | 是做什么的 |
|---|---|
| `setUrl()` / `url()` | 设置或读取请求 URL。|
| `setHeader()` | 设置常用已知请求头。|
| `setRawHeader()` | 设置任意原始 HTTP 头。|
| `setAttribute()` | 设置 Qt 特有请求属性。|
| `setTransferTimeout()` | 为本请求设置超时。|
| `setPriority()` | 设置调度优先级。|
| `setSslConfiguration()` | 指定 TLS 配置。|
| `setOriginatingObject()` | 关联发起对象以便追踪。|

## 使用场景
设置 `Content-Type`、`Authorization`、接受格式与重定向策略后传给 manager。

## 常见坑与经验
- URL 中的用户输入要经 `QUrlQuery` 编码；不能用字符串拼接 query。
- 重定向策略与鉴权头的跨域传播要明确，特别是携带 token 时。
- Header 名大小写不敏感，但值的编码和 HTTP 语义不可随意猜测。

## 知识点覆盖
HTTP 请求、URL 编码、请求头、属性、重定向、TLS 配置、值语义。
