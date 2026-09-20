# Qt QMetaAssociation 关联容器反射笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QMetaAssociation>`  
> 所属模块：`Qt6::Core`  
> 继承：`QMetaContainer`  
> 类型性质：描述关联容器操作的轻量元对象描述器  
> 相关类型：`QMetaAssociation::Iterable`、`QMetaSequence`、`QMetaContainer`、`QMetaType`、`QVariant`、`QMap`、`QHash`

## 1. 它解决什么问题

`QMetaAssociation` 不是一个保存键值对的容器，而是一个“如何通过类型擦除方式操作关联容器”的运行时描述器。它把某个 C++ 关联容器的能力记录成一组元操作：

```text
具体容器类型
QMap<QString, int> / QHash<int, QByteArray> / 其他可识别关联容器
        |
        | QMetaAssociation::fromContainer<T>()
        v
QMetaAssociation
        |
        | 运行时函数表 + key/mapped 的 QMetaType
        v
QMetaAssociation::Iterable
        |
        v
通过 QVariant 读取、查找、插入、修改和遍历
```

它主要解决：

- 编译时不知道具体关联容器类型，但运行时仍要访问它；
- 元对象、属性编辑器、脚本桥接、通用调试器需要统一处理 `QMap`、`QHash` 等键值容器；
- 需要把键和值转换为 `QVariant`，在运行时进行查找和修改；
- 需要按底层容器实际能力决定是否支持 `find`、删除、写入、迭代和随机访问。

最常见的现代使用入口不是直接调用一堆 `void *` API，而是：

```cpp
QMetaAssociation meta =
    QMetaAssociation::fromContainer<QMap<QString, int>>();
QMetaAssociation::Iterable iterable(meta, &map);
```

随后使用 `iterable.find()`、`iterable.value()` 或迭代器。

### 1.1 它不是什么

`QMetaAssociation` 不是：

- `QMap` 或 `QHash` 的替代品；
- 真实容器对象的拥有者；
- 容器数据的快照；
- 自动把任意 C++ 类识别成关联容器的运行时扫描器；
- 保证所有操作都可用的接口；
- 负责管理 `void *` 指向对象生命周期的智能指针。

`QMetaAssociation` 保存的是静态描述和函数指针。实际键值数据仍属于传入的容器对象，容器必须在所有操作和迭代器存活期间保持有效。

## 2. 实际使用场景

### 2.1 运行时遍历未知关联容器

```cpp
QMap<QString, int> values{
    {QStringLiteral("red"), 1},
    {QStringLiteral("blue"), 2}
};

const QMetaAssociation meta =
    QMetaAssociation::fromContainer<QMap<QString, int>>();
const QMetaAssociation::Iterable iterable(meta, &values);

for (auto it = iterable.constBegin();
     it != iterable.constEnd(); ++it) {
    qDebug() << it.key() << it.value();
}
```

这里的代码可以用统一的 `QVariant` 结果访问键和值，而不需要在通用逻辑中写死 `QMap<QString, int>`。

### 2.2 元数据驱动的键查找

```cpp
const QVariant key = QStringLiteral("blue");
const auto it = iterable.find(key);

if (it != iterable.constEnd())
    qDebug() << "value:" << it.value();
```

`find()` 会根据 `keyMetaType()` 尝试把 `QVariant` 转成底层键类型。查找失败有两种不同原因：

- key 不存在；
- key 无法转换成底层键类型。

使用 `containsKey()` 或先检查 `QVariant::canConvert()` 时，要在业务层区分这两类情况。

### 2.3 在运行时修改关联容器

```cpp
QMap<QString, int> values;
QMetaAssociation::Iterable iterable(
    QMetaAssociation::fromContainer<QMap<QString, int>>(),
    &values);

iterable.insertKey(QStringLiteral("count"));
iterable.setValue(QStringLiteral("count"), 42);
iterable.removeKey(QStringLiteral("obsolete"));
```

可写操作要求：

- iterable 由非 const 容器指针构造；
- 底层元容器确实提供相应能力；
- `QVariant` 能转换成 key 或 mapped 类型；
- 修改期间没有其他 iterator 或引用违反底层容器的失效规则。

### 2.4 编写通用属性或调试工具

工具可以接受一个已经注册或已知类型的容器地址，再通过 `QMetaAssociation` 查询：

```cpp
const QMetaType keyType = meta.keyMetaType();
const QMetaType valueType = meta.mappedMetaType();

qDebug() << keyType.name() << valueType.name();
```

这样可以在不依赖具体模板参数的情况下显示键和值的元类型。工具仍需明确对象所有权、线程归属和是否允许修改。

### 2.5 适配 QVariant 中的关联容器

旧式 `QAssociativeIterable` 常用于从 `QVariant` 访问未知关联容器；Qt 6.11 的方向是使用 `QMetaAssociation::Iterable` 及其迭代器。迁移时不要只改类名，还要重新确认：

- 如何取得真实容器地址；
- iterable 是否只读；
- key/value 的 `QVariant` 转换；
- iterator 的生命周期；
- Qt 6.15 计划弃用的旧接口是否仍被项目依赖。

## 3. 构建与包含

### 3.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

### 3.2 头文件

```cpp
#include <QMetaAssociation>
#include <QMetaType>
#include <QVariant>
#include <QMap>
#include <QDebug>
```

