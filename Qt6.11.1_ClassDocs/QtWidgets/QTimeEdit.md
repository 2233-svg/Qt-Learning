# QTimeEdit

> Qt 6.11.1 · Qt Widgets · 来自 `QTimeEdit`

## 1. 先建立直觉

`QTimeEdit` 是只编辑一天中时间的 `QDateTimeEdit`。它适合提醒时间、营业时间、持续时间的时分秒输入、任务每天执行时间等场景。

它表示的是 `QTime`，也就是一天内的时间，不包含日期和时区。需要跨日期或具体瞬间时，用 `QDateTimeEdit` 和清晰的时区策略。

## 2. 类说明

- 头文件：`#include <QTimeEdit>`
- 模块：`Qt6::Widgets`
- 继承自：`QDateTimeEdit`
- 直接派生类：类页未列出

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

它继承父类的显示格式、时间范围、section 编辑、验证、步进和 `timeChanged()` 信号，并新增用户修改信号。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QTimeEdit(parent)` | 创建时间编辑器。 |
| `QTimeEdit(time, parent)` | 用初始时间创建时间编辑器。 |
| `setTime()` / `time()` | 继承自 `QDateTimeEdit`，设置或读取时间。 |
| `setTimeRange()` | 设置可输入时间范围。 |
| `setDisplayFormat()` | 设置时间显示和解析格式，如 `HH:mm:ss`。 |
| `setCurrentSection()` | 让用户直接编辑小时、分钟或秒。 |
| `userTimeChanged(time)` | 仅用户实际修改时间时发出。 |

## 4. 关键用法

时间输入通常要明确精度。只需要小时和分钟，就把格式设为 `HH:mm`；需要秒再显示秒。显示多余 section 会让用户以为业务也关心它。

```cpp
auto *edit = new QTimeEdit(QTime::currentTime(), this);
edit->setDisplayFormat("HH:mm");
edit->setTimeRange(QTime(8, 0), QTime(18, 0));
```

和日期控件一样，`timeChanged()` 对程序设置也触发；只关注用户编辑时连接 `userTimeChanged()`。

## 5. 常见坑与经验

- `QTime` 不包含日期，不能表达“今晚 23:00 到明天 01:00”这种跨日区间的完整语义。
- 12 小时制要处理 AM/PM section，避免只显示 `hh:mm` 却没有上下文。
- 鼠标滚轮可能误改当前 section，复杂表单里要测试焦点和滚动体验。
- 时间范围只约束一天内值，不代表业务日历上的可用时段。
