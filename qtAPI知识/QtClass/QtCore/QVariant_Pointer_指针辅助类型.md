# QVariant::Pointer 可写代理指针笔记

> 适用版本：Qt 6.11.1  
> 所属模块：`Qt6::Core`  
> 定义位置：`#include <QVariant>`  
> 类型性质：保存 `Indirect` 并通过 `operator*()` 生成可写 `Reference` 的代理

## 1. 它解决什么问题

`QVariant::Pointer<Indirect>` 为运行时容器迭代器提供“指针样式”的访问语法。

在 Qt 元容器中：

- 可写 iterator 的 `operator->()` 返回 `QVariant::Pointer<Iterator>`；
- 对这个代理执行 `operator*()`，得到 `QVariant::Reference<Iterator>`；
- `Reference` 再负责把元素读成 `QVariant` 或把 `QVariant` 写回底层元素。

它只是语法适配层，不是 `T *`，也不拥有任何对象。特别是它没有真正的 `operator->()`，不能写成 `pointer->member` 去访问元素成员。

## 2. 实际使用场景

### 2.1 通过元序列 iterator 使用指针式写法

```cpp
auto iterator = iterable.mutableBegin();
QVariant::Pointer<Iterator> pointer = iterator.operator->();

QVariant value = *pointer;
value = value.toInt() + 1;
*pointer = value;
```

通常无需显式声明代理，直接使用 iterator 的 `operator->()` 即可：

```cpp
auto iterator = iterable.mutableBegin();
QVariant value = *iterator.operator->();
*iterator.operator->() = value.toInt() + 1;
```

这类接口主要服务于 `QMetaSequence::Iterable` 和 `QMetaAssociation::Iterable` 的标准迭代器适配。

### 2.2 把可写访问降级为只读访问

```cpp
QVariant::Pointer<Iterator> writable = iterator.operator->();
QVariant::ConstPointer<Iterator> readonly = writable;

const QVariant value = *readonly;
```

转换后只能得到 `ConstReference`，不能再通过只读代理写回容器。

## 3. 构建与包含

```cpp
#include <QVariant>
#include <QMetaSequence>
#include <QMetaAssociation>
```

业务代码一般通过元容器 iterator 获得 `Pointer`，不需要直接构造自定义代理。

## 4. 核心使用模型

### 4.1 `Pointer` 保存的是 `Indirect`

```cpp
QVariant::Pointer<Iterator> pointer = iterator.operator->();
```

它内部保存一个 `Indirect` 副本，不保存元素值，也不保存元素地址。`Indirect` 的具体行为决定如何读取和写入元素。

### 4.2 `operator*()` 返回代理，不返回真实引用

```cpp
QVariant::Reference<Iterator> reference = *pointer;
```

这个返回值是 `Reference`，不是 `T &`。要得到值，需要把它转换为 `QVariant`；要写回，需要给它赋一个 `QVariant`。

### 4.3 它不是内存管理指针

`QVariant::Pointer` 不执行 `delete`、不判断空指针、不拥有 iterator 之外的资源。它的“指针”只是标准迭代器接口命名中的 pointer 类型。

## 5. 生命周期和失效边界

- `Pointer` 不拥有底层容器或 iterator 指向的元素；
- 底层 iterator 失效后，`Pointer` 和由它得到的 `Reference` 都失效；
- 插入、删除、扩容、detach 或容器重分配可能使代理失效；
- 复制 `Pointer` 只复制 `Indirect`，不是元素快照；
- `operator*()` 返回的 `Reference` 是短期代理，长期保存应转成 `QVariant`；
- 转成 `ConstPointer` 后，新的代理只能读不能写。

## 6. 逐项 API 说明

### `Pointer(const Indirect &pointed)`

复制构造间接访问器。不会复制底层元素，也不会取得容器所有权。

### `Pointer(Indirect &&pointed)`

移动构造间接访问器。适合从临时 iterator 生成代理，但不能绕过底层 iterator 的生命周期限制。

### `operator*() const`

返回 `QVariant::Reference<Indirect>`：

```cpp
QVariant::Reference<Iterator> reference = *pointer;
```

返回的是可写间接引用代理。它支持转换成 `QVariant`，也支持把 `QVariant` 写回底层元素，前提是 `Indirect` 的专门化和底层容器支持这些操作。

### `operator ConstPointer<Indirect>() const`

把可写指针代理降级为只读指针代理：

```cpp
QVariant::Pointer<Iterator> writable = iterator.operator->();
QVariant::ConstPointer<Iterator> readonly = writable;
```

这是权限收窄，不是复制元素。原来的 `writable` 仍然可写；只有 `readonly` 不能写回。

## 7. 与真正指针和相邻代理的区别

| 类型 | `operator*()` 返回 | `operator->()` | 是否拥有对象 |
| --- | --- | --- | --- |
| `QVariant::Pointer` | `QVariant::Reference` | 没有 | 否 |
| `QVariant::ConstPointer` | `QVariant::ConstReference` | 没有 | 否 |
| `T *` | `T &` | `T *` | 否 |
| `QSharedPointer<T>` | `T &` | `T *` | 共享拥有 |

不要因为名字中有 `Pointer` 就把它当作 `T *` 或智能指针。

## 8. 常见错误

### 8.1 写 `pointer->member`

`QVariant::Pointer` 没有 `operator->()`，它不是指向元素对象的真实指针。应先解引用为 `Reference`，再转成 `QVariant` 或具体值。

### 8.2 以为 `*pointer` 就是 `T &`

`*pointer` 是 `QVariant::Reference`。读取是值转换，写入是通过 variant 的类型擦除转换后回写。

### 8.3 保存 Pointer 跨越容器修改

容器扩容、删除或 detach 可能使 iterator 失效。重新取得 iterator 和 pointer，不要继续使用旧代理。

### 8.4 以为转换成 ConstPointer 会复制元素

转换只复制 `Indirect` 并收窄写权限。若需要稳定快照，执行：

```cpp
const QVariant snapshot = *readonly;
```

## API 速查表
| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `Pointer(const Indirect &)` | 复制间接访问器 | 不复制元素，不拥有容器 |
| `Pointer(Indirect &&)` | 移动构造间接访问器 | 仍受 iterator 生命周期限制 |
| `operator*()` | 返回可写 `Reference` | 不是 `T &` |
| `operator ConstPointer()` | 降级为只读 pointer 代理 | 不复制元素，丢弃当前路径的写权限 |
| `~Pointer()` | 销毁代理 | 不销毁底层元素 |

## 10. 一句话总结

`QVariant::Pointer` 是元容器迭代器的可写代理指针：它只保存 `Indirect`，`operator*()` 返回 `QVariant::Reference`，不提供真实指针的 `operator->()`，也不拥有容器或元素。
