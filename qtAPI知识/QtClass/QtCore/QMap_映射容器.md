# Qt QMap 有序映射容器深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QMap>`  
> 所属模块：`Qt6::Core`  
> 类型性质：按键排序、隐式共享的键值容器  
> 相关类型：`QHash`、`QMultiMap`、`QList`、`QKeyValueIterator`、`QDataStream`

## 1. 它解决什么问题

`QMap<Key, T>` 保存一组唯一的 `(key, value)`，并始终按 key 的顺序遍历。它适合表达“通过标识找到对象，同时还需要有序输出或范围查找”的数据关系。

常见用途包括：

- 把配置项、字段名或编号映射到值；
- 把时间、分数、优先级等可排序 key 映射到记录；
- 需要输出稳定顺序的索引和缓存；
- 使用 `lowerBound()` / `upperBound()` 查找一个有序范围；
- 需要一个 key 对应一个 value 的注册表。

它和 `QHash` 的选择边界很明确：

| 容器 | 主要保证 | 按 key 查找 | 遍历顺序 |
| --- | --- | --- | --- |
| `QMap` | key 唯一且有序 | O(log n) | 按 key 排序 |
| `QHash` | key 唯一且哈希查找快 | 平均 O(1) | 不保证顺序 |
| `QMultiMap` | 一个 key 可以对应多个 value | O(log n) | 按 key 排序 |

`QMap` 不是“数组下标到元素”的容器，也不是多值索引：

- key 的顺序来自比较关系，不是插入顺序；
- 相同 key 只有一个元素，普通 `insert()` 会覆盖旧 value；
- 需要保留同 key 的多个记录时使用 `QMultiMap`；
- 需要高频精确查找且不关心顺序时通常评估 `QHash`；
- 它不负责 value 指针指向对象的所有权。

## 2. Key 和 value 必须满足什么条件

### 2.1 Key 需要严格弱序

`QMap` 需要能够比较 key，以确定元素的排序位置。自定义 key 应提供稳定的严格弱序关系，通常是 `operator<`：

```cpp
class UserId
{
public:
    explicit UserId(quint64 value = 0) : m_value(value) {}

    friend bool operator<(const UserId &left, const UserId &right)
    {
        return left.m_value < right.m_value;
    }

    friend bool operator==(const UserId &, const UserId &) = default;

private:
    quint64 m_value = 0;
};
```

比较关系必须满足传递性和一致性。若两个 key 互不小于对方，`QMap` 会把它们视为等价 key；此时后插入的 value 会覆盖先前 value。

不要让 key 在放入 map 后改变参与排序的字段。通过指针、引用或外部共享状态间接改变比较结果，会破坏树结构的查找前提。

### 2.2 Value 不需要可比较，除非调用反向查询

普通按 key 的插入和查找不要求 `T` 可比较。但下列 API 会比较 value：

- `key(value, defaultKey)`；
- `keys(value)`；
- `removeIf()` 的自定义谓词可能自行比较 value；
- `operator==` 比较两个 map 时需要比较 value；
- `QDataStream` 序列化需要对应流操作符。

`operator[]` 缺少 key 时会构造一个默认 `T`，所以使用非 const `operator[]` 时，`T` 需要可默认构造。

## 3. 实际使用场景

### 3.1 配置项和有序输出

```cpp
#include <QMap>
#include <QString>

QMap<QString, QString> settings;
settings.insert(QStringLiteral("language"), QStringLiteral("zh_CN"));
settings.insert(QStringLiteral("theme"), QStringLiteral("dark"));

for (auto it = settings.cbegin(); it != settings.cend(); ++it)
    qDebug() << it.key() << '=' << it.value();
```

遍历顺序由字符串 key 的比较关系决定。它不是插入顺序；如果业务需要用户配置的原始顺序，应额外保存顺序列表。

### 3.2 时间范围索引

```cpp
QMap<qint64, QString> events;
events.insert(1000, QStringLiteral("connected"));
events.insert(1500, QStringLiteral("authenticated"));
events.insert(2400, QStringLiteral("closed"));

const auto first = events.lowerBound(1200);
const auto last = events.upperBound(2400);

for (auto it = first; it != last; ++it)
    qDebug() << it.key() << it.value();
```

`lowerBound(1200)` 指向第一个 key 不小于 1200 的元素；`upperBound(2400)` 指向第一个 key 大于 2400 的元素。两者组成半开区间 `[first, last)`。

### 3.3 对象注册表

```cpp
QMap<quint64, QObject *> objects;
objects.insert(objectId, object);

if (auto it = objects.find(objectId); it != objects.end())
    it.value()->setProperty("active", true);
```

`QMap` 只保存指针，不会因为 map 删除元素而删除指针指向的 `QObject`。若对象由父子关系、智能指针或其他管理器拥有，必须让对象销毁时同步清理 map 中的指针。

### 3.4 按 key 更新计数

```cpp
QMap<QString, int> counts;
++counts[QStringLiteral("warning")];
```

这利用了 `operator[]` 的“缺失时插入默认值”语义。若只是读取，不要用非 const `operator[]`，否则查询本身会改变 map：

```cpp
const auto it = counts.constFind(QStringLiteral("error"));
if (it != counts.constEnd())
    qDebug() << it.value();
```

### 3.5 什么时候改用 `QMultiMap`

如果一个 key 需要多个 value，例如“标签对应多篇文章”：

```cpp
QMultiMap<QString, Article> articlesByTag;
```

不要用 `QMap<Key, QList<T>>` 机械模拟多值关系，除非你确实需要把同 key 的所有 value 作为一个列表整体管理。`QMultiMap` 的范围、重复 key 和 `values(key)` API 更直接。

## 4. 值语义、隐式共享和 detach

### 4.1 复制 map 通常只复制共享数据引用

```cpp
QMap<QString, int> original;
original.insert(QStringLiteral("one"), 1);

QMap<QString, int> copy = original;
copy.insert(QStringLiteral("two"), 2);
```

`QMap` 是隐式共享容器。复制初始时，两个对象可以共享同一份内部数据；当 `copy` 被修改时，Qt 会先 detach，让修改只影响 `copy`，`original` 保持不变。

这让按值返回、作为参数传递和保存快照很方便，但不代表写操作是 O(1)：

- 复制 map 本身通常很便宜；
- 第一次修改一个共享 map 可能需要复制全部元素；
- 大 map 的反复复制后分别修改可能产生多次 detach；
- 需要高频并发写入时，隐式共享不替代互斥或消息传递。

### 4.2 const 访问和非 const 访问的差异

```cpp
const QMap<QString, int> map = makeMap();

for (auto it = map.cbegin(); it != map.cend(); ++it)
    use(it.key(), it.value());
```

const 的 `begin()`、`end()`、`find()`、`lowerBound()` 和 `upperBound()` 可以只读访问共享数据。非 const 的 `begin()`、`end()`、`find()`、`lowerBound()`、`upperBound()` 需要返回可修改迭代器，可能触发 detach。

因此，即使没有显式改元素，下面的调用也可能产生分离成本：

