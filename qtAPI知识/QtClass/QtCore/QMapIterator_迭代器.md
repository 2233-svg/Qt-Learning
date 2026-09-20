# Qt QMapIterator Java 风格只读迭代器深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QMapIterator>`  
> 所属模块：`Qt6::Core`  
> 类型性质：保存 QMap 快照的 Java 风格只读迭代器  
> 相关类型：`QMap`、`QMutableMapIterator`、`QMap::const_iterator`

## 1. 它解决什么问题

`QMapIterator<Key, T>` 为 `QMap` 提供 Qt 传统的 Java 风格遍历接口：

- `hasNext()` / `next()` 向前遍历；
- `hasPrevious()` / `previous()` 向后遍历；
- `peekNext()` / `peekPrevious()` 查看相邻元素但不移动；
- `key()` / `value()` 读取最近一次成功访问的元素；
- `findNext()` / `findPrevious()` 按 value 搜索；
- `toFront()` / `toBack()` 重置遍历位置。

它是**只读迭代器**。如果要修改 value 或删除当前元素，应使用 `QMutableMapIterator`，或者使用 `QMap` 的 STL 风格 `iterator`。

它和 `QMap::const_iterator` 的核心差异是：

| 类型 | 位置模型 | 是否保存容器副本 | 是否能删除/修改 |
| --- | --- | --- | --- |
| `QMapIterator` | 元素之间的 Java 风格位置 | 是，按值保存 QMap 副本 | 不能 |
| `QMap::const_iterator` | 指向节点或尾后位置 | 否，指向具体容器数据 | 不能修改 |
| `QMutableMapIterator` | 元素之间的 Java 风格位置 | 否，绑定原 QMap | 可以删除和修改 value |
| `QMap::iterator` | 指向节点或尾后位置 | 否，指向具体容器数据 | 可以修改 value |

新代码如果采用 range-for、STL 算法或结构化绑定，通常优先使用 `QMap::const_iterator`、`asKeyValueRange()` 或 `QMap::iterator`。`QMapIterator` 的价值主要在于兼容旧式 Qt 代码、需要快照遍历，或希望使用 `findNext()` 这类 Java 风格 API。

## 2. 实际使用场景

### 2.1 兼容旧式 Qt 遍历

```cpp
QMap<int, QWidget *> widgets;
QMapIterator<int, QWidget *> iterator(widgets);

while (iterator.hasNext()) {
    iterator.next();
    qDebug() << iterator.key() << ':' << iterator.value();
}
```

调用 `next()` 后，`key()` 和 `value()` 才表示本次访问的元素。

### 2.2 在 value 中搜索多个匹配项

```cpp
QMap<QString, int> scores;
scores.insert(QStringLiteral("alice"), 10);
scores.insert(QStringLiteral("bob"), 20);
scores.insert(QStringLiteral("carol"), 10);

QMapIterator<QString, int> iterator(scores);
while (iterator.findNext(10))
    qDebug() << iterator.key();
```

`findNext()` 按 map 的遍历顺序继续寻找 value 等于给定值的项。QMap 的遍历顺序按 key 排列，因此匹配结果也按 key 顺序出现。

### 2.3 遍历一个稳定的逻辑快照

```cpp
QMap<QString, QByteArray> current = loadData();
QMapIterator<QString, QByteArray> snapshot(current);

current.insert(QStringLiteral("new-key"), QByteArray("new"));

while (snapshot.hasNext()) {
    snapshot.next();
    inspect(snapshot.key(), snapshot.value());
}
```

`QMapIterator` 内部保存构造时的 QMap 值副本。由于 QMap 隐式共享，构造通常不会立即复制所有节点；当 `current` 后续修改并 detach 时，迭代器仍然遍历原来的逻辑内容。

这个快照特性也可能让代码看不到外部更新，因此使用前要明确这是需求还是意外。

## 3. 位置模型：迭代器位于元素之间

`QMapIterator` 不是“当前指向第一个元素”的指针，而是位于元素之间：

```text
front | item[0] | item[1] | ... | item[n - 1] | back
```

构造后的位置是 `front`：

```text
构造 -> front
next() -> 访问 item[0]，位置移动到 item[0] 后
next() -> 访问 item[1]，位置移动到 item[1] 后
toBack() -> back
previous() -> 访问位置左侧的元素
```

### 3.1 `next()` 的结果和当前位置

`next()` 返回当前位置右侧的元素，然后把位置向后移动。成功调用后：

