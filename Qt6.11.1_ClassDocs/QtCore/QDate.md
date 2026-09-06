# QDate

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QDate` 表示一个不带时区和时刻的公历/日历日期。它只回答年、月、日及日期运算，不代表某一天中的具体时间点。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QDate` 表示一个不带时区和时刻的公历/日历日期。它只回答年、月、日及日期运算，不代表某一天中的具体时间点。

**内部模型：** QDate 是值类型，默认构造得到无效日期；用年、月、日构造后应以 `isValid()` 判断。日期加减返回新对象，不修改原对象；月份和年份运算会处理不同月份天数。格式化/解析依赖格式字符串和 locale，时区换算应交给 QDateTime。

**适用场景：** 生日、账期、日历选择、截止日期等只关心日期的业务使用 QDate；需要 UTC、时区、时间戳或一天中的时刻时使用 QDateTime。

**典型调用链：** 构造/解析日期 -> isValid -> year/month/day 查询 -> addDays/addMonths/addYears 运算 -> daysTo 比较间隔 -> toString 格式化。

**先记住的坑：** 无效日期不等于空字符串；不要用 QDate 表示时间戳；`fromString()` 必须匹配格式和 locale；跨月加减遇到月末时要验证业务预期。

## 2. 依赖与对象关系

- 头文件：`#include <QDate>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

QDate 是值类型，默认构造得到无效日期；用年、月、日构造后应以 `isValid()` 判断。日期加减返回新对象，不修改原对象；月份和年份运算会处理不同月份天数。格式化/解析依赖格式字符串和 locale，时区换算应交给 QDateTime。

### 状态、生命周期和线程

**生命周期：** 值对象由作用域、容器或调用者管理，不使用 parent 和 deleteLater。跨线程传递副本通常比传递 QObject 安全，但共享数据在写入时仍可能发生复制，性能和内存峰值要结合数据规模判断。

**状态与结果：** 重点区分空值、无效值、默认值和已初始化值。例如空字符串、空 URL、null 图像和无效索引不一定表示同一件事；转换函数的失败结果要通过对应的状态查询确认。

**线程与事件循环：** 值类型本身通常可以复制后跨线程传递；不要把 data()/bits()/constData() 得到的指针当成跨线程长期有效的所有权。大对象频繁写入会触发 detach，应避免不必要的复制和格式转换。

## 3. 直接使用

生日、账期、日历选择、截止日期等只关心日期的业务使用 QDate；需要 UTC、时区、时间戳或一天中的时刻时使用 QDateTime。 使用时通常按这个过程组织：构造/解析日期 -> isValid -> year/month/day 查询 -> addDays/addMonths/addYears 运算 -> daysTo 比较间隔 -> toString 格式化。

```cpp
#include <QDate>

