# QPushButton

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QPushButton` 是执行命令的矩形按钮，用户点击、按空格或触发快捷键时发出 clicked()。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QPushButton` 是执行命令的矩形按钮，用户点击、按空格或触发快捷键时发出 clicked()。

**内部模型：** 按钮的核心是“触发动作”，不是保存业务状态。按钮负责展示文本/图标、启用状态和可选的默认按钮行为；真正的业务逻辑应连接 clicked() 到窗口或 controller。

**适用场景：** 确定、取消、保存、打开、应用和帮助等离散命令使用 QPushButton；需要小图标工具按钮、连续按压或主要用于切换状态时应考虑 QToolButton/QCheckBox。

**典型调用链：** 创建按钮 -> 设置 text/icon/enabled -> 加入 layout 或 dialog -> connect(clicked) -> 在槽中执行业务动作并更新按钮状态。

**先记住的坑：** 不要在 clicked 槽里做长时间阻塞任务；区分 clicked、pressed、released 和 toggled；对话框中的 default/autoDefault 会影响 Enter 行为。

## 2. 依赖与对象关系

- 头文件：`#include <QPushButton>`
- 继承自：QAbstractButton
- 直接派生类：QCommandLinkButton

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

按钮的核心是“触发动作”，不是保存业务状态。按钮负责展示文本/图标、启用状态和可选的默认按钮行为；真正的业务逻辑应连接 clicked() 到窗口或 controller。

### 状态、生命周期和线程

**生命周期：** 控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

**状态与结果：** 控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

**线程与事件循环：** 所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

## 3. 直接使用

确定、取消、保存、打开、应用和帮助等离散命令使用 QPushButton；需要小图标工具按钮、连续按压或主要用于切换状态时应考虑 QToolButton/QCheckBox。 使用时通常按这个过程组织：创建按钮 -> 设置 text/icon/enabled -> 加入 layout 或 dialog -> connect(clicked) -> 在槽中执行业务动作并更新按钮状态。

```cpp
#include <QPushButton>
#include <QVBoxLayout>
#include <QWidget>

QWidget panel;
auto *button = new QPushButton(QObject::tr("Save"), &panel);
auto *layout = new QVBoxLayout(&panel);
layout->addWidget(button);
QObject::connect(button, &QPushButton::clicked, &panel, [&panel] {
    panel.setWindowTitle(QObject::tr("Saved"));
});
panel.show();
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 属性

- `autoDefault : bool`
- `default : bool`
- `flat : bool`

### 公有函数

- `QPushButton(QWidget *parent = nullptr)`
- `QPushButton(const QString &text, QWidget *parent = nullptr)`
- `QPushButton(const QIcon &icon, const QString &text, QWidget *parent = nullptr)`
- `virtual ~QPushButton()`
- `bool autoDefault() const`
- `bool isDefault() const`
- `bool isFlat() const`
- `QMenu * menu() const`
- `void setAutoDefault(bool)`
- `void setDefault(bool)`
- `void setFlat(bool)`
- `void setMenu(QMenu *menu)`

### 重实现的公有函数

- `virtual QSize minimumSizeHint() const override`
- `virtual QSize sizeHint() const override`

### 公有槽函数

- `void showMenu()`

### 保护函数

- `virtual void initStyleOption(QStyleOptionButton *option) const`

### 重实现的保护函数

- `virtual bool event(QEvent *e) override`
- `virtual void focusInEvent(QFocusEvent *e) override`
- `virtual void focusOutEvent(QFocusEvent *e) override`
- `virtual bool hitButton(const QPoint &pos) const override`
- `virtual void keyPressEvent(QKeyEvent *e) override`
- `virtual void mouseMoveEvent(QMouseEvent *e) override`
- `virtual void paintEvent(QPaintEvent *) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `autoDefault : bool`

**作用与语义：**

该属性决定了按钮是否为自动默认按钮。
如果该属性设置为true，那么按钮就是自动默认按钮。
在某些图形界面样式中，默认按钮会被绘制并额外加一帧，最多可达3像素或更多。Qt会自动在自动默认按钮周围保持该空间空闲，即自动默认按钮的尺寸提示可能稍大。
该属性的默认为具有`QDialog`父的按钮为真;否则默认为假。
有关`default`与自动违约如何相互作用，请参见`default`属性。

**如何使用：** 调用 `autoDefault()` 读取当前值；它不会修改应用状态。

### `default : bool`

**作用与语义：**

