# QProcess

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QProcess` 启动和管理外部程序，提供参数、标准输入输出、错误、退出状态和异步信号。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QProcess` 启动和管理外部程序，提供参数、标准输入输出、错误、退出状态和异步信号。

**内部模型：** QProcess 是 QObject 异步设备；start 后进程未必立即结束，finished/errorOccurred/readReady 信号才是正确的控制流。参数应使用 QStringList 分离传递，避免手工拼接命令行。

**适用场景：** 调用 MarkText、编译器、脚本、系统工具或启动子进程并读取结果时使用。只需一次启动且不关心生命周期时可用 startDetached。

**典型调用链：** 设置 program/arguments/workingDirectory/environment -> start -> waitForStarted 或异步信号 -> readAllStandardOutput/Error -> finished -> deleteLater。

**先记住的坑：** 不要把用户输入直接拼进命令字符串；注意工作目录和环境变量；startDetached 后无法读取输出；阻塞 waitFor... 不要放在 GUI 主线程。

## 2. 依赖与对象关系

- 头文件：`#include <QProcess>`
- 继承自：QIODevice
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

QProcess 是 QObject 异步设备；start 后进程未必立即结束，finished/errorOccurred/readReady 信号才是正确的控制流。参数应使用 QStringList 分离传递，避免手工拼接命令行。

### 状态、生命周期和线程

**生命周期：** 先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

**状态与结果：** QObject 派生对象的状态通常通过属性、状态查询函数和信号变化共同表达。信号是通知，不是返回值；收到通知后应读取当前状态并处理异常路径，不能假设每个信号只会出现一次。

**线程与事件循环：** QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

## 3. 直接使用

调用 MarkText、编译器、脚本、系统工具或启动子进程并读取结果时使用。只需一次启动且不关心生命周期时可用 startDetached。 使用时通常按这个过程组织：设置 program/arguments/workingDirectory/environment -> start -> waitForStarted 或异步信号 -> readAllStandardOutput/Error -> finished -> deleteLater。

```cpp
QProcess *process = new QProcess(this);
connect(process, &QProcess::finished, this, [process](int exitCode) {
    qDebug() << exitCode << process->readAllStandardOutput();
    process->deleteLater();
});
process->start(QStringLiteral("marktext.exe"), {QStringLiteral("README.md")});
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `struct CreateProcessArguments`
- `(since 6.6) struct UnixProcessParameters`
- `CreateProcessArgumentModifier`
- `enum ExitStatus { NormalExit, CrashExit }`
- `enum InputChannelMode { ManagedInputChannel, ForwardedInputChannel }`
- `enum ProcessChannel { StandardOutput, StandardError }`
- `enum ProcessChannelMode { SeparateChannels, MergedChannels, ForwardedChannels, ForwardedErrorChannel, ForwardedOutputChannel }`
- `enum ProcessError { FailedToStart, Crashed, Timedout, WriteError, ReadError, UnknownError }`
- `enum ProcessState { NotRunning, Starting, Running }`
- `(since 6.6) enum class UnixProcessFlag { CloseFileDescriptors, CreateNewSession, DisconnectControllingTerminal, IgnoreSigPipe, ResetIds, …, DisableCoreDumps }`
- `flags UnixProcessFlags`

### 公有函数

- `QProcess(QObject *parent = nullptr)`
- `virtual ~QProcess()`
- `QStringList arguments() const`
- `(since 6.0) std::function<void ()> childProcessModifier() const`
- `void closeReadChannel(QProcess::ProcessChannel channel)`
- `void closeWriteChannel()`
- `QProcess::CreateProcessArgumentModifier createProcessArgumentsModifier() const`
- `QProcess::ProcessError error() const`
- `int exitCode() const`
- `QProcess::ExitStatus exitStatus() const`
- `(since 6.7) void failChildProcessModifier(const char *description, int error = 0)`
- `QProcess::InputChannelMode inputChannelMode() const`
- `QString nativeArguments() const`
- `QProcess::ProcessChannelMode processChannelMode() const`
- `QProcessEnvironment processEnvironment() const`
- `qint64 processId() const`
- `QString program() const`
- `QByteArray readAllStandardError()`
- `QByteArray readAllStandardOutput()`
- `QProcess::ProcessChannel readChannel() const`
- `void setArguments(const QStringList &arguments)`
- `(since 6.0) void setChildProcessModifier(const std::function<void ()> &modifier)`
- `void setCreateProcessArgumentsModifier(QProcess::CreateProcessArgumentModifier modifier)`
- `void setInputChannelMode(QProcess::InputChannelMode mode)`
- `void setNativeArguments(const QString &arguments)`
- `void setProcessChannelMode(QProcess::ProcessChannelMode mode)`
- `void setProcessEnvironment(const QProcessEnvironment &environment)`
- `void setProgram(const QString &program)`
- `void setReadChannel(QProcess::ProcessChannel channel)`
- `void setStandardErrorFile(const QString &fileName, QIODeviceBase::OpenMode mode = Truncate)`
- `void setStandardInputFile(const QString &fileName)`
- `void setStandardOutputFile(const QString &fileName, QIODeviceBase::OpenMode mode = Truncate)`
- `void setStandardOutputProcess(QProcess *destination)`
- `(since 6.6) void setUnixProcessParameters(const QProcess::UnixProcessParameters &params)`
- `(since 6.6) void setUnixProcessParameters(QProcess::UnixProcessFlags flagsOnly)`
- `void setWorkingDirectory(const QString &dir)`
- `void start(const QString &program, const QStringList &arguments = {}, QIODeviceBase::OpenMode mode = ReadWrite)`
- `void start(QIODeviceBase::OpenMode mode = ReadWrite)`
- `(since 6.0) void startCommand(const QString &command, QIODeviceBase::OpenMode mode = ReadWrite)`
- `bool startDetached(qint64 *pid = nullptr)`
- `QProcess::ProcessState state() const`
- `(since 6.6) QProcess::UnixProcessParameters unixProcessParameters() const`
- `bool waitForFinished(int msecs = 30000)`
- `bool waitForStarted(int msecs = 30000)`
- `QString workingDirectory() const`

### 重实现的公有函数

- `virtual qint64 bytesToWrite() const override`
- `virtual void close() override`
- `virtual bool isSequential() const override`
- `virtual bool open(QIODeviceBase::OpenMode mode = ReadWrite) override`
- `virtual bool waitForBytesWritten(int msecs = 30000) override`
- `virtual bool waitForReadyRead(int msecs = 30000) override`

### 公有槽函数

- `void kill()`
- `void terminate()`

### 信号

- `void errorOccurred(QProcess::ProcessError error)`
- `void finished(int exitCode, QProcess::ExitStatus exitStatus = NormalExit)`
- `void readyReadStandardError()`
- `void readyReadStandardOutput()`
- `void started()`
- `void stateChanged(QProcess::ProcessState newState)`

### 静态公有成员

- `int execute(const QString &program, const QStringList &arguments = {})`
- `QString nullDevice()`
- `QStringList splitCommand(QStringView command)`
- `bool startDetached(const QString &program, const QStringList &arguments = {}, const QString &workingDirectory = QString(), qint64 *pid = nullptr)`
- `QStringList systemEnvironment()`

### 保护函数

- `void setProcessState(QProcess::ProcessState state)`

### 重实现的保护函数

- `virtual qint64 readData(char *data, qint64 maxlen) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QProcess::CreateProcessArgumentModifier`

**作用与语义：**

注意：此typedef仅适用于桌面Windows。
在 Windows 上，`QProcess` 使用 Win32 API 函数 `CreateProcess` 启动子进程。虽然`QProcess`提供了一种舒适的方式，无需担心平台细节即可启动进程，但在某些情况下，微调传递给`CreateProcess`的参数是更理想的。这通过定义一个`CreateProcessArgumentModifier`函数并将其传递给`setCreateProcessArgumentsModifier`来实现。
`CreateProcessArgumentModifier`函数只用一个参数：指向`CreateProcessArguments`结构的指针。调用`CreateProcessArgumentModifier`函数后，该结构的成员会传递给`CreateProcess`。
以下示例演示如何将自定义标志传递给`CreateProcess`。当从控制台进程A启动控制台进程B时，`QProcess`默认会为进程B重用进程A的控制台窗口。在此示例中，会为子进程B创建一个带有自定义色彩方案的新控制台窗口。

**官方示例：**

```cpp
     QProcess process;
     process.setCreateProcessArgumentsModifier([] (QProcess::CreateProcessArguments *args)
     {
         args->flags |= CREATE_NEW_CONSOLE;
         args->startupInfo->dwFlags &= ~STARTF_USESTDHANDLES;
         args->startupInfo->dwFlags |= STARTF_USEFILLATTRIBUTE;
         args->startupInfo->dwFillAttribute = BACKGROUND_BLUE | FOREGROUND_RED
                                            | FOREGROUND_INTENSITY;
     });
     process.start("C:\\Windows\\System32\\cmd.exe", QStringList() << "/k" << "title" << "The Child Process");
