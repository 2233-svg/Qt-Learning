# Qt QDBusVirtualObject 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDBusVirtualObject>`  
> 所属模块：`Qt6::DBus`  
> 继承：`QObject`  
> 类型特征：不可拷贝的抽象基类

## 1. 它解决什么问题

普通的 D-Bus 导出方式是：为每个对象创建一个 `QObject`，再把它注册到一个 D-Bus object path。对象路径数量少时，这种方式最清晰。

当路径数量很大、路径动态生成，或你想由一套路由逻辑统一处理整个路径子树时，为每个路径构造 QObject 会变得笨重。`QDBusVirtualObject` 允许**一个 QObject 处理多个 D-Bus 路径**。

```text
/org/example/items/1
/org/example/items/2
/org/example/items/3
          │
          ▼
  一个 QDBusVirtualObject 派生对象统一处理
```

它把 Qt 自动导出 QObject 元对象系统的工作交给实现者：你必须自己处理每条消息，并自行返回用于 D-Bus introspection 的 XML。

适用场景包括设备树、对象数量极多的资源服务、运行时生成路径的代理服务。若只导出少量固定接口，普通 `registerObject()` 往往更易维护。

## 2. 构建与注册方式

```cmake
find_package(Qt6 REQUIRED COMPONENTS DBus)
target_link_libraries(mytarget PRIVATE Qt6::DBus)
```

派生类实例不能单独生效，需要注册到连接：

```cpp
auto *tree = new ItemTree(this);

const bool ok = QDBusConnection::sessionBus().registerVirtualObject(
    "/org/example/items",
    tree,
    QDBusConnection::SubPath);
Q_ASSERT(ok);
```

传入 `QDBusConnection::SubPath` 时，`tree` 将接收根路径及其所有子路径的消息。这正是 virtual object 的核心价值，也意味着实现需要完整处理子树。

## 3. 最小实现骨架

```cpp
#include <QDBusConnection>
#include <QDBusMessage>
#include <QDBusVirtualObject>

class ItemTree final : public QDBusVirtualObject
{
public:
    using QDBusVirtualObject::QDBusVirtualObject;

    QString introspect(const QString &path) const override
    {
        if (path == "/org/example/items")
            return "<node><node name=\"1\"/></node>";

        return "<node/>";
    }

    bool handleMessage(const QDBusMessage &message,
                       const QDBusConnection &connection) override
    {
        if (message.member() != "Name")
            return false;

        connection.send(message.createReply(QStringLiteral("item")));
        return true;
    }
};
```

骨架只展示职责分界。真实实现还需要检查 `message.type()`、`path()`、`interface()`、`member()`、参数类型和调用者权限，并为无效请求选择合适的 D-Bus 错误回复。

## 4. `handleMessage()`：你是消息路由器

当 virtual object 注册时使用 `SubPath`，该函数必须处理属于该路径子树的**所有**消息。消息携带 service、path、interface、method 和参数；`connection` 是发送回复的连接句柄。

返回值有严格含义：

- 返回 `true`：表示消息已经处理。对于方法调用，通常意味着你已发送回复或错误，或者该方法协议允许无回复。
- 返回 `false`：Qt 将生成 D-Bus 错误回复。

因此，不能在“已发送正常回复”后再返回 `false`，也不能对未知调用随手返回 `true` 却不回复。前者可能产生重复或混乱的响应，后者会让调用端等待到超时。

建议的路由顺序：

1. 确认消息类型和 path 是否在负责范围内。
2. 根据 interface 与 member 找到处理器。
3. 校验参数个数和 D-Bus 类型。
4. 执行业务逻辑和权限检查。
5. 通过 `connection` 发送正常回复或明确错误。
6. 只有完全处理后才返回 `true`。

## 5. `introspect()`：动态对象树的协议声明

D-Bus 客户端会通过 Introspect 方法询问路径上有哪些接口、方法、信号、属性和子节点。普通 QObject 注册时 Qt 可从元对象自动生成这些信息；virtual object 则必须由 `introspect(path)` 返回 XML。

