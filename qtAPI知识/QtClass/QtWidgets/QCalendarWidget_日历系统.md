# Qt QCalendarWidget 深入笔记

> 适用版本：Qt 6 Widgets（本文按 Qt 6.11.1 API 整理）  
> 头文件：`#include <QCalendarWidget>`  
> 所属模块：`Qt6::Widgets`  
> 继承：`QWidget -> QCalendarWidget`  
> 定位：可嵌入界面的月历选择控件，而不是日期文本输入框

## 1. QCalendarWidget 解决什么问题

`QCalendarWidget` 在窗口中持续展示一个月历，允许用户查看月份、浏览年月、选择一个日期，并为特殊日期加颜色或字体标记。

```text
        2026 年 9 月
一  二  三  四  五  六  日
31   1   2   3   4   5   6
 7   8   9  10  11  12  13
```

它适合排班面板、任务日历、按日过滤的报表、会议日期选择、节假日展示和设备运行日历。

不要把它与 `QDateEdit` 混为一谈：

| 类型 | 主要体验 | 典型位置 |
| --- | --- | --- |
| `QDateEdit` | 紧凑的单值输入框，可选弹出月历。 | 表单的一行字段。 |
| `QCalendarWidget` | 始终可见的整月视图。 | 侧栏、排期页面、独立日期选择区。 |

`QCalendarWidget` 只支持 `NoSelection` 或单日期 `SingleSelection`。需要选一个日期范围、多天复选、拖拽排班或资源占用热力图时，应在它之上实现状态和绘制，或选择更适合的日历视图方案。

## 2. 最小可用示例：选择未来 30 天内的日期

```cpp
#include <QCalendarWidget>

auto *calendar = new QCalendarWidget(this);
const QDate first(2026, 9, 7);
const QDate last = first.addDays(30);

calendar->setDateRange(first, last);
calendar->setSelectedDate(first);
calendar->setGridVisible(true);
calendar->setFirstDayOfWeek(Qt::Monday);
calendar->setHorizontalHeaderFormat(QCalendarWidget::ShortDayNames);

connect(calendar, &QCalendarWidget::activated, this,
        &BookingController::acceptDate);
```

上例的最早日期是 2026 年 9 月 7 日，最晚日期是其后 30 天。若范围应随当天变化，可把 `first` 改为 `QDate::currentDate()`。

控件接受 `parent` 后由 Qt 父子对象机制管理生命周期；作为独立页面组件时，通常应把它交给布局，而不是靠固定坐标摆放。

## 3. 最重要的状态：选中日期不等于正在看的月份

`QCalendarWidget` 同时维护两个状态：

| 状态 | 查询 API | 改变 API | 用途 |
| --- | --- | --- | --- |
| 选中的日期 | `selectedDate()` | `setSelectedDate(QDate)` | 表单值、筛选条件、真正要提交的日期。 |
| 当前显示页面 | `yearShown()`、`monthShown()` | `setCurrentPage(year, month)` | 用户正在浏览哪个月份。 |

```cpp
calendar->setSelectedDate(QDate(2026, 9, 7));
calendar->setCurrentPage(2026, 12);
```

这段代码会显示 2026 年 12 月，但选中的日期仍是 2026 年 9 月 7 日。`setCurrentPage()` 只翻页，不会偷偷修改业务值；反过来，`showSelectedDate()` 会把当前页面带回选中日期所在月份。

这一区别对“浏览历史月份但不改变报表筛选条件”“预加载用户将要看到的月份数据”非常重要。浏览月变化时连接 `currentPageChanged()`；只有真正选择变化时才处理 `selectionChanged()`。

## 4. 日期范围与禁止选择不是一回事

```cpp
calendar->setDateRange(
    QDate(2026, 9, 7),
    QDate(2026, 10, 7));
```

`minimumDate` / `maximumDate` 限制用户可以选择的日期，范围外日期不能被选择。设置一端时，如果范围或当前选中日期因此失效，Qt 会调整另一端和选中日期来保持一致；传入无效 `QDate` 时，单独设置最小/最大日期不会生效。

`setSelectionMode(QCalendarWidget::NoSelection)` 则是另一种语义：用户不能用鼠标或键盘选择日期，但控件仍保留并允许程序设置 `selectedDate`。它适合“只读日历概览”，不等于清空选中日期。

```cpp
calendar->setSelectionMode(QCalendarWidget::NoSelection);
calendar->setSelectedDate(QDate(2026, 9, 7)); // 仍可由代码设置
```

范围只能表达连续日期。周末不可选、节假日不可选、容量已满日期不可选等业务规则，仍要由业务层校验；可以用 `setDateTextFormat()` 把这些日期标红或弱化，但颜色不是安全约束。

## 5. 选择、点击、确认和翻页信号

