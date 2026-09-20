# Qt QSequentialIterable 旧式顺序容器反射视图笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QSequentialIterable>`  
> 所属模块：`Qt6::Core`  
> 基类：`QIterable<QMetaSequence>`  
> 类型性质：借用真实顺序容器的类型擦除视图  
> 迁移方向：Qt 6.15 起弃用，改用 `QMetaSequence::Iterable`

## 1. 它解决什么问题

`QSequentialIterable` 让旧版 Qt 元类型反射代码在不知道具体容器类型时，仍然可以读取或修改顺序容器。它把真实容器、`QMetaSequence` 描述器和擦除后的 native iterator 组合成一个类似 STL range 的接口：

```text
真实容器 QList<T> / QVector<T> / 其它已适配顺序容器
        |
        v
QMetaSequence：描述元素类型和容器操作
        |
        v
QSequentialIterable：旧式高层视图
        |
        +-- QVariant 元素读取
        +-- QVariant 元素写入
        +-- 索引访问
        +-- 首尾添加和删除
        +-- const / mutable iterator
```

它主要服务于以下类型的通用代码：

- 旧属性编辑器根据运行时元类型显示未知序列；
- 旧脚本、序列化和诊断工具遍历 `QVariant` 里的顺序容器；
- 兼容 Qt 6.0 至 Qt 6.14 期间使用旧 iterable API 的代码；
- 需要把 `QList<T>`、`QVector<T>` 等不同具体类型统一暴露成 `QVariant` 元素的适配层。

## 2. 先说结论：新代码不要再以它为入口

Qt 6.11.1 的头文件已经给 `QSequentialIterable` 加上了：

```cpp
QT_DEPRECATED_VERSION_X_6_15(
    "Use QMetaSequence's iterables and iterators instead.")
```

这表示该类从 Qt 6.15 起进入弃用路径。迁移目标不是简单地把类型名替换成另一个旧别名，而是改用：

```cpp
QMetaSequence::Iterable
QMetaSequence::Iterable::Iterator
QMetaSequence::Iterable::ConstIterator
```

现代接口的变化包括：

- 可写引用从旧的 `QVariantRef` 改为 `QVariant::Reference`；
- 只读引用从旧的 `QVariantConstPointer` 体系改为 `QVariant::ConstPointer`；
- `set()` 改为 `setAt()`；
- `addValue()` / `removeValue()` 改为明确的 `append()`、`prepend()`、`removeLast()`、`removeFirst()`；
- 元素类型查询从旧的 `valueMetaType()` 改为 `metaContainer().valueMetaType()`；
- 迭代器类型和反射描述器的关系更直接，也更适合 Qt 6.15 之后的 API。

维护旧代码时需要读懂本类；设计新接口时应把现代类型作为公共 API。

## 3. 它不是什么

`QSequentialIterable` 不是：

- `QList<T>` 或 `QVector<T>` 的副本；
- 拥有真实容器的智能指针；
- 自动延长容器或 `QVariant` 生命周期的对象；
- 真实元素的 `T *` 指针范围；
- 保证所有顺序容器都支持随机访问的适配器；
- 可以跨容器比较或长期保存的独立 iterator。

它保存的是：

```text
QMetaSequence 描述器
        +
指向真实容器的借用指针
```

视图析构不会删除真实容器。所有 iterator 还依赖创建它们的 `QSequentialIterable` 对象，因此真实容器和 view 都必须在 iterator 使用期间保持有效。

## 4. 最小构建和直接使用

### 4.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

### 4.2 直接包装真实容器

```cpp
#include <QList>
#include <QSequentialIterable>
#include <QVariant>

QList<int> values{10, 20, 30};
QSequentialIterable view(&values);

for (auto it = view.constBegin(); it != view.constEnd(); ++it)
    qDebug() << *it;
```

这里的 `view` 只借用 `values`。`values` 必须比 `view` 以及所有从 `view` 创建的 iterator 活得更久。

### 4.3 可写访问

