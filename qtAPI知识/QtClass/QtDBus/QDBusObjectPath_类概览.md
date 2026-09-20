# QDBusObjectPath：在 QVariant 中保留 D-Bus OBJECT_PATH 类型

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDBusObjectPath>`  
> 模块：`Qt6::DBus`  
> 相关类：`QDBusConnection`、`QDBusMessage`、`QDBusSignature`

## 它解决什么问题

D-Bus 的 object path 看起来像字符串，例如 `/org/example/Player/1`，但在线路协议里它的类型是 `OBJECT_PATH`，不是普通 `STRING`。

`QDBusObjectPath` 是这个类型的 Qt 值包装器。它让值在装进 `QVariant`、消息参数或容器时保留“这是对象路径”的类型信息，而不是被当作普通文本发送。

```text
QString("/org/example/Player/1")
  -> D-Bus STRING

QDBusObjectPath("/org/example/Player/1")
  -> D-Bus OBJECT_PATH
```

它只表达“对象路径”这一段定位信息。访问远程对象通常还需要 service、object path、interface 三者；不要把 object path 当成 URL，也不能脱离服务名唯一定位跨进程对象。

## 适用场景

- D-Bus 方法的参数或返回值规定为 `OBJECT_PATH`。
- 将对象路径放入 `QVariant`、`QDBusMessage`、`QDBusArgument` 或容器后发送。
- 从远程返回值中显式区分路径类型与普通字符串。

不适合：

- 仅用于显示路径文字，普通 `QString` 更直接。
- 把任意本地文件路径、URL 或 Windows 路径包装后发送。

## 最小示例

```cpp
#include <QDBusMessage>
#include <QDBusObjectPath>

const QDBusObjectPath jobPath("/org/example/Jobs/42");

QDBusMessage message = QDBusMessage::createMethodCall(
    "org.example.JobService",
    "/org/example/Manager",
    "org.example.Manager",
    "OpenJob");

message << QVariant::fromValue(jobPath);
```

此处改成直接传 `QString` 会改变 D-Bus 签名，远端若要求 `o`（object path）而收到 `s`（string），调用会因类型不匹配而失败。

## 路径格式与验证边界

有效 D-Bus object path 以 `/` 开头；路径元素由 `/` 分隔，通常使用 ASCII 字母、数字和下划线。根路径 `/` 合法，空元素和随意的文件系统样式通常不合法。

`QDBusObjectPath` 的职责是标记类型和保存值，不应把它当作完整的业务校验器。应用仍应根据接口约定检查路径是否属于允许命名空间，例如只接受 `/org/example/Jobs/` 前缀，而不是任何格式上合法的 object path。

## 与 `QVariant` 的关系

该类可隐式转换成 `QVariant`，等价于 `QVariant::fromValue(path)`。隐式转换写起来简洁，但在重载或容器初始化中可能让类型意图不够明显；跨 D-Bus 边界时，显式写 `QVariant::fromValue()` 常更容易阅读和调试。

从 `QVariant` 取回时应使用匹配的类型：

```cpp
const QDBusObjectPath path =
    variant.value<QDBusObjectPath>();
```

不要直接 `toString()` 后就假设输入原本是 OBJECT_PATH；那会丢掉协议类型检查带来的信息。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QDBusObjectPath()` | 创建空的对象路径包装值。 | 空值通常不能满足需要有效 object path 的远程接口。 |
| 构造 | `QDBusObjectPath(const QString &path)` | 从 Qt 字符串构造对象路径。 | 传入值应符合 D-Bus object path 语法和业务命名空间。 |
| 构造 | `QDBusObjectPath(QLatin1StringView path)` | 从 Latin-1 字符串视图构造路径。 | 适合固定 ASCII 路径常量；视图仅用于构造时读取。 |
| 构造 | `QDBusObjectPath(const char *path)` | 从 C 字符串构造路径。 | 仅传入以空字符结尾且编码明确的字符串常量。 |
| 路径访问 | `path()` | 返回保存的对象路径字符串。 | 返回值是内容，不代表目标服务或对象当前存在。 |
| 路径访问 | `setPath(const QString &path)` | 替换保存的对象路径。 | 修改后仍需由调用方保证语法和业务约束正确。 |
| 类型转换 | `operator QVariant()` | 隐式转换为携带 `QDBusObjectPath` 元类型的 `QVariant`。 | 可读性优先时显式使用 `QVariant::fromValue()`。 |
| 生命周期 | `swap(QDBusObjectPath &other)` | 快速交换两个路径值。 | `noexcept`；适合值对象重排，不校验内容。 |
| 相关非成员 | `swap(QDBusObjectPath &first, QDBusObjectPath &second)` | 调用成员 `swap()` 的自由函数。 | 供泛型算法通过 ADL 使用。 |
| 调试输出 | `operator<<(QDebug, const QDBusObjectPath &path)` | 将路径输出到 `QDebug`。 | Qt 6.8 引入；日志中仍需注意是否包含敏感对象标识。 |

## 最容易踩的坑

- 用 `QString` 代替 `QDBusObjectPath`：在线路上会变成 `STRING`，不是 `OBJECT_PATH`。
- 把 object path 当作完整远程地址：还需要 service 和 interface 才能定位调用目标。
- 将本地文件路径封装进去：文件路径规则与 D-Bus object path 规则无关。
- 只判断字符串前缀而不遵守接口约定：路径类型合法不代表业务对象存在或允许访问。
- 从 `QVariant` 调 `toString()` 后丢掉类型意图：优先按 `QDBusObjectPath` 元类型读取。
