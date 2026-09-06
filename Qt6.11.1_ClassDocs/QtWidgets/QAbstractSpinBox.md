# QAbstractSpinBox

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QAbstractSpinBox` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QAbstractSpinBox` 是 Qt Widgets 中的抽象协议类型，通常通过具体子类、模型、插件或工厂来使用。

**内部模型：** 抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

**适用场景：** 当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。

**典型调用链：** 选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。

**先记住的坑：** 不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

## 2. 依赖与对象关系

- 头文件：`#include <QAbstractSpinBox>`
- 继承自：QWidget
- 直接派生类：QDateTimeEdit、QDoubleSpinBox,、QSpinBox

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

- `enum ButtonSymbols { UpDownArrows, PlusMinus, NoButtons }`
- `enum CorrectionMode { CorrectToPreviousValue, CorrectToNearestValue }`
- `flags StepEnabled`
- `enum StepEnabledFlag { StepNone, StepUpEnabled, StepDownEnabled }`
- `enum StepType { DefaultStepType, AdaptiveDecimalStepType }`

### 属性

- `accelerated : bool`
- `acceptableInput : bool`
- `alignment : Qt::Alignment`
- `buttonSymbols : ButtonSymbols`
- `correctionMode : CorrectionMode`
- `frame : bool`
- `keyboardTracking : bool`
- `readOnly : bool`
- `showGroupSeparator : bool`
- `specialValueText : QString`
- `text : QString`
- `wrapping : bool`

### 公有函数

- `QAbstractSpinBox(QWidget *parent = nullptr)`
- `virtual ~QAbstractSpinBox()`
- `Qt::Alignment alignment() const`
- `QAbstractSpinBox::ButtonSymbols buttonSymbols() const`
- `QAbstractSpinBox::CorrectionMode correctionMode() const`
- `virtual void fixup(QString &input) const`
- `bool hasAcceptableInput() const`
- `bool hasFrame() const`
- `void interpretText()`
- `bool isAccelerated() const`
- `bool isGroupSeparatorShown() const`
- `bool isReadOnly() const`
- `bool keyboardTracking() const`
- `void setAccelerated(bool on)`
- `void setAlignment(Qt::Alignment flag)`
- `void setButtonSymbols(QAbstractSpinBox::ButtonSymbols bs)`
- `void setCorrectionMode(QAbstractSpinBox::CorrectionMode cm)`
- `void setFrame(bool)`
- `void setGroupSeparatorShown(bool shown)`
- `void setKeyboardTracking(bool kt)`
- `void setReadOnly(bool r)`
- `void setSpecialValueText(const QString &txt)`
- `void setWrapping(bool w)`
- `QString specialValueText() const`
- `virtual void stepBy(int steps)`
- `QString text() const`
- `virtual QValidator::State validate(QString &input, int &pos) const`
- `bool wrapping() const`

### 重实现的公有函数

- `virtual bool event(QEvent *event) override`
- `virtual QVariant inputMethodQuery(Qt::InputMethodQuery query) const override`
- `virtual QSize minimumSizeHint() const override`
- `virtual QSize sizeHint() const override`

### 公有槽函数

- `virtual void clear()`
- `void selectAll()`
- `void stepDown()`
- `void stepUp()`

### 信号

- `void editingFinished()`
- `(since 6.10) void returnPressed()`

### 保护函数

- `virtual void initStyleOption(QStyleOptionSpinBox *option) const`
- `QLineEdit * lineEdit() const`
- `void setLineEdit(QLineEdit *lineEdit)`
- `virtual QAbstractSpinBox::StepEnabled stepEnabled() const`

### 重实现的保护函数

- `virtual void changeEvent(QEvent *event) override`
- `virtual void closeEvent(QCloseEvent *event) override`
- `virtual void contextMenuEvent(QContextMenuEvent *event) override`
- `virtual void focusInEvent(QFocusEvent *event) override`
- `virtual void focusOutEvent(QFocusEvent *event) override`
- `virtual void hideEvent(QHideEvent *event) override`
- `virtual void keyPressEvent(QKeyEvent *event) override`
- `virtual void keyReleaseEvent(QKeyEvent *event) override`
- `virtual void mouseMoveEvent(QMouseEvent *event) override`
- `virtual void mousePressEvent(QMouseEvent *event) override`
- `virtual void mouseReleaseEvent(QMouseEvent *event) override`
- `virtual void paintEvent(QPaintEvent *event) override`
- `virtual void resizeEvent(QResizeEvent *event) override`
- `virtual void showEvent(QShowEvent *event) override`
- `virtual void timerEvent(QTimerEvent *event) override`
- `virtual void wheelEvent(QWheelEvent *event) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QAbstractSpinBox::ButtonSymbols`

**作用与语义：**

