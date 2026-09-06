# QDateTime

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 日期加时间值类型，负责时间点、时区、时间戳、比较、解析和格式化。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QDateTime`：日期加时间值类型，负责时间点、时区、时间戳、比较、解析和格式化。

**内部模型：** 这类类型通常可以按值传递、复制和返回。许多 Qt 容器、字符串和图像采用隐式共享：复制时共享数据，发生写操作时才 detach。这样便于 API 传值，但获取原始指针或长期持有引用时必须考虑对象修改和生命周期。

**适用场景：** 先确认值的有效性和表示格式，再调用查询、转换或修改 API；处理文本时区分 Unicode 和字节编码，处理图像时确认 format，处理 URL/路径时使用 Qt 的解析 API 而不是手写字符串规则。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要把空值当成业务成功；不要保存临时对象的内部指针；不要把 QString 当二进制缓冲区；不要假定隐式共享让并发写入自动安全。

## 2. 依赖与对象关系

- 头文件：`#include <QDateTime>`
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

- `(since 6.7) enum class TransitionResolution { Reject, RelativeToBefore, RelativeToAfter, PreferBefore, PreferAfter, …, PreferDaylightSaving }`
- `enum class YearRange { First, Last }`

### 公有函数

- `QDateTime(QDate date, QTime time, const QTimeZone &timeZone, QDateTime::TransitionResolution resolve = TransitionResolution::LegacyBehavior)`
- `QDateTime()`
- `(since 6.5) QDateTime(QDate date, QTime time, QDateTime::TransitionResolution resolve = TransitionResolution::LegacyBehavior)`
- `QDateTime(const QDateTime &other)`
- `QDateTime(QDateTime &&other)`
- `~QDateTime()`
- `QDateTime addDays(qint64 ndays) const`
- `(since 6.4) QDateTime addDuration(std::chrono::milliseconds msecs) const`
- `QDateTime addMSecs(qint64 msecs) const`
- `QDateTime addMonths(int nmonths) const`
- `QDateTime addSecs(qint64 s) const`
- `QDateTime addYears(int nyears) const`
- `QDate date() const`
- `qint64 daysTo(const QDateTime &other) const`
- `bool isDaylightTime() const`
- `bool isNull() const`
- `bool isValid() const`
- `qint64 msecsTo(const QDateTime &other) const`
- `int offsetFromUtc() const`
- `qint64 secsTo(const QDateTime &other) const`
- `void setDate(QDate date, QDateTime::TransitionResolution resolve = TransitionResolution::LegacyBehavior)`
- `void setMSecsSinceEpoch(qint64 msecs)`
- `void setSecsSinceEpoch(qint64 secs)`
- `void setTime(QTime time, QDateTime::TransitionResolution resolve = TransitionResolution::LegacyBehavior)`
- `void setTimeZone(const QTimeZone &toZone, QDateTime::TransitionResolution resolve = TransitionResolution::LegacyBehavior)`
- `void swap(QDateTime &other)`
- `QTime time() const`
- `(since 6.5) QTimeZone timeRepresentation() const`
- `Qt::TimeSpec timeSpec() const`
- `QTimeZone timeZone() const`
- `QString timeZoneAbbreviation() const`
- `CFDateRef toCFDate() const`
- `QDateTime toLocalTime() const`
- `qint64 toMSecsSinceEpoch() const`
- `NSDate * toNSDate() const`
- `QDateTime toOffsetFromUtc(int offsetSeconds) const`
- `qint64 toSecsSinceEpoch() const`
- `(since 6.4) std::chrono::sys_time<std::chrono::milliseconds> toStdSysMilliseconds() const`
- `(since 6.4) std::chrono::sys_seconds toStdSysSeconds() const`
- `QString toString(const QString &format, QCalendar cal) const`
- `QString toString(QStringView format) const`
- `QString toString(Qt::DateFormat format = Qt::TextDate) const`
- `QString toString(const QString &format) const`
- `QString toString(QStringView format, QCalendar cal) const`
- `QDateTime toTimeZone(const QTimeZone &timeZone) const`
- `QDateTime toUTC() const`
- `(since 6.4) QDateTime & operator+=(std::chrono::milliseconds duration)`
- `(since 6.4) QDateTime & operator-=(std::chrono::milliseconds duration)`
- `QDateTime & operator=(const QDateTime &other)`

### 静态公有成员

- `(since 6.5) QDateTime currentDateTime(const QTimeZone &zone)`
- `QDateTime currentDateTime()`
- `QDateTime currentDateTimeUtc()`
- `qint64 currentMSecsSinceEpoch()`
- `qint64 currentSecsSinceEpoch()`
- `QDateTime fromCFDate(CFDateRef date)`
- `QDateTime fromMSecsSinceEpoch(qint64 msecs, const QTimeZone &timeZone)`
- `QDateTime fromMSecsSinceEpoch(qint64 msecs)`
- `QDateTime fromNSDate(const NSDate *date)`
- `QDateTime fromSecsSinceEpoch(qint64 secs, const QTimeZone &timeZone)`
- `QDateTime fromSecsSinceEpoch(qint64 secs)`
- `(since 6.4) QDateTime fromStdLocalTime(const std::chrono::local_time<std::chrono::milliseconds> &time)`
- `(since 6.4) QDateTime fromStdTimePoint(const std::chrono::time_point<Clock, Duration> &time)`
- `(since 6.4) QDateTime fromStdTimePoint(const std::chrono::local_time<std::chrono::milliseconds> &time)`
- `(since 6.4) QDateTime fromStdTimePoint(std::chrono::time_point<std::chrono::system_clock, std::chrono::milliseconds> time)`
- `(since 6.4) QDateTime fromStdZonedTime(const int &time)`
- `QDateTime fromString(const QString &string, const QString &format, int baseYear, QCalendar cal)`
- `(since 6.0) QDateTime fromString(QStringView string, Qt::DateFormat format = Qt::TextDate)`
- `QDateTime fromString(const QString &string, Qt::DateFormat format = Qt::TextDate)`
- `(since 6.0) QDateTime fromString(QStringView string, QStringView format, QCalendar cal)`
- `(since 6.7) QDateTime fromString(QStringView string, QStringView format, int baseYear = QLocale::DefaultTwoDigitBaseYear)`
- `(since 6.0) QDateTime fromString(const QString &string, QStringView format, QCalendar cal)`
- `(since 6.7) QDateTime fromString(const QString &string, QStringView format, int baseYear = QLocale::DefaultTwoDigitBaseYear)`
- `QDateTime fromString(const QString &string, const QString &format, QCalendar cal)`
- `(since 6.7) QDateTime fromString(const QString &string, const QString &format, int baseYear = QLocale::DefaultTwoDigitBaseYear)`
- `(since 6.7) QDateTime fromString(QStringView string, QStringView format, int baseYear, QCalendar cal)`
- `(since 6.0) QDateTime fromString(const QString &string, QStringView format, int baseYear, QCalendar cal)`

