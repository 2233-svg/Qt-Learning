# QFileInfo

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 文件或目录元数据对象，负责查询路径、大小、时间、权限和类型。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QFileInfo`：文件或目录元数据对象，负责查询路径、大小、时间、权限和类型。

**内部模型：** 文件和 I/O 类型把路径/设备描述与打开后的读写状态分开。打开模式决定可执行的操作，当前位置、缓冲区、文本编码、权限和错误状态共同决定一次读写是否正确。

**适用场景：** 构造稳定路径，选择正确的 OpenMode，检查 open 和 errorString，按数据规模使用流式读写或分块处理，明确文本编码，完成后关闭并处理失败。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要手写平台分隔符；不要默认相对路径指向程序目录；不要把本地编码、UTF-8 和二进制混在一起；写文件时要考虑临时文件、覆盖、权限和原子替换。

## 2. 依赖与对象关系

- 头文件：`#include <QFileInfo>`
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

- `QFileInfo()`
- `QFileInfo(const QFileDevice &file)`
- `QFileInfo(const QString &path)`
- `(since 6.0) QFileInfo(const std::filesystem::path &file)`
- `QFileInfo(const QDir &dir, const QString &path)`
- `(since 6.0) QFileInfo(const QDir &dir, const std::filesystem::path &path)`
- `QFileInfo(const QFileInfo &fileinfo)`
- `~QFileInfo()`
- `QDir absoluteDir() const`
- `QString absoluteFilePath() const`
- `QString absolutePath() const`
- `QString baseName() const`
- `QDateTime birthTime() const`
- `(since 6.6) QDateTime birthTime(const QTimeZone &tz) const`
- `QString bundleName() const`
- `bool caching() const`
- `QString canonicalFilePath() const`
- `QString canonicalPath() const`
- `QString completeBaseName() const`
- `QString completeSuffix() const`
- `QDir dir() const`
- `bool exists() const`
- `QString fileName() const`
- `QString filePath() const`
- `QDateTime fileTime(QFileDevice::FileTime time) const`
- `(since 6.6) QDateTime fileTime(QFileDevice::FileTime time, const QTimeZone &tz) const`
- `(since 6.0) std::filesystem::path filesystemAbsoluteFilePath() const`
- `(since 6.0) std::filesystem::path filesystemAbsolutePath() const`
- `(since 6.0) std::filesystem::path filesystemCanonicalFilePath() const`
- `(since 6.0) std::filesystem::path filesystemCanonicalPath() const`
- `(since 6.0) std::filesystem::path filesystemFilePath() const`
- `(since 6.2) std::filesystem::path filesystemJunctionTarget() const`
- `(since 6.0) std::filesystem::path filesystemPath() const`
- `(since 6.6) std::filesystem::path filesystemReadSymLink() const`
- `(since 6.0) std::filesystem::path filesystemSymLinkTarget() const`
- `QString group() const`
- `uint groupId() const`
- `bool isAbsolute() const`
- `(since 6.4) bool isAlias() const`
- `bool isBundle() const`
- `bool isDir() const`
- `bool isExecutable() const`
- `bool isFile() const`
- `bool isHidden() const`
- `bool isJunction() const`
- `bool isNativePath() const`
- `(since 6.10) bool isOther() const`
- `bool isReadable() const`
- `bool isRelative() const`
- `bool isRoot() const`
- `bool isShortcut() const`
- `bool isSymLink() const`
- `bool isSymbolicLink() const`
- `bool isWritable() const`
- `(since 6.2) QString junctionTarget() const`
- `QDateTime lastModified() const`
- `(since 6.6) QDateTime lastModified(const QTimeZone &tz) const`
- `QDateTime lastRead() const`
- `(since 6.6) QDateTime lastRead(const QTimeZone &tz) const`
- `bool makeAbsolute()`
- `QDateTime metadataChangeTime() const`
- `(since 6.6) QDateTime metadataChangeTime(const QTimeZone &tz) const`
- `QString owner() const`
- `uint ownerId() const`
- `QString path() const`
- `bool permission(QFileDevice::Permissions permissions) const`
- `QFileDevice::Permissions permissions() const`
- `(since 6.6) QString readSymLink() const`
- `void refresh()`
- `void setCaching(bool enable)`
- `void setFile(const QString &path)`
- `(since 6.0) void setFile(const std::filesystem::path &path)`
- `void setFile(const QFileDevice &file)`
- `void setFile(const QDir &dir, const QString &path)`
- `qint64 size() const`
- `(since 6.0) void stat()`
- `QString suffix() const`
- `void swap(QFileInfo &other)`
- `QString symLinkTarget() const`
- `QFileInfo & operator=(QFileInfo &&other)`
- `QFileInfo & operator=(const QFileInfo &fileinfo)`

