# QDateTimeEdit

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QDateTimeEdit` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QDateTimeEdit` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QDateTimeEdit>`
- 继承自：QAbstractSpinBox
- 直接派生类：QDateEdit、QTimeEdit

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

- `enum Section { NoSection, AmPmSection, MSecSection, SecondSection, MinuteSection, …, YearSection }`
- `flags Sections`

### 属性

- `calendarPopup : bool`
- `currentSection : Section`
- `currentSectionIndex : int`
- `date : QDate`
- `dateTime : QDateTime`
- `displayFormat : QString`
- `displayedSections : Sections`
- `maximumDate : QDate`
- `maximumDateTime : QDateTime`
- `maximumTime : QTime`
- `minimumDate : QDate`
- `minimumDateTime : QDateTime`
- `minimumTime : QTime`
- `sectionCount : int`
- `time : QTime`
- `(since 6.7) timeZone : QTimeZone`

### 公有函数

- `QDateTimeEdit(QWidget *parent = nullptr)`
- `QDateTimeEdit(QDate date, QWidget *parent = nullptr)`
- `QDateTimeEdit(QTime time, QWidget *parent = nullptr)`
- `QDateTimeEdit(const QDateTime &datetime, QWidget *parent = nullptr)`
- `virtual ~QDateTimeEdit()`
- `QCalendar calendar() const`
- `bool calendarPopup() const`
- `QCalendarWidget * calendarWidget() const`
- `void clearMaximumDate()`
- `void clearMaximumDateTime()`
- `void clearMaximumTime()`
- `void clearMinimumDate()`
- `void clearMinimumDateTime()`
- `void clearMinimumTime()`
- `QDateTimeEdit::Section currentSection() const`
- `int currentSectionIndex() const`
- `QDate date() const`
- `QDateTime dateTime() const`
- `QString displayFormat() const`
- `QDateTimeEdit::Sections displayedSections() const`
- `QDate maximumDate() const`
- `QDateTime maximumDateTime() const`
- `QTime maximumTime() const`
- `QDate minimumDate() const`
- `QDateTime minimumDateTime() const`
- `QTime minimumTime() const`
- `QDateTimeEdit::Section sectionAt(int index) const`
- `int sectionCount() const`
- `QString sectionText(QDateTimeEdit::Section section) const`
- `void setCalendar(QCalendar calendar)`
- `void setCalendarPopup(bool enable)`
- `void setCalendarWidget(QCalendarWidget *calendarWidget)`
- `void setCurrentSection(QDateTimeEdit::Section section)`
- `void setCurrentSectionIndex(int index)`
- `void setDateRange(QDate min, QDate max)`
- `void setDateTimeRange(const QDateTime &min, const QDateTime &max)`
- `void setDisplayFormat(const QString &format)`
- `void setMaximumDate(QDate max)`
- `void setMaximumDateTime(const QDateTime &dt)`
- `void setMaximumTime(QTime max)`
- `void setMinimumDate(QDate min)`
- `void setMinimumDateTime(const QDateTime &dt)`
- `void setMinimumTime(QTime min)`
- `void setSelectedSection(QDateTimeEdit::Section section)`
- `void setTimeRange(QTime min, QTime max)`
- `void setTimeZone(const QTimeZone &zone)`
- `QTime time() const`
- `QTimeZone timeZone() const`

### 重实现的公有函数

- `virtual void clear() override`
- `virtual bool event(QEvent *event) override`
- `virtual QSize sizeHint() const override`
- `virtual void stepBy(int steps) override`

### 公有槽函数

- `void setDate(QDate date)`
- `void setDateTime(const QDateTime &dateTime)`
- `void setTime(QTime time)`

### 信号

- `void dateChanged(QDate date)`
- `void dateTimeChanged(const QDateTime &datetime)`
- `void timeChanged(QTime time)`

### 保护函数

- `virtual QDateTime dateTimeFromText(const QString &text) const`
- `virtual QString textFromDateTime(const QDateTime &dateTime) const`

### 重实现的保护函数

- `virtual void fixup(QString &input) const override`
- `virtual void focusInEvent(QFocusEvent *event) override`
- `virtual bool focusNextPrevChild(bool next) override`
- `virtual void initStyleOption(QStyleOptionSpinBox *option) const override`
- `virtual void keyPressEvent(QKeyEvent *event) override`
- `virtual void mousePressEvent(QMouseEvent *event) override`
- `virtual void paintEvent(QPaintEvent *event) override`
- `virtual QAbstractSpinBox::StepEnabled stepEnabled() const override`
- `virtual QValidator::State validate(QString &text, int &pos) const override`
- `virtual void wheelEvent(QWheelEvent *event) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QDateTimeEdit::Sectionflags QDateTimeEdit::Sections`

**作用与语义：**

- `QDateTimeEdit::NoSection`：`0x0000`
- `QDateTimeEdit::AmPmSection`：`0x0001`
- `QDateTimeEdit::MSecSection`：`0x0002`
- `QDateTimeEdit::SecondSection`：`0x0004`
- `QDateTimeEdit::MinuteSection`：`0x0008`
- `QDateTimeEdit::HourSection`：`0x0010`
- `QDateTimeEdit::DaySection`：`0x0100`
- `QDateTimeEdit::MonthSection`：`0x0200`
- `QDateTimeEdit::YearSection`：`0x0400`
Sections 类型是 QFlags 的 typedef<Section>。它存储 Section 值的 OR 组合。

### `calendarPopup : bool`

**作用与语义：**

该属性包含当前的日历弹出展示模式。
点击箭头按钮后会显示日历弹窗。该属性仅在存在有效日期显示格式时有效。

**如何使用：** 调用 `calendarPopup()` 读取当前值；它不会修改应用状态。

### `currentSection : Section`

**作用与语义：**

该属性表示当前自旋盒截面。

**如何使用：** 调用 `currentSection()` 读取当前值；它不会修改应用状态。

### `currentSectionIndex : int`

**作用与语义：**

该属性表示旋量盒当前截面索引。
如果格式是“yyyy/MM/dd”，displayText是“2001/05/21”，cursorPosition是5，currentSectionIndex返回1。如果cursorPosition是3，currentSectionIndex是0，依此类推。

**如何使用：** 调用 `currentSectionIndex()` 读取当前值；它不会修改应用状态。

### `date : QDate`

**作用与语义：**

该属性包含了控件中设置的`QDate`。
默认情况下，该物业包含一个指向2000年1月1日的日期。

**如何使用：** 调用 `date()` 读取当前值；它不会修改应用状态。

### `dateTime : QDateTime`

**作用与语义：**

该属性表示`QDateTimeEdit`中所设定的`QDateTime`。
设置该属性时，新 `QDateTime` 转换为`QDateTimeEdit`的时间系统，因此时间系统保持不变。
默认情况下，该属性设置为2000 CE的开始。它只能设置为有效的`QDateTime`值。如果任何操作导致该属性的日期-时间值为无效，则重置为`minimumDateTime`属性的值。
如果`QDateTimeEdit`没有日期字段，设置该属性会使小部件的日期范围以该属性新值的日期开始和结束。

**如何使用：** 调用 `dateTime()` 读取当前值；它不会修改应用状态。

### `displayFormat : QString`

**作用与语义：**

该属性保留了显示日期/日期编辑的格式。
该格式在`QDateTime::toString()`和 `QDateTime::fromString()` 中有详细描述。
示例格式字符串（假设日期为1969年7月2日）：
- `Format`：结果
- `dd.MM.yyyy`：1969年7月2日
- `MMM d yy`：1969年7月2日
- `MMMM d yy`：1969年7月2日
请注意，如果你指定两位数年份，它会被解释为编辑日期时间初始化的世纪。默认的世纪是第21世纪（2000-2099）。
如果你指定了无效格式，格式将不会被设置。

**如何使用：** 调用 `displayFormat()` 读取当前值；它不会修改应用状态。

### `[read-only] displayedSections : Sections`

**作用与语义：**

该属性保存了日期时间编辑中当前显示的字段。
返回该格式显示的部分的位集。

**如何使用：** 调用 `displayedSections()` 读取当前值；它不会修改应用状态。

### `maximumDate : QDate`

**作用与语义：**

该属性拥有日期时间的最大日期。
更改该属性会更新`maximumDateTime`属性的日期，同时保留`maximumTime`属性。设置该属性时，必要时会调整`minimumDate`以确保范围有效。发生这种情况时，如果`minimumTime`属性大于`maximumTime`属性，也会相应调整。否则，对该属性的更改会保留`minimumDateTime`属性。
该属性只能被设置为描述当前`maximumTime`属性使`QDateTime`对象有效日期的有效`QDate`对象。setMaximumDate() 接受的最晚日期是公元9999年末。这是该属性的默认时间。该默认值可以通过`clearMaximumDateTime()`恢复。

**如何使用：** 调用 `maximumDate()` 读取当前值；它不会修改应用状态。

### `maximumDateTime : QDateTime`

**作用与语义：**

该属性包含日期时间编辑的最大日期时间。
更改该属性隐式地将`maximumDate`和`maximumTime`属性分别更新为该属性的日期和时间部分。设置该属性时，如有必要，`minimumDateTime`会调整以确保该范围有效。否则，更改该属性则保持`minimumDateTime`属性。
该属性只能设置为有效的`QDateTime`值。setMaximumDateTime() 接受的最晚日期时间为公元9999年末。这是该属性的默认值。该默认值可用 clearMaximumDateTime() 恢复。

**如何使用：** 调用 `maximumDateTime()` 读取当前值；它不会修改应用状态。

### `maximumTime : QTime`

**作用与语义：**

该属性包含了日期时间编辑的最大时间。
更改该属性会更新`maximumDateTime`属性的时间，同时保留`minimumDate`和`maximumDate`属性。如果这些属性的日期重合，设置该属性时会调整`minimumTime`属性，以确保范围有效。否则，更改该属性则保持`minimumDateTime`属性。
该属性可以设置为任意有效的`QTime`值。默认情况下，该属性包含时间为23：59：59和999毫秒。该默认值可以通过clearMaximumTime()恢复。

**如何使用：** 调用 `maximumTime()` 读取当前值；它不会修改应用状态。

### `minimumDate : QDate`

**作用与语义：**

该属性包含日期时间编辑的最小日期。
更改该属性会更新`minimumDateTime`属性的日期，同时保留`minimumTime`属性。设置该属性时，如有必要，`maximumDate`会调整以确保范围保持有效。发生这种情况时，如果`maximumTime`属性小于`minimumTime`属性，也会相应调整。否则，对该属性的更改会保留`maximumDateTime`属性。
该属性只能被设置为描述当前`minimumTime`属性使得有效`QDateTime`对象的有效日期的有效`QDate`对象。setMinimumDate() 接受的最早日期是公元100年的开始。该属性的默认时间为公元1752年9月14日。该默认值可以通过`clearMinimumDateTime()`恢复。

**如何使用：** 调用 `minimumDate()` 读取当前值；它不会修改应用状态。

### `minimumDateTime : QDateTime`

**作用与语义：**

该属性包含了日期时间编辑的最小日期时间。
更改该属性隐式地将`minimumDate`和`minimumTime`属性分别更新为该属性的日期和时间部分。设置该属性时，如有必要，会调整`maximumDateTime`以确保该范围有效。否则，更改该属性则保持`maximumDateTime`属性。
该属性只能设置为有效的`QDateTime`值。setMinimumDateTime() 接受的最早日期时间是公元100年的开始。该属性的默认时间是公元1752年9月14日的开始。该默认可以通过 clearMinimumDateTime() 恢复。

**如何使用：** 调用 `minimumDateTime()` 读取当前值；它不会修改应用状态。

### `minimumTime : QTime`

**作用与语义：**

该属性表示日期时间编辑的最小时间。
更改该属性会更新`minimumDateTime`属性的时间，同时保留`minimumDate`和`maximumDate`属性。如果这些属性的日期重合，设置该属性时会调整`maximumTime`属性，以确保范围有效。否则，更改该属性则保持`maximumDateTime`属性。
该属性可以设置为任意有效的`QTime`值。默认情况下，该属性包含 00：00：00 和 0 毫秒的时间。该默认值可以通过 clearMinimumTime() 恢复。

**如何使用：** 调用 `minimumTime()` 读取当前值；它不会修改应用状态。

### `[read-only] sectionCount : int`

**作用与语义：**

该属性包含显示的分段数量。如果格式为“yyyy/yy/yyyy”，sectionCount返回3。

**如何使用：** 调用 `sectionCount()` 读取当前值；它不会修改应用状态。

### `time : QTime`

**作用与语义：**

该属性包含了控件中设置的`QTime`。
默认情况下，该属性包含时间为00：00：00和0毫秒。

**如何使用：** 调用 `time()` 读取当前值；它不会修改应用状态。

### `[since 6.7] timeZone : QTimeZone`

**作用与语义：**

该属性包含 datetime 编辑控件当前使用的时区。
如果使用的日期时间格式包含时区指示器——即`t`、`tt`、`ttt`或`tttt`格式指定符——用户输入在解析时会在该时区重新表达，覆盖用户可能指定的任何时区。

**如何使用：** 调用 `timeZone()` 读取当前值；它不会修改应用状态。

### `[explicit] QDateTimeEdit::QDateTimeEdit(QWidget *parent = nullptr)`

**作用与语义：**

构建一个空的日期时间编辑器，并配有`parent`。

### `[explicit] QDateTimeEdit::QDateTimeEdit(QDate date, QWidget *parent = nullptr)`

**作用与语义：**

构建一个空的日期时间编辑器，并带有`parent`。该值设置为`date`。

### `[explicit] QDateTimeEdit::QDateTimeEdit(QTime time, QWidget *parent = nullptr)`

**作用与语义：**

构建一个空的日期时间编辑器，并带有`parent`。该值设置为`time`。

### `[explicit] QDateTimeEdit::QDateTimeEdit(const QDateTime &datetime, QWidget *parent = nullptr)`

**作用与语义：**

构建一个空的日期时间编辑器，并带有`parent`。该值设置为`datetime`。

### `[virtual noexcept] QDateTimeEdit::~QDateTimeEdit()`

**作用与语义：**

毁灭者。

### `QCalendar QDateTimeEdit::calendar() const`

**作用与语义：**

报告该小部件正在使用的日历系统。

### `QCalendarWidget *QDateTimeEdit::calendarWidget() const`

**作用与语义：**

如果`calendarPopup`设置为true且（sections() & `DateSections_Mask`） ！= 0，则返回编辑器的日历小部件。
如果没有设置日历小部件，该函数会创建并返回一个日历小部件。

### `[override virtual] void QDateTimeEdit::clear()`

**作用与语义：**

重装：`QAbstractSpinBox::clear()`。
清除行编辑中除前缀和后缀外的所有文本。

### `QDate QDateTimeEdit::date() const`

**作用与语义：**

返回日期时间编辑。
注意：产权日期的获取函数。

### `[signal] void QDateTimeEdit::dateChanged(QDate date)`

**作用与语义：**

该属性包含了控件中设置的`QDate`。
默认情况下，该物业包含一个指向2000年1月1日的日期。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `date` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QDateTimeEdit::dateTimeChanged(const QDateTime &datetime)`

