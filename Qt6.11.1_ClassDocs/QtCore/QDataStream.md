# QDataStream

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 二进制数据流，负责按 Qt 定义的格式序列化和反序列化基本类型及 Qt 类型。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QDataStream`：二进制数据流，负责按 Qt 定义的格式序列化和反序列化基本类型及 Qt 类型。

**内部模型：** 文件和 I/O 类型把路径/设备描述与打开后的读写状态分开。打开模式决定可执行的操作，当前位置、缓冲区、文本编码、权限和错误状态共同决定一次读写是否正确。

**适用场景：** 构造稳定路径，选择正确的 OpenMode，检查 open 和 errorString，按数据规模使用流式读写或分块处理，明确文本编码，完成后关闭并处理失败。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要手写平台分隔符；不要默认相对路径指向程序目录；不要把本地编码、UTF-8 和二进制混在一起；写文件时要考虑临时文件、覆盖、权限和原子替换。

## 2. 依赖与对象关系

- 头文件：`#include <QDataStream>`
- 继承自：QIODeviceBase
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

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

### 公有类型

- `enum ByteOrder { BigEndian, LittleEndian }`
- `enum FloatingPointPrecision { SinglePrecision, DoublePrecision }`
- `enum Status { Ok, ReadPastEnd, ReadCorruptData, WriteFailed, SizeLimitExceeded }`
- `enum Version { Qt_1_0, Qt_2_0, Qt_2_1, Qt_3_0, Qt_3_1, …, Qt_6_11 }`

### 公有函数

- `QDataStream()`
- `QDataStream(QIODevice *d)`
- `QDataStream(const QByteArray &a)`
- `QDataStream(QByteArray *a, QIODeviceBase::OpenMode mode)`
- `~QDataStream()`
- `void abortTransaction()`
- `bool atEnd() const`
- `QDataStream::ByteOrder byteOrder() const`
- `bool commitTransaction()`
- `QIODevice * device() const`
- `QDataStream::FloatingPointPrecision floatingPointPrecision() const`
- `(since 6.7) QDataStream & readBytes(char *&s, qint64 &l)`
- `qint64 readRawData(char *s, qint64 len)`
- `void resetStatus()`
- `void rollbackTransaction()`
- `void setByteOrder(QDataStream::ByteOrder bo)`
- `void setDevice(QIODevice *d)`
- `void setFloatingPointPrecision(QDataStream::FloatingPointPrecision precision)`
- `void setStatus(QDataStream::Status status)`
- `void setVersion(int v)`
- `qint64 skipRawData(qint64 len)`
- `void startTransaction()`
- `QDataStream::Status status() const`
- `int version() const`
- `QDataStream & writeBytes(const char *s, qint64 len)`
- `qint64 writeRawData(const char *s, qint64 len)`
- `(since 6.10) operator bool() const`
- `QDataStream & operator<<(qint8 i)`
- `QDataStream & operator<<(bool i)`
- `(since 6.0) QDataStream & operator<<(char16_t c)`
- `(since 6.0) QDataStream & operator<<(char32_t c)`
- `QDataStream & operator<<(const char *s)`
- `QDataStream & operator<<(double f)`
- `QDataStream & operator<<(float f)`
- `QDataStream & operator<<(qint16 i)`
- `QDataStream & operator<<(qint32 i)`
- `QDataStream & operator<<(qint64 i)`
- `QDataStream & operator<<(quint16 i)`
- `QDataStream & operator<<(quint32 i)`
- `QDataStream & operator<<(quint64 i)`
- `QDataStream & operator<<(quint8 i)`
- `QDataStream & operator<<(std::nullptr_t ptr)`
- `QDataStream & operator>>(bool &i)`
- `QDataStream & operator>>(qint8 &i)`
- `QDataStream & operator>>(char *&s)`
- `(since 6.0) QDataStream & operator>>(char16_t &c)`
- `(since 6.0) QDataStream & operator>>(char32_t &c)`
- `QDataStream & operator>>(double &f)`
- `QDataStream & operator>>(float &f)`
- `QDataStream & operator>>(qint16 &i)`
- `QDataStream & operator>>(qint32 &i)`
- `QDataStream & operator>>(qint64 &i)`
- `QDataStream & operator>>(quint16 &i)`
- `QDataStream & operator>>(quint32 &i)`
- `QDataStream & operator>>(quint64 &i)`
- `QDataStream & operator>>(quint8 &i)`
- `QDataStream & operator>>(std::nullptr_t &ptr)`

