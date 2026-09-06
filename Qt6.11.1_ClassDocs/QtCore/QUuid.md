# QUuid

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“Uuid”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QUuid` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QUuid>`
- 继承自：未在类页中列出
- 直接派生类：QBluetoothUuid

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

### 状态、生命周期和线程

**生命周期：** 先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

**状态与结果：** 把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

**线程与事件循环：** 如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

## 3. 直接使用

围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum StringFormat { WithBraces, WithoutBraces, Id128 }`
- `enum Variant { VarUnknown, NCS, DCE, Microsoft, Reserved }`
- `enum Version { VerUnknown, Time, EmbeddedPOSIX, Name, Md5, …, UnixEpoch }`

### 公有函数

- `QUuid()`
- `QUuid(QAnyStringView text)`
- `QUuid(const GUID &guid)`
- `(since 6.6) QUuid(QUuid::Id128Bytes id128, QSysInfo::Endian order = QSysInfo::BigEndian)`
- `QUuid(uint l, ushort w1, ushort w2, uchar b1, uchar b2, uchar b3, uchar b4, uchar b5, uchar b6, uchar b7, uchar b8)`
- `bool isNull() const`
- `QByteArray toByteArray(QUuid::StringFormat mode = WithBraces) const`
- `(since 6.6) QUuid::Id128Bytes toBytes(QSysInfo::Endian order = QSysInfo::BigEndian) const`
- `CFUUIDRef toCFUUID() const`
- `NSUUID * toNSUUID() const`
- `QByteArray toRfc4122() const`
- `QString toString(QUuid::StringFormat mode = WithBraces) const`
- `(since 6.6) quint128 toUInt128(QSysInfo::Endian order = QSysInfo::BigEndian) const`
- `QUuid::Variant variant() const`
- `QUuid::Version version() const`
- `operator GUID() const`
- `QUuid & operator=(const GUID &guid)`

### 静态公有成员

- `QUuid createUuid()`
- `QUuid createUuidV3(QUuid ns, QByteArrayView baseData)`
- `QUuid createUuidV3(const QUuid &ns, const QString &baseData)`
- `QUuid createUuidV5(QUuid ns, QByteArrayView baseData)`
- `QUuid createUuidV5(const QUuid &ns, const QString &baseData)`
- `(since 6.9) QUuid createUuidV7()`
- `(since 6.6) QUuid fromBytes(const void *bytes, QSysInfo::Endian order = QSysInfo::BigEndian)`
- `QUuid fromCFUUID(CFUUIDRef uuid)`
- `QUuid fromNSUUID(const NSUUID *uuid)`
- `QUuid fromRfc4122(QByteArrayView bytes)`
- `QUuid fromString(QAnyStringView string)`
- `(since 6.6) QUuid fromUInt128(quint128 uuid, QSysInfo::Endian order = QSysInfo::BigEndian)`

### 相关非成员函数

- `size_t qHash(const QUuid &key, size_t seed = 0)`
- `bool operator!=(const QUuid &lhs, const GUID &rhs)`
- `bool operator!=(const QUuid &lhs, const QUuid &rhs)`
- `bool operator<(const QUuid &lhs, const QUuid &rhs)`
- `QDataStream & operator<<(QDataStream &s, const QUuid &id)`
- `QDebug operator<<(QDebug dbg, const QUuid &id)`
- `bool operator<=(const QUuid &lhs, const QUuid &rhs)`
- `bool operator==(const QUuid &lhs, const GUID &rhs)`
- `bool operator==(const QUuid &lhs, const QUuid &rhs)`
- `bool operator>(const QUuid &lhs, const QUuid &rhs)`
- `bool operator>=(const QUuid &lhs, const QUuid &rhs)`
- `QDataStream & operator>>(QDataStream &s, QUuid &id)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QUuid::StringFormat`

**作用与语义：**

`toString`（StringFormat）使用该枚举来控制字符串表示的格式化。可能的值有：
- `QUuid::WithBraces`：`0`;默认情况下，`toString()`返回五个十六进制字段，中间用破折号分隔，并用大括号包围。示例：{00000000-0000-0000-0000-00000000000}。
- `QUuid::WithoutBraces`：`1`;仅使用五个破折号分隔的字段，不使用大括号。示例：00000000-0000-0000-0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
- `QUuid::Id128`：`3`;仅六进制数字，无大括号或破折号。注意`QUuid`无法将此作为输入再次解析回来。

### `enum QUuid::Variant`

**作用与语义：**

该枚举定义了UUID变体字段中使用的值。变体字段中的值决定了128位值的布局。
- `QUuid::VarUnknown`：`-1`;变体未知
- `QUuid::NCS`：`0`;保留给NCS（网络计算系统）向后兼容
- `QUuid::DCE`：`2`;分布式计算环境，`QUuid`所使用的方案
- `QUuid::Microsoft`：`6`;保留给 Microsoft 向后兼容（GUID）
- `QUuid::Reserved`：`7`;预留未来定义

### `enum QUuid::Version`

**作用与语义：**

该枚举定义了UUID版本字段中使用的值。版本字段只有在变体字段中的值为`QUuid::DCE`时才有意义。
- `QUuid::VerUnknown`：`-1`;版本不详
- `QUuid::Time`：`1`;基于时间，通过使用时间戳、时钟序列和MAC网卡地址（如有）来表示节点段
- `QUuid::EmbeddedPOSIX`：`2`;DCE安全版本，内嵌POSIX UUID
- `QUuid::Name`：`Md5`;基于名称，使用所有部分的名称取值
- `QUuid::Md5`：`3`;名字别名
- `QUuid::Random`：`4`;基于随机，通过对所有部分使用随机数
- `QUuid::Sha1`：`5`;基于名称的版本，使用 SHA-1 哈希
- `QUuid::UnixEpoch`：`7`;[自6.9起]基于时间的UUID，使用自UNIX时代以来的毫秒数

### `[constexpr noexcept] QUuid::QUuid()`

**作用与语义：**

创建空UUID。`toString()`会输出空UUID为“{0000000-0000-0000-0000-00000000000}”。

### `[explicit noexcept] QUuid::QUuid(QAnyStringView text)`

**作用与语义：**

从字符串`text`创建一个QUuid对象，必须格式化为五个十六进制字段，中间用“-”分隔，例如“{xxxxxxxx-xxxx-xxxx-xxxxxxxxxxxx}”，其中每个“x”是一个十六进制数字。此处显示的大括号是可选的，但通常会包含它们。如果转换失败，则创建一个空UUID。请参见`toString()`，解释这五个十六进制字段如何映射到QUuid中的公共数据成员。
注意：在 6.3 之前的 Qt 版本中，该构造器是一个超载集，由 `QString`、`QByteArray` 和 `const char*` 组成，而不是一个构造器承担`QAnyStringView`。

### `[constexpr noexcept] QUuid::QUuid(const GUID &guid)`

**作用与语义：**

将 Windows `guid` 投射到 Qt QUuid。
警告：此功能仅适用于Windows平台。

### `[explicit noexcept, since 6.6] QUuid::QUuid(QUuid::Id128Bytes id128, QSysInfo::Endian order = QSysInfo::BigEndian)`

**作用与语义：**

基于积分`id128`参数创建QUuid。输入`id128`参数被视为字节序为`order`。

### `[constexpr noexcept] QUuid::QUuid(uint l, ushort w1, ushort w2, uchar b1, uchar b2, uchar b3, uchar b4, uchar b5, uchar b6, uchar b7, uchar b8)`

**作用与语义：**

创建由参数指定的UUID，参数为`l`、`w1`、`w2`、`b1`、`b2`、`b3`、`b4`、`b5`、`b6`、`b7`、`b8`。

**官方示例：**

```cpp
 // {67C8770B-44F1-410A-AB9A-F9B5446F13EE}
 QUuid IID_MyInterface(0x67c8770b, 0x44f1, 0x410a, 0xab, 0x9a, 0xf9, 0xb5, 0x44, 0x6f, 0x13, 0xee);
