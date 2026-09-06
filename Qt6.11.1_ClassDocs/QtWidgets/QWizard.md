# QWizard

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QWizard` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QWizard` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QWizard>`
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

- `enum WizardButton { BackButton, NextButton, CommitButton, FinishButton, CancelButton, …, Stretch }`
- `enum WizardOption { IndependentPages, IgnoreSubTitles, ExtendedWatermarkPixmap, NoDefaultButton, NoBackButtonOnStartPage, …, StretchBanner }`
- `flags WizardOptions`
- `enum WizardPixmap { WatermarkPixmap, LogoPixmap, BannerPixmap, BackgroundPixmap }`
- `enum WizardStyle { ClassicStyle, ModernStyle, MacStyle, AeroStyle }`

### 属性

- `currentId : int`
- `options : WizardOptions`
- `startId : int`
- `subTitleFormat : Qt::TextFormat`
- `titleFormat : Qt::TextFormat`
- `wizardStyle : WizardStyle`

### 公有函数

- `QWizard(QWidget *parent = nullptr, Qt::WindowFlags flags = Qt::WindowFlags())`
- `virtual ~QWizard()`
- `int addPage(QWizardPage *page)`
- `QAbstractButton * button(QWizard::WizardButton which) const`
- `QString buttonText(QWizard::WizardButton which) const`
- `int currentId() const`
- `QWizardPage * currentPage() const`
- `QVariant field(const QString &name) const`
- `bool hasVisitedPage(int id) const`
- `virtual int nextId() const`
- `QWizard::WizardOptions options() const`
- `QWizardPage * page(int id) const`
- `QList<int> pageIds() const`
- `QPixmap pixmap(QWizard::WizardPixmap which) const`
- `void removePage(int id)`
- `void setButton(QWizard::WizardButton which, QAbstractButton *button)`
- `void setButtonLayout(const QList<QWizard::WizardButton> &layout)`
- `void setButtonText(QWizard::WizardButton which, const QString &text)`
- `void setDefaultProperty(const char *className, const char *property, const char *changedSignal)`
- `void setField(const QString &name, const QVariant &value)`
- `void setOption(QWizard::WizardOption option, bool on = true)`
- `void setOptions(QWizard::WizardOptions options)`
- `void setPage(int id, QWizardPage *page)`
- `void setPixmap(QWizard::WizardPixmap which, const QPixmap &pixmap)`
- `void setSideWidget(QWidget *widget)`
- `void setStartId(int id)`
- `void setSubTitleFormat(Qt::TextFormat format)`
- `void setTitleFormat(Qt::TextFormat format)`
- `void setWizardStyle(QWizard::WizardStyle style)`
- `QWidget * sideWidget() const`
- `int startId() const`
- `Qt::TextFormat subTitleFormat() const`
- `bool testOption(QWizard::WizardOption option) const`
- `Qt::TextFormat titleFormat() const`
- `virtual bool validateCurrentPage()`
- `QList<int> visitedIds() const`
- `QWizard::WizardStyle wizardStyle() const`

### 重实现的公有函数

- `virtual void setVisible(bool visible) override`
- `virtual QSize sizeHint() const override`

### 公有槽函数

- `void back()`
- `void next()`
- `void restart()`
- `void setCurrentId(int id)`

### 信号

- `void currentIdChanged(int id)`
- `void customButtonClicked(int which)`
- `void helpRequested()`
- `void pageAdded(int id)`
- `void pageRemoved(int id)`

### 保护函数

- `virtual void cleanupPage(int id)`
- `virtual void initializePage(int id)`

### 重实现的保护函数

- `virtual void done(int result) override`
- `virtual bool event(QEvent *event) override`
- `virtual bool nativeEvent(const QByteArray &eventType, void *message, qintptr *result) override`
- `virtual void paintEvent(QPaintEvent *event) override`
- `virtual void resizeEvent(QResizeEvent *event) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QWizard::WizardButton`

**作用与语义：**

这个枚举指定了巫师中的按钮。
- `QWizard::BackButton`：`0`;返回按钮（macOS上为返回）
- `QWizard::NextButton`：`1`;下一键（macOS上继续）
- `QWizard::CommitButton`：`2`;提交按钮
- `QWizard::FinishButton`：`3`;完成按钮（macOS上完成）
- `QWizard::CancelButton`：`4`;取消按钮（参见`NoCancelButton`）
- `QWizard::HelpButton`：`5`;帮助按钮（另见`HaveHelpButton`）
- `QWizard::CustomButton1`：`6`;第一个用户自定义按钮（参见 `HaveCustomButton1`）
- `QWizard::CustomButton2`：`7`;第二个用户自定义按钮（参见`HaveCustomButton2`）
- `QWizard::CustomButton3`：`8`;第三个用户自定义按钮（参见`HaveCustomButton3`）
以下数值仅在调用`setButtonLayout()`时有用：
- `QWizard::Stretch`：`9`;按钮布局中的水平拉伸

### `enum QWizard::WizardOptionflags QWizard::WizardOptions`

**作用与语义：**

这个枚举具体说明了各种影响巫师外观和感觉的选项。
- `QWizard::IndependentPages`：`0x00000001`;这些页面彼此独立（即它们不互相推导值）。
- `QWizard::IgnoreSubTitles`：`0x00000002`;即使字幕已设置，也不要显示。
- `QWizard::ExtendedWatermarkPixmap`：`0x00000004`;将任何`WatermarkPixmap`延伸到窗边。
- `QWizard::NoDefaultButton`：`0x00000008`;不要把“下一步”或“结束”按钮设为对话的默认按钮。
- `QWizard::NoBackButtonOnStartPage`：`0x00000010`;开始页上不要显示返回按钮。
- `QWizard::NoBackButtonOnLastPage`：`0x00000020`;最后一页不要显示返回按钮。
- `QWizard::DisabledBackButtonOnLastPage`：`0x00000040`;禁用最后一页的返回按钮。
- `QWizard::HaveNextButtonOnLastPage`：`0x00000080`;在最后一页显示（禁用的）下一页按钮。
- `QWizard::HaveFinishButtonOnEarlyPages`：`0x00000100`;在非最终页面显示（禁用的）结束按钮。
- `QWizard::NoCancelButton`：`0x00000200`;不要显示取消按钮。
- `QWizard::CancelButtonOnLeft`：`0x00000400`;取消按钮放在返回的左侧（而不是结束或下一步的右侧）。
- `QWizard::HaveHelpButton`：`0x00000800`;显示帮助按钮。
- `QWizard::HelpButtonOnRight`：`0x00001000`;将帮助按钮放在按钮布局的最右侧（而不是最左侧）。
- `QWizard::HaveCustomButton1`：`0x00002000`;显示第一个用户自定义按钮（`CustomButton1`）。
- `QWizard::HaveCustomButton2`：`0x00004000`;显示第二个用户自定义按钮（`CustomButton2`）。
- `QWizard::HaveCustomButton3`：`0x00008000`;显示第三个用户自定义按钮（`CustomButton3`）。
- `QWizard::NoCancelButtonOnLastPage`：`0x00010000`;最后一页不要显示取消按钮。
- `QWizard::StretchBanner`：`0x00020000`;如果有`banner`，就将其拉伸到整个向导宽度。
WizardOptions 类型是 QFlags 的 typedef<WizardOption>。它存储 WizardOption 值的 OR 组合。

### `enum QWizard::WizardPixmap`

**作用与语义：**

该枚举指定了可以关联到页面的像素映射。
- `QWizard::WatermarkPixmap`：`0`;`ClassicStyle`或`ModernStyle`页左侧的高像素地图
- `QWizard::LogoPixmap`：`1`;`ClassicStyle`或`ModernStyle`页眉右侧的小像素图
- `QWizard::BannerPixmap`：`2`;占据`ModernStyle`页头背景的像素地图
- `QWizard::BackgroundPixmap`：`3`;占据`MacStyle`巫师背景的像素地图

### `enum QWizard::WizardStyle`

**作用与语义：**

该枚举规定了`QWizard`支持的不同外观。
- `QWizard::ClassicStyle`：`0`;经典Windows外观
- `QWizard::ModernStyle`：`1`;现代Windows外观
- `QWizard::MacStyle`：`2`;macOS 风格
- `QWizard::AeroStyle`：`3`;Windows Aero外观

### `currentId : int`

**作用与语义：**

该属性包含当前页面的 ID。
默认情况下，该属性的值为-1，表示当前没有显示任何页面。

**如何使用：** 调用 `currentId()` 读取当前值；它不会修改应用状态。

### `options : WizardOptions`

**作用与语义：**

这个房产包含了影响巫师外观和感觉的各种选项。
默认情况下，以下选项根据平台而定：
- Windows：`HelpButtonOnRight`。
- macOS：`NoDefaultButton` 和 `NoCancelButton`。
- X11 和 QWS（嵌入式 Linux 的 Qt）：无。

**如何使用：** 调用 `options()` 读取当前值；它不会修改应用状态。

### `startId : int`

**作用与语义：**

该属性包含首页的 ID。
如果该属性未被显式设置，则默认为该向导中最低的页面 ID，若尚未插入页面则为 -1。

**如何使用：** 调用 `startId()` 读取当前值；它不会修改应用状态。

### `subTitleFormat : Qt::TextFormat`

**作用与语义：**

该属性保留了页面字幕所使用的文本格式。
默认格式是`Qt::AutoText`。

**如何使用：** 调用 `subTitleFormat()` 读取当前值；它不会修改应用状态。

### `titleFormat : Qt::TextFormat`

**作用与语义：**

该属性包含页面标题所使用的文本格式。
默认格式是`Qt::AutoText`。

**如何使用：** 调用 `titleFormat()` 读取当前值；它不会修改应用状态。

### `wizardStyle : WizardStyle`

**作用与语义：**

这处房产拥有巫师的外观和氛围。
默认情况下，`QWizard` 在启用 alpha 合成的 Windows Vista 系统上使用该`AeroStyle`，无论当前控件样式为何。如果不是这样，默认向导样式取决于当前控件样式，具体如下：`MacStyle` 是当前控件样式 QMacStyle，`ModernStyle` 是默认，`ClassicStyle` 是其他所有情况下的默认。

**如何使用：** 调用 `wizardStyle()` 读取当前值；它不会修改应用状态。

### `[explicit] QWizard::QWizard(QWidget *parent = nullptr, Qt::WindowFlags flags = Qt::WindowFlags())`

**作用与语义：**

用给定的`parent`和窗口`flags`构造一个巫师。

### `[virtual noexcept] QWizard::~QWizard()`

**作用与语义：**

摧毁巫师及其页面，释放所有分配的资源。

### `int QWizard::addPage(QWizardPage *page)`

**作用与语义：**

将给定的`page`添加到向导中，并返回页面的ID。
该ID保证比`QWizard`中其他ID都要大。

### `[slot] void QWizard::back()`

**作用与语义：**

回到上一页。
这相当于按下返回键。

### `QAbstractButton *QWizard::button(QWizard::WizardButton which) const`

**作用与语义：**

返回对应角色`which`的按钮。

### `QString QWizard::buttonText(QWizard::WizardButton which) const`

**作用与语义：**

返回按钮`which`的文本。
如果文本的 ben 设置为 `setButtonText()`，则返回该文本。
默认情况下，按钮上的文字取决于`wizardStyle`。例如，在macOS上，“下一”按钮称为“继续”。

### `[virtual protected] void QWizard::cleanupPage(int id)`

**作用与语义：**

`QWizard`调用该虚拟功能，在用户点击返回前（除非设置了`QWizard::IndependentPages`选项）以清理页面 `id`。
默认实现调用在 page（`id`） 上`QWizardPage::cleanupPage()`。

### `[signal] void QWizard::currentIdChanged(int id)`

**作用与语义：**

该属性包含当前页面的 ID。
默认情况下，该属性的值为-1，表示当前没有显示任何页面。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `currentId` 的变化，不要把它当作普通函数主动调用。

### `QWizardPage *QWizard::currentPage() const`

**作用与语义：**

返回当前页面的指针，若没有当前页面（例如在向导显示之前），则返回`nullptr`。
这相当于调用 page（`currentId()`）。

### `[signal] void QWizard::customButtonClicked(int which)`

**作用与语义：**

当用户点击自定义按钮时，会发出该信号。`which`可以是`CustomButton1`、`CustomButton2`或`CustomButton3`。
默认情况下，不会显示自定义按钮。用`HaveCustomButton1`、`HaveCustomButton2`或`HaveCustomButton3`调用`setOption()`，并用`setButtonText()`或`setButton()`来配置。

### `[override virtual protected] void QWizard::done(int result)`

**作用与语义：**

重装：`QDialog::done`（int r）。
关闭对话并将结果代码设置为`r`。`finished()`信号会发出`r`;如果`r`是`QDialog::Accepted`或`QDialog::Rejected`，则分别会发出`accepted()`或`rejected()`信号。
如果该对话以`exec()`显示，done() 也会导致本地事件循环结束，`exec()`返回`r`。
与`QWidget::close()`一样，如果设置了`Qt::WA_DeleteOnClose`标志，done() 会删除对话。如果对话框是应用程序的主控件，应用程序将终止。如果对话框是最后关闭的窗口，则发出`QGuiApplication::lastWindowClosed()`信号。

### `[override virtual protected] bool QWizard::event(QEvent *event)`

**作用与语义：**

重实现自：`QWidget::event`（QEvent *事件）。

### `QVariant QWizard::field(const QString &name) const`

**作用与语义：**

返回称为 `name` 的字段值。该函数可用于访问向导任意页面上的字段。

### `bool QWizard::hasVisitedPage(int id) const`

**作用与语义：**

如果页面历史包含页面`id`，返回`true`;否则返回`false`。
按返回键再次将当前页面标记为“未访问”。

### `[signal] void QWizard::helpRequested()`

**作用与语义：**

当用户点击帮助按钮时，会发出该信号。
默认情况下，不会显示帮助按钮。调用`setOption`（`HaveHelpButton`，true）以获得帮助按钮。

**官方示例：**

```cpp
 LicenseWizard::LicenseWizard(QWidget *parent)
     : QWizard(parent)
 {
     ...
     setOption(HaveHelpButton, true);
     connect(this, &QWizard::helpRequested, this, &LicenseWizard::showHelp);
     ...
 }

 void LicenseWizard::showHelp()
 {
     static QString lastHelpMessage;

     QString message;

     switch (currentId()) {
     case Page_Intro:
         message = tr("The decision you make here will affect which page you "
                      "get to see next.");
         break;
     ...
     default:
         message = tr("This help is likely not to be of any help.");
     }

     QMessageBox::information(this, tr("License Wizard Help"), message);

 }
