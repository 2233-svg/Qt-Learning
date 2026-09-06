# QMenu

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QMenu` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QMenu` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QMenu>`
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

- `icon : QIcon`
- `separatorsCollapsible : bool`
- `tearOffEnabled : bool`
- `title : QString`
- `toolTipsVisible : bool`

### 公有函数

- `QMenu(QWidget *parent = nullptr)`
- `QMenu(const QString &title, QWidget *parent = nullptr)`
- `virtual ~QMenu()`
- `QAction * actionAt(const QPoint &pt) const`
- `QRect actionGeometry(QAction *act) const`
- `QAction * activeAction() const`
- `QAction * addMenu(QMenu *menu)`
- `QMenu * addMenu(const QString &title)`
- `QMenu * addMenu(const QIcon &icon, const QString &title)`
- `QAction * addSection(const QString &text)`
- `QAction * addSection(const QIcon &icon, const QString &text)`
- `QAction * addSeparator()`
- `void clear()`
- `QAction * defaultAction() const`
- `QAction * exec()`
- `QAction * exec(const QPoint &p, QAction *action = nullptr)`
- `void hideTearOffMenu()`
- `QIcon icon() const`
- `QAction * insertMenu(QAction *before, QMenu *menu)`
- `QAction * insertSection(QAction *before, const QString &text)`
- `QAction * insertSection(QAction *before, const QIcon &icon, const QString &text)`
- `QAction * insertSeparator(QAction *before)`
- `bool isEmpty() const`
- `bool isTearOffEnabled() const`
- `bool isTearOffMenuVisible() const`
- `QAction * menuAction() const`
- `void popup(const QPoint &p, QAction *atAction = nullptr)`
- `bool separatorsCollapsible() const`
- `void setActiveAction(QAction *act)`
- `void setAsDockMenu()`
- `void setDefaultAction(QAction *act)`
- `void setIcon(const QIcon &icon)`
- `void setSeparatorsCollapsible(bool collapse)`
- `void setTearOffEnabled(bool)`
- `void setTitle(const QString &title)`
- `void setToolTipsVisible(bool visible)`
- `void showTearOffMenu(const QPoint &pos)`
- `void showTearOffMenu()`
- `QString title() const`
- `NSMenu * toNSMenu()`
- `bool toolTipsVisible() const`

### 重实现的公有函数

- `virtual QSize sizeHint() const override`

### 信号

- `void aboutToHide()`
- `void aboutToShow()`
- `void hovered(QAction *action)`
- `void triggered(QAction *action)`

### 静态公有成员

- `QAction * exec(const QList<QAction *> &actions, const QPoint &pos, QAction *at = nullptr, QWidget *parent = nullptr)`
- `QMenu * menuInAction(const QAction *action)`

### 保护函数

- `int columnCount() const`
- `virtual void initStyleOption(QStyleOptionMenuItem *option, const QAction *action) const`

### 重实现的保护函数

- `virtual void actionEvent(QActionEvent *e) override`
- `virtual void changeEvent(QEvent *e) override`
- `virtual void enterEvent(QEnterEvent *) override`
- `virtual bool event(QEvent *e) override`
- `virtual bool focusNextPrevChild(bool next) override`
- `virtual void hideEvent(QHideEvent *) override`
- `virtual void keyPressEvent(QKeyEvent *e) override`
- `virtual void leaveEvent(QEvent *) override`
- `virtual void mouseMoveEvent(QMouseEvent *e) override`
- `virtual void mousePressEvent(QMouseEvent *e) override`
- `virtual void mouseReleaseEvent(QMouseEvent *e) override`
- `virtual void paintEvent(QPaintEvent *e) override`
- `virtual void timerEvent(QTimerEvent *e) override`
- `virtual void wheelEvent(QWheelEvent *e) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `icon : QIcon`

**作用与语义：**

该属性保留菜单图标。
这等价于`menuAction()`的`QAction::icon`属性。
默认情况下，如果没有明确设置图标，该属性包含一个空图标。

