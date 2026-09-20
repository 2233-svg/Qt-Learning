# QMutableHashIterator：遍历 QHash 时安全地删条目或改值

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QMutableHashIterator>`  
> 模块：`Qt6::Core`  
> 模板：`template <typename Key, typename T>`

## 它解决什么问题

`QMutableHashIterator<Key, T>` 是 `QHash<Key, T>` 和 `QMultiHash<Key, T>` 的 Java 风格可写迭代器。它的价值不在于“遍历哈希表”，而在于遍历期间对**刚刚访问的条目**执行删除或改值，不必先收集键再做第二轮处理。

典型需求包括：

- 清理缓存表中过期或空闲的对象；
- 从路由表、订阅表中删除失效记录；
- 扫描配置映射，将符合条件的值原地归一化；
- 在 `QMultiHash` 中删除满足条件的一对 `(key, value)`，而不是删除该键下的全部值。

新代码通常优先选择 STL 风格迭代器：它更高效，也更符合 C++ 算法生态。`QMutableHashIterator` 适合已有 Java 风格 Qt 代码，或“前进、检查、删除当前项”这一控制流特别直观的场合。

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

## 使用模型：游标位于条目之间

它不直接“指向当前元素”，而是位于两个条目之间：

- 构造后以及调用 `toFront()` 后，游标在首项之前；
- `next()` 跨过下一项，返回该项，并把“最近跨过的项”设为当前可操作项；
- `key()`、`value()`、`remove()` 和 `setValue()` 都针对最近跨过的项；
- `toBack()` 后游标在尾项之后，`hasNext()` 为 `false`。

因此，先检查 `hasNext()`，再调用 `next()` 是基本范式。哈希容器没有可依赖的全局遍历顺序；任何依赖“第一个条目”“处理顺序稳定”的业务逻辑都应改用排序后的键列表或 `QMap`。

```cpp
#include <QHash>
#include <QMutableHashIterator>

void removeExpired(QHash<QString, int> &expiresAt, int now)
{
    QMutableHashIterator<QString, int> it(expiresAt);

    while (it.hasNext()) {
        it.next();
        if (it.value() <= now)
            it.remove();              // 只删除刚刚跨过的这一项
    }
}
```

`remove()` 会把内部游标调整到可继续前进的位置；上例可连续删除多项。删除后不要再读取此前取得的 `Item`、`key()` 或 `value()` 所代表的旧条目。

## 真实场景：清理多值索引而不误删同键记录

`QMultiHash` 允许同一个键对应多个值。若按值清理，只能删除匹配的那一对，而不应调用按键删除的容器 API，否则可能把同键的其他记录一并去掉。

```cpp
#include <QMultiHash>
#include <QMutableHashIterator>

void removeOfflineSession(QMultiHash<QString, QString> &sessions,
                          const QString &offlineId)
{
    QMutableHashIterator<QString, QString> it(sessions);

    while (it.findNext(offlineId))
        it.remove();
}
```

`findNext(value)` 从当前位置向后搜索；成功时它已经跨过匹配项，因而紧接着可读取 `key()` 或调用 `remove()`。失败时游标被置于尾后，不能据此继续访问当前项。

## 生命周期、修改与线程边界

可写迭代器保存的是原容器的指针，不会像只读 Java 风格迭代器那样复制一份容器快照。这带来几个必须遵守的边界：

1. 被迭代的 `QHash`/`QMultiHash` 必须比迭代器活得久。
2. 迭代器存活期间，不能直接对容器做插入、删除、清空、赋值、rehash 等修改；只能经该迭代器的 `remove()`、`setValue()` 或非常量 `value()` 修改当前项。直接修改会使迭代器失效，行为未定义。
3. 同一个哈希容器同时只能有一个活动的 mutable iterator。不要在外层 `QMutableHashIterator` 存活时再创建另一个。
4. Qt 容器不为这种并发访问提供同步。多个线程读写同一容器时，调用方必须用互斥量等机制建立排他访问；仅仅拿到迭代器不构成线程安全保证。

只读扫描时使用 `QHashIterator`，或更推荐 `QHash::const_iterator` / 范围 `for`。需要复杂插入、算法组合或性能敏感的遍历时，使用 STL 风格 `QHash::iterator`。

## 常见错误

### 在 `next()` 之前调用 `key()` 或 `value()`

构造后还没有“最近跨过的项”。`key()` 与 `value()` 的前置条件不成立；调试构建通常会断言，发布构建也不能依赖结果。先成功调用 `next()` 或 `findNext()`。

### `hasNext()` 为 false 仍调用 `next()` 或 `peekNext()`

这两个函数在尾后调用会产生未定义结果。`peekNext()` 只看下一项，不移动游标，也不会更新 `key()`/`value()` 所对应的最近项。

### 在循环内直接改 `hash`

下面的写法看似自然，但会使迭代器无效：

```cpp
// 错误：迭代器仍活跃时直接修改其容器。
for (QMutableHashIterator<QString, int> it(hash); it.hasNext(); ) {
    it.next();
    if (it.value() == 0)
        hash.remove(it.key());
}
```

应改为 `it.remove()`。若需要插入新条目或重建整个哈希表，先结束并销毁迭代器，再修改容器。

### 误以为 `findNext()` 从头查找

它从当前游标向后查。要重做一次全表搜索，先调用 `toFront()`；要一次删除全部匹配项，则把它放在 `while` 条件里。

## 关键 API 语义

### 构造、重置与前进

```cpp
QMutableHashIterator<Key, T> it(hash);
it.toFront();             // 回到首项之前

