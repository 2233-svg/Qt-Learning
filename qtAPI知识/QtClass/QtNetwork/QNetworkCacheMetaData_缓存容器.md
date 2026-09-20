# QNetworkCacheMetaData：网络缓存条目的描述信息

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QNetworkCacheMetaData>`  
> CMake：`Qt6::Network`  
> 类型：隐式共享值类型

## 它解决什么问题

`QNetworkCacheMetaData` 保存一个网络缓存条目的非正文信息：请求 URL、响应头、最后修改和过期时间、磁盘存储许可，以及与 `QNetworkRequest::Attribute` 对应的属性。

缓存内容本身放在 `QIODevice` 或后端文件中；本类不含响应体。`QAbstractNetworkCache` 用它将“哪个 URL 的什么响应、可保存到哪里、何时过期”与字节数据关联起来。

## 实际使用场景

- 自定义 `QAbstractNetworkCache` 的 `prepare()`、`metaData()` 和 `updateMetaData()` 实现。
- 检查某个磁盘缓存文件的 URL、HTTP 头、有效期和落盘许可。
- 将缓存元数据用 `QDataStream` 与自己的缓存索引一同持久化。
- 结合请求/响应属性判断缓存条目是否可复用。

普通 HTTP 客户端一般不需要自行构造它；直接让 `QNetworkAccessManager` 和 `QNetworkDiskCache` 协作即可。

## 一个有效条目的最小形状

默认构造的元数据是无效的。`isValid()` 只在对象含有已设置属性时返回 `true`，因此自定义缓存至少应明确设置 URL 与适当的属性/头部，再进入 `prepare()`：

```cpp
#include <QNetworkCacheMetaData>
#include <QNetworkRequest>
#include <QUrl>

QNetworkCacheMetaData metaData;
metaData.setUrl(QUrl(QStringLiteral("https://example.com/assets/app.js")));
metaData.setAttributes({
    {QNetworkRequest::HttpStatusCodeAttribute, 200}
});
metaData.setSaveToDisk(true);

if (metaData.isValid()) {
    // 现在可以交给 QAbstractNetworkCache::prepare(metaData)。
}
```

URL 写入时会移除密码和 fragment。这既避免把凭据写入缓存索引，也使 fragment（不会发送给 HTTP 服务器）不参与条目标识。

## 关键语义与边界

### `rawHeaders()` 与 `headers()` 面向不同用途

`RawHeader` 是 `std::pair<QByteArray, QByteArray>`，`RawHeaderList` 是按设置顺序保存的列表；适合需要保留原始头名称、值和顺序的缓存格式。

Qt 6.8 起可用 `headers()` / `setHeaders()` 取得或设置 `QHttpHeaders`，适合按规范化名称查找、处理多值头和使用结构化 HTTP 头 API。选择哪一个取决于缓存后端及调用链需要，不应自己用逗号拼接语义上不可合并的重复 HTTP 头。

### 有效期不是自动删除命令

`expirationDate()` 和 `lastModified()` 只是元数据时间。缓存后端或请求缓存策略据此决定是否复用；设置过期时间本身不会立即删除内容。实现持久化缓存时，清理过期条目和容量淘汰仍是后端责任。

### `saveToDisk()` 是敏感内容的存储许可

该字段表示关联内容是否允许写入磁盘。缓存实现可以在内存保留某些数据以提升性能，但因安全原因不应写入磁盘。对于 HTTP，`Cache-Control: no-store` 的文档，以及没有 `Cache-Control: public` 的 HTTPS 文档，会令该标志为 `false`。

自定义磁盘缓存必须尊重该值；不能因为“缓存目录可写”就将受限内容落盘。反过来，`true` 也只是允许落盘，仍应服从容量、过期和应用自己的隐私策略。

### 值语义和流序列化

本类是隐式共享值类型，复制、赋值和 `swap()` 都只操作元数据值，不持有 cache 或文件。`QDataStream` 的 `<<` / `>>` 可序列化该值，适合 Qt 内部或配套存储格式；读入外部不可信数据时仍需验证 `isValid()`、URL、日期和 header 大小，不能把反序列化成功当作安全保证。

## 常见误区

- **默认构造后就调用 `prepare()`**：默认元数据无效。
- **把 fragment 或 URL 密码作为缓存 key 的一部分**：`setUrl()` 会移除它们；自定义后端也应保持一致。
- **误以为 `expirationDate` 会自动删除文件**：它是策略信息，清理需要后端执行。
- **忽略 `saveToDisk=false`**：这可能把不应持久化的 HTTPS 或 `no-store` 内容写到磁盘。
- **将所有重复响应头拼成一条字符串**：需要保留多值语义时应使用 `QHttpHeaders` 或 `RawHeaderList`。

## API 速查表

| 类别 | API | 语义与注意点 |
| --- | --- | --- |
| 类型别名 | `RawHeader` | `std::pair<QByteArray, QByteArray>`，表示一条原始 HTTP 头名称和值。 |
| 类型别名 | `RawHeaderList` | `QList<RawHeader>`，按设置顺序保存原始头。 |
| 类型别名 | `AttributesMap` | `QHash<QNetworkRequest::Attribute, QVariant>`，保存请求/响应相关属性。 |
| 构造 | `QNetworkCacheMetaData()` | 构造无效元数据。 |
| 构造 | 拷贝构造、拷贝/移动赋值、`swap(other)` | 隐式共享值操作，不接触缓存内容。 |
| 析构 | `~QNetworkCacheMetaData()` | 普通值类型析构。 |
| 有效性 | `isValid()` | 是否已有设置的 attributes；自定义后端应拒绝无效元数据。 |
| URL | `url()` / `setUrl(url)` | 读取/设置条目 URL；设置时移除 password 与 fragment。 |
| 原始头 | `rawHeaders()` / `setRawHeaders(list)` | 读取/设置原始头列表，保留设置顺序。 |
| 结构化头 | `headers()` / `setHeaders(headers)` | Qt 6.8 起读取/设置 `QHttpHeaders`。 |
| 时间 | `lastModified()` / `setLastModified(dateTime)` | 读取/设置元数据最后修改时间。 |
| 时间 | `expirationDate()` / `setExpirationDate(dateTime)` | 读取/设置过期时间；不自动删除缓存内容。 |
| 存储策略 | `saveToDisk()` / `setSaveToDisk(allow)` | 是否允许关联内容写入磁盘；自定义磁盘后端应尊重。 |
| 属性 | `attributes()` / `setAttributes(map)` | 读取/整体替换 `QNetworkRequest::Attribute` 映射。 |
| 比较 | `operator==(other)` / `operator!=(other)` | 比较元数据值是否完全相等。 |
| 流 | `operator<<(QDataStream &, metaData)` | 将元数据写入 Qt 数据流。 |
| 流 | `operator>>(QDataStream &, metaData)` | 从 Qt 数据流读取元数据；读取外部数据后仍应验证。 |

## 相关类型

- `QAbstractNetworkCache`：使用此对象准备、查询和更新缓存条目。
- `QNetworkDiskCache`：Qt 的磁盘缓存实现。
- `QHttpHeaders`：Qt 6.8 起的结构化响应头表示。
- `QNetworkRequest::Attribute`：属性映射的 key 类型。
