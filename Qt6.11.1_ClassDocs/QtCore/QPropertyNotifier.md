# QPropertyNotifier
> Qt 6.11.1 · Qt Core · 来自 `QPropertyNotifier`

## 作用定位
`QPropertyNotifier` 是类型擦除后的属性变化订阅句柄。它和 `QPropertyChangeHandler<Functor>` 的生命周期语义相同，但把不同类型的 lambda、函数对象统一装入非模板类型，因此更适合做类成员、容器元素或对外接口返回值。

选择它并不是为了让通知“更持久”；持久性仍由 notifier 对象是否存活决定。它解决的是模板类型无法统一存放的问题。

## API 速查
| API | 是做什么的 |
|---|---|
| `QPropertyNotifier()` | 创建未关联属性的空通知器。 |
| `QPropertyNotifier(Functor)` | 保存一个无参数回调，供后续关联属性。 |
| `QPropertyNotifier(property, Functor)` | 直接监听指定属性。 |
| `QProperty<T>::addNotifier(Functor)` | 创建类型擦除的 notifier；属性变化时调用回调。 |
| 析构函数 | 解除订阅并释放保存的回调。 |
| 移动构造/赋值 | 转交订阅责任，旧对象不再维持该监听。 |

## 使用场景

### 在头文件中避免暴露 lambda 的具体类型
```cpp
class Controller {
    QProperty<int> m_retryCount{0};
    QPropertyNotifier m_retryNotifier;

public:
    Controller()
        : m_retryNotifier(m_retryCount.addNotifier([this] {
            scheduleRetry(m_retryCount.value());
        }))
    {}
};
```
若改用 `QPropertyChangeHandler`，成员类型需要携带 lambda 的具体类型，通常不方便在类定义中表达；`QPropertyNotifier` 因此更自然。

### 动态替换监听对象
把 notifier 移动赋给新的值会先结束原订阅，再接管新订阅。适合“当前选中对象”切换时只保留一个监听器，但应确保切换过程不会遗漏必要的一次状态同步。

## 常见坑与经验
- `property.addNotifier([] {...});` 若不保存返回值，只会存在到当前语句结束。
- notifier 回调无参数。需要新值时读取原属性；若回调将被延后执行，不要把它当成变化瞬间的快照。
- 类型擦除通常意味着少量间接调用和可能的动态分配；高频极热路径可比较模板化 handler 的成本。
- 回调捕获的对象必须仍然有效；`QPointer`、弱引用或析构时复位 notifier 可以降低悬空访问风险。
- 不要在通知中写回同一属性，除非你已经验证更新会收敛而非反复触发。

## 知识点覆盖
类型擦除、`std::function` 风格回调、RAII 订阅、属性通知、对象成员设计、移动所有权、回调生命周期、重入控制。
