# QButtonGroup

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QButtonGroup` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QButtonGroup` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QButtonGroup>`
- 继承自：QObject
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

- `exclusive : bool`

### 公有函数

- `QButtonGroup(QObject *parent = nullptr)`
- `virtual ~QButtonGroup()`
- `void addButton(QAbstractButton *button, int id = -1)`
- `QAbstractButton * button(int id) const`
- `QList<QAbstractButton *> buttons() const`
- `QAbstractButton * checkedButton() const`
- `int checkedId() const`
- `bool exclusive() const`
- `int id(QAbstractButton *button) const`
- `void removeButton(QAbstractButton *button)`
- `void setExclusive(bool)`
- `void setId(QAbstractButton *button, int id)`

### 信号

- `void buttonClicked(QAbstractButton *button)`
- `void buttonPressed(QAbstractButton *button)`
- `void buttonReleased(QAbstractButton *button)`
- `void buttonToggled(QAbstractButton *button, bool checked)`
- `void idClicked(int id)`
- `void idPressed(int id)`
- `void idReleased(int id)`
- `void idToggled(int id, bool checked)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `exclusive : bool`

**作用与语义：**

该属性决定按钮群是否互斥。
如果该属性`true`，那么组中任何时候只能勾选一个按钮。用户可以点击任意按钮来勾选，该钮会取代组内已有的勾选钮。
在排他组中，用户不能通过点击当前勾选的按钮来取消勾选;相反，必须点击组内的另一个按钮来设置该组的新勾选按钮。
默认情况下，该属性为`true`。

**如何使用：** 调用 `exclusive()` 读取当前值；它不会修改应用状态。

### `[explicit] QButtonGroup::QButtonGroup(QObject *parent = nullptr)`

**作用与语义：**

用给定的`parent`构建一个新的空按钮组。

### `[virtual noexcept] QButtonGroup::~QButtonGroup()`

**作用与语义：**

摧毁按钮组。

### `void QButtonGroup::addButton(QAbstractButton *button, int id = -1)`

**作用与语义：**

将给定的`button`添加到按钮组中。如果`id`为-1，按钮将被分配一个ID。自动分配的ID保证为负数，从-2开始。如果你自己分配ID，使用正值以避免冲突。

### `QAbstractButton *QButtonGroup::button(int id) const`

**作用与语义：**

返回指定`id`的按钮，若无该按钮则返回`nullptr`。

### `[signal] void QButtonGroup::buttonClicked(QAbstractButton *button)`

**作用与语义：**

当点击给定`button`时，该信号会发出。按钮在首次按下后松开、输入快捷键，或程序调用`QAbstractButton::click()`或`QAbstractButton::animateClick()`时被点击。

### `[signal] void QButtonGroup::buttonPressed(QAbstractButton *button)`

**作用与语义：**

当按下给定`button`时，该信号会发出。

### `[signal] void QButtonGroup::buttonReleased(QAbstractButton *button)`

**作用与语义：**

当释放给定`button`时，该信号会发出。

### `[signal] void QButtonGroup::buttonToggled(QAbstractButton *button, bool checked)`

**作用与语义：**

当该`button`被切换时发出该信号。如果按钮被勾选，`checked`为真;若按钮未勾选，则为假。

### `QList<QAbstractButton *> QButtonGroup::buttons() const`

**作用与语义：**

返回按钮组的按钮列表。这可能是空的。

### `QAbstractButton *QButtonGroup::checkedButton() const`

**作用与语义：**

返回按钮组的已勾选按钮，若未勾选按钮则返回`nullptr`。

### `int QButtonGroup::checkedId() const`

**作用与语义：**

返回`checkedButton()`的ID，如果未勾选按钮则返回-1。

### `int QButtonGroup::id(QAbstractButton *button) const`

**作用与语义：**

返回指定`button`的ID，如果没有该按钮则返回-1。

### `[signal] void QButtonGroup::idClicked(int id)`

**作用与语义：**

当按下带有指定`id`的按钮时，会发出该信号。

### `[signal] void QButtonGroup::idPressed(int id)`

**作用与语义：**

当按下带有该`id`的按钮时，会发出该信号。

### `[signal] void QButtonGroup::idReleased(int id)`

**作用与语义：**

当释放带有指定`id`的按钮时，该信号会发出。

### `[signal] void QButtonGroup::idToggled(int id, bool checked)`

**作用与语义：**

当按钮被切换到具有指定`id`时，该信号会发出。`checked`为真，若按钮未被勾选，则为假。

### `void QButtonGroup::removeButton(QAbstractButton *button)`

**作用与语义：**

将给定的`button`从按钮组中移除。

### `void QButtonGroup::setId(QAbstractButton *button, int id)`

**作用与语义：**

为指定`button`设定`id`。注意`id`不能是-1。

### `bool exclusive() const`

**作用与语义：**

该属性决定按钮群是否互斥。
如果该属性`true`，那么组中任何时候只能勾选一个按钮。用户可以点击任意按钮来勾选，该钮会取代组内已有的勾选钮。
在排他组中，用户不能通过点击当前勾选的按钮来取消勾选;相反，必须点击组内的另一个按钮来设置该组的新勾选按钮。
默认情况下，该属性为`true`。

**如何使用：** 调用 `exclusive()` 读取当前值；它不会修改应用状态。

### `void setExclusive(bool)`

**作用与语义：**

该属性决定按钮群是否互斥。
如果该属性`true`，那么组中任何时候只能勾选一个按钮。用户可以点击任意按钮来勾选，该钮会取代组内已有的勾选钮。
在排他组中，用户不能通过点击当前勾选的按钮来取消勾选;相反，必须点击组内的另一个按钮来设置该组的新勾选按钮。
默认情况下，该属性为`true`。

**如何使用：** 调用 `setExclusive(...)` 修改 `exclusive`；传入的新值会成为后续查询和相关界面行为所使用的值。

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

`QButtonGroup` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
