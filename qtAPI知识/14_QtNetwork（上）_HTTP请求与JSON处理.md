# Qt Network（上）：HTTP 请求与 JSON 处理

> 适用版本：Qt 6.11.1  
> 所属模块：Qt Network  
> 核心类型：`QNetworkAccessManager`、`QNetworkRequest`、`QNetworkReply`、`QUrl`、`QUrlQuery`、`QJsonDocument`

Qt 的 HTTP API 是异步的。调用 `get()` 或 `post()` 只表示请求已经交给网络层，返回的 `QNetworkReply` 会在未来通过信号报告进度、错误和完成。

```text
构造 QNetworkRequest
        ↓
QNetworkAccessManager::get/post/put/deleteResource
        ↓ 立即返回
QNetworkReply（一个请求的进行中状态和响应数据）
        ↓
readyRead / progress / errorOccurred / finished
```

## 1. 构建配置

```cmake
find_package(Qt6 REQUIRED COMPONENTS Network)
target_link_libraries(mytarget PRIVATE Qt6::Network)
```

若程序同时使用 Widgets：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets Network)
target_link_libraries(mytarget PRIVATE Qt6::Widgets Qt6::Network)
```

## 2. 三个核心对象

### 2.1 QNetworkAccessManager

它保存共同配置并管理连接复用、代理、缓存、Cookie 和认证。通常一个应用或一个明确网络上下文使用一个长期存在的实例就够了：

```cpp
class ApiClient : public QObject
{
    Q_OBJECT

public:
    explicit ApiClient(QObject *parent = nullptr)
        : QObject(parent), m_manager(new QNetworkAccessManager(this)) {}

private:
    QNetworkAccessManager *m_manager;
};
```

不要每次请求都创建一个 manager。那会失去连接复用和统一配置，还让生命周期更难管理。

### 2.2 QNetworkRequest

描述请求：URL、Header、属性、传输超时、重定向策略等。它是值类型，可在发送前配置。

### 2.3 QNetworkReply

表示一次具体操作，同时是可读 `QIODevice`。它包含：

- 响应正文；
- HTTP 状态码和响应 Header；
- 网络错误；
- 原始请求和最终 URL；
- 下载/上传进度；
- 取消操作 `abort()`。

Reply 不是“返回数据本身”，而是整个异步操作的句柄。

## 3. 最小可用 GET

```cpp
#include <QCoreApplication>
#include <QDebug>
#include <QNetworkAccessManager>
#include <QNetworkReply>
#include <QNetworkRequest>
#include <QUrl>

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);

    QNetworkAccessManager manager;
    QNetworkRequest request(QUrl("https://httpbin.org/get"));
    request.setHeader(QNetworkRequest::UserAgentHeader,
                      QStringLiteral("QtApiNotes/1.0"));

    QNetworkReply *reply = manager.get(request);

    QObject::connect(reply, &QNetworkReply::finished,
                     &app, [reply, &app] {
        if (reply->error() == QNetworkReply::NoError)
            qDebug().noquote() << reply->readAll();
        else
            qWarning() << reply->error() << reply->errorString();

        reply->deleteLater();
        app.quit();
    });

    return app.exec();
}
```

关键点：

1. manager 活到请求结束之后。
2. 连接的是这一个 Reply 的 `finished`，并发请求不会混淆。
3. 完成时先读取数据和元信息，再 `deleteLater()`。
4. 不在 `finished` 槽中直接 `delete reply`。
5. 没有事件循环，请求信号通常无法正常投递。

## 4. URL 与查询参数

不要自己字符串拼接 `?`、`&` 和百分号编码：

```cpp
QUrl url("https://api.example.com/search");
QUrlQuery query;
query.addQueryItem(QStringLiteral("q"), QStringLiteral("Qt 网络"));
query.addQueryItem(QStringLiteral("page"), QString::number(2));
url.setQuery(query);

QNetworkRequest request(url);
```

`QUrl` / `QUrlQuery` 能表达 URL 各组成部分并处理编码边界。用户输入若是本地路径，不应直接当 URL；使用 `QUrl::fromLocalFile()`。

### 4.1 路径片段与查询值不是同一种编码

```text
https://host.example/users/alice?sort=name
                     └ 路径 ┘ └ 查询 ┘
