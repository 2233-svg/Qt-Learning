# QDir

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QDir` 是目录路径和目录内容操作工具，用于遍历、过滤、创建和拼接目录。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QDir` 是目录路径和目录内容操作工具，用于遍历、过滤、创建和拼接目录。

**内部模型：** QDir 是轻量的路径操作值类型，不负责长期持有目录句柄。先使用 absolutePath/filePath 形成稳定路径，再用 entryInfoList 获取带元数据的目录项。

**适用场景：** 查找文件、扫描资源目录、创建输出目录、拼接跨平台路径时使用。

**典型调用链：** 确定根目录 -> exists/mkpath 验证或创建 -> entryList/entryInfoList 过滤 -> filePath 拼接子路径 -> 交给 QFile/QFileInfo。

**先记住的坑：** 不要手写反斜杠拼路径；不要把文件名过滤器误当正则表达式；遍历结果可能为空，权限错误要结合 QFileInfo 和应用逻辑处理。

## 2. 依赖与对象关系

- 头文件：`#include <QDir>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

QDir 是轻量的路径操作值类型，不负责长期持有目录句柄。先使用 absolutePath/filePath 形成稳定路径，再用 entryInfoList 获取带元数据的目录项。

### 状态、生命周期和线程

**生命周期：** 先设置路径或设备，再 open，成功后读写/定位/刷新，最后 close；析构通常会关闭设备，但关键写入应显式 flush/close 并检查错误。相对路径依赖当前工作目录，资源路径和用户文件路径要区分。

**状态与结果：** 区分设备未打开、打开成功、到达 EOF、暂时无数据、读写失败和写入尚未落盘。`readAll()` 方便小数据但可能占用大量内存，大文件应分块处理并检查返回值。

**线程与事件循环：** 同一个打开设备不要跨线程并发使用，除非类明确保证线程安全；后台 I/O 通过 worker 或异步设备处理，GUI 线程只接收结果。

## 3. 直接使用

查找文件、扫描资源目录、创建输出目录、拼接跨平台路径时使用。 使用时通常按这个过程组织：确定根目录 -> exists/mkpath 验证或创建 -> entryList/entryInfoList 过滤 -> filePath 拼接子路径 -> 交给 QFile/QFileInfo。

```cpp
#include <QDir>

