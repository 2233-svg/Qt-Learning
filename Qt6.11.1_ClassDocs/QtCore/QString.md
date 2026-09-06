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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 368 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `QString::ConstIterator`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QString` 的配置属性。初始化或状态切换时通过 `setConstIterator(...)` 设置，之后用 `ConstIterator()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:ConstIterator`。
- 属性名：`QString`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString::Iterator`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QString` 的配置属性。初始化或状态切换时通过 `setIterator(...)` 设置，之后用 `Iterator()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:Iterator`。
- 属性名：`QString`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QString::NormalizationForm`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QString` 暴露的类型声明 `Normalization、Form`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:NormalizationForm`。
- 属性名：`QString`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QString::SectionFlagflags QString::SectionFlags`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QString` 暴露的类型声明 `Section、Flagflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:SectionFlagflags QString::SectionFlags`。
- 属性名：`QString`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString::const_iterator`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QString` 的配置属性。初始化或状态切换时通过 `setConst_iterator(...)` 设置，之后用 `const_iterator()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:const_iterator`。
- 属性名：`QString`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString::const_pointer`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QString` 的配置属性。初始化或状态切换时通过 `setConst_pointer(...)` 设置，之后用 `const_pointer()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:const_pointer`。
- 属性名：`QString`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString::const_reverse_iterator`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QString` 的配置属性。初始化或状态切换时通过 `setConst_reverse_iterator(...)` 设置，之后用 `const_reverse_iterator()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:const_reverse_iterator`。
- 属性名：`QString`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString::iterator`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QString` 的配置属性。初始化或状态切换时通过 `setIterator(...)` 设置，之后用 `iterator()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:iterator`。
- 属性名：`QString`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString::pointer`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QString` 的配置属性。初始化或状态切换时通过 `setPointer(...)` 设置，之后用 `pointer()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:pointer`。
- 属性名：`QString`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString::reverse_iterator`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QString` 的配置属性。初始化或状态切换时通过 `setReverse_iterator(...)` 设置，之后用 `reverse_iterator()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:reverse_iterator`。
- 属性名：`QString`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] QString::QString()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QString` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString::QString(QChar ch)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QString` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `ch`：类型为 `QChar`。没有默认值，调用时必须提供。传入 `QChar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString::QString(QLatin1StringView str)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QString` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `str`：类型为 `QLatin1StringView`。没有默认值，调用时必须提供。传入 `QLatin1StringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit, since 6.8] QString::QString(QStringView sv)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QString` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `sv`：类型为 `QStringView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString::QString(const QByteArray &ba)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QString` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `ba`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString::QString(const char *str)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QString` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `str`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.1] QString::QString(const char8_t *str)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QString` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `str`：类型为 `const char8_t *`。没有默认值，调用时必须提供。传入 `const char8_t *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QString::QString(const QChar *unicode, qsizetype size = -1)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QString` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `unicode`：类型为 `const QChar *`。没有默认值，调用时必须提供。传入 `const QChar *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `size`：类型为 `qsizetype`。默认值为 `-1`。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString::QString(qsizetype size, QChar ch)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QString` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `size`：类型为 `qsizetype`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。
- 参数 `ch`：类型为 `QChar`。没有默认值，调用时必须提供。传入 `QChar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QString::QString(const QString &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QString` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `const QString &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QString::QString(QString &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QString` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `QString &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QString::~QString()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QString` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::append(const QString &str)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QString` 添加依赖、数据或子对象的 API `append`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `str`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::append(QChar ch)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QString` 添加依赖、数据或子对象的 API `append`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `ch`：类型为 `QChar`。没有默认值，调用时必须提供。传入 `QChar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::append(QLatin1StringView str)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QString` 添加依赖、数据或子对象的 API `append`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `str`：类型为 `QLatin1StringView`。没有默认值，调用时必须提供。传入 `QLatin1StringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] QString &QString::append(QStringView v)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QString` 添加依赖、数据或子对象的 API `append`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `v`：类型为 `QStringView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.5] QString &QString::append(QUtf8StringView str)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QString` 添加依赖、数据或子对象的 API `append`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `str`：类型为 `QUtf8StringView`。没有默认值，调用时必须提供。传入 `QUtf8StringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::append(const QByteArray &ba)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QString` 添加依赖、数据或子对象的 API `append`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `ba`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::append(const char *str)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QString` 添加依赖、数据或子对象的 API `append`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `str`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::append(const QChar *str, qsizetype len)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QString` 添加依赖、数据或子对象的 API `append`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `str`：类型为 `const QChar *`。没有默认值，调用时必须提供。传入 `const QChar *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `len`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename... Args> QString QString::arg(Args &&... args) const`

**API 类别：** 成员函数说明

**中文解读：** `QString::arg` 用于计算、查询或取得与“arg”相关的操作。调用时要先确认当前状态和 `args` 的有效范围；返回类型是 `template <typename... Args> QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename... Args> QString`。
- 参数 `args`：类型为 `Args &&...`。没有默认值，调用时必须提供。传入 `Args &&...` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename T, QString::if_string_like<T> = true> QString QString::arg(const T &a, int fieldWidth = 0, QChar fillChar = u' ') const`

**API 类别：** 成员函数说明

**中文解读：** `QString::arg` 用于计算、查询或取得与“arg”相关的操作。调用时要先确认当前状态和 `a`、`fieldWidth`、`fillChar` 的有效范围；返回类型是 `template <typename T, QString::if_string_like<T> = true> QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename T, QString::if_string_like<T> = true> QString`。
- 参数 `a`：类型为 `const T &`。没有默认值，调用时必须提供。传入 `const T &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `fieldWidth`：类型为 `int`。默认值为 `0`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `fillChar`：类型为 `QChar`。默认值为 `u' '`。传入 `QChar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename T, QString::if_integral_non_char<T> = true> QString QString::arg(T a, int fieldWidth = 0, int base = 10, QChar fillChar = u' ') const`

**API 类别：** 成员函数说明

**中文解读：** `QString::arg` 用于计算、查询或取得与“arg”相关的操作。调用时要先确认当前状态和 `a`、`fieldWidth`、`base`、`fillChar` 的有效范围；返回类型是 `template <typename T, QString::if_integral_non_char<T> = true> QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename T, QString::if_integral_non_char<T> = true> QString`。
- 参数 `a`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `fieldWidth`：类型为 `int`。默认值为 `0`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `base`：类型为 `int`。默认值为 `10`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `fillChar`：类型为 `QChar`。默认值为 `u' '`。传入 `QChar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename T, QString::if_floating_point<T> = true> QString QString::arg(T a, int fieldWidth = 0, char format = 'g', int precision = -1, QChar fillChar = u' ') const`

**API 类别：** 成员函数说明

**中文解读：** `QString::arg` 用于计算、查询或取得与“arg”相关的操作。调用时要先确认当前状态和 `a`、`fieldWidth`、`format`、`precision`、`fillChar` 的有效范围；返回类型是 `template <typename T, QString::if_floating_point<T> = true> QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename T, QString::if_floating_point<T> = true> QString`。
- 参数 `a`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `fieldWidth`：类型为 `int`。默认值为 `0`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `format`：类型为 `char`。默认值为 `'g'`。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `precision`：类型为 `int`。默认值为 `-1`。精度或舍入策略；它可能影响数值转换和数据库结果，不能只按显示位数理解。
- 参数 `fillChar`：类型为 `QChar`。默认值为 `u' '`。传入 `QChar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QString::asprintf(const char *cformat, ...)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `asprintf`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `cformat`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `...`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] QString &QString::assign(QAnyStringView v)`

**API 类别：** 成员函数说明

**中文解读：** `QString::assign` 用于计算、查询或取得与“assign”相关的操作。调用时要先确认当前状态和 `v` 的有效范围；返回类型是 `QString &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `v`：类型为 `QAnyStringView`。没有默认值，调用时必须提供。传入 `QAnyStringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] template <typename InputIterator, QString::if_compatible_iterator<InputIterator> = true> QString &QString::assign(InputIterator first, InputIterator last)`

**API 类别：** 成员函数说明

**中文解读：** `QString::assign` 用于计算、查询或取得与“assign”相关的操作。调用时要先确认当前状态和 `first`、`last` 的有效范围；返回类型是 `template <typename InputIterator, QString::if_compatible_iterator<InputIterator> = true> QString &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename InputIterator, QString::if_compatible_iterator<InputIterator> = true> QString &`。
- 参数 `first`：类型为 `InputIterator`。没有默认值，调用时必须提供。传入 `InputIterator` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `last`：类型为 `InputIterator`。没有默认值，调用时必须提供。传入 `InputIterator` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] QString &QString::assign(qsizetype n, QChar c)`

**API 类别：** 成员函数说明

**中文解读：** `QString::assign` 用于计算、查询或取得与“assign”相关的操作。调用时要先确认当前状态和 `n`、`c` 的有效范围；返回类型是 `QString &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `n`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `c`：类型为 `QChar`。没有默认值，调用时必须提供。传入 `QChar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QChar QString::at(qsizetype position) const`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `at`，用于取得 `QString` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`const QChar`。
- 参数 `position`：类型为 `qsizetype`。没有默认值，调用时必须提供。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QChar &QString::back()`

**API 类别：** 成员函数说明

**中文解读：** `QString::back` 用于计算、查询或取得与“末尾”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QChar &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QChar &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QChar QString::back() const`

**API 类别：** 成员函数说明

**中文解读：** `QString::back` 用于计算、查询或取得与“末尾”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QChar`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QChar`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString::iterator QString::begin()`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `begin`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QString::iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString::const_iterator QString::begin() const`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `begin`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QString::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qsizetype QString::capacity() const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `capacity`，返回 `QString` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString::const_iterator QString::cbegin() const`

