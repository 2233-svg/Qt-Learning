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

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QTextStream::FieldAlignment`

**作用与语义：**

该枚举规定了当字段宽度大于其所占文本时，如何对齐文本。
- `QTextStream::AlignLeft`：`0`;场地右侧的垫子。
- `QTextStream::AlignRight`：`1`;场地左侧的垫子。
- `QTextStream::AlignCenter`：`2`;场地两侧设有护腿台。
- `QTextStream::AlignAccountingStyle`：`3`;与AlignRight相同，但数字符号是左齐。

### `enum QTextStream::NumberFlagflags QTextStream::NumberFlags`

**作用与语义：**

该枚举规定了各种可以设置影响整数输出的标志，包括`float`和`double`。
- `QTextStream::ShowBase`：`0x1`;如果底为16（“0x”）、8（“0”）或2（“0b”），则显示基底为前缀。
- `QTextStream::ForcePoint`：`0x2`;即使没有小数，也一定要用数字分隔符。
- `QTextStream::ForceSign`：`0x4`;符号始终用数字表示，即使是正数也一样。
- `QTextStream::UppercaseBase`：`0x8`;使用基本前缀的大写版本（“0X”、“0B”）。
- `QTextStream::UppercaseDigits`：`0x10`;用大写字母表示数字10到35，而非小写。
NumberFlags 类型是 QFlags 的 typedef<NumberFlag>。它存储 NumberFlag 值的 OR 组合。

### `enum QTextStream::RealNumberNotation`

**作用与语义：**

该枚举指定了用哪些符号来表示`float`和`double`作为字符串。
- `QTextStream::ScientificNotation`：`2`;科学记号法（`printf()`的`%e`标志）。
- `QTextStream::FixedNotation`：`1`;不动点符号（`printf()`的`%f`旗）。
- `QTextStream::SmartNotation`：`0`;科学符号或定点符号，取决于哪种最合理（`printf()`的`%g`旗）。

### `enum QTextStream::Status`

**作用与语义：**

该枚举描述了文本流的当前状态。
- `QTextStream::Ok`：`0`;文本流正常运行。
- `QTextStream::ReadPastEnd`：`1`;文本流已读出底层设备中数据的末端。
- `QTextStream::ReadCorruptData`：`2`;文本流读取了损坏的数据。
- `QTextStream::WriteFailed`：`3`;文本流无法写入底层设备。

### `QTextStream::QTextStream()`

**作用与语义：**

构建一个QTextStream。在你使用它进行读写之前，必须分配一个设备或字符串。

### `[explicit] QTextStream::QTextStream(QIODevice *device)`

**作用与语义：**

构建一个运行在`device`上的QTextStream。

### `[explicit] QTextStream::QTextStream(FILE *fileHandle, QIODeviceBase::OpenMode openMode = ReadWrite)`

**作用与语义：**

构建一个在`fileHandle`上运行的QTextStream，利用`openMode`定义开模式。内部创建一个`QFile`来处理FILE指针。
该构造器适合直接处理基于FILE的常见输入和输出流：stdin、stdout和stderr。示例：

**官方示例：**

```cpp
 QString str;
 QTextStream in(stdin);
 in >> str;
```

### `[explicit] QTextStream::QTextStream(QByteArray *array, QIODeviceBase::OpenMode openMode = ReadWrite)`

**作用与语义：**

构造一个在`array`上操作的QTextStream，利用`openMode`定义开模式。内部，数组被`QBuffer`包裹。

### `[explicit] QTextStream::QTextStream(QString *string, QIODeviceBase::OpenMode openMode = ReadWrite)`

**作用与语义：**

构造一个在`string`上运行的QTextStream，使用`openMode`定义开模式。

### `[explicit] QTextStream::QTextStream(const QByteArray &array, QIODeviceBase::OpenMode openMode = ReadOnly)`

**作用与语义：**

构造一个 QTextStream，运行于 `array`，使用 `openMode` 定义开模式。数组以只读访问，无论 `openMode` 中的值如何。
该构造器便于处理常数字符串。示例：

**官方示例：**

```cpp
 int main(int argc, char *argv[])
 {
     // read numeric arguments (123, 0x20, 4.5...)
     for (int i = 1; i < argc; ++i) {
         int number;
         QTextStream in(argv[i]);
         in >> number;
         //...
     }
 }
