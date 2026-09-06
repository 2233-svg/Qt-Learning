# QCborStreamReader

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“Cbor流读取器”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QCborStreamReader` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QCborStreamReader>`
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

### 公有类型

- `struct StringResult`
- `enum StringResultCode { EndOfString, Ok, Error }`
- `enum Type { UnsignedInteger, NegativeInteger, ByteArray, ByteString, String, …, Invalid }`

### 公有函数

- `QCborStreamReader()`
- `QCborStreamReader(QIODevice *device)`
- `QCborStreamReader(const QByteArray &data)`
- `QCborStreamReader(const char *data, qsizetype len)`
- `QCborStreamReader(const quint8 *data, qsizetype len)`
- `~QCborStreamReader()`
- `void addData(const QByteArray &data)`
- `void addData(const char *data, qsizetype len)`
- `void addData(const quint8 *data, qsizetype len)`
- `void clear()`
- `int containerDepth() const`
- `qint64 currentOffset() const`
- `qsizetype currentStringChunkSize() const`
- `QIODevice * device() const`
- `bool enterContainer()`
- `bool hasNext() const`
- `bool isArray() const`
- `bool isBool() const`
- `bool isByteArray() const`
- `bool isContainer() const`
- `bool isDouble() const`
- `bool isFalse() const`
- `bool isFloat16() const`
- `bool isFloat() const`
- `bool isInteger() const`
- `bool isInvalid() const`
- `bool isLengthKnown() const`
- `bool isMap() const`
- `bool isNegativeInteger() const`
- `bool isNull() const`
- `bool isSimpleType() const`
- `bool isSimpleType(QCborSimpleType st) const`
- `bool isString() const`
- `bool isTag() const`
- `bool isTrue() const`
- `bool isUndefined() const`
- `bool isUnsignedInteger() const`
- `bool isValid() const`
- `QCborError lastError() const`
- `bool leaveContainer()`
- `quint64 length() const`
- `bool next(int maxRecursion = 10000)`
- `QCborStreamReader::Type parentContainerType() const`
- `(since 6.7) QByteArray readAllByteArray()`
- `(since 6.7) QString readAllString()`
- `(since 6.7) QByteArray readAllUtf8String()`
- `(since 6.7) bool readAndAppendToByteArray(QByteArray &dst)`
- `(since 6.7) bool readAndAppendToString(QString &dst)`
- `(since 6.7) bool readAndAppendToUtf8String(QByteArray &dst)`
- `QCborStreamReader::StringResult<QByteArray> readByteArray()`
- `QCborStreamReader::StringResult<QString> readString()`
- `QCborStreamReader::StringResult<qsizetype> readStringChunk(char *ptr, qsizetype maxlen)`
- `(since 6.7) QCborStreamReader::StringResult<QByteArray> readUtf8String()`
- `void reparse()`
- `void reset()`
- `void setDevice(QIODevice *device)`
- `bool toBool() const`
- `double toDouble() const`
- `qfloat16 toFloat16() const`
- `float toFloat() const`
- `qint64 toInteger() const`
- `QCborNegativeInteger toNegativeInteger() const`
- `QCborSimpleType toSimpleType() const`
- `QCborTag toTag() const`
- `quint64 toUnsignedInteger() const`
- `QCborStreamReader::Type type() const`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QCborStreamReader::StringResultCode`

**作用与语义：**

该枚举通过`readString()`和`readByteArray()`返回，用以表示解析状态。
- `QCborStreamReader::EndOfString`：`0`;字符串的解析完成且无错误。
- `QCborStreamReader::Ok`：`1`;函数返回数据;没有错误。
- `QCborStreamReader::Error`：`-1`;解析失败，出现错误。

### `enum QCborStreamReader::Type`

**作用与语义：**

该枚举包含了所有可能的CBOR类型，并由`QCborStreamReader`解码。CBOR有7个主要类型，以及一些无值的简单类型和浮点值。
- `QCborStreamReader::UnsignedInteger`：`0x00`;（主要类型0）范围为0至264 - 1（18,446,744,073,709,551,616）
- `QCborStreamReader::NegativeInteger`：`0x20`;（主要类型1）范围为-1至-264（-18,446,744,073,709,551,616）
- `QCborStreamReader::ByteArray`：`ByteString`;（主要类型2）任意二进制数据。
- `QCborStreamReader::ByteString`：`0x40`;字节阵列的别名。
- `QCborStreamReader::String`：`TextString`;（主要类型3）Unicode文本，可能包含NUL。
- `QCborStreamReader::TextString`：`0x60`;弦的别名
- `QCborStreamReader::Array`：`0x80`;（主要类型4）异构项目阵列。
- `QCborStreamReader::Map`：`0xa0`;（主要类型5）异质项地图/词典。
- `QCborStreamReader::Tag`：`0xc0`;（主类型6）数字为通用CBOR项提供更多语义价值。更多信息请参见 `QCborTag`。
- `QCborStreamReader::SimpleType`：`0xe0`;（主要类型7）不具其他取值的类型。包括布尔（真和假）、空、未定义。
- `QCborStreamReader::Float16`：`HalfFloat`;IEEE 754半精度浮点（`qfloat16`）。
- `QCborStreamReader::HalfFloat`：`0xf9`;Float16的别名。
- `QCborStreamReader::Float`：`0xfa`;IEEE 754单精度浮点（`float`）。
- `QCborStreamReader::Double`：`0xfb`;IEEE 754 双精度浮点（`double`）。
- `QCborStreamReader::Invalid`：`0xff`;不是一个有效的类型，可能是由于解析错误，也可能是到达数组或映射的末尾。

### `QCborStreamReader::QCborStreamReader()`

**作用与语义：**

创建一个没有源数据的 QCborStreamReader 对象。构建完成后，QCborStreamReader 会报告一次错误解析。
你可以通过调用`addData()`或用`setDevice()`设置不同的源设备来添加更多数据。

### `[explicit] QCborStreamReader::QCborStreamReader(QIODevice *device)`

**作用与语义：**

创建一个QCborStreamReader对象，解析通过读取`device`找到的CBOR流。QCborStreamReader不拥有`device`，因此该对象必须保持有效，直到该对象被销毁。

### `[explicit] QCborStreamReader::QCborStreamReader(const QByteArray &data)`

**作用与语义：**

创建一个QCborStreamReader对象，解析`data`中发现的CBOR流。

### `QCborStreamReader::QCborStreamReader(const char *data, qsizetype len)`

**作用与语义：**

创建一个QCborStreamReader对象，数据从`data`开始`len`字节。指针必须保持有效，直到QCborStreamReader被销毁。

### `QCborStreamReader::QCborStreamReader(const quint8 *data, qsizetype len)`

**作用与语义：**

创建一个QCborStreamReader对象，数据从`data`开始`len`字节。指针必须保持有效，直到QCborStreamReader被销毁。

### `[noexcept] QCborStreamReader::~QCborStreamReader()`

**作用与语义：**

摧毁该`QCborStreamReader`对象并释放所有相关资源。

### `void QCborStreamReader::addData(const QByteArray &data)`

**作用与语义：**

向CBOR流添加`data`并重新解析当前元素。当数据在处理流时已到达数据终点，但现在有更多数据可用，此功能非常有用。

### `void QCborStreamReader::addData(const char *data, qsizetype len)`

**作用与语义：**

向CBOR流添加`len`字节，从`data`开始，并对当前元素进行解析。如果之前在处理数据流时到达了数据的终点，但现在有更多数据可用，这个功能非常有用。

### `void QCborStreamReader::addData(const quint8 *data, qsizetype len)`

**作用与语义：**

向CBOR流添加`len`字节，从`data`开始，并对当前元素进行解析。如果之前在处理数据流时到达了数据的终点，但现在有更多数据可用，这个功能非常有用。

### `void QCborStreamReader::clear()`

**作用与语义：**

清除解码器状态并将输入源数据重置为空字节数组。调用此函数后，`QCborStreamReader` 将指示解析错误。
调用 `addData()` 可添加更多待解析数据。

### `int QCborStreamReader::containerDepth() const`

**作用与语义：**

返回该流已进入但尚未离开的容器数量`enterContainer()`。

### `qint64 QCborStreamReader::currentOffset() const`

**作用与语义：**

返回当前解码项目输入流中的偏移量。当前偏移量仅在源数据为`QByteArray`或解码开始时位于起始位置的`QIODevice`时，才表示已解码的字节数。

### `qsizetype QCborStreamReader::currentStringChunkSize() const`

**作用与语义：**

返回当前文本或字节字符串块的大小。如果CBOR流包含非分块字符串（即返回`isLengthKnown()`返回`true`），该函数返回整个字符串的大小，与`length()`相同。
该函数有助于预分配可以传递给`readStringChunk()`的缓冲区。

### `QIODevice *QCborStreamReader::device() const`

**作用与语义：**

返回用 `setDevice()` 或 `QCborStreamReader` 构造函数设置的 `QIODevice`。如果该对象读取 `QByteArray`，则返回 nullptr。

### `bool QCborStreamReader::enterContainer()`

**作用与语义：**

进入当前项的数组或映射，并准备迭代容器中包含的元素。如果成功进入容器返回 true，否则返回 false（通常是解析错误）。每次调用 enterContainer() 都必须与调用 `leaveContainer()` 配对。
仅当当前项为数组或映射时（即 `isArray()`、`isMap()` 或 `isContainer()` 为真）才可以调用此函数。在其他条件下调用是错误的。

### `[noexcept] bool QCborStreamReader::hasNext() const`

**作用与语义：**

如果当前容器中还有更多需要解码的项，则返回 true;如果已经到达，则返回 false。如果我们解析根元素，return为false表示解析完成;否则，如果容器深度非零，则外部代码需要调用`leaveContainer()`。

### `bool QCborStreamReader::isArray() const`

**作用与语义：**

如果当前元素的类型是数组（即返回`type()`返回`QCborStreamReader::Array`），则返回为真。如果该函数返回为真，你可以调用`enterContainer()`开始解析该容器。
当当前元素是数组时，你也可以调用 `isLengthKnown()` 来确定数组大小是否在 CBOR 流中显式。如果显式，可以通过调用 `length()` 获得该大小。
以下示例根据数组大小预分配一个`QVariantList`，以实现更高效的解码：
注意：上述代码并未验证长度是否合理。如果输入流报告长度为10亿元素，上述函数会尝试分配约16GB或更多的内存，可能导致崩溃。

**官方示例：**

```cpp
 QVariantList populateFromCbor(QCborStreamReader &reader)
 {
     QVariantList list;
     if (reader.isLengthKnown())
         list.reserve(reader.length());

     reader.enterContainer();
     while (reader.lastError() == QCborError::NoError && reader.hasNext())
         list.append(readOneElement(reader));
     if (reader.lastError() == QCborError::NoError)
         reader.leaveContainer();

     return list;
 }
