# Qt QPropertyData：属性绑定系统的底层值存储

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QPropertyData>`  
> 所属模块：`Qt6::Core`  
> 继承：`QUntypedPropertyData -> QPropertyData<T>`  
> 派生：`QProperty<T>`、`QObjectBindableProperty<...>`  
> 类型性质：主要供属性实现继承的低层模板基类

## 1. 它解决什么问题

`QPropertyData<T>` 只负责保存一个 `T`，并提供绕过绑定系统的底层读写入口。`QProperty<T>` 和 `QObjectBindableProperty` 在它上面补充绑定、依赖登记、变化通知和 QObject 协作。

```text
QPropertyData<T>
  val: T
  valueBypassingBindings()
  setValueBypassingBindings(...)
       ▲
       ├─ QProperty<T>
       └─ QObjectBindableProperty<...>
```

它适合：

- Qt 属性实现的公共数据层；
- 自定义 bindable property 适配器需要直接访问存储值；
- signal 回调需要取出已经写入的底层值而不再次建立依赖；
- 调试或底层桥接中明确绕过绑定机制。

它不是普通业务代码首选的属性类型。绝大多数场景应调用 `QProperty<T>::value()` / `setValue()` 或 `QObjectBindableProperty::value()` / `setValue()`，而不是直接使用 bypass API。

## 2. 为什么 bypass API 危险

`QPropertyData` 的低层接口不会参与绑定系统：

- 读取不触发当前绑定求值；
- 读取不把属性登记为当前绑定的依赖；
- 写入不移除当前绑定；
- 写入不通知观察者和依赖属性；
- 已有绑定时，读取到底层值可能得到过期数据。

```cpp
QProperty<int> source(1);
QProperty<int> target([&] { return source.value() + 1; });

target.setValueBypassingBindings(99);
// target 的绑定关系仍在，但底层 val 被改成了 99。
// 后续 target.value() 可能重新求值并覆盖这个底层值。
```

这类行为在内部实现中有用途，但对业务代码通常是错误信号。

## 3. 与 QProperty 的正常 API 对比

```cpp
property.value();                 // 正常：读取时登记依赖
property.setValue(value);         // 正常：移除绑定、写值、通知

