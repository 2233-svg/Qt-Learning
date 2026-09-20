# Qt QObjectComputedProperty：QObject 上的只读计算属性

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QObjectComputedProperty>` 或 `#include <QProperty>`  
> 所属模块：`Qt6::Core`  
> 继承：`QUntypedPropertyData -> QObjectComputedProperty<Class, T, Offset, Getter>`  
> 类型性质：嵌入 QObject 的只读计算属性

## 1. 它解决什么问题

`QObjectComputedProperty` 用来把“由对象内部状态计算出来的值”暴露成可绑定属性。它本身不保存 `T`，每次读取都调用指定 getter 重新计算；当底层状态变化时，调用者用 `notify()` 告诉绑定系统这个计算结果可能变了。

```cpp
class Cart : public QObject
{
    Q_OBJECT
    Q_PROPERTY(bool empty READ isEmpty BINDABLE bindableEmpty STORED false)

public:
    bool isEmpty() const { return m_items.isEmpty(); }
    QBindable<bool> bindableEmpty() { return &m_empty; }

    void addItem(const QString &item)
    {
        m_items.append(item);
        m_empty.notify();
    }

private:
    QList<QString> m_items;
    Q_OBJECT_COMPUTED_PROPERTY(Cart, bool, m_empty, &Cart::isEmpty)
};
```

它适合：

- QObject 中已有真实数据字段，只想暴露派生状态；
- 这个派生值不应该被外部写入；
- `Q_PROPERTY` 需要一个 `BINDABLE` 入口，但属性值应该由 getter 计算；
- 希望在底层状态变化时用 `notify()` 精确通知依赖它的绑定。

如果属性需要存值、可写、可安装绑定，用 `QObjectBindableProperty`。如果不在 QObject 里，用 `QProperty`。

## 2. 核心模型

```text
底层状态                 QObjectComputedProperty
QList/缓存/多个字段  -->  value() 调用 Getter 计算 T
        │                 本身不保存 T，不接收 setBinding()
        └─ 变化后调用 notify() 通知观察者
```

`QObjectComputedProperty` 和普通 getter 的差别在于：它有绑定系统可观察的身份。其他属性或 QML 绑定读取它时，可以依赖它；你调用 `notify()` 后，依赖它的绑定会得到重新求值机会。

## 3. 声明方式

通常使用宏，而不是手写模板参数：

```cpp
Q_OBJECT_COMPUTED_PROPERTY(Class, Type, memberName, &Class::getter)
```

宏会在类中声明一个成员，并生成 offset 函数。属性对象借助 offset 从自己的地址反推 owner，然后执行：

```cpp
(owner()->*Getter)()
```

getter 必须是所属类的成员函数指针，并且返回值能作为 `Type` 返回。

## 4. 与 Q_PROPERTY 搭配

```cpp
class Session : public QObject
{
    Q_OBJECT
    Q_PROPERTY(bool active READ isActive BINDABLE bindableActive STORED false)

public:
    bool isActive() const
    {
        return m_socketConnected && !m_userName.isEmpty();
    }

    QBindable<bool> bindableActive()
    {
        return &m_active;
    }

    void setSocketConnected(bool on)
    {
        if (m_socketConnected == on)
            return;
        m_socketConnected = on;
        m_active.notify();
    }

private:
    bool m_socketConnected = false;
    QString m_userName;
    Q_OBJECT_COMPUTED_PROPERTY(Session, bool, m_active, &Session::isActive)
};
```

通常给计算属性标 `STORED false`，因为它不是独立存储的字段，而是由其他状态推导出来的结果。

## 5. 读取语义

```cpp
auto active = m_active.value();
```

`value()` 会先把这个计算属性登记为当前绑定的依赖，然后调用 getter 计算并返回结果。Qt 6.11.1 中 `parameter_type` 就是 `T`，所以返回值按值传递。

`operator*()` 和隐式转换也会读取值；`operator->()` 仅在 `T` 是可解引用类型时提供。

## 6. 通知语义

```cpp
m_active.notify();
```

`QObjectComputedProperty` 不知道你的底层数据什么时候变化。修改列表、缓存、普通成员变量、外部资源状态以后，如果计算结果可能变化，就要调用 `notify()`。

```cpp
void Cart::clear()
{
    if (m_items.isEmpty())
        return;
    m_items.clear();
    m_empty.notify();
}
```

`notify()` 不会重新计算并比较新旧结果；它只是通知观察者“这个计算属性可能变了”。如果计算很重或通知频繁，调用方应在业务层先做必要的变化判断。

## 7. 绑定边界

计算属性是只读的：

- `hasBinding()` 永远返回 `false`；
- 没有 `setValue()`；
- 没有 `setBinding()`；
- 通过 `QBindable<T>` 暴露时属于只读 bindable，不能安装新绑定；
- 可以被其他绑定读取，也可以创建“跟随它的绑定”。

这能防止外部把计算属性改成手写值，从而破坏它与底层状态之间的关系。

## 8. 观察变化

```cpp
auto handler = m_empty.onValueChanged([this] {
    updateActions();
});

auto subscriber = m_empty.subscribe([this] {
    updateActions();
});

QPropertyNotifier notifier = m_empty.addNotifier([this] {
    qDebug() << "empty changed";
});
```