```

### `[virtual protected] void QWizard::initializePage(int id)`

**作用与语义：**

`QWizard`调用该虚拟函数，在页面`id`显示前准备页面，无论是因调用`QWizard::restart()`或用户点击“Next”而显示。（但如果设置了`QWizard::IndependentPages`选项，该函数仅在页面首次显示时调用。）。
通过重新实现这个功能，你可以确保页面的字段是基于之前页面字段正确初始化的。
默认实现调用在 page（`id`） 上`QWizardPage::initializePage()`。

### `[override virtual protected] bool QWizard::nativeEvent(const QByteArray &eventType, void *message, qintptr *result)`

**作用与语义：**

Reimplements： `QWidget::nativeEvent`（const QByteArray &eventType， void *message， qintptr *result）.
该特殊事件处理程序可在子类中重新实现，以接收由`eventType`识别的本地平台事件，这些事件通过`message`参数传递。
在你重新实现该函数时，如果你想停止事件被 Qt 处理，请返回 true，设置 `result`。`result` 参数仅在 Windows 上有意义。如果你返回 false，这个原生事件会返回给 Qt，Qt 将事件转换成 Qt 事件并发送给控件。
注意：只有当该控件具有本地窗口句柄时，事件才会传递到该事件处理程序。
注意：该函数对Qt 4的事件过滤函数x11Event()、winEvent()和macEvent()进行了超种。
- `Platform`：事件类型标识符;消息类型;结果类型
- `Windows`：“windows_generic_MSG”;MSG *;LRESULT
- `macOS`：“NSEvent”;NSEvent *
- `XCB`：“xcb_generic_event_t”;xcb_generic_event_t *

### `[slot] void QWizard::next()`

**作用与语义：**

推进到下一页。
这相当于按下“下一步”或“提交”按钮。

### `[virtual] int QWizard::nextId() const`

**作用与语义：**

`QWizard`调用该虚拟功能，以确定用户点击“下一页”时应显示哪个页面。
返回值为下一页的ID，若无页面后进则为-1。
默认实现调用在`currentPage()`上`QWizardPage::nextId()`。
通过重新实现这个函数，你可以指定动态页面顺序。

### `QWizardPage *QWizard::page(int id) const`

**作用与语义：**

返回带有指定页面`id`的页面，若无该页面则返回`nullptr`。

### `[signal] void QWizard::pageAdded(int id)`

**作用与语义：**

每当向导添加页面时，该信号都会发出。页面的 `id` 作为参数传递。

### `QList<int> QWizard::pageIds() const`

**作用与语义：**

返回页面ID列表。

### `[signal] void QWizard::pageRemoved(int id)`

**作用与语义：**

每当页面从向导中移除时，该信号都会发出。该页面的 `id` 作为参数传递。

### `[override virtual protected] void QWizard::paintEvent(QPaintEvent *event)`

**作用与语义：**

重实现自：`QWidget::paintEvent`（QPaintEvent *event）。
该事件处理程序可以在子类中重新实现，以接收 `event` 传递的绘画事件。
绘图事件是请求重新绘制一个小部件的全部或部分。它可能由以下原因之一发生：
- `repaint()`或`update()`被援引，
- 小部件被遮挡，现已被发现，或
- 还有很多其他原因。
许多控件可以在被要求时重新绘制整个表面，但一些慢速控件需要通过仅绘制请求的区域来优化：`QPaintEvent::region()`。这种速度优化不会改变结果，因为在事件处理过程中绘制会被裁剪到该区域。例如，`QListView`和`QTableView`就是这样做的。
Qt 还试图通过将多个绘画事件合并为一个来加快绘画速度。当 `update()` 被多次调用或窗口系统发送多个绘画事件时，Qt 会将这些事件合并为一个区域更大的事件（参见 `QRegion::united()`）。`repaint()` 函数不支持这种优化，因此我们建议尽可能使用 `update()`。
当绘制事件发生时，更新区域通常已经被擦除，所以你是在小部件的背景上作画。
背景可以用`setBackgroundRole()`和`setPalette()`设置。
自 Qt 4.0 起，`QWidget` 会自动双缓冲绘制，因此无需在 paintEvent() 中编写双缓冲代码以避免闪烁。
注意：通常，你应避免在paintEvent()中调用`update()`或`repaint()`。例如，在paintEvent()中调用`update()`或`repaint()`会导致行为未定义;孩子可能会或不会获得绘画事件。
警告：如果你使用没有 Qt backingstore 的自定义绘图引擎，`Qt::WA_PaintOnScreen`必须设置。否则，`QWidget::paintEngine()` 永远不会被调用;Backingstore 将被使用。

### `QPixmap QWizard::pixmap(QWizard::WizardPixmap which) const`

**作用与语义：**

返回角色`which`的像素映射集。
默认情况下，macOS上唯一设置的像素地图是`BackgroundPixmap`。

### `void QWizard::removePage(int id)`

**作用与语义：**

删除带有指定`id`的页面。如有需要，`cleanupPage()`将被调用。
注意：删除页面可能会影响`startId`房产的价值。

### `[override virtual protected] void QWizard::resizeEvent(QResizeEvent *event)`

**作用与语义：**

重实现自：`QDialog::resizeEvent`（QResizeEvent *）。

### `[slot] void QWizard::restart()`

**作用与语义：**

在开始页面重启向导。当向导显示时，该函数会自动调用。

### `void QWizard::setButton(QWizard::WizardButton which, QAbstractButton *button)`

**作用与语义：**

将对应角色`which`的按钮设置为`button`。
要向向导添加额外按钮（例如打印按钮），一种方法是调用 setButton() 并以 `CustomButton1` `CustomButton3`，并通过`HaveCustomButton1` `HaveCustomButton3`选项使按钮可见。

### `void QWizard::setButtonLayout(const QList<QWizard::WizardButton> &layout)`

**作用与语义：**

将按钮显示顺序设置为`layout`，其中`layout`是`WizardButton`的列表。
默认布局取决于设置的选项（例如是否`HelpButtonOnRight`）。如果你需要比 `options` 现有的更控制按钮布局，可以调用这个函数。
你可以用`Stretch`在布局中指定水平拉伸。

**官方示例：**

```cpp
 MyWizard::MyWizard(QWidget *parent)
     : QWizard(parent)
 {
     //...
     QList<QWizard::WizardButton> layout;
     layout << QWizard::Stretch << QWizard::BackButton << QWizard::CancelButton
            << QWizard::NextButton << QWizard::FinishButton;
     setButtonLayout(layout);
     //...
 }
