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

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum class QSslCertificate::PatternSyntax`

**作用与语义：**

用于解释图案含义的语法。
- `QSslCertificate::PatternSyntax::RegularExpression`：`0`;一种丰富的类Perl模式匹配语法。
- `QSslCertificate::PatternSyntax::Wildcard`：`1`;这提供了一种简单的模式匹配语法，类似于shell（命令解释器）用于“文件globbing”的语法。参见`QRegularExpression::fromWildcard()`。
- `QSslCertificate::PatternSyntax::FixedString`：`2`;该模式是一个固定字符串。这等同于在字符串上使用正则表达式模式，其中所有元字符都通过 escape() 逃脱。这是默认的。

### `enum QSslCertificate::SubjectInfo`

**作用与语义：**

描述了你可以将密钥传递给`QSslCertificate::issuerInfo()`或`QSslCertificate::subjectInfo()`，以获取关于证书发行方或主题的信息。
- `QSslCertificate::Organization`：`0`;“O” 组织名称。
- `QSslCertificate::CommonName`：`1`;“CN”通用名称;通常用于存储主机名称。
- `QSslCertificate::LocalityName`：`2`;“L”。地名。
- `QSslCertificate::OrganizationalUnitName`：`3`;“OU”组织单位名称。
- `QSslCertificate::CountryName`：`4`;“C”国家。
- `QSslCertificate::StateOrProvinceName`：`5`;“ST”代表州或省。
- `QSslCertificate::DistinguishedNameQualifier`：`6`;尊贵姓名资格
- `QSslCertificate::SerialNumber`：`7`;证书的序列号
- `QSslCertificate::EmailAddress`：`8`;与证书关联的电子邮件地址

### `[explicit] QSslCertificate::QSslCertificate(QIODevice *device, QSsl::EncodingFormat format = QSsl::Pem)`

**作用与语义：**

通过读取`device`编码数据并使用第一个找到的证书`format`构建QSslCertificate。之后你可以调用`isNull()`查看`device`是否包含证书，以及该证书是否成功加载。

### `[explicit] QSslCertificate::QSslCertificate(const QByteArray &data = QByteArray(), QSsl::EncodingFormat format = QSsl::Pem)`

**作用与语义：**

通过解析`format`编码的`data`并使用第一个可用的证书构建QSslCertificate。之后你可以调用`isNull()`查看该证书是否包含`data`证书，以及该证书是否成功加载。

### `QSslCertificate::QSslCertificate(const QSslCertificate &other)`

**作用与语义：**

制造了一个与`other`一模一样的复制品。

### `[constexpr noexcept, since 6.8] QSslCertificate::QSslCertificate(QSslCertificate &&other)`

**作用与语义：**

Move-从`other`构建新的QSsl证书。
注意：移除对象 `other` 处于部分成形状态，唯一有效的操作是销毁和赋予新值。

### `[noexcept] QSslCertificate::~QSslCertificate()`

**作用与语义：**

毁掉`QSslCertificate`。

### `void QSslCertificate::clear()`

**作用与语义：**

清除此证书的内容，使其为 null 证书。

### `QByteArray QSslCertificate::digest(QCryptographicHash::Algorithm algorithm = QCryptographicHash::Md5) const`

**作用与语义：**

返回该证书的密码摘要。默认情况下，会生成MD5摘要，但您也可以指定自定义`algorithm`。

### `QDateTime QSslCertificate::effectiveDate() const`

**作用与语义：**

返回证书生效的日期时间，若为空证书则返回空`QDateTime`。

### `QDateTime QSslCertificate::expiryDate() const`

**作用与语义：**

返回证书到期的日期时间，如果是空证书则返回空`QDateTime`。

### `QList<QSslCertificateExtension> QSslCertificate::extensions() const`

**作用与语义：**

返回包含该证书X509扩展的列表。

### `[static] QList<QSslCertificate> QSslCertificate::fromData(const QByteArray &data, QSsl::EncodingFormat format = QSsl::Pem)`

**作用与语义：**

搜索并解析所有编码在指定`format`中的`data`证书，并返回证书列表。

### `[static] QList<QSslCertificate> QSslCertificate::fromDevice(QIODevice *device, QSsl::EncodingFormat format = QSsl::Pem)`

**作用与语义：**

搜索并解析所有编码在指定`format`中的`device`证书，并返回证书列表。

### `[static, since 6.10] QList<QSslCertificate> QSslCertificate::fromFile(const QString &filePath, QSsl::EncodingFormat format = QSsl::Pem)`

**作用与语义：**

从文件`filePath`读取数据，解析指定`format`中编码的所有证书，返回`QSslCertificate`对象列表。
如果`filePath`不是普通文件，该方法会返回一个空列表。

### `[static] QList<QSslCertificate> QSslCertificate::fromPath(const QString &path, QSsl::EncodingFormat format = QSsl::Pem, QSslCertificate::PatternSyntax syntax = PatternSyntax::FixedString)`

**作用与语义：**

搜索`path`中所有文件，查找以指定`format`编码的证书，并以列表返回。`path`必须是与一个或多个文件匹配的文件或模式，符合`syntax`的规定。

**官方示例：**

```cpp
 const auto certs = QSslCertificate::fromPath("C:/ssl/certificate.*.pem",
                                              QSsl::Pem, QSslCertificate::Wildcard);
 for (const QSslCertificate &cert : certs) {
     qDebug() << cert.issuerInfo(QSslCertificate::Organization);
 }
