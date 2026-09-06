# QNetworkCookie

> Qt 6.11.1 · Qt Network

## 1. 先建立直觉

**一句话定位：** HTTP Cookie 值类型，负责保存名称、值、域、路径、过期时间和安全属性。

**模块背景：** Qt Network 提供 TCP/UDP、HTTP、代理、DNS、SSL 和网络请求等异步网络能力。

### 这是什么

`QNetworkCookie`：HTTP Cookie 值类型，负责保存名称、值、域、路径、过期时间和安全属性。

**内部模型：** 网络请求通常由管理器创建并调度，返回一个代表本次操作的 reply。连接建立、DNS、发送、接收和错误都是事件驱动的阶段；响应头、状态码、body 和传输错误分别表达不同层次的信息。

**适用场景：** 创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要把异步请求当同步函数；不要只检查 `error()` 而忽略 HTTP 状态码；不要在 readyRead 中假设一次就收到完整 body；不要在 GUI 线程用阻塞等待替代信号。

## 2. 依赖与对象关系

- 头文件：`#include <QNetworkCookie>`
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

- `enum RawForm { NameAndValueOnly, Full }`
- `(since 6.1) enum class SameSite { Default, None, Lax, Strict }`

### 公有函数

- `QNetworkCookie(const QByteArray &name = QByteArray(), const QByteArray &value = QByteArray())`
- `QNetworkCookie(const QNetworkCookie &other)`
- `~QNetworkCookie()`
- `QString domain() const`
- `QDateTime expirationDate() const`
- `bool hasSameIdentifier(const QNetworkCookie &other) const`
- `bool isHttpOnly() const`
- `bool isSecure() const`
- `bool isSessionCookie() const`
- `QByteArray name() const`
- `void normalize(const QUrl &url)`
- `QString path() const`
- `(since 6.1) QNetworkCookie::SameSite sameSitePolicy() const`
- `void setDomain(const QString &domain)`
- `void setExpirationDate(const QDateTime &date)`
- `void setHttpOnly(bool enable)`
- `void setName(const QByteArray &cookieName)`
- `void setPath(const QString &path)`
- `(since 6.1) void setSameSitePolicy(QNetworkCookie::SameSite sameSite)`
- `void setSecure(bool enable)`
- `void setValue(const QByteArray &value)`
- `void swap(QNetworkCookie &other)`
- `QByteArray toRawForm(QNetworkCookie::RawForm form = Full) const`
- `QByteArray value() const`
- `bool operator!=(const QNetworkCookie &other) const`
- `QNetworkCookie & operator=(const QNetworkCookie &other)`
- `bool operator==(const QNetworkCookie &other) const`

### 静态公有成员

- `QList<QNetworkCookie> parseCookies(QByteArrayView cookieString)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QNetworkCookie::RawForm`

**作用与语义：**

该枚举与`toRawForm()`函数一起使用，用于声明将返回哪种形式的Cookie。
- `QNetworkCookie::NameAndValueOnly`：`0`;使`toRawForm()`只返回cookie中的“NAME=VALUE”部分，以便以客户端请求的“Cookie：”头部“返回服务器。多个Cookie在”Cookie：“头字段中用分号分隔。
- `QNetworkCookie::Full`：`1`;使`toRawForm()`返回完整的 Cookie 内容，以便以服务器的“Set-Cookie：” 头部发送给客户端。
请注意，只有 cookie 的完整形式可以解析回其原始内容。

### `[since 6.1] enum class QNetworkCookie::SameSite`

**作用与语义：**

- `QNetworkCookie::SameSite::Default`：`0`;SameSite 未被设置。浏览器可将其解读为 None 或 Lax。
- `QNetworkCookie::SameSite::None`：`1`;Cookie 可以在所有上下文中发送。这曾经是默认设置，但最近的浏览器将 Lax 变为默认，现在要求 Cookie 既安全又必须设置 SameSite=None。
- `QNetworkCookie::SameSite::Lax`：`2`;Cookie 会在第三方网站发起的第一方请求和 GET 请求中发送。这是现代浏览器的默认设置（自 2020 年中期起）。
- `QNetworkCookie::SameSite::Strict`：`3`;Cookie 仅会在第一方情境下发送。
这个枚举是在Qt 6.1引入的。

### `[explicit] QNetworkCookie::QNetworkCookie(const QByteArray &name = QByteArray(), const QByteArray &value = QByteArray())`

**作用与语义：**

创建一个新的QNetworkCookie对象，将Cookie名初始化为`name`，其值初始化为`value`。
只有当 cookie 有名称时才有效。然而，该值对应用程序来说是不透明的，且为空的对远程服务器可能具有重要意义。

### `QNetworkCookie::QNetworkCookie(const QNetworkCookie &other)`

**作用与语义：**

通过复制`other`的内容创建新的 QNetworkCookie 对象。

### `[noexcept] QNetworkCookie::~QNetworkCookie()`

**作用与语义：**

摧毁了这个`QNetworkCookie`物体。

### `QString QNetworkCookie::domain() const`

**作用与语义：**

返回该 Cookie 关联的域名。这对应于 cookie 字符串中的“domain”字段。
请注意，这里的域名可能以点开头，但这并不是有效的主机名。但这意味着该 cookie 匹配所有以该域名结尾的主机名。

### `QDateTime QNetworkCookie::expirationDate() const`

**作用与语义：**

返回该 cookie 的有效期。如果该 cookie 是会话 cookie，返回的`QDateTime`将无效。如果日期已过去，则该 cookie 已过期，不应再次发送回远程服务器。
到期日期对应于cookie字符串中“过期”条目的参数。