**API 类别：** 成员函数说明

**中文解读：** `QString::cbegin` 用于计算、查询或取得与“cbegin”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString::const_iterator QString::cend() const`

**API 类别：** 成员函数说明

**中文解读：** `QString::cend` 用于计算、查询或取得与“cend”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QString::chop(qsizetype n)`

**API 类别：** 成员函数说明

**中文解读：** `QString::chop` 用于执行与“chop”相关的操作。调用时要先确认当前状态和 `n` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `n`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QString::chopped(qsizetype len) &&`

**API 类别：** 成员函数说明

**中文解读：** `QString::chopped` 用于计算、查询或取得与“chopped”相关的操作。调用时要先确认当前状态和 `len` 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数 `len`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QString::clear()`

**API 类别：** 成员函数说明

**中文解读：** 这是状态清理或重置 API `clear`。调用后原有数据、索引、缓存或绑定可能失效；使用前先确认它影响的是当前对象、子对象还是底层共享资源，之后重新检查状态。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static noexcept] int QString::compare(const QString &s1, const QString &s2, Qt::CaseSensitivity cs = Qt::CaseSensitive)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `compare`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`int`。
- 参数 `s1`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `s2`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] int QString::compare(QChar ch, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**API 类别：** 成员函数说明

**中文解读：** `QString::compare` 用于计算、查询或取得与“比较”相关的操作。调用时要先确认当前状态和 `ch`、`cs` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `ch`：类型为 `QChar`。没有默认值，调用时必须提供。传入 `QChar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] int QString::compare(QLatin1StringView other, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**API 类别：** 成员函数说明

**中文解读：** `QString::compare` 用于计算、查询或取得与“比较”相关的操作。调用时要先确认当前状态和 `other`、`cs` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `other`：类型为 `QLatin1StringView`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] int QString::compare(QStringView s, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**API 类别：** 成员函数说明

**中文解读：** `QString::compare` 用于计算、查询或取得与“比较”相关的操作。调用时要先确认当前状态和 `s`、`cs` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `s`：类型为 `QStringView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] int QString::compare(const QString &other, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**API 类别：** 成员函数说明

**中文解读：** `QString::compare` 用于计算、查询或取得与“比较”相关的操作。调用时要先确认当前状态和 `other`、`cs` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `other`：类型为 `const QString &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static noexcept] int QString::compare(QLatin1StringView s1, const QString &s2, Qt::CaseSensitivity cs = Qt::CaseSensitive)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `compare`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`int`。
- 参数 `s1`：类型为 `QLatin1StringView`。没有默认值，调用时必须提供。传入 `QLatin1StringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `s2`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static noexcept] int QString::compare(QStringView s1, const QString &s2, Qt::CaseSensitivity cs = Qt::CaseSensitive)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `compare`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`int`。
- 参数 `s1`：类型为 `QStringView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `s2`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static noexcept] int QString::compare(const QString &s1, QLatin1StringView s2, Qt::CaseSensitivity cs = Qt::CaseSensitive)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `compare`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`int`。
- 参数 `s1`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `s2`：类型为 `QLatin1StringView`。没有默认值，调用时必须提供。传入 `QLatin1StringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static noexcept] int QString::compare(const QString &s1, QStringView s2, Qt::CaseSensitivity cs = Qt::CaseSensitive)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `compare`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`int`。
- 参数 `s1`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `s2`：类型为 `QStringView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString::const_iterator QString::constBegin() const`

**API 类别：** 成员函数说明

**中文解读：** `QString::constBegin` 用于计算、查询或取得与“const、起始位置”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QChar *QString::constData() const`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `constData`，用于取得 `QString` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`const QChar *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString::const_iterator QString::constEnd() const`

**API 类别：** 成员函数说明

**中文解读：** `QString::constEnd` 用于计算、查询或取得与“const、结束”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString::const_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QString::contains(const QRegularExpression &re, QRegularExpressionMatch *rmatch = nullptr) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `contains`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `re`：类型为 `const QRegularExpression &`。没有默认值，调用时必须提供。传入 `const QRegularExpression &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `rmatch`：类型为 `QRegularExpressionMatch *`。默认值为 `nullptr`。传入 `QRegularExpressionMatch *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QString::contains(const QString &str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `contains`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `str`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QString::contains(QChar ch, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `contains`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `ch`：类型为 `QChar`。没有默认值，调用时必须提供。传入 `QChar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QString::contains(QLatin1StringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `contains`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `str`：类型为 `QLatin1StringView`。没有默认值，调用时必须提供。传入 `QLatin1StringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool QString::contains(QStringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `contains`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `str`：类型为 `QStringView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qsizetype QString::count(const QString &str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `count`，返回 `QString` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数 `str`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qsizetype QString::count(const QRegularExpression &re) const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `count`，返回 `QString` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数 `re`：类型为 `const QRegularExpression &`。没有默认值，调用时必须提供。传入 `const QRegularExpression &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qsizetype QString::count(QChar ch, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `count`，返回 `QString` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数 `ch`：类型为 `QChar`。没有默认值，调用时必须提供。传入 `QChar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] qsizetype QString::count(QStringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `count`，返回 `QString` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数 `str`：类型为 `QStringView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString::const_reverse_iterator QString::crbegin() const`

**API 类别：** 成员函数说明

**中文解读：** `QString::crbegin` 用于计算、查询或取得与“crbegin”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString::const_reverse_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString::const_reverse_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString::const_reverse_iterator QString::crend() const`

**API 类别：** 成员函数说明

**中文解读：** `QString::crend` 用于计算、查询或取得与“crend”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString::const_reverse_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString::const_reverse_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QChar *QString::data()`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `data`，用于取得 `QString` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`QChar *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QChar *QString::data() const`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `data`，用于取得 `QString` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`const QChar *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString::iterator QString::end()`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `end`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`QString::iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString::const_iterator QString::end() const`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `end`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`QString::const_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QString::endsWith(const QString &s, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `endsWith`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`bool`。
- 参数 `s`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QString::endsWith(QChar c, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `endsWith`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`bool`。
- 参数 `c`：类型为 `QChar`。没有默认值，调用时必须提供。传入 `QChar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QString::endsWith(QLatin1StringView s, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `endsWith`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`bool`。
- 参数 `s`：类型为 `QLatin1StringView`。没有默认值，调用时必须提供。传入 `QLatin1StringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool QString::endsWith(QStringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `endsWith`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`bool`。
- 参数 `str`：类型为 `QStringView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.1] QString::iterator QString::erase(QString::const_iterator first, QString::const_iterator last)`

**API 类别：** 成员函数说明

**中文解读：** `QString::erase` 用于计算、查询或取得与“erase”相关的操作。调用时要先确认当前状态和 `first`、`last` 的有效范围；返回类型是 `QString::iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString::iterator`。
- 参数 `first`：类型为 `QString::const_iterator`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `last`：类型为 `QString::const_iterator`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.5] QString::iterator QString::erase(QString::const_iterator it)`

**API 类别：** 成员函数说明

**中文解读：** `QString::erase` 用于计算、查询或取得与“erase”相关的操作。调用时要先确认当前状态和 `it` 的有效范围；返回类型是 `QString::iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString::iterator`。
- 参数 `it`：类型为 `QString::const_iterator`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::fill(QChar ch, qsizetype size = -1)`

**API 类别：** 成员函数说明

**中文解读：** `QString::fill` 用于计算、查询或取得与“fill”相关的操作。调用时要先确认当前状态和 `ch`、`size` 的有效范围；返回类型是 `QString &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `ch`：类型为 `QChar`。没有默认值，调用时必须提供。传入 `QChar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `size`：类型为 `qsizetype`。默认值为 `-1`。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] QString QString::first(qsizetype n) &&`

**API 类别：** 成员函数说明

**中文解读：** `QString::first` 用于计算、查询或取得与“首项”相关的操作。调用时要先确认当前状态和 `n` 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数 `n`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QString::fromCFString(CFStringRef string)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromCFString`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `string`：类型为 `CFStringRef`。没有默认值，调用时必须提供。传入 `CFStringRef` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.6] QString QString::fromEcmaString(emscripten::val jsString)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromEcmaString`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `jsString`：类型为 `emscripten::val`。没有默认值，调用时必须提供。传入 `emscripten::val` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QString::fromLatin1(const char *str, qsizetype size)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromLatin1`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `str`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `size`：类型为 `qsizetype`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.0] QString QString::fromLatin1(QByteArrayView str)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromLatin1`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `str`：类型为 `QByteArrayView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QString::fromLatin1(const QByteArray &str)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromLatin1`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `str`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QString::fromLocal8Bit(const char *str, qsizetype size)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromLocal8Bit`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `str`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `size`：类型为 `qsizetype`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.0] QString QString::fromLocal8Bit(QByteArrayView str)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromLocal8Bit`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `str`：类型为 `QByteArrayView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QString::fromLocal8Bit(const QByteArray &str)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromLocal8Bit`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `str`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QString::fromNSString(const NSString *string)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromNSString`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `string`：类型为 `const NSString *`。没有默认值，调用时必须提供。传入 `const NSString *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.10] QString QString::fromRawData(const char16_t *unicode, qsizetype size)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromRawData`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `unicode`：类型为 `const char16_t *`。没有默认值，调用时必须提供。传入 `const char16_t *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `size`：类型为 `qsizetype`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QString::fromRawData(const QChar *unicode, qsizetype size)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromRawData`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `unicode`：类型为 `const QChar *`。没有默认值，调用时必须提供。传入 `const QChar *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `size`：类型为 `qsizetype`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QString::fromStdString(const std::string &str)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromStdString`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `str`：类型为 `const std::string &`。没有默认值，调用时必须提供。传入 `const std::string &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QString::fromStdU16String(const std::u16string &str)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromStdU16String`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `str`：类型为 `const std::u16string &`。没有默认值，调用时必须提供。传入 `const std::u16string &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QString::fromStdU32String(const std::u32string &str)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromStdU32String`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `str`：类型为 `const std::u32string &`。没有默认值，调用时必须提供。传入 `const std::u32string &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QString::fromStdWString(const std::wstring &str)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromStdWString`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `str`：类型为 `const std::wstring &`。没有默认值，调用时必须提供。传入 `const std::wstring &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QString::fromUcs4(const char32_t *unicode, qsizetype size = -1)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromUcs4`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `unicode`：类型为 `const char32_t *`。没有默认值，调用时必须提供。传入 `const char32_t *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `size`：类型为 `qsizetype`。默认值为 `-1`。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QString::fromUtf8(const char *str, qsizetype size)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromUtf8`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `str`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `size`：类型为 `qsizetype`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.0] QString QString::fromUtf8(QByteArrayView str)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromUtf8`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `str`：类型为 `QByteArrayView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QString::fromUtf8(const QByteArray &str)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromUtf8`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `str`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.1] QString QString::fromUtf8(const char8_t *str)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromUtf8`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `str`：类型为 `const char8_t *`。没有默认值，调用时必须提供。传入 `const char8_t *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.0] QString QString::fromUtf8(const char8_t *str, qsizetype size)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromUtf8`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `str`：类型为 `const char8_t *`。没有默认值，调用时必须提供。传入 `const char8_t *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `size`：类型为 `qsizetype`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QString::fromUtf16(const char16_t *unicode, qsizetype size = -1)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromUtf16`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `unicode`：类型为 `const char16_t *`。没有默认值，调用时必须提供。传入 `const char16_t *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `size`：类型为 `qsizetype`。默认值为 `-1`。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QString::fromWCharArray(const wchar_t *string, qsizetype size = -1)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromWCharArray`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `string`：类型为 `const wchar_t *`。没有默认值，调用时必须提供。传入 `const wchar_t *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `size`：类型为 `qsizetype`。默认值为 `-1`。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QChar &QString::front()`

**API 类别：** 成员函数说明

**中文解读：** `QString::front` 用于计算、查询或取得与“开头”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QChar &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QChar &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QChar QString::front() const`

