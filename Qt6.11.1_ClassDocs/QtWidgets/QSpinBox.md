# QSpinBox

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QSpinBox` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QSpinBox` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QSpinBox>`
- 继承自：QAbstractSpinBox
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

### 属性

- `cleanText : QString`
- `displayIntegerBase : int`
- `maximum : int`
- `minimum : int`
- `prefix : QString`
- `singleStep : int`
- `stepType : StepType`
- `suffix : QString`
- `value : int`

### 公有函数

- `QSpinBox(QWidget *parent = nullptr)`
- `virtual ~QSpinBox()`
- `QString cleanText() const`
- `int displayIntegerBase() const`
- `int maximum() const`
- `int minimum() const`
- `QString prefix() const`
- `void setDisplayIntegerBase(int base)`
- `void setMaximum(int max)`
- `void setMinimum(int min)`
- `void setPrefix(const QString &prefix)`
- `void setRange(int minimum, int maximum)`
- `void setSingleStep(int val)`
- `void setStepType(QAbstractSpinBox::StepType stepType)`
- `void setSuffix(const QString &suffix)`
- `int singleStep() const`
- `QAbstractSpinBox::StepType stepType() const`
- `QString suffix() const`
- `int value() const`

### 公有槽函数

- `void setValue(int val)`

### 信号

- `void textChanged(const QString &text)`
- `void valueChanged(int i)`

### 保护函数

- `virtual QString textFromValue(int value) const`
- `virtual int valueFromText(const QString &text) const`

### 重实现的保护函数

- `virtual bool event(QEvent *event) override`
- `virtual void fixup(QString &input) const override`
- `virtual QValidator::State validate(QString &text, int &pos) const override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[read-only] cleanText : QString`

**作用与语义：**

该属性包含旋转盒的文本，排除任何前缀、后缀或前置或后置空白。

**如何使用：** 调用 `cleanText()` 读取当前值；它不会修改应用状态。

### `displayIntegerBase : int`

**作用与语义：**

该属性表示了用来表示自旋盒值的基数。
默认的 displayIntegerBase 值是 10。

**如何使用：** 调用 `displayIntegerBase()` 读取当前值；它不会修改应用状态。

### `maximum : int`

**作用与语义：**

该属性表示自旋盒的最大值。
设置该属性时，如有必要会调整最小值，以确保范围有效。
默认的最大数值是99。

**如何使用：** 调用 `maximum()` 读取当前值；它不会修改应用状态。

### `minimum : int`

**作用与语义：**

该属性表示自旋盒的最小值。
设置该属性时，如有必要会调整`maximum`以确保范围有效。
默认最低值是0。

**如何使用：** 调用 `minimum()` 读取当前值；它不会修改应用状态。

### `prefix : QString`

**作用与语义：**

该属性表示自旋盒的前缀。
前缀会加在显示值的开头。典型用途是显示计量单位或货币符号。例如：
要关闭前缀显示，将该属性设置为空字符串。默认为无前缀。当 `value()` == `minimum()` 且 `specialValueText()` 被设置时，前缀不会显示。
如果未设置前缀，前缀()返回空字符串。

**如何使用：** 调用 `prefix()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 sb->setPrefix("$");
```

### `singleStep : int`

**作用与语义：**

该属性表示步长值。
当用户使用箭头更改旋转盒的值时，值会根据 singleStep 的数量递增或减少。默认值是 1。将 singleStep 值设为小于 0 则无效。

**如何使用：** 调用 `singleStep()` 读取当前值；它不会修改应用状态。

### `stepType : StepType`

**作用与语义：**

该属性表示 阶梯类型。
步进类型可以是单步或自适应十进制步。

**如何使用：** 调用 `stepType()` 读取当前值；它不会修改应用状态。

### `suffix : QString`

**作用与语义：**

该属性表示旋量盒的后缀。
后缀附加在显示值的末尾。典型用途是显示计量单位或货币符号。例如：
要关闭后缀显示，将该属性设置为空字符串。默认情况下无后缀。如果`specialValueText()`设置，后缀不会在`minimum()`中显示。
如果没有设置后缀，后缀()返回一个空字符串。

**如何使用：** 调用 `suffix()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 sb->setSuffix(" km");
```

### `value : int`

**作用与语义：**

该属性表示自旋盒的值。
如果新值与旧值不同，setValue() 会发出 `valueChanged()`。value 属性带有第二个通知信号，包含旋转盒的前缀和后缀。

**如何使用：** 调用 `value()` 读取当前值；它不会修改应用状态。

### `[explicit] QSpinBox::QSpinBox(QWidget *parent = nullptr)`

**作用与语义：**

构造一个最小值为0、最大值为99的自旋盒，步长值为1。该值最初设为0。其父值为`parent`。

### `[virtual noexcept] QSpinBox::~QSpinBox()`

**作用与语义：**

毁灭者。

### `[override virtual protected] bool QSpinBox::event(QEvent *event)`

**作用与语义：**

重装：`QAbstractSpinBox::event`（QEvent *事件）。

### `[override virtual protected] void QSpinBox::fixup(QString &input) const`

**作用与语义：**

重构：`QAbstractSpinBox::fixup`（QString & input） const.
如果`input`未被验证`QValidator::Acceptable`，当按下Return或`interpretText()`调用时，`QAbstractSpinBox`会调用该虚拟函数。它会尝试修改文本使其有效。在各个子类中重新实现。

### `void QSpinBox::setRange(int minimum, int maximum)`

**作用与语义：**

方便函数用来设置 `minimum`，并用一个函数调用`maximum`值。
等价于：

**官方示例：**

```cpp
 setRange(minimum, maximum);