### 静态公有成员

- `bool exists(const QString &path)`

### 相关非成员函数

- `QFileInfoList`
- `bool operator!=(const QFileInfo &lhs, const QFileInfo &rhs)`
- `bool operator==(const QFileInfo &lhs, const QFileInfo &rhs)`

### 公开宏

- `(since 6.0) QT_IMPLICIT_QFILEINFO_CONSTRUCTION`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QFileInfo::QFileInfo()`

**作用与语义：**

构建一个空的 QFileInfo 对象，不引用任何文件系统条目。

### `[explicit] QFileInfo::QFileInfo(const QFileDevice &file)`

**作用与语义：**

构建一个新的QFileInfo，提供文件`file`的信息。
如果`file`有相对路径，QFileInfo也会有相对路径。

### `[explicit] QFileInfo::QFileInfo(const QString &path)`

**作用与语义：**

构建一个QFileInfo，提供位于`path`的文件系统条目信息，这些条目可以是绝对的，也可以是相对的。
如果`path`是相对的，QFileInfo也会有相对路径。

### `[since 6.0] QFileInfo::QFileInfo(const std::filesystem::path &file)`

**作用与语义：**

构建一个新的QFileInfo，提供关于给定`file`的信息。

### `[explicit] QFileInfo::QFileInfo(const QDir &dir, const QString &path)`

**作用与语义：**

构建一个新的QFileInfo，提供相对于目录`dir`的给定文件系统条目`path`信息。
如果`dir`有相对路径，QFileInfo也会有相对路径。
如果`path`是绝对的，那么`dir`指定的目录将被忽略。

### `[since 6.0] QFileInfo::QFileInfo(const QDir &dir, const std::filesystem::path &path)`

**作用与语义：**

构建一个新的QFileInfo，提供相对于目录`dir`的关于`path`文件系统条目的信息。
如果`dir`有相对路径，QFileInfo也会有相对路径。
如果`path`是绝对的，那么`dir`指定的目录将被忽略。

### `QFileInfo::QFileInfo(const QFileInfo &fileinfo)`

**作用与语义：**

构建一个新的QFileInfo，它是给定`fileinfo`的副本。

### `[noexcept] QFileInfo::~QFileInfo()`

**作用与语义：**

摧毁`QFileInfo`并释放其资源。

### `QDir QFileInfo::absoluteDir() const`

**作用与语义：**

返回一个`QDir`对象，表示该`QFileInfo`所指文件系统条目父目录的绝对路径。

**官方示例：**

```cpp
 // Given a current working directory of "/home/user/Documents/memos/"
 QFileInfo info1(u"relativeFile"_s);
 qDebug() << info1.absolutePath(); // "/home/user/Documents/memos/"
 qDebug() << info1.baseName(); // "relativeFile"
 qDebug() << info1.absoluteDir(); // QDir(u"/home/user/Documents/memos"_s)
 qDebug() << info1.absoluteDir().path(); // "/home/user/Documents/memos"

 // A QFileInfo on a dir
 QFileInfo info2(u"/home/user/Documents/memos"_s);
 qDebug() << info2.absolutePath(); // "/home/user/Documents"
 qDebug() << info2.baseName(); // "memos"
 qDebug() << info2.absoluteDir(); // QDir(u"/home/user/Documents"_s)
 qDebug() << info2.absoluteDir().path(); // "/home/user/Documents"
```

### `QString QFileInfo::absoluteFilePath() const`

**作用与语义：**

返回该`QFileInfo`所指文件系统条目的绝对完整路径，包括条目名称。
在 Unix 上，绝对路径以目录分隔符 `'/'` 开头。在 Windows 上，绝对路径以驱动器规范开头（例如 `D:/`）。
在Windows上，未映射到驱动器代号的网络共享路径以`//sharename/`开头。
`QFileInfo`大写驱动器字母。注意`QDir`不会这样做。下面的代码片段展示了这一点。
该函数返回与`filePath()`相同，除非`isRelative()`为真。与`canonicalFilePath()`不同，符号链接或冗余的“.”或“..”元素不一定被删除。
警告：如果`filePath()`为空，该函数的行为未定义。

**官方示例：**

```cpp
     QFileInfo fi("c:/temp/foo");
     qDebug() << fi.absoluteFilePath(); // "C:/temp/foo"
```

### `QString QFileInfo::absolutePath() const`

**作用与语义：**