**API 类别：** 成员函数说明

**中文解读：** `QString::front` 用于计算、查询或取得与“开头”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QChar`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QChar`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qsizetype QString::indexOf(QLatin1StringView str, qsizetype from = 0, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**API 类别：** 成员函数说明

**中文解读：** `QString::indexOf` 用于计算、查询或取得与“索引、Of”相关的操作。调用时要先确认当前状态和 `str`、`from`、`cs` 的有效范围；返回类型是 `qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数 `str`：类型为 `QLatin1StringView`。没有默认值，调用时必须提供。传入 `QLatin1StringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `from`：类型为 `qsizetype`。默认值为 `0`。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qsizetype QString::indexOf(const QRegularExpression &re, qsizetype from = 0, QRegularExpressionMatch *rmatch = nullptr) const`

**API 类别：** 成员函数说明

**中文解读：** `QString::indexOf` 用于计算、查询或取得与“索引、Of”相关的操作。调用时要先确认当前状态和 `re`、`from`、`rmatch` 的有效范围；返回类型是 `qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数 `re`：类型为 `const QRegularExpression &`。没有默认值，调用时必须提供。传入 `const QRegularExpression &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `from`：类型为 `qsizetype`。默认值为 `0`。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `rmatch`：类型为 `QRegularExpressionMatch *`。默认值为 `nullptr`。传入 `QRegularExpressionMatch *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qsizetype QString::indexOf(const QString &str, qsizetype from = 0, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**API 类别：** 成员函数说明

**中文解读：** `QString::indexOf` 用于计算、查询或取得与“索引、Of”相关的操作。调用时要先确认当前状态和 `str`、`from`、`cs` 的有效范围；返回类型是 `qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数 `str`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `from`：类型为 `qsizetype`。默认值为 `0`。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qsizetype QString::indexOf(QChar ch, qsizetype from = 0, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**API 类别：** 成员函数说明

**中文解读：** `QString::indexOf` 用于计算、查询或取得与“索引、Of”相关的操作。调用时要先确认当前状态和 `ch`、`from`、`cs` 的有效范围；返回类型是 `qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数 `ch`：类型为 `QChar`。没有默认值，调用时必须提供。传入 `QChar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `from`：类型为 `qsizetype`。默认值为 `0`。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] qsizetype QString::indexOf(QStringView str, qsizetype from = 0, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**API 类别：** 成员函数说明

**中文解读：** `QString::indexOf` 用于计算、查询或取得与“索引、Of”相关的操作。调用时要先确认当前状态和 `str`、`from`、`cs` 的有效范围；返回类型是 `qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数 `str`：类型为 `QStringView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `from`：类型为 `qsizetype`。默认值为 `0`。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::insert(qsizetype position, const QString &str)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QString` 添加依赖、数据或子对象的 API `insert`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `position`：类型为 `qsizetype`。没有默认值，调用时必须提供。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。
- 参数 `str`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::insert(qsizetype position, QChar ch)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QString` 添加依赖、数据或子对象的 API `insert`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `position`：类型为 `qsizetype`。没有默认值，调用时必须提供。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。
- 参数 `ch`：类型为 `QChar`。没有默认值，调用时必须提供。传入 `QChar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::insert(qsizetype position, QLatin1StringView str)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QString` 添加依赖、数据或子对象的 API `insert`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `position`：类型为 `qsizetype`。没有默认值，调用时必须提供。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。
- 参数 `str`：类型为 `QLatin1StringView`。没有默认值，调用时必须提供。传入 `QLatin1StringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] QString &QString::insert(qsizetype position, QStringView str)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QString` 添加依赖、数据或子对象的 API `insert`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `position`：类型为 `qsizetype`。没有默认值，调用时必须提供。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。
- 参数 `str`：类型为 `QStringView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.5] QString &QString::insert(qsizetype position, QUtf8StringView str)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QString` 添加依赖、数据或子对象的 API `insert`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `position`：类型为 `qsizetype`。没有默认值，调用时必须提供。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。
- 参数 `str`：类型为 `QUtf8StringView`。没有默认值，调用时必须提供。传入 `QUtf8StringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::insert(qsizetype position, const QByteArray &str)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QString` 添加依赖、数据或子对象的 API `insert`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `position`：类型为 `qsizetype`。没有默认值，调用时必须提供。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。
- 参数 `str`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::insert(qsizetype position, const char *str)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QString` 添加依赖、数据或子对象的 API `insert`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `position`：类型为 `qsizetype`。没有默认值，调用时必须提供。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。
- 参数 `str`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::insert(qsizetype position, const QChar *unicode, qsizetype size)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QString` 添加依赖、数据或子对象的 API `insert`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `position`：类型为 `qsizetype`。没有默认值，调用时必须提供。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。
- 参数 `unicode`：类型为 `const QChar *`。没有默认值，调用时必须提供。传入 `const QChar *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `size`：类型为 `qsizetype`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] bool QString::isEmpty() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isEmpty`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QString::isLower() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isLower`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr] bool QString::isNull() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isNull`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QString::isRightToLeft() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isRightToLeft`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QString::isUpper() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isUpper`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool QString::isValidUtf16() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isValidUtf16`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] QString QString::last(qsizetype n) &&`

**API 类别：** 成员函数说明

**中文解读：** `QString::last` 用于计算、查询或取得与“末项”相关的操作。调用时要先确认当前状态和 `n` 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数 `n`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qsizetype QString::lastIndexOf(const QRegularExpression &re, qsizetype from, QRegularExpressionMatch *rmatch = nullptr) const`

**API 类别：** 成员函数说明

