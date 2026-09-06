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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 259 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QByteArray::Base64Optionflags QByteArray::Base64Options`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QByteArray` 暴露的类型声明 `Base、64、Optionflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Base64Optionflags QByteArray::Base64Options`。
- 属性名：`QByteArray`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray::const_iterator`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QByteArray` 的配置属性。初始化或状态切换时通过 `setConst_iterator(...)` 设置，之后用 `const_iterator()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:const_iterator`。
- 属性名：`QByteArray`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray::const_reverse_iterator`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QByteArray` 的配置属性。初始化或状态切换时通过 `setConst_reverse_iterator(...)` 设置，之后用 `const_reverse_iterator()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:const_reverse_iterator`。
- 属性名：`QByteArray`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray::iterator`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QByteArray` 的配置属性。初始化或状态切换时通过 `setIterator(...)` 设置，之后用 `iterator()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:iterator`。
- 属性名：`QByteArray`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray::reverse_iterator`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QByteArray` 的配置属性。初始化或状态切换时通过 `setReverse_iterator(...)` 设置，之后用 `reverse_iterator()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:reverse_iterator`。
- 属性名：`QByteArray`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] QByteArray::QByteArray()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QByteArray` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit, since 6.8] QByteArray::QByteArray(QByteArrayView v)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QByteArray` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `v`：类型为 `QByteArrayView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray::QByteArray(const char *data, qsizetype size = -1)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QByteArray` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `data`：类型为 `const char *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `size`：类型为 `qsizetype`。默认值为 `-1`。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray::QByteArray(qsizetype size, Qt::Initialization)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QByteArray` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `size`：类型为 `qsizetype`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。
- 参数 `Initialization`：类型为 `Qt::`。没有默认值，调用时必须提供。传入 `Qt::` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray::QByteArray(qsizetype size, char ch)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QByteArray` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `size`：类型为 `qsizetype`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。
- 参数 `ch`：类型为 `char`。没有默认值，调用时必须提供。传入 `char` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QByteArray::QByteArray(const QByteArray &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QByteArray` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QByteArray::QByteArray(QByteArray &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QByteArray` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `QByteArray &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QByteArray::~QByteArray()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QByteArray` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray &QByteArray::append(const QByteArray &ba)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QByteArray` 添加依赖、数据或子对象的 API `append`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数 `ba`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray &QByteArray::append(QByteArrayView data)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QByteArray` 添加依赖、数据或子对象的 API `append`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数 `data`：类型为 `QByteArrayView`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray &QByteArray::append(char ch)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QByteArray` 添加依赖、数据或子对象的 API `append`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数 `ch`：类型为 `char`。没有默认值，调用时必须提供。传入 `char` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray &QByteArray::append(const char *str)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QByteArray` 添加依赖、数据或子对象的 API `append`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数 `str`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray &QByteArray::append(const char *str, qsizetype len)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QByteArray` 添加依赖、数据或子对象的 API `append`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数 `str`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `len`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray &QByteArray::append(qsizetype count, char ch)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QByteArray` 添加依赖、数据或子对象的 API `append`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数 `count`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `ch`：类型为 `char`。没有默认值，调用时必须提供。传入 `char` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] QByteArray &QByteArray::assign(QByteArrayView v)`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::assign` 用于计算、查询或取得与“assign”相关的操作。调用时要先确认当前状态和 `v` 的有效范围；返回类型是 `QByteArray &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数 `v`：类型为 `QByteArrayView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] template <typename InputIterator, QByteArray::if_input_iterator<InputIterator> = true> QByteArray &QByteArray::assign(InputIterator first, InputIterator last)`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::assign` 用于计算、查询或取得与“assign”相关的操作。调用时要先确认当前状态和 `first`、`last` 的有效范围；返回类型是 `template <typename InputIterator, QByteArray::if_input_iterator<InputIterator> = true> QByteArray &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename InputIterator, QByteArray::if_input_iterator<InputIterator> = true> QByteArray &`。
- 参数 `first`：类型为 `InputIterator`。没有默认值，调用时必须提供。传入 `InputIterator` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `last`：类型为 `InputIterator`。没有默认值，调用时必须提供。传入 `InputIterator` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] QByteArray &QByteArray::assign(qsizetype n, char c)`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::assign` 用于计算、查询或取得与“assign”相关的操作。调用时要先确认当前状态和 `n`、`c` 的有效范围；返回类型是 `QByteArray &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数 `n`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `c`：类型为 `char`。没有默认值，调用时必须提供。传入 `char` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `char QByteArray::at(qsizetype i) const`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `at`，用于取得 `QByteArray` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`char`。
- 参数 `i`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `char &QByteArray::back()`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::back` 用于计算、查询或取得与“末尾”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `char &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`char &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `char QByteArray::back() const`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::back` 用于计算、查询或取得与“末尾”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `char`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`char`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray::iterator QByteArray::begin()`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `begin`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QByteArray::iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QByteArray::const_iterator QByteArray::begin() const`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `begin`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QByteArray::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qsizetype QByteArray::capacity() const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `capacity`，返回 `QByteArray` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QByteArray::const_iterator QByteArray::cbegin() const`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::cbegin` 用于计算、查询或取得与“cbegin”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QByteArray::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QByteArray::const_iterator QByteArray::cend() const`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::cend` 用于计算、查询或取得与“cend”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QByteArray::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QByteArray::chop(qsizetype n)`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::chop` 用于执行与“chop”相关的操作。调用时要先确认当前状态和 `n` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `n`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray QByteArray::chopped(qsizetype len) &&`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::chopped` 用于计算、查询或取得与“chopped”相关的操作。调用时要先确认当前状态和 `len` 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `len`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QByteArray::clear()`

**API 类别：** 成员函数说明

**中文解读：** 这是状态清理或重置 API `clear`。调用后原有数据、索引、缓存或绑定可能失效；使用前先确认它影响的是当前对象、子对象还是底层共享资源，之后重新检查状态。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept, since 6.0] int QByteArray::compare(QByteArrayView bv, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::compare` 用于计算、查询或取得与“比较”相关的操作。调用时要先确认当前状态和 `bv`、`cs` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `bv`：类型为 `QByteArrayView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QByteArray::const_iterator QByteArray::constBegin() const`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::constBegin` 用于计算、查询或取得与“const、起始位置”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QByteArray::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] const char *QByteArray::constData() const`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `constData`，用于取得 `QByteArray` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`const char *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QByteArray::const_iterator QByteArray::constEnd() const`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::constEnd` 用于计算、查询或取得与“const、结束”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QByteArray::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] bool QByteArray::contains(QByteArrayView bv) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `contains`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `bv`：类型为 `QByteArrayView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QByteArray::contains(char ch) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `contains`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `ch`：类型为 `char`。没有默认值，调用时必须提供。传入 `char` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] qsizetype QByteArray::count(QByteArrayView bv) const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `count`，返回 `QByteArray` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数 `bv`：类型为 `QByteArrayView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qsizetype QByteArray::count(char ch) const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `count`，返回 `QByteArray` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数 `ch`：类型为 `char`。没有默认值，调用时必须提供。传入 `char` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QByteArray::const_reverse_iterator QByteArray::crbegin() const`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::crbegin` 用于计算、查询或取得与“crbegin”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QByteArray::const_reverse_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray::const_reverse_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QByteArray::const_reverse_iterator QByteArray::crend() const`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::crend` 用于计算、查询或取得与“crend”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QByteArray::const_reverse_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray::const_reverse_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `char *QByteArray::data()`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `data`，用于取得 `QByteArray` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`char *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] const char *QByteArray::data() const`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `data`，用于取得 `QByteArray` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`const char *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray::iterator QByteArray::end()`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `end`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`QByteArray::iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QByteArray::const_iterator QByteArray::end() const`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `end`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`QByteArray::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] bool QByteArray::endsWith(QByteArrayView bv) const`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `endsWith`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`bool`。
- 参数 `bv`：类型为 `QByteArrayView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QByteArray::endsWith(char ch) const`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `endsWith`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`bool`。
- 参数 `ch`：类型为 `char`。没有默认值，调用时必须提供。传入 `char` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.1] QByteArray::iterator QByteArray::erase(QByteArray::const_iterator first, QByteArray::const_iterator last)`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::erase` 用于计算、查询或取得与“erase”相关的操作。调用时要先确认当前状态和 `first`、`last` 的有效范围；返回类型是 `QByteArray::iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray::iterator`。
- 参数 `first`：类型为 `QByteArray::const_iterator`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `last`：类型为 `QByteArray::const_iterator`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.5] QByteArray::iterator QByteArray::erase(QByteArray::const_iterator it)`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::erase` 用于计算、查询或取得与“erase”相关的操作。调用时要先确认当前状态和 `it` 的有效范围；返回类型是 `QByteArray::iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray::iterator`。
- 参数 `it`：类型为 `QByteArray::const_iterator`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray &QByteArray::fill(char ch, qsizetype size = -1)`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::fill` 用于计算、查询或取得与“fill”相关的操作。调用时要先确认当前状态和 `ch`、`size` 的有效范围；返回类型是 `QByteArray &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数 `ch`：类型为 `char`。没有默认值，调用时必须提供。传入 `char` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `size`：类型为 `qsizetype`。默认值为 `-1`。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] QByteArray QByteArray::first(qsizetype n) &&`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::first` 用于计算、查询或取得与“首项”相关的操作。调用时要先确认当前状态和 `n` 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `n`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QByteArray QByteArray::fromBase64(const QByteArray &base64, QByteArray::Base64Options options = Base64Encoding)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromBase64`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `base64`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `options`：类型为 `QByteArray::Base64Options`。默认值为 `Base64Encoding`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QByteArray::FromBase64Result QByteArray::fromBase64Encoding(const QByteArray &base64, QByteArray::Base64Options options = Base64Encoding)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromBase64Encoding`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QByteArray::FromBase64Result`。
- 参数 `base64`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `options`：类型为 `QByteArray::Base64Options`。默认值为 `Base64Encoding`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QByteArray QByteArray::fromCFData(CFDataRef data)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromCFData`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `data`：类型为 `CFDataRef`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.5] QByteArray QByteArray::fromEcmaUint8Array(emscripten::val uint8array)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromEcmaUint8Array`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `uint8array`：类型为 `emscripten::val`。没有默认值，调用时必须提供。传入 `emscripten::val` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QByteArray QByteArray::fromHex(const QByteArray &hexEncoded)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromHex`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `hexEncoded`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QByteArray QByteArray::fromNSData(const NSData *data)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromNSData`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `data`：类型为 `const NSData *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QByteArray QByteArray::fromPercentEncoding(const QByteArray &input, char percent = '%')`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromPercentEncoding`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `input`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `percent`：类型为 `char`。默认值为 `'%'`。传入 `char` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.11] QByteArray QByteArray::fromPercentEncoding(QByteArray &&input, char percent = '%')`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromPercentEncoding`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `input`：类型为 `QByteArray &&`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `percent`：类型为 `char`。默认值为 `'%'`。传入 `char` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QByteArray QByteArray::fromRawCFData(CFDataRef data)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromRawCFData`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `data`：类型为 `CFDataRef`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QByteArray QByteArray::fromRawData(const char *data, qsizetype size)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromRawData`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `data`：类型为 `const char *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `size`：类型为 `qsizetype`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QByteArray QByteArray::fromRawNSData(const NSData *data)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromRawNSData`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `data`：类型为 `const NSData *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QByteArray QByteArray::fromStdString(const std::string &str)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromStdString`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `str`：类型为 `const std::string &`。没有默认值，调用时必须提供。传入 `const std::string &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `char &QByteArray::front()`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::front` 用于计算、查询或取得与“开头”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `char &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`char &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `char QByteArray::front() const`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::front` 用于计算、查询或取得与“开头”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `char`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`char`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] qsizetype QByteArray::indexOf(QByteArrayView bv, qsizetype from = 0) const`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::indexOf` 用于计算、查询或取得与“索引、Of”相关的操作。调用时要先确认当前状态和 `bv`、`from` 的有效范围；返回类型是 `qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数 `bv`：类型为 `QByteArrayView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `from`：类型为 `qsizetype`。默认值为 `0`。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qsizetype QByteArray::indexOf(char ch, qsizetype from = 0) const`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::indexOf` 用于计算、查询或取得与“索引、Of”相关的操作。调用时要先确认当前状态和 `ch`、`from` 的有效范围；返回类型是 `qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数 `ch`：类型为 `char`。没有默认值，调用时必须提供。传入 `char` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `from`：类型为 `qsizetype`。默认值为 `0`。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] QByteArray &QByteArray::insert(qsizetype i, QByteArrayView data)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QByteArray` 添加依赖、数据或子对象的 API `insert`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数 `i`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `data`：类型为 `QByteArrayView`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray &QByteArray::insert(qsizetype i, const QByteArray &data)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QByteArray` 添加依赖、数据或子对象的 API `insert`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数 `i`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `data`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray &QByteArray::insert(qsizetype i, const char *s)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QByteArray` 添加依赖、数据或子对象的 API `insert`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数 `i`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `s`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray &QByteArray::insert(qsizetype i, char ch)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QByteArray` 添加依赖、数据或子对象的 API `insert`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数 `i`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `ch`：类型为 `char`。没有默认值，调用时必须提供。传入 `char` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray &QByteArray::insert(qsizetype i, const char *data, qsizetype len)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QByteArray` 添加依赖、数据或子对象的 API `insert`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数 `i`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `data`：类型为 `const char *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `len`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray &QByteArray::insert(qsizetype i, qsizetype count, char ch)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QByteArray` 添加依赖、数据或子对象的 API `insert`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数 `i`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `ch`：类型为 `char`。没有默认值，调用时必须提供。传入 `char` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] bool QByteArray::isEmpty() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isEmpty`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QByteArray::isLower() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isLower`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool QByteArray::isNull() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isNull`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QByteArray::isUpper() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isUpper`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept, since 6.3] bool QByteArray::isValidUtf8() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isValidUtf8`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] QByteArray QByteArray::last(qsizetype n) &&`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::last` 用于计算、查询或取得与“末项”相关的操作。调用时要先确认当前状态和 `n` 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `n`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] qsizetype QByteArray::lastIndexOf(QByteArrayView bv, qsizetype from) const`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::lastIndexOf` 用于计算、查询或取得与“末项、索引、Of”相关的操作。调用时要先确认当前状态和 `bv`、`from` 的有效范围；返回类型是 `qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数 `bv`：类型为 `QByteArrayView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `from`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] qsizetype QByteArray::lastIndexOf(QByteArrayView bv) const`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::lastIndexOf` 用于计算、查询或取得与“末项、索引、Of”相关的操作。调用时要先确认当前状态和 `bv` 的有效范围；返回类型是 `qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数 `bv`：类型为 `QByteArrayView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qsizetype QByteArray::lastIndexOf(char ch, qsizetype from = -1) const`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::lastIndexOf` 用于计算、查询或取得与“末项、索引、Of”相关的操作。调用时要先确认当前状态和 `ch`、`from` 的有效范围；返回类型是 `qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数 `ch`：类型为 `char`。没有默认值，调用时必须提供。传入 `char` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `from`：类型为 `qsizetype`。默认值为 `-1`。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray QByteArray::left(qsizetype len) &&`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::left` 用于计算、查询或取得与“左侧”相关的操作。调用时要先确认当前状态和 `len` 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `len`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray QByteArray::leftJustified(qsizetype width, char fill = ' ', bool truncate = false) const`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::leftJustified` 用于计算、查询或取得与“左侧、Justified”相关的操作。调用时要先确认当前状态和 `width`、`fill`、`truncate` 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `width`：类型为 `qsizetype`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `fill`：类型为 `char`。默认值为 `' '`。传入 `char` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `truncate`：类型为 `bool`。默认值为 `false`。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] qsizetype QByteArray::length() const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `length`，返回 `QByteArray` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static constexpr noexcept, since 6.8] qsizetype QByteArray::maxSize()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `maxSize`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray QByteArray::mid(qsizetype pos, qsizetype len = -1) &&`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::mid` 用于计算、查询或取得与“mid”相关的操作。调用时要先确认当前状态和 `pos`、`len` 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `pos`：类型为 `qsizetype`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。
- 参数 `len`：类型为 `qsizetype`。默认值为 `-1`。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.10] QByteArray &QByteArray::nullTerminate()`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::nullTerminate` 用于计算、查询或取得与“null、Terminate”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QByteArray &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.10] QByteArray QByteArray::nullTerminated() &&`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::nullTerminated` 用于计算、查询或取得与“null、Terminated”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QByteArray QByteArray::number(int n, int base = 10)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `number`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `n`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `base`：类型为 `int`。默认值为 `10`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QByteArray QByteArray::number(long n, int base = 10)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `number`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `n`：类型为 `long`。没有默认值，调用时必须提供。传入 `long` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `base`：类型为 `int`。默认值为 `10`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QByteArray QByteArray::number(qlonglong n, int base = 10)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `number`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `n`：类型为 `qlonglong`。没有默认值，调用时必须提供。传入 `qlonglong` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `base`：类型为 `int`。默认值为 `10`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QByteArray QByteArray::number(qulonglong n, int base = 10)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `number`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `n`：类型为 `qulonglong`。没有默认值，调用时必须提供。传入 `qulonglong` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `base`：类型为 `int`。默认值为 `10`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QByteArray QByteArray::number(uint n, int base = 10)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `number`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `n`：类型为 `uint`。没有默认值，调用时必须提供。传入 `uint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `base`：类型为 `int`。默认值为 `10`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QByteArray QByteArray::number(ulong n, int base = 10)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `number`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `n`：类型为 `ulong`。没有默认值，调用时必须提供。传入 `ulong` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `base`：类型为 `int`。默认值为 `10`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QByteArray QByteArray::number(double n, char format = 'g', int precision = 6)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `number`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `n`：类型为 `double`。没有默认值，调用时必须提供。传入 `double` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `format`：类型为 `char`。默认值为 `'g'`。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `precision`：类型为 `int`。默认值为 `6`。精度或舍入策略；它可能影响数值转换和数据库结果，不能只按显示位数理解。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.4] QByteArray QByteArray::percentDecoded(char percent = '%') const &`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::percentDecoded` 用于计算、查询或取得与“percent、Decoded”相关的操作。调用时要先确认当前状态和 `percent` 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `percent`：类型为 `char`。默认值为 `'%'`。传入 `char` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.11] QByteArray QByteArray::percentDecoded(char percent = '%') &&`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::percentDecoded` 用于计算、查询或取得与“percent、Decoded”相关的操作。调用时要先确认当前状态和 `percent` 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `percent`：类型为 `char`。默认值为 `'%'`。传入 `char` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray &QByteArray::prepend(QByteArrayView ba)`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::prepend` 用于计算、查询或取得与“前置追加”相关的操作。调用时要先确认当前状态和 `ba` 的有效范围；返回类型是 `QByteArray &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数 `ba`：类型为 `QByteArrayView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray &QByteArray::prepend(char ch)`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::prepend` 用于计算、查询或取得与“前置追加”相关的操作。调用时要先确认当前状态和 `ch` 的有效范围；返回类型是 `QByteArray &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数 `ch`：类型为 `char`。没有默认值，调用时必须提供。传入 `char` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray &QByteArray::prepend(const QByteArray &ba)`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::prepend` 用于计算、查询或取得与“前置追加”相关的操作。调用时要先确认当前状态和 `ba` 的有效范围；返回类型是 `QByteArray &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数 `ba`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray &QByteArray::prepend(const char *str)`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::prepend` 用于计算、查询或取得与“前置追加”相关的操作。调用时要先确认当前状态和 `str` 的有效范围；返回类型是 `QByteArray &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数 `str`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray &QByteArray::prepend(const char *str, qsizetype len)`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::prepend` 用于计算、查询或取得与“前置追加”相关的操作。调用时要先确认当前状态和 `str`、`len` 的有效范围；返回类型是 `QByteArray &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数 `str`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `len`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray &QByteArray::prepend(qsizetype count, char ch)`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::prepend` 用于计算、查询或取得与“前置追加”相关的操作。调用时要先确认当前状态和 `count`、`ch` 的有效范围；返回类型是 `QByteArray &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数 `count`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `ch`：类型为 `char`。没有默认值，调用时必须提供。传入 `char` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QByteArray::push_back(const QByteArray &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QByteArray` 添加依赖、数据或子对象的 API `push_back`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `other`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] void QByteArray::push_back(QByteArrayView str)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QByteArray` 添加依赖、数据或子对象的 API `push_back`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `str`：类型为 `QByteArrayView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QByteArray::push_back(char ch)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QByteArray` 添加依赖、数据或子对象的 API `push_back`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `ch`：类型为 `char`。没有默认值，调用时必须提供。传入 `char` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QByteArray::push_back(const char *str)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QByteArray` 添加依赖、数据或子对象的 API `push_back`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `str`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QByteArray::push_front(const QByteArray &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QByteArray` 添加依赖、数据或子对象的 API `push_front`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `other`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] void QByteArray::push_front(QByteArrayView str)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QByteArray` 添加依赖、数据或子对象的 API `push_front`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `str`：类型为 `QByteArrayView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QByteArray::push_front(char ch)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QByteArray` 添加依赖、数据或子对象的 API `push_front`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `ch`：类型为 `char`。没有默认值，调用时必须提供。传入 `char` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QByteArray::push_front(const char *str)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QByteArray` 添加依赖、数据或子对象的 API `push_front`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `str`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray::reverse_iterator QByteArray::rbegin()`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::rbegin` 用于计算、查询或取得与“rbegin”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QByteArray::reverse_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray::reverse_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QByteArray::const_reverse_iterator QByteArray::rbegin() const`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::rbegin` 用于计算、查询或取得与“rbegin”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QByteArray::const_reverse_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray::const_reverse_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray &QByteArray::remove(qsizetype pos, qsizetype len)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `remove`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数 `pos`：类型为 `qsizetype`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。
- 参数 `len`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.5] QByteArray &QByteArray::removeAt(qsizetype pos)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeAt`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数 `pos`：类型为 `qsizetype`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.5] QByteArray &QByteArray::removeFirst()`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeFirst`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.1] template <typename Predicate> QByteArray &QByteArray::removeIf(Predicate pred)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeIf`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`template <typename Predicate> QByteArray &`。
- 参数 `pred`：类型为 `Predicate`。没有默认值，调用时必须提供。传入 `Predicate` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.5] QByteArray &QByteArray::removeLast()`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeLast`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray::reverse_iterator QByteArray::rend()`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::rend` 用于计算、查询或取得与“rend”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QByteArray::reverse_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray::reverse_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QByteArray::const_reverse_iterator QByteArray::rend() const`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::rend` 用于计算、查询或取得与“rend”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QByteArray::const_reverse_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray::const_reverse_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray QByteArray::repeated(qsizetype times) const`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::repeated` 用于计算、查询或取得与“repeated”相关的操作。调用时要先确认当前状态和 `times` 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `times`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray &QByteArray::replace(qsizetype pos, qsizetype len, QByteArrayView after)`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::replace` 用于计算、查询或取得与“替换”相关的操作。调用时要先确认当前状态和 `pos`、`len`、`after` 的有效范围；返回类型是 `QByteArray &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数 `pos`：类型为 `qsizetype`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。
- 参数 `len`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `after`：类型为 `QByteArrayView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] QByteArray &QByteArray::replace(QByteArrayView before, QByteArrayView after)`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::replace` 用于计算、查询或取得与“替换”相关的操作。调用时要先确认当前状态和 `before`、`after` 的有效范围；返回类型是 `QByteArray &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数 `before`：类型为 `QByteArrayView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `after`：类型为 `QByteArrayView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray &QByteArray::replace(char before, QByteArrayView after)`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::replace` 用于计算、查询或取得与“替换”相关的操作。调用时要先确认当前状态和 `before`、`after` 的有效范围；返回类型是 `QByteArray &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数 `before`：类型为 `char`。没有默认值，调用时必须提供。传入 `char` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `after`：类型为 `QByteArrayView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray &QByteArray::replace(char before, char after)`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::replace` 用于计算、查询或取得与“替换”相关的操作。调用时要先确认当前状态和 `before`、`after` 的有效范围；返回类型是 `QByteArray &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数 `before`：类型为 `char`。没有默认值，调用时必须提供。传入 `char` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `after`：类型为 `char`。没有默认值，调用时必须提供。传入 `char` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray &QByteArray::replace(const char *before, qsizetype bsize, const char *after, qsizetype asize)`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::replace` 用于计算、查询或取得与“替换”相关的操作。调用时要先确认当前状态和 `before`、`bsize`、`after`、`asize` 的有效范围；返回类型是 `QByteArray &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数 `before`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `bsize`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `after`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `asize`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray &QByteArray::replace(qsizetype pos, qsizetype len, const char *after, qsizetype alen)`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::replace` 用于计算、查询或取得与“替换”相关的操作。调用时要先确认当前状态和 `pos`、`len`、`after`、`alen` 的有效范围；返回类型是 `QByteArray &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数 `pos`：类型为 `qsizetype`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。
- 参数 `len`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `after`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `alen`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QByteArray::reserve(qsizetype size)`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::reserve` 用于执行与“reserve”相关的操作。调用时要先确认当前状态和 `size` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `size`：类型为 `qsizetype`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QByteArray::resize(qsizetype size)`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::resize` 用于执行与“调整尺寸”相关的操作。调用时要先确认当前状态和 `size` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `size`：类型为 `qsizetype`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.4] void QByteArray::resize(qsizetype newSize, char c)`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::resize` 用于执行与“调整尺寸”相关的操作。调用时要先确认当前状态和 `newSize`、`c` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `newSize`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `c`：类型为 `char`。没有默认值，调用时必须提供。传入 `char` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.8] void QByteArray::resizeForOverwrite(qsizetype size)`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::resizeForOverwrite` 用于执行与“调整尺寸、For、Overwrite”相关的操作。调用时要先确认当前状态和 `size` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `size`：类型为 `qsizetype`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray QByteArray::right(qsizetype len) &&`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::right` 用于计算、查询或取得与“右侧”相关的操作。调用时要先确认当前状态和 `len` 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `len`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray QByteArray::rightJustified(qsizetype width, char fill = ' ', bool truncate = false) const`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::rightJustified` 用于计算、查询或取得与“右侧、Justified”相关的操作。调用时要先确认当前状态和 `width`、`fill`、`truncate` 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `width`：类型为 `qsizetype`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `fill`：类型为 `char`。默认值为 `' '`。传入 `char` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `truncate`：类型为 `bool`。默认值为 `false`。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray &QByteArray::setNum(int n, int base = 10)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setNum`。调用它会改变 `QByteArray` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数 `n`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `base`：类型为 `int`。默认值为 `10`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray &QByteArray::setNum(long n, int base = 10)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setNum`。调用它会改变 `QByteArray` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数 `n`：类型为 `long`。没有默认值，调用时必须提供。传入 `long` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `base`：类型为 `int`。默认值为 `10`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray &QByteArray::setNum(qlonglong n, int base = 10)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setNum`。调用它会改变 `QByteArray` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数 `n`：类型为 `qlonglong`。没有默认值，调用时必须提供。传入 `qlonglong` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `base`：类型为 `int`。默认值为 `10`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray &QByteArray::setNum(qulonglong n, int base = 10)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setNum`。调用它会改变 `QByteArray` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数 `n`：类型为 `qulonglong`。没有默认值，调用时必须提供。传入 `qulonglong` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `base`：类型为 `int`。默认值为 `10`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray &QByteArray::setNum(short n, int base = 10)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setNum`。调用它会改变 `QByteArray` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数 `n`：类型为 `short`。没有默认值，调用时必须提供。传入 `short` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `base`：类型为 `int`。默认值为 `10`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray &QByteArray::setNum(uint n, int base = 10)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setNum`。调用它会改变 `QByteArray` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数 `n`：类型为 `uint`。没有默认值，调用时必须提供。传入 `uint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `base`：类型为 `int`。默认值为 `10`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray &QByteArray::setNum(ulong n, int base = 10)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setNum`。调用它会改变 `QByteArray` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数 `n`：类型为 `ulong`。没有默认值，调用时必须提供。传入 `ulong` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `base`：类型为 `int`。默认值为 `10`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray &QByteArray::setNum(ushort n, int base = 10)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setNum`。调用它会改变 `QByteArray` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数 `n`：类型为 `ushort`。没有默认值，调用时必须提供。传入 `ushort` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `base`：类型为 `int`。默认值为 `10`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray &QByteArray::setNum(double n, char format = 'g', int precision = 6)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setNum`。调用它会改变 `QByteArray` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数 `n`：类型为 `double`。没有默认值，调用时必须提供。传入 `double` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `format`：类型为 `char`。默认值为 `'g'`。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `precision`：类型为 `int`。默认值为 `6`。精度或舍入策略；它可能影响数值转换和数据库结果，不能只按显示位数理解。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray &QByteArray::setNum(float n, char format = 'g', int precision = 6)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setNum`。调用它会改变 `QByteArray` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数 `n`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `format`：类型为 `char`。默认值为 `'g'`。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `precision`：类型为 `int`。默认值为 `6`。精度或舍入策略；它可能影响数值转换和数据库结果，不能只按显示位数理解。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray &QByteArray::setRawData(const char *data, qsizetype size)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setRawData`。调用它会改变 `QByteArray` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数 `data`：类型为 `const char *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `size`：类型为 `qsizetype`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QByteArray::shrink_to_fit()`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::shrink_to_fit` 用于执行与“shrink、转换输出、fit”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray QByteArray::simplified() const`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::simplified` 用于计算、查询或取得与“simplified”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] qsizetype QByteArray::size() const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `size`，返回 `QByteArray` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.8] QByteArray &QByteArray::slice(qsizetype pos, qsizetype n)`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::slice` 用于计算、查询或取得与“slice”相关的操作。调用时要先确认当前状态和 `pos`、`n` 的有效范围；返回类型是 `QByteArray &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数 `pos`：类型为 `qsizetype`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。
- 参数 `n`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.8] QByteArray &QByteArray::slice(qsizetype pos)`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::slice` 用于计算、查询或取得与“slice”相关的操作。调用时要先确认当前状态和 `pos` 的有效范围；返回类型是 `QByteArray &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数 `pos`：类型为 `qsizetype`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] QByteArray QByteArray::sliced(qsizetype pos, qsizetype n) &&`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::sliced` 用于计算、查询或取得与“sliced”相关的操作。调用时要先确认当前状态和 `pos`、`n` 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `pos`：类型为 `qsizetype`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。
- 参数 `n`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] QByteArray QByteArray::sliced(qsizetype pos) &&`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::sliced` 用于计算、查询或取得与“sliced”相关的操作。调用时要先确认当前状态和 `pos` 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `pos`：类型为 `qsizetype`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QByteArray> QByteArray::split(char sep) const`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::split` 用于计算、查询或取得与“split”相关的操作。调用时要先确认当前状态和 `sep` 的有效范围；返回类型是 `QList<QByteArray>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QByteArray>`。
- 参数 `sep`：类型为 `char`。没有默认值，调用时必须提供。传入 `char` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QByteArray::squeeze()`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::squeeze` 用于执行与“squeeze”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] bool QByteArray::startsWith(QByteArrayView bv) const`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `startsWith`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`bool`。
- 参数 `bv`：类型为 `QByteArrayView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QByteArray::startsWith(char ch) const`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `startsWith`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`bool`。
- 参数 `ch`：类型为 `char`。没有默认值，调用时必须提供。传入 `char` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] void QByteArray::swap(QByteArray &other)`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::swap` 用于执行与“swap”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `other`：类型为 `QByteArray &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray QByteArray::toBase64(QByteArray::Base64Options options = Base64Encoding) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toBase64`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `options`：类型为 `QByteArray::Base64Options`。默认值为 `Base64Encoding`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `CFDataRef QByteArray::toCFData() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toCFData`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`CFDataRef`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `double QByteArray::toDouble(bool *ok = nullptr) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toDouble`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`double`。
- 参数 `ok`：类型为 `bool *`。默认值为 `nullptr`。传入 `bool *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.5] emscripten::val QByteArray::toEcmaUint8Array()`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toEcmaUint8Array`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`emscripten::val`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `float QByteArray::toFloat(bool *ok = nullptr) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toFloat`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`float`。
- 参数 `ok`：类型为 `bool *`。默认值为 `nullptr`。传入 `bool *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray QByteArray::toHex(char separator = '\0') const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toHex`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `separator`：类型为 `char`。默认值为 `'\0'`。传入 `char` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QByteArray::toInt(bool *ok = nullptr, int base = 10) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toInt`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`int`。
- 参数 `ok`：类型为 `bool *`。默认值为 `nullptr`。传入 `bool *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `base`：类型为 `int`。默认值为 `10`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `long QByteArray::toLong(bool *ok = nullptr, int base = 10) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toLong`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`long`。
- 参数 `ok`：类型为 `bool *`。默认值为 `nullptr`。传入 `bool *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `base`：类型为 `int`。默认值为 `10`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qlonglong QByteArray::toLongLong(bool *ok = nullptr, int base = 10) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toLongLong`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`qlonglong`。
- 参数 `ok`：类型为 `bool *`。默认值为 `nullptr`。传入 `bool *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `base`：类型为 `int`。默认值为 `10`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray QByteArray::toLower() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toLower`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `NSData *QByteArray::toNSData() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toNSData`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`NSData *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray QByteArray::toPercentEncoding(const QByteArray &exclude = QByteArray(), const QByteArray &include = QByteArray(), char percent = '%') const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toPercentEncoding`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `exclude`：类型为 `const QByteArray &`。默认值为 `QByteArray()`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `include`：类型为 `const QByteArray &`。默认值为 `QByteArray()`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `percent`：类型为 `char`。默认值为 `'%'`。传入 `char` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `CFDataRef QByteArray::toRawCFData() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toRawCFData`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`CFDataRef`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `NSData *QByteArray::toRawNSData() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toRawNSData`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`NSData *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `short QByteArray::toShort(bool *ok = nullptr, int base = 10) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toShort`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`short`。
- 参数 `ok`：类型为 `bool *`。默认值为 `nullptr`。传入 `bool *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `base`：类型为 `int`。默认值为 `10`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `std::string QByteArray::toStdString() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toStdString`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`std::string`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `uint QByteArray::toUInt(bool *ok = nullptr, int base = 10) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toUInt`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`uint`。
- 参数 `ok`：类型为 `bool *`。默认值为 `nullptr`。传入 `bool *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `base`：类型为 `int`。默认值为 `10`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `ulong QByteArray::toULong(bool *ok = nullptr, int base = 10) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toULong`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`ulong`。
- 参数 `ok`：类型为 `bool *`。默认值为 `nullptr`。传入 `bool *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `base`：类型为 `int`。默认值为 `10`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qulonglong QByteArray::toULongLong(bool *ok = nullptr, int base = 10) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toULongLong`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`qulonglong`。
- 参数 `ok`：类型为 `bool *`。默认值为 `nullptr`。传入 `bool *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `base`：类型为 `int`。默认值为 `10`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `ushort QByteArray::toUShort(bool *ok = nullptr, int base = 10) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toUShort`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`ushort`。
- 参数 `ok`：类型为 `bool *`。默认值为 `nullptr`。传入 `bool *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `base`：类型为 `int`。默认值为 `10`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray QByteArray::toUpper() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toUpper`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray QByteArray::trimmed() const`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::trimmed` 用于计算、查询或取得与“trimmed”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QByteArray::truncate(qsizetype pos)`

**API 类别：** 成员函数说明

**中文解读：** `QByteArray::truncate` 用于执行与“truncate”相关的操作。调用时要先确认当前状态和 `pos` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `pos`：类型为 `qsizetype`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray::operator const void *() const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QByteArray` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept, since 6.10] QByteArray::operator std::string_view() const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QByteArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`由运算符声明决定`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray &QByteArray::operator+=(const QByteArray &ba)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QByteArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数 `ba`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray &QByteArray::operator+=(char ch)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QByteArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数 `ch`：类型为 `char`。没有默认值，调用时必须提供。传入 `char` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray &QByteArray::operator+=(const char *str)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QByteArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数 `str`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QByteArray &QByteArray::operator=(QByteArray &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QByteArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数 `other`：类型为 `QByteArray &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QByteArray &QByteArray::operator=(const QByteArray &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QByteArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数 `other`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray &QByteArray::operator=(const char *str)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QByteArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QByteArray &`。
- 参数 `str`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `char &QByteArray::operator[](qsizetype i)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QByteArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`char &`。
- 参数 `i`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `char QByteArray::operator[](qsizetype i) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QByteArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`char`。
- 参数 `i`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.1] template <typename T> qsizetype erase(QByteArray &ba, const T &t)`

**API 类别：** 相关非成员函数

**中文解读：** `QByteArray::erase` 用于计算、查询或取得与“erase”相关的操作。调用时要先确认当前状态和 `ba`、`t` 的有效范围；返回类型是 `template <typename T> qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename T> qsizetype`。
- 参数 `ba`：类型为 `QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `t`：类型为 `const T &`。没有默认值，调用时必须提供。传入 `const T &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.1] template <typename Predicate> qsizetype erase_if(QByteArray &ba, Predicate pred)`