- `onValueChanged()`：以后 `notify()` 触发时调用；
- `subscribe()`：立即调用一次，再监听后续通知；
- `addNotifier()`：返回类型擦除观察器。

这些函数监听的是 `notify()` 事件，不是 getter 返回值自动比较后的“确实变化”。返回对象必须保存。

## 9. 真实使用场景

### 9.1 派生布尔状态

```cpp
bool Editor::hasSelection() const
{
    return m_cursor.selectionStart() != m_cursor.selectionEnd();
}

Q_OBJECT_COMPUTED_PROPERTY(Editor, bool, m_hasSelection, &Editor::hasSelection)
```

光标变化时调用 `m_hasSelection.notify()`，界面按钮绑定到 `hasSelection` 即可自动更新。

### 9.2 聚合多个字段

```cpp
QString User::displayName() const
{
    return m_nickName.isEmpty() ? m_accountName : m_nickName;
}

Q_OBJECT_COMPUTED_PROPERTY(User, QString, m_displayName, &User::displayName)
```

修改 `m_nickName` 或 `m_accountName` 后都要通知 `m_displayName`。

## 10. 常见错误

### 10.1 修改底层数据后忘记 `notify()`

计算属性不会监视普通成员变量或容器内部变化。忘记通知会让依赖绑定保留旧状态。

### 10.2 以为 `notify()` 会比较新旧值

`notify()` 不保证结果真的改变。频繁通知昂贵计算属性会带来不必要的重新求值。

### 10.3 把计算属性当可写属性暴露

如果 `Q_PROPERTY` 同时提供 WRITE，就会造成 API 语义矛盾。计算属性一般只提供 READ 和 BINDABLE。

### 10.4 getter 有副作用

绑定系统可能多次调用 getter。getter 应尽量是纯读取和计算，不要在里面修改状态、发信号或触发 I/O。

### 10.5 getter 捕获了错误的 owner 假设

该类通过成员 offset 找 owner。属性必须真的是 `Class` 的成员，并由宏声明；放进不匹配的布局或手写错误 offset 都会破坏这一前提。

## 11. 逐项 API 语义

### 宏与构造

| API | 语义 | 边界 |
| --- | --- | --- |
| `Q_OBJECT_COMPUTED_PROPERTY(Class, Type, name, Getter)` | 在 `Class` 中声明一个只读计算属性成员。 | `Getter` 是 `Class` 成员函数指针，返回值匹配 `Type`。 |
| `QObjectComputedProperty()` | 默认构造属性成员。 | 通常由宏生成；不要独立局部使用。 |

### 读取

| API | 语义 | 边界 |
| --- | --- | --- |
| `parameter_type value() const` | 登记依赖并调用 getter 返回计算值。 | Qt 6.11.1 中按 `T` 值返回；getter 应无副作用。 |
| `operator parameter_type() const` | 隐式读取计算值。 | 复杂代码中优先显式写 `value()`。 |
| `parameter_type operator*() const` | 读取计算值。 | 同样会登记依赖。 |
| `operator->() const` | 当 `T` 可解引用时提供成员访问。 | 返回的是计算得到的值，注意临时对象生命周期。 |

### 绑定与通知

| API | 语义 | 边界 |
| --- | --- | --- |
| `constexpr bool hasBinding() const` | 固定返回 `false`。 | 计算属性自身不能安装绑定。 |
| `void notify()` | 通知观察者和依赖绑定：计算值可能变化。 | 不比较新旧值；调用方控制频率。 |
| `QtPrivate::QPropertyBindingData &bindingData() const` | 为 `QBindable` 和观察器提供绑定数据。 | 属于底层协作接口。 |
| `template <typename Functor> QPropertyChangeHandler<Functor> onValueChanged(Functor f)` | 后续 `notify()` 后调用回调。 | 保存返回值。 |
| `template <typename Functor> QPropertyChangeHandler<Functor> subscribe(Functor f)` | 立即调用一次，并监听后续通知。 | 回调无参。 |
| `template <typename Functor> QPropertyNotifier addNotifier(Functor f)` | 添加类型擦除通知器。 | 保存返回值。 |

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 声明 | `Q_OBJECT_COMPUTED_PROPERTY` | 声明 QObject 成员计算属性。 | 用宏保证 owner offset 正确。 |
| 读取 | `value()`、隐式转换、`operator*()`、`operator->()` | 调用 getter 计算当前值。 | getter 不要有副作用。 |
| 可写性 | `hasBinding()` | 表明它没有自身绑定。 | 没有 `setValue()` / `setBinding()`。 |
| 通知 | `notify()` | 底层状态变化后通知依赖者。 | 不自动比较新旧结果。 |
| 观察 | `onValueChanged()`、`subscribe()`、`addNotifier()` | 监听 `notify()` 触发的变化。 | 返回 RAII 句柄，必须保存。 |
| 元属性 | `QBindable<T>(&property)` | 暴露只读 bindable 接口。 | 外部可依赖它，不能给它安装绑定。 |

---

### 一句话总结

`QObjectComputedProperty` 让 QObject 的派生 getter 成为可绑定、可观察的只读属性；它不存值，底层状态变化后必须由你调用 `notify()`。
