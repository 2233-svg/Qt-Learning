# QDebug

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QDebug` 是 Qt 日志与诊断体系中的类型，用于按类别输出调试、信息、警告或错误消息。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QDebug` 是 Qt 日志与诊断机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** Qt 日志 API 把消息级别、类别、源文件/行号上下文和最终处理器分开。`qDebug`、`qInfo`、`qWarning`、`qCritical` 负责产生消息，分类规则和 message handler 决定输出到哪里、是否过滤或持久化。

**适用场景：** 用分类定义稳定的日志边界，使用合适级别记录状态和错误，必要时安装 handler 写入文件或诊断系统；敏感信息、token、密码不要输出。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要用 qFatal 代替普通错误处理；不要在 handler 里再次触发同类日志；不要把日志文本当作稳定的程序接口；注意 release 构建中的上下文宏和过滤规则。

## 2. 依赖与对象关系

- 头文件：`#include <QDebug>`
- 继承自：QIODeviceBase
- 直接派生类：QQmlInfo

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

Qt 日志 API 把消息级别、类别、源文件/行号上下文和最终处理器分开。`qDebug`、`qInfo`、`qWarning`、`qCritical` 负责产生消息，分类规则和 message handler 决定输出到哪里、是否过滤或持久化。

### 状态、生命周期和线程

**生命周期：** 日志上下文通常是一次消息表达式的临时对象；自定义 message handler 的安装和卸载要覆盖整个使用期，处理器内部不要递归调用会再次触发日志的代码。

**状态与结果：** 日志是否输出受级别、类别规则、编译宏和运行时过滤影响。看到某条消息缺失时，要区分代码没有执行、日志级别被过滤、上下文被关闭和 handler 改写输出。

**线程与事件循环：** 日志可能来自多个线程，handler 必须考虑并发、输出原子性和不能阻塞业务线程；不要在 handler 中访问未加锁的 GUI 控件。

## 3. 直接使用

用分类定义稳定的日志边界，使用合适级别记录状态和错误，必要时安装 handler 写入文件或诊断系统；敏感信息、token、密码不要输出。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

```cpp
#include <QDebug>

qInfo() << "operation started";
qWarning() << "operation failed";
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum VerbosityLevel { MinimumVerbosity, DefaultVerbosity, MaximumVerbosity }`

### 公有函数

- `(since 6.9) QDebug(QByteArray *byteArray)`
- `QDebug(QIODevice *device)`
- `QDebug(QString *string)`
- `QDebug(QtMsgType t)`
- `QDebug(const QDebug &o)`
- `~QDebug()`
- `bool autoInsertSpaces() const`
- `QDebug & maybeQuote(char c = '"')`
- `QDebug & maybeSpace()`
- `QDebug & noquote()`
- `QDebug & nospace()`
- `QDebug & quote()`
- `(since 6.7) bool quoteStrings() const`
- `QDebug & resetFormat()`
- `void setAutoInsertSpaces(bool b)`
- `(since 6.7) void setQuoteStrings(bool b)`
- `void setVerbosity(int verbosityLevel)`
- `QDebug & space()`
- `void swap(QDebug &other)`
- `int verbosity() const`
- `QDebug & verbosity(int verbosityLevel)`
- `(since 6.0) QDebug & operator<<(QByteArrayView t)`
- `QDebug & operator<<(QChar t)`
- `QDebug & operator<<(QLatin1StringView t)`
- `QDebug & operator<<(QStringView s)`
- `(since 6.0) QDebug & operator<<(QUtf8StringView s)`
- `(since 6.7) QDebug & operator<<(T i)`
- `QDebug & operator<<(bool t)`
- `QDebug & operator<<(char t)`
- `QDebug & operator<<(char16_t t)`
- `QDebug & operator<<(char32_t t)`
- `QDebug & operator<<(const QByteArray &t)`
- `QDebug & operator<<(const QString &t)`
- `QDebug & operator<<(const char *t)`
- `(since 6.0) QDebug & operator<<(const char16_t *t)`
- `(since 6.5) QDebug & operator<<(const std::basic_string<Char, Args...> &s)`
- `(since 6.7) QDebug & operator<<(const std::optional<T> &opt)`
- `(since 6.9) QDebug & operator<<(const std::tuple<Ts...> &tuple)`
- `QDebug & operator<<(const void *t)`
- `QDebug & operator<<(double t)`
- `QDebug & operator<<(float t)`
- `QDebug & operator<<(int t)`
- `QDebug & operator<<(long t)`
- `QDebug & operator<<(qint64 t)`
- `QDebug & operator<<(quint64 t)`
- `QDebug & operator<<(short t)`
- `(since 6.5) QDebug & operator<<(std::basic_string_view<Char, Args...> s)`
- `(since 6.6) QDebug & operator<<(std::chrono::duration<Rep, Period> duration)`
- `(since 6.7) QDebug & operator<<(std::nullopt_t)`
- `QDebug & operator<<(unsigned int t)`
- `QDebug & operator<<(unsigned long t)`
- `QDebug & operator<<(unsigned short t)`
- `QDebug & operator=(const QDebug &other)`

