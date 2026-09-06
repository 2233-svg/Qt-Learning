# QAction

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QAction` 是 Qt 对象机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QAction` 是 Qt 对象机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

**适用场景：** 使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

## 2. 依赖与对象关系

- 头文件：`#include <QAction>`
- 继承自：QObject
- 直接派生类：QWidgetAction

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

### 状态、生命周期和线程

**生命周期：** 先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

**状态与结果：** QObject 派生对象的状态通常通过属性、状态查询函数和信号变化共同表达。信号是通知，不是返回值；收到通知后应读取当前状态并处理异常路径，不能假设每个信号只会出现一次。

**线程与事件循环：** QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

## 3. 直接使用

使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum ActionEvent { Trigger, Hover }`
- `enum MenuRole { NoRole, TextHeuristicRole, ApplicationSpecificRole, AboutQtRole, AboutRole, …, QuitRole }`
- `enum Priority { LowPriority, NormalPriority, HighPriority }`

### 属性

- `autoRepeat : bool`
- `checkable : bool`
- `checked : bool`
- `enabled : bool`
- `font : QFont`
- `icon : QIcon`
- `iconText : QString`
- `iconVisibleInMenu : bool`
- `menuRole : MenuRole`
- `priority : Priority`
- `shortcut : QKeySequence`
- `shortcutContext : Qt::ShortcutContext`
- `shortcutVisibleInContextMenu : bool`
- `statusTip : QString`
- `text : QString`
- `toolTip : QString`
- `visible : bool`
- `whatsThis : QString`

### 公有函数

- `QAction(QObject *parent = nullptr)`
- `QAction(const QString &text, QObject *parent = nullptr)`
- `QAction(const QIcon &icon, const QString &text, QObject *parent = nullptr)`
- `virtual ~QAction()`
- `QActionGroup * actionGroup() const`
- `void activate(QAction::ActionEvent event)`
- `(since 6.0) QList<QObject *> associatedObjects() const`
- `bool autoRepeat() const`
- `QVariant data() const`
- `QFont font() const`
- `QIcon icon() const`
- `QString iconText() const`
- `bool isCheckable() const`
- `bool isChecked() const`
- `bool isEnabled() const`
- `bool isIconVisibleInMenu() const`
- `bool isSeparator() const`
- `bool isShortcutVisibleInContextMenu() const`
- `bool isVisible() const`
- `QMenu * menu() const`
- `QAction::MenuRole menuRole() const`
- `QAction::Priority priority() const`
- `void setActionGroup(QActionGroup *group)`
- `void setAutoRepeat(bool)`
- `void setCheckable(bool)`
- `void setData(const QVariant &data)`
- `void setFont(const QFont &font)`
- `void setIcon(const QIcon &icon)`
- `void setIconText(const QString &text)`
- `void setIconVisibleInMenu(bool visible)`
- `void setMenu(QMenu *menu)`
- `void setMenuRole(QAction::MenuRole menuRole)`
- `void setPriority(QAction::Priority priority)`
- `void setSeparator(bool b)`
- `void setShortcut(const QKeySequence &shortcut)`
- `void setShortcutContext(Qt::ShortcutContext context)`
- `void setShortcutVisibleInContextMenu(bool show)`
- `void setShortcuts(QKeySequence::StandardKey key)`
- `void setShortcuts(const QList<QKeySequence> &shortcuts)`
- `void setStatusTip(const QString &statusTip)`
- `void setText(const QString &text)`
- `void setToolTip(const QString &tip)`
- `void setWhatsThis(const QString &what)`
- `QKeySequence shortcut() const`
- `Qt::ShortcutContext shortcutContext() const`
- `QList<QKeySequence> shortcuts() const`
- `bool showStatusText(QObject *object = nullptr)`
- `QString statusTip() const`
- `QString text() const`
- `QString toolTip() const`
- `QString whatsThis() const`

### 公有槽函数

- `void hover()`
- `void resetEnabled()`
- `void setChecked(bool)`
- `void setDisabled(bool b)`
- `void setEnabled(bool)`
- `void setVisible(bool)`
- `void toggle()`
- `void trigger()`

### 信号

- `void changed()`
- `void checkableChanged(bool checkable)`
- `void enabledChanged(bool enabled)`
- `void hovered()`
- `void toggled(bool checked)`
- `void triggered(bool checked = false)`
- `void visibleChanged()`

### 重实现的保护函数

- `virtual bool event(QEvent *e) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QAction::ActionEvent`

**作用与语义：**

这种枚举类型用于调用`QAction::activate()`。
- `QAction::Trigger`：`0`;这将使`QAction::triggered()`信号被发射。
- `QAction::Hover`：`1`;这将使`QAction::hovered()`信号被发射。

### `enum QAction::MenuRole`

**作用与语义：**

这个枚举描述了如何在macOS中将某个动作移动到应用程序菜单。
- `QAction::NoRole`：`0`;此操作不应置于应用菜单中
- `QAction::TextHeuristicRole`：`1`;该操作应根据`QMenuBar`文档中描述的动作文本，在应用菜单中设置。
- `QAction::ApplicationSpecificRole`：`2`;该操作应放置在应用程序菜单中，并指定应用特定角色
- `QAction::AboutQtRole`：`3`;此操作处理“关于Qt”菜单项。
- `QAction::AboutRole`：`4`;该操作应放置在应用菜单中“关于”菜单项的位置。菜单项的文本将设置为“关于<应用程序名称>”。应用程序名称从应用包中的`Info.plist`文件中获取（参见macOS的Qt部署）。
- `QAction::PreferencesRole`：`5`;此操作应放置在“偏好设置......”菜单项所在的应用菜单中。
- `QAction::QuitRole`：`6`;该操作应放置在应用菜单中退出菜单项所在的位置。
设置这个值只会影响菜单栏直接菜单中的项目，而不会影响菜单的子菜单。例如，如果你在菜单栏里有文件菜单，而文件菜单有子菜单，那么为该子菜单中的操作设置MenuRole就没有影响。它们永远不会被移动。

### `enum QAction::Priority`

**作用与语义：**

该枚举定义了用户界面中操作的优先级。
- `QAction::LowPriority`: `0`；该操作在用户界面中不应被优先处理。
- `QAction::NormalPriority`: `128`
- `QAction::HighPriority`: `256`；该操作在用户界面中应被优先处理。

### `autoRepeat : bool`

**作用与语义：**

该属性是否能自动重复作用。
如果为真，只要系统启用键盘自动重复，按住快捷键组合时该动作会自动重复。默认值为 true。

**如何使用：** 调用 `autoRepeat()` 读取当前值；它不会修改应用状态。

### `checkable : bool`

**作用与语义：**

该属性是否确定该动作是否为可检验动作。
可检查动作是指具有开/关状态的动作。例如，在文字处理器中，加粗工具栏按钮可以是开或关。不是切换操作的动作是命令动作;命令动作则是简单执行的，例如文件保存。默认情况下，该属性是`false`的。
在某些情况下，一个切换动作的状态应依赖于其他操作的状态。例如，“左对齐”、“中心”和“右对齐”切换动作是互斥的。要实现排他切换，将相关的切换动作添加到一个`QActionGroup`中，并将 QActionGroup：：exclusive 属性设置为 true。

**如何使用：** 调用 `checkable()` 读取当前值；它不会修改应用状态。

### `checked : bool`

**作用与语义：**

该属性决定动作是否被检查。
只能检查可检查的动作。默认情况下，这个操作是假的（该动作未被勾选）。
注意：该属性的通知信号是`toggled()`。由于切换`QAction`改变了状态，它也会发出`changed()`信号。

**如何使用：** 调用 `checked()` 读取当前值；它不会修改应用状态。

### `enabled : bool`

**作用与语义：**

该属性在动作是否被启用时成立。
禁用动作不能被用户选择。它们不会从菜单或工具栏中消失，但显示方式显示为不可用。例如，它们可能仅用灰色调显示。
这是什么？只要`QAction::whatsThis`属性已设置，残障操作帮助仍然可用。
当所有添加该动作的小部件（带有`QWidget::addAction()`）都被禁用或不可见时，该动作将被禁用。当动作被禁用时，无法通过快捷方式触发该动作。
默认情况下，该属性为`true`（动作已启用）。

**如何使用：** 调用 `enabled()` 读取当前值；它不会修改应用状态。

### `font : QFont`

**作用与语义：**

该属性包含动作的字体。
字体属性用于渲染`QAction`上的文本集。字体可以被视为提示，因为根据应用和风格，字体并非所有情况下都会被参考。
默认情况下，该属性包含应用程序的默认字体。

**如何使用：** 调用 `font()` 读取当前值；它不会修改应用状态。

### `icon : QIcon`

**作用与语义：**

该属性包含动作图标。
在工具栏中，图标作为工具按钮图标使用;在菜单中，只要`QAction::iconVisibleInMenu`返回`true`，图标会显示在菜单文本的左侧。
没有默认图标。
如果将空图标（`QIcon::isNull()`）传递到该函数中，该动作图标将被清除。

**如何使用：** 调用 `icon()` 读取当前值；它不会修改应用状态。

### `iconText : QString`

**作用与语义：**

该属性包含动作的描述性图标文本。
如果`QToolBar::toolButtonStyle`设置为允许显示文本的值，则该属性中定义的文本会以标签形式出现在相关工具按钮中。
如果动作未用`setText()`或`setToolTip()`定义，它也会作为菜单和工具提示的默认文本;如果没有用`setIcon()`定义图标，它也会被用于工具栏按钮。
如果图标文本未被显式设置，则使用该动作的正常文本作为图标文本。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `iconText()` 读取当前值；它不会修改应用状态。

### `iconVisibleInMenu : bool`

**作用与语义：**

该属性决定了动作是否应在菜单中显示图标。
在某些应用中，工具栏中出现带图标的动作而菜单中不显示是合理的。如果为真，图标（如果有效）会在菜单中显示;如果为假，则不会显示。
默认情况下，是否为该应用设置了`Qt::AA_DontShowIconsInMenus`属性。显式设置该属性覆盖属性的存在（或缺失）。

**如何使用：** 调用 `iconVisibleInMenu()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 QApplication app(argc, argv);
 app.setAttribute(Qt::AA_DontShowIconsInMenus);  // Icons are *no longer shown* in menus
 // ...
 QAction *myAction = new QAction();
 // ...
 myAction->setIcon(SomeIcon);
 myAction->setIconVisibleInMenu(true);   // Icon *will* be shown in menus for *this* action.