```

### `enum QProcess::ExitStatus`

**作用与语义：**

本枚举描述了`QProcess`的不同退出状态。
- `QProcess::NormalExit`：`0`;进程正常退出。
- `QProcess::CrashExit`：`1`;进程崩溃。

### `enum QProcess::InputChannelMode`

**作用与语义：**

该枚举描述了`QProcess`的过程输入通道模式。将其中一个值传递给`setInputChannelMode()`以设置当前写入通道模式。
- `QProcess::ManagedInputChannel`：`0`;`QProcess` 管理运行进程的输入。这是 `QProcess` 的默认输入通道模式。
- `QProcess::ForwardedInputChannel`：`1`;`QProcess` 将主进程的输入转发到运行中的进程。子进程从与主进程相同的源读取其标准输入。注意，主进程在子进程运行时不得尝试读取其标准输入。

### `enum QProcess::ProcessChannel`

**作用与语义：**

该枚举描述了运行进程所使用的进程通道。将其中一个值传递给`setReadChannel()`以设置当前的读取通道`QProcess`。
- `QProcess::StandardOutput`：`0`;运行进程的标准输出（stdout）。
- `QProcess::StandardError`：`1`;运行进程的标准误（stderr）。

### `enum QProcess::ProcessChannelMode`

**作用与语义：**

该枚举描述了`QProcess`的过程输出通道模式。将其中一个值传递给`setProcessChannelMode()`以设置当前读通道模式。
- `QProcess::SeparateChannels`：`0`;`QProcess` 管理运行进程的输出，将标准输出和标准错误数据分别存放在内部缓冲区。您可以通过调用 `setReadChannel()` 来选择`QProcess`当前的读通道。这是 `QProcess` 的默认通道模式。
- `QProcess::MergedChannels`：`1`;`QProcess` 将运行进程的输出合并到标准输出通道（`stdout`）。标准误差通道（`stderr`）不会接收任何数据。运行进程的标准输出和标准误差数据交错。对于分离进程，运行进程合并后的输出会转发到主进程。
- `QProcess::ForwardedChannels`：`2`;`QProcess` 将运行进程的输出转发到主进程。子进程写入其标准输出和标准错误的任何内容都会写入主进程的标准输出和标准误。
- `QProcess::ForwardedErrorChannel`：`4`;`QProcess` 管理运行进程的标准输出，但将其标准误转发到主进程。这反映了命令行工具作为过滤器的典型使用，标准输出被重定向到其他进程或文件，而标准错误则打印到控制台以供诊断。（该值于 Qt 5.2 引入。）
- `QProcess::ForwardedOutputChannel`：`3`;与ForwardedErrorChannel互补。（该值在Qt 5.2引入。）
注意：Windows 有意抑制仅 GUI 应用程序向继承控制台的输出。这不适用于重定向到文件或管道的输出。然而，要在控制台上转发仅 GUI 应用的输出，你必须使用 SeparateChannels，并通过读取输出写入相应的输出通道来实现转发。

### `enum QProcess::ProcessError`

**作用与语义：**

该枚举描述了`QProcess`报告的不同类型的错误。
- `QProcess::FailedToStart`：`0`;进程未能启动。要么是调用的程序缺失，要么你可能没有足够的权限或资源来调用该程序。
- `QProcess::Crashed`：`1`;进程在成功启动后不久崩溃。
- `QProcess::Timedout`：`2`;最后的waitFor...() 函数超时。`QProcess`状态未变，你可以尝试调用waitFor...()
- `QProcess::WriteError`：`4`;尝试写入进程时发生错误。例如，进程可能未运行，或关闭了输入通道。
- `QProcess::ReadError`：`3`;尝试从进程读取时发生错误。例如，进程可能未运行。
- `QProcess::UnknownError`：`5`;发生了一个未知错误。这是`error()`的默认返回值。

### `enum QProcess::ProcessState`

**作用与语义：**

这个枚举描述了不同的`QProcess`状态。
- `QProcess::NotRunning`：`0`;进程未运行。
- `QProcess::Starting`：`1`;进程正在开始，但程序尚未被调用。
- `QProcess::Running`：`2`;进程正在运行，准备阅读和写入。

### `[since 6.6] enum class QProcess::UnixProcessFlagflags QProcess::UnixProcessFlags`

**作用与语义：**

这些标志可用于`UnixProcessParameters` `flags`领域。
- `QProcess::UnixProcessFlag::CloseFileDescriptors`：`0x0010`;关闭所有超过`lowestFileDescriptorToClose`定义阈值的文件描述符，防止父进程中当前开放的任何描述符意外泄漏给子进程。`stdin`、`stdout`和`stderr`文件描述符永远不会关闭。
- `QProcess::UnixProcessFlag::CreateNewSession (since Qt 6.7)`：`0x0040`;通过调用`setsid(2)`启动一个新的进程会话。这允许子进程比当前进程所在的会话更长。这是`startDetached()`允许进程脱离的步骤之一，也是进程守护进程的守护进程步骤之一。
- `QProcess::UnixProcessFlag::DisconnectControllingTerminal (since Qt 6.7)`：`0x0080`;请求进程断开与其控制终端的连接（如果有的话）。如果没有，则不会发生任何事。仍然连接到控制终端的进程，如果终端关闭，可能会收到挂断（Hang Up，`SIGHUP`）信号，或者其他终端控制信号（`SIGTSTP`、`SIGTTIN`、`SIGTTOU`）之一。注意，在某些操作系统上，进程只有在是会话领导者时才可能断开与控制终端的连接，这意味着可能需要使用`CreateNewSession`标志。同样，这也是进程守护进程的一个步骤。
- `QProcess::UnixProcessFlag::IgnoreSigPipe`：`0x0002`;即使`ResetSignalHandlers`标志已设置，也始终将`SIGPIPE`信号设置为忽略（`SIG_IGN`）。默认情况下，如果子节点在相应通道被`QProcess::closeReadChannel()`关闭后尝试写入其标准输出或标准错误，会收到`SIGPIPE`信号并立即终止;使用此标志时，写操作在没有信号的情况下失败，子节点可以继续执行。
- `QProcess::UnixProcessFlag::ResetIds (since Qt 6.7)`：`0x0100`;丢弃当前进程可能仍保留的任何有效用户或组ID（参见`setuid(2)`和`setgid(2)`及`QCoreApplication::setSetuidAllowed()`）。如果当前进程是setuid或setgid，且不希望子进程保留提升权限，这非常有用。
- `QProcess::UnixProcessFlag::ResetSignalHandlers`：`0x0001`;将所有 Unix 信号处理程序重置回默认状态（即将 `SIG_DFL` 传递给 `signal(2)`）。该标志有助于确保任何被忽略（`SIG_IGN`）信号不会影响子信号的行为。
- `QProcess::UnixProcessFlag::UseVFork`：`0x0020`;请求`QProcess`使用 `vfork(2)` 启动子进程。使用此标志表示带 `setChildProcessModifier()` 的回调函数可在`vfork(2)`的子端安全执行;也就是说，回调不会修改任何非本地变量（无论是直接还是通过调用的函数），也不会尝试与父进程通信。它是实现定义的`QProcess`是否实际使用`vfork(2)`以及`vfork(2)`是否与标准`fork(2)`不同。
- `QProcess::UnixProcessFlag::DisableCoreDumps (since Qt 6.9)`：`0x0200`;请求`QProcess`禁用子进程中的核心转储。如果执行的可执行文件可能会崩溃，但用户和维护者不愿意针对这些条件生成错误报告（例如，可执行文件是测试进程），这很有用。该设置不影响崩溃进程的 `exitStatus()`。它通过将核心转储资源软限制设置为零来实现，意味着应用程序仍可将该变更提高到硬上限。
该枚举于Qt 6.6引入。
UnixProcessFlags 类型是 QFlags 的 typedef<UnixProcessFlag>。它存储 UnixProcessFlag 值的 OR 组合。

### `[explicit] QProcess::QProcess(QObject *parent = nullptr)`

**作用与语义：**

构造一个具有给定`parent`的QProcess对象。

### `[virtual noexcept] QProcess::~QProcess()`

**作用与语义：**

摧毁`QProcess`对象，即终止进程。
注意，该函数只有进程终止后才会返回。

### `QStringList QProcess::arguments() const`

**作用与语义：**

返回进程最后启动时使用的命令行参数。

### `[override virtual] qint64 QProcess::bytesToWrite() const`

**作用与语义：**

重实现自：`QIODevice::bytesToWrite()` const.
对于有缓冲区的设备，该函数返回等待写入的字节数。对于没有缓冲区的设备，该函数返回0。
重新实现该函数的子类必须调用基础实现，以包含`QIODevice`缓冲区大小。

### `[since 6.0] std::function<void ()> QProcess::childProcessModifier() const`

**作用与语义：**

返回之前通过调用`setChildProcessModifier()`设置的修饰函数。
注意：此功能仅适用于Unix平台。

### `[override virtual] void QProcess::close()`

**作用与语义：**

重装：`QIODevice::close()`。
关闭与进程的所有通信并终止进程。调用该函数后，`QProcess`将不再发出`readyRead()`，数据也无法读取或写入。
先发出`aboutToClose()`，然后关闭设备并将其 OpenMode 设置为 NotOpen。错误字符串也会被重置。

### `void QProcess::closeReadChannel(QProcess::ProcessChannel channel)`

**作用与语义：**

关闭读信道`channel`。调用该函数后，`QProcess`将不再接收信道上的数据。任何已接收的数据仍然可用读取。
如果你不关心进程的输出，可以调用这个函数来节省内存。

### `void QProcess::closeWriteChannel()`

**作用与语义：**

将`QProcess`的写信道安排关闭。当所有数据写入进程后，该信道将关闭。调用该函数后，任何写入进程的尝试都会失败。
对于读取输入数据直到通道关闭的程序来说，关闭写入通道是必要的。例如，程序“more”在Unix和Windows的控制台中用于显示文本数据。但在`QProcess`的写入通道关闭之前，它不会显示文本数据。示例：
当调用`start()`时，写信道会隐式打开。

**官方示例：**

```cpp
 QProcess more;
 more.start("more");
 more.write("Text to display");
 more.closeWriteChannel();
 // QProcess will emit readyRead() once "more" starts printing
