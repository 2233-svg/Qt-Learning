# Qt QDateTime 深入笔记

> 适用版本：Qt 6.11.1  
> 头文件：`#include <QDateTime>`  
> 所属模块：`Qt6::Core`  
> 定位：表示某个日期、时间和时区语义组成的时间点，并完成解析、格式化和时区转换

## 1. QDateTime 解决什么问题

`QDateTime` 同时保存日期、时间以及它们的时间表示。它适合：

- 记录事件发生时刻、文件时间和网络时间戳。
- 在 UTC、当地时间、固定偏移和命名时区之间转换。
- 计算两个时间点的间隔。
- 解析和格式化用户可见时间。

它不适合测量代码耗时或超时时间。测量耗时使用 `QElapsedTimer`，表示“还剩多久”使用 `QDeadlineTimer`。

```text
一个绝对时间点
       |
       +-- UTC 表示：适合存储、传输、比较
       |
       +-- 指定时区表示：适合用户界面和本地规则
       |
       +-- 本地时间表示：受系统时区和夏令时影响
```

## 2. 推荐策略：存 UTC，显示时转换

```cpp
const QDateTime createdUtc = QDateTime::currentDateTimeUtc();
store(createdUtc.toMSecsSinceEpoch());

const QDateTime local =
    QDateTime::fromMSecsSinceEpoch(
        storedMsecs,
        QTimeZone::systemTimeZone());
label->setText(local.toString(Qt::ISODate));
```

业务系统中，持久化和协议优先使用：

- epoch milliseconds/seconds。
- 带 `Z` 或明确 offset 的 ISO 8601 字符串。
- 明确写出的 IANA 时区 ID 与时间点。

不要把没有时区的本地文本，例如 `2026-09-09 09:00:00`，当成可跨机器可靠比较的绝对时刻。

## 3. 创建、校验和解析

```cpp
const QDate date(2026, 9, 9);
const QTime time(9, 30);
const QDateTime local(date, time);

if (!local.isValid())
    return;
```

解析外部文本：

```cpp
const QDateTime timestamp =
    QDateTime::fromString(
        "2026-09-09T09:30:00Z",
        Qt::ISODate);

if (!timestamp.isValid())
    return;
```

格式化字符串应固定区域和格式。用户输入使用 `QLocale` 解析；网络协议不要依赖 `Qt::TextDate` 或当前系统区域设置。

```cpp
const QDateTime parsed = QDateTime::fromString(
    "2026-09-09 09:30",
    "yyyy-MM-dd HH:mm");
```

这个结果缺少时区信息，必须按业务规定补上 `QTimeZone`，而不是默认当作 UTC。

## 4. 时区转换和夏令时

```cpp
const QDateTime utc = QDateTime::currentDateTimeUtc();
const QDateTime tokyo = utc.toTimeZone(
    QTimeZone("Asia/Tokyo"));
```

将绝对时间点转换到另一个时区是明确的。真正复杂的是从“当地墙上时间”构造时间点：

```text
夏令时开始：02:30 可能根本不存在
夏令时结束：01:30 可能出现两次
```

Qt 6.7 起可用 `TransitionResolution` 指定处理方式：

```cpp
QDateTime appointment(
    QDate(2026, 11, 1),
    QTime(1, 30),
    QTimeZone("America/New_York"),
    QDateTime::TransitionResolution::Reject);
```

对于预约、排班和计费，遇到不存在或重复的本地时间应明确让用户选择或拒绝输入。不要依赖隐式默认策略。

## 5. 比较和间隔

```cpp
if (deadline < QDateTime::currentDateTimeUtc())
    expire();

const qint64 seconds = start.secsTo(end);
const qint64 milliseconds = start.msecsTo(end);
```

比较的是实际时间点，不是展示字符串。两个具备有效时间表示的 QDateTime 即使处于不同的时区，也可以正确比较。

日历运算和持续时间运算不同：

```cpp
const QDateTime tomorrow = now.addDays(1);
const QDateTime later = now.addSecs(24 * 60 * 60);
```

跨夏令时边界时，“明天同一墙上时间”与“24 小时后”可能不同。业务语义决定用 `addDays()` 还是 `addSecs()`。

## 6. epoch API

