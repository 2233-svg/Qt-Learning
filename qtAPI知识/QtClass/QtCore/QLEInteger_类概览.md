# Qt QLEInteger 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QLEInteger>`  
> 实际实现头文件：`<QtCore/qendian.h>`  
> 所属模块：`Qt6::Core`  
> 形式：模板别名 `QLEInteger<T>`  
> 相关类型：`QBEInteger<T>`、`qint16_le`、`qint32_le`、`qint64_le`、`quint16_le`、`quint32_le`、`quint64_le`

## 1. 先给结论：它解决什么问题

`QLEInteger<T>` 表示一个**以 little-endian（小端）形式存储、但按本机整数类型 `T` 使用的整数对象**。

它主要服务于：

- 文件格式中的固定小端字段；
- 网络协议或设备协议中明确规定的小端整数；
- 跨 CPU 架构共享的二进制结构；
- 需要让结构体字段在内存中保持明确字节序的代码。

它不是：

- 一种新的数值范围；
- 一种浮点数类型；
- 一个拥有外部缓冲区的解析 view；
- 一个自动处理结构体填充和对齐的序列化框架；
- 适合所有普通整数变量的默认替代品。

可以把它理解成：

```text
读取/写入时：值 T <-> 小端存储表示
算术运算时：小端存储表示 -> 本机 T -> 运算 -> 再存回小端
```

Qt 文档明确提醒：使用这类类型可能比使用本机整数慢，因此只有在确实需要精确字节序时才使用。

## 2. 一个最小例子

```cpp
#include <QLEInteger>

struct PacketHeader
{
    quint16_le payloadSize;
    quint32_le messageId;
};

PacketHeader makeHeader()
{
    PacketHeader header;
    header.payloadSize = 1200;
    header.messageId = 42;
    return header;
}
```

无论程序运行在小端还是大端 CPU 上：

- `payloadSize` 的逻辑值都是 `1200`；
- `messageId` 的逻辑值都是 `42`；
- 对象中的整数表示按照小端规则保存。

读取时可以直接转换为原生整数：

```cpp
const quint32 id = header.messageId;
```

## 3. 构建与包含

### 3.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

### 3.2 头文件

```cpp
#include <QLEInteger>
```

这个公开头文件导出 `<QtCore/qendian.h>` 中的定义。

### 3.3 qmake

```qmake
QT += core
```

## 4. `QLEInteger<T>` 的真实实现模型

在普通 Qt 构建中，`QLEInteger<T>` 是下面这个别名：

```cpp
template <typename T>
using QLEInteger = QSpecialInteger<QLittleEndianStorageType<T>>;
```

`QSpecialInteger` 内部保存一个底层 `T`，但写入时经过：

```cpp
qToLittleEndian(value)
```

读取时经过：

```cpp
qFromLittleEndian(storedValue)
```

因此：

- 在小端主机上，转换通常是恒等操作；
- 在大端主机上，转换会交换字节；
- 对外暴露的数值仍然是本机 `T`；
- 内部存储表示始终按小端规则维持。

头文件中的 `QLEInteger` 是公共别名；文档页为了生成 API 文档，展示了一个等价的类接口。

## 5. 哪些 `T` 可以使用

Qt 文档要求模板参数 `T` 是 C++ 整数类型，覆盖：

### 5.1 8 位

- `char`；
- `signed char`；
- `unsigned char`；
- `qint8`；
- `quint8`。

### 5.2 16 位

- `short`；
- `unsigned short`；
- `qint16`；
- `quint16`；
- `char16_t`。

### 5.3 32 位

- `int`；
- `unsigned int`；
- `qint32`；
- `quint32`；
- `char32_t`。

### 5.4 64 位

- `long long`；
- `unsigned long long`；
- `qint64`；
- `quint64`。

### 5.5 平台相关宽度

- `long`；
- `unsigned long`；
- `qintptr`；
- `quintptr`；
- `qptrdiff`。

### 5.6 选择类型时的稳定性

如果字段属于磁盘格式、网络协议或跨进程 ABI，优先使用明确宽度的类型：

```cpp
qint16_le
quint32_le
qint64_le
```

