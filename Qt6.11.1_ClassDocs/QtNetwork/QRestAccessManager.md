# QRestAccessManager
> Qt 6.11.1 · Qt Network · 来自 `QRestAccessManager`

## 作用定位
`QRestAccessManager` 是 `QNetworkAccessManager` 之上的 REST 便捷层，面向 JSON/REST 请求构建与 `QRestReply` 结果处理。

## API 速查
| API | 是做什么的 |
|---|---|
| `get()` | 发起 REST GET。|
| `post()` / `put()` / `patch()` | 发起带 JSON 或 body 的 REST 写操作。|
| `deleteResource()` | 发起 REST DELETE。|
| `setAutoDeleteReplies()` | 控制 reply 自动回收。|
| `networkAccessManager()` | 访问底层网络 manager。|

## 使用场景
JSON API 客户端：用 request factory 统一认证与根 URL，用 REST manager 发请求，并在完成回调解析 JSON。

## 常见坑与经验
- 它不替代 HTTP 语义校验；仍需处理 401、409、429、5xx 和业务错误 JSON。
- 自动删除 reply 时，不要把 `QRestReply *` 保存到异步队列后再访问。

## 知识点覆盖
REST、JSON、异步回调、自动删除、HTTP 状态、客户端封装。
