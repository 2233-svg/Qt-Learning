# Qt D-Bus：总线、服务、接口与异步调用

> Qt D-Bus 将进程间通信映射为 QObject 风格的接口、方法、属性和信号。理解总线类型、对象路径、接口名和异步回调四个标识，是使用 Qt D-Bus 的基础。

## 1. 模块与连接

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core DBus)
target_link_libraries(mytarget PRIVATE Qt6::Core Qt6::DBus)
```

```cpp
#include <QDBusConnection>

QDBusConnection bus = QDBusConnection::sessionBus();
if (!bus.isConnected()) {
    qWarning() << bus.lastError().message();
    return;
}
```

常见总线：`sessionBus()` 面向当前用户会话，`systemBus()` 面向系统服务。连接状态受平台 D-Bus 守护进程影响，Windows 上通常需要额外运行环境或改用其他 IPC。

## 2. D-Bus 名称体系

一次调用通常涉及：服务名、对象路径、接口名和方法/信号名。这些字符串是协议的一部分，应集中定义并保持稳定。对象路径使用 `/` 分隔，服务和接口使用点号分隔，不能混用。

## 3. 注册服务对象

```cpp
class Manager : public QObject
{
    Q_OBJECT
public slots:
    QString status() const { return QStringLiteral("ready"); }
signals:
    void statusChanged(const QString &status);
};

Manager manager;
QDBusConnection bus = QDBusConnection::sessionBus();
bus.registerService(QStringLiteral("org.example.Manager"));
bus.registerObject(QStringLiteral("/org/example/Manager"), &manager,
                   QDBusConnection::ExportAllSlots | QDBusConnection::ExportAllSignals);
```

注册失败时检查服务名是否已被占用以及对象路径是否有效。需要提前切换时显式调用 `unregisterObject()`。

## 4. QDBusAbstractAdaptor

```cpp
class ManagerAdaptor : public QDBusAbstractAdaptor
{
    Q_OBJECT
    Q_CLASSINFO("D-Bus Interface", "org.example.Manager")
public:
    explicit ManagerAdaptor(Manager *parent) : QDBusAbstractAdaptor(parent) {}

public slots:
    QString status() const { return qobject_cast<Manager *>(parent())->status(); }
};
```

Adaptor 让一个 QObject 以明确 D-Bus 接口导出，通常由 `new` 创建并以真实对象为父对象，不由调用者手动删除。它适合把协议层接口与业务对象分离。

## 5. QDBusInterface：调用远程方法

```cpp
QDBusInterface iface(QStringLiteral("org.example.Manager"),
                     QStringLiteral("/org/example/Manager"),
                     QStringLiteral("org.example.Manager"),
                     QDBusConnection::sessionBus());

QDBusReply<QString> reply = iface.call(QStringLiteral("status"));
if (!reply.isValid())
    qWarning() << reply.error().name() << reply.error().message();
else
    qDebug() << reply.value();
```

同步 `call()` 会阻塞当前线程，不能在 GUI 线程调用不受控的远程服务。参数和返回值必须是 D-Bus 支持或已注册的元类型。

## 6. 异步调用

```cpp
QDBusPendingCall pending = iface.asyncCall(QStringLiteral("status"));
auto *watcher = new QDBusPendingCallWatcher(pending, this);
connect(watcher, &QDBusPendingCallWatcher::finished,
        this, [watcher] {
    QDBusPendingReply<QString> reply = *watcher;
    if (reply.isError())
        qWarning() << reply.error().message();
    else
        qDebug() << reply.value();
    watcher->deleteLater();
});
```

异步调用不会阻塞事件循环，但仍需处理服务消失、超时和对象销毁。watcher 设为请求控制器的子对象，页面关闭时即可统一清理。

## 7. 发送和接收信号

```cpp
bus.connect(QStringLiteral("org.example.Manager"),
            QStringLiteral("/org/example/Manager"),
            QStringLiteral("org.example.Manager"),
            QStringLiteral("statusChanged"),
            this,
            SLOT(onStatusChanged(QString)));
```

连接信号前确认接口签名和参数类型。也可以用 `QDBusMessage::createSignal()` 发送自定义信号，但必须遵循固定接口名称。

## 8. 服务发现与 QDBusServiceWatcher

```cpp
QDBusServiceWatcher watcher(QStringLiteral("org.example.Manager"),
                            QDBusConnection::sessionBus(),
                            QDBusServiceWatcher::WatchForRegistration |
                            QDBusServiceWatcher::WatchForUnregistration,
                            this);
connect(&watcher, &QDBusServiceWatcher::serviceRegistered,
        this, &Client::serviceAvailable);
connect(&watcher, &QDBusServiceWatcher::serviceUnregistered,
        this, &Client::serviceUnavailable);
```

服务名注册不等于对象接口已经准备完成，客户端仍应调用探测方法或检查 introspection 结果。

## 9. QDBusMessage 与超时

```cpp
QDBusMessage message = QDBusMessage::createMethodCall(
    QStringLiteral("org.example.Manager"),
    QStringLiteral("/org/example/Manager"),
    QStringLiteral("org.example.Manager"),
    QStringLiteral("setEnabled"));
message << true;
QDBusMessage reply = bus.call(message, QDBus::Block, 2000);
if (reply.type() == QDBusMessage::ErrorMessage)
    qWarning() << reply.errorName() << reply.errorMessage();
```

Qt 6 中固定参数数量的旧式重载已移除，应使用参数列表或模板接口。超时值要有上限，避免远程服务失联时永久阻塞。

## 10. 自定义类型、安全与权限

复杂结构需要 `Q_DECLARE_METATYPE`、`qDBusRegisterMetaType` 以及流运算符，才能在 D-Bus 中序列化。服务应限制可调用方法和发送者，不要把文件操作或高权限动作无条件导出；所有输入都要验证长度、路径和权限。

## 11. 常见问题

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| registerService 失败 | 名称已被占用或总线不可用 | 检查连接和服务生命周期 |
| call 阻塞界面 | 使用同步调用 | 改用 asyncCall + watcher |
| 方法找不到 | 接口名/对象路径/大小写错误 | 与服务端协议逐项核对 |
| 参数类型错误 | 未注册自定义类型或签名不一致 | 注册元类型并固定协议 |
| 服务消失后崩溃 | 异步回调访问已销毁对象 | watcher 设 parent 并检查上下文 |
| 信号收不到 | 总线或 match 规则错误 | 检查 bus、路径、接口和信号名 |

## 12. 自测题

1. D-Bus 的服务名、对象路径和接口名分别标识什么？
2. 为什么 GUI 线程不应进行无超时同步 call？
3. QDBusAbstractAdaptor 的作用是什么？
4. serviceRegistered 是否保证接口已经完全可用？
5. 自定义类型传输前需要哪些准备？

### 参考答案

1. 服务进程、对象层级和对象提供的接口契约。
2. 远程服务可能卡住或消失，同步调用会冻结事件循环。
3. 把明确的 D-Bus 接口从业务 QObject 中抽离并导出。
4. 不保证，还应探测对象和方法是否准备完成。
5. 声明元类型、提供序列化流运算符并调用 qDBusRegisterMetaType。

## 13. 小结

Qt D-Bus 的可靠使用方式是固定协议标识、隔离 adaptor、优先异步调用，并把服务发现、超时、权限和类型签名纳入设计。总线只是传输层，业务层仍需完整验证输入、状态和生命周期。