```

### `menuRole : MenuRole`

**作用与语义：**

该属性承担动作菜单的角色。
这表示该动作在macOS应用菜单中的作用。默认情况下，所有动作都有`TextHeuristicRole`，这意味着该动作是根据文本添加的（更多信息请参见`QMenuBar`）。
菜单角色只能在 macOS 中将操作放入菜单栏之前更改（通常在第一个应用窗口显示之前）。

**如何使用：** 调用 `menuRole()` 读取当前值；它不会修改应用状态。

### `priority : Priority`

**作用与语义：**

该属性在用户界面中保持动作的优先级。
该属性可以设置为用户界面中指示动作应如何优先排序。
例如，当工具栏设置了`Qt::ToolButtonTextBesideIcon`模式时，带有`LowPriority`的动作不会显示文本标签。

**如何使用：** 调用 `priority()` 读取当前值；它不会修改应用状态。

### `shortcut : QKeySequence`

**作用与语义：**

该属性包含动作的主要快捷键。
该属性的有效键码可在`Qt::Key`和`Qt::Modifier`中找到。没有默认快捷键。

**如何使用：** 调用 `shortcut()` 读取当前值；它不会修改应用状态。

### `shortcutContext : Qt::ShortcutContext`

**作用与语义：**

该属性为动作的快捷方式提供了上下文。
该属性的有效值可在`Qt::ShortcutContext`中找到。默认值为`Qt::WindowShortcut`。

**如何使用：** 调用 `shortcutContext()` 读取当前值；它不会修改应用状态。

### `shortcutVisibleInContextMenu : bool`

**作用与语义：**

该属性决定了动作是否应在上下文菜单中显示快捷方式。
在某些应用中，在上下文菜单中设置带有快捷方式的动作可能是合理的。如果为真，则在通过上下文菜单显示动作时（如果有效）会显示该快捷方式;如果为假，则不会显示。
默认情况下，会根据`Qt::AA_DontShowShortcutsInContextMenus`属性是否为应用程序设置。显式设置该属性会覆盖该属性。

**如何使用：** 调用 `shortcutVisibleInContextMenu()` 读取当前值；它不会修改应用状态。

### `statusTip : QString`

**作用与语义：**

该属性包含动作的状态提示。
状态提示会显示在动作顶层父控件提供的所有状态栏上。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `statusTip()` 读取当前值；它不会修改应用状态。

### `text : QString`

**作用与语义：**

该属性包含动作的描述文本。
如果动作被添加到菜单中，菜单选项将由图标（如果有）、文本和快捷方式（如果有）组成。如果文本未在构造函数中明确设置，或使用 setText()，则动作的描述图标文本将被用作文本。没有默认文本。
某些界面元素，如菜单或按钮，可以在字符前使用“&”，自动为该字符创建助记法（快捷方式）。例如，菜单中的“&File”会创建快捷键Alt F，打开文件菜单。“E&xit”会创建快捷键Alt X作为按钮，或者在菜单中允许通过按“x”导航到菜单项。（使用“&”来显示实际的&符号）。小部件可能会对某个快捷方式进行消费和执行动作。

**如何使用：** 调用 `text()` 读取当前值；它不会修改应用状态。

### `toolTip : QString`

**作用与语义：**

该属性包含动作的工具提示。
此文本用于提示。若未指定提示，则使用动作文本。
默认情况下，该属性包含动作的文本。

**如何使用：** 调用 `toolTip()` 读取当前值；它不会修改应用状态。

### `visible : bool`

**作用与语义：**

该属性决定动作是否可见（例如在菜单和工具栏中）。
如果 为真，操作可以被看到（例如在菜单和工具栏中），并由用户选择;如果为 false，则用户无法看到或选择该动作。
不可见的动作不会被灰化;它们根本不会出现。
默认情况下，该属性为`true`（动作可见）。

**如何使用：** 调用 `visible()` 读取当前值；它不会修改应用状态。

### `whatsThis : QString`

**作用与语义：**

该属性包含动作的“这是什么？”帮助文本。
“这是什么？”文本用于简要描述动作。文本可能包含富文本。没有默认的“这是什么？”文本。

**如何使用：** 调用 `whatsThis()` 读取当前值；它不会修改应用状态。

### `[explicit] QAction::QAction(QObject *parent = nullptr)`

**作用与语义：**

构造一个动作，`parent`。如果`parent`是动作组，该动作将自动插入该组中。
注意：`parent`论证自第5.7问卷起为可选。

### `[explicit] QAction::QAction(const QString &text, QObject *parent = nullptr)`

**作用与语义：**

构造一个带有`text`和`parent`的动作。如果`parent`是动作组，动作会自动插入到该组中。
简化版的 `text`（例如，“& 菜单选项......”变成“菜单选项”）将用于工具提示和图标文本，除非你分别用 `setToolTip()` 或 `setIconText()` 指定不同的文本。

### `[explicit] QAction::QAction(const QIcon &icon, const QString &text, QObject *parent = nullptr)`

**作用与语义：**

构造一个动作，包含一个`icon`和一些`text`和`parent`。如果`parent`是动作组，该动作会自动插入到该组中。
简化版的`text`（例如，“&Menu Option...”变成“菜单选项”）将用于工具提示和图标文本，除非你分别用`setToolTip()`或`setIconText()`指定不同的文本。

### `[virtual noexcept] QAction::~QAction()`

**作用与语义：**

摧毁该物体并释放分配的资源。

### `QActionGroup *QAction::actionGroup() const`

**作用与语义：**

返回该动作的动作组。如果没有动作组管理该动作，则返回`nullptr`。

### `void QAction::activate(QAction::ActionEvent event)`

**作用与语义：**

发送相关信号供`ActionEvent` `event`。
基于动作的小部件使用该 API，使`QAction`发出信号，同时发出自己的信号。

### `[since 6.0] QList<QObject *> QAction::associatedObjects() const`

**作用与语义：**

返回该动作被添加的对象列表。

### `[signal] void QAction::changed()`

**作用与语义：**

该属性是否能自动重复作用。
如果为真，只要系统启用键盘自动重复，按住快捷键组合时该动作会自动重复。默认值为 true。

**如何使用：** 调用 `changed()` 读取当前值；它不会修改应用状态。

### `QVariant QAction::data() const`

**作用与语义：**

返回`QAction::setData`中设定的用户数据。

### `[override virtual protected] bool QAction::event(QEvent *e)`

**作用与语义：**

重实现自：`QObject::event`（QEvent *e）。

### `[slot] void QAction::hover()`

**作用与语义：**

这是一个方便的老虎机，可以调用激活（悬停）。

### `[signal] void QAction::hovered()`

**作用与语义：**

当用户高亮某个动作时，会发出该信号;例如，当用户在菜单选项、工具栏按钮上暂停鼠标，或按下动作快捷键组合时。

### `bool QAction::isSeparator() const`

**作用与语义：**

如果该动作是分隔符动作，返回`true`;否则返回`false`。

### `QMenu *QAction::menu() const`

**作用与语义：**

返回由此操作包含的菜单。
在控件应用中，包含菜单的动作可以用来创建带有子菜单的菜单项，或插入工具栏以创建带有弹出菜单的按钮。

### `void QAction::setActionGroup(QActionGroup *group)`

**作用与语义：**

将该动作组设置为`group`。该动作会自动添加到组的动作列表中。
群体内部的行动将相互排斥。

### `void QAction::setData(const QVariant &data)`

**作用与语义：**

将动作的内部数据设置为给定的`data`。

### `[slot] void QAction::setDisabled(bool b)`

**作用与语义：**

这是`enabled`属性的一个便利函数，对信号-槽连接非常有用。如果`b`为真，则该动作被禁用;否则该动作被启用。

### `void QAction::setMenu(QMenu *menu)`

**作用与语义：**

将该动作包含的菜单设置为指定的`menu`。

### `void QAction::setSeparator(bool b)`

**作用与语义：**

如果`b`成立，则该动作将被视为分离子。
分隔符的表示方式取决于它插入到的控件。在大多数情况下，文本、子菜单和图标在分隔符操作时会被忽略。

### `void QAction::setShortcut(const QKeySequence &shortcut)`

**作用与语义：**

该属性包含动作的主要快捷键。
该属性的有效键码可在`Qt::Key`和`Qt::Modifier`中找到。没有默认快捷键。

**如何使用：** 调用 `setShortcut(...)` 修改 `shortcut`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QAction::setShortcuts(QKeySequence::StandardKey key)`

