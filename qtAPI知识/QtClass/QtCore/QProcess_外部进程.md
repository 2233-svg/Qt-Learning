# Qt QProcess：启动和管理外部进程

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QProcess>`  
> 所属模块：`Qt6::Core`  
> 继承：`QIODevice`  
> 类型性质：QObject 异步外部进程控制器  
> 相关类型：`QProcessEnvironment`、`QIODevice`、`QDeadlineTimer`

## 1. 它解决什么问题

`QProcess` 把一个外部程序表示成 Qt 对象，并提供：

- 启动参数和工作目录配置；
- 子进程环境设置；
- 标准输入、标准输出、标准错误的管道访问；
- 异步状态和完成信号；
- 同步等待接口；
- 温和终止和强制终止；
- 标准输出重定向、错误流合并和进程间管道连接。

它适合调用编译器、脚本解释器、命令行工具、辅助服务和平台程序。典型流程是：

```text
配置 program / arguments / environment / workingDirectory
              |
              v
          start()
              |
              +-- started / errorOccurred
              +-- readyReadStandardOutput / readyReadStandardError
              +-- finished
              |
              v
       读取结果，检查 exitCode / exitStatus
```

`QProcess` 不是 shell。它直接创建进程并传递参数，不会自动解析管道符、重定向、环境变量替换或通配符。需要 shell 语义时，必须显式启动对应的 shell，并把命令作为 shell 的参数传入。

## 2. 它不是什么

`QProcess` 不是：

- Qt 内部线程；
- shell 脚本解释器；
- 进程池；
- 远程执行器；
- 安全沙箱；
- 自动把子进程输出转换成文本的解析器；
- 让 GUI 线程可以无限等待而不冻结界面的工具。

外部程序路径、参数和环境可能来自用户输入。启动前应做白名单、参数分离和权限检查，不要为了拼接命令而把不可信字符串交给 shell。

## 3. 构建与包含

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

```cpp
#include <QProcess>
```

`QProcess` 依赖 Qt 的 `Core` 模块和平台进程支持。类对象通常由父 QObject 管理，也可以作为局部对象使用。

## 4. 最小异步使用

```cpp
#include <QProcess>

auto *process = new QProcess(parent);

QObject::connect(process, &QProcess::readyReadStandardOutput,
                 process, [process] {
    const QByteArray output = process->readAllStandardOutput();
    consumeOutput(output);
});

QObject::connect(process, &QProcess::errorOccurred,
                 process, [process](QProcess::ProcessError error) {
    reportProcessError(error, process->errorString());
});

QObject::connect(process, &QProcess::finished,
                 process, [process](int exitCode,
                                    QProcess::ExitStatus status) {
    const QByteArray errorOutput =
        process->readAllStandardError();
    handleFinished(exitCode, status, errorOutput);
    process->deleteLater();
});

process->start(QStringLiteral("tool"),
               {QStringLiteral("--version")});
```

异步模式需要对象所属线程能够处理事件。一般把 `QProcess` 放在有事件循环的线程中，并通过信号响应输出、错误和完成状态。

## 5. 进程状态机

### 5.1 `NotRunning`

对象尚未启动进程，或进程已经退出。此时可以配置下一次启动的程序、参数、环境和工作目录。

### 5.2 `Starting`

Qt 正在创建进程和建立管道。此时不要把“已经运行”当成事实；等待 `started()` 或调用 `waitForStarted()` 确认。

### 5.3 `Running`

进程已经启动。此时可以写入标准输入、读取输出、关闭写通道、等待完成或请求终止。

状态变化通过 `stateChanged()` 通知。不要只靠定时器轮询 `state()`，除非确实处于没有事件循环的特殊同步环境。

## 6. 启动方式和参数边界

### 6.1 `start(program, arguments)` 优先用于结构化参数

```cpp
process.start(
    QStringLiteral("compiler"),
    {QStringLiteral("--input"),
     inputFile,
     QStringLiteral("--output"),
     outputFile});
