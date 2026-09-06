# QRestAccessManager

> Qt 6.11.1 · Qt Network

## 1. 先建立直觉

**一句话定位：** `QRestAccessManager` 是 Qt Network 的“Rest访问管理器”类型，负责描述请求/地址/连接状态或承载异步网络数据。

**模块背景：** Qt Network 提供 TCP/UDP、HTTP、代理、DNS、SSL 和网络请求等异步网络能力。

### 这是什么

`QRestAccessManager` 是 异步网络机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 网络请求通常由管理器创建并调度，返回一个代表本次操作的 reply。连接建立、DNS、发送、接收和错误都是事件驱动的阶段；响应头、状态码、body 和传输错误分别表达不同层次的信息。

**适用场景：** 创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要把异步请求当同步函数；不要只检查 `error()` 而忽略 HTTP 状态码；不要在 readyRead 中假设一次就收到完整 body；不要在 GUI 线程用阻塞等待替代信号。

## 2. 依赖与对象关系

- 头文件：`#include <QRestAccessManager>`
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
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QRestAccessManager(QNetworkAccessManager *manager, QObject *parent = nullptr)`
- `virtual ~QRestAccessManager() override`
- `QNetworkReply * deleteResource(const QNetworkRequest &request, const QRestAccessManager::ContextTypeForFunctor<Functor> *context, Functor &&callback)`
- `QNetworkReply * get(const QNetworkRequest &request, const QRestAccessManager::ContextTypeForFunctor<Functor> *context, Functor &&callback)`
- `QNetworkReply * get(const QNetworkRequest &request, const QByteArray &data, const QRestAccessManager::ContextTypeForFunctor<Functor> *context, Functor &&callback)`
- `QNetworkReply * get(const QNetworkRequest &request, QIODevice *data, const QRestAccessManager::ContextTypeForFunctor<Functor> *context, Functor &&callback)`
- `QNetworkReply * get(const QNetworkRequest &request, const QJsonDocument &data, const QRestAccessManager::ContextTypeForFunctor<Functor> *context, Functor &&callback)`
- `QNetworkReply * head(const QNetworkRequest &request, const QRestAccessManager::ContextTypeForFunctor<Functor> *context, Functor &&callback)`
- `QNetworkAccessManager * networkAccessManager() const`
- `QNetworkReply * patch(const QNetworkRequest &request, const QJsonDocument &data, const QRestAccessManager::ContextTypeForFunctor<Functor> *context, Functor &&callback)`
- `QNetworkReply * patch(const QNetworkRequest &request, QIODevice *data, const QRestAccessManager::ContextTypeForFunctor<Functor> *context, Functor &&callback)`
- `QNetworkReply * patch(const QNetworkRequest &request, const QByteArray &data, const QRestAccessManager::ContextTypeForFunctor<Functor> *context, Functor &&callback)`
- `QNetworkReply * patch(const QNetworkRequest &request, const QVariantMap &data, const QRestAccessManager::ContextTypeForFunctor<Functor> *context, Functor &&callback)`
- `QNetworkReply * post(const QNetworkRequest &request, const QJsonDocument &data, const QRestAccessManager::ContextTypeForFunctor<Functor> *context, Functor &&callback)`
- `QNetworkReply * post(const QNetworkRequest &request, QHttpMultiPart *data, const QRestAccessManager::ContextTypeForFunctor<Functor> *context, Functor &&callback)`
- `QNetworkReply * post(const QNetworkRequest &request, QIODevice *data, const QRestAccessManager::ContextTypeForFunctor<Functor> *context, Functor &&callback)`
- `QNetworkReply * post(const QNetworkRequest &request, const QByteArray &data, const QRestAccessManager::ContextTypeForFunctor<Functor> *context, Functor &&callback)`
- `QNetworkReply * post(const QNetworkRequest &request, const QVariantMap &data, const QRestAccessManager::ContextTypeForFunctor<Functor> *context, Functor &&callback)`
- `QNetworkReply * put(const QNetworkRequest &request, const QJsonDocument &data, const QRestAccessManager::ContextTypeForFunctor<Functor> *context, Functor &&callback)`
- `QNetworkReply * put(const QNetworkRequest &request, QHttpMultiPart *data, const QRestAccessManager::ContextTypeForFunctor<Functor> *context, Functor &&callback)`
- `QNetworkReply * put(const QNetworkRequest &request, QIODevice *data, const QRestAccessManager::ContextTypeForFunctor<Functor> *context, Functor &&callback)`
- `QNetworkReply * put(const QNetworkRequest &request, const QByteArray &data, const QRestAccessManager::ContextTypeForFunctor<Functor> *context, Functor &&callback)`
- `QNetworkReply * put(const QNetworkRequest &request, const QVariantMap &data, const QRestAccessManager::ContextTypeForFunctor<Functor> *context, Functor &&callback)`
- `QNetworkReply * sendCustomRequest(const QNetworkRequest &request, const QByteArray &method, const QByteArray &data, const QRestAccessManager::ContextTypeForFunctor<Functor> *context, Functor &&callback)`
- `QNetworkReply * sendCustomRequest(const QNetworkRequest &request, const QByteArray &method, QHttpMultiPart *data, const QRestAccessManager::ContextTypeForFunctor<Functor> *context, Functor &&callback)`
- `QNetworkReply * sendCustomRequest(const QNetworkRequest &request, const QByteArray &method, QIODevice *data, const QRestAccessManager::ContextTypeForFunctor<Functor> *context, Functor &&callback)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 26 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `[explicit] QRestAccessManager::QRestAccessManager(QNetworkAccessManager *manager, QObject *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QRestAccessManager` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `manager`：类型为 `QNetworkAccessManager *`。没有默认值，调用时必须提供。传入 `QNetworkAccessManager *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `parent`：类型为 `QObject *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual noexcept] QRestAccessManager::~QRestAccessManager()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QRestAccessManager` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *QRestAccessManager::deleteResource(const QNetworkRequest &request, const QRestAccessManager::ContextTypeForFunctor<Functor> *context, Functor &&callback)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `deleteResource`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *`。
- 参数 `request`：类型为 `const QNetworkRequest &`。没有默认值，调用时必须提供。请求描述对象，通常包含 URL、请求头和传输选项；它不等于响应或实际连接。
- 参数 `context`：类型为 `const QRestAccessManager::ContextTypeForFunctor<Functor> *`。没有默认值，调用时必须提供。上下文对象，用于限定回调连接的生命周期或解析/执行环境。
- 参数 `callback`：类型为 `Functor &&`。没有默认值，调用时必须提供。回调或函数对象。要确认可调用签名、捕获对象生命周期和执行线程，不要在回调中做长时间阻塞工作。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *QRestAccessManager::get(const QNetworkRequest &request, const QRestAccessManager::ContextTypeForFunctor<Functor> *context, Functor &&callback)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QRestAccessManager` 的核心操作 `get`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *`。
- 参数 `request`：类型为 `const QNetworkRequest &`。没有默认值，调用时必须提供。请求描述对象，通常包含 URL、请求头和传输选项；它不等于响应或实际连接。
- 参数 `context`：类型为 `const QRestAccessManager::ContextTypeForFunctor<Functor> *`。没有默认值，调用时必须提供。上下文对象，用于限定回调连接的生命周期或解析/执行环境。
- 参数 `callback`：类型为 `Functor &&`。没有默认值，调用时必须提供。回调或函数对象。要确认可调用签名、捕获对象生命周期和执行线程，不要在回调中做长时间阻塞工作。

