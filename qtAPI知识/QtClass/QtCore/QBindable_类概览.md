# Qt QBindable 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QBindable>`  
> 所属模块：`Qt6::Core`  
> 模板声明：`template <typename T> class QBindable`  
> 继承关系：`QUntypedBindable -> QBindable<T>`

## 1. 先建立整体认识：它是“可绑定属性的句柄”

`QBindable<T>` 不是属性值本身，也不是一个新的容器。它是一个指向“支持绑定的属性”的轻量句柄，让外部代码可以用统一、强类型的方式做这些事：

- 读取底层属性当前值。
- 写入一个新值。
- 查询当前是否有绑定。
- 设置、取出或替换绑定表达式。
- 把一个传统 `Q_PROPERTY` 包装成可以进入 C++ property binding 的对象。

它解决的核心问题是：Qt 里可绑定属性可能由不同类型实现，例如 `QProperty<T>`、`QObjectBindableProperty`、`QObjectComputedProperty`，或者带 `NOTIFY` 的传统 `Q_PROPERTY`。使用者不应该为了设置绑定而关心属性底层到底是哪一种实现。

可以这样理解它的位置：

```text
属性存储层：
  QProperty<T>
  QObjectBindableProperty<...>
  QObjectComputedProperty<...>
  传统 Q_PROPERTY + NOTIFY

统一访问层：
  QUntypedBindable      // 类型擦除，运行时看 QMetaType
  QBindable<T>          // 强类型，编译期知道 T
```

`QBindable<T>` 通常由对象提供的 `bindableX()` 函数返回。调用者拿到它后，就可以给属性设置绑定，而不需要知道对象内部是 `QProperty` 还是 `QObjectBindableProperty`。

## 2. 它解决什么场景

### 2.1 让 C++ 属性也能像 QML 那样自动联动

传统写法里，一个属性变化后要手动更新另一个属性：

```cpp
void User::setFirstName(const QString &name)
{
    if (m_firstName == name)
        return;

    m_firstName = name;
    m_fullName = m_firstName + " " + m_lastName;
    emit firstNameChanged();
    emit fullNameChanged();
}
```

绑定属性希望把这种依赖关系直接表达出来：

```cpp
fullName.setBinding([&] {
    return firstName.value() + " " + lastName.value();
});
```

当 `firstName` 或 `lastName` 改变时，`fullName` 会重新计算。`QBindable<T>` 的作用，就是把这种能力暴露给 `Q_PROPERTY` 的使用者。

### 2.2 给公开 `Q_PROPERTY` 加一个绑定入口

典型写法如下：

```cpp
#include <QObject>
#include <QProperty>

class Person final : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QString name READ name WRITE setName NOTIFY nameChanged BINDABLE bindableName)

public:
    QString name() const { return m_name; }
    void setName(const QString &name) { m_name = name; }
    QBindable<QString> bindableName() { return QBindable<QString>(&m_name); }

signals:
    void nameChanged();

private:
    Q_OBJECT_BINDABLE_PROPERTY(Person, QString, m_name, &Person::nameChanged)
};
```

重点有三处：

1. `Q_PROPERTY` 里写 `BINDABLE bindableName`。
2. 类里提供 `QBindable<QString> bindableName()`。
3. 属性数据由 `Q_OBJECT_BINDABLE_PROPERTY` 或其他可绑定属性类型承载。

之后外部代码就可以这样设置依赖：

```cpp
QProperty<QString> fallbackName("guest");

person->bindableName().setBinding([&] {
    return fallbackName.value().toUpper();
});
```

## 3. QBindable 不拥有属性

`QBindable<T>` 更像一个 view 或 handle：它指向某个底层属性，但不负责拥有它。属性对象必须比 `QBindable` 的使用时间更长。

这点在 binding lambda 里尤其重要：

```cpp
QBindable<QDateTime> dateTimeBindable(dateTimeEdit, "dateTime");

displayText.setBinding([dateTimeBindable] {
    return dateTimeBindable.value().toString();
});
```