QDir directory(QStringLiteral("docs"));
directory.mkpath(QStringLiteral("."));
const QStringList files = directory.entryList({QStringLiteral("*.md")},
                                                QDir::Files, QDir::Name);
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum Filter { Dirs, AllDirs, Files, Drives, NoSymLinks, …, CaseSensitive }`
- `flags Filters`
- `enum SortFlag { Name, Time, Size, Type, Unsorted, …, LocaleAware }`
- `flags SortFlags`

### 公有函数

- `QDir(const QString &path = QString())`
- `(since 6.0) QDir(const std::filesystem::path &path)`
- `QDir(const QString &path, const QString &nameFilter, QDir::SortFlags sort = SortFlags(Name | IgnoreCase), QDir::Filters filters = AllEntries)`
- `(since 6.0) QDir(const std::filesystem::path &path, const QString &nameFilter, QDir::SortFlags sort = SortFlags(Name | IgnoreCase), QDir::Filters filters = AllEntries)`
- `QDir(const QDir &dir)`
- `~QDir()`
- `QString absoluteFilePath(const QString &fileName) const`
- `QString absolutePath() const`
- `QString canonicalPath() const`
- `bool cd(const QString &dirName)`
- `bool cdUp()`
- `qsizetype count() const`
- `QString dirName() const`
- `QFileInfoList entryInfoList(const QStringList &nameFilters, QDir::Filters filters = NoFilter, QDir::SortFlags sort = NoSort) const`
- `QFileInfoList entryInfoList(QDir::Filters filters = NoFilter, QDir::SortFlags sort = NoSort) const`
- `QStringList entryList(const QStringList &nameFilters, QDir::Filters filters = NoFilter, QDir::SortFlags sort = NoSort) const`
- `QStringList entryList(QDir::Filters filters = NoFilter, QDir::SortFlags sort = NoSort) const`
- `bool exists(const QString &name) const`
- `bool exists() const`
- `QString filePath(const QString &fileName) const`
- `(since 6.0) std::filesystem::path filesystemAbsolutePath() const`
- `(since 6.0) std::filesystem::path filesystemCanonicalPath() const`
- `(since 6.0) std::filesystem::path filesystemPath() const`
- `QDir::Filters filter() const`
- `bool isAbsolute() const`
- `bool isEmpty(QDir::Filters filters = Filters(AllEntries | NoDotAndDotDot)) const`
- `bool isReadable() const`
- `bool isRelative() const`
- `bool isRoot() const`
- `bool makeAbsolute()`
- `bool mkdir(const QString &dirName, std::optional<QFileDevice::Permissions> permissions = std::nullopt) const`
- `bool mkpath(const QString &dirPath, std::optional<QFileDevice::Permissions> permissions = std::nullopt) const`
- `QStringList nameFilters() const`
- `QString path() const`
- `void refresh() const`
- `QString relativeFilePath(const QString &fileName) const`
- `bool remove(const QString &fileName)`
- `bool removeRecursively()`
- `bool rename(const QString &oldName, const QString &newName)`
- `bool rmdir(const QString &dirName) const`
- `bool rmpath(const QString &dirPath) const`
- `void setFilter(QDir::Filters filters)`
- `void setNameFilters(const QStringList &nameFilters)`
- `void setPath(const QString &path)`
- `(since 6.0) void setPath(const std::filesystem::path &path)`
- `void setSorting(QDir::SortFlags sort)`
- `QDir::SortFlags sorting() const`
- `void swap(QDir &other)`
- `QDir & operator=(QDir &&other)`
- `QDir & operator=(const QDir &dir)`
- `QString operator[](qsizetype pos) const`

### 静态公有成员

- `void addSearchPath(const QString &prefix, const QString &path)`
- `(since 6.0) void addSearchPath(const QString &prefix, const std::filesystem::path &path)`
- `QString cleanPath(const QString &path)`
- `QDir current()`
- `QString currentPath()`
- `QFileInfoList drives()`
- `QString fromNativeSeparators(const QString &pathName)`
- `QDir home()`
- `QString homePath()`
- `bool isAbsolutePath(const QString &path)`
- `bool isRelativePath(const QString &path)`
- `QChar listSeparator()`
- `bool match(const QString &filter, const QString &fileName)`
- `bool match(const QStringList &filters, const QString &fileName)`
- `QDir root()`
- `QString rootPath()`
- `QStringList searchPaths(const QString &prefix)`
- `QChar separator()`
- `bool setCurrent(const QString &path)`
- `void setSearchPaths(const QString &prefix, const QStringList &searchPaths)`
- `QDir temp()`
- `QString tempPath()`
- `QString toNativeSeparators(const QString &pathName)`

### 相关非成员函数

- `bool operator!=(const QDir &lhs, const QDir &rhs)`
- `bool operator==(const QDir &lhs, const QDir &rhs)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QDir::Filterflags QDir::Filters`

**作用与语义：**

该枚举描述了`QDir`可用的过滤选项;例如针对`entryList()`和`entryInfoList()`。过滤值通过使用按位的 OR 运算符将以下列表中的值组合来指定：
- `QDir::Dirs`：`0x001`;列出与筛选条件匹配的目录。
- `QDir::AllDirs`：`0x400`;列出所有目录;即不对目录名称应用筛选。
- `QDir::Files`：`0x002`;列表文件。
- `QDir::Drives`：`0x004`;列出磁盘驱动器（Unix下忽略）。
- `QDir::NoSymLinks`：`0x008`;不列出符号链接（不支持符号链接的操作系统忽略此链接）。
- `QDir::NoDotAndDotDot`：`NoDot | NoDotDot`;不要列出特殊条目“.”和“..”。
- `QDir::NoDot`：`0x2000`;不要列出特殊条目“.”。
- `QDir::NoDotDot`：`0x4000`;不要列出特殊条目“..”。
- `QDir::AllEntries`：`Dirs | Files | Drives`;列出目录、文件、驱动器和符号链接（除非指定系统，否则不列出故障的符号链接）。
- `QDir::Readable`：`0x010`;列出应用程序可读取的文件。可读值需要与 Dirs 或文件结合。
- `QDir::Writable`：`0x020`;列出应用程序有写权限的文件。可写值需要与 Dirs 或 Files 结合。
- `QDir::Executable`：`0x040`;列出应用程序拥有执行权限的文件。可执行值需要与 Dir 或文件合并。
- `QDir::Hidden`：`0x100`;列出隐藏文件（Unix 上，文件以“.”开头）。
- `QDir::System`：`0x200`;列表系统文件（Unix上包含FIFO、套接字和设备文件;Windows上包含`.lnk`文件）
- `QDir::CaseSensitive`：`0x800`;滤波器应区分大小写。
使用Filter enum值来过滤文件和目录列表的函数，除非你设置了NoSymLinks值，否则会包含指向文件和目录的符号链接。
默认构造`QDir`不会根据权限过滤文件，因此`entryList()`和`entryInfoList()`会返回所有可读、可写、可执行或三者任意组合的文件。这使得默认文件易于编写，同时又实用。
例如，设置`Readable`、`Writable`和`Files`标志，可以列出所有应用程序拥有读、写或两者都有权限的文件。如果`Dirs`和`Drives`标志也包含在该组合中，那么所有驱动器、目录、应用程序可以读取、写入或执行的文件，以及这些文件/目录的符号链接都可以列出。
要获取目录权限，使用`entryInfoList()`函数获取关联的`QFileInfo`对象，然后用`QFileInfo::permissions()`获取每个文件的权限和所有权。
Filters类型是QFlags的typedef<Filter>。它存储一组或组合的滤波器值。

### `enum QDir::SortFlagflags QDir::SortFlags`

**作用与语义：**

此枚举描述了 `QDir` 可用的排序选项，例如用于 `entryList()` 和 `entryInfoList()`。排序值是通过将以下列表中的值按位 OR 运算指定的：
- `QDir::Name`: `0x00`；按名称排序。
- `QDir::Time`: `0x01`；按时间（修改时间）排序。
- `QDir::Size`: `0x02`；按文件大小排序。
- `QDir::Type`: `0x80`；按文件类型（扩展名）排序。
- `QDir::Unsorted`: `0x03`；不排序。
- `QDir::NoSort`: `-1`；默认不排序。
- `QDir::DirsFirst`: `0x04`；先列出目录，再列出文件。
- `QDir::DirsLast`: `0x20`；先列出文件，再列出目录。
- `QDir::Reversed`: `0x08`；颠倒排序顺序。
- `QDir::IgnoreCase`: `0x10`；不区分大小写排序。
- `QDir::LocaleAware`: `0x40`；使用当前语言环境设置适当地排序项目。
您只能指定前四项中的一个。
如果同时指定 DirsFirst 和 Reversed，则目录仍然先列出，但顺序反转；文件将列在目录之后，同样以反向顺序排列。
SortFlags 类型是 QFlags<SortFlag> 的类型定义。它存储 SortFlag 值的按位 OR 组合。

### `QDir::QDir(const QString &path = QString())`

**作用与语义：**

构建指向指定目录`path`的QDir。如果路径为空，则使用程序的工作目录（“.”）。

### `[since 6.0] QDir::QDir(const std::filesystem::path &path)`

**作用与语义：**

构建指向指定目录`path`的QDir。如果路径为空，则使用程序的工作目录（“.”）。

### `QDir::QDir(const QString &path, const QString &nameFilter, QDir::SortFlags sort = SortFlags(Name | IgnoreCase), QDir::Filters filters = AllEntries)`

**作用与语义：**

构建一个路径为`path`的QDir，用`nameFilter`过滤条目，用`filters`筛选属性。它还用`sort`排序名称。
默认`nameFilter`是空字符串，不排除任何东西;默认`filters`是`AllEntries`，同样不排除任何东西。默认`sort`是`Name` |`IgnoreCase`，即按名称不区分大小写排序。
如果 `path` 是空字符串，QDir 使用 “.”（当前目录）。如果 `nameFilter` 是空字符串，QDir 使用名称过滤器 “*”（所有文件）。
注意：`path`不必存在。

### `[since 6.0] QDir::QDir(const std::filesystem::path &path, const QString &nameFilter, QDir::SortFlags sort = SortFlags(Name | IgnoreCase), QDir::Filters filters = AllEntries)`

**作用与语义：**

构建一个路径为`path`的QDir，通过名称（`nameFilter`）和属性（`filters`）进行筛选。它还用`sort`排序名称。
默认`nameFilter`是空字符串，不排除任何内容;默认`filters`是`AllEntries`，同样不排除任何内容。默认`sort`是`Name` |`IgnoreCase`，即按名称进行无分大小写排序。
如果`path`为空，QDir 使用 “.”（当前目录）。如果 `nameFilter` 是空字符串，QDir 使用名称过滤器 “*”（所有文件）。
注意：`path`不必存在。

### `QDir::QDir(const QDir &dir)`

**作用与语义：**

构建一个QDir对象，该对象是目录`dir`的QDir对象的复制品。

### `[noexcept] QDir::~QDir()`

**作用与语义：**

销毁`QDir`对象释放其资源。这对文件系统中的底层目录没有影响。

### `QString QDir::absoluteFilePath(const QString &fileName) const`

**作用与语义：**

返回目录中文件的绝对路径名称。不检查文件是否真实存在于目录中;但请参见`exists()`。`fileName`中的冗余多重分隔符或“..”目录不会被移除（参见 `cleanPath()`）。

### `QString QDir::absolutePath() const`

**作用与语义：**

返回绝对路径（以“/”或驱动器规范开头的路径），该路径可能包含符号链接，但绝不包含冗余的“.”、“..”或多个分隔符。

### `[static] void QDir::addSearchPath(const QString &prefix, const QString &path)`

**作用与语义：**

为`prefix`的搜索路径增加了`path`。

### `[static, since 6.0] void QDir::addSearchPath(const QString &prefix, const std::filesystem::path &path)`

**作用与语义：**

为`prefix`的搜索路径增加了`path`。

### `QString QDir::canonicalPath() const`

**作用与语义：**

返回规范路径，即没有符号链接或冗余“.”或“..”元素的路径。
在没有符号链接的系统中，该函数总是返回与`absolutePath()`返回的字符串相同。如果典范路径不存在（通常是由于悬挂符号链接），canonicalPath() 返回一个空字符串。

**官方示例：**

```cpp
 QString bin = "/local/bin";         // where /local/bin is a symlink to /usr/bin
 QDir binDir(bin);
 QString canonicalBin = binDir.canonicalPath();
 // canonicalBin now equals "/usr/bin"

 QString ls = "/local/bin/ls";       // where ls is the executable "ls"
 QDir lsDir(ls);
 QString canonicalLs = lsDir.canonicalPath();
 // canonicalLS now equals "/usr/bin/ls".