```

不要把已百分号编码的字符串再次编码，也不要对整个 URL 使用表单编码规则。尽量把结构交给 `QUrl` API。

## 5. Request Header

常见已知 Header 可用类型化 API：

```cpp
request.setHeader(QNetworkRequest::ContentTypeHeader,
                  QStringLiteral("application/json"));
request.setHeader(QNetworkRequest::UserAgentHeader,
                  QStringLiteral("MyApp/2.3"));
```

自定义或未类型化 Header：

```cpp
request.setRawHeader("Authorization", "Bearer " + accessToken);
request.setRawHeader("Accept", "application/json");
request.setRawHeader("X-Request-Id", requestId.toUtf8());
```

Bearer token 属于敏感信息：不要写入日志、错误对话框或源码。生产中从受保护凭据存储读取，并限定日志脱敏规则。

## 6. 完成不等于业务成功

`finished()` 只表示网络操作结束，不表示 HTTP 2xx，更不表示响应 JSON 符合业务规则。

至少分四层判断：

```text
传输层：reply->error() 是否 NoError
HTTP 层：status code 是否属于预期范围
格式层：Content-Type / JSON 是否可解析
业务层：字段、版本、错误码是否有效
```

### 6.1 读取状态码

```cpp
const int status = reply->attribute(
    QNetworkRequest::HttpStatusCodeAttribute).toInt();
const QByteArray reason = reply->attribute(
    QNetworkRequest::HttpReasonPhraseAttribute).toByteArray();

if (status < 200 || status >= 300)
    qWarning() << "HTTP" << status << reason;
```

HTTP 404/500 常会同时映射为 `QNetworkReply::NetworkError`，但代码仍应读取状态码，因为服务端响应、传输失败和协议错误的处理策略不同。

### 6.2 错误也可能有响应正文

API 往往在 4xx/5xx 返回 JSON 错误详情。完成时可以读取正文，但要限制日志大小并避免泄漏敏感内容：

```cpp
const QByteArray body = reply->readAll();
if (reply->error() != QNetworkReply::NoError) {
    parseServerError(body);
    return;
}
```

## 7. JSON GET：从响应到强业务结构

```cpp
struct User
{
    qint64 id = 0;
    QString name;
};