返回该`QFileInfo`所指文件系统条目的绝对路径，但不包含条目名称。
在 Unix 上，绝对路径以目录分隔符 `'/'` 开头。在 Windows 上，绝对路径以驱动器规范开头（例如 `D:/`）。
在Windows上，未映射到驱动器代号的网络共享路径以`//sharename/`开头。
与`canonicalPath()`符号链接或冗余的“..”或“..”元素不同，元素不一定被移除。
警告：如果`filePath()`为空，该函数的行为是未定义的。

### `QString QFileInfo::baseName() const`

**作用与语义：**

返回文件的基名，但不含路径。
基名包含文件中直到第一个“.”字符（但不包括）的所有字符。
文件的基名在所有平台上均等计算，独立于文件命名惯例（例如，Unix 上的“.bashrc”基名为空，后缀为“bashrc”）。

**官方示例：**

```cpp
 QFileInfo fi("/tmp/archive.tar.gz");
 QString base = fi.baseName();  // base = "archive"
```

### `QDateTime QFileInfo::birthTime() const`

**作用与语义：**

返回文件创建（出生）的日期和时间，按当地时间计算。
如果文件出生时间不可得，该函数返回无效`QDateTime`。
如果文件是符号链接，该函数返回的是目标信息，而非符号链接。
该函数会超载 QFileInfo：：birthTime（const `QTimeZone` &tz），返回与 `birthTime(QTimeZone::LocalTime)` 相同的结果。

### `[since 6.6] QDateTime QFileInfo::birthTime(const QTimeZone &tz) const`

**作用与语义：**

返回文件创建（出生）的日期和时间。
返回的时间位于`tz`指定的时区内。例如，你可以用`QTimeZone::LocalTime`或`QTimeZone::UTC`分别获取本地时区或UTC时间。由于本地文件系统API通常使用UTC，使用`QTimeZone::UTC`通常更快，因为它不需要转换。
如果文件的出生时间不可用，该函数会返回无效的`QDateTime`。
如果文件是符号链接，该函数返回的是目标信息，而非符号链接。

### `QString QFileInfo::bundleName() const`

**作用与语义：**

返回该捆绑包的名称。
在macOS和iOS上，如果路径`isBundle()`，会返回正确的本地化名称。在其他平台上，返回的是空`QString`。

**官方示例：**

```cpp
 QFileInfo fi("/Applications/Safari.app");
 QString bundle = fi.bundleName();                // name = "Safari"
```

### `bool QFileInfo::caching() const`

**作用与语义：**

如果启用了缓存，则返回 `true`；否则返回 `false`。

### `QString QFileInfo::canonicalFilePath() const`

**作用与语义：**

返回文件系统条目的规范路径，包括条目名称，即无符号链接或冗余`'.'`或`'..'`元素的绝对路径。
如果该条目不存在，canonicalFilePath() 返回一个空字符串。

### `QString QFileInfo::canonicalPath() const`

**作用与语义：**

返回文件系统条目的规范路径（不包括条目名称），即无符号链接或冗余“.”或“..”元素的绝对路径。
如果该条目不存在，该方法返回一个空字符串。

### `QString QFileInfo::completeBaseName() const`

**作用与语义：**

返回文件的完整基名，但不含路径。
完整的基名包含文件中直到（但不包括）最后一个“.”字符为止的所有字符。

**官方示例：**

```cpp
 QFileInfo fi("/tmp/archive.tar.gz");
 QString base = fi.completeBaseName();  // base = "archive.tar"
```

### `QString QFileInfo::completeSuffix() const`

**作用与语义：**

返回文件的完整后缀（扩展名）。
完整后缀包含文件中第一个“.”之后（但不包括）的所有字符。

**官方示例：**

```cpp
 QFileInfo fi("/tmp/archive.tar.gz");
 QString ext = fi.completeSuffix();  // ext = "tar.gz"
```

### `QDir QFileInfo::dir() const`

**作用与语义：**

返回一个`QDir`对象，表示该`QFileInfo`所指文件系统条目父目录的路径。
注意：返回的`QDir`始终对应对象的父目录，即使`QFileInfo`代表目录。
对于以下每一种，dir() 返回`QDir` `"~/examples/191697"`。
对于以下每一种，dir() 返回`QDir` `"."`。

**官方示例：**

```cpp
     QFileInfo fileInfo1("~/examples/191697/.");
     QFileInfo fileInfo2("~/examples/191697/..");
     QFileInfo fileInfo3("~/examples/191697/main.cpp");
```

### `bool QFileInfo::exists() const`

**作用与语义：**

如果`QFileInfo`引用的文件系统条目存在，返回`true`;否则返回`false`。
注意：如果条目指向不存在的目标的符号链接，该方法返回`false`。

### `[static] bool QFileInfo::exists(const QString &path)`

**作用与语义：**