```

### `void QWizard::setButtonText(QWizard::WizardButton which, const QString &text)`

**作用与语义：**

把按钮`which`上的文字设置为`text`。
默认情况下，按钮上的文字取决于`wizardStyle`。例如，在macOS上，“下一”按钮称为“继续”。
要向向导添加额外按钮（例如打印按钮），一种方法是调用 setButtonText() 并使用 `CustomButton1`、`CustomButton2` 或 `CustomButton3` 设置文本，并通过 `HaveCustomButton1`、`HaveCustomButton2` 和/或 `HaveCustomButton3` 选项使按钮可见。
按钮文本也可以按页面设置，使用`QWizardPage::setButtonText()`。

### `[slot] void QWizard::setCurrentId(int id)`

**作用与语义：**

该属性包含当前页面的 ID。
默认情况下，该属性的值为-1，表示当前没有显示任何页面。

**如何使用：** 调用 `setCurrentId(...)` 修改 `currentId`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QWizard::setDefaultProperty(const char *className, const char *property, const char *changedSignal)`

**作用与语义：**

将`className`的默认属性设置为`property`，并使相关的变更信号为`changedSignal`。
当 `className` 实例（或其子类之一）传递给 `QWizardPage::registerField()` 且未指定属性时，默认属性被使用。
`QWizard`知道最常见的Qt控件。对于这些（或其子类），你不需要指定`property`或`changedSignal`。下表列出了这些控件：
- `Widget`：属性;变更通知信号
- `QAbstractButton`：bool `checked`;`toggled()`
- `QAbstractSlider`：智力`value`;`valueChanged()`
- `QComboBox`：智力`currentIndex`;`currentIndexChanged()`
- `QDateTimeEdit`：`QDateTime` `dateTime`;`dateTimeChanged()`
- `QLineEdit`：`QString` `text`;`textChanged()`
- `QListWidget`：智力`currentRow`;`currentRowChanged()`
- `QSpinBox`：智力`value`;`valueChanged()`