不要在需要跨平台稳定布局的格式中随意使用 `long`、`unsigned long` 或指针宽度类型，因为它们的宽度可能随平台变化。

## 6. Qt 提供的常用别名

`qendian.h` 直接提供：

```cpp
using qint16_le = QLEInteger<qint16>;
using qint32_le = QLEInteger<qint32>;
using qint64_le = QLEInteger<qint64>;

using quint16_le = QLEInteger<quint16>;
using quint32_le = QLEInteger<quint32>;
using quint64_le = QLEInteger<quint64>;
```

对应的大端别名也存在：

```cpp
using qint16_be = QBEInteger<qint16>;
using qint32_be = QBEInteger<qint32>;
using qint64_be = QBEInteger<qint64>;
```

如果字段规范是小端，优先使用带 `_le` 的别名；如果规范是大端，使用 `QBEInteger<T>` 或 `_be` 别名，不要在字段语义上混用。

## 7. 典型使用场景

### 7.1 文件格式头

```cpp
struct FileHeader
{
    quint32_le magic;
    quint16_le version;
    quint64_le dataOffset;
};
```

这里字段的逻辑访问方式与普通整数类似：

```cpp
FileHeader header;
header.magic = 0x5146494C;
header.version = 3;
header.dataOffset = 4096;
```

写入内存时，字段值的表示采用小端顺序。

### 7.2 协议字段

```cpp
struct Request
{
    quint16_le opcode;
    quint32_le sequence;
    quint32_le bodyLength;
};

bool isValid(const Request &request)
{
    return request.opcode == quint16_le(7)
        && request.bodyLength <= 1024 * 1024;
}
```

比较操作要求对方是同一个 `QLEInteger<T>` 类型，因此显式写 `quint16_le(7)` 可以让字段的类型和字节序意图清楚。

### 7.3 计数和累加

```cpp
quint32_le count = 0;
for (const auto &item : items)
    ++count;
```

每次递增都把逻辑值转换为本机 `quint32` 运算，再保存回小端表示。对热循环中的普通临时变量，这种存储转换可能没有必要；可以先使用原生整数，最后赋值给 `quint32_le`。

### 7.4 与结构体字段配合

```cpp
struct IndexEntry
{
    quint64_le offset;
    quint32_le length;
    quint16_le flags;
};

IndexEntry entry{.offset = 8192, .length = 256, .flags = 1};
```

这里要区分两个问题：

1. 字段的整数表示是否采用小端；
2. 整个结构体是否适合直接写入文件或网络。

`QLEInteger` 只解决第一个问题。结构体仍可能存在：

- 对齐填充；
- 尾部填充；
- 编译器布局差异；
- ABI 差异；
- 版本扩展问题。

因此不能仅因为每个字段都是 `_le` 就无条件使用 `write(sizeof(entry))` 把整个结构体当作稳定文件格式。

## 8. 与 `qToLittleEndian()` / `qFromLittleEndian()` 的区别

### 8.1 `QLEInteger`：字段类型化

```cpp
struct Header
{
    quint32_le length;
};
```

优点：

- 字段类型直接表达小端语义；
- 读写像普通整数；
- 适合定义固定格式结构体；
- 不需要每次访问都手动转换。

### 8.2 `qToLittleEndian()`：显式转换

```cpp
const quint32 wireValue = qToLittleEndian(hostValue);
```

适合：

- 只在写入或读取边界转换一次；
- 对未对齐的字节缓冲区进行解析；
- 不希望结构体字段带特殊整数类型；
- 需要显式控制目标地址。

### 8.3 `qFromLittleEndian(const void *)`：从字节缓冲区读取

```cpp
const quint32 value = qFromLittleEndian<quint32>(data);
```

Qt 的读取函数没有对源地址提出对齐要求，适合从网络包或文件缓冲区读取原始字节。

选择原则：

| 需求 | 更合适的方式 |
| --- | --- |
| 结构体字段本身代表小端整数 | `QLEInteger<T>` |
| 只在边界处转换一次 | `qToLittleEndian()` / `qFromLittleEndian()` |
| 原始缓冲区可能未对齐 | `qFromLittleEndian<T>(const void *)` |
| 需要大端字段 | `QBEInteger<T>` 或 `qToBigEndian()` |
| 普通本地计算变量 | 原生整数类型 |