### 相关非成员函数

- `(since 6.0) QDataStream & operator<<(QDataStream &out, const std::pair<T1, T2> &pair)`
- `(since 6.0) QDataStream & operator>>(QDataStream &in, std::pair<T1, T2> &pair)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QDataStream::ByteOrder`

**作用与语义：**

用于读取/写入数据的字节顺序。 - `QDataStream::BigEndian`: `QSysInfo::BigEndian`；最高有效字节优先（默认） - `QDataStream::LittleEndian`: `QSysInfo::LittleEndian`；最低有效字节优先。

### `enum QDataStream::FloatingPointPrecision`

**作用与语义：**

用于读写数据的浮点数精度。这只会在数据流版本`Qt_4_6`或更高时产生影响。
警告：浮点精度必须在写入对象和读取数据流的对象上设置为相同的值。
- `QDataStream::SinglePrecision`：`0`;数据流中的所有浮点数精度为32位。
- `QDataStream::DoublePrecision`：`1`;数据流中所有浮点数的精度为64位。

### `enum QDataStream::Status`

**作用与语义：**

该枚举描述了数据流的当前状态。
- `QDataStream::Ok`：`0`;数据流运行正常。
- `QDataStream::ReadPastEnd`：`1`;数据流已读取超过底层设备数据的末端。
- `QDataStream::ReadCorruptData`：`2`;数据流读取了损坏的数据。
- `QDataStream::WriteFailed`：`3`;数据流无法写入底层设备。
- `QDataStream::SizeLimitExceeded (since Qt 6.7)`：`4`;数据流无法读写数据，因为其规模超出当前平台的支持。例如，在尝试在32位平台上读取超过2 GiB的数据时，这种情况就会发生。

### `enum QDataStream::Version`

**作用与语义：**

该枚举为数据序列化格式的版本号提供了符号同义词。
- `QDataStream::Qt_1_0`：`1`
- `QDataStream::Qt_2_0`：`2`
- `QDataStream::Qt_2_1`：`3`
- `QDataStream::Qt_3_0`：`4`
- `QDataStream::Qt_3_1`：`5`
- `QDataStream::Qt_3_3`：`6`
- `QDataStream::Qt_4_0`：`7`
- `QDataStream::Qt_4_1`：`Qt_4_0`
- `QDataStream::Qt_4_2`：`8`
- `QDataStream::Qt_4_3`：`9`
- `QDataStream::Qt_4_4`：`10`
- `QDataStream::Qt_4_5`：`11`
- `QDataStream::Qt_4_6`：`12`
- `QDataStream::Qt_4_7`：`Qt_4_6`
- `QDataStream::Qt_4_8`：`Qt_4_7`
- `QDataStream::Qt_4_9`：`Qt_4_8`
- `QDataStream::Qt_5_0`：`13`
- `QDataStream::Qt_5_1`：`14`
- `QDataStream::Qt_5_2`：`15`
- `QDataStream::Qt_5_3`：`Qt_5_2`
- `QDataStream::Qt_5_4`：`16`
- `QDataStream::Qt_5_5`：`Qt_5_4`
- `QDataStream::Qt_5_6`：`17`
- `QDataStream::Qt_5_7`：`Qt_5_6`
- `QDataStream::Qt_5_8`：`Qt_5_7`
- `QDataStream::Qt_5_9`：`Qt_5_8`
- `QDataStream::Qt_5_10`：`Qt_5_9`
- `QDataStream::Qt_5_11`：`Qt_5_10`
- `QDataStream::Qt_5_12`：`18`
- `QDataStream::Qt_5_13`：`19`
- `QDataStream::Qt_5_14`：`Qt_5_13`
- `QDataStream::Qt_5_15`：`Qt_5_14`
- `QDataStream::Qt_6_0`：`20`
- `QDataStream::Qt_6_1`：`Qt_6_0`
- `QDataStream::Qt_6_2`：`Qt_6_0`
- `QDataStream::Qt_6_3`：`Qt_6_0`
- `QDataStream::Qt_6_4`：`Qt_6_0`
- `QDataStream::Qt_6_5`：`Qt_6_0`
- `QDataStream::Qt_6_6`：`21`
- `QDataStream::Qt_6_7`：`22`
- `QDataStream::Qt_6_8`：`Qt_6_7`
- `QDataStream::Qt_6_9`：`Qt_6_7`
- `QDataStream::Qt_6_10`：`23`
- `QDataStream::Qt_6_11`：`24`

