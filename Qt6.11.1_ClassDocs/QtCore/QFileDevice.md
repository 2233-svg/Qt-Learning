# QFileDevice

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QFileDevice` 是 文件、设备与流机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QFileDevice` 是 文件、设备与流机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 文件和 I/O 类型把路径/设备描述与打开后的读写状态分开。打开模式决定可执行的操作，当前位置、缓冲区、文本编码、权限和错误状态共同决定一次读写是否正确。

**适用场景：** 构造稳定路径，选择正确的 OpenMode，检查 open 和 errorString，按数据规模使用流式读写或分块处理，明确文本编码，完成后关闭并处理失败。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要手写平台分隔符；不要默认相对路径指向程序目录；不要把本地编码、UTF-8 和二进制混在一起；写文件时要考虑临时文件、覆盖、权限和原子替换。

## 2. 依赖与对象关系

- 头文件：`#include <QFileDevice>`
- 继承自：QIODevice
- 直接派生类：QFile、QSaveFile

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

### 公有类型

- `enum FileError { NoError, ReadError, WriteError, FatalError, ResourceError, …, CopyError }`
- `enum FileHandleFlag { AutoCloseHandle, DontCloseHandle }`
- `flags FileHandleFlags`
- `enum FileTime { FileAccessTime, FileBirthTime, FileMetadataChangeTime, FileModificationTime }`
- `enum MemoryMapFlag { NoOptions, MapPrivateOption }`
- `flags MemoryMapFlags`
- `enum Permission { ReadOwner, WriteOwner, ExeOwner, ReadUser, WriteUser, …, ExeOther }`
- `flags Permissions`

### 公有函数

- `virtual ~QFileDevice()`
- `QFileDevice::FileError error() const`
- `virtual QString fileName() const`
- `QDateTime fileTime(QFileDevice::FileTime time) const`
- `bool flush()`
- `int handle() const`
- `uchar * map(qint64 offset, qint64 size, QFileDevice::MemoryMapFlags flags = NoOptions)`
- `virtual QFileDevice::Permissions permissions() const`
- `virtual bool resize(qint64 sz)`
- `bool setFileTime(const QDateTime &newDate, QFileDevice::FileTime fileTime)`
- `virtual bool setPermissions(QFileDevice::Permissions permissions)`
- `bool unmap(uchar *address)`
- `void unsetError()`

### 重实现的公有函数

- `virtual bool atEnd() const override`
- `virtual void close() override`
- `virtual bool isSequential() const override`
- `virtual qint64 pos() const override`
- `virtual bool seek(qint64 pos) override`
- `virtual qint64 size() const override`

### 重实现的保护函数

- `virtual qint64 readData(char *data, qint64 len) override`
- `virtual qint64 readLineData(char *data, qint64 maxlen) override`
- `virtual qint64 writeData(const char *data, qint64 len) override`

### 公开宏

