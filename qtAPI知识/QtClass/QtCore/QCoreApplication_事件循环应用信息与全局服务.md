# Qt QCoreApplication 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QCoreApplication>`  
> 所属模块：`Qt6::Core`  
> 继承：`QObject -> QCoreApplication`  
> 定位：无 GUI Qt 程序的应用对象，并为所有 Qt 应用提供主事件循环、应用元数据、事件投递、翻译器、插件路径和权限入口

`QCoreApplication` 是 Qt 程序的运行时中心。控制台服务通常直接创建它；GUI 程序创建派生类 `QGuiApplication` 或 `QApplication`，但仍继承并使用本文的大部分 API。

## 1. 最小可用代码

### 1.1 CMake 配置

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

### 1.2 控制台事件循环

```cpp
#include <QCoreApplication>
#include <QTimer>

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);

    QCoreApplication::setOrganizationName("ExampleOrg");
    QCoreApplication::setApplicationName("WorkerService");
    QCoreApplication::setApplicationVersion("1.0.0");

    QTimer::singleShot(std::chrono::seconds(1), [] {
        qInfo() << "work finished";
        QCoreApplication::quit();
    });

    return QCoreApplication::exec();
}
```

应用对象必须在使用大多数 Qt 全局功能前创建，并在其他 QObject 之后销毁。通常它是 `main()` 中第一个 Qt 对象。

## 2. 三种应用类如何选择

```text
QCoreApplication
  └─ QGuiApplication
       └─ QApplication
```

| 程序类型 | 应用类 |
| --- | --- |
| 控制台、后台服务、纯 Core/Network/SQL | `QCoreApplication` |
| Qt Quick、窗口/屏幕/剪贴板，但不用 Widgets | `QGuiApplication` |
| QWidget 桌面应用 | `QApplication` |

一个进程只能有一个应用对象。不要在库中偷偷创建第二个实例；库应使用 `QCoreApplication::instance()` 检查宿主是否已初始化。

## 3. 构造参数与生命周期

```cpp
QCoreApplication(int &argc, char **argv);
```

`argc` 必须大于 0，`argv` 必须保持有效直到应用对象销毁；Qt 可能修改 `argc/argv` 以移除自己处理的参数。不要传临时构造的字符指针数组。

```cpp
if (QCoreApplication::startingUp())
    qDebug() << "application object not fully established";

if (QCoreApplication::closingDown())
    qDebug() << "global teardown is in progress";
```

`startingUp()`/`closingDown()` 主要供底层库判断全局 Qt 状态。业务对象不应依赖静态析构阶段继续使用 Qt 服务，因为销毁顺序不可靠。

## 4. 全局实例

```cpp
QCoreApplication *app = QCoreApplication::instance();
if (!app)
    return;
```

宏 `qApp` 在相应应用头文件中提供全局实例快捷方式，但库代码使用 `instance()` 更明确。返回指针不拥有对象，不可删除。

应用对象及其事件循环通常位于主线程。创建之前和析构之后，`instance()` 返回空指针。

## 5. 应用元数据

```cpp
QCoreApplication::setOrganizationName("ExampleOrg");
QCoreApplication::setOrganizationDomain("example.com");
QCoreApplication::setApplicationName("Editor");
QCoreApplication::setApplicationVersion("2.4.1");
```

对应读取与变化信号：

```cpp
qDebug() << QCoreApplication::organizationName();
qDebug() << QCoreApplication::organizationDomain();
qDebug() << QCoreApplication::applicationName();
qDebug() << QCoreApplication::applicationVersion();
```

这些值会影响 `QSettings`、`QStandardPaths`、日志和系统集成，应该在创建依赖它们的对象前设置。applicationName 未显式设置时可能从可执行文件名推导，不能把这种默认值当成稳定数据目录标识。

## 6. 可执行文件和进程信息

```cpp
const QString executable = QCoreApplication::applicationFilePath();
const QString directory = QCoreApplication::applicationDirPath();
const qint64 pid = QCoreApplication::applicationPid();
```

`applicationDirPath()` 是可执行文件所在目录，不是当前工作目录。不要用相对路径假设程序从安装目录启动；资源、配置和用户数据分别使用资源系统、`QStandardPaths` 或显式路径。

在某些 Unix 环境中，如果系统无法从 `/proc` 等来源确定路径，结果可能受当前工作目录影响。不要把它用于安全边界判断。