### 静态公有成员

- `(since 6.9) QByteArray toBytes(const T &object)`
- `(since 6.0) QString toString(const T &object)`

### 相关非成员函数

- `QDebug operator<<(QDebug debug, const QList<T> &list)`
- `QDebug operator<<(QDebug debug, const QMap<Key, T> &map)`
- `QDebug operator<<(QDebug debug, const QMultiHash<Key, T> &hash)`
- `QDebug operator<<(QDebug debug, const QMultiMap<Key, T> &map)`
- `QDebug operator<<(QDebug debug, const QSet<T> &set)`
- `(since 6.3) QDebug operator<<(QDebug debug, const QVarLengthArray<T, P> &array)`
- `(since 6.9) QDebug operator<<(QDebug debug, const std::array<T, N> &array)`
- `QDebug operator<<(QDebug debug, const std::list<T, Alloc> &vec)`
- `QDebug operator<<(QDebug debug, const std::map<Key, T, Compare, Alloc> &map)`
- `QDebug operator<<(QDebug debug, const std::multimap<Key, T, Compare, Alloc> &map)`
- `(since 6.9) QDebug operator<<(QDebug debug, const std::multiset<Key, Compare, Alloc> &multiset)`
- `QDebug operator<<(QDebug debug, const std::pair<T1, T2> &pair)`
- `(since 6.9) QDebug operator<<(QDebug debug, const std::set<Key, Compare, Alloc> &set)`
- `(since 6.9) QDebug operator<<(QDebug debug, const std::unordered_map<Key, T, Hash, KeyEqual, Alloc> &map)`
- `(since 6.9) QDebug operator<<(QDebug debug, const std::unordered_set<Key, Hash, KeyEqual, Alloc> &unordered_set)`
- `QDebug operator<<(QDebug debug, const std::vector<T, Alloc> &vec)`
- `(since 6.9) QDebug operator<<(QDebug debug, T t)`
- `QDebug operator<<(QDebug debug, const QContiguousCache<T> &cache)`
- `QDebug operator<<(QDebug debug, const QFlags<T> &flags)`
- `QDebug operator<<(QDebug debug, const QHash<Key, T> &hash)`

### 公开宏

- `QDebug qCritical()`
- `QDebug qDebug()`
- `QDebug qFatal()`
- `QDebug qInfo()`
- `QDebug qWarning()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QDebug::VerbosityLevel`

**作用与语义：**

这个枚举描述了冗长程度的范围。
- `QDebug::MinimumVerbosity`：`0`
- `QDebug::DefaultVerbosity`：`2`
- `QDebug::MaximumVerbosity`：`7`

### `[explicit, since 6.9] QDebug::QDebug(QByteArray *byteArray)`

**作用与语义：**

构建一个编写给定`byteArray`的调试流。
数据采用 UTF-8 编码，这可能与 Windows 上的系统位置不同。
使用该构造函数实例化的对象，数据可能被缓冲，直到流被清除（例如使用`Qt::flush`）才写入字节数组。

### `[explicit] QDebug::QDebug(QIODevice *device)`

**作用与语义：**

构建一个写入给定`device`的调试流。

### `[explicit] QDebug::QDebug(QString *string)`

