# QVariant::ConstReference 只读间接引用笔记

> 适用版本：Qt 6.11.1  
> 所属模块：`Qt6::Core`  
> 定义位置：`#include <QVariant>`  
> 类型性质：保存 `Indirect` 并把读取操作转成 `QVariant` 的只读代理

## 1. 它解决什么问题

`QVariant::ConstReference<Indirect>` 表达一个“可以读取为 `QVariant`、但不能写回”的间接元素。

它主要服务于 Qt 元容器的只读 iterator：

- `QMetaSequence` 的只读 iterator 解引用可以得到 `QVariant::ConstReference`；
- `QMetaAssociation` 的只读 iterator 解引用可以得到 `QVariant::ConstReference`；
- 代理保存的是 iterator 或其他 `Indirect`，不拥有容器和元素；
- 转换为 `QVariant` 时读取当前元素值；
- 没有任何赋值运算符，因此不能通过该代理修改底层容器。

它不是 `const T &` 的通用替代品，而是给“运行时才知道元素类型”的元容器提供只读适配。

## 2. 实际使用场景

### 2.1 遍历元序列中的只读元素

```cpp
for (auto it = iterable.constBegin();
     it != iterable.constEnd(); ++it) {
    QVariant::ConstReference reference = *it;
    const QVariant value = reference;
    qDebug() << value;
}
```

通常可以直接写成：

```cpp
for (auto it = iterable.constBegin();
     it != iterable.constEnd(); ++it) {
    const QVariant value = *it;
    qDebug() << value;
}
```

这里的 `QVariant` 是元素的值副本。修改它不会回写底层容器。

### 2.2 统一处理顺序容器和关联容器

```cpp
void inspect(const QMetaSequence::Iterable &sequence)
{
    for (auto it = sequence.constBegin();
         it != sequence.constEnd(); ++it) {
        const QVariant value = *it;
        qDebug() << value.metaType().name() << value;
    }
}
```

对于关联容器，`ConstReference` 表示 mapped value；key 由关联 iterator 的 `key()` API 单独读取。

### 2.3 把可写代理降级为只读代理

```cpp
QVariant::Reference<Iterator> writable = *mutableIterator;
QVariant::ConstReference<Iterator> readonly = writable;

const QVariant snapshot = readonly;
```

这个转换只保留读取能力。`readonly` 不会让底层元素变成只读，也不会复制元素；它只是不能通过自身执行写回。

## 3. 构建与包含

```cpp
#include <QVariant>
#include <QMetaSequence>
#include <QMetaAssociation>
```

业务代码通常通过只读元 iterator 获得 `ConstReference`，而不是手动指定一个自定义 `Indirect`。

## 4. 核心使用模型

### 4.1 代理保存间接访问器，不保存元素副本

```cpp
QVariant::ConstReference<Iterator> reference = *iterator;
```

复制 `reference` 只会复制 `Indirect`。底层容器被销毁、iterator 失效或容器修改导致 iterator 失效后，所有相关代理都不能继续使用。

### 4.2 转成 QVariant 才得到独立值

```cpp
const QVariant value = reference;
```

转换后 `value` 拥有自己的 variant 值语义。它不会持续绑定到当前 iterator，也不会随着容器中同一元素的后续变化自动更新。

### 4.3 只读代理不能赋值

以下意图不成立：

```cpp
// reference = QVariant(42); // 没有赋值 API
```

需要写回时，必须使用可写 iterator，并通过 `QVariant::Reference` 完成赋值。

## 5. 生命周期和失效边界

- `ConstReference` 不拥有底层容器；
- 代理的有效期不能超过 `Indirect` 和底层 iterator；
- 插入、删除、扩容、detach 或容器重分配可能使 iterator 和代理失效；
- 复制 `ConstReference` 不会产生元素快照；
- 转成 `QVariant` 后，得到的是独立值，之后可以脱离 iterator 使用；
- 只读代理不能阻止其他代码通过可写 iterator 修改同一个元素。

如果需要长期保存读取结果，应尽快转换成 `QVariant` 或具体类型，而不是保存 `ConstReference`。

