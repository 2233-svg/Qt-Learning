# Qt QLocale 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QLocale>`  
> 所属模块：`Qt6::Core`  
> 类型性质：可复制的本地化策略值类型  
> 相关类型：`QString`、`QStringView`、`QDate`、`QTime`、`QDateTime`、`QCalendar`、`QTranslator`、`QCollator`

## 1. 它解决什么问题

`QLocale` 把“一个地区如何表示数据”封装成对象。它既能把数值、日期和时间格式化为当地用户习惯的文本，也能把符合该区域习惯的文本解析回 Qt 值类型。

它主要解决四类问题：

- 用户界面需要显示本地化数字、货币、日期、时间、月份名和星期名；
- 用户输入的数字或日期可能使用本地小数点、分组符号、数字字符和 AM/PM 文本；
- 应用需要根据语言、文字和地区选择翻译或构造区域标识；
- 需要在“面向用户的显示格式”和“稳定的机器协议格式”之间明确分工。

`QLocale` 不是“当前键盘输入法区域”的替代品，也不是所有文本转换的万能 Unicode 规则对象。键盘输入区域应查看 `QInputMethod::locale()`；持久化文件、网络协议和日志格式通常应使用明确规定的 `QLocale::c()` 或协议规定的格式，而不是随用户系统变化的默认区域。

## 2. 实际使用场景

### 2.1 用户界面显示金额和数量

```cpp
const QLocale locale = QLocale::system();

const QString count = locale.toString(1234567);
const QString price = locale.toCurrencyString(1234.5);
```

结果中的分组符、小数点、数字字符、货币符号位置和小数位数都由区域数据决定。不要对 `toCurrencyString()` 的结果再手工拼接货币符号，否则容易得到错误的顺序或间距。

### 2.2 读取本地化输入

```cpp
const QLocale german(QLocale::German, QLocale::Germany);
bool ok = false;
const double value = german.toDouble(QStringLiteral("1.234,56"), &ok);

if (ok) {
    // value == 1234.56
}
```

解析失败通常返回 `0` 或 `0.0`，所以必须传入 `bool *ok`，否则合法的零值和失败无法区分。

### 2.3 用于翻译回退

```cpp
QTranslator translator;
for (const QString &language : QLocale::system().uiLanguages()) {
    if (translator.load(QStringLiteral("app_") + language,
                        QStringLiteral(":/i18n"))) {
        break;
    }
}
```

实际应用更常把 `QLocale` 直接交给 `QTranslator::load()`。`uiLanguages()` 的顺序表达用户偏好，不能把列表当成无序集合，也不应自行用简单截断规则替代 Qt 的回退顺序。

### 2.4 生成稳定的机器格式

```cpp
const QLocale protocolLocale = QLocale::c();
const QString wireNumber = protocolLocale.toString(1234.5, 'g', 17);
```

`QLocale::c()` 适合 POSIX/C 风格的稳定格式，但它并不自动替你定义完整协议。协议仍应明确小数精度、日期格式、时区、允许的分组符和错误处理。

## 3. 构建与最小代码

### 3.1 CMake

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

### 3.2 头文件

```cpp
#include <QLocale>
#include <QString>
```

日期、时间、日历和流 API 还应包含实际使用的类型头文件，例如：

```cpp
#include <QCalendar>
#include <QDate>
#include <QDateTime>
#include <QTime>
#include <QDataStream>
```

### 3.3 最小示例

```cpp
#include <QLocale>
#include <QString>

QString displayTemperature(double celsius)
{
    const QLocale locale = QLocale::system();
    return locale.toString(celsius, 'f', 1) + QStringLiteral(" °C");
}
```

## 4. 先掌握六条核心语义

### 4.1 `QLocale` 是值类型，默认构造依赖全局默认区域

```cpp
const QLocale systemLocale = QLocale::system();
const QLocale defaultLocale;

QLocale::setDefault(QLocale(QLocale::English, QLocale::UnitedStates));
const QLocale newDefault;
```

默认构造的对象使用全局默认区域；如果没有调用 `setDefault()`，通常使用系统区域。已经构造出来的对象不会因为之后改变默认区域而自动改成新区域。

`setDefault()` 是全局设置，应在应用启动阶段、创建其他线程之前完成。它不是 reentrant API；不要在多个线程运行期间随意切换。

### 4.2 系统区域、C 区域和自定义区域用途不同

| 来源 | 适合用途 | 语义 |
| --- | --- | --- |
| `QLocale::system()` | 读取操作系统区域偏好 | 可能使用平台设置中的格式细节 |
| `QLocale()` | 遵循应用全局默认区域 | 受 `setDefault()` 影响 |
| `QLocale::c()` | 稳定的 C/POSIX 风格转换 | 不等同于普通的美国英语显示区域 |
| `QLocale(language, script, territory)` | 明确指定区域 | 使用 Qt 数据库中最合适的匹配 |
| `QLocale(name)` | 读取字符串形式的区域标识 | 方便但比枚举构造慢，格式错误会回退到 C 区域 |

### 4.3 区域身份是语言、文字和地区的组合

`QLocale` 用三个关键值描述区域：

- `language()`：语言，例如 `English`、`Chinese`；
- `script()`：文字系统，例如 `LatinScript`、`SimplifiedHanScript`；
- `territory()`：地区，例如 `UnitedStates`、`China`。

并不是每个三元组合都有完整区域数据。Qt 会依据 CLDR 的 likely-subtag 规则补全缺失值，并在没有精确数据时回退到最接近的可用组合。构造对象后，应调用这三个查询函数确认实际采用的值，不要只相信请求参数。

`AnyLanguage`、`AnyScript` 和 `AnyTerritory` 表示“未指定”，不是一个可以显示给用户的具体语言、文字或地区。

### 4.4 `name()` 和 `bcp47Name()` 不是同一个字符串

- `name()` 是兼容性短名称，默认用下划线，通常只包含语言和地区，不包含显式文字；
- `bcp47Name()` 尽量给出能唯一标识区域的 BCP 47 标签，默认用短横线，可能包含文字；
- `uiLanguages()` 表达用户界面翻译偏好，表示的是“应优先尝试哪些翻译”，不一定等于当前 `QLocale` 的数据区域。

```cpp
const QLocale locale(QLocale::Chinese, QLocale::SimplifiedHanScript,
                     QLocale::Singapore);

const QString compatibilityName = locale.name();       // 兼容性短名
const QString protocolName = locale.bcp47Name();        // BCP 47 风格
const QStringList uiNames = locale.uiLanguages();       // 翻译偏好
```

### 4.5 数字解析的返回值不是错误报告

整数转换失败返回 `0`；浮点转换失败通常返回 `0.0`，溢出时可能返回无穷大。必须检查 `ok`：

```cpp
bool ok = false;
const int number = QLocale::system().toInt(QStringLiteral("0"), &ok);

if (!ok) {
    // 解析失败
} else {
    // number == 0，但这是合法的零
}
```

解析会忽略首尾空白。中间的分组符、小数点、指数格式和尾随零是否接受，受 `NumberOptions` 影响。

### 4.6 本地化显示格式不适合直接持久化

面向用户的文本可能包含非 ASCII 数字、窄不换行空格、方向控制字符、区域特有货币符号或本地月份名。不要把它当作稳定文件格式。机器格式应使用明确的 `QLocale`、明确的格式字符串和明确的精度。

## 5. 公开类型和枚举

### 5.1 `Language`、`Script`、`Country` 和 `Territory`

`Language` 和 `Script` 枚举包含 Qt 6.11.1 支持的语言和文字系统；`Country` 是历史名称，`Territory` 是它的类型别名：

```cpp
using Territory = Country;
```

