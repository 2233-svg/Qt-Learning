# Qt QBEInteger 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QBEInteger>`  
> 所属模块：`Qt6::Core`  
> 模板声明：`template <typename T> class QBEInteger`

## 1. 它解决的问题：让整数按大端字节序稳定存放

不同 CPU 的本机字节序可能不同。比如同一个 `quint32` 值 `0x01020304`，在大端机器内存里通常按 `01 02 03 04` 存，在小端机器内存里通常按 `04 03 02 01` 存。

网络协议、文件格式、硬件寄存器镜像、跨平台缓存和一些二进制包格式常常要求字段必须使用固定字节序。`QBEInteger<T>` 解决的就是这个问题：无论程序跑在大端还是小端平台，它在内存中保存的都是 **big-endian** 形式；读出来参与运算时，又自动转成本机整数值。

可以把它理解成“带固定存储字节序的整数包装器”：

```text
写入 QBEInteger<quint32>(0x01020304)
        ↓
内部以大端字节序存放 01 02 03 04
        ↓
operator T() 读取时返回本机整数 0x01020304
```

它的典型用途不是替代普通 `int`，而是在二进制边界明确表达：这个字段在数据格式中必须是大端。

## 2. 和普通整数、字节序函数怎么选

Qt 同时提供了 `qToBigEndian()`、`qFromBigEndian()` 这类函数。`QBEInteger` 与它们不是互相替代，而是适合不同位置：

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 普通计算 | `quint32`、`qint64` 等本机整数 | 保存程序内部数值，按 CPU 本机字节序存储。 | 最快、最自然；不要直接把内存转成网络或文件格式。 |
| 单次转换 | `qToBigEndian()` / `qFromBigEndian()` | 在读写某个字段时显式转换字节序。 | 适合从 `QByteArray`、socket 缓冲区、文件缓冲区中按偏移读写。 |
| 字段建模 | `QBEInteger<T>` | 让结构体字段或中间对象长期以大端形式存储。 | 适合描述协议头、文件头、磁盘格式字段；不要滥用于普通业务变量。 |
| 小端字段建模 | `QLEInteger<T>` | 让字段长期以 little-endian 形式存储。 | 需要小端格式时使用，语义与 `QBEInteger` 对称。 |

如果你只是从字节数组里读一个整数：

```cpp
quint32 length = qFromBigEndian<quint32>(buffer.constData() + offset);
```

如果你要定义一个“字段本身就是大端”的结构：

```cpp
struct PacketHeader
{
    quint16_be version;
    quint32_be payloadSize;
};
```

`quint16_be`、`quint32_be` 是 Qt 在 `qendian.h` 中提供的便捷 typedef，本质上就是 `QBEInteger<quint16>`、`QBEInteger<quint32>` 这类类型。

## 3. 支持哪些模板参数

模板参数 `T` 必须是 C++ 整数类型。Qt 文档列出的常见范围包括：

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 8 位整数 | `char`、`signed char`、`unsigned char`、`qint8`、`quint8` | 表示单字节字段。 | 单字节没有字节序差异，用它通常只是为了字段类型统一。 |
| 16 位整数 | `short`、`unsigned short`、`qint16`、`quint16`、`char16_t` | 表示两字节大端字段。 | 常见于协议版本、端口、短长度字段。 |
| 32 位整数 | `int`、`unsigned int`、`qint32`、`quint32`、`char32_t` | 表示四字节大端字段。 | 常见于 magic、长度、偏移、CRC。 |
| 64 位整数 | `long long`、`unsigned long long`、`qint64`、`quint64` | 表示八字节大端字段。 | 注意文件格式或协议是否真的允许 64 位范围。 |
| 平台相关整数 | `long`、`unsigned long` | 使用平台相关宽度的整数。 | 不推荐用于跨平台二进制格式，宽度可能随 ABI 改变。 |
| 指针相关整数 | `qintptr`、`quintptr`、`qptrdiff` | 表示指针宽度相关数值。 | 不适合持久文件或网络协议，32/64 位平台宽度不同。 |

跨平台格式中，优先选择 `qint16`、`quint16`、`qint32`、`quint32`、`qint64`、`quint64` 这类宽度固定的 Qt 整数类型。`long` 和指针宽度类型容易把平台差异写进数据格式。

