# QDnsLookup：异步 DNS 记录查询

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDnsLookup>`  
> CMake：`find_package(Qt6 REQUIRED COMPONENTS Network)`，并链接 `Qt6::Network`  
> 继承：`QObject`

## 它解决什么问题

`QDnsLookup` 用于显式查询 DNS 资源记录，而不是只把主机名解析成 IP 地址。它可以请求 A、AAAA、CNAME、MX、NS、PTR、SRV、TXT 和 TLSA 记录，并以异步方式把结果交回事件循环。

这解决了 `QHostInfo::lookupHost()` 不适合的问题：后者只面向常规主机地址解析；当客户端需要根据 SRV 发现服务端口、根据 MX 选择邮件交换服务器、读取 TXT 配置，或取得 TLSA 记录来实现 DANE 逻辑时，应使用 `QDnsLookup`。

## 实际使用场景

- XMPP、SIP、LDAP 等客户端查询 SRV 记录，得到服务目标、端口和优先级。
- 邮件投递程序查询 MX 记录，并按 `preference()` 从小到大尝试服务器。
- 域名验证、服务发现或自定义配置读取 TXT 记录。TXT 记录中的每个值是原始字节片段，不应假定它一定是 UTF-8 文本。
- 诊断工具指定 DNS 服务器，分别查询 A、AAAA、CNAME、PTR 或 NS。
- 支持 DNS-over-TLS（DoT）的平台上，经可信 DNS 服务器查询 TLSA，并在应用自身实现的 DANE 验证流程中使用结果。

## 基本工作流

`QDnsLookup` 是异步对象。先设置查询名与记录类型，连接 `finished()`，再调用 `lookup()`；只有在完成信号到达后，才根据 `error()` 读取对应的结果列表。

```cpp
#include <QDnsLookup>
#include <QDebug>

auto *lookup = new QDnsLookup(QDnsLookup::SRV,
                              u"_xmpp-client._tcp.example.com"_qs,
                              this);

connect(lookup, &QDnsLookup::finished, this, [lookup] {
    if (lookup->error() != QDnsLookup::NoError) {
        qWarning() << lookup->errorString();
        return;
    }

    for (const QDnsServiceRecord &record : lookup->serviceRecords()) {
        qDebug() << record.priority()
                 << record.weight()
                 << record.target()
                 << record.port();
    }
});

