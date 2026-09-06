# QColorDialog

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QColorDialog` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QColorDialog` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QColorDialog>`
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

### 公有类型

- `enum ColorDialogOption { ShowAlphaChannel, NoButtons, NoEyeDropperButton, DontUseNativeDialog }`
- `flags ColorDialogOptions`

### 属性

- `currentColor : QColor`
- `options : ColorDialogOptions`

### 公有函数

- `QColorDialog(QWidget *parent = nullptr)`
- `QColorDialog(const QColor &initial, QWidget *parent = nullptr)`
- `virtual ~QColorDialog()`
- `QColor currentColor() const`
- `void open(QObject *receiver, const char *member)`
- `QColorDialog::ColorDialogOptions options() const`
- `QColor selectedColor() const`
- `void setCurrentColor(const QColor &color)`
- `void setOption(QColorDialog::ColorDialogOption option, bool on = true)`
- `void setOptions(QColorDialog::ColorDialogOptions options)`
- `bool testOption(QColorDialog::ColorDialogOption option) const`

### 重实现的公有函数

- `virtual void setVisible(bool visible) override`

### 信号

- `void colorSelected(const QColor &color)`
- `void currentColorChanged(const QColor &color)`

### 静态公有成员

- `QColor customColor(int index)`
- `int customCount()`
- `QColor getColor(const QColor &initial = Qt::white, QWidget *parent = nullptr, const QString &title = QString(), QColorDialog::ColorDialogOptions options = ColorDialogOptions())`
- `void setCustomColor(int index, QColor color)`
- `void setStandardColor(int index, QColor color)`
- `QColor standardColor(int index)`

### 重实现的保护函数

- `virtual void changeEvent(QEvent *e) override`
- `virtual void done(int result) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QColorDialog::ColorDialogOptionflags QColorDialog::ColorDialogOptions`

**作用与语义：**

该枚举指定了影响色彩对话外观和感觉的各种选项。
- `QColorDialog::ShowAlphaChannel`：`0x00000001`;允许用户选择颜色的α成分。
- `QColorDialog::NoButtons`：`0x00000002`;不显示确定和取消按钮。（对“实时对话”非常有用。）
- `QColorDialog::NoEyeDropperButton`：`0x00000008`;隐藏滴管按钮。该值在第6.6个季度添加。
- `QColorDialog::DontUseNativeDialog`：`0x00000004`;使用 Qt 的标准颜色对话框，而非操作系统原生颜色对话框。
ColorDialogOptions 类型是 QFlags 的 typedef<ColorDialogOption>。它存储 ColorDialogOption 值的 OR 组合。

### `currentColor : QColor`

**作用与语义：**

该属性保留对话中当前选中的颜色。

**如何使用：** 调用 `currentColor()` 读取当前值；它不会修改应用状态。

### `options : ColorDialogOptions`

**作用与语义：**

该属性包含影响对话视觉和感觉的各种选项。
默认情况下，所有选项都是被禁用的。
选项应在显示对话框前设置好。对话框可见时设置选项不保证会立即对对话框产生影响（具体取决于选项和平台）。

**如何使用：** 调用 `options()` 读取当前值；它不会修改应用状态。

### `[explicit] QColorDialog::QColorDialog(QWidget *parent = nullptr)`

**作用与语义：**

用给定的`parent`构建一个颜色对话。

### `[explicit] QColorDialog::QColorDialog(const QColor &initial, QWidget *parent = nullptr)`

**作用与语义：**

构建一个颜色对话，使用给定的`parent`和指定的`initial`颜色。

### `[virtual noexcept] QColorDialog::~QColorDialog()`

**作用与语义：**

破坏了彩色对话。

### `[override virtual protected] void QColorDialog::changeEvent(QEvent *e)`

**作用与语义：**

重装：`QWidget::changeEvent`（QEvent *事件）。
该事件处理程序可以重新实现以处理状态变化。
该事件中被更改的状态可以通过提供的`event`检索。
变更事件包括：`QEvent::ToolBarChange`、`QEvent::ActivationChange`、`QEvent::EnabledChange`、`QEvent::FontChange`、`QEvent::StyleChange`、`QEvent::PaletteChange`、`QEvent::WindowTitleChange`、`QEvent::IconTextChange`、`QEvent::ModifiedChange`、`QEvent::MouseTrackingChange`、`QEvent::ParentChange`、`QEvent::WindowStateChange`、`QEvent::LanguageChange`、`QEvent::LocaleChange`、`QEvent::LayoutDirectionChange`、`QEvent::ReadOnlyChange`。

### `[signal] void QColorDialog::colorSelected(const QColor &color)`

**作用与语义：**

该信号在用户点击确定选择颜色后发出。选择颜色由`color`决定。

### `[signal] void QColorDialog::currentColorChanged(const QColor &color)`

**作用与语义：**

该属性保留对话中当前选中的颜色。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `currentColor` 的变化，不要把它当作普通函数主动调用。

### `[static] QColor QColorDialog::customColor(int index)`

**作用与语义：**

在给定`index`返回自定义颜色，作为`QColor`值。

### `[static] int QColorDialog::customCount()`

**作用与语义：**

返回`QColorDialog`支持的自定义颜色数量。所有颜色对话框共享相同的自定义颜色。

### `[override virtual protected] void QColorDialog::done(int result)`

**作用与语义：**

重实现自：`QDialog::done`（int r）。
关闭对话并将其结果代码设置为`result`。如果该对话显示为`exec()`，done() 会导致本地事件循环结束，`exec()`返回`result`。
关闭对话并将结果码设置为`r`。`finished()`信号会发出`r`;如果`r`是`QDialog::Accepted`或`QDialog::Rejected`，则分别会发出`accepted()`或`rejected()`信号。
如果该对话显示为`exec()`，done() 也会使本地事件循环结束，`exec()`返回`r`。
与`QWidget::close()`一样，如果设置了`Qt::WA_DeleteOnClose`标志，done() 会删除对话。如果对话框是应用程序的主控件，应用程序会终止。如果对话框是最后关闭的窗口，则发出`QGuiApplication::lastWindowClosed()`信号。

### `[static] QColor QColorDialog::getColor(const QColor &initial = Qt::white, QWidget *parent = nullptr, const QString &title = QString(), QColorDialog::ColorDialogOptions options = ColorDialogOptions())`

**作用与语义：**

弹出一个带有指定窗口`title`的模态颜色对话框（若未指定则为“选择颜色”），允许用户选择颜色，并返回该颜色。颜色初始设置为`initial`。该对话框是`parent`的子。如果用户取消对话，它会返回一个无效（见`QColor::isValid()`）颜色。
`options`论点允许你自定义对话内容。

### `void QColorDialog::open(QObject *receiver, const char *member)`

**作用与语义：**

打开对话，并将其`colorSelected()`信号连接到`receiver`和`member`指定的槽函数。
当对话关闭时，信号会从槽函数中断开。

### `QColor QColorDialog::selectedColor() const`

**作用与语义：**

通过点击确定或等效按钮返回用户选择的颜色。
注意：该颜色不总是与`currentColor`属性所持有的颜色相同，因为用户可以在最终选择使用之前选择不同颜色。

### `[static] void QColorDialog::setCustomColor(int index, QColor color)`

**作用与语义：**

将自定义颜色设置为`index`的 `QColor` `color` 值。
注意：该功能不适用于macOS平台上的原生色彩对话框。如果你仍然需要这个功能，请使用`QColorDialog::DontUseNativeDialog`选项。

### `void QColorDialog::setOption(QColorDialog::ColorDialogOption option, bool on = true)`

**作用与语义：**

将给定`option`设为启用，`on`为真;否则，清除给定`option`。

### `[static] void QColorDialog::setStandardColor(int index, QColor color)`

**作用与语义：**

将`index`的标准颜色设置为`QColor` `color`值。
注意：该功能不适用于macOS平台上的原生色彩对话框。如果您仍然需要此功能，请使用`QColorDialog::DontUseNativeDialog`选项。

### `[override virtual] void QColorDialog::setVisible(bool visible)`

**作用与语义：**

重构：`QDialog::setVisible`（bool可见）。
改变对话的可见性。如果`visible`为真，对话会显示;否则，对话是隐藏的。
重新实现属性访问函数：`QWidget::visible`。

### `[static] QColor QColorDialog::standardColor(int index)`

**作用与语义：**

返回给定`index`的标准颜色，作为`QColor`值。

### `bool QColorDialog::testOption(QColorDialog::ColorDialogOption option) const`

**作用与语义：**

如果启用给定`option`，返回 `true`;否则返回 false。

### `enum ColorDialogOption { ShowAlphaChannel, NoButtons, NoEyeDropperButton, DontUseNativeDialog }`

**作用与语义：**

该枚举指定了影响色彩对话外观和感觉的各种选项。
- `QColorDialog::ShowAlphaChannel`：`0x00000001`;允许用户选择颜色的α成分。
- `QColorDialog::NoButtons`：`0x00000002`;不显示确定和取消按钮。（对“实时对话”非常有用。）
- `QColorDialog::NoEyeDropperButton`：`0x00000008`;隐藏滴管按钮。该值在第6.6个季度添加。
- `QColorDialog::DontUseNativeDialog`：`0x00000004`;使用 Qt 的标准颜色对话框，而非操作系统原生颜色对话框。
ColorDialogOptions 类型是 QFlags 的 typedef<ColorDialogOption>。它存储 ColorDialogOption 值的 OR 组合。

### `flags ColorDialogOptions`

**作用与语义：**

该枚举指定了影响色彩对话外观和感觉的各种选项。
- `QColorDialog::ShowAlphaChannel`：`0x00000001`;允许用户选择颜色的α成分。
- `QColorDialog::NoButtons`：`0x00000002`;不显示确定和取消按钮。（对“实时对话”非常有用。）
- `QColorDialog::NoEyeDropperButton`：`0x00000008`;隐藏滴管按钮。该值在第6.6个季度添加。
- `QColorDialog::DontUseNativeDialog`：`0x00000004`;使用 Qt 的标准颜色对话框，而非操作系统原生颜色对话框。
ColorDialogOptions 类型是 QFlags 的 typedef<ColorDialogOption>。它存储 ColorDialogOption 值的 OR 组合。

### `QColor currentColor() const`

**作用与语义：**

该属性保留对话中当前选中的颜色。

**如何使用：** 调用 `currentColor()` 读取当前值；它不会修改应用状态。

### `QColorDialog::ColorDialogOptions options() const`

**作用与语义：**

该属性包含影响对话视觉和感觉的各种选项。
默认情况下，所有选项都是被禁用的。
选项应在显示对话框前设置好。对话框可见时设置选项不保证会立即对对话框产生影响（具体取决于选项和平台）。

**如何使用：** 调用 `options()` 读取当前值；它不会修改应用状态。

### `void setCurrentColor(const QColor &color)`

**作用与语义：**

该属性保留对话中当前选中的颜色。

**如何使用：** 调用 `setCurrentColor(...)` 修改 `currentColor`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setOptions(QColorDialog::ColorDialogOptions options)`

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

优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QColorDialog` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