**作用与语义：**

构建一个写入给定`string`的调试流。

### `[explicit] QDebug::QDebug(QtMsgType t)`

**作用与语义：**

构建一个调试流，写入消息类型 `t` 的处理器。

### `QDebug::QDebug(const QDebug &o)`

**作用与语义：**

构建另一个调试流`o`的副本。

### `[noexcept] QDebug::~QDebug()`

**作用与语义：**

清除所有待写入的数据并销毁调试流。

### `bool QDebug::autoInsertSpaces() const`

**作用与语义：**

返回`true`该`QDebug`实例是否会自动在写入之间插入空格。

### `QDebug &QDebug::maybeQuote(char c = '"')`

**作用与语义：**

根据当前自动插入引号的设置，`c`写入一个字符到调试流，并返回对该流的引用。
默认字符是双引号`"`。

### `QDebug &QDebug::maybeSpace()`

**作用与语义：**

根据当前自动插入空格的设置，为调试流写入空格字符，并返回对流的引用。

### `QDebug &QDebug::noquote()`

**作用与语义：**

禁用`QChar`、`QString`和`QByteArray`内容周围自动插入引号字符，并返回流的引用。
禁用引用时，这些类型打印时不带引号字符，且不可打印字符不导出。

### `QDebug &QDebug::nospace()`

**作用与语义：**

禁用自动插入空格，并返回流的引用。

### `QDebug &QDebug::quote()`

**作用与语义：**

支持在`QChar`、`QString`和`QByteArray`内容周围自动插入引号字符，并返回流的引用。
默认情况下已启用引用功能。

### `[noexcept, since 6.7] bool QDebug::quoteStrings() const`

**作用与语义：**

返回 `true` 该`QDebug`实例是否会引用流入的字符串（这是默认）。

### `QDebug &QDebug::resetFormat()`

**作用与语义：**

重置流格式选项，使其恢复到原始构造状态。

### `void QDebug::setAutoInsertSpaces(bool b)`

**作用与语义：**

如果 `b` 为真，则启用写入间自动插入空格;否则禁用自动插入空格。

### `[since 6.7] void QDebug::setQuoteStrings(bool b)`

**作用与语义：**

如果 `b` `true`，则允许引用流入该`QDebug`实例的字符串;否则禁用引用。
默认做法是引用字符串。

### `void QDebug::setVerbosity(int verbosityLevel)`

**作用与语义：**

将流的冗长度设置为`verbosityLevel`。
允许的范围是0到7。默认值是2。

### `QDebug &QDebug::space()`

**作用与语义：**

向调试流写入空格字符，返回对该流的引用。
流会记住未来写入时启用了自动插入空格的功能。

### `[noexcept] void QDebug::swap(QDebug &other)`

**作用与语义：**

将调试流实例与`other`交换。此操作非常快速且从未失败。

### `[static, since 6.9] template <typename T> QByteArray QDebug::toBytes(const T &object)`

**作用与语义：**

这相当于将`object`传递给`QDebug::toString(object).toUtf8()`，但效率更高。

### `[static, since 6.0] template <typename T> QString QDebug::toString(const T &object)`

**作用与语义：**

流会`object`到一个操作字符串的 `QDebug` 实例，然后返回该字符串。
该函数适用于需要对象文本表示用于调试但无法使用`operator<<`的情况。例如：
字符串通过`nospace()`进行流式传输。

**官方示例：**

```cpp
 QString str = QDebug::toString(list);
```

### `int QDebug::verbosity() const`

**作用与语义：**

返回调试流的冗长度。
流式操作员可以检查该值，判断是否需要冗长输出，并根据电平打印更多信息。数值越高表示需要更多信息。
允许的范围是0到7。默认值是2。

### `QDebug &QDebug::verbosity(int verbosityLevel)`

**作用与语义：**

将流的冗长度设置为`verbosityLevel`，并返回流的引用。
允许的范围是0到7。默认值是2。

### `[since 6.0] QDebug &QDebug::operator<<(QByteArrayView t)`

**作用与语义：**

