# QMultiHash：允许重复键的哈希表

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QMultiHash>`  
> 模块：`Qt6::Core`  
> 类型：`template <typename Key, typename T> class QMultiHash`  
> 相关类型：`QHash`、`QMultiMap`、`QHashIterator`、`QMutableHashIterator`

`QMultiHash<Key, T>` 是一个允许同一 `Key` 关联多个 `T` 的哈希容器。它适合“按键快速归类，同时每个类别有多个条目”的数据，不保证全局遍历顺序，也不按键排序。

## 它解决什么问题

普通 `QHash<Key, T>` 中一个键只保留一个值，再次插入相同键相当于替换旧值。`QMultiHash` 则把每一次插入都保留为独立的 `(key, value)` 项。

典型场景：

- 按用户 ID 索引该用户的多条消息或订阅；
- 按文件扩展名索引多个处理器；
- 按事件类型索引多个处理规则；
- 按标签索引多个对象；
- 构建反向索引，例如“单词 -> 出现位置列表”。

若需要键有严格排序，使用 `QMultiMap`；若每键只有一个当前值，使用 `QHash`；若只是去重集合，使用 `QSet`。

```cpp
#include <QMultiHash>
#include <QString>

QMultiHash<QString, QString> handlers;
handlers.insert("image/png", "builtin-preview");
handlers.insert("image/png", "third-party-export");
handlers.insert("text/plain", "plain-text-viewer");

// 同一 key 的值按“最近插入 -> 最早插入”出现。
const QList<QString> pngHandlers = handlers.values("image/png");
// {"third-party-export", "builtin-preview"}
```

## 数据模型与顺序边界

`QMultiHash` 是哈希表，不是按键排序的多值 map。

- 不同键之间的遍历顺序是任意的，不能用于展示顺序、序列化稳定顺序或测试断言。
- 同一键的所有项会连续出现，且顺序是**最近插入的值在前**、最早插入的值在后。
- `size()` 统计全部 `(key, value)` 项，不是不同键的数量。
- `uniqueKeys().size()` 才接近“不同键的数量”，但会构造一个新 `QList`。
- 同一个 `(key, value)` 也可重复插入；它们是多个独立条目。

Qt 对哈希计算默认带有每进程随机种子，因此即使输入相同，跨进程得到的全局遍历顺序也不应被视为稳定。`QT_HASH_SEED=0` 或 `QHashSeed::setDeterministicGlobalSeed()` 可用于调试或回归测试，不应被当成业务排序方案。

## 类型要求与自定义键

`Key` 与 `T` 必须是可赋值的数据类型。键还必须满足：

1. `operator==()` 能判断相等；
2. 在键类型所在命名空间提供 `qHash(const Key &, size_t seed)`，或提供兼容的 `std::hash` 特化。

正确的哈希函数必须保持：若 `a == b`，则 `qHash(a, seed) == qHash(b, seed)`。它应尽量让不同键分散到不同哈希值；糟糕的哈希分布会把平均接近 O(1) 的按键查询退化为 O(n)。

```cpp
struct DeviceKey {
    QString vendor;
    quint32 product = 0;

    bool operator==(const DeviceKey &other) const noexcept
    {
        return vendor == other.vendor && product == other.product;
    }
};

inline size_t qHash(const DeviceKey &key, size_t seed = 0) noexcept
{
    return qHashMulti(seed, key.vendor, key.product);
}

QMultiHash<DeviceKey, QString> drivers;
```

不要依赖 Qt 内置 `qHash()` 的具体数值跨 Qt 版本保持一致；它只是容器内部散列所需的实现细节。

## 最常用的插入、替换与读取

`insert()` 和 `replace()` 的差异是本类最重要的语义边界。

```cpp
QMultiHash<QString, int> scores;

scores.insert("alice", 82);
scores.insert("alice", 91);
// "alice" 现在有两个值：91, 82

scores.replace("alice", 95);
// 只替换最近插入的那一个，结果为：95, 82

