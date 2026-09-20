# Qt Core 基础：容器与迭代器

> 适用版本：Qt 6.11.1  
> 所属模块：Qt Core  
> 核心类型：`QList`、`QMap`、`QHash`、`QSet`、`QQueue`、`QStack`

## 1. 容器解决什么问题

容器负责保存一组同类型数据，并提供插入、删除、查找和遍历能力。

```cpp
QList<QString> names;
names.append(QStringLiteral("Alice"));
names.append(QStringLiteral("Bob"));
```

Qt 容器是模板类，可以保存基本类型、可复制值类型和指针：

```cpp
QList<int> numbers;
QList<QString> texts;
QHash<QString, int> scores;
QList<QObject *> objects;
```

但“能够保存指针”不等于“容器拥有指针所指对象”。所有权必须单独设计。

## 2. 先按数据语义选择容器

| 需求 | 推荐容器 |
|---|---|
| 按索引保存一串值 | `QList<T>` |
| 先进先出 | `QQueue<T>` |
| 后进先出 | `QStack<T>` |
| 唯一元素集合、快速判断存在 | `QSet<T>` |
| 键值映射且按键排序 | `QMap<Key, T>` |
| 键值映射且更关注查找速度 | `QHash<Key, T>` |
| 一个键允许多个值且按键排序 | `QMultiMap<Key, T>` |
| 一个键允许多个值且使用哈希 | `QMultiHash<Key, T>` |
| 小数组优先在栈上预分配 | `QVarLengthArray<T, N>` |

容器选择首先取决于语义，其次才是性能。不要只因为 `QHash` 平均查找快就放弃业务所需的稳定排序。

## 3. QList：Qt 6 的通用顺序容器

Qt 6 中 `QList<T>` 连续存储元素，`QVector<T>` 与 `QList<T>` 使用统一实现。新代码通常直接选择 `QList`。

```cpp
QList<int> values = {10, 20, 30};

values.append(40);
values.prepend(0);
values.insert(2, 15);
```

### 3.1 访问元素

```cpp
int first = values.first();
int last = values.last();
int item = values.at(2);
int another = values[2];
```

读取时推荐 `at()`，它清楚表达只读意图，且不会触发写时分离。访问前仍需保证索引有效：

```cpp
if (index >= 0 && index < values.size())
    use(values.at(index));
```

### 3.2 头部和中间插入的代价

连续存储意味着中间插入或删除可能移动后续大量元素：

```text
[A][B][C][D]
      ↑ 插入 X
[A][B][X][C][D]
```

尾部追加通常很快；频繁在巨大容器中部插入时，需要重新评估数据结构和算法，而不是先假定 Qt 容器会自动优化。

### 3.3 reserve 与容量

```cpp
QList<Record> records;
records.reserve(expectedCount);

for (const Source &source : sources)
    records.append(makeRecord(source));
```

`reserve()` 预留容量但不改变元素数量：

```cpp
records.reserve(100);
Q_ASSERT(records.size() == 0);
```

它适合已知大致元素数量的批量构造，可减少多次重新分配。

## 4. QQueue 与 QStack

### 4.1 QQueue：FIFO

```cpp
QQueue<QString> tasks;
tasks.enqueue(QStringLiteral("first"));
tasks.enqueue(QStringLiteral("second"));

QString next = tasks.dequeue(); // first
```

读取但不移除队头：

```cpp
if (!tasks.isEmpty())
    qDebug() << tasks.head();
```

### 4.2 QStack：LIFO

```cpp
QStack<QString> history;
history.push(QStringLiteral("page-1"));
history.push(QStringLiteral("page-2"));

QString current = history.pop(); // page-2
```

读取但不移除栈顶：

```cpp
if (!history.isEmpty())
    qDebug() << history.top();
```

调用 `dequeue()`、`pop()`、`head()` 或 `top()` 前先确认非空。

## 5. QSet：只关心唯一性与存在性

```cpp
QSet<QString> permissions;
permissions.insert(QStringLiteral("read"));
permissions.insert(QStringLiteral("write"));
permissions.insert(QStringLiteral("read"));

Q_ASSERT(permissions.size() == 2);
```

检查存在：

```cpp
if (permissions.contains(QStringLiteral("write"))) {
    saveDocument();
}
```

集合运算：

```cpp
QSet<int> left = {1, 2, 3};
QSet<int> right = {3, 4};

QSet<int> all = left | right;       // 并集
QSet<int> common = left & right;    // 交集
QSet<int> onlyLeft = left - right;  // 差集
```

`QSet` 基于哈希，不应依赖遍历顺序。

## 6. QMap 与 QHash 的核心区别

### 6.1 QMap：按键排序

```cpp
QMap<QString, int> scores;
scores.insert(QStringLiteral("Bob"), 80);
scores.insert(QStringLiteral("Alice"), 95);
```

