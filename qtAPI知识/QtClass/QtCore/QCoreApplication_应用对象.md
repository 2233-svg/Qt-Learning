# Qt QCoreApplication 深入笔记

> 适用版本：Qt 6.11（Qt 6.5 起包含权限请求 API）  
> 头文件：`#include <QCoreApplication>`  
> 所属模块：`Qt6::Core`  
> 相关类：`QGuiApplication`、`QApplication`、`QEventLoop`、`QAbstractEventDispatcher`、`QTranslator`

## 1. 它解决的不是“创建一个程序”，而是让程序能活着响应事情

`QCoreApplication` 是没有图形界面的 Qt 应用对象。它负责建立全局应用上下文，并运行事件循环：定时器到期、网络完成、跨线程信号、`postEvent()` 投递的事件、操作系统通知，最终都会在这里被分发。

没有它，许多 Qt Core 类仍可创建，但异步工作通常不会自然推进。例如 `QTimer` 不会超时，排队连接不会执行，事件队列也无人取出处理。

它处于这条继承链的底部：

```text
QObject
  └─ QCoreApplication       控制台程序、后台服务、非 GUI 工具
       └─ QGuiApplication   需要窗口系统、屏幕、剪贴板、QWindow
            └─ QApplication 需要 QWidget 控件体系
```

选择原则很简单：

| 程序类型 | 应使用的应用对象 | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 命令行工具、后台任务、守护进程 | `QCoreApplication` | 提供事件循环与 Qt Core 能力 | 不创建窗口系统或 Widgets 资源 |
| 使用 `QWindow`、QML、屏幕、拖放等 GUI 基础设施 | `QGuiApplication` | 接入窗口系统 | 无法替代 Widgets 的样式和控件行为 |
| 使用 `QWidget`、`QMainWindow`、`QDialog` | `QApplication` | 提供 Widgets 所需的样式和控件行为 | 它已包含 `QGuiApplication` 与 `QCoreApplication` 能力 |

一个进程通常只能有一个 `QCoreApplication` 或其派生类实例。它不是某个业务模块的“服务对象”，也不应该被随意创建、销毁再创建；它代表整个进程的 Qt 运行时。

## 2. 最小正确入口：先建应用对象，再进入事件循环

```cpp
#include <QCoreApplication>
#include <QTimer>
#include <QDebug>

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);

    QTimer::singleShot(0, &app, [] {
        qInfo() << "开始处理任务";
        QCoreApplication::quit();
    });

    return app.exec();
}
```

这里的执行顺序很关键：

1. `QCoreApplication app(argc, argv);` 建立全局实例、事件分发器和应用级配置。
2. 创建对象、连接信号、投递任务。
3. `app.exec()` 开始主事件循环；此调用通常阻塞到应用退出。
4. 主循环结束后，`main()` 返回，栈上的 `app` 析构。

`argc` 和 `argv` 以引用形式传入。它们以及每个参数字符串必须在 `app` 的整个生命周期内保持有效，所以应像示例一样定义在 `main()` 的最外层，不能把临时构造的参数数组交给构造函数。

### 2.1 为什么不能把业务都写在 `exec()` 前

`exec()` 前可以做同步初始化，例如读取配置、注册元类型、创建长期对象；但依赖事件循环的事情要等事件循环开始后才会执行。

```cpp
QCoreApplication app(argc, argv);

QNetworkAccessManager manager;
// manager.get(...) 的异步完成信号，要在 exec() 运行后才有机会触发。

return app.exec();
```

若希望“启动后立刻异步执行一次”，使用 `QTimer::singleShot(0, ...)` 或投递自定义事件，而不是手工反复调用 `processEvents()`。

## 3. 事件循环、退出与析构：最容易写错的生命周期边界

### 3.1 `exec()` 何时返回

以下路径会让主事件循环结束：

- 调用 `QCoreApplication::quit()`；
- 在主线程调用 `QCoreApplication::exit(code)`；
- 最后一个 `QEventLoopLocker` 被释放，且 quit lock 已启用；
- 操作系统要求应用退出，Qt 转换为退出流程。

退出流程中会发出 `aboutToQuit()`。在这个信号里停止后台任务、刷新延迟写入、关闭连接比较合适：

```cpp
QObject::connect(&app, &QCoreApplication::aboutToQuit, [] {
    // 停止任务、请求工作线程收尾、写入最后状态。
});
```