将观察到的字节数组`t`的数据写入流，并返回流的引用。
通常，`QDebug` 会打印引号内的数据，并将控制字符或非 US-ASCII 字符转换为其 C 转义序列（\xAB）。这样，输出始终保持 7 位干净，字符串可以从输出复制并粘贴回 C 源，如有必要。
要打印不可打印的字符而无需变换，请启用`noquote()`功能。请注意，有些`QDebug`后端可能不是8位干净的。
请参见`QByteArray`重载的例子。

### `QDebug &QDebug::operator<<(QChar t)`

**作用与语义：**

将字符 `t` 写入流中，并返回该流的引用。通常，`QDebug` 会将控制字符和非美国 ASCII 字符打印为其 C 转义序列或其 Unicode 值（\u1234）。要在不进行转换的情况下打印不可打印字符，请启用 `noquote()` 功能，但请注意，一些 `QDebug` 后端可能不是 8 位清晰的，可能无法表示 `t`。

### `QDebug &QDebug::operator<<(QLatin1StringView t)`

**作用与语义：**

将字符串`t`写入流，并返回流的引用。通常，`QDebug`将字符串置于引号内，并将不可打印字符转换为其Unicode值（\u1234）。
要打印不可打印字符而无需变换，请启用`noquote()`功能。注意，一些`QDebug`后端可能不是8位干净的。
比如 `QString` overload。

### `QDebug &QDebug::operator<<(QStringView s)`

**作用与语义：**

将字符串视图 `s` 写入流，并返回流的引用。通常，`QDebug` 将字符串印入引号内，并将不可打印字符转换为其 Unicode 值（\u1234）。
要打印不可打印的字符而无需变换，请启用`noquote()`功能。注意，一些`QDebug`后端可能不是8位干净的。
请参见`QString`重载的例子。

### `[since 6.0] QDebug &QDebug::operator<<(QUtf8StringView s)`

**作用与语义：**

将字符串视图 `s` 写入流，并返回流的引用。
通常，`QDebug` 打印引号内的数据，并将控制字符或非美国 ASCII 字符转换为其 C 转义序列（\xAB）。这样，输出始终保持 7 位干净，字符串可以从输出复制并粘贴回 C 源码（如有需要）。
要打印不可打印字符而无需变换，请启用`noquote()`功能。注意，一些`QDebug`后端可能不是8位干净的。

### `[since 6.7] template <typename T, QDebug::if_quint128<T> = true> QDebug &QDebug::operator<<(T i)`

**作用与语义：**

打印128位整数`i`的文本表示。
注意：该操作符仅在 Qt 支持 128 位整数类型时可用。如果您的构建中有 128 位整数类型，但编译时 Qt 库未支持，操作符将打印警告。
注意：由于该算符是函数模板，其参数不进行隐式转换。它必须恰好是 qint128/quint128。

### `QDebug &QDebug::operator<<(bool t)`

**作用与语义：**

打印128位整数`i`的文本表示。
注意：该操作符仅在 Qt 支持 128 位整数类型时可用。如果您的构建中有 128 位整数类型，但编译时 Qt 库未支持，操作符将打印警告。
注意：由于该算符是函数模板，其参数不进行隐式转换。它必须恰好是 qint128/quint128。

### `QDebug &QDebug::operator<<(char t)`

**作用与语义：**

将布尔值 `t` 写入流并返回对该流的引用。

### `QDebug &QDebug::operator<<(char16_t t)`

**作用与语义：**

将字符 `t` 写入流中，并返回对该流的引用。

### `QDebug &QDebug::operator<<(char32_t t)`

**作用与语义：**

将UTF-16字符`t`写入流，并返回流的引用。

### `QDebug &QDebug::operator<<(const QByteArray &t)`

**作用与语义：**

将UTF-32字符`t`写入流，并返回流的引用。

### `QDebug &QDebug::operator<<(const QString &t)`

**作用与语义：**

将字节数组 `t` 写入流中，并返回对该流的引用。通常，`QDebug` 会在引号内打印数组，并将控制字符或非美国 ASCII 字符转换为其 C 转义序列（\xAB）。这样，输出始终是 7 位清晰的，并且字符串可以从输出中复制并粘贴回 C 源代码中（如有必要）。
要打印不可打印字符而不进行转换，请启用 `noquote()` 功能。请注意，某些 `QDebug` 后端可能不是 8 位清晰的。
输出示例：
注意 `QDebug` 如何以 C 语言和 C++ 语言连接字符串字面量的方式关闭并重新打开字符串，从而使字母 'b' 不会被解释为前一个十六进制转义序列的一部分。