- 返回的 `Item` 指向刚访问的节点；
- `key()` / `value()` 也表示刚访问的节点；
- 下一次 `next()` 会继续向后。

### 3.2 `previous()` 的结果和当前位置

`previous()` 先向左移动，再返回左侧元素。成功调用后：

- 返回的 `Item` 指向刚访问的节点；
- `key()` / `value()` 表示该节点；
- 下一次 `previous()` 会继续向前。

### 3.3 `peek` 不移动位置

`peekNext()` 和 `peekPrevious()` 只查看邻近元素，不更新“最近访问的元素”状态。因此：

```cpp
const auto nextItem = iterator.peekNext();
// iterator.key() 仍然表示之前的有效项，而不是 nextItem。
```

如果要让 `key()` / `value()` 切换到查看的元素，必须调用 `next()` 或 `previous()`。

## 4. 快照语义和 QMap 修改边界

### 4.1 构造时复制的是容器值，不是深复制 value

```cpp
QMap<int, QObject *> map;
QMapIterator<int, QObject *> iterator(map);
```

迭代器保存的是 QMap 的值副本。对于裸指针、智能指针或其他间接对象，复制的是 value 本身的容器表示，不会自动复制指针指向的对象。

因此：

- 原 map 后续插入或删除不会改变迭代器看到的 key 集合；
- 指针 value 指向的 QObject 被外部修改时，迭代器读到的指针仍可能指向同一个对象；
- value 如果是隐式共享值类型，其底层对象可能继续共享；
- 迭代器不是深度隔离的业务快照。

### 4.2 原 map 修改后，迭代器仍看旧内容

```cpp
QMap<int, QString> map;
map.insert(1, QStringLiteral("one"));

QMapIterator<int, QString> iterator(map);
map.insert(2, QStringLiteral("two"));

// iterator 不会自动看到 key 2。
```

这是预期的 copy-on-write 行为，而不是迭代器刷新失败。

### 4.3 迭代器自身不能修改原 map

`QMapIterator` 没有 `remove()` 或 `setValue()`。如果遍历期间需要结构修改，改用：

```cpp
QMutableMapIterator<int, QString> iterator(map);
```

或者使用：

```cpp
for (auto it = map.begin(); it != map.end();) {
    if (shouldRemove(it.key()))
        it = map.erase(it);
    else
        ++it;
}
```

## 5. 构建与最小代码

### 5.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

### 5.2 头文件

```cpp
#include <QMapIterator>
#include <QMap>
#include <QDebug>
```

`QMapIterator` 头文件会导出相关 QMap 声明，但让实际使用的类型包含关系显式可读，便于以后迁移和工具分析。

### 5.3 最小遍历

```cpp
QMap<int, QString> map{
    {1, QStringLiteral("one")},
    {2, QStringLiteral("two")},
};

QMapIterator<int, QString> iterator(map);
while (iterator.hasNext()) {
    const auto item = iterator.next();
    qDebug() << item.key() << item.value();
}
```

### 5.4 向后遍历

```cpp
QMapIterator<int, QString> iterator(map);
iterator.toBack();

while (iterator.hasPrevious()) {
    const auto item = iterator.previous();
    qDebug() << item.key() << item.value();
}
```

## 6. 逐项 API 说明

### 6.1 `QMapIterator<Key, T>::Item`

```cpp
using Item = QMap<Key, T>::const_iterator;
```

`Item` 是 `QMap` 的 const iterator 别名。`next()`、`previous()`、`peekNext()` 和 `peekPrevious()` 返回它。

可以通过 `Item` 读取 key/value：

```cpp
const auto item = iterator.next();
qDebug() << item.key() << item.value();
```

**边界：**

- `Item` 是只读 iterator；
- `Item` 不拥有 map；
- `Item` 的有效期受 `QMapIterator` 内部快照生命周期约束；
- 不要用它修改 value 或 key；
- 不要在对应迭代器对象销毁后保存并使用它。

### 6.2 `QMapIterator::QMapIterator(const QMap<Key, T> &map)`

```cpp
QMapIterator(const QMap<Key, T> &map);
```

以 `map` 的当前值内容构造迭代器，初始位置为 `front`。

**关键语义：**

- 构造不会修改原 map；
- 内部保存 QMap 值副本，通常利用隐式共享避免立即复制；
- 后续原 map 的结构修改不会刷新迭代器内容；
- 迭代顺序仍然是 QMap 的 key 顺序；
- value 指针指向的对象不会被深复制。

### 6.3 `QMapIterator<Key, T> &QMapIterator::operator=(const QMap<Key, T> &map)`