**API 类别：** 相关非成员函数

**中文解读：** `QByteArray::erase_if` 用于计算、查询或取得与“erase、if”相关的操作。调用时要先确认当前状态和 `ba`、`pred` 的有效范围；返回类型是 `template <typename Predicate> qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename Predicate> qsizetype`。
- 参数 `ba`：类型为 `QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `pred`：类型为 `Predicate`。没有默认值，调用时必须提供。传入 `Predicate` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `quint16 qChecksum(QByteArrayView data, Qt::ChecksumType standard = Qt::ChecksumIso3309)`

**API 类别：** 相关非成员函数

**中文解读：** `QByteArray::qChecksum` 用于计算、查询或取得与“q、Checksum”相关的操作。调用时要先确认当前状态和 `data`、`standard` 的有效范围；返回类型是 `quint16`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`quint16`。
- 参数 `data`：类型为 `QByteArrayView`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `standard`：类型为 `Qt::ChecksumType`。默认值为 `Qt::ChecksumIso3309`。传入 `Qt::ChecksumType` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray qCompress(const QByteArray &data, int compressionLevel = -1)`

**API 类别：** 相关非成员函数

**中文解读：** `QByteArray::qCompress` 用于计算、查询或取得与“q、Compress”相关的操作。调用时要先确认当前状态和 `data`、`compressionLevel` 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `data`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `compressionLevel`：类型为 `int`。默认值为 `-1`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray qCompress(const uchar *data, qsizetype nbytes, int compressionLevel = -1)`

**API 类别：** 相关非成员函数

**中文解读：** `QByteArray::qCompress` 用于计算、查询或取得与“q、Compress”相关的操作。调用时要先确认当前状态和 `data`、`nbytes`、`compressionLevel` 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `data`：类型为 `const uchar *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `nbytes`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `compressionLevel`：类型为 `int`。默认值为 `-1`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray qUncompress(const QByteArray &data)`

**API 类别：** 相关非成员函数

**中文解读：** `QByteArray::qUncompress` 用于计算、查询或取得与“q、Uncompress”相关的操作。调用时要先确认当前状态和 `data` 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `data`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray qUncompress(const uchar *data, qsizetype nbytes)`

