# QAbstractSlider

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QAbstractSlider` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QAbstractSlider` 是 Qt Widgets 中的抽象协议类型，通常通过具体子类、模型、插件或工厂来使用。

**内部模型：** 抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

**适用场景：** 当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。

**典型调用链：** 选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。

**先记住的坑：** 不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

## 2. 依赖与对象关系

- 头文件：`#include <QAbstractSlider>`
- 继承自：QWidget
- 直接派生类：QDial、QScrollBar,、QSlider

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

### 状态、生命周期和线程

**生命周期：** 控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

**状态与结果：** 控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

**线程与事件循环：** 所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

## 3. 直接使用

当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。 使用时通常按这个过程组织：选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum SliderAction { SliderNoAction, SliderSingleStepAdd, SliderSingleStepSub, SliderPageStepAdd, SliderPageStepSub, …, SliderMove }`

### 属性

- `invertedAppearance : bool`
- `invertedControls : bool`
- `maximum : int`
- `minimum : int`
- `orientation : Qt::Orientation`
- `pageStep : int`
- `singleStep : int`
- `sliderDown : bool`
- `sliderPosition : int`
- `tracking : bool`
- `value : int`

### 公有函数

- `QAbstractSlider(QWidget *parent = nullptr)`
- `virtual ~QAbstractSlider()`
- `bool hasTracking() const`
- `bool invertedAppearance() const`
- `bool invertedControls() const`
- `bool isSliderDown() const`
- `int maximum() const`
- `int minimum() const`
- `Qt::Orientation orientation() const`
- `int pageStep() const`
- `void setInvertedAppearance(bool)`
- `void setInvertedControls(bool)`
- `void setMaximum(int)`
- `void setMinimum(int)`
- `void setPageStep(int)`
- `void setSingleStep(int)`
- `void setSliderDown(bool)`
- `void setSliderPosition(int)`
- `void setTracking(bool enable)`
- `int singleStep() const`
- `int sliderPosition() const`
- `void triggerAction(QAbstractSlider::SliderAction action)`
- `int value() const`

### 公有槽函数

- `void setOrientation(Qt::Orientation)`
- `void setRange(int min, int max)`
- `void setValue(int)`

### 信号

- `void actionTriggered(int action)`
- `void rangeChanged(int min, int max)`
- `void sliderMoved(int value)`
- `void sliderPressed()`
- `void sliderReleased()`
- `void valueChanged(int value)`

### 保护函数

- `QAbstractSlider::SliderAction repeatAction() const`
- `void setRepeatAction(QAbstractSlider::SliderAction action, int thresholdTime = 500, int repeatTime = 50)`
- `virtual void sliderChange(QAbstractSlider::SliderChange change)`

### 重实现的保护函数

- `virtual void changeEvent(QEvent *ev) override`
- `virtual bool event(QEvent *e) override`
- `virtual void keyPressEvent(QKeyEvent *ev) override`
- `virtual void timerEvent(QTimerEvent *e) override`
- `virtual void wheelEvent(QWheelEvent *e) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `invertedAppearance : bool`

**作用与语义：**

无论滑块是否显示其数值反转，这一属性都成立。
如果该属性为`false`（默认），则最小值和最大值会显示在继承的控件的经典位置。如果值为真，最小值和最大值则出现在它们相反的位置。
注意：该特性对滑块和旋钮最为合理。对于滚动条，滚动条子控制的视觉效果取决于样式是否理解反转外观;大多数样式忽略了滚动条的这一特性。

**如何使用：** 调用 `invertedAppearance()` 读取当前值；它不会修改应用状态。

### `invertedControls : bool`

**作用与语义：**

该属性无论滑块是否反转其轮子和键事件，都成立。
如果`false`，滚动鼠标滚轮“向上”并使用“page up”等键，可以将滑块值增加到最大值。否则按页面向上会让值向滑块最小值移动。

**如何使用：** 调用 `invertedControls()` 读取当前值；它不会修改应用状态。

### `maximum : int`

**作用与语义：**

该属性表示滑块的最大值。
设置该属性时，必要时会调整`minimum`以确保范围有效。滑块当前值也会调整到新范围内。