## 4. 使用场景：把协议字段写成“可读的结构”

假设一个文件头规定如下：

```text
offset  size  endian  field
0       4     big     magic
4       2     big     version
6       2     big     headerSize
8       4     big     payloadSize
```

可以用大端字段类型表达：

```cpp
#include <QEndian>

struct FileHeader
{
    quint32_be magic;
    quint16_be version;
    quint16_be headerSize;
    quint32_be payloadSize;
};

FileHeader header;
header.magic = 0x51465431u;
header.version = 1;
header.headerSize = sizeof(FileHeader);
header.payloadSize = payload.size();

quint32 size = header.payloadSize; // 自动转回本机整数
```

这样读代码时能直接看出：这些字段不是普通本机整数，而是二进制格式要求的大端字段。

但要注意，结构体的整体布局仍受 C++ 对齐和填充规则影响。不要随手把任意网络缓冲区 `reinterpret_cast` 成结构体指针；更稳妥的做法是检查长度后用 `memcpy` 拷贝到结构体，或直接用 `qFromBigEndian()` 按偏移读取。

## 5. 它的读写模型：存储是大端，运算按本机值

`QBEInteger<T>` 的构造、赋值和复合赋值大致遵循同一个模式：

1. 写入普通整数 `T`。
2. Qt 把它转换成大端形式保存。
3. 读取或参与运算时先转回本机整数。
4. 运算结果再转换成大端形式写回。

例如：

```cpp
quint32_be count = quint32_be(10);
count += 5;

quint32 native = count; // native == 15
```

`count += 5` 不是直接对大端字节做加法；它先得到本机值 `10`，加上 `5`，再把 `15` 以大端形式存回内部字段。

这让它像普通整数一样可用，但代价是每次读写都可能发生字节序转换。Qt 文档也提醒：它可能比本机整数慢，因此只在确实需要精确字节序时使用。

## 6. 初始化与默认值

文档重点展示的构造函数是：

```cpp
explicit constexpr QBEInteger(T value);
```

推荐始终显式初始化：

```cpp
quint32_be length = quint32_be(0);
quint16_be version = quint16_be(1);
```

不要把它当作“自动清零的整数”。在 Qt 头文件实现里，底层通用存储类型存在默认构造路径；对于局部对象，如果没有做值初始化，内部整数存储可能没有你期望的业务值。协议字段尤其不该依赖未初始化状态。

## 7. 算术和位运算的边界

`QBEInteger<T>` 支持一组复合赋值、递增递减和比较运算符。它们让大端字段在代码里更顺手，但底层仍遵守 C++ 对普通整数的规则：

- 有符号整数溢出仍是 C++ 层面的风险。
- 除法和取余不能用 0 作为除数。
- 移位计数不能为负，也不能大于或等于类型位宽。
- 位运算应优先用于无符号类型，避免符号位带来的可读性问题。
- 后缀 `++` / `--` 返回修改前的副本，前缀版本返回修改后的自身引用。

Qt 6.11.1 头文件实现按运算符符号执行：`operator<<=` 做左移，`operator>>=` 做右移。写协议标志位时，通常选择 `quint16_be`、`quint32_be` 这类无符号大端类型更清楚。

## 8. 逐项 API 说明

### 8.1 `QBEInteger(T value)`

```cpp
explicit constexpr QBEInteger(T value)
```

用本机整数值构造一个大端存储整数。`explicit` 很重要：它避免普通整数在过多场合悄悄变成大端字段。

```cpp
quint32_be magic = quint32_be(0x51465431u);
```

### 8.2 `operator T() const`

```cpp
operator T() const
```

把内部大端存储转换成本机整数值返回。它让 `QBEInteger<T>` 可以放进普通计算、比较和日志输出。

```cpp
quint32 nativeLength = header.payloadSize;
```

读取时会做字节序转换；在热点循环里频繁访问同一个字段时，可以先取成本机整数再计算。

### 8.3 `operator=(T i)`

```cpp
QBEInteger<T> &operator=(T i)
```

把本机整数 `i` 写入当前对象，并以大端形式保存。返回自身引用，方便链式赋值。