```

`arguments` 的每个字符串都是一个逻辑参数。Qt 负责把它们传给平台进程创建 API；调用方不需要为普通空格参数手工加引号。

### 6.2 不要把整条命令当作一个参数

```cpp
// 容易出错：整个字符串只是一个 program 或一个参数
process.start(QStringLiteral("compiler --input file.txt"));
```

需要结构化传参时，拆成 `program` 和 `QStringList arguments`。只有明确需要命令字符串兼容格式时，才使用 `startCommand()` 或 `splitCommand()`。

### 6.3 `startCommand()` 不是 shell

```cpp
process.startCommand(
    QStringLiteral("compiler --input \"file with spaces.txt\""));
```

它按 Qt 的命令字符串规则拆分参数，但不会执行 shell 的 `|`、`>`、`&&`、变量展开或通配符。要执行 shell 语法，应显式启动 `sh -c`、`cmd /c` 或对应平台的命令解释器，并认真处理不可信输入。

### 6.4 `start()` 重载的配置来源

```cpp
process.setProgram(program);
process.setArguments(arguments);
process.start();
```

无参数 `start()` 使用对象当前保存的 program、arguments 和配置。带参数的 `start(program, arguments, mode)` 会设置本次启动的程序和参数。

正在运行或启动中的对象不能被当作可随意重配置的普通值对象。需要重新启动时，应先等待结束、终止并确认状态，再配置下一次启动。

## 7. 标准输入、输出和错误

### 7.1 默认是独立管道

`SeparateChannels` 是默认的进程通道模式。标准输出和标准错误分别可通过：

```cpp
process.readAllStandardOutput();
process.readAllStandardError();
```

读取。可以连接 `readyReadStandardOutput()` 和 `readyReadStandardError()` 分别处理。

### 7.2 合并通道

```cpp
process.setProcessChannelMode(
    QProcess::MergedChannels);
```

标准错误会并入标准输出通道。之后不要再假设两类内容能被独立读取；统一从当前读通道获取。

### 7.3 转发通道

`ForwardedChannels`、`ForwardedOutputChannel` 和 `ForwardedErrorChannel` 会把子进程输出转发到父进程的对应标准流，而不是保存在 QProcess 的内部读取缓冲中。转发的那部分内容不应再期待通过 `readAllStandardOutput()` 或 `readAllStandardError()` 取得。

### 7.4 写入标准输入

在 `ManagedInputChannel` 下，可以像使用 `QIODevice` 一样调用：

```cpp
process.write(input);
process.closeWriteChannel();
```

`closeWriteChannel()` 表示不再提供输入，通常会向子进程的标准输入发送 EOF。很多命令行工具只有读到 EOF 后才开始输出最终结果；忘记关闭写通道可能导致双方互相等待。

`ForwardedInputChannel` 把父进程的标准输入转给子进程，不适合继续通过 `QProcess::write()` 管理输入。

### 7.5 读取是字节流，不是消息边界

`readyRead...` 只表示当前有可读字节，不保证一次信号对应一行、一个 JSON 或一条完整业务消息。调用方应维护缓冲区，按协议组帧，并处理 UTF-8 或其他编码的跨块边界。

## 8. QIODevice 语义和读写边界

`QProcess` 是顺序设备：

- 不支持随机定位；
- `read()`、`readAll()`、`readLine()` 受当前读通道影响；
- `write()` 写入子进程的标准输入；
- `bytesToWrite()` 表示尚未写出的数据；
- `waitForReadyRead()` 和 `waitForBytesWritten()` 是阻塞式等待。

如果使用异步信号，通常不需要在每次信号中调用 `waitForReadyRead()`。混用异步回调和阻塞等待时，要特别注意线程事件循环和重入顺序。

## 9. 环境、工作目录和重定向

### 9.1 工作目录

```cpp
process.setWorkingDirectory(directory);
```

它设置子进程启动时看到的当前目录，不会改变父进程的当前目录。相对路径参数和子进程内部的相对文件访问会以该目录为基准。

### 9.2 环境

优先使用 `QProcessEnvironment`：

```cpp
QProcessEnvironment environment =
    QProcessEnvironment::systemEnvironment();