### `QDataStream::QDataStream()`

**作用与语义：**

构建一个没有I/O设备的数据流。

### `[explicit] QDataStream::QDataStream(QIODevice *d)`

**作用与语义：**

构建使用I/O设备`d`的数据流。

### `QDataStream::QDataStream(const QByteArray &a)`

**作用与语义：**

构建一个只读数据流，操作字节数组`a`。如果你想写入字节数组，可以使用QDataStream（`QByteArray`*， int）。
由于`QByteArray`不是`QIODevice`子类，内部会创建一个`QBuffer`来包裹字节数组。

### `QDataStream::QDataStream(QByteArray *a, QIODeviceBase::OpenMode mode)`

**作用与语义：**

构建一个在字节阵列`a`上运行的数据流。`mode`描述了设备的使用方式。
或者，如果你只是想从字节数组读取，也可以用QDataStream（const `QByteArray` &）。
由于`QByteArray`不是`QIODevice`子类，内部会创建一个`QBuffer`来包裹字节数组。

### `[noexcept] QDataStream::~QDataStream()`

**作用与语义：**

会破坏数据流。
除非是内部I/O设备（例如`QBuffer`）处理构造器传递的`QByteArray`，否则解散器不会影响当前的I/O设备，在这种情况下，内部I/O设备会被销毁。

### `void QDataStream::abortTransaction()`

**作用与语义：**

中止已读交易。
该功能通常用于在更高层次协议错误或流同步丢失后丢弃交易。
如果在内部事务中调用，中止任务会委托到最外层事务，随后启动的内部事务会被强制失败。
对于最外层事务，丢弃恢复点和流内部复制的数据。不会影响流当前的读取位置。
将数据流状态设置为。
- `ReadCorruptData`： 。

### `bool QDataStream::atEnd() const`

**作用与语义：**

如果 I/O 设备已到达终止位置（流或文件的末端），或未设置 I/O 设备，返回 `true`;否则返回 `false`。

### `QDataStream::ByteOrder QDataStream::byteOrder() const`

**作用与语义：**

返回当前字节顺序设置——`BigEndian`或`LittleEndian`。

### `bool QDataStream::commitTransaction()`

**作用与语义：**

完成一次读取事务。如果事务中没有发生读取错误，返回`true`;否则返回`false`。
如果在内部事务中调用，提交将被推迟，直到最外层的commitTransaction()、`rollbackTransaction()`或`abortTransaction()`调用发生。
否则，如果流状态显示已读取超过数据的末端，该函数会将流数据恢复到`startTransaction()`调用的节点。当发生这种情况时，你需要等待更多数据到达，之后再开始新的事务。如果数据流读取了损坏的数据或任何内部事务被中止，该函数会中止该事务。

### `QIODevice *QDataStream::device() const`

**作用与语义：**

返回当前设置的I/O设备，或者如果没有设备设置，则返回`nullptr`。

### `QDataStream::FloatingPointPrecision QDataStream::floatingPointPrecision() const`

**作用与语义：**

返回数据流的浮点精度。

