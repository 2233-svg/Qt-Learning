# QRandomGenerator：可复现、共享和系统随机数该怎样选

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QRandomGenerator>`  
> CMake：`find_package(Qt6 REQUIRED COMPONENTS Core)`，并链接 `Qt6::Core`  
> qmake：`QT += core`

`QRandomGenerator` 提供高质量的伪随机数发生器（PRNG），以及 Qt 对操作系统随机源的统一入口。它解决的并不是“怎样得到一个看起来变化的数字”这么简单，而是让程序能在三种相互冲突的目标之间明确取舍：

- 测试、回放和程序化内容需要**可复现**的序列；
- 普通业务需要随取随用、可跨线程共享的随机样本；
- 安全令牌、密钥材料的种子等场景需要操作系统提供的随机源。

这三个目标分别对应普通对象、`global()` / `securelySeeded()` 与 `system()`。选错入口通常不会立刻报错，却会让测试偶发、性能下降，或者误把普通 PRNG 当成安全随机源。

## 解决的问题与典型场景

### 可复现的随机流程

显式传入相同的种子数据，普通 `QRandomGenerator` 会产生相同的后续序列。这适合：

- 单元测试中稳定重放“随机”输入；
- 联机游戏以种子同步地图、掉落或程序化关卡；
- 排查 bug 时记录种子，在本地重现一次失败。

```cpp
#include <QRandomGenerator>
#include <QtGlobal>

