# Qt QUuid：生成、解析和传输 128 位 UUID

`QUuid` 是 Qt 的 128 位 UUID/GUID 值类型。它用于给分布式对象、数据库记录、缓存项、插件接口和跨进程消息分配稳定标识。它只表示标识值，不会保存对象、注册全局资源或保证业务层的唯一约束。

```cpp
#include <QUuid>

const QUuid id = QUuid::createUuid();
qDebug() << id.toString(QUuid::WithoutBraces);
```

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QUuid>`  
> CMake：`Qt6::Core`  
> 线程：所有 API 可重入；`QUuid` 是小型值类型，无 QObject 生命周期。

## 它解决什么问题

UUID 是 16 字节标识。`QUuid` 避免业务代码自行处理连字符格式、variant/version 位、RFC 4122 字节序、Windows `GUID` 与 Apple UUID 对象的转换。

典型选择：

| 目标 | API | 语义 |
| --- | --- | --- |
| 为新对象生成通常唯一的随机 ID | `createUuid()` | 生成 DCE variant 的 version 4 随机 UUID。 |
| 对同一 namespace 和同一输入稳定生成同一 ID | `createUuidV3()` / `createUuidV5()` | v3 使用 MD5，v5 使用 SHA-1；可重现，不是保密散列。 |
| 希望大致按生成时间排序 | `createUuidV7()` | Qt 6.9 起；使用 Unix epoch 时间布局并加入随机性。 |
| 与协议或磁盘字段交换 16 字节 | `toRfc4122()` / `fromRfc4122()` | RFC 4122 大端字节布局。 |

随机 UUID 不是访问令牌或密码。它的碰撞概率很低，但“难猜”“可撤销”“被授权”都需要独立的安全机制。v3/v5 对已知输入可被重算，绝不可把秘密直接作为其唯一保护。

## 生成、确定性与版本字段

```cpp
const QUuid sessionId = QUuid::createUuid(); // v4 random

const QUuid namespaceId(
    0x67c8770b, 0x44f1, 0x410a, 0xab, 0x9a,
    0xf9, 0xb5, 0x44, 0x6f, 0x13, 0xee);
const QUuid stableId =
    QUuid::createUuidV5(namespaceId, u"customer:42"_s);
```

v3/v5 的 namespace 是输入的一部分。只要 namespace、数据和编码方式不变，输出就相同；更换 namespace 或把文本与原始字节混用都会得到不同值。`QString` 重载先转换为 UTF-8，`QByteArrayView` 重载则直接使用给定字节，跨语言协议应明确采用哪一种。

`variant()` 读取 UUID variant。只有 variant 为 `DCE` 时，`version()` 才返回有效 version；null UUID 的 variant 是 `VarUnknown`，非 DCE UUID 的 `version()` 是 `VerUnknown`。`Time`、`EmbeddedPOSIX`、`Md5`/`Name`、`Random`、`Sha1` 与 `UnixEpoch` 分别是公开识别值，不表示 Qt 能生成每一种版本。

## 文本、null 与二进制表示

默认文本格式为 `{xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx}`：

```cpp
QUuid parsed = QUuid::fromString(u"{67c8770b-44f1-410a-ab9a-f9b5446f13ee}"_s);
if (parsed.isNull())
    return;

