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

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QNetworkRequestFactory::QNetworkRequestFactory()`

**作用与语义：**

创建一个新的 QNetworkRequestFactory 对象。使用 `setBaseUrl()` 设置请求的有效基础 URL。

### `[explicit] QNetworkRequestFactory::QNetworkRequestFactory(const QUrl &baseUrl)`

**作用与语义：**

创建一个新的QNetworkRequestFactory对象，初始化`baseUrl`的基础URL。基础URL用于填充后续的网络请求。
如果 URL 包含路径组件，将被提取并作为后续网络请求的基础路径。这意味着在请求单个请求时提供的任何路径都会附加到该基础路径上，如下图所示：

**官方示例：**

```cpp
 // Here the API version v2 is used as the base path:
 QNetworkRequestFactory api{{"https://example.com/v2"_L1}};
 // ...
 manager.get(api.createRequest("models"_L1)); // https://example.com/v2/models
 // Equivalent with a leading '/'
 manager.get(api.createRequest("/models"_L1)); // https://example.com/v2/models
```

### `QNetworkRequestFactory::QNetworkRequestFactory(const QNetworkRequestFactory &other)`

**作用与语义：**

创建`other`副本。

### `[constexpr noexcept] QNetworkRequestFactory::QNetworkRequestFactory(QNetworkRequestFactory &&other)`

**作用与语义：**

从`other`移动建造工厂。
注意：移出对象 `other` 处于部分成形状态，唯一有效的操作是销毁和赋值。

### `[noexcept] QNetworkRequestFactory::~QNetworkRequestFactory()`

**作用与语义：**

摧毁了这个`QNetworkRequestFactory`物体。

### `[since 6.8] QVariant QNetworkRequestFactory::attribute(QNetworkRequest::Attribute attribute) const`

**作用与语义：**

返回与`attribute`关联的值。如果属性未被设置，返回默认构造的`QVariant`。

### `[since 6.8] QVariant QNetworkRequestFactory::attribute(QNetworkRequest::Attribute attribute, const QVariant &defaultValue) const`

**作用与语义：**

返回与`attribute`关联的值。如果属性未被设置，返回`defaultValue`。

### `QUrl QNetworkRequestFactory::baseUrl() const`

**作用与语义：**

返回用于各个请求的基础URL。
基础URL可能包含路径组件。该路径用作生成单个请求时提供的路径“前缀”。

### `QByteArray QNetworkRequestFactory::bearerToken() const`

**作用与语义：**

返回已设定的持有人令牌。
如果存在，持有令牌用于设置请求的`Authorization: Bearer my_token`头。这是一种常见的授权约定，作为额外的便利。
获取持有人令牌的方法各不相同。标准方法包括 `OAuth2` 和服务提供商的网站/仪表盘。持有人令牌会随时间变化。例如，当更新为刷新令牌时，必须始终重新设置新令牌，确保后续请求拥有最新有效的令牌。
持有人令牌的存在不会影响`commonHeaders()`的挂牌。如果`commonHeaders()`也列出`Authorization`头部，则该头部将被覆盖。

### `[since 6.8] void QNetworkRequestFactory::clearAttribute(QNetworkRequest::Attribute attribute)`

**作用与语义：**

清除`attribute`设置到这个工厂。

### `[since 6.8] void QNetworkRequestFactory::clearAttributes()`

**作用与语义：**

清除所有设置到该工厂的属性。

### `void QNetworkRequestFactory::clearBearerToken()`

**作用与语义：**

清除承载令牌。

### `void QNetworkRequestFactory::clearCommonHeaders()`

**作用与语义：**

清除当前的标题。

### `void QNetworkRequestFactory::clearPassword()`

**作用与语义：**

清除了该工厂设置的密码。

### `void QNetworkRequestFactory::clearQueryParameters()`

**作用与语义：**

清除查询参数。

### `void QNetworkRequestFactory::clearUserName()`

**作用与语义：**

清除设置为此工厂的用户名。

### `QHttpHeaders QNetworkRequestFactory::commonHeaders() const`

**作用与语义：**

返回当前设置的头部。

### `QNetworkRequest QNetworkRequestFactory::createRequest() const`

**作用与语义：**

返回`QNetworkRequest`。
返回的请求会被填入该工厂配置的数据。

### `QNetworkRequest QNetworkRequestFactory::createRequest(const QString &path) const`

**作用与语义：**

还给`QNetworkRequest`。
返回请求的URL是通过在`baseUrl`上附加提供的`path`形成的（本身可能包含路径分量）。

### `QNetworkRequest QNetworkRequestFactory::createRequest(const QUrlQuery &query) const`

**作用与语义：**

回来`QNetworkRequest`。
返回请求的URL是通过在`baseUrl`后附加提供的`query`形成的。

### `QNetworkRequest QNetworkRequestFactory::createRequest(const QString &path, const QUrlQuery &query) const`

**作用与语义：**

返回`QNetworkRequest`。
返回的请求 URL 是通过在`baseUrl`上附加提供的`path`和`query`形成的（可能包含路径成分）。
如果提供的`path`包含查询项，它们将与`query`中的项合并。

### `QString QNetworkRequestFactory::password() const`

**作用与语义：**

返回该工厂设置的密码。

### `[since 6.8] QNetworkRequest::Priority QNetworkRequestFactory::priority() const`

**作用与语义：**

返回该工厂未来创建请求的优先级。

### `QUrlQuery QNetworkRequestFactory::queryParameters() const`

**作用与语义：**

返回添加到单个请求查询参数的查询参数。查询参数被添加到单个`createRequest()`调用中提供的任何潜在查询参数。
重复查询参数的使用场景取决于服务器，但典型例子包括语言设置 `?lang=en`、格式规范`?format=json`、API 版本规范`?version=1.0`和 API 密钥认证。

### `[since 6.8] void QNetworkRequestFactory::setAttribute(QNetworkRequest::Attribute attribute, const QVariant &value)`

**作用与语义：**

将与 `attribute` 关联的值设置为 `value`。如果属性已经设置，则替换之前的值。属性被设置为该工厂未来创建的任何请求。

### `void QNetworkRequestFactory::setBaseUrl(const QUrl &url)`

**作用与语义：**

将单个请求中使用的基础URL设置为`url`。

### `void QNetworkRequestFactory::setBearerToken(const QByteArray &token)`

**作用与语义：**

将持有者令牌设置为`token`。

### `void QNetworkRequestFactory::setCommonHeaders(const QHttpHeaders &headers)`

**作用与语义：**

集合`headers`所有请求共有的。
这些头被添加到单个请求的头中。这是一种方便设置重复请求头的机制。

### `void QNetworkRequestFactory::setPassword(const QString &password)`

**作用与语义：**

把这个工厂的密码设为`password`。
密码在请求URL中设置，`createRequest()`被调用时。当服务器表示需要认证时，该`QRestAccessManager`/`QNetworkAccessManager`会尝试使用这些凭证。

### `[since 6.8] void QNetworkRequestFactory::setPriority(QNetworkRequest::Priority priority)`

**作用与语义：**

设置该工厂未来请求的优先级，`priority`。
默认优先级是`QNetworkRequest::NormalPriority`。

### `void QNetworkRequestFactory::setQueryParameters(const QUrlQuery &query)`

**作用与语义：**

设置`query`参数，添加到单个请求的查询参数上。

### `void QNetworkRequestFactory::setSslConfiguration(const QSslConfiguration &configuration)`

**作用与语义：**

将SSL配置设置为`configuration`。

### `void QNetworkRequestFactory::setTransferTimeout(std::chrono::milliseconds timeout)`

**作用与语义：**

`timeout`转运时使用套装。

### `void QNetworkRequestFactory::setUserName(const QString &userName)`

**作用与语义：**

把这家工厂的用户名设为`userName`。
用户名在请求URL中设置`createRequest()`当被调用时。当服务器表示需要认证时，`QRestAccessManager`/`QNetworkAccessManager`会尝试使用这些凭证。

### `QSslConfiguration QNetworkRequestFactory::sslConfiguration() const`

**作用与语义：**

将SSL配置返回到该工厂。SSL配置设置为每个单独请求。

### `[noexcept] void QNetworkRequestFactory::swap(QNetworkRequestFactory &other)`

**作用与语义：**

把这个工厂换成`other`。这个操作非常快，从不失败。

### `std::chrono::milliseconds QNetworkRequestFactory::transferTimeout() const`

**作用与语义：**

返回传输时使用的超时。

### `QString QNetworkRequestFactory::userName() const`

**作用与语义：**

会将用户名设置归还到这个工厂。

### `[noexcept] QNetworkRequestFactory &QNetworkRequestFactory::operator=(QNetworkRequestFactory &&other)`

**作用与语义：**

Move-assign `other`并返回该工厂的引用。
注意：移出对象 `other` 处于部分成形状态，唯一有效的操作是销毁和赋值。

### `QNetworkRequestFactory &QNetworkRequestFactory::operator=(const QNetworkRequestFactory &other)`

**作用与语义：**

创建`other`副本并返回该工厂的引用。

### `QDebug operator<<(QDebug debug, const QNetworkRequestFactory &factory)`

**作用与语义：**

`factory`写入`debug`流。

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