**如何使用：** 调用 `maximum()` 读取当前值；它不会修改应用状态。

### `minimum : int`

**作用与语义：**

该属性表示滑块的最小值。
设置该属性时，必要时会调整`maximum`以确保范围有效。滑块当前值也会调整到新范围内。

**如何使用：** 调用 `minimum()` 读取当前值；它不会修改应用状态。

### `orientation : Qt::Orientation`

**作用与语义：**

此属性保存滑块的方向。
方向必须为 `Qt::Vertical`（默认值）或 `Qt::Horizontal`。

**如何使用：** 调用 `orientation()` 读取当前值；它不会修改应用状态。

### `pageStep : int`

**作用与语义：**

该属性包含页步。
抽象滑块提供的两个自然步骤中较大的，通常对应用户按下PageUp或PageDown。

**如何使用：** 调用 `pageStep()` 读取当前值；它不会修改应用状态。

### `singleStep : int`

**作用与语义：**

该属性表示单步。
抽象滑块提供的两个自然步骤中较小的，通常对应于用户按下方向键。
如果在自动重复按键事件期间该属性被修改，行为则未定义。

**如何使用：** 调用 `singleStep()` 读取当前值；它不会修改应用状态。

### `sliderDown : bool`

**作用与语义：**

该属性无论滑块是否按下都成立。
该属性由子类设置，以便抽象滑块知道`tracking`是否会产生影响。
更改滑块向下属性会发出`sliderPressed()`和`sliderReleased()`信号。

**如何使用：** 调用 `sliderDown()` 读取当前值；它不会修改应用状态。

### `sliderPosition : int`

**作用与语义：**

该特性保持当前滑块位置。
如果启用`tracking`（默认），这和`value`是一样的。

**如何使用：** 调用 `sliderPosition()` 读取当前值；它不会修改应用状态。

### `tracking : bool`

**作用与语义：**

该属性适用于是否启用滑块跟踪。
如果启用了跟踪（默认），滑块在拖动时会发出`valueChanged()`信号。如果禁用跟踪，只有在用户松开滑块时，滑块才会发出`valueChanged()`信号。

**如何使用：** 调用 `tracking()` 读取当前值；它不会修改应用状态。

### `value : int`

**作用与语义：**

该属性表示滑块当前值。
滑块强制值在法定范围内：`minimum` <= `value` <= `maximum`。
改变数值也会影响`sliderPosition`。

**如何使用：** 调用 `value()` 读取当前值；它不会修改应用状态。

### `[explicit] QAbstractSlider::QAbstractSlider(QWidget *parent = nullptr)`

**作用与语义：**

构造一个抽象滑块。
`parent`参数被发送给`QWidget`构造器。
`minimum`默认为0，`maximum`为99，`singleStep`大小为1，`pageStep`大小为10，初始的 `value`为0。

### `[virtual noexcept] QAbstractSlider::~QAbstractSlider()`

**作用与语义：**

破坏滑球。

### `[signal] void QAbstractSlider::actionTriggered(int action)`

**作用与语义：**

当滑块动作`action`被触发时，该信号会发出。动作包括`SliderSingleStepAdd`、`SliderSingleStepSub`、`SliderPageStepAdd`、`SliderPageStepSub`、`SliderToMinimum`、`SliderToMaximum`和`SliderMove`。
当信号发出时，`sliderPosition`已根据动作调整，但`value`尚未传播（即`valueChanged()`信号尚未发出），视觉显示也未更新。在连接到该信号的槽位中，你可以根据动作和滑块值，自己调用`setSliderPosition()`安全调整任何动作。

### `[override virtual protected] void QAbstractSlider::changeEvent(QEvent *ev)`

**作用与语义：**

重装：`QWidget::changeEvent`（QEvent *事件）。
该事件处理程序可以重新实现以处理状态变化。
该事件中被更改的状态可以通过提供的`event`检索。
变更事件包括：`QEvent::ToolBarChange`、`QEvent::ActivationChange`、`QEvent::EnabledChange`、`QEvent::FontChange`、`QEvent::StyleChange`、`QEvent::PaletteChange`、`QEvent::WindowTitleChange`、`QEvent::IconTextChange`、`QEvent::ModifiedChange`、`QEvent::MouseTrackingChange`、`QEvent::ParentChange`、`QEvent::WindowStateChange`、`QEvent::LanguageChange`、`QEvent::LocaleChange`、`QEvent::LayoutDirectionChange`、`QEvent::ReadOnlyChange`。

