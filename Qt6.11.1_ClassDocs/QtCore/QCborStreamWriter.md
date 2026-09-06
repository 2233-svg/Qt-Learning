# QCborStreamWriter

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“Cbor流写入器”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QCborStreamWriter` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QCborStreamWriter>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

### 状态、生命周期和线程

**生命周期：** 先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

**状态与结果：** 把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

**线程与事件循环：** 如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

## 3. 直接使用

围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QCborStreamWriter(QByteArray *data)`
- `QCborStreamWriter(QIODevice *device)`
- `~QCborStreamWriter()`
- `void append(QByteArrayView ba)`
- `void append(QCborKnownTags tag)`
- `void append(QCborNegativeInteger n)`
- `void append(QCborSimpleType st)`
- `void append(QCborTag tag)`
- `void append(QLatin1StringView str)`
- `void append(QStringView str)`
- `(since 6.10) void append(QUtf8StringView str)`
- `void append(bool b)`
- `void append(const QByteArray &ba)`
- `void append(double d)`
- `void append(float f)`
- `void append(qfloat16 f)`
- `void append(qint64 i)`
- `void append(quint64 u)`
- `void append(std::nullptr_t)`
- `void append(const char *str, qsizetype size = -1)`
- `void appendByteString(const char *data, qsizetype len)`
- `void appendNull()`
- `void appendTextString(const char *utf8, qsizetype len)`
- `void appendUndefined()`
- `QIODevice * device() const`
- `bool endArray()`
- `bool endMap()`
- `void setDevice(QIODevice *device)`
- `void startArray()`
- `void startArray(quint64 count)`
- `void startMap()`
- `void startMap(quint64 count)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[explicit] QCborStreamWriter::QCborStreamWriter(QByteArray *data)`

**作用与语义：**

创建一个QCborStreamWriter对象，将流附加到`data`。所有流式传输直接到字节数组，无需清除任何缓冲区。
以下示例将一个数字写入字节数组，然后返回该数字。
QCborStreamWriter不对`data`拥有所有权。

**官方示例：**

```cpp
 QByteArray encodedNumber(qint64 value)
 {
     QByteArray ba;
     QCborStreamWriter writer(&ba);
     writer.append(value);
     return ba;
 }
```

### `[explicit] QCborStreamWriter::QCborStreamWriter(QIODevice *device)`

**作用与语义：**

创建一个QCborStreamWriter对象，将流写入`device`。设备必须在第一次`append()`调用前打开。该构造函数可用于任何源自`QIODevice`的类，如`QFile`、`QProcess`或`QTcpSocket`。
QCborStreamWriter 没有缓冲功能，因此每次 `append()` 调用都会对设备的 `write()` 方法进行一次或多次调用。
以下示例将一个空映射写入一个文件：
QCborStreamWriter不对`device`拥有所有权。

**官方示例：**

```cpp
 QFile f("output");
 QCborStreamWriter writer(&f);
 writer.startMap(0);
 writer.endMap();
```

### `[noexcept] QCborStreamWriter::~QCborStreamWriter()`

**作用与语义：**

摧毁该`QCborStreamWriter`对象并释放所有相关资源。
`QCborStreamWriter` 不会进行错误检查，以确认在对象被销毁前所有必需的项目是否都写入了流。程序员有责任确保这些任务被写入。

### `void QCborStreamWriter::append(QCborKnownTags tag)`

**作用与语义：**

在流后附加 CBOR 标签`tag`，创建 CBOR 标签值。所有标签后面必须跟一个类型，并为其提供意义。
在下面的例子中，我们向流添加一个CBOR Tag 1（Unix `time_t`）和一个表示当前时间的整数，这些都是通过`time()`函数获得的：

**官方示例：**

```cpp
 void writeCurrentTime(QCborStreamWriter &writer)
 {
     writer.append(QCborKnownTags::UnixTime_t);
     writer.append(qint64(time(nullptr)));
 }
```