lookup->lookup();
```

查询类型决定应读取哪个 getter：

| 请求的 `Type` | 主要读取的结果 |
| --- | --- |
| `A`、`AAAA` | `hostAddressRecords()` |
| `CNAME` | `canonicalNameRecords()` |
| `NS` | `nameServerRecords()` |
| `PTR` | `pointerRecords()` |
| `MX` | `mailExchangeRecords()` |
| `SRV` | `serviceRecords()` |
| `TXT` | `textRecords()` |
| `TLSA` | `tlsAssociationRecords()` |

不能把“列表为空”一律解释为查询失败：应先检查 `error()`。`NoError` 加空列表可以是有效的“没有该类记录”结果。

## 选择解析器与协议

默认构造或只传 `type`、`name` 的构造函数使用系统 DNS 配置。需要指定服务器时，使用带 `QHostAddress` 的构造函数，或调用 `setNameserver()`。

`Protocol::Standard` 是普通 DNS：优先 UDP，必要时回退 TCP，默认端口为 53。`Protocol::DnsOverTls` 是基于 TCP/TLS 的 DoT，默认端口为 853。使用 DoT 前必须检查运行时能力：

```cpp
if (QDnsLookup::isProtocolSupported(QDnsLookup::DnsOverTls)) {
    lookup->setNameserver(QDnsLookup::DnsOverTls,
                          QHostAddress(u"192.0.2.53"_qs));
}
```

`isProtocolSupported()` 只表示当前 Qt/平台是否支持该协议，不表示目标服务器可达、端口已开放或 TLS 握手一定成功。`defaultPortForProtocol()` 用于取得协议的标准端口；若传 `0` 给支持端口参数的构造函数或 `setNameserver()`，则采用相应协议的默认端口。

对 `Standard` 使用非 53 端口存在平台限制：Windows 上 `QDnsLookup` 所使用的系统 API 无法处理替代端口；其他系统也可能被防火墙或解析器策略拦截。因此不能把“能设置 port”理解为“跨平台可用”。

## DoT、DNSSEC 与 TLSA 的边界

DoT 保护的是应用到所选 DNS 服务器之间的传输，不自动证明每条 DNS 记录的 DNSSEC 完整性。Qt 的 DoT 实现采用 opportunistic privacy profile：会验证所连接服务器呈现的证书对该连接有效；可用 `setSslConfiguration()` 施加更多 TLS 限制，并在完成后用 `sslConfiguration()` 读取实际配置。

`isAuthenticData()` 表示解析器报告返回数据已通过认证。`QDnsLookup` 本身不验证 DNS 数据完整性，因此应用只能在自己已通过其他方式确认 DNS 服务器可信时信任这个标志。

尤其是 TLSA：若 `isAuthenticData()` 为 `false`，标准要求忽略 `tlsAssociationRecords()`，不能拿它验证服务器身份。即使为 `true`，Qt 也只负责交付 `QDnsTlsAssociationRecord`；将其与证书、SPKI、`usage()`、`selector()`、`matchType()` 比较的 DANE 验证逻辑仍由应用负责。

## 生命周期、取消与线程边界

- `lookup()` 依赖对象所属线程的事件循环来投递 `finished()`；不要在 UI 线程里同步等待它完成。
- `abort()` 会取消尚未结束的请求；请求已经结束时没有效果。取消后将以 `OperationCancelledError` 结束，因此仍要在 `finished()` 中按错误处理。
- 在查询未完成时销毁 `QDnsLookup` 是安全的，只是不会再收到结果。若由 lambda 使用指针，连接应有合适的 context，或让对象拥有明确的父对象。
- 查询参数和结果属于该 `QObject` 的状态。跨线程协作时，把对象创建并使用在同一线程；需要通知其他线程时使用 queued signal/slot，而不是从另一线程直接改 `name`、`type` 或读取结果。
- 每次重新调用 `lookup()` 前，先把要复用的配置和上一轮结果的消费关系理清；业务代码应把完成时读取的记录当作该次应答的快照，不要让旧结果参与下一次请求决策。

## 关键 API 语义

### 错误与完成状态

`finished()` 同时是 `error`、`errorString` 和 `authenticData` 的通知信号。完成后先判断 `error()`：

- `NoError`：可读取结果列表。
- `OperationCancelledError`：由 `abort()` 取消。
- `InvalidRequestError`：名称、类型或配置无法形成有效请求。
- `NotFoundError`：服务器返回名称或记录不存在。
- `ServerFailureError`、`ServerRefusedError`：服务端明确失败或拒绝。
- `ResolverError`、`InvalidReplyError`、`TimeoutError`：分别对应系统解析器初始化、应答格式或超时问题。

`errorString()` 适合日志和用户可见诊断，程序分支应以 `error()` 枚举为准。

### 记录类型

`ANY` 是 DNS 类型值 255，但不能期待它返回“域名的全部记录”：现代递归解析器、权威服务器和网络策略经常限制或拒绝 ANY 查询。需要哪些记录，就逐类请求。

PTR 查询通常应传入正确的反向 DNS 名称，例如 IPv4 的 `in-addr.arpa` 名称；`QDnsLookup` 不会把普通 IP 字符串自动改写为反向查询名。

SRV 的 `priority()` 数字越小越先选；只在同一优先级中，才按 `weight()` 做加权选择。不要简单按权重降序排序，它不是“数值越大必然优先”的排序键。

### 属性绑定

`name`、`type`、`nameserver`、`nameserverPort` 和 `nameserverProtocol` 有 `bindable...()` 访问器，可接入 Qt 绑定系统。绑定只负责配置属性同步，不替代一次查询的完成、取消和错误处理；发起请求仍要调用 `lookup()`。

## API 速查表

| 类别 | API | 语义与使用重点 |
| --- | --- | --- |
| 枚举 | `Error` | 查询结果状态。完成后先判断它，再读记录；`errorString()` 只用于可读诊断。 |
| 枚举 | `Type` | 请求类型：`A`、`AAAA`、`ANY`、`CNAME`、`MX`、`NS`、`PTR`、`SRV`、`TLSA`、`TXT`；按类型读取对应记录列表。 |
| 枚举 | `Protocol` | `Standard` 为普通 DNS（默认 53）；`DnsOverTls` 为 DoT（默认 853，Qt 6.8 起）。 |
| 构造 | `QDnsLookup(QObject *parent = nullptr)` | 空配置构造；设置 `name`、`type` 等后再调用 `lookup()`。 |
| 构造 | `QDnsLookup(Type type, const QString &name, QObject *parent = nullptr)` | 使用系统 DNS 配置查询指定记录。 |
| 构造 | `QDnsLookup(Type type, const QString &name, const QHostAddress &nameserver, QObject *parent = nullptr)` | 指定普通 DNS 服务器，端口使用默认值。 |
| 构造 | `QDnsLookup(Type type, const QString &name, const QHostAddress &nameserver, quint16 port, QObject *parent = nullptr)` | Qt 6.6 起；指定普通 DNS 服务器及端口。非 53 端口在 Windows 上不可用，其他平台也可能受网络策略影响。 |
| 构造 | `QDnsLookup(Type type, const QString &name, Protocol protocol, const QHostAddress &nameserver, quint16 port = 0, QObject *parent = nullptr)` | Qt 6.8 起；指定协议、服务器与端口。先用 `isProtocolSupported()` 检查 DoT。 |
| 生命周期 | `~QDnsLookup()` | 未完成时销毁是安全的，但结果和 `finished()` 不会再到达。 |
| 状态 | `error()` | 返回 `Error`；完成后的首要判定依据。 |
| 状态 | `errorString()` | 返回错误的可读文本；不应用作机器分支条件。 |
| 状态 | `isFinished()` | 请求完成或已取消时为 `true`。 |
| 状态 | `isAuthenticData()` | Qt 6.8 起；解析器报告数据经认证时为真。Qt 不自行验证 DNSSEC，只信任已确认可信的解析器报告。 |
| 配置 | `name()` / `setName()` / `bindableName()` | 查询 DNS 名称；改变配置后需自行调用 `lookup()`。 |
| 配置 | `type()` / `setType()` / `bindableType()` | 查询记录类型；不要把 `ANY` 当作可靠的全记录查询。 |
| 配置 | `nameserver()` / `setNameserver(const QHostAddress &)` / `bindableNameserver()` | 获取、指定普通 DNS 服务器或恢复为地址配置；协议和端口应与之一起考虑。 |
| 配置 | `nameserverPort()` / `setNameserverPort(quint16)` / `bindableNameserverPort()` | Qt 6.6 起；端口配置。普通 DNS 的替代端口跨平台不可靠。 |
| 配置 | `nameserverProtocol()` / `setNameserverProtocol(Protocol)` / `bindableNameserverProtocol()` | Qt 6.8 起；选择普通 DNS 或 DoT。选择 DoT 后仍需检查平台支持和服务器可达性。 |
| 配置 | `setNameserver(Protocol, const QHostAddress &, quint16 port = 0)` | Qt 6.8 起；一次设置协议、服务器、端口。`0` 使用协议默认端口。 |
| 配置 | `setNameserver(const QHostAddress &, quint16 port)` | Qt 6.6 起；等价于设置 `Standard` 协议、服务器和端口。 |
| TLS 配置 | `setSslConfiguration(const QSslConfiguration &)` | 有 SSL 支持时可用，Qt 6.8 起；为 DoT 施加额外 TLS 限制。 |
| TLS 配置 | `sslConfiguration()` | 有 SSL 支持时可用；查询完成后可取得 TLS 配置相关信息。 |
| 结果 | `hostAddressRecords()` | A/AAAA 的 `QDnsHostAddressRecord` 列表。 |
| 结果 | `canonicalNameRecords()` | CNAME 的 `QDnsDomainNameRecord` 列表。 |
| 结果 | `nameServerRecords()` | NS 的 `QDnsDomainNameRecord` 列表。 |
| 结果 | `pointerRecords()` | PTR 的 `QDnsDomainNameRecord` 列表。 |
| 结果 | `mailExchangeRecords()` | MX 的 `QDnsMailExchangeRecord` 列表；按 `preference()` 小者优先。 |
| 结果 | `serviceRecords()` | SRV 的 `QDnsServiceRecord` 列表；先比较 `priority()`，再在同优先级内按 `weight()` 选择。 |
| 结果 | `textRecords()` | TXT 的 `QDnsTextRecord` 列表；值是字节片段，编码和拼接规则取决于上层协议。 |
| 结果 | `tlsAssociationRecords()` | Qt 6.8 起；TLSA 列表。`isAuthenticData()` 不为真时不得用于 DANE 身份验证。 |
| 槽 | `lookup()` | 异步发起查询；结束时发射 `finished()`。 |
| 槽 | `abort()` | 取消未完成查询；完成的查询不受影响。 |
| 信号 | `finished()` | 查询处理结束；读取错误、认证状态和结果的时机。 |
| 信号 | `nameChanged(const QString &)` | `name` 改变时发射。 |
| 信号 | `typeChanged(Type)` | `type` 改变时发射。 |
| 信号 | `nameserverChanged(const QHostAddress &)` | DNS 服务器地址改变时发射。 |
| 信号 | `nameserverPortChanged(quint16)` | Qt 6.6 起；DNS 服务器端口改变时发射。 |
| 信号 | `nameserverProtocolChanged(Protocol)` | Qt 6.8 起；DNS 协议改变时发射。 |
| 静态函数 | `isProtocolSupported(Protocol)` | Qt 6.8 起；检查当前平台/构建是否支持协议，不检查目标服务器可用性。 |
| 静态函数 | `defaultPortForProtocol(Protocol)` | Qt 6.8 起；返回协议标准端口，普通 DNS 为 53，DoT 为 853。 |

## 一句话总结

`QDnsLookup` 是面向具体 DNS 记录的异步查询器：在 `finished()` 后按 `error()` 消费结果，明确区分 DNS 传输加密、解析器认证报告与应用自身的 DNSSEC/DANE 信任决策。
