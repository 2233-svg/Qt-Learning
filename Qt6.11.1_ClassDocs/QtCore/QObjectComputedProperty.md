# QObjectComputedProperty
> Qt 6.11.1 · Qt Core · 来自 `QObjectComputedProperty`

## 作用定位
`QObjectComputedProperty<Class, T, ...>` 将一个只读计算属性接入 QObject 属性系统与 Qt 绑定系统。属性值由计算函数派生，而非由独立存储字段直接保存。

## API 速查
| API | 是做什么的 |
|---|---|
| `value()` | 计算或读取当前派生值。|
| `bindable()` | 返回可订阅的 `QBindable<T>`。|
| `markDirty()` | 标记依赖变化，需要重新计算。|
| `onValueChanged()` | 订阅派生值变化。|

## 使用场景
暴露 `fullName`、`isReady`、汇总金额、格式化状态等由多个底层属性计算出的只读 Q_PROPERTY。

## 常见坑与经验
- 依赖值改变时必须正确触发失效/通知，否则 UI 会长期显示旧派生值。
- 计算函数应无副作用且足够快；它可能在绑定读取时多次执行。
- 计算属性不能替代缓存策略：昂贵计算需要明确缓存、失效和线程边界。

## 知识点覆盖
计算属性、响应式依赖、Q_PROPERTY、缓存失效、QBindable、无副作用计算。
