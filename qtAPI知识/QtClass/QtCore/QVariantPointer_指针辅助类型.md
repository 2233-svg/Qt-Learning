# QVariantPointer 旧式代理指针笔记

> 适用版本：Qt 6.11.1  
> 弃用状态：Qt 6.15 起弃用，推荐 `QVariant::Pointer`  
> 头文件：`#include <QVariantPointer>`  
> 所属模块：`Qt6::Core`  
> 类型性质：保存旧式 `Pointer` 地址并生成 `QVariantRef` 的兼容代理

## 1. 它解决什么问题

`QVariantPointer<Pointer>` 是旧式元容器迭代器使用的 pointer 代理。它让旧 iterator 的 `operator->()` 可以返回一个“指针样式”的对象：

- `operator*()` 返回 `QVariantRef<Pointer>`；
- `operator->()` 返回底层 `Pointer` 的副本；
- `QVariantRef` 再负责把元素读成 `QVariant` 或写回底层元素。

它不是 `T *`、不是智能指针，也不管理 `Pointer` 的生命周期。Qt 6.15 起已弃用，新的元容器接口使用 `QVariant::Pointer<Indirect>`。

## 2. 实际使用场景

### 2.1 旧式可写 iterator 的间接访问

```cpp
QVariantPointer<Iterator> pointer = iterator.operator->();

QVariantRef<Iterator> reference = *pointer;
reference = QVariant(42);
```

迁移后的写法：

```cpp
QVariant::Pointer<Iterator> pointer = iterator.operator->();
*pointer = QVariant(42);
```

### 2.2 读取底层 Pointer

```cpp
Pointer underlying = pointer.operator->();
```

这里的 `operator->()` 返回的是 `Pointer`，不是原始元素指针。它主要用于旧式迭代器适配协议，不应据此假设可以访问元素成员。

## 3. 生命周期和所有权

- `QVariantPointer` 内部只保存 `const Pointer *`；
- 它不复制底层 pointer 对象；
- 被引用的 `Pointer` 必须在代理使用期间保持有效；
- 底层 iterator 失效时，所有相关代理都失效；
- 容器插入、删除、扩容和 detach 都可能让代理悬空；
- `operator*()` 得到的 `QVariantRef` 只是短期写回代理；
- 任何代理都不会取得容器、iterator 或元素的所有权。

从临时 `Pointer` 构造后长期保存 `QVariantPointer` 是错误用法。

## 4. 逐项 API 说明

### `explicit QVariantPointer(const Pointer *pointer)`

保存旧式 `Pointer` 的地址。构造函数不复制 pointer，也不验证它指向的底层 iterator 是否有效。

传入地址必须在 `QVariantPointer` 的整个使用期间保持有效。

### `QVariantRef<Pointer> operator*() const`

构造并返回一个 `QVariantRef<Pointer>`，用于读取或写回当前旧式间接元素：

```cpp
QVariantRef<Iterator> reference = *pointer;
QVariant value = reference;
reference = value;
```

返回的是代理，不是真实元素引用。

### `Pointer operator->() const`

返回保存的 `Pointer` 对象副本。这个名字来自旧式 iterator 的 pointer 适配接口，不能理解为“返回元素对象指针”。

如果 `Pointer` 本身再提供某种访问接口，应遵守其自身契约；`QVariantPointer` 不会自动提供 `member` 访问。

## 5. 与新 API 的对应关系

| 旧 API | 新 API |
| --- | --- |
| `QVariantPointer<Pointer>` | `QVariant::Pointer<Indirect>` |
| `operator*()` 返回 `QVariantRef` | `operator*()` 返回 `QVariant::Reference` |
| `operator->()` 返回 `Pointer` | 新嵌套代理不提供同名真实指针入口 |

新代理按值保存 `Indirect`，不再借用 `Pointer *` 地址，生命周期关系更清晰。

## 6. 常见错误

### 6.1 写 `pointer->member`

`QVariantPointer::operator->()` 返回 `Pointer`，不是底层元素类型指针。它不保证存在可以访问的 `member`。

### 6.2 保存代理跨越 iterator 失效点

容器修改后重新取得 iterator 和 `QVariantPointer`，不要继续使用旧代理。

### 6.3 从临时 Pointer 构造

```cpp
// pointer 指向的临时对象很快销毁，代理随后悬空
QVariantPointer<Iterator> pointer = makePointer();
```

旧类型的构造函数需要的是 `const Pointer *`，尤其要检查传入地址的生命周期。

### 6.4 新代码依赖旧式 pointer 协议

Qt 6.15 起已弃用。新代码直接使用 `QVariant::Pointer` 和元容器 iterator 的标准返回类型。

## API 速查表
| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QVariantPointer(const Pointer *)` | 保存旧式 Pointer 地址 | Pointer 必须长期有效 |
| `operator*()` | 返回 `QVariantRef<Pointer>` | 不是元素引用，写回依赖旧式代理 |
| `operator->()` | 返回 Pointer 副本 | 不是元素指针，不提供自动成员访问 |
| `~QVariantPointer()` | 销毁代理 | 不销毁 Pointer 或元素 |

## 8. 一句话总结

`QVariantPointer` 是 Qt 6.15 起弃用的旧式 pointer 代理：它借用一个 `Pointer *`，`operator*()` 生成 `QVariantRef`，`operator->()` 返回底层 pointer 副本；新代码应使用按值保存 `Indirect` 的 `QVariant::Pointer`。
