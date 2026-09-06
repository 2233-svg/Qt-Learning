# QFileDevice

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QFileDevice` 是 文件、设备与流机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QFileDevice` 是 文件、设备与流机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 文件和 I/O 类型把路径/设备描述与打开后的读写状态分开。打开模式决定可执行的操作，当前位置、缓冲区、文本编码、权限和错误状态共同决定一次读写是否正确。

**适用场景：** 构造稳定路径，选择正确的 OpenMode，检查 open 和 errorString，按数据规模使用流式读写或分块处理，明确文本编码，完成后关闭并处理失败。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要手写平台分隔符；不要默认相对路径指向程序目录；不要把本地编码、UTF-8 和二进制混在一起；写文件时要考虑临时文件、覆盖、权限和原子替换。

## 2. 依赖与对象关系

- 头文件：`#include <QFileDevice>`
- 继承自：QIODevice
- 直接派生类：QFile、QSaveFile

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

- `enum FileError { NoError, ReadError, WriteError, FatalError, ResourceError, …, CopyError }`
- `enum FileHandleFlag { AutoCloseHandle, DontCloseHandle }`
- `flags FileHandleFlags`
- `enum FileTime { FileAccessTime, FileBirthTime, FileMetadataChangeTime, FileModificationTime }`
- `enum MemoryMapFlag { NoOptions, MapPrivateOption }`
- `flags MemoryMapFlags`
- `enum Permission { ReadOwner, WriteOwner, ExeOwner, ReadUser, WriteUser, …, ExeOther }`
- `flags Permissions`

### 公有函数

- `virtual ~QFileDevice()`
- `QFileDevice::FileError error() const`
- `virtual QString fileName() const`
- `QDateTime fileTime(QFileDevice::FileTime time) const`
- `bool flush()`
- `int handle() const`
- `uchar * map(qint64 offset, qint64 size, QFileDevice::MemoryMapFlags flags = NoOptions)`
- `virtual QFileDevice::Permissions permissions() const`
- `virtual bool resize(qint64 sz)`
- `bool setFileTime(const QDateTime &newDate, QFileDevice::FileTime fileTime)`
- `virtual bool setPermissions(QFileDevice::Permissions permissions)`
- `bool unmap(uchar *address)`
- `void unsetError()`

### 重实现的公有函数

- `virtual bool atEnd() const override`
- `virtual void close() override`
- `virtual bool isSequential() const override`
- `virtual qint64 pos() const override`
- `virtual bool seek(qint64 pos) override`
- `virtual qint64 size() const override`

### 重实现的保护函数

- `virtual qint64 readData(char *data, qint64 len) override`
- `virtual qint64 readLineData(char *data, qint64 maxlen) override`
- `virtual qint64 writeData(const char *data, qint64 len) override`

### 公开宏

- `(since 6.8) QT_NO_USE_NODISCARD_FILE_OPEN`
- `(since 6.8) QT_USE_NODISCARD_FILE_OPEN`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 35 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QFileDevice::FileError`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QFileDevice` 暴露的类型声明 `File、错误`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:FileError`。
- 属性名：`QFileDevice`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QFileDevice::FileHandleFlagflags QFileDevice::FileHandleFlags`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QFileDevice` 暴露的类型声明 `File、Handle、Flagflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:FileHandleFlagflags QFileDevice::FileHandleFlags`。
- 属性名：`QFileDevice`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QFileDevice::FileTime`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QFileDevice` 暴露的类型声明 `File、时间`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:FileTime`。
- 属性名：`QFileDevice`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QFileDevice::MemoryMapFlagflags QFileDevice::MemoryMapFlags`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QFileDevice` 暴露的类型声明 `Memory、映射、Flagflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:MemoryMapFlagflags QFileDevice::MemoryMapFlags`。
- 属性名：`QFileDevice`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QFileDevice::Permissionflags QFileDevice::Permissions`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QFileDevice` 暴露的类型声明 `Permissionflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Permissionflags QFileDevice::Permissions`。
- 属性名：`QFileDevice`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QFileDevice::~QFileDevice()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFileDevice` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QFileDevice::atEnd() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileDevice::atEnd` 用于计算、查询或取得与“按位置访问、结束”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] void QFileDevice::close()`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `close`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFileDevice::FileError QFileDevice::error() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileDevice::error` 用于计算、查询或取得与“错误”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QFileDevice::FileError`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QFileDevice::FileError`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] QString QFileDevice::fileName() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileDevice::fileName` 用于计算、查询或取得与“file、名称”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDateTime QFileDevice::fileTime(QFileDevice::FileTime time) const`

**API 类别：** 成员函数说明

