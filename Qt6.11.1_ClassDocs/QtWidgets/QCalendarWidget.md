# QCalendarWidget

> Qt 6.11.1 · Qt Widgets · 来自 `QCalendarWidget`

## 1. 先建立直觉

`QCalendarWidget` 是月历选择控件，用来显示某个月、切换年月、选择单个日期，并可对日期文字做格式标记。它适合日期选择、简单日程提示、报表日期跳转、生日/截止日期选择。

它不是完整日程系统：不内置多选范围、事件布局、拖拽日程块或资源日历。复杂日历应用通常需要自定义绘制或专门控件。

## 2. 类说明

- 头文件：`#include <QCalendarWidget>`
- 模块：`Qt6::Widgets`
- 继承自：`QWidget`
- 直接派生类：类页未列出

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

它可单独使用，也可作为 `QDateTimeEdit` 的弹出日历。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QCalendarWidget(parent)` | 创建日历控件。 |
| `setSelectedDate()` / `selectedDate()` | 设置或读取当前选中日期。 |
| `setDateRange()` | 设置可选日期范围。 |
| `setMinimumDate()` / `setMaximumDate()` | 设置最小/最大日期。 |
| `clearMinimumDate()` / `clearMaximumDate()` | Qt 6.6 起恢复默认边界。 |
| `setCurrentPage(year, month)` | 切换当前显示年月。 |
| `yearShown()` / `monthShown()` | 当前页面年月。 |
| `showToday()` / `showSelectedDate()` | 跳到今天或选中日期所在页。 |
| `showNextMonth()` / `showPreviousMonth()` | 切换月份。 |
| `showNextYear()` / `showPreviousYear()` | 切换年份。 |
| `setSelectionMode()` / `selectionMode()` | 是否允许选择日期。 |
| `setGridVisible()` / `isGridVisible()` | 显示或隐藏日期网格。 |
| `setNavigationBarVisible()` | 显示或隐藏顶部导航栏。 |
| `setFirstDayOfWeek()` / `firstDayOfWeek()` | 设置每周第一天。 |
| `setHorizontalHeaderFormat()` | 设置星期标题显示方式。 |
| `setVerticalHeaderFormat()` | 显示 ISO 周数或隐藏垂直头。 |
| `setDateEditEnabled()` | 是否允许键盘快速输入日期。 |
| `setDateEditAcceptDelay()` | 快速输入日期后的接受延迟。 |
| `setCalendar()` / `calendar()` | 设置日历系统。 |
| `setDateTextFormat()` / `dateTextFormat()` | 给特定日期设置文本格式。 |
| `setWeekdayTextFormat()` / `weekdayTextFormat()` | 给星期几设置文本格式。 |
| `setHeaderTextFormat()` / `headerTextFormat()` | 设置表头文本格式。 |
| `activated(date)` | 用户激活日期，通常双击或回车。 |
| `clicked(date)` | 用户点击日期。 |
| `selectionChanged()` | 选中日期变化。 |
| `currentPageChanged(year, month)` | 当前页面年月变化。 |
| `paintCell()` | 子类化自定义日期单元格绘制。 |
| `updateCell()` / `updateCells()` | 请求更新某日或全部日期单元格。 |

## 4. 关键用法

### 日期范围是第一层业务约束

订票、报表、截止日期等场景应先设置 `minimumDate` 和 `maximumDate`。用户不能选择范围外日期，程序设置选中日期时也会被边界影响。范围外日期的业务含义不要只靠颜色暗示。

### 格式标记适合轻量提示

`setDateTextFormat()` 可以给某一天改字体、颜色、背景，适合标记节假日、已有记录、今天之外的特殊日期。若要在一天里显示多个事件标题，单靠 text format 不够，应重写 `paintCell()` 或做自定义日历视图。

### `clicked` 和 `activated` 语义不同

`clicked(date)` 是点到某天就发出；`activated(date)` 更像“确认这个日期”。如果点击只用于预览，而双击/回车才执行跳转或关闭对话框，两个信号要分开使用。

### 周起始和周数是本地化问题

`firstDayOfWeek` 和 `ISOWeekNumbers` 会影响用户理解。国际应用应尊重 locale 或用户设置，不要固定假设周日或周一开头。

### 自定义绘制保留可读性

重写 `paintCell()` 时，不要只画自定义背景而丢掉选中、今天、禁用状态。通常先调用基类绘制，再叠加标记，或完整处理所有状态。

## 5. 常见坑与经验

- `QCalendarWidget` 默认只支持单选，不提供日期范围多选。
- `dateTextFormat` 适合少量特殊日期，大量动态事件要注意更新成本。
- 隐藏导航栏后要给用户其他切换年月的方式。
- 键盘 date edit 功能会在控件有焦点时响应数字输入，表单里要测试焦点体验。
- 复杂日程日历不要硬塞进这个控件，早做专门设计。
