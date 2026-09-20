# Qt QDateEdit 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）  
> 头文件：`#include <QDateEdit>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QWidget -> QAbstractSpinBox -> QDateTimeEdit -> QDateEdit`  
> 定位：专门编辑 `QDate` 的日期输入控件

## 1. QDateEdit 解决什么问题

`QDateEdit` 是 `QDateTimeEdit` 的日期专用版本：用户可以输入年月日、用箭头调整字段，或从日历弹窗中挑选日期，但界面不暴露时分秒。

它适合生日、合同生效日、账期截止日、发货日期、只按自然日统计的报表范围等场景。

```text
出生日期： [ 1998-04-23 ][v]
```

关键判断是领域里是否真的只有“日期”：

- 生日、节假日、自然日到期日：用 `QDateEdit`，值保存为 `QDate`；
- “2026 年 9 月 7 日 09:30 在上海开始”：这是带时区语义的时刻，使用 `QDateTimeEdit` 和 `QDateTime`；
- “每天 09:30 提醒”：这是一天中的时间，使用 `QTimeEdit` 和 `QTime`。

不要给纯日期强行附加 `00:00:00` 和本地时区再存储。跨时区或夏令时系统中，它很容易从“某日”意外变成前一天或后一天。

## 2. 最小可用示例：限制出生日期

```cpp
#include <QDateEdit>

auto *birthDate = new QDateEdit(this);
birthDate->setDisplayFormat("yyyy-MM-dd");
birthDate->setCalendarPopup(true);
birthDate->setDateRange(
    QDate(1900, 1, 1),
    QDate(2026, 9, 7));
birthDate->setDate(QDate(2000, 1, 1));

connect(birthDate, &QDateTimeEdit::dateChanged, this,
        &ProfileController::setBirthDate);
```

这里的上界明确是 2026 年 9 月 7 日。若业务要求“不能晚于今天”，应改为 `QDate::currentDate()`，让限制随程序运行日期更新。

`QDateEdit` 被加入布局或拥有 `parent` 后，父对象负责它的生命周期；不要把布局中的控件重复手动释放。

## 3. 日期格式既是外观，也是交互规则

`setDisplayFormat()` 决定日期如何显示，也决定哪些字段能被键盘选中和用箭头步进。

```cpp
dateEdit->setDisplayFormat("yyyy-MM-dd");
```

| 格式 | 效果 | 适用场景 |
| --- | --- | --- |
| `yyyy-MM-dd` | `2026-09-07` | 配置、表格、跨地区业务，最不易歧义。 |
| `dd/MM/yyyy` | `07/09/2026` | 已确定地区习惯的本地表单。 |
| `d MMMM yyyy` | `7 September 2026` | 面向用户的阅读型界面。 |
| `yyyy年M月d日` | `2026年9月7日` | 中文业务表单。 |

`MM` 表示月份，`dd` 表示日期，`yyyy` 表示四位年份。避免使用 `yy`：两位年份要按控件初始化时所在世纪解释，容易把数据写进错误的年份。

格式内没有时间字段是 `QDateEdit` 相比 `QDateTimeEdit` 的语义优势。即使它继承了部分日期时间 API，业务代码也应以 `date()` / `setDate()` 和 `QDate` 作为边界。

## 4. 范围只能表达连续日期

```cpp
dateEdit->setDateRange(
    QDate(2026, 1, 1),
    QDate(2026, 12, 31));
```

`minimumDate` 和 `maximumDate` 限定可选的最早和最晚日期，`setDateRange()` 是同时初始化两端的便捷写法。改变某一端时，Qt 会维护一个合法范围；`clearMinimumDate()`、`clearMaximumDate()` 可恢复默认范围边界。

但范围只能描述连续区间，不能表达“仅工作日”“排除法定假期”“只允许每月最后一个工作日”等规则。处理这类需求时：

1. 仍用 `setDateRange()` 限制最宽的合法区间；
2. 使用 `dateChanged` 做领域校验和提示，或配置 `QCalendarWidget` 的视觉提示；
3. 保存前必须在业务层再次校验，不能只相信控件。

日历弹窗只是选择工具，不是预约可用性或排班规则引擎。

## 5. 弹出日历的边界

```cpp
dateEdit->setCalendarPopup(true);
```

开启后，用户点击箭头按钮可以打开日历。它只有在 `displayFormat` 含有效日期字段时才有意义，这一点对 `QDateEdit` 通常天然满足。

需要定制弹窗外观时：

```cpp
dateEdit->setCalendarPopup(true);

auto *calendar = new QCalendarWidget(parentWidget);
calendar->setGridVisible(true);
dateEdit->setCalendarWidget(calendar);
```

调用顺序很重要：先开启 `calendarPopup`，再传给 `setCalendarWidget()`。`QDateTimeEdit` 不会自动取得传入日历控件的所有权，因此 `calendar` 的父对象仍应由调用方明确安排。只需要默认日历时，不必调用 `calendarWidget()`；在满足条件且尚无自定义控件时，调用它会创建默认日历控件。

## 6. `dateChanged` 与 `userDateChanged` 的区别

`QDateEdit` 可用的日期变化信号有两个：

| 信号 | 应如何使用 |
| --- | --- |
| `dateChanged(QDate)` | 继承自 `QDateTimeEdit` 的常规日期变化信号。程序调用 `setDate()` 和用户操作导致的日期变化都应以它为准。 |
| `userDateChanged(QDate)` | `QDateEdit` 自己声明的属性通知信号，Qt 源码注明它是为属性系统补齐的信号。常规业务代码不应依赖它来判断“是否由用户操作触发”。 |

因此，日期联动、表单脏状态、重新查询数据等常规场景，都连接 `dateChanged`：

