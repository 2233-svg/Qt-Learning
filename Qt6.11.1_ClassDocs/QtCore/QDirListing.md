# QDirListing

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QDirListing` 是 文件、设备与流机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QDirListing` 是 文件、设备与流机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 文件和 I/O 类型把路径/设备描述与打开后的读写状态分开。打开模式决定可执行的操作，当前位置、缓冲区、文本编码、权限和错误状态共同决定一次读写是否正确。

**适用场景：** 构造稳定路径，选择正确的 OpenMode，检查 open 和 errorString，按数据规模使用流式读写或分块处理，明确文本编码，完成后关闭并处理失败。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要手写平台分隔符；不要默认相对路径指向程序目录；不要把本地编码、UTF-8 和二进制混在一起；写文件时要考虑临时文件、覆盖、权限和原子替换。

## 2. 依赖与对象关系

- 头文件：`#include <QDirListing>`
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

### 公有类型

- `class DirEntry`
- `(since 6.8) class const_iterator`
- `(since 6.8) class sentinel`
- `enum class IteratorFlag { Default, ExcludeFiles, ExcludeDirs, ExcludeOther, ResolveSymlinks, …, FollowDirSymlinks }`
- `flags IteratorFlags`

### 公有函数

- `QDirListing(const QString &path, QDirListing::IteratorFlags flags = IteratorFlag::Default)`
- `QDirListing(const QString &path, const QStringList &nameFilters, QDirListing::IteratorFlags flags = IteratorFlag::Default)`
- `QDirListing(QDirListing &&other)`
- `~QDirListing()`
- `QDirListing::const_iterator begin() const`
- `QDirListing::const_iterator cbegin() const`
- `QDirListing::sentinel cend() const`
- `QDirListing::sentinel end() const`
- `QDirListing::IteratorFlags iteratorFlags() const`
- `QString iteratorPath() const`
- `QStringList nameFilters() const`
- `QDirListing & operator=(QDirListing &&other)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum class QDirListing::IteratorFlagflags QDirListing::IteratorFlags`

**作用与语义：**

该枚举类描述了可用于配置`QDirListing`行为的标志。该枚举器的值可以按位或组合。
- `QDirListing::IteratorFlag::Default`：`0x000000`;列出所有条目，即文件、目录、符号链接（包括失效的符号链接（目标不存在）和特殊（其他）系统文件，详情请参见“排除其他”。隐藏文件和目录以及特殊条目`.`和`..`默认不列出。
- `QDirListing::IteratorFlag::ExcludeFiles`：`0x000004`;不要列出普通文件。与 ResolveSymlinks 结合时，也会排除指向普通文件的符号链接。
- `QDirListing::IteratorFlag::ExcludeDirs`：`0x000008`;不要列出目录。与 ResolveSymlinks 结合时，指向目录的符号链接也会被排除。
- `QDirListing::IteratorFlag::ExcludeOther`：`0x000010`;[自6.10版本起]不要列出非目录、非普通文件或符号链接的文件系统条目。
在Unix上，一个特殊的（其他）文件系统条目是FIFO、套接字、字符设备或块设备。更多细节请参见`mknod`手册页面。
在Windows上（出于历史原因），`.lnk`文件被视为特殊的（其他）文件系统条目。
- `QDirListing::IteratorFlag::ResolveSymlinks`：`0x000020`;根据链接目标类型过滤符号链接，而非符号链接本身。不存在目标的断裂符号链接被排除，设置 IncludeBrokenSymlinks 以包含它们。该标志在不支持符号链接的操作系统上被忽略。
- `QDirListing::IteratorFlag::IncludeBrokenSymlinks`：`0x001000`;[自6.11起]列出断裂的符号链接，目标不存在，无论ResolveSymlinks标志的状态如何。该标志在不支持符号链接的操作系统上被忽略。
- `QDirListing::IteratorFlag::FilesOnly`：`ExcludeDirs | ExcludeOther`;只列出普通文件。与 ResolveSymlinks 结合时，也会列出指向文件的符号链接。
- `QDirListing::IteratorFlag::DirsOnly`：`ExcludeFiles | ExcludeOther`;仅列出目录。与 ResolveSymlinks 结合时，符号链接也会被列出。
- `QDirListing::IteratorFlag::IncludeHidden`：`0x000040`;列出隐藏条目。当与递归结合时，迭代也会递归到隐藏子目录。
- `QDirListing::IteratorFlag::IncludeDotAndDotDot`：`0x000080`;列出`.`和`..`特别条目。
- `QDirListing::IteratorFlag::CaseSensitive`：`0x000100`;传给 `QDirListing` 构造函数的名称过滤器中的文件 glob 模式将以大小写区分匹配（详情见 `QDir::setNameFilters()`）。
- `QDirListing::IteratorFlag::Recursive`：`0x000400`;所有子目录中的条目也包含列表。结合FollowDirSymlinks时，符号链接也会迭代。
- `QDirListing::IteratorFlag::FollowDirSymlinks`：`0x000800`;与递归结合时，符号链接到目录也会被迭代。符号链环（例如，link => .或link =>..）会自动检测并忽略。
IteratorFlags 类型是 QFlags 的 typedef<IteratorFlag>。它存储 IteratorFlag 值的 OR 组合。

