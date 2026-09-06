# QNetworkAddressEntry

> Qt 6.11.1 · Qt Network

## 1. 先建立直觉

**一句话定位：** `QNetworkAddressEntry` 是 Qt Network 的“网络AddressEntry”类型，负责描述请求/地址/连接状态或承载异步网络数据。

**模块背景：** Qt Network 提供 TCP/UDP、HTTP、代理、DNS、SSL 和网络请求等异步网络能力。

### 这是什么

`QNetworkAddressEntry` 是 异步网络机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 网络请求通常由管理器创建并调度，返回一个代表本次操作的 reply。连接建立、DNS、发送、接收和错误都是事件驱动的阶段；响应头、状态码、body 和传输错误分别表达不同层次的信息。

**适用场景：** 创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要把异步请求当同步函数；不要只检查 `error()` 而忽略 HTTP 状态码；不要在 readyRead 中假设一次就收到完整 body；不要在 GUI 线程用阻塞等待替代信号。

## 2. 依赖与对象关系

- 头文件：`#include <QNetworkAddressEntry>`
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

- `enum DnsEligibilityStatus { DnsEligibilityUnknown, DnsEligible, DnsIneligible }`

### 公有函数

- `QNetworkAddressEntry()`
- `QNetworkAddressEntry(const QNetworkAddressEntry &other)`
- `~QNetworkAddressEntry()`
- `QHostAddress broadcast() const`
- `void clearAddressLifetime()`
- `QNetworkAddressEntry::DnsEligibilityStatus dnsEligibility() const`
- `QHostAddress ip() const`
- `bool isLifetimeKnown() const`
- `bool isPermanent() const`
- `bool isTemporary() const`
- `QHostAddress netmask() const`
- `QDeadlineTimer preferredLifetime() const`
- `int prefixLength() const`
- `void setAddressLifetime(QDeadlineTimer preferred, QDeadlineTimer validity)`
- `void setBroadcast(const QHostAddress &newBroadcast)`
- `void setDnsEligibility(QNetworkAddressEntry::DnsEligibilityStatus status)`
- `void setIp(const QHostAddress &newIp)`
- `void setNetmask(const QHostAddress &newNetmask)`
- `void setPrefixLength(int length)`
- `void swap(QNetworkAddressEntry &other)`
- `QDeadlineTimer validityLifetime() const`
- `bool operator!=(const QNetworkAddressEntry &other) const`
- `QNetworkAddressEntry & operator=(const QNetworkAddressEntry &other)`
- `bool operator==(const QNetworkAddressEntry &other) const`

### 相关非成员函数

- `(since 6.2) QDebug operator<<(QDebug debug, const QNetworkAddressEntry &entry)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QNetworkAddressEntry::DnsEligibilityStatus`

**作用与语义：**

该枚举表示某一主机地址是否有资格在域名系统（DNS）或其他类似名称解析机制中发布。一般来说，如果该地址是该机器在不确定时间内会被访问的地址，则适合发布，尽管该地址不必是永久的。例如，通过DHCP获得的地址通常符合资格，但通过密码学生成的临时IPv6地址则不符合。
- `QNetworkAddressEntry::DnsEligibilityUnknown`：`-1`;Qt 和操作系统无法判断该地址是否应发布。如果找不到符合条件的地址，应用程序可能需要应用更多启发式方法。
- `QNetworkAddressEntry::DnsEligible`：`1`;该地址有资格在DNS中发布。
- `QNetworkAddressEntry::DnsIneligible`：`0`;该地址不应在DNS中发布，也不应传输给其他方，除非作为发出数据包的源地址。

### `QNetworkAddressEntry::QNetworkAddressEntry()`

**作用与语义：**

构造一个空的 QNetworkAddressEntry 对象。

### `QNetworkAddressEntry::QNetworkAddressEntry(const QNetworkAddressEntry &other)`

**作用与语义：**

构建一个QNetworkAddressEntry对象，该对象是该对象的复制品`other`。

### `[noexcept] QNetworkAddressEntry::~QNetworkAddressEntry()`

**作用与语义：**

摧毁了这个`QNetworkAddressEntry`物体。

### `QHostAddress QNetworkAddressEntry::broadcast() const`

**作用与语义：**

返回与IPv4地址和网掩码相关的广播地址。通常可以通过将网罩中包含0的IP地址位设为1来推导出来。（换句话说，通过用网掩码的倒数对IP地址进行位数或处理）。
对于IPv6地址，该成员总是空的，因为该系统已放弃广播概念，转而采用多播。特别地，对应本地网络所有节点的主机组可以通过“所有节点”特殊组播组（地址FF02：：1）访问。

### `void QNetworkAddressEntry::clearAddressLifetime()`

**作用与语义：**

重置该地址的首选和有效寿命。通话结束后，`isLifetimeKnown()`返回`false`。

### `QNetworkAddressEntry::DnsEligibilityStatus QNetworkAddressEntry::dnsEligibility() const`

**作用与语义：**

返回该地址是否符合在域名系统（DNS）或类似名称解析机制中发布的资格。
一般来说，如果该地址是该机器在不确定时间内会被访问的地址，则适合公开，尽管不一定是永久性的。例如，通过DHCP获得的地址通常符合资格，但加密生成的临时IPv6地址则不符合。
在某些系统上，`QNetworkInterface`需要启发式地确定哪些地址符合资格。

### `QHostAddress QNetworkAddressEntry::ip() const`

