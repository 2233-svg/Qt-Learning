# QTextStream

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 文本数据流，负责编码、行读取、格式化输出和文本设备读写。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QTextStream`：文本数据流，负责编码、行读取、格式化输出和文本设备读写。

**内部模型：** 文件和 I/O 类型把路径/设备描述与打开后的读写状态分开。打开模式决定可执行的操作，当前位置、缓冲区、文本编码、权限和错误状态共同决定一次读写是否正确。

**适用场景：** 构造稳定路径，选择正确的 OpenMode，检查 open 和 errorString，按数据规模使用流式读写或分块处理，明确文本编码，完成后关闭并处理失败。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要手写平台分隔符；不要默认相对路径指向程序目录；不要把本地编码、UTF-8 和二进制混在一起；写文件时要考虑临时文件、覆盖、权限和原子替换。

## 2. 依赖与对象关系

- 头文件：`#include <QTextStream>`
- 继承自：QIODeviceBase
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

### 公有类型

- `enum FieldAlignment { AlignLeft, AlignRight, AlignCenter, AlignAccountingStyle }`
- `enum NumberFlag { ShowBase, ForcePoint, ForceSign, UppercaseBase, UppercaseDigits }`
- `flags NumberFlags`
- `enum RealNumberNotation { ScientificNotation, FixedNotation, SmartNotation }`
- `enum Status { Ok, ReadPastEnd, ReadCorruptData, WriteFailed }`

### 公有函数

- `QTextStream()`
- `QTextStream(QIODevice *device)`
- `QTextStream(FILE *fileHandle, QIODeviceBase::OpenMode openMode = ReadWrite)`
- `QTextStream(QByteArray *array, QIODeviceBase::OpenMode openMode = ReadWrite)`
- `QTextStream(QString *string, QIODeviceBase::OpenMode openMode = ReadWrite)`
- `QTextStream(const QByteArray &array, QIODeviceBase::OpenMode openMode = ReadOnly)`
- `virtual ~QTextStream()`
- `bool atEnd() const`
- `bool autoDetectUnicode() const`
- `QIODevice * device() const`
- `QStringConverter::Encoding encoding() const`
- `QTextStream::FieldAlignment fieldAlignment() const`
- `int fieldWidth() const`
- `void flush()`
- `bool generateByteOrderMark() const`
- `int integerBase() const`
- `QLocale locale() const`
- `QTextStream::NumberFlags numberFlags() const`
- `QChar padChar() const`
- `qint64 pos() const`
- `QString read(qint64 maxlen)`
- `QString readAll()`
- `QString readLine(qint64 maxlen = 0)`
- `bool readLineInto(QString *line, qint64 maxlen = 0)`
- `QTextStream::RealNumberNotation realNumberNotation() const`
- `int realNumberPrecision() const`
- `void reset()`
- `void resetStatus()`
- `bool seek(qint64 pos)`
- `void setAutoDetectUnicode(bool enabled)`
- `void setDevice(QIODevice *device)`
- `(since 6.0) void setEncoding(QStringConverter::Encoding encoding)`
- `void setFieldAlignment(QTextStream::FieldAlignment mode)`
- `void setFieldWidth(int width)`
- `void setGenerateByteOrderMark(bool generate)`
- `void setIntegerBase(int base)`
- `void setLocale(const QLocale &locale)`
- `void setNumberFlags(QTextStream::NumberFlags flags)`
- `void setPadChar(QChar ch)`
- `void setRealNumberNotation(QTextStream::RealNumberNotation notation)`
- `void setRealNumberPrecision(int precision)`
- `void setStatus(QTextStream::Status status)`
- `void setString(QString *string, QIODeviceBase::OpenMode openMode = ReadWrite)`
- `void skipWhiteSpace()`
- `QTextStream::Status status() const`
- `QString * string() const`
- `(since 6.10) operator bool() const`
- `QTextStream & operator<<(QChar c)`
- `QTextStream & operator<<(const QString &string)`
- `QTextStream & operator<<(float f)`
- `QTextStream & operator<<(short i)`
- `QTextStream & operator<<(QLatin1StringView string)`
- `QTextStream & operator<<(QStringView string)`
- `QTextStream & operator<<(char c)`
- `(since 6.3.1) QTextStream & operator<<(char16_t c)`
- `QTextStream & operator<<(const QByteArray &array)`
- `QTextStream & operator<<(const char *string)`
- `QTextStream & operator<<(const void *ptr)`
- `QTextStream & operator<<(double f)`
- `QTextStream & operator<<(int i)`
- `QTextStream & operator<<(long i)`
- `QTextStream & operator<<(qlonglong i)`
- `QTextStream & operator<<(qulonglong i)`
- `QTextStream & operator<<(unsigned int i)`
- `QTextStream & operator<<(unsigned long i)`
- `QTextStream & operator<<(unsigned short i)`
- `QTextStream & operator>>(QChar &c)`
- `QTextStream & operator>>(QString &str)`
- `QTextStream & operator>>(float &f)`
- `QTextStream & operator>>(short &i)`
- `QTextStream & operator>>(QByteArray &array)`
- `QTextStream & operator>>(char &c)`
- `QTextStream & operator>>(char *c)`
- `(since 6.4) QTextStream & operator>>(char16_t &c)`
- `QTextStream & operator>>(double &f)`
- `QTextStream & operator>>(int &i)`
- `QTextStream & operator>>(long &i)`
- `QTextStream & operator>>(qlonglong &i)`
- `QTextStream & operator>>(qulonglong &i)`
- `QTextStream & operator>>(unsigned int &i)`
- `QTextStream & operator>>(unsigned long &i)`
- `QTextStream & operator>>(unsigned short &i)`