void ApiClient::fetchUser(qint64 id)
{
    QUrl url(QStringLiteral("https://api.example.com/users/%1").arg(id));
    QNetworkRequest request(url);
    request.setRawHeader("Accept", "application/json");

    QNetworkReply *reply = m_manager->get(request);
    connect(reply, &QNetworkReply::finished, this, [this, reply] {
        const auto cleanup = qScopeGuard([reply] { reply->deleteLater(); });

        if (reply->error() != QNetworkReply::NoError) {
            emit requestFailed(reply->errorString());
            return;
        }

        const int status = reply->attribute(
            QNetworkRequest::HttpStatusCodeAttribute).toInt();
        if (status != 200) {
            emit requestFailed(QStringLiteral("HTTP %1").arg(status));
            return;
        }

        QJsonParseError parseError;
        const QJsonDocument document = QJsonDocument::fromJson(
            reply->readAll(), &parseError);
        if (parseError.error != QJsonParseError::NoError
            || !document.isObject()) {
            emit requestFailed(QStringLiteral("响应 JSON 无效：%1")
                               .arg(parseError.errorString()));
            return;
        }

        const QJsonObject object = document.object();
        if (!object.value("id").isDouble()
            || !object.value("name").isString()) {
            emit requestFailed(QStringLiteral("响应字段缺失或类型错误"));
            return;
        }

        User user;
        user.id = object.value("id").toInteger();
        user.name = object.value("name").toString();
        emit userReceived(user.id, user.name);
    });
}
```

`qScopeGuard` 确保每个提前 `return` 都会安排 Reply 删除。若不用它，也应让所有完成路径显式调用 `deleteLater()`。

### 7.1 JSON 数字精度

Qt 6 的 `QJsonValue` 可以在内部保留 64 位整数，并用 `toInteger()` 无损读取；但许多 JavaScript 客户端会把 JSON number 当作双精度浮点数，超过 2^53 后可能丢精度。面向多语言客户端的协议若传输超大 ID，更稳妥的做法仍是使用字符串并严格转换。

### 7.2 不要把 QJsonObject 当领域模型

在网络边界验证字段并转换为 `User`、`Order` 等业务结构。这样 UI 不必到处写字符串键名，协议变化也集中在解析层。

## 8. POST JSON

```cpp
void ApiClient::createUser(const QString &name)
{
    QNetworkRequest request(
        QUrl("https://api.example.com/users"));
    request.setHeader(QNetworkRequest::ContentTypeHeader,
                      QStringLiteral("application/json"));
    request.setRawHeader("Accept", "application/json");

    QJsonObject object;
    object.insert("name", name);
    const QByteArray body = QJsonDocument(object).toJson(
        QJsonDocument::Compact);

    QNetworkReply *reply = m_manager->post(request, body);
    connect(reply, &QNetworkReply::finished, this, [this, reply] {
        const QByteArray response = reply->readAll();
        const int status = reply->attribute(
            QNetworkRequest::HttpStatusCodeAttribute).toInt();

        if (reply->error() == QNetworkReply::NoError
            && status >= 200 && status < 300) {
            emit userCreated(response);
        } else {
            emit requestFailed(reply->errorString());
        }
        reply->deleteLater();
    });
}
```

GET、POST、PUT、PATCH 的核心差异属于 HTTP 语义，不是 Qt 语法：

| 方法 | 常见语义 | 通常是否幂等 |
|---|---|---|
| GET | 读取资源 | 是 |
| POST | 新建资源或执行命令 | 通常否 |
| PUT | 整体创建/替换指定资源 | 是 |
| PATCH | 部分更新 | 取决于协议 |
| DELETE | 删除指定资源 | 通常按语义幂等 |

自定义方法可用 `sendCustomRequest()`；不要因为 API 都能发就忽略服务端约定。

## 9. 请求体的生命周期

使用 `QByteArray` 重载时，Qt 可以管理传入数据的副本语义，使用简单。

使用 `QIODevice *` 重载时：

```cpp
QFile *file = new QFile(path, replyOwner);
file->open(QIODevice::ReadOnly);
QNetworkReply *reply = m_manager->post(request, file);
```

设备必须已打开可读，并一直存活到 `finished()`。不能把局部栈上的 `QFile` 指针交给一个异步请求后立即离开作用域。

## 10. 上传 multipart/form-data

```cpp
#include <QFile>
#include <QHttpMultiPart>
#include <QHttpPart>

auto *file = new QFile(filePath);
if (!file->open(QIODevice::ReadOnly)) {
    delete file;
    return;
}

auto *multiPart = new QHttpMultiPart(QHttpMultiPart::FormDataType);

QHttpPart textPart;
textPart.setHeader(QNetworkRequest::ContentDispositionHeader,
                   QVariant("form-data; name=\"title\""));
textPart.setBody(title.toUtf8());
multiPart->append(textPart);

QHttpPart filePart;
filePart.setHeader(QNetworkRequest::ContentDispositionHeader,
                   QVariant("form-data; name=\"file\"; filename=\"upload.bin\""));
filePart.setBodyDevice(file);
file->setParent(multiPart);
multiPart->append(filePart);

QNetworkRequest request(QUrl("https://api.example.com/upload"));
QNetworkReply *reply = m_manager->post(request, multiPart);
multiPart->setParent(reply);

connect(reply, &QNetworkReply::finished, this, [reply] {
    // 读取结果；删除 reply 时会级联删除 multiPart 和 file
    reply->deleteLater();
});
```

所有权链：

```text
reply
└─ multiPart
   └─ file
```

必须在调用 `post()` 后才能把 multipart 的 parent 设置为返回的 reply。文件名和 Content-Disposition 若来自用户输入，还应正确转义并避免 Header 注入。

## 11. 下载模式：小响应和大文件不同

### 11.1 小响应在 finished 后 readAll

适合 JSON、小配置、小图片：

```cpp
connect(reply, &QNetworkReply::finished, this, [reply] {
    const QByteArray all = reply->readAll();
    reply->deleteLater();
});
```

数据会缓存在 Reply 中，文件越大，内存占用越高。

### 11.2 大文件按 readyRead 流式写入

```cpp
auto *file = new QSaveFile(targetPath, reply);
if (!file->open(QIODevice::WriteOnly)) {
    reply->abort();
    reply->deleteLater();
    return;
}

connect(reply, &QIODevice::readyRead, file, [reply, file] {
    const QByteArray chunk = reply->readAll();
    if (file->write(chunk) != chunk.size())
        reply->abort();
});

