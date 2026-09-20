# QDnsDomainNameRecord：表示 CNAME、NS 或 PTR 查询返回的域名记录

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDnsDomainNameRecord>`  
> 所属模块：`Qt6::Network`  
> 类型性质：隐式共享值类型，由 `QDnsLookup` 返回

## 它解决什么问题

DNS 中有一类记录的结果仍然是一个域名，而不是 IP 地址。例如：

- CNAME 把别名指向规范名称；
- NS 指向负责某个区域的名称服务器；
- PTR 把反向查询名称指向主机名。

`QDnsDomainNameRecord` 把这类查询结果封装为“记录所有者名称、目标域名、TTL”三个只读字段。它让调用方不必手工解析 DNS 报文，也避免把 DNS 名称错误地当成 `QHostAddress`。

它不是 DNS 查询器，也不是可编辑记录。要发起查询使用 `QDnsLookup`；要获取 A/AAAA 地址记录使用 `QDnsHostAddressRecord`。

## 实际使用场景

```cpp
QDnsLookup lookup(QDnsLookup::CNAME, u"www.example.test"_s);

connect(&lookup, &QDnsLookup::finished, this, [&lookup] {
    if (lookup.error() != QDnsLookup::NoError)
        return;

    for (const QDnsDomainNameRecord &record : lookup.canonicalNameRecords()) {
        qDebug() << record.name()
                 << "->" << record.value()
                 << "TTL:" << record.timeToLive();
    }
});

lookup.lookup();
```

同一个类型也出现在 `nameServerRecords()` 和 `pointerRecords()`。调用方必须结合这次 `QDnsLookup::Type` 判断 `value()` 的业务含义，不能只看返回类型。

## 字段语义与缓存边界

### `name()`

记录所有者名称，即 DNS 响应中该资源记录关联的名称。它不一定与查询时传入的原始字符串逐字相同：DNS 服务器可能返回规范化、重定向后的名称或查询链上的中间名称。

### `value()`

记录的目标域名。对于 CNAME 它是规范名称；对于 NS 是名称服务器主机名；对于 PTR 是反向解析得到的域名。

`value()` 只是 DNS 数据，不代表 Qt 已再次解析或连通验证该域名。若要连接目标，仍需后续地址解析和连接错误处理。

### `timeToLive()`

返回记录的 TTL，单位是秒。TTL 描述解析结果可被缓存的最长时间窗口，不是目标服务器可用性保证，也不是应用必须永久保存该对象的时长。

使用自建缓存时应以收到响应的时间为基准计算到期；网络变化、服务器数据更新和负缓存策略仍可能使旧结果失效。

## 生命周期、共享和线程

该类是隐式共享值类型。`QDnsLookup::canonicalNameRecords()` 等函数返回一个列表，按值保存记录通常成本较低；修改某个记录并不是公开使用模型，因为它没有 setter。

默认构造对象为空。正常程序不应试图先构造它再填字段，而应在 `QDnsLookup::finished()` 后从结果列表读取。`QDnsLookup` 的结果在一次新查询开始前应被当作上一轮查询的快照，界面或缓存若要保留，应复制值而不是保存指向列表元素的引用。

## 逐项 API 说明

### `QDnsDomainNameRecord()`

创建空记录。它没有可设置字段，主要用于容器、默认初始化或接受随后赋值；业务上的有效记录应来自 `QDnsLookup`。

### `QDnsDomainNameRecord(const QDnsDomainNameRecord &other)`

复制记录。该类型隐式共享，复制通常不需要逐字符复制域名数据。

### `~QDnsDomainNameRecord()`

销毁当前值对象并释放它持有的共享引用。不会影响其它副本。

### `QString name() const`

返回记录所有者名称。它是 DNS 名称，不应假设可直接作为 URL、文件名或安全主机名验证结果使用。

### `QString value() const`

返回该记录承载的目标域名。具体语义取决于查询类型，如 CNAME、NS 或 PTR。

### `quint32 timeToLive() const`

返回 TTL 秒数。用于缓存到期计算，而不是连接超时或重试间隔。

### `void swap(QDnsDomainNameRecord &other) noexcept`

快速交换两个记录值。适合容器算法或移动式赋值实现；不会改变 DNS 服务器中的任何数据。

### `operator=(const QDnsDomainNameRecord &other)` / `operator=(QDnsDomainNameRecord &&other)`

复制或移动赋值当前记录。移动后源对象仍可析构或重新赋值，但不应依赖其原有内容。

## 常见误区

- 把 `value()` 当作已经解析好的 IP 地址。
- 以为 TTL 是连接超时、socket 超时或服务器健康检查周期。
- 手工默认构造一个记录后期待能够设置名称和值。
- 不检查 `QDnsLookup::error()` 就读取结果列表。
- 用 PTR 结果直接做身份验证；反向 DNS 不是认证机制。
- 在下一轮查询后长期保留对旧结果列表元素的引用。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QDnsDomainNameRecord()` | 创建空记录。 | 正常有效值来自 `QDnsLookup`。 |
| 构造 | `QDnsDomainNameRecord(const QDnsDomainNameRecord &)` | 复制记录。 | 隐式共享，复制通常较轻。 |
| 析构 | `~QDnsDomainNameRecord()` | 释放当前共享引用。 | 不影响其它副本。 |
| 字段 | `QString name() const` | 返回记录所有者名称。 | 不一定等于原始查询字符串。 |
| 字段 | `QString value() const` | 返回目标域名。 | CNAME、NS、PTR 的含义不同。 |
| 缓存 | `quint32 timeToLive() const` | 返回 TTL 秒数。 | 不是连接超时或可用性保证。 |
| 工具 | `void swap(QDnsDomainNameRecord &)` | 交换两个记录值。 | 不改变 DNS 服务器数据。 |
| 赋值 | 复制/移动 `operator=` | 替换当前记录值。 | 移动后源对象内容不应再依赖。 |

### 一句话总结

`QDnsDomainNameRecord` 是 `QDnsLookup` 返回的域名型 DNS 记录快照；读懂它要区分记录所有者、目标域名和仅用于缓存的 TTL。