新代码优先使用 `Territory`、`territory()`、`territoryToCode()` 和 `territoryToString()`。Qt 7 计划进一步完成 `Country` 到 `Territory` 的命名迁移。

最重要的特殊值：

| 类型 | 值 | 含义 |
| --- | --- | --- |
| `AnyLanguage` | 语言未指定 | 常用于 `matchingLocales()` |
| `C` | C 区域语言项 | 与 `QLocale::c()` 的稳定转换规则配套 |
| `AnyScript` | 文字未指定 | 构造和匹配时让 Qt 推断 |
| `AnyTerritory` / `AnyCountry` | 地区未指定 | `AnyCountry` 是兼容别名 |
| `LastLanguage` | 枚举末项 | 不应作为业务语言值 |
| `LastScript` | 枚举末项 | 不应作为业务文字值 |
| `LastTerritory` / `LastCountry` | 枚举末项 | 不应作为业务地区值 |

语言枚举中还保留若干旧名称别名，例如 `Bengali` 对应 `Bangla`、`Oriya` 对应 `Odia`、`Uighur` 对应 `Uyghur`。它们是兼容性取值，不代表另一种语言。

### 5.2 `FormatType`

```cpp
enum FormatType {
    LongFormat,   // 详细格式
    ShortFormat,  // 较短格式
    NarrowFormat  // 空间极紧张时的窄格式
};
```

`NarrowFormat` 可能让不同月份或星期得到相同文本，甚至返回空字符串；不要用它作为可靠的日期解析格式。系统区域中它还可能与 `ShortFormat` 相同。

### 5.3 `NumberOption` 和 `NumberOptions`

```cpp
enum NumberOption {
    DefaultNumberOptions = 0x0,
    OmitGroupSeparator = 0x01,
    RejectGroupSeparator = 0x02,
    OmitLeadingZeroInExponent = 0x04,
    RejectLeadingZeroInExponent = 0x08,
    IncludeTrailingZeroesAfterDot = 0x10,
    RejectTrailingZeroesAfterDot = 0x20
};
Q_DECLARE_FLAGS(NumberOptions, NumberOption)
```

| 选项 | 作用 |
| --- | --- |
| `DefaultNumberOptions` | 使用该区域的默认输入输出规则 |
| `OmitGroupSeparator` | 格式化数字时不输出分组符；C 区域默认带此选项 |
| `RejectGroupSeparator` | 解析时拒绝分组符 |
| `OmitLeadingZeroInExponent` | 指数部分省略单数字数值前的零 |
| `RejectLeadingZeroInExponent` | 解析时拒绝指数前导零 |
| `IncludeTrailingZeroesAfterDot` | 保留小数点后的尾随零 |
| `RejectTrailingZeroesAfterDot` | 解析时拒绝小数点后的尾随零 |

这些标志作用于该 `QLocale` 实例，不会修改系统区域，也不会影响其他已有对象。

### 5.4 `FloatingPointPrecisionOption`

```cpp
QLocale::FloatingPointShortest // 值为 -128
```

把它作为 `toString(double, char, int)` 或 `toString(float, char, int)` 的 `precision`，表示寻找能在逆转换中恢复原浮点值的最短表示。其他负精度会回退到默认精度 `6`。

### 5.5 `MeasurementSystem`

| 值 | 含义 |
| --- | --- |
| `MetricSystem` | 公制 |
| `ImperialUSSystem` | 美国英制 |
| `ImperialUKSystem` | 英国英制 |
| `ImperialSystem` | 兼容别名，等于 `ImperialUSSystem` |

它只描述区域的度量体系，不会替你把任意业务单位自动换算。

### 5.6 货币、数据大小和引号

```cpp
enum CurrencySymbolFormat {
    CurrencyIsoCode,
    CurrencySymbol,
    CurrencyDisplayName
};

enum DataSizeFormat {
    DataSizeIecFormat = 0,
    DataSizeTraditionalFormat = DataSizeSIQuantifiers,
    DataSizeSIFormat = DataSizeBase1000 | DataSizeSIQuantifiers
};

enum QuotationStyle {
    StandardQuotation,
    AlternateQuotation
};
```

`DataSizeFormats` 是 `QFlags<DataSizeFormat>`。常用区别：

- `DataSizeIecFormat`：1024 进制和 `KiB`、`MiB`、`GiB`；
- `DataSizeTraditionalFormat`：1024 进制但使用传统的 `kB`、`MB`、`GB`；
- `DataSizeSIFormat`：1000 进制和 SI 前缀 `kB`、`MB`、`GB`。

### 5.7 `TagSeparator`

```cpp
enum class TagSeparator : char {
    Dash = '-',
    Underscore = '_'
};
```

Qt 6.7 起可在 `name()`、`bcp47Name()` 和 `uiLanguages()` 中指定分隔符。协议使用 BCP 47 时保留默认的 `Dash`；旧资源文件使用下划线时选择 `Underscore`。只支持 ASCII 分隔符语义，不应把非 ASCII 字符强行转换成此枚举。

## 6. 构造、复制和区域身份

### 6.1 通过枚举构造

```cpp
const QLocale us(QLocale::English, QLocale::LatinScript,
                 QLocale::UnitedStates);
const QLocale china(QLocale::Chinese, QLocale::China);
```

`QLocale(Language, Territory)` 会推断可能的文字；`QLocale(Language, Script, Territory)` 可以明确指定三元组合。若组合没有精确数据，Qt 会选择最合适的回退。

### 6.2 通过名称构造

```cpp
const QLocale korean(QStringLiteral("ko"));
const QLocale swiss(QStringLiteral("de_CH"));
const QLocale full(QStringLiteral("zh-Hans-SG"));
```

名称允许：

```text
language[_script][_territory][.codeset][@modifier]
```

语言通常是小写 ISO 639 代码，文字是首字母大写的 ISO 15924 代码，地区是大写 ISO 3166 代码或部分数字代码。分隔符可用 `_` 或 `-`；`.codeset` 和 `@modifier` 会被忽略。格式非法或找不到合适数据时使用 C 区域。

字符串构造比枚举构造慢。高频路径中已知语言和地区时，优先使用枚举构造。

### 6.3 复制和 `swap`

`QLocale` 是隐式共享的值类型，复制成本低。`swap()` 很快且不会失败：

```cpp
QLocale left(QLocale::English, QLocale::UnitedStates);
QLocale right(QLocale::German, QLocale::Germany);
left.swap(right);
```

### 6.4 查询实际区域

```cpp
const QLocale locale(QLocale::Chinese, QLocale::AnyScript,
                     QLocale::Singapore);

const QLocale::Language language = locale.language();
const QLocale::Script script = locale.script();
const QLocale::Territory territory = locale.territory();
```

如果请求使用了 `AnyScript`、`AnyTerritory` 或不可用组合，查询结果是 Qt 实际选出的值。它们是判断回退结果的可靠方式。

## 7. 数字解析：从本地化字符串读取数值

### 7.1 共同规则

所有 `toShort`、`toUShort`、`toInt`、`toUInt`、`toLong`、`toULong`、`toLongLong`、`toULongLong`、`toFloat` 和 `toDouble` 都有 `QStringView` 与 `const QString &` 两种重载：

```cpp
bool ok = false;
const int value = locale.toInt(QStringView{u" 1,234 "}, &ok);
```

共同边界：

- `ok == true` 才表示转换成功；
- 整数转换失败返回 `0`；
- 浮点转换失败通常返回 `0.0`；
- `toFloat()` 和 `toDouble()` 溢出可能返回无穷大；
- 首尾空白会被忽略；
- 分组符、小数点、指数前导零和小数尾随零受 `NumberOptions` 控制；
- 输入中的本地化数字字符应由 `QLocale` 解析，不要只接受 ASCII `0` 到 `9`；
- 传入 `nullptr` 作为 `ok` 时只能得到数值，不能可靠判断失败。

