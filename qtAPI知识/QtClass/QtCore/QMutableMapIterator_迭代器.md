# QMutableMapIterator：按有序键双向修改 QMap 条目

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QMutableMapIterator>`  
> 模块：`Qt6::Core`  
> 模板：`template <typename Key, typename T>`

## 它解决什么问题

`QMutableMapIterator<Key, T>` 是 `QMap<Key, T>` 的 Java 风格可写迭代器。它适合在按键排序的映射中双向扫描，并对最近访问的一条 `(key, value)` 记录删除或更新值。

`QMap` 的键唯一且按升序排列，所以它适合按区间、字典序、时间戳或优先级处理记录。可写迭代器的典型用途是：

- 按键顺序清理失效配置；
- 从最新键向旧键回溯，更新最近命中的状态；
- 过滤注册表中无效的对象指针；
- 根据值查找条目后，读取对应键并修正值。

STL 风格的 `QMap::iterator` 更高效，是新代码的首选。`QMutableMapIterator` 的优势是它的游标状态清楚地表达了“前进或后退后，处理刚跨过的条目”。

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

## 顺序和游标：QMap 的两个重要事实

遍历顺序由键决定：

- 正向 `next()` 按键升序；
- 从 `toBack()` 开始的 `previous()` 按键降序；
- 值的大小不影响顺序；
- 键是映射位置的一部分，迭代器只能改值，不能改键。

Java 风格游标位于两条记录之间。构造后处于首项前；`next()` 跨过下一项后停在其后，`previous()` 跨过上一项后停在其前。`key()`、`value()`、`setValue()`、`remove()` 作用于最后一次被跨过的条目。

```cpp
#include <QMap>
#include <QMutableMapIterator>