如果文件系统条目存在，返回`true` `path`;否则返回 `false`。
注意：如果`path`是一个指向不存在目标的符号链接，该方法返回`false`。
注意：使用该函数比使用`QFileInfo(path).exists()`访问文件系统更快。

### `QString QFileInfo::fileName() const`

**作用与语义：**

返回该`QFileInfo`所指的文件系统条目名称，但不含路径。
注意：如果该`QFileInfo`路径以目录分隔符`'/'`结尾，则条目名称部分视为空。

**官方示例：**

```cpp
 QFileInfo fi("/tmp/archive.tar.gz");
 QString name = fi.fileName();                // name = "archive.tar.gz"
```

### `QString QFileInfo::filePath() const`

**作用与语义：**

返回本`QFileInfo`所指文件系统条目的路径;路径可以是绝对的，也可以是相对的。

### `QDateTime QFileInfo::fileTime(QFileDevice::FileTime time) const`

**作用与语义：**

返回`time`指定的文件时间。
如果无法确定时间，则返回无效的日期时间。
如果文件是符号链接，该函数返回的是目标信息，而非符号链接。
该函数会超载 `QFileInfo::fileTime`（QFileDevice：：FileTime， const QTimeZone &），并返回与`fileTime(time, QTimeZone::LocalTime)`相同的结果。

### `[since 6.6] QDateTime QFileInfo::fileTime(QFileDevice::FileTime time, const QTimeZone &tz) const`

**作用与语义：**

返回`time`指定的文件时间。
返回的时间位于`tz`指定的时区内。例如，你可以用`QTimeZone::LocalTime`或`QTimeZone::UTC`分别获取本地时区或UTC时间。由于原生文件系统API通常使用UTC，使用`QTimeZone::UTC`通常更快，因为它不需要任何转换。
如果无法确定时间，则返回无效的日期时间。
如果文件是符号链接，该函数返回的是目标信息，而非符号链接。

### `[since 6.0] std::filesystem::path QFileInfo::filesystemAbsoluteFilePath() const`

**作用与语义：**

`absoluteFilePath()`以`std::filesystem::path`身份回归。

### `[since 6.0] std::filesystem::path QFileInfo::filesystemAbsolutePath() const`

**作用与语义：**

`absolutePath()`回归，成为`std::filesystem::path`。

### `[since 6.0] std::filesystem::path QFileInfo::filesystemCanonicalFilePath() const`

**作用与语义：**

`canonicalFilePath()`以`std::filesystem::path`身份回归。

### `[since 6.0] std::filesystem::path QFileInfo::filesystemCanonicalPath() const`

**作用与语义：**

`canonicalPath()`以`std::filesystem::path`身份回归。

### `[since 6.0] std::filesystem::path QFileInfo::filesystemFilePath() const`

**作用与语义：**

将 `filePath()` 返回为 `std::filesystem::path`。

### `[since 6.2] std::filesystem::path QFileInfo::filesystemJunctionTarget() const`

**作用与语义：**

将 `junctionTarget()` 作为 `std::filesystem::path` 返回。

### `[since 6.0] std::filesystem::path QFileInfo::filesystemPath() const`

**作用与语义：**

将 `path()` 返回为 `std::filesystem::path`。

### `[since 6.6] std::filesystem::path QFileInfo::filesystemReadSymLink() const`

**作用与语义：**

`readSymLink()`回归，作为`std::filesystem::path`。

### `[since 6.0] std::filesystem::path QFileInfo::filesystemSymLinkTarget() const`

**作用与语义：**

`symLinkTarget()`回归，作为`std::filesystem::path`。

### `QString QFileInfo::group() const`

**作用与语义：**

返回文件的组。在Windows系统中，文件没有组，或者发生错误时，返回空字符串。
在Unix下，这个函数可能耗时（以毫秒为单位）。
如果文件是符号链接，该函数返回的是目标信息，而非符号链接。

### `uint QFileInfo::groupId() const`

**作用与语义：**

返回文件所属组的ID。
在Windows和文件没有组的系统中，这个函数总是返回（uint）-2。
如果文件是符号链接，该函数返回的是目标信息，而非符号链接。

### `bool QFileInfo::isAbsolute() const`

**作用与语义：**

如果文件系统条目的路径是绝对的，返回`true`;否则返回 `false`（即路径是相对的）。
注意：以冒号（:) 开头的路径始终被视为绝对路径，因为它们表示一个`QResource`。

### `[since 6.4] bool QFileInfo::isAlias() const`

**作用与语义：**