### 7.2 分组符并不总是小数点

```cpp
bool ok = false;
const QLocale german(QLocale::German, QLocale::Germany);
const double value = german.toDouble(QStringLiteral("1.234"), &ok);
// ok == true, value == 1234.0
```

在德国区域，`.` 是分组符，`,` 才是小数点。因此同一个文本在不同区域中可能表示不同数值或直接解析失败。

### 7.3 `QStringView` 重载的用途

`QStringView` 重载允许从已有 UTF-16 字符串视图解析，避免为了调用 API 额外构造 `QString`。视图引用的字符数据必须在调用期间有效；它不会延长底层数据生命周期。

### 7.4 不要把 `toDouble()` 的无穷大当成成功

`toDouble()` 的文档语义是：溢出返回无穷大，并通过 `ok` 报告转换成功或失败。需要拒绝超出业务范围的值时，除了检查 `ok`，还应检查 `std::isfinite()`、业务上下限和单位。

## 8. 数字格式化：从数值生成本地化字符串

### 8.1 整数重载

```cpp
const QLocale arabic(QLocale::Arabic, QLocale::Egypt);
const QString count = arabic.toString(15714290);
const QString padded = arabic.toString(-42, 6, U'0');
```

整数 `toString()` 使用本地区域的数字字符、正负号和分组规则。`short`、`ushort`、`int`、`uint`、`long`、`ulong`、`qlonglong` 和 `qulonglong` 都有对应重载。

带 `fieldWidth` 的版本：

- `fieldWidth > 0`：不足时在数字前填充；
- `fieldWidth < 0`：不足时在数字后填充，目标宽度为 `-fieldWidth`；
- `fillChar == U'0'`：使用该区域的零数字符填充；
- 负数且前置零填充时，零插入负号和数字之间；
- 宽度是最小宽度，不会截断超过宽度的数字。

### 8.2 浮点格式

```cpp
const QString fixed = locale.toString(12.3456, 'f', 2);
const QString scientific = locale.toString(12.3456, 'e', 4);
const QString shortest =
    locale.toString(0.1, 'g', QLocale::FloatingPointShortest);
```

| `format` | 形式 | `precision` 含义 |
| --- | --- | --- |
| `'e'` | 小写指数 | 小数点后的位数 |
| `'E'` | 大写指数 | 小数点后的位数 |
| `'f'` | 定点小数 | 小数点后的位数 |
| `'F'` | 定点小数 | 小数点后的位数，`INF`/`NAN` 使用大写 |
| `'g'` | 在指数和定点中选更紧凑者 | 有效数字最大位数，尾随零省略 |
| `'G'` | 大写版本的紧凑格式 | 有效数字最大位数，尾随零省略 |

特殊值的文本 `inf`、`-inf`、`nan` 或 `INF`、`NAN` 不随区域改变。负的普通 `precision` 会使用默认值 `6`；只有 `FloatingPointShortest` 有特殊意义。

### 8.3 指定区域选项

```cpp
QLocale locale(QLocale::English, QLocale::UnitedStates);
locale.setNumberOptions(QLocale::OmitGroupSeparator |
                        QLocale::RejectGroupSeparator);

const QString text = locale.toString(1234567);
```

格式化和解析使用同一个 `QLocale` 实例的 `numberOptions()`。如果一个对象既用于展示又用于严格输入验证，建议把“展示区域”和“解析策略”分开保存，避免共享选项导致理解混乱。

## 9. 日期和时间

### 9.1 区域预定义格式

```cpp
const QLocale locale(QLocale::English, QLocale::UnitedStates);
const QString datePattern = locale.dateFormat(QLocale::ShortFormat);
const QString timePattern = locale.timeFormat(QLocale::ShortFormat);
const QString dateTimePattern = locale.dateTimeFormat(QLocale::LongFormat);
```

`dateFormat()`、`timeFormat()` 和 `dateTimeFormat()` 返回适合交给 `QDate`、`QTime` 或 `QDateTime` 使用的格式字符串。`LongFormat` 一般更详细，`ShortFormat` 更紧凑，`NarrowFormat` 主要面向空间极小的显示。

不要把返回的区域格式字符串当成跨区域协议格式。它们的字段顺序、文字和标点随区域改变。

### 9.2 格式化日期、时间和日期时间

```cpp
const QDate date(2026, 9, 10);
const QTime time(15, 42, 7);
const QDateTime dateTime(date, time);

const QString localizedDate = locale.toString(date, QLocale::LongFormat);
const QString localizedTime = locale.toString(time, QLocale::ShortFormat);
const QString customDate = locale.toString(date, QStringLiteral("yyyy-MM-dd"));
const QString customTime = locale.toString(time, QStringLiteral("HH:mm:ss"));
const QString localizedDateTime =
    locale.toString(dateTime, QLocale::LongFormat);
```

自定义格式是 `QDate`、`QTime` 和 `QDateTime` 的格式字符规则；区域主要影响名称、数字字符、分隔和 AM/PM 文本。空格式字符串返回空字符串。

日历感知重载接受 `QCalendar`：

```cpp
const QCalendar calendar = QCalendar::system();
const QString text = locale.toString(date, QLocale::LongFormat, calendar);
```

某些区域格式能表示的年份范围有限，使用非默认日历时应特别检查结果。

### 9.3 解析日期、时间和日期时间

```cpp
const QDate date = locale.toDate(QStringLiteral("9/10/26"),
                                 QLocale::ShortFormat, 2020);
const QTime time = locale.toTime(QStringLiteral("3:42 PM"),
                                 QLocale::ShortFormat);
const QDateTime dateTime = locale.toDateTime(
    QStringLiteral("9/10/26 3:42 PM"), QLocale::ShortFormat, 2020);
```

解析失败返回无效的 `QDate`、`QTime` 或 `QDateTime`。月份名和星期名必须使用该区域的语言；AM/PM 文本必须与 `amText()` 或 `pmText()` 匹配，比较时忽略大小写。

### 9.4 两位年份和 `baseYear`

Qt 6.7 起，`toDate()` 和 `toDateTime()` 可以传入 `baseYear`。当格式只提供两位年份时，Qt 首先在 `[baseYear, baseYear + 99]` 的世纪范围中寻找：

```cpp
const QDate date = locale.toDate(QStringLiteral("01/02/30"),
                                  QStringLiteral("MM/dd/yy"), 2030);
// 优先按 2030 到 2129 的范围解释两位年份
```

`QLocale::DefaultTwoDigitBaseYear` 的值是 `1900`，保持 Qt 6.7 之前的默认行为。需要处理生日、账期或历史数据时，不要盲目依赖默认世纪，应该传入业务明确的基准年。

### 9.5 日历格式与时区边界

`QLocale::toDateTime()` 负责按文本格式构造日期时间，但不会替你解决所有时区业务问题。若文本涉及时区、夏令时跳过的本地时间或重复时间，解析后还要检查 `QDateTime` 的时区和有效性。格式可以解析成功，但业务所代表的本地时间仍可能需要额外验证。

## 10. 区域符号、名称和星期规则

### 10.1 数字符号

| API | 返回内容 |
| --- | --- |
| `decimalPoint()` | 小数部分分隔符 |
| `groupSeparator()` | 数字分组分隔符，可能为空 |
| `zeroDigit()` | 零数字符 |
| `negativeSign()` | 负号标记 |
| `positiveSign()` | 正号标记 |
| `exponential()` | 指数分隔标记 |
| `percent()` | 百分号标记 |

