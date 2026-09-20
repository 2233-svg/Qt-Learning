# QDBusVariant：表达 D-Bus 中“带类型的值”

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDBusVariant>`  
> 模块：`Qt6::DBus`  
> 相关类：`QVariant`、`QDBusArgument`、`QDBusSignature`

## 它解决什么问题

`QVariant` 是 Qt 的通用动态值容器；D-Bus 也有一个名为 `VARIANT` 的协议类型，用于在消息中嵌套“值加上它自己的 D-Bus 类型签名”。

名字相近，但它们不在同一层：

```text
QVariant(42)
  -> 一个普通 D-Bus INT32 参数

QVariant::fromValue(QDBusVariant(42))
  -> 一个 D-Bus VARIANT 参数，内部装着 INT32
```

`QDBusVariant` 就是把 Qt 的 `QVariant` 显式包一层，使 Qt D-Bus 在序列化时发送协议类型 `v`（VARIANT），而不是直接发送内部值的类型。

## 适用场景

- 远程接口参数、返回值或属性的 D-Bus 签名明确要求 `v`。
- 传递像 `a{sv}` 这类“字符串键到 variant 值”的扩展属性字典。
- 编写动态 D-Bus 客户端、属性服务或元数据工具。

不适合：

- 接口参数本身已经是具体类型，例如整数、字符串、对象路径。
- 仅为了“能装任何东西”而多包一层；错误的 variant 嵌套会改变接口签名。

## 最小示例

假设远端方法签名是 `i v s`，即整数、D-Bus variant、字符串：

```cpp
#include <QDBusMessage>
#include <QDBusVariant>

QList<QVariant> arguments;
arguments << QVariant(42)
          << QVariant::fromValue(QDBusVariant(QStringLiteral("dynamic")))
          << QVariant(QStringLiteral("tail"));

message.setArguments(arguments);
```

中间参数若写成 `QVariant(QStringLiteral("dynamic"))`，它会成为普通 D-Bus STRING，而不是 D-Bus VARIANT。

## 嵌套层次要看接口签名

一个 `QDBusVariant` 内部仍然存放 `QVariant`，因此可能出现两层甚至更多层的动态容器。是否正确不取决于“看起来能否转换”，而取决于远端接口签名：

- 期待具体类型 `s`：传 `QString`。
- 期待 variant `v`：传 `QDBusVariant(QString)` 并装入外层 `QVariant`。
- 期待字典 `a{sv}`：字典的每个 value 往往是 `QDBusVariant`。

从消息中读取时也要按相同层次拆包：

```cpp
const QDBusVariant dbusValue =
    reply.arguments().at(0).value<QDBusVariant>();
const QVariant actualValue = dbusValue.variant();
```

不要直接把外层 `QVariant` 当成内部具体类型，否则类型转换可能失败或丢失协议层的 variant 意图。

## 自定义类型并不会因此自动可传输

`QDBusVariant` 只能保留“这是一个 D-Bus variant”的容器语义。内部 `QVariant` 所装的自定义类型，仍必须具备 Qt 元类型信息，并按 Qt D-Bus 类型系统提供正确的编解码支持。它不是自定义类型注册的替代方案。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QDBusVariant()` | 创建内部为空的 D-Bus variant 包装值。 | 空内部值是否允许由远端接口决定。 |
| 构造 | `QDBusVariant(const QVariant &variant)` | 用一个 Qt 动态值构造 D-Bus VARIANT。 | 将对象再装入 `QVariant::fromValue()` 后才能作为消息参数保持 `v` 类型。 |
| 值访问 | `variant()` | 取出内部保存的 Qt `QVariant`。 | 返回的是内部值副本；读取时按接口签名转换为具体类型。 |
| 值访问 | `setVariant(const QVariant &variant)` | 替换内部保存的动态值。 | 更改内部类型会改变嵌套的 D-Bus 签名，应符合远端接口约定。 |
| 生命周期 | `swap(QDBusVariant &other)` | 快速交换两个 D-Bus variant 的内部值。 | `noexcept`；只交换包装内容，不校验可序列化性。 |

## 最容易踩的坑

- 把 `QVariant` 当成 D-Bus `VARIANT`：没有 `QDBusVariant` 包装时，发送的是内部具体类型。
- 多包或少包一层：接口签名会从 `v` 变成具体类型，或反过来。
- 从外层 `QVariant` 直接 `toString()`：先取 `QDBusVariant`，再取内部 `variant()`。
- 把它当作自定义类型注册工具：内部类型仍需正确注册和 D-Bus 编解码。
- 只因数据动态就使用它：是否使用由 D-Bus 接口签名决定，而不是由 C++ 变量是否为 `QVariant` 决定。