**作用与语义：**

该属性表示`QDateTimeEdit`中所设定的`QDateTime`。
设置该属性时，新 `QDateTime` 转换为`QDateTimeEdit`的时间系统，因此时间系统保持不变。
默认情况下，该属性设置为2000 CE的开始。它只能设置为有效的`QDateTime`值。如果任何操作导致该属性的日期-时间值为无效，则重置为`minimumDateTime`属性的值。
如果`QDateTimeEdit`没有日期字段，设置该属性会使小部件的日期范围以该属性新值的日期开始和结束。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `dateTime` 的变化，不要把它当作普通函数主动调用。

### `[virtual protected] QDateTime QDateTimeEdit::dateTimeFromText(const QString &text) const`

**作用与语义：**

返回给定`text`的适当日期时间。
当datetime编辑需要解释用户输入的文本作为值时，会使用这个虚拟功能。

### `[override virtual] bool QDateTimeEdit::event(QEvent *event)`

**作用与语义：**

重装：`QAbstractSpinBox::event`（QEvent *事件）。

### `[override virtual protected] void QDateTimeEdit::fixup(QString &input) const`

**作用与语义：**

重构：`QAbstractSpinBox::fixup`（QString & input） const.
如果`input`未被验证`QValidator::Acceptable`，当按下Return或`interpretText()`调用时，`QAbstractSpinBox`会调用该虚拟函数。它会尝试修改文本使其有效。在各个子类中重新实现。