### `void QWizard::setField(const QString &name, const QVariant &value)`

**作用与语义：**

将称为`name`的字段值设置为`value`。
该函数可用于在向导的任何页面上设置字段。

### `void QWizard::setOption(QWizard::WizardOption option, bool on = true)`

**作用与语义：**

将给定`option`设为启用，`on`为真;否则，清除给定`option`。

### `void QWizard::setPage(int id, QWizardPage *page)`

**作用与语义：**

用指定`id`将给定的`page`加到法师上。
注意：如果页面未被明确设置，添加页面可能会影响`startId`属性的价值。

### `void QWizard::setPixmap(QWizard::WizardPixmap which, const QPixmap &pixmap)`

**作用与语义：**

将角色`which`的像素映射设置为`pixmap`。
像素地图是`QWizard`在显示页面时使用的。具体使用哪些像素地图取决于向导的风格。
像素地图也可以用`QWizardPage::setPixmap()`为特定页面设置。

### `void QWizard::setSideWidget(QWidget *widget)`

**作用与语义：**

将给定`widget`设置在向导左侧显示。对于使用`WatermarkPixmap`的样式（`ClassicStyle`和`ModernStyle`），侧边小部件显示在水印顶部;对于其他样式或未提供水印时，侧边小部件显示在向导左侧。
传递`nullptr`时没有侧边小部件。
当`widget`不`nullptr`时，巫师会重新养育它。
之前的侧边小部件都被隐藏了。
你可以在不同时间调用 setSideWidget() 使用相同的控件。
当小部件被销毁时，所有设置在这里的控件都会被向导删除，除非你在设置其他侧边小部件（或`nullptr`）后单独重新子长该小部件。
默认情况下，没有任何侧边小部件。

