# QCheckBox

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QCheckBox` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QCheckBox` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QCheckBox>`
- 继承自：QAbstractButton
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

- `tristate : bool`

### 公有函数

- `QCheckBox(QWidget *parent = nullptr)`
- `QCheckBox(const QString &text, QWidget *parent = nullptr)`
- `virtual ~QCheckBox()`
- `Qt::CheckState checkState() const`
- `bool isTristate() const`
- `void setCheckState(Qt::CheckState state)`
- `void setTristate(bool y = true)`

### 重实现的公有函数

- `virtual QSize minimumSizeHint() const override`
- `virtual QSize sizeHint() const override`

### 信号

- `(since 6.7) void checkStateChanged(Qt::CheckState state)`

### 保护函数

- `virtual void initStyleOption(QStyleOptionButton *option) const`

### 重实现的保护函数

- `virtual void checkStateSet() override`
- `virtual bool event(QEvent *e) override`
- `virtual bool hitButton(const QPoint &pos) const override`
- `virtual void mouseMoveEvent(QMouseEvent *e) override`
- `virtual void nextCheckState() override`
- `virtual void paintEvent(QPaintEvent *) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `tristate : bool`

**作用与语义：**

该属性确定复选框是否为三态复选框。
默认为假，即复选框只有两个状态。

**如何使用：** 调用 `tristate()` 读取当前值；它不会修改应用状态。

### `[explicit] QCheckBox::QCheckBox(QWidget *parent = nullptr)`

**作用与语义：**

构建一个包含给定`parent`的复选框，但不含文本。
`parent`传递给`QAbstractButton`构造器。

### `[explicit] QCheckBox::QCheckBox(const QString &text, QWidget *parent = nullptr)`

**作用与语义：**

构造一个包含给定`parent`和 `text`的复选框。
`parent`传递给`QAbstractButton`构造者。

### `[virtual noexcept] QCheckBox::~QCheckBox()`

**作用与语义：**

毁灭者。

### `Qt::CheckState QCheckBox::checkState() const`

**作用与语义：**

返回复选框的检查状态。如果你不需要三态支持，也可以使用`QAbstractButton::isChecked()`，返回布尔值。

### `[signal, since 6.7] void QCheckBox::checkStateChanged(Qt::CheckState state)`

**作用与语义：**

每当复选框状态发生变化，即用户勾选或取消勾选时，都会发出该信号。
`state`包含了复选框的新`Qt::CheckState`。

### `[override virtual protected] void QCheckBox::checkStateSet()`

**作用与语义：**

重装：`QAbstractButton::checkStateSet()`。
当使用 `setChecked()` 时调用该虚拟处理器，除非在 `nextCheckState()` 内部调用。它允许子类重置其中间按钮状态。

### `[override virtual protected] bool QCheckBox::event(QEvent *e)`

**作用与语义：**

重实现自：`QAbstractButton::event`（QEvent *e）。

### `[override virtual protected] bool QCheckBox::hitButton(const QPoint &pos) const`

**作用与语义：**

重装：`QAbstractButton::hitButton`（const QPoint & pos） const.
如果`pos`在可点击的按钮矩形内，返回`true`;否则返回`false`。
默认情况下，可点击区域是整个小部件。子类可能会重新实现此功能，以支持不同形状和大小的可点击区域。

### `[virtual protected] void QCheckBox::initStyleOption(QStyleOptionButton *option) const`

**作用与语义：**

用该`QCheckBox`的值初始化`option`。该方法适用于需要`QStyleOptionButton`但不想自行填充所有信息的子类。

### `[override virtual] QSize QCheckBox::minimumSizeHint() const`

**作用与语义：**

重新实现属性的访问函数：`QWidget::minimumSizeHint`。

### `[override virtual protected] void QCheckBox::mouseMoveEvent(QMouseEvent *e)`

**作用与语义：**

重实现自：`QAbstractButton::mouseMoveEvent`（QMouseEvent *e）。

### `[override virtual protected] void QCheckBox::nextCheckState()`

**作用与语义：**

重装：`QAbstractButton::nextCheckState()`。
当按钮被点击时调用这个虚拟处理器。默认实现调用`setChecked`（！`isChecked()`），如果按钮`isCheckable()`。它允许子类实现中间按钮状态。

### `[override virtual protected] void QCheckBox::paintEvent(QPaintEvent *)`

**作用与语义：**

重构：`QAbstractButton::paintEvent`（QPaintEvent *e）。

### `void QCheckBox::setCheckState(Qt::CheckState state)`

**作用与语义：**

将复选框的检查状态设置为`state`。如果你不需要三态支持，也可以使用`QAbstractButton::setChecked()`，这需要布尔值。

### `[override virtual] QSize QCheckBox::sizeHint() const`

**作用与语义：**

重新实现了属性的访问函数：`QWidget::sizeHint`。

### `bool isTristate() const`

**作用与语义：**

该属性确定复选框是否为三态复选框。
默认为假，即复选框只有两个状态。

**如何使用：** 调用 `isTristate()` 读取当前值；它不会修改应用状态。

### `void setTristate(bool y = true)`

**作用与语义：**

该属性确定复选框是否为三态复选框。
默认为假，即复选框只有两个状态。

**如何使用：** 调用 `setTristate(...)` 修改 `tristate`；传入的新值会成为后续查询和相关界面行为所使用的值。

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

`QCheckBox` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
