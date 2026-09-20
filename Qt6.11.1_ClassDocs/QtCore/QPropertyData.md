# QPropertyData
> Qt 6.11.1 · Qt Core · 来自 `QPropertyData<T>`

## 作用定位
`QPropertyData<T>` 是 `QProperty<T>` 与 `QObjectBindableProperty` 使用的底层存值基类。它提供一组刻意“绕开绑定系统”的读写函数，主要服务于自定义属性封装、内部实现和需要控制依赖收集的场景。

日常应用代码应优先使用 `QProperty::value()`、`setValue()` 或绑定 API。只有当你明确知道自己不希望触发绑定求值、变化传播或依赖登记时，才使用本类。

## API 速查
| API | 是做什么的 |
|---|---|
| `setValueBypassingBindings(const T &)` | 直接写入底层存储，不评估或替换已注册的绑定。 |
| `setValueBypassingBindings(T &&)` | 以移动语义直接写入底层值，适合较大的可移动对象。 |
| `valueBypassingBindings()` | 直接读取已存储的值，不触发绑定计算，也不登记读取依赖。 |

## 使用场景

### 在自定义属性类型中维护缓存
派生封装有时需要保存一个缓存值，而不希望缓存维护本身被当成业务属性变化：

```cpp
class CachedNumber : public QPropertyData<int> {
public:
    void updateCachedValue(int value)
    {
        setValueBypassingBindings(value);
    }
};
```
这类代码应把“缓存字段”与“面向外部的绑定属性”明确区分，避免调用者误以为写入会自动通知观察者。

### 避免把内部读取加入依赖图
在绑定表达式运行期间，普通的属性读取会被记录为依赖。内部探测、调试或实现细节确实不应成为依赖时，`valueBypassingBindings()` 能避免产生额外边。

## 常见坑与经验
- 绕过绑定读到的可能是旧缓存：若属性当前由绑定计算，正确的可见值应通过正常 `value()` 路径取得。
- 绕过绑定写入不会替你修复依赖关系、发送你期待的业务通知或更新 UI；它不是“更快的 `setValue()`”。
- 该类属于属性系统的基础设施。把它直接用于业务成员，会使维护者难以判断一次读写是否参与响应式传播。
- 对非平凡 `T`，优先用右值重载转移资源；但不要在写后继续依赖被移动对象的内容。

## 知识点覆盖
Qt 属性系统、底层存储、绑定求值、依赖收集、缓存一致性、移动语义、封装边界、响应式程序设计。
