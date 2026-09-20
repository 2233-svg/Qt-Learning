# QNetworkReply
> Qt 6.11.1 · Qt Network · 来自 `QNetworkReply`

## 作用定位
`QNetworkReply` 是一个正在进行或已完成的网络响应 `QIODevice`。它提供响应头、状态码、流式字节、进度、错误和取消能力。

## API 速查
| API | 是做什么的 |
|---|---|
| `readyRead()` | 有新响应字节可读。|
| `readAll()` / `read()` | 读取已缓冲数据。|
| `finished()` | 响应结束。|
| `error()` / `errorString()` | 查询 Qt 网络层错误。|
| `attribute(HttpStatusCodeAttribute)` | 读取 HTTP 状态码。|
| `rawHeader()` / `header()` | 读取响应头。|
| `downloadProgress()` | 观察已收字节和总量。|
| `abort()` | 取消尚未完成的请求。|
| `redirected()` | 通知重定向目标。|

## 使用场景
大文件下载在 `readyRead()` 里增量写文件；小 JSON 响应可在 `finished()` 中 `readAll()` 后解析。

## 常见坑与经验
- `error() == NoError` 仍可能是 HTTP 404/500；HTTP 状态是另一层判断。
- `finished()` 后调用 `deleteLater()`，不要直接 delete 仍在信号调用栈中的 reply。
- 没有 `Content-Length` 时进度总量可能为 `-1`，进度条应显示不确定状态。

## 知识点覆盖
QIODevice、流式响应、网络错误与 HTTP 状态、进度、取消、内存控制。
