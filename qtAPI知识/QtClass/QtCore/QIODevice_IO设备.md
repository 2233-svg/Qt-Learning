# Qt QIODevice 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QIODevice>`  
> 所属模块：`Qt6::Core`  
> 继承：`QObject`、`QIODeviceBase -> QIODevice`  
> 定位：为文件、缓冲区、进程、socket 和自定义设备统一读写接口的抽象基类

## 1. QIODevice 解决什么问题

`QIODevice` 把不同来源的数据统一成“打开、读取、写入、定位、等待和关闭”的接口。上层代码可以不关心数据来自磁盘、内存、子进程还是网络：

```text
QIODevice
├─ QFileDevice
│  └─ QFile / QSaveFile / QTemporaryFile
├─ QBuffer
├─ QProcess
├─ QAbstractSocket
│  └─ QTcpSocket / QUdpSocket ...
└─ 自定义设备
```

它本身是抽象基类，不能直接提供完整的数据源。派生类需要实现至少：

```cpp
qint64 readData(char *data, qint64 maxSize) override;
qint64 writeData(const char *data, qint64 maxSize) override;
```

选择 `QIODevice` 时，先回答三个问题：

1. 设备是否需要随机定位？文件和内存缓冲区通常可以，TCP socket 通常不可以。
2. 数据是同步读取还是事件驱动？网络和进程通常通过 `readyRead()`，本地文件可以直接读。
3. 失败是“暂时没有数据”还是“设备出错”？`read()` 返回空数据不一定代表 EOF，必须结合 `atEnd()`、信号和错误状态判断。

## 2. 打开模式决定允许做什么

```cpp
QFile file("config.ini");
if (!file.open(QIODevice::ReadOnly | QIODevice::Text)) {
    qWarning() << file.errorString();
    return;
}
```

常用模式：

| 模式 | 含义 | 使用时重点 | 典型使用场景 |
| --- | --- | --- | --- |
| `ReadOnly` | 只读打开 | 不能调用写操作；适合读取配置和资源 | 加载文件、读取协议输入 |
| `WriteOnly` | 只写打开 | 可能截断已有内容，具体行为由派生类决定 | 创建输出文件或导出结果 |
| `ReadWrite` | 同时读写 | 要明确读写位置和是否需要 seek | 随机访问数据库文件或内存设备 |
| `Append` | 写入追加到末尾 | 适合日志；不能把当前写位置理解为普通覆盖位置 | 追加日志和审计记录 |
| `Truncate` | 打开时截断已有内容 | 谨慎使用；写文件更新通常优先 QSaveFile | 明确要完全重写的临时输出 |
| `Text` | 启用文本模式转换 | 主要影响换行处理；二进制协议不要使用 | 文本文件和平台换行兼容 |
| `Unbuffered` | 请求不使用设备缓冲 | 平台和派生类可能有差异，不等同于每次写入都持久化到磁盘 | 底层设备集成和诊断场景 |

`open()` 成功只说明设备进入可用状态，不代表后续每次读写都一定成功。每个关键操作都要检查返回值或状态。

## 3. 顺序设备和随机访问设备

### 3.1 随机访问设备

```cpp
QFile file("data.bin");
file.open(QIODevice::ReadOnly);
file.seek(128);
const QByteArray block = file.read(32);
```

随机访问设备通常支持 `pos()`、`size()`、`seek()` 和 `reset()`。调用 `seek()` 失败时，设备可能保持原位置，不能假设已经移动。

### 3.2 顺序设备

socket、管道和很多进程设备是顺序设备：

```cpp
QTcpSocket socket;
if (socket.isSequential())
    qInfo() << "cannot seek";
```

顺序设备没有可靠的总大小和任意位置概念。读取数据应通过 `readyRead()`、协议帧边界和内部缓冲完成，不能用 `size()` 预判完整消息。

## 4. 同步读写与异步读写

### 4.1 本地文件的同步读取

```cpp
QFile file("input.txt");
if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    return;

while (!file.atEnd()) {
    const QByteArray line = file.readLine();
    if (line.isEmpty() && !file.atEnd())
        qWarning() << file.errorString();
    processLine(line);
}
```

### 4.2 事件驱动设备

```cpp
connect(socket, &QIODevice::readyRead,
        this, &Receiver::readAvailableBytes);

void Receiver::readAvailableBytes()
{
    m_buffer += socket->readAll();
    while (hasCompleteFrame(m_buffer))
        consumeFrame(takeFrame(m_buffer));
}
```

