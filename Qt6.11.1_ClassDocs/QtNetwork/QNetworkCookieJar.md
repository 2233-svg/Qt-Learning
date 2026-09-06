# QNetworkCookieJar

> Qt 6.11.1 · Qt Network

## 1. 先建立直觉

**一句话定位：** `QNetworkCookieJar` 是 Qt Network 的“网络CookieJar”类型，负责描述请求/地址/连接状态或承载异步网络数据。

**模块背景：** Qt Network 提供 TCP/UDP、HTTP、代理、DNS、SSL 和网络请求等异步网络能力。

### 这是什么

`QNetworkCookieJar` 是 异步网络机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 网络请求通常由管理器创建并调度，返回一个代表本次操作的 reply。连接建立、DNS、发送、接收和错误都是事件驱动的阶段；响应头、状态码、body 和传输错误分别表达不同层次的信息。

**适用场景：** 创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要把异步请求当同步函数；不要只检查 `error()` 而忽略 HTTP 状态码；不要在 readyRead 中假设一次就收到完整 body；不要在 GUI 线程用阻塞等待替代信号。

## 2. 依赖与对象关系

- 头文件：`#include <QNetworkCookieJar>`
- 继承自：QObject
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

- `QNetworkCookieJar(QObject *parent = nullptr)`
- `virtual ~QNetworkCookieJar()`
- `virtual QList<QNetworkCookie> cookiesForUrl(const QUrl &url) const`
- `virtual bool deleteCookie(const QNetworkCookie &cookie)`
- `virtual bool insertCookie(const QNetworkCookie &cookie)`
- `virtual bool setCookiesFromUrl(const QList<QNetworkCookie> &cookieList, const QUrl &url)`
- `virtual bool updateCookie(const QNetworkCookie &cookie)`

### 保护函数

- `QList<QNetworkCookie> allCookies() const`
- `void setAllCookies(const QList<QNetworkCookie> &cookieList)`
- `virtual bool validateCookie(const QNetworkCookie &cookie, const QUrl &url) const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[explicit] QNetworkCookieJar::QNetworkCookieJar(QObject *parent = nullptr)`

**作用与语义：**

创建一个 QNetworkCookieJar 对象，并将父对象设置为`parent`。
饼干罐初始化为空。

### `[virtual noexcept] QNetworkCookieJar::~QNetworkCookieJar()`

**作用与语义：**

销毁该 cookie jar 对象，丢弃所有存储在其中的 cookie。`QNetworkCookieJar` 默认实现中 Cookie 不会保存到磁盘。
如果你需要把 Cookie 保存到磁盘，你必须自己从 `QNetworkCookieJar` 导出并保存到 Cookie 到磁盘。

### `[protected] QList<QNetworkCookie> QNetworkCookieJar::allCookies() const`

**作用与语义：**

返回存储在本 cookie jar 中的所有 Cookie。该函数适用于派生类，用于将 Cookie 保存到磁盘，以及实现 Cookie 到期和其他策略。

### `[virtual] QList<QNetworkCookie> QNetworkCookieJar::cookiesForUrl(const QUrl &url) const`

**作用与语义：**

发送请求到`url`时返回需要添加的Cookie。该函数由默认`QNetworkAccessManager::createRequest()`调用，该函数返回的Cookie会添加到发送请求中。
如果发现多个同名但路径不同的cookie，路径较长的返回先返回路径较短的cookie。换句话说，该函数返回的是按路径长度递减排序的cookie。
默认的`QNetworkCookieJar`类只实现一个非常基础的安全策略（确保 cookie 的域名和路径与回复的匹配）。要用自己的算法增强安全策略，可以覆盖 cookiesForUrl()。

### `[virtual] bool QNetworkCookieJar::deleteCookie(const QNetworkCookie &cookie)`

**作用与语义：**

从 Cookie jar 删除的 Cookie 发现与`cookie`具有相同标识符。
如果 cookie 被删除，返回`true`，否则返回 false。

### `[virtual] bool QNetworkCookieJar::insertCookie(const QNetworkCookie &cookie)`

**作用与语义：**

这给这个饼干罐里加了不少东西`cookie`。
如果添加了`cookie`，返回`true`，否则为假。
如果 cookie jar 中已有具有相同标识符的 cookie，则该标识符将被覆盖。

### `[protected] void QNetworkCookieJar::setAllCookies(const QList<QNetworkCookie> &cookieList)`

**作用与语义：**

将该 cookie jar 所持有的 Cookie 内部列表设置为`cookieList`。该函数适用于派生类实现从永久存储加载 Cookie，或通过重新实现 `setCookiesFromUrl()` 来实现自身的 Cookie 接受策略。

### `[virtual] bool QNetworkCookieJar::setCookiesFromUrl(const QList<QNetworkCookie> &cookieList, const QUrl &url)`

**作用与语义：**

将列表中的cookies `cookieList`添加到这个cookiejar中。插入前，cookies会被规范化。
如果设置了一个或多个 cookie 作为 `url`，返回 `true`，否则为假。
如果饼干罐中已有饼干，`cookieList`中的饼干将被覆盖。
默认的`QNetworkCookieJar`类只实现一个非常基础的安全策略（确保 cookie 的域名和路径与回复一致）。要用自己的算法增强安全策略，可以覆盖 setCookiesFromUrl()。
此外，`QNetworkCookieJar`没有最大cookie罐大小。重新实现此功能，丢弃旧cookie，为新cookie腾出空间。

### `[virtual] bool QNetworkCookieJar::updateCookie(const QNetworkCookie &cookie)`

**作用与语义：**

如果 cookie jar 中存在与 `cookie` 相同的标识符的 cookie，它会被更新。该函数使用 `insertCookie()`。
如果`cookie`已更新，返回`true`;如果jar中没有符合`cookie`标识符的cookie，则返回false。

### `[virtual protected] bool QNetworkCookieJar::validateCookie(const QNetworkCookie &cookie, const QUrl &url) const`

**作用与语义：**

如果域和路径有效，返回`true`，否则返回`cookie`，否则为假。`url`参数用于判断Cookie中指定的域是否被允许。

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

`QNetworkCookieJar` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