```cpp
QMap<QString, int> map = makeMap();
auto it = map.begin(); // 可能 detach
```

只读遍历优先使用 const map、`cbegin()`/`cend()` 或 `constBegin()`/`constEnd()`。

### 4.3 迭代器和引用会受到 detach 影响

不要在一个共享副本上保存迭代器或 value 引用，再让另一个副本修改容器，然后继续把旧迭代器当成当前 map 的迭代器使用。迭代器属于具体的内部数据实例，不是 key 的永久句柄。

```cpp
auto it = map.find(key);
QMap<QString, int> copy = map;
copy.insert(otherKey, 1);

// 不要把 it 和 copy 混用，也不要假设它代表 copy 中的元素。
```

## 5. 构建与最小使用

### 5.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

### 5.2 头文件

```cpp
#include <QMap>
#include <QString>
#include <QList>
#include <QDataStream>
#include <map>
#include <utility>
```

按值类型实际需要包含对应的头文件；不要依赖 `<QMap>` 间接带入所有 value 类型的声明。

### 5.3 最小代码

```cpp
#include <QMap>
#include <QString>

int main()
{
    QMap<QString, int> scores;
    scores.insert(QStringLiteral("Alice"), 95);
    scores[QStringLiteral("Bob")] = 88;

    for (auto it = scores.cbegin(); it != scores.cend(); ++it)
        qDebug() << it.key() << it.value();

    return 0;
}
```

## 6. 插入、覆盖和查询的核心区别

### 6.1 `insert()` 对同 key 覆盖

```cpp
QMap<int, QString> map;
map.insert(1, QStringLiteral("old"));
map.insert(1, QStringLiteral("new"));
```

最终 key `1` 只有 value `"new"`。如果不希望覆盖，先调用 `contains()` 或 `find()`，再决定是否插入；需要多值关系时使用 `QMultiMap`。

### 6.2 `value()` 是无副作用查询

```cpp
const QString value = map.value(42, QStringLiteral("missing"));
```

key 不存在时返回指定默认值，不修改 map。这是只读查询的常用入口。

### 6.3 `operator[]` 的 const 和非 const 版本不同

```cpp
QMap<int, QString> map;
map[1] = QStringLiteral("one"); // 缺失时插入默认 QString

const QMap<int, QString> &view = map;
const QString value = view[2];   // 缺失时只返回默认值，不插入
```

非 const 版本返回 `T &`，缺失 key 会插入 `T()`；const 版本返回 `T` 值，缺失时等同于 `value(key)`。不要把两种调用混为一谈。

### 6.4 `find()` 适合“查找并可能修改 value”

```cpp
if (auto it = map.find(1); it != map.end())
    it.value() += QStringLiteral("!");
```

判断缺失时必须和同一个 map 的 `end()` 比较。找到后，`it.key()` 只读，`it.value()` 在非常量迭代器中可修改。

## 7. 逐项 API 说明

### 7.1 类型别名

#### `QMap::key_type`

```cpp
using key_type = Key;
```

表示 map 的 key 类型。算法、泛型代码和 `QMap::key_iterator` 可以使用这个别名。

#### `QMap::mapped_type`

```cpp
using mapped_type = T;
```

表示 map 的 value 类型，也就是模板参数 `T`。

#### `QMap::difference_type`

```cpp
using difference_type = qptrdiff;
```

表示迭代器距离类型。`QMap` 迭代器是双向迭代器，距离操作通常需要线性步进，不应把它当数组下标距离使用。

#### `QMap::size_type`

```cpp
using size_type = qsizetype;
```

表示元素数量和删除数量等大小。它不是 key 或 value 类型，跨平台保存数量时应注意与 `int` 的转换边界。

#### `QMap::iterator`

可修改 value 的双向迭代器：

```cpp
for (QMap<int, QString>::iterator it = map.begin();
     it != map.end(); ++it) {
    it.value().append('!');
}
```

key 不能通过迭代器修改，因为修改 key 会破坏有序结构。迭代器支持 `key()`、`value()`、解引用和 `->`。

#### `QMap::const_iterator`

只读 value 的双向迭代器：

```cpp
for (QMap<int, QString>::const_iterator it = map.cbegin();
     it != map.cend(); ++it) {
    use(it.key(), it.value());
}
```

非常量迭代器可以隐式转换为 const 迭代器。const 迭代器不能修改 value。

#### `QMap::key_iterator`

只遍历 key 的迭代器：

```cpp
for (auto it = map.keyBegin(); it != map.keyEnd(); ++it)
    qDebug() << *it;
```

key 只读。`base()` 可以取得底层的 `const_iterator`。它仍然按照 map 的 key 顺序遍历。

#### `QMap::key_value_iterator`

用于同时遍历 key 和 value 的可修改键值迭代器，通常通过 `keyValueBegin()` 和 `keyValueEnd()` 取得。key 仍然只读，value 可修改。

#### `QMap::const_key_value_iterator`

用于同时遍历 key 和 value 的只读键值迭代器。它由 const `keyValueBegin()`、`constKeyValueBegin()` 等 API 返回。

#### `QMap::Iterator`

`iterator` 的 Qt 风格别名，主要用于兼容旧式 Qt 代码。新代码可以直接使用 `iterator`。

#### `QMap::ConstIterator`

`const_iterator` 的 Qt 风格别名，主要用于兼容旧式 Qt 代码。新代码可以直接使用 `const_iterator`。

### 7.2 构造、赋值和交换

#### `QMap::QMap()`

```cpp
QMap();
```

构造空 map。空 map 可以安全调用 `size()`、`isEmpty()`、`find()`、`begin()` 和 `end()`；但不能调用 `first()`、`last()`、`firstKey()` 或 `lastKey()`。

#### `QMap::QMap(std::initializer_list<std::pair<Key, T>> list)`

```cpp
QMap(std::initializer_list<std::pair<Key, T>> list);
```

从初始化列表构造：

```cpp
QMap<QString, int> priorities{
    {QStringLiteral("low"), 1},
    {QStringLiteral("high"), 3},
};
```

重复 key 遵守 map 的唯一 key 语义，后续插入的 value 会覆盖先前 value。最终遍历仍按 key 排序。

#### `explicit QMap(const std::map<Key, T> &other)`

```cpp
explicit QMap(const std::map<Key, T> &other);
```

从标准库 `std::map` 复制构造 Qt map。key 和 value 会复制到 Qt 的内部容器中，之后两者互不共享。

#### `explicit QMap(std::map<Key, T> &&other)`

```cpp
explicit QMap(std::map<Key, T> &&other);
```

从右值 `std::map` 构造，允许 Qt 尽可能移动内部数据。移动后不要依赖 `other` 的具体内容，但它仍应满足标准库移动后对象的基本有效性要求。

#### `QMap::QMap(const QMap<Key, T> &other)`

```cpp
QMap(const QMap<Key, T> &other);
```

复制构造 map。复制采用隐式共享，通常只增加共享引用；之后任一副本修改时会 detach。

