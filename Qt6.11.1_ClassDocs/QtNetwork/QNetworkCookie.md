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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 30 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QNetworkCookie::RawForm`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QNetworkCookie` 暴露的类型声明 `Raw、Form`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:RawForm`。
- 属性名：`QNetworkCookie`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.1] enum class QNetworkCookie::SameSite`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QNetworkCookie` 暴露的类型声明 `class`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:SameSite`。
- 属性名：`QNetworkCookie`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QNetworkCookie::QNetworkCookie(const QByteArray &name = QByteArray(), const QByteArray &value = QByteArray())`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkCookie` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `name`：类型为 `const QByteArray &`。默认值为 `QByteArray()`。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。
- 参数 `value`：类型为 `const QByteArray &`。默认值为 `QByteArray()`。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QNetworkCookie::QNetworkCookie(const QNetworkCookie &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkCookie` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `const QNetworkCookie &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QNetworkCookie::~QNetworkCookie()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkCookie` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QNetworkCookie::domain() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkCookie::domain` 用于计算、查询或取得与“domain”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDateTime QNetworkCookie::expirationDate() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkCookie::expirationDate` 用于计算、查询或取得与“expiration、日期”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDateTime`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QNetworkCookie::hasSameIdentifier(const QNetworkCookie &other) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `hasSameIdentifier`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `other`：类型为 `const QNetworkCookie &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QNetworkCookie::isHttpOnly() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isHttpOnly`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QNetworkCookie::isSecure() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isSecure`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QNetworkCookie::isSessionCookie() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isSessionCookie`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray QNetworkCookie::name() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkCookie::name` 用于计算、查询或取得与“名称”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkCookie::normalize(const QUrl &url)`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkCookie::normalize` 用于执行与“normalize”相关的操作。调用时要先确认当前状态和 `url` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `url`：类型为 `const QUrl &`。没有默认值，调用时必须提供。资源地址。要确认 scheme、编码、相对路径、重定向和是否包含敏感信息。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QList<QNetworkCookie> QNetworkCookie::parseCookies(QByteArrayView cookieString)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `parseCookies`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QList<QNetworkCookie>`。
- 参数 `cookieString`：类型为 `QByteArrayView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QNetworkCookie::path() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkCookie::path` 用于计算、查询或取得与“path”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.1] QNetworkCookie::SameSite QNetworkCookie::sameSitePolicy() const`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkCookie::sameSitePolicy` 用于计算、查询或取得与“same、Site、Policy”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QNetworkCookie::SameSite`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QNetworkCookie::SameSite`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkCookie::setDomain(const QString &domain)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setDomain`。调用它会改变 `QNetworkCookie` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `domain`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkCookie::setExpirationDate(const QDateTime &date)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setExpirationDate`。调用它会改变 `QNetworkCookie` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `date`：类型为 `const QDateTime &`。没有默认值，调用时必须提供。传入 `const QDateTime &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkCookie::setHttpOnly(bool enable)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setHttpOnly`。调用它会改变 `QNetworkCookie` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enable`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkCookie::setName(const QByteArray &cookieName)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setName`。调用它会改变 `QNetworkCookie` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `cookieName`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkCookie::setPath(const QString &path)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPath`。调用它会改变 `QNetworkCookie` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `path`：类型为 `const QString &`。没有默认值，调用时必须提供。路径字符串。要确认是相对路径还是绝对路径，以及它相对于哪个工作目录。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.1] void QNetworkCookie::setSameSitePolicy(QNetworkCookie::SameSite sameSite)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSameSitePolicy`。调用它会改变 `QNetworkCookie` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `sameSite`：类型为 `QNetworkCookie::SameSite`。没有默认值，调用时必须提供。传入 `QNetworkCookie::SameSite` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkCookie::setSecure(bool enable)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSecure`。调用它会改变 `QNetworkCookie` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enable`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QNetworkCookie::setValue(const QByteArray &value)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setValue`。调用它会改变 `QNetworkCookie` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `value`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] void QNetworkCookie::swap(QNetworkCookie &other)`

**API 类别：** 成员函数说明

**中文解读：** `QNetworkCookie::swap` 用于执行与“swap”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `other`：类型为 `QNetworkCookie &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray QNetworkCookie::toRawForm(QNetworkCookie::RawForm form = Full) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toRawForm`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `form`：类型为 `QNetworkCookie::RawForm`。默认值为 `Full`。传入 `QNetworkCookie::RawForm` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray QNetworkCookie::value() const`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `value`，用于取得 `QNetworkCookie` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QNetworkCookie::operator!=(const QNetworkCookie &other) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkCookie` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `other`：类型为 `const QNetworkCookie &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QNetworkCookie &QNetworkCookie::operator=(const QNetworkCookie &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkCookie` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QNetworkCookie &`。
- 参数 `other`：类型为 `const QNetworkCookie &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QNetworkCookie::operator==(const QNetworkCookie &other) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QNetworkCookie` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `other`：类型为 `const QNetworkCookie &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

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

`QNetworkCookie` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
