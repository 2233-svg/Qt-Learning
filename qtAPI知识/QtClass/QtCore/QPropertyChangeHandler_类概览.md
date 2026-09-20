# Qt QPropertyChangeHandler：属性回调的模板化 RAII 句柄

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QPropertyChangeHandler>`  
> 所属模块：`Qt6::Core`  
> 继承：`QPropertyObserver -> QPropertyChangeHandler<Functor>`  
> 类型性质：不可复制、可移动的模板观察器

## 1. 它解决什么问题

`QPropertyChangeHandler<Functor>` 管理一个属性变化回调的安装期限。它通常由 `QProperty::onValueChanged()` 或 `subscribe()` 返回：句柄活着，回调就保持注册；句柄析构，观察关系自动解除。

```cpp
QProperty<int> count(0);

auto handler = count.onValueChanged([&] {
    qDebug() << "count:" << count.value();
});

count = 1; // 调用回调
```

它适合：

- 让属性回调跟随对象成员或局部作用域自动解绑；
- 不引入 QObject connection id；
- 保留 lambda、函数对象等回调的具体类型；
- 通过移动把观察责任交给另一个作用域或对象。

它不是 `QMetaObject::Connection`，也不依赖 signal/slot。它观察的是 Qt 绑定属性系统中的属性通知。

## 2. 谁创建它

日常代码通常不直接拼出模板类型，而是接住属性 API 的返回值：

```cpp
auto changed = property.onValueChanged(callback);
auto subscribed = property.subscribe(callback);
```

支持这些 API 的对象包括：

- `QProperty<T>`；
- `QObjectBindableProperty<...>`；
- `QObjectComputedProperty<...>`；
- `QBindable<T>` 和 `QUntypedBindable`。

`onValueChanged()` 只监听后续通知；`subscribe()` 会先同步调用一次回调，再安装后续观察器。

## 3. 生命周期就是订阅期限

```cpp
{
    auto handler = count.onValueChanged(updateUi);
    count = 1; // updateUi 被调用
}

count = 2;     // handler 已析构，不再调用
```

最常见错误是忽略返回值：

```cpp
count.onValueChanged(updateUi); // 语句结束，临时 handler 立即析构
```

这段代码编译通过，却几乎没有持续效果。应把 handler 放在生命周期足够长的位置，例如观察者对象的成员。

由于 lambda 类型不便手写，成员存储时通常使用 `auto` 局部变量、具名 functor，或者改用类型擦除的 `QPropertyNotifier`。

```cpp
class ViewModel
{
    QProperty<int> m_count;
    QPropertyNotifier m_handler;

public:
    ViewModel()
        : m_handler(m_count.addNotifier([this] { rebuildText(); }))
    {
        rebuildText();
    }
};
```

## 4. 模板型与类型擦除型的取舍

```text
QPropertyChangeHandler<Functor>
  保存具体 Functor 类型
  由 onValueChanged()/subscribe() 返回
  适合 auto 局部变量或泛型代码

QPropertyNotifier
  内部使用 std::function<void()>
  由 addNotifier() 返回
  类型固定，适合类成员、容器或统一接口
