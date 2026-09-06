# QToolBox

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QToolBox` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QToolBox` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QToolBox>`
- 继承自：QFrame
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

- `count : int`
- `currentIndex : int`

### 公有函数

- `QToolBox(QWidget *parent = nullptr, Qt::WindowFlags f = Qt::WindowFlags())`
- `virtual ~QToolBox()`
- `int addItem(QWidget *widget, const QIcon &iconSet, const QString &text)`
- `int addItem(QWidget *w, const QString &text)`
- `int count() const`
- `int currentIndex() const`
- `QWidget * currentWidget() const`
- `int indexOf(const QWidget *widget) const`
- `int insertItem(int index, QWidget *widget, const QIcon &icon, const QString &text)`
- `int insertItem(int index, QWidget *widget, const QString &text)`
- `bool isItemEnabled(int index) const`
- `QIcon itemIcon(int index) const`
- `QString itemText(int index) const`
- `QString itemToolTip(int index) const`
- `void removeItem(int index)`
- `void setItemEnabled(int index, bool enabled)`
- `void setItemIcon(int index, const QIcon &icon)`
- `void setItemText(int index, const QString &text)`
- `void setItemToolTip(int index, const QString &toolTip)`
- `QWidget * widget(int index) const`

### 公有槽函数

- `void setCurrentIndex(int index)`
- `void setCurrentWidget(QWidget *widget)`

### 信号

- `void currentChanged(int index)`

### 保护函数

- `virtual void itemInserted(int index)`
- `virtual void itemRemoved(int index)`

### 重实现的保护函数

- `virtual void changeEvent(QEvent *ev) override`
- `virtual bool event(QEvent *e) override`
- `virtual void showEvent(QShowEvent *e) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[read-only] count : int`

**作用与语义：**

此属性保存工具箱中包含的项目数量。
默认情况下，该属性的值为 0。

**如何使用：** 调用 `count()` 读取当前值；它不会修改应用状态。

### `currentIndex : int`

**作用与语义：**

该属性包含当前项的索引。
默认情况下，对于空工具箱，该属性的值为-1。

**如何使用：** 调用 `currentIndex()` 读取当前值；它不会修改应用状态。

### `[explicit] QToolBox::QToolBox(QWidget *parent = nullptr, Qt::WindowFlags f = Qt::WindowFlags())`

**作用与语义：**

用给定的`parent`和标志构建一个新工具箱，`f`。

### `[virtual noexcept] QToolBox::~QToolBox()`

**作用与语义：**

毁掉工具箱。

### `int QToolBox::addItem(QWidget *widget, const QIcon &iconSet, const QString &text)`

**作用与语义：**

在工具箱底部的新标签页中添加`widget`。新标签的文本设置为`text`，`iconSet`显示在`text`左侧。返回新标签的索引。

### `int QToolBox::addItem(QWidget *w, const QString &text)`

**作用与语义：**

在工具箱底部的新标签页中添加小部件`w`。新标签页的文本设置为`text`。返回新标签页的索引。

### `[override virtual protected] void QToolBox::changeEvent(QEvent *ev)`

**作用与语义：**

重实现自：`QFrame::changeEvent`（QEvent *ev）。

### `[signal] void QToolBox::currentChanged(int index)`

**作用与语义：**

该属性包含当前项的索引。
默认情况下，对于空工具箱，该属性的值为-1。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `currentIndex` 的变化，不要把它当作普通函数主动调用。

### `QWidget *QToolBox::currentWidget() const`

**作用与语义：**

返回当前控件的指针，若无该项则返回`nullptr`。

### `[override virtual protected] bool QToolBox::event(QEvent *e)`

**作用与语义：**

重实现自：`QFrame::event`（QEvent *e）。

### `int QToolBox::indexOf(const QWidget *widget) const`

**作用与语义：**

返回`widget`的索引，如果该项不存在则返回-1。

### `int QToolBox::insertItem(int index, QWidget *widget, const QIcon &icon, const QString &text)`

**作用与语义：**

将`widget`插入在`index`位置，或者如果`index`超出范围，则插入工具箱底部。新物品的文本设置为`text`，`icon`显示在`text`左侧。返回新物品的索引。

### `int QToolBox::insertItem(int index, QWidget *widget, const QString &text)`

**作用与语义：**

将`widget`插入在工具箱的`index`位置，或者如果`index`超出范围，则插入工具箱底部。新物品的文本设置为`text`。返回新物品的索引。

### `bool QToolBox::isItemEnabled(int index) const`

**作用与语义：**

如果位置`index`的项被启用，返回`true`;否则返回`false`。

### `QIcon QToolBox::itemIcon(int index) const`

**作用与语义：**

返回位置`index`的物品图标，或者如果超出`index`范围，则返回空图标。

### `[virtual protected] void QToolBox::itemInserted(int index)`

**作用与语义：**

在添加或插入新项到位置`index`后调用该虚拟处理程序。

### `[virtual protected] void QToolBox::itemRemoved(int index)`

**作用与语义：**

该虚拟处理程序在物品从位置`index`移除后被调用。

### `QString QToolBox::itemText(int index) const`

**作用与语义：**

返回位置`index`的项目文本，若`index`超出范围则返回空字符串。

### `QString QToolBox::itemToolTip(int index) const`

**作用与语义：**

返回位置`index`的项目提示，如果`index`超出范围，则返回空字符串。

### `void QToolBox::removeItem(int index)`

**作用与语义：**

从工具箱中移除位于`index`的位置物品。注意该小部件并未被删除。

### `[slot] void QToolBox::setCurrentWidget(QWidget *widget)`

**作用与语义：**

Makes`widget` 是当前控件。`widget`必须是该工具箱中的一个项目。

### `void QToolBox::setItemEnabled(int index, bool enabled)`

**作用与语义：**

如果`enabled`为真，则位置`index`的项被启用;否则位置`index`项被禁用。

### `void QToolBox::setItemIcon(int index, const QIcon &icon)`

**作用与语义：**

将位置`index`的物品图标设置为`icon`。

### `void QToolBox::setItemText(int index, const QString &text)`

**作用与语义：**

将位置`index`的项目文本设置为`text`。
如果提供的文本包含&字符（'&'），会自动为其创建助记符。紧随“&”后的字符将用作快捷键。任何之前的助记符都会被覆盖，或者如果文本中没有定义助记词，则会被清除。详情请参见`QShortcut`文档（如需显示实际的&符号，请使用“&&”）。

### `void QToolBox::setItemToolTip(int index, const QString &toolTip)`

**作用与语义：**

将物品在位置`index`的工具提示设置为`toolTip`。

### `[override virtual protected] void QToolBox::showEvent(QShowEvent *e)`

**作用与语义：**

重实现自：`QWidget::showEvent`（QShowEvent *event）。
该事件处理程序可以在子类中重新实现，以接收传递给 `event` 参数的控件显示事件。
非自发的展示事件会在展示前立即发送到小部件。窗口的自发展示事件则在展示之后交付。
注意：当窗口系统改变其映射状态时，小部件会接收自发显示和隐藏事件，例如用户最小化窗口时自发隐藏事件，窗口恢复时自发显示事件。收到自发隐藏事件后，小部件仍被视为`isVisible()`可见。

### `QWidget *QToolBox::widget(int index) const`

**作用与语义：**

返回位置`index`的控件，若无该项则返回`nullptr`。

### `int count() const`

**作用与语义：**

此属性保存工具箱中包含的项目数量。
默认情况下，该属性的值为 0。

**如何使用：** 调用 `count()` 读取当前值；它不会修改应用状态。

### `int currentIndex() const`

**作用与语义：**

该属性包含当前项的索引。
默认情况下，对于空工具箱，该属性的值为-1。

**如何使用：** 调用 `currentIndex()` 读取当前值；它不会修改应用状态。

### `void setCurrentIndex(int index)`

**作用与语义：**

该属性包含当前项的索引。
默认情况下，对于空工具箱，该属性的值为-1。

**如何使用：** 调用 `setCurrentIndex(...)` 修改 `currentIndex`；传入的新值会成为后续查询和相关界面行为所使用的值。

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

`QToolBox` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
