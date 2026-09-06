# QCoreApplication

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QCoreApplication` 是无 GUI Qt 程序的应用对象，负责初始化 Qt、保存全局应用状态并驱动主事件循环。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QCoreApplication` 是无 GUI Qt 程序的应用对象，负责初始化 Qt、保存全局应用状态并驱动主事件循环。

**内部模型：** Qt 的异步能力都依赖事件循环：信号投递、定时器、网络、文件系统监视和 queued connection 都需要它分发事件。`exec()` 返回前，应用通常一直运行。

**适用场景：** 命令行工具、服务、后台任务或不需要窗口的 Qt 程序使用它；Widgets 程序应使用 QApplication，使用窗口系统但不使用 Widgets 的程序使用 QGuiApplication。

**典型调用链：** 构造应用对象 -> 创建需要事件循环的对象 -> 连接退出条件 -> 调用 exec() -> 在 finished/quit 后返回并析构。

**先记住的坑：** 一个进程通常只创建一个应用对象；没有调用 exec() 时异步对象通常不会按预期工作；不要在事件循环线程执行长时间阻塞任务。

## 2. 依赖与对象关系

- 头文件：`#include <QCoreApplication>`
- 继承自：QObject
- 直接派生类：QAndroidService、QGuiApplication

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

Qt 的异步能力都依赖事件循环：信号投递、定时器、网络、文件系统监视和 queued connection 都需要它分发事件。`exec()` 返回前，应用通常一直运行。

### 状态、生命周期和线程

**生命周期：** 先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

**状态与结果：** QObject 派生对象的状态通常通过属性、状态查询函数和信号变化共同表达。信号是通知，不是返回值；收到通知后应读取当前状态并处理异常路径，不能假设每个信号只会出现一次。

**线程与事件循环：** QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

## 3. 直接使用

命令行工具、服务、后台任务或不需要窗口的 Qt 程序使用它；Widgets 程序应使用 QApplication，使用窗口系统但不使用 Widgets 的程序使用 QGuiApplication。 使用时通常按这个过程组织：构造应用对象 -> 创建需要事件循环的对象 -> 连接退出条件 -> 调用 exec() -> 在 finished/quit 后返回并析构。

```cpp
#include <QCoreApplication>
#include <QTimer>

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);
    QTimer::singleShot(1000, &app, &QCoreApplication::quit);
    return app.exec();
}
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 属性

- `applicationName : QString`
- `applicationVersion : QString`
- `organizationDomain : QString`
- `organizationName : QString`
- `quitLockEnabled : bool`

### 公有函数

- `QCoreApplication(int &argc, char **argv)`
- `virtual ~QCoreApplication()`
- `(since 6.5) Qt::PermissionStatus checkPermission(const QPermission &permission)`
- `void installNativeEventFilter(QAbstractNativeEventFilter *filterObj)`
- `virtual bool notify(QObject *receiver, QEvent *event)`
- `void removeNativeEventFilter(QAbstractNativeEventFilter *filterObject)`
- `(since 6.5) void requestPermission(const QPermission &permission, Functor &&functor)`
- `(since 6.5) void requestPermission(const QPermission &permission, const QObject *context, Functor functor)`

### 公有槽函数

- `void exit(int returnCode = 0)`
- `void quit()`

### 信号

- `void aboutToQuit()`
- `void applicationNameChanged()`
- `void applicationVersionChanged()`
- `void organizationDomainChanged()`
- `void organizationNameChanged()`

### 静态公有成员

- `void addLibraryPath(const QString &path)`
- `QString applicationDirPath()`
- `QString applicationFilePath()`
- `QString applicationName()`
- `qint64 applicationPid()`
- `QString applicationVersion()`
- `QStringList arguments()`
- `bool closingDown()`
- `QAbstractEventDispatcher * eventDispatcher()`
- `int exec()`
- `bool installTranslator(QTranslator *translationFile)`
- `QCoreApplication * instance()`
- `bool isQuitLockEnabled()`
- `bool isSetuidAllowed()`
- `QStringList libraryPaths()`
- `QString organizationDomain()`
- `QString organizationName()`
- `void postEvent(QObject *receiver, QEvent *event, int priority = Qt::NormalEventPriority)`
- `void processEvents(QEventLoop::ProcessEventsFlags flags = QEventLoop::AllEvents)`
- `(since 6.7) void processEvents(QEventLoop::ProcessEventsFlags flags, QDeadlineTimer deadline)`
- `void processEvents(QEventLoop::ProcessEventsFlags flags, int ms)`
- `void removeLibraryPath(const QString &path)`
- `void removePostedEvents(QObject *receiver, int eventType = 0)`
- `bool removeTranslator(QTranslator *translationFile)`
- `bool sendEvent(QObject *receiver, QEvent *event)`
- `void sendPostedEvents(QObject *receiver = nullptr, int event_type = 0)`
- `void setApplicationName(const QString &application)`
- `void setApplicationVersion(const QString &version)`
- `void setAttribute(Qt::ApplicationAttribute attribute, bool on = true)`
- `void setEventDispatcher(QAbstractEventDispatcher *eventDispatcher)`
- `void setLibraryPaths(const QStringList &paths)`
- `void setOrganizationDomain(const QString &orgDomain)`
- `void setOrganizationName(const QString &orgName)`
- `void setQuitLockEnabled(bool enabled)`
- `void setSetuidAllowed(bool allow)`
- `bool startingUp()`
- `bool testAttribute(Qt::ApplicationAttribute attribute)`
- `QString translate(const char *context, const char *sourceText, const char *disambiguation = nullptr, int n = -1)`

### 重实现的保护函数

- `virtual bool event(QEvent *e) override`

### 相关非成员函数

- `void qAddPostRoutine(QtCleanUpFunction ptr)`
- `void qRemovePostRoutine(QtCleanUpFunction ptr)`

### 公开宏

- `Q_COREAPP_STARTUP_FUNCTION(QtStartUpFunction ptr)`
- `Q_DECLARE_TR_FUNCTIONS(context)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `applicationName : QString`