```

### `QProcess::CreateProcessArgumentModifier QProcess::createProcessArgumentsModifier() const`

**作用与语义：**

返回之前设置的`CreateProcess`修正函数。
注意：此功能仅适用于Windows平台。

### `QProcess::ProcessError QProcess::error() const`

**作用与语义：**

返回上次发生的错误类型。

### `[signal] void QProcess::errorOccurred(QProcess::ProcessError error)`

**作用与语义：**

当进程发生错误时，该信号会发出。指定的`error`描述了发生的错误类型。

### `[static] int QProcess::execute(const QString &program, const QStringList &arguments = {})`

**作用与语义：**

启动程序`program`，并`arguments`新进程中的参数，等待程序完成，然后返回进程的出口代码。新进程写入控制台的任何数据都会转发给调用进程。
环境和工作目录是从调用进程继承而来的。
参数处理与相应的`start()`重载相同。
如果进程无法启动，返回 -2。如果进程崩溃，返回 -1。否则返回进程的退出代码。

### `int QProcess::exitCode() const`

**作用与语义：**

返回上一个完成进程的退出代码。
除非`exitStatus()`返回`NormalExit`，否则该数值无效。

### `QProcess::ExitStatus QProcess::exitStatus() const`

**作用与语义：**

返回上一个完成进程的退出状态。
在Windows上，如果进程是用其他应用程序的TerminateProcess()终止的，除非退出码小于0，否则该函数仍会返回`NormalExit`。

### `[noexcept, since 6.7] void QProcess::failChildProcessModifier(const char *description, int error = 0)`

**作用与语义：**

这些函数可以在修饰符集内使用，`setChildProcessModifier()`表示遇到了错误条件。当修饰符调用这些函数时，`QProcess`会在父进程中发出带有代码`QProcess::FailedToStart`的`errorOccurred()`。`description`可以用来在 `errorString()` 中包含一些信息，帮助诊断问题，通常是失败调用的名称，类似于 C 库函数 `perror()`。此外，`error` 参数也可以是`<errno.h>`错误代码，其文本形式也会被包含在内。
例如，子修改器可以这样为子进程准备一个额外的文件描述符：
其中`fd` 是父进程中当前打开的文件描述符。如果`dup2()`系统调用导致`EBADF`条件，进程`errorString()`可能是“子进程修改器报告错误：aux comm channel： Bad file descriptor”。
该函数不会返回调用者。除了在子修饰符和正确的 `QProcess` 对象中使用它外，是未定义的行为。
注意：实现对`description`参数的长度限制为约500个字符。这不包括`error`代码中的文本。

**官方示例：**

```cpp
 process.setChildProcessModifier([fd, &process]() {
     if (dup2(fd, TargetFileDescriptor) < 0)
         process.failChildProcessModifier(errno, "aux comm channel");
 });
 process.start();
