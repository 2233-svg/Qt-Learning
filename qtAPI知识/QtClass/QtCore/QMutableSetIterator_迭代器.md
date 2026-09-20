# QMutableSetIterator：遍历 QSet 时筛除元素

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QMutableSetIterator>`  
> 模块：`Qt6::Core`  
> 模板：`template <typename T>`

## 它解决什么问题

`QMutableSetIterator<T>` 是 `QSet<T>` 的 Java 风格可写迭代器，但它的“可写”只体现在**删除当前元素**，并不能原地修改元素值。集合元素同时承担相等性和哈希查找身份；修改它可能破坏容器的哈希结构，所以 API 只返回 `const T &`。

典型使用场景：

- 从权限集合中筛掉已撤销的权限；
- 清理在线 ID 集合中的失效连接；
- 根据白名单、有效期或能力条件过滤去重后的候选项；
- 在保留原集合对象的前提下做一次原地过滤。

新代码通常优先采用 `QSet::iterator` 或先构建新集合。`QMutableSetIterator` 适合“向前扫描，命中即删除”的简单工作流。

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

## 使用方式：前向游标与删除当前元素

构造后，游标位于第一个元素之前。`next()` 返回下一个元素的只读引用并前进；随后 `value()` 与 `remove()` 都对应刚跨过的元素。

```cpp
#include <QMutableSetIterator>
#include <QSet>

void retainAllowed(QSet<QString> &permissions,
                   const QSet<QString> &allowed)
{
    QMutableSetIterator<QString> it(permissions);

    while (it.hasNext()) {
        const QString &permission = it.next();
        if (!allowed.contains(permission))
            it.remove();
    }
}
```

`remove()` 后可继续前进，且只删除该元素。不要在删除后继续使用 `permission`、`value()` 返回的引用，或之前保存的容器迭代器。

## 为什么不能改元素

`QSet` 基于哈希查找。元素的值决定相等性，并通常参与 `qHash()` 计算；若能在原位置改值，元素会留在旧哈希桶中，后续 `contains()`、`remove()` 等操作的结果便不可信。

因此下列需求应使用“删除后再插入”的两阶段做法：

```cpp
QSet<QString> replacement;

{
    QMutableSetIterator<QString> it(names);
    while (it.hasNext()) {
        const QString name = it.next();
        if (name.startsWith("old-")) {
            it.remove();
            replacement.insert(name.mid(4));
        }
    }
}

names.unite(replacement); // mutable iterator 已结束后再插入
```

如果转换可能造成重复，`QSet` 会自动去重。这种做法比试图修改引用更符合集合语义。

## 查找和游标边界

`findNext(value)` 从当前位置向后找相等元素。成功时游标位于匹配元素后，可以读取 `value()` 或调用 `remove()`；失败时游标移到尾后。

```cpp
QMutableSetIterator<int> it(ids);
while (it.findNext(invalidId))
    it.remove(); // QSet 无重复；循环最多删除一次，但写法仍安全
```

`QSet` 没有稳定、可排序的全局遍历顺序。不要以“第一个元素”“处理先后”承载业务语义；需要确定顺序时取出元素后排序，或换用有序容器。

本类是**仅前向** Java 风格迭代器：

- `hasNext()` 为真才可调用 `next()` 或 `peekNext()`；
- `toFront()` 回到首前；
- `toBack()` 移至尾后，但没有 `previous()`、`hasPrevious()` 或 `peekPrevious()`；
- 尾后调用 `next()` 或 `peekNext()` 是未定义行为。

## 生命周期、迭代器失效与线程

`QMutableSetIterator` 保存原集合的引用关系而非快照，使用时遵守以下规则：

1. `QSet` 的生命周期必须覆盖迭代器。
2. 同一集合同时只能有一个活动的 mutable iterator。
3. 迭代器活跃期间不可直接 `insert()`、`remove()`、`clear()`、赋值或进行其他容器修改；只能由该迭代器调用 `remove()`。直接修改可能使迭代器失效，行为未定义。
4. `QSet` 和本迭代器不会自行同步并发访问；跨线程读写须由调用方加锁。

仅仅读取时使用 `QSetIterator` 或 `QSet::const_iterator`。需要在遍历过程中大量插入、合并或执行标准算法时，使用 STL 风格迭代器或构造一个新集合更合适。

## 常见误区

### “mutable” 意味着可以改 `T`

不可以。`next()` 和 `value()` 都返回 `const T &`；`mutable` 指允许删除当前元素。

### 用 `peekNext()` 后调用 `remove()`

`peekNext()` 不移动游标、不设置最近项。必须先成功 `next()` 或 `findNext()`，才能删除。

### 遍历顺序被当成稳定顺序

`QSet` 是哈希集合，顺序不保证稳定。日志展示、序列化、测试断言需要排序时，应显式排序。

## API 速查表

| API | 作用 | 语义与边界 |
| --- | --- | --- |
| `QMutableSetIterator(QSet<T> &set)` | 绑定集合 | 初始位于首元素前；集合必须持续存活。 |
| `operator=(QSet<T> &set)` | 改绑集合 | 重置到新集合首前；之后不再操作旧集合。 |
| `toFront()` | 移到首前 | 重新开始前向扫描。 |
| `toBack()` | 移到尾后 | 停止于末尾；本类没有反向移动 API。 |
| `hasNext() const` | 判断是否存在下一元素 | 为真时才可调用 `next()` 或 `peekNext()`。 |
| `next()` | 返回下一元素并前进 | 返回 `const T &`；尾后调用未定义。成功后当前元素可被 `remove()`。 |
| `peekNext() const` | 预览下一元素 | 不移动游标也不设置当前元素；尾后调用未定义。 |
| `findNext(const T &value)` | 向后搜索相等元素 | 要求 `T` 可 `==` 比较；成功后在匹配元素后，失败后在尾后。 |
| `value() const` | 读取最近跨过元素 | 返回 `const T &`；只在成功 `next()` 或 `findNext()` 后调用。 |
| `remove()` | 删除最近跨过元素 | 唯一的原地修改操作；删除后旧引用失效。 |

## 选择建议

| 需求 | 建议 |
| --- | --- |
| 遍历中按条件删集合元素 | `QMutableSetIterator` |
| 只读 Java 风格遍历 | `QSetIterator` |
| 新代码和标准算法 | `QSet::iterator` / `const_iterator` |
| 要把一个元素变成另一个值 | 删除旧元素，迭代器结束后插入新元素 |
| 需要确定处理顺序 | 排序后的值列表或有序容器 |

一句话记忆：`QMutableSetIterator` 能删不能改；集合元素的哈希身份不可在容器内部原地变化。
