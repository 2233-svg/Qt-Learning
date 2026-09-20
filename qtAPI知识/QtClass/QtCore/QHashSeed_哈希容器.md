# Qt QHashSeed 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QHashSeed>`  
> 所属模块：`Qt6::Core`  
> 类型性质：表示 salted hash 种子的轻量值类型  
> 相关类型：`QHash`、`qHash`、`QRandomGenerator`

## 1. 它解决什么问题

`QHashSeed` 表示 Qt 哈希算法使用的种子。`QHash` 不只对 key 做固定哈希，而是把一个运行时 seed 传给双参数 `qHash(key, seed)`，让相同 key 在不同进程或不同运行期间不必产生可预测的桶分布和遍历顺序。

这种随机化主要解决哈希表被外部输入构造出退化分布的问题，也让攻击者更难预先推断桶位置。大多数应用不需要直接操作 `QHashSeed`，因为 `QHash` 会自动管理它。

它适合两类显式场景：

- 自己实现和 `QHash` 一致的 salted hash；
- 调试或回归测试时临时要求确定性的哈希行为。

## 2. 实际使用场景

### 2.1 读取当前全局 seed

```cpp
const QHashSeed seed = QHashSeed::globalSeed();
const size_t rawSeed = seed;
```

如果程序已经进入确定性模式，`globalSeed()` 返回的值为 0。

### 2.2 为自定义哈希函数使用 seed

Qt 6 推荐为自定义 key 提供双参数重载：

```cpp
struct UserId
{
    int value;
};

size_t qHash(const UserId &id, size_t seed = 0) noexcept
{
    return qHash(id.value, seed);
}
```

`QHash` 会把自己的 seed 传入这个重载。不要在 `qHash` 中忽略 seed 后再假设遍历顺序具有随机化保护。

### 2.3 调试时固定哈希行为

```cpp
QHashSeed::setDeterministicGlobalSeed();
```

它会把全局 seed 置为 0，并要求 `qHash()` 使用确定性的哈希路径，便于复现测试。但这只适合调试和回归定位，不应作为生产配置。

## 3. salted hash 和顺序边界

### 3.1 QHash 本来就无序

即使 seed 固定，`QHash` 也不是按 key 排序的容器。确定性 seed 只能帮助复现当前版本和实现下的哈希行为，不能把 `QHash` 变成有序容器。需要稳定的 key 顺序时使用 `QMap` 或先提取 key 再排序。

### 3.2 seed 可能在进程生命周期内变化

调用 `resetRandomGlobalSeed()` 会重新生成随机 seed。保存 seed 的代码必须把之前的值存下来，不能每次重新调用 `globalSeed()` 再认为得到的是同一个 seed。

如果 seed 变化，依赖旧 seed 的自定义哈希分组、缓存键或调试快照不能直接和新值混用。

### 3.3 环境变量 `QT_HASH_SEED`

把 `QT_HASH_SEED` 设为 `0` 会启用确定性模式。其他值不会按文档产生同样的强制确定性效果。环境变量会影响全局行为，测试脚本应明确设置和清理，避免污染同一进程中的其他测试。

## 4. 构建和线程边界

`QHashSeed` 是 Core 中的轻量类型：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

`globalSeed()`、`resetRandomGlobalSeed()` 和 `setDeterministicGlobalSeed()` 都是线程安全的全局 seed 操作。线程安全只说明 seed 状态操作不会因为并发调用破坏自身；它不保证你用 seed 派生的业务缓存或自定义数据结构自动线程安全。

## 5. 逐项 API 说明

#### `[constexpr] QHashSeed::QHashSeed(size_t data = 0)`

用 `data` 构造一个 seed 值对象。默认值为 0；在 Qt 的确定性模式中，0 也具有“固定哈希”语义。

这个构造函数只包装数值，不会修改 Qt 的全局 seed。

#### `[static noexcept] QHashSeed QHashSeed::globalSeed()`

返回当前全局 QHash seed：

- 正常随机模式下返回当前随机值；
- 调用过 `setDeterministicGlobalSeed()` 或 `QT_HASH_SEED=0` 时返回 0；
- 函数本身线程安全；
- 每次调用得到的值不保证永久不变，因为可以调用 `resetRandomGlobalSeed()`。

#### `[static] void QHashSeed::resetRandomGlobalSeed()`

把 Qt 哈希 seed 重新设为新的随机值。Qt 在应用运行期间不会自动调用它；长时间运行、且哈希信息可能已经暴露给攻击者的应用可以主动重新播种。

当 `QT_HASH_SEED` 为 0 时，该函数不产生效果。调用后不要继续假设之前保存的 seed 代表全局当前 seed。

#### `[static] void QHashSeed::setDeterministicGlobalSeed()`

把全局 seed 强制为 0，并请求 `qHash()` 使用预先确定的哈希函数。它适合调试，不适合生产环境。

恢复正常随机模式调用 `resetRandomGlobalSeed()`；但如果 `QT_HASH_SEED=0`，恢复调用仍会被环境变量限制。

#### `[constexpr noexcept] QHashSeed::operator size_t() const`

把 seed 值转换为 `size_t`，便于传给自定义哈希算法或保存为数值。转换只读取当前对象，不读取或改变全局 seed。

## API 速查表
| API | 作用 | 关键边界 |
|---|---|---|
| `QHashSeed(data = 0)` | 构造 seed 值对象 | 不修改全局 seed |
| `globalSeed()` | 获取当前全局 seed | 可能因重新播种而变化；线程安全 |
| `resetRandomGlobalSeed()` | 重新生成随机 seed | `QT_HASH_SEED=0` 时无操作 |
| `setDeterministicGlobalSeed()` | 强制 seed 为 0 | 只用于调试和复现 |
| `operator size_t()` | 取出数值 | 只读当前对象 |
| `QT_HASH_SEED=0` | 通过环境变量启用确定性模式 | 影响进程全局哈希行为 |

## 7. 使用建议

- 自定义 `qHash` 优先提供 `(const Key &, size_t seed)` 重载，并把 seed 继续传给组合字段的 `qHash`。
- 不要依赖 QHash 的遍历顺序，即使测试中开启了确定性 seed。
- 需要复现 bug 时固定 seed，并记录 Qt 版本、编译器和 key 类型的哈希实现。
- 改变全局 seed 前确认进程内没有依赖旧 seed 的跨组件协议或缓存。
- 生产安全性和随机数需求使用 `QRandomGenerator` 等专门 API，不要把 hash seed 当作通用密码学随机源。

## 8. 排查顺序

1. 测试顺序不稳定，先检查是否错误依赖了 `QHash` 的遍历顺序。
2. 自定义 key 的哈希分布异常，确认使用了双参数 `qHash` 并传播 seed。
3. 调试中 `globalSeed()` 为 0，检查 `setDeterministicGlobalSeed()` 和 `QT_HASH_SEED`。
4. 重新播种后结果变化，确认代码是否缓存了旧 seed 或旧桶分布。
5. 想要排序结果时，停止调 seed，改用 `QMap` 或显式排序。