```cpp
connect(dateEdit, &QDateTimeEdit::dateChanged, this,
        [this](const QDate &date) {
            refreshDailyReport(date);
        });
```

如果要区分“代码初始化”与“真实用户提交”，不要用 `userDateChanged` 猜测来源。初始化阶段可用 `QSignalBlocker` 抑制信号；提交行为则监听继承的 `editingFinished()`，或在界面层显式维护修改状态。

## 7. 常用继承能力

`QDateEdit` 的直接 API 很少，日常能力主要来自 `QDateTimeEdit` 和 `QAbstractSpinBox`：

| 能力 | 什么时候用 |
| --- | --- |
| `setDate()` / `date()` | 设置和读取业务日期。 |
| `setDateRange()` | 约束最早、最晚日期。 |
| `setCalendarPopup()` | 让鼠标用户使用日历选择。 |
| `setDisplayFormat()` | 统一日期显示、输入顺序和字段步进。 |
| `setKeyboardTracking(false)` | 跨越范围边界时，允许用户先形成暂时无效的中间编辑文本。 |
| `editingFinished()` | 用户按 Enter 或失焦后统一提交。 |
| `setSelectedSection(QDateTimeEdit::Section)` | 将焦点定位到年、月或日字段。 |

`time()`、`setTime()`、`timeZone()` 等继承成员在这个日期专用控件上通常不是正确的领域接口。需要时间或时区时，直接换成 `QDateTimeEdit`，代码意图会更清晰。

## API 速查表
### 8.1 QDateEdit 自己声明的 API

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QDateEdit(QWidget *parent = nullptr)` | 创建一个日期编辑控件 | 创建后通常马上设置显示格式、范围和初值；`parent` 负责 Qt 对象生命周期 |
| 构造 | `QDateEdit(QDate date, QWidget *parent = nullptr)` | 用指定 `QDate` 作为初始值创建控件 | 适合编辑已有记录；仍要另外设置业务允许的最小/最大日期 |
| 生命周期 | `~QDateEdit()` | 销毁日期编辑控件 | 通常由父对象自动销毁，业务代码很少直接调用 |
| 信号 | `userDateChanged(QDate date)` | 本类 `date` 属性的通知信号 | 主要服务属性系统；普通业务响应日期变化优先连接继承来的 `dateChanged(QDate)` |

### 8.2 日期编辑常用的继承 API

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 值 | `date() const` | 读取当前日期值 | `QDateEdit` 的业务边界应以 `QDate` 为主，不要把它偷偷转成带时区的 `QDateTime` |
| 值 | `setDate(QDate date)` | 设置当前日期 | 传入值若超出范围，会按控件范围规则被约束；初始化时不想触发联动可配合 `QSignalBlocker` |
| 信号 | `dateChanged(QDate date)` | 日期值改变时发出 | 程序设置和用户操作都会触发，是普通业务联动的首选信号 |
| 日期范围 | `minimumDate() const` / `setMinimumDate(QDate)` / `clearMinimumDate()` | 查询、设置或清除最早可选日期 | `clearMinimumDate()` 只是恢复默认下界，不表示没有业务约束 |
| 日期范围 | `maximumDate() const` / `setMaximumDate(QDate)` / `clearMaximumDate()` | 查询、设置或清除最晚可选日期 | 生日、截止日、有效期等常用；如果上界应是当天，用 `QDate::currentDate()` 动态设置 |
| 日期范围 | `setDateRange(QDate min, QDate max)` | 一次设置最早和最晚日期 | 只能表达连续日期区间；工作日、节假日排除规则要在业务层校验 |
| 格式 | `displayFormat() const` / `setDisplayFormat(const QString &format)` | 查询或设置日期显示格式 | 格式同时影响输入顺序、可编辑字段和步进行为；避免用两位年份 `yy` 保存业务日期 |
| 日历系统 | `calendar() const` / `setCalendar(QCalendar calendar)` | 查询或设置日期计算采用的日历系统 | 它改变历法规则；不是设置弹出的 `QCalendarWidget` 外观 |
| 日历弹窗 | `calendarPopup() const` / `setCalendarPopup(bool enable)` | 查询或开关下拉日历 | 对日期控件通常有意义；若要自定义弹窗控件，先开启 popup 再设置 widget |
| 日历弹窗 | `calendarWidget() const` / `setCalendarWidget(QCalendarWidget *)` | 获取或替换下拉日历控件 | 自定义控件的所有权要由调用方安排，不要假设 `QDateEdit` 自动接管 |
| 编辑提交 | `keyboardTracking()` / `setKeyboardTracking(bool)` | 控制键入过程中是否实时解释并发出变化信号 | 范围复杂或联动昂贵时可设为 `false`，等用户完成编辑后再处理 |
| 编辑提交 | `editingFinished()` | 用户按 Enter 或控件失焦完成编辑时发出 | 适合作为“提交一次日期”的时机，而不是每个字符都提交 |
| 分段 | `currentSection() const` / `setCurrentSection(Section)` | 查询或设置当前正在编辑的日期字段 | 常用于把焦点定位到年、月、日字段 |
| 分段 | `setSelectedSection(Section section)` | 选中指定日期字段 | 适合表单初始化后直接让用户修改某个字段 |
| 分段 | `sectionText(Section section) const` | 读取某个字段当前显示文本 | 返回的是显示文本，不一定适合直接作为业务数据保存 |

---

### 一句话总结

`QDateEdit` 用来表达没有时区、没有时分秒的自然日；范围限制用 `setDateRange()`，业务响应使用 `dateChanged(QDate)`，不要把 `userDateChanged` 当成用户操作判定器。
