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

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QIODevice::QIODevice()`

**作用与语义：**

构造一个QIODevice对象。

### `[explicit] QIODevice::QIODevice(QObject *parent)`

**作用与语义：**

构造一个具有给定`parent`的QIODevice对象。

### `[virtual noexcept] QIODevice::~QIODevice()`

**作用与语义：**

析构函数是虚函数，`QIODevice` 是抽象基类。此析构函数不调用 `close()`，但子类析构函数可能会调用。如果有疑问，请在销毁 `QIODevice` 前调用 `close()`。

### `[signal] void QIODevice::aboutToClose()`

**作用与语义：**

该信号在设备即将关闭时发出。如果您在设备关闭前需要执行操作（例如，有需要写入设备的其他缓冲区数据）时，请连接该信号。

### `[virtual] bool QIODevice::atEnd() const`

**作用与语义：**

如果当前读写位置位于设备末端（即设备无数据可用），返回`true`;否则返回`false`。
对于某些设备，atEnd() 即使有更多数据可读取，也可能返回 true。此特殊情况仅适用于直接响应你调用 `read()` 时生成数据的设备（例如，Unix 和 macOS 上的 `/dev` 或 `/proc` 文件，或所有平台的控制台输入/`stdin`）。

### `[virtual] qint64 QIODevice::bytesAvailable() const`

**作用与语义：**

返回可读取的字节数。该函数通常用于顺序设备，确定在读取前应分配多少字节。
重新实现该函数的子类必须调用基础实现，以包含`QIODevice`缓冲区的大小。示例：

**官方示例：**

```cpp
 qint64 CustomDevice::bytesAvailable() const
 {
     return buffer.size() + QIODevice::bytesAvailable();
 }
```

### `[virtual] qint64 QIODevice::bytesToWrite() const`

**作用与语义：**

对于有缓冲区的设备，该函数返回等待写入的字节数。对于没有缓冲区的设备，该函数返回0。
重新实现该函数的子类必须调用基础实现，以包含`QIODevice`缓冲区的大小。

### `[signal] void QIODevice::bytesWritten(qint64 bytes)`

**作用与语义：**

每当有效载荷数据写入设备当前写入通道时，都会发出该信号。`bytes`参数被设置为该有效载荷中写入的字节数。
bytesWritten() 不会递归地发射;如果你重新进入事件循环或调用连接到 bytesWritten() 信号的槽内的 `waitForBytesWritten()`，该信号不会被重新发射（尽管 `waitForBytesWritten()` 可能仍返回真）。

### `[virtual] bool QIODevice::canReadLine() const`

**作用与语义：**

如果能从设备读取完整数据行，返回`true`;否则返回`false`。
注意，未缓冲设备无法确定可读取内容，总是返回false。
该功能通常与`readyRead()`信号结合使用。
重现该函数的子类必须调用基础实现，以包含`QIODevice`缓冲区的内容。示例：

**官方示例：**

```cpp
 bool CustomDevice::canReadLine() const
 {
     return buffer.contains('\n') || QIODevice::canReadLine();
 }