### `[explicit] QDirListing::QDirListing(const QString &path, QDirListing::IteratorFlags flags = IteratorFlag::Default)`

**作用与语义：**

构建一个可以迭代 `path` 的 QDirListing。
你可以通过`flags`传递选项，控制目录的迭代方式。
默认情况下，`flags`是`IteratorFlag::Default`。

### `[explicit] QDirListing::QDirListing(const QString &path, const QStringList &nameFilters, QDirListing::IteratorFlags flags = IteratorFlag::Default)`

**作用与语义：**

构建一个可以迭代`path`的QDirListing。
你可以通过`flags`传递选项，控制目录的迭代方式。默认情况下，`flags`是`IteratorFlag::Default`。
列出的条目将根据文件中的`nameFilters`颗粒模式进行过滤，这些模式通过`QRegularExpression::fromWildcard`转换为正则表达式（详见 `QDir::setNameFilters()` 详情）。
例如，以下迭代器可用于对音频文件进行迭代：
有时通过使用范围的 for 循环，使用字符串比较，可以更高效地按名称过滤。例如：

**官方示例：**

```cpp
 QDirListing audioFileIt(u"/home/johndoe/"_s, QStringList{u"*.mp3"_s, u"*.wav"_s},
                         QDirListing::IteratorFlag::FilesOnly);
```

### `[noexcept] QDirListing::QDirListing(QDirListing &&other)`

**作用与语义：**

移动构造器。移动`other`进入此QDirListing。
注意：移出对象 `other` 处于部分成形状态，唯一有效的操作是销毁和赋值。

### `[noexcept] QDirListing::~QDirListing()`

**作用与语义：**

摧毁了`QDirListing`。

### `QDirListing::sentinel QDirListing::cend() const`

**作用与语义：**

(c)`begin()` 返回一个可用于遍历目录条目的 `QDirListing::const_iterator`。
- 这是一个只能向前的、单次遍历迭代器（不能逆向遍历目录条目）
- 不能复制，只能 `std::move()`。
- 对模拟 `std::input_iterator` 的对象进行后置递增操作的返回值是部分构造的（一个已经前进的迭代器的副本），对这种对象的唯一有效操作是销毁和赋值一个新的迭代器。因此后置递增操作会前进迭代器并返回 `void`。
- 不允许随机访问
- 可用于范围 for 循环；或与不要求随机访问迭代器的 C 20 std::ranges 算法一起使用
- 对有效迭代器解引用返回 `const DirEntry &`
- (c)`end()` 返回一个表示迭代结束的 `QDirListing::sentinel`。解引用一个与 `end()` 相等的迭代器是未定义行为
注意：每次在同一 `QDirListing` 对象上调用 (c)`begin()` 时，内部状态都会被重置，迭代从头开始。
（上述一些限制由底层系统库函数的实现决定）。
以下是如何递归查找并读取按名称过滤的所有文件：
注意：“经典”STL 算法不支持迭代器/哨兵，因此需要使用 C 20 std::ranges 算法进行 `QDirListing`，或者使用提供基于范围算法的 C 17 第三方库。

