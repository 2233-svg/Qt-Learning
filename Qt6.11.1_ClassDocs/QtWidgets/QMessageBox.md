# QMessageBox

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QMessageBox` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QMessageBox` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QMessageBox>`
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

- `enum ButtonRole { InvalidRole, AcceptRole, RejectRole, DestructiveRole, ActionRole, …, ResetRole }`
- `enum Icon { NoIcon, Question, Information, Warning, Critical }`
- `(since 6.6) enum class Option { DontUseNativeDialog }`
- `flags Options`
- `enum StandardButton { Ok, Open, Save, Cancel, Close, …, ButtonMask }`
- `flags StandardButtons`

### 属性

- `detailedText : QString`
- `icon : Icon`
- `iconPixmap : QPixmap`
- `informativeText : QString`
- `(since 6.6) options : Options`
- `standardButtons : StandardButtons`
- `text : QString`
- `textFormat : Qt::TextFormat`
- `textInteractionFlags : Qt::TextInteractionFlags`

### 公有函数

- `QMessageBox(QWidget *parent = nullptr)`
- `QMessageBox(QMessageBox::Icon icon, const QString &title, const QString &text, QMessageBox::StandardButtons buttons = NoButton, QWidget *parent = nullptr, Qt::WindowFlags f = Qt::Dialog | Qt::MSWindowsFixedSizeDialogHint)`
- `virtual ~QMessageBox()`
- `void addButton(QAbstractButton *button, QMessageBox::ButtonRole role)`
- `QPushButton * addButton(QMessageBox::StandardButton button)`
- `QPushButton * addButton(const QString &text, QMessageBox::ButtonRole role)`
- `QAbstractButton * button(QMessageBox::StandardButton which) const`
- `QMessageBox::ButtonRole buttonRole(QAbstractButton *button) const`
- `QList<QAbstractButton *> buttons() const`
- `QCheckBox * checkBox() const`
- `QAbstractButton * clickedButton() const`
- `QPushButton * defaultButton() const`
- `QString detailedText() const`
- `QAbstractButton * escapeButton() const`
- `QMessageBox::Icon icon() const`
- `QPixmap iconPixmap() const`
- `QString informativeText() const`
- `void open(QObject *receiver, const char *member)`
- `QMessageBox::Options options() const`
- `void removeButton(QAbstractButton *button)`
- `void setCheckBox(QCheckBox *cb)`
- `void setDefaultButton(QMessageBox::StandardButton button)`
- `void setDefaultButton(QPushButton *button)`
- `void setDetailedText(const QString &text)`
- `void setEscapeButton(QAbstractButton *button)`
- `void setEscapeButton(QMessageBox::StandardButton button)`
- `void setIcon(QMessageBox::Icon)`
- `void setIconPixmap(const QPixmap &pixmap)`
- `void setInformativeText(const QString &text)`
- `(since 6.6) void setOption(QMessageBox::Option option, bool on = true)`
- `void setOptions(QMessageBox::Options options)`
- `void setStandardButtons(QMessageBox::StandardButtons buttons)`
- `void setText(const QString &text)`
- `void setTextFormat(Qt::TextFormat format)`
- `void setTextInteractionFlags(Qt::TextInteractionFlags flags)`
- `void setWindowModality(Qt::WindowModality windowModality)`
- `void setWindowTitle(const QString &title)`
- `QMessageBox::StandardButton standardButton(QAbstractButton *button) const`
- `QMessageBox::StandardButtons standardButtons() const`
- `(since 6.6) bool testOption(QMessageBox::Option option) const`
- `QString text() const`
- `Qt::TextFormat textFormat() const`
- `Qt::TextInteractionFlags textInteractionFlags() const`

### 公有槽函数

- `virtual int exec() override`

### 信号

- `void buttonClicked(QAbstractButton *button)`

### 静态公有成员

- `void about(QWidget *parent, const QString &title, const QString &text)`
- `void aboutQt(QWidget *parent, const QString &title = QString())`
- `QMessageBox::StandardButton critical(QWidget *parent, const QString &title, const QString &text, QMessageBox::StandardButtons buttons = Ok, QMessageBox::StandardButton defaultButton = NoButton)`
- `QMessageBox::StandardButton information(QWidget *parent, const QString &title, const QString &text, QMessageBox::StandardButtons buttons = Ok, QMessageBox::StandardButton defaultButton = NoButton)`
- `QMessageBox::StandardButton question(QWidget *parent, const QString &title, const QString &text, QMessageBox::StandardButtons buttons = StandardButtons(Yes | No), QMessageBox::StandardButton defaultButton = NoButton)`
- `QMessageBox::StandardButton warning(QWidget *parent, const QString &title, const QString &text, QMessageBox::StandardButtons buttons = Ok, QMessageBox::StandardButton defaultButton = NoButton)`

### 重实现的保护函数

- `virtual void changeEvent(QEvent *ev) override`
- `virtual void closeEvent(QCloseEvent *e) override`
- `virtual bool event(QEvent *e) override`
- `virtual void keyPressEvent(QKeyEvent *e) override`
- `virtual void resizeEvent(QResizeEvent *event) override`
- `virtual void showEvent(QShowEvent *e) override`

### 公开宏

- `QT_REQUIRE_VERSION(int argc, char **argv, const char *version)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QMessageBox::ButtonRole`

**作用与语义：**

此枚举描述了可用于描述按钮框中按钮的角色。这些角色的组合用作标志，用于描述其行为的不同方面。
- `QMessageBox::InvalidRole`: `-1`; 按钮无效。
- `QMessageBox::AcceptRole`: `0`; 点击按钮会使对话框被接受（例如，确定）。
- `QMessageBox::RejectRole`: `1`; 点击按钮会使对话框被拒绝（例如，取消）。
- `QMessageBox::DestructiveRole`: `2`; 点击按钮会导致破坏性更改（例如，放弃更改）并关闭对话框。
- `QMessageBox::ActionRole`: `3`; 点击按钮会对对话框中的元素进行更改。
- `QMessageBox::HelpRole`: `4`; 按钮可点击以请求帮助。
- `QMessageBox::YesRole`: `5`; 按钮是类似“是”的按钮。
- `QMessageBox::NoRole`: `6`; 按钮是类似“否”的按钮。
- `QMessageBox::ApplyRole`: `8`; 按钮应用当前更改。
- `QMessageBox::ResetRole`: `7`; 按钮将对话框的字段重置为默认值。

### `enum QMessageBox::Icon`

**作用与语义：**

该枚举具有以下数值：
- `QMessageBox::NoIcon`：`0`;消息框没有任何图标。
- `QMessageBox::Question`：`4`;一个图标表示消息正在提问。
- `QMessageBox::Information`：`1`;一个图标，表示消息没有异常。
- `QMessageBox::Warning`：`2`;一个图标表示该消息是警告，但可以处理。
- `QMessageBox::Critical`：`3`;一个图标表示该消息代表一个关键问题。

### `[since 6.6] enum class QMessageBox::Optionflags QMessageBox::Options`

**作用与语义：**

- `QMessageBox::Option::DontUseNativeDialog`：`0x00000001`;不要使用原生消息对话框。
该枚举于Qt 6.6引入。
Options 类型是 QFlags 的 typedef<Option>。它存储 Option 值的 OR 组合。

### `enum QMessageBox::StandardButtonflags QMessageBox::StandardButtons`

**作用与语义：**

这些枚举描述了标准按钮的标志。每个按钮都有定义的`ButtonRole`。
- `QMessageBox::Ok`：`0x00000400`;一个“确定”按钮，定义为`AcceptRole`。
- `QMessageBox::Open`：`0x00002000`;一个“打开”按钮，定义为`AcceptRole`。
- `QMessageBox::Save`：`0x00000800`;一个“保存”按钮，定义为`AcceptRole`。
- `QMessageBox::Cancel`：`0x00400000`;一个用`RejectRole`定义的“取消”按钮。
- `QMessageBox::Close`：`0x00200000`;一个“关闭”按钮，定义为`RejectRole`。
- `QMessageBox::Discard`：`0x00800000`;根据平台不同，一个“弃掉”或“不保存”按钮，由`DestructiveRole`定义。
- `QMessageBox::Apply`：`0x02000000`;一个“应用”按钮，定义为`ApplyRole`。
- `QMessageBox::Reset`：`0x04000000`;一个“重置”按钮，定义为`ResetRole`。
- `QMessageBox::RestoreDefaults`：`0x08000000`;一个由`ResetRole`定义的“恢复默认”按钮。
- `QMessageBox::Help`：`0x01000000`;一个“帮助”按钮，定义为`HelpRole`。
- `QMessageBox::SaveAll`：`0x00001000`;一个“全部保存”按钮，定义为`AcceptRole`。
- `QMessageBox::Yes`：`0x00004000`;一个由`YesRole`定义的“是”按钮。
- `QMessageBox::YesToAll`：`0x00008000`;一个“全部是”按钮，定义为`YesRole`。
- `QMessageBox::No`：`0x00010000`;一个带有`NoRole`定义的“否”按钮。
- `QMessageBox::NoToAll`：`0x00020000`;一个“否对全部”按钮，定义为`NoRole`。
- `QMessageBox::Abort`：`0x00040000`;一个“中止”按钮，定义为`RejectRole`。
- `QMessageBox::Retry`：`0x00080000`;一个“重试”按钮，定义为`AcceptRole`。
- `QMessageBox::Ignore`：`0x00100000`;一个用`AcceptRole`定义的“忽略”按钮。
- `QMessageBox::NoButton`：`0x00000000`;一个无效按钮。
以下数值已过时：
- `QMessageBox::YesAll`：`YesToAll`;改用YesToAll。
- `QMessageBox::NoAll`：`NoToAll`;改用NoToAll。
- `QMessageBox::Default`：`0x00000100`;改用`information()`、`warning()`等`defaultButton`论元，或者叫`setDefaultButton()`。
- `QMessageBox::Escape`：`0x00000200`;改叫`setEscapeButton()`。
- `QMessageBox::FlagMask`：`0x00000300`
- `QMessageBox::ButtonMask`：`~FlagMask`
StandardButtons 类型是 QFlags 的 typedef<StandardButton>。它存储 StandardButton 值的 OR 组合。

### `detailedText : QString`

**作用与语义：**

该属性保存要显示在详细信息区域的文本。
文本将被解释为纯文本。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `detailedText()` 读取当前值；它不会修改应用状态。

### `icon : Icon`

**作用与语义：**

该属性包含消息框的图标。
消息框的图标可以用以下几个值之一来指定：
- `QMessageBox::NoIcon`
- `QMessageBox::Question`
- `QMessageBox::Information`
- `QMessageBox::Warning`
- `QMessageBox::Critical`
默认是`QMessageBox::NoIcon`。
用来显示实际图标的像素映射取决于当前的图形界面样式。你也可以通过设置图标像素映射属性来为图标设置自定义像素映射。

**如何使用：** 调用 `icon()` 读取当前值；它不会修改应用状态。

### `iconPixmap : QPixmap`

**作用与语义：**

该地产保留了当前的图标。
消息框当前使用的图标。请注意，通常很难绘制一个适合所有图形界面风格的像素地图;你可能需要为每个平台提供不同的像素地图。
默认情况下，该属性是未定义的。

**如何使用：** 调用 `iconPixmap()` 读取当前值；它不会修改应用状态。

### `informativeText : QString`

**作用与语义：**

该属性包含信息文本，提供更完整的消息描述。
信息性文本可用于扩展`text()`，向用户提供更多信息，例如描述情境的后果，或提出替代方案。
文本将根据文本格式设置（`QMessageBox::textFormat`）被解释为纯文本或富文本。默认设置为`Qt::AutoText`，即消息框会尝试自动检测文本格式。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `informativeText()` 读取当前值；它不会修改应用状态。

### `[since 6.6] options : Options`

**作用与语义：**

影响对话框外观和感觉的选项。
默认情况下，这些选项是禁用的。
选项 `Option::DontUseNativeDialog` 应在更改对话框属性或显示对话框之前设置。
在对话框可见时设置选项不保证会立即影响对话框。
在更改其他属性后设置选项可能导致这些值无效。

**如何使用：** 调用 `options()` 读取当前值；它不会修改应用状态。

### `standardButtons : StandardButtons`

**作用与语义：**

消息框中标准按钮的集合。
该属性控制消息框使用的标准按钮。
默认情况下，该属性不包含标准按钮。

**如何使用：** 调用 `standardButtons()` 读取当前值；它不会修改应用状态。

### `text : QString`

**作用与语义：**

该属性包含待显示的消息框文本。
文本应是简短的句子或短语，描述情境，理想情况下应以中立陈述或号召性问题的形式表达。
文本将根据文本格式设置（`QMessageBox::textFormat`）被解释为纯文本或富文本。默认设置是`Qt::AutoText`，即消息框会尝试自动检测文本格式。
该属性的默认值是空字符串。

**如何使用：** 调用 `text()` 读取当前值；它不会修改应用状态。

### `textFormat : Qt::TextFormat`

**作用与语义：**

该属性表示消息框显示文本的格式。
当前消息框使用的文本格式。请参阅`Qt::TextFormat`枚举，了解可能选项的说明。
默认格式是`Qt::AutoText`。

**如何使用：** 调用 `textFormat()` 读取当前值；它不会修改应用状态。

### `textInteractionFlags : Qt::TextInteractionFlags`

**作用与语义：**

指定消息框标签应如何与用户输入交互。
默认值取决于样式。

**如何使用：** 调用 `textInteractionFlags()` 读取当前值；它不会修改应用状态。

### `[explicit] QMessageBox::QMessageBox(QWidget *parent = nullptr)`

**作用与语义：**

构建一个无文本和无按钮的应用模态消息框。`parent`传递给`QDialog`构造器。
窗口模态可以通过调用`show()`前的 `setWindowModality()` 覆盖。
注意：使用`open()`或`exec()`显示消息框会影响窗口模态。请参见每个功能的详细文档以获取更多信息。
在macOS中，如果你想让消息框作为其`parent`的`Qt::Sheet`显示，可以将消息框的窗口模式设置为`Qt::WindowModal`或使用`open()`。否则，消息框将是标准对话框。

### `QMessageBox::QMessageBox(QMessageBox::Icon icon, const QString &title, const QString &text, QMessageBox::StandardButtons buttons = NoButton, QWidget *parent = nullptr, Qt::WindowFlags f = Qt::Dialog | Qt::MSWindowsFixedSizeDialogHint)`

**作用与语义：**

构建一个应用模态消息框，包含给定的`icon`、`title`、`text`和标准`buttons`。标准或自定义按钮可随时使用`addButton()`添加。`parent`和`f`参数传递给`QDialog`构造器。
窗口模态可以通过调用`show()`前的 `setWindowModality()` 覆盖。
注意：使用`open()`或`exec()`显示消息框会影响窗口模态。更多信息请参阅每个功能的详细文档。
在macOS上，如果`parent`不`nullptr`，而你希望消息框显示为该父的`Qt::Sheet`，请将消息框的窗口模式设置为`Qt::WindowModal`（默认）。否则，消息框将是标准对话框。

### `[virtual noexcept] QMessageBox::~QMessageBox()`

**作用与语义：**

摧毁了消息箱。

### `[static] void QMessageBox::about(QWidget *parent, const QString &title, const QString &text)`

**作用与语义：**

显示一个简单的关于框，带有标题`title`和文本`text`。关于的上文本框是`parent`。
about() 在四个位置寻找合适的图标：
- 如果有的话，它更喜欢`parent->icon()`。
- 如果不行，则尝试包含`parent`的顶层小部件。
- 如果失败，则尝试激活窗口。
- 作为最后手段，它使用信息图标。
关于页面只有一个标注为“确定”的按钮。
在macOS上，关于对话框弹出为无模式窗口;在其他平台上，目前为应用程序模态。

### `[static] void QMessageBox::aboutQt(QWidget *parent, const QString &title = QString())`

**作用与语义：**

显示一个关于Qt的简单消息框，给定的`title`置中，置中`parent`（如果`parent`未`nullptr`）。消息包含应用程序使用的Qt版本号。
这对于应用的帮助菜单中出现非常有用，如菜单示例所示。
`QApplication` 作为槽函数提供此功能。
在macOS上，aboutQt框以无模式窗口形式弹出;在其他平台上，它目前是应用模态。

### `void QMessageBox::addButton(QAbstractButton *button, QMessageBox::ButtonRole role)`

**作用与语义：**

将给定的`button`添加到消息框中，并带有指定的`role`。

### `QPushButton *QMessageBox::addButton(QMessageBox::StandardButton button)`

**作用与语义：**

如果有标准的，会在消息框中添加一个标准`button`，并返回按钮。

### `QPushButton *QMessageBox::addButton(const QString &text, QMessageBox::ButtonRole role)`

**作用与语义：**

创建一个带有`text`的按钮，添加到指定`role`的消息框中，然后返回。

### `QAbstractButton *QMessageBox::button(QMessageBox::StandardButton which) const`

**作用与语义：**

返回一个对应标准按钮`which`的指针，如果该按钮不存在，则返回`nullptr`。
注意：修改返回按钮的属性可能不会反映在消息对话框的本地实现中。要自定义对话框按钮，可以添加自定义按钮或按钮标题，或设置`Option::DontUseNativeDialog`选项。

### `[signal] void QMessageBox::buttonClicked(QAbstractButton *button)`

**作用与语义：**

每当`QMessageBox`内点击按钮时，该信号都会发出。按下的按钮`button`返回。

### `QMessageBox::ButtonRole QMessageBox::buttonRole(QAbstractButton *button) const`

**作用与语义：**

返回指定`button`的按钮角色。如果`button` `nullptr`或未添加到消息框中，该函数返回`InvalidRole`。

### `QList<QAbstractButton *> QMessageBox::buttons() const`

**作用与语义：**

返回所有已添加到消息框的按钮列表。

### `[override virtual protected] void QMessageBox::changeEvent(QEvent *ev)`

**作用与语义：**

重装：`QWidget::changeEvent`（QEvent *事件）。
该事件处理程序可以重新实现以处理状态变化。
该事件中被更改的状态可以通过提供的`event`检索。
变更事件包括：`QEvent::ToolBarChange`、`QEvent::ActivationChange`、`QEvent::EnabledChange`、`QEvent::FontChange`、`QEvent::StyleChange`、`QEvent::PaletteChange`、`QEvent::WindowTitleChange`、`QEvent::IconTextChange`、`QEvent::ModifiedChange`、`QEvent::MouseTrackingChange`、`QEvent::ParentChange`、`QEvent::WindowStateChange`、`QEvent::LanguageChange`、`QEvent::LocaleChange`、`QEvent::LayoutDirectionChange`、`QEvent::ReadOnlyChange`。

### `QCheckBox *QMessageBox::checkBox() const`

**作用与语义：**

返回对话框中显示的复选框。如果没有设置复选框，则`nullptr`。

### `QAbstractButton *QMessageBox::clickedButton() const`

**作用与语义：**

返回用户点击的按钮，或者如果用户按下Esc键且未设置逃脱键，则返回`nullptr`。
如果`exec()`还没被调用，则返回nullptr。

**官方示例：**

```cpp
 QMessageBox messageBox(this);
 QAbstractButton *disconnectButton =
       messageBox.addButton(tr("Disconnect"), QMessageBox::ActionRole);
 //...
 messageBox.exec();
 if (messageBox.clickedButton() == disconnectButton) {
     //...
 }