```

### `bool QDir::cd(const QString &dirName)`

**作用与语义：**

将`QDir`的目录改为`dirName`。
如果新目录存在，返回`true`;否则返回`false`。注意，如果新目录不存在，则不执行逻辑cd()操作。
调用 cd（“..”）等同于调用 `cdUp()`。

### `bool QDir::cdUp()`

**作用与语义：**

通过从`QDir`当前目录向上移动一个目录来更改目录。
如果新目录存在，返回`true`;否则返回`false`。注意，如果新目录不存在，则不执行逻辑cdUp()操作。
注意：在安卓平台上，内容URI不支持此功能。更多信息请参见DocumentFile.getParentFile()。

### `[static] QString QDir::cleanPath(const QString &path)`

**作用与语义：**

返回`path`目录分隔符归一化（即平台本地分隔符转换为“/”）并移除冗余分隔符，并“.”s和“..”尽可能地解析。
符号链接被保留。该函数不返回规范路径，而是返回输入的最简单版本。例如，“./local”变为“local”，“local/../bin”变为“bin”，“/local/usr/../bin”变为“/local/bin”。

### `qsizetype QDir::count() const`

**作用与语义：**

返回目录中目录和文件的总数。
相当于 `entryList()`.count()。
注意：在 6.5 之前的 Qt 版本中，该函数返回的是 `uint`，而非 `qsizetype`。

### `[static] QDir QDir::current()`

**作用与语义：**

返回应用当前目录。
目录是基于当前目录的绝对路径构建的，确保其`path()`与`absolutePath()`相同。

### `[static] QString QDir::currentPath()`

**作用与语义：**

返回应用当前目录的绝对路径。当前目录是最后一个带有`QDir::setCurrent()`的目录，或者如果从未调用过，则是父进程启动该应用程序的目录。

### `QString QDir::dirName() const`

**作用与语义：**

返回目录名称;这与路径不同，例如名为“mail”的目录可能有路径“/var/spool/mail”。如果目录没有名称（例如它是根目录），则返回空字符串。
没有检查是否真的存在带有该名称的目录;但请参见`exists()`。

### `[static] QFileInfoList QDir::drives()`

**作用与语义：**

返回该系统根目录列表。
在 Windows 上，它返回包含“C：/”、“D：/” 等的`QFileInfo`对象列表。但这不会返回带有可弹出介质且为空的驱动器。在其他操作系统上，它返回的列表仅包含一个根目录（即“/”）。

### `QFileInfoList QDir::entryInfoList(const QStringList &nameFilters, QDir::Filters filters = NoFilter, QDir::SortFlags sort = NoSort) const`

**作用与语义：**

返回目录中所有文件和目录的`QFileInfo`对象列表，按之前用 `setNameFilters()` 和 `setFilter()` 设置的名称和属性过滤器排序，并根据 `setSorting()` 设置的标志排序。
名称过滤器、文件属性过滤器和排序规范可以通过`nameFilters`、`filters`和`sort`参数来覆盖。
如果目录不可读、不存在或没有符合规范，则返回一个空列表。

### `QFileInfoList QDir::entryInfoList(QDir::Filters filters = NoFilter, QDir::SortFlags sort = NoSort) const`

**作用与语义：**

返回目录中所有文件和目录的`QFileInfo`对象列表，按之前用`setNameFilters()`和`setFilter()`设置的名称和属性过滤器排序，并根据`setSorting()`设置的标志排序。
属性过滤器和排序规范可以通过 `filters` 和 `sort` 参数来覆盖。
如果目录不可读、不存在或没有符合规范，则返回一个空列表。

### `QStringList QDir::entryList(const QStringList &nameFilters, QDir::Filters filters = NoFilter, QDir::SortFlags sort = NoSort) const`

**作用与语义：**

返回目录中所有文件和目录的名称列表，按之前用 `setNameFilters()` 和 `setFilter()` 设置的名称和属性过滤器排序，并根据 `setSorting()` 设置的标志排序。
名称过滤器、文件属性过滤器和排序规范可以通过`nameFilters`、`filters`和`sort`参数来覆盖。
如果目录不可读、不存在或没有符合规范，则返回一个空列表。

### `QStringList QDir::entryList(QDir::Filters filters = NoFilter, QDir::SortFlags sort = NoSort) const`

**作用与语义：**

返回目录中所有文件和目录的名称列表，按之前用 `setNameFilters()` 和 `setFilter()` 设置的名称和属性过滤器排序，并根据 `setSorting()` 设置的标志排序。
属性过滤器和排序规范可以通过`filters`和`sort`参数来覆盖。
如果目录不可读、不存在或没有符合规范，则返回一个空列表。
注意：要列出指向不存在文件的符号链接，必须`System`传递给过滤器。

### `bool QDir::exists(const QString &name) const`

**作用与语义：**

如果存在调用`name`的文件，返回`true`;否则返回 false。
除非`name`包含绝对文件路径，否则文件名通常相对于目录本身，因此通常用于检查目录中是否有文件。

### `bool QDir::exists() const`

**作用与语义：**

如果目录存在，返回 `true`;否则返回 `false`。（如果找到同名文件，该函数将返回 false。）。
该函数的重载接受参数用于测试目录中文件和目录的存在。

### `QString QDir::filePath(const QString &fileName) const`

**作用与语义：**

返回目录中文件的路径名称。不检查文件是否实际存在于目录中;但请参见`exists()`。如果`QDir`是相对的，返回的路径名称也会是相对的。`fileName`中的冗余多重分隔符或“.”和“..”目录不会被移除（参见 `cleanPath()`）。

### `[since 6.0] std::filesystem::path QDir::filesystemAbsolutePath() const`

**作用与语义：**

`absolutePath()`以`std::filesystem::path`身份回归。

### `[since 6.0] std::filesystem::path QDir::filesystemCanonicalPath() const`

**作用与语义：**

`canonicalPath()`以`std::filesystem::path`身份返回。

### `[since 6.0] std::filesystem::path QDir::filesystemPath() const`

**作用与语义：**

返回 `path()` 作为 `std::filesystem::path`。

### `QDir::Filters QDir::filter() const`

**作用与语义：**

返回由`setFilter()`设定的值。

### `[static] QString QDir::fromNativeSeparators(const QString &pathName)`

**作用与语义：**

使用 '/' 作为文件分隔符返回 `pathName`。例如，在 Windows 上，fromNativeSeparators("`c:\\winnt\\system32`") 返回 "c:/winnt/system32"。在某些操作系统上，返回的字符串可能与参数相同，例如在 Unix 上。

### `[static] QDir QDir::home()`

**作用与语义：**

返回用户的主目录。
目录是基于主目录的绝对路径构建的，确保其`path()`与`absolutePath()`相同。
详情请参见`homePath()`。

### `[static] QString QDir::homePath()`

**作用与语义：**

返回用户主目录的绝对路径。
在 Windows 下，该函数会返回当前用户配置文件的目录。通常，这包括：
使用`toNativeSeparators()`函数将分隔符转换为适合底层操作系统的分隔符。
如果当前用户配置文件的目录不存在或无法检索，将按给定顺序检查以下替代方案，直到找到现有且可用的路径：
- `USERPROFILE`环境变量指定的路径。
- 通过将`HOMEDRIVE`和`HOMEPATH`环境变量连接形成的路径。
- 由`HOME`环境变量指定的路径。
- `rootPath()`函数返回的路径（使用`SystemDrive`环境变量）
- `C:/`目录。
在非 Windows 操作系统中，如果环境变量存在，`HOME` 环境变量就会被使用，否则则使用`rootPath()`返回的路径。

**官方示例：**

```cpp
 C:/Users/Username