```cpp
QMapIterator &operator=(const QMap<Key, T> &map);
```

让迭代器重新绑定到 `map` 的当前值内容，并把位置重置到 `front`。

```cpp
iterator = anotherMap;
while (iterator.hasNext()) {
    iterator.next();
    inspect(iterator.key(), iterator.value());
}
```

赋值后，之前绑定的快照不再作为当前遍历目标。之前从 `next()` 等 API 得到的 `Item` 不应继续和新目标混用。

### 6.4 `bool QMapIterator::hasNext() const`

```cpp
bool hasNext() const;
```

判断当前位置后方是否还有元素。

```cpp
while (iterator.hasNext()) {
    iterator.next();
    use(iterator.key(), iterator.value());
}
```

当返回 `false` 时，不要调用 `next()` 或 `peekNext()`。遍历空 map 时，构造后 `hasNext()` 立即为 `false`。

### 6.5 `QMapIterator<Key, T>::Item QMapIterator::next()`

```cpp
Item next();
```

返回当前位置右侧的下一个元素，并把位置向后移动。

**调用前提：**

- 应先确认 `hasNext()` 为 `true`；
- 成功后才可以读取 `key()` 和 `value()`；
- 返回的 `Item` 是只读 iterator。

越过 `back` 调用 `next()` 会产生无效结果，不能依赖其返回值。

### 6.6 `QMapIterator<Key, T>::Item QMapIterator::peekNext() const`

```cpp
Item peekNext() const;
```

返回当前位置右侧的元素，但不改变位置和最近访问项。

```cpp
if (iterator.hasNext()) {
    const auto item = iterator.peekNext();
    inspect(item.key(), item.value());
}
```

调用前应确认 `hasNext()`。它不会让 `iterator.key()` 或 `iterator.value()` 变成 `item`。

### 6.7 `bool QMapIterator::hasPrevious() const`

```cpp
bool hasPrevious() const;
```

判断当前位置左侧是否还有元素。

构造后位于 `front`，所以 `hasPrevious()` 初始为 `false`。调用 `toBack()` 后，如果 map 非空，`hasPrevious()` 为 `true`。

### 6.8 `QMapIterator<Key, T>::Item QMapIterator::previous()`

```cpp
Item previous();
```

把位置向前移动一个元素，并返回该元素。

```cpp
iterator.toBack();
while (iterator.hasPrevious()) {
    const auto item = iterator.previous();
    inspect(item.key(), item.value());
}
```

调用前应确认 `hasPrevious()` 为 `true`。在 `front` 调用会越过边界，结果无效。

### 6.9 `QMapIterator<Key, T>::Item QMapIterator::peekPrevious() const`

```cpp
Item peekPrevious() const;
```

返回当前位置左侧的元素，但不改变位置和最近访问项。

```cpp
if (iterator.hasPrevious()) {
    const auto item = iterator.peekPrevious();
    inspect(item.key(), item.value());
}
```

调用前应确认 `hasPrevious()`。它不会更新 `key()` / `value()` 对应的最近访问元素。

### 6.10 `const Key &QMapIterator::key() const`

```cpp
const Key &key() const;
```

返回最近一次成功由 `next()`、`previous()`、`findNext()` 或 `findPrevious()` 访问的元素的 key。

**关键边界：**

- 构造后、`toFront()` 后或失败搜索后，不一定存在有效的最近元素；
- 应在成功访问 API 返回后读取；
- 返回引用只在迭代器内部快照和对应节点存活期间有效；
- key 只读，不能通过它修改 QMap 的排序字段。

### 6.11 `const T &QMapIterator::value() const`

```cpp
const T &value() const;
```

返回最近一次成功访问的元素的只读 value 引用。

```cpp
if (iterator.findNext(expectedValue))
    use(iterator.key(), iterator.value());
```

如果没有成功调用过 `next()`、`previous()` 或搜索 API，就不要读取它。需要长期保存时复制 value，而不是保存引用。

### 6.12 `void QMapIterator::toFront()`

```cpp
void toFront();
```

把位置重置到第一个元素之前，并清除当前最近访问项。

```cpp
iterator.toFront();
while (iterator.hasNext()) {
    iterator.next();
    inspect(iterator.key(), iterator.value());
}
```

调用后 `hasPrevious()` 为 `false`。即使 map 非空，也必须再次调用 `next()` 后才能读取有效的 `key()` / `value()`。

### 6.13 `void QMapIterator::toBack()`

```cpp
void toBack();
```

