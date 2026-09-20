# QContiguousCache 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QContiguousCache>`  
> 所属模块：`Qt6::Core`  
> 模板：`template <typename T> class QContiguousCache`

## 它解决什么问题

`QContiguousCache<T>` 是一个固定容量的、带**逻辑连续索引**的滑动窗口缓存。它特别适合 UI 中按邻近行访问的远程或昂贵数据：用户在列表中缓慢滚动时，已经加载的行围绕当前区域连续保存；继续向下滚动就从尾部加入新行、从头部淘汰最远的旧行。

它不是通用顺序容器，也不是按 key 和成本淘汰对象的 `QCache`：

- `QContiguousCache` 用连续的整数索引定位元素，关注“第 500 到第 699 行”这一段。
- `QCache` 更适合不连续 key 的对象缓存和成本控制。
- `QVector` 或 `QList` 更适合需要稳定保存全部元素的普通序列。

容量表示最多保存多少个 `T`，而不是多少字节。元素自己在堆上分配的内存，例如 `QString` 的字符数据或 `QSharedPointer` 管理的对象，不包含在这个“容量”概念中。

## 先理解逻辑索引，而不是物理下标

```cpp
QContiguousCache<QString> cache(3);

cache.insert(10, "row 10");
cache.append("row 11");
cache.append("row 12");

Q_ASSERT(cache.firstIndex() == 10);
Q_ASSERT(cache.lastIndex() == 12);

cache.append("row 13");

Q_ASSERT(cache.firstIndex() == 11);
Q_ASSERT(cache.lastIndex() == 13);
Q_ASSERT(cache.at(11) == "row 11");
```

缓存内部会循环复用存储空间，但对调用方暴露的是连续的逻辑范围。容量已满后：

- `append()` 从末尾加入新值，并删除开头最旧的值。
- `prepend()` 从开头加入新值，并删除末尾最旧的值。

因此 `at(0)` 并不表示“第一个仍被缓存的元素”。它表示逻辑索引为 `0` 的元素；当缓存窗口已经滑到 `50` 到 `149` 时，`at(0)` 不可用，正确访问应是 `at(50)` 到 `at(149)`。

## 默认容量为零：看起来能插入，实际不会保存

默认构造的容量是 `0`。在设置正容量前，`append()`、`prepend()` 和 `insert()` 都不会保存项目：

```cpp
QContiguousCache<int> cache;
cache.append(42);

Q_ASSERT(cache.isEmpty());

cache.setCapacity(100);
cache.append(42);
Q_ASSERT(cache.size() == 1);
```

这通常不是 bug，而是忘记配置容量。尤其不要在零容量缓存上使用非常量 `operator[]`；它会尝试插入默认值，而这个 API 本来就不适合拿来做普通数组式访问。

## UI 滚动缓存的典型写法

```cpp
class RecordWindow
{
public:
    explicit RecordWindow(qsizetype capacity)
        : cache(capacity)
    {
    }

    QString recordAt(qsizetype row)
    {
        if (cache.containsIndex(row))
            return cache.at(row);

        if (cache.isEmpty()) {
            cache.insert(row, loadRecord(row));
        } else if (row == cache.lastIndex() + 1) {
            cache.append(loadRecord(row));
        } else if (row == cache.firstIndex() - 1) {
            cache.prepend(loadRecord(row));
        } else {
            cache.insert(row, loadRecord(row));
        }

        return cache.at(row);
    }

private:
    QString loadRecord(qsizetype row);
    QContiguousCache<QString> cache;
};
```

最后一个 `insert()` 分支很关键：如果要插入的逻辑索引既不在当前范围内，也不紧邻两端，`QContiguousCache` 会先清空原有窗口，再只保存新值。这样才能维持“无空洞的连续区间”。快速跳转到很远的行时这是合理行为；若你需要同时保留多个相距很远的区间，应选 `QCache`、`QHash` 或专门的页缓存结构。

## 容量、淘汰和收缩规则

`setCapacity()` 可以在运行时调整窗口大小。缩小容量时，缓存只保留**最后** `size` 个项目，也就是逻辑索引较大的那一端；它不是按最近访问时间淘汰。

```cpp
QContiguousCache<int> cache(5);
for (int i = 0; i != 5; ++i)
    cache.append(i);

cache.setCapacity(2);

Q_ASSERT(cache.firstIndex() == 3);
Q_ASSERT(cache.lastIndex() == 4);
```

`clear()` 删除所有元素，但保留当前容量。`available()` 是尚未达到容量前还能加入多少项；`isFull()` 仅表示 `size() == capacity()`，不是“没有可用业务数据”。

