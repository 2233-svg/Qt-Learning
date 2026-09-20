# QVariant::Reference 可写间接引用笔记

> 适用版本：Qt 6.11.1  
> 所属模块：`Qt6::Core`  
> 定义位置：`#include <QVariant>`  
> 类型性质：保存 `Indirect` 并把读写操作转发给它的可写代理

## 1. 它解决什么问题

`QVariant::Reference<Indirect>` 用来表达“一个元素可以像 `QVariant` 一样读取和赋值，但真实元素仍由另一个对象管理”。

最典型的 `Indirect` 是 Qt 元容器的可写 iterator：

- `QMetaSequence` 的可写 iterator 解引用返回 `QVariant::Reference<Iterator>`；
- `QMetaAssociation` 的可写 iterator 解引用返回 `QVariant::Reference<Iterator>`；
- 读取代理会生成当前元素的 `QVariant` 值；
- 给代理赋值会把右侧 `QVariant` 转换成元素类型，再写回底层 iterator。

因此它不是普通的 `T &`，也不拥有元素。代理只负责保存一个间接访问器；底层容器、iterator 和元素生命周期仍由调用方负责。

## 2. 实际使用场景

### 2.1 修改元序列中的元素

```cpp
QVariant::Reference<Iterator> reference = *iterator;

QVariant value = reference;
value = value.toInt() + 1;
reference = value;
```

在真实的 `QMetaSequence::Iterable` 中，通常直接写成：

```cpp
for (auto it = iterable.mutableBegin();
     it != iterable.mutableEnd(); ++it) {
    QVariant value = *it;
    value = value.toInt() + 1;
    *it = value;
}
```

底层元序列必须支持“按 iterator 写回”。如果 `canSetValueAtIterator()` 为 `false`，赋值代理不能完成写回。

### 2.2 读取关联容器的 mapped value 并写回

关联容器 iterator 的 `Reference` 代表 mapped value，不是 key：

```cpp
auto it = association.mutableBegin();
if (it != association.mutableEnd()) {
    QVariant value = *it;
    *it = value.toString().trimmed();
}
```

key 通常通过关联 iterator 自己的 `key()` 查询；给 `Reference` 赋值不会修改 key。

### 2.3 在泛型代码中交换两个元素

```cpp
auto left = iterable.mutableBegin();
auto right = left + 1;

QVariant::Reference<Iterator> a = *left;
QVariant::Reference<Iterator> b = *right;
a.swap(b);
```

这里交换的是两个底层元素的内容，不是交换两个代理对象保存的 iterator 句柄。

## 3. 构建与包含

```cpp
#include <QVariant>
#include <QMetaSequence>      // 顺序容器元迭代器
#include <QMetaAssociation>  // 关联容器元迭代器
```

`Reference` 通常不由业务代码直接实例化，而是由元容器 iterator 的 `operator*()` 或 `operator[]()` 返回。

## 4. 核心使用模型

### 4.1 代理保存 `Indirect`，不保存 `T`

```cpp
Reference<Iterator> reference = *iterator;
```

`Reference` 内部保存的是 `Iterator` 的副本。它不会复制当前元素，也不会脱离 iterator 自动延长容器生命周期。

### 4.2 读取是值语义，赋值是写回语义

```cpp
QVariant value = reference;  // 从底层元素读取一个 QVariant
reference = value;           // 把值转换后写回底层元素
```

读取得到的 `QVariant` 是独立值。修改这个 `QVariant` 不会自动修改底层元素，必须再次赋值给 `Reference`。

### 4.3 `Indirect` 必须提供 Qt 的专门化

`QVariant::Reference` 的转换和 `operator=(const QVariant &)` 在模板层面只是约定；真正如何从 iterator 读取和写入，由具体 `Indirect` 的专门化提供。

Qt 内置的元序列/元关联 iterator 会提供这些专门化。业务代码如果自行创建 `Reference<CustomIndirect>`，必须同时实现与 Qt 约定匹配的转换和赋值逻辑，否则不能只靠模板声明获得可用行为。

## 5. 生命周期和失效边界

- `Reference` 不拥有底层容器；
- 底层容器销毁后，代理立即失效；
- iterator 失效后，代理也失效；
- 插入、删除、扩容、detach 或其他会使 iterator 失效的操作后，不要继续使用旧代理；
- `Reference` 转成 `QVariant` 后，得到的是值副本，不再依赖代理的可写能力；
- 代理对象可以复制，但复制的是 `Indirect` 句柄，不是元素快照。

尤其要注意：保存 `Reference` 不等于保存元素。若需要跨容器修改保存结果，应先转换成 `QVariant` 或具体值类型。

## 6. 逐项 API 说明

### `Reference(const Indirect &referred)`

复制构造一个间接访问器。要求 `Indirect` 可复制；复制不会复制底层元素。

### `Reference(Indirect &&referred)`

移动构造间接访问器。适合 iterator 临时对象，但底层 iterator 是否仍然有效由 `Indirect` 自身规则决定。

### `Reference(const Reference &)`