**正确调用组合：** 通常与 `QNetworkRequest`、`QNetworkReply::finished`、错误信号和 `deleteLater()` 一起使用。

### `template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *QRestAccessManager::get(const QNetworkRequest &request, const QByteArray &data, const QRestAccessManager::ContextTypeForFunctor<Functor> *context, Functor &&callback)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QRestAccessManager` 的核心操作 `get`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *`。
- 参数 `request`：类型为 `const QNetworkRequest &`。没有默认值，调用时必须提供。请求描述对象，通常包含 URL、请求头和传输选项；它不等于响应或实际连接。
- 参数 `data`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `context`：类型为 `const QRestAccessManager::ContextTypeForFunctor<Functor> *`。没有默认值，调用时必须提供。上下文对象，用于限定回调连接的生命周期或解析/执行环境。
- 参数 `callback`：类型为 `Functor &&`。没有默认值，调用时必须提供。回调或函数对象。要确认可调用签名、捕获对象生命周期和执行线程，不要在回调中做长时间阻塞工作。

**正确调用组合：** 通常与 `QNetworkRequest`、`QNetworkReply::finished`、错误信号和 `deleteLater()` 一起使用。

### `template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *QRestAccessManager::get(const QNetworkRequest &request, QIODevice *data, const QRestAccessManager::ContextTypeForFunctor<Functor> *context, Functor &&callback)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QRestAccessManager` 的核心操作 `get`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *`。
- 参数 `request`：类型为 `const QNetworkRequest &`。没有默认值，调用时必须提供。请求描述对象，通常包含 URL、请求头和传输选项；它不等于响应或实际连接。
- 参数 `data`：类型为 `QIODevice *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `context`：类型为 `const QRestAccessManager::ContextTypeForFunctor<Functor> *`。没有默认值，调用时必须提供。上下文对象，用于限定回调连接的生命周期或解析/执行环境。
- 参数 `callback`：类型为 `Functor &&`。没有默认值，调用时必须提供。回调或函数对象。要确认可调用签名、捕获对象生命周期和执行线程，不要在回调中做长时间阻塞工作。

**正确调用组合：** 通常与 `QNetworkRequest`、`QNetworkReply::finished`、错误信号和 `deleteLater()` 一起使用。

### `template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *QRestAccessManager::get(const QNetworkRequest &request, const QJsonDocument &data, const QRestAccessManager::ContextTypeForFunctor<Functor> *context, Functor &&callback)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QRestAccessManager` 的核心操作 `get`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *`。
- 参数 `request`：类型为 `const QNetworkRequest &`。没有默认值，调用时必须提供。请求描述对象，通常包含 URL、请求头和传输选项；它不等于响应或实际连接。
- 参数 `data`：类型为 `const QJsonDocument &`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `context`：类型为 `const QRestAccessManager::ContextTypeForFunctor<Functor> *`。没有默认值，调用时必须提供。上下文对象，用于限定回调连接的生命周期或解析/执行环境。
- 参数 `callback`：类型为 `Functor &&`。没有默认值，调用时必须提供。回调或函数对象。要确认可调用签名、捕获对象生命周期和执行线程，不要在回调中做长时间阻塞工作。