## 索引有效性和极端长寿命窗口

正常情况下，逻辑索引位于 `0` 到 `INT_MAX` 范围，`areIndexesValid()` 始终为真。若缓存被当作极长寿命的环形缓冲区，持续 `append()` 可能让末端越过 `INT_MAX`，持续 `prepend()` 可能让开端小于 `0`。此时缓存内容和顺序仍存在，但索引不再可安全使用。

一旦 `areIndexesValid()` 返回 `false`，先调用 `normalizeIndexes()`，再调用下列依赖逻辑索引的 API：

- `containsIndex()`
- `firstIndex()` 和 `lastIndex()`
- `at()` 和两个 `operator[]` 重载

`normalizeIndexes()` 不会更改元素内容或元素顺序，只会把当前逻辑区间重新映射到有效索引范围。这是面向长期运行环形缓存的维护操作；一般列表页面不需要它。

## 值语义、隐式共享与引用失效

`QContiguousCache` 是隐式共享且可重入的值类型。拷贝构造和拷贝赋值通常是常数时间；任意一个共享副本被修改时会发生 copy-on-write，复制成本变为线性。返回缓存值对象通常很便宜，但在热路径中修改一个共享副本可能不便宜。

```cpp
QContiguousCache<QString> original(100);
original.append("a");

QContiguousCache<QString> snapshot = original;
snapshot.append("b"); // 此处可能分离并复制缓存数据
```

`detach()` 可主动强制分离共享数据，`isDetached()` 可检查是否独占。大多数业务代码不需要手动调用它们；只有需要把一次复制成本安排到特定时机的性能敏感代码才考虑使用。

任何会改变缓存、触发分离或重设容量的操作，都可能使从 `at()`、`first()`、`last()` 或 `operator[]` 得到的引用失效。不要跨 `append()`、`prepend()`、`insert()`、`clear()`、`setCapacity()` 或其他线程修改保存这些引用。`可重入`不等于同一个缓存实例可被多个线程无锁读写。

## 读取与写入 API 的坑