## 9. 原生值、存储表示和对齐

### 9.1 转换后的值不是底层字节顺序

```cpp
quint32_le value = 0x01020304;
const quint32 native = value;
```

`native` 的数值是 `0x01020304`，不应把转换结果理解成“得到一个按小端排列的整数”。字节序是对象表示和序列化边界的属性，数值本身没有大小端。

### 9.2 不是未对齐整数引用

`QLEInteger<T>` 是一个对象类型，内部有存储成员。它不等价于：

```cpp
reinterpret_cast<const quint32 *>(data)
```

如果原始数据地址可能未对齐，不能把它强行 reinterpret_cast 成 `QLEInteger<T> *` 或 `quint32 *`。应使用 `qFromLittleEndian<T>(data)` 或把数据复制到正确对齐的对象中。

### 9.3 结构体布局仍然需要检查

即使每个字段的字节序明确，以下代码也不能自动得到稳定 ABI：

```cpp
struct MaybePadded
{
    quint8 tag;
    quint32_le value;
};
```

编译器可能在 `tag` 和 `value` 之间加入填充。要定义跨平台格式，应明确序列化字段，或者用静态断言、布局测试和固定的读写代码验证。

## 10. 算术操作的共同语义

`QLEInteger<T>` 的复合赋值运算符都接受原生 `T`：

```cpp
quint32_le value = 10;
value += 5;
value *= 2;
value >>= 1;
```

每个操作大致遵循：

```cpp
T native = static_cast<T>(value);
native = native OP i;
value = native;
```

因此，运算的溢出、除零、移位计数和有符号整数规则应按 C++ 原生 `T` 理解，而不是按“字节数组操作”理解。

### 10.1 无符号溢出

```cpp
quint8_le value = quint8_le::max();
++value;
```

无符号 `T` 的算术按无符号整数规则回绕。结果仍会以小端表示保存。

### 10.2 有符号溢出

```cpp
qint32_le value = qint32_le::max();
++value; // 不要依赖有符号溢出的结果
```

有符号整数溢出不是可靠的回绕机制，行为不应被业务代码依赖。

### 10.3 除法和取模

```cpp
quint32_le value = 10;
value /= 3;
value %= 2;
```

除数为零时仍然是原生整数的非法操作。对有符号类型，还要注意最小值除以 `-1` 的边界。

### 10.4 移位

```cpp
quint32_le value = 1;
value <<= 8;
value >>= 2;
```

`<<=` 就是左移，`>>=` 就是右移。移位量必须符合 C++ 对 `T` 的规则；不要传入负数或大于等于位宽的值。

Qt 6.11.1 的类文档在这两个成员的描述文字中把“left-shift”和“right-shift”写反了，但头文件实现和运算符名称给出的实际语义是：

- `operator<<=`：左移；
- `operator>>=`：右移。

## 11. `max()` 和 `min()`

### 11.1 `max()`

```cpp
constexpr auto maxValue = quint32_le::max();
```

返回 `T` 能表示的最大有限值，并包装为 `QLEInteger<T>`。

```cpp
static_assert(static_cast<quint32>(quint32_le::max())
              == std::numeric_limits<quint32>::max());
```

### 11.2 `min()`

```cpp
constexpr auto minValue = qint32_le::min();
```

返回 `T` 能表示的最小有限值：

- 对有符号类型是最小负值；
- 对无符号类型是 `0`。

它不是“绝对值最小的正数”，也不是浮点的最小正数。

## 12. 类型转换和比较

### 12.1 转换为原生整数

```cpp
quint32_le stored = 42;
quint32 native = stored;
```

`operator T() const` 返回按本机语义解释的原生 `T`。读取时会进行从小端存储表示到主机值的转换。

需要显式表达转换时可以写：

```cpp
const auto native = static_cast<quint32>(stored);
```

### 12.2 构造是显式的

```cpp
quint32_le a(42);
quint32_le b = 42; // 不要假设所有编译配置下都接受这种隐式初始化
```

构造函数是 `explicit constexpr`。推荐直接写：

```cpp
quint32_le b(42);
```

或：

```cpp
auto b = quint32_le(42);
```