该属性决定了按键是否为默认按钮。
默认和自动默认按钮决定用户在对话框中按下回车键时会发生什么。
当该属性设置为true（即对话框默认按钮）的按钮，用户按下回车时会自动按下，但有一个例外：如果`autoDefault`按钮当前有对焦，则按`autoDefault`键。当对话框中有`autoDefault`按钮但没有默认按钮时，按回车会按下当前有对焦的`autoDefault`按钮，或者如果没有对焦按钮，则按下对焦链中的下一个`autoDefault`按钮。
在对话框中，默认按钮一次只能有一个。该按钮随后会以额外的帧（取决于图形界面样式）显示。
默认按键行为仅在对话框中提供。当按钮聚焦时，按空格键始终可从键盘上点击。
如果当前默认按钮的默认属性在对话框可见时被设置为false，下一次对话框中的按钮被聚焦时，会自动分配新的默认属性。
该属性的默认值为假。

**如何使用：** 调用 `default()` 读取当前值；它不会修改应用状态。

### `flat : bool`

**作用与语义：**

该属性是否会显示按钮边框是否被抬起。
该属性的默认为 false。如果设置了该属性，大多数样式不会在按钮被按下时绘制背景。`setAutoFillBackground()` 可以用 `QPalette::Button` 画刷确保背景被填充。

**如何使用：** 调用 `flat()` 读取当前值；它不会修改应用状态。

### `[explicit] QPushButton::QPushButton(QWidget *parent = nullptr)`

**作用与语义：**

构建了一个没有文字和`parent`的按钮。

### `[explicit] QPushButton::QPushButton(const QString &text, QWidget *parent = nullptr)`

**作用与语义：**

构建一个带有父`parent`和文本`text`的按钮。

### `QPushButton::QPushButton(const QIcon &icon, const QString &text, QWidget *parent = nullptr)`

**作用与语义：**

制造一个带有`icon`和`text`和`parent`的按钮。
注意，你也可以将`QPixmap`对象作为图标传递（这得益于 C 提供的隐式类型转换）。

### `[virtual noexcept] QPushButton::~QPushButton()`

**作用与语义：**

摧毁按钮。

### `[override virtual protected] bool QPushButton::event(QEvent *e)`

**作用与语义：**

重实现自：`QAbstractButton::event`（QEvent *e）。

### `[override virtual protected] void QPushButton::focusInEvent(QFocusEvent *e)`

**作用与语义：**

重实现自：`QAbstractButton::focusInEvent`（QFocusEvent *e）。

### `[override virtual protected] void QPushButton::focusOutEvent(QFocusEvent *e)`

**作用与语义：**

重实现自：`QAbstractButton::focusOutEvent`（QFocusEvent *e）。

### `[override virtual protected] bool QPushButton::hitButton(const QPoint &pos) const`

**作用与语义：**

重装：`QAbstractButton::hitButton`（const QPoint & pos） const.
如果`pos`在可点击的按钮矩形内，返回`true`;否则返回`false`。
默认情况下，可点击区域是整个小部件。子类可能会重新实现此功能，以支持不同形状和大小的可点击区域。

### `[virtual protected] void QPushButton::initStyleOption(QStyleOptionButton *option) const`

**作用与语义：**

用这个`QPushButton`的值初始化`option`。这种方法适用于需要 `QStyleOptionButton`但不想自己填满所有信息的子类。

### `[override virtual protected] void QPushButton::keyPressEvent(QKeyEvent *e)`

**作用与语义：**

重实现自：`QAbstractButton::keyPressEvent`（QKeyEvent *e）。

### `QMenu *QPushButton::menu() const`

**作用与语义：**

如果没有设置弹出菜单，则返回按钮相关的弹出菜单或`nullptr`。

### `[override virtual] QSize QPushButton::minimumSizeHint() const`

**作用与语义：**

重新实现属性的访问函数：`QWidget::minimumSizeHint`。

### `[override virtual protected] void QPushButton::mouseMoveEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QAbstractButton::mouseMoveEvent`（QMouseEvent *e）。

### `[override virtual protected] void QPushButton::paintEvent(QPaintEvent *)`

**作用与语义：**

重构：`QAbstractButton::paintEvent`（QPaintEvent *e）。

### `void QPushButton::setMenu(QMenu *menu)`

**作用与语义：**

将弹出菜单`menu`与该按钮关联。这会将按钮变成菜单按钮，在某些风格中，按钮文本右侧会出现一个小三角形。
菜单的所有权不会转移到按钮上。
一个带有弹出菜单的按钮，采用Fusion小部件风格。

### `[slot] void QPushButton::showMenu()`

**作用与语义：**

显示（弹出）相关的弹出菜单。如果没有这样的菜单，这个功能就不会有任何作用。直到用户关闭弹出菜单后，这个功能才会返回。

### `[override virtual] QSize QPushButton::sizeHint() const`