**API 类别：** 相关非成员函数

**中文解读：** `QByteArray::qUncompress` 用于计算、查询或取得与“q、Uncompress”相关的操作。调用时要先确认当前状态和 `data`、`nbytes` 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `data`：类型为 `const uchar *`。没有默认值，调用时必须提供。数据载荷或要读取的数据。要确认编码、所有权、大小和是否允许为空。
- 参数 `nbytes`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int qstrcmp(const char *str1, const char *str2)`

**API 类别：** 相关非成员函数

**中文解读：** `QByteArray::qstrcmp` 用于计算、查询或取得与“qstrcmp”相关的操作。调用时要先确认当前状态和 `str1`、`str2` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `str1`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `str2`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `char *qstrcpy(char *dst, const char *src)`

**API 类别：** 相关非成员函数

**中文解读：** `QByteArray::qstrcpy` 用于计算、查询或取得与“qstrcpy”相关的操作。调用时要先确认当前状态和 `dst`、`src` 的有效范围；返回类型是 `char *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`char *`。
- 参数 `dst`：类型为 `char *`。没有默认值，调用时必须提供。传入 `char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `src`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `char *qstrdup(const char *src)`

**API 类别：** 相关非成员函数

**中文解读：** `QByteArray::qstrdup` 用于计算、查询或取得与“qstrdup”相关的操作。调用时要先确认当前状态和 `src` 的有效范围；返回类型是 `char *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`char *`。
- 参数 `src`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int qstricmp(const char *str1, const char *str2)`

**API 类别：** 相关非成员函数

**中文解读：** `QByteArray::qstricmp` 用于计算、查询或取得与“qstricmp”相关的操作。调用时要先确认当前状态和 `str1`、`str2` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `str1`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `str2`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `size_t qstrlen(const char *str)`

**API 类别：** 相关非成员函数

**中文解读：** `QByteArray::qstrlen` 用于计算、查询或取得与“qstrlen”相关的操作。调用时要先确认当前状态和 `str` 的有效范围；返回类型是 `size_t`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`size_t`。
- 参数 `str`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int qstrncmp(const char *str1, const char *str2, size_t len)`

