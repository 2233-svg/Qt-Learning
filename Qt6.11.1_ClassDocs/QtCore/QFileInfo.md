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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 86 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `QFileInfo::QFileInfo()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFileInfo` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QFileInfo::QFileInfo(const QFileDevice &file)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFileInfo` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `file`：类型为 `const QFileDevice &`。没有默认值，调用时必须提供。文件或设备对象。要确认打开状态、读写模式、当前位置和错误状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QFileInfo::QFileInfo(const QString &path)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFileInfo` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `path`：类型为 `const QString &`。没有默认值，调用时必须提供。路径字符串。要确认是相对路径还是绝对路径，以及它相对于哪个工作目录。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] QFileInfo::QFileInfo(const std::filesystem::path &file)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFileInfo` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `file`：类型为 `const std::filesystem::path &`。没有默认值，调用时必须提供。文件或设备对象。要确认打开状态、读写模式、当前位置和错误状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QFileInfo::QFileInfo(const QDir &dir, const QString &path)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFileInfo` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `dir`：类型为 `const QDir &`。没有默认值，调用时必须提供。传入 `const QDir &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `path`：类型为 `const QString &`。没有默认值，调用时必须提供。路径字符串。要确认是相对路径还是绝对路径，以及它相对于哪个工作目录。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] QFileInfo::QFileInfo(const QDir &dir, const std::filesystem::path &path)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFileInfo` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `dir`：类型为 `const QDir &`。没有默认值，调用时必须提供。传入 `const QDir &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `path`：类型为 `const std::filesystem::path &`。没有默认值，调用时必须提供。路径字符串。要确认是相对路径还是绝对路径，以及它相对于哪个工作目录。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFileInfo::QFileInfo(const QFileInfo &fileinfo)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFileInfo` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `fileinfo`：类型为 `const QFileInfo &`。没有默认值，调用时必须提供。传入 `const QFileInfo &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QFileInfo::~QFileInfo()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFileInfo` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDir QFileInfo::absoluteDir() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileInfo::absoluteDir` 用于计算、查询或取得与“absolute、Dir”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDir`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDir`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QFileInfo::absoluteFilePath() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileInfo::absoluteFilePath` 用于计算、查询或取得与“absolute、File、Path”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QFileInfo::absolutePath() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileInfo::absolutePath` 用于计算、查询或取得与“absolute、Path”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QFileInfo::baseName() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileInfo::baseName` 用于计算、查询或取得与“base、名称”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDateTime QFileInfo::birthTime() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileInfo::birthTime` 用于计算、查询或取得与“birth、时间”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDateTime`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] QDateTime QFileInfo::birthTime(const QTimeZone &tz) const`

**API 类别：** 成员函数说明

**中文解读：** `QFileInfo::birthTime` 用于计算、查询或取得与“birth、时间”相关的操作。调用时要先确认当前状态和 `tz` 的有效范围；返回类型是 `QDateTime`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数 `tz`：类型为 `const QTimeZone &`。没有默认值，调用时必须提供。传入 `const QTimeZone &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QFileInfo::bundleName() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileInfo::bundleName` 用于计算、查询或取得与“bundle、名称”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFileInfo::caching() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileInfo::caching` 用于计算、查询或取得与“caching”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QFileInfo::canonicalFilePath() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `canonicalFilePath`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QFileInfo::canonicalPath() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `canonicalPath`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QFileInfo::completeBaseName() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileInfo::completeBaseName` 用于计算、查询或取得与“complete、Base、名称”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QFileInfo::completeSuffix() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileInfo::completeSuffix` 用于计算、查询或取得与“complete、Suffix”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDir QFileInfo::dir() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileInfo::dir` 用于计算、查询或取得与“dir”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDir`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDir`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFileInfo::exists() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `exists`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] bool QFileInfo::exists(const QString &path)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `exists`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数 `path`：类型为 `const QString &`。没有默认值，调用时必须提供。路径字符串。要确认是相对路径还是绝对路径，以及它相对于哪个工作目录。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QFileInfo::fileName() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileInfo::fileName` 用于计算、查询或取得与“file、名称”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QFileInfo::filePath() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileInfo::filePath` 用于计算、查询或取得与“file、Path”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDateTime QFileInfo::fileTime(QFileDevice::FileTime time) const`

**API 类别：** 成员函数说明

