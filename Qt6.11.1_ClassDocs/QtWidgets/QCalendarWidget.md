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

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QCalendarWidget::HorizontalHeaderFormat`

**作用与语义：**

该枚举类型定义了水平头部可以显示的各种格式。
- `QCalendarWidget::SingleLetterDayNames`：`1`;头部显示日名的单字母缩写（例如M代表Monday）。
- `QCalendarWidget::ShortDayNames`：`2`;标题显示日期名称的简短缩写（例如Monday的Monday）。
- `QCalendarWidget::LongDayNames`：`3`;头部显示完整的日期名称（例如星期一）。
- `QCalendarWidget::NoHorizontalHeader`：`0`;头部被隐藏。

### `enum QCalendarWidget::SelectionMode`

**作用与语义：**

本枚举描述了用户在日历中选择日期时所提供的类型。
- `QCalendarWidget::NoSelection`：`0`;日期不可选择。
- `QCalendarWidget::SingleSelection`：`1`;可选择单日期。

### `enum QCalendarWidget::VerticalHeaderFormat`

**作用与语义：**

该枚举类型定义了垂直头部可以显示的各种格式。
- `QCalendarWidget::ISOWeekNumbers`：`1`;头部显示ISO周数，如`QDate::weekNumber()`所述。
- `QCalendarWidget::NoVerticalHeader`：`0`;头部被隐藏。

### `dateEditAcceptDelay : int`

**作用与语义：**

该属性表示在内容被接受前显示非活跃日期编辑的时间。
如果启用了日历小部件的日期编辑功能，该属性会指定在最近用户输入后，日期编辑保持开启的时间（以毫秒为单位）。一旦时间过去，日期编辑中指定的日期将被接受，弹窗关闭。
默认情况下，延迟定义为1500毫秒（1.5秒）。

**如何使用：** 调用 `dateEditAcceptDelay()` 读取当前值；它不会修改应用状态。

### `dateEditEnabled : bool`

**作用与语义：**

该属性决定是否启用了日期编辑弹窗。
如果启用了该属性，按非修饰键（如果日历小部件有焦点），会弹出日期编辑，允许用户在当前位置指定的格式中指定日期。
默认情况下，该属性是被启用的。
日期编辑界面比`QDateEdit`更简单，但允许用户使用左右光标键在字段间导航，使用上下光标键增减单个字段，并直接用数字键输入数值。

**如何使用：** 调用 `dateEditEnabled()` 读取当前值；它不会修改应用状态。

### `firstDayOfWeek : Qt::DayOfWeek`

**作用与语义：**

该属性包含第一列显示的日期值。
默认情况下，第一列显示的日期是该日历所在地的一周第一天。

**如何使用：** 调用 `firstDayOfWeek()` 读取当前值；它不会修改应用状态。

### `gridVisible : bool`

**作用与语义：**

该属性在显示表格网格时成立。
默认值为假。

**如何使用：** 调用 `gridVisible()` 读取当前值；它不会修改应用状态。

### `horizontalHeaderFormat : HorizontalHeaderFormat`

**作用与语义：**

该属性表示水平头部的格式。
默认值是`QCalendarWidget::ShortDayNames`。

**如何使用：** 调用 `horizontalHeaderFormat()` 读取当前值；它不会修改应用状态。

### `maximumDate : QDate`

**作用与语义：**

该物业持有当前指定日期范围的最大日期。
用户将无法选择超过当前设定的最大日期日期的日期。
设置最大日期时，如果选择范围无效，则调整`minimumDate`和`selectedDate`属性。如果提供的日期不是有效的`QDate`对象，setMaximumDate() 函数无效。
默认的最大日期是公元9999年12月31日。你可以通过调用clearMaximumDate()（自第6.6学期起）来恢复该默认日期。

**如何使用：** 调用 `maximumDate()` 读取当前值；它不会修改应用状态。

### `minimumDate : QDate`

**作用与语义：**

该物业持有当前指定日期范围的最小日期。
用户无法选择早于当前设定最低日期的日期。
设置最小日期时，如果选择范围无效，则调整`maximumDate`和`selectedDate`属性。如果提供的日期不是有效的`QDate`对象，setMinimumDate() 函数则无效。
默认的最低日期是公元前4714年11月25日。你可以通过调用clearMinimumDate()（自第6.6学期起）来恢复这个默认日期。

**如何使用：** 调用 `minimumDate()` 读取当前值；它不会修改应用状态。

### `navigationBarVisible : bool`

**作用与语义：**

无论导航栏是否显示，这一属性都成立。
当该属性被`true`（默认状态）时，下个月、上个月、月份选择、年度选择控制项会显示在顶部。
当属性设置为虚假时，这些控制项会被隐藏。

**如何使用：** 调用 `navigationBarVisible()` 读取当前值；它不会修改应用状态。

### `selectedDate : QDate`

**作用与语义：**

该物业持有目前选定的日期。
所选日期必须在`minimumDate`和`maximumDate`物业指定的日期范围内。默认情况下，所选日期即为当前日期。

**如何使用：** 调用 `selectedDate()` 读取当前值；它不会修改应用状态。

### `selectionMode : SelectionMode`

**作用与语义：**

该属性决定了用户在日历中可以选择的类型。
当该属性设置为`SingleSelection`时，用户可以使用鼠标或键盘选择最小和最大允许的日期。
当属性设置为`NoSelection`时，用户无法选择日期，但仍可通过程序选择。注意，当属性设置为`NoSelection`时选择的日期仍是日历中的选定日期。
默认值为`SingleSelection`。

**如何使用：** 调用 `selectionMode()` 读取当前值；它不会修改应用状态。

### `verticalHeaderFormat : VerticalHeaderFormat`

**作用与语义：**

该属性表示垂直头部的格式。
默认值是 QCalendarWidget：：ISOWeekNumber。

**如何使用：** 调用 `verticalHeaderFormat()` 读取当前值；它不会修改应用状态。

### `[explicit] QCalendarWidget::QCalendarWidget(QWidget *parent = nullptr)`

**作用与语义：**

基于给定`parent`构建一个日历小部件。
该小部件初始化为当前月份和年份，当前选择的日期是今天。

### `[virtual noexcept] QCalendarWidget::~QCalendarWidget()`

**作用与语义：**

会破坏日历小部件。

### `[signal] void QCalendarWidget::activated(QDate date)`

**作用与语义：**

每当用户按下回车键或回车键，或在日历小部件中双击`date`时，都会发出该信号。

### `QCalendar QCalendarWidget::calendar() const`

**作用与语义：**

报告该小部件正在使用的日历系统。

### `[signal] void QCalendarWidget::clicked(QDate date)`

**作用与语义：**

当点击鼠标按钮时，该信号会发出。鼠标点击的日期由`date`指定。只有在有效日期点击时才会发出信号，例如日期不在`minimumDate()`和`maximumDate()`之外。如果选择模式为`NoSelection`，则不会发出该信号。

### `[signal] void QCalendarWidget::currentPageChanged(int year, int month)`

**作用与语义：**

当当前显示的月份发生变化时，该信号会发出。新的`year`和`month`作为参数传递。

### `QMap<QDate, QTextCharFormat> QCalendarWidget::dateTextFormat() const`

**作用与语义：**

返回`QDate`到`QTextCharFormat`的`QMap`，显示所有使用特殊格式的日期，该格式会改变其渲染效果。

### `QTextCharFormat QCalendarWidget::dateTextFormat(QDate date) const`

**作用与语义：**

返回`date`的`QTextCharFormat`。如果日期未被特别渲染，字符格式可能为空。

### `[override virtual protected] bool QCalendarWidget::event(QEvent *event)`

**作用与语义：**

重实现自：`QWidget::event`（QEvent *事件）。

### `[override virtual protected] bool QCalendarWidget::eventFilter(QObject *watched, QEvent *event)`

**作用与语义：**

重装：`QObject::eventFilter`（QObject *已观看，QEvent *事件）。

### `QTextCharFormat QCalendarWidget::headerTextFormat() const`

**作用与语义：**

返回文本字符格式以渲染头部。

### `[override virtual protected] void QCalendarWidget::keyPressEvent(QKeyEvent *event)`

**作用与语义：**

重实现自：`QWidget::keyPressEvent`（QKeyEvent *event）。
该事件处理程序用于事件`event`，可以在子类中重新实现，以接收该控件的按键事件。
一个小部件必须调用`setFocusPolicy()`先接受焦点，并且必须有焦点才能接收按键事件。
如果你重新实现这个处理器，如果你不对密钥进行操作，务必调用基类实现。
默认实现会关闭弹出小部件，如果用户按下`QKeySequence::Cancel`的按键序列（通常是 Escape 键）。否则事件会被忽略，以便小部件的父节点能够解释。
注意`QKeyEvent`以 isAccepted() == true 开头，所以你不需要调用 `QKeyEvent::accept()`——只要你对该键执行时不要调用基类实现即可。

### `[override virtual] QSize QCalendarWidget::minimumSizeHint() const`

**作用与语义：**

重新实现属性的访问函数：`QWidget::minimumSizeHint`。

### `int QCalendarWidget::monthShown() const`

**作用与语义：**

返回当前显示的月份。月份编号为1到12。

### `[override virtual protected] void QCalendarWidget::mousePressEvent(QMouseEvent *event)`

**作用与语义：**

重实现自：`QWidget::mousePressEvent`（QMouseEvent *event）。
该事件处理程序用于事件`event`，可以重新实现为子类，以接收该小部件的鼠标按键事件。
如果你在 mousePressEvent() 创建新控件，`mouseReleaseEvent()`可能不会出现在你预期的位置，这取决于底层窗口系统（或 X11 窗口管理器）、控件的位置，甚至可能还有其他因素。
默认实现实现了当你点击窗口外时关闭弹出小部件的功能。对于其他小部件类型，它没有任何作用。

### `[virtual protected] void QCalendarWidget::paintCell(QPainter *painter, const QRect &rect, QDate date) const`

**作用与语义：**

使用给定的`painter`和`rect`，绘制给定`date`指定的单元格。

### `[override virtual protected] void QCalendarWidget::resizeEvent(QResizeEvent *event)`

**作用与语义：**

重实现自：`QWidget::resizeEvent`（QResizeEvent *event）。
该事件处理程序可以在子类中重新实现，以接收通过 `event` 参数传递的控件调整大小事件。当调用 resizeEvent() 时，控件已经拥有新的几何体。旧的大小可以通过 `QResizeEvent::oldSize()` 访问。
控件会被擦除，并在处理调整尺寸事件后立即接收绘图事件。不需要（也不应该）在这个处理程序中进行绘图。

### `[signal] void QCalendarWidget::selectionChanged()`

**作用与语义：**

当当前选定的日期被更改时，该信号会发出。
当前选择的日期可以由用户使用鼠标或键盘更改，程序员也可以用`setSelectedDate()`更改。

### `void QCalendarWidget::setCalendar(QCalendar c)`

**作用与语义：**

将`c`设置为该小部件使用的日历系统。
该小部件可以使用任何支持的历法系统。默认情况下，它使用格里高利历。

### `[slot] void QCalendarWidget::setCurrentPage(int year, int month)`

**作用与语义：**

显示给定`year`的给定`month`，不更改选定日期。使用`setSelectedDate()`函数修改所选日期。
当前显示的月份和年份分别可通过`monthShown()`和`yearShown()`函数检索。

### `[slot] void QCalendarWidget::setDateRange(QDate min, QDate max)`

**作用与语义：**

通过设置`minimumDate`和`maximumDate`属性来定义日期范围。
日期范围限制了用户的选择，即用户只能选择指定日期范围内的日期。注意。
类似于。
如果`min`或`max`参数`QDate`对象不有效，该函数则无效。

**官方示例：**

```cpp
 QCalendarWidget *calendar;

 calendar->setDateRange(min, max);
