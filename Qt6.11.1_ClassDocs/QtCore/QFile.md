# QFile

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QFile` 是基于 QIODevice 的文件设备，提供打开、读取、写入、定位和刷新文件的接口。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QFile` 是基于 QIODevice 的文件设备，提供打开、读取、写入、定位和刷新文件的接口。

**内部模型：** QFile 本身只描述一个文件设备，open() 成功后才有有效的读写状态。文本编码不是 QFile 自动决定的，文本转换应通过 QTextStream 或明确的 fromUtf8/fromLocal8Bit 处理。

**适用场景：** 读写配置、日志、Markdown、二进制资源和临时文件时使用；大文件应采用流式 read/write，而不是无条件 readAll。

**典型调用链：** 构造路径 -> open(mode) -> 检查返回值/errorString -> read/write/seek -> flush/close -> 由对象析构关闭。

**先记住的坑：** 相对路径依赖当前工作目录；写文件前要确认权限和目录存在；覆盖写入会清空原文件；跨平台路径应使用 QDir/QFileInfo。

## 2. 依赖与对象关系

- 头文件：`#include <QFile>`
- 继承自：QFileDevice
- 直接派生类：QTemporaryFile

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

QFile 本身只描述一个文件设备，open() 成功后才有有效的读写状态。文本编码不是 QFile 自动决定的，文本转换应通过 QTextStream 或明确的 fromUtf8/fromLocal8Bit 处理。

### 状态、生命周期和线程

**生命周期：** 先设置路径或设备，再 open，成功后读写/定位/刷新，最后 close；析构通常会关闭设备，但关键写入应显式 flush/close 并检查错误。相对路径依赖当前工作目录，资源路径和用户文件路径要区分。

**状态与结果：** 区分设备未打开、打开成功、到达 EOF、暂时无数据、读写失败和写入尚未落盘。`readAll()` 方便小数据但可能占用大量内存，大文件应分块处理并检查返回值。

**线程与事件循环：** 同一个打开设备不要跨线程并发使用，除非类明确保证线程安全；后台 I/O 通过 worker 或异步设备处理，GUI 线程只接收结果。

## 3. 直接使用

读写配置、日志、Markdown、二进制资源和临时文件时使用；大文件应采用流式 read/write，而不是无条件 readAll。 使用时通常按这个过程组织：构造路径 -> open(mode) -> 检查返回值/errorString -> read/write/seek -> flush/close -> 由对象析构关闭。

```cpp
#include <QFile>

QFile file(QStringLiteral("data.txt"));
if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    return;
const QByteArray data = file.readAll();
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QFile()`
- `QFile(QObject *parent)`
- `QFile(const QString &name)`
- `(since 6.0) QFile(const std::filesystem::path &name)`
- `QFile(const QString &name, QObject *parent)`
- `(since 6.0) QFile(const std::filesystem::path &name, QObject *parent)`
- `virtual ~QFile()`
- `bool copy(const QString &newName)`
- `(since 6.0) bool copy(const std::filesystem::path &newName)`
- `bool exists() const`
- `(since 6.0) std::filesystem::path filesystemFileName() const`
- `(since 6.3) std::filesystem::path filesystemSymLinkTarget() const`
- `bool link(const QString &linkName)`
- `(since 6.0) bool link(const std::filesystem::path &newName)`
- `bool moveToTrash()`
- `(since 6.3) bool open(QIODeviceBase::OpenMode mode, QFileDevice::Permissions permissions)`
- `bool open(FILE *fh, QIODeviceBase::OpenMode mode, QFileDevice::FileHandleFlags handleFlags = DontCloseHandle)`
- `bool open(int fd, QIODeviceBase::OpenMode mode, QFileDevice::FileHandleFlags handleFlags = DontCloseHandle)`
- `bool remove()`
- `bool rename(const QString &newName)`
- `(since 6.0) bool rename(const std::filesystem::path &newName)`
- `void setFileName(const QString &name)`
- `(since 6.0) void setFileName(const std::filesystem::path &name)`
- `QString symLinkTarget() const`