**作用与语义：**

根据`key`设置一个平台相关的快捷方式列表。调用该函数的结果取决于当前运行的平台。注意，该动作可以分配多个快捷方式。如果只需要主快捷方式，则使用`setShortcut`。

### `void QAction::setShortcuts(const QList<QKeySequence> &shortcuts)`

**作用与语义：**

将`shortcuts`设置为触发动作的快捷方式列表。列表的第一个元素是主要快捷方式。

### `QKeySequence QAction::shortcut() const`

**作用与语义：**

返回主要快捷方式。
注意：属性捷径的Getter函数。

### `QList<QKeySequence> QAction::shortcuts() const`

**作用与语义：**

返回快捷方式列表，主快捷方式作为列表的第一个元素。

### `bool QAction::showStatusText(QObject *object = nullptr)`

**作用与语义：**

通过发送`QStatusTipEvent`更新`object`所代表的UI的相关状态栏。返回`true`事件是否已发送，否则返回`false`。
如果指定了空控件，事件会发送给动作的父控件。

### `[slot] void QAction::toggle()`

**作用与语义：**

这是 `checked` 属性的一个方便函数。连接到它以将被检查状态改为其相反状态。

### `[signal] void QAction::toggled(bool checked)`

**作用与语义：**

该属性决定动作是否被检查。
只能检查可检查的动作。默认情况下，这个操作是假的（该动作未被勾选）。
注意：该属性的通知信号是`toggled()`。由于切换`QAction`改变了状态，它也会发出`changed()`信号。

