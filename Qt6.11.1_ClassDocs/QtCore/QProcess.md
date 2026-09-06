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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 79 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `QProcess::CreateProcessArgumentModifier`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QProcess` 的配置属性。初始化或状态切换时通过 `setCreateProcessArgumentModifier(...)` 设置，之后用 `CreateProcessArgumentModifier()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:CreateProcessArgumentModifier`。
- 属性名：`QProcess`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QProcess::ExitStatus`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QProcess` 暴露的类型声明 `Exit、状态`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:ExitStatus`。
- 属性名：`QProcess`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QProcess::InputChannelMode`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QProcess` 暴露的类型声明 `Input、Channel、模式`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:InputChannelMode`。
- 属性名：`QProcess`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QProcess::ProcessChannel`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QProcess` 暴露的类型声明 `处理、Channel`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:ProcessChannel`。
- 属性名：`QProcess`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QProcess::ProcessChannelMode`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QProcess` 暴露的类型声明 `处理、Channel、模式`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:ProcessChannelMode`。
- 属性名：`QProcess`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QProcess::ProcessError`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QProcess` 暴露的类型声明 `处理、错误`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:ProcessError`。
- 属性名：`QProcess`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QProcess::ProcessState`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QProcess` 暴露的类型声明 `处理、State`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:ProcessState`。
- 属性名：`QProcess`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] enum class QProcess::UnixProcessFlagflags QProcess::UnixProcessFlags`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QProcess` 暴露的类型声明 `class`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:UnixProcessFlagflags QProcess::UnixProcessFlags`。
- 属性名：`QProcess`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QProcess::QProcess(QObject *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QProcess` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `parent`：类型为 `QObject *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QProcess::~QProcess()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QProcess` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringList QProcess::arguments() const`

**API 类别：** 成员函数说明

**中文解读：** `QProcess::arguments` 用于计算、查询或取得与“arguments”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QStringList`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStringList`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] qint64 QProcess::bytesToWrite() const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `bytesToWrite`，返回 `QProcess` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`qint64`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] std::function<void ()> QProcess::childProcessModifier() const`

**API 类别：** 成员函数说明

**中文解读：** `QProcess::void` 用于计算、查询或取得与“void”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `std::function<`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`std::function<`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] void QProcess::close()`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `close`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QProcess::closeReadChannel(QProcess::ProcessChannel channel)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `closeReadChannel`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数 `channel`：类型为 `QProcess::ProcessChannel`。没有默认值，调用时必须提供。传入 `QProcess::ProcessChannel` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QProcess::closeWriteChannel()`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `closeWriteChannel`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QProcess::CreateProcessArgumentModifier QProcess::createProcessArgumentsModifier() const`

**API 类别：** 成员函数说明

**中文解读：** `QProcess::createProcessArgumentsModifier` 用于计算、查询或取得与“创建、处理、Arguments、Modifier”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QProcess::CreateProcessArgumentModifier`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QProcess::CreateProcessArgumentModifier`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QProcess::ProcessError QProcess::error() const`

**API 类别：** 成员函数说明

**中文解读：** `QProcess::error` 用于计算、查询或取得与“错误”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QProcess::ProcessError`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QProcess::ProcessError`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QProcess::errorOccurred(QProcess::ProcessError error)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QProcess` 发出的通知信号 `errorOccurred`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `error`：类型为 `QProcess::ProcessError`。没有默认值，调用时必须提供。错误输出对象或错误状态。解析/执行后要检查它，而不能只看主返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] int QProcess::execute(const QString &program, const QStringList &arguments = {})`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `execute`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`int`。
- 参数 `program`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `arguments`：类型为 `const QStringList &`。默认值为 `{}`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QProcess::exitCode() const`

**API 类别：** 成员函数说明

**中文解读：** `QProcess::exitCode` 用于计算、查询或取得与“exit、Code”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QProcess::ExitStatus QProcess::exitStatus() const`

**API 类别：** 成员函数说明

**中文解读：** `QProcess::exitStatus` 用于计算、查询或取得与“exit、状态”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QProcess::ExitStatus`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QProcess::ExitStatus`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept, since 6.7] void QProcess::failChildProcessModifier(const char *description, int error = 0)`

**API 类别：** 成员函数说明