```

### `[override virtual protected] void QMessageBox::closeEvent(QCloseEvent *e)`

**作用与语义：**

重实现自：`QDialog::closeEvent`（QCloseEvent *e）。

### `[static] QMessageBox::StandardButton QMessageBox::critical(QWidget *parent, const QString &title, const QString &text, QMessageBox::StandardButtons buttons = Ok, QMessageBox::StandardButton defaultButton = NoButton)`

**作用与语义：**

在指定`parent`组件前打开一个包含指定`title`和`text`的关键消息框。
标准`buttons`会添加到消息框中。`defaultButton` 指定按下回车键时使用的按钮。`defaultButton` 必须指代 `buttons` 中给出的按钮。如果`defaultButton` `QMessageBox::NoButton`，`QMessageBox` 会自动选择合适的默认选项。
返回被点击的标准按钮的身份。如果按的是Esc键，则返回退出键。
消息框是一个应用模态对话框。
警告：在对话执行过程中请勿删除`parent`。如果你想这样做，应该用`QMessageBox`构造函数之一自己创建对话。

### `QPushButton *QMessageBox::defaultButton() const`

**作用与语义：**

返回应是消息框默认按钮的按钮。如果没有设置默认按钮，返回 nullptr。

### `QAbstractButton *QMessageBox::escapeButton() const`

**作用与语义：**

返回按下Esc键时激活的按钮。
默认情况下，`QMessageBox` 尝试自动检测逃脱按钮，具体如下：
- 如果只有一个按钮，则设为退出按钮。
- 如果有`Cancel`键，则为逃脱键。
- 仅在macOS上，如果角色`QMessageBox::RejectRole`恰好有一个按钮，则该按钮为退出键。
当逃脱键无法自动检测时，按Esc键也无效。

### `[override virtual protected] bool QMessageBox::event(QEvent *e)`

**作用与语义：**

重实现自：`QWidget::event`（QEvent *事件）。

### `[override virtual slot] int QMessageBox::exec()`

**作用与语义：**

重装：`QDialog::exec()`。
以模态对话框显示消息框，直到用户关闭为止。
使用带有标准按钮的`QMessageBox`时，该函数返回一个`StandardButton`值，表示被点击的标准按钮。使用自定义按钮的 `QMessageBox` 时，该函数返回不透明值;使用`clickedButton()`来确定被点击的按钮。
注意：`result()`函数还返回`StandardButton`值而非`QDialog::DialogCode`。
用户在关闭对话框之前，无法与同一应用程序中的任何其他窗互，无论是通过点击按钮还是使用窗口系统提供的机制。
以模态对话框显示，阻塞直到用户关闭。函数返回`DialogCode`结果。
如果对话框是应用模态的，用户在关闭对话框之前不能与同一应用中的任何其他窗互。如果对话框是窗口模态，则在对话框打开期间，只有与父窗口的交互被屏蔽。默认情况下，该对话框是应用模态的。
注意：请避免使用此函数;改用 `open()`。与 exec() 不同，`open()` 是异步的，不会旋转额外的事件循环。这防止了一系列危险的错误发生（例如在对话打开时通过 exec() 删除对话的父节点）。使用`open()`时，你可以连接到对话关闭时收到通知`QDialog`的 `finished()`信号。

### `[static] QMessageBox::StandardButton QMessageBox::information(QWidget *parent, const QString &title, const QString &text, QMessageBox::StandardButtons buttons = Ok, QMessageBox::StandardButton defaultButton = NoButton)`

**作用与语义：**

在指定的`parent`组件前打开一个信息消息框，内含给定的`title`和`text`。
标准`buttons`会添加到消息框中。`defaultButton` 指定按下回车时使用的按钮。`defaultButton` 必须指向 `buttons` 中给出的按钮。如果 `defaultButton` `QMessageBox::NoButton`，`QMessageBox` 会自动选择合适的默认选项。
返回被点击的标准按钮的身份。如果按的是Esc键，则返回退出键。
消息框是一个应用模态对话框。
警告：在对话执行过程中请勿删除`parent`。如果你想这样做，应该用`QMessageBox`构造函数之一自己创建对话。

### `[override virtual protected] void QMessageBox::keyPressEvent(QKeyEvent *e)`

**作用与语义：**

重实现自：`QDialog::keyPressEvent`（QKeyEvent *e）。

### `void QMessageBox::open(QObject *receiver, const char *member)`

**作用与语义：**

打开对话并将其`finished()`或`buttonClicked()`信号连接到`receiver`和`member`指定的槽函数。如果`member`中的槽函数有第一个参数的指针，则连接指向`buttonClicked()`，否则连接指向`finished()`。
当对话关闭时，信号会从槽函数中断开。

### `[static] QMessageBox::StandardButton QMessageBox::question(QWidget *parent, const QString &title, const QString &text, QMessageBox::StandardButtons buttons = StandardButtons(Yes | No), QMessageBox::StandardButton defaultButton = NoButton)`

**作用与语义：**

在指定`parent`组件前打开一个带有指定`title`和`text`的问题消息框。
标准`buttons`会添加到消息框中。`defaultButton` 指定按下回车键时使用的按钮。`defaultButton` 必须指向 `buttons` 中给出的按钮。如果 `defaultButton` `QMessageBox::NoButton`，`QMessageBox` 会自动选择合适的默认值。
返回被点击的标准按钮的身份。如果按的是Esc键，则返回退出键。
消息框是一个应用模态对话框。
警告：在对话执行过程中请勿删除`parent`。如果你想这样做，应该用`QMessageBox`构造函数之一自己创建对话。

### `void QMessageBox::removeButton(QAbstractButton *button)`

**作用与语义：**

可以从按钮框中移除`button`，但不会删除它。

### `[override virtual protected] void QMessageBox::resizeEvent(QResizeEvent *event)`

**作用与语义：**

重实现自：`QDialog::resizeEvent`（QResizeEvent *）。

### `void QMessageBox::setCheckBox(QCheckBox *cb)`

**作用与语义：**

在消息对话框中设置复选框`cb`。消息框拥有该复选框的所有权。参数`cb`可以`nullptr`以移除消息框中的现有复选框。

### `void QMessageBox::setDefaultButton(QMessageBox::StandardButton button)`

**作用与语义：**

将消息框的默认按钮设置为`button`。

### `void QMessageBox::setDefaultButton(QPushButton *button)`

**作用与语义：**

将消息框的默认按钮设置为`button`。

### `void QMessageBox::setEscapeButton(QAbstractButton *button)`

**作用与语义：**

设置按下Esc键时激活的按钮`button`。

### `void QMessageBox::setEscapeButton(QMessageBox::StandardButton button)`

**作用与语义：**

设置按下Esc键时激活的按钮为`button`。

### `[since 6.6] void QMessageBox::setOption(QMessageBox::Option option, bool on = true)`

**作用与语义：**

将给定`option`设置为启用，`on`为真;否则，清除给定`option`。
选项（尤其是`Option::DontUseNativeDialog`选项）应在显示对话前设置好。
在对话框可见时设置选项并不保证会立即对对话框产生影响。
更改其他属性后设置选项可能使这些值无效。

### `void QMessageBox::setWindowModality(Qt::WindowModality windowModality)`

**作用与语义：**

这个功能会`QWidget::setWindowModality()`。
将消息框的模态设置为`windowModality`。
在macOS中，如果模态设置为`Qt::WindowModal`且消息框有父文本，那么消息框将是`Qt::Sheet`，否则消息框将是标准对话框。

### `void QMessageBox::setWindowTitle(const QString &title)`

**作用与语义：**

这个功能会`QWidget::setWindowTitle()`。
将消息框标题设置为`title`。在macOS中，窗口标题被忽略（符合macOS指南的要求）。

### `[override virtual protected] void QMessageBox::showEvent(QShowEvent *e)`

**作用与语义：**

重实现自：`QDialog::showEvent`（QShowEvent *event）。

### `QMessageBox::StandardButton QMessageBox::standardButton(QAbstractButton *button) const`

**作用与语义：**

返回对应给定`button`的标准按钮枚举值，如果给定`button`不是标准按钮，则返回`NoButton`。

### `[since 6.6] bool QMessageBox::testOption(QMessageBox::Option option) const`

**作用与语义：**

如果启用给定`option`，返回 `true`;否则返回 false。

### `[static] QMessageBox::StandardButton QMessageBox::warning(QWidget *parent, const QString &title, const QString &text, QMessageBox::StandardButtons buttons = Ok, QMessageBox::StandardButton defaultButton = NoButton)`

**作用与语义：**

在指定的`parent`组件前打开一个带有指定`title`和`text`的警告消息框。
标准`buttons`会添加到消息框中。`defaultButton` 指定按下回车键时使用的按钮。`defaultButton`必须指的是`buttons`中给出的按钮。如果`defaultButton` `QMessageBox::NoButton`，`QMessageBox`会自动选择合适的默认值。
返回被点击的标准按钮的身份。如果按的是Esc键，则返回退出键。
消息框是一个应用模态对话框。
警告：在对话执行过程中请勿删除`parent`。如果你想这样做，应该自己用`QMessageBox`构造函数之一创建对话。

### `QT_REQUIRE_VERSION(int argc, char **argv, const char *version)`

**作用与语义：**

该宏可用于确保应用程序运行的是足够更新的 Qt 版本。如果您的应用依赖于某个漏洞修复版本（例如 6.1.2）中引入的特定漏洞修复，这尤其有用。
`argc`和`argv`参数分别是`main()`函数的`argc`和`argv`参数。`version`参数是一个字符串字面量，指定应用所需的Qt版本（例如，“6.1.2”）。

**官方示例：**

```cpp
 #include <QApplication>
 #include <QMessageBox>

 int main(int argc, char *argv[])
 {
     QT_REQUIRE_VERSION(argc, argv, "4.0.2")

     QApplication app(argc, argv);
     //...
     return app.exec();
 }
