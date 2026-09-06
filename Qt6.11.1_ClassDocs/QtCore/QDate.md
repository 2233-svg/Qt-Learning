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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 72 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `[constexpr] QDate::QDate()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDate` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept, since 6.4] QDate::QDate(std::chrono::year_month_weekday_last date)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDate` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `date`：类型为 `std::chrono::year_month_weekday_last`。没有默认值，调用时必须提供。传入 `std::chrono::year_month_weekday_last` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDate::QDate(int y, int m, int d)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDate` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `y`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `m`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `d`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDate QDate::addDays(qint64 ndays) const`

**API 类别：** 成员函数说明

**中文解读：** `addDays(ndays)` 返回增加 `ndays` 天后的新 QDate，当前对象不变；负数表示向前移动。若结果超出 QDate 可表示范围则返回无效日期。

**签名拆解：**

- 返回值：`QDate`。
- 参数 `ndays`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.4] QDate QDate::addDuration(std::chrono::days ndays) const`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QDate` 添加依赖、数据或子对象的 API `addDuration`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QDate`。
- 参数 `ndays`：类型为 `std::chrono::days`。没有默认值，调用时必须提供。传入 `std::chrono::days` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDate QDate::addMonths(int nmonths, QCalendar cal) const`

**API 类别：** 成员函数说明

**中文解读：** `addMonths(nmonths)` 返回按日历月移动后的新日期，负数向前。目标月份没有原来的日号时会落到该月可用日期，月末业务必须验证结果。带 QCalendar 的重载按指定日历计算。

**签名拆解：**

- 返回值：`QDate`。
- 参数 `nmonths`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cal`：类型为 `QCalendar`。没有默认值，调用时必须提供。传入 `QCalendar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDate QDate::addMonths(int nmonths) const`

**API 类别：** 成员函数说明

**中文解读：** `addMonths(nmonths)` 返回按日历月移动后的新日期，负数向前。目标月份没有原来的日号时会落到该月可用日期，月末业务必须验证结果。带 QCalendar 的重载按指定日历计算。

**签名拆解：**

- 返回值：`QDate`。
- 参数 `nmonths`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDate QDate::addYears(int nyears, QCalendar cal) const`

**API 类别：** 成员函数说明

**中文解读：** `addYears(nyears)` 返回按日历年移动后的新日期，当前对象不变。闰日跨到非闰年时会调整到有效日期，生日/到期日规则应由业务确认。

**签名拆解：**

- 返回值：`QDate`。
- 参数 `nyears`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cal`：类型为 `QCalendar`。没有默认值，调用时必须提供。传入 `QCalendar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDate QDate::addYears(int nyears) const`

**API 类别：** 成员函数说明

**中文解读：** `addYears(nyears)` 返回按日历年移动后的新日期，当前对象不变。闰日跨到非闰年时会调整到有效日期，生日/到期日规则应由业务确认。

**签名拆解：**

- 返回值：`QDate`。
- 参数 `nyears`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QDate QDate::currentDate()`

**API 类别：** 成员函数说明

**中文解读：** `currentDate()` 读取系统当前本地日期。结果受系统时钟和时区影响；需要 UTC 时间点或可重复测试的业务逻辑时，不要把它散落在代码中。

**签名拆解：**

- 返回值：`QDate`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QDate::day(QCalendar cal) const`

**API 类别：** 成员函数说明

**中文解读：** `day()` 返回月内日号；其有效范围取决于年份、月份和日历，先检查日期有效性。

**签名拆解：**

- 返回值：`int`。
- 参数 `cal`：类型为 `QCalendar`。没有默认值，调用时必须提供。传入 `QCalendar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QDate::day() const`

**API 类别：** 成员函数说明

**中文解读：** `day()` 返回月内日号；其有效范围取决于年份、月份和日历，先检查日期有效性。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QDate::dayOfWeek(QCalendar cal) const`

**API 类别：** 成员函数说明

**中文解读：** `dayOfWeek()` 返回星期序号，Qt 约定 1 为星期一、7 为星期日；显示名称应交给 QLocale/toString 而不是手写数组。

**签名拆解：**

- 返回值：`int`。
- 参数 `cal`：类型为 `QCalendar`。没有默认值，调用时必须提供。传入 `QCalendar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QDate::dayOfWeek() const`

**API 类别：** 成员函数说明

**中文解读：** `dayOfWeek()` 返回星期序号，Qt 约定 1 为星期一、7 为星期日；显示名称应交给 QLocale/toString 而不是手写数组。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QDate::dayOfYear(QCalendar cal) const`

