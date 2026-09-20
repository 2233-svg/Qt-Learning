# Qt QHash 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QHash>`  
> 所属模块：`Qt6::Core`  
> 类型性质：隐式共享的键值哈希容器  
> 相关类型：`QMap`、`QMultiHash`、`QSet`、`QHashSeed`、`QHashIterator`

## 1. 它解决什么问题

`QHash<Key, T>` 保存一组 `(key, value)`，通过 key 快速找到对应的 value。它适合把“标识符”映射到“对象、状态、缓存结果或配置值”：

```cpp
QHash<QString, int> retryCount;
retryCount.insert("upload", 3);
retryCount["download"] = 1;

const int retries = retryCount.value("upload", 0);
```

它和 `QMap<Key, T>` 都是键值容器，但目标不同：

| 类型 | 主要保证 | 典型查找 | 遍历顺序 |
|---|---|---:|---|
| `QHash` | 通过哈希快速按 key 查找 | 平均摊销 O(1) | 任意顺序 |
| `QMap` | 按 key 排序保存 | O(log n) | 按 key 排序 |
| `QMultiHash` | 一个 key 对应多个 value | 平均摊销 O(1) | 任意顺序 |

`QHash` 只允许一个 value 对应一个 key。对已存在的 key 调用普通 `insert()` 会覆盖旧 value；需要保留多个 value 时应使用 `QMultiHash`，而不是依赖重复插入。

### 1.1 它不解决什么问题

- 不提供插入顺序，也不提供稳定的遍历顺序。
- 不保证最坏情况下仍然是 O(1)；恶意或异常的哈希分布仍可能退化。
- 不适合按 value 反向高效查找，`key()` 和 `keys(value)` 都需要线性扫描。
- 不替代对象所有权管理。`QHash<Key, QObject>` 通常不成立，应保存指针、智能指针或其他可赋值句柄。
- 不提供多个相同 key 的记录；多值关系使用 `QMultiHash`。

## 2. 实际使用场景

### 2.1 配置、缓存和计数

这是最常见的用法。key 通常是字符串、整数、枚举或轻量 ID，value 是配置值、缓存结果或计数器。

```cpp
QHash<QString, QByteArray> responseCache;

responseCache.insert("/api/version", QByteArray("6.11"));
if (responseCache.contains("/api/version")) {
    const QByteArray body = responseCache.value("/api/version");
}
```

如果缺失时要创建默认值，`operator[]` 很方便：

```cpp
++retryCount["upload"];
```

如果只是查询，使用 `value()` 或 `contains()`，不要为了读取而调用非 const 的 `operator[]`。

### 2.2 对象索引和注册表

```cpp
QHash<quint64, QObject *> objects;
objects.insert(objectId, object);

if (auto it = objects.find(objectId); it != objects.end())
    it.value()->setProperty("active", true);
```

`QHash` 不会替你删除指针指向的对象。若对象由 Qt 父子对象关系管理，hash 中的指针在对象销毁后需要同步移除；若希望弱引用自动失效，可以评估 `QPointer`。

### 2.3 去重和快速 membership test

如果只关心 key 是否出现，可以使用 `QSet<Key>`。使用 `QHash<Key, T>` 保存额外 value 时，应通过 `contains()` 表达 membership test，而不要把默认构造的 value 当成“未找到”的标志。

### 2.4 后台计算结果缓存

异步任务完成后，可以把任务 ID 映射到结果、状态或 watcher：

```cpp
QHash<QString, QFutureWatcher<QByteArray> *> watchers;
```

这类场景要另外考虑线程同步和对象生命周期。`QHash` 的隐式共享只影响容器值语义，不会让多个线程同时写同一个 hash 变得安全。

### 2.5 什么时候选择其他容器

- 需要按 key 排序、范围查询或可预测输出：`QMap`。
- 一个 key 对应多个 value：`QMultiHash`。
- 只保存唯一 key：`QSet`。
- 需要严格的插入顺序：另存一个顺序容器，或使用 `QList`/`QVector` 配合 hash 做索引。
- 需要标准库容器接口且不需要 Qt 的隐式共享：评估 `std::unordered_map`。

## 3. 构建与最小示例

`QHash` 属于 Qt Core：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QHash>
#include <QString>

int main()
{
    QHash<QString, int> hash;
    hash.reserve(3);

    hash.insert("one", 1);
    hash["two"] = 2;

    if (hash.contains("one"))
        hash.insertOrAssign("one", 10);

    for (const auto &[key, value] : std::as_const(hash).asKeyValueRange()) {
        Q_UNUSED(key);
        Q_UNUSED(value);
    }

    return 0;
}
```

`asKeyValueRange()` 自 Qt 6.4 起提供。若项目要兼容更早的 Qt 6 版本，应使用 `const_iterator`：

```cpp
for (auto it = hash.cbegin(); it != hash.cend(); ++it)
    qDebug() << it.key() << it.value();
```

## 4. 使用前必须建立的规则

### 4.1 Key 的两个契约

`Key` 至少需要满足：

1. 可以比较相等，即支持 `operator==()`；
2. 有可调用的哈希函数。

Qt 6 推荐为自定义 key 提供同一命名空间中的双参数 `qHash()`：

```cpp
class UserId
{
public:
    explicit UserId(quint64 value = 0) : m_value(value) {}

    quint64 value() const noexcept { return m_value; }

    friend bool operator==(const UserId &, const UserId &) = default;

private:
    quint64 m_value = 0;
};

