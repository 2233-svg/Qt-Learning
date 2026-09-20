# QDBusSignature
> Qt 6.11.1 · Qt D-Bus · 来自 `QDBusSignature`

## 作用定位

`QDBusSignature` 是 D-Bus 类型签名的类型包装。签名是协议层的类型描述，例如 `s` 表示字符串，`u` 表示无符号 32 位整数，`a{sv}` 表示字符串到 variant 的字典。用 `QDBusSignature` 作为参数时，D-Bus 签名会是 `g`，而不是普通字符串 `s`。

## 类说明

- 头文件：`#include <QDBusSignature>`
- CMake：链接 `Qt6::DBus`
- 继承：无公开 QObject 继承

## API 速查

| API | 说明 |
| --- | --- |
| `QDBusSignature()` | 创建空签名对象。 |
| `QDBusSignature(QLatin1StringView)` | 从 Latin-1 字符串构造签名。 |
| `QDBusSignature(const QString &)` | 从 QString 构造签名。 |
| `QDBusSignature(const char *)` | 从 C 字符串构造签名。 |
| `setSignature()` | 修改签名字符串。 |
| `signature()` | 读取签名字符串。 |
| `swap()` | 快速交换两个签名对象。 |

## 使用场景

- 调用或实现需要 D-Bus signature 类型参数的接口。
- 调试动态消息，把 `QDBusMessage::signature()` 的内容与预期接口对照。
- 描述 variant 内部允许的类型或动态容器结构。

## 常见坑与经验

- `QDBusSignature("s")` 的协议类型是 signature，本身签名为 `g`；它的内容才是 `s`。
- `QString("s")` 会作为普通字符串传输，不等于 D-Bus signature。
- 签名语法很紧凑，`a{sv}`、`(su)`、`av` 少一个括号或字母都会导致 `InvalidSignature`。
- 不要用签名字符串替代真实类型注册；签名能描述协议形状，但 Qt 仍要知道怎么把 C++ 类型封送进去。

## 知识点覆盖

- D-Bus signature 类型 `g`
- 常见签名：`s`、`u`、`b`、`o`、`v`、`a{sv}`
- 签名与 Qt 元类型的配合
- 类型不匹配错误排查
