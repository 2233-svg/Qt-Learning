# QCalendarWidget

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QCalendarWidget` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QCalendarWidget` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QCalendarWidget>`
- 继承自：QWidget
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

### 状态、生命周期和线程

**生命周期：** 控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

**状态与结果：** 控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

**线程与事件循环：** 所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

## 3. 直接使用

需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。 使用时通常按这个过程组织：创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum HorizontalHeaderFormat { SingleLetterDayNames, ShortDayNames, LongDayNames, NoHorizontalHeader }`
- `enum SelectionMode { NoSelection, SingleSelection }`
- `enum VerticalHeaderFormat { ISOWeekNumbers, NoVerticalHeader }`

### 属性

- `dateEditAcceptDelay : int`
- `dateEditEnabled : bool`
- `firstDayOfWeek : Qt::DayOfWeek`
- `gridVisible : bool`
- `horizontalHeaderFormat : HorizontalHeaderFormat`
- `maximumDate : QDate`
- `minimumDate : QDate`
- `navigationBarVisible : bool`
- `selectedDate : QDate`
- `selectionMode : SelectionMode`
- `verticalHeaderFormat : VerticalHeaderFormat`

### 公有函数

- `QCalendarWidget(QWidget *parent = nullptr)`
- `virtual ~QCalendarWidget()`
- `QCalendar calendar() const`
- `void clearMaximumDate()`
- `void clearMinimumDate()`
- `int dateEditAcceptDelay() const`
- `QMap<QDate, QTextCharFormat> dateTextFormat() const`
- `QTextCharFormat dateTextFormat(QDate date) const`
- `Qt::DayOfWeek firstDayOfWeek() const`
- `QTextCharFormat headerTextFormat() const`
- `QCalendarWidget::HorizontalHeaderFormat horizontalHeaderFormat() const`
- `bool isDateEditEnabled() const`
- `bool isGridVisible() const`
- `bool isNavigationBarVisible() const`
- `QDate maximumDate() const`
- `QDate minimumDate() const`
- `int monthShown() const`
- `QDate selectedDate() const`
- `QCalendarWidget::SelectionMode selectionMode() const`
- `void setCalendar(QCalendar c)`
- `void setDateEditAcceptDelay(int delay)`
- `void setDateEditEnabled(bool enable)`
- `void setDateTextFormat(QDate date, const QTextCharFormat &format)`
- `void setFirstDayOfWeek(Qt::DayOfWeek dayOfWeek)`
- `void setHeaderTextFormat(const QTextCharFormat &format)`
- `void setHorizontalHeaderFormat(QCalendarWidget::HorizontalHeaderFormat format)`
- `void setMaximumDate(QDate date)`
- `void setMinimumDate(QDate date)`
- `void setSelectionMode(QCalendarWidget::SelectionMode mode)`
- `void setVerticalHeaderFormat(QCalendarWidget::VerticalHeaderFormat format)`
- `void setWeekdayTextFormat(Qt::DayOfWeek dayOfWeek, const QTextCharFormat &format)`
- `QCalendarWidget::VerticalHeaderFormat verticalHeaderFormat() const`
- `QTextCharFormat weekdayTextFormat(Qt::DayOfWeek dayOfWeek) const`
- `int yearShown() const`

### 重实现的公有函数

- `virtual QSize minimumSizeHint() const override`
- `virtual QSize sizeHint() const override`

### 公有槽函数

- `void setCurrentPage(int year, int month)`
- `void setDateRange(QDate min, QDate max)`
- `void setGridVisible(bool show)`
- `void setNavigationBarVisible(bool visible)`
- `void setSelectedDate(QDate date)`
- `void showNextMonth()`
- `void showNextYear()`
- `void showPreviousMonth()`
- `void showPreviousYear()`
- `void showSelectedDate()`
- `void showToday()`

### 信号

- `void activated(QDate date)`
- `void clicked(QDate date)`
- `void currentPageChanged(int year, int month)`
- `void selectionChanged()`

### 保护函数

- `virtual void paintCell(QPainter *painter, const QRect &rect, QDate date) const`
- `void updateCell(QDate date)`
- `void updateCells()`

### 重实现的保护函数

