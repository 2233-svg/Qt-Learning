# QGuiApplication

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 非 Widgets GUI 应用程序对象，负责平台 GUI 初始化、全局输入状态和主事件循环。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QGuiApplication`：非 Widgets GUI 应用程序对象，负责平台 GUI 初始化、全局输入状态和主事件循环。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QGuiApplication>`
- 继承自：QCoreApplication
- 直接派生类：QApplication

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

### 状态、生命周期和线程

**生命周期：** 先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

**状态与结果：** 把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

**线程与事件循环：** 如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

## 3. 直接使用

围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。 使用时通常按这个过程组织：构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 属性

- `applicationDisplayName : QString`
- `desktopFileName : QString`
- `layoutDirection : Qt::LayoutDirection`
- `platformName : const QString`
- `primaryScreen : QScreen*`
- `quitOnLastWindowClosed : bool`
- `windowIcon : QIcon`

### 公有函数

- `QGuiApplication(int &argc, char **argv)`
- `virtual ~QGuiApplication()`
- `qreal devicePixelRatio() const`
- `bool isSavingSession() const`
- `bool isSessionRestored() const`
- `QNativeInterface * nativeInterface() const`
- `QString sessionId() const`
- `QString sessionKey() const`

### 重实现的公有函数

- `virtual bool notify(QObject *object, QEvent *event) override`

### 公有槽函数

- `(since 6.5) void setBadgeNumber(qint64 number)`

### 信号

- `void applicationDisplayNameChanged()`
- `void applicationStateChanged(Qt::ApplicationState state)`
- `void commitDataRequest(QSessionManager &manager)`
- `void focusObjectChanged(QObject *focusObject)`
- `void focusWindowChanged(QWindow *focusWindow)`
- `void fontDatabaseChanged()`
- `void lastWindowClosed()`
- `void layoutDirectionChanged(Qt::LayoutDirection direction)`
- `void primaryScreenChanged(QScreen *screen)`
- `void saveStateRequest(QSessionManager &manager)`
- `void screenAdded(QScreen *screen)`
- `void screenRemoved(QScreen *screen)`

### 静态公有成员

- `QWindowList allWindows()`
- `QString applicationDisplayName()`
- `Qt::ApplicationState applicationState()`
- `void changeOverrideCursor(const QCursor &cursor)`
- `QClipboard * clipboard()`
- `QString desktopFileName()`
- `bool desktopSettingsAware()`
- `int exec()`
- `QObject * focusObject()`
- `QWindow * focusWindow()`
- `QFont font()`
- `Qt::HighDpiScaleFactorRoundingPolicy highDpiScaleFactorRoundingPolicy()`
- `QInputMethod * inputMethod()`
- `bool isLeftToRight()`
- `bool isRightToLeft()`
- `Qt::KeyboardModifiers keyboardModifiers()`
- `Qt::LayoutDirection layoutDirection()`
- `QWindow * modalWindow()`
- `Qt::MouseButtons mouseButtons()`
- `QCursor * overrideCursor()`
- `QPalette palette()`
- `QString platformName()`
- `QScreen * primaryScreen()`
- `Qt::KeyboardModifiers queryKeyboardModifiers()`
- `bool quitOnLastWindowClosed()`
- `void restoreOverrideCursor()`
- `QScreen * screenAt(const QPoint &point)`
- `QList<QScreen *> screens()`
- `void setApplicationDisplayName(const QString &name)`
- `void setDesktopFileName(const QString &name)`
- `void setDesktopSettingsAware(bool on)`
- `void setFont(const QFont &font)`
- `void setHighDpiScaleFactorRoundingPolicy(Qt::HighDpiScaleFactorRoundingPolicy policy)`
- `void setLayoutDirection(Qt::LayoutDirection direction)`
- `void setOverrideCursor(const QCursor &cursor)`
- `void setPalette(const QPalette &pal)`
- `void setQuitOnLastWindowClosed(bool quit)`
- `void setWindowIcon(const QIcon &icon)`
- `QStyleHints * styleHints()`
- `void sync()`
- `QWindow * topLevelAt(const QPoint &pos)`
- `QWindowList topLevelWindows()`
- `QIcon windowIcon()`

### 重实现的保护函数

- `virtual bool event(QEvent *e) override`

### 公开宏

- `qGuiApp`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `applicationDisplayName : QString`

**作用与语义：**

该属性表示应用程序显示给用户看的名称，例如窗口标题、任务切换界面或桌面环境中的应用名称。它可以使用翻译后的文本；如果没有显式设置，Qt 会回退到 `QCoreApplication::applicationName()`。

**如何使用：** 在创建应用对象后、显示窗口前设置即可：