```

### `[signal] void QProcess::finished(int exitCode, QProcess::ExitStatus exitStatus = NormalExit)`

**作用与语义：**

该信号在进程结束时发出。`exitCode` 是进程的退出代码（仅适用于正常退出），`exitStatus` 是退出状态。进程结束后，`QProcess` 中的缓冲区仍然完好。你仍然可以读取进程在完成前可能写入的任何数据。

### `QProcess::InputChannelMode QProcess::inputChannelMode() const`

**作用与语义：**

返回`QProcess`标准输入通道的通道模式。

### `[override virtual] bool QProcess::isSequential() const`

**作用与语义：**

重实现自：`QIODevice::isSequential()` const.
如果该装置是顺序的，返回`true`;否则返回假。
顺序设备与随机访问设备不同，没有起始、结束、大小或当前位置的概念，也不支持寻道。只有当设备报告数据可用时，你才能读取数据。最常见的顺序设备例子是网络套接字。在Unix上，特殊文件如/dev/zero和fifo管道是顺序文件。
而普通文件则支持随机访问。它们既有大小也有当前位置，还支持在数据流中向后和向前寻求。普通文件则是非顺序的。

### `[slot] void QProcess::kill()`

**作用与语义：**

会终止当前进程，使其立即退出。
在 Windows 上，kill() 使用 TerminateProcess，而在 Unix 和 macOS 上，SIGKILL 信号发送给进程。

### `QString QProcess::nativeArguments() const`

**作用与语义：**

返回程序的额外本地命令行参数。
注意：此功能仅适用于Windows平台。

### `[static] QString QProcess::nullDevice()`

**作用与语义：**

操作系统的空设备。
返回的文件路径使用本地目录分隔符。

### `[override virtual] bool QProcess::open(QIODeviceBase::OpenMode mode = ReadWrite)`

**作用与语义：**

重实现自：`QIODevice::open`（QIODeviceBase：：OpenMode 模式）。
启动由`setProgram()`设置的程序，参数由`setArguments()`设置。OpenMode 设置为`mode`。
该方法是`start()`的别名，仅用于完整实现`QIODevice`定义的接口。
退货`true`项目是否已启动。
打开设备并将其 OpenMode 设置为 `mode`。成功时返回 `true`;否则返回 `false`。该函数应从任何重新实现的 open() 或其他打开设备的函数中调用。

### `QProcess::ProcessChannelMode QProcess::processChannelMode() const`

**作用与语义：**

返回`QProcess`标准输出和标准误差通道的通道模式。

### `QProcessEnvironment QProcess::processEnvironment() const`

**作用与语义：**

返回`QProcess`将传递给子进程的环境。如果没有使用`setProcessEnvironment()`设置环境，该方法返回一个对象，表明该环境将继承自父进程。

### `qint64 QProcess::processId() const`

**作用与语义：**

如果有，返回运行进程的本地进程标识符。如果当前没有进程在运行，则返回`0`。

### `QString QProcess::program() const`

**作用与语义：**

返回程序，最后一次启动流程时。

### `QByteArray QProcess::readAllStandardError()`

**作用与语义：**

无论当前的读信道如何，该函数都会以`QByteArray`返回进程标准误中所有可用的数据。

### `QByteArray QProcess::readAllStandardOutput()`

**作用与语义：**

无论当前的读信道如何，该函数都会以`QByteArray`返回过程标准输出中所有可用的数据。

### `QProcess::ProcessChannel QProcess::readChannel() const`

**作用与语义：**

返回 `QProcess` 的当前读取通道。

### `[override virtual protected] qint64 QProcess::readData(char *data, qint64 maxlen)`

**作用与语义：**

Reimplements： `QIODevice::readData`（char *data， qint64 maxSize）.
从设备读取最多`maxSize`字节到`data`，返回读取字节数，或如果发生错误则返回-1字节。
如果没有字节可读且永远无法再有更多字节（例如套接字闭合、管道闭合、子进程已完成），该函数返回 -1。
该函数由`QIODevice`调用。创建`QIODevice`子类时重新实现该函数。
在重新实现该函数时，重要的是该函数在返回前读取所有所需数据。这是 `QDataStream` 能够操作该类的必要条件。`QDataStream` 假设所有请求的信息都已读取，因此如果存在问题，不会重新尝试读取。
该函数可调用 maxSize 为 0，可用于执行读取后操作。

### `[private signal] void QProcess::readyReadStandardError()`

**作用与语义：**

当过程通过其标准误差信道（`stderr`）提供新数据时，该信号会被发射。无论当前读信道为何，都会发出该信号。
注意：这是一个私有信号。它可以用于信号连接，但用户不能发射。

### `[private signal] void QProcess::readyReadStandardOutput()`

**作用与语义：**

当进程通过其标准输出通道（`stdout`）提供新数据时，该信号会被发射。无论当前的读通道如何，都会发出该信号。
注意：这是一个私有信号。它可以用于信号连接，但用户不能发射。

### `void QProcess::setArguments(const QStringList &arguments)`

**作用与语义：**

在启动进程时，设置该`arguments`传递给被调用程序。该函数必须在`start()`之前被调用。

### `[since 6.0] void QProcess::setChildProcessModifier(const std::function<void ()> &modifier)`

**作用与语义：**

为子进程设置`modifier`函数，适用于Unix系统（包括macOS;Windows，详见 `setCreateProcessArgumentsModifier()`）。`modifier`参数所包含的函数将在`fork()`或`vfork()`完成且`QProcess`已设置好子进程的标准文件描述符后，在子进程中调用，但在此之前，`execve()`，在`start()`内调用。
以下展示了设置子进程无权限运行的示例：
如果修饰函数出现故障，它可以用`failChildProcessModifier()`向`QProcess`调用者报告情况。或者，它也可以使用其他停止进程的方法，比如 `_exit()` 或 `abort()`。
子进程的某些属性，如关闭所有多余的文件描述符或断开与控制TTY的连接，可以通过使用`setUnixProcessParameters()`更容易实现，能够检测失败并报告`FailedToStart`状态。修饰符有助于更改子进程的某些不常见属性，比如设置额外的文件描述符。如果同时设置了子进程修饰符和Unix进程参数，则在应用这些参数之前运行该修饰符。
注意：在多线程应用中，该函数必须小心不要调用可能锁定其他线程中可能正在使用的互斥组的函数（一般建议仅使用POSIX定义为“异步信号安全”的函数）。大部分Qt API在此回调内不安全，包括`qDebug()`，可能导致死锁。
注意：如果通过`setUnixProcessParameters()`设置了UnixProcessParameters：：UseVFork标志，`QProcess`可能会使用`vfork()`语义来启动子进程，因此该函数必须遵守更严格的约束。首先，由于它仍与父进程共享内存，必须不写入任何非本地变量，并且读取时必须遵守正确的顺序语义，以避免数据竞赛。其次，更多库函数可能会出现异常;因此，该函数应仅使用低级系统调用，如`read()`、`write()`、`setsid()`、`nice()`等。

**官方示例：**

```cpp
 void runSandboxed(const QString &name, const QStringList &arguments)
 {
     QProcess proc;
     proc.setChildProcessModifier([] {
         // Drop all privileges in the child process, and enter
         // a chroot jail.
         ::setgroups(0, nullptr);
         ::chroot("/run/safedir");
         ::chdir("/");
         ::setgid(safeGid);
         ::setuid(safeUid);
         ::umask(077);
     });
     proc.start(name, arguments);
     proc.waitForFinished();
 }
