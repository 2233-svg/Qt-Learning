# Qt QCalendar 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QCalendar>`  
> 所属模块：`Qt6::Core`  
> 类型：不可变、可按值复制的历法规则对象  
> 核心定位：在某一种历法的年月日字段与 `QDate` 表示的具体日期之间转换

## 1. 它解决的不是“存日期”，而是“解释日期”

`QDate` 表示一个确定的日子；`QCalendar` 则规定“把这一天叫作哪一年、哪一月、哪一日”。同一个实际日期，用公历、儒略历或波斯历解释，得到的年月日字段可以不同。

```text
一个确定的日子
      QDate
        ^
        | dateFromParts() / partsFromDate()
        v
某种历法中的 年、月、日
QCalendar::YearMonthDay
```

因此，`QCalendar` 解决的是多历法输入、显示与校验：

- 用户输入的“某历法 1405 年 1 月 1 日”要转换成程序内部可比较的日期。
- 同一个 `QDate` 需要按用户选定的历法显示。
- 不能把“每年 12 个月、每月最多 31 天、有公元 0 年”写死在业务代码中。

它不负责时区和时刻。带时间点的问题用 `QDateTime` 配合 `QTimeZone`；`QCalendar` 只解释其中的日期部分。

## 2. 三个类型各司其职

| 类型 | 保存什么 | 典型职责 | 不负责什么 |
| --- | --- | --- | --- |
| `QDate` | 一个确定的日子 | 比较、加减天数、数据库或业务层传递 | 用户选择的历法显示规则 |
| `QCalendar` | 一套历法规则 | 年月日与 `QDate` 的双向转换 | 存储某一次具体日期 |
| `QLocale` | 语言与地区格式 | 决定月份和星期名称的语言、长短格式 | 改变历法的月数、闰年规则 |
| `QDateTime` | 日期加时间和时区语义 | 表示时刻、时区转换 | 定义某个历法的一年有几个月 |

最实用的分层是：业务逻辑和持久化保存 `QDate`，界面层保留用户选定的 `QCalendar` 与 `QLocale`，显示或输入时才转换。

## 3. 最小可用示例

默认构造得到的是前推公历（proleptic Gregorian calendar）。所谓“前推”是指 Qt 将这套规则扩展到历史年份，但它**没有 0 年**：年份 `1` 前面是 `-1`。

```cpp
#include <QCalendar>
#include <QDate>
#include <QLocale>
#include <QDebug>

int main()
{
    QCalendar calendar; // 默认：Gregorian

    const QDate date = calendar.dateFromParts(2026, 9, 9);
    if (!date.isValid()) {
        return 1;
    }

    const QCalendar::YearMonthDay parts = calendar.partsFromDate(date);
    qDebug() << parts.year << parts.month << parts.day;

    const QString month = calendar.monthName(
        QLocale(QLocale::Chinese, QLocale::China),
        parts.month, parts.year, QLocale::LongFormat);
    qDebug() << month;
}
```

`dateFromParts()` 和 `partsFromDate()` 是一对互补 API：前者把某套规则下的字段变成可处理的 `QDate`，后者用同一套规则读取 `QDate` 的字段。不要把 `QDate::year()` 当作任意历法的年份；它读取的是 Qt 默认公历解释。

## 4. `YearMonthDay`：字段包，不是完整日期对象

`QCalendar::YearMonthDay` 是包含 `year`、`month`、`day` 三个 `int` 的轻量结构，便于将转换结果作为一个值传递。

```cpp
QCalendar calendar;
QCalendar::YearMonthDay parts { 2026, 9, 9 };

if (calendar.isDateValid(parts.year, parts.month, parts.day)) {
    const QDate date = calendar.dateFromParts(parts);
    useDate(date);
}
```

它自身的 `isValid()` 只检查 `month` 与 `day` 是否不是 `QCalendar::Unspecified`；这不是“该年月日一定在当前历法中存在”的完整校验。真正处理用户输入前，调用 `calendar.isDateValid(year, month, day)`。

`Unspecified` 是 Qt 的特殊 `int` 值，用来表示“没有提供年份或字段”。有些查询刻意支持它，例如 `daysInMonth(month)` 会返回该月在任意年份中可能的最大天数；但把它传给 `dateFromParts()` 会得到空的 `QDate`，传给 `daysInYear()` 的行为则未定义。

## 5. 选择历法：枚举、名称和自定义后端

### 5.1 `System` 枚举

`QCalendar::System` 是 Qt 内建历法的选择器。部分历法取决于 Qt 编译时启用的功能，因此不能假定每个部署版本都提供同样集合；对可选历法，优先用 `availableCalendars()` 检查。

