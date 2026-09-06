# QNetworkProxyFactory

> Qt 6.11.1 · Qt Network

## 1. 先建立直觉

**一句话定位：** `QNetworkProxyFactory` 是 Qt Network 的“网络代理工厂”类型，负责描述请求/地址/连接状态或承载异步网络数据。

**模块背景：** Qt Network 提供 TCP/UDP、HTTP、代理、DNS、SSL 和网络请求等异步网络能力。

### 这是什么

`QNetworkProxyFactory` 是 异步网络机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 网络请求通常由管理器创建并调度，返回一个代表本次操作的 reply。连接建立、DNS、发送、接收和错误都是事件驱动的阶段；响应头、状态码、body 和传输错误分别表达不同层次的信息。

**适用场景：** 创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要把异步请求当同步函数；不要只检查 `error()` 而忽略 HTTP 状态码；不要在 readyRead 中假设一次就收到完整 body；不要在 GUI 线程用阻塞等待替代信号。

## 2. 依赖与对象关系

- 头文件：`#include <QNetworkProxyFactory>`
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

- `QNetworkProxyFactory()`
- `virtual ~QNetworkProxyFactory()`
- `virtual QList<QNetworkProxy> queryProxy(const QNetworkProxyQuery &query = QNetworkProxyQuery()) = 0`

### 静态公有成员

- `QList<QNetworkProxy> proxyForQuery(const QNetworkProxyQuery &query)`
- `void setApplicationProxyFactory(QNetworkProxyFactory *factory)`
- `void setUseSystemConfiguration(bool enable)`
- `QList<QNetworkProxy> systemProxyForQuery(const QNetworkProxyQuery &query = QNetworkProxyQuery())`
- `bool usesSystemConfiguration()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QNetworkProxyFactory::QNetworkProxyFactory()`

**作用与语义：**

创建一个 QNetworkProxyFactory 对象。
由于QNetworkProxyFactory是一个抽象类，你不能直接创建类型为QNetworkProxyFactory的对象。

### `[virtual noexcept] QNetworkProxyFactory::~QNetworkProxyFactory()`

**作用与语义：**

摧毁`QNetworkProxyFactory`物体。

### `[static] QList<QNetworkProxy> QNetworkProxyFactory::proxyForQuery(const QNetworkProxyQuery &query)`

**作用与语义：**

该函数接收查询请求`query`，检查套接字或请求类型的详细信息，并返回一份`QNetworkProxy`对象列表，指示将使用的代理服务器，按偏好顺序排列。

### `[pure virtual] QList<QNetworkProxy> QNetworkProxyFactory::queryProxy(const QNetworkProxyQuery &query = QNetworkProxyQuery())`

**作用与语义：**

该函数接收查询请求 `query`，检查套接字或请求类型的详细信息，并返回一个`QNetworkProxy`对象列表，指示所使用的代理服务器，按偏好顺序排列。
在重新实现该类时，请确保至少返回一个元素。
如果你无法确定更好的代理替代方案，可以使用 `QNetworkProxy::DefaultProxy`，它会告诉查询代理的代码使用更高级别的替代方案。例如，如果该工厂设置为`QNetworkAccessManager`对象，DefaultProxy 会告诉它查询应用级代理设置。
如果该出厂设置为应用代理工厂，DefaultProxy 和 NoProxy 的含义相同。

### `[static] void QNetworkProxyFactory::setApplicationProxyFactory(QNetworkProxyFactory *factory)`

**作用与语义：**

将应用范围的代理工厂设置为`factory`。该函数会获得该对象的所有权，并在必要时删除它。
当所有其他代理选择请求返回`QNetworkProxy::DefaultProxy`时，应用范围代理作为最后手段使用。例如，`QTcpSocket`对象可以设置带有QTcpSocket：：setProxy的代理，但如果没有设置，则查询带有该函数的代理工厂类集合。
如果你用这个函数设置代理工厂，任何带有`QNetworkProxy::setApplicationProxy`的应用级代理都会被覆盖，`usesSystemConfiguration()`会返回`false`。

### `[static] void QNetworkProxyFactory::setUseSystemConfiguration(bool enable)`

**作用与语义：**

仅允许使用平台特定的代理设置。更多信息请参见 `systemProxyForQuery()`。
调用该函数时`enable`设置为`true`会重置已设置的任何代理或`QNetworkProxyFactory`。
注意：有关系统代理使用限制的列表，请参见 `systemProxyForQuery()` 文档。

### `[static] QList<QNetworkProxy> QNetworkProxyFactory::systemProxyForQuery(const QNetworkProxyQuery &query = QNetworkProxyQuery())`

**作用与语义：**

该函数接收查询请求`query`，检查套接字或请求类型的详细信息，并返回一份`QNetworkProxy`对象列表，指示将使用代理服务器，按偏好顺序排列。
该函数可用于确定平台特定的代理设置。该函数将利用操作系统提供的库来确定某连接的代理（如果存在此类库）。如果没有，该函数仅返回类型为`QNetworkProxy::NoProxy`的 `QNetworkProxy`。
在 Windows 上，该函数将使用 WinHTTP DLL 函数。尽管名称如此，Microsoft 建议对所有需要网络连接的应用程序使用，而不仅仅是 HTTP。这将尊重注册表中 proxycfg.exe 工具设置的代理设置。如果找不到这些设置，该功能将尝试获取 Internet Explorer 的设置并使用它们。
在macOS上，该功能会通过苹果的CFNetwork框架获取代理设置。它会分别应用包含“ftp”、“http”和“https”协议标签的查询的FTP、HTTP和HTTPS代理配置。如果该配置启用了SOCKS代理，该函数将使用SOCKS服务器处理所有查询。如果未启用SOCKS，则所有TcpSocket和UrlRequest查询都会使用HTTPS代理。
在配置了支持libproxy的系统上，这个功能依赖libproxy获取代理设置。根据libproxy配置，这又可以委托给桌面设置、环境变量等。
在其他系统中，该函数会从“http_proxy”环境变量中获取代理设置。该变量必须是使用以下方案之一的URL：“http”、“socks5”或“socks5h”之一。
以下是当前版本该功能的限制。未来的Qt版本可能会解除这里列出的一些限制。
- 在 Windows 平台上，根据用户系统配置，该功能执行可能需要几秒钟。

### `[static] bool QNetworkProxyFactory::usesSystemConfiguration()`

**作用与语义：**

返回是否启用了平台特定的代理设置。

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

`QNetworkProxyFactory` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