**中文解读：** `QString::lastIndexOf` 用于计算、查询或取得与“末项、索引、Of”相关的操作。调用时要先确认当前状态和 `re`、`from`、`rmatch` 的有效范围；返回类型是 `qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数 `re`：类型为 `const QRegularExpression &`。没有默认值，调用时必须提供。传入 `const QRegularExpression &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `from`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `rmatch`：类型为 `QRegularExpressionMatch *`。默认值为 `nullptr`。传入 `QRegularExpressionMatch *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qsizetype QString::lastIndexOf(const QString &str, qsizetype from, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**API 类别：** 成员函数说明

**中文解读：** `QString::lastIndexOf` 用于计算、查询或取得与“末项、索引、Of”相关的操作。调用时要先确认当前状态和 `str`、`from`、`cs` 的有效范围；返回类型是 `qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数 `str`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `from`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept, since 6.3] qsizetype QString::lastIndexOf(QChar ch, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**API 类别：** 成员函数说明

**中文解读：** `QString::lastIndexOf` 用于计算、查询或取得与“末项、索引、Of”相关的操作。调用时要先确认当前状态和 `ch`、`cs` 的有效范围；返回类型是 `qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数 `ch`：类型为 `QChar`。没有默认值，调用时必须提供。传入 `QChar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] qsizetype QString::lastIndexOf(QLatin1StringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**API 类别：** 成员函数说明

**中文解读：** `QString::lastIndexOf` 用于计算、查询或取得与“末项、索引、Of”相关的操作。调用时要先确认当前状态和 `str`、`cs` 的有效范围；返回类型是 `qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数 `str`：类型为 `QLatin1StringView`。没有默认值，调用时必须提供。传入 `QLatin1StringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept, since 6.2] qsizetype QString::lastIndexOf(QStringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**API 类别：** 成员函数说明

**中文解读：** `QString::lastIndexOf` 用于计算、查询或取得与“末项、索引、Of”相关的操作。调用时要先确认当前状态和 `str`、`cs` 的有效范围；返回类型是 `qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数 `str`：类型为 `QStringView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] qsizetype QString::lastIndexOf(const QRegularExpression &re, QRegularExpressionMatch *rmatch = nullptr) const`

**API 类别：** 成员函数说明

**中文解读：** `QString::lastIndexOf` 用于计算、查询或取得与“末项、索引、Of”相关的操作。调用时要先确认当前状态和 `re`、`rmatch` 的有效范围；返回类型是 `qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数 `re`：类型为 `const QRegularExpression &`。没有默认值，调用时必须提供。传入 `const QRegularExpression &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `rmatch`：类型为 `QRegularExpressionMatch *`。默认值为 `nullptr`。传入 `QRegularExpressionMatch *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.2] qsizetype QString::lastIndexOf(const QString &str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**API 类别：** 成员函数说明

**中文解读：** `QString::lastIndexOf` 用于计算、查询或取得与“末项、索引、Of”相关的操作。调用时要先确认当前状态和 `str`、`cs` 的有效范围；返回类型是 `qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数 `str`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qsizetype QString::lastIndexOf(QChar ch, qsizetype from, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**API 类别：** 成员函数说明

**中文解读：** `QString::lastIndexOf` 用于计算、查询或取得与“末项、索引、Of”相关的操作。调用时要先确认当前状态和 `ch`、`from`、`cs` 的有效范围；返回类型是 `qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数 `ch`：类型为 `QChar`。没有默认值，调用时必须提供。传入 `QChar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `from`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qsizetype QString::lastIndexOf(QLatin1StringView str, qsizetype from, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**API 类别：** 成员函数说明

**中文解读：** `QString::lastIndexOf` 用于计算、查询或取得与“末项、索引、Of”相关的操作。调用时要先确认当前状态和 `str`、`from`、`cs` 的有效范围；返回类型是 `qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数 `str`：类型为 `QLatin1StringView`。没有默认值，调用时必须提供。传入 `QLatin1StringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `from`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] qsizetype QString::lastIndexOf(QStringView str, qsizetype from, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**API 类别：** 成员函数说明

**中文解读：** `QString::lastIndexOf` 用于计算、查询或取得与“末项、索引、Of”相关的操作。调用时要先确认当前状态和 `str`、`from`、`cs` 的有效范围；返回类型是 `qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数 `str`：类型为 `QStringView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `from`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QString::left(qsizetype n) &&`

**API 类别：** 成员函数说明

**中文解读：** `QString::left` 用于计算、查询或取得与“左侧”相关的操作。调用时要先确认当前状态和 `n` 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数 `n`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QString::leftJustified(qsizetype width, QChar fill = u' ', bool truncate = false) const`

**API 类别：** 成员函数说明

**中文解读：** `QString::leftJustified` 用于计算、查询或取得与“左侧、Justified”相关的操作。调用时要先确认当前状态和 `width`、`fill`、`truncate` 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数 `width`：类型为 `qsizetype`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `fill`：类型为 `QChar`。默认值为 `u' '`。传入 `QChar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `truncate`：类型为 `bool`。默认值为 `false`。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] qsizetype QString::length() const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `length`，返回 `QString` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] int QString::localeAwareCompare(const QString &s1, const QString &s2)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `localeAwareCompare`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`int`。
- 参数 `s1`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `s2`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] int QString::localeAwareCompare(QStringView other) const`

**API 类别：** 成员函数说明

**中文解读：** `QString::localeAwareCompare` 用于计算、查询或取得与“locale、Aware、比较”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `other`：类型为 `QStringView`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QString::localeAwareCompare(const QString &other) const`

**API 类别：** 成员函数说明

**中文解读：** `QString::localeAwareCompare` 用于计算、查询或取得与“locale、Aware、比较”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `other`：类型为 `const QString &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.0] int QString::localeAwareCompare(QStringView s1, QStringView s2)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `localeAwareCompare`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`int`。
- 参数 `s1`：类型为 `QStringView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `s2`：类型为 `QStringView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static constexpr noexcept, since 6.8] qsizetype QString::maxSize()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `maxSize`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QString::mid(qsizetype position, qsizetype n = -1) &&`

**API 类别：** 成员函数说明

**中文解读：** `QString::mid` 用于计算、查询或取得与“mid”相关的操作。调用时要先确认当前状态和 `position`、`n` 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数 `position`：类型为 `qsizetype`。没有默认值，调用时必须提供。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。
- 参数 `n`：类型为 `qsizetype`。默认值为 `-1`。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QString::normalized(QString::NormalizationForm mode, QChar::UnicodeVersion version = QChar::Unicode_Unassigned) const`

**API 类别：** 成员函数说明

**中文解读：** `QString::normalized` 用于计算、查询或取得与“normalized”相关的操作。调用时要先确认当前状态和 `mode`、`version` 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数 `mode`：类型为 `QString::NormalizationForm`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。
- 参数 `version`：类型为 `QChar::UnicodeVersion`。默认值为 `QChar::Unicode_Unassigned`。传入 `QChar::UnicodeVersion` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.10] QString &QString::nullTerminate()`

**API 类别：** 成员函数说明

**中文解读：** `QString::nullTerminate` 用于计算、查询或取得与“null、Terminate”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.10] QString QString::nullTerminated() &&`

**API 类别：** 成员函数说明

**中文解读：** `QString::nullTerminated` 用于计算、查询或取得与“null、Terminated”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QString::number(long n, int base = 10)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `number`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `n`：类型为 `long`。没有默认值，调用时必须提供。传入 `long` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `base`：类型为 `int`。默认值为 `10`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QString::number(double n, char format = 'g', int precision = 6)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `number`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `n`：类型为 `double`。没有默认值，调用时必须提供。传入 `double` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `format`：类型为 `char`。默认值为 `'g'`。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `precision`：类型为 `int`。默认值为 `6`。精度或舍入策略；它可能影响数值转换和数据库结果，不能只按显示位数理解。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QString::number(int n, int base = 10)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `number`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `n`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `base`：类型为 `int`。默认值为 `10`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QString::number(qlonglong n, int base = 10)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `number`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `n`：类型为 `qlonglong`。没有默认值，调用时必须提供。传入 `qlonglong` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `base`：类型为 `int`。默认值为 `10`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QString::number(qulonglong n, int base = 10)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `number`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `n`：类型为 `qulonglong`。没有默认值，调用时必须提供。传入 `qulonglong` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `base`：类型为 `int`。默认值为 `10`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QString::number(uint n, int base = 10)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `number`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `n`：类型为 `uint`。没有默认值，调用时必须提供。传入 `uint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `base`：类型为 `int`。默认值为 `10`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QString::number(ulong n, int base = 10)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `number`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `n`：类型为 `ulong`。没有默认值，调用时必须提供。传入 `ulong` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `base`：类型为 `int`。默认值为 `10`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::prepend(const QString &str)`

**API 类别：** 成员函数说明

**中文解读：** `QString::prepend` 用于计算、查询或取得与“前置追加”相关的操作。调用时要先确认当前状态和 `str` 的有效范围；返回类型是 `QString &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `str`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::prepend(QChar ch)`

**API 类别：** 成员函数说明

**中文解读：** `QString::prepend` 用于计算、查询或取得与“前置追加”相关的操作。调用时要先确认当前状态和 `ch` 的有效范围；返回类型是 `QString &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `ch`：类型为 `QChar`。没有默认值，调用时必须提供。传入 `QChar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::prepend(QLatin1StringView str)`

**API 类别：** 成员函数说明

**中文解读：** `QString::prepend` 用于计算、查询或取得与“前置追加”相关的操作。调用时要先确认当前状态和 `str` 的有效范围；返回类型是 `QString &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `str`：类型为 `QLatin1StringView`。没有默认值，调用时必须提供。传入 `QLatin1StringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] QString &QString::prepend(QStringView str)`

**API 类别：** 成员函数说明

**中文解读：** `QString::prepend` 用于计算、查询或取得与“前置追加”相关的操作。调用时要先确认当前状态和 `str` 的有效范围；返回类型是 `QString &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `str`：类型为 `QStringView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.5] QString &QString::prepend(QUtf8StringView str)`

**API 类别：** 成员函数说明

**中文解读：** `QString::prepend` 用于计算、查询或取得与“前置追加”相关的操作。调用时要先确认当前状态和 `str` 的有效范围；返回类型是 `QString &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `str`：类型为 `QUtf8StringView`。没有默认值，调用时必须提供。传入 `QUtf8StringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::prepend(const QByteArray &ba)`

**API 类别：** 成员函数说明

**中文解读：** `QString::prepend` 用于计算、查询或取得与“前置追加”相关的操作。调用时要先确认当前状态和 `ba` 的有效范围；返回类型是 `QString &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `ba`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::prepend(const char *str)`

**API 类别：** 成员函数说明

**中文解读：** `QString::prepend` 用于计算、查询或取得与“前置追加”相关的操作。调用时要先确认当前状态和 `str` 的有效范围；返回类型是 `QString &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `str`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::prepend(const QChar *str, qsizetype len)`

**API 类别：** 成员函数说明

**中文解读：** `QString::prepend` 用于计算、查询或取得与“前置追加”相关的操作。调用时要先确认当前状态和 `str`、`len` 的有效范围；返回类型是 `QString &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `str`：类型为 `const QChar *`。没有默认值，调用时必须提供。传入 `const QChar *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `len`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QString::push_back(const QString &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QString` 添加依赖、数据或子对象的 API `push_back`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `other`：类型为 `const QString &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QString::push_back(QChar ch)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QString` 添加依赖、数据或子对象的 API `push_back`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `ch`：类型为 `QChar`。没有默认值，调用时必须提供。传入 `QChar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QString::push_front(const QString &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QString` 添加依赖、数据或子对象的 API `push_front`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `other`：类型为 `const QString &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QString::push_front(QChar ch)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QString` 添加依赖、数据或子对象的 API `push_front`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `ch`：类型为 `QChar`。没有默认值，调用时必须提供。传入 `QChar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString::reverse_iterator QString::rbegin()`