| 信号 | 触发条件 | 适合做什么 |
| --- | --- | --- |
| `selectionChanged()` | `selectedDate` 改变，用户操作和 `setSelectedDate()` 都会触发。 | 更新依赖日期的预览、表单状态。 |
| `clicked(QDate)` | 用户用鼠标点击了范围内有效日期；`NoSelection` 时不发出。 | 单击即预览或显示当天详情。 |
| `activated(QDate)` | 用户双击日期，或按 Enter / Return。 | 把日期视为“确认”，关闭选择面板或执行跳转。 |
| `currentPageChanged(int year, int month)` | 当前展示的月份变化。 | 延迟加载该月的任务、节假日或可用性标记。 |

```cpp
connect(calendar, &QCalendarWidget::selectionChanged, this,
        [calendar, this] {
            updatePreview(calendar->selectedDate());
        });

connect(calendar, &QCalendarWidget::activated, this,
        [calendar, this](QDate date) {
            openSchedule(date);
        });
```

不要把 `selectionChanged()` 当作“用户确认”的信号，它也会在程序初始化 `setSelectedDate()` 时发出。相反，`activated()` 明确表达用户的确认动作。

## 6. 外观标记：用 QTextCharFormat，但别把它当作任意 CSS

`QCalendarWidget` 用 `QTextCharFormat` 设置三类样式：

```cpp
QTextCharFormat holiday;
holiday.setForeground(Qt::red);
holiday.setFontWeight(QFont::Bold);

calendar->setDateTextFormat(QDate(2026, 10, 1), holiday);
```

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 日期样式 | `setDateTextFormat(QDate, QTextCharFormat)` | 给某一个具体日期设置显示格式 | 适合节假日、截止日、已满日期等单日标记；传空 `QDate()` 可清除全部单日格式 |
| 星期样式 | `setWeekdayTextFormat(Qt::DayOfWeek, QTextCharFormat)` | 给每周固定某一天设置显示格式 | 适合周末或固定休息日；星期格式的前景和背景色会优先于头部格式 |
| 表头样式 | `setHeaderTextFormat(QTextCharFormat)` | 设置顶部月份、年份和表头的基础格式 | 只影响月历支持的文本格式属性，不要把 `QTextCharFormat` 当成完整 CSS |

月历只使用 `QTextCharFormat` 的前景色、背景色和字体属性来绘制单元格；不应期待它完整支持富文本效果。星期格式的前景和背景色优先于头部格式的同类颜色，其他文本属性仍由头部格式决定。

`dateTextFormat()` 可取得所有被单独标记的日期映射或单日格式。传空 `QDate()` 给 `setDateTextFormat()` 会清除全部单日格式，适合刷新整个月的服务端状态后重新标记。

## 7. 导航栏、表头与键盘内嵌日期编辑

默认月历使用短星期名、显示 ISO 周数、首列按当前日历区域设置的一周起始日决定，且不显示格线。以下 API 用来调整它：

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 日期排列 | `setFirstDayOfWeek(Qt::DayOfWeek)` | 指定月历第一列从星期几开始 | 用于固定跨系统一致的列顺序；不设置时受 locale 和日历环境影响 |
| 表头显示 | `setHorizontalHeaderFormat(HorizontalHeaderFormat)` | 控制星期标题显示为单字母、短名、全名或隐藏 | 只改变顶部星期标题，不改变日期选择范围 |
| 表头显示 | `setVerticalHeaderFormat(VerticalHeaderFormat)` | 控制左侧垂直表头，例如 ISO 周数或隐藏 | 显示周数时要确认业务采用的周定义，避免和本地习惯不一致 |
| 网格显示 | `setGridVisible(bool)` | 控制日期单元格之间是否绘制格线 | 适合需要表格感的排班、预约、统计场景；只是视觉效果 |
| 导航显示 | `setNavigationBarVisible(bool)` | 显示或隐藏顶部月份、年份与前后月导航控件 | 纯展示或受控跳转场景可隐藏；隐藏后仍可通过 API 改变显示月份 |

`dateEditEnabled` 是一个不太显眼但有用的键盘能力：当月历本身有焦点时，按非修饰键会弹出一个按当前 locale 编辑日期的小型编辑器。它默认开启；`dateEditAcceptDelay` 默认 1500 毫秒，表示用户停止输入多久后接受日期并关闭这个编辑器。

对于纯展示日历，可关闭这项能力和导航栏：

```cpp
calendar->setSelectionMode(QCalendarWidget::NoSelection);
calendar->setDateEditEnabled(false);
calendar->setNavigationBarVisible(false);
```

## 8. 自定义绘制：优先 `paintCell()`，按需刷新

要绘制任务圆点、容量角标或不规则背景，可继承 `QCalendarWidget` 并重写受保护的 `paintCell()`：