## 6. 逐项 API 说明

### `ConstReference(const Indirect &referred)`

复制构造间接访问器。它复制的是 iterator/访问器，不是当前元素。

### `ConstReference(Indirect &&referred)`

移动构造间接访问器，适合从 iterator 临时对象创建代理。底层 iterator 的失效规则仍然适用。

### `ConstReference(const ConstReference &)`

默认拷贝构造。多个只读代理可以代表同一个逻辑位置，但不会互相同步成独立快照。

### `ConstReference(const Reference<Indirect> &nonConst)`

从可写 `Reference` 构造只读代理：

```cpp
QVariant::Reference<Iterator> writable = *mutableIterator;
QVariant::ConstReference<Iterator> readonly = writable;
```

这个转换会丢弃写回能力，但不会复制底层元素，也不会改变原来的可写代理。

### `ConstReference(ConstReference &&) = delete`

移动构造被删除。Qt 将其设计成可以复制的只读代理，而不是需要移动资源所有权的对象。

### `operator=(...) = delete`

`ConstReference` 的拷贝赋值和移动赋值均被删除。只读代理不能在创建后改指向另一个 `Indirect`；要换目标，应重新构造一个代理。

### `~ConstReference()`

销毁代理自身，不销毁元素，不释放容器，也不影响底层 iterator。

### `operator QVariant() const`

把当前间接元素读取为 `QVariant`。Qt 元序列和元关联 iterator 会根据元素或 mapped value 的 `QMetaType` 生成一个 variant 值。

返回的 `QVariant` 是值容器。它和底层元素之间没有持续写回关系。

## 7. 与相邻类型的区别

| 类型 | 读取 | 写回 | 复制后是否拥有快照 |
| --- | --- | --- | --- |
| `QVariant::ConstReference` | 转 `QVariant` | 不支持 | 否 |
| `QVariant::Reference` | 转 `QVariant` | 支持 | 否 |
| `QVariant::ConstPointer` | `operator*()` 得到 `ConstReference` | 不支持 | 否 |
| `QVariant::Pointer` | `operator*()` 得到 `Reference` | 间接支持 | 否 |
| `QVariant` | 直接保存值 | 修改自身 | 是 |

## 8. 常见错误

### 8.1 把 ConstReference 当成元素快照

```cpp
auto reference = *iterator;
// iterator 失效后继续使用 reference 是错误的。
```

需要快照时立即转换：

```cpp
const QVariant snapshot = *iterator;
```

### 8.2 期待修改 QVariant 自动写回

```cpp
QVariant value = *iterator;
value = 42;
```

这只修改 `value`。只读代理没有写回能力。

### 8.3 用 const 代理绕过底层可写限制

从 `ConstReference` 不能转回 `Reference`。需要写入时重新取得可写 iterable/iterator，并确认底层元容器支持写入。

### 8.4 忽略关联容器的 key/value 区别

关联 iterator 的 `ConstReference` 通常代表 mapped value，不是 key。应通过 iterator 的 `key()` 单独读取 key。

## API 速查表
| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `ConstReference(const Indirect &)` | 复制间接访问器 | 不复制元素 |
| `ConstReference(Indirect &&)` | 移动构造访问器 | 不转移容器所有权 |
| `ConstReference(const ConstReference &)` | 复制只读代理 | 仍依赖同一底层位置 |
| `ConstReference(const Reference &)` | 可写代理降级为只读代理 | 丢弃写回能力，不复制元素 |
| `ConstReference(ConstReference &&) = delete` | 禁止移动构造 | 代理不是资源所有者 |
| `operator=(...) = delete` | 禁止重新赋值代理 | 换目标需重新构造 |
| `~ConstReference()` | 销毁代理 | 不销毁底层元素 |
| `operator QVariant()` | 读取当前元素为 QVariant | 得到值副本，不是持续引用 |

## 10. 一句话总结

`QVariant::ConstReference` 是元容器只读 iterator 的间接引用：它保存访问器、按需把当前元素读成 `QVariant`，但不拥有元素、不支持写回，也不能替代一个长期有效的值快照。
