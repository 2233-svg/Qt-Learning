# QPrintDialog

> Qt 6.11.1 · Qt Print Support

## 1. 先建立直觉

**一句话定位：** `QPrintDialog` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Print Support 提供打印机、打印预览和打印作业相关接口。

### 这是什么

`QPrintDialog` 是 Qt Widgets 界面机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** Widgets 通过父子控件树、布局系统、事件分发和重绘请求组成界面。控件的可见区域、sizeHint、sizePolicy、字体和平台 style 共同影响最终几何；用户输入先进入 Qt 事件系统，再由控件的事件函数、信号或快捷键处理。

**适用场景：** 创建 QApplication 后创建控件，设置 parent 或把控件加入布局，连接用户操作信号，再显示顶层窗口。复合界面用布局嵌套；控件尺寸异常时同时检查 sizePolicy、minimum/maximum size、layout stretch、margins 和 spacing。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要用固定坐标拼接响应式界面；不要给已经加入布局的控件反复 `setGeometry()`；不要在 `paintEvent()` 中修改业务状态；不要忘记窗口关闭、对象销毁和应用退出是三个不同事件。

## 2. 依赖与对象关系

- 头文件：`#include <QPrintDialog>`
- 继承自：QAbstractPrintDialog
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS PrintSupport)
target_link_libraries(mytarget PRIVATE Qt6::PrintSupport)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

Widgets 通过父子控件树、布局系统、事件分发和重绘请求组成界面。控件的可见区域、sizeHint、sizePolicy、字体和平台 style 共同影响最终几何；用户输入先进入 Qt 事件系统，再由控件的事件函数、信号或快捷键处理。

### 状态、生命周期和线程

**生命周期：** 控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

**状态与结果：** 控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

**线程与事件循环：** 所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

## 3. 直接使用

创建 QApplication 后创建控件，设置 parent 或把控件加入布局，连接用户操作信号，再显示顶层窗口。复合界面用布局嵌套；控件尺寸异常时同时检查 sizePolicy、minimum/maximum size、layout stretch、margins 和 spacing。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 属性

- `options : PrintDialogOptions`

### 公有函数

- `QPrintDialog(QWidget *parent = nullptr)`
- `QPrintDialog(QPrinter *printer, QWidget *parent = nullptr)`
- `virtual ~QPrintDialog()`
- `void open(QObject *receiver, const char *member)`
- `QAbstractPrintDialog::PrintDialogOptions options() const`
- `QPrinter * printer()`
- `void setOption(QAbstractPrintDialog::PrintDialogOption option, bool on = true)`
- `void setOptions(QAbstractPrintDialog::PrintDialogOptions options)`
- `bool testOption(QAbstractPrintDialog::PrintDialogOption option) const`

### 重实现的公有函数

- `virtual void done(int result) override`
- `virtual int exec() override`
- `virtual void setVisible(bool visible) override`

### 信号

- `void accepted(QPrinter *printer)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `options : PrintDialogOptions`

**作用与语义：**

该属性包含影响对话视觉和感觉的各种选项。
默认情况下，所有选项都是被禁用的。
选项应在显示对话框前设置好。对话框可见时设置选项不保证会立即对对话框产生影响（具体取决于选项和平台）。

**如何使用：** 调用 `options()` 读取当前值；它不会修改应用状态。

### `[explicit] QPrintDialog::QPrintDialog(QWidget *parent = nullptr)`

**作用与语义：**

构建带有给定`parent`的印刷对话。

### `[explicit] QPrintDialog::QPrintDialog(QPrinter *printer, QWidget *parent = nullptr)`

**作用与语义：**

为给定`printer`和给定`parent`构建新的模态打印机对话框。

### `[virtual noexcept] QPrintDialog::~QPrintDialog()`

**作用与语义：**

会破坏印刷对话。

### `[signal] void QPrintDialog::accepted(QPrinter *printer)`

**作用与语义：**

当用户接受打印对话框中设置的数值时，该信号会发出。`printer`参数包括应用该设置的打印机。

### `[override virtual] void QPrintDialog::done(int result)`

**作用与语义：**

重实现自：`QDialog::done`（int r）。
关闭对话并将其结果代码设置为`result`。如果该对话以`exec()`显示，done() 会导致本地事件循环结束，`exec()`返回`result`。
注意：此功能不适用于Mac的macOS和Windows平台的原生打印对话框，因为该对话框必须是模态的，只有用户能关闭。

### `[override virtual] int QPrintDialog::exec()`

**作用与语义：**

重装：`QDialog::exec()`。

### `void QPrintDialog::open(QObject *receiver, const char *member)`

**作用与语义：**

打开对话，将其`accepted()`信号连接到`receiver`和`member`指定的槽位。
当对话关闭时，信号会从槽函数中断开。

### `QPrinter *QPrintDialog::printer()`

**作用与语义：**

返回该打印机对话框所操作的打印机。这在使用`QPrintDialog::open()`方法时非常有用。

### `void QPrintDialog::setOption(QAbstractPrintDialog::PrintDialogOption option, bool on = true)`

**作用与语义：**

将给定`option`设为启用，`on`为真;否则，清除给定`option`。

### `[override virtual] void QPrintDialog::setVisible(bool visible)`

**作用与语义：**

重装：`QDialog::setVisible`（布尔可见）。

### `bool QPrintDialog::testOption(QAbstractPrintDialog::PrintDialogOption option) const`

**作用与语义：**

如果启用给定`option`，返回 `true`;否则返回 false。

### `QAbstractPrintDialog::PrintDialogOptions options() const`

**作用与语义：**

该属性包含影响对话视觉和感觉的各种选项。
默认情况下，所有选项都是被禁用的。
选项应在显示对话框前设置好。对话框可见时设置选项不保证会立即对对话框产生影响（具体取决于选项和平台）。

**如何使用：** 调用 `options()` 读取当前值；它不会修改应用状态。

### `void setOptions(QAbstractPrintDialog::PrintDialogOptions options)`

**作用与语义：**

该属性包含影响对话视觉和感觉的各种选项。
默认情况下，所有选项都是被禁用的。
选项应在显示对话框前设置好。对话框可见时设置选项不保证会立即对对话框产生影响（具体取决于选项和平台）。

**如何使用：** 调用 `setOptions(...)` 修改 `options`；传入的新值会成为后续查询和相关界面行为所使用的值。

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

`QPrintDialog` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
