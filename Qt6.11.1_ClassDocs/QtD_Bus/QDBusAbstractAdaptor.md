# QDBusAbstractAdaptor
> Qt 6.11.1 · Qt D-Bus · 来自 `QDBusAbstractAdaptor`

## 作用定位

`QDBusAbstractAdaptor` 用来把一个本地 `QObject` 包装成明确的 D-Bus 接口。它通常不是业务对象本身，而是贴在业务对象上的“对外接口层”：D-Bus 看到 adaptor 暴露的属性、槽、信号和 invokable，业务代码仍然留在原来的 QObject 里。

这种设计的好处是导出面可控。你不必把内部对象的所有公开槽都暴露给进程外调用者，而是用 adaptor 定义稳定、窄小、可审计的 IPC 契约。

## 类说明

- 头文件：`#include <QDBusAbstractAdaptor>`
- CMake：链接 `Qt6::DBus`
- 继承：`QObject`
- 构造函数是 `protected`，必须继承后使用
- adaptor 以被包装对象作为 parent；真实对象销毁时 adaptor 会随之销毁

## API 速查

| API | 说明 |
| --- | --- |
| `QDBusAbstractAdaptor(QObject *obj)` | 创建 adaptor，并把 `obj` 作为父对象和真实承载对象。 |
| `~QDBusAbstractAdaptor()` | 释放 adaptor；通常不要手动删除，让父对象管理生命周期。 |
| `autoRelaySignals()` | 查询是否把真实对象上同签名信号自动转发成 adaptor 信号。 |
| `setAutoRelaySignals(bool)` | 开关自动信号中继；适合接口信号只是业务对象信号的外壳时使用。 |
| `Q_NOREPLY` | 宏：标记导出的 void 方法不需要 D-Bus 回复。 |

## 典型写法

```cpp
class PlayerAdaptor : public QDBusAbstractAdaptor
{
    Q_OBJECT
    Q_CLASSINFO("D-Bus Interface", "org.example.Player")
    Q_PROPERTY(QString title READ title)

public:
    explicit PlayerAdaptor(Player *player)
        : QDBusAbstractAdaptor(player), m_player(player)
    {
        setAutoRelaySignals(true);
    }

public slots:
    void Play() { m_player->play(); }
    Q_NOREPLY void Stop() { m_player->stop(); }

signals:
    void TitleChanged(const QString &title);

private:
    QString title() const { return m_player->title(); }
    Player *m_player;
};
```

注册时通常配合：

```cpp
new PlayerAdaptor(player);
QDBusConnection::sessionBus().registerObject(
    "/org/example/Player", player, QDBusConnection::ExportAdaptors);
```

关键点是 `registerObject()` 注册的是真实业务对象 `player`，Qt D-Bus 会在其子对象里找到 adaptor 并导出 adaptor 描述的接口。

## 使用场景

- 对外发布稳定 D-Bus API，同时保留内部 C++ 对象的自由演进。
- 一个业务对象需要导出多个 D-Bus 接口，每个接口一个 adaptor。
- 要控制哪些槽、属性、信号被进程外访问。
- 需要把信号名称、方法名称、属性名称整理成符合 D-Bus 风格的接口。

## 常见坑与经验

- `Q_CLASSINFO("D-Bus Interface", "...")` 是接口身份的关键；忘了写会让内省信息和调用端都很难工作。
- adaptor 不应该随便 `delete`。它的 parent 是真实对象，生命周期跟随真实对象。
- `Q_NOREPLY` 只能用于不返回输出参数的方法；远端如果还期待返回值，会得到不匹配的行为。
- 自动信号中继要求真实对象和 adaptor 上的信号签名完全一致；只是名字相似不够。
- 不要把内部 QObject 的全部 API 用 `ExportAllContents` 直接暴露出去。adaptor 的价值就在于把 IPC 边界收窄。
- D-Bus 方法会进入对象所属线程；槽函数里做慢操作会阻塞调用者和事件循环，必要时转给工作线程并使用延迟回复。

## 知识点覆盖

- Qt D-Bus adaptor 模式
- QObject 元对象、属性、槽、信号如何变成 D-Bus 接口
- D-Bus interface 的稳定契约设计
- 自动信号中继
- `Q_NOREPLY` 与无回复调用
- 导出对象时 `ExportAdaptors` 的意义