```

### `[virtual noexcept] QTextStream::~QTextStream()`

**作用与语义：**

毁掉`QTextStream`。
如果流运行在设备上，`flush()`会被隐式调用。否则，设备不受影响。

### `bool QTextStream::atEnd() const`

**作用与语义：**

如果没有数据可从`QTextStream`读取，返回`true`;否则返回`false`。这类似于，但不等同于调用`QIODevice::atEnd()`，因为`QTextStream`还考虑其内部Unicode缓冲区。

### `bool QTextStream::autoDetectUnicode() const`

**作用与语义：**

如果启用自动Unicode检测，返回`true`;否则返回`false`。自动Unicode检测默认启用。

### `QIODevice *QTextStream::device() const`

**作用与语义：**

返回与`QTextStream`关联的当前设备，若未分配设备则返回`nullptr`。

### `QStringConverter::Encoding QTextStream::encoding() const`

**作用与语义：**

返回当前分配给流的编码。

### `QTextStream::FieldAlignment QTextStream::fieldAlignment() const`

**作用与语义：**

返回当前字段对齐。

### `int QTextStream::fieldWidth() const`

**作用与语义：**

返回当前场宽。

### `void QTextStream::flush()`

**作用与语义：**

冲洗所有等待写入设备的缓冲数据。
如果`QTextStream`操作字符串，这个函数就不做任何事。

### `bool QTextStream::generateByteOrderMark() const`

**作用与语义：**

如果 `QTextStream` 设置为在使用 UTF 编码时生成 UTF BOM（字节顺序标记），则返回 `true`；否则返回 `false`。UTF BOM 生成默认设置为 false。

### `int QTextStream::integerBase() const`

**作用与语义：**

返回当前整数基数。0表示读取时检测到基数，生成数字时检测到10（十进制）。

### `QLocale QTextStream::locale() const`

**作用与语义：**

返回该流的地点。默认位置是C。

### `QTextStream::NumberFlags QTextStream::numberFlags() const`

**作用与语义：**

返回当前的号码标志。

### `QChar QTextStream::padChar() const`

**作用与语义：**

返回当前的填充字符。

### `qint64 QTextStream::pos() const`

**作用与语义：**

返回对应流当前位置的设备位置，或在发生错误时返回 -1（例如，如果没有设备或字符串，或存在设备错误）。
由于`QTextStream`是缓冲的，这个函数可能需要寻找设备来重建有效的设备位置。这个操作可能很昂贵，所以你可能想避免在紧密循环中调用这个函数。

### `QString QTextStream::read(qint64 maxlen)`

**作用与语义：**

最多从流中读取 `maxlen` 个字符，并将读取的数据返回为 `QString`。

### `QString QTextStream::readAll()`

**作用与语义：**

读取整个流内容，并返回为`QString`。处理大文件时避免使用此功能，因为它会占用大量内存。
如果你不知道有多少数据，打电话给`readLine()`会更好。

### `QString QTextStream::readLine(qint64 maxlen = 0)`

**作用与语义：**

读取流中的一行文本，并返回为`QString`。允许的最大行长设置为`maxlen`。如果流中有超过此长度的行，则在`maxlen`字符后将行分段返回。
如果`maxlen`为0，则直线长度可以任意。
返回的行没有后尾字符（“\n”或“\r\n”），因此调用`QString::trimmed()`有时是不必要的。
如果流已读到文件末尾，readLine() 会返回空 `QString`。对于字符串或支持该文件的设备，你可以用 `atEnd()` 显式测试流的结尾。

### `bool QTextStream::readLineInto(QString *line, qint64 maxlen = 0)`

**作用与语义：**

将流中的一行文本读取到`line`。如果`line` `nullptr`，则该读取行不会被存储。
允许的最大行长设置为`maxlen`。如果流中有比这更长的行，则在`maxlen`字符后将线分段返回。
如果`maxlen`为0，则直线长度可以任意。
结果的行没有尾随的行尾字符（“\n”或“\r\n”），因此调用`QString::trimmed()`可能不必要。
如果 `line` 有足够的容量来接收即将读取的数据，该函数可能不需要分配新的内存。因此，它可以比 `readLine()` 更快。
如果流已读到文件末尾或发生错误，返回`false`;否则返回`true`。调用前`line`的内容无论如何都会被丢弃。

### `QTextStream::RealNumberNotation QTextStream::realNumberNotation() const`

**作用与语义：**

返回当前实数表示法。

### `int QTextStream::realNumberPrecision() const`

**作用与语义：**

返回当前实数精度，或 `QTextStream` 生成实数（`FixedNotation`, `ScientificNotation`）时将写入的小数位数，或最大有效数字数（`SmartNotation`）。

### `void QTextStream::reset()`

**作用与语义：**

重置`QTextStream`的格式选项，使其恢复到原始构造状态。设备、字符串及任何缓冲数据保持不动。

### `void QTextStream::resetStatus()`

**作用与语义：**

重置文本流的状态。

### `bool QTextStream::seek(qint64 pos)`

**作用与语义：**

寻求`pos`在装置中的位置。成功后返回`true`;否则返回`false`。

### `void QTextStream::setAutoDetectUnicode(bool enabled)`

**作用与语义：**

如果`enabled`为真，`QTextStream`会尝试通过查看流数据来检测 Unicode 编码，看看是否能找到 UTF-8、UTF-16 或 UTF-32 字节顺序标记（BOM）。如果找到该标记，`QTextStream` 会用 UTF 编码替换当前编码。
该函数可与`setEncoding()`一起使用。通常将编码设置为UTF-8，然后启用UTF-16检测。

### `void QTextStream::setDevice(QIODevice *device)`

**作用与语义：**

将当前设备设置为`device`。如果设备已被分配，`QTextStream`会在旧设备替换前调用`flush()`。
注意：该函数将locale重置为默认locale（“C”），编码为默认编码UTF-8。

### `[since 6.0] void QTextStream::setEncoding(QStringConverter::Encoding encoding)`

**作用与语义：**

将该流的编码设置为`encoding`。编码用于解码从指定设备读取的任何数据，以及编码写入的数据。默认情况下，使用`QStringConverter::Utf8`，并启用自动Unicode检测。
如果`QTextStream`操作字符串，这个函数就不做任何事。
警告：如果你在文本流从打开的顺序套接字读取时调用该函数，内部缓冲区可能仍包含使用旧编码解码的文本。

### `void QTextStream::setFieldAlignment(QTextStream::FieldAlignment mode)`

**作用与语义：**

将字段对齐设置为`mode`。与`setFieldWidth()`一起使用时，该函数允许生成格式化的输出，文本对齐为左、右或中。

### `void QTextStream::setFieldWidth(int width)`

**作用与语义：**

将当前字段宽度设置为`width`。如果`width`为0（默认值），字段宽度等于生成文本的长度。
注意：字段宽度适用于调用该函数后附加到该流的每个元素（例如，它也填充 endl）。这种行为不同于 STL 中的类似类，后者字段宽度只适用于下一个元素。

### `void QTextStream::setGenerateByteOrderMark(bool generate)`

**作用与语义：**

如果`generate`为真且使用UTF编码，`QTextStream`会在任何数据写入设备前插入BOM（字节顺序标记）。如果`generate`为假，则不会插入BOM。必须在写入任何数据之前调用该函数。否则，它不会做任何事。

### `void QTextStream::setIntegerBase(int base)`

**作用与语义：**

将整数基数设为`base`，既用于读取，也用于生成数字。`base`可以是2（二进制）、8（八进制）、10（十进制）或16（十六进制）。如果`base`为0，`QTextStream`会尝试通过检查数据流中的数据来检测基数。生成数字时，除非基数被明确设置，否则`QTextStream`假设基数为10。

### `void QTextStream::setLocale(const QLocale &locale)`

**作用与语义：**

将该流的区域设置为`locale`。指定的区域用于数字与字符串表示之间的转换。
默认位置是 C，这是一个特殊情况——千群分隔符出于向后兼容性原因不使用。

### `void QTextStream::setNumberFlags(QTextStream::NumberFlags flags)`

**作用与语义：**

将当前数字标志设置为`flags`。`flags` 是`NumberFlag`枚举中的一组标志，描述了生成代码格式化的选项（例如，是否总是写出数字的基底或符号）。

### `void QTextStream::setPadChar(QChar ch)`

**作用与语义：**

将填充字符设置为`ch`。默认值为ASCII空格字符（“'”）或`QChar`（0x20）。该字符用于生成文本时填充格子。
该字符串`s`包含：

**官方示例：**

```cpp
 QString s;
 QTextStream out(&s);
 out.setFieldWidth(10);
 out.setFieldAlignment(QTextStream::AlignCenter);
 out.setPadChar('-');
 out << "Qt" << "rocks!";
