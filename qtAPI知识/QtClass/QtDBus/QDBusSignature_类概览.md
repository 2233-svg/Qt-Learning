# QDBusSignature：在 QVariant 中保留 D-Bus SIGNATURE 类型

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDBusSignature>`  
> 模块：`Qt6::DBus`  
> 相关类：`QDBusArgument`、`QDBusObjectPath`、`QDBusMessage`

## 它解决什么问题

D-Bus signature 是描述 D-Bus 值类型序列的紧凑编码。例如：

```text
s      一个 STRING
i      一个 32 位有符号整数
o      一个 OBJECT_PATH
a{sv}  一个以 STRING 为键、VARIANT 为值的字典
```

虽然 signature 的内容也是文本，但 D-Bus 在线路协议上把它定义为独立的 `SIGNATURE` 类型。`QDBusSignature` 让这个差异在 Qt 类型系统和 `QVariant` 中保留下来。

```text
QString("a{sv}")
  -> D-Bus STRING

QDBusSignature("a{sv}")
  -> D-Bus SIGNATURE
```

它不是用来替代 C++ 模板类型检查的工具，也不是大多数业务调用都需要手工创建的对象。它主要在需要传递或接收 D-Bus 类型描述本身时使用。

## 适用场景

- 接口协议将某个参数或返回值定义为 D-Bus `SIGNATURE`。
- 编写通用 D-Bus 浏览器、代理、动态调用器或元数据工具。
- 将签名作为 `QVariant` 或 `QDBusArgument` 中的明确类型传输。

不适合：

- 普通远程方法的参数和返回值，直接传实际 C++ 值即可。
- 用它验证任意字符串一定是合法签名。
- 用它解析复杂数据；解析和流式编解码应使用 D-Bus 类型系统、`QDBusArgument` 或明确的数据结构。

## 最小示例

```cpp
#include <QDBusSignature>
#include <QVariant>

const QDBusSignature signature("a{sv}");
const QVariant value = QVariant::fromValue(signature);

// value 在 D-Bus 上的类型是 SIGNATURE，而不是 STRING。
```

若远端接口签名要求 `g`（SIGNATURE），却传递 `QString("a{sv}")`，实际类型是 `s`（STRING），协议层会出现类型不匹配。

## 签名描述的是 D-Bus 类型，不是 C++ 类型名

`"s"` 不等于 `QString` 这个 C++ 类型名，而是 D-Bus 的 STRING 类型编码；`"a{sv}"` 描述的是字典结构，而不是某个具体 `QMap` 模板实例。Qt 会在传输时根据已注册的类型、`QDBusArgument` 流操作符和 D-Bus 规则做实际映射。

因此，阅读 signature 时要先问两个问题：

1. 它描述的是一个类型，还是一串按顺序排列的方法参数类型。
2. 接口两端是否对自定义类型完成了相同的 D-Bus 注册与编解码定义。

`QDBusSignature` 只保留 signature 的线路类型，并不会自动让任意 C++ 自定义结构可传输。

## 验证与协议边界

典型 signature 只使用 D-Bus 类型代码与容器组合规则。接口 XML、服务端实现和客户端生成代码应是签名的主要来源；不要让外部输入直接决定要调用的方法签名或要解析的嵌套结构。

同样，包装成 `QDBusSignature` 不意味着内容一定符合业务协议。即使语法正确，服务端也可能不支持该类型组合；调用方仍应处理 `QDBusError::InvalidSignature` 等失败。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QDBusSignature()` | 创建空的 signature 包装值。 | 空签名不代表某个实际参数类型；只在协议允许空类型序列时使用。 |
| 构造 | `QDBusSignature(const QString &signature)` | 从 Qt 字符串构造 signature。 | 应传入接口约定的 D-Bus 类型编码，而非 C++ 类型名称。 |
| 构造 | `QDBusSignature(QLatin1StringView signature)` | 从 Latin-1 字符串视图构造 signature。 | 适合固定 ASCII signature 常量，例如 `"a{sv}"`。 |
| 构造 | `QDBusSignature(const char *signature)` | 从 C 字符串构造 signature。 | 字符串应以空字符结尾，通常用于编译期常量。 |
| 签名访问 | `signature()` | 返回保存的 signature 文本。 | 返回文本不自动验证远端是否接受它。 |
| 签名访问 | `setSignature(const QString &signature)` | 替换保存的 signature 文本。 | 改值后要由调用方保证接口契约与类型组合仍匹配。 |
| 生命周期 | `swap(QDBusSignature &other)` | 快速交换两个 signature 值。 | `noexcept`；只交换内容，不解析或校验。 |

## 最容易踩的坑

- 用 `QString` 传签名：发送的是 `STRING`，不是 D-Bus `SIGNATURE`。
- 将 `"a{sv}"` 当作一个普通类型名：它是 D-Bus 容器和元素类型的编码。
- 以为包装器会自动注册自定义 C++ 类型：自定义类型仍需正确的 D-Bus 编解码支持。
- 让不可信输入自由决定 signature：可能导致协议错误、资源消耗和难以维护的动态路径。
- 看见 `InvalidSignature` 只改客户端：接口 XML、服务端元对象信息和自定义类型注册都可能不一致。