environment.insert(QStringLiteral("APP_MODE"),
                   QStringLiteral("test"));
process.setProcessEnvironment(environment);
```

不要把环境字符串列表当作 shell 命令。环境中的敏感令牌也不要无意写入日志或传给不可信的子进程。

`setEnvironment()` / `environment()` 是较早的字符串列表接口；新代码优先用 `setProcessEnvironment()` / `processEnvironment()`，因为键值语义更清晰。

### 9.3 输出文件

```cpp
process.setStandardOutputFile(
    outputPath, QIODeviceBase::Truncate);
process.setStandardErrorFile(
    errorPath, QIODeviceBase::Truncate);
```

设置后，输出由 Qt 重定向到文件，不再按普通内部管道缓冲读取。`Truncate` 和 `Append` 会影响文件打开方式；路径权限和目录存在性仍需调用方处理。

### 9.4 进程间管道

```cpp
first.setStandardOutputProcess(&second);
```

把一个 `QProcess` 的标准输出连接到另一个 `QProcess` 的标准输入。两个进程的启动顺序、生命周期和错误处理仍由调用方负责；这不是 shell pipeline，也不会自动替你处理失败回收。

## 10. 终止、关闭和析构

### 10.1 `terminate()`：请求正常结束

`terminate()` 向进程发送平台相关的温和终止请求。子进程可以忽略、延迟或不支持这个请求，调用后不保证立即结束。

### 10.2 `kill()`：强制结束

`kill()` 使用更强的终止方式。它可能让子进程没有机会刷新文件、保存状态或执行清理，因此只应在正常终止无效、超时或安全策略要求时使用。

### 10.3 `close()` 不是“优雅终止”

`close()` 关闭 QProcess 的设备通道；它不是对业务状态的保存协议，也不等价于等待子进程正常退出。要控制进程生命周期，使用 `terminate()`、`kill()` 和 `waitForFinished()`。

### 10.4 析构运行中的 QProcess

不要把一个仍在运行的 `QProcess` 当作无害局部对象直接销毁。Qt 会处理其关联进程和通道，但析构运行中进程可能导致终止和阻塞，且会丢失后续异步输出。更清晰的做法是先设计完成、超时和终止路径，再销毁对象。

### 10.5 先读完剩余输出

收到 `finished()` 后，内部缓冲中仍可能有尚未读取的输出。处理完成信号时应读取 `readAllStandardOutput()` 和 `readAllStandardError()` 的剩余数据，再根据退出码和退出状态决定结果。

## 11. 异步与同步两种控制风格

### 11.1 异步风格适合 GUI 和服务对象

```cpp
connect(&process, &QProcess::finished,
        this, &Runner::onFinished);
process.start(program, arguments);
```

信号槽让线程继续处理界面和其他事件。必须为每次启动处理：

- `started()`；
- `errorOccurred()`；
- 输出可读信号；
- `finished()`；
- 目标对象销毁和取消操作。

### 11.2 同步风格适合短命令行任务

```cpp
process.start(program, arguments);
if (!process.waitForStarted(5000))
    return failure(process.errorString());

if (!process.waitForFinished(30000))
    return timeout();

const QByteArray output =
    process.readAllStandardOutput();