| 常量 | 数值 | 表示什么 | 使用时注意 |
| --- | --- | --- | --- |
| `Gregorian` | `0` | 国际通用的默认公历。 | 默认构造就是它；Qt 的许多日期 API 也以它为默认解释。 |
| `Julian` | `8` | 古罗马儒略历。 | 适合需要历史历法显示或转换的场景。 |
| `Milankovic` | `9` | 修订儒略历。 | 常见于部分东正教会使用的历法语境。 |
| `Jalali` | `10` | 太阳历，也称波斯历。 | 是否可用受 Qt 的 `jalalicalendar` 功能配置影响。 |
| `IslamicCivil` | `11` | 表格化伊斯兰民用历。 | 它是可计算的民用历，不应与实际观测月相的宗教历混为一谈。 |

```cpp
QCalendar persian(QCalendar::System::Jalali);
if (!persian.isValid()) {
    // 运行环境没有相应后端时，选择回退策略。
}
```

### 5.2 按名称与 `SystemId` 构造

按 `QAnyStringView` 名称构造可接入插件或应用自行注册的历法。名称构造有一个容易遗漏的前提：某个自定义后端可能要先被实例化，才会注册到可按名称查找的列表中。Qt 6.4 之前此构造函数只接受 `QStringView` 和 `QLatin1StringView`，Qt 6.4 起改为 `QAnyStringView`。

`SystemId` 构造函数从 Qt 6.2 提供，主要服务于自定义后端未按名称注册的场景。它是后端的唯一标识，不应把 `index()` 的数值当作跨版本、跨进程或可持久化协议。

## 6. 转换与校验：先校验字段，再得到 `QDate`

### 6.1 从历法字段到具体日期

```cpp
QCalendar calendar(QCalendar::System::Gregorian);

if (!calendar.isDateValid(2026, 2, 29)) {
    qDebug() << "该历法中不存在这个年月日";
}

const QDate leapDay = calendar.dateFromParts(2024, 2, 29);
Q_ASSERT(leapDay.isValid());
```

`dateFromParts()` 对无效月份、无效日期或任何字段为 `Unspecified` 的输入，返回 `isNull()` 为 `true` 的 `QDate`。这使它可以直接用作“尝试转换”，但处理用户输入时仍建议先用 `isDateValid()` 给出更明确的校验分支。

### 6.2 从具体日期读出某历法字段

```cpp
const QDate storedDate(2026, 9, 9);
const auto parts = calendar.partsFromDate(storedDate);

if (!parts.isValid()) {
    // 当前历法无法表示这个 QDate。
    return;
}

renderYearMonthDay(parts.year, parts.month, parts.day);
```

如果该历法无法表示传入的 `QDate`，`partsFromDate()` 返回的结构 `isValid()` 为 `false`。因此多历法日历控件不要只读取字段，必须先检查转换结果。

### 6.3 处理两位年份和星期的歧义

`matchCenturyToWeekday(parts, dow)` 从 Qt 6.7 提供。它用于“年份只给出了末两位、又知道星期几”的解析情形：Qt 尝试找到与这些条件相符的世纪并返回 `QDate`。条件无法同时满足时返回无效日期。

这是格式解析的辅助工具，不是普通日期构造 API。若用户输入的是完整四位年份，直接使用 `dateFromParts()` 更清楚。

## 7. 历法属性与范围：不要假设公历常识

不同历法可能有闰月、不同的年长度、年零或可表示范围差异。下面这些 API 是“写通用日历 UI 或验证器”时的依据。

- `monthsInYear(year)`：该年真正有多少个月；年份为 `Unspecified` 时返回最大可能月数。
- `daysInMonth(month, year)`：该月在指定年份中的天数；省略年份时，返回该月在任何年份中可能的最大长度。
- `maximumDaysInMonth()`、`minimumDaysInMonth()`、`maximumMonthsInYear()`：全局边界，适合预分配或选择器的上限。
- `isLeapYear(year)`：只问该历法意义上的闰年，不能用 `% 4` 自己推。
- `isSolar()`、`isLunar()`、`isLuniSolar()`：描述历法类型；它们不能替代真实月份和日期校验。
- `isProleptic()` 与 `hasYearZero()`：处理历史年份时的关键约束。

特别注意：`isProleptic()` 为 `true` 仅表示这套规则能向最早年份之前延展；不代表存在 0 年。默认前推公历便是“前推但没有 0 年”的典型例子。

## 8. 本地化名称：名称的语法位置很重要

`monthName()` 与 `standaloneMonthName()` 的区别不在“内容长短”，而在词形使用位置：

- `monthName()` 返回适合完整日期中的月名。
- `standaloneMonthName()` 返回适合单独作为标题或下拉项的月名。
- `weekDayName()` 返回适合完整日期中的星期名。
- `standaloneWeekDayName()` 返回适合日历表头的星期名。

不少语言会因语法格、大小写或词形变化而产生不同结果；中文里两者可能看起来相同，但跨语言 UI 不应偷懒地只用其中一个。

