# Qt QMetaSequence::Iterable 顺序容器高层访问笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QMetaSequence>`  
> 所属模块：`Qt6::Core`  
> 类型性质：把 `QMetaSequence` 和真实顺序容器包装成 `QVariant` range 的借用视图  
> 相关类型：`QMetaSequence`、`QIterable`、`QIterator`、`QConstIterator`、`QVariant`

## 1. 它解决什么问题

`QMetaSequence` 的底层 API 使用 `void *`、擦除 iterator 和显式 result 存储，适合 Qt 反射实现，但不适合普通业务代码。`QMetaSequence::Iterable` 在这之上提供一个更容易使用的视图：

- 保存一个 `QMetaSequence` 描述器；
- 借用一个真实顺序容器；
- 用 C++ range-for 和 iterator 遍历；
- 把元素读成 `QVariant`；
- 通过 `QVariant` 修改元素；
- 提供 `at()`、`setAt()`、`append()`、`prepend()`、首尾删除；
- 让擦除 iterator 由 RAII 自动创建和销毁。

它不是容器副本，也不拥有真实容器。视图和它产生的 iterator 都依赖真实容器在使用期间保持存活。

## 2. 最小使用方式

### 2.1 直接包装真实容器

```cpp
QList<int> values{10, 20, 30};

QMetaSequence::Iterable iterable(
    QMetaSequence::fromContainer<QList<int>>(),
    &values);

for (const QVariant &value : iterable)
    qDebug() << value.toInt();
```

这里 `iterable` 借用 `values`，不会复制或接管它。`values` 必须比 `iterable` 和所有 iterator 活得更久。

### 2.2 可写访问

```cpp
if (iterable.metaContainer().canSetValueAtIndex())
    iterable.setAt(1, QVariant(99));

if (iterable.metaContainer().canAddValueAtEnd())
    iterable.append(QVariant(40));
```

高层 API 仍然要求底层能力存在。`Iterable` 不会把一个没有 setter/append 能力的容器凭空变成可写容器。

### 2.3 从 QVariant 中取得

Qt 的元容器体系可以为已注册的顺序容器提供 `QMetaSequence::Iterable` 视图：

```cpp
QVariant variant = QVariant::fromValue(QList<int>{1, 2, 3});
if (variant.canConvert<QMetaSequence::Iterable>()) {
    const auto iterable =
        variant.value<QMetaSequence::Iterable>();
    for (const QVariant &value : iterable)
        qDebug() << value;
}
```

这种视图是否可写取决于 QVariant 内部容器和取得方式。只读来源不要强行调用 `mutableBegin()` 或修改 API。

## 3. 借用视图的生命周期

### 3.1 视图不拥有容器

```cpp
QMetaSequence::Iterable makeView()
{
    QList<int> local{1, 2, 3};
    return QMetaSequence::Iterable(
        QMetaSequence::fromContainer<QList<int>>(),
        &local);
}
```

上例返回的 view 立即悬空，因为 `local` 已经销毁。不要返回指向局部容器的 view。

### 3.2 容器修改会影响 iterator

`append()`、`prepend()`、删除、`setAt()`、`clear()` 和真实容器自己的扩容/移动都可能使已有 iterator 失效。修改容器后，应重新取得 begin/end。

### 3.3 copy/move 只复制视图状态

复制 `Iterable` 通常只复制元描述器和借用指针，不复制真实容器。移动 view 也不让底层容器获得新所有者。将 view 保存为成员时，必须同时设计真实容器的生命周期。

## 4. Iterator 能力层级

`Iterable` 根据 `QMetaContainer` 的真实 iterator 能力提供带标签的 iterator 类型：

| 类型别名 | 语义 |
| --- | --- |
| `InputIterator` | 只保证单向输入遍历 |
| `ForwardIterator` | 支持多次遍历 |
| `BidirectionalIterator` | 还支持 `--` |
| `RandomAccessIterator` | 还支持 `+/- n` 和距离 |
| `InputConstIterator` 等 | 对应只读版本 |

`begin()` 返回的具体 `iterator` 通常使用最合适的类型，但不要因为类型名存在就假定底层一定支持随机访问。请求不受支持的强 iterator 标签时，Qt 可能进入 fatal 路径；先检查：

```cpp
iterable.canInputIterate();
iterable.canForwardIterate();
iterable.canReverseIterate();
iterable.canRandomAccessIterate();
```

## 5. QVariant 元素语义

### 5.1 只读 iterator 解引用