```cpp
QGuiApplication app(argc, argv);
QGuiApplication::setApplicationDisplayName(QObject::tr("图片管理器"));
qInfo() << QGuiApplication::applicationDisplayName();
```

名称需要随语言切换时重新设置；依赖这个名称的界面可监听 `applicationDisplayNameChanged()`。

### `desktopFileName : QString`

**作用与语义：**

该属性指定 Linux/freedesktop 桌面环境中代表本应用的 `.desktop` 文件基本名。只填写文件名，不含目录和 `.desktop` 后缀；例如桌面项为 `/usr/share/applications/org.example.Reader.desktop` 时应设置为 `org.example.Reader`。窗口系统用它把应用窗口与启动器、图标和桌面元数据准确关联，避免靠窗口标题猜测。

**如何使用：** 调用 `desktopFileName()` 读取当前值；它不会修改应用状态。

### `layoutDirection : Qt::LayoutDirection`

**作用与语义：**

该属性控制应用的默认界面排列方向。`Qt::LeftToRight` 适用于中文、英文等语言，`Qt::RightToLeft` 适用于阿拉伯语、希伯来语等语言；设为 `Qt::LayoutDirectionAuto` 时，Qt 根据当前应用语言选择方向。改变它会影响随后采用应用默认方向的窗口和布局。

**如何使用：** 调用 `layoutDirection()` 读取当前值；它不会修改应用状态。

### `[read-only] platformName : const QString`

**作用与语义：**

该只读属性返回当前实际加载的 QPA 平台插件名称，例如 Windows 上通常是 `windows`，X11 环境是 `xcb`，Wayland 环境是 `wayland`，无界面测试可能是 `offscreen`。它适合用于诊断或只在特定后端可用的兼容处理，不应把某个平台名称当成应用正常运行的必要条件。

**如何使用：** 调用 `platformName()` 读取当前值；它不会修改应用状态。

### `[read-only] primaryScreen : QScreen*`

**作用与语义：**

该只读属性返回应用当前的主屏幕。未明确指定屏幕的新 `QWindow` 通常先显示在这里。多显示器配置会在运行中变化，应监听 `primaryScreenChanged(QScreen *)`，不要长期缓存返回指针而不处理屏幕移除。

**如何使用：** 调用 `primaryScreen()` 读取当前值；它不会修改应用状态。

### `quitOnLastWindowClosed : bool`

**作用与语义：**

该属性决定最后一个可见主窗口关闭后，Qt 是否自动尝试退出应用；默认值为 `true`。托盘程序或没有常驻窗口的后台 GUI 应用通常把它设为 `false`。即使为 `true`，活动的 `QEventLoopLocker` 或被忽略的 `QEvent::Quit` 仍可能阻止进程真正退出。

**如何使用：** 调用 `quitOnLastWindowClosed()` 读取当前值；它不会修改应用状态。

### `windowIcon : QIcon`

**作用与语义：**

该属性设置应用窗口的默认图标。没有通过 `QWindow::setIcon()` 单独指定图标的窗口会采用它；任务栏、窗口标题栏等位置是否显示以及采用哪个尺寸由平台决定。

**如何使用：** 调用 `windowIcon()` 读取当前值；它不会修改应用状态。

### `QGuiApplication::QGuiApplication(int &argc, char **argv)`

**作用与语义：**

