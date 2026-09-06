# QStorageInfo

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QStorageInfo` 是 文件、设备与流机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QStorageInfo` 是 文件、设备与流机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 文件和 I/O 类型把路径/设备描述与打开后的读写状态分开。打开模式决定可执行的操作，当前位置、缓冲区、文本编码、权限和错误状态共同决定一次读写是否正确。

**适用场景：** 构造稳定路径，选择正确的 OpenMode，检查 open 和 errorString，按数据规模使用流式读写或分块处理，明确文本编码，完成后关闭并处理失败。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要手写平台分隔符；不要默认相对路径指向程序目录；不要把本地编码、UTF-8 和二进制混在一起；写文件时要考虑临时文件、覆盖、权限和原子替换。

## 2. 依赖与对象关系

- 头文件：`#include <QStorageInfo>`
- 继承自：未在类页中列出
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

- `QStorageInfo()`
- `QStorageInfo(const QDir &dir)`
- `QStorageInfo(const QString &path)`
- `QStorageInfo(const QStorageInfo &other)`
- `(since 6.10) QStorageInfo(QStorageInfo &&other)`
- `~QStorageInfo()`
- `int blockSize() const`
- `qint64 bytesAvailable() const`
- `qint64 bytesFree() const`
- `qint64 bytesTotal() const`
- `QByteArray device() const`
- `QString displayName() const`
- `QByteArray fileSystemType() const`
- `bool isReadOnly() const`
- `bool isReady() const`
- `bool isRoot() const`
- `bool isValid() const`
- `QString name() const`
- `void refresh()`
- `QString rootPath() const`
- `void setPath(const QString &path)`
- `QByteArray subvolume() const`
- `void swap(QStorageInfo &other)`
- `QStorageInfo & operator=(QStorageInfo &&other)`
- `QStorageInfo & operator=(const QStorageInfo &other)`

### 静态公有成员

- `QList<QStorageInfo> mountedVolumes()`
- `QStorageInfo root()`

### 相关非成员函数

- `bool operator!=(const QStorageInfo &lhs, const QStorageInfo &rhs)`
- `bool operator==(const QStorageInfo &lhs, const QStorageInfo &rhs)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QStorageInfo::QStorageInfo()`

**作用与语义：**

构建一个空的 QStorageInfo 对象。
使用默认构造函数创建的对象将无效，因此无法使用。

### `[explicit] QStorageInfo::QStorageInfo(const QDir &dir)`

**作用与语义：**

构建一个新的QStorageInfo对象，提供包含`dir`文件夹的卷的信息。

### `[explicit] QStorageInfo::QStorageInfo(const QString &path)`

**作用与语义：**

构建一个新的QStorageInfo对象，提供`path`上安装的卷的信息。
如果你传递一个目录或文件，QStorageInfo 对象会指向该目录或文件所在的卷。你可以用 `isValid()` 方法检查创建的对象是否正确。
以下示例展示了如何获取应用所在的卷。建议始终检查该卷是否已准备好且有效。

**官方示例：**

```cpp
 QStorageInfo storage(qApp->applicationDirPath());
 if (storage.isValid() && storage.isReady()) {
     // ...
 }
```

### `QStorageInfo::QStorageInfo(const QStorageInfo &other)`

**作用与语义：**

构建一个新的 QStorageInfo 对象，该对象是 `other` QStorageInfo 对象的复制品。

### `[constexpr noexcept, since 6.10] QStorageInfo::QStorageInfo(QStorageInfo &&other)`

**作用与语义：**

从`other`移动构建新的QStorageInfo。
移除对象`other`处于部分形成状态，唯一有效的操作是销毁和赋予新值。

### `[noexcept] QStorageInfo::~QStorageInfo()`

**作用与语义：**

摧毁`QStorageInfo`物体并释放其资源。

### `int QStorageInfo::blockSize() const`

**作用与语义：**

返回该文件系统的最佳传输块大小。
如果无法确定`QStorageInfo`大小或`QStorageInfo`对象无效，则返回-1。

### `qint64 QStorageInfo::bytesAvailable() const`

**作用与语义：**

返回当前用户可用的大小（字节单位）。如果用户是根用户或系统管理员，则返回可用的总大小。
该大小可小于或等于函数返回的自由大小`bytesFree()`。
如果`QStorageInfo`对象无效，返回-1。

### `qint64 QStorageInfo::bytesFree() const`

**作用与语义：**

返回卷中可用的字节数。注意，如果文件系统存在配额，这个值可能大于`bytesAvailable()`返回的值。
如果`QStorageInfo`对象无效，返回-1。

### `qint64 QStorageInfo::bytesTotal() const`

**作用与语义：**

返回总卷大小（字节单位）。
如果`QStorageInfo`对象无效，返回-1。

### `QByteArray QStorageInfo::device() const`

**作用与语义：**

本卷还了设备。
例如，在 Unix 文件系统（包括 macOS）上，这会返回开发路径，类似于本地存储的 `/dev/sda0`。在 Windows 上，它返回以 `\\\\?\\` 开头的 UNC 路径，用于本地存储（换句话说，是卷的 GUID）。

### `QString QStorageInfo::displayName() const`

**作用与语义：**

如果有，返回卷的名称，如果没有则返回根路径。

### `QByteArray QStorageInfo::fileSystemType() const`

**作用与语义：**