- `virtual bool event(QEvent *event) override`
- `virtual bool eventFilter(QObject *watched, QEvent *event) override`
- `virtual void keyPressEvent(QKeyEvent *event) override`
- `virtual void mousePressEvent(QMouseEvent *event) override`
- `virtual void resizeEvent(QResizeEvent *event) override`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 73 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QCalendarWidget::HorizontalHeaderFormat`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QCalendarWidget` 暴露的类型声明 `水平、Header、格式化`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:HorizontalHeaderFormat`。
- 属性名：`QCalendarWidget`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QCalendarWidget::SelectionMode`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QCalendarWidget` 暴露的类型声明 `Selection、模式`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:SelectionMode`。
- 属性名：`QCalendarWidget`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QCalendarWidget::VerticalHeaderFormat`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QCalendarWidget` 暴露的类型声明 `垂直、Header、格式化`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:VerticalHeaderFormat`。
- 属性名：`QCalendarWidget`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `dateEditAcceptDelay : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QCalendarWidget` 的配置属性。初始化或状态切换时通过 `setDateEditAcceptDelay(...)` 设置，之后用 `dateEditAcceptDelay()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`dateEditAcceptDelay`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `dateEditEnabled : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QCalendarWidget` 的配置属性。初始化或状态切换时通过 `setDateEditEnabled(...)` 设置，之后用 `dateEditEnabled()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`dateEditEnabled`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `firstDayOfWeek : Qt::DayOfWeek`

**API 类别：** 属性说明

**中文解读：** 这是 `QCalendarWidget` 的配置属性。初始化或状态切换时通过 `setDayOfWeek(...)` 设置，之后用 `DayOfWeek()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`Qt::DayOfWeek`。
- 属性名：`firstDayOfWeek`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `gridVisible : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QCalendarWidget` 的配置属性。初始化或状态切换时通过 `setGridVisible(...)` 设置，之后用 `gridVisible()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`gridVisible`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `horizontalHeaderFormat : HorizontalHeaderFormat`

**API 类别：** 属性说明

**中文解读：** 这是 `QCalendarWidget` 的配置属性。初始化或状态切换时通过 `setHorizontalHeaderFormat(...)` 设置，之后用 `horizontalHeaderFormat()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`HorizontalHeaderFormat`。
- 属性名：`horizontalHeaderFormat`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `maximumDate : QDate`

**API 类别：** 属性说明

**中文解读：** 这是 `QCalendarWidget` 的配置属性。初始化或状态切换时通过 `setMaximumDate(...)` 设置，之后用 `maximumDate()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QDate`。
- 属性名：`maximumDate`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `minimumDate : QDate`

**API 类别：** 属性说明

**中文解读：** 这是 `QCalendarWidget` 的配置属性。初始化或状态切换时通过 `setMinimumDate(...)` 设置，之后用 `minimumDate()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QDate`。
- 属性名：`minimumDate`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `navigationBarVisible : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QCalendarWidget` 的配置属性。初始化或状态切换时通过 `setNavigationBarVisible(...)` 设置，之后用 `navigationBarVisible()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`navigationBarVisible`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `selectedDate : QDate`

**API 类别：** 属性说明

**中文解读：** 这是 `QCalendarWidget` 的配置属性。初始化或状态切换时通过 `setSelectedDate(...)` 设置，之后用 `selectedDate()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QDate`。
- 属性名：`selectedDate`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `selectionMode : SelectionMode`

**API 类别：** 属性说明

**中文解读：** 这是 `QCalendarWidget` 的配置属性。初始化或状态切换时通过 `setSelectionMode(...)` 设置，之后用 `selectionMode()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`SelectionMode`。
- 属性名：`selectionMode`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `verticalHeaderFormat : VerticalHeaderFormat`

**API 类别：** 属性说明

**中文解读：** 这是 `QCalendarWidget` 的配置属性。初始化或状态切换时通过 `setVerticalHeaderFormat(...)` 设置，之后用 `verticalHeaderFormat()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`VerticalHeaderFormat`。
- 属性名：`verticalHeaderFormat`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QCalendarWidget::QCalendarWidget(QWidget *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QCalendarWidget` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `parent`：类型为 `QWidget *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QCalendarWidget::~QCalendarWidget()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QCalendarWidget` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QCalendarWidget::activated(QDate date)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QCalendarWidget` 发出的通知信号 `activated`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `date`：类型为 `QDate`。没有默认值，调用时必须提供。传入 `QDate` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCalendar QCalendarWidget::calendar() const`

**API 类别：** 成员函数说明

