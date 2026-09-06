# QFrame

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QFrame` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QFrame` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QFrame>`
- 继承自：QWidget
- 直接派生类：QAbstractScrollArea、QLabel、QLCDNumber、QSplitter、QStackedWidget,、QToolBox

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

### 公有类型

- `enum Shadow { Plain, Raised, Sunken }`
- `enum Shape { NoFrame, Box, Panel, StyledPanel, HLine, …, WinPanel }`
- `enum StyleMask { Shadow_Mask, Shape_Mask }`

### 属性

- `frameRect : QRect`
- `frameShadow : Shadow`
- `frameShape : Shape`
- `frameWidth : int`
- `lineWidth : int`
- `midLineWidth : int`

### 公有函数

- `QFrame(QWidget *parent = nullptr, Qt::WindowFlags f = Qt::WindowFlags())`
- `virtual ~QFrame()`
- `QRect frameRect() const`
- `QFrame::Shadow frameShadow() const`
- `QFrame::Shape frameShape() const`
- `int frameStyle() const`
- `int frameWidth() const`
- `int lineWidth() const`
- `int midLineWidth() const`
- `void setFrameRect(const QRect &)`
- `void setFrameShadow(QFrame::Shadow)`
- `void setFrameShape(QFrame::Shape)`
- `void setFrameStyle(int style)`
- `void setLineWidth(int)`
- `void setMidLineWidth(int)`

### 重实现的公有函数

- `virtual QSize sizeHint() const override`

### 保护函数

- `virtual void initStyleOption(QStyleOptionFrame *option) const`

### 重实现的保护函数

- `virtual void changeEvent(QEvent *ev) override`
- `virtual bool event(QEvent *e) override`
- `virtual void paintEvent(QPaintEvent *) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QFrame::Shadow`

**作用与语义：**

这个枚举类型定义了用于赋予帧3D效果的阴影类型。
- `QFrame::Plain`：`0x0010`;画面和内容看起来与周围环境齐平;使用调色板绘制`QPalette::WindowText`颜色（无任何3D效果）
- `QFrame::Raised`：`0x0020`;画面和内容看起来凸起;利用当前色组的明暗颜色绘制3D凸起线条
- `QFrame::Sunken`：`0x0030`;画面和内容物看起来沉没;利用当前色组的明暗颜色绘制三维凹陷线
Shadow 与 `QFrame::Shape`、`lineWidth()` 和 `midLineWidth()` 互动。请参见主类文档中的框架图片。

### `enum QFrame::Shape`

**作用与语义：**

该枚举类型定义了可用的框架形状。
- `QFrame::NoFrame`：`0`;`QFrame` 不抽牌
- `QFrame::Box`：`0x0001`;`QFrame` 在箱子周围画一个盒子
- `QFrame::Panel`：`0x0002`;`QFrame`绘制一格，使内容物看起来凸起或沉没
- `QFrame::StyledPanel`：`0x0006`;绘制一个矩形面板，外观取决于当前的图形界面样式。面板可以升起或下沉。
- `QFrame::HLine`：`0x0004`;`QFrame` 绘制一条水平线，没有框定任何东西（作为分隔符非常有用）
- `QFrame::VLine`：`0x0005`;`QFrame` 绘制一条垂直线，没有框出任何框架（作为分隔符非常有用）
- `QFrame::WinPanel`：`0x0003`;绘制一个矩形面板，可以像Windows 2000一样抬高或下沉。指定该形状会将线宽设置为2像素。为兼容性提供了WinPanel。为了图形界面风格的独立性，我们建议使用StyledPanel。
当它没有调用`QStyle`时，Shape 会与 `QFrame::Shadow`、`lineWidth()` 和 `midLineWidth()` 交互，生成整体结果。请参见主类文档中的框架图片。

### `enum QFrame::StyleMask`

**作用与语义：**

该枚举定义了两个常数，可用于提取`frameStyle()`的两个分量：
- `QFrame::Shadow_Mask`：`0x00f0`;`frameStyle()`的`Shadow`部分
- `QFrame::Shape_Mask`：`0x000f`;`frameStyle()`的`Shape`部分
通常你不需要用这些，因为`frameShadow()`和`frameShape()`已经提取了`frameStyle()`的 `Shadow` 和 `Shape` 部分。

### `frameRect : QRect`

**作用与语义：**

该属性表示框架的矩形。
框架的矩形是画框所在的矩形。默认情况下，它是整个控件。设置矩形不会导致控件更新。控件大小变化时，框架矩形会自动调整。
如果你将矩形设置为空矩形（例如，`QRect`（0， 0， 0， 0）），那么生成的帧矩形等价于控件矩形。

**如何使用：** 调用 `frameRect()` 读取当前值；它不会修改应用状态。

### `frameShadow : Shadow`

**作用与语义：**

该属性保留了帧样式中的影格阴影值。

**如何使用：** 调用 `frameShadow()` 读取当前值；它不会修改应用状态。

### `frameShape : Shape`

**作用与语义：**

该属性表示框架样式的框架形状值。

**如何使用：** 调用 `frameShape()` 读取当前值；它不会修改应用状态。

### `[read-only] frameWidth : int`

**作用与语义：**

该属性决定绘制的帧宽度。
注意，框架宽度取决于框架样式，而不仅仅是线宽和中线宽度。例如，`NoFrame`指定的样式的帧宽度始终为0，而样式`Panel`的帧宽度等同于线宽。

**如何使用：** 调用 `frameWidth()` 读取当前值；它不会修改应用状态。

### `lineWidth : int`

**作用与语义：**

该属性表示线宽。
注意，用作分隔符的帧（`HLine`和`VLine`）的总线宽由`frameWidth`规定。
默认值是1。

**如何使用：** 调用 `lineWidth()` 读取当前值；它不会修改应用状态。

### `midLineWidth : int`

**作用与语义：**

该属性表示中线宽度。
默认值是0。

**如何使用：** 调用 `midLineWidth()` 读取当前值；它不会修改应用状态。

### `[explicit] QFrame::QFrame(QWidget *parent = nullptr, Qt::WindowFlags f = Qt::WindowFlags())`

**作用与语义：**

构建一个带有框架样式`NoFrame`和1像素宽度的框架控件。
`parent`和`f`参数传递给`QWidget`构造器。

### `[virtual noexcept] QFrame::~QFrame()`

**作用与语义：**

毁了车架。

### `[override virtual protected] void QFrame::changeEvent(QEvent *ev)`

**作用与语义：**

重装：`QWidget::changeEvent`（QEvent *事件）。
该事件处理程序可以重新实现以处理状态变化。
该事件中被更改的状态可以通过提供的`event`检索。
变更事件包括：`QEvent::ToolBarChange`、`QEvent::ActivationChange`、`QEvent::EnabledChange`、`QEvent::FontChange`、`QEvent::StyleChange`、`QEvent::PaletteChange`、`QEvent::WindowTitleChange`、`QEvent::IconTextChange`、`QEvent::ModifiedChange`、`QEvent::MouseTrackingChange`、`QEvent::ParentChange`、`QEvent::WindowStateChange`、`QEvent::LanguageChange`、`QEvent::LocaleChange`、`QEvent::LayoutDirectionChange`、`QEvent::ReadOnlyChange`。

### `[override virtual protected] bool QFrame::event(QEvent *e)`

**作用与语义：**

重实现自：`QWidget::event`（QEvent *事件）。

### `int QFrame::frameStyle() const`

**作用与语义：**

还原了框架样式。
默认值是`QFrame::Plain`。

### `[virtual protected] void QFrame::initStyleOption(QStyleOptionFrame *option) const`

**作用与语义：**

用`QFrame`的值初始化`option`。这种方法适用于子类需要`QStyleOptionFrame`但不想自己填写所有信息时。

### `[override virtual protected] void QFrame::paintEvent(QPaintEvent *)`

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

### `void QFrame::setFrameStyle(int style)`

**作用与语义：**

将框架样式设置为`style`。
`style`是帧形状和帧阴影样式之间的位元或。参见主类文档中的帧图片。
框架形状以`QFrame::Shape`表示，阴影样式以 `QFrame::Shadow` 表示。
如果指定中线宽度大于0，则为`Raised`或`Sunken` `Box`、`HLine`和`VLine`帧绘制额外线条。当前颜色组的中间色用于绘制中间线条。

### `[override virtual] QSize QFrame::sizeHint() const`

**作用与语义：**

重新实现了属性的访问函数：`QWidget::sizeHint`。

### `QRect frameRect() const`

**作用与语义：**

该属性表示框架的矩形。
框架的矩形是画框所在的矩形。默认情况下，它是整个控件。设置矩形不会导致控件更新。控件大小变化时，框架矩形会自动调整。
如果你将矩形设置为空矩形（例如，`QRect`（0， 0， 0， 0）），那么生成的帧矩形等价于控件矩形。

**如何使用：** 调用 `frameRect()` 读取当前值；它不会修改应用状态。

### `QFrame::Shadow frameShadow() const`

**作用与语义：**

该属性保留了帧样式中的影格阴影值。

**如何使用：** 调用 `frameShadow()` 读取当前值；它不会修改应用状态。

### `QFrame::Shape frameShape() const`

**作用与语义：**

该属性表示框架样式的框架形状值。

**如何使用：** 调用 `frameShape()` 读取当前值；它不会修改应用状态。

### `int frameWidth() const`

**作用与语义：**

该属性决定绘制的帧宽度。
注意，框架宽度取决于框架样式，而不仅仅是线宽和中线宽度。例如，`NoFrame`指定的样式的帧宽度始终为0，而样式`Panel`的帧宽度等同于线宽。

**如何使用：** 调用 `frameWidth()` 读取当前值；它不会修改应用状态。

### `int lineWidth() const`

**作用与语义：**

该属性表示线宽。
注意，用作分隔符的帧（`HLine`和`VLine`）的总线宽由`frameWidth`规定。
默认值是1。

**如何使用：** 调用 `lineWidth()` 读取当前值；它不会修改应用状态。

### `int midLineWidth() const`

**作用与语义：**

该属性表示中线宽度。
默认值是0。

**如何使用：** 调用 `midLineWidth()` 读取当前值；它不会修改应用状态。

### `void setFrameRect(const QRect &)`

**作用与语义：**

该属性表示框架的矩形。
框架的矩形是画框所在的矩形。默认情况下，它是整个控件。设置矩形不会导致控件更新。控件大小变化时，框架矩形会自动调整。
如果你将矩形设置为空矩形（例如，`QRect`（0， 0， 0， 0）），那么生成的帧矩形等价于控件矩形。

**如何使用：** 调用 `setFrameRect(...)` 修改 `frameRect`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setFrameShadow(QFrame::Shadow)`

**作用与语义：**

该属性保留了帧样式中的影格阴影值。

**如何使用：** 调用 `setFrameShadow(...)` 修改 `frameShadow`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setFrameShape(QFrame::Shape)`

**作用与语义：**

该属性表示框架样式的框架形状值。

**如何使用：** 调用 `setFrameShape(...)` 修改 `frameShape`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setLineWidth(int)`

**作用与语义：**

该属性表示线宽。
注意，用作分隔符的帧（`HLine`和`VLine`）的总线宽由`frameWidth`规定。
默认值是1。

**如何使用：** 调用 `setLineWidth(...)` 修改 `lineWidth`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMidLineWidth(int)`

**作用与语义：**

该属性表示中线宽度。
默认值是0。

**如何使用：** 调用 `setMidLineWidth(...)` 修改 `midLineWidth`；传入的新值会成为后续查询和相关界面行为所使用的值。

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

`QFrame` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
