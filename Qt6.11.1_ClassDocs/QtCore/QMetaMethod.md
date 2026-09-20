# QMetaMethod
> Qt 6.11.1 · Qt Core · 来自 `QMetaMethod`

## 作用定位
`QMetaMethod` 描述 QObject 元对象中的一个信号、槽或 `Q_INVOKABLE` 方法，可在运行时查询签名、参数、访问级别并动态调用。

## API 速查
| API | 是做什么的 |
|---|---|
| `name()` | 返回方法名。|
| `methodSignature()` | 返回规范化方法签名。|
| `parameterTypes()` / `parameterNames()` | 查询参数类型与名称。|
| `returnMetaType()` | 查询返回值元类型。|
| `methodType()` | 区分 Signal、Slot、Method、Constructor。|
| `access()` | 查询 public/protected/private。|
| `invoke()` | 通过对象实例动态调用。|
| `fromSignal()` | 从信号成员指针获取元方法。|

## 使用场景
插件检查、通用 RPC/脚本桥接、运行时调试工具或自动化测试需要发现并调用 QObject 可公开方法。

## 常见坑与经验
- 动态调用失去编译期签名检查；普通代码优先直接函数调用或类型安全 signal/slot。
- queued `invoke()` 参数必须是可复制且已注册的元类型。
- 返回值只能在同步直接调用中自然取得；跨线程异步调用应使用信号或 future。

## 知识点覆盖
元对象方法、信号槽、Q_INVOKABLE、动态调用、参数元类型、线程调用模式。