`QMetaAssociation` 位于 `Qt6::Core`。直接使用 `QMetaAssociation::Iterable` 时，`QMetaAssociation` 头文件会提供相关定义；业务代码仍应为具体容器和输出类型包含所需头文件。

## 4. 描述器、真实容器和 Iterable 的三层关系

### 4.1 `QMetaAssociation` 只描述能力

```cpp
const QMetaAssociation meta =
    QMetaAssociation::fromContainer<QMap<QString, int>>();
```

`meta` 不包含 `QMap` 的任何元素。它记录：

- key 的 `QMetaType`；
- mapped 的 `QMetaType`；
- 是否支持插入、删除、包含判断；
- 是否能按 key 读取或设置 mapped；
- 是否能按 key 创建 iterator；
- 是否能从 iterator 读取 key/mapped；
- 是否能通过 iterator 修改或删除。

### 4.2 `Iterable` 借用真实容器

```cpp
QMap<QString, int> map;
QMetaAssociation::Iterable iterable(meta, &map);
```

`iterable` 保存一个指向 `map` 的借用指针，不复制 `map`。因此：

- `map` 必须比 `iterable` 和它创建的 iterator 活得久；
- 不能把指向局部容器的 iterable 返回到局部容器之外；
- 修改或销毁 `map` 后，旧 iterable/iterator 不能继续使用；
- `iterable` 的析构不会销毁 `map`。

### 4.3 原始 `void *` API 适合元容器适配层

`QMetaAssociation` 的底层成员使用：

```cpp
const void *container;
void *container;
const void *key;
void *mapped;
const void *iterator;
```

这些参数必须准确匹配 `fromContainer<T>()` 对应的实际类型和可写性。普通业务代码若直接使用它们，必须自行负责：

- 地址指向正确的 `T`；
- 对齐满足 `T`；
- 输出存储已经构造；
- iterator 由同一个 `QMetaAssociation` 创建和销毁；
- 所有操作发生在对象生命周期内。

如果不需要实现底层适配，优先使用 `QMetaAssociation::Iterable`。

## 5. 从容器建立描述器

### 5.1 `fromContainer<T>()`

```cpp
template <typename T>
static constexpr QMetaAssociation fromContainer();
```

从编译期容器类型 `T` 创建描述器：

```cpp
using Map = QMap<QString, int>;
constexpr QMetaAssociation meta =
    QMetaAssociation::fromContainer<Map>();
```

Qt 通过容器信息 traits 检查 `T` 是否具有 key 类型、mapped 类型以及相关成员操作。它不是运行时反射任意类；如果 `T` 不满足 Qt 能识别的关联容器形状，返回的描述器可能缺少能力，或在编译期无法实例化。

### 5.2 key 和 mapped 必须有元类型接口

```cpp
const QMetaType keyType = meta.keyMetaType();
const QMetaType mappedType = meta.mappedMetaType();
```

元容器描述器需要为 key 和 mapped 建立 `QMetaType` 接口。自定义类型通常需要先注册或满足 Qt 元类型要求，才能可靠地通过 `QVariant` 在 `Iterable` 中读写。

### 5.3 同一类型的描述器可比较

```cpp
const auto a =
    QMetaAssociation::fromContainer<QMap<QString, int>>();
const auto b =
    QMetaAssociation::fromContainer<QMap<QString, int>>();

Q_ASSERT(a == b);
```

描述器相等比较的是内部静态接口地址，而不是两个真实容器的元素是否相同。两个同类型描述器通常相等；不同容器类型即使 key/value 类型相同，也不要假定描述器相等。

### 5.4 默认构造产生无效描述器

```cpp
const QMetaAssociation invalid;
Q_ASSERT(invalid.keyMetaType() == QMetaType());
```

默认对象不描述任何容器。对它进行能力查询会得到 `false`，读取元类型会得到无效类型，操作不会产生有效容器行为。把默认对象传给 `Iterable` 可以形成空视图，但不能把它当成空的 `QMap`。

## 6. 能力查询是使用前置条件

`QMetaAssociation` 的 API 不承诺所有操作都可用。每个能力查询对应一个函数表槽位是否存在；在调用前检查它们是类型擦除代码的核心步骤。

| 能力 | 对应操作 |
| --- | --- |
| `canInsertKey()` | `insertKey()` |
| `canRemoveKey()` | `removeKey()` |
| `canContainsKey()` | `containsKey()` |
| `canGetMappedAtKey()` | `mappedAtKey()` |
| `canSetMappedAtKey()` | `setMappedAtKey()` |
| `canGetKeyAtIterator()` | `keyAtIterator()` |
| `canGetKeyAtConstIterator()` | `keyAtConstIterator()` |
| `canGetMappedAtIterator()` | `mappedAtIterator()` |
| `canGetMappedAtConstIterator()` | `mappedAtConstIterator()` |
| `canSetMappedAtIterator()` | `setMappedAtIterator()` |
| `canCreateIteratorAtKey()` | `createIteratorAtKey()` |
| `canCreateConstIteratorAtKey()` | `createConstIteratorAtKey()` |

头文件中的操作函数在能力不存在时通常直接不调用函数指针：写入操作无效返回，读取输出不会得到可靠的新值，iterator 创建返回 `nullptr`。因此不能跳过能力检查后再根据“看起来没有崩溃”判断调用成功。

