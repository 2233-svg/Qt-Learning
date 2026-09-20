# Qt QProperty：带绑定依赖追踪的值属性

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QProperty>`  
> 所属模块：`Qt6::Core`  
> 继承：`QPropertyData<T> -> QProperty<T>`  
> 类型性质：不可复制、不可移动的模板值属性

## 1. 它解决什么问题

`QProperty<T>` 把一个普通 C++ 值包装成 Qt 可绑定属性。它既能像变量一样保存 `T`，又能参与 Qt 6 的属性绑定系统：读取属性时记录依赖，写入属性时通知依赖它的绑定重新计算。

```cpp
QProperty<int> width(120);
QProperty<int> height(40);
QProperty<int> area([&] { return width.value() * height.value(); });

Q_ASSERT(area.value() == 4800);
width = 200;
Q_ASSERT(area.value() == 8000);
```

它适合：

- 在纯 C++ 对象里表达“一个值由另一些值自动推导”；
- 让配置项、状态字段、模型字段之间建立响应式关系；
- 给 `QBindable<T>`、`QPropertyBinding<T>`、`onValueChanged()` 这组 API 提供实际存储；
- 在不写 QObject signal 的场景中得到轻量的属性通知。

它不是 QObject 属性声明本身。把属性暴露给元对象系统、QML 或 Designer 时，仍需要 `Q_PROPERTY(... BINDABLE ...)`、`QBindable<T>` 访问器，或者使用 `QObjectBindableProperty`。

## 2. 使用模型

```text
QProperty<T>
  保存当前值
  读取 value() 时登记为当前绑定的依赖
  setValue()/operator= 写入时移除旧绑定并通知观察者
  setBinding() 安装表达式，表达式会在依赖变化时重新求值
```

最常见的三种用法：

```cpp
QProperty<QString> name(QStringLiteral("untitled"));
name = QStringLiteral("report.txt"); // 直接赋值，属性变成手写值

QProperty<int> count(10);
QProperty<int> doubled([&] { return count.value() * 2; });

auto guard = count.onValueChanged([&] {
    qDebug() << "count changed:" << count.value();
});
```

`QProperty` 的通知处理器是 RAII 对象。`onValueChanged()`、`subscribe()`、`addNotifier()` 返回的对象必须保存下来；临时返回值立刻析构，观察关系也会立刻失效。

## 3. 构造与生命周期

```cpp
QProperty<int> a;                  // T 默认构造
QProperty<int> b(42);              // 初始值
QProperty<QString> c(QString{});   // 移动初始值
QProperty<int> d([&] { return a.value() + b.value(); });
```

`QProperty<T>` 在 Qt 6.11.1 中禁止复制和移动。原因很实在：绑定系统内部保存的是属性对象地址，随意复制或移动会让依赖图中的观察节点变得危险。

析构时会断开内部绑定和观察关系；不要让绑定 lambda 捕获已经销毁的对象，也不要让外部保存指向 `QProperty` 内部值的悬空引用。

## 4. 读取语义

### 4.1 `value()`

```cpp
auto current = property.value();
```

`value()` 返回当前值，并在有绑定正在求值时把当前属性登记为依赖。也就是说，在绑定表达式中读 `property.value()`，等同于告诉 Qt：“这个绑定依赖这个属性”。

`QPropertyData<T>` 还提供 `valueBypassingBindings()`，它只读底层值，不登记依赖。日常业务代码通常应使用 `value()`；绕过绑定主要用于底层适配或非常明确的内部场景。

### 4.2 隐式读取操作

`QProperty` 还提供：

- `operator T-like()`：按 `parameter_type` 隐式转出当前值；
- `operator*()`：等价于读取值；
- `operator->()`：当 `T` 是指针或可解引用对象时方便访问成员。

这些操作同样会读取属性值，也会参与依赖登记。为了代码可读性，绑定表达式里优先写 `value()`，因为它把“这里会建立依赖”说得最清楚。

## 5. 写入语义

```cpp
property.setValue(newValue);
property = newValue;
```

直接写入会做三件事：

1. 移除当前属性上的绑定；
2. 如果 `T` 支持 `operator==` 且新旧值相等，不发送变化通知；
3. 更新底层值并通知观察者和依赖绑定。

这一点很容易踩坑：给有绑定的属性手动赋值，不是“临时覆盖绑定结果”，而是把绑定拆掉，让属性回到手写值模式。

```cpp
QProperty<int> source(1);
QProperty<int> target([&] { return source.value() + 1; });