### `[override virtual] void QWizard::setVisible(bool visible)`

**作用与语义：**

重实现自：`QDialog::setVisible`（bool可见）。
重新实现了属性的访问函数：`QWidget::visible`。

### `QWidget *QWizard::sideWidget() const`

**作用与语义：**

返回向导或`nullptr`左侧的小部件。
默认情况下，没有任何侧边小部件。

### `[override virtual] QSize QWizard::sizeHint() const`

**作用与语义：**

重装：`QDialog::sizeHint()` const.
重新实现了属性的访问函数：`QWidget::sizeHint`。

### `bool QWizard::testOption(QWizard::WizardOption option) const`

**作用与语义：**

如果启用给定`option`，返回 `true`;否则返回 false。

### `[virtual] bool QWizard::validateCurrentPage()`

**作用与语义：**

当用户点击“下一步”或“完成”以进行最后时刻的验证时，`QWizard`调用了这个虚拟函数。如果返回`true`，下一页就会显示（或向导完成）;否则，当前页面保持在线。
默认实现调用在`currentPage()`上`QWizardPage::validatePage()`。
如果可能，通常禁用 Next 或 Finish 按钮（通过指定必填字段或重新实现 `QWizardPage::isComplete()`）比重新实现 validCurrentPage() 更符合风格。