```

等待函数会阻塞调用线程。不要在 GUI 线程对未知耗时的进程使用无限等待；不要把阻塞等待放在持有 mutex 的代码中，否则子进程完成路径可能无法取得该锁。

### 11.3 超时不是自动终止

`waitForFinished(msecs)` 返回 `false` 只表示在给定时间内没有完成，通常还要由调用方决定：

1. 读取或记录错误；
2. 调用 `terminate()`；
3. 再等待一个宽限期；
4. 仍未退出时调用 `kill()`；
5. 最后确认状态并清理对象。

## 12. 退出结果和错误处理

### 12.1 启动失败和运行崩溃不同

- `FailedToStart`：程序无法启动，例如路径、权限或平台创建失败；
- `Crashed`：进程启动过但异常终止；
- `Timedout`：等待操作超时；
- `ReadError`：读取进程输出失败；
- `WriteError`：向进程写入失败；
- `UnknownError`：其他未分类错误。

错误信号和 `error()` 用于描述 QProcess 观察到的错误；它们不等同于子进程自己的退出码。

### 12.2 `exitCode()` 和 `exitStatus()`

只有进程结束后，退出码和退出状态才有完整业务意义：

- `NormalExit` 表示正常退出路径；
- `CrashExit` 表示异常终止；
- `exitCode()` 是子进程报告的整数退出码。

“正常退出”不等于业务成功。应按工具约定检查退出码；`0` 常表示成功，但不是 Qt 强制规定的通用协议。

### 12.3 `processId()`

进程成功启动后可以取得平台进程 ID。它只适合作为诊断、日志或平台 API 的句柄线索，不应单独作为“进程仍然可用”的证明；状态变化和完成信号才是 QProcess 的主要生命周期依据。

## 13. 平台相关扩展

### 13.1 Windows `CreateProcessArguments`

Windows 构建提供 `CreateProcessArguments` 和 `setCreateProcessArgumentsModifier()`。modifier 可以在 Qt 调用 Windows `CreateProcess` 前调整启动参数，例如创建控制台或修改 startup info。

这些指针只在 modifier 调用期间有效。不要保存 `arguments`、`startupInfo`、`processInformation` 或相关指针到异步回调中。修改必须符合 Windows API 的生命周期和所有权规则。

### 13.2 Unix `childProcessModifier`

Unix 构建提供 `setChildProcessModifier()`，用于在子进程执行阶段进行低层配置，例如调整文件描述符或会话。该回调运行在非常敏感的进程创建边界，不能把普通 Qt 对象操作、分配、锁和复杂日志逻辑随意放进去。

Qt 6.7 起可以调用：

```cpp
process.failChildProcessModifier(
    "dup2 failed", errno);
```

报告 modifier 失败。该函数不会正常返回，调用前应确保描述字符串和错误值符合 API 要求。

### 13.3 Unix flags

Qt 6.6 起的 `UnixProcessParameters` 可以设置：

- `ResetSignalHandlers`；
- `IgnoreSigPipe`；
- `CloseFileDescriptors`；
- `UseVFork`；
- `CreateNewSession`；
- `DisconnectControllingTerminal`；
- `ResetIds`；
- `DisableCoreDumps`。

这些选项改变子进程创建语义，属于平台策略，不应在不了解部署环境的情况下默认打开。

## 14. 逐项 API 语义

### 14.1 构造和析构

```cpp
explicit QProcess(QObject *parent = nullptr);
virtual ~QProcess();
```

构造一个尚未运行的 QObject。父对象负责 QObject 所有权；析构时不要假设异步工作还会继续。

### 14.2 `start()` 三种使用入口

```cpp
void start(const QString &program,
           const QStringList &arguments = {},
           OpenMode mode = ReadWrite);
void start(OpenMode mode = ReadWrite);
```

第一种设置程序和参数后启动，第二种使用此前通过 setter 配置的程序和参数。`OpenMode` 决定 QProcess 设备通道是否可读写。

### 14.3 `startCommand()`

```cpp
void startCommand(const QString &command,
                  OpenMode mode = ReadWrite);
