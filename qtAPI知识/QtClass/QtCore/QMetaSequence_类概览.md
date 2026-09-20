# Qt QMetaSequence 顺序容器反射与类型擦除操作笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QMetaSequence>`  
> 所属模块：`Qt6::Core`  
> 类型性质：`QMetaContainer` 的顺序容器扩展  
> 相关类型：`QMetaContainer`、`QMetaSequence::Iterable`、`QIterable`、`QVariant`、`QMetaType`

## 1. 它解决什么问题

当程序只拿到一个运行时容器，而不知道它具体是 `QList<int>`、`QVector<QString>` 还是其他已支持的顺序容器时，普通 C++ 模板无法直接操作它。`QMetaSequence` 为这种场景提供一张类型擦除操作表，描述：

- 元素的 `QMetaType`；
- 是否可以按索引读取或写入；
- 是否可以通过 iterator 读取或写入；
- 是否可以在开头/结尾添加或移除元素；
- 是否可以按 iterator 插入和删除；
- 是否可以清空、计数和遍历；
- 如何把真实容器包装成 `QMetaSequence::Iterable`。

它不是具体容器，也不拥有元素。它保存的是“如何操作 `T` 容器”的静态描述；真实容器必须在所有调用期间存活，并以正确的类型地址传入。

## 2. 实际使用场景

### 2.1 从 QVariant 取得未知序列并遍历

```cpp
QVariant value = QVariant::fromValue(QList<int>{7, 11, 42});
if (value.canConvert<QMetaSequence::Iterable>()) {
    const QMetaSequence::Iterable iterable =
        value.value<QMetaSequence::Iterable>();

    for (const QVariant &element : iterable)
        qDebug() << element;
}
```

高层 `Iterable` 把每个元素包装成 `QVariant`，并负责擦除 iterator 的创建和销毁。业务代码优先使用它，而不是直接操作 `void *` iterator。

### 2.2 运行时编辑未知容器

```cpp
QList<int> values{1, 2, 3};
QMetaSequence::Iterable iterable(
    QMetaSequence::fromContainer<QList<int>>(),
    &values);

if (iterable.canRandomAccessIterate()) {
    iterable.setAt(1, 20);
    iterable.append(40);
}
```

`setAt()`、`append()` 等高层操作会把 `QVariant` 转换为元素的 `QMetaType`。转换失败、容器没有对应能力或索引不合法时，不能把调用当作成功。

### 2.3 为通用容器工具探测能力

```cpp
const QMetaSequence meta =
    QMetaSequence::fromContainer<QList<QString>>();

qDebug() << meta.valueMetaType().name()
         << meta.canGetValueAtIndex()
         << meta.canSetValueAtIndex()
         << meta.hasRandomAccessIterator();
```

反射工具应先查询能力，再决定显示哪些操作按钮。`hasSize()`、`canGetValueAtIndex()`、`canGetValueAtIterator()` 互相独立，不能从一种能力推断另一种。

## 3. 描述器和真实容器

### 3.1 创建描述器

```cpp
const QMetaSequence meta =
    QMetaSequence::fromContainer<QVector<double>>();
```

`fromContainer<T>()` 是编译期模板工厂，返回静态的类型擦除描述。`T` 必须是 Qt 元容器体系能够识别的顺序容器类型，并且元素类型可用 `QMetaType` 表示。

### 3.2 真实容器地址

```cpp
QVector<double> values{1.0, 2.0};
meta.valueAtIndex(&values, 0, &result);
```

`&values` 必须与 `fromContainer<QVector<double>>()` 完全匹配。不能把 `QList<double>`、容器副本或错误的 `void *` 地址传进去。描述器不会做运行时 C++ 类型检查。

### 3.3 默认构造状态

```cpp
const QMetaSequence invalid;
Q_ASSERT(!invalid.valueMetaType().isValid());
```

默认构造描述器没有函数表。能力查询通常为 false，不能直接用它访问容器。

