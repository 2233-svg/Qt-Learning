# QCalendar

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“Calendar”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QCalendar` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QCalendar>`
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

- `(since 6.2) class SystemId`
- `enum class System { Gregorian, Julian, Milankovic, Jalali, IslamicCivil }`

### 公有函数

- `QCalendar()`
- `QCalendar(QAnyStringView name)`
- `QCalendar(QCalendar::System system)`
- `(since 6.2) QCalendar(QCalendar::SystemId id)`
- `QDate dateFromParts(const QCalendar::YearMonthDay &parts) const`
- `QDate dateFromParts(int year, int month, int day) const`
- `QString dateTimeToString(QStringView format, const QDateTime &datetime, QDate dateOnly, QTime timeOnly, const QLocale &locale) const`
- `int dayOfWeek(QDate date) const`
- `int daysInMonth(int month, int year = Unspecified) const`
- `int daysInYear(int year) const`
- `bool hasYearZero() const`
- `bool isDateValid(int year, int month, int day) const`
- `bool isGregorian() const`
- `bool isLeapYear(int year) const`
- `bool isLunar() const`
- `bool isLuniSolar() const`
- `bool isProleptic() const`
- `bool isSolar() const`
- `bool isValid() const`
- `(since 6.7) QDate matchCenturyToWeekday(const QCalendar::YearMonthDay &parts, int dow) const`
- `int maximumDaysInMonth() const`
- `int maximumMonthsInYear() const`
- `int minimumDaysInMonth() const`
- `QString monthName(const QLocale &locale, int month, int year = Unspecified, QLocale::FormatType format = QLocale::LongFormat) const`
- `int monthsInYear(int year) const`
- `QString name() const`
- `QCalendar::YearMonthDay partsFromDate(QDate date) const`
- `QString standaloneMonthName(const QLocale &locale, int month, int year = Unspecified, QLocale::FormatType format = QLocale::LongFormat) const`
- `QString standaloneWeekDayName(const QLocale &locale, int day, QLocale::FormatType format = QLocale::LongFormat) const`
- `QString weekDayName(const QLocale &locale, int day, QLocale::FormatType format = QLocale::LongFormat) const`

### 静态公有成员

- `QStringList availableCalendars()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum class QCalendar::System`

**作用与语义：**

这个枚举类型用于指定日历系统的选择。
- `QCalendar::System::Gregorian`: `0`; 默认日历，国际通用。
- `QCalendar::System::Julian`: `8`; 古罗马日历。
- `QCalendar::System::Milankovic`: `9`; 一些东正教教堂使用的修订儒略历。
- `QCalendar::System::Jalali`: `10`; 太阳伊斯兰历（也称波斯历）。
- `QCalendar::System::IslamicCivil`: `11`; （表格）伊斯兰民用历。

### `[explicit] QCalendar::QCalendar(QAnyStringView name)`

**作用与语义：**

构建一个日历对象。
选择所用历法可以通过`system`（枚举`QCalendar::System`）或`name`字符串（Unicode或拉丁1）来表示。按名称构造可能依赖于某个实例先通过其他方式构建。无参数时，默认构造器返回格里高利历。
注意：在6.4之前的Qt版本中，`name`的构造函数只接受`QStringView`和`QLatin1String`，不接受`QAnyStringView`。

### `[explicit, since 6.2] QCalendar::QCalendar(QCalendar::SystemId id)`

**作用与语义：**

构建一个日历对象。
选择所用历法可以通过`system`（枚举`QCalendar::System`）或`name`字符串（Unicode或拉丁1）来表示。按名称构造可能依赖于某个实例先通过其他方式构建。无参数时，默认构造器返回格里高利历。
注意：在6.4之前的Qt版本中，`name`的构造函数只接受`QStringView`和`QLatin1String`，不接受`QAnyStringView`。

### `[static] QStringList QCalendar::availableCalendars()`

**作用与语义：**

返回可用历法系统的名称列表。
这些代码可能由插件或其他代码提供，此外还有 Qt 提供的代码，其中一些由功能控制。

### `QDate QCalendar::dateFromParts(const QCalendar::YearMonthDay &parts) const`

**作用与语义：**

将年、月、天转换为`QDate`。
`year`、`month`和`day`可以作为单独的数字传递，也可以作为`parts`的成员打包在一起。如果有的话，返回一个包含该历法中给定年份、月份和月份的`QDate`。否则，包括任何值为QCalendar：：Unspecified的情况，返回一个isNull()为真的`QDate`。

### `QString QCalendar::dateTimeToString(QStringView format, const QDateTime &datetime, QDate dateOnly, QTime timeOnly, const QLocale &locale) const`

**作用与语义：**

