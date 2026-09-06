# QTime

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 一天中的时间值类型，负责时间的校验、加减、比较、解析和格式化。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QTime`：一天中的时间值类型，负责时间的校验、加减、比较、解析和格式化。

**内部模型：** 这类类型通常可以按值传递、复制和返回。许多 Qt 容器、字符串和图像采用隐式共享：复制时共享数据，发生写操作时才 detach。这样便于 API 传值，但获取原始指针或长期持有引用时必须考虑对象修改和生命周期。

**适用场景：** 先确认值的有效性和表示格式，再调用查询、转换或修改 API；处理文本时区分 Unicode 和字节编码，处理图像时确认 format，处理 URL/路径时使用 Qt 的解析 API 而不是手写字符串规则。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要把空值当成业务成功；不要保存临时对象的内部指针；不要把 QString 当二进制缓冲区；不要假定隐式共享让并发写入自动安全。

## 2. 依赖与对象关系

- 头文件：`#include <QTime>`
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

### 公有函数

- `QTime()`
- `QTime(int h, int m, int s = 0, int ms = 0)`
- `QTime addMSecs(int ms) const`
- `QTime addSecs(int s) const`
- `int hour() const`
- `bool isNull() const`
- `bool isValid() const`
- `int minute() const`
- `int msec() const`
- `int msecsSinceStartOfDay() const`
- `int msecsTo(QTime t) const`
- `int second() const`
- `int secsTo(QTime t) const`
- `bool setHMS(int h, int m, int s, int ms = 0)`
- `QString toString(const QString &format) const`
- `QString toString(QStringView format) const`
- `QString toString(Qt::DateFormat format = Qt::TextDate) const`

### 静态公有成员

- `QTime currentTime()`
- `QTime fromMSecsSinceStartOfDay(int msecs)`
- `QTime fromString(const QString &string, const QString &format)`
- `(since 6.0) QTime fromString(QStringView string, QStringView format)`
- `(since 6.0) QTime fromString(QStringView string, Qt::DateFormat format = Qt::TextDate)`
- `(since 6.0) QTime fromString(const QString &string, QStringView format)`
- `QTime fromString(const QString &string, Qt::DateFormat format = Qt::TextDate)`
- `bool isValid(int h, int m, int s, int ms = 0)`

### 相关非成员函数

- `bool operator!=(const QTime &lhs, const QTime &rhs)`
- `bool operator<(const QTime &lhs, const QTime &rhs)`
- `QDataStream & operator<<(QDataStream &out, QTime time)`
- `bool operator<=(const QTime &lhs, const QTime &rhs)`
- `bool operator==(const QTime &lhs, const QTime &rhs)`
- `bool operator>(const QTime &lhs, const QTime &rhs)`
- `bool operator>=(const QTime &lhs, const QTime &rhs)`
- `QDataStream & operator>>(QDataStream &in, QTime &time)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[constexpr] QTime::QTime()`

**作用与语义：**

构造一个空时间对象。对于空时间，`isNull()`返回`true`，`isValid()`返回`false`。如果你需要零时间，可以使用QTime（0， 0）。关于一天的开始，请参见`QDate::startOfDay()`。

### `QTime::QTime(int h, int m, int s = 0, int ms = 0)`

**作用与语义：**

构建时间，时`h`、分钟`m`、秒`s`和毫秒`ms`。
`h`必须在0到23的范围内，`m`和`s`必须在0到59之间，`ms`必须在0到999之间。

### `QTime QTime::addMSecs(int ms) const`

**作用与语义：**

返回一个`QTime`对象，其时间比该对象的时间晚`ms`毫秒（或如果`ms`为负则更早）。
请注意，如果超过午夜，时间会被终止。请参见`addSecs()`示例。
如果该时间无效，则返回空时间。

### `QTime QTime::addSecs(int s) const`

**作用与语义：**

返回一个`QTime`对象，时间比该对象的时间晚`s`秒（如果`s`为负则更早）。
注意，如果超过午夜，时间会结束。
如果该时间无效，则返回空时间。

**官方示例：**

```cpp
 QTime n(14, 0, 0);                // n == 14:00:00
 QTime t;
 t = n.addSecs(70);                // t == 14:01:10
 t = n.addSecs(-70);               // t == 13:58:50
 t = n.addSecs(10 * 60 * 60 + 5);  // t == 00:00:05
 t = n.addSecs(-15 * 60 * 60);     // t == 23:00:00
```

