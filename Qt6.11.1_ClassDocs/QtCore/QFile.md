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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 47 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `QFile::QFile()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFile` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QFile::QFile(QObject *parent)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFile` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `parent`：类型为 `QObject *`。没有默认值，调用时必须提供。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QFile::QFile(const QString &name)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFile` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `name`：类型为 `const QString &`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit, since 6.0] QFile::QFile(const std::filesystem::path &name)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFile` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `name`：类型为 `const std::filesystem::path &`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFile::QFile(const QString &name, QObject *parent)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFile` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `name`：类型为 `const QString &`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。
- 参数 `parent`：类型为 `QObject *`。没有默认值，调用时必须提供。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] QFile::QFile(const std::filesystem::path &name, QObject *parent)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFile` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `name`：类型为 `const std::filesystem::path &`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。
- 参数 `parent`：类型为 `QObject *`。没有默认值，调用时必须提供。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QFile::~QFile()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFile` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFile::copy(const QString &newName)`

**API 类别：** 成员函数说明

**中文解读：** `QFile::copy` 用于计算、查询或取得与“copy”相关的操作。调用时要先确认当前状态和 `newName` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `newName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] bool QFile::copy(const std::filesystem::path &newName)`

**API 类别：** 成员函数说明

**中文解读：** `QFile::copy` 用于计算、查询或取得与“copy”相关的操作。调用时要先确认当前状态和 `newName` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `newName`：类型为 `const std::filesystem::path &`。没有默认值，调用时必须提供。传入 `const std::filesystem::path &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] bool QFile::copy(const QString &fileName, const QString &newName)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `copy`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数 `fileName`：类型为 `const QString &`。没有默认值，调用时必须提供。文件名或路径。优先使用 Qt 的路径 API 拼接和规范化，不要手写平台分隔符。
- 参数 `newName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QFile::decodeName(const QByteArray &localFileName)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `decodeName`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `localFileName`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QFile::decodeName(const char *localFileName)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `decodeName`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `localFileName`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QByteArray QFile::encodeName(const QString &fileName)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `encodeName`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `fileName`：类型为 `const QString &`。没有默认值，调用时必须提供。文件名或路径。优先使用 Qt 的路径 API 拼接和规范化，不要手写平台分隔符。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] bool QFile::exists(const QString &fileName)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `exists`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数 `fileName`：类型为 `const QString &`。没有默认值，调用时必须提供。文件名或路径。优先使用 Qt 的路径 API 拼接和规范化，不要手写平台分隔符。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFile::exists() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `exists`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QString QFile::fileName() const`

**API 类别：** 成员函数说明

**中文解读：** `QFile::fileName` 用于计算、查询或取得与“file、名称”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] std::filesystem::path QFile::filesystemFileName() const`

**API 类别：** 成员函数说明

**中文解读：** `QFile::filesystemFileName` 用于计算、查询或取得与“filesystem、File、名称”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `std::filesystem::path`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`std::filesystem::path`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.3] std::filesystem::path QFile::filesystemSymLinkTarget() const`

**API 类别：** 成员函数说明

**中文解读：** `QFile::filesystemSymLinkTarget` 用于计算、查询或取得与“filesystem、Sym、Link、目标”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `std::filesystem::path`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`std::filesystem::path`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.3] std::filesystem::path QFile::filesystemSymLinkTarget(const std::filesystem::path &fileName)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `filesystemSymLinkTarget`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`std::filesystem::path`。
- 参数 `fileName`：类型为 `const std::filesystem::path &`。没有默认值，调用时必须提供。文件名或路径。优先使用 Qt 的路径 API 拼接和规范化，不要手写平台分隔符。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFile::link(const QString &linkName)`

**API 类别：** 成员函数说明

**中文解读：** `QFile::link` 用于计算、查询或取得与“link”相关的操作。调用时要先确认当前状态和 `linkName` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `linkName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] bool QFile::link(const std::filesystem::path &newName)`

**API 类别：** 成员函数说明

**中文解读：** `QFile::link` 用于计算、查询或取得与“link”相关的操作。调用时要先确认当前状态和 `newName` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `newName`：类型为 `const std::filesystem::path &`。没有默认值，调用时必须提供。传入 `const std::filesystem::path &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] bool QFile::link(const QString &fileName, const QString &linkName)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `link`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数 `fileName`：类型为 `const QString &`。没有默认值，调用时必须提供。文件名或路径。优先使用 Qt 的路径 API 拼接和规范化，不要手写平台分隔符。
- 参数 `linkName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFile::moveToTrash()`

