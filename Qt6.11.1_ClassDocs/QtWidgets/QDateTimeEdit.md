# QDateTimeEdit

> Qt 6.11.1 · Qt Widgets · 来自 `QDateTimeEdit`

## 1. 先建立直觉

`QDateTimeEdit` 是带上下微调按钮的日期时间输入控件。它把日期时间拆成多个 section，例如年、月、日、小时、分钟，用户可以用键盘、鼠标滚轮或按钮逐段修改。

典型场景包括预约时间、报表时间范围、定时任务、日志过滤、出生日期、过期时间。它适合精确输入；需要完整月历选择时可启用 calendar popup 或直接使用 `QCalendarWidget`。

## 2. 类说明

- 头文件：`#include <QDateTimeEdit>`
- 模块：`Qt6::Widgets`
- 继承自：`QAbstractSpinBox`
- 直接派生类：`QDateEdit`、`QTimeEdit`

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

它继承 spinbox 的验证、步进、修正和文本编辑能力，并把值类型扩展为 `QDate`、`QTime`、`QDateTime`。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QDateTimeEdit(parent)` | 创建默认日期时间编辑器。 |
| `QDateTimeEdit(date/time/datetime, parent)` | 用初始日期、时间或日期时间创建。 |
| `setDateTime()` / `dateTime()` | 设置或读取完整日期时间。 |
| `setDate()` / `date()` | 只设置或读取日期部分。 |
| `setTime()` / `time()` | 只设置或读取时间部分。 |
| `setDisplayFormat()` / `displayFormat()` | 设置显示和解析格式。 |
| `displayedSections()` | 当前格式里实际显示哪些 section。 |
| `sectionCount()` / `sectionAt()` | 查询 section 数量和位置。 |
| `currentSection()` / `setCurrentSection()` | 读取或设置当前编辑的 section。 |
| `currentSectionIndex()` / `setCurrentSectionIndex()` | 按 section 索引定位当前编辑段。 |
| `sectionText(section)` | 读取某段当前显示文本。 |
| `setDateTimeRange()` | 设置完整日期时间范围。 |
| `setDateRange()` / `setTimeRange()` | 设置日期或时间范围。 |
| `setMinimumDateTime()` / `setMaximumDateTime()` | 设置日期时间上下限。 |
| `setMinimumDate()` / `setMaximumDate()` | 设置日期上下限。 |
| `setMinimumTime()` / `setMaximumTime()` | 设置时间上下限。 |
| `clearMinimum...()` / `clearMaximum...()` | 恢复对应默认边界。 |
| `setCalendarPopup()` / `calendarPopup()` | 是否使用日历弹出选择日期。 |
| `setCalendarWidget()` / `calendarWidget()` | 替换弹出的日历控件。 |
| `setCalendar()` / `calendar()` | 设置使用的日历系统。 |
| `setTimeZone()` / `timeZone()` | Qt 6.7 起设置日期时间的时区。 |
| `dateChanged()` / `timeChanged()` / `dateTimeChanged()` | 值变化信号。 |
| `dateTimeFromText()` / `textFromDateTime()` | 子类化自定义文本和值转换。 |
| `validate()` / `fixup()` | 继承验证和修正流程，自定义输入规则时使用。 |
| `stepBy()` / `stepEnabled()` | 自定义上下步进行为。 |

## 4. 关键用法

### displayFormat 决定用户能编辑什么

`setDisplayFormat("yyyy-MM-dd HH:mm")` 不只是外观，它决定显示哪些 section，也影响解析。只显示日期就不会让用户编辑时间；只显示小时分钟就不会暴露秒。格式要和业务精度一致。

格式里的本地化、12/24 小时、月份文本都会影响输入体验。面向国际用户时不要假设每个人都使用同一种日期顺序。

### 范围约束要成套设置

时间范围筛选常常是两个控件：开始和结束。每次一个值改变后，要更新另一个控件的最小/最大值，避免结束早于开始。`setDateTimeRange()` 比分别设置 min/max 更不容易漏。

若操作导致当前值超出范围，控件会把值调整到有效边界。业务层不要假设 set 进去的值一定原样保留。

### section 是键盘体验的核心

用户在年、月、日、时、分之间移动时，`currentSection` 决定上下箭头改哪一段。需要引导用户编辑某段时用 `setCurrentSection()`；想做自定义步进时重写 `stepBy()` 和 `stepEnabled()`。

### 日历弹窗不是完整日程控件

`calendarPopup` 给日期选择提供方便，但它仍是一个日期选择器，不负责事件标记、禁用复杂日期集合或多选。复杂日历 UI 用 `QCalendarWidget` 子类化或自定义控件。

### 时区要显式思考

Qt 6.7 起有 `timeZone`。任务调度、会议时间、日志时间这些跨时区场景不要只存本地时间显示值。控件可以帮助展示和编辑，但持久化格式仍应由业务层明确设计。

## 5. 常见坑与经验

- `dateChanged()` 对程序调用 `setDate()` 也会触发；只关心用户操作时看 `QDateEdit::userDateChanged` 等子类信号。
- `displayFormat` 太复杂会让键盘编辑困难，宁可拆成多个控件。
- 启用滚轮时，用户滚动页面可能误改值；必要时调整焦点策略或拦截 wheel。
- 无效 `QDateTime` 不会成为控件长期值，通常会回到最小值。
- 保存时分清本地时间、UTC 和带时区时间。