**作用与语义：**

该属性保存此应用程序的名称。
应用程序名称在各种 Qt 类和模块中使用，最重要的是在使用默认构造函数构造 `QSettings` 时使用。其他用途包括格式化日志输出（参见 `qSetMessagePattern()`）、`QCommandLineParser` 输出、`QTemporaryDir` 和 `QTemporaryFile` 默认路径，以及 `QStandardPaths` 的某些文件位置。Qt D-Bus、无障碍功能和 XCB 平台集成都使用应用程序名称。
如果未设置，应用程序名称默认为可执行文件名称。

**如何使用：** 调用 `applicationName()` 读取当前值；它不会修改应用状态。

### `applicationVersion : QString`

**作用与语义：**

该属性表示该应用的版本。
如果未设置，应用版本默认为主应用程序可执行文件或包中确定的平台特定值（自Qt 5.9起）：
- `Platform`：来源
- `Windows (classic desktop)`：VERSIONINFO 资源的 PRODUCTVERSION 参数
- `macOS, iOS, tvOS, watchOS`：信息属性列表的CFBundleVersion属性
- `Android`：AndroidManifest.xml manifest 元素的 android：versionName 属性
在其他平台上，默认字符串是空字符串。

**如何使用：** 调用 `applicationVersion()` 读取当前值；它不会修改应用状态。

### `organizationDomain : QString`

**作用与语义：**

该属性拥有编写本申请的组织的互联网域名。
`QSettings`类在使用默认构造函数构造时使用该值。这样就不用每次创建`QSettings`对象时重复这些信息。
在 Mac 上，如果组织不是空字符串，`QSettings` 使用 organizationDomain() 作为组织;否则使用 `organizationName()`。在所有其他平台上，`QSettings` 使用 `organizationName()` 作为组织。

**如何使用：** 调用 `organizationDomain()` 读取当前值；它不会修改应用状态。

### `organizationName : QString`

**作用与语义：**

该属性保存编写此应用程序的组织名称。
该值在使用默认构造函数构造 `QSettings` 类时使用。这避免了每次创建 `QSettings` 对象时重复提供此信息。
在 Mac 上，如果 `QSettings` 的字符串不为空，它会使用 `organizationDomain()` 作为组织；否则使用 organizationName()。在其他所有平台上，`QSettings` 使用 organizationName() 作为组织。

**如何使用：** 调用 `organizationName()` 读取当前值；它不会修改应用状态。

### `quitLockEnabled : bool`

**作用与语义：**

该属性决定使用`QEventLoopLocker`特性是否会导致应用程序退出。
当该属性被`true`时，应用程序中最后剩余的运行`QEventLoopLocker`的释放将尝试退出应用程序。
注意，尝试退出不一定会导致应用程序退出，例如如果仍有开启窗口，或者`QEvent::Quit`事件被忽略。
默认是`true`。

**如何使用：** 调用 `quitLockEnabled()` 读取当前值；它不会修改应用状态。

### `QCoreApplication::QCoreApplication(int &argc, char **argv)`

**作用与语义：**

构建Qt核心应用程序。核心应用程序是没有图形用户界面的应用程序。此类应用程序可在控制台或服务器进程中使用。
应用程序处理`argc`和`argv`参数，并由`arguments()`函数以更便捷的形式提供。
警告：`argc` 和 `argv` 所引用的数据必须在 QCoreApplication 对象的整个生命周期内保持有效。此外，`argc`必须大于零，且`argv`必须至少包含一个有效的字符串。

### `[virtual noexcept] QCoreApplication::~QCoreApplication()`

**作用与语义：**

摧毁`QCoreApplication`物体。

### `[private signal] void QCoreApplication::aboutToQuit()`

**作用与语义：**

当应用程序即将退出主事件循环时，例如事件循环级别降至零时，会发出该信号。这可能发生在应用程序内部调用`quit()`后，或用户关闭整个桌面会话时。
当你的应用程序需要在最后一刻进行清理时，这个信号尤其有用。请注意，在此状态下无法进行用户交互。
注意：此时主事件循环仍在运行，但返回时不会处理其他事件，除了通过`deleteLater()`删除的对象处理`QEvent::DeferredDelete`事件。如果需要处理事件，可以使用嵌套事件循环或手动调用`QCoreApplication::processEvents()`。
注意：这是一个私有信号。它可以用于信号连接，但用户不能发射。

### `[static] void QCoreApplication::addLibraryPath(const QString &path)`

**作用与语义：**

`path`在库路径列表的开头前加，确保先搜索库。如果`path`空或已在路径列表中，路径列表不会被更改。
默认路径列表由一到两个条目组成。第一个是插件安装目录，称为`INSTALL/plugins`，其中 `INSTALL` 是 Qt 安装的目录。第二个是应用程序自身的目录（不是当前目录），但仅在`QCoreApplication`对象实例化后才会显示。
当 `QCoreApplication` 实例被摧毁时，库路径会重置为默认状态。

### `[static] QString QCoreApplication::applicationDirPath()`

**作用与语义：**

返回包含应用可执行文件的目录。
例如，如果你在`C:\Qt`目录安装了 Qt，并运行`regexp`示例，这个函数会返回“C：/Qt/examples/tools/regexp”。
在macOS和iOS上，这会指向实际包含可执行文件的目录，这个目录可能在应用捆绑包内（如果应用是捆绑的话）。
在 Android 上，这会指向实际包含可执行文件的目录，这个目录可能在应用 APK 内部（如果它是支持无压缩库构建的）。
警告：在 Linux 上，该函数会尝试从 `/proc` 文件系统获取路径。如果失败，它假设 `argv[0]` 包含可执行文件的绝对文件名。该函数还假设当前目录未被应用程序更改。