inline size_t qHash(const UserId &id, size_t seed = 0) noexcept
{
    return qHash(id.value(), seed);
}
```

必须满足下面的逻辑：

```text
if (a == b) then qHash(a, seed) == qHash(b, seed)
```

反过来不要求哈希值不同。不同 key 发生碰撞是允许的，只是碰撞越多，查找性能越差。

也可以为 key 专门化 `std::hash<Key>`。如果同一个类型同时提供 `qHash()` 和 `std::hash`，Qt 优先使用 `qHash()`。

### 4.2 用 `qHashMulti()` 组合多个字段

自定义 key 通常按参与相等比较的字段计算哈希：

```cpp
struct Employee
{
    QString name;
    QDate birthday;

    friend bool operator==(const Employee &, const Employee &) = default;
};

inline size_t qHash(const Employee &employee, size_t seed = 0) noexcept
{
    return qHashMulti(seed, employee.name, employee.birthday);
}
```

参与 `operator==()` 的字段必须和参与 `qHash()` 的字段保持一致。`qHashMulti()` 的参数顺序有意义；如果一个类型的字段顺序本身没有意义，才考虑 `qHashMultiCommutative()`。

### 4.3 哈希 seed 和遍历顺序

Qt 6 默认使用 salted hash。`QHash` 会向双参数 `qHash(key, seed)` 传入 seed，用于降低攻击者预先构造哈希碰撞的可能性。

- 正常运行时 seed 通常是随机的；
- 不要依赖 hash 值、桶位置或遍历顺序；
- `QT_HASH_SEED=0` 或 `QHashSeed::setDeterministicGlobalSeed()` 可用于调试和回归复现；
- 固定 seed 也不会让 `QHash` 变成有序容器；
- Qt 7 将要求自定义 key 使用双参数哈希接口，Qt 6 中的单参数 `qHash(key)` 已弃用；
- 可以定义 `QT_NO_SINGLE_ARGUMENT_QHASH_OVERLOAD`，在 Qt 6 中提前禁止单参数重载支持。

Qt 自带的 `qHash()` 实现可能随 Qt 版本变化。不要把 `qHash()` 数值写进跨版本协议、持久化格式或测试快照中。

### 4.4 Key 在容器中必须保持可哈希

不要在元素已经存入 hash 后，改变会影响 `operator==()` 或 `qHash()` 的字段。否则元素可能仍在旧桶中，但查找会根据新哈希值去错误的桶，表现为“明明存在却查不到”。

正确做法是删除旧 key 后，以新 key 重新插入：

```cpp
const UserId oldId = id;
hash.remove(oldId);
hash.insert(newId, value);
```

### 4.5 隐式共享和 copy-on-write

`QHash` 是隐式共享类型：

```cpp
QHash<QString, int> first;
first.insert("jobs", 4);

QHash<QString, int> second = first; // 通常是 O(1)
second.insert("jobs", 5);            // 修改时分离数据
```

复制 hash 通常只增加共享引用，不立即复制全部节点。对共享实例进行写入时会 detach，第一次分离的成本与元素数量相关。

因此：

- 从函数返回 `QHash` 通常成本较低；
- 只读访问适合使用 const 对象或 const 迭代器；
- 需要独立副本时，直接复制后再修改即可；
- 共享容器的写操作不能和另一个线程的读写无同步地并发进行；
- 非 const `begin()` 可能为了提供可修改迭代器而 detach，纯遍历优先使用 `cbegin()` 或 const 对象。

### 4.6 Key 和 value 必须是可赋值的值类型

Qt 容器要求存储类型能满足 Qt 容器的赋值、构造和析构要求。不能按值存放不可复制或不适合值语义的 QObject 派生对象：

```cpp
QHash<QString, QWidget *> widgets; // 保存指针
```

保存裸指针时，hash 不拥有对象。保存 `QSharedPointer<T>`、`std::shared_ptr<T>` 或 `QPointer<T>` 时，所有权和失效语义分别由对应指针类型决定。

## 5. 插入、查询和更新：先选对语义

这些 API 名称相近，但对“已有 key”处理完全不同：

| API | key 不存在 | key 已存在 | 适合场景 |
|---|---|---|---|
| `insert(key, value)` | 插入 | 覆盖 | 明确要写入最终值 |
| `operator[](key)` | 插入默认构造 value，并返回引用 | 返回引用 | 计数器、逐步构造 value |
| `emplace(key, args...)` | 按参数构造 | 用参数重新构造 value | 需要构造参数，且允许覆盖 |
| `tryInsert(key, value)` | 插入 | 保留旧值 | 只允许首次写入 |
| `tryEmplace(key, args...)` | 按参数构造 | 不做任何插入 | 首次创建昂贵 value |
| `insertOrAssign(key, value)` | 插入 | 覆盖 | 类似 STL 的 insert-or-update |

### 5.1 读取优先使用 `value()`

```cpp
const int timeout = hash.value("timeout", 30);
```

不要把下面的代码当成普通查询：

```cpp
if (hash["timeout"] == 30) {
    // 如果 timeout 不存在，这一行已经插入了默认值
}
```

非 const `operator[]` 在 key 不存在时会插入 `T()`。当 `T` 是指针时，甚至会悄悄插入一个空指针；循环查询大量不存在的 key 可能让 hash 无意中增长。

### 5.2 `tryEmplace()` 和 `tryInsert()` 不覆盖旧值

```cpp
auto result = cache.tryEmplace(key, 1024, Qt::Uninitialized);
if (result.inserted) {
    // 只有 key 不存在时才创建 value
    initialize(*result.iterator);
}
```

如果 key 已存在，`result.iterator` 指向已有元素，`result.inserted` 为 `false`，旧 value 不会被改变。

注意：`tryEmplace(key, makeArgument())` 中的 `makeArgument()` 作为 C++ 函数实参仍会在调用前执行；`tryEmplace()` 避免的是 `T` 的构造和插入，不会自动延迟计算调用点上的参数表达式。

### 5.3 `insertOrAssign()` 的 `inserted` 语义

```cpp
auto result = hash.insertOrAssign(key, newValue);
if (!result.inserted)
    qDebug() << "key existed; value was assigned";
