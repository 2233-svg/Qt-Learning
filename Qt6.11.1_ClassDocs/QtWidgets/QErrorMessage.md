# QErrorMessage

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QErrorMessage` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QErrorMessage` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QErrorMessage>`
- 继承自：QDialog
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

- `QErrorMessage(QWidget *parent = nullptr)`
- `virtual ~QErrorMessage()`

### 公有槽函数

- `void showMessage(const QString &message)`
- `void showMessage(const QString &message, const QString &type)`

### 静态公有成员

- `QErrorMessage * qtHandler()`

### 重实现的保护函数

- `virtual void changeEvent(QEvent *e) override`
- `virtual void done(int a) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[explicit] QErrorMessage::QErrorMessage(QWidget *parent = nullptr)`

**作用与语义：**

构造并安装带有给定`parent`的错误处理窗口。
对话的默认窗口模态取决于平台。窗口模态可以通过调用`setWindowModality()`覆盖`showMessage()`。

### `[virtual noexcept] QErrorMessage::~QErrorMessage()`

**作用与语义：**

会破坏错误信息对话框。

### `[override virtual protected] void QErrorMessage::changeEvent(QEvent *e)`

**作用与语义：**

重装：`QWidget::changeEvent`（QEvent *事件）。
该事件处理程序可以重新实现以处理状态变化。
该事件中被更改的状态可以通过提供的`event`检索。
变更事件包括：`QEvent::ToolBarChange`、`QEvent::ActivationChange`、`QEvent::EnabledChange`、`QEvent::FontChange`、`QEvent::StyleChange`、`QEvent::PaletteChange`、`QEvent::WindowTitleChange`、`QEvent::IconTextChange`、`QEvent::ModifiedChange`、`QEvent::MouseTrackingChange`、`QEvent::ParentChange`、`QEvent::WindowStateChange`、`QEvent::LanguageChange`、`QEvent::LocaleChange`、`QEvent::LayoutDirectionChange`、`QEvent::ReadOnlyChange`。

### `[override virtual protected] void QErrorMessage::done(int a)`

**作用与语义：**

重装：`QDialog::done`（int r）。
关闭对话并将结果代码设置为`r`。`finished()`信号会发出`r`;如果`r`是`QDialog::Accepted`或`QDialog::Rejected`，则分别会发出`accepted()`或`rejected()`信号。
如果该对话以`exec()`显示，done() 也会导致本地事件循环结束，`exec()`返回`r`。
与`QWidget::close()`一样，如果设置了`Qt::WA_DeleteOnClose`标志，done() 会删除对话。如果对话框是应用程序的主控件，应用程序将终止。如果对话框是最后关闭的窗口，则发出`QGuiApplication::lastWindowClosed()`信号。

### `[static] QErrorMessage *QErrorMessage::qtHandler()`

**作用与语义：**

返回指向一个`QErrorMessage`对象的指针，输出默认的Qt消息。如果没有这样的对象，这个函数会创建这样的对象。
该对象只输出`QLoggingCategory::defaultCategory()`的日志消息。
该对象会将所有消息转发给原始消息处理器。

### `[slot] void QErrorMessage::showMessage(const QString &message)`

**作用与语义：**

显示给定消息，`message`，并立即返回。如果用户请求不再显示该消息，该功能无效。
通常，消息会立即显示。但如果有待处理消息，则会排队稍后显示。
注意：该槽位已超载。连接该槽位：


使用 qOverload 连接：
connect（sender， &SenderClass：：signal，。
errorMessage， qOverload（&QErrorMessage：：showMessage））;

或者用lambda作为包装器：
connect（sender， &SenderClass：：signal，。
errorMessage， [receiver = errorMessage]（const QString &message） { receiver->showMessage（message）; }）;


更多示例和方法，请参见连接超载槽位。

### `[slot] void QErrorMessage::showMessage(const QString &message, const QString &type)`

**作用与语义：**

显示给定消息`message`，并立即返回。如果用户请求的消息类型为 `type`，且不再显示，该函数不做任何事。
通常，消息会立即显示。但如果有待处理消息，则会排队稍后显示。
注意：该槽位已超载。连接该槽位：


使用 qOverload 连接：
connect（sender， &SenderClass：：signal，。
errorMessage， qOverload（&QErrorMessage：：showMessage））;

或者用lambda作为包装器：
connect（sender， &SenderClass：：signal，。
errorMessage， [receiver = errorMessage]（const QString &message， const QString &type） { receiver->showMessage（message， type）; }）;


更多示例和方法，请参见连接超载槽位。

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

`QErrorMessage` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
