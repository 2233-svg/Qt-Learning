# QMultiMap：按键排序的一对多映射

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QMultiMap>`  
> 模块：`Qt6::Core`  
> 类型：`template <typename Key, typename T> class QMultiMap`  
> 相关类型：`QMap`、`QMultiHash`、`std::multimap`

`QMultiMap<Key, T>` 是允许重复键的有序关联容器。它按 `Key` 升序保存所有 `(key, value)` 项，同一键可以有多条记录；同键记录中，最近插入的值排在前面。

## 它解决什么问题

当数据既需要“一键多值”，又需要按键稳定排序、范围查询或顺序遍历时，`QMultiMap` 比 `QMultiHash` 更合适。

常见场景：

- 时间戳或优先级到多个任务的索引；
- 分类 ID 到多条有序记录；
- 配置层级、路由规则或区间边界的查找；
- 根据键区间做批处理，例如处理 `[beginKey, endKey)` 内的事件；
- 需要最小键、最大键、`lowerBound()` 和 `upperBound()` 的数据结构。

```cpp
#include <QMultiMap>
#include <QString>

QMultiMap<int, QString> queue;
queue.insert(20, "background-sync");
queue.insert(10, "open-document");
queue.insert(20, "refresh-thumbnail");

// 遍历顺序按 key 升序：
// (10, "open-document"),
// (20, "refresh-thumbnail"), (20, "background-sync")
```

## `QMultiMap`、`QMultiHash` 与 `QMap` 如何选

| 容器 | 一个键可有多个值 | 键顺序 | 典型优势 |
| --- | --- | --- | --- |
| `QMap<Key, T>` | 否 | 升序 | 一个键对应一个当前值，需要范围查询或有序遍历。 |
| `QMultiMap<Key, T>` | 是 | 升序 | 一对多、相同键连续、需要上下界或有序输出。 |
| `QHash<Key, T>` | 否 | 无保证 | 平均按键查找更快。 |
| `QMultiHash<Key, T>` | 是 | 无保证 | 一对多且更在意平均查询速度，不需要排序。 |

`QMultiMap` 的查找、插入、删除基于平衡树，通常为 O(log n)；`QMultiHash` 的按键操作平均接近 O(1)，但没有全局键序。不要因为容器名相近而把两者的迭代顺序视为可以互换。

## 键类型与排序契约

`Key` 必须可排序，即支持能形成严格弱序的 `operator<()`。与 `QMultiHash` 不同，`QMultiMap` 不要求 `qHash()`。

排序契约应满足自反性、传递性和等价关系一致性：若两个键在比较器看来互不小于对方，它们被视作同一个键组。不要让比较逻辑依赖会在插入后改变的字段；修改用作键的对象会让查找和排序语义失真。

```cpp
struct Version {
    int major = 0;
    int minor = 0;

    bool operator<(const Version &other) const noexcept
    {
        if (major != other.major)
            return major < other.major;
        return minor < other.minor;
    }
};

QMultiMap<Version, QString> compatibilityRules;
```

`T` 也应为可赋值类型。若需要 `contains(key, value)`、`remove(key, value)`、`find(key, value)`、`count(key, value)` 或相等比较，`T` 还需要 `operator==()`。

## 重复键、插入与替换

同键条目连续，且顺序是**最近插入 -> 最早插入**。`insert()` 追加一条，`replace()` 只更新该键最近插入的一条。

```cpp
QMultiMap<QString, int> samples;
samples.insert("cpu", 41);
samples.insert("cpu", 44);
samples.insert("cpu", 47);

// samples.values("cpu") 为 {47, 44, 41}

