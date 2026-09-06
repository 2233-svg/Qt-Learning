# QNetworkRequestFactory

> Qt 6.11.1 · Qt Network

## 1. 先建立直觉

**一句话定位：** `QNetworkRequestFactory` 是 Qt Network 的“网络请求工厂”类型，负责描述请求/地址/连接状态或承载异步网络数据。

**模块背景：** Qt Network 提供 TCP/UDP、HTTP、代理、DNS、SSL 和网络请求等异步网络能力。

### 这是什么

`QNetworkRequestFactory` 是 异步网络机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 网络请求通常由管理器创建并调度，返回一个代表本次操作的 reply。连接建立、DNS、发送、接收和错误都是事件驱动的阶段；响应头、状态码、body 和传输错误分别表达不同层次的信息。

**适用场景：** 创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要把异步请求当同步函数；不要只检查 `error()` 而忽略 HTTP 状态码；不要在 readyRead 中假设一次就收到完整 body；不要在 GUI 线程用阻塞等待替代信号。

## 2. 依赖与对象关系

- 头文件：`#include <QNetworkRequestFactory>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Network)
target_link_libraries(mytarget PRIVATE Qt6::Network)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

网络请求通常由管理器创建并调度，返回一个代表本次操作的 reply。连接建立、DNS、发送、接收和错误都是事件驱动的阶段；响应头、状态码、body 和传输错误分别表达不同层次的信息。

### 状态、生命周期和线程

**生命周期：** manager 必须在线程事件循环中存活到 reply 完成；reply 完成后读取结果并调用 `deleteLater()`，不能在信号触发前直接释放。请求对象是值类型，reply 才是带有异步状态和资源的对象。

**状态与结果：** 请求成功发出不等于 HTTP 成功，HTTP 状态码成功也不等于业务 JSON 有效。至少分别处理网络错误、HTTP 状态码、响应头、响应体解析和业务字段校验。上传/下载还要处理进度、分段读取和取消。

**线程与事件循环：** QNetworkAccessManager、QNetworkReply 和相关请求应在同一个有事件循环的线程使用。跨线程时把网络对象整体放到目标线程，通过信号传递结果，不要跨线程直接读写 reply。

## 3. 直接使用

创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

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

### 公有函数

- `QNetworkRequestFactory()`
- `QNetworkRequestFactory(const QUrl &baseUrl)`
- `QNetworkRequestFactory(const QNetworkRequestFactory &other)`
- `QNetworkRequestFactory(QNetworkRequestFactory &&other)`
- `~QNetworkRequestFactory()`
- `(since 6.8) QVariant attribute(QNetworkRequest::Attribute attribute) const`
- `(since 6.8) QVariant attribute(QNetworkRequest::Attribute attribute, const QVariant &defaultValue) const`
- `QUrl baseUrl() const`
- `QByteArray bearerToken() const`
- `(since 6.8) void clearAttribute(QNetworkRequest::Attribute attribute)`
- `(since 6.8) void clearAttributes()`
- `void clearBearerToken()`
- `void clearCommonHeaders()`
- `void clearPassword()`
- `void clearQueryParameters()`
- `void clearUserName()`
- `QHttpHeaders commonHeaders() const`
- `QNetworkRequest createRequest() const`
- `QNetworkRequest createRequest(const QString &path) const`
- `QNetworkRequest createRequest(const QUrlQuery &query) const`
- `QNetworkRequest createRequest(const QString &path, const QUrlQuery &query) const`
- `QString password() const`
- `(since 6.8) QNetworkRequest::Priority priority() const`
- `QUrlQuery queryParameters() const`
- `(since 6.8) void setAttribute(QNetworkRequest::Attribute attribute, const QVariant &value)`
- `void setBaseUrl(const QUrl &url)`
- `void setBearerToken(const QByteArray &token)`
- `void setCommonHeaders(const QHttpHeaders &headers)`
- `void setPassword(const QString &password)`
- `(since 6.8) void setPriority(QNetworkRequest::Priority priority)`
- `void setQueryParameters(const QUrlQuery &query)`
- `void setSslConfiguration(const QSslConfiguration &configuration)`
- `void setTransferTimeout(std::chrono::milliseconds timeout)`
- `void setUserName(const QString &userName)`
- `QSslConfiguration sslConfiguration() const`
- `void swap(QNetworkRequestFactory &other)`
- `std::chrono::milliseconds transferTimeout() const`
- `QString userName() const`
- `QNetworkRequestFactory & operator=(QNetworkRequestFactory &&other)`
- `QNetworkRequestFactory & operator=(const QNetworkRequestFactory &other)`

### 相关非成员函数

- `QDebug operator<<(QDebug debug, const QNetworkRequestFactory &factory)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 41 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `QNetworkRequestFactory::QNetworkRequestFactory()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkRequestFactory` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QNetworkRequestFactory::QNetworkRequestFactory(const QUrl &baseUrl)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkRequestFactory` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `baseUrl`：类型为 `const QUrl &`。没有默认值，调用时必须提供。传入 `const QUrl &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QNetworkRequestFactory::QNetworkRequestFactory(const QNetworkRequestFactory &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkRequestFactory` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `const QNetworkRequestFactory &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] QNetworkRequestFactory::QNetworkRequestFactory(QNetworkRequestFactory &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkRequestFactory` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `QNetworkRequestFactory &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QNetworkRequestFactory::~QNetworkRequestFactory()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkRequestFactory` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.8] QVariant QNetworkRequestFactory::attribute(QNetworkRequest::Attribute attribute) const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkRequestFactory::attribute` 用于计算、查询或取得与“attribute”相关的操作。调用时要先确认当前状态和 `attribute` 的有效范围；返回类型是 `QVariant`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVariant`。
- 参数 `attribute`：类型为 `QNetworkRequest::Attribute`。没有默认值，调用时必须提供。传入 `QNetworkRequest::Attribute` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.8] QVariant QNetworkRequestFactory::attribute(QNetworkRequest::Attribute attribute, const QVariant &defaultValue) const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkRequestFactory::attribute` 用于计算、查询或取得与“attribute”相关的操作。调用时要先确认当前状态和 `attribute`、`defaultValue` 的有效范围；返回类型是 `QVariant`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVariant`。
- 参数 `attribute`：类型为 `QNetworkRequest::Attribute`。没有默认值，调用时必须提供。传入 `QNetworkRequest::Attribute` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `defaultValue`：类型为 `const QVariant &`。没有默认值，调用时必须提供。传入 `const QVariant &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QUrl QNetworkRequestFactory::baseUrl() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkRequestFactory::baseUrl` 用于计算、查询或取得与“base、Url”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QUrl`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QUrl`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray QNetworkRequestFactory::bearerToken() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkRequestFactory::bearerToken` 用于计算、查询或取得与“bearer、Token”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.8] void QNetworkRequestFactory::clearAttribute(QNetworkRequest::Attribute attribute)`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkRequestFactory::clearAttribute` 用于执行与“清空、Attribute”相关的操作。调用时要先确认当前状态和 `attribute` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `attribute`：类型为 `QNetworkRequest::Attribute`。没有默认值，调用时必须提供。传入 `QNetworkRequest::Attribute` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.8] void QNetworkRequestFactory::clearAttributes()`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkRequestFactory::clearAttributes` 用于执行与“清空、Attributes”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkRequestFactory::clearBearerToken()`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkRequestFactory::clearBearerToken` 用于执行与“清空、Bearer、Token”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkRequestFactory::clearCommonHeaders()`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkRequestFactory::clearCommonHeaders` 用于执行与“清空、Common、Headers”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkRequestFactory::clearPassword()`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkRequestFactory::clearPassword` 用于执行与“清空、Password”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkRequestFactory::clearQueryParameters()`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkRequestFactory::clearQueryParameters` 用于执行与“清空、查询、Parameters”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkRequestFactory::clearUserName()`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkRequestFactory::clearUserName` 用于执行与“清空、User、名称”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QHttpHeaders QNetworkRequestFactory::commonHeaders() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkRequestFactory::commonHeaders` 用于计算、查询或取得与“common、Headers”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QHttpHeaders`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QHttpHeaders`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QNetworkRequest QNetworkRequestFactory::createRequest() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkRequestFactory::createRequest` 用于计算、查询或取得与“创建、请求”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QNetworkRequest`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QNetworkRequest`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QNetworkRequest QNetworkRequestFactory::createRequest(const QString &path) const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkRequestFactory::createRequest` 用于计算、查询或取得与“创建、请求”相关的操作。调用时要先确认当前状态和 `path` 的有效范围；返回类型是 `QNetworkRequest`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QNetworkRequest`。
- 参数 `path`：类型为 `const QString &`。没有默认值，调用时必须提供。路径字符串。要确认是相对路径还是绝对路径，以及它相对于哪个工作目录。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QNetworkRequest QNetworkRequestFactory::createRequest(const QUrlQuery &query) const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkRequestFactory::createRequest` 用于计算、查询或取得与“创建、请求”相关的操作。调用时要先确认当前状态和 `query` 的有效范围；返回类型是 `QNetworkRequest`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QNetworkRequest`。
- 参数 `query`：类型为 `const QUrlQuery &`。没有默认值，调用时必须提供。传入 `const QUrlQuery &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QNetworkRequest QNetworkRequestFactory::createRequest(const QString &path, const QUrlQuery &query) const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkRequestFactory::createRequest` 用于计算、查询或取得与“创建、请求”相关的操作。调用时要先确认当前状态和 `path`、`query` 的有效范围；返回类型是 `QNetworkRequest`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QNetworkRequest`。
- 参数 `path`：类型为 `const QString &`。没有默认值，调用时必须提供。路径字符串。要确认是相对路径还是绝对路径，以及它相对于哪个工作目录。
- 参数 `query`：类型为 `const QUrlQuery &`。没有默认值，调用时必须提供。传入 `const QUrlQuery &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QNetworkRequestFactory::password() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkRequestFactory::password` 用于计算、查询或取得与“password”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.8] QNetworkRequest::Priority QNetworkRequestFactory::priority() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkRequestFactory::priority` 用于计算、查询或取得与“priority”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QNetworkRequest::Priority`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QNetworkRequest::Priority`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QUrlQuery QNetworkRequestFactory::queryParameters() const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkRequestFactory` 的核心操作 `queryParameters`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`QUrlQuery`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.8] void QNetworkRequestFactory::setAttribute(QNetworkRequest::Attribute attribute, const QVariant &value)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setAttribute`。调用它会改变 `QNetworkRequestFactory` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `attribute`：类型为 `QNetworkRequest::Attribute`。没有默认值，调用时必须提供。传入 `QNetworkRequest::Attribute` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const QVariant &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkRequestFactory::setBaseUrl(const QUrl &url)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setBaseUrl`。调用它会改变 `QNetworkRequestFactory` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `url`：类型为 `const QUrl &`。没有默认值，调用时必须提供。资源地址。要确认 scheme、编码、相对路径、重定向和是否包含敏感信息。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkRequestFactory::setBearerToken(const QByteArray &token)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setBearerToken`。调用它会改变 `QNetworkRequestFactory` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `token`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkRequestFactory::setCommonHeaders(const QHttpHeaders &headers)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setCommonHeaders`。调用它会改变 `QNetworkRequestFactory` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `headers`：类型为 `const QHttpHeaders &`。没有默认值，调用时必须提供。传入 `const QHttpHeaders &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkRequestFactory::setPassword(const QString &password)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPassword`。调用它会改变 `QNetworkRequestFactory` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `password`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.8] void QNetworkRequestFactory::setPriority(QNetworkRequest::Priority priority)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPriority`。调用它会改变 `QNetworkRequestFactory` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `priority`：类型为 `QNetworkRequest::Priority`。没有默认值，调用时必须提供。传入 `QNetworkRequest::Priority` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkRequestFactory::setQueryParameters(const QUrlQuery &query)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setQueryParameters`。调用它会改变 `QNetworkRequestFactory` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `query`：类型为 `const QUrlQuery &`。没有默认值，调用时必须提供。传入 `const QUrlQuery &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkRequestFactory::setSslConfiguration(const QSslConfiguration &configuration)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSslConfiguration`。调用它会改变 `QNetworkRequestFactory` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `configuration`：类型为 `const QSslConfiguration &`。没有默认值，调用时必须提供。传入 `const QSslConfiguration &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkRequestFactory::setTransferTimeout(std::chrono::milliseconds timeout)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setTransferTimeout`。调用它会改变 `QNetworkRequestFactory` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `timeout`：类型为 `std::chrono::milliseconds`。没有默认值，调用时必须提供。超时时间或超时对象，可能表示等待时长，也可能表示 QNetworkReply/QTimer 等异步对象，不能只看名称判断。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkRequestFactory::setUserName(const QString &userName)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setUserName`。调用它会改变 `QNetworkRequestFactory` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `userName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslConfiguration QNetworkRequestFactory::sslConfiguration() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkRequestFactory::sslConfiguration` 用于计算、查询或取得与“ssl、Configuration”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSslConfiguration`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSslConfiguration`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] void QNetworkRequestFactory::swap(QNetworkRequestFactory &other)`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkRequestFactory::swap` 用于执行与“swap”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `other`：类型为 `QNetworkRequestFactory &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `std::chrono::milliseconds QNetworkRequestFactory::transferTimeout() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkRequestFactory::transferTimeout` 用于计算、查询或取得与“transfer、超时”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `std::chrono::milliseconds`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`std::chrono::milliseconds`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QNetworkRequestFactory::userName() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkRequestFactory::userName` 用于计算、查询或取得与“user、名称”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QNetworkRequestFactory &QNetworkRequestFactory::operator=(QNetworkRequestFactory &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkRequestFactory` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QNetworkRequestFactory &`。
- 参数 `other`：类型为 `QNetworkRequestFactory &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QNetworkRequestFactory &QNetworkRequestFactory::operator=(const QNetworkRequestFactory &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkRequestFactory` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QNetworkRequestFactory &`。
- 参数 `other`：类型为 `const QNetworkRequestFactory &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDebug operator<<(QDebug debug, const QNetworkRequestFactory &factory)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QNetworkRequestFactory` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDebug`。
- 参数 `debug`：类型为 `QDebug`。没有默认值，调用时必须提供。传入 `QDebug` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `factory`：类型为 `const QNetworkRequestFactory &`。没有默认值，调用时必须提供。传入 `const QNetworkRequestFactory &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

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

`QNetworkRequestFactory` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