#### `QMap::QMap(QMap<Key, T> &&other)`

```cpp
QMap(QMap<Key, T> &&other);
```

移动构造 map，接收其他 map 的内部数据。移动后的 `other` 仍可销毁、赋值或重新使用，但不能假定它保留原有元素。

#### `QMap::~QMap()`

```cpp
~QMap();
```

销毁 map。若内部数据仍被其他隐式共享副本使用，数据会继续保留到最后一个引用释放。容器销毁只销毁 value 对象本身，不负责删除 value 中的裸指针目标。

#### `QMap<Key, T> &QMap::operator=(const QMap<Key, T> &other)`

```cpp
QMap &operator=(const QMap &other);
```

复制赋值，使当前 map 表示和 `other` 相同的键值集合。赋值后两者可能共享内部数据；后续修改当前对象会 detach。

#### `QMap<Key, T> &QMap::operator=(QMap<Key, T> &&other)`

```cpp
QMap &operator=(QMap &&other);
```

移动赋值，接管 `other` 的内部数据。当前对象原来的元素会被替换，移动后的 `other` 保持有效但内容不应假定。

#### `void QMap::swap(QMap<Key, T> &other)`

```cpp
void swap(QMap &other) noexcept;
```

交换两个 map 的内容。通常只交换内部共享指针，适合高效返回临时结果或实现提交式更新。

```cpp
QMap<QString, int> result = buildMap();
map.swap(result);
```

交换不会复制每个 key/value，但交换后原有迭代器应按所属容器的新内容重新理解，不要继续把它们当作交换前的 map 迭代器。

### 7.3 共享状态和高级 detach API

#### `void QMap::detach()`

```cpp
void detach();
```

确保当前 map 拥有一份独立的内部数据。若当前为空，会建立可写的内部数据；若当前与其他 map 共享，会复制数据。

一般业务代码不需要主动调用它，因为 Qt 的写操作会自动 detach。它适合需要提前明确分离成本、或需要对内部引用做严格生命周期安排的底层代码。

#### `bool QMap::isDetached() const`

```cpp
bool isDetached() const noexcept;
```

查询当前 map 是否没有与其他 map 共享内部数据。它是实现和性能诊断工具，不应成为业务逻辑判断条件。空 map 的共享状态不应被解读为“已经有一份独立数据”。

#### `bool QMap::isSharedWith(const QMap<Key, T> &other) const`

```cpp
bool isSharedWith(const QMap &other) const noexcept;
```

判断两个 map 是否引用同一份内部共享数据。它只反映当前实现级共享关系，不表示两个 map 的内容永远相同，也不应作为业务等价判断；内容比较应使用 `operator==`。

#### `QMap QMap::referenceHoldingDetach()`

```cpp
QMap referenceHoldingDetach();
```

这是 Qt 头文件中可见的引用保护辅助接口，用于在可能返回内部 key/value 引用的操作前暂时保留旧共享副本。它主要服务于容器内部实现和非常底层的代码，普通应用不应依赖其细节。

#### `QMap QMap::referenceHoldingDetachExcept(const Key &key)`

```cpp
QMap referenceHoldingDetachExcept(const Key &key);
```

这是 `referenceHoldingDetach()` 的 key 特化辅助版本，用于在修改一个 key 对应的元素时保留引用相关的共享状态。它不是普通业务容器操作的首选 API，若代码需要调用它，应同时阅读目标 Qt 版本的头文件实现。

### 7.4 容量和基础状态

#### `QMap::size_type QMap::size() const`

```cpp
size_type size() const;
```

返回元素数量。`QMap` 的每个 key 最多对应一个 value，所以 size 也等于不同 key 的数量。

#### `bool QMap::isEmpty() const`

```cpp
bool isEmpty() const;
```

判断 map 是否没有元素。空 map 上调用 `clear()`、`remove()`、`take()` 和各种查找是安全的。

#### `bool QMap::empty() const`

```cpp
bool empty() const;
```

STL 风格的空状态查询，语义等同于 `isEmpty()`。它适合泛型代码和标准容器风格代码。

#### `void QMap::clear()`

```cpp
void clear();
```

删除所有元素，使 map 为空。

**共享边界：**

- 如果当前数据没有共享，直接清空当前内部 map；
- 如果当前数据被共享，当前对象会放弃共享数据，让其他副本保持不变；
- 清空后原有 iterator、reference 和 value 指针都不能继续使用；
- `clear()` 不会发出信号，因为 `QMap` 不是 QObject。

### 7.5 按 key 查询和取值

#### `bool QMap::contains(const Key &key) const`

```cpp
bool contains(const Key &key) const;
```

判断 key 是否存在，不会插入默认 value。只做 membership test 时优先使用它。

#### `QMap::size_type QMap::count(const Key &key) const`

```cpp
size_type count(const Key &key) const;
```

返回指定 key 的元素数量。对于 `QMap`，结果只有 `0` 或 `1`；需要表达“数量”时可用于统一泛型代码，但普通存在性判断用 `contains()` 更直观。

#### `QMap::size_type QMap::count() const`

```cpp
size_type count() const;
```

无参数版本返回 map 的元素总数，语义等同于 `size()`。

#### `T QMap::value(const Key &key, const T &defaultValue = T()) const`

```cpp
T value(const Key &key, const T &defaultValue = T()) const;
```

按 key 读取 value。key 不存在时返回 `defaultValue`，不修改 map。

```cpp
const int timeout = settings.value(QStringLiteral("timeout"), 30);
```

如果 map 里确实保存了一个等于默认值的 value，调用者无法仅通过返回值区分“存在”和“缺失”；需要区分时先用 `contains()` 或 `find()`。

#### `T QMap::operator[](const Key &key) const`

```cpp
T operator[](const Key &key) const;
```

const map 的下标访问是只读查询，返回 value 副本。key 不存在时返回默认构造的 `T`，不会插入元素。

#### `T &QMap::operator[](const Key &key)`

```cpp
T &operator[](const Key &key);
```

非常量 map 的下标访问返回可写 value 引用。key 不存在时先插入 `T()`：

```cpp
QMap<QString, int> counters;
counters[QStringLiteral("requests")] += 1;
```

**关键边界：**

- 查询缺失 key 也会改变 map 的 size；
- 需要 `T` 可默认构造；
- 返回的引用在 map 的结构修改、detach 或对象销毁后可能失效；
- 不要在只读代码中使用它来代替 `value()`。

#### `QMap::iterator QMap::find(const Key &key)`

```cpp
iterator find(const Key &key);
```

返回指向 key 的可修改迭代器；找不到时返回 `end()`。

非 const `find()` 可能为了提供可修改 iterator 而 detach。若只读查找，应使用 const map 或 const overload。

#### `QMap::const_iterator QMap::find(const Key &key) const`

```cpp
const_iterator find(const Key &key) const;
```

返回只读迭代器；找不到时返回 const `end()`。它不会因提供可写访问而主动 detach。

#### `QMap::const_iterator QMap::constFind(const Key &key) const`