```cpp
QList<int> values{10, 20, 30};
QSequentialIterable view(&values);

for (auto it = view.mutableBegin(); it != view.mutableEnd(); ++it) {
    const QVariant oldValue = *it;
    *it = oldValue.toInt() + 1;
}
```

`mutableBegin()` 只有在 view 从非 const 容器指针构造时才有合法的可写对象。右侧 `QVariant` 会先尝试转换为真实元素类型，再通过元容器写回。

### 4.4 只读 view

```cpp
const QList<int> values{10, 20, 30};
QSequentialIterable view(&values);

for (const QVariant value : view)
    qDebug() << value.toInt();
```

从 `const T *` 构造会保留 const 资格。即使 `view` 本身不是 const，也不能借此取得合法的可写容器地址。

## 5. 生命周期：视图和 iterator 都是借用关系

### 5.1 不能返回指向局部容器的 view

```cpp
QSequentialIterable makeBadView()
{
    QList<int> local{1, 2, 3};
    return QSequentialIterable(&local);
} // local 销毁，返回的 view 悬空
```

正确做法是让调用方持有容器：

```cpp
QSequentialIterable makeView(QList<int> &values)
{
    return QSequentialIterable(&values);
}
```

调用方仍需保证 `values` 在 view 使用期间存在。

### 5.2 iterator 不能脱离 view 保存

`QSequentialIterator` 和 `QSequentialConstIterator` 的基类内部保存了指向 `QIterable` 的指针，用它查询元容器并销毁擦除 iterator。因此下面的结构不安全：

```cpp
auto makeBadIterator(QList<int> &values)
{
    return QSequentialIterable(&values).mutableBegin();
}
```

临时 view 在完整表达式结束后销毁，返回的 iterator 仍然引用已经不存在的 view。安全结构应把 view 放在外层：

```cpp
QSequentialIterable view(&values);
auto it = view.mutableBegin();
```

### 5.3 容器修改可能使 iterator 失效

以下操作都应视为可能使旧 iterator、元素代理和 end 失效：

- `append()`、`prepend()` 或旧的 `addValue()`；
- `removeFirst()`、`removeLast()` 或旧的 `removeValue()`；
- `clear()`；
- 真实容器自己的插入、删除、扩容、移动和赋值；
- 修改 `QVariant` 内部容器导致的分离或重新分配。

修改结构后重新调用 `begin()`、`end()`、`mutableBegin()` 或 `mutableEnd()`，不要继续复用旧位置。

## 6. 元素访问的 QVariant 语义

### 6.1 const iterator 返回值

`QSequentialConstIterator::operator*()` 返回 `QVariant`：

```cpp
const QVariant value = *view.constBegin();
```

它是读取结果，不是底层元素地址。修改这个 `QVariant` 不会回写真实容器。

返回的 `QVariant` 使用元容器报告的元素 `QMetaType` 构造。元素本身就是 `QVariant` 时，Qt 会使用特殊的存储路径避免把结果再包成不符合预期的嵌套值。

### 6.2 mutable iterator 返回旧式代理

`QSequentialIterator::operator*()` 返回：

```cpp
QVariantRef<QSequentialIterator>
```

它不是 `QVariant &`，而是一个保存 iterator 位置的间接代理：

```cpp
auto it = view.mutableBegin();
QVariantRef<QSequentialIterator> reference = *it;
reference = QVariant(42);
```

赋值时会尝试把右侧值转换为真实元素类型，再调用元容器的 `setValueAtIterator()`。如果底层容器没有可写 iterator 能力，不能把代理赋值当作可靠写入。

### 6.3 `operator->()` 不是元素指针

`QSequentialIterator::operator->()` 返回 `QVariantPointer<QSequentialIterator>`；`QSequentialConstIterator::operator->()` 返回 `QVariantConstPointer`。这两个类型都是间接访问辅助对象：

```text
iterator
  -> QVariantPointer
      -> QVariantRef
          -> QVariant
```

它们都不是 `T *`，不会让调用方取得真实元素地址，也不应保存为跨修改操作的长期指针。

## 7. 迭代器能力和随机访问边界

类中提供了多组带标准 iterator tag 的类型别名：