### 12.3 赋值接受原生 `T`

```cpp
quint32_le value;
value = 42;
```

赋值会把 `42` 按小端存储规则写入对象，并返回当前对象引用。

### 12.4 相等比较只列出同类型包装器

```cpp
quint32_le lhs = 10;
quint32_le rhs = 10;

if (lhs == rhs)
    handleEqual();
```

公开接口是：

```cpp
bool operator==(QLEInteger<T> other) const;
bool operator!=(QLEInteger<T> other) const;
```

如果一侧是原生整数，显式包装通常最清楚：

```cpp
if (lhs == quint32_le(10))
    handleEqual();
```

## 13. 前缀和后缀递增/递减

### 13.1 前缀 `++`

```cpp
quint32_le value = 7;
quint32_le &ref = ++value;
```

先递增，再返回当前对象引用。

### 13.2 后缀 `++`

```cpp
quint32_le value = 7;
quint32_le old = value++;
```

返回递增前的旧值副本，再把当前对象加一。头文件的实际返回类型是 `QLEInteger<T>`，不是引用。

### 13.3 前缀和后缀 `--`

```cpp
--value; // 先减一，返回引用
value--; // 返回旧值副本，再减一
```

如果只需要修改，不需要旧值，前缀形式通常更直接。

## 14. 复合赋值 API

### 14.1 加法 `operator+=`

```cpp
value += increment;
```

按原生 `T` 的加法规则更新值，并返回 `QLEInteger<T> &`。

### 14.2 减法 `operator-=`

```cpp
value -= decrement;
```

按原生 `T` 的减法规则更新值。

### 14.3 乘法 `operator*=`

```cpp
value *= factor;
```

按原生 `T` 的乘法规则更新值。注意有符号溢出风险。

### 14.4 除法 `operator/=`

```cpp
value /= divisor;
```

按原生 `T` 的整数除法规则更新值。除数不能为零。

### 14.5 取模 `operator%=`

```cpp
value %= divisor;
```

按原生 `T` 的取模规则更新值。除数不能为零。

### 14.6 左移 `operator<<=`

```cpp
value <<= shift;
```

将逻辑值左移 `shift` 位。移位量必须合法。

### 14.7 右移 `operator>>=`

```cpp
value >>= shift;
```

将逻辑值右移 `shift` 位。对有符号类型，右移负值的具体结果按 C++ 规则理解，不要把它当作跨语言的固定二进制操作。

### 14.8 按位或 `operator|=`

```cpp
value |= mask;
```

按位 OR 后保存结果。常用于位标志。

### 14.9 按位与 `operator&=`

```cpp
value &= mask;
```

按位 AND 后保存结果。

### 14.10 按位异或 `operator^=`

```cpp
value ^= mask;
```

按位 XOR 后保存结果。

所有这些运算都只改变当前 `QLEInteger` 对象，不改变传入的原生 `T` 参数。

## 15. 固定格式结构体的正确姿势

### 15.1 字段类型表达协议字节序

```cpp
struct Record
{
    quint32_le type;
    quint16_le flags;
    quint64_le timestamp;
};
```

字段访问仍然像整数：

```cpp
record.type = 2;
record.flags |= 0x04;
const quint64 timestamp = record.timestamp;
```

### 15.2 不要直接假设整个结构体可转储

以下代码可能存在问题：

```cpp
file.write(reinterpret_cast<const char *>(&record), sizeof(record));
```

风险包括：

- 成员间填充；
- 结构体尾部填充；
- 不同编译器 ABI；
- 未来版本新增字段；
- 文件格式需要校验和、对齐或长度字段；
- 原生 `struct` 对象生命周期和对象表示不等于字节协议。

更稳妥的做法是逐字段写入：

```cpp
writeLittleEndian(record.type);
writeLittleEndian(record.flags);
writeLittleEndian(record.timestamp);
```

或者明确定义二进制格式并对 `sizeof`、`alignof`、字段偏移和端到端字节结果做测试。

### 15.3 对齐和原始缓冲区

如果输入来自网络或文件：

```cpp
const quint32 length = qFromLittleEndian<quint32>(data);
```