### `[override virtual protected] bool QAbstractSlider::event(QEvent *e)`

**作用与语义：**

重实现自：`QWidget::event`（QEvent *事件）。

### `[override virtual protected] void QAbstractSlider::keyPressEvent(QKeyEvent *ev)`

**作用与语义：**

重实现自：`QWidget::keyPressEvent`（QKeyEvent *event）。
该事件处理程序用于事件`event`，可以在子类中重新实现，以接收该控件的按键事件。
一个小部件必须调用`setFocusPolicy()`先接受焦点，并且必须有焦点才能接收按键事件。
如果你重新实现这个处理器，如果你不对密钥进行操作，务必调用基类实现。
默认实现会关闭弹出小部件，如果用户按下`QKeySequence::Cancel`的按键序列（通常是 Escape 键）。否则事件会被忽略，以便小部件的父节点能够解释。
注意`QKeyEvent`以 isAccepted() == true 开头，所以你不需要调用 `QKeyEvent::accept()`——只要你对该键执行时不要调用基类实现即可。

### `[signal] void QAbstractSlider::rangeChanged(int min, int max)`

**作用与语义：**

当滑块范围发生变化时，`min`为新的最小值，`max`为新的最大值，这个信号会发出来。

### `[protected] QAbstractSlider::SliderAction QAbstractSlider::repeatAction() const`

**作用与语义：**

返回当前的重复动作。

### `[slot] void QAbstractSlider::setRange(int min, int max)`

**作用与语义：**

将滑块的最小值设为`min`，最大值设为`max`。
如果`max`小于`min`，`min`就成为唯一的法律价值。

### `[protected] void QAbstractSlider::setRepeatAction(QAbstractSlider::SliderAction action, int thresholdTime = 500, int repeatTime = 50)`

**作用与语义：**

动作组`action`在初始延迟`thresholdTime`后，以`repeatTime`为间隔重复触发。

### `[virtual protected] void QAbstractSlider::sliderChange(QAbstractSlider::SliderChange change)`

**作用与语义：**

重新实现该虚拟函数以跟踪滑块变化，如`SliderRangeChange`、`SliderOrientationChange`、`SliderStepsChange`或`SliderValueChange`。默认实现仅更新显示，忽略`change`参数。

### `[signal] void QAbstractSlider::sliderMoved(int value)`

**作用与语义：**

该特性保持当前滑块位置。
如果启用`tracking`（默认），这和`value`是一样的。

**如何使用：** 调用 `sliderMoved()` 读取当前值；它不会修改应用状态。

### `[signal] void QAbstractSlider::sliderPressed()`

**作用与语义：**

当用户用鼠标按下滑块时，或在调用`setSliderDown`（true）时，程序性地会发出该信号。

### `[signal] void QAbstractSlider::sliderReleased()`

**作用与语义：**

当用户用鼠标松开滑块时，或在调用`setSliderDown`（false）时，通过程序方式发出该信号。

### `[override virtual protected] void QAbstractSlider::timerEvent(QTimerEvent *e)`

**作用与语义：**

重实现自：`QObject::timerEvent`（QTimerEvent *event）。

### `void QAbstractSlider::triggerAction(QAbstractSlider::SliderAction action)`

**作用与语义：**

触发滑块`action`。可能的动作有`SliderSingleStepAdd`、`SliderSingleStepSub`、`SliderPageStepAdd`、`SliderPageStepSub`、`SliderToMinimum`、`SliderToMaximum`和`SliderMove`。

### `[signal] void QAbstractSlider::valueChanged(int value)`

**作用与语义：**

该属性表示滑块当前值。
滑块强制值在法定范围内：`minimum` <= `value` <= `maximum`。
改变数值也会影响`sliderPosition`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `value` 的变化，不要把它当作普通函数主动调用。

### `[override virtual protected] void QAbstractSlider::wheelEvent(QWheelEvent *e)`