### 8.4 `operator==` 与 `operator!=`

```cpp
bool operator==(QBEInteger<T> other) const
bool operator!=(QBEInteger<T> other) const
```

比较两个同类型大端整数是否表示同一个数值。比较的是字段语义上的整数值；在当前实现中，同一类型的大端存储值相同也就意味着数值相同。

如果要与普通整数比较，先显式转成本机值通常更清楚：

```cpp
if (quint32(header.magic) == 0x51465431u)
    accept();
```

### 8.5 加减乘除取余复合赋值

```cpp
QBEInteger<T> &operator+=(T i)
QBEInteger<T> &operator-=(T i)
QBEInteger<T> &operator*=(T i)
QBEInteger<T> &operator/=(T i)
QBEInteger<T> &operator%=(T i)
```

这些运算先把当前值转成本机整数，执行对应算术操作，再把结果写回大端存储。

```cpp
header.payloadSize += chunk.size();
```

它们适合维护计数、长度、偏移这类字段。除法和取余要先保证 `i != 0`。

### 8.6 位运算复合赋值

```cpp
QBEInteger<T> &operator&=(T i)
QBEInteger<T> &operator|=(T i)
QBEInteger<T> &operator^=(T i)
```

分别执行按位与、按位或、按位异或，并把结果写回大端存储。

```cpp
flags |= 0x0004u;
flags &= ~0x0002u;
```

这类操作通常用于协议标志位。建议使用无符号类型，避免符号扩展和符号位语义让代码变难读。

### 8.7 移位复合赋值

```cpp
QBEInteger<T> &operator<<=(T i)
QBEInteger<T> &operator>>=(T i)
```

分别对本机整数值做左移和右移，然后写回大端存储。

移位计数要在合法范围内。对有符号负数右移的语义也不适合作为跨平台二进制格式逻辑，协议位操作优先使用 `quint*_be`。

### 8.8 前缀和后缀递增递减

```cpp
QBEInteger<T> &operator++()
QBEInteger<T> operator++(int)
QBEInteger<T> &operator--()
QBEInteger<T> operator--(int)
```

前缀版本修改当前对象并返回自身引用；后缀版本返回修改前的值副本，然后再修改当前对象。

```cpp
++header.sequence;
quint16 old = header.sequence++;
```

后缀版本需要保留旧值，通常比前缀版本多一个副本；不需要旧值时优先用前缀写法。

### 8.9 `max()` 与 `min()`

```cpp
static constexpr QBEInteger<T> max()
static constexpr QBEInteger<T> min()
```

返回底层数值类型 `T` 能表示的最大值和最小值，并以大端整数对象返回。

```cpp
auto maxLength = quint32_be::max();
auto minOffset = qint32_be::min();
```

无符号类型的 `min()` 是 0；有符号类型的 `min()` 是该类型最小负值。它们表达的是数值范围，不是当前平台字节序。

## 9. 常见误区与排查顺序

### 9.1 误以为它提高跨平台结构体布局稳定性

`QBEInteger` 固定的是单个整数字段的字节序，不负责取消结构体 padding，也不改变成员对齐规则。如果整个结构体要直接落盘或走网络，要同时控制字段顺序、大小、对齐和版本演进。

### 9.2 误把它用于普通业务计算

普通计算使用本机整数更快、更简单。`QBEInteger` 每次读取和写入都可能做转换，适合格式边界，不适合在算法内部大量使用。

### 9.3 从原始缓冲区直接强转结构体

网络包或文件块可能未对齐，长度也可能不足。直接 `reinterpret_cast<const Header *>(data)` 容易踩到未对齐、越界和 padding 问题。需要安全解析时优先使用 `qFromBigEndian()` 按偏移读，或在确认长度和布局后 `memcpy` 到本地对象。

### 9.4 使用平台相关宽度类型定义文件格式

`QBEInteger<unsigned long>` 在不同平台可能是 32 位或 64 位。文件格式和网络协议应优先使用固定宽度类型，例如 `quint32_be`。

### 9.5 忘记初始化字段

