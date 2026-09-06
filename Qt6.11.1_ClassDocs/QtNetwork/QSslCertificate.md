# QSslCertificate

> Qt 6.11.1 · Qt Network

## 1. 先建立直觉

**一句话定位：** `QSslCertificate` 是 Qt Network 的“SslCertificate”类型，负责描述请求/地址/连接状态或承载异步网络数据。

**模块背景：** Qt Network 提供 TCP/UDP、HTTP、代理、DNS、SSL 和网络请求等异步网络能力。

### 这是什么

`QSslCertificate` 是 异步网络机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 网络请求通常由管理器创建并调度，返回一个代表本次操作的 reply。连接建立、DNS、发送、接收和错误都是事件驱动的阶段；响应头、状态码、body 和传输错误分别表达不同层次的信息。

**适用场景：** 创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要把异步请求当同步函数；不要只检查 `error()` 而忽略 HTTP 状态码；不要在 readyRead 中假设一次就收到完整 body；不要在 GUI 线程用阻塞等待替代信号。

## 2. 依赖与对象关系

- 头文件：`#include <QSslCertificate>`
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
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum class PatternSyntax { RegularExpression, Wildcard, FixedString }`
- `enum SubjectInfo { Organization, CommonName, LocalityName, OrganizationalUnitName, CountryName, …, EmailAddress }`

### 公有函数

- `QSslCertificate(QIODevice *device, QSsl::EncodingFormat format = QSsl::Pem)`
- `QSslCertificate(const QByteArray &data = QByteArray(), QSsl::EncodingFormat format = QSsl::Pem)`
- `QSslCertificate(const QSslCertificate &other)`
- `(since 6.8) QSslCertificate(QSslCertificate &&other)`
- `~QSslCertificate()`
- `void clear()`
- `QByteArray digest(QCryptographicHash::Algorithm algorithm = QCryptographicHash::Md5) const`
- `QDateTime effectiveDate() const`
- `QDateTime expiryDate() const`
- `QList<QSslCertificateExtension> extensions() const`
- `Qt::HANDLE handle() const`
- `bool isBlacklisted() const`
- `bool isNull() const`
- `bool isSelfSigned() const`
- `QString issuerDisplayName() const`
- `QStringList issuerInfo(QSslCertificate::SubjectInfo subject) const`
- `QStringList issuerInfo(const QByteArray &attribute) const`
- `QList<QByteArray> issuerInfoAttributes() const`
- `QSslKey publicKey() const`
- `QByteArray serialNumber() const`
- `QMultiMap<QSsl::AlternativeNameEntryType, QString> subjectAlternativeNames() const`
- `QString subjectDisplayName() const`
- `QStringList subjectInfo(QSslCertificate::SubjectInfo subject) const`
- `QStringList subjectInfo(const QByteArray &attribute) const`
- `QList<QByteArray> subjectInfoAttributes() const`
- `void swap(QSslCertificate &other)`
- `QByteArray toDer() const`
- `QByteArray toPem() const`
- `QString toText() const`
- `QByteArray version() const`
- `bool operator!=(const QSslCertificate &other) const`
- `QSslCertificate & operator=(const QSslCertificate &other)`
- `bool operator==(const QSslCertificate &other) const`

### 静态公有成员

- `QList<QSslCertificate> fromData(const QByteArray &data, QSsl::EncodingFormat format = QSsl::Pem)`
- `QList<QSslCertificate> fromDevice(QIODevice *device, QSsl::EncodingFormat format = QSsl::Pem)`
- `(since 6.10) QList<QSslCertificate> fromFile(const QString &filePath, QSsl::EncodingFormat format = QSsl::Pem)`
- `QList<QSslCertificate> fromPath(const QString &path, QSsl::EncodingFormat format = QSsl::Pem, QSslCertificate::PatternSyntax syntax = PatternSyntax::FixedString)`
- `bool importPkcs12(QIODevice *device, QSslKey *key, QSslCertificate *certificate, QList<QSslCertificate> *caCertificates = nullptr, const QByteArray &passPhrase = QByteArray())`
- `QList<QSslError> verify(const QList<QSslCertificate> &certificateChain, const QString &hostName = QString())`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 41 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum class QSslCertificate::PatternSyntax`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QSslCertificate` 暴露的类型声明 `class`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:PatternSyntax`。
- 属性名：`QSslCertificate`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QSslCertificate::SubjectInfo`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QSslCertificate` 暴露的类型声明 `Subject、Info`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:SubjectInfo`。
- 属性名：`QSslCertificate`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QSslCertificate::QSslCertificate(QIODevice *device, QSsl::EncodingFormat format = QSsl::Pem)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSslCertificate` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `device`：类型为 `QIODevice *`。没有默认值，调用时必须提供。QIODevice 或绘制设备。调用前要确认已经打开、支持所需模式，或处于合法绘制阶段。
- 参数 `format`：类型为 `QSsl::EncodingFormat`。默认值为 `QSsl::Pem`。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QSslCertificate::QSslCertificate(const QByteArray &data = QByteArray(), QSsl::EncodingFormat format = QSsl::Pem)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSslCertificate` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `data`：类型为 `const QByteArray &`。默认值为 `QByteArray()`。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `format`：类型为 `QSsl::EncodingFormat`。默认值为 `QSsl::Pem`。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslCertificate::QSslCertificate(const QSslCertificate &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSslCertificate` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `const QSslCertificate &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept, since 6.8] QSslCertificate::QSslCertificate(QSslCertificate &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSslCertificate` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `QSslCertificate &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QSslCertificate::~QSslCertificate()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSslCertificate` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QSslCertificate::clear()`

**API 类别：** 成员函数说明

**中文解读：** 这是状态清理或重置 API `clear`。调用后原有数据、索引、缓存或绑定可能失效；使用前先确认它影响的是当前对象、子对象还是底层共享资源，之后重新检查状态。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray QSslCertificate::digest(QCryptographicHash::Algorithm algorithm = QCryptographicHash::Md5) const`