```

### `void QProcess::setCreateProcessArgumentsModifier(QProcess::CreateProcessArgumentModifier modifier)`

**作用与语义：**

设置`CreateProcess` Win32 API 调用的`modifier`。通过 Pass `QProcess::CreateProcessArgumentModifier()` 移除之前设置的 API 调用。
注意：此功能仅在Windows平台上可用，且需要C 11。

### `void QProcess::setInputChannelMode(QProcess::InputChannelMode mode)`

**作用与语义：**

将`QProcess`标准输入通道的通道模式设置为指定的`mode`。下次调用`start()`时将使用此模式。

### `void QProcess::setNativeArguments(const QString &arguments)`

**作用与语义：**

为程序设置额外的本地命令行`arguments`。
在操作系统中，系统API原生使用单个字符串传递命令行`arguments`，可以构想出无法通过`QProcess`可移植的基于列表的API传递的命令行。在这种情况下，必须使用该函数设置字符串，并附加于由通常参数列表组成的字符串，并带有分隔空间。
注意：此功能仅适用于Windows平台。

### `void QProcess::setProcessChannelMode(QProcess::ProcessChannelMode mode)`

**作用与语义：**

将`QProcess`标准输出和标准误差通道的通道模式设置为指定的`mode`。该模式将在下次调用`start()`时使用。例如：

**官方示例：**

```cpp
 QProcess builder;
 builder.setProcessChannelMode(QProcess::MergedChannels);
 builder.start("make", QStringList() << "-j2");

 if (!builder.waitForFinished())
     qDebug() << "Make failed:" << builder.errorString();
 else
     qDebug() << "Make output:" << builder.readAll();
```

### `void QProcess::setProcessEnvironment(const QProcessEnvironment &environment)`

**作用与语义：**

设定将`QProcess`传递给子进程的`environment`。
例如，以下代码添加了环境变量 `TMPDIR`：
注意在 Windows 上，环境变量名称不区分大小写。

**官方示例：**

```cpp
 QProcess process;
 QProcessEnvironment env = QProcessEnvironment::systemEnvironment();
 env.insert("TMPDIR", "C:\\MyApp\\temp"); // Add an environment variable
 process.setProcessEnvironment(env);
 process.start("myapp");
```

### `[protected] void QProcess::setProcessState(QProcess::ProcessState state)`

**作用与语义：**

将`QProcess`当前状态设置为指定的`state`。

### `void QProcess::setProgram(const QString &program)`

**作用与语义：**

将该 `program`设置为启动进程时使用。该函数必须在 `start()` 前调用。
如果 `program` 是绝对路径，则指定将启动的具体可执行文件。相对路径将以平台特定方式解析，包括搜索`PATH`环境变量（详见“查找可执行文件”）。

### `void QProcess::setReadChannel(QProcess::ProcessChannel channel)`

**作用与语义：**

将`QProcess`当前读通道设置为给定的`channel`。当前输入通道被`read()`、`readAll()`、`readLine()`和`getChar()`等函数使用。它还决定`QProcess`哪个通道触发`readyRead()`。

### `void QProcess::setStandardErrorFile(const QString &fileName, QIODeviceBase::OpenMode mode = Truncate)`

**作用与语义：**

将进程的标准误重定向到文件`fileName`。当重定向到位时，标准误差读取通道关闭：使用`read()`读取通道总是失败，文件`readAllStandardError()`也会失败。如果`mode`是附加，文件将被附加，否则将被截断。
有关文件如何开启的更多信息，请参见`setStandardOutputFile()`。
注意：如果调用`setProcessChannelMode()`时参数为`QProcess::MergedChannels`，则该函数无效。

### `void QProcess::setStandardInputFile(const QString &fileName)`

**作用与语义：**

将进程的标准输入重定向到`fileName`指示的文件。当输入重定向存在时，`QProcess`对象将处于只读模式（调用`write()`会导致错误）。
要让进程立即读取EOF，请传递这里`nullDevice()`。这比在写入任何数据前使用`closeWriteChannel()`更干净，因为它可以在进程启动前设置好。
如果文件`fileName`在调用时不存在或无法读取`start()`，启动进程将失败。
进程启动后调用 setStandardInputFile() 无效。

### `void QProcess::setStandardOutputFile(const QString &fileName, QIODeviceBase::OpenMode mode = Truncate)`

**作用与语义：**

将进程的标准输出重定向到文件`fileName`。当重定向生效时，标准输出读信道关闭：使用`read()`读取信道总是失败，且`readAllStandardOutput()`也会失败。
要丢弃进程中的所有标准输出，请在这里传递`nullDevice()`。这比单纯不读取标准输出更高效，因为没有填充`QProcess`缓冲区。
如果`fileName`文件在调用时不存在，`start()`文件会被创建。如果无法创建，起始程序将失败。
如果文件存在且`mode` `QIODeviceBase::Truncate`，文件将被截断。否则（如果`mode` `QIODeviceBase::Append`），文件将被附加到。
进程启动后调用 setStandardOutputFile() 则无效。
如果`fileName`是空字符串，它会停止重定向标准输出。这对于重定向后恢复标准输出非常有用。

### `void QProcess::setStandardOutputProcess(QProcess *destination)`

**作用与语义：**

将该进程的标准输出流管道连接到`destination`进程的标准输入。
以下shell命令：
可用以下代码`QProcess`实现：

**官方示例：**

```cpp
 command1 | command2