**作用与语义：**

重新实现了属性的访问函数：`QWidget::sizeHint`。

### `bool autoDefault() const`

**作用与语义：**

该属性决定了按钮是否为自动默认按钮。
如果该属性设置为true，那么按钮就是自动默认按钮。
在某些图形界面样式中，默认按钮会被绘制并额外加一帧，最多可达3像素或更多。Qt会自动在自动默认按钮周围保持该空间空闲，即自动默认按钮的尺寸提示可能稍大。
该属性的默认为具有`QDialog`父的按钮为真;否则默认为假。
有关`default`与自动违约如何相互作用，请参见`default`属性。

**如何使用：** 调用 `autoDefault()` 读取当前值；它不会修改应用状态。

### `bool isDefault() const`

**作用与语义：**

该属性决定了按键是否为默认按钮。
默认和自动默认按钮决定用户在对话框中按下回车键时会发生什么。
当该属性设置为true（即对话框默认按钮）的按钮，用户按下回车时会自动按下，但有一个例外：如果`autoDefault`按钮当前有对焦，则按`autoDefault`键。当对话框中有`autoDefault`按钮但没有默认按钮时，按回车会按下当前有对焦的`autoDefault`按钮，或者如果没有对焦按钮，则按下对焦链中的下一个`autoDefault`按钮。
在对话框中，默认按钮一次只能有一个。该按钮随后会以额外的帧（取决于图形界面样式）显示。
默认按键行为仅在对话框中提供。当按钮聚焦时，按空格键始终可从键盘上点击。
如果当前默认按钮的默认属性在对话框可见时被设置为false，下一次对话框中的按钮被聚焦时，会自动分配新的默认属性。
该属性的默认值为假。

**如何使用：** 调用 `isDefault()` 读取当前值；它不会修改应用状态。

### `bool isFlat() const`

**作用与语义：**

该属性是否会显示按钮边框是否被抬起。
该属性的默认为 false。如果设置了该属性，大多数样式不会在按钮被按下时绘制背景。`setAutoFillBackground()` 可以用 `QPalette::Button` 画刷确保背景被填充。

**如何使用：** 调用 `isFlat()` 读取当前值；它不会修改应用状态。

### `void setAutoDefault(bool)`

**作用与语义：**

该属性决定了按钮是否为自动默认按钮。
如果该属性设置为true，那么按钮就是自动默认按钮。
在某些图形界面样式中，默认按钮会被绘制并额外加一帧，最多可达3像素或更多。Qt会自动在自动默认按钮周围保持该空间空闲，即自动默认按钮的尺寸提示可能稍大。
该属性的默认为具有`QDialog`父的按钮为真;否则默认为假。
有关`default`与自动违约如何相互作用，请参见`default`属性。

**如何使用：** 调用 `setAutoDefault(...)` 修改 `autoDefault`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setDefault(bool)`

**作用与语义：**

该属性决定了按键是否为默认按钮。
默认和自动默认按钮决定用户在对话框中按下回车键时会发生什么。
当该属性设置为true（即对话框默认按钮）的按钮，用户按下回车时会自动按下，但有一个例外：如果`autoDefault`按钮当前有对焦，则按`autoDefault`键。当对话框中有`autoDefault`按钮但没有默认按钮时，按回车会按下当前有对焦的`autoDefault`按钮，或者如果没有对焦按钮，则按下对焦链中的下一个`autoDefault`按钮。
在对话框中，默认按钮一次只能有一个。该按钮随后会以额外的帧（取决于图形界面样式）显示。
默认按键行为仅在对话框中提供。当按钮聚焦时，按空格键始终可从键盘上点击。
如果当前默认按钮的默认属性在对话框可见时被设置为false，下一次对话框中的按钮被聚焦时，会自动分配新的默认属性。
该属性的默认值为假。

**如何使用：** 调用 `setDefault(...)` 修改 `default`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setFlat(bool)`

**作用与语义：**

该属性是否会显示按钮边框是否被抬起。
该属性的默认为 false。如果设置了该属性，大多数样式不会在按钮被按下时绘制背景。`setAutoFillBackground()` 可以用 `QPalette::Button` 画刷确保背景被填充。

**如何使用：** 调用 `setFlat(...)` 修改 `flat`；传入的新值会成为后续查询和相关界面行为所使用的值。

## 6. 深入实践与常见坑

### 生命周期和资源边界

控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

### 状态和错误边界

控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

### 线程边界

所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

### 最容易出现的错误

不要在 clicked 槽里做长时间阻塞任务；区分 clicked、pressed、released 和 toggled；对话框中的 default/autoDefault 会影响 Enter 行为。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QPushButton` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