```cpp
using InputIterator = ...;
using ForwardIterator = ...;
using BidirectionalIterator = ...;
using RandomAccessIterator = ...;
```

但这些别名本身不是对每个底层容器能力的承诺。真正的能力来自 `QMetaSequence` 描述器，使用前应查询：

```cpp
view.canInputIterate();
view.canForwardIterate();
view.canReverseIterate();
view.canRandomAccessIterate();
```

尤其要注意：Qt 6.11.1 头文件明确把 `QSequentialIterable::canRandomAccessIterate()` 实现为：

```cpp
constexpr bool canRandomAccessIterate() const { return false; }
```

头文件还说明 `QSequentialIterator` 的随机访问存在问题，这也是旧类进入弃用路径的原因之一。因此：

- 不要把 `RandomAccessIterator` 别名理解成旧类真的支持可靠随机访问；
- 不要在没有确认能力时使用 `operator[]`、`operator+`、`operator-` 或距离运算；
- 新代码使用 `QMetaSequence::Iterable`，其 iterator 能力由现代元容器描述器直接检查；
- 只需要顺序遍历时，使用 `++it` 是最稳妥的路径。

## 8. 索引访问：`at()` 的语义和边界

### 8.1 `at(qsizetype index)`

```cpp
QVariant at(qsizetype index) const;
```

它按索引读取元素，并返回一个 `QVariant` 值。底层优先使用 `QMetaSequence::valueAtIndex()`；如果没有原生索引读取能力，Qt 6.11 兼容路径可能从 const begin 开始前进 `index` 步，再读取当前元素。

因此不能把它无条件当作 O(1)：

- 原生索引访问通常更直接；
- 没有原生索引能力时可能是线性前进；
- 兼容路径可能触发 synthesized access 警告；
- 负索引和越界索引没有可依赖的业务语义；
- 无效索引不要通过“返回空 QVariant”猜测是否失败，因为元素类型本身也可能有默认值或无效状态。

通用代码应先取得：

```cpp
const qsizetype count = view.size();
if (count >= 0 && index >= 0 && index < count)
    value = view.at(index);
```

如果 `size()` 返回负值，表示无法得到可靠的数量，不应把它转换成无符号整数。

### 8.2 `set()` 不应再使用

Qt 6.11.1 的现代 `QMetaSequence::Iterable` 已将旧的 `set(index, value)` 声明为删除式接口，并要求使用：

```cpp
setAt(index, value);
```

`QSequentialIterable` 的旧模板稿若把 `set()` 列成可调用 API，不能作为 Qt 6.11.1 的准确说明。迁移时直接改为：

```cpp
QMetaSequence::Iterable modernView(
    QMetaSequence::fromContainer<QList<int>>(),
    &values);
modernView.setAt(index, value);
```

## 9. 旧式首尾修改 API

### 9.1 `Position`

```cpp
enum Position {
    Unspecified,
    AtBegin,
    AtEnd
};
```

该枚举在 Qt 6.11 已进入弃用路径。它把“添加或删除的位置”塞进一个可选参数，导致 `Unspecified` 的实际动作还要依赖元容器是否提供通用 `addValue` / `removeValue` 函数。

新代码应让操作名称直接表达位置：

```text
append()     -> 尾部添加
prepend()    -> 头部添加
removeLast() -> 尾部删除
removeFirst()-> 头部删除
```

### 9.2 `addValue(const QVariant &, Position)`

```cpp
void addValue(const QVariant &value,
              Position position = Unspecified);
```

Qt 6.11 起 deprecated。实现逻辑按位置选择底层能力：

| position | 底层能力 | 行为 |
| --- | --- | --- |
| `AtBegin` | `canAddValueAtBegin()` | 能力存在时在头部添加 |
| `AtEnd` | `canAddValueAtEnd()` | 能力存在时在尾部添加 |
| `Unspecified` | `canAddValue()` | 能力存在时调用通用添加 |

这个函数返回 `void`，没有“添加成功/失败”的返回值。缺少相应能力时，调用可能什么也不做。因此通用代码必须在调用前自行检查能力，并且要处理 `QVariant` 到元素类型的转换。

