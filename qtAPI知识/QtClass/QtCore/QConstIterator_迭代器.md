# QConstIterator 深入笔记

> 适用版本：Qt 6.0 及以上，本文按 Qt 6.11.1 说明  
> 头文件：`#include <QConstIterator>`  
> 所属模块：`Qt6::Core`  
> 模板：`template <typename Container> struct QConstIterator`

## 它解决什么问题

`QConstIterator` 不是 `QList<T>::const_iterator` 的同义替代品。它服务于 Qt 的**运行时容器反射**：当代码只拿到一个 `QVariant`，事先不知道里面是 `QList<int>`、`QStringList` 还是其他已注册的序列容器时，Qt 用 `QMetaSequence::Iterable` 或 `QMetaAssociation::Iterable` 提供统一的遍历入口，而 `QConstIterator` 是这套入口的只读迭代基础。

可以把它理解成下面这层关系：

```text
QVariant 中保存的未知容器
        ↓
QMetaSequence::Iterable 或 QMetaAssociation::Iterable
        ↓
QConstIterator<...>
        ↓
底层容器的原生 const_iterator
```

对已知类型的日常容器代码，优先使用容器自身的 `constBegin()`、`cend()` 或范围 `for`。只有当容器类型要到运行时才能确定，例如属性编辑器、序列化框架、通用日志查看器、插件参数检查器，才需要这套元类型迭代 API。

## 不要手工构造它

构造函数的签名是：

```cpp
QConstIterator(const QIterable<Container> *iterable, void *iterator)
```

其中的 `void *iterator` 是底层原生迭代器的擦除表示，供 `QIterable` 及其派生包装器内部创建使用。业务代码不应伪造这个指针，也不应直接调用构造函数。

正确入口是从 `QMetaSequence::Iterable` 或 `QMetaAssociation::Iterable` 取得 `begin()`、`end()`、`constBegin()`、`constEnd()`。这些更具体的迭代器类型在 `QConstIterator` 基础上补上了解引用能力：序列迭代通常得到一个 `QVariant` 值，关联迭代还可以读取 key。

## 真实使用场景：遍历 QVariant 里的未知序列

下面是反射式读取的典型样子。此时元素在编译期不是 `int`，而是统一以 `QVariant` 交给调用方。

```cpp
#include <QMetaSequence>
#include <QVariant>
#include <QDebug>

void printUnknownSequence(const QVariant &value)
{
    if (!value.canConvert<QVariantList>())
        return;

    QMetaSequence::Iterable iterable =
        value.value<QMetaSequence::Iterable>();

    auto it = iterable.begin();
    const auto end = iterable.end();
    for (; it != end; ++it) {
        const QVariant element = *it;
        qDebug() << element;
    }
}
```

这里真正持有的类型是 `QMetaSequence::Iterable::const_iterator`，它派生自 `QConstIterator<QMetaSequence>`。文档单列 `QConstIterator`，是为了说明其共用的比较、前进、后退和距离运算。

关联容器使用 `QMetaAssociation::Iterable`。其 const iterator 同样能读取 value，并额外有 `key()`；这适用于运行时检查一个未知 `QMap`、`QHash` 或其他已注册关联容器的键值对。

## “const” 的边界和对象寿命

`QConstIterator` 只提供只读迭代路径，不能通过它修改当前元素。需要修改运行时容器时，应使用对应 `QIterable` 的 mutable iterator 入口及 `QIterator` 派生类型，并确认 `QVariant` 的存储值可写。

迭代器依赖包装它的 `QIterable`，后者又指向实际容器数据。因此遍历期间必须让保存容器的 `QVariant` 与 `Iterable` 对象持续存活：

```cpp
QMetaSequence::Iterable makeBadIterator()
{
    QVariant local = QVariant::fromValue(QStringList{"a", "b"});
    return local.value<QMetaSequence::Iterable>(); // 返回的视图依赖 local，不能这样使用。
}
```

不要在取得迭代器后修改、替换或销毁底层容器，也不要让另一个线程并发修改它。迭代器失效规则最终取决于真实容器类型；元类型包装不会让原生容器的失效规则消失。

## 前进、后退和跳跃不是所有容器都支持

`QIterable` 能报告底层容器的迭代能力：

- `canInputIterate()`：是否至少可单向读取。
- `canForwardIterate()`：是否支持多次前向遍历。
- `canReverseIterate()`：是否支持反向移动。
- `canRandomAccessIterate()`：是否能高效跳过多个元素。

这些检查属于 `QIterable`，不是 `QConstIterator` 自己的成员。使用 `--it`、`it--`、`it - n` 或 `it -= n` 前，先确认 `canReverseIterate()`；否则行为未定义。对频繁的 `it + n`、`it += n` 和两个迭代器求距离，也不要假设一定是常数时间，性能敏感时先确认 `canRandomAccessIterate()`。