### `QList<int> QWizard::visitedIds() const`

**作用与语义：**

返回访问页面的ID列表，按访问顺序排列。

### `enum WizardOption { IndependentPages, IgnoreSubTitles, ExtendedWatermarkPixmap, NoDefaultButton, NoBackButtonOnStartPage, …, StretchBanner }`

**作用与语义：**

这个枚举具体说明了各种影响巫师外观和感觉的选项。
- `QWizard::IndependentPages`：`0x00000001`;这些页面彼此独立（即它们不互相推导值）。
- `QWizard::IgnoreSubTitles`：`0x00000002`;即使字幕已设置，也不要显示。
- `QWizard::ExtendedWatermarkPixmap`：`0x00000004`;将任何`WatermarkPixmap`延伸到窗边。
- `QWizard::NoDefaultButton`：`0x00000008`;不要把“下一步”或“结束”按钮设为对话的默认按钮。
- `QWizard::NoBackButtonOnStartPage`：`0x00000010`;开始页上不要显示返回按钮。
- `QWizard::NoBackButtonOnLastPage`：`0x00000020`;最后一页不要显示返回按钮。
- `QWizard::DisabledBackButtonOnLastPage`：`0x00000040`;禁用最后一页的返回按钮。
- `QWizard::HaveNextButtonOnLastPage`：`0x00000080`;在最后一页显示（禁用的）下一页按钮。
- `QWizard::HaveFinishButtonOnEarlyPages`：`0x00000100`;在非最终页面显示（禁用的）结束按钮。
- `QWizard::NoCancelButton`：`0x00000200`;不要显示取消按钮。
- `QWizard::CancelButtonOnLeft`：`0x00000400`;取消按钮放在返回的左侧（而不是结束或下一步的右侧）。
- `QWizard::HaveHelpButton`：`0x00000800`;显示帮助按钮。
- `QWizard::HelpButtonOnRight`：`0x00001000`;将帮助按钮放在按钮布局的最右侧（而不是最左侧）。
- `QWizard::HaveCustomButton1`：`0x00002000`;显示第一个用户自定义按钮（`CustomButton1`）。
- `QWizard::HaveCustomButton2`：`0x00004000`;显示第二个用户自定义按钮（`CustomButton2`）。
- `QWizard::HaveCustomButton3`：`0x00008000`;显示第三个用户自定义按钮（`CustomButton3`）。
- `QWizard::NoCancelButtonOnLastPage`：`0x00010000`;最后一页不要显示取消按钮。
- `QWizard::StretchBanner`：`0x00020000`;如果有`banner`，就将其拉伸到整个向导宽度。
WizardOptions 类型是 QFlags 的 typedef<WizardOption>。它存储 WizardOption 值的 OR 组合。