**正确调用组合：** 通常与 `QNetworkRequest`、`QNetworkReply::finished`、错误信号和 `deleteLater()` 一起使用。

### `template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *QRestAccessManager::head(const QNetworkRequest &request, const QRestAccessManager::ContextTypeForFunctor<Functor> *context, Functor &&callback)`

**API 类别：** 成员函数说明

**中文解读：** `QRestAccessManager::head` 用于计算、查询或取得与“head”相关的操作。调用时要先确认当前状态和 `request`、`context`、`callback` 的有效范围；返回类型是 `template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *`。
- 参数 `request`：类型为 `const QNetworkRequest &`。没有默认值，调用时必须提供。请求描述对象，通常包含 URL、请求头和传输选项；它不等于响应或实际连接。
- 参数 `context`：类型为 `const QRestAccessManager::ContextTypeForFunctor<Functor> *`。没有默认值，调用时必须提供。上下文对象，用于限定回调连接的生命周期或解析/执行环境。
- 参数 `callback`：类型为 `Functor &&`。没有默认值，调用时必须提供。回调或函数对象。要确认可调用签名、捕获对象生命周期和执行线程，不要在回调中做长时间阻塞工作。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QNetworkAccessManager *QRestAccessManager::networkAccessManager() const`

**API 类别：** 成员函数说明

**中文解读：** `QRestAccessManager::networkAccessManager` 用于计算、查询或取得与“network、Access、Manager”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QNetworkAccessManager *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QNetworkAccessManager *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *QRestAccessManager::patch(const QNetworkRequest &request, const QJsonDocument &data, const QRestAccessManager::ContextTypeForFunctor<Functor> *context, Functor &&callback)`

