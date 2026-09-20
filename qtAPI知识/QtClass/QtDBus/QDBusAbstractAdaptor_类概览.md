# QDBusAbstractAdaptor：把本地 QObject 包装成 D-Bus 服务接口

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDBusAbstractAdaptor>`  
> 模块：`Qt6::DBus`  
> 继承：`QObject`  
> 相关类：`QDBusConnection`、`QDBusContext`、`QDBusInterface`

## 它解决什么问题

业务对象通常是一个普通 `QObject`：它有本地方法、信号、属性和内部状态。把整个对象原样注册到 D-Bus，往往会意外暴露不该公开的成员，也难以稳定地定义远程接口名称。

`QDBusAbstractAdaptor` 就是服务端的“接口门面”。它附着在真实业务对象上，只暴露该 D-Bus 接口需要的方法、属性和信号，再由 `QDBusConnection::registerObject()` 将真实对象注册到总线。

```text
真实业务对象（QObject）
  <- 父对象 -
QDBusAbstractAdaptor 派生类
  -> 一个明确的 D-Bus interface
  -> registerObject() 后对远程客户端可见
```

一个真实对象可以挂多个 adaptor，从而在同一个 D-Bus object path 下实现多个接口。每个 adaptor 类应只声明一个 D-Bus 接口。

## 适用场景

- 服务端需要将现有业务对象的一小部分能力暴露给其他进程。
- 需要将私有实现与稳定的 D-Bus ABI 分开维护。
- 一个对象实现多个 D-Bus interface，例如控制接口、诊断接口和属性接口。

不适合：

- 作为客户端调用远程服务的对象，客户端应使用 `QDBusInterface` 或生成的接口类。
- 临时在栈上创建的包装对象，adaptor 必须由真实对象拥有。

## 最小服务端示例

```cpp
#include <QDBusAbstractAdaptor>
#include <QDBusConnection>
#include <QObject>

class Player : public QObject
{
    Q_OBJECT
public slots:
    void play() { /* 实际播放逻辑 */ }
signals:
    void stateChanged(const QString &state);
};

class PlayerAdaptor : public QDBusAbstractAdaptor
{
    Q_OBJECT
    Q_CLASSINFO("D-Bus Interface", "org.example.Player")
public:
    explicit PlayerAdaptor(Player *player)
        : QDBusAbstractAdaptor(player)
    {
        setAutoRelaySignals(true);
    }

public slots:
    void Play()
    {
        qobject_cast<Player *>(parent())->play();
    }

signals:
    void stateChanged(const QString &state);
};

auto *player = new Player;
new PlayerAdaptor(player); // 堆上创建，由 player 自动销毁

QDBusConnection::sessionBus().registerObject(
    "/Player", player, QDBusConnection::ExportAdaptors);
```

关键点不在 `new` 这一个动作，而在父子关系：构造基类时传入真实对象，使它成为 adaptor 的 QObject 父对象。真实对象销毁时，adaptor 会自动销毁；调用方不应手动 `delete` adaptor。

## QObject 成员如何成为 D-Bus 成员

adaptor 使用 Qt 元对象系统识别自身的 signals、slots、`Q_INVOKABLE` 方法和属性。`Q_CLASSINFO("D-Bus Interface", "...")` 声明接口名，注册对象时配合 `ExportAdaptors` 导出。

这意味着 adaptor 是 API 边界，不应只是把真实对象的所有成员机械转发出去。应在此处处理：

- 远程方法名与参数类型的稳定性。
- 本地复杂类型能否转换成 D-Bus 类型。
- 权限与调用者身份检查。
- 同步调用是否可能阻塞服务端线程。

## 自动转发信号的真实含义

调用 `setAutoRelaySignals(true)` 后，Qt 会把真实对象和 adaptor 中**方法签名完全相同**的信号做 signal-to-signal 连接。它不是按信号名字模糊匹配，也不会转换参数。

自动转发适合 adaptor 只是镜像业务信号的情况；若要更改信号名、过滤状态、组合多个本地信号或做权限判断，应关闭自动转发，并自己连接到 adaptor 的导出信号。

## `Q_NOREPLY` 不能让带返回值的方法变成异步

在 adaptor 的方法声明前写 `Q_NOREPLY`，表示该 D-Bus 方法不等待处理完成就返回给调用方：

```cpp
Q_NOREPLY void RefreshCache();
```

被标记的方法必须返回 `void`，也不能输出参数；任何输出都会被丢弃。它适合“通知式命令”，不适合客户端必须知道结果、错误或新状态的操作。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 受保护构造 | `QDBusAbstractAdaptor(QObject *obj)` | 将 adaptor 附着到真实业务对象，并把它设为 QObject 父对象。 | 派生类在初始化列表中传入真实对象；不要传短生命周期对象。 |
| 生命周期 | `~QDBusAbstractAdaptor()` | 销毁 adaptor。 | 正常由父对象自动销毁，调用方不应手动 `delete`。 |
| 信号转发 | `autoRelaySignals()` | 返回是否启用了从真实对象到 adaptor 的自动信号转发。 | 只反映当前设置，不保证两个类已经拥有同签名信号。 |
| 信号转发 | `setAutoRelaySignals(bool enable)` | 开启或关闭真实对象到 adaptor 的自动 signal-to-signal 转发。 | 仅转发签名完全一致的信号；复杂映射应手动连接。 |
| 宏 | `Q_NOREPLY` | 将 adaptor 方法标记为不等待回复的 D-Bus 方法。 | 方法必须为 `void` 且没有输出参数；调用方无法获得结果或错误。 |

## 最容易踩的坑

- 在栈上创建 adaptor：它应堆分配并交给真实对象的父子生命周期管理。
- 直接注册业务对象的全部成员：用 adaptor 明确远程边界。
- 忘记 `Q_CLASSINFO("D-Bus Interface", ...)`：接口元数据不完整，客户端难以稳定调用。
- 开启自动转发却只让信号名字相同：参数或返回类型签名不完全一致时不会转发。
- 用 `Q_NOREPLY` 标记需要结果的方法：远程调用者得到不到返回值和错误。