**API 类别：** 成员函数说明

**中文解读：** `QString::rbegin` 用于计算、查询或取得与“rbegin”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString::reverse_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString::reverse_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString::const_reverse_iterator QString::rbegin() const`

**API 类别：** 成员函数说明

**中文解读：** `QString::rbegin` 用于计算、查询或取得与“rbegin”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString::const_reverse_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString::const_reverse_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::remove(const QRegularExpression &re)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `remove`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `re`：类型为 `const QRegularExpression &`。没有默认值，调用时必须提供。传入 `const QRegularExpression &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::remove(QChar ch, Qt::CaseSensitivity cs = Qt::CaseSensitive)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `remove`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `ch`：类型为 `QChar`。没有默认值，调用时必须提供。传入 `QChar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::remove(const QString &str, Qt::CaseSensitivity cs = Qt::CaseSensitive)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `remove`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `str`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::remove(qsizetype position, qsizetype n)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `remove`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `position`：类型为 `qsizetype`。没有默认值，调用时必须提供。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。
- 参数 `n`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::remove(QLatin1StringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `remove`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `str`：类型为 `QLatin1StringView`。没有默认值，调用时必须提供。传入 `QLatin1StringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.5] QString &QString::removeAt(qsizetype pos)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeAt`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `pos`：类型为 `qsizetype`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.5] QString &QString::removeFirst()`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeFirst`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`QString &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.1] template <typename Predicate> QString &QString::removeIf(Predicate pred)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeIf`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`template <typename Predicate> QString &`。
- 参数 `pred`：类型为 `Predicate`。没有默认值，调用时必须提供。传入 `Predicate` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.5] QString &QString::removeLast()`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeLast`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`QString &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString::reverse_iterator QString::rend()`

**API 类别：** 成员函数说明

**中文解读：** `QString::rend` 用于计算、查询或取得与“rend”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString::reverse_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString::reverse_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString::const_reverse_iterator QString::rend() const`

**API 类别：** 成员函数说明

**中文解读：** `QString::rend` 用于计算、查询或取得与“rend”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString::const_reverse_iterator`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString::const_reverse_iterator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QString::repeated(qsizetype times) const`

**API 类别：** 成员函数说明

**中文解读：** `QString::repeated` 用于计算、查询或取得与“repeated”相关的操作。调用时要先确认当前状态和 `times` 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数 `times`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::replace(qsizetype position, qsizetype n, const QString &after)`

**API 类别：** 成员函数说明

**中文解读：** `QString::replace` 用于计算、查询或取得与“替换”相关的操作。调用时要先确认当前状态和 `position`、`n`、`after` 的有效范围；返回类型是 `QString &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `position`：类型为 `qsizetype`。没有默认值，调用时必须提供。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。
- 参数 `n`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `after`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::replace(const QRegularExpression &re, const QString &after)`

**API 类别：** 成员函数说明

**中文解读：** `QString::replace` 用于计算、查询或取得与“替换”相关的操作。调用时要先确认当前状态和 `re`、`after` 的有效范围；返回类型是 `QString &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `re`：类型为 `const QRegularExpression &`。没有默认值，调用时必须提供。传入 `const QRegularExpression &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `after`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::replace(QChar before, QChar after, Qt::CaseSensitivity cs = Qt::CaseSensitive)`

**API 类别：** 成员函数说明

**中文解读：** `QString::replace` 用于计算、查询或取得与“替换”相关的操作。调用时要先确认当前状态和 `before`、`after`、`cs` 的有效范围；返回类型是 `QString &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `before`：类型为 `QChar`。没有默认值，调用时必须提供。传入 `QChar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `after`：类型为 `QChar`。没有默认值，调用时必须提供。传入 `QChar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::replace(QChar c, QLatin1StringView after, Qt::CaseSensitivity cs = Qt::CaseSensitive)`

**API 类别：** 成员函数说明

**中文解读：** `QString::replace` 用于计算、查询或取得与“替换”相关的操作。调用时要先确认当前状态和 `c`、`after`、`cs` 的有效范围；返回类型是 `QString &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `c`：类型为 `QChar`。没有默认值，调用时必须提供。传入 `QChar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `after`：类型为 `QLatin1StringView`。没有默认值，调用时必须提供。传入 `QLatin1StringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::replace(QChar ch, const QString &after, Qt::CaseSensitivity cs = Qt::CaseSensitive)`

**API 类别：** 成员函数说明

**中文解读：** `QString::replace` 用于计算、查询或取得与“替换”相关的操作。调用时要先确认当前状态和 `ch`、`after`、`cs` 的有效范围；返回类型是 `QString &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `ch`：类型为 `QChar`。没有默认值，调用时必须提供。传入 `QChar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `after`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::replace(QLatin1StringView before, QLatin1StringView after, Qt::CaseSensitivity cs = Qt::CaseSensitive)`

**API 类别：** 成员函数说明

**中文解读：** `QString::replace` 用于计算、查询或取得与“替换”相关的操作。调用时要先确认当前状态和 `before`、`after`、`cs` 的有效范围；返回类型是 `QString &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `before`：类型为 `QLatin1StringView`。没有默认值，调用时必须提供。传入 `QLatin1StringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `after`：类型为 `QLatin1StringView`。没有默认值，调用时必须提供。传入 `QLatin1StringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::replace(QLatin1StringView before, const QString &after, Qt::CaseSensitivity cs = Qt::CaseSensitive)`

**API 类别：** 成员函数说明

**中文解读：** `QString::replace` 用于计算、查询或取得与“替换”相关的操作。调用时要先确认当前状态和 `before`、`after`、`cs` 的有效范围；返回类型是 `QString &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `before`：类型为 `QLatin1StringView`。没有默认值，调用时必须提供。传入 `QLatin1StringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `after`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::replace(const QString &before, QLatin1StringView after, Qt::CaseSensitivity cs = Qt::CaseSensitive)`

**API 类别：** 成员函数说明

**中文解读：** `QString::replace` 用于计算、查询或取得与“替换”相关的操作。调用时要先确认当前状态和 `before`、`after`、`cs` 的有效范围；返回类型是 `QString &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `before`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `after`：类型为 `QLatin1StringView`。没有默认值，调用时必须提供。传入 `QLatin1StringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::replace(const QString &before, const QString &after, Qt::CaseSensitivity cs = Qt::CaseSensitive)`

**API 类别：** 成员函数说明

**中文解读：** `QString::replace` 用于计算、查询或取得与“替换”相关的操作。调用时要先确认当前状态和 `before`、`after`、`cs` 的有效范围；返回类型是 `QString &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `before`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `after`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::replace(qsizetype position, qsizetype n, QChar after)`

**API 类别：** 成员函数说明

**中文解读：** `QString::replace` 用于计算、查询或取得与“替换”相关的操作。调用时要先确认当前状态和 `position`、`n`、`after` 的有效范围；返回类型是 `QString &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `position`：类型为 `qsizetype`。没有默认值，调用时必须提供。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。
- 参数 `n`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `after`：类型为 `QChar`。没有默认值，调用时必须提供。传入 `QChar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::replace(qsizetype position, qsizetype n, const QChar *after, qsizetype alen)`

**API 类别：** 成员函数说明

**中文解读：** `QString::replace` 用于计算、查询或取得与“替换”相关的操作。调用时要先确认当前状态和 `position`、`n`、`after`、`alen` 的有效范围；返回类型是 `QString &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `position`：类型为 `qsizetype`。没有默认值，调用时必须提供。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。
- 参数 `n`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `after`：类型为 `const QChar *`。没有默认值，调用时必须提供。传入 `const QChar *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `alen`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::replace(const QChar *before, qsizetype blen, const QChar *after, qsizetype alen, Qt::CaseSensitivity cs = Qt::CaseSensitive)`

**API 类别：** 成员函数说明

**中文解读：** `QString::replace` 用于计算、查询或取得与“替换”相关的操作。调用时要先确认当前状态和 `before`、`blen`、`after`、`alen`、`cs` 的有效范围；返回类型是 `QString &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `before`：类型为 `const QChar *`。没有默认值，调用时必须提供。传入 `const QChar *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `blen`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `after`：类型为 `const QChar *`。没有默认值，调用时必须提供。传入 `const QChar *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `alen`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QString::reserve(qsizetype size)`

**API 类别：** 成员函数说明

**中文解读：** `QString::reserve` 用于执行与“reserve”相关的操作。调用时要先确认当前状态和 `size` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `size`：类型为 `qsizetype`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QString::resize(qsizetype size)`

**API 类别：** 成员函数说明

**中文解读：** `QString::resize` 用于执行与“调整尺寸”相关的操作。调用时要先确认当前状态和 `size` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `size`：类型为 `qsizetype`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QString::resize(qsizetype newSize, QChar fillChar)`

**API 类别：** 成员函数说明

**中文解读：** `QString::resize` 用于执行与“调整尺寸”相关的操作。调用时要先确认当前状态和 `newSize`、`fillChar` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `newSize`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `fillChar`：类型为 `QChar`。没有默认值，调用时必须提供。传入 `QChar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.8] void QString::resizeForOverwrite(qsizetype size)`

**API 类别：** 成员函数说明

**中文解读：** `QString::resizeForOverwrite` 用于执行与“调整尺寸、For、Overwrite”相关的操作。调用时要先确认当前状态和 `size` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `size`：类型为 `qsizetype`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QString::right(qsizetype n) &&`