### `[static] QString QCoreApplication::applicationFilePath()`

**作用与语义：**

返回应用程序可执行文件的文件路径。
例如，如果你在`/usr/local/qt`目录中安装了Qt，并运行`regexp`示例，这个函数会返回“/usr/local/qt/examples/tools/regexp/regexp”。
警告：在 Linux 上，该函数会尝试从 `/proc` 文件系统获取路径。如果失败，它会假设 `argv[0]` 包含可执行文件的绝对文件名。该函数还假设当前目录未被应用程序更改。

### `[static noexcept] qint64 QCoreApplication::applicationPid()`

**作用与语义：**

返回应用程序的当前进程 ID。

### `[static] QStringList QCoreApplication::arguments()`

**作用与语义：**

返回命令行参数列表。
通常，arguments().at（0） 是程序名，arguments().at（1） 是第一个参数，arguments().last() 是最后一个参数。请参见下方关于 Windows 的说明。
调用这个函数很慢——解析命令行时你应该把结果存到变量里。
警告：在 Unix 上，此列表由 main() 函数中传递给构造函数的 argc 和 argv 参数构建而成。argv 中的字符串数据通过 `QString::fromLocal8Bit()` 解释;因此，例如，无法在运行于 Latin1 区域的系统上传递日文命令行参数。大多数现代 Unix 系统没有此限制，因为它们基于 Unicode。
在Windows上，只有当修改后的argv/argc参数传递给构造函数时，列表才会从argc和argv参数构建。在这种情况下，可能会出现编码问题。
否则，参数()由GetCommandLine()的返回值构造而来。因此，arguments().at（0） 给出的字符串可能不是Windows上启动应用程序的确切程序。

### `[since 6.5] Qt::PermissionStatus QCoreApplication::checkPermission(const QPermission &permission)`

**作用与语义：**

检查给定的状态`permission`。
如果结果`Qt::PermissionStatus::Undetermined`，则应通过`requestPermission()`请求许可以确定用户意图。

### `[static] bool QCoreApplication::closingDown()`

**作用与语义：**

如果应用对象正在被销毁，返回`true`;否则返回`false`。

### `[override virtual protected] bool QCoreApplication::event(QEvent *e)`

**作用与语义：**

重实现自：`QObject::event`（QEvent *e）。
该虚拟函数接收对象事件，如果事件`e`被识别并处理，应返回真。
event() 函数可以重新实现，以自定义对象的行为。
确保你调用所有未处理的事件的父事件类实现。

### `[static] QAbstractEventDispatcher *QCoreApplication::eventDispatcher()`

**作用与语义：**

返回主线程事件调度器对象的指针。如果线程不存在事件调度器，该函数返回`nullptr`。

### `[static] int QCoreApplication::exec()`

**作用与语义：**

进入主事件循环，等待`exit()`被调用。返回传递给`exit()`的值（如果通过`quit()`调用`exit()`则为0）。
启动事件处理需要调用该函数。主事件循环接收来自窗口系统的事件，并将其分发给应用控件。
要让你的应用程序执行空闲处理（在没有待处理事件时执行特殊函数），可以使用超时为0ns的`QChronoTimer`。更高级的空闲处理方案可以通过`processEvents()`实现。
我们建议你将清理代码连接到`aboutToQuit()`信号，而不是放在应用程序的`main()`函数中，因为在某些平台上exec()调用可能不会返回。例如，在Windows上，当用户登出时，系统会在Qt关闭所有顶层窗口后终止进程。因此，无法保证应用程序在exec()调用后，有时间退出事件循环并在`main()`函数结束时执行代码。

### `[static slot] void QCoreApplication::exit(int returnCode = 0)`

**作用与语义：**

告诉应用程序用返回码退出。
调用该函数后，应用程序离开主事件循环，返回调用`exec()`。`exec()`函数返回`returnCode`。如果事件循环未运行，该函数不做任何操作。
按照惯例，`returnCode`为0表示成功，任何非零值表示错误。
使用`QueuedConnection`连接该槽函数时，始终是良好做法。如果在控制进入主事件环路之前（例如“int main”调用`exec()`之前）发出与该槽函数连接（非排队）信号，该槽函数无效，应用程序永远不会退出。使用队列连接确保该槽函数直到控制进入主事件环路后才会被调用。
注意，与同名的 C 库函数不同，该函数会返回调用者——停止的是事件处理。
还要注意，该函数并非线程安全。它应仅从主线程（`QCoreApplication`对象处理事件的线程）调用。要请求应用程序退出其他线程，可以使用`QCoreApplication::quit()`，或者用 QMetaMethod：：invokeMethod() 从主线程调用该函数。

### `void QCoreApplication::installNativeEventFilter(QAbstractNativeEventFilter *filterObj)`

**作用与语义：**

安装一个事件过滤器`filterObj`，用于主线程中应用程序接收的所有本地事件。
事件过滤器`filterObj`通过其`nativeEventFilter()`函数接收事件，该函数会调用主线程中所有本地事件。
如果事件需要被过滤，即停止事件，`QAbstractNativeEventFilter::nativeEventFilter()`函数应返回true。它应返回false以允许正常的Qt处理继续：本地事件随后可以转换为`QEvent`，并由标准Qt `event`过滤处理，例如`QObject::installEventFilter()`。
如果安装了多个事件过滤器，最后安装的过滤器会先被激活。
注意：这里的过滤函数集接收本地消息、i.e. MSG或XCB事件结构。
注意：当`Qt::AA_PluginApplication`属性设置时，应用程序中将禁用本地事件过滤器。
为了最大化便携性，你应尽量使用`QEvent`和`QObject::installEventFilter()`。

### `[static] bool QCoreApplication::installTranslator(QTranslator *translationFile)`

**作用与语义：**