const QDate start(2026, 9, 5);
if (start.isValid()) {
    const QDate due = start.addDays(30);
    const qint64 days = start.daysTo(due);
    const QString text = due.toString(Qt::ISODate);
}
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QDate()`
- `(since 6.4) QDate(std::chrono::year_month_day date)`
- `(since 6.4) QDate(std::chrono::year_month_day_last date)`
- `(since 6.4) QDate(std::chrono::year_month_weekday date)`
- `(since 6.4) QDate(std::chrono::year_month_weekday_last date)`
- `QDate(int y, int m, int d)`
- `QDate addDays(qint64 ndays) const`
- `(since 6.4) QDate addDuration(std::chrono::days ndays) const`
- `QDate addMonths(int nmonths, QCalendar cal) const`
- `QDate addMonths(int nmonths) const`
- `QDate addYears(int nyears, QCalendar cal) const`
- `QDate addYears(int nyears) const`
- `int day(QCalendar cal) const`
- `int day() const`
- `int dayOfWeek(QCalendar cal) const`
- `int dayOfWeek() const`
- `int dayOfYear(QCalendar cal) const`
- `int dayOfYear() const`
- `int daysInMonth(QCalendar cal) const`
- `int daysInMonth() const`
- `int daysInYear(QCalendar cal) const`
- `int daysInYear() const`
- `qint64 daysTo(QDate d) const`
- `QDateTime endOfDay(const QTimeZone &zone) const`
- `(since 6.5) QDateTime endOfDay() const`
- `void getDate(int *year, int *month, int *day) const`
- `bool isNull() const`
- `bool isValid() const`
- `int month(QCalendar cal) const`
- `int month() const`
- `bool setDate(int year, int month, int day)`
- `bool setDate(int year, int month, int day, QCalendar cal)`
- `QDateTime startOfDay(const QTimeZone &zone) const`
- `(since 6.5) QDateTime startOfDay() const`
- `qint64 toJulianDay() const`
- `std::chrono::sys_days toStdSysDays() const`
- `QString toString(const QString &format, QCalendar cal) const`
- `QString toString(QStringView format) const`
- `QString toString(Qt::DateFormat format = Qt::TextDate) const`
- `QString toString(const QString &format) const`
- `QString toString(QStringView format, QCalendar cal) const`
- `int weekNumber(int *yearNumber = nullptr) const`
- `int year(QCalendar cal) const`
- `int year() const`

### 静态公有成员

- `QDate currentDate()`
- `QDate fromJulianDay(qint64 jd)`
- `(since 6.4) QDate fromStdSysDays(const std::chrono::sys_days &days)`
- `QDate fromString(const QString &string, const QString &format, int baseYear, QCalendar cal)`
- `(since 6.0) QDate fromString(QStringView string, Qt::DateFormat format = Qt::TextDate)`
- `QDate fromString(const QString &string, Qt::DateFormat format = Qt::TextDate)`
- `(since 6.0) QDate fromString(QStringView string, QStringView format, QCalendar cal)`
- `(since 6.7) QDate fromString(QStringView string, QStringView format, int baseYear = QLocale::DefaultTwoDigitBaseYear)`
- `(since 6.0) QDate fromString(const QString &string, QStringView format, QCalendar cal)`
- `(since 6.7) QDate fromString(const QString &string, QStringView format, int baseYear = QLocale::DefaultTwoDigitBaseYear)`
- `QDate fromString(const QString &string, const QString &format, QCalendar cal)`
- `(since 6.7) QDate fromString(const QString &string, const QString &format, int baseYear = QLocale::DefaultTwoDigitBaseYear)`
- `(since 6.7) QDate fromString(QStringView string, QStringView format, int baseYear, QCalendar cal)`
- `(since 6.0) QDate fromString(const QString &string, QStringView format, int baseYear, QCalendar cal)`
- `bool isLeapYear(int year)`
- `bool isValid(int year, int month, int day)`

### 相关非成员函数

- `bool operator!=(const QDate &lhs, const QDate &rhs)`
- `(since 6.11) QDate & operator++(QDate &date)`
- `(since 6.11) QDate operator++(QDate &date, int)`
- `(since 6.11) QDate & operator--(QDate &date)`
- `(since 6.11) QDate operator--(QDate &date, int)`
- `bool operator<(const QDate &lhs, const QDate &rhs)`
- `QDataStream & operator<<(QDataStream &out, QDate date)`
- `bool operator<=(const QDate &lhs, const QDate &rhs)`
- `bool operator==(const QDate &lhs, const QDate &rhs)`
- `bool operator>(const QDate &lhs, const QDate &rhs)`
- `bool operator>=(const QDate &lhs, const QDate &rhs)`
- `QDataStream & operator>>(QDataStream &in, QDate &date)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[constexpr] QDate::QDate()`

**作用与语义：**

构造一个空日期。空日期无效。

### `[constexpr noexcept, since 6.4] QDate::QDate(std::chrono::year_month_weekday_last date)`

**作用与语义：**

构建一个表示与`date`同一日期的`QDate`。这使得标准库的日历类和Qt的datetime类之间能够轻松互操作。
注意：与`QDate`不同，std：：chrono：：year 及相关类别都包含零年。这意味着如果`date`处于零年或更早，所得`QDate`对象的年份将比`date`指定的年份少一年。
注意：此函数需要C 20。

**官方示例：**

```cpp
 // 23 April 2012:
 QDate date = std::chrono::year_month_day(std::chrono::year(2012),
                                         std::chrono::month(4),
                                         std::chrono::day(23));

 // Same, under `using std::chrono` convenience:
 QDate dateWithLiterals1 = 23d / April / 2012y;
 QDate dateWithLiterals2 = 2012y / April / 23;

 // Last day of February 2000
 QDate lastDayFeb2020 = 2000y / February / last;

 // First Monday of January 2020:
 QDate firstMonday = 2020y / January / Monday[0];

 // Last Monday of January 2020:
 QDate lastMonday = 2020y / January / Monday[last];
```

### `QDate::QDate(int y, int m, int d)`

**作用与语义：**

构建一个表示与`date`同一日期的`QDate`。这使得标准库的日历类和Qt的datetime类之间能够轻松互操作。
注意：与`QDate`不同，std：：chrono：：year 及相关类别都包含零年。这意味着如果`date`处于零年或更早，所得`QDate`对象的年份将比`date`指定的年份少一年。
注意：此函数需要C 20。

**官方示例：**

```cpp
 // 23 April 2012:
 QDate date = std::chrono::year_month_day(std::chrono::year(2012),
                                         std::chrono::month(4),
                                         std::chrono::day(23));

 // Same, under `using std::chrono` convenience:
 QDate dateWithLiterals1 = 23d / April / 2012y;
 QDate dateWithLiterals2 = 2012y / April / 23;

 // Last day of February 2000
 QDate lastDayFeb2020 = 2000y / February / last;

 // First Monday of January 2020:
 QDate firstMonday = 2020y / January / Monday[0];

 // Last Monday of January 2020:
 QDate lastMonday = 2020y / January / Monday[last];