```cpp
const_iterator constFind(const Key &key) const;
```

显式使用 const 语义查找。它和 const `find()` 结果相同，适合旧式 Qt 代码或需要在重载选择中明确只读意图的代码。

#### `Key QMap::key(const T &value, const Key &defaultKey = Key()) const`

```cpp
Key key(const T &value, const Key &defaultKey = Key()) const;
```

按 value 反向查找一个 key。它会按 key 顺序线性扫描，找不到时返回 `defaultKey`。

```cpp
const QString name =
    users.key(userId, QStringLiteral("<unknown>"));
```

它不是反向索引，复杂度为 O(n)。如果业务经常按 value 查找，应额外维护 `QMap<T, Key>` 或其他反向索引。

#### `QList<Key> QMap::keys() const`

```cpp
QList<Key> keys() const;
```

复制返回全部 key，结果按 QMap 的 key 顺序排列。它会创建新的 `QList`，大 map 上频繁调用会产生额外内存和复制。

#### `QList<Key> QMap::keys(const T &value) const`

```cpp
QList<Key> keys(const T &value) const;
```

返回所有 value 等于给定 value 的 key，按 key 顺序排列。它需要线性扫描，不适合高频反向查询。

#### `QList<T> QMap::values() const`

```cpp
QList<T> values() const;
```

复制返回所有 value，顺序与 key 的排序顺序一致。它不返回 key/value 对，也不保留 map 的关联结构。

#### `T QMap::take(const Key &key)`

```cpp
T take(const Key &key);
```

取出并删除指定 key 的 value。key 不存在时返回默认构造的 `T`：

```cpp
const bool existed = map.contains(key);
const auto value = map.take(key);
```

如果必须区分“缺失”和“实际 value 等于 `T()`”，应先调用 `contains()` 或用 `find()`。

**隐式共享边界：** 为了安全地返回 value 并删除节点，`take()` 可能在共享 map 上先分离内部数据；即使 key 不存在，也不要把它当成纯 const 查询。

### 7.6 首尾元素

#### `const Key &QMap::firstKey() const`

```cpp
const Key &firstKey() const;
```

返回排序后最小 key 的引用。map 为空时调用违反前置条件，调试构建通常会触发断言。

返回的引用只在 map 不发生相关结构变化且对象存活期间有效；需要长期保存时复制 key。

#### `const Key &QMap::lastKey() const`

```cpp
const Key &lastKey() const;
```

返回排序后最大 key 的引用。空 map 上调用同样是错误用法。

#### `T &QMap::first()`

```cpp
T &first();
```

返回最小 key 对应的可修改 value 引用。空 map 上调用违反前置条件。

#### `const T &QMap::first() const`

```cpp
const T &first() const;
```

返回最小 key 对应的只读 value 引用。引用不拥有 value，map 的结构修改或销毁会使其失效。

#### `T &QMap::last()`

```cpp
T &last();
```

返回最大 key 对应的可修改 value 引用。空 map 上调用违反前置条件。

#### `const T &QMap::last() const`

```cpp
const T &last() const;
```

返回最大 key 对应的只读 value 引用。需要长期保存时复制 value，不要保存引用跨越 map 修改。

### 7.7 有序边界查找

#### `QMap::iterator QMap::lowerBound(const Key &key)`

```cpp
iterator lowerBound(const Key &key);
```

返回第一个不小于给定 key 的可修改迭代器；若没有这样的元素，返回 `end()`。

```cpp
auto it = map.lowerBound(start);
if (it != map.end())
    it.value() = replacement;
```

非 const overload 可能触发 detach。

#### `QMap::const_iterator QMap::lowerBound(const Key &key) const`

```cpp
const_iterator lowerBound(const Key &key) const;
```

返回第一个不小于 key 的只读迭代器。适合只读范围查询。

#### `QMap::iterator QMap::upperBound(const Key &key)`

```cpp
iterator upperBound(const Key &key);
```

返回第一个大于给定 key 的可修改迭代器；没有时返回 `end()`。

#### `QMap::const_iterator QMap::upperBound(const Key &key) const`

```cpp
const_iterator upperBound(const Key &key) const;
```

返回第一个大于 key 的只读迭代器。

#### `std::pair<QMap::iterator, QMap::iterator> QMap::equal_range(const Key &key)`

```cpp
std::pair<iterator, iterator> equal_range(const Key &key);
```

返回包含所有等价 key 的半开区间。因为 `QMap` 不允许重复 key，区间最多包含一个元素；它主要用于 STL 风格泛型代码和与 `QMultiMap` 共享算法。

#### `std::pair<QMap::const_iterator, QMap::const_iterator> QMap::equal_range(const Key &key) const`

```cpp
std::pair<const_iterator, const_iterator>
equal_range(const Key &key) const;
```

返回只读的等价 key 区间。key 存在时 `first` 指向该元素、`second` 指向它之后；key 不存在时两者相等。

### 7.8 插入、合并和删除

#### `QMap::iterator QMap::insert(const Key &key, const T &value)`

```cpp
iterator insert(const Key &key, const T &value);
```

插入 `(key, value)`；如果 key 已存在，则覆盖旧 value，并返回最终元素的 iterator。

```cpp
auto it = map.insert(id, state);
it.value() = normalize(it.value());
```

它可能触发 detach。若 key 或 value 引用指向当前 map 内部，调用前应先复制必要数据，避免修改期间引用失效。

#### `QMap::iterator QMap::insert(QMap::const_iterator pos, const Key &key, const T &value)`

```cpp
iterator insert(const_iterator pos,
                const Key &key,
                const T &value);
```

带位置提示的插入或覆盖。`pos` 只用于帮助有序树定位；它不是强制插入位置，也不能让 key 违反排序。

提示应来自同一个 map，且应接近最终位置。错误提示通常仍能得到正确结果，但可能失去性能收益；不要把其他 map 的 iterator 传入。

#### `void QMap::insert(const QMap<Key, T> &map)`

```cpp
void insert(const QMap &map);
```

把另一个 map 的元素插入当前 map。若两者存在相同 key，参数 `map` 中的 value 覆盖当前 value。

```cpp
QMap<int, QString> defaults;
QMap<int, QString> overrides;
settings = defaults;
settings.insert(overrides);
```

如果 `map` 就是当前对象本身，应避免依赖自插入的细节，直接跳过或使用明确的临时副本。

#### `void QMap::insert(QMap<Key, T> &&map)`

```cpp
void insert(QMap &&map);
```

从右值 map 插入元素，允许移动内部 key/value，通常用于减少临时对象复制。移动后的参数对象仍有效，但不要依赖它还保留哪些元素。

#### `QMap::iterator QMap::erase(QMap::const_iterator pos)`

```cpp
iterator erase(const_iterator pos);
```

删除 `pos` 指向的元素并返回下一个元素的 iterator：

```cpp
for (auto it = map.begin(); it != map.end();) {
    if (shouldRemove(it.key()))
        it = map.erase(it);
    else
        ++it;
}
```

`pos` 必须来自当前 map，且不能是 `end()`。删除当前节点后，不要继续解引用旧 iterator。

