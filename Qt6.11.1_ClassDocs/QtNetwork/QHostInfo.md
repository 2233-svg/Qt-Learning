# QHostInfo

> Qt 6.11.1 · Qt Network

## 1. 先建立直觉

**一句话定位：** 主机名解析结果类型，负责保存 DNS 查询得到的地址列表和错误状态。

**模块背景：** Qt Network 提供 TCP/UDP、HTTP、代理、DNS、SSL 和网络请求等异步网络能力。

### 这是什么

`QHostInfo`：主机名解析结果类型，负责保存 DNS 查询得到的地址列表和错误状态。

**内部模型：** 网络请求通常由管理器创建并调度，返回一个代表本次操作的 reply。连接建立、DNS、发送、接收和错误都是事件驱动的阶段；响应头、状态码、body 和传输错误分别表达不同层次的信息。

**适用场景：** 创建长期存在的 manager，构造带 URL 和请求头的 request，调用 get/post 等操作，连接 reply 的完成、数据、进度和错误信号，读取结果后清理 reply。敏感头部和 token 不要写入日志。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要把异步请求当同步函数；不要只检查 `error()` 而忽略 HTTP 状态码；不要在 readyRead 中假设一次就收到完整 body；不要在 GUI 线程用阻塞等待替代信号。

## 2. 依赖与对象关系

- 头文件：`#include <QHostInfo>`
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

- `enum HostInfoError { NoError, HostNotFound, UnknownError }`

### 公有函数

- `QHostInfo(int id = -1)`
- `QHostInfo(const QHostInfo &other)`
- `QHostInfo(QHostInfo &&other)`
- `~QHostInfo()`
- `QList<QHostAddress> addresses() const`
- `QHostInfo::HostInfoError error() const`
- `QString errorString() const`
- `QString hostName() const`
- `int lookupId() const`
- `void setAddresses(const QList<QHostAddress> &addresses)`
- `void setError(QHostInfo::HostInfoError error)`
- `void setErrorString(const QString &str)`
- `void setHostName(const QString &hostName)`
- `void setLookupId(int id)`
- `void swap(QHostInfo &other)`
- `QHostInfo & operator=(QHostInfo &&other)`
- `QHostInfo & operator=(const QHostInfo &other)`

### 静态公有成员

- `void abortHostLookup(int id)`
- `QHostInfo fromName(const QString &name)`
- `QString localDomainName()`
- `QString localHostName()`
- `int lookupHost(const QString &name, const QObject *receiver, const char *member)`
- `int lookupHost(const QString &name, Functor &&functor)`
- `int lookupHost(const QString &name, const QObject *context, Functor functor)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QHostInfo::HostInfoError`

**作用与语义：**

该枚举描述了尝试解析主机名称时可能出现的各种错误。
- `QHostInfo::NoError`：`0`;查找成功。
- `QHostInfo::HostNotFound`：`1`;未找到主机的IP地址。
- `QHostInfo::UnknownError`：`2`;发生了未知错误。

### `[explicit] QHostInfo::QHostInfo(int id = -1)`

**作用与语义：**

构建一个带有查询ID `id`的空主机信息对象。

### `QHostInfo::QHostInfo(const QHostInfo &other)`

**作用与语义：**

复制了`other`。

### `[noexcept] QHostInfo::QHostInfo(QHostInfo &&other)`

**作用与语义：**

从`other`移动构建一个新的QHostInfo。
注意：移出对象`other`处于部分成形状态，唯一有效的操作是销毁和赋予新值。

### `[noexcept] QHostInfo::~QHostInfo()`

**作用与语义：**

会摧毁宿主信息对象。

### `[static] void QHostInfo::abortHostLookup(int id)`

**作用与语义：**

中止`lookupHost()`返回的ID查询`id`。

### `QList<QHostAddress> QHostInfo::addresses() const`

**作用与语义：**

返回与`hostName()`关联的IP地址列表。该列表可能是空的。

**官方示例：**

```cpp
 QHostInfo info;
 ...
 if (!info.addresses().isEmpty()) {
     QHostAddress address = info.addresses().first();
     // use the first IP address
 }
```

### `QHostInfo::HostInfoError QHostInfo::error() const`

**作用与语义：**

返回主机名称查询失败时发生的错误类型;否则返回`NoError`。

### `QString QHostInfo::errorString() const`

**作用与语义：**

如果查找失败，该函数返回一个人类可读的错误描述;否则返回“未知错误”。

### `[static] QHostInfo QHostInfo::fromName(const QString &name)`

**作用与语义：**

查找给定主机的IP地址`name`。该函数在查找过程中会阻塞，这意味着程序的执行会暂停，直到查找结果准备好。返回查找结果在`QHostInfo`对象中。
如果你把一个字面上的IP地址传给`name`而不是主机名，`QHostInfo`会搜索该IP的域名（即`QHostInfo`会进行反向查找）。成功后，返回的`QHostInfo`会同时包含已解析的域名和主机名的IP地址。

