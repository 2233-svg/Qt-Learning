# Qt qfloat16 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QFloat16>`  
> 所属模块：`Qt6::Core`  
> 类型性质：16 位 IEEE 754 binary16 存储类型、POD 风格、可哈希、部分可比较

## 1. qfloat16 解决什么问题

`qfloat16` 用 16 位浮点格式保存数值。它的主要价值不是让 CPU 上的普通数学运算“自动变快”，而是在数据量很大、存储或带宽更重要时，用更小的表示保存可接受精度的数据：

- 神经网络权重、激活值或推理输入；
- 图像、深度图、HDR 或纹理数据；
- 传感器批量数据和内存中的数值缓存；
- GPU、DSP 或其他支持 half 数据的设备接口；
- 明确规定 IEEE 754 binary16 编码的二进制文件和协议。

它的核心取舍是：

```text
更少的存储空间和带宽
        +
更低的有效精度和更窄的动态范围
        |
        v
适合存储，计算时通常转成 float
```

Qt 文档明确把 `qfloat16` 定位为 half-precision 的存储类型。对 `qfloat16` 做算术时，值会先转换成 `float`；具体运算结果再根据运算符重载转换成相应的结果类型。因此不要把它当作“所有数学表达式都在 16 位上高效执行”的类型。

## 2. binary16 的表示能力

`qfloat16` 遵循 IEEE 754 half-precision 格式：

| 属性 | binary16 |
| --- | --- |
| 总位数 | 16 |
| 符号位 | 1 |
| 指数位 | 5 |
| 显式尾数位 | 10 |
| 有效精度 | 11 位二进制有效位，约 3 位十进制有效数字 |
| 最大有限值 | 65504 |
| 最小正规格正数 | 约 `6.10352e-5` |
| 最小正非正规格数 | 约 `5.96046e-8` |
| `epsilon()` | `2^-10`，约 `0.0009765625` |

格式还支持：

- 正零和负零；
- 正负无穷；
- quiet NaN，以及平台实现支持的 signaling NaN；
- subnormal 非正规格数；
- normal 正规格有限数。

这意味着很多 `float` 能表示的数，在转成 `qfloat16` 时会被舍入、变成 subnormal、变成零，或者溢出成无穷。转换不是无损压缩。

```cpp
const qfloat16 stored = 0.1f;
const float recovered = static_cast<float>(stored);

// recovered 通常不等于 0.1f 的二进制 float 原值。
```

如果协议要求保留原始 `float` 精度，不能用 `qfloat16` 作为中间存储。

## 3. 构造、转换和未初始化对象

### 3.1 默认构造

```cpp
qfloat16 zero;
Q_ASSERT(qIsNull(zero));
```

默认构造得到零值。它适合用于需要值初始化的容器元素或普通局部变量。

### 3.2 从浮点或整数构造

```cpp
qfloat16 fromFloat = 1.25f;
qfloat16 fromDouble = qfloat16(1.25);
qfloat16 fromInt = qfloat16(3);
```

`float` 是最接近的通用计算类型。头文件在不同平台上用 native half 类型或 `float` 作为 `NearestFloat`，并为其他算术类型提供显式构造。为了让舍入边界清楚，业务代码可以显式写出转换：

```cpp
const qfloat16 value = qfloat16(static_cast<float>(input));
```

### 3.3 `Qt::Uninitialized`

Qt 6.1 起可以使用：

```cpp
qfloat16 value(Qt::Uninitialized);
```

这种构造不会初始化数值。读取它、参与计算或把它当作零使用，都是错误的；必须在读取前写入有效的 `qfloat16` 值。

它主要用于下面这类“即将由批量转换函数填满”的缓冲区：

```cpp
QVector<qfloat16> halfValues(count, Qt::Uninitialized);
qFloatToFloat16(halfValues.data(), floats.constData(), count);
```

如果只是声明一个普通数值，不要使用未初始化构造来省略初始化成本，因为后续读取未初始化值会产生未定义行为。

### 3.4 转回 float

```cpp
const float value = static_cast<float>(halfValue);
```

`qfloat16` 可以转换到它的平台 nearest floating type；非 native 实现通常表现为转换到 `float`。业务代码用 `static_cast<float>` 更清楚，也能减少重载解析的意外。

