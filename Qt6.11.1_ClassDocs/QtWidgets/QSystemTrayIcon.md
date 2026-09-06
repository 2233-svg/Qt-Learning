# QSystemTrayIcon

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QSystemTrayIcon` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QSystemTrayIcon` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QSystemTrayIcon>`
- 继承自：QObject
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

### 公有类型

- `enum ActivationReason { Unknown, Context, DoubleClick, Trigger, MiddleClick }`
- `enum MessageIcon { NoIcon, Information, Warning, Critical }`

### 属性

- `icon : QIcon`
- `toolTip : QString`
- `visible : bool`

### 公有函数

- `QSystemTrayIcon(QObject *parent = nullptr)`
- `QSystemTrayIcon(const QIcon &icon, QObject *parent = nullptr)`
- `virtual ~QSystemTrayIcon()`
- `QMenu * contextMenu() const`
- `QRect geometry() const`
- `QIcon icon() const`
- `bool isVisible() const`
- `void setContextMenu(QMenu *menu)`
- `void setIcon(const QIcon &icon)`
- `void setToolTip(const QString &tip)`
- `QString toolTip() const`

### 公有槽函数

- `void hide()`
- `void setVisible(bool visible)`
- `void show()`
- `void showMessage(const QString &title, const QString &message, QSystemTrayIcon::MessageIcon icon = QSystemTrayIcon::Information, int millisecondsTimeoutHint = 10000)`
- `void showMessage(const QString &title, const QString &message, const QIcon &icon, int millisecondsTimeoutHint = 10000)`

### 信号

- `void activated(QSystemTrayIcon::ActivationReason reason)`
- `void messageClicked()`

### 静态公有成员

- `bool isSystemTrayAvailable()`
- `bool supportsMessages()`

### 重实现的保护函数

- `virtual bool event(QEvent *e) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QSystemTrayIcon::ActivationReason`

**作用与语义：**

这个枚举描述了系统托盘被激活的原因。
- `QSystemTrayIcon::Unknown`：`0`;原因不明
- `QSystemTrayIcon::Context`：`1`;系统托盘输入的上下文菜单被请求
- `QSystemTrayIcon::DoubleClick`：`2`;系统托盘条目被双击。
注意：在macOS上，只有在没有设置右键菜单时才会发出双击声，因为菜单是按鼠标打开的。
- `QSystemTrayIcon::Trigger`：`3`;点击系统托盘条目
- `QSystemTrayIcon::MiddleClick`：`4`;系统托盘输入用鼠标中键点击

### `enum QSystemTrayIcon::MessageIcon`

**作用与语义：**

该枚举描述了显示气泡消息时显示的图标。
- `QSystemTrayIcon::NoIcon`：`0`;不显示任何图标。
- `QSystemTrayIcon::Information`：`1`;显示信息图标。
- `QSystemTrayIcon::Warning`：`2`;显示标准警告图标。
- `QSystemTrayIcon::Critical`：`3`;显示一个关键警告图标。

### `icon : QIcon`

**作用与语义：**

该属性保留系统托盘图标。
在Windows上，系统托盘图标大小为16x16;在X11上，首选尺寸为22x22。图标将根据需要缩放至相应大小。

**如何使用：** 调用 `icon()` 读取当前值；它不会修改应用状态。

### `toolTip : QString`

**作用与语义：**

该属性包含系统托盘输入的工具提示。
在某些系统上，提示长度是有限的。如有需要，提示会被截断。

**如何使用：** 调用 `toolTip()` 读取当前值；它不会修改应用状态。

### `visible : bool`

**作用与语义：**

该属性是否存在系统托盘条目是否可见。
将该属性设置为 true 或调用 `show()` 会显示系统托盘图标;将该属性设置为 false 或调用 `hide()` 则隐藏它。

**如何使用：** 调用 `visible()` 读取当前值；它不会修改应用状态。

### `QSystemTrayIcon::QSystemTrayIcon(QObject *parent = nullptr)`

**作用与语义：**

构造一个带有给定`parent`的QSystemTrayIcon对象。
图标最初是隐形的。

### `QSystemTrayIcon::QSystemTrayIcon(const QIcon &icon, QObject *parent = nullptr)`

**作用与语义：**

构造一个带有给定`icon`和`parent`的QSystemTrayIcon对象。
图标最初是隐形的。

### `[virtual noexcept] QSystemTrayIcon::~QSystemTrayIcon()`

**作用与语义：**

移除系统托盘上的图标，释放所有分配的资源。

### `[signal] void QSystemTrayIcon::activated(QSystemTrayIcon::ActivationReason reason)`

**作用与语义：**

当用户激活系统托盘图标时，会发出该信号。`reason` 说明激活原因。`QSystemTrayIcon::ActivationReason`枚举各种原因。

### `QMenu *QSystemTrayIcon::contextMenu() const`

**作用与语义：**

返回系统托盘当前的右键菜单。

### `[override virtual protected] bool QSystemTrayIcon::event(QEvent *e)`

**作用与语义：**

重实现自：`QObject::event`（QEvent *e）。

### `QRect QSystemTrayIcon::geometry() const`

**作用与语义：**

返回系统托盘图标的几何形状，显示屏幕坐标。

### `[slot] void QSystemTrayIcon::hide()`

**作用与语义：**

它隐藏了系统托盘的入口。

### `[static] bool QSystemTrayIcon::isSystemTrayAvailable()`

**作用与语义：**

如果系统托盘可用，返回`true`;否则返回`false`。
如果系统托盘目前不可用，但稍后可用，`QSystemTrayIcon`会自动添加系统托盘中的条目（如果`visible`）。

### `[signal] void QSystemTrayIcon::messageClicked()`

**作用与语义：**

当用户点击使用`showMessage()`显示的消息时，该信号会发出。
注意：我们遵循 Microsoft Windows 的行为，因此当用户点击显示气泡信息的托盘图标时，也会发出该信号。

### `void QSystemTrayIcon::setContextMenu(QMenu *menu)`

**作用与语义：**

将指定的`menu`设置为系统托盘图标的右键菜单。
当用户点击鼠标按钮请求系统托盘图标的上下文菜单时，菜单会弹出。
注意：系统托盘图标不占有菜单的所有权。你必须确保在适当时间删除该图标，例如创建带有合适父对象的菜单。

### `[slot] void QSystemTrayIcon::show()`

**作用与语义：**

系统托盘中显示图标。

### `[slot] void QSystemTrayIcon::showMessage(const QString &title, const QString &message, QSystemTrayIcon::MessageIcon icon = QSystemTrayIcon::Information, int millisecondsTimeoutHint = 10000)`

**作用与语义：**

显示条目气泡消息，包含给定的`title`、`message`和`icon`，时间在`millisecondsTimeoutHint`中指定。`title`和`message`必须是明文字符串。
用户可以点击消息;此时`messageClicked()`信号会发出。
请注意，消息的显示取决于系统配置和用户偏好，消息可能根本不会出现。因此，不应仅依赖它作为提供关键信息的唯一手段。
在Windows上，当应用程序聚焦时，系统通常会忽略`millisecondsTimeoutHint`。
已经变成了Qt 5.2的一个槽函数。
注意：该槽位已超载。连接该槽位：


使用 qOverload 连接：
connect（sender， &SenderClass：：signal，。
systemTrayIcon， qOverload（&QSystemTrayIcon：：showMessage））;

或者用lambda作为包装器：
connect（sender， &SenderClass：：signal，。
systemTrayIcon， [receiver = systemTrayIcon]（const QString &title， const QString &message， QSystemTrayIcon：：MessageIcon icon， int millisecondsTimeoutHint） { receiver->showMessage（title， message， icon， millisecondsTimeoutHint）; }）;


更多示例和方法，请参见连接超载槽位。

### `[slot] void QSystemTrayIcon::showMessage(const QString &title, const QString &message, const QIcon &icon, int millisecondsTimeoutHint = 10000)`

**作用与语义：**

显示条目气泡消息，`title`、`message`和自定义图标`icon`，时间为`millisecondsTimeoutHint`指定时间。
注意：该槽位已超载。连接该槽位：


使用 qOverload 连接：
connect（sender， &SenderClass：：signal，。
systemTrayIcon， qOverload（&QSystemTrayIcon：：showMessage））;

或者用lambda作为包装器：
connect（sender， &SenderClass：：signal，。
systemTrayIcon， [receiver = systemTrayIcon]（const QString &title， const QString &message， const QIcon &icon， int millisecondsTimeoutHint） { receiver->showMessage（title， message， icon， 毫秒TimeoutHint）; }）;


更多示例和方法，请参见连接超载槽位。

### `[static] bool QSystemTrayIcon::supportsMessages()`

**作用与语义：**

如果系统托盘支持气泡消息，返回`true`;否则返回`false`。

### `QIcon icon() const`

**作用与语义：**

该属性保留系统托盘图标。
在Windows上，系统托盘图标大小为16x16;在X11上，首选尺寸为22x22。图标将根据需要缩放至相应大小。

**如何使用：** 调用 `icon()` 读取当前值；它不会修改应用状态。

### `bool isVisible() const`

**作用与语义：**

该属性是否存在系统托盘条目是否可见。
将该属性设置为 true 或调用 `show()` 会显示系统托盘图标;将该属性设置为 false 或调用 `hide()` 则隐藏它。

**如何使用：** 调用 `isVisible()` 读取当前值；它不会修改应用状态。

### `void setIcon(const QIcon &icon)`

**作用与语义：**

该属性保留系统托盘图标。
在Windows上，系统托盘图标大小为16x16;在X11上，首选尺寸为22x22。图标将根据需要缩放至相应大小。

**如何使用：** 调用 `setIcon(...)` 修改 `icon`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setToolTip(const QString &tip)`

**作用与语义：**

该属性包含系统托盘输入的工具提示。
在某些系统上，提示长度是有限的。如有需要，提示会被截断。

**如何使用：** 调用 `setToolTip(...)` 修改 `toolTip`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QString toolTip() const`

**作用与语义：**

该属性包含系统托盘输入的工具提示。
在某些系统上，提示长度是有限的。如有需要，提示会被截断。

**如何使用：** 调用 `toolTip()` 读取当前值；它不会修改应用状态。

### `void setVisible(bool visible)`

**作用与语义：**

该属性是否存在系统托盘条目是否可见。
将该属性设置为 true 或调用 `show()` 会显示系统托盘图标;将该属性设置为 false 或调用 `hide()` 则隐藏它。

**如何使用：** 调用 `setVisible(...)` 修改 `visible`；传入的新值会成为后续查询和相关界面行为所使用的值。

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

`QSystemTrayIcon` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