这种枚举类型描述了旋转框中按钮上可以显示的符号。
- `QAbstractSpinBox::UpDownArrows`：`0`;经典风格的小箭头。
- `QAbstractSpinBox::PlusMinus`：`1`;以及——符号。
- `QAbstractSpinBox::NoButtons`：`2`;不要显示按钮。

### `enum QAbstractSpinBox::CorrectionMode`

**作用与语义：**

该枚举类型描述了旋转盒在编辑结束后纠正`Intermediate`值的模式。
- `QAbstractSpinBox::CorrectToPreviousValue`：`0`;自旋盒将恢复到最后有效值。
- `QAbstractSpinBox::CorrectToNearestValue`：`1`;自旋盒将恢复到最接近的有效值。

### `enum QAbstractSpinBox::StepEnabledFlagflags QAbstractSpinBox::StepEnabled`

**作用与语义：**

- `QAbstractSpinBox::StepNone`：`0x00`
- `QAbstractSpinBox::StepUpEnabled`：`0x01`
- `QAbstractSpinBox::StepDownEnabled`：`0x02`
StepEnabled 类型是 QFlags 的 typedef<StepEnabledFlag>。它存储 StepEnabledFlag 值的 OR 组合。

### `accelerated : bool`

**作用与语义：**

该属性决定了当按下阶级上/下按钮时，旋转盒是否会加速步进频率。
如果启用了，旋转框会随着你按住按钮的时间越长，数值的增减会越快。

**如何使用：** 调用 `accelerated()` 读取当前值；它不会修改应用状态。

### `[read-only] acceptableInput : bool`

**作用与语义：**

该属性是否满足当前验证。

**如何使用：** 调用 `acceptableInput()` 读取当前值；它不会修改应用状态。

### `alignment : Qt::Alignment`

**作用与语义：**

该属性表示自旋盒的对齐。
可能的数值有`Qt::AlignLeft`、`Qt::AlignRight`和`Qt::AlignHCenter`。
默认情况下，对齐是`Qt::AlignLeft`。
尝试将对齐设置为非法标志组合毫无效果。

**如何使用：** 调用 `alignment()` 读取当前值；它不会修改应用状态。

### `buttonSymbols : ButtonSymbols`

**作用与语义：**

该属性保留当前按钮符号模式。
可能的值可以是`UpDownArrows`或`PlusMinus`。默认值是`UpDownArrows`。
注意，有些样式可能渲染`PlusMinus`和`UpDownArrows`完全相同。

**如何使用：** 调用 `buttonSymbols()` 读取当前值；它不会修改应用状态。

### `correctionMode : CorrectionMode`

**作用与语义：**

该属性具有编辑结束时纠正`Intermediate`值的模式。
默认模式是`QAbstractSpinBox::CorrectToPreviousValue`。

**如何使用：** 调用 `correctionMode()` 读取当前值；它不会修改应用状态。

### `frame : bool`

**作用与语义：**

该属性是否成立，取决于自旋盒是否以一个框架绘制自身。
如果启用（默认），旋转盒会在一个框架内绘制自己，否则旋转盒会在没有任何框架的情况下绘制自己。

**如何使用：** 调用 `frame()` 读取当前值；它不会修改应用状态。

### `keyboardTracking : bool`

**作用与语义：**

该属性决定自旋盒启用键盘跟踪。
如果启用了键盘跟踪（默认），旋转盒在输入新值时会发出valueChanged()和textChanged()信号。
例如，当用户输入600输入600时，自旋盒会发出3个信号，分别为60、60和600。
如果禁用键盘跟踪，旋转盒在输入时不会发出valueChanged()和textChanged()信号。它会在之后、按回车键、键盘失去焦点或使用其他旋转盒功能（如按方向键）时发出信号。

**如何使用：** 调用 `keyboardTracking()` 读取当前值；它不会修改应用状态。

### `readOnly : bool`

**作用与语义：**

该属性决定自旋盒是否为只读。
在只读模式下，用户仍可将文本复制到剪贴板，或拖拽文本;但无法编辑。
`QAbstractSpinBox`中的`QLineEdit`在只读模式下没有显示光标。

**如何使用：** 调用 `readOnly()` 读取当前值；它不会修改应用状态。

### `showGroupSeparator : bool`

**作用与语义：**

该属性判定是否启用千分隔符。默认情况下，该属性为假。

**如何使用：** 调用 `showGroupSeparator()` 读取当前值；它不会修改应用状态。

### `specialValueText : QString`

**作用与语义：**

