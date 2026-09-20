# QRandomGenerator
> Qt 6.11.1 · Qt Core · 来自 `QRandomGenerator`

## 作用定位
`QRandomGenerator` 生成伪随机的 32 位、64 位和 `[0, 1)` 双精度数。它既能创建可复现的本地生成器，也提供应用级 `global()` 和操作系统随机源 `system()`。

“随机”要先分用途：测试、动画、抽样和游戏地图需要可复现序列；令牌、会话标识和密钥材料需要密码学质量的熵。不要把固定种子的本地生成器用于安全用途。

## API 速查
| API | 是做什么的 |
|---|---|
| `QRandomGenerator(seed)` | 由单个种子创建可复现序列。 |
| 种子数组 / `std::seed_seq` 构造 | 用更多熵初始化本地生成器。 |
| `seed(...)` | 重新从给定种子开始生成；会重置序列位置。 |
| `generate()` / `operator()()` | 生成完整范围的 `quint32`。 |
| `generate64()` | 生成完整范围的 `quint64`。 |
| `generateDouble()` | 生成 `[0.0, 1.0)` 的双精度随机数。 |
| `bounded(highest)` | 生成 `[0, highest)` 的均匀整数或浮点数。 |
| `bounded(lowest, highest)` | 生成 `[lowest, highest)` 的均匀整数。 |
| `fillRange(buffer, count)` / `generate(begin,end)` | 批量填充随机数，减少逐次调用开销。 |
| `discard(n)` | 跳过序列中的后续 `n` 个 32 位结果。 |
| `global()` | 返回全局生成器，适合普通非安全随机需求。 |
| `system()` | 返回操作系统随机源，适合安全敏感数据。 |
| `securelySeeded()` | 创建一个由安全熵播种的独立本地生成器。 |
| `min()` / `max()` | 提供符合 UniformRandomBitGenerator 约定的范围边界。 |

## 使用场景

### 可重复的测试数据
```cpp
QRandomGenerator rng(0xC0FFEEu);
const int index = rng.bounded(items.size());
```
固定种子能让失败用例复现。记录种子而不是只记录“随机测试失败”，否则很难重建输入。

### 从集合中均匀抽取
```cpp
if (!items.isEmpty()) {
    auto &chosen = items[QRandomGenerator::global()->bounded(items.size())];
    use(chosen);
}
```
上界是排他的，正好可直接传 `size()`。空集合必须先处理，不能向 `bounded(0)` 传入无效范围。

### 安全令牌
```cpp
QByteArray bytes(32, Qt::Uninitialized);
auto *rng = QRandomGenerator::system();
for (char &byte : bytes)
    byte = char(rng->generate() & 0xff);
```
安全协议还需要正确的编码、保存期限和比较方式；随机源本身不等于完整认证方案。

## 常见坑与经验
- 所有 `bounded(lowest, highest)` 都是前闭后开，`highest` 必须大于 `lowest`。
- 想得到完整 `quint32/quint64` 范围时用 `generate/generate64`，不要试图用最大上界的 `bounded()`。
- `bounded(double)` 的无穷和 NaN 输入不会产生有意义的随机结果；先验证数值域。
- 复制普通本地生成器后，两份会从相同状态继续，因此会产生相同序列；这对测试有用，对独立流不一定合适。
- 不要复制 `global()` 以求“独占序列”；需要独立且安全播种的实例使用 `securelySeeded()`。

## 知识点覆盖
伪随机数、随机分布、前闭后开区间、种子与可复现性、UniformRandomBitGenerator、批量生成、密码学随机源、测试设计。
