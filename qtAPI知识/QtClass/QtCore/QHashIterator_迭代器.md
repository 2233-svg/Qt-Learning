# Qt QHashIterator 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QHashIterator>`  
> 所属模块：`Qt6::Core`  
> 类型性质：QHash/QMultiHash 的 Java 风格只读迭代器  
> 相关类型：`QHash`、`QMultiHash`、`QMutableHashIterator`、`QHash::const_iterator`

## 1. 它解决什么问题

`QHashIterator<Key, T>` 让已有 Qt Java 风格迭代器代码可以遍历 `QHash` 或 `QMultiHash`。它提供：

- `hasNext()` / `next()` 的顺序遍历；
- `key()` / `value()` 读取最近一次跳过的元素；
- `peekNext()` 查看下一个元素但不移动；
- `findNext()` 在后续 value 中查找匹配项；
- `toFront()` / `toBack()` 重置位置。

它是只读迭代器。需要在遍历期间删除或修改 value 时使用 `QMutableHashIterator`，或者使用 QHash 的 STL 风格可变迭代器。

## 2. 实际使用场景

### 2.1 兼容旧式 Qt 遍历代码

```cpp
QHash<int, QWidget *> widgets;
QHashIterator<int, QWidget *> iterator(widgets);

while (iterator.hasNext()) {
    iterator.next();
    qDebug() << iterator.key() << iterator.value();
}
```

调用 `next()` 后，`key()` 和 `value()` 才代表刚刚跳过的元素。

### 2.2 查找所有相同 value

```cpp
QHashIterator<QString, int> iterator(hash);
while (iterator.findNext(42))
    qDebug() << iterator.key();
```

找到后，迭代器的当前位置已经越过匹配元素，`key()` / `value()` 可读取该元素。

### 2.3 遍历一个稳定快照

迭代器内部保存传入 hash 的共享副本。如果原始 hash 后续被修改并发生 detach，迭代器仍遍历构造时的原始内容。这个特性对“边准备下一份容器边遍历当前副本”的旧式代码有用，但也可能让调用者误以为迭代器会看到外部修改。

## 3. Java 风格位置语义

位置位于元素之间：

```text
front | item[0] | item[1] | ... | item[n - 1] | back
```

- 构造后位于 front；
- `next()` 返回右侧元素，再向 back 移动；
- `toBack()` 把位置放到最后一个元素之后；
- `peekNext()` 不移动；
- `key()` / `value()` 读取上一次 `next()` 或 `findNext()` 找到的元素。

QHashIterator 是正向迭代器，Qt 6.11 的公开接口没有 `previous()` 和 `hasPrevious()`。需要双向或随机访问时，使用 QHash 的 STL 风格迭代器，但哈希容器本身仍然不提供按 key 排序的顺序。

## 4. QHash 的顺序和修改边界

### 4.1 遍历顺序不稳定

QHash 使用哈希桶，元素顺序是任意的，不能依赖插入顺序、字典序或不同运行之间的顺序。salted hash 还会让不同进程的桶顺序变化。

需要按 key 排序时：

- 使用 `QMap`；
- 或先提取 key，再显式排序；
- 不要通过固定 `QHashSeed` 把它当成有序容器。

### 4.2 迭代器是只读且持有容器副本

`QHashIterator` 不能修改容器结构，也不能调用 `remove()`。构造时会保存一个 QHash 值副本，依靠隐式共享避免立即复制数据。

如果原 hash 继续修改，发生 copy-on-write detach 后，iterator 看到的仍是旧副本。对于指针 value，容器副本只复制指针，不复制指针指向的对象。

### 4.3 越过边界是未定义结果

在 `hasNext()` 为 `false` 时调用 `next()` 或 `peekNext()`，会产生未定义结果。`key()` 和 `value()` 也必须在已经成功调用 `next()` 或 `findNext()` 且当前位置有有效项后读取。

## 5. 逐项 API 说明

### 成员类型

#### `QHashIterator<Key, T>::Item`

`Item` 是 `QHash<Key, T>::const_iterator` 的别名。`next()` 和 `peekNext()` 返回它，调用者可以通过该迭代器读取 key/value，但不能修改 value。

