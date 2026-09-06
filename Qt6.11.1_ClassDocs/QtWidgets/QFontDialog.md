# QFontDialog

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QFontDialog` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QFontDialog` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QFontDialog>`
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

- `enum FontDialogOption { NoButtons, DontUseNativeDialog, ScalableFonts, NonScalableFonts, MonospacedFonts, ProportionalFonts }`
- `flags FontDialogOptions`

### 属性

- `currentFont : QFont`
- `options : FontDialogOptions`

### 公有函数

- `QFontDialog(QWidget *parent = nullptr)`
- `QFontDialog(const QFont &initial, QWidget *parent = nullptr)`
- `QFont currentFont() const`
- `void open(QObject *receiver, const char *member)`
- `QFontDialog::FontDialogOptions options() const`
- `QFont selectedFont() const`
- `void setCurrentFont(const QFont &font)`
- `void setOption(QFontDialog::FontDialogOption option, bool on = true)`
- `void setOptions(QFontDialog::FontDialogOptions options)`
- `bool testOption(QFontDialog::FontDialogOption option) const`

### 重实现的公有函数

- `virtual void setVisible(bool visible) override`

### 信号

- `void currentFontChanged(const QFont &font)`
- `void fontSelected(const QFont &font)`

### 静态公有成员

- `QFont getFont(bool *ok, const QFont &initial, QWidget *parent = nullptr, const QString &title = QString(), QFontDialog::FontDialogOptions options = FontDialogOptions())`
- `QFont getFont(bool *ok, QWidget *parent = nullptr)`

### 重实现的保护函数

- `virtual void changeEvent(QEvent *e) override`
- `virtual void done(int result) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QFontDialog::FontDialogOptionflags QFontDialog::FontDialogOptions`

**作用与语义：**

这个枚举指定了影响字体对话框外观和感觉的各种选项。
例如，它允许指定显示哪种字体类型。如果未指定字体，所有可用字体都会被列出。
请注意，字体过滤选项可能在某些平台（如 Mac）不支持。非原生对话框（在 Windows 或 Linux 上使用）始终支持这些选项。
- `QFontDialog::NoButtons`：`0x00000001`;不显示确定和取消按钮。（对“实时对话”非常有用。）
- `QFontDialog::DontUseNativeDialog`：`0x00000002`;在 Mac 上使用 Qt 的标准字体对话框，而非苹果原生字体面板。
- `QFontDialog::ScalableFonts`：`0x00000004`;显示可扩展字体
- `QFontDialog::NonScalableFonts`：`0x00000008`;显示不可扩展字体
- `QFontDialog::MonospacedFonts`：`0x00000010`;显示等宽字体
- `QFontDialog::ProportionalFonts`：`0x00000020`;显示比例字体
FontDialogOptions 类型是 QFlags 的 typedef<FontDialogOption>。它存储 FontDialogOption 值的 OR 组合。

### `currentFont : QFont`

**作用与语义：**

该属性包含当前对话的字体。

**如何使用：** 调用 `currentFont()` 读取当前值；它不会修改应用状态。

### `options : FontDialogOptions`

**作用与语义：**

该属性包含影响对话视觉和感觉的各种选项。
默认情况下，所有选项都是被禁用的。
选项应在显示对话框前设置好。对话框可见时设置选项不保证会立即对对话框产生影响（具体取决于选项和平台）。

**如何使用：** 调用 `options()` 读取当前值；它不会修改应用状态。

### `[explicit] QFontDialog::QFontDialog(QWidget *parent = nullptr)`

**作用与语义：**

构建标准字体对话框。
用`setCurrentFont()`设置初始字体属性。
`parent`参数传递给`QDialog`构造器。

### `[explicit] QFontDialog::QFontDialog(const QFont &initial, QWidget *parent = nullptr)`

**作用与语义：**

用给定的`parent`和指定的`initial`字体构建标准字体对话框。

### `[override virtual protected] void QFontDialog::changeEvent(QEvent *e)`

**作用与语义：**

重装：`QWidget::changeEvent`（QEvent *事件）。
该事件处理程序可以重新实现以处理状态变化。
该事件中被更改的状态可以通过提供的`event`检索。
变更事件包括：`QEvent::ToolBarChange`、`QEvent::ActivationChange`、`QEvent::EnabledChange`、`QEvent::FontChange`、`QEvent::StyleChange`、`QEvent::PaletteChange`、`QEvent::WindowTitleChange`、`QEvent::IconTextChange`、`QEvent::ModifiedChange`、`QEvent::MouseTrackingChange`、`QEvent::ParentChange`、`QEvent::WindowStateChange`、`QEvent::LanguageChange`、`QEvent::LocaleChange`、`QEvent::LayoutDirectionChange`、`QEvent::ReadOnlyChange`。

### `QFont QFontDialog::currentFont() const`

**作用与语义：**

返回当前字体。
注意：当前字体属性的获取函数。

### `[signal] void QFontDialog::currentFontChanged(const QFont &font)`

**作用与语义：**

该属性包含当前对话的字体。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `currentFont` 的变化，不要把它当作普通函数主动调用。

### `[override virtual protected] void QFontDialog::done(int result)`

**作用与语义：**

重实现自：`QDialog::done`（int r）。
关闭对话并将其结果代码设置为`result`。如果该对话显示为`exec()`，done() 会导致本地事件循环结束，`exec()`返回`result`。
关闭对话并将结果码设置为`r`。`finished()`信号会发出`r`;如果`r`是`QDialog::Accepted`或`QDialog::Rejected`，则分别会发出`accepted()`或`rejected()`信号。
如果该对话显示为`exec()`，done() 也会使本地事件循环结束，`exec()`返回`r`。
与`QWidget::close()`一样，如果设置了`Qt::WA_DeleteOnClose`标志，done() 会删除对话。如果对话框是应用程序的主控件，应用程序会终止。如果对话框是最后关闭的窗口，则发出`QGuiApplication::lastWindowClosed()`信号。

### `[signal] void QFontDialog::fontSelected(const QFont &font)`

**作用与语义：**

当字体被选中时，会发出该信号。所选字体在`font`中指定。
只有当用户选择了最终要使用的字体时，才会发出该信号。在用户在字体对话框中更改当前字体时，信号不会发出。

### `[static] QFont QFontDialog::getFont(bool *ok, const QFont &initial, QWidget *parent = nullptr, const QString &title = QString(), QFontDialog::FontDialogOptions options = FontDialogOptions())`

**作用与语义：**

执行模态字体对话框并返回字体。
如果用户点击确定，所选字体会返回。如果用户点击取消，则返回`initial`字体。
对话由给定的`parent`和`options`中指定的选项构成。`title` 作为对话框的窗口标题显示，`initial` 是最初选择的字体。如果 `ok` 参数不是空的，用户点击确定时所指值设为真，点击取消则设为假。
示例：
该对话框也可以直接设置小部件的字体：
在这个例子中，如果用户点击确定，则使用他们选择的字体;如果点击取消，则使用原字体。

**官方示例：**

```cpp
 bool ok;
 QFont font = QFontDialog::getFont(&ok, QFont("Times", 12), this);
 if (ok) {
     // font is set to the font the user selected
 } else {
     // the user canceled the dialog; font is set to the initial
     // value, in this case Times, 12.
 }
