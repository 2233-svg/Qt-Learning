# Qt QTime：一天内的时刻值

`QTime` 表示“一天之内的钟表时间”：小时、分钟、秒和毫秒。它不保存日期，不保存时区，也不代表一段持续时间。把它当作一个很小的值类型使用就好：可以拷贝、比较、作为函数参数传递，也可以放进模型、配置或协议字段里。

它最适合描述“每天几点发生”的信息，例如闹钟时间、营业开始时间、班次时间、日志里只有时分秒的字段，或者 UI 里让用户选择一天内某个时刻。只要问题涉及跨日期、夏令时、时区换算或真实耗时测量，就不要只用 `QTime`，应改用 `QDateTime`、`QTimeZone` 或 `QElapsedTimer`。

```cpp
#include <QTime>

QTime start(9, 30);        // 09:30:00.000
QTime end = start.addSecs(45 * 60);

if (end > QTime(10, 0))
    qInfo() << "跨过了 10 点";
```

## 解决的问题

`QTime` 解决的是“把一天内的时刻作为结构化数据处理”的问题。用整数毫秒当然也能表达同样的信息，但 `QTime` 给了你合法性校验、格式化、解析、比较、加减秒/毫秒以及 Qt 序列化支持。这样代码里不会到处散落 `3600000`、`86400000` 这类魔法数。

典型场景包括：

- 表单控件或设置项保存用户选择的时间，例如每天 `18:30` 提醒。
- 文件、网络协议或数据库字段只包含 `HH:mm:ss.zzz`，需要解析后再显示或比较。
- 排班、开关机计划、定时规则等只关心一天内的时刻，不关心是哪一天。
- 将时间值通过 `QVariant`、模型数据或 `QDataStream` 在 Qt 组件之间传递。

它不解决这些问题：

- 不表示时间跨度。`QTime(1, 30)` 不是“一小时三十分钟”，而是“凌晨 1:30”。
- 不处理日期变化。`23:50` 加 20 分钟会绕回 `00:10`，但不会告诉你“到了明天”。
- 不处理时区和夏令时。`QTime` 内部没有 `UTC+8`、`Europe/Berlin` 这样的信息。
- 不适合测量真实耗时。`currentTime()` 受系统时间调整、午夜回绕影响，计时应使用 `QElapsedTimer`。

## 值域、空值与有效性

`QTime` 的合法范围是一天内的毫秒：

- 小时：`0..23`
- 分钟：`0..59`
- 秒：`0..59`
- 毫秒：`0..999`

默认构造的 `QTime()` 是空值，也是无效值。`QTime(0, 0)` 是有效的午夜，不是空值。这个区别很重要：业务上如果允许“00:00”，就不能用 `isNull()` 来判断“用户没有填时间”，更稳妥的做法是用 `isValid()` 或额外的业务状态。

```cpp
QTime none;
QTime midnight(0, 0);

Q_ASSERT(none.isNull());
Q_ASSERT(!none.isValid());

Q_ASSERT(!midnight.isNull());
Q_ASSERT(midnight.isValid());
```

访问字段时，`hour()`、`minute()`、`second()`、`msec()` 在无效时间上返回 `-1`。`msecsSinceStartOfDay()` 在空/无效时间上返回 `0`，因此不能只靠它判断时间是否有效；有效的午夜也会返回 `0`。

## 构造与校验

最直接的构造方式是 `QTime(h, m, s, ms)`。参数不合法时对象会成为无效时间。需要先判断一组数字能否组成时间时，用静态函数 `QTime::isValid()`。

```cpp
QTime a(21, 10, 30);          // valid
QTime b(22, 5, 62);           // invalid

if (QTime::isValid(7, 45, 0))
    schedule(QTime(7, 45));
```

`setHMS()` 会修改已有对象，并用返回值告诉你新值是否合法。调用失败时，不要继续把对象当作业务有效值使用；实际代码通常应立即分支处理错误。

```cpp
QTime t;
if (!t.setHMS(hour, minute, second, msec))
    return false;
```

`fromMSecsSinceStartOfDay()` 适合和整数毫秒字段对接。有效范围是 `0..86399999`，也就是从当天开始到当天最后一毫秒。超出范围会得到无效时间。