```

### `(since 6.6) enum class Option { DontUseNativeDialog }`

**作用与语义：**

- `QMessageBox::Option::DontUseNativeDialog`：`0x00000001`;不要使用原生消息对话框。
该枚举于Qt 6.6引入。
Options 类型是 QFlags 的 typedef<Option>。它存储 Option 值的 OR 组合。

### `flags Options`

**作用与语义：**

- `QMessageBox::Option::DontUseNativeDialog`：`0x00000001`;不要使用原生消息对话框。
该枚举于Qt 6.6引入。
Options 类型是 QFlags 的 typedef<Option>。它存储 Option 值的 OR 组合。

### `enum StandardButton { Ok, Open, Save, Cancel, Close, …, ButtonMask }`

**作用与语义：**

这些枚举描述了标准按钮的标志。每个按钮都有定义的`ButtonRole`。
- `QMessageBox::Ok`：`0x00000400`;一个“确定”按钮，定义为`AcceptRole`。
- `QMessageBox::Open`：`0x00002000`;一个“打开”按钮，定义为`AcceptRole`。
- `QMessageBox::Save`：`0x00000800`;一个“保存”按钮，定义为`AcceptRole`。
- `QMessageBox::Cancel`：`0x00400000`;一个用`RejectRole`定义的“取消”按钮。
- `QMessageBox::Close`：`0x00200000`;一个“关闭”按钮，定义为`RejectRole`。
- `QMessageBox::Discard`：`0x00800000`;根据平台不同，一个“弃掉”或“不保存”按钮，由`DestructiveRole`定义。
- `QMessageBox::Apply`：`0x02000000`;一个“应用”按钮，定义为`ApplyRole`。
- `QMessageBox::Reset`：`0x04000000`;一个“重置”按钮，定义为`ResetRole`。
- `QMessageBox::RestoreDefaults`：`0x08000000`;一个由`ResetRole`定义的“恢复默认”按钮。
- `QMessageBox::Help`：`0x01000000`;一个“帮助”按钮，定义为`HelpRole`。
- `QMessageBox::SaveAll`：`0x00001000`;一个“全部保存”按钮，定义为`AcceptRole`。
- `QMessageBox::Yes`：`0x00004000`;一个由`YesRole`定义的“是”按钮。
- `QMessageBox::YesToAll`：`0x00008000`;一个“全部是”按钮，定义为`YesRole`。
- `QMessageBox::No`：`0x00010000`;一个带有`NoRole`定义的“否”按钮。
- `QMessageBox::NoToAll`：`0x00020000`;一个“否对全部”按钮，定义为`NoRole`。
- `QMessageBox::Abort`：`0x00040000`;一个“中止”按钮，定义为`RejectRole`。
- `QMessageBox::Retry`：`0x00080000`;一个“重试”按钮，定义为`AcceptRole`。
- `QMessageBox::Ignore`：`0x00100000`;一个用`AcceptRole`定义的“忽略”按钮。
- `QMessageBox::NoButton`：`0x00000000`;一个无效按钮。
以下数值已过时：
- `QMessageBox::YesAll`：`YesToAll`;改用YesToAll。
- `QMessageBox::NoAll`：`NoToAll`;改用NoToAll。
- `QMessageBox::Default`：`0x00000100`;改用`information()`、`warning()`等`defaultButton`论元，或者叫`setDefaultButton()`。
- `QMessageBox::Escape`：`0x00000200`;改叫`setEscapeButton()`。
- `QMessageBox::FlagMask`：`0x00000300`
- `QMessageBox::ButtonMask`：`~FlagMask`
StandardButtons 类型是 QFlags 的 typedef<StandardButton>。它存储 StandardButton 值的 OR 组合。

### `flags StandardButtons`

**作用与语义：**

这些枚举描述了标准按钮的标志。每个按钮都有定义的`ButtonRole`。
- `QMessageBox::Ok`：`0x00000400`;一个“确定”按钮，定义为`AcceptRole`。
- `QMessageBox::Open`：`0x00002000`;一个“打开”按钮，定义为`AcceptRole`。
- `QMessageBox::Save`：`0x00000800`;一个“保存”按钮，定义为`AcceptRole`。
- `QMessageBox::Cancel`：`0x00400000`;一个用`RejectRole`定义的“取消”按钮。
- `QMessageBox::Close`：`0x00200000`;一个“关闭”按钮，定义为`RejectRole`。
- `QMessageBox::Discard`：`0x00800000`;根据平台不同，一个“弃掉”或“不保存”按钮，由`DestructiveRole`定义。
- `QMessageBox::Apply`：`0x02000000`;一个“应用”按钮，定义为`ApplyRole`。
- `QMessageBox::Reset`：`0x04000000`;一个“重置”按钮，定义为`ResetRole`。
- `QMessageBox::RestoreDefaults`：`0x08000000`;一个由`ResetRole`定义的“恢复默认”按钮。
- `QMessageBox::Help`：`0x01000000`;一个“帮助”按钮，定义为`HelpRole`。
- `QMessageBox::SaveAll`：`0x00001000`;一个“全部保存”按钮，定义为`AcceptRole`。
- `QMessageBox::Yes`：`0x00004000`;一个由`YesRole`定义的“是”按钮。
- `QMessageBox::YesToAll`：`0x00008000`;一个“全部是”按钮，定义为`YesRole`。
- `QMessageBox::No`：`0x00010000`;一个带有`NoRole`定义的“否”按钮。
- `QMessageBox::NoToAll`：`0x00020000`;一个“否对全部”按钮，定义为`NoRole`。
- `QMessageBox::Abort`：`0x00040000`;一个“中止”按钮，定义为`RejectRole`。
- `QMessageBox::Retry`：`0x00080000`;一个“重试”按钮，定义为`AcceptRole`。
- `QMessageBox::Ignore`：`0x00100000`;一个用`AcceptRole`定义的“忽略”按钮。
- `QMessageBox::NoButton`：`0x00000000`;一个无效按钮。
以下数值已过时：
- `QMessageBox::YesAll`：`YesToAll`;改用YesToAll。
- `QMessageBox::NoAll`：`NoToAll`;改用NoToAll。
- `QMessageBox::Default`：`0x00000100`;改用`information()`、`warning()`等`defaultButton`论元，或者叫`setDefaultButton()`。
- `QMessageBox::Escape`：`0x00000200`;改叫`setEscapeButton()`。
- `QMessageBox::FlagMask`：`0x00000300`
- `QMessageBox::ButtonMask`：`~FlagMask`
StandardButtons 类型是 QFlags 的 typedef<StandardButton>。它存储 StandardButton 值的 OR 组合。

### `QString detailedText() const`

**作用与语义：**

该属性保存要显示在详细信息区域的文本。
文本将被解释为纯文本。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `detailedText()` 读取当前值；它不会修改应用状态。

### `QMessageBox::Icon icon() const`

**作用与语义：**

该属性包含消息框的图标。
消息框的图标可以用以下几个值之一来指定：
- `QMessageBox::NoIcon`
- `QMessageBox::Question`
- `QMessageBox::Information`
- `QMessageBox::Warning`
- `QMessageBox::Critical`
默认是`QMessageBox::NoIcon`。
用来显示实际图标的像素映射取决于当前的图形界面样式。你也可以通过设置图标像素映射属性来为图标设置自定义像素映射。

**如何使用：** 调用 `icon()` 读取当前值；它不会修改应用状态。

### `QPixmap iconPixmap() const`

**作用与语义：**

该地产保留了当前的图标。
消息框当前使用的图标。请注意，通常很难绘制一个适合所有图形界面风格的像素地图;你可能需要为每个平台提供不同的像素地图。
默认情况下，该属性是未定义的。

**如何使用：** 调用 `iconPixmap()` 读取当前值；它不会修改应用状态。

### `QString informativeText() const`

**作用与语义：**

该属性包含信息文本，提供更完整的消息描述。
信息性文本可用于扩展`text()`，向用户提供更多信息，例如描述情境的后果，或提出替代方案。
文本将根据文本格式设置（`QMessageBox::textFormat`）被解释为纯文本或富文本。默认设置为`Qt::AutoText`，即消息框会尝试自动检测文本格式。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `informativeText()` 读取当前值；它不会修改应用状态。

### `QMessageBox::Options options() const`

**作用与语义：**

影响对话框外观和感觉的选项。
默认情况下，这些选项是禁用的。
选项 `Option::DontUseNativeDialog` 应在更改对话框属性或显示对话框之前设置。
在对话框可见时设置选项不保证会立即影响对话框。
在更改其他属性后设置选项可能导致这些值无效。

**如何使用：** 调用 `options()` 读取当前值；它不会修改应用状态。

### `void setDetailedText(const QString &text)`

**作用与语义：**

该属性保存要显示在详细信息区域的文本。
文本将被解释为纯文本。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `setDetailedText(...)` 修改 `detailedText`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setIcon(QMessageBox::Icon)`