### 重实现的公有函数

- `virtual QString fileName() const override`
- `virtual bool open(QIODeviceBase::OpenMode mode) override`
- `virtual QFileDevice::Permissions permissions() const override`
- `virtual bool resize(qint64 sz) override`
- `virtual bool setPermissions(QFileDevice::Permissions permissions) override`
- `virtual qint64 size() const override`

### 静态公有成员

- `bool copy(const QString &fileName, const QString &newName)`
- `QString decodeName(const QByteArray &localFileName)`
- `QString decodeName(const char *localFileName)`
- `QByteArray encodeName(const QString &fileName)`
- `bool exists(const QString &fileName)`
- `(since 6.3) std::filesystem::path filesystemSymLinkTarget(const std::filesystem::path &fileName)`
- `bool link(const QString &fileName, const QString &linkName)`
- `bool moveToTrash(const QString &fileName, QString *pathInTrash = nullptr)`
- `QFileDevice::Permissions permissions(const QString &fileName)`
- `(since 6.0) QFileDevice::Permissions permissions(const std::filesystem::path &filename)`
- `bool remove(const QString &fileName)`
- `bool rename(const QString &oldName, const QString &newName)`
- `bool resize(const QString &fileName, qint64 sz)`
- `bool setPermissions(const QString &fileName, QFileDevice::Permissions permissions)`
- `(since 6.0) bool setPermissions(const std::filesystem::path &filename, QFileDevice::Permissions permissionSpec)`
- `(since 6.9) bool supportsMoveToTrash()`
- `QString symLinkTarget(const QString &fileName)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QFile::QFile()`

**作用与语义：**

构建一个QFile对象。

### `[explicit] QFile::QFile(QObject *parent)`

**作用与语义：**

用给定的 `parent` 构建一个新的文件对象。

### `[explicit] QFile::QFile(const QString &name)`

**作用与语义：**

构造一个新的文件对象，以表示该文件的给定`name`。
注意：在包括Qt 6.8在内的版本中，该构造函数为隐式，以保证向后兼容。从Qt 6.9开始，该构造函数无条件`explicit`。用户即使在早期版本的Qt中，也可以通过在包含任何Qt头部前定义`QT_EXPLICIT_QFILE_CONSTRUCTION_FROM_PATH`宏，强制`explicit`该构造函数。

### `[explicit, since 6.0] QFile::QFile(const std::filesystem::path &name)`

**作用与语义：**

构造一个新的文件对象，以表示该文件的给定`name`。
注意：在包括Qt 6.8在内的版本中，该构造函数为隐式，以保证向后兼容。从Qt 6.9开始，该构造函数无条件`explicit`。用户即使在早期版本的Qt中，也可以通过在包含任何Qt头部前定义`QT_EXPLICIT_QFILE_CONSTRUCTION_FROM_PATH`宏，强制`explicit`该构造函数。

### `QFile::QFile(const QString &name, QObject *parent)`

**作用与语义：**

构造一个带有指定`parent`的新文件对象，以表示指定`name`的文件。

### `[since 6.0] QFile::QFile(const std::filesystem::path &name, QObject *parent)`

**作用与语义：**

构造一个带有指定`parent`的新文件对象，以表示指定`name`的文件。

### `[virtual noexcept] QFile::~QFile()`

**作用与语义：**

销毁文件对象，必要时关闭。

### `bool QFile::copy(const QString &newName)`

**作用与语义：**

复制名为`fileName()`的文件`newName`。
该文件在复制前会关闭。
如果复制的文件是符号链接（symlink），则复制的是它所指的文件，而不是链接本身。除了权限外（权限会被复制），其他文件元数据不会被复制。
成功时返回`true`;否则返回`false`。
注意，如果已有名为 `newName` 的文件存在，copy() 返回 `false`。这意味着`QFile`不会覆盖它。
注意：在 Android 平台上，`content`协议 URI 尚未支持该操作。

