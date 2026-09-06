# QNetworkAccessManager

> Qt 6.11.1 · Qt Network

## 1. 先建立直觉

**一句话定位：** `QNetworkAccessManager` 是 Qt 异步网络请求的调度中心，通常一个应用或一个网络服务对象持有一个实例。

**模块背景：** Qt Network 提供 TCP/UDP、HTTP、代理、DNS、SSL 和网络请求等异步网络能力。

### 这是什么

`QNetworkAccessManager` 是 Qt 异步网络请求的调度中心，通常一个应用或一个网络服务对象持有一个实例。

**内部模型：** 请求返回 QNetworkReply，真正结果通过 finished/readyRead/errorOccurred 等事件通知。manager 不会同步返回响应，也不应在每个请求里重复创建。

**适用场景：** HTTP/HTTPS GET、POST、上传下载、代理、缓存和 cookie 管理使用。必须在有事件循环的线程中运行。

**典型调用链：** 创建 manager -> 构造 QNetworkRequest -> get/post -> 连接 reply/manager 信号 -> 读取状态码和 body -> deleteLater reply。

**先记住的坑：** 不要在 finished 前释放 reply；检查 HTTP 状态码和 network error 两套错误；HTTPS 要处理 sslErrors；大响应使用 readyRead 分段读取。

## 2. 依赖与对象关系

- 头文件：`#include <QNetworkAccessManager>`
- 继承自：QObject
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Network)
target_link_libraries(mytarget PRIVATE Qt6::Network)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

请求返回 QNetworkReply，真正结果通过 finished/readyRead/errorOccurred 等事件通知。manager 不会同步返回响应，也不应在每个请求里重复创建。

### 状态、生命周期和线程

**生命周期：** manager 必须在线程事件循环中存活到 reply 完成；reply 完成后读取结果并调用 `deleteLater()`，不能在信号触发前直接释放。请求对象是值类型，reply 才是带有异步状态和资源的对象。

**状态与结果：** 请求成功发出不等于 HTTP 成功，HTTP 状态码成功也不等于业务 JSON 有效。至少分别处理网络错误、HTTP 状态码、响应头、响应体解析和业务字段校验。上传/下载还要处理进度、分段读取和取消。

**线程与事件循环：** QNetworkAccessManager、QNetworkReply 和相关请求应在同一个有事件循环的线程使用。跨线程时把网络对象整体放到目标线程，通过信号传递结果，不要跨线程直接读写 reply。

## 3. 直接使用

HTTP/HTTPS GET、POST、上传下载、代理、缓存和 cookie 管理使用。必须在有事件循环的线程中运行。 使用时通常按这个过程组织：创建 manager -> 构造 QNetworkRequest -> get/post -> 连接 reply/manager 信号 -> 读取状态码和 body -> deleteLater reply。

```cpp
#include <QNetworkAccessManager>
#include <QNetworkReply>
#include <QNetworkRequest>
#include <QUrl>

QNetworkAccessManager *manager = new QNetworkAccessManager(this);
QNetworkReply *reply = manager->get(QNetworkRequest(QUrl("https://example.com")));
connect(reply, &QNetworkReply::finished, this, [reply] {
    const QByteArray body = reply->readAll();
    reply->deleteLater();
});
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum Operation { HeadOperation, GetOperation, PutOperation, PostOperation, DeleteOperation, CustomOperation }`

### 公有函数

