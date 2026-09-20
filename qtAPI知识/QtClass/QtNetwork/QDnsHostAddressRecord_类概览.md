# QDnsHostAddressRecord：表示 A 或 AAAA 查询返回的地址记录

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDnsHostAddressRecord>`  
> 所属模块：`Qt6::Network`  
> 类型性质：隐式共享值类型，由 `QDnsLookup` 返回

## 它解决什么问题

`QDnsHostAddressRecord` 表示一次 DNS 地址查询返回的一条 A 或 AAAA 记录。它把记录所有者名称、IP 地址和 TTL 封装在一个只读值对象中。

它适合保留 DNS 协议层的完整结果。相比 `QHostInfo`，它不会把地址查询简化为一个主机名加地址列表，也不会隐藏每条记录自己的 TTL。

它不是 socket 连接对象，也不会验证该地址当前能否连通。连接仍要交给 `QTcpSocket`、`QUdpSocket` 或其它网络对象，并独立处理失败。

## 实际使用场景

```cpp
QDnsLookup lookup(QDnsLookup::AAAA, u"api.example.test"_s);

connect(&lookup, &QDnsLookup::finished, this, [&lookup] {
    if (lookup.error() != QDnsLookup::NoError)
        return;

    for (const QDnsHostAddressRecord &record : lookup.hostAddressRecords()) {
        qDebug() << record.name()
                 << record.value().toString()
                 << "TTL:" << record.timeToLive();
    }
});

lookup.lookup();
```

查询 `QDnsLookup::A` 时结果通常是 IPv4；查询 `AAAA` 时通常是 IPv6。`hostAddressRecords()` 的实际内容以 DNS 应答为准，业务不能只凭请求类型推断结果一定非空。

## 三个字段的边界

### `name()`

返回该记录的所有者 DNS 名称。CNAME 链、DNS 规范化和服务器应答可能使它不同于应用最初输入的名称。

### `value()`

返回 `QHostAddress`。它只是 DNS 返回的数值地址：

- 不是已经建立的连接；
- 不带端口；
- 不代表主机名验证、TLS SNI 或证书验证已完成；
- 也不保证地址在当前网络中仍可达。

### `timeToLive()`

返回 TTL，单位为秒。若应用构建自己的地址缓存，应从收到 DNS 响应时开始计算过期时间；TTL 不等价于 socket 超时、HTTP 缓存时间或服务健康时间。

## 生命周期、共享和查询时机

该类隐式共享，按值复制通常很轻量。默认构造得到空值；公开 API 没有 setter，完整记录应从 `QDnsLookup::hostAddressRecords()` 取得。

应在 `QDnsLookup::finished()` 中先检查 `error()`，再读取结果。启动下一次 `lookup()` 前，将上一轮结果视为可被替换的快照；需要在异步任务、模型或缓存中长期使用时，复制记录而不是保存列表元素引用。

## 逐项 API 说明

### `QDnsHostAddressRecord()`

创建空地址记录。它适用于容器或占位，不表示一个可连接的默认地址。

### `QDnsHostAddressRecord(const QDnsHostAddressRecord &other)`

复制记录。值对象采用隐式共享语义；若只传递或保存查询结果，通常不需要深复制地址数据。

### `~QDnsHostAddressRecord()`

销毁记录对象并释放当前共享引用。

### `QString name() const`

返回记录的 DNS 所有者名称。它不是经过 URL、IDN 或安全策略处理后的主机名。

### `QHostAddress value() const`

返回 A/AAAA 记录中的网络地址。用 `protocol()`、`toString()` 或 `isNull()` 等 `QHostAddress` API 判断地址形态，但不要把它直接等同于“服务可信且可连接”。

### `quint32 timeToLive() const`

返回缓存有效期秒数。TTL 到期后应重新解析或按业务策略刷新。

### `void swap(QDnsHostAddressRecord &other) noexcept`

交换两个地址记录值。它只是本地对象操作，不会影响 DNS 缓存或网络请求。

### 复制/移动 `operator=`

用另一个记录替换当前值。移动后源对象只保证可析构或重新赋值。

## 常见误区

- 将 DNS 返回地址当成已经验证身份的服务器。
- 忽略 IPv6，只按字符串冒号或点号猜测地址类型。
- 把 TTL 当作连接超时或重试间隔。
- 不检查 `QDnsLookup::error()` 就使用空结果列表。
- 默认构造后期待能够设置 `name`、地址和 TTL。
- 在后续查询后继续保存对旧结果列表元素的引用。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QDnsHostAddressRecord()` | 创建空地址记录。 | 不表示可连接的默认地址。 |
| 构造 | `QDnsHostAddressRecord(const QDnsHostAddressRecord &)` | 复制记录。 | 隐式共享，复制通常较轻。 |
| 析构 | `~QDnsHostAddressRecord()` | 释放当前共享引用。 | 不影响其它副本。 |
| 字段 | `QString name() const` | 返回 DNS 所有者名称。 | 不一定等于原始查询字符串。 |
| 字段 | `QHostAddress value() const` | 返回记录中的 IP 地址。 | 不含端口，也不验证连通性或身份。 |
| 缓存 | `quint32 timeToLive() const` | 返回 TTL 秒数。 | 不是 socket 或 HTTP 超时。 |
| 工具 | `void swap(QDnsHostAddressRecord &)` | 交换两个记录值。 | 不改变 DNS 服务器或缓存。 |
| 赋值 | 复制/移动 `operator=` | 替换当前记录值。 | 移动后不依赖源对象内容。 |

### 一句话总结

`QDnsHostAddressRecord` 保留一条 A/AAAA DNS 应答的地址与 TTL；它是解析结果，不是连接、认证或可用性结论。