## 7. 命令行参数

```cpp
const QStringList arguments = QCoreApplication::arguments();
for (const QString &arg : arguments)
    qDebug() << arg;
```

通常第一项是程序路径，但平台细节不同。在 Unix 上参数由本地 8 位编码转换，无法表示的字符可能丢失；Windows 上如果没有修改传给构造函数的参数，Qt 可从系统宽字符命令行重建参数。

正式解析使用 `QCommandLineParser`：

```cpp
QCommandLineParser parser;
parser.setApplicationDescription("Batch converter");
parser.addHelpOption();
parser.addVersionOption();
parser.addPositionalArgument("input", "Input file");
parser.process(app);
```

反复调用 `arguments()` 可能较慢；需要多次访问时保存结果。

## 8. 主事件循环 `exec()`

```cpp
const int exitCode = QCoreApplication::exec();
return exitCode;
```

事件循环持续取出并分发：

- 窗口系统和平台事件。
- 定时器事件。
- socket/notifier 事件。
- queued signal/slot 调用。
- `postEvent()` 投递事件。
- deferred delete 事件。

`exec()` 应从主线程调用。它直到 `quit()`/`exit()` 或平台终止流程才返回。部分平台可能在系统注销或进程结束时不给 `main()` 尾部完整执行机会，因此清理工作应连接到 `aboutToQuit()`。

## 9. `quit()`、`exit()` 与 `aboutToQuit()`

### 9.1 正常退出

```cpp
connect(controller, &Controller::finished,
        qApp, &QCoreApplication::quit,
        Qt::QueuedConnection);
```

`quit()` 请求事件循环以返回码 0 退出，并且是线程安全的。建议使用 queued connection：如果在 `exec()` 之前直接发射连接到 quit 的信号，直接调用可能无效果。

### 9.2 指定退出码

```cpp
QCoreApplication::exit(2);
```

`exit(returnCode)` 让事件循环返回指定值，但它不是线程安全函数。其他线程要退出主循环，应通过 queued invocation 调用：

```cpp
QMetaObject::invokeMethod(qApp, [] {
    QCoreApplication::exit(2);
}, Qt::QueuedConnection);
```

### 9.3 收尾信号

```cpp
connect(qApp, &QCoreApplication::aboutToQuit,
        &manager, &Manager::flushState);
```

`aboutToQuit()` 发出时主事件循环即将停止，此时不适合启动依赖长期事件处理的新异步工作。收尾应短小、确定，复杂持久化应在更早阶段完成。

## 10. Quit Lock

```cpp
QCoreApplication::setQuitLockEnabled(true);
```

启用后，最后一个 `QEventLoopLocker` 销毁可能触发应用退出。它适合让后台活动明确持有“应用仍应运行”的锁。关闭 quit lock 后，锁计数归零不再自动请求退出。

不要用 quit lock 代替任务取消和资源管理；它只控制退出条件。

## 11. `processEvents()`：谨慎使用

```cpp
QCoreApplication::processEvents(QEventLoop::AllEvents);
```

它手工处理当前线程事件，经常被用于长循环中“保持界面响应”，但容易引入重入：用户可以再次触发同一操作，对象可能在循环中被删除，状态机也可能被打断。

更好的方向是把长任务拆分、异步化或移到工作线程。

带期限的 Qt 6 重载：

```cpp
QCoreApplication::processEvents(
    QEventLoop::AllEvents,
    QDeadlineTimer(std::chrono::milliseconds(20)));
```

期限重载也会处理调用期间新投递的事件；无期限旧重载通常只处理调用前已排队的事件集合。即使有 deadline，也不保证业务代码不发生重入。

## 12. 同步发送与异步投递事件

### 12.1 `sendEvent()`

```cpp
QEvent event(MyEventType);
const bool accepted = QCoreApplication::sendEvent(receiver, &event);
```

同步调用 receiver 的事件处理路径，调用返回后栈事件仍由调用者拥有。通常应在 receiver 所属线程使用。

### 12.2 `postEvent()`

```cpp
QCoreApplication::postEvent(
    receiver,
    new MyEvent(payload),
    Qt::NormalEventPriority);
```

异步、线程安全地把事件加入 receiver 所在线程队列，并接管事件所有权。事件必须在堆上创建，投递后不可再访问。

高优先级事件先于低优先级处理；同优先级通常保持投递顺序。滥用高优先级会让普通事件饥饿。