将翻译文件`translationFile`添加到用于翻译的翻译文件列表中。
可以安装多个翻译文件。翻译按安装顺序倒序搜索，因此先搜索最近安装的翻译文件，最后搜索第一个安装的翻译文件。一旦找到包含匹配字符串的翻译，搜索即停止。
安装或移除`QTranslator`，或更改已安装的`QTranslator`，都会为`QCoreApplication`实例生成一个`LanguageChange`事件。`QApplication`实例会将事件传播到所有顶层控件，在这些节点上，changeEvent的重新实现可以通过`tr()`函数将用户可见的字符串传递给相应的属性设置器，重新转换用户界面。Qt Widgets Designer生成的用户界面类提供了一个可调用的`retranslateUi()`函数。
函数成功时返回`true`，失败时返回`false`。
注意：`QCoreApplication`不对`translationFile`拥有权。应用程序有责任确保如果函数返回`true`，`translationFile`对象在调用`removeTranslator()`或应用程序退出前仍然存在。

### `[static noexcept] QCoreApplication *QCoreApplication::instance()`

**作用与语义：**

返回指向应用程序`QCoreApplication`（或`QGuiApplication`/`QApplication`）实例的指针。
如果没有实例被分配，`nullptr`会返回。

### `[static] bool QCoreApplication::isSetuidAllowed()`

**作用与语义：**

如果应用程序被允许在 UNIX 平台上运行 setuid，则返回为真。

### `[static] QStringList QCoreApplication::libraryPaths()`

**作用与语义：**

返回一份路径列表，应用程序在动态加载库时将搜索这些路径。
创建`QCoreApplication`时，该函数的返回值可能会发生变化。不建议在创建`QCoreApplication`前调用该函数。如果已知应用可执行文件目录（而非工作目录）将成为列表的一部分。为了使其已知，必须构建一个`QCoreApplication`，因为它会使用`argv[0]`来查找该文件。
Qt 提供默认库路径，但也可以通过 qt.conf 文件设置。该文件中指定的路径会覆盖默认值。注意，如果 qt.conf 文件位于应用程序可执行文件的目录中，可能要等创建`QCoreApplication`才能找到。如果调用该函数时找不到，则使用默认库路径。
如果插件安装目录存在，列表将包含（插件默认安装目录为 `INSTALL/plugins`，其中 Qt 的安装目录为 `INSTALL`）。环境变量`QT_PLUGIN_PATH`的冒号分隔条目总是被添加。插件安装目录（及其存在）可能会在应用可执行文件目录已知时发生变化。

### `[virtual] bool QCoreApplication::notify(QObject *receiver, QEvent *event)`

**作用与语义：**

发送`event`到`receiver`：`receiver`->event（`event`）。返回接收方事件处理器返回的值。注意，该函数被调用用于发送到任意线程中任意对象的所有事件。
对于某些类型的事件（例如鼠标和键事件），如果接收方对事件不感兴趣（即返回`false`），事件会传播到接收方的父对象，依此类推直到顶层对象。
事件处理方式有五种;重新实现该虚拟功能只是其中之一。以下列出了所有五种方法：
- 重新实现`paintEvent()`、`mousePressEvent()`等。这是最常见、最简单且最不强大的方式。
- 重新实现该功能。这非常强大，提供完全控制;但一次只能激活一个子类。
- 在`QCoreApplication::instance()`上安装事件过滤器。这样的事件过滤器能够处理所有控件的所有事件，因此它的强大功能与重新实现 notify(); 一样强大。此外，还可以设置多个应用全局事件过滤器。全局事件过滤器甚至能识别禁用控件的鼠标事件。注意，应用程序事件过滤器只调用存在主线程中的对象。
- 重新实现`QObject::event()`（正如`QWidget`所做的那样）。这样做时，你会获得Tab键的点击，并且可以在任何针对小部件的事件筛选之前看到事件。
- 在对象上安装事件过滤器。此类事件过滤器接收所有事件，包括Tab和Shift按键，只要不改变焦点控件。
未来方向：在Qt 7中，对于主线程外的对象，该函数将不再调用。需要该功能的应用程序应在此期间寻找其他事件检查解决方案。该变更可能会扩展到主线程，导致该函数被弃用。
警告：如果你覆盖了该函数，必须确保所有处理事件的线程在你的应用对象开始销毁前停止处理事件。这包括你可能正在使用的其他库启动的线程，但不适用于 Qt 自身的线程。

### `[static] void QCoreApplication::postEvent(QObject *receiver, QEvent *event, int priority = Qt::NormalEventPriority)`

**作用与语义：**

将事件`event`，`receiver`对象作为事件接收方，添加到事件队列中并立即返回。
事件必须被分配到堆上，因为事件发布队列会接管事件所有权并删除事件。事件发布后访问事件是不安全的。
当控制返回主事件循环时，队列中存储的所有事件将通过`notify()`函数发送。
事件按`priority`级排序，即`priority`较高的事件排队于`priority`较低的事件之前。`priority`可以是任意整数值，即介于INT_MAX到INT_MIN之间，含;详见 `Qt::EventPriority` 详情。`priority`相等的事件将按发布的顺序处理。
注意：`QObject::deleteLater()` 将对象调度为延迟删除，通常由接收端的事件循环处理。如果线程中没有事件循环运行，删除将在线程结束时执行。一个常见且安全的模式是将线程的 finished() 信号连接到对象的 `deleteLater()` 槽：
注意：该功能是线程安全的。

**官方示例：**

```cpp
 QObject::connect(thread, &QThread::finished, worker, &QObject::deleteLater);
```

### `[static] void QCoreApplication::processEvents(QEventLoop::ProcessEventsFlags flags = QEventLoop::AllEvents)`

**作用与语义：**