### `[static] QTime QTime::currentTime()`

**作用与语义：**

返回系统时钟报告的当前时间。
注意，准确度取决于底层操作系统的精度;并非所有系统都提供1毫秒的精度。
此外，currentTime()仅在每天内增加;每过一次午夜，时间会下降24小时;此外，如果发生夏令时过渡，当前时间的变化可能与已经过时间不符。

### `[static constexpr] QTime QTime::fromMSecsSinceStartOfDay(int msecs)`

**作用与语义：**

返回一个新的`QTime`实例，时间设置为自当天开始以来的`msecs`数，即自00：00：00起。
如果`msecs`超出有效范围，将返回无效`QTime`。

### `[static] QTime QTime::fromString(const QString &string, const QString &format)`

**作用与语义：**

返回`string`所表示的`QTime`，使用给定的`format`;如果字符串无法解析，则返回无效时间。
这些表达可用于格式：
- `Expression`：输出
- `h`：无前置零的整点（AM/PM显示时为0至23或1至12）
- `hh`：前置零的整点（00到23，或如果是AM/PM显示则为01到12）
- `H`：无前置零的整点（0到23，即使显示AM/PM时段）
- `HH`：带零前置的整点（00到23，即使显示AM/PM时段）
- `m`：无前导零的分钟（0到59）
- `mm`：前置零的分钟（00至59）
- `s`：整秒，无前置零（0到59）
- `ss`：整秒，适用时前置零（00至59）
- `z or zz`：秒的分数部分，通常跟随小数点，无需尾随零（0到999）。因此`"s.z"`与秒匹配，最多三位小分部分提供毫秒精度，无需尾随零。例如，`"s.z"`会识别`"00.250"`或`"0.25"`表示时间的四分之一秒。
- `zzz`：秒的三位数小数部分，精度至毫秒级，包括尾随零（如000到999）。例如，`"ss.zzz"`会拒绝`"0.25"`但识别`"00.250"`表示时间的四分之一秒。
- `AP, A, ap, a, aP or Ap`：“AM”表示12：00之前的时间，或“PM”表示较晚时间，且不区分大小写。
所有其他输入字符都将被视为文本。任何非空的字符序列如果被单引号包围，也会被当作文本处理（去掉引号），不会被解释为表达式。
如果格式不满足，返回无效`QTime`。不期望给出前置零（h、m、s和z）的表达式是贪婪的。这意味着即使这超出了接受值范围，且其他部分的数字太少，它们仍会使用两位数字（z则为三位）。例如，以下字符串可能代表00：07：10，但m会抓取两个数字，导致时间无效：
格式中未表示的任何字段将被设为零。例如：
注意：如果要识别本地化的am或pm格式（AP、AP、Ap、aP、A或a格式），请使用`QLocale::system()`.toTime()。
注意：如果使用该格式字符重复次数超过表中最长表达式，该格式部分将被读取为多个表达式，且之间无分隔符;最长的表达式可能重复次数与其副本数量相等，结尾剩余表达式可能较短。因此`'HHHHH'`匹配`"08088"`或`"080808"`，并将小时设为8;如果时间串包含“070809”，则“匹配”但结果不一致，导致时间无效。

**官方示例：**

```cpp
 QTime time = QTime::fromString("1mm12car00", "m'mm'hcarss");
 // time is 12:01.00
```

### `[static, since 6.0] QTime QTime::fromString(QStringView string, QStringView format)`

**作用与语义：**

注意：该功能会超载`QTime::fromString()`。

### `[static, since 6.0] QTime QTime::fromString(QStringView string, Qt::DateFormat format = Qt::TextDate)`

**作用与语义：**

注意：该功能会超载`QTime::fromString()`。

### `[static, since 6.0] QTime QTime::fromString(const QString &string, QStringView format)`

**作用与语义：**

注意：该功能会超载`QTime::fromString()`。

### `[static] QTime QTime::fromString(const QString &string, Qt::DateFormat format = Qt::TextDate)`

**作用与语义：**

返回`string`中表示的时间，作为`QTime`，使用给定的`format`;如果无法返回，则返回无效时间。

### `int QTime::hour() const`

**作用与语义：**