```cpp
class ScheduleCalendar final : public QCalendarWidget
{
protected:
    void paintCell(QPainter *painter, const QRect &rect,
                   QDate date) const override
    {
        QCalendarWidget::paintCell(painter, rect, date);

        if (busyDates.contains(date)) {
            painter->save();
            painter->setBrush(Qt::red);
            painter->setPen(Qt::NoPen);
            painter->drawEllipse(rect.bottomRight() - QPoint(7, 7), 4, 4);
            painter->restore();
        }
    }

private:
    QSet<QDate> busyDates;
};
```

重写时先调用 `QCalendarWidget::paintCell()`，保留主题、禁用状态、选中状态和可访问性相关绘制，再叠加自己的标记。数据只影响一个日期时调用 `updateCell(date)`；整批状态改变时调用 `updateCells()`。不要在 `paintCell()` 中发请求、修改模型或改变选中日期，绘制会被频繁调用。

## API 速查表
### 9.1 枚举与显示策略

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 类型 | `HorizontalHeaderFormat` | 定义星期标题栏的显示策略。 | 通过 `setHorizontalHeaderFormat()` 设置。 |
| 枚举值 | `NoHorizontalHeader` | 隐藏星期标题栏。 | 适合空间很紧或外部已经有星期说明的界面。 |
| 枚举值 | `SingleLetterDayNames` | 用单个字母显示星期名。 | 极窄布局可用；中文界面通常不如短名称直观。 |
| 枚举值 | `ShortDayNames` | 用本地化简称显示星期名。 | 常见默认选择，信息密度和可读性比较平衡。 |
| 枚举值 | `LongDayNames` | 用完整名称显示星期名。 | 宽界面或可访问性优先时更清楚。 |
| 类型 | `SelectionMode` | 定义用户是否可以选择日期。 | 本类只有无选择和单选择，不支持日期范围多选。 |
| 枚举值 | `NoSelection` | 禁止用户通过鼠标和键盘选择日期。 | 程序仍可以调用 `setSelectedDate()` 设置选中日期。 |
| 枚举值 | `SingleSelection` | 允许用户选择一个日期。 | 默认模式，适合日期选择表单。 |
| 类型 | `VerticalHeaderFormat` | 定义左侧周数栏的显示策略。 | 通过 `setVerticalHeaderFormat()` 设置。 |
| 枚举值 | `ISOWeekNumbers` | 显示 ISO 周数。 | 项目排期、生产计划等按周查看的场景有用。 |
| 枚举值 | `NoVerticalHeader` | 隐藏周数栏。 | 普通消费者日历通常更简洁。 |

### 9.2 状态、范围与格式 API

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 选中状态 | `selectedDate() const` / `setSelectedDate(QDate date)` | 读取或设置业务上真正选中的日期。 | 日期必须在有效范围内；设置后会触发 `selectionChanged()`。 |
| 选择模式 | `selectionMode() const` / `setSelectionMode(SelectionMode mode)` | 读取或设置用户是否能选择日期。 | `NoSelection` 只禁止用户操作，不会清掉已有 `selectedDate`。 |
| 日期下限 | `minimumDate() const` / `setMinimumDate(QDate date)` / `clearMinimumDate()` | 管理最早可选日期。 | 无效日期设置不会生效；改变边界可能连带调整最大日期和选中日期。 |
| 日期上限 | `maximumDate() const` / `setMaximumDate(QDate date)` / `clearMaximumDate()` | 管理最晚可选日期。 | 与最小日期共同形成连续可选范围。 |
| 日期范围 | `setDateRange(QDate min, QDate max)` | 一次设置最小和最大日期。 | 只能表达连续范围，不能直接表达周末或节假日禁选。 |
| 日历系统 | `calendar() const` / `setCalendar(QCalendar calendar)` | 读取或设置日历规则系统。 | 默认是公历；改变的是日期规则和显示，不是控件类型。 |
| 周起始日 | `firstDayOfWeek() const` / `setFirstDayOfWeek(Qt::DayOfWeek dayOfWeek)` | 读取或设置月历第一列星期。 | 跨地区产品最好明确设置，避免系统区域设置造成列顺序不同。 |
| 网格 | `isGridVisible() const` / `setGridVisible(bool show)` | 查询或开关日期格线。 | 默认通常不显示；排班和密集业务日历常开启。 |
| 星期标题 | `horizontalHeaderFormat() const` / `setHorizontalHeaderFormat(HorizontalHeaderFormat format)` | 查询或设置星期标题显示方式。 | 需要结合语言、宽度和可访问性选择。 |
| 周数栏 | `verticalHeaderFormat() const` / `setVerticalHeaderFormat(VerticalHeaderFormat format)` | 查询或设置左侧周数栏。 | ISO 周数适合项目、生产和排期界面。 |
| 导航栏 | `isNavigationBarVisible() const` / `setNavigationBarVisible(bool visible)` | 查询或开关顶部月份/年份导航。 | 隐藏后仍可通过代码和翻页槽导航。 |
| 内嵌编辑 | `isDateEditEnabled() const` / `setDateEditEnabled(bool enable)` | 控制键盘输入日期时是否弹出内嵌编辑器。 | 只读展示通常关闭；需要键盘快速输入时保留。 |
| 内嵌编辑 | `dateEditAcceptDelay() const` / `setDateEditAcceptDelay(int delay)` | 查询或设置内嵌日期编辑器停止输入后的接受延迟。 | 单位是毫秒；只在 date edit 开启时有意义。 |
| 表头格式 | `headerTextFormat() const` / `setHeaderTextFormat(const QTextCharFormat &format)` | 设置月份、年份和表头的基础字体/颜色格式。 | 星期格式的前景和背景可能覆盖这里的同类设置。 |
| 星期格式 | `weekdayTextFormat(Qt::DayOfWeek dayOfWeek) const` / `setWeekdayTextFormat(...)` | 设置某个星期几的文本格式。 | 常用于周末、固定休息日或值班日标记。 |
| 日期格式 | `dateTextFormat() const` / `dateTextFormat(QDate date) const` / `setDateTextFormat(...)` | 查询或设置特殊日期的字体、前景和背景。 | 传空日期给 setter 可清除全部单日格式；颜色标记不等于业务禁选。 |