初始化窗口系统，并在`argv`中构建带有`argc`命令行参数的应用对象。
警告：`argc` 和 `argv` 所引用的数据必须在 QGuiApplication 对象的整个生命周期内保持有效。此外，`argc` 必须大于 0，且 `argv` 至少包含一个有效字符串。
全局`qApp`指针指向该应用对象。只需创建一个应用对象。
该应用对象必须在任何绘图设备（包括像素图、位图等）之前构建完成。
注意：`argc`和`argv`可能会随着Qt移除其识别的命令行参数而发生变化。
所有 Qt 程序都会自动支持一组命令行选项，允许修改 Qt 与窗口系统交互的方式。部分选项也可以通过环境变量访问，如果应用程序能启动 GUI 子进程或其他应用程序，环境变量是首选形式（环境变量将继承给子进程）。不确定时，使用环境变量。
目前支持的选项如下：
- `-platform` `platformName`[：options]，指定 Qt 平台抽象（QPA）插件。覆盖`QT_QPA_PLATFORM`环境变量。
- `-platformpluginpath`路径，指定通往平台插件的路径。覆盖`QT_QPA_PLATFORM_PLUGIN_PATH`环境变量。
- `-platformtheme` platformTheme，指定平台主题。覆盖`QT_QPA_PLATFORMTHEME`环境变量。
- `-plugin`插件，指定需要加载的额外插件。该参数可以多次出现。与插件串接在`QT_QPA_GENERIC_PLUGINS`环境变量中。
- `-qmljsdebugger=`，激活指定端口的QML/JS调试器。该值格式必须为`port:1234`[，block]，其中block为可选，会让应用程序等待调试器连接到它。
- `-qwindowgeometry` 几何，使用 X11 语法指定主窗口的几何形状。例如：`-qwindowgeometry 100x100+50+50`
- `-qwindowicon`，设置默认窗口图标
- `-qwindowtitle`，设定第一个窗口的标题
- `-reverse`，将应用程序的布局方向设置为`Qt::RightToLeft`。该选项旨在辅助调试，不应在生产环境中使用。默认值是从用户所在地自动检测到的（参见`QLocale::textDirection()`）。
- `-session`会话，恢复之前会话中的应用程序。
X11 提供以下标准命令行选项：
- `-display`主机名：screen_number，切换X11上的显示。覆盖`DISPLAY`环境变量。
- `-geometry`几何，与`-qwindowgeometry`相同。
你可以为`-platform`选项指定平台特定的参数。将它们放在平台插件名称后面，冒号后面，作为逗号分隔的列表。例如，`-platform windows:dialogs=xp,fontengine=freetype`。
`-platform windows`可用的参数如下：
- `altgr`，检测某些键盘上的按键`AltGr`为`Qt::GroupSwitchModifier`（自Qt 5.12起）。
- `darkmode=[0|1|2]` 控制 Qt 如何响应 Windows 10 1903（自 Qt 5.15 起）引入的应用程序激活暗黑模式。值为 0 则禁用暗黑模式支持。
当值为1时，当应用的暗黑模式被激活且未使用高对比度主题时，Qt会将窗口边框切换为黑色。这适用于实现自身主题的应用程序。
值为2时，Windows Vista样式会被停用，并在暗模式下切换到使用简化调色板的Windows样式。目前该方法还处于试验阶段，等待新样式的引入，能够正确适应暗黑模式。
从 Qt 6.5 起，默认值为 2;要禁用暗黑模式支持，请将该值设为 0 或 1。
- `dialogs=[xp|none]`，`xp`使用类似XP的原生对话，`none`禁用它们。
- `fontengine=freetype`，使用FreeType字体引擎。
- `fontengine=gdi`，使用基于GDI的旧字体数据库，默认使用GDI字体引擎（该引擎仅用于某些字体类型或字体属性）。（自Qt 6.8起）
- `menus=[native|none]`，控制原生菜单的使用。原生菜单采用 Win32 API 实现，比基于`QMenu`的菜单更简单，例如允许在菜单上放置小部件或更改属性（如字体），且不提供悬停信号。它们主要面向 Qt Quick。默认情况下，如果应用程序不是 `QApplication` 实例或 Qt Quick Controls 2 应用程序（自 Qt 5.10 起）会使用。
- `nocolorfonts` 关闭 DirectWrite Color 字体（自第 5.8 卷起）。
- `nodirectwrite` 关闭 DirectWrite 字体（自 Qt 5.8 起）。这也隐式地选择了 GDI 字体引擎。
- `nomousefromtouch` 忽略操作系统从触摸事件合成的鼠标事件。
- `nowmpointer` 从指针输入消息处理切换到传统鼠标处理（自Qt 5.12起）。
- `reverse` 激活从右到左模式（实验性）。自第5.13个Qt起，Windows标题栏将相应显示在从右到左的位置中。
- `tabletabsoluterange=<value>` 为WinTab平板的鼠标模式检测设定值（自第5.3量子起称为Legacy）。
以下参数可用于`-platform cocoa`（macOS版本）：
- `fontengine=freetype`，使用FreeType字体引擎。
关于嵌入式Linux平台可用的平台特定论元的更多信息，请参见Qt for Embedded Linux。

### `[virtual noexcept] QGuiApplication::~QGuiApplication()`

**作用与语义：**

销毁应用程序对象并结束由它管理的 GUI 平台资源。通常在 `main()` 返回时自动发生；应用中只能存在一个应用程序对象。

### `[static] QWindowList QGuiApplication::allWindows()`

**作用与语义：**

返回应用程序中所有窗口的列表。
如果没有窗口，列表为空。

### `[static] Qt::ApplicationState QGuiApplication::applicationState()`

**作用与语义：**

返回应用当前状态。
你可以对应用状态变化做出反应，执行诸如停止/恢复CPU密集型任务、释放/加载资源或保存/恢复应用数据等操作。