**作用与语义：**

该属性包含消息框的图标。
消息框的图标可以用以下几个值之一来指定：
- `QMessageBox::NoIcon`
- `QMessageBox::Question`
- `QMessageBox::Information`
- `QMessageBox::Warning`
- `QMessageBox::Critical`
默认是`QMessageBox::NoIcon`。
用来显示实际图标的像素映射取决于当前的图形界面样式。你也可以通过设置图标像素映射属性来为图标设置自定义像素映射。

**如何使用：** 调用 `setIcon(...)` 修改 `icon`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setIconPixmap(const QPixmap &pixmap)`

**作用与语义：**

该地产保留了当前的图标。
消息框当前使用的图标。请注意，通常很难绘制一个适合所有图形界面风格的像素地图;你可能需要为每个平台提供不同的像素地图。
默认情况下，该属性是未定义的。

**如何使用：** 调用 `setIconPixmap(...)` 修改 `iconPixmap`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setInformativeText(const QString &text)`

**作用与语义：**

该属性包含信息文本，提供更完整的消息描述。
信息性文本可用于扩展`text()`，向用户提供更多信息，例如描述情境的后果，或提出替代方案。
文本将根据文本格式设置（`QMessageBox::textFormat`）被解释为纯文本或富文本。默认设置为`Qt::AutoText`，即消息框会尝试自动检测文本格式。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `setInformativeText(...)` 修改 `informativeText`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setOptions(QMessageBox::Options options)`

**作用与语义：**

影响对话框外观和感觉的选项。
默认情况下，这些选项是禁用的。
选项 `Option::DontUseNativeDialog` 应在更改对话框属性或显示对话框之前设置。
在对话框可见时设置选项不保证会立即影响对话框。
在更改其他属性后设置选项可能导致这些值无效。

**如何使用：** 调用 `setOptions(...)` 修改 `options`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setStandardButtons(QMessageBox::StandardButtons buttons)`