返回文件系统的类型名称。
这是一个平台依赖的功能，文件系统名称在不同操作系统之间可能有所不同。例如，在 Windows 文件系统中，文件系统可以命名为 `NTFS`，在 Linux 上可以命名为 `ntfs-3g` 或 `fuseblk`。

### `bool QStorageInfo::isReadOnly() const`

**作用与语义：**

如果当前文件系统受到写入保护，则返回 true;否则返回 false。

### `bool QStorageInfo::isReady() const`

**作用与语义：**

如果当前文件系统已准备好工作，则返回 true;否则返回 false。例如，如果未插入 CD 卷，则返回 false。
注意，`fileSystemType()`、`name()`、`bytesTotal()`、`bytesFree()`和`bytesAvailable()`在卷准备好前都会返回无效数据。

### `bool QStorageInfo::isRoot() const`

**作用与语义：**

如果该`QStorageInfo`代表系统根体积，则返回真;否则返回为假。
在Unix文件系统中，根卷是挂载在`/`上的卷。在Windows上，根卷是操作系统安装的卷。

### `bool QStorageInfo::isValid() const`

**作用与语义：**

如果`rootPath`指定的`QStorageInfo`存在且正确挂载，则返回为真。

### `[static] QList<QStorageInfo> QStorageInfo::mountedVolumes()`

**作用与语义：**

返回对应当前挂载文件系统列表的`QStorageInfo`对象列表。
在 Windows 上，返回的是“我的电脑”文件夹中可见的驱动器。在 Unix 操作系统中，返回所有已挂载文件系统的列表（伪文件系统除外）。
默认返回所有当前挂载的文件系统。
示例展示了如何检索所有可用的文件系统，跳过只读文件。

**官方示例：**

```cpp
 foreach (const QStorageInfo &storage, QStorageInfo::mountedVolumes()) {
     if (storage.isValid() && storage.isReady()) {
         if (!storage.isReadOnly()) {
             // ...
         }
     }
 }
```

### `QString QStorageInfo::name() const`

**作用与语义：**

返回一个人类可读的文件系统名称，通常称为`label`。
并非所有文件系统都支持此功能。在这种情况下，该方法返回的值可能是空的。如果文件系统不支持标签，或者没有设置标签，则返回空字符串。
在 Linux 上，获取卷标签需要系统中有`udev`。

### `void QStorageInfo::refresh()`

**作用与语义：**

重置`QStorageInfo`的内部缓存。
`QStorageInfo`缓存关于存储的信息以加快性能。`QStorageInfo`在对象构建和/或调用`setPath()`方法时检索信息。你必须手动重置缓存，通过调用该函数来更新存储信息。

### `[static] QStorageInfo QStorageInfo::root()`

**作用与语义：**

返回一个`QStorageInfo`对象，代表系统根卷。
在 Unix 系统中，该调用返回根（'/'）卷;在 Windows 中返回安装操作系统的卷。

### `QString QStorageInfo::rootPath() const`

**作用与语义：**

返回该`QStorageInfo`对象所代表的文件系统的挂载点。
在Windows上，如果卷未挂载到目录，它会返回卷函。
注意，rootPath() 返回的值是卷的实际挂载点，可能不等于传递给构造函数或`setPath()`方法的值。例如，如果你系统中只有根卷，并将“/directory”传递给`setPath()`，那么该方法会返回 '/'。

### `void QStorageInfo::setPath(const QString &path)`

**作用与语义：**

将该`QStorageInfo`对象设置为挂载的文件系统，`path`所在位置。
`path`可以是文件系统的根路径、目录，或该文件系统内的文件。

### `QByteArray QStorageInfo::subvolume() const`

**作用与语义：**

返回该卷的子卷名。
某些文件系统类型允许在同一设备内有多个子卷，这些子卷可以通过不同路径挂载（例如在 Unix 上“绑定”挂载，或 Btrfs 文件系统子卷）。如果能检测到子卷，该函数会返回其名称。子卷名称的格式针对每种文件系统类型而异。
如果该卷不是从更大文件系统的子卷挂载，或者无法检测到该子卷，该函数会返回一个空字节数组。

### `[noexcept] void QStorageInfo::swap(QStorageInfo &other)`

**作用与语义：**

将这些音量信息与`other`交换。这个操作非常快，而且从未失败过。

### `[noexcept] QStorageInfo &QStorageInfo::operator=(QStorageInfo &&other)`

**作用与语义：**

Move-assign `other`到这个`QStorageInfo`实例。
被移出的对象`other`被置于有效但未指定的状态。

### `QStorageInfo &QStorageInfo::operator=(const QStorageInfo &other)`

**作用与语义：**

复制`QStorageInfo`对象`other`并将其分配给该`QStorageInfo`对象。

### `[noexcept] bool operator!=(const QStorageInfo &lhs, const QStorageInfo &rhs)`

**作用与语义：**

返回`true`如果`QStorageInfo`物体`lhs`指的是与  不同的驱动器或卷`QStorageInfo`物体`rhs`; 否则返回 `false`.

### `[noexcept] bool operator==(const QStorageInfo &lhs, const QStorageInfo &rhs)`

**作用与语义：**

如果 `QStorageInfo` 对象 `lhs` 指向与 `QStorageInfo` 对象 `rhs` 相同的驱动器或卷，则返回 `true`；否则返回 `false`。请注意，比较两个无效的 `QStorageInfo` 对象的结果总是为正。

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

`QStorageInfo` 所属机制类型：文件、设备与流机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