```

### `bool QDir::isAbsolute() const`

**作用与语义：**

如果目录的路径是绝对的，返回`true`;否则返回 `false`。参见`isAbsolutePath()`。
注意：以冒号（:) 开头的路径始终被视为绝对路径，因为它们表示一个`QResource`。

### `[static] bool QDir::isAbsolutePath(const QString &path)`

**作用与语义：**

如果`path`是绝对的，则返回`true`;如果是相对的，则返回`false`。
注意：以冒号（:) 开头的路径始终被视为绝对路径，因为它们表示`QResource`。

### `bool QDir::isEmpty(QDir::Filters filters = Filters(AllEntries | NoDotAndDotDot)) const`

**作用与语义：**

返回目录是否为空。
相当于带过滤器的`count() == 0` `QDir::AllEntries | QDir::NoDotAndDotDot`，但更快，因为它只是检查目录是否至少包含一个条目。
注意：除非你设置`filters`标志包含`QDir::NoDotAndDotDot`（默认数值是这样），否则没有哪个目录是空的。

### `bool QDir::isReadable() const`

**作用与语义：**

如果目录可读且能按名称打开文件，返回`true`;否则返回`false`。
警告：该函数的虚假值并不保证目录中的文件不可访问。

### `bool QDir::isRelative() const`

**作用与语义：**

如果目录路径是相对的，则返回`true`;否则返回false。（在Unix中，如果路径不以“/”开头，则是相对的。）。
注意：以冒号（:) 开头的路径始终被视为绝对路径，因为它们表示一个`QResource`。

### `[static] bool QDir::isRelativePath(const QString &path)`

**作用与语义：**

如果`path`是相对的，则返回`true`;如果是绝对的，则返回`false`。
注意：以冒号开头的路径（:)始终被视为绝对路径，因为它们表示`QResource`。

### `bool QDir::isRoot() const`

**作用与语义：**

如果该目录是根目录，返回`true`;否则返回`false`。
注意：如果目录是指向根目录的符号链接，该函数返回`false`。如果你想测试这一点，可以用`canonicalPath()`，例如：

**官方示例：**

```cpp
 QDir dir("/tmp/root_link");
 dir = dir.canonicalPath();
 if (dir.isRoot())
     qWarning("It is a root link");
