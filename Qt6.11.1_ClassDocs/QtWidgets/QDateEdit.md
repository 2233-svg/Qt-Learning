# QDateEdit

> Qt 6.11.1 · Qt Widgets · 来自 `QDateEdit`

## 1. 先建立直觉

`QDateEdit` 是只编辑日期的 `QDateTimeEdit`。它适合生日、截止日期、报表日期、有效期开始/结束这类不关心具体时刻的输入。

如果需要同时编辑日期和时间，用 `QDateTimeEdit`；如果只需要在月历中点选日期，用 `QCalendarWidget` 或开启日历弹窗。

## 2. 类说明

- 头文件：`#include <QDateEdit>`
- 模块：`Qt6::Widgets`
- 继承自：`QDateTimeEdit`
- 直接派生类：类页未列出

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

它继承父类的显示格式、日期范围、日历弹窗、验证、步进和 `dateChanged()` 信号，并新增用户修改信号。

## 3. API 速查

| API | 用途速查 |
| --- | --- |
| `QDateEdit(parent)` | 创建日期编辑器。 |
| `QDateEdit(date, parent)` | 用初始日期创建日期编辑器。 |
| `setDate()` / `date()` | 继承自 `QDateTimeEdit`，设置或读取日期。 |
| `setDateRange()` | 设置可输入日期范围。 |
| `setDisplayFormat()` | 设置日期显示和解析格式。 |
| `setCalendarPopup()` | 开启下拉日历。 |
| `userDateChanged(date)` | 仅用户实际修改日期时发出。 |

## 4. 关键用法

`QDateEdit` 最常见组合是设置格式、范围和初值：

```cpp
auto *edit = new QDateEdit(QDate::currentDate(), this);
edit->setDisplayFormat("yyyy-MM-dd");
edit->setCalendarPopup(true);
edit->setDateRange(QDate(2000, 1, 1), QDate(2099, 12, 31));
```

`dateChanged()` 会在程序调用 `setDate()` 时触发；`userDateChanged()` 只关心用户操作，适合驱动“用户已修改”标记。

## 5. 常见坑与经验

- 日期不含时区和具体时间，不要用它表示瞬间时间戳。
- 范围变化可能会把当前日期夹到边界上。
- `displayFormat` 应符合用户所在地区或业务标准。
- 开启日历弹窗时仍要测试键盘输入路径。