不要把任意 `data` 地址 reinterpret_cast 成 `const quint32 *`。`qFromLittleEndian(const void *)` 的接口就是为可能未对齐的源数据准备的。

`QLEInteger<T>` 更适合已经进入对象字段或已正确构造的结构体成员，不是任意裸缓冲区的读取指针。

## 16. 与大端类型 `QBEInteger` 的区别

```cpp
quint32_le little = 1;
quint32_be big = 1;
```

二者逻辑值都为 `1`，但对象中的存储表示不同：

- `QLEInteger<T>`：小端；
- `QBEInteger<T>`：大端。

不要用主机当前字节序来替代协议规定的字节序。即使程序目前只运行在小端 CPU 上，明确使用 `_le` 仍然可以把协议契约写进类型。

## 17. 性能和适用边界

### 17.1 适合格式字段，不适合所有局部变量

```cpp
quint32_le fileLength; // 适合作为格式字段
quint32 accumulator;   // 局部计算通常用原生整数
```

如果局部循环频繁执行算术，使用原生整数通常更直接；在读写格式边界时再转换为 `QLEInteger` 或调用 endian 函数。

### 17.2 访问可能包含转换成本

在大端主机上，每次从字段读取或写回都可能发生字节交换。即使在小端主机上，包装类型也可能让编译器生成与普通整数不同的代码。Qt 文档因此建议只有在需要确定字节序时使用。

### 17.3 不要把“类型安全”误解成“格式完整性”

`QLEInteger` 能表达字段的整数宽度和字节序，但不能自动表达：

- 字段是否存在；
- 长度是否合理；
- 魔数是否正确；
- 校验和是否通过；
- 结构体是否没有填充；
- 文件版本是否兼容。

这些仍需要协议层代码负责。

## 18. 常见误区与排查顺序

### 18.1 把 QLEInteger 当作 `quint32` 的别名

它的逻辑值使用方式类似 `quint32`，但存储表示不同。需要对外暴露普通数值时显式转换：

```cpp
const quint32 value = field;
```

### 18.2 直接 reinterpret_cast 裸字节

裸缓冲区可能未对齐，也可能不是一个活跃的 `QLEInteger<T>` 对象。使用 `qFromLittleEndian<T>()` 读取。

### 18.3 以为结构体没有填充

字段类型带 `_le` 不会删除编译器的 padding。不要未经验证就把整个结构体当文件格式。

### 18.4 用 `long` 表达固定格式字段

`long` 的宽度是平台相关的。需要稳定格式时使用 `qint16`、`qint32`、`qint64` 对应的 `_le` 别名。

### 18.5 把有符号整数当作无符号位容器

位运算 API 可以用于有符号类型，但移位、溢出和右移负数的语义仍受 C++ 有符号整数规则影响。纯位字段优先使用对应的无符号类型。

### 18.6 忘记除零和移位边界

`/=`、`%=` 的右操作数不能为零；`<<=`、`>>=` 的移位量必须满足原生 `T` 的规则。

### 18.7 混淆 `<<=` 和 `>>=`

实际语义是：

- `<<=` 左移；
- `>>=` 右移。

不要按 Qt 6.11.1 类页中相反的描述文字编写代码。

### 18.8 把 `min()` 当作最小正数

对于有符号整数，`min()` 是最负的可表示值；对于无符号整数是 `0`。

## 19. 逐项 API 说明

### 19.1 `QLEInteger(T value)`

```cpp
explicit constexpr QLEInteger(T value);
```

以逻辑值 `value` 构造小端整数对象。构造函数是显式的，适合写：

```cpp
quint32_le value(42);
```

它不会改变 `value` 变量本身，只把值转换为小端存储表示。

### 19.2 `max()`

```cpp
static constexpr QLEInteger<T> max();
```

返回 `T` 的最大有限值，结果仍是 `QLEInteger<T>` 包装对象。

### 19.3 `min()`

```cpp
static constexpr QLEInteger<T> min();
```

返回 `T` 的最小有限值，结果仍是 `QLEInteger<T>` 包装对象。

### 19.4 `operator T() const`

```cpp
operator T() const;
```

把当前小端存储转换为本机 `T` 并返回。该转换允许对象在需要 `T` 的表达式中参与计算，但复杂表达式中建议显式转换以保持字节序边界清楚。