### `[signal] void QGuiApplication::applicationStateChanged(Qt::ApplicationState state)`

**作用与语义：**

当应用`state`发生变化时，该信号会发出。

### `[static] void QGuiApplication::changeOverrideCursor(const QCursor &cursor)`

**作用与语义：**

将当前激活的应用覆盖光标改为`cursor`。
如果没有调用`setOverrideCursor()`，这个函数没有任何作用。

### `[static] QClipboard *QGuiApplication::clipboard()`

**作用与语义：**

返回该对象以便与剪贴板交互。

### `[signal] void QGuiApplication::commitDataRequest(QSessionManager &manager)`

**作用与语义：**

该信号涉及会话管理。当`QSessionManager`希望应用程序提交所有数据时，该信号会发出。
通常这意味着在获得用户许可后保存所有已打开的文件。此外，你可能还想提供一种方式，让用户能够取消关闭。
你不应该在这个信号内退出应用程序。相反，会话管理器可能会根据上下文在之后退出，也可能不会。
警告：在此信号内，除非你向`manager`明确请求许可，否则无法进行任何用户交互。详情和示例使用情况请参见`QSessionManager::allowsInteraction()`和`QSessionManager::allowsErrorInteraction()`。
注意：连接该信号时应使用`Qt::DirectConnection`。

### `[static] bool QGuiApplication::desktopSettingsAware()`

**作用与语义：**

如果Qt设置为使用系统的标准颜色、字体等，返回`true`;否则返回`false`。默认为`true`。

### `qreal QGuiApplication::devicePixelRatio() const`

**作用与语义：**

返回系统中最高的屏幕设备像素比。这是物理像素与设备无关像素的比值。
只有在不知道目标窗口时才使用这个函数。如果你知道目标窗口，就用`QWindow::devicePixelRatio()`。

### `[override virtual protected] bool QGuiApplication::event(QEvent *e)`

**作用与语义：**

重实现 `QCoreApplication::event()`，处理发送给应用程序对象自身的事件。只有在子类需要截获应用级事件时才重写；未处理的事件必须交给基类。

### `[static] int QGuiApplication::exec()`

**作用与语义：**

进入主事件循环，等待调用`exit()`，然后返回设置为`exit()`的值（如果通过`quit()`调用`exit()`则为0）。
启动事件处理需要调用该函数。主事件循环接收来自窗口系统的事件，并将其分发给应用控件。
通常，在调用exec()之前，不能进行任何用户交互。
为了让你的应用程序执行空闲处理，例如在没有待处理事件时执行特殊函数，可以使用超时为0ns的`QChronoTimer`。更高级的空闲处理方案可以通过`processEvents()`实现。
我们建议你将清理代码连接到`aboutToQuit()`信号，而不是放在应用的`main()`函数中。这是因为在某些平台上，`QApplication::exec()`调用可能不会返回。

### `[static] QObject *QGuiApplication::focusObject()`

**作用与语义：**

返回当前活跃窗口内的`QObject`，作为与焦点相关事件（如按键事件）的最终接收者。

### `[signal] void QGuiApplication::focusObjectChanged(QObject *focusObject)`

**作用与语义：**

当与焦点相关的事件最终接收器更换时，该信号会发出。`focusObject`是新的接收器。

### `[static] QWindow *QGuiApplication::focusWindow()`

**作用与语义：**

返回接收与焦点相关的事件的`QWindow`，如按键事件。

### `[signal] void QGuiApplication::focusWindowChanged(QWindow *focusWindow)`

**作用与语义：**

当聚焦窗口变化时，该信号会发出。`focusWindow` 是新的聚焦窗口。

### `[static] QFont QGuiApplication::font()`

**作用与语义：**

返回默认的应用字体。

### `[signal] void QGuiApplication::fontDatabaseChanged()`

**作用与语义：**

当可用字体发生变化时，会发出该信号。
这可能发生在添加或移除应用程序字体，或系统字体发生变化时。

### `[static] Qt::HighDpiScaleFactorRoundingPolicy QGuiApplication::highDpiScaleFactorRoundingPolicy()`

**作用与语义：**

返回高DPI比例因子四舍五入策略。

### `[static] QInputMethod *QGuiApplication::inputMethod()`

**作用与语义：**

返回输入法。
输入法返回关于虚拟键盘状态和位置的属性。它还提供当前焦点输入元素的位置信息。

### `[static] bool QGuiApplication::isLeftToRight()`

**作用与语义：**

如果应用程序的布局方向`Qt::LeftToRight`，返回`true`;否则返回`false`。

### `[static] bool QGuiApplication::isRightToLeft()`

**作用与语义：**

