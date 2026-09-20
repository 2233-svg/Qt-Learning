# Qt QBaseIterator 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QBaseIterator>`  
> 所属模块：`Qt6::Core`  
> 模板声明：`template <typename Container> class QBaseIterator`

## 1. 它不是给业务代码遍历容器用的

`QBaseIterator` 是 Qt 元类型容器迭代体系里的底层基类。它解决的问题不是“怎样遍历一个 `QList`”，而是让 Qt 可以在不知道具体容器元素类型的前提下，统一保存和传递一个迭代位置。

它处在这一组类型的底层：

```text
QIterable
  ├─ QConstIterator<Container>
  └─ QIterator<Container>
        └─ QBaseIterator<Container>
```

`QIterable` 用于把支持运行时类型信息的容器包装成可统一访问的对象；`QConstIterator` 和 `QIterator` 分别表示只读、可写迭代器。`QBaseIterator` 为这两种迭代器提供共同的“内部原生迭代器地址”访问能力。

因此，它更接近 Qt 框架内部的适配层，而不是 STL 风格的公开迭代器接口。普通应用代码几乎不应该直接声明、构造或操作它。

## 2. 它解决的具体问题：运行时不知道容器类型时，怎样记录位置

C++ 模板容器的迭代器类型通常依赖完整的容器类型。例如，`QList<int>::iterator` 和 `QMap<QString, int>::iterator` 是不同类型，不能直接放进同一种变量。

但 Qt 的元对象系统有时需要以运行时方式处理容器，例如某段通用代码只知道“这里有一个可迭代的 Qt 容器”，却不知道元素的编译期类型。此时 Qt 需要：

1. 用 `QIterable` 抹平不同容器的对外访问方式。
2. 在内部保存该容器对应的 native iterator。
3. 让只读和可写迭代器能共享这套保存机制。

`QBaseIterator<Container>` 正是第 2、3 步的共同底座。它将 native iterator 以 `const void *` 或 `void *` 的形式暴露给 Qt 的配套实现，避免在公共抽象层泄露每个容器的具体迭代器类型。

这也解释了为什么它的 API 看起来很少：它不是负责 `++`、`*`、比较或查找的完整迭代器，只负责把已经存在的内部迭代器交给框架协作代码。

## 3. 与日常容器遍历的区别

下面是日常业务代码应优先采用的写法：

```cpp
QList<QString> names = {"Ada", "Lin", "Ming"};

for (const QString &name : names)
    qDebug() << name;
```

或者在确实需要保存位置时，使用具体容器的迭代器：

```cpp
QMap<QString, int> scores;
scores.insert("Ada", 92);

auto it = scores.constFind("Ada");
if (it != scores.cend())
    qDebug() << it.key() << it.value();
```

这里的 `auto` 保留了正确的具体迭代器类型，编译器可以检查解引用、递增和容器匹配关系。不要为了“通用”而把它转换成 `QBaseIterator` 所给出的 `void *`。

`QBaseIterator` 有意义的场景通常是：

- 编写 Qt 自身的容器元类型支持或阅读其实现。
- 在极少数需要通过 `QIterable` 做运行时容器访问的框架代码中理解迭代器如何传递。
- 调试 Qt 迭代包装层，确认当前对象是否持有内部 native iterator。

如果你的代码已经知道容器类型，直接用该容器的迭代器或范围 `for` 循环，类型更安全，也更容易维护。

## 4. 构造、所有权与生命周期边界

`QBaseIterator` 的公开文档没有提供供用户直接调用的构造函数。它由派生的 `QConstIterator`、`QIterator` 在 Qt 的迭代包装流程中使用。

它也不拥有容器，更不会延长容器或 native iterator 的寿命。通过 `constIterator()`、`mutableIterator()` 取得的指针只表示内部实现对象：

- 指针的实际类型不是公开 API 契约的一部分。
- 指针的有效期依赖原迭代器及其关联容器。
- 容器析构、迭代器销毁或可能使迭代器失效的容器修改后，先前取得的地址都不应再使用。
- 不要保存、`static_cast`、`reinterpret_cast` 或解引用这些 `void *`。