- `(since 6.8) QT_NO_USE_NODISCARD_FILE_OPEN`
- `(since 6.8) QT_USE_NODISCARD_FILE_OPEN`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QFileDevice::FileError`

**作用与语义：**

该枚举描述了`error()`函数可能返回的错误。
- `QFileDevice::NoError`：`0`;未发生错误。
- `QFileDevice::ReadError`：`1`;读取文件时发生错误。
- `QFileDevice::WriteError`：`2`;写入文件时发生错误。
- `QFileDevice::FatalError`：`3`;发生了致命错误。
- `QFileDevice::ResourceError`：`4`;资源不足（例如，打开文件过多、内存不足等）
- `QFileDevice::OpenError`：`5`;文件无法打开。
- `QFileDevice::AbortError`：`6`;行动被中止。
- `QFileDevice::TimeOutError`：`7`;暂停发生。
- `QFileDevice::UnspecifiedError`：`8`;发生了未说明的错误。
- `QFileDevice::RemoveError`：`9`;文件无法被删除。
- `QFileDevice::RenameError`：`10`;该文件无法重命名。
- `QFileDevice::PositionError`：`11`;文件中的位置无法更改。
- `QFileDevice::ResizeError`：`12`;文件无法调整大小。
- `QFileDevice::PermissionsError`：`13`;文件无法访问。
- `QFileDevice::CopyError`：`14`;文件无法复制。

### `enum QFileDevice::FileHandleFlagflags QFileDevice::FileHandleFlags`

**作用与语义：**

该枚举用于打开文件时指定仅适用于文件而非泛`QIODevice`的额外选项。
- `QFileDevice::AutoCloseHandle`：`0x0001`;传递给`open()`的文件句柄应由`close()`关闭，默认行为是关闭文件，应用程序负责关闭文件句柄。当按名称打开文件时，该标志被忽略，因为 Qt 始终拥有文件柄并必须关闭它。
- `QFileDevice::DontCloseHandle`：`0`;如果没有显式关闭，`QFile`对象被销毁时，底层文件句柄会保持开放。
FileHandleFlags 类型是 QFlags 的 typedef<FileHandleFlag>。它存储 FileHandleFlag 值的 OR 组合。

### `enum QFileDevice::FileTime`

**作用与语义：**

该枚举被`fileTime()`和`setFileTime()`函数使用。
- `QFileDevice::FileAccessTime`：`0`;文件最近一次被访问（例如读取或写入）。
- `QFileDevice::FileBirthTime`：`1`;文件创建时间（可能不支持 UNIX）。
- `QFileDevice::FileMetadataChangeTime`：`2`;文件元数据最后更改的时间。
- `QFileDevice::FileModificationTime`：`3`;文件最近一次修改的时间。

### `enum QFileDevice::MemoryMapFlagflags QFileDevice::MemoryMapFlags`

**作用与语义：**

该枚举描述了`map()`函数可能使用的特殊选项。
- `QFileDevice::NoOptions`：`0`;无选项。
- `QFileDevice::MapPrivateOption`：`0x0001`;映射后的内存将是私有的，因此任何修改对其他进程都不可见，也不会写入磁盘。当内存被取消映射时，任何此类修改都会丢失。目前尚不确定映射创建后对文件所做的修改是否会通过映射存储器可见。该枚举值是在Qt 5.4中引入的。
MemoryMapFlags 类型是 QFlags 的 typedef<MemoryMapFlag>。它存储 MemoryMapFlag 值的 OR 组合。

### `enum QFileDevice::Permissionflags QFileDevice::Permissions`

**作用与语义：**

此枚举由 permission() 函数使用，用于报告文件的权限和所有权。可将值进行 OR 运算以测试多个权限和所有权值。
- `QFileDevice::ReadOwner`: `0x4000`；文件可以被文件所有者读取。
- `QFileDevice::WriteOwner`: `0x2000`；文件可以被文件所有者写入。
- `QFileDevice::ExeOwner`: `0x1000`；文件可以被文件所有者执行。
- `QFileDevice::ReadUser`: `0x0400`；文件可以被用户读取。
- `QFileDevice::WriteUser`: `0x0200`；文件可以被用户写入。
- `QFileDevice::ExeUser`: `0x0100`；文件可以被用户执行。
- `QFileDevice::ReadGroup`: `0x0040`；文件可以被组读取。
- `QFileDevice::WriteGroup`: `0x0020`；文件可以被组写入。
- `QFileDevice::ExeGroup`: `0x0010`；文件可以被组执行。
- `QFileDevice::ReadOther`: `0x0004`；文件可以被其他人读取。
- `QFileDevice::WriteOther`: `0x0002`；文件可以被其他人写入。
- `QFileDevice::ExeOther`: `0x0001`；文件可以被其他人执行。
警告：由于 Qt 支持的平台存在差异，ReadUser、WriteUser 和 ExeUser 的语义依赖于平台：在 Unix 上返回文件所有者的权限，在 Windows 上返回当前用户的权限。此行为可能在未来的 Qt 版本中发生变化。

注意：在 NTFS 文件系统上，默认出于性能考虑禁用所有权和权限检查。要启用它，包含以下行：

extern Q_CORE_EXPORT int qt_ntfs_permission_lookup;
之后，通过增加或减少 `qt_ntfs_permission_lookup` 的值 1 来打开或关闭权限检查。
注意：由于这是一个非原子全局变量，仅在主线程启动前或其他线程全部结束后，安全地增加或减少 `qt_ntfs_permission_lookup`。
注意：从 Qt 6.6 起，变量 `qt_ntfs_permission_lookup` 已弃用。请使用以下替代方案。
管理权限检查的安全简便方法是使用 RAII 类 `QNtfsPermissionCheckGuard`。
如果需要更细粒度的控制，可以使用以下函数管理权限：
Permissions 类型是 Permission 的 QFlags<Permission> 类型定义。它存储 Permission 值的 OR 组合。

**官方示例：**

```cpp
 qt_ntfs_permission_lookup++; // turn checking on
 qt_ntfs_permission_lookup--; // turn it off again
