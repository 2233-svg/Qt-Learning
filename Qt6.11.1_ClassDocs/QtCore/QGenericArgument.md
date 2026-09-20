# QGenericArgument
> Qt 6.11.1 · Qt Core · 来自 `QGenericArgument`

## 作用定位
`QGenericArgument` 是旧式运行时元对象调用的参数包装类型，主要服务于字符串方法名形式的 `QMetaObject::invokeMethod()`。

## API 速查
| API | 是做什么的 |
|---|---|
| `Q_ARG(Type, value)` | 从编译期类型和值生成通用参数。|
| `name()` | 返回注册的参数类型名。|
| `data()` | 返回参数数据指针。|

## 使用场景
兼容旧代码，或需要按运行时方法名调用 QObject 槽/可调用方法时作为 invokeMethod 参数。

## 常见坑与经验
- 新代码优先使用函数指针或 lambda 形式的 `invokeMethod()`，能获得编译期参数检查。
- queued 调用要求参数类型已注册为元类型，且传入数据要能被安全复制。
- `data()` 指针不拥有值，不能跨越原始对象生命周期保存。

## 知识点覆盖
元对象调用、Q_ARG、运行时类型、queued connection、元类型注册、生命周期。
