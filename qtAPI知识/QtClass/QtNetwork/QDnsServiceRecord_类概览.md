# QDnsServiceRecord：表示 DNS SRV 服务发现记录

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDnsServiceRecord>`  
> 所属模块：`Qt6::Network`  
> 类型性质：隐式共享值类型，由 `QDnsLookup` 返回

## 它解决什么问题

SRV 记录为“某个服务在某个域中由谁提供、端口是多少、候选如何排序”提供 DNS 层描述。`QDnsServiceRecord` 保存一条 SRV 应答的名称、目标主机、端口、优先级、权重和 TTL。

它适合服务发现，而不是通用主机名解析。它不会自行连接目标、解析目标主机的地址、执行 TLS 协商或按权重选出最终服务器。

## 实际使用场景

```cpp
QDnsLookup lookup(QDnsLookup::SRV, u"_xmpp-client._tcp.example.test"_s);

connect(&lookup, &QDnsLookup::finished, this, [&lookup] {
    if (lookup.error() != QDnsLookup::NoError)
        return;

    for (const QDnsServiceRecord &record : lookup.serviceRecords()) {
        qDebug() << record.target()
                 << record.port()
                 << "priority:" << record.priority()
                 << "weight:" << record.weight();
    }
});

lookup.lookup();
```

常见于支持 SRV 的即时通信、目录服务、游戏服务或企业内部服务发现。查询名称通常包含服务标签和传输协议标签；应用应按所使用协议的规范构造该名称。

## 优先级、权重与目标选择

### `priority()`

SRV priority 用于候选分层：数值越小优先级越高。选择服务端时，应先只考虑最小 priority 的记录集合；较大 priority 常用于备用端点。

### `weight()`

weight 只在同一 priority 的候选之间参与相对选择。它不是百分比，也不应该跨不同 priority 直接比较。需要遵循 SRV 加权选择时，应用必须实现相应的随机选择逻辑；`QDnsServiceRecord` 只保存数据，不会替你调度。

### `target()` 与 `port()`

`target()` 是服务主机的 DNS 名称，`port()` 是该服务端点的网络端口。两者合起来仍不是可连接 socket：

1. 解析 `target()` 的地址；
2. 按协议连接 `port()`；
3. 独立处理连接、TLS 和认证。

### `name()` 与 `timeToLive()`

`name()` 是 SRV 记录所有者名称。`timeToLive()` 以秒为单位，控制 DNS 结果的缓存期限，不代表业务会话有效期。

## 生命周期与数据来源

`QDnsServiceRecord` 是隐式共享值类型，通常由 `QDnsLookup::serviceRecords()` 返回。默认构造对象为空，且没有公开 setter；应用应把它视为查询结果快照而不是可编辑服务注册表。

`QDnsLookup` 完成后先检查 `error()`。刷新查询会替换上一轮结果，异步保存候选时应复制值对象，而非持有列表元素引用。

## 逐项 API 说明

### `QDnsServiceRecord()`

创建空 SRV 记录。它没有可用端点含义，正常记录来自成功查询。

### `QDnsServiceRecord(const QDnsServiceRecord &other)`

复制记录并共享底层数据。复制不会进行 DNS 解析或网络探测。

### `QString name() const`

返回 SRV 记录所有者名称，通常是带服务和协议标签的查询名称。

### `QString target() const`

返回目标主机 DNS 名称。还需地址解析，不能当作 IP 或 URL。

### `quint16 port() const`

返回服务端口。端口 0 或异常结果应由协议层按业务规则处理，不能仅凭对象存在就发起连接。

### `quint16 priority() const`

返回候选优先级，数值越小越先尝试。

### `quint16 weight() const`

返回同优先级候选间的相对权重。不是线程调度权重，也不是全局负载百分比。

### `quint32 timeToLive() const`

返回 DNS TTL 秒数，用于缓存刷新时机。

### `void swap(QDnsServiceRecord &other) noexcept`

交换两个本地记录值，不会修改 DNS 数据。

### 复制/移动 `operator=`

替换当前记录内容。移动后源对象只保证可析构或重新赋值。

## 常见误区

- 把 `weight()` 当成跨所有候选的百分比。
- 忽略 priority，直接挑选 weight 最大的记录。
- 将 `target()` 当作已解析、可信且已连通的地址。
- 把 TTL 当作服务连接的保活周期。
- 不检查 `QDnsLookup::error()` 就用空的 `serviceRecords()`。
- 误以为该类会自动执行 SRV 加权调度。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QDnsServiceRecord()` | 创建空 SRV 记录。 | 有效数据来自成功查询。 |
| 构造 | `QDnsServiceRecord(const QDnsServiceRecord &)` | 复制记录。 | 隐式共享，不发起查询。 |
| 字段 | `QString name() const` | 返回记录所有者名称。 | 常带服务/协议标签。 |
| 端点 | `QString target() const` | 返回目标主机名。 | 仍需 A/AAAA 解析。 |
| 端点 | `quint16 port() const` | 返回服务端口。 | 不表示已经连接。 |
| 排序 | `quint16 priority() const` | 返回候选优先级。 | 数值越小越优先。 |
| 调度 | `quint16 weight() const` | 返回同优先级相对权重。 | 需应用实现加权选择。 |
| 缓存 | `quint32 timeToLive() const` | 返回 TTL 秒数。 | 不是会话保活时间。 |
| 工具 | `void swap(QDnsServiceRecord &)` | 交换本地记录值。 | 不影响 DNS 服务端。 |
| 赋值 | 复制/移动 `operator=` | 替换当前记录。 | 移动后不依赖源内容。 |

### 一句话总结

`QDnsServiceRecord` 描述一个服务发现候选端点；优先级负责分层，权重只用于同层选择，连接和故障转移仍由应用完成。