```

### `void QSpinBox::setStepType(QAbstractSpinBox::StepType stepType)`

**作用与语义：**

该属性表示 阶梯类型。
步进类型可以是单步或自适应十进制步。

**如何使用：** 调用 `setStepType(...)` 修改 `stepType`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `[signal] void QSpinBox::textChanged(const QString &text)`

**作用与语义：**

每当旋转盒的文本发生变化时，该信号都会发出。新文本以与`prefix()`和`suffix()`的 `text` 传递。

### `[virtual protected] QString QSpinBox::textFromValue(int value) const`

**作用与语义：**

当旋转盒需要显示给定`value`时，会使用这个虚拟函数。默认实现返回包含`value`的字符串，按照标准方式使用 `QWidget::locale()`。`toString()`，但除非设置了千分隔符`setGroupSeparatorShown()`。重实现可以返回任何内容。（详见详细描述中的示例。）。
注意：`QSpinBox` 不调用该函数`specialValueText()`，返回值中不应包含`prefix()`和`suffix()`。
如果你重新实现这个，可能还需要重新实现 `valueFromText()` 和 `validate()`。

### `[override virtual protected] QValidator::State QSpinBox::validate(QString &text, int &pos) const`

**作用与语义：**

重实现自：`QAbstractSpinBox::validate`（QString & input， int and pos） const.
`QAbstractSpinBox`调用该虚拟函数以判断`input`是否有效。`pos`参数表示字符串中的位置。在各个子类中重新实现。

### `[signal] void QSpinBox::valueChanged(int i)`

**作用与语义：**

该属性表示自旋盒的值。
如果新值与旧值不同，setValue() 会发出 `valueChanged()`。value 属性带有第二个通知信号，包含旋转盒的前缀和后缀。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `value` 的变化，不要把它当作普通函数主动调用。

### `[virtual protected] int QSpinBox::valueFromText(const QString &text) const`

**作用与语义：**

当旋转盒需要将用户输入的`text`解释为一个值时，就会使用这个虚拟函数。
需要以非数字方式显示自旋盒值的子类需要重新实现这个函数。
注意：`QSpinBox` 单独处理`specialValueText()`;该函数只涉及其他值。

### `QString cleanText() const`

**作用与语义：**

该属性包含旋转盒的文本，排除任何前缀、后缀或前置或后置空白。

**如何使用：** 调用 `cleanText()` 读取当前值；它不会修改应用状态。

### `int displayIntegerBase() const`

**作用与语义：**

该属性表示了用来表示自旋盒值的基数。
默认的 displayIntegerBase 值是 10。

**如何使用：** 调用 `displayIntegerBase()` 读取当前值；它不会修改应用状态。

### `int maximum() const`

**作用与语义：**

该属性表示自旋盒的最大值。
设置该属性时，如有必要会调整最小值，以确保范围有效。
默认的最大数值是99。

**如何使用：** 调用 `maximum()` 读取当前值；它不会修改应用状态。

### `int minimum() const`

**作用与语义：**

该属性表示自旋盒的最小值。
设置该属性时，如有必要会调整`maximum`以确保范围有效。
默认最低值是0。

**如何使用：** 调用 `minimum()` 读取当前值；它不会修改应用状态。

### `QString prefix() const`

**作用与语义：**

该属性表示自旋盒的前缀。
前缀会加在显示值的开头。典型用途是显示计量单位或货币符号。例如：
要关闭前缀显示，将该属性设置为空字符串。默认为无前缀。当 `value()` == `minimum()` 且 `specialValueText()` 被设置时，前缀不会显示。
如果未设置前缀，前缀()返回空字符串。

**如何使用：** 调用 `prefix()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 sb->setPrefix("$");
```

### `void setDisplayIntegerBase(int base)`

**作用与语义：**

该属性表示了用来表示自旋盒值的基数。
默认的 displayIntegerBase 值是 10。

**如何使用：** 调用 `setDisplayIntegerBase(...)` 修改 `displayIntegerBase`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMaximum(int max)`

