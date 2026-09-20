# QNetworkProxy：一项网络代理配置

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QNetworkProxy>`  
> CMake：`Qt6::Network`  
> 类型：可重入、隐式共享值类型

## 它解决什么问题

`QNetworkProxy` 描述“通过哪个代理、以什么方式连接网络”：代理类型、主机、端口、用户名密码、能力声明以及 HTTP 代理专用的头。

它是配置值，不会自行建立连接。`QAbstractSocket`、`QTcpServer`、`QUdpSocket`、`QTcpSocket` 和 `QNetworkAccessManager` 才会在创建或发送连接时使用它。

## 实际使用场景

- 为一个 `QNetworkAccessManager` 的未来 HTTP 请求设置明确的 SOCKS5 或 HTTP 代理。
- 为应用全部默认 socket 设置静态代理。
- 对某个 socket 明确设为 `NoProxy`，绕开全局默认代理。
- 给 HTTP 代理添加代理端需要的自定义请求头。

如果代理选择要随目标域名、协议或连接类型变化，应使用 `QNetworkProxyFactory`；`QNetworkProxy` 适合“已经选定的一条代理”。

## 典型配置

建议将代理配置在发起请求或连接之前：

```cpp
#include <QNetworkAccessManager>
#include <QNetworkProxy>

QNetworkProxy proxy(QNetworkProxy::Socks5Proxy,
                    QStringLiteral("proxy.example.com"),
                    1080);
proxy.setUser(QStringLiteral("alice"));
proxy.setPassword(QStringLiteral("secret"));