该属性包含特殊值文本。
如果设置为，旋转框会在当前值等于最小值()时显示该文本而非数值。通常用来表示该选择具有特殊（默认）含义。
例如，如果你的旋转框允许用户选择显示图像的缩放因子（或缩放等级），而你的应用程序能够自动选择一个缩放因子，使图像完全嵌入显示窗口，你可以这样设置旋转框：
用户可以选择从1%到1000%的缩放，或者选择“自动”，由应用程序自行选择。你的代码必须将自转盒值为0，视为用户请求将图像缩放以适应窗口内。
所有值都以前缀和后缀（如已设置）显示，唯独特殊值仅显示特殊值文本。该特殊文本通过传递`QString`的 `QSpinBox::textChanged()` 信号传递。
要关闭特殊值文本显示，请用空字符串调用该函数。默认情况下没有特殊值文本，即数值按常显示。
如果没有设置特殊值文本，specialValueText() 返回一个空字符串。

**如何使用：** 调用 `specialValueText()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
     QSpinBox *zoomSpinBox = new QSpinBox;
     zoomSpinBox->setRange(0, 1000);
     zoomSpinBox->setSingleStep(10);
     zoomSpinBox->setSuffix("%");
     zoomSpinBox->setSpecialValueText(tr("Automatic"));
     zoomSpinBox->setValue(100);
```

### `[read-only] text : QString`

**作用与语义：**

该属性包含自旋盒的文本，包括任何前缀和后缀。
没有默认文本。

**如何使用：** 调用 `text()` 读取当前值；它不会修改应用状态。

### `wrapping : bool`

**作用与语义：**

该属性适用于自旋盒是否为圆形。
如果包裹为真，从最大值()向上移动会到达最小值，反之亦然。包裹只有在设置了最小值()和最大值时才有意义。

**如何使用：** 调用 `wrapping()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 QSpinBox *spinBox = new QSpinBox(this);
 spinBox->setRange(0, 100);
 spinBox->setWrapping(true);
 spinBox->setValue(100);
 spinBox->stepBy(1);
 // value is 0
```

### `[explicit] QAbstractSpinBox::QAbstractSpinBox(QWidget *parent = nullptr)`

**作用与语义：**

构造一个带有默认`wrapping`和对齐属性的抽象自旋盒，`parent`。

### `[virtual noexcept] QAbstractSpinBox::~QAbstractSpinBox()`

**作用与语义：**

当 `QAbstractSpinBox` 被销毁时调用。

### `[override virtual protected] void QAbstractSpinBox::changeEvent(QEvent *event)`

**作用与语义：**

重装：`QWidget::changeEvent`（QEvent *事件）。
该事件处理程序可以重新实现以处理状态变化。
该事件中被更改的状态可以通过提供的`event`检索。
变更事件包括：`QEvent::ToolBarChange`、`QEvent::ActivationChange`、`QEvent::EnabledChange`、`QEvent::FontChange`、`QEvent::StyleChange`、`QEvent::PaletteChange`、`QEvent::WindowTitleChange`、`QEvent::IconTextChange`、`QEvent::ModifiedChange`、`QEvent::MouseTrackingChange`、`QEvent::ParentChange`、`QEvent::WindowStateChange`、`QEvent::LanguageChange`、`QEvent::LocaleChange`、`QEvent::LayoutDirectionChange`、`QEvent::ReadOnlyChange`。

### `[virtual slot] void QAbstractSpinBox::clear()`

**作用与语义：**

清除行编辑中除前缀和后缀外的所有文本。

### `[override virtual protected] void QAbstractSpinBox::closeEvent(QCloseEvent *event)`

**作用与语义：**

重实现自：`QWidget::closeEvent`（QCloseEvent *event）。
当 Qt 收到来自窗口系统顶层控件的窗口关闭请求时，该事件处理程序会以该`event`调用。
默认情况下，事件被接受，小部件关闭。你可以重新实现这个函数，改变小部件对窗口关闭请求的响应方式。例如，你可以通过调用所有事件的 `ignore()` 来阻止窗口关闭。
主窗口应用程序通常会重新实现该函数，以检查用户的工作是否已被保存，并在关闭前请求许可。

### `[override virtual protected] void QAbstractSpinBox::contextMenuEvent(QContextMenuEvent *event)`

**作用与语义：**

重实现自：`QWidget::contextMenuEvent`（QContextMenuEvent *event）。
该事件处理程序用于事件`event`，可以在子类中重新实现，以接收控件上下文菜单事件。
当控件的 `contextMenuPolicy` `Qt::DefaultContextMenu`时调用处理器。
默认实现忽略上下文事件。详情请参见`QContextMenuEvent`文档。

### `[signal] void QAbstractSpinBox::editingFinished()`

**作用与语义：**

该信号发出后编辑完成。当旋转盒失去焦点且按下回车键时，就会发生这种情况。

### `[override virtual] bool QAbstractSpinBox::event(QEvent *event)`

**作用与语义：**

重实现自：`QWidget::event`（QEvent *事件）。

### `[virtual] void QAbstractSpinBox::fixup(QString &input) const`

**作用与语义：**

