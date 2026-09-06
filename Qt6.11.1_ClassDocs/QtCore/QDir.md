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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 82 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QDir::Filterflags QDir::Filters`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QDir` 暴露的类型声明 `Filterflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Filterflags QDir::Filters`。
- 属性名：`QDir`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QDir::SortFlagflags QDir::SortFlags`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QDir` 暴露的类型声明 `Sort、Flagflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:SortFlagflags QDir::SortFlags`。
- 属性名：`QDir`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDir::QDir(const QString &path = QString())`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDir` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `path`：类型为 `const QString &`。默认值为 `QString()`。路径字符串。要确认是相对路径还是绝对路径，以及它相对于哪个工作目录。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] QDir::QDir(const std::filesystem::path &path)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDir` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `path`：类型为 `const std::filesystem::path &`。没有默认值，调用时必须提供。路径字符串。要确认是相对路径还是绝对路径，以及它相对于哪个工作目录。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDir::QDir(const QString &path, const QString &nameFilter, QDir::SortFlags sort = SortFlags(Name | IgnoreCase), QDir::Filters filters = AllEntries)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDir` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `path`：类型为 `const QString &`。没有默认值，调用时必须提供。路径字符串。要确认是相对路径还是绝对路径，以及它相对于哪个工作目录。
- 参数 `nameFilter`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `sort`：类型为 `QDir::SortFlags`。默认值为 `SortFlags(Name | IgnoreCase)`。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `filters`：类型为 `QDir::Filters`。默认值为 `AllEntries`。传入 `QDir::Filters` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] QDir::QDir(const std::filesystem::path &path, const QString &nameFilter, QDir::SortFlags sort = SortFlags(Name | IgnoreCase), QDir::Filters filters = AllEntries)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDir` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `path`：类型为 `const std::filesystem::path &`。没有默认值，调用时必须提供。路径字符串。要确认是相对路径还是绝对路径，以及它相对于哪个工作目录。
- 参数 `nameFilter`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `sort`：类型为 `QDir::SortFlags`。默认值为 `SortFlags(Name | IgnoreCase)`。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `filters`：类型为 `QDir::Filters`。默认值为 `AllEntries`。传入 `QDir::Filters` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDir::QDir(const QDir &dir)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDir` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `dir`：类型为 `const QDir &`。没有默认值，调用时必须提供。传入 `const QDir &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QDir::~QDir()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDir` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QDir::absoluteFilePath(const QString &fileName) const`

**API 类别：** 成员函数说明

**中文解读：** `QDir::absoluteFilePath` 用于计算、查询或取得与“absolute、File、Path”相关的操作。调用时要先确认当前状态和 `fileName` 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数 `fileName`：类型为 `const QString &`。没有默认值，调用时必须提供。文件名或路径。优先使用 Qt 的路径 API 拼接和规范化，不要手写平台分隔符。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QDir::absolutePath() const`

**API 类别：** 成员函数说明