```

按 Qt 的命令字符串规则拆分并启动，不经过 shell。需要 shell 特性时显式启动 shell。

### 14.4 `startDetached()`

```cpp
bool startDetached(qint64 *pid = nullptr);
static bool startDetached(const QString &program,
                          const QStringList &arguments = {},
                          const QString &workingDirectory = QString(),
                          qint64 *pid = nullptr);
```

启动与当前 QProcess 生命周期分离的进程。返回值表示创建是否成功，`pid` 可选接收平台进程 ID。分离后不能通过当前 QProcess 读取输出、接收 `finished()` 或控制完整生命周期。

### 14.5 `open()` 和 `close()`

```cpp
bool open(OpenMode mode = ReadWrite) override;
void close() override;
```

`open()` 使用当前配置启动进程并打开设备通道；`close()` 关闭设备通道。它们不能替代完整的进程完成和终止协议。

### 14.6 程序和参数

```cpp
QString program() const;
void setProgram(const QString &program);
QStringList arguments() const;
void setArguments(const QStringList &arguments);
```

读取或设置下一次启动使用的程序和参数。参数应使用独立字符串，不要把 shell 语法塞进单个参数。

### 14.7 通道模式

```cpp
ProcessChannelMode processChannelMode() const;
void setProcessChannelMode(ProcessChannelMode mode);
InputChannelMode inputChannelMode() const;
void setInputChannelMode(InputChannelMode mode);
ProcessChannel readChannel() const;
void setReadChannel(ProcessChannel channel);
```

分别控制标准输出/错误的合并或转发、标准输入的管理方式，以及当前读取哪个输出通道。

### 14.8 `closeReadChannel()` 和 `closeWriteChannel()`

```cpp
void closeReadChannel(ProcessChannel channel);
void closeWriteChannel();
```

关闭指定读通道或子进程标准输入通道。关闭写通道常用于向会等待 EOF 的命令行程序表明输入已经结束。

### 14.9 文件和进程管道

```cpp
void setStandardInputFile(const QString &fileName);
void setStandardOutputFile(const QString &fileName,
                           OpenMode mode = Truncate);
void setStandardErrorFile(const QString &fileName,
                          OpenMode mode = Truncate);
void setStandardOutputProcess(QProcess *destination);
```

把标准流绑定到文件或另一个 QProcess。重定向后，不应再把该流当作内部可读缓冲；destination 的生命周期和启动协议由调用方负责。

### 14.10 工作目录和环境

```cpp
QString workingDirectory() const;
void setWorkingDirectory(const QString &dir);
void setEnvironment(const QStringList &environment);
QStringList environment() const;
void setProcessEnvironment(
    const QProcessEnvironment &environment);
QProcessEnvironment processEnvironment() const;
```

配置子进程的当前目录和环境。新代码优先使用 `QProcessEnvironment` 版本；环境列表接口适合兼容旧代码。

### 14.11 状态和错误

```cpp
ProcessError error() const;
ProcessState state() const;
qint64 processId() const;
```

查询最近错误、当前状态和平台进程 ID。状态查询不替代异步信号，进程 ID 也不等同于业务完成状态。

### 14.12 等待函数

```cpp
bool waitForStarted(int msecs = 30000);
bool waitForReadyRead(int msecs = 30000) override;
bool waitForBytesWritten(int msecs = 30000) override;
bool waitForFinished(int msecs = 30000);
```

阻塞当前线程直到相应事件或超时。负超时通常表示无限等待；GUI、锁内和不受控外部程序场景要慎用。

### 14.13 标准输出和错误

```cpp
QByteArray readAllStandardOutput();
QByteArray readAllStandardError();
```

读取对应通道当前可用的全部字节。调用后数据从 QProcess 的对应缓冲中取出；仍需处理输出分块、编码和剩余数据。

### 14.14 结果

```cpp
int exitCode() const;
ExitStatus exitStatus() const;
```

查询进程退出码和退出方式。应在 `finished()` 或 `waitForFinished()` 成功后使用，并结合工具自身的退出码约定判断业务结果。

### 14.15 `terminate()` 和 `kill()`

```cpp
void terminate();
void kill();
```

前者请求进程正常终止，后者强制终止。两者都不替代等待和结果检查；强制终止可能丢失子进程清理和输出。

### 14.16 静态辅助函数

```cpp
static int execute(const QString &program,
                   const QStringList &arguments = {});