## 4. 添加、移除和索引访问

### 4.1 开头和结尾操作

`canAddValueAtBegin()`/`addValueAtBegin()` 对应前端插入，`canAddValueAtEnd()`/`addValueAtEnd()` 对应尾端追加；移除操作同理。

并非每种容器都支持两端操作：

- `QVector` 通常有尾部追加，但没有常数时间前端添加；
- `QList` 的具体能力由 Qt 容器适配器提供；
- `std::vector` 通常只有尾部 `push_back`；
- 只有容器确实提供可识别的接口，能力查询才会为 true。

### 4.2 未指定位置的 `addValue()`/`removeValue()`

`canAddValue()` 和 `addValue()` 是兼容层的“未指定位置”操作。底层适配器可能把它映射到尾部、头部或容器自己的 insert 方式；不要把它当成固定的 append。

Qt 6.11 的 `QMetaSequence::Iterable` 推荐使用 `append()`、`prepend()`、`removeLast()` 和 `removeFirst()`。旧的 position 风格高层接口属于兼容方向，优先迁移到明确的操作。

### 4.3 按索引读取和写入

```cpp
if (meta.canGetValueAtIndex()) {
    int result = 0;
    meta.valueAtIndex(&values, 0, &result);
}

if (meta.canSetValueAtIndex()) {
    const int replacement = 99;
    meta.setValueAtIndex(&values, 0, &replacement);
}
```

这些 API 的 `result` 和 `value` 必须指向正确元素类型的已构造对象或只读值。索引是否越界由底层容器操作决定；通用代码应先检查 `0 <= index < size`，而且 `size()` 可能不可用。

## 5. iterator 访问和修改

### 5.1 可写 iterator

`canGetValueAtIterator()`、`canSetValueAtIterator()`、`canInsertValueAtIterator()` 和删除能力分别描述 iterator 路径。iterator 必须由同一个 `QMetaSequence` 和同一个真实容器创建：

```cpp
void *it = meta.begin(&values);
void *end = meta.end(&values);

while (!meta.compareIterator(it, end)) {
    int current = 0;
    meta.valueAtIterator(it, &current);
    meta.advanceIterator(it, 1);
}

meta.destroyIterator(it);
meta.destroyIterator(end);
```

普通代码不要手写这套 raw 循环，示例只用于说明所有权和配对关系。高层 `Iterable` 会自动销毁 iterator。

### 5.2 迭代器修改导致失效

插入、删除、扩容、清空和真实容器移动都可能使旧 iterator 失效。调用 `insertValueAtIterator()` 或 `erase...()` 后，不要继续使用旧的 begin/end，除非底层容器明确保证相应 iterator 仍有效。

### 5.3 只读 iterator

`canGetValueAtConstIterator()` 描述 const iterator 读取能力。只读 iterator 仍依赖真实容器生命周期；容器修改可能使它失效。`valueAtConstIterator()` 的 result 同样必须是正确元素类型的可写存储，因为函数需要把元素复制出来。

## 6. `QMetaType` 与 QVariant 转换

### 6.1 `valueMetaType()`

```cpp
const QMetaType type = meta.valueMetaType();
if (!type.isValid())
    return;
```

它返回元素类型，不是容器类型。`QMetaSequence::Iterable` 用它创建每一个元素的 QVariant。

### 6.2 高层 `setAt()`/append 的转换

```cpp
iterable.setAt(0, QVariant::fromValue(42));
iterable.append(QVariant::fromValue(99));
```

高层接口会尝试把 QVariant 转成 `valueMetaType()`。转换失败时不要假定元素已写入；对于需要严格类型的工具，应先检查 `value.canConvert(meta.valueMetaType())` 或用 `QMetaType` 转换 API 明确处理错误。

### 6.3 元素是 QVariant 时的特殊性

如果真实容器元素类型本身就是 `QVariant`，高层 iterable 会直接在 QVariant 存储中操作元素；如果元素是普通类型，则会创建一个对应类型的 QVariant。不要把返回的 QVariant 地址当作真实容器元素地址保存。