根据指定`flags`处理调用线程的一些待处理事件。
不建议使用该函数。相反，建议将长操作从图形界面线程移到辅助线程，完全避免嵌套事件循环处理。如果事件处理确实必要，建议使用`QEventLoop`。
如果你运行的是一个本地循环，连续调用该函数，没有事件循环，`DeferredDelete`事件将不会被处理。这会影响依赖`DeferredDelete`事件正常工作的控件，例如`QToolTip`。另一种方法是从该本地循环中调用`sendPostedEvents()`。
调用该函数只处理调用线程的事件，处理完所有可用事件后返回。可用事件是在函数调用之前排队的。这意味着在函数运行时发布的事件会被排队，直到后续的事件处理轮次。
注意：该功能是线程安全的。

### `[static, since 6.7] void QCoreApplication::processEvents(QEventLoop::ProcessEventsFlags flags, QDeadlineTimer deadline)`

**作用与语义：**

调用线程未瓦片`deadline`的待处理事件已过期，或直到没有更多事件可处理，以先发生者为准。
不建议使用该函数。相反，更倾向于将长操作从GUI线程中移到辅助线程，并完全避免嵌套事件循环处理。如果事件处理确实必要，可以考虑使用`QEventLoop`。
调用该函数只处理调用线程的事件。
注意：与`processEvents()`重载不同，该函数还处理在运行时发布的事件。
注意：所有在超时前排队的事件都会被处理，无论需要多长时间。
注意：该功能是线程安全的。

### `[static] void QCoreApplication::processEvents(QEventLoop::ProcessEventsFlags flags, int ms)`

**作用与语义：**

处理调用线程的待处理事件，时间为`ms`毫秒或直到没有更多事件可处理，以较短者为准。
这等同于调用：

**官方示例：**

```cpp
 QCoreApplication::processEvents(flags, QDeadlineTimer(ms));
```

### `[static slot] void QCoreApplication::quit()`

**作用与语义：**

要求申请人退出。
如果应用程序阻止退出，例如某个窗口无法关闭，请求可能会被忽略。应用程序可以通过在应用层面处理`QEvent::Quit`事件，或为单个窗口处理`QEvent::Close`事件来影响这一点。
如果退出未被中断，应用程序将以返回码 0（成功）退出。
为了避免被中断地退出应用程序，直接调用`exit()`。注意该方法不支持线程安全。
使用该槽函数连接信号时使用`QueuedConnection`是良好习惯。如果在控制进入主事件循环前（例如“int main”调用`exec()`之前）发出连接（非排队）的信号，该槽函数无效，应用程序永远不会退出。使用队列连接确保该槽函数直到控制进入主事件循环后才会被调用。
线程安全说明：该函数可从任意线程调用线程安全，导致当前运行的主应用循环退出。但如果`QCoreApplication`对象同时被摧毁，线程安全无法保证。
注意：该功能是线程安全的。

**官方示例：**

```cpp
 QPushButton *quitButton = new QPushButton("Quit");
 QObject::connect(quitButton, &QPushButton::clicked, &app, &QCoreApplication::quit, Qt::QueuedConnection);
```

### `[static] void QCoreApplication::removeLibraryPath(const QString &path)`

**作用与语义：**

从库路径列表中移除`path`。如果`path`空或不在路径列表中，列表不会被更改。
当`QCoreApplication`实例被摧毁时，库路径会重置为默认状态。

### `void QCoreApplication::removeNativeEventFilter(QAbstractNativeEventFilter *filterObject)`

**作用与语义：**

从该对象中移除事件`filterObject`。如果未安装此类事件过滤器，请求将被忽略。
当该对象被销毁时，所有针对该对象的事件过滤器都会自动移除。
即使在事件过滤器激活期间（即从nativeEventFilter()函数中移除事件过滤器，也总是安全的。

### `[static] void QCoreApplication::removePostedEvents(QObject *receiver, int eventType = 0)`

**作用与语义：**

删除所有使用`postEvent()`发布的`eventType`事件`receiver`。
事件不会被调度，而是从队列中移除。你永远不需要调用这个函数。如果你调用它，请注意，杀死事件可能导致`receiver`破坏一个或多个不变量。
如果`receiver`为`nullptr`，则所有对象的`eventType`事件将被移除。如果`eventType`为0，则所有`receiver`事件均被移除。你绝不应以`eventType`为0的状态调用该函数。
注意：该功能是线程安全的。

### `[static] bool QCoreApplication::removeTranslator(QTranslator *translationFile)`

**作用与语义：**

从该应用程序使用的翻译文件列表中移除`translationFile`翻译文件。（它不会从文件系统中删除翻译文件。）。
函数成功时返回`true`，失败时返回false。

### `[since 6.5] template <typename Functor> void QCoreApplication::requestPermission(const QPermission &permission, Functor &&functor)`

**作用与语义：**

请求给出的`permission`。
当请求准备好时，`functor`将被调用为`functor(const QPermission &permission)`，`permission`描述请求的结果。
`functor`可以是独立的或静态的成员函数：
或一个λ：
如果用户明确授予应用程序请求的`permission`，或者该`permission`已知在指定平台上不需要用户授权，状态将变为`Qt::PermissionStatus::Granted`。
如果用户明确拒绝应用请求的`permission`，或已知该`permission`无法访问或适用于该平台上的应用程序，状态将`Qt::PermissionStatus::Denied`。
请求的结果永远不会`Qt::PermissionStatus::Undetermined`。
注意：权限只能向主线程请求。

**官方示例：**

```cpp
 qApp->requestPermission(QCameraPermission{}, &permissionUpdated);
```

### `[since 6.5] template <typename Functor> void QCoreApplication::requestPermission(const QPermission &permission, const QObject *context, Functor functor)`

**作用与语义：**

