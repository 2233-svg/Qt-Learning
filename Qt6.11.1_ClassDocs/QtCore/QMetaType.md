# QMetaType
> Qt 6.11.1 · Qt Core · 来自 `QMetaType`

## 作用定位
`QMetaType` 是 Qt 运行时类型系统的入口，标识、构造、销毁、转换、比较和注册可在 QVariant、属性、队列信号槽与反射 API 中流转的类型。

## API 速查
| API | 是做什么的 |
|---|---|
| `fromType<T>()` | 从编译期 C++ 类型取得元类型。|
| `id()` / `name()` | 读取运行时类型 ID 与名称。|
| `create()` / `destroy()` | 通过元类型构造或销毁实例。|
| `convert()` | 在注册支持时转换两个运行时类型。|
| `canConvert()` | 判断类型转换是否可行。|
| `registerType()` | 注册类型名与元类型系统。|
| `registerConverter()` | 注册自定义类型转换。|
| `isValid()` | 判断元类型是否有效。|

## 使用场景
把自定义值放入 `QVariant`、跨线程 queued signal/slot 传递、动态属性编辑、通用序列化和插件协议。

## 常见坑与经验
- `Q_DECLARE_METATYPE` 使类型可被元类型系统识别；跨线程队列调用还要确保类型在使用前正确注册。
- 指针类型注册不延长对象寿命；传递 `T*` 仍需明确所有权和线程安全。
- 使用 `void*` 的 create/destroy/convert API 时必须遵守构造、对齐和析构规则。

## 知识点覆盖
元类型、QVariant、queued connection、类型注册、运行时转换、对象生命周期、反射。