## 7. key/mapped 访问的语义边界

### 7.1 `keyMetaType()` 和 `mappedMetaType()`

```cpp
QMetaType keyMetaType() const;
QMetaType mappedMetaType() const;
```

分别返回键和值的元类型。它们用于：

- 构造适合输出的 `QVariant`；
- 检查 `QVariant` 是否可转换；
- 了解 `void *` 输入和输出应指向的实际类型；
- 构造通用属性编辑器或脚本桥接层。

无效描述器或无法提供元类型的容器可能返回无效 `QMetaType`。

### 7.2 `mappedAtKey()` 不是统一的“安全查找”

```cpp
meta.mappedAtKey(container, key, mapped);
```

它只表示“调用底层描述器提供的按 key 读取函数”。底层函数可能来自：

- 容器的 `at(key)`；
- 容器的下标访问 `operator[](key)` 的 const 形式。

因此调用方应先确认 key 是否存在，尤其是自己实现或适配的容器。不能假定所有底层容器都对缺失 key 返回同样的结果，也不能把它当作带 `std::optional` 的查找 API。

### 7.3 `setMappedAtKey()` 可能插入缺失 key

```cpp
meta.setMappedAtKey(container, key, mapped);
```

Qt 通过可写下标访问适配这类操作时，缺失 key 可能被创建并赋值。若业务要求“只更新已有项”，先调用 `containsKey()` 或使用 `Iterable::mutableFind()` 检查，再修改 iterator 指向的项。

### 7.4 `insertKey()` 的 mapped 初值由适配规则决定

`insertKey()` 会使用底层容器支持的插入方式，并在需要 mapped 值时提供默认构造的 mapped 对象：

```cpp
iterable.insertKey(key);
```

它不是“只预留一个 key 的空槽”抽象。是否允许重复 key、重复插入的结果以及 mapped 默认值，仍由底层容器类型决定：

- `QMap` 通常保持唯一 key；
- 多值关联容器可能允许多个相同 key；
- 自定义容器的插入规则由其成员函数决定。

### 7.5 `removeKey()` 的删除粒度由底层容器决定

`removeKey()` 通过底层 `erase(key)` 或 `remove(key)` 适配。对于唯一 key 容器通常删除一个条目；对于多值容器可能删除同 key 的多个条目，不能只根据函数名猜测数量。

## 8. 逐项成员 API：元类型与插入删除

### 8.1 `keyMetaType() const`

```cpp
QMetaType keyMetaType() const;
```

返回关联容器 key 的 `QMetaType`。它不返回某个具体 key 值，也不检查真实容器当前是否为空。

### 8.2 `mappedMetaType() const`

```cpp
QMetaType mappedMetaType() const;
```

返回关联容器 mapped 值的 `QMetaType`。它描述值的类型，不返回当前值。

### 8.3 `canInsertKey() const`

```cpp
bool canInsertKey() const;
```

报告描述器是否有按 key 插入函数。检查通过后才能可靠调用 `insertKey()`：

```cpp
if (meta.canInsertKey())
    meta.insertKey(&map, &key);
```

### 8.4 `insertKey(void *, const void *) const`

```cpp
void insertKey(void *container,
               const void *key) const;
```

按底层关联容器的插入规则插入 key。`container` 必须指向与 `fromContainer<T>()` 匹配的可写 `T`，`key` 必须指向已构造的 `T::key_type`：

```cpp
QMap<QString, int> map;
QString key = QStringLiteral("count");
meta.insertKey(&map, &key);
```

如果不支持插入，该调用不执行底层函数。插入是否覆盖、是否允许重复和 mapped 初值由容器适配规则决定。

### 8.5 `canRemoveKey() const`

```cpp
bool canRemoveKey() const;
```

报告是否有按 key 删除函数。它不表示 key 一定存在，也不表示删除后一定只影响一个元素。

### 8.6 `removeKey(void *, const void *) const`

```cpp
void removeKey(void *container,
               const void *key) const;
```

按 key 删除元素。调用前应确认容器可写和 key 存储类型正确。不存在的 key 通常不会改变容器，但具体结果仍由底层 `erase` 或 `remove` 语义决定。

### 8.7 `canContainsKey() const`

```cpp
bool canContainsKey() const;
```

报告是否能够判断 key 是否存在。底层可能使用 `contains()`，也可能使用 `find() != end()` 合成。

### 8.8 `containsKey(const void *, const void *) const`

```cpp
bool containsKey(const void *container,
                 const void *key) const;
```

判断 key 是否存在：

```cpp
if (meta.canContainsKey() &&
    meta.containsKey(&map, &key)) {
    // key 已存在
}
```

不支持该能力时返回 `false`，因此“返回 false”不能区分“不存在”和“描述器没有 contains 能力”。通用代码如需区分，应先检查 `canContainsKey()`。

## 9. 逐项成员 API：按 key 读取和修改 mapped

### 9.1 `canGetMappedAtKey() const`

```cpp
bool canGetMappedAtKey() const;
```

报告是否有按 key 读取 mapped 的函数。它只报告操作存在，不保证给定 key 在容器中存在。

### 9.2 `mappedAtKey(const void *, const void *, void *) const`

```cpp
void mappedAtKey(const void *container,
                 const void *key,
                 void *mapped) const;
```

读取指定 key 对应的 mapped 值，并写入调用方提供的 mapped 存储：