```

### `void QTextStream::setRealNumberNotation(QTextStream::RealNumberNotation notation)`

**作用与语义：**

将实数符号设为`notation`（`SmartNotation`、`FixedNotation`、`ScientificNotation`）。读取和生成数字时，`QTextStream`用该值检测实数的格式化。

### `void QTextStream::setRealNumberPrecision(int precision)`

**作用与语义：**

将实数的精度设为`precision`。该值描述了`QTextStream`在生成实数时应写入的分数数字数（`FixedNotation`、`ScientificNotation`），或最大有效位数（`SmartNotation`）。
精度不能为负值。默认值为6。

### `void QTextStream::setStatus(QTextStream::Status status)`

**作用与语义：**

将文本流的状态设置为给定的 `status`。
后续对 setStatus() 的调用会被忽略，直到调用 `resetStatus()`。

### `void QTextStream::setString(QString *string, QIODeviceBase::OpenMode openMode = ReadWrite)`

**作用与语义：**

将当前字符串设置为`string`，使用给定的`openMode`。如果设备已被分配，`QTextStream`会调用`flush()`再替换。

### `void QTextStream::skipWhiteSpace()`

**作用与语义：**

读取并丢弃流中的空白，直到检测到非空格字符，或`atEnd()`返回为真。该功能在逐字符读取流时非常有用。
空白字符是指所有`QChar::isSpace()`返回`true`的字符。

### `QTextStream::Status QTextStream::status() const`

**作用与语义：**

返回文本流的状态。

### `QString *QTextStream::string() const`

**作用与语义：**

返回分配给`QTextStream`当前字符串，若未分配字符串则返回`nullptr`。

### `[explicit noexcept, since 6.10] QTextStream::operator bool() const`

**作用与语义：**

返回该流是否无错误（`status()`返回`Ok`）。

### `QTextStream &QTextStream::operator<<(QChar c)`

**作用与语义：**

将字符 `c` 写入流，然后返回指向 `QTextStream` 的引用。

### `QTextStream &QTextStream::operator<<(const QString &string)`

**作用与语义：**

将字符串`string`写入流，并返回对`QTextStream`的引用。字符串首先使用分配的编码（默认为UTF-8）编码，然后再写入流。

### `QTextStream &QTextStream::operator<<(float f)`

**作用与语义：**

将实数写入`f`流，然后返回`QTextStream`的引用。默认情况下，`QTextStream`用`SmartNotation`存储，精度最高可达6位。你可以通过调用`setRealNumberNotation()`、`setRealNumberPrecision()`和`setNumberFlags()`来更改实数`QTextStream`的文本表示。

### `QTextStream &QTextStream::operator<<(short i)`

**作用与语义：**

将整数写入`i`流，然后返回`QTextStream`的引用。默认情况下，数字以十进制形式存储，但你也可以通过调用`setIntegerBase()`来设置基位。

### `QTextStream &QTextStream::operator<<(QLatin1StringView string)`

**作用与语义：**

写入`string`流，并返回对`QTextStream`的引用。

### `QTextStream &QTextStream::operator<<(QStringView string)`

**作用与语义：**

写入`string`流，并返回对`QTextStream`的引用。

### `QTextStream &QTextStream::operator<<(char c)`

**作用与语义：**

将`c`从ASCII转换为`QChar`，然后写入流。

### `[since 6.3.1] QTextStream &QTextStream::operator<<(char16_t c)`

**作用与语义：**

将 Unicode 字符写入 `c` 流，然后返回对`QTextStream`的引用。

### `QTextStream &QTextStream::operator<<(const QByteArray &array)`

**作用与语义：**

写入`array`流。`array`内容通过 `QString::fromUtf8()` 转换。

### `QTextStream &QTextStream::operator<<(const char *string)`

**作用与语义：**

将 `string` 指向的常量字符串写入流中。假设 `string` 是 UTF-8 编码的。当处理常量字符串数据时，此运算符非常方便。例如：
警告：`QTextStream` 假设 `string` 指向以 '\0' 字符终止的文本字符串。如果没有终止的 '\0' 字符，您的应用程序可能会崩溃。

**官方示例：**

```cpp
 QTextStream out(stdout);
 out << "Qt rocks!" << Qt::endl;