connect(reply, &QNetworkReply::finished, file, [reply, file] {
    file->write(reply->readAll());
    if (reply->error() == QNetworkReply::NoError) {
        if (!file->commit())
            qWarning() << file->errorString();
    } else {
        file->cancelWriting();
    }
    reply->deleteLater();
});
```

`QSaveFile` 先写临时文件，成功 `commit()` 才替换目标，避免失败时留下半个文件。

生产代码还要处理磁盘写入失败状态，不能仅 `abort()` 后继续在 finished 中误判提交。

## 12. 进度信号

```cpp
connect(reply, &QNetworkReply::downloadProgress,
        this, [](qint64 received, qint64 total) {
    if (total > 0)
        qDebug() << received * 100 / total << '%';
    else
        qDebug() << "已接收" << received << "字节，总量未知";
});
```

`total` 可能是 `-1`，例如服务端未提供 Content-Length 或使用流式传输。此时 UI 应显示不确定进度，而不是除法计算百分比。

进度信号的数值可能与底层实际网络字节略有不同，例如协议压缩、缓存和缓冲会影响观察结果。

## 13. Reply 信号如何分工

| 信号 | 用途 |
|---|---|
| `readyRead()` | 新正文数据可读，适合流式处理 |
| `downloadProgress()` | 下载进度 |
| `uploadProgress()` | 上传进度 |
| `metaDataChanged()` | 响应 Header/元信息改变 |
| `redirected()` | 收到重定向信息 |
| `errorOccurred()` | 网络错误已发生，可立即更新状态 |
| `sslErrors()` | TLS 证书或握手验证问题 |
| `finished()` | 统一收尾、读取剩余数据和释放 Reply |

`errorOccurred()` 后通常仍会有 `finished()`。若两个槽都弹错误对话框，用户会看到两次。推荐：errorOccurred 记录状态，finished 做一次统一收尾。

## 14. 每请求连接与 Manager 全局 finished

两种写法都合法：

```cpp
connect(reply, &QNetworkReply::finished, ...);
```

```cpp
connect(m_manager, &QNetworkAccessManager::finished,
        this, &ApiClient::handleFinished);
```

每 Reply 连接更容易捕获该操作上下文，例如用户 ID 和目标文件。Manager 全局连接适合统一日志、指标或通用响应管道。若两边都处理正文和删除，容易重复消费或重复清理，应明确唯一所有者。

## 15. Lambda 捕获与接收上下文

```cpp
connect(reply, &QNetworkReply::finished,
        this, [this, reply] { /* ... */ });
```

这里的 `this` 是 context object。`this` 销毁时连接会自动断开，lambda 不会再调用已销毁对象。但 Reply 仍可能继续运行，通常应让 client/manager 销毁时一起取消其子 Reply，或显式管理在途请求。

避免按引用捕获即将离开作用域的局部变量：

```cpp
QString userId = ...;
connect(reply, &QNetworkReply::finished, this,
        [reply, userId] { /* 按值捕获 */ });
```

## 16. QRestAccessManager：面向 REST 的便捷层

Qt 6 提供 `QRestAccessManager` 和 `QRestReply`，在已有 `QNetworkAccessManager` 上封装回调、JSON body 和常用成功判断：

```cpp
QNetworkAccessManager networkManager;
QRestAccessManager restManager(&networkManager);

QNetworkRequest request(QUrl("https://api.example.com/users/42"));
restManager.get(request, &networkManager,
    [](QRestReply &reply) {
        if (!reply.isSuccess()) {
            qWarning() << reply.errorString();
            return;
        }
        const auto json = reply.readJson();
        // 继续验证 JSON 结构
    });
```

它适合大量 JSON REST API，可以减少重复样板代码；它不是新的传输栈，底层仍依赖 `QNetworkAccessManager`。文件流式下载、特殊协议和细粒度 Reply 控制仍常直接使用 QNAM。

## 17. API Client 的分层

推荐边界：

```text
UI
  ↓ 调用 loadUsers()
业务服务
  ↓ 需要用户数据
ApiClient
  ├─ 构造 URL/Request
  ├─ 发送与管理 Reply
  ├─ 验证 HTTP/JSON
  └─ 转换为业务结构
  ↓
