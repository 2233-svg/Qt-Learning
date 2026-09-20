# QCborStreamWriter 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QCborStreamWriter>`  
> 模块：`Qt6::Core`  
> 定位：直接向 `QByteArray` 或 `QIODevice` 单向编码 CBOR

## 它解决什么问题

`QCborStreamWriter` 是低层、StAX 风格的 CBOR 编码器。它适合大数据分段产生、直接写文件或套接字、以及不希望先在内存构造完整 `QCborValue` 树的场景。

它是单向写入器：写出的字节无法回退或重排。结构简单且数据量可控时，先构造 `QCborValue` / `QCborMap` / `QCborArray` 再 `toCbor()` 通常更不容易出错；需要流式输出或精确控制类型时再用它。

```cpp
QByteArray bytes;
QCborStreamWriter writer(&bytes);

writer.startMap(2);
writer.append("id");
writer.append(42);
writer.append("payload");
writer.appendByteString(raw.constData(), raw.size());
if (!writer.endMap())
    return; // 当前流已经不可信
```

## 容器必须配对，显式长度必须准确

`startArray()` / `startMap()` 打开不定长容器，必须由对应 `endArray()` / `endMap()` 关闭。`startArray(count)` 的 `count` 是元素个数；`startMap(count)` 的 `count` 是键值对数量，不是键和值总数。

显式长度容器必须写入恰好指定数量的元素或键值对。多写、少写时，结束函数返回 `false`，并且输出流已无法安全继续使用。嵌套时按栈式顺序关闭容器，不能交叉关闭。

规范 CBOR 要求显式长度，因此需要 canonical encoding 时使用带 `count` 的重载；不定长数组和 map 不符合规范编码要求。

## map 的正确性由调用方负责

写入器只写字节，不验证 map 键是否唯一、是否按规范顺序排序，也不验证 tag 与后续值的类型是否匹配。签名、哈希、缓存键或跨实现互操作需要规范 CBOR 时，调用方必须：

- 使用显式长度数组和 map。
- 先对 map 键按规范顺序排序，并确保唯一。
- 自行选择足够小但无损的浮点表示。
- 让 tag 与值满足对应标准的约束。

## 文本、字节串和类型选择

`append(QByteArray)` 写的是 CBOR byte string；`append(QStringView)` / `append(QLatin1StringView)` 写的是 CBOR text string。二进制摘要、压缩内容和任意原始字节必须用 byte string，不能把它伪装成 UTF-8 文本。

`appendTextString(const char *, len)` 假定输入已经是合法 UTF-8，不做验证；来源不可信时更应使用 `QString` 或先验证 UTF-8。`appendByteString()` 没有编码含义，只写给定字节。

## 设备与失败边界

构造时可接 `QByteArray *` 或 `QIODevice *`。写入器不拥有外部 `QIODevice`，设备必须在整个写入期间存活并处于可写状态。`device()` 在以 `QByteArray` 构造时返回写入器内部拥有的 `QBuffer`，不应把该指针当作外部设备所有权。

`setDevice()` 会切换目标；只应在没有打开未闭合容器时执行。设备 I/O 错误由设备自身状态和 `errorString()` 体现，写入器没有独立的通用错误查询接口。

## 常见误区

- 以为 writer 会替你纠正 map 键重复、键顺序或 tag 类型错误。
- 对显式长度 map 传递“键和值总数”而不是 pair 数。
- `endMap()` 或 `endArray()` 返回 `false` 后继续追加。
- 把 `QByteArray` 当文本写入，造成协议类型错误。
- 使用 `appendTextString()` 写未经验证的字节数据。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QCborStreamWriter(QByteArray *)` | 向内存字节数组编码。 | 目标数组在 writer 存活期内必须有效。 |
| 构造 | `QCborStreamWriter(QIODevice *)` | 向设备直接编码。 | writer 不拥有设备，设备应已打开可写。 |
| 目标 | `setDevice(QIODevice *)`、`device()` | 切换或取得当前写入设备。 | 未闭合容器时不要切换；内存构造时返回内部 `QBuffer`。 |
| 整数 | `append(quint64)`、`append(qint64)`、`append(QCborNegativeInteger)` | 写无符号、常规有符号或超出 `qint64` 的负整数表达。 | 选择与协议范围匹配的类型；writer 会压缩整数编码。 |
| 浮点 | `append(qfloat16)`、`append(float)`、`append(double)` | 写指定宽度浮点数。 | 规范编码要求开发者自己选择可无损表示的最小宽度。 |
| 布尔与空 | `append(bool)`、`appendNull()`、`appendUndefined()`、`append(QCborSimpleType)` | 写 simple type。 | `null` 与 `undefined` 有不同协议含义。 |
| 标签 | `append(QCborTag)`、`append(QCborKnownTags)` | 在后续值前写 CBOR tag。 | writer 不验证 tag 和后续值是否匹配。 |
| 文本 | `append(QLatin1StringView / QStringView / QUtf8StringView / const char *)` | 写 CBOR text string。 | 文本必须是 UTF-8 语义；Qt 6.10 提供 `QUtf8StringView` 重载。 |
| 原始文本 | `appendTextString(const char *, qsizetype)` | 直接写 UTF-8 字节为 text string。 | 不验证 UTF-8，调用方负责正确性。 |
| 二进制 | `append(QByteArray / QByteArrayView)`、`appendByteString()` | 写 CBOR byte string。 | 不要把二进制 payload 写成 text string。 |
| 数组 | `startArray()` | 打开不定长数组。 | 必须调用 `endArray()`；不符合 canonical CBOR。 |
| 数组 | `startArray(quint64 count)` | 打开指定元素数量的数组。 | 元素数量必须恰好为 count。 |
| 数组 | `endArray()` | 关闭最近打开的数组。 | 返回 `false` 说明长度错误，流不可恢复。 |
| map | `startMap()` | 打开不定长 map。 | 必须 `endMap()`；不符合 canonical CBOR。 |
| map | `startMap(quint64 count)` | 打开指定键值对数量的 map。 | count 是 pair 数；确保键唯一且按需要排序。 |
| map | `endMap()` | 关闭最近打开的 map。 | 返回 `false` 后停止使用该输出流。 |
| 生命周期 | 析构函数 | 释放 writer 自身资源。 | 不替你补写遗漏的容器结束标记。 |

## 一句话总结

`QCborStreamWriter` 用最少中间对象直接产出 CBOR，但也把结构、长度、键排序、标签匹配和设备失败处理交还给调用方。每个 `start` 都要有正确的 `end`，每次 `end` 都值得检查返回值。