### `[since 6.7] QDataStream &QDataStream::readBytes(char *&s, qint64 &l)`

**作用与语义：**

从流读取缓冲区`s`并返回流的引用。
缓冲区`s`是用`new []`分配的。用`delete []`操作符销毁它。
`l`参数设置为缓冲区长度。如果字符串读取为空，`l`设为0，`s`设为`nullptr`。
序列化格式是先用长度指定符，然后是`l`字节的数据。如果版本小于6.7或元素数小于0xfffffffe（2^32 -2），长度指定符为1 quint32，否则会有一个扩展值0xfffffffe后面跟一个quint64，后面是实际值。此外，对于支持 isNull() 的容器，它被编码为一个 quint32，所有位都设置为且没有数据。

### `qint64 QDataStream::readRawData(char *s, qint64 len)`

**作用与语义：**

最多从流中读取`len`字节到`s`，返回已读字节数。如果发生错误，该函数返回-1。
缓冲区`s`必须预分配。数据不会被解码。

### `void QDataStream::resetStatus()`

**作用与语义：**

重置数据流状态。

### `void QDataStream::rollbackTransaction()`

**作用与语义：**

回退已读事务。
该函数通常用于在提交事务前检测到不完整读取时回滚事务。
如果在内部事务中被调用，恢复任务会委托到最外层事务，随后启动的内部事务会被强制失败。
对于最外层事务， 将流数据恢复到`startTransaction()`调用点。如果数据流读取损坏数据或任何内部事务被中止，该函数会中止该事务。
如果之前的流操作成功，则将数据流状态设置为。
- `ReadPastEnd`： 。

### `void QDataStream::setByteOrder(QDataStream::ByteOrder bo)`

**作用与语义：**

将序列化字节顺序设置为`bo`。
`bo`参数可以是`QDataStream::BigEndian`或`QDataStream::LittleEndian`。
默认设置是大端序。除非有特殊需求，否则建议不要使用这个设置。

### `void QDataStream::setDevice(QIODevice *d)`

**作用与语义：**

void QDataStream：：setDevice（`QIODevice` *d）。
将I/O设备设置为`d`，可以`nullptr`为当前I/O设备。

### `void QDataStream::setFloatingPointPrecision(QDataStream::FloatingPointPrecision precision)`

**作用与语义：**

将数据流的浮点精度设置为`precision`。如果浮点精度为`DoublePrecision`且数据流版本为`Qt_4_6`或更高，所有浮点数将以64位精度写入和读取。如果浮点精度为`SinglePrecision`且版本为`Qt_4_6`或更高，则所有浮点数将以32位精度写入和读取。
对于`Qt_4_6`之前的版本，数据流中浮点数的精度取决于调用的流操作符。
默认是`DoublePrecision`。
注意，该属性不影响`qfloat16`实例的序列化或反序列化。
警告：该属性必须在写入对象和读取数据流的对象上设置为相同的值。

### `void QDataStream::setStatus(QDataStream::Status status)`

**作用与语义：**

将数据流的状态设置为给定的 `status`。
后续对 setStatus() 的调用会被忽略，直到调用 `resetStatus()`。

### `void QDataStream::setVersion(int v)`

**作用与语义：**

将数据序列化格式的版本号设置为`v`，`Version`枚举的值。
如果你使用当前版本的 Qt，不必设置版本，但对于你自己的自定义二进制格式，我们建议你设置;详见详细说明中的`Versioning`。
为了适应新功能，部分Qt类的数据流序列化格式在某些版本中有所更改。如果你想读取由早期Qt版本创建的数据，或写入用早期Qt编译的程序可读取的数据，可以使用该函数修改`QDataStream`所使用的序列化格式。
`Version`枚举为不同版本的Qt提供了符号常数。例如：

**官方示例：**

```cpp
 QDataStream out(&file);
 out.setVersion(QDataStream::Qt_4_0);
```

### `qint64 QDataStream::skipRawData(qint64 len)`

**作用与语义：**