```

### `QDate QDate::addDays(qint64 ndays) const`

**作用与语义：**

返回一个`QDate`对象，包含比该对象日期晚`ndays`日期（或如果`ndays`为负则更早）。
如果当前日期无效或新日期超出范围，则返回空日期。

### `[since 6.4] QDate QDate::addDuration(std::chrono::days ndays) const`

**作用与语义：**

返回一个`QDate`对象，包含比该对象日期晚`ndays`的日期（或如果`ndays`为负则更早）。
如果当前日期无效或新日期超出范围，则返回空日期。
注意：用`std::chrono::months`或用`std::chrono::years`表示的持续时间添加，无法得到使用`addMonths()`或`addYears()`相同的结果。前者是固定的持续时间，基于太阳年计算;后者使用格里高利历中月份/年份的定义。
注意：此函数需要C 20。

### `QDate QDate::addMonths(int nmonths, QCalendar cal) const`

**作用与语义：**

返回一个`QDate`对象，包含比该对象日期晚`nmonths`（或如果`nmonths`为负则更早）。
如果提供，使用`cal`作为日历，否则使用格里高利历。
注意：如果在最终的月份/年份中没有结束日/月份的组合，该函数将返回选定月份中最晚有效日期。

### `QDate QDate::addMonths(int nmonths) const`

**作用与语义：**

注意：该功能会让`QDate::addMonths()`重载。

### `QDate QDate::addYears(int nyears, QCalendar cal) const`

**作用与语义：**

返回一个`QDate`对象，包含比该对象日期晚`nyears`的日期（如果`nyears`为负则更早）。
如果提供，使用`cal`作为历法，否则使用格里高利历。
注意：如果在后续年份中不存在结束日/月份组合（例如，公历中日期为2月29日且最后一年不是闰年），该函数将返回给定月份中最晚有效日期（例中为2月28日）。

### `QDate QDate::addYears(int nyears) const`

**作用与语义：**

注意：该功能会让`QDate::addYears()`重载。

### `[static] QDate QDate::currentDate()`

**作用与语义：**

返回系统时钟的当前日期。

### `int QDate::day(QCalendar cal) const`

**作用与语义：**

该日期的月份日期返回。
如提供日期，使用`cal`作为日历，否则使用格里高利历（回归范围为1至31）。若日期无效，返回0。

### `int QDate::day() const`

**作用与语义：**

注意：该功能会超载`QDate::day()`。

### `int QDate::dayOfWeek(QCalendar cal) const`

**作用与语义：**

返回该日期的工作日（1 = 周一 至 7 = 周日）。
如果提供日期，使用`cal`作为日历，否则使用格里高利历。如果日期无效，返回0。某些历法可能会赋予大于7的值特殊含义（例如召唤日）。

### `int QDate::dayOfWeek() const`

**作用与语义：**

注意：这个功能会让`QDate::dayOfWeek()`重载。

### `int QDate::dayOfYear(QCalendar cal) const`

**作用与语义：**

该日期会返回一年中的某一天（第一天有1个）。
如果提供日期或年份的第一天无效，则使用`cal`作为日历。如果日期或年份的第一天无效，返回0。

### `int QDate::dayOfYear() const`

**作用与语义：**

注意：该功能会超载`QDate::dayOfYear()`。

### `int QDate::daysInMonth(QCalendar cal) const`

**作用与语义：**

返回该日期的月份天数。
如果提供日期，则使用`cal`作为日历，否则使用格里高利历（其结果范围为28至31）。若日期无效，返回0。

### `int QDate::daysInMonth() const`

**作用与语义：**

注意：该功能会超载`QDate::daysInMonth()`。

### `int QDate::daysInYear(QCalendar cal) const`

**作用与语义：**

返回该日期的年度天数。
如果提供日期，则使用`cal`作为日历，否则使用格里高利历（结果为365或366）。如果日期无效，返回0。

### `int QDate::daysInYear() const`

**作用与语义：**

注意：该功能会让`QDate::daysInYear()`重载。

### `qint64 QDate::daysTo(QDate d) const`

**作用与语义：**

返回从该日期到`d`天数（如果`d`比该日期早则为负数）。
如果任一日期无效，返回0。

**官方示例：**

```cpp
 QDate d1(1995, 5, 17);  // May 17, 1995
 QDate d2(1995, 5, 20);  // May 20, 1995
 d1.daysTo(d2);          // returns 3
 d2.daysTo(d1);          // returns -3
