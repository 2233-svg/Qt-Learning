# QGroupBox

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QGroupBox` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QGroupBox` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QGroupBox>`
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

- `alignment : Qt::Alignment`
- `checkable : bool`
- `checked : bool`
- `flat : bool`
- `title : QString`

### 公有函数

- `QGroupBox(QWidget *parent = nullptr)`
- `QGroupBox(const QString &title, QWidget *parent = nullptr)`
- `virtual ~QGroupBox()`
- `Qt::Alignment alignment() const`
- `bool isCheckable() const`
- `bool isChecked() const`
- `bool isFlat() const`
- `void setAlignment(int alignment)`
- `void setCheckable(bool checkable)`
- `void setFlat(bool flat)`
- `void setTitle(const QString &title)`
- `QString title() const`

### 重实现的公有函数

- `virtual QSize minimumSizeHint() const override`

### 公有槽函数

- `void setChecked(bool checked)`

### 信号

- `void clicked(bool checked = false)`
- `void toggled(bool on)`

### 保护函数

- `virtual void initStyleOption(QStyleOptionGroupBox *option) const`

### 重实现的保护函数

- `virtual void changeEvent(QEvent *ev) override`
- `virtual void childEvent(QChildEvent *c) override`
- `virtual bool event(QEvent *e) override`
- `virtual void focusInEvent(QFocusEvent *fe) override`
- `virtual void mouseMoveEvent(QMouseEvent *event) override`
- `virtual void mousePressEvent(QMouseEvent *event) override`
- `virtual void mouseReleaseEvent(QMouseEvent *event) override`
- `virtual void paintEvent(QPaintEvent *event) override`
- `virtual void resizeEvent(QResizeEvent *e) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `alignment : Qt::Alignment`

**作用与语义：**

该属性表示了组框标题的对齐。
大多数样式将标题置于画面顶部。标题的水平对齐可用以下列表中的单个值来指定：
- `Qt::AlignLeft` 将标题文本与组框的左侧对齐。
- `Qt::AlignRight` 将标题文本与组框的右侧对齐。
- `Qt::AlignHCenter` 将标题文本与组框的水平中心对齐。
默认阵营是`Qt::AlignLeft`。

**如何使用：** 调用 `alignment()` 读取当前值；它不会修改应用状态。

### `checkable : bool`

**作用与语义：**

该属性决定该组方块标题中是否包含复选框。
如果该属性被`true`，组框会用复选框代替普通标签显示标题。如果勾选该复选框，则该组框的子节点被启用;否则，子节点被禁用且无法访问。
默认情况下，组组方框不可勾选。
如果该属性为组框启用，也会初步检查以确保其内容已被启用。

**如何使用：** 调用 `checkable()` 读取当前值；它不会修改应用状态。

### `checked : bool`

**作用与语义：**

该属性是否满足群组框的勾选。
如果组框可勾选，则以复选框显示。勾选该框时，组框的子节点被启用;否则，子节点被禁用，用户无法访问。
默认情况下，可勾选的组组选项也会被勾选。
注意：当取消勾选该选项时，组框本身不会被禁用，你可以在未勾选的组框中明确启用单个子节点。但这不推荐，因为这可能会给最终用户带来意外体验。

**如何使用：** 调用 `checked()` 读取当前值；它不会修改应用状态。

### `flat : bool`

**作用与语义：**

无论分组盒是平整的还是有框架，这一属性都成立。
组框通常由顶部带有标题的环绕框架组成。如果启用了该属性，大多数样式中只绘制框架的顶部;否则，绘制整个框架。
默认情况下，该属性被禁用，即除非明确指定，组框并非平坦的。
注：在某些风格中，平面和非平面组合盒的表示方式相似，可能不像其他样式那样易于区分。

**如何使用：** 调用 `flat()` 读取当前值；它不会修改应用状态。

### `title : QString`

**作用与语义：**

该属性包含组框标题文本。
如果标题包含一个&符号（'&'）后面跟一个字母，则该组框标题文本将带有键盘快捷键。
在上面的例子中，Alt U 将键盘焦点移到组框上。详情请参见 `QShortcut` 文档（要显示实际的 & 符号，请使用 '&&'）。
没有默认的标题文本。