**API 类别：** 相关非成员函数

**中文解读：** `QByteArray::qstrncmp` 用于计算、查询或取得与“qstrncmp”相关的操作。调用时要先确认当前状态和 `str1`、`str2`、`len` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `str1`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `str2`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `len`：类型为 `size_t`。没有默认值，调用时必须提供。传入 `size_t` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `char *qstrncpy(char *dst, const char *src, size_t len)`

**API 类别：** 相关非成员函数

**中文解读：** `QByteArray::qstrncpy` 用于计算、查询或取得与“qstrncpy”相关的操作。调用时要先确认当前状态和 `dst`、`src`、`len` 的有效范围；返回类型是 `char *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`char *`。
- 参数 `dst`：类型为 `char *`。没有默认值，调用时必须提供。传入 `char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `src`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `len`：类型为 `size_t`。没有默认值，调用时必须提供。传入 `size_t` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int qstrnicmp(const char *str1, const char *str2, size_t len)`

**API 类别：** 相关非成员函数

**中文解读：** `QByteArray::qstrnicmp` 用于计算、查询或取得与“qstrnicmp”相关的操作。调用时要先确认当前状态和 `str1`、`str2`、`len` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `str1`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `str2`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `len`：类型为 `size_t`。没有默认值，调用时必须提供。传入 `size_t` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `size_t qstrnlen(const char *str, size_t maxlen)`

**API 类别：** 相关非成员函数

**中文解读：** `QByteArray::qstrnlen` 用于计算、查询或取得与“qstrnlen”相关的操作。调用时要先确认当前状态和 `str`、`maxlen` 的有效范围；返回类型是 `size_t`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`size_t`。
- 参数 `str`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `maxlen`：类型为 `size_t`。没有默认值，调用时必须提供。传入 `size_t` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator!=(const QByteArray &lhs, const QByteArray &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QByteArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator!=(const QByteArray &lhs, const char *const &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QByteArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const char *const &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator!=(const char *const &lhs, const QByteArray &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QByteArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const char *const &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept, since 6.4] QByteArray operator""_ba(const char *str, size_t size)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QByteArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `str`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `size`：类型为 `size_t`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray operator+(char a1, const QByteArray &a2)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QByteArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `a1`：类型为 `char`。没有默认值，调用时必须提供。传入 `char` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `a2`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.9] QByteArray operator+(QByteArrayView lhs, const QByteArray &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QByteArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `lhs`：类型为 `QByteArrayView`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray operator+(const QByteArray &a1, char a2)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QByteArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `a1`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `a2`：类型为 `char`。没有默认值，调用时必须提供。传入 `char` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray operator+(const QByteArray &a1, const QByteArray &a2)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QByteArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `a1`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `a2`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray operator+(const QByteArray &a1, const char *a2)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QByteArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `a1`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `a2`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray operator+(const char *a1, const QByteArray &a2)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QByteArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `a1`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `a2`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator<(const QByteArray &lhs, const QByteArray &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QByteArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator<(const QByteArray &lhs, const char *const &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QByteArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const char *const &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator<(const char *const &lhs, const QByteArray &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QByteArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const char *const &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDataStream &operator<<(QDataStream &out, const QByteArray &ba)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QByteArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDataStream &`。
- 参数 `out`：类型为 `QDataStream &`。没有默认值，调用时必须提供。传入 `QDataStream &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `ba`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator<=(const QByteArray &lhs, const QByteArray &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QByteArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator<=(const QByteArray &lhs, const char *const &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QByteArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const char *const &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator<=(const char *const &lhs, const QByteArray &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QByteArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const char *const &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator==(const QByteArray &lhs, const QByteArray &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QByteArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator==(const QByteArray &lhs, const char *const &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QByteArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const char *const &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator==(const char *const &lhs, const QByteArray &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QByteArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const char *const &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator>(const QByteArray &lhs, const QByteArray &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QByteArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator>(const QByteArray &lhs, const char *const &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QByteArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const char *const &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator>(const char *const &lhs, const QByteArray &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QByteArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const char *const &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator>=(const QByteArray &lhs, const QByteArray &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QByteArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator>=(const QByteArray &lhs, const char *const &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QByteArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const char *const &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator>=(const char *const &lhs, const QByteArray &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QByteArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const char *const &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDataStream &operator>>(QDataStream &in, QByteArray &ba)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QByteArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDataStream &`。
- 参数 `in`：类型为 `QDataStream &`。没有默认值，调用时必须提供。传入 `QDataStream &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `ba`：类型为 `QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArrayLiteral(ba)`

**API 类别：** 宏说明

**中文解读：** `QByteArray::QByteArrayLiteral` 用于执行与“Q、Byte、Array、Literal”相关的操作。调用时要先确认当前状态和 `ba` 的有效范围；返回类型是 `未标注`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`由运算符声明决定`。
- 参数 `ba`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QT_NO_CAST_FROM_BYTEARRAY`