`qfloat16` 没有公开的“取得原始 16 位编码”的成员函数。不要把对象地址直接 `reinterpret_cast` 成 `quint16 *` 来实现协议序列化；使用 `QDataStream` 或明确的协议编码层。

## 4. qfloat16 不是普通的计算类型

### 4.1 两个 qfloat16 运算

对两个 `qfloat16` 做 `+`、`-`、`*`、`/` 时，运算过程先提升到 `NearestFloat`，结果再构造成 `qfloat16`：

```cpp
qfloat16 a = 1.1f;
qfloat16 b = 2.2f;
qfloat16 c = a + b; // 结果类型是 qfloat16，再次舍入到 binary16
```

因此连续执行很多步 qfloat16 运算，会在每次结果保存时损失 half 精度：

```cpp
qfloat16 sum = 0.0f;
for (qfloat16 value : values)
    sum += value;
```

如果这是数值敏感的累加，应改用 `float` 或 `double` 累加，最后一步再转成 `qfloat16`：

```cpp
float sum = 0.0f;
for (qfloat16 value : values)
    sum += static_cast<float>(value);

const qfloat16 storedSum = sum;
```

### 4.2 与 float、double 和整数混合

Qt 为 `qfloat16` 提供了与多种浮点和整数类型的混合算术重载。常见结果类型如下：

```cpp
qfloat16 h = 1.0f;

auto a = h + h;       // qfloat16
auto b = h + 1.0f;   // float
auto c = h + 1.0;     // double
auto d = h + 1;       // double
```

具体代码不要只凭 `auto` 猜结果类型。需要稳定 API 或模板行为时，显式转换：

```cpp
const float result = static_cast<float>(h) + inputFloat;
```

与 `float` 或更宽浮点类型混合，通常是把 `qfloat16` 作为低精度输入提升后计算；与整数混合的 Qt 重载返回 `double`，不是 `qfloat16`。

### 4.3 复合赋值会回到 half

与 `float`、`double`、`long double` 和 native floating type 的 `+=`、`-=`、`*=`、`/=` 会把运算结果重新赋值回 `qfloat16`：

```cpp
qfloat16 value = 1.0f;
value += 0.1f; // 运算可在 float 中进行，但最终回存为 qfloat16
```

这仍然有每一步舍入问题。不要因为右侧是 `float` 就以为 `value` 会保留 float 精度。

## 5. 溢出、下溢和舍入

从 `float` 或 `double` 转到 `qfloat16` 时可能发生：

- 舍入到相邻可表示的 half 值；
- 很小的非零数变成 subnormal 或零；
- 大于最大有限值的数变成无穷；
- NaN 保持 NaN 类别，但具体 payload 不应当作为跨平台协议值依赖。

```cpp
const qfloat16 tooLarge = qfloat16(100000.0f);
if (qIsInf(tooLarge))
    qWarning() << "half precision overflow";
```

如果应用需要检查压缩后的数值是否仍然可用，应在转换后检查 `qIsFinite()`、范围或业务误差，而不是只检查转换前的 `float`。

`std::numeric_limits<qfloat16>` 已由 Qt 提供特化，可以用它查询边界：

```cpp
const qfloat16 maxValue =
    std::numeric_limits<qfloat16>::max();
const qfloat16 minNormal =
    std::numeric_limits<qfloat16>::min();
```

注意 `min()` 是最小正规格正数，不是最小正 subnormal；需要最小 subnormal 时使用 `denorm_min()`。

## 6. 分类：有限数、无穷、NaN 和正规数

### 6.1 基本分类函数

```cpp
if (qIsNaN(value)) {
    // NaN
} else if (qIsInf(value)) {
    // 正无穷或负无穷
} else if (qIsFinite(value)) {
    // 有限数，包括零、subnormal 和 normal
}
```

成员函数与全局辅助函数对应：

| 成员 | 对应辅助函数 | 含义 |
| --- | --- | --- |
| `isInf()` | `qIsInf()` | 是否为无穷 |
| `isNaN()` | `qIsNaN()` | 是否为 NaN |
| `isFinite()` | `qIsFinite()` | 是否为有限数 |
| `fpClassify()` | `qFpClassify()` | 返回浮点分类 |
| `isNormal()` | 无同名全局函数 | 是否为有限且正规格的数 |

### 6.2 `isNormal()` 不等于“不是 NaN”