```

### `[static] QUuid QUuid::createUuid()`

**作用与语义：**

在 Windows 以外的任何平台上，该函数返回一个带有变体 `QUuid::DCE` 和版本 `QUuid::Random` 的新 UUID。在 Windows 上，GUID 是通过 Windows API 生成的，且是 API 决定创建的类型。

### `[static noexcept] QUuid QUuid::createUuidV3(QUuid ns, QByteArrayView baseData)`

**作用与语义：**

该函数返回一个带有变体`QUuid::DCE`和版本`QUuid::Md5`的新UUID。`ns`是命名空间，`baseData`是RFC 4122描述的基本数据。
注意：在 6.8 之前的 Qt 版本中，该功能采用了 `QByteArray` 的频率，而非 `QByteArrayView`。

### `[static] QUuid QUuid::createUuidV3(const QUuid &ns, const QString &baseData)`

**作用与语义：**

该函数返回一个新的UUID，带有变体`QUuid::DCE`和版本`QUuid::Md5`。`ns`是命名空间，`baseData`是RFC 4122描述的基本数据。

### `[static noexcept] QUuid QUuid::createUuidV5(QUuid ns, QByteArrayView baseData)`

**作用与语义：**

该函数返回一个带有变体`QUuid::DCE`和版本`QUuid::Sha1`的新UUID。`ns`是命名空间，`baseData`是RFC 4122描述的基本数据。
注意：在6.8之前的Qt版本中，该功能采用`QByteArray`，而非`QByteArrayView`。

### `[static] QUuid QUuid::createUuidV5(const QUuid &ns, const QString &baseData)`

**作用与语义：**

该函数返回一个带有变体`QUuid::DCE`和版本`QUuid::Sha1`的新UUID。`ns`是命名空间，`baseData`是RFC 4122描述的基本数据。

### `[static, since 6.9] QUuid QUuid::createUuidV7()`

**作用与语义：**

该函数返回一个带有变体`QUuid::DCE`和版本`QUuid::UnixEpoch`的新UUID。
它使用一个时间顺序值字段，该字段由 RFC9562 描述的 UNIX 纪元以来的毫秒数推导出来。

### `[static, since 6.6] QUuid QUuid::fromBytes(const void *bytes, QSysInfo::Endian order = QSysInfo::BigEndian)`

**作用与语义：**

使用字节顺序`order`读取`bytes`中的128位（16字节），并返回对应这些字节的`QUuid`。如果字节顺序`order` `QSysInfo::BigEndian`，该函数的作用与`fromRfc4122()`相同。

### `[static] QUuid QUuid::fromCFUUID(CFUUIDRef uuid)`

**作用与语义：**

构建包含`uuid` CFUUID副本的新`QUuid`。
注意：此功能仅在苹果平台提供。

### `[static] QUuid QUuid::fromNSUUID(const NSUUID *uuid)`

**作用与语义：**

构建包含`uuid` NSUUID 副本的新`QUuid`。
注意：此功能仅在苹果平台提供。

### `[static noexcept] QUuid QUuid::fromRfc4122(QByteArrayView bytes)`

**作用与语义：**

从 UUID 的二进制表示创建 `QUuid` 对象，如 RFC 4122 第 4.1.2 节所述。有关所需 `bytes` 顺序的进一步解释，请参见 `toRfc4122()`。
接受的字节数组不是可读格式。
如果转换失败，将创建一个空 UUID。
注意：在 Qt 6.3 之前的版本中，此函数使用 `QByteArray`，而不是 `QByteArrayView`。

### `[static noexcept] QUuid QUuid::fromString(QAnyStringView string)`

**作用与语义：**

从字符串 `string` 创建 `QUuid` 对象，该字符串必须格式化为由 '-' 分隔的五个十六进制字段，例如 "{xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx}"，其中每个 'x' 是十六进制数字。此处显示的大括号是可选的，但通常会包含它们。如果转换失败，将返回一个空 UUID。有关五个十六进制字段如何映射到 `QUuid` 中的公共数据成员，请参见 `toString()`。
注意：在 Qt 6.3 之前的版本中，此函数是由 `QStringView` 和 `QLatin1StringView` 组成的重载集，而不是一个使用 `QAnyStringView` 的函数。

### `[static constexpr noexcept, since 6.6] QUuid QUuid::fromUInt128(quint128 uuid, QSysInfo::Endian order = QSysInfo::BigEndian)`

**作用与语义：**

基于整体 `uuid` 参数创建 `QUuid`。输入的 `uuid` 参数被视为具有字节顺序 `order`。
注意：此函数仅在提供 128 位整数类型的平台上存在。

### `[constexpr noexcept] bool QUuid::isNull() const`

**作用与语义：**

如果是空UUID {0000000-0000-0000-0000-0000-00000000000000}，则返回`true`;否则返回`false`。

### `QByteArray QUuid::toByteArray(QUuid::StringFormat mode = WithBraces) const`

**作用与语义：**

返回该`QUuid`的字符串表示，格式由`mode`参数控制。从左到右，五个十六进制字段分别由`QUuid`中的四个公共数据成员得到如下：
- `Field #`：来源
- `1`：data1
- `2`：data2
- `3`：data3
- `4`：数据4[0] ..数据4[1]
- `5`：data4[2] ..data4[7]