```

### `QTextStream &QTextStream::operator<<(const void *ptr)`

**作用与语义：**

将`ptr`写入流，作为带底的十六进制数。

### `QTextStream &QTextStream::operator<<(double f)`

**作用与语义：**

把双重的 `f` 写入流。

### `QTextStream &QTextStream::operator<<(int i)`

**作用与语义：**

将签名的int写入流`i`。

### `QTextStream &QTextStream::operator<<(long i)`

**作用与语义：**

将签名的长 S 写入流`i`。

### `QTextStream &QTextStream::operator<<(qlonglong i)`

**作用与语义：**

写入qlonglong的`i`到流中。

### `QTextStream &QTextStream::operator<<(qulonglong i)`

**作用与语义：**

把qulonglong写`i`到溪流上。

### `QTextStream &QTextStream::operator<<(unsigned int i)`

**作用与语义：**

将未签名的 int `i`写入流。

### `QTextStream &QTextStream::operator<<(unsigned long i)`

**作用与语义：**

将未签名的长长 写入流`i`。

### `QTextStream &QTextStream::operator<<(unsigned short i)`

**作用与语义：**

将未签名的短`i`写入流。

### `QTextStream &QTextStream::operator>>(QChar &c)`

**作用与语义：**

从流中读取字符并存储在`c`中。返回`QTextStream`的引用，以便嵌套多个操作符。示例：
空白区域不会被跳过。

**官方示例：**

```cpp
 QTextStream in(file);
 QChar ch1, ch2, ch3;
 in >> ch1 >> ch2 >> ch3;