这里把 `dateTimeBindable` 按值捕获，是为了避免每次绑定重新求值时都通过对象和属性名重新构造一次句柄。但这不意味着它延长了 `dateTimeEdit` 的生命周期；如果底层对象销毁，继续让绑定访问它就会出问题。实际工程中应让绑定的生命周期受拥有对象控制，或者在对象销毁前拆掉绑定。

## 4. 两种构造来源

### 4.1 从真正的可绑定属性对象构造

在实现 `BINDABLE` 属性时，通常从成员属性指针构造：

```cpp
QBindable<int> bindableX()
{
    return QBindable<int>(&m_x);
}
```

`m_x` 可以是 `QProperty<int>`，也可以是 `Q_OBJECT_BINDABLE_PROPERTY` 宏声明出的 `QObjectBindableProperty`。这是实现新属性时最推荐的入口，因为它保留了完整依赖跟踪能力。

如果从 `const` 属性指针构造，得到的 bindable 是只读的。只读句柄可以读取、观察、做依赖来源，但不能成功设置值或替换绑定。

### 4.2 从 `QObject` 和属性名构造

Qt 6.5 起，`QBindable<T>` 可以直接包装某个 `QObject` 上的 `Q_PROPERTY`：

```cpp
QBindable<QDateTime> dateTimeBindable(dateTimeEdit, "dateTime");
```

这个能力适合“使用已有 Qt 类的属性”，例如把 `QDateTimeEdit::dateTime` 纳入绑定表达式。该属性必须有 `NOTIFY` 信号；即使它的 `Q_PROPERTY` 没写 `BINDABLE`，也可以通过这种方式用于绑定。

但有一个非常重要的区别：如果这个传统属性本身没有 `BINDABLE`，在绑定表达式里必须通过 `QBindable::value()` 读取，依赖跟踪才知道你读了它。

```cpp
displayText.setBinding([dateTimeBindable] {
    return dateTimeBindable.value().toString();
});
```

不要在 binding lambda 里改用普通 getter：

```cpp
// 对非 BINDABLE 的传统属性，这样读不到依赖关系。
displayText.setBinding([dateTimeEdit] {
    return dateTimeEdit->dateTime().toString();
});
```

这个 `QObject` 构造函数不适合拿来实现你自己的 `BINDABLE` 访问器。自己写类时，应使用 `QProperty`、`QObjectBindableProperty` 或 `Q_OBJECT_BINDABLE_PROPERTY`。

## 5. 绑定表达式的规则

绑定表达式是一个 C++ 可调用对象，通常是 lambda。它会在依赖变化时被重新求值，因此要按“可能执行很多次”的函数来写：

- 读取依赖属性时，要读可绑定属性的 `value()`。
- lambda 捕获的对象必须比绑定活得更久。
- 不要在绑定表达式里写入目标属性。
- 不要在绑定表达式里读取目标属性本身，否则可能形成绑定循环。
- 不要在绑定表达式里做有副作用的业务操作，例如网络写入、文件写入、弹窗、发复杂信号。
- 绑定系统不是线程安全的，属性只能在创建它的线程中读写；参与绑定的 `QObject` 也不应在绑定存在期间移动线程。
- 绑定函数以及它调用的代码不应使用 `co_await`。

绑定表达式应尽量像“纯计算”：读取几个属性，返回一个值。

## 6. 写值会移除绑定

`setValue()` 的语义和 `QProperty::setValue()` 一致：直接写入新值，并移除当前属性上已有的绑定。

这不是小细节，而是使用 `QBindable` 时最常见的状态变化：

```cpp
auto bindable = person->bindableName();

bindable.setBinding([&] {
    return fallbackName.value();
});

bindable.setValue("manual"); // 绑定被移除，之后不再跟随 fallbackName
```

如果你只是想让依赖重新计算，不应该通过 `setValue()` 写一个中间值；应该改变依赖源，或者重新设置绑定。

绑定属性也不适合当普通算法变量反复写中间值。每次写属性都可能通知依赖者和观察者。复杂计算先用局部变量完成，最后只把最终值写回属性。

## 7. 有效性、只读性和观察回调

