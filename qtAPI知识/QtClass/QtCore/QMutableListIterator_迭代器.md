# QMutableListIterator：在 QList 中双向扫描、删除、改值和插入

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QMutableListIterator>`  
> 模块：`Qt6::Core`  
> 模板：`template <typename T>`

## 它解决什么问题

`QMutableListIterator<T>` 是 `QList<T>` 的 Java 风格可写迭代器，也可用于以 `QList` 为基础的 `QQueue<T>` 与 `QStack<T>`。它把“位于元素之间的游标”与删除、替换、插入操作放在同一个对象中，适合需要一边扫描一边重写列表的旧式 Qt 控制流。

常见场景：

- 清理待处理队列中的取消任务；
- 从配置列表中删除无效项，并把旧格式值规范化；
- 按逆序查找最近一次出现的元素；
- 在当前游标位置插入补偿项或分隔项。

新代码通常优先用 `QList::iterator`、索引或范围 `for`：STL 风格迭代器更高效，而列表又天然支持按位置操作。需要清晰表达“扫描后删除当前项”或维护既有 Java 风格代码时，`QMutableListIterator` 仍很合适。

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

## 心智模型：游标与最近跨过项

Java 风格迭代器位于元素之间，而不是直接指向元素：

- 构造后和 `toFront()` 后，在第一项之前；
- `next()` 返回右侧元素，并跨到它之后；
- `previous()` 返回左侧元素，并退到它之前；
- `toBack()` 后在最后一项之后；
- `value()`、`setValue()`、`remove()` 操作最后一次由 `next()`、`previous()`、`findNext()` 或 `findPrevious()` 跨过的元素。

```cpp
#include <QList>
#include <QMutableListIterator>

void normalize(QList<int> &values)
{
    QMutableListIterator<int> it(values);

    while (it.hasNext()) {
        const int value = it.next();
        if (value == 0)
            it.remove();
        else if (value < 0)
            it.setValue(-value);
    }
}
```

删除后可继续使用这个迭代器前进。不要在删除后继续持有此前 `next()` 或 `value()` 返回的引用。

## 实际使用：在游标处插入

`insert(value)` 在当前游标位置插入，即“下一次 `next()` 原本会返回的元素之前”。调用后游标位于新元素之后，因此不会在下一次前进时再次访问刚插入的元素。

```cpp
void insertSeparators(QList<QString> &parts)
{
    QMutableListIterator<QString> it(parts);

    while (it.hasNext()) {
        const QString part = it.next();
        if (part == ";")
            it.insert("\n");
    }
}
```

这比通过索引插入时手动维护偏移量更直观。它只适合局部、顺序性的改写；若需要根据全局规则重排或大量随机插入，先构造新的 `QList` 往往更容易验证。

## 双向搜索与方向的影响

`findNext(value)` 从当前位置向后找；成功后游标在匹配项之后，失败后游标在尾后。`findPrevious(value)` 则向前找；成功后游标在匹配项之前，失败后游标在首前。

```cpp
QMutableListIterator<QString> it(history);
it.toBack();

