# QVariantConstPointer 旧式只读代理指针笔记

> 适用版本：Qt 6.11.1  
> 弃用状态：Qt 6.15 起弃用，推荐 `QVariant::ConstPointer`  
> 头文件：`#include <QVariantConstPointer>`  
> 所属模块：`Qt6::Core`  
> 类型性质：保存一个 `QVariant` 值并提供只读指针样式访问

## 1. 它解决什么问题

`QVariantConstPointer` 是 Qt 旧式容器代理体系中的只读 pointer 类型。它和 `QVariantPointer<Pointer>` 不同：

- `QVariantPointer` 保存的是旧式 `Pointer *`，服务于 iterator 元素代理；
- `QVariantConstPointer` 直接保存一个 `QVariant` 对象；
- `operator*()` 返回一个 `QVariant` 值；
- `operator->()` 返回指向内部 `QVariant` 的只读指针。

它不提供元素写回能力，也不拥有任何外部容器或元素。Qt 6.15 起它已弃用，新代码应优先使用 `QVariant::ConstPointer<Indirect>` 或直接使用 `QVariant`。

## 2. 实际使用场景

### 2.1 对一个 QVariant 做只读代理

```cpp
QVariant value = QStringLiteral("hello");
QVariantConstPointer pointer(value);

const QVariant copy = *pointer;
const QString text = pointer->toString();
```

`operator*()` 返回的是 `QVariant` 值副本；`operator->()` 让调用方可以直接调用 `QVariant` 的 const 成员函数。

### 2.2 兼容旧式泛型接口

旧代码可能把“元素代理”抽象成：

```cpp
template <typename Pointer>
void inspect(Pointer pointer)
{
    qDebug() << pointer->metaType().name();
}
```

`QVariantConstPointer` 可以作为这种接口的只读 variant 包装，但它只是兼容类型，不应作为新 API 的基础设计。

## 3. 构建与包含

```cpp
#include <QVariantConstPointer>
```

Qt 6.15 起该头文件对应的类型已弃用。新代码通常只需：

```cpp
#include <QVariant>
```

然后直接保存 `QVariant`，或使用 `QVariant::ConstPointer` 处理元容器 iterator。

## 4. 核心使用模型

### 4.1 构造时复制 QVariant

```cpp
QVariant source = QStringLiteral("hello");
QVariantConstPointer pointer(source);
```

构造函数按值接收 `QVariant`，因此代理保存自己的 `QVariant` 成员。后续修改 `source` 不会改变 `pointer` 内部的 variant。

### 4.2 `operator*()` 返回值，不返回引用

```cpp
QVariant copy = *pointer;
```

这个操作产生一个 `QVariant` 值。修改 `copy` 不会改变 `pointer` 内部的 variant。

### 4.3 `operator->()` 才返回只读地址

```cpp
const QVariant *address = pointer.operator->();
if (address->isValid())
    qDebug() << address->typeName();
```

返回的地址指向 `pointer` 内部成员，只在 `pointer` 不被销毁或移动、且没有改变其内部布局的期间有效。它不是外部元素地址。

## 5. 生命周期、复制和所有权

- `QVariantConstPointer` 按值保存一个 `QVariant`；
- 它不借用构造参数的外部存储；
- 它不拥有裸指针 variant 内部所指向的 QObject 或其他对象；
- 复制 `QVariantConstPointer` 会复制其 variant 的值语义；
- `operator->()` 返回的地址不能超过代理对象生命周期；
- 该类型不提供写入内部 variant 的 API；
- 如果内部 variant 保存裸指针，代理的复制不会延长裸指针目标的生命周期。

它的“const”只约束代理对内部 `QVariant` 的访问，不会把 variant 中保存的裸指针目标对象变成 const，也不改变其所有权。

## 6. 逐项 API 说明

### `explicit QVariantConstPointer(QVariant variant)`

按值保存一个 `QVariant`：

```cpp
QVariantConstPointer pointer(QVariant(42));
```

临时 variant 在构造调用结束后仍然安全，因为对象已经保存了自己的 `QVariant` 成员。内部值是否使用隐式共享由 Qt 实现决定，但对外保持值语义。

### `QVariant operator*() const`

返回内部 variant 的值副本。它不返回 `QVariant &`，因此：

```cpp
QVariant copy = *pointer;
copy.clear(); // 不影响 pointer 内部的 variant
```

### `const QVariant *operator->() const`

返回指向内部 `QVariant` 成员的只读指针。它用于方便调用：

```cpp
if (pointer->canConvert<int>()) {
    const int number = pointer->toInt();
}
```

返回地址只在 `pointer` 存活期间有效。不要保存到代理外部长期使用。

## 7. 与新式 `QVariant::ConstPointer` 的区别

| 类型 | 内部保存 | `operator*()` | `operator->()` | 用途 |
| --- | --- | --- | --- | --- |
| `QVariantConstPointer` | 一个 `QVariant` 值 | 返回 `QVariant` 副本 | 返回 `const QVariant *` | 旧式 variant 只读包装 |
| `QVariant::ConstPointer<Indirect>` | `Indirect` 访问器 | 返回 `ConstReference` | 不提供真实箭头访问 | 元容器只读 iterator 适配 |

两者名字相近，但不是同一个抽象。迁移时要先确认旧代码是在包装一个现成 `QVariant`，还是在适配元容器 iterator。

## 8. 常见错误

### 8.1 以为 `operator*()` 返回引用

```cpp
(*pointer).clear(); // 修改的是临时副本
```

需要判断或读取可以这样写；但它不会修改 `pointer` 内部值。

### 8.2 保存 `operator->()` 返回地址过久

代理销毁后，返回的 `const QVariant *` 立即失效。只在表达式或受控作用域内使用。

### 8.3 以为复制代理会管理裸指针对象

若内部 variant 保存 `QObject *`，复制 `QVariantConstPointer` 只复制指针值，不会创建对象所有权或自动跟踪销毁。

### 8.4 把它替换成嵌套 ConstPointer 而不检查语义

`QVariantConstPointer` 包装现成 `QVariant`；`QVariant::ConstPointer` 包装 `Indirect`。两者构造方式和解引用结果不同，不能机械替换。

## API 速查表
| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QVariantConstPointer(QVariant)` | 按值保存一个 variant | 不借用外部 variant 存储 |
| `operator*()` | 返回内部 variant 的值副本 | 修改副本不回写 |
| `operator->()` | 返回内部 variant 的只读地址 | 地址不能超过代理生命周期 |
| `~QVariantConstPointer()` | 销毁代理及其内部 variant | 不销毁 variant 中裸指针目标 |

## 10. 一句话总结

`QVariantConstPointer` 是 Qt 6.15 起弃用的旧式只读 variant 包装：它按值保存一个 `QVariant`，`operator*()` 返回副本，`operator->()` 返回内部只读地址；它与面向元容器 iterator 的 `QVariant::ConstPointer` 不是同一种类型。
