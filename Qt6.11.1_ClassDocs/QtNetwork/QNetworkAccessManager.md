# QNetworkAccessManager
> Qt 6.11.1 · Qt Network · 来自 `QNetworkAccessManager`

## 作用定位
`QNetworkAccessManager` 是 Qt 的异步 HTTP 网络会话管理器，负责连接复用、cookie、认证、代理、缓存和请求调度。一个有事件循环的线程通常只需一个长期复用实例。

## API 速查
| API | 是做什么的 |
|---|---|
| `get()` / `head()` | 发起 GET 或 HEAD 请求。|
| `post()` / `put()` / `sendCustomRequest()` | 发起带请求体或自定义方法的请求。|
| `deleteResource()` | 发起 DELETE 请求。|
| `setCookieJar()` | 安装 cookie 管理器。|
| `setCache()` | 安装网络缓存。|
| `setProxy()` | 配置代理。|
| `setTransferTimeout()` | 设置传输超时。|
| `finished(reply)` | 某个请求已结束，成功或失败均会发出。|
| `authenticationRequired()` | 需要 HTTP 认证凭据。|
| `sslErrors()` | 报告 TLS 证书问题。|

## 使用场景
```cpp
auto *reply = manager.get(QNetworkRequest(url));
connect(reply, &QNetworkReply::finished, this, [reply] {
    const QByteArray body = reply->readAll();
    reply->deleteLater();
});
```

## 常见坑与经验
- 不要每个请求创建一个 manager，否则连接池、cookie 和 HTTP/2 复用都失效。
- manager 与 reply 应在同一线程并有事件循环；不能把它当成同步 API。
- `finished()` 不代表 HTTP 2xx，先检查 `reply->error()`、状态码和业务响应体。

## 知识点覆盖
异步 HTTP、连接复用、事件循环、cookie、缓存、认证、TLS、超时。