```

### `[static] QFont QFontDialog::getFont(bool *ok, QWidget *parent = nullptr)`

**作用与语义：**

执行模态字体对话框并返回字体。
如果用户点击确定，则返回所选字体。如果用户点击取消，则返回 Qt 默认字体。
对话是基于给定的 `parent` 构建的。如果 `ok` 参数不是空，则当用户点击确定时，所指值设置为真;如果用户点击取消，则设为假。

**官方示例：**

```cpp
 bool ok;
 QFont font = QFontDialog::getFont(&ok, this);
 if (ok) {
     // font is set to the font the user selected
 } else {
     // the user canceled the dialog; font is set to the default
     // application font, QApplication::font()
 }
```

### `void QFontDialog::open(QObject *receiver, const char *member)`

**作用与语义：**

打开对话，并将其`fontSelected()`信号连接到`receiver`和`member`指定的槽位。
当对话关闭时，信号会从槽函数中断开。

### `QFont QFontDialog::selectedFont() const`

**作用与语义：**

通过点击确定或等效按钮返回用户选择的字体。
注意：该字体不总是与`currentFont`属性所持有的字体相同，因为用户可以在最终选择使用之前选择不同的字体。

### `void QFontDialog::setCurrentFont(const QFont &font)`

**作用与语义：**

该属性包含当前对话的字体。

**如何使用：** 调用 `setCurrentFont(...)` 修改 `currentFont`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QFontDialog::setOption(QFontDialog::FontDialogOption option, bool on = true)`

