# Qt QObjectBindableProperty：嵌入 QObject 的可绑定成员属性

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QObjectBindableProperty>` 或 `#include <QProperty>`  
> 所属模块：`Qt6::Core`  
> 继承：`QPropertyData<T> -> QObjectBindableProperty<Class, T, Offset, Signal>`  
> 类型性质：供 QObject 成员使用的模板属性存储

## 1. 它解决什么问题

`QObjectBindableProperty` 用来把 Qt 6 的绑定属性直接嵌入 `QObject` 子类，并和 `Q_PROPERTY(... BINDABLE ...)`、NOTIFY signal、对象内部的 `QBindingStorage` 协作。

```cpp
class Counter : public QObject
{
    Q_OBJECT
    Q_PROPERTY(int value READ value WRITE setValue BINDABLE bindableValue NOTIFY valueChanged)

public:
    int value() const { return m_value.value(); }
    void setValue(int value) { m_value = value; }
    QBindable<int> bindableValue() { return &m_value; }

signals:
    void valueChanged();

private:
    Q_OBJECT_BINDABLE_PROPERTY(Counter, int, m_value, &Counter::valueChanged)
};
```

它适合：

- QObject 类需要一个可绑定 C++ 属性；
- `Q_PROPERTY` 要暴露 `BINDABLE` 接口；
- 既希望绑定系统更新依赖，又希望同步发出传统 NOTIFY signal；
- 属性值作为对象成员，不希望每个属性都单独分配额外 QObject。

它不是普通独立变量的首选。没有 QObject 归属时用 `QProperty<T>` 更直接；`QObjectBindableProperty` 依赖它作为成员时能通过 offset 找回所属对象。

## 2. 它和 QProperty 的区别

```text
QProperty<T>
  自己携带绑定数据，适合普通 C++ 成员

QObjectBindableProperty<Class, T, Offset, Signal>
  值存在成员对象里，绑定数据存在所属 QObject 的 QBindingStorage 里
  可通过宏自动计算 member offset
  可在变化时调用指定 NOTIFY signal
```

`QObjectBindableProperty` 的模板参数里有 `Class` 和 `Offset`。实际代码通常不手写这些参数，而是用宏声明成员：

```cpp
Q_OBJECT_BINDABLE_PROPERTY(MyObject, QString, m_title, &MyObject::titleChanged)
```

宏会生成一个 `_qt_property_m_title_offset()` 函数，让属性对象能从自己的地址反推出包含它的 `MyObject` 实例。

## 3. 与 Q_PROPERTY 的标准搭配

```cpp
class Document : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QString title READ title WRITE setTitle BINDABLE bindableTitle NOTIFY titleChanged)

public:
    QString title() const { return m_title.value(); }
    void setTitle(const QString &title) { m_title = title; }
    QBindable<QString> bindableTitle() { return &m_title; }

signals:
    void titleChanged(const QString &title);

private:
    Q_OBJECT_BINDABLE_PROPERTY(Document, QString, m_title, &Document::titleChanged)
};
```

当属性变化时，如果宏里传入了 signal 指针，`QObjectBindableProperty` 会调用它：

- signal 无参：调用 `owner()->signal()`；
- signal 接收 `T`：调用 `owner()->signal(valueBypassingBindings())`。

所以 signal 的签名要么不带参数，要么能接收当前属性值。

## 4. 构造与初始化

最常见方式是用宏：

```cpp
Q_OBJECT_BINDABLE_PROPERTY(MyObject, int, m_count)
Q_OBJECT_BINDABLE_PROPERTY_WITH_ARGS(MyObject, int, m_limit, 100)
Q_OBJECT_BINDABLE_PROPERTY_WITH_ARGS(MyObject, QString, m_name, QStringLiteral("untitled"),
                                     &MyObject::nameChanged)
```

也可以从值、移动值、typed binding 或 functor 初始化成员。由于该类要根据成员 offset 找 owner，不建议在普通局部变量里把它当裸模板类型手写使用。

