# QDBusInterface
> Qt 6.11.1 · Qt D-Bus · 来自 `QDBusInterface`

## 作用定位

`QDBusInterface` 是 Qt D-Bus 的动态远端接口代理。给它 service、object path、interface 和 connection，它就能用继承自 `QDBusAbstractInterface` 的 `call()`、`asyncCall()` 等函数调用远端方法。

它适合没有生成专用代理类、接口数量少、调用较简单的场景。接口复杂、需要编译期类型检查时，更推荐用 XML introspection 配合 `qdbusxml2cpp` 生成强类型代理。

## 类说明

- 头文件：`#include <QDBusInterface>`
- CMake：链接 `Qt6::DBus`
- 继承：`QDBusAbstractInterface`
- 对象规则：QObject 派生类，受 parent 和线程归属约束

## API 速查

| API | 说明 |
| --- | --- |
| `QDBusInterface(service, path, interface, connection, parent)` | 创建动态代理；`interface` 为空时会尝试合并对象内省到的接口。 |
| `~QDBusInterface()` | 销毁代理对象，释放缓存和 QObject 资源。 |
| 继承的 `call()` | 同步调用远端方法。 |
| 继承的 `asyncCall()` | 异步调用远端方法。 |
| 继承的 `isValid()` | 检查代理创建是否成功。 |
| 继承的 `lastError()` | 获取创建或调用时的错误。 |

## 典型用法

```cpp
QDBusInterface iface("org.example.Service",
                     "/org/example/Object",
                     "org.example.Interface",
                     QDBusConnection::sessionBus());

if (!iface.isValid()) {
    qWarning() << iface.lastError().name();
    return;
}

QDBusReply<QString> reply = iface.call("Version");
if (reply.isValid())
    qDebug() << reply.value();
```

## 使用场景

- 快速调用一个已知 D-Bus 服务的方法。
- 调试、工具程序或插件中运行期才知道接口名。
- 项目还没有引入 XML 生成代理，但需要先接入服务。

## 常见坑与经验

- `interface` 为空会依赖内省并合并接口，遇到多个接口有同名方法时会让行为不清晰；生产代码尽量填完整接口名。
- `isValid()` 不等于远端服务之后一直在线，调用仍可能失败。
- 动态代理没有编译期方法名和参数检查，字符串拼错只会在运行时变成 `UnknownMethod` 或 `InvalidArgs`。
- 高频调用建议缓存 `QDBusInterface`，避免重复内省和构造。
- GUI 线程调用远端慢方法时，优先使用 `asyncCall()`。

## 知识点覆盖

- 动态 D-Bus 代理
- service/path/interface 三元定位
- 内省与接口缓存
- 同步与异步调用继承关系
- 动态代理和生成代理的取舍