**API 类别：** 成员函数说明

**中文解读：** `QRestAccessManager::patch` 用于计算、查询或取得与“patch”相关的操作。调用时要先确认当前状态和 `request`、`data`、`context`、`callback` 的有效范围；返回类型是 `template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *`。
- 参数 `request`：类型为 `const QNetworkRequest &`。没有默认值，调用时必须提供。请求描述对象，通常包含 URL、请求头和传输选项；它不等于响应或实际连接。
- 参数 `data`：类型为 `const QJsonDocument &`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `context`：类型为 `const QRestAccessManager::ContextTypeForFunctor<Functor> *`。没有默认值，调用时必须提供。上下文对象，用于限定回调连接的生命周期或解析/执行环境。
- 参数 `callback`：类型为 `Functor &&`。没有默认值，调用时必须提供。回调或函数对象。要确认可调用签名、捕获对象生命周期和执行线程，不要在回调中做长时间阻塞工作。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *QRestAccessManager::patch(const QNetworkRequest &request, QIODevice *data, const QRestAccessManager::ContextTypeForFunctor<Functor> *context, Functor &&callback)`

**API 类别：** 成员函数说明

**中文解读：** `QRestAccessManager::patch` 用于计算、查询或取得与“patch”相关的操作。调用时要先确认当前状态和 `request`、`data`、`context`、`callback` 的有效范围；返回类型是 `template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *`。
- 参数 `request`：类型为 `const QNetworkRequest &`。没有默认值，调用时必须提供。请求描述对象，通常包含 URL、请求头和传输选项；它不等于响应或实际连接。
- 参数 `data`：类型为 `QIODevice *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `context`：类型为 `const QRestAccessManager::ContextTypeForFunctor<Functor> *`。没有默认值，调用时必须提供。上下文对象，用于限定回调连接的生命周期或解析/执行环境。
- 参数 `callback`：类型为 `Functor &&`。没有默认值，调用时必须提供。回调或函数对象。要确认可调用签名、捕获对象生命周期和执行线程，不要在回调中做长时间阻塞工作。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *QRestAccessManager::patch(const QNetworkRequest &request, const QByteArray &data, const QRestAccessManager::ContextTypeForFunctor<Functor> *context, Functor &&callback)`

**API 类别：** 成员函数说明

**中文解读：** `QRestAccessManager::patch` 用于计算、查询或取得与“patch”相关的操作。调用时要先确认当前状态和 `request`、`data`、`context`、`callback` 的有效范围；返回类型是 `template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *`。
- 参数 `request`：类型为 `const QNetworkRequest &`。没有默认值，调用时必须提供。请求描述对象，通常包含 URL、请求头和传输选项；它不等于响应或实际连接。
- 参数 `data`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `context`：类型为 `const QRestAccessManager::ContextTypeForFunctor<Functor> *`。没有默认值，调用时必须提供。上下文对象，用于限定回调连接的生命周期或解析/执行环境。
- 参数 `callback`：类型为 `Functor &&`。没有默认值，调用时必须提供。回调或函数对象。要确认可调用签名、捕获对象生命周期和执行线程，不要在回调中做长时间阻塞工作。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *QRestAccessManager::patch(const QNetworkRequest &request, const QVariantMap &data, const QRestAccessManager::ContextTypeForFunctor<Functor> *context, Functor &&callback)`

**API 类别：** 成员函数说明