**如何使用：** 调用 `title()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 g->setTitle("&User information");
```

### `[explicit] QGroupBox::QGroupBox(QWidget *parent = nullptr)`

**作用与语义：**

构建一个包含给定`parent`但无标题的组框小部件。

### `[explicit] QGroupBox::QGroupBox(const QString &title, QWidget *parent = nullptr)`

**作用与语义：**

构造一个包含给定`title`和`parent`的群盒。

### `[virtual noexcept] QGroupBox::~QGroupBox()`

**作用与语义：**

会摧毁群组盒子。

### `[override virtual protected] void QGroupBox::changeEvent(QEvent *ev)`

**作用与语义：**

重装：`QWidget::changeEvent`（QEvent *事件）。
该事件处理程序可以重新实现以处理状态变化。
该事件中被更改的状态可以通过提供的`event`检索。
变更事件包括：`QEvent::ToolBarChange`、`QEvent::ActivationChange`、`QEvent::EnabledChange`、`QEvent::FontChange`、`QEvent::StyleChange`、`QEvent::PaletteChange`、`QEvent::WindowTitleChange`、`QEvent::IconTextChange`、`QEvent::ModifiedChange`、`QEvent::MouseTrackingChange`、`QEvent::ParentChange`、`QEvent::WindowStateChange`、`QEvent::LanguageChange`、`QEvent::LocaleChange`、`QEvent::LayoutDirectionChange`、`QEvent::ReadOnlyChange`。

### `[override virtual protected] void QGroupBox::childEvent(QChildEvent *c)`

**作用与语义：**

重实现自：`QObject::childEvent`（QChildEvent *event）。

### `[signal] void QGroupBox::clicked(bool checked = false)`

**作用与语义：**

当激活复选框（即鼠标光标在按钮内时按下再松开）或快捷键输入时，会发出该信号。值得注意的是，如果你调用`setChecked()`，则不会发出该信号。
如果勾选了复选框，`checked`为真;如果未勾选该复选框，则为假。

### `[override virtual protected] bool QGroupBox::event(QEvent *e)`

**作用与语义：**

重实现自：`QWidget::event`（QEvent *事件）。

### `[override virtual protected] void QGroupBox::focusInEvent(QFocusEvent *fe)`

**作用与语义：**

重实现自：`QWidget::focusInEvent`（QFocusEvent *event）。
该事件处理程序可以在子类中重新实现，以接收控件的键盘焦点事件（焦点接收）。事件通过`event`参数传递。
小部件通常必须`setFocusPolicy()`到非`Qt::NoFocus`的对象才能接收焦点事件。（注意，应用程序员可以调用任何小部件`setFocus()`，即使是那些通常不接受焦点的小部件。）。
默认实现会更新小部件（除非是没有指定`focusPolicy()`的窗口）。

### `[virtual protected] void QGroupBox::initStyleOption(QStyleOptionGroupBox *option) const`

**作用与语义：**

用这个`QGroupBox`的值初始化`option`。这种方法适用于子类需要一个`QStyleOptionGroupBox`但不想自己填满所有信息时。

### `[override virtual] QSize QGroupBox::minimumSizeHint() const`

**作用与语义：**

重新实现属性的访问函数：`QWidget::minimumSizeHint`。

### `[override virtual protected] void QGroupBox::mouseMoveEvent(QMouseEvent *event)`

**作用与语义：**

重实现自：`QWidget::mouseMoveEvent`（QMouseEvent *event）。
该事件处理程序用于事件`event`，可以重新实现为子类，以接收该小部件的鼠标移动事件。
如果关闭鼠标追踪，只有在鼠标移动过程中按下鼠标按钮时才会发生鼠标移动事件。如果开启鼠标追踪，即使未按键，鼠标移动事件也会发生。
`QMouseEvent::position()`报告鼠标光标相对于该小部件的位置。对于按下和释放事件，位置通常与最后一次鼠标移动事件的位置相同，但如果用户的手握手，可能会有所不同。这是底层窗口系统的功能，而非Qt。
如果你想在鼠标移动时立即显示提示（例如，获取鼠标坐标与`QMouseEvent::position()`并显示为提示），你必须先启用上述的鼠标追踪功能。然后，为了确保提示立即更新，你必须在鼠标移动事件（mouseMoveEvent）实现中调用`QToolTip::showText()`而不是`setToolTip()`。

