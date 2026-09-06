# QCalendar

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“Calendar”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QCalendar` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QCalendar>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

### 状态、生命周期和线程

**生命周期：** 先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

**状态与结果：** 把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

**线程与事件循环：** 如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

## 3. 直接使用

围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `(since 6.2) class SystemId`
- `enum class System { Gregorian, Julian, Milankovic, Jalali, IslamicCivil }`

### 公有函数

- `QCalendar()`
- `QCalendar(QAnyStringView name)`
- `QCalendar(QCalendar::System system)`
- `(since 6.2) QCalendar(QCalendar::SystemId id)`
- `QDate dateFromParts(const QCalendar::YearMonthDay &parts) const`
- `QDate dateFromParts(int year, int month, int day) const`
- `QString dateTimeToString(QStringView format, const QDateTime &datetime, QDate dateOnly, QTime timeOnly, const QLocale &locale) const`
- `int dayOfWeek(QDate date) const`
- `int daysInMonth(int month, int year = Unspecified) const`
- `int daysInYear(int year) const`
- `bool hasYearZero() const`
- `bool isDateValid(int year, int month, int day) const`
- `bool isGregorian() const`
- `bool isLeapYear(int year) const`
- `bool isLunar() const`
- `bool isLuniSolar() const`
- `bool isProleptic() const`
- `bool isSolar() const`
- `bool isValid() const`
- `(since 6.7) QDate matchCenturyToWeekday(const QCalendar::YearMonthDay &parts, int dow) const`
- `int maximumDaysInMonth() const`
- `int maximumMonthsInYear() const`
- `int minimumDaysInMonth() const`
- `QString monthName(const QLocale &locale, int month, int year = Unspecified, QLocale::FormatType format = QLocale::LongFormat) const`
- `int monthsInYear(int year) const`
- `QString name() const`
- `QCalendar::YearMonthDay partsFromDate(QDate date) const`
- `QString standaloneMonthName(const QLocale &locale, int month, int year = Unspecified, QLocale::FormatType format = QLocale::LongFormat) const`
- `QString standaloneWeekDayName(const QLocale &locale, int day, QLocale::FormatType format = QLocale::LongFormat) const`
- `QString weekDayName(const QLocale &locale, int day, QLocale::FormatType format = QLocale::LongFormat) const`

### 静态公有成员

- `QStringList availableCalendars()`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 33 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum class QCalendar::System`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QCalendar` 暴露的类型声明 `class`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:System`。
- 属性名：`QCalendar`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QCalendar::QCalendar(QAnyStringView name)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QCalendar` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `name`：类型为 `QAnyStringView`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit, since 6.2] QCalendar::QCalendar(QCalendar::SystemId id)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QCalendar` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `id`：类型为 `QCalendar::SystemId`。没有默认值，调用时必须提供。传入 `QCalendar::SystemId` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QStringList QCalendar::availableCalendars()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `availableCalendars`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QStringList`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDate QCalendar::dateFromParts(const QCalendar::YearMonthDay &parts) const`

**API 类别：** 成员函数说明

**中文解读：** `QCalendar::dateFromParts` 用于计算、查询或取得与“日期、转换进入、Parts”相关的操作。调用时要先确认当前状态和 `parts` 的有效范围；返回类型是 `QDate`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDate`。
- 参数 `parts`：类型为 `const QCalendar::YearMonthDay &`。没有默认值，调用时必须提供。传入 `const QCalendar::YearMonthDay &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QCalendar::dateTimeToString(QStringView format, const QDateTime &datetime, QDate dateOnly, QTime timeOnly, const QLocale &locale) const`

**API 类别：** 成员函数说明

**中文解读：** `QCalendar::dateTimeToString` 用于计算、查询或取得与“日期、时间、转换输出、字符串”相关的操作。调用时要先确认当前状态和 `format`、`datetime`、`dateOnly`、`timeOnly`、`locale` 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数 `format`：类型为 `QStringView`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。
- 参数 `datetime`：类型为 `const QDateTime &`。没有默认值，调用时必须提供。传入 `const QDateTime &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `dateOnly`：类型为 `QDate`。没有默认值，调用时必须提供。传入 `QDate` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `timeOnly`：类型为 `QTime`。没有默认值，调用时必须提供。传入 `QTime` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `locale`：类型为 `const QLocale &`。没有默认值，调用时必须提供。传入 `const QLocale &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QCalendar::dayOfWeek(QDate date) const`

**API 类别：** 成员函数说明

**中文解读：** `QCalendar::dayOfWeek` 用于计算、查询或取得与“天、Of、Week”相关的操作。调用时要先确认当前状态和 `date` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `date`：类型为 `QDate`。没有默认值，调用时必须提供。传入 `QDate` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QCalendar::daysInMonth(int month, int year = Unspecified) const`

**API 类别：** 成员函数说明

**中文解读：** `QCalendar::daysInMonth` 用于计算、查询或取得与“天数、In、月”相关的操作。调用时要先确认当前状态和 `month`、`year` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `month`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `year`：类型为 `int`。默认值为 `Unspecified`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QCalendar::daysInYear(int year) const`

**API 类别：** 成员函数说明