`QBindable<T>` 继承自 `QUntypedBindable`，所以实际使用前常常会检查这些状态：

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 状态查询 | `isValid()` | 判断句柄是否真的指向一个可访问属性。 | 无效句柄上多数操作没有效果；`value()` 会返回默认构造的 `T`。 |
| 状态查询 | `isReadOnly()` | 判断底层属性是否只读。 | 只读句柄不能成功 `setValue()` 或 `setBinding()`。 |
| 状态查询 | `hasBinding()` | 判断底层属性当前是否有绑定表达式。 | 只能说明是否存在绑定，不说明绑定求值是否符合业务预期。 |
| 类型查询 | `metaType()` | 返回底层属性的 `QMetaType`。 | 来自基类，适合调试或运行时框架代码；无效句柄返回无效元类型。 |
| 观察变化 | `onValueChanged(Functor)` | 属性变化时调用回调。 | 必须保存返回的 handler 对象，否则订阅会立刻失效。 |
| 观察变化 | `subscribe(Functor)` | 先立刻调用一次回调，再在后续变化时继续调用。 | 适合同步 UI 初始状态；同样要保存返回对象。 |
| 观察变化 | `addNotifier(Functor)` | 安装非模板化的变化通知对象。 | 返回 `QPropertyNotifier`，更方便作为成员变量保存。 |

观察 API 的返回对象控制订阅生命周期。下面这种写法看起来注册了回调，其实返回对象马上销毁，订阅随即解除：

```cpp
person->bindableName().onValueChanged([&] {
    refresh();
});
```

应该把返回对象保存起来：

```cpp
m_nameChangeHandler = person->bindableName().onValueChanged([&] {
    refresh();
});
```

## 8. 每个 API 的作用与用法

### 8.1 `QBindable(Property *property)`

```cpp
template <typename Property>
QBindable(Property *property)
```

这是从 `QUntypedBindable` 继承来的构造入口，也是实现 `BINDABLE` 访问器最常见的写法。它把 `QProperty<T>`、`QObjectBindableProperty` 等可绑定属性包装成 `QBindable<T>`。

如果 `Property` 是 `const`，得到的是只读句柄；如果指针无效，就不应继续把这个句柄当成可操作属性使用。

### 8.2 `QBindable(QObject *obj, const QMetaProperty &property)`

```cpp
explicit QBindable(QObject *obj, const QMetaProperty &property)
```

Qt 6.5 引入。用运行时拿到的 `QMetaProperty` 在某个 `QObject` 实例上构造强类型 bindable。

它适合元对象驱动的框架代码：先枚举或查找属性，再按期望类型包装。调用前要确认 `property` 属于 `obj` 的元对象，并且类型与 `T` 匹配。

### 8.3 `QBindable(QObject *obj, const char *property)`

```cpp
explicit QBindable(QObject *obj, const char *property)
```

Qt 6.5 引入。通过属性名包装 `obj` 上的 `Q_PROPERTY`。

该属性必须有 `NOTIFY` 信号，才能在传统属性不带 `BINDABLE` 的情况下参与依赖更新。绑定表达式里要捕获 `QBindable` 并调用它的 `value()`，不要绕回普通 getter。

### 8.4 `value()`

```cpp
T value() const
```

读取底层属性当前值。对真正的可绑定属性，这个读取也参与依赖跟踪；对通过 `QObject` 和属性名包装的传统属性，在 binding lambda 里调用它尤其关键。

如果句柄无效，返回默认构造的 `T`。不要把默认值误判成真实业务值；需要区分时先检查 `isValid()`。

### 8.5 `setValue(const T &value)`

```cpp
void setValue(const T &value)
```

把底层属性改成指定值，并移除当前绑定。只读或无效句柄上调用没有效果。

它适合用户手动覆盖自动绑定结果，例如“用户手动输入后解除自动跟随”。如果只是想改变绑定结果，应改依赖源而不是直接写目标属性。

### 8.6 `binding()`

```cpp
QPropertyBinding<T> binding() const
```

返回底层属性当前的强类型绑定对象。如果没有绑定，返回无效的 `QPropertyBinding<T>`。

它适合临时查看、保存或迁移当前绑定。只想知道有没有绑定时，`hasBinding()` 更直接。

### 8.7 `setBinding(const QPropertyBinding<T> &binding)`