遍历时按 key 的排序规则输出 `Alice`、`Bob`。键类型需要提供严格弱序关系，通常通过 `operator<` 或比较支持。

典型复杂度：查找、插入和删除为对数级。

### 6.2 QHash：哈希查找

```cpp
QHash<QString, int> scores;
scores.insert(QStringLiteral("Bob"), 80);
scores.insert(QStringLiteral("Alice"), 95);
```

平均查找通常接近常数级，但遍历顺序未定义，并且不同运行中可能不同。需要排序显示时，应显式排序 key，而不是碰巧观察当前顺序。

### 6.3 选择原则

```text
需要按 key 排序或稳定的键顺序 → QMap
不需要顺序，查找量较大          → QHash
只判断元素是否存在              → QSet
```

## 7. 安全查询键值

### 7.1 contains + value

```cpp
if (scores.contains(name)) {
    const int score = scores.value(name);
}
```

### 7.2 find 避免重复查找

```cpp
auto iterator = scores.constFind(name);
if (iterator != scores.cend()) {
    const int score = iterator.value();
}
```

### 7.3 指定默认值

```cpp
const int score = scores.value(name, -1);
```

默认值必须不会和合法业务值产生歧义，或者配合 `contains()` 判断。

## 8. 非 const operator[] 的隐式插入陷阱

```cpp
QHash<QString, int> counts;

int count = counts[QStringLiteral("missing")];
```

对非 const 映射使用 `operator[]` 时，键不存在会插入一个默认构造值。这里会新增键并将值设为 0。

如果只想查询：

```cpp
const int count = counts.value(QStringLiteral("missing"), 0);
```

如果明确要统计，隐式插入反而很方便：

```cpp
for (const QString &word : words)
    ++counts[word];
```

关键不在于 `operator[]` 好坏，而在于是否明确需要“缺失时插入”。

## 9. Multi 容器

一个键需要多个值时：

```cpp
QMultiMap<QString, QString> tags;
tags.insert(QStringLiteral("language"), QStringLiteral("C++"));
tags.insert(QStringLiteral("language"), QStringLiteral("QML"));

const QList<QString> languages =
    tags.values(QStringLiteral("language"));
```

如果经常整体读取和替换一个键下的全部值，下面的结构有时更清晰：

```cpp
QHash<QString, QList<QString>> tags;
```

选择取决于操作模式：是把每个键值对视为独立记录，还是把列表视为一个键的整体值。

## 10. 容器中保存什么类型

Qt 容器适合保存可复制或可移动的值类型：

```cpp
QList<QString> names;
QList<QDateTime> times;
QList<MyValueType> records;
```

`QObject` 不可复制，因此不能这样写：

```cpp
QList<QObject> objects; // 错误
```

可以保存指针：

```cpp
QList<QObject *> objects;
```

但必须明确所有权：

- 对象由共同父对象拥有
- 容器仅观察对象
- 使用 `QPointer<T>` 防止观察指针悬空
- 使用智能指针表达非 QObject 所有权

清空指针容器只会删除指针值，不会自动删除目标对象：

```cpp
objects.clear(); // 不等于逐个 delete
```

## 11. 范围 for

只读遍历：

```cpp
for (const QString &name : names)
    qDebug() << name;
```

修改元素：

```cpp
for (QString &name : names)
    name = name.trimmed();
```

### 11.1 隐式共享容器的 detach

Qt 容器通常隐式共享。对一个非 const 容器调用非 const `begin()` 可能触发数据分离，即使循环体只读。

明确只读：

```cpp
#include <utility>

for (const QString &name : std::as_const(names))
    qDebug() << name;
```

这避免意外调用非 const 迭代入口。

### 11.2 不要在范围 for 中改变容器结构

危险：

```cpp
for (const QString &name : names) {
    if (name.isEmpty())
        names.removeOne(name); // 迭代器可能失效
}
```

优先使用 `removeIf()`：

```cpp
names.removeIf([](const QString &name) {
    return name.isEmpty();
});
```

## 12. STL 风格迭代器

```cpp
for (auto it = names.cbegin(); it != names.cend(); ++it)
    qDebug() << *it;
```

- `begin()/end()`：可修改迭代器
- `cbegin()/cend()`：只读迭代器
- `rbegin()/rend()`：反向迭代器
- `crbegin()/crend()`：只读反向迭代器

`end()` 表示尾后位置，绝不能解引用。空容器中 `begin() == end()`。

优先使用前置递增：

```cpp
++it;
```

后置 `it++` 需要保留递增前的值，某些迭代器上可能产生不必要临时对象。

## 13. 迭代中安全删除

```cpp
for (auto it = names.begin(); it != names.end(); ) {
    if (it->isEmpty())
        it = names.erase(it);
    else
        ++it;
}
```