while (it.hasNext()) {
    const auto item = it.next();
    // item.key()、item.value() 可读取返回的 QHash::iterator
}
```

`operator=(QHash<Key, T> &hash)` 让已有迭代器改为操作另一个容器，并把游标置于新容器的首项之前。赋值前必须确保旧迭代器不再被用于旧容器；通常重新构造一个局部迭代器更清晰。

`Item` 是容器的非常量迭代器类型，实际为 `QHash<Key, T>::iterator`。`next()` 和 `peekNext()` 返回这个迭代器对象；可用 `.key()` 读取键、`.value()` 读取或修改值。不要把它长期保存，更不能跨越会改变容器结构的操作。

### 改值的两种方式

```cpp
while (it.hasNext()) {
    it.next();
    if (it.value() < 0)
        it.setValue(0);
}
```

也可以通过非常量 `value()` 直接改当前值：

```cpp
it.next();
it.value() += 1;
```

两种方式均只允许在 `next()` 或成功的 `findNext()` 之后使用。键不能通过该迭代器修改：改变键等同于改变哈希位置，应删除旧条目后以新键插入，且插入应在迭代器结束后进行。

## API 速查表

| API | 作用 | 语义与边界 |
| --- | --- | --- |
| `QMutableHashIterator(QHash<Key, T> &hash)` | 绑定可写容器 | 游标初始在首项之前；容器须在迭代器整个生命周期内有效。`QMultiHash` 也可使用此接口。 |
| `operator=(QHash<Key, T> &hash)` | 改绑容器 | 重置到新容器首前；之后不再操作旧容器。 |
| `toFront()` | 回到首前 | 适合重新进行一次前向扫描；会清除“最近项”的可用语义。 |
| `toBack()` | 移到尾后 | 之后 `hasNext()` 为 `false`；不支持反向遍历 API。 |
| `hasNext() const` | 判断是否还有下一项 | 为 `true` 才能调用 `next()` 或 `peekNext()`。 |
| `next()` | 返回下一项并前进 | 返回 `Item`；尾后调用未定义。调用成功后当前项可由 `key()`/`value()`/`remove()` 操作。 |
| `peekNext() const` | 查看下一项但不前进 | 返回 `Item`，不改变游标和最近项；尾后调用未定义。 |
| `findNext(const T &value)` | 向后找下一个值相等的项 | 成功返回 `true` 且当前项变为匹配项；失败返回 `false` 并移动到尾后。比较要求 `T` 可用 `==`。 |
| `key() const` | 取最近跨过项的键 | 只读引用；只可在成功 `next()` 或 `findNext()` 后使用。 |
| `value() const` | 读最近跨过项的值 | 返回 `const T &`；不要在删除当前项后继续保存或使用该引用。 |
| `value()` | 读写最近跨过项的值 | 返回 `T &`，可原地改值；不能借此改键。仅在存在最近项时调用。 |
| `setValue(const T &value)` | 替换最近跨过项的值 | 适合明确表达“整体替换”；只对有效最近项使用。 |
| `remove()` | 删除最近跨过项 | 删除单个 `(key, value)` 条目；在 `QMultiHash` 中不会自动删除同键的其他值。 |

## 选择建议

| 需求 | 更合适的选择 |
| --- | --- |
| 遍历时删除或改当前项，已有 Java 风格代码 | `QMutableHashIterator` |
| 只读遍历，想要 Java 风格接口 | `QHashIterator` |
| 新代码、性能或泛型算法优先 | `QHash::iterator` / `const_iterator` |
| 需要稳定的键排序或范围查找 | `QMap`，而不是 `QHash` |

一句话记忆：`QMutableHashIterator` 的“当前项”来自最后一次成功跨越；容器结构只能由它自己在遍历中删除，不能绕过它直接修改哈希表。