if (it.findPrevious("open")) {
    // value() 是刚匹配到的 "open"；
    // 下一次 previous() 会继续向更早的记录移动。
    it.setValue("open-document");
}
```

反向遍历必须先 `toBack()` 并用 `hasPrevious()` 防护。首前调用 `previous()` 或 `peekPrevious()`，尾后调用 `next()` 或 `peekNext()`，均是未定义行为。

## 生命周期、失效与线程边界

迭代器直接操作传入的列表，不是数据快照。因此：

1. `QList` 必须比迭代器活得久。
2. 一个列表同时只能有一个活动的 mutable iterator。
3. 迭代器活跃期间，不要直接调用 `list.append()`、`removeAt()`、`clear()`、赋值等容器修改函数；只能经该迭代器的 `remove()`、`setValue()`、`insert()` 或非常量 `value()` 修改。绕过迭代器可能导致未定义行为。
4. 该类不提供跨线程同步。多个线程访问同一列表时，由调用方用锁建立排他关系。

只读遍历可用 `QListIterator`；需要更现代的算法组合或性能，用 `QList::iterator`。需要随机定位时，索引通常比此类迭代器更自然。

## 容易踩到的边界

### `peek...()` 不会设定当前项

`peekNext()` 和 `peekPrevious()` 只预览，不移动游标，也不改变 `value()` 所指的最近跨过项。不能 `peekNext()` 后立刻 `remove()`，期待删除预览到的项。

### `value()` 与方向有关

成功 `next()` 或 `findNext()` 后，`value()` 等价于 `peekPrevious()`；成功 `previous()` 或 `findPrevious()` 后，则等价于 `peekNext()`。这是“最近跨过项”语义的直接结果。

### 引用不是稳定句柄

`next()`、`previous()`、`peek...()` 与 `value()` 都返回容器内元素的引用。插入、删除、容器分离或任何会使相关元素失效的操作之后，不应继续保存这些引用。

## API 速查表

| API | 作用 | 语义与边界 |
| --- | --- | --- |
| `QMutableListIterator(QList<T> &list)` | 绑定列表 | 初始在首项之前；也可传入以 `QList` 为基础的 `QQueue`/`QStack`。 |
| `operator=(QList<T> &list)` | 改绑列表 | 游标重置为首前；不要再用它操作旧列表。 |
| `toFront()` | 移到首前 | 用于重新正向扫描；`hasPrevious()` 随后为 `false`。 |
| `toBack()` | 移到尾后 | 用于开始反向扫描；`hasNext()` 随后为 `false`。 |
| `hasNext() const` | 判断右侧是否有元素 | 为 `true` 才可调用 `next()` 或 `peekNext()`。 |
| `hasPrevious() const` | 判断左侧是否有元素 | 为 `true` 才可调用 `previous()` 或 `peekPrevious()`。 |
| `next()` | 返回下一项并前进 | 返回 `T &`；尾后调用未定义。成功后 `value()` 指向该项。 |
| `previous()` | 返回上一项并后退 | 返回 `T &`；首前调用未定义。成功后 `value()` 指向该项。 |
| `peekNext() const` | 预览下一项 | 不移动游标；尾后调用未定义，也不会改变当前项。 |
| `peekPrevious() const` | 预览上一项 | 不移动游标；首前调用未定义，也不会改变当前项。 |
| `findNext(const T &value)` | 向后找相等元素 | 要求 `T` 可比较 `==`；成功后在匹配项后，失败后在尾后。 |
| `findPrevious(const T &value)` | 向前找相等元素 | 成功后在匹配项前，失败后在首前。 |
| `value() const` | 只读最近跨过项 | 返回 `const T &`；只在成功跨过元素后调用。 |
| `value()` | 读写最近跨过项 | 返回 `T &`；可原地改值，不能在无当前项时调用。 |
| `setValue(const T &value) const` | 替换最近跨过项 | 语义明确的整体替换；即使成员函数是 `const`，仍会写入列表。 |
| `remove()` | 删除最近跨过项 | 仅能删除有效当前项；删除后旧引用失效。 |
| `insert(const T &value)` | 在游标位置插入 | 插入在下一项之前；调用后游标移动到插入项之后。 |

## 选择建议

| 需求 | 建议 |
| --- | --- |
| 扫描中删除、替换或在游标处插入 | `QMutableListIterator` |
| 只读 Java 风格双向扫描 | `QListIterator` |
| 新代码或结合标准算法 | `QList::iterator` |
| 基于下标的随机访问、批量编辑 | `QList` 索引或新建结果列表 |

一句话记忆：它维护的是“元素之间”的游标；插入发生在游标处，删除和改值发生在最近一次跨过的元素上。