**官方示例：**

```cpp
 QByteArray ba;

 ba = "a";
 qDebug().noquote() << ba;    // prints: a
 qDebug() << ba;              // prints: "a"

 ba = "\"a\r\n\"";
 qDebug() << ba;              // prints: "\"a\r\n\""

 ba = "\033";                 // escape character
 qDebug() << ba;              // prints: "\x1B"

 ba = "\xC3\xA1";
 qDebug() << ba;              // prints: "\xC3\xA1"

 ba = QByteArray("a\0b", 3);
 qDebug() << ba;               // prints: "\a\x00""b"
```

### `QDebug &QDebug::operator<<(const char *t)`

**作用与语义：**

将字符串 `t` 写入流，并返回流的引用。通常，`QDebug` 将字符串印入引号内，并将不可打印字符转换为其 Unicode 值（\u1234）。
要打印不可打印字符而不进行变换，请启用`noquote()`功能。注意，一些`QDebug`后端可能不是8位干净的。
输出示例：

**官方示例：**

```cpp
 QString s;

 s = "a";
 qDebug().noquote() << s;    // prints: a
 qDebug() << s;              // prints: "a"

 s = "\"a\r\n\"";
 qDebug() << s;              // prints: "\"a\r\n\""

 s = "\033";                 // escape character
 qDebug() << s;              // prints: "\u001B"

 s = "\u00AD";               // SOFT HYPHEN
 qDebug() << s;              // prints: "\u00AD"

 s = "\u00E1";               // LATIN SMALL LETTER A WITH ACUTE
 qDebug() << s;              // prints: "á"

 s = "a\u0301";              // "a" followed by COMBINING ACUTE ACCENT
 qDebug() << s;              // prints: "á";

 s = "\u0430\u0301";         // CYRILLIC SMALL LETTER A followed by COMBINING ACUTE ACCENT
 qDebug() << s;              // prints: "а́"
```

### `[since 6.0] QDebug &QDebug::operator<<(const char16_t *t)`

**作用与语义：**

将终止为“\0”的UTF-8字符串`t`写入流，并返回流的引用。该字符串在输出时从不被引用或转义。注意`QDebug`内部缓冲为UTF-16，可能需要使用本地编解码器转换为8位以使用某些后端，这可能导致输出杂乱（如mojibake）。建议限制使用美国ASCII字符串。

### `[since 6.5] template <typename Char, typename... Args> QDebug &QDebug::operator<<(std::basic_string_view<Char, Args...> s)`

**作用与语义：**

将u'\0'终止的UTF-16字符串`t`写入流，并返回流的引用。该字符串在输出时绝不被引号或转义。注意`QDebug`内部缓冲为UTF-16，可能需要使用本地编解码器转换为8位以使用某些后端，这可能导致输出杂乱（如mojibake）。建议限制使用US-ASCII字符串。

### `[since 6.7] template <typename T, QDebug::if_streamable<T> = true> QDebug &QDebug::operator<<(const std::optional<T> &opt)`

**作用与语义：**

将字符串或字符串视图`s`写入流，并返回流的引用。
这些算符只有在 `Char` 是以下之一时才参与重载决议。
- 红点
- char8_t（仅限C 20）
- char16_t
- char32_t
- wchar_t

### `[since 6.9] template <typename... Ts, QDebug::if_streamable<Ts...> = true> QDebug &QDebug::operator<<(const std::tuple<Ts...> &tuple)`

**作用与语义：**

将字符串或字符串视图`s`写入流，并返回流的引用。
这些算符只有在 `Char` 是以下之一时才参与重载决议。
- 红点
- char8_t（仅限C 20）
- char16_t
- char32_t
- wchar_t

### `QDebug &QDebug::operator<<(const void *t)`

**作用与语义：**

将 `opt`（如果未设置，则为 `nullopt`）的内容写入此流。`T` 需要支持流式写入 `QDebug`。