这些 API 从 Qt 6 起返回 `QString`，因为某些区域的标记可能由多个 UTF-16 代码单元构成，例如包含方向控制字符。`zeroDigit()` 返回的是字符串，不应假定它一定是一个 `QChar`，也不要假定其他数字一定是从它连续递增得到。

应用代码通常应直接调用 `toString()`，而不是拿 `zeroDigit()` 自行拼装数字。

### 10.2 月名、日名和 standalone 形式

```cpp
const QString month = locale.monthName(1, QLocale::LongFormat);
const QString standaloneMonth =
    locale.standaloneMonthName(1, QLocale::LongFormat);
const QString day = locale.dayName(1, QLocale::ShortFormat);
const QString standaloneDay =
    locale.standaloneDayName(1, QLocale::ShortFormat);
```

- `monthName()` 和 `dayName()` 适合放在日期上下文中；
- `standaloneMonthName()` 和 `standaloneDayName()` 适合单独显示在选择器、标题或列表中；
- 如果区域没有独立形式的数据，standalone API 会回退到普通名称；
- 月份编号是 `1` 到 `12`；
- 星期编号是 `1` 到 `7`，其中 `1` 表示星期一；
- 超出范围的编号不应作为有效月份或星期使用，返回结果不应被当成合法名称。

### 10.3 星期规则和方向

```cpp
const Qt::DayOfWeek first = locale.firstDayOfWeek();
const QList<Qt::DayOfWeek> workingDays = locale.weekdays();
const Qt::LayoutDirection direction = locale.textDirection();
```

`firstDayOfWeek()` 描述日历界面通常从哪一天开始；`weekdays()` 给出该区域认为属于工作日的星期集合；`textDirection()` 返回 `Qt::LeftToRight` 或 `Qt::RightToLeft`。这些值用于界面布局，不应替代业务自己的工作日、节假日和周末政策。

### 10.4 AM/PM

`amText()` 和 `pmText()` 返回 12 小时制的本地化后缀。解析文本时，使用本地区域格式的 AM/PM 文本，比较时忽略大小写。

### 10.5 大小写转换

```cpp
const QString upper = locale.toUpper(QStringLiteral("istanbul"));
const QString lower = locale.toLower(QStringLiteral("Istanbul"));
```

如果 Qt Core 使用 ICU，会按当前区域规则处理；否则可能使用平台实现或 `QString` 的通用回退。大写结果可能比原字符串更长。需要协议级、与区域无关的大小写规则时，不要把用户区域当作协议规则。

### 10.6 `collation()`

```cpp
const QLocale sortingLocale = locale.collation();
QCollator collator(sortingLocale);
```

`collation()` 返回适合传给 `QCollator` 构造函数的排序区域。通常结果就是当前区域，但系统区域可能使用平台提供的专门排序区域。它描述的是文本排序和比较规则，不等于数字格式或日期格式规则；需要用户可见的字典序、大小写敏感性和自然语言排序时，应使用 `QCollator`，不要直接比较 `QString` 的 Unicode 码点。

## 11. 货币和数据大小

### 11.1 `currencySymbol()`

```cpp
const QString iso = locale.currencySymbol(QLocale::CurrencyIsoCode);
const QString symbol = locale.currencySymbol(QLocale::CurrencySymbol);
const QString displayName =
    locale.currencySymbol(QLocale::CurrencyDisplayName);
```

返回值分别是 ISO 4217 代码、货币符号或面向用户的货币名称。它只查询区域默认货币，不表示账户实际结算货币；跨境业务应由业务数据明确货币代码。

### 11.2 `toCurrencyString()`

```cpp
const QString amount = locale.toCurrencyString(1234.5);
const QString usd = locale.toCurrencyString(1234.5, QStringLiteral("USD"), 2);
```

整数重载覆盖 `short`、`ushort`、`int`、`uint`、`qlonglong` 和 `qulonglong`；浮点重载覆盖 `float` 和 `double`。`symbol` 非空时覆盖区域默认货币符号；浮点 `precision == -1` 时使用货币默认精度或 Qt 的默认策略。

这类输出是面向用户的货币文本，不应直接作为数据库金额字段或跨服务协议字段。金额计算应使用整数最小货币单位或专用十进制定点类型，`double` 只适合显示或非精确计算场景。

### 11.3 `formattedDataSize()`

```cpp
const QString size = locale.formattedDataSize(
    16384, 2, QLocale::DataSizeIecFormat);
// 类似 "16.00 KiB"
```

该函数把字节数转换成带单位的本地化文本，并选择使数值至少为 `1` 且尽可能小的单位。`bytes` 可以为负值，结果应按显示需求验证；`precision` 控制数值精度，格式决定 1000/1024 基数和单位前缀。

## 12. 文本辅助

### 12.1 `quoteString()`

```cpp
const QString quoted =
    locale.quoteString(QStringLiteral("report.csv"),
                       QLocale::StandardQuotation);
```

根据区域使用本地化引号包裹文本。`StandardQuotation` 和 `AlternateQuotation` 允许选择两种区域定义的引号样式。它不是 HTML、SQL、Shell 或 C++ 转义函数；不要把它当作安全转义。

### 12.2 `createSeparatedList()`

```cpp
const QString text = locale.createSeparatedList(
    {QStringLiteral("red"), QStringLiteral("green"), QStringLiteral("blue")});
```

使用区域习惯的连接词和分隔规则把字符串列表合成为自然语言列表。它适合用户界面，不适合机器解析。空列表、单元素和多元素列表可能使用不同的连接方式。

### 12.3 `uiLanguages()`

```cpp
const QStringList dashNames = locale.uiLanguages();
const QStringList underscoreNames =
    locale.uiLanguages(QLocale::TagSeparator::Underscore);
```

返回值顺序有意义：前面的语言比后面的语言更优先。Qt 6.9 起，明确配置项之后还会包含合理的截断回退；调用方通常不需要自己把 `en-Latn-US` 截成 `en-US`、`en-Latn` 和 `en`。

## 13. 静态 API：区域工厂、代码转换和匹配

### 13.1 `c()`、`system()` 和 `setDefault()`

```cpp
const QLocale cLocale = QLocale::c();
const QLocale systemLocale = QLocale::system();

QLocale::setDefault(QLocale(QLocale::Japanese, QLocale::Japan));
```

`c()` 是 `noexcept` 的稳定 C 区域工厂；`system()` 读取平台系统区域；`setDefault()` 修改全局默认区域，必须在多线程程序早期调用。

### 13.2 语言代码

```cpp
const QString code = QLocale::languageToCode(
    QLocale::English, QLocale::ISO639Part1);
const QLocale::Language language =
    QLocale::codeToLanguage(QStringView{u"de"});
```

`LanguageCodeType` 主要值：

| 值 | 含义 |
| --- | --- |
| `ISO639Part1` | 两字母代码 |
| `ISO639Part2B` | ISO 639-2 bibliographic 三字母代码 |
| `ISO639Part2T` | ISO 639-2 terminologic 三字母代码 |
| `ISO639Part3` | ISO 639-3 三字母代码 |
| `LegacyLanguageCode` | Qt 兼容旧代码，主要供反向解析 |
| `ISO639Part2` | `Part2B | Part2T` |
| `ISO639Alpha2` | `Part1` |
| `ISO639Alpha3` | `Part2 | Part3` |
| `ISO639` | 所有 ISO 代码集合 |
| `AnyLanguageCode` | 反向解析时接受所有已知代码 |

`languageToCode()` 对 `C` 返回 `"C"`，对 `AnyLanguage` 或没有所选代码的语言返回空字符串。`codeToLanguage()` 找不到代码返回 `AnyLanguage`。默认匹配顺序是 Part 1、Part 2B、Part 2T、Part 3、Legacy。

### 13.3 文字和地区代码