- `QNetworkAccessManager(QObject *parent = nullptr)`
- `virtual ~QNetworkAccessManager()`
- `void addStrictTransportSecurityHosts(const QList<QHstsPolicy> &knownHosts)`
- `bool autoDeleteReplies() const`
- `QAbstractNetworkCache * cache() const`
- `void clearAccessCache()`
- `void clearConnectionCache()`
- `void connectToHost(const QString &hostName, quint16 port = 80)`
- `void connectToHostEncrypted(const QString &hostName, quint16 port = 443, const QSslConfiguration &sslConfiguration = QSslConfiguration::defaultConfiguration())`
- `void connectToHostEncrypted(const QString &hostName, quint16 port, const QSslConfiguration &sslConfiguration, const QString &peerName)`
- `QNetworkCookieJar * cookieJar() const`
- `QNetworkReply * deleteResource(const QNetworkRequest &request)`
- `void enableStrictTransportSecurityStore(bool enabled, const QString &storeDir = QString())`
- `QNetworkReply * get(const QNetworkRequest &request)`
- `(since 6.7) QNetworkReply * get(const QNetworkRequest &request, QIODevice *data)`
- `(since 6.7) QNetworkReply * get(const QNetworkRequest &request, const QByteArray &data)`
- `QNetworkReply * head(const QNetworkRequest &request)`
- `bool isStrictTransportSecurityEnabled() const`
- `bool isStrictTransportSecurityStoreEnabled() const`
- `QNetworkReply * post(const QNetworkRequest &request, QIODevice *data)`
- `QNetworkReply * post(const QNetworkRequest &request, QHttpMultiPart *multiPart)`
- `QNetworkReply * post(const QNetworkRequest &request, const QByteArray &data)`
- `(since 6.8) QNetworkReply * post(const QNetworkRequest &request, std::nullptr_t nptr)`
- `QNetworkProxy proxy() const`
- `QNetworkProxyFactory * proxyFactory() const`
- `QNetworkReply * put(const QNetworkRequest &request, QIODevice *data)`
- `QNetworkReply * put(const QNetworkRequest &request, QHttpMultiPart *multiPart)`
- `QNetworkReply * put(const QNetworkRequest &request, const QByteArray &data)`
- `(since 6.8) QNetworkReply * put(const QNetworkRequest &request, std::nullptr_t nptr)`
- `QNetworkRequest::RedirectPolicy redirectPolicy() const`
- `QNetworkReply * sendCustomRequest(const QNetworkRequest &request, const QByteArray &verb, QIODevice *data = nullptr)`
- `QNetworkReply * sendCustomRequest(const QNetworkRequest &request, const QByteArray &verb, QHttpMultiPart *multiPart)`
- `QNetworkReply * sendCustomRequest(const QNetworkRequest &request, const QByteArray &verb, const QByteArray &data)`
- `void setAutoDeleteReplies(bool shouldAutoDelete)`
- `void setCache(QAbstractNetworkCache *cache)`
- `void setCookieJar(QNetworkCookieJar *cookieJar)`
- `void setProxy(const QNetworkProxy &proxy)`
- `void setProxyFactory(QNetworkProxyFactory *factory)`
- `void setRedirectPolicy(QNetworkRequest::RedirectPolicy policy)`
- `void setStrictTransportSecurityEnabled(bool enabled)`
- `void setTransferTimeout(int timeout)`
- `(since 6.7) void setTransferTimeout(std::chrono::milliseconds duration = QNetworkRequest::DefaultTransferTimeout)`
- `QList<QHstsPolicy> strictTransportSecurityHosts() const`
- `virtual QStringList supportedSchemes() const`
- `int transferTimeout() const`
- `(since 6.7) std::chrono::milliseconds transferTimeoutAsDuration() const`

### 信号

- `void authenticationRequired(QNetworkReply *reply, QAuthenticator *authenticator)`
- `void encrypted(QNetworkReply *reply)`
- `void finished(QNetworkReply *reply)`
- `void preSharedKeyAuthenticationRequired(QNetworkReply *reply, QSslPreSharedKeyAuthenticator *authenticator)`
- `void proxyAuthenticationRequired(const QNetworkProxy &proxy, QAuthenticator *authenticator)`
- `void sslErrors(QNetworkReply *reply, const QList<QSslError> &errors)`

### 保护函数

