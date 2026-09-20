# QBitArray 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QBitArray>`  
> 所属模块：`Qt6::Core`  
> 类型性质：不继承 `QObject`；隐式共享的值类型；所有成员函数可重入。

## 1. QBitArray 到底解决什么问题

`QBitArray` 是 Qt 的紧凑 bit 容器。它解决的不是“如何保存几个 `bool`”，而是“如何按索引保存大量只有真/假两种状态的数据，并且能把整段状态做位运算”。

一个 `bool` 在普通容器中往往至少按一个字节存储；`QBitArray` 把八个状态压进一个字节。对象行数很多的选中标记、访问标记、权限位、功能开关、算法访问状态、协议标志字段，都是它的合适场景。

```cpp
QBitArray visited(100000);   // 100000 个访问标记，初始均为 false
visited.setBit(42);

if (visited.testBit(42)) {
    // 已访问
}
```

它的另一项长处是对整组状态直接做 `AND`、`OR`、`XOR`、`NOT`。例如，两个权限集合做按位或可以得到“任意一侧拥有的权限”；按位与可以得到“双方共同拥有的权限”。

不适合用 `QBitArray` 的情况也很明确：

- 需要频繁在中间插入、删除元素，且需要丰富的迭代器接口。
- 状态数量固定在一个机器整数范围内，例如不超过 32 或 64 个枚举标志；这时 `QFlags` 或整数 mask 往往更直观。
- 协议采用特殊的“高位优先”bit 编号，却没有先处理 bit 顺序转换。

## 2. 构建与最小用法

CMake：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

qmake：

```qmake
QT += core
```

```cpp
#include <QBitArray>

QBitArray flags(8);       // 八个 bit，默认都是 false
flags.setBit(0);
flags.setBit(3, true);
flags.clearBit(0);

const bool enabled = flags.testBit(3);
```

索引从 0 开始，合法范围始终是 `[0, size())`。`at()`、`testBit()`、`setBit()`、`clearBit()`、`toggleBit()` 和下标访问都要求索引有效；它们不是带运行时错误返回值的越界查询接口。

## 3. 核心模型：bit、字节和隐式共享

### 3.1 size 是 bit 数，不是字节数

```cpp
QBitArray flags(10);
flags.size();             // 10
```

10 个 bit 在内部至少需要 2 个字节。若要得到承载有效 bit 所需的字节数，自己计算：

```cpp
const qsizetype byteCount = (flags.size() + 7) / 8;
```

最后一个字节可能没有全部用完。例如 10 个 bit 时，第二个字节只有低 2 位有效；剩余高 6 位不是数组内容。

### 3.2 原始存储中的 bit 顺序

`bits()` 返回紧凑的内部字节数据。在每一个字节中，bit 从最低有效位向最高有效位编号：

- bit 0 是第 0 个字节的最低位。
- bit 7 是第 0 个字节的最高位。
- bit 8 是第 1 个字节的最低位。

```cpp
QBitArray bits(10);
bits.setBit(0);
bits.setBit(8);

const char *raw = bits.bits();
```

这一规则容易和网络协议文档混淆。很多协议把一个字节的最高有效位称作“第 0 位”，而 `QBitArray` 不是这种约定。拿它解析协议时，要先确认协议的字节内 bit 顺序、整数端序和字段长度；不能仅凭 `fromBits()` 就认为解析一定正确。

### 3.3 隐式共享与写时复制

`QBitArray` 是隐式共享类。拷贝通常不立即复制整段 bit 数据：

```cpp
QBitArray a(4096);
QBitArray b = a;          // 通常共享内部数据

b.setBit(1);              // 必要时 b 分离出自己的数据再写入
```

这很适合按值传参、按值返回和读多写少的工作流。但它不等于“同一个对象可被多个线程随意并发修改”。可重入只保证不同实例可由不同线程独立使用；同一个 `QBitArray` 对象的并发读写仍须由调用方同步。

## 4. 如何读写单个 bit

### 4.1 `testBit()` 和 `setBit()` 是高频路径的首选

```cpp
if (!visited.testBit(row)) {
    visited.setBit(row);
}
```