### `void QCborStreamWriter::append(QCborNegativeInteger n)`

**作用与语义：**

将64位负值`n`附加到CBOR流中。QCborNegativeInteger是一个64位枚举，保存我们想写的负数的绝对值。如果n为零，写入的值等价于264（即-18,446,744,073,709,551,616）。
在下例中，我们写出 -1、-232 和 INT64_MIN：
注意该函数如何用于编码无法适应标准计算机64位带符号整数的数字，如`qint64`。也就是说，如果`n`大于`std::numeric_limits<qint64>::max()`或为0，则该函数表示小于`std::numeric_limits<qint64>::min()`的负数。

**官方示例：**

```cpp
 writer.append(QCborNegativeInteger(1));
 writer.append(QCborNegativeInteger(Q_INT64_C(4294967296)));
 writer.append(QCborNegativeInteger(-quint64(std::numeric_limits<qint64>::min())));
```

### `void QCborStreamWriter::append(QCborSimpleType st)`

**作用与语义：**

将 CBOR 简单类型 `st` 附加到流中，生成 CBOR 简单类型值。在下例中，我们将 Null 和类型 32 分别写出简单类型，而 Qt 不支持类型 32。
注意：使用无规范的简单类型可能导致远程接收方的验证错误。此外，简单类型值24至31（含）被保留，不得使用。

**官方示例：**

```cpp
 writer.append(QCborSimpleType::Null);
 writer.append(QCborSimpleType(32));
```

### `void QCborStreamWriter::append(QCborTag tag)`

**作用与语义：**

将 CBOR 标签 `tag` 附加到流后，创建 CBOR 标签值。所有标签后面必须跟一个类型，并为其提供意义。
在下例中，我们在流中附加一个CBOR Tag 36（正则表达式）和一个`QRegularExpression`的模式：

**官方示例：**

```cpp
 void writeRxPattern(QCborStreamWriter &writer, const QRegularExpression &rx)
 {
     writer.append(QCborTag(36));
     writer.append(rx.pattern());
 }
```

### `void QCborStreamWriter::append(QLatin1StringView str)`

**作用与语义：**

将`str` 查看的 Latin-1 字符串附加到流中，创建 CBOR 文本字符串值。`QCborStreamWriter` 尝试将整个字符串写入一个区块。
以下示例在流中附加了一个简单的拉丁1字符串字面：
性能说明：CBOR 要求所有文本字符串都以 UTF-8 编码，因此该函数会遍历字符串中的字符，以判断内容是否为 US-ASCII。如果发现字符串包含 US-ASCII 以外的字符，它将分配内存并转换为 UTF-8。如果不需要此检查，请使用 `appendTextString()` 代替 overload take a `QUtf8StringView`。

**官方示例：**

```cpp
 using namespace Qt::StringLiterals;
 // ...
 writer.append("Hello, World"_L1);
```

### `void QCborStreamWriter::append(QStringView str)`

**作用与语义：**

将文本字符串`str`附加到流中，生成 CBOR 文本字符串值。`QCborStreamWriter` 尝试将整个字符串写入一个区块。
以下示例为流写入任意`QString`：

**官方示例：**

```cpp
 void writeString(QCborStreamWriter &writer, const QString &str)
 {
     writer.append(str);
 }
```

### `[since 6.10] void QCborStreamWriter::append(QUtf8StringView str)`

**作用与语义：**

将`str`查看的UTF-8字符串附加到流中，创建CBOR文本字符串值。`QCborStreamWriter`会尝试将整个字符串写入一个分块。

### `void QCborStreamWriter::append(bool b)`

**作用与语义：**

将`b`的布尔值附加到流中，生成CBOR False值或CBOR True值。该函数等价于（并实现为）：

**官方示例：**

```cpp
 writer.append(b ? QCborSimpleType::True : QCborSimpleType::False);
```

### `void QCborStreamWriter::append(QByteArrayView ba)`

**作用与语义：**

