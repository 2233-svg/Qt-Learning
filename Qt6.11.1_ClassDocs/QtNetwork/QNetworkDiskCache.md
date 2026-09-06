# QNetworkDiskCache

> Qt 6.11.1 · Qt Network

## 1. 先建立直觉

**一句话定位：** `QNetworkDiskCache` 是 Qt Network 的“网络Disk缓存”类型，负责描述请求/地址/连接状态或承载异步网络数据。

**模块背景：** Qt Network 提供 TCP/UDP、HTTP、代理、DNS、SSL 和网络请求等异步网络能力。

### 这是什么

`QNetworkDiskCache` 是 异步网络机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 网络请求通常由管理器创建并调度，返回一个代表本次操作的 reply。连接建立、DNS、发送、接收和错误都是事件驱动的阶段；响应头、状态码、body 和传输错误分别表达不同层次的信息。

**适用场景：** 创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要把异步请求当同步函数；不要只检查 `error()` 而忽略 HTTP 状态码；不要在 readyRead 中假设一次就收到完整 body；不要在 GUI 线程用阻塞等待替代信号。

## 2. 依赖与对象关系

- 头文件：`#include <QNetworkDiskCache>`
- 继承自：QAbstractNetworkCache
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

- `QNetworkDiskCache(QObject *parent = nullptr)`
- `virtual ~QNetworkDiskCache()`
- `QString cacheDirectory() const`
- `QNetworkCacheMetaData fileMetaData(const QString &fileName) const`
- `qint64 maximumCacheSize() const`
- `void setCacheDirectory(const QString &cacheDir)`
- `void setMaximumCacheSize(qint64 size)`

### 重实现的公有函数

- `virtual qint64 cacheSize() const override`
- `virtual QIODevice * data(const QUrl &url) override`
- `virtual void insert(QIODevice *device) override`
- `virtual QNetworkCacheMetaData metaData(const QUrl &url) override`
- `virtual QIODevice * prepare(const QNetworkCacheMetaData &metaData) override`
- `virtual bool remove(const QUrl &url) override`
- `virtual void updateMetaData(const QNetworkCacheMetaData &metaData) override`

### 公有槽函数

- `virtual void clear() override`

### 保护函数

- `virtual qint64 expire()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[explicit] QNetworkDiskCache::QNetworkDiskCache(QObject *parent = nullptr)`

**作用与语义：**

创建新的磁盘缓存。`parent`参数传递给`QAbstractNetworkCache`的构造函数。

### `[virtual noexcept] QNetworkDiskCache::~QNetworkDiskCache()`

**作用与语义：**

销毁缓存对象。这不会清除磁盘缓存。

### `QString QNetworkDiskCache::cacheDirectory() const`

**作用与语义：**

返回缓存文件将存储的位置。

### `[override virtual] qint64 QNetworkDiskCache::cacheSize() const`

**作用与语义：**

重装：`QAbstractNetworkCache::cacheSize()` const.
返回缓存当前占用的大小。根据缓存实现，可能是磁盘大小或内存大小。
在基类中，这是一个纯虚拟函数。

### `[override virtual slot] void QNetworkDiskCache::clear()`

**作用与语义：**

重装：`QAbstractNetworkCache::clear()`。
移除缓存中的所有项目。除非清除缓存失败，否则调用清除后`cacheSize()`应该返回0。
在基类中，这是一个纯虚拟函数。

### `[override virtual] QIODevice *QNetworkDiskCache::data(const QUrl &url)`

**作用与语义：**

Reimpations： `QAbstractNetworkCache::data`（const QUrl & url）。
返回与`url`相关的数据。
请求数据的应用程序在完成`QIODevice`后是否删除。
如果没有缓存，`url` URL 无效;如果内存内部缓存错误，则返回`nullptr`。
在基类中，这是一个纯虚拟函数。

### `[virtual protected] qint64 QNetworkDiskCache::expire()`

**作用与语义：**

清理缓存使其大小低于最大缓存大小。返回当前缓存大小。
当当前缓存大小大于当前缓存大小`maximumCacheSize()`旧缓存文件会被移除，直到总大小低于`maximumCacheSize()`的90%从最早的缓存开始，利用文件创建日期确定缓存文件的年代。
子类可以重新实现该函数，改变缓存文件移除的顺序，考虑应用程序中已知的信息而`QNetworkDiskCache`不知道，例如缓存被访问的次数。
注意：如果当前缓存大小未知，`cacheSize()`调用将失效。

### `QNetworkCacheMetaData QNetworkDiskCache::fileMetaData(const QString &fileName) const`

**作用与语义：**

返回缓存文件`fileName`的`QNetworkCacheMetaData`。
如果`fileName`不是缓存文件，`QNetworkCacheMetaData`将无效。

### `[override virtual] void QNetworkDiskCache::insert(QIODevice *device)`

**作用与语义：**

重实现自：`QAbstractNetworkCache::insert`（QIODevice *设备）。
将数据插入`device`，并将准备好的元数据插入缓存。调用该函数后，数据和元数据应可用`data()`和`metaData()`检索。
取消预设的插入调用，`remove()`元数据的 URL 上。
在基类中，这是一个纯虚拟函数。

### `qint64 QNetworkDiskCache::maximumCacheSize() const`

**作用与语义：**

返回当前磁盘缓存的最大容量。

### `[override virtual] QNetworkCacheMetaData QNetworkDiskCache::metaData(const QUrl &url)`

**作用与语义：**

重实现自：`QAbstractNetworkCache::metaData`（const QUrl & url）。
返回该网址`url`的元数据。
如果 URL 有效且缓存包含 URL 数据，则返回有效 `QNetworkCacheMetaData`。
在基类中，这是一个纯虚拟函数。

### `[override virtual] QIODevice *QNetworkDiskCache::prepare(const QNetworkCacheMetaData &metaData)`

**作用与语义：**

重实现自：`QAbstractNetworkCache::prepare`（const QNetworkCacheMetaData &metaData）。
返回应填充缓存项目数据的设备`metaData`。当所有数据写入后，应调用`insert()`。如果`metaData`无效或元数据中的URL无效，则返回`nullptr`。
缓存拥有设备，并在插入或移除时负责删除。
取消预先插入的调用，`remove()`元数据的 URL 上。
在基类中，这是一个纯虚拟函数。

### `[override virtual] bool QNetworkDiskCache::remove(const QUrl &url)`

**作用与语义：**

重实现自：`QAbstractNetworkCache::remove`（const QUrl & url）。
移除`url`的缓存条目，如果成功则返回true，否则为false。
在基类中，这是一个纯虚拟函数。

### `void QNetworkDiskCache::setCacheDirectory(const QString &cacheDir)`

**作用与语义：**

设置缓存文件存储的目录`cacheDir`。
如果这个目录不存在，`QNetworkDiskCache`会创建它。
准备好的缓存项目在插入时会存储在新的缓存目录中。

### `void QNetworkDiskCache::setMaximumCacheSize(qint64 size)`

**作用与语义：**

将磁盘缓存的最大容量设置为`size`。
如果新缓存大小小于当前缓存大小，缓存就会调用`expire()`。

### `[override virtual] void QNetworkDiskCache::updateMetaData(const QNetworkCacheMetaData &metaData)`

**作用与语义：**

重实现自：`QAbstractNetworkCache::updateMetaData`（const QNetworkCacheMetaData &metaData）。
更新`metaData` 网址的缓存元日期`metaData`。
如果缓存中没有该URL的缓存项，则不会采取任何操作。
在基类中，这是一个纯虚拟函数。

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

`QNetworkDiskCache` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
