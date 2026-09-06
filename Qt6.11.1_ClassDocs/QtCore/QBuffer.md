# QBuffer

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 以内存字节数组为后端的 QIODevice，适合把内存数据接入流式读写 API。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QBuffer`：以内存字节数组为后端的 QIODevice，适合把内存数据接入流式读写 API。

**内部模型：** 文件和 I/O 类型把路径/设备描述与打开后的读写状态分开。打开模式决定可执行的操作，当前位置、缓冲区、文本编码、权限和错误状态共同决定一次读写是否正确。

**适用场景：** 构造稳定路径，选择正确的 OpenMode，检查 open 和 errorString，按数据规模使用流式读写或分块处理，明确文本编码，完成后关闭并处理失败。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要手写平台分隔符；不要默认相对路径指向程序目录；不要把本地编码、UTF-8 和二进制混在一起；写文件时要考虑临时文件、覆盖、权限和原子替换。

## 2. 依赖与对象关系

- 头文件：`#include <QBuffer>`
- 继承自：QIODevice
- 直接派生类：未在类页中列出

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

构造稳定路径，选择正确的 OpenMode，检查 open 和 errorString，按数据规模使用流式读写或分块处理，明确文本编码，完成后关闭并处理失败。 使用时通常按这个过程组织：构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

```cpp
QFile file(path);
if (file.open(QIODevice::ReadOnly | QIODevice::Text)) {
    const QByteArray data = file.readAll();
}
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QBuffer(QObject *parent = nullptr)`
- `QBuffer(QByteArray *byteArray, QObject *parent = nullptr)`
- `virtual ~QBuffer()`
- `QByteArray & buffer()`
- `const QByteArray & buffer() const`
- `const QByteArray & data() const`
- `void setBuffer(QByteArray *byteArray)`
- `void setData(const QByteArray &data)`
- `void setData(const char *data, qsizetype size)`

### 重实现的公有函数

- `virtual bool atEnd() const override`
- `virtual bool canReadLine() const override`
- `virtual void close() override`
- `virtual bool open(QIODeviceBase::OpenMode mode) override`
- `virtual qint64 pos() const override`
- `virtual bool seek(qint64 pos) override`
- `virtual qint64 size() const override`

### 重实现的保护函数

- `virtual qint64 readData(char *data, qint64 len) override`
- `virtual qint64 writeData(const char *data, qint64 len) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[explicit] QBuffer::QBuffer(QObject *parent = nullptr)`

**作用与语义：**

用给定的 `parent` 构建一个空缓冲区。你可以调用 `setData()` 来填充缓冲区数据，或者在写入模式打开并使用 `write()`。

### `QBuffer::QBuffer(QByteArray *byteArray, QObject *parent = nullptr)`

**作用与语义：**

构建一个QBuffer，使用`byteArray`指向的`QByteArray`作为内部缓冲区，并带有给定的`parent`。调用者负责确保`byteArray`在QBuffer被销毁或`setBuffer()`被调用更改缓冲区之前保持有效。QBuffer不拥有`QByteArray`的所有权。
如果你以只写或读写模式打开缓冲区，并向QBuffer写入内容，`byteArray`会被修改。

**官方示例：**

```cpp
     QByteArray byteArray("abc");
     QBuffer buffer(&byteArray);
     buffer.open(QIODevice::WriteOnly);
     buffer.seek(3);
     buffer.write("def", 3);
     buffer.close();
     // byteArray == "abcdef"
```

### `[virtual noexcept] QBuffer::~QBuffer()`

**作用与语义：**

会破坏缓冲区。

### `[override virtual] bool QBuffer::atEnd() const`

**作用与语义：**

重装：`QIODevice::atEnd()` const.
如果当前读写位置位于设备末端（即设备上没有更多可读取的数据），返回`true`;否则返回`false`。
对于某些设备，atEnd() 即使有更多数据可读取，也可能返回 true。这种特殊情况仅适用于那些在你调用 `read()` 时直接生成数据的设备（例如，Unix 和 macOS 上的 `/dev` 或 `/proc` 文件，或所有平台上的控制台输入/`stdin`）。

### `QByteArray &QBuffer::buffer()`

**作用与语义：**

返回`QBuffer`内部缓冲区的引用。你可以用它在`QBuffer`背后修改`QByteArray`。

### `const QByteArray &QBuffer::buffer() const`

**作用与语义：**

这和`data()`一样。

### `[override virtual] bool QBuffer::canReadLine() const`

**作用与语义：**

重装：`QIODevice::canReadLine()` const.
如果能从设备读取完整数据行，返回`true`;否则返回`false`。
注意，未缓冲设备无法确定可读取内容，总是返回false。
该功能通常与`readyRead()`信号结合使用。
重新实现该函数的子类必须调用基础实现，以包含`QIODevice`缓冲区的内容。示例：

### `[override virtual] void QBuffer::close()`

**作用与语义：**

重装：`QIODevice::close()`。
先发出`aboutToClose()`，然后关闭设备并将其 OpenMode 设置为 NotOpen。错误字符串也会被重置。

### `const QByteArray &QBuffer::data() const`