```

### `bool QCborStreamReader::isBool() const`

**作用与语义：**

如果当前元素是布尔值（`true`或 `false`），返回真;如果是其他值，则返回假。如果该函数返回真，你可以调用 `toBool()` 来获取布尔值。你也可以调用 `toSimpleType()`，并与 QCborSimpleValue：：True 或 QCborSimpleValue：：False 进行比较。

### `bool QCborStreamReader::isByteArray() const`

**作用与语义：**

如果当前元素类型是字节数组（即返回`type()`返回`QCborStreamReader::ByteArray`），则返回为真。如果该函数返回为真，你可以调用`readByteArray()`读取该数据。

### `bool QCborStreamReader::isContainer() const`

**作用与语义：**

如果当前元素是容器（即数组或映射），则返回真;如果是其他元素，则返回 false。如果当前元素是容器，可以使用`isLengthKnown()`函数来确定容器大小是否在流中显式，如果是，可以用 `length()` 来获得该大小。
更重要的是，对于容器，`enterContainer()`函数可以开始遍历其中的元素。

### `bool QCborStreamReader::isDouble() const`

**作用与语义：**

如果当前元件类型是IEEE 754双精度浮点（即返回`type()`返回`QCborStreamReader::Double`，则返回真。如果该函数返回真，你可以调用`toDouble()`读取该数据。

### `bool QCborStreamReader::isFalse() const`

**作用与语义：**

如果当前元素是`false`值，则返回真;如果是其他值，则返回假。

### `bool QCborStreamReader::isFloat16() const`

**作用与语义：**

如果当前元件类型是IEEE 754半精度浮点（即返回`QCborStreamReader::Float16`，则返回真`type()`）。如果该函数返回真，你可以调用`toFloat16()`读取该数据。

### `bool QCborStreamReader::isFloat() const`

**作用与语义：**

如果当前元素类型是IEEE 754单精度浮点（即返回`QCborStreamReader::Float`，则返回真`type()`）。如果该函数返回真，你可以调用`toFloat()`读取该数据。

### `bool QCborStreamReader::isInteger() const`

**作用与语义：**

如果当前元素的类型是无符号整数或负数（即返回`type()` `QCborStreamReader::UnsignedInteger`或 `QCborStreamReader::NegativeInteger`），则返回真。如果该函数返回真，你可以调用`toInteger()`读取该值。

### `bool QCborStreamReader::isInvalid() const`

**作用与语义：**

如果当前元素无效，则返回真，否则返回假。如果存在解码错误，或者我们刚刚解析了数组或映射中的最后一个元素，当前元素可能无效。
注意：该函数不应与`isNull()`混淆。空是一种正常的CBOR类型，应用程序必须处理。

### `[noexcept] bool QCborStreamReader::isLengthKnown() const`

**作用与语义：**

如果已知当前数组、映射、字节数组或字符串的长度（在CBOR流中明确表示），返回true，否则返回false。只有当元素属于这些元素时才应调用该函数。
如果已知长度，可以通过调用 `length()` 得到。
如果未知映射或数组的长度，则由流中元素的数量推断。`QCborStreamReader` 没有 API 来计算该条件下的长度。
字符串和字节数组也可能具有不确定长度（即它们可以分多个块传输）。目前这些数据块无法用`QCborStreamWriter`创建，但可以用其他编码器创建，因此`QCborStreamReader`支持它们。

### `bool QCborStreamReader::isMap() const`

**作用与语义：**

如果当前元素的类型是映射（即返回 `type()` 返回 `QCborStreamReader::Map`），则返回 true。如果该函数返回为真，你可以调用 `enterContainer()` 开始解析该容器。
当当前元素是映射时，你还可以调用 `isLengthKnown()`，以确定该映射的大小是否在 CBOR 流中显式。如果是，可以通过调用 `length()` 获得该大小。
以下示例预先分配一个`QVariantMap`，给定映射大小以实现更高效的解码：
上述示例使用了一个称为`readElementAsString`的函数来读取映射的密钥并获得字符串。这是因为CBOR映射可以包含任意类型的键，而不仅仅是字符串。用户代码需要执行这种转换，拒绝非字符串键，或者使用除`QVariantMap`和`QVariantHash`以外的其他容器。例如，如果映射预期包含整数键，这推荐以减少流规模和解析，那么正确的容器应是`\l{QMap}<int, QVariant>`或`\l{QHash}<int, QVariant>`。
注意：上述代码并未验证长度是否合理。如果输入流报告长度为10亿个元素，上述函数会尝试分配约24GB或更多的内存，这可能导致崩溃。

**官方示例：**

```cpp
 QVariantMap populateFromCbor(QCborStreamReader &reader)
 {
     QVariantMap map;
     if (reader.isLengthKnown())
         map = setMapLength(map, reader.length());

     reader.enterContainer();
     while (reader.lastError() == QCborError::NoError && reader.hasNext()) {
         QString key = readElementAsString(reader);
         map.insert(key, readOneElement(reader));
     }
     if (reader.lastError() == QCborError::NoError)
         reader.leaveContainer();

     return map;
 }