const int latest = scores.value("alice");       // 95
const QList<int> all = scores.values("alice");  // {95, 82}
```

| 需求 | 应用 API | 结果 |
| --- | --- | --- |
| 保留一个新条目，即使键已经存在 | `insert()` / `emplace()` | 增加 `size()`；新值成为该键的最新值。 |
| 更新该键当前最新的值 | `replace()` / `emplaceReplace()` | 若键存在，只覆盖最近插入的一项；若不存在，插入一项。 |
| 读取当前最新值 | `value(key)` | 没有该键时返回 `T()` 或传入的默认值。 |
| 取出并删除当前最新值 | `take(key)` | 仅删除最近插入的一项；缺失时返回默认构造的 `T`。 |
| 读取该键的全部值 | `values(key)` | 返回一个新 `QList<T>`，顺序为最近到最早。 |
| 删除该键的全部值 | `remove(key)` | 返回删除的项目数。 |

`value()` 和 `take()` 都只作用于“最近插入”的值；这不是随机挑选。若 `T()` 本身也可能是有效业务值，不能仅凭 `value(key) == T()` 判断键是否存在，应先调用 `contains(key)` 或 `count(key)`。

## 高效遍历同一键的多值

`values(key)` 最易用，但会分配并复制一个 `QList`。对热路径或大结果集，更适合使用 `equal_range()`，或者从 `constFind(key)` 起遍历到键变化为止。

```cpp
QMultiHash<QString, int> readings;
readings.insert("sensor-A", 10);
readings.insert("sensor-A", 12);
readings.insert("sensor-B", 20);

const auto [first, last] = std::as_const(readings).equal_range("sensor-A");
for (auto it = first; it != last; ++it)
    qDebug() << it.key() << it.value();
```

`equal_range(key)` 返回的半开区间 `[first, last)` 恰好覆盖该键的全部值；找不到键时两个迭代器都等于 `end()`。由于同键条目连续，它是比“遍历整个容器并比较 key”更直接的表达。

## 迭代器、隐式共享与失效

`QMultiHash` 是隐式共享值类型：拷贝容器通常只增加引用计数，首次对其中一个副本做非 const 修改时才分离（copy-on-write）。这让按值返回或传参较便宜，但也使迭代器边界格外重要。

- 任意非 const 成员调用后，都应认为此前取得的迭代器、引用和 `asKeyValueRange()` 解构出的引用失效。
- 非 const `begin()`、`find()` 等即使只是为了读取，也可能因隐式共享而触发分离；只读遍历优先使用 `cbegin()`、`constFind()` 或 `std::as_const(hash)`。
- 容器被销毁后，全部迭代器和引用当然失效。
- `erase(it)` 是遍历中删除的例外用法：它不会触发 rehash，返回下一个位置的迭代器；仍应使用它的返回值继续循环。
- 不要在一个容器的迭代器仍活跃时随意复制并修改其隐式共享副本，这容易落入 Qt 容器的 implicit-sharing iterator problem。

```cpp
for (auto it = values.begin(); it != values.end(); ) {
    if (it.value() < 0)
        it = values.erase(it); // 用返回的下一个位置继续
    else
        ++it;
}
```

`asKeyValueRange()`（Qt 6.4 起）让范围 for 支持结构化绑定；可变容器上得到的 `value` 是原容器中的引用，修改它会直接修改值。键通过该范围也是引用，但键不应被改动，因为会破坏哈希表定位。

```cpp
for (auto [key, value] : readings.asKeyValueRange()) {
    Q_UNUSED(key);
    value += 1; // 修改 readings 内部的值
}
```

## 容量、性能与线程

哈希表的按键查找、插入、删除平均为常数时间；大量哈希冲突时可能退化。若提前知道将插入约 `n` 个条目，先调用 `reserve(n)` 可减少反复 rehash 和元素迁移。

```cpp
QMultiHash<QString, QByteArray> index;
index.reserve(expectedRecordCount);
```

`capacity()` 是无需 rehash 可容纳的项目数估计；`squeeze()` 尝试收缩多余容量；`load_factor()`、`bucket_count()`、`max_load_factor()` 和 `max_bucket_count()` 是偏底层的哈希表诊断信息，普通业务代码很少需要依赖它们。

本类可重入。多个线程分别操作各自的 `QMultiHash` 实例没有问题；同一个实例在所有线程都只读时也可安全共享。任何线程写入同一实例时，调用方必须自行加锁，并且不能让其他线程同时使用该容器的迭代器或引用。

## 版本说明：`operator[]` 文档不一致

Qt 6.11.1 的 `QMultiHash` 详细说明仍写着“没有 `operator[]`”，但同页的成员列表以及实际 `qhash.h` 都公开了：

```cpp
T &operator[](const Key &key);
const T operator[](const Key &key) const;
```

因此 Qt 6.11.1 中该 API 实际可用：非 const `operator[]` 在键不存在时插入 `T()`，键有多个值时返回最近插入值的可写引用；const 版本等同于读取 `value(key)`。这是一处离线说明文本滞后的地方。为了避免无意插入，查询场景仍优先使用 `value()` 或 `contains()`。

## 构造与合并

`QMultiHash` 支持默认构造、初始化列表、迭代器范围、拷贝和移动。由 `QHash<Key, T>` 构造或 `unite()` 时，每个键值对都会成为一个 `QMultiHash` 条目。

```cpp
QMultiHash<QString, int> a{
    {"temperature", 20},
    {"temperature", 21},
    {"pressure", 100}
};