```

如果代码能使用 `auto`，模板型 handler 避免类型擦除；如果必须在头文件中声明固定成员类型，`QPropertyNotifier` 往往更方便。

## 5. 移动语义

handler 不可复制，但可移动：

```cpp
auto first = count.onValueChanged(callback);
auto second = std::move(first);
```

移动后，订阅责任由 `second` 持有；被移动对象进入有效但不再承担原观察关系的状态。不要把“移动 handler”误解成复制出第二份订阅。

将 handler 存入容器时，容器操作必须支持 move-only 元素；也不要让容器重建、清空或覆盖元素时无意取消订阅。

## 6. 属性与回调的生命周期边界

回调持续有效需要：

- handler 仍然存活；
- 被观察属性仍然存活；
- 回调捕获的对象仍然有效。

handler 能管理“自己何时解绑”，却不能自动保护 lambda 捕获的裸指针。

```cpp
QPointer<QObject> context = object;
auto handler = property.onValueChanged([context] {
    if (context)
        updateObject(context);
});
```

如果捕获的是 QObject，可用 `QPointer` 防止对象销毁后继续解引用。普通 C++ 对象则应通过成员析构顺序、智能指针或显式重置 handler 保证安全。

## 7. 回调时机与重入

属性通知可能立即执行，也可能因属性更新组等上下文而延迟。不要把回调当作排队到事件循环的 queued slot，也不要依赖它必然异步。

回调必须可无参调用。需要新值时，在回调内读取属性：

```cpp
auto handler = count.onValueChanged([&] {
    consume(count.value());
});
```

回调中再修改属性可能触发更多绑定求值和通知。应避免：

- 无条件写回被观察属性；
- A 回调写 B、B 回调又写 A；
- 在回调中销毁仍处于通知链中的复杂对象；
- 假定多个相关属性已经全部更新。

需要成组提交多个值时，可以用 `QScopedPropertyUpdateGroup` 缩小中间状态暴露。

## 8. 重新指定观察源

基类 `QPropertyObserver` 提供 `setSource()`，因此一个已构造的 handler 可以被连接到属性的绑定数据。直接使用这一低层入口时，调用者必须保证 handler 已经带有正确回调，并确认切换后旧观察关系不再需要。

日常代码优先从 `onValueChanged()` / `subscribe()` 获取已经正确连接的 handler；它们更清楚，也不容易得到“有回调但没有 source”的半成品。

## 9. 常见错误

### 9.1 不保存返回值

临时 handler 在完整表达式结束时析构，订阅立即取消。

### 9.2 handler 成员比属性后析构

C++ 成员按声明逆序析构。最稳妥的声明顺序是先声明属性，再声明观察它的 handler，使 handler 先析构、属性后析构。

### 9.3 捕获比 handler 短命的对象

RAII 只管理观察关系，不管理 lambda 捕获。捕获引用和裸指针时要单独检查生命周期。

### 9.4 把通知当成跨线程消息

属性观察器不是 queued connection。共享或 QObject 成员属性的跨线程访问仍要遵守相应同步和线程归属规则。

### 9.5 用 `subscribe()` 后又手工初始化两次

`subscribe()` 本身会先调用回调。若只想监听后续变化，用 `onValueChanged()`。

## 10. 逐项 API 语义

### 构造与连接

| API | 语义 | 边界 |
| --- | --- | --- |
| `explicit QPropertyChangeHandler(Functor handler)` | 创建带回调但尚未指定 source 的观察器。 | 常供 `QBindable` 等内部连接流程使用；回调必须无参可调用。 |
| `template <typename Property> QPropertyChangeHandler(const Property &property, Functor handler)` | 创建回调并立即观察 `property`。 | `Property` 必须提供属性绑定数据。 |
| `property.onValueChanged(Functor f)` | 返回监听后续变化的 handler。 | 不立即调用；必须保存返回值。 |
| `property.subscribe(Functor f)` | 先调用 `f()`，再返回监听后续变化的 handler。 | 初始化动作同步发生在调用点。 |
| `setSource(const Property &property)` | 从基类继承，重新指定观察源。 | 切换 source 会改变当前观察关系。 |

### 生命周期

| API | 语义 | 边界 |
| --- | --- | --- |
| `QPropertyChangeHandler(QPropertyChangeHandler &&other)` | 移交观察节点与回调。 | 不复制订阅；被移动对象不再持有原关系。 |
| `operator=(QPropertyChangeHandler &&other)` | 先释放当前关系，再接管 `other`。 | 覆盖现有 handler 会取消原订阅。 |
| `~QPropertyChangeHandler()` | 解除仍持有的观察关系。 | 回调停止时间由对象析构位置决定。 |
| 复制构造/复制赋值 | 不可用。 | 一个观察节点不能被复制成两个 owner。 |

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 获取 | `onValueChanged()` | 监听后续属性通知。 | 创建时不调用回调。 |
| 获取 | `subscribe()` | 立即同步一次，再监听后续通知。 | 不要重复手工初始化。 |
| 直接构造 | `QPropertyChangeHandler(property, callback)` | 把具体 functor 与属性连接。 | 通常让属性 API 推导模板参数。 |
| 切换源 | `setSource()` | 让 handler 观察另一个属性。 | 属于较低层操作，注意旧订阅被替换。 |
| 转移 | 移动构造、移动赋值 | 转移订阅责任。 | 不会复制订阅。 |
| 取消 | 析构或覆盖 handler | 自动解除观察。 | handler 生命周期就是订阅期限。 |

---

### 一句话总结

`QPropertyChangeHandler<Functor>` 是属性回调的 move-only RAII 句柄：保存它才有持续订阅，销毁它就是取消订阅。
