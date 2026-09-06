# QProgressDialog

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QProgressDialog` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QProgressDialog` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QProgressDialog>`
- 继承自：QDialog
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

- `autoClose : bool`
- `autoReset : bool`
- `labelText : QString`
- `maximum : int`
- `minimum : int`
- `minimumDuration : int`
- `value : int`
- `wasCanceled : bool`

### 公有函数

- `QProgressDialog(QWidget *parent = nullptr, Qt::WindowFlags f = Qt::WindowFlags())`
- `QProgressDialog(const QString &labelText, const QString &cancelButtonText, int minimum, int maximum, QWidget *parent = nullptr, Qt::WindowFlags f = Qt::WindowFlags())`
- `virtual ~QProgressDialog()`
- `bool autoClose() const`
- `bool autoReset() const`
- `QString labelText() const`
- `int maximum() const`
- `int minimum() const`
- `int minimumDuration() const`
- `void open(QObject *receiver, const char *member)`
- `void setAutoClose(bool close)`
- `void setAutoReset(bool reset)`
- `void setBar(QProgressBar *bar)`
- `void setCancelButton(QPushButton *cancelButton)`
- `void setLabel(QLabel *label)`
- `int value() const`
- `bool wasCanceled() const`

### 重实现的公有函数

- `virtual QSize sizeHint() const override`

### 公有槽函数

- `void cancel()`
- `void reset()`
- `void setCancelButtonText(const QString &cancelButtonText)`
- `void setLabelText(const QString &text)`
- `void setMaximum(int maximum)`
- `void setMinimum(int minimum)`
- `void setMinimumDuration(int ms)`
- `void setRange(int minimum, int maximum)`
- `void setValue(int progress)`

### 信号

- `void canceled()`

### 重实现的保护函数

- `virtual void changeEvent(QEvent *ev) override`
- `virtual void closeEvent(QCloseEvent *e) override`
- `virtual void resizeEvent(QResizeEvent *event) override`
- `virtual void showEvent(QShowEvent *e) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `autoClose : bool`

**作用与语义：**

该属性在对话被隐藏时成立`reset()`。
默认是真的。

**如何使用：** 调用 `autoClose()` 读取当前值；它不会修改应用状态。

### `autoReset : bool`

**作用与语义：**

该属性是否在进度对话框在 `value()` 等于 `maximum()` 时立即调用 `reset()`。
默认是真的。

**如何使用：** 调用 `autoReset()` 读取当前值；它不会修改应用状态。

### `labelText : QString`

**作用与语义：**

该属性包含标签的文本。
默认文本是空字符串。

**如何使用：** 调用 `labelText()` 读取当前值；它不会修改应用状态。

### `maximum : int`

**作用与语义：**

该属性由进度条代表的最高值。
默认是100。

**如何使用：** 调用 `maximum()` 读取当前值；它不会修改应用状态。

### `minimum : int`

**作用与语义：**

该属性是进度条表示的最低值。
默认值是0。

**如何使用：** 调用 `minimum()` 读取当前值；它不会修改应用状态。

### `minimumDuration : int`

**作用与语义：**

该属性表示对话出现前必须经过的时间。
如果任务的预期持续时间低于最小持续时间，对话框将完全不会出现。这会防止快速结束的任务弹出对话框。对于预期超过最小持续时间的任务，对话框会在最小持续时间后或任何进度设置后弹出。
如果设置为0，任何进度设置后都会显示对话。默认是4000毫秒。

**如何使用：** 调用 `minimumDuration()` 读取当前值；它不会修改应用状态。

### `value : int`

**作用与语义：**

该物业记录了当前取得的进展。
为了让进度对话框正常工作，你应该先把这个属性设置为`QProgressDialog::minimum()`，最后再设置为`QProgressDialog::maximum()`;你可以在中间任意次数调用 setValue()。
警告：如果进度对话框是模态的（见`QProgressDialog::QProgressDialog()`），setValue() 会调用 `QCoreApplication::processEvents()`，因此请注意这不会导致代码中出现不良的重复输入。例如，不要在 `paintEvent()` 中使用 `QProgressDialog`！

**如何使用：** 调用 `value()` 读取当前值；它不会修改应用状态。

### `[read-only] wasCanceled : bool`

**作用与语义：**

该属性 表示对话是否被取消。

**如何使用：** 调用 `wasCanceled()` 读取当前值；它不会修改应用状态。

### `[explicit] QProgressDialog::QProgressDialog(QWidget *parent = nullptr, Qt::WindowFlags f = Qt::WindowFlags())`

**作用与语义：**

构建进度对话框。
默认设置：
- 标签文本为空。
- 取消按钮的文字（翻译为）“取消”。
- 最小值为0;
- 最大100
`parent`参数是 dialog 的父控件。控件标志 `f` 传递给 `QDialog::QDialog()` 构造函数。