```

### `[signal] void QIODevice::channelBytesWritten(int channel, qint64 bytes)`

**作用与语义：**

每当数据载入到设备时，都会发出该信号。`bytes`参数设为该载荷中写入的字节数，`channel` 表示该参数写入的通道。与`bytesWritten()`不同，该参数无论当前写入通道如何都会发出。
channelBytesWritten() 可以递归地发射——即使是同一通道。

### `[signal] void QIODevice::channelReadyRead(int channel)`

**作用与语义：**

当设备有新数据可供读取时，该信号会发出。`channel`参数被设置为数据到达的读取通道的索引。与`readyRead()`不同，该参数无论当前读通道如何都会发出。
channelReadyRead() 可以递归地发射——即使是针对同一通道。

### `[virtual] void QIODevice::close()`

**作用与语义：**

首先发出`aboutToClose()`，然后关闭设备并将其 OpenMode 设置为 NotOpen。错误字符串也会被重置。

### `void QIODevice::commitTransaction()`

**作用与语义：**

完成一次读取事务。
对于顺序设备，交易期间记录在内部缓冲区的所有数据都会被丢弃。

### `int QIODevice::currentReadChannel() const`

**作用与语义：**

返回当前读通道的索引。

### `int QIODevice::currentWriteChannel() const`

**作用与语义：**

返回当前写信道的索引。

### `QString QIODevice::errorString() const`

**作用与语义：**

返回对最后一次设备错误的人类可读描述。

### `bool QIODevice::getChar(char *c)`

**作用与语义：**

从设备读取一个字符并存储在`c`中。如果`c` `nullptr`，该字符被丢弃。成功时返回`true`;否则返回`false`。

### `bool QIODevice::isOpen() const`

**作用与语义：**

如果设备打开，返回`true`;否则返回`false`。如果设备可以被读取和/或写入，则该功能是打开的。默认情况下，如果`openMode()`返回`NotOpen`，该函数返回`false`。

### `bool QIODevice::isReadable() const`

**作用与语义：**

返回`true`是否能从设备读取数据;否则返回假。使用`bytesAvailable()`确定可读取多少字节。
这是一个方便功能，用于检查设备的OpenMode是否包含只读标志。

### `[virtual] bool QIODevice::isSequential() const`

**作用与语义：**

如果该设备是顺序的，返回`true`;否则返回false。
顺序设备与随机访问设备不同，没有起始、结束、大小或当前位置的概念，也不支持寻道。只有当设备报告数据可用时，你才能读取数据。最常见的顺序设备例子是网络套接字。在Unix上，特殊文件如/dev/zero和fifo管道是顺序文件。
而普通文件则支持随机访问。它们既有大小也有当前位置，还支持在数据流中向后和向前寻求。普通文件则是非顺序的。

### `bool QIODevice::isTextModeEnabled() const`

**作用与语义：**

如果启用了 `Text` 标志，则返回 `true`；否则返回 `false`。

### `bool QIODevice::isTransactionStarted() const`

**作用与语义：**

如果设备上正在进行交易，退货`true`，否则则`false`。

### `bool QIODevice::isWritable() const`

**作用与语义：**

如果可以写入设备，返回`true`;否则返回假。
这是一个方便功能，用于检查设备的OpenMode是否包含WriteOnly标志。

### `[virtual] bool QIODevice::open(QIODeviceBase::OpenMode mode)`

**作用与语义：**

打开设备并将其 OpenMode 设置为 `mode`。成功时返回 `true`;否则返回 `false`。该函数应从任何重新实现的 open() 或其他打开设备的函数中调用。

### `QIODeviceBase::OpenMode QIODevice::openMode() const`

**作用与语义：**

返回设备被打开的模式;即只读或仅写。

### `qint64 QIODevice::peek(char *data, qint64 maxSize)`

**作用与语义：**

最多从设备读取`maxSize`字节到`data`，且无副作用（即在peek（后调用`read()`），会得到相同的数据。返回读取的字节数。如果发生错误，例如尝试读取以WriteOnly模式打开的设备时，该函数返回-1。
当没有更多可读取的数据时，返回0。

**官方示例：**

```cpp
 bool isExeFile(QFile *file)
 {
     char buf[2];
     if (file->peek(buf, sizeof(buf)) == sizeof(buf))
         return (buf[0] == 'M' && buf[1] == 'Z');
     return false;
 }
```

### `QByteArray QIODevice::peek(qint64 maxSize)`

**作用与语义：**

从设备中最多查看`maxSize`字节，返回以 `QByteArray` 读取的数据。
该函数无法报告错误;返回空`QByteArray`可能意味着当前没有可供读取的数据，或者发生了错误。

**官方示例：**

```cpp
 bool isExeFile(QFile *file)
 {
     return file->peek(2) == "MZ";
 }
