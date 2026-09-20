# QUntypedBindable
> Qt 6.11.1 · Qt Core · 来自 `QUntypedBindable`
## 作用定位
`QUntypedBindable` 是属性绑定系统的类型擦除入口，用于在不知道属性具体 `T` 的情况下检查、设置或观察绑定。
## API 速查
| API | 是做什么的 |
|---|---|
| `isValid()` | 判断是否指向可绑定属性。 |
| `makeBinding()` / `setBinding()` | 创建或安装无类型绑定。 |
| `binding()` / `takeBinding()` | 查询或取走当前绑定。 |
| `hasBinding()` | 判断是否已绑定。 |
| `metaType()` | 查询属性值的元类型。 |
| `addNotifier()` | 添加无类型变化通知。 |
## 使用场景
元对象、属性编辑器或 QML/C++ 桥接层按属性名处理绑定时使用。
## 常见坑与经验
- 类型擦除不等于无类型安全；写入前必须检查 `QMetaType`。
- 通知器返回值仍要保存，否则订阅立即失效。
- 业务代码能用 `QBindable<T>` 时更清晰。
## 知识点覆盖
属性绑定、类型擦除、元类型、反射、通知生命周期。
