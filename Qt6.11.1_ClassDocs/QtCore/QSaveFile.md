# QSaveFile

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 安全写文件设备，负责先写临时文件再原子替换目标文件，避免半写入配置。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QSaveFile`：安全写文件设备，负责先写临时文件再原子替换目标文件，避免半写入配置。

**内部模型：** 文件和 I/O 类型把路径/设备描述与打开后的读写状态分开。打开模式决定可执行的操作，当前位置、缓冲区、文本编码、权限和错误状态共同决定一次读写是否正确。

**适用场景：** 构造稳定路径，选择正确的 OpenMode，检查 open 和 errorString，按数据规模使用流式读写或分块处理，明确文本编码，完成后关闭并处理失败。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要手写平台分隔符；不要默认相对路径指向程序目录；不要把本地编码、UTF-8 和二进制混在一起；写文件时要考虑临时文件、覆盖、权限和原子替换。

## 2. 依赖与对象关系

- 头文件：`#include <QSaveFile>`
- 继承自：QFileDevice
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

### 公有函数

- `QSaveFile(QObject *parent = nullptr)`
- `QSaveFile(const QString &name, QObject *parent = nullptr)`
- `(since 6.11) QSaveFile(const std::filesystem::path &path, QObject *parent = nullptr)`
- `virtual ~QSaveFile()`
- `void cancelWriting()`
- `bool commit()`
- `bool directWriteFallback() const`
- `(since 6.11) std::filesystem::path filesystemFileName() const`
- `void setDirectWriteFallback(bool enabled)`
- `void setFileName(const QString &name)`
- `(since 6.11) void setFileName(const std::filesystem::path &name)`

### 重实现的公有函数

- `virtual QString fileName() const override`
- `virtual bool open(QIODeviceBase::OpenMode mode) override`

### 重实现的保护函数

- `virtual qint64 writeData(const char *data, qint64 len) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[explicit] QSaveFile::QSaveFile(QObject *parent = nullptr)`

**作用与语义：**

用给定的 `parent` 构建一个新的文件对象。你需要在`open()`之前调用 `setFileName()`。

### `[explicit] QSaveFile::QSaveFile(const QString &name, QObject *parent = nullptr)`

**作用与语义：**

构造一个带有指定`parent`的新文件对象，以表示指定`name`的文件。

### `[since 6.11] QSaveFile::QSaveFile(const std::filesystem::path &path, QObject *parent = nullptr)`

**作用与语义：**

构造一个带有指定`parent`的新文件对象，以表示指定`path`的文件。

### `[virtual noexcept] QSaveFile::~QSaveFile()`

**作用与语义：**

销毁文件对象，除非调用`commit()`，否则丢弃保存的内容。

### `void QSaveFile::cancelWriting()`

**作用与语义：**

取消写入新文件。
如果应用程序在保存时改变主意，可以调用cancelWriting()，该错误代码会`commit()`丢弃临时文件。
或者，它也可以确保不打电话给`commit()`。
调用该方法后可以进行进一步写入操作，但都无效，写入文件会被丢弃。
当使用直接写入后退时，这种方法没有效果。这种情况适用于只读目录中对现有文件进行保存：无法创建临时文件，因此无论如何，现有文件都会被覆盖，而 cancelWriting() 无法处理此问题，文件内容将丢失。

### `bool QSaveFile::commit()`

**作用与语义：**

如果之前所有写入都成功，则将更改提交到磁盘。
必须在保存操作结束时调用此功能，否则文件将被丢弃。
如果写入过程中出现错误，删除临时文件并返回`false`。否则，将其重命名为最终的`fileName`，成功后返回`true`。最后，关闭设备。

### `bool QSaveFile::directWriteFallback() const`

**作用与语义：**

如果启用了只读目录中保存文件的备用方案，返回`true`。

### `[override virtual] QString QSaveFile::fileName() const`

**作用与语义：**

重装：`QFileDevice::fileName()` const.
返回由`setFileName()`或`QSaveFile`构造器设置的名称。
返回文件名称。`QFileDevice` 的默认实现返回空字符串。

### `[since 6.11] std::filesystem::path QSaveFile::filesystemFileName() const`

**作用与语义：**

回归`fileName()`为`std::filesystem::path`。

### `[override virtual] bool QSaveFile::open(QIODeviceBase::OpenMode mode)`

**作用与语义：**

重实现自：`QIODevice::open`（QIODeviceBase：：OpenMode 模式）。
使用`mode`标志打开文件。成功时返回`true`;否则返回`false`。
重要提示：`mode`的标志必须包含`QIODeviceBase::WriteOnly`。其他常见的标志还有 `Text` 和 `Unbuffered`。目前不支持的标志有 `ReadOnly`（因此是 `ReadWrite`）、`Append`、`NewOnly` 和 `ExistingOnly`;它们会生成运行时警告。
打开设备并将其 OpenMode 设置为 `mode`。成功时返回 `true`;否则返回 `false`。该函数应从任何重新实现的 open() 或其他打开设备的函数中调用。

### `void QSaveFile::setDirectWriteFallback(bool enabled)`

**作用与语义：**

必要时允许对现有文件进行写入。
`QSaveFile` 在与最终文件相同的目录中创建一个临时文件，并对其进行原子重命名。但如果目录权限不允许创建新文件，这是不可能的。为了保持原子性保证，`open()` 在无法创建临时文件时失败。
为了允许用户在权限受限的目录中编辑带有写权限的文件，调用 setDirectWriteFallback() 并将 `enabled` 设为 true，随后对 `open()` 的调用将退回到直接打开现有文件并写入，无需使用临时文件。这没有原子性保证，例如应用程序崩溃或例如断电可能导致磁盘上文件部分写入。这也意味着在这种情况下`cancelWriting()`没有影响。
通常，要保存用户编辑的文档，调用 setDirectWriteFallback（true），保存应用内部文件（配置文件、数据文件等），则保持确保原子性的默认设置。

### `void QSaveFile::setFileName(const QString &name)`

**作用与语义：**

设置文件的 `name`。名称可以是无路径、相对路径或绝对路径。

### `[since 6.11] void QSaveFile::setFileName(const std::filesystem::path &name)`

**作用与语义：**

设置文件的 `name`。名称可以是无路径、相对路径或绝对路径。

### `[override virtual protected] qint64 QSaveFile::writeData(const char *data, qint64 len)`

**作用与语义：**

把 `data` 中最多 `len` 字节写入 `QSaveFile` 的临时文件，返回实际接收的字节数，失败返回 -1。它由 `QIODevice::write()` 间接调用，不应直接调用；只有最后 `commit()` 成功后，目标文件才会被原子替换。

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

`QSaveFile` 所属机制类型：文件、设备与流机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