### `QProgressDialog::QProgressDialog(const QString &labelText, const QString &cancelButtonText, int minimum, int maximum, QWidget *parent = nullptr, Qt::WindowFlags f = Qt::WindowFlags())`

**作用与语义：**

构建进度对话框。
`labelText`是用来提醒用户进展情况的文本。
`cancelButtonText`是取消按钮上要显示的文本。如果通过QString()，则不显示取消按钮。
`minimum`和`maximum`是该进度对话框显示进度的操作步骤数。例如，如果操作是检查50个文件，最小值为0，最大值为50。在检查第一个文件之前，调用`setValue`（0）。当每个文件处理完毕时，调用`setValue`（1）、`setValue`（2）等，检查最后一个文件后调用`setValue`（50）。
`parent`参数是对话的父控件。父节点、`parent`节点和控件标志`f`传递给`QDialog::QDialog()`构造函数。

### `[virtual noexcept] QProgressDialog::~QProgressDialog()`

**作用与语义：**

会破坏进度对话框。

### `[slot] void QProgressDialog::cancel()`

**作用与语义：**

重置进度对话框。`wasCanceled()`在进度对话框重置前变为真。进度对话框会被隐藏。

### `[signal] void QProgressDialog::canceled()`

**作用与语义：**

当按下取消按钮时，该信号会发出。默认情况下，它连接到`cancel()`槽函数。

### `[override virtual protected] void QProgressDialog::changeEvent(QEvent *ev)`

**作用与语义：**

重装：`QWidget::changeEvent`（QEvent *事件）。
该事件处理程序可以重新实现以处理状态变化。
该事件中被更改的状态可以通过提供的`event`检索。
变更事件包括：`QEvent::ToolBarChange`、`QEvent::ActivationChange`、`QEvent::EnabledChange`、`QEvent::FontChange`、`QEvent::StyleChange`、`QEvent::PaletteChange`、`QEvent::WindowTitleChange`、`QEvent::IconTextChange`、`QEvent::ModifiedChange`、`QEvent::MouseTrackingChange`、`QEvent::ParentChange`、`QEvent::WindowStateChange`、`QEvent::LanguageChange`、`QEvent::LocaleChange`、`QEvent::LayoutDirectionChange`、`QEvent::ReadOnlyChange`。

### `[override virtual protected] void QProgressDialog::closeEvent(QCloseEvent *e)`

**作用与语义：**

重实现自：`QDialog::closeEvent`（QCloseEvent *e）。

### `[protected slot] void QProgressDialog::forceShow()`

**作用与语义：**

如果算法启动后`minimumDuration`毫秒后对话仍隐藏，会显示对话。

### `void QProgressDialog::open(QObject *receiver, const char *member)`

**作用与语义：**

打开对话，并将其`canceled()`信号连接到`receiver`和`member`指定的槽函数。
当对话关闭时，信号会从槽函数中断开。

### `[slot] void QProgressDialog::reset()`

**作用与语义：**

重置进度对话框。如果`autoClose()`为真，进度对话框会被隐藏。

### `[override virtual protected] void QProgressDialog::resizeEvent(QResizeEvent *event)`

**作用与语义：**

重实现自：`QDialog::resizeEvent`（QResizeEvent *）。

### `void QProgressDialog::setBar(QProgressBar *bar)`

**作用与语义：**

将进度条小部件设置为`bar`。进度对话框大小调整以适应。进度对话框拥有进度`bar`所有权，必要时会删除，因此不要使用堆栈中分配的进度条。

### `void QProgressDialog::setCancelButton(QPushButton *cancelButton)`

**作用与语义：**

将取消按钮设置为按下按钮，`cancelButton`。进度对话框会拥有该按钮的所有权，必要时会删除，因此不要传递栈中对象的地址，即使用 new() 创建按钮。如果`nullptr`被传递，则不会显示取消按钮。

### `[slot] void QProgressDialog::setCancelButtonText(const QString &cancelButtonText)`

**作用与语义：**

将取消按钮的文本设置为`cancelButtonText`。如果文本设置为QString()，则取消按钮会被隐藏并删除。

### `void QProgressDialog::setLabel(QLabel *label)`

**作用与语义：**

将标签设置为`label`。进度对话框大小调整以适应。标签会被进度对话框拥有，必要时会被删除，因此不要传递堆栈中对象的地址。

### `[slot] void QProgressDialog::setRange(int minimum, int maximum)`

**作用与语义：**

将进度对话框的最小值和最大值分别设置为`minimum`和`maximum`。
如果`maximum`小于`minimum`，`minimum`成为唯一的法律价值。
如果当前值超出新范围，进度对话框会随`reset()`重置。

### `[override virtual protected] void QProgressDialog::showEvent(QShowEvent *e)`

**作用与语义：**

重实现自：`QDialog::showEvent`（QShowEvent *event）。