```cpp
int result = 0;
if (meta.canGetMappedAtKey())
    meta.mappedAtKey(&map, &key, &result);
```

注意：

- `mapped` 必须指向已构造、可写的 `mapped_type` 存储；
- 调用方需要先确认 key 存在，避免依赖缺失 key 的底层差异；
- 不支持时函数不会写入可靠结果；
- 这不是返回 `QVariant` 的 API，类型和生命周期由调用方负责。

### 9.3 `canSetMappedAtKey() const`

```cpp
bool canSetMappedAtKey() const;
```

报告是否能通过 key 设置 mapped。它通常要求底层容器支持可写下标或等价的按 key 更新操作。

### 9.4 `setMappedAtKey(void *, const void *, const void *) const`

```cpp
void setMappedAtKey(void *container,
                    const void *key,
                    const void *mapped) const;
```

按 key 写入 mapped：

```cpp
int value = 42;
if (meta.canSetMappedAtKey())
    meta.setMappedAtKey(&map, &key, &value);
```

`mapped` 指向只读输入值，函数会把它复制或赋值到容器。缺失 key 是否插入取决于底层操作，不能把它统一解释成“仅更新”。

## 10. 逐项成员 API：iterator 访问

### 10.1 `canGetKeyAtIterator() const`

```cpp
bool canGetKeyAtIterator() const;
```

报告是否能从可写 iterator 读取 key。key 输出仍然是复制到调用方存储，不是返回对 key 的长期引用。

### 10.2 `keyAtIterator(const void *, void *) const`

```cpp
void keyAtIterator(const void *iterator,
                   void *key) const;
```

从可写 iterator 当前位置复制 key 到 `key` 存储。iterator 必须由同一描述器针对同一容器创建，并且不能位于 end 位置。

### 10.3 `canGetKeyAtConstIterator() const`

```cpp
bool canGetKeyAtConstIterator() const;
```

报告是否能从只读 iterator 读取 key。通用只读遍历通常优先依赖这个能力。

### 10.4 `keyAtConstIterator(const void *, void *) const`

```cpp
void keyAtConstIterator(const void *iterator,
                        void *key) const;
```

从只读 iterator 当前位置复制 key。它不会修改容器，也不会把 key 转换为 `QVariant`；转换由 `QMetaAssociation::Iterable` 的迭代器层完成。

### 10.5 `canGetMappedAtIterator() const`

```cpp
bool canGetMappedAtIterator() const;
```

报告是否能从可写 iterator 读取 mapped。

### 10.6 `mappedAtIterator(const void *, void *) const`

```cpp
void mappedAtIterator(const void *iterator,
                      void *mapped) const;
```

把可写 iterator 当前元素的 mapped 复制到调用方存储。iterator 不能是 end，也不能在底层容器修改后继续使用。

### 10.7 `canGetMappedAtConstIterator() const`

```cpp
bool canGetMappedAtConstIterator() const;
```

报告是否能从只读 iterator 读取 mapped。`QMetaAssociation::Iterable::ConstIterator::value()` 依赖这一类能力。

### 10.8 `mappedAtConstIterator(const void *, void *) const`

```cpp
void mappedAtConstIterator(const void *iterator,
                           void *mapped) const;
```

把只读 iterator 当前元素的 mapped 复制到调用方存储。它不修改容器。

### 10.9 `canSetMappedAtIterator() const`

```cpp
bool canSetMappedAtIterator() const;
```

报告是否能直接修改可写 iterator 当前元素的 mapped。并非所有关联容器的 iterator 都提供可写 mapped 引用。

### 10.10 `setMappedAtIterator(const void *, const void *) const`

```cpp
void setMappedAtIterator(const void *iterator,
                         const void *mapped) const;
```

把输入 mapped 赋给 iterator 当前元素：

```cpp
if (meta.canSetMappedAtIterator())
    meta.setMappedAtIterator(iterator, &newValue);
```

它要求 iterator 指向有效元素，而不是 end；底层 iterator 还必须允许修改 mapped。对于只读 iterable 或 const 容器，不能把此操作当成可写。

## 11. 逐项成员 API：按 key 创建 iterator

### 11.1 `canCreateIteratorAtKey() const`

```cpp
bool canCreateIteratorAtKey() const;
```

报告是否能针对可写容器创建 iterator。通常依赖底层容器有 `find()` 和可写 iterator。

### 11.2 `createIteratorAtKey(void *, const void *) const`

```cpp
void *createIteratorAtKey(void *container,
                          const void *key) const;
```

创建指向 key 查找结果的类型擦除 iterator。返回值由描述器分配，使用完成后必须调用：

```cpp
meta.destroyIterator(iterator);
```

特别注意：找不到 key 时，底层 `find()` 通常返回 end iterator，返回的指针本身仍可能非空。调用方必须用 `compareIterator(iterator, end)` 判断是否命中，不能只判断返回指针是否为空。

### 11.3 `canCreateConstIteratorAtKey() const`

```cpp
bool canCreateConstIteratorAtKey() const;
```

报告是否能针对 const 容器创建只读 iterator。

### 11.4 `createConstIteratorAtKey(const void *, const void *) const`

```cpp
void *createConstIteratorAtKey(const void *container,
                               const void *key) const;
```

创建只读查找 iterator。使用完成后必须用对应的：

