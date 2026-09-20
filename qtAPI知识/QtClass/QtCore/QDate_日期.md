# Qt QDate 深入笔记

> 适用版本：Qt 6.11  
> 头文件：`#include <QDate>`  
> 所属模块：`Qt6::Core`  
> 相关类：`QTime`、`QDateTime`、`QTimeZone`、`QCalendar`、`QLocale`

## 1. 它表示“哪一天”，不表示“哪一刻”

`QDate` 是一个纯日期值：年、月、日对应的某个日历日。它不带时分秒、不带时区、不表示一个绝对时间点，也不依赖创建时的系统语言或时区。

因此它适合：

- 生日、节假日、合同到期日、账期结束日；
- 仅按自然日比较和计算的业务规则；
- 表单中只让用户选择日期的字段；
- 用 `QCalendar` 将同一个实际日期展示为不同历法的年月日。

它不适合直接表示“2026 年 9 月 9 日 09:00 北京时间”或网络协议中的时间戳。那些需要 `QDateTime` 加 `QTime` 与 `QTimeZone`，或直接用 UTC 时间点。

| 需求 | 更合适的类型 | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 某个自然日 | `QDate` | 只表达日期，不表达具体时刻 | 不能从它推导时区或 UTC 时间 |
| 一天中的时间 | `QTime` | 表达时、分、秒、毫秒 | 同样不含日期和时区 |
| 带时区的具体时刻 | `QDateTime` | 将日期、时间、时区组合成一个时刻表示 | DST 和无效本地时间需要显式处理 |
| 各种历法中的年月日 | `QDate` 加 `QCalendar` | 同一个实际日期按指定历法解释 | 不同历法的月数、闰月和年零规则不同 |

`QDate` 是一个很轻的值类型，内部用儒略日序号保存一个绝对日期。传递和返回时应直接按值传递，不需要为了“避免拷贝”而使用 `const QDate &`。

## 2. 最小可用代码：构造、校验和格式化

```cpp
#include <QDate>
#include <QDebug>

int main()
{
    const QDate deadline(2026, 9, 30);
    if (!deadline.isValid())
        return 1;

    qDebug().noquote() << deadline.toString(Qt::ISODate);
    qDebug() << deadline.addDays(7);
}
```

`QDate(2026, 9, 30)` 使用的是公历。`toString(Qt::ISODate)` 生成稳定的 `yyyy-MM-dd` 形式，适合日志、协议和配置文本；面向用户的显示通常应交给 `QLocale`，不要把英文月份名称或固定格式硬编码进界面。

## 3. 有效日期、无效日期和公历的年份边界

默认构造的 `QDate()` 是无效日期。构造函数、`setDate()` 或 `fromString()` 接收到不存在的日期时也会得到无效值，例如 `QDate(2026, 2, 29)`。

```cpp
const QDate leap(2024, 2, 29);
const QDate invalid(2026, 2, 29);

Q_ASSERT(leap.isValid());
Q_ASSERT(!invalid.isValid());
```

无效值不是异常，而是这个值类型表示“无法构造或解析日期”的正常结果。接收用户输入、解析文件或读取数据库文本时，要先检查 `isValid()`，再使用 `year()`、`addDays()` 或格式化结果。

### 3.1 公历没有 0 年

默认公历遵循历史上没有 year 0 的约定：

```cpp
QDate(1, 1, 1);     // 公元 1 年 1 月 1 日
QDate(-1, 12, 31);  // 公元前 1 年 12 月 31 日
QDate(0, 1, 1);     // 无效
```

不同 `QCalendar` 是否有 year 0 要看该历法自身规则。不要把 `QDate` 的负年份直接展示给用户；展示层应使用选定历法的格式化和本地化策略。

### 3.2 `isNull()` 与 `isValid()`

对 `QDate` 而言，`isNull()` 等价于“不是有效日期”。它不是像某些指针类型那样区分“空对象”和“错误对象”的额外状态。业务代码一般只需要写 `isValid()`，表达更直接。

## 4. 日期计算不是固定秒数计算

### 4.1 加天、加月、加年有不同语义

```cpp
const QDate jan31(2024, 1, 31);

const QDate byDays = jan31.addDays(31);
const QDate byMonths = jan31.addMonths(1);
```

`addDays()` 按连续自然日偏移；`addMonths()` 和 `addYears()` 按选定历法的月、年概念偏移。月末跨到短月份、闰日跨到平年时，结果会调整为目标月或目标年中可表示的日期，不应凭“30 天等于一个月”自行替代。