### 相关非成员函数

- `QTextStreamManipulator qSetFieldWidth(int width)`
- `QTextStreamManipulator qSetPadChar(QChar ch)`
- `QTextStreamManipulator qSetRealNumberPrecision(int precision)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 91 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QTextStream::FieldAlignment`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QTextStream` 暴露的类型声明 `Field、对齐方式`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:FieldAlignment`。
- 属性名：`QTextStream`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QTextStream::NumberFlagflags QTextStream::NumberFlags`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QTextStream` 暴露的类型声明 `Number、Flagflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:NumberFlagflags QTextStream::NumberFlags`。
- 属性名：`QTextStream`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QTextStream::RealNumberNotation`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QTextStream` 暴露的类型声明 `Real、Number、Notation`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:RealNumberNotation`。
- 属性名：`QTextStream`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QTextStream::Status`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QTextStream` 暴露的类型声明 `状态`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Status`。
- 属性名：`QTextStream`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextStream::QTextStream()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextStream` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QTextStream::QTextStream(QIODevice *device)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextStream` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `device`：类型为 `QIODevice *`。没有默认值，调用时必须提供。QIODevice 或绘制设备。调用前要确认已经打开、支持所需模式，或处于合法绘制阶段。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QTextStream::QTextStream(FILE *fileHandle, QIODeviceBase::OpenMode openMode = ReadWrite)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextStream` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `fileHandle`：类型为 `FILE *`。没有默认值，调用时必须提供。传入 `FILE *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `openMode`：类型为 `QIODeviceBase::OpenMode`。默认值为 `ReadWrite`。传入 `QIODeviceBase::OpenMode` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QTextStream::QTextStream(QByteArray *array, QIODeviceBase::OpenMode openMode = ReadWrite)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextStream` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `array`：类型为 `QByteArray *`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `openMode`：类型为 `QIODeviceBase::OpenMode`。默认值为 `ReadWrite`。传入 `QIODeviceBase::OpenMode` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QTextStream::QTextStream(QString *string, QIODeviceBase::OpenMode openMode = ReadWrite)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextStream` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `string`：类型为 `QString *`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `openMode`：类型为 `QIODeviceBase::OpenMode`。默认值为 `ReadWrite`。传入 `QIODeviceBase::OpenMode` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QTextStream::QTextStream(const QByteArray &array, QIODeviceBase::OpenMode openMode = ReadOnly)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextStream` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `array`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `openMode`：类型为 `QIODeviceBase::OpenMode`。默认值为 `ReadOnly`。传入 `QIODeviceBase::OpenMode` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QTextStream::~QTextStream()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextStream` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QTextStream::atEnd() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextStream::atEnd` 用于计算、查询或取得与“按位置访问、结束”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QTextStream::autoDetectUnicode() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextStream::autoDetectUnicode` 用于计算、查询或取得与“auto、Detect、Unicode”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QIODevice *QTextStream::device() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextStream::device` 用于计算、查询或取得与“device”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QIODevice *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QIODevice *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringConverter::Encoding QTextStream::encoding() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextStream::encoding` 用于计算、查询或取得与“encoding”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QStringConverter::Encoding`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStringConverter::Encoding`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextStream::FieldAlignment QTextStream::fieldAlignment() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextStream::fieldAlignment` 用于计算、查询或取得与“field、对齐方式”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QTextStream::FieldAlignment`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextStream::FieldAlignment`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QTextStream::fieldWidth() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextStream::fieldWidth` 用于计算、查询或取得与“field、宽度”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextStream::flush()`

**API 类别：** 成员函数说明

**中文解读：** `QTextStream::flush` 用于执行与“刷新”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QTextStream::generateByteOrderMark() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextStream::generateByteOrderMark` 用于计算、查询或取得与“generate、Byte、Order、Mark”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QTextStream::integerBase() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextStream::integerBase` 用于计算、查询或取得与“integer、Base”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QLocale QTextStream::locale() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextStream::locale` 用于计算、查询或取得与“locale”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QLocale`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QLocale`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextStream::NumberFlags QTextStream::numberFlags() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextStream::numberFlags` 用于计算、查询或取得与“number、标志”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QTextStream::NumberFlags`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextStream::NumberFlags`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QChar QTextStream::padChar() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextStream::padChar` 用于计算、查询或取得与“pad、Char”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QChar`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QChar`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qint64 QTextStream::pos() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextStream::pos` 用于计算、查询或取得与“pos”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qint64`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qint64`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QTextStream::read(qint64 maxlen)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextStream` 的核心操作 `read`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`QString`。
- 参数 `maxlen`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 要区分 EOF、暂时无数据和错误；大文件优先分块读取。