## 加减与跨午夜边界

`addSecs()` 和 `addMSecs()` 返回新对象，不修改原对象。它们按一天 24 小时循环，超过午夜会绕回当天开头，向前减也会从当天末尾绕回。

```cpp
QTime n(14, 0, 0);

Q_ASSERT(n.addSecs(70) == QTime(14, 1, 10));
Q_ASSERT(n.addSecs(-70) == QTime(13, 58, 50));
Q_ASSERT(n.addSecs(10 * 60 * 60 + 5) == QTime(0, 0, 5));
Q_ASSERT(n.addSecs(-15 * 60 * 60) == QTime(23, 0, 0));
```

这个“自动绕回”既方便也危险。它适合处理钟面上的时间，不适合表达“从今天 23:50 到明天 00:10 已经过 20 分钟”这种带日期含义的问题。需要知道是否跨天时，要把日期一起保存，或者自己记录天数偏移。

`secsTo()` 和 `msecsTo()` 计算两个 `QTime` 在同一天坐标上的差值，不会自动跨午夜取最短距离。如果目标时间更早，结果就是负数。任一对象无效时返回 `0`，所以调用前应先检查 `isValid()`。

```cpp
QTime late(23, 50);
QTime early(0, 10);

Q_ASSERT(late.secsTo(early) < 0);  // 不会理解成“20 分钟后”
```

`secsTo()` 忽略毫秒部分；需要精确到毫秒时使用 `msecsTo()`。

## 当前时间与计时误区

`QTime::currentTime()` 读取系统当前本地钟表时间，返回的是一个 `QTime`。它适合显示“现在几点”，也可以作为用户界面里的默认值。

它不适合测量耗时，原因有三点：

- 到了午夜会从 `23:59:59.999` 跳回 `00:00:00.000`。
- 用户或系统服务可以调整系统时间。
- 夏令时或平台时间规则变化会影响本地时间的表现。

测量耗时请用 `QElapsedTimer`；需要当前日期和时区语义请用 `QDateTime::currentDateTime()`。

## 字符串格式化与解析

`toString()` 和 `fromString()` 支持 `Qt::DateFormat`，也支持自定义格式字符串。自定义格式常见符号如下：

| 符号 | 含义 |
| --- | --- |
| `h` / `hh` | 12 小时制小时 |
| `H` / `HH` | 24 小时制小时 |
| `m` / `mm` | 分钟 |
| `s` / `ss` | 秒 |
| `z` / `zz` / `zzz` | 毫秒 |
| `AP` / `A`、`ap` / `a` | 上午/下午标记 |
| `aP` / `Ap` | Qt 6.3 起支持的大小写组合 |
| `t` / `tt` / `ttt` / `tttt` | 时区相关文本，主要用于日期时间格式 |

字面量要放在单引号里，两个连续单引号表示一个真正的单引号。没有分隔符的格式容易产生歧义，解析用户输入时建议优先使用清晰的分隔符。

```cpp
QTime t = QTime::fromString("1mm12car00", "m'mm'hcarss");
Q_ASSERT(t == QTime(12, 1, 0));

Q_ASSERT(!QTime::fromString("00:710", "hh:ms").isValid());
Q_ASSERT(QTime::fromString("1.30", "m.s") == QTime(0, 1, 30));
```

`QTime` 的字符串转换使用 C locale。需要本地化的上午/下午文本、数字或区域格式时，用 `QLocale` 做格式化和解析，不要把本地化规则硬塞进 `QTime::fromString()`。

无效时间调用 `toString()` 会得到空字符串；`fromString()` 解析失败会返回无效 `QTime`。

## 比较、线程与序列化

`QTime` 是可重入的值类型。多个线程可以各自操作自己的 `QTime` 实例；共享同一个变量时仍然要遵守普通 C++ 数据竞争规则。

比较运算按一天内的时间先后排序。`23:00` 大于 `01:00`，即使业务上你想表达“第二天凌晨一点”。跨天逻辑必须额外建模。