**作用与语义：**

重实现自：`QWidget::wheelEvent`（QWheelEvent *event）。
该事件处理程序用于事件`event`，可以在子类中重新实现，以接收该控件的轮事件。
如果你重新实现了这个处理程序，非常重要的是，如果你不处理事件，必须`ignore()`事件，这样小部件的父节点才能解释它。
默认实现会忽略该事件。

### `enum SliderAction { SliderNoAction, SliderSingleStepAdd, SliderSingleStepSub, SliderPageStepAdd, SliderPageStepSub, …, SliderMove }`

**作用与语义：**

表示要对滑块执行的逻辑动作，包括不操作、单步加减、整页加减、跳到最小/最大值以及移动到指定位置。把它传给 `triggerAction()` 会按范围、步长和反向设置更新值，并触发相应信号。

### `bool hasTracking() const`

**作用与语义：**

该属性适用于是否启用滑块跟踪。
如果启用了跟踪（默认），滑块在拖动时会发出`valueChanged()`信号。如果禁用跟踪，只有在用户松开滑块时，滑块才会发出`valueChanged()`信号。

**如何使用：** 调用 `hasTracking()` 读取当前值；它不会修改应用状态。

### `bool invertedAppearance() const`

**作用与语义：**

无论滑块是否显示其数值反转，这一属性都成立。
如果该属性为`false`（默认），则最小值和最大值会显示在继承的控件的经典位置。如果值为真，最小值和最大值则出现在它们相反的位置。
注意：该特性对滑块和旋钮最为合理。对于滚动条，滚动条子控制的视觉效果取决于样式是否理解反转外观;大多数样式忽略了滚动条的这一特性。

**如何使用：** 调用 `invertedAppearance()` 读取当前值；它不会修改应用状态。

### `bool invertedControls() const`

**作用与语义：**

该属性无论滑块是否反转其轮子和键事件，都成立。
如果`false`，滚动鼠标滚轮“向上”并使用“page up”等键，可以将滑块值增加到最大值。否则按页面向上会让值向滑块最小值移动。

**如何使用：** 调用 `invertedControls()` 读取当前值；它不会修改应用状态。

### `bool isSliderDown() const`

**作用与语义：**

该属性无论滑块是否按下都成立。
该属性由子类设置，以便抽象滑块知道`tracking`是否会产生影响。
更改滑块向下属性会发出`sliderPressed()`和`sliderReleased()`信号。

**如何使用：** 调用 `isSliderDown()` 读取当前值；它不会修改应用状态。

### `int maximum() const`

**作用与语义：**

该属性表示滑块的最大值。
设置该属性时，必要时会调整`minimum`以确保范围有效。滑块当前值也会调整到新范围内。

**如何使用：** 调用 `maximum()` 读取当前值；它不会修改应用状态。

### `int minimum() const`

**作用与语义：**

该属性表示滑块的最小值。
设置该属性时，必要时会调整`maximum`以确保范围有效。滑块当前值也会调整到新范围内。

**如何使用：** 调用 `minimum()` 读取当前值；它不会修改应用状态。

### `Qt::Orientation orientation() const`

**作用与语义：**

此属性保存滑块的方向。
方向必须为 `Qt::Vertical`（默认值）或 `Qt::Horizontal`。

**如何使用：** 调用 `orientation()` 读取当前值；它不会修改应用状态。

### `int pageStep() const`

**作用与语义：**

该属性包含页步。
抽象滑块提供的两个自然步骤中较大的，通常对应用户按下PageUp或PageDown。

**如何使用：** 调用 `pageStep()` 读取当前值；它不会修改应用状态。

### `void setInvertedAppearance(bool)`

**作用与语义：**

无论滑块是否显示其数值反转，这一属性都成立。
如果该属性为`false`（默认），则最小值和最大值会显示在继承的控件的经典位置。如果值为真，最小值和最大值则出现在它们相反的位置。
注意：该特性对滑块和旋钮最为合理。对于滚动条，滚动条子控制的视觉效果取决于样式是否理解反转外观;大多数样式忽略了滚动条的这一特性。

