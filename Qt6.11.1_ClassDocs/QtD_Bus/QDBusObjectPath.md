# QDBusObjectPath
> Qt 6.11.1 · Qt D-Bus · 来自 `QDBusObjectPath`

## 作用定位

`QDBusObjectPath` 是 D-Bus 对象路径的类型包装。对象路径不是普通字符串；它是远端对象树中的地址，例如 `/org/freedesktop/DBus`。用专门类型能让 Qt D-Bus 生成正确签名 `o`，也能让接口声明更准确。

## 类说明

- 头文件：`#include <QDBusObjectPath>`
- CMake：链接 `Qt6::DBus`
- 继承：无公开 QObject 继承
- Qt 6.8 起支持 `QDebug << QDBusObjectPath`

## API 速查

| API | 说明 |
| --- | --- |
| `QDBusObjectPath()` | 创建空路径对象。 |
| `QDBusObjectPath(QLatin1StringView)` | 从 Latin-1 字符串构造路径。 |
| `QDBusObjectPath(const QString &)` | 从 `QString` 构造路径。 |
| `QDBusObjectPath(const char *)` | 从 C 字符串构造路径。 |
| `path()` | 返回路径字符串。 |
| `setPath()` | 修改路径。 |
| `operator QVariant()` | 作为 QVariant 传入 D-Bus 参数。 |
| `swap()` | 快速交换路径对象。 |
| `operator<<(QDebug, path)` | 调试输出路径。 |

## 使用场景

- 远端方法返回对象路径，下一步要对该对象再创建 `QDBusInterface`。
- 方法参数签名明确要求 object path，而不是普通 string。
- 导出或管理树状对象模型，例如 `/org/example/Device/0`。

## 常见坑与经验

- D-Bus 对象路径通常以 `/` 开头，路径段不要使用任意文件系统字符；它不是文件路径。
- `QString` 发送出去会生成字符串签名 `s`，`QDBusObjectPath` 才是对象路径签名 `o`。
- 对象路径只是地址，不代表对象一定存在；调用前仍可能得到 `UnknownObject`。
- 如果使用 `ExportChildObjects`，子对象的 `objectName()` 会参与路径生成，命名要稳定。

## 知识点覆盖

- D-Bus object path 类型签名 `o`
- 对象树寻址模型
- 对象路径与服务名、接口名的区别
- QVariant 包装特殊 D-Bus 类型