**作用与语义：**

将给定`option`设为启用，`on`为真;否则，清除给定`option`。

### `[override virtual] void QFontDialog::setVisible(bool visible)`

**作用与语义：**

重实现自：`QDialog::setVisible`（bool可见）。
重新实现了属性的访问函数：`QWidget::visible`。

### `bool QFontDialog::testOption(QFontDialog::FontDialogOption option) const`

**作用与语义：**

如果启用给定`option`，返回 `true`;否则返回 false。

### `enum FontDialogOption { NoButtons, DontUseNativeDialog, ScalableFonts, NonScalableFonts, MonospacedFonts, ProportionalFonts }`

**作用与语义：**

这个枚举指定了影响字体对话框外观和感觉的各种选项。
例如，它允许指定显示哪种字体类型。如果未指定字体，所有可用字体都会被列出。
请注意，字体过滤选项可能在某些平台（如 Mac）不支持。非原生对话框（在 Windows 或 Linux 上使用）始终支持这些选项。
- `QFontDialog::NoButtons`：`0x00000001`;不显示确定和取消按钮。（对“实时对话”非常有用。）
- `QFontDialog::DontUseNativeDialog`：`0x00000002`;在 Mac 上使用 Qt 的标准字体对话框，而非苹果原生字体面板。
- `QFontDialog::ScalableFonts`：`0x00000004`;显示可扩展字体
- `QFontDialog::NonScalableFonts`：`0x00000008`;显示不可扩展字体
- `QFontDialog::MonospacedFonts`：`0x00000010`;显示等宽字体
- `QFontDialog::ProportionalFonts`：`0x00000020`;显示比例字体
FontDialogOptions 类型是 QFlags 的 typedef<FontDialogOption>。它存储 FontDialogOption 值的 OR 组合。

### `flags FontDialogOptions`

**作用与语义：**

这个枚举指定了影响字体对话框外观和感觉的各种选项。
例如，它允许指定显示哪种字体类型。如果未指定字体，所有可用字体都会被列出。
请注意，字体过滤选项可能在某些平台（如 Mac）不支持。非原生对话框（在 Windows 或 Linux 上使用）始终支持这些选项。
- `QFontDialog::NoButtons`：`0x00000001`;不显示确定和取消按钮。（对“实时对话”非常有用。）
- `QFontDialog::DontUseNativeDialog`：`0x00000002`;在 Mac 上使用 Qt 的标准字体对话框，而非苹果原生字体面板。
- `QFontDialog::ScalableFonts`：`0x00000004`;显示可扩展字体
- `QFontDialog::NonScalableFonts`：`0x00000008`;显示不可扩展字体
- `QFontDialog::MonospacedFonts`：`0x00000010`;显示等宽字体
- `QFontDialog::ProportionalFonts`：`0x00000020`;显示比例字体
FontDialogOptions 类型是 QFlags 的 typedef<FontDialogOption>。它存储 FontDialogOption 值的 OR 组合。

### `QFontDialog::FontDialogOptions options() const`

**作用与语义：**

该属性包含影响对话视觉和感觉的各种选项。
默认情况下，所有选项都是被禁用的。
选项应在显示对话框前设置好。对话框可见时设置选项不保证会立即对对话框产生影响（具体取决于选项和平台）。

**如何使用：** 调用 `options()` 读取当前值；它不会修改应用状态。

### `void setOptions(QFontDialog::FontDialogOptions options)`

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

`QFontDialog` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