### 相关非成员函数

- `bool operator!=(const QDateTime &lhs, const QDateTime &rhs)`
- `(since 6.4) QDateTime operator+(const QDateTime &dateTime, std::chrono::milliseconds duration)`
- `(since 6.4) QDateTime operator+(std::chrono::milliseconds duration, const QDateTime &dateTime)`
- `(since 6.4) std::chrono::milliseconds operator-(const QDateTime &lhs, const QDateTime &rhs)`
- `(since 6.4) QDateTime operator-(const QDateTime &dateTime, std::chrono::milliseconds duration)`
- `bool operator<(const QDateTime &lhs, const QDateTime &rhs)`
- `QDataStream & operator<<(QDataStream &out, const QDateTime &dateTime)`
- `bool operator<=(const QDateTime &lhs, const QDateTime &rhs)`
- `bool operator==(const QDateTime &lhs, const QDateTime &rhs)`
- `bool operator>(const QDateTime &lhs, const QDateTime &rhs)`
- `bool operator>=(const QDateTime &lhs, const QDateTime &rhs)`
- `QDataStream & operator>>(QDataStream &in, QDateTime &dateTime)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[since 6.7] enum class QDateTime::TransitionResolution`

**作用与语义：**

该枚举用于解析落入时区转换的日期时间组合。
当构造一个日期时间，以当地时间或具有夏令时的时区来表示，或用`setDate()`、`setTime()`或`setTimeZone()`修订时，给定参数可能意味着一个时间表示，该表示在该区域内要么没有意义，要么有两个含义。这些时间表示被描述为处于过渡区。无论哪种情况，我们都可以返回一个无效的日期时间，表示操作定义不明确。在模糊情况下，我们可以选择两个可能指的时间之一。当没有意义时，我们可以选择其任一一侧的时间，且可能被合理地指着。例如，从较早时间推进时，我们可以选择转移后的时间，实际上是该时间后指定的时间。这里指定的选项配置了这种选择的执行方式。
- `QDateTime::TransitionResolution::Reject`：`0`;将过渡中的任意时间视为无效。要么它确实有效，要么是模糊的。
- `QDateTime::TransitionResolution::RelativeToBefore`：`1`;选择时间，仿佛从过渡前的某个时间向前迈进。它利用转换前生效的偏移量来解释请求的时间，并在必要时将结果转换为该时间点生效的偏移。
- `QDateTime::TransitionResolution::RelativeToAfter`：`2`;选择时间，仿佛从转移后的时间倒退。该方法利用转移后生效的偏移来解释请求时间，并在必要时将结果转换为该时间点生效的偏移。
- `QDateTime::TransitionResolution::PreferBefore`：`3`;选择过渡前的时间，
- `QDateTime::TransitionResolution::PreferAfter`：`4`;选择过渡后的某个时间点。
- `QDateTime::TransitionResolution::PreferStandard`：`5`;选择过渡标准时间侧的时间。
- `QDateTime::TransitionResolution::PreferDaylightSaving`：`6`;选择过渡中夏令时一侧的时间。
另一个常量`LegacyBehavior`被用作某些构造函数和设定器函数中过渡解析参数的默认值。这是`RelativeToBefore`的别名，实现了最接近Qt 6.7之前`QDateTime`行为的行为。
对于`addDays()`、`addMonths()`或`addYears()`，行为是，并且（大多数情况下）如果添加正向调整时使用`RelativeToBefore`正向调整，使用`RelativeToAfter`作为负向调整。
注意：在夏令时增加夏季与UTC偏移（称为“正夏令时”）的时区，PreferStandard是RelativeToAfter的别名，PreferDaylightSaving是RelativeToBefore的别名。在夏令时机制减少冬季UTC偏移（称为“负DST”）的时区，情况相反，前提是操作系统会报告日期时间是DST还是标准时间。对于某些平台，即使`Qt::TimeZone`日期时间也无法获得过渡细节，`QTimeZone`必须假定偏移较小的一方为标准时间，实际上假设正DST。
下表展示了`QDateTime`构造器如何在当地时间在02：00至03：00之间有过渡的一天，在两种可能情况下，识别标准时间LST，同时两侧为夏令时LDT，解决02：30的请求。转换类型可能是跳过一小时或重复。过渡类型和参数值`resolve`决定当天选择的实际时间。首先，常见的正夏令时情况，其中：
- `Before`：02：00–03：00;之后;`resolve`;精选
- `LST`：skip;LDT;RelativeToBefore;03：30 LDT
- `LST`：skip;LDT;RelativeToAfter;01：30 LST
- `LST`：skip;LDT;PreferBefore;01：30 LST（LST）
- `LST`：skip;LDT;PreferAfter;03：30 LDT
- `LST`：skip;LDT;PreferStandard;01：30 LST（世界标准时）
- `LST`：跳过;LDT;PreferDaylightSaving;03：30 LDT
- `LDT`：重复;LST;RelativeToBefore;02：30 LDT
- `LDT`：重复;LST;RelativeToAfter;02：30 LST
- `LDT`：重复;LST;PreferBefore;02：30 LDT
- `LDT`：重复;LST;PreferAfter;02：30 LST（LST）
- `LDT`：重复;LST;PreferStandard;02：30 LST
- `LDT`：重播;LST;优先夏令时;02：30 LDT
其次，关于负日光節約的理由，冬季使用LDT，夏季跳过一小时切换到LST，然后在过渡回冬季时重复一小时：
- `LDT`：跳过;LST;RelativeToBefore;03：30 LST
- `LDT`：skip;LST;RelativeToAfter;01：30 LDT
- `LDT`：跳过;LST;优先前;01：30 LDT
- `LDT`：跳过;LST;PreferAfter;03：30 LST
- `LDT`：skip;LST;PreferStandard;03：30 LST
- `LDT`：跳过;LST;偏好夏令时间;01：30 LDT
- `LST`：重复;LDT;RelativeToBefore;02：30 LST
- `LST`：重复;LDT;RelativeToAfter;02：30 LDT
- `LST`：重复;LDT;优先前;02：30 LST
- `LST`：重复;LDT;PreferAfter;02：30 LDT
- `LST`：重复;LDT;PreferStandard;02：30 LST
- `LST`：重播;LDT;PreferDaylightSaving;02：30 LDT
拒绝可以用来提示相关`QDateTime` API返回无效的datetime对象，以便你的代码能自行处理过渡，例如提醒用户他们选择的日期时间处于过渡区间内，从而给他们解决冲突或歧义的机会。使用这种方法的代码可能会发现上述其他选项有助于确定相关信息，用于自身（或用户）的解决。如果过渡的开始或结束，或过渡本身的时刻是正确的分辨率，`QTimeZone`的过渡API可以用来获取该信息。你可以通过使用`secsTo()`测量前一天中午和之后几天中午之间的实际时间，来判断过渡是重复还是跳过的。跳过的间隔（如弹簧前进）将缩短至48小时以下，重复间隔（如回退）则超过48小时。
注意：当指定除拒绝外的解析时，尽可能返回有效的`QDateTime`对象。如果请求的日期时间落在空档中，返回的日期时间不会包含请求的`time()`——或者在某些情况下，如果跳过了整天，则不会包含该请求的`date()`。因此，您可以通过比较`date()`和`time()`与请求的空档来检测空缺。
Python 编程语言的 datetime API 有一个 `fold` 参数，对应于 `RelativeToBefore`（`fold = True`）和 `RelativeToAfter`（`fold = False`）。
替代JavaScript `Date`的`Temporal`提案提供了四个解决过渡的选项，作为`disambiguation`参数的值。其`'reject'`引发一个例外，大致相当于产生无效结果的`Reject`。其`'earlier'`和`'later'`选项对应于`PreferBefore`和`PreferAfter`。它的`'compatible'`选项对应于`RelativeToBefore`（以及Python的`fold = True`）。
该枚举于Qt 6.7引入。