`isNormal()` 只有在值是有限数且处于 normal 形式时才返回 true。它对以下值返回 false：

- 正零和负零；
- subnormal；
- 正负无穷；
- NaN。

```cpp
if (value.isNormal()) {
    // 可用于需要正规格有限数的算法
}
```

如果只想判断“不是 NaN 且不是无穷”，使用 `qIsFinite()`；如果还要排除零和 subnormal，才使用 `isNormal()`。

### 6.3 `qFpClassify()`

```cpp
switch (qFpClassify(value)) {
case FP_NAN:
    break;
case FP_INFINITE:
    break;
case FP_ZERO:
    break;
case FP_SUBNORMAL:
    break;
case FP_NORMAL:
    break;
}
```

返回值使用 C/C++ 浮点分类宏。它适合需要区分 zero、subnormal、normal、infinity 和 NaN 的底层数值代码。

## 7. 符号位、负零和 copysign

Qt 6.11 起提供 qfloat16 的 `signbit()` 和非成员 `copysign()`：

```cpp
const qfloat16 magnitude = qfloat16(3.0f);
const qfloat16 negative =
    copysign(magnitude, qfloat16(-0.0f));

if (signbit(negative))
    qInfo() << "negative sign bit";
```

`signbit()` 检查的是符号位，因此对负零、负无穷和负 NaN 也会返回 true。它不是“数值是否小于零”的替代品：

```cpp
qfloat16 negativeZero = qfloat16(-0.0f);
Q_ASSERT(signbit(negativeZero));
Q_ASSERT(!(negativeZero < qfloat16(0.0f)));
```

旧的成员函数：

```cpp
const qfloat16 result = value.copySign(sign);
```

在 Qt 6.11 文档中已经 deprecated，新代码使用：

```cpp
const qfloat16 result = copysign(value, sign);
```

## 8. 比较和 NaN 的边界

`qfloat16` 是 partially comparable。它可以与 qfloat16、`float`、`double`、`long double` 以及多种整数类型比较，但 NaN 会让比较结果进入 unordered 状态：

```cpp
const qfloat16 nan =
    std::numeric_limits<qfloat16>::quiet_NaN();

Q_ASSERT(qIsNaN(nan));
Q_ASSERT(!(nan == nan));
Q_ASSERT(!(nan < qfloat16(1.0f)));
Q_ASSERT(!(nan > qfloat16(1.0f)));
```

需要三路比较时：

```cpp
const Qt::partial_ordering order =
    compareThreeWay(left, right);

if (order == Qt::partial_ordering::unordered) {
    // 至少一个操作数是 NaN
}
```

不要把 NaN 放进要求严格全序的排序逻辑后就假设算法自然正确。需要排序、去重或作为 map key 时，先定义 NaN 的业务策略：

- 拒绝 NaN；
- 将所有 NaN 归到一个明确的末端；
- 先按浮点分类再按数值比较；
- 或把原始编码当作专门的 bit key。

`qFuzzyCompare()` 也不是 NaN 处理函数；遇到 NaN 时应先做分类判断。

## 9. 批量转换：qFloatToFloat16 和 qFloatFromFloat16

逐个构造 `qfloat16` 适合少量数据。大数组转换应使用 Qt 提供的批量函数：

```cpp
QVector<qfloat16> halfValues(values.size(),
                              Qt::Uninitialized);
qFloatToFloat16(halfValues.data(),
                values.constData(),
                values.size());

QVector<float> restored(values.size());
qFloatFromFloat16(restored.data(),
                  halfValues.constData(),
                  halfValues.size());
```

两个函数都要求输入和输出数组已经分配至少 `len` 个元素：

```cpp
void qFloatToFloat16(qfloat16 *out,
                     const float *in,
                     qsizetype len) noexcept;

void qFloatFromFloat16(float *out,
                       const qfloat16 *in,
                       qsizetype len) noexcept;
```

边界：

- Qt 不会替调用方分配数组；
- `len` 必须与两个数组的有效容量匹配；
- 输入和输出指针必须在整个调用期间有效；
- 不要假设重叠缓冲区一定被支持，转换时使用独立的输入输出区域；
- 函数不返回错误，非法指针或不足容量会变成调用方的内存错误；
- 文档说明它比逐个转换更快，并且在 x86/x86-64 上可运行时检测 F16C。