#### `[since 6.0] QMap::iterator QMap::erase(QMap::const_iterator first, QMap::const_iterator last)`

```cpp
iterator erase(const_iterator first, const_iterator last);
```

删除半开区间 `[first, last)`，返回删除范围之后的 iterator。Qt 6.0 起提供。

空范围是安全的；两个 iterator 必须属于同一个 map，并且范围顺序有效。删除后范围内的 iterator 和 reference 都失效。

#### `QMap::size_type QMap::remove(const Key &key)`

```cpp
size_type remove(const Key &key);
```

删除指定 key，返回实际删除的元素数量。对于 `QMap`，结果为 `0` 或 `1`。

删除不会自动把 key 对应的裸指针目标 delete；它只移除 map 中的键值节点。

#### `[since 6.1] QMap::size_type QMap::removeIf(Predicate pred)`

```cpp
template <typename Predicate>
size_type removeIf(Predicate pred);
```

Qt 6.1 起按谓词删除元素，返回删除数量。谓词可以接收当前 map 的 `iterator`，也可以接收 `std::pair<const Key &, T &>` 形式的键值视图：

```cpp
const qsizetype removed = map.removeIf(
    [](auto it) {
        return it.value() < 0;
    });
```

或：

```cpp
map.removeIf([](const auto &entry) {
    return entry.second.isEmpty();
});
```

谓词执行期间不要再对同一个 map 做结构修改；删除操作由 `removeIf()` 自己完成。

#### `[since 6.1] qsizetype erase_if(QMap<Key, T> &map, Predicate pred)`

```cpp
template <typename Key, typename T, typename Predicate>
qsizetype erase_if(QMap<Key, T> &map, Predicate pred);
```

Qt 6.1 起的非成员版本，语义等同于 `map.removeIf(pred)`，适合标准库风格泛型代码：

```cpp
const qsizetype removed = erase_if(map, [](auto it) {
    return it.value() == 0;
});
```

### 7.9 遍历入口

#### `QMap::iterator QMap::begin()`

```cpp
iterator begin();
```

返回可修改遍历的起点。非 const `begin()` 可能触发 detach。空 map 时 `begin() == end()`。

#### `QMap::const_iterator QMap::begin() const`

```cpp
const_iterator begin() const;
```

返回只读遍历起点，不提供 value 修改权限。

#### `QMap::iterator QMap::end()`

```cpp
iterator end();
```

返回可修改遍历的尾后 iterator。不能解引用 `end()`；空 map 的 `begin()` 和 `end()` 相等。

#### `QMap::const_iterator QMap::end() const`

```cpp
const_iterator end() const;
```

返回只读遍历的尾后 iterator。

#### `QMap::const_iterator QMap::cbegin() const`

```cpp
const_iterator cbegin() const;
```

显式返回只读遍历起点，适合表达“无论对象是否为 const，这段代码都不修改容器”的意图。

#### `QMap::const_iterator QMap::cend() const`

```cpp
const_iterator cend() const;
```

显式返回只读遍历尾后 iterator。

#### `QMap::const_iterator QMap::constBegin() const`

```cpp
const_iterator constBegin() const;
```

Qt 风格的只读遍历起点，语义等同于 `cbegin()`。

#### `QMap::const_iterator QMap::constEnd() const`

```cpp
const_iterator constEnd() const;
```

Qt 风格的只读遍历尾后 iterator，语义等同于 `cend()`。

#### `QMap::key_iterator QMap::keyBegin() const`

```cpp
key_iterator keyBegin() const;
```

返回只遍历 key 的起点。key 不可修改，顺序与 map 的普通遍历相同。

#### `QMap::key_iterator QMap::keyEnd() const`

```cpp
key_iterator keyEnd() const;
```

返回只遍历 key 的尾后位置。不能解引用尾后迭代器。

#### `QMap::key_value_iterator QMap::keyValueBegin()`

```cpp
key_value_iterator keyValueBegin();
```

返回可修改 value 的键值范围起点。key 仍然只读，value 可通过键值迭代器修改。

#### `QMap::const_key_value_iterator QMap::keyValueBegin() const`

```cpp
const_key_value_iterator keyValueBegin() const;
```

返回只读键值范围起点。

#### `QMap::const_key_value_iterator QMap::constKeyValueBegin() const`

```cpp
const_key_value_iterator constKeyValueBegin() const;
```

显式返回 const 键值范围起点，与 const `keyValueBegin()` 语义相同。

#### `QMap::key_value_iterator QMap::keyValueEnd()`

```cpp
key_value_iterator keyValueEnd();
```

返回可修改键值范围的尾后位置。

#### `QMap::const_key_value_iterator QMap::keyValueEnd() const`

```cpp
const_key_value_iterator keyValueEnd() const;
```

返回只读键值范围的尾后位置。

#### `QMap::const_key_value_iterator QMap::constKeyValueEnd() const`

```cpp
const_key_value_iterator constKeyValueEnd() const;
```

显式返回 const 键值范围尾后位置，与 const `keyValueEnd()` 语义相同。

#### `[since 6.4] auto QMap::asKeyValueRange() &`

```cpp
auto asKeyValueRange() &;
```

Qt 6.4 起把左值 map 包装成键值 range，适合结构化绑定：

```cpp
for (auto [key, value] : map.asKeyValueRange()) {
    qDebug() << key << value;
    value += 1;
}
```

对非常量左值，key 是只读引用，value 是可修改引用。range 不拥有独立的 map，底层 map 必须在遍历期间保持存活。

#### `[since 6.4] auto QMap::asKeyValueRange() const &`

```cpp
auto asKeyValueRange() const &;
```

对 const 左值返回只读键值 range：

```cpp
for (auto [key, value] : std::as_const(map).asKeyValueRange())
    use(key, value);
```

不能通过该 range 修改 value。

#### `[since 6.4] auto QMap::asKeyValueRange() &&`

```cpp
auto asKeyValueRange() &&;
```

对右值 map 返回拥有移动后 map 生命周期的 range，可以安全地遍历临时 map：

```cpp
for (auto [key, value] :
     QMap<int, QString>{{1, QStringLiteral("one")}}
         .asKeyValueRange()) {
    use(key, value);
}
```

它适合一次性消费临时容器；不要把 range 或其中的引用保存到完整表达式结束之后。

#### `[since 6.4] auto QMap::asKeyValueRange() const &&`

```cpp
auto asKeyValueRange() const &&;
```

对 const 右值返回只读键值 range。临时对象的生命周期由 range 表达式管理，但 range 本身也不应被保存到超出其设计生命周期的位置。

### 7.10 非 const 修改范围与迭代器失效

#### `QMap::iterator::key() const`

```cpp
const Key &key() const;
```

返回当前节点的 key，只读。不能通过 iterator 修改 key；如果需要改变 key，应复制 value、删除旧 key 后以新 key 重新插入。

#### `QMap::iterator::value() const`

```cpp
T &value() const;
```