返回小时部分（0到23）。
如果时间无效，则返回-1。

### `[constexpr] bool QTime::isNull() const`

**作用与语义：**

如果时间为空（即`QTime`对象是用默认构造函数构造的），则返回`true`;否则返回为假。空时间也是一个无效时间。

### `bool QTime::isValid() const`

**作用与语义：**

如果时间有效，返回`true`;否则返回`false`。例如，时间23：30：55.746有效，但24：12：30无效。

### `[static] bool QTime::isValid(int h, int m, int s, int ms = 0)`

**作用与语义：**

如果指定时间有效，返回`true`;否则返回假。
如果`h`在0到23之间，`m`和`s`在0到59之间，`ms`在0到999之间，则该时间有效。
注意：该功能会让`QTime::isValid()`重载。

**官方示例：**

```cpp
 QTime::isValid(21, 10, 30); // returns true
 QTime::isValid(22, 5,  62); // returns false
```

### `int QTime::minute() const`

**作用与语义：**

返回时间的分钟部分（0到59）。
如果时间无效，则返回-1。

### `int QTime::msec() const`

**作用与语义：**

返回毫秒部分（0到999）的时间。
如果时间无效，则返回-1。

### `[constexpr] int QTime::msecsSinceStartOfDay() const`

**作用与语义：**

返回自当天开始以来的毫秒数，即自00：00：00起。

### `int QTime::msecsTo(QTime t) const`

**作用与语义：**

返回从该时间到`t`的毫秒数。如果`t`早于此时间，返回的毫秒数为负数。
由于`QTime`测量的是一天内的时间，而一天中有86400秒，结果总是在-86400000到8640000毫秒之间。
如果任一时间无效，则返回0。

### `int QTime::second() const`

**作用与语义：**

返回时间的第二部分（0到59）。
如果时间无效，则返回-1。

### `int QTime::secsTo(QTime t) const`

**作用与语义：**

返回从该时间到`t`的秒数。如果`t`早于此时间，返回的秒数为负数。
由于`QTime`测量的是一天内的时间，而一天中有86400秒，结果总是在-86400到86400之间。
secsTo() 不考虑毫秒。
如果任一时间无效，则返回0。

### `bool QTime::setHMS(int h, int m, int s, int ms = 0)`

**作用与语义：**

时间设置为小时`h`、分钟`m`、秒`s`和毫秒`ms`。
`h`必须在0到23的范围内，`m`和`s`必须在0到59之间，`ms`必须在0到999之间。如果设定时间有效，返回`true`;否则返回`false`。

### `QString QTime::toString(QStringView format) const`

**作用与语义：**