### 9.3 `removeValue(Position)`

```cpp
void removeValue(Position position = Unspecified);
```

Qt 6.11 起 deprecated。实现逻辑按位置选择：

| position | 底层能力 | 行为 |
| --- | --- | --- |
| `AtBegin` | `canRemoveValueAtBegin()` | 能力存在时删除第一个元素 |
| `AtEnd` | `canRemoveValueAtEnd()` | 能力存在时删除最后一个元素 |
| `Unspecified` | `canRemoveValue()` | 能力存在时调用通用删除 |

它同样没有成功状态返回值。空容器上删除是否安全由真实容器的操作契约决定，不能因为函数签名允许调用就认为空容器也安全。

## 10. `valueMetaType()` 和现代替代

### 10.1 `valueMetaType() const`

```cpp
QMetaType valueMetaType() const;
```

Qt 6.11 起 deprecated。它返回序列元素的 `QMetaType`，不是容器本身的元类型，也不是某个元素的 `QVariant` 实例。

旧代码：

```cpp
const QMetaType elementType = view.valueMetaType();
```

现代写法：

```cpp
const QMetaType elementType =
    view.metaContainer().valueMetaType();
```

### 10.2 用它检查 QVariant 转换

```cpp
const QMetaType elementType =
    view.metaContainer().valueMetaType();

QVariant input = 42;
if (input.canConvert(elementType)) {
    // 旧 API 没有错误返回值，至少先验证转换能力。
    view.addValue(input, QSequentialIterable::AtEnd);
}
```

这段代码仅适合维护旧接口。新代码应改用现代 `append()`，并同时检查 `canAddValueAtEnd()`。

## 11. 构造函数逐项语义

### 11.1 `QSequentialIterable()`

```cpp
QSequentialIterable();
```

构造空 view，内部没有有效 `QMetaSequence` 和真实容器指针。它适合表示“尚未绑定”的状态，不适合直接调用遍历、索引或修改 API。

### 11.2 `QSequentialIterable(const T *p)`

```cpp
template <class T>
QSequentialIterable(const T *p);
```

根据 `T` 创建 `QMetaSequence`，并保存只读的真实容器指针。`p` 必须指向与 `T` 对应的活对象，且该对象在所有使用期间保持不变或遵守真实容器的 iterator 规则。

### 11.3 `QSequentialIterable(T *p)`

```cpp
template <class T>
QSequentialIterable(T *p);
```

根据 `T` 创建 `QMetaSequence`，并保存可写的真实容器指针。它不取得所有权，也不保证底层一定提供 setter、append 或 erase 能力。

### 11.4 `QSequentialIterable(const QMetaSequence &, Pointer)`

```cpp
template <typename Pointer>
QSequentialIterable(const QMetaSequence &metaSequence,
                    Pointer iterable);
```

使用显式元描述器和指针创建 view。`metaSequence` 必须与指针实际指向的容器类型匹配。错误的描述器不会被编译器自动纠正，可能在 iterator 创建或元素访问时产生未定义行为。

### 11.5 带 `QMetaType` 的擦除指针构造

```cpp
QSequentialIterable(const QMetaSequence &metaSequence,
                    const QMetaType &metaType,
                    void *iterable);

QSequentialIterable(const QMetaSequence &metaSequence,
                    const QMetaType &metaType,
                    const void *iterable);
```

这些构造函数主要供元类型和类型擦除桥接使用。`metaType` 用于取得对齐信息，必须描述真实容器类型，而不是元素类型。普通业务代码优先使用模板指针构造。

### 11.6 从 `QIterable<QMetaSequence>` 移动构造和赋值

```cpp
QSequentialIterable(QIterable<QMetaSequence> &&other);

QSequentialIterable &operator=(
    QIterable<QMetaSequence> &&other);
```

它们把底层 iterable 的元描述器和借用指针移动到旧式顺序 view 中。移动不会转移真实容器所有权，也不会复制真实容器；移动后原 iterable 不应再被当作有效 view 使用。