返回当前节点的可修改 value 引用。函数本身是 const 是迭代器代理语义，不表示返回的 value 不能修改。

#### `QMap::const_iterator::key() const`

```cpp
const Key &key() const;
```

返回当前节点的只读 key 引用。

#### `QMap::const_iterator::value() const`

```cpp
const T &value() const;
```

返回当前节点的只读 value 引用。

#### 迭代器的 `operator*()` 和 `operator->()`

非常量 iterator 解引用得到 `T &` 或 `T *`；const iterator 解引用得到 `const T &` 或 `const T *`。这些接口不能用于访问 key，访问 key 应调用 `key()`。

#### 迭代器递增和递减

`++it`、`it++`、`--it` 和 `it--` 都可用。`QMap` 迭代器是双向迭代器，不是随机访问迭代器。

Qt 6 中旧的 `operator+`、`operator-`、`operator+=`、`operator-=` 步进接口已标记为弃用，应改用 `std::next()`、`std::prev()` 或 `std::advance()`：

```cpp
auto middle = std::next(map.cbegin(), 3);
```

这类步进对树容器需要逐项移动，复杂度为 O(n)，不是数组式 O(1)。

## 8. 典型遍历方式

### 8.1 只读遍历

```cpp
for (auto it = map.cbegin(); it != map.cend(); ++it) {
    process(it.key(), it.value());
}
```

### 8. 修改 value

```cpp
for (auto it = map.begin(); it != map.end(); ++it)
    it.value() = normalize(it.value());
```

不要修改 key。需要重命名 key 时：

```cpp
const auto it = map.find(oldKey);
if (it != map.end()) {
    const auto value = it.value();
    map.erase(it);
    map.insert(newKey, value);
}
```

### 8.3 边遍历边删除

```cpp
for (auto it = map.begin(); it != map.end();) {
    if (expired(it.key()))
        it = map.erase(it);
    else
        ++it;
}
```

`erase(it)` 返回下一个有效迭代器，是边遍历边删除的标准写法。

### 8.4 结构化绑定遍历

```cpp
for (auto [key, value] : map.asKeyValueRange())
    value = transform(key, value);
```

若只读取并且项目需要兼容 Qt 6.3 或更低版本，使用 `const_iterator` 更稳妥。`asKeyValueRange()` 自 Qt 6.4 起提供。

## 9. 复杂度和性能边界

`QMap` 的典型有序树操作复杂度如下：

| 操作 | 典型复杂度 | 说明 |
| --- | --- | --- |
| `find` / `contains` | O(log n) | 按 key 查找 |
| `lowerBound` / `upperBound` | O(log n) | 找有序边界 |
| 单个 `insert` | O(log n) | 同 key 时更新已有节点 |
| `remove(key)` | O(log n) | 找到后删除 |
| `erase(iterator)` | 摊销接近 O(1) | 已经拿到节点 iterator |
| `keys()` / `values()` | O(n) | 复制整个结果列表 |
| `key(value)` / `keys(value)` | O(n) | 按 value 线性扫描 |
| `std::distance(iterator, end)` | O(n) | 双向迭代器不能随机跳转 |
| 首次修改共享 map | 可能 O(n) | detach 复制共享数据 |

### 9.1 预先排序不能像向量那样提供 reserve

`QMap` 没有 `reserve()`。它按树节点动态分配，不能像连续序列容器一样预留一段元素空间。大批量构造时可以：

- 尽量使用接近 key 顺序的插入；
- 让临时 map 在构造完成后一次性移动；
- 若数据本来是连续记录且主要按位置访问，重新评估 `QList`/`QVector`；
- 若主要按 key 查询且不要求顺序，重新评估 `QHash`。

### 9.2 `keys()`、`values()` 不应代替遍历

下面的代码会创建两个临时列表：

```cpp
for (const auto &key : map.keys())
    process(key, map.value(key));
```

直接遍历 iterator 可以避免复制 key 列表，并且不需要再次按 key 查找：

```cpp
for (auto it = map.cbegin(); it != map.cend(); ++it)
    process(it.key(), it.value());
```

## 10. 线程和所有权边界

### 10.1 隐式共享不等于多个线程可以同时写

多个线程同时读取同一个没有被修改的 map 通常符合值类型使用方式；但只要有线程写入，就需要外部同步。

```cpp
QReadWriteLock lock;
QMap<QString, QByteArray> cache;
```

读取用读锁，更新用写锁，或通过消息传递让一个线程独占 map。不要把“复制是隐式共享”误认为“并发写入自动安全”。

### 10.2 value 指针不是所有权

```cpp
QMap<quint64, QObject *> objects;
```

删除 map 元素不会销毁 `QObject`。如果 QObject 先被父对象销毁，map 中的裸指针也不会自动变成空指针。可以使用 `QPointer` 或对象销毁信号维护索引，但仍需要处理线程和生命周期。

### 10.3 iterator、reference 和返回列表的所有权

- iterator 不拥有 map；
- `first()`、`last()`、`value()` 引用不拥有元素；
- `keys()` 和 `values()` 返回独立列表副本；
- `take()` 返回 value 副本或移动结果，map 不再保存该 value；
- map 销毁或结构修改后，不要继续使用旧 iterator/reference。

## 11. 标准库转换和非成员 API

### 11.1 `std::map<Key, T> QMap::toStdMap() const &`

```cpp
std::map<Key, T> toStdMap() const &;
```

复制当前 QMap 到 `std::map`。结果是独立的标准库容器，之后修改其中一方不影响另一方。

### 11.2 `[since 6.0] std::map<Key, T> QMap::toStdMap() &&`

```cpp
std::map<Key, T> toStdMap() &&;
```

Qt 6.0 起的右值 overload。对临时或明确不再使用的 QMap，可以移动内部数据到 `std::map`，减少复制：

```cpp
std::map<int, QString> result =
    buildQMap().toStdMap();
```

调用后源 QMap 处于有效但内容不应依赖的移动后状态。

### 11.3 `bool operator==(const QMap<Key, T> &, const QMap<Key, T> &)`

比较两个 map 是否有相同的 key/value 集合。比较的是内容，不是内部共享指针；两个独立构造但内容相同的 map 也相等。

### 11.4 `bool operator!=(const QMap<Key, T> &, const QMap<Key, T> &)`

返回 `operator==` 的否定语义，适合直接判断两个 map 内容不同。

### 11.5 `QDataStream &operator<<(QDataStream &, const QMap<Key, T> &)`

```cpp
QDataStream &operator<<(QDataStream &out,
                        const QMap<Key, T> &map);
```

把 map 写入 Qt 数据流。`Key` 和 `T` 必须提供对应的 `QDataStream` 插入操作符。

序列化格式还受到 `QDataStream` version、key/value 类型实现和字节序设置影响。不要把默认数据流字节直接当成永远稳定的跨版本协议；持久化协议应明确版本和兼容策略。

### 11.6 `QDataStream &operator>>(QDataStream &, QMap<Key, T> &)`

```cpp
QDataStream &operator>>(QDataStream &in,
                        QMap<Key, T> &map);
```