如果应用程序的布局方向`Qt::RightToLeft`，返回`true`;否则返回`false`。

### `bool QGuiApplication::isSavingSession() const`

**作用与语义：**

如果应用程序当前正在保存会话，返回`true`;否则返回`false`。
当`commitDataRequest()`和`saveStateRequest()`发出时，以及会话管理关闭窗口时，这`true`。

### `bool QGuiApplication::isSessionRestored() const`

**作用与语义：**

如果应用程序从早期会话恢复，返回`true`;否则返回`false`。

### `[static] Qt::KeyboardModifiers QGuiApplication::keyboardModifiers()`

**作用与语义：**

返回键盘修饰键的当前状态。当前状态同步更新，因为事件队列中会清除会自发改变键盘状态的事件（`QEvent::KeyPress`和`QEvent::KeyRelease`事件）。
需要注意的是，这可能并不反映调用时输入设备上实际持有的密钥，而是上述事件中最后报告的修饰符。如果没有持有密钥，`Qt::NoModifier`会返回。

### `[signal] void QGuiApplication::lastWindowClosed()`

**作用与语义：**

当最后一个可见的主窗口（即无瞬态父窗口的顶层窗口）关闭时，该信号从`exec()`发出。
默认情况下，`QGuiApplication`在该信号发出后退出。该功能可通过将`quitOnLastWindowClosed`设置为`false`关闭。

### `[static] QWindow *QGuiApplication::modalWindow()`

**作用与语义：**

返回最近显示的模态窗口。如果没有可见模态窗口，该函数返回零。
模态窗口是指其`modality`属性设置为`Qt::WindowModal`或`Qt::ApplicationModal`的窗口。必须关闭模态窗口，用户才能继续程序的其他部分。
模态窗口组织成栈。该函数返回栈顶端的模态窗口。

### `[static] Qt::MouseButtons QGuiApplication::mouseButtons()`

**作用与语义：**

返回鼠标按钮的当前状态。当前状态同步更新，因为事件队列中会清除会自发改变鼠标状态的事件（`QEvent::MouseButtonPress`和`QEvent::MouseButtonRelease`事件）。
需要注意的是，这可能并不反映调用时输入设备上实际按住的按键，而是上述事件中最后报告的鼠标按键。如果没有按住鼠标按键，`Qt::NoButton`会返回。

### `template <typename QNativeInterface> QNativeInterface *QGuiApplication::nativeInterface() const`

**作用与语义：**

返回该应用的本地接口类型。
该功能提供访问`QGuiApplication`特定平台的功能，定义在`QNativeInterface`命名空间中：
- `QNativeInterface::QWaylandApplication`：Wayland应用的原生接口
- `QNativeInterface::QX11Application`：X11应用的原生接口
如果请求的接口不可用，则返回`nullptr`。

### `[override virtual] bool QGuiApplication::notify(QObject *object, QEvent *event)`

**作用与语义：**

重实现 `QCoreApplication::notify()`，把一个事件分派给目标 `object`。返回值表示事件是否被处理。它是全局事件分派入口，重写时必须谨慎，并通常调用基类实现以维持 Qt 的正常事件传递。

### `[static] QCursor *QGuiApplication::overrideCursor()`

**作用与语义：**

返回激活应用覆盖光标。
如果没有定义应用光标（即内部光标栈为空），该函数返回`nullptr`。

### `[static] QPalette QGuiApplication::palette()`

**作用与语义：**

返回当前的应用调色板。
未明确设定的角色将反映系统的平台主题。

### `[static] Qt::KeyboardModifiers QGuiApplication::queryKeyboardModifiers()`

**作用与语义：**

查询和返回键盘修饰键的状态。与`keyboardModifiers`不同，该方法返回调用时输入设备上实际持有的键。
它不依赖于该进程是否接收到按键事件，这使得在移动窗口时可以检查修改器。注意，在大多数情况下，你应该使用`keyboardModifiers()`，因为它包含了当前处理事件接收时修改器的状态，因此更快更准确。

### `[static] void QGuiApplication::restoreOverrideCursor()`

**作用与语义：**

撤销上次的 `setOverrideCursor()`。
如果`setOverrideCursor()`被调用了两次，调用 restoreOverrideCursor() 将激活第一个光标集。第二次调用该函数会恢复原始控件的光标。

### `[signal] void QGuiApplication::saveStateRequest(QSessionManager &manager)`

**作用与语义：**