**中文解读：** `QDir::absolutePath` 用于计算、查询或取得与“absolute、Path”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] void QDir::addSearchPath(const QString &prefix, const QString &path)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `addSearchPath`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `prefix`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `path`：类型为 `const QString &`。没有默认值，调用时必须提供。路径字符串。要确认是相对路径还是绝对路径，以及它相对于哪个工作目录。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.0] void QDir::addSearchPath(const QString &prefix, const std::filesystem::path &path)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `addSearchPath`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `prefix`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `path`：类型为 `const std::filesystem::path &`。没有默认值，调用时必须提供。路径字符串。要确认是相对路径还是绝对路径，以及它相对于哪个工作目录。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QDir::canonicalPath() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `canonicalPath`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QDir::cd(const QString &dirName)`

**API 类别：** 成员函数说明

**中文解读：** `QDir::cd` 用于计算、查询或取得与“cd”相关的操作。调用时要先确认当前状态和 `dirName` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `dirName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QDir::cdUp()`

**API 类别：** 成员函数说明

**中文解读：** `QDir::cdUp` 用于计算、查询或取得与“cd、Up”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QDir::cleanPath(const QString &path)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `cleanPath`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `path`：类型为 `const QString &`。没有默认值，调用时必须提供。路径字符串。要确认是相对路径还是绝对路径，以及它相对于哪个工作目录。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qsizetype QDir::count() const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `count`，返回 `QDir` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QDir QDir::current()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `current`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QDir`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QDir::currentPath()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `currentPath`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QDir::dirName() const`

**API 类别：** 成员函数说明

**中文解读：** `QDir::dirName` 用于计算、查询或取得与“dir、名称”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QFileInfoList QDir::drives()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `drives`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QFileInfoList`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFileInfoList QDir::entryInfoList(const QStringList &nameFilters, QDir::Filters filters = NoFilter, QDir::SortFlags sort = NoSort) const`

**API 类别：** 成员函数说明

**中文解读：** `QDir::entryInfoList` 用于计算、查询或取得与“entry、Info、List”相关的操作。调用时要先确认当前状态和 `nameFilters`、`filters`、`sort` 的有效范围；返回类型是 `QFileInfoList`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QFileInfoList`。
- 参数 `nameFilters`：类型为 `const QStringList &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `filters`：类型为 `QDir::Filters`。默认值为 `NoFilter`。传入 `QDir::Filters` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sort`：类型为 `QDir::SortFlags`。默认值为 `NoSort`。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFileInfoList QDir::entryInfoList(QDir::Filters filters = NoFilter, QDir::SortFlags sort = NoSort) const`

**API 类别：** 成员函数说明

**中文解读：** `QDir::entryInfoList` 用于计算、查询或取得与“entry、Info、List”相关的操作。调用时要先确认当前状态和 `filters`、`sort` 的有效范围；返回类型是 `QFileInfoList`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QFileInfoList`。
- 参数 `filters`：类型为 `QDir::Filters`。默认值为 `NoFilter`。传入 `QDir::Filters` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sort`：类型为 `QDir::SortFlags`。默认值为 `NoSort`。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringList QDir::entryList(const QStringList &nameFilters, QDir::Filters filters = NoFilter, QDir::SortFlags sort = NoSort) const`

**API 类别：** 成员函数说明

**中文解读：** `QDir::entryList` 用于计算、查询或取得与“entry、List”相关的操作。调用时要先确认当前状态和 `nameFilters`、`filters`、`sort` 的有效范围；返回类型是 `QStringList`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStringList`。
- 参数 `nameFilters`：类型为 `const QStringList &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `filters`：类型为 `QDir::Filters`。默认值为 `NoFilter`。传入 `QDir::Filters` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sort`：类型为 `QDir::SortFlags`。默认值为 `NoSort`。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringList QDir::entryList(QDir::Filters filters = NoFilter, QDir::SortFlags sort = NoSort) const`

**API 类别：** 成员函数说明

**中文解读：** `QDir::entryList` 用于计算、查询或取得与“entry、List”相关的操作。调用时要先确认当前状态和 `filters`、`sort` 的有效范围；返回类型是 `QStringList`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStringList`。
- 参数 `filters`：类型为 `QDir::Filters`。默认值为 `NoFilter`。传入 `QDir::Filters` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sort`：类型为 `QDir::SortFlags`。默认值为 `NoSort`。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QDir::exists(const QString &name) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `exists`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `name`：类型为 `const QString &`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QDir::exists() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `exists`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QDir::filePath(const QString &fileName) const`

**API 类别：** 成员函数说明

**中文解读：** `QDir::filePath` 用于计算、查询或取得与“file、Path”相关的操作。调用时要先确认当前状态和 `fileName` 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数 `fileName`：类型为 `const QString &`。没有默认值，调用时必须提供。文件名或路径。优先使用 Qt 的路径 API 拼接和规范化，不要手写平台分隔符。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] std::filesystem::path QDir::filesystemAbsolutePath() const`

**API 类别：** 成员函数说明

**中文解读：** `QDir::filesystemAbsolutePath` 用于计算、查询或取得与“filesystem、Absolute、Path”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `std::filesystem::path`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`std::filesystem::path`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] std::filesystem::path QDir::filesystemCanonicalPath() const`

**API 类别：** 成员函数说明

**中文解读：** `QDir::filesystemCanonicalPath` 用于计算、查询或取得与“filesystem、Canonical、Path”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `std::filesystem::path`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`std::filesystem::path`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] std::filesystem::path QDir::filesystemPath() const`

**API 类别：** 成员函数说明