**如何使用：** 调用 `toggled()` 读取当前值；它不会修改应用状态。

### `[slot] void QAction::trigger()`

**作用与语义：**

这是一个方便的老虎机，可以调用激活（触发）。

### `[signal] void QAction::triggered(bool checked = false)`

**作用与语义：**

当用户激活某个动作时，会发出该信号;例如，当用户点击菜单选项、工具栏按钮或按下动作快捷键组合时，或当`trigger()`被调用时。值得注意的是，当调用`setChecked()`或`toggle()`时不会发出该信号。
如果动作可检验，`checked` 在被检查时为真;若动作未被检查，则为假。

### `bool autoRepeat() const`

**作用与语义：**

该属性是否能自动重复作用。
如果为真，只要系统启用键盘自动重复，按住快捷键组合时该动作会自动重复。默认值为 true。

**如何使用：** 调用 `autoRepeat()` 读取当前值；它不会修改应用状态。

### `QFont font() const`

**作用与语义：**

该属性包含动作的字体。
字体属性用于渲染`QAction`上的文本集。字体可以被视为提示，因为根据应用和风格，字体并非所有情况下都会被参考。
默认情况下，该属性包含应用程序的默认字体。

**如何使用：** 调用 `font()` 读取当前值；它不会修改应用状态。