### `[override virtual protected] void QGroupBox::mousePressEvent(QMouseEvent *event)`

**作用与语义：**

重实现自：`QWidget::mousePressEvent`（QMouseEvent *event）。
该事件处理程序用于事件`event`，可以重新实现为子类，以接收该小部件的鼠标按键事件。
如果你在 mousePressEvent() 创建新控件，`mouseReleaseEvent()`可能不会出现在你预期的位置，这取决于底层窗口系统（或 X11 窗口管理器）、控件的位置，甚至可能还有其他因素。
默认实现实现了当你点击窗口外时关闭弹出小部件的功能。对于其他小部件类型，它没有任何作用。

### `[override virtual protected] void QGroupBox::mouseReleaseEvent(QMouseEvent *event)`

**作用与语义：**

重实现自：`QWidget::mouseReleaseEvent`（QMouseEvent *event）。
该事件处理程序用于事件`event`，可以重新实现为子类，以接收该小部件的鼠标释放事件。

### `[override virtual protected] void QGroupBox::paintEvent(QPaintEvent *event)`

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

### `[override virtual protected] void QGroupBox::resizeEvent(QResizeEvent *e)`

**作用与语义：**

重实现自：`QWidget::resizeEvent`（QResizeEvent *event）。
该事件处理程序可以在子类中重新实现，以接收通过 `event` 参数传递的控件调整大小事件。当调用 resizeEvent() 时，控件已经拥有新的几何体。旧的大小可以通过 `QResizeEvent::oldSize()` 访问。
控件会被擦除，并在处理调整尺寸事件后立即接收绘图事件。不需要（也不应该）在这个处理程序中进行绘图。

### `[signal] void QGroupBox::toggled(bool on)`

**作用与语义：**

该属性是否满足群组框的勾选。
如果组框可勾选，则以复选框显示。勾选该框时，组框的子节点被启用;否则，子节点被禁用，用户无法访问。
默认情况下，可勾选的组组选项也会被勾选。
注意：当取消勾选该选项时，组框本身不会被禁用，你可以在未勾选的组框中明确启用单个子节点。但这不推荐，因为这可能会给最终用户带来意外体验。

**如何使用：** 调用 `toggled()` 读取当前值；它不会修改应用状态。

### `Qt::Alignment alignment() const`

**作用与语义：**

该属性表示了组框标题的对齐。
大多数样式将标题置于画面顶部。标题的水平对齐可用以下列表中的单个值来指定：
- `Qt::AlignLeft` 将标题文本与组框的左侧对齐。
- `Qt::AlignRight` 将标题文本与组框的右侧对齐。
- `Qt::AlignHCenter` 将标题文本与组框的水平中心对齐。
默认阵营是`Qt::AlignLeft`。

**如何使用：** 调用 `alignment()` 读取当前值；它不会修改应用状态。

### `bool isCheckable() const`

**作用与语义：**

该属性决定该组方块标题中是否包含复选框。
如果该属性被`true`，组框会用复选框代替普通标签显示标题。如果勾选该复选框，则该组框的子节点被启用;否则，子节点被禁用且无法访问。
默认情况下，组组方框不可勾选。
如果该属性为组框启用，也会初步检查以确保其内容已被启用。

**如何使用：** 调用 `isCheckable()` 读取当前值；它不会修改应用状态。

### `bool isChecked() const`

**作用与语义：**

该属性是否满足群组框的勾选。
如果组框可勾选，则以复选框显示。勾选该框时，组框的子节点被启用;否则，子节点被禁用，用户无法访问。
默认情况下，可勾选的组组选项也会被勾选。
注意：当取消勾选该选项时，组框本身不会被禁用，你可以在未勾选的组框中明确启用单个子节点。但这不推荐，因为这可能会给最终用户带来意外体验。