**作用与语义：**

消息框中标准按钮的集合。
该属性控制消息框使用的标准按钮。
默认情况下，该属性不包含标准按钮。

**如何使用：** 调用 `setStandardButtons(...)` 修改 `standardButtons`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setText(const QString &text)`

**作用与语义：**

该属性包含待显示的消息框文本。
文本应是简短的句子或短语，描述情境，理想情况下应以中立陈述或号召性问题的形式表达。
文本将根据文本格式设置（`QMessageBox::textFormat`）被解释为纯文本或富文本。默认设置是`Qt::AutoText`，即消息框会尝试自动检测文本格式。
该属性的默认值是空字符串。

**如何使用：** 调用 `setText(...)` 修改 `text`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTextFormat(Qt::TextFormat format)`

**作用与语义：**

该属性表示消息框显示文本的格式。
当前消息框使用的文本格式。请参阅`Qt::TextFormat`枚举，了解可能选项的说明。
默认格式是`Qt::AutoText`。

**如何使用：** 调用 `setTextFormat(...)` 修改 `textFormat`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTextInteractionFlags(Qt::TextInteractionFlags flags)`

**作用与语义：**

指定消息框标签应如何与用户输入交互。
默认值取决于样式。

**如何使用：** 调用 `setTextInteractionFlags(...)` 修改 `textInteractionFlags`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QMessageBox::StandardButtons standardButtons() const`

