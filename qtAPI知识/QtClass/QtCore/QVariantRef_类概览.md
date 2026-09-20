# QVariantRef 旧式可写代理笔记

> 适用版本：Qt 6.11.1  
> 弃用状态：Qt 6.15 起弃用，推荐 `QVariant::Reference`  
> 头文件：`#include <QVariantRef>`  
> 所属模块：`Qt6::Core`  
> 类型性质：保存一个间接 pointer 并把 `QVariant` 读写转发给它的兼容代理

## 1. 它解决什么问题

`QVariantRef<Pointer>` 是 Qt 旧式元容器迭代器接口使用的可写代理。它让一个迭代器元素可以表现得像：

```cpp
QVariant value = reference;
reference = value;
```

但它并不保存 `QVariant` 值，也不拥有元素。内部保存的是一个指向间接访问器的地址，真正的读取和写回由 `Pointer` 类型提供。

Qt 6.15 起，新的元容器 API 使用嵌套类型 `QVariant::Reference<Indirect>`。新代码应迁移到嵌套代理；旧类型只适合维护仍需兼容旧头文件或旧迭代器接口的代码。

## 2. 实际使用场景

### 2.1 旧式 iterator 的元素赋值

```cpp
QVariantRef<Iterator> reference = *iterator;

QVariant value = reference;
value = value.toInt() + 1;
reference = value;
```

### 2.2 旧式 pointer 代理解引用

```cpp
QVariantPointer<Iterator> pointer = iterator.operator->();
QVariantRef<Iterator> reference = *pointer;
reference = QVariant(42);
```

迁移后的对应写法是：

```cpp
QVariant::Pointer<Iterator> pointer = iterator.operator->();
*pointer = QVariant(42);
```

## 3. 生命周期和所有权

- `QVariantRef` 不拥有 `Pointer` 指向的访问器；
- 构造时只保存 `const Pointer *`；
- 被引用的 `Pointer` 必须在 `QVariantRef` 使用期间保持有效；
- 底层 iterator 失效后，`QVariantRef` 也失效；
- 容器修改、扩容、detach、删除元素都可能使代理失效；
- 转成 `QVariant` 后得到值副本，可以脱离代理使用；
- 赋值时可能执行类型转换，失败行为由旧式 `Pointer`/iterator 实现决定。

不要把 `QVariantRef` 存成长期成员，也不要把它当成稳定的 `QVariant &`。

## 4. 逐项 API 说明

### `explicit QVariantRef(const Pointer *reference)`

保存一个指向间接访问器的地址。构造函数不复制元素，也不取得底层容器所有权。

传入的 `Pointer` 必须在代理存活期间保持地址稳定；从临时对象构造后立即离开作用域，会产生悬空代理。

### `operator QVariant() const`

读取被引用的间接元素并生成一个 `QVariant` 值。返回值是副本，修改它不会自动写回原容器。

### `operator=(const QVariant &value)`

把 `value` 写回被引用的元素。旧式实现通常会通过 `Pointer` 的间接访问接口完成转换和写入。

### `operator=(const QVariantRef &value)`

先把源代理转换成 `QVariant`，再写入当前代理。它不是交换操作，也不是复制代理地址。

### `operator=(QVariantRef &&value)`

右值代理版本，仍然按“读取源值，再写入目标”的语义工作。它不会转移底层容器或元素所有权。

### `swap(QVariantRef a, QVariantRef b)`

非成员 `swap` 使用临时 `QVariant` 交换两个代理所代表的元素内容：

```cpp
swap(firstReference, secondReference);
```

可能发生复制和类型转换；两个代理自身保存的地址不会互换。

## 5. 与新 API 的对应关系

| 旧 API | 新 API |
| --- | --- |
| `QVariantRef<Pointer>` | `QVariant::Reference<Indirect>` |
| `QVariantRef(const Pointer *)` | `QVariant::Reference(const Indirect &)` 或由 iterator 返回 |
| `operator QVariant()` | `QVariant::Reference::operator QVariant()` |
| `operator=(const QVariant &)` | `QVariant::Reference::operator=(const QVariant &)` |
| 旧式 `QVariantPointer` | `QVariant::Pointer` |

迁移时不要只做名称替换：旧代理保存的是 `Pointer *`，新代理按值保存 `Indirect`。应使用新元容器 iterator 的返回类型和 `operator*()`/`operator->()`，让模板类型自动推导。

## 6. 常见错误

### 6.1 从临时 Pointer 构造

```cpp
// 错误风险：pointer 临时对象销毁后 reference 悬空
QVariantRef<Iterator> reference = *makePointer();
```

确保被引用的 pointer/iterator 在代理整个使用期间有效。

### 6.2 把读取出的 QVariant 当成回写引用

```cpp
QVariant value = reference;
value = 10; // 只改 value
```

需要写回时执行 `reference = value`。

### 6.3 新代码继续依赖旧头文件

Qt 6.15 起该类型已弃用。新代码使用 `QVariant::Reference`，旧代理只在兼容旧 API 时保留。

## API 速查表
| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QVariantRef(const Pointer *)` | 保存旧式间接 pointer 地址 | 被引用 Pointer 不能提前销毁 |
| `operator QVariant()` | 读取元素为值 | 得到副本，不持续绑定 |
| `operator=(const QVariant &)` | 把 variant 写回元素 | 依赖旧式间接访问实现 |
| `operator=(const QVariantRef &)` | 读取源代理并写入目标 | 不是交换 |
| `operator=(QVariantRef &&)` | 右值代理写回 | 不转移元素所有权 |
| `swap(QVariantRef, QVariantRef)` | 交换两个底层元素内容 | 可能复制或转换 |

## 8. 一句话总结

`QVariantRef` 是 Qt 6.15 起弃用的旧式可写元素代理：它借用一个 `Pointer` 地址，把读取转成 `QVariant`、把赋值转发回容器；新代码应迁移到按值保存 `Indirect` 的 `QVariant::Reference`。