**API 类别：** 成员函数说明

**中文解读：** `QSslCertificate::digest` 用于计算、查询或取得与“digest”相关的操作。调用时要先确认当前状态和 `algorithm` 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `algorithm`：类型为 `QCryptographicHash::Algorithm`。默认值为 `QCryptographicHash::Md5`。传入 `QCryptographicHash::Algorithm` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDateTime QSslCertificate::effectiveDate() const`

**API 类别：** 成员函数说明

**中文解读：** `QSslCertificate::effectiveDate` 用于计算、查询或取得与“effective、日期”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDateTime`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDateTime QSslCertificate::expiryDate() const`

**API 类别：** 成员函数说明

**中文解读：** `QSslCertificate::expiryDate` 用于计算、查询或取得与“expiry、日期”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDateTime`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QSslCertificateExtension> QSslCertificate::extensions() const`

**API 类别：** 成员函数说明

**中文解读：** `QSslCertificate::extensions` 用于计算、查询或取得与“extensions”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<QSslCertificateExtension>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QSslCertificateExtension>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QList<QSslCertificate> QSslCertificate::fromData(const QByteArray &data, QSsl::EncodingFormat format = QSsl::Pem)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromData`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QList<QSslCertificate>`。
- 参数 `data`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `format`：类型为 `QSsl::EncodingFormat`。默认值为 `QSsl::Pem`。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QList<QSslCertificate> QSslCertificate::fromDevice(QIODevice *device, QSsl::EncodingFormat format = QSsl::Pem)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromDevice`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QList<QSslCertificate>`。
- 参数 `device`：类型为 `QIODevice *`。没有默认值，调用时必须提供。QIODevice 或绘制设备。调用前要确认已经打开、支持所需模式，或处于合法绘制阶段。
- 参数 `format`：类型为 `QSsl::EncodingFormat`。默认值为 `QSsl::Pem`。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.10] QList<QSslCertificate> QSslCertificate::fromFile(const QString &filePath, QSsl::EncodingFormat format = QSsl::Pem)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromFile`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QList<QSslCertificate>`。
- 参数 `filePath`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `format`：类型为 `QSsl::EncodingFormat`。默认值为 `QSsl::Pem`。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QList<QSslCertificate> QSslCertificate::fromPath(const QString &path, QSsl::EncodingFormat format = QSsl::Pem, QSslCertificate::PatternSyntax syntax = PatternSyntax::FixedString)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromPath`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QList<QSslCertificate>`。
- 参数 `path`：类型为 `const QString &`。没有默认值，调用时必须提供。路径字符串。要确认是相对路径还是绝对路径，以及它相对于哪个工作目录。
- 参数 `format`：类型为 `QSsl::EncodingFormat`。默认值为 `QSsl::Pem`。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `syntax`：类型为 `QSslCertificate::PatternSyntax`。默认值为 `PatternSyntax::FixedString`。传入 `QSslCertificate::PatternSyntax` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Qt::HANDLE QSslCertificate::handle() const`

**API 类别：** 成员函数说明

