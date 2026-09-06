# QSplashScreen

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QSplashScreen` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QSplashScreen` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QSplashScreen>`
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

### 公有函数

- `QSplashScreen(const QPixmap &pixmap = QPixmap(), Qt::WindowFlags f = Qt::WindowFlags())`
- `QSplashScreen(QScreen *screen, const QPixmap &pixmap = QPixmap(), Qt::WindowFlags f = Qt::WindowFlags())`
- `virtual ~QSplashScreen()`
- `void finish(QWidget *mainWin)`
- `QString message() const`
- `const QPixmap pixmap() const`
- `void repaint()`
- `void setPixmap(const QPixmap &pixmap)`

### 公有槽函数

- `void clearMessage()`
- `void showMessage(const QString &message, int alignment = Qt::AlignLeft, const QColor &color = Qt::black)`

### 信号

- `void messageChanged(const QString &message)`

### 保护函数

- `virtual void drawContents(QPainter *painter)`

### 重实现的保护函数

- `virtual bool event(QEvent *e) override`
- `virtual void mousePressEvent(QMouseEvent *) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[explicit] QSplashScreen::QSplashScreen(const QPixmap &pixmap = QPixmap(), Qt::WindowFlags f = Qt::WindowFlags())`

**作用与语义：**

制作一个启动画面来显示`pixmap`。
`f`，除了可能`Qt::WindowStaysOnTopHint`之外，根本不需要设置小部件标志。

### `QSplashScreen::QSplashScreen(QScreen *screen, const QPixmap &pixmap = QPixmap(), Qt::WindowFlags f = Qt::WindowFlags())`

**作用与语义：**

这个功能允许你指定启动画面的画面。这个构造函数的典型用途是你有多个屏幕，并且希望启动画面出现在与主屏幕不同的画面上。在这种情况下，请通过相应的`screen`。

### `[virtual noexcept] QSplashScreen::~QSplashScreen()`

**作用与语义：**

毁灭者。

### `[slot] void QSplashScreen::clearMessage()`

**作用与语义：**

移除启动画面上显示的提示。

### `[virtual protected] void QSplashScreen::drawContents(QPainter *painter)`

**作用与语义：**

用画家`painter`绘制启动画面的内容。默认实现会绘制`showMessage()`传递的消息。如果你想在启动画面上自己画，可以重新实现这个功能。

### `[override virtual protected] bool QSplashScreen::event(QEvent *e)`

**作用与语义：**

重实现自：`QWidget::event`（QEvent *事件）。

### `void QSplashScreen::finish(QWidget *mainWin)`

**作用与语义：**

它会让启动画面等到小部件`mainWin`显示出来后，才调用`close()`。

### `QString QSplashScreen::message() const`

**作用与语义：**

返回当前启动画面上显示的消息。

### `[signal] void QSplashScreen::messageChanged(const QString &message)`

**作用与语义：**

当启动画面上的消息发生变化时，该信号会发出。`message` 是新消息，当消息被移除时则是空字符串。

### `[override virtual protected] void QSplashScreen::mousePressEvent(QMouseEvent *)`

**作用与语义：**

重实现自：`QWidget::mousePressEvent`（QMouseEvent *event）。
该事件处理程序用于事件`event`，可以重新实现为子类，以接收该小部件的鼠标按键事件。
如果你在 mousePressEvent() 创建新控件，`mouseReleaseEvent()`可能不会出现在你预期的位置，这取决于底层窗口系统（或 X11 窗口管理器）、控件的位置，甚至可能还有其他因素。
默认实现实现了当你点击窗口外时关闭弹出小部件的功能。对于其他小部件类型，它没有任何作用。

### `const QPixmap QSplashScreen::pixmap() const`

**作用与语义：**

返回启动画面中使用的像素映射。图像中没有`showMessage()`调用绘制的任何文本。

### `void QSplashScreen::repaint()`

**作用与语义：**

这会覆盖`QWidget::repaint()`。它与标准的重绘函数不同之处在于，它也会调用`QCoreApplication::processEvents()`确保更新显示，即使没有事件循环。

### `void QSplashScreen::setPixmap(const QPixmap &pixmap)`

**作用与语义：**

将用作启动画面图像的像素地图设置为`pixmap`。

### `[slot] void QSplashScreen::showMessage(const QString &message, int alignment = Qt::AlignLeft, const QColor &color = Qt::black)`

**作用与语义：**

将`message`文本绘制到启动画面上，并`color`颜色，并根据`alignment`中的标志对齐文本。该函数调用`repaint()`确保启动画面立即重新绘制。因此，消息会随着你的应用程序正在做的事情（例如加载文件）保持最新状态。

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

`QSplashScreen` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
