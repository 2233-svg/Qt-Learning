# QIODevice

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QIODevice` 是 文件、设备与流机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QIODevice` 是 文件、设备与流机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 文件和 I/O 类型把路径/设备描述与打开后的读写状态分开。打开模式决定可执行的操作，当前位置、缓冲区、文本编码、权限和错误状态共同决定一次读写是否正确。

**适用场景：** 构造稳定路径，选择正确的 OpenMode，检查 open 和 errorString，按数据规模使用流式读写或分块处理，明确文本编码，完成后关闭并处理失败。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要手写平台分隔符；不要默认相对路径指向程序目录；不要把本地编码、UTF-8 和二进制混在一起；写文件时要考虑临时文件、覆盖、权限和原子替换。

## 2. 依赖与对象关系

- 头文件：`#include <QIODevice>`
- 继承自：QObject、QIODeviceBase
- 直接派生类：QAbstractSocket、QBluetoothSocket、QBuffer、QCoapReply、QFileDevice、QLocalSocket、QNetworkReply、QProcess,、QSerialPort

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

文件和 I/O 类型把路径/设备描述与打开后的读写状态分开。打开模式决定可执行的操作，当前位置、缓冲区、文本编码、权限和错误状态共同决定一次读写是否正确。

### 状态、生命周期和线程

**生命周期：** 先设置路径或设备，再 open，成功后读写/定位/刷新，最后 close；析构通常会关闭设备，但关键写入应显式 flush/close 并检查错误。相对路径依赖当前工作目录，资源路径和用户文件路径要区分。

**状态与结果：** 区分设备未打开、打开成功、到达 EOF、暂时无数据、读写失败和写入尚未落盘。`readAll()` 方便小数据但可能占用大量内存，大文件应分块处理并检查返回值。

**线程与事件循环：** 同一个打开设备不要跨线程并发使用，除非类明确保证线程安全；后台 I/O 通过 worker 或异步设备处理，GUI 线程只接收结果。

## 3. 直接使用

构造稳定路径，选择正确的 OpenMode，检查 open 和 errorString，按数据规模使用流式读写或分块处理，明确文本编码，完成后关闭并处理失败。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

```cpp
QFile file(path);
if (file.open(QIODevice::ReadOnly | QIODevice::Text)) {
    const QByteArray data = file.readAll();
}
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QIODevice()`
- `QIODevice(QObject *parent)`
- `virtual ~QIODevice()`
- `virtual bool atEnd() const`
- `virtual qint64 bytesAvailable() const`
- `virtual qint64 bytesToWrite() const`
- `virtual bool canReadLine() const`
- `virtual void close()`
- `void commitTransaction()`
- `int currentReadChannel() const`
- `int currentWriteChannel() const`
- `QString errorString() const`
- `bool getChar(char *c)`
- `bool isOpen() const`
- `bool isReadable() const`
- `virtual bool isSequential() const`
- `bool isTextModeEnabled() const`
- `bool isTransactionStarted() const`
- `bool isWritable() const`
- `virtual bool open(QIODeviceBase::OpenMode mode)`
- `QIODeviceBase::OpenMode openMode() const`
- `qint64 peek(char *data, qint64 maxSize)`
- `QByteArray peek(qint64 maxSize)`
- `virtual qint64 pos() const`
- `bool putChar(char c)`
- `qint64 read(char *data, qint64 maxSize)`
- `QByteArray read(qint64 maxSize)`
- `QByteArray readAll()`
- `int readChannelCount() const`
- `qint64 readLine(char *data, qint64 maxSize)`
- `QByteArray readLine(qint64 maxSize = 0)`
- `(since 6.9) QByteArrayView readLineInto(QSpan<char> buffer)`
- `(since 6.9) QByteArrayView readLineInto(QSpan<std::byte> buffer)`
- `(since 6.9) QByteArrayView readLineInto(QSpan<uchar> buffer)`
- `(since 6.9) bool readLineInto(QByteArray *line, qint64 maxSize = 0)`
- `virtual bool reset()`
- `void rollbackTransaction()`
- `virtual bool seek(qint64 pos)`
- `void setCurrentReadChannel(int channel)`
- `void setCurrentWriteChannel(int channel)`
- `void setTextModeEnabled(bool enabled)`
- `virtual qint64 size() const`
- `qint64 skip(qint64 maxSize)`
- `void startTransaction()`
- `void ungetChar(char c)`
- `virtual bool waitForBytesWritten(int msecs)`
- `virtual bool waitForReadyRead(int msecs)`
- `qint64 write(const char *data, qint64 maxSize)`
- `qint64 write(const QByteArray &data)`
- `qint64 write(const char *data)`
- `int writeChannelCount() const`

### 信号