**中文解读：** `QRestAccessManager::patch` 用于计算、查询或取得与“patch”相关的操作。调用时要先确认当前状态和 `request`、`data`、`context`、`callback` 的有效范围；返回类型是 `template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *`。
- 参数 `request`：类型为 `const QNetworkRequest &`。没有默认值，调用时必须提供。请求描述对象，通常包含 URL、请求头和传输选项；它不等于响应或实际连接。
- 参数 `data`：类型为 `const QVariantMap &`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `context`：类型为 `const QRestAccessManager::ContextTypeForFunctor<Functor> *`。没有默认值，调用时必须提供。上下文对象，用于限定回调连接的生命周期或解析/执行环境。
- 参数 `callback`：类型为 `Functor &&`。没有默认值，调用时必须提供。回调或函数对象。要确认可调用签名、捕获对象生命周期和执行线程，不要在回调中做长时间阻塞工作。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *QRestAccessManager::post(const QNetworkRequest &request, const QJsonDocument &data, const QRestAccessManager::ContextTypeForFunctor<Functor> *context, Functor &&callback)`

**API 类别：** 成员函数说明

**中文解读：** `QRestAccessManager::post` 用于计算、查询或取得与“post”相关的操作。调用时要先确认当前状态和 `request`、`data`、`context`、`callback` 的有效范围；返回类型是 `template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *`。
- 参数 `request`：类型为 `const QNetworkRequest &`。没有默认值，调用时必须提供。请求描述对象，通常包含 URL、请求头和传输选项；它不等于响应或实际连接。
- 参数 `data`：类型为 `const QJsonDocument &`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `context`：类型为 `const QRestAccessManager::ContextTypeForFunctor<Functor> *`。没有默认值，调用时必须提供。上下文对象，用于限定回调连接的生命周期或解析/执行环境。
- 参数 `callback`：类型为 `Functor &&`。没有默认值，调用时必须提供。回调或函数对象。要确认可调用签名、捕获对象生命周期和执行线程，不要在回调中做长时间阻塞工作。

**正确调用组合：** 通常与 Content-Type、请求体编码、finished/errorOccurred 和 HTTP 状态码检查一起使用。

### `template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *QRestAccessManager::post(const QNetworkRequest &request, QHttpMultiPart *data, const QRestAccessManager::ContextTypeForFunctor<Functor> *context, Functor &&callback)`

**API 类别：** 成员函数说明

**中文解读：** `QRestAccessManager::post` 用于计算、查询或取得与“post”相关的操作。调用时要先确认当前状态和 `request`、`data`、`context`、`callback` 的有效范围；返回类型是 `template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *`。
- 参数 `request`：类型为 `const QNetworkRequest &`。没有默认值，调用时必须提供。请求描述对象，通常包含 URL、请求头和传输选项；它不等于响应或实际连接。
- 参数 `data`：类型为 `QHttpMultiPart *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `context`：类型为 `const QRestAccessManager::ContextTypeForFunctor<Functor> *`。没有默认值，调用时必须提供。上下文对象，用于限定回调连接的生命周期或解析/执行环境。
- 参数 `callback`：类型为 `Functor &&`。没有默认值，调用时必须提供。回调或函数对象。要确认可调用签名、捕获对象生命周期和执行线程，不要在回调中做长时间阻塞工作。

**正确调用组合：** 通常与 Content-Type、请求体编码、finished/errorOccurred 和 HTTP 状态码检查一起使用。

### `template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *QRestAccessManager::post(const QNetworkRequest &request, QIODevice *data, const QRestAccessManager::ContextTypeForFunctor<Functor> *context, Functor &&callback)`

**API 类别：** 成员函数说明