**官方示例：**

```cpp
 using ItFlag = QDirListing::IteratorFlag;
 for (const auto &dirEntry : QDirListing(u"/etc"_s, ItFlag::Recursive)) {
     qDebug() << dirEntry.filePath();
     // /etc/.
     // /etc/..
     // /etc/X11
     // /etc/X11/fs
     // ...
 }
```

### `QDirListing::IteratorFlags QDirListing::iteratorFlags() const`

**作用与语义：**

返回用于构造该`QDirListing`的`IteratorFlags`集合。

### `QString QDirListing::iteratorPath() const`

**作用与语义：**

返回用于构建该`QDirListing`的目录路径。

### `QStringList QDirListing::nameFilters() const`

**作用与语义：**

返回用于构造该`QDirListing`的文件名glob过滤器列表。

### `[noexcept] QDirListing &QDirListing::operator=(QDirListing &&other)`

**作用与语义：**

Move-Assign `other`到这个`QDirListing`。
注意：移出对象 `other` 处于部分成形状态，唯一有效的操作是销毁和赋予新值。

### `class DirEntry`

**作用与语义：**

解引用有效`QDirListing::const_iterator`返回一个 DirEntry 对象。
DirEntry 提供了 `QFileInfo` API 的一个子集（例如 `fileName()`、`filePath()`、`exists()`）。在内部，DirEntry 只有在需要时才构建一个`QFileInfo`对象，也就是说，当信息尚未被其他系统函数获取时。你可以用 `DirEntry::fileInfo()` 来获取一个`QFileInfo`。例如：

**官方示例：**

```cpp
 using ItFlag = QDirListing::IteratorFlag;
 for (const auto &dirEntry : QDirListing(u"/etc"_s, ItFlag::Recursive)) {
     // Faster
     if (dirEntry.fileName().endsWith(u".conf")) { /* ... */ }

     // This works, but might be potentially slower, since it has to construct a
     // QFileInfo, whereas (depending on the implementation) the fileName could
     // be known already
     if (dirEntry.fileInfo().fileName().endsWith(u".conf")) { /* ... */ }
 }
 using ItFlag = QDirListing::IteratorFlag;
 for (const auto &dirEntry : QDirListing(u"/etc"_s, ItFlag::Recursive)) {
     // Both approaches are the same, because DirEntry will have to construct
     // a QFileInfo to get this info (for example, by calling system stat())

     if (dirEntry.size() >= 4'000 /* 4KB */) { /* ...*/ }
     if (dirEntry.fileInfo().size() >= 4'000 /* 4KB */) { /* ... */ }
 }
```

### `(since 6.8) class const_iterator`

**作用与语义：**

迭代类型返回`QDirListing::cbegin()`。
- 这是一个仅前向、单次遍历的迭代器（不能按反向顺序迭代目录条目）
- 无法复制，只能复制`std::move()`d。
- 对`std::input_iterator`建模对象的后增值返回值是部分形成的（即已推进迭代器的复制品），此类对象唯一有效的操作是销毁和赋予新的迭代器。因此，增量后算符推进迭代器并返回`void`。
- 不允许随机访问
- 可用于 ranged-for 循环;或用于不需要随机访问迭代器的 C 20 std：：range 算法
- 取消引用有效的迭代器返回`const DirEntry &`
- （c）`end()` 返回一个`QDirListing::sentinel`，表示迭代结束。取消引用一个迭代器比较等于 `end()` 是未定义行为
注意：“经典”STL算法不支持迭代器/哨兵，因此你需要使用C 20标准：：ranges算法来处理`QDirListing`，或者使用第三方库提供基于范围的C 17算法。

### `(since 6.8) class sentinel`

**作用与语义：**