### `enum class QDateTime::YearRange`

**作用与语义：**

这种列举类型描述了可表示的年份范围（在公历中），`QDateTime`：
- `QDateTime::YearRange::First`：`-292275056`;今年后期可代表
- `QDateTime::YearRange::Last`：`+292278994`;今年的早期部分可代表
所有严格介于这两年之间的日期也可以表示。但请注意，公历没有零年。
注：`QDate`可以描述更广泛的年份范围。在大多数情况下，这影响不大，因为`QDateTime`能支持的年份范围可达1970年前后2.92亿年。

### `QDateTime::QDateTime(QDate date, QTime time, const QTimeZone &timeZone, QDateTime::TransitionResolution resolve = TransitionResolution::LegacyBehavior)`

**作用与语义：**

利用`timeZone`描述的时间表示，构造带有给定`date`和`time`的日期时间。
如果`date`有效且`time`无效，时间将设为午夜。如果`timeZone`无效，则日期时间无效。如果`date`和`time`描述了接近`timeZone`过渡的时刻，`resolve`控制该情况的解决方式。
注意：在Qt 6.7之前，该函数版本缺少`resolve`参数，因此无法解决与转移相关的歧义。

### `[noexcept] QDateTime::QDateTime()`

**作用与语义：**

构造一个空日期时间，名义上使用本地时间。
空日期时间无效，因为其日期和时间均无效。

### `[since 6.5] QDateTime::QDateTime(QDate date, QTime time, QDateTime::TransitionResolution resolve = TransitionResolution::LegacyBehavior)`

**作用与语义：**

利用当地时间，用给定的`date`和`time`构造一个日期时间。
如果`date`有效且`time`无效，则午夜作为时间。如果`date`和`time`描述了接近本地时间过渡的时刻，`resolve`控制该情况的解决方式。
注意：在Qt 6.7之前，该函数版本缺少`resolve`参数，因此无法解决与转移相关的歧义。

### `[noexcept] QDateTime::QDateTime(const QDateTime &other)`

**作用与语义：**

构建`other`日期时间的副本。

### `[noexcept] QDateTime::QDateTime(QDateTime &&other)`

**作用与语义：**

将临时`other` datetime的内容迁移到该对象，并`other`处于未指定（但适当的）状态。

### `[noexcept] QDateTime::~QDateTime()`

**作用与语义：**

毁了约会时间。

### `QDateTime QDateTime::addDays(qint64 ndays) const`

**作用与语义：**

返回一个`QDateTime`对象，包含比该对象日期时间晚`ndays`天（或如果`ndays`为负则更早）。
如果`timeSpec()`为`Qt::LocalTime`或`Qt::TimeZone`，且结果时间落在标准夏令时到夏令时的过渡时，那么结果将刚好超过该间隔，朝着变化方向。如果过渡时间为凌晨2点，时钟快进到凌晨3点，则将调整为凌晨2点前（如`ndays < 0`）或凌晨3点后。

### `[since 6.4] QDateTime QDateTime::addDuration(std::chrono::milliseconds msecs) const`

**作用与语义：**

返回一个`QDateTime`对象，包含比该对象日期时间晚`msecs`毫秒（或如果`msecs`为负则更早）。
如果该日期时间无效，则返回一个无效日期时间。
注意：用`std::chrono::months`或`std::chrono::years`表示的持续时间，无法得到与`addMonths()`或`addYears()`相同的结果。前者是固定的持续时间，基于太阳年计算;后者使用格里高利历中月份/年份的定义。

### `QDateTime QDateTime::addMSecs(qint64 msecs) const`

**作用与语义：**

返回一个`QDateTime`对象，包含比该对象日期时间晚`msecs`毫秒（或如果`msecs`为负则更早）。
如果该日期时间无效，则返回一个无效日期时间。

### `QDateTime QDateTime::addMonths(int nmonths) const`

**作用与语义：**

返回一个`QDateTime`对象，包含比该对象日期时间晚`nmonths`个月（或如果`nmonths`为负则更早）。
如果`timeSpec()`为`Qt::LocalTime`或`Qt::TimeZone`，且结果落在标准夏令时至夏令时的过渡时，那么结果将刚好超过这一间隙，朝着变化方向。如果过渡在凌晨2点，时钟快进到凌晨3点，则在凌晨2点到3点之间进行调整，如果`nmonths < 0`，则在凌晨2点之前，否则则在凌晨3点之后。

### `QDateTime QDateTime::addSecs(qint64 s) const`

**作用与语义：**

返回一个`QDateTime`对象，包含比该对象日期时间晚`s`秒（如果`s`为负则更早）。
如果该日期时间无效，则返回一个无效日期时间。

### `QDateTime QDateTime::addYears(int nyears) const`

**作用与语义：**

返回一个`QDateTime`对象，包含比该对象日期时间晚`nyears`年（或如果`nyears`为负则更早）。
如果`timeSpec()`为`Qt::LocalTime`或`Qt::TimeZone`，且结果时间落在标准夏令时到夏令时的过渡时段内，那么结果将刚好超过该间隔，朝着变化方向。如果过渡时间为凌晨2点，时钟快进到凌晨3点，则2点至凌晨3点的目标将调整为凌晨2点之前（如果`nyears < 0`）或3点之后（否则）。

### `[static, since 6.5] QDateTime QDateTime::currentDateTime(const QTimeZone &zone)`

**作用与语义：**

返回系统时钟当前的日期时间，使用`zone`描述的时间表示法。如果省略`zone`，则使用本地时间。

### `[static] QDateTime QDateTime::currentDateTime()`

**作用与语义：**