**中文解读：** `QRestAccessManager::post` 用于计算、查询或取得与“post”相关的操作。调用时要先确认当前状态和 `request`、`data`、`context`、`callback` 的有效范围；返回类型是 `template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *`。
- 参数 `request`：类型为 `const QNetworkRequest &`。没有默认值，调用时必须提供。请求描述对象，通常包含 URL、请求头和传输选项；它不等于响应或实际连接。
- 参数 `data`：类型为 `QIODevice *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `context`：类型为 `const QRestAccessManager::ContextTypeForFunctor<Functor> *`。没有默认值，调用时必须提供。上下文对象，用于限定回调连接的生命周期或解析/执行环境。
- 参数 `callback`：类型为 `Functor &&`。没有默认值，调用时必须提供。回调或函数对象。要确认可调用签名、捕获对象生命周期和执行线程，不要在回调中做长时间阻塞工作。

**正确调用组合：** 通常与 Content-Type、请求体编码、finished/errorOccurred 和 HTTP 状态码检查一起使用。

### `template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *QRestAccessManager::post(const QNetworkRequest &request, const QByteArray &data, const QRestAccessManager::ContextTypeForFunctor<Functor> *context, Functor &&callback)`

**API 类别：** 成员函数说明

**中文解读：** `QRestAccessManager::post` 用于计算、查询或取得与“post”相关的操作。调用时要先确认当前状态和 `request`、`data`、`context`、`callback` 的有效范围；返回类型是 `template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *`。
- 参数 `request`：类型为 `const QNetworkRequest &`。没有默认值，调用时必须提供。请求描述对象，通常包含 URL、请求头和传输选项；它不等于响应或实际连接。
- 参数 `data`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `context`：类型为 `const QRestAccessManager::ContextTypeForFunctor<Functor> *`。没有默认值，调用时必须提供。上下文对象，用于限定回调连接的生命周期或解析/执行环境。
- 参数 `callback`：类型为 `Functor &&`。没有默认值，调用时必须提供。回调或函数对象。要确认可调用签名、捕获对象生命周期和执行线程，不要在回调中做长时间阻塞工作。

**正确调用组合：** 通常与 Content-Type、请求体编码、finished/errorOccurred 和 HTTP 状态码检查一起使用。

### `template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *QRestAccessManager::post(const QNetworkRequest &request, const QVariantMap &data, const QRestAccessManager::ContextTypeForFunctor<Functor> *context, Functor &&callback)`

**API 类别：** 成员函数说明

**中文解读：** `QRestAccessManager::post` 用于计算、查询或取得与“post”相关的操作。调用时要先确认当前状态和 `request`、`data`、`context`、`callback` 的有效范围；返回类型是 `template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *`。
- 参数 `request`：类型为 `const QNetworkRequest &`。没有默认值，调用时必须提供。请求描述对象，通常包含 URL、请求头和传输选项；它不等于响应或实际连接。
- 参数 `data`：类型为 `const QVariantMap &`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `context`：类型为 `const QRestAccessManager::ContextTypeForFunctor<Functor> *`。没有默认值，调用时必须提供。上下文对象，用于限定回调连接的生命周期或解析/执行环境。
- 参数 `callback`：类型为 `Functor &&`。没有默认值，调用时必须提供。回调或函数对象。要确认可调用签名、捕获对象生命周期和执行线程，不要在回调中做长时间阻塞工作。

**正确调用组合：** 通常与 Content-Type、请求体编码、finished/errorOccurred 和 HTTP 状态码检查一起使用。

### `template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *QRestAccessManager::put(const QNetworkRequest &request, const QJsonDocument &data, const QRestAccessManager::ContextTypeForFunctor<Functor> *context, Functor &&callback)`

**API 类别：** 成员函数说明

**中文解读：** `QRestAccessManager::put` 用于计算、查询或取得与“put”相关的操作。调用时要先确认当前状态和 `request`、`data`、`context`、`callback` 的有效范围；返回类型是 `template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *`。
- 参数 `request`：类型为 `const QNetworkRequest &`。没有默认值，调用时必须提供。请求描述对象，通常包含 URL、请求头和传输选项；它不等于响应或实际连接。
- 参数 `data`：类型为 `const QJsonDocument &`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `context`：类型为 `const QRestAccessManager::ContextTypeForFunctor<Functor> *`。没有默认值，调用时必须提供。上下文对象，用于限定回调连接的生命周期或解析/执行环境。
- 参数 `callback`：类型为 `Functor &&`。没有默认值，调用时必须提供。回调或函数对象。要确认可调用签名、捕获对象生命周期和执行线程，不要在回调中做长时间阻塞工作。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *QRestAccessManager::put(const QNetworkRequest &request, QHttpMultiPart *data, const QRestAccessManager::ContextTypeForFunctor<Functor> *context, Functor &&callback)`