## 12. 迭代器入口逐项语义

### 12.1 `begin()` 和 `end()`

```cpp
const_iterator begin() const;
const_iterator end() const;
```

这两个函数返回只读旧式 iterator，等价于 `constBegin()` 和 `constEnd()`。`end()` 只用于比较，不能解引用。

### 12.2 `constBegin()` 和 `constEnd()`

```cpp
const_iterator constBegin() const;
const_iterator constEnd() const;
```

通过 `QIterable<QMetaSequence>` 创建擦除后的 const iterator，并包装成 `QSequentialConstIterator`。底层容器结构改变后，它们返回的旧 iterator 可能失效。

### 12.3 `mutableBegin()` 和 `mutableEnd()`

```cpp
iterator mutableBegin();
iterator mutableEnd();
```

创建可写旧式 iterator。view 必须保留可写容器指针，且元容器必须支持可写 iterator。`mutableEnd()` 仍然只是边界位置，不能解引用。

## 13. 相关旧式 iterator 的逐项语义

### 13.1 `QSequentialIterator::operator*()`

```cpp
QVariantRef<QSequentialIterator> operator*() const;
```

返回当前元素的旧式可写代理。它通过 iterator 位置读取元素，赋值时再把 `QVariant` 转换并写回。代理不能脱离 iterator、view 和真实容器长期保存。

### 13.2 `QSequentialIterator::operator->()`

```cpp
QVariantPointer<QSequentialIterator> operator->() const;
```

返回旧式指针式代理，而不是元素地址。它的 `operator*()` 仍然得到 `QVariantRef`，`operator->()` 也不能用于调用真实元素类型的成员函数。

### 13.3 `QSequentialConstIterator::operator*()`

```cpp
QVariant operator*() const;
```

返回当前元素的 `QVariant` 值。它不提供回写通道，修改返回值不会改变容器。

### 13.4 `QSequentialConstIterator::operator->()`

```cpp
QVariantConstPointer operator->() const;
```

返回只读 `QVariant` 指针辅助对象。它依赖当前 iterator 的位置，不能在容器修改后继续保存或使用。

## 14. 从 QVariant 获取顺序 iterable 时的版本边界

Qt 6.11.1 的 `qmetatype.h` 中，顺序容器的通用 converter 和 mutable view 注册目标是：

```cpp
QIterable<QMetaSequence>
```

而现代代码中的 `QMetaSequence::Iterable` 就是这个元容器 iterable 的具体接口。因此新代码应使用：

```cpp
QVariant value = QVariant::fromValue(QList<int>{1, 2, 3});

if (value.canConvert<QMetaSequence::Iterable>()) {
    const auto view = value.value<QMetaSequence::Iterable>();
    for (const QVariant element : view)
        qDebug() << element;
}
```

不要在 Qt 6.11.1 的新代码里假设：

```cpp
value.value<QSequentialIterable>()
```

一定是公开注册路径。`QSequentialIterable` 是旧兼容类；即使某个旧项目曾这样使用，也应把迁移目标改成 `QMetaSequence::Iterable`，并重新检查 view 的所有权和可写性。

## 15. 与 `QMetaSequence::Iterable` 的迁移对照

| 旧式接口 | 现代接口 | 迁移重点 |
| --- | --- | --- |
| `QSequentialIterable` | `QMetaSequence::Iterable` | 不再把旧兼容类作为新公共 API |
| `QSequentialIterable::iterator` | `QMetaSequence::Iterable::Iterator` | 旧 iterator 使用 `QVariantRef`，新 iterator 使用 `QVariant::Reference` |
| `QSequentialIterable::const_iterator` | `QMetaSequence::Iterable::ConstIterator` | 新 const iterator 采用现代 `QVariant` 代理体系 |
| `at(index)` | `at(index)` | 都要处理索引范围和无原生索引时的合成访问 |
| `set(index, value)` | `setAt(index, value)` | Qt 6.11 的旧 `set()` 不应再调用 |
| `addValue(value, AtEnd)` | `append(value)` | 先检查 `canAddValueAtEnd()` |
| `addValue(value, AtBegin)` | `prepend(value)` | 先检查 `canAddValueAtBegin()` |
| `removeValue(AtEnd)` | `removeLast()` | 空容器和 iterator 失效规则仍由真实容器决定 |
| `removeValue(AtBegin)` | `removeFirst()` | 不要在旧 iterator 上继续遍历 |
| `valueMetaType()` | `metaContainer().valueMetaType()` | 元素类型来自 `QMetaSequence` 描述器 |