```

### `[virtual noexcept] QFileDevice::~QFileDevice()`

**作用与语义：**

销毁文件设备，必要时关闭。

### `[override virtual] bool QFileDevice::atEnd() const`

**作用与语义：**

重装：`QIODevice::atEnd()` const.
如果到达文件末尾，返回`true`;否则返回false。
对于Unix上的普通空文件（例如`/proc`中的文件），该函数返回`true`，因为文件系统报告该文件大小为0。因此，读取此类文件数据时不应依赖atEnd()，而是调用`read()`直到无法读取更多数据。
如果当前读写位置位于设备末端（即设备上没有更多可读取的数据），返回`true`;否则返回`false`。
对于某些设备，即使有更多数据可读取，atEnd() 仍可返回 true。此特殊情况仅适用于直接响应你调用 `read()` 生成数据的设备（例如，Unix 和 macOS 上的 `/dev` 或 `/proc` 文件，或所有平台的控制台输入/`stdin`）。

### `[override virtual] void QFileDevice::close()`

**作用与语义：**

重装：`QIODevice::close()`。
调用`QFileDevice::flush()`并关闭文件。冲洗错误被忽略。
先发出`aboutToClose()`，然后关闭设备并将其OpenMode设置为NotOpen。错误字符串也会被重置。

### `QFileDevice::FileError QFileDevice::error() const`

**作用与语义：**

返回文件错误状态。
I/O 设备状态返回错误代码。例如，如果 `open()`返回 `false`，或读写操作返回 -1，可以调用该函数来查找操作失败的原因。

### `[virtual] QString QFileDevice::fileName() const`

**作用与语义：**

返回文件名称。`QFileDevice` 的默认实现返回空字符串。

### `QDateTime QFileDevice::fileTime(QFileDevice::FileTime time) const`

**作用与语义：**

返回`time`指定的文件时间。如果无法确定时间，返回QDateTime()（一个无效的日期时间）。

### `bool QFileDevice::flush()`

**作用与语义：**

将缓冲数据冲入文件。成功时返回`true`;否则返回`false`。

### `int QFileDevice::handle() const`

**作用与语义：**

返回文件的地址。
这是一个小的正整数，适合用于 C 库函数，如 `fdopen()` 和 `fcntl()`。在使用文件描述符表示套接字的系统（如 Unix 系统，但不包括 Windows），该句柄也可以与 `QSocketNotifier` 一起使用。
如果文件未打开或存在错误，handle() 返回 -1。

### `[override virtual] bool QFileDevice::isSequential() const`

**作用与语义：**

重装：`QIODevice::isSequential()` const.
如果文件只能顺序操作，返回`true`;否则返回`false`。
大多数文件支持随机访问，但有些特殊文件可能不支持。
如果该装置是顺序的，返回`true`;否则返回假。
顺序设备与随机访问设备不同，没有起始、结束、大小或当前位置的概念，也不支持寻道。只有当设备报告数据可用时，你才能读取数据。最常见的顺序设备例子是网络套接字。在Unix上，特殊文件如/dev/zero和fifo管道是顺序文件。
而普通文件则支持随机访问。它们既有大小也有当前位置，还支持在数据流中向后和向前寻求。普通文件则是非顺序的。

### `uchar *QFileDevice::map(qint64 offset, qint64 size, QFileDevice::MemoryMapFlags flags = NoOptions)`

**作用与语义：**

从`offset`开始将文件的字节映射到内存中`size`。文件应当是打开的，映射成功，但文件在映射内存完成后不必保持开放。当`QFile`被销毁或用该对象打开新文件时，任何未解映射的映射都会自动被取消映射。
映射的开启模式与文件相同（读和/或写），除非使用`MapPrivateOption`，此时总可以写入映射存储器。
任何映射选项都可以通过`flags`传递。
如果出现错误，返回指向内存或`nullptr`的指针。

### `[virtual] QFileDevice::Permissions QFileDevice::permissions() const`

**作用与语义：**

返回文件中 QFile：:P ermission 的完整 OR ed 组合。

### `[override virtual] qint64 QFileDevice::pos() const`

**作用与语义：**

重装：`QIODevice::pos()` const.
对于随机访问设备，该函数返回数据写入或读取的位置。对于顺序设备或封闭设备，若不存在“当前位置”概念，则返回0。
设备的当前读写位置由`QIODevice`内部维护，因此无需重新实现此功能。在子类化`QIODevice`时，使用`QIODevice::seek()`通知`QIODevice`设备位置的变化。

### `[override virtual protected] qint64 QFileDevice::readData(char *data, qint64 len)`

**作用与语义：**

Reimplements： `QIODevice::readData`（char *data， qint64 maxSize）.
从设备读取最多`maxSize`字节到`data`，返回读取字节数，或如果发生错误则返回-1字节。
如果没有字节可读且永远无法再有更多字节（例如套接字闭合、管道闭合、子进程已完成），该函数返回 -1。
该函数由`QIODevice`调用。创建`QIODevice`子类时重新实现该函数。
在重新实现该函数时，重要的是该函数在返回前读取所有所需数据。这是 `QDataStream` 能够操作该类的必要条件。`QDataStream` 假设所有请求的信息都已读取，因此如果存在问题，不会重新尝试读取。
该函数可调用 maxSize 为 0，可用于执行读取后操作。

### `[override virtual protected] qint64 QFileDevice::readLineData(char *data, qint64 maxlen)`

**作用与语义：**

Reimplements： `QIODevice::readLineData`（char *data， qint64 maxSize）.
读取最多`maxSize`字符`data`并返回已读字符数。
该函数由`readLine()`调用，并通过`getChar()`提供其基础实现。缓冲设备通过重新实现该函数可以提升`readLine()`的性能。
`readLine()` 会在 `data` 上附加一个 '\0' 字节;readLineData() 不需要这样做。
如果重新实现该函数，请注意返回正确的值：应返回该行读取的字节数，包括终止的换行，或者如果此时没有可读的行，则返回0。如果发生错误，应返回-1，当且仅当没有读取字节。超过EOF的读取被视为错误。

### `[virtual] bool QFileDevice::resize(qint64 sz)`

**作用与语义：**

设置文件大小（字节为单位）`sz`。如果调整大小成功，返回 `true`;否则为假。如果 `sz` 比当前文件大，则新字节设为 0;如果 `sz` 较小，文件被简单截断。
警告：如果文件不存在，该功能可能会失败。

### `[override virtual] bool QFileDevice::seek(qint64 pos)`

**作用与语义：**

重制版本：`QIODevice::seek`（qint64 pos）。
对于随机访问设备，该函数将当前位置设置为`pos`，成功时返回true，发生错误时返回false。对于顺序设备，默认行为是不做并返回false。
在文件末尾之外寻找：如果位置在文件末尾之外，则 seek() 不会立即扩展文件。如果在该位置写入，文件将被扩展。文件从前一端到新写入数据之间的内容为 UNDEFINED 的，且因平台和文件系统而异。
对于随机访问设备，该函数将当前位置设置为`pos`，成功时返回true，发生错误时返回false。对于顺序设备，默认行为是发送警告并返回false。
在子类`QIODevice`时，你必须在函数开头调用 QIODevice：：seek()，以确保与 `QIODevice` 内置缓冲区的完整性。

### `bool QFileDevice::setFileTime(const QDateTime &newDate, QFileDevice::FileTime fileTime)`

**作用与语义：**

将`fileTime`指定的文件时间设置为`newDate`，成功时返回true;否则返回false。
注意：文件必须是打开的，才能使用此功能。

### `[virtual] bool QFileDevice::setPermissions(QFileDevice::Permissions permissions)`

**作用与语义：**

将文件权限设置为指定的`permissions`。如果成功，返回`true`;如果权限无法修改，则返回`false`。
警告：该功能不操控前交叉韧带，这可能会限制其效果。

### `[override virtual] qint64 QFileDevice::size() const`

**作用与语义：**

重装：`QIODevice::size()` const.
返回文件大小。
对于Unix上的普通空文件（例如`/proc`中的文件），该函数返回0;此类文件的内容会根据调用`read()`按需生成。
对于开放随机访问设备，该函数返回设备的大小。对于开放顺序设备，返回`bytesAvailable()`。
如果设备关闭，返回的尺寸不会反映设备的实际大小。

### `bool QFileDevice::unmap(uchar *address)`

**作用与语义：**

解除内存`address`映射。
如果解映射成功，返回`true`;否则为假。

### `void QFileDevice::unsetError()`

**作用与语义：**

将文件错误设置为`QFileDevice::NoError`。

### `[override virtual protected] qint64 QFileDevice::writeData(const char *data, qint64 len)`

**作用与语义：**

Reimplements： `QIODevice::writeData`（const char *data， qint64 maxSize）.
从`data`写入最多`maxSize`字节到设备。返回写入字节数，或如果发生错误则返回-1字节。
该函数由`QIODevice`调用。创建`QIODevice`子类时重新实现该函数。
在重新实现该函数时，重要的是该函数在返回前写入所有可用数据。这是`QDataStream`能够操作该类所必需的。`QDataStream`假设所有信息都已写入，因此如果出现问题，不会重试写入。

### `[since 6.8] QT_NO_USE_NODISCARD_FILE_OPEN`

**作用与语义：**

与文件相关的I/O类（如`QFile`、`QSaveFile`、`QTemporaryFile`）有一种`open()`方法来打开它们所操作的文件。在继续读写数据到文件之前，务必检查调用`open()`的返回值。
因此，从 Qt 6.8 开始，部分 `open()` 的超载被标记为 `[[nodiscard]]` 属性。由于此变更可能在现有代码库中引发警告，用户代码可以通过定义某些宏来选择加入或退出该属性：
- 如果定义了`QT_USE_NODISCARD_FILE_OPEN`宏，`open()`的重载标记为`[[nodiscard]]`。
- 如果`QT_NO_USE_NODISCARD_FILE_OPEN`定义，`open()`的重载不会标记为`[[nodiscard]]`。
- 如果两个宏都未定义，则默认在包括Qt 6.9之前不包含该属性。从Qt 6.10开始，该属性会自动应用。
- 如果两个宏都被定义，程序是错误形式的。
这些宏在Qt 6.8引入。

### `enum FileHandleFlag { AutoCloseHandle, DontCloseHandle }`

**作用与语义：**

该枚举用于打开文件时指定仅适用于文件而非泛`QIODevice`的额外选项。
- `QFileDevice::AutoCloseHandle`：`0x0001`;传递给`open()`的文件句柄应由`close()`关闭，默认行为是关闭文件，应用程序负责关闭文件句柄。当按名称打开文件时，该标志被忽略，因为 Qt 始终拥有文件柄并必须关闭它。
- `QFileDevice::DontCloseHandle`：`0`;如果没有显式关闭，`QFile`对象被销毁时，底层文件句柄会保持开放。
FileHandleFlags 类型是 QFlags 的 typedef<FileHandleFlag>。它存储 FileHandleFlag 值的 OR 组合。

### `flags FileHandleFlags`

**作用与语义：**

该枚举用于打开文件时指定仅适用于文件而非泛`QIODevice`的额外选项。
- `QFileDevice::AutoCloseHandle`：`0x0001`;传递给`open()`的文件句柄应由`close()`关闭，默认行为是关闭文件，应用程序负责关闭文件句柄。当按名称打开文件时，该标志被忽略，因为 Qt 始终拥有文件柄并必须关闭它。
- `QFileDevice::DontCloseHandle`：`0`;如果没有显式关闭，`QFile`对象被销毁时，底层文件句柄会保持开放。
FileHandleFlags 类型是 QFlags 的 typedef<FileHandleFlag>。它存储 FileHandleFlag 值的 OR 组合。

### `enum MemoryMapFlag { NoOptions, MapPrivateOption }`

**作用与语义：**

该枚举描述了`map()`函数可能使用的特殊选项。
- `QFileDevice::NoOptions`：`0`;无选项。
- `QFileDevice::MapPrivateOption`：`0x0001`;映射后的内存将是私有的，因此任何修改对其他进程都不可见，也不会写入磁盘。当内存被取消映射时，任何此类修改都会丢失。目前尚不确定映射创建后对文件所做的修改是否会通过映射存储器可见。该枚举值是在Qt 5.4中引入的。
MemoryMapFlags 类型是 QFlags 的 typedef<MemoryMapFlag>。它存储 MemoryMapFlag 值的 OR 组合。

### `flags MemoryMapFlags`

**作用与语义：**

该枚举描述了`map()`函数可能使用的特殊选项。
- `QFileDevice::NoOptions`：`0`;无选项。
- `QFileDevice::MapPrivateOption`：`0x0001`;映射后的内存将是私有的，因此任何修改对其他进程都不可见，也不会写入磁盘。当内存被取消映射时，任何此类修改都会丢失。目前尚不确定映射创建后对文件所做的修改是否会通过映射存储器可见。该枚举值是在Qt 5.4中引入的。
MemoryMapFlags 类型是 QFlags 的 typedef<MemoryMapFlag>。它存储 MemoryMapFlag 值的 OR 组合。

### `enum Permission { ReadOwner, WriteOwner, ExeOwner, ReadUser, WriteUser, …, ExeOther }`

**作用与语义：**

此枚举由 permission() 函数使用，用于报告文件的权限和所有权。可将值进行 OR 运算以测试多个权限和所有权值。
- `QFileDevice::ReadOwner`: `0x4000`；文件可以被文件所有者读取。
- `QFileDevice::WriteOwner`: `0x2000`；文件可以被文件所有者写入。
- `QFileDevice::ExeOwner`: `0x1000`；文件可以被文件所有者执行。
- `QFileDevice::ReadUser`: `0x0400`；文件可以被用户读取。
- `QFileDevice::WriteUser`: `0x0200`；文件可以被用户写入。
- `QFileDevice::ExeUser`: `0x0100`；文件可以被用户执行。
- `QFileDevice::ReadGroup`: `0x0040`；文件可以被组读取。
- `QFileDevice::WriteGroup`: `0x0020`；文件可以被组写入。
- `QFileDevice::ExeGroup`: `0x0010`；文件可以被组执行。
- `QFileDevice::ReadOther`: `0x0004`；文件可以被其他人读取。
- `QFileDevice::WriteOther`: `0x0002`；文件可以被其他人写入。
- `QFileDevice::ExeOther`: `0x0001`；文件可以被其他人执行。
警告：由于 Qt 支持的平台存在差异，ReadUser、WriteUser 和 ExeUser 的语义依赖于平台：在 Unix 上返回文件所有者的权限，在 Windows 上返回当前用户的权限。此行为可能在未来的 Qt 版本中发生变化。

注意：在 NTFS 文件系统上，默认出于性能考虑禁用所有权和权限检查。要启用它，包含以下行：

extern Q_CORE_EXPORT int qt_ntfs_permission_lookup;
之后，通过增加或减少 `qt_ntfs_permission_lookup` 的值 1 来打开或关闭权限检查。
注意：由于这是一个非原子全局变量，仅在主线程启动前或其他线程全部结束后，安全地增加或减少 `qt_ntfs_permission_lookup`。
注意：从 Qt 6.6 起，变量 `qt_ntfs_permission_lookup` 已弃用。请使用以下替代方案。
管理权限检查的安全简便方法是使用 RAII 类 `QNtfsPermissionCheckGuard`。
如果需要更细粒度的控制，可以使用以下函数管理权限：
Permissions 类型是 Permission 的 QFlags<Permission> 类型定义。它存储 Permission 值的 OR 组合。

**官方示例：**

```cpp
 qt_ntfs_permission_lookup++; // turn checking on
 qt_ntfs_permission_lookup--; // turn it off again