**如何使用：** 调用 `isChecked()` 读取当前值；它不会修改应用状态。

### `bool isFlat() const`

**作用与语义：**

无论分组盒是平整的还是有框架，这一属性都成立。
组框通常由顶部带有标题的环绕框架组成。如果启用了该属性，大多数样式中只绘制框架的顶部;否则，绘制整个框架。
默认情况下，该属性被禁用，即除非明确指定，组框并非平坦的。
注：在某些风格中，平面和非平面组合盒的表示方式相似，可能不像其他样式那样易于区分。

**如何使用：** 调用 `isFlat()` 读取当前值；它不会修改应用状态。

### `void setAlignment(int alignment)`

**作用与语义：**

该属性表示了组框标题的对齐。
大多数样式将标题置于画面顶部。标题的水平对齐可用以下列表中的单个值来指定：
- `Qt::AlignLeft` 将标题文本与组框的左侧对齐。
- `Qt::AlignRight` 将标题文本与组框的右侧对齐。
- `Qt::AlignHCenter` 将标题文本与组框的水平中心对齐。
默认阵营是`Qt::AlignLeft`。

**如何使用：** 调用 `setAlignment(...)` 修改 `alignment`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setCheckable(bool checkable)`

**作用与语义：**

该属性决定该组方块标题中是否包含复选框。
如果该属性被`true`，组框会用复选框代替普通标签显示标题。如果勾选该复选框，则该组框的子节点被启用;否则，子节点被禁用且无法访问。
默认情况下，组组方框不可勾选。
如果该属性为组框启用，也会初步检查以确保其内容已被启用。

**如何使用：** 调用 `setCheckable(...)` 修改 `checkable`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setFlat(bool flat)`

**作用与语义：**

无论分组盒是平整的还是有框架，这一属性都成立。
组框通常由顶部带有标题的环绕框架组成。如果启用了该属性，大多数样式中只绘制框架的顶部;否则，绘制整个框架。
默认情况下，该属性被禁用，即除非明确指定，组框并非平坦的。
注：在某些风格中，平面和非平面组合盒的表示方式相似，可能不像其他样式那样易于区分。

**如何使用：** 调用 `setFlat(...)` 修改 `flat`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTitle(const QString &title)`

**作用与语义：**

该属性包含组框标题文本。
如果标题包含一个&符号（'&'）后面跟一个字母，则该组框标题文本将带有键盘快捷键。
在上面的例子中，Alt U 将键盘焦点移到组框上。详情请参见 `QShortcut` 文档（要显示实际的 & 符号，请使用 '&&'）。
没有默认的标题文本。

**如何使用：** 调用 `setTitle(...)` 修改 `title`；传入的新值会成为后续查询和相关界面行为所使用的值。

**官方示例：**

```cpp
 g->setTitle("&User information");
```

### `QString title() const`

**作用与语义：**

该属性包含组框标题文本。
如果标题包含一个&符号（'&'）后面跟一个字母，则该组框标题文本将带有键盘快捷键。
在上面的例子中，Alt U 将键盘焦点移到组框上。详情请参见 `QShortcut` 文档（要显示实际的 & 符号，请使用 '&&'）。
没有默认的标题文本。

**如何使用：** 调用 `title()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 g->setTitle("&User information");
```

### `void setChecked(bool checked)`

**作用与语义：**

该属性是否满足群组框的勾选。
如果组框可勾选，则以复选框显示。勾选该框时，组框的子节点被启用;否则，子节点被禁用，用户无法访问。
默认情况下，可勾选的组组选项也会被勾选。
注意：当取消勾选该选项时，组框本身不会被禁用，你可以在未勾选的组框中明确启用单个子节点。但这不推荐，因为这可能会给最终用户带来意外体验。

**如何使用：** 调用 `setChecked(...)` 修改 `checked`；传入的新值会成为后续查询和相关界面行为所使用的值。

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

`QGroupBox` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