**中文解读：** `QFileDevice::fileTime` 用于计算、查询或取得与“file、时间”相关的操作。调用时要先确认当前状态和 `time` 的有效范围；返回类型是 `QDateTime`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数 `time`：类型为 `QFileDevice::FileTime`。没有默认值，调用时必须提供。传入 `QFileDevice::FileTime` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFileDevice::flush()`

**API 类别：** 成员函数说明

**中文解读：** `QFileDevice::flush` 用于计算、查询或取得与“刷新”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QFileDevice::handle() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileDevice::handle` 用于计算、查询或取得与“handle”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QFileDevice::isSequential() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isSequential`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `uchar *QFileDevice::map(qint64 offset, qint64 size, QFileDevice::MemoryMapFlags flags = NoOptions)`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `map`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`uchar *`。
- 参数 `offset`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `size`：类型为 `qint64`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。
- 参数 `flags`：类型为 `QFileDevice::MemoryMapFlags`。默认值为 `NoOptions`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] QFileDevice::Permissions QFileDevice::permissions() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileDevice::permissions` 用于计算、查询或取得与“permissions”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QFileDevice::Permissions`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QFileDevice::Permissions`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] qint64 QFileDevice::pos() const`

**API 类别：** 成员函数说明

**中文解读：** `QFileDevice::pos` 用于计算、查询或取得与“pos”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qint64`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qint64`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] qint64 QFileDevice::readData(char *data, qint64 len)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFileDevice` 的核心操作 `readData`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`qint64`。
- 参数 `data`：类型为 `char *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `len`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 要区分 EOF、暂时无数据和错误；大文件优先分块读取。

### `[override virtual protected] qint64 QFileDevice::readLineData(char *data, qint64 maxlen)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFileDevice` 的核心操作 `readLineData`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`qint64`。
- 参数 `data`：类型为 `char *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `maxlen`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 要区分 EOF、暂时无数据和错误；大文件优先分块读取。

### `[virtual] bool QFileDevice::resize(qint64 sz)`

**API 类别：** 成员函数说明

**中文解读：** `QFileDevice::resize` 用于计算、查询或取得与“调整尺寸”相关的操作。调用时要先确认当前状态和 `sz` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `sz`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] bool QFileDevice::seek(qint64 pos)`

**API 类别：** 成员函数说明

**中文解读：** `QFileDevice::seek` 用于计算、查询或取得与“定位”相关的操作。调用时要先确认当前状态和 `pos` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `pos`：类型为 `qint64`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFileDevice::setFileTime(const QDateTime &newDate, QFileDevice::FileTime fileTime)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFileTime`。调用它会改变 `QFileDevice` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`bool`。
- 参数 `newDate`：类型为 `const QDateTime &`。没有默认值，调用时必须提供。传入 `const QDateTime &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `fileTime`：类型为 `QFileDevice::FileTime`。没有默认值，调用时必须提供。传入 `QFileDevice::FileTime` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] bool QFileDevice::setPermissions(QFileDevice::Permissions permissions)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPermissions`。调用它会改变 `QFileDevice` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`bool`。
- 参数 `permissions`：类型为 `QFileDevice::Permissions`。没有默认值，调用时必须提供。传入 `QFileDevice::Permissions` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] qint64 QFileDevice::size() const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `size`，返回 `QFileDevice` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`qint64`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QFileDevice::unmap(uchar *address)`

**API 类别：** 成员函数说明

**中文解读：** `QFileDevice::unmap` 用于计算、查询或取得与“unmap”相关的操作。调用时要先确认当前状态和 `address` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `address`：类型为 `uchar *`。没有默认值，调用时必须提供。传入 `uchar *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QFileDevice::unsetError()`

**API 类别：** 成员函数说明

**中文解读：** `QFileDevice::unsetError` 用于执行与“unset、错误”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] qint64 QFileDevice::writeData(const char *data, qint64 len)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QFileDevice` 的核心操作 `writeData`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`qint64`。
- 参数 `data`：类型为 `const char *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `len`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 要检查返回字节数和错误，关键数据考虑 flush、临时文件和原子替换。

### `[since 6.8] QT_NO_USE_NODISCARD_FILE_OPEN`

**API 类别：** 宏说明

**中文解读：** 这是 `QFileDevice` 的 `打开` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum FileHandleFlag { AutoCloseHandle, DontCloseHandle }`

**API 类别：** 公有类型

**中文解读：** 这是 `QFileDevice` 暴露的类型声明 `File、Handle、Flag`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags FileHandleFlags`

**API 类别：** 公有类型

**中文解读：** 这是 `QFileDevice` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum MemoryMapFlag { NoOptions, MapPrivateOption }`

**API 类别：** 公有类型

**中文解读：** 这是 `QFileDevice` 暴露的类型声明 `Memory、映射、Flag`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags MemoryMapFlags`

**API 类别：** 公有类型

**中文解读：** 这是 `QFileDevice` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum Permission { ReadOwner, WriteOwner, ExeOwner, ReadUser, WriteUser, …, ExeOther }`

**API 类别：** 公有类型

**中文解读：** 这是 `QFileDevice` 暴露的类型声明 `Permission`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags Permissions`

**API 类别：** 公有类型

**中文解读：** 这是 `QFileDevice` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.8) QT_USE_NODISCARD_FILE_OPEN`

**API 类别：** 公开宏

**中文解读：** 这是 `QFileDevice` 的 `打开` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

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

`QFileDevice` 所属机制类型：文件、设备与流机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