**中文解读：** `QDir::filesystemPath` 用于计算、查询或取得与“filesystem、Path”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `std::filesystem::path`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`std::filesystem::path`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDir::Filters QDir::filter() const`

**API 类别：** 成员函数说明

**中文解读：** `QDir::filter` 用于计算、查询或取得与“filter”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDir::Filters`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDir::Filters`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QDir::fromNativeSeparators(const QString &pathName)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromNativeSeparators`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `pathName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QDir QDir::home()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `home`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QDir`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QDir::homePath()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `homePath`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QDir::isAbsolute() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isAbsolute`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] bool QDir::isAbsolutePath(const QString &path)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `isAbsolutePath`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数 `path`：类型为 `const QString &`。没有默认值，调用时必须提供。路径字符串。要确认是相对路径还是绝对路径，以及它相对于哪个工作目录。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QDir::isEmpty(QDir::Filters filters = Filters(AllEntries | NoDotAndDotDot)) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isEmpty`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `filters`：类型为 `QDir::Filters`。默认值为 `Filters(AllEntries | NoDotAndDotDot)`。传入 `QDir::Filters` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QDir::isReadable() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isReadable`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QDir::isRelative() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isRelative`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] bool QDir::isRelativePath(const QString &path)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `isRelativePath`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数 `path`：类型为 `const QString &`。没有默认值，调用时必须提供。路径字符串。要确认是相对路径还是绝对路径，以及它相对于哪个工作目录。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QDir::isRoot() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isRoot`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static constexpr noexcept] QChar QDir::listSeparator()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `listSeparator`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QChar`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QDir::makeAbsolute()`

**API 类别：** 成员函数说明

**中文解读：** `QDir::makeAbsolute` 用于计算、查询或取得与“make、Absolute”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] bool QDir::match(const QString &filter, const QString &fileName)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `match`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数 `filter`：类型为 `const QString &`。没有默认值，调用时必须提供。过滤条件、匹配器或过滤标志；要确认它作用于显示结果、输入数据还是事件传播。
- 参数 `fileName`：类型为 `const QString &`。没有默认值，调用时必须提供。文件名或路径。优先使用 Qt 的路径 API 拼接和规范化，不要手写平台分隔符。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] bool QDir::match(const QStringList &filters, const QString &fileName)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `match`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数 `filters`：类型为 `const QStringList &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `fileName`：类型为 `const QString &`。没有默认值，调用时必须提供。文件名或路径。优先使用 Qt 的路径 API 拼接和规范化，不要手写平台分隔符。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QDir::mkdir(const QString &dirName, std::optional<QFileDevice::Permissions> permissions = std::nullopt) const`

**API 类别：** 成员函数说明

**中文解读：** `QDir::mkdir` 用于计算、查询或取得与“mkdir”相关的操作。调用时要先确认当前状态和 `dirName`、`permissions` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `dirName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `permissions`：类型为 `std::optional<QFileDevice::Permissions>`。默认值为 `std::nullopt`。传入 `std::optional<QFileDevice::Permissions>` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QDir::mkpath(const QString &dirPath, std::optional<QFileDevice::Permissions> permissions = std::nullopt) const`

**API 类别：** 成员函数说明

**中文解读：** `QDir::mkpath` 用于计算、查询或取得与“mkpath”相关的操作。调用时要先确认当前状态和 `dirPath`、`permissions` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `dirPath`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `permissions`：类型为 `std::optional<QFileDevice::Permissions>`。默认值为 `std::nullopt`。传入 `std::optional<QFileDevice::Permissions>` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringList QDir::nameFilters() const`

**API 类别：** 成员函数说明

**中文解读：** `QDir::nameFilters` 用于计算、查询或取得与“名称、Filters”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QStringList`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStringList`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QDir::path() const`

**API 类别：** 成员函数说明

**中文解读：** `QDir::path` 用于计算、查询或取得与“path”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QDir::refresh() const`

**API 类别：** 成员函数说明

**中文解读：** `QDir::refresh` 用于执行与“refresh”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QDir::relativeFilePath(const QString &fileName) const`

**API 类别：** 成员函数说明

**中文解读：** `QDir::relativeFilePath` 用于计算、查询或取得与“relative、File、Path”相关的操作。调用时要先确认当前状态和 `fileName` 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数 `fileName`：类型为 `const QString &`。没有默认值，调用时必须提供。文件名或路径。优先使用 Qt 的路径 API 拼接和规范化，不要手写平台分隔符。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QDir::remove(const QString &fileName)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `remove`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`bool`。
- 参数 `fileName`：类型为 `const QString &`。没有默认值，调用时必须提供。文件名或路径。优先使用 Qt 的路径 API 拼接和规范化，不要手写平台分隔符。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QDir::removeRecursively()`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeRecursively`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QDir::rename(const QString &oldName, const QString &newName)`

**API 类别：** 成员函数说明