```

### `QDateTime QDate::endOfDay(const QTimeZone &zone) const`

**作用与语义：**

返回一天结束的时刻。
一天结束的时间取决于时间的描述方式：在更西边的时区，每一天的开始和结束时间较早，而在更东边的时区则较晚。使用的时间表示方式可以通过可选的时间`zone`来指定。默认的时间表示方式是系统的本地时间。
通常，一天结束时间是在午夜前一毫秒，即24：00;但如果时区转换导致指定日期跳过该时刻（例如夏令时春季快进跳过23：00及随后一小时），则返回当天实际最晚时间。这只会在时间表示为时区或本地时间时出现。
当`zone`的timeSpec()为`Qt::OffsetFromUTC`或`Qt::UTC`时，时间表示没有转移，因此一天结束时为`QTime`（23， 59， 59， 999）。
在极少数完全跳过日期的情况（即国际日期变更线以东的区域变为其以西时），返回无效。`zone`无效时区也会产生无效结果，超出`QDateTime`可表示范围的日期同样无效。

### `[since 6.5] QDateTime QDate::endOfDay() const`

**作用与语义：**

注意：该功能会`QDate::endOfDay()`重载。

### `[static constexpr] QDate QDate::fromJulianDay(qint64 jd)`

**作用与语义：**

将儒略日`jd`转变为`QDate`。

### `[static constexpr noexcept, since 6.4] QDate QDate::fromStdSysDays(const std::chrono::sys_days &days)`

**作用与语义：**

返回时间为1970年1月1日（UNIX纪元）后`QDate` `days`天。如果`days`为负，返回日期将早于该纪元。
注意：此函数需要C 20。

### `[static] QDate QDate::fromString(const QString &string, const QString &format, int baseYear, QCalendar cal)`

**作用与语义：**

返回`string`表示的`QDate`，使用给定的`format`;如果字符串无法解析，则返回无效日期。
如提供，使用`cal`作为日历，否则使用格里高利历。以下格式描述中的数值范围适用于后者;其他日历可能有所不同。
这些表达可用于格式：
- `Expression`：输出
- `d`：以无前置零的数字表示的日期（1到31）
- `dd`：以数字表示的日期，前置零（01到31）
- `ddd`：日名的缩写（从“Mon”到“Sun”）。
- `dddd`：长日名称（“星期一”到“星期天”）。
- `M`：月份作为无前置零的数字（1到12）
- `MM`：以数字表示月份，前置零（01到12）
- `MMM`：缩写月份名称（“Jan”到“Dec”）。
- `MMMM`：长月名（'January' to 'December'）。
- `yy`：年份以两位数字表示（00至99）
- `yyyy`：年份为四位数字，负年份可能加上前置减号。
注意：日期和月份名称必须以英文（C locale）提供。如果要识别本地化的月份和日期名称，请使用 `QLocale::system()`.toDate()。
所有其他输入字符都将被视为文本。任何非空的字符序列如果被单引号包围，也会被视为文本（去掉引号），不会被解释为表达式。例如：
如果格式不满足，返回无效`QDate`。不期望前置零（d， M）的表达式是贪婪的。这意味着即使这会超出接受范围，且留给其他部分的数字太少，它们仍会使用两位数字。例如，以下格式字符串可能表示1月30日，但M会抓取两位数字，导致日期无效：
对于格式中未表示的任何字段，使用以下默认值：
- `Field`：默认值
- `Year`：`baseYear`（或1900年）
- `Month`：1（1月）
- `Day`：1
当`format`只指定年份的最后两位时，首先考虑的候选年份是从`baseYear`开始的100年。6.7之前没有`baseYear`参数，始终使用1900年。这是`baseYear`的默认选择年份，从1999年到1999年。例如，通过1976年，`baseYear`将选择1976年至2075年。当格式还包括月份、日期（月份）和星期数时，这些就足以暗示世纪。在这种情况下，选择与`baseYear`所示最接近的世纪的匹配日期，优先选择较晚的年份而非更早的年份。更多细节请参见`QCalendar::matchCenturyToWeekday()`和日期歧义，。
以下示例展示了默认值：
注意：如果使用该格式字符重复次数超过表中最长表达式，该格式部分将被解读为多个表达式，中间没有分隔符;最长的表达式可能重复次数与其副本数量相等，结尾剩余表达式可能更短。因此`'MMMMMMMMMM'`匹配`"MayMay05"`并将月份设为五月。同样，`'MMMMMM'`匹配`"May08"`但发现不一致，导致日期无效。
不同文化使用不同的日期格式，因此用户可能会混淆日期字段的顺序。例如，`"Wed 28-Nov-01"`可能指的是2028年11月1日或2001年11月28日（这两个日期恰好是星期三）。使用格式`"ddd yy-MMM-dd"`应用第一种方式解释，`"ddd dd-MMM-yy"`用第二种方式。然而，用户所指的可能取决于用户通常写日期的方式，而非代码预期的格式。
上述例子将月份的日期和两位数年份混淆。当月份和月份的日期互换时，也会出现类似的混淆，因为两者都以数字表示。在这种情况下，在日期格式中加入星期几字段可以提供一定的冗余，有助于发现此类错误。然而，正如上述例子所示，这并不总是有效：两个字段（或其含义）互换可能导致日期与星期几相同。
在格式中加入星期几也可以只用年份的最后两位数字来解析日期的世纪。不幸的是，当用户（或其他数据来源）将两个字段混淆的日期结合时，这种解决可能导致找到一个与格式读法相符但并非作者意图的日期。同样，如果用户在一个本应正确的日期中错误地填入星期几，可能会导致日期出现在不同的世纪。在每种情况下，找到不同世纪的日期都可能使错误输入的日期变成截然不同的日期。
避免日期歧义的最佳方法是使用以名称（无论是完整还是缩写）标注的四位数年份和月份，理想情况下通过用户界面的习语收集，让用户清楚知道他们选择的日期部分。包含星期几也有助于检查数据的一致性。当数据来自用户，使用由用户选择的地点提供的格式时，最好使用长格式，因为短格式更可能使用两位数年份。当然，格式并非总是能控制——例如，数据可能来自你无法控制的来源。
由于这些可能的混淆来源，尤其是当你无法确定是否使用了明确的格式时，检查将字符串作为日期读取的结果不仅有效，而且符合其提供目的的合理性非常重要。如果结果超出某个合理范围，建议用户确认日期选择，以包含月份名称和四位年份的长格式显示从字符串读取的日期，以便更容易识别错误。

**官方示例：**

```cpp
 QDate date = QDate::fromString("1MM12car2003", "d'MM'MMcaryyyy");
 // date is 1 December 2003
