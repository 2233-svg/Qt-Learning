# QMultiMapIterator：QMultiMap 的 Java 风格只读迭代器

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QMultiMapIterator>`  
> 模块：`Qt6::Core`  
> 类型：`template <typename Key, typename T> class QMultiMapIterator`  
> 相关类型：`QMultiMap`、`QMutableMultiMapIterator`

`QMultiMapIterator<Key, T>` 是用于 `QMultiMap` 的 Java 风格只读迭代器。它的游标位于条目**之间**，而不是直接指向条目；因此必须先用 `next()` 或 `previous()` 跨过一条记录，之后才可通过 `key()` 和 `value()` 读取那条记录。

Qt 现在更推荐 STL 风格的 `QMultiMap::const_iterator`，因为它更高效且能直接和标准算法配合。`QMultiMapIterator` 仍适合已有 Java 风格迭代代码、需要前后移动状态机的代码，以及需要“遍历快照不受原 map 后续写入影响”的场景。

## 它解决什么问题

普通 STL 迭代器直接“站在”某一项上：`*it` 就是当前值。`QMultiMapIterator` 则将位置放在两项之间，提供：

- `hasNext()` / `next()`：从前向后跨越记录；
- `hasPrevious()` / `previous()`：从后向前跨越记录；
- `toFront()` / `toBack()`：跳到首前或尾后；
- `findNext(value)` / `findPrevious(value)`：按值持续搜索；
- `key()` / `value()`：读取最近一次跨越或成功找到的记录。

```cpp
#include <QMultiMap>
#include <QMultiMapIterator>

QMultiMap<int, QString> events;
events.insert(10, "open");
events.insert(20, "render");
events.insert(20, "thumbnail");

QMultiMapIterator<int, QString> it(events);
while (it.hasNext()) {
    it.next();
    qDebug() << it.key() << it.value();
}
```

这里按 `QMultiMap` 的顺序输出：键整体升序；相同键的值从最近插入到最早插入。

## 最重要的模型：游标在条目之间

构造后或调用 `toFront()` 后，游标位于第一条记录之前：

```text
front  | item 1 | item 2 | ... | item n | back
       ^ 初始位置 / toFront()
```

调用 `next()` 后，函数返回 item 1，游标移动到 item 1 与 item 2 之间；此时 `key()` / `value()` 对应 item 1。调用 `previous()` 的方向相反：它跨越游标之前的记录，并把游标移到该记录之前。

这解释了几条常见规则：

- 初始位置可以 `hasNext()`，但不能 `key()`、`value()` 或 `peekPrevious()`；
- `toBack()` 后可以 `hasPrevious()`，但不能 `key()`、`value()` 或 `next()`；
- `next()` / `previous()` 返回的是跨越的条目，并更新“当前可读项”；
- `peekNext()` / `peekPrevious()` 只观察，不移动游标，也不把被观察项设为 `key()` / `value()` 的当前项。

## 正向、反向与按值查找

```cpp
QMultiMapIterator<int, QString> it(events);

// 正向：构造后已在 front
while (it.hasNext()) {
    const auto item = it.next();
    qDebug() << item.key() << item.value();
}

// 反向：先移动到 back
it.toBack();
while (it.hasPrevious()) {
    const auto item = it.previous();
    qDebug() << item.key() << item.value();
}
```

`Item` 是 `QMultiMap<Key, T>::const_iterator` 的别名。因此 `next()`、`previous()`、`peekNext()`、`peekPrevious()` 的返回值都可以使用 `.key()`、`.value()` 或 `*item`。

按值搜索从**当前位置**开始，而不是每次从头开始：

```cpp
QMultiMapIterator<int, QString> it(events);
while (it.findNext("render")) {
    // 成功后游标位于匹配项之后，key()/value() 指向该匹配项。
    qDebug() << "render at priority" << it.key();
}
```

`findNext(value)` 找不到时返回 `false`，并把游标放到 `back`；`findPrevious(value)` 找不到时返回 `false`，并把游标放到 `front`。失败后没有“最近跨越的有效项”，因此不要再调用 `key()` 或 `value()`。

## `key()` / `value()` 何时有效

`key()` 与 `value()` 不是“游标当前位置”的值，而是**最近一次由移动或搜索函数跨越的条目**：

| 前一步操作 | 此时 `key()` / `value()` 的含义 |
| --- | --- |
| `next()` | 返回刚刚越过的下一条记录。 |
| `previous()` | 返回刚刚越过的上一条记录。 |
| `findNext()` 成功 | 返回找到的匹配记录。 |
| `findPrevious()` 成功 | 返回找到的匹配记录。 |
| 构造、`toFront()`、`toBack()` | 无效。 |
| `findNext()` / `findPrevious()` 失败 | 无效。 |
| 仅调用 `peekNext()` / `peekPrevious()` | 仍是上一次有效跨越项，或仍无效。 |

```cpp
QMultiMapIterator<int, QString> it(events);

if (it.hasNext()) {
    it.next();
    qDebug() << it.key() << it.value();
}

