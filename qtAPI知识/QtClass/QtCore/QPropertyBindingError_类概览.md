# Qt QPropertyBindingError：属性绑定求值错误

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QPropertyBindingError>`  
> 所属模块：`Qt6::Core`  
> 类型性质：可复制、可移动的隐式共享错误值

## 1. 它解决什么问题

`QPropertyBindingError` 描述 Qt 属性绑定求值过程中发生的错误。它由 `QPropertyBinding<T>::error()` 或 `QUntypedPropertyBinding::error()` 返回，让调用者区分绑定环、求值异常和其他错误，并读取可选的诊断文本。

```cpp
QPropertyBindingError error = property.binding().error();
if (error.hasError()) {
    qWarning() << error.type() << error.description();
}
```

它适合：

- 检查一个当前绑定为何没有正常得到结果；
- 在调试面板或日志里记录绑定错误；
- 由属性系统、QML 适配层或自定义绑定基础设施传递错误；
- 在不抛异常的 API 边界上携带错误类型和说明。

它不是异常对象，也不会自动修复绑定。发现错误后，仍要回到绑定依赖和求值逻辑中排查。

## 2. 获取错误的正确入口

错误属于“绑定”，不是属性值本身：

```cpp
auto binding = property.binding();
QPropertyBindingError error = binding.error();
```

如果属性当前没有绑定，`binding()` 返回空绑定，通常也不会得到有效错误。错误状态主要反映绑定最近一次求值时记录的失败。

检查顺序可以写成：

```cpp
const auto binding = property.binding();
if (binding.isNull())
    return;

const auto error = binding.error();
if (!error.hasError())
    return;

switch (error.type()) {
case QPropertyBindingError::BindingLoop:
    qWarning() << "binding loop:" << error.description();
    break;
case QPropertyBindingError::EvaluationError:
case QPropertyBindingError::UnknownError:
    qWarning() << error.description();
    break;
case QPropertyBindingError::NoError:
    break;
}
```

## 3. 四种错误类型

### 3.1 `NoError`

绑定求值没有记录错误。默认构造的 `QPropertyBindingError` 就是这个状态：

- `hasError()` 返回 `false`；
- `type()` 返回 `NoError`；
- `description()` 返回空字符串。

### 3.2 `BindingLoop`

属性直接或间接依赖自己，绑定求值因循环依赖而停止。

```text
A depends on B
B depends on C
C depends on A
```

排查时不要只找直接的 `A -> A`；实际循环经常跨多个派生属性、回调和适配层。

### 3.3 `EvaluationError`

绑定表达式求值失败，但原因不是绑定环。例如 QML 引擎在绑定求值期间遇到异常时可以使用这个错误类型。

纯 C++ 绑定 functor 中的具体失败如何映射到这一类型，取决于创建和执行绑定的设施；不要假定任意 C++ 异常都会自动变成 `EvaluationError`。

### 3.4 `UnknownError`

错误确实存在，但其他类型都不合适。此时 `description()` 尤其重要，但描述也可能为空，调用方仍需保留上下文日志。

## 4. `hasError()`、`type()` 与 `description()`

```cpp
if (error.hasError()) {
    const auto kind = error.type();
    const QString message = error.description();
}
```

- `hasError()` 是最直接的“有无错误”判断；
- `type()` 用于程序分支和分类统计；
- `description()` 面向诊断，可能提供更具体信息。

不要用 `description().isEmpty()` 代替 `hasError()`：一个有效错误允许没有描述文本，默认无错误状态才保证为空描述。

## 5. 值语义与移动后状态

`QPropertyBindingError` 内部使用共享数据，复制成本较低：

```cpp
QPropertyBindingError copy = error;
```

复制后两者表达相同错误。移动构造或移动赋值会把源对象恢复到默认状态：

```cpp
QPropertyBindingError moved = std::move(error);
Q_ASSERT(!error.hasError());
Q_ASSERT(error.type() == QPropertyBindingError::NoError);
```

因此移动后的源对象仍可析构和重新赋值，但不再保留原错误。

## 6. 诊断策略

### 6.1 绑定环

看到 `BindingLoop` 时，优先记录：

- 当前目标属性；
- 绑定表达式创建位置；
- 表达式读取了哪些源属性；
- 变化回调里是否又写回了依赖链；
- 是否有双向绑定或同步桥接。

Qt 的 source-location 支持可以帮助绑定记录创建位置，但最终可见诊断取决于构建配置和具体绑定设施。

### 6.2 求值错误

看到 `EvaluationError` 时，检查绑定求值中的：

- 空指针和已销毁 QObject；
- 越界、解析失败和无效转换；
- 调用外部脚本或 QML 时抛出的异常；
- functor 捕获对象的生命周期；
- 表达式是否依赖尚未初始化的状态。

### 6.3 保留上下文

`description()` 不是结构化日志。生产日志最好同时记录错误类型、属性名、对象类型和业务操作，不要只输出一条可能为空的描述。

## 7. 手工构造错误

该类提供公开构造函数：

```cpp
QPropertyBindingError error(
    QPropertyBindingError::EvaluationError,
    QStringLiteral("Failed to evaluate user expression"));
