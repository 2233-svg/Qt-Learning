# Qt QUuid::Id128Bytes：携带 UUID 二进制 16 字节的端序承载类型

`QUuid::Id128Bytes` 是 Qt 6.6 引入的平凡 union，用于承载一个 UUID 的完整 128 位二进制内容。它的作用是与要求“恰好 16 字节”的库、协议字段或 GUID/UUID 结构交换数据，而无需手写临时数组和字段拼接。

它不是 UUID 解析器，也不带 variant/version 校验；真正的 UUID 语义由 `QUuid` 负责。`Id128Bytes` 只表达 16 字节存储以及如何按指定端序解释该存储。

```cpp
#include <QUuid>

const QUuid id = QUuid::createUuid();
const QUuid::Id128Bytes bytes = id.toBytes(QSysInfo::BigEndian);

const QUuid restored(bytes, QSysInfo::BigEndian);
Q_ASSERT(restored == id);
```

> 适用版本：Qt 6.11.1，Qt 6.6 起提供  
> 头文件：`#include <QUuid>`  
> 模块：`Qt6::Core`

## 它解决什么问题

很多 UUID API 接受一个 16 字节块，但 C++ 中常见表示不统一：`uint8_t[16]`、两个 `uint64_t`、平台 GUID 结构或支持 128 位整数的编译器扩展。`Id128Bytes` 提供同一块内存的多种视图：

```cpp
union alignas(16) Id128Bytes {
    quint8  data[16];
    quint16 data16[8];
    quint32 data32[4];
    quint64 data64[2];
};
```

它是 16 字节、16 字节对齐的平凡类型，可用 `memcpy()` 与其他明确要求 128 位二进制数据的结构交换。最可靠的跨进程/跨语言表示仍是 `data[16]` 加上协议规定的字节序。

## 端序是 API 的一部分

`data16`、`data32`、`data64` 是对同一内存的机器字视图，数值含义取决于主机端序。不要把 `data64[0]` 直接写入文件或网络后期待另一台机器得到相同数值。

`QUuid::toBytes(order)` 和 `QUuid(Id128Bytes, order)` 显式声明传输端序：

- `BigEndian`：与 `QUuid::toRfc4122()` 的 16 字节内容一致，适合 RFC 4122 风格协议；
- `LittleEndian`：仅在双方明确采用该布局时使用；
- 两端必须使用同一个 `order`，否则 UUID 的字段会被错读。

相关的 `qToBigEndian()` / `qToLittleEndian()` 将 host-order `Id128Bytes` 转为指定字节序；`qFromBigEndian()` / `qFromLittleEndian()` 做反向转换。它们返回新值，不修改输入。

```cpp
QUuid::Id128Bytes host = loadHostRepresentation();
QUuid::Id128Bytes wire = qToBigEndian(host);
sendBytes(wire.data, 16);
```

若 `wire` 本来就是 RFC 4122 网络字节序，不要再额外调用转换；端序转换只能发生一次。

## 生命周期、union 访问与平台边界

`Id128Bytes` 不拥有外部资源，没有 QObject 或线程亲和性，按值复制即可。其 `data` 可隐式转换为 `QByteArrayView`，这只是非拥有视图；不要把该 view 保存到 `Id128Bytes` 已销毁之后。

使用 union 的宽成员有两个边界：

- `data[16]` 是可移植的字节级交换入口；
- 用 `data16` / `data32` / `data64` 解读内容前，必须明确对象来自 host order 还是经过 `qFrom...Endian()` 转换。

存在 `data128` 成员仅取决于编译器是否支持 `unsigned __int128`；它不能作为所有 Qt 目标都能编译的公共接口。需要可移植的 128 位表示时使用 `data` 或 `QUuid::toBytes()`。

## 常见错误

- 将 `data64` 的内存布局当作网络 UUID 规范。
- 同时做 `toBytes(BigEndian)` 和 `qToBigEndian()`，导致重复转换。
- 从外部缓冲区只复制少于 16 字节，或让 `fromBytes()` 读取不足 16 字节。
- 将 `QByteArrayView(id128)` 保存到 `id128` 生命周期之外。
- 把 `Id128Bytes` 当作合法 UUID 的证明；它可以承载任意 16 字节。

## 逐项 API 说明

### 数据成员与转换

`data`、`data16`、`data32`、`data64` 是同一 16 字节的不同粒度视图。应用与外部协议交换时优先使用 `data`。显式转换到 `QByteArrayView` 用于临时只读传参，长度固定为 16。

### 端序辅助函数

四个 `q...Endian()` 函数自 Qt 6.6 起提供，面向 host-order 与指定 byte order 的转换。它们和泛型 `<QtEndian>` 工具一致，但处理完整的 128 位块。

## API 速查表

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `QUuid::Id128Bytes` | 承载完整 UUID 二进制数据 | Qt 6.6 起；固定 16 字节、16 字节对齐的平凡 union。 |
| `data[16]` | 以字节访问内容 | 跨平台/协议交换的首选表示。 |
| `data16[8]` / `data32[4]` / `data64[2]` | 以机器字访问同一内存 | 数值解释依赖端序，不能直接当网络布局。 |
| `data128[1]` | 以编译器 128 位整数访问 | 仅在编译器支持时存在，不能作为可移植契约。 |
| `operator QByteArrayView()` | 创建 16 字节非拥有视图 | view 不延长 `Id128Bytes` 生命周期。 |
| `QUuid::toBytes(order)` | 从 UUID 得到 `Id128Bytes` | `BigEndian` 与 RFC 4122 字节内容一致。 |
| `QUuid(Id128Bytes, order)` | 按指定端序还原 UUID | 生产端与消费端必须使用同一端序。 |
| `QUuid::fromBytes(void *, order)` | 从外部 16 字节读 UUID | 指针必须至少可读 16 字节。 |
| `qToBigEndian(src)` | host-order 转大端 | 返回副本；用于写明确的大端协议。 |
| `qToLittleEndian(src)` | host-order 转小端 | 只用于协议明确要求小端时。 |
| `qFromBigEndian(src)` | 大端转 host-order | 读取网络/磁盘大端块时使用。 |
| `qFromLittleEndian(src)` | 小端转 host-order | 读取明确的小端块时使用。 |

---

### 一句话总结

`QUuid::Id128Bytes` 是 UUID 的 16 字节承载层：协议交换用 `data[16]`，构造/还原时显式声明端序，绝不把 union 的机器字视图当作天然跨平台格式。
