# Qt QTimeZone：把 UTC 与民用时间规则连接起来

`QTimeZone` 描述一个从 UTC 到其它时间表示的规则集合。这个表示可以是 UTC、本机本地时间、固定 UTC 偏移，也可以是由系统时区数据库提供的 IANA 时区，例如 `Asia/Shanghai`、`Europe/Berlin`。

它本身是一个无状态的计算对象，最常见的用途是传给 `QDateTime`，让日期时间在特定时区中解释、转换和显示。你通常不需要把它当作“当前时区服务”长期监听；构造出的对象是当时规则的值表示，系统时区之后改变不会自动改写已有对象。

```cpp
#include <QDateTime>
#include <QTimeZone>

const QTimeZone zone("Asia/Shanghai");
if (!zone.isValid())
    return;

const QDateTime utc = QDateTime::currentDateTimeUtc();
const QDateTime local = utc.toTimeZone(zone);
qInfo() << local.toString(Qt::ISODate);
```

## 它解决什么问题

只保存一个 `+08:00` 偏移不能完整表达时区。真实地区可能有夏令时、历史规则变化、名称变化和不同日期的不同偏移。`QTimeZone` 把这些规则与 IANA ID 关联起来，让 `QDateTime` 可以回答：

- 某个 UTC 时刻在 `Europe/Berlin` 是几点。
- 某个日期是否处于夏令时。
- 当前时区的总偏移由标准偏移和 DST 偏移组成多少。
- 某个日期范围内发生了哪些时区转换。

它不解决：

- 日期本身的表示，日期时间值仍由 `QDateTime` 保存。
- 闰秒。和 `QDateTime` 一样，Qt 不按闰秒建模。
- 一个地区未来一定不会修改规则。时区数据库会更新，程序应以运行环境提供的数据为准。
- 只依赖缩写做稳定身份识别。`CET`、`CST` 之类缩写可能不唯一，还可能随系统本地化。

## 时区表示的三种层次

Qt 6.5 起，`QTimeZone` 统一了几种时间表示。`timeSpec()` 可以帮助你区分它们：

| 表示 | 构造方式 | 特点 |
| --- | --- | --- |
| 无效 | `QTimeZone()` | 没有可用规则，必须检查 `isValid()` |
| 本地时间 | `QTimeZone(QTimeZone::LocalTime)` | 使用系统本地时间规则的轻量表示 |
| UTC | `QTimeZone(QTimeZone::UTC)` 或 `QTimeZone::utc()` | 偏移永远是 0 |
| 固定偏移 | `fromSecondsAheadOfUtc()` | 不随日期变化，不含 DST |
| 数据库时区 | `QTimeZone("Europe/Berlin")` | 使用系统/标准数据库，可有历史和季节转换 |

`Qt::UTC` 和 `Qt::OffsetFromUTC` 是轻量表示；`Qt::TimeZone` 表示由系统或标准数据支持的时区后端。`asBackendZone()` 可以把轻量表示转换成后端时区对象，便于调用只对时区数据库开放的 API。

```cpp
QTimeZone fixed = QTimeZone::fromSecondsAheadOfUtc(8 * 60 * 60);
Q_ASSERT(fixed.isUtcOrFixedOffset());

QTimeZone backend = fixed.asBackendZone();
Q_ASSERT(backend.timeSpec() == Qt::TimeZone);
```

## IANA ID、有效性与平台数据

Qt 使用 IANA Time Zone Database 的 ID，目的是在 Windows、Linux、macOS 等平台间使用统一名称。可用 ID 不是永久不变的：

- 主机的 tzdata、系统版本和 Qt 构建方式会影响可用列表。
- Windows 原生 ID 与 IANA ID 不同，Qt 通过 CLDR 映射表转换。
- 某些系统缺少时区数据或配置错误时，数据库时区可能无效。
- UTC 偏移形式可能被构造函数接受，但不一定出现在 `availableTimeZoneIds()` 列表里。

需要从配置加载时，先检查 ID 是否可用，再处理失败：

```cpp
QByteArray id = settings.value("timeZoneId", "UTC").toByteArray();
if (!QTimeZone::isTimeZoneIdAvailable(id))
    id = "UTC";

QTimeZone zone(id);
if (!zone.isValid())
    return false;
```

不要把 IANA ID 的存在当成跨所有设备的恒定事实。对于用户选择项，最好保存 ID，同时在加载时验证并提供明确的回退策略。