### `QString QHostInfo::hostName() const`

**作用与语义：**

返回查询IP地址的主机名称。

### `[static] QString QHostInfo::localDomainName()`

**作用与语义：**

返回该机器的DNS域。
注意：DNS 域名与 Windows 网络中的域名无关。

### `[static] QString QHostInfo::localHostName()`

**作用与语义：**

如果配置了主机名，返回该机器的主机名称。注意，主机名不保证全局唯一，尤其是自动配置的。
该功能并不保证返回的主机名是完全限定域名（FQDN）。为此，使用`fromName()`将返回的域名解析为FQDN。
该函数返回的效果与`QSysInfo::machineHostName()`相同。

### `[static] int QHostInfo::lookupHost(const QString &name, const QObject *receiver, const char *member)`

**作用与语义：**

查找与主机名称`name`相关的IP地址，并返回查找的ID。当查找结果准备好时，`receiver`中`member`的槽函数或信号会被调用，并引用`QHostInfo`参数。然后可以检查`QHostInfo`对象以获取查找结果。
查找通过一个函数调用完成，例如：
该槽的实现会打印查找返回地址的基本信息，若失败则报告错误：
如果你把一个字面IP地址传递给`name`而不是主机名，`QHostInfo`会搜索该IP的域名（即`QHostInfo`会进行反向查找）。成功后，得到的`QHostInfo`会同时包含解析后的域名和主机名的IP地址。示例：
注意：如果你用 lookupHost() 启动多个请求，信号的发出顺序无法保证。
注意：在 6.7 之前的 Qt 版本中，该函数将 `receiver` 取为（非const）`QObject*`。

**官方示例：**

```cpp
 QHostInfo::lookupHost("www.kde.org", this, &MyWidget::lookedUp);
```

### `[static] template <typename Functor> int QHostInfo::lookupHost(const QString &name, Functor &&functor)`

**作用与语义：**

查找与主机名`name`关联的IP地址，并返回查找的ID。查找结果准备好后，调用`functor`并引用`QHostInfo`参数。随后可以检查`QHostInfo`对象以获取查找结果。
`functor`会在调用 lookupHost 的线程中运行;该线程必须有一个正在运行的 Qt 事件循环。
注意：如果你用 lookupHost() 启动多个请求，信号的发出顺序无法保证。

### `[static] template <typename Functor> int QHostInfo::lookupHost(const QString &name, const QObject *context, Functor functor)`

**作用与语义：**

查找与主机名 `name` 关联的 IP 地址，并返回查找的 ID。查找结果准备好后，调用`functor`并`QHostInfo`参数。然后可以检查`QHostInfo`对象以获取查找结果。
如果`context`在查找完成前被销毁，`functor`将不会被调用。`functor`会在`context`的线程中运行。上下文线程必须有运行中的Qt事件循环。
以下是函数的另一种签名：
在这种情况下，当查找结果准备好时，`receiver`中的槽函数或信号`function`会被调用并`QHostInfo`参数。然后可以检查`QHostInfo`对象以获得查找结果。
注意：如果你用 lookupHost() 启动多个请求，信号的发出顺序无法保证。

**官方示例：**

```cpp
 lookupHost(const QString &name, const QObject *receiver, PointerToMemberFunction function)
```

### `int QHostInfo::lookupId() const`

**作用与语义：**

返回该查询的ID。

### `void QHostInfo::setAddresses(const QList<QHostAddress> &addresses)`

**作用与语义：**

将该`QHostInfo`中的地址列表设置为`addresses`。

### `void QHostInfo::setError(QHostInfo::HostInfoError error)`

**作用与语义：**

将该`QHostInfo`的错误类型设置为`error`。

### `void QHostInfo::setErrorString(const QString &str)`

**作用与语义：**

设置对错误的人类可读描述，作为查找失败时`str`。

### `void QHostInfo::setHostName(const QString &hostName)`

**作用与语义：**

将该`QHostInfo`的主机名设置为`hostName`。

### `void QHostInfo::setLookupId(int id)`

**作用与语义：**

将这次查询的ID设置为`id`。

### `[noexcept] void QHostInfo::swap(QHostInfo &other)`

**作用与语义：**

将这些主机信息与`other`交换。这个操作非常快，从未出错。

### `[noexcept] QHostInfo &QHostInfo::operator=(QHostInfo &&other)`

**作用与语义：**

移动分配`other`到该`QHostInfo`实例。
注意：移除对象`other`处于部分成形状态，唯一有效的操作是销毁和赋予新值。

### `QHostInfo &QHostInfo::operator=(const QHostInfo &other)`

**作用与语义：**

将`other`对象的数据分配给该主机信息对象，并返回对其的引用。

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

`QHostInfo` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
