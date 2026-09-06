# QDnsTlsAssociationRecord

> Qt 6.11.1 · Qt Network

## 1. 先建立直觉

**一句话定位：** `QDnsTlsAssociationRecord` 是 Qt Network 的“DnsTlsAssociation记录”类型，负责描述请求/地址/连接状态或承载异步网络数据。

**模块背景：** Qt Network 提供 TCP/UDP、HTTP、代理、DNS、SSL 和网络请求等异步网络能力。

### 这是什么

`QDnsTlsAssociationRecord` 是 异步网络机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 网络请求通常由管理器创建并调度，返回一个代表本次操作的 reply。连接建立、DNS、发送、接收和错误都是事件驱动的阶段；响应头、状态码、body 和传输错误分别表达不同层次的信息。

**适用场景：** 创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要把异步请求当同步函数；不要只检查 `error()` 而忽略 HTTP 状态码；不要在 readyRead 中假设一次就收到完整 body；不要在 GUI 线程用阻塞等待替代信号。

## 2. 依赖与对象关系

- 头文件：`#include <QDnsTlsAssociationRecord>`
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

- `enum class CertificateUsage { CertificateAuthorityConstrait, ServiceCertificateConstraint, TrustAnchorAssertion, DomainIssuedCertificate, PrivateUse, …, PrivCert }`
- `enum class MatchingType { Exact, Sha256, Sha512, PrivateUse, PrivMatch }`
- `enum class Selector { FullCertificate, SubjectPublicKeyInfo, PrivateUse, Cert, SPKI, PrivSel }`

### 公有函数

- `QDnsTlsAssociationRecord()`
- `QDnsTlsAssociationRecord(const QDnsTlsAssociationRecord &other)`
- `~QDnsTlsAssociationRecord()`
- `QDnsTlsAssociationRecord::MatchingType matchType() const`
- `QString name() const`
- `QDnsTlsAssociationRecord::Selector selector() const`
- `quint32 timeToLive() const`
- `QDnsTlsAssociationRecord::CertificateUsage usage() const`
- `QByteArray value() const`
- `QDnsTlsAssociationRecord & operator=(const QDnsTlsAssociationRecord &other)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum class QDnsTlsAssociationRecord::CertificateUsage`

**作用与语义：**

该枚举包含TLS关联查询中证书使用字段的有效值。以下列表为RFC 6698第2.1.1节和RFC 7218第2.1节的最新内容。请参阅这些文档以获取关于解释该枚举的权威说明。
- `QDnsTlsAssociationRecord::CertificateUsage::CertificateAuthorityConstrait`：`0`;表示记录包含与特定证书授权机构的关联，必须在TLS服务器的证书链中找到，并且必须通过PKIX验证。
- `QDnsTlsAssociationRecord::CertificateUsage::ServiceCertificateConstraint`：`1`;表示记录包含与证书的关联，该证书必须与TLS服务器提供的终端实体证书匹配，并且必须通过PKIX验证。
- `QDnsTlsAssociationRecord::CertificateUsage::TrustAnchorAssertion`：`2`;表示记录包含必须作为最终信任锚点以验证TLS服务器证书的证书的证书，并且必须通过PKIX验证。
- `QDnsTlsAssociationRecord::CertificateUsage::DomainIssuedCertificate`：`3`;表示记录包含与证书的关联，必须与TLS服务器提供的终端实体证书匹配。PKIX验证不进行测试。
- `QDnsTlsAssociationRecord::CertificateUsage::PrivateUse`：`255`;不适用标准含义。
- `QDnsTlsAssociationRecord::CertificateUsage::PKIX_TA`：`0`;别名;公钥基础设施信托锚点助记符
- `QDnsTlsAssociationRecord::CertificateUsage::PKIX_EE`：`1`;别名;公钥基础设施终端实体助记法
- `QDnsTlsAssociationRecord::CertificateUsage::DANE_TA`：`2`;别名;基于DNS认证的命名实体信托锚助记符
- `QDnsTlsAssociationRecord::CertificateUsage::DANE_EE`：`3`;别名;基于DNS认证命名实体的助记法终端实体
- `QDnsTlsAssociationRecord::CertificateUsage::PrivCert`：`255`;别名
其他数值目前为预留值，但未来标准可能已非保留值。即使未提供枚举器，这些数值仍可使用该枚举。