### `[noexcept, since 6.6] QUuid::Id128Bytes QUuid::toBytes(QSysInfo::Endian order = QSysInfo::BigEndian) const`

**作用与语义：**

返回由该`QUuid`创建的128位ID，按`order`指定的字节顺序。如果顺序`QSysInfo::BigEndian`，该函数的二进制内容与`toRfc4122()`相同。详情请参见该函数。

### `CFUUIDRef QUuid::toCFUUID() const`

**作用与语义：**

从`QUuid`生成CFUUID。
调用者拥有CFUUID，并负责释放该信息。
注意：此功能仅在苹果平台提供。

### `NSUUID *QUuid::toNSUUID() const`

**作用与语义：**

从`QUuid`创建一个非标准化（NSUUID）。
非标准分级（NSUUID）为自动发布。
注意：此功能仅在苹果平台提供。

### `QByteArray QUuid::toRfc4122() const`

**作用与语义：**

返回该`QUuid`的二进制表示。字节数组采用大端序格式，格式遵循RFC 4122第4.1.2节——“布局和字节顺序”。
顺序如下：
- `Field #`：来源
- `1`：数据1
- `2`：data2
- `3`：data3
- `4`：数据4[0] ..数据4[7]
该函数返回的字节数组中包含与`toBytes()`相同的二进制内容。