QNetworkAccessManager manager;
manager.setProxy(proxy); // 仅影响此后由 manager 发出的请求
```

代理用户名和密码是敏感数据。避免写入日志、设置到可随意导出的配置中，且不要依靠 `QNetworkProxy` 作为凭据的安全存储。

## 关键语义与边界

### 代理类型决定适用范围，能力决定实际可做什么

| 类型 | 主要用途 |
| --- | --- |
| `DefaultProxy` | 交给应用级代理、应用级 factory 或系统代理选择。默认构造即为此类型。 |
| `NoProxy` | 禁用代理。 |
| `Socks5Proxy` | 通用 SOCKS5，支持 TCP、UDP、监听和用户名/密码认证；是否远端 DNS 解析由 `HostNameLookupCapability` 控制。 |
| `HttpProxy` | 通过 HTTP `CONNECT` 的出站 TCP 隧道代理，支持认证。 |
| `HttpCachingProxy` | 仅用于 HTTP 请求的缓存型代理，适合 `QNetworkAccessManager`。 |
| `FtpCachingProxy` | 仅用于 FTP 请求的缓存型代理。 |

`Capabilities` 是可按位组合的声明。`isTransparentProxy()` 实际检查 `TunnelingCapability`，`isCachingProxy()` 实际检查 `CachingCapability`，并不只是检查 type。显式调用过 `setCapabilities()` 后，再 `setType()` 不会自动重置已经手动设置的能力集合。

不要把不含 `TunnelingCapability` 的代理设置成应用默认代理，否则 `QTcpSocket` 无法按默认方式打开连接。

### 全局、对象级和 factory 选择有优先关系

`setApplicationProxy()` 配置应用级静态默认代理。它会覆盖应用级 `QNetworkProxyFactory`，并关闭系统代理使用；反过来，设置应用级 factory 也会覆盖先前的应用级静态代理。两者不要在不同模块里各自“偷偷设置”，否则最后执行者决定整个进程的网络路径。

对于 `QNetworkAccessManager`，优先在实例上使用 `setProxy()` 或 `setProxyFactory()`，把影响范围收敛到该 manager。设置静态或实例代理只影响未来连接/未来请求；已发送请求、已连接 socket 不会因修改配置而改变，想切换已连接 socket 必须重连。

对等地址等价于 `QHostAddress::LocalHost` 或 `LocalHostIPv6` 时，`connectToHost()`、`bind()`、`listen()` 不使用网络代理。

### SOCKS5 的 DNS 与 UDP 边界

SOCKS5 开启 `HostNameLookupCapability` 时，域名交给 SOCKS server 解析；关闭时，应用先本地解析再将 IP 发给代理。这会影响 DNS 隐私、内网名称可见性和失败位置，不能把两个模式混为一谈。

代理 UDP 经过两条 UDP 连接，丢包概率更高。若对 `QUdpSocket::bind()` 指定非 0 端口，SOCKS5 不能保证最终实际端口相同，应在成功后读取 `localPort()` / `localAddress()`。同样，SOCKS5 下 `QTcpServer::listen()` 可能超时，非 0 指定端口也不能保证实际端口相同。

### HTTP 代理头只对 HTTP 类型有效

`headers()`、`setHeaders()`、`header()`、`setHeader()`、`rawHeader()`、`setRawHeader()` 等只适用于 `HttpProxy` 或 `HttpCachingProxy`。其他代理类型读取时得到空结果，设置时没有效果。

`setHeader()` 会覆盖之前的同类设置，同时写入等价 raw header；`setRawHeader()` 若匹配已知头也会解析并更新“cooked”值。重复设置同名 raw header 会覆盖旧值。API 文档建议要表达可逗号合并的多值 HTTP 头时使用一个逗号分隔值；对于语义上不可合并的头，不能用这种方式硬拼。

## 常见误区

- **修改代理后期待已连接 socket 自动切换**：不会，必须重连。
- **把 HTTP caching proxy 用作任意 TCP 代理**：它只适用于 HTTP 请求。
- **把 `DefaultProxy` 当作“永远直接连接”**：它会继续向更高层全局/系统配置回退。
- **认为 SOCKS5 一定远端解析 DNS**：取决于 `HostNameLookupCapability`。
- **在 SOCKS5 监听时信任所请求的固定端口**：实际端口可能不同，应读取实际值。

## API 速查表

| 类别 | API | 语义与注意点 |
| --- | --- | --- |
| 类型 | `ProxyType` | 代理协议/用途类别，决定默认能力与适用的 Qt 网络类。 |
| 类型 | `DefaultProxy` / `NoProxy` | 使用上层默认选择 / 显式禁用代理。 |
| 类型 | `Socks5Proxy` | 通用 SOCKS5；支持 TCP、UDP、监听和用户名密码认证。 |
| 类型 | `HttpProxy` | HTTP CONNECT 出站 TCP 代理。 |
| 类型 | `HttpCachingProxy` / `FtpCachingProxy` | 分别仅用于 HTTP / FTP 请求的缓存代理。 |
| 能力 | `TunnelingCapability` | 能建立透明 TCP 隧道。 |
| 能力 | `ListeningCapability` | 能创建监听 TCP socket。 |
| 能力 | `UdpTunnelingCapability` | 能中继 UDP 数据报。 |
| 能力 | `CachingCapability` | 能缓存传输内容。 |
| 能力 | `HostNameLookupCapability` | 能在代理侧解析目标主机名。 |
| 能力 | `SctpTunnelingCapability` / `SctpListeningCapability` | SCTP 隧道 / SCTP 监听能力。 |
| 构造 | `QNetworkProxy()` | 创建 `DefaultProxy` 配置。 |
| 构造 | `QNetworkProxy(type, host, port, user, password)` | 以类型、端点和凭据构造，并按 type 设置默认能力。 |
| 值语义 | 拷贝构造、拷贝/移动赋值、`swap(other)` | 隐式共享值操作；没有 I/O。 |
| 比较 | `operator==(other)` / `operator!=(other)` | 比较代理配置值。 |
| 类型配置 | `setType(type)` / `type()` | 设置/读取代理类型；不会改写已显式设置的 capabilities。 |
| 能力配置 | `setCapabilities(flags)` / `capabilities()` | 设置/读取能力位，需与实际代理服务能力一致。 |
| 能力查询 | `isCachingProxy()` / `isTransparentProxy()` | 分别检查 caching / tunneling 能力。 |
| 端点 | `setHostName()` / `hostName()` | 设置/读取代理主机名。 |
| 端点 | `setPort()` / `port()` | 设置/读取代理端口。 |
| 凭据 | `setUser()` / `user()` | 设置/读取代理用户名。 |
| 凭据 | `setPassword()` / `password()` | 设置/读取代理密码；避免日志输出。 |
| HTTP 头 | `headers()` / `setHeaders(const QHttpHeaders &)` / `setHeaders(QHttpHeaders &&)` | Qt 6.8 起读写结构化代理头；非 HTTP 代理类型无效。 |
| HTTP 头 | `header(known)` / `setHeader(known, value)` | 读写已知 HTTP 头；设置会同步等价 raw header。 |
| HTTP 头 | `hasRawHeader()` / `rawHeader()` / `rawHeaderList()` / `setRawHeader()` | 管理 raw 代理头；同名重复设置覆盖，非 HTTP 类型读取为空/设置无效。 |
| 全局配置 | `applicationProxy()` | 读取当前应用级默认代理。 |
| 全局配置 | `setApplicationProxy(proxy)` | 设置应用级静态代理；覆盖应用 factory 并禁用系统代理选择。 |
| 调试 | `operator<<(QDebug, proxy)` | 非禁用 debug stream 构建可输出代理；注意不要泄露 password。 |

## 相关类型

- `QNetworkProxyQuery`：描述一次连接或 URL 请求，供代理 factory 决策。
- `QNetworkProxyFactory`：按 query 返回优先级代理列表。
- `QNetworkAccessManager`：可为某个 manager 设置 proxy 或 proxy factory。
- `QAuthenticator`：处理代理认证挑战时填写凭据。