### 构造和重绑定

#### `QHashIterator::QHashIterator(const QHash<Key, T> &hash)`

以 `hash` 的当前内容创建只读迭代器，位置设为 front。构造的是共享容器副本，不启动额外工作，也不会修改原 hash。

虽然签名写的是 `QHash`，该 Java 风格迭代器也用于 `QMultiHash`。

#### `QHashIterator<Key, T> &QHashIterator::operator=(const QHash<Key, T> &hash)`

让迭代器改为遍历另一个 hash，并把位置重置到 front。原来绑定的 hash 内容不再作为当前遍历目标。

### 位置和读取

#### `bool QHashIterator::hasNext() const`

返回当前位置后是否还有元素。为 `false` 时不能调用 `next()` 或 `peekNext()`。

#### `QHashIterator<Key, T>::Item QHashIterator::next()`

返回下一个元素的 const iterator，并向后移动一格。调用成功后，`key()` 和 `value()` 返回该元素的 key/value。

#### `QHashIterator<Key, T>::Item QHashIterator::peekNext() const`

返回下一个元素的 const iterator，但不改变位置。调用前应确认 `hasNext()`。

#### `const Key &QHashIterator::key() const`

返回最近一次由 `next()` 或 `findNext()` 跳过的元素的 key。没有有效的“最近元素”时读取会触发断言或产生无效结果。

#### `const T &QHashIterator::value() const`

返回最近一次由 `next()` 或 `findNext()` 跳过的元素的 value。返回只读引用，且引用的有效期受 iterator 和其内部 hash 副本生命周期约束。

#### `void QHashIterator::toFront()`

把位置移动到第一个元素之前，并清除当前遍历位置。

#### `void QHashIterator::toBack()`

把位置移动到最后一个元素之后。调用后 `hasNext()` 为 `false`，可以再用 `toFront()` 重新开始。

### 搜索

#### `bool QHashIterator::findNext(const T &value)`

从当前位置向前查找等于 `value` 的元素：

- 找到返回 `true`，位置越过匹配元素；
- 找不到返回 `false`，位置移动到 back；
- 成功后 `key()` / `value()` 表示匹配元素。

`QHash` 允许多个 key 对应相同 value，因此可以在循环中找到多个匹配项。`QHash` 本身不保证这些匹配项的顺序。

## API 速查表
| API | 作用 | 关键边界 |
|---|---|---|
| `QHashIterator(hash)` | 创建只读迭代器 | 初始在 front；保存共享副本 |
| `operator=(hash)` | 重绑定 hash 并回到 front | 不再遍历旧目标 |
| `hasNext()` | 查询后方是否有元素 | false 时不能读取 next |
| `next()` | 返回下一个 const iterator 并前进 | 成功后 key/value 才有效 |
| `peekNext()` | 查看下一个元素不移动 | 不能在 back 调用 |
| `key()` | 读取最近跳过元素的 key | 需要先成功 next/findNext |
| `value()` | 读取最近跳过元素的 value | 只读引用 |
| `findNext(value)` | 向前找匹配 value | 找不到会到 back |
| `toFront()` | 回到第一个元素之前 | 清除当前项位置 |
| `toBack()` | 移到最后一个元素之后 | `hasNext()` 为 false |

## 7. 和相邻迭代器如何选择

- 只读且项目使用 Qt Java 风格：`QHashIterator`。
- 需要删除或修改：`QMutableHashIterator`。
- 需要 range-for、STL 算法或 key/value 结构化绑定：QHash 的 STL 风格迭代器或 `asKeyValueRange()`。
- 需要排序：`QMap`，或显式排序 key 列表。

## 8. 排查顺序

1. 遍历顺序变化：确认没有依赖 QHash 顺序，且没有把它当成 QMap。
2. `key()` / `value()` 无效：确认前面成功调用了 `next()` 或 `findNext()`。
3. `next()` 崩溃：检查是否遗漏了 `hasNext()`。
4. 外部修改后 iterator 看不到新数据：这是它保存原始 hash 副本的预期行为。
5. 需要修改容器却仍使用此类：改用 `QMutableHashIterator` 或 STL 风格可变迭代器。