**中文解读：** `QFileInfo::fileTime` 用于计算、查询或取得与“file、时间”相关的操作。调用时要先确认当前状态和 `time` 的有效范围；返回类型是 `QDateTime`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数 `time`：类型为 `QFileDevice::FileTime`。没有默认值，调用时必须提供。传入 `QFileDevice::FileTime` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] QDateTime QFileInfo::fileTime(QFileDevice::FileTime time, const QTimeZone &tz) const`

**API 类别：** 成员函数说明

**中文解读：** `QFileInfo::fileTime` 用于计算、查询或取得与“file、时间”相关的操作。调用时要先确认当前状态和 `time`、`tz` 的有效范围；返回类型是 `QDateTime`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数 `time`：类型为 `QFileDevice::FileTime`。没有默认值，调用时必须提供。传入 `QFileDevice::FileTime` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `tz`：类型为 `const QTimeZone &`。没有默认值，调用时必须提供。传入 `const QTimeZone &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] std::filesystem::path QFileInfo::filesystemAbsoluteFilePath() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileInfo::filesystemAbsoluteFilePath` 用于计算、查询或取得与“filesystem、Absolute、File、Path”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `std::filesystem::path`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`std::filesystem::path`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] std::filesystem::path QFileInfo::filesystemAbsolutePath() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileInfo::filesystemAbsolutePath` 用于计算、查询或取得与“filesystem、Absolute、Path”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `std::filesystem::path`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`std::filesystem::path`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] std::filesystem::path QFileInfo::filesystemCanonicalFilePath() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileInfo::filesystemCanonicalFilePath` 用于计算、查询或取得与“filesystem、Canonical、File、Path”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `std::filesystem::path`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`std::filesystem::path`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] std::filesystem::path QFileInfo::filesystemCanonicalPath() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileInfo::filesystemCanonicalPath` 用于计算、查询或取得与“filesystem、Canonical、Path”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `std::filesystem::path`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`std::filesystem::path`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] std::filesystem::path QFileInfo::filesystemFilePath() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileInfo::filesystemFilePath` 用于计算、查询或取得与“filesystem、File、Path”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `std::filesystem::path`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`std::filesystem::path`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] std::filesystem::path QFileInfo::filesystemJunctionTarget() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileInfo::filesystemJunctionTarget` 用于计算、查询或取得与“filesystem、Junction、目标”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `std::filesystem::path`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`std::filesystem::path`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] std::filesystem::path QFileInfo::filesystemPath() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileInfo::filesystemPath` 用于计算、查询或取得与“filesystem、Path”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `std::filesystem::path`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`std::filesystem::path`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] std::filesystem::path QFileInfo::filesystemReadSymLink() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileInfo::filesystemReadSymLink` 用于计算、查询或取得与“filesystem、读取、Sym、Link”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `std::filesystem::path`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`std::filesystem::path`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] std::filesystem::path QFileInfo::filesystemSymLinkTarget() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileInfo::filesystemSymLinkTarget` 用于计算、查询或取得与“filesystem、Sym、Link、目标”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `std::filesystem::path`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`std::filesystem::path`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QFileInfo::group() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileInfo::group` 用于计算、查询或取得与“group”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `uint QFileInfo::groupId() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileInfo::groupId` 用于计算、查询或取得与“group、Id”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `uint`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`uint`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFileInfo::isAbsolute() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isAbsolute`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.4] bool QFileInfo::isAlias() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isAlias`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFileInfo::isBundle() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isBundle`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFileInfo::isDir() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isDir`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFileInfo::isExecutable() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isExecutable`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFileInfo::isFile() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isFile`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFileInfo::isHidden() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isHidden`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFileInfo::isJunction() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isJunction`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFileInfo::isNativePath() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isNativePath`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.10] bool QFileInfo::isOther() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isOther`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFileInfo::isReadable() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isReadable`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFileInfo::isRelative() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isRelative`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFileInfo::isRoot() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isRoot`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFileInfo::isShortcut() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isShortcut`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFileInfo::isSymLink() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isSymLink`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFileInfo::isSymbolicLink() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isSymbolicLink`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFileInfo::isWritable() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isWritable`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] QString QFileInfo::junctionTarget() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileInfo::junctionTarget` 用于计算、查询或取得与“junction、目标”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDateTime QFileInfo::lastModified() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileInfo::lastModified` 用于计算、查询或取得与“末项、Modified”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDateTime`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] QDateTime QFileInfo::lastModified(const QTimeZone &tz) const`

**API 类别：** 成员函数说明

**中文解读：** `QFileInfo::lastModified` 用于计算、查询或取得与“末项、Modified”相关的操作。调用时要先确认当前状态和 `tz` 的有效范围；返回类型是 `QDateTime`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数 `tz`：类型为 `const QTimeZone &`。没有默认值，调用时必须提供。传入 `const QTimeZone &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDateTime QFileInfo::lastRead() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileInfo::lastRead` 用于计算、查询或取得与“末项、读取”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDateTime`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] QDateTime QFileInfo::lastRead(const QTimeZone &tz) const`

**API 类别：** 成员函数说明

**中文解读：** `QFileInfo::lastRead` 用于计算、查询或取得与“末项、读取”相关的操作。调用时要先确认当前状态和 `tz` 的有效范围；返回类型是 `QDateTime`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数 `tz`：类型为 `const QTimeZone &`。没有默认值，调用时必须提供。传入 `const QTimeZone &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFileInfo::makeAbsolute()`

**API 类别：** 成员函数说明

**中文解读：** `QFileInfo::makeAbsolute` 用于计算、查询或取得与“make、Absolute”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDateTime QFileInfo::metadataChangeTime() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileInfo::metadataChangeTime` 用于计算、查询或取得与“metadata、Change、时间”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDateTime`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] QDateTime QFileInfo::metadataChangeTime(const QTimeZone &tz) const`