```cpp
for (auto it = iterable.constBegin();
     it != iterable.constEnd(); ++it) {
    const QVariant value = *it;
    qDebug() << value;
}
```

只读序列 iterator 解引用得到一个 `QVariant` 值副本。这个 QVariant 不等于真实容器元素的地址，修改它不会回写容器。

### 5.2 可写 iterator 解引用

```cpp
for (auto it = iterable.mutableBegin();
     it != iterable.mutableEnd(); ++it) {
    QVariant value = *it;
    value = value.toInt() + 1;
    *it = value;
}
```

可写 iterator 的 `operator*()` 返回 `QVariant::Reference`，赋值时会尝试把右侧 QVariant 转成元素类型并写回底层 iterator。底层没有 `canSetValueAtIterator()` 时，不应使用这种写法。

### 5.3 `operator[]`

随机访问 iterator 的 `operator[](n)` 依赖底层 random access 能力。它返回元素的 QVariant 视图/副本语义，不应保存为跨容器修改的引用。

## 6. 索引 API 的边界

### 6.1 `at()` 的优先路径

`at(index)` 首先使用 `QMetaSequence::canGetValueAtIndex()` 和 `valueAtIndex()`。这通常是最直接的索引访问。

如果底层没有索引读取能力，Qt 6.11 可能通过 const iterator 从 begin 前进 `index` 步来合成访问，并发出 synthesized access 警告：

- 复杂度可能是 O(n)；
- 需要完整 const iterator；
- 负 index 不提供特殊语义；
- 越界访问不应被依赖。

### 6.2 `setAt()` 的前置条件

```cpp
if (iterable.metaContainer().canSetValueAtIndex())
    iterable.setAt(index, value);
```

`setAt()` 需要底层按索引写入能力和可写真实容器。它会尝试 QVariant 到元素 `QMetaType` 的转换；类型不兼容或索引不合法时，不应把调用当作成功。

## 7. 添加和删除 API

### 7.1 新 API

```cpp
iterable.append(QVariant(4));
iterable.prepend(QVariant(0));
iterable.removeLast();
iterable.removeFirst();
```

调用前分别检查：

- `canAddValueAtEnd()`；
- `canAddValueAtBegin()`；
- `canRemoveValueAtEnd()`；
- `canRemoveValueAtBegin()`。

空容器上调用 remove 属于底层容器边界错误；通用工具应先检查 `size()` 或记录容器非空状态。

### 7.2 Qt 6.11 以前的兼容 API

`addValue(value, Position)`、`removeValue(Position)` 和 `valueMetaType()` 仍可能存在，但在 Qt 6.11 已标记 deprecated。新代码使用：

- `append()`；
- `prepend()`；
- `removeLast()`；
- `removeFirst()`；
- `metaContainer().valueMetaType()`。

## 8. `size()`、`clear()` 和元容器能力

`Iterable` 继承 `QIterable<QMetaSequence>`：

```cpp
const qsizetype count = iterable.size();
iterable.clear();
```

在 Qt 6.11：

- 有原生 `hasSize()` 时，`size()` 使用原生 size；
- 没有原生 size 但有 const iterator 时，`size()` 可能通过距离合成并发出警告；
- 没有可用 const iterator 时，可能返回 `-1`；
- `clear()` 需要 `canClear()` 和可写真实容器。

`size()` 的返回值 `-1` 表示无法取得可靠大小，不应转成无符号整数。

## 9. 构造形式

### 9.1 按真实类型构造

```cpp
QMetaSequence::Iterable readOnly(
    QMetaSequence::fromContainer<QList<int>>(),
    static_cast<const QList<int> *>(&values));

QMetaSequence::Iterable writable(
    QMetaSequence::fromContainer<QList<int>>(),
    &values);
```

const 指针构造产生只读视图；非 const 指针构造才允许 `mutableBegin()` 和写入操作。

### 9.2 传入类型擦除指针

```cpp
QMetaType containerType = QMetaType::fromType<QList<int>>();
QMetaSequence::Iterable view(
    QMetaSequence::fromContainer<QList<int>>(),
    containerType,
    &values);
```

带 `QMetaType` 的构造主要用于更底层的类型擦除桥接。传入的 `QMetaType`、对齐、真实指针和 `QMetaSequence` 必须描述同一个容器类型；普通业务优先使用类型模板构造。

## 10. 逐项 API 说明

### 10.1 默认构造

```cpp
Iterable();
```

构造空视图。它没有有效元描述器和真实容器，begin/end/at 等操作不应作为正常业务路径调用。

