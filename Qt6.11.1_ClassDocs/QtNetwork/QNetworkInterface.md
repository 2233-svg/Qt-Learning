# QNetworkInterface

> Qt 6.11.1 · Qt Network

## 1. 先建立直觉

**一句话定位：** `QNetworkInterface` 是 Qt Network 的“网络Interface”类型，负责描述请求/地址/连接状态或承载异步网络数据。

**模块背景：** Qt Network 提供 TCP/UDP、HTTP、代理、DNS、SSL 和网络请求等异步网络能力。

### 这是什么

`QNetworkInterface` 是 Qt Network 中的抽象协议类型，通常通过具体子类、模型、插件或工厂来使用。

**内部模型：** 抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

**适用场景：** 当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。

**典型调用链：** 选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。

**先记住的坑：** 不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

## 2. 依赖与对象关系

- 头文件：`#include <QNetworkInterface>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Network)
target_link_libraries(mytarget PRIVATE Qt6::Network)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

### 状态、生命周期和线程

**生命周期：** manager 必须在线程事件循环中存活到 reply 完成；reply 完成后读取结果并调用 `deleteLater()`，不能在信号触发前直接释放。请求对象是值类型，reply 才是带有异步状态和资源的对象。

**状态与结果：** 请求成功发出不等于 HTTP 成功，HTTP 状态码成功也不等于业务 JSON 有效。至少分别处理网络错误、HTTP 状态码、响应头、响应体解析和业务字段校验。上传/下载还要处理进度、分段读取和取消。

**线程与事件循环：** QNetworkAccessManager、QNetworkReply 和相关请求应在同一个有事件循环的线程使用。跨线程时把网络对象整体放到目标线程，通过信号传递结果，不要跨线程直接读写 reply。

## 3. 直接使用

当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。 使用时通常按这个过程组织：选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。

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

- `enum InterfaceFlag { IsUp, IsRunning, CanBroadcast, IsLoopBack, IsPointToPoint, CanMulticast }`
- `flags InterfaceFlags`
- `enum InterfaceType { Unknown, Loopback, Virtual, Ethernet, Wifi, …, Ieee1394 }`

### 公有函数

- `QNetworkInterface()`
- `QNetworkInterface(const QNetworkInterface &other)`
- `~QNetworkInterface()`
- `QList<QNetworkAddressEntry> addressEntries() const`
- `QNetworkInterface::InterfaceFlags flags() const`
- `QString hardwareAddress() const`
- `QString humanReadableName() const`
- `int index() const`
- `bool isValid() const`
- `int maximumTransmissionUnit() const`
- `QString name() const`
- `void swap(QNetworkInterface &other)`
- `QNetworkInterface::InterfaceType type() const`
- `QNetworkInterface & operator=(const QNetworkInterface &other)`

### 静态公有成员

- `QList<QHostAddress> allAddresses()`
- `QList<QNetworkInterface> allInterfaces()`
- `QNetworkInterface interfaceFromIndex(int index)`
- `QNetworkInterface interfaceFromName(const QString &name)`
- `int interfaceIndexFromName(const QString &name)`
- `QString interfaceNameFromIndex(int index)`

### 相关非成员函数

- `QDebug operator<<(QDebug debug, const QNetworkInterface &networkInterface)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QNetworkInterface::InterfaceFlagflags QNetworkInterface::InterfaceFlags`

**作用与语义：**

指定与该网络接口关联的标志。可能的值为：
- `QNetworkInterface::IsUp`：`0x1`;网络接口“上线”——由管理员操作启用
- `QNetworkInterface::IsRunning`：`0x2`;网络接口处于操作状态：配置为“上行”，并（通常）物理连接到网络
- `QNetworkInterface::CanBroadcast`：`0x4`;网络接口以广播模式工作
- `QNetworkInterface::IsLoopBack`：`0x8`;网络接口是环回接口：即一个虚拟接口，其目的地是主机本身
- `QNetworkInterface::IsPointToPoint`：`0x10`;网络接口是点对点接口：即只有一个可直接访问的另一个地址。
- `QNetworkInterface::CanMulticast`：`0x20`;网络接口支持多播
注意，一个网络接口不能同时是基于广播和点对点的。
InterfaceFlags 类型是 QFlags 的 typedef<InterfaceFlag>。它存储 InterfaceFlag 值的 OR 组合。

### `enum QNetworkInterface::InterfaceType`

**作用与语义：**

指定该接口的硬件类型（PHY层，OSI层1，如果可以确定的话）。不在下文列出的接口类型通常会显示为未知，尽管Qt的未来版本可能会添加新的枚举值。
可能的数值如下：
- `QNetworkInterface::Unknown`：`0`;接口类型无法确定，或者不是其他列出的类型之一。
- `QNetworkInterface::Loopback`：`1`;虚拟环回接口，分配环回IP地址（127.0.0.1，：：1）。
- `QNetworkInterface::Virtual`：`2`;一种被确定为虚拟接口，但不包括其他可能类型的接口。例如，隧道接口（目前）被检测为虚拟接口。
- `QNetworkInterface::Ethernet`：`3`;IEEE 802.3 以太网接口，尽管在许多系统中，其他类型的 IEEE 802 接口也可能被检测为以太网（尤其是 Wi-Fi）。
- `QNetworkInterface::Wifi`：`8`;IEEE 802.11 Wi-Fi 接口。注意，在某些系统中，`QNetworkInterface`可能无法区分普通以太网和 Wi-Fi，因此不会返回该枚举值。
- `QNetworkInterface::Ieee80211`：`Wifi`;WiFi的别名。
- `QNetworkInterface::CanBus`：`5`;ISO 11898控制器区域网络总线接口，通常用于汽车系统。
- `QNetworkInterface::Fddi`：`7`;ANSI X3T12光纤分布式数据接口，基于光纤的局域网。
- `QNetworkInterface::Ppp`：`6`;点对点协议接口，通过较低的传输层（通常通过无线或物理线路串行）建立两个节点之间的直接连接。
- `QNetworkInterface::Slip`：`4`;串行线路互联网协议接口。
- `QNetworkInterface::Phonet`：`9`;使用 Linux Phonet 套接字系列的接口，用于与蜂巢调制解调器通信。更多信息请参见 Linux 内核文档。
- `QNetworkInterface::Ieee802154`：`10`;IEEE 802.15.4 个人区域网络接口（除6LoWPAN外）（见下文）。
- `QNetworkInterface::SixLoWPAN`：`11`;6LoWPAN（低功耗无线个人局网上的IPv6）接口，运行在IEEE 802.15.4 PHY上，但对IPv6和UDP有特定的头部压缩方案。这种接口常用于网状网络。
- `QNetworkInterface::Ieee80216`：`12`;IEEE 802.16无线都市区网，也被称为“WiMAX”商业名称。
- `QNetworkInterface::Ieee1394`：`13`;IEEE 1394接口（又称“FireWire”）。

### `QNetworkInterface::QNetworkInterface()`

**作用与语义：**

构建一个空的网络接口对象。

### `QNetworkInterface::QNetworkInterface(const QNetworkInterface &other)`

**作用与语义：**

创建包含在`other`中的QNetworkInterface对象的副本。

### `[noexcept] QNetworkInterface::~QNetworkInterface()`

**作用与语义：**

释放了与`QNetworkInterface`对象相关的资源。

### `QList<QNetworkAddressEntry> QNetworkInterface::addressEntries() const`

**作用与语义：**

返回该接口所拥有的IP地址列表及其相关的网掩码和广播地址。
如果不需要网掩码、广播地址或其他信息，你可以调用`allAddresses()`函数，只获取活动接口的IP地址。

### `[static] QList<QHostAddress> QNetworkInterface::allAddresses()`

**作用与语义：**

这个便利函数返回主机上找到的所有IP地址。它等价于对处于`QNetworkInterface::IsUp`状态的`allInterfaces()`返回的所有对象调用`addressEntries()`以获取`QNetworkAddressEntry`对象的列表，然后对这些对象中的每一个调用`QNetworkAddressEntry::ip()`。

### `[static] QList<QNetworkInterface> QNetworkInterface::allInterfaces()`

**作用与语义：**

返回主机上所有网络接口的列表。如果发生故障，则返回一个元素为零的列表。

### `QNetworkInterface::InterfaceFlags QNetworkInterface::flags() const`

**作用与语义：**

返回与该网络接口相关的标志。

### `QString QNetworkInterface::hardwareAddress() const`

**作用与语义：**

返回该接口的低级硬件地址。在以太网接口上，该地址以字符串表示，中间用冒号分隔。
其他接口类型可能拥有其他类型的硬件地址。实现不应依赖该函数返回有效的MAC地址。

### `QString QNetworkInterface::humanReadableName() const`

**作用与语义：**

如果能确定该名称，则返回该网络接口的人类可读名称，例如“局域连接”。如果无法确定，该功能返回与`name()`相同。人类可读名称是用户可在Windows控制面板中修改的名称，因此在程序执行过程中可能会发生变化。
在Unix上，这个函数目前总是返回与`name()`相同，因为Unix系统不存储人类可读名称的配置。

### `int QNetworkInterface::index() const`

**作用与语义：**

如果已知，返回接口系统索引。这是操作系统分配的一个整数，用于识别该接口，通常不会改变。它与IPv6地址中的作用域ID字段匹配。
如果索引未知，该函数返回0。

### `[static] QNetworkInterface QNetworkInterface::interfaceFromIndex(int index)`

**作用与语义：**

返回一个`QNetworkInterface`对象，代表内部ID为`index`的接口。网络接口有一个唯一的标识符，称为“接口索引”，以区别于系统中的其他接口。通常，这个值是逐步分配的，每次移除又添加的接口都会得到不同的值。
该索引也出现在IPv6地址的范围ID字段中。

### `[static] QNetworkInterface QNetworkInterface::interfaceFromName(const QString &name)`

**作用与语义：**

返回名为`name`的接口的`QNetworkInterface`对象。如果不存在这样的接口，该函数返回一个无效的`QNetworkInterface`对象。
字符串`name`可以是实际的接口名称（如“eth0”或“en1”）或字符串形式的接口索引（“1”、“2”等）。

### `[static] int QNetworkInterface::interfaceIndexFromName(const QString &name)`

**作用与语义：**

返回名称为`name`的接口索引，若无该名称接口则为0。该函数应产生与后续代码相同的结果，但执行速度可能更快。

**官方示例：**

```cpp
     QNetworkInterface::interfaceFromName(name).index()