`QDirListing`返回此类对象，表示迭代结束。对等于 `sentinel{}` 的`QDirListing::const_iterator`进行解引用是未定义行为。
注意：“经典”STL算法不支持迭代器/哨兵，因此你需要使用C 20标准：：ranges算法来进行`QDirListing`，或者使用第三方库提供基于范围的C 17算法。

### `enum class IteratorFlag { Default, ExcludeFiles, ExcludeDirs, ExcludeOther, ResolveSymlinks, …, FollowDirSymlinks }`

**作用与语义：**

该枚举类描述了可用于配置`QDirListing`行为的标志。该枚举器的值可以按位或组合。
- `QDirListing::IteratorFlag::Default`：`0x000000`;列出所有条目，即文件、目录、符号链接（包括失效的符号链接（目标不存在）和特殊（其他）系统文件，详情请参见“排除其他”。隐藏文件和目录以及特殊条目`.`和`..`默认不列出。
- `QDirListing::IteratorFlag::ExcludeFiles`：`0x000004`;不要列出普通文件。与 ResolveSymlinks 结合时，也会排除指向普通文件的符号链接。
- `QDirListing::IteratorFlag::ExcludeDirs`：`0x000008`;不要列出目录。与 ResolveSymlinks 结合时，指向目录的符号链接也会被排除。
- `QDirListing::IteratorFlag::ExcludeOther`：`0x000010`;[自6.10版本起]不要列出非目录、非普通文件或符号链接的文件系统条目。
在Unix上，一个特殊的（其他）文件系统条目是FIFO、套接字、字符设备或块设备。更多细节请参见`mknod`手册页面。
在Windows上（出于历史原因），`.lnk`文件被视为特殊的（其他）文件系统条目。
- `QDirListing::IteratorFlag::ResolveSymlinks`：`0x000020`;根据链接目标类型过滤符号链接，而非符号链接本身。不存在目标的断裂符号链接被排除，设置 IncludeBrokenSymlinks 以包含它们。该标志在不支持符号链接的操作系统上被忽略。
- `QDirListing::IteratorFlag::IncludeBrokenSymlinks`：`0x001000`;[自6.11起]列出断裂的符号链接，目标不存在，无论ResolveSymlinks标志的状态如何。该标志在不支持符号链接的操作系统上被忽略。
- `QDirListing::IteratorFlag::FilesOnly`：`ExcludeDirs | ExcludeOther`;只列出普通文件。与 ResolveSymlinks 结合时，也会列出指向文件的符号链接。
- `QDirListing::IteratorFlag::DirsOnly`：`ExcludeFiles | ExcludeOther`;仅列出目录。与 ResolveSymlinks 结合时，符号链接也会被列出。
- `QDirListing::IteratorFlag::IncludeHidden`：`0x000040`;列出隐藏条目。当与递归结合时，迭代也会递归到隐藏子目录。
- `QDirListing::IteratorFlag::IncludeDotAndDotDot`：`0x000080`;列出`.`和`..`特别条目。
- `QDirListing::IteratorFlag::CaseSensitive`：`0x000100`;传给 `QDirListing` 构造函数的名称过滤器中的文件 glob 模式将以大小写区分匹配（详情见 `QDir::setNameFilters()`）。
- `QDirListing::IteratorFlag::Recursive`：`0x000400`;所有子目录中的条目也包含列表。结合FollowDirSymlinks时，符号链接也会迭代。
- `QDirListing::IteratorFlag::FollowDirSymlinks`：`0x000800`;与递归结合时，符号链接到目录也会被迭代。符号链环（例如，link => .或link =>..）会自动检测并忽略。
IteratorFlags 类型是 QFlags 的 typedef<IteratorFlag>。它存储 IteratorFlag 值的 OR 组合。

### `flags IteratorFlags`

**作用与语义：**