`constIterator()` 返回 `const void *`，从类型上限制调用方通过该指针修改内部迭代器；`mutableIterator()` 则为 Qt 的可写包装实现保留修改入口。后者不是对业务代码开放的“绕过 const”的工具。

## 5. 两个 API 分别做什么

### 5.1 `constIterator()`

```cpp
const void *QBaseIterator<Container>::constIterator() const
```

返回内部 native iterator 的只读地址。Qt 的只读迭代包装代码可以用它取得底层状态，而不允许通过该返回值修改该状态。

返回类型是 `const void *`，意味着调用方无法从函数签名得知真实迭代器类型；这正是它用于类型擦除适配的原因。也正因为如此，外部代码没有可移植、受支持的方式把它还原成某个具体迭代器。

### 5.2 `mutableIterator()`

```cpp
void *QBaseIterator<Container>::mutableIterator()
```

返回内部 native iterator 的可写地址，供可变迭代包装层在 Qt 的实现内部更新或操作迭代位置。

它不代表“可以安全修改容器”。迭代器位置可写和容器内容可写是两回事；容器是否可修改、修改是否会使迭代器失效，仍取决于具体容器及当前使用方式。

## 6. 常见误区

### 6.1 把它当作 `QList` 或 `QMap` 的迭代器

它没有标准遍历操作，不能直接做 `++it`、`*it` 或与 end iterator 比较。请使用 `QList<T>::iterator`、`QMap<Key, T>::iterator`，或者范围 `for`。

### 6.2 拿到 `void *` 后强制转换

这种写法把 Qt 私有实现细节变成业务代码依赖：

```cpp
// 不要这样做：真实类型、布局和有效期都不是公开契约。
auto *native = static_cast<SomeIterator *>(base.mutableIterator());
```

即使当前 Qt 版本中恰好可用，换容器、升级 Qt 或改变包装方式后也可能失效。需要遍历时，应回到具体容器 API。

### 6.3 以为 `constIterator()` 能解决迭代器失效

返回 `const` 只限制通过该指针写入内部状态，不能保证底层容器不会变，也不能让失效的迭代器重新有效。遍历期间修改容器前，仍要查阅该容器的迭代器失效规则。

### 6.4 自己管理返回指针的释放

两个函数返回的是内部对象的地址，不是新分配的堆内存。调用方既不拥有它，也不能 `delete` 它。

## 7. 关联类型怎么选

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 具体容器只读遍历 | 范围 `for` 或 `const_iterator` | 在已知容器类型时顺序读取元素。 | 类型安全，表达意图直接，优先于运行时迭代包装。 |
| 具体容器可写遍历 | 容器的 `iterator` | 在已知容器类型时修改当前迭代位置对应的元素。 | 遵守具体容器的迭代器失效规则。 |
| 运行时只读访问 | `QIterable` / `QConstIterator` | 在不知道完整容器类型时通过 Qt 抽象层读取元素。 | 适合元类型、反射和框架代码，不是普通遍历的首选。 |
| 运行时可写访问 | `QIterable` / `QIterator` | 在 Qt 的运行时容器包装层中修改元素或位置。 | 是否能写取决于底层容器和包装方式。 |
| 底层迭代桥接 | `QBaseIterator::constIterator()` | 读取 Qt 内部包装的 native iterator 地址。 | 框架实现边界，业务代码通常不需要直接使用。 |

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 只读桥接 | `const void *constIterator() const` | 返回内部 native iterator 的只读地址，供 Qt 的迭代包装层取得当前位置。 | 不知道也不应假设其真实类型；不要转换、保存、解引用或释放返回指针。 |
| 可写桥接 | `void *mutableIterator()` | 返回内部 native iterator 的可写地址，供 Qt 的可变迭代包装层操作内部状态。 | 可写地址不等于可以随意修改容器；它是框架协作接口，业务代码不要直接依赖。 |

---

### 一句话总结

`QBaseIterator` 是 `QIterable` 迭代包装体系的内部共同基类，用 `void *` 把具体容器的 native iterator 交给 Qt 框架协作；常规应用代码应使用具体容器迭代器、`QConstIterator`、`QIterator` 或范围 `for`，而不是直接操作它。