如果`input`在按回车键或调用`interpretText()`时未被验证为`QValidator::Acceptable`，`QAbstractSpinBox`会调用该虚拟函数。它会尝试修改文本使其有效。在各个子类中重新实现。

### `[override virtual protected] void QAbstractSpinBox::focusInEvent(QFocusEvent *event)`

**作用与语义：**

重实现自：`QWidget::focusInEvent`（QFocusEvent *event）。
该事件处理程序可以在子类中重新实现，以接收控件的键盘焦点事件（焦点接收）。事件通过`event`参数传递。
小部件通常必须`setFocusPolicy()`到非`Qt::NoFocus`的对象才能接收焦点事件。（注意，应用程序员可以调用任何小部件`setFocus()`，即使是那些通常不接受焦点的小部件。）。
默认实现会更新小部件（除非是没有指定`focusPolicy()`的窗口）。

### `[override virtual protected] void QAbstractSpinBox::focusOutEvent(QFocusEvent *event)`

**作用与语义：**

重现：`QWidget::focusOutEvent`（QFocusEvent *event）。
该事件处理程序可以在子类中重新实现，以接收控件的键盘焦点事件（焦点丢失）。事件通过`event`参数传递。
小部件通常必须`setFocusPolicy()`到非`Qt::NoFocus`的对象才能接收焦点事件。（注意，应用程序员可以调用任何小部件`setFocus()`，即使是那些通常不接受焦点的小部件。）。
默认实现会更新小部件（除非是没有指定`focusPolicy()`的窗口）。

### `[override virtual protected] void QAbstractSpinBox::hideEvent(QHideEvent *event)`

**作用与语义：**

重实现自：`QWidget::hideEvent`（QHideEvent *event）。
该事件处理程序可以在子类中重新实现，以接收控件隐藏事件。事件通过`event`参数传递。
隐藏事件会在小部件被隐藏后立即发送。
注意：当窗口系统改变其映射状态时，小部件会接收自发显示和隐藏事件，例如用户最小化窗口时自发隐藏事件，恢复窗口时自发显示事件。收到自发隐藏事件后，小部件仍被视为可见，意义`isVisible()`。

### `[virtual protected] void QAbstractSpinBox::initStyleOption(QStyleOptionSpinBox *option) const`

**作用与语义：**

用这个`QSpinBox`的值初始化`option`。这种方法对需要 `QStyleOptionSpinBox`但不想自己填满所有信息的子类很有用。

### `[override virtual] QVariant QAbstractSpinBox::inputMethodQuery(Qt::InputMethodQuery query) const`

**作用与语义：**

重实现自：`QWidget::inputMethodQuery`（Qt：：InputMethodQuery query） const.
该方法仅适用于输入控件。输入方法用于查询控件的一组属性，以支持复杂的输入法操作，以支持周围文本和重新转换。
`query` 指定查询的属性。

### `void QAbstractSpinBox::interpretText()`

**作用与语义：**

该函数解释自旋盒的文本。如果值自上次解释以来发生变化，则会发出信号。

### `[override virtual protected] void QAbstractSpinBox::keyPressEvent(QKeyEvent *event)`

**作用与语义：**

重实现自：`QWidget::keyPressEvent`（QKeyEvent *event）。
该功能负责键盘输入。
具体处理的密钥如下：
- `Enter/Return`：即使值自上次发出以来未变，也会重新解释文本并发出信号。
- `Up`：这将调用`stepBy`（1）
- `Down`：这将触发`stepBy`（-1）
- `Page up`：这将引发`stepBy`（10）
- `Page down`：这将触发`stepBy`（-10）
该事件处理程序用于事件`event`，可以在子类中重新实现，以接收该控件的按键事件。
小部件必须先调用`setFocusPolicy()`接受焦点，并且必须拥有焦点才能接收按键事件。
如果你重新实现这个处理器，如果你不对密钥进行操作，务必调用基类实现。
默认实现会关闭弹出小部件，如果用户按下`QKeySequence::Cancel`的按键序列（通常是Escape键）。否则事件会被忽略，以便小部件的父节点能够解释。
注意`QKeyEvent`以 isAccepted() == true 开头，所以你不需要调用 `QKeyEvent::accept()`——只要你对密钥执行时不要调用基类实现即可。

### `[override virtual protected] void QAbstractSpinBox::keyReleaseEvent(QKeyEvent *event)`

**作用与语义：**

重实现自：`QWidget::keyReleaseEvent`（QKeyEvent *event）。
该事件处理程序用于事件`event`，可以在子类中重新实现，以接收该小部件的密钥释放事件。
小部件必须先接受焦点并拥有焦点，才能接收密钥释放事件。
如果你重新实现这个处理器，如果你不对密钥进行操作，务必调用基类实现。
默认实现忽略事件，以便小部件的父节点能够解释事件。
注意`QKeyEvent`以 isAccepted() == true开头，所以你不需要调用`QKeyEvent::accept()`——只要你对密钥操作时不要调用基类实现即可。