**API 类别：** 宏说明

**中文解读：** 这是 `QByteArray` 的 `BYTEARRAY` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.8] QT_NO_QSNPRINTF`

**API 类别：** 宏说明

**中文解读：** 这是 `QByteArray` 的 `QSNPRINTF` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `class FromBase64Result`

**API 类别：** 公有类型

**中文解读：** 这是 `QByteArray` 暴露的类型声明 `转换进入、Base、64、结果`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum Base64Option { Base64Encoding, Base64UrlEncoding, KeepTrailingEquals, OmitTrailingEquals, IgnoreBase64DecodingErrors, AbortOnBase64DecodingErrors }`

**API 类别：** 公有类型

**中文解读：** 这是 `QByteArray` 暴露的类型声明 `Base、64、Option`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags Base64Options`

**API 类别：** 公有类型

**中文解读：** 这是 `QByteArray` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const_iterator`

**API 类别：** 公有类型

**中文解读：** 这是 `QByteArray` 的 `const、iterator` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const_reverse_iterator`

**API 类别：** 公有类型

**中文解读：** 这是 `QByteArray` 的 `const、reverse、iterator` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `iterator`

**API 类别：** 公有类型

**中文解读：** 这是 `QByteArray` 的 `iterator` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `reverse_iterator`

**API 类别：** 公有类型

**中文解读：** 这是 `QByteArray` 的 `reverse、iterator` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray chopped(qsizetype len) const &`