**中文解读：** `QProcess::failChildProcessModifier` 用于执行与“fail、Child、处理、Modifier”相关的操作。调用时要先确认当前状态和 `description`、`error` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `description`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `error`：类型为 `int`。默认值为 `0`。错误输出对象或错误状态。解析/执行后要检查它，而不能只看主返回值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QProcess::finished(int exitCode, QProcess::ExitStatus exitStatus = NormalExit)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QProcess` 发出的通知信号 `finished`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `exitCode`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `exitStatus`：类型为 `QProcess::ExitStatus`。默认值为 `NormalExit`。传入 `QProcess::ExitStatus` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QProcess::InputChannelMode QProcess::inputChannelMode() const`

**API 类别：** 成员函数说明

**中文解读：** `QProcess::inputChannelMode` 用于计算、查询或取得与“input、Channel、模式”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QProcess::InputChannelMode`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QProcess::InputChannelMode`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QProcess::isSequential() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isSequential`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QProcess::kill()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `kill`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QProcess::nativeArguments() const`

**API 类别：** 成员函数说明

**中文解读：** `QProcess::nativeArguments` 用于计算、查询或取得与“native、Arguments”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QProcess::nullDevice()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `nullDevice`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QProcess::open(QIODeviceBase::OpenMode mode = ReadWrite)`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `open`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`bool`。
- 参数 `mode`：类型为 `QIODeviceBase::OpenMode`。默认值为 `ReadWrite`。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QProcess::ProcessChannelMode QProcess::processChannelMode() const`

**API 类别：** 成员函数说明

**中文解读：** `QProcess::processChannelMode` 用于计算、查询或取得与“处理、Channel、模式”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QProcess::ProcessChannelMode`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QProcess::ProcessChannelMode`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QProcessEnvironment QProcess::processEnvironment() const`

**API 类别：** 成员函数说明

**中文解读：** `QProcess::processEnvironment` 用于计算、查询或取得与“处理、Environment”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QProcessEnvironment`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QProcessEnvironment`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qint64 QProcess::processId() const`

**API 类别：** 成员函数说明