- `void aboutToClose()`
- `void bytesWritten(qint64 bytes)`
- `void channelBytesWritten(int channel, qint64 bytes)`
- `void channelReadyRead(int channel)`
- `void readChannelFinished()`
- `void readyRead()`

### 保护函数

- `virtual qint64 readData(char *data, qint64 maxSize) = 0`
- `virtual qint64 readLineData(char *data, qint64 maxSize)`
- `void setErrorString(const QString &str)`
- `void setOpenMode(QIODeviceBase::OpenMode openMode)`
- `(since 6.0) virtual qint64 skipData(qint64 maxSize)`
- `virtual qint64 writeData(const char *data, qint64 maxSize) = 0`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 63 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `QIODevice::QIODevice()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QIODevice` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QIODevice::QIODevice(QObject *parent)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QIODevice` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `parent`：类型为 `QObject *`。没有默认值，调用时必须提供。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QIODevice::~QIODevice()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QIODevice` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QIODevice::aboutToClose()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QIODevice` 发出的通知信号 `aboutToClose`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] bool QIODevice::atEnd() const`

**API 类别：** 成员函数说明

**中文解读：** `QIODevice::atEnd` 用于计算、查询或取得与“按位置访问、结束”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] qint64 QIODevice::bytesAvailable() const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `bytesAvailable`，返回 `QIODevice` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`qint64`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] qint64 QIODevice::bytesToWrite() const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `bytesToWrite`，返回 `QIODevice` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`qint64`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QIODevice::bytesWritten(qint64 bytes)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QIODevice` 发出的通知信号 `bytesWritten`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `bytes`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] bool QIODevice::canReadLine() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `canReadLine`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QIODevice::channelBytesWritten(int channel, qint64 bytes)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QIODevice` 发出的通知信号 `channelBytesWritten`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `channel`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `bytes`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QIODevice::channelReadyRead(int channel)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QIODevice` 发出的通知信号 `channelReadyRead`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `channel`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] void QIODevice::close()`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `close`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QIODevice::commitTransaction()`

**API 类别：** 成员函数说明

**中文解读：** `QIODevice::commitTransaction` 用于执行与“提交、Transaction”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QIODevice::currentReadChannel() const`

**API 类别：** 成员函数说明

**中文解读：** `QIODevice::currentReadChannel` 用于计算、查询或取得与“当前、读取、Channel”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QIODevice::currentWriteChannel() const`

**API 类别：** 成员函数说明

**中文解读：** `QIODevice::currentWriteChannel` 用于计算、查询或取得与“当前、写入、Channel”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QIODevice::errorString() const`

**API 类别：** 成员函数说明

**中文解读：** `QIODevice::errorString` 用于计算、查询或取得与“错误、字符串”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QIODevice::getChar(char *c)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QIODevice` 的核心操作 `getChar`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`bool`。
- 参数 `c`：类型为 `char *`。没有默认值，调用时必须提供。传入 `char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QIODevice::isOpen() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isOpen`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QIODevice::isReadable() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isReadable`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] bool QIODevice::isSequential() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isSequential`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QIODevice::isTextModeEnabled() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isTextModeEnabled`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QIODevice::isTransactionStarted() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isTransactionStarted`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QIODevice::isWritable() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isWritable`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] bool QIODevice::open(QIODeviceBase::OpenMode mode)`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `open`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`bool`。
- 参数 `mode`：类型为 `QIODeviceBase::OpenMode`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 成功后才能 read/write/seek；失败时检查 `errorString()`，结束时 close 或让对象安全析构。

### `QIODeviceBase::OpenMode QIODevice::openMode() const`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `openMode`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QIODeviceBase::OpenMode`。
- 参数：无。

**正确调用组合：** 成功后才能 read/write/seek；失败时检查 `errorString()`，结束时 close 或让对象安全析构。

### `qint64 QIODevice::peek(char *data, qint64 maxSize)`

**API 类别：** 成员函数说明

**中文解读：** `QIODevice::peek` 用于计算、查询或取得与“peek”相关的操作。调用时要先确认当前状态和 `data`、`maxSize` 的有效范围；返回类型是 `qint64`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qint64`。
- 参数 `data`：类型为 `char *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `maxSize`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray QIODevice::peek(qint64 maxSize)`

**API 类别：** 成员函数说明

**中文解读：** `QIODevice::peek` 用于计算、查询或取得与“peek”相关的操作。调用时要先确认当前状态和 `maxSize` 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `maxSize`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] qint64 QIODevice::pos() const`

**API 类别：** 成员函数说明