在 x86/x86-64 上，直接逐个转换是否使用硬件指令取决于编译选项；批量转换函数可以自行做运行时 F16C 检测。即使使用硬件转换，精度和 binary16 舍入规则也不会改变。

## 10. 数值辅助函数

### 10.1 `qSqrt()`

```cpp
const qfloat16 root = qSqrt(qfloat16(2.0f));
```

`qSqrt()` 返回 `qfloat16`。它会尽可能使用 native half 或底层数学实现，否则通过 `float` 计算后再转回 half。结果最终仍受 binary16 精度限制。

负数、NaN 和无穷的行为遵循浮点平方根的分类规则。需要更高精度的中间结果时，先转换为 `float` 并使用 `std::sqrt`，最后按需存回 `qfloat16`。

### 10.2 `qHypot()`

`qHypot()` 为 qfloat16 提供与其他浮点类型组合的重载。所有操作数都是 qfloat16 时，结果保持 qfloat16；混合其他浮点类型时，结果类型按 Qt 的 `QHypotType` 规则选择：

```cpp
const qfloat16 h = qHypot(qfloat16(3.0f),
                          qfloat16(4.0f));

const double mixed = qHypot(qfloat16(3.0f), 4.0);
```

不要只根据变量名假设返回类型，混合表达式需要查看重载或显式转换。

### 10.3 `qRound()`、`qRound64()` 和 `qIntCast()`

```cpp
const int rounded = qRound(qfloat16(2.6f));
const qint64 rounded64 = qRound64(qfloat16(2.6f));
const int truncated = qIntCast(qfloat16(2.6f));
```

- `qRound()` 返回 `int`，按 Qt 的整数舍入语义取最近整数；
- `qRound64()` 返回 `qint64`；
- `qIntCast()` 直接转换为 `int`，适合明确需要转换语义而不是“取最近整数”的场景。

输入超出目标整数类型可表示范围时，不要把结果当作安全的饱和转换。需要饱和、范围检查或协议合法性时，先检查浮点范围。

### 10.4 `qFuzzyCompare()` 和 `qFuzzyIsNull()`

```cpp
if (qFuzzyCompare(actual, expected))
    accept();

if (qFuzzyIsNull(error))
    treatAsZero();
```

`qFuzzyCompare()` 使用相对比较，数值越小，比较窗口越严格；它不是固定绝对误差比较。half 精度只有约 3 位十进制有效数字，因此“模糊相等”不能掩盖数据压缩带来的真实误差。

`qFuzzyIsNull(qfloat16)` 使用适合 qfloat16 精度的零阈值，约为 `0.00976`。如果业务有自己的单位和误差预算，应使用业务阈值，不要把该阈值当作所有领域的零定义。

### 10.5 `qHash()`

```cpp
QHash<qfloat16, int> buckets;
buckets.insert(qfloat16(0.5f), 1);
```

Qt 6.5.3 起提供 `qHash(qfloat16, size_t seed)`。Qt 文档特别说明：

- Qt 6.5 之前由 `qHash(float)` 重载提供相关能力；
- Qt 6.5.0 到 6.5.2 存在不同形式的问题；
- Qt 6.5.3 和 Qt 6.6 起恢复 Qt 6.4 的行为。

如果项目需要跨 Qt 版本稳定复现 hash 值，不要把 Qt 内部 hash 算法当作文件格式或网络协议的一部分。

## 11. 流和二进制序列化

### 11.1 QDataStream

```cpp
QDataStream stream(&device);
stream << halfValue;

qfloat16 restored;
stream >> restored;
```

`QDataStream` 以标准 IEEE 754 格式写入和读取 qfloat16。它适合 Qt 生态内的二进制数据流，但仍应明确数据流版本、字节序和协议字段顺序。

Qt 6.3 之前，相关运算符曾经是 `QDataStream` 的成员；Qt 6.3 起是 qfloat16 的相关非成员运算符。新代码按当前头文件和文档使用即可。

### 11.2 QTextStream

Qt 头文件还提供 qfloat16 与 `QTextStream` 的流运算符。文本流会把值转换为文本表示，受文本流格式、locale 和精度设置影响。它不是保存 16 位原始编码的方式；需要精确 binary16 存储时使用 `QDataStream` 或专门的二进制协议。

