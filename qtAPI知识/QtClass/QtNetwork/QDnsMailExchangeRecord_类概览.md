# QDnsMailExchangeRecord：表示 DNS MX 邮件交换记录

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDnsMailExchangeRecord>`  
> 所属模块：`Qt6::Network`  
> 类型性质：隐式共享值类型，由 `QDnsLookup` 返回

## 它解决什么问题

MX 记录把一个邮件域名映射到一个或多个负责接收邮件的主机，并为它们提供优先级。`QDnsMailExchangeRecord` 表示其中的一条结果：记录名称、交换主机、优先级和 TTL。

它是 DNS 结果快照，不会建立 SMTP 连接、解析交换主机地址、尝试备用服务器或验证 TLS 证书。邮件投递逻辑必须在读取记录后继续完成这些步骤。

## 实际使用场景

```cpp
QDnsLookup lookup(QDnsLookup::MX, u"example.test"_s);

connect(&lookup, &QDnsLookup::finished, this, [&lookup] {
    if (lookup.error() != QDnsLookup::NoError)
        return;

    auto records = lookup.mailExchangeRecords();
    std::sort(records.begin(), records.end(),
              [](const QDnsMailExchangeRecord &a,
                 const QDnsMailExchangeRecord &b) {
                  return a.preference() < b.preference();
              });

    for (const auto &record : records)
        qDebug() << record.preference() << record.exchange();
});

lookup.lookup();
```

典型用途是邮件诊断、域名配置检查或实现需要自行解析 MX 的协议组件。普通 SMTP 客户端不应仅凭查询成功就认为投递已成功。

## 优先级与目标主机

### `preference()`

MX preference 是排序字段，数值越小优先级越高。多个记录可能拥有同一个 preference；这时该值本身不提供进一步的负载分配规则。

应用不应把 preference 当成端口、重试次数或权重。若要按标准邮件投递流程尝试候选主机，应先处理更小的 preference，再按业务或协议规范处理同优先级记录。

### `exchange()`

返回邮件交换主机的 DNS 名称。它不是 IP 地址，也不带 SMTP 端口；通常还需要执行 A/AAAA 解析，并使用 SMTP 或 submission 规范决定端口、TLS 策略和失败回退。

### `name()` 与 `timeToLive()`

`name()` 是当前 MX 记录关联的所有者名称。`timeToLive()` 是秒单位的缓存有效期，不代表远端 SMTP 服务的会话超时或可用性。

## 生命周期和查询边界

记录由 `QDnsLookup::mailExchangeRecords()` 提供。默认构造会得到空值，公开 API 没有 setter，因此不能把它当作 MX 记录构建器。

对象隐式共享，按值保存通常成本较低。应在 `finished()` 后检查 `QDnsLookup::error()`，再读取列表；需要保留跨刷新周期的数据时复制记录，不要保留旧列表元素引用。

## 逐项 API 说明

### `QDnsMailExchangeRecord()`

创建空记录，适用于默认初始化或容器元素。有效字段通常来自 DNS 查询结果。

### `QDnsMailExchangeRecord(const QDnsMailExchangeRecord &other)`

复制记录并共享内部数据。复制不发起网络请求。

### `QString name() const`

返回记录所有者名称。它不一定与原始查询字符串逐字相同。

### `QString exchange() const`

返回 MX 目标主机名。需要另行解析为地址并尝试连接。

### `quint16 preference() const`

返回 MX 优先级，值越小越优先。相同优先级不表示其中一条天然更可靠。

### `quint32 timeToLive() const`

返回 TTL 秒数，用于 DNS 结果缓存到期计算。

### `void swap(QDnsMailExchangeRecord &other) noexcept`

交换两个本地记录对象。不会修改 DNS 服务端内容。

### 复制/移动 `operator=`

用另一个记录替换当前值。移动后不应再依赖源对象原有字段。

## 常见误区

- 认为 `exchange()` 已是可直接连接的 IP 地址。
- 将较大的 preference 误判为更高优先级。
- 把 TTL 当作 SMTP 连接或重试超时。
- 不解析 MX 目标的 A/AAAA 就尝试建立连接。
- 用空的默认构造记录代替查询结果。
- 忽略 `QDnsLookup` 失败后结果列表可能为空。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QDnsMailExchangeRecord()` | 创建空 MX 记录。 | 有效数据来自 `QDnsLookup`。 |
| 构造 | `QDnsMailExchangeRecord(const QDnsMailExchangeRecord &)` | 复制记录。 | 隐式共享，不发起查询。 |
| 字段 | `QString name() const` | 返回记录所有者名称。 | 可能不同于原始查询名称。 |
| 字段 | `QString exchange() const` | 返回邮件交换主机名。 | 仍需解析地址并连接。 |
| 排序 | `quint16 preference() const` | 返回 MX 优先级。 | 数值越小越优先。 |
| 缓存 | `quint32 timeToLive() const` | 返回 TTL 秒数。 | 不是 SMTP 超时。 |
| 工具 | `void swap(QDnsMailExchangeRecord &)` | 交换两个记录值。 | 不影响 DNS 服务端。 |
| 赋值 | 复制/移动 `operator=` | 替换当前记录。 | 移动后不依赖源内容。 |

### 一句话总结

`QDnsMailExchangeRecord` 告诉应用“哪个域名接收邮件、其优先级是多少”；真正的地址解析、SMTP 连接与投递回退仍在它之后。