### `[protected] QLineEdit *QAbstractSpinBox::lineEdit() const`

**作用与语义：**

该函数返回指向自旋盒的行编辑位置的指针。

### `[override virtual] QSize QAbstractSpinBox::minimumSizeHint() const`

**作用与语义：**

重新实现属性的访问函数：`QWidget::minimumSizeHint`。

### `[override virtual protected] void QAbstractSpinBox::mouseMoveEvent(QMouseEvent *event)`

**作用与语义：**

重实现自：`QWidget::mouseMoveEvent`（QMouseEvent *event）。
该事件处理程序用于事件`event`，可以重新实现为子类，以接收该小部件的鼠标移动事件。
如果关闭鼠标追踪，只有在鼠标移动过程中按下鼠标按钮时才会发生鼠标移动事件。如果开启鼠标追踪，即使未按键，鼠标移动事件也会发生。
`QMouseEvent::position()`报告鼠标光标相对于该小部件的位置。对于按下和释放事件，位置通常与最后一次鼠标移动事件的位置相同，但如果用户的手握手，可能会有所不同。这是底层窗口系统的功能，而非Qt。
如果你想在鼠标移动时立即显示提示（例如，获取鼠标坐标与`QMouseEvent::position()`并显示为提示），你必须先启用上述的鼠标追踪功能。然后，为了确保提示立即更新，你必须在鼠标移动事件（mouseMoveEvent）实现中调用`QToolTip::showText()`而不是`setToolTip()`。

### `[override virtual protected] void QAbstractSpinBox::mousePressEvent(QMouseEvent *event)`

**作用与语义：**

重实现自：`QWidget::mousePressEvent`（QMouseEvent *event）。
该事件处理程序用于事件`event`，可以重新实现为子类，以接收该小部件的鼠标按键事件。
如果你在 mousePressEvent() 创建新控件，`mouseReleaseEvent()`可能不会出现在你预期的位置，这取决于底层窗口系统（或 X11 窗口管理器）、控件的位置，甚至可能还有其他因素。
默认实现实现了当你点击窗口外时关闭弹出小部件的功能。对于其他小部件类型，它没有任何作用。

### `[override virtual protected] void QAbstractSpinBox::mouseReleaseEvent(QMouseEvent *event)`

**作用与语义：**

重实现自：`QWidget::mouseReleaseEvent`（QMouseEvent *event）。
该事件处理程序用于事件`event`，可以重新实现为子类，以接收该小部件的鼠标释放事件。

### `[override virtual protected] void QAbstractSpinBox::paintEvent(QPaintEvent *event)`

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

### `[override virtual protected] void QAbstractSpinBox::resizeEvent(QResizeEvent *event)`

**作用与语义：**

重实现自：`QWidget::resizeEvent`（QResizeEvent *event）。
该事件处理程序可以在子类中重新实现，以接收通过 `event` 参数传递的控件调整大小事件。当调用 resizeEvent() 时，控件已经拥有新的几何体。旧的大小可以通过 `QResizeEvent::oldSize()` 访问。
控件会被擦除，并在处理调整尺寸事件后立即接收绘图事件。不需要（也不应该）在这个处理程序中进行绘图。

### `[signal, since 6.10] void QAbstractSpinBox::returnPressed()`

**作用与语义：**

当使用返回键或回车键时，会发出该信号。

### `[slot] void QAbstractSpinBox::selectAll()`

**作用与语义：**

选择旋转框中除前缀和后缀外的所有文本。

### `[protected] void QAbstractSpinBox::setLineEdit(QLineEdit *lineEdit)`

**作用与语义：**

将旋转盒的行编辑设置为`lineEdit`，而不是当前的行编辑小部件。`lineEdit`不能被`nullptr`。
`QAbstractSpinBox`接管了新`lineEdit`。
如果`QLineEdit::validator()` 返回`lineEdit`返回`nullptr`，旋转盒的内部验证器将在行编辑时被设置。

### `[override virtual protected] void QAbstractSpinBox::showEvent(QShowEvent *event)`

**作用与语义：**

重实现自：`QWidget::showEvent`（QShowEvent *event）。
该事件处理程序可以在子类中重新实现，以接收传递给 `event` 参数的控件显示事件。
非自发的展示事件会在展示前立即发送到小部件。窗口的自发展示事件则在展示之后交付。
注意：当窗口系统改变其映射状态时，小部件会接收自发显示和隐藏事件，例如用户最小化窗口时自发隐藏事件，窗口恢复时自发显示事件。收到自发隐藏事件后，小部件仍被视为`isVisible()`可见。

### `[override virtual] QSize QAbstractSpinBox::sizeHint() const`

**作用与语义：**

重新实现了属性的访问函数：`QWidget::sizeHint`。