**如何使用：** 调用 `icon()` 读取当前值；它不会修改应用状态。

### `separatorsCollapsible : bool`

**作用与语义：**

该属性适用于是否折叠连续分隔符。
该属性指定菜单中是否将连续分隔符在视觉上折叠为一个。菜单开头或结尾的分隔符亦被隐藏。
默认情况下，该属性为 `true`。

**如何使用：** 调用 `separatorsCollapsible()` 读取当前值；它不会修改应用状态。

### `tearOffEnabled : bool`

**作用与语义：**

该属性是否支持菜单被撕下。
当为真时，菜单包含一个特殊的撕下物品（通常在菜单顶部以虚线显示），触发时会生成菜单的副本。
这个“撕下”的副本存在一个独立窗口。它包含与原始菜单相同的菜单项，唯一不同的是撕下手柄。
默认情况下，该属性为`false`。

**如何使用：** 调用 `tearOffEnabled()` 读取当前值；它不会修改应用状态。

### `title : QString`

**作用与语义：**

该物业拥有菜单的标题。
这等价于`menuAction()`的`QAction::text`属性。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `title()` 读取当前值；它不会修改应用状态。

### `toolTipsVisible : bool`

**作用与语义：**

该属性决定菜单操作的工具提示是否应可见。
该属性指定操作菜单条目是否显示其提示。
默认情况下，该属性为`false`。

**如何使用：** 调用 `toolTipsVisible()` 读取当前值；它不会修改应用状态。

### `[explicit] QMenu::QMenu(QWidget *parent = nullptr)`

**作用与语义：**

构建带有父`parent`的菜单。
虽然弹出菜单始终是顶层小部件，但如果父菜单被传递，弹出菜单会在父节点被销毁时被删除（与其他`QObject`一样）。

### `[explicit] QMenu::QMenu(const QString &title, QWidget *parent = nullptr)`

**作用与语义：**

构建包含`title`和一个`parent`的菜单。
虽然弹出菜单始终是顶层小部件，但如果通过父菜单，当该父节点被销毁时（与其他`QObject`一样），弹出菜单会被删除。

### `[virtual noexcept] QMenu::~QMenu()`

**作用与语义：**

菜单都毁了。

### `[signal] void QMenu::aboutToHide()`

**作用与语义：**

该信号在菜单被隐藏前发出。

### `[signal] void QMenu::aboutToShow()`

**作用与语义：**

该信号在菜单显示给用户之前发出。

### `QAction *QMenu::actionAt(const QPoint &pt) const`

**作用与语义：**

在`pt`返回该物品;如果没有物品，则返回`nullptr`。

### `[override virtual protected] void QMenu::actionEvent(QActionEvent *e)`

**作用与语义：**

重实现自：`QWidget::actionEvent`（QActionEvent *event）。
每当控件的动作发生变化时，该事件处理程序都会被调用给定的`event`。

### `QRect QMenu::actionGeometry(QAction *act) const`

**作用与语义：**

返回作用的几何形状`act`。

### `QAction *QMenu::activeAction() const`

**作用与语义：**

返回当前高亮的动作，若当前无动作则返回`nullptr`。

### `QAction *QMenu::addMenu(QMenu *menu)`

**作用与语义：**

这个便利功能将`menu`作为菜单的子菜单添加。它返回`menu`的`menuAction()`。该菜单不对`menu`拥有所有权。

### `QMenu *QMenu::addMenu(const QString &title)`

**作用与语义：**

在菜单中附加一个带有`title`的新`QMenu`。菜单对菜单拥有所有权。返回新菜单。

### `QMenu *QMenu::addMenu(const QIcon &icon, const QString &title)`

**作用与语义：**

在菜单中附加一个带有`icon`和`title`的新`QMenu`。菜单对菜单拥有所有权。返回新菜单。

### `QAction *QMenu::addSection(const QString &text)`

**作用与语义：**

