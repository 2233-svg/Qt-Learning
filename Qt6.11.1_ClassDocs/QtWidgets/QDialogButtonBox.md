# QDialogButtonBox

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QDialogButtonBox` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QDialogButtonBox` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QDialogButtonBox>`
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

### 公有类型

- `enum ButtonLayout { WinLayout, MacLayout, KdeLayout, GnomeLayout, AndroidLayout }`
- `enum ButtonRole { InvalidRole, AcceptRole, RejectRole, DestructiveRole, ActionRole, …, ResetRole }`
- `enum StandardButton { Ok, Open, Save, Cancel, Close, …, NoButton }`
- `flags StandardButtons`

### 属性

- `centerButtons : bool`
- `orientation : Qt::Orientation`
- `standardButtons : StandardButtons`

### 公有函数

- `QDialogButtonBox(QWidget *parent = nullptr)`
- `QDialogButtonBox(QDialogButtonBox::StandardButtons buttons, QWidget *parent = nullptr)`
- `QDialogButtonBox(Qt::Orientation orientation, QWidget *parent = nullptr)`
- `QDialogButtonBox(QDialogButtonBox::StandardButtons buttons, Qt::Orientation orientation, QWidget *parent = nullptr)`
- `virtual ~QDialogButtonBox()`
- `QPushButton * addButton(QDialogButtonBox::StandardButton button)`
- `void addButton(QAbstractButton *button, QDialogButtonBox::ButtonRole role)`
- `QPushButton * addButton(const QString &text, QDialogButtonBox::ButtonRole role)`
- `QPushButton * button(QDialogButtonBox::StandardButton which) const`
- `QDialogButtonBox::ButtonRole buttonRole(QAbstractButton *button) const`
- `QList<QAbstractButton *> buttons() const`
- `bool centerButtons() const`
- `void clear()`
- `Qt::Orientation orientation() const`
- `void removeButton(QAbstractButton *button)`
- `void setCenterButtons(bool center)`
- `void setOrientation(Qt::Orientation orientation)`
- `void setStandardButtons(QDialogButtonBox::StandardButtons buttons)`
- `QDialogButtonBox::StandardButton standardButton(QAbstractButton *button) const`
- `QDialogButtonBox::StandardButtons standardButtons() const`

### 信号

- `void accepted()`
- `void clicked(QAbstractButton *button)`
- `void helpRequested()`
- `void rejected()`

### 重实现的保护函数

- `virtual void changeEvent(QEvent *event) override`
- `virtual bool event(QEvent *event) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QDialogButtonBox::ButtonLayout`

**作用与语义：**

该枚举描述了在排列按钮框中按钮时应使用的布局策略。
- `QDialogButtonBox::WinLayout`：`0`;使用适合Windows应用的策略。
- `QDialogButtonBox::MacLayout`：`1`;使用适用于macOS应用的策略。
- `QDialogButtonBox::KdeLayout`：`2`;使用适合 KDE 应用的策略。
- `QDialogButtonBox::GnomeLayout`：`3`;使用适合GNOME应用的策略。
- `QDialogButtonBox::AndroidLayout`：`4`;使用适用于Android应用的策略。该枚举值是在Qt 5.10中添加的。
按键布局由当前样式指定。但在 X11 平台上，可能会受到桌面环境的影响。

### `enum QDialogButtonBox::ButtonRole`

**作用与语义：**

这个枚举描述了可以用来描述按钮框中按钮的角色。这些角色的组合作为标志，用来描述其行为的不同方面。
- `QDialogButtonBox::InvalidRole`：`-1`;按钮无效。
- `QDialogButtonBox::AcceptRole`：`0`;点击按钮会使对话被接受（例如确定）。
- `QDialogButtonBox::RejectRole`：`1`;点击按钮会导致对话被拒绝（例如取消）。
- `QDialogButtonBox::DestructiveRole`：`2`;点击按钮会造成破坏性变化（例如丢弃更改），并关闭对话框。
- `QDialogButtonBox::ActionRole`：`3`;点击按钮会改变对话框中的元素。
- `QDialogButtonBox::HelpRole`：`4`;按钮可点击请求帮助。
- `QDialogButtonBox::YesRole`：`5`;按钮类似“是”。
- `QDialogButtonBox::NoRole`：`6`;按钮是类似“否”按钮。
- `QDialogButtonBox::ApplyRole`：`8`;按钮应用当前变化。
- `QDialogButtonBox::ResetRole`：`7`;按钮将对话框字段重置为默认值。

### `enum QDialogButtonBox::StandardButtonflags QDialogButtonBox::StandardButtons`

**作用与语义：**

这些枚举描述了标准按钮的标志。每个按钮都有定义的`ButtonRole`。
- `QDialogButtonBox::Ok`：`0x00000400`;一个“OK”按钮，定义为`AcceptRole`。
- `QDialogButtonBox::Open`：`0x00002000`;一个“打开”按钮，定义为`AcceptRole`。
- `QDialogButtonBox::Save`：`0x00000800`;一个“保存”按钮，定义为`AcceptRole`。
- `QDialogButtonBox::Cancel`：`0x00400000`;一个“取消”按钮，定义为`RejectRole`。
- `QDialogButtonBox::Close`：`0x00200000`;一个“关闭”按钮，定义为`RejectRole`。
- `QDialogButtonBox::Discard`：`0x00800000`;根据平台不同，`DestructiveRole`定义为“弃牌”或“不保存”按钮。
- `QDialogButtonBox::Apply`：`0x02000000`;一个“应用”按钮，定义为`ApplyRole`。
- `QDialogButtonBox::Reset`：`0x04000000`;一个“重置”按钮，定义为`ResetRole`。
- `QDialogButtonBox::RestoreDefaults`：`0x08000000`;一个由`ResetRole`定义的“恢复默认值”按钮。
- `QDialogButtonBox::Help`：`0x01000000`;一个“帮助”按钮，定义为`HelpRole`。
- `QDialogButtonBox::SaveAll`：`0x00001000`;一个“全部保存”按钮，定义为`AcceptRole`。
- `QDialogButtonBox::Yes`：`0x00004000`;一个“是”按钮，定义为`YesRole`。
- `QDialogButtonBox::YesToAll`：`0x00008000`;一个“对全部”按钮，定义为`YesRole`。
- `QDialogButtonBox::No`：`0x00010000`;一个带有`NoRole`定义的“否”按钮。
- `QDialogButtonBox::NoToAll`：`0x00020000`;一个“否对全部”按钮，定义为`NoRole`。
- `QDialogButtonBox::Abort`：`0x00040000`;一个“中止”按钮，定义为`RejectRole`。
- `QDialogButtonBox::Retry`：`0x00080000`;一个用`AcceptRole`定义的“重试”按钮。
- `QDialogButtonBox::Ignore`：`0x00100000`;一个用`AcceptRole`定义的“忽略”按钮。
- `QDialogButtonBox::NoButton`：`0x00000000`;一个无效按钮。
StandardButtons 类型是 QFlags 的 typedef<StandardButton>。它存储 StandardButton 值的 OR 组合。

### `centerButtons : bool`

**作用与语义：**

该属性决定按钮框内的按钮是否居中。
默认情况下，该属性为`false`。这种行为适用于大多数类型的对话。一个显著的例外是大多数平台（如Windows）的消息框，按钮框水平置中。

**如何使用：** 调用 `centerButtons()` 读取当前值；它不会修改应用状态。

### `orientation : Qt::Orientation`

**作用与语义：**

该属性决定了按钮盒的方向。
默认方向是水平的（即按钮并排排列）。可能的方向有`Qt::Horizontal`和有`Qt::Vertical`。

**如何使用：** 调用 `orientation()` 读取当前值；它不会修改应用状态。

### `standardButtons : StandardButtons`

**作用与语义：**

按钮盒中的标准按钮集合。
该属性控制按钮盒使用哪些标准按钮。

**如何使用：** 调用 `standardButtons()` 读取当前值；它不会修改应用状态。

### `QDialogButtonBox::QDialogButtonBox(QWidget *parent = nullptr)`

**作用与语义：**

用给定的`parent`构造一个空的水平按钮框。

### `[explicit] QDialogButtonBox::QDialogButtonBox(QDialogButtonBox::StandardButtons buttons, QWidget *parent = nullptr)`

**作用与语义：**

构建一个水平按钮盒，包含`buttons`指定的标准按钮`parent`。

### `QDialogButtonBox::QDialogButtonBox(Qt::Orientation orientation, QWidget *parent = nullptr)`

**作用与语义：**

构建一个空按钮框，包含给定的`orientation`和`parent`。

### `QDialogButtonBox::QDialogButtonBox(QDialogButtonBox::StandardButtons buttons, Qt::Orientation orientation, QWidget *parent = nullptr)`

**作用与语义：**

构建一个带有`orientation`和`parent`的按钮框，包含`buttons`指定的标准按钮。

### `[virtual noexcept] QDialogButtonBox::~QDialogButtonBox()`

**作用与语义：**

能摧毁按钮盒。

### `[signal] void QDialogButtonBox::accepted()`

**作用与语义：**

当按钮框内的按钮被点击时，只要该按钮是用`AcceptRole`或`YesRole`定义的，就会发出该信号。

### `QPushButton *QDialogButtonBox::addButton(QDialogButtonBox::StandardButton button)`

**作用与语义：**

如果按钮框有效，会添加一个标准`button`，并返回一个按键。如果`button`无效，则不添加到按钮框中，返回零。

### `void QDialogButtonBox::addButton(QAbstractButton *button, QDialogButtonBox::ButtonRole role)`

**作用与语义：**

将给定的`button`添加到按钮框中，并附有指定的`role`。如果角色无效，按钮不会被添加。
如果按钮已经被添加，则会移除并重新添加新角色。
注意：按钮盒对按钮拥有所有权。

### `QPushButton *QDialogButtonBox::addButton(const QString &text, QDialogButtonBox::ButtonRole role)`

**作用与语义：**

用给定`text`创建一个按钮，添加到指定`role`的按钮框中，返回相应的按钮。如果`role`无效，则不生成按钮，返回零。

### `QPushButton *QDialogButtonBox::button(QDialogButtonBox::StandardButton which) const`

**作用与语义：**

返回对应标准按钮`which`的`QPushButton`，如果该按钮盒中没有标准按钮，则返回`nullptr`。

### `QDialogButtonBox::ButtonRole QDialogButtonBox::buttonRole(QAbstractButton *button) const`

**作用与语义：**

返回指定`button`的按钮角色。如果`button` `nullptr`或未添加到按钮框中，该函数返回`InvalidRole`。

### `QList<QAbstractButton *> QDialogButtonBox::buttons() const`

**作用与语义：**

返回所有已添加到按钮框中的按钮列表。

### `[override virtual protected] void QDialogButtonBox::changeEvent(QEvent *event)`

**作用与语义：**

重装：`QWidget::changeEvent`（QEvent *事件）。
该事件处理程序可以重新实现以处理状态变化。
该事件中被更改的状态可以通过提供的`event`检索。
变更事件包括：`QEvent::ToolBarChange`、`QEvent::ActivationChange`、`QEvent::EnabledChange`、`QEvent::FontChange`、`QEvent::StyleChange`、`QEvent::PaletteChange`、`QEvent::WindowTitleChange`、`QEvent::IconTextChange`、`QEvent::ModifiedChange`、`QEvent::MouseTrackingChange`、`QEvent::ParentChange`、`QEvent::WindowStateChange`、`QEvent::LanguageChange`、`QEvent::LocaleChange`、`QEvent::LayoutDirectionChange`、`QEvent::ReadOnlyChange`。

### `void QDialogButtonBox::clear()`

**作用与语义：**

清除按钮框，删除其中的所有按钮。

### `[signal] void QDialogButtonBox::clicked(QAbstractButton *button)`

**作用与语义：**

当按钮盒内的按钮被点击时，该信号会发出。具体按下的按钮由`button`指定。

### `[override virtual protected] bool QDialogButtonBox::event(QEvent *event)`

**作用与语义：**

重实现自：`QWidget::event`（QEvent *事件）。

### `[signal] void QDialogButtonBox::helpRequested()`

**作用与语义：**

只要按钮框内的按钮被点击，只要该按钮是用`HelpRole`定义的，就会发出该信号。

### `[signal] void QDialogButtonBox::rejected()`

**作用与语义：**

只要按钮框内的按钮被按下，只要该按钮用`RejectRole`或`NoRole`定义，就会发出该信号。

### `void QDialogButtonBox::removeButton(QAbstractButton *button)`

**作用与语义：**

从按钮框中移除`button`，但不删除它，并将其父节点设为零。

### `QDialogButtonBox::StandardButton QDialogButtonBox::standardButton(QAbstractButton *button) const`

**作用与语义：**

返回对应给定`button`的标准按钮枚举值，如果给定`button`不是标准按钮，则返回`NoButton`。

### `enum StandardButton { Ok, Open, Save, Cancel, Close, …, NoButton }`

**作用与语义：**

这些枚举描述了标准按钮的标志。每个按钮都有定义的`ButtonRole`。
- `QDialogButtonBox::Ok`：`0x00000400`;一个“OK”按钮，定义为`AcceptRole`。
- `QDialogButtonBox::Open`：`0x00002000`;一个“打开”按钮，定义为`AcceptRole`。
- `QDialogButtonBox::Save`：`0x00000800`;一个“保存”按钮，定义为`AcceptRole`。
- `QDialogButtonBox::Cancel`：`0x00400000`;一个“取消”按钮，定义为`RejectRole`。
- `QDialogButtonBox::Close`：`0x00200000`;一个“关闭”按钮，定义为`RejectRole`。
- `QDialogButtonBox::Discard`：`0x00800000`;根据平台不同，`DestructiveRole`定义为“弃牌”或“不保存”按钮。
- `QDialogButtonBox::Apply`：`0x02000000`;一个“应用”按钮，定义为`ApplyRole`。
- `QDialogButtonBox::Reset`：`0x04000000`;一个“重置”按钮，定义为`ResetRole`。
- `QDialogButtonBox::RestoreDefaults`：`0x08000000`;一个由`ResetRole`定义的“恢复默认值”按钮。
- `QDialogButtonBox::Help`：`0x01000000`;一个“帮助”按钮，定义为`HelpRole`。
- `QDialogButtonBox::SaveAll`：`0x00001000`;一个“全部保存”按钮，定义为`AcceptRole`。
- `QDialogButtonBox::Yes`：`0x00004000`;一个“是”按钮，定义为`YesRole`。
- `QDialogButtonBox::YesToAll`：`0x00008000`;一个“对全部”按钮，定义为`YesRole`。
- `QDialogButtonBox::No`：`0x00010000`;一个带有`NoRole`定义的“否”按钮。
- `QDialogButtonBox::NoToAll`：`0x00020000`;一个“否对全部”按钮，定义为`NoRole`。
- `QDialogButtonBox::Abort`：`0x00040000`;一个“中止”按钮，定义为`RejectRole`。
- `QDialogButtonBox::Retry`：`0x00080000`;一个用`AcceptRole`定义的“重试”按钮。
- `QDialogButtonBox::Ignore`：`0x00100000`;一个用`AcceptRole`定义的“忽略”按钮。
- `QDialogButtonBox::NoButton`：`0x00000000`;一个无效按钮。
StandardButtons 类型是 QFlags 的 typedef<StandardButton>。它存储 StandardButton 值的 OR 组合。

### `flags StandardButtons`

**作用与语义：**

这些枚举描述了标准按钮的标志。每个按钮都有定义的`ButtonRole`。
- `QDialogButtonBox::Ok`：`0x00000400`;一个“OK”按钮，定义为`AcceptRole`。
- `QDialogButtonBox::Open`：`0x00002000`;一个“打开”按钮，定义为`AcceptRole`。
- `QDialogButtonBox::Save`：`0x00000800`;一个“保存”按钮，定义为`AcceptRole`。
- `QDialogButtonBox::Cancel`：`0x00400000`;一个“取消”按钮，定义为`RejectRole`。
- `QDialogButtonBox::Close`：`0x00200000`;一个“关闭”按钮，定义为`RejectRole`。
- `QDialogButtonBox::Discard`：`0x00800000`;根据平台不同，`DestructiveRole`定义为“弃牌”或“不保存”按钮。
- `QDialogButtonBox::Apply`：`0x02000000`;一个“应用”按钮，定义为`ApplyRole`。
- `QDialogButtonBox::Reset`：`0x04000000`;一个“重置”按钮，定义为`ResetRole`。
- `QDialogButtonBox::RestoreDefaults`：`0x08000000`;一个由`ResetRole`定义的“恢复默认值”按钮。
- `QDialogButtonBox::Help`：`0x01000000`;一个“帮助”按钮，定义为`HelpRole`。
- `QDialogButtonBox::SaveAll`：`0x00001000`;一个“全部保存”按钮，定义为`AcceptRole`。
- `QDialogButtonBox::Yes`：`0x00004000`;一个“是”按钮，定义为`YesRole`。
- `QDialogButtonBox::YesToAll`：`0x00008000`;一个“对全部”按钮，定义为`YesRole`。
- `QDialogButtonBox::No`：`0x00010000`;一个带有`NoRole`定义的“否”按钮。
- `QDialogButtonBox::NoToAll`：`0x00020000`;一个“否对全部”按钮，定义为`NoRole`。
- `QDialogButtonBox::Abort`：`0x00040000`;一个“中止”按钮，定义为`RejectRole`。
- `QDialogButtonBox::Retry`：`0x00080000`;一个用`AcceptRole`定义的“重试”按钮。
- `QDialogButtonBox::Ignore`：`0x00100000`;一个用`AcceptRole`定义的“忽略”按钮。
- `QDialogButtonBox::NoButton`：`0x00000000`;一个无效按钮。
StandardButtons 类型是 QFlags 的 typedef<StandardButton>。它存储 StandardButton 值的 OR 组合。

### `bool centerButtons() const`

**作用与语义：**

该属性决定按钮框内的按钮是否居中。
默认情况下，该属性为`false`。这种行为适用于大多数类型的对话。一个显著的例外是大多数平台（如Windows）的消息框，按钮框水平置中。

**如何使用：** 调用 `centerButtons()` 读取当前值；它不会修改应用状态。

### `Qt::Orientation orientation() const`

**作用与语义：**

该属性决定了按钮盒的方向。
默认方向是水平的（即按钮并排排列）。可能的方向有`Qt::Horizontal`和有`Qt::Vertical`。

**如何使用：** 调用 `orientation()` 读取当前值；它不会修改应用状态。

### `void setCenterButtons(bool center)`

**作用与语义：**

该属性决定按钮框内的按钮是否居中。
默认情况下，该属性为`false`。这种行为适用于大多数类型的对话。一个显著的例外是大多数平台（如Windows）的消息框，按钮框水平置中。

**如何使用：** 调用 `setCenterButtons(...)` 修改 `centerButtons`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setOrientation(Qt::Orientation orientation)`

**作用与语义：**

该属性决定了按钮盒的方向。
默认方向是水平的（即按钮并排排列）。可能的方向有`Qt::Horizontal`和有`Qt::Vertical`。

**如何使用：** 调用 `setOrientation(...)` 修改 `orientation`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setStandardButtons(QDialogButtonBox::StandardButtons buttons)`

**作用与语义：**

按钮盒中的标准按钮集合。
该属性控制按钮盒使用哪些标准按钮。

**如何使用：** 调用 `setStandardButtons(...)` 修改 `standardButtons`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QDialogButtonBox::StandardButtons standardButtons() const`

**作用与语义：**

按钮盒中的标准按钮集合。
该属性控制按钮盒使用哪些标准按钮。

**如何使用：** 调用 `standardButtons()` 读取当前值；它不会修改应用状态。

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

`QDialogButtonBox` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