```

### `[virtual] qint64 QIODevice::pos() const`

**作用与语义：**

对于随机访问设备，该函数返回数据写入或读取的位置。对于顺序设备或封闭设备，若不存在“当前位置”概念，则返回0。
设备的当前读写位置由`QIODevice`内部保持，因此无需重新实现此功能。在子类化`QIODevice`时，使用`QIODevice::seek()`通知`QIODevice`设备位置的变化。

### `bool QIODevice::putChar(char c)`

**作用与语义：**

将字符 `c` 写入设备。成功时返回 `true`；否则返回 `false`。

### `qint64 QIODevice::read(char *data, qint64 maxSize)`

**作用与语义：**

最多从设备读取`maxSize`字节到`data`，返回读取的字节数。如果发生错误，例如尝试从以WriteOnly模式打开的设备读取时，该函数返回-1。
当没有更多可读取的数据时返回0。然而，读取超过流末端的部分被视为错误，因此该函数在这些情况下返回-1（即在闭合套接字上读取或进程死亡后）。

### `QByteArray QIODevice::read(qint64 maxSize)`

**作用与语义：**

最多从设备读取`maxSize`字节，并返回读取的数据作为`QByteArray`。
该函数无法报告错误;返回空`QByteArray`可能意味着当前没有数据可供读取，或者发生了错误。

### `QByteArray QIODevice::readAll()`

**作用与语义：**

读取设备中剩余的所有数据，并以字节数组的形式返回。
该函数无法报告错误;返回空`QByteArray`可能意味着当前没有可用数据可读取，或者发生了错误。该函数也无法表示可能有更多数据可用且无法读取。

### `int QIODevice::readChannelCount() const`

**作用与语义：**

如果设备打开，返回可用读通道数量;否则返回0。

### `[signal] void QIODevice::readChannelFinished()`

**作用与语义：**

当输入（读取）流在该设备中闭合时，该信号会发出。一旦检测到闭合，信号就会立即发出，这意味着可能仍有数据可用`read()`读取。

### `[pure virtual protected] qint64 QIODevice::readData(char *data, qint64 maxSize)`

**作用与语义：**

从设备读取最多`maxSize`字节到`data`，并返回读取的字节数，如果发生错误则返回-1字节。
如果没有字节可读且永远无法再有更多字节（例如套接字闭合、管道闭合、子进程已完成），该函数返回 -1。
该函数由`QIODevice`调用。创建`QIODevice`子类时重新实现该函数。
在重新实现该函数时，重要的是该函数必须在返回前读取所有所需数据。这是`QDataStream`能够对类进行操作的必要条件。`QDataStream`假设所有请求的信息都已读取，因此如果存在问题，不会重试读取。
该函数可调用 maxSize 为 0，可用于执行读取后操作。

### `qint64 QIODevice::readLine(char *data, qint64 maxSize)`

**作用与语义：**

该函数从设备读取一行ASCII字符，最多`maxSize` - 1字节，将字符存储为`data`，返回已读取的字节数。如果无法读取某行但未发生错误，该函数返回0。如果发生错误，该函数返回可读取长度，若未读取则返回-1。
`data`后总会附加一个终止的“\0”字节，因此`maxSize`必须大于1。
数据读取直到满足以下任一条件：
- 读出第一个“\n”字符。
- `maxSize` - 读取1字节。
- 检测到设备数据的末端。
例如，以下代码读取文件中的一行字符：
缓冲区中包含换行字符（“\n”）。如果在 maxSize - 1 字节读取前未遇到换行，则不会插入该换行。
注意：换行转换（例如将 \r 转换为 \n）仅在设备被打开读取时使用 QIODevice：：Text 标志进行。
注意，在顺序设备上，数据可能无法立即获取，可能导致返回部分行。通过在读取前调用`canReadLine()`函数，您可以检查是否能读取完整的行（包括换行字符）。
该函数调用`readLineData()`，通过反复调用`getChar()`实现。通过在自己的子类中重新实现`readLineData()`，可以实现更高效的实现。

**官方示例：**

```cpp
 QFile file("box.txt");
 if (file.open(QFile::ReadOnly)) {
     char buf[1024];
     qint64 lineLength = file.readLine(buf, sizeof(buf));
     if (lineLength != -1) {
         // the line is available in buf
     }
 }