返回表示给定日期、时间或日期-时间的字符串。
如果`datetime`有效，则表示它，并且识别日期和时间字段的格式化说明符;否则，如果`dateOnly`有效，则表示它，且仅识别日期字段的格式化说明符;最后，如果`timeOnly`有效，则表示，且仅识别时间字段的格式化说明符。如果这些都不成立，则返回空字符串。
有关支持的字段指定符，请参见 `QDate::toString` 和 `QTime::toString()`。`format`中被识别为字段指定词的字符会被表示所表示日期和/或时间的适当数据的文本替换。表示这些字符的文本可能取决于指定的`locale`。`format` 中的其他字符会被逐字复制到返回字符串中。

### `int QCalendar::dayOfWeek(QDate date) const`

**作用与语义：**

返回给定`date`的星期几编号。
如果日历无法表示指定日期，则返回零。返回周一的1，周日的7。带有召唤日的历法可用其他数字来表示这些日期。

### `int QCalendar::daysInMonth(int month, int year = Unspecified) const`

**作用与语义：**

返回给定`year` `month`的天数。
月份按顺序编号，每年第一个月以1开头。如果`year` `Unspecified`（默认，未通过），则返回该月份在任一年中最长的月份长度。

### `int QCalendar::daysInYear(int year) const`

**作用与语义：**

返回给定`year`的天数。
`Unspecified`的处理方式`year`尚不明确。

### `bool QCalendar::hasYearZero() const`

**作用与语义：**

如果这个日历是零年，退货会`true`。
历法可以表示从第一年开始的年份，但无法描述其第一年之前的年份;这样的历法没有零年，也不是预言的。
表示其第一年之前的历法，可以通过通常的整数计数来编号这些年，即第一年之前的年份为零年，负数年份在前;这样的历法是预言性的，具有零年。一个历法也可能有零年（例如某重大事件的年份，后续年份为该事件后的一年，第二年依此类推），但不描述其零年前的年份。这样的历法会有一个零年，但并非预言性的。
然而，有些历法用替代编号表示其第一年之前的年份;例如，预言格里高利历的第一年为公元1年，前一年为公元前1年，前一年为公元前2年，依此类推。在这种情况下，我们使用负数年来表示这种替代编号，比如年-1为第一年前的一年，-2年为-1年前的一年，依此类推。这样的历法是预言历，但没有零年。

### `bool QCalendar::isDateValid(int year, int month, int day) const`

**作用与语义：**

如果给定的`year`、`month`和`day`在该历法中指定有效日期，返回`true`。
通常这意味着1<= 月<= `monthsInYear`年，1<= 天<= `daysInMonth`月，年）。然而，带有插入日或月的历法可能会使情况复杂。

### `bool QCalendar::isGregorian() const`

**作用与语义：**

如果该历对象是其他 Qt API 默认使用的格里高利历对象，例如在 `QDate` 中，则返回`true`。

### `bool QCalendar::isLeapYear(int year) const`

**作用与语义：**

如果给定`year`是闰年，回报率`true`。
由于一年不是整数天，有些年份比其他年份更长。差异可能是一个月，也可能只有一天;具体细节因日历而异。

### `bool QCalendar::isLunar() const`

**作用与语义：**

如果这个历法是阴历，返回的话`true`。
阴历主要基于月相。

### `bool QCalendar::isLuniSolar() const`

**作用与语义：**

如果这个历法是月太阳历，回归`true`。
阴阳历表示月相，同时调整自身以追踪太阳相对于固定恒星在天空中变化的位置。

### `bool QCalendar::isProleptic() const`

**作用与语义：**

如果这个历法是预估的，回归`true`。
预言历能够任意描述其初始年份之前很久的年份。这些年份用负数表示，可能用零年。

### `bool QCalendar::isSolar() const`

**作用与语义：**

如果这个日历是太阳能的，回`true`。
太阳历主要基于太阳在天空中相对于固定恒星的位置变化。

### `bool QCalendar::isValid() const`

**作用与语义：**

如果这是有效的日历对象，则返回为真。
用未识别的日历名称构建日历可能导致对象无效。创建日历后，请使用此方法进行检查。

### `[since 6.7] QDate QCalendar::matchCenturyToWeekday(const QCalendar::YearMonthDay &parts, int dow) const`

**作用与语义：**

调整日期的世纪以匹配某一周中的某一天。
用于给定日期的星期、月、月份和年份的最后两位数字。返回以给定`dow`为`dayOfWeek()`的`QDate`实例，与月份和月份的`parts`匹配。返回`QDate`的`year()`与`parts.year`相差100倍，偏好小倍数而非大倍数，且偏好正倍数而非其否定值。
如果没有日期符合这些条件，则返回无效`QDate`：星期几与其他数据不兼容。例如，格里高利历400年周期为整数周，因此该月的任意月份和日期，在后两位数字的年份中，只有四天才会被安排在一周的四天。（在世纪之交的2月29日这一闰年特殊情况下，一周中只有一天可能：星期二。）。

### `int QCalendar::maximumDaysInMonth() const`

**作用与语义：**

返回历法中最长月份的天数，无论哪一年。

### `int QCalendar::maximumMonthsInYear() const`

**作用与语义：**

返回任何一年中最多月份的回报。