`readyRead()` 表示当前有数据可读，不表示一条完整业务消息已经到达。TCP 没有消息边界，应用协议必须自己定义长度、分隔符或固定头部。

### 4.3 `waitFor...()` 不是 GUI 代码的默认方案

```cpp
if (!socket.waitForReadyRead(3'000)) {
    qWarning() << socket.errorString();
}
```

`waitForReadyRead()` 和 `waitForBytesWritten()` 会阻塞调用线程。它们适合后台线程中的同步封装、命令行程序或测试，不适合 GUI 线程，否则窗口和其他事件会停止响应。

## 5. 读写返回值和错误状态

读写接口常见返回语义：

- `read()` 返回实际读取字节数；`-1` 通常表示错误。
- `write()` 返回接受的字节数；并不一定表示数据已经物理写入磁盘或网络对端。
- `readAll()` 返回当前可获得的数据；空数组可能表示暂时没有数据、EOF 或错误。
- `bytesAvailable()` 表示当前可立即读取的数据量，不是远端未来会发送的总量。
- `bytesToWrite()` 表示设备内部尚未写出的缓冲数据量。
- `errorString()` 提供面向诊断的错误描述，不应作为稳定的错误枚举。

对网络和进程设备，优先连接错误信号和状态信号；不要用高频定时器轮询 `bytesAvailable()`。

## 6. 事务：处理协议读取的半包

`QIODevice` 的事务主要用于读取过程中的试探性解析：

```cpp
device->startTransaction();

quint32 length = 0;
QDataStream stream(device);
stream >> length;

if (device->bytesAvailable() < length) {
    device->rollbackTransaction();
    return; // 等待更多数据
}

QByteArray payload;
stream >> payload;
if (stream.status() == QDataStream::Ok)
    device->commitTransaction();
else
    device->rollbackTransaction();
```

事务不是数据库事务，不会回滚设备已经写出的数据，也不会撤销外部副作用。它主要让可回滚的读取位置和数据缓冲恢复到开始时状态。

不同派生类对事务的具体支持可能不同。使用前确认设备是可回滚的读设备，并检查底层流的状态。

## 7. 自定义 QIODevice 的实现边界

实现自定义设备时，至少要明确：

- `readData()` 在无数据、EOF 和错误时分别返回什么。
- `writeData()` 是否允许部分写入。
- `isSequential()` 是否返回 true。
- `open()` 和 `close()` 如何更新 `openMode`。
- 是否需要发出 `readyRead()`、`bytesWritten()` 和 `readChannelFinished()`。
- 多线程访问由谁负责串行化。

一个最小内存设备的骨架：

```cpp
class MemoryDevice final : public QIODevice
{
public:
    explicit MemoryDevice(QByteArray data = {}, QObject *parent = nullptr)
        : QIODevice(parent), m_data(std::move(data))
    {
    }

    bool open(OpenMode mode) override
    {
        if (!QIODevice::open(mode))
            return false;
        m_pos = 0;
        return true;
    }

protected:
    qint64 readData(char *data, qint64 maxSize) override
    {
        const qint64 available = m_data.size() - m_pos;
        const qint64 count = qMin(maxSize, available);
        if (count <= 0)
            return 0;
        memcpy(data, m_data.constData() + m_pos, size_t(count));
        m_pos += count;
        return count;
    }

    qint64 writeData(const char *data, qint64 maxSize) override
    {
        m_data.append(data, maxSize);
        m_pos = m_data.size();
        return maxSize;
    }

private:
    QByteArray m_data;
    qint64 m_pos = 0;
};
```

真实实现还要覆盖 `size()`、`pos()`、`seek()`、只读/只写模式和并发约束。不要只让 `readData()` 能返回数据，就认为设备契约完成了。

## 8. 常见误区

### 把 `readyRead()` 当成完整消息

一次信号可能只带来半包，也可能带来多包。保留接收缓冲，按协议拆包。

### 用 `atEnd()` 判断 socket 是否暂时没有数据

顺序设备的 `atEnd()` 不能替代协议状态。socket 还活着但当前没有数据时，应该等待下一次 `readyRead()`。

### 在 GUI 线程使用 `waitForReadyRead()`

这会阻塞事件循环。改用信号槽，或把同步读取放到有明确生命周期的 Worker 线程。

### 把 `write()` 返回成功当成持久化成功

对于文件，数据可能还在缓存；对于网络，数据可能只进入本地发送队列。需要持久化或协议确认时，使用设备和业务层各自的完成信号。

### 读文本时混用二进制模式

