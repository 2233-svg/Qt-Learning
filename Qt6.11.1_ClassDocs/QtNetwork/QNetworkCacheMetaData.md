# QNetworkCacheMetaData

> Qt 6.11.1 · Qt Network

## 1. 先建立直觉

**一句话定位：** `QNetworkCacheMetaData` 是 Qt Network 的“网络缓存Meta数据”类型，负责描述请求/地址/连接状态或承载异步网络数据。

**模块背景：** Qt Network 提供 TCP/UDP、HTTP、代理、DNS、SSL 和网络请求等异步网络能力。

### 这是什么

`QNetworkCacheMetaData` 是 异步网络机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 网络请求通常由管理器创建并调度，返回一个代表本次操作的 reply。连接建立、DNS、发送、接收和错误都是事件驱动的阶段；响应头、状态码、body 和传输错误分别表达不同层次的信息。

**适用场景：** 创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要把异步请求当同步函数；不要只检查 `error()` 而忽略 HTTP 状态码；不要在 readyRead 中假设一次就收到完整 body；不要在 GUI 线程用阻塞等待替代信号。

## 2. 依赖与对象关系

- 头文件：`#include <QNetworkCacheMetaData>`
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

### 公有类型

- `AttributesMap`
- `RawHeader`
- `RawHeaderList`

### 公有函数

- `QNetworkCacheMetaData()`
- `QNetworkCacheMetaData(const QNetworkCacheMetaData &other)`
- `~QNetworkCacheMetaData()`
- `QNetworkCacheMetaData::AttributesMap attributes() const`
- `QDateTime expirationDate() const`
- `(since 6.8) QHttpHeaders headers() const`
- `bool isValid() const`
- `QDateTime lastModified() const`
- `QNetworkCacheMetaData::RawHeaderList rawHeaders() const`
- `bool saveToDisk() const`
- `void setAttributes(const QNetworkCacheMetaData::AttributesMap &attributes)`
- `void setExpirationDate(const QDateTime &dateTime)`
- `(since 6.8) void setHeaders(const QHttpHeaders &headers)`
- `void setLastModified(const QDateTime &dateTime)`
- `void setRawHeaders(const QNetworkCacheMetaData::RawHeaderList &list)`
- `void setSaveToDisk(bool allow)`
- `void setUrl(const QUrl &url)`
- `void swap(QNetworkCacheMetaData &other)`
- `QUrl url() const`
- `bool operator!=(const QNetworkCacheMetaData &other) const`
- `QNetworkCacheMetaData & operator=(const QNetworkCacheMetaData &other)`
- `bool operator==(const QNetworkCacheMetaData &other) const`

### 相关非成员函数

- `QDataStream & operator<<(QDataStream &out, const QNetworkCacheMetaData &metaData)`
- `QDataStream & operator>>(QDataStream &in, QNetworkCacheMetaData &metaData)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QNetworkCacheMetaData::AttributesMap`

**作用与语义：**

`QHash`<`QNetworkRequest::Attribute`的同义词，`QVariant`>。

### `QNetworkCacheMetaData::RawHeader`

**作用与语义：**

STD的同义词：:p air<`QByteArray`，`QByteArray`>。

### `QNetworkCacheMetaData::RawHeaderList`

**作用与语义：**

`QList`<`RawHeader`>的同义词。

### `QNetworkCacheMetaData::QNetworkCacheMetaData()`

**作用与语义：**

构建无效的网络缓存元数据。

### `QNetworkCacheMetaData::QNetworkCacheMetaData(const QNetworkCacheMetaData &other)`

**作用与语义：**

构建`other` QNetworkCacheMetaData 的副本。

### `[noexcept] QNetworkCacheMetaData::~QNetworkCacheMetaData()`

**作用与语义：**

会销毁网络缓存的元数据。

### `QNetworkCacheMetaData::AttributesMap QNetworkCacheMetaData::attributes() const`

**作用与语义：**

返回与该缓存项目存储的所有属性。

### `QDateTime QNetworkCacheMetaData::expirationDate() const`

**作用与语义：**

返回元数据到期的日期和时间。

