# QString

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QString` 是 Qt 的 Unicode 字符串值类型，负责文本存储、查找、切分、格式化、编码转换和大小写处理。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QString` 是 Qt 的 Unicode 字符串值类型，负责文本存储、查找、切分、格式化、编码转换和大小写处理。

**内部模型：** QString 处理的是文本，不是任意二进制数据；二进制协议优先使用 QByteArray。它使用隐式共享，按值传递通常成本较低，但拿到 data() 指针后仍要注意对象修改和生命周期。

**适用场景：** 界面文本、文件路径、JSON 字段、日志、用户输入和国际化字符串使用 QString；固定英文常量优先 QStringLiteral。

**典型调用链：** 构造或接收文本 -> arg/number/section 等转换 -> contains/indexOf/split 等查询 -> trimmed/normalized 等清理 -> toUtf8/toLocal8Bit 转为字节。

**先记住的坑：** 不要把 QString 当作 UTF-8 字节数组；QStringLiteral 和 fromUtf8/fromLocal8Bit 的语义不同；拼接大量字符串时要考虑 reserve 或 QStringBuilder。

## 2. 依赖与对象关系

- 头文件：`#include <QString>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

QString 处理的是文本，不是任意二进制数据；二进制协议优先使用 QByteArray。它使用隐式共享，按值传递通常成本较低，但拿到 data() 指针后仍要注意对象修改和生命周期。

### 状态、生命周期和线程

**生命周期：** 值对象由作用域、容器或调用者管理，不使用 parent 和 deleteLater。跨线程传递副本通常比传递 QObject 安全，但共享数据在写入时仍可能发生复制，性能和内存峰值要结合数据规模判断。

**状态与结果：** 重点区分空值、无效值、默认值和已初始化值。例如空字符串、空 URL、null 图像和无效索引不一定表示同一件事；转换函数的失败结果要通过对应的状态查询确认。

**线程与事件循环：** 值类型本身通常可以复制后跨线程传递；不要把 data()/bits()/constData() 得到的指针当成跨线程长期有效的所有权。大对象频繁写入会触发 detach，应避免不必要的复制和格式转换。

## 3. 直接使用

界面文本、文件路径、JSON 字段、日志、用户输入和国际化字符串使用 QString；固定英文常量优先 QStringLiteral。 使用时通常按这个过程组织：构造或接收文本 -> arg/number/section 等转换 -> contains/indexOf/split 等查询 -> trimmed/normalized 等清理 -> toUtf8/toLocal8Bit 转为字节。

```cpp
#include <QString>

const QString userName = QStringLiteral("Qt");
const QString message = QStringLiteral("Hello, %1").arg(userName);
const QByteArray utf8 = message.toUtf8();
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `ConstIterator`
- `Iterator`
- `enum NormalizationForm { NormalizationForm_D, NormalizationForm_C, NormalizationForm_KD, NormalizationForm_KC }`
- `enum SectionFlag { SectionDefault, SectionSkipEmpty, SectionIncludeLeadingSep, SectionIncludeTrailingSep, SectionCaseInsensitiveSeps }`
- `flags SectionFlags`
- `const_iterator`
- `const_pointer`
- `const_reference`
- `const_reverse_iterator`
- `difference_type`
- `iterator`
- `pointer`
- `reference`
- `reverse_iterator`
- `size_type`
- `value_type`

### 公有函数

