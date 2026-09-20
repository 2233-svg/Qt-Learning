# QNetworkProxyQuery：描述一次代理选择请求

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QNetworkProxyQuery>`  
> CMake：`Qt6::Network`  
> 类型：隐式共享值类型

## 它解决什么问题

`QNetworkProxyQuery` 不是代理配置，而是一份“该为这次网络操作选择什么代理”的上下文。它把连接类型、目标主机和端口、本地端口偏好、协议标签及 URL 提供给 `QNetworkProxyFactory`。

因此它解决的是细粒度路由：例如 HTTP 请求选择 HTTP 缓存代理、数据库或自定义 TCP 协议选择 SOCKS5、内网域名直接连接。

## 实际使用场景

- 在自定义 `QNetworkProxyFactory::queryProxy()` 中按 URL scheme、目标 host 或 port 决定代理。
- 直接调用 `QNetworkProxyFactory::systemProxyForQuery()` 查询某个目的地的系统代理。
- 测试代理策略是否正确区分 HTTPS、内部域名和普通 TCP socket。

普通应用很少手动构造 query 后直接连接；Qt 网络类会为它们生成合适 query。手动构造主要用于 factory 实现和诊断。

## 选择条件与查询类型

一个 query 可包含以下线索：

- `queryType`：操作是出站 TCP、UDP、SCTP、监听 server，还是高层 URL 请求；
- `peerHostName` / `peerPort`：出站目标，或部分监听/UDP 情况下期望的远端；
- `localPort`：本地绑定端口偏好；
- `protocolTag`：任意协议字符串，例如 `http`、`https`、`xmpp`；
- `url`：高层 URL 请求的完整 URL。

默认构造的类型是 `TcpSocket`。缺失信息是合法的：未知 hostname/protocol 用空 `QString`，未知或不适用端口用 `-1`。factory 必须为这些不完整 query 做合理回退，不能假定每一项都存在。

## 创建 URL query

对 HTTP 等 URL 请求，使用 URL 构造函数或 `setUrl()`：

```cpp
#include <QNetworkProxyFactory>
#include <QNetworkProxyQuery>
#include <QUrl>

const QUrl url(QStringLiteral("https://api.example.com:8443/v1/items"));
QNetworkProxyQuery query(url); // 默认 UrlRequest

const QList<QNetworkProxy> candidates =
    QNetworkProxyFactory::systemProxyForQuery(query);
```

`setUrl()` 同时设置 URL、protocol tag、peer host 和 peer port，便于 factory 只读取一致的字段。对 `UrlRequest`，`protocolTag()` 返回 scheme，`peerHostName()` / `peerPort()` 对应 URL host/port；框架通常会补上协议默认端口。

## 端口值与边界

- `setLocalPort(port)` 接受 `0..65535`，其中 `0` 表示任意本地端口；`-1` 表示未知或不适用。
- `setPeerPort(port)` 接受 `1..65535`；`-1` 表示未知。
- bind-port 构造函数参数是 `quint16`，表示确切请求值，不能用 `-1` 表示未知。

`TcpServer` 与 `SctpServer` 通常主要关心本地端口；`TcpSocket` / `SctpSocket` 主要关心 peer host 和 peer port；`UdpSocket` 两组字段都可能有意义；`UrlRequest` 则应优先使用 URL 信息。

## 自定义 factory 中的使用原则

factory 不应在 `queryProxy()` 内再发网络请求、同步读远端配置或阻塞等待 PAC 下载。代理查询通常发生在连接建立路径，缓慢或重入的实现会拖慢所有请求。将策略预加载到内存，把 query 当作纯输入，快速返回按优先级排序的候选列表。

不要把 `protocolTag` 误解为可信安全断言。它是帮助选择代理的任意文本，若策略涉及安全边界，应同时检查 URL、host、端口及实际应用上下文。

## API 速查表

| 类别 | API | 语义与注意点 |
| --- | --- | --- |
| 枚举 | `TcpSocket` | 普通出站 TCP；主要使用 peer host/port。 |
| 枚举 | `UdpSocket` | UDP 数据报；本地端口和远端信息都可能有用。 |
| 枚举 | `SctpSocket` | 出站 SCTP 连接。 |
| 枚举 | `TcpServer` | 被动 TCP 监听；通常主要使用 local port。 |
| 枚举 | `UrlRequest` | 高层 URL 请求；URL、scheme、host、port 可用。 |
| 枚举 | `SctpServer` | 被动 SCTP 监听；通常主要使用 local port。 |
| 构造 | `QNetworkProxyQuery()` | 默认 `TcpSocket` query，其余条件未知。 |
| 构造 | `QNetworkProxyQuery(url, type)` | 设置 URL query；默认类型为 `UrlRequest`。 |
| 构造 | `QNetworkProxyQuery(bindPort, protocolTag, type)` | 设置明确本地端口，默认类型 `TcpServer`；参数不支持未知端口。 |
| 构造 | `QNetworkProxyQuery(host, port, protocolTag, type)` | 设置出站目标，默认类型 `TcpSocket`。 |
| 值语义 | 拷贝构造、拷贝/移动赋值、`swap(other)` | 隐式共享值操作，适合按值传入 factory。 |
| 比较 | `operator==(other)` / `operator!=(other)` | 比较 query 描述的所有值。 |
| 类型 | `queryType()` / `setQueryType(type)` | 读取/设置操作种类，决定各字段的解释。 |
| 目标 | `peerHostName()` / `setPeerHostName(host)` | 读取/设置目标或预期来源主机；空字符串表示未知。 |
| 目标 | `peerPort()` / `setPeerPort(port)` | 读取/设置目标端口；`1..65535` 有效，`-1` 未知。 |
| 本地 | `localPort()` / `setLocalPort(port)` | 读取/设置本地绑定端口；`0` 允许任意端口，`-1` 未知/不适用。 |
| 协议 | `protocolTag()` / `setProtocolTag(tag)` | 读取/设置任意协议标签；对 `UrlRequest` 通常为 URL scheme。 |
| URL | `url()` / `setUrl(url)` | 读取/设置 URL；设置时同步 protocol tag、peer host、peer port。 |
| 调试 | `operator<<(QDebug, query)` | 非禁用 debug stream 构建下输出 query。 |

## 相关类型

- `QNetworkProxyFactory`：消费 query 并返回候选代理。
- `QNetworkProxy`：factory 返回的单条代理配置。
- `QNetworkAccessManager`：会为 URL 请求生成 `UrlRequest` query。