```

已有 key 时，`inserted == false`，但 value 仍然可能已经被覆盖。因此这里的 `inserted` 表示“是否新建 entry”，不是“是否发生了 value 修改”。

### 5.4 `emplace()` 不是 `tryEmplace()`

`emplace()` 在 key 不存在时按参数构造新 value；Qt 6.11 中 key 已存在时会用这些参数重新构造已有 value。需要“已有 key 保持原值”时必须使用 `tryEmplace()` 或 `tryInsert()`。

## 6. 遍历、修改和迭代器有效期

### 6.1 QHash 的遍历顺序不可依赖

下面的代码可以遍历全部元素，但输出顺序不应写进业务逻辑：

```cpp
for (auto it = hash.cbegin(); it != hash.cend(); ++it)
    qDebug() << it.key() << it.value();
```

如果 UI、日志、序列化或测试需要排序输出：

```cpp
QStringList keys = hash.keys();
std::sort(keys.begin(), keys.end());
for (const QString &key : keys)
    qDebug() << key << hash.value(key);
```

或者直接使用 `QMap` 保存有序映射。

### 6.2 结构化绑定访问 key/value

```cpp
for (auto [key, value] : hash.asKeyValueRange()) {
    Q_UNUSED(key);
    value += 1; // 修改 hash 中的 value
}
```

`key` 是对 hash 内 key 的 const 引用，不能通过它改变 key；非 const hash 的 range 中 `value` 可以修改容器内的 value。只读遍历可以写成：

```cpp
for (const auto &[key, value] : std::as_const(hash).asKeyValueRange())
    qDebug() << key << value;
```

### 6.3 迭代器和引用通常不要跨越容器修改保存

文档要求把由 `begin()`、`find()`、`asKeyValueRange()` 等得到的迭代器或引用视为可能在下一次非 const 成员调用后失效；容器析构后更必然失效。

尤其要小心：

- 插入可能触发 rehash；
- 写入共享 hash 可能触发 detach；
- `clear()` 会使全部元素和迭代器失效；
- 删除当前元素会使指向该元素的迭代器失效；
- 保存 `T &` 后再调用 `operator[]`、`insert()` 或 `reserve()` 不安全。

删除遍历中的当前元素时使用 `erase()` 返回的下一个迭代器：

```cpp
for (auto it = hash.begin(); it != hash.end(); ) {
    if (it.value() < 0)
        it = hash.erase(it);
    else
        ++it;
}
```

`erase(pos)` 不会让 QHash 重新哈希内部结构，并返回下一个元素的迭代器，因此这个删除循环是专门支持的安全模式。仍然不要把其他旧迭代器长期保存到后续修改之后。

### 6.4 `keyValueBegin()` 和 `keyValueEnd()`

当泛型算法需要解包成 key/value 对时，可以使用：

```cpp
for (auto it = hash.keyValueBegin(); it != hash.keyValueEnd(); ++it) {
    const auto &[key, value] = *it;
    Q_UNUSED(key);
    value += 1;
}
```

`key_value_iterator` 的 `operator*()` 返回类似 `std::pair<const Key &, T &>` 的 key/value 视图，而普通 `iterator` 的 `operator*()` 只返回 value。

## 7. 容量、内存和复杂度

### 7.1 `reserve()` 用于大量构建

```cpp
QHash<QString, Record> records;
records.reserve(expectedCount);
for (const Record &record : input)
    records.insert(record.id(), record);