**API 类别：** 成员函数说明

**中文解读：** `QRestAccessManager::put` 用于计算、查询或取得与“put”相关的操作。调用时要先确认当前状态和 `request`、`data`、`context`、`callback` 的有效范围；返回类型是 `template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *`。
- 参数 `request`：类型为 `const QNetworkRequest &`。没有默认值，调用时必须提供。请求描述对象，通常包含 URL、请求头和传输选项；它不等于响应或实际连接。
- 参数 `data`：类型为 `QHttpMultiPart *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `context`：类型为 `const QRestAccessManager::ContextTypeForFunctor<Functor> *`。没有默认值，调用时必须提供。上下文对象，用于限定回调连接的生命周期或解析/执行环境。
- 参数 `callback`：类型为 `Functor &&`。没有默认值，调用时必须提供。回调或函数对象。要确认可调用签名、捕获对象生命周期和执行线程，不要在回调中做长时间阻塞工作。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *QRestAccessManager::put(const QNetworkRequest &request, QIODevice *data, const QRestAccessManager::ContextTypeForFunctor<Functor> *context, Functor &&callback)`

**API 类别：** 成员函数说明

**中文解读：** `QRestAccessManager::put` 用于计算、查询或取得与“put”相关的操作。调用时要先确认当前状态和 `request`、`data`、`context`、`callback` 的有效范围；返回类型是 `template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *`。
- 参数 `request`：类型为 `const QNetworkRequest &`。没有默认值，调用时必须提供。请求描述对象，通常包含 URL、请求头和传输选项；它不等于响应或实际连接。
- 参数 `data`：类型为 `QIODevice *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `context`：类型为 `const QRestAccessManager::ContextTypeForFunctor<Functor> *`。没有默认值，调用时必须提供。上下文对象，用于限定回调连接的生命周期或解析/执行环境。
- 参数 `callback`：类型为 `Functor &&`。没有默认值，调用时必须提供。回调或函数对象。要确认可调用签名、捕获对象生命周期和执行线程，不要在回调中做长时间阻塞工作。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *QRestAccessManager::put(const QNetworkRequest &request, const QByteArray &data, const QRestAccessManager::ContextTypeForFunctor<Functor> *context, Functor &&callback)`

**API 类别：** 成员函数说明