**API 类别：** 成员函数说明

**中文解读：** `dayOfYear()` 返回一年中的第几天，从 1 开始；闰年会影响最大值。

**签名拆解：**

- 返回值：`int`。
- 参数 `cal`：类型为 `QCalendar`。没有默认值，调用时必须提供。传入 `QCalendar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QDate::dayOfYear() const`

**API 类别：** 成员函数说明

**中文解读：** `dayOfYear()` 返回一年中的第几天，从 1 开始；闰年会影响最大值。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QDate::daysInMonth(QCalendar cal) const`

**API 类别：** 成员函数说明

**中文解读：** `daysInMonth()` 返回当前年月在指定日历中的天数，可用于限制日期输入；当前日期无效时先处理错误。

**签名拆解：**

- 返回值：`int`。
- 参数 `cal`：类型为 `QCalendar`。没有默认值，调用时必须提供。传入 `QCalendar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QDate::daysInMonth() const`

**API 类别：** 成员函数说明

**中文解读：** `daysInMonth()` 返回当前年月在指定日历中的天数，可用于限制日期输入；当前日期无效时先处理错误。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QDate::daysInYear(QCalendar cal) const`

**API 类别：** 成员函数说明

**中文解读：** `daysInYear()` 返回当前年份的天数，公历通常为 365 或 366；带 QCalendar 的重载按目标日历计算。

**签名拆解：**

- 返回值：`int`。
- 参数 `cal`：类型为 `QCalendar`。没有默认值，调用时必须提供。传入 `QCalendar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QDate::daysInYear() const`

**API 类别：** 成员函数说明

**中文解读：** `daysInYear()` 返回当前年份的天数，公历通常为 365 或 366；带 QCalendar 的重载按目标日历计算。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qint64 QDate::daysTo(QDate d) const`

**API 类别：** 成员函数说明

**中文解读：** `daysTo(other)` 计算从当前日期到 `other` 的有符号天数：other 在未来返回正数，在过去返回负数；任一日期无效时不要使用结果。

**签名拆解：**

- 返回值：`qint64`。
- 参数 `d`：类型为 `QDate`。没有默认值，调用时必须提供。传入 `QDate` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDateTime QDate::endOfDay(const QTimeZone &zone) const`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `endOfDay`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数 `zone`：类型为 `const QTimeZone &`。没有默认值，调用时必须提供。传入 `const QTimeZone &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.5] QDateTime QDate::endOfDay() const`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `endOfDay`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static constexpr] QDate QDate::fromJulianDay(qint64 jd)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromJulianDay`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QDate`。
- 参数 `jd`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static constexpr noexcept, since 6.4] QDate QDate::fromStdSysDays(const std::chrono::sys_days &days)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromStdSysDays`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QDate`。
- 参数 `days`：类型为 `const std::chrono::sys_days &`。没有默认值，调用时必须提供。传入 `const std::chrono::sys_days &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QDate QDate::fromString(const QString &string, const QString &format, int baseYear, QCalendar cal)`

**API 类别：** 成员函数说明

**中文解读：** `fromString()` 按指定格式解析文本并返回 QDate。解析失败返回无效日期；格式串、locale 和输入必须一致，不能只根据返回对象存在就认为成功。

**签名拆解：**

- 返回值：`QDate`。
- 参数 `string`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `format`：类型为 `const QString &`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `baseYear`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cal`：类型为 `QCalendar`。没有默认值，调用时必须提供。传入 `QCalendar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.0] QDate QDate::fromString(QStringView string, Qt::DateFormat format = Qt::TextDate)`

**API 类别：** 成员函数说明

**中文解读：** `fromString()` 按指定格式解析文本并返回 QDate。解析失败返回无效日期；格式串、locale 和输入必须一致，不能只根据返回对象存在就认为成功。

**签名拆解：**

- 返回值：`QDate`。
- 参数 `string`：类型为 `QStringView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `format`：类型为 `Qt::DateFormat`。默认值为 `Qt::TextDate`。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QDate QDate::fromString(const QString &string, Qt::DateFormat format = Qt::TextDate)`

**API 类别：** 成员函数说明

**中文解读：** `fromString()` 按指定格式解析文本并返回 QDate。解析失败返回无效日期；格式串、locale 和输入必须一致，不能只根据返回对象存在就认为成功。

**签名拆解：**

- 返回值：`QDate`。
- 参数 `string`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `format`：类型为 `Qt::DateFormat`。默认值为 `Qt::TextDate`。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.0] QDate QDate::fromString(QStringView string, QStringView format, QCalendar cal)`