**如何使用：** 调用 `setInvertedAppearance(...)` 修改 `invertedAppearance`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setInvertedControls(bool)`

**作用与语义：**

该属性无论滑块是否反转其轮子和键事件，都成立。
如果`false`，滚动鼠标滚轮“向上”并使用“page up”等键，可以将滑块值增加到最大值。否则按页面向上会让值向滑块最小值移动。

**如何使用：** 调用 `setInvertedControls(...)` 修改 `invertedControls`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMaximum(int)`

**作用与语义：**

该属性表示滑块的最大值。
设置该属性时，必要时会调整`minimum`以确保范围有效。滑块当前值也会调整到新范围内。

**如何使用：** 调用 `setMaximum(...)` 修改 `maximum`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMinimum(int)`

**作用与语义：**

该属性表示滑块的最小值。
设置该属性时，必要时会调整`maximum`以确保范围有效。滑块当前值也会调整到新范围内。

**如何使用：** 调用 `setMinimum(...)` 修改 `minimum`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setPageStep(int)`

**作用与语义：**

该属性包含页步。
抽象滑块提供的两个自然步骤中较大的，通常对应用户按下PageUp或PageDown。

**如何使用：** 调用 `setPageStep(...)` 修改 `pageStep`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setSingleStep(int)`

**作用与语义：**

该属性表示单步。
抽象滑块提供的两个自然步骤中较小的，通常对应于用户按下方向键。
如果在自动重复按键事件期间该属性被修改，行为则未定义。

**如何使用：** 调用 `setSingleStep(...)` 修改 `singleStep`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setSliderDown(bool)`

**作用与语义：**

该属性无论滑块是否按下都成立。
该属性由子类设置，以便抽象滑块知道`tracking`是否会产生影响。
更改滑块向下属性会发出`sliderPressed()`和`sliderReleased()`信号。

**如何使用：** 调用 `setSliderDown(...)` 修改 `sliderDown`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setSliderPosition(int)`

**作用与语义：**

该特性保持当前滑块位置。
如果启用`tracking`（默认），这和`value`是一样的。

**如何使用：** 调用 `setSliderPosition(...)` 修改 `sliderPosition`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTracking(bool enable)`

**作用与语义：**

该属性适用于是否启用滑块跟踪。
如果启用了跟踪（默认），滑块在拖动时会发出`valueChanged()`信号。如果禁用跟踪，只有在用户松开滑块时，滑块才会发出`valueChanged()`信号。

**如何使用：** 调用 `setTracking(...)` 修改 `tracking`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `int singleStep() const`

**作用与语义：**

该属性表示单步。
抽象滑块提供的两个自然步骤中较小的，通常对应于用户按下方向键。
如果在自动重复按键事件期间该属性被修改，行为则未定义。

**如何使用：** 调用 `singleStep()` 读取当前值；它不会修改应用状态。

### `int sliderPosition() const`

**作用与语义：**

该特性保持当前滑块位置。
如果启用`tracking`（默认），这和`value`是一样的。

**如何使用：** 调用 `sliderPosition()` 读取当前值；它不会修改应用状态。

### `int value() const`

**作用与语义：**

该属性表示滑块当前值。
滑块强制值在法定范围内：`minimum` <= `value` <= `maximum`。
改变数值也会影响`sliderPosition`。

**如何使用：** 调用 `value()` 读取当前值；它不会修改应用状态。

### `void setOrientation(Qt::Orientation)`

**作用与语义：**

此属性保存滑块的方向。
方向必须为 `Qt::Vertical`（默认值）或 `Qt::Horizontal`。

**如何使用：** 调用 `setOrientation(...)` 修改 `orientation`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setValue(int)`

**作用与语义：**

该属性表示滑块当前值。
滑块强制值在法定范围内：`minimum` <= `value` <= `maximum`。
改变数值也会影响`sliderPosition`。

**如何使用：** 调用 `setValue(...)` 修改 `value`；传入的新值会成为后续查询和相关界面行为所使用的值。

## 6. 深入实践与常见坑

### 生命周期和资源边界

控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

### 状态和错误边界

控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

### 线程边界

所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

### 最容易出现的错误

不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QAbstractSlider` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
