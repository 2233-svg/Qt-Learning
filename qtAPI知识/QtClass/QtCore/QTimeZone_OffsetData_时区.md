# QTimeZone::OffsetData：某个时刻的偏移快照

`QTimeZone::OffsetData` 是 `QTimeZone` 查询结果使用的小型结构体。它描述一个具体 UTC 时刻的时区状态：转换发生在什么时候、总偏移是多少、标准偏移和夏令时偏移各是多少，以及该时刻使用的缩写。

它不是一个独立的时区对象，也不负责把日期时间转换成另一个时区。要取得它，应通过 `QTimeZone::offsetData()`、`nextTransition()`、`previousTransition()` 或 `transitions()`；要解释或转换日期时间，应回到 `QDateTime` 和 `QTimeZone`。

```cpp
#include <QDateTime>
#include <QTimeZone>

const QTimeZone zone("Europe/Berlin");
const QDateTime instant = QDateTime::currentDateTimeUtc();
const QTimeZone::OffsetData data = zone.offsetData(instant);

if (data.atUtc.isValid()) {
    qInfo() << "offset:" << data.offsetFromUtc
            << "standard:" << data.standardTimeOffset
            << "dst:" << data.daylightTimeOffset
            << "abbr:" << data.abbreviation;
}
```

## 它解决什么问题

只调用 `offsetFromUtc()` 能得到总偏移，但在诊断夏令时、展示规则变化或审计时，通常还需要知道：

- 这组数据对应哪个 UTC 时刻。
- 总偏移中有多少是标准时间偏移。
- 有多少是 DST 调整。
- 系统在该时刻使用了什么缩写。

`OffsetData` 把这些结果打包成一个值，便于一次返回和批量处理。`QTimeZone::OffsetDataList` 就是 `QList<QTimeZone::OffsetData>`，主要用于查询一段时间内的转换记录。

## 五个字段的关系

### `atUtc`

`atUtc` 是这条数据对应的 UTC 时间点，类型为 `QDateTime`。对于 `offsetData()`，它表示被查询时刻的有效偏移数据；对于 transition API，它表示转换开始生效的时刻。

它也是结果有效性的标志。Qt 文档明确规定：查询没有有效答案时，可能返回 `atUtc` 无效的结构体。先检查它，再使用其它字段：

```cpp
if (!data.atUtc.isValid())
    return;  // 没有可用的时区数据
```

不要只检查 `offsetFromUtc != 0`。UTC 的合法偏移就是零，无效结果的其它整数成员也不能承担有效性标记。

### `offsetFromUtc`

这是该时刻的总偏移，单位为秒，含义是：

```text
当地时间 = UTC + offsetFromUtc
```

它包含标准偏移和 DST 偏移：

```text
offsetFromUtc = standardTimeOffset + daylightTimeOffset
```

例如 Berlin 的标准偏移是 `3600`，夏令时额外偏移是 `3600`，夏季总偏移就是 `7200`。

### `standardTimeOffset`

这是标准时间相对于 UTC 的偏移，单位为秒，不包含当前夏令时调整。它本身也可能随历史规则变化，不要假设一个地区永远固定为同一个标准偏移。

### `daylightTimeOffset`

这是加在标准偏移之上的 DST 分量，单位为秒。常见夏令时是正数，但时区数据库允许历史规则出现负的 DST 偏移，因此不要把它写成只接受非负数的业务逻辑。

没有夏令时的时区通常返回 `0`，但“没有 DST”与“查询失败”仍然要靠 `atUtc.isValid()` 区分。

### `abbreviation`

这是该时刻使用的时区缩写，例如 `CET` 或 `CEST`。缩写可能随季节、历史规则和平台本地化变化，也不能保证全局唯一。它适合日志展示，不适合作为数据库主键、配置 ID 或时区身份。

需要稳定、可本地化的显示文本时，使用 `QTimeZone::displayName()`；需要保存身份时保存 IANA ID。

## `OffsetData` 的来源和边界

不同查询函数对字段的含义略有不同：

- `offsetData(forDateTime)`：返回给定时刻生效的偏移快照。
- `nextTransition(afterDateTime)`：返回给定时刻之后的下一次转换；边界排他。
- `previousTransition(beforeDateTime)`：返回给定时刻之前的上一次转换；边界排他。
- `transitions(fromDateTime, toDateTime)`：返回范围内的转换列表；范围边界包含。

transition 结果中的 `atUtc` 是“规则切换生效的时刻”，不是查询区间的起点。对于本身没有季节/历史转换的固定偏移时区，列表通常为空，`nextTransition()` 和 `previousTransition()` 会返回无效结果。

这些查询依赖 Qt 的 `timezone` feature 和系统可用的时区数据库。系统缺少 tzdata、Windows 映射失败或输入日期超出后端数据能力时，都应准备空/无效结果路径。

## 示例：判断是否处于夏令时

不要通过缩写字符串猜测 DST。直接使用分量：

```cpp
const auto data = zone.offsetData(instant);
if (data.atUtc.isValid()) {
    const bool daylight = data.daylightTimeOffset != 0;
    qInfo() << (daylight ? "daylight time" : "standard time");
}
```

如果业务需要区分“确实处于 DST”和“某些特殊规则下 DST 分量为零”，使用 `QTimeZone::isDaylightTime()`，并以时区后端的定义为准。

## API 速查表

| API/字段 | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `QTimeZone::OffsetData` | 保存一次时区偏移查询结果 | Qt `timezone` feature 可用时提供；通常由 `QTimeZone` 返回 |
| `atUtc` | 记录对应的 UTC 时刻 | 必须先检查 `isValid()`；无效表示查询没有有效答案 |
| `offsetFromUtc` | 记录总 UTC 偏移 | 单位秒；等于标准偏移加 DST 偏移；零不代表无效 |
| `standardTimeOffset` | 记录标准时间偏移 | 单位秒；不包含 DST 分量，历史上可能变化 |
| `daylightTimeOffset` | 记录 DST 偏移分量 | 单位秒；通常为 0 或正数，但不能假定永远非负 |
| `abbreviation` | 记录该时刻的时区缩写 | 可能变化、不唯一或被本地化；不要作为稳定 ID |
| `QTimeZone::offsetData(QDateTime)` | 获取指定时刻的完整偏移快照 | 结果无效时检查 `atUtc` |
| `QTimeZone::nextTransition(QDateTime)` | 获取之后的下一次转换 | 起点排他；找不到返回无效结构 |
| `QTimeZone::previousTransition(QDateTime)` | 获取之前的上一次转换 | 终点排他；找不到返回无效结构 |
| `QTimeZone::transitions(QDateTime, QDateTime)` | 获取范围内所有转换 | 起止边界包含；返回 `OffsetDataList` |
| `QTimeZone::OffsetDataList` | `QList<OffsetData>` 的别名 | 适合遍历转换记录；仍需逐项检查 `atUtc` |