```

### `[static constexpr noexcept] QChar QDir::listSeparator()`

**作用与语义：**

返回本地路径列表分隔符：Unix 下为 '：'，Windows 下为 ';'。

### `bool QDir::makeAbsolute()`

**作用与语义：**

将目录路径转换为绝对路径。如果已经是绝对路径，则不会发生任何事。如果转换成功，返回`true`;否则返回`false`。

### `[static] bool QDir::match(const QString &filter, const QString &fileName)`

**作用与语义：**

返回`true`如果`fileName`匹配通配符（glob）模式`filter`; 否则返回 `false`. `filter`可能包含由空格或分号分隔的多个模式。匹配不区分大小写。

### `[static] bool QDir::match(const QStringList &filters, const QString &fileName)`

**作用与语义：**

如果 `fileName` 与 `filters` 列表中的任何通配符（glob）模式匹配，则返回 `true`；否则返回 `false`。匹配不区分大小写。

### `bool QDir::mkdir(const QString &dirName, std::optional<QFileDevice::Permissions> permissions = std::nullopt) const`

**作用与语义：**

创建一个名为`dirName`的子目录，包含给定的`permissions`。
如果`permissions`是`std::nullopt`（默认），这个函数会设置默认权限。
成功时返回`true`;如果操作失败或`dirName`已存在，返回`false`。
如果`dirName`已经存在，这个方法不会改变它的权限。
在POSIX系统中，`permissions`会被当前进程的`umask`（文件创建掩码）修改，这意味着某些权限位可能会被禁用。
在 Windows 上，默认情况下，新目录会继承其父目录的权限。`permissions` 是通过 ACL 模拟的。当组获得的权限比其他组少时，这些 ACL 可能处于非规范顺序。当打开属性对话框的安全标签时，具有此类权限的文件和目录会生成警告。授予该组所有授予他人权限可以避免此类警告。
注意：Qt 6.10 增加了 `permissions` 参数。要实现旧的行为（使用默认平台权限），`mkdir(const QString &)` 将 `permissions` 设为 `std::nullopt`（默认）。这个新方法也透明地替换了 `mkdir(const QString &, QFile::Permissions)` 重载。

### `bool QDir::mkpath(const QString &dirPath, std::optional<QFileDevice::Permissions> permissions = std::nullopt) const`

**作用与语义：**

创建一个名为`dirPath`的目录。
如果`dirPath`尚不存在，此方法将创建它——以及任何不存在的父目录——并使用`permissions`。
如果`dirPath`已经存在，此方法不会更改其权限；对于任何已存在的父目录也是如此。
如果`permissions`为`std::nullopt`（默认值），此函数将设置默认权限。
成功时返回`true`，或者如果`dirPath`已存在也返回；否则返回`false`。
在POSIX系统上，`permissions`会被当前进程的`umask`（文件创建掩码）修改，这意味着某些权限位可能会被禁用。
在Windows上，默认情况下，新目录继承其父目录的权限。`permissions`通过ACL进行模拟。当组权限少于其他权限时，这些ACL可能不是规范顺序。具有此类权限的文件和目录在打开属性对话框的安全选项卡时会生成警告。授予组与其他人相同的所有权限可以避免此类警告。
注意：Qt 6.10添加了`permissions`参数。要获得旧行为（使用平台特定默认权限）的`mkpath(const QString &)`，将`permissions`设置为`std::nullopt`（默认）。

### `QStringList QDir::nameFilters() const`

**作用与语义：**

返回由`setNameFilters()`设置的字符串列表。

### `QString QDir::path() const`

**作用与语义：**

返回路径。这可能包含符号链接，但绝不包含冗余的“.”、“..”或多个分隔符。
返回路径可以是绝对路径或相对路径（见 `setPath()`）。

### `void QDir::refresh() const`

**作用与语义：**

刷新目录信息。

### `QString QDir::relativeFilePath(const QString &fileName) const`

**作用与语义：**

返回相对于目录的路径到`fileName`。

**官方示例：**

```cpp
 QDir dir("/home/bob");
 QString s;

 s = dir.relativeFilePath("images/file.jpg");     // s is "images/file.jpg"
 s = dir.relativeFilePath("/home/mary/file.txt"); // s is "../mary/file.txt"