**API 类别：** 成员函数说明

**中文解读：** `QFile::moveToTrash` 用于计算、查询或取得与“移动、转换输出、Trash”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] bool QFile::moveToTrash(const QString &fileName, QString *pathInTrash = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `moveToTrash`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数 `fileName`：类型为 `const QString &`。没有默认值，调用时必须提供。文件名或路径。优先使用 Qt 的路径 API 拼接和规范化，不要手写平台分隔符。
- 参数 `pathInTrash`：类型为 `QString *`。默认值为 `nullptr`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QFile::open(QIODeviceBase::OpenMode mode)`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `open`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`bool`。
- 参数 `mode`：类型为 `QIODeviceBase::OpenMode`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 成功后才能 read/write/seek；失败时检查 `errorString()`，结束时 close 或让对象安全析构。

### `[since 6.3] bool QFile::open(QIODeviceBase::OpenMode mode, QFileDevice::Permissions permissions)`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `open`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`bool`。
- 参数 `mode`：类型为 `QIODeviceBase::OpenMode`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。
- 参数 `permissions`：类型为 `QFileDevice::Permissions`。没有默认值，调用时必须提供。传入 `QFileDevice::Permissions` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 成功后才能 read/write/seek；失败时检查 `errorString()`，结束时 close 或让对象安全析构。

### `bool QFile::open(FILE *fh, QIODeviceBase::OpenMode mode, QFileDevice::FileHandleFlags handleFlags = DontCloseHandle)`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `open`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`bool`。
- 参数 `fh`：类型为 `FILE *`。没有默认值，调用时必须提供。传入 `FILE *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `mode`：类型为 `QIODeviceBase::OpenMode`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。
- 参数 `handleFlags`：类型为 `QFileDevice::FileHandleFlags`。默认值为 `DontCloseHandle`。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。

**正确调用组合：** 成功后才能 read/write/seek；失败时检查 `errorString()`，结束时 close 或让对象安全析构。

### `bool QFile::open(int fd, QIODeviceBase::OpenMode mode, QFileDevice::FileHandleFlags handleFlags = DontCloseHandle)`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `open`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`bool`。
- 参数 `fd`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `mode`：类型为 `QIODeviceBase::OpenMode`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。
- 参数 `handleFlags`：类型为 `QFileDevice::FileHandleFlags`。默认值为 `DontCloseHandle`。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。

**正确调用组合：** 成功后才能 read/write/seek；失败时检查 `errorString()`，结束时 close 或让对象安全析构。

### `[override virtual] QFileDevice::Permissions QFile::permissions() const`

**API 类别：** 成员函数说明

**中文解读：** `QFile::permissions` 用于计算、查询或取得与“permissions”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QFileDevice::Permissions`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QFileDevice::Permissions`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QFileDevice::Permissions QFile::permissions(const QString &fileName)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `permissions`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QFileDevice::Permissions`。
- 参数 `fileName`：类型为 `const QString &`。没有默认值，调用时必须提供。文件名或路径。优先使用 Qt 的路径 API 拼接和规范化，不要手写平台分隔符。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.0] QFileDevice::Permissions QFile::permissions(const std::filesystem::path &filename)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `permissions`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QFileDevice::Permissions`。
- 参数 `filename`：类型为 `const std::filesystem::path &`。没有默认值，调用时必须提供。文件名或路径。优先使用 Qt 的路径 API 拼接和规范化，不要手写平台分隔符。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFile::remove()`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `remove`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] bool QFile::remove(const QString &fileName)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `remove`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数 `fileName`：类型为 `const QString &`。没有默认值，调用时必须提供。文件名或路径。优先使用 Qt 的路径 API 拼接和规范化，不要手写平台分隔符。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFile::rename(const QString &newName)`

**API 类别：** 成员函数说明

**中文解读：** `QFile::rename` 用于计算、查询或取得与“rename”相关的操作。调用时要先确认当前状态和 `newName` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `newName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] bool QFile::rename(const std::filesystem::path &newName)`

**API 类别：** 成员函数说明

**中文解读：** `QFile::rename` 用于计算、查询或取得与“rename”相关的操作。调用时要先确认当前状态和 `newName` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `newName`：类型为 `const std::filesystem::path &`。没有默认值，调用时必须提供。传入 `const std::filesystem::path &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] bool QFile::rename(const QString &oldName, const QString &newName)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `rename`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数 `oldName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `newName`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QFile::resize(qint64 sz)`

**API 类别：** 成员函数说明

**中文解读：** `QFile::resize` 用于计算、查询或取得与“调整尺寸”相关的操作。调用时要先确认当前状态和 `sz` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `sz`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] bool QFile::resize(const QString &fileName, qint64 sz)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `resize`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数 `fileName`：类型为 `const QString &`。没有默认值，调用时必须提供。文件名或路径。优先使用 Qt 的路径 API 拼接和规范化，不要手写平台分隔符。
- 参数 `sz`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFile::setFileName(const QString &name)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFileName`。调用它会改变 `QFile` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `name`：类型为 `const QString &`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] void QFile::setFileName(const std::filesystem::path &name)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFileName`。调用它会改变 `QFile` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `name`：类型为 `const std::filesystem::path &`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QFile::setPermissions(QFileDevice::Permissions permissions)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPermissions`。调用它会改变 `QFile` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`bool`。
- 参数 `permissions`：类型为 `QFileDevice::Permissions`。没有默认值，调用时必须提供。传入 `QFileDevice::Permissions` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] bool QFile::setPermissions(const QString &fileName, QFileDevice::Permissions permissions)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `setPermissions`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数 `fileName`：类型为 `const QString &`。没有默认值，调用时必须提供。文件名或路径。优先使用 Qt 的路径 API 拼接和规范化，不要手写平台分隔符。
- 参数 `permissions`：类型为 `QFileDevice::Permissions`。没有默认值，调用时必须提供。传入 `QFileDevice::Permissions` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.0] bool QFile::setPermissions(const std::filesystem::path &filename, QFileDevice::Permissions permissionSpec)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `setPermissions`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数 `filename`：类型为 `const std::filesystem::path &`。没有默认值，调用时必须提供。文件名或路径。优先使用 Qt 的路径 API 拼接和规范化，不要手写平台分隔符。
- 参数 `permissionSpec`：类型为 `QFileDevice::Permissions`。没有默认值，调用时必须提供。传入 `QFileDevice::Permissions` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] qint64 QFile::size() const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `size`，返回 `QFile` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`qint64`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.9] bool QFile::supportsMoveToTrash()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `supportsMoveToTrash`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QFile::symLinkTarget(const QString &fileName)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `symLinkTarget`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `fileName`：类型为 `const QString &`。没有默认值，调用时必须提供。文件名或路径。优先使用 Qt 的路径 API 拼接和规范化，不要手写平台分隔符。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QFile::symLinkTarget() const`

**API 类别：** 成员函数说明

**中文解读：** `QFile::symLinkTarget` 用于计算、查询或取得与“sym、Link、目标”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

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
