# QByteArray

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 紧凑的字节数组类型，负责二进制数据、协议数据和编码转换。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QByteArray`：紧凑的字节数组类型，负责二进制数据、协议数据和编码转换。

**内部模型：** 这类类型通常可以按值传递、复制和返回。许多 Qt 容器、字符串和图像采用隐式共享：复制时共享数据，发生写操作时才 detach。这样便于 API 传值，但获取原始指针或长期持有引用时必须考虑对象修改和生命周期。

**适用场景：** 先确认值的有效性和表示格式，再调用查询、转换或修改 API；处理文本时区分 Unicode 和字节编码，处理图像时确认 format，处理 URL/路径时使用 Qt 的解析 API 而不是手写字符串规则。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要把空值当成业务成功；不要保存临时对象的内部指针；不要把 QString 当二进制缓冲区；不要假定隐式共享让并发写入自动安全。

## 2. 依赖与对象关系

- 头文件：`#include <QByteArray>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

这类类型通常可以按值传递、复制和返回。许多 Qt 容器、字符串和图像采用隐式共享：复制时共享数据，发生写操作时才 detach。这样便于 API 传值，但获取原始指针或长期持有引用时必须考虑对象修改和生命周期。

### 状态、生命周期和线程

**生命周期：** 值对象由作用域、容器或调用者管理，不使用 parent 和 deleteLater。跨线程传递副本通常比传递 QObject 安全，但共享数据在写入时仍可能发生复制，性能和内存峰值要结合数据规模判断。

**状态与结果：** 重点区分空值、无效值、默认值和已初始化值。例如空字符串、空 URL、null 图像和无效索引不一定表示同一件事；转换函数的失败结果要通过对应的状态查询确认。

**线程与事件循环：** 值类型本身通常可以复制后跨线程传递；不要把 data()/bits()/constData() 得到的指针当成跨线程长期有效的所有权。大对象频繁写入会触发 detach，应避免不必要的复制和格式转换。

## 3. 直接使用

先确认值的有效性和表示格式，再调用查询、转换或修改 API；处理文本时区分 Unicode 和字节编码，处理图像时确认 format，处理 URL/路径时使用 Qt 的解析 API 而不是手写字符串规则。 使用时通常按这个过程组织：构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `class FromBase64Result`
- `enum Base64Option { Base64Encoding, Base64UrlEncoding, KeepTrailingEquals, OmitTrailingEquals, IgnoreBase64DecodingErrors, AbortOnBase64DecodingErrors }`
- `flags Base64Options`
- `const_iterator`
- `const_reverse_iterator`
- `iterator`
- `reverse_iterator`

### 公有函数

- `QByteArray()`
- `(since 6.8) QByteArray(QByteArrayView v)`
- `QByteArray(const char *data, qsizetype size = -1)`
- `QByteArray(qsizetype size, Qt::Initialization)`
- `QByteArray(qsizetype size, char ch)`
- `QByteArray(const QByteArray &other)`
- `QByteArray(QByteArray &&other)`
- `~QByteArray()`
- `QByteArray & append(const QByteArray &ba)`
- `QByteArray & append(QByteArrayView data)`
- `QByteArray & append(char ch)`
- `QByteArray & append(const char *str)`
- `QByteArray & append(const char *str, qsizetype len)`
- `QByteArray & append(qsizetype count, char ch)`
- `(since 6.6) QByteArray & assign(QByteArrayView v)`
- `(since 6.6) QByteArray & assign(InputIterator first, InputIterator last)`
- `(since 6.6) QByteArray & assign(qsizetype n, char c)`
- `char at(qsizetype i) const`
- `char & back()`
- `char back() const`
- `QByteArray::iterator begin()`
- `QByteArray::const_iterator begin() const`
- `qsizetype capacity() const`
- `QByteArray::const_iterator cbegin() const`
- `QByteArray::const_iterator cend() const`
- `void chop(qsizetype n)`
- `QByteArray chopped(qsizetype len) &&`
- `QByteArray chopped(qsizetype len) const &`
- `void clear()`
- `(since 6.0) int compare(QByteArrayView bv, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `QByteArray::const_iterator constBegin() const`
- `const char * constData() const`
- `QByteArray::const_iterator constEnd() const`
- `(since 6.0) bool contains(QByteArrayView bv) const`
- `bool contains(char ch) const`
- `(since 6.0) qsizetype count(QByteArrayView bv) const`
- `qsizetype count(char ch) const`
- `QByteArray::const_reverse_iterator crbegin() const`
- `QByteArray::const_reverse_iterator crend() const`
- `char * data()`
- `const char * data() const`
- `QByteArray::iterator end()`
- `QByteArray::const_iterator end() const`
- `(since 6.0) bool endsWith(QByteArrayView bv) const`
- `bool endsWith(char ch) const`
- `(since 6.1) QByteArray::iterator erase(QByteArray::const_iterator first, QByteArray::const_iterator last)`
- `(since 6.5) QByteArray::iterator erase(QByteArray::const_iterator it)`
- `QByteArray & fill(char ch, qsizetype size = -1)`
- `(since 6.0) QByteArray first(qsizetype n) &&`
- `(since 6.0) QByteArray first(qsizetype n) const &`
- `char & front()`
- `char front() const`
- `(since 6.0) qsizetype indexOf(QByteArrayView bv, qsizetype from = 0) const`
- `qsizetype indexOf(char ch, qsizetype from = 0) const`
- `(since 6.0) QByteArray & insert(qsizetype i, QByteArrayView data)`
- `QByteArray & insert(qsizetype i, const QByteArray &data)`
- `QByteArray & insert(qsizetype i, const char *s)`
- `QByteArray & insert(qsizetype i, char ch)`
- `QByteArray & insert(qsizetype i, const char *data, qsizetype len)`
- `QByteArray & insert(qsizetype i, qsizetype count, char ch)`
- `bool isEmpty() const`
- `bool isLower() const`
- `bool isNull() const`
- `bool isUpper() const`
- `(since 6.3) bool isValidUtf8() const`
- `(since 6.0) QByteArray last(qsizetype n) &&`
- `(since 6.0) QByteArray last(qsizetype n) const &`
- `(since 6.0) qsizetype lastIndexOf(QByteArrayView bv, qsizetype from) const`
- `(since 6.2) qsizetype lastIndexOf(QByteArrayView bv) const`
- `qsizetype lastIndexOf(char ch, qsizetype from = -1) const`
- `QByteArray left(qsizetype len) &&`
- `QByteArray left(qsizetype len) const &`
- `QByteArray leftJustified(qsizetype width, char fill = ' ', bool truncate = false) const`
- `qsizetype length() const`
- `(since 6.8) qsizetype max_size() const`
- `QByteArray mid(qsizetype pos, qsizetype len = -1) &&`
- `QByteArray mid(qsizetype pos, qsizetype len = -1) const &`
- `(since 6.10) QByteArray & nullTerminate()`
- `(since 6.10) QByteArray nullTerminated() &&`
- `(since 6.10) QByteArray nullTerminated() const &`
- `(since 6.4) QByteArray percentDecoded(char percent = '%') const &`
- `(since 6.11) QByteArray percentDecoded(char percent = '%') &&`
- `QByteArray & prepend(QByteArrayView ba)`
- `QByteArray & prepend(char ch)`
- `QByteArray & prepend(const QByteArray &ba)`
- `QByteArray & prepend(const char *str)`
- `QByteArray & prepend(const char *str, qsizetype len)`
- `QByteArray & prepend(qsizetype count, char ch)`
- `void push_back(const QByteArray &other)`
- `(since 6.0) void push_back(QByteArrayView str)`
- `void push_back(char ch)`
- `void push_back(const char *str)`
- `void push_front(const QByteArray &other)`
- `(since 6.0) void push_front(QByteArrayView str)`
- `void push_front(char ch)`
- `void push_front(const char *str)`
- `QByteArray::reverse_iterator rbegin()`
- `QByteArray::const_reverse_iterator rbegin() const`
- `QByteArray & remove(qsizetype pos, qsizetype len)`
- `(since 6.5) QByteArray & removeAt(qsizetype pos)`
- `(since 6.5) QByteArray & removeFirst()`
- `(since 6.1) QByteArray & removeIf(Predicate pred)`
- `(since 6.5) QByteArray & removeLast()`
- `QByteArray::reverse_iterator rend()`
- `QByteArray::const_reverse_iterator rend() const`
- `QByteArray repeated(qsizetype times) const`
- `QByteArray & replace(qsizetype pos, qsizetype len, QByteArrayView after)`
- `(since 6.0) QByteArray & replace(QByteArrayView before, QByteArrayView after)`
- `QByteArray & replace(char before, QByteArrayView after)`
- `QByteArray & replace(char before, char after)`
- `QByteArray & replace(const char *before, qsizetype bsize, const char *after, qsizetype asize)`
- `QByteArray & replace(qsizetype pos, qsizetype len, const char *after, qsizetype alen)`
- `void reserve(qsizetype size)`
- `void resize(qsizetype size)`
- `(since 6.4) void resize(qsizetype newSize, char c)`
- `(since 6.8) void resizeForOverwrite(qsizetype size)`
- `QByteArray right(qsizetype len) &&`
- `QByteArray right(qsizetype len) const &`
- `QByteArray rightJustified(qsizetype width, char fill = ' ', bool truncate = false) const`
- `QByteArray & setNum(int n, int base = 10)`
- `QByteArray & setNum(long n, int base = 10)`
- `QByteArray & setNum(qlonglong n, int base = 10)`
- `QByteArray & setNum(qulonglong n, int base = 10)`
- `QByteArray & setNum(short n, int base = 10)`
- `QByteArray & setNum(uint n, int base = 10)`
- `QByteArray & setNum(ulong n, int base = 10)`
- `QByteArray & setNum(ushort n, int base = 10)`
- `QByteArray & setNum(double n, char format = 'g', int precision = 6)`
- `QByteArray & setNum(float n, char format = 'g', int precision = 6)`
- `QByteArray & setRawData(const char *data, qsizetype size)`
- `void shrink_to_fit()`
- `QByteArray simplified() const`
- `qsizetype size() const`
- `(since 6.8) QByteArray & slice(qsizetype pos, qsizetype n)`
- `(since 6.8) QByteArray & slice(qsizetype pos)`
- `(since 6.0) QByteArray sliced(qsizetype pos, qsizetype n) &&`
- `(since 6.0) QByteArray sliced(qsizetype pos, qsizetype n) const &`
- `(since 6.0) QByteArray sliced(qsizetype pos) &&`
- `(since 6.0) QByteArray sliced(qsizetype pos) const &`
- `QList<QByteArray> split(char sep) const`
- `void squeeze()`
- `(since 6.0) bool startsWith(QByteArrayView bv) const`
- `bool startsWith(char ch) const`
- `void swap(QByteArray &other)`
- `QByteArray toBase64(QByteArray::Base64Options options = Base64Encoding) const`
- `CFDataRef toCFData() const`
- `double toDouble(bool *ok = nullptr) const`
- `(since 6.5) emscripten::val toEcmaUint8Array()`
- `float toFloat(bool *ok = nullptr) const`
- `QByteArray toHex(char separator = '\0') const`
- `int toInt(bool *ok = nullptr, int base = 10) const`
- `long toLong(bool *ok = nullptr, int base = 10) const`
- `qlonglong toLongLong(bool *ok = nullptr, int base = 10) const`
- `QByteArray toLower() const`
- `NSData * toNSData() const`
- `QByteArray toPercentEncoding(const QByteArray &exclude = QByteArray(), const QByteArray &include = QByteArray(), char percent = '%') const`
- `CFDataRef toRawCFData() const`
- `NSData * toRawNSData() const`
- `short toShort(bool *ok = nullptr, int base = 10) const`
- `std::string toStdString() const`
- `uint toUInt(bool *ok = nullptr, int base = 10) const`
- `ulong toULong(bool *ok = nullptr, int base = 10) const`
- `qulonglong toULongLong(bool *ok = nullptr, int base = 10) const`
- `ushort toUShort(bool *ok = nullptr, int base = 10) const`
- `QByteArray toUpper() const`
- `QByteArray trimmed() const`
- `void truncate(qsizetype pos)`
- `operator const char *() const`
- `operator const void *() const`
- `(since 6.10) operator std::string_view() const`
- `QByteArray & operator+=(const QByteArray &ba)`
- `QByteArray & operator+=(char ch)`
- `QByteArray & operator+=(const char *str)`
- `QByteArray & operator=(QByteArray &&other)`
- `QByteArray & operator=(const QByteArray &other)`
- `QByteArray & operator=(const char *str)`
- `char & operator[](qsizetype i)`
- `char operator[](qsizetype i) const`

### 静态公有成员

- `QByteArray fromBase64(const QByteArray &base64, QByteArray::Base64Options options = Base64Encoding)`
- `QByteArray::FromBase64Result fromBase64Encoding(QByteArray &&base64, QByteArray::Base64Options options = Base64Encoding)`
- `QByteArray::FromBase64Result fromBase64Encoding(const QByteArray &base64, QByteArray::Base64Options options = Base64Encoding)`
- `QByteArray fromCFData(CFDataRef data)`
- `(since 6.5) QByteArray fromEcmaUint8Array(emscripten::val uint8array)`
- `QByteArray fromHex(const QByteArray &hexEncoded)`
- `QByteArray fromNSData(const NSData *data)`
- `QByteArray fromPercentEncoding(const QByteArray &input, char percent = '%')`
- `(since 6.11) QByteArray fromPercentEncoding(QByteArray &&input, char percent = '%')`
- `QByteArray fromRawCFData(CFDataRef data)`
- `QByteArray fromRawData(const char *data, qsizetype size)`
- `QByteArray fromRawNSData(const NSData *data)`
- `QByteArray fromStdString(const std::string &str)`
- `(since 6.8) qsizetype maxSize()`
- `QByteArray number(int n, int base = 10)`
- `QByteArray number(long n, int base = 10)`
- `QByteArray number(qlonglong n, int base = 10)`
- `QByteArray number(qulonglong n, int base = 10)`
- `QByteArray number(uint n, int base = 10)`
- `QByteArray number(ulong n, int base = 10)`
- `QByteArray number(double n, char format = 'g', int precision = 6)`

### 相关非成员函数

- `(since 6.1) qsizetype erase(QByteArray &ba, const T &t)`
- `(since 6.1) qsizetype erase_if(QByteArray &ba, Predicate pred)`
- `quint16 qChecksum(QByteArrayView data, Qt::ChecksumType standard = Qt::ChecksumIso3309)`
- `QByteArray qCompress(const QByteArray &data, int compressionLevel = -1)`
- `QByteArray qCompress(const uchar *data, qsizetype nbytes, int compressionLevel = -1)`
- `QByteArray qUncompress(const QByteArray &data)`
- `QByteArray qUncompress(const uchar *data, qsizetype nbytes)`
- `int qstrcmp(const char *str1, const char *str2)`
- `char * qstrcpy(char *dst, const char *src)`
- `char * qstrdup(const char *src)`
- `int qstricmp(const char *str1, const char *str2)`
- `size_t qstrlen(const char *str)`
- `int qstrncmp(const char *str1, const char *str2, size_t len)`
- `char * qstrncpy(char *dst, const char *src, size_t len)`
- `int qstrnicmp(const char *str1, const char *str2, size_t len)`
- `size_t qstrnlen(const char *str, size_t maxlen)`
- `bool operator!=(const QByteArray &lhs, const QByteArray &rhs)`
- `bool operator!=(const QByteArray &lhs, const char *const &rhs)`
- `bool operator!=(const char *const &lhs, const QByteArray &rhs)`
- `(since 6.4) QByteArray operator""_ba(const char *str, size_t size)`
- `(since 6.9) QByteArray operator+(QByteArrayView lhs, const QByteArray &rhs)`
- `QByteArray operator+(char a1, const QByteArray &a2)`
- `(since 6.9) QByteArray operator+(const QByteArray &lhs, QByteArrayView rhs)`
- `QByteArray operator+(const QByteArray &a1, char a2)`
- `QByteArray operator+(const QByteArray &a1, const QByteArray &a2)`
- `QByteArray operator+(const QByteArray &a1, const char *a2)`
- `QByteArray operator+(const char *a1, const QByteArray &a2)`
- `bool operator<(const QByteArray &lhs, const QByteArray &rhs)`
- `bool operator<(const QByteArray &lhs, const char *const &rhs)`
- `bool operator<(const char *const &lhs, const QByteArray &rhs)`
- `QDataStream & operator<<(QDataStream &out, const QByteArray &ba)`
- `bool operator<=(const QByteArray &lhs, const QByteArray &rhs)`
- `bool operator<=(const QByteArray &lhs, const char *const &rhs)`
- `bool operator<=(const char *const &lhs, const QByteArray &rhs)`
- `bool operator==(const QByteArray &lhs, const QByteArray &rhs)`
- `bool operator==(const QByteArray &lhs, const char *const &rhs)`
- `bool operator==(const char *const &lhs, const QByteArray &rhs)`
- `bool operator>(const QByteArray &lhs, const QByteArray &rhs)`
- `bool operator>(const QByteArray &lhs, const char *const &rhs)`
- `bool operator>(const char *const &lhs, const QByteArray &rhs)`
- `bool operator>=(const QByteArray &lhs, const QByteArray &rhs)`
- `bool operator>=(const QByteArray &lhs, const char *const &rhs)`
- `bool operator>=(const char *const &lhs, const QByteArray &rhs)`
- `QDataStream & operator>>(QDataStream &in, QByteArray &ba)`

### 公开宏

- `QByteArrayLiteral(ba)`
- `QT_NO_CAST_FROM_BYTEARRAY`
- `(since 6.8) QT_NO_QSNPRINTF`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QByteArray::Base64Optionflags QByteArray::Base64Options`