### `bool QNetworkCookie::hasSameIdentifier(const QNetworkCookie &other) const`

**作用与语义：**

如果该 cookie 与 `other` 的标识符元组相同，返回`true`。标识符元组由名称、域名和路径组成。

### `bool QNetworkCookie::isHttpOnly() const`

**作用与语义：**

如果该cookie启用了“仅HttpOnly”标志，返回`true`。
仅“HttpOnly”的Cookie仅由网络请求和回复设置和检索;即HTTP协议。浏览器脚本无法访问该Cookie。

### `bool QNetworkCookie::isSecure() const`

**作用与语义：**

如果 cookie 字符串中指定了“安全”选项，返回`true`，否则返回 false。
安全Cookie可能包含私人信息，不应通过未加密连接重新发送。

### `bool QNetworkCookie::isSessionCookie() const`

**作用与语义：**

返回`true` 如果该 Cookie 是会话 Cookie。会话 Cookie 是没有有效期的 Cookie，这意味着当应用程序的会话概念结束时（通常是应用程序退出时）应丢弃它。

### `QByteArray QNetworkCookie::name() const`

**作用与语义：**

返回该 cookie 的名称。Cookie 唯一必须填写的字段是其名称，否则不被视为有效。

### `void QNetworkCookie::normalize(const QUrl &url)`

**作用与语义：**

该函数会规范 cookie 的路径和域（如果之前为空的话）。`url` 参数用于确定正确的域和路径。

### `[static] QList<QNetworkCookie> QNetworkCookie::parseCookies(QByteArrayView cookieString)`

**作用与语义：**

解析从服务器响应收到的 cookie 字符串`cookieString`，在“Set-Cookie：”头部中。如果出现解析错误，该函数返回一个空列表。
由于 HTTP 头部可以同时设置多个 Cookie，该函数会返回<`QNetworkCookie`>一个 `QList`，每个解析的 cookie 都对应一个。
注意：在6.7之前的Qt版本中，该功能仅使用`QByteArray`。

### `QString QNetworkCookie::path() const`

**作用与语义：**

返回与该 cookie 关联的路径。这对应于 cookie 字符串的“path”字段。

### `[since 6.1] QNetworkCookie::SameSite QNetworkCookie::sameSitePolicy() const`

**作用与语义：**

如果 cookie 字符串中指定了，返回“`SameSite`”选项;如果不存在，`SameSite::Default`返回。

### `void QNetworkCookie::setDomain(const QString &domain)`

**作用与语义：**

将与该 cookie 关联的域名设置为`domain`。

### `void QNetworkCookie::setExpirationDate(const QDateTime &date)`

**作用与语义：**

将该 cookie 的有效期设置为 `date`。将该 cookie 设置无效的有效期意味着它是会话 cookie。

### `void QNetworkCookie::setHttpOnly(bool enable)`

**作用与语义：**

将该 cookie 的“仅 HttpOnly” 标志设置为`enable`。

### `void QNetworkCookie::setName(const QByteArray &cookieName)`

**作用与语义：**

将该 Cookie 的名称设置为 `cookieName`。注意，将 Cookie 名称设置为空`QByteArray`会使该 Cookie 无效。

### `void QNetworkCookie::setPath(const QString &path)`

**作用与语义：**

将与该 cookie 关联的路径设置为`path`。

### `[since 6.1] void QNetworkCookie::setSameSitePolicy(QNetworkCookie::SameSite sameSite)`

**作用与语义：**

将该Cookie的“`SameSite`”选项设置为`sameSite`。

### `void QNetworkCookie::setSecure(bool enable)`

**作用与语义：**

将该 cookie 的安全标志设置为 `enable`。
安全Cookie可能包含私人信息，不应通过未加密连接重新发送。

### `void QNetworkCookie::setValue(const QByteArray &value)`

**作用与语义：**

将该 cookie 的值设置为`value`。

### `[noexcept] void QNetworkCookie::swap(QNetworkCookie &other)`

**作用与语义：**

将这个cookie与`other`交换。这个操作非常快，而且从未失败过。

### `QByteArray QNetworkCookie::toRawForm(QNetworkCookie::RawForm form = Full) const`

**作用与语义：**

返回该`QNetworkCookie`的原始形式。该函数返回的`QByteArray`适用于HTTP头，无论是在服务器响应（Set-Cookie首部）还是客户端请求（Cookie首部）。你可以选择两种格式之一，使用`form`。

### `QByteArray QNetworkCookie::value() const`

**作用与语义：**

返回该 cookie 的值，如 cookie 字符串中指定的。注意，如果 cookie 的值为空，它仍然有效。
Cookie 名称-值对对应用程序来说是不透明的：也就是说，它们的值没有任何意义。

### `bool QNetworkCookie::operator!=(const QNetworkCookie &other) const`

**作用与语义：**

如果该 cookie 不等于 `other`，返回`true`。

### `QNetworkCookie &QNetworkCookie::operator=(const QNetworkCookie &other)`

**作用与语义：**

将`QNetworkCookie`对象的内容`other`复制到该对象上。

### `bool QNetworkCookie::operator==(const QNetworkCookie &other) const`

**作用与语义：**

如果该 Cookie 等于 `other`，则返回 `true`。该函数只有在 Cookie 的所有字段相同时才返回 `true`。
然而，在某些情况下，同名的两个cookie可以被视为相等。

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

`QNetworkCookie` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