## UTC 偏移的符号和范围

偏移量单位是秒，含义是“加到 UTC 上得到当地时间”。例如 `+28800` 表示 UTC+08:00，`-18000` 表示 UTC-05:00。Qt 提供的常量范围是：

- `MinUtcOffsetSecs = -16 * 3600`
- `MaxUtcOffsetSecs = +16 * 3600`

越界的固定偏移会得到无效对象。固定偏移没有季节变化，因此它适合协议、设备或业务明确给出的固定偏移，不适合替代一个真实地区的 IANA 时区。

```cpp
QTimeZone utc8 = QTimeZone::fromSecondsAheadOfUtc(8 * 3600);
Q_ASSERT(utc8.isValid());
Q_ASSERT(utc8.fixedSecondsAheadOfUtc() == 8 * 3600);

QTimeZone invalid = QTimeZone::fromSecondsAheadOfUtc(17 * 3600);
Q_ASSERT(!invalid.isValid());
```

`fixedSecondsAheadOfUtc()` 对 UTC 返回 `0`，对非固定时区也可能返回 `0`，所以不要用它单独判断是否为固定偏移；先用 `isUtcOrFixedOffset()` 或 `timeSpec()`。

## 偏移、夏令时和 `OffsetData`

一个日期时间点的总偏移满足：

```text
offsetFromUtc = standardTimeOffset + daylightTimeOffset
```

例如 Berlin 的标准偏移可能是 `3600` 秒，夏令时额外偏移是 `3600` 秒，因此夏季总偏移是 `7200` 秒。`daylightTimeOffset()` 不一定总是正数，时区历史规则也可能出现负的 DST 偏移。

当需要一次取得某一时刻的全部信息时，用 `offsetData()`：

```cpp
const QDateTime instant =
    QDateTime::fromString("2026-07-01T12:00:00Z", Qt::ISODate);
const QTimeZone berlin("Europe/Berlin");
const QTimeZone::OffsetData data = berlin.offsetData(instant);

if (data.atUtc.isValid()) {
    qInfo() << data.abbreviation
            << data.offsetFromUtc
            << data.standardTimeOffset
            << data.daylightTimeOffset;
}
```

`OffsetData` 的 `atUtc` 是 UTC 时间点；其它字段描述从这个时间点开始生效的偏移和缩写。没有可用数据时，返回的 `OffsetData` 会带无效的 `atUtc`，不能只看整数偏移是否为零。

缩写不是稳定 ID。要给用户显示本地化、可重复的名称，用 `displayName()` 并传入 `QLocale`；要保存或比较身份，保存 IANA ID。

## 转换和夏令时边界

`QTimeZone` 最常与 `QDateTime` 一起使用。建议先明确输入是绝对时刻还是本地民用时间：

- 已经是 UTC/绝对时刻：使用 `toTimeZone(zone)` 转换显示。
- 已知日期时间字段属于某个时区：用对应时区构造 `QDateTime`，再转成 UTC 保存。
- 只有 `QDate` 和 `QTime` 而没有时区：它只是本地日历值，不能凭空推断绝对时刻。

夏令时切换会产生两类麻烦：

- 春季跳时会出现一段本地钟表时间不存在。
- 秋季回拨会出现一段本地钟表时间重复。

涉及预约、账单、日志排序时，内部最好保存 UTC 或带时区的 `QDateTime`，只在输入和显示边界转换为本地时间。

## 转换记录

`hasTransitions()` 表示后端是否支持查询转换记录。`nextTransition()` 和 `previousTransition()` 的查询边界是排他的：给定时间点本身的转换不会作为结果返回。找不到结果时返回无效 `OffsetData`。

`transitions(from, to)` 返回指定范围内的所有转换，两个边界都是包含的；每项的 `atUtc` 是转换生效的 UTC 时刻。

这些 API 依赖 Qt 的 `timezone` 构建特性和运行时数据库。固定偏移或轻量表示可能没有完整转换历史；调用前检查后端能力，并为没有数据的情况留出路径。

## 名称、地区和 Windows 映射

`NameType` 决定显示形式：

- `LongName`：长名称，例如 `Central European Time`。
- `ShortName`：短名称或缩写，例如 `CET`。
- `OffsetName`：标准偏移形式，例如 `UTC+01:00`。
- `DefaultName`：由后端选择合适形式。