it.toBack();
// it.key() / it.value() 现在无效，不能访问。
```

返回类型是 `const Key &` 和 `const T &`。不要把这些引用保存到迭代器重置、析构或可能改变底层快照寿命之后。

## 快照语义：修改原 map 后会怎样

构造函数和 `operator=(map)` 都会按值保存一个 `QMultiMap` 副本。由于 `QMultiMap` 隐式共享，这通常只增加引用计数；当外部 map 随后被修改时，它会分离数据，迭代器继续遍历它构造时看到的原始内容。

```cpp
QMultiMap<int, QString> map;
map.insert(1, "before");

QMultiMapIterator<int, QString> it(map);
map.insert(2, "after");

// it 仍只会看到 (1, "before")。
```

这并不表示它是跨线程同步工具。它只是利用 copy-on-write 得到稳定快照：多个线程对相同数据只读可以安全共享；涉及同一 `QMultiMap` 对象的并发写入仍需要调用方同步。若需要遍历时直接修改 map，改用 `QMutableMultiMapIterator`，或采用 STL 迭代器配合 `erase()`。

## 与 STL 风格迭代器如何选

| 需求 | 推荐 |
| --- | --- |
| 新代码的单向/双向遍历 | `QMultiMap::const_iterator`、`cbegin()` / `cend()`。 |
| 传给 STL 算法 | `const_iterator` 或 `key_iterator`。 |
| 遍历中修改/删除 map | `QMutableMultiMapIterator`，或 STL `iterator` + `erase()`。 |
| 需要“首前/尾后”游标、连续 `findNext` / `findPrevious` 状态 | `QMultiMapIterator`。 |
| 想让迭代结果不受原 map 后续写入影响 | `QMultiMapIterator` 的隐式共享快照语义。 |

不要在性能敏感的新代码中仅因习惯而选择 Java 风格迭代器。Qt 文档明确指出 STL 风格迭代器更高效，且更自然地适配范围 for 和泛型算法。

## 常见错误

### 构造后直接调用 `key()` 或 `value()`

构造完成时在 `front`，尚未跨越任何记录。先调用成功的 `next()`、`previous()`、`findNext()` 或 `findPrevious()`。

### 忘记在反向遍历前调用 `toBack()`

构造后在 `front`，`hasPrevious()` 为 `false`。反向遍历应从 `toBack()` 开始。

### 未检查 `hasNext()` / `hasPrevious()`

在 `back` 上调用 `next()`，或在 `front` 上调用 `previous()`，都会导致未定义行为。循环条件应由相应的 `has...()` 方法控制。

### 误以为 `findNext()` 始终从头搜索

它从当前游标向后搜索；连续调用可找到后续匹配项。想重新扫描全部记录先调用 `toFront()`。

### 用它修改 map

这是 const iterator，返回项和 `key()` / `value()` 都只读。需要修改使用 `QMutableMultiMapIterator` 或 STL 可写迭代器。

### 以为它会看到后续插入

它持有构造/赋值时的隐式共享快照。外部 map 修改后，迭代器会继续读取旧版本，忽略新版本。

## API 速查表

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `Item` | 条目返回类型。 | 是 `QMultiMap<Key, T>::const_iterator`；可用 `.key()`、`.value()`。 |
| `QMultiMapIterator(const QMultiMap &map)` | 为 map 创建只读快照迭代器。 | 初始位于 `front`；后续 map 写入不会出现在当前迭代中。 |
| `operator=(const QMultiMap &map)` | 改为遍历另一个 map。 | 重新保存快照并重置到 `front`；之前的当前项失效。 |
| `toFront()` | 移到第一项之前。 | 之后 `hasPrevious()` 为假；`key()` / `value()` 无效。 |
| `toBack()` | 移到最后一项之后。 | 之后 `hasNext()` 为假；`key()` / `value()` 无效。 |
| `hasNext() const` | 判断前方是否有项。 | 为真后才可安全调用 `next()` 或 `peekNext()`。 |
| `hasPrevious() const` | 判断后方是否有项。 | 为真后才可安全调用 `previous()` 或 `peekPrevious()`。 |
| `Item next()` | 返回下一项并向前移动。 | 在 `back` 调用未定义；成功后 `key()` / `value()` 对应返回项。 |
| `Item previous()` | 返回上一项并向后移动。 | 在 `front` 调用未定义；成功后 `key()` / `value()` 对应返回项。 |
| `Item peekNext() const` | 查看下一项但不移动。 | 头文件公开的接口；在 `back` 调用未定义，不更新 `key()` / `value()` 当前项。 |
| `Item peekPrevious() const` | 查看上一项但不移动。 | 在 `front` 调用未定义，不更新 `key()` / `value()` 当前项。 |
| `bool findNext(const T &value)` | 从当前位置向后找值。 | 成功后在匹配项之后且可读 `key()` / `value()`；失败后位于 `back`。 |
| `bool findPrevious(const T &value)` | 从当前位置向前找值。 | 成功后在匹配项之前且可读 `key()` / `value()`；失败后位于 `front`。 |
| `const Key &key() const` | 取得最后跨越项的键。 | 只有成功移动/搜索后有效；返回内部 const 引用。 |
| `const T &value() const` | 取得最后跨越项的值。 | 只有成功移动/搜索后有效；返回内部 const 引用。 |

## 一句话总结

`QMultiMapIterator` 是带快照语义的 Java 风格只读游标：它位于条目之间，用 `next()` / `previous()` 跨越记录后再读 `key()` / `value()`；新代码通常优先 STL 迭代器，只有需要这种状态机时再选它。