从 Qt 数据流读取 map。读取失败时应检查 `QDataStream::status()`，不要仅因为函数返回了流引用就认为 map 数据完整。

反序列化会修改目标 map，读取期间目标原有内容可能被替换或清空。对不可信数据还要设置合理的大小限制，避免异常数据导致过大的内存申请。

### 11.7 `size_t qHash(const QMap<Key, T> &map, size_t seed = 0)`

```cpp
size_t qHash(const QMap<Key, T> &map, size_t seed = 0);
```

为整个 map 计算哈希值。`Key` 和 `T` 必须有可用的 `qHash()`；哈希会按 map 的有序 key/value 范围组合。

这个值适合当前进程内的哈希容器或查找，不适合持久化、跨机器比较或用作密码学摘要。seed 和 Qt 实现版本都可能改变结果。

### 11.8 非成员 `erase_if(QMap &, Predicate)`

这个 API 与成员 `removeIf()` 等价，详见“删除”一节。它不会建立新 map，而是在原 map 上删除谓词匹配的节点并返回数量。

## 12. 常见误区与排查顺序

### 12.1 用 `operator[]` 做只读查询

**症状：** 查一个不存在的配置项后，map 的 size 增加了。

**原因：** 非 const `operator[]` 会插入默认 value。

**修复：** 用 `value()`、`contains()` 或 `find()`。

### 12.2 以为 QMap 保留插入顺序

**症状：** 输出顺序和插入顺序不同。

**原因：** QMap 按 key 排序。

**修复：** 需要插入顺序时单独保存顺序列表；需要按 key 排序时继续使用 QMap。

### 12.3 以为 `insert()` 会保留旧 value

**症状：** 同一个 key 的旧数据被覆盖。

**原因：** QMap 是唯一 key 映射，普通 `insert()` 对已有 key 进行更新。

**修复：** 插入前 `contains()`，或者使用不允许重复/覆盖的业务分支；需要多个 value 时用 `QMultiMap`。

### 12.4 空 map 上调用 `first()` 或 `last()`

**症状：** 调试构建断言，发布构建出现未定义行为风险。

**原因：** 首尾 API 要求 map 非空。

**修复：**

```cpp
if (!map.isEmpty())
    use(map.firstKey(), map.first());
```

### 12.5 把 iterator 当随机访问 iterator

**症状：** 代码使用 `it + n`，或者误以为 `std::distance` 是 O(1)。

**原因：** QMap iterator 是双向迭代器。

**修复：** 用 `std::next`/`std::advance`，并接受线性步进成本；范围查找优先使用 `lowerBound()`/`upperBound()`。

### 12.6 只读遍历意外触发 detach

**症状：** 一个看似只读的函数产生复制开销。

**原因：** 对非常量 map 调用了需要可写 iterator 的 `begin()`、`find()` 或边界查找。

**修复：** 通过 const 引用访问，或使用 const overload。

### 12.7 修改 key

**症状：** 查找失败、顺序损坏或数据无法按预期定位。

**原因：** key 是树排序结构的一部分，不能通过 iterator 直接修改。

**修复：** 保存 value，删除旧 key，再以新 key 插入。

### 12.8 保存引用跨越 map 修改

**症状：** 引用指向旧值，或者访问已经失效的内存。

**原因：** map 插入、删除、detach、clear 或销毁可能改变节点或共享数据。

**修复：** 只在不修改 map 的短作用域内使用引用；需要跨操作保存时复制 value/key。

### 12.9 用 `key()` 作为高性能反向索引

**症状：** 按 value 查询越来越慢。

**原因：** `key(value)` 和 `keys(value)` 都是 O(n) 线性扫描。

**修复：** 建立反向 map/hash，或者重新设计数据模型。

### 12.10 以为删除裸指针会释放对象

**症状：** map 变空了，但对象仍然存在，或者对象先销毁后 map 中出现悬空指针。

**原因：** QMap 不拥有裸指针目标。

**修复：** 明确对象所有权，使用 QObject 父子关系、智能指针或 `QPointer`，并在对象销毁时维护索引。

### 12.11 用 `QMap` 模拟高频哈希表

**症状：** 大量精确 key 查询性能不理想。

**原因：** QMap 的有序树查找是 O(log n)，而业务不需要排序或范围查找。

**修复：** 评估 `QHash`；如果既需要快速查找又需要输出排序，可在输出时复制 key 后排序，或维护两个结构。

## 13. 推荐设计模板

### 13.1 只读查找

```cpp
QString lookupName(const QMap<int, QString> &names, int id)
{
    const auto it = names.constFind(id);
    return it == names.constEnd()
        ? QString()
        : it.value();
}
```

### 13.2 不覆盖旧值

```cpp
bool addIfMissing(QMap<QString, int> &map,
                  const QString &key,
                  int value)
{
    if (map.contains(key))
        return false;

    map.insert(key, value);
    return true;
}
```

若并发环境要求“检查和插入”原子化，必须在外层锁住整个操作；QMap 的两个成员调用不会自动组成跨线程原子事务。

### 13.3 有序范围处理

```cpp
QList<QString> messagesInRange(
    const QMap<qint64, QString> &messages,
    qint64 beginTime,
    qint64 endTime)
{
    QList<QString> result;

    const auto first = messages.lowerBound(beginTime);
    const auto last = messages.lowerBound(endTime);
    for (auto it = first; it != last; ++it)
        result.append(it.value());

    return result;
}
```

这里使用 `[beginTime, endTime)` 半开区间。若要包含恰好等于 `endTime` 的唯一 key，可根据业务改用 `upperBound(endTime)`。

### 13.4 批量删除

```cpp
qsizetype removeInactive(QMap<quint64, Session> &sessions)
{
    return sessions.removeIf([](auto it) {
        return !it.value().isActive();
    });
}
```

谓词只负责判断，不要在其中修改 `sessions` 的结构。

## API 速查表
### 14.1 类型和生命周期

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `key_type` | key 类型别名 | key 必须具有稳定的严格弱序 |
| `mapped_type` | value 类型别名 | `operator[]` 缺失插入时需要默认构造 |
| `difference_type` | 迭代器距离类型 | 双向迭代器，步进通常是 O(n) |
| `size_type` | 数量和删除结果类型 | Qt 6 为 `qsizetype` |
| `iterator` | 可修改 value 的双向迭代器 | key 只读；结构修改可能使其失效 |
| `const_iterator` | 只读双向迭代器 | 只读首选 |
| `key_iterator` | 只遍历 key | key 只读 |
| `key_value_iterator` | 遍历 key/value | value 可修改，key 只读 |
| `const_key_value_iterator` | 只读键值遍历 | key/value 都只读 |
| `Iterator` | `iterator` 的 Qt 别名 | 兼容旧代码 |
| `ConstIterator` | `const_iterator` 的 Qt 别名 | 兼容旧代码 |
| `QMap()` | 构造空 map | 空 map 不能调用首尾 API |
| `QMap(initializer_list)` | 初始化构造 | 重复 key 后者覆盖前者 |
| `QMap(const std::map &)` | 从标准 map 复制 | 两个容器独立 |
| `QMap(std::map &&)` | 从标准 map 移动 | 源 map 内容不应假定 |
| `QMap(const QMap &)` | 隐式共享复制 | 首次写入可能 detach |
| `QMap(QMap &&)` | 移动构造 | 源对象仍有效但内容不确定 |
| `~QMap()` | 销毁 map | 不负责删除裸指针目标 |
| `operator=(const QMap &)` | 复制赋值 | 可能共享内部数据 |
| `operator=(QMap &&)` | 移动赋值 | 替换当前内容 |
| `swap(other)` | 交换两个 map | 通常 O(1)；重新确认 iterator 所属 |