返回表示时间的字符串。
`format`参数决定了结果字符串的格式。如果时间无效，将返回空字符串。
这些表达可以使用：
- `Expression`：输出
- `h`：无前置零的整点（0到23，或如果是AM/PM显示，则为1到12）
- `hh`：前置零的整点（00到23，或如果显示为01到12，则为AM/PM显示）
- `H`：无前置零的整点（0到23，即使显示AM/PM时段）
- `HH`：带零前置的整点（00到23，即使显示AM/PM也如此）
- `m`：无前置零的分钟（0到59）
- `mm`：前置零的分钟（00至59）
- `s`：整秒，无前置零（0到59）
- `ss`：整秒，适用时首零（00至59）
- `z or zz`：秒的分数部分，位于小数点之后，不带尾随零。因此`"s.z"`以完全可用的毫秒精度报告秒数，没有尾随零（0到999）。例如，`"s.z"`会在一分钟中四分之一秒产生`"0.25"`。
- `zzz`：秒的分数部分，精确到毫秒级，包括适用的尾随零（000到999）。例如，`"ss.zzz"`会在一分钟中四分之一秒产生`"00.250"`。
- `AP or A`：使用AM/PM显示。`A/AP`将被“AM”或“PM”替换。在本地化形式（仅适用于`QLocale::toString()`）中，适合本地的文本转换为大写字母。
- `ap or a`：使用上午/下午显示。`a/ap`将被“am”或“pm”替换。在本地化形式（仅适用于`QLocale::toString()`）中，适合本地的文本会转换为小写。
- `aP or Ap`：使用AM/PM显示（自6.3版本起）。`aP/Ap`将被“AM”或“PM”取代。在本地化形式（仅与`QLocale::toString()`相关）中，使用本地适宜文本（由`QLocale::amText()`或`QLocale::pmText()`返回）且不改变大小写。
- `t`：时区缩写（例如“CEST”）。注意时区缩写并非唯一。特别是，`fromString()`无法解析此缩写。
- `tt`：时区偏移于UTC，时分与分钟之间无冒号（例如“0200”）。
- `ttt`：时区偏移于UTC，时分和分钟之间加冒号（例如“02：00”）。
- `tttt`：时区名称，由`QTimeZone::displayName()`提供，`QTimeZone::LongName`类型。这可能取决于所使用的操作系统。如果没有此类名称，可以使用该区域的IANA ID（如“Europe/Berlin”）。它可能无法显示日期时间是夏令时还是标准时间，如果日期时间落在一小时内，且两者之间有过渡，可能会产生歧义。
注意：要获取本地化的AM或PM格式（`AP`、`ap`、`A`、`a`、`aP`或`Ap`格式）或时区表示（`t`格式），请使用`QLocale::system()`。`toString()`。
当无法确定时区或没有合适的表示时，可以跳过表示时区的 `t` 形式。有关返回空字符串时的详细信息，请参见`QTimeZone::displayName()`。
任何非空的单引号字符序列都会被逐字包含在输出字符串中（去掉引号），即使其中包含格式化字符。两个连续的单引号（“'”）在输出中被一个引号替换。格式字符串中的所有其他字符都被逐字包含在输出字符串中。
支持无分隔符的格式（例如“hhmm”），但使用时必须谨慎，因为生成字符串并不总是可靠可读（例如，如果“Hm”生成“212”，可能意味着02：12或21：02）。
示例格式字符串（假设`QTime`为14：13：09.042）。
- `Format`：结果
- `hh:mm:ss.zzz`：14：13：09.042
- `h:m:s ap`：下午2：13：9
- `H:m:s a`：下午14：13：9
注意：如果使用该格式字符重复次数超过表中最长表达式，该格式部分将被读取为多个表达式，且无分隔符;最长的表达式可能重复次数与其副本数量相等，结尾剩余表达式可能较短。因此，08：00 时间的`'HHHHH'`会对输出贡献`"08088"`。

### `QString QTime::toString(Qt::DateFormat format = Qt::TextDate) const`

**作用与语义：**

返回表示时间的字符串。
`format`参数决定了结果字符串的格式。如果时间无效，将返回空字符串。
这些表达可以使用：
- `Expression`：输出
- `h`：无前置零的整点（0到23，或如果是AM/PM显示，则为1到12）
- `hh`：前置零的整点（00到23，或如果显示为01到12，则为AM/PM显示）
- `H`：无前置零的整点（0到23，即使显示AM/PM时段）
- `HH`：带零前置的整点（00到23，即使显示AM/PM也如此）
- `m`：无前置零的分钟（0到59）
- `mm`：前置零的分钟（00至59）
- `s`：整秒，无前置零（0到59）
- `ss`：整秒，适用时首零（00至59）
- `z or zz`：秒的分数部分，位于小数点之后，不带尾随零。因此`"s.z"`以完全可用的毫秒精度报告秒数，没有尾随零（0到999）。例如，`"s.z"`会在一分钟中四分之一秒产生`"0.25"`。
- `zzz`：秒的分数部分，精确到毫秒级，包括适用的尾随零（000到999）。例如，`"ss.zzz"`会在一分钟中四分之一秒产生`"00.250"`。
- `AP or A`：使用AM/PM显示。`A/AP`将被“AM”或“PM”替换。在本地化形式（仅适用于`QLocale::toString()`）中，适合本地的文本转换为大写字母。
- `ap or a`：使用上午/下午显示。`a/ap`将被“am”或“pm”替换。在本地化形式（仅适用于`QLocale::toString()`）中，适合本地的文本会转换为小写。
- `aP or Ap`：使用AM/PM显示（自6.3版本起）。`aP/Ap`将被“AM”或“PM”取代。在本地化形式（仅与`QLocale::toString()`相关）中，使用本地适宜文本（由`QLocale::amText()`或`QLocale::pmText()`返回）且不改变大小写。
- `t`：时区缩写（例如“CEST”）。注意时区缩写并非唯一。特别是，`fromString()`无法解析此缩写。
- `tt`：时区偏移于UTC，时分与分钟之间无冒号（例如“0200”）。
- `ttt`：时区偏移于UTC，时分和分钟之间加冒号（例如“02：00”）。
- `tttt`：时区名称，由`QTimeZone::displayName()`提供，`QTimeZone::LongName`类型。这可能取决于所使用的操作系统。如果没有此类名称，可以使用该区域的IANA ID（如“Europe/Berlin”）。它可能无法显示日期时间是夏令时还是标准时间，如果日期时间落在一小时内，且两者之间有过渡，可能会产生歧义。
注意：要获取本地化的AM或PM格式（`AP`、`ap`、`A`、`a`、`aP`或`Ap`格式）或时区表示（`t`格式），请使用`QLocale::system()`。`toString()`。
当无法确定时区或没有合适的表示时，可以跳过表示时区的 `t` 形式。有关返回空字符串时的详细信息，请参见`QTimeZone::displayName()`。
任何非空的单引号字符序列都会被逐字包含在输出字符串中（去掉引号），即使其中包含格式化字符。两个连续的单引号（“'”）在输出中被一个引号替换。格式字符串中的所有其他字符都被逐字包含在输出字符串中。
支持无分隔符的格式（例如“hhmm”），但使用时必须谨慎，因为生成字符串并不总是可靠可读（例如，如果“Hm”生成“212”，可能意味着02：12或21：02）。
示例格式字符串（假设`QTime`为14：13：09.042）。
- `Format`：结果
- `hh:mm:ss.zzz`：14：13：09.042
- `h:m:s ap`：下午2：13：9
- `H:m:s a`：下午14：13：9
注意：如果使用该格式字符重复次数超过表中最长表达式，该格式部分将被读取为多个表达式，且无分隔符;最长的表达式可能重复次数与其副本数量相等，结尾剩余表达式可能较短。因此，08：00 时间的`'HHHHH'`会对输出贡献`"08088"`。