注意：该功能会让`QDateTime::currentDateTime()`重载。

### `[static] QDateTime QDateTime::currentDateTimeUtc()`

**作用与语义：**

返回系统时钟当前的日期时间，以UTC表示。
相当于`currentDateTime(QTimeZone::UTC)`。

### `[static noexcept] qint64 QDateTime::currentMSecsSinceEpoch()`

**作用与语义：**

返回自1970年UTC起的当前毫秒数。
这个数字类似于POSIX的time_t变量，但以毫秒为单位表示，而不是秒。

### `[static noexcept] qint64 QDateTime::currentSecsSinceEpoch()`

**作用与语义：**

返回自1970年UTC起的秒数。
这个数字就像POSIX time_t变量。

### `QDate QDateTime::date() const`

**作用与语义：**

返回datetime中的日期部分。

### `qint64 QDateTime::daysTo(const QDateTime &other) const`

**作用与语义：**

返回从该日期时间到`other`日期时间的天数。天数计算为从该日期时间到`other`日期时间之间达到午夜的次数。这意味着从23：55到第二天0：05相差10分钟，算作一天。
如果`other`日期时间早于该日期时间，返回的值为负。

**官方示例：**

```cpp
 QDateTime startDate(QDate(2012, 7, 6), QTime(8, 30, 0));
 QDateTime endDate(QDate(2012, 7, 7), QTime(16, 30, 0));
 qDebug() << "Days from startDate to endDate: " << startDate.daysTo(endDate);

 startDate = QDateTime(QDate(2012, 7, 6), QTime(23, 55, 0));
 endDate = QDateTime(QDate(2012, 7, 7), QTime(0, 5, 0));
 qDebug() << "Days from startDate to endDate: " << startDate.daysTo(endDate);

 qSwap(startDate, endDate); // Make endDate before startDate.
 qDebug() << "Days from startDate to endDate: " << startDate.daysTo(endDate);
```

### `[static] QDateTime QDateTime::fromCFDate(CFDateRef date)`

**作用与语义：**

构建包含CFDate副本的新`QDateTime` `date`。

### `[static] QDateTime QDateTime::fromMSecsSinceEpoch(qint64 msecs, const QTimeZone &timeZone)`

**作用与语义：**

返回一个日期时间，表示1970年UTC起点后给定数`msecs`毫秒的时刻，`timeZone`规定。默认时间表示为当地时间。
注意，`msecs`的值可能超出有效`QDateTime`范围，包括负值和正值。该函数在这些值下的行为未定义。

### `[static] QDateTime QDateTime::fromMSecsSinceEpoch(qint64 msecs)`

**作用与语义：**

注意：该功能会超载`QDateTime::fromMSecsSinceEpoch()`。

### `[static] QDateTime QDateTime::fromNSDate(const NSDate *date)`

**作用与语义：**

构建包含NSDate复印件的新`QDateTime` `date`。

### `[static] QDateTime QDateTime::fromSecsSinceEpoch(qint64 secs, const QTimeZone &timeZone)`

**作用与语义：**

返回一个日期时间，表示1970年UTC开始后`secs`秒数的指定时刻，该时间由`timeZone`规定。默认时间表示为当地时间。
注意，存在一些可能的`secs`值超出有效`QDateTime`范围，包括负值和正值。该函数的行为在这些值下未定义。

### `[static] QDateTime QDateTime::fromSecsSinceEpoch(qint64 secs)`

**作用与语义：**

注意：该功能会超载`QDateTime::fromSecsSinceEpoch()`。

### `[static, since 6.4] QDateTime QDateTime::fromStdLocalTime(const std::chrono::local_time<std::chrono::milliseconds> &time)`

**作用与语义：**

构造一个日期时间，其日期和时间为由`time`表示的毫秒数，自1970-01-01T00：00：00.000以当地时间（`Qt::LocalTime`）开始计数。
注意：此函数需要C 20。

### `[static, since 6.4] template <typename Clock, typename Duration> QDateTime QDateTime::fromStdTimePoint(const std::chrono::time_point<Clock, Duration> &time)`

**作用与语义：**

构造一个表示与`time`同一时间点的日期时间，使用`Qt::UTC`作为时间表示。
`time`的时钟必须与`std::chrono::system_clock`兼容;特别地，必须存在`std::chrono::clock_cast`支持的转换。转换完成后，结果的时长类型必须可转换为`std::chrono::milliseconds`。
如果不是这样，调用方必须对`std::chrono::system_clock`进行必要的时钟转换，并对时长类型（铸造/圆/地板/天幕/等）进行必要的转换，以确保该函数的输入满足上述约束。
注意：此函数需要C 20。

### `[static, since 6.4] QDateTime QDateTime::fromStdTimePoint(const std::chrono::local_time<std::chrono::milliseconds> &time)`

**作用与语义：**

构造一个日期时间，其日期和时间为由`time`表示的毫秒数，自1970-01-01T00：00：00.000以当地时间（`Qt::LocalTime`）开始计数。
注意：此函数需要C 20。

### `[static, since 6.4] QDateTime QDateTime::fromStdTimePoint(std::chrono::time_point<std::chrono::system_clock, std::chrono::milliseconds> time)`

**作用与语义：**

构造一个表示与`time`相同时间点的日期时间，使用`Qt::UTC`作为其时间表示。
注意：该功能会让`QDateTime::fromStdTimePoint()`重载。

### `[static, since 6.4] QDateTime QDateTime::fromStdZonedTime(const int &time)`

**作用与语义：**

构造一个与`time`相同的时间点。结果将以`time`的时区表示。
注意：此函数需要C 20。

### `[static] QDateTime QDateTime::fromString(const QString &string, const QString &format, int baseYear, QCalendar cal)`

**作用与语义：**