### `QIcon icon() const`

**作用与语义：**

该属性包含动作图标。
在工具栏中，图标作为工具按钮图标使用;在菜单中，只要`QAction::iconVisibleInMenu`返回`true`，图标会显示在菜单文本的左侧。
没有默认图标。
如果将空图标（`QIcon::isNull()`）传递到该函数中，该动作图标将被清除。

**如何使用：** 调用 `icon()` 读取当前值；它不会修改应用状态。

### `QString iconText() const`

**作用与语义：**

该属性包含动作的描述性图标文本。
如果`QToolBar::toolButtonStyle`设置为允许显示文本的值，则该属性中定义的文本会以标签形式出现在相关工具按钮中。
如果动作未用`setText()`或`setToolTip()`定义，它也会作为菜单和工具提示的默认文本;如果没有用`setIcon()`定义图标，它也会被用于工具栏按钮。
如果图标文本未被显式设置，则使用该动作的正常文本作为图标文本。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `iconText()` 读取当前值；它不会修改应用状态。

### `bool isCheckable() const`

**作用与语义：**

该属性是否确定该动作是否为可检验动作。
可检查动作是指具有开/关状态的动作。例如，在文字处理器中，加粗工具栏按钮可以是开或关。不是切换操作的动作是命令动作;命令动作则是简单执行的，例如文件保存。默认情况下，该属性是`false`的。
在某些情况下，一个切换动作的状态应依赖于其他操作的状态。例如，“左对齐”、“中心”和“右对齐”切换动作是互斥的。要实现排他切换，将相关的切换动作添加到一个`QActionGroup`中，并将 QActionGroup：：exclusive 属性设置为 true。

**如何使用：** 调用 `isCheckable()` 读取当前值；它不会修改应用状态。

### `bool isChecked() const`

**作用与语义：**

该属性决定动作是否被检查。
只能检查可检查的动作。默认情况下，这个操作是假的（该动作未被勾选）。
注意：该属性的通知信号是`toggled()`。由于切换`QAction`改变了状态，它也会发出`changed()`信号。

**如何使用：** 调用 `isChecked()` 读取当前值；它不会修改应用状态。

### `bool isEnabled() const`

**作用与语义：**

该属性在动作是否被启用时成立。
禁用动作不能被用户选择。它们不会从菜单或工具栏中消失，但显示方式显示为不可用。例如，它们可能仅用灰色调显示。
这是什么？只要`QAction::whatsThis`属性已设置，残障操作帮助仍然可用。
当所有添加该动作的小部件（带有`QWidget::addAction()`）都被禁用或不可见时，该动作将被禁用。当动作被禁用时，无法通过快捷方式触发该动作。
默认情况下，该属性为`true`（动作已启用）。

**如何使用：** 调用 `isEnabled()` 读取当前值；它不会修改应用状态。

### `bool isIconVisibleInMenu() const`

**作用与语义：**

该属性决定了动作是否应在菜单中显示图标。
在某些应用中，工具栏中出现带图标的动作而菜单中不显示是合理的。如果为真，图标（如果有效）会在菜单中显示;如果为假，则不会显示。
默认情况下，是否为该应用设置了`Qt::AA_DontShowIconsInMenus`属性。显式设置该属性覆盖属性的存在（或缺失）。

**如何使用：** 调用 `isIconVisibleInMenu()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 QApplication app(argc, argv);
 app.setAttribute(Qt::AA_DontShowIconsInMenus);  // Icons are *no longer shown* in menus
 // ...
 QAction *myAction = new QAction();
 // ...
 myAction->setIcon(SomeIcon);
 myAction->setIconVisibleInMenu(true);   // Icon *will* be shown in menus for *this* action.
```