### `[constexpr noexcept] bool operator!=(const QTime &lhs, const QTime &rhs)`

**作用与语义：**

如果 `lhs` 与 `rhs` 不同，则返回 `true`；否则返回 `false`。

### `[constexpr noexcept] bool operator<(const QTime &lhs, const QTime &rhs)`

**作用与语义：**

如果 `lhs` 早于 `rhs`，则返回 `true`；否则返回 `false`。

### `QDataStream &operator<<(QDataStream &out, QTime time)`

**作用与语义：**

写入`time`流媒体`out`。

### `[constexpr noexcept] bool operator<=(const QTime &lhs, const QTime &rhs)`

**作用与语义：**

如果 `lhs` 早于或等于 `rhs`，则返回 `true`；否则返回 `false`。

### `[constexpr noexcept] bool operator==(const QTime &lhs, const QTime &rhs)`

**作用与语义：**

如果 `lhs` 等于 `rhs`，则返回 `true`；否则返回 `false`。

### `[constexpr noexcept] bool operator>(const QTime &lhs, const QTime &rhs)`

**作用与语义：**

如果 `lhs` 晚于 `rhs`，则返回 `true`；否则返回 `false`。

### `[constexpr noexcept] bool operator>=(const QTime &lhs, const QTime &rhs)`

**作用与语义：**

如果 `lhs` 晚于或等于 `rhs`，则返回 `true`；否则返回 `false`。

### `QDataStream &operator>>(QDataStream &in, QTime &time)`

**作用与语义：**

从流`in`读取到给定`time`的时间。

### `QString toString(const QString &format) const`

**作用与语义：**

返回时间为字符串。`format`参数决定字符串的格式。
如果`format`为`Qt::TextDate`，字符串格式为 HH：mm：ss;例如午夜前一秒为“23：59：59”。
如果`format` `Qt::ISODate`，字符串格式对应ISO 8601扩展的日期表示规范，表示为HH：mm：ss。要在ISO 8601日期中包含毫秒，请使用`format` `Qt::ISODateWithMs`，对应HH：mm：ss.zzz。
如果`format`是`Qt::RFC2822Date`，字符串格式化为RFC 2822兼容的格式。这种格式的一个例子是“23：59：20”。
如果时间无效，将返回一个空字符串。
注意：该功能会让`QTime::toString()`重载。

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

`QTime` 所属机制类型：Qt 值类型与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
