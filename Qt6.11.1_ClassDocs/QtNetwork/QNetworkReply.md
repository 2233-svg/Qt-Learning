# QNetworkReply

> Qt 6.11.1 · Qt Network

## 1. 先建立直觉

**一句话定位：** 一次异步网络请求的响应对象，负责提供响应头、状态、数据、进度和错误通知。

**模块背景：** Qt Network 提供 TCP/UDP、HTTP、代理、DNS、SSL 和网络请求等异步网络能力。

### 这是什么

`QNetworkReply`：一次异步网络请求的响应对象，负责提供响应头、状态、数据、进度和错误通知。

**内部模型：** 网络请求通常由管理器创建并调度，返回一个代表本次操作的 reply。连接建立、DNS、发送、接收和错误都是事件驱动的阶段；响应头、状态码、body 和传输错误分别表达不同层次的信息。

**适用场景：** 创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要把异步请求当同步函数；不要只检查 `error()` 而忽略 HTTP 状态码；不要在 readyRead 中假设一次就收到完整 body；不要在 GUI 线程用阻塞等待替代信号。

## 2. 依赖与对象关系

- 头文件：`#include <QNetworkReply>`
- 继承自：QIODevice
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Network)
target_link_libraries(mytarget PRIVATE Qt6::Network)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

网络请求通常由管理器创建并调度，返回一个代表本次操作的 reply。连接建立、DNS、发送、接收和错误都是事件驱动的阶段；响应头、状态码、body 和传输错误分别表达不同层次的信息。

### 状态、生命周期和线程

**生命周期：** manager 必须在线程事件循环中存活到 reply 完成；reply 完成后读取结果并调用 `deleteLater()`，不能在信号触发前直接释放。请求对象是值类型，reply 才是带有异步状态和资源的对象。

**状态与结果：** 请求成功发出不等于 HTTP 成功，HTTP 状态码成功也不等于业务 JSON 有效。至少分别处理网络错误、HTTP 状态码、响应头、响应体解析和业务字段校验。上传/下载还要处理进度、分段读取和取消。

**线程与事件循环：** QNetworkAccessManager、QNetworkReply 和相关请求应在同一个有事件循环的线程使用。跨线程时把网络对象整体放到目标线程，通过信号传递结果，不要跨线程直接读写 reply。

## 3. 直接使用

创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。 使用时通常按这个过程组织：构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

```cpp
// manager、reply 和事件循环必须在正确线程中存活。
QNetworkReply *reply = manager->get(request);
connect(reply, &QNetworkReply::finished, this, [reply] {
    const QByteArray body = reply->readAll();
    reply->deleteLater();
});
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum NetworkError { NoError, ConnectionRefusedError, RemoteHostClosedError, HostNotFoundError, TimeoutError, …, UnknownServerError }`
- `RawHeaderPair`

### 公有函数

- `virtual ~QNetworkReply()`
- `QVariant attribute(QNetworkRequest::Attribute code) const`
- `QNetworkReply::NetworkError error() const`
- `bool hasRawHeader(QAnyStringView headerName) const`
- `QVariant header(QNetworkRequest::KnownHeaders header) const`
- `(since 6.8) QHttpHeaders headers() const`
- `void ignoreSslErrors(const QList<QSslError> &errors)`
- `bool isFinished() const`
- `bool isRunning() const`
- `QNetworkAccessManager * manager() const`
- `QNetworkAccessManager::Operation operation() const`
- `QByteArray rawHeader(QAnyStringView headerName) const`
- `QList<QByteArray> rawHeaderList() const`
- `const QList<QNetworkReply::RawHeaderPair> & rawHeaderPairs() const`
- `qint64 readBufferSize() const`
- `QNetworkRequest request() const`
- `virtual void setReadBufferSize(qint64 size)`
- `void setSslConfiguration(const QSslConfiguration &config)`
- `QSslConfiguration sslConfiguration() const`
- `QUrl url() const`

### 重实现的公有函数

- `virtual void close() override`
- `virtual bool isSequential() const override`

### 公有槽函数

- `virtual void abort() = 0`
- `virtual void ignoreSslErrors()`

### 信号

- `void downloadProgress(qint64 bytesReceived, qint64 bytesTotal)`
- `void encrypted()`
- `void errorOccurred(QNetworkReply::NetworkError code)`
- `void finished()`
- `void metaDataChanged()`
- `void preSharedKeyAuthenticationRequired(QSslPreSharedKeyAuthenticator *authenticator)`
- `void redirectAllowed()`
- `void redirected(const QUrl &url)`
- `(since 6.3) void requestSent()`
- `(since 6.3) void socketStartedConnecting()`
- `void sslErrors(const QList<QSslError> &errors)`
- `void uploadProgress(qint64 bytesSent, qint64 bytesTotal)`