property.valueBypassingBindings();       // 低层：只读 val
property.setValueBypassingBindings(value); // 低层：只写 val
```

选择原则：

- 要表达业务状态变化：使用正常 API；
- 要实现 signal 回调、属性适配器或 Qt 内部桥接：才考虑 bypass API；
- 要绕过绑定时，必须在调用点写清楚后续如何恢复一致性。

## 4. 类型别名与值传递

`QPropertyData<T>` 根据 `T` 的类别定义类型别名：

- `value_type`：就是 `T`；
- `parameter_type`：对算术、枚举、指针通常按值传递，对其他类型通常是 `const T &`；
- `rvalue_ref`：对需要移动的大对象提供 `T &&`；
- `arrow_operator_result`：为指针或可解引用类型支持 `operator->()` 的返回形式。

因此文档签名中的 `parameter_type` 不是另一个业务类型，而是 Qt 根据 `T` 自动选择的参数传递策略。

## 5. 读取 `valueBypassingBindings()`

```cpp
const auto raw = property.valueBypassingBindings();
```

它直接返回存储在 `val` 中的数据，不触发绑定系统。

若属性当前安装了绑定，`val` 可能是上一次存储的值，而真正的当前值需要通过 `QProperty::value()` 触发/读取绑定求值。不要用 bypass 读值来判断绑定属性当前对外可见的结果。

适合的例子是 `QObjectBindableProperty` 内部触发带值 signal 时读取刚刚写入的底层值：

```cpp
signalCallBack(this->valueBypassingBindings());
```

这里的目的不是建立一个新的依赖，而是把已经确定的值传给回调。

## 6. 写入 `setValueBypassingBindings()`

```cpp
property.setValueBypassingBindings(value);
```

它直接覆盖 `val`：

- 不移除当前 binding；
- 不检查新旧值是否相等；
- 不调用 `notify()`；
- 不触发 QObject NOTIFY signal；
- 不更新依赖属性。

如果绑定仍然存在，后续正常求值可能覆盖该值；如果绑定依赖链没有再次触发，这个不一致可能暂时隐藏。因此除非正在实现底层适配，不要用它替代 `setValue()`。

## 7. 继承与访问级别

`QPropertyData<T>` 的构造函数和底层 `val` 主要为派生类准备。业务代码通常不会直接实例化它来代替 `QProperty<T>`，因为它没有公开的绑定生命周期和通知协议。

两个派生类的差异：

- `QProperty<T>` 自己持有绑定数据；
- `QObjectBindableProperty` 把绑定数据放入所属 QObject 的绑定存储；
- 两者都复用 `QPropertyData<T>` 的 `val` 和 bypass API。

## 8. 真实使用场景

### 8.1 内部 signal 回调

`QObjectBindableProperty` 在写值后需要发出 signal，但不希望通过 `value()` 重新登记依赖，此时可以用 `valueBypassingBindings()` 取得已写入的原始值。

### 8.2 自定义绑定适配器

当一层通用接口已经负责通知和绑定管理，底层存储层可以只用 bypass API 搬运数据，避免重复注册依赖或递归通知。

### 8.3 单元测试底层状态

测试 Qt 属性实现时，bypass API 可以用来验证“存储值”和“绑定公开值”之间的差别。但测试应明确这是实现层行为，不要把它当作普通应用契约。

## 9. 常见错误

### 9.1 用 bypass API 代替 setter

这会绕过通知和绑定，使界面或派生属性不更新。

### 9.2 已有绑定时读取 bypass 值

可能读到旧值。对外语义应使用 `value()`。

### 9.3 写入后等待自动通知

bypass 写入没有通知。需要让依赖刷新，应使用正常 setter，或由底层实现明确调用通知机制。

### 9.4 以为相等值会自动跳过

`setValueBypassingBindings()` 只是赋值，不执行 `operator==` 检查。

### 9.5 把它当独立 bindable 属性

它本身没有 `setBinding()`、`onValueChanged()` 或 `notify()`。这些能力由派生类提供。

## 10. 逐项 API 语义

### 类型别名

| API | 语义 | 边界 |
| --- | --- | --- |
| `using value_type = T` | 表示底层存储类型。 | 与模板参数相同。 |
| `using parameter_type` | 按 `T` 的性质选择值传递或 const 引用。 | 调用者通常不需要手写具体展开类型。 |
| `using rvalue_ref` | 对适合移动的类型提供右值引用参数。 | 算术、枚举、指针类型可能没有可用的右值重载。 |
| `using arrow_operator_result` | 支持派生属性的 `operator->()` 返回策略。 | 只对指针或可解引用类型有意义。 |

### 构造与析构

| API | 语义 | 边界 |
| --- | --- | --- |
| `QPropertyData()` | 默认构造 `val`。 | `T` 需要可默认构造。 |
| `QPropertyData(parameter_type t)` | 用值构造底层存储。 | 主要供派生类初始化。 |
| `QPropertyData(rvalue_ref t)` | 移动构造底层存储。 | 适合大对象或 move-only 值。 |
| `~QPropertyData()` | 销毁底层值。 | 不负责绑定观察器，那由派生类管理。 |

### 绕过绑定的访问

| API | 语义 | 边界 |
| --- | --- | --- |
| `parameter_type valueBypassingBindings() const` | 直接返回 `val`。 | 可能过期；不登记依赖。 |
| `void setValueBypassingBindings(parameter_type v)` | 直接复制写入 `val`。 | 不移除绑定、不通知、不比较。 |
| `void setValueBypassingBindings(rvalue_ref v)` | 直接移动写入 `val`。 | 不移除绑定、不通知；移动后的实参状态由 C++ 规则决定。 |

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型 | `value_type`、`parameter_type`、`rvalue_ref` | 描述底层值和参数传递形式。 | 由模板参数 `T` 决定。 |
| 读取 | `valueBypassingBindings()` | 直接读取底层 `val`。 | 可能过期，不登记依赖。 |
| 写入 | `setValueBypassingBindings(...)` | 直接写底层 `val`。 | 不通知、不拆绑定、不比较。 |
| 派生 | `QProperty<T>` | 在底层值上加完整绑定能力。 | 业务代码优先使用它。 |
| 派生 | `QObjectBindableProperty` | 在 QObject 成员中复用底层存储。 | 通过宏声明并由 owner 管理绑定存储。 |

---

### 一句话总结

`QPropertyData<T>` 是 Qt 属性实现的底层存储层；它的 bypass API 很有用，但故意绕过依赖追踪和通知，应用代码应把它当作低层工具而不是普通 setter/getter。