```

### `QByteArray QIODevice::readLine(qint64 maxSize = 0)`

**作用与语义：**

读取设备中的一行，但不超过`maxSize`字符，并将结果返回为字节数组。
如果`maxSize`为0或未指定，行长度可以任意，从而实现无限读取。
最终的行尾可能带有尾随字符（“\n”或“\r\n”），因此可能需要调用`QByteArray::trimmed()`。
该函数无法报告错误;返回空`QByteArray`可能意味着当前没有可供读取的数据，或者发生了错误。

### `[virtual protected] qint64 QIODevice::readLineData(char *data, qint64 maxSize)`

**作用与语义：**

读取最多`maxSize`个字符`data`并返回已读字符数。
该函数由`readLine()`调用，并通过`getChar()`提供其基础实现。缓冲设备通过重新实现该函数可以提升`readLine()`的性能。
`readLine()` 会在 `data` 后附加一个 '\0' 字节;readLineData() 则不需要这样做。
如果重新实现该函数，请注意返回正确的值：应返回该行读取的字节数，包括终止的换行，或者如果此时没有可读的行，则返回0。如果发生错误，应返回-1，当且仅当没有读取字节。超过EOF的读取被视为错误。

### `[since 6.9] QByteArrayView QIODevice::readLineInto(QSpan<std::byte> buffer)`

**作用与语义：**

从该设备读取一行到`buffer`，返回包含读取数据的子集`buffer`。
如果`buffer`的大小小于行长，只有符合`buffer`的字符才会被读取并返回。此时，再次调用`readLineInto()`将检索到该行的剩余部分。为了确定整行是否被读取，首先检查设备是否被`atEnd()`，以防最后一行没有换行。如果没有`atEnd()`，则验证返回的视图是否以“\n”结尾。否则，需要再次调用`readLineInto()`。
结果行尾可能有行尾字符（“\n”或“\r\n”），因此可能需要调用`QByteArrayView::trimmed()`。
如果发生错误，该函数返回空`QByteArrayView`。否则是`buffer`的子张成。如果当前没有可用数据或设备`atEnd()`，该函数返回空`QByteArrayView`。
注意返回值并非空终止。如果你想要空终止，可以通过`buffer.chopped(1)`，然后在`buffer[result.size()]`处插入“\0”。

### `[since 6.9] bool QIODevice::readLineInto(QByteArray *line, qint64 maxSize = 0)`

**作用与语义：**

从该设备读取一行到`buffer`，返回包含读取数据的子集`buffer`。
如果`buffer`的大小小于行长，只有符合`buffer`的字符才会被读取并返回。此时，再次调用`readLineInto()`将检索到该行的剩余部分。为了确定整行是否被读取，首先检查设备是否被`atEnd()`，以防最后一行没有换行。如果没有`atEnd()`，则验证返回的视图是否以“\n”结尾。否则，需要再次调用`readLineInto()`。
结果行尾可能有行尾字符（“\n”或“\r\n”），因此可能需要调用`QByteArrayView::trimmed()`。
如果发生错误，该函数返回空`QByteArrayView`。否则是`buffer`的子张成。如果当前没有可用数据或设备`atEnd()`，该函数返回空`QByteArrayView`。
注意返回值并非空终止。如果你想要空终止，可以通过`buffer.chopped(1)`，然后在`buffer[result.size()]`处插入“\0”。

### `[signal] void QIODevice::readyRead()`

**作用与语义：**

每当设备当前读信道有新数据可用时，该信号会发出一次。只有当有新数据可用时，比如网络接口上有新的网络数据负载到达，或设备新增数据块，才会再次发出。
readyRead() 不会递归地发射;如果你重新进入事件环路或调用连接到 readyRead() 信号的槽内的 `waitForReadyRead()`，该信号不会被重新发射（尽管 `waitForReadyRead()` 仍可能返回 true）。
给实现基于`QIODevice`类的开发者注意：当新数据到达时，你应始终发出 readyRead()（不要仅因为缓冲区里还有数据未读就发出）。在其他情况下不要发出 readyRead()。

### `[virtual] bool QIODevice::reset()`

**作用与语义：**

寻求随机访问设备的输入起始点。成功时返回真;否则返回`false`（例如设备未打开时）。
注意，在`QFile`上使用`QTextStream`时，调用`QFile`上的reset()不会得到预期结果，因为`QTextStream`会缓冲文件。改用`QTextStream::seek()`函数。

### `void QIODevice::rollbackTransaction()`

**作用与语义：**

回滚已读交易。
将输入流恢复到`startTransaction()`调用点。该函数通常用于在提交事务前检测到未完成读取时回滚事务。

### `[virtual] bool QIODevice::seek(qint64 pos)`

**作用与语义：**

对于随机访问设备，该函数将当前位置设置为`pos`，成功时返回true，发生错误时返回false。对于顺序设备，默认行为是发送警告并返回false。
在子类 `QIODevice` 时，你必须在函数开头调用 QIODevice：：seek()，以确保与 `QIODevice` 内置缓冲区的完整性。

### `void QIODevice::setCurrentReadChannel(int channel)`

**作用与语义：**

将`QIODevice`当前的读信道设置为给定的`channel`。当前输入信道被功能 `read()`、`readAll()`、`readLine()` 和 `getChar()` 使用。它还决定触发哪个信道`QIODevice`发射`readyRead()`。

### `void QIODevice::setCurrentWriteChannel(int channel)`

**作用与语义：**

将`QIODevice`当前写通道设置为给定`channel`。电流输出通道被函数`write()` `putChar()`使用。它还决定哪个通道触发`QIODevice`发射`bytesWritten()`。

### `[protected] void QIODevice::setErrorString(const QString &str)`

**作用与语义：**

将最后一次设备错误的人类可读描述设置为`str`。

### `[protected] void QIODevice::setOpenMode(QIODeviceBase::OpenMode openMode)`

**作用与语义：**

将设备的OpenMode设置为`openMode`。如果设备打开后标志发生变化，调用该函数设置开启模式。

### `void QIODevice::setTextModeEnabled(bool enabled)`

**作用与语义：**

如果`enabled`为真，该函数会在设备上设置`Text`标志;否则`Text`标志将被移除。此功能对于在`QIODevice`上提供自定义终端处理的类非常有用。
在调用该函数之前，应先打开IO设备。

### `[virtual] qint64 QIODevice::size() const`

**作用与语义：**

对于开放随机访问设备，该函数返回设备的大小。对于开放顺序设备，返回`bytesAvailable()`。
如果设备关闭，返回的尺寸不会反映设备的实际大小。

### `qint64 QIODevice::skip(qint64 maxSize)`

**作用与语义：**

从设备中跳过最多`maxSize`字节。返回实际跳过的字节数，错误时返回-1字节数。
该函数不等待，只丢弃已可读取的数据。
如果设备以文本模式打开，线尾终止符会被转换为“\n”符号，并作为一个字节计数，与`read()`和`peek()`行为相同。
该功能适用于所有设备，包括无法`seek()`的顺序设备。它经过优化，在`peek()`调用后跳过不需要的数据。
对于随机存取设备，可以使用skip()从当前位置向前寻。不允许负`maxSize`值。

### `[virtual protected, since 6.0] qint64 QIODevice::skipData(qint64 maxSize)`

**作用与语义：**

从设备中跳过最多`maxSize`字节。返回实际跳过的字节数，错误时返回-1字节数。
该函数由`QIODevice`调用。创建`QIODevice`子类时考虑重新实现它。
基础实现通过读取到虚拟缓冲区来丢弃数据。这虽然慢，但适用于所有类型的设备。子类可以重新实现这个函数来改进。

### `void QIODevice::startTransaction()`

**作用与语义：**

在设备上启动新的读取事务。
定义了读取操作序列中的一个可恢复点。对于顺序设备，读取数据会在内部复制，以便在读取不完整时恢复。对于随机访问设备，该功能保存当前位置。调用`commitTransaction()`或`rollbackTransaction()`以完成交易。
注意：不支持嵌套交易。

### `void QIODevice::ungetChar(char c)`

**作用与语义：**

将字符`c`重新放入设备，并递减当前位置，除非位置为0。该函数通常用于“撤销”`getChar()`操作，例如编写回溯解析器时。
如果`c`之前没有从设备读取，行为是未定义的。
注意：该功能在交易进行时不可用。

### `[virtual] bool QIODevice::waitForBytesWritten(int msecs)`

**作用与语义：**

对于缓冲设备，该功能等待到设备写入缓冲的写入数据负载并发出`bytesWritten()`信号后，或经过`msecs`毫秒后才启用。如果msecs为-1，该函数不会超时。对于未缓冲设备，该功能会立即返回。
如果数据载荷写入设备，返回`true`;否则返回`false`（即操作超时或发生错误）。
该函数可以在没有事件循环的情况下运行。它在编写非 GUI 应用以及在非 GUI 线程中执行 I/O 操作时非常有用。
如果从连接到`bytesWritten()`信号的槽函数内调用，则不会重新发射`bytesWritten()`。
重新实现这个函数，为自定义设备提供阻断 API。默认实现不做任何事，返回`false`。
警告：从主线（GUI）线程调用该函数可能会导致用户界面卡死。

### `[virtual] bool QIODevice::waitForReadyRead(int msecs)`

**作用与语义：**

直到有新数据可供读取且`readyRead()`信号已发出，或`msecs`毫秒后才会阻塞。如果毫秒为-1，该函数不会超时。
如果有新数据可供读取，返回`true`;否则返回 false（如果操作超时或发生错误）。
该函数可以在没有事件循环的情况下运行。它在编写非 GUI 应用以及在非 GUI 线程中执行 I/O 操作时非常有用。
如果从连接到`readyRead()`信号的槽函数内调用，则`readyRead()`不会被重新发射。
重新实现这个函数，为自定义设备提供阻断API。默认实现不做任何操作，返回`false`。
警告：从主线（GUI）线程调用该函数可能会导致用户界面卡死。

### `qint64 QIODevice::write(const char *data, qint64 maxSize)`

**作用与语义：**

最多从`data`写入`maxSize`字节的数据到设备。返回实际写入的字节数，或如果发生错误则返回-1字节。

### `qint64 QIODevice::write(const QByteArray &data)`

**作用与语义：**

将 `data` 的内容写入设备。返回实际写入的字节数，如果发生错误则返回 -1。

### `qint64 QIODevice::write(const char *data)`

**作用与语义：**

将零终端字符串的8位字符写入数据到设备。返回实际写入的字节数，或如果发生错误则返回-1字节数。这等价于。

**官方示例：**

```cpp
 ...
 QIODevice::write(data, qstrlen(data));
 ...