const QString compact = parsed.toString(QUuid::Id128);
```

`WithBraces` 带花括号，`WithoutBraces` 只去花括号，`Id128` 输出 32 个十六进制字符且没有连字符。`toByteArray()` 是相同文本表示的 ASCII `QByteArray`，不是 16 字节二进制 UUID。

默认构造是 null UUID `{00000000-0000-0000-0000-000000000000}`。`fromString()`/文本构造解析失败也会产生 null，因此“null 是否允许”应由业务层明确判断；若 null 在业务中合法，不能仅靠 `isNull()` 区分“输入恰好全零”和“文本非法”。

`toRfc4122()` 产生 16 字节 RFC 大端表示，`fromRfc4122()` 从该布局读取。短于 16 字节的输入没有可用 UUID 语义，调用前先检查长度。

## `Id128Bytes`、整数与字节序

Qt 6.6 的 `Id128Bytes` 是对齐为 16 字节的 union，可按 `data[16]`、16/32/64 位数组访问。`toBytes(BigEndian)` 与 `toRfc4122()` 二进制内容一致；`fromBytes()`/构造 `Id128Bytes` 时必须让调用双方使用同一 `QSysInfo::Endian`。

```cpp
const QUuid::Id128Bytes bytes = id.toBytes(QSysInfo::BigEndian);
const QUuid restored(bytes, QSysInfo::BigEndian);
Q_ASSERT(restored == id);
```

`fromBytes(const void *)` 会读取 16 字节，指针必须指向至少 16 个有效字节。`fromUInt128()`/`toUInt128()` 也自 Qt 6.6 起，但只在编译器/平台提供 128 位整数类型时存在；不要把它作为可移植 API 的唯一表示。

## 平台互操作与排序

Windows 上可在 `GUID` 与 `QUuid` 间构造、赋值、比较和转换；这些 API 仅 Windows 可用。Apple 平台上的 `fromCFUUID()` / `toCFUUID()`、`fromNSUUID()` / `toNSUUID()` 仅 Darwin 可用：`toCFUUID()` 的返回对象由调用方释放，`toNSUUID()` 返回 autoreleased 对象。

`QUuid` 可哈希、强比较和放进 Qt 容器。比较顺序是 Qt 的 UUID 排序规则，文档明确它不必等同于 `toString()`、`toBytes()` 或整数表示的词典序。若数据库/协议要求特定排序，直接排序对应的规范化表示。

## 常见错误

- 将 `createUuid()` 生成的值当作授权凭据。
- 用 v3/v5 处理秘密输入并假定输出不可推测。
- 把 `toByteArray()` 当作 16 字节网络字段，而不是文本。
- 在读写二进制 UUID 时未约定 `BigEndian`/`LittleEndian`。
- 将解析失败得到的 null 与合法全零 UUID 混为一谈。
- 用 `QUuid` 的比较顺序替代协议规定的字节序排序。
- 在非 Windows/Apple 平台调用平台专属转换 API。

## 逐项 API 说明

### 创建与解析

`createUuid()` 用于随机 v4；v3/v5 用 namespace 和数据生成确定性 ID；v7 用于时间有序场景。`fromString()` 和文本构造解析 UUID；`fromRfc4122()`、`fromBytes()`、`fromUInt128()` 分别处理协议字节、可指定端序的 16 字节和平台提供的 128 位整数。

### 输出与元数据

`toString()` / `toByteArray()` 输出文本，`toRfc4122()` / `toBytes()` 输出二进制，不能互换。`isNull()`、`variant()`、`version()` 只读取值的结构，不验证它在某个数据库或网络中是否唯一。

## API 速查表

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `QUuid()` | 创建 null UUID | 全零值，不是随机 ID。 |
| `QUuid(QAnyStringView)` / `fromString()` | 从文本解析 | 失败为 null；业务需处理非法输入与全零值歧义。 |
| `QUuid(uint, ushort, ushort, uchar...)` | 从字段显式构造 | 需自行正确设置 variant/version 位。 |
| `QUuid(Id128Bytes, Endian)` | 从 16 字节 union 构造 | Qt 6.6 起；端序必须与生产端一致。 |
| `createUuid()` | 生成随机 UUID | v4/DCE；不可替代认证 token。 |
| `createUuidV3(ns, QByteArrayView/QString)` | 生成确定性 MD5 name UUID | 同 namespace 和字节输入结果相同；不适合保密。 |
| `createUuidV5(ns, QByteArrayView/QString)` | 生成确定性 SHA-1 name UUID | 同样可重现；明确文本 UTF-8 与原始字节语义。 |
| `createUuidV7()` | 生成 Unix-epoch UUID | Qt 6.9 起；适合需要时间相关排序的场景。 |
| `isNull()` | 判断是否全零 | 解析失败也常表现为 null。 |
| `variant()` | 查询 variant 位 | null 为 `VarUnknown`。 |
| `version()` | 查询 version 位 | 只有 DCE variant 返回已知 version，否则 `VerUnknown`。 |
| `WithBraces` | 文本带 `{}` | `toString()` / `toByteArray()` 默认格式。 |
| `WithoutBraces` | 文本不带花括号 | 仍含连字符。 |
| `Id128` | 32 位十六进制文本 | 无花括号和连字符，不是二进制。 |
| `toString()` / `toByteArray()` | 输出 UUID 文本 | 后者是 ASCII 文本字节，不是 RFC 16 字节。 |
| `toRfc4122()` / `fromRfc4122()` | RFC 4122 16 字节转换 | 大端布局；输入前检查 16 字节长度。 |
| `toBytes()` / `fromBytes()` | 可选端序 16 字节转换 | Qt 6.6 起；`fromBytes` 指针必须可读 16 字节。 |
| `toUInt128()` / `fromUInt128()` | 与 128 位整数转换 | Qt 6.6 起，仅存在于支持该整数类型的平台。 |
| `Id128Bytes` | 16 字节对齐二进制承载 | Qt 6.6 起；详见独立 `QUuid_Id128Bytes` 笔记。 |
| `qHash()` | 生成哈希 | 用于 `QHash` / `QSet`。 |
| `operator==`, `!=`, `<`, `<=`, `>`, `>=` | 比较 UUID | 排序未必等同文本或字节序排序。 |
| `QDataStream << >>` | 读写 Qt 数据流 | 双方约定流版本；不是公开跨语言协议。 |
| `QDebug <<` | 调试输出 | 仅用于日志/诊断。 |
| `GUID` 构造、转换、比较、赋值 | Windows GUID 互操作 | 仅 Windows。 |
| `fromCFUUID()` / `toCFUUID()` | Core Foundation UUID 互操作 | 仅 Apple；返回 CFUUID 由调用方释放。 |
| `fromNSUUID()` / `toNSUUID()` | Objective-C UUID 互操作 | 仅 Apple；返回 NSUUID 为 autoreleased。 |

---

### 一句话总结

`QUuid` 提供 UUID 的随机生成、确定性 name UUID、v7 时间布局和规范字节/文本转换；先选对版本，再明确文本还是 16 字节、以及二进制交换的端序。