## 12. NativeType、NearestFloat 和 IsNative

`qfloat16` 暴露几个用于跨编译器和平台实现的类型信息：

```cpp
using Native = qfloat16::NativeType;
using Nearest = qfloat16::NearestFloat;
constexpr bool native = qfloat16::IsNative;
```

- `NativeType` 是平台支持的原生 half 类型；
- `NearestFloat` 是 Qt 进行中间计算时使用的最近浮点类型；
- `IsNative` 表示当前编译配置是否有原生 half 表示。

这些 API 适合模板库、性能适配和 ABI 相关代码。普通业务代码不应依赖 native half 的具体名称、寄存器传递方式或编译器扩展；跨平台接口优先使用 `qfloat16`、`float` 和 Qt 的批量转换函数。

## 13. 常见使用场景

### 13.1 大数组的低带宽存储

```cpp
QVector<float> values = loadValues();
QVector<qfloat16> compact(values.size(), Qt::Uninitialized);

qFloatToFloat16(compact.data(), values.constData(), values.size());
```

只在需要计算或展示时转换回 `float`：

```cpp
QVector<float> working(values.size());
qFloatFromFloat16(working.data(),
                  compact.constData(),
                  compact.size());
```

### 13.2 GPU 或设备接口边界

在设备 API 要求 binary16 的边界，`qfloat16` 可以表达存储类型和容器元素类型。设备是否接受 Qt 对象布局、是否要求特定对齐和字节序，仍由设备 API 决定；不要因为 `qfloat16` 是 16 位就跳过设备接口的布局要求。

### 13.3 传感器或图像缓存

当传感器噪声、显示精度或下游协议本身低于 half 精度时，用 qfloat16 降低内存占用很合适。若数据要用于积分、滤波、标定或财务类计算，应在计算阶段提升到 `float` 或 `double`。

## 14. 常见误区

### 把 qfloat16 当作更快的 float

它主要优化存储和带宽。普通算术通常会提升到 `float`，硬件是否加速取决于平台和编译配置。

### 忽略每次存回带来的舍入

`qfloat16 sum; sum += value;` 会在每次复合赋值后回到 half。数值敏感的累加使用 `float` 或 `double`。

### 使用未初始化构造后直接读取

`qfloat16(Qt::Uninitialized)` 没有有效值。只适合马上由写入或批量转换填满的缓冲区。

### 用 `==` 处理 NaN

NaN 与任何值都不按普通数值相等。先调用 `qIsNaN()`，再应用业务策略。

### 用 `qFuzzyCompare()` 代替范围验证

模糊比较不能证明数据在协议、物理或业务允许范围内。先做有限性、范围和单位检查。

### 把 qHash 结果当协议字段

Qt 不保证跨版本保持相同 hash 算法。hash 只用于当前程序的数据结构。

### 直接把对象内存当作网络字节

使用 `QDataStream` 或明确的 binary16 编码，处理字节序、版本和字段边界。

## 15. API 逐项说明

### 15.1 类型、构造和转换

| API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `using NativeType` | 暴露平台原生 half 类型。 | 适合模板或平台适配；不要依赖具体编译器类型名。 |
| `static constexpr bool IsNative` | 表示当前实现是否使用 native half。 | 不代表所有算术都在 half 中执行。 |
| `using NearestFloat` | 表示中间计算使用的最近浮点类型。 | 通常是 native half 或 float，属于实现适配信息。 |
| `qfloat16()` | 默认构造为零值。 | 适合普通值初始化。 |
| `qfloat16(Qt::Initialization)` | 构造未初始化的 qfloat16。 | Qt 6.1 起；读取前必须先写入。 |
| `qfloat16(float)` / native half 构造 | 从最近的浮点类型转换为 half。 | 可能舍入、下溢或溢出。 |
| `qfloat16(T)`（算术类型） | 显式从其他算术类型构造。 | 结果受 binary16 精度和范围限制。 |
| `operator float()` 或 native 转换 | 将 qfloat16 转为计算浮点类型。 | 推荐显式 `static_cast<float>` 表达意图。 |
| `std::numeric_limits<qfloat16>` | 查询 half 精度和范围。 | `min()` 是最小正规格，不是 `denorm_min()`。 |

### 15.2 分类和符号