```

### `Qt::HANDLE QSslCertificate::handle() const`

**作用与语义：**

如果有本地证书句柄，返回指向该地址的指针，否则`nullptr`。
你可以使用该句号，结合本地 API，访问关于证书的扩展信息。
警告：该功能的使用很可能不可移植，且其返回值可能因平台而异，或在次要版本间有所变化。

### `[static] bool QSslCertificate::importPkcs12(QIODevice *device, QSslKey *key, QSslCertificate *certificate, QList<QSslCertificate> *caCertificates = nullptr, const QByteArray &passPhrase = QByteArray())`

**作用与语义：**

从指定的 `device` 导入 PKCS#12 (pfx) 文件。PKCS#12 文件是一个可以包含多个证书和密钥的捆绑包。此方法从捆绑包中读取单个 `key`、其 `certificate` 及任何相关的 `caCertificates`。如果指定了 `passPhrase`，则将用于解密捆绑包。如果 PKCS#12 文件加载成功，则返回 `true`。
注意：`device` 必须是打开状态且可读取。

### `bool QSslCertificate::isBlacklisted() const`

**作用与语义：**

如果该证书被列入黑名单，返回`true`;否则返回`false`。

### `bool QSslCertificate::isNull() const`

**作用与语义：**

如果是空证书（即无内容的证书），返回`true`;否则返回`false`。
默认情况下，`QSslCertificate`构造一个空证书。

### `bool QSslCertificate::isSelfSigned() const`

**作用与语义：**

如果该证书是自签名，返回`true`;否则返回`false`。
证书被视为自签名，其发行方和主题是相同的。

### `QString QSslCertificate::issuerDisplayName() const`

**作用与语义：**

返回描述发行人的名称。如果有`QSslCertificate::CommonName`，返回，否则回退到第一个`QSslCertificate::Organization`或第一个`QSslCertificate::OrganizationalUnitName`。

### `QStringList QSslCertificate::issuerInfo(QSslCertificate::SubjectInfo subject) const`

**作用与语义：**

从证书中返回`subject`的发行者信息，或者如果证书中没有`subject`信息，则返回一个空列表。每种类型的条目可以有多个条目。

### `QStringList QSslCertificate::issuerInfo(const QByteArray &attribute) const`

**作用与语义：**

返回发行者信息，返回证书中的`attribute`信息，或者如果证书中没有`attribute`信息，则返回一个空列表。一个属性可以有多个条目。

### `QList<QByteArray> QSslCertificate::issuerInfoAttributes() const`

**作用与语义：**

返回该证书的发行者信息中具有值的属性列表。与给定属性相关的信息可以通过`issuerInfo()`方法访问。请注意，该列表可能包含SSL后端未知的任何元素的OID。

### `QSslKey QSslCertificate::publicKey() const`

**作用与语义：**

返回证书主体的公钥。

### `QByteArray QSslCertificate::serialNumber() const`

**作用与语义：**

返回证书的序列号字符串，格式为十六进制格式。

### `QMultiMap<QSsl::AlternativeNameEntryType, QString> QSslCertificate::subjectAlternativeNames() const`

**作用与语义：**

返回该证书的备用主题名称列表。备用名称通常包含对该证书有效的主机名（可选带万用符）。
如果 `CommonName` 的主体信息无法定义有效的主机名，或者主体信息名称与对等端的主机名不匹配，这些名称会与连接节点的主机名进行测试。

### `QString QSslCertificate::subjectDisplayName() const`

**作用与语义：**

返回描述主题的名称。如果有，返回`QSslCertificate::CommonName`，否则回退到第一个`QSslCertificate::Organization`或第一个`QSslCertificate::OrganizationalUnitName`。

### `QStringList QSslCertificate::subjectInfo(QSslCertificate::SubjectInfo subject) const`

**作用与语义：**

返回`subject`信息，或如果证书中没有`subject`信息，则返回空列表。每种类型可以有多个条目。

### `QStringList QSslCertificate::subjectInfo(const QByteArray &attribute) const`

**作用与语义：**

返回主题信息以供`attribute`，或如果证书中没有`attribute`信息，则返回空列表。一个属性可以有多个条目。

### `QList<QByteArray> QSslCertificate::subjectInfoAttributes() const`

**作用与语义：**

返回与该证书主体信息相关值的属性列表。与给定属性相关的信息可以通过`subjectInfo()`方法访问。请注意，该列表可能包含SSL后端未知的任何元素的OID。

### `[noexcept] void QSslCertificate::swap(QSslCertificate &other)`

**作用与语义：**

将该证书实例与`other`交换。此操作非常快速且从未失败。

### `QByteArray QSslCertificate::toDer() const`

**作用与语义：**

返回该证书转换为DER（二进制）编码表示。

### `QByteArray QSslCertificate::toPem() const`

**作用与语义：**

返回该证书转换为PEM（Base64）编码表示。

### `QString QSslCertificate::toText() const`

**作用与语义：**

返回该证书转换为人类可读文本表示。

### `[static] QList<QSslError> QSslCertificate::verify(const QList<QSslCertificate> &certificateChain, const QString &hostName = QString())`

**作用与语义：**

验证证书链。待验证链在`certificateChain`参数中传递。列表中的第一个证书应是待验证链的叶子证书。如果指定了`hostName`，则还会检查证书是否适用于指定的主机名称。
注意，根证书（CA）不应包含在待验证列表中，该列表将通过默认`QSslConfiguration`中指定的CA列表自动查找，此外，如果可能的话，还会在Unix和Windows上按需加载CA证书。

### `QByteArray QSslCertificate::version() const`

**作用与语义：**

返回证书的版本字符串。

### `bool QSslCertificate::operator!=(const QSslCertificate &other) const`

**作用与语义：**

如果该证书与`other`不同，返回`true`;否则返回`false`。

### `QSslCertificate &QSslCertificate::operator=(const QSslCertificate &other)`

**作用与语义：**

将`other`的内容复制到该证书中，使两份证书完全相同。

### `bool QSslCertificate::operator==(const QSslCertificate &other) const`

**作用与语义：**

如果该证书与`other`相同，返回`true`;否则返回`false`。

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