### 保护函数

- `QNetworkReply(QObject *parent = nullptr)`
- `virtual void ignoreSslErrorsImplementation(const QList<QSslError> &errors)`
- `void setAttribute(QNetworkRequest::Attribute code, const QVariant &value)`
- `void setError(QNetworkReply::NetworkError errorCode, const QString &errorString)`
- `void setFinished(bool finished)`
- `void setHeader(QNetworkRequest::KnownHeaders header, const QVariant &value)`
- `(since 6.8) void setHeaders(const QHttpHeaders &newHeaders)`
- `(since 6.8) void setHeaders(QHttpHeaders &&newHeaders)`
- `void setOperation(QNetworkAccessManager::Operation operation)`
- `void setRawHeader(const QByteArray &headerName, const QByteArray &value)`
- `void setRequest(const QNetworkRequest &request)`
- `virtual void setSslConfigurationImplementation(const QSslConfiguration &configuration)`
- `void setUrl(const QUrl &url)`
- `(since 6.8) void setWellKnownHeader(QHttpHeaders::WellKnownHeader name, QByteArrayView value)`
- `virtual void sslConfigurationImplementation(QSslConfiguration &configuration) const`

### 重实现的保护函数

- `virtual qint64 writeData(const char *data, qint64 len) override`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 55 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QNetworkReply::NetworkError`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QNetworkReply` 暴露的类型声明 `Network、错误`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:NetworkError`。
- 属性名：`QNetworkReply`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QNetworkReply::RawHeaderPair`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QNetworkReply` 的配置属性。初始化或状态切换时通过 `setRawHeaderPair(...)` 设置，之后用 `RawHeaderPair()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:RawHeaderPair`。
- 属性名：`QNetworkReply`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit protected] QNetworkReply::QNetworkReply(QObject *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkReply` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `parent`：类型为 `QObject *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QNetworkReply::~QNetworkReply()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkReply` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[pure virtual slot] void QNetworkReply::abort()`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `abort`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVariant QNetworkReply::attribute(QNetworkRequest::Attribute code) const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkReply::attribute` 用于计算、查询或取得与“attribute”相关的操作。调用时要先确认当前状态和 `code` 的有效范围；返回类型是 `QVariant`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVariant`。
- 参数 `code`：类型为 `QNetworkRequest::Attribute`。没有默认值，调用时必须提供。传入 `QNetworkRequest::Attribute` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] void QNetworkReply::close()`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `close`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QNetworkReply::downloadProgress(qint64 bytesReceived, qint64 bytesTotal)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkReply` 发出的通知信号 `downloadProgress`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `bytesReceived`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `bytesTotal`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QNetworkReply::encrypted()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkReply` 发出的通知信号 `encrypted`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QNetworkReply::NetworkError QNetworkReply::error() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkReply::error` 用于计算、查询或取得与“错误”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QNetworkReply::NetworkError`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QNetworkReply::NetworkError`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QNetworkReply::errorOccurred(QNetworkReply::NetworkError code)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkReply` 发出的通知信号 `errorOccurred`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `code`：类型为 `QNetworkReply::NetworkError`。没有默认值，调用时必须提供。传入 `QNetworkReply::NetworkError` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QNetworkReply::finished()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkReply` 发出的通知信号 `finished`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QNetworkReply::hasRawHeader(QAnyStringView headerName) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `hasRawHeader`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `headerName`：类型为 `QAnyStringView`。没有默认值，调用时必须提供。传入 `QAnyStringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVariant QNetworkReply::header(QNetworkRequest::KnownHeaders header) const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkReply::header` 用于计算、查询或取得与“header”相关的操作。调用时要先确认当前状态和 `header` 的有效范围；返回类型是 `QVariant`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVariant`。
- 参数 `header`：类型为 `QNetworkRequest::KnownHeaders`。没有默认值，调用时必须提供。传入 `QNetworkRequest::KnownHeaders` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.8] QHttpHeaders QNetworkReply::headers() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkReply::headers` 用于计算、查询或取得与“headers”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QHttpHeaders`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QHttpHeaders`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual slot] void QNetworkReply::ignoreSslErrors()`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkReply::ignoreSslErrors` 用于执行与“ignore、Ssl、Errors”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkReply::ignoreSslErrors(const QList<QSslError> &errors)`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkReply::ignoreSslErrors` 用于执行与“ignore、Ssl、Errors”相关的操作。调用时要先确认当前状态和 `errors` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `errors`：类型为 `const QList<QSslError> &`。没有默认值，调用时必须提供。传入 `const QList<QSslError> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QNetworkReply::ignoreSslErrorsImplementation(const QList<QSslError> &errors)`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkReply::ignoreSslErrorsImplementation` 用于执行与“ignore、Ssl、Errors、Implementation”相关的操作。调用时要先确认当前状态和 `errors` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `errors`：类型为 `const QList<QSslError> &`。没有默认值，调用时必须提供。传入 `const QList<QSslError> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QNetworkReply::isFinished() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isFinished`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QNetworkReply::isRunning() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isRunning`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QNetworkReply::isSequential() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isSequential`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QNetworkAccessManager *QNetworkReply::manager() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkReply::manager` 用于计算、查询或取得与“manager”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QNetworkAccessManager *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QNetworkAccessManager *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QNetworkReply::metaDataChanged()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkReply` 发出的通知信号 `metaDataChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QNetworkAccessManager::Operation QNetworkReply::operation() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkReply::operation` 用于计算、查询或取得与“operation”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QNetworkAccessManager::Operation`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QNetworkAccessManager::Operation`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QNetworkReply::preSharedKeyAuthenticationRequired(QSslPreSharedKeyAuthenticator *authenticator)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkReply` 发出的通知信号 `preSharedKeyAuthenticationRequired`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `authenticator`：类型为 `QSslPreSharedKeyAuthenticator *`。没有默认值，调用时必须提供。传入 `QSslPreSharedKeyAuthenticator *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray QNetworkReply::rawHeader(QAnyStringView headerName) const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkReply::rawHeader` 用于计算、查询或取得与“raw、Header”相关的操作。调用时要先确认当前状态和 `headerName` 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `headerName`：类型为 `QAnyStringView`。没有默认值，调用时必须提供。传入 `QAnyStringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QByteArray> QNetworkReply::rawHeaderList() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkReply::rawHeaderList` 用于计算、查询或取得与“raw、Header、List”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<QByteArray>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QByteArray>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QList<QNetworkReply::RawHeaderPair> &QNetworkReply::rawHeaderPairs() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkReply::rawHeaderPairs` 用于计算、查询或取得与“raw、Header、Pairs”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QList<QNetworkReply::RawHeaderPair> &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QList<QNetworkReply::RawHeaderPair> &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qint64 QNetworkReply::readBufferSize() const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkReply` 的核心操作 `readBufferSize`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`qint64`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QNetworkReply::redirectAllowed()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkReply` 发出的通知信号 `redirectAllowed`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QNetworkReply::redirected(const QUrl &url)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkReply` 发出的通知信号 `redirected`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `url`：类型为 `const QUrl &`。没有默认值，调用时必须提供。资源地址。要确认 scheme、编码、相对路径、重定向和是否包含敏感信息。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QNetworkRequest QNetworkReply::request() const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkReply` 的核心操作 `request`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`QNetworkRequest`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal, since 6.3] void QNetworkReply::requestSent()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkReply` 的核心操作 `requestSent`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] void QNetworkReply::setAttribute(QNetworkRequest::Attribute code, const QVariant &value)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setAttribute`。调用它会改变 `QNetworkReply` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `code`：类型为 `QNetworkRequest::Attribute`。没有默认值，调用时必须提供。传入 `QNetworkRequest::Attribute` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const QVariant &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] void QNetworkReply::setError(QNetworkReply::NetworkError errorCode, const QString &errorString)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setError`。调用它会改变 `QNetworkReply` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `errorCode`：类型为 `QNetworkReply::NetworkError`。没有默认值，调用时必须提供。传入 `QNetworkReply::NetworkError` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `errorString`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] void QNetworkReply::setFinished(bool finished)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFinished`。调用它会改变 `QNetworkReply` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `finished`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] void QNetworkReply::setHeader(QNetworkRequest::KnownHeaders header, const QVariant &value)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setHeader`。调用它会改变 `QNetworkReply` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `header`：类型为 `QNetworkRequest::KnownHeaders`。没有默认值，调用时必须提供。传入 `QNetworkRequest::KnownHeaders` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const QVariant &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected, since 6.8] void QNetworkReply::setHeaders(const QHttpHeaders &newHeaders)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setHeaders`。调用它会改变 `QNetworkReply` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `newHeaders`：类型为 `const QHttpHeaders &`。没有默认值，调用时必须提供。传入 `const QHttpHeaders &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected, since 6.8] void QNetworkReply::setHeaders(QHttpHeaders &&newHeaders)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setHeaders`。调用它会改变 `QNetworkReply` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `newHeaders`：类型为 `QHttpHeaders &&`。没有默认值，调用时必须提供。传入 `QHttpHeaders &&` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] void QNetworkReply::setOperation(QNetworkAccessManager::Operation operation)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setOperation`。调用它会改变 `QNetworkReply` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `operation`：类型为 `QNetworkAccessManager::Operation`。没有默认值，调用时必须提供。传入 `QNetworkAccessManager::Operation` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] void QNetworkReply::setRawHeader(const QByteArray &headerName, const QByteArray &value)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setRawHeader`。调用它会改变 `QNetworkReply` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `headerName`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `value`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] void QNetworkReply::setReadBufferSize(qint64 size)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setReadBufferSize`。调用它会改变 `QNetworkReply` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `size`：类型为 `qint64`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] void QNetworkReply::setRequest(const QNetworkRequest &request)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setRequest`。调用它会改变 `QNetworkReply` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `request`：类型为 `const QNetworkRequest &`。没有默认值，调用时必须提供。请求描述对象，通常包含 URL、请求头和传输选项；它不等于响应或实际连接。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkReply::setSslConfiguration(const QSslConfiguration &config)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSslConfiguration`。调用它会改变 `QNetworkReply` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `config`：类型为 `const QSslConfiguration &`。没有默认值，调用时必须提供。传入 `const QSslConfiguration &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QNetworkReply::setSslConfigurationImplementation(const QSslConfiguration &configuration)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSslConfigurationImplementation`。调用它会改变 `QNetworkReply` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `configuration`：类型为 `const QSslConfiguration &`。没有默认值，调用时必须提供。传入 `const QSslConfiguration &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] void QNetworkReply::setUrl(const QUrl &url)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setUrl`。调用它会改变 `QNetworkReply` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `url`：类型为 `const QUrl &`。没有默认值，调用时必须提供。资源地址。要确认 scheme、编码、相对路径、重定向和是否包含敏感信息。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected, since 6.8] void QNetworkReply::setWellKnownHeader(QHttpHeaders::WellKnownHeader name, QByteArrayView value)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setWellKnownHeader`。调用它会改变 `QNetworkReply` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `name`：类型为 `QHttpHeaders::WellKnownHeader`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。
- 参数 `value`：类型为 `QByteArrayView`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal, since 6.3] void QNetworkReply::socketStartedConnecting()`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkReply::socketStartedConnecting` 用于执行与“socket、Started、Connecting”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslConfiguration QNetworkReply::sslConfiguration() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkReply::sslConfiguration` 用于计算、查询或取得与“ssl、Configuration”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSslConfiguration`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSslConfiguration`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QNetworkReply::sslConfigurationImplementation(QSslConfiguration &configuration) const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkReply::sslConfigurationImplementation` 用于执行与“ssl、Configuration、Implementation”相关的操作。调用时要先确认当前状态和 `configuration` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `configuration`：类型为 `QSslConfiguration &`。没有默认值，调用时必须提供。传入 `QSslConfiguration &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QNetworkReply::sslErrors(const QList<QSslError> &errors)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkReply` 发出的通知信号 `sslErrors`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `errors`：类型为 `const QList<QSslError> &`。没有默认值，调用时必须提供。传入 `const QList<QSslError> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QNetworkReply::uploadProgress(qint64 bytesSent, qint64 bytesTotal)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkReply` 发出的通知信号 `uploadProgress`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `bytesSent`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `bytesTotal`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QUrl QNetworkReply::url() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkReply::url` 用于计算、查询或取得与“url”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QUrl`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QUrl`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] qint64 QNetworkReply::writeData(const char *data, qint64 len)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkReply` 的核心操作 `writeData`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`qint64`。
- 参数 `data`：类型为 `const char *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `len`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `RawHeaderPair`

**API 类别：** 公有类型

**中文解读：** 这是 `QNetworkReply` 的 `Raw、Header、Pair` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

## 6. 深入实践与常见坑

### 生命周期和资源边界

manager 必须在线程事件循环中存活到 reply 完成；reply 完成后读取结果并调用 `deleteLater()`，不能在信号触发前直接释放。请求对象是值类型，reply 才是带有异步状态和资源的对象。

### 状态和错误边界

请求成功发出不等于 HTTP 成功，HTTP 状态码成功也不等于业务 JSON 有效。至少分别处理网络错误、HTTP 状态码、响应头、响应体解析和业务字段校验。上传/下载还要处理进度、分段读取和取消。

### 线程边界

QNetworkAccessManager、QNetworkReply 和相关请求应在同一个有事件循环的线程使用。跨线程时把网络对象整体放到目标线程，通过信号传递结果，不要跨线程直接读写 reply。

### 最容易出现的错误

不要把异步请求当同步函数；不要只检查 `error()` 而忽略 HTTP 状态码；不要在 readyRead 中假设一次就收到完整 body；不要在 GUI 线程用阻塞等待替代信号。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QNetworkReply` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