### `[override virtual protected] void QDateTimeEdit::focusInEvent(QFocusEvent *event)`

**作用与语义：**

重实现自：`QAbstractSpinBox::focusInEvent`（QFocusEvent *event）。

### `[override virtual protected] bool QDateTimeEdit::focusNextPrevChild(bool next)`

**作用与语义：**

重构：`QWidget::focusNextPrevChild`（下一个布尔）。
根据 Tab 和 Shift Tab 找到一个新的控件来给键盘焦点，如果能找到新控件，则返回 `true`，找不到则返回 false。
如果`next`为真，该函数向前搜索;如果`next`为假，则向后搜索。
有时，你会想重新实现这个函数。例如，浏览器可能会重新实现它，将“当前活跃链接”向前或向后移动，只有当它到达“页面”的最后或第一个链接时才调用 focusNextPrevChild()。
子控件调用其父控件的 focusNextPrevChild()，但只有包含子控件的窗口决定将焦点重定向到哪里。通过重新实现该函数，你就能控制所有子控件的焦点遍历。

### `[override virtual protected] void QDateTimeEdit::initStyleOption(QStyleOptionSpinBox *option) const`

**作用与语义：**

重实现自：`QAbstractSpinBox::initStyleOption`（QStyleOptionSpinBox *option） const.
用这个 QDataTimeEdit 中的值初始化`option`。这种方法适用于需要 `QStyleOptionSpinBox` 但不想自己填满所有信息的子类。
用这个`QSpinBox`的值初始化`option`。这种方法适用于需要`QStyleOptionSpinBox`但不想自己填满所有信息的子类。