该枚举类描述了可用于配置`QDirListing`行为的标志。该枚举器的值可以按位或组合。
- `QDirListing::IteratorFlag::Default`：`0x000000`;列出所有条目，即文件、目录、符号链接（包括失效的符号链接（目标不存在）和特殊（其他）系统文件，详情请参见“排除其他”。隐藏文件和目录以及特殊条目`.`和`..`默认不列出。
- `QDirListing::IteratorFlag::ExcludeFiles`：`0x000004`;不要列出普通文件。与 ResolveSymlinks 结合时，也会排除指向普通文件的符号链接。
- `QDirListing::IteratorFlag::ExcludeDirs`：`0x000008`;不要列出目录。与 ResolveSymlinks 结合时，指向目录的符号链接也会被排除。
- `QDirListing::IteratorFlag::ExcludeOther`：`0x000010`;[自6.10版本起]不要列出非目录、非普通文件或符号链接的文件系统条目。
在Unix上，一个特殊的（其他）文件系统条目是FIFO、套接字、字符设备或块设备。更多细节请参见`mknod`手册页面。
在Windows上（出于历史原因），`.lnk`文件被视为特殊的（其他）文件系统条目。
- `QDirListing::IteratorFlag::ResolveSymlinks`：`0x000020`;根据链接目标类型过滤符号链接，而非符号链接本身。不存在目标的断裂符号链接被排除，设置 IncludeBrokenSymlinks 以包含它们。该标志在不支持符号链接的操作系统上被忽略。
- `QDirListing::IteratorFlag::IncludeBrokenSymlinks`：`0x001000`;[自6.11起]列出断裂的符号链接，目标不存在，无论ResolveSymlinks标志的状态如何。该标志在不支持符号链接的操作系统上被忽略。
- `QDirListing::IteratorFlag::FilesOnly`：`ExcludeDirs | ExcludeOther`;只列出普通文件。与 ResolveSymlinks 结合时，也会列出指向文件的符号链接。
- `QDirListing::IteratorFlag::DirsOnly`：`ExcludeFiles | ExcludeOther`;仅列出目录。与 ResolveSymlinks 结合时，符号链接也会被列出。
- `QDirListing::IteratorFlag::IncludeHidden`：`0x000040`;列出隐藏条目。当与递归结合时，迭代也会递归到隐藏子目录。
- `QDirListing::IteratorFlag::IncludeDotAndDotDot`：`0x000080`;列出`.`和`..`特别条目。
- `QDirListing::IteratorFlag::CaseSensitive`：`0x000100`;传给 `QDirListing` 构造函数的名称过滤器中的文件 glob 模式将以大小写区分匹配（详情见 `QDir::setNameFilters()`）。
- `QDirListing::IteratorFlag::Recursive`：`0x000400`;所有子目录中的条目也包含列表。结合FollowDirSymlinks时，符号链接也会迭代。
- `QDirListing::IteratorFlag::FollowDirSymlinks`：`0x000800`;与递归结合时，符号链接到目录也会被迭代。符号链环（例如，link => .或link =>..）会自动检测并忽略。
IteratorFlags 类型是 QFlags 的 typedef<IteratorFlag>。它存储 IteratorFlag 值的 OR 组合。

### `QDirListing::const_iterator begin() const`

**作用与语义：**

(c)`begin()` 返回一个可用于遍历目录条目的 `QDirListing::const_iterator`。
- 这是一个只能向前的、单次遍历迭代器（不能逆向遍历目录条目）
- 不能复制，只能 `std::move()`。
- 对模拟 `std::input_iterator` 的对象进行后置递增操作的返回值是部分构造的（一个已经前进的迭代器的副本），对这种对象的唯一有效操作是销毁和赋值一个新的迭代器。因此后置递增操作会前进迭代器并返回 `void`。
- 不允许随机访问
- 可用于范围 for 循环；或与不要求随机访问迭代器的 C 20 std::ranges 算法一起使用
- 对有效迭代器解引用返回 `const DirEntry &`
- (c)`end()` 返回一个表示迭代结束的 `QDirListing::sentinel`。解引用一个与 `end()` 相等的迭代器是未定义行为
注意：每次在同一 `QDirListing` 对象上调用 (c)`begin()` 时，内部状态都会被重置，迭代从头开始。
（上述一些限制由底层系统库函数的实现决定）。
以下是如何递归查找并读取按名称过滤的所有文件：
注意：“经典”STL 算法不支持迭代器/哨兵，因此需要使用 C 20 std::ranges 算法进行 `QDirListing`，或者使用提供基于范围算法的 C 17 第三方库。