如果该对象指向别名，返回`true`;否则返回`false`。
别名只存在于macOS上。它们被视为普通文件，因此打开别名会打开文件本身。要打开文件或目录，别名引用需要`symLinkTarget()`。
注意：即使别名指向不存在的文件，isAlias() 返回 true。

### `bool QFileInfo::isBundle() const`

**作用与语义：**

如果该对象指向捆绑包或 macOS 和 iOS 上的捆绑包符号链接，则返回 `true`;否则返回 `false`。
如果文件是符号链接，该函数返回的是目标信息，而非符号链接。

### `bool QFileInfo::isDir() const`

**作用与语义：**

如果该对象指向目录或指向指向目录的符号链接，返回`true`。如果该对象指向非目录（如文件）或不存在的事物，返回`false`。
如果文件是符号链接，该函数返回的是目标信息，而非符号链接。

### `bool QFileInfo::isExecutable() const`

**作用与语义：**

如果该`QFileInfo`所指的文件系统条目是可执行的，返回`true`;否则返回`false`。
如果文件是符号链接，该函数返回的是目标信息，而非符号链接。

### `bool QFileInfo::isFile() const`

**作用与语义：**

如果该对象指向文件或指向文件的符号链接，返回`true`。如果该对象指向非文件（如目录）或不存在的对象，返回`false`。
如果文件是符号链接，该函数返回的是目标信息，而非符号链接。

### `bool QFileInfo::isHidden() const`

**作用与语义：**

如果本`QFileInfo`指的文件系统条目是 `hidden'; otherwise returns `false'，则返回`true`。
注意：该函数在Unix上返回`true`，针对特殊条目“..”和“..”，尽管`QDir::entryList`对它们如图处理。注意，由于该函数检查文件名，在Unix上如果该文件是符号链接，它会检查符号链接的名称，而非目标名称。
在Windows上，如果目标文件被隐藏（不是符号链接），该函数会返回`true`。

### `bool QFileInfo::isJunction() const`

**作用与语义：**

如果对象指向交汇点，返回`true`;否则返回`false`。
连接仅存在于 Windows 的 NTFS 文件系统中，通常由 `mklink` 命令创建。它们可以被视为目录的符号链接，只能为本地卷上的绝对路径创建。

### `bool QFileInfo::isNativePath() const`

**作用与语义：**

如果文件路径可以直接与本地 API 一起使用，返回`true`。如果文件在 Qt 内部的虚拟文件系统（如 Qt 资源系统）中支持，返回`false`。
注意：原生路径仍可能需要转换路径分隔符和字符编码，具体取决于本地API的平台和输入需求。

### `[since 6.10] bool QFileInfo::isOther() const`

**作用与语义：**

如果该`QFileInfo`指的是非目录、非常规文件或符号链接的文件系统条目，返回`true`。否则返回`false`。
如果该`QFileInfo`指向不存在的条目，该方法返回`false`。
如果条目是悬挂符号链路（目标不存在），该方法返回`false`。对于非悬挂符号链路，该函数返回的是目标的信息，而非符号链路。
在Unix上，特殊的（其他）文件系统条目是FIFO、套接字、字符设备或块设备。更多详情请参见`mknod`手册页面。
在Windows上（出于历史原因，参见符号链接和快捷方式），该方法返回`.lnk`文件的 `true`。

### `bool QFileInfo::isReadable() const`

**作用与语义：**

如果用户能读取该`QFileInfo`指的文件系统条目，返回 `true`;否则返回 `false`。
如果文件是符号链接，该函数返回的是目标信息，而非符号链接。
注意：如果未启用NTFS权限检查，Windows上的结果仅反映该条目是否存在。

### `bool QFileInfo::isRelative() const`

**作用与语义：**

如果文件系统条目的路径是相对的，返回`true`;否则返回 ，返回`false`（即路径是绝对的）。
在 Unix 上，绝对路径以目录分隔符 `'/'` 开头。在 Windows 上，绝对路径以驱动器规格开头（例如 `D:/`）。
注意：以冒号（:)开头的路径总是被视为绝对的，因为它们表示`QResource`。

### `bool QFileInfo::isRoot() const`

**作用与语义：**

如果对象指向目录或指向指向某个目录的符号链接，且该目录是根目录，则返回`true`;否则返回`false`。

### `bool QFileInfo::isShortcut() const`

**作用与语义：**

如果该对象指向快捷方式，返回`true`;否则返回`false`。
快捷方式仅存在于 Windows，通常为`.lnk`文件。例如，在 Windows 上，快捷方式（`*.lnk` 文件）会返回 true，而在 Unix（包括 macOS 和 iOS）上返回 false。
快捷方式（.lnk）文件被视为普通文件。打开这些文件会打开`.lnk`文件本身。为了打开快捷方式所引用的文件，必须使用快捷方式上的`symLinkTarget()`。
注意：即使某个快捷方式（坏掉的快捷方式）指向不存在的文件，isShortcut() 也会返回 true。