### `enum class QDnsTlsAssociationRecord::MatchingType`

**作用与语义：**

该枚举包含TLS关联查询匹配类型字段的有效值。以下列表符合RFC 6698第2.1.3节和RFC 7218第2.3节的最新信息。请参阅这些文档以获取关于解释该枚举的权威指导。
- `QDnsTlsAssociationRecord::MatchingType::Exact`：`0`;表示证书或SPKI数据是逐字存储在本记录中。
- `QDnsTlsAssociationRecord::MatchingType::Sha256`：`1`;表示这是该记录中证书或SPKI数据的SHA-256校验和。
- `QDnsTlsAssociationRecord::MatchingType::Sha512`：`2`;表示这是本记录中证书或SPKI数据的SHA-512校验和。
- `QDnsTlsAssociationRecord::MatchingType::PrivateUse`：`255`;不适用标准含义。
- `QDnsTlsAssociationRecord::MatchingType::PrivMatch`：`PrivateUse`;别名
其他数值目前为预留值，但未来标准可能已非保留值。即使未提供枚举器，这些数值仍可使用该枚举。

### `enum class QDnsTlsAssociationRecord::Selector`

**作用与语义：**

本枚举包含TLS关联查询选择器字段的有效值。以下列表为RFC 6698第2.1.2节和RFC 7218第2.2节的最新内容。请参阅这些文档以获取关于解释该枚举的权威指导。
- `QDnsTlsAssociationRecord::Selector::FullCertificate`：`0`;表示该记录指的是完整证书的二进制结构形式。
- `QDnsTlsAssociationRecord::Selector::SubjectPublicKeyInfo`：`1`;表示记录指涉证书的主题和公钥信息，采用DER编码的二进制结构形式。
- `QDnsTlsAssociationRecord::Selector::PrivateUse`：`255`;不适用标准含义。
- `QDnsTlsAssociationRecord::Selector::Cert`：`FullCertificate`;别名
- `QDnsTlsAssociationRecord::Selector::SPKI`：`SubjectPublicKeyInfo`;别名
- `QDnsTlsAssociationRecord::Selector::PrivSel`：`PrivateUse`;别名
其他数值目前为预留值，但未来标准可能已非保留值。即使未提供枚举器，这些数值仍可使用该枚举。

### `QDnsTlsAssociationRecord::QDnsTlsAssociationRecord()`

**作用与语义：**

构建一个空的TLS协会记录。

### `QDnsTlsAssociationRecord::QDnsTlsAssociationRecord(const QDnsTlsAssociationRecord &other)`

**作用与语义：**

复制了`other`。

### `[noexcept] QDnsTlsAssociationRecord::~QDnsTlsAssociationRecord()`

**作用与语义：**

销毁了这个TLS关联记录对象。

### `QDnsTlsAssociationRecord::MatchingType QDnsTlsAssociationRecord::matchType() const`

**作用与语义：**

返回该记录的匹配类型字段。

### `QString QDnsTlsAssociationRecord::name() const`

**作用与语义：**

返回这张唱片的名称。

### `QDnsTlsAssociationRecord::Selector QDnsTlsAssociationRecord::selector() const`

**作用与语义：**

返回本记录的选择器字段。

### `quint32 QDnsTlsAssociationRecord::timeToLive() const`

**作用与语义：**

返回该记录有效时长（秒数）。

### `QDnsTlsAssociationRecord::CertificateUsage QDnsTlsAssociationRecord::usage() const`

**作用与语义：**

返回该记录的证书使用字段。

### `QByteArray QDnsTlsAssociationRecord::value() const`

**作用与语义：**

返回该记录的二进制数据字段。对该二进制数据的解释依赖于 certificateUsage()、`selector()` 和 `matchType()` 提供的三个数值字段。
请注意，这其实是一个二进制字段，即使是校验和，类似于 QCyrptographicHash：：result() 返回的。

### `QDnsTlsAssociationRecord &QDnsTlsAssociationRecord::operator=(const QDnsTlsAssociationRecord &other)`

**作用与语义：**

将`other`的内容移入该对象。

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

`QDnsTlsAssociationRecord` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
