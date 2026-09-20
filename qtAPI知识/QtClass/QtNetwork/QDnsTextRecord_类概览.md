# QDnsTextRecord：表示 DNS TXT 查询返回的原始文本片段

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDnsTextRecord>`  
> 所属模块：`Qt6::Network`  
> 类型性质：隐式共享值类型，由 `QDnsLookup` 返回

## 它解决什么问题

DNS TXT 记录常用于携带协议配置、域名所有权证明、邮件策略和服务元数据。`QDnsTextRecord` 保存一条 TXT 记录的所有者名称、TTL，以及一个 `QList<QByteArray>` 形式的原始片段列表。

它不把 TXT 内容自动解释为 UTF-8、JSON、SPF、DKIM、DMARC 或任意业务协议。DNS 的 TXT 数据在协议层是字节片段，正确的拼接、字符集和语法必须由使用该记录的上层规范决定。

## 实际使用场景

```cpp
QDnsLookup lookup(QDnsLookup::TXT, u"example.test"_s);

connect(&lookup, &QDnsLookup::finished, this, [&lookup] {
    if (lookup.error() != QDnsLookup::NoError)
        return;

    for (const QDnsTextRecord &record : lookup.textRecords()) {
        for (const QByteArray &part : record.values())
            qDebug() << record.name() << part;
    }
});

lookup.lookup();
```

常见用途包括读取某项协议规定的 TXT 数据、诊断 DNS 配置、取得服务验证挑战值。调用方应先确定“查询的这个名称遵循哪一个协议”，再决定如何处理 `values()`。

## `values()` 不是一个普通字符串

`values()` 返回 `QList<QByteArray>`，而不是单个 `QString`。原因是 DNS TXT RDATA 可以被拆分为多个字符字符串：

- 每个元素保留一段原始字节；
- 多段是否应连接、用什么顺序连接，由具体协议定义；
- 字节不保证是可显示文本，更不保证符合 UTF-8；
- 不应先转换成 `QString` 再丢失无法表示的字节。

例如协议明确规定将全部片段依次连接时，才可以执行：

```cpp
QByteArray combined;
for (const QByteArray &part : record.values())
    combined += part;
```

连接后仍应按该协议规定验证长度、编码、转义和语法。不能因为内容“看起来像文本”就跳过解析和校验。

## `name()`、TTL 与缓存

`name()` 返回 TXT 记录的 DNS 所有者名称。它与原始请求名称可能不完全相同，例如应答包含规范化或重定向后的名称时。

`timeToLive()` 的单位是秒，表示 DNS 缓存有效期。它不代表某项业务令牌、域名验证挑战或服务配置本身在业务层的有效期限；业务协议可规定更短的刷新时间。

## 生命周期和数据来源

`QDnsTextRecord` 是隐式共享值类型，正常结果来自 `QDnsLookup::textRecords()`。默认构造得到空记录，且没有 setter；它不适合作为手工 TXT 记录构造器。

应在 `QDnsLookup::finished()` 之后检查 `error()` 再读取结果。若将记录转发给后台分析或缓存，按值保存即可，但不要保存对查询列表元素或 `values()` 临时返回对象的引用。

## 逐项 API 说明

### `QDnsTextRecord()`

创建空 TXT 记录。它用于默认初始化或容器，不表示一个空字符串形式的有效 DNS 记录。

### `QDnsTextRecord(const QDnsTextRecord &other)`

复制记录。隐式共享使正常的按值传递成本较低。

### `QString name() const`

返回 TXT 记录所有者名称。它只是 DNS 名称，不保证可直接作为 URL 或用户可见文本。

### `QList<QByteArray> values() const`

返回原始 TXT 片段列表。每项是字节数据；是否连接、如何解码必须由业务协议决定。

### `quint32 timeToLive() const`

返回 TTL 秒数，用于 DNS 缓存失效处理。

### `void swap(QDnsTextRecord &other) noexcept`

快速交换两个本地记录值。不会影响 DNS 服务器或 resolver 缓存。

### 复制/移动 `operator=`

用另一个记录替换当前值。移动后源对象内容不应继续依赖。

## 常见误区

- 把 `values()` 的第一个元素当作全部 TXT 内容。
- 不经协议确认就把所有片段转换为 UTF-8 `QString`。
- 盲目拼接片段后把结果当作可信配置。
- 将 DNS TTL 当作业务令牌或授权状态的有效期。
- 在查询失败后把空列表解释为“域名没有 TXT 记录”。
- 试图通过默认构造对象手工设置 TXT 内容。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QDnsTextRecord()` | 创建空 TXT 记录。 | 有效记录来自 `QDnsLookup`。 |
| 构造 | `QDnsTextRecord(const QDnsTextRecord &)` | 复制记录。 | 隐式共享，复制通常较轻。 |
| 字段 | `QString name() const` | 返回记录所有者名称。 | 不一定等于原始查询名称。 |
| 数据 | `QList<QByteArray> values() const` | 返回 TXT 原始片段。 | 不是自动拼接或自动解码的文本。 |
| 缓存 | `quint32 timeToLive() const` | 返回 TTL 秒数。 | 不等价于业务数据有效期。 |
| 工具 | `void swap(QDnsTextRecord &)` | 交换两个记录值。 | 不影响 resolver 或服务端。 |
| 赋值 | 复制/移动 `operator=` | 替换当前记录。 | 移动后不依赖源内容。 |

### 一句话总结

`QDnsTextRecord` 给出 DNS TXT 的原始字节片段；只有知道上层协议后，才能决定如何拼接、解码和验证它们。