## 7. 排序能力和类型擦除边界

`isSortable()` 表示 Qt 的顺序容器适配器能否把元素视为可排序类型。它不是“当前容器已经有序”，也不会自动执行排序。排序还需要比较规则、可写 iterator 和元素类型的可比较能力。

若通用工具需要排序：

1. 先检查 `isSortable()`；
2. 确认容器和元素的 iterator/写入能力；
3. 明确比较规则和异常/失败策略；
4. 预计排序会使 iterator 和外部元素引用失效。

## 8. 与 `QMetaContainer` 的关系

`QMetaSequence` 继承 `QMetaContainer`，因此还拥有：

- `hasInputIterator()` 到 `hasRandomAccessIterator()`；
- `hasSize()`/`size()`；
- `canClear()`/`clear()`；
- 可写和只读 iterator 的创建、复制、移动、比较、距离和销毁。

本篇只重复顺序容器新增的 API。raw iterator 的通用配对规则、能力层级和 `QIterable::size()` fallback 见 `QMetaContainer` 笔记。

## 9. `QMetaSequence::Iterable` 的推荐入口

```cpp
QList<QString> names{"A", "B"};
QMetaSequence::Iterable iterable(
    QMetaSequence::fromContainer<QList<QString>>(),
    &names);

for (const QVariant &name : iterable)
    qDebug() << name.toString();
```

它提供：

- `begin()`/`end()` 只读 range；
- `constBegin()`/`constEnd()`；
- `mutableBegin()`/`mutableEnd()`；
- `at()`/`setAt()`；
- `append()`/`prepend()`；
- `removeLast()`/`removeFirst()`；
- `QVariant` 元素解引用。

`Iterable` 仍然只借用真实容器，不延长容器生命周期。它不是容器副本。

## 10. 逐项 API 说明

### 10.1 `QMetaSequence()`

```cpp
QMetaSequence();
```

构造无效的顺序容器描述器。不能把它当成一个空的、可操作的真实容器。

### 10.2 `fromContainer<T>()`

```cpp
template <typename T>
static constexpr QMetaSequence fromContainer();
```

Qt 6.0 起提供。按真实容器类型创建顺序容器描述器。类型和元素必须满足 Qt 元容器适配要求；这是编译期创建，不会复制任何容器对象。

### 10.3 `valueMetaType() const`

```cpp
QMetaType valueMetaType() const;
```

返回元素类型的 `QMetaType`。无效描述器或无法表示元素类型时可能无效。

### 10.4 `isSortable() const`

```cpp
bool isSortable() const;
```

查询元素和适配器是否提供可排序能力。true 不代表容器当前有序，也不代表排序不会使 iterator 失效。

### 10.5 `canAddValueAtBegin() const`

```cpp
bool canAddValueAtBegin() const;
```

查询是否可以在头部添加元素。必须先为 true，才能调用 `addValueAtBegin()` 或高层 `prepend()`。

### 10.6 `addValueAtBegin(void *, const void *) const`

```cpp
void addValueAtBegin(void *container,
                     const void *value) const;
```

把一个已经是元素类型的值添加到容器头部。container 必须可写，value 必须指向匹配类型；操作可能使 iterator 失效。

### 10.7 `canAddValueAtEnd() const`

```cpp
bool canAddValueAtEnd() const;
```

查询尾部追加能力。高层 `Iterable::append()` 使用这类能力。

### 10.8 `addValueAtEnd(void *, const void *) const`

```cpp
void addValueAtEnd(void *container,
                   const void *value) const;
```

把元素追加到尾部。它不负责 QVariant 转换，raw API 的 value 必须已经是元素类型。

### 10.9 `canRemoveValueAtBegin() const`

```cpp
bool canRemoveValueAtBegin() const;
```

查询能否移除第一个元素。空容器上调用移除属于底层容器边界问题，业务代码应先判断非空。