```

### `flags Permissions`

**作用与语义：**

此枚举由 permission() 函数使用，用于报告文件的权限和所有权。可将值进行 OR 运算以测试多个权限和所有权值。
- `QFileDevice::ReadOwner`: `0x4000`；文件可以被文件所有者读取。
- `QFileDevice::WriteOwner`: `0x2000`；文件可以被文件所有者写入。
- `QFileDevice::ExeOwner`: `0x1000`；文件可以被文件所有者执行。
- `QFileDevice::ReadUser`: `0x0400`；文件可以被用户读取。
- `QFileDevice::WriteUser`: `0x0200`；文件可以被用户写入。
- `QFileDevice::ExeUser`: `0x0100`；文件可以被用户执行。
- `QFileDevice::ReadGroup`: `0x0040`；文件可以被组读取。
- `QFileDevice::WriteGroup`: `0x0020`；文件可以被组写入。
- `QFileDevice::ExeGroup`: `0x0010`；文件可以被组执行。
- `QFileDevice::ReadOther`: `0x0004`；文件可以被其他人读取。
- `QFileDevice::WriteOther`: `0x0002`；文件可以被其他人写入。
- `QFileDevice::ExeOther`: `0x0001`；文件可以被其他人执行。
警告：由于 Qt 支持的平台存在差异，ReadUser、WriteUser 和 ExeUser 的语义依赖于平台：在 Unix 上返回文件所有者的权限，在 Windows 上返回当前用户的权限。此行为可能在未来的 Qt 版本中发生变化。

注意：在 NTFS 文件系统上，默认出于性能考虑禁用所有权和权限检查。要启用它，包含以下行：

extern Q_CORE_EXPORT int qt_ntfs_permission_lookup;
之后，通过增加或减少 `qt_ntfs_permission_lookup` 的值 1 来打开或关闭权限检查。
注意：由于这是一个非原子全局变量，仅在主线程启动前或其他线程全部结束后，安全地增加或减少 `qt_ntfs_permission_lookup`。
注意：从 Qt 6.6 起，变量 `qt_ntfs_permission_lookup` 已弃用。请使用以下替代方案。
管理权限检查的安全简便方法是使用 RAII 类 `QNtfsPermissionCheckGuard`。
如果需要更细粒度的控制，可以使用以下函数管理权限：
Permissions 类型是 Permission 的 QFlags<Permission> 类型定义。它存储 Permission 值的 OR 组合。

**官方示例：**

```cpp
 qt_ntfs_permission_lookup++; // turn checking on
 qt_ntfs_permission_lookup--; // turn it off again
```

### `(since 6.8) QT_USE_NODISCARD_FILE_OPEN`

**作用与语义：**

与文件相关的I/O类（如`QFile`、`QSaveFile`、`QTemporaryFile`）有一种`open()`方法来打开它们所操作的文件。在继续读写数据到文件之前，务必检查调用`open()`的返回值。
因此，从 Qt 6.8 开始，部分 `open()` 的超载被标记为 `[[nodiscard]]` 属性。由于此变更可能在现有代码库中引发警告，用户代码可以通过定义某些宏来选择加入或退出该属性：
- 如果定义了`QT_USE_NODISCARD_FILE_OPEN`宏，`open()`的重载标记为`[[nodiscard]]`。
- 如果`QT_NO_USE_NODISCARD_FILE_OPEN`定义，`open()`的重载不会标记为`[[nodiscard]]`。
- 如果两个宏都未定义，则默认在包括Qt 6.9之前不包含该属性。从Qt 6.10开始，该属性会自动应用。
- 如果两个宏都被定义，程序是错误形式的。
这些宏在Qt 6.8引入。

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

`QFileDevice` 所属机制类型：文件、设备与流机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