static QStringList systemEnvironment();
static QString nullDevice();
static QStringList splitCommand(QStringView command);
```

- `execute()` 同步启动并等待，返回执行结果；
- `systemEnvironment()` 返回当前系统环境的字符串列表；
- `nullDevice()` 返回平台空设备路径；
- `splitCommand()` 按 Qt 规则把命令字符串拆成参数。

这些函数不自动提供安全校验，也不让字符串变成 shell。

### 14.17 Windows modifier

```cpp
QString nativeArguments() const;
void setNativeArguments(const QString &arguments);
CreateProcessArgumentModifier
createProcessArgumentsModifier() const;
void setCreateProcessArgumentsModifier(
    CreateProcessArgumentModifier modifier);
```

用于 Windows 原生参数和 `CreateProcess` 参数修改。只在 Windows 可用，modifier 中的结构体指针不能保存到回调外。

### 14.18 Unix modifier

```cpp
std::function<void(void)> childProcessModifier() const;
void setChildProcessModifier(
    const std::function<void(void)> &modifier);
void failChildProcessModifier(
    const char *description, int error = 0) noexcept;
UnixProcessParameters unixProcessParameters() const noexcept;
void setUnixProcessParameters(
    const UnixProcessParameters &params);
void setUnixProcessParameters(UnixProcessFlags flagsOnly);
```

用于 Unix 子进程创建阶段的低层配置。回调运行环境受平台进程创建约束；只放置必要、可在该阶段安全执行的操作。

### 14.19 QIODevice 重写和受保护扩展点

```cpp
qint64 bytesToWrite() const override;
bool isSequential() const override;
qint64 readData(char *data, qint64 maxlen) override;
qint64 writeData(const char *data, qint64 len) override;
void setProcessState(ProcessState state);
```

前四项实现顺序设备的 QIODevice 契约。`setProcessState()` 是受保护扩展点，派生类重写或调用时必须保持 QProcess 状态机和信号契约。

### 14.20 信号

```cpp
void started();
void finished(int exitCode,
              QProcess::ExitStatus exitStatus = NormalExit);
void errorOccurred(QProcess::ProcessError error);
void stateChanged(QProcess::ProcessState state);
void readyReadStandardOutput();
void readyReadStandardError();
```

这些信号是异步控制的主要入口。`started()` 只表示进程已启动，`finished()` 才表示子进程退出；输出信号只表示有字节可读，不表示业务消息完整。

## 15. 实际使用模式

### 15.1 异步执行并收集结果

```cpp
auto *process = new QProcess(this);

connect(process, &QProcess::readyReadStandardOutput,
        this, [process] {
    outputBuffer += process->readAllStandardOutput();
});

connect(process, &QProcess::finished,
        this, [process](int code,
                        QProcess::ExitStatus status) {
    outputBuffer += process->readAllStandardOutput();
    errorBuffer += process->readAllStandardError();
    finishJob(code, status, outputBuffer, errorBuffer);
    process->deleteLater();
});

process->start(program, arguments);
```

真实代码还应处理 `errorOccurred()` 和重复启动。

### 15.2 通过 stdin 发送完整输入

```cpp
process.start(program, arguments);
if (!process.waitForStarted())
    return false;

process.write(input);
process.closeWriteChannel();

if (!process.waitForFinished(30000))
    return false;