### `bool QFileInfo::isSymLink() const`

**作用与语义：**

如果该对象指向符号链接、快捷方式或别名，返回`true`;否则返回`false`。
符号链接存在于 Unix（包括 macOS 和 iOS）和 Windows 上，通常分别由 `ln -s` 或 `mklink` 命令创建。打开符号链接实际上是打开该链接的目标。
此外，Windows 上的快捷方式（`*.lnk` 文件）和 macOS 上的别名会返回 true。这种行为已被弃用，未来 Qt 版本可能会改变。打开快捷方式或别名会打开 `.lnk` 或别名文件本身。
注意：如果符号链接指向已有目标，则`exists()`返回`true`，否则返回`false`。

**官方示例：**

```cpp
 QFileInfo info(fileName);
 if (info.isSymLink())
     fileName = info.symLinkTarget();
```

### `bool QFileInfo::isSymbolicLink() const`

**作用与语义：**

如果该对象指向符号链接，则返回`true`;否则返回`false`。
符号链接存在于Unix（包括macOS和iOS）和Windows（NTFS符号链接）上，通常分别由`ln -s`或`mklink`命令创建。
Unix 透明地处理符号链接。打开符号链接实际上是打开了链接的目标。
与`isSymLink()`不同，Windows上的快捷方式（`*.lnk`文件）和macOS上的别名会返回false。请使用`QFileInfo::isShortcut()`和`QFileInfo::isAlias()`。
注意：如果符号链接指向已有目标，则`exists()`返回`true`，否则返回`false`。

### `bool QFileInfo::isWritable() const`

**作用与语义：**

如果用户能够写入该`QFileInfo`所指的文件系统条目，返回`true`;否则返回`false`。
如果文件是符号链接，该函数返回的是目标信息，而非符号链接。
注意：如果未启用NTFS权限检查，Windows上的结果仅显示该条目是否被标记为只读。

### `[since 6.2] QString QFileInfo::junctionTarget() const`

**作用与语义：**

将NTFS交接点解析为其参考路径。
返回NTFS连接所指向目录的绝对路径，如果对象不是NTFS连接，则返回空字符串。
无法保证由NTFS连接命名的目录确实存在。

### `QDateTime QFileInfo::lastModified() const`

**作用与语义：**

返回文件最后修改的日期和时间。
如果文件是符号链接，该函数返回的是目标信息，而非符号链接。
该函数会超载 `QFileInfo::lastModified`（const QTimeZone &），返回与 `lastModified(QTimeZone::LocalTime)` 相同的结果。

### `[since 6.6] QDateTime QFileInfo::lastModified(const QTimeZone &tz) const`

**作用与语义：**

返回文件最后修改的日期和时间。
返回的时间位于`tz`指定的时区内。例如，你可以用`QTimeZone::LocalTime`或`QTimeZone::UTC`分别获取当地时区或UTC的时间。由于本地文件系统API通常使用UTC，使用`QTimeZone::UTC`通常更快，因为它不需要任何转换。
如果文件是符号链接，该函数返回的是目标信息，而非符号链接。

### `QDateTime QFileInfo::lastRead() const`

**作用与语义：**

返回文件最后一次读取（访问）的日期和时间。
在没有这些信息的平台上，会与`lastModified()`同时返回。
如果文件是符号链接，该函数返回的是目标信息，而非符号链接。
该函数会超载 `QFileInfo::lastRead`（const QTimeZone &），返回与 `lastRead(QTimeZone::LocalTime)` 相同的结果。

### `[since 6.6] QDateTime QFileInfo::lastRead(const QTimeZone &tz) const`

**作用与语义：**

返回文件最后一次读取（访问）的日期和时间。
返回的时间位于`tz`指定的时区内。例如，你可以用`QTimeZone::LocalTime`或`QTimeZone::UTC`分别获取本地时区或UTC时间。由于本地文件系统API通常使用UTC，使用`QTimeZone::UTC`通常更快，因为它不需要转换。
在没有这些信息的平台上，会与`lastModified()`时间相同返回。
如果文件是符号链接，该函数返回的是目标信息，而非符号链接。

### `bool QFileInfo::makeAbsolute()`

**作用与语义：**

如果文件系统条目的路径是相对的，该方法将其转换为绝对路径并返回`true`;如果路径本身是绝对的，则返回`false`。

### `QDateTime QFileInfo::metadataChangeTime() const`

**作用与语义：**