**中文解读：** `QCalendar::daysInYear` 用于计算、查询或取得与“天数、In、年”相关的操作。调用时要先确认当前状态和 `year` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `year`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QCalendar::hasYearZero() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `hasYearZero`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QCalendar::isDateValid(int year, int month, int day) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isDateValid`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `year`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `month`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `day`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QCalendar::isGregorian() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isGregorian`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QCalendar::isLeapYear(int year) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isLeapYear`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `year`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QCalendar::isLunar() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isLunar`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QCalendar::isLuniSolar() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isLuniSolar`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QCalendar::isProleptic() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isProleptic`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QCalendar::isSolar() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isSolar`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QCalendar::isValid() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isValid`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.7] QDate QCalendar::matchCenturyToWeekday(const QCalendar::YearMonthDay &parts, int dow) const`

**API 类别：** 成员函数说明

**中文解读：** `QCalendar::matchCenturyToWeekday` 用于计算、查询或取得与“匹配、Century、转换输出、Weekday”相关的操作。调用时要先确认当前状态和 `parts`、`dow` 的有效范围；返回类型是 `QDate`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDate`。
- 参数 `parts`：类型为 `const QCalendar::YearMonthDay &`。没有默认值，调用时必须提供。传入 `const QCalendar::YearMonthDay &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `dow`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QCalendar::maximumDaysInMonth() const`

**API 类别：** 成员函数说明

**中文解读：** `QCalendar::maximumDaysInMonth` 用于计算、查询或取得与“最大值、天数、In、月”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QCalendar::maximumMonthsInYear() const`

**API 类别：** 成员函数说明

**中文解读：** `QCalendar::maximumMonthsInYear` 用于计算、查询或取得与“最大值、月数、In、年”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QCalendar::minimumDaysInMonth() const`

**API 类别：** 成员函数说明

**中文解读：** `QCalendar::minimumDaysInMonth` 用于计算、查询或取得与“最小值、天数、In、月”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QCalendar::monthName(const QLocale &locale, int month, int year = Unspecified, QLocale::FormatType format = QLocale::LongFormat) const`

**API 类别：** 成员函数说明

**中文解读：** `QCalendar::monthName` 用于计算、查询或取得与“月、名称”相关的操作。调用时要先确认当前状态和 `locale`、`month`、`year`、`format` 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数 `locale`：类型为 `const QLocale &`。没有默认值，调用时必须提供。传入 `const QLocale &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `month`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `year`：类型为 `int`。默认值为 `Unspecified`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `format`：类型为 `QLocale::FormatType`。默认值为 `QLocale::LongFormat`。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QCalendar::monthsInYear(int year) const`

**API 类别：** 成员函数说明

**中文解读：** `QCalendar::monthsInYear` 用于计算、查询或取得与“月数、In、年”相关的操作。调用时要先确认当前状态和 `year` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `year`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QCalendar::name() const`

**API 类别：** 成员函数说明

**中文解读：** `QCalendar::name` 用于计算、查询或取得与“名称”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCalendar::YearMonthDay QCalendar::partsFromDate(QDate date) const`

**API 类别：** 成员函数说明

**中文解读：** `QCalendar::partsFromDate` 用于计算、查询或取得与“parts、转换进入、日期”相关的操作。调用时要先确认当前状态和 `date` 的有效范围；返回类型是 `QCalendar::YearMonthDay`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCalendar::YearMonthDay`。
- 参数 `date`：类型为 `QDate`。没有默认值，调用时必须提供。传入 `QDate` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QCalendar::standaloneMonthName(const QLocale &locale, int month, int year = Unspecified, QLocale::FormatType format = QLocale::LongFormat) const`

**API 类别：** 成员函数说明

**中文解读：** `QCalendar::standaloneMonthName` 用于计算、查询或取得与“standalone、月、名称”相关的操作。调用时要先确认当前状态和 `locale`、`month`、`year`、`format` 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数 `locale`：类型为 `const QLocale &`。没有默认值，调用时必须提供。传入 `const QLocale &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `month`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `year`：类型为 `int`。默认值为 `Unspecified`。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `format`：类型为 `QLocale::FormatType`。默认值为 `QLocale::LongFormat`。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QCalendar::standaloneWeekDayName(const QLocale &locale, int day, QLocale::FormatType format = QLocale::LongFormat) const`

**API 类别：** 成员函数说明

**中文解读：** `QCalendar::standaloneWeekDayName` 用于计算、查询或取得与“standalone、Week、天、名称”相关的操作。调用时要先确认当前状态和 `locale`、`day`、`format` 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数 `locale`：类型为 `const QLocale &`。没有默认值，调用时必须提供。传入 `const QLocale &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `day`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `format`：类型为 `QLocale::FormatType`。默认值为 `QLocale::LongFormat`。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QCalendar::weekDayName(const QLocale &locale, int day, QLocale::FormatType format = QLocale::LongFormat) const`

**API 类别：** 成员函数说明

**中文解读：** `QCalendar::weekDayName` 用于计算、查询或取得与“week、天、名称”相关的操作。调用时要先确认当前状态和 `locale`、`day`、`format` 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数 `locale`：类型为 `const QLocale &`。没有默认值，调用时必须提供。传入 `const QLocale &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `day`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `format`：类型为 `QLocale::FormatType`。默认值为 `QLocale::LongFormat`。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.2) class SystemId`

**API 类别：** 公有类型

**中文解读：** 这是 `QCalendar` 暴露的类型声明 `System、Id`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCalendar()`

**API 类别：** 公有函数

**中文解读：** 这是 `QCalendar` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCalendar(QCalendar::System system)`

**API 类别：** 公有函数

**中文解读：** 这是 `QCalendar` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `system`：类型为 `QCalendar::System`。没有默认值，调用时必须提供。传入 `QCalendar::System` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDate dateFromParts(int year, int month, int day) const`

**API 类别：** 公有函数

**中文解读：** `QCalendar::dateFromParts` 用于计算、查询或取得与“日期、转换进入、Parts”相关的操作。调用时要先确认当前状态和 `year`、`month`、`day` 的有效范围；返回类型是 `QDate`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDate`。
- 参数 `year`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `month`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `day`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

### 状态和错误边界

把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

### 线程边界

如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

### 最容易出现的错误

不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QCalendar` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
