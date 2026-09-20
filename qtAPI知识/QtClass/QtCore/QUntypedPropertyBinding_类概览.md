# Qt QUntypedPropertyBinding：类型擦除的属性绑定句柄

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QUntypedPropertyBinding>`  
> 所属模块：`Qt6::Core`  
> 自 Qt：6.0  
> 类型性质：可复制、可移动的类型擦除绑定值

## 1. 它解决什么问题

`QUntypedPropertyBinding` 表示一个不在 C++ 类型中携带属性值类型的绑定句柄。它保留绑定的运行时 `QMetaType`、错误状态和内部求值函数，供 `QBindable`、元对象属性适配器以及 `setBinding(const QUntypedPropertyBinding &)` 使用。

```cpp
QProperty<int> source(10);
QProperty<int> target;

QPropertyBinding<int> typed = Qt::makePropertyBinding(source);
QUntypedPropertyBinding untyped = typed;

if (target.setBinding(untyped))
    qDebug() << target.value();
```

业务代码如果知道 `T`，优先使用 `QPropertyBinding<T>`。untyped 版本适合属性类型只在运行时确定、需要通用适配器，或在 `QBindable`/`QMetaProperty` 边界传递。

## 2. typed 与 untyped 的关系

```text
QPropertyBinding<T>
  编译期知道结果类型 T
  可以直接安装到 QProperty<T>

QUntypedPropertyBinding
  只在运行时携带 QMetaType
  用于通用属性接口和类型适配
  安装前必须检查目标属性的元类型
```

`QPropertyBinding<T>` 公开继承 `QUntypedPropertyBinding`。从 typed 转成 untyped 通常是安全的；反向转换由 Qt 内部或调用者在确认类型匹配后完成。

## 3. null 状态

默认构造对象是 null binding：

```cpp
QUntypedPropertyBinding binding;
Q_ASSERT(binding.isNull());
Q_ASSERT(!binding.valueMetaType().isValid());
```

移动构造和移动赋值后，源对象也进入 null 状态：

```cpp
QUntypedPropertyBinding moved = std::move(binding);
Q_ASSERT(binding.isNull());
```

null 绑定常用于：

- 表示属性没有绑定；
- 传给 `setBinding()` 以清除已有绑定；
- 表示 `takeBinding()` 没有取出任何东西；
- 作为类型擦除 API 的无效/空结果。

## 4. 安装和移除绑定

`QUntypedPropertyBinding` 自身没有 `setBinding()`。它是绑定值，不是属性容器；实际安装发生在：

```cpp
property.setBinding(untyped);
bindable.setBinding(untyped);
```

目标属性会检查：

```cpp
if (!untyped.isNull() && untyped.valueMetaType() != targetMetaType)
    return false;
```

类型不匹配时不能强行安装。不要只依赖 `static_cast<QPropertyBinding<T>>` 绕过检查，错误的类型会破坏绑定求值的数据写入约定。

清除绑定通常传入默认构造的空对象：

```cpp
target.setBinding(QUntypedPropertyBinding{});
```

## 5. `valueMetaType()` 的边界

```cpp
QMetaType type = binding.valueMetaType();
```

有效绑定返回它产生的属性类型，例如 `QMetaType::fromType<int>()`。null binding 返回无效 `QMetaType`。

`QMetaType` 只说明绑定结果的运行时类型，不代表：

- 绑定当前求值一定成功；
- 目标属性一定接受它；
- 绑定表达式捕获的对象仍然有效；
- 绑定一定没有循环依赖。

类型匹配和错误检查是两个独立步骤。

## 6. `error()` 的语义

```cpp
QPropertyBindingError error = binding.error();
if (error.hasError())
    qWarning() << error.type() << error.description();