### `flags WizardOptions`

**作用与语义：**

这个枚举具体说明了各种影响巫师外观和感觉的选项。
- `QWizard::IndependentPages`：`0x00000001`;这些页面彼此独立（即它们不互相推导值）。
- `QWizard::IgnoreSubTitles`：`0x00000002`;即使字幕已设置，也不要显示。
- `QWizard::ExtendedWatermarkPixmap`：`0x00000004`;将任何`WatermarkPixmap`延伸到窗边。
- `QWizard::NoDefaultButton`：`0x00000008`;不要把“下一步”或“结束”按钮设为对话的默认按钮。
- `QWizard::NoBackButtonOnStartPage`：`0x00000010`;开始页上不要显示返回按钮。
- `QWizard::NoBackButtonOnLastPage`：`0x00000020`;最后一页不要显示返回按钮。
- `QWizard::DisabledBackButtonOnLastPage`：`0x00000040`;禁用最后一页的返回按钮。
- `QWizard::HaveNextButtonOnLastPage`：`0x00000080`;在最后一页显示（禁用的）下一页按钮。
- `QWizard::HaveFinishButtonOnEarlyPages`：`0x00000100`;在非最终页面显示（禁用的）结束按钮。
- `QWizard::NoCancelButton`：`0x00000200`;不要显示取消按钮。
- `QWizard::CancelButtonOnLeft`：`0x00000400`;取消按钮放在返回的左侧（而不是结束或下一步的右侧）。
- `QWizard::HaveHelpButton`：`0x00000800`;显示帮助按钮。
- `QWizard::HelpButtonOnRight`：`0x00001000`;将帮助按钮放在按钮布局的最右侧（而不是最左侧）。
- `QWizard::HaveCustomButton1`：`0x00002000`;显示第一个用户自定义按钮（`CustomButton1`）。
- `QWizard::HaveCustomButton2`：`0x00004000`;显示第二个用户自定义按钮（`CustomButton2`）。
- `QWizard::HaveCustomButton3`：`0x00008000`;显示第三个用户自定义按钮（`CustomButton3`）。
- `QWizard::NoCancelButtonOnLastPage`：`0x00010000`;最后一页不要显示取消按钮。
- `QWizard::StretchBanner`：`0x00020000`;如果有`banner`，就将其拉伸到整个向导宽度。
WizardOptions 类型是 QFlags 的 typedef<WizardOption>。它存储 WizardOption 值的 OR 组合。