```

这适合自定义属性绑定适配层内部传递错误。普通 `QProperty` 使用者多数只需读取 `binding().error()`，无需手工创建。

传入 `NoError` 和非空描述虽然类型上可行，但语义矛盾；无错误状态应使用默认构造。

## 8. 常见错误

### 8.1 只检查描述是否为空

错误可以没有描述。先调用 `hasError()`，再读 `type()` 和 `description()`。

### 8.2 把 `BindingLoop` 当作线程死锁

它指属性依赖图的循环，不是 mutex 死锁，也不表示线程互相等待。

### 8.3 认为错误对象会持续实时更新

`QPropertyBindingError` 是取出时的值。要观察后续绑定状态，应重新从绑定读取错误或在相关属性通知后检查。

### 8.4 只打印 `UnknownError`

枚举名信息很少。应连同 `description()`、绑定目标和创建上下文一起记录。

### 8.5 移动后继续读取原错误

Qt 文档明确约定移动后的源对象回到默认状态；原错误已经在目标对象中。

## 9. 逐项 API 语义

### 枚举

| API | 值 | 语义 |
| --- | ---: | --- |
| `QPropertyBindingError::NoError` | `0` | 绑定求值没有错误。 |
| `QPropertyBindingError::BindingLoop` | `1` | 属性直接或间接依赖自身，求值被停止。 |
| `QPropertyBindingError::EvaluationError` | `2` | 求值发生非循环错误，例如适配层执行绑定时遇到异常。 |
| `QPropertyBindingError::UnknownError` | `3` | 其他类型都不适用的通用错误。 |

### 构造、复制与移动

| API | 语义 | 边界 |
| --- | --- | --- |
| `QPropertyBindingError()` | 创建无错误对象。 | `hasError() == false`，描述为空。 |
| `QPropertyBindingError(Type type, const QString &description = QString())` | 创建指定类型和描述的错误。 | `NoError` 通常应配空描述。 |
| `QPropertyBindingError(const QPropertyBindingError &other)` | 复制错误值。 | 内部隐式共享，语义独立。 |
| `operator=(const QPropertyBindingError &other)` | 复制赋值。 | 覆盖当前错误。 |
| `QPropertyBindingError(QPropertyBindingError &&other)` | 移动错误值。 | `other` 回到默认无错误状态。 |
| `operator=(QPropertyBindingError &&other)` | 移动赋值。 | 覆盖自身，源对象回到默认状态。 |
| `~QPropertyBindingError()` | 释放错误值。 | 不影响产生该错误的绑定对象。 |

### 查询

| API | 语义 | 边界 |
| --- | --- | --- |
| `bool hasError() const` | 判断是否存在错误。 | 比检查描述是否为空可靠。 |
| `Type type() const` | 返回错误分类。 | 无错误时为 `NoError`。 |
| `QString description() const` | 返回可选诊断文字。 | 有错误时也可能为空；不要解析成稳定机器协议。 |
| `binding.error() const` | 从 typed 或 untyped property binding 读取错误。 | 返回的是错误值快照。 |

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 获取 | `property.binding().error()` | 读取当前绑定记录的求值错误。 | 先确认属性确实有绑定。 |
| 判断 | `hasError()` | 判断错误是否存在。 | 不要用空描述代替。 |
| 分类 | `type()` | 区分环、求值失败和未知错误。 | `BindingLoop` 不是线程死锁。 |
| 说明 | `description()` | 获取面向诊断的附加文本。 | 可能为空，也不是稳定协议。 |
| 创建 | `QPropertyBindingError(type, text)` | 为自定义绑定设施创建错误值。 | 普通属性使用者通常只读取。 |
| 传递 | 复制/移动构造与赋值 | 跨 API 保存或传递错误。 | 移动后源对象恢复默认状态。 |

---

### 一句话总结

`QPropertyBindingError` 是绑定求值失败的值对象：先用 `hasError()` 判断，再结合 `type()`、`description()` 和绑定上下文定位依赖环或求值故障。
