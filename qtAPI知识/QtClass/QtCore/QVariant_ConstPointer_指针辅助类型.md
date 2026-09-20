# QVariant::ConstPointer 只读代理指针笔记

> 适用版本：Qt 6.11.1  
> 所属模块：`Qt6::Core`  
> 定义位置：`#include <QVariant>`  
> 类型性质：保存 `Indirect` 并通过 `operator*()` 生成只读 `ConstReference` 的代理

## 1. 它解决什么问题

`QVariant::ConstPointer<Indirect>` 为 Qt 元容器的只读 iterator 提供“指针样式”的访问接口。

它的典型关系是：

- `QMetaSequence` 的只读 iterator 的 `operator->()` 返回 `QVariant::ConstPointer<ConstIterator>`；
- `QMetaAssociation` 的只读 iterator 的 `operator->()` 返回 `QVariant::ConstPointer<ConstIterator>`；
- `operator*()` 返回 `QVariant::ConstReference<Indirect>`；
- `ConstReference` 再把底层元素读成 `QVariant` 值。

它不是 `const T *`，也没有真正的 `operator->()`。名字中的 Pointer 是迭代器 traits 中的 pointer 角色，不代表它拥有或直接暴露元素地址。

## 2. 实际使用场景

### 2.1 只读遍历元序列

```cpp
auto iterator = iterable.constBegin();
if (iterator != iterable.constEnd()) {
    QVariant::ConstPointer<ConstIterator> pointer =
        iterator.operator->();

    const QVariant value = *pointer;
    qDebug() << value;
}
```

更常见的写法是直接解引用 iterator：

```cpp
for (auto it = iterable.constBegin();
     it != iterable.constEnd(); ++it) {
    const QVariant value = *it;
    qDebug() << value;
}
```

### 2.2 统一封装只读 iterator

```cpp
template <typename Pointer>
QVariant readThroughPointer(const Pointer &pointer)
{
    return *pointer;
}
```

只要 `Pointer` 的 `operator*()` 返回可转换为 `QVariant` 的只读代理，就可以用同一套只读代码处理元序列和元关联 iterator。

## 3. 构建与包含

```cpp
#include <QVariant>
#include <QMetaSequence>
#include <QMetaAssociation>
```

通常由元容器 iterator 的 `operator->()` 返回，不建议业务代码手写自定义 `Indirect`，除非正在实现一个符合 Qt 元迭代器约定的适配器。

## 4. 核心使用模型

### 4.1 保存的是 `Indirect`，不是元素地址

```cpp
QVariant::ConstPointer<ConstIterator> pointer =
    iterator.operator->();
```

代理内部保存 `Indirect` 的副本。它不会保存 `T *`，也不会复制当前元素。

### 4.2 `operator*()` 返回 `ConstReference`

```cpp
QVariant::ConstReference<ConstIterator> reference = *pointer;
const QVariant value = reference;
```

`operator*()` 的结果不是 `const T &`，而是只读间接引用代理。要得到独立的值，需要把它转换成 `QVariant` 或具体值类型。

### 4.3 没有写回路径

`ConstPointer` 和它生成的 `ConstReference` 都不支持把值写回底层容器。需要修改元素时，必须重新取得可写 iterable/iterator，并满足底层容器的写入能力。

## 5. 生命周期和失效边界

- `ConstPointer` 不拥有容器、iterator 或元素；
- 底层只读 iterator 失效后，pointer 和 reference 都失效；
- 容器销毁、重分配、detach、插入或删除都可能影响 iterator 有效性；
- 复制 pointer 只复制 `Indirect`，不是快照；
- `operator*()` 得到的 `ConstReference` 不能跨 iterator 失效点使用；
- 转成 `QVariant` 后，值可以脱离 iterator 独立保存。

## 6. 逐项 API 说明

### `ConstPointer(const Indirect &pointed)`

复制构造 `Indirect`。不复制元素，不拥有底层容器。

### `ConstPointer(Indirect &&pointed)`

移动构造 `Indirect`。适合由临时只读 iterator 创建，但仍受底层 iterator 生命周期约束。

### `operator*() const`

返回 `QVariant::ConstReference<Indirect>`：

```cpp
QVariant::ConstReference<ConstIterator> reference = *pointer;
```

该代理只能读取当前元素并转换为 `QVariant`，不能赋值和写回。

## 7. 与相邻类型的区别

| 类型 | `operator*()` 返回 | 写回 | 是否拥有对象 |
| --- | --- | --- | --- |
| `QVariant::ConstPointer` | `ConstReference` | 否 | 否 |
| `QVariant::Pointer` | `Reference` | 间接支持 | 否 |
| `const T *` | `const T &` | 否 | 否 |
| `QSharedPointer<const T>` | `const T &` | 否 | 共享拥有 |

`ConstPointer` 不提供 `operator->()`，不能把它当作真实对象指针使用。

## 8. 常见错误

### 8.1 写 `pointer->member`

`QVariant::ConstPointer` 没有 `operator->()`。应使用 `*pointer` 得到 `ConstReference`，再转换成 `QVariant` 或具体值。

### 8.2 把 `*pointer` 当成 const 元素引用

它返回的是代理，不是 `const T &`。代理转成 variant 后才得到值语义对象。

### 8.3 通过 const pointer 期待写回

只读代理没有赋值运算符。需要写入时使用可写 iterator 的 `QVariant::Pointer`/`Reference` 路径。

### 8.4 保存代理跨越容器修改

容器修改可能使 iterator 失效。只保存转换后的 `QVariant` 快照，或在修改后重新取得 iterator 和 pointer。

### 8.5 误以为复制代理就是复制元素

复制 `ConstPointer` 只复制 `Indirect`，底层元素仍然由容器管理。需要副本时执行：

```cpp
const QVariant snapshot = *pointer;
```

## API 速查表
| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `ConstPointer(const Indirect &)` | 复制只读间接访问器 | 不复制元素、不拥有容器 |
| `ConstPointer(Indirect &&)` | 移动构造只读访问器 | 仍受 iterator 生命周期限制 |
| `operator*()` | 返回只读 `ConstReference` | 不是 `const T &` |
| `~ConstPointer()` | 销毁代理 | 不销毁底层元素 |

## 10. 一句话总结

`QVariant::ConstPointer` 是元容器只读 iterator 的指针适配层：它保存 `Indirect`，`operator*()` 返回 `ConstReference`，不提供真实 `operator->()`、不支持写回，也不拥有底层元素。
