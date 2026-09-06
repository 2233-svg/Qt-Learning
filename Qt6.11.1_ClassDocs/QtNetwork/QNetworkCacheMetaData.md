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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 30 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `QNetworkCacheMetaData::AttributesMap`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QNetworkCacheMetaData` 的配置属性。初始化或状态切换时通过 `setAttributesMap(...)` 设置，之后用 `AttributesMap()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:AttributesMap`。
- 属性名：`QNetworkCacheMetaData`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QNetworkCacheMetaData::RawHeader`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QNetworkCacheMetaData` 的配置属性。初始化或状态切换时通过 `setRawHeader(...)` 设置，之后用 `RawHeader()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:RawHeader`。
- 属性名：`QNetworkCacheMetaData`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QNetworkCacheMetaData::RawHeaderList`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QNetworkCacheMetaData` 的配置属性。初始化或状态切换时通过 `setRawHeaderList(...)` 设置，之后用 `RawHeaderList()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:RawHeaderList`。
- 属性名：`QNetworkCacheMetaData`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QNetworkCacheMetaData::QNetworkCacheMetaData()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkCacheMetaData` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QNetworkCacheMetaData::QNetworkCacheMetaData(const QNetworkCacheMetaData &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkCacheMetaData` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `const QNetworkCacheMetaData &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QNetworkCacheMetaData::~QNetworkCacheMetaData()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkCacheMetaData` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QNetworkCacheMetaData::AttributesMap QNetworkCacheMetaData::attributes() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkCacheMetaData::attributes` 用于计算、查询或取得与“attributes”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QNetworkCacheMetaData::AttributesMap`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QNetworkCacheMetaData::AttributesMap`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDateTime QNetworkCacheMetaData::expirationDate() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkCacheMetaData::expirationDate` 用于计算、查询或取得与“expiration、日期”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDateTime`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.8] QHttpHeaders QNetworkCacheMetaData::headers() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkCacheMetaData::headers` 用于计算、查询或取得与“headers”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QHttpHeaders`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QHttpHeaders`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QNetworkCacheMetaData::isValid() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isValid`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDateTime QNetworkCacheMetaData::lastModified() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkCacheMetaData::lastModified` 用于计算、查询或取得与“末项、Modified”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDateTime`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QNetworkCacheMetaData::RawHeaderList QNetworkCacheMetaData::rawHeaders() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkCacheMetaData::rawHeaders` 用于计算、查询或取得与“raw、Headers”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QNetworkCacheMetaData::RawHeaderList`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QNetworkCacheMetaData::RawHeaderList`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QNetworkCacheMetaData::saveToDisk() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkCacheMetaData::saveToDisk` 用于计算、查询或取得与“保存、转换输出、Disk”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkCacheMetaData::setAttributes(const QNetworkCacheMetaData::AttributesMap &attributes)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setAttributes`。调用它会改变 `QNetworkCacheMetaData` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `attributes`：类型为 `const QNetworkCacheMetaData::AttributesMap &`。没有默认值，调用时必须提供。传入 `const QNetworkCacheMetaData::AttributesMap &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkCacheMetaData::setExpirationDate(const QDateTime &dateTime)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setExpirationDate`。调用它会改变 `QNetworkCacheMetaData` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `dateTime`：类型为 `const QDateTime &`。没有默认值，调用时必须提供。传入 `const QDateTime &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.8] void QNetworkCacheMetaData::setHeaders(const QHttpHeaders &headers)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setHeaders`。调用它会改变 `QNetworkCacheMetaData` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `headers`：类型为 `const QHttpHeaders &`。没有默认值，调用时必须提供。传入 `const QHttpHeaders &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkCacheMetaData::setLastModified(const QDateTime &dateTime)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setLastModified`。调用它会改变 `QNetworkCacheMetaData` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `dateTime`：类型为 `const QDateTime &`。没有默认值，调用时必须提供。传入 `const QDateTime &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkCacheMetaData::setRawHeaders(const QNetworkCacheMetaData::RawHeaderList &list)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setRawHeaders`。调用它会改变 `QNetworkCacheMetaData` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `list`：类型为 `const QNetworkCacheMetaData::RawHeaderList &`。没有默认值，调用时必须提供。传入 `const QNetworkCacheMetaData::RawHeaderList &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkCacheMetaData::setSaveToDisk(bool allow)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSaveToDisk`。调用它会改变 `QNetworkCacheMetaData` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `allow`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkCacheMetaData::setUrl(const QUrl &url)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setUrl`。调用它会改变 `QNetworkCacheMetaData` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `url`：类型为 `const QUrl &`。没有默认值，调用时必须提供。资源地址。要确认 scheme、编码、相对路径、重定向和是否包含敏感信息。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] void QNetworkCacheMetaData::swap(QNetworkCacheMetaData &other)`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkCacheMetaData::swap` 用于执行与“swap”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `other`：类型为 `QNetworkCacheMetaData &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QUrl QNetworkCacheMetaData::url() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkCacheMetaData::url` 用于计算、查询或取得与“url”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QUrl`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QUrl`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QNetworkCacheMetaData::operator!=(const QNetworkCacheMetaData &other) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkCacheMetaData` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `other`：类型为 `const QNetworkCacheMetaData &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QNetworkCacheMetaData &QNetworkCacheMetaData::operator=(const QNetworkCacheMetaData &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkCacheMetaData` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QNetworkCacheMetaData &`。
- 参数 `other`：类型为 `const QNetworkCacheMetaData &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QNetworkCacheMetaData::operator==(const QNetworkCacheMetaData &other) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkCacheMetaData` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `other`：类型为 `const QNetworkCacheMetaData &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDataStream &operator<<(QDataStream &out, const QNetworkCacheMetaData &metaData)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QNetworkCacheMetaData` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDataStream &`。
- 参数 `out`：类型为 `QDataStream &`。没有默认值，调用时必须提供。传入 `QDataStream &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `metaData`：类型为 `const QNetworkCacheMetaData &`。没有默认值，调用时必须提供。传入 `const QNetworkCacheMetaData &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDataStream &operator>>(QDataStream &in, QNetworkCacheMetaData &metaData)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QNetworkCacheMetaData` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDataStream &`。
- 参数 `in`：类型为 `QDataStream &`。没有默认值，调用时必须提供。传入 `QDataStream &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `metaData`：类型为 `QNetworkCacheMetaData &`。没有默认值，调用时必须提供。传入 `QNetworkCacheMetaData &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `AttributesMap`

**API 类别：** 公有类型

**中文解读：** 这是 `QNetworkCacheMetaData` 的 `Attributes、映射` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `RawHeader`

**API 类别：** 公有类型

**中文解读：** 这是 `QNetworkCacheMetaData` 的 `Raw、Header` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `RawHeaderList`

**API 类别：** 公有类型

**中文解读：** 这是 `QNetworkCacheMetaData` 的 `Raw、Header、List` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

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

`QNetworkCacheMetaData` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