### `QDebug &QDebug::operator<<(double t)`

**作用与语义：**

将 `tuple` 的内容写入流。所有 `Ts...` 都需要支持流式写入 `QDebug`。

### `QDebug &QDebug::operator<<(float t)`

**作用与语义：**

写入指向流的指针`t`，并返回流的引用。

### `QDebug &QDebug::operator<<(int t)`

**作用与语义：**

将64位浮点数`t`写入流，并返回流的引用。

### `QDebug &QDebug::operator<<(long t)`

**作用与语义：**

将32位浮点数`t`写入流，并返回流的引用。

### `QDebug &QDebug::operator<<(qint64 t)`

**作用与语义：**

将带符号整数`t`写入流，并返回流的引用。

### `QDebug &QDebug::operator<<(quint64 t)`

**作用与语义：**

写入带符号的长整数`t`，并返回流的引用。

### `QDebug &QDebug::operator<<(short t)`

**作用与语义：**

将有符号的64位整数写入`t`，并返回流的引用。

### `[since 6.6] template <typename Rep, typename Period> QDebug &QDebug::operator<<(std::chrono::duration<Rep, Period> duration)`

**作用与语义：**

然后将无符号的64位整数写入`t`，并返回流的引用。

### `[since 6.7] QDebug &QDebug::operator<<(std::nullopt_t)`

**作用与语义：**

将带符号的短整数`t`写入流，并返回流的引用。

### `QDebug &QDebug::operator<<(unsigned int t)`

**作用与语义：**

打印时间时长`duration`流，并返回流的引用。打印字符串是周期的数字表示，后加上时间单位，类似于C标准库用`std::ostream`生成的。
该单位并非本地化。

### `QDebug &QDebug::operator<<(unsigned long t)`

**作用与语义：**

写入空选（nullopt）到流中。

### `QDebug &QDebug::operator<<(unsigned short t)`

**作用与语义：**

然后写入无符号整数`t`，返回流的引用。

### `QDebug &QDebug::operator=(const QDebug &other)`

**作用与语义：**

将`other`调试流分配给该流，并返回对该流的引用。

### `template <typename T> QDebug operator<<(QDebug debug, const QList<T> &list)`

**作用与语义：**

然后写入无符号的长整数`t`，返回流的引用。

### `template <typename Key, typename T> QDebug operator<<(QDebug debug, const QMap<Key, T> &map)`

**作用与语义：**

然后写入无符号的短整数 `t` 到流中，并返回流的引用。

### `template <typename Key, typename T> QDebug operator<<(QDebug debug, const QMultiHash<Key, T> &hash)`

**作用与语义：**

将 `list` 的内容写入 `debug`。`T` 需要支持流式写入 `QDebug`。

### `template <typename Key, typename T> QDebug operator<<(QDebug debug, const QMultiMap<Key, T> &map)`

**作用与语义：**

将 `map` 的内容写入 `debug`。`Key` 和 `T` 都需要支持流式传输到 `QDebug`。

### `template <typename T> QDebug operator<<(QDebug debug, const QSet<T> &set)`

**作用与语义：**

将 `hash` 的内容写入 `debug`。`Key` 和 `T` 都需要支持流式传输到 `QDebug`。

### `[since 6.3] template <typename T, qsizetype P> QDebug operator<<(QDebug debug, const QVarLengthArray<T, P> &array)`

**作用与语义：**

将 `map` 的内容写入 `debug`。`Key` 和 `T` 都需要支持流式传输到 `QDebug`。

### `[since 6.9] template <typename T, std::size_t N> QDebug operator<<(QDebug debug, const std::array<T, N> &array)`

**作用与语义：**

将 `set` 的内容写入 `debug`。`T` 需要支持流式写入 `QDebug`。

### `template <typename T, typename Alloc> QDebug operator<<(QDebug debug, const std::list<T, Alloc> &vec)`

**作用与语义：**

将 `array` 的内容写入 `debug`。`T` 需要支持流式写入 `QDebug`。

### `template < typename Key, typename T, typename Compare, typename Alloc > QDebug operator<<(QDebug debug, const std::map<Key, T, Compare, Alloc> &map)`