```

只要子进程协议以 EOF 作为输入结束标志，就必须调用 `closeWriteChannel()`。

### 15.3 超时终止策略

```cpp
if (!process.waitForFinished(5000)) {
    process.terminate();
    if (!process.waitForFinished(1000))
        process.kill();
}
```

终止后仍应读取剩余输出并检查最终状态。对可能生成子进程的工具，还要考虑平台上的子进程树清理问题。

## 16. 常见错误

### 16.1 把 QProcess 当 shell

把 `a | b > out.txt` 直接传给 `startCommand()` 不会自动得到 shell 管道。应显式启动 shell，或使用 `setStandardOutputProcess()` 建立 Qt 管道。

### 16.2 只读标准输出，不读标准错误

子进程如果大量写标准错误，而父进程只读取标准输出，错误管道可能填满并阻塞子进程。需要时分别连接并持续读取两个通道，或选择合并/转发模式。

### 16.3 忘记关闭 stdin

很多过滤器会一直等待更多输入。写完后不关闭写通道，`waitForFinished()` 可能一直等到超时。

### 16.4 在 GUI 线程无限等待

阻塞等待会冻结事件处理和界面刷新。GUI 场景优先使用信号；必须等待时设置有限超时并提供取消路径。

### 16.5 把超时当成子进程已经结束

`waitForFinished()` 返回 `false` 可能只是超时。先检查 `state()`，再决定继续等待、terminate 还是 kill。

### 16.6 把退出码当成 QProcess::ProcessError

进程退出码是子进程协议；`ProcessError` 是 Qt 观察到的错误。两者要分别处理。

### 16.7 在持有锁时等待子进程

子进程完成回调或读取路径可能需要同一线程或同一把锁。不要在持锁期间调用不可控的 `waitForFinished()`。

### 16.8 不限制外部程序来源

程序路径、参数和环境可能造成命令注入、任意程序执行或敏感信息泄漏。优先使用固定可执行文件和独立参数，必要时做白名单和权限降级。

## API 速查表
### 17.1 状态和生命周期

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `QProcess(parent)` | 创建进程控制对象 | 不会启动子进程；父对象管理 QObject 生命周期 |
| `~QProcess()` | 销毁控制对象和关联通道 | 不要让运行中的进程在未设计的析构路径中结束 |
| `state()` | 查询 `NotRunning` / `Starting` / `Running` | 状态查询不替代状态信号 |
| `processId()` | 查询平台进程 ID | 只作诊断和平台线索，不是完成状态 |
| `error()` | 查询最近的 QProcess 错误 | 与子进程退出码分开处理 |

### 17.2 启动和终止

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `start(program, arguments, mode)` | 用结构化参数异步启动 | 每个参数独立传入，不要手工拼 shell 字符串 |
| `start(mode)` | 使用已配置程序和参数启动 | 启动前确认 setter 状态 |
| `startCommand(command, mode)` | 按 Qt 命令字符串规则拆分并启动 | 不执行 shell 语法 |
| `open(mode)` | 通过 QIODevice 接口启动并打开通道 | 不替代完成和错误处理 |
| `startDetached(...)` | 启动与当前对象分离的进程 | 无法通过当前对象读取输出或接收完成信号 |
| `terminate()` | 请求温和终止 | 可能被忽略或延迟 |
| `kill()` | 强制终止 | 可能丢失子进程清理和输出 |
| `close()` | 关闭设备通道 | 不等价于优雅终止 |

### 17.3 程序、目录和环境

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `program()` / `setProgram()` | 查询或设置可执行文件 | 固定来源更安全 |
| `arguments()` / `setArguments()` | 查询或设置参数列表 | 每个元素是一个逻辑参数 |
| `workingDirectory()` / `setWorkingDirectory()` | 查询或设置子进程工作目录 | 不改变父进程目录 |
| `setProcessEnvironment()` / `processEnvironment()` | 设置或查询结构化环境 | 新代码优先使用 `QProcessEnvironment` |
| `setEnvironment()` / `environment()` | 使用字符串列表设置或查询环境 | 旧式接口，注意 `NAME=VALUE` 格式 |
| `setStandardInputFile()` | 将标准输入重定向到文件 | 不再由 QProcess 写入管道 |
| `setStandardOutputFile()` | 将标准输出重定向到文件 | 注意 `Truncate` / `Append` |
| `setStandardErrorFile()` | 将标准错误重定向到文件 | 与标准输出独立配置 |
| `setStandardOutputProcess()` | 把输出连接到另一个 QProcess | 生命周期和启动顺序由调用方负责 |

### 17.4 通道和 QIODevice I/O

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `processChannelMode()` / `setProcessChannelMode()` | 查询或设置输出分离、合并、转发 | 转发后的数据不能按内部缓冲读取 |
| `inputChannelMode()` / `setInputChannelMode()` | 查询或设置标准输入管理方式 | forwarded 输入不适合调用 `write()` |
| `readChannel()` / `setReadChannel()` | 选择当前读取标准输出或错误 | 影响 QIODevice 通用读取 |
| `closeReadChannel()` | 关闭指定读通道 | 关闭后不能继续从该通道读取 |
| `closeWriteChannel()` | 关闭子进程 stdin | 常用于发送 EOF |
| `readAllStandardOutput()` | 读取全部可用标准输出字节 | 不保证消息边界 |
| `readAllStandardError()` | 读取全部可用标准错误字节 | 不要让错误管道无人读取 |
| `bytesToWrite()` | 查询待写字节数 | 异步写入可能尚未到达子进程 |
| `waitForReadyRead()` | 阻塞等待输入可读 | 不要在 GUI 或锁内无限等待 |
| `waitForBytesWritten()` | 阻塞等待写入完成 | 超时要有后续处理 |

### 17.5 等待和结果

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `waitForStarted()` | 等待启动完成或失败 | 阻塞当前线程 |
| `waitForFinished()` | 等待进程退出 | 超时不等于已退出 |
| `exitCode()` | 读取子进程退出码 | 结合工具协议判断成功 |
| `exitStatus()` | 判断正常退出或崩溃退出 | `NormalExit` 不保证业务成功 |
| `started()` | 通知启动完成 | 异步风格入口 |
| `finished()` | 通知进程退出 | 先读取剩余输出再收尾 |
| `errorOccurred()` | 通知 QProcess 错误 | 与退出码分开记录 |
| `stateChanged()` | 通知进程状态变化 | 可替代轮询 |
| `readyReadStandardOutput()` | 通知标准输出有数据 | 只表示字节可读，不表示完整消息 |
| `readyReadStandardError()` | 通知标准错误有数据 | 持续读取以避免管道阻塞 |

### 17.6 静态和平台 API

| API | 作用 | 使用时重点注意 |
| --- | --- | --- |
| `execute()` | 同步执行程序并返回退出结果 | 会阻塞；不适合未知耗时 GUI 任务 |
| `systemEnvironment()` | 获取当前系统环境字符串列表 | 不要把敏感环境写入日志 |
| `nullDevice()` | 获取平台空设备路径 | 用于重定向而非跨平台硬编码 |
| `splitCommand()` | 按 Qt 规则拆分命令字符串 | 不执行 shell 展开 |
| Windows modifier API | 调整 `CreateProcess` 参数 | 指针只在 modifier 回调期间有效 |
| Unix modifier API | 调整子进程创建阶段参数 | 遵守 fork/vfork 阶段的低层安全约束 |

## 18. 一句话总结

`QProcess` 是带 QIODevice 管道的外部进程状态机：用结构化参数启动，按信号或有限等待处理输出、错误和完成，用 `terminate()` / `kill()` 明确终止策略。最容易出问题的边界是把它误当 shell、忽略标准错误或 stdin EOF、在 GUI/锁内阻塞等待，以及把 Qt 错误和子进程退出码混为一谈。