**作用与语义：**

消息框中标准按钮的集合。
该属性控制消息框使用的标准按钮。
默认情况下，该属性不包含标准按钮。

**如何使用：** 调用 `standardButtons()` 读取当前值；它不会修改应用状态。

### `QString text() const`

**作用与语义：**

该属性包含待显示的消息框文本。
文本应是简短的句子或短语，描述情境，理想情况下应以中立陈述或号召性问题的形式表达。
文本将根据文本格式设置（`QMessageBox::textFormat`）被解释为纯文本或富文本。默认设置是`Qt::AutoText`，即消息框会尝试自动检测文本格式。
该属性的默认值是空字符串。

**如何使用：** 调用 `text()` 读取当前值；它不会修改应用状态。

### `Qt::TextFormat textFormat() const`

**作用与语义：**

该属性表示消息框显示文本的格式。
当前消息框使用的文本格式。请参阅`Qt::TextFormat`枚举，了解可能选项的说明。
默认格式是`Qt::AutoText`。

**如何使用：** 调用 `textFormat()` 读取当前值；它不会修改应用状态。

### `Qt::TextInteractionFlags textInteractionFlags() const`

**作用与语义：**

指定消息框标签应如何与用户输入交互。
默认值取决于样式。

**如何使用：** 调用 `textInteractionFlags()` 读取当前值；它不会修改应用状态。

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

`QMessageBox` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
