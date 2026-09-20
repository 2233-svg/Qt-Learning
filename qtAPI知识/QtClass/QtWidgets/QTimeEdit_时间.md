# Qt QTimeEdit 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）  
> 头文件：`#include <QTimeEdit>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QWidget -> QAbstractSpinBox -> QDateTimeEdit -> QTimeEdit`  
> 定位：专门编辑一天中某个 `QTime` 的控件

## 1. QTimeEdit 解决什么问题

`QTimeEdit` 用来输入“一天中的时刻”：闹钟时间、每日执行时刻、营业开始时间、提醒时间、班次开始时间等。

```text
每日提醒： [ 09:30 ][▲]
                    [▼]
```

它的值是 `QTime`，只有时、分、秒、毫秒，没有日期和时区。因此先区分三种容易混淆的概念：

| 领域含义 | 应使用什么 |
| --- | --- |
| 每天 `09:30` 执行一次 | `QTimeEdit` + `QTime` |
| 从 09:30 到 10:15，持续 45 分钟 | 开始时间用 `QTimeEdit`，持续时间用整数秒、`std::chrono::minutes` 或专用时长输入。 |
| 2026 年 9 月 7 日 09:30 在某时区发生的时刻 | `QDateTimeEdit` + `QDateTime` + 明确的 `QTimeZone`。 |

不要用 `QTimeEdit` 输入“用时 01:30”后直接当作 90 分钟。`QTime(1, 30)` 是凌晨一点半，不是一个持续时长。

## 2. 最小可用示例：每日营业开始时间

```cpp
#include <QTimeEdit>

auto *opensAt = new QTimeEdit(QTime(9, 0), this);
opensAt->setDisplayFormat("HH:mm");
opensAt->setTimeRange(QTime(6, 0), QTime(22, 0));

connect(opensAt, &QDateTimeEdit::timeChanged, this,
        &StoreSettings::setOpeningTime);
```

`setTimeRange()` 将这里的可选时刻限制在 06:00 至 22:00 的连续区间。控件传入 `parent` 或由布局管理后，会遵循 Qt 父子对象的生命周期。

## 3. 显示格式决定精度和键盘交互

```cpp
timeEdit->setDisplayFormat("HH:mm:ss");
```

| 格式 | 效果 | 适用场景 |
| --- | --- | --- |
| `HH:mm` | `09:30`，24 小时制到分钟 | 日常表单、提醒、营业时间。 |
| `HH:mm:ss` | `09:30:15` | 日志过滤、设备控制、秒级计划。 |
| `HH:mm:ss.zzz` | `09:30:15.042` | 毫秒级诊断或媒体时间码。 |
| `h:mm AP` | `9:30 AM`，12 小时制 | 面向使用上午下午习惯的用户。 |

格式不仅是输出字符串。它决定哪些字段存在：

- `HH:mm` 中光标只能选择小时和分钟；
- 加上 `ss` 后，用户才能编辑秒；
- 加上 `zzz` 后，用户才能编辑毫秒；
- `HH` 是 24 小时制，`hh` 搭配 `AP` / `ap` 才适合 12 小时制。

若业务只精确到分钟，显示和保存都应主动归一到分钟；不要在界面隐藏秒、却让模型保留不可见的秒数，用户会觉得“明明没改时间，为什么结果不同”。

## 4. `setTimeRange()` 只能表示同一日内的连续窗口

```cpp
timeEdit->setTimeRange(QTime(9, 0), QTime(18, 0));
```

它适合办公时间、设备允许操作窗口等从早到晚的连续区间。`minimumTime`、`maximumTime` 分别控制上下界；`clearMinimumTime()`、`clearMaximumTime()` 可恢复默认边界。

但“夜间时段 22:00 到次日 06:00”并不是 `QTime` 上的一个单一连续区间，而是两个区间的并集：

```text
[22:00, 24:00) U [00:00, 06:00]
```

不要写：

```cpp
timeEdit->setTimeRange(QTime(22, 0), QTime(6, 0)); // 不是跨午夜范围
```

这不会表达“跨到第二天”；在父类的范围规则下，结束值早于开始值会被调整以保持合法范围。应改用下列一种设计：

- 用 `QDateTimeEdit` 表达真正跨日的开始和结束时刻；
- 保持 `QTimeEdit` 不设这一类范围，在业务层校验 `time >= 22:00 || time <= 06:00`；
- 将“夜班”设计为离散选项，而不是一个自由时间输入框。

## 5. `timeChanged` 与 `userTimeChanged`

`QTimeEdit` 的常规时间变化信号来自父类：

| 信号 | 应如何使用 |
| --- | --- |
| `timeChanged(QTime)` | 常规业务信号。程序调用 `setTime()` 和用户操作导致的时间变化都应由它处理。 |
| `userTimeChanged(QTime)` | `QTimeEdit` 额外声明的 `time` 属性通知信号，服务于 Qt 属性系统。不要依靠它来判定“是否真由用户操作”。 |

```cpp
connect(timeEdit, &QDateTimeEdit::timeChanged, this,
        [this](const QTime &time) {
            updateReminderPreview(time);
        });
```

要在用户按 Enter 或离开控件后才提交，用继承的 `editingFinished()`。若输入每改一个数字都会触发昂贵计算，使用 `setKeyboardTracking(false)`，然后在完成编辑时处理一次。