迁移示例：

```cpp
QList<int> values{1, 2, 3};

QMetaSequence::Iterable view(
    QMetaSequence::fromContainer<QList<int>>(),
    &values);

view.setAt(0, QVariant(10));
view.append(QVariant(4));
view.prepend(QVariant(0));
view.removeLast();
```

## 16. 常见错误

### 16.1 把 view 当成容器副本

**问题：** 原容器销毁后仍使用 `QSequentialIterable`。

**原因：** view 只保存借用指针。

**处理：** 让真实容器覆盖 view 和 iterator 的完整生命周期；需要脱离源对象时创建 `QList<QVariant>` 等真正快照。

### 16.2 以为 `operator->()` 返回 `T *`

**问题：** 试图通过 `it->someMember()` 调用真实元素类型的成员函数。

**原因：** `QVariantPointer` 是代理，不是元素地址。

**处理：** 先把元素取成 `QVariant`，或者改用已知具体容器和原生 iterator。

### 16.3 以为 `RandomAccessIterator` 别名保证随机访问

**问题：** 对旧类使用 `operator[]` 或距离运算。

**原因：** 类型别名存在不等于底层容器提供对应能力，且 Qt 6.11 旧类明确把 `canRandomAccessIterate()` 返回为 false。

**处理：** 只使用顺序递增；需要随机访问时迁移到 `QMetaSequence::Iterable` 并检查元容器能力。

### 16.4 忽略 `QVariant` 到元素类型的转换

**问题：** `addValue()` 或 iterator 赋值没有得到预期结果。

**原因：** 右值类型不能转换成元容器的元素类型，旧 API 又没有失败返回值。

**处理：** 用 `view.metaContainer().valueMetaType()` 检查目标类型和 `QVariant::canConvert()`，并在新代码中使用现代 API。

### 16.5 把 `Unspecified` 当成固定的尾部操作

**问题：** 旧的 `addValue(value)` 在不同容器或注册方式下行为不一致。

**原因：** `Unspecified` 调用通用 `canAddValue()` / `addValue()`，不等于 `AtEnd`。

**处理：** 旧代码明确传 `AtBegin` 或 `AtEnd`；新代码用 `prepend()` 或 `append()`。

### 16.6 空容器上调用删除

**问题：** `removeValue()`、`removeFirst()` 或 `removeLast()` 触发底层错误。

**原因：** 删除 API 没有统一的失败返回值，空容器边界由真实容器决定。

**处理：** 先取得可靠的 `size()`，或由具体元容器契约保证非空。

### 16.7 用旧 `set()` 作为 Qt 6.11 API

**问题：** 编译时遇到 deleted function 或弃用诊断。

**原因：** 现代 `QMetaSequence::Iterable` 已用 `setAt()` 替代 `set()`。

**处理：** 迁移到 `QMetaSequence::Iterable::setAt()`。