target = 99;       // target 的绑定被移除
source = 10;
Q_ASSERT(target.value() == 99);
```

如果 `T` 没有可用的相等比较，Qt 无法跳过“相同值写入”的通知；设计属性值类型时，给状态类型提供合理的 `operator==` 通常更省心。

## 6. 绑定语义

### 6.1 构造或安装绑定

```cpp
QProperty<int> sum([&] {
    return left.value() + right.value();
});

sum.setBinding([&] {
    return left.value() - right.value();
});
```

绑定函数必须能无参调用，并产生可转换为 `T` 的结果。绑定求值期间读到的其他 `QProperty` 会成为依赖；依赖变化后，当前绑定会被重新求值。

绑定 lambda 的捕获生命周期由调用者负责。不要捕获局部变量引用后让绑定活得更久，也不要捕获可能先于属性销毁的 QObject 裸指针；必要时使用 `QPointer` 或明确的断开策略。

### 6.2 `setBinding()` 的返回值

```cpp
QPropertyBinding<int> old = property.setBinding(newBinding);
```

typed `setBinding()` 返回被替换掉的旧绑定；之前没有绑定时返回空绑定。这个返回值适合临时保存、迁移或诊断，而不是表示“新绑定是否成功”。

`setBinding(const QUntypedPropertyBinding &)` 返回 `bool`：当非空绑定的元类型不是 `T` 时返回 `false`，属性不会接收这个绑定。

### 6.3 `binding()`、`hasBinding()`、`takeBinding()`

```cpp
if (property.hasBinding()) {
    QPropertyBinding<int> current = property.binding();
}

QPropertyBinding<int> detached = property.takeBinding();
```

- `binding()` 返回当前绑定的句柄，不移除它；
- `hasBinding()` 判断当前是否装有绑定；
- `takeBinding()` 移除当前绑定并返回旧绑定，属性保留取出前的当前值。

取出绑定后，依赖变化不会再自动更新该属性。

## 7. 观察变化

```cpp
auto h1 = property.onValueChanged([&] {
    repaint();
});

auto h2 = property.subscribe([&] {
    updateLabel(property.value());
});

QPropertyNotifier h3 = property.addNotifier([&] {
    qDebug() << "changed";
});
```

- `onValueChanged()`：以后发生变化时调用；创建时不立即调用；
- `subscribe()`：先立即调用一次回调，再像 `onValueChanged()` 一样监听后续变化；
- `addNotifier()`：返回类型擦除的 `QPropertyNotifier`，适合不想暴露 functor 类型的存储位置。

回调必须是无参可调用对象。回调中可以读取属性，但要避免形成无意的绑定环或在通知链里反复写回同一个属性。

## 8. 属性更新组

Qt 提供 `Qt::beginPropertyUpdateGroup()` / `Qt::endPropertyUpdateGroup()` 和 RAII 包装 `QScopedPropertyUpdateGroup`，用于把一组属性写入合并成一次延迟通知。

```cpp
{
    QScopedPropertyUpdateGroup group;
    width = 640;
    height = 480;
} // 离开作用域后统一发送依赖通知
```

这适合“多个输入必须一起提交”的状态更新。不要把 update group 跨越很长时间、阻塞等待或复杂回调；它应该包住一段短小、确定的同步修改。

## 9. 常见使用场景

### 9.1 C++ 状态派生

```cpp
struct LayoutState
{
    QProperty<int> columns { 3 };
    QProperty<int> rows { 2 };
    QProperty<int> cellCount { [this] { return columns.value() * rows.value(); } };
};
```

适合把“派生状态”从手动同步改成自动绑定。

### 9.2 暴露为 `QBindable`

```cpp
class Document : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QString title READ title WRITE setTitle BINDABLE bindableTitle)