不要只依赖 `exec()` 之后的代码做清理。某些平台或嵌入式场景中，主事件循环不保证像普通桌面程序那样返回到 `main()`；`aboutToQuit()` 才是 Qt 提供的应用关闭通知。

### 3.2 `quit()` 与 `exit()` 不可互换

```cpp
QCoreApplication::quit();      // 建议的正常退出请求，线程安全
QCoreApplication::exit(42);    // 指定退出码，必须由主线程执行
```

- `quit()` 等价于请求 `exit(0)`，会让事件循环在合适的时机结束，适合从工作线程、信号槽或业务逻辑中发起正常关闭。
- `exit(int)` **不是线程安全的**。只能在应用主线程中调用；事件循环尚未运行时调用没有效果。
- 若在 `exec()` 前连接信号到 `quit()`，应指定 `Qt::QueuedConnection`，确保槽在事件循环启动后执行：

```cpp
QObject::connect(worker, &Worker::finished,
                 &app, &QCoreApplication::quit,
                 Qt::QueuedConnection);
```

### 3.3 quit lock 是什么

`QEventLoopLocker` 可在一个关键异步活动期间阻止 Qt 因“没有可保持运行的对象”而自动退出。`quitLockEnabled` 控制这种锁是否起作用，默认通常为启用。

它用于“还有一项必须完成的异步收尾工作”，不是用来替代明确的程序生命周期管理。服务程序应有明确的停止协议，例如停止接收任务、取消或等待正在运行的任务、最后调用 `quit()`。

## 4. 事件如何到达 QObject：同步发送、异步投递与手工泵事件

Qt 的事件系统有三个常见入口，语义差异很大。

### 4.1 `sendEvent()`：当前调用栈内同步处理

```cpp
QEvent event(QEvent::User);
const bool handled = QCoreApplication::sendEvent(receiver, &event);
```

`sendEvent()` 立刻调用接收者的事件处理路径，返回前事件已经处理完。事件的所有权仍属于调用方，所以栈对象完全正常；Qt 不会替你删除它。

适合测试某个 `event()` 分支，或确实需要立即完成的内部事件分发。不要拿它跨线程“通知另一个对象”：接收者的 `QObject::event()` 会在**当前调用线程**运行，容易违反该对象的线程归属。

### 4.2 `postEvent()`：进入接收者线程的事件队列

```cpp
QCoreApplication::postEvent(
    receiver, new QEvent(QEvent::User), Qt::HighEventPriority);
```

`postEvent()` 把堆分配的事件放入接收者所属线程的队列，控制权立即交给 Qt。调用后不得读取、释放或复用该 `QEvent *`；事件最终处理完后由 Qt 删除。

它是线程安全的，适合工作线程把小型通知交给主线程对象处理：

```cpp
// 在工作线程中：
QCoreApplication::postEvent(mainController,
                            new ResultReadyEvent(result));
```

优先级只决定同一事件队列中较早或较晚处理的倾向，不会让事件抢占正在执行的槽函数。高优先级事件若持续大量产生，也可能饿死低优先级工作，通常不要滥用。

### 4.3 `sendPostedEvents()` 与 `removePostedEvents()`：少用的队列维护工具

`sendPostedEvents()` 立即处理已经投递的事件；它必须在接收者所属线程运行。它不是跨线程同步工具，也不是普通业务代码中“强制刷新 UI”的按钮。

`removePostedEvents(receiver, type)` 从队列移除尚未分发的事件，且线程安全。但是事件往往承载对象内部状态转换，随意移除会让接收者的状态机失去前后对应关系。除非你实现了完整的对象协议，否则不要调用它；尤其不能传 `eventType == 0` 来删除该对象的全部待处理事件。

### 4.4 `processEvents()`：看似方便，实则会引入重入

```cpp
QCoreApplication::processEvents(QEventLoop::ExcludeUserInputEvents);
```

它临时处理当前线程的待处理事件。常见诱惑是在耗时循环里调用它，让窗口“不假死”；问题是它会让计时器、网络回调、用户操作或其它槽函数插进当前函数，造成重入、对象被删除、状态被二次修改等难以复现的问题。

优先方案：

- 把耗时工作移到工作线程；
- 分块处理，并在每块结束后排队执行下一块；
- 使用异步 API 和信号槽链路；
- 需要局部等待时，审慎使用有明确退出条件的 `QEventLoop`。