这个便利函数会创建一个新的部分动作，即一个`QAction::isSeparator()`返回真且`text`同时带有提示的动作，并将该新动作添加到该菜单的动作列表中。它返回新创建的动作。
提示的渲染取决于样式和平台。控件样式可以在渲染中使用文本信息来区分部分，也可以选择忽略它，像简单的分隔符一样渲染部分。
`QMenu`接管归还的归还`QAction`。

### `QAction *QMenu::addSection(const QIcon &icon, const QString &text)`

**作用与语义：**

这个便利功能会创建一个新的部分动作，即一个`QAction::isSeparator()`返回为真且带有 `text` 和 `icon` 提示的动作，并将该新动作添加到该菜单的动作列表中。它返回新创建的动作。
提示的渲染取决于样式和平台。控件样式可以在渲染中使用文本和图标信息来区分部分，也可以选择忽略它们，像简单的分隔符一样渲染部分。
`QMenu`接管了归还的这`QAction`。

### `QAction *QMenu::addSeparator()`

**作用与语义：**

这个便利函数会创建一个新的分隔符动作，即一个返回 true `QAction::isSeparator()` 的动作，并将该新动作添加到该菜单的动作列表中。它返回了新创建的动作。
`QMenu`接管了归还的`QAction`。

### `[override virtual protected] void QMenu::changeEvent(QEvent *e)`

**作用与语义：**

重装：`QWidget::changeEvent`（QEvent *事件）。
该事件处理程序可以重新实现以处理状态变化。
该事件中被更改的状态可以通过提供的`event`检索。
变更事件包括：`QEvent::ToolBarChange`、`QEvent::ActivationChange`、`QEvent::EnabledChange`、`QEvent::FontChange`、`QEvent::StyleChange`、`QEvent::PaletteChange`、`QEvent::WindowTitleChange`、`QEvent::IconTextChange`、`QEvent::ModifiedChange`、`QEvent::MouseTrackingChange`、`QEvent::ParentChange`、`QEvent::WindowStateChange`、`QEvent::LanguageChange`、`QEvent::LocaleChange`、`QEvent::LayoutDirectionChange`、`QEvent::ReadOnlyChange`。

### `void QMenu::clear()`

**作用与语义：**

移除菜单中的所有操作。菜单拥有且未显示在其他小部件中的动作被删除。

### `[protected] int QMenu::columnCount() const`

**作用与语义：**

如果菜单不适合放在屏幕上，它会自己布局，使其能放下。这取决于样式，取决于布局的含义（例如，在Windows上会使用多列）。
该函数返回所需的列数。

### `QAction *QMenu::defaultAction() const`

**作用与语义：**

返回当前默认动作。

### `[override virtual protected] void QMenu::enterEvent(QEnterEvent *)`

**作用与语义：**

重实现自：`QWidget::enterEvent`（QEnterEvent *event）。
该事件处理程序可以在子类中重新实现，以接收通过 `event` 参数传递的控件进入事件。
当鼠标光标进入控件时，会发送一个事件到控件。

### `[override virtual protected] bool QMenu::event(QEvent *e)`

**作用与语义：**

重实现自：`QWidget::event`（QEvent *事件）。

### `QAction *QMenu::exec()`

**作用与语义：**

同步执行该菜单。
这相当于`exec(pos())`。
这会在弹出菜单或其子菜单中返回触发`QAction`，如果没有触发（通常是因为用户按了Esc键），则返回`nullptr`。
在大多数情况下，你需要自己指定位置，比如当前鼠标的位置：
或与小部件对齐：
或者对`QMouseEvent` *e 的反应：

**官方示例：**

```cpp
 exec(QCursor::pos());
```

### `QAction *QMenu::exec(const QPoint &p, QAction *action = nullptr)`

**作用与语义：**