**API 类别：** 成员函数说明

**中文解读：** `QString::right` 用于计算、查询或取得与“右侧”相关的操作。调用时要先确认当前状态和 `n` 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数 `n`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QString::rightJustified(qsizetype width, QChar fill = u' ', bool truncate = false) const`

**API 类别：** 成员函数说明

**中文解读：** `QString::rightJustified` 用于计算、查询或取得与“右侧、Justified”相关的操作。调用时要先确认当前状态和 `width`、`fill`、`truncate` 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数 `width`：类型为 `qsizetype`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `fill`：类型为 `QChar`。默认值为 `u' '`。传入 `QChar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `truncate`：类型为 `bool`。默认值为 `false`。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QString::section(QChar sep, qsizetype start, qsizetype end = -1, QString::SectionFlags flags = SectionDefault) const`

**API 类别：** 成员函数说明

**中文解读：** `QString::section` 用于计算、查询或取得与“section”相关的操作。调用时要先确认当前状态和 `sep`、`start`、`end`、`flags` 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数 `sep`：类型为 `QChar`。没有默认值，调用时必须提供。传入 `QChar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `start`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `end`：类型为 `qsizetype`。默认值为 `-1`。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `flags`：类型为 `QString::SectionFlags`。默认值为 `SectionDefault`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QString::section(const QRegularExpression &re, qsizetype start, qsizetype end = -1, QString::SectionFlags flags = SectionDefault) const`

**API 类别：** 成员函数说明

**中文解读：** `QString::section` 用于计算、查询或取得与“section”相关的操作。调用时要先确认当前状态和 `re`、`start`、`end`、`flags` 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数 `re`：类型为 `const QRegularExpression &`。没有默认值，调用时必须提供。传入 `const QRegularExpression &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `start`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `end`：类型为 `qsizetype`。默认值为 `-1`。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `flags`：类型为 `QString::SectionFlags`。默认值为 `SectionDefault`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QString::section(const QString &sep, qsizetype start, qsizetype end = -1, QString::SectionFlags flags = SectionDefault) const`

**API 类别：** 成员函数说明

**中文解读：** `QString::section` 用于计算、查询或取得与“section”相关的操作。调用时要先确认当前状态和 `sep`、`start`、`end`、`flags` 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数 `sep`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `start`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `end`：类型为 `qsizetype`。默认值为 `-1`。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `flags`：类型为 `QString::SectionFlags`。默认值为 `SectionDefault`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::setNum(int n, int base = 10)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setNum`。调用它会改变 `QString` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `n`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `base`：类型为 `int`。默认值为 `10`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::setNum(long n, int base = 10)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setNum`。调用它会改变 `QString` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `n`：类型为 `long`。没有默认值，调用时必须提供。传入 `long` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `base`：类型为 `int`。默认值为 `10`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::setNum(qlonglong n, int base = 10)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setNum`。调用它会改变 `QString` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `n`：类型为 `qlonglong`。没有默认值，调用时必须提供。传入 `qlonglong` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `base`：类型为 `int`。默认值为 `10`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::setNum(qulonglong n, int base = 10)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setNum`。调用它会改变 `QString` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `n`：类型为 `qulonglong`。没有默认值，调用时必须提供。传入 `qulonglong` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `base`：类型为 `int`。默认值为 `10`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::setNum(short n, int base = 10)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setNum`。调用它会改变 `QString` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `n`：类型为 `short`。没有默认值，调用时必须提供。传入 `short` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `base`：类型为 `int`。默认值为 `10`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::setNum(uint n, int base = 10)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setNum`。调用它会改变 `QString` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `n`：类型为 `uint`。没有默认值，调用时必须提供。传入 `uint` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `base`：类型为 `int`。默认值为 `10`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::setNum(ulong n, int base = 10)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setNum`。调用它会改变 `QString` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `n`：类型为 `ulong`。没有默认值，调用时必须提供。传入 `ulong` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `base`：类型为 `int`。默认值为 `10`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::setNum(ushort n, int base = 10)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setNum`。调用它会改变 `QString` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `n`：类型为 `ushort`。没有默认值，调用时必须提供。传入 `ushort` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `base`：类型为 `int`。默认值为 `10`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::setNum(double n, char format = 'g', int precision = 6)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setNum`。调用它会改变 `QString` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `n`：类型为 `double`。没有默认值，调用时必须提供。传入 `double` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `format`：类型为 `char`。默认值为 `'g'`。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `precision`：类型为 `int`。默认值为 `6`。精度或舍入策略；它可能影响数值转换和数据库结果，不能只按显示位数理解。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::setNum(float n, char format = 'g', int precision = 6)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setNum`。调用它会改变 `QString` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `n`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `format`：类型为 `char`。默认值为 `'g'`。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `precision`：类型为 `int`。默认值为 `6`。精度或舍入策略；它可能影响数值转换和数据库结果，不能只按显示位数理解。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::setRawData(const QChar *unicode, qsizetype size)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setRawData`。调用它会改变 `QString` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `unicode`：类型为 `const QChar *`。没有默认值，调用时必须提供。传入 `const QChar *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `size`：类型为 `qsizetype`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::setUnicode(const QChar *unicode, qsizetype size)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setUnicode`。调用它会改变 `QString` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `unicode`：类型为 `const QChar *`。没有默认值，调用时必须提供。传入 `const QChar *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `size`：类型为 `qsizetype`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.9] QString &QString::setUnicode(const char16_t *unicode, qsizetype size)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setUnicode`。调用它会改变 `QString` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `unicode`：类型为 `const char16_t *`。没有默认值，调用时必须提供。传入 `const char16_t *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `size`：类型为 `qsizetype`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.9] QString &QString::setUtf16(const char16_t *unicode, qsizetype size)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setUtf16`。调用它会改变 `QString` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `unicode`：类型为 `const char16_t *`。没有默认值，调用时必须提供。传入 `const char16_t *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `size`：类型为 `qsizetype`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QString::shrink_to_fit()`

**API 类别：** 成员函数说明

**中文解读：** `QString::shrink_to_fit` 用于执行与“shrink、转换输出、fit”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QString::simplified() const`

**API 类别：** 成员函数说明

**中文解读：** `QString::simplified` 用于计算、查询或取得与“simplified”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] qsizetype QString::size() const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `size`，返回 `QString` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.8] QString &QString::slice(qsizetype pos, qsizetype n)`

**API 类别：** 成员函数说明

**中文解读：** `QString::slice` 用于计算、查询或取得与“slice”相关的操作。调用时要先确认当前状态和 `pos`、`n` 的有效范围；返回类型是 `QString &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `pos`：类型为 `qsizetype`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。
- 参数 `n`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.8] QString &QString::slice(qsizetype pos)`

**API 类别：** 成员函数说明

**中文解读：** `QString::slice` 用于计算、查询或取得与“slice”相关的操作。调用时要先确认当前状态和 `pos` 的有效范围；返回类型是 `QString &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `pos`：类型为 `qsizetype`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] QString QString::sliced(qsizetype pos, qsizetype n) &&`

**API 类别：** 成员函数说明

**中文解读：** `QString::sliced` 用于计算、查询或取得与“sliced”相关的操作。调用时要先确认当前状态和 `pos`、`n` 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数 `pos`：类型为 `qsizetype`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。
- 参数 `n`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] QString QString::sliced(qsizetype pos) &&`

**API 类别：** 成员函数说明

**中文解读：** `QString::sliced` 用于计算、查询或取得与“sliced”相关的操作。调用时要先确认当前状态和 `pos` 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数 `pos`：类型为 `qsizetype`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringList QString::split(const QString &sep, Qt::SplitBehavior behavior = Qt::KeepEmptyParts, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**API 类别：** 成员函数说明

**中文解读：** `QString::split` 用于计算、查询或取得与“split”相关的操作。调用时要先确认当前状态和 `sep`、`behavior`、`cs` 的有效范围；返回类型是 `QStringList`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStringList`。
- 参数 `sep`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `behavior`：类型为 `Qt::SplitBehavior`。默认值为 `Qt::KeepEmptyParts`。传入 `Qt::SplitBehavior` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringList QString::split(const QRegularExpression &re, Qt::SplitBehavior behavior = Qt::KeepEmptyParts) const`

**API 类别：** 成员函数说明

**中文解读：** `QString::split` 用于计算、查询或取得与“split”相关的操作。调用时要先确认当前状态和 `re`、`behavior` 的有效范围；返回类型是 `QStringList`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStringList`。
- 参数 `re`：类型为 `const QRegularExpression &`。没有默认值，调用时必须提供。传入 `const QRegularExpression &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `behavior`：类型为 `Qt::SplitBehavior`。默认值为 `Qt::KeepEmptyParts`。传入 `Qt::SplitBehavior` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringList QString::split(QChar sep, Qt::SplitBehavior behavior = Qt::KeepEmptyParts, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**API 类别：** 成员函数说明

**中文解读：** `QString::split` 用于计算、查询或取得与“split”相关的操作。调用时要先确认当前状态和 `sep`、`behavior`、`cs` 的有效范围；返回类型是 `QStringList`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStringList`。
- 参数 `sep`：类型为 `QChar`。没有默认值，调用时必须提供。传入 `QChar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `behavior`：类型为 `Qt::SplitBehavior`。默认值为 `Qt::KeepEmptyParts`。传入 `Qt::SplitBehavior` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QString::squeeze()`

**API 类别：** 成员函数说明