Qt 文档特别指出，从技术实现角度看，访问 bit 时 `testBit()` 和 `setBit()` 比 `operator[]` 更高效。它们也更容易表达“读标记”或“设置标记”的意图。

### 4.2 下标写入返回的是 QBitRef，不是 bool 引用

```cpp
QBitArray bits(3);
bits[0] = true;
bits[1] = false;
bits[2] = bits[0] ^ bits[1];
```

非 const `operator[]` 返回 `QBitRef`。它是“数组对象加索引”的代理对象，能转换为 `bool`，也能接收赋值；但它不是 `bool &`，因为一个 bit 不能像独立 C++ 对象那样取地址。

因此：

- 可以写 `bits[i] = true`。
- 不应把 `bits[i]` 当作长期有效的 `bool &` 保存。
- 泛型代码若硬性要求元素引用类型是 `bool &`，不适合直接套用在 `QBitArray` 上。
- 需要翻转时使用 `toggleBit(i)`，它会返回翻转前的值。

## 5. 大小、空和 null

`QBitArray` 区分 empty 与 null，这主要是 Qt 的历史兼容语义：

```cpp
QBitArray().isNull();     // true
QBitArray().isEmpty();    // true

QBitArray(0).isNull();    // false
QBitArray(0).isEmpty();   // true
```

默认构造的对象既是 null 也是 empty。显式构造 `QBitArray(0)` 是 empty，但不是 null。

日常业务中，想判断“有没有 bit”时用 `isEmpty()`。只有确实要区分“默认状态”和“显式的零长度状态”时，才应该依赖 `isNull()`。

`resize()` 扩容时会将新增 bit 初始化为 `false`；缩容时丢弃尾部 bit。`truncate(pos)` 只缩不扩：仅在 `pos < size()` 时把数组缩到 `pos` 个 bit。

## 6. 批量填充、统计与逻辑组合

### 6.1 fill 的两种语义

```cpp
QBitArray mask(8);
mask.fill(true);              // 现有 8 个 bit 全为 true
mask.fill(false, 3);          // 重建为 3 个 false bit
```

`fill(value, size)` 的 `size` 小于 0 时沿用当前长度，否则先改变数组长度再填充。范围版本的区间是左闭右开 `[begin, end)`：

```cpp
QBitArray bits(4);
bits.fill(true, 1, 3);        // 只改 bit 1、bit 2
```

### 6.2 count 的含义

`count()` 返回总 bit 数，等价于 `size()`。`count(true)` 统计 true 的数量，`count(false)` 统计 false 的数量。

### 6.3 不等长数组的位运算规则

`&`、`|`、`^` 以及对应的复合赋值运算，结果长度是两个数组中较长者的长度。较短数组不存在的位置按 false，也就是 0 参与运算。

```cpp
QBitArray a(3);
QBitArray b(2);

a.setBit(0, true);
a.setBit(2, true);        // a: 1 0 1
b.setBit(0, true);
b.setBit(1, true);        // b: 1 1

QBitArray andResult = a & b;  // 1 0 0
QBitArray orResult = a | b;   // 1 1 1
QBitArray xorResult = a ^ b;  // 0 1 1
QBitArray notResult = ~a;     // 0 1 0
```

这条长度规则很实用，但也可能掩盖业务错误。若两份权限表本应拥有相同长度，先比较 `size()` 再运算通常更可靠。

## 7. 从原始数据导入和导出

### 7.1 bits() 只提供临时只读视图

```cpp
QBitArray flags(16);
flags.setBit(0);
flags.setBit(9);

const char *data = flags.bits();
const qsizetype bytes = (flags.size() + 7) / 8;
```

`bits()` 返回的指针属于 `QBitArray` 自己：

- 空数组返回 `nullptr`。
- 返回数据只读，不可借此修改对象。
- 只应在对象未修改、未销毁的短时间内使用。
- 数组的 resize、赋值、写时复制或析构后，旧指针都应视为无效。

### 7.2 fromBits() 的 size 仍是 bit 数

```cpp
char raw[] = { char(0b00000101) };
QBitArray bits = QBitArray::fromBits(raw, 3);

// bit 0 为 true，bit 1 为 false，bit 2 为 true
```