返回文件元数据最后更改的日期和时间，以当地时间计算。
元数据变更发生在文件首次创建时，但用户写入或设置 inode 信息（例如更改文件权限）时也会发生。
如果文件是符号链接，该函数返回的是目标信息，而非符号链接。
该函数会超载 QFileInfo：：metadataChangeTime（const `QTimeZone` &tz），并返回与 `metadataChangeTime(QTimeZone::LocalTime)` 相同的结果。

### `[since 6.6] QDateTime QFileInfo::metadataChangeTime(const QTimeZone &tz) const`

**作用与语义：**

返回文件元数据最后更改的日期和时间。元数据变更发生在文件首次创建时，但用户写入或设置 inode 信息（例如更改文件权限）时也会发生。
返回的时间位于`tz`指定的时区内。例如，你可以用`QTimeZone::LocalTime`或`QTimeZone::UTC`分别获得本地时区或UTC时间。由于本地文件系统API通常使用UTC，使用`QTimeZone::UTC`通常更快，因为它不需要转换。
如果文件是符号链接，该函数返回的是目标信息，而非符号链接。

### `QString QFileInfo::owner() const`

**作用与语义：**

返回文件所有者。在文件没有所有者的系统中，或发生错误时，返回一个空字符串。
在 Unix 下，这个函数可能耗时（以毫秒为单位）。在 Windows 上，除非启用 NTFS 权限检查，否则会返回空字符串。
如果文件是符号链接，该函数返回的是目标信息，而非符号链接。

### `uint QFileInfo::ownerId() const`

**作用与语义：**

返回文件所有者的ID。
在Windows及文件无所有者的系统中，该功能返回（（uint）-2）。
如果文件是符号链接，该函数返回的是目标信息，而非符号链接。

### `QString QFileInfo::path() const`

**作用与语义：**

返回该`QFileInfo`所指文件系统条目的路径，但不包含条目名称。
注意：如果该`QFileInfo`的路径以目录分隔符`'/'`结尾，则条目名称部分视为空。此时，该函数返回整条路径。

### `bool QFileInfo::permission(QFileDevice::Permissions permissions) const`

**作用与语义：**

测试文件权限。`permissions` 参数可以是多种 QFile::Permissions 类型的标志按位或组合，用于检查权限组合。
在文件没有权限的系统上，此函数始终返回 `true`。
注意：如果未启用 NTFS 权限检查，在 Windows 上结果可能不准确。
如果文件是符号链接，该函数返回关于目标的信息，而不是符号链接本身。

**官方示例：**

```cpp
 QFileInfo fi("/tmp/archive.tar.gz");
 if (fi.permission(QFile::WriteUser | QFile::ReadGroup))
     qWarning("I can change the file; my group can read the file");
 if (fi.permission(QFile::WriteGroup | QFile::WriteOther))
     qWarning("The group or others can change the file");
```

### `QFileDevice::Permissions QFileInfo::permissions() const`

**作用与语义：**

返回文件中完整的 OR-ed 组合的 QFile：:P ermissions。
注意：如果未启用NTFS权限检查，Windows上结果可能不准确。
如果文件是符号链接，该函数返回的是目标信息，而非符号链接。

### `[since 6.6] QString QFileInfo::readSymLink() const`

**作用与语义：**

阅读符号链接所提到的路径。
返回符号链接所引用的原始路径，但不解析相对于包含符号链接的目录的相对路径。只有当符号链接实际引用该字符串时，返回的字符串才是绝对路径。如果对象不是符号链接，返回空字符串。

### `void QFileInfo::refresh()`

**作用与语义：**

刷新该`QFileInfo`所指的文件系统条目信息，即在下一次抓取缓存属性时从文件系统读取信息。

### `void QFileInfo::setCaching(bool enable)`

**作用与语义：**

如果`enable`为真，则启用文件信息缓存。如果`enable`为假，则禁用缓存。
启用缓存时，`QFileInfo`会在第一次需要时读取文件系统的信息，但通常不会在之后读取。
缓存默认是启用的。

### `void QFileInfo::setFile(const QString &path)`

**作用与语义：**

将该`QFileInfo`提供信息的文件系统条目路径设置为`path`路径，路径可以是绝对的也可以是相对的。
在 Unix 上，绝对路径以目录分隔符 `'/'` 开头。在 Windows 上，绝对路径以驱动器规范开头（例如 `D:/`）。
相对路径以目录名或普通文件名开头，指定文件系统条目相对于当前工作目录的路径。

**官方示例：**

```cpp
 QFileInfo info("/usr/bin/env");

 QString path = info.absolutePath(); // path = /usr/bin
 QString base = info.baseName(); // base = env

 info.setFile("/etc/hosts");

 path = info.absolutePath(); // path = /etc
 base = info.baseName(); // base = hosts
```