返回`string`所代表的`QDateTime`，使用给定的`format`;如果字符串无法解析，则返回无效的日期时间。
如果提供，使用历`cal`，否则使用公历。
当`format`只指定年份的最后两位时，首先考虑的候选对象是从`baseYear`开始的100年。6.7之前没有`baseYear`参数，始终使用1900年。这是`baseYear`的默认，选择从那时到1999年的年份。在某些情况下，其他字段可能会选择下一个或上一个世纪，以获得与所有字段一致的结果。详情请参见 `QDate::fromString()`。
除了格式字符串中识别的表达式（用`QDate::fromString()`和 `QTime::fromString()`表示日期和时间的部分外，该方法还支持：
- `Expression`：输出
- `t`：时区（偏移、名称、“Z”或带“UTC”前缀的偏移）
- `tt`：时区，按偏移格式表示，小时和分钟之间无冒号（例如“0200”）
- `ttt`：时区偏移格式，时与分钟之间加冒号（例如“02：00”）
- `tttt`：时区名称，可能是`QTimeZone::displayName()`报告的`QTimeZone::LongName`或该区域的IANA ID（例如“Europe/Berlin”）。识别的名称是`QTimeZone`已知的，这可能取决于所使用的操作系统。
如果没有“t”格式的指定符，则使用系统的本地时区。关于所有其他字段的默认设置，请参见`QDate::fromString()`和 `QTime::fromString()`。
所有其他输入字符都将被视为文本。任何非空的字符序列如果被单引号包围，也会被当作文本处理（去掉引号），不会被解释为表达式。
如果格式不满足，则返回无效`QDateTime`。如果格式满足但`string`表示无效的日期时间（例如时区跳过的间隔），则返回一个有效的`QDateTime`，代表一个有效的近时间。
没有前置零的表达式（d、M、h、m、s、z）会变得贪婪。这意味着即使这会超出范围和/或留给其他部分的数字太少，他们也会使用两位数字（或三位，z）。
这本可以指1月1日00：30：00，但M会抓取两位数字。
`string`字段错误的字段会导致返回无效`QDateTime`。仅支持本地时间从100年开始到9999年末之间的日期时间。注意，在其他时区，尤其是UTC中，接近该范围末端的日期时间，可能超出该范围（因此被视为无效），具体取决于当地时区。
注意：日期和月份名称以及AM/PM指示必须以英文（C语言格式）表示。如果需要识别本地化的月份和日期名称或AM/PM的本地化形式，请使用`QLocale::system()`.toDateTime()。
注意：如果使用该格式字符重复次数超过表中最长表达式，该格式部分将被读取为多个表达式，且无分隔符;上述最长字符可能重复次数与其副本数量相等，结尾剩余表达式可能更短。因此`'tttttt'`匹配`"Europe/BerlinEurope/Berlin"`并将区域设置为柏林时间;如果datetime字符串包含“Europe/BerlinZ”，则会“匹配”但结果不一致，导致日期时间无效。

**官方示例：**

```cpp
 QDateTime dateTime = QDateTime::fromString("1.30.1", "M.d.s");
 // dateTime is January 30 in 1900 at 00:00:01.
 dateTime = QDateTime::fromString("12", "yy");
 // dateTime is January 1 in 1912 at 00:00:00.
```

### `[static, since 6.0] QDateTime QDateTime::fromString(QStringView string, Qt::DateFormat format = Qt::TextDate)`

**作用与语义：**

注意：该功能会超载`QDateTime::fromString()`。

### `[static] QDateTime QDateTime::fromString(const QString &string, Qt::DateFormat format = Qt::TextDate)`

**作用与语义：**

返回`string`表示的`QDateTime`，使用给定的`format`，或者如果无法返回则返回无效的日期时间。
`Qt::TextDate`注意：仅认可英文短月名（例如简称“Jan”或长称“January”）。

### `[static, since 6.0] QDateTime QDateTime::fromString(QStringView string, QStringView format, QCalendar cal)`

**作用与语义：**

注意：该功能会超载`QDateTime::fromString()`。

### `[static, since 6.7] QDateTime QDateTime::fromString(QStringView string, QStringView format, int baseYear = QLocale::DefaultTwoDigitBaseYear)`

**作用与语义：**

使用默认构造的`QCalendar`。
注意：该功能会让`QDateTime::fromString()`重载。

### `[static, since 6.0] QDateTime QDateTime::fromString(const QString &string, QStringView format, QCalendar cal)`

**作用与语义：**

注意：该功能会超载`QDateTime::fromString()`。

### `[static, since 6.7] QDateTime QDateTime::fromString(const QString &string, QStringView format, int baseYear = QLocale::DefaultTwoDigitBaseYear)`

**作用与语义：**

使用默认构造的`QCalendar`。
注意：该功能会让`QDateTime::fromString()`重载。

### `[static] QDateTime QDateTime::fromString(const QString &string, const QString &format, QCalendar cal)`

**作用与语义：**

注意：该功能会超载`QDateTime::fromString()`。

### `[static, since 6.7] QDateTime QDateTime::fromString(const QString &string, const QString &format, int baseYear = QLocale::DefaultTwoDigitBaseYear)`

**作用与语义：**

使用默认构造的`QCalendar`。
注意：该功能会让`QDateTime::fromString()`重载。

### `[static, since 6.7] QDateTime QDateTime::fromString(QStringView string, QStringView format, int baseYear, QCalendar cal)`

**作用与语义：**

注意：该功能会超载`QDateTime::fromString()`。

### `[static, since 6.0] QDateTime QDateTime::fromString(const QString &string, QStringView format, int baseYear, QCalendar cal)`

**作用与语义：**

注意：该功能会超载`QDateTime::fromString()`。

### `bool QDateTime::isDaylightTime() const`

**作用与语义：**

如果该日期时间落在夏令时，则返回。
如果`Qt::TimeSpec`不是`Qt::LocalTime`或`Qt::TimeZone`，则总是返回假。

### `bool QDateTime::isNull() const`

**作用与语义：**

如果日期和时间均为空，返回`true`;否则返回`false`。空日期时间无效。

### `bool QDateTime::isValid() const`

**作用与语义：**

如果该日期时间代表确定的时刻，返回`true`，否则返回`false`。
如果日期时间的日期和时间都有效，且所用的时间表示法能为它们的组合赋予有效含义，则该日期时间有效。当时间表示是特定的时区或当地时间时，某些日期可能会跳过时间，例如夏令时切换时跳过一小时（通常是春季的夜晚）。例如，如果夏令时在凌晨2点结束，时钟快进到凌晨3点，那么当天02：00：00至02：59：59.99的日期时间无效。

### `qint64 QDateTime::msecsTo(const QDateTime &other) const`

**作用与语义：**

返回从该日期时间到`other`日期时间的毫秒数。如果`other`日期时间早于该日期时间，返回的值为负数。
在进行比较前，会将两个日期时间转换为`Qt::UTC`，以确保当夏令时（DST）适用于其中一个日期时间而另一个不适用时，结果是正确的。
如果任一日期时间无效，返回0。

### `int QDateTime::offsetFromUtc() const`

**作用与语义：**

在几秒内返回该日期时间的偏移量。
结果取决于`timeSpec()`：
- `Qt::UTC` 偏移量为0。
- `Qt::OffsetFromUTC` 偏移量是最初设定的值。
- `Qt::LocalTime` 返回当地时间与UTC的偏移。
- `Qt::TimeZone` 返回时区使用的偏移量。
后两种时间的差移将返回，考虑夏令时差。差移是当地时间或该时区时间与UTC时间的差;在UTC之前（本初子午线以东）的时区为正，UTC以西的时区为负。

### `qint64 QDateTime::secsTo(const QDateTime &other) const`

**作用与语义：**