同步执行该菜单。
弹出菜单，使动作`action`位于指定的全局位置`p`。要将小部件的本地坐标转换为全局坐标，请使用`QWidget::mapToGlobal()`。
这会在弹窗菜单或其子菜单中返回触发`QAction`，如果没有触发物品（通常是因为用户按了Esc键），则返回`nullptr`。
注意所有信号均照常发射。如果你将`QAction`连接到槽函数并调用菜单的exec()，你会通过信号槽连接和exec（返回值）获得结果。
常用方法是将菜单置于当前鼠标位置：
或与小部件对齐：
或者对`QMouseEvent`*e的反应：
在用exec()或`popup()`定位菜单时，请记住不能依赖菜单当前的当前大小`size()`。出于性能考虑，菜单只在必要时调整大小。因此，在许多情况下，节目前后的大小是不同的。相反，使用根据菜单当前内容计算正确大小的 `sizeHint()`。

**官方示例：**

```cpp
 exec(QCursor::pos());
```

### `[static] QAction *QMenu::exec(const QList<QAction *> &actions, const QPoint &pos, QAction *at = nullptr, QWidget *parent = nullptr)`

**作用与语义：**

同步执行菜单。
菜单的操作由`actions`列表指定。菜单会弹出，使指定的动作`at`显示在全局位置`pos`。如果未指定`at`，菜单会显示在位置`pos`。`parent` 是菜单的父控件;当仅有 `pos` 无法决定菜单的放置位置时，指定父节点可以提供上下文（例如，多个桌面或父节点嵌入 `QGraphicsView` 时）。
该函数会在弹出菜单或其子菜单中返回触发`QAction`，如果没有触发（通常是用户按了 Esc），则返回`nullptr`。
这等价于：

**官方示例：**

```cpp
 QMenu menu;
 QAction *at = actions[0]; // Assumes actions is not empty
 for (QAction *a : std::as_const(actions))
     menu.addAction(a);
 menu.exec(pos, at);
```

### `[override virtual protected] bool QMenu::focusNextPrevChild(bool next)`

**作用与语义：**

重构：`QWidget::focusNextPrevChild`（下一个布尔）。
根据 Tab 和 Shift Tab 找到一个新的控件来给键盘焦点，如果能找到新控件，则返回 `true`，找不到则返回 false。
如果`next`为真，该函数向前搜索;如果`next`为假，则向后搜索。
有时，你会想重新实现这个函数。例如，浏览器可能会重新实现它，将“当前活跃链接”向前或向后移动，只有当它到达“页面”的最后或第一个链接时才调用 focusNextPrevChild()。
子控件调用其父控件的 focusNextPrevChild()，但只有包含子控件的窗口决定将焦点重定向到哪里。通过重新实现该函数，你就能控制所有子控件的焦点遍历。

### `[override virtual protected] void QMenu::hideEvent(QHideEvent *)`

**作用与语义：**

重实现自：`QWidget::hideEvent`（QHideEvent *event）。
该事件处理程序可以在子类中重新实现，以接收控件隐藏事件。事件通过`event`参数传递。
隐藏事件会在小部件被隐藏后立即发送。
注意：当窗口系统改变其映射状态时，小部件会接收自发显示和隐藏事件，例如用户最小化窗口时自发隐藏事件，恢复窗口时自发显示事件。收到自发隐藏事件后，小部件仍被视为可见，意义`isVisible()`。

### `void QMenu::hideTearOffMenu()`

**作用与语义：**

该功能会强制隐藏被撕下的菜单，使其从用户桌面消失。

### `[signal] void QMenu::hovered(QAction *action)`

**作用与语义：**

当菜单动作被高亮时，该信号会被发出;`action` 是导致该信号发出的动作。
通常用于更新状态信息。

### `[virtual protected] void QMenu::initStyleOption(QStyleOptionMenuItem *option, const QAction *action) const`

**作用与语义：**

用菜单中的数值和`action`的信息初始化`option`。这种方法对子类需要一个 `QStyleOptionMenuItem`，但不想自己填满所有信息时非常有用。

### `QAction *QMenu::insertMenu(QAction *before, QMenu *menu)`

**作用与语义：**

这个便利功能会在操作`before`前插入`menu`，并返回菜单`menuAction()`。