`fromBits(data, size)` 至少要求输入有 `(size + 7) / 8` 个字节。若 `size` 不是 8 的倍数，最后一个字节仅低 `size % 8` 位会成为数组有效内容。

导入后得到的是 `QBitArray` 的值，不应假定它持续借用外部 `data` 缓冲区。外部内存的生命周期仍由调用方负责。

## 8. 转成整数：toUInt32()

`toUInt32()` 是 Qt 6.0 引入的转换 API：

```cpp
bool ok = false;
const quint32 value = bits.toUInt32(QSysInfo::LittleEndian, &ok);
```

它读取前 32 个以内的 bit，并按传入的 `QSysInfo::Endian` 解释字节顺序。

- bit 数不超过 32 时，转换成功，传入的 `ok` 会被设为 `true`。
- bit 数超过 32 时，转换失败；若提供 `ok`，它会被设为 `false`，函数返回 0。
- 若省略 `ok`，就无法区分“转换失败返回 0”和“有效值本来就是 0”。

这里的端序不能替代协议 bit 顺序判断。端序解决的是多字节整数的排列问题；协议中“一个字节内从左到右的第一个标志位”是否对应最低位，仍要按协议单独确认。

## 9. 常见场景和选择建议

### 9.1 大量行或对象的状态标记

```cpp
QBitArray selected(model->rowCount());

for (qsizetype row = 0; row < selected.size(); ++row) {
    if (shouldSelect(row))
        selected.setBit(row);
}
```

当每个对象只需要一个开关状态，`QBitArray` 比一组整数或单字节标记更节省空间。

### 9.2 动态长度的能力集合

```cpp
QBitArray remoteCapabilities(128);
QBitArray localCapabilities(128);

QBitArray common = remoteCapabilities & localCapabilities;
```

能力项数量来自服务器、插件或配置时，长度通常不是编译期常量。此时 `QBitArray` 的数组长度和整段位运算正好契合。

### 9.3 协议解析

```cpp
const QByteArray payload = socket.read(2);
const QBitArray flags = QBitArray::fromBits(payload.constData(), 16);

const bool ack = flags.testBit(0);
```

只有当协议的 bit 编号规则与 `QBitArray` 一致时，上面代码才正确。若协议是 MSB-first，需要先做字节内 bit 翻转或按协议单独读取。

## 10. 容易踩的坑

### 10.1 把 bit 数当字节数

`QBitArray(16)` 是 16 个 bit，不是 16 个字节。`fromBits()` 的第二个参数也是 bit 数。

### 10.2 保存 QBitRef 或 bits() 指针

两者都依赖 `QBitArray` 的当前对象状态。代理和指针适合立即使用，不适合跨函数、跨线程或跨数组修改保存。

### 10.3 用 isNull 判断“是否有数据”

判断空内容请用 `isEmpty()`。`isNull()` 只对默认构造语义敏感。

### 10.4 忽略最后一个字节的无效高位

数组长度非 8 的倍数时，最后一字节的部分高位不属于有效数组内容。协议比较和手工序列化必须以 `size()` 为准。

### 10.5 假设不同长度的逻辑运算会报错