## API 速查表
### 17.1 构造和 view

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QSequentialIterable()` | 构造空 view | 没有有效容器；不要直接遍历或修改 |
| `QSequentialIterable(const T *)` | 构造只读顺序 view | 不复制容器；保留 const 资格 |
| `QSequentialIterable(T *)` | 构造可写顺序 view | 不拥有容器；可写能力仍由元容器决定 |
| `QSequentialIterable(const QMetaSequence &, Pointer)` | 用显式元描述器和指针构造 | `Pointer` 的真实容器类型必须和描述器匹配 |
| `QSequentialIterable(const QMetaSequence &, const QMetaType &, void *)` | 用可写擦除地址构造 | 对齐信息和容器元类型必须准确 |
| `QSequentialIterable(const QMetaSequence &, const QMetaType &, const void *)` | 用只读擦除地址构造 | 只能走 const 访问路径 |
| `QSequentialIterable(QIterable<QMetaSequence> &&)` | 从底层 iterable 移动构造 | 只移动 view 状态，不转移真实容器所有权 |
| `operator=(QIterable<QMetaSequence> &&)` | 从底层 iterable 移动赋值 | 覆盖当前 view；原 view 不再作为有效入口使用 |

### 17.2 遍历和元素访问

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `begin()` | 返回只读 begin iterator | 等价于 `constBegin()`；iterator 依赖 view |
| `end()` | 返回只读 end iterator | 只能比较，不能解引用 |
| `constBegin()` | 创建只读起点 | 底层容器必须存活 |
| `constEnd()` | 创建只读终点 | 只能和同一 view 的 iterator 比较 |
| `mutableBegin()` | 创建可写起点 | 需要非 const view 和 mutable iterator 能力 |
| `mutableEnd()` | 创建可写终点 | end 不能解引用 |
| `at(qsizetype)` | 按索引读取元素 | 越界和负索引不应依赖；无原生索引时可能线性 |
| `QSequentialIterator::operator*()` | 返回旧式可写 `QVariantRef` | 代理赋值会尝试转换并写回 |
| `QSequentialIterator::operator->()` | 返回旧式 `QVariantPointer` | 不是真实元素指针 |
| `QSequentialConstIterator::operator*()` | 返回 `QVariant` 值 | 修改返回值不会回写 |
| `QSequentialConstIterator::operator->()` | 返回只读 `QVariantConstPointer` | 不能修改真实元素 |

### 17.3 旧式修改接口

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `Position::Unspecified` | 使用通用添加或删除能力 | 不等于尾部操作；迁移后不要再使用 |
| `Position::AtBegin` | 选择头部操作 | 需要对应 begin 能力 |
| `Position::AtEnd` | 选择尾部操作 | 需要对应 end 能力 |
| `addValue(value, position)` | 旧式添加 | Qt 6.11 起 deprecated；无成功返回值 |
| `removeValue(position)` | 旧式删除 | Qt 6.11 起 deprecated；空容器边界由底层决定 |
| `valueMetaType()` | 返回元素 `QMetaType` | Qt 6.11 起 deprecated，改用 `metaContainer().valueMetaType()` |
| `set(index, value)` | 旧式索引写入名称 | Qt 6.11 现代接口中应使用 `setAt()`；不要把它当有效新 API |

### 17.4 继承自 `QIterable` 的常用 API

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `canInputIterate()` | 查询 input iterator 能力 | 只保证基本单向遍历 |
| `canForwardIterate()` | 查询 forward iterator 能力 | 不保证后退或随机访问 |
| `canReverseIterate()` | 查询双向迭代能力 | 允许后退，不代表有独立 reverse view |
| `canRandomAccessIterate()` | 查询随机访问能力 | 对本旧类在 Qt 6.11 明确返回 false |
| `size()` | 取得容器大小 | 可能使用合成访问；负值不能转无符号 |
| `clear()` | 清空真实容器 | 需要可写 view；旧 iterator 通常失效 |
| `metaContainer()` | 返回 `QMetaSequence` 描述器副本 | 不返回真实容器，不拥有元素 |
| `constIterable()` | 取得只读擦除容器指针 | 主要供框架层使用 |
| `mutableIterable()` | 取得可写擦除容器指针 | 只对可写 view 有效；不要传给错误描述器 |

## 18. 一句话总结

`QSequentialIterable` 是 Qt 旧式顺序容器反射的借用视图：它把真实容器包装成 `QVariant` 元素的只读或可写 range，但不拥有容器，旧 iterator 和代理也不能脱离 view 独立存在。Qt 6.11.1 中它已进入迁移阶段，维护旧代码时要特别注意 `QVariant` 转换、`Unspecified` 语义、随机访问失效和 iterator 生命周期；新代码直接使用 `QMetaSequence::Iterable`。