### 19.5 `operator=(T i)`

```cpp
QLEInteger<T> &operator=(T i);
```

把逻辑值 `i` 存入当前对象，并返回当前对象引用。

### 19.6 `operator==(QLEInteger<T> other)`

```cpp
bool operator==(QLEInteger<T> other) const;
```

比较两个同类型小端整数的逻辑值是否相等。

### 19.7 `operator!=(QLEInteger<T> other)`

```cpp
bool operator!=(QLEInteger<T> other) const;
```

比较两个同类型小端整数的逻辑值是否不相等。

### 19.8 `operator+=(T i)`

```cpp
QLEInteger<T> &operator+=(T i);
```

按 `T` 的加法规则累加 `i`，然后把结果重新按小端存储。

### 19.9 `operator-=(T i)`

```cpp
QLEInteger<T> &operator-=(T i);
```

按 `T` 的减法规则减去 `i`。

### 19.10 `operator*=(T i)`

```cpp
QLEInteger<T> &operator*=(T i);
```

按 `T` 的乘法规则乘以 `i`。

### 19.11 `operator/=(T i)`

```cpp
QLEInteger<T> &operator/=(T i);
```

按 `T` 的整数除法规则除以 `i`。`i == 0` 时不能调用。

### 19.12 `operator%=(T i)`

```cpp
QLEInteger<T> &operator%=(T i);
```

按 `T` 的取模规则处理 `i`。`i == 0` 时不能调用。

### 19.13 `operator<<=(T i)`

```cpp
QLEInteger<T> &operator<<=(T i);
```

将逻辑值左移 `i` 位。移位量必须合法。

### 19.14 `operator>>=(T i)`

```cpp
QLEInteger<T> &operator>>=(T i);
```

将逻辑值右移 `i` 位。对有符号类型，具体结果遵循本机 C++ 整数规则。

### 19.15 `operator|=(T i)`

```cpp
QLEInteger<T> &operator|=(T i);
```

执行按位 OR。

### 19.16 `operator&=(T i)`

```cpp
QLEInteger<T> &operator&=(T i);
```

执行按位 AND。

### 19.17 `operator^=(T i)`

```cpp
QLEInteger<T> &operator^=(T i);
```

执行按位 XOR。

### 19.18 前缀 `operator++()`

```cpp
QLEInteger<T> &operator++();
```

先递增，再返回当前对象引用。

### 19.19 前缀 `operator--()`

```cpp
QLEInteger<T> &operator--();
```

先递减，再返回当前对象引用。

### 19.20 后缀 `operator++(int)`

```cpp
QLEInteger<T> operator++(int);
```

返回修改前的对象副本，然后递增当前对象。

### 19.21 后缀 `operator--(int)`

```cpp
QLEInteger<T> operator--(int);
```

返回修改前的对象副本，然后递减当前对象。

## API 速查表
### 20.1 类型与构造

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QLEInteger<T>` | 以小端表示保存 `T` 类型整数。 | 只在需要固定小端表示时使用。 |
| `QLEInteger(T value)` | 用逻辑值构造对象。 | `explicit constexpr`；构造时执行小端存储转换。 |
| `operator T() const` | 读取为本机整数。 | 结果是数值 `T`，不是小端字节数组。 |

### 20.2 边界值

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `static constexpr QLEInteger<T> max()` | 返回 `T` 的最大有限值。 | 返回包装对象；转为 `T` 后再与原生值比较。 |
| `static constexpr QLEInteger<T> min()` | 返回 `T` 的最小有限值。 | 有符号类型是最负值；无符号类型为零。 |

### 20.3 赋值与比较

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QLEInteger<T> &operator=(T i)` | 写入逻辑值。 | 结果按小端保存。 |
| `bool operator==(QLEInteger<T> other) const` | 比较同类型包装整数是否相等。 | 需要与原生值比较时显式构造包装值。 |
| `bool operator!=(QLEInteger<T> other) const` | 比较同类型包装整数是否不等。 | 比较的是逻辑值。 |

