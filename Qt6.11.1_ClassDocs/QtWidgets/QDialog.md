# QDialog

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** 模态或非模态对话框基类，负责临时交互、接受/拒绝结果和对话框生命周期。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QDialog`：模态或非模态对话框基类，负责临时交互、接受/拒绝结果和对话框生命周期。

**内部模型：** Widgets 通过父子控件树、布局系统、事件分发和重绘请求组成界面。控件的可见区域、sizeHint、sizePolicy、字体和平台 style 共同影响最终几何；用户输入先进入 Qt 事件系统，再由控件的事件函数、信号或快捷键处理。

**适用场景：** 创建 QApplication 后创建控件，设置 parent 或把控件加入布局，连接用户操作信号，再显示顶层窗口。复合界面用布局嵌套；控件尺寸异常时同时检查 sizePolicy、minimum/maximum size、layout stretch、margins 和 spacing。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要用固定坐标拼接响应式界面；不要给已经加入布局的控件反复 `setGeometry()`；不要在 `paintEvent()` 中修改业务状态；不要忘记窗口关闭、对象销毁和应用退出是三个不同事件。

## 2. 依赖与对象关系

- 头文件：`#include <QDialog>`
- 继承自：QWidget
- 直接派生类：QColorDialog、QErrorMessage、QFileDialog、QFontDialog、QInputDialog、QMessageBox、QProgressDialog,、QWizard

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

Widgets 通过父子控件树、布局系统、事件分发和重绘请求组成界面。控件的可见区域、sizeHint、sizePolicy、字体和平台 style 共同影响最终几何；用户输入先进入 Qt 事件系统，再由控件的事件函数、信号或快捷键处理。

### 状态、生命周期和线程

**生命周期：** 控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

**状态与结果：** 控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

**线程与事件循环：** 所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

## 3. 直接使用