### `[override virtual protected] void QDateTimeEdit::keyPressEvent(QKeyEvent *event)`

**作用与语义：**

重实现自：`QAbstractSpinBox::keyPressEvent`（QKeyEvent *event）。

### `[override virtual protected] void QDateTimeEdit::mousePressEvent(QMouseEvent *event)`

**作用与语义：**

重实现自：`QAbstractSpinBox::mousePressEvent`（QMouseEvent *event）。

### `[override virtual protected] void QDateTimeEdit::paintEvent(QPaintEvent *event)`

**作用与语义：**

重实现自：`QAbstractSpinBox::paintEvent`（QPaintEvent *event）。

### `QDateTimeEdit::Section QDateTimeEdit::sectionAt(int index) const`

**作用与语义：**

返回`index`段。
如果格式为“yyyy/MM/dd”，sectionAt（0） 返回 `YearSection`，sectionAt（1） 返回 `MonthSection`，sectionAt（2） 返回 `YearSection`，。

### `QString QDateTimeEdit::sectionText(QDateTimeEdit::Section section) const`

**作用与语义：**

返回给定`section`的文本。

### `void QDateTimeEdit::setCalendar(QCalendar calendar)`

**作用与语义：**

将`calendar`设置为该小部件使用的日历系统。
该小部件可以使用任何支持的历法系统。默认情况下，它使用格里高利历。

### `void QDateTimeEdit::setCalendarWidget(QCalendarWidget *calendarWidget)`

**作用与语义：**

将给定的`calendarWidget`设置为日历弹窗的控件。编辑器不会自动拥有该日历控件的所有权。
注意：在设置日历小部件之前，必须将`calendarPopup`设置为true。

### `void QDateTimeEdit::setDateRange(QDate min, QDate max)`

**作用与语义：**

设置日期时间编辑时允许的日期范围。
该便利函数设定`minimumDate`和`maximumDate`属性。
类似于：
如果`min`或`max`无效，该函数不做任何事。该函数保持`minimumTime`属性。如果`max`小于`min`，则新的`maximumDateTime`属性即为新的`minimumDateTime`属性。如果`max`等于`min`且`maximumTime`属性小于`minimumTime`属性，则`maximumTime`属性被设为`minimumTime`属性。否则，保持`maximumTime`属性。
如果该范围比其末期的时间区间更窄，例如跨越月末的一周，用户只能在禁用键盘追踪的情况下将日期编辑到该范围后半部分的日期。

**官方示例：**

```cpp
 setDateRange(min, max);
```

### `void QDateTimeEdit::setDateTimeRange(const QDateTime &min, const QDateTime &max)`

**作用与语义：**

设置允许的日期时间范围以进行日期时间编辑。
该便利函数设定`minimumDateTime`和`maximumDateTime`属性。
类似于：
如果`min`或`max`无效，该函数无效。如果`max`小于`min`，`min`也用作`max`。
如果该范围比其末期的时间区间更窄，例如跨越月末的一周，用户只能在禁用键盘追踪的情况下将日期时间编辑为该范围后期的日期时间。

**官方示例：**

```cpp
 setDateTimeRange(min, max);
```

### `void QDateTimeEdit::setSelectedSection(QDateTimeEdit::Section section)`

**作用与语义：**

选择`section`。如果当前显示的部分中不存在`section`，这个函数就不做任何事。如果`section` `NoSection`，这个函数会取消编辑器中的所有文本。否则，这个函数会将光标和当前部分移动到所选的部分。

### `void QDateTimeEdit::setTimeRange(QTime min, QTime max)`

**作用与语义：**

设置日期时间编辑时允许的时间范围。
该便利函数设定`minimumTime`和`maximumTime`属性。
注意，这些限制仅限制日期时间编辑在`minimumDate`和 `maximumDate` 上的值。当这些日期属性不一致时，`max`之后的时间允许在`maximumDate`之前的日期使用，`min`之前的时间则允许在`minimumDate`之后的日期使用。
类似于：
如果`min`或`max`无效，该函数不做任何事。该函数保持`minimumDate`和`maximumDate`属性。如果这些属性重合且`max`小于`min`，则`min`用作`max`。
如果该范围比其末端的时间区间更窄，例如从十点到一小时，再到同一小时后十点，用户只能在关闭键盘追踪的情况下将时间编辑到音域后段。

**官方示例：**

```cpp
 setTimeRange(min, max);
```

### `[override virtual] QSize QDateTimeEdit::sizeHint() const`

**作用与语义：**

重装：`QAbstractSpinBox::sizeHint()` const.
重新实现了属性的访问函数：`QWidget::sizeHint`。

### `[override virtual] void QDateTimeEdit::stepBy(int steps)`

**作用与语义：**