Qt 6.7 增加了接受 `QDeadlineTimer` 的重载；`int ms` 版本会转发到这一能力。它们只是限制本次泵事件的时间预算，不会消除重入风险。

## 5. 应用身份与启动参数：全局设置应尽早完成

### 5.1 名称、版本与组织信息

```cpp
QCoreApplication app(argc, argv);

QCoreApplication::setOrganizationName("Example Studio");
QCoreApplication::setOrganizationDomain("example.com");
QCoreApplication::setApplicationName("batch-importer");
QCoreApplication::setApplicationVersion("2.4.0");
```

这些值不只是“关于对话框里的文字”。`QSettings` 的默认存储位置、日志信息、`QCommandLineParser` 的帮助文本、临时目录和标准路径等都会参考它们。

因此要在创建 `QSettings`、初始化依赖这些信息的组件、解析命令行之前设置好。`applicationName` 默认通常来自可执行文件名，但不要把这个默认值当作稳定的产品标识。

### 5.2 `arguments()` 只用于获取，不负责解析

```cpp
const QStringList args = QCoreApplication::arguments();
```

这个函数返回启动参数列表。在某些平台上它需要额外转换，频繁调用可能较慢，应缓存结果。真正需要选项、位置参数、默认值、帮助文本和错误提示时，交给 `QCommandLineParser`：

```cpp
QCommandLineParser parser;
parser.addHelpOption();
parser.process(app);
```

不要依赖旧的 `-qmljsdebugger` 参数；Qt 6 中它已被移除。

### 5.3 可执行文件路径不是永远可靠的部署定位方案

`applicationDirPath()` 和 `applicationFilePath()` 可帮助定位随程序部署的资源或插件。在 Linux 上，Qt 优先依赖 `/proc` 等机制；若不可用会退回 `argv[0]`。如果程序启动后改变了当前工作目录，退回路径可能不再可靠。

更稳妥的资源策略是 Qt 资源系统 `:/`，或在部署方案中明确配置路径；不要把“当前工作目录”等同于“可执行文件目录”。

## 6. 插件搜索路径：部署错误常发生在这里

Qt 用 library paths 寻找可加载插件，例如平台插件、图像格式插件、SQL 驱动和样式插件。搜索路径可来自安装目录、应用目录、`qt.conf` 和 `QT_PLUGIN_PATH` 等环境配置。

```cpp
QCoreApplication app(argc, argv);

QCoreApplication::addLibraryPath(
    QCoreApplication::applicationDirPath() + "/plugins");
```

注意：

- 必须在创建应用对象后再查询 `libraryPaths()`；早期结果不适合作为部署判断依据。
- `addLibraryPath()` 将新路径插到列表前面，优先级更高。
- `setLibraryPaths()` 会整体替换路径列表，应只在完全掌握部署环境时使用。
- 应用对象销毁后，这套路径配置会重置。
- 不要把不受信任目录加入插件路径，否则动态库加载本身可能成为安全边界问题。

## 7. 翻译：运行期切换语言需要触发界面重译

```cpp
#include <QTranslator>

QTranslator translator;
if (translator.load(":/i18n/app_zh_CN.qm"))
    QCoreApplication::installTranslator(&translator);
```

安装的翻译器由调用方持有，必须在应用仍可能翻译文本期间保持存活。多个翻译器同时安装时，最后安装的翻译器优先匹配。

`installTranslator()`、`removeTranslator()` 会令 Qt 向顶层对象发送语言变化相关事件。使用 Widgets 时，通常在窗口的 `changeEvent()` 中处理 `QEvent::LanguageChange` 并重新调用 `ui->retranslateUi(this)`；仅调用 `installTranslator()` 不会自动改写你已经保存到控件中的普通字符串。

不继承 `QObject` 的工具类可借助宏提供 `tr()`：

```cpp
class ErrorText
{
    Q_DECLARE_TR_FUNCTIONS(ErrorText)
public:
    static QString missingFile()
    {
        return tr("File does not exist");
    }
};
```

该宏必须放在类的第一个访问说明符之前，因为它自身会展开出 `public` 和 `private` 成员。

`QCoreApplication::translate()` 是线程安全的；找不到翻译时会返回源文本。带 `n` 的调用用于复数规则，不能自己用 `QString::arg()` 模拟不同语言的复数形式。

