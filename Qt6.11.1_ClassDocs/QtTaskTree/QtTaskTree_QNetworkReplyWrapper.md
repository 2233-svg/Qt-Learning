# QtTaskTree::QNetworkReplyWrapper

> Qt 6.11.1 · Qt TaskTree

## 1. 先建立直觉

**一句话定位：** `QtTaskTree::QNetworkReplyWrapper` 是 Qt Network 的“网络响应Wrapper”类型，负责描述请求/地址/连接状态或承载异步网络数据。

**模块背景：** 这是 Qt TaskTree 模块中的公开 C++ API，具体职责以类摘要和继承关系为准。

### 这是什么

`QtTaskTree::QNetworkReplyWrapper` 是 异步网络机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 网络请求通常由管理器创建并调度，返回一个代表本次操作的 reply。连接建立、DNS、发送、接收和错误都是事件驱动的阶段；响应头、状态码、body 和传输错误分别表达不同层次的信息。

**适用场景：** 创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要把异步请求当同步函数；不要只检查 `error()` 而忽略 HTTP 状态码；不要在 readyRead 中假设一次就收到完整 body；不要在 GUI 线程用阻塞等待替代信号。

## 2. 依赖与对象关系

- 头文件：`#include <qnetworkwrappertask.h>`
- 继承自：QObject
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS TaskTree)
target_link_libraries(mytarget PRIVATE Qt6::TaskTree)
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

- `QNetworkReplyWrapper(QObject *parent)`
- `virtual ~QNetworkReplyWrapper() override`
- `QNetworkReply * reply() const`
- `void setData(const QByteArray &data)`
- `void setNetworkAccessManager(QNetworkAccessManager *manager)`
- `void setOperation(QNetworkAccessManager::Operation operation)`
- `void setRequest(const QNetworkRequest &request)`
- `void setVerb(const QByteArray &verb)`
- `void start()`

### 信号

- `void done(QtTaskTree::DoneResult result)`
- `void downloadProgress(qint64 bytesReceived, qint64 bytesTotal)`
- `void sslErrors(const QList<QSslError> &errors)`
- `void started()`

### 重实现的保护函数

- `virtual bool event(QEvent *event) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[explicit] QNetworkReplyWrapper::QNetworkReplyWrapper(QObject *parent)`

**作用与语义：**

创建带有指定`parent`的QNetworkReplyWrapper。

### `[override virtual noexcept] QNetworkReplyWrapper::~QNetworkReplyWrapper()`

**作用与语义：**

会破坏`QNetworkReplyWrapper`。如果已加速的`reply()`仍在运行，则中止。

### `[signal] void QNetworkReplyWrapper::done(QtTaskTree::DoneResult result)`

**作用与语义：**

该信号是在相关`QNetworkReply`结束后发出的。传递`result`表示是否成功或错误。

### `[signal] void QNetworkReplyWrapper::downloadProgress(qint64 bytesReceived, qint64 bytesTotal)`

**作用与语义：**

该信号从运行`QNetworkReply`重新发射，穿过`bytesReceived`和`bytesTotal`。

### `[override virtual protected] bool QNetworkReplyWrapper::event(QEvent *event)`

**作用与语义：**

重实现自：`QObject::event`（QEvent *e）。

### `QNetworkReply *QNetworkReplyWrapper::reply() const`

**作用与语义：**

返回已加复`QNetworkReply`的指针。`QNetworkReplyWrapper`开始前和结束后，该函数返回 nullptr。在`started()`信号发出后，直到信号发出`done()`，访问`QNetworkReply`是安全的。

### `void QNetworkReplyWrapper::setData(const QByteArray &data)`

**作用与语义：**

把`data`设置为`start()`。只在`QNetworkAccessManager::PutOperation`、`QNetworkAccessManager::PostOperation`或`QNetworkAccessManager::CustomOperation`时使用。

### `void QNetworkReplyWrapper::setNetworkAccessManager(QNetworkAccessManager *manager)`

**作用与语义：**

把`manager`设置为`start()`上使用。

### `void QNetworkReplyWrapper::setOperation(QNetworkAccessManager::Operation operation)`

**作用与语义：**

把`operation`设置为`start()`使用。

### `void QNetworkReplyWrapper::setRequest(const QNetworkRequest &request)`

**作用与语义：**

把`request`设置为`start()`使用。

### `void QNetworkReplyWrapper::setVerb(const QByteArray &verb)`

**作用与语义：**

把`verb`设置为用在`start()`上。只在`QNetworkAccessManager::CustomOperation`情况下使用。

### `[signal] void QNetworkReplyWrapper::sslErrors(const QList<QSslError> &errors)`

**作用与语义：**

该信号从运行`QNetworkReply`重新发射，传递一串SSL的列表`errors`。

### `void QNetworkReplyWrapper::start()`

**作用与语义：**

`QNetworkReplyWrapper`开始了。

### `[signal] void QNetworkReplyWrapper::started()`

**作用与语义：**

该信号是在管理`QNetworkReply`成功启动后发出的。

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

`QtTaskTree::QNetworkReplyWrapper` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