重实现自：`QAbstractSpinBox::stepBy`（int steps）。
每当用户触发一步时调用的虚拟函数。`steps`参数表示已完成的步数。例如，按`Qt::Key_Down`会触发对`stepBy(-1)`的调用，而按`Qt::Key_PageUp`则会触发对`stepBy(10)`的调用。
如果你对`QAbstractSpinBox`子类，必须重新实现这个函数。注意，即使最终值超出最小值和最大值范围，这个函数仍然被调用。处理这些情况是这个函数的工作。

### `[override virtual protected] QAbstractSpinBox::StepEnabled QDateTimeEdit::stepEnabled() const`

**作用与语义：**

重装：`QAbstractSpinBox::stepEnabled()` const.
虚拟功能决定在任何时刻是否合法。
除非 （stepEnabled() & `StepUpEnabled`） ！= 0，否则向上箭头将被涂成禁用。
默认实现会返回 （`StepUpEnabled`|`StepDownEnabled`） 如果开启了包裹。否则，如果值是最小值>则返回 `StepDownEnabled`;如果值为 < maximum()，则返回 `StepUpEnabled`。
如果你`QAbstractSpinBox`子类，就需要重新实现这个函数。

### `[virtual protected] QString QDateTimeEdit::textFromDateTime(const QDateTime &dateTime) const`

**作用与语义：**

这个虚拟功能由日期时间编辑在需要显示`dateTime`时使用。
如果你重新实现这个，可能也需要重新实现`validate()`。

### `QTime QDateTimeEdit::time() const`

**作用与语义：**

返回日期时间编辑。
注意：属性时间的获取函数。

### `[signal] void QDateTimeEdit::timeChanged(QTime time)`

**作用与语义：**

该属性包含了控件中设置的`QTime`。
默认情况下，该属性包含时间为00：00：00和0毫秒。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `time` 的变化，不要把它当作普通函数主动调用。

### `[override virtual protected] QValidator::State QDateTimeEdit::validate(QString &text, int &pos) const`

**作用与语义：**

重实现自：`QAbstractSpinBox::validate`（QString & input， int and pos） const.
`QAbstractSpinBox`调用该虚拟函数以判断`input`是否有效。`pos`参数表示字符串中的位置。在各个子类中重新实现。

### `[override virtual protected] void QDateTimeEdit::wheelEvent(QWheelEvent *event)`

**作用与语义：**

重实现自：`QAbstractSpinBox::wheelEvent`（QWheelEvent *event）。

### `enum Section { NoSection, AmPmSection, MSecSection, SecondSection, MinuteSection, …, YearSection }`

**作用与语义：**

- `QDateTimeEdit::NoSection`：`0x0000`
- `QDateTimeEdit::AmPmSection`：`0x0001`
- `QDateTimeEdit::MSecSection`：`0x0002`
- `QDateTimeEdit::SecondSection`：`0x0004`
- `QDateTimeEdit::MinuteSection`：`0x0008`
- `QDateTimeEdit::HourSection`：`0x0010`
- `QDateTimeEdit::DaySection`：`0x0100`
- `QDateTimeEdit::MonthSection`：`0x0200`
- `QDateTimeEdit::YearSection`：`0x0400`
Sections 类型是 QFlags 的 typedef<Section>。它存储 Section 值的 OR 组合。

### `flags Sections`

**作用与语义：**

- `QDateTimeEdit::NoSection`：`0x0000`
- `QDateTimeEdit::AmPmSection`：`0x0001`
- `QDateTimeEdit::MSecSection`：`0x0002`
- `QDateTimeEdit::SecondSection`：`0x0004`
- `QDateTimeEdit::MinuteSection`：`0x0008`
- `QDateTimeEdit::HourSection`：`0x0010`
- `QDateTimeEdit::DaySection`：`0x0100`
- `QDateTimeEdit::MonthSection`：`0x0200`
- `QDateTimeEdit::YearSection`：`0x0400`
Sections 类型是 QFlags 的 typedef<Section>。它存储 Section 值的 OR 组合。

### `bool calendarPopup() const`

**作用与语义：**

该属性包含当前的日历弹出展示模式。
点击箭头按钮后会显示日历弹窗。该属性仅在存在有效日期显示格式时有效。

**如何使用：** 调用 `calendarPopup()` 读取当前值；它不会修改应用状态。

### `void clearMaximumDate()`

**作用与语义：**

该属性拥有日期时间的最大日期。
更改该属性会更新`maximumDateTime`属性的日期，同时保留`maximumTime`属性。设置该属性时，必要时会调整`minimumDate`以确保范围有效。发生这种情况时，如果`minimumTime`属性大于`maximumTime`属性，也会相应调整。否则，对该属性的更改会保留`minimumDateTime`属性。
该属性只能被设置为描述当前`maximumTime`属性使`QDateTime`对象有效日期的有效`QDate`对象。setMaximumDate() 接受的最晚日期是公元9999年末。这是该属性的默认时间。该默认值可以通过`clearMaximumDateTime()`恢复。

**如何使用：** 调用 `clearMaximumDate()` 读取当前值；它不会修改应用状态。

### `void clearMaximumDateTime()`

**作用与语义：**

该属性包含日期时间编辑的最大日期时间。
更改该属性隐式地将`maximumDate`和`maximumTime`属性分别更新为该属性的日期和时间部分。设置该属性时，如有必要，`minimumDateTime`会调整以确保该范围有效。否则，更改该属性则保持`minimumDateTime`属性。
该属性只能设置为有效的`QDateTime`值。setMaximumDateTime() 接受的最晚日期时间为公元9999年末。这是该属性的默认值。该默认值可用 clearMaximumDateTime() 恢复。

**如何使用：** 调用 `clearMaximumDateTime()` 读取当前值；它不会修改应用状态。

### `void clearMaximumTime()`

**作用与语义：**