Qt 还提供 `QDataStream` 的 `operator<<` / `operator>>`，可以把 `QTime` 写入二进制流。读写双方应保持兼容的流版本和数据格式；它适合 Qt 程序内部协议，不适合拿来做长期公开文件格式的唯一说明。

## 常见错误

- 把 `QTime` 当持续时间使用。持续时间请用毫秒数、`std::chrono` 或业务自己的 duration 类型。
- 用 `currentTime().msecsTo(...)` 计时。跨午夜或系统时间调整会让结果错误。
- 忘记检查 `fromString()` 的结果。解析失败返回无效对象，不会抛异常。
- 用 `msecsSinceStartOfDay() == 0` 判断空值。有效午夜同样是 `0`。
- 期望 `secsTo()` 自动跨午夜。它只在同一天坐标上相减。
- 把 `QTime` 当作时区时间。单独的 `QTime` 没有任何时区语义。

## API 速查表

| API | 作用 | 关键语义与边界 |
| --- | --- | --- |
| `QTime()` | 构造空时间 | 空时间无效；不同于有效的 `QTime(0, 0)` |
| `QTime(int h, int m, int s = 0, int ms = 0)` | 按时分秒毫秒构造 | 合法范围为 `0..23`、`0..59`、`0..59`、`0..999`；参数非法得到无效时间 |
| `isNull() const` | 判断是否为空时间 | 默认构造为空；不要用它排除午夜 |
| `isValid() const` | 判断对象是否为有效时间 | 业务使用前最常用的守卫 |
| `static isValid(int h, int m, int s, int ms = 0)` | 判断一组字段是否合法 | 适合在构造或接受用户输入前校验 |
| `setHMS(int h, int m, int s, int ms = 0)` | 重设对象的时分秒毫秒 | 返回 `false` 表示参数非法；调用方要处理失败 |
| `hour() const` | 取小时 | 无效时间返回 `-1` |
| `minute() const` | 取分钟 | 无效时间返回 `-1` |
| `second() const` | 取秒 | 无效时间返回 `-1` |
| `msec() const` | 取毫秒 | 无效时间返回 `-1` |
| `msecsSinceStartOfDay() const` | 返回从午夜起的毫秒数 | 空/无效时间也返回 `0`；不能单独作为有效性判断 |
| `static fromMSecsSinceStartOfDay(int msecs)` | 从当天起始毫秒数构造 | 有效范围 `0..86399999`；越界返回无效时间 |
| `addSecs(int s) const` | 返回加减秒后的新时间 | 按 24 小时绕回；无效输入时间返回空/无效结果 |
| `addMSecs(int ms) const` | 返回加减毫秒后的新时间 | 同样绕回午夜；不携带跨天信息 |
| `secsTo(QTime t) const` | 返回到目标时间的秒差 | 不跨午夜取最短距离；目标更早则为负；任一无效返回 `0` |
| `msecsTo(QTime t) const` | 返回到目标时间的毫秒差 | 保留毫秒精度；任一无效返回 `0` |
| `static currentTime()` | 读取当前本地钟表时间 | 受系统时间、午夜和平台规则影响；不要用于耗时测量 |
| `toString(Qt::DateFormat format = Qt::TextDate) const` | 按 Qt 预设格式输出字符串 | 无效时间返回空字符串 |
| `toString(const QString &format) const` / `toString(QStringView format) const` | 按自定义格式输出字符串 | 使用 C locale；本地化输出用 `QLocale` |
| `static fromString(..., Qt::DateFormat format = Qt::TextDate)` | 按 Qt 预设格式解析 | 解析失败返回无效时间 |
| `static fromString(..., QStringView/QString format)` | 按自定义格式解析 | 注意格式歧义、字面量引号和本地化限制 |
| 比较运算符 | 比较一天内先后顺序 | 不含日期；`23:00 > 01:00` |
| `QDataStream <<` / `>>` | 二进制流读写 | 适合 Qt 内部序列化；注意流版本兼容 |

## 实用判断

看到一个需求时可以先问一句：它是不是只关心“钟面上几点几分几秒”？如果答案是是，`QTime` 很合适；如果答案里出现“今天/明天”“UTC”“持续了多久”“夏令时”“跨时区”，就应该换成更完整的时间模型。