## 8. 权限请求：Qt 6.5+ 的异步边界

移动平台或受权限约束的系统中，应用可通过 `QPermission` 派生类型查询与请求权限，例如相机、蓝牙、日历或联系人权限。

```cpp
#include <QCameraPermission>

QCameraPermission permission;
if (app.checkPermission(permission) == Qt::PermissionStatus::Granted) {
    startCamera();
} else {
    app.requestPermission(permission, &app,
        [](const QPermission &result) {
            if (result.status() == Qt::PermissionStatus::Granted)
                startCamera();
        });
}
```

请求必须从主线程发起。带 `context` 的重载会在 `context` 所在线程调用回调；若 `context` 已销毁，回调不会调用，这能避免异步权限对已关闭页面进行回调。无 context 的重载更容易留下悬空捕获，应只用于对象生命周期明确受控的场合。

权限状态并非所有平台都支持相同的权限类型；桌面系统上它也可能永远返回已授权或由系统策略控制。业务逻辑仍要处理拒绝、受限和不可用的结果。

## 9. 进阶接口：全局钩子很强，也会扩大问题范围

### 9.1 `notify()` 与原生事件过滤器

重写 `notify()` 能在 Qt 分发事件给对象前观察或拦截事件：

```cpp
class MyApplication : public QCoreApplication
{
public:
    using QCoreApplication::QCoreApplication;

    bool notify(QObject *receiver, QEvent *event) override
    {
        return QCoreApplication::notify(receiver, event);
    }
};
```

这适合少量全局诊断、异常隔离或统一埋点，不适合承担业务分发。Qt 7 起，`notify()` 不再为主线程以外的对象调用；若重写它，还要确保应用析构前由你创建的外部事件处理线程已经停止。

`installNativeEventFilter()` 更靠近操作系统消息层。它面向窗口系统的原生事件，平台相关、可移植性差；优先用普通 Qt 事件过滤器 `QObject::installEventFilter()`。一旦插件启用了 `Qt::AA_PluginApplication` 属性，原生事件过滤器不会被调用。

### 9.2 事件分发器与启动/结束例程

`setEventDispatcher()` 用于替换线程的事件分发器，必须在 `QCoreApplication` 创建前调用，并且应用对象接管传入分发器的所有权。这属于事件循环集成或平台适配层需求，普通应用不应调用。

`Q_COREAPP_STARTUP_FUNCTION(function)` 注册一个在 `QCoreApplication` 构造结束时调用的函数，发生在 GUI 初始化前。静态链接库中的注册函数可能被链接器丢弃，不能把它当成可靠的插件发现机制。

`qAddPreRoutine()` 注册构造前例程，`qAddPostRoutine()` 注册析构期间的清理例程；后注册的 post routine 会先执行。若清理函数属于可动态卸载的模块，模块卸载后函数地址会失效，因此更建议用明确对象所有权管理资源；不再需要时可用 `qRemovePostRoutine()` 取消。

### 9.3 setuid 程序不是普通 Qt 部署目标

Unix 上，Qt 默认拒绝 setuid 程序，因为插件、环境变量和动态加载可能扩大提权风险。确有审计过的特殊需求时，必须在创建应用对象**之前**调用：

```cpp
QCoreApplication::setSetuidAllowed(true);
QCoreApplication app(argc, argv);
```

它在非 Unix 平台无实际意义。不要把它当成“修复启动失败”的常规配置；应先重新评估权限模型。

## 10. 常见误区速览

