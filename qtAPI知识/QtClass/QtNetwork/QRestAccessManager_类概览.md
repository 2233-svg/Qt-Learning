# QRestAccessManager：面向 REST 客户端的请求便捷层

> Qt 6.11.1  
> 头文件：`#include <QRestAccessManager>`  
> 模块：`Qt6::Network`  
> 继承：`QObject -> QRestAccessManager`  
> 类型性质：不拥有底层管理器的 REST 请求包装器

## 它解决什么问题

`QNetworkAccessManager` 已经能完成 HTTP 请求，但常见 REST 客户端还会反复处理几件事：把 JSON 文档序列化成请求体、把 `QVariantMap` 转成 JSON、为不同 HTTP 方法选择相同的完成回调，以及在请求结束时把 `QNetworkReply` 包装成更容易读取状态和正文的 `QRestReply`。

`QRestAccessManager` 就是这一层便捷封装。它持有一个外部传入的 `QNetworkAccessManager` 指针，提供 `get()`、`post()`、`put()`、`patch()`、`deleteResource()`、`head()` 和 `sendCustomRequest()` 等入口，并统一返回 `QNetworkReply *`。它不替代底层 manager 的缓存、Cookie、代理、TLS 和连接复用能力；这些仍然要配置在被包装的 `QNetworkAccessManager` 或 `QNetworkRequest` 上。

类名中的 `AccessManager` 不代表它拥有或管理传入的 manager。构造时传入的 manager 必须在 `QRestAccessManager` 使用期间保持有效，`QRestAccessManager` 析构时不会删除它。

## 实际使用场景

### 1. 用 callback 处理 REST 请求

callback 版本把“请求完成”作为唯一处理入口，网络错误和 HTTP 错误状态都会调用 callback，因此不能只在 callback 被调用这一事实下判断成功：

```cpp
QNetworkAccessManager network;
QRestAccessManager rest(&network);

QNetworkRequest request(QUrl("https://api.example.com/items"));
rest.get(request, this, [this](QRestReply &reply) {
    if (!reply.isSuccess()) {
        qWarning() << reply.errorString() << reply.httpStatus();
        return;
    }

    if (const auto json = reply.readJson())
        consumeJson(*json);
});
```

context 应尽量传入实际拥有 callback 所需状态的 QObject。context 被销毁后，callback 不会再被调用；传 `nullptr` 虽然允许，但会失去这层生命周期保护。

### 2. 用传统信号槽处理回复

每个请求函数仍返回底层 `QNetworkReply *`，所以可以不用 callback，直接连接 `finished()`：

```cpp
QNetworkReply *reply = rest.get(request);
connect(reply, &QNetworkReply::finished, this, [reply] {
    QRestReply restReply(reply);
    if (restReply.isSuccess())
        qInfo() << restReply.readText();
    reply->deleteLater();
});
```

这种方式适合需要连接上传下载进度、`sslErrors()`、`readyRead()` 等底层信号的场景。`QRestReply` 只是访问便利 API，不会接管 `QNetworkReply` 的所有权。

### 3. 发送 JSON、表单映射和文件内容

- `QJsonDocument` 会按 `QJsonDocument::Compact` 格式发送；如果 request 尚未设置 `Content-Type`，会自动设置为 `application/json`。
- `QVariantMap` 会转换为 `QJsonObject`，适合简单的 JSON 对象请求体。
- `QByteArray` 表示调用方已经准备好的原始请求体，内容类型和编码由 request 头决定。
- `QIODevice *` 适合文件或流式上传；设备的生命周期必须覆盖请求发送过程。
- `QHttpMultiPart *` 适合 `multipart/form-data` 或相关多段上传。

```cpp
QVariantMap fields{
    {QStringLiteral("name"), QStringLiteral("Ada")},
    {QStringLiteral("enabled"), true}
};

rest.post(request, fields, this, [](QRestReply &reply) {
    if (reply.isSuccess())
        qInfo() << reply.readBody();
});
```

### 4. 调用非标准 HTTP 方法

服务端提供 `MERGE`、`REPORT` 或其他扩展方法时，用 `sendCustomRequest()` 传入方法名和 `QByteArray`、`QIODevice` 或 `QHttpMultiPart` 数据。方法名应符合服务端和 HTTP 解析器的约定，不要把 URL、查询参数或空格混进 method 参数。

## 关键 API 语义与边界

### manager 的所有权和线程归属

