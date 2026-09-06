# QNetworkRequest

> Qt 6.11.1 · Qt Network

## 1. 先建立直觉

**一句话定位：** `QNetworkRequest` 描述一次网络请求：URL、请求头、缓存策略、优先级和传输相关属性都放在这里。

**模块背景：** Qt Network 提供 TCP/UDP、HTTP、代理、DNS、SSL 和网络请求等异步网络能力。

### 这是什么

`QNetworkRequest` 描述一次网络请求：URL、请求头、缓存策略、优先级和传输相关属性都放在这里。

**内部模型：** 它是值类型，创建后传给 QNetworkAccessManager；请求对象本身不代表连接或响应。响应状态和错误要从 QNetworkReply 读取。

**适用场景：** 需要设置 URL、Content-Type、Authorization、User-Agent、缓存或重定向策略时使用。

**典型调用链：** 构造 URL -> setRawHeader/setHeader -> 按需设置属性 -> manager.get/post/request -> 从 reply 读取结果。

**先记住的坑：** 不要把敏感 token 写入日志；Content-Type 要和 body 匹配；URL 编码参数应使用 QUrlQuery；请求头和响应头是两个不同对象。

## 2. 依赖与对象关系

- 头文件：`#include <QNetworkRequest>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Network)
target_link_libraries(mytarget PRIVATE Qt6::Network)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

它是值类型，创建后传给 QNetworkAccessManager；请求对象本身不代表连接或响应。响应状态和错误要从 QNetworkReply 读取。

### 状态、生命周期和线程

**生命周期：** manager 必须在线程事件循环中存活到 reply 完成；reply 完成后读取结果并调用 `deleteLater()`，不能在信号触发前直接释放。请求对象是值类型，reply 才是带有异步状态和资源的对象。

**状态与结果：** 请求成功发出不等于 HTTP 成功，HTTP 状态码成功也不等于业务 JSON 有效。至少分别处理网络错误、HTTP 状态码、响应头、响应体解析和业务字段校验。上传/下载还要处理进度、分段读取和取消。

**线程与事件循环：** QNetworkAccessManager、QNetworkReply 和相关请求应在同一个有事件循环的线程使用。跨线程时把网络对象整体放到目标线程，通过信号传递结果，不要跨线程直接读写 reply。

## 3. 直接使用

需要设置 URL、Content-Type、Authorization、User-Agent、缓存或重定向策略时使用。 使用时通常按这个过程组织：构造 URL -> setRawHeader/setHeader -> 按需设置属性 -> manager.get/post/request -> 从 reply 读取结果。

```cpp
QNetworkRequest request(QUrl("https://example.com/api"));
request.setHeader(QNetworkRequest::ContentTypeHeader,
                  QStringLiteral("application/json"));