`TimeType` 决定名称对应标准时间、夏令时还是不区分季节的通用时间。没有 DST 的时区，三种名称可能相同。

Windows 与 IANA 的转换是多对多关系：

- `ianaIdToWindowsId()`：IANA 到 Windows。
- `windowsIdToIanaIds()`：取得一个 Windows ID 对应的所有 IANA ID。
- `windowsIdToDefaultIanaId()`：取得默认 IANA ID。若不指定地区，可能只是使用频率最高的代表，不一定最适合用户。

需要给具体地区选择时，优先传 `QLocale::Territory`，不要盲目使用全局默认映射。

## 系统时区是快照

`systemTimeZoneId()` 返回当前系统 IANA ID，`systemTimeZone()` 返回相应的对象。这个对象不跟随之后的系统设置变化自动更新。若程序允许用户在运行期间修改系统时区，应在需要时重新获取，而不是永久缓存一次。

`QTimeZone(QTimeZone::LocalTime)` 是轻量的本地时间表示；它和 `systemTimeZone()` 后端对象在系统 API 行为和更新时机上不一定完全相同。需要历史转换、名称或 transition 数据时，优先使用后端时区对象。

## 线程、拷贝和平台桥接

Qt 文档将 `QTimeZone` 的函数标记为线程安全。它是可拷贝的值类型，适合按值传递、放入容器或作为 `QDateTime` 的成员数据。线程安全不意味着共享的外部容器或业务缓存不需要同步。

macOS/iOS 平台桥接只在相应平台和构建条件下存在：

- `fromCFTimeZone()` / `toCFTimeZone()` 对接 Core Foundation。
- `toCFTimeZone()` 返回的对象由调用方负责释放。
- `fromNSTimeZone()` / `toNSTimeZone()` 对接 Objective-C Foundation。
- `toNSTimeZone()` 返回 autoreleased 对象。

跨平台业务代码不要无条件依赖这些类型，必要时用条件编译隔离。

## 常见错误

- 把固定 `+08:00` 当成 `Asia/Shanghai`。固定偏移没有历史和夏令时规则。
- 保存缩写而不是 ID。缩写不唯一，也可能被本地化。
- 假定 `QTimeZone("某个 IANA ID")` 在所有机器都有效。必须检查 `isValid()`。
- 把 `systemTimeZone()` 当成会自动更新的全局对象。它是获取时的时区快照。
- 误读偏移符号。偏移是“加到 UTC 得到当地时间”的秒数。
- 用 `offsetFromUtc()` 的零值判断无效。UTC 的合法总偏移也正好是零。
- 不检查 `OffsetData::atUtc`。没有转换或时区数据时，返回结构可能无效。
- 在本地时间重复/缺失的 DST 区间直接生成账务时间。存储层应优先使用 UTC 或明确的时区时间。
- 用未经地区筛选的 Windows 默认映射。一个 Windows ID 可能覆盖多个 IANA 地区。