```cpp
const qint64 now = QDateTime::currentMSecsSinceEpoch();

const QDateTime time =
    QDateTime::fromMSecsSinceEpoch(
        1'788'911'000'000,
        QTimeZone::UTC);
```

epoch 值适合数据库、日志、网络和排序。写秒还是毫秒必须在字段名和协议中明确，例如 `createdAtMs`。不要在同一接口中混用 seconds 与 milliseconds。

## 7. 常见误区

### 用 QDateTime 测量函数耗时

系统时钟可能被 NTP 或用户调整。用 `QElapsedTimer`。

### 存储本地字符串却不存时区

跨时区或夏令时切换后会歧义。存 UTC epoch 或 ISO offset。

### 用 `addSecs(86400)` 表示明天

夏令时切换日未必正好 24 小时。按日历语义用 `addDays(1)`。

### 忽略 `isValid()`

外部文本、越界日期和不存在的当地时刻都可能无效。

### 将 offset 当命名时区

`+08:00` 只是固定偏移，不包含北京、上海或其他地区未来的时区规则。需要规则时使用 `QTimeZone`。

## API 速查表
| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QDateTime()` | 创建空的无效日期时间。 | 使用前检查 isValid；不能当作 Unix epoch。 |
| 构造 | `QDateTime(QDate, QTime, QTimeZone, TransitionResolution)` | 从日期、时间和明确时区构造时间点。 | 处理夏令时不存在或重复时间时明确选择 resolution。 |
| 构造 | `QDateTime(QDate, QTime, TransitionResolution)` | 从日期和当地时间构造日期时间。 | 依赖系统本地时区，持久化和协议中不如显式 QTimeZone 清晰。 |
| 析构 | `~QDateTime()` | 销毁日期时间值。 | 值类型，通常按值传递即可。 |
| 状态 | `isNull()` | 判断是否为空日期时间。 | 空值和有效 epoch 0 不同。 |
| 状态 | `isValid()` | 判断日期、时间和时间表示是否有效。 | 解析外部输入和时区转换后必须检查。 |
| 读取 | `date()` / `time()` | 返回日期或时间部分。 | 这是展示层字段，不自行表达完整时区语义。 |
| 读取 | `timeSpec()` | 返回时间表示类别。 | Qt 6.9 起偏向使用 QTimeZone 相关 API，而非仅靠 TimeSpec。 |
| 读取 | `timeZone()` / `timeRepresentation()` | 返回当前时区或时间表示。 | 固定 offset 与命名时区不同，后者包含规则。 |
| 读取 | `offsetFromUtc()` | 返回当前时间点相对于 UTC 的秒偏移。 | 偏移会因夏令时随时刻变化，不能当作永久时区 ID。 |
| 读取 | `timeZoneAbbreviation()` | 返回此刻的时区缩写。 | 缩写可能有歧义，不应用作机器可读时区标识。 |
| 读取 | `isDaylightTime()` | 判断此时刻是否处于夏令时。 | 只对当前时刻有意义，不能预测所有未来规则。 |
| epoch | `toMSecsSinceEpoch()` | 转为自 Unix epoch 起的毫秒数。 | 协议字段明确单位，避免与秒混用。 |
| epoch | `toSecsSinceEpoch()` | 转为自 Unix epoch 起的秒数。 | 会丢弃毫秒精度。 |
| 修改 | `setDate(QDate, TransitionResolution)` | 修改日期部分。 | 修改后可能落入 DST 歧义时间，检查 isValid。 |
| 修改 | `setTime(QTime, TransitionResolution)` | 修改时间部分。 | 对排班和预约要明确歧义处理。 |
| 修改 | `setTimeZone(QTimeZone, TransitionResolution)` | 改变日期时间的时区表示或解释方式。 | 分清是转换同一时刻还是重新解释墙上时间，测试 DST 边界。 |
| 修改 | `setMSecsSinceEpoch(qint64)` | 将对象设为 epoch 毫秒对应时间。 | 使用已有时区表示转换展示；输入单位必须明确。 |
| 修改 | `setSecsSinceEpoch(qint64)` | 将对象设为 epoch 秒对应时间。 | 秒精度会丢失子秒信息。 |
| 格式化 | `toString(Qt::DateFormat)` | 按预置格式输出文本。 | `TextDate` 不是稳定网络协议格式；协议优先 ISO 8601。 |
| 格式化 | `toString(QString/QStringView)` | 按自定义格式输出文本。 | 格式字符与区域、时区字段必须明确。 |
| 运算 | `addDays()` / `addMonths()` / `addYears()` | 按日历单位移动日期时间。 | 跨 DST、月末和闰年时与固定秒数不同。 |
| 运算 | `addSecs()` / `addMSecs()` / `addDuration()` | 按实际持续时间移动时间点。 | 与“下一日同一时间”不是同一业务语义。 |
| 转换 | `toUTC()` | 转为 UTC 表示。 | 存储和跨系统传输优先使用 UTC。 |
| 转换 | `toLocalTime()` | 转为系统本地时区表示。 | 展示使用方便，但结果依赖机器配置。 |
| 转换 | `toOffsetFromUtc(int)` | 转为固定 UTC 偏移表示。 | 不包含 DST 或地区规则。 |
| 转换 | `toTimeZone(QTimeZone)` | 转为指定命名时区表示。 | 同一绝对时刻不变，仅展示和规则上下文变化。 |
| 比较 | `daysTo()` | 计算到另一个时间点的日数差。 | 适合日历粒度，细粒度用 secsTo/msecsTo。 |
| 比较 | `secsTo()` / `msecsTo()` | 计算到另一个时间点的秒或毫秒差。 | 输入均应有效；比较的是实际时间点。 |
| 当前时间 | `currentDateTime()` | 返回当前系统本地时间。 | 用于 UI，持久化前最好转 UTC 或 epoch。 |
| 当前时间 | `currentDateTimeUtc()` | 返回当前 UTC 时间。 | 协议和日志的推荐起点。 |
| 当前时间 | `currentDateTime(QTimeZone)` | 返回指定时区的当前时间。 | 时区必须有效，适合用户指定地区显示。 |
| 当前 epoch | `currentMSecsSinceEpoch()` / `currentSecsSinceEpoch()` | 返回当前 epoch 时间。 | 适合排序和持久化，不用于耗时测量。 |
| 解析 | `fromString(QStringView, DateFormat)` | 从预置格式文本解析日期时间。 | 外部文本必须检查 isValid；无时区字符串仍需业务解释。 |
| 解析 | `fromString(QString, QStringView, baseYear, QCalendar)` | 按格式、两位年份基准和日历解析文本。 | 用户输入通常配合 QLocale；避免模糊两位年份。 |
| epoch 构造 | `fromMSecsSinceEpoch(qint64, QTimeZone)` | 从毫秒 epoch 创建指定时区表示。 | 存储单位和展示时区分离最清晰。 |
| epoch 构造 | `fromSecsSinceEpoch(qint64, QTimeZone)` | 从秒 epoch 创建指定时区表示。 | 秒精度协议不适合需要毫秒排序的场景。 |
| chrono | `fromStdTimePoint()` | 从兼容的 std::chrono 时间点创建 QDateTime。 | 时钟和时区语义要明确；本地时间 conversion 可能有歧义。 |
| chrono | `toStdSysMilliseconds()` / `toStdSysSeconds()` | 转为 std::chrono system 时间点。 | 需要可用的 C++ chrono 支持；秒转换会丢失毫秒。 |
| 枚举 | `TransitionResolution` | 指定 DST gap 或 overlap 中如何选择时间。 | Qt 6.7 起可用；预约和排班应显式选策略。 |
| 枚举 | `YearRange` | 表示 QDateTime 支持的极端年份范围。 | 主要用于边界代码，普通业务避免靠极端年份表达特殊值。 |
| 流 | `operator<<(QDataStream &, QDateTime)` | 将 QDateTime 写入 Qt 二进制流。 | 依赖 QDataStream version；长期协议需要明确兼容性。 |
| 流 | `operator>>(QDataStream &, QDateTime &)` | 从 Qt 二进制流读取 QDateTime。 | 外部数据读取后检查 stream status 和 isValid。 |

---

### 一句话总结

`QDateTime` 表示的是时间点加时间表示，不只是“日期字符串”。持久化使用 UTC epoch 或带 offset 的 ISO 文本，展示再转换到用户时区；遇到夏令时边界时显式选择规则，测耗时则交给 `QElapsedTimer`。