默认拷贝构造。两个代理通常指向逻辑上相同的底层位置，但不要把它当成两个独立元素。

### `Reference(Reference &&) = delete`

`Reference` 的移动构造被删除。它的语义更接近“可复制的间接引用代理”，不是需要转移所有权的资源对象。

### `~Reference()`

销毁代理自身。不会销毁、释放或从容器中删除底层元素。

### `operator QVariant() const`

把代理当前指向的元素读取为 `QVariant`。对元序列 iterator，Qt 会按元素 `QMetaType` 构造一个值；对元关联 iterator，通常读取 mapped value。

该转换可能失败或受 `Indirect` 的专门化限制；不要假设所有任意 `Reference<Indirect>` 都自动可转成 variant。

### `operator=(const QVariant &value)`

把一个 `QVariant` 写回底层位置。Qt 元容器 iterator 的实现通常会：

1. 查询底层元素的 `QMetaType`；
2. 尝试把 `value` 转换成元素类型；
3. 调用元容器的 iterator 写入操作；
4. 返回当前代理。

赋值失败时的具体行为取决于 `Indirect` 专门化和底层元容器能力；使用前应检查容器是否支持写入以及转换是否可行。

### `operator=(const Reference &value)`

先读取 `value` 所代表的元素，再把读取到的 `QVariant` 写入当前元素。它不是交换操作，也不保证两个元素类型相同。

### `operator=(Reference &&value)`

同样是读取源代理再写入当前代理。右值限定不会把底层元素所有权转移给当前代理。

### `operator=(const ConstReference &value)`

从只读代理读取一个 `QVariant`，再尝试写入当前可写元素。源代理不会因此变成可写。

### `operator=(ConstReference &&value)`

从右值只读代理读取并写回当前元素。它仍然是值转换和写回，不是移动底层元素。

### `void swap(Reference other)`

交换两个代理所代表的底层元素内容：

```cpp
Reference a = *left;
Reference b = *right;
a.swap(b);
```

实现通常通过临时 `QVariant` 完成，因此可能发生复制或类型转换。它不会交换代理内部的 `Indirect` 句柄。

## 7. 与相邻类型的区别

| 类型 | 读操作 | 写操作 | 是否拥有底层值 |
| --- | --- | --- | --- |
| `QVariant::Reference` | 转成 `QVariant` | 支持写回 | 否 |
| `QVariant::ConstReference` | 转成 `QVariant` | 不支持 | 否 |
| `QVariant::Pointer` | `operator*()` 得到 `Reference` | 间接支持 | 否 |
| `QVariant::ConstPointer` | `operator*()` 得到 `ConstReference` | 不支持 | 否 |
| `QVariant` | 读取自身值 | 修改自身值 | 是 |

## 8. 常见错误

### 8.1 把读取出的 QVariant 修改后期待容器自动变化

```cpp
QVariant value = *iterator;
value = 10; // 只修改 value
```

要写回必须执行：

```cpp
*iterator = value;
```

### 8.2 在 iterator 失效后保存并使用 Reference

删除元素、扩容或容器 detach 后，旧 iterator 和旧 `Reference` 可能都已失效。重新取得 iterator 和代理。

### 8.3 对不支持写入的元容器强行赋值

检查底层元容器是否具备 `canSetValueAtIterator()`；只读 iterable 返回的是 `ConstReference` 或值，不应强行转换成可写代理。

### 8.4 把 `swap()` 理解成交换代理

`a.swap(b)` 交换的是 `a`、`b` 代表的元素内容。两个代理对象的 `m_referred` 并不会互换。

## API 速查表
| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `Reference(const Indirect &)` | 复制间接访问器 | 不复制底层元素 |
| `Reference(Indirect &&)` | 移动构造间接访问器 | 不转移容器所有权 |
| `Reference(const Reference &)` | 复制代理 | 仍代表相同逻辑位置 |
| `Reference(Reference &&) = delete` | 禁止移动构造 | 代理不是资源所有者 |
| `~Reference()` | 销毁代理 | 不销毁底层元素 |
| `operator QVariant()` | 读取当前元素为 QVariant | 得到值，不是持续引用 |
| `operator=(const QVariant &)` | 转换并写回底层元素 | 依赖 Indirect 专门化和容器写能力 |
| `operator=(const Reference &)` | 读取源代理并写入当前元素 | 不是交换 |
| `operator=(Reference &&)` | 从右值代理读取并写入 | 不是移动元素所有权 |
| `operator=(const ConstReference &)` | 从只读代理读取并写回 | 目标仍需可写 |
| `operator=(ConstReference &&)` | 从右值只读代理读取并写回 | 不改变源代理权限 |
| `swap(Reference)` | 交换两个底层元素内容 | 可能复制或转换 |

## 10. 一句话总结

`QVariant::Reference` 是元容器 iterator 的可写间接引用：读它得到一个 `QVariant` 值，给它赋值才会尝试写回底层元素；它不拥有容器、不保证 iterator 长期有效，也不是原生 C++ 引用。