从设备中跳过`len`字节。返回实际跳过的字节数，或错误时返回-1字节数。
这相当于调用长度为`len`的缓冲区上的`readRawData()`并忽略该缓冲区。

### `void QDataStream::startTransaction()`

**作用与语义：**

在流上启动一个新的读取事务。
在读取操作序列中定义一个可恢复的点。对于顺序设备，读取的数据将在内部被复制，以便在读取不完整的情况下进行恢复。对于随机访问设备，此函数会保存流的当前位置。调用 `commitTransaction()`、`rollbackTransaction()` 或 `abortTransaction()` 来完成当前事务。
一旦事务启动，随后对该函数的调用将使事务成为递归的。内部事务充当最外层事务的代理（即，将读取操作的状态报告给最外层事务，最外层事务可以恢复流的位置）。
注意：不支持恢复到嵌套 startTransaction() 调用的点。
当事务发生错误时（包括内部事务失败），从数据流中读取将被暂停（随后所有读取操作返回空值或零值），并且随后的内部事务将被强制失败。启动一个新的最外层事务可以从该状态中恢复。此行为使得无需单独检查每个读取操作的错误。

### `QDataStream::Status QDataStream::status() const`

**作用与语义：**

返回数据流的状态。

### `int QDataStream::version() const`

**作用与语义：**

返回数据序列化格式的版本号。

### `QDataStream &QDataStream::writeBytes(const char *s, qint64 len)`

**作用与语义：**

写入长度指定符`len`，缓冲区`s`给流，返回流的引用。
`len`序列化为quint32和可选的quint64，后面是`s`的`len`字节。注意，数据未编码。

### `qint64 QDataStream::writeRawData(const char *s, qint64 len)`

**作用与语义：**

从`s`写入`len`字节到流。返回实际写入的字节数，错误时返回-1字节数。数据未编码。

### `[explicit noexcept, since 6.10] QDataStream::operator bool() const`

**作用与语义：**

返回该流是否无错误（`status()`返回`Ok`）。

### `QDataStream &QDataStream::operator<<(qint8 i)`

**作用与语义：**

向流写入签名字节 `i`，并返回流的引用。

### `QDataStream &QDataStream::operator<<(bool i)`

**作用与语义：**

向流写入一个布尔值 `i`。返回流的引用。

### `[since 6.0] QDataStream &QDataStream::operator<<(char16_t c)`

**作用与语义：**

向流写入字符 `c`。返回流的引用。

### `[since 6.0] QDataStream &QDataStream::operator<<(char32_t c)`

**作用与语义：**

向流写入字符 `c`。返回流的引用。

### `QDataStream &QDataStream::operator<<(const char *s)`

**作用与语义：**

将“\0”终止字符串写入`s`流，并返回流的引用。
字符串通过`writeBytes()`序列化。

### `QDataStream &QDataStream::operator<<(double f)`

**作用与语义：**

使用标准IEEE 754格式向流写入浮点数`f`。返回流的引用。

### `QDataStream &QDataStream::operator<<(float f)`

**作用与语义：**

使用标准IEEE 754格式向流写入浮点数`f`。返回流的引用。

### `QDataStream &QDataStream::operator<<(qint16 i)`

**作用与语义：**

向流写入一个带符号的16位整数，`i`，并返回流的引用。

### `QDataStream &QDataStream::operator<<(qint32 i)`

**作用与语义：**

向流写入一个有符号的32位整数`i`，并返回流的引用。

### `QDataStream &QDataStream::operator<<(qint64 i)`

**作用与语义：**

向流写入一个带符号的64位整数，`i`，并返回流的引用。

### `QDataStream &QDataStream::operator<<(quint16 i)`

**作用与语义：**

向流写入一个无符号的16位整数，`i`，并返回流的引用。

### `QDataStream &QDataStream::operator<<(quint32 i)`

**作用与语义：**

将一个无符号整数`i`写入流，作为32位无符号整数（quint32）。返回流的引用。

### `QDataStream &QDataStream::operator<<(quint64 i)`