**中文解读：** `QString::squeeze` 用于执行与“squeeze”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QString::startsWith(const QString &s, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `startsWith`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`bool`。
- 参数 `s`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QString::startsWith(QChar c, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `startsWith`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`bool`。
- 参数 `c`：类型为 `QChar`。没有默认值，调用时必须提供。传入 `QChar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QString::startsWith(QLatin1StringView s, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `startsWith`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`bool`。
- 参数 `s`：类型为 `QLatin1StringView`。没有默认值，调用时必须提供。传入 `QLatin1StringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool QString::startsWith(QStringView str, Qt::CaseSensitivity cs = Qt::CaseSensitive) const`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `startsWith`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`bool`。
- 参数 `str`：类型为 `QStringView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `cs`：类型为 `Qt::CaseSensitivity`。默认值为 `Qt::CaseSensitive`。传入 `Qt::CaseSensitivity` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] void QString::swap(QString &other)`

**API 类别：** 成员函数说明

**中文解读：** `QString::swap` 用于执行与“swap”相关的操作。调用时要先确认当前状态和 `other` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `other`：类型为 `QString &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `CFStringRef QString::toCFString() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toCFString`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`CFStringRef`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QString::toCaseFolded() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toCaseFolded`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `double QString::toDouble(bool *ok = nullptr) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toDouble`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`double`。
- 参数 `ok`：类型为 `bool *`。默认值为 `nullptr`。传入 `bool *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.6] emscripten::val QString::toEcmaString() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toEcmaString`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`emscripten::val`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `float QString::toFloat(bool *ok = nullptr) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toFloat`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`float`。
- 参数 `ok`：类型为 `bool *`。默认值为 `nullptr`。传入 `bool *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QString::toHtmlEscaped() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toHtmlEscaped`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QString::toInt(bool *ok = nullptr, int base = 10) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toInt`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`int`。
- 参数 `ok`：类型为 `bool *`。默认值为 `nullptr`。传入 `bool *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `base`：类型为 `int`。默认值为 `10`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray QString::toLatin1() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toLatin1`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray QString::toLocal8Bit() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toLocal8Bit`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `long QString::toLong(bool *ok = nullptr, int base = 10) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toLong`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`long`。
- 参数 `ok`：类型为 `bool *`。默认值为 `nullptr`。传入 `bool *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `base`：类型为 `int`。默认值为 `10`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qlonglong QString::toLongLong(bool *ok = nullptr, int base = 10) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toLongLong`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`qlonglong`。
- 参数 `ok`：类型为 `bool *`。默认值为 `nullptr`。传入 `bool *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `base`：类型为 `int`。默认值为 `10`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QString::toLower() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toLower`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `NSString *QString::toNSString() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toNSString`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`NSString *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `short QString::toShort(bool *ok = nullptr, int base = 10) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toShort`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`short`。
- 参数 `ok`：类型为 `bool *`。默认值为 `nullptr`。传入 `bool *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `base`：类型为 `int`。默认值为 `10`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `std::string QString::toStdString() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toStdString`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`std::string`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `std::u16string QString::toStdU16String() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toStdU16String`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`std::u16string`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `std::u32string QString::toStdU32String() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toStdU32String`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`std::u32string`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `std::wstring QString::toStdWString() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toStdWString`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`std::wstring`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `uint QString::toUInt(bool *ok = nullptr, int base = 10) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toUInt`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`uint`。
- 参数 `ok`：类型为 `bool *`。默认值为 `nullptr`。传入 `bool *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `base`：类型为 `int`。默认值为 `10`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `ulong QString::toULong(bool *ok = nullptr, int base = 10) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toULong`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`ulong`。
- 参数 `ok`：类型为 `bool *`。默认值为 `nullptr`。传入 `bool *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `base`：类型为 `int`。默认值为 `10`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qulonglong QString::toULongLong(bool *ok = nullptr, int base = 10) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toULongLong`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`qulonglong`。
- 参数 `ok`：类型为 `bool *`。默认值为 `nullptr`。传入 `bool *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `base`：类型为 `int`。默认值为 `10`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `ushort QString::toUShort(bool *ok = nullptr, int base = 10) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toUShort`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`ushort`。
- 参数 `ok`：类型为 `bool *`。默认值为 `nullptr`。传入 `bool *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `base`：类型为 `int`。默认值为 `10`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<uint> QString::toUcs4() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toUcs4`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QList<uint>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QString::toUpper() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toUpper`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray QString::toUtf8() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toUtf8`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qsizetype QString::toWCharArray(wchar_t *array) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toWCharArray`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数 `array`：类型为 `wchar_t *`。没有默认值，调用时必须提供。传入 `wchar_t *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept(...), since 6.0] template <typename Needle, typename... Flags> auto QString::tokenize(Needle &&sep, Flags... flags) &&`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `tokenize`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`template <typename Needle, typename... Flags> auto`。
- 参数 `sep`：类型为 `Needle &&`。没有默认值，调用时必须提供。传入 `Needle &&` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `flags`：类型为 `Flags...`。没有默认值，调用时必须提供。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QString::trimmed() const`

**API 类别：** 成员函数说明

**中文解读：** `QString::trimmed` 用于计算、查询或取得与“trimmed”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QString::truncate(qsizetype position)`

**API 类别：** 成员函数说明

**中文解读：** `QString::truncate` 用于执行与“truncate”相关的操作。调用时要先确认当前状态和 `position` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `position`：类型为 `qsizetype`。没有默认值，调用时必须提供。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QChar *QString::unicode() const`

**API 类别：** 成员函数说明

**中文解读：** `QString::unicode` 用于计算、查询或取得与“unicode”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QChar *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QChar *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const ushort *QString::utf16() const`

**API 类别：** 成员函数说明

