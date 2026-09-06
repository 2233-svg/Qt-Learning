# QFileSystemWatcher

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 文件系统变化监视器，负责通过信号通知文件或目录被修改、删除或重命名。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QFileSystemWatcher`：文件系统变化监视器，负责通过信号通知文件或目录被修改、删除或重命名。

**内部模型：** 文件和 I/O 类型把路径/设备描述与打开后的读写状态分开。打开模式决定可执行的操作，当前位置、缓冲区、文本编码、权限和错误状态共同决定一次读写是否正确。

**适用场景：** 构造稳定路径，选择正确的 OpenMode，检查 open 和 errorString，按数据规模使用流式读写或分块处理，明确文本编码，完成后关闭并处理失败。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要手写平台分隔符；不要默认相对路径指向程序目录；不要把本地编码、UTF-8 和二进制混在一起；写文件时要考虑临时文件、覆盖、权限和原子替换。

## 2. 依赖与对象关系

- 头文件：`#include <QFileSystemWatcher>`
- 继承自：QObject
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

- `QFileSystemWatcher(QObject *parent = nullptr)`
- `QFileSystemWatcher(const QStringList &paths, QObject *parent = nullptr)`
- `virtual ~QFileSystemWatcher()`
- `bool addPath(const QString &path)`
- `QStringList addPaths(const QStringList &paths)`
- `QStringList directories() const`
- `QStringList files() const`
- `bool removePath(const QString &path)`
- `QStringList removePaths(const QStringList &paths)`

### 信号

- `void directoryChanged(const QString &path)`
- `void fileChanged(const QString &path)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QFileSystemWatcher::QFileSystemWatcher(QObject *parent = nullptr)`

**作用与语义：**

构建一个带有给定`parent`的新文件系统监视对象。

### `QFileSystemWatcher::QFileSystemWatcher(const QStringList &paths, QObject *parent = nullptr)`

**作用与语义：**

构建一个带有指定`parent`的新文件系统监视对象，用于监控指定的`paths`列表。

### `[virtual noexcept] QFileSystemWatcher::~QFileSystemWatcher()`

**作用与语义：**

会摧毁文件系统监视器。

### `bool QFileSystemWatcher::addPath(const QString &path)`

**作用与语义：**

如果存在`path`，则向文件系统监视者添加`path`。如果路径不存在，或者已经被文件系统监视器监控，则不添加该路径。
如果`path`指定了目录，`directoryChanged()`信号将在`path`被修改或移除磁盘时发出;否则，`fileChanged()`信号在修改、重命名或移除时`path`会发出。
如果手表成功，则返回真值。
手表故障的原因通常取决于系统，但可能包括资源不存在、访问失败，或如果平台有总手表数量限制。
注意：同时监控的文件和目录数量可能有系统限制。如果达到该限制，`path`将不被监控，错误结果返回。

### `QStringList QFileSystemWatcher::addPaths(const QStringList &paths)`

**作用与语义：**

将每个路径添加到文件系统监视器`paths`。如果路径不存在，或者已经被文件系统监视器监控，则不会添加。
如果路径指定了目录，当路径被修改或从磁盘中移除时，`directoryChanged()`信号会被发射;否则，当路径被修改、重命名或移除时，`fileChanged()`信号会被发出。
返回值是无法被监控的路径列表。
手表故障的原因通常取决于系统，但可能包括资源不存在、访问失败，或如果平台有总手表数量限制。
注意：同时监控的文件和目录数量可能有系统限制。如果超过该限制，多余的`paths`将不被监控，它们会被添加到返回的`QStringList`中。

### `QStringList QFileSystemWatcher::directories() const`

**作用与语义：**

返回正在监控的目录路径列表。

### `[private signal] void QFileSystemWatcher::directoryChanged(const QString &path)`

**作用与语义：**

当指定`path`目录被修改（例如文件被添加或删除）或从磁盘中移除时，会发出该信号。注意，如果在短时间内发生多次变更，部分变更可能不会发出该信号。然而，变更序列中的最后一次变更总是会产生该信号。
注意：这是一个私有信号。它可以用于信号连接，但用户不能发射。

### `[private signal] void QFileSystemWatcher::fileChanged(const QString &path)`

**作用与语义：**

当指定`path`的文件被修改、重命名或从磁盘中移除时，会发出该信号。
注意：作为安全措施，许多应用程序通过写入新文件然后删除旧文件来保存打开文件。在你的槽函数中，你可以检查`watcher.files().contains(path)`。如果返回`false`，检查文件是否仍然存在，然后调用`addPath()`继续观看。
注意：这是一个私有信号。它可以用于信号连接，但用户不能发射。

### `QStringList QFileSystemWatcher::files() const`

**作用与语义：**

返回正在监控的文件路径列表。

### `bool QFileSystemWatcher::removePath(const QString &path)`

**作用与语义：**

从文件系统监视器中移除指定的`path`。
如果手表成功移除，则返回true。
手表移除失败的原因通常取决于系统，但也可能是因为路径已被删除。

### `QStringList QFileSystemWatcher::removePaths(const QStringList &paths)`

**作用与语义：**

从文件系统监视器中移除指定的`paths`。
返回值是未能成功取消观看的路径列表。
手表移除失败的原因通常取决于系统，但也可能是因为路径已被删除。

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

`QFileSystemWatcher` 所属机制类型：文件、设备与流机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