```cpp
meta.destroyConstIterator(iterator);
```

不能用 `destroyIterator()` 销毁 const iterator，也不能把不同描述器创建的 iterator 混合比较或销毁。

## 12. `QMetaAssociation::Iterable`：推荐的高层入口

Qt 6.11 起，`QMetaAssociation::Iterable` 是现代关联容器反射入口。它建立在 `QIterable<QMetaAssociation>` 之上，负责把底层 `void *` 访问转换为 `QVariant` 和更易用的迭代器。

### 12.1 构造 `Iterable`

```cpp
QMap<QString, int> map;

QMetaAssociation::Iterable iterable(
    QMetaAssociation::fromContainer<QMap<QString, int>>(),
    &map);
```

也可以从指针直接构造：

```cpp
QMetaAssociation::Iterable iterable(&map);
```

这种构造会按 `T` 自动使用 `QMetaAssociation::fromContainer<T>()`。const 指针构造只产生只读视图：

```cpp
const QMap<QString, int> map;
QMetaAssociation::Iterable readOnly(&map);
```

视图不拥有 map，且 const 性会被保留。不要通过类型转换绕过只读约束。

### 12.2 `Iterator`、`ConstIterator` 和能力标签

`Iterable` 提供：

```cpp
using Iterator = ...;
using ConstIterator = ...;
using RandomAccessIterator = ...;
using BidirectionalIterator = ...;
using ForwardIterator = ...;
using InputIterator = ...;
```

这些类型把 `QIterator<QMetaAssociation>` 或 `QConstIterator<QMetaAssociation>` 包装成带 key/value 访问的迭代器。能力标签不是承诺所有关联容器都支持随机访问；构造带更强标签的 iterator 时，Qt 会检查底层 `QMetaContainer` 能力，不满足时会触发 fatal 路径。

普通代码用 `auto` 接收 `begin()`、`find()` 和 `mutableBegin()` 返回值，避免手写错误的迭代器标签类型。

### 12.3 `begin() const` 和 `end() const`

```cpp
ConstIterator begin() const;
ConstIterator end() const;
```

提供只读范围遍历：

```cpp
for (auto it = iterable.begin();
     it != iterable.end(); ++it) {
    const QVariant key = it.key();
    const QVariant value = it.value();
}
```

`end()` 只能用于比较，不能读取 key 或 value。两个 iterator 必须来自同一个 iterable 和同一个底层容器。

### 12.4 `constBegin()` 和 `constEnd()`

```cpp
ConstIterator constBegin() const;
ConstIterator constEnd() const;
```

与 `begin()`/`end()` 一样创建只读 iterator。显式写出 `constBegin()` 适合在同时存在 mutable API 时表达只读意图。

### 12.5 `mutableBegin()` 和 `mutableEnd()`

```cpp
Iterator mutableBegin();
Iterator mutableEnd();
```

创建可写 iterator：

```cpp
for (auto it = iterable.mutableBegin();
     it != iterable.mutableEnd(); ++it) {
    it.value() = QVariant(0);
}
```

真正能否赋值取决于 `canSetMappedAtIterator()` 和底层 iterator 的 mapped 写能力。`mutableBegin()` 需要 iterable 由可写容器构造；const iterable 不提供有效可写对象。

### 12.6 `find(const QVariant &) const`

```cpp
ConstIterator find(const QVariant &key) const;
```

把 `QVariant` key 转换为底层 key 类型后查找，并返回只读 iterator。转换失败时返回 `constEnd()`；key 不存在时同样返回 end，因此调用方只能通过额外的转换检查区分两种失败。

### 12.7 `constFind(const QVariant &) const`

```cpp
ConstIterator constFind(const QVariant &key) const;
```

是 `find()` 的只读命名形式，当前实现语义等同于 `find()`。它适合与 Qt 容器的 `constFind` 命名保持一致。

### 12.8 `mutableFind(const QVariant &)`

```cpp
Iterator mutableFind(const QVariant &key);
```

在可写视图中查找并返回可写 iterator。找不到时返回 `mutableEnd()`；它不会因为查找失败自动插入 key。

如果需要“找不到就插入”，应明确写出：

```cpp
auto it = iterable.mutableFind(key);
if (it == iterable.mutableEnd()) {
    iterable.insertKey(key);
    it = iterable.mutableFind(key);
}
```

插入后重新查找比保存旧 end 或假定 iterator 自动指向新元素更可靠。

### 12.9 `containsKey(const QVariant &) const`

```cpp
bool containsKey(const QVariant &key) const;
```

把 key 转换为底层 key 类型并查询存在性。转换失败和不存在都会返回 `false`；需要区分时先使用 `key.canConvert(meta.keyMetaType())`。

### 12.10 `insertKey(const QVariant &)`

```cpp
void insertKey(const QVariant &key);
```

把 QVariant key 转成底层 key 类型并插入。该方法不接收 mapped 值，mapped 通常使用底层适配提供的默认构造值。它需要可写 iterable 和底层 `canInsertKey()` 能力。

如果 key 转换失败或容器不支持插入，不应继续假设容器已改变。通用工具最好在调用前检查 key 类型和能力。

### 12.11 `removeKey(const QVariant &)`

```cpp
void removeKey(const QVariant &key);
```

转换 key 后调用底层删除操作。不存在的 key 通常不改变容器；多值关联容器的删除数量由底层 `remove`/`erase` 语义决定。