该属性包含了日期时间编辑的最大时间。
更改该属性会更新`maximumDateTime`属性的时间，同时保留`minimumDate`和`maximumDate`属性。如果这些属性的日期重合，设置该属性时会调整`minimumTime`属性，以确保范围有效。否则，更改该属性则保持`minimumDateTime`属性。
该属性可以设置为任意有效的`QTime`值。默认情况下，该属性包含时间为23：59：59和999毫秒。该默认值可以通过clearMaximumTime()恢复。

**如何使用：** 调用 `clearMaximumTime()` 读取当前值；它不会修改应用状态。

### `void clearMinimumDate()`

**作用与语义：**

该属性包含日期时间编辑的最小日期。
更改该属性会更新`minimumDateTime`属性的日期，同时保留`minimumTime`属性。设置该属性时，如有必要，`maximumDate`会调整以确保范围保持有效。发生这种情况时，如果`maximumTime`属性小于`minimumTime`属性，也会相应调整。否则，对该属性的更改会保留`maximumDateTime`属性。
该属性只能被设置为描述当前`minimumTime`属性使得有效`QDateTime`对象的有效日期的有效`QDate`对象。setMinimumDate() 接受的最早日期是公元100年的开始。该属性的默认时间为公元1752年9月14日。该默认值可以通过`clearMinimumDateTime()`恢复。

**如何使用：** 调用 `clearMinimumDate()` 读取当前值；它不会修改应用状态。

### `void clearMinimumDateTime()`

**作用与语义：**

该属性包含了日期时间编辑的最小日期时间。
更改该属性隐式地将`minimumDate`和`minimumTime`属性分别更新为该属性的日期和时间部分。设置该属性时，如有必要，会调整`maximumDateTime`以确保该范围有效。否则，更改该属性则保持`maximumDateTime`属性。
该属性只能设置为有效的`QDateTime`值。setMinimumDateTime() 接受的最早日期时间是公元100年的开始。该属性的默认时间是公元1752年9月14日的开始。该默认可以通过 clearMinimumDateTime() 恢复。

**如何使用：** 调用 `clearMinimumDateTime()` 读取当前值；它不会修改应用状态。

### `void clearMinimumTime()`

**作用与语义：**

该属性表示日期时间编辑的最小时间。
更改该属性会更新`minimumDateTime`属性的时间，同时保留`minimumDate`和`maximumDate`属性。如果这些属性的日期重合，设置该属性时会调整`maximumTime`属性，以确保范围有效。否则，更改该属性则保持`maximumDateTime`属性。
该属性可以设置为任意有效的`QTime`值。默认情况下，该属性包含 00：00：00 和 0 毫秒的时间。该默认值可以通过 clearMinimumTime() 恢复。

**如何使用：** 调用 `clearMinimumTime()` 读取当前值；它不会修改应用状态。

### `QDateTimeEdit::Section currentSection() const`

**作用与语义：**

该属性表示当前自旋盒截面。

**如何使用：** 调用 `currentSection()` 读取当前值；它不会修改应用状态。

### `int currentSectionIndex() const`

**作用与语义：**

该属性表示旋量盒当前截面索引。
如果格式是“yyyy/MM/dd”，displayText是“2001/05/21”，cursorPosition是5，currentSectionIndex返回1。如果cursorPosition是3，currentSectionIndex是0，依此类推。

**如何使用：** 调用 `currentSectionIndex()` 读取当前值；它不会修改应用状态。

### `QDateTime dateTime() const`

**作用与语义：**

该属性表示`QDateTimeEdit`中所设定的`QDateTime`。
设置该属性时，新 `QDateTime` 转换为`QDateTimeEdit`的时间系统，因此时间系统保持不变。
默认情况下，该属性设置为2000 CE的开始。它只能设置为有效的`QDateTime`值。如果任何操作导致该属性的日期-时间值为无效，则重置为`minimumDateTime`属性的值。
如果`QDateTimeEdit`没有日期字段，设置该属性会使小部件的日期范围以该属性新值的日期开始和结束。

**如何使用：** 调用 `dateTime()` 读取当前值；它不会修改应用状态。

### `QString displayFormat() const`

**作用与语义：**

该属性保留了显示日期/日期编辑的格式。
该格式在`QDateTime::toString()`和 `QDateTime::fromString()` 中有详细描述。
示例格式字符串（假设日期为1969年7月2日）：
- `Format`：结果
- `dd.MM.yyyy`：1969年7月2日
- `MMM d yy`：1969年7月2日
- `MMMM d yy`：1969年7月2日
请注意，如果你指定两位数年份，它会被解释为编辑日期时间初始化的世纪。默认的世纪是第21世纪（2000-2099）。
如果你指定了无效格式，格式将不会被设置。

**如何使用：** 调用 `displayFormat()` 读取当前值；它不会修改应用状态。

### `QDateTimeEdit::Sections displayedSections() const`

**作用与语义：**

该属性保存了日期时间编辑中当前显示的字段。
返回该格式显示的部分的位集。

**如何使用：** 调用 `displayedSections()` 读取当前值；它不会修改应用状态。

### `QDate maximumDate() const`

**作用与语义：**

该属性拥有日期时间的最大日期。
更改该属性会更新`maximumDateTime`属性的日期，同时保留`maximumTime`属性。设置该属性时，必要时会调整`minimumDate`以确保范围有效。发生这种情况时，如果`minimumTime`属性大于`maximumTime`属性，也会相应调整。否则，对该属性的更改会保留`minimumDateTime`属性。
该属性只能被设置为描述当前`maximumTime`属性使`QDateTime`对象有效日期的有效`QDate`对象。setMaximumDate() 接受的最晚日期是公元9999年末。这是该属性的默认时间。该默认值可以通过`clearMaximumDateTime()`恢复。

**如何使用：** 调用 `maximumDate()` 读取当前值；它不会修改应用状态。

### `QDateTime maximumDateTime() const`

**作用与语义：**

