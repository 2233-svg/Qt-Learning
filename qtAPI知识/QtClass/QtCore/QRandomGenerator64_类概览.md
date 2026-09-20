# QRandomGenerator64：让标准算法默认消费 64 位随机样本

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QRandomGenerator64>`  
> CMake：`find_package(Qt6 REQUIRED COMPONENTS Core)`，并链接 `Qt6::Core`  
> qmake：`QT += core`  
> 基类：`QRandomGenerator`

`QRandomGenerator64` 是 `QRandomGenerator` 的轻量适配器。它没有引入另一套随机算法，唯一的核心改变是把默认输出宽度从 32 位改成 64 位：`generate()` 与 `operator()()` 都等价于基类的 `generate64()`。

它解决的是标准库算法和随机分布“通过调用函数对象取得样本”时的位宽问题。若算法需要 64 位样本，直接传入 `QRandomGenerator` 时会默认得到 `quint32`；传入 `QRandomGenerator64` 则默认得到 `quint64`。

## 真实使用场景

### 交给需要 64 位样本的标准库算法

`operator()()` 符合随机引擎的调用形式，因此可直接传给许多 `<random>` 算法和分布：

```cpp
#include <QRandomGenerator64>
#include <random>

quint64 chooseId()
{
    std::uniform_int_distribution<quint64> distribution(0, 999999999999ULL);
    return distribution(*QRandomGenerator64::global());
}
```

对于只需要 32 位范围或小范围整数的场景，`QRandomGenerator` 已足够；不要仅因“64 位看起来更大”就无差别替换。更宽的样本不能使一个糟糕的范围映射或并发设计自动正确。

### 生成完整 64 位标识、掩码或模拟输入

```cpp
QRandomGenerator64 local(0x13572468);
quint64 mask = local.generate();
```

显式种子时，`QRandomGenerator64` 仍遵循基类的确定性规则：相同种子数据得到相同序列。它非常适合需要完整 64 位、又需要回放的模拟和测试。

## 它与 QRandomGenerator 的关系

可以把它看成以下两行语义：

```cpp
quint64 QRandomGenerator64::generate()   { return generate64(); }
quint64 QRandomGenerator64::operator()() { return generate64(); }
```

其余能力都来自基类：构造与播种、`bounded()`、`generate64()`、`generateDouble()`、`fillRange()`、`discard()`，以及 `global()`、`system()`、`securelySeeded()`。

头文件通过 `using QRandomGenerator::generate;` 保留基类的批量 `generate(begin, end)` 重载。因此：

- 无参 `generate()` 返回 `quint64`；
- 带迭代器的 `generate(begin, end)` 仍是基类的 32 位批量写入接口；
- 连续的 `quint64` 缓冲区应使用继承的 `fillRange()`，而不是误以为带迭代器的 `generate()` 会自动填入 64 位值。

## 64 位与有符号转换的边界

`generate()` 的 64 个 bit 都是随机的，最高位有约一半概率为 1。把返回值转成 `qint64` 时，约一半结果会是负数：

```cpp
#include <limits>

qint64 nonNegative =
    QRandomGenerator64::global()->generate()
    & std::numeric_limits<qint64>::max();