返回值是 `<node>` 形式的 D-Bus introspection XML，例如：

```xml
<node>
  <interface name="org.example.Item">
    <method name="Name">
      <arg name="value" type="s" direction="out"/>
    </method>
  </interface>
  <node name="1"/>
</node>
```

若注册时使用 `SubPath`，返回 XML 还必须包含子节点；否则 Qt 只能知道根对象，客户端无法发现动态树中的后代路径。

XML 与 `handleMessage()` 必须同步维护：XML 声称存在的方法，handler 必须能处理；handler 允许的方法，也应被 XML 描述。两者不一致会让工具、自动生成代理与实际运行行为脱节。

## 6. 普通 QObject 导出与 virtual object 的选择

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 固定对象导出 | `QDBusConnection::registerObject()` | 将一个 QObject 的元对象导出到固定路径。 | Qt 自动处理大量 introspection 与调用分派，优先用于少量稳定对象。 |
| 动态树导出 | `registerVirtualObject()` | 将一个 virtual object 注册为一个路径或子树的处理器。 | 需要自行实现消息分派、回复和 introspection XML。 |

不要仅为“看起来更高级”而使用 virtual object；它给了更高的扩展性，也把更大的协议正确性责任交给你的代码。

## 7. 常见误区

### 7.1 误区：`handleMessage()` 只会收到注册根路径

使用 `SubPath` 时会收到整个子树的消息。必须按 `message.path()` 路由每个动态对象。

### 7.2 误区：返回 `true` 只表示“我看到了消息”

不是。它表示消息已经被处理。方法调用通常还必须已经产生可用回复或明确按无回复规则处理。

### 7.3 误区：Introspection XML 只是给开发工具看的

不是。它是 D-Bus 协议发现机制的一部分，影响客户端浏览对象树、生成代理和调用接口。

### 7.4 误区：可以直接实例化或复制本类

不能。它有两个纯虚函数且禁用复制；必须定义派生类并通过 QObject parent 管理生命周期。

## 8. 逐项 API 说明

### 生命周期

#### `explicit QDBusVirtualObject(QObject *parent = nullptr)`

构造派生对象的基类部分，并可设置 QObject 父对象。它本身抽象，不能直接实例化。

#### `virtual ~QDBusVirtualObject()`

销毁 virtual object 及其 QObject 子对象。注册关系应与连接和对象生命周期一起设计，避免连接仍在使用已销毁对象。

### 必须重写的接口

#### `QString introspect(const QString &path) const`

返回指定 path 的 introspection XML。若使用 `SubPath`，XML 中应包含可发现的子节点；接口、方法、信号和属性声明要与实际 handler 保持一致。

#### `bool handleMessage(const QDBusMessage &message, const QDBusConnection &connection)`

处理发往负责路径的 D-Bus 消息。成功完整处理返回 `true`；不能处理返回 `false`，让 Qt 生成错误回复。实现中负责协议校验、权限、业务调用及发送回复。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QDBusVirtualObject(QObject *parent)` | 初始化派生 virtual object 的 QObject 基类部分。 | 本类抽象且不可复制，必须在派生类中使用。 |
| 析构 | `~QDBusVirtualObject()` | 销毁对象及其 QObject 子对象。 | 规划好连接注册与对象生命周期，避免悬空注册。 |
| 纯虚函数 | `QString introspect(const QString &path) const` | 返回 path 对应的 D-Bus introspection XML。 | `SubPath` 注册时必须描述子节点；XML 必须和真实处理逻辑同步。 |
| 纯虚函数 | `bool handleMessage(const QDBusMessage &message, const QDBusConnection &connection)` | 分派并处理收到的 D-Bus 消息。 | 处理完才返回 `true`；返回 `false` 会由 Qt 产生错误回复。 |

---

### 一句话总结

`QDBusVirtualObject` 用一个对象处理动态 D-Bus 路径树；它的自由度很高，但消息路由、回复、权限和 introspection XML 都必须由派生类严格维护。