返回从该日期时间到`other`日期时间的秒数。如果`other`日期时间早于该日期时间，返回的值为负数。
在进行比较前，会将两个日期时间转换为`Qt::UTC`，以确保如果夏令时（DST）适用于其中一个日期时间而另一个不适用，结果是正确的。
如果任一日期时间无效，返回0。

**官方示例：**

```cpp
 QDateTime now = QDateTime::currentDateTime();
 QDateTime xmas(QDate(now.date().year(), 12, 25).startOfDay());
 qDebug("There are %d seconds to Christmas", now.secsTo(xmas));
```

### `void QDateTime::setDate(QDate date, QDateTime::TransitionResolution resolve = TransitionResolution::LegacyBehavior)`

**作用与语义：**

将这个日期时间的日期部分设置为`date`。
如果还没有设定时间，则设置为午夜。如果`date`无效，这个`QDateTime`也无效。
如果`date`和`time()`描述了该日期时间表示中接近转换的时刻，`resolve`控制该情况的解决方式。
注意：在Qt 6.7之前，该函数版本缺少`resolve`参数，因此无法解决与转移相关的歧义。

### `void QDateTime::setMSecsSinceEpoch(qint64 msecs)`

**作用与语义：**

将日期时间设定为表示1970年UTC开始后某一毫秒的某一时刻，`msecs`毫秒。
在不支持时区的系统中，该功能表现得就像当地时间`Qt::UTC`。
注意，将最小值的`qint64`（`std::numeric_limits<qint64>::min()`）传递给`msecs`会导致行为不明确。

### `void QDateTime::setSecsSinceEpoch(qint64 secs)`

**作用与语义：**

将日期时间设定为表示1970年UTC开始后某秒数`secs`秒的某一刻。
在不支持时区的系统中，该函数表现得就像当地时间`Qt::UTC`。

### `void QDateTime::setTime(QTime time, QDateTime::TransitionResolution resolve = TransitionResolution::LegacyBehavior)`

**作用与语义：**

将datetime的时间部分设置为`time`。如果`time`不成立，该函数将其设置为午夜。因此，可以通过将`QDateTime`中任意时间设置为默认时间来清除`QTime`：
如果`date()`和`time`描述了该日期时间时间表示中接近过渡的时刻，`resolve`控制该情况的解决方式。
注意：在Qt 6.7之前，该函数版本缺少`resolve`参数，因此无法解决与转移相关的歧义。

**官方示例：**

```cpp
 QDateTime dt = QDateTime::currentDateTime();
 dt.setTime(QTime());
```

### `void QDateTime::setTimeZone(const QTimeZone &toZone, QDateTime::TransitionResolution resolve = TransitionResolution::LegacyBehavior)`

**作用与语义：**

将该日期时间中使用的时区设置为`toZone`。
datetime 可能指的是不同的时间点。它使用`toZone`的时间表示，这可能会改变其未变`date()`和`time()`的含义。
如果`toZone`无效，那么日期时间将无效。否则，通话后的该日期时间`timeSpec()`将与`toZone.timeSpec()`匹配。
如果`date()`和`time()`描述了接近`toZone`转变的时刻，`resolve`控制该情况的解决方式。
注意：在Qt 6.7之前，该函数版本缺少`resolve`参数，因此无法解决与转移相关的歧义。

### `[noexcept] void QDateTime::swap(QDateTime &other)`

**作用与语义：**

将这个日期时间与`other`交换。这个操作非常快，而且从未失败过。

### `QTime QDateTime::time() const`

**作用与语义：**

返回datetime的时间部分。

### `[since 6.5] QTimeZone QDateTime::timeRepresentation() const`

**作用与语义：**

返回一个`QTimeZone`，识别该日期时间如何代表时间。
返回`QTimeZone`的`timeSpec()`与该日期时间的日期时间一致;如果不`Qt::TimeZone`，则返回的`QTimeZone`是时间表示。当返回`timeSpec()`被`Qt::OffsetFromUTC`时，返回`QTimeZone`的固定SecondsAheadOfUtc()提供偏移量。当`timeSpec()` `Qt::TimeZone`时，`QTimeZone`对象本身就是该时区的完整表示。

### `Qt::TimeSpec QDateTime::timeSpec() const`

**作用与语义：**

返回日期时间的时间规格。
这将其时间表示归类为当地时间、UTC时间、UTC的固定偏移（不标明偏移）或时区（不提供该时区的详细信息）。相当于`timeRepresentation().timeSpec()`。

### `QTimeZone QDateTime::timeZone() const`

**作用与语义：**

返回日期时间的时区。
结果和`timeRepresentation().asBackendZone()`一样。在所有情况下，结果的 `timeSpec()` 都是`Qt::TimeZone`。
当`timeSpec()` `Qt::LocalTime`时，结果将描述该方法被调用时的本地时间。即使获得该方法的`QDateTime`发生了，结果也不会反映系统时区的后续变化。

### `QString QDateTime::timeZoneAbbreviation() const`

**作用与语义：**

返回该日期时间的时区缩写。
返回的字符串取决于`timeSpec()`：
- `Qt::UTC` 是“UTC”。
- 对于`Qt::OffsetFromUTC`，格式为“UTC±00：00”。
- 对于`Qt::LocalTime`，查询主机系统。
- 对于`Qt::TimeZone`，查询关联的`QTimeZone`对象。
注意：缩写不保证唯一，即不同时区可能使用相同的缩写。对于`Qt::LocalTime`和`Qt::TimeZone`，当主机系统返回缩写时，缩写可能会被本地化。

### `CFDateRef QDateTime::toCFDate() const`

**作用与语义：**

从`QDateTime`创建CFDate。
调用者拥有CFDate对象，并负责释放它。

### `QDateTime QDateTime::toLocalTime() const`

**作用与语义：**

返回该日期时间的副本，转换为当地时间。
结果代表与该日期时间相同的时刻，且等于。

**官方示例：**

```cpp
 QDateTime UTC(QDateTime::currentDateTimeUtc());
 QDateTime local(UTC.toLocalTime());
 qDebug() << "UTC time is:" << UTC;
 qDebug() << "Local time is:" << local;
 qDebug() << "No difference between times:" << UTC.secsTo(local);
```

### `qint64 QDateTime::toMSecsSinceEpoch() const`

**作用与语义：**

返回日期时间为1970年UTC开始后的毫秒数。
在不支持时区的系统中，该功能表现得就像当地时间`Qt::UTC`。
如果该对象存储的日期时间无效，该函数的行为是未定义的。然而，对于所有有效日期，该函数返回唯一的值。

### `NSDate *QDateTime::toNSDate() const`

**作用与语义：**

从`QDateTime`创建一个NSDate。
NSDate 对象是自动释放的。

### `QDateTime QDateTime::toOffsetFromUtc(int offsetSeconds) const`

**作用与语义：**