```cpp
const QString scriptCode = QLocale::scriptToCode(QLocale::LatinScript);
const QLocale::Script script =
    QLocale::codeToScript(QStringView{u"Latn"});

const QString territoryCode =
    QLocale::territoryToCode(QLocale::UnitedStates);
const QLocale::Territory territory =
    QLocale::codeToTerritory(QStringView{u"US"});
```

`scriptToCode(AnyScript)` 和 `territoryToCode(AnyTerritory)` 返回空字符串。反向转换失败分别返回 `AnyScript` 和 `AnyTerritory`。地区代码接受 ISO 3166 的两字母代码和部分三位数字代码。

### 13.4 枚举转可读名称

```cpp
const QString languageName =
    QLocale::languageToString(QLocale::English);
const QString scriptName =
    QLocale::scriptToString(QLocale::LatinScript);
const QString territoryName =
    QLocale::territoryToString(QLocale::UnitedStates);
```

这些函数返回 Qt 数据库中的可读英文名称，不是当前用户语言的翻译文本，也不是稳定协议代码。

### 13.5 `matchingLocales()`

```cpp
const QList<QLocale> allLocales = QLocale::matchingLocales(
    QLocale::AnyLanguage, QLocale::AnyScript, QLocale::AnyTerritory);

const QList<QLocale> russianLocales = QLocale::matchingLocales(
    QLocale::Russian, QLocale::AnyScript, QLocale::AnyTerritory);
```

该函数返回与给定语言、文字和地区匹配的有效区域对象。使用 `Any*` 可以查询一组候选；返回结果为空时表示 Qt 数据库中没有匹配项。不要把 `matchingLocales()` 的结果当作翻译优先顺序，翻译顺序应使用 `uiLanguages()`。

## 14. 比较、哈希、流和调试输出

### 14.1 相等比较包含数字选项

```cpp
QLocale left = QLocale::system();
QLocale right = left;

if (left == right) {
    // 区域身份和相关选项一致
}
```

`operator==` 和 `operator!=` 比较的是 `QLocale` 的完整语义状态，不只是语言、文字和地区。两个区域的 `NumberOptions` 不同，则不相等；系统区域对象和用其三个身份值重新构造的对象，即使显示数据相同，也不保证相等。

### 14.2 `qHash()`

```cpp
QHash<QLocale, QString> labels;
labels.insert(QLocale(QLocale::English, QLocale::UnitedStates),
              QStringLiteral("English (US)"));
```

`qHash(const QLocale &, size_t seed = 0)` 为 `QHash` 和 `QSet` 提供哈希。哈希与相等比较保持一致；不要自行只哈希 `name()` 来代替 `QLocale` 的完整键语义。

### 14.3 `QDataStream` 和 `QDebug`

头文件还声明了非成员流和调试运算符：

```cpp
QDataStream &operator<<(QDataStream &, const QLocale &);
QDataStream &operator>>(QDataStream &, QLocale &);
QDebug operator<<(QDebug, const QLocale &);
```

`QDataStream` 序列化适合 Qt 对 Qt 的数据交换，但跨版本、跨语言或长期存档仍应设计版本号和兼容策略。`QDebug` 运算符用于调试输出，不应作为稳定日志协议。

## 15. 弃用 API：Qt 6.6 起使用 `Territory`

下列 API 仍为兼容旧代码保留，但新代码应迁移：

| 弃用 API | 替代 API | 说明 |
| --- | --- | --- |
| `country()` | `territory()` | 查询区域 |
| `nativeCountryName()` | `nativeTerritoryName()` | 查询本地地区名称 |
| `countryToCode(Country)` | `territoryToCode(Territory)` | 地区转 ISO 代码 |
| `codeToCountry(QStringView)` | `codeToTerritory(QStringView)` | ISO 代码转地区 |
| `countryToString(Country)` | `territoryToString(Territory)` | 地区转可读名称 |
| `countriesForLanguage(Language)` | `matchingLocales()` 后查询每项 `territory()` | 更完整地表达语言、文字、地区组合 |

`Country` 枚举本身仍是 `Territory` 的别名，因此旧枚举值通常可以继续编译，但 API 命名应逐步迁移。

## API 速查表

下面按 Qt 6.11.1 类页和头文件中的公共 API 展开。相同语义的重载仍逐项列出，以便查签名和参数边界。

### 16.1 构造、析构、复制和赋值

| API | 作用 | 关键语义和边界 |
| --- | --- | --- |
| `QLocale()` | 构造默认区域 | 使用 `setDefault()` 设置的默认区域，否则通常是系统区域。 |
| `explicit QLocale(QStringView name)` | 从区域名构造 | Qt 6.3；接受 `_`/`-`；格式非法或无匹配时回退到 C 区域；比枚举构造慢。 |
| `explicit QLocale(const QString &name)` | 从 `QString` 区域名构造 | 与 `QStringView` 重载语义相同。 |
| `QLocale(Language language, Territory territory)` | 以语言和地区构造 | 文字由 Qt 推断；无精确数据时选择最合适回退。 |
| `QLocale(Language language, Script script = AnyScript, Territory territory = AnyTerritory)` | 以语言、文字、地区构造 | `Any*` 表示未指定；无匹配时按 CLDR 和 Qt 数据库回退。 |
| `QLocale(const QLocale &other)` | 复制构造 | `noexcept`；值语义，通常共享内部数据。 |
| `QLocale &operator=(const QLocale &other)` | 复制赋值 | `noexcept`；返回 `*this`。 |
| `~QLocale()` | 析构 | `noexcept`；释放当前对象对共享数据的引用。 |
| `void swap(QLocale &other)` | 交换两个区域 | `noexcept`、很快、不失败。 |

### 16.2 区域身份和名称

| API | 作用 | 关键语义和边界 |
| --- | --- | --- |
| `Language language() const` | 返回语言 | 可能是构造请求经过回退后实际采用的语言。 |
| `Script script() const` | 返回文字 | 可能是从 `AnyScript` 推断出的实际文字。 |
| `Territory territory() const` | 返回地区 | Qt 6.2；新代码替代 `country()`。 |
| `QLocale collation() const` | 返回排序区域 | 通常是当前区域；系统区域可能使用平台排序区域，适合交给 `QCollator`。 |
| `QString name(TagSeparator separator = TagSeparator::Underscore) const` | 返回兼容性短名 | 默认下划线；通常不包含脚本；需要完整身份时用 `bcp47Name()`。 |
| `QString bcp47Name(TagSeparator separator = TagSeparator::Dash) const` | 返回 BCP 47 风格名称 | 默认短横线；可能包含脚本；不等同于 UI 翻译偏好。 |
| `QString nativeLanguageName() const` | 返回本地语言名称 | 例如瑞士德语区域的本地化语言名；不是协议代码。 |
| `QString nativeTerritoryName() const` | 返回本地地区名称 | Qt 6.2；新代码替代 `nativeCountryName()`。 |
| `QStringList uiLanguages(TagSeparator separator = TagSeparator::Dash) const` | 返回翻译候选列表 | 顺序表达偏好；Qt 6.9 起包含合理截断回退。 |

### 16.3 数字解析