该信号涉及会话管理。当会话管理器希望应用程序为未来会话保留其状态时，该信号会被调用。
例如，文本编辑器会创建一个临时文件，包含当前编辑缓冲区的内容、光标位置以及当前编辑会话的其他方面。
你绝不应在这个信号内退出应用程序。相反，会话管理器可能会根据上下文在之后这样做，也可能不会。此外，大多数会话管理器很可能会在应用程序启动后立即请求保存状态。这使会话管理器能够了解应用程序的重启策略。
警告：在此信号内，除非你向`manager`明确请求许可，否则无法进行用户交互。详情请参见`QSessionManager::allowsInteraction()`和`QSessionManager::allowsErrorInteraction()`。
注意：连接该信号时应使用`Qt::DirectConnection`。

### `[signal] void QGuiApplication::screenAdded(QScreen *screen)`

**作用与语义：**

每当系统新增屏幕`screen`时，该信号都会发出。

### `[static] QScreen *QGuiApplication::screenAt(const QPoint &point)`

**作用与语义：**

返回包含全局坐标 `point` 的屏幕；点不在任何屏幕上时返回 `nullptr`。在存在多个彼此独立的虚拟桌面组时，若坐标同时匹配多个组，只返回第一个匹配项。

### `[signal] void QGuiApplication::screenRemoved(QScreen *screen)`

**作用与语义：**

每当系统中移除`screen`时，该信号都会发出。它提供了一个在Qt退回将窗口移至主屏幕之前，管理屏幕上窗口的机会。

### `[static] QList<QScreen *> QGuiApplication::screens()`

**作用与语义：**

返回与该应用程序连接的窗口系统相关的所有屏幕列表。

### `QString QGuiApplication::sessionId() const`

**作用与语义：**

返回当前会话的标识符。
如果应用程序是从早期会话恢复的，该标识符与前一会话相同。会话标识符保证对不同应用程序和同一应用的不同实例都是唯一的。

### `QString QGuiApplication::sessionKey() const`

**作用与语义：**

返回当前会话中的会话密钥。
如果应用程序是从早期会话恢复的，该密钥与上一个会话结束时相同。
每次保存会话时，会话密钥都会更换。如果关闭进程被取消，关闭时会使用另一个会话密钥。

### `[slot, since 6.5] void QGuiApplication::setBadgeNumber(qint64 number)`

**作用与语义：**

将应用的徽章设置为`number`。
对于向用户反馈未读消息数量等方面非常有用。
徽章会叠加在macOS的Dock应用图标上，iOS的主屏幕图标，Windows和Linux的任务栏上。
如果号码超出平台支持范围，号码将被夹在支持范围内。如果号码不适合徽章，号码可能会被视觉上省略。
将数字设为0会清除徽章。

### `[static] void QGuiApplication::setDesktopSettingsAware(bool on)`

**作用与语义：**

设置Qt是否应使用系统的标准颜色、字体等为`on`。默认情况下，这是`true`。
在创建`QGuiApplication`对象之前必须调用该函数，如下：

**官方示例：**

```cpp
 int main(int argc, char *argv[])
 {
     QApplication::setDesktopSettingsAware(false);
     QApplication app(argc, argv);
     // ...
     return app.exec();
 }
```

### `[static] void QGuiApplication::setFont(const QFont &font)`

**作用与语义：**

将默认应用字体改为`font`。

### `[static] void QGuiApplication::setHighDpiScaleFactorRoundingPolicy(Qt::HighDpiScaleFactorRoundingPolicy policy)`

**作用与语义：**

为应用程序设定高DPI比例因子的四舍五入策略。`policy`决定非整数比例因子（如Windows 150%）的处理方式。
主要有两个选项：分数比例因子是否应将整数四舍五入。保持比例尺因子不变，用户界面大小将完全匹配操作系统设置，但可能导致绘制错误，例如Windows样式。
如果需要四舍五入，那么接下来应决定哪种四舍五入类型。支持数学上正确的四舍五入，但可能不会带来最佳的视觉效果：考虑你想将1.5倍渲染为1倍（“小界面”）还是2倍（“大界面”）。详见`Qt::HighDpiScaleFactorRoundingPolicy`枚举中所有选项的完整列表。
该函数必须在创建应用对象之前调用。`QGuiApplication::highDpiScaleFactorRoundingPolicy()`访问器如果设置为环境，将反映环境。
默认值是`Qt::HighDpiScaleFactorRoundingPolicy::PassThrough`。

### `[static] void QGuiApplication::setOverrideCursor(const QCursor &cursor)`

**作用与语义：**