构造函数的 `manager` 是底层通信对象，`networkAccessManager()` 返回同一个指针。`QRestAccessManager` 不拥有它，也不会把它移动到自己的线程。

`QRestAccessManager` 和相关 `QRestReply` 只能在它们所属的线程中使用。不要从其他线程直接调用请求函数或访问 callback 中的回复；应把工作安排到对象线程，或在线程内创建各自的网络对象。

### callback 的时机和有效期

callback 在底层 reply 完成处理时调用，包括处理因网络错误而结束的情况。callback 参数是一个临时的 `QRestReply &`，只在 callback 执行期间有效：

- 不能保存 `QRestReply &` 的引用；
- 需要稍后使用时，可以移动构造另一个 `QRestReply`；
- 也可以先取得 `networkReply()`，再在合适的生命周期内构造新的包装对象；
- 被包装的 `QNetworkReply` 仍按 `QNetworkAccessManager` 的自动删除设置管理。

### “成功”分成两层

`QRestReply::hasError()` 只表示网络或协议层是否出错；服务器返回 `404`、`500` 这类合法 HTTP 响应时，它通常仍为 false。业务判断应使用 `isSuccess()`，它同时要求没有网络错误且 HTTP 状态在 `200..299`。

### 数据重载不是任意组合

无数据操作只有 `deleteResource()`、`head()` 和无数据 `get()`。带数据的重载根据 HTTP 方法限制类型，具体组合如下：

| 方法 | 无数据 | `QByteArray` | `QJsonDocument` | `QVariantMap` | `QIODevice *` | `QHttpMultiPart *` |
| --- | --- | --- | --- | --- | --- | --- |
| `get()` | 支持 | 支持 | 支持 | 不支持 | 支持 | 不支持 |
| `post()` | 不提供 | 支持 | 支持 | 支持 | 支持 | 支持 |
| `put()` | 不提供 | 支持 | 支持 | 支持 | 支持 | 支持 |
| `patch()` | 不提供 | 支持 | 支持 | 支持 | 支持 | 不支持 |
| `head()` | 支持 | 不支持 | 不支持 | 不支持 | 不支持 | 不支持 |
| `deleteResource()` | 支持 | 不支持 | 不支持 | 不支持 | 不支持 | 不支持 |
| `sendCustomRequest()` | 不提供 | 支持 | 不支持 | 不支持 | 支持 | 支持 |

不提供某种重载不是运行时拒绝，而是编译期接口限制。需要发送其他数据类型时先自行序列化为 `QByteArray`，或使用 `QIODevice`。

## API 速查表

### 生命周期和关联对象

| API | 语义 | 边界与注意 |
| --- | --- | --- |
| `explicit QRestAccessManager(QNetworkAccessManager *manager, QObject *parent = nullptr)` | 创建 REST 包装器，指定 parent 和底层 manager。 | `manager` 不转移所有权；使用期间必须保持有效；对象与 manager 应在同一线程使用。 |
| `~QRestAccessManager()` | 销毁包装器。 | 不删除传入的 `QNetworkAccessManager`。 |
| `QNetworkAccessManager *networkAccessManager() const` | 返回被包装的底层 manager。 | 仅返回指针，不创建、不复制、不转移所有权。 |

### 无数据请求

| API | 语义 | 边界与注意 |
| --- | --- | --- |
| `QNetworkReply *deleteResource(const QNetworkRequest &request)` | 发出 HTTP DELETE。 | 无 callback 版本；通过返回的 reply 连接信号并负责其生命周期。 |
| `deleteResource(request, context, callback)` | 发出 HTTP DELETE，并在完成时调用 `void(QRestReply &)` callback。 | callback 也会在网络错误时调用；context 销毁后不再调用。 |
| `QNetworkReply *head(const QNetworkRequest &request)` | 发出 HTTP HEAD。 | 通常只读取响应头，不应假设存在响应正文。 |
| `head(request, context, callback)` | 发出 HTTP HEAD 并使用 REST callback。 | callback 参数只在回调执行期间有效。 |
| `QNetworkReply *get(const QNetworkRequest &request)` | 发出无请求体的 HTTP GET。 | 返回底层 reply。 |
| `get(request, context, callback)` | 发出无请求体的 HTTP GET 并回调。 | context 建议使用拥有业务状态的 QObject。 |

### 带数据的标准方法