```

### `QTextStream &QTextStream::operator>>(QString &str)`

**作用与语义：**

读取流中的一个词并将其存储为`str`，然后返回流的引用。单词之间用空白分隔（即所有`QChar::isSpace()`返回`true`的字符）。
跳过前置空白。

### `QTextStream &QTextStream::operator>>(float &f)`

**作用与语义：**

从流中读取实数并存储在`f`，然后返回`QTextStream`的引用。该数字被铸造成正确类型。如果流中检测不到实数，`f`设为0.0。
作为特殊例外，`QTextStream`允许字符串“nan”和“inf”表示 NAN 和 INF 浮点数或双数点数。
跳过前置空白。

### `QTextStream &QTextStream::operator>>(short &i)`

**作用与语义：**

从流中读取一个整数并存储为`i`，然后返回对`QTextStream`的引用。数字在存储前会被铸造为正确的类型。如果流中未检测到数字，`i` 设置为 0。
默认情况下，`QTextStream`会尝试用以下规则检测该数字的底数：
- `Prefix`：基地
- `"0b" or "0B"`：2（二进制）
- `"0" followed by "0-7"`：8（八进制）
- `"0" otherwise`：10（十进制）
- `"0x" or "0X"`：16（十六进制）
- `"1" to "9"`：10（小数）
通过调用`setIntegerBase()`，你可以显式指定整数基数。这样可以禁用自动检测，并稍微加快`QTextStream`速度。
跳过前置空白。

### `QTextStream &QTextStream::operator>>(QByteArray &array)`

**作用与语义：**

将单词转换为 UTF-8，然后存储在 `array`。

### `QTextStream &QTextStream::operator>>(char &c)`

**作用与语义：**

从流中读取一个字符并将其存储在`c`中。流中的字符在存储前会转换为ISO-8859-1。

### `QTextStream &QTextStream::operator>>(char *c)`

**作用与语义：**

将单词转换为 UTF-8，并以 `c` 存储，末尾以 '\0' 字符结束。如果没有单词可用，则仅存储 '\0' 字符。
警告：虽然方便，但该操作符存在危险性，必须谨慎使用。`QTextStream`假设`c`指向一个有足够空间存储该字的缓冲区。如果缓冲区过小，你的应用程序可能会崩溃。对于由`n`个QChar组成的词，缓冲区长度至少需要`3*n+1`个字符。
如果可能的话，改用`QByteArray`操作符。

### `[since 6.4] QTextStream &QTextStream::operator>>(char16_t &c)`

**作用与语义：**

读取流中的字符并存储在`c`中。

### `QTextStream &QTextStream::operator>>(double &f)`

**作用与语义：**

将真实号码存储在双重 `f`中。

### `QTextStream &QTextStream::operator>>(int &i)`

**作用与语义：**

将整数存储在符号的整数`i`中。

### `QTextStream &QTextStream::operator>>(long &i)`

**作用与语义：**

将整数存储在带符号的长长 `i`中。

### `QTextStream &QTextStream::operator>>(qlonglong &i)`

**作用与语义：**

将整数存储在qlonglong的 qlonglong 中`i`。

### `QTextStream &QTextStream::operator>>(qulonglong &i)`

**作用与语义：**

将整数存储在qulonglong的 qulonglong `i`。

### `QTextStream &QTextStream::operator>>(unsigned int &i)`

**作用与语义：**

将整数存储在未符号的整`i`中。

### `QTextStream &QTextStream::operator>>(unsigned long &i)`

**作用与语义：**

将整数存储在无符号长长的长边中`i`。

### `QTextStream &QTextStream::operator>>(unsigned short &i)`

**作用与语义：**

将整数存储在无符号短`i`中。

### `QTextStreamManipulator qSetFieldWidth(int width)`

**作用与语义：**

相当于`QTextStream::setFieldWidth`（`width`）。

### `QTextStreamManipulator qSetPadChar(QChar ch)`

**作用与语义：**

相当于`QTextStream::setPadChar`（`ch`）。

### `QTextStreamManipulator qSetRealNumberPrecision(int precision)`

**作用与语义：**

相当于`QTextStream::setRealNumberPrecision`（`precision`）。

### `enum NumberFlag { ShowBase, ForcePoint, ForceSign, UppercaseBase, UppercaseDigits }`

**作用与语义：**

该枚举规定了各种可以设置影响整数输出的标志，包括`float`和`double`。
- `QTextStream::ShowBase`：`0x1`;如果底为16（“0x”）、8（“0”）或2（“0b”），则显示基底为前缀。
- `QTextStream::ForcePoint`：`0x2`;即使没有小数，也一定要用数字分隔符。
- `QTextStream::ForceSign`：`0x4`;符号始终用数字表示，即使是正数也一样。
- `QTextStream::UppercaseBase`：`0x8`;使用基本前缀的大写版本（“0X”、“0B”）。
- `QTextStream::UppercaseDigits`：`0x10`;用大写字母表示数字10到35，而非小写。
NumberFlags 类型是 QFlags 的 typedef<NumberFlag>。它存储 NumberFlag 值的 OR 组合。

### `flags NumberFlags`

**作用与语义：**

该枚举规定了各种可以设置影响整数输出的标志，包括`float`和`double`。
- `QTextStream::ShowBase`：`0x1`;如果底为16（“0x”）、8（“0”）或2（“0b”），则显示基底为前缀。
- `QTextStream::ForcePoint`：`0x2`;即使没有小数，也一定要用数字分隔符。
- `QTextStream::ForceSign`：`0x4`;符号始终用数字表示，即使是正数也一样。
- `QTextStream::UppercaseBase`：`0x8`;使用基本前缀的大写版本（“0X”、“0B”）。
- `QTextStream::UppercaseDigits`：`0x10`;用大写字母表示数字10到35，而非小写。
NumberFlags 类型是 QFlags 的 typedef<NumberFlag>。它存储 NumberFlag 值的 OR 组合。

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