将应用覆盖光标设置为`cursor`。
应用覆盖光标旨在向用户显示应用处于特殊状态，例如在可能需要较长时间的操作中。
该光标会显示在所有应用的控件中，直到调用`restoreOverrideCursor()`或其他 setOverrideCursor() 。
应用光标存储在内部栈中。setOverrideCursor() 将光标推入栈，`restoreOverrideCursor()`将激活光标从栈中弹出。`changeOverrideCursor()` 更改当前激活的应用覆盖光标。
每个 setOverrideCursor() 必须最终跟着对应的 `restoreOverrideCursor()`，否则堆栈永远不会被清空。

**官方示例：**

```cpp
 QGuiApplication::setOverrideCursor(QCursor(Qt::WaitCursor));
 calculateHugeMandelbrot();              // lunch time...
 QGuiApplication::restoreOverrideCursor();
```

### `[static] void QGuiApplication::setPalette(const QPalette &pal)`

**作用与语义：**

将应用调色板改为`pal`。
该调色板中的颜色角色与系统的平台主题结合，形成应用程序的最终调色板。

### `[static] QStyleHints *QGuiApplication::styleHints()`

**作用与语义：**

返回应用的风格提示。
样式提示包含了一系列平台相关的属性，如双击间隔、全宽选择等。
这些提示可以用来更紧密地与底层平台整合。

### `[static] void QGuiApplication::sync()`

**作用与语义：**

先处理 Qt 中待分派的事件，再让平台插件与底层窗口系统同步，最后再次处理同步过程中产生的事件。这个操作开销较大且官方不建议在常规业务代码中使用；不要把它当作强制重绘或刷新界面的通用办法。

### `[static] QWindow *QGuiApplication::topLevelAt(const QPoint &pos)`

**作用与语义：**

返回给定位置`pos`的顶层窗口（如果有的话）。

### `[static] QWindowList QGuiApplication::topLevelWindows()`

**作用与语义：**

返回应用程序顶层窗口的列表。

### `qGuiApp`

**作用与语义：**

指代唯一应用对象的全局指针。仅在该对象是`QGuiApplication`时才有效。

### `void applicationDisplayNameChanged()`

**作用与语义：**

该属性表示应用程序显示给用户看的名称，例如窗口标题、任务切换界面或桌面环境中的应用名称。它可以使用翻译后的文本；如果没有显式设置，Qt 会回退到 `QCoreApplication::applicationName()`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `applicationDisplayName` 的变化，不要把它当作普通函数主动调用。

### `void layoutDirectionChanged(Qt::LayoutDirection direction)`

**作用与语义：**

该属性控制应用的默认界面排列方向。`Qt::LeftToRight` 适用于中文、英文等语言，`Qt::RightToLeft` 适用于阿拉伯语、希伯来语等语言；设为 `Qt::LayoutDirectionAuto` 时，Qt 根据当前应用语言选择方向。改变它会影响随后采用应用默认方向的窗口和布局。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `layoutDirection` 的变化，不要把它当作普通函数主动调用。

### `void primaryScreenChanged(QScreen *screen)`

**作用与语义：**

该只读属性返回应用当前的主屏幕。未明确指定屏幕的新 `QWindow` 通常先显示在这里。多显示器配置会在运行中变化，应监听 `primaryScreenChanged(QScreen *)`，不要长期缓存返回指针而不处理屏幕移除。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `primaryScreen` 的变化，不要把它当作普通函数主动调用。

### `QString applicationDisplayName()`

**作用与语义：**

该属性表示应用程序显示给用户看的名称，例如窗口标题、任务切换界面或桌面环境中的应用名称。它可以使用翻译后的文本；如果没有显式设置，Qt 会回退到 `QCoreApplication::applicationName()`。

**如何使用：** 调用 `applicationDisplayName()` 读取当前值；它不会修改应用状态。

### `QString desktopFileName()`

**作用与语义：**

该属性指定 Linux/freedesktop 桌面环境中代表本应用的 `.desktop` 文件基本名。只填写文件名，不含目录和 `.desktop` 后缀；例如桌面项为 `/usr/share/applications/org.example.Reader.desktop` 时应设置为 `org.example.Reader`。窗口系统用它把应用窗口与启动器、图标和桌面元数据准确关联，避免靠窗口标题猜测。

**如何使用：** 调用 `desktopFileName()` 读取当前值；它不会修改应用状态。

### `Qt::LayoutDirection layoutDirection()`

**作用与语义：**

该属性控制应用的默认界面排列方向。`Qt::LeftToRight` 适用于中文、英文等语言，`Qt::RightToLeft` 适用于阿拉伯语、希伯来语等语言；设为 `Qt::LayoutDirectionAuto` 时，Qt 根据当前应用语言选择方向。改变它会影响随后采用应用默认方向的窗口和布局。

**如何使用：** 调用 `layoutDirection()` 读取当前值；它不会修改应用状态。