### `[since 6.0] bool QFile::copy(const std::filesystem::path &newName)`

**作用与语义：**

复制名为`fileName()`的文件`newName`。
该文件在复制前会关闭。
如果复制的文件是符号链接（symlink），则复制的是它所指的文件，而不是链接本身。除了权限外（权限会被复制），其他文件元数据不会被复制。
成功时返回`true`;否则返回`false`。
注意，如果已有名为 `newName` 的文件存在，copy() 返回 `false`。这意味着`QFile`不会覆盖它。
注意：在 Android 平台上，`content`协议 URI 尚未支持该操作。

### `[static] bool QFile::copy(const QString &fileName, const QString &newName)`

**作用与语义：**

将名为`fileName`的文件复制给`newName`。
如果复制的文件是符号链接（symlink），则复制的是它所指的文件，而不是链接本身。除了权限外（权限会被复制），其他文件元数据不会被复制。
成功时返回`true`;否则返回`false`。
注意，如果已有名为 `newName` 的文件存在，copy() 返回 `false`。这意味着`QFile`不会覆盖该文件。
注意：在 Android 平台上，`content` 协议 URI 尚未支持此操作。

### `[static] QString QFile::decodeName(const QByteArray &localFileName)`

**作用与语义：**

这和`QFile::encodeName()`用`localFileName`相反。

### `[static] QString QFile::decodeName(const char *localFileName)`

**作用与语义：**

返回给定`localFileName`的Unicode版本。详情请参见 `encodeName()`。

### `[static] QByteArray QFile::encodeName(const QString &fileName)`

**作用与语义：**

将`fileName`转换为 8 位编码，可以在原生 API 中使用。在 Windows 上，编码来自 Windows 活跃 Windows 代码页（ANSI）。在其他平台上，macOS 的分解形式（NFD）是 UTF-8。

### `[static] bool QFile::exists(const QString &fileName)`

**作用与语义：**

如果`fileName`指定的文件存在，返回`true`;否则返回`false`。
注意：如果`fileName`是一个指向不存在文件的符号链接，则返回false。

### `bool QFile::exists() const`

**作用与语义：**

如果`fileName()`指定的文件存在，返回`true`;否则返回`false`。

### `[override virtual] QString QFile::fileName() const`

**作用与语义：**

重实现自：`QFileDevice::fileName()` const.
返回文件名称，由`setFileName()`、`rename()`或`QFile`构造函数设置。
返回文件名称。`QFileDevice` 的默认实现返回一个空字符串。

### `[since 6.0] std::filesystem::path QFile::filesystemFileName() const`

**作用与语义：**

回归`fileName()`为`std::filesystem::path`。

### `[since 6.3] std::filesystem::path QFile::filesystemSymLinkTarget() const`

**作用与语义：**

以`std::filesystem::path`的身份`symLinkTarget()`回归。

### `[static, since 6.3] std::filesystem::path QFile::filesystemSymLinkTarget(const std::filesystem::path &fileName)`

**作用与语义：**

`symLinkTarget()`回归，作为`std::filesystem::path` `fileName`。

### `bool QFile::link(const QString &linkName)`

**作用与语义：**

创建名为 `linkName` 的链接，指向当前由 `fileName()` 指定的文件。链接的定义取决于底层文件系统（无论是 Windows 上的快捷方式，还是 Unix 上的符号链接）。如果成功，返回 `true`;否则返回 `false`。
该函数不会覆盖文件系统中已存在的实体;此时，`link()` 返回 false，并将 `error()` 返回 `RenameError`。
注意：要在Windows上创建有效的链接，`linkName`必须有`.lnk`的文件扩展名。

### `[since 6.0] bool QFile::link(const std::filesystem::path &newName)`

**作用与语义：**