请求给定的`permission`，在`context`语境下。
当请求准备好时，`functor`将被调用为`functor(const QPermission &permission)`，`permission`描述请求的结果。
`functor`可以是独立的或静态成员函数：
一个λ：
或者`context`对象上的一个槽：
`functor`将在`context`对象的线程中被调用。如果`context`在请求完成前被销毁，`functor`将不会被调用。
如果用户明确授予应用请求的`permission`，或该`permission`已知在该平台上不需要用户授权，状态将`Qt::PermissionStatus::Granted`。
如果用户明确拒绝应用请求的`permission`，或已知该`permission`无法访问或适用于该平台上的应用程序，状态将`Qt::PermissionStatus::Denied`。
请求的结果永远不会`Qt::PermissionStatus::Undetermined`。
注意：权限只能向主线程请求。

**官方示例：**

```cpp
 qApp->requestPermission(QCameraPermission{}, context, &permissionUpdated);
```

### `[static] bool QCoreApplication::sendEvent(QObject *receiver, QEvent *event)`

**作用与语义：**

使用`notify()`函数直接将事件`event`发送给接收方`receiver`。返回事件处理器返回的值。
事件发送后不会被删除。通常的做法是在栈上创建事件，例如：

**官方示例：**

```cpp
 QMouseEvent event(QEvent::MouseButtonPress, localPos, globalPos, Qt::LeftButton, Qt::LeftButton, Qt::NoModifier);
 QCoreApplication::sendEvent(mainWindow, &event);
```

### `[static] void QCoreApplication::sendPostedEvents(QObject *receiver = nullptr, int event_type = 0)`

**作用与语义：**

立即调度所有之前`QCoreApplication::postEvent()`已排队且为对象`receiver`且事件类型为`event_type`的事件。
窗口系统的事件不由该函数调度，而是由 `processEvents()` 调度。
如果`receiver`为`nullptr`，则`event_type`的事件将发送到所有对象。如果`event_type`为0，则所有事件都发送为`receiver`。
注意：该方法必须从其`QObject`参数`receiver`所在线程中调用。

### `[static] void QCoreApplication::setAttribute(Qt::ApplicationAttribute attribute, bool on = true)`

**作用与语义：**

如果 `on`为真，则将属性设为 `attribute`;否则则清除该属性。
注意：在创建`QCoreApplication`实例之前，必须设置部分应用属性。更多信息请参阅`Qt::ApplicationAttribute`文档。

### `[static] void QCoreApplication::setEventDispatcher(QAbstractEventDispatcher *eventDispatcher)`

**作用与语义：**

将主线程的事件调度器设置为`eventDispatcher`。这只有在尚未安装事件调度器的情况下才可行。也就是说，在`QCoreApplication`实例化之前。该方法会获得对象的所有权。

### `[static] void QCoreApplication::setLibraryPaths(const QStringList &paths)`

**作用与语义：**

在加载插件时设置目录列表，`QLibrary` 为 `paths`。所有现有路径将被删除，路径列表将由`paths`中给出的路径和应用路径组成。
当`QCoreApplication`实例被摧毁时，库路径会重置为默认状态。

### `[static] void QCoreApplication::setSetuidAllowed(bool allow)`

**作用与语义：**

如果`allow`为真，允许应用程序在 UNIX 平台上运行 setuid。
如果`allow`为假（默认值），且Qt检测到应用运行的有效用户ID与真实用户ID，则在创建`QCoreApplication`实例时应用将被中止。
由于 Qt 攻击面较大，不适合 setuid 程序。然而，由于历史原因，某些应用程序可能需要以这种方式运行。该标志将防止 Qt 在检测到此类情况下终止应用，且必须在创建 `QCoreApplication` 实例前设置。
注意：强烈建议不要启用此选项，因为它会引入安全风险。如果该应用程序启用了该标志并启动子进程，应尽早通过调用自身`setuid(2)`，或最迟使用QProcess：：UnixProcessParameters：：ResetIds标志来移除权限。

### `[static] bool QCoreApplication::startingUp()`

**作用与语义：**

如果应用对象尚未被创建，返回`true`;否则返回`false`。

### `[static] bool QCoreApplication::testAttribute(Qt::ApplicationAttribute attribute)`

**作用与语义：**

如果设置了属性`attribute`，返回`true`;否则返回`false`。

### `[static] QString QCoreApplication::translate(const char *context, const char *sourceText, const char *disambiguation = nullptr, int n = -1)`

**作用与语义：**

通过查询已安装的翻译文件返回翻译文本以供`sourceText`。翻译文件会从最近安装的文件回溯到第一个安装的文件。
`QObject::tr()`更方便地提供此功能。
`context`通常是类名（例如“MyDialog”），`sourceText`则是英文文本或简短的识别文本。
`disambiguation` 是一个识别字符串，用于同一上下文中相同 `sourceText` 在不同角色中使用。默认情况下，它是 `nullptr`。
请参阅 `QTranslator` 和 `QObject::tr()` 文档，了解更多关于上下文、消歧义和评论的信息。
`n`与`%n`结合使用以支持复数形式。详情请参见 `QObject::tr()`。
如果没有任何翻译文件包含`context`中`sourceText`的翻译，该函数返回的`QString`等价于`sourceText`。
这个函数不是虚拟的。你可以通过子类化`QTranslator`来使用替代的翻译技术。
注意：该功能是线程安全的。

### `void qAddPostRoutine(QtCleanUpFunction ptr)`

**作用与语义：**

添加一个全局例程，将从`QCoreApplication`结构化器中调用。该函数通常用于添加程序范围功能的清理例程。
清理程序按加法的倒序顺序调用。
`ptr`指定函数不应接受参数，且不应返回任何参数。例如：
注意，对于应用或模块范围的清理，qAddPostRoutine() 通常不适用。例如，如果程序被拆分为动态加载模块，相关模块可能在调用`QCoreApplication`解构器之前很久就被卸载。在这种情况下，如果仍希望使用 qAddPostRoutine() 使用，可以使用`qRemovePostRoutine()`来防止 `QCoreApplication` 的结构化程序调用该例程。例如，如果该例程在模块卸载前被调用。
对于模块和库，使用引用计数初始化管理器或Qt的父子删除机制可能更好。这里有一个私有类的例子，它利用父子机制在合适的时间调用清理函数：
通过选择正确的父对象，通常可以在合适的时刻清理模块的数据。
注意：该功能自Qt 5.10起就已实现线程安全。
注意：该功能是线程安全的。