### 14.2 共享和基础状态

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `detach()` | 强制当前对象独占内部数据 | 一般不需手动调用，可能复制 O(n) |
| `isDetached()` | 查询是否未共享 | 实现/性能诊断，不是业务状态 |
| `isSharedWith(other)` | 查询是否共享同一内部数据 | 不等同于内容相等 |
| `referenceHoldingDetach()` | 内部引用保护辅助 | 头文件可见但不建议普通业务依赖 |
| `referenceHoldingDetachExcept(key)` | key 特化引用保护辅助 | 依赖 Qt 实现细节 |
| `size()` | 返回元素数量 | 不等于分配节点容量 |
| `count()` | 返回元素数量 | 无参时等同 `size()` |
| `isEmpty()` | 判断为空 | 不修改 map |
| `empty()` | STL 风格空判断 | 等同 `isEmpty()` |
| `clear()` | 删除全部元素 | 旧 iterator/reference 全部失效 |

### 14.3 按 key 和 value 查询

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `contains(key)` | 判断 key 是否存在 | 不会插入默认 value |
| `count(key)` | 返回 key 数量 | QMap 只会是 0 或 1 |
| `value(key)` | 读取 value | 缺失返回 `T()`，不修改 |
| `value(key, defaultValue)` | 带默认值读取 | 仍不修改 map |
| `operator[](key) const` | const 下标查询 | 缺失返回副本，不插入 |
| `operator[](key)` | 非 const 下标访问 | 缺失插入默认 value |
| `find(key)` | 可修改 iterator 查找 | 缺失返回 `end()`；可能 detach |
| `find(key) const` | const iterator 查找 | 缺失返回 const `end()` |
| `constFind(key)` | 显式只读查找 | 语义等同 const `find()` |
| `key(value)` | 按 value 找一个 key | O(n)，缺失返回默认 key |
| `key(value, defaultKey)` | 按 value 找 key | 不能区分默认 key 与缺失，除非另行判断 |
| `keys()` | 返回全部 key 副本 | 按 key 排序，O(n) |
| `keys(value)` | 返回匹配 value 的 key | 线性扫描 |
| `values()` | 返回全部 value 副本 | 顺序对应 key 排序 |
| `take(key)` | 取出并删除 value | 缺失返回 `T()`；可能 detach |

### 14.4 首尾、边界和插入

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `firstKey()` | 读取最小 key | 空 map 上调用错误；返回引用 |
| `lastKey()` | 读取最大 key | 空 map 上调用错误；返回引用 |
| `first()` | 读取/修改最小 key 的 value | 空 map 上调用错误 |
| `last()` | 读取/修改最大 key 的 value | 空 map 上调用错误 |
| `lowerBound(key)` | 第一个 `>= key` 的 iterator | 没有时返回 `end()` |
| `upperBound(key)` | 第一个 `> key` 的 iterator | 没有时返回 `end()` |
| `equal_range(key)` | 返回等价 key 的半开范围 | QMap 最多一个元素 |
| `insert(key, value)` | 插入或覆盖 | 同 key 覆盖旧 value |
| `insert(pos, key, value)` | 带提示插入或覆盖 | pos 必须来自当前 map |
| `insert(const QMap &other)` | 合并另一个 map | other 的同 key value 优先 |
| `insert(QMap &&other)` | 移动合并另一个 map | 源对象内容不应假定 |
| `erase(pos)` | 删除一个节点 | 返回下一个 iterator |
| `erase(first, last)` | 删除半开范围 | Qt 6.0 起；范围必须属于当前 map |
| `remove(key)` | 删除指定 key | 返回 0 或 1 |
| `removeIf(pred)` | 按谓词删除 | Qt 6.1 起；返回删除数 |
| `erase_if(map, pred)` | 非成员按谓词删除 | Qt 6.1 起；等同 `removeIf` |

### 14.5 遍历和键值范围

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `begin()` | 可修改遍历起点 | 可能 detach |
| `begin() const` | 只读遍历起点 | 不修改 value |
| `end()` | 可修改遍历尾后位置 | 不可解引用；可能 detach |
| `end() const` | 只读遍历尾后位置 | 不可解引用 |
| `cbegin()` / `cend()` | const 遍历入口 | 只读首选 |
| `constBegin()` / `constEnd()` | Qt 风格 const 遍历 | 等同 cbegin/cend |
| `keyBegin()` / `keyEnd()` | 只遍历 key | key 只读 |
| `keyValueBegin()` / `keyValueEnd()` | 遍历 key/value | 非 const value 可修改 |
| `constKeyValueBegin()` / `constKeyValueEnd()` | 显式只读键值遍历 | key/value 都只读 |
| `keyValueBegin() const` / `keyValueEnd() const` | const 键值遍历 | 与 constKeyValue 语义相同 |
| `asKeyValueRange() &` | 左值结构化绑定 range | Qt 6.4 起；引用指向原 map |
| `asKeyValueRange() const &` | const 左值 range | Qt 6.4 起；只读 |
| `asKeyValueRange() &&` | 右值消费 range | Qt 6.4 起；不要保存内部引用 |
| `asKeyValueRange() const &&` | const 右值只读 range | Qt 6.4 起 |

### 14.6 标准库转换和非成员

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `toStdMap() const &` | 复制为 `std::map` | 结果独立；需要复制 |
| `toStdMap() &&` | 移动为 `std::map` | Qt 6.0 起；源对象内容不应假定 |
| `operator==(lhs, rhs)` | 比较内容相等 | 不比较共享身份 |
| `operator!=(lhs, rhs)` | 比较内容不等 | 与 equality 配套 |
| `operator<<(QDataStream &, map)` | 序列化 map | key/value 需支持数据流 |
| `operator>>(QDataStream &, map)` | 反序列化 map | 检查 stream status 和输入大小 |
| `qHash(map, seed)` | 对整个 map 求哈希 | 需 hash key/value；不用于持久化 |

## 15. 一句话总结

`QMap` 是按 key 排序、key 唯一且隐式共享的映射容器：用 `value()`/`find()` 做无副作用查询，用 `operator[]` 明确表达“缺失时创建”，用 `lowerBound()`/`upperBound()` 做范围检索，用 const 遍历避免不必要的 detach，并始终把双向迭代器、引用失效和裸指针所有权当作显式边界处理。