### `[since 6.0] void QFileInfo::setFile(const std::filesystem::path &path)`

**作用与语义：**

设置该`QFileInfo`提供信息的文件系统条目路径`path`。
如果`path`是相对的，`QFileInfo`也会有相对路径。

### `void QFileInfo::setFile(const QFileDevice &file)`

**作用与语义：**

设置`QFileInfo`提供信息的文件给`file`。
如果`file`包含相对路径，`QFileInfo`也会有相对路径。

### `void QFileInfo::setFile(const QDir &dir, const QString &path)`

**作用与语义：**

设置该`QFileInfo`提供信息的文件系统条目路径，`path`目录`dir`。
如果`dir`有相对路径，`QFileInfo`也会有相对路径。
如果`path`是绝对的，那么由`dir`指定的目录将被忽略。

### `qint64 QFileInfo::size() const`

**作用与语义：**

返回文件大小（字节单位）。如果文件不存在或无法获取，则返回 0。
如果文件是符号链接，该函数返回的是目标信息，而非符号链接。

### `[since 6.0] void QFileInfo::stat()`

**作用与语义：**

读取文件系统中的所有属性。
当文件系统信息在工作线程中收集，然后以缓存`QFileInfo`实例的形式传递给界面时，这非常有用。

### `QString QFileInfo::suffix() const`

**作用与语义：**

返回文件的后缀（扩展名）。
后缀包含文件中最后一个“.”之后（但不包括）所有字符。
文件的后缀在所有平台上均等计算，独立于文件命名惯例（例如，Unix上的“.bashrc”基础名为空，后缀为“bashrc”）。

**官方示例：**

```cpp
 QFileInfo fi("/tmp/archive.tar.gz");
 QString ext = fi.suffix();  // ext = "gz"
```

### `[noexcept] void QFileInfo::swap(QFileInfo &other)`

**作用与语义：**

将这些文件信息与`other`交换。这个操作非常快，而且从未失败过。

### `QString QFileInfo::symLinkTarget() const`

**作用与语义：**

返回符号链接指向的文件或目录的绝对路径，如果对象不是符号链接，则返回空字符串。
这个名称可能不代表已有的文件;它只是一个字符串。
注意：如果符号链接指向已有目标，则`exists()`返回`true`，否则返回`false`。

### `[noexcept] QFileInfo &QFileInfo::operator=(QFileInfo &&other)`

**作用与语义：**

Move-assign `other`到这个`QFileInfo`实例。

### `QFileInfo &QFileInfo::operator=(const QFileInfo &fileinfo)`

**作用与语义：**

复制给定`fileinfo`并分配给该`QFileInfo`。

### `QFileInfoList`

**作用与语义：**

`QList`的同义词<`QFileInfo`>。

### `[noexcept] bool operator!=(const QFileInfo &lhs, const QFileInfo &rhs)`

**作用与语义：**

如果 `QFileInfo` `lhs` 指向的文件系统条目与 `rhs` 指向的不同，则返回 `true`；否则返回 `false`。

### `[noexcept] bool operator==(const QFileInfo &lhs, const QFileInfo &rhs)`

**作用与语义：**

如果 `QFileInfo` `lhs` 和 `QFileInfo` `rhs` 参考文件系统中的同一条目，则返回 `true`；否则返回 `false`。
注意，比较两个不包含文件系统条目引用（路径不存在或为空）的空 `QFileInfo` 对象的结果是未定义的。
警告：这不会比较指向相同目标的两个不同符号链接。
警告：在 Windows 上，指向同一文件系统条目的长路径和短路径将被视为引用不同条目。

### `[since 6.0] QT_IMPLICIT_QFILEINFO_CONSTRUCTION`

**作用与语义：**

定义该宏使大多数`QFileInfo`构造器成为隐式而非显式。由于构建`QFileInfo`对象成本高昂，应避免意外创建它们，尤其是当存在更便宜的替代方案时。例如：
相反，请使用正确的API：
通过直接初始化而非复制初始化，总能从`QString`、`QFile`等方式构造：
此宏的提供是为了兼容性考虑。不建议在新代码中使用。
该宏在Qt 6.0中引入。

**官方示例：**

```cpp
 QDirIterator it(dir);
 while (it.hasNext()) {
     // Implicit conversion from QString (returned by it.next()):
     // may create unnecessary data structures and cause additional
     // accesses to the file system. Unless this macro is defined,
     // this line does not compile.

     QFileInfo fi = it.next();

     ~~~
 }
```

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

`QFileInfo` 所属机制类型：文件、设备与流机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