```

### `bool QCborStreamReader::isNegativeInteger() const`

**作用与语义：**

如果当前元素的类型为负整数（即 `type()`返回 `QCborStreamReader::NegativeInteger`），则返回 true。如果该函数返回 true，你可以调用 `toNegativeInteger()` 或 `toInteger()` 读取该值。

### `bool QCborStreamReader::isNull() const`

**作用与语义：**

如果当前元素是`null`值，则返回真;如果是其他值，则返回假。空值可用于表示某些可选数据的缺失。
注意：该函数并非`isValid()`的反义词。Null值是有效的CBOR值。

### `bool QCborStreamReader::isSimpleType() const`

**作用与语义：**

如果当前元素的类型是任意 CBOR 简单类型，包括布尔值（真和假）以及空和未定义，则返回真。要确定该简单类型，请调用 `toSimpleType()`。或者，为了测试某个特定的简单类型，调用取 `QCborSimpleType` 参数的超载。
CBOR 简单类型是指不携带额外值的类型。有 255 种可能性，但目前只有四个有明确意义的值。代码不被期望处理未知的简单类型，如果发现未知的简单类型，可能会直接丢弃该流为无效。

### `bool QCborStreamReader::isSimpleType(QCborSimpleType st) const`

**作用与语义：**

如果当前元素的类型是简单类型 `st`，则返回真;否则返回 false。如果该函数返回真，则返回`toSimpleType()`返回 `st`。
CBOR 简单类型是指不携带额外值的类型。有 255 种可能性，但目前只有四个有明确意义的值。代码不被期望处理未知的简单类型，如果发现未知的简单类型，可能会直接丢弃该流为无效。

### `bool QCborStreamReader::isString() const`

**作用与语义：**

如果当前元素的类型是文本字符串（即返回`type()`返回`QCborStreamReader::String`），则返回为真。如果该函数返回为真，你可以调用`readString()`读取该数据。

### `bool QCborStreamReader::isTag() const`

**作用与语义：**

如果当前元素类型是 CBOR 标签（即 返回 `type()` 返回 `QCborStreamReader::Tag`），则返回 true。如果该函数返回为真，你可以调用 `toTag()` 读取该数据。

### `bool QCborStreamReader::isTrue() const`

**作用与语义：**

如果当前元素是`true`值，则返回真;如果是其他值，则返回假。

### `bool QCborStreamReader::isUndefined() const`

**作用与语义：**

如果当前元素是`undefined`值，则返回真;如果是其他值，则返回假。未定义的值可以被编码为表示在创建流时某些转换失败或无法实现。`QCborStreamReader`从不进行任何替换，且该函数仅在流包含显式未定义值时返回真。

### `bool QCborStreamReader::isUnsignedInteger() const`

**作用与语义：**

如果当前元素的类型是无符号整数（即 返回 `QCborStreamReader::UnsignedInteger`，则返回真`type()`）。如果该函数返回真，你可以调用 `toUnsignedInteger()` 或 `toInteger()` 读取该值。

### `bool QCborStreamReader::isValid() const`

**作用与语义：**

如果当前元素有效，则返回 true，否则返回 false。如果当前元素存在解码错误，或者我们刚刚解析了数组或映射中的最后一个元素，当前元素可能无效。
注意：该函数与`isNull()`的相反。Null 是应用程序必须处理的正常 CBOR 类型。

### `QCborError QCborStreamReader::lastError() const`

**作用与语义：**

返回解码流中最后一次错误（如有）。如果未遇到错误，返回`QCborError::NoError`。

### `bool QCborStreamReader::leaveContainer()`

**作用与语义：**

离开正在处理的数组或映射，并将解码器定位在容器结束后的下一个项目。如果成功离开容器，则返回true，否则返回false（通常是解析错误）。每次调用`enterContainer()`都必须与对leaveContainer()的调用配对。
只有当`hasNext()`返回false且`containerDepth()`不是零时，才能调用该函数。在其他条件下调用该函数则为错误。

### `quint64 QCborStreamReader::length() const`

**作用与语义：**

返回字符串或字节数组的长度，或数组中的项数，或如果已知的话，映射中条目对的数量。如果长度未知（即返回 false，`isLengthKnown()`，则不应调用该函数）。这样做是错误，会导致`QCborStreamReader`停止解析输入流。

### `bool QCborStreamReader::next(int maxRecursion = 10000)`

**作用与语义：**

先推进 CBOR 流解码一个元素。通常在解析固定宽度基本元素（即整数、简单值、标签和浮点值）时应调用这个函数。但当当前项是字符串、数组或映射时，也可以调用这个函数，并且会跳过整个元素，包括所有包含的元素。
如果推进成功，该函数返回true，否则返回false。如果流损坏、不完整，或数组和映射的嵌套层级超过`maxRecursion`，则该函数可能会失败。当`hasNext()`返回false时调用该函数也是错误。如果该函数返回false，`lastError()`会返回详细说明失败原因的错误代码。

### `QCborStreamReader::Type QCborStreamReader::parentContainerType() const`

**作用与语义：**

返回`QCborStreamReader::Array`或`QCborStreamReader::Map`，分别表示当前项目的容器是数组还是映射。如果我们当前解析根元素，该函数返回`QCborStreamReader::Invalid`。

### `[since 6.7] QByteArray QCborStreamReader::readAllByteArray()`

**作用与语义：**

解码当前字节串并返回。如果字符串被分块，该函数会遍历所有块并串接它们。如果发生错误，该函数返回默认构造的QByteArray()，但这可能与某些空字节串无法区分。相反，检查`lastError()`以确定是否发生了错误。
该函数不进行任何类型转换，包括整数或字符串的转换。因此，只有当 `isByteArray()` 为真时才能调用;在其他条件下调用是错误。
注意：此功能不可恢复。也就是说，该功能不应用于可能仍接收CBOR数据的情境，例如从套接字或管道接收。只有在完整数据已接收且输入`QByteArray`或输入`QIODevice`中可用时，才应使用此功能。

### `[since 6.7] QString QCborStreamReader::readAllString()`

**作用与语义：**

解码当前文本字符串并返回。如果字符串被分块，该函数会遍历所有分块并连接它们。如果发生错误，该函数返回默认构造的QString()，但这可能与某些空文本字符串无法区分。相反，检查`lastError()`以确定是否发生了错误。
该函数不执行任何类型转换，包括从整数或字节数组进行。因此，只有当`isString()`返回为真时才可调用;在其他条件下调用则为错误。
注意：该功能不可恢复。也就是说，该功能不应用于可能仍接收 CBOR 数据的上下文，例如来自套接字或管道。只有在完整数据已被接收且输入`QByteArray`或 `QIODevice` 中可用时，才应使用。

### `[since 6.7] QByteArray QCborStreamReader::readAllUtf8String()`

**作用与语义：**

解码当前文本字符串并返回。如果字符串被分块，该函数会遍历所有分块并连接它们。如果发生错误，该函数返回默认构造的QString()，但这可能与某些空文本字符串无法区分。相反，检查`lastError()`以确定是否发生了错误。
该函数不执行任何类型转换，包括从整数或字节数组进行。因此，只有当`isString()`返回为真时才可调用;在其他条件下调用则为错误。
注意：该功能不可恢复。也就是说，该功能不应用于可能仍接收 CBOR 数据的上下文，例如来自套接字或管道。只有在完整数据已被接收且输入`QByteArray`或 `QIODevice` 中可用时，才应使用。

### `[since 6.7] bool QCborStreamReader::readAndAppendToByteArray(QByteArray &dst)`

**作用与语义：**

解码当前字节串并附加到`dst`。如果字符串被分块，该函数会遍历所有分块并串接它们。如果解码过程中出现错误，其他本可成功解码的分块可能仍然写入`dst`。如果解码没有错误，返回`true`，否则`false`。
该函数不进行任何类型转换，包括从整数或字符串转换。因此，只有当 `isByteArray()` 为真时才能调用;在任何其他条件下调用它都是错误。
注意：此功能不可恢复。也就是说，该功能不应用于仍可接收CBOR数据的情境，例如从套接字或管道接收。只有在完整数据已被接收且输入`QByteArray`或`QIODevice`中可用时，才应使用。

### `[since 6.7] bool QCborStreamReader::readAndAppendToString(QString &dst)`

**作用与语义：**

解码当前文本字符串并附加到`dst`。如果字符串被分块，该函数会遍历所有分块并连接它们。如果解码过程中出现错误，其他可能已成功解码的区块仍被写入`dst`。如果解码无错误，返回`true`，否则`false`。
该函数不进行任何类型转换，包括从整数或字节数组进行。因此，只有当`isString()`返回为真时才能调用;在其他条件下调用则为错误。
注意：此功能不可恢复。也就是说，该功能不应用于仍可能接收CBOR数据的情境，例如来自套接字或管道。只有在完整数据已接收且输入`QByteArray`或输入`QIODevice`可用时才应使用。

### `[since 6.7] bool QCborStreamReader::readAndAppendToUtf8String(QByteArray &dst)`

**作用与语义：**

解码当前文本字符串并附加到`dst`。如果字符串被分块，该函数会遍历所有分块并连接它们。如果解码过程中出现错误，其他可能已成功解码的区块仍被写入`dst`。如果解码无错误，返回`true`，否则`false`。
该函数不进行任何类型转换，包括从整数或字节数组进行。因此，只有当`isString()`返回为真时才能调用;在其他条件下调用则为错误。
注意：此功能不可恢复。也就是说，该功能不应用于仍可能接收CBOR数据的情境，例如来自套接字或管道。只有在完整数据已接收且输入`QByteArray`或输入`QIODevice`可用时才应使用。

### `QCborStreamReader::StringResult<QByteArray> QCborStreamReader::readByteArray()`

**作用与语义：**

从CBOR字符串中解码一个字节数组块并返回。该函数用于常规和分块内容，因此调用者必须始终绕着调用该函数，即使`isLengthKnown()`为真。该函数的典型用途如下：
`readAllByteArray()`函数实现了上述循环和一些额外的检查。
该函数不执行任何类型转换，包括整数或字符串的转换。因此，只有当 `isByteArray()` 为真时才能调用;在其他条件下调用则为错误。

**官方示例：**

```cpp
 QByteArray decodeBytearray(QCborStreamReader &reader)
 {
     QByteArray result;
     auto r = reader.readByteArray();
     while (r.status == QCborStreamReader::Ok) {
         result += r.data;
         r = reader.readByteArray();
     }

     if (r.status == QCborStreamReader::Error) {
         // handle error condition
         result.clear();
     }
     return result;
 }
