# QRestReply：REST 响应的状态与正文便捷访问器

> Qt 6.11.1  
> 头文件：`#include <QRestReply>`  
> 模块：`Qt6::Network`  
> 继承：无  
> 类型性质：不可复制、可移动的轻量响应包装对象

## 它解决什么问题

`QNetworkReply` 提供了完整的异步网络设备接口，但 REST 客户端最常见的读取动作通常只是三类：判断网络和 HTTP 是否成功、读取整个响应体、把响应体解析为 JSON 或文本。`QRestReply` 把这些动作收拢为一组小而明确的函数。

它包装一个现有的 `QNetworkReply *`，不创建新的网络请求，也不拥有被包装 reply。它本身不是 `QObject`，没有信号槽和事件循环；网络生命周期、自动删除和异步完成时机仍由 `QNetworkAccessManager`/`QNetworkReply` 决定。

## 实际使用场景

### 1. 在 `finished()` 中统一判断结果

```cpp
QNetworkReply *reply = manager->get(request);
connect(reply, &QNetworkReply::finished, this, [reply] {
    QRestReply rest(reply);

    if (!rest.isSuccess()) {
        qWarning() << "network:" << rest.errorString()
                   << "HTTP:" << rest.httpStatus();
        reply->deleteLater();
        return;
    }

    qInfo() << rest.readText();
    reply->deleteLater();
});
```

`isSuccess()` 同时检查网络层错误和 HTTP 状态。服务器返回 `404` 或 `500` 是一个成功收到的 HTTP 响应，不属于 `hasError()` 的网络错误，但 `isSuccess()` 会返回 false。

### 2. 读取 JSON 并保留解析错误

```cpp
QJsonParseError parseError;
if (const auto json = rest.readJson(&parseError)) {
    useJson(*json);
} else {
    qWarning() << parseError.errorString();
}
```

`readJson()` 返回 `std::optional<QJsonDocument>`。空 optional 表示无法得到有效 JSON 文档，可能是正文格式错误，也可能是底层 reply 不再可用。需要诊断格式时传入 `QJsonParseError *`。

### 3. 在 callback 中临时使用

`QRestAccessManager` 的 callback 参数是临时 `QRestReply &`：

```cpp
rest.get(request, this, [this](QRestReply &reply) {
    if (reply.isSuccess()) {
        const QByteArray body = reply.readBody();
        emit loaded(body);
    }
});
```

如果需要在 callback 返回后继续持有包装状态，应移动构造另一个 `QRestReply`；但仍要确保底层 `QNetworkReply` 不会在使用前被自动删除。

## 关键 API 语义与边界

### 不拥有 reply，且 `QPointer` 会自动失效

构造 `QRestReply` 只记录被包装的 `QNetworkReply`。析构包装对象不会删除 reply；反过来，如果 reply 先被销毁，包装器内部指针会变为空，后续查询应按无效底层对象处理。

因此，最稳妥的用法是在 `finished()` 槽或 `QRestAccessManager` callback 中立即消费数据，并按 manager 的自动删除设置安排生命周期。不要把 `networkReply()` 裸指针长期缓存。

### 正文读取会消耗设备

`readBody()`、`readJson()` 和 `readText()` 都是读取操作，不是对已经保存字符串的重复查询。通常它们会从底层 reply 的当前位置读取剩余内容；调用其中一个后，再调用另一个可能只能得到剩余字节或空内容。

若需要多种表示，先调用一次 `readBody()` 保存 `QByteArray`，再自行转换或解析。

### HTTP 状态为 0 的含义

`httpStatus()` 在 HTTP 状态行尚未收到或底层回复不提供 HTTP 状态时返回 `0`。不要把 `0` 解释为服务器返回的正式 HTTP 状态码，也不要只以 `httpStatus() == 200` 作为所有成功响应的条件；`204`、`201` 等 2xx 状态也属于成功。

### `readText()` 的编码边界

HTTP 并不保证所有正文都是 UTF-8。`readText()` 适合服务端和接口约定为 UTF-8 的 REST 文本；如果服务端声明了其他字符集，或正文是二进制数据，应使用 `readBody()` 并根据协议头自行解码。不要把 `readText()` 当作二进制安全 API。

## API 速查表

### 构造、移动和交换

| API | 语义 | 边界与注意 |
| --- | --- | --- |
| `explicit QRestReply(QNetworkReply *reply)` | 用已有网络 reply 初始化包装器。 | 不取得所有权；reply 的生命周期仍由网络管理器定义。 |
| `QRestReply(QRestReply &&other) noexcept` | 移动构造包装器。 | `other` 被置于可析构但不应继续当作原响应使用的状态。 |
| `QRestReply &operator=(QRestReply &&other) noexcept` | 移动赋值。 | 原对象的包装状态被替换；不支持拷贝赋值。 |
| `~QRestReply() noexcept` | 销毁包装对象。 | 不删除底层 `QNetworkReply`。 |
| `void swap(QRestReply &other) noexcept` | 交换两个包装器的底层指针和内部状态。 | 只交换包装状态，不交换或删除网络对象。 |
| `Q_DECLARE_SHARED(QRestReply)` | 让 Qt 容器和共享类型工具识别其共享语义。 | 不等于可复制；类本身仍通过 `Q_DISABLE_COPY` 禁止拷贝构造和拷贝赋值。 |

### 底层 reply 和状态

| API | 语义 | 边界与注意 |
| --- | --- | --- |
| `QNetworkReply *networkReply() const` | 返回被包装的底层 reply。 | 可能为空或随后失效；不转移所有权。 |
| `bool hasError() const` | 判断是否发生网络或协议层错误。 | HTTP `4xx/5xx` 本身通常不算网络错误。 |
| `QNetworkReply::NetworkError error() const` | 返回底层网络错误码。 | 没有错误时是 `NoError`；不能代替 HTTP 状态判断。 |
| `QString errorString() const` | 返回人类可读的网络错误描述。 | 服务器合法返回的 HTTP 错误状态不一定有网络错误文本。 |
| `int httpStatus() const` | 返回收到的 HTTP 状态码。 | 状态行不可用时返回 `0`。 |
| `bool isHttpStatusSuccess() const` | 判断状态码是否在 `200..299`。 | 只检查 HTTP 状态，不检查网络/协议错误。 |
| `bool isSuccess() const` | 同时要求无底层错误且 HTTP 状态为 2xx。 | REST 客户端通常优先使用此函数。 |

### 读取正文

| API | 语义 | 边界与注意 |
| --- | --- | --- |
| `QByteArray readBody()` | 读取收到的正文。 | 会消耗底层 reply 的可读数据；适合二进制和需要自行解码的内容。 |
| `std::optional<QJsonDocument> readJson(QJsonParseError *error = nullptr)` | 读取正文并解析成 JSON 文档。 | 解析失败返回空 optional；可通过 error 获取解析错误；读取位置会前进。 |
| `QString readText()` | 读取正文并转换为文本。 | 只适合协议约定的文本编码；读取位置会前进。 |

### 调试输出

| API | 语义 | 边界与注意 |
| --- | --- | --- |
| `QDebug operator<<(QDebug debug, const QRestReply &reply)` | 把包装器状态写入调试流。 | 用于诊断，不应依赖输出文本作为稳定协议。 |

