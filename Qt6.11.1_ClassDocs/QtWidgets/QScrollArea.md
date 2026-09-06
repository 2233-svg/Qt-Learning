# QScrollArea

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QScrollArea` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QScrollArea` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QScrollArea>`
- 继承自：QAbstractScrollArea
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
- `widgetResizable : bool`

### 公有函数

- `QScrollArea(QWidget *parent = nullptr)`
- `virtual ~QScrollArea()`
- `Qt::Alignment alignment() const`
- `void ensureVisible(int x, int y, int xmargin = 50, int ymargin = 50)`
- `void ensureWidgetVisible(QWidget *childWidget, int xmargin = 50, int ymargin = 50)`
- `void setAlignment(Qt::Alignment)`
- `void setWidget(QWidget *widget)`
- `void setWidgetResizable(bool resizable)`
- `QWidget * takeWidget()`
- `QWidget * widget() const`
- `bool widgetResizable() const`

### 重实现的公有函数

- `virtual bool focusNextPrevChild(bool next) override`
- `virtual QSize sizeHint() const override`

### 重实现的保护函数

- `virtual bool event(QEvent *e) override`
- `virtual bool eventFilter(QObject *o, QEvent *e) override`
- `virtual void resizeEvent(QResizeEvent *) override`
- `virtual void scrollContentsBy(int dx, int dy) override`
- `virtual QSize viewportSizeHint() const override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `alignment : Qt::Alignment`

**作用与语义：**

该属性包含滚动区域控件的对齐。
有效的对齐是以下标志的组合：
- `Qt::AlignLeft`
- `Qt::AlignHCenter`
- `Qt::AlignRight`
- `Qt::AlignTop`
- `Qt::AlignVCenter`
- `Qt::AlignBottom`
默认情况下，小部件会固定在滚动区域的左上角。

**如何使用：** 调用 `alignment()` 读取当前值；它不会修改应用状态。

### `widgetResizable : bool`

**作用与语义：**

该属性决定滚动区域是否应调整视图控件大小。
如果该属性设置为 false（默认），滚动区域会尊重其控件的大小。无论该属性如何，你都可以用 `widget()`->`resize()` 程序调整控件大小，滚动区域会自动调整到新的大小。
如果该属性设置为 true，滚动区域会自动调整控件大小，以避免滚动条出现，或利用额外空间。

**如何使用：** 调用 `widgetResizable()` 读取当前值；它不会修改应用状态。

### `[explicit] QScrollArea::QScrollArea(QWidget *parent = nullptr)`

**作用与语义：**

用给定的`parent`构建一个空白卷轴区域。

### `[virtual noexcept] QScrollArea::~QScrollArea()`

**作用与语义：**

销毁滚动区域及其子控件。

### `void QScrollArea::ensureVisible(int x, int y, int xmargin = 50, int ymargin = 50)`

**作用与语义：**

滚动滚动区域的内容，使得点（`x`、`y`）在视口区域内可见，边距以像素为单位，`xmargin`和`ymargin`。如果无法到达指定点，内容会滚动到最近的有效位置。两个边距的默认值为50像素。

### `void QScrollArea::ensureWidgetVisible(QWidget *childWidget, int xmargin = 50, int ymargin = 50)`

**作用与语义：**

滚动滚动区域内容，使`QScrollArea::widget()`的 `childWidget` 在视口内可见，边距以像素为单位，`xmargin` 和 `ymargin` 指定。如果无法到达指定点，内容会滚动到最近的有效位置。两个边距的默认值为 50 像素。

### `[override virtual protected] bool QScrollArea::event(QEvent *e)`

**作用与语义：**

重装：`QAbstractScrollArea::event`（QEvent *事件）。

### `[override virtual protected] bool QScrollArea::eventFilter(QObject *o, QEvent *e)`

**作用与语义：**

重装：`QObject::eventFilter`（QObject *已观看，QEvent *事件）。

### `[override virtual] bool QScrollArea::focusNextPrevChild(bool next)`

**作用与语义：**

重构：`QWidget::focusNextPrevChild`（下一个布尔）。
根据 Tab 和 Shift Tab 找到一个新的控件来给键盘焦点，如果能找到新控件，则返回 `true`，找不到则返回 false。
如果`next`为真，该函数向前搜索;如果`next`为假，则向后搜索。
有时，你会想重新实现这个函数。例如，浏览器可能会重新实现它，将“当前活跃链接”向前或向后移动，只有当它到达“页面”的最后或第一个链接时才调用 focusNextPrevChild()。
子控件调用其父控件的 focusNextPrevChild()，但只有包含子控件的窗口决定将焦点重定向到哪里。通过重新实现该函数，你就能控制所有子控件的焦点遍历。