```

### `[static, since 6.0] QDate QDate::fromString(QStringView string, Qt::DateFormat format = Qt::TextDate)`

**作用与语义：**

注意：该功能会让`QDate::fromString()`重载。

### `[static] QDate QDate::fromString(const QString &string, Qt::DateFormat format = Qt::TextDate)`

**作用与语义：**

返回`string`所代表的`QDate`，使用给定的`format`;如果字符串无法解析，则返回无效日期。
`Qt::TextDate`注意：仅认可英文月份名称（例如简称“Jan”或长称“January”）。

### `[static, since 6.0] QDate QDate::fromString(QStringView string, QStringView format, QCalendar cal)`

**作用与语义：**

注意：该功能会让`QDate::fromString()`重载。

### `[static, since 6.7] QDate QDate::fromString(QStringView string, QStringView format, int baseYear = QLocale::DefaultTwoDigitBaseYear)`

**作用与语义：**

使用默认构造的`QCalendar`。
注意：该功能会让`QDate::fromString()`重载。

### `[static, since 6.0] QDate QDate::fromString(const QString &string, QStringView format, QCalendar cal)`

**作用与语义：**

注意：该功能会让`QDate::fromString()`重载。

### `[static, since 6.7] QDate QDate::fromString(const QString &string, QStringView format, int baseYear = QLocale::DefaultTwoDigitBaseYear)`

**作用与语义：**

使用默认构造的`QCalendar`。
注意：该功能会让`QDate::fromString()`重载。

### `[static] QDate QDate::fromString(const QString &string, const QString &format, QCalendar cal)`

**作用与语义：**

注意：该功能会让`QDate::fromString()`重载。

### `[static, since 6.7] QDate QDate::fromString(const QString &string, const QString &format, int baseYear = QLocale::DefaultTwoDigitBaseYear)`

**作用与语义：**

使用默认构造的`QCalendar`。
注意：该功能会让`QDate::fromString()`重载。

### `[static, since 6.7] QDate QDate::fromString(QStringView string, QStringView format, int baseYear, QCalendar cal)`

**作用与语义：**

注意：该功能会让`QDate::fromString()`重载。

### `[static, since 6.0] QDate QDate::fromString(const QString &string, QStringView format, int baseYear, QCalendar cal)`

**作用与语义：**

注意：该功能会让`QDate::fromString()`重载。

### `void QDate::getDate(int *year, int *month, int *day) const`

**作用与语义：**

提取日期的年份、月份和日期，并将其分配给 *`year`、*`month` 和 *`day`。指针可能是空指针。
如果日期无效，则返回0。
注意：在5.7之前的Qt版本中，该功能被标记为非`const`。

### `[static] bool QDate::isLeapYear(int year)`

**作用与语义：**

如果指定的`year`是格里高利历闰年，则返回`true`;否则返回`false`。

### `[constexpr] bool QDate::isNull() const`

**作用与语义：**

如果日期为空，返回`true`;否则返回`false`。空日期无效。
注意：该函数的行为等价于`isValid()`。

### `[constexpr] bool QDate::isValid() const`

**作用与语义：**

如果该日期有效，返回`true`;否则返回`false`。

### `[static] bool QDate::isValid(int year, int month, int day)`

**作用与语义：**

如果指定日期（`year`、`month`和`day`）在格里高利历中有效，返回`true`;否则返回`false`。
注意：该功能会让`QDate::isValid()`重载。

**官方示例：**

```cpp
 QDate::isValid(2002, 5, 17);  // true
 QDate::isValid(2002, 2, 30);  // false (Feb 30 does not exist)
 QDate::isValid(2004, 2, 29);  // true (2004 is a leap year)
 QDate::isValid(2000, 2, 29);  // true (2000 is a leap year)
 QDate::isValid(2006, 2, 29);  // false (2006 is not a leap year)
 QDate::isValid(2100, 2, 29);  // false (2100 is not a leap year)
 QDate::isValid(1202, 6, 6);   // true (even though 1202 is pre-Gregorian)