```cpp
timeEdit->setKeyboardTracking(false);
connect(timeEdit, &QAbstractSpinBox::editingFinished, this,
        [timeEdit, this] { saveAlarmTime(timeEdit->time()); });
```

## 6. 常用继承能力与边界

`QTimeEdit` 直接声明的成员很少，主要依赖 `QDateTimeEdit` 的时间相关 API：

| 能力 | 作用与使用时机 |
| --- | --- |
| `time()` / `setTime(QTime)` | 读写业务时间，是本类最核心的接口。 |
| `minimumTime()` / `maximumTime()` | 查询可选时间边界。 |
| `setTimeRange()` | 一次设置连续时间窗口。 |
| `setDisplayFormat()` | 决定用户能编辑到小时、分钟、秒还是毫秒。 |
| `currentSection()` / `setSelectedSection()` | 查询或定位当前的时、分、秒字段。 |
| `stepUp()` / `stepDown()` | 对当前字段步进。 |
| `setWrapping(bool)` | 在上下界之间循环步进。 |

`setWrapping(true)` 仅适合确有循环语义的时间选择，例如调节“小时”时希望 23 后回到 00。对受业务范围约束的开始时间，循环可能让用户不小心从上界跳到下界，通常应保持默认关闭。

`date()`、`setDate()` 和 `setCalendarPopup()` 虽然在继承链上可见，但不属于纯时间输入的主要语义。需要日期或时区时直接选择 `QDateTimeEdit`，不要让调用者猜测一个 `QTimeEdit` 隐含了哪一天。

## API 速查表
### 7.1 QTimeEdit 自己声明的 API

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QTimeEdit(QWidget *parent = nullptr)` | 创建一个时间编辑控件 | 创建后通常设置显示格式、时间范围和初始值；`parent` 负责 Qt 对象生命周期 |
| 构造 | `QTimeEdit(QTime time, QWidget *parent = nullptr)` | 用指定 `QTime` 作为初始值创建控件 | 适合已有默认提醒时间、营业时间或班次时间的表单 |
| 生命周期 | `~QTimeEdit()` | 销毁时间编辑控件 | 通常由父对象自动销毁，业务代码很少直接调用 |
| 信号 | `userTimeChanged(QTime time)` | 本类 `time` 属性的通知信号 | 主要服务属性系统；普通业务响应时间变化优先连接继承来的 `timeChanged(QTime)` |

### 7.2 时间编辑常用的继承 API

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 值 | `time() const` | 读取当前一天中的时刻 | 返回的是 `QTime`，不是时长，也不包含日期和时区 |
| 值 | `setTime(QTime time)` | 设置当前时间值 | 传入值若超出范围，会按控件范围规则被约束 |
| 信号 | `timeChanged(QTime time)` | 时间值改变时发出 | 程序设置和用户操作都会触发，是普通业务联动的首选信号 |
| 时间范围 | `minimumTime() const` / `setMinimumTime(QTime)` / `clearMinimumTime()` | 查询、设置或清除最早可选时刻 | 只能作为同一日连续窗口的下界 |
| 时间范围 | `maximumTime() const` / `setMaximumTime(QTime)` / `clearMaximumTime()` | 查询、设置或清除最晚可选时刻 | 只能作为同一日连续窗口的上界 |
| 时间范围 | `setTimeRange(QTime min, QTime max)` | 一次设置连续时间范围 | 不表达跨午夜区间；`22:00` 到次日 `06:00` 应拆成业务规则或改用 `QDateTimeEdit` |
| 格式 | `displayFormat() const` / `setDisplayFormat(const QString &format)` | 查询或设置时间显示格式 | 格式决定用户能编辑到小时、分钟、秒还是毫秒 |
| 编辑提交 | `keyboardTracking()` / `setKeyboardTracking(bool)` | 控制键入过程中是否实时解释并发信号 | 昂贵联动、复杂校验时可设为 `false`，等编辑完成再处理 |
| 编辑提交 | `editingFinished()` | 用户按 Enter 或控件失焦完成编辑时发出 | 适合作为一次性保存提醒时间、营业时间的时机 |
| 分段 | `currentSection() const` / `setCurrentSection(Section)` | 查询或设置当前正在编辑的时间字段 | 常用于定位小时、分钟、秒字段 |
| 分段 | `setSelectedSection(Section section)` | 选中指定时间字段 | 适合进入页面后直接让用户改分钟或小时 |
| 分段 | `sectionText(Section section) const` | 读取某个字段当前显示文本 | 返回显示字符串；保存业务值应使用 `time()` |
| 步进 | `stepUp()` / `stepDown()` | 对当前字段执行一次增减 | 适合外部按钮、快捷键或测试自动化触发 |
| 步进 | `wrapping()` / `setWrapping(bool)` | 查询或设置是否从最大值循环到最小值 | 只用于明确有循环语义的时间选择；有严格业务范围时慎用 |

---

### 一句话总结

`QTimeEdit` 表达的是一天中的时刻，不是时长或带日期的绝对时刻；使用 `timeChanged(QTime)` 响应变化，跨午夜规则需要 `QDateTimeEdit` 或额外业务校验。