创建 QApplication 后创建控件，设置 parent 或把控件加入布局，连接用户操作信号，再显示顶层窗口。复合界面用布局嵌套；控件尺寸异常时同时检查 sizePolicy、minimum/maximum size、layout stretch、margins 和 spacing。 使用时通常按这个过程组织：构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum DialogCode { Accepted, Rejected }`

### 属性

- `modal : bool`
- `sizeGripEnabled : bool`

### 公有函数

- `QDialog(QWidget *parent = nullptr, Qt::WindowFlags f = Qt::WindowFlags())`
- `virtual ~QDialog()`
- `bool isSizeGripEnabled() const`
- `int result() const`
- `void setModal(bool modal)`
- `void setResult(int i)`
- `void setSizeGripEnabled(bool)`

### 重实现的公有函数

- `virtual QSize minimumSizeHint() const override`
- `virtual void setVisible(bool visible) override`
- `virtual QSize sizeHint() const override`

### 公有槽函数

- `virtual void accept()`
- `virtual void done(int r)`
- `virtual int exec()`
- `virtual void open()`
- `virtual void reject()`

### 信号

- `void accepted()`
- `void finished(int result)`
- `void rejected()`

### 重实现的保护函数

- `virtual void closeEvent(QCloseEvent *e) override`
- `virtual void contextMenuEvent(QContextMenuEvent *e) override`
- `virtual bool eventFilter(QObject *o, QEvent *e) override`
- `virtual void keyPressEvent(QKeyEvent *e) override`
- `virtual void resizeEvent(QResizeEvent *) override`
- `virtual void showEvent(QShowEvent *event) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QDialog::DialogCode`

**作用与语义：**

模态对话框返回的值。
- `QDialog::Accepted`：`1`
- `QDialog::Rejected`：`0`

### `modal : bool`

**作用与语义：**

该属性决定了 `show()` 应该以模态还是无模式形式弹出对话。
默认情况下，该属性为`false`，`show()`会弹出无模式的对话框。将该属性设置为true等同于将`QWidget::windowModality`设置为`Qt::ApplicationModal`。
`exec()` 忽略了该属性的值，总是以模态形式弹出对话。

**如何使用：** 调用 `modal()` 读取当前值；它不会修改应用状态。

### `sizeGripEnabled : bool`

**作用与语义：**

该属性在尺寸握法是否启用时依然成立。
启用该属性时，对话框右下角会放置一个`QSizeGrip`。默认情况下，握把尺寸是禁用的。

**如何使用：** 调用 `sizeGripEnabled()` 读取当前值；它不会修改应用状态。

### `[explicit] QDialog::QDialog(QWidget *parent = nullptr, Qt::WindowFlags f = Qt::WindowFlags())`

**作用与语义：**

构建与父`parent`的对话。
对话框始终是顶层控件，但如果有父控件，其默认位置会置于父控件的顶部。它还会共享父控件的任务栏条目。
小部件`f`的标志会传递给`QWidget`构造器。例如，如果你不想在对话框标题栏中放置“这是怎么回事”按钮，可以传递`Qt::WindowTitleHint` |`Qt::WindowSystemMenuHint` `f`。

### `[virtual noexcept] QDialog::~QDialog()`

**作用与语义：**

摧毁`QDialog`，删除所有子嗣。

### `[virtual slot] void QDialog::accept()`

**作用与语义：**

隐藏模态对话框，并将结果代码设置为`Accepted`。

### `[signal] void QDialog::accepted()`

**作用与语义：**

当对话被用户接受，或通过调用带有`QDialog::Accepted`参数的`accept()`或`done()`时，该信号就会发出。
注意，当用`hide()`或`setVisible`（false）隐藏对话时，该信号不会发出。这包括在对话可见时删除对话。

### `[override virtual protected] void QDialog::closeEvent(QCloseEvent *e)`

**作用与语义：**

重实现自：`QWidget::closeEvent`（QCloseEvent *event）。
当 Qt 收到来自窗口系统顶层控件的窗口关闭请求时，该事件处理程序会以该`event`调用。
默认情况下，事件被接受，小部件关闭。你可以重新实现这个函数，改变小部件对窗口关闭请求的响应方式。例如，你可以通过调用所有事件的 `ignore()` 来阻止窗口关闭。
主窗口应用程序通常会重新实现该函数，以检查用户的工作是否已被保存，并在关闭前请求许可。

### `[override virtual protected] void QDialog::contextMenuEvent(QContextMenuEvent *e)`

**作用与语义：**

重实现自：`QWidget::contextMenuEvent`（QContextMenuEvent *event）。
该事件处理程序用于事件`event`，可以在子类中重新实现，以接收控件上下文菜单事件。
当控件的 `contextMenuPolicy` `Qt::DefaultContextMenu`时调用处理器。
默认实现忽略上下文事件。详情请参见`QContextMenuEvent`文档。

### `[virtual slot] void QDialog::done(int r)`

**作用与语义：**

关闭对话框并将结果码设置为`r`。`finished()`信号会发出`r`;如果`r`是`QDialog::Accepted`或`QDialog::Rejected`，则分别会发出`accepted()`或`rejected()`信号。
如果该对话显示为`exec()`，done() 也会使本地事件循环结束，`exec()`返回`r`。
与`QWidget::close()`一样，如果设置了`Qt::WA_DeleteOnClose`标志，done() 会删除对话。如果对话框是应用程序的主控件，应用程序会终止。如果对话框是最后关闭的窗口，则发出`QGuiApplication::lastWindowClosed()`信号。

### `[override virtual protected] bool QDialog::eventFilter(QObject *o, QEvent *e)`

**作用与语义：**

重装：`QObject::eventFilter`（QObject *已观看，QEvent *事件）。

### `[virtual slot] int QDialog::exec()`

**作用与语义：**

以模态对话框显示对话，阻塞直到用户关闭。函数返回`DialogCode`结果。
如果对话框是应用模态的，用户在关闭对话框之前不能与同一应用中的任何其他窗互。如果对话框是窗口模态，则在对话框打开期间，只有与父窗口的交互被屏蔽。默认情况下，该对话框是应用模态的。
注意：避免使用此函数;改用 `open()`。与 exec() 不同，`open()` 是异步的，不会旋转额外的事件循环。这防止了一系列危险的错误发生（例如，在对话打开时通过 exec()删除对话的父节点）。使用 `open()` 时，你可以连接到`QDialog`的`finished()`信号，以获得对话关闭时的通知。

### `[signal] void QDialog::finished(int result)`

**作用与语义：**

当对话框的`result`代码被设置时，该信号由用户或调用`done()`、`accept()`或`reject()`发出。
注意，当用`hide()`或`setVisible`（false）隐藏对话时，这个信号不会发出。这包括在对话可见时删除。

### `[override virtual protected] void QDialog::keyPressEvent(QKeyEvent *e)`

**作用与语义：**

重实现自：`QWidget::keyPressEvent`（QKeyEvent *event）。
该事件处理程序用于事件`event`，可以在子类中重新实现，以接收该控件的按键事件。
一个小部件必须调用`setFocusPolicy()`先接受焦点，并且必须有焦点才能接收按键事件。
如果你重新实现这个处理器，如果你不对密钥进行操作，务必调用基类实现。
默认实现会关闭弹出小部件，如果用户按下`QKeySequence::Cancel`的按键序列（通常是 Escape 键）。否则事件会被忽略，以便小部件的父节点能够解释。
注意`QKeyEvent`以 isAccepted() == true 开头，所以你不需要调用 `QKeyEvent::accept()`——只要你对该键执行时不要调用基类实现即可。

### `[override virtual] QSize QDialog::minimumSizeHint() const`

**作用与语义：**

重新实现属性的访问函数：`QWidget::minimumSizeHint`。

### `[virtual slot] void QDialog::open()`

**作用与语义：**

以窗口模态对话框显示对话，立即返回。

### `[virtual slot] void QDialog::reject()`

**作用与语义：**

隐藏模态对话框，并将结果代码设置为`Rejected`。

### `[signal] void QDialog::rejected()`

**作用与语义：**

当用户或通过调用`QDialog::Rejected`参数的`reject()`或`done()`拒绝对话时，该信号会发出。
注意，当用`hide()`或`setVisible`（false）隐藏对话时，该信号不会发出。这包括在对话可见时删除对话。

### `[override virtual protected] void QDialog::resizeEvent(QResizeEvent *)`

**作用与语义：**

重实现自：`QWidget::resizeEvent`（QResizeEvent *event）。
该事件处理程序可以在子类中重新实现，以接收通过 `event` 参数传递的控件调整大小事件。当调用 resizeEvent() 时，控件已经拥有新的几何体。旧的大小可以通过 `QResizeEvent::oldSize()` 访问。
控件会被擦除，并在处理调整尺寸事件后立即接收绘图事件。不需要（也不应该）在这个处理程序中进行绘图。

### `int QDialog::result() const`

**作用与语义：**

通常返回模态对话框的结果代码，`Accepted`或`Rejected`。
注意：当在`QMessageBox`实例中调用时，返回的值是`QMessageBox::StandardButton`枚举的一个值。
如果对话是用`Qt::WA_DeleteOnClose`属性构建的，不要调用该函数。

### `void QDialog::setResult(int i)`

**作用与语义：**

将模态对话框的结果代码设置为`i`。
注意：我们建议您使用`QDialog::DialogCode`定义的某个数值。

### `[override virtual] void QDialog::setVisible(bool visible)`

**作用与语义：**

重新实现了属性的访问函数：`QWidget::visible`。

### `[override virtual protected] void QDialog::showEvent(QShowEvent *event)`

**作用与语义：**

重实现自：`QWidget::showEvent`（QShowEvent *event）。
该事件处理程序可以在子类中重新实现，以接收传递给 `event` 参数的控件显示事件。
非自发的展示事件会在展示前立即发送到小部件。窗口的自发展示事件则在展示之后交付。
注意：当窗口系统改变其映射状态时，小部件会接收自发显示和隐藏事件，例如用户最小化窗口时自发隐藏事件，窗口恢复时自发显示事件。收到自发隐藏事件后，小部件仍被视为`isVisible()`可见。

### `[override virtual] QSize QDialog::sizeHint() const`

**作用与语义：**

重新实现了属性的访问函数：`QWidget::sizeHint`。

### `bool isSizeGripEnabled() const`

**作用与语义：**

该属性在尺寸握法是否启用时依然成立。
启用该属性时，对话框右下角会放置一个`QSizeGrip`。默认情况下，握把尺寸是禁用的。

**如何使用：** 调用 `isSizeGripEnabled()` 读取当前值；它不会修改应用状态。

### `void setModal(bool modal)`

**作用与语义：**

该属性决定了 `show()` 应该以模态还是无模式形式弹出对话。
默认情况下，该属性为`false`，`show()`会弹出无模式的对话框。将该属性设置为true等同于将`QWidget::windowModality`设置为`Qt::ApplicationModal`。
`exec()` 忽略了该属性的值，总是以模态形式弹出对话。

**如何使用：** 调用 `setModal(...)` 修改 `modal`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setSizeGripEnabled(bool)`

**作用与语义：**

该属性在尺寸握法是否启用时依然成立。
启用该属性时，对话框右下角会放置一个`QSizeGrip`。默认情况下，握把尺寸是禁用的。

**如何使用：** 调用 `setSizeGripEnabled(...)` 修改 `sizeGripEnabled`；传入的新值会成为后续查询和相关界面行为所使用的值。

## 6. 深入实践与常见坑

### 生命周期和资源边界

控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

### 状态和错误边界

控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

### 线程边界

所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

### 最容易出现的错误

不要用固定坐标拼接响应式界面；不要给已经加入布局的控件反复 `setGeometry()`；不要在 `paintEvent()` 中修改业务状态；不要忘记窗口关闭、对象销毁和应用退出是三个不同事件。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QDialog` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