**API 类别：** 成员函数说明

**中文解读：** `fromString()` 按指定格式解析文本并返回 QDate。解析失败返回无效日期；格式串、locale 和输入必须一致，不能只根据返回对象存在就认为成功。

**签名拆解：**

- 返回值：`QDate`。
- 参数 `string`：类型为 `QStringView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `format`：类型为 `QStringView`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `cal`：类型为 `QCalendar`。没有默认值，调用时必须提供。传入 `QCalendar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.7] QDate QDate::fromString(QStringView string, QStringView format, int baseYear = QLocale::DefaultTwoDigitBaseYear)`

**API 类别：** 成员函数说明

**中文解读：** `fromString()` 按指定格式解析文本并返回 QDate。解析失败返回无效日期；格式串、locale 和输入必须一致，不能只根据返回对象存在就认为成功。

**签名拆解：**

- 返回值：`QDate`。
- 参数 `string`：类型为 `QStringView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `format`：类型为 `QStringView`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `baseYear`：类型为 `int`。默认值为 `QLocale::DefaultTwoDigitBaseYear`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.0] QDate QDate::fromString(const QString &string, QStringView format, QCalendar cal)`

**API 类别：** 成员函数说明

**中文解读：** `fromString()` 按指定格式解析文本并返回 QDate。解析失败返回无效日期；格式串、locale 和输入必须一致，不能只根据返回对象存在就认为成功。

**签名拆解：**

- 返回值：`QDate`。
- 参数 `string`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `format`：类型为 `QStringView`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `cal`：类型为 `QCalendar`。没有默认值，调用时必须提供。传入 `QCalendar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.7] QDate QDate::fromString(const QString &string, QStringView format, int baseYear = QLocale::DefaultTwoDigitBaseYear)`

**API 类别：** 成员函数说明

**中文解读：** `fromString()` 按指定格式解析文本并返回 QDate。解析失败返回无效日期；格式串、locale 和输入必须一致，不能只根据返回对象存在就认为成功。

**签名拆解：**

- 返回值：`QDate`。
- 参数 `string`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `format`：类型为 `QStringView`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `baseYear`：类型为 `int`。默认值为 `QLocale::DefaultTwoDigitBaseYear`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QDate QDate::fromString(const QString &string, const QString &format, QCalendar cal)`

**API 类别：** 成员函数说明

**中文解读：** `fromString()` 按指定格式解析文本并返回 QDate。解析失败返回无效日期；格式串、locale 和输入必须一致，不能只根据返回对象存在就认为成功。

**签名拆解：**

- 返回值：`QDate`。
- 参数 `string`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `format`：类型为 `const QString &`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `cal`：类型为 `QCalendar`。没有默认值，调用时必须提供。传入 `QCalendar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.7] QDate QDate::fromString(const QString &string, const QString &format, int baseYear = QLocale::DefaultTwoDigitBaseYear)`

**API 类别：** 成员函数说明

**中文解读：** `fromString()` 按指定格式解析文本并返回 QDate。解析失败返回无效日期；格式串、locale 和输入必须一致，不能只根据返回对象存在就认为成功。

**签名拆解：**

- 返回值：`QDate`。
- 参数 `string`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `format`：类型为 `const QString &`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `baseYear`：类型为 `int`。默认值为 `QLocale::DefaultTwoDigitBaseYear`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.7] QDate QDate::fromString(QStringView string, QStringView format, int baseYear, QCalendar cal)`

**API 类别：** 成员函数说明

**中文解读：** `fromString()` 按指定格式解析文本并返回 QDate。解析失败返回无效日期；格式串、locale 和输入必须一致，不能只根据返回对象存在就认为成功。

**签名拆解：**

- 返回值：`QDate`。
- 参数 `string`：类型为 `QStringView`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `format`：类型为 `QStringView`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `baseYear`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cal`：类型为 `QCalendar`。没有默认值，调用时必须提供。传入 `QCalendar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.0] QDate QDate::fromString(const QString &string, QStringView format, int baseYear, QCalendar cal)`

**API 类别：** 成员函数说明

**中文解读：** `fromString()` 按指定格式解析文本并返回 QDate。解析失败返回无效日期；格式串、locale 和输入必须一致，不能只根据返回对象存在就认为成功。

**签名拆解：**