**中文解读：** `QRestAccessManager::put` 用于计算、查询或取得与“put”相关的操作。调用时要先确认当前状态和 `request`、`data`、`context`、`callback` 的有效范围；返回类型是 `template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *`。
- 参数 `request`：类型为 `const QNetworkRequest &`。没有默认值，调用时必须提供。请求描述对象，通常包含 URL、请求头和传输选项；它不等于响应或实际连接。
- 参数 `data`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `context`：类型为 `const QRestAccessManager::ContextTypeForFunctor<Functor> *`。没有默认值，调用时必须提供。上下文对象，用于限定回调连接的生命周期或解析/执行环境。
- 参数 `callback`：类型为 `Functor &&`。没有默认值，调用时必须提供。回调或函数对象。要确认可调用签名、捕获对象生命周期和执行线程，不要在回调中做长时间阻塞工作。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *QRestAccessManager::put(const QNetworkRequest &request, const QVariantMap &data, const QRestAccessManager::ContextTypeForFunctor<Functor> *context, Functor &&callback)`

**API 类别：** 成员函数说明

**中文解读：** `QRestAccessManager::put` 用于计算、查询或取得与“put”相关的操作。调用时要先确认当前状态和 `request`、`data`、`context`、`callback` 的有效范围；返回类型是 `template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *`。
- 参数 `request`：类型为 `const QNetworkRequest &`。没有默认值，调用时必须提供。请求描述对象，通常包含 URL、请求头和传输选项；它不等于响应或实际连接。
- 参数 `data`：类型为 `const QVariantMap &`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `context`：类型为 `const QRestAccessManager::ContextTypeForFunctor<Functor> *`。没有默认值，调用时必须提供。上下文对象，用于限定回调连接的生命周期或解析/执行环境。
- 参数 `callback`：类型为 `Functor &&`。没有默认值，调用时必须提供。回调或函数对象。要确认可调用签名、捕获对象生命周期和执行线程，不要在回调中做长时间阻塞工作。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *QRestAccessManager::sendCustomRequest(const QNetworkRequest &request, const QByteArray &method, const QByteArray &data, const QRestAccessManager::ContextTypeForFunctor<Functor> *context, Functor &&callback)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QRestAccessManager` 的核心操作 `sendCustomRequest`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *`。
- 参数 `request`：类型为 `const QNetworkRequest &`。没有默认值，调用时必须提供。请求描述对象，通常包含 URL、请求头和传输选项；它不等于响应或实际连接。
- 参数 `method`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `data`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `context`：类型为 `const QRestAccessManager::ContextTypeForFunctor<Functor> *`。没有默认值，调用时必须提供。上下文对象，用于限定回调连接的生命周期或解析/执行环境。
- 参数 `callback`：类型为 `Functor &&`。没有默认值，调用时必须提供。回调或函数对象。要确认可调用签名、捕获对象生命周期和执行线程，不要在回调中做长时间阻塞工作。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *QRestAccessManager::sendCustomRequest(const QNetworkRequest &request, const QByteArray &method, QHttpMultiPart *data, const QRestAccessManager::ContextTypeForFunctor<Functor> *context, Functor &&callback)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QRestAccessManager` 的核心操作 `sendCustomRequest`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *`。
- 参数 `request`：类型为 `const QNetworkRequest &`。没有默认值，调用时必须提供。请求描述对象，通常包含 URL、请求头和传输选项；它不等于响应或实际连接。
- 参数 `method`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `data`：类型为 `QHttpMultiPart *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `context`：类型为 `const QRestAccessManager::ContextTypeForFunctor<Functor> *`。没有默认值，调用时必须提供。上下文对象，用于限定回调连接的生命周期或解析/执行环境。
- 参数 `callback`：类型为 `Functor &&`。没有默认值，调用时必须提供。回调或函数对象。要确认可调用签名、捕获对象生命周期和执行线程，不要在回调中做长时间阻塞工作。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *QRestAccessManager::sendCustomRequest(const QNetworkRequest &request, const QByteArray &method, QIODevice *data, const QRestAccessManager::ContextTypeForFunctor<Functor> *context, Functor &&callback)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QRestAccessManager` 的核心操作 `sendCustomRequest`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`template <typename Functor, QRestAccessManager::if_compatible_callback<Functor>> QNetworkReply *`。
- 参数 `request`：类型为 `const QNetworkRequest &`。没有默认值，调用时必须提供。请求描述对象，通常包含 URL、请求头和传输选项；它不等于响应或实际连接。
- 参数 `method`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `data`：类型为 `QIODevice *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `context`：类型为 `const QRestAccessManager::ContextTypeForFunctor<Functor> *`。没有默认值，调用时必须提供。上下文对象，用于限定回调连接的生命周期或解析/执行环境。
- 参数 `callback`：类型为 `Functor &&`。没有默认值，调用时必须提供。回调或函数对象。要确认可调用签名、捕获对象生命周期和执行线程，不要在回调中做长时间阻塞工作。

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

`QRestAccessManager` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