| API | 作用 | 关键语义和边界 |
| --- | --- | --- |
| `short toShort(QStringView s, bool *ok = nullptr) const` | 解析 `short` | 失败返回 `0`；首尾空白忽略；用 `ok` 区分合法零值。 |
| `short toShort(const QString &s, bool *ok = nullptr) const` | 解析 `short` | 与 `QStringView` 重载语义相同。 |
| `ushort toUShort(QStringView s, bool *ok = nullptr) const` | 解析 `ushort` | 失败返回 `0`；输入不得超出目标类型范围。 |
| `ushort toUShort(const QString &s, bool *ok = nullptr) const` | 解析 `ushort` | 与 `QStringView` 重载语义相同。 |
| `int toInt(QStringView s, bool *ok = nullptr) const` | 解析 `int` | 失败返回 `0`；按本地区域数字规则解析。 |
| `int toInt(const QString &s, bool *ok = nullptr) const` | 解析 `int` | 与 `QStringView` 重载语义相同。 |
| `uint toUInt(QStringView s, bool *ok = nullptr) const` | 解析 `uint` | 失败返回 `0`；负数或溢出应检查 `ok`。 |
| `uint toUInt(const QString &s, bool *ok = nullptr) const` | 解析 `uint` | 与 `QStringView` 重载语义相同。 |
| `long toLong(QStringView s, bool *ok = nullptr) const` | 解析 `long` | 失败返回 `0`；平台上的 `long` 宽度可能不同。 |
| `long toLong(const QString &s, bool *ok = nullptr) const` | 解析 `long` | 与 `QStringView` 重载语义相同。 |
| `ulong toULong(QStringView s, bool *ok = nullptr) const` | 解析 `ulong` | 失败返回 `0`；负数或溢出应检查 `ok`。 |
| `ulong toULong(const QString &s, bool *ok = nullptr) const` | 解析 `ulong` | 与 `QStringView` 重载语义相同。 |
| `qlonglong toLongLong(QStringView s, bool *ok = nullptr) const` | 解析 64 位有符号整数 | 失败返回 `0`；溢出由 `ok` 报告。 |
| `qlonglong toLongLong(const QString &s, bool *ok = nullptr) const` | 解析 64 位有符号整数 | 与 `QStringView` 重载语义相同。 |
| `qulonglong toULongLong(QStringView s, bool *ok = nullptr) const` | 解析 64 位无符号整数 | 失败返回 `0`；负数由 `ok` 报告失败。 |
| `qulonglong toULongLong(const QString &s, bool *ok = nullptr) const` | 解析 64 位无符号整数 | 与 `QStringView` 重载语义相同。 |
| `float toFloat(QStringView s, bool *ok = nullptr) const` | 解析 `float` | 失败通常返回 `0.0f`；溢出可能返回无穷大。 |
| `float toFloat(const QString &s, bool *ok = nullptr) const` | 解析 `float` | 与 `QStringView` 重载语义相同。 |
| `double toDouble(QStringView s, bool *ok = nullptr) const` | 解析 `double` | 失败通常返回 `0.0`；溢出可能返回无穷大；必须检查 `ok`。 |
| `double toDouble(const QString &s, bool *ok = nullptr) const` | 解析 `double` | 与 `QStringView` 重载语义相同。 |

### 16.4 整数和浮点格式化

| API | 作用 | 关键语义和边界 |
| --- | --- | --- |
| `QString toString(qlonglong i) const` | 格式化 64 位有符号整数 | 使用区域数字、分组和符号。 |
| `QString toString(qulonglong i) const` | 格式化 64 位无符号整数 | 使用区域数字和分组。 |
| `QString toString(short i) const` | 格式化 `short` | 等价语义的整数重载。 |
| `QString toString(ushort i) const` | 格式化 `ushort` | 等价语义的整数重载。 |
| `QString toString(int i) const` | 格式化 `int` | 等价语义的整数重载。 |
| `QString toString(uint i) const` | 格式化 `uint` | 等价语义的整数重载。 |
| `QString toString(long i) const` | 格式化 `long` | 等价语义的整数重载。 |
| `QString toString(ulong i) const` | 格式化 `ulong` | 等价语义的整数重载。 |
| `QString toString(qlonglong number, int fieldWidth, char32_t fillChar) const` | 格式化并填充有符号整数 | 正宽度左填充，负宽度右填充；`U'0'` 使用本地区域零数字符。 |
| `QString toString(qulonglong number, int fieldWidth, char32_t fillChar) const` | 格式化并填充无符号整数 | 宽度是最小宽度，不截断较长数字。 |
| `QString toString(short number, int fieldWidth, char32_t fillChar) const` | `short` 的宽度重载 | 与有符号整数宽度规则相同。 |
| `QString toString(int number, int fieldWidth, char32_t fillChar) const` | `int` 的宽度重载 | 与有符号整数宽度规则相同。 |
| `QString toString(long number, int fieldWidth, char32_t fillChar) const` | `long` 的宽度重载 | 与有符号整数宽度规则相同。 |
| `QString toString(ushort number, int fieldWidth, char32_t fillChar) const` | `ushort` 的宽度重载 | 与无符号整数宽度规则相同。 |
| `QString toString(uint number, int fieldWidth, char32_t fillChar) const` | `uint` 的宽度重载 | 与无符号整数宽度规则相同。 |
| `QString toString(ulong number, int fieldWidth, char32_t fillChar) const` | `ulong` 的宽度重载 | 与无符号整数宽度规则相同。 |
| `QString toString(double f, char format = 'g', int precision = 6) const` | 格式化 `double` | 支持 `e/E/f/F/g/G`；`FloatingPointShortest` 选择最短准确表示。 |
| `QString toString(float f, char format = 'g', int precision = 6) const` | 格式化 `float` | `format` 和 `precision` 与 `double` 重载相同。 |

### 16.5 日期、时间和日历重载

| API | 作用 | 关键语义和边界 |
| --- | --- | --- |
| `QString toString(QDate date, FormatType format = LongFormat) const` | 按区域预定义格式输出日期 | 使用 `dateFormat()` 对应格式。 |
| `QString toString(QDate date, QStringView format) const` | 按自定义格式输出日期 | 空格式返回空字符串；视图调用期间必须有效。 |
| `QString toString(QDate date, const QString &format) const` | 按自定义格式输出日期 | 与 `QStringView` 重载语义相同。 |
| `QString toString(QTime time, FormatType format = LongFormat) const` | 按区域预定义格式输出时间 | 使用 `timeFormat()` 对应格式。 |
| `QString toString(QTime time, QStringView format) const` | 按自定义格式输出时间 | 空格式返回空字符串。 |
| `QString toString(QTime time, const QString &format) const` | 按自定义格式输出时间 | 与 `QStringView` 重载语义相同。 |
| `QString toString(const QDateTime &dateTime, FormatType format = LongFormat) const` | 按区域预定义格式输出日期时间 | 使用 `dateTimeFormat()` 对应格式。 |
| `QString toString(const QDateTime &dateTime, QStringView format) const` | 按自定义格式输出日期时间 | 空格式返回空字符串。 |
| `QString toString(const QDateTime &dateTime, const QString &format) const` | 按自定义格式输出日期时间 | 与 `QStringView` 重载语义相同。 |
| `QString toString(QDate date, FormatType format, QCalendar cal) const` | 按区域和指定日历输出日期 | 某些格式的可表示年份范围有限。 |
| `QString toString(QDate date, QStringView format, QCalendar cal) const` | 按自定义格式和日历输出日期 | 空格式返回空字符串。 |
| `QString toString(const QDateTime &dateTime, FormatType format, QCalendar cal) const` | 按区域和指定日历输出日期时间 | 检查日历对年份范围的限制。 |
| `QString toString(const QDateTime &dateTime, QStringView format, QCalendar cal) const` | 按自定义格式和日历输出日期时间 | 空格式返回空字符串。 |
| `QString dateFormat(FormatType format = LongFormat) const` | 查询区域日期格式 | 返回格式字符串，不是稳定协议格式。 |
| `QString timeFormat(FormatType format = LongFormat) const` | 查询区域时间格式 | `LongFormat` 一般含秒和时区，具体以区域数据为准。 |
| `QString dateTimeFormat(FormatType format = LongFormat) const` | 查询区域日期时间格式 | 返回格式字符串，不是稳定协议格式。 |
| `QTime toTime(const QString &string, FormatType format = LongFormat) const` | 按区域格式解析时间 | 失败返回无效 `QTime`；AM/PM 必须匹配区域文本。 |
| `QTime toTime(const QString &string, const QString &format) const` | 按自定义格式解析时间 | 失败返回无效 `QTime`。 |
| `QDate toDate(const QString &string, FormatType format = LongFormat, int baseYear = DefaultTwoDigitBaseYear) const` | 按区域格式解析日期 | 失败返回无效 `QDate`；两位年份使用 `baseYear`。 |
| `QDate toDate(const QString &string, const QString &format, int baseYear = DefaultTwoDigitBaseYear) const` | 按自定义格式解析日期 | 月名和日名使用区域语言；两位年份使用 `baseYear`。 |
| `QDate toDate(const QString &string, FormatType format, QCalendar cal, int baseYear = DefaultTwoDigitBaseYear) const` | 按区域格式和日历解析日期 | 日历参数没有默认值；失败返回无效日期。 |
| `QDate toDate(const QString &string, const QString &format, QCalendar cal, int baseYear = DefaultTwoDigitBaseYear) const` | 按自定义格式和日历解析日期 | 失败返回无效日期。 |
| `QDateTime toDateTime(const QString &string, FormatType format = LongFormat, int baseYear = DefaultTwoDigitBaseYear) const` | 按区域格式解析日期时间 | 失败返回无效 `QDateTime`；注意时区和 DST 边界。 |
| `QDateTime toDateTime(const QString &string, const QString &format, int baseYear = DefaultTwoDigitBaseYear) const` | 按自定义格式解析日期时间 | 两位年份使用 `baseYear`；AM/PM 必须匹配。 |
| `QDateTime toDateTime(const QString &string, FormatType format, QCalendar cal, int baseYear = DefaultTwoDigitBaseYear) const` | 按区域格式和日历解析日期时间 | 失败返回无效日期时间。 |
| `QDateTime toDateTime(const QString &string, const QString &format, QCalendar cal, int baseYear = DefaultTwoDigitBaseYear) const` | 按自定义格式和日历解析日期时间 | 日历参数没有默认值；失败返回无效日期时间。 |