返回该日期时间的副本，转换为带有给定`offsetSeconds`的`Qt::OffsetFromUTC`规格。相当于`toTimeZone(QTimeZone::fromSecondsAheadOfUtc(offsetSeconds))`。
如果`offsetSeconds`为0，则返回UTC日期时间。
结果代表与该日期时间相同的时刻，且等于。

### `qint64 QDateTime::toSecsSinceEpoch() const`

**作用与语义：**

返回日期时间为1970年开始后的秒数（UTC）。
在不支持时区的系统中，该功能表现得就像当地时间`Qt::UTC`。
如果该对象存储的日期时间无效，该函数的行为是未定义的。然而，对于所有有效日期，该函数返回唯一的值。

### `[since 6.4] std::chrono::sys_time<std::chrono::milliseconds> QDateTime::toStdSysMilliseconds() const`

**作用与语义：**

将该日期时间对象转换为以毫秒表示的等效时间点，使用`std::chrono::system_clock`作为时钟。
注意：此函数需要C 20。

### `[since 6.4] std::chrono::sys_seconds QDateTime::toStdSysSeconds() const`

**作用与语义：**

将该日期时间对象转换为以秒表示的等效时间点，使用`std::chrono::system_clock`作为时钟。
注意：此函数需要C 20。

### `QString QDateTime::toString(QStringView format, QCalendar cal) const`

**作用与语义：**

返回日期时间的字符串。`format`参数决定结果字符串的格式。如果提供`cal`，则确定表示日期的历法;默认为公历。在Qt 5.14之前，没有`cal`参数，始终使用格里高利历。参见`QTime::toString()`和`QDate::toString()`，了解`format`参数中支持的时间和日期指定符。
任何用单引号包围的字符序列都会被逐字包含在输出字符串中（去掉引号），即使其中包含格式化字符。两个连续的单引号（“''”）在输出中被一个引号替换。格式字符串中的所有其他字符都逐字包含在输出字符串中。
支持无分隔符的格式（如“ddMM”），但必须谨慎使用，因为生成字符串并不总是可靠可读（例如，如果“dM”生成“212”，可能意味着12月2日或2月21日）。
示例格式字符串（假设`QDateTime`为2001年5月21日 14：13：09.120）：
- `Format`：结果
- `dd.MM.yyyy`：2001年5月21日
- `ddd MMMM d yy`：5月21日星期二 01
- `hh:mm:ss.zzz`：14：13：09.120
- `hh:mm:ss.z`：14：13：09.12
- `h:m:s ap`：下午2：13：9
如果 datetime 无效，则返回一个空字符串。
注意：日期和月份名称以及上午/下午指示均以英文（C locale）表示。要获取本地化的月份和日期名称及AM/PM的本地化形式，请使用`QLocale::system()`.toDateTime()。

### `QString QDateTime::toString(QStringView format) const`

**作用与语义：**

返回日期时间的字符串。`format`参数决定结果字符串的格式。如果提供`cal`，则确定表示日期的历法;默认为公历。在Qt 5.14之前，没有`cal`参数，始终使用格里高利历。参见`QTime::toString()`和`QDate::toString()`，了解`format`参数中支持的时间和日期指定符。
任何用单引号包围的字符序列都会被逐字包含在输出字符串中（去掉引号），即使其中包含格式化字符。两个连续的单引号（“''”）在输出中被一个引号替换。格式字符串中的所有其他字符都逐字包含在输出字符串中。
支持无分隔符的格式（如“ddMM”），但必须谨慎使用，因为生成字符串并不总是可靠可读（例如，如果“dM”生成“212”，可能意味着12月2日或2月21日）。
示例格式字符串（假设`QDateTime`为2001年5月21日 14：13：09.120）：
- `Format`：结果
- `dd.MM.yyyy`：2001年5月21日
- `ddd MMMM d yy`：5月21日星期二 01
- `hh:mm:ss.zzz`：14：13：09.120
- `hh:mm:ss.z`：14：13：09.12
- `h:m:s ap`：下午2：13：9
如果 datetime 无效，则返回一个空字符串。
注意：日期和月份名称以及上午/下午指示均以英文（C locale）表示。要获取本地化的月份和日期名称及AM/PM的本地化形式，请使用`QLocale::system()`.toDateTime()。

### `QString QDateTime::toString(Qt::DateFormat format = Qt::TextDate) const`

**作用与语义：**

注意：该功能会超载`QDateTime::toString()`。

### `QString QDateTime::toString(const QString &format) const`

**作用与语义：**

在给定的`format`中返回日期时间作为字符串。
如果`format`为`Qt::TextDate`，字符串格式为默认格式。日期和月份名称为英文。此格式示例为“Wed May 20 03：40：13 1998”。本地化格式请参见 `QLocale::toString()`。
如果`format` `Qt::ISODate`，字符串格式对应 ISO 8601 扩展的日期和时间表示规范，形式为 yyyy-MM-ddTHH：mm：ss[Z|±HH：mm]，具体取决于`QDateTime`的`timeSpec()`。如果`timeSpec()` `Qt::UTC`，则 Z 会附加在字符串上;如果`timeSpec()`是`Qt::OffsetFromUTC`，则从协调世界时（UTC）到小时和分钟的偏移会附加到字符串上。要在ISO 8601日期中包含毫秒，请使用`format` `Qt::ISODateWithMs`，对应于yyyy-MM-ddTHH：mm：ss.zzz[Z|±HH：mm]。
如果`format` `Qt::RFC2822Date`，字符串格式遵循RFC 2822。
如果 datetime 无效，则返回一个空字符串。
警告：`Qt::ISODate`格式仅适用于0至9999年间的年份。
注意：该功能会超载`QDateTime::toString()`。

### `QDateTime QDateTime::toTimeZone(const QTimeZone &timeZone) const`

**作用与语义：**

返回该日期时间的副本，转换为给定的`timeZone`。
结果代表与该日期时间相同的时刻，且等于。
结果用`timeZone`的时间表示来描述时间上的瞬间。例如：
如果`timeZone`无效，那么日期时间将无效。否则返回日期时间的`timeSpec()`将与`timeZone.timeSpec()`匹配。

**官方示例：**

```cpp
 QDateTime local(QDateTime::currentDateTime());
 QDateTime UTC(local.toTimeZone(QTimeZone::UTC));
 qDebug() << "Local time is:" << local;
 qDebug() << "UTC time is:" << UTC;
 qDebug() << "No difference between times represented:" << local.secsTo(UTC);
```

### `QDateTime QDateTime::toUTC() const`

**作用与语义：**

返回一份已转换为UTC的日期时间副本。
结果代表与该日期时间相同的时刻，且等于。

**官方示例：**

```cpp
 QDateTime local(QDateTime::currentDateTime());
 QDateTime UTC(local.toUTC());
 qDebug() << "Local time is:" << local;
 qDebug() << "UTC time is:" << UTC;
 qDebug() << "No difference between times:" << local.secsTo(UTC);
```

