# QMetaProperty
> Qt 6.11.1 · Qt Core · 来自 `QMetaProperty`

## 作用定位
`QMetaProperty` 描述 QObject 的一个 `Q_PROPERTY`，可在运行时查询名称、类型、读写能力、通知信号、枚举信息，并按对象读写属性值。

## API 速查
| API | 是做什么的 |
|---|---|
| `name()` | 返回属性名。|
| `metaType()` | 返回属性的 `QMetaType`。|
| `read()` | 从 QObject 读取为 QVariant。|
| `write()` | 向 QObject 写入 QVariant 值。|
| `reset()` | 调用属性 RESET 函数。|
| `hasNotifySignal()` | 判断是否提供变化通知。|
| `notifySignal()` | 获取 notify 信号描述。|
| `isReadable()` / `isWritable()` | 查询读写能力。|
| `isEnumType()` / `enumerator()` | 查询是否关联枚举。|
| `isBindable()` | 查询是否支持 Qt 属性绑定。|

## 使用场景
属性编辑器、通用序列化、调试工具、脚本桥接和 QML/C++ 动态集成。

## 常见坑与经验
- `write()` 成功只表示元对象接受值，业务校验与副作用仍应由属性 setter 正确实现。
- 没有 notify signal 的可变属性不适合作为 QML 绑定源。
- QVariant 转换失败必须检测，不能让默认值悄悄覆盖真实配置。

## 知识点覆盖
Q_PROPERTY、QVariant、属性读写、notify、枚举、绑定、反射式编辑。