将`ba`字节数组附加到流中，生成一个 CBOR 字节字符串值。`QCborStreamWriter` 尝试将整个字符串写入一个分块。
以下示例将加载并附加文件内容到流中：
正如示例所示，与JSON不同，CBOR对二进制内容不要求跳出。
注意：超载加持`QByteArrayView`自第6.10季度起就已存在。

**官方示例：**

```cpp
 void writeFile(QCborStreamWriter &writer, const QString &fileName)
 {
     QFile f(fileName);
     if (f.open(QIODevice::ReadOnly))
         writer.append(f.readAll());
 }
```

### `void QCborStreamWriter::append(double d)`

**作用与语义：**

将`ba`字节数组附加到流中，生成一个 CBOR 字节字符串值。`QCborStreamWriter` 尝试将整个字符串写入一个分块。
以下示例将加载并附加文件内容到流中：
正如示例所示，与JSON不同，CBOR对二进制内容不要求跳出。
注意：超载加持`QByteArrayView`自第6.10季度起就已存在。

**官方示例：**

```cpp
 void writeFile(QCborStreamWriter &writer, const QString &fileName)
 {
     QFile f(fileName);
     if (f.open(QIODevice::ReadOnly))
         writer.append(f.readAll());
 }
```

### `void QCborStreamWriter::append(float f)`

**作用与语义：**

将浮点数`d`附加到流中，生成一个CBOR 64位双精度浮点值。`QCborStreamWriter`总是按原样附加数字，不检查该数字是NaN的典范形式、无限形态、是否非正规或是否可以用更短格式写成。
以下代码执行了所有这些检查，唯独不包括非正规检查，系统浮点计算单元或浮点仿真应直接考虑该检查。
判断是否可以将重叠映射转换为积分而不丢失精度，则留给读者来做一个练习。

**官方示例：**

```cpp
 void writeDouble(QCborStreamWriter &writer, double d)
 {
     float f;
     if (qIsNaN(d)) {
         writer.append(qfloat16(qQNaN()));
     } else if (qIsInf(d)) {
         writer.append(d < 0 ? -qInf() : qInf());
     } else if ((f = d) == d) {
         qfloat16 f16 = qfloat16(f);
         if (f16 == f)
             writer.append(f16);
         else
             writer.append(f);
     } else {
         writer.append(d);
     }
 }
```

### `void QCborStreamWriter::append(qfloat16 f)`

**作用与语义：**

将浮点数`f`附加到流后，生成CBOR 32位单精度浮点值。如果精度不损失，以下代码可用于将C `double`转换为`float`并附加，或者直接附加`double`。

**官方示例：**

```cpp
 void writeFloat(QCborStreamWriter &writer, double d)
 {
     float f = d;
     if (qIsNaN(d) || d == f)
         writer.append(f);
     else
         writer.append(d);
 }
```

### `void QCborStreamWriter::append(qint64 i)`

**作用与语义：**

将浮点数`f`附加到流中，生成一个CBOR 16位半精度浮点值。以下代码可用于将C `float`转换为`qfloat16`，如果精度不损失并附加，或者直接附加`float`。

**官方示例：**

```cpp
 void writeFloat(QCborStreamWriter &writer, float f)
 {
     qfloat16 f16 = qfloat16(f);
     if (qIsNaN(f) || f16 == f)
         writer.append(f16);
     else
         writer.append(f);
 }
```

### `void QCborStreamWriter::append(quint64 u)`

**作用与语义：**

将64位带符号值`i`附加到CBOR流中。这将根据参数符号生成CBOR无符号整数或CBOR负整数值。在下例中，我们写入0、-1、232和`INT64_MAX`：

**官方示例：**

```cpp
 writer.append(0);
 writer.append(-1);
 writer.append(Q_INT64_C(4294967296));
 writer.append(std::numeric_limits<qint64>::max());
```

### `void QCborStreamWriter::append(std::nullptr_t)`

**作用与语义：**