- 返回值：`QDate`。
- 参数 `string`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `format`：类型为 `QStringView`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `baseYear`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cal`：类型为 `QCalendar`。没有默认值，调用时必须提供。传入 `QCalendar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QDate::getDate(int *year, int *month, int *day) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QDate` 的核心操作 `getDate`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `year`：类型为 `int *`。没有默认值，调用时必须提供。传入 `int *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `month`：类型为 `int *`。没有默认值，调用时必须提供。传入 `int *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `day`：类型为 `int *`。没有默认值，调用时必须提供。传入 `int *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] bool QDate::isLeapYear(int year)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `isLeapYear`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数 `year`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr] bool QDate::isNull() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isNull`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr] bool QDate::isValid() const`

**API 类别：** 成员函数说明

**中文解读：** `isValid()` 判断当前对象是否代表真实存在的日期。默认构造、越界年月日或解析失败会得到无效日期；调用 year/month/day、运算或格式化前应先检查它。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] bool QDate::isValid(int year, int month, int day)`

**API 类别：** 成员函数说明

**中文解读：** `isValid()` 判断当前对象是否代表真实存在的日期。默认构造、越界年月日或解析失败会得到无效日期；调用 year/month/day、运算或格式化前应先检查它。

**签名拆解：**

- 返回值：`bool`。
- 参数 `year`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `month`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `day`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QDate::month(QCalendar cal) const`

**API 类别：** 成员函数说明

**中文解读：** `month()` 返回 1 到 12 的月份；先用 isValid() 排除无效日期，带 QCalendar 的重载遵守目标日历。

**签名拆解：**

- 返回值：`int`。
- 参数 `cal`：类型为 `QCalendar`。没有默认值，调用时必须提供。传入 `QCalendar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QDate::month() const`

**API 类别：** 成员函数说明

**中文解读：** `month()` 返回 1 到 12 的月份；先用 isValid() 排除无效日期，带 QCalendar 的重载遵守目标日历。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QDate::setDate(int year, int month, int day)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setDate`。调用它会改变 `QDate` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`bool`。
- 参数 `year`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `month`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `day`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QDate::setDate(int year, int month, int day, QCalendar cal)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setDate`。调用它会改变 `QDate` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`bool`。
- 参数 `year`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `month`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `day`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `cal`：类型为 `QCalendar`。没有默认值，调用时必须提供。传入 `QCalendar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDateTime QDate::startOfDay(const QTimeZone &zone) const`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `startOfDay`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数 `zone`：类型为 `const QTimeZone &`。没有默认值，调用时必须提供。传入 `const QTimeZone &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.5] QDateTime QDate::startOfDay() const`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `startOfDay`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QDateTime`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr] qint64 QDate::toJulianDay() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toJulianDay`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`qint64`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] std::chrono::sys_days QDate::toStdSysDays() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toStdSysDays`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`std::chrono::sys_days`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QDate::toString(QStringView format, QCalendar cal) const`

**API 类别：** 成员函数说明

**中文解读：** `toString()` 把有效日期格式化为文本。Qt::DateFormat 重载适合标准格式，自定义格式要区分 `M/MM/MMM` 与 `d/dd/ddd`；本地化显示应配合 QLocale。

**签名拆解：**

- 返回值：`QString`。
- 参数 `format`：类型为 `QStringView`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `cal`：类型为 `QCalendar`。没有默认值，调用时必须提供。传入 `QCalendar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QDate::toString(QStringView format) const`

**API 类别：** 成员函数说明

**中文解读：** `toString()` 把有效日期格式化为文本。Qt::DateFormat 重载适合标准格式，自定义格式要区分 `M/MM/MMM` 与 `d/dd/ddd`；本地化显示应配合 QLocale。

**签名拆解：**

- 返回值：`QString`。
- 参数 `format`：类型为 `QStringView`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QDate::toString(Qt::DateFormat format = Qt::TextDate) const`

**API 类别：** 成员函数说明

**中文解读：** `toString()` 把有效日期格式化为文本。Qt::DateFormat 重载适合标准格式，自定义格式要区分 `M/MM/MMM` 与 `d/dd/ddd`；本地化显示应配合 QLocale。

**签名拆解：**

- 返回值：`QString`。
- 参数 `format`：类型为 `Qt::DateFormat`。默认值为 `Qt::TextDate`。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QDate::toString(const QString &format) const`

**API 类别：** 成员函数说明

**中文解读：** `toString()` 把有效日期格式化为文本。Qt::DateFormat 重载适合标准格式，自定义格式要区分 `M/MM/MMM` 与 `d/dd/ddd`；本地化显示应配合 QLocale。

**签名拆解：**