```

### `void QCalendarWidget::setDateTextFormat(QDate date, const QTextCharFormat &format)`

**作用与语义：**

将渲染给定`date`的格式设置为`format`指定的格式。
如果`date`为空，所有日期格式都会被清除。

### `void QCalendarWidget::setHeaderTextFormat(const QTextCharFormat &format)`

**作用与语义：**

将渲染标题的文本字符格式设置为`format`。如果你还设置了工作日文本格式，该格式的前景和背景颜色将优先于标题的格式。其他格式信息仍将由标题的格式决定。

### `void QCalendarWidget::setWeekdayTextFormat(Qt::DayOfWeek dayOfWeek, const QTextCharFormat &format)`

**作用与语义：**

将周中日的渲染文本字符格式设置为`format` `dayOfWeek`。在前景和背景色的情况下，该格式优先于头部格式。其他文本格式信息取自头部格式。

### `[slot] void QCalendarWidget::showNextMonth()`

**作用与语义：**

显示下个月相对于当前显示月份的关系。注意所选日期未变。

### `[slot] void QCalendarWidget::showNextYear()`

**作用与语义：**

显示当前显示的月份相对于当前显示年份的下一年。注意，所选日期未被更改。

### `[slot] void QCalendarWidget::showPreviousMonth()`

**作用与语义：**

显示上个月相对于当前显示月份的差异。注意所选日期未变。

### `[slot] void QCalendarWidget::showPreviousYear()`

**作用与语义：**

显示上一年当前显示月份相对于当前显示年份。注意，所选日期未变。

### `[slot] void QCalendarWidget::showSelectedDate()`

**作用与语义：**

显示所选日期的月份。

### `[slot] void QCalendarWidget::showToday()`

**作用与语义：**

显示的是今天日期的月份。

### `[override virtual] QSize QCalendarWidget::sizeHint() const`

**作用与语义：**

重新实现了属性的访问函数：`QWidget::sizeHint`。

### `[protected] void QCalendarWidget::updateCell(QDate date)`

**作用与语义：**

除非关闭更新或该单元被隐藏，否则更新由给定`date`指定的单元格。

### `[protected] void QCalendarWidget::updateCells()`

**作用与语义：**

除非禁用更新，否则会更新所有可见的单元格。

### `QTextCharFormat QCalendarWidget::weekdayTextFormat(Qt::DayOfWeek dayOfWeek) const`

**作用与语义：**

返回文本字符格式，用于渲染周`dayOfWeek`的一天。

### `int QCalendarWidget::yearShown() const`

**作用与语义：**

返回当前显示月份的年份。月份编号为1到12。

### `void clearMaximumDate()`

**作用与语义：**

该物业持有当前指定日期范围的最大日期。
用户将无法选择超过当前设定的最大日期日期的日期。
设置最大日期时，如果选择范围无效，则调整`minimumDate`和`selectedDate`属性。如果提供的日期不是有效的`QDate`对象，setMaximumDate() 函数无效。
默认的最大日期是公元9999年12月31日。你可以通过调用clearMaximumDate()（自第6.6学期起）来恢复该默认日期。

**如何使用：** 调用 `clearMaximumDate()` 读取当前值；它不会修改应用状态。

### `void clearMinimumDate()`

**作用与语义：**

该物业持有当前指定日期范围的最小日期。
用户无法选择早于当前设定最低日期的日期。
设置最小日期时，如果选择范围无效，则调整`maximumDate`和`selectedDate`属性。如果提供的日期不是有效的`QDate`对象，setMinimumDate() 函数则无效。
默认的最低日期是公元前4714年11月25日。你可以通过调用clearMinimumDate()（自第6.6学期起）来恢复这个默认日期。

**如何使用：** 调用 `clearMinimumDate()` 读取当前值；它不会修改应用状态。

### `int dateEditAcceptDelay() const`

**作用与语义：**

该属性表示在内容被接受前显示非活跃日期编辑的时间。
如果启用了日历小部件的日期编辑功能，该属性会指定在最近用户输入后，日期编辑保持开启的时间（以毫秒为单位）。一旦时间过去，日期编辑中指定的日期将被接受，弹窗关闭。
默认情况下，延迟定义为1500毫秒（1.5秒）。

**如何使用：** 调用 `dateEditAcceptDelay()` 读取当前值；它不会修改应用状态。

### `Qt::DayOfWeek firstDayOfWeek() const`

**作用与语义：**

该属性包含第一列显示的日期值。
默认情况下，第一列显示的日期是该日历所在地的一周第一天。

**如何使用：** 调用 `firstDayOfWeek()` 读取当前值；它不会修改应用状态。

### `QCalendarWidget::HorizontalHeaderFormat horizontalHeaderFormat() const`

**作用与语义：**

该属性表示水平头部的格式。
默认值是`QCalendarWidget::ShortDayNames`。

**如何使用：** 调用 `horizontalHeaderFormat()` 读取当前值；它不会修改应用状态。

### `bool isDateEditEnabled() const`

**作用与语义：**

该属性决定是否启用了日期编辑弹窗。
如果启用了该属性，按非修饰键（如果日历小部件有焦点），会弹出日期编辑，允许用户在当前位置指定的格式中指定日期。
默认情况下，该属性是被启用的。
日期编辑界面比`QDateEdit`更简单，但允许用户使用左右光标键在字段间导航，使用上下光标键增减单个字段，并直接用数字键输入数值。

**如何使用：** 调用 `isDateEditEnabled()` 读取当前值；它不会修改应用状态。

### `bool isGridVisible() const`

**作用与语义：**

该属性在显示表格网格时成立。
默认值为假。

**如何使用：** 调用 `isGridVisible()` 读取当前值；它不会修改应用状态。

### `bool isNavigationBarVisible() const`

**作用与语义：**

无论导航栏是否显示，这一属性都成立。
当该属性被`true`（默认状态）时，下个月、上个月、月份选择、年度选择控制项会显示在顶部。
当属性设置为虚假时，这些控制项会被隐藏。

**如何使用：** 调用 `isNavigationBarVisible()` 读取当前值；它不会修改应用状态。

### `QDate maximumDate() const`

**作用与语义：**

该物业持有当前指定日期范围的最大日期。
用户将无法选择超过当前设定的最大日期日期的日期。
设置最大日期时，如果选择范围无效，则调整`minimumDate`和`selectedDate`属性。如果提供的日期不是有效的`QDate`对象，setMaximumDate() 函数无效。
默认的最大日期是公元9999年12月31日。你可以通过调用clearMaximumDate()（自第6.6学期起）来恢复该默认日期。

**如何使用：** 调用 `maximumDate()` 读取当前值；它不会修改应用状态。

### `QDate minimumDate() const`

**作用与语义：**

该物业持有当前指定日期范围的最小日期。
用户无法选择早于当前设定最低日期的日期。
设置最小日期时，如果选择范围无效，则调整`maximumDate`和`selectedDate`属性。如果提供的日期不是有效的`QDate`对象，setMinimumDate() 函数则无效。
默认的最低日期是公元前4714年11月25日。你可以通过调用clearMinimumDate()（自第6.6学期起）来恢复这个默认日期。

**如何使用：** 调用 `minimumDate()` 读取当前值；它不会修改应用状态。

### `QDate selectedDate() const`

**作用与语义：**

该物业持有目前选定的日期。
所选日期必须在`minimumDate`和`maximumDate`物业指定的日期范围内。默认情况下，所选日期即为当前日期。

**如何使用：** 调用 `selectedDate()` 读取当前值；它不会修改应用状态。

### `QCalendarWidget::SelectionMode selectionMode() const`

**作用与语义：**

该属性决定了用户在日历中可以选择的类型。
当该属性设置为`SingleSelection`时，用户可以使用鼠标或键盘选择最小和最大允许的日期。
当属性设置为`NoSelection`时，用户无法选择日期，但仍可通过程序选择。注意，当属性设置为`NoSelection`时选择的日期仍是日历中的选定日期。
默认值为`SingleSelection`。

**如何使用：** 调用 `selectionMode()` 读取当前值；它不会修改应用状态。

### `void setDateEditAcceptDelay(int delay)`

**作用与语义：**

该属性表示在内容被接受前显示非活跃日期编辑的时间。
如果启用了日历小部件的日期编辑功能，该属性会指定在最近用户输入后，日期编辑保持开启的时间（以毫秒为单位）。一旦时间过去，日期编辑中指定的日期将被接受，弹窗关闭。
默认情况下，延迟定义为1500毫秒（1.5秒）。

**如何使用：** 调用 `setDateEditAcceptDelay(...)` 修改 `dateEditAcceptDelay`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setDateEditEnabled(bool enable)`