### `[virtual] void QAbstractSpinBox::stepBy(int steps)`

**作用与语义：**

每当用户触发一步时调用的虚拟函数。`steps`参数表示已采取的步数。例如，按`Qt::Key_Down`会触发对`stepBy(-1)`的调用，而按`Qt::Key_PageUp`则会触发对`stepBy(10)`的调用。
如果你对`QAbstractSpinBox`子类，必须重新实现这个函数。注意，即使最终值超出极小值和最大值范围，这个函数也会被调用。处理这些情况是这个函数的工作。

### `[slot] void QAbstractSpinBox::stepDown()`

**作用与语义：**

下行一步 调用该槽函数类似于调用`stepBy`（-1）;

### `[virtual protected] QAbstractSpinBox::StepEnabled QAbstractSpinBox::stepEnabled() const`

**作用与语义：**

虚拟函数，决定在任一时刻上下步进是否合法。除非 （stepEnabled() & `StepUpEnabled`） ！= 0，否则上箭头将被涂为禁用。如果开启了包裹，默认实现会返回 （`StepUpEnabled`| `StepDownEnabled`）。否则如果值>为 minimum()，则返回 （`StepDownEnabled`），如果值为 maximum()，则返回 `StepUpEnabled`，< 最大化。
如果你`QAbstractSpinBox`子类，就需要重新实现这个函数。

### `[slot] void QAbstractSpinBox::stepUp()`

**作用与语义：**

上调一行步 调用该槽函数类似于调用 `stepBy`（1）;

### `[override virtual protected] void QAbstractSpinBox::timerEvent(QTimerEvent *event)`

**作用与语义：**

重实现自：`QObject::timerEvent`（QTimerEvent *event）。

### `[virtual] QValidator::State QAbstractSpinBox::validate(QString &input, int &pos) const`

**作用与语义：**

`QAbstractSpinBox`调用该虚拟函数以判断`input`是否有效。`pos`参数表示字符串中的位置。在各个子类中重新实现。

### `[override virtual protected] void QAbstractSpinBox::wheelEvent(QWheelEvent *event)`

**作用与语义：**

重实现自：`QWidget::wheelEvent`（QWheelEvent *event）。
该事件处理程序用于事件`event`，可以在子类中重新实现，以接收该控件的轮事件。
如果你重新实现了这个处理程序，非常重要的是，如果你不处理事件，必须`ignore()`事件，这样小部件的父节点才能解释它。
默认实现会忽略该事件。

### `flags StepEnabled`

**作用与语义：**

- `QAbstractSpinBox::StepNone`：`0x00`
- `QAbstractSpinBox::StepUpEnabled`：`0x01`
- `QAbstractSpinBox::StepDownEnabled`：`0x02`
StepEnabled 类型是 QFlags 的 typedef<StepEnabledFlag>。它存储 StepEnabledFlag 值的 OR 组合。

### `enum StepEnabledFlag { StepNone, StepUpEnabled, StepDownEnabled }`

**作用与语义：**

- `QAbstractSpinBox::StepNone`：`0x00`
- `QAbstractSpinBox::StepUpEnabled`：`0x01`
- `QAbstractSpinBox::StepDownEnabled`：`0x02`
StepEnabled 类型是 QFlags 的 typedef<StepEnabledFlag>。它存储 StepEnabledFlag 值的 OR 组合。

### `enum StepType { DefaultStepType, AdaptiveDecimalStepType }`

**作用与语义：**

指定步进算法。`DefaultStepType` 始终使用 `singleStep`；`AdaptiveDecimalStepType` 根据当前数值的数量级自动调整步长，例如较大数值每次改变得更多。自适应模式下 `singleStep` 不参与实际步长计算。

### `Qt::Alignment alignment() const`

**作用与语义：**

该属性表示自旋盒的对齐。
可能的数值有`Qt::AlignLeft`、`Qt::AlignRight`和`Qt::AlignHCenter`。
默认情况下，对齐是`Qt::AlignLeft`。
尝试将对齐设置为非法标志组合毫无效果。

**如何使用：** 调用 `alignment()` 读取当前值；它不会修改应用状态。

### `QAbstractSpinBox::ButtonSymbols buttonSymbols() const`

**作用与语义：**

该属性保留当前按钮符号模式。
可能的值可以是`UpDownArrows`或`PlusMinus`。默认值是`UpDownArrows`。
注意，有些样式可能渲染`PlusMinus`和`UpDownArrows`完全相同。

**如何使用：** 调用 `buttonSymbols()` 读取当前值；它不会修改应用状态。

### `QAbstractSpinBox::CorrectionMode correctionMode() const`

**作用与语义：**

该属性具有编辑结束时纠正`Intermediate`值的模式。
默认模式是`QAbstractSpinBox::CorrectToPreviousValue`。

**如何使用：** 调用 `correctionMode()` 读取当前值；它不会修改应用状态。