`WITH_ARGS` 的 `value` 会作为构造参数传给属性成员，适合给成员一个非默认初始值。

## 5. 读取语义

```cpp
int value() const { return m_value.value(); }
```

`value()` 返回当前值，并通过所属 QObject 的绑定存储登记依赖。也就是说，当另一个绑定表达式读取这个属性时，Qt 能知道它依赖 `m_value`。

`operator*()`、隐式转换和 `operator->()` 也会读取值并登记依赖。业务代码里仍推荐显式写 `value()`，尤其是在绑定表达式和 getter 里。

## 6. 写入语义

```cpp
void setValue(int v)
{
    m_value = v;
}
```

`setValue()` 或 `operator=` 会：

1. 找到所属 QObject 的绑定数据；
2. 移除当前属性上的绑定；
3. 如果新旧值相等则直接返回；
4. 写入新值；
5. 通知绑定观察者；
6. 如果声明了 signal，则调用对应 NOTIFY signal。

这意味着手动写入同样会拆掉旧绑定。它也意味着属性类型 `T` 应提供可用的 `operator==`，因为 Qt 6.11.1 的实现会直接比较新旧值来避免重复通知。

## 7. 绑定语义

```cpp
m_total.setBinding([this] {
    return m_price.value() * m_count.value();
});
```

`setBinding(const QPropertyBinding<T> &)` 安装新的 typed 绑定，并返回被替换的旧绑定。`setBinding(const QUntypedPropertyBinding &)` 会先检查绑定的 `QMetaType` 是否匹配 `T`，不匹配时返回 `false`。

```cpp
if (!m_value.setBinding(untypedBinding)) {
    qWarning() << "wrong property type";
}
```

`binding()` 返回当前绑定；没有绑定时返回空绑定。`takeBinding()` 等价于装入一个空绑定并返回旧绑定，之后属性保留当前值，不再自动跟随依赖。

## 8. 通知与观察

```cpp
auto handler = m_value.onValueChanged([this] {
    rebuildCache();
});

auto subscriber = m_value.subscribe([this] {
    updateActionState();
});

QPropertyNotifier notifier = m_value.addNotifier([this] {
    qDebug() << "value changed";
});
```

- `onValueChanged()`：变化后调用，不立即调用；
- `subscribe()`：创建时先调用一次，随后监听变化；
- `addNotifier()`：返回类型擦除的 `QPropertyNotifier`。

这些返回对象都要保存。销毁返回对象会取消观察关系。

`notify()` 用于“底层数据可能变了，但不是通过 `setValue()` 写入”的场景。对 `QObjectBindableProperty` 来说，`notify()` 会通知绑定观察者，并触发声明的 NOTIFY signal。

## 9. 真实使用场景

### 9.1 QObject 状态字段

```cpp
class DownloadItem : public QObject
{
    Q_OBJECT
    Q_PROPERTY(int progress READ progress WRITE setProgress BINDABLE bindableProgress NOTIFY progressChanged)

public:
    int progress() const { return m_progress.value(); }
    void setProgress(int p) { m_progress = p; }
    QBindable<int> bindableProgress() { return &m_progress; }

signals:
    void progressChanged(int progress);

private:
    Q_OBJECT_BINDABLE_PROPERTY(DownloadItem, int, m_progress, &DownloadItem::progressChanged)
};
```

外部既可以连接 `progressChanged`，也可以用 `bindableProgress().setBinding(...)`。

### 9.2 从另一个属性派生

```cpp
class Meter : public QObject
{
    Q_OBJECT
public:
    Meter()
    {
        m_percent.setBinding([this] {
            return m_total.value() == 0 ? 0 : m_done.value() * 100 / m_total.value();
        });
    }

private:
    Q_OBJECT_BINDABLE_PROPERTY(Meter, int, m_done)
    Q_OBJECT_BINDABLE_PROPERTY(Meter, int, m_total)
    Q_OBJECT_BINDABLE_PROPERTY(Meter, int, m_percent)
};
```