**中文解读：** `QProcess::processId` 用于计算、查询或取得与“处理、Id”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qint64`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qint64`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QProcess::program() const`

**API 类别：** 成员函数说明

**中文解读：** `QProcess::program` 用于计算、查询或取得与“program”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray QProcess::readAllStandardError()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QProcess` 的核心操作 `readAllStandardError`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray QProcess::readAllStandardOutput()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QProcess` 的核心操作 `readAllStandardOutput`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QProcess::ProcessChannel QProcess::readChannel() const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QProcess` 的核心操作 `readChannel`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`QProcess::ProcessChannel`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] qint64 QProcess::readData(char *data, qint64 maxlen)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QProcess` 的核心操作 `readData`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`qint64`。
- 参数 `data`：类型为 `char *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `maxlen`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[private signal] void QProcess::readyReadStandardError()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QProcess` 的核心操作 `readyReadStandardError`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[private signal] void QProcess::readyReadStandardOutput()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QProcess` 的核心操作 `readyReadStandardOutput`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QProcess::setArguments(const QStringList &arguments)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setArguments`。调用它会改变 `QProcess` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `arguments`：类型为 `const QStringList &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] void QProcess::setChildProcessModifier(const std::function<void ()> &modifier)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setChildProcessModifier`。调用它会改变 `QProcess` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `modifier`：类型为 `const std::function<void ()> &`。没有默认值，调用时必须提供。传入 `const std::function<void ()> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QProcess::setCreateProcessArgumentsModifier(QProcess::CreateProcessArgumentModifier modifier)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setCreateProcessArgumentsModifier`。调用它会改变 `QProcess` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `modifier`：类型为 `QProcess::CreateProcessArgumentModifier`。没有默认值，调用时必须提供。传入 `QProcess::CreateProcessArgumentModifier` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QProcess::setInputChannelMode(QProcess::InputChannelMode mode)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setInputChannelMode`。调用它会改变 `QProcess` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `mode`：类型为 `QProcess::InputChannelMode`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QProcess::setNativeArguments(const QString &arguments)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setNativeArguments`。调用它会改变 `QProcess` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `arguments`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QProcess::setProcessChannelMode(QProcess::ProcessChannelMode mode)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setProcessChannelMode`。调用它会改变 `QProcess` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `mode`：类型为 `QProcess::ProcessChannelMode`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QProcess::setProcessEnvironment(const QProcessEnvironment &environment)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setProcessEnvironment`。调用它会改变 `QProcess` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `environment`：类型为 `const QProcessEnvironment &`。没有默认值，调用时必须提供。传入 `const QProcessEnvironment &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] void QProcess::setProcessState(QProcess::ProcessState state)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setProcessState`。调用它会改变 `QProcess` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `state`：类型为 `QProcess::ProcessState`。没有默认值，调用时必须提供。状态值或状态对象；它描述调用时的阶段，不能把某个状态下有效的 API 用到其他阶段。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QProcess::setProgram(const QString &program)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setProgram`。调用它会改变 `QProcess` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QProcess::setReadChannel(QProcess::ProcessChannel channel)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setReadChannel`。调用它会改变 `QProcess` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `channel`：类型为 `QProcess::ProcessChannel`。没有默认值，调用时必须提供。传入 `QProcess::ProcessChannel` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QProcess::setStandardErrorFile(const QString &fileName, QIODeviceBase::OpenMode mode = Truncate)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setStandardErrorFile`。调用它会改变 `QProcess` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `fileName`：类型为 `const QString &`。没有默认值，调用时必须提供。文件名或路径。优先使用 Qt 的路径 API 拼接和规范化，不要手写平台分隔符。
- 参数 `mode`：类型为 `QIODeviceBase::OpenMode`。默认值为 `Truncate`。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QProcess::setStandardInputFile(const QString &fileName)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setStandardInputFile`。调用它会改变 `QProcess` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `fileName`：类型为 `const QString &`。没有默认值，调用时必须提供。文件名或路径。优先使用 Qt 的路径 API 拼接和规范化，不要手写平台分隔符。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QProcess::setStandardOutputFile(const QString &fileName, QIODeviceBase::OpenMode mode = Truncate)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setStandardOutputFile`。调用它会改变 `QProcess` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `fileName`：类型为 `const QString &`。没有默认值，调用时必须提供。文件名或路径。优先使用 Qt 的路径 API 拼接和规范化，不要手写平台分隔符。
- 参数 `mode`：类型为 `QIODeviceBase::OpenMode`。默认值为 `Truncate`。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QProcess::setStandardOutputProcess(QProcess *destination)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setStandardOutputProcess`。调用它会改变 `QProcess` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `destination`：类型为 `QProcess *`。没有默认值，调用时必须提供。目标对象或目标位置；要确认目标可写、容量足够，并且不会与源数据发生不允许的重叠。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] void QProcess::setUnixProcessParameters(const QProcess::UnixProcessParameters &params)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setUnixProcessParameters`。调用它会改变 `QProcess` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `params`：类型为 `const QProcess::UnixProcessParameters &`。没有默认值，调用时必须提供。传入 `const QProcess::UnixProcessParameters &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] void QProcess::setUnixProcessParameters(QProcess::UnixProcessFlags flagsOnly)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setUnixProcessParameters`。调用它会改变 `QProcess` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `flagsOnly`：类型为 `QProcess::UnixProcessFlags`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QProcess::setWorkingDirectory(const QString &dir)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setWorkingDirectory`。调用它会改变 `QProcess` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `dir`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QStringList QProcess::splitCommand(QStringView command)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `splitCommand`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QStringList`。
- 参数 `command`：类型为 `QStringView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QProcess::start(const QString &program, const QStringList &arguments = {}, QIODeviceBase::OpenMode mode = ReadWrite)`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `start`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`void`。
- 参数 `program`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `arguments`：类型为 `const QStringList &`。默认值为 `{}`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `mode`：类型为 `QIODeviceBase::OpenMode`。默认值为 `ReadWrite`。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QProcess::start(QIODeviceBase::OpenMode mode = ReadWrite)`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `start`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`void`。
- 参数 `mode`：类型为 `QIODeviceBase::OpenMode`。默认值为 `ReadWrite`。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] void QProcess::startCommand(const QString &command, QIODeviceBase::OpenMode mode = ReadWrite)`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `startCommand`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`void`。
- 参数 `command`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `mode`：类型为 `QIODeviceBase::OpenMode`。默认值为 `ReadWrite`。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QProcess::startDetached(qint64 *pid = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `startDetached`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`bool`。
- 参数 `pid`：类型为 `qint64 *`。默认值为 `nullptr`。传入 `qint64 *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] bool QProcess::startDetached(const QString &program, const QStringList &arguments = {}, const QString &workingDirectory = QString(), qint64 *pid = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `startDetached`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数 `program`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `arguments`：类型为 `const QStringList &`。默认值为 `{}`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `workingDirectory`：类型为 `const QString &`。默认值为 `QString()`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `pid`：类型为 `qint64 *`。默认值为 `nullptr`。传入 `qint64 *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[private signal] void QProcess::started()`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `started`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QProcess::ProcessState QProcess::state() const`

**API 类别：** 成员函数说明

**中文解读：** `QProcess::state` 用于计算、查询或取得与“state”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QProcess::ProcessState`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QProcess::ProcessState`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[private signal] void QProcess::stateChanged(QProcess::ProcessState newState)`

**API 类别：** 成员函数说明

**中文解读：** 这是状态变化通知 `stateChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `newState`：类型为 `QProcess::ProcessState`。没有默认值，调用时必须提供。传入 `QProcess::ProcessState` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QStringList QProcess::systemEnvironment()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `systemEnvironment`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QStringList`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QProcess::terminate()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `terminate`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept, since 6.6] QProcess::UnixProcessParameters QProcess::unixProcessParameters() const`

**API 类别：** 成员函数说明

**中文解读：** `QProcess::unixProcessParameters` 用于计算、查询或取得与“unix、处理、Parameters”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QProcess::UnixProcessParameters`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QProcess::UnixProcessParameters`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QProcess::waitForBytesWritten(int msecs = 30000)`

**API 类别：** 成员函数说明

**中文解读：** `QProcess::waitForBytesWritten` 用于计算、查询或取得与“等待、For、字节、Written”相关的操作。调用时要先确认当前状态和 `msecs` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `msecs`：类型为 `int`。默认值为 `30000`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QProcess::waitForFinished(int msecs = 30000)`

**API 类别：** 成员函数说明

**中文解读：** `QProcess::waitForFinished` 用于计算、查询或取得与“等待、For、Finished”相关的操作。调用时要先确认当前状态和 `msecs` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `msecs`：类型为 `int`。默认值为 `30000`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QProcess::waitForReadyRead(int msecs = 30000)`

**API 类别：** 成员函数说明

**中文解读：** `QProcess::waitForReadyRead` 用于计算、查询或取得与“等待、For、Ready、读取”相关的操作。调用时要先确认当前状态和 `msecs` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `msecs`：类型为 `int`。默认值为 `30000`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QProcess::waitForStarted(int msecs = 30000)`

**API 类别：** 成员函数说明

**中文解读：** `QProcess::waitForStarted` 用于计算、查询或取得与“等待、For、Started”相关的操作。调用时要先确认当前状态和 `msecs` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `msecs`：类型为 `int`。默认值为 `30000`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QProcess::workingDirectory() const`

**API 类别：** 成员函数说明

**中文解读：** `QProcess::workingDirectory` 用于计算、查询或取得与“working、Directory”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `struct CreateProcessArguments`

**API 类别：** 公有类型

**中文解读：** 这是 `QProcess` 的 `创建、处理、Arguments` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.6) struct UnixProcessParameters`

**API 类别：** 公有类型

**中文解读：** 这是 `QProcess` 的 `Unix、处理、Parameters` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `CreateProcessArgumentModifier`

**API 类别：** 公有类型

**中文解读：** 这是 `QProcess` 的 `创建、处理、Argument、Modifier` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.6) enum class UnixProcessFlag { CloseFileDescriptors, CreateNewSession, DisconnectControllingTerminal, IgnoreSigPipe, ResetIds, …, DisableCoreDumps }`

**API 类别：** 公有类型

**中文解读：** 这是 `QProcess` 暴露的类型声明 `class`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags UnixProcessFlags`

**API 类别：** 公有类型

**中文解读：** 这是 `QProcess` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

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