```

### `int QDate::month(QCalendar cal) const`

**作用与语义：**

返回日期的月份数字。
编号年份中的月份，以1开头表示第一个月份。如果提供，使用`cal`作为历法，否则使用格里高利历，月份编号如下：
- 1 = “一月”
- 2 = “二月”
- 3 = “进行曲”
- 4 = “四月”
- 5 = “五月”
- 6 = “六月”
- 7 = “七月”
- 8 = “八月”
- 9 = “九月”
- 10 = “十月”
- 11 = “十一月”
- 12 = “十二月”
如果日期无效，则返回0。请注意，有些日历在某些年份可能超过12个月。

### `int QDate::month() const`

**作用与语义：**

注意：该功能会让`QDate::month()`重载。

### `bool QDate::setDate(int year, int month, int day)`

**作用与语义：**

将该日期设置为表示格里高利历中的日期，包含给定的`year`、`month`和`day`数。如果结果日期有效，返回真;否则，表示无效日期，返回假。

### `bool QDate::setDate(int year, int month, int day, QCalendar cal)`

**作用与语义：**

将该日期设置为表示给定历`cal`中的日期，包含给定的`year`、`month`和`day`数字。如果结果日期有效，则返回真;否则，它将表示无效日期，返回假。

### `QDateTime QDate::startOfDay(const QTimeZone &zone) const`

**作用与语义：**

返回一天的开始时刻。
一天的开始时间取决于时间的描述方式：对于更西边的时区，每一天的开始和结束都更早，而在更东边的时区，每一天都较早开始和结束。可用的时间表示方式可以通过可选的时间`zone`来指定。默认的时间表示方式是系统的本地时间。
通常，一天的开始时间是午夜00：00：但如果时区转换导致给定日期跳过了午夜（例如夏令时春季快进跳过了一天的第一小时），则返回当天实际最早的时间。这只会在时间表示为时区或本地时间时出现。
当 `zone` 的 timeSpec() 为 `Qt::OffsetFromUTC` 或 `Qt::UTC` 时，时间表示没有变换，因此一天的开始时间为 `QTime`（0， 0）。
在极少数完全跳过日期的情况下（即国际日期变更线以东的区域切换为其以西），返回无效。以无效时区方式过`zone`也会产生无效结果，起始日期超出`QDateTime`可表示范围的日期亦然。

### `[since 6.5] QDateTime QDate::startOfDay() const`

**作用与语义：**

注意：该功能会让`QDate::startOfDay()`重载。

### `[constexpr] qint64 QDate::toJulianDay() const`

**作用与语义：**

将日期转换为儒略历日。

### `[constexpr noexcept] std::chrono::sys_days QDate::toStdSysDays() const`

**作用与语义：**

返回1970年1月1日（UNIX纪元）与该日期之间的天数，表示为`std::chrono::sys_days`对象。如果该日期早于该纪元，天数为负数。
注意：此函数需要C 20。

### `QString QDate::toString(QStringView format, QCalendar cal) const`

**作用与语义：**

返回日期为字符串。`format`参数决定结果字符串的格式。如果提供`cal`，则决定表示日期的历法;默认为格里高利历。在Qt 5.14之前，没有`cal`参数，始终使用格里高利历。
这些表达式可用于`format`参数：
- `Expression`：输出
- `d`：以无前置零的数字表示的日期（1到31）
- `dd`：以数字表示的日期，前置零（01到31）
- `ddd`：日名的缩写（从“Mon”到“Sun”）。
- `dddd`：长日名称（“星期一”到“星期天”）。
- `M`：月份作为无前置零的数字（1到12）
- `MM`：以数字表示月份，前置零（01到12）
- `MMM`：缩写月份名称（“Jan”到“Dec”）。
- `MMMM`：长月名（'January' to 'December'）。
- `yy`：年份以两位数字表示（00至99）
- `yyyy`：年份以四位数字表示。如果年份为负数，则前加负号，共五个字符。
任何用单引号包围的字符序列都会被逐字包含在输出字符串中（去掉引号），即使其中包含格式化字符。两个连续的单引号（“''”）在输出中被一个引号替换。格式字符串中的所有其他字符都逐字包含在输出字符串中。
支持无分隔符的格式（如“ddMM”），但必须谨慎使用，因为生成字符串并不总是可靠可读（例如，如果“dM”生成“212”，可能意味着12月2日或2月21日）。
示例格式字符串（假设`QDate`为1969年7月20日）：
- `Format`：结果
- `dd.MM.yyyy`：1969年7月20日
- `ddd MMMM d yy`：7月20日星期日 69
- `'The day is' dddd`：今天是星期天
如果 datetime 无效，则返回一个空字符串。
注意：日期和月份名称均为英文（C本地）。要获得本地化的月份和日期名称，请使用`QLocale::system()`。`toString()`。
注意：如果使用该格式字符重复次数超过表格中最长表达式，该部分格式将被解读为多个表达式，且无分隔符;上述最长字符可能被重复次数与副本数量相等，结尾剩余表达式可能较短。因此，五月某日期的 `'MMMMMMMMMM'` 会对输出贡献`"MayMay05"`。

### `QString QDate::toString(QStringView format) const`

**作用与语义：**

返回日期为字符串。`format`参数决定结果字符串的格式。如果提供`cal`，则决定表示日期的历法;默认为格里高利历。在Qt 5.14之前，没有`cal`参数，始终使用格里高利历。
这些表达式可用于`format`参数：
- `Expression`：输出
- `d`：以无前置零的数字表示的日期（1到31）
- `dd`：以数字表示的日期，前置零（01到31）
- `ddd`：日名的缩写（从“Mon”到“Sun”）。
- `dddd`：长日名称（“星期一”到“星期天”）。
- `M`：月份作为无前置零的数字（1到12）
- `MM`：以数字表示月份，前置零（01到12）
- `MMM`：缩写月份名称（“Jan”到“Dec”）。
- `MMMM`：长月名（'January' to 'December'）。
- `yy`：年份以两位数字表示（00至99）
- `yyyy`：年份以四位数字表示。如果年份为负数，则前加负号，共五个字符。
任何用单引号包围的字符序列都会被逐字包含在输出字符串中（去掉引号），即使其中包含格式化字符。两个连续的单引号（“''”）在输出中被一个引号替换。格式字符串中的所有其他字符都逐字包含在输出字符串中。
支持无分隔符的格式（如“ddMM”），但必须谨慎使用，因为生成字符串并不总是可靠可读（例如，如果“dM”生成“212”，可能意味着12月2日或2月21日）。
示例格式字符串（假设`QDate`为1969年7月20日）：
- `Format`：结果
- `dd.MM.yyyy`：1969年7月20日
- `ddd MMMM d yy`：7月20日星期日 69
- `'The day is' dddd`：今天是星期天
如果 datetime 无效，则返回一个空字符串。
注意：日期和月份名称均为英文（C本地）。要获得本地化的月份和日期名称，请使用`QLocale::system()`。`toString()`。
注意：如果使用该格式字符重复次数超过表格中最长表达式，该部分格式将被解读为多个表达式，且无分隔符;上述最长字符可能被重复次数与副本数量相等，结尾剩余表达式可能较短。因此，五月某日期的 `'MMMMMMMMMM'` 会对输出贡献`"MayMay05"`。

### `QString QDate::toString(Qt::DateFormat format = Qt::TextDate) const`

**作用与语义：**

注意：该功能会让`QDate::toString()`重载。

### `QString QDate::toString(const QString &format) const`

**作用与语义：**

返回字符串的日期。`format`参数决定字符串的格式。
如果`format`为`Qt::TextDate`，字符串格式为默认格式。日期和月份名称为英文。此格式示例为“Sat May 20 1995”。有关本地化格式，请参见 `QLocale::toString()`。
如果`format`是`Qt::ISODate`，字符串格式对应于ISO 8601扩展规范中的日期和时间表示，形式为yyyy-MM-dd，其中yyyy是年份，MM是年份的月份（01到12之间），dd是01到31之间的月份的日期。
如果`format`是`Qt::RFC2822Date`，字符串格式化为RFC 2822兼容的格式化。这种格式的一个例子是“20 May 1995”。
如果日期无效，将返回空字符串。
警告：`Qt::ISODate`格式仅适用于0至9999之间的年份。
注意：该功能会超载`QDate::toString()`。

### `int QDate::weekNumber(int *yearNumber = nullptr) const`

**作用与语义：**

返回ISO 8601周数（1到53）。
如果日期无效，则返回0。否则，返回日期的周数。如果`yearNumber`不是`nullptr`（默认），则将年份存储为*`yearNumber`。
根据ISO 8601，每个周都属于其大部分天数所属的年份，即公历。由于ISO 8601的周从星期一开始，这一年则是该周的星期四。大多数年份有52周，但有些年份有53周。
注意：*`yearNumber`不总是与`year()`相同。例如，2000年1月1日是1999年的第52周，2002年12月31日是2003年的第1周。

### `int QDate::year(QCalendar cal) const`

**作用与语义：**

返回该年份。
如果提供，使用`cal`作为历法，否则使用格里高利历。
如果日期无效，则返回0。对于某些日历，第一年之前的日期可能全部无效。
如果使用年为0的历法，检查返回是否为0，使用第`isValid()`。此类历法使用负年数，年份前加0年，0年前加0年，依此类推。
有些历法虽然没有0年，但对其第一年之前的年份有惯例编号，从1倒数。例如，在前置格里高利历中，公元1年前（第一年）之前的连续年份被识别为公元前1年、公元前2年、公元前3年等。对于此类历法，使用负数年份表示1年前的年份，-1表示1年前的年份。

### `int QDate::year() const`

**作用与语义：**

注意：该功能会让`QDate::year()`重载。

### `[constexpr noexcept] bool operator!=(const QDate &lhs, const QDate &rhs)`

**作用与语义：**

如果 `lhs` 和 `rhs` 表示不同的日期，则返回 `true`；否则返回 `false`。

### `[since 6.11] QDate &operator++(QDate &date)`

**作用与语义：**

前缀 `++` 操作符，会在 `date` 上加上一个日期，并返回对修改日期对象的引用。

### `[since 6.11] QDate operator++(QDate &date, int)`

**作用与语义：**

后缀`++`操作员会在`date`上添加一天，并返回带有前一日期的 `date`副本。

### `[since 6.11] QDate &operator--(QDate &date)`

**作用与语义：**

前缀 `--` 操作符，从 `date` 减去一天，并返回对修改日期对象的引用。

### `[since 6.11] QDate operator--(QDate &date, int)`

**作用与语义：**

后缀`--`操作员会从 `date` 中减去一天，并返回带有下一个日期的 `date` 副本。

### `[constexpr noexcept] bool operator<(const QDate &lhs, const QDate &rhs)`

**作用与语义：**

如果 `lhs` 早于 `rhs`，则返回 `true`；否则返回 `false`。

### `QDataStream &operator<<(QDataStream &out, QDate date)`

**作用与语义：**

写媒体`date` `out`。

### `[constexpr noexcept] bool operator<=(const QDate &lhs, const QDate &rhs)`

**作用与语义：**

如果 `lhs` 早于或等于 `rhs`，则返回 `true`；否则返回 `false`。

### `[constexpr noexcept] bool operator==(const QDate &lhs, const QDate &rhs)`

**作用与语义：**

如果 `lhs` 和 `rhs` 表示同一天，则返回 `true`，否则返回 `false`。

### `[constexpr noexcept] bool operator>(const QDate &lhs, const QDate &rhs)`

**作用与语义：**

如果 `lhs` 晚于 `rhs`，则返回 `true`；否则返回 `false`。

### `[constexpr noexcept] bool operator>=(const QDate &lhs, const QDate &rhs)`

**作用与语义：**

如果 `lhs` 晚于或等于 `rhs`，则返回 `true`；否则返回 `false`。

### `QDataStream &operator>>(QDataStream &in, QDate &date)`

**作用与语义：**

读取了`in`流的日期，进入`date`。

### `(since 6.4) QDate(std::chrono::year_month_day date)`

**作用与语义：**

构建一个表示与`date`同一日期的`QDate`。这使得标准库的日历类和Qt的datetime类之间能够轻松互操作。
注意：与`QDate`不同，std：：chrono：：year 及相关类别都包含零年。这意味着如果`date`处于零年或更早，所得`QDate`对象的年份将比`date`指定的年份少一年。
注意：此函数需要C 20。

**官方示例：**

```cpp
 // 23 April 2012:
 QDate date = std::chrono::year_month_day(std::chrono::year(2012),
                                         std::chrono::month(4),
                                         std::chrono::day(23));

 // Same, under `using std::chrono` convenience:
 QDate dateWithLiterals1 = 23d / April / 2012y;
 QDate dateWithLiterals2 = 2012y / April / 23;

 // Last day of February 2000
 QDate lastDayFeb2020 = 2000y / February / last;

 // First Monday of January 2020:
 QDate firstMonday = 2020y / January / Monday[0];

 // Last Monday of January 2020:
 QDate lastMonday = 2020y / January / Monday[last];