绑定表达式里的 `value()` 读取会自动登记依赖。

## 10. 常见错误

### 10.1 手写模板参数

`Offset` 必须和成员在 `Class` 中的实际偏移一致。业务代码应使用 `Q_OBJECT_BINDABLE_PROPERTY` 宏，少手写 `QObjectBindableProperty<Class, T, Offset, Signal>`。

### 10.2 忘记保存观察器

`m_value.onValueChanged(...)` 的返回值如果不保存，观察关系会马上断开。

### 10.3 NOTIFY signal 签名不匹配

宏里传入的 signal 必须能以无参或 `T` 值调用。传错成员函数指针会在模板实例化时报一串很长的编译错误。

### 10.4 直接改底层对象却不通知

如果 `T` 是可变对象、指针指向的对象或容器内部状态被绕过属性 API 修改，绑定系统不会自动知道。修改后需要重新赋值或调用 `notify()`。

### 10.5 跨线程直接读写 QObject 属性

它属于 QObject 成员状态，不是线程安全同步原语。跨线程更新应通过 queued signal/slot、`QMetaObject::invokeMethod()` 或明确的锁策略回到对象所属线程。

## 11. 逐项 API 语义

### 宏

| API | 语义 | 边界 |
| --- | --- | --- |
| `Q_OBJECT_BINDABLE_PROPERTY(Class, Type, name)` | 在 `Class` 中声明一个无 NOTIFY signal 的 bindable 成员属性。 | 必须放在 `Class` 定义内部；`name` 是成员名。 |
| `Q_OBJECT_BINDABLE_PROPERTY(Class, Type, name, Signal)` | 声明属性，并在变化时调用 `Signal`。 | `Signal` 通常写 `&Class::xxxChanged`。 |
| `Q_OBJECT_BINDABLE_PROPERTY_WITH_ARGS(Class, Type, name, value)` | 声明属性并用 `value` 初始化。 | `value` 作为构造参数使用，注意类型和生命周期。 |
| `Q_OBJECT_BINDABLE_PROPERTY_WITH_ARGS(Class, Type, name, value, Signal)` | 声明带初值和 NOTIFY signal 的属性。 | signal 签名需无参或接收 `Type`。 |

### 构造与析构

| API | 语义 | 边界 |
| --- | --- | --- |
| `QObjectBindableProperty()` | 默认构造成 `T` 的默认值。 | 通常由宏生成成员。 |
| `explicit QObjectBindableProperty(const T &initialValue)` | 复制初始值。 | 成员 offset 仍必须来自宏。 |
| `explicit QObjectBindableProperty(T &&initialValue)` | 移动初始值。 | 移动后的实参不要继续依赖原值。 |
| `explicit QObjectBindableProperty(const QPropertyBinding<T> &binding)` | 构造后安装绑定。 | 绑定捕获对象生命周期由调用者保证。 |
| `template <typename Functor> explicit QObjectBindableProperty(Functor &&f, const QPropertyBindingSourceLocation &location = QT_PROPERTY_DEFAULT_BINDING_LOCATION)` | 用 functor 创建初始绑定。 | functor 必须返回 `T`。 |

### 读取与写入

| API | 语义 | 边界 |
| --- | --- | --- |
| `parameter_type value() const` | 读取当前值，并在所属 QObject 的绑定存储中登记依赖。 | getter 中优先使用它。 |
| `arrow_operator_result operator->() const` | 对指针或可解引用值提供成员访问。 | 仍会登记依赖。 |
| `parameter_type operator*() const` | 读取当前值。 | 可读性通常不如 `value()`。 |
| `operator parameter_type() const` | 隐式读取当前值。 | 复杂表达式里可能让依赖关系不明显。 |
| `void setValue(parameter_type t)` | 移除绑定、复制写入、通知观察者和 signal。 | 要求新旧值可比较。 |
| `void setValue(rvalue_ref t)` | 移除绑定、移动写入、通知观察者和 signal。 | 会拆掉旧绑定。 |
| `QObjectBindableProperty &operator=(parameter_type newValue)` | 复制赋值并返回自身。 | 等价于 `setValue()`。 |
| `QObjectBindableProperty &operator=(rvalue_ref newValue)` | 移动赋值并返回自身。 | 等价于 `setValue(std::move(...))`。 |
| `void notify()` | 手动通知当前值可能变化。 | 会触发观察者和宏指定的 signal。 |