## 13. Posted Event 管理

```cpp
QCoreApplication::sendPostedEvents(receiver, MyEventType);
QCoreApplication::removePostedEvents(receiver, MyEventType);
```

`sendPostedEvents()` 立即发送匹配的已投递事件；`removePostedEvents()` 删除匹配事件而不分发。后者可能破坏对象内部不变量，文档建议一般不要使用。

不要移除 `DeferredDelete` 事件，否则 `deleteLater()` 对象会泄漏或延迟到不可预测的时机。

## 14. 事件分发器与 `notify()`

```cpp
QAbstractEventDispatcher *dispatcher =
    QCoreApplication::eventDispatcher();
```

自定义 dispatcher 必须在目标线程建立事件分发器前设置：

```cpp
QCoreApplication::setEventDispatcher(customDispatcher);
```

这是平台和嵌入式事件循环集成的底层接口，普通应用不应更换。

`notify(receiver, event)` 把事件发送给对象，派生应用类可重载做全局观察或异常边界。但 Qt 未来版本对非主线程事件调用的支持范围可能收紧；全局事件监控优先使用事件过滤器和平台明确接口。

## 15. 应用属性

```cpp
QCoreApplication::setAttribute(Qt::AA_Use96Dpi, true);

if (QCoreApplication::testAttribute(Qt::AA_Use96Dpi))
    qDebug() << "fixed DPI behavior enabled";
```

许多 `Qt::ApplicationAttribute` 必须在创建应用对象前设置才有效：

```cpp
int main(int argc, char *argv[])
{
    QCoreApplication::setAttribute(...);
    QCoreApplication app(argc, argv);
    // ...
}
```

属性含义与平台/渲染后端密切相关。不要为了消除警告随意启用；根据对应枚举文档和目标平台验证。

## 16. 动态库与插件路径

```cpp
QStringList paths = QCoreApplication::libraryPaths();
QCoreApplication::addLibraryPath("plugins");
QCoreApplication::removeLibraryPath("plugins");
QCoreApplication::setLibraryPaths({"plugins", "extensions"});
```

这些路径用于 Qt 插件加载。应用对象创建时，Qt 会加入安装插件目录和可执行文件目录等默认位置；应用对象析构后列表可能恢复。

安全注意：不要把用户可写的任意目录或当前工作目录加入生产插件搜索路径。攻击者可放置同名平台、图像格式或 SQL 驱动插件，被进程加载执行。

`addLibraryPath()` 会把新路径放在搜索列表前部；路径不存在时可能被忽略。需要确定部署时，使用绝对、受信任路径并记录实际 `libraryPaths()`。

## 17. 翻译器

```cpp
QTranslator translator;
if (translator.load(":/i18n/app_zh_CN.qm"))
    QCoreApplication::installTranslator(&translator);
```

后安装的翻译器优先搜索：

```cpp
QCoreApplication::removeTranslator(&translator);
```

翻译器必须在安装期间保持存活。安装或移除会产生语言变化事件；Widgets 需要重新设置界面文字，QML 引擎需要 retranslate。

底层翻译入口：

```cpp
QString text = QCoreApplication::translate(
    "LoginDialog", "Sign in", nullptr, -1);
```

## 18. 原生事件过滤器

```cpp
class NativeFilter : public QAbstractNativeEventFilter
{
public:
    bool nativeEventFilter(const QByteArray &eventType,
                           void *message,
                           qintptr *result) override;
};

NativeFilter filter;
app.installNativeEventFilter(&filter);
```

移除：

```cpp
app.removeNativeEventFilter(&filter);
```

这是平台原生消息的低层入口，数据结构因 Windows、X11 等平台不同。过滤器对象必须保持存活。设置某些插件应用属性时原生过滤器可能被禁用。

普通键鼠和窗口事件应使用 Qt 事件系统，避免平台分支污染业务代码。

## 19. 运行时权限

### 19.1 检查

```cpp
QCameraPermission permission;
const Qt::PermissionStatus status =
    QCoreApplication::checkPermission(permission);
```

### 19.2 请求

```cpp
qApp->requestPermission(permission, this,
    [this](const QPermission &result) {
        if (result.status() == Qt::PermissionStatus::Granted)
            startCamera();
        else
            showPermissionDenied();
    });
```

权限请求是异步的，使用带 context 的重载可在页面销毁时自动取消回调关联。某些平台不需要运行时权限，状态会直接为 Granted；业务仍应处理 Denied 和 Undetermined。