将64位无符号值`u`附加到CBOR流中，生成一个CBOR无符号整数值。在以下示例中，我们写入0、232和`UINT64_MAX`：

**官方示例：**

```cpp
 writer.append(0U);
 writer.append(Q_UINT64_C(4294967296));
 writer.append(std::numeric_limits<quint64>::max());
```

### `void QCborStreamWriter::append(const char *str, qsizetype size = -1)`

**作用与语义：**

在流中附加一个CBOR Null值。该函数等价于（并实现为）：忽略该参数。

**官方示例：**

```cpp
 writer.append(QCborSimpleType::Null);
```

### `void QCborStreamWriter::appendByteString(const char *data, qsizetype len)`

**作用与语义：**

从`data`开始`len`字节的数据附加到流中，生成一个CBOR字节字符串值。`QCborStreamWriter`尝试将整个字符串写入一个区块。

### `void QCborStreamWriter::appendNull()`

**作用与语义：**

在流中附加一个CBOR空值。该函数等价于（并实现为）：

**官方示例：**

```cpp
 writer.append(QCborSimpleType::Null);
```

### `void QCborStreamWriter::appendTextString(const char *utf8, qsizetype len)`

**作用与语义：**

从`utf8`开始附加 `len` 字节的文本到流中，创建 CBOR 文本字符串值。`QCborStreamWriter` 会尝试将整个字符串写入一个区块。
`utf8`指向的字符串应被正确编码为UTF-8。`QCborStreamWriter`未进行验证。

### `void QCborStreamWriter::appendUndefined()`

**作用与语义：**

在流中附加一个CBOR未定义值。该函数等价于（并实现为）：

**官方示例：**

```cpp
 writer.append(QCborSimpleType::Undefined);
```

### `QIODevice *QCborStreamWriter::device() const`

**作用与语义：**

返回该`QCborStreamWriter`对象写入的`QIODevice`。设备必须先用构造函数或`setDevice()`设置过。
如果该对象是通过写入`QByteArray`创建的，该函数将返回一个内部实例`QBuffer`，该实例归`QCborStreamWriter`所有。

### `bool QCborStreamWriter::endArray()`

**作用与语义：**

终止由任一 `startArray()` 重载启动的数组，若数组中元素数正确，则返回为真。该函数必须对每个使用的`startArray()`调用。
返回false表示应用有误，该流则为无法恢复的错误。如果发生这种情况，`QCborStreamWriter`也会用`qWarning()`写警告。
当当前容器不是数组时调用该函数也是错误，尽管`QCborStreamWriter`目前无法检测到此状态。

### `bool QCborStreamWriter::endMap()`

**作用与语义：**

终止由 `startMap()` 的任意重载启动的映射，如果正确数量的元素被添加到数组中，则返回 true。每次使用 `startMap()` 时，必须调用此函数。
返回 false 表示应用程序错误以及此流中的不可恢复错误。如果发生这种情况，`QCborStreamWriter` 也会使用 `qWarning()` 发出警告。
在当前容器不是映射时调用此函数也是错误，不过 `QCborStreamWriter` 目前无法检测此情况。

### `void QCborStreamWriter::setDevice(QIODevice *device)`

**作用与语义：**

用`device`替换该`QCborStreamWriter`对象正在写入的设备或字节阵列。

### `void QCborStreamWriter::startArray()`

**作用与语义：**

在 CBOR 流中启动一个长度不确定的 CBOR 数组。每次调用 startArray() 都必须配对一个 `endArray()` 调用，并且当前 CBOR 元素一直延伸到数组末尾。该函数创建的数组没有明确的长度，其长度由其中包含的元素决定。然而，请注意，使用长度不确定的数组不符合规范的 CBOR 编码。下面的示例将附加作为输入传入的字符串列表中的元素：

**官方示例：**

```cpp
 void appendList(QCborStreamWriter &writer, const QList<QString> &values)
 {
     writer.startArray();
     for (const QString &s : values)
         writer.append(s);
     writer.endArray();
 }
```