`Text` 会影响换行处理；二进制协议、压缩数据和序列化文件应保持二进制模式。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QIODevice()` / `QIODevice(QObject *)` | 创建设备基类部分，初始化未打开状态。 | QIODevice 是抽象类，实际使用应选择派生类或实现纯虚读写函数。 |
| 析构 | `~QIODevice()` | 销毁设备对象并释放其内部状态。 | parent 和线程归属仍按 QObject 规则处理；设备是否自动关闭由派生类语义确认。 |
| 状态 | `openMode()` | 返回当前打开模式。 | 未打开时为空；不要只看模式不检查 `isOpen()`。 |
| 状态 | `isOpen()` | 判断设备是否已打开。 | 打开不代表读写一定成功，仍要检查具体操作返回值。 |
| 状态 | `isReadable()` | 判断当前模式是否允许读取。 | 只是模式检查，不表示当前确实有数据可读。 |
| 状态 | `isWritable()` | 判断当前模式是否允许写入。 | 只是模式检查，不表示底层空间或对端可用。 |
| 类型 | `isSequential()` | 判断设备是否是顺序设备。 | 顺序设备通常不能 seek、size 或按位置重读。 |
| 模式 | `open(OpenMode)` | 打开设备并设置读写模式。 | 派生类负责实际资源；失败后读取 `errorString()`。 |
| 模式 | `close()` | 关闭设备并结束当前 I/O 会话。 | 关闭可能触发 `aboutToClose()`；未写完数据的设备要按派生类文档处理。 |
| 文本 | `setTextModeEnabled(bool)` | 开启或关闭文本模式。 | 只对支持文本转换的设备有意义；二进制协议不要开启。 |
| 文本 | `isTextModeEnabled()` | 查询是否启用文本模式。 | 它不等同于文件编码选择，UTF-8 等编码要由上层处理。 |
| 位置 | `pos()` | 返回当前读写位置。 | 顺序设备可能没有有意义的位置；失败值要结合设备文档判断。 |
| 位置 | `size()` | 返回设备可报告的大小。 | socket、管道等顺序设备通常不能用它判断完整数据。 |
| 位置 | `seek(qint64)` | 把当前位置移动到指定位置。 | 只对支持随机访问的设备可靠；失败后不要继续假设位置已改变。 |
| 位置 | `reset()` | 将设备位置重置到起始位置。 | 等价语义由派生类提供；顺序设备通常不支持。 |
| 结束 | `atEnd()` | 判断设备是否到达可读数据末尾。 | 对网络设备不等于“当前暂时没有数据”；要配合 readyRead 和连接状态。 |
| 读取 | `read(char *, qint64)` | 读取最多指定字节到调用者缓冲区。 | 返回实际字节数；检查 `-1`、0 和设备错误状态。 |
| 读取 | `read(qint64)` | 读取最多指定字节并返回 QByteArray。 | 空数组可能是无数据、EOF 或错误，不能单独判断原因。 |
| 读取 | `readAll()` | 读取当前可获得的所有数据。 | 大数据设备上可能一次分配很大内存；网络协议通常应分帧读取。 |
| 读取 | `readLine(char *, qint64)` | 读取一行到调用者缓冲区。 | 行长度超过缓冲区时要设计分段或动态缓冲策略。 |
| 读取 | `readLine(qint64)` | 读取一行并返回 QByteArray。 | 文本行仍可能包含换行符；二进制数据不要靠它解析。 |
| 读取 | `readLineInto(...)` | 把一行读入 QByteArray 或 span 缓冲区，减少临时分配。 | Qt 6.9 起提供；调用者负责保证缓冲区有效，长度不足时要检查结果。 |
| 读取 | `canReadLine()` | 判断当前缓冲中是否存在完整行。 | 只适合以换行分隔的协议；不表示远端不会继续发送。 |
| 读取 | `peek(char *, qint64)` / `peek(qint64)` | 查看数据但不移动读位置。 | 适合检查协议头；顺序设备上的 peek 缓冲仍受设备实现限制。 |
| 读取 | `skip(qint64)` | 跳过指定数量的可读数据。 | 可能实际跳过更少；检查返回值和错误。 |
| 字节操作 | `getChar(char *)` | 读取一个字节。 | 适合小型协议解析；高吞吐代码优先批量读取。 |
| 字节操作 | `ungetChar(char)` | 将一个字节放回设备的读缓冲。 | 只适合少量回退；不能当作通用事务回滚。 |
| 写入 | `write(const char *, qint64)` | 写入指定长度的原始字节。 | 返回接受的字节数，可能是部分写入；不要默认已持久化。 |
| 写入 | `write(const char *)` | 写入以零结尾的 C 字符串。 | 二进制数据不要使用，内部依赖 `strlen`。 |
| 写入 | `write(const QByteArray &)` | 写入 QByteArray 内容。 | 处理大块数据时仍检查返回值和 bytesToWrite。 |
| 字节操作 | `putChar(char)` | 写入一个字节。 | 适合协议标记；大量数据不要逐字节调用。 |
| 缓冲 | `bytesAvailable()` | 返回当前可立即读取的字节数。 | 不代表完整业务消息，也不代表远端总数据量。 |
| 缓冲 | `bytesToWrite()` | 返回内部尚未写出的字节数。 | 不等同于已经写到磁盘或对端确认。 |
| 等待 | `waitForReadyRead(int)` | 阻塞等待可读数据或超时。 | 不要在 GUI 线程使用；后台同步封装必须有有限超时。 |
| 等待 | `waitForBytesWritten(int)` | 阻塞等待部分数据写出或超时。 | 可能阻塞事件处理；网络业务优先使用异步信号。 |
| 事务 | `startTransaction()` | 开始一个可回滚的读取事务。 | 主要用于半包解析；不是数据库事务，也不能回滚外部副作用。 |
| 事务 | `commitTransaction()` | 提交当前设备读取事务。 | 提交后不能再回滚已消费的数据；检查底层流状态。 |
| 事务 | `rollbackTransaction()` | 回滚当前设备读取事务。 | 设备必须支持相应回滚语义；写入行为不会被撤销。 |
| 事务 | `isTransactionStarted()` | 判断设备读取事务是否活动。 | 只能说明事务状态，不表示数据已经构成完整协议帧。 |
| 通道 | `readChannelCount()` / `writeChannelCount()` | 查询设备读写通道数量。 | 多通道设备要明确当前通道和各通道信号。 |
| 通道 | `currentReadChannel()` / `currentWriteChannel()` | 查询当前读写通道。 | 通道切换会改变后续 read/write 目标。 |
| 通道 | `setCurrentReadChannel(int)` / `setCurrentWriteChannel(int)` | 切换当前读写通道。 | 索引必须有效；切换前确认设备已经打开。 |
| 错误 | `errorString()` | 返回最近一次错误的文字描述。 | 用于日志和诊断，不应依赖文字内容做程序分支。 |
| 信号 | `readyRead()` | 通知当前有新数据可读。 | 不保证完整消息；槽函数应尽快读取并返回。 |
| 信号 | `channelReadyRead(int)` | 通知指定通道有数据可读。 | 多通道设备要使用信号参数选择正确通道。 |
| 信号 | `bytesWritten(qint64)` | 通知一部分数据已写入设备。 | 不等同于业务层确认或持久化完成。 |
| 信号 | `channelBytesWritten(int, qint64)` | 通知指定写通道写出数据。 | 关注通道参数和部分写入语义。 |
| 信号 | `aboutToClose()` | 设备即将关闭时通知观察者。 | 适合刷新状态；不要在其中再次启动依赖该设备的写操作。 |
| 信号 | `readChannelFinished()` | 顺序读取通道已经结束。 | 与当前暂时无数据不同，通常表示不会再有数据。 |
| 派生接口 | `readData(char *, qint64)` | 派生类真正提供底层读取实现。 | 纯虚函数；明确 EOF、无数据、错误和部分读取的返回语义。 |
| 派生接口 | `readLineData(char *, qint64)` | 派生类可优化逐行读取。 | 默认实现会基于普通读取；只在设备有高效行读取能力时重写。 |
| 派生接口 | `skipData(qint64)` | 派生类可优化跳过数据。 | Qt 6.0 起可用；返回实际跳过量或错误。 |
| 派生接口 | `writeData(const char *, qint64)` | 派生类真正提供底层写入实现。 | 纯虚函数；要处理部分写入、错误和缓冲策略。 |
| 派生状态 | `setOpenMode(OpenMode)` | 派生类更新设备打开模式。 | 受保护接口；通常在 `open()` 和 `close()` 的实现中使用。 |
| 派生状态 | `setErrorString(QString)` | 派生类设置面向诊断的错误文本。 | 受保护接口；不要用它代替更明确的错误状态设计。 |

---

### 一句话总结

`QIODevice` 是 Qt I/O 的共同契约：先判断设备是否顺序访问，再决定同步还是事件驱动读取；用 `readyRead()` 处理到达，用缓冲和协议边界处理半包，用返回值和 `errorString()` 处理失败，才不会把“暂时没数据”和“设备已经坏了”混为一谈。