void purgeOld(QMap<qint64, QString> &messages, qint64 cutoff)
{
    QMutableMapIterator<qint64, QString> it(messages);

    while (it.hasNext()) {
        it.next();
        if (it.key() < cutoff)
            it.remove();
        else
            break; // QMap 按键升序，后面不可能再更旧
    }
}
```

这正是 `QMap` 有序性带来的实际收益；对 `QHash` 不能使用同样的提前退出假设。

## 实际场景：从最新记录向前回溯

```cpp
QString lastNonEmptyValue(QMap<int, QString> &revisions)
{
    QMutableMapIterator<int, QString> it(revisions);
    it.toBack();

    while (it.hasPrevious()) {
        it.previous();
        if (!it.value().isEmpty())
            return it.value();
    }
    return {};
}
```

`previous()` 成功后，`key()` 和 `value()` 表示刚跨过的旧记录。调用它之前必须检查 `hasPrevious()`；在首项前调用会导致未定义行为。

## 搜索、更新与删除

`findNext(value)` 和 `findPrevious(value)` 按**值**做线性搜索，而不是按键查找。若已知键，应使用 `QMap::find()`、`lowerBound()` 或 `upperBound()`，这比遍历整个映射更合适。

```cpp
void disableValue(QMap<QString, bool> &flags, bool oldValue)
{
    QMutableMapIterator<QString, bool> it(flags);

    while (it.findNext(oldValue)) {
        if (it.key().startsWith("legacy."))
            it.setValue(false);
    }
}
```

成功的 `findNext()` 把游标放到匹配项之后；成功的 `findPrevious()` 放到匹配项之前。失败分别落在尾后和首前。`T` 必须能用 `==` 比较。

`remove()` 删除最近跨过的一对键值；由于 `QMap` 键唯一，删除该条目等同于删除该键。`setValue()` 或非常量 `value()` 只能改变值，不能重命名键；要改键，应在迭代器销毁后删除旧键并插入新键。

## 生命周期、失效和并发

此迭代器保存原 `QMap` 的指针，而非快照：

1. 映射必须在迭代器销毁后才可销毁。
2. 同一映射同时只能有一个活动的 mutable iterator。
3. 活跃期间不可绕过迭代器直接 `insert()`、`remove()`、`clear()`、赋值或进行其他结构性修改；这样会使迭代器失效并导致未定义行为。
4. 在迭代器存活期间，允许通过 `remove()`、`setValue()` 或非常量 `value()` 操作当前条目。
5. 该类没有同步能力。跨线程访问同一映射，须由调用方确保互斥。

`peekNext()` 与 `peekPrevious()` 仅查看相邻项，不移动游标，也不更新 `key()`/`value()` 的最近条目。任何返回的 `Item` 或值引用都不应跨越删除、容器结构修改或容器销毁保存。

## 常见错误

### 将 `findNext()` 当作按键查找

它比较的是 `value`。已知键时，直接使用容器的键查找 API；否则复杂度会从对数级或更低退化为线性扫描。

### 在迭代中插入新键

本类没有 `insert()`，这不是遗漏。插入会改变有序树的结构和迭代范围；结束迭代后再插入，或改用能明确处理该需求的 `QMap::iterator` 工作流。

### 指望 `peek...()` 之后可以删除预览项

预览不会形成“最近跨过项”。只有成功的 `next()`、`previous()`、`findNext()`、`findPrevious()` 后，才可调用 `remove()`、`setValue()`、`key()`、`value()`。

## API 速查表

| API | 作用 | 语义与边界 |
| --- | --- | --- |
| `QMutableMapIterator(QMap<Key, T> &map)` | 绑定映射 | 初始位于最小键之前；容器须比迭代器活得久。 |
| `operator=(QMap<Key, T> &map)` | 改绑映射 | 重置到新映射首前；不要再以此对象访问旧映射。 |
| `toFront()` | 移到最小键之前 | 用于重启升序扫描。 |
| `toBack()` | 移到最大键之后 | 用于开始降序扫描。 |
| `hasNext() const` | 判断是否可升序前进 | 为真才可 `next()` / `peekNext()`。 |
| `hasPrevious() const` | 判断是否可降序后退 | 为真才可 `previous()` / `peekPrevious()`。 |
| `next()` | 取得下一条并前进 | 返回 `Item`（`QMap::iterator`）；尾后调用未定义。 |
| `previous()` | 取得上一条并后退 | 返回 `Item`；首前调用未定义。 |
| `peekNext() const` | 查看下一条 | 不移动游标且不改变最近项；尾后调用未定义。 |
| `peekPrevious() const` | 查看上一条 | 不移动游标且不改变最近项；首前调用未定义。 |
| `findNext(const T &value)` | 向后按值查找 | 成功后在匹配项后；失败后在尾后；需要 `T::operator==`。 |
| `findPrevious(const T &value)` | 向前按值查找 | 成功后在匹配项前；失败后在首前。 |
| `key() const` | 取最近跨过项的键 | 返回 `const Key &`，不可改键；只有有效最近项时可用。 |
| `value() const` | 只读最近跨过项的值 | 返回 `const T &`；删除当前项后引用失效。 |
| `value()` | 读写最近跨过项的值 | 返回 `T &`；适用于原地更新当前值。 |
| `setValue(const T &value)` | 替换当前条目的值 | 不改变键和键序；只在存在最近项时调用。 |
| `remove()` | 删除当前条目 | 删除最近跨过的唯一键值对；之后不再使用旧引用或 `Item`。 |

## 选择建议

| 需求 | 建议 |
| --- | --- |
| 按有序键双向删除或改值 | `QMutableMapIterator` |
| 只读 Java 风格遍历 | `QMapIterator` |
| 新代码、算法或复杂范围操作 | `QMap::iterator` |
| 已知键并希望高效定位 | `QMap::find()`、`lowerBound()`、`upperBound()` |

一句话记忆：`QMutableMapIterator` 按键的自然顺序移动，能改值和删当前键，但不能在活跃遍历中插入或改键。