### 16.6 符号、名称、星期和文本

| API | 作用 | 关键语义和边界 |
| --- | --- | --- |
| `QString decimalPoint() const` | 查询小数分隔符 | 返回 `QString`，可能包含多个 UTF-16 代码单元。 |
| `QString groupSeparator() const` | 查询分组分隔符 | 可能为空或是空白字符。 |
| `QString zeroDigit() const` | 查询零数字符 | 可能是代理对；不要用它自行生成其他数字。 |
| `QString negativeSign() const` | 查询负号 | 可能包含方向控制字符。 |
| `QString positiveSign() const` | 查询正号 | 可能包含方向控制字符。 |
| `QString exponential() const` | 查询指数分隔符 | 可能不是单个字符。 |
| `QString percent() const` | 查询百分号标记 | 可能包含方向控制字符。 |
| `QString monthName(int month, FormatType format = LongFormat) const` | 查询月份名 | 月份范围 `1..12`；用于日期上下文。 |
| `QString standaloneMonthName(int month, FormatType format = LongFormat) const` | 查询独立月份名 | 没有独立数据时回退到 `monthName()`。 |
| `QString dayName(int day, FormatType format = LongFormat) const` | 查询星期名 | `1` 是星期一，`7` 是星期日；用于日期上下文。 |
| `QString standaloneDayName(int day, FormatType format = LongFormat) const` | 查询独立星期名 | 没有独立数据时回退到 `dayName()`。 |
| `Qt::DayOfWeek firstDayOfWeek() const` | 查询一周起始日 | 用于界面日历，不等价于业务周定义。 |
| `QList<Qt::DayOfWeek> weekdays() const` | 查询工作日集合 | 不包含节假日策略。 |
| `QString amText() const` | 查询 AM 文本 | 用于显示和解析 12 小时制时间。 |
| `QString pmText() const` | 查询 PM 文本 | 用于显示和解析 12 小时制时间。 |
| `Qt::LayoutDirection textDirection() const` | 查询文字方向 | 返回左到右或右到左。 |
| `QString toUpper(const QString &str) const` | 区域相关大写转换 | ICU 可用时按区域规则；结果可能变长。 |
| `QString toLower(const QString &str) const` | 区域相关小写转换 | ICU 可用时按区域规则，否则可能平台相关。 |
| `QString quoteString(const QString &str, QuotationStyle style = StandardQuotation) const` | 本地化加引号 | 不是安全转义函数。 |
| `QString quoteString(QStringView str, QuotationStyle style = StandardQuotation) const` | `QStringView` 版本加引号 | Qt 6.0；视图调用期间必须有效。 |
| `QString createSeparatedList(const QStringList &list) const` | 本地化连接列表 | 适合用户界面，不适合机器解析。 |

### 16.7 货币和数据大小

| API | 作用 | 关键语义和边界 |
| --- | --- | --- |
| `QString currencySymbol(CurrencySymbolFormat format = CurrencySymbol) const` | 查询货币代码、符号或名称 | 查询区域默认货币，不等于业务结算货币。 |
| `QString toCurrencyString(qlonglong value, const QString &symbol = QString()) const` | 格式化有符号整数金额 | `symbol` 非空时覆盖默认货币符号。 |
| `QString toCurrencyString(qulonglong value, const QString &symbol = QString()) const` | 格式化无符号整数金额 | 使用区域金额布局。 |
| `QString toCurrencyString(short value, const QString &symbol = QString()) const` | `short` 金额重载 | 转发到有符号整数实现。 |
| `QString toCurrencyString(ushort value, const QString &symbol = QString()) const` | `ushort` 金额重载 | 转发到无符号整数实现。 |
| `QString toCurrencyString(int value, const QString &symbol = QString()) const` | `int` 金额重载 | 转发到有符号整数实现。 |
| `QString toCurrencyString(uint value, const QString &symbol = QString()) const` | `uint` 金额重载 | 转发到无符号整数实现。 |
| `QString toCurrencyString(double value, const QString &symbol = QString(), int precision = -1) const` | 格式化浮点金额 | `precision == -1` 使用默认精度；不适合作为精确金额计算。 |
| `QString toCurrencyString(float value, const QString &symbol = QString(), int precision = -1) const` | `float` 金额重载 | 与 `double` 重载相同。 |
| `QString formattedDataSize(qint64 bytes, int precision = 2, DataSizeFormats format = DataSizeIecFormat) const` | 格式化字节数 | 1024/1000 和单位前缀由 `format` 决定。 |

### 16.8 静态 API