```

### `[since 6.6] void QProcess::setUnixProcessParameters(const QProcess::UnixProcessParameters &params)`

**作用与语义：**

设置 Unix 系统中子进程的额外设置和参数，使其`params`。该函数可用于请求 `QProcess` 在启动目标可执行文件前修改子进程。
该函数可用于更改子进程的某些属性，如关闭所有多余的文件描述符、更改子进程的良好级别，或断开与控制 TTY 的连接。如需更细致地控制子进程或以其他方式修改，可以使用 `setChildProcessModifier()` 函数。如果同时设置了子进程修改器和 Unix 进程参数，则在应用这些参数之前运行该修改器。
注意：此功能仅适用于Unix平台。

### `[since 6.6] void QProcess::setUnixProcessParameters(QProcess::UnixProcessFlags flagsOnly)`

**作用与语义：**

将 Unix 系统子进程的额外设置设置为 `flagsOnly`。这和仅设置 `flags` 字段时的超载相同。
注意：此功能仅适用于Unix平台。

### `void QProcess::setWorkingDirectory(const QString &dir)`

**作用与语义：**

将工作目录设置为 `dir`。`QProcess` 会在这个目录中启动进程。默认行为是从调用进程的工作目录中启动进程。

### `[static] QStringList QProcess::splitCommand(QStringView command)`

**作用与语义：**

将字符串`command`拆分为一个令牌列表，并返回该列表。
带空格的标记可以用双引号包围;三个连续的双引号代表引号字符本身。

### `void QProcess::start(const QString &program, const QStringList &arguments = {}, QIODeviceBase::OpenMode mode = ReadWrite)`

**作用与语义：**

在新进程中启动给定的`program`，并以`arguments`传递命令行参数。有关`QProcess`如何搜索要运行的可执行文件，请参见 `setProgram()`。OpenMode 设置为 `mode`。不再对参数进行进一步拆分。
`QProcess`对象会立即进入起始状态。如果进程成功启动，`QProcess`会发出`started()`;否则会发出`errorOccurred()`。请注意，在能够同步启动子进程的平台上（尤其是Windows），这些信号会在该函数返回前被发射，`QProcess`对象分别会转变为`QProcess::Running`或`QProcess::NotRunning`状态。在其他终端形式上，`started()`和 `errorOccurred()` 信号会被延迟。
调用`waitForStarted()`确认进程已启动（或未启动）且这些信号已发出。即使进程启动状态已知，调用该函数也是安全的，但信号不会再次发出。
Windows：参数被引号并合并成一个与 `CommandLineToArgvW()` Windows 函数兼容的命令行。对于要求不同的命令行引号的程序，你需要使用 `setNativeArguments()`。有一个显著的程序不遵循`CommandLineToArgvW()`规则，cmd.exe 以及所有批处理脚本。
如果`QProcess`对象已经在运行进程，控制台可能会打印警告，现有进程将继续运行，不受影响。
注意：成功启动子进程仅意味着操作系统成功创建了该进程并分配了每个进程拥有的资源，如进程ID。子进程可能会很早崩溃或失败，从而无法产生预期输出。在大多数操作系统中，这可能包括动态链接错误。

### `void QProcess::start(QIODeviceBase::OpenMode mode = ReadWrite)`

**作用与语义：**

启动由`setProgram()`设置的程序，参数由`setArguments()`设置。OpenMode 设置为`mode`。

### `[since 6.0] void QProcess::startCommand(const QString &command, QIODeviceBase::OpenMode mode = ReadWrite)`

**作用与语义：**

在新进程中`command`启动命令。OpenMode 设置为 `mode`。
`command` 是一串包含程序名称和参数的单一字符串。参数之间用一个或多个空格分隔。例如：
包含空格的参数必须引用，才能正确地提供给新进程。例如：
`command`串中的字面引号用三引号表示。例如：
在`command`字符串被拆分并取消引号后，该函数的行为类似于`start()`。
在操作系统中，系统API原生使用单一字符串传递命令行参数的操作系统（Windows），可以想象出无法通过`QProcess`可移植列表API传递的命令行。在这些罕见情况下，你需要使用`setProgram()`和`setNativeArguments()`代替这个函数。

**官方示例：**

```cpp
 QProcess process;
 process.startCommand("del /s *.txt");
 // same as process.start("del", QStringList() << "/s" << "*.txt");
 //...
```

### `bool QProcess::startDetached(qint64 *pid = nullptr)`

**作用与语义：**

在新进程中启动由`setProgram()`设置的程序，并以`setArguments()`参数设置，并与程序分离。成功时返回`true`;否则返回`false`。如果调用进程退出，分离进程将继续不受影响地运行。
Unix：启动进程会在自己的会话中运行，并像守护进程一样。
进程将从`setWorkingDirectory()`设置的目录中启动。如果`workingDirectory()`为空，工作目录将继承自调用进程。
如果函数成功，则将 *`pid` 设置为启动进程的进程标识符;否则，设置为 -1。注意，子进程可能会退出，PID 可能会无效且无预警。此外，子进程退出后，同一 PID 可能会被回收并被完全不同的进程使用。用户代码在使用该变量时应当谨慎，尤其是当用户打算通过操作系统强制终止进程时。
startDetached() 仅支持以下属性设置器：
- `setArguments()`
- `setCreateProcessArgumentsModifier()`
- `setNativeArguments()`
- `setProcessEnvironment()`
- `setProgram()`
- `setStandardErrorFile()`
- `setStandardInputFile()`
- `setStandardOutputFile()`
- `setProcessChannelMode`（`QProcess::MergedChannels`）
- `setStandardOutputProcess()`
- `setWorkingDirectory()`
`QProcess`对象的其他所有属性都被忽略。
注意：被调用进程继承调用进程的控制台窗口。为了抑制控制台输出，将标准/错误输出重定向到`QProcess::nullDevice()`。

### `[static] bool QProcess::startDetached(const QString &program, const QStringList &arguments = {}, const QString &workingDirectory = QString(), qint64 *pid = nullptr)`

**作用与语义：**

启动程序`program`，并`arguments`新进程中的参数，并与该进程分离。成功时返回`true`;否则返回`false`。如果调用进程退出，分离进程将继续不受影响地运行。
参数处理与相应的`start()`重载相同。
进程将从目录`workingDirectory`启动。如果`workingDirectory`空，工作目录将继承自调用进程。
如果函数成功，则将 *`pid` 设置为启动进程的进程标识符。
注意：该功能会让`QProcess::startDetached()`重载。

### `[private signal] void QProcess::started()`

**作用与语义：**

当过程开始时，`QProcess`会发出该信号，`state()`返回`Running`。
注意：这是一个私有信号。它可以用于信号连接，但用户不能发射。

### `QProcess::ProcessState QProcess::state() const`

**作用与语义：**

返回进程的当前状态。

### `[private signal] void QProcess::stateChanged(QProcess::ProcessState newState)`

**作用与语义：**

每当`QProcess`状态变化时，这个信号就会发出。`newState`论证是`QProcess`改变到的状态。
注意：这是一个私有信号。它可以用于信号连接，但用户不能发射。

### `[static] QStringList QProcess::systemEnvironment()`

**作用与语义：**

返回调用进程的环境，作为键=值对的列表。示例：
该函数不缓存系统环境。因此，如果调用了低级C库函数如`setenv`或`putenv`，可以获得环境的更新版本。
但需要注意的是，反复调用该函数会重新创建环境变量列表，这是一个非简单的操作。
注意：对于新代码，建议使用`QProcessEnvironment::systemEnvironment()`。

**官方示例：**

```cpp
 QStringList environment = QProcess::systemEnvironment();
 // environment = {"PATH=/usr/bin:/usr/local/bin",
 //                "USER=greg", "HOME=/home/greg"}