### `bool isShortcutVisibleInContextMenu() const`

**作用与语义：**

该属性决定了动作是否应在上下文菜单中显示快捷方式。
在某些应用中，在上下文菜单中设置带有快捷方式的动作可能是合理的。如果为真，则在通过上下文菜单显示动作时（如果有效）会显示该快捷方式;如果为假，则不会显示。
默认情况下，会根据`Qt::AA_DontShowShortcutsInContextMenus`属性是否为应用程序设置。显式设置该属性会覆盖该属性。

**如何使用：** 调用 `isShortcutVisibleInContextMenu()` 读取当前值；它不会修改应用状态。

### `bool isVisible() const`

**作用与语义：**

该属性决定动作是否可见（例如在菜单和工具栏中）。
如果 为真，操作可以被看到（例如在菜单和工具栏中），并由用户选择;如果为 false，则用户无法看到或选择该动作。
不可见的动作不会被灰化;它们根本不会出现。
默认情况下，该属性为`true`（动作可见）。

**如何使用：** 调用 `isVisible()` 读取当前值；它不会修改应用状态。

### `QAction::MenuRole menuRole() const`

**作用与语义：**

该属性承担动作菜单的角色。
这表示该动作在macOS应用菜单中的作用。默认情况下，所有动作都有`TextHeuristicRole`，这意味着该动作是根据文本添加的（更多信息请参见`QMenuBar`）。
菜单角色只能在 macOS 中将操作放入菜单栏之前更改（通常在第一个应用窗口显示之前）。

**如何使用：** 调用 `menuRole()` 读取当前值；它不会修改应用状态。

### `QAction::Priority priority() const`

**作用与语义：**

该属性在用户界面中保持动作的优先级。
该属性可以设置为用户界面中指示动作应如何优先排序。
例如，当工具栏设置了`Qt::ToolButtonTextBesideIcon`模式时，带有`LowPriority`的动作不会显示文本标签。

**如何使用：** 调用 `priority()` 读取当前值；它不会修改应用状态。

### `void setAutoRepeat(bool)`

**作用与语义：**

该属性是否能自动重复作用。
如果为真，只要系统启用键盘自动重复，按住快捷键组合时该动作会自动重复。默认值为 true。

**如何使用：** 调用 `setAutoRepeat(...)` 修改 `autoRepeat`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setCheckable(bool)`

**作用与语义：**

该属性是否确定该动作是否为可检验动作。
可检查动作是指具有开/关状态的动作。例如，在文字处理器中，加粗工具栏按钮可以是开或关。不是切换操作的动作是命令动作;命令动作则是简单执行的，例如文件保存。默认情况下，该属性是`false`的。
在某些情况下，一个切换动作的状态应依赖于其他操作的状态。例如，“左对齐”、“中心”和“右对齐”切换动作是互斥的。要实现排他切换，将相关的切换动作添加到一个`QActionGroup`中，并将 QActionGroup：：exclusive 属性设置为 true。

**如何使用：** 调用 `setCheckable(...)` 修改 `checkable`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setFont(const QFont &font)`

**作用与语义：**

该属性包含动作的字体。
字体属性用于渲染`QAction`上的文本集。字体可以被视为提示，因为根据应用和风格，字体并非所有情况下都会被参考。
默认情况下，该属性包含应用程序的默认字体。

**如何使用：** 调用 `setFont(...)` 修改 `font`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setIcon(const QIcon &icon)`

**作用与语义：**

该属性包含动作图标。
在工具栏中，图标作为工具按钮图标使用;在菜单中，只要`QAction::iconVisibleInMenu`返回`true`，图标会显示在菜单文本的左侧。
没有默认图标。
如果将空图标（`QIcon::isNull()`）传递到该函数中，该动作图标将被清除。

**如何使用：** 调用 `setIcon(...)` 修改 `icon`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setIconText(const QString &text)`

**作用与语义：**

该属性包含动作的描述性图标文本。
如果`QToolBar::toolButtonStyle`设置为允许显示文本的值，则该属性中定义的文本会以标签形式出现在相关工具按钮中。
如果动作未用`setText()`或`setToolTip()`定义，它也会作为菜单和工具提示的默认文本;如果没有用`setIcon()`定义图标，它也会被用于工具栏按钮。
如果图标文本未被显式设置，则使用该动作的正常文本作为图标文本。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `setIconText(...)` 修改 `iconText`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setIconVisibleInMenu(bool visible)`

**作用与语义：**

该属性决定了动作是否应在菜单中显示图标。
在某些应用中，工具栏中出现带图标的动作而菜单中不显示是合理的。如果为真，图标（如果有效）会在菜单中显示;如果为假，则不会显示。
默认情况下，是否为该应用设置了`Qt::AA_DontShowIconsInMenus`属性。显式设置该属性覆盖属性的存在（或缺失）。

**如何使用：** 调用 `setIconVisibleInMenu(...)` 修改 `iconVisibleInMenu`；传入的新值会成为后续查询和相关界面行为所使用的值。

**官方示例：**

```cpp
 QApplication app(argc, argv);
 app.setAttribute(Qt::AA_DontShowIconsInMenus);  // Icons are *no longer shown* in menus
 // ...
 QAction *myAction = new QAction();
 // ...
 myAction->setIcon(SomeIcon);
 myAction->setIconVisibleInMenu(true);   // Icon *will* be shown in menus for *this* action.