### 12.12 `value(const QVariant &) const`

```cpp
QVariant value(const QVariant &key) const;
```

按 key 读取 mapped，并包装成 `QVariant` 返回。结果的元类型通常是 `mappedMetaType()`。key 转换失败、底层不支持按 key 读取或 key 不存在时，不应把返回的默认/无效值简单当成业务上的合法 mapped；需要明确命中状态时，先调用 `containsKey()` 或 `find()`。

### 12.13 `setValue(const QVariant &, const QVariant &)`

```cpp
void setValue(const QVariant &key,
              const QVariant &mapped);
```

把 key 和 mapped 分别转换成底层类型后写入容器：

```cpp
iterable.setValue(QStringLiteral("count"), 42);
```

它可能通过下标写入缺失 key，因此可能同时具有“插入并赋值”的副作用。需要只更新已有项时，先 `mutableFind()`，再对 iterator 的 value 赋值。

## 13. 继承自 `QMetaContainer` 的通用能力

`QMetaAssociation` 继承 `QMetaContainer`，因此它还携带通用容器和 iterator 描述：

| API | 作用 | 边界 |
| --- | --- | --- |
| `hasInputIterator()` | 是否支持 input 级别迭代 | 只保证最基本的前进读取 |
| `hasForwardIterator()` | 是否支持 forward 迭代 | 不等于可后退 |
| `hasBidirectionalIterator()` | 是否支持双向迭代 | 不等于随机访问 |
| `hasRandomAccessIterator()` | 是否支持随机访问 | 关联容器通常不应默认假设支持 |
| `hasSize()` | 是否有原生 size 操作 | 与 iterator 能力独立 |
| `size(const void *)` | 读取真实容器大小 | 传入容器地址必须匹配描述器 |
| `canClear()` | 是否支持 clear | 只读容器或无 clear 成员时为 false |
| `clear(void *)` | 清空真实容器 | 会使已有 iterator 失效 |
| `begin()` / `end()` | 创建可写擦除 iterator | 用完要对应销毁 |
| `constBegin()` / `constEnd()` | 创建只读擦除 iterator | 用完要对应销毁 |
| `destroyIterator()` | 销毁可写 iterator | 必须使用创建它的描述器 |
| `destroyConstIterator()` | 销毁只读 iterator | 不能和可写销毁函数混用 |
| `compareIterator()` / `compareConstIterator()` | 比较同源 iterator | 不要比较不同容器或不同描述器的 iterator |
| `advanceIterator()` / `advanceConstIterator()` | 按步数移动 | 只有底层 iterator 支持的方向和范围才有效 |
| `diffIterator()` / `diffConstIterator()` | 计算 iterator 距离 | 需要适配器提供相应差值能力 |

对现代使用者来说，`QMetaAssociation::Iterable` 会把这些底层细节封装成 RAII iterator；直接调用继承 API 主要适合实现更底层的元容器适配。

## 14. 生命周期、迭代器失效和线程边界

### 14.1 iterable 不延长容器生命周期

```cpp
QMetaAssociation::Iterable makeView()
{
    QMap<QString, int> local;
    return QMetaAssociation::Iterable(&local); // 错误
}
```

返回后的 view 指向已经销毁的 `local`。正确做法是让调用方持有容器，或让 view 与容器一起由同一个拥有对象管理。

### 14.2 修改可能使 iterator 失效

插入、删除、清空和某些底层容器的重新分配都可能使已有 iterator 失效。不要在遍历时无条件调用 `insertKey()`、`removeKey()` 或 `setValue()`，除非底层容器文档明确保证该操作不会使当前 iterator 失效。

### 14.3 同一个 iterator 只能在同一坐标体系中比较

```cpp
auto a = firstIterable.constBegin();
auto b = secondIterable.constEnd();
// 不要比较 a 和 b
```

即使两个 iterable 使用相同的 `QMetaAssociation` 描述器，只要它们指向不同的真实容器，iterator 比较也没有可靠意义。

### 14.4 QMetaAssociation 本身可以跨线程复制，但容器访问不自动安全

描述器通常只是静态接口指针，复制它不等于复制容器。多线程使用时仍要由调用方同步真实容器、保证 iterator 不与并发写入冲突，并遵守容器本身的线程规则。

## 15. 常见错误与排查顺序

### 15.1 把默认构造对象当成空容器

**症状：** `QMetaAssociation()` 的 `value()` 或 `begin()` 被当成空 map 使用。

**原因：** 默认对象没有 key/mapped 类型和函数表。

**修复：** 使用 `fromContainer<T>()` 创建描述器；需要空容器时创建真实 `T` 对象。

### 15.2 只检查返回指针，不检查 iterator 是否等于 end

**症状：** `createConstIteratorAtKey()` 返回非空指针，但读取 key/value 得到无效数据。

**原因：** 底层 `find()` 找不到时仍可能返回一个指向 end iterator 的已分配对象。

**修复：** 创建 end iterator，与查找 iterator 比较；高层代码使用 `find()` 后比较 `constEnd()`。

### 15.3 把 `canXxx()` 当成“这次调用一定成功”

**症状：** 能力存在，但 key 类型不匹配、容器地址错误或 iterator 已失效。

**原因：** `canXxx()` 只报告函数表能力，不验证本次参数和对象状态。

