# Qt QPropertyNotifier：类型擦除的属性通知 RAII 句柄

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QPropertyNotifier>`  
> 所属模块：`Qt6::Core`  
> 自 Qt：6.2  
> 继承：`QPropertyObserver -> QPropertyNotifier`  
> 类型性质：不可复制、可移动的类型擦除观察器

## 1. 它解决什么问题

`QPropertyNotifier` 保存一个无参属性变化回调，并用自身生命周期控制回调是否仍注册在属性上。它和 `QPropertyChangeHandler<Functor>` 的职责相同，但内部使用 `std::function<void()>` 擦除了具体回调类型，因此更容易声明成固定的类成员。

```cpp
class StatusPresenter
{
public:
    explicit StatusPresenter(QProperty<int> &status)
        : m_notifier(status.addNotifier([this, &status] {
              showStatus(status.value());
          }))
    {
    }

private:
    QPropertyNotifier m_notifier;
};
```

它适合：

- 把属性观察器保存为普通成员，而不暴露 lambda 类型；
- 在统一容器或接口里保存不同回调；
- 需要移动观察责任；
- 希望离开作用域时自动取消属性回调。

## 2. 与 QPropertyChangeHandler 的区别

```text
QPropertyChangeHandler<Functor>
  回调具体类型是模板参数
  通常由 onValueChanged()/subscribe() 返回
  局部 auto 使用最自然

QPropertyNotifier
  回调统一存为 std::function<void()>
  通常由 addNotifier() 返回
  成员字段和统一存储更方便
