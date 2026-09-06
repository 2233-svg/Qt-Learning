# QResource

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QResource` 是 文件、设备与流机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QResource` 是 文件、设备与流机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 文件和 I/O 类型把路径/设备描述与打开后的读写状态分开。打开模式决定可执行的操作，当前位置、缓冲区、文本编码、权限和错误状态共同决定一次读写是否正确。

**适用场景：** 构造稳定路径，选择正确的 OpenMode，检查 open 和 errorString，按数据规模使用流式读写或分块处理，明确文本编码，完成后关闭并处理失败。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要手写平台分隔符；不要默认相对路径指向程序目录；不要把本地编码、UTF-8 和二进制混在一起；写文件时要考虑临时文件、覆盖、权限和原子替换。

## 2. 依赖与对象关系

- 头文件：`#include <QResource>`
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

- `enum Compression { NoCompression, ZlibCompression, ZstdCompression }`

### 公有函数

- `QResource(const QString &file = QString(), const QLocale &locale = QLocale())`
- `~QResource()`
- `QString absoluteFilePath() const`
- `QResource::Compression compressionAlgorithm() const`
- `const uchar * data() const`
- `QString fileName() const`
- `bool isValid() const`
- `QDateTime lastModified() const`
- `QLocale locale() const`
- `void setFileName(const QString &file)`
- `void setLocale(const QLocale &locale)`
- `qint64 size() const`
- `QByteArray uncompressedData() const`
- `qint64 uncompressedSize() const`

### 静态公有成员

- `bool registerResource(const QString &rccFileName, const QString &mapRoot = QString())`
- `bool registerResource(const uchar *rccData, const QString &mapRoot = QString())`
- `bool unregisterResource(const QString &rccFileName, const QString &mapRoot = QString())`
- `bool unregisterResource(const uchar *rccData, const QString &mapRoot = QString())`

### 保护函数

- `QStringList children() const`
- `bool isDir() const`
- `bool isFile() const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QResource::Compression`

**作用与语义：**

`compressionAlgorithm()`用这个枚举表示RCC工具用来压缩有效载荷的算法。
- `QResource::NoCompression`：`0`;内容不压缩
- `QResource::ZlibCompression`：`1`;内容通过zlib进行压缩，并可通过`qUncompress()`函数进行解压。
- `QResource::ZstdCompression`：`2`;内容通过zstd进行压缩。解压时，使用zstd库中的`ZSTD_decompress`函数。

### `QResource::QResource(const QString &file = QString(), const QLocale &locale = QLocale())`

**作用与语义：**

构建指向`file`的QResource。`locale`用于加载资源数据的特定本地化。

### `[noexcept] QResource::~QResource()`

**作用与语义：**

释放`QResource`对象的资源。

### `QString QResource::absoluteFilePath() const`

**作用与语义：**

返回该`QResource`所代表的真实路径，如果资源是通过`QDir::searchPaths()`找到的，路径中会显示该路径。

### `[protected] QStringList QResource::children() const`

**作用与语义：**

返回该目录中所有资源的列表，如果资源代表文件，列表将为空。

### `QResource::Compression QResource::compressionAlgorithm() const`

**作用与语义：**

返回该资源被压缩的压缩类型（如果有的话）。如果未被压缩，该函数返回`QResource::NoCompression`。
如果该函数返回`QResource::ZlibCompression`，你可以用`qUncompress()`函数对数据进行解压。直到Qt 5.13之前，这是唯一可能的压缩算法。
如果该函数返回`QResource::ZstdCompression`，你需要使用 Zstandard 库函数（`<zstd.h>` 头部）。Qt 不提供包装器。
参见Zstandard手册。

### `const uchar *QResource::data() const`

**作用与语义：**

返回对该资源所代表的只读数据段的直接访问。如果资源被压缩，返回的数据也会被压缩。调用者必须解压数据或使用该`uncompressedData()`。如果资源是目录，则返回`nullptr`。

### `QString QResource::fileName() const`

**作用与语义：**

返回该`QResource`所代表文件的完整路径，以传递方式。

### `[protected] bool QResource::isDir() const`

**作用与语义：**

如果资源代表目录，因此可能包含`children()`，则返回`true`;如果代表文件，则返回假。

### `[protected] bool QResource::isFile() const`

**作用与语义：**

如果资源代表文件并有数据支持，则返回`true`;如果代表目录，则返回 false。

### `bool QResource::isValid() const`

**作用与语义：**

如果资源确实存在于资源层级中，返回`true`，否则返回 false。

### `QDateTime QResource::lastModified() const`

**作用与语义：**

返回文件最后一次修改的日期和时间，然后打包成资源。

### `QLocale QResource::locale() const`

**作用与语义：**

返回用于定位`QResource`数据的地点。

### `[static] bool QResource::registerResource(const QString &rccFileName, const QString &mapRoot = QString())`

**作用与语义：**

在`mapRoot`指定的位置用给定`rccFileName`注册资源，如果文件成功打开，返回`true`;否则返回`false`。

### `[static] bool QResource::registerResource(const uchar *rccData, const QString &mapRoot = QString())`

**作用与语义：**

在`mapRoot`指定的位置用给定`rccData`注册资源，文件成功打开时返回`true`;否则返回`false`。
警告：数据必须在整个可能引用资源数据的 `QFile` 生命周期内保持有效。

### `void QResource::setFileName(const QString &file)`

**作用与语义：**

设置一个`QResource`指向`file`。`file`可以是绝对的，这种情况下直接打开;如果是相对的，则会尝试在`QDir::searchPaths()`中查找该文件。

### `void QResource::setLocale(const QLocale &locale)`

**作用与语义：**

设置一个`QResource`，只加载资源的本地化到 `locale`。如果找不到特定区域的资源，则使用 C 区域。

### `qint64 QResource::size() const`

**作用与语义：**

返回支持资源的存储数据大小。
如果资源被压缩，该函数返回压缩数据的大小。关于未压缩的大小，请参见 `uncompressedSize()`。

### `QByteArray QResource::uncompressedData() const`

**作用与语义：**

如果数据是压缩存储的，则返回资源数据，先解压。如果资源是目录或解压时发生错误，则返回空`QByteArray`。
注意：如果数据被压缩，该函数每次调用都会解压。结果不会在调用之间缓存。

### `qint64 QResource::uncompressedSize() const`

**作用与语义：**

返回该资源中数据的大小。如果数据未被压缩，该函数返回的大小与`size()`相同。如果被压缩，则该函数从存储流中提取原始未压缩数据的大小。

### `[static] bool QResource::unregisterResource(const QString &rccFileName, const QString &mapRoot = QString())`

**作用与语义：**

在`mapRoot`指定的资源树位置取消注册该`rccFileName`资源，如果资源成功卸载且无资源引用，则返回`true`;否则返回`false`。

### `[static] bool QResource::unregisterResource(const uchar *rccData, const QString &mapRoot = QString())`

**作用与语义：**

在`mapRoot`指定的资源树位置取消注册与给定`rccData`的资源，如果资源成功卸载且没有资源引用，则返回`true`;否则返回`false`。

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

`QResource` 所属机制类型：文件、设备与流机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