```cpp
QPropertyBinding<T> setBinding(const QPropertyBinding<T> &binding)
```

给底层属性设置一个强类型绑定，并返回之前的绑定。只读或无效句柄上调用不会改变属性，并返回无效绑定。

返回旧绑定这一点很有用：你可以临时替换绑定，稍后再恢复。

### 8.8 `setBinding(Functor f)`

```cpp
template <typename Functor>
QPropertyBinding<T> setBinding(Functor f)
```

从 lambda 或其他可调用对象创建 `QPropertyBinding<T>`，并设置到底层属性上。返回之前的绑定。

```cpp
bindableWidth.setBinding([&] {
    return contentWidth.value() + padding.value() * 2;
});
```

`f` 的返回值必须能作为 `T` 使用。lambda 捕获对象的生命周期必须覆盖绑定生命周期。

### 8.9 `makeBinding()`

```cpp
QPropertyBinding<T> makeBinding(
    const QPropertyBindingSourceLocation &location = QT_PROPERTY_DEFAULT_BINDING_LOCATION) const
```

构造一个“读取当前底层属性值”的绑定对象。它常用于让另一个 `QProperty<T>` 直接跟随这个属性。

```cpp
QProperty<int> mirror;
mirror.setBinding(sourceBindable.makeBinding());
```

`location` 用于记录绑定来源位置，方便调试和诊断。通常保留默认参数即可。

### 8.10 `takeBinding()`

```cpp
QPropertyBinding<T> takeBinding()
```

移除底层属性当前绑定，并把旧绑定返回给调用者。没有绑定时返回无效 `QPropertyBinding<T>`。

调用后，属性不再自动跟随原依赖；之后只有直接写值或设置新绑定才会改变它。

## 9. 继承自 QUntypedBindable 的接口如何看

`QBindable<T>` 继承了 `QUntypedBindable` 的若干接口。日常使用中，最常用的是 `isValid()`、`isReadOnly()`、`hasBinding()`、`onValueChanged()`、`subscribe()` 和 `addNotifier()`。

还有一些无类型版本的绑定 API，例如：

```cpp
QUntypedPropertyBinding QUntypedBindable::binding() const;
bool QUntypedBindable::setBinding(const QUntypedPropertyBinding &binding);
QUntypedPropertyBinding QUntypedBindable::takeBinding();
```

这些适合运行时框架代码。当你已经知道属性类型时，优先使用 `QBindable<T>` 的强类型版本，编译器能帮你检查绑定返回值类型。

## 10. 常见误区与排查顺序

### 10.1 `setBinding()` 调了但没有效果

先检查：

1. `bindable.isValid()` 是否为 `true`。
2. `bindable.isReadOnly()` 是否为 `false`。
3. `QPropertyBinding<T>` 的返回类型是否和 `T` 匹配。
4. 包装传统 `Q_PROPERTY` 时，该属性是否有 `NOTIFY` 信号。
5. binding lambda 是否真的读取了可跟踪的属性。

### 10.2 传统 getter 被放进绑定表达式

如果属性不是 `BINDABLE`，普通 getter 不会自动建立依赖跟踪。用 `QBindable(obj, "property")` 包装后，在 lambda 中读 `bindable.value()`。

### 10.3 写 setter 时夹杂业务副作用

可绑定属性的 setter 应尽量只写底层属性。属性也可能因为绑定重新求值而改变，此时普通 setter 里的业务代码未必会执行。依赖属性变化的逻辑应放在绑定、观察回调或更明确的业务层。

### 10.4 绑定表达式捕获了短生命周期对象

绑定可能在以后任意一次依赖变化时重新求值。lambda 捕获局部引用、临时对象指针、即将销毁的控件，都会让后续求值变得危险。

### 10.5 回调对象没有保存

`onValueChanged()`、`subscribe()`、`addNotifier()` 的返回对象控制订阅生命周期。返回值一销毁，通知就取消。

### 10.6 跨线程读写绑定属性