```

### `QCborStreamReader::StringResult<QString> QCborStreamReader::readString()`

**作用与语义：**

从CBOR字符串中解码一个字符串块并返回。该函数可用于常规字符串和分块字符串内容，因此调用者必须始终绕着调用该函数，即使`isLengthKnown()`为真。该函数的典型用途如下：
`readAllString()`函数实现了上述循环和一些额外的检查。
该函数不进行任何类型转换，包括从整数或字节数组。因此，只有当`isString()`返回为真时才能调用;在其他条件下调用则为错误。

**官方示例：**

```cpp
 QString decodeString(QCborStreamReader &reader)
 {
     QString result;
     auto r = reader.readString();
     while (r.status == QCborStreamReader::Ok) {
         result += r.data;
         r = reader.readString();
     }

     if (r.status == QCborStreamReader::Error) {
         // handle error condition
         result.clear();
     }
     return result;
 }
```

### `QCborStreamReader::StringResult<qsizetype> QCborStreamReader::readStringChunk(char *ptr, qsizetype maxlen)`

**作用与语义：**

将当前字符串块读取到`ptr`指向的缓冲区，缓冲区大小为`maxlen`。该函数返回一个`StringResult`对象，复制到`ptr`的字节数保存在`\l` `StringResult::data`成员中。`\l` `StringResult::status`成员表示读取字符串时是否出现错误，数据是否被复制，或是否为最后一个块。
该函数可以同时调用`String`类型和`ByteArray`类型。对于后者，该函数读取的将与`readByteArray()`返回的数据相同。对于字符串，它返回的 UTF-8 等价于本应返回的`QString`。
该函数通常与`currentStringChunkSize()`一起在循环中使用。例如：
与`readByteArray()`和`readString()`不同，该功能不受`QByteArray`和 `QString`实现限制。
注意：该函数不验证 UTF-8 内容格式正确。这意味着即使 `readString()` 出现了，该函数也不会`QCborError::InvalidUtf8String`错误。

**官方示例：**

```cpp
 QCborStreamReader::StringResult<qsizetype> result;
 do {
     qsizetype size = reader.currentStringChunkSize();
     qsizetype oldsize = buffer.size();
     buffer.resize(oldsize + size);
     result = reader.readStringChunk(buffer.data() + oldsize, size);
 } while (result.status == QCborStreamReader::Ok);