### `bool hasAcceptableInput() const`

**作用与语义：**

该属性是否满足当前验证。

**如何使用：** 调用 `hasAcceptableInput()` 读取当前值；它不会修改应用状态。

### `bool hasFrame() const`

**作用与语义：**

该属性是否成立，取决于自旋盒是否以一个框架绘制自身。
如果启用（默认），旋转盒会在一个框架内绘制自己，否则旋转盒会在没有任何框架的情况下绘制自己。

**如何使用：** 调用 `hasFrame()` 读取当前值；它不会修改应用状态。

### `bool isAccelerated() const`

**作用与语义：**

该属性决定了当按下阶级上/下按钮时，旋转盒是否会加速步进频率。
如果启用了，旋转框会随着你按住按钮的时间越长，数值的增减会越快。

**如何使用：** 调用 `isAccelerated()` 读取当前值；它不会修改应用状态。

### `bool isGroupSeparatorShown() const`

**作用与语义：**

该属性判定是否启用千分隔符。默认情况下，该属性为假。

**如何使用：** 调用 `isGroupSeparatorShown()` 读取当前值；它不会修改应用状态。

### `bool isReadOnly() const`

**作用与语义：**

该属性决定自旋盒是否为只读。
在只读模式下，用户仍可将文本复制到剪贴板，或拖拽文本;但无法编辑。
`QAbstractSpinBox`中的`QLineEdit`在只读模式下没有显示光标。

**如何使用：** 调用 `isReadOnly()` 读取当前值；它不会修改应用状态。

### `bool keyboardTracking() const`

**作用与语义：**

该属性决定自旋盒启用键盘跟踪。
如果启用了键盘跟踪（默认），旋转盒在输入新值时会发出valueChanged()和textChanged()信号。
例如，当用户输入600输入600时，自旋盒会发出3个信号，分别为60、60和600。
如果禁用键盘跟踪，旋转盒在输入时不会发出valueChanged()和textChanged()信号。它会在之后、按回车键、键盘失去焦点或使用其他旋转盒功能（如按方向键）时发出信号。

**如何使用：** 调用 `keyboardTracking()` 读取当前值；它不会修改应用状态。

### `void setAccelerated(bool on)`

**作用与语义：**

该属性决定了当按下阶级上/下按钮时，旋转盒是否会加速步进频率。
如果启用了，旋转框会随着你按住按钮的时间越长，数值的增减会越快。

**如何使用：** 调用 `setAccelerated(...)` 修改 `accelerated`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setAlignment(Qt::Alignment flag)`

**作用与语义：**

该属性表示自旋盒的对齐。
可能的数值有`Qt::AlignLeft`、`Qt::AlignRight`和`Qt::AlignHCenter`。
默认情况下，对齐是`Qt::AlignLeft`。
尝试将对齐设置为非法标志组合毫无效果。

**如何使用：** 调用 `setAlignment(...)` 修改 `alignment`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setButtonSymbols(QAbstractSpinBox::ButtonSymbols bs)`

**作用与语义：**

该属性保留当前按钮符号模式。
可能的值可以是`UpDownArrows`或`PlusMinus`。默认值是`UpDownArrows`。
注意，有些样式可能渲染`PlusMinus`和`UpDownArrows`完全相同。

**如何使用：** 调用 `setButtonSymbols(...)` 修改 `buttonSymbols`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setCorrectionMode(QAbstractSpinBox::CorrectionMode cm)`

**作用与语义：**

该属性具有编辑结束时纠正`Intermediate`值的模式。
默认模式是`QAbstractSpinBox::CorrectToPreviousValue`。

**如何使用：** 调用 `setCorrectionMode(...)` 修改 `correctionMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setFrame(bool)`

**作用与语义：**

该属性是否成立，取决于自旋盒是否以一个框架绘制自身。
如果启用（默认），旋转盒会在一个框架内绘制自己，否则旋转盒会在没有任何框架的情况下绘制自己。

**如何使用：** 调用 `setFrame(...)` 修改 `frame`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setGroupSeparatorShown(bool shown)`

**作用与语义：**

该属性判定是否启用千分隔符。默认情况下，该属性为假。

**如何使用：** 调用 `setGroupSeparatorShown(...)` 修改 `showGroupSeparator`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setKeyboardTracking(bool kt)`

**作用与语义：**

该属性决定自旋盒启用键盘跟踪。
如果启用了键盘跟踪（默认），旋转盒在输入新值时会发出valueChanged()和textChanged()信号。
例如，当用户输入600输入600时，自旋盒会发出3个信号，分别为60、60和600。
如果禁用键盘跟踪，旋转盒在输入时不会发出valueChanged()和textChanged()信号。它会在之后、按回车键、键盘失去焦点或使用其他旋转盒功能（如按方向键）时发出信号。

**如何使用：** 调用 `setKeyboardTracking(...)` 修改 `keyboardTracking`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setReadOnly(bool r)`