| API | 作用 | 关键语义和边界 |
| --- | --- | --- |
| `static constexpr int DefaultTwoDigitBaseYear` | 两位年份默认基准 | Qt 6.7；值为 `1900`。 |
| `static QLocale c() noexcept` | 构造 C 区域 | 稳定转换规则；不等于完整用户显示区域。 |
| `static QLocale system()` | 构造系统区域 | 可能读取平台特定格式设置。 |
| `static void setDefault(const QLocale &locale)` | 设置全局默认区域 | 非 reentrant；多线程程序应在启动早期调用。 |
| `static QString languageToCode(Language language, LanguageCodeTypes codeTypes = AnyLanguageCode)` | 语言转 ISO 代码 | `C` 返回 `"C"`；`AnyLanguage` 或无代码返回空字符串。 |
| `static Language codeToLanguage(QStringView languageCode, LanguageCodeTypes codeTypes = AnyLanguageCode) noexcept` | ISO 代码转语言 | 失败返回 `AnyLanguage`；Qt 6.3。 |
| `static QString scriptToCode(Script script)` | 文字转 ISO 15924 代码 | `AnyScript` 返回空字符串；Qt 6.1。 |
| `static Script codeToScript(QStringView scriptCode) noexcept` | ISO 15924 代码转文字 | 失败返回 `AnyScript`；Qt 6.1。 |
| `static QString territoryToCode(Territory territory)` | 地区转 ISO 3166 代码 | `AnyTerritory` 返回空字符串；Qt 6.2。 |
| `static Territory codeToTerritory(QStringView territoryCode) noexcept` | ISO 3166 代码转地区 | 失败返回 `AnyTerritory`；Qt 6.2。 |
| `static QString languageToString(Language language)` | 语言转可读名称 | 返回 Qt 数据库名称，不是当前 UI 翻译。 |
| `static QString scriptToString(Script script)` | 文字转可读名称 | 返回 Qt 数据库名称。 |
| `static QString territoryToString(Territory territory)` | 地区转可读名称 | Qt 6.2；返回 Qt 数据库名称。 |
| `static QList<QLocale> matchingLocales(Language language, Script script, Territory territory)` | 查找匹配区域集合 | 使用 `Any*` 查询更宽集合；空列表表示无匹配。 |

### 16.9 状态和相关非成员

| API | 作用 | 关键语义和边界 |
| --- | --- | --- |
| `void setNumberOptions(NumberOptions options)` | 设置数字转换选项 | 只影响当前实例。 |
| `NumberOptions numberOptions() const` | 查询数字转换选项 | C 区域默认包含 `OmitGroupSeparator`。 |
| `size_t qHash(const QLocale &key, size_t seed = 0) noexcept` | 哈希区域 | 与 `operator==` 的完整语义配套。 |
| `bool operator==(const QLocale &lhs, const QLocale &rhs) noexcept` | 相等比较 | 数字选项不同也会导致不等。 |
| `bool operator!=(const QLocale &lhs, const QLocale &rhs) noexcept` | 不等比较 | `operator==` 的否定。 |
| `QDataStream &operator<<(QDataStream &, const QLocale &)` | 序列化区域 | 需要启用 DataStream；长期存档应考虑版本策略。 |
| `QDataStream &operator>>(QDataStream &, QLocale &)` | 反序列化区域 | 检查流状态和输入来源。 |
| `QDebug operator<<(QDebug, const QLocale &)` | 调试输出 | 仅用于调试，不是稳定日志协议。 |

### 16.10 Qt 6.6 弃用 API

| API | 替代 | 版本和边界 |
| --- | --- | --- |
| `Country country() const` | `territory()` | Qt 6.6 弃用。 |
| `QString nativeCountryName() const` | `nativeTerritoryName()` | Qt 6.6 弃用。 |
| `static Country codeToCountry(QStringView countryCode) noexcept` | `codeToTerritory()` | Qt 6.1 引入，Qt 6.6 弃用；失败返回 `AnyTerritory`。 |
| `static QList<Country> countriesForLanguage(Language language)` | `matchingLocales()` | Qt 6.6 弃用；遍历结果并查询 `territory()`。 |
| `static QString countryToCode(Country country)` | `territoryToCode()` | Qt 6.6 弃用；`AnyCountry` 返回空字符串。 |
| `static QString countryToString(Country country)` | `territoryToString()` | Qt 6.6 弃用。 |

## 17. 常见误区

### 17.1 把 `QLocale::system()` 当成协议区域

系统设置可能随用户、机器、容器或部署环境变化。协议、缓存键和持久化格式应明确使用 `QLocale::c()` 或协议指定的区域和格式。

### 17.2 只看转换返回值，不看 `ok`

```cpp
const int value = locale.toInt(text);
// value == 0 既可能是输入 "0"，也可能是解析失败
```

正确做法是始终传出 `ok`，尤其是在读取用户输入、配置文件和网络数据时。

### 17.3 手工拼接本地化数字

不要用 `QString::number()`、`zeroDigit()` 和字符串替换拼出本地数字。数字字符可能不连续，分组符和方向控制字符也可能不是单个字符。直接使用 `QLocale::toString()`。

### 17.4 把 `name()` 当成完整区域身份

显式脚本可能不会出现在 `name()` 中。需要唯一表示语言、文字和地区时使用 `bcp47Name()`，需要自定义存储格式时分别使用 `languageToCode()`、`scriptToCode()` 和 `territoryToCode()`。

### 17.5 自己实现 `uiLanguages()` 的回退截断

Qt 6.9 起 `uiLanguages()` 已包含合理截断，且明确配置的语言优先级必须保持在前面。调用方直接按返回顺序尝试翻译即可。

### 17.6 误用 `NarrowFormat`

窄格式可能重复或为空，适合小空间标签，不适合可靠日期文本、唯一月份标题或解析输入。

### 17.7 把 `toCurrencyString()` 当金额计算器

它负责本地化显示，不负责精确金额运算、舍入政策、税率或货币换算。计算层应使用适合金额的数值模型。

### 17.8 依赖系统区域对象和重建对象一定相等

系统区域可能包含平台特定格式信息。即使 `language()`、`script()` 和 `territory()` 一致，`QLocale::system()` 与按这三个值重建的对象也不保证 `operator==` 为真。

## 18. 完整示例：本地化输入、显示和协议分工

```cpp
#include <QLocale>
#include <QString>

struct ParsedOrder
{
    double unitPrice = 0.0;
    int quantity = 0;
};

bool parseOrder(const QLocale &inputLocale,
                QStringView priceText,
                QStringView quantityText,
                ParsedOrder *order)
{
    if (!order)
        return false;

    bool priceOk = false;
    bool quantityOk = false;

    const double price = inputLocale.toDouble(priceText, &priceOk);
    const int quantity = inputLocale.toInt(quantityText, &quantityOk);

    if (!priceOk || !quantityOk || price < 0.0 || quantity < 0)
        return false;

    order->unitPrice = price;
    order->quantity = quantity;
    return true;
}

QString displayOrder(const QLocale &displayLocale, const ParsedOrder &order)
{
    const QString price = displayLocale.toCurrencyString(order.unitPrice);
    const QString quantity = displayLocale.toString(order.quantity);
    return QStringLiteral("%1 x %2").arg(quantity, price);
}

QString serializePrice(const ParsedOrder &order)
{
    // 协议格式不跟随用户区域变化。
    return QLocale::c().toString(order.unitPrice, 'g', 17);
}
```

这里把三个职责分开：

1. `inputLocale` 负责理解用户输入；
2. `displayLocale` 负责界面显示；
3. `QLocale::c()` 负责生成稳定的协议数值文本。

## 19. 选型结论

1. `QLocale` 适合所有面向用户的数字、日期、时间、货币和文本格式化。
2. 解析数字时始终检查 `bool *ok`，不能用返回值本身判断成功。
3. `QLocale::c()` 适合稳定的 C/POSIX 风格转换，但协议仍需明确定义精度和格式。
4. `name()` 是兼容性短名，`bcp47Name()` 才适合表达完整的语言、文字、地区组合。
5. `uiLanguages()` 是翻译优先顺序，不是当前区域身份的简单字符串。
6. `NarrowFormat` 适合紧凑 UI，不适合可靠解析和唯一标识。
7. `DefaultTwoDigitBaseYear` 是 `1900`；涉及历史或未来日期时显式传入 `baseYear`。
8. `Country` API 从 Qt 6.6 起逐步迁移到 `Territory` API。
9. 货币和本地化文本是显示层结果，不应直接承担精确计算和长期存储职责。
10. `setDefault()` 是全局、非 reentrant 设置，应在应用启动和创建线程之前完成。
