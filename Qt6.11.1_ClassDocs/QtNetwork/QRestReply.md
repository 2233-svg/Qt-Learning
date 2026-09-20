# QRestReply
> Qt 6.11.1 · Qt Network · 来自 `QRestReply`

## 作用定位
`QRestReply` 封装 REST 请求结果，提供 HTTP 状态、网络错误、JSON 和原始响应体的便捷访问。

## API 速查
| API | 是做什么的 |
|---|---|
| `isSuccess()` | 判断请求是否被视为成功。|
| `networkReply()` | 获取底层 `QNetworkReply`。|
| `readJson()` | 读取并解析 JSON 文档。|
| `readBody()` | 读取原始响应体。|
| `httpStatus()` | 读取 HTTP 状态信息。|
| `error()` | 读取网络/REST 错误。|

## 使用场景
完成回调中先验证成功与状态，再读 JSON；解析失败时记录响应片段和服务端追踪 ID。

## 常见坑与经验
- body 是一次性流，`readJson()` 后不能假设还能再次完整 `readBody()`。
- 成功 HTTP 状态不保证 JSON 结构符合业务协议，必须验证字段。

## 知识点覆盖
REST 响应、JSON 解析、一次性读取、状态码、业务校验、错误诊断。