**官方示例：**

```cpp
 static int *global_ptr = nullptr;

 static void cleanup_ptr()
 {
     delete [] global_ptr;
     global_ptr = nullptr;
 }

 void init_ptr()
 {
     global_ptr = new int[100];      // allocate data
     qAddPostRoutine(cleanup_ptr);   // delete later
 }
```

### `void qRemovePostRoutine(QtCleanUpFunction ptr)`

**作用与语义：**

将`ptr`指定的清理例程从`QCoreApplication`解构程序调用的例程列表中移除。例程必须先通过调用`qAddPostRoutine()`添加到列表中，否则该函数无效。
注意：该功能自Qt 5.10起就已实现线程安全。
注意：该功能是线程安全的。

### `Q_COREAPP_STARTUP_FUNCTION(QtStartUpFunction ptr)`

**作用与语义：**

添加一个全局函数，调用`QCoreApplication`构造函数。该宏通常用于初始化程序范围的库功能，无需应用程序调用库初始化。
`ptr` 指定的函数应不包含参数，且不应返回任何参数。例如：
注意，启动函数会在`QCoreApplication`构造器结束时运行，在任何图形界面初始化之前。如果函数需要GUI代码，使用定时器（或队列调用）在事件循环中进行初始化。
如果`QCoreApplication`被删除并创建了另一个`QCoreApplication`，启动函数将再次被调用。
注意：该宏不适合用于库代码，因为该函数可能因链接器而被消除而无法调用。
注意：该宏是重录的。

**官方示例：**

```cpp
 // Called once QCoreApplication exists
 static void preRoutineMyDebugTool()
 {
     MyDebugTool* tool = new MyDebugTool(QCoreApplication::instance());
     QCoreApplication::instance()->installEventFilter(tool);
 }

 Q_COREAPP_STARTUP_FUNCTION(preRoutineMyDebugTool)
```

### `Q_DECLARE_TR_FUNCTIONS(context)`

**作用与语义：**

Q_DECLARE_TR_FUNCTIONS() 宏声明并实现了翻译函数`tr()`，签名如下：
如果你想在不继承`QObject`的类中使用`QObject::tr()`，这个宏很有用。
Q_DECLARE_TR_FUNCTIONS()必须出现在类定义的最顶端（在第一个`public:`或`protected:`之前）。例如：
`context`参数通常是类名，但也可以是任何文本。

**官方示例：**

```cpp
 static inline QString tr(const char *sourceText,
                          const char *comment = nullptr);
```

### `void applicationNameChanged()`

**作用与语义：**

该属性保存此应用程序的名称。
应用程序名称在各种 Qt 类和模块中使用，最重要的是在使用默认构造函数构造 `QSettings` 时使用。其他用途包括格式化日志输出（参见 `qSetMessagePattern()`）、`QCommandLineParser` 输出、`QTemporaryDir` 和 `QTemporaryFile` 默认路径，以及 `QStandardPaths` 的某些文件位置。Qt D-Bus、无障碍功能和 XCB 平台集成都使用应用程序名称。
如果未设置，应用程序名称默认为可执行文件名称。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `applicationName` 的变化，不要把它当作普通函数主动调用。

### `void applicationVersionChanged()`

**作用与语义：**

该属性表示该应用的版本。
如果未设置，应用版本默认为主应用程序可执行文件或包中确定的平台特定值（自Qt 5.9起）：
- `Platform`：来源
- `Windows (classic desktop)`：VERSIONINFO 资源的 PRODUCTVERSION 参数
- `macOS, iOS, tvOS, watchOS`：信息属性列表的CFBundleVersion属性
- `Android`：AndroidManifest.xml manifest 元素的 android：versionName 属性
在其他平台上，默认字符串是空字符串。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `applicationVersion` 的变化，不要把它当作普通函数主动调用。

### `void organizationDomainChanged()`

**作用与语义：**

该属性拥有编写本申请的组织的互联网域名。
`QSettings`类在使用默认构造函数构造时使用该值。这样就不用每次创建`QSettings`对象时重复这些信息。
在 Mac 上，如果组织不是空字符串，`QSettings` 使用 organizationDomain() 作为组织;否则使用 `organizationName()`。在所有其他平台上，`QSettings` 使用 `organizationName()` 作为组织。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `organizationDomain` 的变化，不要把它当作普通函数主动调用。

### `void organizationNameChanged()`

**作用与语义：**

该属性保存编写此应用程序的组织名称。
该值在使用默认构造函数构造 `QSettings` 类时使用。这避免了每次创建 `QSettings` 对象时重复提供此信息。
在 Mac 上，如果 `QSettings` 的字符串不为空，它会使用 `organizationDomain()` 作为组织；否则使用 organizationName()。在其他所有平台上，`QSettings` 使用 organizationName() 作为组织。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `organizationName` 的变化，不要把它当作普通函数主动调用。

### `QString applicationName()`

**作用与语义：**

该属性保存此应用程序的名称。
应用程序名称在各种 Qt 类和模块中使用，最重要的是在使用默认构造函数构造 `QSettings` 时使用。其他用途包括格式化日志输出（参见 `qSetMessagePattern()`）、`QCommandLineParser` 输出、`QTemporaryDir` 和 `QTemporaryFile` 默认路径，以及 `QStandardPaths` 的某些文件位置。Qt D-Bus、无障碍功能和 XCB 平台集成都使用应用程序名称。
如果未设置，应用程序名称默认为可执行文件名称。

**如何使用：** 调用 `applicationName()` 读取当前值；它不会修改应用状态。