### 9.3 页面、导航与尺寸 API

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QCalendarWidget(QWidget *parent = nullptr)` | 创建可嵌入窗口的月历控件。 | 初始页面和选中日期由控件初始化；通常放进布局。 |
| 析构 | `~QCalendarWidget()` | 销毁月历控件。 | 一般由父对象或页面容器负责生命周期。 |
| 浏览状态 | `monthShown() const` / `yearShown() const` | 查询当前正在显示的月份和年份。 | 与 `selectedDate()` 分离，浏览月份不会自动改业务选中值。 |
| 翻页 | `setCurrentPage(int year, int month)` | 直接跳到指定年月。 | 只改变展示页面，不改变选中日期。 |
| 翻页 | `showNextMonth()` / `showPreviousMonth()` | 向前或向后浏览一个月。 | 只改变展示页面。 |
| 翻页 | `showNextYear()` / `showPreviousYear()` | 向前或向后浏览一年。 | 当前月份保持不变。 |
| 回到选中 | `showSelectedDate()` | 把页面翻回选中日期所在月份。 | 适合用户浏览很远月份后回到业务日期。 |
| 回到今天 | `showToday()` | 把页面翻到今天所在月份。 | 不会自动把 selectedDate 改成今天。 |
| 尺寸 | `minimumSizeHint() const` / `sizeHint() const` | 返回布局系统参考的最小尺寸和推荐尺寸。 | 一般交给布局，不要固定写死几何。 |

### 9.4 信号与扩展 API

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 信号 | `selectionChanged()` | 选中日期变化时通知。 | 用户操作和程序调用 `setSelectedDate()` 都会触发，不能当作用户确认信号。 |
| 信号 | `clicked(QDate date)` | 用户鼠标点击有效日期时通知。 | `NoSelection` 或范围外日期不会触发。 |
| 信号 | `activated(QDate date)` | 用户双击日期或按 Enter/Return 时通知。 | 更适合表达“确认选择”或打开当天详情。 |
| 信号 | `currentPageChanged(int year, int month)` | 当前展示月份变化时通知。 | 适合按月懒加载事件、节假日或容量状态。 |
| 绘制 | `paintCell(QPainter *painter, const QRect &rect, QDate date) const` | 绘制单个日期单元格的保护虚函数。 | 先调用基类保留主题、禁用和选中态，再叠加业务标记。 |
| 刷新 | `updateCell(QDate date)` | 请求刷新某一个日期单元格。 | 单日状态变化时比整月刷新更轻量。 |
| 刷新 | `updateCells()` | 请求刷新所有日期单元格。 | 批量状态改变时使用，避免高频重复调用。 |
| 事件 | `event(QEvent *event)` / `eventFilter(QObject *watched, QEvent *event)` | 处理月历事件和内部事件过滤。 | 普通使用不需要碰，派生时保留基类行为。 |
| 事件 | `keyPressEvent(...)` / `mousePressEvent(...)` / `resizeEvent(...)` | 扩展键盘、鼠标和尺寸变化行为。 | 自定义交互时重写，并处理好默认导航和选择逻辑。 |

---

### 一句话总结

`QCalendarWidget` 是一块可嵌入的单日期月历：业务值看 `selectedDate()`，浏览状态看 `monthShown()` / `yearShown()`；用 `activated()` 表示确认，用 `paintCell()` 叠加日历业务标记。