| API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `isInf()` | 判断正负无穷。 | 无穷不是有限值。 |
| `isNaN()` | 判断 NaN。 | NaN 不参与普通全序比较。 |
| `isFinite()` | 判断是否为有限数。 | zero、subnormal、normal 都是 finite。 |
| `fpClassify()` | 返回浮点分类。 | 与 `FP_NAN` 等分类宏配合。 |
| `isNormal()` | 判断是否为有限且正规格的数。 | zero、subnormal、inf、NaN 都返回 false。 |
| `copysign(qfloat16, qfloat16)` | 用第二个值的符号替换第一个值的符号。 | Qt 6.11 起；保留负零、负 NaN 等符号位语义。 |
| `signbit(qfloat16)` | 检查符号位。 | Qt 6.11 起；负零、负无穷、负 NaN 也可能为 true。 |
| `copySign(qfloat16) const` | 旧的成员形式复制符号。 | 已 deprecated，新代码使用非成员 `copysign()`。 |

### 15.3 算术、比较和赋值

| API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| unary `-` | 改变 qfloat16 符号位。 | 负零的符号仍有意义。 |
| `qfloat16 op qfloat16` | 执行加减乘除并返回 qfloat16。 | 中间提升后结果再次舍入到 half。 |
| `qfloat16 op float` | 与 float 混合运算。 | 返回 float，通常不立即回到 half。 |
| `qfloat16 op double/long double` | 与更宽浮点混合运算。 | 结果保持对应宽浮点类型。 |
| `qfloat16 op integer` | 与整数混合运算。 | Qt 重载返回 double。 |
| `qfloat16 op= floating` | 复合运算并回存到 qfloat16。 | 每次赋值都会发生 half 舍入。 |
| `operator==` 等部分比较 | 与 qfloat16、浮点和整数比较。 | NaN 使比较无序；类是 partially comparable。 |
| `compareThreeWay()` | 返回 `Qt::partial_ordering`。 | 遇 NaN 时检查 `unordered`。 |

### 15.4 批量转换

| API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `qFloatToFloat16(out, in, len)` | 把 `len` 个 float 转成 qfloat16。 | 两个数组都要有足够容量；不负责分配和检查。 |
| `qFloatFromFloat16(out, in, len)` | 把 `len` 个 qfloat16 转成 float。 | 指针和容量由调用方保证；适合大批量转换。 |

### 15.5 数值和容器辅助

| API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `qSqrt(qfloat16)` | 计算 qfloat16 平方根。 | 返回 qfloat16；结果精度受 half 限制。 |
| `qHypot(...)` | 计算一个或多个参数的平方和平方根。 | 混合类型时返回类型按重载规则变化。 |
| `qRound(qfloat16)` | 舍入为 `int`。 | 目标范围和浮点特殊值要先处理。 |
| `qRound64(qfloat16)` | 舍入为 `qint64`。 | 不等于饱和转换。 |
| `qIntCast(qfloat16)` | 转为 `int`。 | 与取最近整数不同，按整数转换语义处理。 |
| `qFuzzyCompare(qfloat16, qfloat16)` | 相对模糊比较。 | 不适合 NaN 处理或业务范围验证。 |
| `qFuzzyIsNull(qfloat16)` | 按 qfloat16 精度判断接近零。 | 阈值约为 0.00976，领域阈值需自行定义。 |
| `qHash(qfloat16, size_t)` | 为 QHash/QSet 提供 hash。 | Qt 6.5.3 起；不要用于跨版本协议。 |

### 15.6 流运算符