### `QString platformName()`

**作用与语义：**

该只读属性返回当前实际加载的 QPA 平台插件名称，例如 Windows 上通常是 `windows`，X11 环境是 `xcb`，Wayland 环境是 `wayland`，无界面测试可能是 `offscreen`。它适合用于诊断或只在特定后端可用的兼容处理，不应把某个平台名称当成应用正常运行的必要条件。

**如何使用：** 调用 `platformName()` 读取当前值；它不会修改应用状态。

### `QScreen * primaryScreen()`

**作用与语义：**

该只读属性返回应用当前的主屏幕。未明确指定屏幕的新 `QWindow` 通常先显示在这里。多显示器配置会在运行中变化，应监听 `primaryScreenChanged(QScreen *)`，不要长期缓存返回指针而不处理屏幕移除。

**如何使用：** 调用 `primaryScreen()` 读取当前值；它不会修改应用状态。

### `bool quitOnLastWindowClosed()`

**作用与语义：**

该属性决定最后一个可见主窗口关闭后，Qt 是否自动尝试退出应用；默认值为 `true`。托盘程序或没有常驻窗口的后台 GUI 应用通常把它设为 `false`。即使为 `true`，活动的 `QEventLoopLocker` 或被忽略的 `QEvent::Quit` 仍可能阻止进程真正退出。

**如何使用：** 调用 `quitOnLastWindowClosed()` 读取当前值；它不会修改应用状态。

### `void setApplicationDisplayName(const QString &name)`

**作用与语义：**

该属性表示应用程序显示给用户看的名称，例如窗口标题、任务切换界面或桌面环境中的应用名称。它可以使用翻译后的文本；如果没有显式设置，Qt 会回退到 `QCoreApplication::applicationName()`。

**如何使用：** 传入希望用户看到的名称，通常在显示第一个窗口前调用；设置后会发出 `applicationDisplayNameChanged()`。

### `void setDesktopFileName(const QString &name)`

**作用与语义：**

该属性指定 Linux/freedesktop 桌面环境中代表本应用的 `.desktop` 文件基本名。只填写文件名，不含目录和 `.desktop` 后缀；例如桌面项为 `/usr/share/applications/org.example.Reader.desktop` 时应设置为 `org.example.Reader`。窗口系统用它把应用窗口与启动器、图标和桌面元数据准确关联，避免靠窗口标题猜测。

**如何使用：** 传入 `.desktop` 文件的基本名，不要包含路径或 `.desktop` 后缀；应在创建窗口前设置。

### `void setLayoutDirection(Qt::LayoutDirection direction)`

**作用与语义：**

该属性控制应用的默认界面排列方向。`Qt::LeftToRight` 适用于中文、英文等语言，`Qt::RightToLeft` 适用于阿拉伯语、希伯来语等语言；设为 `Qt::LayoutDirectionAuto` 时，Qt 根据当前应用语言选择方向。改变它会影响随后采用应用默认方向的窗口和布局。

**如何使用：** 调用 `setLayoutDirection(...)` 修改 `layoutDirection`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setQuitOnLastWindowClosed(bool quit)`

**作用与语义：**

该属性决定最后一个可见主窗口关闭后，Qt 是否自动尝试退出应用；默认值为 `true`。托盘程序或没有常驻窗口的后台 GUI 应用通常把它设为 `false`。即使为 `true`，活动的 `QEventLoopLocker` 或被忽略的 `QEvent::Quit` 仍可能阻止进程真正退出。

**如何使用：** 托盘程序调用 `setQuitOnLastWindowClosed(false)` 后，最后一个窗口关闭时事件循环仍会继续，退出动作要由菜单或业务逻辑显式触发。

### `void setWindowIcon(const QIcon &icon)`

**作用与语义：**

该属性设置应用窗口的默认图标。没有通过 `QWindow::setIcon()` 单独指定图标的窗口会采用它；任务栏、窗口标题栏等位置是否显示以及采用哪个尺寸由平台决定。

**如何使用：** 传入包含合适尺寸资源的 `QIcon`，并在创建窗口前调用；需要例外图标的窗口再使用 `QWindow::setIcon()` 覆盖。

### `QIcon windowIcon()`

**作用与语义：**

该属性设置应用窗口的默认图标。没有通过 `QWindow::setIcon()` 单独指定图标的窗口会采用它；任务栏、窗口标题栏等位置是否显示以及采用哪个尺寸由平台决定。

**如何使用：** 调用 `windowIcon()` 读取当前值；它不会修改应用状态。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

### 状态和错误边界

把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

### 线程边界

如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

### 最容易出现的错误

不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QGuiApplication` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