- `at(i)` 只读且要求 `i` 在当前逻辑范围内；越界是未定义行为。
- 常量 `operator[](i)` 等价于 `at(i)`。
- 非常量 `operator[](i)` 若位置不存在，会插入一个默认构造的 `T`；若位置离当前区间很远，可能因 `insert()` 规则清空整个窗口。它还会触发隐式共享分离。
- 即使对象本身不是 `const`，只读时也优先使用 `at()`，不要为了“写起来短”调用非常量 `operator[]`。
- `first()`、`last()`、`removeFirst()`、`removeLast()`、`takeFirst()`、`takeLast()` 都假定缓存非空。先用 `isEmpty()` 判断。
- 不使用被取出的返回值时，`removeFirst()`、`removeLast()` 比 `takeFirst()`、`takeLast()` 更合适。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QContiguousCache(qsizetype capacity = 0)` | 创建指定容量的连续窗口缓存。 | 默认容量为 `0`，插入类操作不会保存元素；先设正容量。 |
| 构造 | `QContiguousCache(const QContiguousCache &)` | 拷贝另一个缓存。 | 隐式共享，通常是常数时间；后续写入可能触发线性复制。 |
| 析构 | `~QContiguousCache()` | 销毁缓存及它持有的元素。 | 不管理 `T` 间接指向资源的额外所有权语义。 |
| 赋值 | `operator=(const QContiguousCache &)` | 让当前缓存共享另一个缓存的值。 | 修改任一方会分离；旧引用不要跨赋值保留。 |
| 赋值 | `operator=(QContiguousCache &&)` | 移动赋值缓存数据。 | 被移动对象仅保证可析构或重新赋值。 |
| 交换 | `swap(QContiguousCache &) noexcept` | 快速交换两个缓存的全部状态。 | 同时交换容量、内容与逻辑索引范围。 |
| 共享控制 | `detach()` | 主动让当前缓存拥有独立数据副本。 | 一般无需调用；只用于控制 copy-on-write 发生时机。 |
| 共享控制 | `isDetached() const` | 判断当前缓存是否未与其他缓存共享数据。 | 仅反映当前共享状态，不提供并发同步保证。 |
| 容量 | `capacity() const` | 返回最多可保存的元素数量。 | 不是字节数；元素自身额外分配的内存不计入此值。 |
| 容量 | `setCapacity(qsizetype)` | 修改缓存容量。 | 缩小时仅保留最后的元素；会使现有引用失效。 |
| 容量 | `available() const` | 返回填满缓存前还能加入的元素数量。 | 等于 `capacity() - size()`；满后继续插入会淘汰另一端。 |
| 状态 | `size() const` | 返回当前保存的元素数。 | 与 `count()` 完全相同；新代码通常使用 `size()`。 |
| 状态 | `count() const` | 返回当前保存的元素数。 | `size()` 的同义 API，不代表逻辑索引范围长度以外的数据。 |
| 状态 | `isEmpty() const` | 判断缓存是否没有元素。 | 调用 `first()`、`last()`、移除或取走 API 前先检查。 |
| 状态 | `isFull() const` | 判断元素数是否已达到容量。 | 满后 `append()` 或 `prepend()` 仍成功，但会淘汰最远端元素。 |
| 状态 | `areIndexesValid() const` | 判断逻辑索引是否仍在可用范围。 | 极端长期 append 或 prepend 后可能为假；此时先 `normalizeIndexes()`。 |
| 索引 | `firstIndex() const` | 返回当前窗口最小的逻辑索引。 | 空缓存时没有可用业务索引；先检查 `isEmpty()`。 |
| 索引 | `lastIndex() const` | 返回当前窗口最大的逻辑索引。 | 空缓存时没有可用业务索引；索引无效时先规范化。 |
| 索引 | `containsIndex(qsizetype) const` | 判断某个逻辑索引是否仍在窗口内。 | 索引失效时不可调用；不要把它当作 `0 <= i < size()` 检查。 |
| 索引 | `normalizeIndexes()` | 重置逻辑索引到有效范围而不改变元素顺序。 | 专用于索引溢出恢复；会改变外部保存的逻辑位置含义。 |
| 读取 | `at(qsizetype) const` | 按逻辑索引只读返回元素引用。 | 索引必须存在且有效；只读访问优先用它，不会触发分离。 |
| 读取 | `first() const` 和 `first()` | 返回窗口首元素的常量或可修改引用。 | 缓存不能为空；可修改重载可能因隐式共享而分离。 |
| 读取 | `last() const` 和 `last()` | 返回窗口末元素的常量或可修改引用。 | 缓存不能为空；可修改重载可能因隐式共享而分离。 |
| 下标 | `operator[](qsizetype) const` | 等价于 `at()` 的只读下标访问。 | 索引必须存在；越界是未定义行为。 |
| 下标 | `operator[](qsizetype)` | 返回可修改元素，不存在时插入默认构造元素。 | 可能分离共享数据，远距离索引可能清空已有窗口；读取时不要用它。 |
| 加入 | `append(const T &)` 和 `append(T &&)` | 在窗口末端加入元素。 | 满时删除开头元素；容量为零时不保存任何元素。 |
| 加入 | `prepend(const T &)` 和 `prepend(T &&)` | 在窗口开端加入元素。 | 满时删除末端元素；长期使用可能让索引低于零。 |
| 加入 | `insert(qsizetype, const T &)` 和 `insert(qsizetype, T &&)` | 在指定逻辑索引写入或插入元素。 | 已存在则替换，相邻则等价 append 或 prepend，远跳会先清空缓存；索引须在 `0` 到 `INT_MAX`。 |
| 删除 | `clear()` | 移除全部元素但保留容量。 | 不会把容量恢复为零；已取得的元素引用失效。 |
| 删除 | `removeFirst()` | 删除首元素。 | 缓存不能为空；不需要元素值时比 `takeFirst()` 更合适。 |
| 删除 | `removeLast()` | 删除末元素。 | 缓存不能为空；不需要元素值时比 `takeLast()` 更合适。 |
| 取走 | `takeFirst()` | 移除并按值返回首元素。 | 缓存不能为空；返回值会发生移动或复制。 |
| 取走 | `takeLast()` | 移除并按值返回末元素。 | 缓存不能为空；返回值会发生移动或复制。 |
| 比较 | `operator==(const QContiguousCache &) const` | 比较两个缓存是否在相同索引保存相同值。 | `T` 必须支持相等比较；相同元素但逻辑索引不同也不相等。 |
| 比较 | `operator!=(const QContiguousCache &) const` | 判断两个缓存是否不相等。 | 语义是 `operator==` 的反面，条件同样包含逻辑索引。 |

## 一句话记忆

`QContiguousCache` 是面向连续行号窗口的固定容量滑动缓存：追加或前插会从另一端淘汰，远距离 `insert()` 会清空旧窗口，访问时始终以 `firstIndex()` 到 `lastIndex()` 的逻辑范围为准。