```

### `[since 6.7] QCborStreamReader::StringResult<QByteArray> QCborStreamReader::readUtf8String()`

**作用与语义：**

从CBOR字符串中解码一个字符串块并返回。该函数可用于常规字符串和分块字符串内容，因此调用者必须始终绕着调用该函数，即使`isLengthKnown()`为真。该函数的典型用途类似于以下`readString()`：
`readAllUtf8String()`函数实现了上述循环和一些额外的检查。
该函数不进行任何类型转换，包括从整数或字节数组。因此，只有当`isString()`返回为真时才能调用;以其他条件调用则为错误。

**官方示例：**

```cpp
 QString decodeString(QCborStreamReader &reader)
 {
     QString result;
     auto r = reader.readString();
     while (r.status == QCborStreamReader::Ok) {
         result += r.data;
         r = reader.readString();
     }

     if (r.status == QCborStreamReader::Error) {
         // handle error condition
         result.clear();
     }
     return result;
 }
```

### `void QCborStreamReader::reparse()`

**作用与语义：**

对当前元素进行解析。当解析失败后，源 `QIODevice` 中出现更多数据，因为输入数据在 CBOR 流结束前到达，必须调用该函数。
当读取QByteArray()时，`addData()`函数会自动调用该函数。在读取未失败时调用该函数是no-op。

### `void QCborStreamReader::reset()`

**作用与语义：**

将源数据重置回起始并清除解码器状态。如果源数据是`QByteArray`，`QCborStreamReader`将从数组的起始处重新开始。
如果源数据是`QIODevice`，该函数会调用`QIODevice::reset()`，会寻找字节位置0。如果在设备开头（例如文件开头）找不到CBOR流，那么该函数很可能会做错。相反，将`QIODevice`定位到正确的偏移量并调用`setDevice()`。

### `void QCborStreamReader::setDevice(QIODevice *device)`

**作用与语义：**

将数据源设置为`device`，将解码器重置为初始状态。

### `bool QCborStreamReader::toBool() const`

**作用与语义：**

返回当前元素的布尔值。
该函数不执行任何类型转换，包括从整数的转换。因此，只有当 `isTrue()`、`isFalse()` 或 `isBool()` 返回为真时才能调用;以任何其他条件调用它都是错误。

### `double QCborStreamReader::toDouble() const`

**作用与语义：**

返回当前元素的64位双精度浮点值。
该函数不进行任何类型转换，包括从其他浮点类型或整数值转换。因此，只有当 `isDouble()` 为真时才能调用;在其他条件下调用则为错误。

### `qfloat16 QCborStreamReader::toFloat16() const`

**作用与语义：**

返回当前元素的16位半精度浮点值。
该函数不进行任何类型转换，包括从其他浮点类型或整数值转换。因此，只有当 `isFloat16()` 为真时才能调用;在其他条件下调用则为错误。

### `float QCborStreamReader::toFloat() const`

**作用与语义：**

返回当前元素的32位单精度浮点值。
该函数不进行任何类型转换，包括从其他浮点类型或整数值转换。因此，只有当 `isFloat()` 为真时才能调用;在其他条件下调用则为错误。

### `qint64 QCborStreamReader::toInteger() const`

**作用与语义：**

返回当前元素的整数值，无论是负数、正数还是零值。如果值大于263 - 1或小于-263，返回的值会溢出并符号错误。如果需要处理这些值，请使用`toUnsignedInteger()`或`toNegativeInteger()`。
该函数不执行任何类型转换，包括从布尔或CBOR标签转换。因此，只有当`isInteger()`为真时才可调用;在其他条件下调用则为错误。

### `QCborNegativeInteger QCborStreamReader::toNegativeInteger() const`

**作用与语义：**

返回当前元素的负整数值。QCborNegativeValue 是一个 64 位无符号整数，包含存储在 CBOR 流中的负数的绝对值。此外，QCborNegativeValue（0） 表示数字 -264。
该函数不执行任何类型转换，包括从布尔或CBOR标签转换。因此，只有当`isNegativeInteger()`为真时才能调用;在任何其他条件下调用是错误。
该函数可用于获取`toInteger()`返回类型范围之外的数字。然而，极不建议使用小于-263的负数。

### `QCborSimpleType QCborStreamReader::toSimpleType() const`

**作用与语义：**

返回当前简单类型的值。
该函数不进行任何类型转换，包括从整数的转换。因此，只有当 `isSimpleType()` 为真时才可调用;在其他条件下调用则为错误。

### `QCborTag QCborStreamReader::toTag() const`

**作用与语义：**

返回当前元素的标签值。
该函数不进行任何类型转换，包括从整数的转换。因此，只有当 `isTag()` 为真时才能调用;在其他条件下调用则为错误。
标签是附加在通用CBOR类型的64位数字，赋予它们更多意义。有关已知标签列表，请参见`QCborKnownTags`枚举。

### `quint64 QCborStreamReader::toUnsignedInteger() const`

**作用与语义：**

返回当前元素的无符号整数值。
该函数不执行任何类型转换，包括从布尔或CBOR标签转换。因此，只有当`isUnsignedInteger()`为真时才能调用;在其他条件下调用则为错误。
该函数可用于获取超出返回类型范围的数值`toInteger()`。

### `QCborStreamReader::Type QCborStreamReader::type() const`

**作用与语义：**

返回当前元素的类型。它是有效类型之一，或为无效。

### `struct StringResult`

**作用与语义：**

该类由`readString()`和`readByteArray()`返回，包含读取字符串的内容或解析已完成或发现错误的指示。
`data` 的内容只有在 `status` `Ok`时才有效。否则，它应为空。

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

`QCborStreamReader` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
