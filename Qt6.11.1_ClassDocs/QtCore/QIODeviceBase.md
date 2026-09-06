# QIODeviceBase

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QIODeviceBase` 是 文件、设备与流机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QIODeviceBase` 是 文件、设备与流机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 文件和 I/O 类型把路径/设备描述与打开后的读写状态分开。打开模式决定可执行的操作，当前位置、缓冲区、文本编码、权限和错误状态共同决定一次读写是否正确。

**适用场景：** 构造稳定路径，选择正确的 OpenMode，检查 open 和 errorString，按数据规模使用流式读写或分块处理，明确文本编码，完成后关闭并处理失败。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要手写平台分隔符；不要默认相对路径指向程序目录；不要把本地编码、UTF-8 和二进制混在一起；写文件时要考虑临时文件、覆盖、权限和原子替换。

## 2. 依赖与对象关系

- 头文件：`#include <QIODevice>`
- 继承自：未在类页中列出
- 直接派生类：QDataStream、QDebug、QIODevice,、QTextStream

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

- `flags OpenMode`
- `enum OpenModeFlag { NotOpen, ReadOnly, WriteOnly, ReadWrite, Append, …, ExistingOnly }`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QIODeviceBase::OpenModeFlagflags QIODeviceBase::OpenMode`

**作用与语义：**

该枚举与`QIODevice::open()`一起使用，描述设备打开的模式。它也会被`QIODevice::openMode()`返回。
- `QIODeviceBase::NotOpen`：`0x0000`;设备未打开。
- `QIODeviceBase::ReadOnly`：`0x0001`;设备已开放读取。
- `QIODeviceBase::WriteOnly`：`0x0002`;设备可写入。注意，对于文件系统子类（如`QFile`），此模式意味着截断，除非与只读、附加或仅新操作结合。
- `QIODeviceBase::ReadWrite`：`ReadOnly | WriteOnly`;该设备可开放用于阅读和写入。
- `QIODeviceBase::Append`：`0x0004`;设备以附加模式打开，使所有数据写入文件末尾。
- `QIODeviceBase::Truncate`：`0x0008`;如果可能，设备在打开前被截断。设备中所有早期内容均丢失。
- `QIODeviceBase::Text`：`0x0010`;读取时，行尾终止符被翻译为“\n”。写入时，行尾终止符被翻译为本地编码，例如Win32的“\r\n”。
- `QIODeviceBase::Unbuffered`：`0x0020`;设备中的任何缓冲区都会被绕过。
- `QIODeviceBase::NewOnly`：`0x0040`;如果要打开的文件已经存在，则失败。只有在文件不存在时才创建并打开该文件。操作系统保证只有你自己创建和打开该文件。注意，此模式意味着仅写，允许将其与读写结合。该标志目前只影响`QFile`。未来其他类可能会使用该标志，但在那之前，除`QFile`类外使用该标志可能导致行为未定义。（自Qt 5.11起）
- `QIODeviceBase::ExistingOnly`：`0x0080`;如果要打开的文件不存在，则失败。该标志必须与 ReadOnly、WriteOnly 或 ReadWrite 一起指定。注意，单独使用该标志是多余的，因为当文件不存在时，ReadOnly 已经失败了。该标志目前只影响 `QFile`。未来其他类可能会使用该标志，但在那之前，除了 `QFile` 之外的类使用该标志可能会导致行为未定义。（自 Qt 5.11 起）
某些标志，如`Unbuffered`和`Truncate`，在某些子类中使用时是无意义的。其中一些限制是由子类所代表的设备类型所隐含的。在其他情况下，限制可能源于实现方式，也可能由底层平台施加;例如，`QTcpSocket`不支持`Unbuffered`模式，且原生API的限制阻止`QFile`在Windows上支持`Unbuffered`。
OpenMode 类型是 QFlags 的 typedef<OpenModeFlag>。它存储 OpenModeFlag 值的 OR 组合。

### `flags OpenMode`

**作用与语义：**

该枚举与`QIODevice::open()`一起使用，描述设备打开的模式。它也会被`QIODevice::openMode()`返回。
- `QIODeviceBase::NotOpen`：`0x0000`;设备未打开。
- `QIODeviceBase::ReadOnly`：`0x0001`;设备已开放读取。
- `QIODeviceBase::WriteOnly`：`0x0002`;设备可写入。注意，对于文件系统子类（如`QFile`），此模式意味着截断，除非与只读、附加或仅新操作结合。
- `QIODeviceBase::ReadWrite`：`ReadOnly | WriteOnly`;该设备可开放用于阅读和写入。
- `QIODeviceBase::Append`：`0x0004`;设备以附加模式打开，使所有数据写入文件末尾。
- `QIODeviceBase::Truncate`：`0x0008`;如果可能，设备在打开前被截断。设备中所有早期内容均丢失。
- `QIODeviceBase::Text`：`0x0010`;读取时，行尾终止符被翻译为“\n”。写入时，行尾终止符被翻译为本地编码，例如Win32的“\r\n”。
- `QIODeviceBase::Unbuffered`：`0x0020`;设备中的任何缓冲区都会被绕过。
- `QIODeviceBase::NewOnly`：`0x0040`;如果要打开的文件已经存在，则失败。只有在文件不存在时才创建并打开该文件。操作系统保证只有你自己创建和打开该文件。注意，此模式意味着仅写，允许将其与读写结合。该标志目前只影响`QFile`。未来其他类可能会使用该标志，但在那之前，除`QFile`类外使用该标志可能导致行为未定义。（自Qt 5.11起）
- `QIODeviceBase::ExistingOnly`：`0x0080`;如果要打开的文件不存在，则失败。该标志必须与 ReadOnly、WriteOnly 或 ReadWrite 一起指定。注意，单独使用该标志是多余的，因为当文件不存在时，ReadOnly 已经失败了。该标志目前只影响 `QFile`。未来其他类可能会使用该标志，但在那之前，除了 `QFile` 之外的类使用该标志可能会导致行为未定义。（自 Qt 5.11 起）
某些标志，如`Unbuffered`和`Truncate`，在某些子类中使用时是无意义的。其中一些限制是由子类所代表的设备类型所隐含的。在其他情况下，限制可能源于实现方式，也可能由底层平台施加;例如，`QTcpSocket`不支持`Unbuffered`模式，且原生API的限制阻止`QFile`在Windows上支持`Unbuffered`。
OpenMode 类型是 QFlags 的 typedef<OpenModeFlag>。它存储 OpenModeFlag 值的 OR 组合。

### `enum OpenModeFlag { NotOpen, ReadOnly, WriteOnly, ReadWrite, Append, …, ExistingOnly }`

**作用与语义：**

该枚举与`QIODevice::open()`一起使用，描述设备打开的模式。它也会被`QIODevice::openMode()`返回。
- `QIODeviceBase::NotOpen`：`0x0000`;设备未打开。
- `QIODeviceBase::ReadOnly`：`0x0001`;设备已开放读取。
- `QIODeviceBase::WriteOnly`：`0x0002`;设备可写入。注意，对于文件系统子类（如`QFile`），此模式意味着截断，除非与只读、附加或仅新操作结合。
- `QIODeviceBase::ReadWrite`：`ReadOnly | WriteOnly`;该设备可开放用于阅读和写入。
- `QIODeviceBase::Append`：`0x0004`;设备以附加模式打开，使所有数据写入文件末尾。
- `QIODeviceBase::Truncate`：`0x0008`;如果可能，设备在打开前被截断。设备中所有早期内容均丢失。
- `QIODeviceBase::Text`：`0x0010`;读取时，行尾终止符被翻译为“\n”。写入时，行尾终止符被翻译为本地编码，例如Win32的“\r\n”。
- `QIODeviceBase::Unbuffered`：`0x0020`;设备中的任何缓冲区都会被绕过。
- `QIODeviceBase::NewOnly`：`0x0040`;如果要打开的文件已经存在，则失败。只有在文件不存在时才创建并打开该文件。操作系统保证只有你自己创建和打开该文件。注意，此模式意味着仅写，允许将其与读写结合。该标志目前只影响`QFile`。未来其他类可能会使用该标志，但在那之前，除`QFile`类外使用该标志可能导致行为未定义。（自Qt 5.11起）
- `QIODeviceBase::ExistingOnly`：`0x0080`;如果要打开的文件不存在，则失败。该标志必须与 ReadOnly、WriteOnly 或 ReadWrite 一起指定。注意，单独使用该标志是多余的，因为当文件不存在时，ReadOnly 已经失败了。该标志目前只影响 `QFile`。未来其他类可能会使用该标志，但在那之前，除了 `QFile` 之外的类使用该标志可能会导致行为未定义。（自 Qt 5.11 起）
某些标志，如`Unbuffered`和`Truncate`，在某些子类中使用时是无意义的。其中一些限制是由子类所代表的设备类型所隐含的。在其他情况下，限制可能源于实现方式，也可能由底层平台施加;例如，`QTcpSocket`不支持`Unbuffered`模式，且原生API的限制阻止`QFile`在Windows上支持`Unbuffered`。
OpenMode 类型是 QFlags 的 typedef<OpenModeFlag>。它存储 OpenModeFlag 值的 OR 组合。

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

`QIODeviceBase` 所属机制类型：文件、设备与流机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