**作用与语义：**

该属性表示自旋盒的最大值。
设置该属性时，如有必要会调整最小值，以确保范围有效。
默认的最大数值是99。

**如何使用：** 调用 `setMaximum(...)` 修改 `maximum`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMinimum(int min)`

**作用与语义：**

该属性表示自旋盒的最小值。
设置该属性时，如有必要会调整`maximum`以确保范围有效。
默认最低值是0。

**如何使用：** 调用 `setMinimum(...)` 修改 `minimum`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setPrefix(const QString &prefix)`

**作用与语义：**

该属性表示自旋盒的前缀。
前缀会加在显示值的开头。典型用途是显示计量单位或货币符号。例如：
要关闭前缀显示，将该属性设置为空字符串。默认为无前缀。当 `value()` == `minimum()` 且 `specialValueText()` 被设置时，前缀不会显示。
如果未设置前缀，前缀()返回空字符串。

**如何使用：** 调用 `setPrefix(...)` 修改 `prefix`；传入的新值会成为后续查询和相关界面行为所使用的值。

**官方示例：**

```cpp
 sb->setPrefix("$");
```

### `void setSingleStep(int val)`

**作用与语义：**

该属性表示步长值。
当用户使用箭头更改旋转盒的值时，值会根据 singleStep 的数量递增或减少。默认值是 1。将 singleStep 值设为小于 0 则无效。

**如何使用：** 调用 `setSingleStep(...)` 修改 `singleStep`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setSuffix(const QString &suffix)`

**作用与语义：**

该属性表示旋量盒的后缀。
后缀附加在显示值的末尾。典型用途是显示计量单位或货币符号。例如：
要关闭后缀显示，将该属性设置为空字符串。默认情况下无后缀。如果`specialValueText()`设置，后缀不会在`minimum()`中显示。
如果没有设置后缀，后缀()返回一个空字符串。

**如何使用：** 调用 `setSuffix(...)` 修改 `suffix`；传入的新值会成为后续查询和相关界面行为所使用的值。

**官方示例：**

```cpp
 sb->setSuffix(" km");
```

### `int singleStep() const`

**作用与语义：**

该属性表示步长值。
当用户使用箭头更改旋转盒的值时，值会根据 singleStep 的数量递增或减少。默认值是 1。将 singleStep 值设为小于 0 则无效。

**如何使用：** 调用 `singleStep()` 读取当前值；它不会修改应用状态。

### `QAbstractSpinBox::StepType stepType() const`

**作用与语义：**

该属性表示 阶梯类型。
步进类型可以是单步或自适应十进制步。

**如何使用：** 调用 `stepType()` 读取当前值；它不会修改应用状态。

### `QString suffix() const`

**作用与语义：**

该属性表示旋量盒的后缀。
后缀附加在显示值的末尾。典型用途是显示计量单位或货币符号。例如：
要关闭后缀显示，将该属性设置为空字符串。默认情况下无后缀。如果`specialValueText()`设置，后缀不会在`minimum()`中显示。
如果没有设置后缀，后缀()返回一个空字符串。

**如何使用：** 调用 `suffix()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 sb->setSuffix(" km");
```

### `int value() const`

**作用与语义：**

该属性表示自旋盒的值。
如果新值与旧值不同，setValue() 会发出 `valueChanged()`。value 属性带有第二个通知信号，包含旋转盒的前缀和后缀。

**如何使用：** 调用 `value()` 读取当前值；它不会修改应用状态。

### `void setValue(int val)`

**作用与语义：**

该属性表示自旋盒的值。
如果新值与旧值不同，setValue() 会发出 `valueChanged()`。value 属性带有第二个通知信号，包含旋转盒的前缀和后缀。

**如何使用：** 调用 `setValue(...)` 修改 `value`；传入的新值会成为后续查询和相关界面行为所使用的值。

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

`QSpinBox` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