**官方示例：**

```cpp
 using ItFlag = QDirListing::IteratorFlag;
 for (const auto &dirEntry : QDirListing(u"/etc"_s, ItFlag::Recursive)) {
     qDebug() << dirEntry.filePath();
     // /etc/.
     // /etc/..
     // /etc/X11
     // /etc/X11/fs
     // ...
 }
```

### `QDirListing::const_iterator cbegin() const`

**作用与语义：**

(c)`begin()` 返回一个可用于遍历目录条目的 `QDirListing::const_iterator`。
- 这是一个只能向前的、单次遍历迭代器（不能逆向遍历目录条目）
- 不能复制，只能 `std::move()`。
- 对模拟 `std::input_iterator` 的对象进行后置递增操作的返回值是部分构造的（一个已经前进的迭代器的副本），对这种对象的唯一有效操作是销毁和赋值一个新的迭代器。因此后置递增操作会前进迭代器并返回 `void`。
- 不允许随机访问
- 可用于范围 for 循环；或与不要求随机访问迭代器的 C 20 std::ranges 算法一起使用
- 对有效迭代器解引用返回 `const DirEntry &`
- (c)`end()` 返回一个表示迭代结束的 `QDirListing::sentinel`。解引用一个与 `end()` 相等的迭代器是未定义行为
注意：每次在同一 `QDirListing` 对象上调用 (c)`begin()` 时，内部状态都会被重置，迭代从头开始。
（上述一些限制由底层系统库函数的实现决定）。
以下是如何递归查找并读取按名称过滤的所有文件：
注意：“经典”STL 算法不支持迭代器/哨兵，因此需要使用 C 20 std::ranges 算法进行 `QDirListing`，或者使用提供基于范围算法的 C 17 第三方库。

**官方示例：**

```cpp
 using ItFlag = QDirListing::IteratorFlag;
 for (const auto &dirEntry : QDirListing(u"/etc"_s, ItFlag::Recursive)) {
     qDebug() << dirEntry.filePath();
     // /etc/.
     // /etc/..
     // /etc/X11
     // /etc/X11/fs
     // ...
 }
```

### `QDirListing::sentinel end() const`

**作用与语义：**

(c)`begin()` 返回一个可用于遍历目录条目的 `QDirListing::const_iterator`。
- 这是一个只能向前的、单次遍历迭代器（不能逆向遍历目录条目）
- 不能复制，只能 `std::move()`。
- 对模拟 `std::input_iterator` 的对象进行后置递增操作的返回值是部分构造的（一个已经前进的迭代器的副本），对这种对象的唯一有效操作是销毁和赋值一个新的迭代器。因此后置递增操作会前进迭代器并返回 `void`。
- 不允许随机访问
- 可用于范围 for 循环；或与不要求随机访问迭代器的 C 20 std::ranges 算法一起使用
- 对有效迭代器解引用返回 `const DirEntry &`
- (c)`end()` 返回一个表示迭代结束的 `QDirListing::sentinel`。解引用一个与 `end()` 相等的迭代器是未定义行为
注意：每次在同一 `QDirListing` 对象上调用 (c)`begin()` 时，内部状态都会被重置，迭代从头开始。
（上述一些限制由底层系统库函数的实现决定）。
以下是如何递归查找并读取按名称过滤的所有文件：
注意：“经典”STL 算法不支持迭代器/哨兵，因此需要使用 C 20 std::ranges 算法进行 `QDirListing`，或者使用提供基于范围算法的 C 17 第三方库。

**官方示例：**

```cpp
 using ItFlag = QDirListing::IteratorFlag;
 for (const auto &dirEntry : QDirListing(u"/etc"_s, ItFlag::Recursive)) {
     qDebug() << dirEntry.filePath();
     // /etc/.
     // /etc/..
     // /etc/X11
     // /etc/X11/fs
     // ...
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

`QDirListing` 所属机制类型：文件、设备与流机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