### `QString applicationVersion()`

**作用与语义：**

该属性表示该应用的版本。
如果未设置，应用版本默认为主应用程序可执行文件或包中确定的平台特定值（自Qt 5.9起）：
- `Platform`：来源
- `Windows (classic desktop)`：VERSIONINFO 资源的 PRODUCTVERSION 参数
- `macOS, iOS, tvOS, watchOS`：信息属性列表的CFBundleVersion属性
- `Android`：AndroidManifest.xml manifest 元素的 android：versionName 属性
在其他平台上，默认字符串是空字符串。

**如何使用：** 调用 `applicationVersion()` 读取当前值；它不会修改应用状态。

### `bool isQuitLockEnabled()`

**作用与语义：**

该属性决定使用`QEventLoopLocker`特性是否会导致应用程序退出。
当该属性被`true`时，应用程序中最后剩余的运行`QEventLoopLocker`的释放将尝试退出应用程序。
注意，尝试退出不一定会导致应用程序退出，例如如果仍有开启窗口，或者`QEvent::Quit`事件被忽略。
默认是`true`。

**如何使用：** 调用 `isQuitLockEnabled()` 读取当前值；它不会修改应用状态。

### `QString organizationDomain()`

**作用与语义：**

该属性拥有编写本申请的组织的互联网域名。
`QSettings`类在使用默认构造函数构造时使用该值。这样就不用每次创建`QSettings`对象时重复这些信息。
在 Mac 上，如果组织不是空字符串，`QSettings` 使用 organizationDomain() 作为组织;否则使用 `organizationName()`。在所有其他平台上，`QSettings` 使用 `organizationName()` 作为组织。

**如何使用：** 调用 `organizationDomain()` 读取当前值；它不会修改应用状态。

### `QString organizationName()`

**作用与语义：**

该属性保存编写此应用程序的组织名称。
该值在使用默认构造函数构造 `QSettings` 类时使用。这避免了每次创建 `QSettings` 对象时重复提供此信息。
在 Mac 上，如果 `QSettings` 的字符串不为空，它会使用 `organizationDomain()` 作为组织；否则使用 organizationName()。在其他所有平台上，`QSettings` 使用 organizationName() 作为组织。

**如何使用：** 调用 `organizationName()` 读取当前值；它不会修改应用状态。

### `void setApplicationName(const QString &application)`

**作用与语义：**

该属性保存此应用程序的名称。
应用程序名称在各种 Qt 类和模块中使用，最重要的是在使用默认构造函数构造 `QSettings` 时使用。其他用途包括格式化日志输出（参见 `qSetMessagePattern()`）、`QCommandLineParser` 输出、`QTemporaryDir` 和 `QTemporaryFile` 默认路径，以及 `QStandardPaths` 的某些文件位置。Qt D-Bus、无障碍功能和 XCB 平台集成都使用应用程序名称。
如果未设置，应用程序名称默认为可执行文件名称。

**如何使用：** 调用 `setApplicationName(...)` 修改 `applicationName`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setApplicationVersion(const QString &version)`

**作用与语义：**

该属性表示该应用的版本。
如果未设置，应用版本默认为主应用程序可执行文件或包中确定的平台特定值（自Qt 5.9起）：
- `Platform`：来源
- `Windows (classic desktop)`：VERSIONINFO 资源的 PRODUCTVERSION 参数
- `macOS, iOS, tvOS, watchOS`：信息属性列表的CFBundleVersion属性
- `Android`：AndroidManifest.xml manifest 元素的 android：versionName 属性
在其他平台上，默认字符串是空字符串。

**如何使用：** 调用 `setApplicationVersion(...)` 修改 `applicationVersion`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setOrganizationDomain(const QString &orgDomain)`

**作用与语义：**

该属性拥有编写本申请的组织的互联网域名。
`QSettings`类在使用默认构造函数构造时使用该值。这样就不用每次创建`QSettings`对象时重复这些信息。
在 Mac 上，如果组织不是空字符串，`QSettings` 使用 organizationDomain() 作为组织;否则使用 `organizationName()`。在所有其他平台上，`QSettings` 使用 `organizationName()` 作为组织。

**如何使用：** 调用 `setOrganizationDomain(...)` 修改 `organizationDomain`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setOrganizationName(const QString &orgName)`

**作用与语义：**

该属性保存编写此应用程序的组织名称。
该值在使用默认构造函数构造 `QSettings` 类时使用。这避免了每次创建 `QSettings` 对象时重复提供此信息。
在 Mac 上，如果 `QSettings` 的字符串不为空，它会使用 `organizationDomain()` 作为组织；否则使用 organizationName()。在其他所有平台上，`QSettings` 使用 organizationName() 作为组织。

**如何使用：** 调用 `setOrganizationName(...)` 修改 `organizationName`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setQuitLockEnabled(bool enabled)`

**作用与语义：**

该属性决定使用`QEventLoopLocker`特性是否会导致应用程序退出。
当该属性被`true`时，应用程序中最后剩余的运行`QEventLoopLocker`的释放将尝试退出应用程序。
注意，尝试退出不一定会导致应用程序退出，例如如果仍有开启窗口，或者`QEvent::Quit`事件被忽略。
默认是`true`。

**如何使用：** 调用 `setQuitLockEnabled(...)` 修改 `quitLockEnabled`；传入的新值会成为后续查询和相关界面行为所使用的值。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

### 状态和错误边界

QObject 派生对象的状态通常通过属性、状态查询函数和信号变化共同表达。信号是通知，不是返回值；收到通知后应读取当前状态并处理异常路径，不能假设每个信号只会出现一次。

### 线程边界

QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

### 最容易出现的错误

一个进程通常只创建一个应用对象；没有调用 exec() 时异步对象通常不会按预期工作；不要在事件循环线程执行长时间阻塞任务。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QCoreApplication` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
