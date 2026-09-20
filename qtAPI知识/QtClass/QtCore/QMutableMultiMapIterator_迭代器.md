# QMutableMultiMapIterator：逐条处理 QMultiMap 的重复键记录

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QMutableMultiMapIterator>`  
> 模块：`Qt6::Core`  
> 模板：`template <typename Key, typename T>`

## 它解决什么问题

`QMutableMultiMapIterator<Key, T>` 是 `QMultiMap<Key, T>` 的 Java 风格可写迭代器。`QMultiMap` 与 `QMap` 的关键区别是一个键可关联多个值；此迭代器让你在遍历中对某一条具体的 `(key, value)` 记录删除或改值，而不是误操作该键下的整组记录。

它适合：

- 从“标签到对象”的多值索引中清除某个失效对象；
- 遍历用户到权限的映射，删除单项授权；
- 扫描同一时间点的多条事件，修正个别事件载荷；
- 逆序检查某键下最近插入的关联值。

新代码一般优先选 `QMultiMap::iterator`。`QMutableMultiMapIterator` 的优势是把“最近跨过的那一条”明确为可删除、可修改的目标，适合条件式清理。

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

## 顺序：键升序，同键条目仍是独立记录

`QMultiMap` 按键升序迭代；对于相同键，较晚插入的值先出现。因此：

- `next()` 从小键到大键移动；
- `toBack()` 后用 `previous()` 从大键到小键移动；
- 同键的每个值都要单独跨过、判断和删除；
- 不要把单次 `remove()` 误解为“删除此键的全部值”。

```cpp
#include <QMultiMap>
#include <QMutableMultiMapIterator>

void removeDisconnected(QMultiMap<QString, QString> &rooms,
                        const QString &connectionId)
{
    QMutableMultiMapIterator<QString, QString> it(rooms);

    while (it.hasNext()) {
        it.next();
        if (it.value() == connectionId)
            it.remove(); // 只删除当前 (room, connectionId)
    }
}
```

若调用 `rooms.remove(room)`，则会删除该键的所有值；要保留同房间的其他连接，必须使用上例的 `it.remove()`。

## 游标和“当前条目”

这是 Java 风格双向迭代器，游标位于条目之间：

- 构造后、`toFront()` 后：首项前；
- `next()`：返回下一条，并把游标放在它后面；
- `previous()`：返回上一条，并把游标放在它前面；
- `toBack()` 后：尾项后。

`key()`、`value()`、`setValue()`、`remove()` 都针对最后一次由 `next()`、`previous()`、`findNext()` 或 `findPrevious()` 跨过的记录。`peekNext()`/`peekPrevious()` 仅预览，不能据此建立当前条目。

```cpp
QMutableMultiMapIterator<int, QString> it(index);
it.toBack();

while (it.hasPrevious()) {
    it.previous();
    if (it.key() == wantedKey) {
        it.setValue(it.value().trimmed());
        break;
    }
}
```

按键有序可以帮助定位键区间，但该类本身没有按键搜索函数。已知键范围时，`QMultiMap::lowerBound()`、`upperBound()` 与 STL 风格迭代器通常更直接。

## 按值搜索：方向与失败位置

`findNext(value)` 从当前游标向后查找值相等的记录。成功后游标在匹配项后，失败后在尾后。`findPrevious(value)` 的方向相反：成功后在匹配项前，失败后在首前。

```cpp
QMutableMultiMapIterator<QString, QString> it(headers);
while (it.findNext("deprecated"))
    it.remove();