**中文解读：** `QIODevice::pos` 用于计算、查询或取得与“pos”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qint64`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qint64`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QIODevice::putChar(char c)`

**API 类别：** 成员函数说明

**中文解读：** `QIODevice::putChar` 用于计算、查询或取得与“put、Char”相关的操作。调用时要先确认当前状态和 `c` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `c`：类型为 `char`。没有默认值，调用时必须提供。传入 `char` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qint64 QIODevice::read(char *data, qint64 maxSize)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QIODevice` 的核心操作 `read`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`qint64`。
- 参数 `data`：类型为 `char *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `maxSize`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 要区分 EOF、暂时无数据和错误；大文件优先分块读取。

### `QByteArray QIODevice::read(qint64 maxSize)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QIODevice` 的核心操作 `read`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `maxSize`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 要区分 EOF、暂时无数据和错误；大文件优先分块读取。

### `QByteArray QIODevice::readAll()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QIODevice` 的核心操作 `readAll`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数：无。

**正确调用组合：** 要区分 EOF、暂时无数据和错误；大文件优先分块读取。

### `int QIODevice::readChannelCount() const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QIODevice` 的核心操作 `readChannelCount`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 要区分 EOF、暂时无数据和错误；大文件优先分块读取。

### `[signal] void QIODevice::readChannelFinished()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QIODevice` 发出的通知信号 `readChannelFinished`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 要区分 EOF、暂时无数据和错误；大文件优先分块读取。

### `[pure virtual protected] qint64 QIODevice::readData(char *data, qint64 maxSize)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QIODevice` 的核心操作 `readData`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`qint64`。
- 参数 `data`：类型为 `char *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `maxSize`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 要区分 EOF、暂时无数据和错误；大文件优先分块读取。

### `qint64 QIODevice::readLine(char *data, qint64 maxSize)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QIODevice` 的核心操作 `readLine`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`qint64`。
- 参数 `data`：类型为 `char *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `maxSize`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 要区分 EOF、暂时无数据和错误；大文件优先分块读取。

### `QByteArray QIODevice::readLine(qint64 maxSize = 0)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QIODevice` 的核心操作 `readLine`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `maxSize`：类型为 `qint64`。默认值为 `0`。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 要区分 EOF、暂时无数据和错误；大文件优先分块读取。

### `[virtual protected] qint64 QIODevice::readLineData(char *data, qint64 maxSize)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QIODevice` 的核心操作 `readLineData`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`qint64`。
- 参数 `data`：类型为 `char *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `maxSize`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 要区分 EOF、暂时无数据和错误；大文件优先分块读取。

### `[since 6.9] QByteArrayView QIODevice::readLineInto(QSpan<std::byte> buffer)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QIODevice` 的核心操作 `readLineInto`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`QByteArrayView`。
- 参数 `buffer`：类型为 `QSpan<std::byte>`。没有默认值，调用时必须提供。传入 `QSpan<std::byte>` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 要区分 EOF、暂时无数据和错误；大文件优先分块读取。

### `[since 6.9] bool QIODevice::readLineInto(QByteArray *line, qint64 maxSize = 0)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QIODevice` 的核心操作 `readLineInto`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`bool`。
- 参数 `line`：类型为 `QByteArray *`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `maxSize`：类型为 `qint64`。默认值为 `0`。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 要区分 EOF、暂时无数据和错误；大文件优先分块读取。

### `[signal] void QIODevice::readyRead()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QIODevice` 发出的通知信号 `readyRead`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 要区分 EOF、暂时无数据和错误；大文件优先分块读取。

### `[virtual] bool QIODevice::reset()`

**API 类别：** 成员函数说明

**中文解读：** 这是状态清理或重置 API `reset`。调用后原有数据、索引、缓存或绑定可能失效；使用前先确认它影响的是当前对象、子对象还是底层共享资源，之后重新检查状态。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QIODevice::rollbackTransaction()`

**API 类别：** 成员函数说明

**中文解读：** `QIODevice::rollbackTransaction` 用于执行与“rollback、Transaction”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] bool QIODevice::seek(qint64 pos)`

**API 类别：** 成员函数说明

**中文解读：** `QIODevice::seek` 用于计算、查询或取得与“定位”相关的操作。调用时要先确认当前状态和 `pos` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `pos`：类型为 `qint64`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QIODevice::setCurrentReadChannel(int channel)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setCurrentReadChannel`。调用它会改变 `QIODevice` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `channel`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QIODevice::setCurrentWriteChannel(int channel)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setCurrentWriteChannel`。调用它会改变 `QIODevice` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `channel`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] void QIODevice::setErrorString(const QString &str)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setErrorString`。调用它会改变 `QIODevice` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `str`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] void QIODevice::setOpenMode(QIODeviceBase::OpenMode openMode)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setOpenMode`。调用它会改变 `QIODevice` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `openMode`：类型为 `QIODeviceBase::OpenMode`。没有默认值，调用时必须提供。传入 `QIODeviceBase::OpenMode` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QIODevice::setTextModeEnabled(bool enabled)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setTextModeEnabled`。调用它会改变 `QIODevice` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enabled`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] qint64 QIODevice::size() const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `size`，返回 `QIODevice` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`qint64`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qint64 QIODevice::skip(qint64 maxSize)`

**API 类别：** 成员函数说明

**中文解读：** `QIODevice::skip` 用于计算、查询或取得与“skip”相关的操作。调用时要先确认当前状态和 `maxSize` 的有效范围；返回类型是 `qint64`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qint64`。
- 参数 `maxSize`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected, since 6.0] qint64 QIODevice::skipData(qint64 maxSize)`

**API 类别：** 成员函数说明

**中文解读：** `QIODevice::skipData` 用于计算、查询或取得与“skip、数据访问”相关的操作。调用时要先确认当前状态和 `maxSize` 的有效范围；返回类型是 `qint64`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qint64`。
- 参数 `maxSize`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QIODevice::startTransaction()`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `startTransaction`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QIODevice::ungetChar(char c)`