把位置移动到最后一个元素之后，并清除当前最近访问项。

```cpp
iterator.toBack();
while (iterator.hasPrevious()) {
    iterator.previous();
    inspect(iterator.key(), iterator.value());
}
```

调用后 `hasNext()` 为 `false`。需要向后读取时，应先检查 `hasPrevious()`。

### 6.14 `bool QMapIterator::findNext(const T &value)`

```cpp
bool findNext(const T &value);
```

从当前位置向后查找 value 等于给定值的元素。

```cpp
iterator.toFront();
while (iterator.findNext(target)) {
    qDebug() << iterator.key() << iterator.value();
}
```

**返回和位置语义：**

- 找到时返回 `true`，最近访问项变为匹配元素，位置越过该元素；
- 找不到时返回 `false`，位置移动到 `back`，最近访问项变为无效；
- 成功时可读取 `key()` / `value()`；
- 比较的是 value，不是 key；
- QMap 的顺序按 key 排列，因此搜索顺序是排序后的顺序。

如果 value 类型包含昂贵比较，`findNext()` 会逐项比较，复杂度为 O(n)。

### 6.15 `bool QMapIterator::findPrevious(const T &value)`

```cpp
bool findPrevious(const T &value);
```

从当前位置向前查找 value 等于给定值的元素。

```cpp
iterator.toBack();
while (iterator.findPrevious(target)) {
    qDebug() << iterator.key() << iterator.value();
}
```

**返回和位置语义：**

- 找到时返回 `true`，最近访问项变为匹配元素，位置移动到该元素之前；
- 找不到时返回 `false`，位置回到 `front`，最近访问项无效；
- 失败后不能继续读取 `key()` / `value()`；
- 比较的是 value，不是 key；
- 复杂度为 O(n)。

## 7. 典型状态流程

### 7.1 正向完整遍历

```text
构造
  |
  v
front --next()--> item[0] 后 --next()--> ... --next()--> back
```

代码：

```cpp
QMapIterator<int, QString> iterator(map);
while (iterator.hasNext()) {
    iterator.next();
    process(iterator.key(), iterator.value());
}
```

### 7.2 反向完整遍历

```text
构造 --toBack()--> back
back --previous()--> item[n - 1] 前 --previous()--> ... --previous()--> front
```

### 7.3 搜索多个匹配 value

```cpp
QMapIterator<QString, int> iterator(map);
while (iterator.findNext(targetValue))
    collect(iterator.key());
```

循环条件中的下一次 `findNext()` 会从上一次匹配项之后继续。不要在循环体中调用 `toFront()`，否则会重新从头搜索。

## 8. 迭代器与容器选择

### 8.1 只读且需要快照

使用 `QMapIterator`：

```cpp
QMapIterator<Key, Value> iterator(map);
```

适合原 map 可能随后 detach，但当前遍历必须保持构造时内容的场景。

### 8.2 只读且需要现代 C++ 遍历

优先：

```cpp
for (auto it = map.cbegin(); it != map.cend(); ++it)
    process(it.key(), it.value());
```

或 Qt 6.4 起：

```cpp
for (auto [key, value] : map.asKeyValueRange())
    process(key, value);
```

这两种方式直接作用于 map 当前数据，不自动创建 `QMapIterator` 的快照副本。

### 8.3 需要删除或修改

使用 `QMutableMapIterator`：

```cpp
QMutableMapIterator<Key, Value> iterator(map);
while (iterator.hasNext()) {
    iterator.next();
    if (shouldRemove(iterator.key()))
        iterator.remove();
}
```

或者使用 QMap 的 STL 风格 iterator。不要试图通过 `QMapIterator::Item` 修改 value。

## 9. 常见误区与排查顺序

### 9.1 构造后直接读取 `key()` / `value()`

**问题：** 构造后迭代器在 `front`，还没有当前元素。

**修复：** 先调用 `hasNext()`，再调用 `next()`，成功后读取。

### 9.2 `hasNext()` 为 false 仍调用 `next()`

**问题：** 越过 `back`，结果无效。

**修复：** 用 `while (hasNext())` 包住 `next()`。

### 9.3 `peekNext()` 后误以为当前项已经移动

**问题：** `peekNext()` 不会更新当前位置或 `key()`/`value()`。

**修复：** 只想查看就读取返回的 `Item`；想移动就调用 `next()`。

### 9.4 失败搜索后继续读取当前项

**问题：** `findNext()` 或 `findPrevious()` 返回 `false` 时，当前位置已经到边界，最近访问项无效。

