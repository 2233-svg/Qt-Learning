# QPropertyChangeHandler
> Qt 6.11.1 · Qt Core · 来自 `QPropertyChangeHandler<Functor>`

## 作用定位
`QPropertyChangeHandler` 是 `QProperty` 的 RAII 订阅句柄。它把“监听属性变化”绑定到一个 C++ 对象的生命周期：句柄存在，回调有效；句柄析构、被移动覆盖或显式替换后，订阅自动解除。

它不同于 `QObject::connect()` 返回的连接对象：这里的回调是无参数函子，通常在回调中再次读取属性的当前值。选择它的核心理由是让订阅所有权变得显式。

## API 速查
| API | 是做什么的 |
|---|---|
| `QPropertyChangeHandler(Functor)` | 保存回调，供低层属性观察流程后续关联。 |
| `QPropertyChangeHandler(property, Functor)` | 立即监听指定属性。 |
| `QProperty<T>::onValueChanged(Functor)` | 值以后变化时调用回调，返回应长期保存的 handler。 |
| `QProperty<T>::subscribe(Functor)` | 先立刻调用一次，再继续监听变化。 |
| 析构函数 | 自动注销观察关系。 |
| 移动构造/赋值 | 转移订阅所有权；适合把 handler 放进成员变量。 |

## 使用场景

### 让视图状态跟随一个 C++ 属性
```cpp
class StatusPresenter {
    QProperty<QString> m_status;
    QPropertyChangeHandler<std::function<void()>> m_statusHandler;

public:
    StatusPresenter()
        : m_statusHandler(m_status.onValueChanged([this] {
            refreshStatusText(m_status.value());
        }))
    {}
};
```
成员顺序很重要：回调捕获的对象和被观察属性应当比 `m_statusHandler` 更晚销毁，避免析构期间回调访问已经结束生命周期的成员。

### 区分首次同步与后续变化
初始化 UI、缓存或派生状态时用 `subscribe()` 很合适，因为不必额外手动调用一次同步函数；只希望响应未来变化时，用 `onValueChanged()`。

```cpp
auto initialAndFuture = temperature.subscribe([&] {
    updateLabel(temperature.value());
});
```

## 常见坑与经验
- 最常见的漏订阅写法是 `property.onValueChanged(...);`：返回的临时 handler 在分号处析构，回调从未持续存在。
- 回调没有新值参数，读取 `property.value()` 时拿到的是当前值；不要假定它等同于事件发生瞬间的历史快照。
- 回调内不要修改会再次触发该回调的依赖链；确有需要时要设计明确的收敛条件。
- 句柄不是跨线程消息队列。属性和回调所访问对象仍须遵守所属线程与同步规则。
- 捕获裸 `this` 时，handler 必须在对象销毁前解除或随对象一同销毁。

## 知识点覆盖
RAII、属性观察、订阅所有权、回调捕获、初始化同步、重入、析构顺序、线程亲和性、与 signals/slots 的取舍。