Qt 的绑定属性系统不是通用线程同步机制。参与绑定的属性不能从其他线程读写；带绑定的 `QObject` 也不应在绑定存在期间移动到别的线程。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `template <typename Property> QBindable(Property *property)` | 从 `QProperty`、`QObjectBindableProperty` 等可绑定属性对象创建强类型句柄。 | 这是实现 `BINDABLE` 访问器的常用入口；句柄不拥有底层属性。 |
| 构造 | `explicit QBindable(QObject *obj, const QMetaProperty &property)` | 通过元属性对象包装 `QObject` 上的属性。 | Qt 6.5 引入；类型要和 `T` 匹配，适合运行时框架代码。 |
| 构造 | `explicit QBindable(QObject *obj, const char *property)` | 通过属性名包装 `QObject` 上的 `Q_PROPERTY`。 | Qt 6.5 引入；传统属性需要 `NOTIFY`，绑定表达式中要用 `value()` 读取。 |
| 读取 | `T value() const` | 返回底层属性当前值。 | 无效句柄返回默认构造的 `T`；在绑定表达式中读取会建立依赖。 |
| 写入 | `void setValue(const T &value)` | 直接写入新值。 | 会移除当前绑定；只读或无效句柄上没有效果。 |
| 查询绑定 | `QPropertyBinding<T> binding() const` | 返回当前强类型绑定对象。 | 没有绑定时返回无效绑定；只查状态时用 `hasBinding()` 更清楚。 |
| 设置绑定 | `QPropertyBinding<T> setBinding(const QPropertyBinding<T> &binding)` | 设置强类型绑定，并返回旧绑定。 | 只读或无效句柄不会改变属性；可保存返回值用于恢复。 |
| 设置绑定 | `template <typename Functor> QPropertyBinding<T> setBinding(Functor f)` | 用 lambda 等可调用对象创建绑定并设置到属性。 | 返回值类型要适配 `T`；捕获对象必须比绑定活得久。 |
| 创建绑定 | `QPropertyBinding<T> makeBinding(const QPropertyBindingSourceLocation &location = QT_PROPERTY_DEFAULT_BINDING_LOCATION) const` | 创建一个读取当前属性值的绑定对象。 | 常用于让另一个属性跟随当前属性；默认 location 通常够用。 |
| 取出绑定 | `QPropertyBinding<T> takeBinding()` | 移除当前绑定并返回旧绑定。 | 之后属性不再自动更新；没有绑定时返回无效绑定。 |
| 继承状态 | `bool isValid() const` | 判断句柄是否指向有效属性。 | 调用写入或设置绑定前先检查，特别是运行时属性名包装场景。 |
| 继承状态 | `bool isReadOnly() const` | 判断底层属性是否只读。 | 只读句柄可以读和观察，但不能成功写值或设绑定。 |
| 继承状态 | `bool hasBinding() const` | 判断底层属性是否已有绑定。 | 只表示有无绑定，不会返回绑定内容。 |
| 继承类型 | `QMetaType metaType() const` | 返回底层属性元类型。 | Qt 6.2 引入；无效句柄返回无效 `QMetaType`。 |
| 继承观察 | `QPropertyChangeHandler<Functor> onValueChanged(Functor f) const` | 属性值变化时调用回调。 | 必须保存返回对象；回调不保证适合做重活。 |
| 继承观察 | `QPropertyChangeHandler<Functor> subscribe(Functor f) const` | 立即调用一次回调，并订阅后续变化。 | 适合同步初始状态；同样由返回对象控制生命周期。 |
| 继承观察 | `QPropertyNotifier addNotifier(Functor f)` | 安装属性变化通知回调并返回非模板通知对象。 | 更适合作为成员保存；属性和 notifier 都要保持存活。 |
| 继承无类型绑定 | `bool setBinding(const QUntypedPropertyBinding &binding)` | 用类型擦除绑定设置底层属性。 | 运行时框架代码使用；类型不匹配、无效或只读会失败。 |

---

### 一句话总结

`QBindable<T>` 是可绑定属性的强类型句柄：它不拥有属性，只负责统一读取、写入、设置绑定和观察变化；新属性用 `QProperty` 或 `QObjectBindableProperty` 提供真实存储，传统 `Q_PROPERTY` 也能通过 `QObject` 构造函数接入绑定系统。