```

### `(since 6.4) QDate(std::chrono::year_month_day_last date)`

**作用与语义：**

构建一个表示与`date`同一日期的`QDate`。这使得标准库的日历类和Qt的datetime类之间能够轻松互操作。
注意：与`QDate`不同，std：：chrono：：year 及相关类别都包含零年。这意味着如果`date`处于零年或更早，所得`QDate`对象的年份将比`date`指定的年份少一年。
注意：此函数需要C 20。

**官方示例：**

```cpp
 // 23 April 2012:
 QDate date = std::chrono::year_month_day(std::chrono::year(2012),
                                         std::chrono::month(4),
                                         std::chrono::day(23));

 // Same, under `using std::chrono` convenience:
 QDate dateWithLiterals1 = 23d / April / 2012y;
 QDate dateWithLiterals2 = 2012y / April / 23;

 // Last day of February 2000
 QDate lastDayFeb2020 = 2000y / February / last;

 // First Monday of January 2020:
 QDate firstMonday = 2020y / January / Monday[0];

 // Last Monday of January 2020:
 QDate lastMonday = 2020y / January / Monday[last];
```

### `(since 6.4) QDate(std::chrono::year_month_weekday date)`

**作用与语义：**

构造包含年份`y`、月`m`和日`d`的日期。
该日期的理解是基于公历的。如果指定的日期无效，日期不被设定，`isValid()`返回`false`。
警告：第1年至第99年按原样解释。第0年无效。

### `QString toString(const QString &format, QCalendar cal) const`

**作用与语义：**

注意：该功能会让`QDate::toString()`重载。

## 6. 深入实践与常见坑

### 生命周期和资源边界

值对象由作用域、容器或调用者管理，不使用 parent 和 deleteLater。跨线程传递副本通常比传递 QObject 安全，但共享数据在写入时仍可能发生复制，性能和内存峰值要结合数据规模判断。

### 状态和错误边界

重点区分空值、无效值、默认值和已初始化值。例如空字符串、空 URL、null 图像和无效索引不一定表示同一件事；转换函数的失败结果要通过对应的状态查询确认。

### 线程边界

值类型本身通常可以复制后跨线程传递；不要把 data()/bits()/constData() 得到的指针当成跨线程长期有效的所有权。大对象频繁写入会触发 detach，应避免不必要的复制和格式转换。

### 最容易出现的错误

无效日期不等于空字符串；不要用 QDate 表示时间戳；`fromString()` 必须匹配格式和 locale；跨月加减遇到月末时要验证业务预期。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QDate` 所属机制类型：Qt 值类型与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