### `[since 6.8] QHttpHeaders QNetworkCacheMetaData::headers() const`

**作用与语义：**

返回以`QHttpHeaders`形式出现的头部，这些首部已在元数据中设置。

### `bool QNetworkCacheMetaData::isValid() const`

**作用与语义：**

如果该网络缓存元数据的属性被设置为false，则返回`true`。

### `QDateTime QNetworkCacheMetaData::lastModified() const`

**作用与语义：**

返回元数据最后修改的日期和时间。

### `QNetworkCacheMetaData::RawHeaderList QNetworkCacheMetaData::rawHeaders() const`

**作用与语义：**

返回所有在该元数据中设置的原始头部列表。列表顺序与头部设置顺序相同。

### `bool QNetworkCacheMetaData::saveToDisk() const`

**作用与语义：**

返回时，这个缓存应该允许存储在磁盘上。
一些缓存实现可以出于性能原因将这些缓存项保留在内存中，但出于安全原因，不应将它们写入磁盘。
特别是在 http 中，缓存控制设置为无存储的文档，或者任何没有设置“Cache-control： public”的 https 文档，都会将 saveToDisk 设置为 false。

### `void QNetworkCacheMetaData::setAttributes(const QNetworkCacheMetaData::AttributesMap &attributes)`

**作用与语义：**

将该缓存项目的所有属性设置为映射`attributes`。

### `void QNetworkCacheMetaData::setExpirationDate(const QDateTime &dateTime)`

**作用与语义：**

将元数据到期的日期和时间设定为`dateTime`。

### `[since 6.8] void QNetworkCacheMetaData::setHeaders(const QHttpHeaders &headers)`

**作用与语义：**

将该网络缓存元数据的头设置为`headers`。

### `void QNetworkCacheMetaData::setLastModified(const QDateTime &dateTime)`

**作用与语义：**

将元数据最后修改的时间设置为`dateTime`。

### `void QNetworkCacheMetaData::setRawHeaders(const QNetworkCacheMetaData::RawHeaderList &list)`

**作用与语义：**

将原始头设置为`list`。

### `void QNetworkCacheMetaData::setSaveToDisk(bool allow)`

**作用与语义：**

决定是否允许该网络缓存元数据及相关内容存储在磁盘上`allow`。

### `void QNetworkCacheMetaData::setUrl(const QUrl &url)`

**作用与语义：**

将该网络缓存元数据的URL设置为`url`。
密码和片段会从URL中移除。

### `[noexcept] void QNetworkCacheMetaData::swap(QNetworkCacheMetaData &other)`

**作用与语义：**

将该元数据实例与`other`交换。该操作非常快且从未失败。

### `QUrl QNetworkCacheMetaData::url() const`

**作用与语义：**

返回该网络缓存元数据所指的URL。

### `bool QNetworkCacheMetaData::operator!=(const QNetworkCacheMetaData &other) const`

**作用与语义：**

如果元数据与`other`元数据不相等，返回`true`;否则返回`false`。

### `QNetworkCacheMetaData &QNetworkCacheMetaData::operator=(const QNetworkCacheMetaData &other)`

**作用与语义：**

复制`other` `QNetworkCacheMetaData`并返回该副本的引用。

### `bool QNetworkCacheMetaData::operator==(const QNetworkCacheMetaData &other) const`

**作用与语义：**

如果元数据等于`other`元数据，返回`true`;否则返回`false`。

### `QDataStream &operator<<(QDataStream &out, const QNetworkCacheMetaData &metaData)`

**作用与语义：**

写入`metaData` `out`流。

### `QDataStream &operator>>(QDataStream &in, QNetworkCacheMetaData &metaData)`

**作用与语义：**

读取溪流`in`到`metaData`的`QNetworkCacheMetaData`。

### `AttributesMap`

**作用与语义：**

`QHash`<`QNetworkRequest::Attribute`的同义词，`QVariant`>。

### `RawHeader`

**作用与语义：**

STD的同义词：:p air<`QByteArray`，`QByteArray`>。

### `RawHeaderList`

**作用与语义：**

`QList`<`RawHeader`>的同义词。

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

`QNetworkCacheMetaData` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