**作用与语义：**

该属性决定自旋盒是否为只读。
在只读模式下，用户仍可将文本复制到剪贴板，或拖拽文本;但无法编辑。
`QAbstractSpinBox`中的`QLineEdit`在只读模式下没有显示光标。

**如何使用：** 调用 `setReadOnly(...)` 修改 `readOnly`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setSpecialValueText(const QString &txt)`

**作用与语义：**

该属性包含特殊值文本。
如果设置为，旋转框会在当前值等于最小值()时显示该文本而非数值。通常用来表示该选择具有特殊（默认）含义。
例如，如果你的旋转框允许用户选择显示图像的缩放因子（或缩放等级），而你的应用程序能够自动选择一个缩放因子，使图像完全嵌入显示窗口，你可以这样设置旋转框：
用户可以选择从1%到1000%的缩放，或者选择“自动”，由应用程序自行选择。你的代码必须将自转盒值为0，视为用户请求将图像缩放以适应窗口内。
所有值都以前缀和后缀（如已设置）显示，唯独特殊值仅显示特殊值文本。该特殊文本通过传递`QString`的 `QSpinBox::textChanged()` 信号传递。
要关闭特殊值文本显示，请用空字符串调用该函数。默认情况下没有特殊值文本，即数值按常显示。
如果没有设置特殊值文本，specialValueText() 返回一个空字符串。

**如何使用：** 调用 `setSpecialValueText(...)` 修改 `specialValueText`；传入的新值会成为后续查询和相关界面行为所使用的值。

**官方示例：**

```cpp
     QSpinBox *zoomSpinBox = new QSpinBox;
     zoomSpinBox->setRange(0, 1000);
     zoomSpinBox->setSingleStep(10);
     zoomSpinBox->setSuffix("%");
     zoomSpinBox->setSpecialValueText(tr("Automatic"));
     zoomSpinBox->setValue(100);
```

### `void setWrapping(bool w)`

**作用与语义：**

该属性适用于自旋盒是否为圆形。
如果包裹为真，从最大值()向上移动会到达最小值，反之亦然。包裹只有在设置了最小值()和最大值时才有意义。

**如何使用：** 调用 `setWrapping(...)` 修改 `wrapping`；传入的新值会成为后续查询和相关界面行为所使用的值。

**官方示例：**

```cpp
 QSpinBox *spinBox = new QSpinBox(this);
 spinBox->setRange(0, 100);
 spinBox->setWrapping(true);
 spinBox->setValue(100);
 spinBox->stepBy(1);
 // value is 0
```

### `QString specialValueText() const`

**作用与语义：**

该属性包含特殊值文本。
如果设置为，旋转框会在当前值等于最小值()时显示该文本而非数值。通常用来表示该选择具有特殊（默认）含义。
例如，如果你的旋转框允许用户选择显示图像的缩放因子（或缩放等级），而你的应用程序能够自动选择一个缩放因子，使图像完全嵌入显示窗口，你可以这样设置旋转框：
用户可以选择从1%到1000%的缩放，或者选择“自动”，由应用程序自行选择。你的代码必须将自转盒值为0，视为用户请求将图像缩放以适应窗口内。
所有值都以前缀和后缀（如已设置）显示，唯独特殊值仅显示特殊值文本。该特殊文本通过传递`QString`的 `QSpinBox::textChanged()` 信号传递。
要关闭特殊值文本显示，请用空字符串调用该函数。默认情况下没有特殊值文本，即数值按常显示。
如果没有设置特殊值文本，specialValueText() 返回一个空字符串。

**如何使用：** 调用 `specialValueText()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
     QSpinBox *zoomSpinBox = new QSpinBox;
     zoomSpinBox->setRange(0, 1000);
     zoomSpinBox->setSingleStep(10);
     zoomSpinBox->setSuffix("%");
     zoomSpinBox->setSpecialValueText(tr("Automatic"));
     zoomSpinBox->setValue(100);
```

### `QString text() const`

**作用与语义：**

该属性包含自旋盒的文本，包括任何前缀和后缀。
没有默认文本。

**如何使用：** 调用 `text()` 读取当前值；它不会修改应用状态。

### `bool wrapping() const`

**作用与语义：**

该属性适用于自旋盒是否为圆形。
如果包裹为真，从最大值()向上移动会到达最小值，反之亦然。包裹只有在设置了最小值()和最大值时才有意义。

**如何使用：** 调用 `wrapping()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 QSpinBox *spinBox = new QSpinBox(this);
 spinBox->setRange(0, 100);
 spinBox->setWrapping(true);
 spinBox->setValue(100);
 spinBox->stepBy(1);
 // value is 0
```

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

`QAbstractSpinBox` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