**API 类别：** 公有函数

**中文解读：** `QByteArray::chopped` 用于计算、查询或取得与“chopped”相关的操作。调用时要先确认当前状态和 `len` 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `len`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.0) QByteArray first(qsizetype n) const &`

**API 类别：** 公有函数

**中文解读：** `QByteArray::first` 用于计算、查询或取得与“首项”相关的操作。调用时要先确认当前状态和 `n` 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `n`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.0) QByteArray last(qsizetype n) const &`

**API 类别：** 公有函数

**中文解读：** `QByteArray::last` 用于计算、查询或取得与“末项”相关的操作。调用时要先确认当前状态和 `n` 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `n`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray left(qsizetype len) const &`

**API 类别：** 公有函数

**中文解读：** `QByteArray::left` 用于计算、查询或取得与“左侧”相关的操作。调用时要先确认当前状态和 `len` 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `len`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.8) qsizetype max_size() const`

**API 类别：** 公有函数

**中文解读：** `QByteArray::max_size` 用于计算、查询或取得与“max、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray mid(qsizetype pos, qsizetype len = -1) const &`

**API 类别：** 公有函数

**中文解读：** `QByteArray::mid` 用于计算、查询或取得与“mid”相关的操作。调用时要先确认当前状态和 `pos`、`len` 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `pos`：类型为 `qsizetype`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。
- 参数 `len`：类型为 `qsizetype`。默认值为 `-1`。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.10) QByteArray nullTerminated() const &`