**中文解读：** `QCalendarWidget::calendar` 用于计算、查询或取得与“calendar”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QCalendar`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCalendar`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QCalendarWidget::clicked(QDate date)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QCalendarWidget` 发出的通知信号 `clicked`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `date`：类型为 `QDate`。没有默认值，调用时必须提供。传入 `QDate` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QCalendarWidget::currentPageChanged(int year, int month)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QCalendarWidget` 发出的通知信号 `currentPageChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `year`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `month`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMap<QDate, QTextCharFormat> QCalendarWidget::dateTextFormat() const`

**API 类别：** 成员函数说明

**中文解读：** `QCalendarWidget::dateTextFormat` 用于计算、查询或取得与“日期、文本、格式化”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMap<QDate, QTextCharFormat>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMap<QDate, QTextCharFormat>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextCharFormat QCalendarWidget::dateTextFormat(QDate date) const`

**API 类别：** 成员函数说明

**中文解读：** `QCalendarWidget::dateTextFormat` 用于计算、查询或取得与“日期、文本、格式化”相关的操作。调用时要先确认当前状态和 `date` 的有效范围；返回类型是 `QTextCharFormat`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextCharFormat`。
- 参数 `date`：类型为 `QDate`。没有默认值，调用时必须提供。传入 `QDate` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] bool QCalendarWidget::event(QEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QCalendarWidget::event` 用于计算、查询或取得与“event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `event`：类型为 `QEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] bool QCalendarWidget::eventFilter(QObject *watched, QEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QCalendarWidget::eventFilter` 用于计算、查询或取得与“event、Filter”相关的操作。调用时要先确认当前状态和 `watched`、`event` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `watched`：类型为 `QObject *`。没有默认值，调用时必须提供。Qt 对象参数。要确认对象有效、线程归属、所有权和该 API 是否只处理直接子对象。
- 参数 `event`：类型为 `QEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTextCharFormat QCalendarWidget::headerTextFormat() const`

**API 类别：** 成员函数说明

**中文解读：** `QCalendarWidget::headerTextFormat` 用于计算、查询或取得与“header、文本、格式化”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QTextCharFormat`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextCharFormat`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QCalendarWidget::keyPressEvent(QKeyEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QCalendarWidget::keyPressEvent` 用于执行与“key、Press、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QKeyEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QSize QCalendarWidget::minimumSizeHint() const`

**API 类别：** 成员函数说明

**中文解读：** `QCalendarWidget::minimumSizeHint` 用于计算、查询或取得与“最小值、尺寸或数量、Hint”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSize`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSize`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QCalendarWidget::monthShown() const`

**API 类别：** 成员函数说明

**中文解读：** `QCalendarWidget::monthShown` 用于计算、查询或取得与“月、Shown”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QCalendarWidget::mousePressEvent(QMouseEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QCalendarWidget::mousePressEvent` 用于执行与“mouse、Press、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QMouseEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QCalendarWidget::paintCell(QPainter *painter, const QRect &rect, QDate date) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QCalendarWidget` 的核心操作 `paintCell`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `painter`：类型为 `QPainter *`。没有默认值，调用时必须提供。绘制上下文。要确认它已经绑定有效绘制设备，并处于允许绘制的阶段。
- 参数 `rect`：类型为 `const QRect &`。没有默认值，调用时必须提供。矩形区域；要确认坐标系、是否包含右下边界以及空矩形的语义。
- 参数 `date`：类型为 `QDate`。没有默认值，调用时必须提供。传入 `QDate` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QCalendarWidget::resizeEvent(QResizeEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QCalendarWidget::resizeEvent` 用于执行与“调整尺寸、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QResizeEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QCalendarWidget::selectionChanged()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QCalendarWidget` 发出的通知信号 `selectionChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QCalendarWidget::setCalendar(QCalendar c)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setCalendar`。调用它会改变 `QCalendarWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `c`：类型为 `QCalendar`。没有默认值，调用时必须提供。传入 `QCalendar` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QCalendarWidget::setCurrentPage(int year, int month)`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `setCurrentPage`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `year`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `month`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QCalendarWidget::setDateRange(QDate min, QDate max)`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `setDateRange`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `min`：类型为 `QDate`。没有默认值，调用时必须提供。传入 `QDate` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `max`：类型为 `QDate`。没有默认值，调用时必须提供。传入 `QDate` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QCalendarWidget::setDateTextFormat(QDate date, const QTextCharFormat &format)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setDateTextFormat`。调用它会改变 `QCalendarWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `date`：类型为 `QDate`。没有默认值，调用时必须提供。传入 `QDate` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `format`：类型为 `const QTextCharFormat &`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QCalendarWidget::setHeaderTextFormat(const QTextCharFormat &format)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setHeaderTextFormat`。调用它会改变 `QCalendarWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `format`：类型为 `const QTextCharFormat &`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QCalendarWidget::setWeekdayTextFormat(Qt::DayOfWeek dayOfWeek, const QTextCharFormat &format)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setWeekdayTextFormat`。调用它会改变 `QCalendarWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `dayOfWeek`：类型为 `Qt::DayOfWeek`。没有默认值，调用时必须提供。传入 `Qt::DayOfWeek` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `format`：类型为 `const QTextCharFormat &`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QCalendarWidget::showNextMonth()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `showNextMonth`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 通常在控件完成 parent、layout、属性和信号连接后调用；顶层窗口显示后由事件循环处理绘制和输入。

### `[slot] void QCalendarWidget::showNextYear()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `showNextYear`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 通常在控件完成 parent、layout、属性和信号连接后调用；顶层窗口显示后由事件循环处理绘制和输入。

### `[slot] void QCalendarWidget::showPreviousMonth()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `showPreviousMonth`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 通常在控件完成 parent、layout、属性和信号连接后调用；顶层窗口显示后由事件循环处理绘制和输入。

### `[slot] void QCalendarWidget::showPreviousYear()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `showPreviousYear`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 通常在控件完成 parent、layout、属性和信号连接后调用；顶层窗口显示后由事件循环处理绘制和输入。

### `[slot] void QCalendarWidget::showSelectedDate()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `showSelectedDate`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 通常在控件完成 parent、layout、属性和信号连接后调用；顶层窗口显示后由事件循环处理绘制和输入。

### `[slot] void QCalendarWidget::showToday()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `showToday`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 通常在控件完成 parent、layout、属性和信号连接后调用；顶层窗口显示后由事件循环处理绘制和输入。

### `[override virtual] QSize QCalendarWidget::sizeHint() const`

**API 类别：** 成员函数说明

**中文解读：** `QCalendarWidget::sizeHint` 用于计算、查询或取得与“尺寸或数量、Hint”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSize`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSize`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] void QCalendarWidget::updateCell(QDate date)`

**API 类别：** 成员函数说明

**中文解读：** `QCalendarWidget::updateCell` 用于执行与“更新、Cell”相关的操作。调用时要先确认当前状态和 `date` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `date`：类型为 `QDate`。没有默认值，调用时必须提供。传入 `QDate` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 通常在数据变化后调用，让 Qt 合并重绘请求；不要直接调用 `paintEvent()`。

### `[protected] void QCalendarWidget::updateCells()`

**API 类别：** 成员函数说明

**中文解读：** `QCalendarWidget::updateCells` 用于执行与“更新、Cells”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 通常在数据变化后调用，让 Qt 合并重绘请求；不要直接调用 `paintEvent()`。

### `QTextCharFormat QCalendarWidget::weekdayTextFormat(Qt::DayOfWeek dayOfWeek) const`

**API 类别：** 成员函数说明

**中文解读：** `QCalendarWidget::weekdayTextFormat` 用于计算、查询或取得与“weekday、文本、格式化”相关的操作。调用时要先确认当前状态和 `dayOfWeek` 的有效范围；返回类型是 `QTextCharFormat`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QTextCharFormat`。
- 参数 `dayOfWeek`：类型为 `Qt::DayOfWeek`。没有默认值，调用时必须提供。传入 `Qt::DayOfWeek` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QCalendarWidget::yearShown() const`

**API 类别：** 成员函数说明

**中文解读：** `QCalendarWidget::yearShown` 用于计算、查询或取得与“年、Shown”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void clearMaximumDate()`

**API 类别：** 公有函数

**中文解读：** `QCalendarWidget::clearMaximumDate` 用于执行与“清空、最大值、日期”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void clearMinimumDate()`

**API 类别：** 公有函数

**中文解读：** `QCalendarWidget::clearMinimumDate` 用于执行与“清空、最小值、日期”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int dateEditAcceptDelay() const`

**API 类别：** 公有函数

**中文解读：** `QCalendarWidget::dateEditAcceptDelay` 用于计算、查询或取得与“日期、Edit、接受、Delay”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Qt::DayOfWeek firstDayOfWeek() const`

**API 类别：** 公有函数

**中文解读：** `QCalendarWidget::firstDayOfWeek` 用于计算、查询或取得与“首项、天、Of、Week”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `Qt::DayOfWeek`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::DayOfWeek`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCalendarWidget::HorizontalHeaderFormat horizontalHeaderFormat() const`

**API 类别：** 公有函数

**中文解读：** `QCalendarWidget::horizontalHeaderFormat` 用于计算、查询或取得与“水平、Header、格式化”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QCalendarWidget::HorizontalHeaderFormat`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCalendarWidget::HorizontalHeaderFormat`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool isDateEditEnabled() const`

**API 类别：** 公有函数

**中文解读：** 这是查询 API `isDateEditEnabled`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool isGridVisible() const`

**API 类别：** 公有函数

**中文解读：** 这是查询 API `isGridVisible`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool isNavigationBarVisible() const`

**API 类别：** 公有函数

**中文解读：** 这是查询 API `isNavigationBarVisible`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDate maximumDate() const`

**API 类别：** 公有函数

**中文解读：** `QCalendarWidget::maximumDate` 用于计算、查询或取得与“最大值、日期”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDate`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDate`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDate minimumDate() const`

**API 类别：** 公有函数

**中文解读：** `QCalendarWidget::minimumDate` 用于计算、查询或取得与“最小值、日期”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDate`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDate`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDate selectedDate() const`

**API 类别：** 公有函数

**中文解读：** `QCalendarWidget::selectedDate` 用于计算、查询或取得与“selected、日期”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QDate`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QDate`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCalendarWidget::SelectionMode selectionMode() const`

**API 类别：** 公有函数

**中文解读：** `QCalendarWidget::selectionMode` 用于计算、查询或取得与“selection、模式”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QCalendarWidget::SelectionMode`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCalendarWidget::SelectionMode`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setDateEditAcceptDelay(int delay)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setDateEditAcceptDelay`。调用它会改变 `QCalendarWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `delay`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setDateEditEnabled(bool enable)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setDateEditEnabled`。调用它会改变 `QCalendarWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enable`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setFirstDayOfWeek(Qt::DayOfWeek dayOfWeek)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setFirstDayOfWeek`。调用它会改变 `QCalendarWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `dayOfWeek`：类型为 `Qt::DayOfWeek`。没有默认值，调用时必须提供。传入 `Qt::DayOfWeek` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setHorizontalHeaderFormat(QCalendarWidget::HorizontalHeaderFormat format)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setHorizontalHeaderFormat`。调用它会改变 `QCalendarWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `format`：类型为 `QCalendarWidget::HorizontalHeaderFormat`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setMaximumDate(QDate date)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setMaximumDate`。调用它会改变 `QCalendarWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `date`：类型为 `QDate`。没有默认值，调用时必须提供。传入 `QDate` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setMinimumDate(QDate date)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setMinimumDate`。调用它会改变 `QCalendarWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `date`：类型为 `QDate`。没有默认值，调用时必须提供。传入 `QDate` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setSelectionMode(QCalendarWidget::SelectionMode mode)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setSelectionMode`。调用它会改变 `QCalendarWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `mode`：类型为 `QCalendarWidget::SelectionMode`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setVerticalHeaderFormat(QCalendarWidget::VerticalHeaderFormat format)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setVerticalHeaderFormat`。调用它会改变 `QCalendarWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `format`：类型为 `QCalendarWidget::VerticalHeaderFormat`。没有默认值，调用时必须提供。数据格式或显示格式。格式通常会影响解析、像素布局、精度、编码或兼容性。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCalendarWidget::VerticalHeaderFormat verticalHeaderFormat() const`

**API 类别：** 公有函数

**中文解读：** `QCalendarWidget::verticalHeaderFormat` 用于计算、查询或取得与“垂直、Header、格式化”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QCalendarWidget::VerticalHeaderFormat`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCalendarWidget::VerticalHeaderFormat`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setGridVisible(bool show)`

**API 类别：** 公有槽函数

**中文解读：** 这是可被信号连接或元对象调用的槽 `setGridVisible`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `show`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setNavigationBarVisible(bool visible)`

**API 类别：** 公有槽函数

**中文解读：** 这是可被信号连接或元对象调用的槽 `setNavigationBarVisible`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `visible`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setSelectedDate(QDate date)`

**API 类别：** 公有槽函数

**中文解读：** 这是可被信号连接或元对象调用的槽 `setSelectedDate`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `date`：类型为 `QDate`。没有默认值，调用时必须提供。传入 `QDate` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

## 6. 深入实践与常见坑

### 生命周期和资源边界

控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

### 状态和错误边界

控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

### 线程边界

所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

### 最容易出现的错误

优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QCalendarWidget` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