### `QString QTextStream::readAll()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextStream` 的核心操作 `readAll`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 要区分 EOF、暂时无数据和错误；大文件优先分块读取。

### `QString QTextStream::readLine(qint64 maxlen = 0)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextStream` 的核心操作 `readLine`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`QString`。
- 参数 `maxlen`：类型为 `qint64`。默认值为 `0`。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 要区分 EOF、暂时无数据和错误；大文件优先分块读取。

### `bool QTextStream::readLineInto(QString *line, qint64 maxlen = 0)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextStream` 的核心操作 `readLineInto`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`bool`。
- 参数 `line`：类型为 `QString *`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `maxlen`：类型为 `qint64`。默认值为 `0`。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 要区分 EOF、暂时无数据和错误；大文件优先分块读取。

### `QTextStream::RealNumberNotation QTextStream::realNumberNotation() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextStream::realNumberNotation` 用于计算、查询或取得与“real、Number、Notation”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QTextStream::RealNumberNotation`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextStream::RealNumberNotation`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QTextStream::realNumberPrecision() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextStream::realNumberPrecision` 用于计算、查询或取得与“real、Number、Precision”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextStream::reset()`

**API 类别：** 成员函数说明

**中文解读：** 这是状态清理或重置 API `reset`。调用后原有数据、索引、缓存或绑定可能失效；使用前先确认它影响的是当前对象、子对象还是底层共享资源，之后重新检查状态。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextStream::resetStatus()`

**API 类别：** 成员函数说明

**中文解读：** `QTextStream::resetStatus` 用于执行与“重置、状态”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QTextStream::seek(qint64 pos)`