QNetworkAccessManager
```

UI 不应直接解析 JSON 和判断状态码。这样网络错误、鉴权、重试和协议升级可集中处理，也便于用假实现测试 UI。

## 18. 常见错误

### 18.1 每次请求创建局部 Manager

函数返回后 manager 被销毁，请求也随之终止。Manager 应长期存在。

### 18.2 忘记释放 Reply

每次请求泄漏一个 QObject 和相关缓冲。完成后调用 `deleteLater()`，或统一配置自动删除并确保不在之后访问它。

### 18.3 finished 中直接 delete

Reply 仍处于信号分发栈中。使用 `deleteLater()`。

### 18.4 只检查 `error()`，不检查状态码和 JSON

传输成功不代表业务成功。至少逐层验证网络、HTTP、格式和字段。

### 18.5 大文件使用 readAll

会让整个响应进入内存。使用 `readyRead()` 流式写入并限制缓冲。

### 18.6 捕获局部变量引用

异步完成时局部变量早已销毁。对小值按值捕获，复杂上下文放在有生命周期的请求对象中。

### 18.7 在日志中打印 Authorization 和完整响应

可能泄漏 token、个人数据和服务端内部信息。日志默认脱敏、截断，并按环境控制级别。

## 19. API 速查

| API | 用途 |
|---|---|
| `QNetworkAccessManager::get()` | 发起 GET |
| `post()` / `put()` | 上传请求体 |
| `deleteResource()` | 发起 DELETE |
| `sendCustomRequest()` | 自定义 HTTP 方法 |
| `QNetworkRequest::setHeader()` | 设置已知类型 Header |
| `setRawHeader()` | 设置原始 Header |
| `HttpStatusCodeAttribute` | 读取 HTTP 状态码 |
| `QNetworkReply::readAll()` | 读取当前已缓冲正文 |
| `readyRead()` | 流式读取正文 |
| `error()` / `errorString()` | 查询传输/协议错误 |
| `abort()` | 取消进行中的操作 |
| `deleteLater()` | 在安全时机销毁 Reply |
| `QJsonDocument::fromJson()` | 解析 JSON |
| `QHttpMultiPart` | multipart/form-data 上传 |
| `QRestAccessManager` | REST/JSON 便捷封装 |

## 20. 自测题

1. 为什么通常不应每个请求创建一个 QNetworkAccessManager？
2. `get()` 返回时响应是否已经完成？
3. 为什么要在 finished 中使用 `deleteLater()`？
4. `finished()` 是否代表 HTTP 请求成功？
5. 如何读取 HTTP 状态码？
6. 为什么查询参数应通过 `QUrlQuery` 构造？
7. 使用 `QIODevice *` 作为上传 body 时，设备要存活多久？
8. 大文件为什么应使用 `readyRead()`？
9. `errorOccurred()` 后还会不会有 `finished()`？
10. `QRestAccessManager` 是否替换了底层 QNetworkAccessManager？

## 21. 参考答案

1. 长期 manager 才能复用连接并集中管理代理、缓存、Cookie、认证和生命周期。
2. 没有；它立即返回代表在途操作的 `QNetworkReply`。
3. Reply 还处在信号调用栈中，延迟删除可避免当前分发过程中对象失效。
4. 不代表。还要检查网络错误、HTTP 状态码、内容格式和业务字段。
5. 读取 `QNetworkRequest::HttpStatusCodeAttribute`。
6. 它正确表达查询结构并处理编码，避免手工拼接导致转义和分隔符错误。
7. 必须保持已打开可读并一直存活到请求完成。
8. 可分块消费并写入磁盘，避免整个响应常驻内存。
9. 通常会；因此一般在 finished 做统一收尾，避免重复提示和清理。
10. 没有。它是构建在 QNetworkAccessManager 上的 REST 便捷层。

## 22. 本篇结论

可靠 HTTP 代码的基本模板是：

```text
长期存在的 Manager
  → 构造结构化 URL 和 Request
  → 得到单次操作 Reply
  → 异步等待，不阻塞事件循环
  → 分层验证网络、HTTP、格式和业务
  → 小响应 readAll / 大响应流式处理
  → 所有结束路径 deleteLater
```

下一篇将在这个模板上加入超时、取消、并发控制、重定向、TLS、认证、Cookie、缓存、代理、重试与离线恢复，使它从“能请求”升级为可投入真实应用的网络层。