```

### `[slot] void QProcess::terminate()`

**作用与语义：**

试图终止进程。
调用该函数后进程可能不会退出（它会被提示用户是否存档等）。
在 Windows 上，terminate() 会向进程的所有顶层窗口发送 WM_CLOSE 消息，然后发送到进程的主线程。在 Unix 和 macOS 上，发送 `SIGTERM` 信号。
Windows上不运行事件循环或事件循环无法处理WM_CLOSE消息的控制台应用程序只能通过调用`kill()`终止。

### `[noexcept, since 6.6] QProcess::UnixProcessParameters QProcess::unixProcessParameters() const`

**作用与语义：**

返回描述 Unix 系统中子进程将应用的额外标志和设置的 `UnixProcessParameters` 对象。默认设置对应于默认构造的 `UnixProcessParameters`。
注意：此功能仅适用于Unix平台。

### `[override virtual] bool QProcess::waitForBytesWritten(int msecs = 30000)`

**作用与语义：**

重实现自：`QIODevice::waitForBytesWritten`（int msecs）。
对于缓冲设备，该功能等待在设备写入缓冲数据且`bytesWritten()`信号发出后，或经过`msecs`毫秒后才启用。如果msecs为-1，该函数不会超时。对于未缓冲设备，该功能会立即返回。
如果数据载荷写入设备，返回`true`;否则返回`false`（即操作超时或发生错误）。
该函数可以在没有事件循环的情况下运行。它在编写非 GUI 应用以及在非 GUI 线程中执行 I/O 操作时非常有用。
如果从连接到`bytesWritten()`信号的槽函数内调用，则`bytesWritten()`不会被重新发射。
重新实现这个函数，为自定义设备提供阻断API。默认实现不做任何事，返回`false`。
警告：从主线（GUI）线程调用该函数可能会导致用户界面卡死。

### `bool QProcess::waitForFinished(int msecs = 30000)`

**作用与语义：**

直到过程结束且发出`finished()`信号，或直到`msecs`毫秒过去。
如果进程完成，返回`true`;否则返回`false`（如果操作超时、发生错误，或该`QProcess`已经完成）。
该函数可以在没有事件循环的情况下运行。它在编写非 GUI 应用以及在非 GUI 线程中执行 I/O 操作时非常有用。
警告：从主线（GUI）线程调用该函数可能会导致用户界面卡死。
如果 msecs 为 -1，该函数不会超时。

### `[override virtual] bool QProcess::waitForReadyRead(int msecs = 30000)`

**作用与语义：**

重实现自：`QIODevice::waitForReadyRead`（int msecs）。
阻塞直到有新数据可供读取且`readyRead()`信号已发出，或`msecs`毫秒过去。如果msecs为-1，该函数不会超时。
如果有新数据可供读取，返回`true`;否则返回 false（如果操作超时或发生错误）。
该函数可以在没有事件循环的情况下运行。它在编写非 GUI 应用以及在非 GUI 线程中执行 I/O 操作时非常有用。
如果从连接到`readyRead()`信号的槽函数内调用，则`readyRead()`不会被重新发射。
重新实现这个函数，为自定义设备提供阻断API。默认实现不做任何事，返回`false`。
警告：从主线（GUI）线程调用该函数可能会导致用户界面卡死。

### `bool QProcess::waitForStarted(int msecs = 30000)`

**作用与语义：**

直到过程开始且`started()`信号发出，或直到`msecs`毫秒过去。
如果进程成功启动，返回`true`;否则返回`false`（如果操作超时或发生错误）。如果进程在此功能之前已成功启动，则立即返回。
该函数可以在没有事件循环的情况下运行。它在编写非 GUI 应用以及在非 GUI 线程中执行 I/O 操作时非常有用。
警告：从主线（GUI）线程调用该函数可能会导致用户界面卡死。
如果 msecs 为 -1，该函数不会超时。

### `QString QProcess::workingDirectory() const`

**作用与语义：**

如果`QProcess`被分配了一个工作目录，该函数返回`QProcess`在程序启动前将进入的工作目录。否则（即未分配目录），返回空字符串，`QProcess`将使用应用程序当前的工作目录。

### `struct CreateProcessArguments`

**作用与语义：**

注意：该结构体仅在Windows平台上可用。
该结构体表示了 Windows API 函数 `CreateProcess` 的所有参数。它被用作`CreateProcessArgumentModifier`函数的参数。

### `(since 6.6) struct UnixProcessParameters`

**作用与语义：**

注意：该结构体仅在Unix平台上可用。
该结构体可用于通过 `QProcess::setUnixProcessParameters()` 传递子进程的额外、Unix 专用配置。
其成员包括：
- UnixProcessParameters：：flags 标志，详见`QProcess::UnixProcessFlags`
- UnixProcessParameters：：lowestFileDescriptorToClose 最低关闭文件描述符。
当 QProcess：：UnixProcessFlags：：CloseFileDescriptors 标志被设置在 `flags` 字段时，`QProcess` 会在执行子进程前关闭应用程序的打开文件描述符。描述符 0、1 和 2（即 `stdin`、`stdout` 和 `stderr`）保持不动，以及编号低于 `lowestFileDescriptorToClose` 字段值的描述符。
上述所有设置也可以通过从带有`QProcess::setChildProcessModifier()`的处理程序集调用相应的POSIX函数来手动实现。这种结构允许`QProcess`处理平台特定的差异，享受某些优化，并减少代码重复。此外，如果这些函数中的任何一个失败，`QProcess`将进入`QProcess::FailedToStart`状态，而子进程修饰符回调不允许失败。

### `CreateProcessArgumentModifier`

**作用与语义：**

注意：此typedef仅适用于桌面Windows。
在 Windows 上，`QProcess` 使用 Win32 API 函数 `CreateProcess` 启动子进程。虽然`QProcess`提供了一种舒适的方式，无需担心平台细节即可启动进程，但在某些情况下，微调传递给`CreateProcess`的参数是更理想的。这通过定义一个`CreateProcessArgumentModifier`函数并将其传递给`setCreateProcessArgumentsModifier`来实现。
`CreateProcessArgumentModifier`函数只用一个参数：指向`CreateProcessArguments`结构的指针。调用`CreateProcessArgumentModifier`函数后，该结构的成员会传递给`CreateProcess`。
以下示例演示如何将自定义标志传递给`CreateProcess`。当从控制台进程A启动控制台进程B时，`QProcess`默认会为进程B重用进程A的控制台窗口。在此示例中，会为子进程B创建一个带有自定义色彩方案的新控制台窗口。

**官方示例：**

```cpp
     QProcess process;
     process.setCreateProcessArgumentsModifier([] (QProcess::CreateProcessArguments *args)
     {
         args->flags |= CREATE_NEW_CONSOLE;
         args->startupInfo->dwFlags &= ~STARTF_USESTDHANDLES;
         args->startupInfo->dwFlags |= STARTF_USEFILLATTRIBUTE;
         args->startupInfo->dwFillAttribute = BACKGROUND_BLUE | FOREGROUND_RED
                                            | FOREGROUND_INTENSITY;
     });
     process.start("C:\\Windows\\System32\\cmd.exe", QStringList() << "/k" << "title" << "The Child Process");