### 绑定与观察

| API | 语义 | 边界 |
| --- | --- | --- |
| `QPropertyBinding<T> setBinding(const QPropertyBinding<T> &newBinding)` | 安装 typed 绑定并返回旧绑定。 | 返回值不是成功标志。 |
| `template <typename Functor> QPropertyBinding<T> setBinding(Functor &&f, const QPropertyBindingSourceLocation &location = QT_PROPERTY_DEFAULT_BINDING_LOCATION)` | 用 functor 安装绑定。 | functor 无参可调用且返回 `T`。 |
| `bool setBinding(const QUntypedPropertyBinding &newBinding)` | 安装 untyped 绑定。 | 非空绑定元类型不匹配时返回 `false`。 |
| `bool hasBinding() const` | 查询是否有当前绑定。 | 无绑定时返回 `false`。 |
| `QPropertyBinding<T> binding() const` | 返回当前绑定。 | 没有绑定时返回空绑定。 |
| `QPropertyBinding<T> takeBinding()` | 移除并返回当前绑定。 | 属性保留取出时的值。 |
| `template <typename Functor> QPropertyChangeHandler<Functor> onValueChanged(Functor f)` | 后续变化时调用回调。 | 保存返回值维持订阅。 |
| `template <typename Functor> QPropertyChangeHandler<Functor> subscribe(Functor f)` | 立即调用一次并继续监听。 | 回调无参。 |
| `template <typename Functor> QPropertyNotifier addNotifier(Functor f)` | 添加类型擦除观察器。 | 保存返回值。 |
| `const QtPrivate::QPropertyBindingData &bindingData() const` | 暴露绑定数据给 `QBindable` 和观察器。 | 普通业务代码很少直接调用。 |

### 比较

| API | 语义 | 边界 |
| --- | --- | --- |
| `operator==` / `operator!=` 与同属性类型 | 按 `value()` 比较两个属性当前值。 | 仅当 `T` 支持相等比较。 |
| `operator==` / `operator!=` 与 `T` | 比较属性当前值和普通值。 | 比较会读取属性并可能登记依赖。 |

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 声明 | `Q_OBJECT_BINDABLE_PROPERTY...` | 在 QObject 类里声明 bindable 成员。 | 用宏计算 offset，别手写偏移。 |
| 元属性 | `Q_PROPERTY(... BINDABLE bindableX NOTIFY xChanged)` | 把成员属性暴露给 Qt 元对象系统。 | getter、setter、bindable 访问器要读写同一个成员。 |
| 读取 | `value()`、`operator*()`、`operator->()`、隐式转换 | 获取值并登记依赖。 | getter 中推荐 `value()`。 |
| 写入 | `setValue()`、`operator=` | 手动写值并通知。 | 会移除当前绑定。 |
| 绑定 | `setBinding()`、`binding()`、`hasBinding()`、`takeBinding()` | 管理绑定表达式。 | untyped 绑定要检查元类型。 |
| 通知 | `notify()`、NOTIFY signal | 手动或自动通知变化。 | 直接改内部状态后必须显式通知。 |
| 观察 | `onValueChanged()`、`subscribe()`、`addNotifier()` | 监听属性变化。 | 返回 RAII 句柄，必须保存。 |

---

### 一句话总结

`QObjectBindableProperty` 是 `QProperty` 在 QObject 成员里的版本：它用宏拿到 owner，变化时既通知绑定系统，也能同步触发传统 NOTIFY signal。