请求权限前还可能需要在 Android manifest、Apple Info.plist 等部署元数据中声明用途，否则系统会拒绝或终止应用。

## 20. Setuid 安全开关

Qt 默认拒绝在 Unix setuid 环境下运行应用对象，因为环境变量、插件路径和平台集成带来高风险。`setSetuidAllowed(true)` 可以覆盖，但官方明确警告其安全风险：

```cpp
QCoreApplication::setSetuidAllowed(true);
```

一般不要使用。需要特权操作时采用最小权限辅助进程、操作系统服务或权限分离架构。

## 21. 常见误区

### 把 applicationDirPath 当工作目录

两者没有必然关系。用户文件、配置、插件和应用资源应各用正确路径来源。

### 在长循环里频繁 processEvents

这会产生难以控制的重入。改用异步状态机、线程池或分块 `QTimer`。

### 从工作线程直接调用 exit

`exit()` 不是线程安全的；使用 queued invocation 或线程安全的 `quit()`。

### `postEvent` 后继续修改事件

所有权已转给 Qt，调用后不可再访问。

### 翻译器是局部临时变量

函数返回后 translator 被销毁，但应用仍曾安装其地址。把翻译器作为应用级长生命周期对象，并在销毁前移除。

### 把可写目录放入 libraryPaths

这可能变成代码执行入口。插件目录必须受信任。