```

`reserve(size)` 确保内部表能够容纳至少约 `size` 个元素而不必立即扩容。它适合已知数据规模的大批量构建，但普通代码通常不需要手工调用。

### 7.2 `capacity()` 不是元素个数

`size()` 返回元素数量；`capacity()` 返回内部哈希表可用桶容量。两者不是同一个概念：

```cpp
qDebug() << hash.size() << hash.capacity();
```

删除元素后 `QHash` 不会自动缩小。需要回收多余桶时调用 `squeeze()`，但它会带来重新组织数据的成本，通常只在内存优化阶段使用。

`clear()` 会移除所有元素并释放 hash 使用的内存。

### 7.3 STL 兼容的容量诊断 API

Qt 6.11 的头文件还提供：

- `load_factor()`：查询当前内部负载因子，主要用于诊断；
- `max_load_factor()`：返回实现目标的最大负载因子；
- `bucket_count()`：查询桶数量；
- `max_bucket_count()`：查询理论上限。

这些函数不应成为一般业务逻辑的一部分。正常性能问题先确认 key 的哈希质量、是否频繁扩容以及是否错误依赖顺序。

### 7.4 复杂度边界

- `contains()`、`find()`、`value()`、`insert()` 等按 key 操作平均摊销 O(1)；
- `keys()`、`values()`、`key(value)`、`keys(value)` 需要遍历或复制，通常是 O(n)；
- `reserve()`、`squeeze()`、copy-on-write detach 可能需要线性时间；
- 哈希碰撞严重时按 key 操作可能退化。

## 8. 版本差异和迁移要点

| API 或行为 | 引入/变化 |
|---|---|
| `removeIf()`、非成员 `erase_if()` | Qt 6.1 |
| `asKeyValueRange()` | Qt 6.4 |
| `TryEmplaceResult`、`tryEmplace()`、`tryInsert()`、`insertOrAssign()` 及 STL 风格小写接口 | Qt 6.9 |
| `insert()` 的 key/value rvalue 重载 | Qt 6.11 |
| 单参数 `qHash(key)` | Qt 6 仍兼容但已弃用，Qt 7 要求双参数形式 |

跨 Qt 版本编写自定义 key 时，直接提供带默认 seed 的双参数版本最稳妥：

```cpp
size_t qHash(const MyKey &key, size_t seed = 0) noexcept;
```

如果要提前发现遗留单参数重载，可以在 Qt 6 编译配置中定义 `QT_NO_SINGLE_ARGUMENT_QHASH_OVERLOAD`。

## 9. 逐项 API 说明

### 9.1 成员类型和别名

#### `QHash::key_type`

即模板参数 `Key`，表示键类型。

#### `QHash::mapped_type`

即模板参数 `T`，表示 value 类型。

#### `QHash::value_type`

Qt 6.11 头文件中的 value 类型别名，等同于 `T`。它和 `std::unordered_map` 的 `pair<const Key, T>` 设计不同；访问 key/value 对应使用 `key_value_iterator`。

#### `QHash::size_type`

元素数量和容量相关 API 使用的大小类型，Qt 6 中是 `qsizetype`。

#### `QHash::difference_type`

用于 STL 兼容迭代器距离的类型，Qt 6.11 头文件中为 `qsizetype`。

#### `QHash::reference`、`QHash::const_reference`

分别是 `T &` 和 `const T &` 的别名。

#### `QHash::iterator`

可修改 value 的 STL 风格前向迭代器：

- `key()` 返回 `const Key &`；
- `value()` 返回 `T &`；
- `operator*()` 返回 `T &`；
- `operator->()` 指向 value；
- 支持前置和后置 `operator++`；
- 不提供随机访问，也不能修改 key。

#### `QHash::const_iterator`

只读 STL 风格前向迭代器：

- `key()` 返回 `const Key &`；
- `value()` 返回 `const T &`；
- `operator*()` 返回 `const T &`；
- 可由 `iterator` 构造；
- 不允许修改 value。

#### `QHash::key_iterator`

只遍历 key 的 const 前向迭代器。`operator*()` 返回 `const Key &`，适合与 `keyBegin()`、`keyEnd()` 配合。

#### `QHash::key_value_iterator`

可修改 key/value 视图中的 value 的迭代器。解引用结果是 key/value 对式访问，适合结构化绑定和 STL 风格算法。

#### `QHash::const_key_value_iterator`

只读的 key/value 迭代器，解引用结果中的 key 和 value 都是 const 引用。

#### `QHash::Iterator`、`QHash::ConstIterator`

Qt 风格别名，分别等同于 `iterator` 和 `const_iterator`。

#### `QHash::TryEmplaceResult`

Qt 6.9 起提供的插入结果结构，包含：

```cpp
QHash<Key, T>::iterator iterator;
bool inserted;
```

`iterator` 指向新插入的元素，或指向已经存在且阻止插入的元素；`inserted` 只表示这次是否新建 entry。

### 9.2 构造、赋值和交换

#### `QHash()`

构造空 hash。默认构造不包含任何元素。

#### `QHash(std::initializer_list<std::pair<Key, T>> list)`

从初始化列表构造 hash：

```cpp
QHash<QString, int> hash{{"one", 1}, {"two", 2}};
```

如果列表中出现相同 key，后续插入按普通 `insert()` 规则覆盖先前 value；不要把初始化列表当成多值容器。

#### `template <typename InputIterator> QHash(InputIterator begin, InputIterator end)`

从半开区间 `[begin, end)` 构造。元素可以提供 `.first/.second`，也可以提供 `.key()/.value()`。输入元素的 key/value 必须能转换为 `Key`/`T`。

#### `QHash(const QHash &other)`

复制 hash。由于隐式共享，通常是常数时间；后续修改共享实例时触发 copy-on-write。

#### `QHash(QHash &&other)`

移动构造，接管原 hash 的内部数据。移动后的 `other` 仍是有效对象，但不应假设其中还保留原有元素。

#### `~QHash()`

销毁 hash。该 hash 中的所有迭代器、引用和指针式 value 的容器引用关系都不能继续使用；析构不会自动删除裸指针指向的对象。

#### `operator=(const QHash &other)`

复制赋值并共享数据。赋值前指向左侧旧数据的迭代器和引用不应继续使用。

#### `operator=(QHash &&other)`

移动赋值。接管 `other` 的数据并返回 `*this`。

#### `swap(QHash &other)`

交换两个 hash 的内部数据，通常是常数时间。交换后，两者保存的元素集合互换。

### 9.3 状态、容量和清理

#### `size() const`

返回元素数量，类型为 `qsizetype`。

#### `count() const`

无参数重载等同于 `size()`。

#### `isEmpty() const`

hash 没有元素时返回 `true`。

#### `empty() const`

STL 兼容名称，等同于 `isEmpty()`。

#### `capacity() const`

返回内部哈希表容量，不是元素数量。主要用于内存调优和诊断。

#### `reserve(qsizetype size)`

为至少约 `size` 个元素预留内部空间，减少大批量插入过程中的扩容。传入过小的估计不会破坏正确性，只可能少获得性能收益。

#### `squeeze()`

尝试减少内部哈希表占用的空间。删除大量元素后才可能有意义；不要在频繁增删的热路径中反复调用。

#### `clear()`

移除全部元素并释放 hash 使用的内部内存。

#### `load_factor() const`

Qt 6.11 的 STL 兼容诊断 API，返回内部负载因子。它不是业务层的元素占用百分比，也不应被用来推导遍历顺序。

#### `max_load_factor()`

静态 API，返回实现目标的最大负载因子。QHash 的容量策略由 Qt 管理，通常不需要手工调节。

#### `bucket_count() const`

返回内部桶数量，属于诊断/兼容 API。

#### `max_bucket_count()`

返回实现支持的最大桶数量，属于静态诊断/兼容 API。

### 9.4 查询和取值

#### `contains(const Key &key) const`

检查 key 是否存在，不会插入默认 value。返回 `bool`。

Qt 6.11 还提供受约束的异构查询重载；只有当 key 类型和查询类型满足 Qt 的哈希与相等比较要求时才参与重载解析。

#### `count(const Key &key) const`

返回 key 对应的元素数量。由于 `QHash` 每个 key 最多一个 value，结果只能是 `0` 或 `1`。

#### `value(const Key &key) const`

返回 key 对应的 value。key 不存在时返回 `T()`，因此无法仅通过返回值区分“缺失”和“存储了一个默认构造 value”。

#### `value(const Key &key, const T &defaultValue) const`

key 不存在时返回调用者提供的默认值，不修改 hash。

#### `operator[](const Key &key) const`

const 重载等同于 `value(key)`，返回 value 的副本，不会插入。

#### `operator[](const Key &key)`

非 const 重载返回 `T &`。key 不存在时先插入默认构造的 `T`，再返回该元素引用。这个 API 适合更新、计数和延迟初始化，不适合无副作用查询。

#### `key(const T &value) const`

在线性扫描中查找第一个匹配 value 的 key。不存在时返回默认构造的 `Key`。如果默认 key 也可能是有效 key，应使用带 `defaultKey` 的重载或先设计明确的查询状态。

#### `key(const T &value, const Key &defaultKey) const`

找不到匹配 value 时返回 `defaultKey`。按 value 查找是 O(n)，不是 hash 的快速路径。

#### `keys() const`

返回包含所有 key 的新 `QList<Key>`。顺序任意；创建列表需要线性时间和额外内存。

#### `keys(const T &value) const`

返回所有映射到指定 value 的 key。需要线性扫描，结果顺序任意。

#### `values() const`

返回包含所有 value 的新 `QList<T>`。顺序任意，但与同一 hash 的 `keys()` 返回顺序相对应；同样需要线性时间和额外内存。

### 9.5 查找和迭代器入口

#### `begin()`、`end()`

返回可修改迭代器的起点和尾后位置：

```cpp
for (auto it = hash.begin(); it != hash.end(); ++it)
    it.value() += 1;