```

如果业务要的是一个有界正数，更清晰的写法通常是 `bounded()`。只有确实需要保留随机低 63 位时，才掩掉符号位。不要用 `abs(static_cast<qint64>(value))`，因为最小有符号整数没有可表示的正绝对值。

## 播种、共享和线程

`QRandomGenerator64` 的构造函数、`seed()`、`global()`、`system()` 与 `securelySeeded()` 都沿用基类模型：

- 相同显式种子产生相同序列，不同种子不保证必然不同；
- 局部实例可重入，但同一个局部实例被多线程共享时需要外部同步；
- `global()` 和 `system()` 返回 Qt 管理的共享对象，访问线程安全；
- `global()` 已由系统源安全播种，但多线程谁先取到下一项不可预测；
- `system()` 是操作系统随机源，适合少量安全样本或播种，不适合高频批量数据；
- `securelySeeded()` 创建独立、系统安全播种的普通发生器；短期只取少量数据时通常比 `global()` 更浪费。

静态成员 `QRandomGenerator64::global()`、`system()` 和 `securelySeeded()` 返回的是 64 位适配器版本，便于直接作为 64 位随机引擎传给标准算法。返回指针由 Qt 所有，不能删除，也不要调用 `seed()` 改写共享状态。

## `discard()` 的特殊单位

基类 `QRandomGenerator::discard(z)` 跳过 `z` 个 32 位样本。`QRandomGenerator64::discard(z)` 则把 `z` 解释为 **64 位样本数**，内部跳过两倍数量的 32 位样本。

这带来一个极端边界：实现会检查 `z * 2` 是否溢出。接近 `unsigned long long` 最大值的大 `z` 会触发断言，而不是可靠地跳到一个极端远的状态之后。大量跳过状态应重新审视算法设计，而非把它作为常规索引手段。

## 常见错误

1. 以为 `QRandomGenerator64` 是更安全的随机算法。它只是改变默认输出位宽，安全性取决于种子来源和是否直接使用 `system()`。
2. 把 `quint64` 直接转 `qint64` 后假定非负。最高位随机，约一半会变负。
3. 调用 `generate(begin, end)` 填 `quint64` 容器并期望 64 位样本。继承的该重载只产生 32 位数据，高位为零。
4. 多线程无锁共享局部 `QRandomGenerator64`。可重入意味着不同对象可并发，不意味着同一对象可并发修改。
5. 使用 `discard()` 的极大计数。该适配器会把计数乘二，存在溢出断言边界。

## API 速查表

| API | 语义 | 前置条件与边界 |
| --- | --- | --- |
| `QRandomGenerator64(quint32 seed = 1)` | 以单个种子构造 64 位默认输出的发生器。 | 相同种子产生相同序列；默认种子也是确定性的。 |
| `QRandomGenerator64(const quint32 (&buffer)[N])` | 以 32 位种子数组构造。 | 缓冲区只在构造时读取，不转移所有权。 |
| `QRandomGenerator64(const quint32 *buffer, qsizetype len)` | 以指定数量的 32 位种子构造。 | `len >= 0`；`len > 0` 时指针必须有效。 |
| `QRandomGenerator64(const quint32 *begin, const quint32 *end)` | 以半开种子范围构造。 | `[begin, end)` 必须是有效范围。 |
| `QRandomGenerator64(std::seed_seq &seedSeq)` | 以标准库种子序列构造。 | 继承基类种子语义。 |
| `QRandomGenerator64(const QRandomGenerator &other)` | 从基类发生器当前状态构造。 | 复制的是状态，不是自动独立分流。 |
| `generate()` | 返回一个完整的 `quint64` 随机样本。 | 默认输出与基类 `generate64()` 相同；转 `qint64` 可能为负。 |
| `operator()()` | 返回一个 64 位样本。 | 适合要求 64 位随机引擎调用符的标准算法。 |
| `result_type` | `operator()()` 的结果类型。 | 固定为 `quint64`。 |
| `discard(unsigned long long z)` | 丢弃 `z` 个 64 位样本。 | 内部会跳过 `2*z` 个 32 位样本；极大 `z` 会触发乘二溢出断言。 |
| `min()` | 返回 64 位引擎的最小可输出值。 | 固定为 `0`。 |
| `max()` | 返回 64 位引擎的最大可输出值。 | 固定为 `quint64` 最大值。 |
| `global()` | 返回共享、安全播种的 64 位适配器。 | 线程安全、Qt 所有；全局取样顺序不保证可复现。 |
| `system()` | 返回共享的操作系统 64 位随机源适配器。 | 线程安全；不要高频批量使用，不能删除。 |
| `securelySeeded()` | 返回独立、安全播种的 64 位适配器对象。 | 适合长期持有；少量短期取样优先 `global()`。 |
| 继承的 `bounded(...)` | 生成上界排除的有界数。 | 整型要求有效、非空范围；完整 64 位范围用无参 `generate()`。 |
| 继承的 `fillRange(...)` | 高效写入连续 32/64 位无符号缓冲区。 | 元素必须是至少 32 位的无符号类型。 |
| 继承的 `generate(begin, end)` | 按基类规则批量产生 32 位样本。 | 对宽元素高位补零，不等价于无参 64 位 `generate()`。 |
| 继承的 `seed(...)` | 重新播种当前对象。 | 会丢弃现有序列；共享局部对象时须外部同步。 |
| 继承的 `generateDouble()` | 返回 `[0.0, 1.0)`。 | 与默认位宽无关；绝不返回 `1.0`。 |

## 一句话总结

`QRandomGenerator64` 不是另一种随机算法，而是让 `generate()` 和 `operator()()` 默认给出 `quint64` 的适配器；用它服务 64 位标准算法和完整 64 位样本，用基类规则处理播种、范围、线程与系统随机源。