### `[override virtual protected] void QScrollArea::resizeEvent(QResizeEvent *)`

**作用与语义：**

重实现自：`QAbstractScrollArea::resizeEvent`（QResizeEvent *event）。

### `[override virtual protected] void QScrollArea::scrollContentsBy(int dx, int dy)`

**作用与语义：**

重实现自：`QAbstractScrollArea::scrollContentsBy`（智力 dx，智力 dy）。
当滚动条被移动`dx`、`dy`时调用，因此视口内容应相应滚动。
默认实现只需调用整个`viewport()`的`update()`，子类可以重新实现该处理程序以优化，或者像`QScrollArea`一样移动内容控件。参数`dx`和`dy`是为了方便，让类知道应该滚动多少（比如像素移动时很有用）。你也可以忽略这些值，直接滚动到滚动条指示的位置。
调用该函数进行程序滚动是错误，建议使用滚动条（例如直接调用`QScrollBar::setValue()`）。

### `void QScrollArea::setWidget(QWidget *widget)`

**作用与语义：**

设定卷轴区域的`widget`。
`widget`会成为滚动区域的子节点，当滚动区域被删除或设置新控件时，会被销毁。
小部件的 `autoFillBackground` 属性将设置为 `true`。
如果滚动区域在添加`widget`时可见，必须明确`show()`。
注意，你必须在调用该函数前添加`widget`的布局;如果后来添加，`widget`将不可见——无论你何时`show()`滚动区域。在这种情况下，你也不能之后`show()` `widget`。

### `[override virtual] QSize QScrollArea::sizeHint() const`

**作用与语义：**

重装：`QAbstractScrollArea::sizeHint()` const.

### `QWidget *QScrollArea::takeWidget()`

**作用与语义：**

移除滚动区域的小部件，并将小部件的所有权转交给调用者。

### `[override virtual protected] QSize QScrollArea::viewportSizeHint() const`

**作用与语义：**

重装：`QAbstractScrollArea::viewportSizeHint()` const.
返回视口推荐大小。默认实现返回`viewport()`->`sizeHint()`。注意，大小仅为视口大小，没有可见的滚动条。

### `QWidget *QScrollArea::widget() const`

**作用与语义：**

返回滚动区域的小部件，或者如果没有则返回`nullptr`。

### `Qt::Alignment alignment() const`

**作用与语义：**

该属性包含滚动区域控件的对齐。
有效的对齐是以下标志的组合：
- `Qt::AlignLeft`
- `Qt::AlignHCenter`
- `Qt::AlignRight`
- `Qt::AlignTop`
- `Qt::AlignVCenter`
- `Qt::AlignBottom`
默认情况下，小部件会固定在滚动区域的左上角。

**如何使用：** 调用 `alignment()` 读取当前值；它不会修改应用状态。

### `void setAlignment(Qt::Alignment)`

**作用与语义：**

该属性包含滚动区域控件的对齐。
有效的对齐是以下标志的组合：
- `Qt::AlignLeft`
- `Qt::AlignHCenter`
- `Qt::AlignRight`
- `Qt::AlignTop`
- `Qt::AlignVCenter`
- `Qt::AlignBottom`
默认情况下，小部件会固定在滚动区域的左上角。

**如何使用：** 调用 `setAlignment(...)` 修改 `alignment`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setWidgetResizable(bool resizable)`

**作用与语义：**

该属性决定滚动区域是否应调整视图控件大小。
如果该属性设置为 false（默认），滚动区域会尊重其控件的大小。无论该属性如何，你都可以用 `widget()`->`resize()` 程序调整控件大小，滚动区域会自动调整到新的大小。
如果该属性设置为 true，滚动区域会自动调整控件大小，以避免滚动条出现，或利用额外空间。

**如何使用：** 调用 `setWidgetResizable(...)` 修改 `widgetResizable`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `bool widgetResizable() const`

**作用与语义：**

该属性决定滚动区域是否应调整视图控件大小。
如果该属性设置为 false（默认），滚动区域会尊重其控件的大小。无论该属性如何，你都可以用 `widget()`->`resize()` 程序调整控件大小，滚动区域会自动调整到新的大小。
如果该属性设置为 true，滚动区域会自动调整控件大小，以避免滚动条出现，或利用额外空间。

**如何使用：** 调用 `widgetResizable()` 读取当前值；它不会修改应用状态。

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

`QScrollArea` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