创建名为 `linkName` 的链接，指向当前由 `fileName()` 指定的文件。链接的定义取决于底层文件系统（无论是 Windows 上的快捷方式，还是 Unix 上的符号链接）。如果成功，返回 `true`;否则返回 `false`。
该函数不会覆盖文件系统中已存在的实体;此时，`link()` 返回 false，并将 `error()` 返回 `RenameError`。
注意：要在Windows上创建有效的链接，`linkName`必须有`.lnk`的文件扩展名。

### `[static] bool QFile::link(const QString &fileName, const QString &linkName)`

**作用与语义：**

创建一个名为 `linkName` 的链接，指向文件 `fileName`。链接的含义取决于底层文件系统（无论是 Windows 上的快捷方式，还是 Unix 上的符号链接）。成功时返回 `true`;否则返回 `false`。

### `bool QFile::moveToTrash()`

**作用与语义：**

将`fileName()`指定的文件移入垃圾桶。成功返回`true`，并将`fileName()`设置为文件在垃圾桶中可找到的路径;否则返回`false`。
该函数运行时间与被丢弃文件大小无关。如果在目录中调用该函数，可能与被丢弃文件数量成正比。如果当前`fileName()`指向符号链接，该函数会将链接移动到垃圾桶，甚至可能破坏它，而不是链接的目标。
该函数使用 Windows 和 macOS API 在这两个操作系统上执行垃圾处理。在其他地方（Unix 系统），该功能实现了 FreeDesktop.org 垃圾规范 1.0 版本。
注意：使用 FreeDesktop.org 垃圾桶实现时，如果无法通过文件重命名和硬链接将文件移动到垃圾桶位置，该功能将失败。这种情况发生在被垃圾文件位于当前用户无权创建`.Trash`目录的卷（挂载点），或存在一些特殊文件系统类型或配置（如子卷本身不是挂载点）时。
注意：在系统API不报告垃圾桶中文件位置的系统中，文件移动后`fileName()`将被设置为空字符串。在没有垃圾桶的系统中，该函数总是返回`false`（参见 `supportsMoveToTrash()`）。

### `[static] bool QFile::moveToTrash(const QString &fileName, QString *pathInTrash = nullptr)`

**作用与语义：**

将`fileName`指定的文件移入垃圾桶。如果成功返回`true`，并将`pathInTrash`设置为文件在垃圾桶中可找到的路径;否则返回`false`。
该函数运行时间与被丢弃文件大小无关。如果在目录中调用该函数，可能与被丢弃文件数量成正比。如果当前`fileName()`指向符号链接，该函数会将链接移动到垃圾堆，甚至可能破坏它，而不是链接的目标。
该函数使用 Windows 和 macOS API 在这两个操作系统上执行垃圾处理。在其他地方（Unix 系统），该功能实现了 FreeDesktop.org 垃圾规范 1.0 版本。
注意：使用 FreeDesktop.org 垃圾桶实现时，如果无法通过文件重命名和硬链接将文件移动到垃圾桶位置，该功能将失败。这种情况发生在被垃圾文件位于当前用户无权创建`.Trash`目录的卷（挂载点），或存在某些特殊文件系统类型或配置（如子卷本身不是挂载点）。
注意：在系统 API 不报告垃圾桶中文件路径的系统上，文件移动后 `pathInTrash` 将设置为空字符串。在没有垃圾桶的系统中，这个函数总是返回 false。

### `[override virtual] bool QFile::open(QIODeviceBase::OpenMode mode)`

**作用与语义：**

重实现自：`QIODevice::open`（QIODeviceBase：：OpenMode 模式）。
使用`mode`标志打开文件，成功时返回`true`;否则返回`false`。
`mode`的标志必须包括`QIODeviceBase::ReadOnly`、`WriteOnly`或`ReadWrite`。还可以有额外的标志，如`Text`和`Unbuffered`。
注意：在`WriteOnly`或`ReadWrite`模式下，如果相关文件不存在，该功能会尝试在打开前创建新文件。该文件创建时模式为0666，在POSIX系统中由umask掩蔽，且在Windows上权限继承自父目录。在Android中，预期拥有访问文件名父文件的权限，否则无法创建这个不存在的文件。
打开设备并将其 OpenMode 设置为 `mode`。成功时返回 `true`;否则返回 `false`。该函数应从任何重新实现的 open() 或其他打开设备的函数中调用。