```

### `void setMenuRole(QAction::MenuRole menuRole)`

**作用与语义：**

该属性承担动作菜单的角色。
这表示该动作在macOS应用菜单中的作用。默认情况下，所有动作都有`TextHeuristicRole`，这意味着该动作是根据文本添加的（更多信息请参见`QMenuBar`）。
菜单角色只能在 macOS 中将操作放入菜单栏之前更改（通常在第一个应用窗口显示之前）。

**如何使用：** 调用 `setMenuRole(...)` 修改 `menuRole`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setPriority(QAction::Priority priority)`

**作用与语义：**

该属性在用户界面中保持动作的优先级。
该属性可以设置为用户界面中指示动作应如何优先排序。
例如，当工具栏设置了`Qt::ToolButtonTextBesideIcon`模式时，带有`LowPriority`的动作不会显示文本标签。

**如何使用：** 调用 `setPriority(...)` 修改 `priority`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setShortcutContext(Qt::ShortcutContext context)`

**作用与语义：**

该属性为动作的快捷方式提供了上下文。
该属性的有效值可在`Qt::ShortcutContext`中找到。默认值为`Qt::WindowShortcut`。

**如何使用：** 调用 `setShortcutContext(...)` 修改 `shortcutContext`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setShortcutVisibleInContextMenu(bool show)`

**作用与语义：**

该属性决定了动作是否应在上下文菜单中显示快捷方式。
在某些应用中，在上下文菜单中设置带有快捷方式的动作可能是合理的。如果为真，则在通过上下文菜单显示动作时（如果有效）会显示该快捷方式;如果为假，则不会显示。
默认情况下，会根据`Qt::AA_DontShowShortcutsInContextMenus`属性是否为应用程序设置。显式设置该属性会覆盖该属性。

**如何使用：** 调用 `setShortcutVisibleInContextMenu(...)` 修改 `shortcutVisibleInContextMenu`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setStatusTip(const QString &statusTip)`

**作用与语义：**

该属性包含动作的状态提示。
状态提示会显示在动作顶层父控件提供的所有状态栏上。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `setStatusTip(...)` 修改 `statusTip`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setText(const QString &text)`

**作用与语义：**

该属性包含动作的描述文本。
如果动作被添加到菜单中，菜单选项将由图标（如果有）、文本和快捷方式（如果有）组成。如果文本未在构造函数中明确设置，或使用 setText()，则动作的描述图标文本将被用作文本。没有默认文本。
某些界面元素，如菜单或按钮，可以在字符前使用“&”，自动为该字符创建助记法（快捷方式）。例如，菜单中的“&File”会创建快捷键Alt F，打开文件菜单。“E&xit”会创建快捷键Alt X作为按钮，或者在菜单中允许通过按“x”导航到菜单项。（使用“&”来显示实际的&符号）。小部件可能会对某个快捷方式进行消费和执行动作。

**如何使用：** 调用 `setText(...)` 修改 `text`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setToolTip(const QString &tip)`

**作用与语义：**

该属性包含动作的工具提示。
此文本用于提示。若未指定提示，则使用动作文本。
默认情况下，该属性包含动作的文本。

**如何使用：** 调用 `setToolTip(...)` 修改 `toolTip`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setWhatsThis(const QString &what)`

**作用与语义：**

该属性包含动作的“这是什么？”帮助文本。
“这是什么？”文本用于简要描述动作。文本可能包含富文本。没有默认的“这是什么？”文本。

**如何使用：** 调用 `setWhatsThis(...)` 修改 `whatsThis`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `Qt::ShortcutContext shortcutContext() const`

**作用与语义：**

该属性为动作的快捷方式提供了上下文。
该属性的有效值可在`Qt::ShortcutContext`中找到。默认值为`Qt::WindowShortcut`。

**如何使用：** 调用 `shortcutContext()` 读取当前值；它不会修改应用状态。

### `QString statusTip() const`

**作用与语义：**

该属性包含动作的状态提示。
状态提示会显示在动作顶层父控件提供的所有状态栏上。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `statusTip()` 读取当前值；它不会修改应用状态。

### `QString text() const`

**作用与语义：**

该属性包含动作的描述文本。
如果动作被添加到菜单中，菜单选项将由图标（如果有）、文本和快捷方式（如果有）组成。如果文本未在构造函数中明确设置，或使用 setText()，则动作的描述图标文本将被用作文本。没有默认文本。
某些界面元素，如菜单或按钮，可以在字符前使用“&”，自动为该字符创建助记法（快捷方式）。例如，菜单中的“&File”会创建快捷键Alt F，打开文件菜单。“E&xit”会创建快捷键Alt X作为按钮，或者在菜单中允许通过按“x”导航到菜单项。（使用“&”来显示实际的&符号）。小部件可能会对某个快捷方式进行消费和执行动作。

