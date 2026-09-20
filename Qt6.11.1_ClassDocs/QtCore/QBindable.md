# QBindable
> Qt 6.11.1 · Qt Core · 来自 `QBindable`

## 作用定位
`QBindable<T>` 是 Qt 属性绑定 API 的类型安全句柄，用于读取、安装或观察 `QProperty`/`Q_OBJECT_BINDABLE_PROPERTY` 的绑定。

## API 速查
| API | 是做什么的 |
|---|---|
| `value()` | 读取当前计算值。|
| `setBinding()` | 安装属性绑定。|
| `takeBinding()` | 移除并取走绑定。|
| `hasBinding()` | 判断是否由绑定驱动。|
| `subscribe()` | 订阅值变化。|
| `makeBinding()` | 从可调用对象创建绑定。|

## 使用场景
C++ 侧构建响应式属性关系，而不只依赖 QML binding。

## 常见坑与经验
- 直接 `setValue()` 通常会移除原绑定；先确认谁是值的唯一来源。
- 绑定表达式不能产生循环依赖或副作用。

## 知识点覆盖
响应式编程、属性绑定、依赖图、订阅、绑定覆盖。