void verifyDeterminism()
{
    QRandomGenerator first(1234);
    QRandomGenerator second(1234);

    Q_ASSERT(first.generate() == second.generate());
    Q_ASSERT(first.generate64() == second.generate64());
}
```

不同种子通常会得到显著不同的序列，但 Qt 不承诺“不同种子必然映射到不同序列”。种子经过混合，且内部状态有限，所以把种子当作唯一 ID 是错误的。

### GUI、模拟和普通业务中的随机取样

例如随机颜色、抽样、退避时间、非安全的测试数据，通常直接使用 `QRandomGenerator::global()`：

```cpp
int delayMs = QRandomGenerator::global()->bounded(50, 151); // [50, 151)
quint32 value = QRandomGenerator::global()->generate();
```

它由 Qt 安全播种、可跨线程共享且访问线程安全，避免为一次性取样创建并安全播种一个较大的发生器对象。

### 生成长期独立的随机流

需要一个可长期保存、与全局流分开的随机流时，用 `securelySeeded()` 创建普通对象：

```cpp
class Simulation
{
    QRandomGenerator random = QRandomGenerator::securelySeeded();
};
```

这个对象的初始状态来自系统随机源，随后按普通 PRNG 工作。它适合长寿命模拟、会话级随机流等；若只生成少量值，创建成本反而高，优先使用 `global()`。

### 系统级安全随机源

`system()` 返回共享的操作系统随机源。它适合安全敏感数据的少量生成，或给其他引擎安全播种：

```cpp
std::seed_seq seed {
    QRandomGenerator::system()->generate(),
    QRandomGenerator::system()->generate()
};
QRandomGenerator worker(seed);
```

不要把它用于高频、大批量数据。Qt 文档给出的经验上限约为每秒 1 KiB；硬件真随机源或系统熵池在某些平台上是有限资源，耗尽后会发生降级，降级后的安全性质由实现决定。

## 三种来源的选择

| 需求 | 应选 API | 关键理由 |
| --- | --- | --- |
| 固定回放、确定性测试 | 构造函数或 `seed()` | 相同种子得到相同序列。 |
| 少量、普通用途随机数 | `global()` | 安全播种、共享对象、线程安全、没有反复创建成本。 |
| 长期持有的独立随机流 | `securelySeeded()` | 安全播种后得到独立的普通 PRNG。 |
| 少量安全随机数据或为引擎播种 | `system()` | 直接使用操作系统随机设施。 |
| 大批量普通随机数据 | 普通实例或 `global()` 的 `fillRange()` | 避免频繁消耗系统随机源。 |

`global()` 并不适合需要可复现顺序的算法。虽然可以复制该对象，复制品会从同一状态开始产生相同流，但其他线程可能在不可预测的时刻从全局对象取样，因此“下一项是谁先拿到”不可复现。

## 随机数的范围语义

### 原始样本

- `generate()` 产生完整的 `quint32` 范围，即 `[0, 2^32 - 1]`。
- `generate64()` 产生完整的 `quint64` 范围。
- `generateDouble()` 产生 `[0.0, 1.0)`，包含 `0.0`，绝不返回 `1.0`。
- `operator()()` 等同于 `generate()`，这样对象可以直接交给大部分标准库随机分布。

把 `generate()` 的结果直接转成有符号数，会让最高位为 1 的一半结果成为负数。需要非负值时应使用合适的 `bounded()`，而不是靠取绝对值；对最小负数取绝对值本身也有溢出问题。

### `bounded()` 的上界永远排除

整型 `bounded(highest)` 生成 `[0, highest)`；整型 `bounded(lowest, highest)` 生成 `[lowest, highest)`。因此：

```cpp
int die = QRandomGenerator::global()->bounded(1, 7); // 1 到 6
```

单上界整型重载要求 `highest > 0`，双边界重载要求 `highest > lowest`。违反前置条件会触发断言，发布构建中不能把断言当作输入校验；来自用户、文件或网络的边界必须先检查。

双边界重载还依赖 `highest - lowest`。不要用 `qint64` 的最小值与最大值试图覆盖完整有符号范围，差值会超出可表示范围。若确实要完整 32/64 位样本，请用 `generate()` / `generate64()`。

`bounded(double highest)` 的实现是 `generateDouble() * highest`。正数时可理解为 `[0, highest)`，负数时得到 `(highest, 0]` 方向的结果；`NaN` 和无穷值会遵循 IEEE 浮点乘法传播。业务 API 应先拒绝非有限值，且不要假定浮点边界与整型 `bounded()` 有同样的断言保护。

## 批量写入与性能

连续的无符号缓冲区优先使用 `fillRange()`。元素类型必须是至少 32 位的无符号整数，Qt 才能完整填入 32 或 64 位数据：

```cpp
QList<quint64> ids(128);
QRandomGenerator::global()->fillRange(ids.data(), ids.size());
```

`generate(begin, end)` 是为了兼容 `std::seed_seq` 风格的前向迭代器接口，它写入的始终是 32 位值。目标元素即使宽于 32 位，高位也会是零；填 `quint64` 数组时请改用 `fillRange()` 或循环调用 `generate64()`。

`fillRange(pointer, count)` 不替你管理内存：`pointer` 必须指向至少 `count` 个有效元素，`count` 不能为负，缓冲区不得在调用中失效。

## 种子、拷贝与状态

构造函数和 `seed()` 接受单个 `quint32`、32 位种子数组、指针范围或 `std::seed_seq`。理想的种子数据量大约与 `QRandomGenerator` 自身状态大小相当；只有一个 32 位种子可复现，但不会提供很大的初始状态空间。

拷贝普通发生器会复制当前状态，之后两个副本会产生相同的后续序列，直到其中一个被单独推进或重新播种。这个行为很适合建立检查点，却容易在“每个 worker 都复制同一 master”时制造完全相同的数据流。

`system()` 的副本仍会读取操作系统设施，不会复制出相同序列。无论哪种共享对象，都不要经由返回的指针调用 `seed()`，否则会把进程中其他代码依赖的共享流也改掉。

## 线程与生命周期边界

`QRandomGenerator` 的所有成员函数都是可重入的：不同对象可在不同线程并发使用。普通对象**不是**共享时自动加锁的；多个线程同时读写同一实例时，调用方必须同步，或者每个线程持有自己的对象。

`global()` 与 `system()` 返回的共享对象可在线程间无锁使用，且这两个静态访问函数也线程安全。返回指针由 Qt 管理，不能 `delete`，也不应保存为需要跨 DLL 卸载或进程结束阶段仍可用的资源。

`QRandomGenerator` 不依赖事件循环，不是 `QObject`，没有父子对象关系，也没有 GUI 线程限制。

## 常见错误

1. 用 `bounded(6)` 模拟骰子却期望得到 1 到 6。它实际返回 0 到 5，应使用 `bounded(1, 7)`。
2. 把 `system()` 当作海量数据填充器。它应主要用于少量安全样本或播种，大批量数据改用安全播种后的普通实例。
3. 在多个线程共享一个局部 `QRandomGenerator` 而不加锁。可重入不等于同一个对象线程安全。
4. 对 `global()` 调用 `seed()`。这会改变共享全局流，造成难以追踪的耦合。
5. 用 `generate(begin, end)` 填 `quint64` 并期待 64 位熵。此 API 只写 32 位随机数，高位为零。
6. 用不同种子作为“必不重复”的保证。Qt 只承诺相同种子对应可复现序列，不承诺不同种子互异。
7. 把 `securelySeeded()` 放进短小的热循环。安全播种自身昂贵；生成少于约 2600 bytes 数据时通常不划算。

## API 速查表

| API | 语义 | 前置条件与边界 |
| --- | --- | --- |
| `QRandomGenerator(quint32 seed = 1)` | 用单个 32 位值初始化可复现 PRNG。 | 默认种子也是确定性的；相同种子产生相同序列。 |
| `QRandomGenerator(const quint32 (&seedBuffer)[N])` | 用固定长度的 32 位种子数组初始化。 | 数组内容被读取为种子数据；不保留数组所有权。 |
| `QRandomGenerator(const quint32 *begin, const quint32 *end)` | 用半开指针范围 `[begin, end)` 初始化。 | 指针范围必须有效且可遍历；不能传倒置或悬空范围。 |
| `QRandomGenerator(const quint32 *buffer, qsizetype len)` | 用 `len` 个 32 位种子初始化。 | `len >= 0`；`len > 0` 时 `buffer` 必须有效。 |
| `QRandomGenerator(std::seed_seq &seedSeq)` | 用标准库种子序列初始化。 | 参数是非常量引用，符合 `std::seed_seq` 的生成接口。 |
| `QRandomGenerator(const QRandomGenerator &other)` | 复制发生器当前状态。 | 普通副本将产生同样的后续流；不要误认为已自动分流。 |
| `operator=(const QRandomGenerator &other)` | 用另一个发生器的当前状态覆盖自己。 | 覆盖后当前序列丢失；并发共享对象需外部同步。 |
| `generate()` | 返回一个 32 位无符号随机样本。 | 覆盖完整 `quint32` 范围。 |
| `generate64()` | 返回一个 64 位无符号随机样本。 | 覆盖完整 `quint64` 范围；需要全 64 位范围时用它。 |
| `generateDouble()` | 返回 `[0.0, 1.0)` 的 `double`。 | 包含 0，不包含 1；不适合作为离散整数的取模替代。 |
| `operator()()` | 返回一个 32 位样本，等同 `generate()`。 | 用于要求 UniformRandomBitGenerator 风格调用符的标准算法。 |
| `generate(ForwardIterator begin, ForwardIterator end)` | 向前向迭代器范围写入 32 位样本。 | 宽于 32 位的元素高位为零；连续内存批量填充优先 `fillRange()`。 |
| `generate(quint32 *begin, quint32 *end)` | 向 `quint32` 指针半开范围批量写入。 | 指针范围必须有效、非倒置且可写。 |
| `fillRange(UInt (&buffer)[N])` | 高效填满无符号数组。 | `UInt` 必须是至少 32 位的无符号整数。 |
| `fillRange(UInt *buffer, qsizetype count)` | 高效填满连续缓冲区。 | 缓冲区必须容纳 `count` 个元素；`count` 不可为负。 |
| `bounded(int highest)` | 返回 `[0, highest)` 的 `int`。 | `highest > 0`。 |
| `bounded(qint64 highest)` | 返回 `[0, highest)` 的 `qint64`。 | `highest > 0`。 |
| `bounded(quint32 highest)` | 返回 `[0, highest)` 的 32 位无符号数。 | `highest` 必须非零。 |
| `bounded(quint64 highest)` | 返回 `[0, highest)` 的 64 位无符号数。 | `highest` 必须非零；内部拒绝采样，耗时不是严格常量。 |
| `bounded(double highest)` | 用 `[0, 1)` 浮点样本缩放。 | 先验证有限性；负值、`NaN`、无穷值不应直接暴露为业务随机范围。 |
| `bounded(int lowest, int highest)` | 返回 `[lowest, highest)`。 | `highest > lowest`，并避免差值溢出。 |
| `bounded(qint64 lowest, qint64 highest)` | 返回 64 位有符号半开范围。 | `highest > lowest`；不能借此覆盖完整有符号 64 位范围。 |
| `bounded(quint32 lowest, quint32 highest)` | 返回 32 位无符号半开范围。 | `highest > lowest`。 |
| `bounded(quint64 lowest, quint64 highest)` | 返回 64 位无符号半开范围。 | `highest > lowest`；完整范围改用 `generate64()`。 |
| `bounded(int, qint64)` / `bounded(qint64, int)` | 为混合有符号参数消除重载歧义。 | 语义同 `qint64` 双边界重载。 |
| `bounded(unsigned, quint64)` / `bounded(quint64, unsigned)` | 为混合无符号参数消除重载歧义。 | 语义同 `quint64` 双边界重载。 |
| `seed(quint32 seed = 1)` | 重置为单一 32 位种子。 | 会丢弃当前状态和剩余序列。 |
| `seed(std::seed_seq &seedSeq)` | 用标准库种子序列重新播种。 | 会丢弃当前状态；共享实例调用需同步。 |
| `discard(unsigned long long z)` | 丢弃接下来的 `z` 个 32 位样本。 | 等价于调用 `generate()` `z` 次，适合按样本数跳过状态。 |
| `global()` | 返回 Qt 管理的共享、安全播种发生器。 | 对象访问线程安全；不可删除、不可重播种；多线程顺序不可复现。 |
| `securelySeeded()` | 返回用 `system()` 安全播种的新普通发生器。 | 创建较贵，长时间持有更合适；新对象本身共享时仍要加锁。 |
| `system()` | 返回 Qt 管理的共享操作系统随机源。 | 线程安全；不用于高频/批量生成，不能 `delete`。 |
| `min()` | 返回 `result_type` 最小值。 | 固定为 `0`。 |
| `max()` | 返回 `result_type` 最大值。 | 固定为 `quint32` 最大值。 |
| `result_type` | `operator()()` 的结果类型别名。 | 对本类为 `quint32`。 |
| `operator==` / `operator!=` | 比较两个引擎的状态及是否读取系统源。 | 同样的未来序列才可视为同状态；系统源与普通引擎不同。 |

## 一句话总结

需要可复现就自己播种，需要普通随机值就用 `global()`，需要长期独立流就用 `securelySeeded()`，只有少量安全随机数据或播种才直接使用 `system()`；所有整型范围 API 都遵循“下界包含、上界排除”。
