# QNetworkReplyWrapper：把一次网络请求包装成 TaskTree 任务

> Qt 6.11.1 · `#include <qnetworkreplywrappertask.h>` · 模块：`Qt6::TaskTree` · 继承：`QObject`

`QNetworkReplyWrapper` 把 `QNetworkAccessManager` 和一次 `QNetworkReply` 的生命周期包装在一个可由 `QCustomTask` 运行的对象里。它解决的是“让 HTTP 请求像 TaskTree 任务一样启动、发进度、结束并报告成功/失败”。

## 使用场景

在 recipe 中下载配置、提交表单、拉取 JSON、上传数据时，可以用 `QNetworkReplyWrapperTask`。setup handler 里配置 manager、request、operation 和数据；done handler 里读取 `reply()` 的结果或错误信息。

它适合一次性请求。若需要复杂重试、认证刷新、流式处理或共享 reply 生命周期，通常应在外层写更明确的任务对象。

## 配置和生命周期

必须在 `start()` 前调用 `setNetworkAccessManager()` 和 `setRequest()`。默认 operation 是 `QNetworkAccessManager::GetOperation`；POST/PUT/CUSTOM 需要设置 data，CUSTOM 还需要设置 verb。

`reply()` 在 `start()` 创建 `QNetworkReply` 后才非空。安全访问窗口是 `started()` 发出之后，到 `done()` 发出之前；`done()` 后 wrapper 会删除 reply，`reply()` 又变回 `nullptr`。析构 wrapper 时如果 reply 仍在运行，会 abort。

## API 速查表

| API | 语义与边界 |
|---|---|
| `QNetworkReplyWrapper(QObject *parent = nullptr)` | 构造网络请求包装器。 |
| `~QNetworkReplyWrapper()` | 若关联 reply 仍运行，会中止它。 |
| `setNetworkAccessManager(QNetworkAccessManager *manager)` | 设置启动时使用的 manager；必需配置。 |
| `setRequest(const QNetworkRequest &request)` | 设置启动时使用的请求；必需配置。 |
| `setOperation(QNetworkAccessManager::Operation)` | 设置 GET/POST/PUT/CUSTOM 等操作；默认 GET。 |
| `setData(const QByteArray &data)` | 设置 PUT、POST、CUSTOM 操作的数据。 |
| `setVerb(const QByteArray &verb)` | 设置 CUSTOM 操作的 HTTP verb。 |
| `start()` | 创建并启动 `QNetworkReply`。 |
| `reply() const` | 返回当前 reply；未启动或 done 后为 `nullptr`。 |
| `started()` | reply 成功创建并启动后发出。 |
| `downloadProgress(qint64, qint64)` | 转发运行中 reply 的下载进度。 |
| `sslErrors(const QList<QSslError> &)` | SSL 可用时转发 reply 的 SSL 错误。 |
| `done(DoneResult)` | reply 完成后发出，表示成功或错误；发出后 reply 将被删除。 |
| `QNetworkReplyWrapperTask` | `QCustomTask<QNetworkReplyWrapper>`，用于 recipe。 |