**作用与语义：**

将 `array` 的内容写入 `debug`。`T` 需要支持流式写入 `QDebug`。

### `template < typename Key, typename T, typename Compare, typename Alloc > QDebug operator<<(QDebug debug, const std::multimap<Key, T, Compare, Alloc> &map)`

**作用与语义：**

将列表`vec`的内容写入`debug`。`T`需要支持流媒体传输到`QDebug`。

### `[since 6.9] template < typename Key, typename Compare, typename Alloc > QDebug operator<<(QDebug debug, const std::multiset<Key, Compare, Alloc> &multiset)`

**作用与语义：**

将 `map` 的内容写入 `debug`。`Key` 和 `T` 都需要支持流式传输到 `QDebug`。

### `template <typename T1, typename T2> QDebug operator<<(QDebug debug, const std::pair<T1, T2> &pair)`

**作用与语义：**

将 `map` 的内容写入 `debug`。`Key` 和 `T` 都需要支持流式传输到 `QDebug`。

### `[since 6.9] template < typename Key, typename Compare, typename Alloc > QDebug operator<<(QDebug debug, const std::set<Key, Compare, Alloc> &set)`

**作用与语义：**

将 `multiset` 的内容写入 `debug`。`Key` 类型需要支持流式写入 `QDebug`。

### `[since 6.9] template < typename Key, typename T, typename Hash, typename KeyEqual, typename Alloc > QDebug operator<<(QDebug debug, const std::unordered_map<Key, T, Hash, KeyEqual, Alloc> &map)`

**作用与语义：**

将 `pair` 的内容写入 `debug`。`T1` 和 `T2` 都需要支持流式写入 `QDebug`。

### `[since 6.9] template < typename Key, typename Hash, typename KeyEqual, typename Alloc > QDebug operator<<(QDebug debug, const std::unordered_set<Key, Hash, KeyEqual, Alloc> &unordered_set)`

**作用与语义：**

将 `set` 的内容写入 `debug`。`Key` 类型需要支持流式写入 `QDebug`。

### `template <typename T, typename Alloc> QDebug operator<<(QDebug debug, const std::vector<T, Alloc> &vec)`

**作用与语义：**

将 `map` 的内容写入 `debug`。`Key` 和 `T` 都需要支持流式传输到 `QDebug`。

### `[since 6.9] template <typename T, QDebug::if_ordering_type<T> = true> QDebug operator<<(QDebug debug, T t)`

**作用与语义：**

将 `unordered_set` 的内容写入 `debug`。`Key` 类型需要支持流式写入 `QDebug`。

### `template <typename T> QDebug operator<<(QDebug debug, const QContiguousCache<T> &cache)`

**作用与语义：**

将矢量 `vec` 的内容写入 `debug`。`T`需要支持流媒体进入`QDebug`。

### `template <typename T> QDebug operator<<(QDebug debug, const QFlags<T> &flags)`

**作用与语义：**

将Qt或标准排序值`t`打印到`debug`对象。
只有当`T`属于<Qt/Std>：：<弱/部分/强>_ordering时，才参与超载解析。

### `template <typename Key, typename T> QDebug operator<<(QDebug debug, const QHash<Key, T> &hash)`

**作用与语义：**

将 `cache` 的内容写入 `debug`。`T` 需要支持流式写入 `QDebug`。

### `QDebug qCritical()`

**作用与语义：**

返回一个`QDebug`对象，将关键消息日志到中央消息处理程序。
使用 qCritical() 是 `qCritical`（const char *， ...）的替代方案，后者遵循 printf 范式。
请注意，`QDebug`和类型特定的流操作符确实会添加各种格式化，使调试消息更易阅读。更多详情请参见格式选项文档。
为了调试目的，有时允许程序在关键消息时中止是方便的。这样你就可以检查核心转储，或附加调试器——参见`qFatal()`。要实现此功能，将环境变量`QT_FATAL_CRITICALS`设置为数字`n`。程序在第n次关键消息时终止。也就是说，如果环境变量设置为1，则在第一次调用时终止;如果包含值10，则在第10次调用时退出。环境变量中的任何非数字值等价于1。
注意：该宏是线程安全的。