### 10.10 `removeValueAtBegin(void *) const`

```cpp
void removeValueAtBegin(void *container) const;
```

移除头部元素。会销毁该元素，并可能使 iterator、引用和指针失效。

### 10.11 `canRemoveValueAtEnd() const`

```cpp
bool canRemoveValueAtEnd() const;
```

查询能否移除最后一个元素。空容器上不能调用。

### 10.12 `removeValueAtEnd(void *) const`

```cpp
void removeValueAtEnd(void *container) const;
```

移除尾部元素。调用后旧的 end、元素引用和相关 iterator 可能失效。

### 10.13 `canGetValueAtIndex() const`

```cpp
bool canGetValueAtIndex() const;
```

查询是否有按索引读取函数。没有时，高层 `Iterable::at()` 在 Qt 6 中可能通过 const iterator 合成访问，并发出合成访问警告。

### 10.14 `valueAtIndex(const void *, qsizetype, void *) const`

```cpp
void valueAtIndex(const void *container,
                  qsizetype index,
                  void *result) const;
```

把指定索引的元素复制到 result。result 必须指向已构造的 `valueMetaType()` 存储；索引边界由调用方检查，负索引不能当作 Python 风格索引。

### 10.15 `canSetValueAtIndex() const`

```cpp
bool canSetValueAtIndex() const;
```

查询是否能按索引写入元素。它与 `canGetValueAtIndex()` 独立。

### 10.16 `setValueAtIndex(void *, qsizetype, const void *) const`

```cpp
void setValueAtIndex(void *container,
                     qsizetype index,
                     const void *value) const;
```

把匹配类型的 value 写入索引位置。不会执行 QVariant 转换；高层 `Iterable::setAt()` 会先转换。

### 10.17 `canAddValue() const`

```cpp
bool canAddValue() const;
```

查询未指定位置的兼容添加能力。具体映射由适配器决定，不应假定一定是尾部追加。

### 10.18 `addValue(void *, const void *) const`

```cpp
void addValue(void *container,
              const void *value) const;
```

以底层适配器定义的默认位置添加元素。Qt 6.11 高层代码优先用明确的 begin/end 版本。

### 10.19 `canRemoveValue() const`

```cpp
bool canRemoveValue() const;
```

查询未指定位置的兼容移除能力。具体移除位置由底层适配器决定。

### 10.20 `removeValue(void *) const`

```cpp
void removeValue(void *container) const;
```

执行未指定位置的兼容移除。调用前确认容器非空并准备丢弃旧 iterator。

### 10.21 `canGetValueAtIterator() const`

```cpp
bool canGetValueAtIterator() const;
```

查询可写 iterator 的元素读取能力。它要求底层 iterator 能解引用为元素。

### 10.22 `valueAtIterator(const void *, void *) const`

```cpp
void valueAtIterator(const void *iterator,
                     void *result) const;
```

把可写 iterator 当前元素复制到 result。iterator 不能是 end，也必须来自同一描述器和真实容器。

### 10.23 `canSetValueAtIterator() const`

```cpp
bool canSetValueAtIterator() const;
```

查询能否通过可写 iterator 修改当前元素。

### 10.24 `setValueAtIterator(const void *, const void *) const`

```cpp
void setValueAtIterator(const void *iterator,
                        const void *value) const;
```

修改 iterator 当前元素。value 必须是元素类型；end iterator 不可写入。

### 10.25 `canInsertValueAtIterator() const`

```cpp
bool canInsertValueAtIterator() const;
```

查询是否支持在可写 iterator 位置插入元素。插入后 iterator 失效规则由真实容器决定。

### 10.26 `insertValueAtIterator(void *, const void *, const void *) const`

```cpp
void insertValueAtIterator(void *container,
                           const void *iterator,
                           const void *value) const;
```

在 iterator 指向的位置插入元素。container、iterator 和 value 必须来自同一描述器/真实容器坐标系。

### 10.27 `canEraseValueAtIterator() const`