`erase(it)` 返回删除位置之后的有效迭代器。不能删除后再对旧迭代器执行 `++it`。

对于条件删除，`removeIf()` 或自由函数 `erase_if()` 通常更清晰。

## 14. 关联容器迭代器

```cpp
for (auto it = scores.cbegin(); it != scores.cend(); ++it) {
    qDebug() << it.key() << it.value();
}
```

只遍历 key：

```cpp
for (const QString &key : scores.keys())
    qDebug() << key;
```

`keys()` 会创建一个新列表。性能敏感时使用 key 迭代器：

```cpp
for (auto it = scores.keyBegin(); it != scores.keyEnd(); ++it)
    qDebug() << *it;
```

同时访问键和值可使用键值范围：

```cpp
for (auto [key, value] : scores.asKeyValueRange())
    qDebug() << key << value;
```

是否加引用和 const 取决于是否需要修改值以及希望避免复制。

## 15. 迭代器失效与隐式共享问题

容器结构变化、重新分配或隐式共享分离可能使迭代器失效：

```cpp
QList<int> first = {1, 2, 3};
QList<int> second = first; // 共享数据

auto it = first.cbegin();
first.append(4);           // first 可能分离，it 失效
```

基本规则：

1. 修改容器后重新获取迭代器。
2. 不要跨越未知函数调用长期保存迭代器。
3. 不要混用一个共享副本的迭代器和另一个副本。
4. 删除时使用 API 返回的新迭代器。
5. 如果需要稳定引用，确认具体容器和操作的失效规则。

## 16. 隐式共享的成本模型

```cpp
QList<LargeValue> first = loadValues();
QList<LargeValue> second = first;
```

复制容器通常只增加共享数据的引用计数。首次修改某个共享副本时才深复制：

```cpp
second.append(newValue); // 可能复制底层容器数据
```

这有两面性：

- 按值传递和返回通常比想象中便宜。
- 某次看似简单的修改可能突然承担深复制成本。

性能优化应关注实际数据规模和修改模式，不能只数 C++ 源码中的复制语句。

## 17. QHash 自定义键

自定义键需要相等比较和哈希函数：

```cpp
struct UserId
{
    int organization;
    int user;

    friend bool operator==(const UserId &, const UserId &) = default;
};

size_t qHash(const UserId &id, size_t seed = 0) noexcept
{
    return qHashMulti(seed, id.organization, id.user);
}
```

使用：

```cpp
QHash<UserId, QString> names;
names.insert(UserId{7, 42}, QStringLiteral("Alice"));
```

哈希必须遵守：相等的键产生相同哈希值。不要忽略 `seed`，它用于增强哈希表对恶意碰撞输入的抵抗能力。

## 18. QMap 自定义键

键需要可排序：

```cpp
struct Version
{
    int major;
    int minor;

    friend bool operator<(const Version &left, const Version &right)
    {
        return std::tie(left.major, left.minor)
             < std::tie(right.major, right.minor);
    }
};
```

比较必须形成严格弱序。相互矛盾或不稳定的比较会破坏映射内部结构假设。

## 19. Qt 容器与标准库算法

Qt 的 STL 风格迭代器可以配合标准算法：

```cpp
#include <algorithm>

QList<int> values = {4, 1, 3, 2};
std::sort(values.begin(), values.end());

auto found = std::find(values.cbegin(), values.cend(), 3);
```

也可以使用 C++20 ranges，但要确认当前编译器和目标类型支持情况。

Qt 容器与 `std::vector`、`std::map` 等并非互斥。选择应考虑：

- Qt API 是否直接接收该容器
- 是否需要隐式共享
- 标准算法和团队习惯
- ABI、库边界和性能特征

不要进行没有必要的 Qt/STL 容器来回转换。

## 20. 容器与线程安全

Qt 容器通常是可重入的：不同线程操作各自独立的容器实例没有问题。

隐式共享允许多个线程只读各自的共享副本，但这不代表可以无同步地同时修改同一个容器对象：

```text
不同实例，各自操作       → 通常安全
同一实例，多线程只读     → 在没有并发写入时可行
同一实例，至少一个线程写 → 需要锁或线程封闭
```

最简单可靠的设计通常是让一个容器归属于一个线程，通过信号传递值副本或不可变快照。

## 21. 综合示例：统计并排序单词