该属性包含日期时间编辑的最大日期时间。
更改该属性隐式地将`maximumDate`和`maximumTime`属性分别更新为该属性的日期和时间部分。设置该属性时，如有必要，`minimumDateTime`会调整以确保该范围有效。否则，更改该属性则保持`minimumDateTime`属性。
该属性只能设置为有效的`QDateTime`值。setMaximumDateTime() 接受的最晚日期时间为公元9999年末。这是该属性的默认值。该默认值可用 clearMaximumDateTime() 恢复。

**如何使用：** 调用 `maximumDateTime()` 读取当前值；它不会修改应用状态。

### `QTime maximumTime() const`

**作用与语义：**

该属性包含了日期时间编辑的最大时间。
更改该属性会更新`maximumDateTime`属性的时间，同时保留`minimumDate`和`maximumDate`属性。如果这些属性的日期重合，设置该属性时会调整`minimumTime`属性，以确保范围有效。否则，更改该属性则保持`minimumDateTime`属性。
该属性可以设置为任意有效的`QTime`值。默认情况下，该属性包含时间为23：59：59和999毫秒。该默认值可以通过clearMaximumTime()恢复。

**如何使用：** 调用 `maximumTime()` 读取当前值；它不会修改应用状态。

### `QDate minimumDate() const`

**作用与语义：**

该属性包含日期时间编辑的最小日期。
更改该属性会更新`minimumDateTime`属性的日期，同时保留`minimumTime`属性。设置该属性时，如有必要，`maximumDate`会调整以确保范围保持有效。发生这种情况时，如果`maximumTime`属性小于`minimumTime`属性，也会相应调整。否则，对该属性的更改会保留`maximumDateTime`属性。
该属性只能被设置为描述当前`minimumTime`属性使得有效`QDateTime`对象的有效日期的有效`QDate`对象。setMinimumDate() 接受的最早日期是公元100年的开始。该属性的默认时间为公元1752年9月14日。该默认值可以通过`clearMinimumDateTime()`恢复。

**如何使用：** 调用 `minimumDate()` 读取当前值；它不会修改应用状态。

### `QDateTime minimumDateTime() const`

**作用与语义：**

该属性包含了日期时间编辑的最小日期时间。
更改该属性隐式地将`minimumDate`和`minimumTime`属性分别更新为该属性的日期和时间部分。设置该属性时，如有必要，会调整`maximumDateTime`以确保该范围有效。否则，更改该属性则保持`maximumDateTime`属性。
该属性只能设置为有效的`QDateTime`值。setMinimumDateTime() 接受的最早日期时间是公元100年的开始。该属性的默认时间是公元1752年9月14日的开始。该默认可以通过 clearMinimumDateTime() 恢复。

**如何使用：** 调用 `minimumDateTime()` 读取当前值；它不会修改应用状态。

### `QTime minimumTime() const`

**作用与语义：**

该属性表示日期时间编辑的最小时间。
更改该属性会更新`minimumDateTime`属性的时间，同时保留`minimumDate`和`maximumDate`属性。如果这些属性的日期重合，设置该属性时会调整`maximumTime`属性，以确保范围有效。否则，更改该属性则保持`maximumDateTime`属性。
该属性可以设置为任意有效的`QTime`值。默认情况下，该属性包含 00：00：00 和 0 毫秒的时间。该默认值可以通过 clearMinimumTime() 恢复。

**如何使用：** 调用 `minimumTime()` 读取当前值；它不会修改应用状态。

### `int sectionCount() const`

**作用与语义：**

该属性包含显示的分段数量。如果格式为“yyyy/yy/yyyy”，sectionCount返回3。

**如何使用：** 调用 `sectionCount()` 读取当前值；它不会修改应用状态。

### `void setCalendarPopup(bool enable)`

**作用与语义：**

该属性包含当前的日历弹出展示模式。
点击箭头按钮后会显示日历弹窗。该属性仅在存在有效日期显示格式时有效。

**如何使用：** 调用 `setCalendarPopup(...)` 修改 `calendarPopup`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setCurrentSection(QDateTimeEdit::Section section)`

**作用与语义：**

该属性表示当前自旋盒截面。

**如何使用：** 调用 `setCurrentSection(...)` 修改 `currentSection`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setCurrentSectionIndex(int index)`

**作用与语义：**

该属性表示旋量盒当前截面索引。
如果格式是“yyyy/MM/dd”，displayText是“2001/05/21”，cursorPosition是5，currentSectionIndex返回1。如果cursorPosition是3，currentSectionIndex是0，依此类推。

**如何使用：** 调用 `setCurrentSectionIndex(...)` 修改 `currentSectionIndex`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setDisplayFormat(const QString &format)`

**作用与语义：**

该属性保留了显示日期/日期编辑的格式。
该格式在`QDateTime::toString()`和 `QDateTime::fromString()` 中有详细描述。
示例格式字符串（假设日期为1969年7月2日）：
- `Format`：结果
- `dd.MM.yyyy`：1969年7月2日
- `MMM d yy`：1969年7月2日
- `MMMM d yy`：1969年7月2日
请注意，如果你指定两位数年份，它会被解释为编辑日期时间初始化的世纪。默认的世纪是第21世纪（2000-2099）。
如果你指定了无效格式，格式将不会被设置。

**如何使用：** 调用 `setDisplayFormat(...)` 修改 `displayFormat`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMaximumDate(QDate max)`

**作用与语义：**

该属性拥有日期时间的最大日期。
更改该属性会更新`maximumDateTime`属性的日期，同时保留`maximumTime`属性。设置该属性时，必要时会调整`minimumDate`以确保范围有效。发生这种情况时，如果`minimumTime`属性大于`maximumTime`属性，也会相应调整。否则，对该属性的更改会保留`minimumDateTime`属性。
该属性只能被设置为描述当前`maximumTime`属性使`QDateTime`对象有效日期的有效`QDate`对象。setMaximumDate() 接受的最晚日期是公元9999年末。这是该属性的默认时间。该默认值可以通过`clearMaximumDateTime()`恢复。