```

非 const `begin()` 可能触发 detach；`end()` 表示尾后位置，不能解引用。

#### `begin() const`、`cbegin()`

返回 const 迭代器起点。只读遍历优先使用它们。

#### `end() const`、`cend()`

返回 const 尾后迭代器。

#### `constBegin()`、`constEnd()`

Qt 风格的 const 迭代器入口，分别对应 `cbegin()` 和 `cend()`。

#### `find(const Key &key)`

非 const 重载返回指向元素的 `iterator`；找不到返回 `end()`。找到后可以通过 `value()` 修改 value。

#### `find(const Key &key) const`

const 重载返回 `const_iterator`；找不到返回 const `end()`。

#### `constFind(const Key &key) const`

显式返回 `const_iterator` 的查找 API。它适合想明确表达只读查找的代码。

#### `equal_range(const Key &key)`

返回一对迭代器，表示匹配 key 的半开区间。由于 `QHash` 一个 key 只有一个 value，返回区间最多包含一个元素；它主要用于 STL 兼容泛型代码。

### 9.6 插入和更新

#### `insert(const Key &key, const T &value)`

插入或覆盖 key 对应 value，并返回指向最终元素的 `iterator`。key 已存在时旧 value 被替换。

#### `insert()` 的 Qt 6.11 rvalue 重载

Qt 6.11 新增：

```cpp
insert(const Key &, T &&value);
insert(Key &&, const T &value);
insert(Key &&, T &&value);
```

它们减少 key 或 value 可移动时的不必要拷贝；语义仍然是插入或覆盖。

#### `insert(const QHash &other)`

把 `other` 中所有元素插入当前 hash。共同 key 的 value 使用 `other` 中的 value 覆盖。它不是“只补缺失项”的合并操作；只补缺失项使用 `tryInsert()` 或逐项判断。

#### `emplace(const Key &key, Args &&... args)`

按参数构造 value 并返回 iterator。key 不存在时原地构造；key 已存在时 Qt 6.11 会用参数重新构造已有 value，因此它具有覆盖语义。

#### `emplace(Key &&key, Args &&... args)`

移动 key 后按参数构造或替换 value。与 const key 重载的主要差别是 key 的移动，不改变“已有 key 会更新”的语义。

#### `tryEmplace(const Key &key, Args &&... args)`

Qt 6.9 起提供。key 不存在时按参数构造 value；key 已存在时不改变旧 value。返回 `TryEmplaceResult`。

#### `tryEmplace(Key &&key, Args &&... args)`

Qt 6.9 起提供的移动 key 版本，其他语义与上一个重载相同。

#### `tryEmplace(K &&key, Args &&... args)` 的异构重载

Qt 6.9 起提供受约束的异构 key 重载。查询类型 `K` 可以和 `Key` 不同，但必须满足可哈希、可比较以及构造 `Key` 的约束。它可避免先显式构造临时 key。

#### `tryInsert(const Key &key, const T &value)`

Qt 6.9 起提供。key 不存在时插入 value；key 已存在时保留旧 value。返回 `TryEmplaceResult`。它接收 const value 引用，想按构造参数延迟构造应使用 `tryEmplace()`。

#### `tryInsert(K &&key, const T &value)` 的异构重载

Qt 6.9 起提供的异构 key 版本，value 语义与普通 `tryInsert()` 相同。

#### `insertOrAssign(const Key &key, Value &&value)`

Qt 6.9 起提供。key 不存在时插入，已存在时赋值覆盖，返回 `TryEmplaceResult`。`inserted` 只表示是否新建。

#### `insertOrAssign(Key &&key, Value &&value)` 和异构重载

分别支持移动 key 和满足约束的异构 key。最终都遵循插入或赋值覆盖语义。

#### `try_emplace(...)`

Qt 6.9 起提供的 STL 风格小写接口。它和 `tryEmplace()` 语义相同，但返回：

```cpp
std::pair<QHash<Key, T>::key_value_iterator, bool>
```

第二个成员表示是否新插入，迭代器是 key/value 迭代器。

#### `try_emplace(hint, ...)`

STL 兼容的 hint 重载。QHash 不按有序位置插入，`hint` 会被忽略；不要期待它改善插入位置或性能。

#### `insert_or_assign(...)`

Qt 6.9 起提供的 STL 风格接口，和 `insertOrAssign()` 语义相同，返回 `std::pair<key_value_iterator, bool>`。

#### `insert_or_assign(hint, ...)`

带 hint 的 STL 风格重载。`hint` 被忽略，只是为了兼容标准库风格代码。

### 9.7 删除和取出

#### `remove(const Key &key)`

删除指定 key，成功删除返回 `true`，key 不存在返回 `false`。删除后 hash 不会自动缩小。

#### `remove(K &&key)` 的异构重载

在查询类型满足异构查找约束时，可以不先构造 `Key`。

#### `removeIf(Predicate pred)`

Qt 6.1 起按谓词删除所有匹配元素，返回删除数量。谓词可以接收 `QHash::iterator`，也可以接收 key/value pair 视图：

```cpp
const qsizetype removed = hash.removeIf([](auto it) {
    return it.value() < 0;
});
```

谓词执行期间不要再对同一个 hash 做额外结构修改。

#### `erase_if(QHash &hash, Predicate pred)`

Qt 6.1 起的非成员版本，语义等同于 `hash.removeIf(pred)`，适合泛型代码和标准库风格调用。

#### `take(const Key &key)`

取出并删除指定 key 的 value。key 不存在时返回默认构造的 `T`。如果必须区分“缺失”和“存储的是默认值”，应先调用 `contains()`，或用 `find()` 获取迭代器。

#### `take(K &&key)` 的异构重载

异构 key 版本，删除和返回语义相同。

#### `erase(const_iterator pos)`

删除 `pos` 指向的元素并返回下一个元素的 iterator。它不会触发内部 rehash，适合在遍历时删除当前元素；`pos` 必须来自当前 hash，不能传 `end()`。

### 9.8 范围式 key/value 访问

#### `keyBegin()`、`keyEnd()`

返回只遍历 key 的 const 迭代器起点和尾后位置。

#### `keyValueBegin()`、`keyValueEnd()`

非 const 重载返回可修改 value 的 `key_value_iterator` 起点和尾后位置。

#### `keyValueBegin() const`、`keyValueEnd() const`

返回 const key/value 迭代器。

#### `constKeyValueBegin()`、`constKeyValueEnd()`

显式返回 const key/value 迭代器，与 const `keyValueBegin()`/`keyValueEnd()` 作用相同。

#### `asKeyValueRange()`

Qt 6.4 起提供四个 ref-qualified 重载：

```cpp
asKeyValueRange() &;
asKeyValueRange() const &;
asKeyValueRange() &&;
asKeyValueRange() const &&;
```

返回可用于 range-based for 和结构化绑定的 range。对左值 hash 返回的 range 引用原容器；对右值 hash 返回的 range 负责延续临时对象的生命周期。range 中的迭代器和引用仍受普通 QHash 失效规则约束。

## 10. 相关非成员 API

### 10.1 `operator==` 和 `operator!=`

比较两个 `QHash` 的 key/value 集合是否相同，与内部桶顺序无关。相同 key 的 value 也必须相等；不能用它判断两个 hash 是否以相同顺序插入。

### 10.2 `operator<<` 和 `operator>>`

与 `QDataStream` 配合序列化和反序列化 `QHash`：

```cpp
QDataStream stream(&device);
stream << hash;
stream >> hash;
```

`Key` 和 `T` 必须有对应的数据流操作符。因为 QHash 无序，不要把序列化字节流当成跨版本、跨实现都稳定的排序格式，除非协议另外定义了排序规则。

### 10.3 `qHash(const QHash<Key, T> &, size_t seed)`

计算一个 hash 对象的哈希值。`Key` 和 `T` 都必须支持 `qHash()`。该数值同样不应跨 Qt 版本持久化。

### 10.4 `qHashBits(const void *p, size_t len, size_t seed)`

对连续原始字节计算哈希，适合明确拥有连续内存布局的场景。不要直接把带 padding 的对象内存当作稳定对象哈希；如果数据是元素范围，应使用 `qHashRange()`。

### 10.5 `qHashMulti(size_t seed, const T &... args)`

按参数顺序组合多个字段的哈希。适合实现自定义 key 的 `qHash()`：

```cpp
return qHashMulti(seed, key.partA(), key.partB());
```

参数顺序会影响结果。

### 10.6 `qHashMultiCommutative(size_t seed, const T &... args)`

以不关心参数顺序的方式组合字段。只有在业务等价关系确实不区分顺序时才使用；如果顺序有意义，应使用 `qHashMulti()`，通常质量更好。

### 10.7 `qHashRange(first, last, seed)`

按迭代顺序组合一个范围的元素。适合 vector、array 等顺序有意义的集合。

### 10.8 `qHashRangeCommutative(first, last, seed)`

以不关心元素顺序的方式组合一个范围。适合集合语义，不适合顺序敏感的序列。

### 10.9 内置 `qHash()` 重载族

`QHash` 头文件为大量 Qt/C++ 基础类型提供哈希重载，例如整数、枚举、指针、`QChar`、`QString`、`QByteArray`、日期时间和部分 Qt 容器。自定义 key 不要依赖隐式转换“碰巧”选到正确重载，应显式提供双参数 `qHash()`。

## 11. 常见误区和排查顺序

### 11.1 查询导致 hash 变大

检查是否在非 const 对象上使用了 `operator[]`。只读查询改用：

```cpp
hash.contains(key);
hash.value(key);
hash.find(key);
```

### 11. 测试顺序偶尔变化

这是 QHash 的正常属性。不要通过固定 seed 来掩盖业务依赖；需要有序结果就用 `QMap` 或显式排序。

### 11.3 自定义 key 查不到

依次检查：

1. `operator==()` 是否比较了正确字段；
2. `qHash()` 是否使用了完全相同的字段；
3. 是否传播了 `seed`；
4. key 存入后是否修改过参与哈希的字段；
5. 是否把单参数 `qHash()` 当成 Qt 7 兼容实现。

### 11.4 已有 key 不应被覆盖却被覆盖

检查 API：

- `insert()`、`emplace()`、`insertOrAssign()` 都可能覆盖；
- `tryInsert()` 和 `tryEmplace()` 才是不覆盖策略。

### 11.5 返回 iterator 或引用后来失效

检查得到 iterator/reference 后是否调用了插入、`reserve()`、`squeeze()`、`clear()`、删除或其他非 const API。需要遍历删除时使用 `it = hash.erase(it)`。

### 11.6 `capacity()` 被误认为元素数量

元素数量使用 `size()`；桶容量使用 `capacity()` 或 `bucket_count()`。删除后容量不自动缩小是正常行为。

### 11.7 把 value 反查当成快速操作

`key(value)`、`keys(value)` 会线性扫描。若应用经常按 value 查询，应建立反向 hash，或重新设计数据模型。

## API 速查表
### 12.1 类型、构造和基础状态

| API | 作用 | 关键边界 |
|---|---|---|
| `key_type` | `Key` 类型别名 | key 必须可比较并可哈希 |
| `mapped_type` | `T` 类型别名 | value 需要满足 Qt 容器值类型要求 |
| `value_type` | value 类型别名，等同 `T` | 不等同于 STL map 的 pair |
| `size_type` | 大小类型，`qsizetype` | 用于 size/capacity |
| `difference_type` | 迭代器距离类型 | STL 兼容 |
| `iterator` | 可修改 value 的前向迭代器 | key 只读 |
| `const_iterator` | 只读前向迭代器 | 修改容器后可能失效 |
| `key_iterator` | 只遍历 key | key 只读 |
| `key_value_iterator` | 遍历 key/value 对 | 可修改 value |
| `const_key_value_iterator` | 只读 key/value 对 | key/value 都只读 |
| `Iterator` | `iterator` 的 Qt 风格别名 | 兼容旧式 Qt 代码 |
| `ConstIterator` | `const_iterator` 的 Qt 风格别名 | 兼容旧式 Qt 代码 |
| `TryEmplaceResult` | 插入结果结构 | Qt 6.9；含 `iterator`、`inserted` |
| `QHash()` | 构造空 hash | 不包含元素 |
| `QHash(initializer_list)` | 从初始化列表构造 | 重复 key 后者覆盖前者 |
| `QHash(begin, end)` | 从半开区间构造 | 元素需提供 pair 或 key/value 接口 |
| `QHash(const QHash &)` | 复制构造 | 隐式共享，通常 O(1) |
| `QHash(QHash &&)` | 移动构造 | 源对象仍有效但状态不应假设 |
| `~QHash()` | 销毁 hash | 所有迭代器和引用失效 |
| `operator=(const QHash &)` | 复制赋值 | 共享数据 |
| `operator=(QHash &&)` | 移动赋值 | 接管源数据 |
| `swap(other)` | 交换两个 hash | 通常 O(1) |
| `size()` | 返回元素数量 | 不等于桶数量 |
| `count()` | 无参时等同 `size()` | STL/Qt 兼容 |
| `isEmpty()` | 判断是否为空 | 不修改 hash |
| `empty()` | `isEmpty()` 的 STL 名称 | 不修改 hash |

### 12.2 查询和取值

| API | 作用 | 关键边界 |
|---|---|---|
| `contains(key)` | 检查 key 是否存在 | 不会插入默认 value |
| `count(key)` | 返回 key 的数量 | `QHash` 中只能是 0 或 1 |
| `value(key)` | 读取 value | 缺失时返回 `T()` |
| `value(key, defaultValue)` | 带默认值读取 | 缺失时不修改 hash |
| `operator[](key) const` | const 查询 | 缺失时不插入，返回 value 副本 |
| `operator[](key)` | 可写访问 | 缺失时插入默认 value |
| `key(value)` | 按 value 找一个 key | O(n)，缺失返回默认 key |
| `key(value, defaultKey)` | 按 value 找 key | 缺失返回指定默认 key |
| `keys()` | 复制出全部 key | O(n)，顺序任意 |
| `keys(value)` | 找出匹配 value 的 key | O(n)，顺序任意 |
| `values()` | 复制出全部 value | O(n)，顺序任意 |
| `find(key)` | 返回可修改 iterator | 缺失返回 `end()` |
| `find(key) const` | 返回 const iterator | 缺失返回 const `end()` |
| `constFind(key)` | 显式只读查找 | 缺失返回 const `end()` |
| `equal_range(key)` | 返回匹配区间 | 最多一个元素 |

### 12.3 插入和更新

| API | 作用 | 关键边界 |
|---|---|---|
| `insert(key, value)` | 插入或覆盖 | 返回最终元素 iterator |
| `insert(other)` | 合并另一个 hash | 同 key 使用 `other` 的 value |
| rvalue `insert()` 重载 | 减少移动 key/value 的拷贝 | Qt 6.11 |
| `emplace(key, args...)` | 按参数构造 value | 已有 key 时会更新/重构 value |
| `tryInsert(key, value)` | 只在缺失时插入 | 已有 key 不覆盖；Qt 6.9 |
| `tryEmplace(key, args...)` | 缺失时原地构造 | 已有 key 不改；Qt 6.9 |
| `insertOrAssign(key, value)` | 缺失插入，已有覆盖 | `inserted == false` 仍可能改 value；Qt 6.9 |
| `try_emplace(...)` | STL 风格不覆盖插入 | 返回 `pair<key_value_iterator, bool>`；Qt 6.9 |
| `try_emplace(hint, ...)` | 带 hint 的兼容重载 | hint 被忽略 |
| `insert_or_assign(...)` | STL 风格插入或覆盖 | 返回 pair；Qt 6.9 |
| `insert_or_assign(hint, ...)` | 带 hint 的兼容重载 | hint 被忽略 |

### 12.4 删除、容量和遍历

| API | 作用 | 关键边界 |
|---|---|---|
| `remove(key)` | 删除 key | 返回是否删除成功 |
| `removeIf(pred)` | 按谓词删除 | 返回删除数量；Qt 6.1 |
| `erase_if(hash, pred)` | 非成员按谓词删除 | 等同 `removeIf`；Qt 6.1 |
| `take(key)` | 取出并删除 value | 缺失返回 `T()`，无法单独区分默认值 |
| `erase(pos)` | 删除当前迭代器元素 | 返回下一个 iterator，不重新哈希 |
| `clear()` | 清空并释放内部内存 | 全部 iterator/reference 失效 |
| `reserve(size)` | 预留元素空间 | 适合大批量构建 |
| `capacity()` | 查询内部桶容量 | 不是元素数量 |
| `squeeze()` | 尝试释放多余桶 | 不要频繁调用 |
| `load_factor()` | 查询内部负载因子 | 诊断用途 |
| `max_load_factor()` | 查询目标最大负载因子 | 静态诊断 API |
| `bucket_count()` | 查询桶数量 | STL 兼容诊断 API |
| `max_bucket_count()` | 查询最大桶数量 | STL 兼容静态 API |
| `begin()` / `end()` | 可修改遍历 | 非 const begin 可能 detach |
| `cbegin()` / `cend()` | const 遍历 | 只读首选 |
| `constBegin()` / `constEnd()` | Qt 风格 const 遍历 | 等同 cbegin/cend |
| `keyBegin()` / `keyEnd()` | 只遍历 key | key 只读 |
| `keyValueBegin()` / `keyValueEnd()` | 遍历 key/value 对 | 非 const 可改 value |
| `constKeyValueBegin()` / `constKeyValueEnd()` | const key/value 遍历 | 只读 |
| `asKeyValueRange()` | 结构化绑定遍历 | Qt 6.4；引用受失效规则约束 |

### 12.5 非成员和哈希辅助 API

| API | 作用 | 关键边界 |
|---|---|---|
| `operator==(lhs, rhs)` | 比较两个 hash 内容 | 与桶顺序无关 |
| `operator!=(lhs, rhs)` | 不等比较 | 与桶顺序无关 |
| `operator<<(QDataStream &, hash)` | 写入数据流 | key/value 需支持流操作 |
| `operator>>(QDataStream &, hash)` | 从数据流读取 | 不应依赖无序输出顺序 |
| `qHash(hash, seed)` | 对 QHash 本身求哈希 | Key/T 都需可哈希 |
| `qHashBits(p, len, seed)` | 对连续原始字节求哈希 | 不适合带 padding 的对象 |
| `qHashMulti(seed, args...)` | 顺序敏感地组合字段 | 字段顺序影响结果 |
| `qHashMultiCommutative(seed, args...)` | 无序地组合字段 | 只用于顺序无意义的值 |
| `qHashRange(first, last, seed)` | 顺序敏感地组合范围 | 适合序列 |
| `qHashRangeCommutative(first, last, seed)` | 无序地组合范围 | 适合集合 |
| 双参数 `qHash(key, seed)` | 自定义 key 哈希入口 | Qt 6 推荐，Qt 7 必需 |
| `QT_NO_SINGLE_ARGUMENT_QHASH_OVERLOAD` | 禁止单参数 qHash 兼容路径 | 用于提前迁移检查 |

## 13. 选型结论

把 `QHash` 当成“无序、单值、按 key 快速查找的隐式共享字典”最准确：

- 读取时优先 `value()`/`contains()`；
- 新建且不覆盖时用 `tryEmplace()` 或 `tryInsert()`；
- 必须覆盖时用 `insert()`、`emplace()` 或 `insertOrAssign()`；
- 需要稳定顺序时使用 `QMap` 或显式排序；
- 自定义 key 始终实现双参数 `qHash()`，并传播 seed；
- 把迭代器、引用和容量调优 API 都视为有明确失效和性能边界的工具，不要把它们当成普通字段访问。