### `QAction *QMenu::insertSection(QAction *before, const QString &text)`

**作用与语义：**

该便利函数创建新的标题动作，即 `QAction::isSeparator()` 返回真且同时带有提示`text`的动作。该函数将新创建的动作插入该菜单的动作列表中，然后返回该动作`before`。
提示的渲染取决于样式和平台。控件样式可以在渲染中使用文本信息来区分部分，也可以选择忽略它，像简单的分隔符一样渲染部分。
`QMenu`接管归还的归还`QAction`。

### `QAction *QMenu::insertSection(QAction *before, const QIcon &icon, const QString &text)`

**作用与语义：**

这个便利函数会创建一个新的标题动作，即一个 `QAction::isSeparator()` 返回为真但同时包含 `text` 和 `icon` 提示的动作。该函数会在动作`before`前将新创建的动作插入该菜单的动作列表中并返回。
提示的渲染取决于样式和平台。控件样式可以在渲染中使用文本和图标信息来区分部分，也可以选择忽略它们，像简单的分隔符一样渲染部分。
`QMenu`接管了归还的那`QAction`。

### `QAction *QMenu::insertSeparator(QAction *before)`

**作用与语义：**

该便利函数创建新的分隔符动作，即返回 true `QAction::isSeparator()` 的动作。该函数在动作`before`前将新创建的动作插入该菜单的动作列表中并返回。
`QMenu`接管归还的`QAction`。

### `bool QMenu::isEmpty() const`

**作用与语义：**

如果菜单中没有显示的动作，返回`true`，否则返回，否则为false。

### `bool QMenu::isTearOffMenuVisible() const`

**作用与语义：**

当菜单被撕下时，会显示第二个菜单，在新窗口中显示菜单内容。当菜单处于该模式且菜单可见时，返回`true`;否则为假。

### `[override virtual protected] void QMenu::keyPressEvent(QKeyEvent *e)`

**作用与语义：**

重实现自：`QWidget::keyPressEvent`（QKeyEvent *event）。
该事件处理程序用于事件`event`，可以在子类中重新实现，以接收该控件的按键事件。
一个小部件必须调用`setFocusPolicy()`先接受焦点，并且必须有焦点才能接收按键事件。
如果你重新实现这个处理器，如果你不对密钥进行操作，务必调用基类实现。
默认实现会关闭弹出小部件，如果用户按下`QKeySequence::Cancel`的按键序列（通常是 Escape 键）。否则事件会被忽略，以便小部件的父节点能够解释。
注意`QKeyEvent`以 isAccepted() == true 开头，所以你不需要调用 `QKeyEvent::accept()`——只要你对该键执行时不要调用基类实现即可。

### `[override virtual protected] void QMenu::leaveEvent(QEvent *)`

**作用与语义：**

重装：`QWidget::leaveEvent`（QEvent *事件）。
该事件处理程序可以被子类重新实现，以接收通过 `event` 参数传递的控件离开事件。
当鼠标光标离开控件时，会向控件发送一个离开事件。

### `QAction *QMenu::menuAction() const`

**作用与语义：**

返回与该菜单相关的操作。

### `[static] QMenu *QMenu::menuInAction(const QAction *action)`

**作用与语义：**

返回`action`包含的菜单，或者如果`action`没有菜单，则返回`nullptr`。
在控件应用中，包含菜单的动作可以用来创建带有子菜单的菜单项，或插入工具栏以创建带有弹出菜单的按钮。