```

类型擦除可能带来 `std::function` 的存储或间接调用成本，但多数界面状态与业务通知场景里，它换来的固定类型更实用。

## 3. 创建与保存

最常见入口是：

```cpp
QPropertyNotifier notifier = property.addNotifier([&] {
    refresh();
});
```

`addNotifier()` 支持 `QProperty`、QObject bindable 属性、computed 属性以及 `QBindable`/`QUntypedBindable`。回调必须无参可调用。

不要忽略返回值：

```cpp
property.addNotifier(refresh); // 临时 notifier 立即析构，观察马上取消
```

作为成员时，通常先声明属性或保证外部属性长寿，再声明 notifier，使 notifier 能在属性之前解除连接。

## 4. 默认构造与延后连接

`QPropertyNotifier` 可以默认构造为空观察器：

```cpp
QPropertyNotifier notifier;
```

也可以先用回调构造，再通过继承的 `setSource()` 指定属性。这个方式适合底层封装，但业务代码通常直接使用 `addNotifier()`，因为它能一次完成回调创建和 source 连接。

默认构造的 notifier 没有回调和观察源，析构它不会产生属性通知。

## 5. 移动与重置

```cpp
QPropertyNotifier first = property.addNotifier(callback);
QPropertyNotifier second = std::move(first);
```

移动把现有观察关系交给 `second`，不会复制出两次回调。移动赋值还会先释放目标对象原本持有的观察关系。

若要显式取消订阅，可以让 notifier 析构、用空 notifier 覆盖它，或从拥有它的容器中移除：

```cpp
notifier = QPropertyNotifier{};
```

## 6. 回调执行边界

回调是在属性系统发出变化通知时调用的。它不保证排队到事件循环，也不等同于 queued signal/slot；根据更新组等上下文，通知可能立即发生或被延迟。

回调没有参数，需要时应在回调内读取属性：

```cpp
QPropertyNotifier notifier = progress.addNotifier([&] {
    updateProgress(progress.value());
});
```

读取源属性要保证源仍存活。捕获 QObject 裸指针时，必要时使用 `QPointer`：

```cpp
QPointer<Widget> widget = target;
QPropertyNotifier notifier = property.addNotifier([widget] {
    if (widget)
        widget->update();
});
```

## 7. 实际使用场景

### 7.1 固定成员观察器

```cpp
class ActionState
{
public:
    explicit ActionState(QProperty<bool> &enabled)
        : m_enabledNotifier(enabled.addNotifier([this, &enabled] {
              apply(enabled.value());
          }))
    {
        apply(enabled.value());
    }

private:
    QPropertyNotifier m_enabledNotifier;
};
```

由于 `addNotifier()` 不会像 `subscribe()` 那样先调用一次，这里手工执行一次初始化。

### 7.2 可替换的观察目标

```cpp
void Presenter::watch(QProperty<QString> &title)
{
    m_titleNotifier = title.addNotifier([this, &title] {
        setTitle(title.value());
    });
    setTitle(title.value());
}
```

新的移动赋值会解除旧属性的观察，再接管新 notifier。注意 lambda 捕获的 `title` 必须比 notifier 活得久。

## 8. 常见错误

### 8.1 认为 `addNotifier()` 会立即调用

它只安装后续通知。需要“先初始化一次，再持续监听”时，手工调用一次，或使用 `subscribe()` 返回的模板 handler。

### 8.2 把 notifier 当成属性值快照

它不保存属性值，只保存回调和观察节点。新值要在回调中读取。

### 8.3 复制 notifier

该类不可复制。用 `std::move()` 转移责任，或者分别调用 `addNotifier()` 创建两个独立观察器。

### 8.4 source 或捕获对象先销毁

观察器的 RAII 只能解除自己仍连接的节点，不能延长源属性或捕获对象的生命周期。成员声明顺序和外部 owner 必须明确。

### 8.5 在回调中形成递归写入

无条件写回源属性，或两个 notifier 互相写对方，可能形成通知环。先比较状态、明确单向数据流，或使用批量更新组。

## 9. 逐项 API 语义

### 构造与连接

| API | 语义 | 边界 |
| --- | --- | --- |
| `QPropertyNotifier()` | 创建空 notifier。 | 没有回调，也没有 source。 |
| `template <typename Functor> QPropertyNotifier(Functor handler)` | 保存类型擦除后的无参回调。 | 尚需 `setSource()`；通常由框架内部流程使用。 |
| `template <typename Functor, typename Property> QPropertyNotifier(const Property &property, Functor handler)` | 创建回调并立即观察属性。 | `Property` 必须提供绑定数据。 |
| `property.addNotifier(Functor f)` | 创建并返回已连接 notifier。 | 不立即调用回调；必须保存返回值。 |
| `setSource(const Property &property)` | 从 `QPropertyObserver` 继承，设置或切换观察源。 | 低层入口；优先使用 `addNotifier()`。 |

### 生命周期

| API | 语义 | 边界 |
| --- | --- | --- |
| `QPropertyNotifier(QPropertyNotifier &&other)` | 接管 `other` 的回调和观察关系。 | `other` 不再持有原订阅。 |
| `operator=(QPropertyNotifier &&other)` | 释放当前观察关系后接管另一个。 | 可用于替换当前观察目标。 |
| `~QPropertyNotifier()` | 自动解除仍持有的观察关系。 | 析构位置决定订阅何时结束。 |
| 复制构造/复制赋值 | 不可用。 | 需要两个观察者时分别调用 `addNotifier()`。 |

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 获取 | `property.addNotifier(callback)` | 创建已连接的类型擦除观察器。 | 不立即调用，保存返回值。 |
| 空状态 | `QPropertyNotifier()` | 创建无回调、无 source 的句柄。 | 可用于成员默认状态或显式重置。 |
| 直接构造 | `QPropertyNotifier(property, callback)` | 同时保存回调并连接属性。 | 通常让 `addNotifier()` 完成。 |
| 切换源 | `setSource()` | 改变观察目标。 | 注意回调捕获是否仍适配新 source。 |
| 转移 | 移动构造、移动赋值 | 转移唯一订阅责任。 | 移动赋值会取消目标原订阅。 |
| 取消 | 析构或赋空 notifier | 解除属性观察。 | 没有单独的 QObject disconnect。 |

---

### 一句话总结

`QPropertyNotifier` 是固定类型的属性通知句柄：它用 `std::function` 擦除回调类型，并用 move-only RAII 生命周期控制订阅。