**修复：** 只在返回 `true` 时读取 `key()` / `value()`。

### 9.5 以为原 map 的新插入会被迭代器看到

**问题：** QMapIterator 保存了构造时的值副本。

**修复：** 需要遍历最新内容时重新构造或使用 `operator=` 重新绑定。

### 9.6 以为快照是深复制

**问题：** 指针 value 或隐式共享对象仍可能指向共同对象。

**修复：** 如果业务需要深快照，显式复制 value 指向的数据，而不是只复制 QMap。

### 9.7 用 `findNext()` 期待按 key 查找

**问题：** 它比较的是 value。

**修复：** 按 key 查找使用 `QMap::find()`、`constFind()` 或边界查找 API。

### 9.8 在快照迭代器中修改原 map

**问题：** 迭代器不会因此变成可变迭代器，也不会同步新结构。

**修复：** 使用 `QMutableMapIterator` 或 QMap 的可变 iterator。

### 9.9 用 QMapIterator 做高性能随机访问

**问题：** QMap 本身按树结构组织，迭代器只能逐步前进或后退。

**修复：** 需要按位置访问时使用序列容器；需要按 key 范围访问时使用 `lowerBound()` / `upperBound()`。

## 10. 线程和生命周期边界

### 10.1 迭代器对象本身是值类型

`QMapIterator` 可以复制和赋值，因为它内部保存 QMap 值副本和当前位置。复制迭代器会复制当前遍历状态的值语义，不会让两个迭代器共享一个可变光标。

```cpp
QMapIterator<int, QString> first(map);
QMapIterator<int, QString> second = first;

first.next();
// second 的位置不随 first 自动移动。
```

### 10.2 线程安全只来自快照的结构隔离，不来自 value 业务

原 map 在另一个线程修改并 detach 后，当前 iterator 仍可遍历自己的共享快照；但这不代表：

- value 指向的对象可以无锁并发访问；
- value 类型内部状态自动线程安全；
- 原 map 的销毁可以打断正在执行的 value 业务；
- 迭代器可以跨线程随意传递而不考虑线程同步。

需要跨线程传递时，先明确是传递 QMap 值副本，还是传递共享对象引用。

### 10.3 迭代器不拥有外部对象

如果 value 是裸指针，QMapIterator 不负责保持指针目标存活。快照只保证 map 节点和指针值的生命周期，不保证外部 QObject 或业务对象的生命周期。

## API 速查表
| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QMapIterator<Key, T>::Item` | `QMap::const_iterator` 别名 | 只读、不拥有容器；来源 iterator 销毁后不要使用 |
| `QMapIterator(const QMap<Key, T> &map)` | 创建快照式只读迭代器 | 初始位置为 front；原 map 后续结构修改不会刷新快照 |
| `operator=(const QMap<Key, T> &map)` | 重新绑定 map 并重置位置 | 旧快照和旧 Item 不再是当前遍历目标 |
| `hasNext() const` | 判断后方是否有元素 | false 时不能调用 `next()`/`peekNext()` |
| `next()` | 返回下一个 Item 并向后移动 | 成功后 `key()`/`value()` 才有效 |
| `peekNext() const` | 查看下一个 Item 但不移动 | 不更新当前位置和最近访问项 |
| `hasPrevious() const` | 判断前方是否有元素 | 构造或 `toFront()` 后为 false |
| `previous()` | 返回前一个 Item 并向前移动 | false 时不能调用 |
| `peekPrevious() const` | 查看前一个 Item 但不移动 | 不更新当前位置和最近访问项 |
| `key() const` | 读取最近成功访问项的 key | 先成功调用 next/previous/find |
| `value() const` | 读取最近成功访问项的 value | 返回 const 引用，注意生命周期 |
| `toFront()` | 移到第一个元素之前 | 清除当前访问项 |
| `toBack()` | 移到最后一个元素之后 | 清除当前访问项 |
| `findNext(value)` | 向后查找匹配 value | 成功返回 true；失败到 back |
| `findPrevious(value)` | 向前查找匹配 value | 成功返回 true；失败到 front |

## 12. 一句话总结

`QMapIterator` 是保存 QMap 值副本的 Java 风格只读迭代器：位置在元素之间，先用 `hasNext()`/`hasPrevious()` 检查边界，再用 `next()`/`previous()` 取得当前项；`key()`/`value()` 只在成功访问后有效，原 map 的结构修改不会刷新快照，需要修改或删除时应改用 `QMutableMapIterator` 或 QMap 的 STL 风格迭代器。