**API 类别：** 成员函数说明

**中文解读：** `QTextStream::seek` 用于计算、查询或取得与“定位”相关的操作。调用时要先确认当前状态和 `pos` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `pos`：类型为 `qint64`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextStream::setAutoDetectUnicode(bool enabled)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setAutoDetectUnicode`。调用它会改变 `QTextStream` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enabled`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextStream::setDevice(QIODevice *device)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setDevice`。调用它会改变 `QTextStream` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `device`：类型为 `QIODevice *`。没有默认值，调用时必须提供。QIODevice 或绘制设备。调用前要确认已经打开、支持所需模式，或处于合法绘制阶段。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] void QTextStream::setEncoding(QStringConverter::Encoding encoding)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setEncoding`。调用它会改变 `QTextStream` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `encoding`：类型为 `QStringConverter::Encoding`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextStream::setFieldAlignment(QTextStream::FieldAlignment mode)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFieldAlignment`。调用它会改变 `QTextStream` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `mode`：类型为 `QTextStream::FieldAlignment`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextStream::setFieldWidth(int width)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFieldWidth`。调用它会改变 `QTextStream` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `width`：类型为 `int`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextStream::setGenerateByteOrderMark(bool generate)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setGenerateByteOrderMark`。调用它会改变 `QTextStream` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `generate`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextStream::setIntegerBase(int base)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setIntegerBase`。调用它会改变 `QTextStream` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `base`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextStream::setLocale(const QLocale &locale)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setLocale`。调用它会改变 `QTextStream` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `locale`：类型为 `const QLocale &`。没有默认值，调用时必须提供。传入 `const QLocale &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextStream::setNumberFlags(QTextStream::NumberFlags flags)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setNumberFlags`。调用它会改变 `QTextStream` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `flags`：类型为 `QTextStream::NumberFlags`。没有默认值，调用时必须提供。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextStream::setPadChar(QChar ch)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setPadChar`。调用它会改变 `QTextStream` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `ch`：类型为 `QChar`。没有默认值，调用时必须提供。传入 `QChar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextStream::setRealNumberNotation(QTextStream::RealNumberNotation notation)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setRealNumberNotation`。调用它会改变 `QTextStream` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `notation`：类型为 `QTextStream::RealNumberNotation`。没有默认值，调用时必须提供。传入 `QTextStream::RealNumberNotation` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextStream::setRealNumberPrecision(int precision)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setRealNumberPrecision`。调用它会改变 `QTextStream` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `precision`：类型为 `int`。没有默认值，调用时必须提供。精度或舍入策略；它可能影响数值转换和数据库结果，不能只按显示位数理解。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextStream::setStatus(QTextStream::Status status)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setStatus`。调用它会改变 `QTextStream` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `status`：类型为 `QTextStream::Status`。没有默认值，调用时必须提供。传入 `QTextStream::Status` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextStream::setString(QString *string, QIODeviceBase::OpenMode openMode = ReadWrite)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setString`。调用它会改变 `QTextStream` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `string`：类型为 `QString *`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `openMode`：类型为 `QIODeviceBase::OpenMode`。默认值为 `ReadWrite`。传入 `QIODeviceBase::OpenMode` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QTextStream::skipWhiteSpace()`

**API 类别：** 成员函数说明

**中文解读：** `QTextStream::skipWhiteSpace` 用于执行与“skip、White、Space”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextStream::Status QTextStream::status() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextStream::status` 用于计算、查询或取得与“状态”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QTextStream::Status`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextStream::Status`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString *QTextStream::string() const`

**API 类别：** 成员函数说明

