# QObjectBindableProperty
> Qt 6.11.1 · Qt Core · 来自 `QObjectBindableProperty`

## 作用定位
`QObjectBindableProperty<Class, T, ...>` 将 Qt 绑定属性与 QObject 的 `Q_PROPERTY`/notify 机制结合，使 C++ 属性既可被元对象和 QML 访问，也可参与 C++ 响应式绑定。

## API 速查
| API | 是做什么的 |
|---|---|
| `value()` | 读取当前属性值。|
| `setValue()` | 设置值，通常会移除已有绑定。|
| `setBinding()` | 安装计算绑定。|
| `bindable()` | 返回 `QBindable<T>` 句柄。|
| `onValueChanged()` | 注册值变化处理器。|
| `takeBinding()` | 移除并取回绑定。|

## 使用场景
为 QObject 子类实现需暴露给 QML、又希望在 C++ 中建立自动依赖更新的现代属性。

## 常见坑与经验
- 直接 `setValue()` 与绑定是两种不同的值来源；业务设计应规定谁拥有最终写入权。
- 绑定表达式避免副作用和循环依赖，否则变化链难以诊断。
- notify 信号、Q_PROPERTY 读写函数与底层属性值必须保持一致。

## 知识点覆盖
Q_PROPERTY、QBindable、响应式属性、QML、notify、依赖图、绑定覆盖。