## API 速查表
### 22.1 构造、实例和应用元数据

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QCoreApplication(int &argc, char **argv)` | 创建当前进程的 Qt 应用对象，并初始化全局事件基础设施。 | 一个进程通常只能有一个 application object；`argc/argv` 要在对象存活期间保持有效，Qt 可能移除自己识别的参数。 |
| 析构 | `~QCoreApplication()` | 销毁应用对象并结束其全局服务生命周期。 | 应在其他 QObject 和依赖事件循环的对象之后销毁；静态析构阶段不要再假设 Qt 服务可用。 |
| 全局实例 | `instance()` | 返回当前进程的 `QCoreApplication` 实例。 | 返回指针不转移所有权；应用对象尚未创建或已经销毁时返回 `nullptr`。 |
| 全局实例 | `instanceExists()` | 判断应用实例是否已经存在。 | 适合库代码做能力探测；它不代表事件循环已经运行。 |
| 命令行 | `arguments()` | 返回 Qt 看到的命令行参数列表。 | 需要选项、位置参数和帮助信息时使用 `QCommandLineParser`；频繁读取时应缓存结果。 |
| 应用属性 | `setAttribute(Qt::ApplicationAttribute, bool on = true)` | 设置应用级行为开关。 | 很多属性必须在构造 application object 之前设置；不要为了消除警告随意启用。 |
| 应用属性 | `testAttribute(Qt::ApplicationAttribute)` | 查询应用属性是否启用。 | 只能说明属性状态，不能替代对具体平台行为的验证。 |
| 组织信息 | `setOrganizationName(const QString &)` | 设置组织名称。 | 会参与 `QSettings` 等默认组织标识；应在创建依赖它的对象前设置。 |
| 组织信息 | `organizationName()` | 读取组织名称。 | 未设置时可能为空或使用平台默认值，不要把默认值当成稳定业务 ID。 |
| 组织信息 | `setOrganizationDomain(const QString &)` | 设置组织域名。 | 用于应用身份和系统集成；不要把它当作网络连接地址。 |
| 组织信息 | `organizationDomain()` | 读取组织域名。 | 返回的是应用元数据，不是当前网络域名解析结果。 |
| 应用信息 | `setApplicationName(const QString &)` | 设置应用名称。 | 会影响配置、日志和系统集成；应在创建依赖它的对象前确定。 |
| 应用信息 | `applicationName()` | 读取应用名称。 | 未显式设置时可能从可执行文件名推导，不适合作为未经确认的稳定数据目录标识。 |
| 应用信息 | `setApplicationVersion(const QString &)` | 设置应用版本。 | 供命令行帮助、日志和系统集成使用；版本格式由应用自行约定。 |
| 应用信息 | `applicationVersion()` | 读取应用版本。 | 返回字符串，不负责版本比较；需要比较时使用明确的版本解析策略。 |
| 元数据通知 | `organizationNameChanged()` / `organizationDomainChanged()` | 通知组织元数据发生变化。 | 适合刷新依赖应用身份的绑定；普通程序通常在启动阶段设置一次。 |
| 元数据通知 | `applicationNameChanged()` / `applicationVersionChanged()` | 通知应用名称或版本发生变化。 | 不要在通知槽中无条件写回同一属性，避免重复更新。 |

### 22.2 事件循环和退出

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 主循环 | `exec()` | 启动当前应用的主事件循环并返回退出码。 | 通常从主线程调用；没有事件循环时 queued 调用、定时器和 `deleteLater()` 无法按正常节奏工作。 |
| 退出 | `quit()` | 请求事件循环以返回码 `0` 退出。 | 线程安全；从其他线程发起退出时优先使用 queued connection。 |
| 退出 | `exit(int retcode = 0)` | 请求事件循环返回指定退出码。 | 不是线程安全函数；其他线程应通过 queued invocation 回到应用线程调用。 |
| 退出通知 | `aboutToQuit()` | 在主事件循环即将停止前通知收尾代码。 | 适合快速保存、刷新和释放资源；不要在这里启动依赖长期事件循环的新异步任务。 |
| 退出锁 | `isQuitLockEnabled()` | 查询是否启用 quit lock 机制。 | 它只影响 `QEventLoopLocker` 对退出条件的作用，不负责取消任务或释放资源。 |
| 退出锁 | `setQuitLockEnabled(bool enabled)` | 开启或关闭由 `QEventLoopLocker` 参与控制应用退出的机制。 | 需要明确应用的生命周期策略；不要把它当作后台任务管理器。 |
| 启动阶段 | `startingUp()` | 查询 Qt 应用对象是否仍处于启动阶段。 | 主要供 Qt 或底层库判断全局初始化状态，业务代码不应依赖静态初始化顺序。 |
| 关闭阶段 | `closingDown()` | 查询 Qt 全局对象是否正在关闭。 | 关闭阶段的对象析构顺序不适合启动新工作或访问不确定的全局服务。 |

### 22.3 事件发送、投递和分发器

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 手工处理 | `processEvents(QEventLoop::ProcessEventsFlags flags = AllEvents)` | 立即处理当前线程事件队列中的一批事件。 | 容易产生重入；长任务优先拆分、异步化或移到工作线程，不要把它当作通用“刷新界面”函数。 |
| 手工处理 | `processEvents(flags, int maxtime)` | 在给定最大毫秒数内处理事件。 | 仍然可能让用户操作重入当前业务；时间上限不是逻辑隔离。 |
| 手工处理 | `processEvents(flags, QDeadlineTimer deadline)` | 在截止时间前处理事件，Qt 6 的 deadline 重载还会处理期间新投递的事件。 | 适合底层集成的短暂事件泵；使用前必须评估重入和对象删除风险。 |
| 同步发送 | `sendEvent(QObject *receiver, QEvent *event)` | 立即把事件同步交给接收对象处理。 | 调用者拥有事件对象；通常应在接收对象所属线程调用。 |
| 异步投递 | `postEvent(QObject *receiver, QEvent *event, int priority = Qt::NormalEventPriority)` | 把事件加入接收对象所属线程的事件队列。 | `event` 必须是堆对象，投递后所有权交给 Qt，不得继续访问或重复删除。 |
| 已投递事件 | `sendPostedEvents(QObject *receiver = nullptr, int event_type = 0)` | 立即分发匹配的已投递事件。 | 主要用于底层事件循环集成；过度手工发送会改变正常事件顺序。 |
| 已投递事件 | `removePostedEvents(QObject *receiver, int eventType = 0)` | 删除匹配的已投递事件而不分发。 | 可能破坏对象内部不变量；尤其不要随意删除 `DeferredDelete` 事件。 |
| 事件分发器 | `eventDispatcher()` | 获取当前线程的事件分发器。 | 返回对象由 Qt 管理；它反映调用线程的分发器，不是跨线程全局服务。 |
| 事件分发器 | `setEventDispatcher(QAbstractEventDispatcher *eventDispatcher)` | 在事件分发器建立前为当前线程设置自定义分发器。 | 这是平台集成级接口；设置时机、所有权和线程必须正确。 |
| 全局通知 | `notify(QObject *receiver, QEvent *event)` | 进入 Qt 对象事件处理路径的总入口。 | 重载时必须保持基类行为和返回值契约；全局观察优先考虑事件过滤器。 |
| 应用事件 | `event(QEvent *event)` | 处理 `QCoreApplication` 自身收到的事件。 | 通常由框架调用；重载时应保留基类处理。 |

### 22.4 路径、进程和插件

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 进程路径 | `applicationFilePath()` | 返回当前可执行文件的路径。 | 不等于资源目录、配置目录或当前工作目录。 |
| 进程路径 | `applicationDirPath()` | 返回当前可执行文件所在目录。 | 程序启动位置和工作目录可能不同；不要用它替代 `QDir::currentPath()`。 |
| 进程信息 | `applicationPid()` | 返回当前进程 ID。 | 适合日志、单实例协调和诊断；不是跨重启稳定的应用标识。 |
| 插件路径 | `libraryPaths()` | 查询 Qt 当前的插件搜索路径列表。 | 需要排查插件加载时记录实际结果。 |
| 插件路径 | `setLibraryPaths(const QStringList &paths)` | 完整替换 Qt 插件搜索路径。 | 只使用受信任、明确的路径；不要把用户可写目录加入生产环境。 |
| 插件路径 | `addLibraryPath(const QString &path)` | 把一个路径加入插件搜索列表。 | 新路径通常优先搜索；路径来源必须可信。 |
| 插件路径 | `removeLibraryPath(const QString &path)` | 从插件搜索列表移除路径。 | 已加载的插件不会自动卸载，只影响后续搜索。 |
| Setuid 安全 | `setSetuidAllowed(bool allow)` | 配置是否允许 Qt 应用在 Unix setuid 环境运行。 | 开启会扩大环境变量、插件和平台集成风险，一般保持默认安全策略。 |
| Setuid 安全 | `isSetuidAllowed()` | 查询当前 setuid 运行开关。 | 查询结果不代表当前进程一定处于 setuid 环境。 |

### 22.5 翻译、原生事件和权限

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 翻译器 | `installTranslator(QTranslator *translator)` | 把翻译器加入应用的翻译器栈。 | 翻译器对象必须在安装期间保持存活；后安装的翻译器优先搜索。 |
| 翻译器 | `removeTranslator(QTranslator *translator)` | 从应用移除指定翻译器。 | 移除后已有界面不会自动完成所有业务文本刷新，需要处理语言变化事件或主动 retranslate。 |
| 显式翻译 | `translate(const char *context, const char *key, const char *disambiguation = nullptr, int n = -1)` | 按上下文、源文本、歧义说明和复数数量查找翻译。 | `context` 和源文本要稳定；需要复数时正确传入 `n`，不要把翻译结果当持久化数据。 |
| 原生事件 | `installNativeEventFilter(QAbstractNativeEventFilter *filterObj)` | 安装平台原生消息过滤器。 | 过滤器对象必须保持存活；消息结构依赖具体平台。 |
| 原生事件 | `removeNativeEventFilter(QAbstractNativeEventFilter *filterObj)` | 移除已安装的原生消息过滤器。 | 普通 Qt 键鼠和窗口事件不应绕到这里处理。 |
| 权限查询 | `checkPermission(const QPermission &permission)` | 查询当前运行时权限状态。 | 业务必须处理 Granted、Denied 和 Undetermined；部署清单仍可能决定最终结果。 |
| 权限请求 | `requestPermission(const QPermission &, context, functor)` | 异步请求运行时权限并在结果返回时执行回调。 | 优先使用带 context 的重载，context 销毁后回调自动失效；不要同步等待。 |

### 22.6 属性和信号

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 属性 | `applicationName` / `applicationVersion` | 以 Qt 属性形式访问应用名称和版本。 | 写入仍应通过对应 setter；变化时会发出相应 changed 信号。 |
| 属性 | `organizationName` / `organizationDomain` | 以 Qt 属性形式访问组织身份。 | 会影响设置和系统集成；应在依赖它们的对象创建前确定。 |
| 属性 | `quitLockEnabled` | 以 Qt 属性形式访问 quit lock 开关。 | 它控制事件循环退出条件，不代表任务已经完成。 |

---

### 一句话总结

`QCoreApplication` 把 Qt 进程的事件循环和全局服务组织起来：应用对象要最早创建、最晚销毁，用异步事件而非手工泵循环组织工作，用明确路径和可信插件目录部署，并通过 `aboutToQuit()`、权限回调和翻译器生命周期完成可靠收尾。