无论底层能力如何，边界规则都和 STL 风格迭代器一致：

- 对 `end()` 执行 `++it` 是未定义行为。
- 对 `begin()` 执行 `--it` 是未定义行为。
- 比较或求距离应只针对同一个 iterable 产生的迭代器；把来自不同容器的迭代器混在一起没有有意义的结果。

## 运算符该怎样选

最常见的循环使用前置递增：

```cpp
for (auto it = iterable.begin(), end = iterable.end(); it != end; ++it) {
    const QVariant value = *it;
    // 读取 value。
}
```

`++it` 就地移动并返回自身；`it++` 必须保留移动前的副本，通常没有必要时优先前置形式。`operator+`、`operator-` 返回新迭代器，不改变原位置；`+=`、`-=` 则原地移动。两个迭代器相减得到的是它们之间的距离，不是元素值之差。

`QConstIterator` 的基类 `QBaseIterator` 还暴露 `constIterator()` 与 `mutableIterator()`，可取得内部原生迭代器的擦除指针。这是元类型系统的低层扩展接口，不是跨容器通用句柄；应用代码不应缓存、转换或解引用它。

## 常见误区

- 把它当作 `QList` 的常规 `const_iterator`。已知容器类型时，直接使用容器 API，类型安全且没有 `QVariant` 转换成本。
- 手工传入 `void *` 构造迭代器。底层 iterator 的内存布局由容器实现决定，错误指针会导致未定义行为。
- 只因 `it + 100` 能编译就假定高效或合法。先通过 `QIterable` 查询能力，再决定是否采用跳跃、反向或距离操作。
- 取得 iterator 后修改 `QVariant` 中的容器。隐式共享分离、扩容、插入和删除都可能使迭代位置失效。
- 以为 `QConstIterator` 能直接定义统一的 `operator*()`。实际解引用语义由 `QMetaSequence::Iterable::ConstIterator`、`QMetaAssociation::Iterable::ConstIterator` 等派生类型提供。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QConstIterator(const QIterable<Container> *, void *)` | 包装某个 iterable 的底层 const iterator。 | 面向 Qt 元类型迭代内部；业务代码从 `begin()` 或 `constBegin()` 获取，勿手工传裸指针。 |
| 比较 | `operator==(const QConstIterator &) const` | 判断两个迭代器是否指向同一位置。 | 只比较同一个 iterable 产生的迭代器；通常用于与 `end()` 判断循环结束。 |
| 比较 | `operator!=(const QConstIterator &) const` | 判断两个迭代器是否指向不同位置。 | 常用于 `it != end`；不同底层容器的比较没有可依赖的语义。 |
| 前进 | `operator++()` | 前置递增，移动到下一个元素并返回自身。 | 不可对 `end()` 调用；普通循环优先使用这个重载。 |
| 前进 | `operator++(int)` | 后置递增，返回旧位置后再移动到下一个元素。 | 不可对 `end()` 调用；会保留旧位置副本，不需要旧值时用前置递增。 |
| 前进 | `operator+=(qsizetype)` | 原地前进指定步数。 | 是否高效取决于底层容器；不要越过 `end()`。 |
| 跳跃 | `operator+(qsizetype) const` | 返回当前位置向前若干步的新迭代器。 | 不改变原迭代器；性能敏感时检查 `canRandomAccessIterate()`。 |
| 非成员跳跃 | `operator+(qsizetype, const QConstIterator &)` | 提供 `n + it` 形式的对称写法。 | 语义等同于 `it + n`；同样不能越过有效范围。 |
| 后退 | `operator--()` | 前置递减，移动到前一个元素并返回自身。 | 仅双向迭代容器可用；对 `begin()` 调用是未定义行为。 |
| 后退 | `operator--(int)` | 后置递减，返回旧位置后再移动到前一个元素。 | 仅双向迭代容器可用；对 `begin()` 调用是未定义行为。 |
| 后退 | `operator-=(qsizetype)` | 原地后退指定步数。 | 先确认 `canReverseIterate()`；不要移到 `begin()` 之前。 |
| 后退 | `operator-(qsizetype) const` | 返回当前位置向后若干步的新迭代器。 | 仅双向迭代容器可用；不改变原迭代器。 |
| 距离 | `operator-(const QConstIterator &) const` | 返回两个位置之间的距离。 | 两个迭代器必须来自同一 iterable；复杂度依赖底层容器能力。 |

## 一句话记忆

`QConstIterator` 是 Qt 元类型容器反射的只读迭代底座：从 `QMetaSequence::Iterable` 或 `QMetaAssociation::Iterable` 获取它，底层容器活着且不变时再按其真实迭代能力前进、后退或跳跃。
