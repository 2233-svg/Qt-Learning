# QSetIterator：为 QSet 保留只读快照的 Java 风格迭代器

> 适用版本：Qt 6.11.1  
> 所属头文件：`#include <QSetIterator>`  
> 所属模块：Qt Core

`QSetIterator<T>` 是 `QSet<T>` 的只读 Java 风格 iterator。它不像 STL iterator 那样直接“指向元素”，而是概念上位于元素之间：构造后在第一个元素之前，`next()` 返回下一个元素并把位置向后移动。

现代 C++ 代码通常优先使用范围 for 或 `QSet::const_iterator`，因为它们更贴近标准算法且开销更直接。`QSetIterator` 的独特价值在于：它内部保存一份 `QSet` 的隐式共享副本，因此原 set 之后发生 detach 式修改时，iterator 仍按构造时的集合视图继续只读遍历。

## 它解决的问题

例如日志导出正在遍历当前订阅集合，而 UI 同时修改原集合。STL iterator 不应跨这种复制/结构变化继续使用；`QSetIterator` 可以把“导出时看到的集合”固定下来：

```cpp
QSetIterator<QString> it(subscriptions);

subscriptions.insert("new-topic"); // 原 set 修改；it 继续遍历旧快照

while (it.hasNext()) {
    writeLog(it.next());
}
```

这不是深拷贝所有元素的万能线程同步工具。它利用 `QSet` 的隐式共享保存容器数据视图；元素若是指针，iterator 复制的仍是指针值，指向对象的生命周期和线程安全仍由调用方负责。

## 基本遍历和“元素之间”的位置

```cpp
QSetIterator<QString> it(tags);

while (it.hasNext()) {
    const QString &tag = it.next();
    consume(tag);
}
```

状态模型：

```text
构造 / toFront()：第一个元素之前
next()           ：返回后一个元素，并移至其后
toBack()         ：最后一个元素之后
```

所以：

- 调用 `next()` 前必须 `hasNext()`；
- 调用 `peekNext()` 前也必须 `hasNext()`；
- `toFront()` 后可重新从快照开始；
- `toBack()` 后 `hasNext()` 为 false；
- QSet 无序，所谓“第一个”“下一个”只是当前哈希遍历序列中的位置，不表示按值排序。

QSet 的 iterator 在 Qt 6.11.1 中是前向 iterator，因此 `QSetIterator` 没有实际可用的反向 `previous()`、`peekPrevious()` 和 `hasPrevious()` 接口。不要从其他 Java 风格 Qt 容器的经验推断 QSet 可以倒序遍历。

## 查找下一个匹配值

`findNext(value)` 从当前位置向后搜索。找到时，它会把当前位置推进到该元素之后并返回 true：

```cpp
while (it.findNext("critical")) {
    // QSet 去重，因此一个未修改的快照中至多会找到一次
}
```

由于 `QSet` 本身不允许重复值，典型静态快照里不需要“找所有 occurrence”的循环；该模式主要是 Java 风格 iterator 的通用接口。在调用 `findNext()` 之前已经经过的元素不会被重新搜索；要从头查找先 `toFront()`。

`next()`、`peekNext()` 和 `findNext()` 返回或暴露的都是 `const T &`。如果要长期保存值，尤其是 iterator 即将重绑定到另一个 set 时，复制它；如果 `T` 是指针，按业务规则验证对象仍存活。

## 快照、修改与线程边界

构造函数接收 `const QSet<T> &`，但 iterator 内部保存自己的 `QSet<T>` 副本。因为隐式共享，创建成本通常很低；原集合后续修改会使原集合或 iterator 副本 detach，因此 iterator 继续看到创建时的内容而忽略新修改。

这条规则只适用于**修改原 set**。不要依赖它处理：

- 同时跨线程读写同一个元素对象；
- 指针元素指向对象已删除；
- 自定义元素内部可变状态影响 `operator==` 或 `qHash`；
- 多线程中无同步地构造 iterator 与同时写原 set 的竞态。

在跨线程传递前，应先完成容器副本构造并有明确同步；之后把 iterator 当作只读快照使用。要修改集合边遍历，使用 `QMutableSetIterator` 或更推荐的 STL `it = set.erase(it)` 模式。

## 常见错误

1. **期待稳定排序。** QSet 的“下一项”顺序未指定。
2. **在 `hasNext()` 为 false 时调用 `next()` 或 `peekNext()`。** 这是越过有效范围。
3. **以为 iterator 观察原 set 的后续更新。** 它遍历构造时的快照。
4. **以为快照复制会复制指针指向对象。** 只复制指针值。
5. **把它用于边遍历边删除。** 它只读；改用 `QMutableSetIterator` 或 `erase()`。
6. **尝试反向 `previous()`。** QSet 的底层 iterator 不支持反向移动。

## API 速查表

| API | 语义 | 使用时重点 |
| --- | --- | --- |
| `QSetIterator(const QSet<T> &set)` | 创建并定位到 set 快照的前端。 | 之后原 set 的 detach 式修改不会加入本次遍历。 |
| `operator=(const QSet<T> &set)` | 改为遍历另一 set 的快照，并回到前端。 | 先前从 `next()` 得到的引用不应跨重绑定保存。 |
| `hasNext()` | 判断当前位置之后是否还有元素。 | `next()` / `peekNext()` 的必要前置条件。 |
| `next()` | 返回下一元素并前进。 | 返回 `const T &`；不可在尾后调用。 |
| `peekNext()` | 查看下一元素但不前进。 | 不可在尾后调用；返回引用只作短时使用。 |
| `toFront()` | 回到第一个元素之前。 | 用于从快照重新遍历。 |
| `toBack()` | 移到最后元素之后。 | 之后 `hasNext()` 为 false。 |
| `findNext(value)` | 从当前位置向后查找 value。 | 找到后位置在该元素之后；要重查先 `toFront()`。 |

## 一句话总结

`QSetIterator` 是只读、前向、快照式的 QSet 遍历器：它能隔离原集合之后的 detach 修改，却不提供排序、元素修改、反向遍历或指针对象生命周期保证。
