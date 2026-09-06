# QKeySequenceEdit

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QKeySequenceEdit` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QKeySequenceEdit` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QKeySequenceEdit>`
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

### 属性

- `(since 6.4) clearButtonEnabled : bool`
- `(since 6.5) finishingKeyCombinations : QList<QKeyCombination>`
- `keySequence : QKeySequence`
- `(since 6.5) maximumSequenceLength : qsizetype`

### 公有函数

- `QKeySequenceEdit(QWidget *parent = nullptr)`
- `QKeySequenceEdit(const QKeySequence &keySequence, QWidget *parent = nullptr)`
- `virtual ~QKeySequenceEdit()`
- `QList<QKeyCombination> finishingKeyCombinations() const`
- `bool isClearButtonEnabled() const`
- `QKeySequence keySequence() const`
- `qsizetype maximumSequenceLength() const`
- `void setClearButtonEnabled(bool enable)`
- `void setFinishingKeyCombinations(const QList<QKeyCombination> &finishingKeyCombinations)`

### 公有槽函数

- `void clear()`
- `void setKeySequence(const QKeySequence &keySequence)`
- `void setMaximumSequenceLength(qsizetype count)`

### 信号

- `void editingFinished()`
- `void keySequenceChanged(const QKeySequence &keySequence)`

### 重实现的保护函数

- `virtual bool event(QEvent *e) override`
- `virtual void focusOutEvent(QFocusEvent *e) override`
- `virtual void keyPressEvent(QKeyEvent *e) override`
- `virtual void keyReleaseEvent(QKeyEvent *e) override`
- `virtual void timerEvent(QTimerEvent *e) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[since 6.4] clearButtonEnabled : bool`

**作用与语义：**

该属性决定键序列编辑是否在未空时显示清除按钮。
如果启用，键序列编辑包含文本时会显示一个尾随的清除按钮，否则行编辑不会显示清除按钮（默认设置）。

**如何使用：** 调用 `clearButtonEnabled()` 读取当前值；它不会修改应用状态。

### `[since 6.5] finishingKeyCombinations : QList<QKeyCombination>`

**作用与语义：**

该属性包含完成编辑密钥序列的密钥组合列表。
列表中任意组合都可以完成按键序列的编辑。所有其他按键组合都可以作为按键序列的一部分被记录。默认情况下，`Qt::Key_Tab`和`Qt::Key_Backtab`会完成按键序列的录制。

**如何使用：** 调用 `finishingKeyCombinations()` 读取当前值；它不会修改应用状态。

### `keySequence : QKeySequence`

**作用与语义：**

该属性包含当前选择的密钥序列。
快捷方式可以由用户或设置功能更改。
注意：如果`QKeySequence`长于`maximumSequenceLength`属性，则键序列被截断。

**如何使用：** 调用 `keySequence()` 读取当前值；它不会修改应用状态。

### `[since 6.5] maximumSequenceLength : qsizetype`

**作用与语义：**

该属性表示序列的最大长度。
用户可输入的最大密钥序列数。值应在1到4之间，默认为4。

**如何使用：** 调用 `maximumSequenceLength()` 读取当前值；它不会修改应用状态。

### `[explicit] QKeySequenceEdit::QKeySequenceEdit(QWidget *parent = nullptr)`

**作用与语义：**

构建一个带有给定`parent`的QKeySequenceEdit小部件。

### `[explicit] QKeySequenceEdit::QKeySequenceEdit(const QKeySequence &keySequence, QWidget *parent = nullptr)`

**作用与语义：**

构建一个带有给定`keySequence`和`parent`的QKeySequenceEdit小部件。

### `[virtual noexcept] QKeySequenceEdit::~QKeySequenceEdit()`

**作用与语义：**

摧毁`QKeySequenceEdit`物体。

### `[slot] void QKeySequenceEdit::clear()`

**作用与语义：**

清除当前键序列。

### `[signal] void QKeySequenceEdit::editingFinished()`

**作用与语义：**

当用户完成快捷输入时，该信号会发出。
注意：在释放最后一个密钥并发出该信号之前，有一个一秒的延迟。

### `[override virtual protected] bool QKeySequenceEdit::event(QEvent *e)`

**作用与语义：**

重实现自：`QWidget::event`（QEvent *事件）。

### `[override virtual protected] void QKeySequenceEdit::focusOutEvent(QFocusEvent *e)`

**作用与语义：**

重现：`QWidget::focusOutEvent`（QFocusEvent *event）。
该事件处理程序可以在子类中重新实现，以接收控件的键盘焦点事件（焦点丢失）。事件通过`event`参数传递。
小部件通常必须`setFocusPolicy()`到非`Qt::NoFocus`的对象才能接收焦点事件。（注意，应用程序员可以调用任何小部件`setFocus()`，即使是那些通常不接受焦点的小部件。）。
默认实现会更新小部件（除非是没有指定`focusPolicy()`的窗口）。

### `[override virtual protected] void QKeySequenceEdit::keyPressEvent(QKeyEvent *e)`

**作用与语义：**

重实现自：`QWidget::keyPressEvent`（QKeyEvent *event）。
该事件处理程序用于事件`event`，可以在子类中重新实现，以接收该控件的按键事件。
一个小部件必须调用`setFocusPolicy()`先接受焦点，并且必须有焦点才能接收按键事件。
如果你重新实现这个处理器，如果你不对密钥进行操作，务必调用基类实现。
默认实现会关闭弹出小部件，如果用户按下`QKeySequence::Cancel`的按键序列（通常是 Escape 键）。否则事件会被忽略，以便小部件的父节点能够解释。
注意`QKeyEvent`以 isAccepted() == true 开头，所以你不需要调用 `QKeyEvent::accept()`——只要你对该键执行时不要调用基类实现即可。

### `[override virtual protected] void QKeySequenceEdit::keyReleaseEvent(QKeyEvent *e)`

**作用与语义：**

重实现自：`QWidget::keyReleaseEvent`（QKeyEvent *event）。
该事件处理程序用于事件`event`，可以在子类中重新实现，以接收该小部件的密钥释放事件。
小部件必须先接受焦点并拥有焦点，才能接收密钥释放事件。
如果你重新实现这个处理器，如果你不对密钥进行操作，务必调用基类实现。
默认实现忽略事件，以便小部件的父节点能够解释事件。
注意`QKeyEvent`以 isAccepted() == true开头，所以你不需要调用`QKeyEvent::accept()`——只要你对密钥操作时不要调用基类实现即可。

### `[override virtual protected] void QKeySequenceEdit::timerEvent(QTimerEvent *e)`

**作用与语义：**

重实现自：`QObject::timerEvent`（QTimerEvent *event）。

### `QList<QKeyCombination> finishingKeyCombinations() const`

**作用与语义：**

该属性包含完成编辑密钥序列的密钥组合列表。
列表中任意组合都可以完成按键序列的编辑。所有其他按键组合都可以作为按键序列的一部分被记录。默认情况下，`Qt::Key_Tab`和`Qt::Key_Backtab`会完成按键序列的录制。

**如何使用：** 调用 `finishingKeyCombinations()` 读取当前值；它不会修改应用状态。

### `bool isClearButtonEnabled() const`

**作用与语义：**

该属性决定键序列编辑是否在未空时显示清除按钮。
如果启用，键序列编辑包含文本时会显示一个尾随的清除按钮，否则行编辑不会显示清除按钮（默认设置）。

**如何使用：** 调用 `isClearButtonEnabled()` 读取当前值；它不会修改应用状态。

### `QKeySequence keySequence() const`

**作用与语义：**

该属性包含当前选择的密钥序列。
快捷方式可以由用户或设置功能更改。
注意：如果`QKeySequence`长于`maximumSequenceLength`属性，则键序列被截断。

**如何使用：** 调用 `keySequence()` 读取当前值；它不会修改应用状态。

### `qsizetype maximumSequenceLength() const`

**作用与语义：**

该属性表示序列的最大长度。
用户可输入的最大密钥序列数。值应在1到4之间，默认为4。

**如何使用：** 调用 `maximumSequenceLength()` 读取当前值；它不会修改应用状态。

### `void setClearButtonEnabled(bool enable)`

**作用与语义：**

该属性决定键序列编辑是否在未空时显示清除按钮。
如果启用，键序列编辑包含文本时会显示一个尾随的清除按钮，否则行编辑不会显示清除按钮（默认设置）。

**如何使用：** 调用 `setClearButtonEnabled(...)` 修改 `clearButtonEnabled`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setFinishingKeyCombinations(const QList<QKeyCombination> &finishingKeyCombinations)`