### `[override virtual protected] void QMenu::mouseMoveEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QWidget::mouseMoveEvent`（QMouseEvent *event）。
该事件处理程序用于事件`event`，可以重新实现为子类，以接收该小部件的鼠标移动事件。
如果关闭鼠标追踪，只有在鼠标移动过程中按下鼠标按钮时才会发生鼠标移动事件。如果开启鼠标追踪，即使未按键，鼠标移动事件也会发生。
`QMouseEvent::position()`报告鼠标光标相对于该小部件的位置。对于按下和释放事件，位置通常与最后一次鼠标移动事件的位置相同，但如果用户的手握手，可能会有所不同。这是底层窗口系统的功能，而非Qt。
如果你想在鼠标移动时立即显示提示（例如，获取鼠标坐标与`QMouseEvent::position()`并显示为提示），你必须先启用上述的鼠标追踪功能。然后，为了确保提示立即更新，你必须在鼠标移动事件（mouseMoveEvent）实现中调用`QToolTip::showText()`而不是`setToolTip()`。

### `[override virtual protected] void QMenu::mousePressEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QWidget::mousePressEvent`（QMouseEvent *event）。
该事件处理程序用于事件`event`，可以重新实现为子类，以接收该小部件的鼠标按键事件。
如果你在 mousePressEvent() 创建新控件，`mouseReleaseEvent()`可能不会出现在你预期的位置，这取决于底层窗口系统（或 X11 窗口管理器）、控件的位置，甚至可能还有其他因素。
默认实现实现了当你点击窗口外时关闭弹出小部件的功能。对于其他小部件类型，它没有任何作用。

### `[override virtual protected] void QMenu::mouseReleaseEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QWidget::mouseReleaseEvent`（QMouseEvent *event）。
该事件处理程序用于事件`event`，可以重新实现为子类，以接收该小部件的鼠标释放事件。

### `[override virtual protected] void QMenu::paintEvent(QPaintEvent *e)`

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

### `void QMenu::popup(const QPoint &p, QAction *atAction = nullptr)`

**作用与语义：**

显示菜单，使动作`atAction`位于指定的全局位置`p`。要将小部件的本地坐标转换为全局坐标，请使用`QWidget::mapToGlobal()`。
在用`exec()`或弹出菜单定位菜单时，请记住不能依赖菜单当前的 `size()`。出于性能考虑，菜单只在必要时调整大小，因此在许多情况下，节目前后的大小是不同的。相反，可以使用根据菜单当前内容计算正确大小的 `sizeHint()`。

### `void QMenu::setActiveAction(QAction *act)`

**作用与语义：**

将当前高亮的动作设置为`act`。

### `void QMenu::setAsDockMenu()`

**作用与语义：**

将此菜单设置为通过点击应用底座图标选项即可获得的扩展座菜单。仅在macOS上使用。

### `void QMenu::setDefaultAction(QAction *act)`

**作用与语义：**

这会将默认动作设置为`act`。默认动作可能会有视觉提示，具体取决于当前`QStyle`。默认动作通常表示掉落发生时默认会发生什么。

### `void QMenu::showTearOffMenu(const QPoint &pos)`

**作用与语义：**

该功能会强制显示被撕下的菜单，使其在用户桌面的指定全局位置`pos`显示。

### `void QMenu::showTearOffMenu()`

**作用与语义：**

该功能会强制显示被撕下的菜单，使其在鼠标光标下显示在用户桌面上。

### `[override virtual] QSize QMenu::sizeHint() const`

**作用与语义：**

重新实现了属性的访问函数：`QWidget::sizeHint`。

### `[override virtual protected] void QMenu::timerEvent(QTimerEvent *e)`

**作用与语义：**

重实现自：`QObject::timerEvent`（QTimerEvent *event）。

### `NSMenu *QMenu::toNSMenu()`

**作用与语义：**

返回本菜单的原生 NSMenu。仅支持 macOS。
注意：Qt在本地菜单上设置代理。如果你需要自己设置代理，确保保存原始代理并转发任何调用。

### `[signal] void QMenu::triggered(QAction *action)`

**作用与语义：**

当菜单中触发动作时，会发出该信号。
`action`是导致信号发出的动作。
通常，你会把每个菜单动作的`triggered()`信号连接到它自己的自定义槽，但有时你会想把多个动作连接到同一个槽，比如当你有一组密切相关的动作，比如“左二位对位”、“居中”、“右右对位”时。
注意：该信号是针对层级结构中的主父菜单发出的。因此，只需连接父菜单到槽函数;子菜单则无需连接。