### `[since 6.3] bool QFile::open(QIODeviceBase::OpenMode mode, QFileDevice::Permissions permissions)`

**作用与语义：**

如果文件不存在且`mode`意味着创建它，则以指定的`permissions`创建。
在POSIX系统中，实际权限受`umask`值影响。
在Windows上，这些权限是通过ACL模拟的。当该组获得的权限比其他组少时，这些ACL可能处于非规范顺序。当打开属性对话框的安全标签时，带有此类权限的文件和目录会生成警告。将所有授予他人的权限授予该组可以避免此类警告。

### `bool QFile::open(FILE *fh, QIODeviceBase::OpenMode mode, QFileDevice::FileHandleFlags handleFlags = DontCloseHandle)`

**作用与语义：**

在给定`mode`中打开现有的文件句柄`fh`。`handleFlags` 可用于指定额外选项。成功时返回`true`;否则返回`false`。
当使用该函数打开`QFile`时，`close()`的行为由 AutoCloseHandle 标志控制。如果指定了 autoCloseHandle，且该函数成功，则调用 `close()` 关闭已采用的句柄。否则，`close()` 实际上并不会关闭文件，只是清除文件。
警告：
- 如果`fh`不指普通文件，例如`stdin`、`stdout`或`stderr`，您可能无法进行`seek()`。`size()`在这些情况下返回`0`。更多信息请参见 `QIODevice::isSequential()`。
- 由于该函数在未指定文件名的情况下打开文件，因此无法将该`QFile`与`QFileInfo`使用。
关于Windows平台的说明。
访问文件和其他随机访问设备时，`fh`必须以二进制模式打开（即模式字符串必须包含“b”，如“rb”或“wb”）。如果你将QIODevice：：Text传给`mode`，Qt会将行尾字符转换。顺序设备，如stdin和stdout不受此限制影响。
你需要启用对控制台应用的支持，才能在控制台上使用 stdin、stdout 和 stderr 流。为此，请在你的应用程序项目文件中添加以下声明：

**官方示例：**

```cpp
 #include <stdio.h>

 void printError(const char* msg)
 {
     QFile file;
     file.open(stderr, QIODevice::WriteOnly);
     file.write(msg, qstrlen(msg));        // write to stderr
     file.close();
 }
```

### `bool QFile::open(int fd, QIODeviceBase::OpenMode mode, QFileDevice::FileHandleFlags handleFlags = DontCloseHandle)`

**作用与语义：**

在给定`mode`中打开现有文件描述符`fd`。`handleFlags`可用于指定额外选项。成功时返回`true`;否则返回`false`。
当使用该函数打开`QFile`时，`close()`的行为由 AutoCloseHandle 标志控制。如果指定了 autoCloseHandle，且该函数成功，则调用 `close()` 关闭所采用的句柄。否则，`close()` 实际上并不会关闭文件，只是清除文件。
警告：如果`fd`不是普通文件，例如0（`stdin`）、1（`stdout`）或2（`stderr`），你可能无法进行`seek()`。在这种情况下，`size()`返回`0`。更多信息请参见 `QIODevice::isSequential()`。
警告：由于该函数在未指定文件名的情况下打开文件，因此无法使用`QFileInfo`的该`QFile`。

### `[override virtual] QFileDevice::Permissions QFile::permissions() const`

**作用与语义：**

重装：`QFileDevice::permissions()` const.
返回文件中 QFile：:P ermission 的完整 OR ed 组合。

### `[static] QFileDevice::Permissions QFile::permissions(const QString &fileName)`