```

### `[static] QString QNetworkInterface::interfaceNameFromIndex(int index)`

**作用与语义：**

返回索引为`index`的接口名称，若无该索引接口则返回空字符串。该函数应产生与后续代码相同的结果，但执行速度可能更快。

**官方示例：**

```cpp
     QNetworkInterface::interfaceFromIndex(index).name()
```

### `bool QNetworkInterface::isValid() const`

**作用与语义：**

如果该`QNetworkInterface`对象包含关于网络接口的有效信息，返回`true`。

### `int QNetworkInterface::maximumTransmissionUnit() const`

**作用与语义：**

如果已知，返回该接口的最大传输单元，否则返回0。
最大传输单元是指在该接口上可发送的最大数据包，且不会产生链路级碎片化。应用程序可以使用该值计算能够容纳未分片UDP数据报的有效载荷大小。在计算可传输的有效载荷大小时，记得减去接口通信中使用的头部大小，例如TCP（20字节）或UDP（12字节）、IPv4（20字节）或IPv6（40字节，若无某种头部压缩）。还要注意，沿完整路径到目的节点的MTU（路径MTU）可能小于接口的MTU。

### `QString QNetworkInterface::name() const`

**作用与语义：**

返回该网络接口的名称。在Unix系统中，这是一个包含接口类型和可选择序列号的字符串，如“eth0”、“lo”或“pcn0”。在Windows中，它是用户无法更改的内部ID。

### `[noexcept] void QNetworkInterface::swap(QNetworkInterface &other)`

**作用与语义：**

将该网络接口实例与`other`交换。该操作非常快且从未失败。

### `QNetworkInterface::InterfaceType QNetworkInterface::type() const`

**作用与语义：**

如果可以确定该接口，返回该接口的类型。如果无法确定，该函数返回`QNetworkInterface::Unknown`。

### `QNetworkInterface &QNetworkInterface::operator=(const QNetworkInterface &other)`

**作用与语义：**

将`other`中`QNetworkInterface`对象的内容复制到这个中。

### `QDebug operator<<(QDebug debug, const QNetworkInterface &networkInterface)`

**作用与语义：**

将`QNetworkInterface` `networkInterface`写入流，并返回`debug`流的引用。

### `enum InterfaceFlag { IsUp, IsRunning, CanBroadcast, IsLoopBack, IsPointToPoint, CanMulticast }`

**作用与语义：**

指定与该网络接口关联的标志。可能的值为：
- `QNetworkInterface::IsUp`：`0x1`;网络接口“上线”——由管理员操作启用
- `QNetworkInterface::IsRunning`：`0x2`;网络接口处于操作状态：配置为“上行”，并（通常）物理连接到网络
- `QNetworkInterface::CanBroadcast`：`0x4`;网络接口以广播模式工作
- `QNetworkInterface::IsLoopBack`：`0x8`;网络接口是环回接口：即一个虚拟接口，其目的地是主机本身
- `QNetworkInterface::IsPointToPoint`：`0x10`;网络接口是点对点接口：即只有一个可直接访问的另一个地址。
- `QNetworkInterface::CanMulticast`：`0x20`;网络接口支持多播
注意，一个网络接口不能同时是基于广播和点对点的。
InterfaceFlags 类型是 QFlags 的 typedef<InterfaceFlag>。它存储 InterfaceFlag 值的 OR 组合。

### `flags InterfaceFlags`

**作用与语义：**

指定与该网络接口关联的标志。可能的值为：
- `QNetworkInterface::IsUp`：`0x1`;网络接口“上线”——由管理员操作启用
- `QNetworkInterface::IsRunning`：`0x2`;网络接口处于操作状态：配置为“上行”，并（通常）物理连接到网络
- `QNetworkInterface::CanBroadcast`：`0x4`;网络接口以广播模式工作
- `QNetworkInterface::IsLoopBack`：`0x8`;网络接口是环回接口：即一个虚拟接口，其目的地是主机本身
- `QNetworkInterface::IsPointToPoint`：`0x10`;网络接口是点对点接口：即只有一个可直接访问的另一个地址。
- `QNetworkInterface::CanMulticast`：`0x20`;网络接口支持多播
注意，一个网络接口不能同时是基于广播和点对点的。
InterfaceFlags 类型是 QFlags 的 typedef<InterfaceFlag>。它存储 InterfaceFlag 值的 OR 组合。

## 6. 深入实践与常见坑

### 生命周期和资源边界

manager 必须在线程事件循环中存活到 reply 完成；reply 完成后读取结果并调用 `deleteLater()`，不能在信号触发前直接释放。请求对象是值类型，reply 才是带有异步状态和资源的对象。

### 状态和错误边界

请求成功发出不等于 HTTP 成功，HTTP 状态码成功也不等于业务 JSON 有效。至少分别处理网络错误、HTTP 状态码、响应头、响应体解析和业务字段校验。上传/下载还要处理进度、分段读取和取消。

### 线程边界

QNetworkAccessManager、QNetworkReply 和相关请求应在同一个有事件循环的线程使用。跨线程时把网络对象整体放到目标线程，通过信号传递结果，不要跨线程直接读写 reply。

### 最容易出现的错误

不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QNetworkInterface` 所属机制类型：异步网络机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