C++20 的 `std::chrono::days` 是固定天数，`addDuration(std::chrono::days)` 与 `addDays()` 语义对应。不要把 `std::chrono::months` 或 `std::chrono::years` 当作 `addMonths()`、`addYears()` 的替代：前者是 chrono 的时长模型，后者是日历运算。

### 4.2 计算相差天数

```cpp
const qint64 days = start.daysTo(end);
```

`daysTo()` 返回 `end - start` 的自然日差，`end` 更晚时为正，反之为负。它不涉及一天有 23 或 25 小时的夏令时问题，因为 `QDate` 还没有时区和时刻。

### 4.3 周序号遵循 ISO 8601

`weekNumber()` 按 ISO 8601 计算周数：周一是每周第一天，第 1 周是包含该年首个周四的那周。因此一月初可能属于上一 ISO 周年，十二月底也可能属于下一 ISO 周年。

```cpp
int isoYear = 0;
const int week = date.weekNumber(&isoYear);
```

需要存储“第几周”时必须同时存 `isoYear`；只存 `week` 会在跨年边界产生歧义。该函数固定按公历 ISO 周定义，不受传给其它函数的 `QCalendar` 影响。

## 5. 历法视图：同一天可有不同的年月日

一个 `QDate` 代表绝对的一天，`QCalendar` 决定如何把这一天解释成“第几年、第几月、第几日”。

```cpp
#include <QCalendar>

const QDate date(2026, 9, 9);
const QCalendar islamic(QCalendar::System::IslamicCivil);

const int year = date.year(islamic);
const int month = date.month(islamic);
const int day = date.day(islamic);
```

不带 `QCalendar` 参数的 `year()`、`month()`、`day()` 等成员使用公历。需要一次取多个部分时，比起连续调用三次成员函数，更适合调用 `QCalendar::partsFromDate()`，避免重复进行历法换算。

`dayOfWeek(QCalendar)` 在大多数历法中仍是 1 到 7，其中 1 为周一、7 为周日；有些历法存在特殊的插入日，可能返回大于 7 的值。不要假设它永远可直接转换为 `Qt::DayOfWeek`。

## 6. 字符串：机器交换、用户显示、解析输入必须分开

### 6.1 机器可读格式优先 ISO

```cpp
const QString saved = date.toString(Qt::ISODate); // 2026-09-09
const QDate loaded = QDate::fromString(saved, Qt::ISODate);
```

这是固定格式，不取决于当前用户语言，适合配置文件、数据库文本列、日志和网络传输。若协议需严格的日期格式，优先规定 ISO 8601 或完整的自定义格式，并在解析失败时拒绝数据。

### 6.2 自定义格式的大小写有语义

```cpp
const QDate parsed = QDate::fromString("2026/09/09", "yyyy/MM/dd");
```

常用字段：

- `yyyy`：四位年份；
- `yy`：两位年份；
- `MM`：两位月份，`M`：不补零月份；
- `dd`：两位日期，`d`：不补零日期；
- `MMM`、`MMMM`：英文月份简称或全称；
- `ddd`、`dddd`：英文星期简称或全称。

格式中要显示的字面量可放进单引号，例如 `"yyyy'年'M'月'd'日'"`。`QDate::toString()` 与 `fromString()` 的月份和星期名是英文形式；面向用户的本地化格式请使用 `QLocale::toString()` / `QLocale::toDate()`。

### 6.3 两位年份必须给出业务窗口

`fromString()` 解析 `yy` 时依赖 `baseYear` 决定候选世纪。Qt 6.7 起可以显式传入它；不要让金融、档案或长期数据依赖隐式默认窗口。

```cpp
const QDate date = QDate::fromString(
    "76-09-09", "yy-MM-dd", 1976);
```

以上选择从 1976 开始的 100 年窗口。更可靠的外部数据格式仍然是四位年份。

## 7. 从日期得到当天的开始或结束时刻

`startOfDay()` 和 `endOfDay()` 返回 `QDateTime`，这是 `QDate` 与时区真正发生交界的地方：

```cpp
#include <QTimeZone>

const QTimeZone zone("Asia/Shanghai");
const QDateTime start = date.startOfDay(zone);
const QDateTime end = date.endOfDay(zone);
```

无参数版本从 Qt 6.5 起，使用系统本地时区。带 `QTimeZone` 的版本更适合业务规则，因为“当天开始”和“当天结束”取决于所说的是哪个时区。夏令时切换可能使某地的一天不是 24 小时，少数时区规则甚至会使某个本地日期整体跳过；结果可能是无效 `QDateTime`，不能盲目假设一定存在 `00:00:00` 或 `23:59:59.999`。