**官方示例：**

```cpp
 qCritical() << "Brush:" << myQBrush << "Other value:" << i;
```

### `QDebug qDebug()`

**作用与语义：**

返回一个`QDebug`对象，将调试消息记录给中央消息处理器。
使用 qDebug() 是 `qDebug`（const char *， ...）的替代方案，后者遵循 printf 范式。
请注意，`QDebug`和类型专用流操作符会添加各种格式，使调试消息更易阅读。更多细节请参见格式选项文档。
如果`QT_NO_DEBUG_OUTPUT`在编译时定义了，这个函数就没有任何作用。
注意：该宏是线程安全的。

**官方示例：**

```cpp
 qDebug() << "Brush:" << myQBrush << "Other value:" << i;
```

### `QDebug qFatal()`

**作用与语义：**

返回一个`QDebug`对象，将致命消息记录给中央消息处理器。
使用 qFatal() 是 `qFatal`（const char *， ...）的替代方案，后者遵循 printf 范式。
请注意，`QDebug`和类型特定的流运算符确实会添加各种格式化，使调试消息更易阅读。更多细节请参见格式选项文档。
如果你使用默认消息处理程序，返回的流会中止以创建核心转储。在 Windows 上，对于调试构建，这个函数会报告一个_CRT_ERROR，使你能够将调试器连接到应用程序。
注意：该宏是线程安全的。

### `QDebug qInfo()`

**作用与语义：**

返回一个`QDebug`对象，将信息消息记录给中央消息处理器。
使用 qInfo() 是 `qInfo`（const char *， ...）的替代方案，后者遵循 printf 范式。
请注意，`QDebug`和类型特定的流操作符会添加各种格式，使调试消息更易阅读。更多细节请参见格式选项文档。
如果`QT_NO_INFO_OUTPUT`在编译过程中被定义，这个函数就没有任何作用。
注意：该宏是线程安全的。

**官方示例：**

```cpp
 qInfo() << "Brush:" << myQBrush << "Other value:" << i;
```

### `QDebug qWarning()`

**作用与语义：**

返回一个`QDebug`对象，将警告消息记录给中央消息处理器。
使用 qWarning() 是 `qWarning`（const char *， ...）的替代方案，后者遵循 printf 范式。
请注意，`QDebug`和类型专用流操作符会添加各种格式，使调试消息更易阅读。更多详情请参见格式选项文档。
如果`QT_NO_WARNING_OUTPUT`在编译过程中被定义，这个函数就没有任何作用。
为了调试目的，有时允许程序在警告消息时中止。这样你可以检查核心转储，或附加调试器——参见`qFatal()`。启用此功能，将环境变量 `QT_FATAL_WARNINGS` 设置为数字 `n`。程序在第 n 次警告时终止。也就是说，如果环境变量设置为 1，则在第一次调用时终止;如果包含值 10，则在第十次调用时退出。环境变量中的任何非数字值等价于 1。
注意：该宏是线程安全的。

**官方示例：**

```cpp
 qWarning() << "Brush:" << myQBrush << "Other value:" << i;
```

### `(since 6.5) QDebug & operator<<(const std::basic_string<Char, Args...> &s)`

**作用与语义：**

给`debug`写`flags`。

## 6. 深入实践与常见坑

### 生命周期和资源边界

日志上下文通常是一次消息表达式的临时对象；自定义 message handler 的安装和卸载要覆盖整个使用期，处理器内部不要递归调用会再次触发日志的代码。

### 状态和错误边界

日志是否输出受级别、类别规则、编译宏和运行时过滤影响。看到某条消息缺失时，要区分代码没有执行、日志级别被过滤、上下文被关闭和 handler 改写输出。

### 线程边界

日志可能来自多个线程，handler 必须考虑并发、输出原子性和不能阻塞业务线程；不要在 handler 中访问未加锁的 GUI 控件。

### 最容易出现的错误

不要用 qFatal 代替普通错误处理；不要在 handler 里再次触发同类日志；不要把日志文本当作稳定的程序接口；注意 release 构建中的上下文宏和过滤规则。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QDebug` 所属机制类型：Qt 日志与诊断机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