```

它按值比较，不按键查找，并要求 `T` 支持 `==`。要查某个键的全部值，优先用容器的 `values(key)`、`equal_range(key)` 或键范围迭代，而不是全表 `findNext()`。

## 修改边界、生命周期与线程

可写迭代器持有原容器，不是快照。使用期间：

1. `QMultiMap` 必须保持存活。
2. 同一容器最多一个活动的 mutable iterator。
3. 不可直接调用容器的 `insert()`、`remove()`、`clear()`、赋值等修改操作；这可能使迭代器失效并导致未定义行为。
4. 允许通过该迭代器的 `remove()`、`setValue()` 或非常量 `value()` 修改当前记录。
5. 该类型不提供线程同步；并发读写同一容器必须由调用方加锁。

`Item` 是 `QMultiMap<Key, T>::iterator`。`next()`、`previous()` 和 `peek...()` 返回它；可用 `item.key()` 与 `item.value()` 读取。它只是容器迭代器，不是可跨结构修改保存的稳定句柄。

键不能原地修改。若要把记录移至另一键，先记录值，结束迭代后删除旧关联并插入新关联；这样也避免在迭代中改变排序结构。

## 常见错误

### 用 `remove(key)` 代替迭代器的 `remove()`

前者按键批量删除，后者只删除最近跨过的一条记录。多值映射中这两者的业务影响完全不同。

### 忽略同键值的遍历顺序

键有序并不等于同键值按字典序或数值排序。需要该键下按值排序时，取出值后单独排序。

### 在边界调用移动或预览函数

尾后调用 `next()`/`peekNext()`，首前调用 `previous()`/`peekPrevious()`，均为未定义行为。必须以 `hasNext()` 或 `hasPrevious()` 守卫。

## API 速查表

| API | 作用 | 语义与边界 |
| --- | --- | --- |
| `QMutableMultiMapIterator(QMultiMap<Key, T> &map)` | 绑定多值映射 | 初始在首项前；遍历按键升序，键可重复。 |
| `operator=(QMultiMap<Key, T> &map)` | 改绑容器 | 重置到新容器首前；不再操作旧容器。 |
| `toFront()` | 移到首项前 | 重新开始正向扫描。 |
| `toBack()` | 移到尾项后 | 用于反向扫描。 |
| `hasNext() const` | 判断是否有下一条 | 为真才调用 `next()` 或 `peekNext()`。 |
| `hasPrevious() const` | 判断是否有上一条 | 为真才调用 `previous()` 或 `peekPrevious()`。 |
| `next()` | 取得下一条并前进 | 返回 `Item`（`QMultiMap::iterator`）；尾后调用未定义。 |
| `previous()` | 取得上一条并后退 | 返回 `Item`；首前调用未定义。 |
| `peekNext() const` | 预览下一条 | 不移动游标，不设置当前条目；尾后调用未定义。 |
| `peekPrevious() const` | 预览上一条 | 不移动游标，不设置当前条目；首前调用未定义。 |
| `findNext(const T &value)` | 向后按值搜索 | 成功后在匹配项后，失败后在尾后；不是按键查找。 |
| `findPrevious(const T &value)` | 向前按值搜索 | 成功后在匹配项前，失败后在首前。 |
| `key() const` | 取得当前记录的键 | 返回 `const Key &`；只有最近跨过有效条目后可用。 |
| `value() const` | 只读当前记录的值 | 返回 `const T &`；删除条目后相关引用失效。 |
| `value()` | 读写当前记录的值 | 返回 `T &`；可更新单条关联值。 |
| `setValue(const T &value)` | 替换当前记录的值 | 不影响键，也不删除同键其他条目。 |
| `remove()` | 删除当前记录 | 仅删除最近跨过的一个 `(key, value)` 对。 |

## 选择建议

| 需求 | 建议 |
| --- | --- |
| 遍历中删除或改一个具体重复键条目 | `QMutableMultiMapIterator` |
| 只读 Java 风格遍历 | `QMultiMapIterator` |
| 以键范围高效处理 | `lowerBound()` / `upperBound()` 加 STL 迭代器 |
| 对某键的全部值做批量操作 | `values(key)`、`equal_range(key)` 或容器键 API |

一句话记忆：`QMutableMultiMapIterator` 的删除粒度是一条关联记录，不是一整个键桶；同键的其他值会保留。