samples.replace("cpu", 50);
// samples.values("cpu") 为 {50, 44, 41}
```

| 需求 | API | 结果 |
| --- | --- | --- |
| 保留一条新记录 | `insert(key, value)` | 总大小加一；新记录成为该键的第一个值。 |
| 在提示位置附近插入 | `insert(pos, key, value)` | `pos` 是性能提示，容器仍保持按键排序。 |
| 更新该键的当前值 | `replace(key, value)` | 键存在时更新最近插入项；不存在时插入。 |
| 读取当前值 | `value(key)` | 返回最近插入值；缺失时返回默认值。 |
| 读取全部值 | `values(key)` | 返回新 `QList<T>`，从最近到最早。 |
| 删除当前值并取得它 | `take(key)` | 只移除最近插入项。 |
| 删除此键的所有记录 | `remove(key)` | 返回删除的条目数。 |

`QMultiMap` **没有** `operator[]`。这是刻意的：一个键可能有多个值，`map[key]` 无法表达应返回哪一条可写记录。需要读当前值使用 `value()`，需要更新当前值使用 `replace()`，需要新增值使用 `insert()`。

## 范围查询是它的主场

`lowerBound(key)` 返回第一个键“不小于” `key` 的条目；`upperBound(key)` 返回第一个键“大于” `key` 的条目。两者组成的半开区间 `[lowerBound(key), upperBound(key))` 覆盖该键的所有记录，`equal_range(key)` 正是这组边界的直接封装。

```cpp
QMultiMap<int, QString> tasks;
tasks.insert(10, "parse");
tasks.insert(20, "render");
tasks.insert(20, "thumbnail");
tasks.insert(30, "upload");

const auto [first, last] = std::as_const(tasks).equal_range(20);
for (auto it = first; it != last; ++it)
    qDebug() << it.key() << it.value();

// 查询半开键区间 [10, 30)
for (auto it = tasks.cbegin(), end = tasks.lowerBound(30);
     it != end; ++it) {
    qDebug() << it.key() << it.value();
}
```

要注意 `lowerBound(30)` 只给出第一个 `key >= 30` 的条目；如果要取得单键 `30` 的所有记录，应使用 `equal_range(30)` 或 `lowerBound(30)` 配对 `upperBound(30)`。

`find(key)` 与 `lowerBound(key)` 对一个存在的键都会定位同键组的首项，也就是最近插入值。`find(key, value)` 在该键组内按值寻找一项，找不到时返回 `end()`。

## 首尾 API 的真实含义

由于全局按键升序：

- `firstKey()` 是最小键，`lastKey()` 是最大键；
- `first()` 是最小键组中的最新值；
- `last()` 是最大键组中的最早值，因为同键最新项在前、最早项在后；
- 这些 API 在空容器上无效，调试构建会触发断言；调用前先确认 `!isEmpty()`。

```cpp
QMultiMap<int, QString> map;
map.insert(1, "newer");
map.insert(1, "older");
map.insert(2, "only");