**作用与语义：**

该功能返回一个在网络接口中找到的IPv4或IPv6地址。

### `bool QNetworkAddressEntry::isLifetimeKnown() const`

**作用与语义：**

如果已知地址寿命，返回`true`;如果不知道，返回`false`。如果未知寿命，`preferredLifetime()`和`validityLifetime()`都会返回`QDeadlineTimer::Forever`。

### `bool QNetworkAddressEntry::isPermanent() const`

**作用与语义：**

如果该地址在该接口上是永久的，`false`是否是临时的，返回`true`。永久地址是没有有效期且通常是静态的（手动配置的）。
如果无法确定该信息，该函数返回`true`。
注意：根据操作系统和网络配置工具的不同，如果工具未能正确向操作系统提供详细信息，临时地址可能会被解释为永久地址。

### `bool QNetworkAddressEntry::isTemporary() const`

**作用与语义：**

如果该地址在该接口上是临时的，`false`是否永久，返回`true`。

### `QHostAddress QNetworkAddressEntry::netmask() const`

**作用与语义：**

返回与IP地址关联的网络掩码。掩码以IP地址的形式表示，例如255.255.0.0。
对于IPv6地址，前缀长度转换为一个设为1的位数等于前缀长度的地址。对于前缀长度为64位（最常见的数值），网掩码将表示为一个`QHostAddress`，地址为FFFF：FFFF：FFFF：FFFF：：

### `QDeadlineTimer QNetworkAddressEntry::preferredLifetime() const`

**作用与语义：**

如果已知地址被弃用（不再优先），返回截止日期。如果地址寿命未知（见`isLifetimeKnown()`），该函数总是返回`QDeadlineTimer::Forever`。
虽然优先使用地址，但操作系统可能会将其用作新发送数据包的源地址。弃用后，该地址仍对入站数据包有效一段时间，直到最终移除（参见`validityLifetime()`）。

### `int QNetworkAddressEntry::prefixLength() const`

**作用与语义：**

返回该IP地址的前缀长度。前缀长度与网掩码中设为1的位数相匹配（参见`netmask()`）。IPv4地址的值介于0到32之间。IPv6地址的值介于0到128之间，是表示地址的首选形式。
如果无法确定前缀长度（即`netmask()`返回空QHostAddress()），该函数返回-1。

### `void QNetworkAddressEntry::setAddressLifetime(QDeadlineTimer preferred, QDeadlineTimer validity)`

**作用与语义：**

将该地址的首选和有效寿命分别设定为`preferred`和`validity`截止日期。调用后，`isLifetimeKnown()`返回`true`，即使两个参数都`QDeadlineTimer::Forever`。

### `void QNetworkAddressEntry::setBroadcast(const QHostAddress &newBroadcast)`

**作用与语义：**

将该`QNetworkAddressEntry`对象的广播IP地址设置为`newBroadcast`。

### `void QNetworkAddressEntry::setDnsEligibility(QNetworkAddressEntry::DnsEligibilityStatus status)`

**作用与语义：**

将该地址的DNS资格标志设置为`status`。

### `void QNetworkAddressEntry::setIp(const QHostAddress &newIp)`

**作用与语义：**

将`QNetworkAddressEntry`对象所包含的IP地址设置为`newIp`。

### `void QNetworkAddressEntry::setNetmask(const QHostAddress &newNetmask)`

**作用与语义：**

将该`QNetworkAddressEntry`对象所包含的网遮罩设置为`newNetmask`。设置网遮罩还会将前缀长度设置为与新的遮罩匹配。

### `void QNetworkAddressEntry::setPrefixLength(int length)`

**作用与语义：**

将该IP地址的前缀长度设置为`length`。`length`值必须对此类IP地址有效：IPv4地址应在0到32之间，IPv6地址在0到128之间。设置为任意无效值等同于设置为-1，即“无前缀长度”。
设置前缀长度也决定了网掩码（参见`netmask()`）。

### `[noexcept] void QNetworkAddressEntry::swap(QNetworkAddressEntry &other)`

**作用与语义：**

将该网络地址入口实例与`other`交换。该操作非常快速且从未失败。

### `QDeadlineTimer QNetworkAddressEntry::validityLifetime() const`

**作用与语义：**

当该地址变得无效且已知时，返回截止日期，并从网络栈中移除。如果地址寿命未知（见 `isLifetimeKnown()`），该函数总是返回`QDeadlineTimer::Forever`。
地址有效时，操作系统会接受它作为该机器的有效目的地址。是否用作新发包的源地址由包括首选寿命（见`preferredLifetime()`）在内的规则控制。

### `bool QNetworkAddressEntry::operator!=(const QNetworkAddressEntry &other) const`

**作用与语义：**

如果该网络地址条目与`other`不同，返回`true`。

### `QNetworkAddressEntry &QNetworkAddressEntry::operator=(const QNetworkAddressEntry &other)`

**作用与语义：**

复制`QNetworkAddressEntry`对象`other`。

### `bool QNetworkAddressEntry::operator==(const QNetworkAddressEntry &other) const`

**作用与语义：**

如果该网络地址条目与`other`相同，返回`true`。

### `[since 6.2] QDebug operator<<(QDebug debug, const QNetworkAddressEntry &entry)`

**作用与语义：**

将`QNetworkAddressEntry` `entry`写入流，并返回`debug`流的引用。

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

`QNetworkAddressEntry` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