**中文解读：** `QTextStream::string` 用于计算、查询或取得与“字符串”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit noexcept, since 6.10] QTextStream::operator bool() const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextStream` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`由运算符声明决定`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextStream &QTextStream::operator<<(QChar c)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextStream` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QTextStream &`。
- 参数 `c`：类型为 `QChar`。没有默认值，调用时必须提供。传入 `QChar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextStream &QTextStream::operator<<(const QString &string)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextStream` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QTextStream &`。
- 参数 `string`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextStream &QTextStream::operator<<(float f)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextStream` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QTextStream &`。
- 参数 `f`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextStream &QTextStream::operator<<(short i)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextStream` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QTextStream &`。
- 参数 `i`：类型为 `short`。没有默认值，调用时必须提供。传入 `short` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextStream &QTextStream::operator<<(QLatin1StringView string)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextStream` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QTextStream &`。
- 参数 `string`：类型为 `QLatin1StringView`。没有默认值，调用时必须提供。传入 `QLatin1StringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextStream &QTextStream::operator<<(QStringView string)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextStream` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QTextStream &`。
- 参数 `string`：类型为 `QStringView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextStream &QTextStream::operator<<(char c)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextStream` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QTextStream &`。
- 参数 `c`：类型为 `char`。没有默认值，调用时必须提供。传入 `char` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.3.1] QTextStream &QTextStream::operator<<(char16_t c)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextStream` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QTextStream &`。
- 参数 `c`：类型为 `char16_t`。没有默认值，调用时必须提供。传入 `char16_t` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextStream &QTextStream::operator<<(const QByteArray &array)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextStream` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QTextStream &`。
- 参数 `array`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextStream &QTextStream::operator<<(const char *string)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextStream` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QTextStream &`。
- 参数 `string`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextStream &QTextStream::operator<<(const void *ptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextStream` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QTextStream &`。
- 参数 `ptr`：类型为 `const void *`。没有默认值，调用时必须提供。传入 `const void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextStream &QTextStream::operator<<(double f)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextStream` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QTextStream &`。
- 参数 `f`：类型为 `double`。没有默认值，调用时必须提供。传入 `double` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextStream &QTextStream::operator<<(int i)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextStream` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QTextStream &`。
- 参数 `i`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextStream &QTextStream::operator<<(long i)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextStream` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QTextStream &`。
- 参数 `i`：类型为 `long`。没有默认值，调用时必须提供。传入 `long` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextStream &QTextStream::operator<<(qlonglong i)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextStream` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QTextStream &`。
- 参数 `i`：类型为 `qlonglong`。没有默认值，调用时必须提供。传入 `qlonglong` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextStream &QTextStream::operator<<(qulonglong i)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextStream` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QTextStream &`。
- 参数 `i`：类型为 `qulonglong`。没有默认值，调用时必须提供。传入 `qulonglong` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextStream &QTextStream::operator<<(unsigned int i)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextStream` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QTextStream &`。
- 参数 `i`：类型为 `unsigned int`。没有默认值，调用时必须提供。传入 `unsigned int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextStream &QTextStream::operator<<(unsigned long i)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextStream` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QTextStream &`。
- 参数 `i`：类型为 `unsigned long`。没有默认值，调用时必须提供。传入 `unsigned long` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextStream &QTextStream::operator<<(unsigned short i)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextStream` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QTextStream &`。
- 参数 `i`：类型为 `unsigned short`。没有默认值，调用时必须提供。传入 `unsigned short` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextStream &QTextStream::operator>>(QChar &c)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextStream` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QTextStream &`。
- 参数 `c`：类型为 `QChar &`。没有默认值，调用时必须提供。传入 `QChar &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextStream &QTextStream::operator>>(QString &str)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextStream` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QTextStream &`。
- 参数 `str`：类型为 `QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextStream &QTextStream::operator>>(float &f)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextStream` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QTextStream &`。
- 参数 `f`：类型为 `float &`。没有默认值，调用时必须提供。传入 `float &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextStream &QTextStream::operator>>(short &i)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextStream` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QTextStream &`。
- 参数 `i`：类型为 `short &`。没有默认值，调用时必须提供。传入 `short &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextStream &QTextStream::operator>>(QByteArray &array)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextStream` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QTextStream &`。
- 参数 `array`：类型为 `QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextStream &QTextStream::operator>>(char &c)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextStream` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QTextStream &`。
- 参数 `c`：类型为 `char &`。没有默认值，调用时必须提供。传入 `char &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextStream &QTextStream::operator>>(char *c)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextStream` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QTextStream &`。
- 参数 `c`：类型为 `char *`。没有默认值，调用时必须提供。传入 `char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.4] QTextStream &QTextStream::operator>>(char16_t &c)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextStream` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QTextStream &`。
- 参数 `c`：类型为 `char16_t &`。没有默认值，调用时必须提供。传入 `char16_t &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextStream &QTextStream::operator>>(double &f)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextStream` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QTextStream &`。
- 参数 `f`：类型为 `double &`。没有默认值，调用时必须提供。传入 `double &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextStream &QTextStream::operator>>(int &i)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextStream` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QTextStream &`。
- 参数 `i`：类型为 `int &`。没有默认值，调用时必须提供。传入 `int &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextStream &QTextStream::operator>>(long &i)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextStream` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QTextStream &`。
- 参数 `i`：类型为 `long &`。没有默认值，调用时必须提供。传入 `long &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextStream &QTextStream::operator>>(qlonglong &i)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextStream` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QTextStream &`。
- 参数 `i`：类型为 `qlonglong &`。没有默认值，调用时必须提供。传入 `qlonglong &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextStream &QTextStream::operator>>(qulonglong &i)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextStream` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QTextStream &`。
- 参数 `i`：类型为 `qulonglong &`。没有默认值，调用时必须提供。传入 `qulonglong &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextStream &QTextStream::operator>>(unsigned int &i)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextStream` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QTextStream &`。
- 参数 `i`：类型为 `unsigned int &`。没有默认值，调用时必须提供。传入 `unsigned int &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextStream &QTextStream::operator>>(unsigned long &i)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextStream` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QTextStream &`。
- 参数 `i`：类型为 `unsigned long &`。没有默认值，调用时必须提供。传入 `unsigned long &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextStream &QTextStream::operator>>(unsigned short &i)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QTextStream` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QTextStream &`。
- 参数 `i`：类型为 `unsigned short &`。没有默认值，调用时必须提供。传入 `unsigned short &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextStreamManipulator qSetFieldWidth(int width)`

**API 类别：** 相关非成员函数

**中文解读：** `QTextStream::qSetFieldWidth` 用于计算、查询或取得与“q、设置、Field、宽度”相关的操作。调用时要先确认当前状态和 `width` 的有效范围；返回类型是 `QTextStreamManipulator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextStreamManipulator`。
- 参数 `width`：类型为 `int`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextStreamManipulator qSetPadChar(QChar ch)`

**API 类别：** 相关非成员函数

**中文解读：** `QTextStream::qSetPadChar` 用于计算、查询或取得与“q、设置、Pad、Char”相关的操作。调用时要先确认当前状态和 `ch` 的有效范围；返回类型是 `QTextStreamManipulator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextStreamManipulator`。
- 参数 `ch`：类型为 `QChar`。没有默认值，调用时必须提供。传入 `QChar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextStreamManipulator qSetRealNumberPrecision(int precision)`

**API 类别：** 相关非成员函数

**中文解读：** `QTextStream::qSetRealNumberPrecision` 用于计算、查询或取得与“q、设置、Real、Number、Precision”相关的操作。调用时要先确认当前状态和 `precision` 的有效范围；返回类型是 `QTextStreamManipulator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextStreamManipulator`。
- 参数 `precision`：类型为 `int`。没有默认值，调用时必须提供。精度或舍入策略；它可能影响数值转换和数据库结果，不能只按显示位数理解。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum NumberFlag { ShowBase, ForcePoint, ForceSign, UppercaseBase, UppercaseDigits }`

**API 类别：** 公有类型

**中文解读：** 这是 `QTextStream` 暴露的类型声明 `Number、Flag`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags NumberFlags`

**API 类别：** 公有类型

**中文解读：** 这是 `QTextStream` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

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

`QTextStream` 所属机制类型：文件、设备与流机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