- `QString()`
- `QString(QChar ch)`
- `QString(QLatin1StringView str)`
- `(since 6.8) QString(QStringView sv)`
- `QString(const QByteArray &ba)`
- `QString(const char *str)`
- `(since 6.1) QString(const char8_t *str)`
- `QString(const QChar *unicode, qsizetype size = -1)`
- `QString(qsizetype size, QChar ch)`
- `QString(const QString &other)`
- `QString(QString &&other)`
- `~QString()`
- `QString & append(const QString &str)`
- `QString & append(QChar ch)`
- `QString & append(QLatin1StringView str)`
- `(since 6.0) QString & append(QStringView v)`
- `(since 6.5) QString & append(QUtf8StringView str)`
- `QString & append(const QByteArray &ba)`
- `QString & append(const char *str)`
- `QString & append(const QChar *str, qsizetype len)`
- `QString arg(Args &&... args) const`
- `QString arg(const T &a, int fieldWidth = 0, QChar fillChar = u' ') const`
- `QString arg(T a, int fieldWidth = 0, int base = 10, QChar fillChar = u' ') const`
- `QString arg(T a, int fieldWidth = 0, char format = 'g', int precision = -1, QChar fillChar = u' ') const`
- `(since 6.6) QString & assign(QAnyStringView v)`
- `(since 6.6) QString & assign(InputIterator first, InputIterator last)`
- `(since 6.6) QString & assign(qsizetype n, QChar c)`
- `const QChar at(qsizetype position) const`
- `QChar & back()`
- `QChar back() const`
- `QString::iterator begin()`
- `QString::const_iterator begin() const`
- `qsizetype capacity() const`
- `QString::const_iterator cbegin() const`
- `QString::const_iterator cend() const`
- `void chop(qsizetype n)`
- `QString chopped(qsizetype len) &&`
- `QString chopped(qsizetype len) const &`
- `void clear()`
- `int compare(QChar ch, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `int compare(QLatin1StringView other, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `int compare(QStringView s, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `int compare(const QString &other, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `QString::const_iterator constBegin() const`
- `const QChar * constData() const`
- `QString::const_iterator constEnd() const`
- `bool contains(const QRegularExpression &re, QRegularExpressionMatch *rmatch = nullptr) const`
- `bool contains(const QString &str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `bool contains(QChar ch, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `bool contains(QLatin1StringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `bool contains(QStringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `qsizetype count(const QString &str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `qsizetype count(const QRegularExpression &re) const`
- `qsizetype count(QChar ch, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `(since 6.0) qsizetype count(QStringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `QString::const_reverse_iterator crbegin() const`
- `QString::const_reverse_iterator crend() const`
- `QChar * data()`
- `const QChar * data() const`
- `QString::iterator end()`
- `QString::const_iterator end() const`
- `bool endsWith(const QString &s, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `bool endsWith(QChar c, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `bool endsWith(QLatin1StringView s, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `bool endsWith(QStringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `(since 6.1) QString::iterator erase(QString::const_iterator first, QString::const_iterator last)`
- `(since 6.5) QString::iterator erase(QString::const_iterator it)`
- `QString & fill(QChar ch, qsizetype size = -1)`
- `(since 6.0) QString first(qsizetype n) &&`
- `(since 6.0) QString first(qsizetype n) const &`
- `QChar & front()`
- `QChar front() const`
- `qsizetype indexOf(QLatin1StringView str, qsizetype from = 0, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `qsizetype indexOf(const QRegularExpression &re, qsizetype from = 0, QRegularExpressionMatch *rmatch = nullptr) const`
- `qsizetype indexOf(const QString &str, qsizetype from = 0, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `qsizetype indexOf(QChar ch, qsizetype from = 0, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `qsizetype indexOf(QStringView str, qsizetype from = 0, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `QString & insert(qsizetype position, const QString &str)`
- `QString & insert(qsizetype position, QChar ch)`
- `QString & insert(qsizetype position, QLatin1StringView str)`
- `(since 6.0) QString & insert(qsizetype position, QStringView str)`
- `(since 6.5) QString & insert(qsizetype position, QUtf8StringView str)`
- `QString & insert(qsizetype position, const QByteArray &str)`
- `QString & insert(qsizetype position, const char *str)`
- `QString & insert(qsizetype position, const QChar *unicode, qsizetype size)`
- `bool isEmpty() const`
- `bool isLower() const`
- `bool isNull() const`
- `bool isRightToLeft() const`
- `bool isUpper() const`
- `bool isValidUtf16() const`
- `(since 6.0) QString last(qsizetype n) &&`
- `(since 6.0) QString last(qsizetype n) const &`
- `qsizetype lastIndexOf(const QRegularExpression &re, qsizetype from, QRegularExpressionMatch *rmatch = nullptr) const`
- `qsizetype lastIndexOf(const QString &str, qsizetype from, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `(since 6.3) qsizetype lastIndexOf(QChar ch, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `(since 6.2) qsizetype lastIndexOf(QLatin1StringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `(since 6.2) qsizetype lastIndexOf(QStringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `(since 6.2) qsizetype lastIndexOf(const QRegularExpression &re, QRegularExpressionMatch *rmatch = nullptr) const`
- `(since 6.2) qsizetype lastIndexOf(const QString &str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `qsizetype lastIndexOf(QChar ch, qsizetype from, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `qsizetype lastIndexOf(QLatin1StringView str, qsizetype from, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `qsizetype lastIndexOf(QStringView str, qsizetype from, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `QString left(qsizetype n) &&`
- `QString left(qsizetype n) const &`
- `QString leftJustified(qsizetype width, QChar fill = u' ', bool truncate = false) const`
- `qsizetype length() const`
- `(since 6.0) int localeAwareCompare(QStringView other) const`
- `int localeAwareCompare(const QString &other) const`
- `(since 6.8) qsizetype max_size() const`
- `QString mid(qsizetype position, qsizetype n = -1) &&`
- `QString mid(qsizetype position, qsizetype n = -1) const &`
- `QString normalized(QString::NormalizationForm mode, QChar::UnicodeVersion version = QChar::Unicode_Unassigned) const`
- `(since 6.10) QString & nullTerminate()`
- `(since 6.10) QString nullTerminated() &&`
- `(since 6.10) QString nullTerminated() const &`
- `QString & prepend(const QString &str)`
- `QString & prepend(QChar ch)`
- `QString & prepend(QLatin1StringView str)`
- `(since 6.0) QString & prepend(QStringView str)`
- `(since 6.5) QString & prepend(QUtf8StringView str)`
- `QString & prepend(const QByteArray &ba)`
- `QString & prepend(const char *str)`
- `QString & prepend(const QChar *str, qsizetype len)`
- `void push_back(const QString &other)`
- `void push_back(QChar ch)`
- `void push_front(const QString &other)`
- `void push_front(QChar ch)`
- `QString::reverse_iterator rbegin()`
- `QString::const_reverse_iterator rbegin() const`
- `QString & remove(const QRegularExpression &re)`
- `QString & remove(QChar ch, Qt::CaseSensitivity cs = Qt::CaseSensitive)`
- `QString & remove(const QString &str, Qt::CaseSensitivity cs = Qt::CaseSensitive)`
- `QString & remove(qsizetype position, qsizetype n)`
- `QString & remove(QLatin1StringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive)`
- `(since 6.5) QString & removeAt(qsizetype pos)`
- `(since 6.5) QString & removeFirst()`
- `(since 6.1) QString & removeIf(Predicate pred)`
- `(since 6.5) QString & removeLast()`
- `QString::reverse_iterator rend()`
- `QString::const_reverse_iterator rend() const`
- `QString repeated(qsizetype times) const`
- `QString & replace(qsizetype position, qsizetype n, const QString &after)`
- `QString & replace(const QRegularExpression &re, const QString &after)`
- `QString & replace(QChar before, QChar after, Qt::CaseSensitivity cs = Qt::CaseSensitive)`
- `QString & replace(QChar c, QLatin1StringView after, Qt::CaseSensitivity cs = Qt::CaseSensitive)`
- `QString & replace(QChar ch, const QString &after, Qt::CaseSensitivity cs = Qt::CaseSensitive)`
- `QString & replace(QLatin1StringView before, QLatin1StringView after, Qt::CaseSensitivity cs = Qt::CaseSensitive)`
- `QString & replace(QLatin1StringView before, const QString &after, Qt::CaseSensitivity cs = Qt::CaseSensitive)`
- `QString & replace(const QString &before, QLatin1StringView after, Qt::CaseSensitivity cs = Qt::CaseSensitive)`
- `QString & replace(const QString &before, const QString &after, Qt::CaseSensitivity cs = Qt::CaseSensitive)`
- `QString & replace(qsizetype position, qsizetype n, QChar after)`
- `QString & replace(qsizetype position, qsizetype n, const QChar *after, qsizetype alen)`
- `QString & replace(const QChar *before, qsizetype blen, const QChar *after, qsizetype alen, Qt::CaseSensitivity cs = Qt::CaseSensitive)`
- `void reserve(qsizetype size)`
- `void resize(qsizetype size)`
- `void resize(qsizetype newSize, QChar fillChar)`
- `(since 6.8) void resizeForOverwrite(qsizetype size)`
- `QString right(qsizetype n) &&`
- `QString right(qsizetype n) const &`
- `QString rightJustified(qsizetype width, QChar fill = u' ', bool truncate = false) const`
- `QString section(QChar sep, qsizetype start, qsizetype end = -1, QString::SectionFlags flags = SectionDefault) const`
- `QString section(const QRegularExpression &re, qsizetype start, qsizetype end = -1, QString::SectionFlags flags = SectionDefault) const`
- `QString section(const QString &sep, qsizetype start, qsizetype end = -1, QString::SectionFlags flags = SectionDefault) const`
- `QString & setNum(int n, int base = 10)`
- `QString & setNum(long n, int base = 10)`
- `QString & setNum(qlonglong n, int base = 10)`
- `QString & setNum(qulonglong n, int base = 10)`
- `QString & setNum(short n, int base = 10)`
- `QString & setNum(uint n, int base = 10)`
- `QString & setNum(ulong n, int base = 10)`
- `QString & setNum(ushort n, int base = 10)`
- `QString & setNum(double n, char format = 'g', int precision = 6)`
- `QString & setNum(float n, char format = 'g', int precision = 6)`
- `QString & setRawData(const QChar *unicode, qsizetype size)`
- `QString & setUnicode(const QChar *unicode, qsizetype size)`
- `(since 6.9) QString & setUnicode(const char16_t *unicode, qsizetype size)`
- `(since 6.9) QString & setUtf16(const char16_t *unicode, qsizetype size)`
- `void shrink_to_fit()`
- `QString simplified() const`
- `qsizetype size() const`
- `(since 6.8) QString & slice(qsizetype pos, qsizetype n)`
- `(since 6.8) QString & slice(qsizetype pos)`
- `(since 6.0) QString sliced(qsizetype pos, qsizetype n) &&`
- `(since 6.0) QString sliced(qsizetype pos, qsizetype n) const &`
- `(since 6.0) QString sliced(qsizetype pos) &&`
- `(since 6.0) QString sliced(qsizetype pos) const &`
- `QStringList split(const QString &sep, Qt::SplitBehavior behavior = Qt::KeepEmptyParts, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `QStringList split(const QRegularExpression &re, Qt::SplitBehavior behavior = Qt::KeepEmptyParts) const`
- `QStringList split(QChar sep, Qt::SplitBehavior behavior = Qt::KeepEmptyParts, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `void squeeze()`
- `bool startsWith(const QString &s, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `bool startsWith(QChar c, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `bool startsWith(QLatin1StringView s, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `bool startsWith(QStringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`
- `void swap(QString &other)`
- `CFStringRef toCFString() const`
- `QString toCaseFolded() const`
- `double toDouble(bool *ok = nullptr) const`
- `(since 6.6) emscripten::val toEcmaString() const`
- `float toFloat(bool *ok = nullptr) const`
- `QString toHtmlEscaped() const`
- `int toInt(bool *ok = nullptr, int base = 10) const`
- `QByteArray toLatin1() const`
- `QByteArray toLocal8Bit() const`
- `long toLong(bool *ok = nullptr, int base = 10) const`
- `qlonglong toLongLong(bool *ok = nullptr, int base = 10) const`
- `QString toLower() const`
- `NSString * toNSString() const`
- `short toShort(bool *ok = nullptr, int base = 10) const`
- `std::string toStdString() const`
- `std::u16string toStdU16String() const`
- `std::u32string toStdU32String() const`
- `std::wstring toStdWString() const`
- `uint toUInt(bool *ok = nullptr, int base = 10) const`
- `ulong toULong(bool *ok = nullptr, int base = 10) const`
- `qulonglong toULongLong(bool *ok = nullptr, int base = 10) const`
- `ushort toUShort(bool *ok = nullptr, int base = 10) const`
- `QList<uint> toUcs4() const`
- `QString toUpper() const`
- `QByteArray toUtf8() const`
- `qsizetype toWCharArray(wchar_t *array) const`
- `(since 6.0) auto tokenize(Needle &&sep, Flags... flags) &&`
- `(since 6.0) auto tokenize(Needle &&sep, Flags... flags) const &&`
- `(since 6.0) auto tokenize(Needle &&sep, Flags... flags) const &`
- `QString trimmed() const`
- `void truncate(qsizetype position)`
- `const QChar * unicode() const`
- `const ushort * utf16() const`
- `(since 6.7) operator std::u16string_view() const`
- `QString & operator+=(const QString &other)`
- `QString & operator+=(QChar ch)`
- `QString & operator+=(QLatin1StringView str)`
- `(since 6.0) QString & operator+=(QStringView str)`
- `(since 6.5) QString & operator+=(QUtf8StringView str)`
- `QString & operator+=(const QByteArray &ba)`
- `QString & operator+=(const char *str)`
- `QString & operator=(QString &&other)`
- `QString & operator=(const QString &other)`
- `QString & operator=(QChar ch)`
- `QString & operator=(QLatin1StringView str)`
- `QString & operator=(const QByteArray &ba)`
- `QString & operator=(const char *str)`
- `QChar & operator[](qsizetype position)`
- `const QChar operator[](qsizetype position) const`

### 静态公有成员

- `QString asprintf(const char *cformat, ...)`
- `int compare(const QString &s1, const QString &s2, Qt::CaseSensitivity cs = Qt::CaseSensitive)`
- `int compare(QLatin1StringView s1, const QString &s2, Qt::CaseSensitivity cs = Qt::CaseSensitive)`
- `int compare(QStringView s1, const QString &s2, Qt::CaseSensitivity cs = Qt::CaseSensitive)`
- `int compare(const QString &s1, QLatin1StringView s2, Qt::CaseSensitivity cs = Qt::CaseSensitive)`
- `int compare(const QString &s1, QStringView s2, Qt::CaseSensitivity cs = Qt::CaseSensitive)`
- `QString fromCFString(CFStringRef string)`
- `(since 6.6) QString fromEcmaString(emscripten::val jsString)`
- `QString fromLatin1(const char *str, qsizetype size)`
- `(since 6.0) QString fromLatin1(QByteArrayView str)`
- `QString fromLatin1(const QByteArray &str)`
- `QString fromLocal8Bit(const char *str, qsizetype size)`
- `(since 6.0) QString fromLocal8Bit(QByteArrayView str)`
- `QString fromLocal8Bit(const QByteArray &str)`
- `QString fromNSString(const NSString *string)`
- `(since 6.10) QString fromRawData(const char16_t *unicode, qsizetype size)`
- `QString fromRawData(const QChar *unicode, qsizetype size)`
- `QString fromStdString(const std::string &str)`
- `QString fromStdU16String(const std::u16string &str)`
- `QString fromStdU32String(const std::u32string &str)`
- `QString fromStdWString(const std::wstring &str)`
- `QString fromUcs4(const char32_t *unicode, qsizetype size = -1)`
- `QString fromUtf8(const char *str, qsizetype size)`
- `(since 6.0) QString fromUtf8(QByteArrayView str)`
- `QString fromUtf8(const QByteArray &str)`
- `(since 6.1) QString fromUtf8(const char8_t *str)`
- `(since 6.0) QString fromUtf8(const char8_t *str, qsizetype size)`
- `QString fromUtf16(const char16_t *unicode, qsizetype size = -1)`
- `QString fromWCharArray(const wchar_t *string, qsizetype size = -1)`
- `int localeAwareCompare(const QString &s1, const QString &s2)`
- `(since 6.0) int localeAwareCompare(QStringView s1, QStringView s2)`
- `(since 6.8) qsizetype maxSize()`
- `QString number(long n, int base = 10)`
- `QString number(double n, char format = 'g', int precision = 6)`
- `QString number(int n, int base = 10)`
- `QString number(qlonglong n, int base = 10)`
- `QString number(qulonglong n, int base = 10)`
- `QString number(uint n, int base = 10)`
- `QString number(ulong n, int base = 10)`
- `QString vasprintf(const char *cformat, va_list ap)`

### 相关非成员函数

- `(since 6.1) qsizetype erase(QString &s, const T &t)`
- `(since 6.1) qsizetype erase_if(QString &s, Predicate pred)`
- `bool operator!=(const QByteArray &lhs, const QString &rhs)`
- `bool operator!=(const QString &lhs, const QString &rhs)`
- `bool operator!=(const char *const &lhs, const QString &rhs)`
- `bool operator!=(const QString &lhs, const QByteArray &rhs)`
- `bool operator!=(const QString &lhs, const QLatin1StringView &rhs)`
- `bool operator!=(const QString &lhs, const char *const &rhs)`
- `(since 6.4) QString operator""_s(const char16_t *str, size_t size)`
- `QString operator+(QString &&s1, const QString &s2)`
- `(since 6.9) QString operator+(QStringView lhs, const QString &rhs)`
- `(since 6.9) QString operator+(const QString &lhs, QStringView rhs)`
- `QString operator+(const QString &s1, const QString &s2)`
- `QString operator+(const QString &s1, const char *s2)`
- `QString operator+(const char *s1, const QString &s2)`
- `bool operator<(const QByteArray &lhs, const QString &rhs)`
- `bool operator<(const char *const &lhs, const QString &rhs)`
- `bool operator<(const QLatin1StringView &lhs, const QString &rhs)`
- `bool operator<(const QString &lhs, const QByteArray &rhs)`
- `bool operator<(const QString &lhs, const QLatin1StringView &rhs)`
- `bool operator<(const QString &lhs, const QString &rhs)`
- `bool operator<(const QString &lhs, const char *const &rhs)`
- `QDataStream & operator<<(QDataStream &stream, const QString &string)`
- `bool operator<=(const QByteArray &lhs, const QString &rhs)`
- `bool operator<=(const QString &lhs, const QString &rhs)`
- `bool operator<=(const char *const &lhs, const QString &rhs)`
- `bool operator<=(const QLatin1StringView &lhs, const QString &rhs)`
- `bool operator<=(const QString &lhs, const QByteArray &rhs)`
- `bool operator<=(const QString &lhs, const QLatin1StringView &rhs)`
- `bool operator<=(const QString &lhs, const char *const &rhs)`
- `bool operator==(const QByteArray &lhs, const QString &rhs)`
- `bool operator==(const QLatin1StringView &lhs, const QString &rhs)`
- `bool operator==(const QString &lhs, const QByteArray &rhs)`
- `bool operator==(const QString &lhs, const QLatin1StringView &rhs)`
- `bool operator==(const QString &lhs, const QString &rhs)`
- `bool operator==(const QString &lhs, const char *const &rhs)`
- `bool operator==(const char *const &lhs, const QString &rhs)`
- `bool operator>(const QByteArray &lhs, const QString &rhs)`
- `bool operator>(const QString &lhs, const QString &rhs)`
- `bool operator>(const char *const &lhs, const QString &rhs)`
- `bool operator>(const QLatin1StringView &lhs, const QString &rhs)`
- `bool operator>(const QString &lhs, const QByteArray &rhs)`
- `bool operator>(const QString &lhs, const QLatin1StringView &rhs)`
- `bool operator>(const QString &lhs, const char *const &rhs)`
- `bool operator>=(const QByteArray &lhs, const QString &rhs)`
- `bool operator>=(const QString &lhs, const QString &rhs)`
- `bool operator>=(const char *const &lhs, const QString &rhs)`
- `bool operator>=(const QLatin1StringView &lhs, const QString &rhs)`
- `bool operator>=(const QString &lhs, const QByteArray &rhs)`
- `bool operator>=(const QString &lhs, const QLatin1StringView &rhs)`
- `bool operator>=(const QString &lhs, const char *const &rhs)`
- `QDataStream & operator>>(QDataStream &stream, QString &string)`

### 公开宏

- `QStringLiteral(str)`
- `QT_NO_CAST_FROM_ASCII`
- `QT_NO_CAST_TO_ASCII`
- `QT_RESTRICTED_CAST_FROM_ASCII`
- `const char * qPrintable(const QString &str)`
- `const wchar_t * qUtf16Printable(const QString &str)`
- `const char * qUtf8Printable(const QString &str)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QString::ConstIterator`

**作用与语义：**

Qt风格的同义词`QString::const_iterator`。

### `QString::Iterator`

**作用与语义：**

Qt风格的`QString::iterator`同义词。

### `enum QString::NormalizationForm`

**作用与语义：**

此枚举描述了 Unicode 文本的各种规范化形式。
- `QString::NormalizationForm_D`: `0`; 规范分解
- `QString::NormalizationForm_C`: `1`; 规范分解后进行规范组合
- `QString::NormalizationForm_KD`: `2`; 兼容分解
- `QString::NormalizationForm_KC`: `3`; 兼容分解后进行规范组合

### `enum QString::SectionFlagflags QString::SectionFlags`

**作用与语义：**

该枚举指定了可用于影响`section()`函数在分离符和空字段行为方面各方面的标志。
- `QString::SectionDefault`：`0x00`;空字段被计数，不包括前置和后置分隔符，并对分隔符进行大小写敏感比较。
- `QString::SectionSkipEmpty`：`0x01`;将空字段视为不存在，即在起点和结束时不考虑空字段。
- `QString::SectionIncludeLeadingSep`：`0x02`;在结果字符串中包含前置分隔符（如有）。
- `QString::SectionIncludeTrailingSep`：`0x04`;在结果字符串中包含尾部分隔符（如有）。
- `QString::SectionCaseInsensitiveSeps`：`0x08`;对分隔符进行不敏感的比较。
SectionFlags 类型是 QFlags 的 typedef<SectionFlag>。它存储 SectionFlag 值的 OR 组合。

### `QString::const_iterator`

**作用与语义：**

只读的 STL 风格正向迭代器类型，用于从 `begin()`/`cbegin()` 遍历到 `end()`/`cend()`，不能通过它修改元素。

### `QString::const_pointer`

**作用与语义：**

QString：：const_pointer typedef 提供了一个 STL 风格的 cont 指针，指向一个`QString`元素（`QChar`）。

### `QString::const_reverse_iterator`

**作用与语义：**

只读的 STL 风格反向迭代器类型，用于从 `rbegin()`/`crbegin()` 反向遍历到 `rend()`/`crend()`。

### `QString::iterator`

**作用与语义：**

可修改元素的 STL 风格正向迭代器类型；容器发生分离或结构性修改后，已有迭代器可能失效。

### `QString::pointer`

**作用与语义：**

QString：:p ointer typedef 提供一个 STL 风格的指针指向一个`QString`元素（`QChar`）。

### `QString::reverse_iterator`

**作用与语义：**

可修改元素的 STL 风格反向迭代器类型；容器发生分离或结构性修改后，已有迭代器可能失效。

### `[constexpr noexcept] QString::QString()`

**作用与语义：**

构造一个空字符串。空字符串也被视为空的。

### `QString::QString(QChar ch)`

**作用与语义：**

构建一个大小为1的字符串，包含字符 `ch`。

### `QString::QString(QLatin1StringView str)`

**作用与语义：**

构造 `str` 所见的 Latin-1 字符串的副本。

### `[explicit, since 6.8] QString::QString(QStringView sv)`

**作用与语义：**

构建一个用字符串视图数据初始化的字符串。
QString 是空的当且仅当 `sv` 是空的。

### `QString::QString(const QByteArray &ba)`

**作用与语义：**

构造一个以字节数组初始化的字符串`ba`。给定的字节数组通过`fromUtf8()`转换为Unicode。
你可以通过在编译应用时定义`QT_NO_CAST_FROM_ASCII`来禁用这个构造函数。例如，如果你想确保所有用户可见的字符串都经过`QObject::tr()`，这非常有用。
注意：字节数组中任何空（\0）字节都会包含在该字符串中，并转换为 Unicode 空字符（U 0000）。此行为不同于 Qt 5.x。

### `QString::QString(const char *str)`

**作用与语义：**

构造一个以8位字符串`str`初始化的字符串。给定的cont char指针通过`fromUtf8()`函数转换为Unicode。
你可以通过在编译应用时定义 `QT_NO_CAST_FROM_ASCII` 来禁用这个构造函数。例如，如果你想确保所有用户可见的字符串都经过 `QObject::tr()`，这非常有用。
注意：定义`QT_RESTRICTED_CAST_FROM_ASCII`也会禁用该构造函数，但启用`QString(const char (&ch)[N])`构造器。使用非文字输入、嵌入 NUL 字符或非 7 位字符的输入在此情况下未定义。

### `[since 6.1] QString::QString(const char8_t *str)`

**作用与语义：**

构造一个以 UTF-8 字符串 `str` 初始化的字符串。给定的 cont char8_t 指针通过 `fromUtf8()` 函数转换为 Unicode。

### `[explicit] QString::QString(const QChar *unicode, qsizetype size = -1)`

**作用与语义：**

构造一个字符串，初始化为 `QChar` 数组 `unicode` 的前`size`字符。
如果`unicode`为0，则构造一个空字符串。
如果 `size`为负，`unicode` 被假定指向一个 '\0' 终止数组，其长度通过动态确定。终止的空特征不被视为字符串的一部分。
QString 会对字符串数据进行深度复制。Unicode 数据被原样复制，如果存在字节顺序标记会被保留。

### `QString::QString(qsizetype size, QChar ch)`

**作用与语义：**

构造一个由给定 `size` 组成的字符串，并将每个字符设置为 `ch`。

### `[noexcept] QString::QString(const QString &other)`

**作用与语义：**

构建了一份`other`的副本。
该操作耗时为常数，因为QString是隐式共享的。这使得从函数返回QStriing的速度非常快。如果共享实例被修改，它将被复制（写时复制），这需要线性时间。

### `[noexcept] QString::QString(QString &&other)`

**作用与语义：**

Move-构造一个QString实例，使其指向`other`所指向的同一个对象。

### `[noexcept] QString::~QString()`

**作用与语义：**

会破坏那根弦。

### `QString &QString::append(const QString &str)`

**作用与语义：**

将字符串`str`附加到该字符串的末尾。
这与使用`insert()`函数相同：
append() 函数通常非常快（常数时间），因为 `QString` 在字符串数据末尾预分配额外空间，使数据可以增长而不必每次重新分配整个字符串。

**官方示例：**

```cpp
 QString x = "free";
 QString y = "dom";

 x.append(y);
 // x == "freedom"
```

### `QString &QString::append(QChar ch)`

**作用与语义：**

附加该字符串中的字符`ch`。
注意：该功能会让`QString::append()`重载。

### `QString &QString::append(QLatin1StringView str)`

**作用与语义：**

将`str`查看的拉丁-1字符串附加到该字符串上。
注意：该功能会`QString::append()`重载。

### `[since 6.0] QString &QString::append(QStringView v)`

**作用与语义：**

将给定字符串视图`v`附加到该字符串上并返回结果。
注意：该功能会让`QString::append()`重载。

### `[since 6.5] QString &QString::append(QUtf8StringView str)`

**作用与语义：**

在此字符串后附加 UTF-8 字符串视图`str`。
注意：该功能会让`QString::append()`重载。

### `QString &QString::append(const QByteArray &ba)`

**作用与语义：**

将字节数组`ba`附加到该字符串后。给定的字节数组通过 `fromUtf8()` 函数转换为 Unicode。
你可以通过在编译应用时定义`QT_NO_CAST_FROM_ASCII`来禁用这个功能。例如，如果你想确保所有用户可见的字符串都通过`QObject::tr()`，这会很有用。
注意：该功能会超载`QString::append()`。

### `QString &QString::append(const char *str)`

**作用与语义：**

将`str`字符串附加到该字符串上。给定的cont char指针通过`fromUtf8()`函数转换为Unicode。
你可以在编译应用时定义`QT_NO_CAST_FROM_ASCII`来禁用这个功能。如果你想确保所有用户可见的字符串都经过`QObject::tr()`，这会很有用。
注意：该功能会让`QString::append()`重载。

### `QString &QString::append(const QChar *str, qsizetype len)`

**作用与语义：**

将`QChar`数组`str`中的`len`字符附加到该字符串中。
注意：该功能会超载`QString::append()`。

### `template <typename... Args> QString QString::arg(Args &&... args) const`

**作用与语义：**

用 `args` 中对应的参数替换该字符串中出现的 `%N`。这些参数不是位置论元：`args`中的第一个用最低的`N`替换`%N`（全部），第二个用`args`的`%N`替换为下一个最低的`N`，依此类推。
`Args`可以包含任何隐含转换为`QAnyStringView`的内容。
注意：在6.9之前的Qt版本中，`QAnyStringView`和UTF-8字符串（`QUtf8StringView`、`QByteArray`、`QByteArrayView`、`const char8_t*`等）不支持`args`。

### `template <typename T, QString::if_string_like<T> = true> QString QString::arg(const T &a, int fieldWidth = 0, QChar fillChar = u' ') const`

**作用与语义：**

返回该字符串的副本，最小编号的位标被字符串`a`替换，即`%1`、`%2`、...、`%99`。
`fieldWidth` 指定了 `a` 占用的最小空间。如果 `a` 需要的空间少于 `fieldWidth`，则用字符 `fillChar` 填充到`fieldWidth`。正`fieldWidth`产生右对齐文本。负`fieldWidth`生成左对齐文本。
这个例子展示了我们如何在处理文件列表时创建一个`status`字符串来报告进度：
首先，`arg(i)`取代`%1`。然后`arg(total)`取代`%2`。最后，由`arg(fileName)`取代`%3`。
使用 arg() 而非 `asprintf()` 的一个优点是，如果应用程序字符串被翻译成其他语言，编号位置标记的顺序可能会改变，但每个 arg() 仍然会替换编号最低且未替换的位置标记，无论它出现在哪里。此外，如果位置标记 `%i` 在字符串中出现超过一次，arg() 会替换所有位置标记。
如果没有未替换的位标，则会打印警告信息，结果未定义。位标编号必须在1到99之间。
注意：在 6.9 之前的 Qt 版本中，该函数在 `char`、`QChar`、`QString`、`QStringView` 和 `QLatin1StringView` 时会被超载，在某些情况下，`wchar_t` 和 `char16_t` 参数会被解析为整数超载。在 5.10 之前的 Qt 版本中，该函数缺少 `QStringView` 和 `QLatin1StringView` 的重载。

**官方示例：**

```cpp
 int i;                // current file's number
 int total;            // number of files to process
 QStringView fileName; // current file's name

 QString status = QString("Processing file %1 of %2: %3")
                 .arg(i).arg(total).arg(fileName);
```

### `template <typename T, QString::if_integral_non_char<T> = true> QString QString::arg(T a, int fieldWidth = 0, int base = 10, QChar fillChar = u' ') const`

**作用与语义：**

`a`论元以`base`为底表示，默认为10，且必须介于2到36之间。对于非10的基，`a`被视为无符号整数。
`fieldWidth` 指定了`a`填充并填充字符`fillChar`的最小空间。正值表示右对齐文本;负值表示左对齐文本。
“%”后面可以跟一个“L”，此时序列被本地化的`a`表示替代。转换使用由`QLocale::setDefault()`设定的默认区域。如果未指定默认区域，则使用系统区域。如果`base`不是10，则忽略“L”标志。
注意：在 6.10.1 之前的 Qt 版本中，该函数接受隐式转换为整数类型的参数。该参数现已不再支持，除非（无作用域）枚举，因为它也接受可转换为浮点类型的类型，且当这些类型以整数形式打印时精度会下降。向下兼容的解决方案是将此类类型转换为显示形式与你意图相符的 C 类型（`int`、`float` 等）。
注意：在6.9之前的Qt版本中，该函数在各种积分类型上被重载，有时`char`和`char16_t`参数也被错误接受。
注意：该功能会超载`QString::arg()`。

**官方示例：**

```cpp
 QString str;
 str = QString("Decimal 63 is %1 in hexadecimal")
         .arg(63, 0, 16);
 // str == "Decimal 63 is 3f in hexadecimal"

 QLocale::setDefault(QLocale(QLocale::English, QLocale::UnitedStates));
 str = QString("%1 %L2 %L3")
         .arg(12345)
         .arg(12345)
         .arg(12345, 0, 16);
 // str == "12345 12,345 3039"
```

### `template <typename T, QString::if_floating_point<T> = true> QString QString::arg(T a, int fieldWidth = 0, char format = 'g', int precision = -1, QChar fillChar = u' ') const`

**作用与语义：**

参数`a`按照指定的`format`和`precision`进行格式化。详情请参见浮点格式。
`fieldWidth` 指定了`a`填充字符`fillChar`的最小空间。正值表示右对齐文本;负值表示左对齐文本。
注意：在 6.9 之前的 Qt 版本中，该函数是一个常规函数，取`double`。由于现在是模板函数，它不再接受仅隐式转换为浮点类型的参数。向下兼容的解决方案是将此类类型转换为 C 浮点类型之一。
注意：该功能会`QString::arg()`重载。

**官方示例：**

```cpp
 double d = 12.34;
 QString str = QString("delta: %1").arg(d, 0, 'E', 3);
 // str == "delta: 1.234E+01"
```

### `[static] QString QString::asprintf(const char *cformat, ...)`

**作用与语义：**

安全地从格式字符串`cformat`和任意参数列表构建格式化字符串。
格式字符串支持标准 C 库中 printf() 提供的转换规格、长度修饰符和标志。`cformat` 字符串和 `%s` 参数必须采用 UTF-8 编码。
注意：`%lc`转义序列期望一个类型为`char16_t`的Unicode字符（由`QChar::unicode()`返回），或`ushort`。`%ls`转义序列期望指向一个指向零终端的类型`char16_t`或`ushort`类型Unicode字符数组的指针（由`QString::utf16()`返回）。这与标准C库中的printf()不符，后者定义`%lc`打印wchar_t和打印`%ls` `wchar_t*`，并且在`wchar_t`大小不小于16位的平台上也可能产生编译器警告。
警告：我们不建议在新 Qt 代码中使用 QString：：asprintf()。相反，建议使用 `QTextStream` 或 `arg()`，这两种工具都支持无缝的 Unicode 字符串且类型安全。这里有一个使用 `QTextStream` 的示例：
对于`translations`，尤其是字符串包含多个转义序列时，你应该考虑使用`arg()`函数。这样翻译器可以控制替换顺序。

**官方示例：**

```cpp
 QString result;
 QTextStream(&result) << "pi = " << 3.14;
 // result == "pi = 3.14"
```

### `[since 6.6] QString &QString::assign(QAnyStringView v)`

**作用与语义：**

用 `v` 的副本替换该字符串的内容，并返回对该字符串的引用。
该字符串的大小将等于 `v` 的大小，转换为 UTF-16，就像 `v.toString()` 一样。但与 `QAnyStringView::toString()` 不同的是，该函数只有在估计大小超过该字符串容量或该字符串被共享时才分配内存。

### `[since 6.6] template <typename InputIterator, QString::if_compatible_iterator<InputIterator> = true> QString &QString::assign(InputIterator first, InputIterator last)`

**作用与语义：**

用迭代范围 [`first`， `last`） 中的元素副本替换该字符串的内容，并返回对该字符串的引用。
该字符串的长度等于该区间 [`first`， `last`] 中元素的解码长度，这不必等同于该区间本身的长度，因为该函数会透明地将输入字符集重新编码为 UTF-16。
该函数只有在该区间的元素数量，或者对于非UTF-16编码输入时，生成字符串的最大可能大小超过该字符串的容量，或者该字符串被共享时，才会分配内存。
注意：如果任一参数是*这个或[`first`， `last`）的迭代子，则该行为未定义。
只有当`InputIterator`满足LegacyInputIterator的要求且`InputIterator`的`value_type`是以下字符类型之一时，才参与超载解析：
- `QChar`
- `QLatin1Char`
- `char`
- `unsigned char`
- `signed char`
- `char8_t`
- `char16_t`
- （在Windows等平台，采用16位类型）`wchar_t`
- `char32_t`

### `[since 6.6] QString &QString::assign(qsizetype n, QChar c)`

**作用与语义：**

用`n`份`c`的副本替换该字符串的内容，并返回对该字符串的引用。
这串的大小等于`n`，必须是非负的。
该函数仅在内存超过该字符串容量或该字符串被共享时`n`分配。

### `const QChar QString::at(qsizetype position) const`

**作用与语义：**

返回字符串中给定索引`position`的字符。
`position`必须是字符串中的有效索引位置（即0 <= `position` < `size()`）。

### `QChar &QString::back()`

**作用与语义：**

返回字符串最后一个字符的引用。和`operator[](size() - 1)`一样。
此功能是为了STL兼容性而提供。
警告：调用空字符串的函数构成未定义行为。

### `QChar QString::back() const`

**作用与语义：**

返回字符串中的最后一个字符。和`at(size() - 1)`一样。
此功能是为了STL兼容性而提供。
警告：调用空字符串的函数构成未定义行为。

### `QString::iterator QString::begin()`

**作用与语义：**

返回一个指向字符串第一个字符的STL式迭代器。
警告：返回的迭代器在脱离或`QString`修改时将失效。

### `QString::const_iterator QString::begin() const`

**作用与语义：**

注意：该功能会超载`QString::begin()`。

### `qsizetype QString::capacity() const`

**作用与语义：**

返回字符串中可存储的最大字符数而不强制重新分配。
该函数的唯一目的是提供一种微调`QString`内存使用的方法。一般来说，你很少需要调用这个函数。如果你想知道字符串中有多少字符，可以调用`size()`。
注意：静态分配的字符串即使不是空的，也会导致容量为0。
注意：分配内存块中的空闲空间位置未定义。换句话说，不应假设空闲内存总是位于初始化元素之后。

### `QString::const_iterator QString::cbegin() const`

**作用与语义：**

返回一个const STL风格的迭代器，指向字符串中的第一个字符。
警告：返回的迭代器在分离或`QString`修改时将失效。

### `QString::const_iterator QString::cend() const`

**作用与语义：**

返回一个const STL风格的迭代器，指向字符串中最后一个字符之后。
警告：返回的迭代器在脱离或`QString`修改时会失效。

### `void QString::chop(qsizetype n)`

**作用与语义：**

从字符串末尾移除`n`字符。
如果`n`大于或等于`size()`，则结果为空字符串;若`n`为负，则等同于通过零。
如果你想去除字符串开头的字符，可以用`remove()`。

**官方示例：**

```cpp
 QString str("LOGOUT\r\n");
 str.chop(2);
 // str == "LOGOUT"
```

### `QString QString::chopped(qsizetype len) &&`

**作用与语义：**

返回一个字符串，该字符串包含此字符串的最左边 `size()` - `len` 个字符。
注意：如果 `len` 为负数或大于 `size()`，则行为未定义。

### `void QString::clear()`

**作用与语义：**

清除字符串内容，使其为 null。

### `[static noexcept] int QString::compare(const QString &s1, const QString &s2, Qt::CaseSensitivity cs = Qt::CaseSensitive)`

**作用与语义：**

比较字符串`s1`与字符串`s2`，如果`s1`小于`s2`，返回负整数;如果大于`s2`，返回正整数;相等则返回零。
如果`cs`是`Qt::CaseSensitive`（默认），则比较区分大小写;否则比较不区分大小写。
大小写区分比较仅基于字符的数值Unicode，速度非常快，但并非人类预期。考虑用`localeAwareCompare()`排序用户可见字符串。
注意：该函数将空字符串视为空字符串，详情请参见空字符串与空字符串的区分。

**官方示例：**

```cpp
 int x = QString::compare("aUtO", "AuTo", Qt::CaseInsensitive);  // x == 0
 int y = QString::compare("auto", "Car", Qt::CaseSensitive);     // y > 0
 int z = QString::compare("auto", "Car", Qt::CaseInsensitive);   // z < 0
```

### `[noexcept] int QString::compare(QChar ch, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

使用大小写敏感度设置`cs`，对此与`ch`进行比较。
注意：该功能会让`QString::compare()`重载。

### `[noexcept] int QString::compare(QLatin1StringView other, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

和compare（*this， `other`， `cs`）一样。
注意：该功能会让`QString::compare()`重载。

### `[noexcept] int QString::compare(QStringView s, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

使用大小写敏感度设置`cs`，将此与`s`进行比较。
注意：该功能会让`QString::compare()`重载。

### `[noexcept] int QString::compare(const QString &other, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

在词法上将该字符串与字符串`other`比较，若该字符串小于`other`则返回负整数;若大于`other` 4，返回正整数;相等则返回0。
和compare（*this， `other`， `cs`）一样。
注意：该功能会超载`QString::compare()`。

### `[static noexcept] int QString::compare(QLatin1StringView s1, const QString &s2, Qt::CaseSensitivity cs = Qt::CaseSensitive)`

**作用与语义：**

使用大小写敏感设置`cs`进行`s1`与`s2`比较。
注意：该功能会`QString::compare()`重载。

### `[static noexcept] int QString::compare(QStringView s1, const QString &s2, Qt::CaseSensitivity cs = Qt::CaseSensitive)`

**作用与语义：**

注意：该功能会超载`QString::compare()`。

### `[static noexcept] int QString::compare(const QString &s1, QLatin1StringView s2, Qt::CaseSensitivity cs = Qt::CaseSensitive)`

**作用与语义：**

使用大小写敏感设置`cs`进行`s1`与`s2`比较。
注意：该功能会`QString::compare()`重载。

### `[static noexcept] int QString::compare(const QString &s1, QStringView s2, Qt::CaseSensitivity cs = Qt::CaseSensitive)`

**作用与语义：**

注意：该功能会超载`QString::compare()`。

### `QString::const_iterator QString::constBegin() const`

**作用与语义：**

返回一个const STL风格的迭代器，指向字符串中的第一个字符。
警告：返回的迭代器在分离或`QString`修改时将失效。

### `const QChar *QString::constData() const`

**作用与语义：**

返回存储在`QString`中的数据指针。该指针可用于访问构成字符串的字符。
注意，指针只有在字符串未被修改时才有效。
注意：返回的字符串可能不是“\0”终止的。使用`size()`来确定数组的长度。

### `QString::const_iterator QString::constEnd() const`

**作用与语义：**

返回一个const STL风格的迭代器，指向字符串中最后一个字符之后。
警告：返回的迭代器在脱离或`QString`修改时会失效。

### `bool QString::contains(const QRegularExpression &re, QRegularExpressionMatch *rmatch = nullptr) const`

**作用与语义：**

如果正则表达式`re`匹配，返回`true`;否则返回`false`。
如果匹配成功且`rmatch`未`nullptr`，它还会将匹配结果写入`rmatch`指向的`QRegularExpressionMatch`对象中。

### `bool QString::contains(const QString &str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

如果该字符串包含字符串 `str` 的出现，返回 `true`;否则返回 `false`。
如果`cs`是`Qt::CaseSensitive`（默认），则搜索是区分大小写的;否则搜索是无大小写区分的。

**官方示例：**

```cpp
 QString str = "Peter Pan";
 str.contains("peter", Qt::CaseInsensitive);    // returns true
```

### `bool QString::contains(QChar ch, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

如果该字符串包含字符 `ch`，返回 `true`;否则返回 `false`。
注意：该功能会使`QString::contains()`重载。

### `bool QString::contains(QLatin1StringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

如果该字符串包含拉丁字母1字符串的出现，返回`true` `str`;否则返回`false`。
注意：该功能会超载`QString::contains()`。

### `[noexcept] bool QString::contains(QStringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

如果该字符串包含字符串视图的出现，返回`true` `str`;否则返回`false`。
如果`cs`为`Qt::CaseSensitive`（默认），则搜索区分大小写;否则搜索不区分大小写。
注意：该功能会超载`QString::contains()`。

### `qsizetype QString::count(const QString &str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

返回该字符串在该字符串中出现的（可能重叠的）次数`str`。
如果`cs`是`Qt::CaseSensitive`（默认），则搜索区分大小写;否则搜索不区分大小写。

### `qsizetype QString::count(const QRegularExpression &re) const`

**作用与语义：**

返回正则表达式`re`在字符串中匹配的次数。
出于历史原因，该函数会计数重叠匹配，因此在下面的例子中，“ana”或“ama”有四个实例：
这种行为不同于简单地用 `QRegularExpressionMatchIterator` 遍历字符串中的匹配。
注意：该功能会让`QString::count()`重载。

**官方示例：**

```cpp
 QString str = "banana and panama";
 str.count(QRegularExpression("a[nm]a"));    // returns 4
```

### `qsizetype QString::count(QChar ch, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

返回字符串中字符`ch`的出现次数。
如果`cs`是`Qt::CaseSensitive`（默认），则搜索是区分大小写的;否则搜索是不区分大小写的。
注意：该功能会让`QString::count()`重载。

### `[since 6.0] qsizetype QString::count(QStringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

返回该字符串视图`str`可能重叠的次数。
如果`cs`是`Qt::CaseSensitive`（默认），则搜索是区分大小写的;否则搜索是不区分大小写的。
注意：该功能会超载`QString::count()`。

### `QString::const_reverse_iterator QString::crbegin() const`

**作用与语义：**

返回一个const STL风格的反迭代子，指向字符串中的第一个字符，顺序相反。
警告：返回的迭代器在分离或`QString`修改时会失效。

### `QString::const_reverse_iterator QString::crend() const`

**作用与语义：**

返回一个const STL风格的反向迭代子，指向字符串最后一个字符之后，顺序相反。
警告：返回的迭代器在脱离或`QString`修改时将失效。

### `QChar *QString::data()`

**作用与语义：**

返回存储在`QString`中的数据指针。该指针可用于访问和修改构成字符串的字符。
与`constData()`和`unicode()`不同，返回的数据始终是“\0”终端。
注意，指针只有在字符串未被其他方式修改时才有效。对于只读访问`constData()`，该指针更快，因为它从不导致深度复制。

**官方示例：**

```cpp
 QString str = "Hello world";
 QChar *data = str.data();
 while (!data->isNull()) {
     qDebug() << data->unicode();
     ++data;
 }
```

### `const QChar *QString::data() const`

**作用与语义：**

注意：返回字符串不得为“\0”终止。使用`size()`来确定数组长度。

### `QString::iterator QString::end()`

**作用与语义：**

返回一个STL风格的迭代器，指向字符串中最后一个字符之后。
警告：返回的迭代器在分离或`QString`修改时将失效。

### `QString::const_iterator QString::end() const`

**作用与语义：**

注意：此功能会超载`QString::end()`。

### `bool QString::endsWith(const QString &s, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

如果字符串以`s`结尾，返回`true`;否则返回`false`。
如果`cs`为`Qt::CaseSensitive`（默认），则搜索区分大小写;否则搜索不区分大小写。

**官方示例：**

```cpp
 QString str = "Bananas";
 str.endsWith("anas");         // returns true
 str.endsWith("pple");         // returns false
```

### `bool QString::endsWith(QChar c, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

如果字符串以`c`结尾，返回`true`;否则返回`false`。
注意：该功能会让`QString::endsWith()`重载。

### `bool QString::endsWith(QLatin1StringView s, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

注意：该功能会超载`QString::endsWith()`。

### `[noexcept] bool QString::endsWith(QStringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

如果字符串以字符串视图`str`结尾，返回`true`;否则返回`false`。
如果`cs`是`Qt::CaseSensitive`（默认），则搜索是区分大小写的;否则搜索是不区分大小写的。
注意：该功能会让`QString::endsWith()`重载。

### `[since 6.1] QString::iterator QString::erase(QString::const_iterator first, QString::const_iterator last)`

**作用与语义：**

从字符串中移除半开范围的字符[`first`，`last`）。在最后一个被擦除的字符（即擦除前`last`所指字符）后，立即返回一个迭代器。

### `[since 6.5] QString::iterator QString::erase(QString::const_iterator it)`

**作用与语义：**

从字符串中移除以`it`表示的字符。在擦除字符后立即返回迭代器。

**官方示例：**

```cpp
 QString c = "abcdefg";
 auto it = c.erase(c.cbegin()); // c is now "bcdefg"; "it" points to "b"
```

### `QString &QString::fill(QChar ch, qsizetype size = -1)`

**作用与语义：**

将字符串中的每个字符设置为字符`ch`。如果`size`与默认值-1不同，字符串会提前调整为`size`。

**官方示例：**

```cpp
 QString str = "Berlin";
 str.fill('z');
 // str == "zzzzzz"

 str.fill('A', 2);
 // str == "AA"
```

### `[since 6.0] QString QString::first(qsizetype n) &&`

**作用与语义：**

返回一个字符串，该字符串包含此字符串的前 `n` 个字符（也就是说，从此字符串的开头一直到但不包括索引位置 `n` 处的元素）。
注意：当 `n` < 0 或 `n` > `size()` 时，其行为未定义。

**官方示例：**

```cpp
 QString x = "Pineapple";
 QString y = x.first(4);      // y == "Pine"
```

### `[static] QString QString::fromCFString(CFStringRef string)`

**作用与语义：**

构建包含`string` CFString 副本的新`QString`。
注意：此功能仅适用于macOS和iOS。

### `[static, since 6.6] QString QString::fromEcmaString(emscripten::val jsString)`

**作用与语义：**

将ECMAScript字符串`jsString`转换为`QString`。如果参数不是字符串，行为为未定义。

### `[static] QString QString::fromLatin1(const char *str, qsizetype size)`

**作用与语义：**

返回一个以拉丁1字符串`str`首`size`字符初始化的`QString`。
如果`size` `-1`，则使用`strlen(str)`。

### `[static, since 6.0] QString QString::fromLatin1(QByteArrayView str)`

**作用与语义：**

返回一个以拉丁-1字符串`str`初始化的`QString`。
注意：字节数组中的任何空（'\0'）字节都包含在本字符串中，转换为Unicode的空字符（U 0000）。

### `[static] QString QString::fromLatin1(const QByteArray &str)`

**作用与语义：**

返回一个以拉丁-1字符串`str`初始化的`QString`。
注意：字节数组中任何空（'\0'）字节都包含在本字符串中，转换为Unicode空字符（U 0000）。此行为与Qt 5.x不同。

### `[static] QString QString::fromLocal8Bit(const char *str, qsizetype size)`

**作用与语义：**

返回一个初始化为8位字符串`str`前`size`字符的`QString`。
如果`size` `-1`，则使用`strlen(str)`。
在 Unix 系统上，这相当于 `fromUtf8()`。注意，在 Apple 系统上，该函数不考虑 NSString.defaultCStringEncoding 或 CFStringGetSystemEncoding() 功能，因为这些函数通常返回传统的“Western （Mac OS Roman）”编码，现代苹果操作系统不应使用该编码。在 Windows 上，系统使用的是当前的代码页。

### `[static, since 6.0] QString QString::fromLocal8Bit(QByteArrayView str)`

**作用与语义：**

返回一个以8位字符串`str`初始化的`QString`。
在 Unix 系统上，这相当于 `fromUtf8()`。注意，在 Apple 系统中，该函数不考虑 NSString.defaultCStringEncoding 或 CFStringGetSystemEncoding() 的编码，因为这些函数通常返回遗留的“Western （Mac OS Roman）”编码，现代苹果操作系统不应使用该编码。在 Windows 上，系统当前代码页被使用。
注意：字节数组中的任何空（'\0'）字节都包含在本字符串中，转换为Unicode的空字符（U 0000）。

### `[static] QString QString::fromLocal8Bit(const QByteArray &str)`

**作用与语义：**

返回一个以8位字符串`str`初始化的`QString`。
在Unix系统上，这相当于`fromUtf8()`。注意，在苹果系统上，该函数不考虑NSString.defaultCStringEncoding或CFStringGetSystemEncoding()，因为这些函数通常返回传统的“Western （Mac OS Roman）”编码，现代苹果操作系统不应使用该编码。在Windows上，系统使用当前代码页。
注意：字节数组中任何空（'\0'）字节都包含在本字符串中，转换为Unicode空字符（U 0000）。此行为与Qt 5.x不同。

### `[static] QString QString::fromNSString(const NSString *string)`

**作用与语义：**

构建一个包含`string` NSString 副本的新`QString`。
注意：此功能仅适用于macOS和iOS。

### `[static, since 6.10] QString QString::fromRawData(const char16_t *unicode, qsizetype size)`

**作用与语义：**

构造一个使用数组`unicode`中前`size` Unicode字符的 `QString`。数据不被复制`unicode`。调用者必须能够保证只要`QString`（或其未修改的副本）存在，`unicode`不会被删除或修改。
任何修改`QString`或其副本的尝试都会让它生成数据的深度副本，确保原始数据不会被修改。
以下是我们如何在内存中的原始数据上使用`QRegularExpression`的示例，而无需将数据复制到`QString`：
警告：使用 fromRawData() 创建的字符串不会被 '\0'-终止，除非原始数据在位置 `size` 包含 '\0' 字符。这意味着 `unicode()` 不会返回 '\0' 终止字符串（尽管 `utf16()` 会，但会复制原始数据）。

**官方示例：**

```cpp
 QRegularExpression pattern("\u00A4");
 static const char16_t unicode[] = {
         0x005A, 0x007F, 0x00A4, 0x0060,
         0x1009, 0x0020, 0x0020};

 QString str = QString::fromRawData(unicode, std::size(unicode));
 if (str.contains(pattern)) {
     // ...
 }
```

### `[static] QString QString::fromRawData(const QChar *unicode, qsizetype size)`

**作用与语义：**

构造一个使用数组`unicode`中前`size` Unicode字符的 `QString`。数据不被复制`unicode`。调用者必须能够保证只要`QString`（或其未修改的副本）存在，`unicode`不会被删除或修改。
任何修改`QString`或其副本的尝试都会让它生成数据的深度副本，确保原始数据不会被修改。
以下是我们如何在内存中的原始数据上使用`QRegularExpression`的示例，而无需将数据复制到`QString`：
警告：使用 fromRawData() 创建的字符串不会被 '\0'-终止，除非原始数据在位置 `size` 包含 '\0' 字符。这意味着 `unicode()` 不会返回 '\0' 终止字符串（尽管 `utf16()` 会，但会复制原始数据）。

**官方示例：**

```cpp
 QRegularExpression pattern("\u00A4");
 static const char16_t unicode[] = {
         0x005A, 0x007F, 0x00A4, 0x0060,
         0x1009, 0x0020, 0x0020};

 QString str = QString::fromRawData(unicode, std::size(unicode));
 if (str.contains(pattern)) {
     // ...
 }
```

### `[static] QString QString::fromStdString(const std::string &str)`

**作用与语义：**

返回`str`字符串的副本。假设给定字符串编码为UTF-8，并通过`fromUtf8()`函数转换为`QString`。

### `[static] QString QString::fromStdU16String(const std::u16string &str)`

**作用与语义：**

返回`str`字符串的副本。假设给定字符串编码为UTF-16，并通过`fromUtf16()`函数转换为`QString`。

### `[static] QString QString::fromStdU32String(const std::u32string &str)`

**作用与语义：**

返回`str`字符串的副本。假设给定字符串编码为UTF-32，并利用`fromUcs4()`函数转换为`QString`。

### `[static] QString QString::fromStdWString(const std::wstring &str)`

**作用与语义：**

返回`str`字符串的副本。如果wchar_t的大小为2字节（例如Windows），则假设该字符串编码为utf16;如果wchar_t大小为4字节（大多数Unix系统），则假设为ucs4编码。

### `[static] QString QString::fromUcs4(const char32_t *unicode, qsizetype size = -1)`

**作用与语义：**

返回一个以Unicode字符串`unicode`首`size`字符初始化的 `QString`（编码为 UTF-32）。
如果`size`为-1（默认），`unicode`必须被“\0”终止。

### `[static] QString QString::fromUtf8(const char *str, qsizetype size)`

**作用与语义：**

返回一个以UTF-8字符串`str`前`size`字节初始化的`QString`。
如果`size` `-1`，则使用`strlen(str)`。
UTF-8 是一种 Unicode 编解码器，可以表示 Unicode 字符串中的所有字符，如 `QString`。然而，UTF-8 可能出现无效序列，如果发现，将被替换为一个或多个“替换字符”，或被抑制。这些序列包括非 Unicode 序列、非字符、过长序列或编码在 UTF-8 中的替代码点。
只要所有UTF-8字符在输入数据中终止，该函数即可逐步处理输入数据。字符串末尾的任何未终止字符将被替换或抑制。要进行有状态解码，请使用`QStringDecoder`。

### `[static, since 6.0] QString QString::fromUtf8(QByteArrayView str)`

**作用与语义：**

返回一个初始化为UTF-8字符串`str`的`QString`。
注意：字节数组中的任何空（'\0'）字节都包含在本字符串中，转换为Unicode的空字符（U 0000）。

### `[static] QString QString::fromUtf8(const QByteArray &str)`

**作用与语义：**

返回一个初始化为UTF-8字符串`str`的`QString`。
注意：字节数组中任何空（'\0'）字节都包含在本字符串中，转换为Unicode空字符（U 0000）。此行为与Qt 5.x不同。

### `[static, since 6.1] QString QString::fromUtf8(const char8_t *str)`

**作用与语义：**

仅在以 C 20 模式编译时，此重载才可用。

### `[static, since 6.0] QString QString::fromUtf8(const char8_t *str, qsizetype size)`

**作用与语义：**

仅在以 C 20 模式编译时，此重载才可用。

### `[static] QString QString::fromUtf16(const char16_t *unicode, qsizetype size = -1)`

**作用与语义：**

返回一个以Unicode字符串`unicode`首`size`字符初始化的`QString`（ISO-10646-UTF-16编码）。
如果`size`为-1（默认），`unicode`必须被“\0”终止。
该函数检查字节顺序标记（BOM）。如果缺少，则假设主机字节顺序。
与其他Unicode转换相比，这个函数运行较慢。如果可能，使用`QString`（const `QChar` *， qsizetype）或`QString`（const `QChar` *）。
`QString`会对Unicode数据进行深度复制。

### `[static] QString QString::fromWCharArray(const wchar_t *string, qsizetype size = -1)`

**作用与语义：**

读取`wchar_t`数组的前`size`码单元，其起始`string`指向，转换为Unicode并返回结果为`QString`。`wchar_t`所使用的编码假设类型大小为四字节时为UTF-32;若大小为两字节，则假设为UTF-16。
如果`size`为-1（默认），`string`必须被“\0”终止。

### `QChar &QString::front()`

**作用与语义：**

返回字符串中第一个字符的引用。和`operator[](0)`一样。
此功能是为了STL兼容性而提供。
警告：调用空字符串的函数构成未定义行为。

### `QChar QString::front() const`

**作用与语义：**

返回字符串中的第一个字符。和 `at(0)` 一样。
此功能是为了STL兼容性而提供。
警告：调用空字符串的函数构成未定义行为。

### `qsizetype QString::indexOf(QLatin1StringView str, qsizetype from = 0, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

返回 `str` 从索引位置 `from` 向前搜索时，首次出现拉丁语 1 字符串的索引位置。如果未找到 `str`，返回 -1。
如果`cs`是`Qt::CaseSensitive`（默认），则搜索是区分大小写的;否则搜索是不区分大小写的。
如果`from`为-1，则从最后一个字符开始搜索;如果是-2，则从倒数第二个字符开始，依此类推。

**官方示例：**

```cpp
 QString x = "sticky question";
 QString y = "sti";
 x.indexOf(y);               // returns 0
 x.indexOf(y, 1);            // returns 10
 x.indexOf(y, 10);           // returns 10
 x.indexOf(y, 11);           // returns -1
```

### `qsizetype QString::indexOf(const QRegularExpression &re, qsizetype from = 0, QRegularExpressionMatch *rmatch = nullptr) const`

**作用与语义：**

返回字符串中正则表达式`re`的第一个匹配的索引位置，从索引位置`from`向前搜索。如果`re`在任何地方都不匹配，返回-1。
如果匹配成功且`rmatch`未`nullptr`，它也会将匹配结果写入`rmatch`指向的`QRegularExpressionMatch`对象中。

**官方示例：**

```cpp
 QString str = "the minimum";
 str.indexOf(QRegularExpression("m[aeiou]"), 0);       // returns 4

 QRegularExpressionMatch match;
 str.indexOf(QRegularExpression("m[aeiou]"), 0, &match);       // returns 4
 // match.captured() == mi
```

### `qsizetype QString::indexOf(const QString &str, qsizetype from = 0, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

返回该字符串首次出现`str`的索引位置，从索引位置`from`向前搜索。如果未找到`str`，返回-1。
如果`cs`是`Qt::CaseSensitive`（默认），则搜索是区分大小写的;否则搜索是不区分大小写的。
如果`from`为-1，则从最后一个字符开始搜索;如果是-2，则从倒数第二个字符开始，依此类推。

**官方示例：**

```cpp
 QString x = "sticky question";
 QString y = "sti";
 x.indexOf(y);               // returns 0
 x.indexOf(y, 1);            // returns 10
 x.indexOf(y, 10);           // returns 10
 x.indexOf(y, 11);           // returns -1
```

### `qsizetype QString::indexOf(QChar ch, qsizetype from = 0, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

返回该字符串中字符`ch`首次出现的索引位置，从索引位置`from`向前搜索。如果找不到 `ch`，返回 -1。
注意：该功能会让`QString::indexOf()`重载。

### `[noexcept] qsizetype QString::indexOf(QStringView str, qsizetype from = 0, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

返回该字符串视图首次出现的索引位置，`str`从索引位置`from`向前搜索。如果找不到`str`，返回-1。
如果`cs`为`Qt::CaseSensitive`（默认），则搜索是区分大小写的;否则搜索是不区分大小写的。
如果`from`为-1，则从最后一个字符开始搜索;如果是-2，则从倒数第二个字符开始，依此类推。
注意：该功能会超载`QString::indexOf()`。

### `QString &QString::insert(qsizetype position, const QString &str)`

**作用与语义：**

在给定的索引`position`插入字符串`str`，并返回对该字符串的引用。
该字符串会增长以适应插入。如果 `position` 超出了字符串的末端，则在字符串上加上空格字符以达到该`position`，然后是 `str`。

**官方示例：**

```cpp
 QString str = "Meal";
 str.insert(1, QString("ontr"));
 // str == "Montreal"
```

### `QString &QString::insert(qsizetype position, QChar ch)`

**作用与语义：**

插入`ch`在字符串中给定的索引`position`处。
该字符串会随着插入而增长。如果`position`超出字符串末尾，则在字符串后加上空格字符以达到该`position`，然后是`ch`。
注意：该功能会超载`QString::insert()`。

### `QString &QString::insert(qsizetype position, QLatin1StringView str)`

**作用与语义：**

插入`str`在给定索引`position`处看到的拉丁1字符串。
该字符串会随着插入而增长。如果`position`超出了字符串的末端，则在字符串上加上空格字符以达到该`position`，然后是`str`。
注意：该功能会让`QString::insert()`重载。

### `[since 6.0] QString &QString::insert(qsizetype position, QStringView str)`

**作用与语义：**

在给定的索引`position`插入字符串视图`str`并返回该字符串的引用。
该字符串会增长以适应插入。如果`position`超出字符串末端，则在字符串上加上空格字符以达到该`position`，然后是`str`。
注意：该功能会让`QString::insert()`重载。

### `[since 6.5] QString &QString::insert(qsizetype position, QUtf8StringView str)`

**作用与语义：**

在给定的索引`position`插入UTF-8字符串视图`str`。
注意：插入变长UTF-8编码字符串数据在概念上比插入固定宽度字符串数据（如UTF-16（`QStringView`）或拉丁语1（`QLatin1StringView`）慢，因此应谨慎使用。
该字符串会随着插入而增长。如果`position`超出字符串末端，则在字符串后加上空格字符以达到该`position`，然后是`str`。
注意：该功能会让`QString::insert()`重载。

### `QString &QString::insert(qsizetype position, const QByteArray &str)`

**作用与语义：**

将`str`内容解释为UTF-8，插入它在给定索引`position`编码的Unicode字符串，并返回该字符串的引用。
该字符串会增长以适应插入。如果 `position` 超出了字符串的末端，则在字符串上加上空格字符以达到该`position`，然后是 `str`。
当`QT_NO_CAST_FROM_ASCII`定义时，该函数不可用。
注意：该功能会超载`QString::insert()`。

### `QString &QString::insert(qsizetype position, const char *str)`

**作用与语义：**

在给定的索引`position`插入 C 字符串 `str`，并返回对该字符串的引用。
该字符串会增加以适应插入。如果`position`超出字符串末尾，则在字符串后加上空格字符以达到该`position`，然后是`str`。
当`QT_NO_CAST_FROM_ASCII`定义时，该函数不可用。
注意：该功能会让`QString::insert()`重载。

### `QString &QString::insert(qsizetype position, const QChar *unicode, qsizetype size)`

**作用与语义：**

在字符串中给定的索引`position`处插入`QChar`数组`unicode`的前`size`字符。
该字符串会增长以适应插入。如果`position`超出字符串末端，则在字符串上加上空格字符以达到该`position`，随后添加`QChar`数组`unicode`的`size`字符。
注意：该功能会让`QString::insert()`重载。

### `[constexpr noexcept] bool QString::isEmpty() const`

**作用与语义：**

如果字符串没有字符，返回`true`;否则返回`false`。

**官方示例：**

```cpp
 QString().isEmpty();            // returns true
 QString("").isEmpty();          // returns true
 QString("x").isEmpty();         // returns false
 QString("abc").isEmpty();       // returns false
```

### `bool QString::isLower() const`

**作用与语义：**

如果字符串是小写字母，也就是说，它与`toLower()`折叠相同，返回`true`。
注意，这并不意味着字符串不含大写字母（有些大写字母没有小写字母折叠;`toLower()`保持不变）。更多信息请参阅Unicode标准第3.13节。

### `[constexpr] bool QString::isNull() const`

**作用与语义：**

如果该字符串为 null，则返回 `true`；否则返回 `false`。出于历史原因，Qt 区分 null 字符串和空字符串。对于大多数应用程序而言，重要的是字符串是否包含任何数据，这可以使用 `isEmpty()` 函数来确定。

**官方示例：**

```cpp
 QString().isNull();             // returns true
 QString("").isNull();           // returns false
 QString("abc").isNull();        // returns false
```

### `bool QString::isRightToLeft() const`

**作用与语义：**

如果字符串从右到左读取，返回`true`。

### `bool QString::isUpper() const`

**作用与语义：**

如果字符串是大写的，也就是说，与其`toUpper()`折叠相同，返回`true`。
注意，这并不意味着字符串不包含小写字母（有些小写字母没有大写字母折叠;它们被`toUpper()`保持不变）。更多信息请参阅Unicode标准第3.13节。

### `[noexcept] bool QString::isValidUtf16() const`

**作用与语义：**

如果字符串包含有效的UTF-16编码数据，则返回`true`，否则`false`返回。
注意，该函数不对数据进行任何特殊验证;它仅检查数据是否能成功从UTF-16解码。假设数据按主机字节顺序排列;BOM的存在无意义。

### `[since 6.0] QString QString::last(qsizetype n) &&`

**作用与语义：**

返回包含该字符串最后`n`字符的字符串。
注意：当`n` <0或`n` > `size()`时，行为未定义。

**官方示例：**

```cpp
 QString x = "Pineapple";
 QString y = x.last(5);      // y == "apple"
```

### `qsizetype QString::lastIndexOf(const QRegularExpression &re, qsizetype from, QRegularExpressionMatch *rmatch = nullptr) const`

**作用与语义：**

返回字符串中正则表达式`re`最后匹配的索引位置，该匹配始于索引位置`from`。
如果`from`为-1，则从最后一个字符开始搜索;如果是-2，则从倒数第二个字符开始，依此类推。
如果没有匹配`re`回报率为-1。
如果匹配成功且`rmatch`未`nullptr`，它还会将匹配结果写入`rmatch`指向的`QRegularExpressionMatch`对象中。
注意：由于正则表达式匹配算法的工作原理，该函数实际上会从字符串开头反复匹配直到达到`from`的位置。
注意：在搜索可能匹配0字符的正则表达式`re`时，数据末尾的匹配被负`from`排除，尽管`-1`通常被视为从字符串末尾搜索：末尾匹配位于最后一个字符之后，因此被排除。要包含这样的最终空匹配，要么给出`from`的正值，要么完全省略`from`参数。

**官方示例：**

```cpp
 QString str = "the minimum";
 str.lastIndexOf(QRegularExpression("m[aeiou]"));      // returns 8

 QRegularExpressionMatch match;
 str.lastIndexOf(QRegularExpression("m[aeiou]"), -1, &match);      // returns 8
 // match.captured() == mu
```

### `qsizetype QString::lastIndexOf(const QString &str, qsizetype from, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

返回该字符串最后一次出现的索引位置，`str`从索引位置`from`向后搜索。
如果`from`为-1，则从最后一个字符开始搜索;如果是-2，则从倒数第二个字符开始，依此类推。
如果找不到 `str`，返回 -1。
如果`cs`是`Qt::CaseSensitive`（默认），则搜索是区分大小写的;否则搜索是不区分大小写的。
注意：在寻找长度为0的`str`时，数据末尾的匹配被负`from`排除，尽管`-1`通常被视为从字符串末尾搜索：结尾的匹配位于最后一个字符之后，因此被排除。要包含这样的最终空匹配，要么给出`from`的正值，要么完全省略`from`参数。

**官方示例：**

```cpp
 QString x = "crazy azimuths";
 QString y = "az";
 x.lastIndexOf(y);           // returns 6
 x.lastIndexOf(y, 6);        // returns 6
 x.lastIndexOf(y, 5);        // returns 2
 x.lastIndexOf(y, 1);        // returns -1
```

### `[noexcept, since 6.3] qsizetype QString::lastIndexOf(QChar ch, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

注意：这个功能会让`QString::lastIndexOf()`重载。

### `[since 6.2] qsizetype QString::lastIndexOf(QLatin1StringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

返回该字符串最后一次出现的索引位置`str`该字符串。如果找不到`str`，返回 -1。
如果`cs`是`Qt::CaseSensitive`（默认），则搜索是区分大小写的;否则搜索是不区分大小写的。
注意：该功能会超载`QString::lastIndexOf()`。

**官方示例：**

```cpp
 QString x = "crazy azimuths";
 QString y = "az";
 x.lastIndexOf(y);           // returns 6
 x.lastIndexOf(y, 6);        // returns 6
 x.lastIndexOf(y, 5);        // returns 2
 x.lastIndexOf(y, 1);        // returns -1
```

### `[noexcept, since 6.2] qsizetype QString::lastIndexOf(QStringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

返回该字符串视图最后一次出现的索引位置`str`该字符串。如果找不到`str`，返回 -1。
如果`cs`是`Qt::CaseSensitive`（默认），则搜索是大小写区分的;否则搜索是不区分大小写的。
注意：该功能会超载`QString::lastIndexOf()`。

### `[since 6.2] qsizetype QString::lastIndexOf(const QRegularExpression &re, QRegularExpressionMatch *rmatch = nullptr) const`

**作用与语义：**

返回字符串中正则表达式`re`最后匹配的索引位置。如果没有匹配`re`返回-1。
如果匹配成功且`rmatch`未`nullptr`，它也会将匹配结果写入`rmatch`指向的`QRegularExpressionMatch`对象中。
注意：由于正则表达式匹配算法的工作原理，该函数实际上会从字符串开头到末尾反复匹配。
注意：该功能会让`QString::lastIndexOf()`重载。

**官方示例：**

```cpp
 QString str = "the minimum";
 str.lastIndexOf(QRegularExpression("m[aeiou]"));      // returns 8

 QRegularExpressionMatch match;
 str.lastIndexOf(QRegularExpression("m[aeiou]"), -1, &match);      // returns 8
 // match.captured() == mu
```

### `[since 6.2] qsizetype QString::lastIndexOf(const QString &str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

返回该字符串最后一次出现的索引位置`str`该字符串。如果找不到`str`，返回 -1。
如果`cs`是`Qt::CaseSensitive`（默认），则搜索是区分大小写的;否则搜索是不区分大小写的。
注意：该功能会超载`QString::lastIndexOf()`。

**官方示例：**

```cpp
 QString x = "crazy azimuths";
 QString y = "az";
 x.lastIndexOf(y);           // returns 6
 x.lastIndexOf(y, 6);        // returns 6
 x.lastIndexOf(y, 5);        // returns 2
 x.lastIndexOf(y, 1);        // returns -1
```

### `qsizetype QString::lastIndexOf(QChar ch, qsizetype from, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

返回该字符串中字符`ch`最后出现的索引位置，从索引位置`from`向后搜索。
注意：该功能会让`QString::lastIndexOf()`重载。

### `qsizetype QString::lastIndexOf(QLatin1StringView str, qsizetype from, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

返回`str`在该字符串中最后一次出现的拉丁语1字符串的索引位置，从索引位置`from`往后搜索。
如果`from`为-1，则从最后一个字符开始搜索;如果是-2，则从倒数第二个字符开始，依此类推。
如果找不到`str`，返回-1。
如果`cs`是`Qt::CaseSensitive`（默认），则搜索是区分大小写的;否则搜索是不区分大小写的。
注意：在寻找长度为0的`str`时，数据末尾的匹配被负`from`排除，尽管`-1`通常被认为是从字符串末尾搜索：结尾的匹配位于最后一个字符之后，因此被排除。要包含这样的最终空匹配，要么给出`from`的正值，要么完全省略`from`参数。
注意：该功能会让`QString::lastIndexOf()`重载。

**官方示例：**

```cpp
 QString x = "crazy azimuths";
 QString y = "az";
 x.lastIndexOf(y);           // returns 6
 x.lastIndexOf(y, 6);        // returns 6
 x.lastIndexOf(y, 5);        // returns 2
 x.lastIndexOf(y, 1);        // returns -1
```

### `[noexcept] qsizetype QString::lastIndexOf(QStringView str, qsizetype from, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

返回该字符串视图最后一次出现的索引位置，`str`从索引位置`from`回溯搜索。
如果`from`为-1，则从最后一个字符开始搜索;如果是-2，则从倒数第二个字符开始，依此类推。
如果找不到`str`，返回-1。
如果`cs`是`Qt::CaseSensitive`（默认），则搜索是区分大小写的;否则搜索是不区分大小写的。
注意：在寻找长度为0的`str`时，数据末尾的匹配被负`from`排除，尽管`-1`通常被认为是从字符串末尾搜索：结尾的匹配位于最后一个字符之后，因此被排除。要包含这样的最终空匹配，要么给出`from`的正值，要么完全省略`from`参数。
注意：该功能会让`QString::lastIndexOf()`重载。

### `QString QString::left(qsizetype n) &&`

**作用与语义：**

返回一个子串，包含该字符串最左边`n`个字符（即从字符串开头到索引位置`n`的元素，但不包括）。
如果你知道`n`不能越界，就用新代码中的`first()`，因为它更快。
如果 `n` 大于或等于 `size()`，或小于 0，则返回整个字符串。

### `QString QString::leftJustified(qsizetype width, QChar fill = u' ', bool truncate = false) const`

**作用与语义：**

返回一个大小为 `width` 的字符串，包含该字符串并由 `fill` 字符填充。
如果`truncate` `false`且字符串的 `size()` 大于 `width`，则返回的字符串是字符串的复制品。
如果`truncate`是`true`且字符串的`size()`大于`width`，则字符串副本中位置`width`之后的任何字符都会被移除，副本会被返回。

**官方示例：**

```cpp
 QString s = "apple";
 QString t = s.leftJustified(8, '.');    // t == "apple..."
```

### `[constexpr noexcept] qsizetype QString::length() const`

**作用与语义：**

返回该字符串中的字符数。等价于`size()`。

### `[static] int QString::localeAwareCompare(const QString &s1, const QString &s2)`

**作用与语义：**

将 `s1` 与 `s2` 进行比较，如果 `s1` 小于、等于或大于 `s2`，则返回小于、等于或大于零的整数。
比较是以依赖于区域设置和平台的方式执行的。使用此函数向用户展示排序后的字符串列表。

### `[since 6.0] int QString::localeAwareCompare(QStringView other) const`

**作用与语义：**

将该字符串与`other`字符串比较，如果该字符串小于、等于或大于`other`字符串，则返回小于、等于或大于零的整数。
比较以本地和平台为依据的方式进行。使用此功能向用户展示排序的字符串列表。
和`localeAwareCompare(*this, other)`一样。
注意：该功能会让`QString::localeAwareCompare()`重载。

### `int QString::localeAwareCompare(const QString &other) const`

**作用与语义：**

将该字符串与`other`字符串比较，如果该字符串小于、等于或大于`other`字符串，则返回小于、等于或大于零的整数。
比较以本地和平台为依据的方式进行。使用此功能向用户展示排序的字符串列表。
和`localeAwareCompare(*this, other)`一样。
注意：该功能会让`QString::localeAwareCompare()`重载。

### `[static, since 6.0] int QString::localeAwareCompare(QStringView s1, QStringView s2)`

**作用与语义：**

将 `s1` 与 `s2` 进行比较，如果 `s1` 小于、等于或大于 `s2`，则返回小于、等于或大于零的整数。
比较是在与区域和平台相关的方式下进行的。使用此函数向用户显示已排序的字符串列表。
注意：此函数重载了 `QString::localeAwareCompare()`。

### `[static constexpr noexcept, since 6.8] qsizetype QString::maxSize()`

**作用与语义：**

它返回字符串理论上能容纳的最大元素数。实际上，这个数量可以更小，受限于系统可用的内存容量。

### `QString QString::mid(qsizetype position, qsizetype n = -1) &&`

**作用与语义：**

返回包含该字符串的`n`个字符的字符串，从指定的`position`索引开始，直到索引位置`position` `n`的元素，但不包括。
如果你知道`position`和`n`不能越界，就用新代码中的`sliced()`，因为这样更快。
如果`position`索引超过字符串长度，返回空字符串。如果字符串中从给定`position`开始的字符少于`n`个字符，`n`或者默认值为-1，函数返回指定`position`中可用的所有字符。

### `QString QString::normalized(QString::NormalizationForm mode, QChar::UnicodeVersion version = QChar::Unicode_Unassigned) const`

**作用与语义：**

根据Unicode标准的给定`version`，返回给定Unicode规范化的字符串`mode`。

### `[since 6.10] QString &QString::nullTerminate()`

**作用与语义：**

如果字符串数据没有空终止，该方法会对数据进行深度复制，使其为空终止。
`QString`默认是空终止，但在某些情况下（例如使用`fromRawData()`时），字符串数据不一定以`\0`字符结尾，这在调用期望空终止字符串的方法时可能会成为问题。

### `[since 6.10] QString QString::nullTerminated() &&`

**作用与语义：**

返回该字符串的副本，且始终为空终止。

### `[static] QString QString::number(long n, int base = 10)`

**作用与语义：**

返回与指定`base`数相当于`n`的字符串。
默认底数为10，且必须介于2到36之间。对于非10的底，`n`被视为无符号整数。
格式总是使用`QLocale::C`，即英语/美国。要获得数字的本地字符串表示，请使用带有相应位置的`QLocale::toString()`。

**官方示例：**

```cpp
 long a = 63;
 QString s = QString::number(a, 16);             // s == "3f"
 QString t = QString::number(a, 16).toUpper();     // t == "3F"
```

### `[static] QString QString::number(double n, char format = 'g', int precision = 6)`

**作用与语义：**

返回表示浮点数 `n` 的字符串。 返回表示 `n` 的字符串，并根据指定的 `format` 和 `precision` 格式化。 对于带指数的格式，指数将显示其符号并至少有两位数字，如有需要会在指数前补零。

### `[static] QString QString::number(int n, int base = 10)`

**作用与语义：**

返回与指定`base`数相当于`n`的字符串。
默认底数为10，且必须介于2到36之间。对于非10的底，`n`被视为无符号整数。
格式总是使用`QLocale::C`，即英语/美国。要获得数字的本地字符串表示，请使用带有相应位置的`QLocale::toString()`。

**官方示例：**

```cpp
 long a = 63;
 QString s = QString::number(a, 16);             // s == "3f"
 QString t = QString::number(a, 16).toUpper();     // t == "3F"
```

### `[static] QString QString::number(qlonglong n, int base = 10)`

**作用与语义：**

返回与指定`base`数相当于`n`的字符串。
默认底数为10，且必须介于2到36之间。对于非10的底，`n`被视为无符号整数。
格式总是使用`QLocale::C`，即英语/美国。要获得数字的本地字符串表示，请使用带有相应位置的`QLocale::toString()`。

**官方示例：**

```cpp
 long a = 63;
 QString s = QString::number(a, 16);             // s == "3f"
 QString t = QString::number(a, 16).toUpper();     // t == "3F"
```

### `[static] QString QString::number(qulonglong n, int base = 10)`

**作用与语义：**

返回与指定`base`数相当于`n`的字符串。
默认底数为10，且必须介于2到36之间。对于非10的底，`n`被视为无符号整数。
格式总是使用`QLocale::C`，即英语/美国。要获得数字的本地字符串表示，请使用带有相应位置的`QLocale::toString()`。

**官方示例：**

```cpp
 long a = 63;
 QString s = QString::number(a, 16);             // s == "3f"
 QString t = QString::number(a, 16).toUpper();     // t == "3F"
```

### `[static] QString QString::number(uint n, int base = 10)`

**作用与语义：**

返回与指定`base`数相当于`n`的字符串。
默认底数为10，且必须介于2到36之间。对于非10的底，`n`被视为无符号整数。
格式总是使用`QLocale::C`，即英语/美国。要获得数字的本地字符串表示，请使用带有相应位置的`QLocale::toString()`。

**官方示例：**

```cpp
 long a = 63;
 QString s = QString::number(a, 16);             // s == "3f"
 QString t = QString::number(a, 16).toUpper();     // t == "3F"
```

### `[static] QString QString::number(ulong n, int base = 10)`

**作用与语义：**

返回与指定`base`数相当于`n`的字符串。
默认底数为10，且必须介于2到36之间。对于非10的底，`n`被视为无符号整数。
格式总是使用`QLocale::C`，即英语/美国。要获得数字的本地字符串表示，请使用带有相应位置的`QLocale::toString()`。

**官方示例：**

```cpp
 long a = 63;
 QString s = QString::number(a, 16);             // s == "3f"
 QString t = QString::number(a, 16).toUpper();     // t == "3F"
```

### `QString &QString::prepend(const QString &str)`

**作用与语义：**

在该字符串的开头前加字符串`str`，并返回对该字符串的引用。
该操作通常非常快速（常数时间），因为`QString`在字符串数据开头预分配额外空间，因此数据可以增长而无需每次重新分配整个字符串。

**官方示例：**

```cpp
 QString x = "ship";
 QString y = "air";
 x.prepend(y);
 // x == "airship"
```

### `QString &QString::prepend(QChar ch)`

**作用与语义：**

在该字符串前加字符`ch`。
注意：该功能会超载`QString::prepend()`。

### `QString &QString::prepend(QLatin1StringView str)`

**作用与语义：**

`str` 在该字符串之前 是 Latin-1 字符串。
注意：该功能会让`QString::prepend()`重载。

### `[since 6.0] QString &QString::prepend(QStringView str)`

**作用与语义：**

在字符串视图`str`前加到该字符串的开头，并返回对该字符串的引用。
注意：该功能会让`QString::prepend()`重载。

### `[since 6.5] QString &QString::prepend(QUtf8StringView str)`

**作用与语义：**

`str` 将 UTF-8 字符串视图置于该字符串前。
注意：该功能会超载`QString::prepend()`。

### `QString &QString::prepend(const QByteArray &ba)`

**作用与语义：**

在该字符串前`ba`字节数组前加。字节数组通过 `fromUtf8()` 函数转换为 Unicode。
你可以通过在编译应用时定义`QT_NO_CAST_FROM_ASCII`来禁用这个功能。例如，如果你想确保所有用户可见的字符串都通过`QObject::tr()`，这会很有用。
注意：该功能会`QString::prepend()`重载。

### `QString &QString::prepend(const char *str)`

**作用与语义：**

在字符串`str`前加上字符串。const 字符指针通过 `fromUtf8()` 函数转换为 Unicode。
你可以通过在编译应用程序时定义`QT_NO_CAST_FROM_ASCII`来禁用这个功能。例如，如果你想确保所有用户可见的字符串都通过`QObject::tr()`，这会非常有用。
注意：该功能会超载`QString::prepend()`。

### `QString &QString::prepend(const QChar *str, qsizetype len)`

**作用与语义：**

`QChar`数组`str`前加`len`字符到该字符串前，并返回对该字符串的引用。
注意：该功能会超载`QString::prepend()`。

### `void QString::push_back(const QString &other)`

**作用与语义：**

该函数是为了STL兼容性而提供，将给定的`other`字符串附加到该字符串的末尾。它等价于`append(other)`。

### `void QString::push_back(QChar ch)`

**作用与语义：**

将给定的`ch`字符附加到该字符串末尾。

### `void QString::push_front(const QString &other)`

**作用与语义：**

该函数是为了STL兼容性而提供，将给定`other`字符串置于该字符串的开头。它等价于`prepend(other)`。

### `void QString::push_front(QChar ch)`

**作用与语义：**

将给定的`ch`字符置于该字符串的开头。

### `QString::reverse_iterator QString::rbegin()`

**作用与语义：**

返回一个STL风格的反向迭代子，指向字符串中的第一个字符，顺序相反。
警告：返回的迭代器在分离或`QString`修改时将失效。

### `QString::const_reverse_iterator QString::rbegin() const`

**作用与语义：**

返回一个STL风格的反向迭代子，指向字符串中的第一个字符，顺序相反。
警告：返回的迭代器在分离或`QString`修改时将失效。

### `QString &QString::remove(const QRegularExpression &re)`

**作用与语义：**

删除字符串中所有正则表达式`re`的出现，并返回字符串的引用。例如：
元素移除可以保留字符串的容量，同时不会减少分配的内存。为了减少多余容量并释放尽可能多的内存，可以在字符串大小最后一次更改后调用`squeeze()`。

**官方示例：**

```cpp
 QString r = "Telephone";
 r.remove(QRegularExpression("[aeiou]."));
 // r == "The"
```

### `QString &QString::remove(QChar ch, Qt::CaseSensitivity cs = Qt::CaseSensitive)`

**作用与语义：**

删除该字符串中所有字符`ch`的出现，并返回对该字符串的引用。
如果`cs`是`Qt::CaseSensitive`（默认），则搜索是区分大小写的;否则搜索是不区分大小写的。
这和`replace(ch, "", cs)`一样。
元素移除可以保留字符串的容量，而不会减少分配的内存。为了减少多余容量并释放尽可能多的内存，可以在字符串大小最后一次更改后调用`squeeze()`。

**官方示例：**

```cpp
 QString t = "Ali Baba";
 t.remove(QChar('a'), Qt::CaseInsensitive);
 // t == "li Bb"
```

### `QString &QString::remove(const QString &str, Qt::CaseSensitivity cs = Qt::CaseSensitive)`

**作用与语义：**

删除该字符串中所有出现的给定`str`字符串，并返回该字符串的引用。
如果`cs`是`Qt::CaseSensitive`（默认），则搜索是区分大小写的;否则搜索是不区分大小写的。
这和`replace(str, "", cs)`一样。
元素移除可以保留字符串的容量，同时不会减少分配的内存。为了减少多余容量并释放尽可能多的内存，可以在字符串大小最后一次更改后调用`squeeze()`。

### `QString &QString::remove(qsizetype position, qsizetype n)`

**作用与语义：**

从给定的`position`索引开始，从字符串中移除`n`字符，并返回对字符串的引用。
如果指定的`position`索引在字符串内，但`position` `n`在字符串末尾之外，则字符串在指定`position`处被截断。
如果`n` <= 0，则不变。
元素移除可以保留字符串的容量，而不会减少分配的内存。为了减少额外容量并释放尽可能多的内存，可以在字符串大小最后一次更改后调用`squeeze()`。

**官方示例：**

```cpp
 QString s = "Montreal";
 s.remove(1, 4);
 // s == "Meal"
```

### `QString &QString::remove(QLatin1StringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive)`

**作用与语义：**

从该字符串中移除`str`所见的给定拉丁-1字符串的所有出现，并返回对该字符串的引用。
如果`cs`为`Qt::CaseSensitive`（默认），则搜索是区分大小写的;否则搜索为不区分大小写。
这和`replace(str, "", cs)`一样。
元素移除可以保留字符串的容量，同时不会减少分配的内存。为了减少多余的容量并尽可能释放内存，可以在字符串大小最后一次更改后调用`squeeze()`。

### `[since 6.5] QString &QString::removeAt(qsizetype pos)`

**作用与语义：**

移除索引`pos`的字符。如果`pos`超出界限（即`pos` >= `size()`），该函数不做任何事。

### `[since 6.5] QString &QString::removeFirst()`

**作用与语义：**

删除该字符串中的第一个字符。如果字符串为空，该函数不做任何操作。

### `[since 6.1] template <typename Predicate> QString &QString::removeIf(Predicate pred)`

**作用与语义：**

从字符串中移除所有谓词 `pred` 返回为真元素。返回字符串的引用。

### `[since 6.5] QString &QString::removeLast()`

**作用与语义：**

删除该字符串中的最后一个字符。如果字符串为空，该函数不做任何操作。

### `QString::reverse_iterator QString::rend()`

**作用与语义：**

返回一个STL风格的反迭代子，指向字符串中最后一个字符之后，按倒序返回。
警告：返回的迭代器在分离或`QString`修改时会失效。

### `QString::const_reverse_iterator QString::rend() const`

**作用与语义：**

返回一个STL风格的反迭代子，指向字符串中最后一个字符之后，按倒序返回。
警告：返回的迭代器在分离或`QString`修改时会失效。

### `QString QString::repeated(qsizetype times) const`

**作用与语义：**

返回该字符串的副本，重复了指定数量的`times`。
如果`times`小于1，则返回一个空字符串。

**官方示例：**

```cpp
 QString str("ab");
 str.repeated(4);            // returns "abababab"
```

### `QString &QString::replace(qsizetype position, qsizetype n, const QString &after)`

**作用与语义：**

用字符串`after`替换从索引`n` `position`开始的字符，并返回对该字符串的引用。
注意：如果指定的`position`索引在字符串内，但`position` `n`超出字符串范围，则将`n`调整为在字符串末尾停止。

**官方示例：**

```cpp
 QString x = "Say yes!";
 QString y = "no";
 x.replace(4, 3, y);
 // x == "Say no!"
```

### `QString &QString::replace(const QRegularExpression &re, const QString &after)`

**作用与语义：**

将字符串中`re`的正则表达式的每次出现都替换为 `after`。返回字符串的引用。例如：
对于包含捕获群的正则表达式，`after`中出现的\1， \2， ...被对应捕获群捕获的字符串所替代。
注意：该功能会让`QString::replace()`重载。

**官方示例：**

```cpp
 QString s = "Banana";
 s.replace(QRegularExpression("a[mn]"), "ox");
 // s == "Boxoxa"
```

### `QString &QString::replace(QChar before, QChar after, Qt::CaseSensitivity cs = Qt::CaseSensitive)`

**作用与语义：**

用字符`after`替换所有出现的字符`before`，并返回对该字符串的引用。
如果`cs`是`Qt::CaseSensitive`（默认），则搜索是大小写区分的;否则搜索是不区分大小写的。
注意：该功能会超载`QString::replace()`。

### `QString &QString::replace(QChar c, QLatin1StringView after, Qt::CaseSensitivity cs = Qt::CaseSensitive)`

**作用与语义：**

将字符`c`的每次出现都替换为字符串`after`，并返回对该字符串的引用。
如果`cs`是`Qt::CaseSensitive`（默认），则搜索是区分大小写的;否则搜索是不区分大小写的。
注意：文本在更换后不会重新扫描。
注意：该功能会`QString::replace()`重载。

### `QString &QString::replace(QChar ch, const QString &after, Qt::CaseSensitivity cs = Qt::CaseSensitive)`

**作用与语义：**

将字符串中所有出现的字符`ch`替换为 `after`，并返回该字符串的引用。
如果`cs`是`Qt::CaseSensitive`（默认），则搜索区分大小写;否则搜索不区分大小写。
注意：此功能会让`QString::replace()`重载。

### `QString &QString::replace(QLatin1StringView before, QLatin1StringView after, Qt::CaseSensitivity cs = Qt::CaseSensitive)`

**作用与语义：**

将`before`看到的拉丁1字符串中出现的每一个字符串替换为`after`看到的拉丁1字符串，并返回对该字符串的引用。
如果`cs`是`Qt::CaseSensitive`（默认），则搜索是区分大小写的;否则搜索是不区分大小写的。
注意：文本在更换后不会重新扫描。
注意：如果使用空的`before`参数，`after`参数会在字符串的每个字符前后插入。
注意：该功能会超载`QString::replace()`。

### `QString &QString::replace(QLatin1StringView before, const QString &after, Qt::CaseSensitivity cs = Qt::CaseSensitive)`

**作用与语义：**

将`before` 查看的拉丁字母1字符串中的所有出现替换为字符串 `after`，并返回该字符串的引用。
如果`cs`为`Qt::CaseSensitive`（默认），则搜索区分大小写;否则搜索不区分大小写。
注意：文本在更换后不会重新扫描。
注意：如果你使用空的`before`参数，`after`参数会在字符串的每个字符前后插入。
注意：该功能会让`QString::replace()`重载。

### `QString &QString::replace(const QString &before, QLatin1StringView after, Qt::CaseSensitivity cs = Qt::CaseSensitive)`

**作用与语义：**

将字符串`before`的每次出现替换为字符串`after`，并返回对该字符串的引用。
如果`cs`是`Qt::CaseSensitive`（默认），则搜索区分大小写;否则搜索不区分大小写。
注意：文本在更换后不会重新扫描。
注意：如果使用空的`before`参数，`after`参数会在字符串的每个字符前后插入。
注意：该功能会超载`QString::replace()`。

### `QString &QString::replace(const QString &before, const QString &after, Qt::CaseSensitivity cs = Qt::CaseSensitive)`

**作用与语义：**

将字符串`before`的每次出现替换为字符串`after`，并返回对该字符串的引用。
如果`cs`是`Qt::CaseSensitive`（默认），则搜索是区分大小写的;否则搜索是不区分大小写的。
注意：替换文本插入后不会重新扫描。
注意：如果使用空`before`参数，`after`参数会在字符串的每个字符前后插入。
注意：该功能会让`QString::replace()`重载。

**官方示例：**

```cpp
 QString str = "colour behaviour flavour neighbour";
 str.replace(QString("ou"), QString("o"));
 // str == "color behavior flavor neighbor"
```

### `QString &QString::replace(qsizetype position, qsizetype n, QChar after)`

**作用与语义：**

将索引`position`开始的`n`字符替换为字符`after`，并返回该字符串的引用。
注意：该功能会超载`QString::replace()`。

### `QString &QString::replace(qsizetype position, qsizetype n, const QChar *after, qsizetype alen)`

**作用与语义：**

将索引`position`开始的`n`字符替换为`QChar`数组`after`的前`alen`字符，并返回对该字符串的引用。
`n`不能是负面的。
注意：该功能会让`QString::replace()`重载。

### `QString &QString::replace(const QChar *before, qsizetype blen, const QChar *after, qsizetype alen, Qt::CaseSensitivity cs = Qt::CaseSensitive)`

**作用与语义：**

将该字符串中 `before` 的前`blen`字符替换为 `after` 的前`alen`字符，并返回该字符串的引用。
如果`cs`是`Qt::CaseSensitive`（默认），则搜索是区分大小写的;否则搜索是不区分大小写的。
注意：如果`before`指向空字符串（即`blen` == 0），`after`指向的字符串会在该字符串的每个字符之前和之后插入。
注意：该功能会超载`QString::replace()`。

### `void QString::reserve(qsizetype size)`

**作用与语义：**

确保字符串至少有 `size` 个字符的空间。
如果你事先知道字符串的大小，可以调用此函数以在构建过程中避免重复重新分配。这在逐步构建字符串时可以提升性能。对字符串进行长序列添加操作可能会触发多次重新分配，最后一次重新分配可能会比实际所需空间多得多。这比在开始时进行一次正确大小的分配效率低。
如果不确定需要多少空间，通常最好将 `size` 作为上限，或者对最可能的大小进行高估，如果严格的上限比此大得多。如果 `size` 被低估，一旦超过预留大小，字符串将按需增长，这可能导致比最佳估计更大的分配，并且会减慢触发该操作的速度。
警告：reserve() 仅预留内存，但不会改变字符串大小。访问字符串末尾之外的数据是未定义行为。如果你需要访问字符串当前末尾之外的内存，请使用 `resize()`。
此函数对于需要构建长字符串且希望避免重复重新分配的代码非常有用。在此示例中，我们希望向字符串添加内容，直到某个条件 `true` 满足，并且我们相当确定该大小足够，使得调用 reserve() 是值得的：

**官方示例：**

```cpp
 QString result;
 qsizetype maxSize;
 bool condition;
 QChar nextChar;

 result.reserve(maxSize);

 while (condition)
     result.append(nextChar);

 result.squeeze();
```

### `void QString::resize(qsizetype size)`

**作用与语义：**

将字符串大小设置为`size`字符。
如果`size`大于当前大小，字符串会被扩展为 `size` 字符长度，并加上额外的字符。新字符未初始化。
如果`size`小于当前大小，超出位置`size`的字符将被排除在字符串之外。
注意：虽然resize()会根据需要增加容量，但不会缩减容量。要减少多余容量，请使用`squeeze()`。
如果你想在字符串上附加一定数量的相同字符，可以使用 `resize`（qsizetype， QChar） 重载。
如果你想扩展字符串使其达到一定宽度，并用特定字符填充新位置，可以使用`leftJustified()`函数：
如果`size`为负，则等同于通过零。

**官方示例：**

```cpp
 QString s = "Hello world";
 s.resize(5);
 // s == "Hello"

 s.resize(8);
 // s == "Hello???" (where ? stands for any character)
```

### `void QString::resize(qsizetype newSize, QChar fillChar)`

**作用与语义：**

与 `resize`（qsizetype） 不同，该超载将新字符初始化为 `fillChar`：

**官方示例：**

```cpp
 QString t = "Hello";
 t.resize(t.size() + 10, 'X');
 // t == "HelloXXXXXXXXXX"
```

### `[since 6.8] void QString::resizeForOverwrite(qsizetype size)`

**作用与语义：**

将字符串大小设置为`size`字符。如果字符串大小增加，新字符将被初始化。
行为和`resize(size)`完全一样。

### `QString QString::right(qsizetype n) &&`

**作用与语义：**

返回包含该字符串最右`n`字符的子串。
如果你知道`n`不能越界，就用新代码中的`last()`，因为这样更快。
如果`n`大于或等于`size()`或小于零，则返回整个字符串。

### `QString QString::rightJustified(qsizetype width, QChar fill = u' ', bool truncate = false) const`

**作用与语义：**

返回一串包含`fill`字符后跟字符串的`size()` `width`字符串。例如：
如果`truncate` `false`且字符串的`size()`大于`width`，则返回的字符串是字符串的复制品。
如果`truncate`为真且弦的 `size()` 大于 `width`，则该弦在位置 `width` 被截断。

**官方示例：**

```cpp
 QString s = "apple";
 QString t = s.rightJustified(8, '.');    // t == "...apple"
```

### `QString QString::section(QChar sep, qsizetype start, qsizetype end = -1, QString::SectionFlags flags = SectionDefault) const`

**作用与语义：**

该函数返回字符串的一段。
该字符串被视为由字符`sep`分隔的一系列字段。返回的字符串包含从位置`start`到位置`end`的字段。如果未指定`end`，则包含从位置`start`到字符串末尾的所有字段。字段编号为0、1、2等，从左开始计数，以及-1、-2等，从右到左数。
`flags`参数可用于影响函数行为的某些方面，例如是否区分大小写，是否跳过空字段，以及如何处理前置和后置分隔符;参见`SectionFlags`。
如果`start`或`end`为负，则计数字符串右侧的场，最右端的场为-1，最右端的场为-2，依此类推。

**官方示例：**

```cpp
 QString str;
 QString csv = "forename,middlename,surname,phone";
 QString path = "/usr/local/bin/myapp"; // First field is empty
 QString::SectionFlag flag = QString::SectionSkipEmpty;

 str = csv.section(',', 2, 2);   // str == "surname"
 str = path.section('/', 3, 4);  // str == "bin/myapp"
 str = path.section('/', 3, 3, flag); // str == "myapp"
```

### `QString QString::section(const QRegularExpression &re, qsizetype start, qsizetype end = -1, QString::SectionFlags flags = SectionDefault) const`

**作用与语义：**

该字符串被视为由正则表达式`re`分隔的一系列场。
警告：使用此`QRegularExpression`版本的成本远高于重载字符串和字符版本。
注意：该功能会让`QString::section()`重载。

**官方示例：**

```cpp
 QString line = "forename\tmiddlename  surname \t \t phone";
 QRegularExpression sep("\\s+");
 str = line.section(sep, 2, 2); // str == "surname"
 str = line.section(sep, -3, -2); // str == "middlename  surname"
```

### `QString QString::section(const QString &sep, qsizetype start, qsizetype end = -1, QString::SectionFlags flags = SectionDefault) const`

**作用与语义：**

注意：此功能会让`QString::section()`重载。

**官方示例：**

```cpp
 QString str;
 QString data = "forename**middlename**surname**phone";

 str = data.section("**", 2, 2); // str == "surname"
 str = data.section("**", -3, -2); // str == "middlename**surname"
```

### `QString &QString::setNum(int n, int base = 10)`

**作用与语义：**

将字符串设置为指定`base`中`n`的打印值，并返回对该字符串的引用。
默认基础是10，必须在2到36之间。
格式总是使用`QLocale::C`，即英语/UnitedStates。要获得数字的本地字符串表示，请使用带有相应位置的 `QLocale::toString()`。

**官方示例：**

```cpp
 QString str;
 str.setNum(1234);       // str == "1234"
```

### `QString &QString::setNum(long n, int base = 10)`

**作用与语义：**

将字符串设置为指定`base`中`n`的打印值，并返回对该字符串的引用。
默认基础是10，必须在2到36之间。
格式总是使用`QLocale::C`，即英语/UnitedStates。要获得数字的本地字符串表示，请使用带有相应位置的 `QLocale::toString()`。

**官方示例：**

```cpp
 QString str;
 str.setNum(1234);       // str == "1234"
```

### `QString &QString::setNum(qlonglong n, int base = 10)`

**作用与语义：**

将字符串设置为指定`base`中`n`的打印值，并返回对该字符串的引用。
默认基础是10，必须在2到36之间。
格式总是使用`QLocale::C`，即英语/UnitedStates。要获得数字的本地字符串表示，请使用带有相应位置的 `QLocale::toString()`。

**官方示例：**

```cpp
 QString str;
 str.setNum(1234);       // str == "1234"
```

### `QString &QString::setNum(qulonglong n, int base = 10)`

**作用与语义：**

将字符串设置为指定`base`中`n`的打印值，并返回对该字符串的引用。
默认基础是10，必须在2到36之间。
格式总是使用`QLocale::C`，即英语/UnitedStates。要获得数字的本地字符串表示，请使用带有相应位置的 `QLocale::toString()`。

**官方示例：**

```cpp
 QString str;
 str.setNum(1234);       // str == "1234"
```

### `QString &QString::setNum(short n, int base = 10)`

**作用与语义：**

将字符串设置为指定`base`中`n`的打印值，并返回对该字符串的引用。
默认基础是10，必须在2到36之间。
格式总是使用`QLocale::C`，即英语/UnitedStates。要获得数字的本地字符串表示，请使用带有相应位置的 `QLocale::toString()`。

**官方示例：**

```cpp
 QString str;
 str.setNum(1234);       // str == "1234"
```

### `QString &QString::setNum(uint n, int base = 10)`

**作用与语义：**

将字符串设置为指定`base`中`n`的打印值，并返回对该字符串的引用。
默认基础是10，必须在2到36之间。
格式总是使用`QLocale::C`，即英语/UnitedStates。要获得数字的本地字符串表示，请使用带有相应位置的 `QLocale::toString()`。

**官方示例：**

```cpp
 QString str;
 str.setNum(1234);       // str == "1234"
```

### `QString &QString::setNum(ulong n, int base = 10)`

**作用与语义：**

将字符串设置为指定`base`中`n`的打印值，并返回对该字符串的引用。
默认基础是10，必须在2到36之间。
格式总是使用`QLocale::C`，即英语/UnitedStates。要获得数字的本地字符串表示，请使用带有相应位置的 `QLocale::toString()`。

**官方示例：**

```cpp
 QString str;
 str.setNum(1234);       // str == "1234"
```

### `QString &QString::setNum(ushort n, int base = 10)`

**作用与语义：**

将字符串设置为指定`base`中`n`的打印值，并返回对该字符串的引用。
默认基础是10，必须在2到36之间。
格式总是使用`QLocale::C`，即英语/UnitedStates。要获得数字的本地字符串表示，请使用带有相应位置的 `QLocale::toString()`。

**官方示例：**

```cpp
 QString str;
 str.setNum(1234);       // str == "1234"
```

### `QString &QString::setNum(double n, char format = 'g', int precision = 6)`

**作用与语义：**

将字符串设置为打印值的 `n`，格式化为给定的`format`和`precision`，并返回字符串的引用。

### `QString &QString::setNum(float n, char format = 'g', int precision = 6)`

**作用与语义：**

将字符串设置为打印值的 `n`，格式化为给定的`format`和`precision`，并返回字符串的引用。
格式总是使用`QLocale::C`，即英语/美国。要获得数字的本地化字符串表示，请使用带有相应位置的 `QLocale::toString()`。

### `QString &QString::setRawData(const QChar *unicode, qsizetype size)`

**作用与语义：**

重置`QString`，使 Unicode 字符在数组中使用前`size`个字符`unicode`。其中的数据`unicode`不会被复制。调用者必须能够保证只要`QString`（或其未修改的副本）存在，就不会`unicode`被删除或修改。
该函数可以代替`fromRawData()`，用于重复利用已有`QString`对象，从而节省内存重新分配。

### `QString &QString::setUnicode(const QChar *unicode, qsizetype size)`

**作用与语义：**

将字符串调整为`size`字符，并将`unicode`复制到字符串中。
如果`unicode` `nullptr`，则不会复制任何内容，但字符串仍会被调整为`size`。

### `[since 6.9] QString &QString::setUnicode(const char16_t *unicode, qsizetype size)`

**作用与语义：**

将字符串调整为`size`字符，并将`unicode`复制到字符串中。
如果`unicode` `nullptr`，则不会复制任何内容，但字符串仍会被调整为`size`。

### `[since 6.9] QString &QString::setUtf16(const char16_t *unicode, qsizetype size)`

**作用与语义：**

将字符串调整为`size`字符，并将`unicode`复制到字符串中。
如果`unicode`是`nullptr`，则不会复制任何内容，但字符串仍会被调整为`size`。
注意，与`fromUtf16()`不同，该函数不考虑BOM及可能的不同字节顺序。

### `void QString::shrink_to_fit()`

**作用与语义：**

该功能是为了STL兼容性而提供。它等同于`squeeze()`。

### `QString QString::simplified() const`

**作用与语义：**

返回一个字符串，该字符串已从开头和结尾移除空白，并且将每个内部空白序列替换为单个空格。空白指的是任何 `QChar::isSpace()` 返回 `true` 的字符。这包括 ASCII 字符 '\t'、'\n'、'\v'、'\f'、'\r' 和 ' '。

**官方示例：**

```cpp
 QString str = "  lots\t of\nwhitespace\r\n ";
 str = str.simplified();
 // str == "lots of whitespace";
```

### `[constexpr noexcept] qsizetype QString::size() const`

**作用与语义：**

返回该字符串中的字符数。
字符串中的最后一个字符位置大小为() - 1。

**官方示例：**

```cpp
 QString str = "World";
 qsizetype n = str.size();   // n == 5
 str.data()[0];              // returns 'W'
 str.data()[4];              // returns 'd'
```

### `[since 6.8] QString &QString::slice(qsizetype pos, qsizetype n)`

**作用与语义：**

修改该字符串，使其从位置`pos`开始，直到但不包括索引位置`pos` `n`的字符（码点）;并返回对该字符串的引用。
注意：行为未定义，`pos` <为0、`n` <0或`pos` `n` > `size()`。

**官方示例：**

```cpp
 QString x = u"Nine pineapples"_s;
 x.slice(5);     // x == "pineapples"
 x.slice(4, 3);  // x == "app"
```

### `[since 6.8] QString &QString::slice(qsizetype pos)`

**作用与语义：**

修改该字符串，使其从位置`pos`开始并延伸至末尾，并返回该字符串的引用。
注意：行为未定义`pos` <0或`pos` > `size()`。

### `[since 6.0] QString QString::sliced(qsizetype pos, qsizetype n) &&`

**作用与语义：**

返回包含该字符串的`n`个字符的字符串，从位置`pos`开始，直到索引位置`pos` `n`的元素，但不包括。
注意：当`pos` <为0、`n` <0或`pos` `n` > `size()`时，行为未定义。

**官方示例：**

```cpp
 QString x = "Nine pineapples";
 QString y = x.sliced(5, 4);            // y == "pine"
 QString z = x.sliced(5);               // z == "pineapples"
```

### `[since 6.0] QString QString::sliced(qsizetype pos) &&`

**作用与语义：**

返回包含该字符串的`n`个字符的字符串，从位置`pos`开始，直到索引位置`pos` `n`的元素，但不包括。
注意：当`pos` <为0、`n` <0或`pos` `n` > `size()`时，行为未定义。

**官方示例：**

```cpp
 QString x = "Nine pineapples";
 QString y = x.sliced(5, 4);            // y == "pine"
 QString z = x.sliced(5);               // z == "pineapples"
```

### `QStringList QString::split(const QString &sep, Qt::SplitBehavior behavior = Qt::KeepEmptyParts, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

在 `sep` 出现的地方将字符串拆分为子串，并返回这些字符串的列表。如果 `sep` 在字符串中没有匹配，split() 返回包含该字符串的单元素列表。
`cs`规定`sep`应是按大小写区分匹配还是不区分大小写。
如果`behavior` `Qt::SkipEmptyParts`，结果中不会出现空条目。默认情况下，空条目会被保留。
如果`sep`为空，split() 返回一个空字符串，后面是该字符串的每个字符，再返回另一个空字符串：
要理解这种行为，请记住空字符串在所有地方都匹配，因此上述在质上与以下内容相同：

**官方示例：**

```cpp
 QString str = QStringLiteral("a,,b,c");

 QStringList list1 = str.split(u',');
 // list1: [ "a", "", "b", "c" ]

 QStringList list2 = str.split(u',', Qt::SkipEmptyParts);
 // list2: [ "a", "b", "c" ]
```

### `QStringList QString::split(const QRegularExpression &re, Qt::SplitBehavior behavior = Qt::KeepEmptyParts) const`

**作用与语义：**

将字符串拆分为子串，正则表达式`re`匹配的部分，返回这些字符串的列表。如果字符串中`re`不匹配，split() 返回包含该字符串的单元素列表。
这里有一个例子，我们用一个或多个空白字符作为分隔符提取句子中的单词：
这里有一个类似的例子，但这次我们使用任意非单词字符序列作为分隔符：
这里有第三个例子，我们使用零长度断言\b（词边界）将字符串拆分为交替的非词和词序列：

**官方示例：**

```cpp
 QString str;
 QStringList list;

 str = "Some  text\n\twith  strange whitespace.";
 list = str.split(QRegularExpression("\\s+"));
 // list: [ "Some", "text", "with", "strange", "whitespace." ]
```

### `QStringList QString::split(QChar sep, Qt::SplitBehavior behavior = Qt::KeepEmptyParts, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

在 `sep` 出现的地方将字符串拆分为子串，并返回这些字符串的列表。如果 `sep` 在字符串中没有匹配，split() 返回包含该字符串的单元素列表。
`cs`规定`sep`应是按大小写区分匹配还是不区分大小写。
如果`behavior` `Qt::SkipEmptyParts`，结果中不会出现空条目。默认情况下，空条目会被保留。
如果`sep`为空，split() 返回一个空字符串，后面是该字符串的每个字符，再返回另一个空字符串：
要理解这种行为，请记住空字符串在所有地方都匹配，因此上述在质上与以下内容相同：

**官方示例：**

```cpp
 QString str = QStringLiteral("a,,b,c");

 QStringList list1 = str.split(u',');
 // list1: [ "a", "", "b", "c" ]

 QStringList list2 = str.split(u',', Qt::SkipEmptyParts);
 // list2: [ "a", "b", "c" ]
```

### `void QString::squeeze()`

**作用与语义：**

释放所有不需要存储字符数据的内存。
该函数的唯一目的是提供一种微调`QString`内存使用的方法。一般来说，你很少需要调用这个函数。

### `bool QString::startsWith(const QString &s, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

如果字符串以 `s` 开头，返回 `true`;否则返回 `false`。
如果`cs`是`Qt::CaseSensitive`（默认），则搜索是大小写区分的;否则搜索是大小写不区分的。

**官方示例：**

```cpp
 QString str = "Bananas";
 str.startsWith("Ban");     // returns true
 str.startsWith("Car");     // returns false
```

### `bool QString::startsWith(QChar c, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

如果字符串以 `c` 开头，返回 `true`;否则返回 `false`。
注意：该功能会超载`QString::startsWith()`。

### `bool QString::startsWith(QLatin1StringView s, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

注意：该功能会超载`QString::startsWith()`。

### `[noexcept] bool QString::startsWith(QStringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**作用与语义：**

如果字符串以字符串视图`str`开头，返回`true`;否则返回`false`。
如果`cs`是`Qt::CaseSensitive`（默认），则搜索不区分大小写;否则搜索不区分大小写。

### `[noexcept] void QString::swap(QString &other)`

**作用与语义：**

将这串与`other`交换。这个操作非常快，从未失败过。

### `CFStringRef QString::toCFString() const`

**作用与语义：**

从`QString`创建CFStriring。
调用者拥有CFStriing，并负责释放该系统。
注意：此功能仅适用于macOS和iOS。

### `QString QString::toCaseFolded() const`

**作用与语义：**

返回字符串的大小叠折等价值。对于大多数Unicode字符，这与`toLower()`相同。

### `double QString::toDouble(bool *ok = nullptr) const`

**作用与语义：**

返回转换为`double`值的字符串。
如果转换溢出，返回无穷大;如果因其他原因（如溢出），则返回0.0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`来报告失败，成功则将*`ok`设为`true`。
警告：`QString`内容可能仅包含有效的数字字符，包括加号/减号、科学记号中的字符e和小数点。添加单位或额外字符会导致换算错误。
字符串转换总是在“C”区域进行。对于位置相关转换，请使用`QLocale::toDouble()`。
出于历史原因，该函数无法处理成千上万个群分隔符。如果你需要转换这些数字，可以使用`QLocale::toDouble()`。
该函数忽略前置和后置的空白。

**官方示例：**

```cpp
 QString str = "1234.56";
 double val = str.toDouble();   // val == 1234.56
```

### `[since 6.6] emscripten::val QString::toEcmaString() const`

**作用与语义：**

将该对象转换为ECMAScript字符串。

### `float QString::toFloat(bool *ok = nullptr) const`

**作用与语义：**

返回转换为`float`值的字符串。
如果转换溢出，返回无穷大;如果因其他原因（如溢出），则返回0.0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`来报告失败，成功则将*`ok`设为`true`。
警告：`QString`内容可能仅包含有效的数字字符，包括加号/减号、科学记号中使用的字符e和小数点。添加单位或额外字符会导致转换错误。
字符串转换总是在“C”区域内进行。对于依赖位置的转换，请使用`QLocale::toFloat()`。
出于历史原因，该函数无法处理成千上万个组分隔符。如果你需要转换这些数字，可以使用`QLocale::toFloat()`。
该函数忽略前置和后置的空白。

**官方示例：**

```cpp
 QString str1 = "1234.56";
 str1.toFloat();             // returns 1234.56

 bool ok;
 QString str2 = "R2D2";
 str2.toFloat(&ok);          // returns 0.0, sets ok to false

 QString str3 = "1234.56 Volt";
 str3.toFloat(&ok);          // returns 0.0, sets ok to false
```

### `QString QString::toHtmlEscaped() const`

**作用与语义：**

将纯文本字符串转换为带有 HTML 元字符 `<`、`>`、`&` 和 `"` 的 HTML 字符串，并被 HTML 实体替代。

**官方示例：**

```cpp
 QString plain = "#include <QtCore>";
 QString html = plain.toHtmlEscaped();
 // html == "#include <QtCore>"
```

### `int QString::toInt(bool *ok = nullptr, int base = 10) const`

**作用与语义：**

返回使用底`base`转换为`int`的字符串，默认为10，且必须介于2到36之间，即0。转换失败时返回0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`报告失败，成功则将*`ok`设为`true`。
如果`base`为0，则使用C语言惯例：如果字符串以“0x”开头，使用进制16;否则，如果字符串以“0b”开头，使用进制2;否则，如果字符串以“0”开头，使用进制8;否则，使用进制10。
字符串转换总是在“C”区域内进行。对于位置相关转换，请使用`QLocale::toInt()`。
该函数忽略前置和后置的空白。
注意：在Qt 6.4中加入了对“0b”前缀的支持。

**官方示例：**

```cpp
 QString str = "FF";
 bool ok;
 int hex = str.toInt(&ok, 16);       // hex == 255, ok == true
 int dec = str.toInt(&ok, 10);       // dec == 0, ok == false
```

### `QByteArray QString::toLatin1() const`

**作用与语义：**

返回字符串的拉丁-1表示，作为`QByteArray`。
如果字符串包含非 Latin1 字符，返回的字节数组是未定义的。这些字符可以被抑制或用问号替换。

### `QByteArray QString::toLocal8Bit() const`

**作用与语义：**

返回字符串的本地8位表示，作为`QByteArray`。
在 Unix 系统上，这相当于 `toUtf8()`。注意，在 Apple 系统中，该函数不考虑 NSString.defaultCStringEncoding 或 CFStringGetSystemEncoding()，因为这些函数通常返回传统的“Western （Mac OS Roman）”编码，现代苹果操作系统不应使用该编码。在 Windows 上，系统当前代码页被使用。
如果该字符串包含任何无法用本地8位编码编码的字符，返回的字节数组是未定义的。这些字符可以被抑制或替换为其他字符。

### `long QString::toLong(bool *ok = nullptr, int base = 10) const`

**作用与语义：**

返回使用基数`base`转换为`long`的字符串，默认为10，且必须介于2到36之间，即0。如果转换失败，返回0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`来报告失败，成功则将*`ok`设为`true`。
如果`base`为0，则使用C语言惯例：如果字符串以“0x”开头，使用进制16;否则，如果字符串以“0b”开头，使用进制2;否则，如果字符串以“0”开头，使用进制8;否则，使用进制10。
字符串转换总是在“C”区域进行。对于依赖位置的转换，请使用`QLocale::toLongLong()`。
该函数忽略前置和后置的空白。
注意：在Qt 6.4中加入了对“0b”前缀的支持。

**官方示例：**

```cpp
 QString str = "FF";
 bool ok;

 long hex = str.toLong(&ok, 16);     // hex == 255, ok == true
 long dec = str.toLong(&ok, 10);     // dec == 0, ok == false
```

### `qlonglong QString::toLongLong(bool *ok = nullptr, int base = 10) const`

**作用与语义：**

返回使用基数`base`转换为`long long`的字符串，默认为10，且必须介于2到36之间，即0。如果转换失败，返回0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`报告失败，成功则将*`ok`设为`true`。
如果`base`为0，则使用C语言的惯例：如果字符串以“0x”开头，使用进制16;否则，如果字符串以“0b”开头，使用进制2;否则，如果字符串以“0”开头，使用进制8;否则，使用进制10。
字符串转换总是在“C”区域进行。对于依赖位置的转换，请使用`QLocale::toLongLong()`。
该函数忽略前置和后置的空白。
注意：在Qt 6.4中加入了对“0b”前缀的支持。

**官方示例：**

```cpp
 QString str = "FF";
 bool ok;

 qint64 hex = str.toLongLong(&ok, 16);      // hex == 255, ok == true
 qint64 dec = str.toLongLong(&ok, 10);      // dec == 0, ok == false
```

### `QString QString::toLower() const`

**作用与语义：**

返回字符串的小写副本。
大小写转换总是在“C”区域进行。对于局部相关的大小写折叠，使用`QLocale::toLower()`。

**官方示例：**

```cpp
 QString str = "The Qt PROJECT";
 str = str.toLower();        // str == "the qt project"
```

### `NSString *QString::toNSString() const`

**作用与语义：**

从`QString`创建一个NSStriring。
国家安全链是自动释放的。
注意：此功能仅适用于macOS和iOS。

### `short QString::toShort(bool *ok = nullptr, int base = 10) const`

**作用与语义：**

返回用`base`底数转换为`short`的字符串，默认为10，且必须介于2到36之间，即0。转换失败时返回0。
如果 `ok` 未`nullptr`，则通过将 *`ok` 设为 `false` 来报告失败，通过将 *`ok` 设为 `true` 来报告失败。
如果`base`为0，则使用C语言的惯例：如果字符串以“0x”开头，使用进制16;否则，如果字符串以“0b”开头，使用进制2;否则，如果字符串以“0”开头，使用进制8;否则，使用进制10。
字符串转换总是在“C”区域进行。对于依赖位置的转换，请使用`QLocale::toShort()`。
该函数忽略前置和后置的空白。
注意：在Qt 6.4中加入了对“0b”前缀的支持。

**官方示例：**

```cpp
 QString str = "FF";
 bool ok;

 short hex = str.toShort(&ok, 16);   // hex == 255, ok == true
 short dec = str.toShort(&ok, 10);   // dec == 0, ok == false
```

### `std::string QString::toStdString() const`

**作用与语义：**

返回包含该`QString`数据的 std：：string 对象。Unicode 数据通过 `toUtf8()` 函数转换为 8 位字符。
该方法主要用于将`QString`传递给接受 std：：string 对象的函数。

### `std::u16string QString::toStdU16String() const`

**作用与语义：**

返回一个带有该`QString`数据的 std：：u16string 对象。Unicode 数据与 `utf16()` 方法返回相同。

### `std::u32string QString::toStdU32String() const`

**作用与语义：**

返回一个包含该`QString`数据的 std：：u32string 对象。Unicode 数据与 `toUcs4()` 方法返回相同。

### `std::wstring QString::toStdWString() const`

**作用与语义：**

返回包含该`QString`中数据的 std：：wstring 对象。std：：wstring 在 wchar_t 宽度为 2 字节的平台上（例如 Windows）以 UTF-16 编码;在 wchar_t 宽度为 4 字节的平台（大多数 Unix 系统）则以 UTF-32 编码。
该方法主要用于将`QString`传递给接受 std：：wstring 对象的函数。

### `uint QString::toUInt(bool *ok = nullptr, int base = 10) const`

**作用与语义：**

返回用基数`base`转换为`unsigned int`的字符串，默认为10，且必须介于2到36之间，即0。转换失败时返回0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`报告失败，成功通过将*`ok`设为`true`来报告。
如果`base`为0，则使用C语言的约定：如果字符串以“0x”开头，则使用进制16;否则，如果字符串以“0b”开头，使用进制2;否则，如果字符串以“0”开头，使用进制8;否则，使用进制10。
字符串转换总是在“C”区域进行。对于依赖位置的转换，使用`QLocale::toUInt()`。
该函数忽略前置和后置的空白。
注意：在Qt 6.4中加入了对“0b”前缀的支持。

**官方示例：**

```cpp
 QString str = "FF";
 bool ok;

 uint hex = str.toUInt(&ok, 16);     // hex == 255, ok == true
 uint dec = str.toUInt(&ok, 10);     // dec == 0, ok == false
```

### `ulong QString::toULong(bool *ok = nullptr, int base = 10) const`

**作用与语义：**

返回使用基数`base`转换为`unsigned long`的字符串，默认为10，且必须在2到36之间，即0。如果转换失败，返回0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`来报告失败，成功则将*`ok`设为`true`。
如果`base`为0，则使用C语言惯例：如果字符串以“0x”开头，使用进制16;否则，如果字符串以“0b”开头，使用进制2;否则，如果字符串以“0”开头，使用进制8;否则，使用进制10。
字符串转换总是在“C”区域进行。对于依赖位置的转换，请使用`QLocale::toULongLong()`。
该函数忽略前置和后置的空白。
注意：在Qt 6.4中加入了对“0b”前缀的支持。

**官方示例：**

```cpp
 QString str = "FF";
 bool ok;

 ulong hex = str.toULong(&ok, 16);   // hex == 255, ok == true
 ulong dec = str.toULong(&ok, 10);   // dec == 0, ok == false
```

### `qulonglong QString::toULongLong(bool *ok = nullptr, int base = 10) const`

**作用与语义：**

返回使用底`base`转换为`unsigned long long`的字符串，默认为10，且必须介于2到36之间，即0。如果转换失败，返回0。
如果`ok`未`nullptr`，则通过将*`ok`设为`false`报告失败，成功则将*`ok`设为`true`。
如果 `base` 为 0，则使用 C 语言惯例：如果字符串以“0x”开头，使用进制 16;否则，如果字符串以“0b”开头，使用进制 2;否则，如果字符串以“0”开头，使用进制 8;否则，使用进制 10。
字符串转换总是在“C”区域进行。对于位置相关转换，请使用`QLocale::toULongLong()`。
该函数忽略前置和后置的空白。
注意：在Qt 6.4中加入了对“0b”前缀的支持。

**官方示例：**

```cpp
 QString str = "FF";
 bool ok;

 quint64 hex = str.toULongLong(&ok, 16);    // hex == 255, ok == true
 quint64 dec = str.toULongLong(&ok, 10);    // dec == 0, ok == false
```

### `ushort QString::toUShort(bool *ok = nullptr, int base = 10) const`

**作用与语义：**

返回用基数`base`转换为`unsigned short`的字符串，默认为10，且必须介于2到36之间，即0。如果转换失败，返回0。
如果 `ok` 未`nullptr`，则通过将 *`ok` 设为 `false` 来报告失败，通过将 *`ok` 设为 `true` 来报告失败。
如果`base`为0，则使用C语言的惯例：如果字符串以“0x”开头，使用进制16;否则，如果字符串以“0b”开头，使用进制2;否则，如果字符串以“0”开头，使用进制8;否则，使用进制10。
字符串转换总是在“C”区域进行。对于依赖位置的转换，请使用`QLocale::toUShort()`。
该函数忽略前置和后置的空白。
注意：在Qt 6.4中加入了对“0b”前缀的支持。

**官方示例：**

```cpp
 QString str = "FF";
 bool ok;

 ushort hex = str.toUShort(&ok, 16);     // hex == 255, ok == true
 ushort dec = str.toUShort(&ok, 10);     // dec == 0, ok == false
```

### `QList<uint> QString::toUcs4() const`

**作用与语义：**

返回字符串的UCS-4/UTF-32表示，作为`QList`<uint>。
UTF-32 是 Unicode 编解码器，因此是无损的。该字符串中的所有字符都将编码为 UTF-32。该字符串中任何无效的代码单元序列将被 Unicode 替换字符（`QChar::ReplacementCharacter`，对应于 `U+FFFD`）。
返回的列表并非0终止。

### `QString QString::toUpper() const`

**作用与语义：**

返回字符串的大写副本。
格转换总是在“C”区域进行。对于局部相关的大小写折叠，使用`QLocale::toUpper()`。
注意：在某些情况下，字符串的大写形式可能比原字母更长。
注意：自2024年起，德语官方更倾向于大写 ß（U 00DF 拉丁小写升 S）为 ẞ（U 1E9E 拉丁大写升S）。Qt 的实现遵循 Unicode，但 Unicode 仍强制使用“SS”。如果你需要实现新的德语规则，需要在调用该函数前手动完成`replace(u'ß', u'ẞ')`。

**官方示例：**

```cpp
 QString str = "TeXt";
 str = str.toUpper();        // str == "TEXT"
```

### `QByteArray QString::toUtf8() const`

**作用与语义：**

返回字符串的UTF-8表示，作为`QByteArray`。
UTF-8 是一种 Unicode 编解码器，可以表示 Unicode 字符串中的所有字符，比如 `QString`。

### `qsizetype QString::toWCharArray(wchar_t *array) const`

**作用与语义：**

用该`QString`对象中包含的数据填充`array`。在wchar_t宽度为2字节的平台上（如Windows），数组以UTF-16编码，在wchar_t宽为4字节的平台上（大多数Unix系统）采用UTF-32编码。
调用者必须分配`array`，并包含足够空间容纳整个字符串（分配与字符串长度相同的数组始终足够）。
该函数返回字符串的实际长度，单位为`array`。
注意：该函数不会向数组附加空字符。

### `[noexcept(...), since 6.0] template <typename Needle, typename... Flags> auto QString::tokenize(Needle &&sep, Flags... flags) &&`

**作用与语义：**

在出现这些元素的地方，将字符串拆分为子串视图，并返回`sep`的字符串的懒散序列。
等价于。
但该功能在编译器中未启用 C 17 类模板参数推理（CTAD）时可正常工作。
参见`QStringTokenizer`，了解`sep`和`flags`如何相互作用形成结果。
注意：虽然该函数返回`QStringTokenizer`，但你绝不应明确命名其模板参数。如果你能使用 C 17 类模板参数演绎（CTAD），你可以写道。
（不含模板参数）。如果你不能使用 C 17 CTAD，你必须只将返回值存储在`auto`变量中：
这是因为`QStringTokenizer`的模板参数对返回的具体`tokenize()`重载有非常微妙的依赖，且通常不对应分隔符所用的类型。
注意：（1）除`noexcept(qTokenize(std::declval<const QString &>(), std::forward<Needle>(needle), flags...))`为`true`时外，均为无效。
注意：（2）除`noexcept(qTokenize(std::declval<const QString>(), std::forward<Needle>(needle), flags...))`为`true`时除外。
注意：（3）是除`noexcept(qTokenize(std::declval<QString>(), std::forward<Needle>(needle), flags...))`为`true`时外。

**官方示例：**

```cpp
 return QStringTokenizer{std::forward<Needle>(sep), flags...};
```

### `QString QString::trimmed() const`

**作用与语义：**

返回一个字符串，其开头和结尾的空白都被移除了。
空白空间指`QChar::isSpace()`返回`true`的任何字符。这包括ASCII字符“\t”、“\n”、“\v”、“\f”、“\r'和' '。
与`simplified()`不同，trimmed() 保留内部空白。

**官方示例：**

```cpp
 QString str = "  lots\t of\nwhitespace\r\n ";
 str = str.trimmed();
 // str == "lots\t of\nwhitespace"
```

### `void QString::truncate(qsizetype position)`

**作用与语义：**

截断从索引`position`元素开始并包含的字符串。
如果指定的`position`索引超出字符串末尾，则不会发生任何事。
如果`position`为负，则等价于通过零。

**官方示例：**

```cpp
 QString str = "Vladivostok";
 str.truncate(4);
 // str == "Vlad"
```

### `const QChar *QString::unicode() const`

**作用与语义：**

返回字符串的Unicode表示。结果在字符串被修改前保持有效。
注意：返回字符串可能不是“\0”终止的。使用`size()`来确定数组长度。

### `const ushort *QString::utf16() const`

**作用与语义：**

返回`QString`为一个“\0”终止的无符号短路数组。结果在字符串被修改前保持有效。
返回的字符串按主机字节顺序排列。

### `[static] QString QString::vasprintf(const char *cformat, va_list ap)`

**作用与语义：**

与`asprintf()`等价的方法，但采用va_list `ap`而非变量参数列表。有关`cformat`的解释，请参见`asprintf()`文档。
该方法不调用va_end宏，调用者需负责调用`ap`上的 va_end。

### `[noexcept, since 6.7] QString::operator std::u16string_view() const`

**作用与语义：**

将`QString`对象转换为`std::u16string_view`对象。

### `QString &QString::operator+=(const QString &other)`

**作用与语义：**

将字符串`other`附加到该字符串的末尾，并返回对该字符串的引用。
该操作通常非常快速（常数时间），因为`QString`在字符串数据末尾预先分配额外空间，使数据可以增长而无需每次重新分配整个字符串。

**官方示例：**

```cpp
 QString x = "free";
 QString y = "dom";
 x += y;
 // x == "freedom"
```

### `QString &QString::operator+=(QChar ch)`

**作用与语义：**

在字符串后加上字符`ch`。
注意：该函数会超载 QString：：operator =()。

### `QString &QString::operator+=(QLatin1StringView str)`

**作用与语义：**

附加`str` 查看的拉丁-1字符串。
注意：该函数会超载 QString：：operator =()。

### `[since 6.0] QString &QString::operator+=(QStringView str)`

**作用与语义：**

将字符串视图`str`附加到该字符串上。
注意：该函数会超载 QString：：operator =()。

### `[since 6.5] QString &QString::operator+=(QUtf8StringView str)`

**作用与语义：**

将UTF-8字符串视图`str`附加到该字符串后。
注意：该函数会超载 QString：：operator =()。

### `QString &QString::operator+=(const QByteArray &ba)`

**作用与语义：**

将字节数组`ba`附加到该字符串后。字节数组通过 `fromUtf8()` 函数转换为 Unicode。如果 `ba` 字节数组中嵌入了任何 NUL 字符（'\0'），它们将被包含在变换中。
你可以通过在编译应用程序时定义`QT_NO_CAST_FROM_ASCII`来禁用这个功能。例如，如果你想确保所有用户可见的字符串都通过`QObject::tr()`，这会很有用。
注意：该函数会超载 QString：：operator =()。

### `QString &QString::operator+=(const char *str)`

**作用与语义：**

将字符串 `str` 附加到该字符串上。const 字符指针通过 `fromUtf8()` 函数转换为 Unicode。
你可以通过在编译应用程序时定义`QT_NO_CAST_FROM_ASCII`来禁用这个功能。例如，如果你想确保所有用户可见的字符串都经过`QObject::tr()`，这会很有用。
注意：该函数会超载 QString：：operator =()。

### `[noexcept] QString &QString::operator=(QString &&other)`

**作用与语义：**

Move-assign `other`到这个`QString`实例。

### `[noexcept] QString &QString::operator=(const QString &other)`

**作用与语义：**

将`other`分配到该字符串，并返回对该字符串的引用。

### `QString &QString::operator=(QChar ch)`

**作用与语义：**

设置字符串包含单个字符`ch`。
注意：该函数会超载 QString：：operator=()。

### `QString &QString::operator=(QLatin1StringView str)`

**作用与语义：**

将`str` 所见的拉丁-1字符串分配给该字符串。
注意：该函数会超载 QString：：operator=()。

### `QString &QString::operator=(const QByteArray &ba)`

**作用与语义：**

将`ba`分配到该字符串。字节数组通过 `fromUtf8()` 函数转换为 Unicode。
你可以通过在编译应用时定义`QT_NO_CAST_FROM_ASCII`来禁用该操作符。例如，如果你想确保所有用户可见字符串都经过`QObject::tr()`，这非常有用。
注意：该函数会超载 QString：：operator=()。

### `QString &QString::operator=(const char *str)`

**作用与语义：**

将`str`分配给该字符串。cont char 指针通过 `fromUtf8()` 函数转换为 Unicode。
你可以通过在编译应用时定义 `QT_NO_CAST_FROM_ASCII` 或 `QT_RESTRICTED_CAST_FROM_ASCII` 来禁用该操作符。例如，如果你想确保所有用户可见字符串都通过 `QObject::tr()`，这会非常有用。
注意：该函数会超载 QString：：operator=()。

### `QChar &QString::operator[](qsizetype position)`

**作用与语义：**

返回字符串指定`position`的字符作为可修改的引用。

**官方示例：**

```cpp
 QString str;

 if (str[0] == QChar('?'))
     str[0] = QChar('_');
```

### `const QChar QString::operator[](qsizetype position) const`

**作用与语义：**

注意：该函数会使 QString：：operator[]() 重载。

### `[since 6.1] template <typename T> qsizetype erase(QString &s, const T &t)`

**作用与语义：**

从字符串`s`中移除所有比较为`t`的元素。返回移除的元素数量（如果有的话）。

### `[since 6.1] template <typename Predicate> qsizetype erase_if(QString &s, Predicate pred)`

**作用与语义：**

从字符串`s`中移除所有谓词 `pred` 返回为真元素。返回移除的元素数量（如有）。

### `[noexcept] bool operator!=(const QByteArray &lhs, const QString &rhs)`

**作用与语义：**

如果字节数组 `lhs` 不等于 `rhs` 的 UTF-8 编码，则返回 `QT_NO_CAST_FROM_ASCII`；否则返回 `false`。
比较区分大小写。
您可以在编译应用程序时通过定义 `QT_NO_CAST_FROM_ASCII` 来禁用此运算符。如果希望在进行比较之前将字节数组转换为 `QString`，则需要显式调用 `QString::fromUtf8()`、`QString::fromLatin1()` 或 `QString::fromLocal8Bit()`。

### `[noexcept] bool operator!=(const QString &lhs, const QString &rhs)`

**作用与语义：**

如果字符串 `lhs` 不等于字符串 `rhs`，则返回 `true`；否则返回 `false`。

### `[noexcept] bool operator!=(const char *const &lhs, const QString &rhs)`

**作用与语义：**

返回`true`如果`lhs`不等于`rhs`; 否则返回 `false`。
对于 `lhs` != 0，这等同于 `compare(` `lhs`, `rhs` `) != 0`. 请注意，没有字符串等于 `lhs`为0。

### `[noexcept] bool operator!=(const QString &lhs, const QByteArray &rhs)`

**作用与语义：**

`rhs`字节数组被转换为`QUtf8StringView`。如果字节数组中嵌入了任何NUL字符（'\0'），它们将被包含在变换中。
你可以通过在编译应用时定义`QT_NO_CAST_FROM_ASCII`来禁用该操作符。例如，如果你想确保所有用户可见的字符串都通过`QObject::tr()`，这会非常有用。
注意：该函数会超载 QString：：operator！=()。

### `[noexcept] bool operator!=(const QString &lhs, const QLatin1StringView &rhs)`

**作用与语义：**

如果字符串 `lhs` 不等于字符串 `rhs`，则返回 `true`。否则返回 `false`。
注意：此函数重载了 QString::operator!=()。

### `[noexcept] bool operator!=(const QString &lhs, const char *const &rhs)`

**作用与语义：**

`rhs` const char 指针被转换为 `QUtf8StringView`。 你可以在编译应用程序时通过定义 `QT_NO_CAST_FROM_ASCII` 来禁用此操作符。例如，如果你希望确保所有用户可见的字符串都经过 `QObject::tr()`，这会很有用。 注意：此函数重载了 QString::operator!=()。

### `[noexcept, since 6.4] QString operator""_s(const char16_t *str, size_t size)`

**作用与语义：**

字面操作符，将char16_t字符串的前`size`字符创建`QString`，字面 `str`。
`QString`在编译时创建，生成的字符串数据存储在编译对象文件的只读段中。重复的文字可以共享相同的只读内存。此功能可与`QStringLiteral`互换，但当代码中存在多个字符串文字时，可以省去输入。
以下代码创建`QString`：

**官方示例：**

```cpp
 using namespace Qt::StringLiterals;

 auto str = u"hello"_s;
```

### `[since 6.9] QString operator+(const QString &lhs, QStringView rhs)`

**作用与语义：**

返回一个字符串，该字符串是 `lhs` 和 `rhs` 连接的结果。

### `QString operator+(QString &&s1, const QString &s2)`

**作用与语义：**

返回一个字符串，该字符串是 `lhs` 和 `rhs` 连接的结果。

### `QString operator+(const QString &s1, const char *s2)`

**作用与语义：**

返回一个字符串，该字符串是 `s1` 和 `s2` 连接的结果。

### `QString operator+(const char *s1, const QString &s2)`

**作用与语义：**

返回一个字符串，该字符串是 `s1` 和 `s2` 连接的结果。

### `[noexcept] bool operator<(const QByteArray &lhs, const QString &rhs)`

**作用与语义：**

如果字节数组 `lhs` 在词法上小于 `rhs` 的 UTF-8 编码，则返回 `true`；否则返回 `false`。比较区分大小写。您可以在编译应用程序时通过定义 `QT_NO_CAST_FROM_ASCII` 来禁用此运算符。如果您希望在进行比较之前将字节数组转换为 `QString`，则需要显式调用 `QString::fromUtf8()`、`QString::fromLatin1()` 或 `QString::fromLocal8Bit()`。

### `[noexcept] bool operator<(const char *const &lhs, const QString &rhs)`

**作用与语义：**

如果 `lhs` 在字面上小于 `rhs`，则返回 `true`；否则返回 `false`。对于 `lhs` != 0，这相当于 `compare(lhs, rhs) < 0`。

### `[noexcept] bool operator<(const QLatin1StringView &lhs, const QString &rhs)`

**作用与语义：**

如果 `lhs` 在词汇上小于 `rhs`，则返回 `true`；否则返回 `false`。
注意：此函数重载了 `QString::operator<()`。

### `[noexcept] bool operator<(const QString &lhs, const QByteArray &rhs)`

**作用与语义：**

`rhs`字节数组被转换为`QUtf8StringView`。如果字节数组中嵌入了任何NUL字符（'\0'），它们将被包含在变换中。
你可以在编译应用时禁用这个操作符`QT_NO_CAST_FROM_ASCII`。例如，如果你想确保所有用户可见字符串都通过`QObject::tr()`，这会很有用。
注意：该功能会超载`QString::operator<()`。

### `[noexcept] bool operator<(const QString &lhs, const QLatin1StringView &rhs)`

**作用与语义：**

如果 `lhs` 在词汇上小于 `rhs`，则返回 `true`；否则返回 `false`。
注意：此函数重载了 `QString::operator<()`。

### `[noexcept] bool operator<(const QString &lhs, const QString &rhs)`

**作用与语义：**

如果字符串 `lhs` 在字典序上小于字符串 `rhs`，则返回 `true`；否则返回 `false`。
注意：此函数重载了 `QString::operator<()`。

### `[noexcept] bool operator<(const QString &lhs, const char *const &rhs)`

**作用与语义：**

如果字符串 `lhs` 在词法上小于字符串 `rhs`，则返回 `rhs`。否则返回 `false`。
`rhs` 常量字符指针被转换为 `QUtf8StringView`。
通过在编译应用程序时定义 `QT_NO_CAST_FROM_ASCII`，可以禁用此操作符。如果你希望确保所有用户可见字符串都通过 `QObject::tr()`，这会很有用。
注意：此函数重载了 `QString::operator<()`。

### `QDataStream &operator<<(QDataStream &stream, const QString &string)`

**作用与语义：**

将给定`string`写入指定的`stream`。

### `[noexcept] bool operator<=(const QByteArray &lhs, const QString &rhs)`

**作用与语义：**

如果字节数组`lhs`词汇上小于或等于`rhs`的UTF-8编码，返回`true`;否则返回`false`。
比较时要区分大小写。
你可以通过在编译应用时定义`QT_NO_CAST_FROM_ASCII`来禁用这个操作符。然后如果你想在比较前将字节数组转换为`QString`，则需要明确调用`QString::fromUtf8()`、`QString::fromLatin1()`或`QString::fromLocal8Bit()`。

### `[noexcept] bool operator<=(const QString &lhs, const QString &rhs)`

**作用与语义：**

如果字符串 `lhs` 在字面上小于或等于字符串 `rhs`，则返回 `true`；否则返回 `false`。

### `[noexcept] bool operator<=(const char *const &lhs, const QString &rhs)`

**作用与语义：**

如果 `lhs` 在词法上小于或等于 `rhs`，则返回 `true`；否则返回 `false`。对于 `lhs` != 0，这等同于 `compare(lhs, rhs) <= 0`。

### `[noexcept] bool operator<=(const QLatin1StringView &lhs, const QString &rhs)`

**作用与语义：**

如果 `lhs` 在字面上小于或等于 `rhs`，则返回 `true`；否则返回 `false`。
注意：此函数重载了 QString::operator<=()。

### `[noexcept] bool operator<=(const QString &lhs, const QByteArray &rhs)`

**作用与语义：**

`rhs`字节数组被转换为`QUtf8StringView`。如果字节数组中嵌入任何NUL字符（'\0'），它们将被包含在变换中。
你可以通过在编译应用时定义`QT_NO_CAST_FROM_ASCII`来禁用这个操作符。例如，如果你想确保所有用户可见的字符串都通过`QObject::tr()`，这会非常有用。
注意：该函数会超载 QString：：operator<=()。

### `[noexcept] bool operator<=(const QString &lhs, const QLatin1StringView &rhs)`

**作用与语义：**

如果 `lhs` 在字面上小于或等于 `rhs`，则返回 `true`；否则返回 `false`。
注意：此函数重载了 QString::operator<=()。

### `[noexcept] bool operator<=(const QString &lhs, const char *const &rhs)`

**作用与语义：**

`rhs` const char 指针被转换为 `QUtf8StringView`。 你可以在编译应用程序时通过定义 `QT_NO_CAST_FROM_ASCII` 来禁用此操作符。例如，如果你希望确保所有用户可见的字符串都经过 `QObject::tr()`，这会很有用。 注意：此函数重载了 QString::operator<=()。

### `[noexcept] bool operator==(const QByteArray &lhs, const QString &rhs)`

**作用与语义：**

如果字节数组 `lhs` 等于 `rhs` 的 UTF-8 编码，返回 `true`;否则返回 `false`。
比较时要区分大小写。
你可以在编译应用时定义`QT_NO_CAST_FROM_ASCII`来禁用这个操作符。然后如果你想在比较前将字节数组转换为`QString`，就需要明确调用`QString::fromUtf8()`、`QString::fromLatin1()`或`QString::fromLocal8Bit()`。

### `[noexcept] bool operator==(const QLatin1StringView &lhs, const QString &rhs)`

**作用与语义：**

如果 `lhs` 等于 `rhs`，则返回 `true`；否则返回 `false`。
注意：此函数重载了 QString::operator==()。

### `[noexcept] bool operator==(const QString &lhs, const QByteArray &rhs)`

**作用与语义：**

`rhs`字节数组被转换为`QUtf8StringView`。
你可以通过在编译应用时定义`QT_NO_CAST_FROM_ASCII`来禁用这个操作符。例如，如果你想确保所有用户可见的字符串都经过`QObject::tr()`，这会非常有用。
如果字符串`lhs`词汇上等于`rhs`，则返回`true`。否则返回`false`。
注意：该函数会超载 QString：：operator==()。

### `[noexcept] bool operator==(const QString &lhs, const QLatin1StringView &rhs)`

**作用与语义：**

如果 `lhs` 等于 `rhs`，则返回 `true`；否则返回 `false`。
注意：此函数重载了 QString::operator==()。

### `[noexcept] bool operator==(const QString &lhs, const QString &rhs)`

**作用与语义：**

如果字符串 `lhs` 等于字符串 `rhs`，则返回 `true`；否则返回 `false`。
注意：此函数将 null 字符串视为与空字符串相同，更多详情请参见 Null 和空字符串的区别。
注意：此函数重载了 QString::operator==()。

### `[noexcept] bool operator==(const QString &lhs, const char *const &rhs)`

**作用与语义：**

`rhs` const char 指针被转换为 `QUtf8StringView`。 你可以在编译应用程序时通过定义 `QT_NO_CAST_FROM_ASCII` 来禁用此操作符。例如，如果你希望确保所有用户可见的字符串都经过 `QObject::tr()`，这会很有用。 注意：此函数重载了 QString::operator==()。

### `[noexcept] bool operator==(const char *const &lhs, const QString &rhs)`

**作用与语义：**

如果 `lhs` 等于 `rhs`，则返回 `lhs`；否则返回 `false`。注意，没有字符串等于 `lhs` 为 0。等价于 `lhs != 0 && compare(lhs, rhs) == 0`。注意：此函数重载了 QString::operator==()。

### `[noexcept] bool operator>(const QByteArray &lhs, const QString &rhs)`

**作用与语义：**

如果字节数组`lhs`词汇大于`rhs`的UTF-8编码，返回`true`;否则返回`false`。
比较时要区分大小写。
你可以在编译应用时定义`QT_NO_CAST_FROM_ASCII`来禁用这个操作符。然后如果你想在比较前将字节数组转换为`QString`，就需要明确调用`QString::fromUtf8()`、`QString::fromLatin1()`或`QString::fromLocal8Bit()`。

### `[noexcept] bool operator>(const QString &lhs, const QString &rhs)`

**作用与语义：**

如果字符串 `lhs` 在字面上大于字符串 `rhs`，则返回 `true`；否则返回 `false`。

### `[noexcept] bool operator>(const char *const &lhs, const QString &rhs)`

**作用与语义：**

如果 `lhs` 在词法上大于 `rhs`，则返回 `true`；否则返回 `false`。等同于 `compare(lhs, rhs) > 0`。

### `[noexcept] bool operator>(const QLatin1StringView &lhs, const QString &rhs)`

**作用与语义：**

如果 `lhs` 在词汇上大于 `rhs`，则返回 `true`；否则返回 `false`。
注意：此函数重载了 `QString::operator>()`。

### `[noexcept] bool operator>(const QString &lhs, const QByteArray &rhs)`

**作用与语义：**

`rhs` 字节数组被转换为 `QUtf8StringView`。如果字节数组中嵌入了任何 NUL 字符 ('\0')，它们将在转换中被包含。 你可以在编译应用程序时通过定义 `QT_NO_CAST_FROM_ASCII` 来禁用此操作符。例如，如果你希望确保所有用户可见的字符串都经过 `QObject::tr()`，这会很有用。 注意：此函数重载了 `QString::operator>()`。

### `[noexcept] bool operator>(const QString &lhs, const QLatin1StringView &rhs)`

**作用与语义：**

如果 `lhs` 在词汇上大于 `rhs`，则返回 `true`；否则返回 `false`。
注意：此函数重载了 `QString::operator>()`。

### `[noexcept] bool operator>(const QString &lhs, const char *const &rhs)`

**作用与语义：**

`rhs` const char 指针被转换为 `QUtf8StringView`。 你可以在编译应用程序时通过定义 `QT_NO_CAST_FROM_ASCII` 来禁用此操作符。例如，如果你希望确保所有用户可见的字符串都经过 `QObject::tr()`，这会很有用。 注意：此函数重载了 `QString::operator>()`。

### `[noexcept] bool operator>=(const QByteArray &lhs, const QString &rhs)`

**作用与语义：**

如果字节数组`lhs`大于或等于`rhs`的UTF-8编码，返回`true`;否则返回`false`。
比较时要区分大小写。
你可以在编译应用时定义`QT_NO_CAST_FROM_ASCII`来禁用这个操作符。然后如果你想在比较前将字节数组转换为`QString`，就需要明确调用`QString::fromUtf8()`、`QString::fromLatin1()`或`QString::fromLocal8Bit()`。

### `[noexcept] bool operator>=(const QString &lhs, const QString &rhs)`

**作用与语义：**

如果字符串 `lhs` 在词汇上大于或等于字符串 `rhs`，则返回 `true`；否则返回 `false`。

### `[noexcept] bool operator>=(const char *const &lhs, const QString &rhs)`

**作用与语义：**

如果 `lhs` 在词法上大于或等于 `rhs`，则返回 `true`；否则返回 `false`。对于 `lhs` != 0，这等同于 `compare(lhs, rhs) >= 0`。

### `[noexcept] bool operator>=(const QLatin1StringView &lhs, const QString &rhs)`

**作用与语义：**

如果 `lhs` 在字典序上大于或等于 `rhs`，则返回 `true`；否则返回 `false`。
注意：此函数重载了 QString::operator>=()。

### `[noexcept] bool operator>=(const QString &lhs, const QByteArray &rhs)`

**作用与语义：**

`rhs` 字节数组被转换为 `QUtf8StringView`。如果字节数组中嵌入了任何 NUL 字符 ('\0')，它们将在转换中被包含。 你可以在编译应用程序时通过定义 `QT_NO_CAST_FROM_ASCII` 来禁用此操作符。例如，如果你希望确保所有用户可见的字符串都经过 `QObject::tr()`，这会很有用。 注意：此函数重载了 QString::operator>=()。

### `[noexcept] bool operator>=(const QString &lhs, const QLatin1StringView &rhs)`

**作用与语义：**

如果 `lhs` 在字典序上大于或等于 `rhs`，则返回 `true`；否则返回 `false`。
注意：此函数重载了 QString::operator>=()。

### `[noexcept] bool operator>=(const QString &lhs, const char *const &rhs)`

**作用与语义：**

`rhs` const char 指针被转换为 `QUtf8StringView`。 你可以在编译应用程序时通过定义 `QT_NO_CAST_FROM_ASCII` 来禁用此操作符。例如，如果你希望确保所有用户可见的字符串都经过 `QObject::tr()`，这会很有用。 注意：此函数重载了 QString::operator>=()。

### `QDataStream &operator>>(QDataStream &stream, QString &string)`

**作用与语义：**

将指定`stream`中的字符串读取到给定的`string`。

### `QStringLiteral(str)`

**作用与语义：**

宏在编译时从字符串的字面值`str`生成`QString`数据。在这种情况下，从字符串创建`QString`是免费的，生成的字符串数据存储在编译后的对象文件的只读段中。
如果你有类似这样的代码：
然后创建一个临时的`QString`，作为`hasAttribute`函数参数传递。这可能相当昂贵，因为涉及内存分配以及将数据复制/转换成`QString`内部编码。
通过使用 QStringLiteral 可以避免此成本：
在这种情况下，`QString`的内部数据将在编译时生成;运行时不会进行转换或分配。
使用QStringLiteral代替双引号的普通C字符串文字，可以显著加快从编译时已知数据创建`QString`实例的速度。
注意：当字符串传递给带有重载`QLatin1StringView`的函数时，`QLatin1StringView`仍然比QStringLiteral更高效，而该重载避免了`QString`转换。例如，QString：：operator==()可以直接与`QLatin1StringView`进行比较：
注意：有些编译器在编码包含 US-ASCII 字符集外字符的字符串时存在错误。在这些情况下，确保字符串前缀加上 `u`。否则是可选的。
注意：QStringLiteral 可与操作符“”“_s互换。后者在代码中存在多个字符串文字时节省了输入。

**官方示例：**

```cpp
 // hasAttribute takes a QString argument
 if (node.hasAttribute("http-contents-length")) {
     //...
 }
```

### `QT_NO_CAST_FROM_ASCII`

**作用与语义：**

禁用从 8 位字符串（`char *`）到 Unicode QStrings 的自动转换，以及从 8 位 `char`类型（`char` 和 `unsigned char`）转换为 `QChar`。

### `QT_NO_CAST_TO_ASCII`

**作用与语义：**

禁用从`QString`位字符串自动转换为8位字符串（`char *`）。

### `QT_RESTRICTED_CAST_FROM_ASCII`

**作用与语义：**

禁用大部分自动从源文字和8位数据转换为Unicode QStrins，但允许使用`QChar(char)`和`QString(const char (&ch)[N]`构造函数以及`QString::operator=(const char (&ch)[N])`赋值运算符。这提供了`QT_NO_CAST_FROM_ASCII`大部分的类型安全优势，但不需要用户代码用`QLatin1Char`、`QLatin1StringView`等格式封装字符和字符串文字。
使用该宏与7位范围外的源字符串、非文字字符串或带有嵌入NUL字符的文字一起使用是未定义的。

### `const char *qPrintable(const QString &str)`

**作用与语义：**

返回`str`为`const char *`。这相当于`str`。`toLocal8Bit()`。`constData()`。
char 指针在使用 qPrintable() 的语句之后将失效。这是因为 `QString::toLocal8Bit()` 返回的数组会超出作用域。
注意：`qDebug()`、`qInfo()`、`qWarning()`、`qCritical()` `qFatal()` 期望 %s 参数采用 UTF-8 编码，而 qPrintable() 则转换为本地 8 位编码。因此，`qUtf8Printable()` 应用于日志字符串，而非 qPrintable()。

### `const wchar_t *qUtf16Printable(const QString &str)`

**作用与语义：**

`str`以`const ushort *`身份回归，但为避免警告而施放为`const wchar_t *`。这相当于`str`。`utf16()`加上一些施法。
你唯一能用这个宏的返回值做的就是传给`QString::asprintf()`用于`%ls`转换。特别是，返回值不是一个有效的`const wchar_t*`！
一般来说，指针在使用 qUtf16Printable() 的语句之后将失效。这是因为指针可能来自临时表达式，该表达式会落入作用域。

**官方示例：**

```cpp
 qWarning("%ls: %ls", qUtf16Printable(key), qUtf16Printable(value));
```

### `const char *qUtf8Printable(const QString &str)`

**作用与语义：**

以`const char *`的形式返回`str`。这相当于`str`。`toUtf8()`。`constData()`。
字符指针在使用 qUtf8Printable() 的语句后将失效。这是因为 的 数组返回`QString::toUtf8()`会脱离作用域。

**官方示例：**

```cpp
 qWarning("%s: %s", qUtf8Printable(key), qUtf8Printable(value));
```

### `ConstIterator`

**作用与语义：**

Qt风格的同义词`QString::const_iterator`。

### `Iterator`

**作用与语义：**

Qt风格的`QString::iterator`同义词。

### `enum SectionFlag { SectionDefault, SectionSkipEmpty, SectionIncludeLeadingSep, SectionIncludeTrailingSep, SectionCaseInsensitiveSeps }`

**作用与语义：**

该枚举指定了可用于影响`section()`函数在分离符和空字段行为方面各方面的标志。
- `QString::SectionDefault`：`0x00`;空字段被计数，不包括前置和后置分隔符，并对分隔符进行大小写敏感比较。
- `QString::SectionSkipEmpty`：`0x01`;将空字段视为不存在，即在起点和结束时不考虑空字段。
- `QString::SectionIncludeLeadingSep`：`0x02`;在结果字符串中包含前置分隔符（如有）。
- `QString::SectionIncludeTrailingSep`：`0x04`;在结果字符串中包含尾部分隔符（如有）。
- `QString::SectionCaseInsensitiveSeps`：`0x08`;对分隔符进行不敏感的比较。
SectionFlags 类型是 QFlags 的 typedef<SectionFlag>。它存储 SectionFlag 值的 OR 组合。

### `flags SectionFlags`

**作用与语义：**

该枚举指定了可用于影响`section()`函数在分离符和空字段行为方面各方面的标志。
- `QString::SectionDefault`：`0x00`;空字段被计数，不包括前置和后置分隔符，并对分隔符进行大小写敏感比较。
- `QString::SectionSkipEmpty`：`0x01`;将空字段视为不存在，即在起点和结束时不考虑空字段。
- `QString::SectionIncludeLeadingSep`：`0x02`;在结果字符串中包含前置分隔符（如有）。
- `QString::SectionIncludeTrailingSep`：`0x04`;在结果字符串中包含尾部分隔符（如有）。
- `QString::SectionCaseInsensitiveSeps`：`0x08`;对分隔符进行不敏感的比较。
SectionFlags 类型是 QFlags 的 typedef<SectionFlag>。它存储 SectionFlag 值的 OR 组合。

### `const_iterator`

**作用与语义：**

只读的 STL 风格正向迭代器类型，用于从 `begin()`/`cbegin()` 遍历到 `end()`/`cend()`，不能通过它修改元素。

### `const_pointer`

**作用与语义：**

QString：：const_pointer typedef 提供了一个 STL 风格的 cont 指针，指向一个`QString`元素（`QChar`）。

### `const_reference`

**作用与语义：**

元素只读引用类型，适合在不复制元素且不允许修改时作为返回值或局部别名使用。

### `const_reverse_iterator`

**作用与语义：**

只读的 STL 风格反向迭代器类型，用于从 `rbegin()`/`crbegin()` 反向遍历到 `rend()`/`crend()`。

### `difference_type`

**作用与语义：**

表示两个迭代器之间距离的有符号整数类型，主要供标准库迭代器算法和泛型代码使用。

### `iterator`

**作用与语义：**

可修改元素的 STL 风格正向迭代器类型；容器发生分离或结构性修改后，已有迭代器可能失效。

### `pointer`

**作用与语义：**

QString：:p ointer typedef 提供一个 STL 风格的指针指向一个`QString`元素（`QChar`）。

### `reference`

**作用与语义：**

元素可写引用类型；它直接引用字符串或容器内部元素，所属对象修改、分离或销毁后不能继续使用。

### `reverse_iterator`

**作用与语义：**

可修改元素的 STL 风格反向迭代器类型；容器发生分离或结构性修改后，已有迭代器可能失效。

### `size_type`

**作用与语义：**

表示字符串长度、容量或索引范围的整数类型；写泛型代码时用它与本类的尺寸 API 保持类型一致。

### `value_type`

**作用与语义：**

表示单个元素的类型；对 `QString` 而言元素是一个 UTF-16 码元 `QChar`，不一定等于完整的 Unicode 字符。

### `QString chopped(qsizetype len) const &`

**作用与语义：**

返回一个字符串，该字符串包含此字符串的最左边 `size()` - `len` 个字符。
注意：如果 `len` 为负数或大于 `size()`，则行为未定义。

### `(since 6.0) QString first(qsizetype n) const &`

**作用与语义：**

返回一个字符串，该字符串包含此字符串的前 `n` 个字符（也就是说，从此字符串的开头一直到但不包括索引位置 `n` 处的元素）。
注意：当 `n` < 0 或 `n` > `size()` 时，其行为未定义。

**官方示例：**

```cpp
 QString x = "Pineapple";
 QString y = x.first(4);      // y == "Pine"
```

### `(since 6.0) QString last(qsizetype n) const &`

**作用与语义：**

返回包含该字符串最后`n`字符的字符串。
注意：当`n` <0或`n` > `size()`时，行为未定义。

**官方示例：**

```cpp
 QString x = "Pineapple";
 QString y = x.last(5);      // y == "apple"
```

### `QString left(qsizetype n) const &`

**作用与语义：**

返回一个子串，包含该字符串最左边`n`个字符（即从字符串开头到索引位置`n`的元素，但不包括）。
如果你知道`n`不能越界，就用新代码中的`first()`，因为它更快。
如果 `n` 大于或等于 `size()`，或小于 0，则返回整个字符串。

### `(since 6.8) qsizetype max_size() const`

**作用与语义：**

它返回字符串理论上能容纳的最大元素数。实际上，这个数量可以更小，受限于系统可用的内存容量。

### `QString mid(qsizetype position, qsizetype n = -1) const &`

**作用与语义：**

返回包含该字符串的`n`个字符的字符串，从指定的`position`索引开始，直到索引位置`position` `n`的元素，但不包括。
如果你知道`position`和`n`不能越界，就用新代码中的`sliced()`，因为这样更快。
如果`position`索引超过字符串长度，返回空字符串。如果字符串中从给定`position`开始的字符少于`n`个字符，`n`或者默认值为-1，函数返回指定`position`中可用的所有字符。

### `(since 6.10) QString nullTerminated() const &`

**作用与语义：**

返回该字符串的副本，且始终为空终止。

### `QString right(qsizetype n) const &`

**作用与语义：**

返回包含该字符串最右`n`字符的子串。
如果你知道`n`不能越界，就用新代码中的`last()`，因为这样更快。
如果`n`大于或等于`size()`或小于零，则返回整个字符串。

### `(since 6.0) QString sliced(qsizetype pos, qsizetype n) const &`

**作用与语义：**

返回一个字符串，该字符串包含从位置 `pos` 开始直到其结尾的部分。注意：当 `pos` < 0 或 `pos` > `size()` 时，其行为未定义。

### `(since 6.0) QString sliced(qsizetype pos) const &`

**作用与语义：**

返回一个字符串，该字符串包含从位置 `pos` 开始直到其结尾的部分。注意：当 `pos` < 0 或 `pos` > `size()` 时，其行为未定义。

### `(since 6.0) auto tokenize(Needle &&sep, Flags... flags) const &&`

**作用与语义：**

在出现这些元素的地方，将字符串拆分为子串视图，并返回`sep`的字符串的懒散序列。
等价于。
但该功能在编译器中未启用 C 17 类模板参数推理（CTAD）时可正常工作。
参见`QStringTokenizer`，了解`sep`和`flags`如何相互作用形成结果。
注意：虽然该函数返回`QStringTokenizer`，但你绝不应明确命名其模板参数。如果你能使用 C 17 类模板参数演绎（CTAD），你可以写道。
（不含模板参数）。如果你不能使用 C 17 CTAD，你必须只将返回值存储在`auto`变量中：
这是因为`QStringTokenizer`的模板参数对返回的具体`tokenize()`重载有非常微妙的依赖，且通常不对应分隔符所用的类型。
注意：（1）除`noexcept(qTokenize(std::declval<const QString &>(), std::forward<Needle>(needle), flags...))`为`true`时外，均为无效。
注意：（2）除`noexcept(qTokenize(std::declval<const QString>(), std::forward<Needle>(needle), flags...))`为`true`时除外。
注意：（3）是除`noexcept(qTokenize(std::declval<QString>(), std::forward<Needle>(needle), flags...))`为`true`时外。

**官方示例：**

```cpp
 return QStringTokenizer{std::forward<Needle>(sep), flags...};
```

### `(since 6.9) QString operator+(QStringView lhs, const QString &rhs)`

**作用与语义：**

返回一个字符串，该字符串是将 `s1` 和 `s2` 连接的结果（`s2` 使用 `QString::fromUtf8()` 函数转换为 Unicode）。

### `QString operator+(const QString &s1, const QString &s2)`

**作用与语义：**

返回一个字符串，该字符串是将 `s1` 和 `s2` 连接的结果（`s1` 使用 `QString::fromUtf8()` 函数转换为 Unicode）。

## 6. 深入实践与常见坑

### 生命周期和资源边界

值对象由作用域、容器或调用者管理，不使用 parent 和 deleteLater。跨线程传递副本通常比传递 QObject 安全，但共享数据在写入时仍可能发生复制，性能和内存峰值要结合数据规模判断。

### 状态和错误边界

重点区分空值、无效值、默认值和已初始化值。例如空字符串、空 URL、null 图像和无效索引不一定表示同一件事；转换函数的失败结果要通过对应的状态查询确认。

### 线程边界

值类型本身通常可以复制后跨线程传递；不要把 data()/bits()/constData() 得到的指针当成跨线程长期有效的所有权。大对象频繁写入会触发 detach，应避免不必要的复制和格式转换。

### 最容易出现的错误

不要把 QString 当作 UTF-8 字节数组；QStringLiteral 和 fromUtf8/fromLocal8Bit 的语义不同；拼接大量字符串时要考虑 reserve 或 QStringBuilder。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QString` 所属机制类型：Qt 值类型与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