QMultiHash<QString, int> b;
b.insert("temperature", 22);

QMultiHash<QString, int> all = a + b; // 三个 temperature 项都会保留
```

`unite(other)`、`operator+=` 直接把 `other` 的所有项插入当前容器；`operator+` 返回合并后的新容器。它们不会因为键相同而做去重或替换。

## 常见错误

### 以为相同键会覆盖旧值

`insert()` 一定追加一项。只想维护每键一个当前值时，请用 `QHash`，或在 `QMultiHash` 中改用 `replace()`。

### 以为 `remove(key, value)` 只删一项

它会删除所有完全相同的 `(key, value)` 项。若只删当前迭代器指向的一项，使用 `erase(it)`。

### 用 `value()` 判断键是否存在

键缺失时返回 `T()`；当默认构造值本身合法时会混淆“缺失”与“值恰好等于默认值”。先用 `contains(key)` 或 `count(key)`。

### 把 `keys()` / `values()` 当零成本视图

两者都会构造新的 `QList`，且全量版本是线性时间和额外内存。只需遍历时使用迭代器、`asKeyValueRange()` 或 `equal_range()`。

### 依赖遍历顺序

除同键条目保持最近插入到最早插入的连续顺序外，哈希表的全局顺序没有承诺，且可受哈希随机化、扩容和 Qt 版本影响。

### 用指针存对象却误以为容器管理对象

`QMultiHash<Key, QObject *>` 只保存指针值，不拥有 `QObject`。删除条目不会删除对象；对象的生命周期仍由父对象、智能指针或其他所有权策略管理。

## API 速查表

### 类型、构造与值语义

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `key_type`、`mapped_type`、`value_type`、`size_type` 等 | STL 风格类型别名。 | `value_type` 是 `T`，单次迭代的 `*it` 也是值而非键值对。 |
| `iterator` / `const_iterator` | 遍历值，配合 `it.key()` 和 `it.value()` 访问键和值。 | 任意非 const 操作后视为失效；读遍历优先 const 迭代器。 |
| `key_iterator` | 仅遍历每个条目的键。 | 重复键会重复出现。 |
| `key_value_iterator` / `const_key_value_iterator` | 解引用得到键值对引用。 | 适合结构化绑定；可变版本只能安全修改 value，不能修改 key。 |
| `QMultiHash()` | 构造空容器。 | `size()` 为 0。 |
| `QMultiHash({{key, value}, ...})` | 从初始化列表构造。 | 每个 pair 都插入；重复键和值都保留。 |
| `QMultiHash(first, last)` | 从 pair-like 或有 `key()` / `value()` 的迭代器范围构造。 | 复制区间 `[first, last)` 的每一项。 |
| `QMultiHash(const QHash<Key, T> &)` | 从单值哈希构造。 | 每个 `QHash` 项变成一条多值项。 |
| 拷贝 / 移动 / 赋值 | 复制或转移容器。 | 拷贝采用隐式共享；首次写入可能产生线性时间分离。 |
| `swap(other)` | 快速交换两个容器。 | `noexcept`，不逐项复制。 |

### 容量、共享与整体状态

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `size()` / `count()` | 返回总条目数。 | 同一 key 的多条记录分别计数。 |
| `isEmpty()` / `empty()` | 判断是否没有任何条目。 | 不区分键数量。 |
| `capacity()` | 返回当前容量估计。 | 不要把它当作 size 或不同键数量。 |
| `reserve(n)` | 为约 `n` 条目预留容量。 | 大批量插入前调用可减少 rehash；会使旧迭代器/引用不可靠。 |
| `squeeze()` | 尝试收缩多余容量。 | 可能重新分配；旧迭代器/引用失效。 |
| `detach()` | 强制当前实例脱离共享数据。 | 极少需要手动调用；用于明确把 copy-on-write 成本放在可控位置。 |
| `isDetached()` | 查询是否独占内部数据。 | `false` 不表示不可读，只表示下一次写可能复制。 |
| `isSharedWith(other)` | 判断是否与另一个 `QMultiHash` 共享内部数据。 | 是实现/优化诊断接口，不是内容相等比较。 |
| `load_factor()` / `max_load_factor()` | 查询当前/最大装载因子。 | 偏底层性能诊断；最大值在 Qt 6.11.1 为 `0.5`。 |
| `bucket_count()` / `max_bucket_count()` | 查询桶数量/上限。 | 不要把桶序号或数量用于业务逻辑。 |
| `clear()` | 删除全部条目并释放所用内存。 | 容器变空；所有迭代器和引用失效。 |

### 插入、替换与合并

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `insert(key, value)` | 新增一条 `(key, value)`。 | 即使 key 已存在也会保留新项；Qt 6.11 起有 key/value 的移动重载。 |
| `emplace(key, args...)` | 原地构造并新增一条值。 | 与 `insert()` 一样不覆盖旧项；适合避免临时 `T`。 |
| `replace(key, value)` | 插入或更新该键最近插入的一项。 | 多个同键值时只替换最新项，不会清掉其余项。 |
| `emplaceReplace(key, args...)` | 原地构造后插入或替换最新项。 | 行为与 `replace()` 相同，减少临时对象。 |
| `operator[](key)` | 返回该键最新值的可写引用。 | 键缺失时插入 `T()`；同键多个值时只访问最新项。 |
| `unite(const QHash &)` | 合并单值哈希。 | 把 `other` 的每项作为新条目插入。 |
| `unite(const QMultiHash &)` | 合并另一多值哈希。 | 不去重、不替换，返回 `*this`。 |
| `operator+=(other)` / `operator+(other)` | 原地合并 / 返回合并副本。 | 相同键依然保留多项。 |

### 按键和值查询

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `contains(key)` | 判断是否至少有一项使用该键。 | 适合区分键缺失与默认值。 |
| `contains(key, value)` | 判断是否存在匹配的键值对。 | 只判断存在性，不报告重复次数。 |
| `count(key)` | 返回该键关联的条目数。 | 不同于无参 `count()`，后者等于总 `size()`。 |
| `count(key, value)` | 返回完全相同键值对的重复次数。 | 用于确认重复插入的数量。 |
| `value(key)` / `value(key, defaultValue)` | 返回该键最近插入的值。 | 缺失时返回 `T()` 或给定默认值；返回的是拷贝。 |
| `values(key)` | 返回该键的所有值。 | 新建 `QList<T>`；顺序为最近插入到最早插入。 |
| `values()` | 返回所有值。 | 新建列表，键间顺序任意；与 `keys()` 结果位置一一对应。 |
| `key(value)` / `key(value, defaultKey)` | 查找一个映射到该值的键。 | 线性时间；值有多个键时“第一个”没有稳定业务含义。 |
| `keys(value)` | 返回所有映射到该值的键。 | 会创建列表，且重复键可重复出现。 |
| `keys()` | 返回每个条目的键。 | 新建列表、顺序任意、重复键重复出现；和 `values()` 位置对应。 |
| `uniqueKeys()` | 返回每个不同键一次。 | 新建列表、顺序任意。 |

### 查找与遍历

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `begin()` / `end()` | 取得可写迭代器边界。 | `begin()` 可能触发隐式分离；任何后续非 const 调用会使迭代器/引用失效。 |
| `cbegin()` / `cend()`、`constBegin()` / `constEnd()` | 取得只读迭代器边界。 | 纯读取优先使用，避免不必要 detach。 |
| `find(key)` / `constFind(key)` | 定位该键最近插入的一项。 | 未找到返回 `end()`；随后可沿同键连续区间继续迭代。 |
| `find(key, value)` / `constFind(key, value)` | 定位一个精确键值对。 | 若有重复，定位最近插入的一项；未找到返回结束迭代器。 |
| `equal_range(key)` | 返回该键所有值的 `[first, last)` 区间。 | 未找到时二者都为 `end()`；热路径上优于 `values(key)` 的复制。 |
| `keyBegin()` / `keyEnd()` | 仅遍历每个条目的键。 | 重复键仍会出现多次。 |
| `keyValueBegin()` / `keyValueEnd()` | 用键值迭代器遍历。 | `*it` 是键值对引用；有 const 和非 const 重载。 |
| `constKeyValueBegin()` / `constKeyValueEnd()` | 只读键值迭代器边界。 | 避免因读取而 detach。 |
| `asKeyValueRange()` | 用范围 for 迭代键值对，Qt 6.4 起。 | 解构出的 key/value 是容器内部引用；可变 range 中改 value 会改容器。 |

### 删除

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `remove(key)` | 删除该键的全部条目。 | 返回删除数量。 |
| `remove(key, value)` | 删除所有匹配的键值对。 | 不是删除一条；重复项会全删。 |
| `take(key)` | 移除并返回该键最新值。 | 仅移除一条；缺失时返回 `T()`；若不需要返回值，用 `remove(key)` 更合适。 |
| `erase(pos)` | 删除迭代器所指的一条。 | 不 rehash，返回下一个迭代器，适合边遍历边删除。 |
| `removeIf(pred)` | 删除谓词返回 `true` 的所有项，Qt 6.1 起。 | 谓词参数可为 `iterator` 或 `std::pair<const Key &, T &>`；返回删除数量。 |
| `erase_if(hash, pred)` | `removeIf` 的非成员形式，Qt 6.1 起。 | 语义相同，便于泛型算法风格代码。 |

### 比较、散列与流

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `operator==` / `operator!=` | 比较两个多值哈希。 | 比较键值对集合语义，不应依赖内部遍历顺序；`T` 需支持 `operator==`。 |
| `qHash(const QMultiHash &, size_t seed)` | 计算整个容器的哈希值。 | `Key` 和 `T` 均须可 `qHash`；用于把 `QMultiHash` 再作为哈希键的少见场景。 |
| `QDataStream << hash` | 写入二进制数据流。 | `Key` 和 `T` 必须支持 `operator<<`；设置流版本以维护持久化兼容性。 |
| `QDataStream >> hash` | 从二进制数据流读取。 | `Key` 和 `T` 必须支持 `operator>>`；处理 `QDataStream` 状态错误。 |

## 一句话总结

`QMultiHash` 用于“一个键对应多条记录”的快速索引：`insert()` 追加，`replace()` 只改最新项，`values(key)` 按新到旧返回全部同键值；不要依赖全局顺序，并把迭代器和引用严格限制在下一次非 const 操作之前。