**作用与语义：**

返回缓冲区中的数据。
这和`buffer()`一样。

### `[override virtual] bool QBuffer::open(QIODeviceBase::OpenMode mode)`

**作用与语义：**

重实现自：`QIODevice::open`（QIODeviceBase：：OpenMode 模式）。
使用`mode`标志打开缓冲区，成功时返回`true`;否则返回`false`。
`mode`的标志必须包含`QIODeviceBase::ReadOnly`、`WriteOnly`或`ReadWrite`。如果没有，则会被打印出错误，方法失败。在其他情况下，它成功了。
与`QFile::open()`不同，开启`QBuffer`时用`WriteOnly`不会截断。不过，`pos()`设置为`0`。使用`Append`或`Truncate`来更改任一行为。
打开设备并将其 OpenMode 设置为 `mode`。成功时返回 `true`;否则返回 `false`。该函数应从任何重新实现的 open() 或其他打开设备的函数中调用。

### `[override virtual] qint64 QBuffer::pos() const`

**作用与语义：**

重装：`QIODevice::pos()` const.
对于随机访问设备，该函数返回数据写入或读取的位置。对于顺序设备或封闭设备，若不存在“当前位置”概念，则返回0。
设备的当前读写位置由`QIODevice`内部维护，因此无需重新实现此功能。在子类化`QIODevice`时，使用`QIODevice::seek()`通知`QIODevice`设备位置的变化。

### `[override virtual protected] qint64 QBuffer::readData(char *data, qint64 len)`

**作用与语义：**

Reimplements： `QIODevice::readData`（char *data， qint64 maxSize）.
从设备读取最多`maxSize`字节到`data`，返回读取字节数，或如果发生错误则返回-1字节。
如果没有字节可读且永远无法再有更多字节（例如套接字闭合、管道闭合、子进程已完成），该函数返回 -1。
该函数由`QIODevice`调用。创建`QIODevice`子类时重新实现该函数。
在重新实现该函数时，重要的是该函数在返回前读取所有所需数据。这是 `QDataStream` 能够操作该类的必要条件。`QDataStream` 假设所有请求的信息都已读取，因此如果存在问题，不会重新尝试读取。
该函数可调用 maxSize 为 0，可用于执行读取后操作。

### `[override virtual] bool QBuffer::seek(qint64 pos)`

**作用与语义：**

重装：`QIODevice::seek`（qint64 pos）。
对于随机访问设备，该函数将当前位置设置为`pos`，成功时返回true，发生错误时返回false。对于顺序设备，默认行为是发送警告并返回false。
在子类`QIODevice`时，你必须在函数开头调用 QIODevice：：seek()，以确保与 `QIODevice` 内置缓冲区的完整性。

### `void QBuffer::setBuffer(QByteArray *byteArray)`

**作用与语义：**

使`QBuffer`使用`byteArray`指向的`QByteArray`作为内部缓冲区。调用者负责确保`byteArray`在`QBuffer`被销毁或调用setBuffer()更改缓冲区之前保持有效。`QBuffer`不对`QByteArray`拥有权。
如果`isOpen()`是真的，那就什么都没用。
如果你以只写或读写模式打开缓冲区并写入`QBuffer`，`byteArray`会被修改。
如果`byteArray` `nullptr`，缓冲区会创建自己的内部`QByteArray`来处理。该字节数组最初是空的。

**官方示例：**

```cpp
     QByteArray byteArray("abc");
     QBuffer buffer;
     buffer.setBuffer(&byteArray);
     buffer.open(QIODevice::WriteOnly);
     buffer.seek(3);
     buffer.write("def", 3);
     buffer.close();
     // byteArray == "abcdef"
```

### `void QBuffer::setData(const QByteArray &data)`

**作用与语义：**

将内部缓冲区的内容设置为`data`。这与将`data`分配给`buffer()`是一样的。
如果`isOpen()`是真的，那也无济于事。

### `void QBuffer::setData(const char *data, qsizetype size)`

**作用与语义：**

将内部缓冲区的内容设置为`data`的前`size`字节。
注意：在 6.5 之前的 Qt 版本中，该函数以长度为`int`参数，可能会截断大小。

### `[override virtual] qint64 QBuffer::size() const`

**作用与语义：**

重装：`QIODevice::size()` const.
对于开放随机访问设备，该函数返回设备的大小。对于开放顺序设备，返回`bytesAvailable()`。
如果设备关闭，返回的尺寸不会反映设备的实际大小。

### `[override virtual protected] qint64 QBuffer::writeData(const char *data, qint64 len)`

**作用与语义：**

Reimplements： `QIODevice::writeData`（const char *data， qint64 maxSize）.
从`data`写入最多`maxSize`字节到设备。返回写入字节数，或如果发生错误则返回-1字节。
该函数由`QIODevice`调用。创建`QIODevice`子类时重新实现该函数。
在重新实现该函数时，重要的是该函数在返回前写入所有可用数据。这是`QDataStream`能够操作该类所必需的。`QDataStream`假设所有信息都已写入，因此如果出现问题，不会重试写入。

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

`QBuffer` 所属机制类型：文件、设备与流机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