**中文解读：** `QString::utf16` 用于计算、查询或取得与“utf、16”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const ushort *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const ushort *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QString QString::vasprintf(const char *cformat, va_list ap)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `vasprintf`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QString`。
- 参数 `cformat`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `ap`：类型为 `va_list`。没有默认值，调用时必须提供。传入 `va_list` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept, since 6.7] QString::operator std::u16string_view() const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`由运算符声明决定`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::operator+=(const QString &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `other`：类型为 `const QString &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::operator+=(QChar ch)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `ch`：类型为 `QChar`。没有默认值，调用时必须提供。传入 `QChar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::operator+=(QLatin1StringView str)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `str`：类型为 `QLatin1StringView`。没有默认值，调用时必须提供。传入 `QLatin1StringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] QString &QString::operator+=(QStringView str)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `str`：类型为 `QStringView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.5] QString &QString::operator+=(QUtf8StringView str)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `str`：类型为 `QUtf8StringView`。没有默认值，调用时必须提供。传入 `QUtf8StringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::operator+=(const QByteArray &ba)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `ba`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::operator+=(const char *str)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `str`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QString &QString::operator=(QString &&other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `other`：类型为 `QString &&`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QString &QString::operator=(const QString &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `other`：类型为 `const QString &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::operator=(QChar ch)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `ch`：类型为 `QChar`。没有默认值，调用时必须提供。传入 `QChar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::operator=(QLatin1StringView str)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `str`：类型为 `QLatin1StringView`。没有默认值，调用时必须提供。传入 `QLatin1StringView` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::operator=(const QByteArray &ba)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `ba`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString &QString::operator=(const char *str)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QString &`。
- 参数 `str`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QChar &QString::operator[](qsizetype position)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QChar &`。
- 参数 `position`：类型为 `qsizetype`。没有默认值，调用时必须提供。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QChar QString::operator[](qsizetype position) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`const QChar`。
- 参数 `position`：类型为 `qsizetype`。没有默认值，调用时必须提供。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.1] template <typename T> qsizetype erase(QString &s, const T &t)`

**API 类别：** 相关非成员函数

**中文解读：** `QString::erase` 用于计算、查询或取得与“erase”相关的操作。调用时要先确认当前状态和 `s`、`t` 的有效范围；返回类型是 `template <typename T> qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename T> qsizetype`。
- 参数 `s`：类型为 `QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `t`：类型为 `const T &`。没有默认值，调用时必须提供。传入 `const T &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.1] template <typename Predicate> qsizetype erase_if(QString &s, Predicate pred)`

**API 类别：** 相关非成员函数

**中文解读：** `QString::erase_if` 用于计算、查询或取得与“erase、if”相关的操作。调用时要先确认当前状态和 `s`、`pred` 的有效范围；返回类型是 `template <typename Predicate> qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename Predicate> qsizetype`。
- 参数 `s`：类型为 `QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `pred`：类型为 `Predicate`。没有默认值，调用时必须提供。传入 `Predicate` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator!=(const QByteArray &lhs, const QString &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QString &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator!=(const QString &lhs, const QString &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QString &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QString &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator!=(const char *const &lhs, const QString &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const char *const &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QString &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator!=(const QString &lhs, const QByteArray &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QString &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator!=(const QString &lhs, const QLatin1StringView &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QString &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QLatin1StringView &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator!=(const QString &lhs, const char *const &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QString &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const char *const &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept, since 6.4] QString operator""_s(const char16_t *str, size_t size)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QString`。
- 参数 `str`：类型为 `const char16_t *`。没有默认值，调用时必须提供。传入 `const char16_t *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `size`：类型为 `size_t`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.9] QString operator+(const QString &lhs, QStringView rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QString`。
- 参数 `lhs`：类型为 `const QString &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `QStringView`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString operator+(QString &&s1, const QString &s2)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QString`。
- 参数 `s1`：类型为 `QString &&`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `s2`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString operator+(const QString &s1, const char *s2)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QString`。
- 参数 `s1`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `s2`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString operator+(const char *s1, const QString &s2)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QString`。
- 参数 `s1`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `s2`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator<(const QByteArray &lhs, const QString &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QString &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator<(const char *const &lhs, const QString &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const char *const &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QString &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator<(const QLatin1StringView &lhs, const QString &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QLatin1StringView &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QString &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator<(const QString &lhs, const QByteArray &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QString &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator<(const QString &lhs, const QLatin1StringView &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QString &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QLatin1StringView &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator<(const QString &lhs, const QString &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QString &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QString &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator<(const QString &lhs, const char *const &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QString &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const char *const &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDataStream &operator<<(QDataStream &stream, const QString &string)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDataStream &`。
- 参数 `stream`：类型为 `QDataStream &`。没有默认值，调用时必须提供。传入 `QDataStream &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `string`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator<=(const QByteArray &lhs, const QString &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QString &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator<=(const QString &lhs, const QString &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QString &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QString &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator<=(const char *const &lhs, const QString &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const char *const &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QString &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator<=(const QLatin1StringView &lhs, const QString &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QLatin1StringView &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QString &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator<=(const QString &lhs, const QByteArray &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QString &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator<=(const QString &lhs, const QLatin1StringView &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QString &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QLatin1StringView &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator<=(const QString &lhs, const char *const &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QString &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const char *const &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator==(const QByteArray &lhs, const QString &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QString &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator==(const QLatin1StringView &lhs, const QString &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QLatin1StringView &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QString &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator==(const QString &lhs, const QByteArray &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QString &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator==(const QString &lhs, const QLatin1StringView &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QString &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QLatin1StringView &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator==(const QString &lhs, const QString &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QString &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QString &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator==(const QString &lhs, const char *const &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QString &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const char *const &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator==(const char *const &lhs, const QString &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const char *const &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QString &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator>(const QByteArray &lhs, const QString &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QString &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator>(const QString &lhs, const QString &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QString &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QString &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator>(const char *const &lhs, const QString &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const char *const &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QString &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator>(const QLatin1StringView &lhs, const QString &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QLatin1StringView &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QString &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator>(const QString &lhs, const QByteArray &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QString &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator>(const QString &lhs, const QLatin1StringView &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QString &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QLatin1StringView &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator>(const QString &lhs, const char *const &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QString &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const char *const &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator>=(const QByteArray &lhs, const QString &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QString &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator>=(const QString &lhs, const QString &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QString &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QString &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator>=(const char *const &lhs, const QString &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const char *const &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QString &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator>=(const QLatin1StringView &lhs, const QString &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QLatin1StringView &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QString &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator>=(const QString &lhs, const QByteArray &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QString &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator>=(const QString &lhs, const QLatin1StringView &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QString &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QLatin1StringView &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool operator>=(const QString &lhs, const char *const &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QString &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const char *const &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDataStream &operator>>(QDataStream &stream, QString &string)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDataStream &`。
- 参数 `stream`：类型为 `QDataStream &`。没有默认值，调用时必须提供。传入 `QDataStream &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `string`：类型为 `QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStringLiteral(str)`

**API 类别：** 宏说明

**中文解读：** `QString::QStringLiteral` 用于执行与“Q、字符串、Literal”相关的操作。调用时要先确认当前状态和 `str` 的有效范围；返回类型是 `未标注`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`由运算符声明决定`。
- 参数 `str`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QT_NO_CAST_FROM_ASCII`

**API 类别：** 宏说明

**中文解读：** 这是 `QString` 的 `ASCII` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QT_NO_CAST_TO_ASCII`

**API 类别：** 宏说明

**中文解读：** 这是 `QString` 的 `ASCII` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QT_RESTRICTED_CAST_FROM_ASCII`

**API 类别：** 宏说明

**中文解读：** 这是 `QString` 的 `ASCII` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const char *qPrintable(const QString &str)`

**API 类别：** 宏说明

**中文解读：** `QString::qPrintable` 用于计算、查询或取得与“q、Printable”相关的操作。调用时要先确认当前状态和 `str` 的有效范围；返回类型是 `const char *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const char *`。
- 参数 `str`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const wchar_t *qUtf16Printable(const QString &str)`

**API 类别：** 宏说明

**中文解读：** `QString::qUtf16Printable` 用于计算、查询或取得与“q、Utf、16、Printable”相关的操作。调用时要先确认当前状态和 `str` 的有效范围；返回类型是 `const wchar_t *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const wchar_t *`。
- 参数 `str`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const char *qUtf8Printable(const QString &str)`

**API 类别：** 宏说明

**中文解读：** `QString::qUtf8Printable` 用于计算、查询或取得与“q、Utf、8、Printable”相关的操作。调用时要先确认当前状态和 `str` 的有效范围；返回类型是 `const char *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const char *`。
- 参数 `str`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `ConstIterator`

**API 类别：** 公有类型

**中文解读：** 这是 `QString` 的 `Const、Iterator` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Iterator`

**API 类别：** 公有类型

**中文解读：** 这是 `QString` 的 `Iterator` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum SectionFlag { SectionDefault, SectionSkipEmpty, SectionIncludeLeadingSep, SectionIncludeTrailingSep, SectionCaseInsensitiveSeps }`

**API 类别：** 公有类型

**中文解读：** 这是 `QString` 暴露的类型声明 `Section、Flag`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags SectionFlags`

**API 类别：** 公有类型

**中文解读：** 这是 `QString` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const_iterator`

**API 类别：** 公有类型

**中文解读：** 这是 `QString` 的 `const、iterator` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const_pointer`

**API 类别：** 公有类型

**中文解读：** 这是 `QString` 的 `const、pointer` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const_reference`

**API 类别：** 公有类型

**中文解读：** 这是 `QString` 的 `const、reference` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const_reverse_iterator`

**API 类别：** 公有类型

**中文解读：** 这是 `QString` 的 `const、reverse、iterator` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `difference_type`

**API 类别：** 公有类型

**中文解读：** 这是 `QString` 的 `difference、类型` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `iterator`

**API 类别：** 公有类型

**中文解读：** 这是 `QString` 的 `iterator` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `pointer`

**API 类别：** 公有类型

**中文解读：** 这是 `QString` 的 `pointer` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `reference`

**API 类别：** 公有类型

**中文解读：** 这是 `QString` 的 `reference` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `reverse_iterator`

**API 类别：** 公有类型

**中文解读：** 这是 `QString` 的 `reverse、iterator` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `size_type`

**API 类别：** 公有类型

**中文解读：** 这是 `QString` 的 `尺寸或数量、类型` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `value_type`

**API 类别：** 公有类型

**中文解读：** 这是 `QString` 的 `值访问、类型` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString chopped(qsizetype len) const &`

**API 类别：** 公有函数

**中文解读：** `QString::chopped` 用于计算、查询或取得与“chopped”相关的操作。调用时要先确认当前状态和 `len` 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数 `len`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.0) QString first(qsizetype n) const &`

**API 类别：** 公有函数

**中文解读：** `QString::first` 用于计算、查询或取得与“首项”相关的操作。调用时要先确认当前状态和 `n` 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数 `n`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.0) QString last(qsizetype n) const &`

**API 类别：** 公有函数

**中文解读：** `QString::last` 用于计算、查询或取得与“末项”相关的操作。调用时要先确认当前状态和 `n` 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数 `n`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString left(qsizetype n) const &`

**API 类别：** 公有函数

**中文解读：** `QString::left` 用于计算、查询或取得与“左侧”相关的操作。调用时要先确认当前状态和 `n` 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数 `n`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.8) qsizetype max_size() const`

**API 类别：** 公有函数

**中文解读：** `QString::max_size` 用于计算、查询或取得与“max、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString mid(qsizetype position, qsizetype n = -1) const &`

**API 类别：** 公有函数

**中文解读：** `QString::mid` 用于计算、查询或取得与“mid”相关的操作。调用时要先确认当前状态和 `position`、`n` 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数 `position`：类型为 `qsizetype`。没有默认值，调用时必须提供。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。
- 参数 `n`：类型为 `qsizetype`。默认值为 `-1`。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.10) QString nullTerminated() const &`

**API 类别：** 公有函数

**中文解读：** `QString::nullTerminated` 用于计算、查询或取得与“null、Terminated”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString right(qsizetype n) const &`

**API 类别：** 公有函数

**中文解读：** `QString::right` 用于计算、查询或取得与“右侧”相关的操作。调用时要先确认当前状态和 `n` 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数 `n`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.0) QString sliced(qsizetype pos, qsizetype n) const &`

**API 类别：** 公有函数

**中文解读：** `QString::sliced` 用于计算、查询或取得与“sliced”相关的操作。调用时要先确认当前状态和 `pos`、`n` 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数 `pos`：类型为 `qsizetype`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。
- 参数 `n`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.0) QString sliced(qsizetype pos) const &`

**API 类别：** 公有函数

**中文解读：** `QString::sliced` 用于计算、查询或取得与“sliced”相关的操作。调用时要先确认当前状态和 `pos` 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数 `pos`：类型为 `qsizetype`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.0) auto tokenize(Needle &&sep, Flags... flags) const &&`

**API 类别：** 公有函数

**中文解读：** 这是转换/映射 API `tokenize`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`auto`。
- 参数 `sep`：类型为 `Needle &&`。没有默认值，调用时必须提供。传入 `Needle &&` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `flags`：类型为 `Flags...`。没有默认值，调用时必须提供。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.9) QString operator+(QStringView lhs, const QString &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QString`。
- 参数 `lhs`：类型为 `QStringView`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QString &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString operator+(const QString &s1, const QString &s2)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QString` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QString`。
- 参数 `s1`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `s2`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

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