```cpp
#include <QHash>
#include <QList>
#include <QRegularExpression>
#include <QString>
#include <QStringList>
#include <algorithm>

struct WordCount
{
    QString word;
    int count;
};

QList<WordCount> countWords(const QString &text)
{
    const QStringList words = text.toCaseFolded().split(
        QRegularExpression(QStringLiteral(R"(\W+)")),
        Qt::SkipEmptyParts);

    QHash<QString, int> counts;
    counts.reserve(words.size());

    for (const QString &word : words)
        ++counts[word];

    QList<WordCount> result;
    result.reserve(counts.size());

    for (auto it = counts.cbegin(); it != counts.cend(); ++it)
        result.append(WordCount{it.key(), it.value()});

    std::sort(result.begin(), result.end(),
              [](const WordCount &left, const WordCount &right) {
        if (left.count != right.count)
            return left.count > right.count;
        return left.word < right.word;
    });

    return result;
}
```

这里的容器选择：

- `QStringList` 保存分割后的顺序数据。
- `QHash` 快速累计每个单词次数。
- `QList<WordCount>` 保存最终可排序结果。
- `std::sort` 明确规定输出顺序，不依赖 `QHash` 遍历顺序。

## 22. 常见错误

### 22.1 依赖 QHash 的遍历顺序

顺序未定义。需要顺序时使用 `QMap` 或提取后显式排序。

### 22.2 查询时误用非 const operator[]

会插入缺失键。只读查询使用 `value()`、`constFind()` 或先 `contains()`。

### 22.3 修改容器后继续使用旧迭代器

修改可能重新分配或分离共享数据。重新获取迭代器。

### 22.4 在范围 for 内删除元素

会破坏循环内部迭代器。使用 `removeIf()` 或正确的 `erase()` 循环。

### 22.5 以为指针容器会删除对象

清空容器只移除指针值。对象应由父对象、智能指针或明确清理代码拥有。

### 22.6 为了性能盲目选择 QHash

数据规模很小时差异可能无意义，而丢失有序性反而增加后续排序复杂度。先按语义选择并测量热点。

## 23. API 速查

| API | 作用 | 注意点 |
|---|---|---|
| `append()` | 尾部追加 | QList 常用高效操作 |
| `prepend()` | 头部插入 | 可能移动大量元素 |
| `insert()` | 指定位置插入 | 可能使迭代器失效 |
| `at()` | 只读索引访问 | 调用前保证索引有效 |
| `reserve()` | 预留容量 | 不改变 size |
| `removeIf()` | 按条件删除 | 比循环中手动删除清晰 |
| `contains()` | 判断元素或键存在 | QSet/QHash 常用 |
| `value()` | 查询映射值 | 缺失时不插入 |
| `operator[]` | 查询或写入映射 | 非 const 对象缺失时插入 |
| `find/constFind` | 返回键迭代器 | 可避免重复查找 |
| `erase(iterator)` | 删除迭代位置 | 使用返回的新迭代器 |
| `cbegin/cend` | 只读遍历 | 避免意外修改和 detach |
| `keys()` | 复制全部键到列表 | 大容器注意分配成本 |
| `keyBegin/keyEnd` | 不复制地遍历键 | 适合性能敏感代码 |
| `asKeyValueRange()` | 同时遍历键和值 | 可配合结构化绑定 |
| `qHashMulti()` | 组合自定义键字段 | 保留 seed |

## 24. 自测题

1. Qt 6 中 `QList` 的主要存储特点是什么？
2. `QMap` 和 `QHash` 最重要的区别是什么？
3. 为什么只读查询不应随意使用非 const `operator[]`？
4. `reserve(100)` 后容器的 `size()` 是多少？
5. 为什么不能在范围 for 中直接删除当前容器元素？
6. 隐式共享如何影响复制和首次修改？
7. `QList<QObject *>` 是否拥有其中对象？
8. 自定义 QHash 键需要提供什么？
9. 删除迭代器位置后应怎样继续循环？
10. 多线程可以无锁修改同一个 Qt 容器吗？

### 参考答案

1. 元素连续存储，适合索引和尾部追加；中间插入可能移动元素。
2. QMap 按键排序，QHash 顺序未定义但平均查找更快。
3. 键不存在时会插入默认值，意外改变容器。
4. 仍为 0，reserve 只改变容量。
5. 结构修改可能使循环使用的迭代器失效。
6. 复制通常共享数据，首次非 const 修改可能深复制分离。
7. 不一定；指针容器本身不表达目标对象所有权。
8. 相等比较和接收 seed 的 `qHash()`。
9. 使用 `erase()` 返回的下一个有效迭代器。
10. 不可以；同一实例有并发写入时需要同步或线程封闭。

---

## 总结

容器学习的重点不是记住所有函数，而是让数据结构匹配业务语义：顺序数据用 `QList`，唯一集合用 `QSet`，有序映射用 `QMap`，快速无序映射用 `QHash`。进阶使用必须理解连续存储、隐式共享和迭代器失效，并明确指针元素的所有权。只要查询不意外插入、修改不继续使用旧迭代器、遍历不依赖未定义顺序，绝大多数容器问题都能提前避免。