### 20.4 算术和位运算

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QLEInteger<T> &operator+=(T i)` | 加法复合赋值。 | 遵循 `T` 的溢出规则。 |
| `QLEInteger<T> &operator-=(T i)` | 减法复合赋值。 | 有符号溢出不要依赖。 |
| `QLEInteger<T> &operator*=(T i)` | 乘法复合赋值。 | 结果重新存为小端。 |
| `QLEInteger<T> &operator/=(T i)` | 整数除法复合赋值。 | `i` 不能为零。 |
| `QLEInteger<T> &operator%=(T i)` | 取模复合赋值。 | `i` 不能为零。 |
| `QLEInteger<T> &operator<<=(T i)` | 左移复合赋值。 | 移位量必须合法。 |
| `QLEInteger<T> &operator>>=(T i)` | 右移复合赋值。 | 有符号右移遵循 C++ 规则。 |
| `QLEInteger<T> &operator|=(T i)` | 按位 OR。 | 位掩码优先使用无符号 `T`。 |
| `QLEInteger<T> &operator&=(T i)` | 按位 AND。 | 不改变字节序契约。 |
| `QLEInteger<T> &operator^=(T i)` | 按位 XOR。 | 结果按小端保存。 |

### 20.5 自增和自减

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QLEInteger<T> &operator++()` | 前缀递增。 | 先改值，返回引用。 |
| `QLEInteger<T> &operator--()` | 前缀递减。 | 先改值，返回引用。 |
| `QLEInteger<T> operator++(int)` | 后缀递增。 | 返回旧值副本，再修改当前对象。 |
| `QLEInteger<T> operator--(int)` | 后缀递减。 | 返回旧值副本，再修改当前对象。 |

### 20.6 常用别名

| 别名 | 等价类型 | 典型用途 |
| --- | --- | --- |
| `qint16_le` | `QLEInteger<qint16>` | 16 位有符号小端字段。 |
| `qint32_le` | `QLEInteger<qint32>` | 32 位有符号小端字段。 |
| `qint64_le` | `QLEInteger<qint64>` | 64 位有符号小端字段。 |
| `quint16_le` | `QLEInteger<quint16>` | 16 位无符号小端字段。 |
| `quint32_le` | `QLEInteger<quint32>` | 32 位无符号小端字段。 |
| `quint64_le` | `QLEInteger<quint64>` | 64 位无符号小端字段。 |

## 21. 一段完整的格式字段示例

```cpp
#include <QLEInteger>

struct ChunkHeader
{
    quint32_le magic;
    quint16_le version;
    quint16_le flags;
    quint64_le payloadSize;
};

ChunkHeader makeHeader(quint64 size)
{
    ChunkHeader header;
    header.magic = 0x43484E4B;
    header.version = 1;
    header.flags = 0;
    header.payloadSize = size;
    return header;
}

bool accepts(const ChunkHeader &header)
{
    return header.magic == quint32_le(0x43484E4B)
        && header.version == quint16_le(1)
        && header.payloadSize <= 64 * 1024 * 1024;
}
```

这个例子展示的是字段语义，不代表整个 `ChunkHeader` 可以未经布局验证直接写入磁盘。真正的文件格式仍应有明确的序列化和兼容策略。

## 22. 最后的选型规则

1. 需要固定小端字段时使用 `QLEInteger<T>` 或 `_le` 别名。
2. 需要固定大端字段时使用 `QBEInteger<T>` 或 `_be` 别名。
3. 只在边界转换一次时，优先考虑 `qToLittleEndian()`/`qFromLittleEndian()`。
4. 解析未对齐裸缓冲区时，不要直接 reinterpret_cast，使用 `qFromLittleEndian<T>()`。
5. 固定格式优先使用 `qint16`、`qint32`、`qint64` 等明确宽度类型。
6. 普通本地临时计算不要无理由替换成 QLEInteger。
7. `QLEInteger` 解决整数的字节序，不解决结构体 padding、版本、校验和或完整序列化。
8. `<<=` 是左移，`>>=` 是右移；Qt 6.11.1 类页中的两句说明文字写反了。

`QLEInteger` 的核心价值是把“小端存储”写进字段类型，同时保留接近原生整数的访问和运算方式。它适合协议和文件格式边界，不应被误当作通用整数优化或完整二进制序列化方案。