### 10.2 `Iterable(const QMetaSequence &, const T *)`

```cpp
template <typename T>
Iterable(const QMetaSequence &meta,
         const T *container);
```

创建只读借用视图。`T` 必须和 meta 描述的真实容器相匹配，container 的生命周期必须覆盖 view 和 iterator。

### 10.3 `Iterable(const QMetaSequence &, T *)`

```cpp
template <typename T>
Iterable(const QMetaSequence &meta,
         T *container);
```

创建可写借用视图。它不会取得所有权，也不会防止真实容器被其他代码修改。

### 10.4 `Iterable(const QMetaSequence &, Pointer)`

```cpp
template <typename Pointer>
Iterable(const QMetaSequence &meta,
         Pointer iterable);
```

以类型擦除或适配指针构造 view。只有在明确掌握指针真实类型、对齐和 const 资格时才使用。

### 10.5 带 `QMetaType` 的构造函数

```cpp
Iterable(const QMetaSequence &meta,
         QMetaType metaType,
         void *iterable);

Iterable(const QMetaSequence &meta,
         QMetaType metaType,
         const void *iterable);
```

为低层类型擦除场景提供对齐信息。`metaType` 必须描述 iterable 指向的容器类型，不是元素类型。

### 10.6 `begin()`/`end()`

```cpp
const_iterator begin() const;
const_iterator end() const;
```

返回只读遍历范围。end 只能比较，不能解引用。它们借用 view 和真实容器，容器修改后可能失效。

### 10.7 `constBegin()`/`constEnd()`

```cpp
const_iterator constBegin() const;
const_iterator constEnd() const;
```

显式创建只读 iterator。`begin()`/`end()` 对序列 view 通常等价于 constBegin/constEnd。

### 10.8 `mutableBegin()`/`mutableEnd()`

```cpp
iterator mutableBegin();
iterator mutableEnd();
```

创建可写 iterator。view 必须来自非 const 容器，底层必须有可写 iterator。end 仍不能解引用。

### 10.9 `at(qsizetype)`

```cpp
QVariant at(qsizetype index) const;
```

读取索引元素并返回 QVariant。优先走原生索引操作，没有时 Qt 6.11 可能通过 iterator 合成；没有合法访问能力或索引无效时不要依赖返回值。

### 10.10 `setAt(qsizetype, const QVariant &) `

```cpp
void setAt(qsizetype index,
           const QVariant &value);
```

把 QVariant 转成元素类型并写入索引位置。调用前检查 `canSetValueAtIndex()`、索引范围和 view 的可写性。

### 10.11 `append(const QVariant &)`

```cpp
void append(const QVariant &value);
```

把值转换成元素类型并添加到尾部。需要 `canAddValueAtEnd()`；操作可能使所有 iterator 失效。

### 10.12 `prepend(const QVariant &)`

```cpp
void prepend(const QVariant &value);
```

把值转换成元素类型并添加到头部。需要 `canAddValueAtBegin()`；前端插入通常会使已有 iterator 失效。

### 10.13 `removeLast()`

```cpp
void removeLast();
```

移除最后一个元素。需要底层 `canRemoveValueAtEnd()`，空容器上不要调用。

### 10.14 `removeFirst()`

```cpp
void removeFirst();
```

移除第一个元素。需要底层 `canRemoveValueAtBegin()`，空容器上不要调用。

### 10.15 `Iterator` 与 iterator 别名

```cpp
using iterator = Iterator;
using RandomAccessIterator = ...;
using BidirectionalIterator = ...;
using ForwardIterator = ...;
using InputIterator = ...;
```

这些别名代表不同强度的可写 iterator。具体类型通过 `operator*()`、`operator->()` 和随机访问 `operator[]` 暴露 QVariant 元素；强能力别名不能绕过底层能力检查。

### 10.16 `ConstIterator` 与 const iterator 别名

```cpp
using const_iterator = ConstIterator;
using RandomAccessConstIterator = ...;
using BidirectionalConstIterator = ...;
using ForwardConstIterator = ...;
using InputConstIterator = ...;
```

这些别名代表只读 iterator。只读 iterator 的解引用产生 QVariant 读取结果，不提供回写。

### 10.17 `Iterator::operator*()`

```cpp
QVariant::Reference<Iterator> operator*() const;
```

返回当前元素的可写 QVariant reference。对其赋值会尝试写回底层元素；当前 iterator 不能是 end，底层必须支持 iterator 写入。