**作用与语义：**

返回完整的 QFile：:P ermission 组合，用于`fileName`。

### `[static, since 6.0] QFileDevice::Permissions QFile::permissions(const std::filesystem::path &filename)`

**作用与语义：**

重装：`QFileDevice::permissions()` const.
返回文件中 QFile：:P ermission 的完整 OR ed 组合。

### `bool QFile::remove()`

**作用与语义：**

移除`fileName()`指定的文件。
如果文件被成功移除，返回`true`;否则返回`false`。
如果文件是打开的，则在移除前就已经关闭了。

### `[static] bool QFile::remove(const QString &fileName)`

**作用与语义：**

移除`fileName`指定的文件。
如果文件被成功移除，返回`true`;否则返回`false`。

### `bool QFile::rename(const QString &newName)`

**作用与语义：**

将当前由`fileName()`指定的文件重命名为`newName`。成功时返回`true`;否则返回`false`。
如果已有名为 `newName` 的文件，rename() 返回 `false`（即 `QFile` 不会覆盖该文件）。
文件在重命名前就已关闭。
如果重命名操作失败，Qt 会尝试将该文件内容复制到 `newName`，然后删除该文件，只保留 `newName`。如果复制操作失败或无法移除该文件，则移除目标文件 `newName`，恢复旧状态。

### `[since 6.0] bool QFile::rename(const std::filesystem::path &newName)`

**作用与语义：**

将当前由`fileName()`指定的文件重命名为`newName`。成功时返回`true`;否则返回`false`。
如果已有名为 `newName` 的文件，rename() 返回 `false`（即 `QFile` 不会覆盖该文件）。
文件在重命名前就已关闭。
如果重命名操作失败，Qt 会尝试将该文件内容复制到 `newName`，然后删除该文件，只保留 `newName`。如果复制操作失败或无法移除该文件，则移除目标文件 `newName`，恢复旧状态。

### `[static] bool QFile::rename(const QString &oldName, const QString &newName)`

**作用与语义：**

将文件重命名为`oldName`为`newName`。成功时返回`true`;否则返回`false`。
如果已有名为 `newName` 的文件，rename() 返回 `false`（即 `QFile` 不会覆盖它）。

### `[override virtual] bool QFile::resize(qint64 sz)`

**作用与语义：**

重装：`QFileDevice::resize`（qint64 sz）。
设置文件大小（字节为单位）`sz`。如果调整大小成功，返回 `true`;否则为假。如果`sz`比当前文件大，则新字节设为0;如果`sz`小，则文件被简单截断。
警告：如果文件不存在，该功能可能会失败。

### `[static] bool QFile::resize(const QString &fileName, qint64 sz)`

**作用与语义：**

将 `fileName` 设置为大小（以字节为单位）`sz`。如果调整大小成功，返回 `true`;否则为假。如果 `sz` 大于当前 `fileName`，则新字节设为 0，若 `sz` 较小，则文件被简单截断。
警告：如果文件不存在，该功能可能会失败。

### `void QFile::setFileName(const QString &name)`

**作用与语义：**

设置文件的`name`。名称可以是无路径、相对路径或绝对路径。
如果文件已经被打开，不要调用该函数。
如果文件名没有路径或相对路径，所使用的路径将是调用`open()`时应用程序当前的目录路径。
注意，目录分隔符“/”适用于Qt支持的所有操作系统。

**官方示例：**

```cpp
 QFile file;
 QDir::setCurrent("/tmp");
 file.setFileName("readme.txt");
 QDir::setCurrent("/home");
 file.open(QIODevice::ReadOnly);      // opens "/home/readme.txt" under Unix
```

### `[since 6.0] void QFile::setFileName(const std::filesystem::path &name)`

**作用与语义：**

设置文件的`name`。名称可以是无路径、相对路径或绝对路径。
如果文件已经被打开，不要调用该函数。
如果文件名没有路径或相对路径，所使用的路径将是调用`open()`时应用程序当前的目录路径。
注意，目录分隔符“/”适用于Qt支持的所有操作系统。