**中文解读：** `QSslCertificate::handle` 用于计算、查询或取得与“handle”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `Qt::HANDLE`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::HANDLE`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] bool QSslCertificate::importPkcs12(QIODevice *device, QSslKey *key, QSslCertificate *certificate, QList<QSslCertificate> *caCertificates = nullptr, const QByteArray &passPhrase = QByteArray())`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `importPkcs12`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数 `device`：类型为 `QIODevice *`。没有默认值，调用时必须提供。QIODevice 或绘制设备。调用前要确认已经打开、支持所需模式，或处于合法绘制阶段。
- 参数 `key`：类型为 `QSslKey *`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `certificate`：类型为 `QSslCertificate *`。没有默认值，调用时必须提供。传入 `QSslCertificate *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `caCertificates`：类型为 `QList<QSslCertificate> *`。默认值为 `nullptr`。传入 `QList<QSslCertificate> *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `passPhrase`：类型为 `const QByteArray &`。默认值为 `QByteArray()`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QSslCertificate::isBlacklisted() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isBlacklisted`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QSslCertificate::isNull() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isNull`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QSslCertificate::isSelfSigned() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isSelfSigned`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QSslCertificate::issuerDisplayName() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `issuerDisplayName`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringList QSslCertificate::issuerInfo(QSslCertificate::SubjectInfo subject) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `issuerInfo`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`QStringList`。
- 参数 `subject`：类型为 `QSslCertificate::SubjectInfo`。没有默认值，调用时必须提供。传入 `QSslCertificate::SubjectInfo` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringList QSslCertificate::issuerInfo(const QByteArray &attribute) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `issuerInfo`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`QStringList`。
- 参数 `attribute`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QByteArray> QSslCertificate::issuerInfoAttributes() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `issuerInfoAttributes`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`QList<QByteArray>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslKey QSslCertificate::publicKey() const`

**API 类别：** 成员函数说明

**中文解读：** `QSslCertificate::publicKey` 用于计算、查询或取得与“public、Key”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSslKey`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSslKey`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray QSslCertificate::serialNumber() const`

**API 类别：** 成员函数说明

**中文解读：** `QSslCertificate::serialNumber` 用于计算、查询或取得与“serial、Number”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMultiMap<QSsl::AlternativeNameEntryType, QString> QSslCertificate::subjectAlternativeNames() const`

**API 类别：** 成员函数说明

**中文解读：** `QSslCertificate::subjectAlternativeNames` 用于计算、查询或取得与“subject、Alternative、Names”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMultiMap<QSsl::AlternativeNameEntryType, QString>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMultiMap<QSsl::AlternativeNameEntryType, QString>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QSslCertificate::subjectDisplayName() const`

**API 类别：** 成员函数说明

**中文解读：** `QSslCertificate::subjectDisplayName` 用于计算、查询或取得与“subject、Display、名称”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringList QSslCertificate::subjectInfo(QSslCertificate::SubjectInfo subject) const`

**API 类别：** 成员函数说明

**中文解读：** `QSslCertificate::subjectInfo` 用于计算、查询或取得与“subject、Info”相关的操作。调用时要先确认当前状态和 `subject` 的有效范围；返回类型是 `QStringList`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStringList`。
- 参数 `subject`：类型为 `QSslCertificate::SubjectInfo`。没有默认值，调用时必须提供。传入 `QSslCertificate::SubjectInfo` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringList QSslCertificate::subjectInfo(const QByteArray &attribute) const`

**API 类别：** 成员函数说明

**中文解读：** `QSslCertificate::subjectInfo` 用于计算、查询或取得与“subject、Info”相关的操作。调用时要先确认当前状态和 `attribute` 的有效范围；返回类型是 `QStringList`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStringList`。
- 参数 `attribute`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QByteArray> QSslCertificate::subjectInfoAttributes() const`

**API 类别：** 成员函数说明

**中文解读：** `QSslCertificate::subjectInfoAttributes` 用于计算、查询或取得与“subject、Info、Attributes”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<QByteArray>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QByteArray>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] void QSslCertificate::swap(QSslCertificate &other)`

**API 类别：** 成员函数说明

**中文解读：** `QSslCertificate::swap` 用于执行与“swap”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `other`：类型为 `QSslCertificate &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray QSslCertificate::toDer() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toDer`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray QSslCertificate::toPem() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toPem`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QSslCertificate::toText() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toText`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QList<QSslError> QSslCertificate::verify(const QList<QSslCertificate> &certificateChain, const QString &hostName = QString())`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `verify`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QList<QSslError>`。
- 参数 `certificateChain`：类型为 `const QList<QSslCertificate> &`。没有默认值，调用时必须提供。传入 `const QList<QSslCertificate> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `hostName`：类型为 `const QString &`。默认值为 `QString()`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray QSslCertificate::version() const`

**API 类别：** 成员函数说明

**中文解读：** `QSslCertificate::version` 用于计算、查询或取得与“version”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QSslCertificate::operator!=(const QSslCertificate &other) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSslCertificate` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `other`：类型为 `const QSslCertificate &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSslCertificate &QSslCertificate::operator=(const QSslCertificate &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSslCertificate` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QSslCertificate &`。
- 参数 `other`：类型为 `const QSslCertificate &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QSslCertificate::operator==(const QSslCertificate &other) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QSslCertificate` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `other`：类型为 `const QSslCertificate &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

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

`QSslCertificate` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