旧版 `startOfDay(Qt::TimeSpec, int)` / `endOfDay(Qt::TimeSpec, int)` 已从 Qt 6.9 起弃用，应改用 `QTimeZone`。

## 8. 儒略日与 C++20 `chrono` 互操作

`toJulianDay()` 和 `fromJulianDay()` 提供稳定的整数形式，适合日期运算、跨历法换算或需要精确的日序号存储。Qt 所用儒略日以午夜为日界，与天文学的正午日界定义不同；不要自行把它当成 Unix 秒数。

Qt 6.4 起，在满足 C++20 chrono 支持的构建中，可以同 `std::chrono::sys_days` 相互转换：

```cpp
using namespace std::chrono;

const QDate qtDate = 2026y / September / 9;
const sys_days stdDate = qtDate.toStdSysDays();
const QDate roundTrip = QDate::fromStdSysDays(stdDate);
```

这些接口在不支持所需 chrono 功能的平台上不可用，例如 Qt 文档标注的 QNX INTEGRITY 限制。若项目需要跨多个 Qt 和编译器版本构建，应以功能检测和最低版本策略约束，而不是假设所有目标都存在这些重载。

## API 速查表
### 9.1 构造、有效性和基本字段

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QDate()` | 创建无效日期 | 解析或计算失败的结果也常是无效值，使用前检查 `isValid()` |
| 构造 | `QDate(int year, int month, int day)` | 按公历构造日期 | 公历没有 year 0；不存在的日历日得到无效值 |
| 构造 | `QDate(int year, int month, int day, QCalendar cal)` | 按指定历法的年月日构造绝对日期 | `cal` 的年零、月份和闰月规则与公历可不同 |
| chrono 构造 | `QDate(std::chrono::year_month_day)` | 从 C++20 年月日构造 | Qt 6.4 起且依赖 chrono 支持；无效 chrono 值产生无效日期 |
| chrono 构造 | `QDate(std::chrono::year_month_day_last)` | 从“某月最后一天”构造 | Qt 6.4 起；按公历 chrono 规则解释 |
| chrono 构造 | `QDate(std::chrono::year_month_weekday)` | 从“某月第几个星期几”构造 | Qt 6.4 起；确认索引星期几确实存在 |
| chrono 构造 | `QDate(std::chrono::year_month_weekday_last)` | 从“某月最后一个星期几”构造 | Qt 6.4 起；适合计算规则性节日 |
| 有效性 | `isValid() const` | 判断此对象是否代表可表示的日期 | 所有解析结果和外部输入都应先检查它 |
| 有效性 | `isNull() const` | 判断是否为空日期状态 | 对 `QDate` 等同于无效；通常写 `isValid()` 更清楚 |
| 有效性 | `isValid(int year, int month, int day)` | 检查一组公历年月日能否构成日期 | 仅检查公历；其它历法请用 `QCalendar` 的能力 |
| 年份 | `year() const` | 返回公历年份 | 无效日期返回 0；不要把 0 误认为真实公历年份 |
| 年份 | `year(QCalendar cal) const` | 返回指定历法的年份 | 需与同一个 `cal` 的月和日配套使用 |
| 月份 | `month() const` | 返回公历月份 | 无效日期返回 0 |
| 月份 | `month(QCalendar cal) const` | 返回指定历法的月份 | 非公历可能有不同月数或闰月编码 |
| 日期 | `day() const` | 返回公历月内日号 | 无效日期返回 0 |
| 日期 | `day(QCalendar cal) const` | 返回指定历法的月内日号 | 数值范围由历法决定 |
| 批量读取 | `getDate(int *year, int *month, int *day) const` | 一次取公历年月日 | 指针应有效；需要非公历数据用 `QCalendar::partsFromDate()` |

### 9.2 日历查询和日期运算

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 星期 | `dayOfWeek() const` | 返回公历星期，1 为周一、7 为周日 | 无效日期返回 0；不要把 0 当周日 |
| 星期 | `dayOfWeek(QCalendar cal) const` | 返回指定历法的星期信息 | 特殊插入日可能得到大于 7 的值 |
| 年内日 | `dayOfYear() const` | 返回公历年内第几天 | 无效日期返回 0；闰年 12 月 31 日是第 366 天 |
| 年内日 | `dayOfYear(QCalendar cal) const` | 返回指定历法年内第几天 | 结果依赖该历法年首和闰月规则 |
| 月天数 | `daysInMonth() const` | 返回公历当前月的天数 | 无效日期返回 0；二月天数依赖年份 |
| 月天数 | `daysInMonth(QCalendar cal) const` | 返回指定历法当前月的天数 | 不能用公历的 28 到 31 范围判断 |
| 年天数 | `daysInYear() const` | 返回公历当前年的天数 | 无效日期返回 0，结果通常为 365 或 366 |
| 年天数 | `daysInYear(QCalendar cal) const` | 返回指定历法当前年的天数 | 历法可能有不同闰年和月份体系 |
| 周数 | `weekNumber(int *yearNumber = nullptr) const` | 返回 ISO 8601 周数，并可写出 ISO 周年 | 固定采用公历 ISO 规则，跨年时务必取出 yearNumber |
| 加天 | `addDays(qint64 days) const` | 返回偏移指定自然日数后的日期 | 负数向过去；超范围或无效输入返回无效日期 |
| 加时长 | `addDuration(std::chrono::days days) const` | 按 C++20 固定天数偏移日期 | Qt 6.4 起；不要以 chrono 的月或年代替日历月年 |
| 加月 | `addMonths(int months) const` | 按公历偏移月份 | 月末跨短月会调整为目标月可表示日期 |
| 加月 | `addMonths(int months, QCalendar cal) const` | 按指定历法偏移月份 | 结果服从 `cal` 的月与闰月规则 |
| 加年 | `addYears(int years) const` | 按公历偏移年份 | 2 月 29 日跨到非闰年时会调整 |
| 加年 | `addYears(int years, QCalendar cal) const` | 按指定历法偏移年份 | 不同历法的年长度与年零规则不同 |
| 差值 | `daysTo(QDate other) const` | 返回从当前日期到 other 的自然日差 | other 更早时为负；不包含时区或 DST 时长 |
| 闰年 | `isLeapYear(int year)` | 判断公历年份是否为闰年 | 公历 year 0 不存在；其它历法请用 `QCalendar` |

### 9.3 当天时刻、字符串和儒略日

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 日初 | `startOfDay() const` | 返回系统本地时区中该日开始的 `QDateTime` | Qt 6.5 起；系统时区变化会影响结果 |
| 日初 | `startOfDay(const QTimeZone &zone) const` | 返回指定时区中该日开始的 `QDateTime` | DST 或整日跳过可能产生无效结果，需检查 |
| 日末 | `endOfDay() const` | 返回系统本地时区中该日结束的 `QDateTime` | Qt 6.5 起；不要假设总是 23:59:59.999 |
| 日末 | `endOfDay(const QTimeZone &zone) const` | 返回指定时区中该日结束的 `QDateTime` | 与业务时区保持一致，不要默认为机器本地时区 |
| 弃用日初 | `startOfDay(Qt::TimeSpec, int offsetSeconds = 0)` | 用旧时区规格得到日初时刻 | Qt 6.9 起弃用，改用 `QTimeZone` |
| 弃用日末 | `endOfDay(Qt::TimeSpec, int offsetSeconds = 0)` | 用旧时区规格得到日末时刻 | Qt 6.9 起弃用，改用 `QTimeZone` |
| 格式化 | `toString(Qt::DateFormat format = Qt::TextDate) const` | 以 Qt 预设格式输出字符串 | 存储和协议优先 `Qt::ISODate`，`TextDate` 不是本地化 UI 格式 |
| 格式化 | `toString(const QString &format) const` | 用 QString 格式串输出公历日期 | `M` 和 `m` 不可混淆；日期格式中 `M` 是月 |
| 格式化 | `toString(QStringView format) const` | 用非拥有格式视图输出公历日期 | Qt 6 的高效重载；调用期间 view 必须有效 |
| 格式化 | `toString(const QString &format, QCalendar cal) const` | 用 QString 格式串和指定历法输出 | 格式字段的范围服从 `cal`，不一定是公历范围 |
| 格式化 | `toString(QStringView format, QCalendar cal) const` | 用格式视图和指定历法输出 | 仅做格式化，不自动按用户 locale 翻译月份名 |
| 儒略日 | `toJulianDay() const` | 返回内部日期对应的儒略日序号 | 这是日序号，不是 Unix 时间戳；无效日期返回内部无效值 |
| 儒略日 | `fromJulianDay(qint64 jd)` | 从儒略日序号构造日期 | 超出 QDate 可表示范围时得到无效日期 |
| chrono | `toStdSysDays() const` | 转为 C++20 `std::chrono::sys_days` | Qt 6.4 起且依赖平台 chrono 支持；无效日期映射为 epoch 日 |
| chrono | `fromStdSysDays(const std::chrono::sys_days &days)` | 从 C++20 日精度系统时间构造日期 | Qt 6.4 起；超出可表示范围时得到无效日期 |

### 9.4 当前日期与 `fromString()` 重载

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 当前日期 | `currentDate()` | 读取系统本地时钟的今天日期 | 测试中应注入日期而不是依赖真实系统日期 |
| 解析 | `fromString(QStringView text, Qt::DateFormat format = Qt::TextDate)` | 按 Qt 预设格式解析视图文本 | Qt 6.0 起；失败返回无效日期 |
| 解析 | `fromString(const QString &text, Qt::DateFormat format = Qt::TextDate)` | 按 Qt 预设格式解析 QString | 对外部数据优先用 `Qt::ISODate` 或严格自定义格式 |
| 解析 | `fromString(QStringView text, QStringView format, QCalendar cal)` | 按格式视图和指定历法解析 | Qt 6.0 起；两位年份使用默认基准年 |
| 解析 | `fromString(const QString &text, QStringView format, QCalendar cal)` | 按 QString 和格式视图、指定历法解析 | Qt 6.0 起；解析不到完整有效日期即返回无效 |
| 解析 | `fromString(const QString &text, const QString &format, QCalendar cal)` | 按两个 QString 和指定历法解析 | 适合已有 QString 输入；业务格式仍应明确年位数 |
| 解析 | `fromString(QStringView text, QStringView format, int baseYear)` | 按格式解析，并指定两位年份窗口起点 | Qt 6.7 起；`yy` 数据必须由业务明确窗口 |
| 解析 | `fromString(const QString &text, QStringView format, int baseYear)` | 同上，文本为 QString | Qt 6.7 起；不要让默认 1900 窗口决定长期数据 |
| 解析 | `fromString(const QString &text, const QString &format, int baseYear)` | 同上，文本和格式均为 QString | Qt 6.7 起；检查返回值有效性 |
| 解析 | `fromString(QStringView text, QStringView format, int baseYear, QCalendar cal)` | 指定格式、两位年窗口和历法解析 | Qt 6.7 起；这是最完整的 view 版本 |
| 解析 | `fromString(const QString &text, QStringView format, int baseYear, QCalendar cal)` | 指定格式、两位年窗口和历法解析 | Qt 6.0 起；所有年月日含义均由 `cal` 决定 |
| 解析 | `fromString(const QString &text, const QString &format, int baseYear, QCalendar cal)` | 用 QString 指定全部解析条件 | 最完整 QString 版本；失败统一返回无效日期 |

### 9.5 修改和相关运算符

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 修改 | `setDate(int year, int month, int day)` | 将对象改为指定公历日期并返回是否成功 | 无效输入会令对象变为无效状态 |
| 修改 | `setDate(int year, int month, int day, QCalendar cal)` | 将对象改为指定历法日期并返回是否成功 | 调用后原日期会被替换，失败也要处理 |
| 自增 | `operator++(QDate &date)` | 将日期前置加一天并返回自身 | Qt 6.11 起；接近表示范围边界时检查结果有效性 |
| 自增 | `operator++(QDate &date, int)` | 将日期后置加一天并返回旧值 | Qt 6.11 起；后置形式会产生旧值副本 |
| 自减 | `operator--(QDate &date)` | 将日期前置减一天并返回自身 | Qt 6.11 起；语义等同 `addDays(-1)` 后赋回 |
| 自减 | `operator--(QDate &date, int)` | 将日期后置减一天并返回旧值 | Qt 6.11 起；不适合代替清晰的业务日期计算 |
| 比较 | `==`, `!=`, `<`, `<=`, `>`, `>=` | 比较两个日期的先后或相等性 | 无效日期也参与值比较；业务上先决定是否允许无效值 |
| 数据流 | `QDataStream << QDate` | 将日期写入 Qt 数据流 | 跨版本或跨系统持久化时设置数据流版本 |
| 数据流 | `QDataStream >> QDate` | 从 Qt 数据流读取日期 | 读取后检查流状态和日期有效性 |

## 10. 一个表单日期的稳妥处理方式

```cpp
QDate parseDeadline(const QString &text)
{
    const QDate date = QDate::fromString(text.trimmed(), Qt::ISODate);
    if (!date.isValid())
        return {};

    return date;
}

bool isOverdue(const QDate &deadline, const QDate &today)
{
    return deadline.isValid()
        && today.isValid()
        && deadline < today;
}
```

这个例子刻意将“输入解析失败”和“日期已经过期”分开：无效日期不是一个可以默认当作最早日期或最晚日期参与排序的业务值。需要时把校验错误返回给调用方，或改用 `std::optional<QDate>` 明确区分“字段缺失”和“字段存在但内容非法”。