- 返回值：`QString`。
- 参数 `format`：类型为 `const QString &`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QDate::weekNumber(int *yearNumber = nullptr) const`

**API 类别：** 成员函数说明

**中文解读：** `QDate::weekNumber` 用于计算、查询或取得与“week、Number”相关的操作。调用时要先确认当前状态和 `yearNumber` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `yearNumber`：类型为 `int *`。默认值为 `nullptr`。传入 `int *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QDate::year(QCalendar cal) const`

**API 类别：** 成员函数说明

**中文解读：** `year()` 返回年份；无效日期的结果不能作为业务年份使用。带 QCalendar 的重载按指定日历解释。

**签名拆解：**

- 返回值：`int`。
- 参数 `cal`：类型为 `QCalendar`。没有默认值，调用时必须提供。传入 `QCalendar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QDate::year() const`

**API 类别：** 成员函数说明

**中文解读：** `year()` 返回年份；无效日期的结果不能作为业务年份使用。带 QCalendar 的重载按指定日历解释。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] bool operator!=(const QDate &lhs, const QDate &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDate` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QDate &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QDate &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.11] QDate &operator++(QDate &date)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDate` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDate &`。
- 参数 `date`：类型为 `QDate &`。没有默认值，调用时必须提供。传入 `QDate &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.11] QDate operator++(QDate &date, int)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDate` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDate`。
- 参数 `date`：类型为 `QDate &`。没有默认值，调用时必须提供。传入 `QDate &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `int`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.11] QDate &operator--(QDate &date)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDate` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDate &`。
- 参数 `date`：类型为 `QDate &`。没有默认值，调用时必须提供。传入 `QDate &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.11] QDate operator--(QDate &date, int)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDate` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDate`。
- 参数 `date`：类型为 `QDate &`。没有默认值，调用时必须提供。传入 `QDate &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `int`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] bool operator<(const QDate &lhs, const QDate &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDate` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QDate &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QDate &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDataStream &operator<<(QDataStream &out, QDate date)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDate` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDataStream &`。
- 参数 `out`：类型为 `QDataStream &`。没有默认值，调用时必须提供。传入 `QDataStream &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `date`：类型为 `QDate`。没有默认值，调用时必须提供。传入 `QDate` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] bool operator<=(const QDate &lhs, const QDate &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDate` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QDate &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QDate &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] bool operator==(const QDate &lhs, const QDate &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDate` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QDate &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QDate &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] bool operator>(const QDate &lhs, const QDate &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDate` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QDate &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QDate &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] bool operator>=(const QDate &lhs, const QDate &rhs)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDate` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `lhs`：类型为 `const QDate &`。没有默认值，调用时必须提供。运算符左侧的值；要注意返回新值还是修改当前对象。
- 参数 `rhs`：类型为 `const QDate &`。没有默认值，调用时必须提供。运算符右侧的另一个值；通常不会被当前 API 接管所有权。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDataStream &operator>>(QDataStream &in, QDate &date)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QDate` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDataStream &`。
- 参数 `in`：类型为 `QDataStream &`。没有默认值，调用时必须提供。传入 `QDataStream &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `date`：类型为 `QDate &`。没有默认值，调用时必须提供。传入 `QDate &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.4) QDate(std::chrono::year_month_day date)`

**API 类别：** 公有函数

**中文解读：** 这是 `QDate` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `date`：类型为 `std::chrono::year_month_day`。没有默认值，调用时必须提供。传入 `std::chrono::year_month_day` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.4) QDate(std::chrono::year_month_day_last date)`

**API 类别：** 公有函数

**中文解读：** 这是 `QDate` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `date`：类型为 `std::chrono::year_month_day_last`。没有默认值，调用时必须提供。传入 `std::chrono::year_month_day_last` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.4) QDate(std::chrono::year_month_weekday date)`

**API 类别：** 公有函数

**中文解读：** 这是 `QDate` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `date`：类型为 `std::chrono::year_month_weekday`。没有默认值，调用时必须提供。传入 `std::chrono::year_month_weekday` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString toString(const QString &format, QCalendar cal) const`

**API 类别：** 公有函数

**中文解读：** `toString()` 把有效日期格式化为文本。Qt::DateFormat 重载适合标准格式，自定义格式要区分 `M/MM/MMM` 与 `d/dd/ddd`；本地化显示应配合 QLocale。

**签名拆解：**

- 返回值：`QString`。
- 参数 `format`：类型为 `const QString &`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `cal`：类型为 `QCalendar`。没有默认值，调用时必须提供。传入 `QCalendar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

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