**中文解读：** `QDir::rename` 用于计算、查询或取得与“rename”相关的操作。调用时要先确认当前状态和 `oldName`、`newName` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `oldName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `newName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QDir::rmdir(const QString &dirName) const`

**API 类别：** 成员函数说明

**中文解读：** `QDir::rmdir` 用于计算、查询或取得与“rmdir”相关的操作。调用时要先确认当前状态和 `dirName` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `dirName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QDir::rmpath(const QString &dirPath) const`

**API 类别：** 成员函数说明

**中文解读：** `QDir::rmpath` 用于计算、查询或取得与“rmpath”相关的操作。调用时要先确认当前状态和 `dirPath` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `dirPath`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QDir QDir::root()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `root`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QDir`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QDir::rootPath()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `rootPath`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QStringList QDir::searchPaths(const QString &prefix)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `searchPaths`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QStringList`。
- 参数 `prefix`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QChar QDir::separator()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `separator`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QChar`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] bool QDir::setCurrent(const QString &path)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `setCurrent`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数 `path`：类型为 `const QString &`。没有默认值，调用时必须提供。路径字符串。要确认是相对路径还是绝对路径，以及它相对于哪个工作目录。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QDir::setFilter(QDir::Filters filters)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFilter`。调用它会改变 `QDir` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `filters`：类型为 `QDir::Filters`。没有默认值，调用时必须提供。传入 `QDir::Filters` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QDir::setNameFilters(const QStringList &nameFilters)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setNameFilters`。调用它会改变 `QDir` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `nameFilters`：类型为 `const QStringList &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QDir::setPath(const QString &path)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPath`。调用它会改变 `QDir` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `path`：类型为 `const QString &`。没有默认值，调用时必须提供。路径字符串。要确认是相对路径还是绝对路径，以及它相对于哪个工作目录。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] void QDir::setPath(const std::filesystem::path &path)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPath`。调用它会改变 `QDir` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `path`：类型为 `const std::filesystem::path &`。没有默认值，调用时必须提供。路径字符串。要确认是相对路径还是绝对路径，以及它相对于哪个工作目录。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] void QDir::setSearchPaths(const QString &prefix, const QStringList &searchPaths)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `setSearchPaths`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `prefix`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `searchPaths`：类型为 `const QStringList &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QDir::setSorting(QDir::SortFlags sort)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSorting`。调用它会改变 `QDir` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `sort`：类型为 `QDir::SortFlags`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDir::SortFlags QDir::sorting() const`

**API 类别：** 成员函数说明

**中文解读：** `QDir::sorting` 用于计算、查询或取得与“sorting”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDir::SortFlags`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDir::SortFlags`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] void QDir::swap(QDir &other)`

**API 类别：** 成员函数说明

**中文解读：** `QDir::swap` 用于执行与“swap”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `other`：类型为 `QDir &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QDir QDir::temp()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `temp`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QDir`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QDir::tempPath()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `tempPath`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QDir::toNativeSeparators(const QString &pathName)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `toNativeSeparators`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `pathName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QDir &QDir::operator=(QDir &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDir` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDir &`。
- 参数 `other`：类型为 `QDir &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDir &QDir::operator=(const QDir &dir)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDir` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDir &`。
- 参数 `dir`：类型为 `const QDir &`。没有默认值，调用时必须提供。传入 `const QDir &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QDir::operator[](qsizetype pos) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDir` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QString`。
- 参数 `pos`：类型为 `qsizetype`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator!=(const QDir &lhs, const QDir &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDir` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QDir &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QDir &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator==(const QDir &lhs, const QDir &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDir` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QDir &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QDir &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum Filter { Dirs, AllDirs, Files, Drives, NoSymLinks, …, CaseSensitive }`

**API 类别：** 公有类型

**中文解读：** 这是 `QDir` 暴露的类型声明 `Filter`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags Filters`

**API 类别：** 公有类型

**中文解读：** 这是 `QDir` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum SortFlag { Name, Time, Size, Type, Unsorted, …, LocaleAware }`

**API 类别：** 公有类型

**中文解读：** 这是 `QDir` 暴露的类型声明 `Sort、Flag`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags SortFlags`

**API 类别：** 公有类型

**中文解读：** 这是 `QDir` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

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

不要手写反斜杠拼路径；不要把文件名过滤器误当正则表达式；遍历结果可能为空，权限错误要结合 QFileInfo 和应用逻辑处理。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QDir` 所属机制类型：文件、设备与流机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