request.setRawHeader("Authorization", "Bearer token");
QNetworkReply *reply = manager->post(request, jsonData);
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum Attribute { HttpStatusCodeAttribute, HttpReasonPhraseAttribute, RedirectionTargetAttribute, ConnectionEncryptedAttribute, CacheLoadControlAttribute, …, UserMax }`
- `enum CacheLoadControl { AlwaysNetwork, PreferNetwork, PreferCache, AlwaysCache }`
- `enum KnownHeaders { ContentDispositionHeader, ContentTypeHeader, ContentLengthHeader, LocationHeader, LastModifiedHeader, …, ServerHeader }`
- `enum LoadControl { Automatic, Manual }`
- `enum Priority { HighPriority, NormalPriority, LowPriority }`
- `enum RedirectPolicy { ManualRedirectPolicy, NoLessSafeRedirectPolicy, SameOriginRedirectPolicy, UserVerifiedRedirectPolicy }`
- `enum TransferTimeoutConstant { DefaultTransferTimeoutConstant }`

### 公有函数

- `QNetworkRequest()`
- `QNetworkRequest(const QUrl &url)`
- `QNetworkRequest(const QNetworkRequest &other)`
- `~QNetworkRequest()`
- `QVariant attribute(QNetworkRequest::Attribute code, const QVariant &defaultValue = QVariant()) const`
- `(since 6.2) qint64 decompressedSafetyCheckThreshold() const`
- `bool hasRawHeader(QAnyStringView headerName) const`
- `QVariant header(QNetworkRequest::KnownHeaders header) const`
- `(since 6.8) QHttpHeaders headers() const`
- `(since 6.5) QHttp1Configuration http1Configuration() const`
- `QHttp2Configuration http2Configuration() const`
- `int maximumRedirectsAllowed() const`
- `QObject * originatingObject() const`
- `QString peerVerifyName() const`
- `QNetworkRequest::Priority priority() const`
- `QByteArray rawHeader(QAnyStringView headerName) const`
- `QList<QByteArray> rawHeaderList() const`
- `void setAttribute(QNetworkRequest::Attribute code, const QVariant &value)`
- `(since 6.2) void setDecompressedSafetyCheckThreshold(qint64 threshold)`
- `void setHeader(QNetworkRequest::KnownHeaders header, const QVariant &value)`
- `(since 6.8) void setHeaders(QHttpHeaders &&newHeaders)`
- `(since 6.8) void setHeaders(const QHttpHeaders &newHeaders)`
- `(since 6.5) void setHttp1Configuration(const QHttp1Configuration &configuration)`
- `void setHttp2Configuration(const QHttp2Configuration &configuration)`
- `void setMaximumRedirectsAllowed(int maxRedirectsAllowed)`
- `void setOriginatingObject(QObject *object)`
- `void setPeerVerifyName(const QString &peerName)`
- `void setPriority(QNetworkRequest::Priority priority)`
- `void setRawHeader(const QByteArray &headerName, const QByteArray &headerValue)`
- `void setSslConfiguration(const QSslConfiguration &config)`
- `(since 6.11) void setTcpKeepAliveIdleTimeBeforeProbes(std::chrono::seconds idle)`
- `(since 6.11) void setTcpKeepAliveIntervalBetweenProbes(std::chrono::seconds interval)`
- `(since 6.11) void setTcpKeepAliveProbeCount(int probes)`
- `void setTransferTimeout(int timeout)`
- `(since 6.7) void setTransferTimeout(std::chrono::milliseconds duration = DefaultTransferTimeout)`
- `void setUrl(const QUrl &url)`
- `QSslConfiguration sslConfiguration() const`
- `void swap(QNetworkRequest &other)`
- `(since 6.11) std::chrono::seconds tcpKeepAliveIdleTimeBeforeProbes() const`
- `(since 6.11) std::chrono::seconds tcpKeepAliveIntervalBetweenProbes() const`
- `(since 6.11) int tcpKeepAliveProbeCount() const`
- `int transferTimeout() const`
- `(since 6.7) std::chrono::milliseconds transferTimeoutAsDuration() const`
- `QUrl url() const`
- `bool operator!=(const QNetworkRequest &other) const`
- `QNetworkRequest & operator=(const QNetworkRequest &other)`
- `bool operator==(const QNetworkRequest &other) const`

### 静态公有成员

- `const std::chrono::std::chrono::milliseconds DefaultTransferTimeout`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 56 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QNetworkRequest::Attribute`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QNetworkRequest` 暴露的类型声明 `Attribute`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Attribute`。
- 属性名：`QNetworkRequest`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QNetworkRequest::CacheLoadControl`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QNetworkRequest` 暴露的类型声明 `Cache、加载、Control`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:CacheLoadControl`。
- 属性名：`QNetworkRequest`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QNetworkRequest::KnownHeaders`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QNetworkRequest` 暴露的类型声明 `Known、Headers`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:KnownHeaders`。
- 属性名：`QNetworkRequest`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QNetworkRequest::LoadControl`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QNetworkRequest` 暴露的类型声明 `加载、Control`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:LoadControl`。
- 属性名：`QNetworkRequest`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QNetworkRequest::Priority`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QNetworkRequest` 暴露的类型声明 `Priority`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Priority`。
- 属性名：`QNetworkRequest`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QNetworkRequest::RedirectPolicy`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QNetworkRequest` 暴露的类型声明 `Redirect、Policy`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:RedirectPolicy`。
- 属性名：`QNetworkRequest`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QNetworkRequest::TransferTimeoutConstant`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QNetworkRequest` 暴露的类型声明 `Transfer、超时、Constant`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:TransferTimeoutConstant`。
- 属性名：`QNetworkRequest`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QNetworkRequest::QNetworkRequest()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkRequest` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QNetworkRequest::QNetworkRequest(const QUrl &url)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkRequest` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `url`：类型为 `const QUrl &`。没有默认值，调用时必须提供。资源地址。要确认 scheme、编码、相对路径、重定向和是否包含敏感信息。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QNetworkRequest::QNetworkRequest(const QNetworkRequest &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkRequest` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `const QNetworkRequest &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QNetworkRequest::~QNetworkRequest()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkRequest` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVariant QNetworkRequest::attribute(QNetworkRequest::Attribute code, const QVariant &defaultValue = QVariant()) const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkRequest::attribute` 用于计算、查询或取得与“attribute”相关的操作。调用时要先确认当前状态和 `code`、`defaultValue` 的有效范围；返回类型是 `QVariant`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVariant`。
- 参数 `code`：类型为 `QNetworkRequest::Attribute`。没有默认值，调用时必须提供。传入 `QNetworkRequest::Attribute` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `defaultValue`：类型为 `const QVariant &`。默认值为 `QVariant()`。传入 `const QVariant &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] qint64 QNetworkRequest::decompressedSafetyCheckThreshold() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkRequest::decompressedSafetyCheckThreshold` 用于计算、查询或取得与“decompressed、Safety、Check、Threshold”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qint64`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qint64`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QNetworkRequest::hasRawHeader(QAnyStringView headerName) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `hasRawHeader`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `headerName`：类型为 `QAnyStringView`。没有默认值，调用时必须提供。传入 `QAnyStringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVariant QNetworkRequest::header(QNetworkRequest::KnownHeaders header) const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkRequest::header` 用于计算、查询或取得与“header”相关的操作。调用时要先确认当前状态和 `header` 的有效范围；返回类型是 `QVariant`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVariant`。
- 参数 `header`：类型为 `QNetworkRequest::KnownHeaders`。没有默认值，调用时必须提供。传入 `QNetworkRequest::KnownHeaders` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.8] QHttpHeaders QNetworkRequest::headers() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkRequest::headers` 用于计算、查询或取得与“headers”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QHttpHeaders`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QHttpHeaders`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.5] QHttp1Configuration QNetworkRequest::http1Configuration() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkRequest::http1Configuration` 用于计算、查询或取得与“http、1、Configuration”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QHttp1Configuration`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QHttp1Configuration`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QHttp2Configuration QNetworkRequest::http2Configuration() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkRequest::http2Configuration` 用于计算、查询或取得与“http、2、Configuration”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QHttp2Configuration`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QHttp2Configuration`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QNetworkRequest::maximumRedirectsAllowed() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkRequest::maximumRedirectsAllowed` 用于计算、查询或取得与“最大值、Redirects、Allowed”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QObject *QNetworkRequest::originatingObject() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkRequest::originatingObject` 用于计算、查询或取得与“originating、Object”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QObject *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QObject *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QNetworkRequest::peerVerifyName() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkRequest::peerVerifyName` 用于计算、查询或取得与“peer、Verify、名称”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QNetworkRequest::Priority QNetworkRequest::priority() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkRequest::priority` 用于计算、查询或取得与“priority”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QNetworkRequest::Priority`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QNetworkRequest::Priority`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray QNetworkRequest::rawHeader(QAnyStringView headerName) const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkRequest::rawHeader` 用于计算、查询或取得与“raw、Header”相关的操作。调用时要先确认当前状态和 `headerName` 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `headerName`：类型为 `QAnyStringView`。没有默认值，调用时必须提供。传入 `QAnyStringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QByteArray> QNetworkRequest::rawHeaderList() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkRequest::rawHeaderList` 用于计算、查询或取得与“raw、Header、List”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<QByteArray>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QByteArray>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkRequest::setAttribute(QNetworkRequest::Attribute code, const QVariant &value)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setAttribute`。调用它会改变 `QNetworkRequest` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `code`：类型为 `QNetworkRequest::Attribute`。没有默认值，调用时必须提供。传入 `QNetworkRequest::Attribute` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const QVariant &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] void QNetworkRequest::setDecompressedSafetyCheckThreshold(qint64 threshold)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setDecompressedSafetyCheckThreshold`。调用它会改变 `QNetworkRequest` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `threshold`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkRequest::setHeader(QNetworkRequest::KnownHeaders header, const QVariant &value)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setHeader`。调用它会改变 `QNetworkRequest` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `header`：类型为 `QNetworkRequest::KnownHeaders`。没有默认值，调用时必须提供。传入 `QNetworkRequest::KnownHeaders` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const QVariant &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.8] void QNetworkRequest::setHeaders(QHttpHeaders &&newHeaders)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setHeaders`。调用它会改变 `QNetworkRequest` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `newHeaders`：类型为 `QHttpHeaders &&`。没有默认值，调用时必须提供。传入 `QHttpHeaders &&` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.8] void QNetworkRequest::setHeaders(const QHttpHeaders &newHeaders)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setHeaders`。调用它会改变 `QNetworkRequest` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `newHeaders`：类型为 `const QHttpHeaders &`。没有默认值，调用时必须提供。传入 `const QHttpHeaders &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.5] void QNetworkRequest::setHttp1Configuration(const QHttp1Configuration &configuration)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setHttp1Configuration`。调用它会改变 `QNetworkRequest` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `configuration`：类型为 `const QHttp1Configuration &`。没有默认值，调用时必须提供。传入 `const QHttp1Configuration &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkRequest::setHttp2Configuration(const QHttp2Configuration &configuration)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setHttp2Configuration`。调用它会改变 `QNetworkRequest` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `configuration`：类型为 `const QHttp2Configuration &`。没有默认值，调用时必须提供。传入 `const QHttp2Configuration &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkRequest::setMaximumRedirectsAllowed(int maxRedirectsAllowed)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setMaximumRedirectsAllowed`。调用它会改变 `QNetworkRequest` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `maxRedirectsAllowed`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkRequest::setOriginatingObject(QObject *object)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setOriginatingObject`。调用它会改变 `QNetworkRequest` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `object`：类型为 `QObject *`。没有默认值，调用时必须提供。Qt 对象参数。要确认对象有效、线程归属、所有权和该 API 是否只处理直接子对象。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkRequest::setPeerVerifyName(const QString &peerName)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPeerVerifyName`。调用它会改变 `QNetworkRequest` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `peerName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkRequest::setPriority(QNetworkRequest::Priority priority)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPriority`。调用它会改变 `QNetworkRequest` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `priority`：类型为 `QNetworkRequest::Priority`。没有默认值，调用时必须提供。传入 `QNetworkRequest::Priority` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkRequest::setRawHeader(const QByteArray &headerName, const QByteArray &headerValue)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setRawHeader`。调用它会改变 `QNetworkRequest` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `headerName`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `headerValue`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkRequest::setSslConfiguration(const QSslConfiguration &config)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSslConfiguration`。调用它会改变 `QNetworkRequest` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `config`：类型为 `const QSslConfiguration &`。没有默认值，调用时必须提供。传入 `const QSslConfiguration &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.11] void QNetworkRequest::setTcpKeepAliveIdleTimeBeforeProbes(std::chrono::seconds idle)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setTcpKeepAliveIdleTimeBeforeProbes`。调用它会改变 `QNetworkRequest` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `idle`：类型为 `std::chrono::seconds`。没有默认值，调用时必须提供。传入 `std::chrono::seconds` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.11] void QNetworkRequest::setTcpKeepAliveIntervalBetweenProbes(std::chrono::seconds interval)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setTcpKeepAliveIntervalBetweenProbes`。调用它会改变 `QNetworkRequest` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `interval`：类型为 `std::chrono::seconds`。没有默认值，调用时必须提供。时间间隔，Qt 定时器通常使用毫秒；要检查 0、负数和超出范围时的语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.11] void QNetworkRequest::setTcpKeepAliveProbeCount(int probes)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setTcpKeepAliveProbeCount`。调用它会改变 `QNetworkRequest` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `probes`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkRequest::setTransferTimeout(int timeout)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setTransferTimeout`。调用它会改变 `QNetworkRequest` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `timeout`：类型为 `int`。没有默认值，调用时必须提供。超时时间或超时对象，可能表示等待时长，也可能表示 QNetworkReply/QTimer 等异步对象，不能只看名称判断。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.7] void QNetworkRequest::setTransferTimeout(std::chrono::milliseconds duration = DefaultTransferTimeout)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setTransferTimeout`。调用它会改变 `QNetworkRequest` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `duration`：类型为 `std::chrono::milliseconds`。默认值为 `DefaultTransferTimeout`。持续时间，通常以毫秒表示；要确认 0、负数、循环和平台精度。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkRequest::setUrl(const QUrl &url)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setUrl`。调用它会改变 `QNetworkRequest` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `url`：类型为 `const QUrl &`。没有默认值，调用时必须提供。资源地址。要确认 scheme、编码、相对路径、重定向和是否包含敏感信息。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslConfiguration QNetworkRequest::sslConfiguration() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkRequest::sslConfiguration` 用于计算、查询或取得与“ssl、Configuration”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSslConfiguration`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSslConfiguration`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] void QNetworkRequest::swap(QNetworkRequest &other)`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkRequest::swap` 用于执行与“swap”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `other`：类型为 `QNetworkRequest &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.11] std::chrono::seconds QNetworkRequest::tcpKeepAliveIdleTimeBeforeProbes() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkRequest::tcpKeepAliveIdleTimeBeforeProbes` 用于计算、查询或取得与“tcp、Keep、Alive、Idle、时间、Before、Probes”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `std::chrono::seconds`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`std::chrono::seconds`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.11] std::chrono::seconds QNetworkRequest::tcpKeepAliveIntervalBetweenProbes() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkRequest::tcpKeepAliveIntervalBetweenProbes` 用于计算、查询或取得与“tcp、Keep、Alive、间隔、Between、Probes”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `std::chrono::seconds`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`std::chrono::seconds`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.11] int QNetworkRequest::tcpKeepAliveProbeCount() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkRequest::tcpKeepAliveProbeCount` 用于计算、查询或取得与“tcp、Keep、Alive、Probe、数量统计”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QNetworkRequest::transferTimeout() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkRequest::transferTimeout` 用于计算、查询或取得与“transfer、超时”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.7] std::chrono::milliseconds QNetworkRequest::transferTimeoutAsDuration() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkRequest::transferTimeoutAsDuration` 用于计算、查询或取得与“transfer、超时、As、持续时间”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `std::chrono::milliseconds`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`std::chrono::milliseconds`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QUrl QNetworkRequest::url() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkRequest::url` 用于计算、查询或取得与“url”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QUrl`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QUrl`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QNetworkRequest::operator!=(const QNetworkRequest &other) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkRequest` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `other`：类型为 `const QNetworkRequest &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QNetworkRequest &QNetworkRequest::operator=(const QNetworkRequest &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkRequest` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QNetworkRequest &`。
- 参数 `other`：类型为 `const QNetworkRequest &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QNetworkRequest::operator==(const QNetworkRequest &other) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkRequest` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `other`：类型为 `const QNetworkRequest &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const std::chrono::std::chrono::milliseconds QNetworkRequest::DefaultTransferTimeout`

**API 类别：** Member Variable Documentation

**中文解读：** 这是 `QNetworkRequest` 的配置属性。初始化或状态切换时通过 `setDefaultTransferTimeout(...)` 设置，之后用 `DefaultTransferTimeout()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:chrono::std::chrono::milliseconds QNetworkRequest::DefaultTransferTimeout`。
- 属性名：`std`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const std::chrono::std::chrono::milliseconds DefaultTransferTimeout`

**API 类别：** 静态公有成员

**中文解读：** 这是 `QNetworkRequest` 的配置属性。初始化或状态切换时通过 `setConst(...)` 设置，之后用 `const()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:chrono::std::chrono::milliseconds DefaultTransferTimeout`。
- 属性名：`std`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

## 6. 深入实践与常见坑

### 生命周期和资源边界

manager 必须在线程事件循环中存活到 reply 完成；reply 完成后读取结果并调用 `deleteLater()`，不能在信号触发前直接释放。请求对象是值类型，reply 才是带有异步状态和资源的对象。

### 状态和错误边界

请求成功发出不等于 HTTP 成功，HTTP 状态码成功也不等于业务 JSON 有效。至少分别处理网络错误、HTTP 状态码、响应头、响应体解析和业务字段校验。上传/下载还要处理进度、分段读取和取消。

### 线程边界

QNetworkAccessManager、QNetworkReply 和相关请求应在同一个有事件循环的线程使用。跨线程时把网络对象整体放到目标线程，通过信号传递结果，不要跨线程直接读写 reply。

### 最容易出现的错误

不要把敏感 token 写入日志；Content-Type 要和 body 匹配；URL 编码参数应使用 QUrlQuery；请求头和响应头是两个不同对象。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QNetworkRequest` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
