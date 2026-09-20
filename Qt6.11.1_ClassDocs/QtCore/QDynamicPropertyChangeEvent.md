# QDynamicPropertyChangeEvent
> Qt 6.11.1 · Qt Core · 来自 `QDynamicPropertyChangeEvent`

## 作用定位
`QDynamicPropertyChangeEvent` 在 QObject 的动态属性通过 `setProperty()` 改变时投递给对象，携带被修改属性名。

## API 速查
| API | 是做什么的 |
|---|---|
| `propertyName()` | 返回变化的动态属性名。|
| `QEvent::DynamicPropertyChange` | 对应事件类型。|

## 使用场景
通用组件框架用动态属性附加主题、测试标记或元数据，并在对象 `event()` 中观察更新。

## 常见坑与经验
- 动态属性没有编译期类型约束和 notify signal；长期业务状态优先使用正式 `Q_PROPERTY`。
- 事件到来后读取的值应按 `QVariant` 类型校验，不能假设设置方始终正确。

## 知识点覆盖
动态属性、QVariant、事件通知、元对象、类型校验、框架扩展。