**如何使用：** 调用 `setMaximumDate(...)` 修改 `maximumDate`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMaximumDateTime(const QDateTime &dt)`

**作用与语义：**

该属性包含日期时间编辑的最大日期时间。
更改该属性隐式地将`maximumDate`和`maximumTime`属性分别更新为该属性的日期和时间部分。设置该属性时，如有必要，`minimumDateTime`会调整以确保该范围有效。否则，更改该属性则保持`minimumDateTime`属性。
该属性只能设置为有效的`QDateTime`值。setMaximumDateTime() 接受的最晚日期时间为公元9999年末。这是该属性的默认值。该默认值可用 clearMaximumDateTime() 恢复。

**如何使用：** 调用 `setMaximumDateTime(...)` 修改 `maximumDateTime`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMaximumTime(QTime max)`

**作用与语义：**

该属性包含了日期时间编辑的最大时间。
更改该属性会更新`maximumDateTime`属性的时间，同时保留`minimumDate`和`maximumDate`属性。如果这些属性的日期重合，设置该属性时会调整`minimumTime`属性，以确保范围有效。否则，更改该属性则保持`minimumDateTime`属性。
该属性可以设置为任意有效的`QTime`值。默认情况下，该属性包含时间为23：59：59和999毫秒。该默认值可以通过clearMaximumTime()恢复。

**如何使用：** 调用 `setMaximumTime(...)` 修改 `maximumTime`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMinimumDate(QDate min)`

**作用与语义：**

该属性包含日期时间编辑的最小日期。
更改该属性会更新`minimumDateTime`属性的日期，同时保留`minimumTime`属性。设置该属性时，如有必要，`maximumDate`会调整以确保范围保持有效。发生这种情况时，如果`maximumTime`属性小于`minimumTime`属性，也会相应调整。否则，对该属性的更改会保留`maximumDateTime`属性。
该属性只能被设置为描述当前`minimumTime`属性使得有效`QDateTime`对象的有效日期的有效`QDate`对象。setMinimumDate() 接受的最早日期是公元100年的开始。该属性的默认时间为公元1752年9月14日。该默认值可以通过`clearMinimumDateTime()`恢复。

**如何使用：** 调用 `setMinimumDate(...)` 修改 `minimumDate`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMinimumDateTime(const QDateTime &dt)`

**作用与语义：**

该属性包含了日期时间编辑的最小日期时间。
更改该属性隐式地将`minimumDate`和`minimumTime`属性分别更新为该属性的日期和时间部分。设置该属性时，如有必要，会调整`maximumDateTime`以确保该范围有效。否则，更改该属性则保持`maximumDateTime`属性。
该属性只能设置为有效的`QDateTime`值。setMinimumDateTime() 接受的最早日期时间是公元100年的开始。该属性的默认时间是公元1752年9月14日的开始。该默认可以通过 clearMinimumDateTime() 恢复。

**如何使用：** 调用 `setMinimumDateTime(...)` 修改 `minimumDateTime`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMinimumTime(QTime min)`

**作用与语义：**

该属性表示日期时间编辑的最小时间。
更改该属性会更新`minimumDateTime`属性的时间，同时保留`minimumDate`和`maximumDate`属性。如果这些属性的日期重合，设置该属性时会调整`maximumTime`属性，以确保范围有效。否则，更改该属性则保持`maximumDateTime`属性。
该属性可以设置为任意有效的`QTime`值。默认情况下，该属性包含 00：00：00 和 0 毫秒的时间。该默认值可以通过 clearMinimumTime() 恢复。

**如何使用：** 调用 `setMinimumTime(...)` 修改 `minimumTime`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTimeZone(const QTimeZone &zone)`

**作用与语义：**

该属性包含 datetime 编辑控件当前使用的时区。
如果使用的日期时间格式包含时区指示器——即`t`、`tt`、`ttt`或`tttt`格式指定符——用户输入在解析时会在该时区重新表达，覆盖用户可能指定的任何时区。

**如何使用：** 调用 `setTimeZone(...)` 修改 `timeZone`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QTimeZone timeZone() const`

**作用与语义：**

该属性包含 datetime 编辑控件当前使用的时区。
如果使用的日期时间格式包含时区指示器——即`t`、`tt`、`ttt`或`tttt`格式指定符——用户输入在解析时会在该时区重新表达，覆盖用户可能指定的任何时区。

**如何使用：** 调用 `timeZone()` 读取当前值；它不会修改应用状态。

### `void setDate(QDate date)`

**作用与语义：**

该属性包含了控件中设置的`QDate`。
默认情况下，该物业包含一个指向2000年1月1日的日期。

**如何使用：** 调用 `setDate(...)` 修改 `date`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setDateTime(const QDateTime &dateTime)`

**作用与语义：**

该属性表示`QDateTimeEdit`中所设定的`QDateTime`。
设置该属性时，新 `QDateTime` 转换为`QDateTimeEdit`的时间系统，因此时间系统保持不变。
默认情况下，该属性设置为2000 CE的开始。它只能设置为有效的`QDateTime`值。如果任何操作导致该属性的日期-时间值为无效，则重置为`minimumDateTime`属性的值。
如果`QDateTimeEdit`没有日期字段，设置该属性会使小部件的日期范围以该属性新值的日期开始和结束。

**如何使用：** 调用 `setDateTime(...)` 修改 `dateTime`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTime(QTime time)`

**作用与语义：**

该属性包含了控件中设置的`QTime`。
默认情况下，该属性包含时间为00：00：00和0毫秒。

**如何使用：** 调用 `setTime(...)` 修改 `time`；传入的新值会成为后续查询和相关界面行为所使用的值。

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

`QDateTimeEdit` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