```cpp
bool canEraseValueAtIterator() const;
```

查询是否支持删除单个 iterator 元素。

### 10.28 `eraseValueAtIterator(void *, const void *) const`

```cpp
void eraseValueAtIterator(void *container,
                          const void *iterator) const;
```

删除 iterator 当前元素。不能删除 end；删除后不要继续使用旧 iterator。

### 10.29 `canEraseRangeAtIterator() const`

```cpp
bool canEraseRangeAtIterator() const;
```

查询是否支持按 `[iterator1, iterator2)` 删除范围。

### 10.30 `eraseRangeAtIterator(void *, const void *, const void *) const`

```cpp
void eraseRangeAtIterator(void *container,
                          const void *iterator1,
                          const void *iterator2) const;
```

删除半开区间 `[iterator1, iterator2)`。两个 iterator 必须同源、顺序合法，并且属于同一真实容器。

### 10.31 `canGetValueAtConstIterator() const`

```cpp
bool canGetValueAtConstIterator() const;
```

查询只读 iterator 的元素读取能力。它独立于可写 iterator 的读取能力。

### 10.32 `valueAtConstIterator(const void *, void *) const`

```cpp
void valueAtConstIterator(const void *iterator,
                          void *result) const;
```

从只读 iterator 复制当前元素到 result。end、失效 iterator 和错误 result 类型都不能使用。

## 11. 常见错误

### 11.1 把 QMetaSequence 当成容器对象

**症状：** 创建描述器后希望直接遍历或查看元素。

**原因：** 描述器不保存真实容器。

**修复：** 同时持有 `QList`/`QVector` 等真实对象，并通过 `Iterable` 或 raw API 传入地址。

### 11.2 跳过能力检查

**症状：** 对不支持的容器调用索引、头部添加或 iterator 写入。

**原因：** 元容器接口槽位可能为空。

**修复：** 先检查对应 `can...()`/`has...()`，高层代码使用 `Iterable` 的能力查询。

### 11.3 把 raw value 当成 QVariant

**症状：** `valueAtIndex()` 复制到错误内存或堆损坏。

**原因：** raw API 要求 result/value 是元素类型存储，不是 `QVariant *`。

**修复：** 用 `valueMetaType()` 构造正确的存储，或直接使用高层 `Iterable`。

### 11.4 用负索引访问

**症状：** 负值索引产生未定义行为或错误元素。

**原因：** QMetaSequence 的索引是 `qsizetype`，不承诺 Python 风格负索引。

**修复：** 先执行显式范围检查。

### 11.5 修改容器后继续使用 iterator

**症状：** 比较、解引用或距离计算异常。

**原因：** 插入、删除、扩容和清空可能使 iterator 失效。

**修复：** 修改后销毁并重新创建相关 iterator。

### 11.6 混淆 `addValue()` 和 `addValueAtEnd()`

**症状：** 元素加入位置与预期不一致。

**原因：** 未指定位置操作由底层适配器决定。

**修复：** 需要明确位置时使用 begin/end 版本或 `Iterable::append()`/`prepend()`。

### 11.7 把 `isSortable()` 当成排序操作

**症状：** 查询为 true 后以为容器已经排序。

**原因：** 它只是能力标志。

**修复：** 另行执行排序并处理 iterator 失效。