| 误区 | 为什么会出问题 | 应该怎样做 | 使用时重点注意 |
| --- | --- | --- | --- |
| 没有 `exec()` 也期待定时器、网络回调执行 | 没有线程事件循环取出队列工作 | 让主线程运行 `exec()`，或在工作线程调用 `QThread::exec()` | 线程是否有事件循环要按线程分别判断 |
| 工作线程直接调用 GUI 或 `sendEvent()` 给主线程对象 | 槽或 `event()` 可能在错误线程运行 | 使用信号槽的队列连接或 `postEvent()` | GUI 对象只能由 GUI 线程操作 |
| 给 `postEvent()` 传栈事件 | Qt 稍后会删除它，造成非法释放 | 始终传 `new QEvent(...)` 或自定义堆事件 | 投递后也不得保留或访问原始指针 |
| 在长循环里不断 `processEvents()` | 其它业务可重入当前状态 | 使用工作线程、异步分块或状态机 | 仅在理解嵌套事件循环后才使用 |
| 用 `exit()` 结束工作线程中的应用 | `exit()` 不是线程安全的 | 工作线程调用 `quit()` 或发信号给主线程 | 需要非零退出码时让主线程调用 `exit(code)` |
| 任意调用 `removePostedEvents()` | 破坏对象内部事件序列 | 设计取消协议，必要时只移除你定义且可证明安全的类型 | 不传 `eventType == 0` 批量清空 |
| 翻译器是局部变量 | 函数返回后翻译器销毁，翻译立即失效 | 让翻译器成为应用或长期控制器成员 | 卸载前让界面收到并处理语言变化事件 |
| `applicationDirPath()` 当作当前目录 | 两者本来不是同一个概念 | 分别使用可执行目录和 `QDir::currentPath()` | 部署资源优先使用 `:/` 或明确配置路径 |