```

`error()` 返回绑定记录的错误状态。详细错误类别见 `QPropertyBindingError`：

- `NoError`；
- `BindingLoop`；
- `EvaluationError`；
- `UnknownError`。

绑定句柄是值对象，`error()` 得到的也是错误值快照。绑定后续重新求值，应该重新读取 `binding().error()`，不要长期缓存旧错误来代表当前状态。

## 7. 拷贝、移动和内部所有权

`QUntypedPropertyBinding` 可以复制和移动。复制是共享内部绑定状态的值语义，移动则把句柄转移给目标对象并让源对象变 null。

```cpp
QUntypedPropertyBinding first = makeBinding();
QUntypedPropertyBinding copy = first;          // 两个句柄指向同一绑定状态
QUntypedPropertyBinding moved = std::move(first);
```

复制句柄不会把绑定安装到第二个属性，也不会复制出第二套依赖图。它只是复制“对同一个绑定对象的值句柄”。想让两个属性分别绑定，需要把同一 binding 安装到两个目标属性，并确认绑定表达式的捕获生命周期适用。

## 8. 真实使用场景

### 8.1 通用属性转发器

```cpp
bool installBinding(QBindable<int> destination,
                    const QUntypedPropertyBinding &binding)
{
    return destination.setBinding(binding);
}
```

适配器不需要知道 binding 在上游如何创建，只需在目标边界检查类型。

### 8.2 暂存并迁移绑定

```cpp
QUntypedPropertyBinding saved = target.takeBinding();
// target 暂时没有绑定
otherTarget.setBinding(saved);
```

迁移后仍要保证绑定表达式捕获的源属性和对象都活着。

### 8.3 通过 `QBindable` 清除

```cpp
auto bindable = object.bindableTitle();
bindable.setBinding(QUntypedPropertyBinding{});
```

清除后属性保留当前值，但不再由原 binding 自动更新。

## 9. 常见错误

### 9.1 把 null binding 当成有效绑定

先用 `isNull()` 判断。null 的 `valueMetaType()` 无效，`error()` 也没有“最近一次有效求值”的意义。

### 9.2 只检查类型，不检查错误

`valueMetaType()` 正确只能说明结果类型正确；binding 仍可能处于循环或求值错误状态。

### 9.3 以为复制会产生独立绑定

复制的是句柄和共享状态，不是独立依赖图。

### 9.4 用错误的 untyped binding 强行转换

先比较目标 `QMetaType`。类型擦除不是绕过类型安全的许可。

### 9.5 从绑定中保存悬空引用

句柄本身不会延长 lambda 捕获对象的生命周期。迁移 binding 后，捕获对象仍需保持有效。

## 10. 逐项 API 语义

### 构造与赋值

| API | 语义 | 边界 |
| --- | --- | --- |
| `QUntypedPropertyBinding()` | 创建 null binding。 | `isNull() == true`，元类型无效。 |
| `QUntypedPropertyBinding(const QUntypedPropertyBinding &other)` | 复制 binding 句柄。 | 共享内部绑定状态，不复制依赖图。 |
| `QUntypedPropertyBinding(QUntypedPropertyBinding &&other)` | 移动 binding 句柄。 | `other` 变为 null。 |
| `operator=(const QUntypedPropertyBinding &other)` | 复制赋值。 | 覆盖当前句柄。 |
| `operator=(QUntypedPropertyBinding &&other)` | 移动赋值。 | 源对象变为 null。 |
| `~QUntypedPropertyBinding()` | 释放句柄引用。 | 不等于从属性上卸载 binding。 |

### 查询

| API | 语义 | 边界 |
| --- | --- | --- |
| `bool isNull() const` | 判断是否为默认或移动后的空句柄。 | 只有这两类状态保证为 true。 |
| `QMetaType valueMetaType() const` | 返回 binding 的结果元类型。 | null binding 返回 invalid `QMetaType`。 |
| `QPropertyBindingError error() const` | 返回 binding 的错误状态。 | 是错误值快照，不主动重新求值。 |

### 协作 API

| API | 语义 | 边界 |
| --- | --- | --- |
| `QProperty<T> / QObjectBindableProperty::setBinding(untyped)` | 把类型擦除 binding 安装到目标属性。 | 非空且类型不匹配时返回 `false`。 |
| `QBindable<T>::setBinding(untyped)` | 通过 bindable 接口安装 binding。 | 还要满足 bindable 可写且支持绑定。 |
| `property.takeBinding()` | 取出 typed/untyped binding。 | 属性保留当前值并解除自动更新。 |
| `setBinding(QUntypedPropertyBinding{})` | 用空 binding 清除目标属性上的 binding。 | 空对象本身不是一个可求值表达式。 |

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 空值 | `QUntypedPropertyBinding()` | 表示没有绑定。 | `valueMetaType()` 无效。 |
| 复制 | 复制构造、复制赋值 | 复制 binding 句柄。 | 共享状态，不生成独立依赖图。 |
| 移动 | 移动构造、移动赋值 | 转移 binding 句柄。 | 源对象变 null。 |
| 判断 | `isNull()` | 判断是否为空句柄。 | 先判断再查询类型或错误。 |
| 类型 | `valueMetaType()` | 获取绑定结果的运行时元类型。 | 类型正确不代表求值成功。 |
| 错误 | `error()` | 获取绑定求值错误状态。 | 重新求值后要重新读取。 |
| 安装 | `setBinding(untyped)` | 将通用 binding 安装到属性。 | 检查目标类型和 bindable 可写性。 |
| 清除 | `setBinding(QUntypedPropertyBinding{})` | 移除目标属性绑定。 | 属性保留当前值。 |

---

### 一句话总结

`QUntypedPropertyBinding` 是类型擦除的绑定句柄：它携带运行时元类型和错误状态，但不负责安装自身，类型匹配与捕获生命周期必须由目标和调用者共同保证。