**作用与语义：**

该枚举包含可用于编码和解码Base64的选项。Base64由RFC 4648定义，具有以下选项：
- `QByteArray::Base64Encoding`：`0`;（默认）常规的Base64字母表，简称为“base64”
- `QByteArray::Base64UrlEncoding`：`1`;一种替代字母表，称为“base64url”，它替换字母表中的两个字符，以更友好于网址。
- `QByteArray::KeepTrailingEquals`：`0`;（默认）保持编码数据末尾的填充等号，使数据始终是四的倍数。
- `QByteArray::OmitTrailingEquals`：`2`;省略在编码数据末尾添加填充等号。
- `QByteArray::IgnoreBase64DecodingErrors`：`0`;解码Base64编码数据时，忽略输入中的错误;无效字符被简单跳过。该枚举值在Qt 5.15中加入。
- `QByteArray::AbortOnBase64DecodingErrors`：`4`;解码Base64编码数据时，停止于第一次译码误差。该枚举值在Qt 5.15中加入。
`QByteArray::fromBase64Encoding()` 和 `QByteArray::fromBase64()` 忽略 KeepTrailingEquals 和 OmitTrailingEquals 选项。如果指定了 IgnoreBase64DecodingErrors 选项，它们不会在缺少等号尾部或数量过多时标记错误。如果指定了 AbortOnBase64DecodingErrors，那么输入必须没有填充或等号数量正确。
Base64Options 类型是 QFlag 的 typedef<Base64Option>。它存储 Base64Option 值的 OR 组合。

### `QByteArray::const_iterator`

**作用与语义：**

该typedef为`QByteArray`提供了一个STL风格的const迭代器。

### `QByteArray::const_reverse_iterator`

**作用与语义：**

该typedef为`QByteArray`提供了一个STL风格的const反迭代器。

### `QByteArray::iterator`

**作用与语义：**

该typedef为`QByteArray`提供了一个STL风格的非const迭代器。

### `QByteArray::reverse_iterator`

**作用与语义：**

该typedef为`QByteArray`提供了一个STL风格的非const反迭代器。

### `[constexpr noexcept] QByteArray::QByteArray()`

**作用与语义：**

构造一个空字节数组。

### `[explicit, since 6.8] QByteArray::QByteArray(QByteArrayView v)`

**作用与语义：**

构造一个以字节数组视图数据初始化的字节数组。
QByteArray 是空的当且仅当 `v` 是空的。

### `QByteArray::QByteArray(const char *data, qsizetype size = -1)`

**作用与语义：**

构建包含数组`data`前`size`字节的字节数组。
如果`data`为0，则构造一个空字节数组。
如果`size`为负，则假设`data`指向一个“\0”终止的字符串，其长度通过动态确定。
QByteArray 会对字符串数据进行深度复制。

### `QByteArray::QByteArray(qsizetype size, Qt::Initialization)`

**作用与语义：**

构造一个大小为`size`的字节数组，内容未初始化。

**官方示例：**

```cpp
 QByteArray buffer(123, Qt::Uninitialized);
```

### `QByteArray::QByteArray(qsizetype size, char ch)`

**作用与语义：**

构造大小为 `size` 的字节数组，每个字节设置为 `ch`。

### `[noexcept] QByteArray::QByteArray(const QByteArray &other)`

**作用与语义：**

构建了`other`的复制品。
该操作耗时为常数，因为QByteArray是隐式共享的。这使得从函数返回QByteArray非常快捷。如果共享实例被修改，它将被复制（写时复制），耗时为线性时间。

### `[noexcept] QByteArray::QByteArray(QByteArray &&other)`

**作用与语义：**

Move构造一个QByteArray实例，使其指向`other`指向的同一个对象。

### `[noexcept] QByteArray::~QByteArray()`

**作用与语义：**

会破坏字节数组。

### `QByteArray &QByteArray::append(const QByteArray &ba)`

**作用与语义：**

将字节数组`ba`附加到该字节数组末尾。
这和插入（`size()`、`ba`）是一样的。
注意：`QByteArray` 是一个隐式共享类。因此，如果你附加到空字节数组，字节数组只会共享`ba`中存储的数据。在这种情况下，不进行数据复制，耗时为常数。如果共享实例被修改，则会被复制（写时复制），耗时线性时间。
如果被附加的字节数组不是空的，则会对数据进行深度复制，时间为线性。
append() 函数通常非常快（常数时间），因为 `QByteArray` 在数据末尾预分配额外空间，因此数据可以增长而无需每次重新分配整个数组。

**官方示例：**

```cpp
 QByteArray x("free");
 QByteArray y("dom");
 x.append(y);
 // x == "freedom"
```

### `QByteArray &QByteArray::append(QByteArrayView data)`

**作用与语义：**

将`data`附加到该字节数组上。

### `QByteArray &QByteArray::append(char ch)`

**作用与语义：**

将字节`ch`附加到该字节数组中。

### `QByteArray &QByteArray::append(const char *str)`

**作用与语义：**

将“\0”终止字符串 `str` 附加到该字节数组中。

### `QByteArray &QByteArray::append(const char *str, qsizetype len)`

**作用与语义：**

将从`str`开始的前`len`字节附加到该字节数组，并返回对该字节数组的引用。附加的字节可能包含“\0”字节。
如果`len`为负，`str`将被假定为一个“\0”终止字符串，复制长度将自动通过`qstrlen()`确定。
如果`len`为零或`str`为空，则字节数组中不添加任何内容。确保`len`不超过`str`。

### `QByteArray &QByteArray::append(qsizetype count, char ch)`

**作用与语义：**

将`count`个字节`ch`的副本附加到该字节数组，并返回对该字节数组的引用。
如果`count`为负或为零，字节数组中不会附加任何内容。

### `[since 6.6] QByteArray &QByteArray::assign(QByteArrayView v)`

**作用与语义：**

用`v`的副本替换该字节数组的内容，并返回对该字节数组的引用。
该字节数组的大小将等于 的 个 `v`。
该函数仅在`v`大小超过该字节数组容量或该字节数组被共享时分配内存。

### `[since 6.6] template <typename InputIterator, QByteArray::if_input_iterator<InputIterator> = true> QByteArray &QByteArray::assign(InputIterator first, InputIterator last)`

**作用与语义：**