```

### `(since 6.6) enum class UnixProcessFlag { CloseFileDescriptors, CreateNewSession, DisconnectControllingTerminal, IgnoreSigPipe, ResetIds, …, DisableCoreDumps }`

**作用与语义：**

这些标志可用于`UnixProcessParameters` `flags`领域。
- `QProcess::UnixProcessFlag::CloseFileDescriptors`：`0x0010`;关闭所有超过`lowestFileDescriptorToClose`定义阈值的文件描述符，防止父进程中当前开放的任何描述符意外泄漏给子进程。`stdin`、`stdout`和`stderr`文件描述符永远不会关闭。
- `QProcess::UnixProcessFlag::CreateNewSession (since Qt 6.7)`：`0x0040`;通过调用`setsid(2)`启动一个新的进程会话。这允许子进程比当前进程所在的会话更长。这是`startDetached()`允许进程脱离的步骤之一，也是进程守护进程的守护进程步骤之一。
- `QProcess::UnixProcessFlag::DisconnectControllingTerminal (since Qt 6.7)`：`0x0080`;请求进程断开与其控制终端的连接（如果有的话）。如果没有，则不会发生任何事。仍然连接到控制终端的进程，如果终端关闭，可能会收到挂断（Hang Up，`SIGHUP`）信号，或者其他终端控制信号（`SIGTSTP`、`SIGTTIN`、`SIGTTOU`）之一。注意，在某些操作系统上，进程只有在是会话领导者时才可能断开与控制终端的连接，这意味着可能需要使用`CreateNewSession`标志。同样，这也是进程守护进程的一个步骤。
- `QProcess::UnixProcessFlag::IgnoreSigPipe`：`0x0002`;即使`ResetSignalHandlers`标志已设置，也始终将`SIGPIPE`信号设置为忽略（`SIG_IGN`）。默认情况下，如果子节点在相应通道被`QProcess::closeReadChannel()`关闭后尝试写入其标准输出或标准错误，会收到`SIGPIPE`信号并立即终止;使用此标志时，写操作在没有信号的情况下失败，子节点可以继续执行。
- `QProcess::UnixProcessFlag::ResetIds (since Qt 6.7)`：`0x0100`;丢弃当前进程可能仍保留的任何有效用户或组ID（参见`setuid(2)`和`setgid(2)`及`QCoreApplication::setSetuidAllowed()`）。如果当前进程是setuid或setgid，且不希望子进程保留提升权限，这非常有用。
- `QProcess::UnixProcessFlag::ResetSignalHandlers`：`0x0001`;将所有 Unix 信号处理程序重置回默认状态（即将 `SIG_DFL` 传递给 `signal(2)`）。该标志有助于确保任何被忽略（`SIG_IGN`）信号不会影响子信号的行为。
- `QProcess::UnixProcessFlag::UseVFork`：`0x0020`;请求`QProcess`使用 `vfork(2)` 启动子进程。使用此标志表示带 `setChildProcessModifier()` 的回调函数可在`vfork(2)`的子端安全执行;也就是说，回调不会修改任何非本地变量（无论是直接还是通过调用的函数），也不会尝试与父进程通信。它是实现定义的`QProcess`是否实际使用`vfork(2)`以及`vfork(2)`是否与标准`fork(2)`不同。
- `QProcess::UnixProcessFlag::DisableCoreDumps (since Qt 6.9)`：`0x0200`;请求`QProcess`禁用子进程中的核心转储。如果执行的可执行文件可能会崩溃，但用户和维护者不愿意针对这些条件生成错误报告（例如，可执行文件是测试进程），这很有用。该设置不影响崩溃进程的 `exitStatus()`。它通过将核心转储资源软限制设置为零来实现，意味着应用程序仍可将该变更提高到硬上限。
该枚举于Qt 6.6引入。
UnixProcessFlags 类型是 QFlags 的 typedef<UnixProcessFlag>。它存储 UnixProcessFlag 值的 OR 组合。

### `flags UnixProcessFlags`

**作用与语义：**

这些标志可用于`UnixProcessParameters` `flags`领域。
- `QProcess::UnixProcessFlag::CloseFileDescriptors`：`0x0010`;关闭所有超过`lowestFileDescriptorToClose`定义阈值的文件描述符，防止父进程中当前开放的任何描述符意外泄漏给子进程。`stdin`、`stdout`和`stderr`文件描述符永远不会关闭。
- `QProcess::UnixProcessFlag::CreateNewSession (since Qt 6.7)`：`0x0040`;通过调用`setsid(2)`启动一个新的进程会话。这允许子进程比当前进程所在的会话更长。这是`startDetached()`允许进程脱离的步骤之一，也是进程守护进程的守护进程步骤之一。
- `QProcess::UnixProcessFlag::DisconnectControllingTerminal (since Qt 6.7)`：`0x0080`;请求进程断开与其控制终端的连接（如果有的话）。如果没有，则不会发生任何事。仍然连接到控制终端的进程，如果终端关闭，可能会收到挂断（Hang Up，`SIGHUP`）信号，或者其他终端控制信号（`SIGTSTP`、`SIGTTIN`、`SIGTTOU`）之一。注意，在某些操作系统上，进程只有在是会话领导者时才可能断开与控制终端的连接，这意味着可能需要使用`CreateNewSession`标志。同样，这也是进程守护进程的一个步骤。
- `QProcess::UnixProcessFlag::IgnoreSigPipe`：`0x0002`;即使`ResetSignalHandlers`标志已设置，也始终将`SIGPIPE`信号设置为忽略（`SIG_IGN`）。默认情况下，如果子节点在相应通道被`QProcess::closeReadChannel()`关闭后尝试写入其标准输出或标准错误，会收到`SIGPIPE`信号并立即终止;使用此标志时，写操作在没有信号的情况下失败，子节点可以继续执行。
- `QProcess::UnixProcessFlag::ResetIds (since Qt 6.7)`：`0x0100`;丢弃当前进程可能仍保留的任何有效用户或组ID（参见`setuid(2)`和`setgid(2)`及`QCoreApplication::setSetuidAllowed()`）。如果当前进程是setuid或setgid，且不希望子进程保留提升权限，这非常有用。
- `QProcess::UnixProcessFlag::ResetSignalHandlers`：`0x0001`;将所有 Unix 信号处理程序重置回默认状态（即将 `SIG_DFL` 传递给 `signal(2)`）。该标志有助于确保任何被忽略（`SIG_IGN`）信号不会影响子信号的行为。
- `QProcess::UnixProcessFlag::UseVFork`：`0x0020`;请求`QProcess`使用 `vfork(2)` 启动子进程。使用此标志表示带 `setChildProcessModifier()` 的回调函数可在`vfork(2)`的子端安全执行;也就是说，回调不会修改任何非本地变量（无论是直接还是通过调用的函数），也不会尝试与父进程通信。它是实现定义的`QProcess`是否实际使用`vfork(2)`以及`vfork(2)`是否与标准`fork(2)`不同。
- `QProcess::UnixProcessFlag::DisableCoreDumps (since Qt 6.9)`：`0x0200`;请求`QProcess`禁用子进程中的核心转储。如果执行的可执行文件可能会崩溃，但用户和维护者不愿意针对这些条件生成错误报告（例如，可执行文件是测试进程），这很有用。该设置不影响崩溃进程的 `exitStatus()`。它通过将核心转储资源软限制设置为零来实现，意味着应用程序仍可将该变更提高到硬上限。
该枚举于Qt 6.6引入。
UnixProcessFlags 类型是 QFlags 的 typedef<UnixProcessFlag>。它存储 UnixProcessFlag 值的 OR 组合。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

### 状态和错误边界

QObject 派生对象的状态通常通过属性、状态查询函数和信号变化共同表达。信号是通知，不是返回值；收到通知后应读取当前状态并处理异常路径，不能假设每个信号只会出现一次。

### 线程边界

QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

### 最容易出现的错误

不要把用户输入直接拼进命令字符串；注意工作目录和环境变量；startDetached 后无法读取输出；阻塞 waitFor... 不要放在 GUI 主线程。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QProcess` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