### `QString QUuid::toString(QUuid::StringFormat mode = WithBraces) const`

**作用与语义：**

返回该`QUuid`的字符串表示，格式由`mode`参数控制。从左到右，五个十六进制字段分别由`QUuid`中的四个公共数据成员得到如下：
- `Field #`：来源
- `1`：data1
- `2`：data2
- `3`：data3
- `4`：数据4[0] ..数据4[1]
- `5`：data4[2] ..data4[7]

### `[constexpr noexcept, since 6.6] quint128 QUuid::toUInt128(QSysInfo::Endian order = QSysInfo::BigEndian) const`

**作用与语义：**

返回由该`QUuid`创建的128位整数，按`order`指定的字节顺序。如果顺序为`QSysInfo::BigEndian`，该函数的二进制内容与`toRfc4122()`相同。详情请参见该函数。
注意：该功能仅存在于提供128位整数类型的平台上。

### `[constexpr noexcept] QUuid::Variant QUuid::variant() const`

**作用与语义：**

返回UUID变体字段中的值。如果返回值为`QUuid::DCE`，调用`version()`查看其采用的布局。空UUID被视为未知变体。

### `[constexpr noexcept] QUuid::Version QUuid::version() const`

**作用与语义：**

如果UUID的变体字段为`QUuid::DCE`，返回UUID的版本字段。否则返回`QUuid::VerUnknown`。