| API | 语义 | 边界与注意 |
| --- | --- | --- |
| `get(request, const QByteArray &data)` / callback 重载 | 发送带原始字节数据的 GET。 | GET 请求体是否被服务端接受取决于服务端和协议栈。 |
| `get(request, const QJsonDocument &data)` / callback 重载 | 以紧凑 JSON 形式发送 GET 数据。 | 未设置 `Content-Type` 时自动设置 `application/json`。 |
| `get(request, QIODevice *data)` / callback 重载 | 从设备读取 GET 请求体。 | 设备必须在整个异步请求期间有效、可读。 |
| `post(request, const QByteArray &data)` / callback 重载 | 发送原始字节 POST。 | 内容类型需由 request 头明确设置。 |
| `post(request, const QJsonDocument &data)` / callback 重载 | 发送 JSON POST。 | 使用 Compact 格式；默认补 `application/json`。 |
| `post(request, const QVariantMap &data)` / callback 重载 | 把 map 转为 JSON 对象后发送 POST。 | map 的值必须能按 Qt JSON 规则转换。 |
| `post(request, QIODevice *data)` / callback 重载 | 从设备流式读取 POST 请求体。 | 设备所有权不由该类自动转移。 |
| `post(request, QHttpMultiPart *data)` / callback 重载 | 发送多段 POST 数据。 | 多段对象必须覆盖请求生命周期；通常按 `QNetworkAccessManager` 的 multipart 规则管理。 |
| `put(request, const QByteArray &data)` / callback 重载 | 发送原始字节 PUT。 | request 负责描述内容类型和其他头部。 |
| `put(request, const QJsonDocument &data)` / callback 重载 | 发送 JSON PUT。 | 使用 Compact 格式并按需设置 JSON 类型。 |
| `put(request, const QVariantMap &data)` / callback 重载 | 把 map 转成 JSON 对象后发送 PUT。 | 不是表单编码；需要表单时自行生成对应字节或 multipart。 |
| `put(request, QIODevice *data)` / callback 重载 | 从设备读取 PUT 请求体。 | 异步期间不要提前关闭或销毁设备。 |
| `put(request, QHttpMultiPart *data)` / callback 重载 | 发送多段 PUT 数据。 | 多段对象的生命周期必须覆盖请求。 |
| `patch(request, const QByteArray &data)` / callback 重载 | 发送原始字节 PATCH。 | 服务端必须支持 PATCH。 |
| `patch(request, const QJsonDocument &data)` / callback 重载 | 发送 JSON PATCH。 | 使用 Compact JSON；是否符合 RFC 语义由服务端 API 决定。 |
| `patch(request, const QVariantMap &data)` / callback 重载 | 把 map 转成 JSON 对象后发送 PATCH。 | 只能表达 JSON 对象，不能直接表达 JSON Patch 数组。 |
| `patch(request, QIODevice *data)` / callback 重载 | 从设备读取 PATCH 请求体。 | 设备需保持可读和有效。 |

### 自定义方法

| API | 语义 | 边界与注意 |
| --- | --- | --- |
| `sendCustomRequest(request, const QByteArray &method, const QByteArray &data)` / callback 重载 | 用自定义 HTTP method 和原始字节体发请求。 | method 应是服务端接受的 token；内容类型由 request 设置。 |
| `sendCustomRequest(request, const QByteArray &method, QIODevice *data)` / callback 重载 | 用自定义 method 从设备读取请求体。 | 设备生命周期和线程归属由调用方保证。 |
| `sendCustomRequest(request, const QByteArray &method, QHttpMultiPart *data)` / callback 重载 | 用自定义 method 发送 multipart。 | 适合服务端定义的扩展上传操作；不支持 `QJsonDocument` 直传重载。 |

### callback 形式

| API 形态 | 语义 | 边界与注意 |
| --- | --- | --- |
| `template <typename Functor> ... callback` | 接受可调用对象，包括 lambda 和兼容的成员函数指针。 | callback 必须能接收一个 `QRestReply &`；返回值应为 void。 |
| `const ContextTypeForFunctor<Functor> *context` | 指定 callback 的 QObject 上下文。 | context 被销毁后取消 callback；传 `nullptr` 可用但不推荐。 |
| 所有请求函数的返回值 `QNetworkReply *` | 返回底层异步 reply。 | 即使使用 callback 仍可连接底层信号；不得把 callback 的临时包装对象当作长期对象保存。 |