### `[override virtual] QSize QProgressDialog::sizeHint() const`

**作用与语义：**

重实现自：`QDialog::sizeHint()` const.
返回一个大小，与进度对话框内容相符。进度对话框会根据需要自动调整大小，所以你不需要自己调用它。
重新实现了属性的访问函数：`QWidget::sizeHint`。

### `bool autoClose() const`

**作用与语义：**

该属性在对话被隐藏时成立`reset()`。
默认是真的。

**如何使用：** 调用 `autoClose()` 读取当前值；它不会修改应用状态。

### `bool autoReset() const`

**作用与语义：**

该属性是否在进度对话框在 `value()` 等于 `maximum()` 时立即调用 `reset()`。
默认是真的。

**如何使用：** 调用 `autoReset()` 读取当前值；它不会修改应用状态。

### `QString labelText() const`

**作用与语义：**

该属性包含标签的文本。
默认文本是空字符串。

**如何使用：** 调用 `labelText()` 读取当前值；它不会修改应用状态。

### `int maximum() const`

**作用与语义：**

该属性由进度条代表的最高值。
默认是100。

**如何使用：** 调用 `maximum()` 读取当前值；它不会修改应用状态。

### `int minimum() const`

**作用与语义：**

该属性是进度条表示的最低值。
默认值是0。

**如何使用：** 调用 `minimum()` 读取当前值；它不会修改应用状态。

### `int minimumDuration() const`

**作用与语义：**

该属性表示对话出现前必须经过的时间。
如果任务的预期持续时间低于最小持续时间，对话框将完全不会出现。这会防止快速结束的任务弹出对话框。对于预期超过最小持续时间的任务，对话框会在最小持续时间后或任何进度设置后弹出。
如果设置为0，任何进度设置后都会显示对话。默认是4000毫秒。

**如何使用：** 调用 `minimumDuration()` 读取当前值；它不会修改应用状态。

### `void setAutoClose(bool close)`

**作用与语义：**

该属性在对话被隐藏时成立`reset()`。
默认是真的。

**如何使用：** 调用 `setAutoClose(...)` 修改 `autoClose`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setAutoReset(bool reset)`

**作用与语义：**

该属性是否在进度对话框在 `value()` 等于 `maximum()` 时立即调用 `reset()`。
默认是真的。

**如何使用：** 调用 `setAutoReset(...)` 修改 `autoReset`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `int value() const`

**作用与语义：**

该物业记录了当前取得的进展。
为了让进度对话框正常工作，你应该先把这个属性设置为`QProgressDialog::minimum()`，最后再设置为`QProgressDialog::maximum()`;你可以在中间任意次数调用 setValue()。
警告：如果进度对话框是模态的（见`QProgressDialog::QProgressDialog()`），setValue() 会调用 `QCoreApplication::processEvents()`，因此请注意这不会导致代码中出现不良的重复输入。例如，不要在 `paintEvent()` 中使用 `QProgressDialog`！

**如何使用：** 调用 `value()` 读取当前值；它不会修改应用状态。

### `bool wasCanceled() const`

**作用与语义：**

该属性 表示对话是否被取消。

**如何使用：** 调用 `wasCanceled()` 读取当前值；它不会修改应用状态。

### `void setLabelText(const QString &text)`

**作用与语义：**

该属性包含标签的文本。
默认文本是空字符串。

**如何使用：** 调用 `setLabelText(...)` 修改 `labelText`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMaximum(int maximum)`

**作用与语义：**

该属性由进度条代表的最高值。
默认是100。

**如何使用：** 调用 `setMaximum(...)` 修改 `maximum`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMinimum(int minimum)`

**作用与语义：**

该属性是进度条表示的最低值。
默认值是0。

**如何使用：** 调用 `setMinimum(...)` 修改 `minimum`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMinimumDuration(int ms)`

**作用与语义：**

该属性表示对话出现前必须经过的时间。
如果任务的预期持续时间低于最小持续时间，对话框将完全不会出现。这会防止快速结束的任务弹出对话框。对于预期超过最小持续时间的任务，对话框会在最小持续时间后或任何进度设置后弹出。
如果设置为0，任何进度设置后都会显示对话。默认是4000毫秒。

**如何使用：** 调用 `setMinimumDuration(...)` 修改 `minimumDuration`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setValue(int progress)`

**作用与语义：**

该物业记录了当前取得的进展。
为了让进度对话框正常工作，你应该先把这个属性设置为`QProgressDialog::minimum()`，最后再设置为`QProgressDialog::maximum()`;你可以在中间任意次数调用 setValue()。
警告：如果进度对话框是模态的（见`QProgressDialog::QProgressDialog()`），setValue() 会调用 `QCoreApplication::processEvents()`，因此请注意这不会导致代码中出现不良的重复输入。例如，不要在 `paintEvent()` 中使用 `QProgressDialog`！

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

`QProgressDialog` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
