# QDBusVirtualObject
> Qt 6.11.1 · Qt D-Bus · 来自 `QDBusVirtualObject`

## 作用定位

`QDBusVirtualObject` 是高级服务端扩展点：它允许你不把每个 D-Bus 对象都做成真实 QObject，而是用一个虚拟对象统一处理消息和内省。适合对象树很大、对象数量动态变化、接口完全由数据驱动生成的服务。

普通服务端优先用 `QObject` + `QDBusAbstractAdaptor`；只有当真实 QObject 模型太重或不适合动态对象树时，再考虑虚拟对象。

## 类说明

- 头文件：`#include <QDBusVirtualObject>`
- CMake：链接 `Qt6::DBus`
- 继承：`QObject`
- 必须实现：`handleMessage()`、`introspect()`
- 注册方式：配合 `QDBusConnection::registerVirtualObject()` 相关机制使用

## API 速查

| API | 说明 |
| --- | --- |
| `QDBusVirtualObject(parent)` | 创建虚拟对象基类。 |
| `~QDBusVirtualObject()` | 释放虚拟对象资源。 |
| `handleMessage(message, connection)` | 处理到达虚拟对象路径的调用消息；返回是否已处理。 |
| `introspect(path)` | 返回指定虚拟路径的 XML introspection 描述。 |

## 典型设计

```cpp
class DeviceTreeObject : public QDBusVirtualObject
{
public:
    bool handleMessage(const QDBusMessage &message,
                       const QDBusConnection &connection) override
    {
        if (message.member() == "Read") {
            connection.send(message.createReply(readDevice(message.path())));
            return true;
        }
        connection.send(message.createErrorReply(QDBusError::UnknownMethod,
                                                 "Unknown virtual method"));
        return true;
    }

    QString introspect(const QString &path) const override
    {
        return makeIntrospectionXmlFor(path);
    }
};
```

## 使用场景

- 动态设备树、会话树、文档树等大量对象路径。
- 对象接口来自配置或运行期数据，而不是固定 C++ 类。
- 想自己控制内省 XML、方法分派和错误处理。
- 桥接已有 IPC/对象模型到 D-Bus，不想为每个节点创建 QObject。

## 常见坑与经验

- `introspect()` 返回的 XML 必须与 `handleMessage()` 实际支持的方法一致，否则客户端会按错误契约调用。
- `handleMessage()` 要负责正常回复和错误回复；没有回复会让调用者超时。
- 虚拟对象绕开了 QObject 元对象自动导出，灵活性更高，安全审计责任也更重。
- 如果对象数量不大，adaptor 更简单、更不容易写错。
- 返回 false 通常意味着消息未被处理，调用者最终可能得到 unknown method/object 一类错误。

## 知识点覆盖

- 虚拟 D-Bus 对象树
- 手写消息分派
- XML introspection 生成
- 大规模动态对象导出
- adaptor 模式与 virtual object 模式取舍