### 10.18 `Iterator::operator->()`

```cpp
QVariant::Pointer<Iterator> operator->() const;
```

提供当前 QVariant reference 的指针式访问。它仍依赖 iterator 和真实容器生命周期，不能保存为长期指针。

### 10.19 `Iterator::operator[](qsizetype)`

```cpp
QVariant::Reference<Iterator>
operator[](qsizetype offset) const;
```

随机访问当前位置偏移的元素。需要底层 random access 能力；offset 越界不受支持。

### 10.20 `ConstIterator::operator*()`

```cpp
QVariant operator*() const;
```

读取当前元素并返回 QVariant 值。返回值是业务侧副本，修改它不回写容器。

### 10.21 `ConstIterator::operator->()`

```cpp
QVariant::ConstPointer<ConstIterator> operator->() const;
```

提供只读的 QVariant pointer 访问。它不能用于修改真实元素。

### 10.22 `ConstIterator::operator[](qsizetype)`

```cpp
QVariant operator[](qsizetype offset) const;
```

读取随机访问偏移元素并返回 QVariant。需要 random access const iterator 能力。

### 10.23 `Position`

```cpp
enum Position {
    Unspecified,
    AtBegin,
    AtEnd
};
```

Qt 6.11 起 deprecated 的兼容枚举。新代码不要用它控制添加/移除位置，改用明确的 `append()`、`prepend()`、`removeLast()` 和 `removeFirst()`。

### 10.24 `addValue(const QVariant &, Position)`

```cpp
void addValue(const QVariant &value,
              Position position = Unspecified);
```

Qt 6.11 起 deprecated。它是旧的未指定/头部/尾部添加入口，转换 value 后根据 position 调用相应元容器能力。新代码使用明确 API。

### 10.25 `removeValue(Position)`

```cpp
void removeValue(Position position = Unspecified);
```

Qt 6.11 起 deprecated。新代码使用 `removeFirst()`、`removeLast()`；未指定位置的旧行为由底层适配器决定。

### 10.26 `valueMetaType() const`

```cpp
QMetaType valueMetaType() const;
```

Qt 6.11 起 deprecated，改用 `metaContainer().valueMetaType()`。它返回元素类型，不是 view 或容器类型。

## 11. 继承自 `QIterable` 的常用 API

### 11.1 能力查询

```cpp
bool canInputIterate() const;
bool canForwardIterate() const;
bool canReverseIterate() const;
bool canRandomAccessIterate() const;
```

它们分别反映底层 iterator 能力。不要在 `canReverseIterate()` 为 false 时使用 `--`，也不要在 random access 为 false 时使用 `operator[]`。

### 11.2 `size()`

```cpp
qsizetype size() const;
```

优先使用原生 size；Qt 6.11 可能通过 const iterator 合成。返回 `-1` 时表示无法取得可靠大小。

### 11.3 `clear()`

```cpp
void clear();
```

调用底层清空能力。先检查 `metaContainer().canClear()`，并在调用后丢弃所有 iterator、引用和元素指针。

### 11.4 `metaContainer()`

```cpp
QMetaSequence metaContainer() const;
```

返回该 view 使用的元描述器副本。副本仍不拥有真实容器。

### 11.5 `constIterable()`/`mutableIterable()`

```cpp
const void *constIterable() const;
void *mutableIterable();
```

返回底层类型擦除容器指针。它们主要供 Qt/框架代码使用；普通业务不要把这些指针传给不匹配的 raw API。

## 12. 常见错误

### 12.1 返回局部容器的 Iterable

**症状：** range-for 崩溃或读到随机数据。

**原因：** view 只借用容器，局部变量已经销毁。

**修复：** 让真实容器拥有更长生命周期，或直接返回元素副本。

### 12.2 只读 view 调用 mutableBegin

**症状：** 得到空可写 iterator 或行为未定义。

**原因：** const 指针构造保留了 const 资格。

**修复：** 明确使用非 const 容器指针构造可写 view。

### 12.3 忽略 `QVariant` 转换

**症状：** `setAt()`/append 后元素没有按预期改变。

**原因：** QVariant 类型不能转换为元素 `QMetaType`。

**修复：** 预先用 `canConvert()`/`QMetaType` 检查并处理错误。

### 12.4 在 end 上解引用

**症状：** 空容器或循环结束处崩溃。

**原因：** end 只用于比较。

**修复：** 先比较 iterator 和 end，再解引用。

### 12.5 把 `size()` 的 -1 转成无符号