public:
    QString title() const { return m_title.value(); }
    void setTitle(const QString &title) { m_title = title; }
    QBindable<QString> bindableTitle() { return &m_title; }

private:
    QProperty<QString> m_title;
};
```

这里 `QProperty` 存储值，`QBindable` 提供元属性系统可识别的绑定入口。

## 10. 常见错误

### 10.1 不保存 handler

```cpp
property.onValueChanged([] { qDebug() << "never"; });
```

返回值是 RAII 观察器；这一行结束后观察器销毁，回调不会在后续变化中执行。

### 10.2 给有绑定的属性直接赋值

直接赋值会移除绑定。想改变绑定结果，应修改绑定依赖的源属性；想替换规则，应调用 `setBinding()`。

### 10.3 绑定 lambda 捕获悬空引用

绑定可能晚于创建它的函数继续求值。捕获局部引用、临时对象或已销毁 QObject 裸指针都会变成悬空访问。

### 10.4 在回调里制造循环

属性 A 的变化写 B，B 的变化又写 A，很容易得到重复通知或绑定环。复杂状态应明确数据流方向，必要时使用 update group 或保护标志。

### 10.5 把它当线程同步工具

`QProperty` 的绑定和通知不是互斥锁，也不替你保证跨线程读写安全。跨线程修改共享状态仍需要 Qt queued 调用、锁或明确的线程归属协议。

## 11. 逐项 API 语义

### 构造与析构

| API | 语义 | 边界 |
| --- | --- | --- |
| `QProperty()` | 默认构造，底层 `T` 默认初始化。 | `T` 必须可默认构造。 |
| `explicit QProperty(parameter_type initialValue)` | 用初始值复制构造属性。 | 对非小型类型，`parameter_type` 通常是 `const T &`。 |
| `explicit QProperty(rvalue_ref initialValue)` | 移动初始值。 | 算术、枚举、指针类型没有这个 rvalue-ref 形式。 |
| `explicit QProperty(const QPropertyBinding<T> &binding)` | 构造后安装绑定。 | 绑定捕获对象必须活得足够久。 |
| `template <typename Functor> explicit QProperty(Functor &&f, const QPropertyBindingSourceLocation &location = QT_PROPERTY_DEFAULT_BINDING_LOCATION)` | 用 functor 创建绑定属性。 | functor 必须能返回 `T`；location 用于错误诊断。 |
| `~QProperty()` | 销毁属性并释放绑定观察节点。 | 不要让外部保存内部引用或指针。 |

### 读取

| API | 语义 | 边界 |
| --- | --- | --- |
| `parameter_type value() const` | 返回当前值，并在绑定求值期间登记依赖。 | 返回引用还是值取决于 `T` 的类型。 |
| `arrow_operator_result operator->() const` | 对指针或可解引用 `T` 提供成员访问。 | 仍会触发读取语义；不适合模糊表达依赖。 |
| `parameter_type operator*() const` | 读取当前值。 | 可读性通常不如 `value()`。 |
| `operator parameter_type() const` | 隐式转换为当前值。 | 在重载解析中可能隐藏依赖读取，复杂代码少用。 |
| `valueBypassingBindings() const` | 从 `QPropertyData` 继承，读取底层值但不登记依赖。 | 主要用于底层或刻意绕过依赖追踪的场景。 |

### 写入与绑定

| API | 语义 | 边界 |
| --- | --- | --- |
| `void setValue(parameter_type newValue)` | 移除当前绑定，复制写入新值并通知。 | 相等值通常不通知；依赖 `T` 的相等比较。 |
| `void setValue(rvalue_ref newValue)` | 移除当前绑定，移动写入新值并通知。 | 移动后不要再依赖传入对象原值。 |
| `QProperty<T> &operator=(parameter_type newValue)` | 调用 `setValue()` 后返回自身。 | 会拆掉已有绑定。 |
| `QProperty<T> &operator=(rvalue_ref newValue)` | 移动赋值形式。 | 会拆掉已有绑定。 |
| `QPropertyBinding<T> setBinding(const QPropertyBinding<T> &newBinding)` | 安装 typed 绑定并返回旧绑定。 | 返回值不是“成功标志”。 |
| `template <typename Functor> QPropertyBinding<T> setBinding(Functor &&f, const QPropertyBindingSourceLocation &location = QT_PROPERTY_DEFAULT_BINDING_LOCATION)` | 用 functor 创建并安装绑定。 | functor 无参可调用；捕获生命周期由调用者保证。 |
| `bool setBinding(const QUntypedPropertyBinding &newBinding)` | 安装 untyped 绑定。 | 非空绑定元类型不匹配时返回 `false`。 |
| `bool hasBinding() const` | 查询当前是否有绑定。 | 不代表绑定求值一定无错误。 |
| `QPropertyBinding<T> binding() const` | 返回当前绑定句柄。 | 空绑定表示当前没有绑定。 |
| `QPropertyBinding<T> takeBinding()` | 移除并返回当前绑定。 | 取出后属性保留当前值但不再自动更新。 |

### 观察与协作

| API | 语义 | 边界 |
| --- | --- | --- |
| `template <typename Functor> QPropertyChangeHandler<Functor> onValueChanged(Functor f)` | 后续值变化时调用回调。 | 必须保存返回的 RAII 对象；回调无参。 |
| `template <typename Functor> QPropertyChangeHandler<Functor> subscribe(Functor f)` | 立即调用一次，再监听后续变化。 | 初始化 UI 时常用；同样要保存返回值。 |
| `template <typename Functor> QPropertyNotifier addNotifier(Functor f)` | 添加类型擦除通知器。 | Qt 6.2 起提供；保存返回值维持订阅。 |
| `const QtPrivate::QPropertyBindingData &bindingData() const` | 暴露给 `QBindable`/观察器使用的绑定数据。 | 属于低层协作接口，业务代码通常不用直接碰。 |
| `Qt::makePropertyBinding(const QProperty<T> &otherProperty)` | 创建一个跟随另一个属性值的绑定。 | 绑定捕获的是被跟随属性的引用。 |
| `Qt::beginPropertyUpdateGroup()` / `Qt::endPropertyUpdateGroup()` | 手动开始/结束属性更新组。 | 必须配对；优先用 `QScopedPropertyUpdateGroup`。 |

### 比较

| API | 语义 | 边界 |
| --- | --- | --- |
| `operator==` / `operator!=` 与同类型 `QProperty<T>` | 比较两边 `value()`。 | 仅当 `T` 支持相等比较时可用。 |
| `operator==` / `operator!=` 与 `T` 或可比较类型 | 比较属性当前值与右值。 | 不同 `QProperty<T>`/`QProperty<U>` 之间被刻意禁止隐式比较。 |

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QProperty()` / `QProperty(value)` / `QProperty(binding)` / `QProperty(functor)` | 创建带初值或带绑定的属性。 | 构造后对象地址应保持稳定，不能复制移动。 |
| 读取 | `value()`、`operator*()`、`operator->()`、隐式转换 | 读取当前值并参与依赖追踪。 | 绑定表达式里优先显式写 `value()`。 |
| 写入 | `setValue()`、`operator=` | 手动设置属性值。 | 会移除已有绑定。 |
| 绑定 | `setBinding()`、`binding()`、`hasBinding()`、`takeBinding()` | 安装、查询或取出绑定。 | untyped 绑定要检查元类型匹配。 |
| 观察 | `onValueChanged()`、`subscribe()`、`addNotifier()` | 监听属性变化。 | 返回值是 RAII 句柄，必须保存。 |
| 批量更新 | `QScopedPropertyUpdateGroup` / `Qt::beginPropertyUpdateGroup()` | 合并一组变化通知。 | 用短作用域，避免跨阻塞或复杂回调。 |
| 比较 | `operator==` / `operator!=` | 按当前值比较。 | 要求值类型可比较，跨属性类型不做隐式比较。 |

---

### 一句话总结

`QProperty<T>` 是 Qt 6 响应式属性系统的核心值容器：读它会建立依赖，写它会通知依赖，而直接赋值会把已有绑定拆掉。