**作用与语义：**

该属性决定是否启用了日期编辑弹窗。
如果启用了该属性，按非修饰键（如果日历小部件有焦点），会弹出日期编辑，允许用户在当前位置指定的格式中指定日期。
默认情况下，该属性是被启用的。
日期编辑界面比`QDateEdit`更简单，但允许用户使用左右光标键在字段间导航，使用上下光标键增减单个字段，并直接用数字键输入数值。

**如何使用：** 调用 `setDateEditEnabled(...)` 修改 `dateEditEnabled`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setFirstDayOfWeek(Qt::DayOfWeek dayOfWeek)`

**作用与语义：**

该属性包含第一列显示的日期值。
默认情况下，第一列显示的日期是该日历所在地的一周第一天。

**如何使用：** 调用 `setFirstDayOfWeek(...)` 修改 `firstDayOfWeek`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setHorizontalHeaderFormat(QCalendarWidget::HorizontalHeaderFormat format)`

**作用与语义：**

该属性表示水平头部的格式。
默认值是`QCalendarWidget::ShortDayNames`。

**如何使用：** 调用 `setHorizontalHeaderFormat(...)` 修改 `horizontalHeaderFormat`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMaximumDate(QDate date)`

**作用与语义：**

该物业持有当前指定日期范围的最大日期。
用户将无法选择超过当前设定的最大日期日期的日期。
设置最大日期时，如果选择范围无效，则调整`minimumDate`和`selectedDate`属性。如果提供的日期不是有效的`QDate`对象，setMaximumDate() 函数无效。
默认的最大日期是公元9999年12月31日。你可以通过调用clearMaximumDate()（自第6.6学期起）来恢复该默认日期。

**如何使用：** 调用 `setMaximumDate(...)` 修改 `maximumDate`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMinimumDate(QDate date)`