**作用与语义：**

该属性包含完成编辑密钥序列的密钥组合列表。
列表中任意组合都可以完成按键序列的编辑。所有其他按键组合都可以作为按键序列的一部分被记录。默认情况下，`Qt::Key_Tab`和`Qt::Key_Backtab`会完成按键序列的录制。

**如何使用：** 调用 `setFinishingKeyCombinations(...)` 修改 `finishingKeyCombinations`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setKeySequence(const QKeySequence &keySequence)`

**作用与语义：**

该属性包含当前选择的密钥序列。
快捷方式可以由用户或设置功能更改。
注意：如果`QKeySequence`长于`maximumSequenceLength`属性，则键序列被截断。

**如何使用：** 调用 `setKeySequence(...)` 修改 `keySequence`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMaximumSequenceLength(qsizetype count)`

**作用与语义：**

该属性表示序列的最大长度。
用户可输入的最大密钥序列数。值应在1到4之间，默认为4。

**如何使用：** 调用 `setMaximumSequenceLength(...)` 修改 `maximumSequenceLength`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void keySequenceChanged(const QKeySequence &keySequence)`

**作用与语义：**

该属性包含当前选择的密钥序列。
快捷方式可以由用户或设置功能更改。
注意：如果`QKeySequence`长于`maximumSequenceLength`属性，则键序列被截断。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `keySequence` 的变化，不要把它当作普通函数主动调用。

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

`QKeySequenceEdit` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