## API 速查表
### 11.1 构造、属性与应用状态

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QCoreApplication(int &argc, char **argv)` | 创建全局应用对象并准备事件循环环境 | 通常全进程仅一个；`argc`、`argv` 和参数字符串必须活到应用析构 |
| 析构 | `~QCoreApplication()` | 销毁全局应用对象，执行已注册的 post routine 并重置部分全局状态 | 关闭前用 `aboutToQuit()` 协调异步任务；不要让后台线程继续访问 Qt 全局对象 |
| 属性 | `applicationName()` | 返回应用名称 | 默认通常来自可执行文件名；稳定产品标识应主动设置 |
| 属性 | `setApplicationName(const QString &)` | 设置应用名称 | 在创建 `QSettings`、命令行解析器等消费者前设置 |
| 信号 | `applicationNameChanged()` | 应用名称改变时发出 | 用于依赖名称的动态 UI 或服务；普通程序很少需要监听 |
| 属性 | `applicationVersion()` | 返回应用版本字符串 | 不做版本比较；比较版本请用结构化版本数据 |
| 属性 | `setApplicationVersion(const QString &)` | 设置应用版本字符串 | 尽早设置，便于帮助文本、诊断和日志使用 |
| 信号 | `applicationVersionChanged()` | 应用版本改变时发出 | 多数程序只在启动时设置一次 |
| 属性 | `organizationName()` | 返回组织名称 | 影响默认设置存储位置 |
| 属性 | `setOrganizationName(const QString &)` | 设置组织名称 | 与组织域名一起在访问 `QSettings` 前设定 |
| 信号 | `organizationNameChanged()` | 组织名称改变时发出 | 适合动态配置工具，普通桌面程序通常不需要 |
| 属性 | `organizationDomain()` | 返回组织域名 | 常用于标识组织，非 DNS 校验接口 |
| 属性 | `setOrganizationDomain(const QString &)` | 设置组织域名 | 在创建默认 `QSettings` 前设置，避免配置落到意外位置 |
| 信号 | `organizationDomainChanged()` | 组织域名改变时发出 | 仅在运行时允许改组织配置时才有价值 |
| 属性 | `isQuitLockEnabled()` | 查询 quit lock 是否有效 | 关系到 `QEventLoopLocker` 对自动退出的影响 |
| 属性 | `setQuitLockEnabled(bool)` | 启用或禁用 quit lock | 不要以此替代显式退出协议 |
| 全局状态 | `instance()` | 返回当前应用实例，没有时返回空指针 | 不拥有返回指针；构造前和析构后可能为空 |
| 全局状态 | `instanceExists()` | 判断是否存在应用实例 | Qt 6.11 头文件提供；用于库中避免在无应用环境访问全局实例 |
| 全局状态 | `startingUp()` | 判断 Qt 应用是否仍在启动阶段 | 面向底层集成代码，普通业务很少需要 |
| 全局状态 | `closingDown()` | 判断应用对象是否正在或已经销毁 | 不能据此挽救已经失效的 QObject 指针 |
| 进程 | `applicationPid()` | 返回当前进程 ID | 适合日志、单实例协调；不是跨平台进程管理 API |
| 属性 | `setAttribute(Qt::ApplicationAttribute, bool)` | 设置 Qt 全局应用属性 | 很多属性必须在创建应用对象前设定；逐项查属性文档 |
| 属性 | `testAttribute(Qt::ApplicationAttribute)` | 查询某个 Qt 全局应用属性 | 查询的是 Qt 属性，不等同于操作系统能力检测 |

### 11.2 事件循环与退出

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 主循环 | `exec()` | 启动主线程事件循环并返回退出码 | 通常作为 `main()` 最后一行；清理优先连接 `aboutToQuit()` |
| 主循环 | `processEvents(QEventLoop::ProcessEventsFlags)` | 临时处理当前线程待处理事件 | 会带来重入；不能用作长期异步架构 |
| 主循环 | `processEvents(flags, int ms)` | 在时间预算内临时处理事件 | Qt 6.7 起转向 deadline 语义；仍有重入风险 |
| 主循环 | `processEvents(flags, QDeadlineTimer deadline)` | 处理事件直到达到给定 deadline | 适合低层循环集成；不要把它当作取消或线程模型 |
| 退出槽 | `quit()` | 请求以退出码 0 结束主事件循环 | 线程安全；最常用的正常退出入口 |
| 退出槽 | `exit(int retcode = 0)` | 指定退出码并结束事件循环 | 非线程安全，只在主线程、事件循环运行后调用 |
| 信号 | `aboutToQuit()` | Qt 即将退出主事件循环时发出 | 用来收尾；不要假定 `exec()` 后的代码必定可执行 |
| 事件循环 | `QEventLoopLocker`（相关类） | 暂时阻止自动退出 | 只保护明确短暂的关键活动，生命周期要清楚 |

### 11.3 QObject 事件投递和派发

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 同步事件 | `sendEvent(QObject *, QEvent *)` | 立即把事件发送给接收者 | 不转移所有权；在调用线程执行，不能借此跨线程调用对象 |
| 异步事件 | `postEvent(QObject *, QEvent *, int priority)` | 把事件排入接收者线程队列 | 转移事件所有权，必须传堆对象；调用后不能再访问事件 |
| 队列维护 | `sendPostedEvents(QObject * = nullptr, int type = 0)` | 立即分发已投递事件 | 必须在接收者线程调用；不应用于常规 UI 刷新 |
| 队列维护 | `removePostedEvents(QObject *, int eventType = 0)` | 移除还未处理的投递事件 | 线程安全但危险；绝不要以 `0` 批量删除全部事件 |
| 派发 | `notify(QObject *, QEvent *)` | 将 Qt 事件分发给对象，可由派生类重写 | 全局影响大；Qt 7 不再处理主线程外对象的事件 |
| 保护函数 | `event(QEvent *)` | 处理发给应用对象自身的事件 | 仅在派生应用类确有需要时重写，并保留基类行为 |
| 原生事件 | `installNativeEventFilter(QAbstractNativeEventFilter *)` | 安装操作系统原生消息过滤器 | 平台相关；优先用 `QObject::installEventFilter()` |
| 原生事件 | `removeNativeEventFilter(QAbstractNativeEventFilter *)` | 移除已安装的原生事件过滤器 | 移除后确认过滤器对象不会再被其它机制使用 |
| 分发器 | `eventDispatcher()` | 返回主线程当前事件分发器 | 不拥有返回指针；面向底层事件循环集成 |
| 分发器 | `setEventDispatcher(QAbstractEventDispatcher *)` | 设置主线程事件分发器 | 必须在创建应用对象前调用；应用接管传入对象所有权 |

### 11.4 启动参数、路径与插件库路径

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 参数 | `arguments()` | 返回应用启动参数 | 某些平台开销相对高，重复使用应缓存；解析选项请用 `QCommandLineParser` |
| 路径 | `applicationDirPath()` | 返回可执行文件所在目录 | 不等于当前工作目录；Linux 回退 `argv[0]` 时受工作目录变化影响 |
| 路径 | `applicationFilePath()` | 返回可执行文件完整路径 | 与部署、软链接和平台实现有关，不能替代资源系统 |
| 插件路径 | `libraryPaths()` | 返回 Qt 当前插件库搜索路径 | 在应用对象创建后查询才有意义；环境变量和 `qt.conf` 可影响结果 |
| 插件路径 | `setLibraryPaths(const QStringList &)` | 完全替换插件库搜索路径 | 易破坏平台插件发现；只用于受控部署 |
| 插件路径 | `addLibraryPath(const QString &)` | 将目录加入插件搜索路径前部 | 路径优先级提高；不要加入不受信任目录 |
| 插件路径 | `removeLibraryPath(const QString &)` | 移除一个插件搜索路径 | 需确认不会影响已经依赖该目录的延迟加载插件 |

### 11.5 翻译与权限

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 翻译 | `installTranslator(QTranslator *)` | 安装翻译器，供 `tr()` 与 `translate()` 查询 | 不接管翻译器所有权；最后安装者优先，翻译器必须持续存活 |
| 翻译 | `removeTranslator(QTranslator *)` | 卸载已安装的翻译器 | 语言切换后让界面处理 `QEvent::LanguageChange` 并重译 |
| 翻译 | `translate(const char *context, const char *key, const char *disambiguation = nullptr, int n = -1)` | 按上下文查译文 | 线程安全；`n` 用于复数规则，找不到时返回源文本 |
| 权限 | `checkPermission(const QPermission &)` | 查询权限当前状态 | Qt 6.5 起可用；结果受平台能力和系统策略影响 |
| 权限 | `requestPermission(const QPermission &, const QObject *context, Functor)` | 异步请求权限并在 context 线程回调 | 必须从主线程请求；context 销毁则不调用回调 |
| 权限 | `requestPermission(const QPermission &, Functor)` | 异步请求权限，不绑定 context | 避免捕获可能销毁的对象；更推荐带 context 的版本 |

### 11.6 平台、安全和初始化辅助

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 安全 | `setSetuidAllowed(bool)` | 允许或拒绝 Unix setuid 程序使用 Qt | 必须在构造应用对象前调用；开启前应完成安全审计 |
| 安全 | `isSetuidAllowed()` | 查询是否允许 setuid 使用 Qt | 仅与 Unix setuid 场景相关 |
| 启动例程 | `qAddPreRoutine(QtStartUpFunction)` | 注册在应用构造前执行的函数 | 底层库初始化接口；避免依赖尚不存在的应用对象 |
| 结束例程 | `qAddPostRoutine(QtCleanUpFunction)` | 注册应用析构时执行的清理函数 | 后注册先执行；动态模块卸载前须移除或避免注册 |
| 结束例程 | `qRemovePostRoutine(QtCleanUpFunction)` | 取消一个 post routine | 用于避免调用已卸载模块中的函数 |
| 宏 | `Q_COREAPP_STARTUP_FUNCTION(function)` | 注册应用构造末尾、GUI 初始化前的启动函数 | 静态库代码可能被链接器裁剪；不替代明确初始化 |
| 宏 | `Q_DECLARE_TR_FUNCTIONS(context)` | 为非 `QObject` 类生成静态 `tr()` | 必须放在首个访问说明符前，翻译上下文使用传入名称 |
| 宏 | `qApp` | 当前 `QCoreApplication` 实例的快捷宏 | 应用尚未创建或正在销毁时不可假定它有效 |

## 12. 一个小型控制台任务的完整骨架

下面的例子演示了实际项目更常见的组织方式：先配置应用身份，启动一个异步任务，在关闭信号中统一收尾。

```cpp
#include <QCommandLineParser>
#include <QCoreApplication>
#include <QTimer>

class ImportController : public QObject
{
    Q_OBJECT
public:
    using QObject::QObject;

    void start()
    {
        QTimer::singleShot(0, this, [this] {
            // 此处可替换成网络、进程或工作线程完成后的逻辑。
            emit finished(0);
        });
    }

signals:
    void finished(int exitCode);
};

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);
    QCoreApplication::setOrganizationName("Example Studio");
    QCoreApplication::setApplicationName("import-tool");
    QCoreApplication::setApplicationVersion("1.0.0");

    QCommandLineParser parser;
    parser.addHelpOption();
    parser.addVersionOption();
    parser.process(app);

    ImportController controller;
    QObject::connect(&controller, &ImportController::finished,
                     &app, [](int code) {
        QCoreApplication::exit(code);
    });
    QObject::connect(&app, &QCoreApplication::aboutToQuit,
                     &controller, [] {
        // 在此处停止尚未完成的异步资源。
    });

    controller.start();
    return app.exec();
}
```

这个骨架的重点不是“所有控制台程序都必须这样写”，而是把三件事分开：应用级配置在启动期完成，业务任务由对象管理，退出动作回到应用对象。这样将来添加线程、网络请求、超时和取消机制时，不会把生命周期散落在 `main()` 的各个角落。