```cpp
const QLocale locale(QLocale::Russian, QLocale::Russia);
const QString inDate = calendar.monthName(
    locale, 3, 2026, QLocale::LongFormat);
const QString heading = calendar.standaloneMonthName(
    locale, 3, 2026, QLocale::LongFormat);
```

当历法存在位置不固定的闰月时，月序号对应的名称可能依赖年份。已知年份时应始终传入 `year`；月号或星期号无法识别时，这些名称 API 返回空字符串。

## 9. 格式化、线程与生命周期

`QCalendar` 是不可变值类型，可按值保存、复制与传参；它没有 `QObject` 父子关系，也不依赖事件循环。日历规则本身不会随着 `QLocale` 改变，语言、地区和长短格式要通过名称 API 或格式化 API 显式传入 `QLocale`。

`dateTimeToString()` 是 `QDate`、`QTime`、`QDateTime` 的格式化底层辅助接口。通常业务代码优先使用 `QDate::toString()`、`QDateTime::toString()` 或 `QLocale` 的高层 API；只有自定义历法格式化流程时，才需要直接调用它。它会优先格式化有效的 `datetime`，其次是 `dateOnly`，再其次是 `timeOnly`，三者都无效则返回空字符串。

## 10. 常见误区

### 10.1 以为 `QDate` 的 `year()` 会跟随当前历法

不会。`QDate` 保存的是确定的日子，`QDate::year()` 使用默认公历解释。要取得用户选择历法的年份，调用 `calendar.partsFromDate(date).year`。

### 10.2 只限制月份 1 到 12

并非所有历法每年恰有 12 个月。日期选择器应基于 `monthsInYear(year)` 和 `daysInMonth(month, year)` 构建选项，而不是硬编码公历范围。

### 10.3 把负年份当作有 0 年

默认前推公历没有 0 年：`1` 前面是 `-1`。跨越纪元的计算和输入校验必须先询问 `hasYearZero()`。

### 10.4 月份名称没有传入年份

对带闰月或月份位置会变化的历法，`monthName(locale, month)` 只给“典型年份”的名称。已知年份时使用四参数重载。

## API 速查表
### 类型与常量

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 结构 | `QCalendar::YearMonthDay` | 打包历法中的 `year`、`month`、`day` 三个字段。 | 它的 `isValid()` 不是完整日期校验；仍要调用 `QCalendar::isDateValid()`。 |
| 成员函数 | `YearMonthDay(int year, int month = 1, int day = 1)` | 构造一组年月日字段。 | 默认月、日都是 1；不保证字段在任何历法中真实存在。 |
| 成员函数 | `bool YearMonthDay::isValid() const` | 判断月与日是否不是 `Unspecified`。 | 不检查月份范围、日期范围和年份有效性。 |
| 常量 | `QCalendar::Unspecified` | 表示没有指定年份、月份或日期字段的特殊 `int` 值。 | 不要用 `0` 代替；不同 API 对它的处理不同。 |
| 枚举 | `QCalendar::System` | 选择 Qt 内建的历法系统。 | 可选历法受构建功能影响；先检查 `isValid()` 或可用名称列表。 |
| 类型 | `QCalendar::SystemId` | 表示自定义日历后端的唯一标识。 | Qt 6.2 起提供；该类型的细节见单独的 `QCalendar_SystemId` 笔记。 |

### 构造与发现

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `explicit QCalendar()` | 构造默认的前推公历。 | 默认公历没有 0 年。 |
| 构造 | `explicit QCalendar(QCalendar::System system)` | 用内建枚举选择历法。 | 对 feature 控制的枚举值要检查最终 `isValid()`。 |
| 构造 | `explicit QCalendar(QAnyStringView name)` | 按历法名称构造对象。 | Qt 6.4 前签名不同；插件后端可能要先实例化并注册。 |
| 构造 | `explicit QCalendar(QCalendar::SystemId id)` | 用自定义后端 ID 构造对象。 | Qt 6.2 起提供，主要用于没有名称注册的自定义后端。 |
| 发现 | `static QStringList availableCalendars()` | 返回当前应用可用的历法名称。 | 列表可受插件、链接代码和 Qt 功能配置影响。 |
| 状态 | `bool isValid() const` | 判断是否成功关联到有效历法后端。 | 按名称或可选系统构造后先检查；无效对象不能当作默认公历使用。 |
| 标识 | `QString name() const` | 返回该历法的主名称。 | 按别名构造后，返回值不一定等于传入别名。 |