**API 类别：** 成员函数说明

**中文解读：** `QIODevice::ungetChar` 用于执行与“unget、Char”相关的操作。调用时要先确认当前状态和 `c` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `c`：类型为 `char`。没有默认值，调用时必须提供。传入 `char` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] bool QIODevice::waitForBytesWritten(int msecs)`

**API 类别：** 成员函数说明

**中文解读：** `QIODevice::waitForBytesWritten` 用于计算、查询或取得与“等待、For、字节、Written”相关的操作。调用时要先确认当前状态和 `msecs` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `msecs`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] bool QIODevice::waitForReadyRead(int msecs)`

**API 类别：** 成员函数说明

**中文解读：** `QIODevice::waitForReadyRead` 用于计算、查询或取得与“等待、For、Ready、读取”相关的操作。调用时要先确认当前状态和 `msecs` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `msecs`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qint64 QIODevice::write(const char *data, qint64 maxSize)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QIODevice` 的核心操作 `write`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`qint64`。
- 参数 `data`：类型为 `const char *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `maxSize`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 要检查返回字节数和错误，关键数据考虑 flush、临时文件和原子替换。

### `qint64 QIODevice::write(const QByteArray &data)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QIODevice` 的核心操作 `write`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`qint64`。
- 参数 `data`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 要检查返回字节数和错误，关键数据考虑 flush、临时文件和原子替换。

### `qint64 QIODevice::write(const char *data)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QIODevice` 的核心操作 `write`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`qint64`。
- 参数 `data`：类型为 `const char *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 要检查返回字节数和错误，关键数据考虑 flush、临时文件和原子替换。

### `int QIODevice::writeChannelCount() const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QIODevice` 的核心操作 `writeChannelCount`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 要检查返回字节数和错误，关键数据考虑 flush、临时文件和原子替换。

### `[pure virtual protected] qint64 QIODevice::writeData(const char *data, qint64 maxSize)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QIODevice` 的核心操作 `writeData`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`qint64`。
- 参数 `data`：类型为 `const char *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `maxSize`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 要检查返回字节数和错误，关键数据考虑 flush、临时文件和原子替换。

### `(since 6.9) QByteArrayView readLineInto(QSpan<char> buffer)`

**API 类别：** 公有函数

**中文解读：** 这是 `QIODevice` 的核心操作 `readLineInto`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`QByteArrayView`。
- 参数 `buffer`：类型为 `QSpan<char>`。没有默认值，调用时必须提供。传入 `QSpan<char>` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 要区分 EOF、暂时无数据和错误；大文件优先分块读取。

### `(since 6.9) QByteArrayView readLineInto(QSpan<uchar> buffer)`

**API 类别：** 公有函数

**中文解读：** 这是 `QIODevice` 的核心操作 `readLineInto`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`QByteArrayView`。
- 参数 `buffer`：类型为 `QSpan<uchar>`。没有默认值，调用时必须提供。传入 `QSpan<uchar>` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 要区分 EOF、暂时无数据和错误；大文件优先分块读取。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先设置路径或设备，再 open，成功后读写/定位/刷新，最后 close；析构通常会关闭设备，但关键写入应显式 flush/close 并检查错误。相对路径依赖当前工作目录，资源路径和用户文件路径要区分。

### 状态和错误边界

区分设备未打开、打开成功、到达 EOF、暂时无数据、读写失败和写入尚未落盘。`readAll()` 方便小数据但可能占用大量内存，大文件应分块处理并检查返回值。

### 线程边界

同一个打开设备不要跨线程并发使用，除非类明确保证线程安全；后台 I/O 通过 worker 或异步设备处理，GUI 线程只接收结果。

### 最容易出现的错误

不要手写平台分隔符；不要默认相对路径指向程序目录；不要把本地编码、UTF-8 和二进制混在一起；写文件时要考虑临时文件、覆盖、权限和原子替换。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QIODevice` 所属机制类型：文件、设备与流机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