## API 速查表

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `QTimeZone()` | 构造空时区 | 返回无效对象；使用前检查 `isValid()` |
| `QTimeZone(QTimeZone::LocalTime/UTC)` | 构造轻量本地时间或 UTC | Qt 6.5 起；不是完整数据库后端 |
| `QTimeZone(const QByteArray &ianaId)` | 按 IANA ID构造 | ID 不可用时无效；可接受部分 UTC 偏移形式 |
| `QTimeZone(int offsetSeconds)` | 构造固定偏移后端时区 | 范围 `-16h..+16h`；需要 timezone feature |
| 自定义构造函数 | 建立固定偏移、名称和地区信息 | ID 不能与已有可用 ID 冲突；偏移仍受范围限制 |
| `isValid()` | 判断对象是否有效 | 失败构造、缺失系统数据都会得到 false |
| `timeSpec()` | 查询表示类型 | `Qt::TimeZone` 表示后端时区；其它表示轻量形式 |
| `isUtcOrFixedOffset()` | 判断是否 UTC 或固定偏移 | 不能只用 `fixedSecondsAheadOfUtc() == 0` 替代 |
| `fixedSecondsAheadOfUtc()` | 读取固定 UTC 偏移 | UTC 和非固定时区都可能返回 0，应配合 `timeSpec()` |
| `fromSecondsAheadOfUtc(int)` | 构造固定偏移轻量表示 | 越界返回无效；0 变成 UTC |
| `fromDurationAheadOfUtc(seconds)` | chrono 版固定偏移构造 | Qt 6.5 起；偏移单位是秒 |
| `asBackendZone()` | 把轻量表示转成后端时区 | Qt 6.5 起；可能访问系统时区数据库 |
| `id()` | 读取 IANA/规范化 ID | 输入的 UTC 偏移文本不一定原样返回 |
| `abbreviation(QDateTime)` | 读取某时刻缩写 | 可能随 DST/历史变化且不唯一 |
| `displayName(TimeType, NameType, QLocale)` | 按类型和本地化设置获取名称 | `LongName`、`ShortName`、`OffsetName` 语义不同 |
| `displayName(QDateTime, NameType, QLocale)` | 获取某时刻适用的显示名 | 可反映季节和历史规则 |
| `territory()` | 查询关联地区 | Qt 6.2 起；可能是 `AnyTerritory` |
| `comment()` | 读取后端或自定义说明 | 适合 UI 辅助信息，不是稳定标识 |
| `offsetFromUtc(QDateTime)` | 读取总偏移 | 等于标准偏移加 DST 偏移，单位秒 |
| `standardTimeOffset(QDateTime)` | 读取标准偏移 | 不含当前 DST 调整 |
| `daylightTimeOffset(QDateTime)` | 读取 DST 偏移 | 不保证为正，单位秒 |
| `hasDaylightTime()` | 判断历史上是否使用过 DST | 不表示当前时刻一定处于 DST |
| `isDaylightTime(QDateTime)` | 判断指定时刻是否处于 DST | 依赖给定日期时间和后端数据 |
| `offsetData(QDateTime)` | 一次读取完整偏移信息 | 无数据时检查返回值的 `atUtc.isValid()` |
| `hasTransitions()` | 判断后端是否支持转换查询 | 不支持时 transition API 不应假定有数据 |
| `nextTransition(QDateTime)` | 查找之后的第一次转换 | 查询起点排他；找不到返回无效 `OffsetData` |
| `previousTransition(QDateTime)` | 查找之前的第一次转换 | 查询终点排他；找不到返回无效 `OffsetData` |
| `transitions(from, to)` | 查询范围内所有转换 | 两端包含；每项 `atUtc` 是生效时刻 |
| `systemTimeZoneId()` | 读取系统 IANA ID | 可能为空；Windows 映射失败不等于有效 ID |
| `systemTimeZone()` | 构造系统时区对象 | 是获取时的快照，不会自动跟随系统设置变化 |
| `utc()` | 获取 UTC 后端时区 | 需要 timezone feature；与轻量 UTC 不同于实现层级 |
| `isTimeZoneIdAvailable(QByteArray)` | 判断 ID 是否在本机可用 | 可能接受不在列表中的 UTC 偏移 ID |
| `availableTimeZoneIds()` | 列出所有可用 IANA ID | 内容随系统数据库和 Qt 构建变化 |
| `availableTimeZoneIds(Territory)` | 按地区筛选 ID | `AnyTerritory`、`World` 有特殊含义 |
| `availableTimeZoneIds(int offsetSeconds)` | 按标准偏移筛选 | 偏移单位秒；可能包含规范化偏移 ID |
| `ianaIdToWindowsId(QByteArray)` | IANA 映射 Windows ID | 映射表和平台数据可能限制结果 |
| `windowsIdToIanaIds(QByteArray[, Territory])` | 查询一个 Windows ID 对应的 IANA ID | 不指定地区是多对多列表；地区版顺序按使用频率 |
| `windowsIdToDefaultIanaId(QByteArray[, Territory])` | 取得默认 IANA 映射 | 无地区时只是常用代表，优先使用地区版 |
| `fromCFTimeZone()` / `toCFTimeZone()` | macOS Core Foundation 桥接 | `toCFTimeZone()` 返回对象由调用方释放 |
| `fromNSTimeZone()` / `toNSTimeZone()` | macOS Foundation 桥接 | `toNSTimeZone()` 返回 autoreleased 对象 |
| `fromStdTimeZonePtr()` | 从 C++20 时区数据库对象构造 | Qt 6.4/对应标准库条件下可用；指针为空得到无效对象 |
| `operator==` / `operator!=` | 比较时区值 | 比较的是时区表示/规则身份，不要用显示名比较 |
| `QDataStream <<` / `>>` | 二进制流读写 | 适合 Qt 内部数据；跨版本协议应明确流版本 |