**API 类别：** 公有函数

**中文解读：** `QByteArray::nullTerminated` 用于计算、查询或取得与“null、Terminated”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray right(qsizetype len) const &`

**API 类别：** 公有函数

**中文解读：** `QByteArray::right` 用于计算、查询或取得与“右侧”相关的操作。调用时要先确认当前状态和 `len` 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `len`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.0) QByteArray sliced(qsizetype pos, qsizetype n) const &`

**API 类别：** 公有函数

**中文解读：** `QByteArray::sliced` 用于计算、查询或取得与“sliced”相关的操作。调用时要先确认当前状态和 `pos`、`n` 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `pos`：类型为 `qsizetype`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。
- 参数 `n`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.0) QByteArray sliced(qsizetype pos) const &`

**API 类别：** 公有函数

**中文解读：** `QByteArray::sliced` 用于计算、查询或取得与“sliced”相关的操作。调用时要先确认当前状态和 `pos` 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `pos`：类型为 `qsizetype`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `operator const char *() const`

**API 类别：** 公有函数

**中文解读：** 这是 `QByteArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `operator const void *() const`

**API 类别：** 公有函数

**中文解读：** 这是 `QByteArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray::FromBase64Result fromBase64Encoding(QByteArray &&base64, QByteArray::Base64Options options = Base64Encoding)`

**API 类别：** 静态公有成员

**中文解读：** 这是静态工具 API `fromBase64Encoding`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QByteArray::FromBase64Result`。
- 参数 `base64`：类型为 `QByteArray &&`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `options`：类型为 `QByteArray::Base64Options`。默认值为 `Base64Encoding`。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.9) QByteArray operator+(const QByteArray &lhs, QByteArrayView rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QByteArray` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数 `lhs`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `QByteArrayView`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

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