```

### `bool QDir::remove(const QString &fileName)`

**作用与语义：**

删除文件，`fileName`。
如果文件成功移除，返回`true`;否则返回`false`。

### `bool QDir::removeRecursively()`

**作用与语义：**

移除目录，包括所有内容。
如果成功，则`true`，否则为假。
如果文件或目录无法被删除，removeRecursively() 会继续操作，尝试尽可能多地删除文件和子目录，然后返回`false`。
如果目录已被移除，方法返回`true`（预期结果已达）。
注意：该功能旨在删除小型应用内部目录（如临时目录），但不包括用户可见目录。对于用户可见操作，建议更精确地向用户报告错误，提供错误解决方案，显示删除过程中的进展，因为删除可能需要几分钟。

### `bool QDir::rename(const QString &oldName, const QString &newName)`

**作用与语义：**

将文件或目录从`oldName`重命名为`newName`，成功时返回true;否则返回`false`。
在大多数文件系统中，rename() 只有在 `oldName` 不存在或已有新名称的文件时才会失败。然而，rename() 也可能失败的其他原因。例如，在至少一个文件系统中，如果 `newName` 指向已打开的文件，rename() 会失败。
如果`oldName`是一个文件（不是目录），不能立即重命名，Qt 会尝试将`oldName`复制到 `newName` 并移除`oldName`。

### `bool QDir::rmdir(const QString &dirName) const`

**作用与语义：**

移除`dirName`指定的目录。
目录必须为空，rmdir() 才能成功。
成功时返回`true`;否则返回`false`。

### `bool QDir::rmpath(const QString &dirPath) const`

**作用与语义：**

移除目录路径`dirPath`。
该函数会移除`dirPath`中所有的父目录，前提是它们是空的。这与 mkpath（dirPath） 相反。
成功时返回`true`;成功时返回`false`。

### `[static] QDir QDir::root()`

**作用与语义：**

返回根目录。
目录是基于根目录的绝对路径构建的，确保其`path()`与`absolutePath()`相同。
详情请参见`rootPath()`。

### `[static] QString QDir::rootPath()`

**作用与语义：**

返回根目录的绝对路径。
对于 Unix 操作系统，这通常返回“/”。对于 Windows 文件系统，通常返回“c：/”。

### `[static] QStringList QDir::searchPaths(const QString &prefix)`

**作用与语义：**

返回`prefix`的搜索路径。

### `[static] QChar QDir::separator()`

**作用与语义：**

返回本地目录分隔符：Unix 下为“/”，Windows 为“\”。
你不需要用这个函数来构建文件路径。如果你总是使用“/”，Qt 会将你的路径转换到符合底层操作系统的标准。如果你想向使用操作系统分隔符的用户显示路径，请使用`toNativeSeparators()`。

### `[static] bool QDir::setCurrent(const QString &path)`

**作用与语义：**

将应用程序当前工作目录设置为 `path`。如果目录成功更改，返回`true`;否则返回 `false`。

**官方示例：**

```cpp
 QString absolute = "/local/bin";
 QString relative = "local/bin";
 QFileInfo absFile(absolute);
 QFileInfo relFile(relative);

 QDir::setCurrent(QDir::rootPath());
 // absFile and relFile now point to the same file

 QDir::setCurrent("/tmp");
 // absFile now points to "/local/bin",
 // while relFile points to "/tmp/local/bin"
```

### `void QDir::setFilter(QDir::Filters filters)`

**作用与语义：**

将`entryList()`和`entryInfoList()`使用的过滤器设置为`filters`。该过滤器用于指定`entryList()`和`entryInfoList()`应返回的文件类型。参见 `QDir::Filter`。

### `void QDir::setNameFilters(const QStringList &nameFilters)`

**作用与语义：**

将`entryList()`和`entryInfoList()`所使用的名称过滤器设置为`nameFilters`指定的过滤器列表。
每个名称过滤器是一个万用字（环形）过滤器，能够理解`*`和`?`万用符。详见`QRegularExpression::fromWildcard()`。
例如，以下代码在`QDir`上设置了三个名称过滤器，以确保只列出通常用于C源文件的扩展名文件：

**官方示例：**

```cpp
     QStringList filters;
     filters << "*.cpp" << "*.cxx" << "*.cc";
     dir.setNameFilters(filters);
```

### `void QDir::setPath(const QString &path)`

**作用与语义：**

将目录路径设置为`path`。路径被清除冗余的“.”、“..”以及多个分隔符。不会检查是否存在带有该路径的目录;但你可以自己用`exists()`检查。
路径可以是绝对的，也可以是相对的。绝对路径以目录分隔符“/”开头（在Windows下可选地前面加上驱动器规范）。相对文件名以目录名或文件名开头，并指定相对于当前目录的路径。绝对路径的一个例子是字符串“/tmp/quartz”，相对路径可能看起来像“src/fatlib”。

### `[since 6.0] void QDir::setPath(const std::filesystem::path &path)`

**作用与语义：**

将目录路径设置为`path`。路径被清除冗余的“.”、“..”以及多个分隔符。不会检查是否存在带有该路径的目录;但你可以自己用`exists()`检查。
路径可以是绝对的，也可以是相对的。绝对路径以目录分隔符“/”开头（在Windows下可选地前面加上驱动器规范）。相对文件名以目录名或文件名开头，并指定相对于当前目录的路径。绝对路径的一个例子是字符串“/tmp/quartz”，相对路径可能看起来像“src/fatlib”。

### `[static] void QDir::setSearchPaths(const QString &prefix, const QStringList &searchPaths)`

**作用与语义：**

将 Qt 的文件名搜索路径设置为前缀 `prefix` to `searchPaths`。
要指定文件名的前缀，请在前缀前加上一个冒号（例如，“images:undo.png”、“xmldocs:books.xml”）。`prefix`只能包含字母或数字（例如，不能包含冒号或斜杠）。
Qt 使用该搜索路径来定位已知前缀的文件。搜索路径条目按顺序测试，从第一个条目开始。
文件名前缀必须至少为2个字符，以避免与Windows驱动器代号冲突。
搜索路径可能包含通往 Qt 资源系统的路径。

**官方示例：**

```cpp
 QDir::setSearchPaths("icons", QStringList(QDir::homePath() + "/images"));
 QDir::setSearchPaths("docs", QStringList(":/embeddedDocuments"));
 //...
 QPixmap pixmap("icons:undo.png"); // will look for undo.png in QDir::homePath() + "/images"
 QFile file("docs:design.odf"); // will look in the :/embeddedDocuments resource path