### `[override virtual protected] void QMenu::wheelEvent(QWheelEvent *e)`

**作用与语义：**

重实现自：`QWidget::wheelEvent`（QWheelEvent *event）。
该事件处理程序用于事件`event`，可以在子类中重新实现，以接收该控件的轮事件。
如果你重新实现了这个处理程序，非常重要的是，如果你不处理事件，必须`ignore()`事件，这样小部件的父节点才能解释它。
默认实现会忽略该事件。

### `QIcon icon() const`

**作用与语义：**

该属性保留菜单图标。
这等价于`menuAction()`的`QAction::icon`属性。
默认情况下，如果没有明确设置图标，该属性包含一个空图标。

**如何使用：** 调用 `icon()` 读取当前值；它不会修改应用状态。

### `bool isTearOffEnabled() const`

**作用与语义：**

该属性是否支持菜单被撕下。
当为真时，菜单包含一个特殊的撕下物品（通常在菜单顶部以虚线显示），触发时会生成菜单的副本。
这个“撕下”的副本存在一个独立窗口。它包含与原始菜单相同的菜单项，唯一不同的是撕下手柄。
默认情况下，该属性为`false`。

**如何使用：** 调用 `isTearOffEnabled()` 读取当前值；它不会修改应用状态。

### `bool separatorsCollapsible() const`

**作用与语义：**

该属性适用于是否折叠连续分隔符。
该属性指定菜单中是否将连续分隔符在视觉上折叠为一个。菜单开头或结尾的分隔符亦被隐藏。
默认情况下，该属性为 `true`。

**如何使用：** 调用 `separatorsCollapsible()` 读取当前值；它不会修改应用状态。

### `void setIcon(const QIcon &icon)`

**作用与语义：**

该属性保留菜单图标。
这等价于`menuAction()`的`QAction::icon`属性。
默认情况下，如果没有明确设置图标，该属性包含一个空图标。

**如何使用：** 调用 `setIcon(...)` 修改 `icon`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setSeparatorsCollapsible(bool collapse)`

**作用与语义：**

该属性适用于是否折叠连续分隔符。
该属性指定菜单中是否将连续分隔符在视觉上折叠为一个。菜单开头或结尾的分隔符亦被隐藏。
默认情况下，该属性为 `true`。

**如何使用：** 调用 `setSeparatorsCollapsible(...)` 修改 `separatorsCollapsible`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTearOffEnabled(bool)`

**作用与语义：**

该属性是否支持菜单被撕下。
当为真时，菜单包含一个特殊的撕下物品（通常在菜单顶部以虚线显示），触发时会生成菜单的副本。
这个“撕下”的副本存在一个独立窗口。它包含与原始菜单相同的菜单项，唯一不同的是撕下手柄。
默认情况下，该属性为`false`。

**如何使用：** 调用 `setTearOffEnabled(...)` 修改 `tearOffEnabled`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTitle(const QString &title)`

**作用与语义：**

该物业拥有菜单的标题。
这等价于`menuAction()`的`QAction::text`属性。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `setTitle(...)` 修改 `title`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setToolTipsVisible(bool visible)`

**作用与语义：**

该属性决定菜单操作的工具提示是否应可见。
该属性指定操作菜单条目是否显示其提示。
默认情况下，该属性为`false`。

**如何使用：** 调用 `setToolTipsVisible(...)` 修改 `toolTipsVisible`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QString title() const`

**作用与语义：**

该物业拥有菜单的标题。
这等价于`menuAction()`的`QAction::text`属性。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `title()` 读取当前值；它不会修改应用状态。

### `bool toolTipsVisible() const`

**作用与语义：**

该属性决定菜单操作的工具提示是否应可见。
该属性指定操作菜单条目是否显示其提示。
默认情况下，该属性为`false`。

**如何使用：** 调用 `toolTipsVisible()` 读取当前值；它不会修改应用状态。

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

`QMenu` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