二进制格式字段不应依赖默认构造后的偶然内容。创建结构体后，明确写入每个字段。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `explicit constexpr QBEInteger(T value)` | 用本机整数构造一个按大端字节序存储的字段。 | 构造是显式的；协议字段应明确初始化。 |
| 静态范围 | `static constexpr QBEInteger<T> max()` | 返回底层类型 `T` 的最大有限值，并包装成大端整数。 | 表示数值范围，不表示内存中字节序可见值。 |
| 静态范围 | `static constexpr QBEInteger<T> min()` | 返回底层类型 `T` 的最小有限值，并包装成大端整数。 | 无符号类型最小值为 0；有符号类型有负值下界。 |
| 转换 | `operator T() const` | 把内部大端存储转换成本机整数返回。 | 频繁读取会有转换成本，热点路径可先缓存本机值。 |
| 比较 | `bool operator==(QBEInteger<T> other) const` | 判断两个同类型大端整数表示的值是否相等。 | 只接受同包装类型；与普通整数比较时显式转成本机值更清楚。 |
| 比较 | `bool operator!=(QBEInteger<T> other) const` | 判断两个同类型大端整数表示的值是否不同。 | 与 `operator==` 语义相反；不要混用不同宽度字段。 |
| 赋值 | `QBEInteger<T> &operator=(T i)` | 把本机整数写入当前对象，并保存为大端形式。 | 写入后内存字节序固定为大端，读取时再转回本机值。 |
| 算术复合赋值 | `QBEInteger<T> &operator+=(T i)` | 当前值加上 `i`，再写回大端存储。 | 有符号溢出仍按 C++ 整数规则处理。 |
| 算术复合赋值 | `QBEInteger<T> &operator-=(T i)` | 当前值减去 `i`，再写回大端存储。 | 注意无符号下溢和有符号溢出。 |
| 算术复合赋值 | `QBEInteger<T> &operator*=(T i)` | 当前值乘以 `i`，再写回大端存储。 | 大字段长度或偏移计算要注意溢出。 |
| 算术复合赋值 | `QBEInteger<T> &operator/=(T i)` | 当前值除以 `i`，再写回大端存储。 | `i` 不能为 0。 |
| 算术复合赋值 | `QBEInteger<T> &operator%=(T i)` | 当前值对 `i` 取余，再写回大端存储。 | `i` 不能为 0；负数取余语义按 C++ 规则。 |
| 位运算复合赋值 | `QBEInteger<T> &operator&=(T i)` | 对当前值执行按位与，再写回大端存储。 | 标志位字段优先使用无符号大端类型。 |
| 位运算复合赋值 | `QBEInteger<T> &operator&#124;=(T i)` | 对当前值执行按位或，再写回大端存储。 | 用于设置标志位；表中用实体写竖线以避免 Markdown 分列。 |
| 位运算复合赋值 | `QBEInteger<T> &operator^=(T i)` | 对当前值执行按位异或，再写回大端存储。 | 适合翻转掩码位；确认掩码宽度与 `T` 一致。 |
| 移位复合赋值 | `QBEInteger<T> &operator<<=(T i)` | 对当前值左移 `i` 位，再写回大端存储。 | 移位计数必须在合法范围内。 |
| 移位复合赋值 | `QBEInteger<T> &operator>>=(T i)` | 对当前值右移 `i` 位，再写回大端存储。 | 有符号负数右移不适合写跨平台协议逻辑。 |
| 前缀递增 | `QBEInteger<T> &operator++()` | 当前值加 1，并返回修改后的自身引用。 | 不需要旧值时优先用前缀版本。 |
| 后缀递增 | `QBEInteger<T> operator++(int)` | 返回修改前副本，然后当前值加 1。 | 会产生旧值副本；只在确实需要旧值时使用。 |
| 前缀递减 | `QBEInteger<T> &operator--()` | 当前值减 1，并返回修改后的自身引用。 | 注意无符号字段从 0 递减的下溢。 |
| 后缀递减 | `QBEInteger<T> operator--(int)` | 返回修改前副本，然后当前值减 1。 | 与后缀递增一样，可能多一次副本。 |

---

### 一句话总结

`QBEInteger<T>` 是“以大端字节序存储、以本机整数语义读写”的字段包装器；它适合协议、文件和硬件数据格式边界，不适合替代普通整数做日常计算。