```

### `void QDir::setSorting(QDir::SortFlags sort)`

**作用与语义：**

设置`entryList()`和`entryInfoList()`使用的排序顺序。
`sort`通过从枚举`QDir::SortFlag`中进行 OR 计算来指定。

### `QDir::SortFlags QDir::sorting() const`

**作用与语义：**

返回由`setSorting()`设定的值。

### `[noexcept] void QDir::swap(QDir &other)`

**作用与语义：**

将该`QDir`实例与`other`交换。该操作非常快且从未失败。

### `[static] QDir QDir::temp()`

**作用与语义：**

返回系统的临时目录。
目录是基于临时目录的绝对规范路径构建的，确保其`path()`与`absolutePath()`相同。
详情请参见`tempPath()`。

### `[static] QString QDir::tempPath()`

**作用与语义：**

返回系统临时目录的绝对规范路径。
在Unix/Linux系统中，这是`TMPDIR`环境变量中的路径，如果`TMPDIR`未定义，则为`/tmp`路径。在Windows上，这通常是`TEMP`或`TMP`环境变量中的路径。该方法返回的路径不会以目录分隔符结束，除非它是驱动器的根目录。

### `[static] QString QDir::toNativeSeparators(const QString &pathName)`

**作用与语义：**

返回`pathName`时，'/'分隔符转换为适合底层操作系统的分隔符。
在Windows上，toNativeSeparators（“c：/winnt/system32”）返回“c：\winnt\system32”。
返回的字符串可能与某些操作系统中的参数相同，例如在 Unix 系统中。

### `[noexcept] QDir &QDir::operator=(QDir &&other)`

**作用与语义：**

Move-assign `other`到该`QDir`实例。

### `QDir &QDir::operator=(const QDir &dir)`

**作用与语义：**

复制`dir`对象并将其分配给该`QDir`对象。

### `QString QDir::operator[](qsizetype pos) const`

**作用与语义：**

返回文件名列表中位置`pos`的文件名。等价于 `entryList()`.at（索引）。`pos`必须是列表中有效的索引位置（即0 <= pos < `count()`）。
注意：在6.5之前的Qt版本中，`pos`是`int`，不是`qsizetype`。

### `[noexcept] bool operator!=(const QDir &lhs, const QDir &rhs)`

**作用与语义：**

如果目录`lhs`和目录`rhs`有不同的路径或不同的排序或过滤设置，返回`true`;否则返回`false`。

**官方示例：**

```cpp
 // The current directory is "/usr/local"
 QDir d1("/usr/local/bin");
 d1.setFilter(QDir::Executable);
 QDir d2("bin");
 if (d1 != d2)
     qDebug("They differ");
```

### `[noexcept] bool operator==(const QDir &lhs, const QDir &rhs)`

**作用与语义：**

如果目录`lhs`和目录`rhs`拥有相同的路径且排序和过滤器设置相同，返回`true`;否则返回`false`。

**官方示例：**

```cpp
 // The current directory is "/usr/local"
 QDir d1("/usr/local/bin");
 QDir d2("bin");
 if (d1 == d2)
     qDebug("They're the same");