**症状：** 得到极大的容器长度。

**原因：** `size()` 可能无法合成可靠大小。

**修复：** 保留 `qsizetype`，先判断 `< 0`。

### 12.6 修改后继续使用旧 iterator

**症状：** 比较或写回错误元素。

**原因：** 底层容器修改使 iterator 失效。

**修复：** 修改后重新创建遍历范围。

## API 速查表
| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `Iterable()` | 构造空视图 | 没有有效容器 |
| `Iterable(meta, const T *)` | 构造只读借用视图 | 容器必须长生命周期 |
| `Iterable(meta, T *)` | 构造可写借用视图 | 不拥有容器 |
| `Iterable(meta, Pointer)` | 低层指针构造 | 类型、对齐、const 必须匹配 |
| `Iterable(meta, QMetaType, void *)` | 带类型擦除信息构造 | metaType 是容器类型 |
| `begin()`/`end()` | 只读 range 起止 | end 不可解引用 |
| `constBegin()`/`constEnd()` | 显式只读 iterator | 修改容器可能失效 |
| `mutableBegin()`/`mutableEnd()` | 可写 iterator 起止 | 需要非 const view 和可写能力 |
| `at(index)` | 读取索引元素 | 无索引能力时 Qt 6.11 可能合成且变慢 |
| `setAt(index, value)` | QVariant 写入索引元素 | 先检查 setter 能力和转换 |
| `append(value)` | 尾部添加 | 需要 `canAddValueAtEnd()` |
| `prepend(value)` | 头部添加 | 需要 `canAddValueAtBegin()` |
| `removeLast()` | 删除尾部 | 空容器不可用 |
| `removeFirst()` | 删除头部 | 空容器不可用 |
| `Iterator`/`iterator` | 可写 iterator 类型 | 解引用赋值可能回写 |
| `ConstIterator`/`const_iterator` | 只读 iterator 类型 | 解引用返回值副本 |
| `Iterator::operator*()` | 当前可写元素 reference | 不能是 end；需 setter |
| `Iterator::operator->()` | 当前可写元素 pointer | 不要长期保存 |
| `Iterator::operator[]()` | 随机访问可写元素 | 需要 random access |
| `ConstIterator::operator*()` | 当前元素 QVariant 值 | 修改不回写 |
| `ConstIterator::operator->()` | 当前只读 QVariant pointer | 只读 |
| `ConstIterator::operator[]()` | 随机访问只读元素 | 需要 random access |
| `canInputIterate()` 等 | 查询迭代能力 | 强 iterator 不能越级使用 |
| `size()` | 获取数量或合成数量 | 可能返回 -1/触发警告 |
| `clear()` | 清空真实容器 | 需要 `canClear()`；旧 iterator 失效 |
| `metaContainer()` | 返回 `QMetaSequence` 描述副本 | 不拥有容器 |
| `constIterable()`/`mutableIterable()` | 取得 raw 容器指针 | 主要用于框架层 |
| `addValue(value, Position)` | 旧式添加 | Qt 6.11 deprecated |
| `removeValue(Position)` | 旧式删除 | Qt 6.11 deprecated |
| `valueMetaType()` | 旧式元素类型查询 | Qt 6.11 deprecated，改用 metaContainer |

## 14. 推荐模板

### 14.1 优先用 range-for 生成快照

```cpp
QList<QVariant> snapshot(const QMetaSequence::Iterable &iterable)
{
    QList<QVariant> result;
    for (const QVariant &value : iterable)
        result.append(value);
    return result;
}
```

快照脱离真实容器后仍可使用；view 和 iterator 则不具备这种独立生命周期。

### 14.2 可写操作统一做能力检查

```cpp
bool appendInt(QMetaSequence::Iterable &iterable, int value)
{
    const QMetaSequence meta = iterable.metaContainer();
    if (!meta.canAddValueAtEnd())
        return false;

    const QVariant variant = value;
    if (!variant.canConvert(meta.valueMetaType()))
        return false;

    iterable.append(variant);
    return true;
}
```

实际项目还应根据容器 API 的错误模型决定是否需要在 append 后再次读取验证。

## 15. 一句话总结

`QMetaSequence::Iterable` 是顺序容器反射的业务友好视图：它借用真实容器，用 `QVariant` 暴露元素并自动管理擦除 iterator；它不是副本，不能延长容器生命周期，所有写入、首尾修改、随机访问和强 iterator 操作都必须服从底层 `QMetaSequence` 的能力与失效规则。