**作用与语义：**

向流写入一个无符号的64位整数，`i`，并返回流的引用。

### `QDataStream &QDataStream::operator<<(quint8 i)`

**作用与语义：**

写入一个无符号字节 `i`，并返回流的引用。

### `QDataStream &QDataStream::operator<<(std::nullptr_t ptr)`

**作用与语义：**

模拟向流写入`std::nullptr_t` `ptr`，并返回流的引用。该函数实际上不写入流，因为`std::nullptr_t`值以0字节形式存储。

### `QDataStream &QDataStream::operator>>(bool &i)`

**作用与语义：**

从流读取一个布尔值到`i`。返回流的引用。

### `QDataStream &QDataStream::operator>>(qint8 &i)`

**作用与语义：**

从流中读取一个签名字节到`i`，并返回流的引用。

### `QDataStream &QDataStream::operator>>(char *&s)`

**作用与语义：**

从流中读取字符串`s`并返回流的引用。
字符串通过 `readBytes()` 进行反序列化，其中序列化格式先是一个`quint32`长度的指定符，然后是相应数量的数据字节。最终字符串总是以“\0”结尾。
字符串的空间通过`new []`分配——调用者必须用`delete []`销毁它。

### `[since 6.0] QDataStream &QDataStream::operator>>(char16_t &c)`

**作用与语义：**

从流中读取一个16位宽的字符到`c`并返回流的引用。

### `[since 6.0] QDataStream &QDataStream::operator>>(char32_t &c)`

**作用与语义：**

从流中读取一个32位宽的字符`c`并返回流的引用。

### `QDataStream &QDataStream::operator>>(double &f)`

**作用与语义：**

使用标准IEEE 754格式，将流中的浮点数读取到`f`。返回流的引用。

### `QDataStream &QDataStream::operator>>(float &f)`

**作用与语义：**

使用标准IEEE 754格式，将流中的浮点数读取到`f`。返回流的引用。

### `QDataStream &QDataStream::operator>>(qint16 &i)`

**作用与语义：**

从流中读取一个带符号的16位整数到`i`，并返回对流的引用。

### `QDataStream &QDataStream::operator>>(qint32 &i)`

**作用与语义：**

从流中读取一个带符号的32位整数到`i`，并返回流的引用。

### `QDataStream &QDataStream::operator>>(qint64 &i)`

**作用与语义：**

从流中读取一个有符号的64位整数到`i`，并返回流的引用。

### `QDataStream &QDataStream::operator>>(quint16 &i)`

**作用与语义：**

从流中读取一个无符号的16位整数到`i`，并返回对流的引用。

### `QDataStream &QDataStream::operator>>(quint32 &i)`

**作用与语义：**

从流中读取一个无符号的32位整数到`i`，并返回流的引用。

### `QDataStream &QDataStream::operator>>(quint64 &i)`

**作用与语义：**

从流中读取一个无符号的64位整数，进入`i`，并返回对流的引用。

### `QDataStream &QDataStream::operator>>(quint8 &i)`

**作用与语义：**

从流中读取一个无符号字节到`i`，并返回流的引用。

### `QDataStream &QDataStream::operator>>(std::nullptr_t &ptr)`

**作用与语义：**

模拟从流读取`std::nullptr_t`到`ptr`，并返回流的引用。该函数实际上不从流中读取任何数据，因为`std::nullptr_t`值以0字节形式存储。

### `[since 6.0] template <typename T1, typename T2> QDataStream &operator<<(QDataStream &out, const std::pair<T1, T2> &pair)`

**作用与语义：**

写入`pair`流式`out`。
该函数需要T1和T2类型来实现`operator<<()`。

### `[since 6.0] template <typename T1, typename T2> QDataStream &operator>>(QDataStream &in, std::pair<T1, T2> &pair)`

**作用与语义：**

读取一对从流`in`到`pair`。
该函数需要 T1 和 T2 类型来实现 `operator>>()`。

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

`QDataStream` 所属机制类型：文件、设备与流机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