**修复：** 同时检查元类型转换、容器生命周期、可写性和 iterator 有效性。

### 15.4 把 `value()` 当成带命中状态的查找

**症状：** 缺失 key 返回的默认值被误认为容器中的真实值。

**原因：** `value()` 只返回 `QVariant`，不单独返回 found 标记。

**修复：** 先 `containsKey()` 或 `find()`，再读取 value。

### 15.5 以为 `setValue()` 只更新已有 key

**症状：** 设置一个不存在的 key 后容器大小增加。

**原因：** 底层可写下标操作可能自动插入默认条目。

**修复：** 只更新已有项时先 `mutableFind()`，确认不等于 `mutableEnd()` 后再赋值。

### 15.6 直接伪造 `void *` 类型

**症状：** 崩溃、内存破坏、读取出奇怪的 QVariant。

**原因：** `void *` API 没有运行时检查指针实际指向的 C++ 类型。

**修复：** 只把指向真实 `T`、`T::key_type`、`T::mapped_type` 或由同一描述器创建的 iterator 传入；普通代码优先用 `Iterable`。

### 15.7 忽略 `QVariant` 转换

**症状：** `"1"` 被转换成整数、浮点被截断或自定义类型写入失败。

**原因：** `Iterable` 会使用 Qt 的 `QMetaType` 转换规则，不是业务校验器。

**修复：** 预先检查 `canConvert()`，必要时显式构造目标类型并拒绝有损转换。

### 15.8 在 const view 上尝试修改

**症状：** `mutableFind()` 或 `setValue()` 无法得到有效可写操作。

**原因：** const 指针构造的 iterable 会保留 const 属性。

**修复：** 从非 const 容器构造可写 view，并检查 `canSetMappedAtIterator()` 或 `canSetMappedAtKey()`。

### 15.9 假设所有关联容器都是随机访问

**症状：** 使用随机访问 iterator 标签触发 fatal，或对 iterator 做 `+ n` 得到无效结果。

**原因：** 关联容器的 iterator 能力由 `QMetaContainer` 运行时报告，不能从 key/value 结构推断。

**修复：** 使用普通 `auto` iterator，先检查 `hasRandomAccessIterator()`。

## 16. 推荐设计模板

### 16.1 只读通用遍历

```cpp
template <typename Container>
void dumpAssociation(const Container &container)
{
    QMetaAssociation::Iterable iterable(&container);

    for (auto it = iterable.constBegin();
         it != iterable.constEnd(); ++it) {
        qDebug() << it.key() << it.value();
    }
}
```

该模板仍要求 `Container` 能被 Qt 的关联容器 traits 识别，并且 key/mapped 可以构造 `QVariant`。

### 16.2 区分“转换失败”和“key 不存在”

```cpp
bool tryRead(const QMetaAssociation::Iterable &iterable,
             const QVariant &key,
             QVariant *result)
{
    const QMetaAssociation meta = iterable.metaContainer();
    const QMetaType keyType = meta.keyMetaType();

    if (!key.canConvert(keyType))
        return false;

    const auto it = iterable.find(key);
    if (it == iterable.constEnd())
        return false;

    *result = it.value();
    return true;
}
```

如果业务需要把两类失败分开，应返回更丰富的状态枚举，而不是只返回一个 bool。

### 16.3 只更新已有项

```cpp
void updateExisting(QMetaAssociation::Iterable &iterable,
                    const QVariant &key,
                    const QVariant &mapped)
{
    auto it = iterable.mutableFind(key);
    if (it == iterable.mutableEnd())
        return;

    it.value() = mapped;
}
```

实际代码还应检查 mapped 是否能转换为 `meta.mappedMetaType()`，并确认 `canSetMappedAtIterator()`。

### 16.4 低层 API 的 RAII iterator 保护

```cpp
void inspectRaw(const QMetaAssociation &meta,
                const void *container)
{
    if (!meta.canCreateConstIteratorAtKey())
        return;

    QMetaType keyType = meta.keyMetaType();
    QVariant keyValue(keyType);
    void *keyData = keyValue.data();

    void *it = meta.createConstIteratorAtKey(container, keyData);
    if (!it)
        return;

    void *end = meta.constEnd(container);
    const bool found = end &&
        !meta.compareConstIterator(it, end);

    if (end)
        meta.destroyConstIterator(end);
    meta.destroyConstIterator(it);

    if (!found)
        return;
}
```

这个底层示例只展示资源配对。真实代码还需要正确构造 keyValue、填入实际 key、验证 key 类型和保证 container 地址与描述器匹配；普通业务逻辑优先使用 `Iterable::find()`。