它们不会报错，而是将短数组缺失位视为 0，并产生较长长度的结果。业务上要求同长度时需自行检查。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QBitArray()` | 构造 null 且 empty 的 bit 数组。 | 默认构造和 `QBitArray(0)` 都为空，但只有前者为 null。 |
| 构造 | `explicit QBitArray(qsizetype size, bool value = false)` | 构造指定数量的 bit，并全部初始化为 `value`。 | `size` 单位是 bit；默认值是 `false`。 |
| 构造 | `QBitArray(const QBitArray &other)` | 拷贝构造另一个 bit 数组。 | 隐式共享，真正写入时才可能复制数据。 |
| 构造 | `QBitArray(QBitArray &&other)` | 移动构造，接管另一个对象的内容。 | 被移动对象只保证可析构和可重新赋值。 |
| 赋值 | `operator=(const QBitArray &other)` | 将当前对象拷贝为 `other`。 | 后续修改任一副本可能触发写时复制。 |
| 赋值 | `operator=(QBitArray &&other)` | 用右值内容替换当前对象。 | 不要继续依赖被移动对象的原 bit 内容。 |
| 状态 | `qsizetype size() const` | 返回有效 bit 的总数。 | 不是内部存储的字节数。 |
| 状态 | `qsizetype count() const` | 返回 bit 总数。 | 等价于 `size()`；统计 true 数使用 `count(true)`。 |
| 状态 | `qsizetype count(bool on) const` | 统计等于 `on` 的 bit 数量。 | 只统计有效 bit，不把末尾填充位算进去。 |
| 状态 | `bool isEmpty() const` | 判断数组是否包含 0 个 bit。 | 判断业务上的空内容时优先用它。 |
| 状态 | `bool isNull() const` | 判断是否保持默认构造的 null 状态。 | null 必然 empty，empty 不一定 null。 |
| 容量 | `void resize(qsizetype size)` | 调整 bit 数量。 | 扩容新增 bit 为 false；缩容删掉尾部 bit。 |
| 容量 | `void truncate(qsizetype pos)` | 将数组最多缩短到 `pos` 个 bit。 | 仅当 `pos < size()` 时生效，不能扩容。 |
| 容量 | `void clear()` | 清空全部 bit。 | 之后 `isEmpty()` 为 true，已取得的原始指针不再可用。 |
| 读取 | `bool at(qsizetype i) const` | 返回第 `i` 个 bit。 | `i` 必须位于 `[0, size())`。 |
| 读取 | `bool testBit(qsizetype i) const` | 测试第 `i` 个 bit 是否为 true。 | 高频读取的推荐 API，索引必须有效。 |
| 下标 | `QBitRef operator[](qsizetype i)` | 返回可写 bit 的代理对象。 | 不是 `bool &`；不要长期保存 `QBitRef`。 |
| 下标 | `bool operator[](qsizetype i) const` | 返回只读 bit 值。 | 返回普通 bool，索引仍必须有效。 |
| 修改 | `void setBit(qsizetype i)` | 将第 `i` 个 bit 置为 true。 | 写入共享数组时可能触发 detach。 |
| 修改 | `void setBit(qsizetype i, bool value)` | 将第 `i` 个 bit 设为指定值。 | `true` 相当于 set，`false` 相当于 clear。 |
| 修改 | `void clearBit(qsizetype i)` | 将第 `i` 个 bit 清为 false。 | 适合表达清除标志位；索引必须有效。 |
| 修改 | `bool toggleBit(qsizetype i)` | 翻转第 `i` 个 bit。 | 返回的是翻转前的值，不是翻转后的值。 |
| 批量修改 | `bool fill(bool value, qsizetype size = -1)` | 填充整个数组；可同时指定新长度。 | `size < 0` 保持当前长度；参数单位为 bit。 |
| 批量修改 | `void fill(bool value, qsizetype begin, qsizetype end)` | 填充 `[begin, end)` 范围。 | 左闭右开；边界和顺序必须合理。 |
| 交换 | `void swap(QBitArray &other) noexcept` | 与另一个数组交换内容。 | 常数时间交换，适合无异常替换。 |
| 原始数据 | `const char *bits() const` | 返回内部紧凑字节数据的只读指针。 | 空数组为 `nullptr`；字节内低位对应较小索引；不要保存或写入。 |
| 原始数据 | `static QBitArray fromBits(const char *data, qsizetype size)` | 从紧凑字节缓冲构造数组。 | `size` 是 bit 数；输入至少有 `(size + 7) / 8` 字节。 |
| 转换 | `quint32 toUInt32(QSysInfo::Endian endianness, bool *ok = nullptr) const` | 按指定端序转换至多 32 个 bit 为 `quint32`。 | Qt 6.0 起提供；超过 32 bit 时返回 0，应用 `ok` 区分失败。 |
| 复合位运算 | `operator&=(const QBitArray &other)` | 将当前数组改为与 `other` 的按位与。 | 结果取较长长度，短数组缺失 bit 按 0。 |
| 复合位运算 | `operator&=(QBitArray &&other)` | 用右值参与按位与并写回当前对象。 | 语义同 const 引用重载，适合临时对象。 |
| 复合位运算 | `operator&#124;=(const QBitArray &other)` | 将当前数组改为与 `other` 的按位或。 | 结果取较长长度，短数组缺失 bit 按 0。 |
| 复合位运算 | `operator&#124;=(QBitArray &&other)` | 用右值参与按位或并写回当前对象。 | 语义同 const 引用重载，适合临时对象。 |
| 复合位运算 | `operator^=(const QBitArray &other)` | 将当前数组改为与 `other` 的按位异或。 | 结果取较长长度，短数组缺失 bit 按 0。 |
| 复合位运算 | `operator^=(QBitArray &&other)` | 用右值参与按位异或并写回当前对象。 | 语义同 const 引用重载，适合临时对象。 |
| 比较 | `operator==(const QBitArray &lhs, const QBitArray &rhs)` | 判断两个数组是否相等。 | 比较有效长度和 bit 内容。 |
| 比较 | `operator!=(const QBitArray &lhs, const QBitArray &rhs)` | 判断两个数组是否不相等。 | 与相等比较的结果相反。 |
| 非成员位运算 | `operator&(const QBitArray &a1, const QBitArray &a2)` | 返回两个数组的按位与结果。 | 结果长度取较长者，缺失 bit 视为 0。 |
| 非成员位运算 | `operator&(QBitArray &&a1, const QBitArray &a2)` | 右值与 const 数组按位与。 | 语义同普通按位与，主要优化临时对象。 |
| 非成员位运算 | `operator&(const QBitArray &a1, QBitArray &&a2)` | const 数组与右值按位与。 | 不要继续依赖被移动参数的旧内容。 |
| 非成员位运算 | `operator&(QBitArray &&a1, QBitArray &&a2)` | 两个右值做按位与。 | 主要服务表达式临时对象优化。 |
| 非成员位运算 | `operator&#124;(const QBitArray &a1, const QBitArray &a2)` | 返回两个数组的按位或结果。 | 结果长度取较长者，缺失 bit 视为 0。 |
| 非成员位运算 | `operator&#124;(QBitArray &&a1, const QBitArray &a2)` | 右值与 const 数组按位或。 | 语义同普通按位或，主要优化临时对象。 |
| 非成员位运算 | `operator&#124;(const QBitArray &a1, QBitArray &&a2)` | const 数组与右值按位或。 | 不要继续依赖被移动参数的旧内容。 |
| 非成员位运算 | `operator&#124;(QBitArray &&a1, QBitArray &&a2)` | 两个右值做按位或。 | 主要服务表达式临时对象优化。 |
| 非成员位运算 | `operator^(const QBitArray &a1, const QBitArray &a2)` | 返回两个数组的按位异或结果。 | 结果长度取较长者，缺失 bit 视为 0。 |
| 非成员位运算 | `operator^(QBitArray &&a1, const QBitArray &a2)` | 右值与 const 数组按位异或。 | 语义同普通按位异或，主要优化临时对象。 |
| 非成员位运算 | `operator^(const QBitArray &a1, QBitArray &&a2)` | const 数组与右值按位异或。 | 不要继续依赖被移动参数的旧内容。 |
| 非成员位运算 | `operator^(QBitArray &&a1, QBitArray &&a2)` | 两个右值做按位异或。 | 主要服务表达式临时对象优化。 |
| 非成员位运算 | `operator~(QBitArray a)` | 返回所有有效 bit 取反后的新数组。 | 只针对有效 bit；可复用右值参数的存储。 |
| 数据流 | `operator<<(QDataStream &out, const QBitArray &ba)` | 将数组写入 `QDataStream`。 | 用于 Qt 数据流序列化；跨版本格式需设置并核对流版本。 |
| 数据流 | `operator>>(QDataStream &in, QBitArray &ba)` | 从 `QDataStream` 读入数组。 | 读取后检查流状态；它不是通用网络协议解析接口。 |

## 12. 一句话总结

`QBitArray` 是“按 bit 保存动态长度状态集合”的专用值类型：它以紧凑存储和整段位运算换取效率，但代码必须明确索引边界、bit 顺序、末尾有效位和写时复制的生命周期边界。