```

### `int QIODevice::writeChannelCount() const`

**作用与语义：**

如果设备打开，返回可用写信道数量;否则返回0。

### `[pure virtual protected] qint64 QIODevice::writeData(const char *data, qint64 maxSize)`

**作用与语义：**

从`data`写入最多`maxSize`字节到设备。返回写入字节数，或如果发生错误则返回-1字节。
该函数由`QIODevice`调用。创建`QIODevice`子类时重新实现该函数。
在重新实现该函数时，重要的是该函数在返回前写入所有可用数据。这是 `QDataStream` 能够操作该类的必要条件。`QDataStream` 假设所有信息都已写入，因此如果出现问题不会重试写入。

### `(since 6.9) QByteArrayView readLineInto(QSpan<char> buffer)`

**作用与语义：**

从该设备读取一行到`buffer`，返回包含读取数据的子集`buffer`。
如果`buffer`的大小小于行长，只有符合`buffer`的字符才会被读取并返回。此时，再次调用`readLineInto()`将检索到该行的剩余部分。为了确定整行是否被读取，首先检查设备是否被`atEnd()`，以防最后一行没有换行。如果没有`atEnd()`，则验证返回的视图是否以“\n”结尾。否则，需要再次调用`readLineInto()`。
结果行尾可能有行尾字符（“\n”或“\r\n”），因此可能需要调用`QByteArrayView::trimmed()`。
如果发生错误，该函数返回空`QByteArrayView`。否则是`buffer`的子张成。如果当前没有可用数据或设备`atEnd()`，该函数返回空`QByteArrayView`。
注意返回值并非空终止。如果你想要空终止，可以通过`buffer.chopped(1)`，然后在`buffer[result.size()]`处插入“\0”。

### `(since 6.9) QByteArrayView readLineInto(QSpan<uchar> buffer)`

**作用与语义：**

读取设备中的一行，但不超过`maxSize`字符。并以字节数组形式存储在`line`中。
注意：即使`line` `nullptr`，也能读取该设备的线路。
如果`maxSize`为0或未指定，行长度可以任意，从而实现无限读取。
最终的行尾可能有尾随字符（“\n”或“\r\n”），因此可能需要调用`QByteArray::trimmed()`。
如果当前没有可读取的数据，或发生错误，该函数返回`false`并将`line`设置为`empty`。否则返回`true`。
注意，调用前`line`的内容无论如何都会被丢弃，但其`capacity()`永远不会减少。

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