| API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- |
| `QDataStream &operator<<(QDataStream &, qfloat16)` | 按标准 IEEE 754 格式写入 qfloat16。 | 明确数据流版本、字节序和字段布局。 |
| `QDataStream &operator>>(QDataStream &, qfloat16 &)` | 从数据流读取 qfloat16。 | 读取失败仍应检查 `QDataStream` 状态。 |
| `QTextStream &operator<<(QTextStream &, qfloat16)` | 把 qfloat16 写成文本。 | 受文本流格式和 locale 影响，不保存原始 16 位编码。 |
| `QTextStream &operator>>(QTextStream &, qfloat16 &)` | 从文本读取 qfloat16。 | 文本格式、精度和 locale 影响解析。 |

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型 | `qfloat16` | 16 位 IEEE 754 binary16 存储类型。 | 主要用于存储和带宽优化，不是通用高精度计算类型。 |
| 类型 | `NativeType` / `NearestFloat` / `IsNative` | 暴露平台实现信息。 | 普通业务不要依赖 native half 细节。 |
| 构造 | `qfloat16()` | 构造零值。 | 可安全用于普通值初始化。 |
| 构造 | `qfloat16(Qt::Uninitialized)` | 构造未初始化值。 | Qt 6.1 起；必须先写后读。 |
| 转换 | `qfloat16(float)` | 把 float 压缩为 half。 | 可能舍入、下溢或溢出。 |
| 转换 | `static_cast<float>(value)` | 把 half 提升为 float。 | 计算前显式提升更清晰。 |
| 范围 | `numeric_limits<qfloat16>` | 查询 epsilon、min、max、NaN 和无穷。 | `min()` 与 `denorm_min()` 含义不同。 |
| 分类 | `isInf()` / `qIsInf()` | 判断无穷。 | 需与 `isFinite()` 区分。 |
| 分类 | `isNaN()` / `qIsNaN()` | 判断 NaN。 | NaN 不按普通数值比较。 |
| 分类 | `isFinite()` / `qIsFinite()` | 判断有限数。 | 包括零、subnormal、normal。 |
| 分类 | `fpClassify()` / `qFpClassify()` | 区分 NaN、inf、zero、subnormal、normal。 | 与 `FP_*` 宏配合。 |
| 分类 | `isNormal()` | 判断有限正规格数。 | 不包括零和 subnormal。 |
| 符号 | `copysign(x, sign)` | 复制 sign 的符号位。 | Qt 6.11 起；支持负零等符号。 |
| 符号 | `signbit(x)` | 读取符号位。 | 负 NaN 和负零也可为 true。 |
| 符号 | `copySign(sign)` | 旧成员符号复制 API。 | deprecated，用 `copysign()`。 |
| 算术 | `qfloat16 op qfloat16` | half 值之间运算。 | 结果回到 half，累计舍入。 |
| 算术 | `qfloat16 op float/double` | 与宽浮点混合运算。 | 返回宽浮点，`auto` 类型要确认。 |
| 算术 | `qfloat16 op integer` | 与整数混合运算。 | Qt 重载返回 double。 |
| 赋值 | `op=` | 运算并回存 qfloat16。 | 每次复合赋值都会舍入。 |
| 比较 | `operator==` / `<` / `>` | 部分可比较。 | NaN 导致 unordered 语义。 |
| 比较 | `compareThreeWay()` | 返回部分排序结果。 | 检查 `Qt::partial_ordering::unordered`。 |
| 批量 | `qFloatToFloat16()` | float 数组转 half 数组。 | 输出容量和指针必须由调用方保证。 |
| 批量 | `qFloatFromFloat16()` | half 数组转 float 数组。 | 适合大数组；可运行时检测 F16C。 |
| 数学 | `qSqrt()` | qfloat16 平方根。 | 结果是 qfloat16。 |
| 数学 | `qHypot()` | 计算 hypot。 | 混合类型结果类型可能不同。 |
| 整数 | `qRound()` / `qRound64()` | 舍入为 int 或 qint64。 | 先处理 NaN、inf 和范围。 |
| 整数 | `qIntCast()` | 转为 int。 | 不等于取最近整数。 |
| 比较 | `qFuzzyCompare()` | 相对模糊比较。 | 不适合 NaN 和固定业务误差。 |
| 比较 | `qFuzzyIsNull()` | 判断接近零。 | 约 0.00976 的 half 精度阈值。 |
| 容器 | `qHash()` | 为 QHash/QSet 计算 hash。 | Qt 6.5.3 起；不用于稳定协议。 |
| 二进制流 | `QDataStream` 运算符 | 按 IEEE 754 half 格式读写。 | 检查流状态和协议版本。 |
| 文本流 | `QTextStream` 运算符 | 以文本读写 qfloat16。 | 不保存原始 16 位编码。 |

### 一句话总结

`qfloat16` 的强项是用 16 位保存 IEEE 754 half 数据，适合压缩大数组、设备接口和带宽受限场景；它的代价是约 3 位十进制有效数字、有限的动态范围，以及每次回存时的舍入。存储用 half，计算通常提升到 float，最终再按业务需要压回去。