**如何使用：** 调用 `text()` 读取当前值；它不会修改应用状态。

### `QString toolTip() const`

**作用与语义：**

该属性包含动作的工具提示。
此文本用于提示。若未指定提示，则使用动作文本。
默认情况下，该属性包含动作的文本。

**如何使用：** 调用 `toolTip()` 读取当前值；它不会修改应用状态。

### `QString whatsThis() const`

**作用与语义：**

该属性包含动作的“这是什么？”帮助文本。
“这是什么？”文本用于简要描述动作。文本可能包含富文本。没有默认的“这是什么？”文本。

**如何使用：** 调用 `whatsThis()` 读取当前值；它不会修改应用状态。

### `void resetEnabled()`

**作用与语义：**

该属性在动作是否被启用时成立。
禁用动作不能被用户选择。它们不会从菜单或工具栏中消失，但显示方式显示为不可用。例如，它们可能仅用灰色调显示。
这是什么？只要`QAction::whatsThis`属性已设置，残障操作帮助仍然可用。
当所有添加该动作的小部件（带有`QWidget::addAction()`）都被禁用或不可见时，该动作将被禁用。当动作被禁用时，无法通过快捷方式触发该动作。
默认情况下，该属性为`true`（动作已启用）。

**如何使用：** 调用 `resetEnabled()` 撤销对 `enabled` 的显式覆盖，让它重新采用继承值或默认值。

### `void setChecked(bool)`

**作用与语义：**

该属性决定动作是否被检查。
只能检查可检查的动作。默认情况下，这个操作是假的（该动作未被勾选）。
注意：该属性的通知信号是`toggled()`。由于切换`QAction`改变了状态，它也会发出`changed()`信号。

**如何使用：** 调用 `setChecked(...)` 修改 `checked`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setEnabled(bool)`

**作用与语义：**

该属性在动作是否被启用时成立。
禁用动作不能被用户选择。它们不会从菜单或工具栏中消失，但显示方式显示为不可用。例如，它们可能仅用灰色调显示。
这是什么？只要`QAction::whatsThis`属性已设置，残障操作帮助仍然可用。
当所有添加该动作的小部件（带有`QWidget::addAction()`）都被禁用或不可见时，该动作将被禁用。当动作被禁用时，无法通过快捷方式触发该动作。
默认情况下，该属性为`true`（动作已启用）。

**如何使用：** 调用 `setEnabled(...)` 修改 `enabled`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setVisible(bool)`

**作用与语义：**

该属性决定动作是否可见（例如在菜单和工具栏中）。
如果 为真，操作可以被看到（例如在菜单和工具栏中），并由用户选择;如果为 false，则用户无法看到或选择该动作。
不可见的动作不会被灰化;它们根本不会出现。
默认情况下，该属性为`true`（动作可见）。

**如何使用：** 调用 `setVisible(...)` 修改 `visible`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void checkableChanged(bool checkable)`

**作用与语义：**

该属性是否确定该动作是否为可检验动作。
可检查动作是指具有开/关状态的动作。例如，在文字处理器中，加粗工具栏按钮可以是开或关。不是切换操作的动作是命令动作;命令动作则是简单执行的，例如文件保存。默认情况下，该属性是`false`的。
在某些情况下，一个切换动作的状态应依赖于其他操作的状态。例如，“左对齐”、“中心”和“右对齐”切换动作是互斥的。要实现排他切换，将相关的切换动作添加到一个`QActionGroup`中，并将 QActionGroup：：exclusive 属性设置为 true。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `checkable` 的变化，不要把它当作普通函数主动调用。

### `void enabledChanged(bool enabled)`

**作用与语义：**

该属性在动作是否被启用时成立。
禁用动作不能被用户选择。它们不会从菜单或工具栏中消失，但显示方式显示为不可用。例如，它们可能仅用灰色调显示。
这是什么？只要`QAction::whatsThis`属性已设置，残障操作帮助仍然可用。
当所有添加该动作的小部件（带有`QWidget::addAction()`）都被禁用或不可见时，该动作将被禁用。当动作被禁用时，无法通过快捷方式触发该动作。
默认情况下，该属性为`true`（动作已启用）。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `enabled` 的变化，不要把它当作普通函数主动调用。

### `void visibleChanged()`

**作用与语义：**

该属性决定动作是否可见（例如在菜单和工具栏中）。
如果 为真，操作可以被看到（例如在菜单和工具栏中），并由用户选择;如果为 false，则用户无法看到或选择该动作。
不可见的动作不会被灰化;它们根本不会出现。
默认情况下，该属性为`true`（动作可见）。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `visible` 的变化，不要把它当作普通函数主动调用。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

### 状态和错误边界

QObject 派生对象的状态通常通过属性、状态查询函数和信号变化共同表达。信号是通知，不是返回值；收到通知后应读取当前状态并处理异常路径，不能假设每个信号只会出现一次。

### 线程边界

QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

### 最容易出现的错误

不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QAction` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