### `int QCalendar::minimumDaysInMonth() const`

**作用与语义：**

返回历法中最短月份的天数，无论哪一年。

### `QString QCalendar::monthName(const QLocale &locale, int month, int year = Unspecified, QLocale::FormatType format = QLocale::LongFormat) const`

**作用与语义：**

一个月内会回归一个本地化的名称。
月份用数字表示，`month` = 1 表示一年的第一个月，随后的月份编号相应。如果`month`数字未被识别，返回空字符串。
`year`可能是未指定的，此时应使用典型年份月份的数字与名称的映射。一些历法的闰月不总是在年底;月数与名称的映射可能取决于闰月的位置。因此，如果已知年份，通常应指定年份。
名称以通常在完整日期中使用的形式返回，在指定的`locale`日期内;`format`决定了其表达的完整程度（即缩写的程度）。

### `int QCalendar::monthsInYear(int year) const`

**作用与语义：**

返回给定`year`中的月份数。
如果`year`被`Unspecified`，则返回一年中最多的月份数。

### `QString QCalendar::name() const`

**作用与语义：**

这个历法的主要名称。
日历也可能有一些别名。以名称实例化的日历可以使用此类别名，此时其名称()不必与实例化时的别名相匹配。

### `QCalendar::YearMonthDay QCalendar::partsFromDate(QDate date) const`

**作用与语义：**

将`QDate`转换为年份、月份和月份。
如果历法无法代表给定的 `date`，则返回结构的 `isValid()` 为假。否则，其年份、月份和日子成员将记录其表示中所列部分。

### `QString QCalendar::standaloneMonthName(const QLocale &locale, int month, int year = Unspecified, QLocale::FormatType format = QLocale::LongFormat) const`

**作用与语义：**

一个月内会以一个本地化的独立名称返回。
月份用数字表示，`month` = 1 表示该年的第一个月及相应编号的后续月份。如果未识别`month`数字，返回空字符串。
`year`可能是未指定的，在这种情况下应使用典型年份月份的数字映射到名称。有些历法的闰月并不总是在年底;它们将月份数字映射到名称的过程可能取决于闰月的位置。因此，如果已知年份，通常应指定年份。
名称以指定`locale`中单独使用的形式返回;`format`决定了该名称应如何完整表达（即缩写程度）。

### `QString QCalendar::standaloneWeekDayName(const QLocale &locale, int day, QLocale::FormatType format = QLocale::LongFormat) const`

**作用与语义：**

返回一个适合本地化的独立名称，适用于一周中的某一天。
星期几编号从周一的1到周日的7。有些日历可能支持其他日子的更高数字（例如不属于任何周的召唤日）。如果`day`数字未被识别，则返回空字符串。
名称以单独使用的形式返回（例如作为日历表格中月份的列标题，月份以连续周为行），在指定`locale`中;`format`决定了名称应表达得多完整（即缩写程度）。

### `QString QCalendar::weekDayName(const QLocale &locale, int day, QLocale::FormatType format = QLocale::LongFormat) const`

**作用与语义：**

返回一个适合本地化的星期几名称。
星期几编号从周一的1到周日的7。有些日历可能支持其他日子的更高数字（例如不属于任何周的轮换日）。如果`day`数字未被识别，则返回空字符串。
名称以通常在完整日期中使用的形式返回，在指定`locale`中;`format`决定了该名称应如何完整表达（即缩写的程度）。

### `(since 6.2) class SystemId`

**作用与语义：**

这是一种不透明类型，用于识别自定义日历实现。该类型值唯一支持的来源是后端的`calendarId()`方法。该类型的值如果`isValid()`为假，则无法识别成功注册的后端。该类型值的唯一有效使用者是`QCalendar`构造器，只有当传递给它的ID有效时，构造器才会产生有效的`QCalendar`实例。

### `QCalendar()`

**作用与语义：**

构建一个日历对象。
选择所用历法可以通过`system`（枚举`QCalendar::System`）或`name`字符串（Unicode或拉丁1）来表示。按名称构造可能依赖于某个实例先通过其他方式构建。无参数时，默认构造器返回格里高利历。
注意：在6.4之前的Qt版本中，`name`的构造函数只接受`QStringView`和`QLatin1String`，不接受`QAnyStringView`。

### `QCalendar(QCalendar::System system)`

**作用与语义：**

构建一个日历对象。
使用自定义日历实现时，其后端在创建时会被分配一个唯一ID;将该ID作为`id`传递给该构造器，会获得使用该后端的QCalendar。当后端没有以名称注册时，这非常有用。

### `QDate dateFromParts(int year, int month, int day) const`

**作用与语义：**

将年、月、天转换为`QDate`。
`year`、`month`和`day`可以作为单独的数字传递，也可以作为`parts`的成员打包在一起。如果有的话，返回一个包含该历法中给定年份、月份和月份的`QDate`。否则，包括任何值为QCalendar：：Unspecified的情况，返回一个isNull()为真的`QDate`。

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

`QCalendar` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