- `virtual QNetworkReply * createRequest(QNetworkAccessManager::Operation op, const QNetworkRequest &originalReq, QIODevice *outgoingData = nullptr)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 54 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QNetworkAccessManager::Operation`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QNetworkAccessManager` 暴露的类型声明 `Operation`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Operation`。
- 属性名：`QNetworkAccessManager`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QNetworkAccessManager::QNetworkAccessManager(QObject *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkAccessManager` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `parent`：类型为 `QObject *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QNetworkAccessManager::~QNetworkAccessManager()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkAccessManager` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkAccessManager::addStrictTransportSecurityHosts(const QList<QHstsPolicy> &knownHosts)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QNetworkAccessManager` 添加依赖、数据或子对象的 API `addStrictTransportSecurityHosts`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `knownHosts`：类型为 `const QList<QHstsPolicy> &`。没有默认值，调用时必须提供。传入 `const QList<QHstsPolicy> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QNetworkAccessManager::authenticationRequired(QNetworkReply *reply, QAuthenticator *authenticator)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkAccessManager` 发出的通知信号 `authenticationRequired`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `reply`：类型为 `QNetworkReply *`。没有默认值，调用时必须提供。异步响应对象。它通常有自己的生命周期、状态和错误信号，读取前要确认仍然有效。
- 参数 `authenticator`：类型为 `QAuthenticator *`。没有默认值，调用时必须提供。传入 `QAuthenticator *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QNetworkAccessManager::autoDeleteReplies() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkAccessManager::autoDeleteReplies` 用于计算、查询或取得与“auto、删除、Replies”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QAbstractNetworkCache *QNetworkAccessManager::cache() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkAccessManager::cache` 用于计算、查询或取得与“cache”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QAbstractNetworkCache *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QAbstractNetworkCache *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkAccessManager::clearAccessCache()`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkAccessManager::clearAccessCache` 用于执行与“清空、Access、Cache”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkAccessManager::clearConnectionCache()`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkAccessManager::clearConnectionCache` 用于执行与“清空、Connection、Cache”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkAccessManager::connectToHost(const QString &hostName, quint16 port = 80)`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `connectToHost`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`void`。
- 参数 `hostName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `port`：类型为 `quint16`。默认值为 `80`。传入 `quint16` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkAccessManager::connectToHostEncrypted(const QString &hostName, quint16 port = 443, const QSslConfiguration &sslConfiguration = QSslConfiguration::defaultConfiguration())`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `connectToHostEncrypted`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`void`。
- 参数 `hostName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `port`：类型为 `quint16`。默认值为 `443`。传入 `quint16` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sslConfiguration`：类型为 `const QSslConfiguration &`。默认值为 `QSslConfiguration::defaultConfiguration()`。传入 `const QSslConfiguration &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkAccessManager::connectToHostEncrypted(const QString &hostName, quint16 port, const QSslConfiguration &sslConfiguration, const QString &peerName)`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `connectToHostEncrypted`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`void`。
- 参数 `hostName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `port`：类型为 `quint16`。没有默认值，调用时必须提供。传入 `quint16` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sslConfiguration`：类型为 `const QSslConfiguration &`。没有默认值，调用时必须提供。传入 `const QSslConfiguration &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `peerName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QNetworkCookieJar *QNetworkAccessManager::cookieJar() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkAccessManager::cookieJar` 用于计算、查询或取得与“cookie、Jar”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QNetworkCookieJar *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QNetworkCookieJar *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] QNetworkReply *QNetworkAccessManager::createRequest(QNetworkAccessManager::Operation op, const QNetworkRequest &originalReq, QIODevice *outgoingData = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkAccessManager::createRequest` 用于计算、查询或取得与“创建、请求”相关的操作。调用时要先确认当前状态和 `op`、`originalReq`、`outgoingData` 的有效范围；返回类型是 `QNetworkReply *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QNetworkReply *`。
- 参数 `op`：类型为 `QNetworkAccessManager::Operation`。没有默认值，调用时必须提供。传入 `QNetworkAccessManager::Operation` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `originalReq`：类型为 `const QNetworkRequest &`。没有默认值，调用时必须提供。传入 `const QNetworkRequest &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `outgoingData`：类型为 `QIODevice *`。默认值为 `nullptr`。传入 `QIODevice *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QNetworkReply *QNetworkAccessManager::deleteResource(const QNetworkRequest &request)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `deleteResource`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`QNetworkReply *`。
- 参数 `request`：类型为 `const QNetworkRequest &`。没有默认值，调用时必须提供。请求描述对象，通常包含 URL、请求头和传输选项；它不等于响应或实际连接。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkAccessManager::enableStrictTransportSecurityStore(bool enabled, const QString &storeDir = QString())`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkAccessManager::enableStrictTransportSecurityStore` 用于执行与“enable、Strict、Transport、Security、Store”相关的操作。调用时要先确认当前状态和 `enabled`、`storeDir` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `enabled`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `storeDir`：类型为 `const QString &`。默认值为 `QString()`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QNetworkAccessManager::encrypted(QNetworkReply *reply)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkAccessManager` 发出的通知信号 `encrypted`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `reply`：类型为 `QNetworkReply *`。没有默认值，调用时必须提供。异步响应对象。它通常有自己的生命周期、状态和错误信号，读取前要确认仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QNetworkAccessManager::finished(QNetworkReply *reply)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkAccessManager` 发出的通知信号 `finished`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `reply`：类型为 `QNetworkReply *`。没有默认值，调用时必须提供。异步响应对象。它通常有自己的生命周期、状态和错误信号，读取前要确认仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QNetworkReply *QNetworkAccessManager::get(const QNetworkRequest &request)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkAccessManager` 的核心操作 `get`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`QNetworkReply *`。
- 参数 `request`：类型为 `const QNetworkRequest &`。没有默认值，调用时必须提供。请求描述对象，通常包含 URL、请求头和传输选项；它不等于响应或实际连接。

**正确调用组合：** 通常与 `QNetworkRequest`、`QNetworkReply::finished`、错误信号和 `deleteLater()` 一起使用。

### `[since 6.7] QNetworkReply *QNetworkAccessManager::get(const QNetworkRequest &request, QIODevice *data)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkAccessManager` 的核心操作 `get`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`QNetworkReply *`。
- 参数 `request`：类型为 `const QNetworkRequest &`。没有默认值，调用时必须提供。请求描述对象，通常包含 URL、请求头和传输选项；它不等于响应或实际连接。
- 参数 `data`：类型为 `QIODevice *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 通常与 `QNetworkRequest`、`QNetworkReply::finished`、错误信号和 `deleteLater()` 一起使用。

### `[since 6.7] QNetworkReply *QNetworkAccessManager::get(const QNetworkRequest &request, const QByteArray &data)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkAccessManager` 的核心操作 `get`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`QNetworkReply *`。
- 参数 `request`：类型为 `const QNetworkRequest &`。没有默认值，调用时必须提供。请求描述对象，通常包含 URL、请求头和传输选项；它不等于响应或实际连接。
- 参数 `data`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 通常与 `QNetworkRequest`、`QNetworkReply::finished`、错误信号和 `deleteLater()` 一起使用。

### `QNetworkReply *QNetworkAccessManager::head(const QNetworkRequest &request)`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkAccessManager::head` 用于计算、查询或取得与“head”相关的操作。调用时要先确认当前状态和 `request` 的有效范围；返回类型是 `QNetworkReply *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QNetworkReply *`。
- 参数 `request`：类型为 `const QNetworkRequest &`。没有默认值，调用时必须提供。请求描述对象，通常包含 URL、请求头和传输选项；它不等于响应或实际连接。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QNetworkAccessManager::isStrictTransportSecurityEnabled() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isStrictTransportSecurityEnabled`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QNetworkAccessManager::isStrictTransportSecurityStoreEnabled() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isStrictTransportSecurityStoreEnabled`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QNetworkReply *QNetworkAccessManager::post(const QNetworkRequest &request, QIODevice *data)`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkAccessManager::post` 用于计算、查询或取得与“post”相关的操作。调用时要先确认当前状态和 `request`、`data` 的有效范围；返回类型是 `QNetworkReply *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QNetworkReply *`。
- 参数 `request`：类型为 `const QNetworkRequest &`。没有默认值，调用时必须提供。请求描述对象，通常包含 URL、请求头和传输选项；它不等于响应或实际连接。
- 参数 `data`：类型为 `QIODevice *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 通常与 Content-Type、请求体编码、finished/errorOccurred 和 HTTP 状态码检查一起使用。

### `QNetworkReply *QNetworkAccessManager::post(const QNetworkRequest &request, QHttpMultiPart *multiPart)`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkAccessManager::post` 用于计算、查询或取得与“post”相关的操作。调用时要先确认当前状态和 `request`、`multiPart` 的有效范围；返回类型是 `QNetworkReply *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QNetworkReply *`。
- 参数 `request`：类型为 `const QNetworkRequest &`。没有默认值，调用时必须提供。请求描述对象，通常包含 URL、请求头和传输选项；它不等于响应或实际连接。
- 参数 `multiPart`：类型为 `QHttpMultiPart *`。没有默认值，调用时必须提供。传入 `QHttpMultiPart *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 通常与 Content-Type、请求体编码、finished/errorOccurred 和 HTTP 状态码检查一起使用。

### `QNetworkReply *QNetworkAccessManager::post(const QNetworkRequest &request, const QByteArray &data)`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkAccessManager::post` 用于计算、查询或取得与“post”相关的操作。调用时要先确认当前状态和 `request`、`data` 的有效范围；返回类型是 `QNetworkReply *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QNetworkReply *`。
- 参数 `request`：类型为 `const QNetworkRequest &`。没有默认值，调用时必须提供。请求描述对象，通常包含 URL、请求头和传输选项；它不等于响应或实际连接。
- 参数 `data`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 通常与 Content-Type、请求体编码、finished/errorOccurred 和 HTTP 状态码检查一起使用。

### `[since 6.8] QNetworkReply *QNetworkAccessManager::post(const QNetworkRequest &request, std::nullptr_t nptr)`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkAccessManager::post` 用于计算、查询或取得与“post”相关的操作。调用时要先确认当前状态和 `request`、`nptr` 的有效范围；返回类型是 `QNetworkReply *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QNetworkReply *`。
- 参数 `request`：类型为 `const QNetworkRequest &`。没有默认值，调用时必须提供。请求描述对象，通常包含 URL、请求头和传输选项；它不等于响应或实际连接。
- 参数 `nptr`：类型为 `std::nullptr_t`。没有默认值，调用时必须提供。传入 `std::nullptr_t` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 通常与 Content-Type、请求体编码、finished/errorOccurred 和 HTTP 状态码检查一起使用。

### `[signal] void QNetworkAccessManager::preSharedKeyAuthenticationRequired(QNetworkReply *reply, QSslPreSharedKeyAuthenticator *authenticator)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkAccessManager` 发出的通知信号 `preSharedKeyAuthenticationRequired`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `reply`：类型为 `QNetworkReply *`。没有默认值，调用时必须提供。异步响应对象。它通常有自己的生命周期、状态和错误信号，读取前要确认仍然有效。
- 参数 `authenticator`：类型为 `QSslPreSharedKeyAuthenticator *`。没有默认值，调用时必须提供。传入 `QSslPreSharedKeyAuthenticator *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QNetworkProxy QNetworkAccessManager::proxy() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkAccessManager::proxy` 用于计算、查询或取得与“proxy”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QNetworkProxy`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QNetworkProxy`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QNetworkAccessManager::proxyAuthenticationRequired(const QNetworkProxy &proxy, QAuthenticator *authenticator)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkAccessManager` 发出的通知信号 `proxyAuthenticationRequired`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `proxy`：类型为 `const QNetworkProxy &`。没有默认值，调用时必须提供。传入 `const QNetworkProxy &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `authenticator`：类型为 `QAuthenticator *`。没有默认值，调用时必须提供。传入 `QAuthenticator *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QNetworkProxyFactory *QNetworkAccessManager::proxyFactory() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkAccessManager::proxyFactory` 用于计算、查询或取得与“proxy、Factory”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QNetworkProxyFactory *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QNetworkProxyFactory *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QNetworkReply *QNetworkAccessManager::put(const QNetworkRequest &request, QIODevice *data)`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkAccessManager::put` 用于计算、查询或取得与“put”相关的操作。调用时要先确认当前状态和 `request`、`data` 的有效范围；返回类型是 `QNetworkReply *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QNetworkReply *`。
- 参数 `request`：类型为 `const QNetworkRequest &`。没有默认值，调用时必须提供。请求描述对象，通常包含 URL、请求头和传输选项；它不等于响应或实际连接。
- 参数 `data`：类型为 `QIODevice *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QNetworkReply *QNetworkAccessManager::put(const QNetworkRequest &request, QHttpMultiPart *multiPart)`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkAccessManager::put` 用于计算、查询或取得与“put”相关的操作。调用时要先确认当前状态和 `request`、`multiPart` 的有效范围；返回类型是 `QNetworkReply *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QNetworkReply *`。
- 参数 `request`：类型为 `const QNetworkRequest &`。没有默认值，调用时必须提供。请求描述对象，通常包含 URL、请求头和传输选项；它不等于响应或实际连接。
- 参数 `multiPart`：类型为 `QHttpMultiPart *`。没有默认值，调用时必须提供。传入 `QHttpMultiPart *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QNetworkReply *QNetworkAccessManager::put(const QNetworkRequest &request, const QByteArray &data)`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkAccessManager::put` 用于计算、查询或取得与“put”相关的操作。调用时要先确认当前状态和 `request`、`data` 的有效范围；返回类型是 `QNetworkReply *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QNetworkReply *`。
- 参数 `request`：类型为 `const QNetworkRequest &`。没有默认值，调用时必须提供。请求描述对象，通常包含 URL、请求头和传输选项；它不等于响应或实际连接。
- 参数 `data`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.8] QNetworkReply *QNetworkAccessManager::put(const QNetworkRequest &request, std::nullptr_t nptr)`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkAccessManager::put` 用于计算、查询或取得与“put”相关的操作。调用时要先确认当前状态和 `request`、`nptr` 的有效范围；返回类型是 `QNetworkReply *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QNetworkReply *`。
- 参数 `request`：类型为 `const QNetworkRequest &`。没有默认值，调用时必须提供。请求描述对象，通常包含 URL、请求头和传输选项；它不等于响应或实际连接。
- 参数 `nptr`：类型为 `std::nullptr_t`。没有默认值，调用时必须提供。传入 `std::nullptr_t` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QNetworkRequest::RedirectPolicy QNetworkAccessManager::redirectPolicy() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkAccessManager::redirectPolicy` 用于计算、查询或取得与“redirect、Policy”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QNetworkRequest::RedirectPolicy`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QNetworkRequest::RedirectPolicy`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QNetworkReply *QNetworkAccessManager::sendCustomRequest(const QNetworkRequest &request, const QByteArray &verb, QIODevice *data = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkAccessManager` 的核心操作 `sendCustomRequest`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`QNetworkReply *`。
- 参数 `request`：类型为 `const QNetworkRequest &`。没有默认值，调用时必须提供。请求描述对象，通常包含 URL、请求头和传输选项；它不等于响应或实际连接。
- 参数 `verb`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `data`：类型为 `QIODevice *`。默认值为 `nullptr`。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QNetworkReply *QNetworkAccessManager::sendCustomRequest(const QNetworkRequest &request, const QByteArray &verb, QHttpMultiPart *multiPart)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkAccessManager` 的核心操作 `sendCustomRequest`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`QNetworkReply *`。
- 参数 `request`：类型为 `const QNetworkRequest &`。没有默认值，调用时必须提供。请求描述对象，通常包含 URL、请求头和传输选项；它不等于响应或实际连接。
- 参数 `verb`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `multiPart`：类型为 `QHttpMultiPart *`。没有默认值，调用时必须提供。传入 `QHttpMultiPart *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QNetworkReply *QNetworkAccessManager::sendCustomRequest(const QNetworkRequest &request, const QByteArray &verb, const QByteArray &data)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkAccessManager` 的核心操作 `sendCustomRequest`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`QNetworkReply *`。
- 参数 `request`：类型为 `const QNetworkRequest &`。没有默认值，调用时必须提供。请求描述对象，通常包含 URL、请求头和传输选项；它不等于响应或实际连接。
- 参数 `verb`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `data`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkAccessManager::setAutoDeleteReplies(bool shouldAutoDelete)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setAutoDeleteReplies`。调用它会改变 `QNetworkAccessManager` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `shouldAutoDelete`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkAccessManager::setCache(QAbstractNetworkCache *cache)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setCache`。调用它会改变 `QNetworkAccessManager` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `cache`：类型为 `QAbstractNetworkCache *`。没有默认值，调用时必须提供。传入 `QAbstractNetworkCache *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkAccessManager::setCookieJar(QNetworkCookieJar *cookieJar)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setCookieJar`。调用它会改变 `QNetworkAccessManager` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `cookieJar`：类型为 `QNetworkCookieJar *`。没有默认值，调用时必须提供。传入 `QNetworkCookieJar *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkAccessManager::setProxy(const QNetworkProxy &proxy)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setProxy`。调用它会改变 `QNetworkAccessManager` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `proxy`：类型为 `const QNetworkProxy &`。没有默认值，调用时必须提供。传入 `const QNetworkProxy &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkAccessManager::setProxyFactory(QNetworkProxyFactory *factory)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setProxyFactory`。调用它会改变 `QNetworkAccessManager` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `factory`：类型为 `QNetworkProxyFactory *`。没有默认值，调用时必须提供。传入 `QNetworkProxyFactory *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkAccessManager::setRedirectPolicy(QNetworkRequest::RedirectPolicy policy)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setRedirectPolicy`。调用它会改变 `QNetworkAccessManager` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `policy`：类型为 `QNetworkRequest::RedirectPolicy`。没有默认值，调用时必须提供。传入 `QNetworkRequest::RedirectPolicy` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkAccessManager::setStrictTransportSecurityEnabled(bool enabled)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setStrictTransportSecurityEnabled`。调用它会改变 `QNetworkAccessManager` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enabled`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkAccessManager::setTransferTimeout(int timeout)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setTransferTimeout`。调用它会改变 `QNetworkAccessManager` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `timeout`：类型为 `int`。没有默认值，调用时必须提供。超时时间或超时对象，可能表示等待时长，也可能表示 QNetworkReply/QTimer 等异步对象，不能只看名称判断。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.7] void QNetworkAccessManager::setTransferTimeout(std::chrono::milliseconds duration = QNetworkRequest::DefaultTransferTimeout)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setTransferTimeout`。调用它会改变 `QNetworkAccessManager` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `duration`：类型为 `std::chrono::milliseconds`。默认值为 `QNetworkRequest::DefaultTransferTimeout`。持续时间，通常以毫秒表示；要确认 0、负数、循环和平台精度。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QNetworkAccessManager::sslErrors(QNetworkReply *reply, const QList<QSslError> &errors)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkAccessManager` 发出的通知信号 `sslErrors`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `reply`：类型为 `QNetworkReply *`。没有默认值，调用时必须提供。异步响应对象。它通常有自己的生命周期、状态和错误信号，读取前要确认仍然有效。
- 参数 `errors`：类型为 `const QList<QSslError> &`。没有默认值，调用时必须提供。传入 `const QList<QSslError> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QHstsPolicy> QNetworkAccessManager::strictTransportSecurityHosts() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkAccessManager::strictTransportSecurityHosts` 用于计算、查询或取得与“strict、Transport、Security、Hosts”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<QHstsPolicy>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QHstsPolicy>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] QStringList QNetworkAccessManager::supportedSchemes() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkAccessManager::supportedSchemes` 用于计算、查询或取得与“supported、Schemes”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QStringList`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStringList`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QNetworkAccessManager::transferTimeout() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkAccessManager::transferTimeout` 用于计算、查询或取得与“transfer、超时”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.7] std::chrono::milliseconds QNetworkAccessManager::transferTimeoutAsDuration() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkAccessManager::transferTimeoutAsDuration` 用于计算、查询或取得与“transfer、超时、As、持续时间”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `std::chrono::milliseconds`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`std::chrono::milliseconds`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

## 6. 深入实践与常见坑

### 生命周期和资源边界

manager 必须在线程事件循环中存活到 reply 完成；reply 完成后读取结果并调用 `deleteLater()`，不能在信号触发前直接释放。请求对象是值类型，reply 才是带有异步状态和资源的对象。

### 状态和错误边界

请求成功发出不等于 HTTP 成功，HTTP 状态码成功也不等于业务 JSON 有效。至少分别处理网络错误、HTTP 状态码、响应头、响应体解析和业务字段校验。上传/下载还要处理进度、分段读取和取消。

### 线程边界

QNetworkAccessManager、QNetworkReply 和相关请求应在同一个有事件循环的线程使用。跨线程时把网络对象整体放到目标线程，通过信号传递结果，不要跨线程直接读写 reply。

### 最容易出现的错误

不要在 finished 前释放 reply；检查 HTTP 状态码和 network error 两套错误；HTTPS 要处理 sslErrors；大响应使用 readyRead 分段读取。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QNetworkAccessManager` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