**官方示例：**

```cpp
 QFile file;
 QDir::setCurrent("/tmp");
 file.setFileName("readme.txt");
 QDir::setCurrent("/home");
 file.open(QIODevice::ReadOnly);      // opens "/home/readme.txt" under Unix
```

### `[override virtual] bool QFile::setPermissions(QFileDevice::Permissions permissions)`

**作用与语义：**

重实现自：`QFileDevice::setPermissions`（QFileDevice：:P ermissions permissions）。
将文件权限设置为指定的`permissions`。如果成功，返回`true`;如果权限无法修改，则返回`false`。
警告：该功能不操控前交叉韧带，这可能会限制其效果。
将文件权限设置为指定的`permissions`。如果成功，返回`true`;如果权限无法修改，则返回`false`。
警告：该功能不操控前交叉韧带，这可能会限制其效果。

### `[static] bool QFile::setPermissions(const QString &fileName, QFileDevice::Permissions permissions)`

**作用与语义：**

将`fileName`文件权限设置为`permissions`。

### `[static, since 6.0] bool QFile::setPermissions(const std::filesystem::path &filename, QFileDevice::Permissions permissionSpec)`

**作用与语义：**

重实现自：`QFileDevice::setPermissions`（QFileDevice：:P ermissions permissions）。
将文件权限设置为指定的`permissions`。如果成功，返回`true`;如果权限无法修改，则返回`false`。
警告：该功能不操控前交叉韧带，这可能会限制其效果。
将文件权限设置为指定的`permissions`。如果成功，返回`true`;如果权限无法修改，则返回`false`。
警告：该功能不操控前交叉韧带，这可能会限制其效果。

### `[override virtual] qint64 QFile::size() const`

**作用与语义：**

重装：`QFileDevice::size()` const.

### `[static, since 6.9] bool QFile::supportsMoveToTrash()`

**作用与语义：**

如果 Qt 支持使用 `moveToTrash()` 函数将文件移到当前操作系统中的垃圾桶（回收站），返回`true`，否则`false`。注意，返回 `true` 并不意味着`moveToTrash()`一定成功。特别是，该函数不会检查用户是否在设置中禁用了该功能。

### `[static] QString QFile::symLinkTarget(const QString &fileName)`

**作用与语义：**

返回由`fileName`指定的符号链接（或Windows上的快捷方式）所引用的文件或目录的绝对路径;如果`fileName`不对应符号链接，则返回空字符串。
这个名称可能不代表已有的文件;它只是字符串。如果符号链接指向已有文件，`QFile::exists()`返回`true`。

### `QString QFile::symLinkTarget() const`

**作用与语义：**

返回符号链接（或 Windows 上的快捷方式）指向的文件或目录的绝对路径，如果对象不是符号链接，则返回空字符串。
该名称可能不代表已有文件;它只是字符串。`QFile::exists()`返回 `true`，如果符号链接指向已有文件。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先设置路径或设备，再 open，成功后读写/定位/刷新，最后 close；析构通常会关闭设备，但关键写入应显式 flush/close 并检查错误。相对路径依赖当前工作目录，资源路径和用户文件路径要区分。

### 状态和错误边界

区分设备未打开、打开成功、到达 EOF、暂时无数据、读写失败和写入尚未落盘。`readAll()` 方便小数据但可能占用大量内存，大文件应分块处理并检查返回值。

### 线程边界

同一个打开设备不要跨线程并发使用，除非类明确保证线程安全；后台 I/O 通过 worker 或异步设备处理，GUI 线程只接收结果。

### 最容易出现的错误

相对路径依赖当前工作目录；写文件前要确认权限和目录存在；覆盖写入会清空原文件；跨平台路径应使用 QDir/QFileInfo。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QFile` 所属机制类型：文件、设备与流机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