用迭代符域 [`first`， `last`） 中的元素副本替换该字节数组的内容，并返回对该字节数组的引用。
该字节数组的大小将等于该区间 [`first`， `last`] 中的元素数。
该函数只有在该区间的元素数超过该字节数组的容量或该字节数组被共享时才会分配内存。
注意：如果任一参数是*这个或[`first`， `last`）的迭代器，则该行为未定义。
只有当`InputIterator`满足LegacyInputIterator的要求时，才参与重载决议。

### `[since 6.6] QByteArray &QByteArray::assign(qsizetype n, char c)`

**作用与语义：**

用`n`份`c`副本替换该字节数组的内容，并返回对该字节数组的引用。
该字节数组的大小将等于 `n`，且必须为非负数。
该函数只有在内存超过该字节数组容量或该字节数组被共享时才会分配内存`n`。

### `char QByteArray::at(qsizetype i) const`

**作用与语义：**

返回字节数组中索引位置`i`的字节。
`i`必须是字节数组中的有效索引位置（即0 <= `i` < `size()`）。

### `char &QByteArray::back()`

**作用与语义：**

返回字节数组最后一个字节的引用。和`operator[](size() - 1)`一样。
此功能是为了STL兼容性而提供。
警告：在空字节数组上调用该函数属于未定义行为。

### `char QByteArray::back() const`

**作用与语义：**

返回字节数组的最后一个字节。和 `at(size() - 1)` 一样。
此功能是为了STL兼容性而提供。
警告：在空字节数组上调用该函数属于未定义行为。

### `QByteArray::iterator QByteArray::begin()`

**作用与语义：**

返回一个指向字节数组第一个字节的STL式迭代器。
警告：返回迭代器在分离或`QByteArray`修改时失效。

### `[noexcept] QByteArray::const_iterator QByteArray::begin() const`

**作用与语义：**

注意：该功能会让`QByteArray::begin()`重载。

### `qsizetype QByteArray::capacity() const`

**作用与语义：**

返回在不强制重分配的情况下，字节数组中可存储的最大字节数。
该函数的唯一目的是提供一种微调`QByteArray`内存使用的方法。一般来说，你很少需要调用这个函数。如果你想知道字节数组中有多少字节，可以调用`size()`。
注意：静态分配的字节数组即使不是空的，也会报告容量为0。
注意：分配内存块中的空闲空间位置未定义。换句话说，不应假设空闲内存总是位于初始化元素之后。

### `[noexcept] QByteArray::const_iterator QByteArray::cbegin() const`

**作用与语义：**

返回一个const型STL风格的迭代子，指向字节数组中的第一个字节。
警告：返回的迭代器在分离或`QByteArray`修改时将失效。

### `[noexcept] QByteArray::const_iterator QByteArray::cend() const`

**作用与语义：**

返回一个const STL风格的迭代器，指向字节数组最后一个字节之后。
警告：返回的迭代器在分离或`QByteArray`修改时将失效。

### `void QByteArray::chop(qsizetype n)`

**作用与语义：**

从字节数组末端移除`n`字节。
如果`n`大于`size()`，结果是一个空字节数组。

**官方示例：**

```cpp
 QByteArray ba("STARTTLS\r\n");
 ba.chop(2);                 // ba == "STARTTLS"
```

### `QByteArray QByteArray::chopped(qsizetype len) &&`

**作用与语义：**

返回一个字节数组，包含该字节数组最左侧`size()` - `len`字节。
注意：行为未定义`len`是否为负或大于`size()`。

### `void QByteArray::clear()`

**作用与语义：**

清除字节数组的内容，使其为 null。

### `[noexcept, since 6.0] int QByteArray::compare(QByteArrayView bv, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

返回一个整数，大小于、等于或大于零，具体取决于该`QByteArray`在`QByteArrayView` `bv`之前、相同位置还是之后排序。比较根据大小写区分`cs`进行。

### `[noexcept] QByteArray::const_iterator QByteArray::constBegin() const`

**作用与语义：**

返回一个const型STL风格的迭代子，指向字节数组中的第一个字节。
警告：返回的迭代器在分离或`QByteArray`修改时将失效。

### `[noexcept] const char *QByteArray::constData() const`

**作用与语义：**

返回存储在字节数组中的const数据的指针。该指针可用于访问组成数组的字节。除非`QByteArray`对象是从原始数据创建的，否则数据为“\0”终止。
只要不发生分离且`QByteArray`未被修改，指针依然有效。
该函数主要用于将字节数组传递给接受`const char *`的函数。
注意：`QByteArray`可以存储包括“\0”在内的任何字节值，但大多数`char *`参数函数假设数据在遇到的第一个“\0”处结束。

### `[noexcept] QByteArray::const_iterator QByteArray::constEnd() const`

**作用与语义：**

返回一个const STL风格的迭代器，指向字节数组最后一个字节之后。
警告：返回的迭代器在分离或`QByteArray`修改时将失效。

### `[since 6.0] bool QByteArray::contains(QByteArrayView bv) const`

**作用与语义：**

如果该字节数组包含`bv`查看的字节序列的出现，返回`true`;否则返回`false`。

### `bool QByteArray::contains(char ch) const`

**作用与语义：**

如果字节数组包含字节`ch`，返回`true`;否则返回`false`。

### `[since 6.0] qsizetype QByteArray::count(QByteArrayView bv) const`

**作用与语义：**

返回`bv`在该字节数组中看到的字节序列出现的次数（可能重叠）。

### `qsizetype QByteArray::count(char ch) const`

**作用与语义：**

返回字节数组中字节`ch`的出现次数。

### `[noexcept] QByteArray::const_reverse_iterator QByteArray::crbegin() const`

**作用与语义：**

返回一个const STL风格的反迭代器，指向字节数组中的第一个字节，顺序相反。
警告：返回的迭代器在脱离或`QByteArray`修改时将失效。

### `[noexcept] QByteArray::const_reverse_iterator QByteArray::crend() const`

**作用与语义：**

返回一个const STL风格的反向迭代器，指向字节数组最后一个字节之后，顺序相反。
警告：返回的迭代器在分离或`QByteArray`修改时将失效。

### `char *QByteArray::data()`

**作用与语义：**

返回存储在字节数组中的数据指针。该指针可用于访问和修改组成数组的字节。数据是“\0”终止的，即返回指针后可访问的字节数`size()`为1，包括“\0”终止符。
只要不发生分离且`QByteArray`未被修改，指针依然有效。
对于只读访问，由于不会导致深度复制，`constData()`更快。
该函数主要用于将字节数组传递给接受`const char *`的函数。
以下示例复制了data()返回的char*，但会损坏堆并导致崩溃，因为它没有为结尾的“\0”分配字节：
这个方案分配了正确的空间：
注意：`QByteArray`可以存储包括“\0”在内的任何字节值，但大多数`char *`参数的函数假设数据在遇到的第一个“\0”处结束。

**官方示例：**

```cpp
 QByteArray ba("Hello world");
 char *data = ba.data();
 while (*data) {
     cout << "[" << *data << "]" << endl;
     ++data;
 }
```

### `[noexcept] const char *QByteArray::data() const`

**作用与语义：**

返回存储在字节数组中的数据指针。该指针可用于访问和修改组成数组的字节。数据是“\0”终止的，即返回指针后可访问的字节数`size()`为1，包括“\0”终止符。
只要不发生分离且`QByteArray`未被修改，指针依然有效。
对于只读访问，由于不会导致深度复制，`constData()`更快。
该函数主要用于将字节数组传递给接受`const char *`的函数。
以下示例复制了data()返回的char*，但会损坏堆并导致崩溃，因为它没有为结尾的“\0”分配字节：
这个方案分配了正确的空间：
注意：`QByteArray`可以存储包括“\0”在内的任何字节值，但大多数`char *`参数的函数假设数据在遇到的第一个“\0”处结束。

**官方示例：**

```cpp
 QByteArray ba("Hello world");
 char *data = ba.data();
 while (*data) {
     cout << "[" << *data << "]" << endl;
     ++data;
 }
```

### `QByteArray::iterator QByteArray::end()`

**作用与语义：**

返回一个STL风格的迭代器，指向字节数组最后一个字节之后。
警告：返回的迭代器在脱离或`QByteArray`修改时会失效。

### `[noexcept] QByteArray::const_iterator QByteArray::end() const`

**作用与语义：**

注意：该功能会让`QByteArray::end()`重载。

### `[since 6.0] bool QByteArray::endsWith(QByteArrayView bv) const`

**作用与语义：**

如果该字节数组以`bv`所见的字节序列结束，返回`true`;否则返回`false`。

**官方示例：**

```cpp
 QByteArray url("http://qt-project.org/doc/qt-5.0/qtdoc/index.html");
 if (url.endsWith(".html"))
     {/*...*/}
```

### `bool QByteArray::endsWith(char ch) const`

**作用与语义：**

如果该字节数组以字节`ch`结尾，返回`true`;否则返回`false`。

### `[since 6.1] QByteArray::iterator QByteArray::erase(QByteArray::const_iterator first, QByteArray::const_iterator last)`

**作用与语义：**

从字节数组中移除半开范围的字符 [ `first` ， `last` ）。返回一个迭代器，返回到擦除前 `last` 所引用的字符。

### `[since 6.5] QByteArray::iterator QByteArray::erase(QByteArray::const_iterator it)`

**作用与语义：**

从字节数组中移除以 `it` 表示的字符。在被擦除字符后立即返回迭代器。

**官方示例：**

```cpp
 QByteArray ba = "abcdefg";
 auto it = ba.erase(ba.cbegin()); // ba is now "bcdefg" and it points to "b"
```

### `QByteArray &QByteArray::fill(char ch, qsizetype size = -1)`

**作用与语义：**

将字节数组中的每个字节设置为 `ch`。如果 `size` 与默认值 -1 不同，字节数组会提前调整为 `size` 大小。

**官方示例：**

```cpp
 QByteArray ba("Istambul");
 ba.fill('o');
 // ba == "oooooooo"

 ba.fill('X', 2);
 // ba == "XX"
```

### `[since 6.0] QByteArray QByteArray::first(qsizetype n) &&`

**作用与语义：**

返回字节数组的前`n`字节。
注意：当`n` <0或`n` > `size()`时，行为未定义。

**官方示例：**

```cpp
 QByteArray x("Pineapple");
 QByteArray y = x.first(4);
 // y == "Pine"
```

### `[static] QByteArray QByteArray::fromBase64(const QByteArray &base64, QByteArray::Base64Options options = Base64Encoding)`

**作用与语义：**

返回 Base64 数组的解码副本，`base64` 使用 `options` 定义的选项。如果 `options` 包含 `IgnoreBase64DecodingErrors`（默认），则不检查输入有效性;输入中的无效字符会被跳过，使解码过程能够继续后续字符。如果 包含 `options` `AbortOnBase64DecodingErrors`，则解码将在第一个无效字符处停止。
用于解码 Base64 编码数据的算法在 RFC 4648 中定义。
返回解码数据，或者如果`AbortOnBase64DecodingErrors`选项被传递且输入数据无效，则返回一个空字节数组。
注意：新代码中推荐使用`fromBase64Encoding()`函数。

**官方示例：**

```cpp
 QByteArray text = QByteArray::fromBase64("UXQgaXMgZ3JlYXQh");
 text.data();            // returns "Qt is great!"

 QByteArray::fromBase64("PHA+SGVsbG8/PC9wPg==", QByteArray::Base64Encoding); // returns "<p>Hello?</p>"
 QByteArray::fromBase64("PHA-SGVsbG8_PC9wPg==", QByteArray::Base64UrlEncoding); // returns "<p>Hello?</p>"
```

### `[static] QByteArray::FromBase64Result QByteArray::fromBase64Encoding(const QByteArray &base64, QByteArray::Base64Options options = Base64Encoding)`

**作用与语义：**

解码 Base64 数组`base64`，使用`options`定义的选项。如果`options`包含 `IgnoreBase64DecodingErrors`（默认），则不检查输入有效性;输入中的无效字符会被跳过，使解码过程能够继续后续字符。如果 包含 `options` `AbortOnBase64DecodingErrors`，则解码将在第一个无效字符处停止。
用于解码 Base64 编码数据的算法在 RFC 4648 中定义。
返回一个 QByteArrayFromBase64Result 对象，包含解码数据和一个标志，说明解码是否成功。如果`AbortOnBase64DecodingErrors`选项被传递且输入数据无效，则未说明解码数据包含什么。

**官方示例：**

```cpp
 void process(const QByteArray &);

 if (auto result = QByteArray::fromBase64Encoding(encodedData))
     process(*result);
```

### `[static] QByteArray QByteArray::fromCFData(CFDataRef data)`

**作用与语义：**

构建包含CFData `data`副本的新`QByteArray`。

### `[static, since 6.5] QByteArray QByteArray::fromEcmaUint8Array(emscripten::val uint8array)`

**作用与语义：**

构建一个包含Uint8Array副本的新`QByteArray` `uint8array`。
该函数将数据从JavaScript数据缓冲区（C代码无法寻址）传输到`QByteArray`拥有的堆内存。该函数返回并复制后，Uint8Array即可释放。
`uint8array`参数必须有一个 emscripten：：val，引用 Uint8Array 对象，例如从全局 JavaScript 变量获得：
如果Uint8Array的大小超过最大容量`QByteArray`，或者`uint8array`参数不是Uint8Array类型，该函数会返回空`QByteArray`。

**官方示例：**

```cpp
 emscripten::val uint8array = emscripten::val::global("g_uint8array");
 QByteArray byteArray = QByteArray::fromEcmaUint8Array(uint8array);
```

### `[static] QByteArray QByteArray::fromHex(const QByteArray &hexEncoded)`

**作用与语义：**

返回十六进制编码数组的解码副本`hexEncoded`。输入不检查有效性;输入中的无效字符被跳过，使解码过程能够继续后续字符。

**官方示例：**

```cpp
 QByteArray text = QByteArray::fromHex("517420697320677265617421");
 text.data();            // returns "Qt is great!"
```

### `[static] QByteArray QByteArray::fromNSData(const NSData *data)`

**作用与语义：**

构建了一个包含《国家大`data`》副本的新`QByteArray`。

### `[static] QByteArray QByteArray::fromPercentEncoding(const QByteArray &input, char percent = '%')`

**作用与语义：**

通过URI/URL风格的百分比编码解码`input`。
返回包含解码文本的字节数组。`percent`参数允许使用与“%”不同的字符（例如“_”或“='）作为转义字符。等价于输入。`percentDecoded`（百分比）。

**官方示例：**

```cpp
 QByteArray text = QByteArray::fromPercentEncoding("Qt%20is%20great%33");
 qDebug("%s", text.data());      // reports "Qt is great!"
```

### `[static, since 6.11] QByteArray QByteArray::fromPercentEncoding(QByteArray &&input, char percent = '%')`

**作用与语义：**

通过URI/URL风格的百分比编码解码`input`。
返回包含解码文本的字节数组。`percent`参数允许使用与“%”不同的字符（例如“_”或“='）作为转义字符。等价于输入。`percentDecoded`（百分比）。

**官方示例：**

```cpp
 QByteArray text = QByteArray::fromPercentEncoding("Qt%20is%20great%33");
 qDebug("%s", text.data());      // reports "Qt is great!"
```

### `[static] QByteArray QByteArray::fromRawCFData(CFDataRef data)`

**作用与语义：**

构建一个使用 CFData `data`字节的 `QByteArray`。
`data`的字节不会被复制。
调用者保证只要该`QByteArray`对象存在，CFData 就不会被删除或修改。

### `[static] QByteArray QByteArray::fromRawData(const char *data, qsizetype size)`

**作用与语义：**

构造一个`QByteArray`，使用`data`数组的前`size`字节。这些字节不会被复制。`QByteArray`将包含`data`指针。调用者保证只要该`QByteArray`及其未被修改的副本存在，`data`不会被删除或修改。换句话说，由于`QByteArray`是一个隐式共享类，且该函数返回的实例包含`data`指针，调用者无需删除或直接修改`data`，只要返回的`QByteArray`和任何副本存在。然而，`QByteArray`不拥有`data`的所有权，因此`QByteArray`的析构器永远不会删除原始`data`，即使最后引用`data`的`QByteArray`被销毁。
随后尝试修改返回`QByteArray`内容或从中复制的任何内容时，会在修改前创建`data`数组的深度副本。这确保了原始`data`数组本身不会被`QByteArray`修改。
以下是如何用`QDataStream`读取内存中原始数据而不将原始数据复制到`QByteArray`的示例：
警告：使用 fromRawData() 创建的字节数组不会被 '\0' 终止，除非原始数据在位置 `size` 包含 '\0' 字节。虽然这对 `QDataStream` 或 `indexOf()` 等函数无关紧要，但将字节数组传递给接受预期会被 '\0' 终止的函数`const char *`会失败。

**官方示例：**

```cpp
 static const char mydata[] = {
     '\x00', '\x00', '\x03', '\x84', '\x78', '\x9c', '\x3b', '\x76',
     '\xec', '\x18', '\xc3', '\x31', '\x0a', '\xf1', '\xcc', '\x99',
     //...
     '\x6d', '\x5b'
 };

 QByteArray data = QByteArray::fromRawData(mydata, sizeof(mydata));
 QDataStream in(&data, QIODevice::ReadOnly);
 //...
```

### `[static] QByteArray QByteArray::fromRawNSData(const NSData *data)`

**作用与语义：**

构建一个使用 NSData `data`字节的 `QByteArray`。
`data`的字节不会被复制。
调用者保证只要该`QByteArray`对象存在，NSData不会被删除或修改。

### `[static] QByteArray QByteArray::fromStdString(const std::string &str)`

**作用与语义：**

返回`str`字符串的副本作为`QByteArray`。

### `char &QByteArray::front()`

**作用与语义：**

返回字节数组中的第一个字节引用。与`operator[](0)`相同。
此功能是为了STL兼容性而提供。
警告：在空字节数组上调用该函数属于未定义行为。

### `char QByteArray::front() const`

**作用与语义：**

返回字节数组中的第一个字节。和 `at(0)` 一样。
此功能是为了STL兼容性而提供。
警告：在空字节数组上调用该函数属于未定义行为。

### `[since 6.0] qsizetype QByteArray::indexOf(QByteArrayView bv, qsizetype from = 0) const`

**作用与语义：**

返回该字节数组中`bv`从索引位置`from`向前搜索时，首次出现的字节序列起始位置。如果未找到匹配，返回-1。

**官方示例：**

```cpp
 QByteArray x("sticky question");
 QByteArrayView y("sti");
 x.indexOf(y);               // returns 0
 x.indexOf(y, 1);            // returns 10
 x.indexOf(y, 10);           // returns 10
 x.indexOf(y, 11);           // returns -1
```

### `qsizetype QByteArray::indexOf(char ch, qsizetype from = 0) const`

**作用与语义：**

返回该字节数组中字节`ch`首次出现的起始位置，从索引位置`from`向前搜索。如果未找到匹配，返回-1。

**官方示例：**

```cpp
 QByteArray ba("ABCBA");
 ba.indexOf("B");            // returns 1
 ba.indexOf("B", 1);         // returns 1
 ba.indexOf("B", 2);         // returns 3
 ba.indexOf("X");            // returns -1
```

### `[since 6.0] QByteArray &QByteArray::insert(qsizetype i, QByteArrayView data)`

**作用与语义：**

在索引位置`i`插入`data`，并返回该字节数组的引用。
对于大字节数组，这一操作可能较慢（线性时间），因为它需要将索引`i`及以上的所有字节至少往内存中移动一个位置。
该数组会随着插入而增长。如果`i`超出数组末端，先扩展空格字符以达到该`i`。

**官方示例：**

```cpp
 QByteArray ba("Meal");
 ba.insert(1, QByteArrayView("ontr"));
 // ba == "Montreal"
```

### `QByteArray &QByteArray::insert(qsizetype i, const QByteArray &data)`

**作用与语义：**

在索引位置`i`插入`data`，并返回对该字节数组的引用。
该数组会随着插入而增长。如果`i`超出数组末端，阵列首先会扩展空格字符以达到该`i`。

### `QByteArray &QByteArray::insert(qsizetype i, const char *s)`

**作用与语义：**

在索引位置`i`插入`s`，并返回该字节数组的引用。
该数组会随着插入而扩展。如果`i`超出数组末端，阵列首先会扩展空格字符以达到该`i`。
该函数等价于`insert(i, QByteArrayView(s))`。

### `QByteArray &QByteArray::insert(qsizetype i, char ch)`

**作用与语义：**

在字节数组的索引位置`i`插入字节`ch`。
该数组会根据插入而扩展。如果`i`超出数组末端，阵列首先扩展空格字符以达到该`i`。

### `QByteArray &QByteArray::insert(qsizetype i, const char *data, qsizetype len)`

**作用与语义：**

从字节数组的`i`位置插入`len`字节，从`data`开始。
该数组会随着插入而扩展。如果`i`超出数组末端，阵列首先会扩展空格字符以达到该`i`。

### `QByteArray &QByteArray::insert(qsizetype i, qsizetype count, char ch)`

**作用与语义：**

在字节数组的索引位置`i`插入`count`字节`ch`副本。
该数组会随着插入而扩展。如果`i`超出数组末端，先用空格字符扩展到该`i`。

### `[constexpr noexcept] bool QByteArray::isEmpty() const`

**作用与语义：**

如果字节数组大小为0，返回`true`;否则返回`false`。

**官方示例：**

```cpp
 QByteArray().isEmpty();         // returns true
 QByteArray("").isEmpty();       // returns true
 QByteArray("abc").isEmpty();    // returns false
```

### `bool QByteArray::isLower() const`

**作用与语义：**

如果该字节数组是小写的，也就是与其`toLower()`折叠相同，返回`true`。
注意，这并不意味着字节数组只包含小写字母;仅意味着它不包含 ASCII 大写字母。

### `[noexcept] bool QByteArray::isNull() const`

**作用与语义：**

如果该字节数组为空，返回`true`;否则返回`false`。
Qt 出于历史原因区分空字节数组和空字节数组。对于大多数应用来说，关键在于字节数组是否包含任何数据，这可以通过`isEmpty()`来确定。

**官方示例：**

```cpp
 QByteArray().isNull();          // returns true
 QByteArray("").isNull();        // returns false
 QByteArray("abc").isNull();     // returns false
```

### `bool QByteArray::isUpper() const`

**作用与语义：**

如果该字节数组是大写的，也就是与其`toUpper()`折叠相同，返回`true`。
注意，这并不意味着字节数组只包含大写字母;仅意味着它不包含 ASCII 小写字母。

### `[noexcept, since 6.3] bool QByteArray::isValidUtf8() const`

**作用与语义：**

如果该字节数组包含有效的UTF-8编码数据，返回`true`，否则`false`返回。

### `[since 6.0] QByteArray QByteArray::last(qsizetype n) &&`

**作用与语义：**

返回字节数组的最后`n`字节。
注意：当`n` <0或`n` > `size()`时，行为未定义。

**官方示例：**

```cpp
 QByteArray x("Pineapple");
 QByteArray y = x.last(5);
 // y == "apple"
```

### `[since 6.0] qsizetype QByteArray::lastIndexOf(QByteArrayView bv, qsizetype from) const`

**作用与语义：**

返回该字节数组中 `bv` 最后一次出现的字节序列起始位置，从索引位置 `from` 向后搜索。
如果`from`为-1，则从最后一个字符开始搜索;如果是-2，则从倒数第二个字符开始，依此类推。
如果没有匹配，则返回-1。
注意：在搜索长度为0的`bv`时，数据末尾的匹配被负`from`排除，尽管`-1`通常被认为是从字节数组末尾搜索：结尾的匹配位于最后一个字符之后，因此被排除。要包含这样的最终空匹配，要么给出`from`的正值，要么完全省略`from`参数。

**官方示例：**

```cpp
 QByteArray x("crazy azimuths");
 QByteArrayView y("az");
 x.lastIndexOf(y);           // returns 6
 x.lastIndexOf(y, 6);        // returns 6
 x.lastIndexOf(y, 5);        // returns 2
 x.lastIndexOf(y, 1);        // returns -1
```

### `[since 6.2] qsizetype QByteArray::lastIndexOf(QByteArrayView bv) const`

**作用与语义：**

返回该字节数组中`bv`所见字节序列最后一次出现的起始位置，从字节数组末尾向后搜索。如果未找到匹配，返回-1。

**官方示例：**

```cpp
 QByteArray x("crazy azimuths");
 QByteArrayView y("az");
 x.lastIndexOf(y);           // returns 6
 x.lastIndexOf(y, 6);        // returns 6
 x.lastIndexOf(y, 5);        // returns 2
 x.lastIndexOf(y, 1);        // returns -1
```

### `qsizetype QByteArray::lastIndexOf(char ch, qsizetype from = -1) const`

**作用与语义：**

返回该字节数组中字节`ch`最后一次出现的起始位置，从索引位置`from`向后搜索。如果`from`为-1（默认值），搜索从最后一个字节（索引`size()`-1）开始。如果未找到匹配，返回-1。

**官方示例：**

```cpp
 QByteArray ba("ABCBA");
 ba.lastIndexOf("B");        // returns 3
 ba.lastIndexOf("B", 3);     // returns 3
 ba.lastIndexOf("B", 2);     // returns 1
 ba.lastIndexOf("X");        // returns -1
```

### `QByteArray QByteArray::left(qsizetype len) &&`

**作用与语义：**

返回一个包含该字节数组前`len`字节的字节数组。
如果你知道`len`不能越界，就在新代码中使用`first()`，因为它更快。
如果 `len` 大于 `size()`，则返回整个字节数组。
如果`len`小于0，返回空`QByteArray`。

### `QByteArray QByteArray::leftJustified(qsizetype width, char fill = ' ', bool truncate = false) const`

**作用与语义：**

返回一个大小为 `width` 的字节数组，包含该字节数组并填充了 `fill` 字节。
如果`truncate`为假且字节数组的`size()`大于`width`，则返回的字节数组就是该字节数组的复制品。
如果`truncate`为真且字节数组的`size()`大于`width`，则字节数组中位置`width`之后的字节会被移除，并返回该副本。

**官方示例：**

```cpp
 QByteArray x("apple");
 QByteArray y = x.leftJustified(8, '.');   // y == "apple..."
```

### `[constexpr noexcept] qsizetype QByteArray::length() const`

**作用与语义：**

和`size()`一样。

### `[static constexpr noexcept, since 6.8] qsizetype QByteArray::maxSize()`

**作用与语义：**

它返回字节数组理论上能容纳的最大元素数。实际上，这个数量可以更小，受限于系统可用的内存容量。

### `QByteArray QByteArray::mid(qsizetype pos, qsizetype len = -1) &&`

**作用与语义：**

返回一个包含该字节数组 `len` 字节的字节数组，从位置 `pos` 开始。
如果你知道`pos`和`len`不能越界，那就在新代码中使用`sliced()`，因为这样更快。
如果 `len` 为 -1（默认值）或 `pos` `len` >= `size()`，则返回一个字节数组，包含从位置 `pos` 开始直到字节数组末尾的所有字节。

### `[since 6.10] QByteArray &QByteArray::nullTerminate()`

**作用与语义：**

如果该字节数组的数据没有空终止，该方法会对数据进行深度复制，使其为空终止。
`QByteArray`默认是空终止，但在某些情况下（例如使用`fromRawData()`时），数据结尾不一定带有 `\0`，这在调用期望空终止字符串的方法（例如 C API）时可能会成为问题。

### `[since 6.10] QByteArray QByteArray::nullTerminated() &&`

**作用与语义：**

返回该字节数组的副本，且始终为空终止。参见 `nullTerminate()`。

### `[static] QByteArray QByteArray::number(int n, int base = 10)`

**作用与语义：**

返回一个表示整个数字的字节数组，`n`文本。
返回一个包含代表`n`的字符串的字节数组，使用指定的`base`（默认为十）。支持第2到第36进位，数字9以上使用字母：A为10，B为11，依此类推。
注意：数字格式未本地化;默认的 C 区域不使用，无论用户所在位置如何。使用`QLocale`进行数字和字符串之间的区域感知转换。

**官方示例：**

```cpp
 int n = 63;
 QByteArray::number(n);              // returns "63"
 QByteArray::number(n, 16);          // returns "3f"
 QByteArray::number(n, 16).toUpper();  // returns "3F"
```

### `[static] QByteArray QByteArray::number(long n, int base = 10)`

**作用与语义：**

返回一个表示整个数字的字节数组，`n`文本。
返回一个包含代表`n`的字符串的字节数组，使用指定的`base`（默认为十）。支持第2到第36进位，数字9以上使用字母：A为10，B为11，依此类推。
注意：数字格式未本地化;默认的 C 区域不使用，无论用户所在位置如何。使用`QLocale`进行数字和字符串之间的区域感知转换。

**官方示例：**

```cpp
 int n = 63;
 QByteArray::number(n);              // returns "63"
 QByteArray::number(n, 16);          // returns "3f"
 QByteArray::number(n, 16).toUpper();  // returns "3F"
```

### `[static] QByteArray QByteArray::number(qlonglong n, int base = 10)`

**作用与语义：**

返回一个表示整个数字的字节数组，`n`文本。
返回一个包含代表`n`的字符串的字节数组，使用指定的`base`（默认为十）。支持第2到第36进位，数字9以上使用字母：A为10，B为11，依此类推。
注意：数字格式未本地化;默认的 C 区域不使用，无论用户所在位置如何。使用`QLocale`进行数字和字符串之间的区域感知转换。

**官方示例：**

```cpp
 int n = 63;
 QByteArray::number(n);              // returns "63"
 QByteArray::number(n, 16);          // returns "3f"
 QByteArray::number(n, 16).toUpper();  // returns "3F"
```

### `[static] QByteArray QByteArray::number(qulonglong n, int base = 10)`

**作用与语义：**

返回一个表示整个数字的字节数组，`n`文本。
返回一个包含代表`n`的字符串的字节数组，使用指定的`base`（默认为十）。支持第2到第36进位，数字9以上使用字母：A为10，B为11，依此类推。
注意：数字格式未本地化;默认的 C 区域不使用，无论用户所在位置如何。使用`QLocale`进行数字和字符串之间的区域感知转换。

**官方示例：**

```cpp
 int n = 63;
 QByteArray::number(n);              // returns "63"
 QByteArray::number(n, 16);          // returns "3f"
 QByteArray::number(n, 16).toUpper();  // returns "3F"
```

### `[static] QByteArray QByteArray::number(uint n, int base = 10)`

**作用与语义：**

返回一个表示整个数字的字节数组，`n`文本。
返回一个包含代表`n`的字符串的字节数组，使用指定的`base`（默认为十）。支持第2到第36进位，数字9以上使用字母：A为10，B为11，依此类推。
注意：数字格式未本地化;默认的 C 区域不使用，无论用户所在位置如何。使用`QLocale`进行数字和字符串之间的区域感知转换。

**官方示例：**

```cpp
 int n = 63;
 QByteArray::number(n);              // returns "63"
 QByteArray::number(n, 16);          // returns "3f"
 QByteArray::number(n, 16).toUpper();  // returns "3F"
```

### `[static] QByteArray QByteArray::number(ulong n, int base = 10)`

**作用与语义：**

返回一个表示整个数字的字节数组，`n`文本。
返回一个包含代表`n`的字符串的字节数组，使用指定的`base`（默认为十）。支持第2到第36进位，数字9以上使用字母：A为10，B为11，依此类推。
注意：数字格式未本地化;默认的 C 区域不使用，无论用户所在位置如何。使用`QLocale`进行数字和字符串之间的区域感知转换。

**官方示例：**

```cpp
 int n = 63;
 QByteArray::number(n);              // returns "63"
 QByteArray::number(n, 16);          // returns "3f"
 QByteArray::number(n, 16).toUpper();  // returns "3F"
```

### `[static] QByteArray QByteArray::number(double n, char format = 'g', int precision = 6)`

**作用与语义：**

返回一个字节数组，表示浮点数，`n`文本。
返回一个字节数组，包含表示`n`的字符串，`format`和`precision`，含义与`QLocale::toString`（double、char、int）相同。例如：

**官方示例：**

```cpp
 QByteArray ba = QByteArray::number(12.3456, 'E', 3);
 // ba == 1.235E+01
```

### `[since 6.4] QByteArray QByteArray::percentDecoded(char percent = '%') const &`

**作用与语义：**

解码URI/URL风格的百分比编码。
返回包含解码文本的字节数组。`percent`参数允许使用与“%”不同的字符（例如“_”或“='）作为转义字符。
注意：给定无效输入（例如包含序列“%G5”的字符串，这不是有效的十六进制数），输出也会无效。举例来说：“%G5”序列可以解码为“W”。

**官方示例：**

```cpp
 QByteArray encoded("Qt%20is%20great%33");
 QByteArray decoded = encoded.percentDecoded(); // Set to "Qt is great!"
```

### `[since 6.11] QByteArray QByteArray::percentDecoded(char percent = '%') &&`

**作用与语义：**

解码URI/URL风格的百分比编码。
返回包含解码文本的字节数组。`percent`参数允许使用与“%”不同的字符（例如“_”或“='）作为转义字符。
注意：给定无效输入（例如包含序列“%G5”的字符串，这不是有效的十六进制数），输出也会无效。举例来说：“%G5”序列可以解码为“W”。

**官方示例：**

```cpp
 QByteArray encoded("Qt%20is%20great%33");
 QByteArray decoded = encoded.percentDecoded(); // Set to "Qt is great!"
```

### `QByteArray &QByteArray::prepend(QByteArrayView ba)`

**作用与语义：**

`ba`字节数组视图前加上该字节数组，并返回对该字节数组的引用。
该操作通常非常快速（常数时间），因为`QByteArray`在数据开头预分配额外空间，因此数据可以增长而无需每次重新分配整个数组。
这与插入（0， `ba`）相同。

**官方示例：**

```cpp
 QByteArray x("ship");
 QByteArray y("air");
 x.prepend(y);
 // x == "airship"
```

### `QByteArray &QByteArray::prepend(char ch)`

**作用与语义：**

在该字节数组前加上字节`ch`。

### `QByteArray &QByteArray::prepend(const QByteArray &ba)`

**作用与语义：**

`ba` 前加于该字节数组。

### `QByteArray &QByteArray::prepend(const char *str)`

**作用与语义：**

在该字节数组前加上“\0”终止字符串`str`。

### `QByteArray &QByteArray::prepend(const char *str, qsizetype len)`

**作用与语义：**

在该字节数组前加`len`字节，从`str`开始。前置的字节可能包括“\0”字节。

### `QByteArray &QByteArray::prepend(qsizetype count, char ch)`

**作用与语义：**

在该字节数组前加`count`个字节`ch`副本。

### `void QByteArray::push_back(const QByteArray &other)`

**作用与语义：**

该功能是为了STL兼容性而提供。它等同于append（`other`）。

### `[since 6.0] void QByteArray::push_back(QByteArrayView str)`

**作用与语义：**

和 append（`str`） 一样。

### `void QByteArray::push_back(char ch)`

**作用与语义：**

和 append（`ch`）一样。

### `void QByteArray::push_back(const char *str)`

**作用与语义：**

和 append（`str`） 一样。

### `void QByteArray::push_front(const QByteArray &other)`

**作用与语义：**

该功能是为了STL兼容性而提供。它等价于prepend（`other`）。

### `[since 6.0] void QByteArray::push_front(QByteArrayView str)`

**作用与语义：**

和prepend（`str`）一样。

### `void QByteArray::push_front(char ch)`

**作用与语义：**

和prepend（`ch`）一样。

### `void QByteArray::push_front(const char *str)`

**作用与语义：**

和prepend（`str`）一样。

### `QByteArray::reverse_iterator QByteArray::rbegin()`

**作用与语义：**

返回一个STL风格的反向迭代器，指向字节数组中的第一个字节，顺序相反。
警告：返回的迭代器在脱离或`QByteArray`修改时将失效。

### `[noexcept] QByteArray::const_reverse_iterator QByteArray::rbegin() const`

**作用与语义：**

返回一个STL风格的反向迭代器，指向字节数组中的第一个字节，顺序相反。
警告：返回的迭代器在脱离或`QByteArray`修改时将失效。

### `QByteArray &QByteArray::remove(qsizetype pos, qsizetype len)`

**作用与语义：**

从数组中移除`len`字节，从索引位置`pos`开始，返回数组的引用。
如果`pos`超出范围，则不会发生任何事。如果`pos`有效，但`pos` `len`大于数组大小，则数组在位置`pos`被截断。
元素移除可以保留数组容量，而不会减少分配的内存。为了减少多余容量并释放尽可能多的内存，可以在数组大小最后一次更改后调用`squeeze()`。

**官方示例：**

```cpp
 QByteArray ba("Montreal");
 ba.remove(1, 4);
 // ba == "Meal"
```

### `[since 6.5] QByteArray &QByteArray::removeAt(qsizetype pos)`

**作用与语义：**

移除索引`pos`的字符。如果`pos`超出边界（即 `pos` >= `size()`），该函数不做任何事。

### `[since 6.5] QByteArray &QByteArray::removeFirst()`

**作用与语义：**

移除该字节数组中的第一个字符。如果字节数组为空，该函数不做任何操作。

### `[since 6.1] template <typename Predicate> QByteArray &QByteArray::removeIf(Predicate pred)`

**作用与语义：**

从字节数组中移除所有谓词`pred`返回为真字节的字节。返回对字节数组的引用。

### `[since 6.5] QByteArray &QByteArray::removeLast()`

**作用与语义：**

移除该字节数组中的最后一个字符。如果字节数组为空，该函数不做任何操作。

### `QByteArray::reverse_iterator QByteArray::rend()`

**作用与语义：**

返回一个STL风格的反向迭代器，指向字节数组最后一个字节之后，顺序相反。
警告：返回的迭代器在分离或`QByteArray`修改时将失效。

### `[noexcept] QByteArray::const_reverse_iterator QByteArray::rend() const`

**作用与语义：**

返回一个STL风格的反向迭代器，指向字节数组最后一个字节之后，顺序相反。
警告：返回的迭代器在分离或`QByteArray`修改时将失效。

### `QByteArray QByteArray::repeated(qsizetype times) const`

**作用与语义：**

返回一个重复指定数量`times`字节数组的副本。
如果`times`小于1，则返回一个空字节数组。

**官方示例：**

```cpp
 QByteArray ba("ab");
 ba.repeated(4);             // returns "abababab"
```

### `QByteArray &QByteArray::replace(qsizetype pos, qsizetype len, QByteArrayView after)`

**作用与语义：**

用字节数组 `after` 替换`pos` 的索引位置的`len`字节，并返回该字节数组的引用。

**官方示例：**

```cpp
 QByteArray x("Say yes!");
 QByteArray y("no");
 x.replace(4, 3, y);
 // x == "Say no!"
```

### `[since 6.0] QByteArray &QByteArray::replace(QByteArrayView before, QByteArrayView after)`

**作用与语义：**

将字节数组`before`的每次出现都替换为字节数组`after`。

**官方示例：**

```cpp
 QByteArray ba("colour behaviour flavour neighbour");
 ba.replace(QByteArray("ou"), QByteArray("o"));
 // ba == "color behavior flavor neighbor"
```

### `QByteArray &QByteArray::replace(char before, QByteArrayView after)`

**作用与语义：**

用字节数组`after`替换了所有字节`before`的出现。

### `QByteArray &QByteArray::replace(char before, char after)`

**作用与语义：**

将每一次字节`before`的出现都替换为字节`after`。

### `QByteArray &QByteArray::replace(const char *before, qsizetype bsize, const char *after, qsizetype asize)`

**作用与语义：**

将从`before`开始的`bsize`字节的出现替换为从`after`开始的`asize`字节。由于字符串大小由`bsize`和`asize`决定，它们可能包含“\0”字节，无需“\0”终止。

### `QByteArray &QByteArray::replace(qsizetype pos, qsizetype len, const char *after, qsizetype alen)`

**作用与语义：**

将索引位置`pos`的`len`字节替换为从位置`after`开始的 `alen` 字节。插入的字节可能包括 '\0' 字节。

### `void QByteArray::reserve(qsizetype size)`

**作用与语义：**

尝试分配至少`size`字节的内存。
如果你提前知道字节数组的大小，就可以调用这个函数，而且频繁调用`resize()`通常会获得更好的性能。
如果不确定需要多少空间，通常最好用`size`的上限，或者如果严格的上限远大于这个，则使用最可能规模的较高估计值。如果`size`是低估，一旦超过预留空间，数组会根据需要增长，这可能导致分配比最佳高估更大，并减缓触发该值的操作速度。
警告：reserve() 保留内存，但不会改变字节数组的大小。访问字节数组末尾以外的数据是未定义的行为。如果你需要访问数组当前端以外的内存，请使用 `resize()`。
该函数的唯一目的是提供一种微调`QByteArray`内存使用的方法。一般来说，你很少需要调用这个函数。

### `void QByteArray::resize(qsizetype size)`

**作用与语义：**

将字节数组大小设置为`size`字节。
如果`size`大于当前大小，字节数组会扩展为`size`字节，后面加了额外的字节。新字节未初始化。
如果`size`小于当前大小，超出位置`size`的字节将被排除在字节数组之外。
注意：虽然resize()会在需要时增加容量，但不会减少容量。要减少多余容量，请使用`squeeze()`。

### `[since 6.4] void QByteArray::resize(qsizetype newSize, char c)`

**作用与语义：**

将字节数组大小设置为`newSize`字节。
如果`newSize`大于当前大小，字节数组会扩展为`newSize`字节，并加上额外的字节。新字节被初始化为`c`。
如果`newSize`小于当前大小，超出位置`newSize`的字节将被排除在字节数组之外。
注意：虽然resize()会根据需要增加容量，但不会减少容量。要减少多余容量，请使用`squeeze()`。

### `[since 6.8] void QByteArray::resizeForOverwrite(qsizetype size)`

**作用与语义：**

将字节数组调整为`size`字节。如果字节数组大小增加，新字节将未初始化。
行为和`resize(size)`完全一样。

### `QByteArray QByteArray::right(qsizetype len) &&`

**作用与语义：**

返回一个字节数组，包含该字节数组的最后`len`字节。
如果你知道`len`不能越界，就用新代码中的`last()`，因为这样更快。
如果 `len` 大于 `size()`，整个字节数组将返回。
如果`len`小于0，则返回空`QByteArray`。

### `QByteArray QByteArray::rightJustified(qsizetype width, char fill = ' ', bool truncate = false) const`

**作用与语义：**

返回一个大小为 `width` 的字节数组，包含 `fill` 字节后面跟着该字节数组。
如果`truncate`为假且字节数组大小大于`width`，则返回的字节数组是该字节数组的复制品。
如果`truncate`为真且字节数组大小大于`width`，则生成的字节数组在`width`处被截断。

**官方示例：**

```cpp
 QByteArray x("apple");
 QByteArray y = x.rightJustified(8, '.');    // y == "...apple"
```

### `QByteArray &QByteArray::setNum(int n, int base = 10)`

**作用与语义：**

将整数表示为文本`n`。
将该字节数组设置为代表`n`的字符串，底部为`base`（默认为十），并返回对该字节数组的引用。支持第2到第36进制，使用字母表示9以上的数字;A为十，B为十一，依此类推。
注意：数字格式未本地化;默认的 C 区域不使用，无论用户所在位置如何。使用`QLocale`进行数字和字符串之间的区域感知转换。

**官方示例：**

```cpp
 QByteArray ba;
 int n = 63;
 ba.setNum(n);           // ba == "63"
 ba.setNum(n, 16);       // ba == "3f"
```

### `QByteArray &QByteArray::setNum(long n, int base = 10)`

**作用与语义：**

将整数表示为文本`n`。
将该字节数组设置为代表`n`的字符串，底部为`base`（默认为十），并返回对该字节数组的引用。支持第2到第36进制，使用字母表示9以上的数字;A为十，B为十一，依此类推。
注意：数字格式未本地化;默认的 C 区域不使用，无论用户所在位置如何。使用`QLocale`进行数字和字符串之间的区域感知转换。

**官方示例：**

```cpp
 QByteArray ba;
 int n = 63;
 ba.setNum(n);           // ba == "63"
 ba.setNum(n, 16);       // ba == "3f"
```

### `QByteArray &QByteArray::setNum(qlonglong n, int base = 10)`

**作用与语义：**

将整数表示为文本`n`。
将该字节数组设置为代表`n`的字符串，底部为`base`（默认为十），并返回对该字节数组的引用。支持第2到第36进制，使用字母表示9以上的数字;A为十，B为十一，依此类推。
注意：数字格式未本地化;默认的 C 区域不使用，无论用户所在位置如何。使用`QLocale`进行数字和字符串之间的区域感知转换。

**官方示例：**

```cpp
 QByteArray ba;
 int n = 63;
 ba.setNum(n);           // ba == "63"
 ba.setNum(n, 16);       // ba == "3f"
```

### `QByteArray &QByteArray::setNum(qulonglong n, int base = 10)`

**作用与语义：**

将整数表示为文本`n`。
将该字节数组设置为代表`n`的字符串，底部为`base`（默认为十），并返回对该字节数组的引用。支持第2到第36进制，使用字母表示9以上的数字;A为十，B为十一，依此类推。
注意：数字格式未本地化;默认的 C 区域不使用，无论用户所在位置如何。使用`QLocale`进行数字和字符串之间的区域感知转换。

**官方示例：**

```cpp
 QByteArray ba;
 int n = 63;
 ba.setNum(n);           // ba == "63"
 ba.setNum(n, 16);       // ba == "3f"
```

### `QByteArray &QByteArray::setNum(short n, int base = 10)`

**作用与语义：**

将整数表示为文本`n`。
将该字节数组设置为代表`n`的字符串，底部为`base`（默认为十），并返回对该字节数组的引用。支持第2到第36进制，使用字母表示9以上的数字;A为十，B为十一，依此类推。
注意：数字格式未本地化;默认的 C 区域不使用，无论用户所在位置如何。使用`QLocale`进行数字和字符串之间的区域感知转换。

**官方示例：**

```cpp
 QByteArray ba;
 int n = 63;
 ba.setNum(n);           // ba == "63"
 ba.setNum(n, 16);       // ba == "3f"
```

### `QByteArray &QByteArray::setNum(uint n, int base = 10)`

**作用与语义：**

将整数表示为文本`n`。
将该字节数组设置为代表`n`的字符串，底部为`base`（默认为十），并返回对该字节数组的引用。支持第2到第36进制，使用字母表示9以上的数字;A为十，B为十一，依此类推。
注意：数字格式未本地化;默认的 C 区域不使用，无论用户所在位置如何。使用`QLocale`进行数字和字符串之间的区域感知转换。

**官方示例：**

```cpp
 QByteArray ba;
 int n = 63;
 ba.setNum(n);           // ba == "63"
 ba.setNum(n, 16);       // ba == "3f"
```

### `QByteArray &QByteArray::setNum(ulong n, int base = 10)`

**作用与语义：**

将整数表示为文本`n`。
将该字节数组设置为代表`n`的字符串，底部为`base`（默认为十），并返回对该字节数组的引用。支持第2到第36进制，使用字母表示9以上的数字;A为十，B为十一，依此类推。
注意：数字格式未本地化;默认的 C 区域不使用，无论用户所在位置如何。使用`QLocale`进行数字和字符串之间的区域感知转换。

**官方示例：**

```cpp
 QByteArray ba;
 int n = 63;
 ba.setNum(n);           // ba == "63"
 ba.setNum(n, 16);       // ba == "3f"
```

### `QByteArray &QByteArray::setNum(ushort n, int base = 10)`

**作用与语义：**

将整数表示为文本`n`。
将该字节数组设置为代表`n`的字符串，底部为`base`（默认为十），并返回对该字节数组的引用。支持第2到第36进制，使用字母表示9以上的数字;A为十，B为十一，依此类推。
注意：数字格式未本地化;默认的 C 区域不使用，无论用户所在位置如何。使用`QLocale`进行数字和字符串之间的区域感知转换。

**官方示例：**

```cpp
 QByteArray ba;
 int n = 63;
 ba.setNum(n);           // ba == "63"
 ba.setNum(n, 16);       // ba == "3f"
```

### `QByteArray &QByteArray::setNum(double n, char format = 'g', int precision = 6)`

**作用与语义：**

将浮点数表示为文本`n`。
将该字节数组设置为表示 `n` 的字符串，`format` 和 `precision`（含义与 `QString::number`（double， char， int）相同），并返回对该字节数组的引用。

### `QByteArray &QByteArray::setNum(float n, char format = 'g', int precision = 6)`

**作用与语义：**

将浮点数表示为文本`n`。
将该字节数组设置为表示 `n` 的字符串，`format` 和 `precision`（含义与 `QString::number`（double， char， int）相同），并返回对该字节数组的引用。

### `QByteArray &QByteArray::setRawData(const char *data, qsizetype size)`

**作用与语义：**

重置`QByteArray`，使用`data`数组的前`size`字节。这些字节不会被复制。`QByteArray`将包含`data`指针。调用者保证只要该`QByteArray`及其未被修改的副本存在，`data`不会被删除或修改。
该函数可以代替`fromRawData()`，用于重复利用现有`QByteArray`对象，以节省内存重新分配。

### `void QByteArray::shrink_to_fit()`

**作用与语义：**

该功能是为了STL兼容性而提供。它等同于`squeeze()`。

### `QByteArray QByteArray::simplified() const`

**作用与语义：**

返回该字节数组的副本，其间距字符从起始和结束处被移除，且每个内部间距字符序列被替换为单一空格。
间距字符是标准 C `isspace()` 函数在 C 区域返回 `true` 的字符;这些字符包括 ASCII 字符的表表 '\t'、换行 '\n'、回车 '\r'、垂直表单 '\v'、表单 feed '\f' 和空格 ' '。

**官方示例：**

```cpp
 QByteArray ba("  lots\t of\nwhitespace\r\n ");
 ba = ba.simplified();
 // ba == "lots of whitespace";
```

### `[constexpr noexcept] qsizetype QByteArray::size() const`

**作用与语义：**

返回该字节数组中的字节数。
字节数组的最后一个字节位置大小为 () - 1。此外，`QByteArray` 确保位置大小()的字节始终为 “\0”，这样你可以使用 `data()` 和 `constData()` 的返回值作为期望 '\0' 终止字符串的函数的参数。如果`QByteArray`对象是从不包含尾随 '\0' 终止字节的原始数据创建的，那么除非创建深度副本，`QByteArray` 就不会自动添加。

**官方示例：**

```cpp
 QByteArray ba("Hello");
 qsizetype n = ba.size();    // n == 5
 ba.data()[0];               // returns 'H'
 ba.data()[4];               // returns 'o'
 ba.data()[5];               // returns '\0'
```

### `[since 6.8] QByteArray &QByteArray::slice(qsizetype pos, qsizetype n)`

**作用与语义：**

修改该字节数组从位置`pos`开始，延伸`n`字节，并返回该字节数组的引用。
注意：行为未定义，`pos` <为0、`n` <0或`pos` `n` > `size()`。

**官方示例：**

```cpp
 QByteArray x = "Five pineapples"_ba;
 x.slice(5);     // x == "pineapples"
 x.slice(4, 3);  // x == "app"
```

### `[since 6.8] QByteArray &QByteArray::slice(qsizetype pos)`

**作用与语义：**

修改该字节数组从位置`pos`开始，延伸至末尾，并返回该字节数组的引用。
注意：行为未定义，`pos` <0或`pos` > `size()`。

### `[since 6.0] QByteArray QByteArray::sliced(qsizetype pos, qsizetype n) &&`

**作用与语义：**

返回一个字节数组，包含该对象从位置`pos`开始的`n`字节。
注意：当`pos` <0、`n` <0或`pos` `n` > `size()`时，行为未定义。

**官方示例：**

```cpp
 QByteArray x("Five pineapples");
 QByteArray y = x.sliced(5, 4);     // y == "pine"
 QByteArray z = x.sliced(5);        // z == "pineapples"
```

### `[since 6.0] QByteArray QByteArray::sliced(qsizetype pos) &&`

**作用与语义：**

返回一个字节数组，包含该对象从位置`pos`开始的`n`字节。
注意：当`pos` <0、`n` <0或`pos` `n` > `size()`时，行为未定义。

**官方示例：**

```cpp
 QByteArray x("Five pineapples");
 QByteArray y = x.sliced(5, 4);     // y == "pine"
 QByteArray z = x.sliced(5);        // z == "pineapples"
```

### `QList<QByteArray> QByteArray::split(char sep) const`

**作用与语义：**

在出现`sep`的地方将字节数组拆分为子数组，并返回这些数组的列表。如果`sep`在字节数组中任何地方不匹配，split() 返回包含该字节数组的单元素列表。

### `void QByteArray::squeeze()`

**作用与语义：**

释放不需要存储数组数据的内存。
该函数的唯一目的是提供一种微调`QByteArray`内存使用的方法。一般来说，你很少需要调用这个函数。

### `[since 6.0] bool QByteArray::startsWith(QByteArrayView bv) const`

**作用与语义：**

如果该字节数组以`bv`所见的字节序列开始，返回`true`;否则返回`false`。

**官方示例：**

```cpp
 QByteArray url("ftp://ftp.qt-project.org/");
 if (url.startsWith("ftp:"))
     {/*...*/}
```

### `bool QByteArray::startsWith(char ch) const`

**作用与语义：**

如果该字节数组以字节`ch`开头，返回`true`;否则返回`false`。

### `[noexcept] void QByteArray::swap(QByteArray &other)`

**作用与语义：**

将该字节数组与`other`交换。此操作非常快且从未失败。

### `QByteArray QByteArray::toBase64(QByteArray::Base64Options options = Base64Encoding) const`

**作用与语义：**

返回一个字节数组的副本，使用选项`options`编码。
用于编码Base64编码数据的算法定义在RFC 4648中。

**官方示例：**

```cpp
 QByteArray text("Qt is great!");
 text.toBase64();        // returns "UXQgaXMgZ3JlYXQh"

 QByteArray hello("<p>Hello?</p>");
 hello.toBase64(QByteArray::Base64Encoding | QByteArray::OmitTrailingEquals);      // returns "PHA+SGVsbG8/PC9wPg"
 hello.toBase64(QByteArray::Base64Encoding);                                       // returns "PHA+SGVsbG8/PC9wPg=="
 hello.toBase64(QByteArray::Base64UrlEncoding);                                    // returns "PHA-SGVsbG8_PC9wPg=="
 hello.toBase64(QByteArray::Base64UrlEncoding | QByteArray::OmitTrailingEquals);   // returns "PHA-SGVsbG8_PC9wPg"
```

### `CFDataRef QByteArray::toCFData() const`

**作用与语义：**

从`QByteArray`创建CFData。
调用者拥有CFData对象，并负责释放它。

### `double QByteArray::toDouble(bool *ok = nullptr) const`

**作用与语义：**

返回转换为`double`值的字节数组。
如果转换溢出，返回无穷大;如果因其他原因（如溢出），则返回0.0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`来报告失败，成功则将*`ok`设为`true`。
警告：`QByteArray`内容可能仅包含有效的数字字符，包括加号/减号、科学记号中使用的字符e和小数点。添加单位或额外字符会导致转换错误。
注意：数字转换在默认的 C 区域执行，无论用户所在位置如何。使用 `QLocale` 进行数字和字符串之间的区域感知转换。
该函数忽略前置和后置的空白。

**官方示例：**

```cpp
 QByteArray string("1234.56");
 bool ok;
 double a = string.toDouble(&ok);   // a == 1234.56, ok == true

 string = "1234.56 Volt";
 a = string.toDouble(&ok);             // a == 0, ok == false
```

### `[since 6.5] emscripten::val QByteArray::toEcmaUint8Array()`

**作用与语义：**

从`QByteArray`创建Uint8Array。
该函数将`QByteArray`拥有的堆内存数据传输到JavaScript数据缓冲区。该函数将数据分配并复制到ArrayBuffer中，并返回Uint8Array视图到该缓冲区。
JavaScript对象拥有数据的副本，复制后该`QByteArray`可以安全删除。

**官方示例：**

```cpp
 QByteArray byteArray = "test";
 emscripten::val uint8array = byteArray.toEcmaUint8Array();
```

### `float QByteArray::toFloat(bool *ok = nullptr) const`

**作用与语义：**

返回转换为`float`值的字节数组。
如果转换溢出，返回无穷大;如果因其他原因（如溢出），则返回0.0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`报告失败，成功则将*`ok`设为`true`。
警告：`QByteArray`内容可能仅包含有效的数字字符，包括加减号、科学记号中的字符e和小数点。添加单位或额外字符会导致转换错误。
注意：数字转换在默认的 C 区域内进行，无论用户所在的位置如何。使用 `QLocale` 进行数字和字符串之间的区域感知转换。
该函数忽略前置和后置的空白。

**官方示例：**

```cpp
 QByteArray string("1234.56");
 bool ok;
 float a = string.toFloat(&ok);    // a == 1234.56, ok == true

 string = "1234.56 Volt";
 a = string.toFloat(&ok);              // a == 0, ok == false
```

### `QByteArray QByteArray::toHex(char separator = '\0') const`

**作用与语义：**

返回一个十六进制编码的字节数组副本。
十六进制编码使用数字0-9和字母a-f。
如果`separator`不是“\0”，则在十六进制字节之间插入分隔符。

**官方示例：**

```cpp
 QByteArray macAddress = QByteArray::fromHex("123456abcdef");
 macAddress.toHex(':'); // returns "12:34:56:ab:cd:ef"
 macAddress.toHex(0);   // returns "123456abcdef"
```

### `int QByteArray::toInt(bool *ok = nullptr, int base = 10) const`

**作用与语义：**

返回使用底`base`转换为`int`的字节数组，默认为十。支持底数0和2至36，数字9以上使用字母;A为十，B为十一，依此类推。
如果`base`为0，则根据以下规则自动确定基数：如果字节数组以“0x”开头，则假设为十六进制（以16为底）;否则，如果以“0b”开头，则假设为二进制（以2为底）;否则，如果以“0”开头，则假设为八进制（以8为底）;否则则假设为十进制。
如果转换失败，则返回0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`报告失败，成功则将*`ok`设为`true`。
注意：数字转换在默认的 C 区域执行，无论用户所在位置如何。使用 `QLocale` 进行数字和字符串之间的区域感知转换。
注意：在Qt 6.4中加入了对“0b”前缀的支持。

**官方示例：**

```cpp
 QByteArray str("FF");
 bool ok;
 int hex = str.toInt(&ok, 16);     // hex == 255, ok == true
 int dec = str.toInt(&ok, 10);     // dec == 0, ok == false
```

### `long QByteArray::toLong(bool *ok = nullptr, int base = 10) const`

**作用与语义：**

返回使用底`base`转换为`long`整数的字节数组，默认为十。支持底数0和2至36，使用字母表示9以上的数字;A为十，B为十一，依此类推。
如果`base`为0，则根据以下规则自动确定基位：如果字节数组以“0x”开头，则假设为十六进制（进制16）;否则，如果以“0b”开头，则假设为二进制（进制2）;否则，如果以“0”开头，则假设为八进制（以8为底）;否则则假设为十进制。
如果转换失败，则返回0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`报告失败，成功则将*`ok`设为`true`。
注意：数字转换在默认的 C 区域执行，无论用户所在的位置如何。使用`QLocale`进行数字和字符串之间的区域感知转换。
注意：在Qt 6.4中加入了对“0b”前缀的支持。

**官方示例：**

```cpp
 QByteArray str("FF");
 bool ok;
 long hex = str.toLong(&ok, 16);   // hex == 255, ok == true
 long dec = str.toLong(&ok, 10);   // dec == 0, ok == false
```

### `qlonglong QByteArray::toLongLong(bool *ok = nullptr, int base = 10) const`

**作用与语义：**

返回用`base`为底的字节数组转换为`long long`，默认为十。支持0、2到36的数字，使用字母表示9以上的数字;A为十，B为十一，依此类推。
如果`base`为0，则根据以下规则自动确定基位：如果字节数组以“0x”开头，则假设为十六进制（进制16）;否则，如果以“0b”开头，则假设为二进制（进制2）;否则，如果以“0”开头，则假设为八进制（以8为底）;否则则假设为十进制。
如果转换失败，则返回0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`报告失败，成功则将*`ok`设为`true`。
注意：数字转换在默认的 C 区域执行，无论用户所在位置如何。使用 `QLocale` 进行数字和字符串之间的区域感知转换。
注意：在Qt 6.4中加入了对“0b”前缀的支持。

### `QByteArray QByteArray::toLower() const`

**作用与语义：**

返回字节数组副本，其中每个 ASCII 大写字母转换为小写字母。

**官方示例：**

```cpp
 QByteArray x("Qt by THE QT COMPANY");
 QByteArray y = x.toLower();
 // y == "qt by the qt company"
```

### `NSData *QByteArray::toNSData() const`

**作用与语义：**

从`QByteArray`创建NSData。
NSData对象是自动释放的。

### `QByteArray QByteArray::toPercentEncoding(const QByteArray &exclude = QByteArray(), const QByteArray &include = QByteArray(), char percent = '%') const`

**作用与语义：**

返回一个类似URI/URL的百分比编码字节数组副本。`percent`参数允许你覆盖默认的“%”字符以换取另一个字节。
默认情况下，该函数会编码所有不属于以下之一的字节：
ALPHA（“a”到“z”，“A”到“Z”）/DIGIT（0到9）/“-” / “.”/“_” / “~”。
为了防止字节被编码，将字节传递给`exclude`。为了强制编码字节，则传给`include`。`percent`字符始终被编码。
十六进制编码使用数字0-9和大写字母A-F。

**官方示例：**

```cpp
 QByteArray text = "{a fishy string?}";
 QByteArray ba = text.toPercentEncoding("{}", "s");
 qDebug("%s", ba.constData());
 // prints "{a fi%73hy %73tring%3F}"
```

### `CFDataRef QByteArray::toRawCFData() const`

**作用与语义：**

构建一个使用 `QByteArray` 字节的 CFData。
`QByteArray`的字节不会被复制。
调用者保证只要该CFData对象存在，该`QByteArray`不会被删除或修改。

### `NSData *QByteArray::toRawNSData() const`

**作用与语义：**

构建一个使用`QByteArray`字节的NSData。
`QByteArray`的字节不会被复制。
调用者保证只要该NSData对象存在，`QByteArray`不会被删除或修改。

### `short QByteArray::toShort(bool *ok = nullptr, int base = 10) const`

**作用与语义：**

返回使用底数`base`转换为`short`的字节数组，默认为十。支持底数0和2至36，数字9以上使用字母;A为十，B为十一，依此类推。
如果 `base` 为 0，则根据以下规则自动确定基数：如果字节数组以“0x”开头，则假设为十六进制（以 16 为底）;否则，如果以 “0b” 开头，则假设为二进制（以 2 为底）;否则，如果以“0”开头，则假设为八进制（以 8 进制为本）;否则则假设为十进制。
如果转换失败，则返回0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`报告失败，成功则将*`ok`设为`true`。
注意：数字转换在默认的 C 区域执行，无论用户所在的位置如何。使用 `QLocale` 进行数字和字符串之间的区域感知转换。
注意：在Qt 6.4中加入了对“0b”前缀的支持。

### `std::string QByteArray::toStdString() const`

**作用与语义：**

返回一个包含该`QByteArray`数据的std：：string对象。
该运算符主要用于将`QByteArray`传递给接受 std：：string 对象的函数。

### `uint QByteArray::toUInt(bool *ok = nullptr, int base = 10) const`

**作用与语义：**

返回用`base`为底的字节数组转换为`unsigned int`，默认为十。支持第0和第2到第36进制，使用字母表示9以上的数字;A为十，B为十一，依此类推。
如果`base`为0，则根据以下规则自动确定基位：如果字节数组以“0x”开头，则假设为十六进制（进制16）;否则，如果以“0b”开头，则假设为二进制（进制2）;否则，如果以“0”开头，则假设为八进制（以8为底）;否则则假设为十进制。
如果转换失败，则返回0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`报告失败，成功则将*`ok`设为`true`。
注意：数字转换在默认的 C 区域执行，无论用户所在位置如何。使用 `QLocale` 进行数字和字符串之间的区域感知转换。
注意：在Qt 6.4中加入了对“0b”前缀的支持。

### `ulong QByteArray::toULong(bool *ok = nullptr, int base = 10) const`

**作用与语义：**

返回使用底`base`转换为`unsigned long int`的字节数组，默认为十。支持底数0和2至36，数字9以上使用字母表示;A为十，B为十一，依此类推。
如果`base`为0，则根据以下规则自动确定基位：如果字节数组以“0x”开头，则假设为十六进制（进制16）;否则，如果以“0b”开头，则假设为二进制（进制2）;否则，如果以“0”开头，则假设为八进制（以8为底）;否则则假设为十进制。
如果转换失败，则返回0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`报告失败，成功则将*`ok`设为`true`。
注意：数字转换在默认的 C 区域执行，无论用户所在的位置如何。使用`QLocale`进行数字和字符串之间的区域感知转换。
注意：在Qt 6.4中加入了对“0b”前缀的支持。

### `qulonglong QByteArray::toULongLong(bool *ok = nullptr, int base = 10) const`

**作用与语义：**

返回用`base`为底的`unsigned long long`转换为的字节数组，默认为十。支持第0、2到36的底数，使用字母表示9以上的数字;A为十，B为十一，依此类推。
如果 `base` 为 0，则根据以下规则自动确定基数：如果字节数组以“0x”开头，则假设为十六进制（以 16 为底）;否则，如果以 “0b” 开头，则假设为二进制（以 2 为底）;否则，如果以“0”开头，则假设为八进制（以 8 进制为本）;否则则假设为十进制。
如果转换失败，则返回0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`报告失败，成功则将*`ok`设为`true`。
注意：数字转换在默认的 C 区域执行，无论用户所在的位置如何。使用 `QLocale` 进行数字和字符串之间的区域感知转换。
注意：在Qt 6.4中加入了对“0b”前缀的支持。

### `ushort QByteArray::toUShort(bool *ok = nullptr, int base = 10) const`

**作用与语义：**

返回使用底`base`转换为`unsigned short`的字节数组，默认为十。支持底数0和2至36，数字9以上使用字母;A为十，B为十一，依此类推。
如果`base`为0，则根据以下规则自动确定基数：如果字节数组以“0x”开头，则假设为十六进制（以16为底）;否则，如果以“0b”开头，则假设为二进制（以2为底）;否则，如果以“0”开头，则假设为八进制（以8为底）;否则则假设为十进制。
如果转换失败，则返回0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`报告失败，成功则将*`ok`设为`true`。
注意：数字转换在默认的 C 区域执行，无论用户所在位置如何。使用 `QLocale` 进行数字和字符串之间的区域感知转换。
注意：在Qt 6.4中加入了对“0b”前缀的支持。

### `QByteArray QByteArray::toUpper() const`

**作用与语义：**

返回一个字节数组副本，其中每个 ASCII 小写字母转换为大写字母。

**官方示例：**

```cpp
 QByteArray x("Qt by THE QT COMPANY");
 QByteArray y = x.toUpper();
 // y == "QT BY THE QT COMPANY"
```

### `QByteArray QByteArray::trimmed() const`

**作用与语义：**

返回该字节数组的副本，且在开头和结尾去除了空格字符。
间距字符是标准C `isspace()`函数在C语言区域返回`true`的字符;这些字符包括ASCII字符的“\t”、换行“\n”、回车“\r”、垂直表单“\v”、表单输入“\f”和空格“'。
与`simplified()`不同，trimmed() 保持内部间距不变。

**官方示例：**

```cpp
 QByteArray ba("  lots\t of\nwhitespace\r\n ");
 ba = ba.trimmed();
 // ba == "lots\t of\nwhitespace";
```

### `void QByteArray::truncate(qsizetype pos)`

**作用与语义：**

在索引位置`pos`截断字节数组。
如果`pos`在阵列的尽头之外，则不会发生任何事。

**官方示例：**

```cpp
 QByteArray ba("Stockholm");
 ba.truncate(5);             // ba == "Stock"
```

### `QByteArray::operator const void *() const`

**作用与语义：**

注意：新代码中请使用`constData()`。
返回存储在字节数组中的数据指针。该指针可用于访问组成数组的字节。数据为“\0”终止。
只要不发生分离且`QByteArray`未被修改，指针依然有效。
该运算符主要用于将字节数组传递给接受`const char *`的函数。
你可以通过在编译应用程序时定义`QT_NO_CAST_FROM_BYTEARRAY`来禁用这个操作符。
注意：`QByteArray`可以存储包括“\0”在内的任何字节值，但大多数`char *`参数的函数假设数据在遇到的第一个“\0”处结束。

### `[noexcept, since 6.10] QByteArray::operator std::string_view() const`

**作用与语义：**

将该`QByteArray`对象转换为`std::string_view`对象。返回的字符串视图将跨越整个字节数组。

### `QByteArray &QByteArray::operator+=(const QByteArray &ba)`

**作用与语义：**

将`ba`字节数组附加到该字节数组末尾，并返回对该字节数组的引用。
注意：`QByteArray` 是一个隐式共享类。因此，如果你对空字节数组进行附加，字节数组将仅共享`ba`中存储的数据。在这种情况下，不进行数据复制，耗时为常数。如果共享实例被修改，则会被复制（写时复制），耗时为线性时间。
如果被附加的字节数组不是空的，则会对数据进行深度复制，时间为线性。
该操作通常不会有分配开销，因为`QByteArray`在数据末尾预先分配额外空间，使数据可以增长而无需每次附加操作重新分配。

**官方示例：**

```cpp
 QByteArray x("free");
 QByteArray y("dom");
 x += y;
 // x == "freedom"
```

### `QByteArray &QByteArray::operator+=(char ch)`

**作用与语义：**

将字节`ch`附加到该字节数组末尾，并返回对该字节数组的引用。

### `QByteArray &QByteArray::operator+=(const char *str)`

**作用与语义：**

将“\0”终止字符串`str`附加到该字节数组末尾，返回该字节数组的引用。

### `[noexcept] QByteArray &QByteArray::operator=(QByteArray &&other)`

**作用与语义：**

Move-assign `other`到该`QByteArray`实例。

### `[noexcept] QByteArray &QByteArray::operator=(const QByteArray &other)`

**作用与语义：**

将`other`分配到该字节数组，并返回对该字节数组的引用。

### `QByteArray &QByteArray::operator=(const char *str)`

**作用与语义：**

将`str`分配到该字节数组。
`str`假定指向一个零端结字符串，其长度通过动态确定。

### `char &QByteArray::operator[](qsizetype i)`

**作用与语义：**

返回索引位置的字节 `i` 作为可修改的引用。
`i` 必须是字节数组中的有效索引位置（即 0 <= `i` < `size()`）。

**官方示例：**

```cpp
 QByteArray ba("Hello, world");
 cout << ba[0]; // prints H
 ba[7] = 'W';
 // ba == "Hello, World"
```

### `char QByteArray::operator[](qsizetype i) const`

**作用与语义：**

和at（`i`）一样。

### `[since 6.1] template <typename T> qsizetype erase(QByteArray &ba, const T &t)`

**作用与语义：**

从字节数组中移除所有与`t`比较的元素`ba`。返回移除的元素数量（如有）。

### `[since 6.1] template <typename Predicate> qsizetype erase_if(QByteArray &ba, Predicate pred)`

**作用与语义：**

从字节数组中移除所有谓词 `pred` 返回为真元素`ba`。返回被移除的元素数量（如有）。

### `quint16 qChecksum(QByteArrayView data, Qt::ChecksumType standard = Qt::ChecksumIso3309)`

**作用与语义：**

返回CRC-16的校验码`data`。
校验和与字节顺序（端序）无关，计算将依据`standard`中发布的算法进行计算。默认情况下，使用ISO 3309（`Qt::ChecksumIso3309`）中发布的算法。
注意：该函数是CRC-16-CCITT算法的16位缓存守恒（16条表）实现。

### `QByteArray qCompress(const QByteArray &data, int compressionLevel = -1)`

**作用与语义：**

压缩`data`字节数组，并将压缩数据返回到新的字节数组中。
`compressionLevel`参数指定应使用多少压缩。有效值在0到9之间，9对应最大压缩（即较小的压缩数据），但代价是使用较慢的算法。较小的值（8、7、...、1）则提供逐渐减少的压缩，速度稍快。值0对应完全不压缩。默认值为-1，表示zlib的默认压缩。

### `QByteArray qCompress(const uchar *data, qsizetype nbytes, int compressionLevel = -1)`

**作用与语义：**

在压缩级别`compressionLevel`压缩`data`的第一个`nbytes`，并将压缩后的数据以新的字节数组形式返回。

### `QByteArray qUncompress(const QByteArray &data)`

**作用与语义：**

解压`data`字节数组，返回一个包含未压缩数据的新字节数组。
如果输入数据损坏，则返回空`QByteArray`。
该功能会将该版本及更早Qt版本中`qCompress()`压缩的数据解压回Qt 3.1版本，当时此功能加入。
注意：如果你想使用此函数来解压用zlib压缩的外部数据，首先需要在包含数据的字节数组前加上一个四字节的头部。头部必须包含未压缩数据的预期长度（以字节计），表示为无符号的大端序32位整数。不过，这个数字只是输出缓冲区初始大小的一个提示。如果指示的大小太小无法容纳结果，输出缓冲区大小仍会增加，直到输出容量符合或系统内存耗尽为止。因此，尽管有32位头部，该函数在64位平台上仍能产生超过4GiB的输出。
注意：在Qt 6.5之前的Qt版本中，超过2GiB的数据运行不可靠;在Qt 6.0之前的Qt版本中，完全不可靠。

### `QByteArray qUncompress(const uchar *data, qsizetype nbytes)`

**作用与语义：**

解压`data`的第一个`nbytes`，返回一个包含未压缩数据的新字节数组。

### `int qstrcmp(const char *str1, const char *str2)`

**作用与语义：**

一个安全的`strcmp()`功能。
比较`str1`和`str2`。如果`str1`小于`str2`，返回负值;如果`str1`等于`str2`，则返回0;如果`str1`大于`str2`，则返回正值。
如果两串都`nullptr`，则视为相等;否则，如果任一串是`nullptr`，则视为小于另一串（即使另一串是空串）。

### `char *qstrcpy(char *dst, const char *src)`

**作用与语义：**

将所有字符（包括 \0）从 `src` 复制到 `dst`，并返回指向 `dst`。如果 `src` `nullptr`，立即返回 `nullptr`。
该函数假设`dst`足够大以容纳`src`的内容。
注意：如果`dst`和`src`重叠，行为未定义。

### `char *qstrdup(const char *src)`

**作用与语义：**

返回一个重复字符串。
为`src`的副本分配空间，复制它，并返回该副本的指针。如果`src` `nullptr`，它会立即返回`nullptr`。
所有权会传给调用者，因此返回的字符串必须通过`delete[]`删除。

### `int qstricmp(const char *str1, const char *str2)`

**作用与语义：**

一个安全的`stricmp()`功能。
比较`str1`和 `str2`，忽略任何 ASCII 字符的差异。
如果`str1`小于`str2`，返回负值;如果`str1`等于`str2`，则返回0;如果`str1`大于`str2`，则返回正值。
如果两串都`nullptr`，则视为相等;否则，如果其中一串`nullptr`，则视为小于另一串（即使另一串是空串）。

### `size_t qstrlen(const char *str)`

**作用与语义：**

一个安全的`strlen()`功能。
返回结尾“\0”之前的字符数，若`str`为`nullptr`则返回0。

### `int qstrncmp(const char *str1, const char *str2, size_t len)`

**作用与语义：**

一个安全的`strncmp()`功能。
比较最多`len`字节的`str1`和 `str2`。
如果`str1`小于`str2`，返回负值;如果`str1`等于`str2`，则返回0;如果`str1`大于`str2`，则返回正值。
如果两个字符串都`nullptr`，则视为相等;否则，如果其中一个`nullptr`，则视为小于另一个（即使另一个是空字符串或`len`为0）。

### `char *qstrncpy(char *dst, const char *src, size_t len)`

**作用与语义：**

一个安全的`strncpy()`功能。
从`src`（停止于`len`或终止的“\0”以先到者为准）最多复制`len`字节到`dst`。保证`dst`是“\0”终止，除非`dst`为`nullptr`或`len`为0。如果`src` `nullptr`，返回`nullptr`，否则返回`dst`。
该函数假设`dst`至少长`len`个字符。
注意：如果`dst`和`src`重叠，行为是未定义的。
注意：与 strncpy() 不同，该函数不会写入 `dst` `len` 字节 '\0'，而是在终止的 '\0' 后停止。从这个意义上说，它类似于 C11 的 strncpy_s()。

### `int qstrnicmp(const char *str1, const char *str2, size_t len)`

**作用与语义：**

一个安全的`strnicmp()`功能。
最多比较`len`字节的`str1`和`str2`，忽略任何ASCII字符的差异。
如果`str1`小于`str2`，返回负值;如果`str1`等于`str2`，则返回0;如果`str1`大于`str2`，则返回正值。
如果两串都`nullptr`，则视为相等;否则，如果其中一串`nullptr`，则视为小于另一串（即使另一串是空串或`len`为0）。

### `size_t qstrnlen(const char *str, size_t maxlen)`

**作用与语义：**

一个安全的`strnlen()`功能。
返回结尾 '\0' 前的字符数，但最多为 `maxlen`。如果 `str` 是`nullptr`，则返回 0。

### `[noexcept] bool operator!=(const QByteArray &lhs, const QByteArray &rhs)`

**作用与语义：**

如果字节数组 `lhs` 不等于字节数组 `rhs`，则返回 `rhs`；否则返回 `false`。

### `[noexcept] bool operator!=(const QByteArray &lhs, const char *const &rhs)`

**作用与语义：**

如果字节数组 `lhs` 不等于以 '\0' 结尾的字符串 `rhs`，则返回 `false`; 否则返回 `false`。

### `[noexcept] bool operator!=(const char *const &lhs, const QByteArray &rhs)`

**作用与语义：**

如果以 '\0' 结尾的字符串 `lhs` 与字节数组 `rhs` 不相等，则返回 `true`；否则返回 `false`。

### `[noexcept, since 6.4] QByteArray operator""_ba(const char *str, size_t size)`

**作用与语义：**

字面操作符，将字符字符串的前`size`字符组成`QByteArray`，字面意义`str`。
`QByteArray`在编译时创建，生成的字符串数据存储在编译对象文件的只读段中。重复的文字可以共享相同的只读内存。该功能与`QByteArrayLiteral`互换，但当代码中存在多个字符串文字时，可以省去打字。
以下代码创建`QByteArray`：

**官方示例：**

```cpp
 using namespace Qt::StringLiterals;

 auto str = "hello"_ba;
```

### `QByteArray operator+(char a1, const QByteArray &a2)`

**作用与语义：**

返回一个字节数组，该数组是通过串接字节`a1`和字节数组`a2`的结果。

### `[since 6.9] QByteArray operator+(QByteArrayView lhs, const QByteArray &rhs)`

**作用与语义：**

返回一个由`lhs`和`rhs`连接的结果字节数组。

### `QByteArray operator+(const QByteArray &a1, char a2)`

**作用与语义：**

返回一个由`lhs`和`rhs`连接的结果字节数组。

### `QByteArray operator+(const QByteArray &a1, const QByteArray &a2)`

**作用与语义：**

返回一个字节数组，该数组是将字节数组`a1`和字节`a2`串接的结果。

### `QByteArray operator+(const QByteArray &a1, const char *a2)`

**作用与语义：**

返回一个字节数组，该数组是将字节数组`a1`和字节数组 `a2` 连接的结果。

### `QByteArray operator+(const char *a1, const QByteArray &a2)`

**作用与语义：**

返回一个字节数组，该数组是串接字节数组`a1`和“\0”终止字符串`a2`的结果。

### `[noexcept] bool operator<(const QByteArray &lhs, const QByteArray &rhs)`

**作用与语义：**

如果字节数组`lhs`词汇小于字节数组`rhs`，返回`true`;否则返回`false`。

### `[noexcept] bool operator<(const QByteArray &lhs, const char *const &rhs)`

**作用与语义：**

如果字节数组 `lhs` 在词法上小于以 '\0' 结尾的字符串 `rhs`，则返回 `true`；否则返回 `false`。

### `[noexcept] bool operator<(const char *const &lhs, const QByteArray &rhs)`

**作用与语义：**

如果以 '\0' 结尾的字符串 `lhs` 在字节数组 `rhs` 的字典序中小于，则返回 `true`；否则返回 `false`。

### `QDataStream &operator<<(QDataStream &out, const QByteArray &ba)`

**作用与语义：**

将字节数组 `ba` 写入流`out`并返回流的引用。

### `[noexcept] bool operator<=(const QByteArray &lhs, const QByteArray &rhs)`

**作用与语义：**

如果字节数组`lhs`词汇大小于或等于字节数组`rhs`，返回`true`;否则返回`false`。

### `[noexcept] bool operator<=(const QByteArray &lhs, const char *const &rhs)`

**作用与语义：**

如果字节数组`lhs`词法上小于或等于或等于“\0”终止字符串`rhs`，返回`true`;否则返回`false`。

### `[noexcept] bool operator<=(const char *const &lhs, const QByteArray &rhs)`

**作用与语义：**

如果以 '\0' 结尾的字符串 `lhs` 在字节数组 `rhs` 的字典序中小于或等于，则返回 `true`；否则返回 `false`。

### `[noexcept] bool operator==(const QByteArray &lhs, const QByteArray &rhs)`

**作用与语义：**

如果字节数组`lhs`等于字节数组`rhs`，则返回`true`;否则返回`false`。

### `[noexcept] bool operator==(const QByteArray &lhs, const char *const &rhs)`

**作用与语义：**

如果字节数组 `lhs` 等于 '\0' 终止字符串 `rhs`，则返回 `true`;否则返回 `false`。

### `[noexcept] bool operator==(const char *const &lhs, const QByteArray &rhs)`

**作用与语义：**

如果“\0”终止字符串`lhs`等于字节数组`rhs`，返回`true`;否则返回`false`。

### `[noexcept] bool operator>(const QByteArray &lhs, const QByteArray &rhs)`

**作用与语义：**

如果字节数组`lhs`词汇大于字节数组`rhs`，返回`true`;否则返回`false`。

### `[noexcept] bool operator>(const QByteArray &lhs, const char *const &rhs)`

**作用与语义：**

如果字节数组 `lhs` 词法大于 '\0' 终止字符串 `rhs`，返回 `true`;否则返回 `false`。

### `[noexcept] bool operator>(const char *const &lhs, const QByteArray &rhs)`

**作用与语义：**

如果“\0”终止字符串`lhs`词汇大于字节数组`rhs`，返回`true`;否则返回`false`。

### `[noexcept] bool operator>=(const QByteArray &lhs, const QByteArray &rhs)`

**作用与语义：**

如果字节数组`lhs`词汇大于或等于字节数组`rhs`，返回`true`;否则返回`false`。

### `[noexcept] bool operator>=(const QByteArray &lhs, const char *const &rhs)`

**作用与语义：**

如果字节数组`lhs`词汇大于或等于“\0”终止字符串`rhs`，返回`true`;否则返回`false`。

### `[noexcept] bool operator>=(const char *const &lhs, const QByteArray &rhs)`

**作用与语义：**

如果以 '\0' 结尾的字符串 `lhs` 在字节数组 `rhs` 的字典序中大于或等于，则返回 `true`；否则返回 `false`。

### `QDataStream &operator>>(QDataStream &in, QByteArray &ba)`

**作用与语义：**

从流`in`读取一个字节数组到`ba`，并返回流的引用。

### `QByteArrayLiteral(ba)`

**作用与语义：**

宏在编译时从字符串的字面量`ba`生成`QByteArray`数据。在这种情况下，从中创建`QByteArray`是免费的，生成的字节数组数据存储在已编译对象文件的只读段中。
例如：
使用QByteArrayLiteral代替双引号的普通C字符串文字，可以显著加快从编译时已知数据创建`QByteArray`实例的速度。

**官方示例：**

```cpp
 QByteArray ba = QByteArrayLiteral("byte array contents");
```

### `QT_NO_CAST_FROM_BYTEARRAY`

**作用与语义：**

禁用从`QByteArray`自动转换为const char *或const void *。

### `[since 6.8] QT_NO_QSNPRINTF`

**作用与语义：**

定义这个宏会移除 qsnprintf() 和 qvsnprintf() 函数的可用性。请参阅函数文档，了解为什么你可能想禁用它们。
该宏在Qt 6.8中引入。

### `class FromBase64Result`

**作用与语义：**

QByteArray：：FromBase64Result 类包含调用 QByteArray：：fromBase64Encoding 的结果。
此类对象可用于检查转换是否成功，若成功，则检索解码后的`QByteArray`。为`QByteArray::FromBase64Result`定义的转换算符使其使用简单明了：
或者，也可以直接访问转换状态和解码数据：

**官方示例：**

```cpp
 void process(const QByteArray &);

 if (auto result = QByteArray::fromBase64Encoding(encodedData))
     process(*result);
```

### `enum Base64Option { Base64Encoding, Base64UrlEncoding, KeepTrailingEquals, OmitTrailingEquals, IgnoreBase64DecodingErrors, AbortOnBase64DecodingErrors }`

**作用与语义：**

该枚举包含可用于编码和解码Base64的选项。Base64由RFC 4648定义，具有以下选项：
- `QByteArray::Base64Encoding`：`0`;（默认）常规的Base64字母表，简称为“base64”
- `QByteArray::Base64UrlEncoding`：`1`;一种替代字母表，称为“base64url”，它替换字母表中的两个字符，以更友好于网址。
- `QByteArray::KeepTrailingEquals`：`0`;（默认）保持编码数据末尾的填充等号，使数据始终是四的倍数。
- `QByteArray::OmitTrailingEquals`：`2`;省略在编码数据末尾添加填充等号。
- `QByteArray::IgnoreBase64DecodingErrors`：`0`;解码Base64编码数据时，忽略输入中的错误;无效字符被简单跳过。该枚举值在Qt 5.15中加入。
- `QByteArray::AbortOnBase64DecodingErrors`：`4`;解码Base64编码数据时，停止于第一次译码误差。该枚举值在Qt 5.15中加入。
`QByteArray::fromBase64Encoding()` 和 `QByteArray::fromBase64()` 忽略 KeepTrailingEquals 和 OmitTrailingEquals 选项。如果指定了 IgnoreBase64DecodingErrors 选项，它们不会在缺少等号尾部或数量过多时标记错误。如果指定了 AbortOnBase64DecodingErrors，那么输入必须没有填充或等号数量正确。
Base64Options 类型是 QFlag 的 typedef<Base64Option>。它存储 Base64Option 值的 OR 组合。

### `flags Base64Options`

**作用与语义：**

该枚举包含可用于编码和解码Base64的选项。Base64由RFC 4648定义，具有以下选项：
- `QByteArray::Base64Encoding`：`0`;（默认）常规的Base64字母表，简称为“base64”
- `QByteArray::Base64UrlEncoding`：`1`;一种替代字母表，称为“base64url”，它替换字母表中的两个字符，以更友好于网址。
- `QByteArray::KeepTrailingEquals`：`0`;（默认）保持编码数据末尾的填充等号，使数据始终是四的倍数。
- `QByteArray::OmitTrailingEquals`：`2`;省略在编码数据末尾添加填充等号。
- `QByteArray::IgnoreBase64DecodingErrors`：`0`;解码Base64编码数据时，忽略输入中的错误;无效字符被简单跳过。该枚举值在Qt 5.15中加入。
- `QByteArray::AbortOnBase64DecodingErrors`：`4`;解码Base64编码数据时，停止于第一次译码误差。该枚举值在Qt 5.15中加入。
`QByteArray::fromBase64Encoding()` 和 `QByteArray::fromBase64()` 忽略 KeepTrailingEquals 和 OmitTrailingEquals 选项。如果指定了 IgnoreBase64DecodingErrors 选项，它们不会在缺少等号尾部或数量过多时标记错误。如果指定了 AbortOnBase64DecodingErrors，那么输入必须没有填充或等号数量正确。
Base64Options 类型是 QFlag 的 typedef<Base64Option>。它存储 Base64Option 值的 OR 组合。

### `const_iterator`

**作用与语义：**

该typedef为`QByteArray`提供了一个STL风格的const迭代器。

### `const_reverse_iterator`

**作用与语义：**

该typedef为`QByteArray`提供了一个STL风格的const反迭代器。

### `iterator`

**作用与语义：**

该typedef为`QByteArray`提供了一个STL风格的非const迭代器。

### `reverse_iterator`

**作用与语义：**

该typedef为`QByteArray`提供了一个STL风格的非const反迭代器。

### `QByteArray chopped(qsizetype len) const &`

**作用与语义：**

返回一个字节数组，包含该字节数组最左侧`size()` - `len`字节。
注意：行为未定义`len`是否为负或大于`size()`。

### `(since 6.0) QByteArray first(qsizetype n) const &`

**作用与语义：**

返回字节数组的前`n`字节。
注意：当`n` <0或`n` > `size()`时，行为未定义。

**官方示例：**

```cpp
 QByteArray x("Pineapple");
 QByteArray y = x.first(4);
 // y == "Pine"
```

### `(since 6.0) QByteArray last(qsizetype n) const &`

**作用与语义：**

返回字节数组的最后`n`字节。
注意：当`n` <0或`n` > `size()`时，行为未定义。

**官方示例：**

```cpp
 QByteArray x("Pineapple");
 QByteArray y = x.last(5);
 // y == "apple"
```

### `QByteArray left(qsizetype len) const &`

**作用与语义：**

返回一个包含该字节数组前`len`字节的字节数组。
如果你知道`len`不能越界，就在新代码中使用`first()`，因为它更快。
如果 `len` 大于 `size()`，则返回整个字节数组。
如果`len`小于0，返回空`QByteArray`。

### `(since 6.8) qsizetype max_size() const`

**作用与语义：**

它返回字节数组理论上能容纳的最大元素数。实际上，这个数量可以更小，受限于系统可用的内存容量。

### `QByteArray mid(qsizetype pos, qsizetype len = -1) const &`

**作用与语义：**

返回一个包含该字节数组 `len` 字节的字节数组，从位置 `pos` 开始。
如果你知道`pos`和`len`不能越界，那就在新代码中使用`sliced()`，因为这样更快。
如果 `len` 为 -1（默认值）或 `pos` `len` >= `size()`，则返回一个字节数组，包含从位置 `pos` 开始直到字节数组末尾的所有字节。

### `(since 6.10) QByteArray nullTerminated() const &`

**作用与语义：**

返回该字节数组的副本，且始终为空终止。参见 `nullTerminate()`。

### `QByteArray right(qsizetype len) const &`

**作用与语义：**

返回一个字节数组，包含该字节数组的最后`len`字节。
如果你知道`len`不能越界，就用新代码中的`last()`，因为这样更快。
如果 `len` 大于 `size()`，整个字节数组将返回。
如果`len`小于0，则返回空`QByteArray`。

### `(since 6.0) QByteArray sliced(qsizetype pos, qsizetype n) const &`

**作用与语义：**

返回一个字节数组，包含从该对象位置`pos`开始并延伸到该对象末端的字节。
注意：当`pos` <0或`pos` > `size()`时，行为未定义。

### `(since 6.0) QByteArray sliced(qsizetype pos) const &`

**作用与语义：**

返回一个字节数组，包含从该对象位置`pos`开始并延伸到该对象末端的字节。
注意：当`pos` <0或`pos` > `size()`时，行为未定义。

### `operator const char *() const`

**作用与语义：**

注意：新代码中请使用`constData()`。
返回存储在字节数组中的数据指针。该指针可用于访问组成数组的字节。数据为“\0”终止。
只要不发生分离且`QByteArray`未被修改，指针依然有效。
该运算符主要用于将字节数组传递给接受`const char *`的函数。
你可以通过在编译应用程序时定义`QT_NO_CAST_FROM_BYTEARRAY`来禁用这个操作符。
注意：`QByteArray`可以存储包括“\0”在内的任何字节值，但大多数`char *`参数的函数假设数据在遇到的第一个“\0”处结束。

### `operator const void *() const`

**作用与语义：**

注意：新代码中请使用`constData()`。
返回存储在字节数组中的数据指针。该指针可用于访问组成数组的字节。数据为“\0”终止。
只要不发生分离且`QByteArray`未被修改，指针依然有效。
该运算符主要用于将字节数组传递给接受`const char *`的函数。
你可以通过在编译应用程序时定义`QT_NO_CAST_FROM_BYTEARRAY`来禁用这个操作符。
注意：`QByteArray`可以存储包括“\0”在内的任何字节值，但大多数`char *`参数的函数假设数据在遇到的第一个“\0”处结束。

### `QByteArray::FromBase64Result fromBase64Encoding(QByteArray &&base64, QByteArray::Base64Options options = Base64Encoding)`

**作用与语义：**

解码 Base64 数组`base64`，使用`options`定义的选项。如果`options`包含 `IgnoreBase64DecodingErrors`（默认），则不检查输入有效性;输入中的无效字符会被跳过，使解码过程能够继续后续字符。如果 包含 `options` `AbortOnBase64DecodingErrors`，则解码将在第一个无效字符处停止。
用于解码 Base64 编码数据的算法在 RFC 4648 中定义。
返回一个 QByteArrayFromBase64Result 对象，包含解码数据和一个标志，说明解码是否成功。如果`AbortOnBase64DecodingErrors`选项被传递且输入数据无效，则未说明解码数据包含什么。

**官方示例：**

```cpp
 void process(const QByteArray &);

 if (auto result = QByteArray::fromBase64Encoding(encodedData))
     process(*result);
```

### `(since 6.9) QByteArray operator+(const QByteArray &lhs, QByteArrayView rhs)`

**作用与语义：**

返回一个字节数组，该数组是将“\0”终止字符串`a1`和字节数组 `a2` 串接而成。

## 6. 深入实践与常见坑

### 生命周期和资源边界

值对象由作用域、容器或调用者管理，不使用 parent 和 deleteLater。跨线程传递副本通常比传递 QObject 安全，但共享数据在写入时仍可能发生复制，性能和内存峰值要结合数据规模判断。

### 状态和错误边界

重点区分空值、无效值、默认值和已初始化值。例如空字符串、空 URL、null 图像和无效索引不一定表示同一件事；转换函数的失败结果要通过对应的状态查询确认。

### 线程边界

值类型本身通常可以复制后跨线程传递；不要把 data()/bits()/constData() 得到的指针当成跨线程长期有效的所有权。大对象频繁写入会触发 detach，应避免不必要的复制和格式转换。

### 最容易出现的错误

不要把空值当成业务成功；不要保存临时对象的内部指针；不要把 QString 当二进制缓冲区；不要假定隐式共享让并发写入自动安全。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QByteArray` 所属机制类型：Qt 值类型与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