// firstKey() == 1, first() == "older"  <-- 注意插入顺序：
// insert(1, "newer") 后再 insert(1, "older")，"older" 才是最新项。
// lastKey() == 2, last() == "only"
```

上例说明要以实际插入时间判断“最新”，不要从变量文字猜测。`values(key)` 是验证同键顺序最直观的方法。

## 迭代器、隐式共享与失效

`QMultiMap` 是隐式共享值类型，拷贝通常很便宜，写入时才分离底层树。它标记为可重入（reentrant），但这不等于同一实例可在多个线程中同时修改。

- 所有线程只读同一个实例是安全的；写入共享实例时由调用方同步。
- 任一非 const 操作后，应认为此前取得的迭代器、引用和键值 range 引用都失效。
- 非 const `begin()`、`find()`、`lowerBound()`、`equal_range()` 为了提供可写迭代器会触发 detach；纯读取使用 `cbegin()`、`constFind()`、const `lowerBound()` 或 `std::as_const(map)`。
- 迭代器是双向迭代器，不是随机访问迭代器。Qt 6 已废弃迭代器的 `+ n`、`- n` 等用法，使用 `std::next()`、`std::prev()` 或 `std::advance()`。
- `erase(pos)` / `erase(first, last)` 返回删除范围后的位置；删除时使用其返回值继续遍历。

```cpp
for (auto it = rules.begin(); it != rules.end(); ) {
    if (it.value().isEmpty())
        it = rules.erase(it);
    else
        ++it;
}
```

`asKeyValueRange()`（Qt 6.4 起）可与结构化绑定配合。非 const range 中 `value` 是容器内值的可写引用；键是 `const Key &`，不能也不应修改。

```cpp
for (auto [key, value] : tasks.asKeyValueRange()) {
    Q_UNUSED(key);
    value = value.trimmed();
}
```

## 列表转换、合并与标准库互操作

`keys()`、`values()`、`uniqueKeys()` 都创建新的 `QList`。其中：

- `keys()` 与 `values()` 按键升序，位置一一对应；重复键也重复出现；
- `values(key)` 在同键组内是最近到最早；
- `keys(value)` 与 `key(value)` 都需要扫描值，属于线性查找；
- 大量遍历时优先用迭代器而不是先构造列表。

`unite()`、非成员 `operator+=` 和 `operator+` 合并两个多值 map，不会因键相同而丢弃记录。`QMultiMap` 还可从 `QMap`、`std::multimap` 构造，并用 `toStdMultiMap()` 转回标准库容器；转出副本时保留键排序和重复键项。

## 常见错误

### 把 `insert()` 当作覆盖操作

`insert()` 永远保留新项。要替换当前最新值用 `replace()`；只需要单值映射时改用 `QMap`。

### 误解同键的顺序

容器整体按键升序，但同键值按最近插入到最早插入。不能把 `last()` 简化理解成“最大键的最新值”。

### 用 `value()` 判断键是否存在

键不存在时返回 `T()` 或传入默认值；若默认值合法会混淆状态。先使用 `contains(key)` 或 `count(key)`。

### 把 `lowerBound()` 当成精确查找

找不到精确键时，`lowerBound()` 仍会返回下一个更大的键。精确查找使用 `find()` 或检查 `it != end() && it.key() == key`。

### 依赖 `keys()` / `values()` 作为零成本视图

这些函数都会构造列表。需要流式处理、避免复制时使用迭代器、`keyBegin()` / `keyEnd()` 或 `asKeyValueRange()`。

### 在空 map 上调用首尾 API

`first()`、`last()`、`firstKey()`、`lastKey()` 没有空值返回约定。空容器时先分支，不要依赖 release 构建中的未定义后果。

## API 速查表

### 类型与构造

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `key_type` / `mapped_type` / `size_type` / `difference_type` | STL 风格类型别名。 | `Key` 需支持严格弱序的 `<`；`size_type` 是 `qsizetype`。 |
| `iterator` / `const_iterator` | 双向遍历值，使用 `it.key()` 取键。 | 不是随机访问迭代器；非 const 操作后迭代器与引用失效。 |
| `Iterator` / `ConstIterator` | 旧式 Qt 别名。 | 分别等同于 `iterator` / `const_iterator`。 |
| `key_iterator` | 遍历每一项的键。 | 全局升序，重复键重复出现。 |
| `key_value_iterator` / `const_key_value_iterator` | 解引用得到键值对的迭代器。 | 适合结构化绑定；可变版本仅可修改 value。 |
| `QMultiMap()` | 构造空 map。 | `isEmpty()` 为真。 |
| `QMultiMap({{key, value}, ...})` | 用初始化列表构造。 | 保留重复键项，最终按键排序。 |
| `QMultiMap(const/rvalue QMap &)` | 从单值 `QMap` 构造，Qt 6.0 起。 | 每个 QMap 项变为一项。 |
| `QMultiMap(const/rvalue std::multimap &)` | 从标准多重 map 构造。 | 需要包含 `<map>`；复制或转移取决于值类别。 |
| 拷贝 / 移动 / 赋值 | 复制或转移容器。 | 拷贝隐式共享；第一次写可能线性分离。 |
| `toStdMultiMap() const & / &&` | 转为 `std::multimap<Key, T>`。 | 左值版本复制；右值且独占数据时可移动内部数据。 |
| `swap(other)` | 快速交换两个容器。 | `noexcept`，不逐项复制。 |

### 容器状态与键值读取

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `size()` / `count()` | 返回全部条目数量。 | 不同于 `count(key)`。 |
| `isEmpty()` / `empty()` | 判断是否没有条目。 | 空容器不能调用首尾 API。 |
| `contains(key)` | 判断该键是否存在。 | 适合与 `value()` 配合区分缺失。 |
| `contains(key, value)` | 判断是否存在完全匹配的条目。 | 需要 `T::operator==`。 |
| `count(key)` | 返回该键的条目数量。 | 同键的全部记录都会计入。 |
| `count(key, value)` | 返回完全匹配键值对的数量。 | 可用于统计重复插入。 |
| `value(key, defaultValue)` | 返回该键最新插入的值。 | 无键时返回默认值；返回的是拷贝。 |
| `values(key)` | 返回此键的全部值。 | 新建 `QList<T>`；顺序最新到最早。 |
| `values()` | 返回全部值。 | 新建列表；按 key 升序，同键最新到最早。 |
| `key(value, defaultKey)` | 找一个映射到 value 的键。 | 线性扫描；多个匹配时只返回第一个。 |
| `keys(value)` | 返回所有映射到 value 的键。 | 线性扫描并创建列表。 |
| `keys()` | 返回每条记录的键。 | 新建列表，按升序，重复键重复出现；位置与 `values()` 对齐。 |
| `uniqueKeys()` | 返回每个不同键一次。 | 新建升序列表。 |
| `firstKey()` / `lastKey()` | 返回最小/最大键。 | 空容器上不可调用。 |
| `first()` / `last()` | 返回全局首/尾条目的值引用。 | 空容器上不可调用；同键内部顺序也会影响结果。 |

### 插入、删除与合并

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `insert(key, value)` | 新增一条记录。 | 不覆盖同键旧值；新项是该键最新项。 |
| `insert(pos, key, value)` | 使用位置提示插入。 | `pos` 只用于优化；最终位置仍服从 key 排序和同键顺序。 |
| `replace(key, value)` | 插入或更新该键最新项。 | 键存在时仅替换一项，不删除其他同键条目。 |
| `remove(key)` | 删除该键所有记录。 | 返回删除数量。 |
| `remove(key, value)` | 删除全部匹配键值对。 | 重复的同一 pair 会一起删除。 |
| `take(key)` | 删除并返回该键最新值。 | 仅删一项；缺失时返回 `T()`；不需要返回值则 `remove()` 更合适。 |
| `erase(pos)` | 删除一个迭代器位置。 | 返回下一位置，适合遍历中删除。 |
| `erase(first, last)` | 删除半开迭代器区间，Qt 6.0 起。 | 返回删除区间后的迭代器；范围必须来自同一容器。 |
| `removeIf(pred)` | 删除谓词命中的项，Qt 6.1 起。 | 谓词参数可为 `iterator` 或 `std::pair<const Key &, T &>`。 |
| `erase_if(map, pred)` | 非成员批量删除，Qt 6.1 起。 | 与 `removeIf()` 同义，适合泛型算法形式。 |
| `unite(const QMultiMap &)` / `unite(QMultiMap &&)` | 合并另一个多值 map。 | 保留相同键的全部项，返回 `*this`。 |
| `operator+=` / `operator+` | 原地合并 / 返回合并结果。 | 都不做去重。 |

### 查找与遍历

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `begin()` / `end()` | 可写迭代器边界。 | 可能 detach；读遍历不要优先用它们。 |
| `cbegin()` / `cend()`、`constBegin()` / `constEnd()` | 只读迭代器边界。 | 适合并发只读和避免 copy-on-write。 |
| `find(key)` / `constFind(key)` | 查找键组的首项。 | 找到时是该键最新值；找不到返回 `end()`。 |
| `find(key, value)` / `constFind(key, value)` | 查找一个精确键值对。 | 不存在返回 `end()`；同 pair 重复时定位其中一个匹配项。 |
| `lowerBound(key)` | 查找第一个 `>= key` 的条目。 | 键缺失时可能指向下一个更大键。 |
| `upperBound(key)` | 查找第一个 `> key` 的条目。 | 与 `lowerBound(key)` 组成该键组边界。 |
| `equal_range(key)` | 返回该键的 `[first, last)`。 | 直接、无复制地遍历同键全部项。 |
| `keyBegin()` / `keyEnd()` | 只遍历键。 | 重复键重复出现，整体升序。 |
| `keyValueBegin()` / `keyValueEnd()` | 键值迭代器边界。 | 有 const 和非 const 重载。 |
| `constKeyValueBegin()` / `constKeyValueEnd()` | 只读键值迭代器。 | 适合避免 detach。 |
| `asKeyValueRange()` | 用 range-for 遍历键值，Qt 6.4 起。 | 解构变量引用内部元素；下一次非 const 操作后失效。 |

### 比较与流

| API | 作用 | 关键语义与边界 |
| --- | --- | ---|
| `operator==` / `operator!=` | 比较两个 `QMultiMap`。 | 要求键值对相同且顺序相同；重复键时值顺序影响结果。 |
| `QDataStream << map` | 写入二进制流。 | `Key` 与 `T` 均需支持 `operator<<`；持久化时设置流版本。 |
| `QDataStream >> map` | 从二进制流读取。 | `Key` 与 `T` 均需支持 `operator>>`；检查流状态。 |

## 一句话总结

`QMultiMap` 是“一键多值且按键排序”的容器：用 `insert()` 保留记录，用 `replace()` 更新最新项，用 `equal_range()` 或上下界做高效范围遍历，并始终把同键顺序理解为最近插入到最早插入。