### `[constexpr noexcept] QUuid::operator GUID() const`

**作用与语义：**

从`QUuid`返回一个Windows的GUID。
警告：此功能仅适用于Windows平台。

### `[constexpr noexcept] QUuid &QUuid::operator=(const GUID &guid)`

**作用与语义：**

将Windows `guid`分配给Qt `QUuid`。
警告：此功能仅适用于Windows平台。

### `[noexcept] size_t qHash(const QUuid &key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `[constexpr noexcept] bool operator!=(const QUuid &lhs, const GUID &rhs)`

**作用与语义：**

如果 `lhs` UUID 不等于 Windows GUID `rhs`，则返回 `true`；否则返回 `false`。

### `[constexpr noexcept] bool operator!=(const QUuid &lhs, const QUuid &rhs)`

**作用与语义：**

如果 `lhs` `QUuid` 和 `rhs` `QUuid` 不同，则返回 `true`；否则返回 `false`。

### `[constexpr noexcept] bool operator>=(const QUuid &lhs, const QUuid &rhs)`

**作用与语义：**

对`lhs`与`rhs`进行比较，如果`lhs`和`rhs`的相对排序对该操作正确，则返回`true`，否则`false`。注意，这些函数的排序可能不等于`toString()`创建字符串的排序，也不能等于`toBytes()`和`toRfc4122()`返回的字节数组。

### `QDataStream &operator<<(QDataStream &s, const QUuid &id)`

**作用与语义：**

将UUID `id`写入数据流 `s`。

### `QDebug operator<<(QDebug dbg, const QUuid &id)`

**作用与语义：**

将UUID `id`写入输出流，用于调试信息`dbg`。

### `[constexpr noexcept] bool operator==(const QUuid &lhs, const GUID &rhs)`

**作用与语义：**

如果 `lhs` UUID 等于 Windows GUID `rhs`，则返回 `true`；否则返回 `false`。

### `[constexpr noexcept] bool operator==(const QUuid &lhs, const QUuid &rhs)`

**作用与语义：**

如果 `lhs`、`QUuid` 与 `rhs`、`QUuid` 相同，则返回 `true`；否则返回 `false`。

### `QDataStream &operator>>(QDataStream &s, QUuid &id)`

**作用与语义：**

它会从流`s`读取UUID到`id`。

### `bool operator<(const QUuid &lhs, const QUuid &rhs)`

**作用与语义：**

对`lhs`与`rhs`进行比较，如果`lhs`和`rhs`的相对排序对该操作正确，则返回`true`，否则`false`。注意，这些函数的排序可能不等于`toString()`创建字符串的排序，也不能等于`toBytes()`和`toRfc4122()`返回的字节数组。

### `bool operator<=(const QUuid &lhs, const QUuid &rhs)`

**作用与语义：**

对`lhs`与`rhs`进行比较，如果`lhs`和`rhs`的相对排序对该操作正确，则返回`true`，否则`false`。注意，这些函数的排序可能不等于`toString()`创建字符串的排序，也不能等于`toBytes()`和`toRfc4122()`返回的字节数组。

### `bool operator>(const QUuid &lhs, const QUuid &rhs)`

**作用与语义：**

对`lhs`与`rhs`进行比较，如果`lhs`和`rhs`的相对排序对该操作正确，则返回`true`，否则`false`。注意，这些函数的排序可能不等于`toString()`创建字符串的排序，也不能等于`toBytes()`和`toRfc4122()`返回的字节数组。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

### 状态和错误边界

把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

### 线程边界

如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

### 最容易出现的错误

不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QUuid` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