**API 类别：** 成员函数说明

**中文解读：** `QFileInfo::metadataChangeTime` 用于计算、查询或取得与“metadata、Change、时间”相关的操作。调用时要先确认当前状态和 `tz` 的有效范围；返回类型是 `QDateTime`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数 `tz`：类型为 `const QTimeZone &`。没有默认值，调用时必须提供。传入 `const QTimeZone &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QFileInfo::owner() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileInfo::owner` 用于计算、查询或取得与“owner”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `uint QFileInfo::ownerId() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileInfo::ownerId` 用于计算、查询或取得与“owner、Id”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `uint`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`uint`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QFileInfo::path() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileInfo::path` 用于计算、查询或取得与“path”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFileInfo::permission(QFileDevice::Permissions permissions) const`

**API 类别：** 成员函数说明

**中文解读：** `QFileInfo::permission` 用于计算、查询或取得与“permission”相关的操作。调用时要先确认当前状态和 `permissions` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `permissions`：类型为 `QFileDevice::Permissions`。没有默认值，调用时必须提供。传入 `QFileDevice::Permissions` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFileDevice::Permissions QFileInfo::permissions() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileInfo::permissions` 用于计算、查询或取得与“permissions”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QFileDevice::Permissions`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QFileDevice::Permissions`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] QString QFileInfo::readSymLink() const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFileInfo` 的核心操作 `readSymLink`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 要区分 EOF、暂时无数据和错误；大文件优先分块读取。

### `void QFileInfo::refresh()`

**API 类别：** 成员函数说明

**中文解读：** `QFileInfo::refresh` 用于执行与“refresh”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFileInfo::setCaching(bool enable)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setCaching`。调用它会改变 `QFileInfo` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enable`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFileInfo::setFile(const QString &path)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFile`。调用它会改变 `QFileInfo` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `path`：类型为 `const QString &`。没有默认值，调用时必须提供。路径字符串。要确认是相对路径还是绝对路径，以及它相对于哪个工作目录。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] void QFileInfo::setFile(const std::filesystem::path &path)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFile`。调用它会改变 `QFileInfo` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `path`：类型为 `const std::filesystem::path &`。没有默认值，调用时必须提供。路径字符串。要确认是相对路径还是绝对路径，以及它相对于哪个工作目录。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFileInfo::setFile(const QFileDevice &file)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFile`。调用它会改变 `QFileInfo` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `file`：类型为 `const QFileDevice &`。没有默认值，调用时必须提供。文件或设备对象。要确认打开状态、读写模式、当前位置和错误状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFileInfo::setFile(const QDir &dir, const QString &path)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFile`。调用它会改变 `QFileInfo` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `dir`：类型为 `const QDir &`。没有默认值，调用时必须提供。传入 `const QDir &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `path`：类型为 `const QString &`。没有默认值，调用时必须提供。路径字符串。要确认是相对路径还是绝对路径，以及它相对于哪个工作目录。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qint64 QFileInfo::size() const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `size`，返回 `QFileInfo` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`qint64`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] void QFileInfo::stat()`

**API 类别：** 成员函数说明

**中文解读：** `QFileInfo::stat` 用于执行与“stat”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QFileInfo::suffix() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileInfo::suffix` 用于计算、查询或取得与“suffix”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] void QFileInfo::swap(QFileInfo &other)`

**API 类别：** 成员函数说明

**中文解读：** `QFileInfo::swap` 用于执行与“swap”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `other`：类型为 `QFileInfo &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QFileInfo::symLinkTarget() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileInfo::symLinkTarget` 用于计算、查询或取得与“sym、Link、目标”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QFileInfo &QFileInfo::operator=(QFileInfo &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFileInfo` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QFileInfo &`。
- 参数 `other`：类型为 `QFileInfo &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFileInfo &QFileInfo::operator=(const QFileInfo &fileinfo)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFileInfo` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QFileInfo &`。
- 参数 `fileinfo`：类型为 `const QFileInfo &`。没有默认值，调用时必须提供。传入 `const QFileInfo &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFileInfoList`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QFileInfo` 的 `Q、File、Info、List` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator!=(const QFileInfo &lhs, const QFileInfo &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QFileInfo` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QFileInfo &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QFileInfo &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator==(const QFileInfo &lhs, const QFileInfo &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QFileInfo` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QFileInfo &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QFileInfo &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] QT_IMPLICIT_QFILEINFO_CONSTRUCTION`

**API 类别：** 宏说明

**中文解读：** 这是 `QFileInfo` 的 `CONSTRUCTION` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

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