## API 速查表
### 17.1 创建和比较描述器

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QMetaAssociation()` | 创建无效描述器 | 没有 key/mapped 类型和操作能力 |
| `fromContainer<T>()` | 从编译期容器类型建立描述器 | Qt 6.0 起；要求容器满足可识别 traits |
| `operator==(lhs, rhs)` | 比较描述器接口身份 | 比较的是元描述，不是容器元素 |
| `operator!=(lhs, rhs)` | 比较描述器不等 | 同上 |
| `keyMetaType()` | 获取 key 的 `QMetaType` | 无效描述器可能返回无效类型 |
| `mappedMetaType()` | 获取 mapped 的 `QMetaType` | 描述类型，不返回当前值 |

### 17.2 按 key 的能力和操作

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `canInsertKey()` | 查询是否支持按 key 插入 | 不代表 QVariant 转换一定成功 |
| `insertKey(void *, const void *)` | 插入 key | 可能使用默认 mapped；容器必须可写 |
| `canRemoveKey()` | 查询是否支持按 key 删除 | 不代表只删除一个条目 |
| `removeKey(void *, const void *)` | 删除 key | 多值容器的删除粒度由底层决定 |
| `canContainsKey()` | 查询是否支持存在性判断 | false 可能表示“不支持”，不是“不存在” |
| `containsKey(const void *, const void *)` | 判断 key 是否存在 | 先检查能力；参数类型必须准确 |
| `canGetMappedAtKey()` | 查询是否能按 key 读取 mapped | 不保证 key 存在 |
| `mappedAtKey(const void *, const void *, void *)` | 按 key 写出 mapped | 输出存储必须已构造；缺失 key 要谨慎 |
| `canSetMappedAtKey()` | 查询是否能按 key 设置 mapped | 可能使用下标并插入缺失 key |
| `setMappedAtKey(void *, const void *, const void *)` | 按 key 写入 mapped | 只更新已有项时先查找 |

### 17.3 Iterator 访问

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `canGetKeyAtIterator()` | 查询可写 iterator 是否能读 key | iterator 不能是 end |
| `keyAtIterator(const void *, void *)` | 从可写 iterator 复制 key | 输出是复制值，不是长期引用 |
| `canGetKeyAtConstIterator()` | 查询只读 iterator 是否能读 key | 常用于只读通用遍历 |
| `keyAtConstIterator(const void *, void *)` | 从只读 iterator 复制 key | iterator 必须来自同一描述器 |
| `canGetMappedAtIterator()` | 查询可写 iterator 是否能读 mapped | 不等于可写 |
| `mappedAtIterator(const void *, void *)` | 从可写 iterator 复制 mapped | 当前 iterator 必须有效 |
| `canGetMappedAtConstIterator()` | 查询只读 iterator 是否能读 mapped | 依赖底层 mapped 提取能力 |
| `mappedAtConstIterator(const void *, void *)` | 从只读 iterator 复制 mapped | 不修改真实容器 |
| `canSetMappedAtIterator()` | 查询是否能修改 iterator 当前 mapped | const view 不可用 |
| `setMappedAtIterator(const void *, const void *)` | 修改 iterator 当前 mapped | 不能操作 end iterator |

### 17.4 按 key 创建和销毁 iterator

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `canCreateIteratorAtKey()` | 查询是否能创建可写查找 iterator | 需要底层 find 和可写 iterator |
| `createIteratorAtKey(void *, const void *)` | 创建可写查找 iterator | 找不到时可能返回指向 end 的非空 iterator |
| `canCreateConstIteratorAtKey()` | 查询是否能创建只读查找 iterator | const 容器和 iterator 能力必须存在 |
| `createConstIteratorAtKey(const void *, const void *)` | 创建只读查找 iterator | 用 `destroyConstIterator()` 配对销毁 |
| `QMetaContainer::destroyIterator()` | 销毁可写擦除 iterator | 不能销毁 const iterator |
| `QMetaContainer::destroyConstIterator()` | 销毁只读擦除 iterator | 必须使用同一描述器 |

### 17.5 `QMetaAssociation::Iterable`

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `Iterable(meta, T *)` | 创建可写关联容器视图 | 不拥有 `T`；保留可写性 |
| `Iterable(meta, const T *)` | 创建只读关联容器视图 | 不能通过它修改容器 |
| `begin()` / `end()` | 只读范围迭代 | end 不能解引用 |
| `constBegin()` / `constEnd()` | 显式只读迭代 | iterator 和容器必须保持有效 |
| `mutableBegin()` / `mutableEnd()` | 可写范围迭代 | 需要可写 view 和底层能力 |
| `find(const QVariant &)` | 查找并返回只读 iterator | 转换失败与不存在都可能到 end |
| `constFind(const QVariant &)` | `find()` 的只读命名形式 | 不插入缺失 key |
| `mutableFind(const QVariant &)` | 查找并返回可写 iterator | 找不到返回 mutable end |
| `containsKey(const QVariant &)` | QVariant 形式的存在性查询 | false 不能区分转换失败 |
| `insertKey(const QVariant &)` | QVariant 形式插入 key | mapped 通常默认构造 |
| `removeKey(const QVariant &)` | QVariant 形式删除 key | 多值删除数量由底层决定 |
| `value(const QVariant &)` | QVariant 形式读取 mapped | 先确认命中状态更可靠 |
| `setValue(const QVariant &, const QVariant &)` | QVariant 形式设置 mapped | 可能插入缺失 key |
| `metaContainer()` | 取得底层 `QMetaAssociation` | 只是描述器，不是实际容器 |

## 18. 一句话总结

`QMetaAssociation` 是关联容器的运行时操作描述器，不保存元素，也不拥有真实容器：用 `fromContainer<T>()` 建立 key/mapped 类型和能力函数表，用 `canXxx()` 检查操作契约，再优先通过 Qt 6.11 的 `QMetaAssociation::Iterable` 以 `QVariant` 和 iterator 访问未知容器；处理 `void *`、缺失 key、下标插入、iterator 销毁和容器生命周期时必须格外严格。