```

### `enum Filter { Dirs, AllDirs, Files, Drives, NoSymLinks, …, CaseSensitive }`

**作用与语义：**

该枚举描述了`QDir`可用的过滤选项;例如针对`entryList()`和`entryInfoList()`。过滤值通过使用按位的 OR 运算符将以下列表中的值组合来指定：
- `QDir::Dirs`：`0x001`;列出与筛选条件匹配的目录。
- `QDir::AllDirs`：`0x400`;列出所有目录;即不对目录名称应用筛选。
- `QDir::Files`：`0x002`;列表文件。
- `QDir::Drives`：`0x004`;列出磁盘驱动器（Unix下忽略）。
- `QDir::NoSymLinks`：`0x008`;不列出符号链接（不支持符号链接的操作系统忽略此链接）。
- `QDir::NoDotAndDotDot`：`NoDot | NoDotDot`;不要列出特殊条目“.”和“..”。
- `QDir::NoDot`：`0x2000`;不要列出特殊条目“.”。
- `QDir::NoDotDot`：`0x4000`;不要列出特殊条目“..”。
- `QDir::AllEntries`：`Dirs | Files | Drives`;列出目录、文件、驱动器和符号链接（除非指定系统，否则不列出故障的符号链接）。
- `QDir::Readable`：`0x010`;列出应用程序可读取的文件。可读值需要与 Dirs 或文件结合。
- `QDir::Writable`：`0x020`;列出应用程序有写权限的文件。可写值需要与 Dirs 或 Files 结合。
- `QDir::Executable`：`0x040`;列出应用程序拥有执行权限的文件。可执行值需要与 Dir 或文件合并。
- `QDir::Hidden`：`0x100`;列出隐藏文件（Unix 上，文件以“.”开头）。
- `QDir::System`：`0x200`;列表系统文件（Unix上包含FIFO、套接字和设备文件;Windows上包含`.lnk`文件）
- `QDir::CaseSensitive`：`0x800`;滤波器应区分大小写。
使用Filter enum值来过滤文件和目录列表的函数，除非你设置了NoSymLinks值，否则会包含指向文件和目录的符号链接。
默认构造`QDir`不会根据权限过滤文件，因此`entryList()`和`entryInfoList()`会返回所有可读、可写、可执行或三者任意组合的文件。这使得默认文件易于编写，同时又实用。
例如，设置`Readable`、`Writable`和`Files`标志，可以列出所有应用程序拥有读、写或两者都有权限的文件。如果`Dirs`和`Drives`标志也包含在该组合中，那么所有驱动器、目录、应用程序可以读取、写入或执行的文件，以及这些文件/目录的符号链接都可以列出。
要获取目录权限，使用`entryInfoList()`函数获取关联的`QFileInfo`对象，然后用`QFileInfo::permissions()`获取每个文件的权限和所有权。
Filters类型是QFlags的typedef<Filter>。它存储一组或组合的滤波器值。

### `flags Filters`

**作用与语义：**

该枚举描述了`QDir`可用的过滤选项;例如针对`entryList()`和`entryInfoList()`。过滤值通过使用按位的 OR 运算符将以下列表中的值组合来指定：
- `QDir::Dirs`：`0x001`;列出与筛选条件匹配的目录。
- `QDir::AllDirs`：`0x400`;列出所有目录;即不对目录名称应用筛选。
- `QDir::Files`：`0x002`;列表文件。
- `QDir::Drives`：`0x004`;列出磁盘驱动器（Unix下忽略）。
- `QDir::NoSymLinks`：`0x008`;不列出符号链接（不支持符号链接的操作系统忽略此链接）。
- `QDir::NoDotAndDotDot`：`NoDot | NoDotDot`;不要列出特殊条目“.”和“..”。
- `QDir::NoDot`：`0x2000`;不要列出特殊条目“.”。
- `QDir::NoDotDot`：`0x4000`;不要列出特殊条目“..”。
- `QDir::AllEntries`：`Dirs | Files | Drives`;列出目录、文件、驱动器和符号链接（除非指定系统，否则不列出故障的符号链接）。
- `QDir::Readable`：`0x010`;列出应用程序可读取的文件。可读值需要与 Dirs 或文件结合。
- `QDir::Writable`：`0x020`;列出应用程序有写权限的文件。可写值需要与 Dirs 或 Files 结合。
- `QDir::Executable`：`0x040`;列出应用程序拥有执行权限的文件。可执行值需要与 Dir 或文件合并。
- `QDir::Hidden`：`0x100`;列出隐藏文件（Unix 上，文件以“.”开头）。
- `QDir::System`：`0x200`;列表系统文件（Unix上包含FIFO、套接字和设备文件;Windows上包含`.lnk`文件）
- `QDir::CaseSensitive`：`0x800`;滤波器应区分大小写。
使用Filter enum值来过滤文件和目录列表的函数，除非你设置了NoSymLinks值，否则会包含指向文件和目录的符号链接。
默认构造`QDir`不会根据权限过滤文件，因此`entryList()`和`entryInfoList()`会返回所有可读、可写、可执行或三者任意组合的文件。这使得默认文件易于编写，同时又实用。
例如，设置`Readable`、`Writable`和`Files`标志，可以列出所有应用程序拥有读、写或两者都有权限的文件。如果`Dirs`和`Drives`标志也包含在该组合中，那么所有驱动器、目录、应用程序可以读取、写入或执行的文件，以及这些文件/目录的符号链接都可以列出。
要获取目录权限，使用`entryInfoList()`函数获取关联的`QFileInfo`对象，然后用`QFileInfo::permissions()`获取每个文件的权限和所有权。
Filters类型是QFlags的typedef<Filter>。它存储一组或组合的滤波器值。

### `enum SortFlag { Name, Time, Size, Type, Unsorted, …, LocaleAware }`

**作用与语义：**

此枚举描述了 `QDir` 可用的排序选项，例如用于 `entryList()` 和 `entryInfoList()`。排序值是通过将以下列表中的值按位 OR 运算指定的：
- `QDir::Name`: `0x00`；按名称排序。
- `QDir::Time`: `0x01`；按时间（修改时间）排序。
- `QDir::Size`: `0x02`；按文件大小排序。
- `QDir::Type`: `0x80`；按文件类型（扩展名）排序。
- `QDir::Unsorted`: `0x03`；不排序。
- `QDir::NoSort`: `-1`；默认不排序。
- `QDir::DirsFirst`: `0x04`；先列出目录，再列出文件。
- `QDir::DirsLast`: `0x20`；先列出文件，再列出目录。
- `QDir::Reversed`: `0x08`；颠倒排序顺序。
- `QDir::IgnoreCase`: `0x10`；不区分大小写排序。
- `QDir::LocaleAware`: `0x40`；使用当前语言环境设置适当地排序项目。
您只能指定前四项中的一个。
如果同时指定 DirsFirst 和 Reversed，则目录仍然先列出，但顺序反转；文件将列在目录之后，同样以反向顺序排列。
SortFlags 类型是 QFlags<SortFlag> 的类型定义。它存储 SortFlag 值的按位 OR 组合。

### `flags SortFlags`

**作用与语义：**

此枚举描述了 `QDir` 可用的排序选项，例如用于 `entryList()` 和 `entryInfoList()`。排序值是通过将以下列表中的值按位 OR 运算指定的：
- `QDir::Name`: `0x00`；按名称排序。
- `QDir::Time`: `0x01`；按时间（修改时间）排序。
- `QDir::Size`: `0x02`；按文件大小排序。
- `QDir::Type`: `0x80`；按文件类型（扩展名）排序。
- `QDir::Unsorted`: `0x03`；不排序。
- `QDir::NoSort`: `-1`；默认不排序。
- `QDir::DirsFirst`: `0x04`；先列出目录，再列出文件。
- `QDir::DirsLast`: `0x20`；先列出文件，再列出目录。
- `QDir::Reversed`: `0x08`；颠倒排序顺序。
- `QDir::IgnoreCase`: `0x10`；不区分大小写排序。
- `QDir::LocaleAware`: `0x40`；使用当前语言环境设置适当地排序项目。
您只能指定前四项中的一个。
如果同时指定 DirsFirst 和 Reversed，则目录仍然先列出，但顺序反转；文件将列在目录之后，同样以反向顺序排列。
SortFlags 类型是 QFlags<SortFlag> 的类型定义。它存储 SortFlag 值的按位 OR 组合。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先设置路径或设备，再 open，成功后读写/定位/刷新，最后 close；析构通常会关闭设备，但关键写入应显式 flush/close 并检查错误。相对路径依赖当前工作目录，资源路径和用户文件路径要区分。

### 状态和错误边界

区分设备未打开、打开成功、到达 EOF、暂时无数据、读写失败和写入尚未落盘。`readAll()` 方便小数据但可能占用大量内存，大文件应分块处理并检查返回值。

### 线程边界

同一个打开设备不要跨线程并发使用，除非类明确保证线程安全；后台 I/O 通过 worker 或异步设备处理，GUI 线程只接收结果。

### 最容易出现的错误

不要手写反斜杠拼路径；不要把文件名过滤器误当正则表达式；遍历结果可能为空，权限错误要结合 QFileInfo 和应用逻辑处理。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QDir` 所属机制类型：文件、设备与流机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