### 日期转换与校验

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 校验 | `bool isDateValid(int year, int month, int day) const` | 判断字段能否组成该历法中的一个日期。 | 对闰月、不同月长和历史年份有效；不要自行写公历范围。 |
| 转换 | `QDate dateFromParts(int year, int month, int day) const` | 将三个字段转换为确定的 `QDate`。 | 任何字段无效或为 `Unspecified` 时返回 `isNull()` 的 `QDate`。 |
| 转换 | `QDate dateFromParts(const YearMonthDay &parts) const` | 用字段结构进行相同转换。 | 适合承接 `partsFromDate()` 或表单模型；仍可能得到空日期。 |
| 转换 | `YearMonthDay partsFromDate(QDate date) const` | 以当前历法把 `QDate` 拆成年月日。 | 当前历法无法表示日期时，返回结构的 `isValid()` 为 `false`。 |
| 查询 | `int dayOfWeek(QDate date) const` | 返回该日期的星期序号。 | 一般 1 是周一、7 是周日；无法表示时为 0，插日历可能使用更多序号。 |
| 解析辅助 | `QDate matchCenturyToWeekday(const YearMonthDay &parts, int dow) const` | 结合月份、日期、两位年份线索与星期几推断世纪。 | Qt 6.7 起提供；无匹配条件时返回无效 `QDate`。 |

### 历法规则与范围

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 月长 | `int daysInMonth(int month, int year = Unspecified) const` | 返回指定年份中该月的天数。 | 省略年份返回任何年份中的最大可能天数，不能当作某一年实际月长。 |
| 年长 | `int daysInYear(int year) const` | 返回指定年份的天数。 | 传入 `Unspecified` 的行为未定义。 |
| 月数 | `int monthsInYear(int year) const` | 返回指定年份的月份数。 | `Unspecified` 时返回最大可能月数。 |
| 闰年 | `bool isLeapYear(int year) const` | 判断该历法中的某年是否为闰年。 | 不要套用公历整除规则。 |
| 月长范围 | `int maximumDaysInMonth() const` | 返回任意年份中最长月份的天数。 | 用于控件上界或预分配，不能确认某月实际天数。 |
| 月长范围 | `int minimumDaysInMonth() const` | 返回任意年份中最短月份的天数。 | 与 `maximumDaysInMonth()` 一起描述总体范围。 |
| 月数范围 | `int maximumMonthsInYear() const` | 返回一年中可能出现的最大月份数。 | 有闰月的历法中可能大于普通年份的月份数。 |
| 属性 | `bool isGregorian() const` | 判断是否为 Qt 其它日期 API 默认使用的公历对象。 | 不是“看起来像公历”的宽泛比较；用于明确分支。 |
| 属性 | `bool isSolar() const` | 判断是否为太阳历。 | 分类信息，不代替具体月份和日期校验。 |
| 属性 | `bool isLunar() const` | 判断是否为阴历。 | 分类信息，不等于按天文观测计算的全部语义。 |
| 属性 | `bool isLuniSolar() const` | 判断是否为阴阳历。 | 可能存在闰月，构造月名时尤其应传入年份。 |
| 历史范围 | `bool isProleptic() const` | 判断历法规则是否延伸到其首年以前。 | 为真也不意味着存在 0 年。 |
| 历史范围 | `bool hasYearZero() const` | 判断这套年份编号是否有 0 年。 | 处理 BCE、负年份或跨纪元输入前必须确认。 |

### 本地化名称与格式化

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 月名 | `QString monthName(const QLocale &locale, int month, int year = Unspecified, QLocale::FormatType format = QLocale::LongFormat) const` | 返回适合完整日期语境的本地化月名。 | 已知年份时应传入，闰月的位置与名称映射可能依赖年份。 |
| 月名 | `QString standaloneMonthName(const QLocale &locale, int month, int year = Unspecified, QLocale::FormatType format = QLocale::LongFormat) const` | 返回适合标题、列表等独立语境的本地化月名。 | 不要和 `monthName()` 混用；某些语言的词形会不同。 |
| 星期名 | `QString weekDayName(const QLocale &locale, int day, QLocale::FormatType format = QLocale::LongFormat) const` | 返回适合完整日期语境的星期名称。 | 常规编号为 1 到 7；无法识别编号返回空字符串。 |
| 星期名 | `QString standaloneWeekDayName(const QLocale &locale, int day, QLocale::FormatType format = QLocale::LongFormat) const` | 返回适合日历表头等独立语境的星期名称。 | 国际化日历控件应使用此 API 生成表头。 |
| 格式化 | `QString dateTimeToString(QStringView format, const QDateTime &datetime, QDate dateOnly, QTime timeOnly, const QLocale &locale) const` | 依指定历法和 locale 格式化日期、时间或日期时间。 | 优先使用有效的 `datetime`，再是 `dateOnly`、`timeOnly`；都无效返回空字符串。 |

---

### 一句话总结

`QCalendar` 让程序把“一个确定的日子”和“某套历法中的年月日”明确分开：业务层保存 `QDate`，输入和显示时使用 `QCalendar` 转换，再由 `QLocale` 决定语言形式。
