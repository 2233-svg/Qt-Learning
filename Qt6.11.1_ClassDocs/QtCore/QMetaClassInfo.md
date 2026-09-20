# QMetaClassInfo
> Qt 6.11.1 · Qt Core · 来自 `QMetaClassInfo`

## 作用定位
`QMetaClassInfo` 描述 `Q_CLASSINFO` 宏写入 QObject 元对象的静态名称值信息，常用于声明式元数据而非运行时业务状态。

## API 速查
| API | 是做什么的 |
|---|---|
| `name()` | 返回 class info 的键名。|
| `value()` | 返回 class info 的字符串值。|
| `Q_CLASSINFO(name, value)` | 在类声明中添加元信息。|

## 使用场景
为插件、QML 类型、RPC 服务或属性编辑器附加固定描述、版本或能力标签。

## 常见坑与经验
- class info 是编译期静态文本，不能替代可变化的 `Q_PROPERTY`。
- 值是字符串，复杂结构需要自行定义编码并处理版本兼容。

## 知识点覆盖
Q_CLASSINFO、元对象、静态元数据、插件描述、字符串协议。