### `int currentId() const`

**作用与语义：**

该属性包含当前页面的 ID。
默认情况下，该属性的值为-1，表示当前没有显示任何页面。

**如何使用：** 调用 `currentId()` 读取当前值；它不会修改应用状态。

### `QWizard::WizardOptions options() const`

**作用与语义：**

这个房产包含了影响巫师外观和感觉的各种选项。
默认情况下，以下选项根据平台而定：
- Windows：`HelpButtonOnRight`。
- macOS：`NoDefaultButton` 和 `NoCancelButton`。
- X11 和 QWS（嵌入式 Linux 的 Qt）：无。

**如何使用：** 调用 `options()` 读取当前值；它不会修改应用状态。

### `void setOptions(QWizard::WizardOptions options)`

**作用与语义：**

这个房产包含了影响巫师外观和感觉的各种选项。
默认情况下，以下选项根据平台而定：
- Windows：`HelpButtonOnRight`。
- macOS：`NoDefaultButton` 和 `NoCancelButton`。
- X11 和 QWS（嵌入式 Linux 的 Qt）：无。

**如何使用：** 调用 `setOptions(...)` 修改 `options`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setStartId(int id)`

**作用与语义：**

该属性包含首页的 ID。
如果该属性未被显式设置，则默认为该向导中最低的页面 ID，若尚未插入页面则为 -1。

**如何使用：** 调用 `setStartId(...)` 修改 `startId`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setSubTitleFormat(Qt::TextFormat format)`

**作用与语义：**

该属性保留了页面字幕所使用的文本格式。
默认格式是`Qt::AutoText`。

**如何使用：** 调用 `setSubTitleFormat(...)` 修改 `subTitleFormat`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTitleFormat(Qt::TextFormat format)`

**作用与语义：**

该属性包含页面标题所使用的文本格式。
默认格式是`Qt::AutoText`。

**如何使用：** 调用 `setTitleFormat(...)` 修改 `titleFormat`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setWizardStyle(QWizard::WizardStyle style)`

**作用与语义：**

这处房产拥有巫师的外观和氛围。
默认情况下，`QWizard` 在启用 alpha 合成的 Windows Vista 系统上使用该`AeroStyle`，无论当前控件样式为何。如果不是这样，默认向导样式取决于当前控件样式，具体如下：`MacStyle` 是当前控件样式 QMacStyle，`ModernStyle` 是默认，`ClassicStyle` 是其他所有情况下的默认。

**如何使用：** 调用 `setWizardStyle(...)` 修改 `wizardStyle`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `int startId() const`

**作用与语义：**

该属性包含首页的 ID。
如果该属性未被显式设置，则默认为该向导中最低的页面 ID，若尚未插入页面则为 -1。

**如何使用：** 调用 `startId()` 读取当前值；它不会修改应用状态。

### `Qt::TextFormat subTitleFormat() const`

**作用与语义：**

该属性保留了页面字幕所使用的文本格式。
默认格式是`Qt::AutoText`。

**如何使用：** 调用 `subTitleFormat()` 读取当前值；它不会修改应用状态。

### `Qt::TextFormat titleFormat() const`

**作用与语义：**

该属性包含页面标题所使用的文本格式。
默认格式是`Qt::AutoText`。

**如何使用：** 调用 `titleFormat()` 读取当前值；它不会修改应用状态。

### `QWizard::WizardStyle wizardStyle() const`

**作用与语义：**

这处房产拥有巫师的外观和氛围。
默认情况下，`QWizard` 在启用 alpha 合成的 Windows Vista 系统上使用该`AeroStyle`，无论当前控件样式为何。如果不是这样，默认向导样式取决于当前控件样式，具体如下：`MacStyle` 是当前控件样式 QMacStyle，`ModernStyle` 是默认，`ClassicStyle` 是其他所有情况下的默认。

**如何使用：** 调用 `wizardStyle()` 读取当前值；它不会修改应用状态。

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

`QWizard` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