## API 速查表
| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QMetaSequence()` | 构造无效顺序容器描述器 | 不保存真实容器 |
| `fromContainer<T>()` | 创建 `T` 的类型擦除描述 | Qt 6.0 起；T/元素需可元类型化 |
| `valueMetaType()` | 返回元素类型 | 不是容器类型；无效描述器可能无效 |
| `isSortable()` | 查询可排序能力 | 不代表当前有序或自动排序 |
| `canAddValueAtBegin()` | 查询头部添加能力 | 配合 `addValueAtBegin()` |
| `addValueAtBegin()` | 头部添加元素 | raw value 必须是元素类型 |
| `canAddValueAtEnd()` | 查询尾部添加能力 | 配合 `addValueAtEnd()` |
| `addValueAtEnd()` | 尾部追加元素 | 可能使 iterator 失效 |
| `canRemoveValueAtBegin()` | 查询头部移除能力 | 空容器不可移除 |
| `removeValueAtBegin()` | 移除第一个元素 | 丢弃引用和可能失效的 iterator |
| `canRemoveValueAtEnd()` | 查询尾部移除能力 | 空容器不可移除 |
| `removeValueAtEnd()` | 移除最后一个元素 | 检查旧 end/iterator |
| `canGetValueAtIndex()` | 查询按索引读取能力 | false 时高层可能合成访问 |
| `valueAtIndex()` | 按索引复制元素 | result 是元素存储，不是 QVariant |
| `canSetValueAtIndex()` | 查询按索引写入能力 | 与读取独立 |
| `setValueAtIndex()` | 按索引写入元素 | raw API 不自动 QVariant 转换 |
| `canAddValue()` | 查询未指定位置添加能力 | 不保证是 append |
| `addValue()` | 按适配器默认位置添加 | 优先明确 begin/end |
| `canRemoveValue()` | 查询未指定位置移除能力 | 不保证移除头或尾 |
| `removeValue()` | 按适配器默认位置移除 | 先确认非空 |
| `canGetValueAtIterator()` | 查询可写 iterator 读取能力 | iterator 不可为 end |
| `valueAtIterator()` | 从 iterator 复制元素 | iterator 必须同源 |
| `canSetValueAtIterator()` | 查询 iterator 写入能力 | 需要可写 iterator |
| `setValueAtIterator()` | 修改 iterator 当前元素 | 修改后遵守容器失效规则 |
| `canInsertValueAtIterator()` | 查询 iterator 插入能力 | 插入可能使旧 iterator 失效 |
| `insertValueAtIterator()` | 在 iterator 位置插入 | container/iterator/value 必须同源 |
| `canEraseValueAtIterator()` | 查询单元素删除能力 | 不能删除 end |
| `eraseValueAtIterator()` | 删除 iterator 当前元素 | 删除后丢弃旧 iterator |
| `canEraseRangeAtIterator()` | 查询范围删除能力 | 需要同源半开区间 |
| `eraseRangeAtIterator()` | 删除 `[first, last)` | 顺序和容器归属必须正确 |
| `canGetValueAtConstIterator()` | 查询只读 iterator 读取能力 | 与可写 iterator 独立 |
| `valueAtConstIterator()` | 从只读 iterator 复制元素 | result 仍需正确元素存储 |

## 13. 推荐模板

### 13.1 通过高层 Iterable 读取

```cpp
template <typename Container>
QList<QVariant> snapshot(const Container &container)
{
    QMetaSequence::Iterable iterable(&container);
    QList<QVariant> result;
    for (const QVariant &value : iterable)
        result.append(value);
    return result;
}
```

返回的 QVariant 列表拥有元素副本，因此可以脱离真实容器保存；iterable 本身仍然只是借用 container。

### 13.2 反射式写入前检查

```cpp
bool replaceAt(QMetaSequence::Iterable &iterable,
               qsizetype index,
               const QVariant &value)
{
    if (!iterable.canRandomAccessIterate())
        return false;
    if (index < 0 || index >= iterable.size())
        return false;

    iterable.setAt(index, value);
    return true;
}
```

如果 `size()` 是通过 iterator 合成的，可能较慢并触发诊断；性能敏感工具应先检查 `metaContainer().hasSize()`。

## 14. 一句话总结

`QMetaSequence` 是顺序容器的类型擦除操作描述器：它把元素类型、索引访问、iterator 访问、添加删除和清空能力统一暴露给反射框架；业务代码优先用 `QMetaSequence::Iterable`，raw `void *` API 则必须先查能力、匹配真实容器和元素存储，并把所有修改后的 iterator 视为可能失效。