**作用与语义：**

该物业持有当前指定日期范围的最小日期。
用户无法选择早于当前设定最低日期的日期。
设置最小日期时，如果选择范围无效，则调整`maximumDate`和`selectedDate`属性。如果提供的日期不是有效的`QDate`对象，setMinimumDate() 函数则无效。
默认的最低日期是公元前4714年11月25日。你可以通过调用clearMinimumDate()（自第6.6学期起）来恢复这个默认日期。

**如何使用：** 调用 `setMinimumDate(...)` 修改 `minimumDate`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setSelectionMode(QCalendarWidget::SelectionMode mode)`

**作用与语义：**

该属性决定了用户在日历中可以选择的类型。
当该属性设置为`SingleSelection`时，用户可以使用鼠标或键盘选择最小和最大允许的日期。
当属性设置为`NoSelection`时，用户无法选择日期，但仍可通过程序选择。注意，当属性设置为`NoSelection`时选择的日期仍是日历中的选定日期。
默认值为`SingleSelection`。

**如何使用：** 调用 `setSelectionMode(...)` 修改 `selectionMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setVerticalHeaderFormat(QCalendarWidget::VerticalHeaderFormat format)`

**作用与语义：**

该属性表示垂直头部的格式。
默认值是 QCalendarWidget：：ISOWeekNumber。

**如何使用：** 调用 `setVerticalHeaderFormat(...)` 修改 `verticalHeaderFormat`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QCalendarWidget::VerticalHeaderFormat verticalHeaderFormat() const`

**作用与语义：**

该属性表示垂直头部的格式。
默认值是 QCalendarWidget：：ISOWeekNumber。

**如何使用：** 调用 `verticalHeaderFormat()` 读取当前值；它不会修改应用状态。

### `void setGridVisible(bool show)`

**作用与语义：**

该属性在显示表格网格时成立。
默认值为假。

**如何使用：** 调用 `setGridVisible(...)` 修改 `gridVisible`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setNavigationBarVisible(bool visible)`

**作用与语义：**

无论导航栏是否显示，这一属性都成立。
当该属性被`true`（默认状态）时，下个月、上个月、月份选择、年度选择控制项会显示在顶部。
当属性设置为虚假时，这些控制项会被隐藏。

**如何使用：** 调用 `setNavigationBarVisible(...)` 修改 `navigationBarVisible`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setSelectedDate(QDate date)`

**作用与语义：**

该物业持有目前选定的日期。
所选日期必须在`minimumDate`和`maximumDate`物业指定的日期范围内。默认情况下，所选日期即为当前日期。

**如何使用：** 调用 `setSelectedDate(...)` 修改 `selectedDate`；传入的新值会成为后续查询和相关界面行为所使用的值。

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