### `void QCborStreamWriter::startArray(quint64 count)`

**作用与语义：**

启动一个 CBOR 数组，其 CBOR 流中显式的 `count` 项长度。每个 startArray 调用必须与一个 `endArray()` 调用配对，当前 CBOR 元素会延伸到数组结束。
该函数创建的数组有显式长度，因此必须精确添加`count`项到CBOR流中。添加更少或增加的项会导致`endArray()`失败，CBOR流会损坏。然而，典型的CBOR编码要求显式长度的数组。
以下示例附加了作为输入传递的`QStringList`中所有字符串：
大小限制：该函数的参数为quint64，似乎允许数组中最多264-1个元素。然而，目前32位系统上`QCborStreamWriter`和`QCborStreamReader`都限制为232-2个元素，64位系统限制为264-2个元素。还请注意，`QCborArray`目前在32位平台上限制为227个元素，在64位平台上限制为259个元素。

**官方示例：**

```cpp
 void appendList(QCborStreamWriter &writer, const QStringList &list)
 {
     writer.startArray(list.size());
     for (const QString &s : list)
         writer.append(s);
     writer.endArray();
 }
```

### `void QCborStreamWriter::startMap()`

**作用与语义：**

在 CBOR 流中启动一个长度不确定的 CBOR 映射。每次 startMap() 调用必须配对一个 `endMap()` 调用，并且当前 CBOR 元素一直延伸到映射末尾。该函数创建的映射没有明确长度，其长度由其中包含的元素决定。然而，请注意，使用长度不确定的映射不符合规范的 CBOR 编码（规范编码还要求键唯一且按顺序排列）。下面的示例将附加作为输入传入的整数和字符串对列表中的元素：

**官方示例：**

```cpp
 void appendMap(QCborStreamWriter &writer, const QList<std::pair<int, QString>> &values)
 {
     writer.startMap();
     for (const auto pair : values) {
         writer.append(pair.first);
         writer.append(pair.second);
     }
     writer.endMap();
 }
```

### `void QCborStreamWriter::startMap(quint64 count)`

**作用与语义：**

在 CBOR 流中启动一个具有 `count` 项明确长度的 CBOR 映射。每次 startMap 调用必须配对一个 `endMap()` 调用，并且当前 CBOR 元素一直延伸到映射末尾。该函数创建的映射具有明确长度，因此必须向 CBOR 流中添加恰好 `count` 对项。添加较少或较多的项将在 `endMap()` 期间导致失败，并且会破坏 CBOR 流。然而，规范的 CBOR 编码要求使用明确长度的映射。下面的示例将附加在输入 `QMap` 中找到的所有字符串：
大小限制：首页参数为 quint64，这似乎允许映射中最多有 2^64-1 对。然而，目前 `QCborStreamWriter` 和 `QCborStreamReader` 在 32 位系统上限制为 2^31-1 项，在 64 位系统上限制为 2^63-1 项。还要注意，`QCborMap` 目前在 32 位平台上限制为 2^26 个元素，在 64 位平台上限制为 2^58 个元素。

**官方示例：**

```cpp
 void appendMap(QCborStreamWriter &writer, const QMap<int, QString> &map)
 {
     writer.startMap(map.size());
     for (auto it = map.cbegin(), end = map.cend(); it != end; ++it) {
         writer.append(it.key());
         writer.append(it.value());
     }
     writer.endMap();
 }
```

### `void append(const QByteArray &ba)`

**作用与语义：**

从`str`开始，向流中添加`size`字节文本，创建CBOR文本字符串值。`QCborStreamWriter`尝试将整个字符串写入一个分块。如果`size`为-1，该函数将写入`strlen(\a str)`字节。
`str`指向的字符串预期为正确编码的UTF-8。`QCborStreamWriter`未对此进行验证。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

### 状态和错误边界

把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

### 线程边界

如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

### 最容易出现的错误

不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QCborStreamWriter` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
