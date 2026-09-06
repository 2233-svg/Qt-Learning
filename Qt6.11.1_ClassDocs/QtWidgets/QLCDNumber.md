# QLCDNumber

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QLCDNumber` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QLCDNumber` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QLCDNumber>`
- 继承自：QFrame
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

- `enum Mode { Hex, Dec, Oct, Bin }`
- `enum SegmentStyle { Outline, Filled, Flat }`

### 属性

- `digitCount : int`
- `intValue : int`
- `mode : Mode`
- `segmentStyle : SegmentStyle`
- `smallDecimalPoint : bool`
- `value : double`

### 公有函数

- `QLCDNumber(QWidget *parent = nullptr)`
- `QLCDNumber(uint numDigits, QWidget *parent = nullptr)`
- `virtual ~QLCDNumber()`
- `bool checkOverflow(double num) const`
- `bool checkOverflow(int num) const`
- `int digitCount() const`
- `int intValue() const`
- `QLCDNumber::Mode mode() const`
- `QLCDNumber::SegmentStyle segmentStyle() const`
- `void setDigitCount(int numDigits)`
- `void setMode(QLCDNumber::Mode)`
- `void setSegmentStyle(QLCDNumber::SegmentStyle)`
- `bool smallDecimalPoint() const`
- `double value() const`

### 重实现的公有函数

- `virtual QSize sizeHint() const override`

### 公有槽函数

- `void display(const QString &s)`
- `void display(double num)`
- `void display(int num)`
- `void setBinMode()`
- `void setDecMode()`
- `void setHexMode()`
- `void setOctMode()`
- `void setSmallDecimalPoint(bool)`

### 信号

- `void overflow()`

### 重实现的保护函数

- `virtual bool event(QEvent *e) override`
- `virtual void paintEvent(QPaintEvent *) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QLCDNumber::Mode`

**作用与语义：**

这种类型决定了数字的显示方式。
- `QLCDNumber::Hex`：`0`;十六进制
- `QLCDNumber::Dec`：`1`;十进制
- `QLCDNumber::Oct`：`2`;八进制
- `QLCDNumber::Bin`：`3`;二进制
如果显示设置为十六进制、八进制或二进制，则显示该值的整数等价值。

### `enum QLCDNumber::SegmentStyle`

**作用与语义：**

这种类型决定了`QLCDNumber`小部件的视觉外观。
- `QLCDNumber::Outline`：`0`;给出填充背景色的凸起部分。
- `QLCDNumber::Filled`：`1`;给出填充 windowText 颜色的凸起段。
- `QLCDNumber::Flat`：`2`;给出填充 windowText 颜色的平面段。

### `digitCount : int`

**作用与语义：**

该属性包含当前显示的数字数。
对应当前数字。如果`QLCDNumber::smallDecimalPoint`为假，小数点占据一个数字位置。
默认情况下，该属性包含5的值。

**如何使用：** 调用 `digitCount()` 读取当前值；它不会修改应用状态。

### `intValue : int`

**作用与语义：**

该属性将显示值四舍五入至最接近的整数。
该属性对应于LCDNumber显示的当前值最接近的整数。这是用于十六进制、八进制和二进制模式的值。
如果显示的值不是数字，则该属性的值为0。
默认情况下，该属性的值为0。

**如何使用：** 调用 `intValue()` 读取当前值；它不会修改应用状态。

### `mode : Mode`

**作用与语义：**

该属性表示当前显示模式（数字基数）。
对应当前显示模式，包括`Bin`、`Oct`、`Dec`（默认）和`Hex`。`Dec`模式可以显示浮点数值，其他模式显示整数等效值。

**如何使用：** 调用 `mode()` 读取当前值；它不会修改应用状态。

### `segmentStyle : SegmentStyle`

**作用与语义：**

该物业拥有LCDNumber的风格。
- `Style`：结果
- `Outline`：产生填充背景色的凸起段
- `Filled`（默认）。'：生成填充前景色的凸起段。
- `Flat`：产生填充前景色的平面段。
`Outline`和`Filled`还会用`QPalette::light()`和`QPalette::dark()`来做阴影效果。

**如何使用：** 调用 `segmentStyle()` 读取当前值；它不会修改应用状态。

### `smallDecimalPoint : bool`

**作用与语义：**

该属性表示小数点的样式。
如果为真，小数点位于两个数字位置之间。否则它占据独立的数字位置，即绘制在数字位置。默认为假。
当数字之间的小数点被画出时，数字间距会稍微变宽。

**如何使用：** 调用 `smallDecimalPoint()` 读取当前值；它不会修改应用状态。

### `value : double`

**作用与语义：**

该属性表示显示价值。
该属性对应于LCDNumber显示的当前值。
如果显示的值不是数字，则该属性的值为0。
默认情况下，该属性的值为0。

**如何使用：** 调用 `value()` 读取当前值；它不会修改应用状态。

### `[explicit] QLCDNumber::QLCDNumber(QWidget *parent = nullptr)`

**作用与语义：**

构建液晶数字，将数字数设置为5，底部为十进制，小数点模式为“小”，框架样式为凸起方格。`segmentStyle()`设置为`Outline`。
`parent`参数传递给`QFrame`构造器。

### `[explicit] QLCDNumber::QLCDNumber(uint numDigits, QWidget *parent = nullptr)`

**作用与语义：**

构建LCD编号，将数字数设置为`numDigits`，底部为十进制，小数点模式为“小”，框架样式为凸起方格。`segmentStyle()`设置为`Filled`。
`parent`参数传递给`QFrame`构造函数。

### `[virtual noexcept] QLCDNumber::~QLCDNumber()`

**作用与语义：**

会破坏LCD编号。

### `bool QLCDNumber::checkOverflow(double num) const`

**作用与语义：**

如果`num`太大无法完整显示，则返回`true`;否则返回`false`。

### `bool QLCDNumber::checkOverflow(int num) const`

**作用与语义：**

如果`num`太大无法完整显示，则返回`true`;否则返回`false`。

### `int QLCDNumber::digitCount() const`

**作用与语义：**

返回当前数字数。
注意：属性 digitCount 的 Getter 函数。

### `[slot] void QLCDNumber::display(const QString &s)`

**作用与语义：**

该属性将显示值四舍五入至最接近的整数。
该属性对应于LCDNumber显示的当前值最接近的整数。这是用于十六进制、八进制和二进制模式的值。
如果显示的值不是数字，则该属性的值为0。
默认情况下，该属性的值为0。

**如何使用：** 调用 `display()` 读取当前值；它不会修改应用状态。

### `[slot] void QLCDNumber::display(double num)`

**作用与语义：**

该属性将显示值四舍五入至最接近的整数。
该属性对应于LCDNumber显示的当前值最接近的整数。这是用于十六进制、八进制和二进制模式的值。
如果显示的值不是数字，则该属性的值为0。
默认情况下，该属性的值为0。

**如何使用：** 调用 `display()` 读取当前值；它不会修改应用状态。

### `[slot] void QLCDNumber::display(int num)`

**作用与语义：**

该属性将显示值四舍五入至最接近的整数。
该属性对应于LCDNumber显示的当前值最接近的整数。这是用于十六进制、八进制和二进制模式的值。
如果显示的值不是数字，则该属性的值为0。
默认情况下，该属性的值为0。

**如何使用：** 调用 `display()` 读取当前值；它不会修改应用状态。

### `[override virtual protected] bool QLCDNumber::event(QEvent *e)`

**作用与语义：**

重实现自：`QFrame::event`（QEvent *e）。

### `[signal] void QLCDNumber::overflow()`

**作用与语义：**

每当`QLCDNumber`被要求显示过大数字或字符串过长时，都会发出该信号。
它从未由`setDigitCount()`发出。

### `[override virtual protected] void QLCDNumber::paintEvent(QPaintEvent *)`

**作用与语义：**

重实现自：`QFrame::paintEvent`（QPaintEvent *）。

### `[slot] void QLCDNumber::setBinMode()`

**作用与语义：**

调用 `setMode`（Bin）。为方便提供（例如连接按钮）。

### `[slot] void QLCDNumber::setDecMode()`

**作用与语义：**

调用`setMode`（12月）。为方便提供（例如连接按钮）。

### `void QLCDNumber::setDigitCount(int numDigits)`

**作用与语义：**

该属性包含当前显示的数字数。
对应当前数字。如果`QLCDNumber::smallDecimalPoint`为假，小数点占据一个数字位置。
默认情况下，该属性包含5的值。

**如何使用：** 调用 `setDigitCount(...)` 修改 `digitCount`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `[slot] void QLCDNumber::setHexMode()`

**作用与语义：**

调用`setMode`（六边形）。为方便而提供（例如连接按钮）。

### `[slot] void QLCDNumber::setOctMode()`

**作用与语义：**

调用时间`setMode`（10月）。为方便提供（例如连接按钮）。

### `[override virtual] QSize QLCDNumber::sizeHint() const`

**作用与语义：**

重实现自：`QFrame::sizeHint()` const.
重新实现了属性的访问函数：`QWidget::sizeHint`。

### `int intValue() const`

**作用与语义：**

该属性将显示值四舍五入至最接近的整数。
该属性对应于LCDNumber显示的当前值最接近的整数。这是用于十六进制、八进制和二进制模式的值。
如果显示的值不是数字，则该属性的值为0。
默认情况下，该属性的值为0。

**如何使用：** 调用 `intValue()` 读取当前值；它不会修改应用状态。

### `QLCDNumber::Mode mode() const`

**作用与语义：**

该属性表示当前显示模式（数字基数）。
对应当前显示模式，包括`Bin`、`Oct`、`Dec`（默认）和`Hex`。`Dec`模式可以显示浮点数值，其他模式显示整数等效值。

**如何使用：** 调用 `mode()` 读取当前值；它不会修改应用状态。

### `QLCDNumber::SegmentStyle segmentStyle() const`

**作用与语义：**

该物业拥有LCDNumber的风格。
- `Style`：结果
- `Outline`：产生填充背景色的凸起段
- `Filled`（默认）。'：生成填充前景色的凸起段。
- `Flat`：产生填充前景色的平面段。
`Outline`和`Filled`还会用`QPalette::light()`和`QPalette::dark()`来做阴影效果。

**如何使用：** 调用 `segmentStyle()` 读取当前值；它不会修改应用状态。

### `void setMode(QLCDNumber::Mode)`

**作用与语义：**

该属性表示当前显示模式（数字基数）。
对应当前显示模式，包括`Bin`、`Oct`、`Dec`（默认）和`Hex`。`Dec`模式可以显示浮点数值，其他模式显示整数等效值。

**如何使用：** 调用 `setMode(...)` 修改 `mode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setSegmentStyle(QLCDNumber::SegmentStyle)`

**作用与语义：**

该物业拥有LCDNumber的风格。
- `Style`：结果
- `Outline`：产生填充背景色的凸起段
- `Filled`（默认）。'：生成填充前景色的凸起段。
- `Flat`：产生填充前景色的平面段。
`Outline`和`Filled`还会用`QPalette::light()`和`QPalette::dark()`来做阴影效果。

**如何使用：** 调用 `setSegmentStyle(...)` 修改 `segmentStyle`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `bool smallDecimalPoint() const`

**作用与语义：**

该属性表示小数点的样式。
如果为真，小数点位于两个数字位置之间。否则它占据独立的数字位置，即绘制在数字位置。默认为假。
当数字之间的小数点被画出时，数字间距会稍微变宽。

**如何使用：** 调用 `smallDecimalPoint()` 读取当前值；它不会修改应用状态。

### `double value() const`

**作用与语义：**

该属性表示显示价值。
该属性对应于LCDNumber显示的当前值。
如果显示的值不是数字，则该属性的值为0。
默认情况下，该属性的值为0。

**如何使用：** 调用 `value()` 读取当前值；它不会修改应用状态。

### `void setSmallDecimalPoint(bool)`

**作用与语义：**

该属性表示小数点的样式。
如果为真，小数点位于两个数字位置之间。否则它占据独立的数字位置，即绘制在数字位置。默认为假。
当数字之间的小数点被画出时，数字间距会稍微变宽。

**如何使用：** 调用 `setSmallDecimalPoint(...)` 修改 `smallDecimalPoint`；传入的新值会成为后续查询和相关界面行为所使用的值。

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

`QLCDNumber` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