### `[since 6.4] QDateTime &QDateTime::operator+=(std::chrono::milliseconds duration)`

**作用与语义：**

通过添加给定的`duration`来修改该日期时间对象。如果`duration`为正，更新对象会更晚;如果是负，则更新更早。
如果该日期时间无效，该函数无效。
返回对该 datetime 对象的引用。

### `[since 6.4] QDateTime &QDateTime::operator-=(std::chrono::milliseconds duration)`

**作用与语义：**

通过减去给定的`duration`来修改该日期时间对象。如果`duration`为正，更新对象会更早;如果是负，则更新后。
如果该日期时间无效，该函数无效。
返回对该 datetime 对象的引用。

### `[noexcept] QDateTime &QDateTime::operator=(const QDateTime &other)`

**作用与语义：**

将`other`日期时间复制到这个副本中，并返回这份副本。

### `[noexcept] bool operator!=(const QDateTime &lhs, const QDateTime &rhs)`

**作用与语义：**

如果 `lhs` 与 `rhs` 不同，则返回 `true`；否则返回 `false`。
使用不同时间表示的两个日期时间可能与 UTC 的偏移不同。在这种情况下，即使它们的 `date()` 和 `time()` 不同，如果该差异与 UTC 偏移差匹配，它们仍可能比较相等。如果它们的 `date()` 和 `time()` 重合，那么 UTC 偏移较高的那个比偏移较低的那个更早。因此，日期时间只是弱顺序的。
自 5.14 版本起，所有无效日期时间都是相等的，并且小于所有有效日期时间。

### `[since 6.4] QDateTime operator+(std::chrono::milliseconds duration, const QDateTime &dateTime)`

**作用与语义：**

返回一个包含比`dateTime`晚`duration`毫秒的日期时间的`QDateTime`对象（如果`duration`为负则更早）。
如果`dateTime`无效，则会返回无效的日期时间。

### `[since 6.4] std::chrono::milliseconds operator-(const QDateTime &lhs, const QDateTime &rhs)`

**作用与语义：**

返回`lhs`到`rhs`之间的毫秒数。如果`lhs`早于`rhs`，结果为负。
如果任一日期时间无效，返回0。

### `[since 6.4] QDateTime operator-(const QDateTime &dateTime, std::chrono::milliseconds duration)`

**作用与语义：**

返回一个包含日期时间比`dateTime`早`duration`毫秒的`QDateTime`对象（如果`duration`为负则更晚）。
如果`dateTime`无效，则会返回一个无效的日期时间。

### `[noexcept] bool operator<(const QDateTime &lhs, const QDateTime &rhs)`

**作用与语义：**

如果 `lhs` 早于 `rhs`，则返回 `true`；否则返回 `false`。
使用不同时间表示的两个日期时间可能与 UTC 的偏移不同。在这种情况下，即使它们的 `date()` 和 `time()` 不同，只要这种差异与 UTC 偏移的差异匹配，它们也可能比较相等。如果它们的 `date()` 和 `time()` 重合，则 UTC 偏移较高的那个比偏移较低的那个更小（更早）。因此，日期时间只是弱顺序排列。
自 5.14 版本以来，所有无效的日期时间都是等价的，并且小于所有有效的日期时间。

### `QDataStream &operator<<(QDataStream &out, const QDateTime &dateTime)`

**作用与语义：**

写入`dateTime` `out`流。

### `[noexcept] bool operator<=(const QDateTime &lhs, const QDateTime &rhs)`

**作用与语义：**

如果 `lhs` 早于或等于 `rhs`，则返回 `true`；否则返回 `false`。 使用不同时间表示的两个日期时间可能与 UTC 有不同的偏移。在这种情况下，即使它们的 `date()` 和 `time()` 不同，只要这种差异与 UTC 偏移的差异相匹配，它们可能仍然被视为相等。如果它们的 `date()` 和 `time()` 重合，则 UTC 偏移较高的那个日期时间小（更早）于偏移较低的那个。因此，日期时间仅为弱顺序。 自 5.14 版本起，所有无效的日期时间都是相等的，并且小于所有有效日期时间。

### `[noexcept] bool operator==(const QDateTime &lhs, const QDateTime &rhs)`

**作用与语义：**

如果`lhs`表示与`rhs`相同的时刻，则返回`true`;否则返回`false`。
使用不同时间表示的两个日期时间可能与UTC的偏移不同。在这种情况下，即使`date()`和`time()`不同，只要差值与UTC偏移的差值相符，它们也可能比较等效时间。如果它们的`date()`和`time()`重合，那么与UTC偏移较大的日期时间比偏移较小的日期时间更早。因此，日期时间的顺序仅为弱序。
自5.14起，所有无效日期时间等价且小于所有有效日期时间。

### `[noexcept] bool operator>(const QDateTime &lhs, const QDateTime &rhs)`

**作用与语义：**

返回`true`如果`lhs`比……晚`rhs`; 否则返回 `false`使用不同时间表示的两个日期时间可能与 UTC 有不同的偏移量。在这种情况下，即使它们的`date()`和`time()`不同，如果这种差异与 UTC 偏移的差异相符。如果它们的`date()`和`time()`重合时，UTC 偏移量较高的时间点比偏移量较低的时间点要早（更小）。因此，日期时间只是弱顺序排列的。自 5.14 起，所有无效的日期时间都是等价的，并且小于所有有效的日期时间。

### `[noexcept] bool operator>=(const QDateTime &lhs, const QDateTime &rhs)`

**作用与语义：**

如果 `lhs` 晚于或等于 `rhs`，则返回 `true`；否则返回 `false`。 使用不同时间表示的两个日期时间可能与 UTC 有不同的偏移。在这种情况下，即使它们的 `date()` 和 `time()` 不同，只要这种差异与 UTC 偏移的差异相匹配，它们可能仍然被视为相等。如果它们的 `date()` 和 `time()` 重合，则 UTC 偏移较高的那个日期时间比偏移较低的那个日期时间更小（更早）。因此，日期时间只是弱排序的。 自 5.14 起，所有无效的日期时间都是相等的，并且小于所有有效日期时间。

### `QDataStream &operator>>(QDataStream &in, QDateTime &dateTime)`

**作用与语义：**

读取流`in`的日期时间到`dateTime`。

### `QString toString(const QString &format, QCalendar cal) const`

**作用与语义：**

注意：该功能会超载`QDateTime::toString()`。

### `(since 6.4) QDateTime operator+(const QDateTime &dateTime, std::chrono::milliseconds duration)`

**作用与语义：**

返回一个包含比`dateTime`晚`duration`毫秒的日期时间的`QDateTime`对象（如果`duration`为负则更早）。
如果`dateTime`无效，则会返回无效的日期时间。

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

`QDateTime` 所属机制类型：Qt 值类型与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
