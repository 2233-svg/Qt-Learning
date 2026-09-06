# QApplication

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QApplication` 是 Qt Widgets 应用程序的全局入口，管理桌面平台资源、控件风格、输入事件和主事件循环。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QApplication` 是 Qt Widgets 应用程序的全局入口，管理桌面平台资源、控件风格、输入事件和主事件循环。

**内部模型：** 它不是某个窗口的父类，而是整个 Widgets 进程的应用对象。所有 QWidget 都应在 QApplication 创建后使用，并且通常在主线程中创建。

**适用场景：** 任何使用 QWidget、QMainWindow、QDialog 或标准桌面控件的程序都应先创建 QApplication。

**典型调用链：** 构造 QApplication -> 创建主窗口/控件 -> show() -> app.exec() -> 退出时由栈对象清理。

**先记住的坑：** 不要在 QApplication 前创建 QWidget；不要在 GUI 线程执行耗时循环；高 DPI、平台风格和命令行参数应在构造或显示窗口前配置。

## 2. 依赖与对象关系

- 头文件：`#include <QApplication>`
- 继承自：QGuiApplication
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

它不是某个窗口的父类，而是整个 Widgets 进程的应用对象。所有 QWidget 都应在 QApplication 创建后使用，并且通常在主线程中创建。

### 状态、生命周期和线程

**生命周期：** 控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

**状态与结果：** 控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

**线程与事件循环：** 所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

## 3. 直接使用

任何使用 QWidget、QMainWindow、QDialog 或标准桌面控件的程序都应先创建 QApplication。 使用时通常按这个过程组织：构造 QApplication -> 创建主窗口/控件 -> show() -> app.exec() -> 退出时由栈对象清理。

```cpp
#include <QApplication>
#include <QMainWindow>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    QMainWindow window;
    window.resize(800, 600);
    window.show();
    return app.exec();
}
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 属性

- `autoSipEnabled : bool`
- `cursorFlashTime : int`
- `doubleClickInterval : int`
- `keyboardInputInterval : int`
- `startDragDistance : int`
- `startDragTime : int`
- `styleSheet : QString`
- `wheelScrollLines : int`

### 公有函数

- `QApplication(int &argc, char **argv)`
- `virtual ~QApplication()`
- `bool autoSipEnabled() const`
- `QString styleSheet() const`

### 重实现的公有函数

- `virtual bool notify(QObject *receiver, QEvent *e) override`

### 公有槽函数

- `void aboutQt()`
- `void closeAllWindows()`
- `void setAutoSipEnabled(const bool enabled)`
- `void setStyleSheet(const QString &sheet)`

### 信号

- `void focusChanged(QWidget *old, QWidget *now)`

### 静态公有成员

- `QWidget * activeModalWidget()`
- `QWidget * activePopupWidget()`
- `QWidget * activeWindow()`
- `void alert(QWidget *widget, int msec = 0)`
- `QWidgetList allWidgets()`
- `void beep()`
- `int cursorFlashTime()`
- `int doubleClickInterval()`
- `int exec()`
- `QWidget * focusWidget()`
- `QFont font()`
- `QFont font(const QWidget *widget)`
- `QFont font(const char *className)`
- `bool isEffectEnabled(Qt::UIEffect effect)`
- `int keyboardInputInterval()`
- `Qt::NavigationMode navigationMode()`
- `QPalette palette(const QWidget *widget)`
- `QPalette palette(const char *className)`
- `void setCursorFlashTime(int)`
- `void setDoubleClickInterval(int)`
- `void setEffectEnabled(Qt::UIEffect effect, bool enable = true)`
- `void setFont(const QFont &font, const char *className = nullptr)`
- `void setKeyboardInputInterval(int)`
- `void setNavigationMode(Qt::NavigationMode mode)`
- `void setPalette(const QPalette &palette, const char *className = nullptr)`
- `void setStartDragDistance(int l)`
- `void setStartDragTime(int ms)`
- `void setStyle(QStyle *style)`
- `QStyle * setStyle(const QString &style)`
- `void setWheelScrollLines(int)`
- `int startDragDistance()`
- `int startDragTime()`
- `QStyle * style()`
- `QWidget * topLevelAt(const QPoint &point)`
- `QWidget * topLevelAt(int x, int y)`
- `QWidgetList topLevelWidgets()`
- `int wheelScrollLines()`
- `QWidget * widgetAt(const QPoint &point)`
- `QWidget * widgetAt(int x, int y)`

### 重实现的保护函数

- `virtual bool event(QEvent *e) override`

### 公开宏

- `qApp`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `autoSipEnabled : bool`

**作用与语义：**

切换自动SIP（软件输入面板）可视化。
将该属性设置为`true`，以便在输入接受键盘输入的小部件时自动显示SIP。该属性仅影响设置WA_InputMethodEnabled属性的小部件，通常用于在键数极少或没有键的设备上启动虚拟键盘。
该特性仅对使用软件输入面板的平台产生影响。
默认是平台相关。

**如何使用：** 调用 `autoSipEnabled()` 读取当前值；它不会修改应用状态。

### `cursorFlashTime : int`

**作用与语义：**

该特性将文本光标的闪烁时间以毫秒计定。
闪光时间是显示、反转和恢复插入图显示所需的时间。通常文本光标显示时间为光标闪光时间的一半，然后隐藏同样时间，但时间可能有所不同。
X11 的默认值是 1000 毫秒。在 Windows 上，使用控制面板值，设置该属性会设置所有应用程序的光标闪烁时间。
我们建议小部件不要缓存该值，因为如果用户更改全局桌面设置，该值随时可能发生变化。
注意：该属性可能为负值，例如禁用光标闪烁。

**如何使用：** 调用 `cursorFlashTime()` 读取当前值；它不会修改应用状态。

### `doubleClickInterval : int`

**作用与语义：**

该特性具有以毫秒为单位的时间限制，将双击点击与连续两次鼠标点击区分开来。
X11 的默认值是 400 毫秒。在 Windows 和 Mac OS 上，使用操作系统的值。

**如何使用：** 调用 `doubleClickInterval()` 读取当前值；它不会修改应用状态。

### `keyboardInputInterval : int`

**作用与语义：**

该特性具有以毫秒为单位的时间限制，用以区分按键与连续两次按键。
X11 的默认值是 400 毫秒。在 Windows 和 Mac OS 上，使用操作系统的值。

**如何使用：** 调用 `keyboardInputInterval()` 读取当前值；它不会修改应用状态。

### `startDragDistance : int`

**作用与语义：**

该属性表示拖拽操作启动所需的最小距离。
如果你在应用中支持拖放，并且想在用户按住按钮移动光标一定距离后启动拖放操作，你应该用该属性的值作为所需的最小距离。
例如，如果点击的鼠标位置存储在`startPos`，当前位置（例如鼠标移动事件中）是`currentPos`，你可以通过以下代码判断是否应该开始拖动：
Qt在内部使用该值，例如`QFileDialog`。
默认值（如果平台没有提供不同的默认值）是10像素。

**如何使用：** 调用 `startDragDistance()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 if ((startPos - currentPos).manhattanLength() >=
         QApplication::startDragDistance())
     startTheDrag();
```

### `startDragTime : int`

**作用与语义：**

该特性表示按住鼠标按键的时间（毫秒）才会开始拖放操作。
如果你的应用程序支持拖放，并且想在用户按住鼠标按键一定时间后启动拖放操作，你应该用该属性的值作为延迟。
Qt也在内部使用这种延迟，例如在`QTextEdit`和`QLineEdit`中，用于启动拖拽。
默认值是500毫秒。

**如何使用：** 调用 `startDragTime()` 读取当前值；它不会修改应用状态。

### `styleSheet : QString`

**作用与语义：**

该属性包含应用样式表。
默认情况下，除非用户在运行应用时在命令行中指定`-stylesheet`选项，否则该属性会返回空字符串。

**如何使用：** 调用 `styleSheet()` 读取当前值；它不会修改应用状态。

### `wheelScrollLines : int`

**作用与语义：**

该属性包含旋转鼠标滚轮时，用于滚动控件的行数。
如果该值超过了控件可见的行数，控件应将滚动操作解释为单页向上或向下。如果控件是物品视图类，那么滚动一行的结果取决于控件滚动模式的设置。滚动一行可以表示滚动一个项目或滚动一个像素。
默认情况下，该属性的值为3。

**如何使用：** 调用 `wheelScrollLines()` 读取当前值；它不会修改应用状态。

### `QApplication::QApplication(int &argc, char **argv)`

**作用与语义：**

初始化窗口系统并使用 `argc` 命令行参数在 `argv` 中构建应用程序对象。
警告：`argc` 和 `argv` 所引用的数据在 QApplication 对象的整个生命周期内必须保持有效。此外，`argc` 必须大于零，且 `argv` 必须包含至少一个有效的字符串。
全局 `qApp` 指针指向此应用程序对象。只应创建一个应用程序对象。
此应用程序对象必须在任何绘图设备（包括小部件、像素图、位图等）之前构建。
注意：`argc` 和 `argv` 可能会在 Qt 删除其识别的命令行参数时发生变化。
所有 Qt 程序自动支持以下命令行选项：
- -style= style，设置应用程序的 GUI 样式。可用值取决于您的系统配置。如果您使用了额外样式编译 Qt 或将额外样式作为插件，这些将可通过 `-style` 命令行选项使用。您还可以通过设置 `QT_STYLE_OVERRIDE` 环境变量为所有 Qt 应用程序设置样式。
- -style style，与上述相同。
- -stylesheet= stylesheet，设置应用程序的样式表。值必须是包含样式表的文件路径。
注意：样式表文件中的相对 URL 是相对于样式表文件的路径的。
- -stylesheet stylesheet，与上述相同。
- -widgetcount，在结束时打印调试信息，显示未销毁的小部件数量以及同时存在的小部件最多数量。
- -reverse，将应用程序的布局方向设置为 `Qt::RightToLeft`。
- -qmljsdebugger=，使用指定端口激活 QML/JS 调试器。值的格式必须为 port:1234[,block]，其中 block 可选，如果指定，应用程序将等待调试器连接。

### `[virtual noexcept] QApplication::~QApplication()`

**作用与语义：**

清理该应用程序分配的窗口系统资源。将全局变量 `qApp` 设置为 `nullptr`。

### `[static slot] void QApplication::aboutQt()`

**作用与语义：**

显示一个关于Qt的简单消息框。该消息包含应用程序使用的Qt版本号。
这对于应用的帮助菜单中出现非常有用，如菜单示例所示。
这个功能是`QMessageBox::aboutQt()`的便利时段。

### `[static] QWidget *QApplication::activeModalWidget()`

**作用与语义：**

返回激活的模态小部件。
模态小部件是一种特殊的顶层小部件，是`QDialog`的一个子类，指定构造函数的模态参数为真。必须关闭模态小部件，用户才能继续程序的其他部分。
模态小部件组织成栈。该函数返回栈顶端的活跃模态小部件。

### `[static] QWidget *QApplication::activePopupWidget()`

**作用与语义：**

返回激活的弹窗小部件。
弹出小部件是一个特殊的顶层小部件，用于设置`Qt::WType_Popup`小部件标志，例如`QMenu`小部件。当应用程序打开弹出小部件时，所有事件都会发送到弹出小部件。普通小部件和模态小部件在弹出小部件关闭前无法访问。
当弹出小部件出现时，只有其他弹出小部件可以被打开。弹出小部件被组织成堆栈。该函数返回栈顶的激活弹出小部件。

### `[static] QWidget *QApplication::activeWindow()`

**作用与语义：**

返回包含键盘输入焦点的应用顶层窗口;如果没有应用程序窗口，则返回`nullptr`。即使没有`focusWidget()`，例如该窗口中没有控件接受键事件，也可能存在 activeWindow()。

### `[static] void QApplication::alert(QWidget *widget, int msec = 0)`

**作用与语义：**

如果窗口不是激活窗口，会显示`widget`警报。警报显示时间为`msec`毫秒。如果`msec`为零（默认值），则警报会无限期显示，直到窗口再次激活。
目前，这个函数在 Qt for Embedded Linux 上没有任何作用。
在macOS上，这更多是在应用层面起作用，会导致应用图标在底座上跳动。
在Windows上，这会导致窗口的任务栏条目闪烁一段时间。如果`msec`为零，闪烁会停止，任务栏条目会变成不同的颜色（目前是橙色）。
在 X11 上，这会导致窗口被标记为“需要注意”，窗口必须不能被隐藏（即不能调用 hide()，但必须以某种方式可见，才能实现。

### `[static] QWidgetList QApplication::allWidgets()`

**作用与语义：**

返回应用程序中所有控件的列表。
如果没有控件，列表为空（`QList::isEmpty()`）。
注意：部分小部件可能被隐藏。

**官方示例：**

```cpp
 void updateAllWidgets()
 {
     const QWidgetList allWidgets = QApplication::allWidgets();
     for (QWidget *widget : allWidgets)
         widget->update();
 }
```

### `[static] void QApplication::beep()`

**作用与语义：**

按铃，使用默认音量和声音。该功能在 Qt for Embedded Linux 中没有。

### `[static slot] void QApplication::closeAllWindows()`

**作用与语义：**

关闭所有顶层窗口。
该功能对于拥有多个顶层窗口的应用程序尤其有用。
窗口以随机顺序关闭，直到某个窗口不接受关闭事件。当最后一个窗口成功关闭时，应用程序退出，除非`quitOnLastWindowClosed`设置为false。如从菜单触发应用终止，请使用`QCoreApplication::quit()`代替此功能。

### `[override virtual protected] bool QApplication::event(QEvent *e)`

**作用与语义：**

重装：`QGuiApplication::event`（QEvent *e）。

### `[static] int QApplication::exec()`

**作用与语义：**

进入主事件循环，等待调用`exit()`，然后返回设定为`exit()`的值（如果通过`quit()`调用`exit()`则为0）。
启动事件处理需要调用该函数。主事件循环接收来自窗口系统的事件，并将其分发给应用控件。
通常，调用exec()之前不能进行任何用户交互。作为特殊情况，像`QMessageBox`这样的模态小部件可以在调用exec()之前使用，因为模态小部件调用exec()来启动本地事件循环。
为了让你的应用程序执行空闲处理，即在没有待处理事件时执行特殊函数，可以使用超时为0ns的`QChronoTimer`。更高级的空闲处理方案可以通过`processEvents()`实现。
我们建议你将清理代码连接到`aboutToQuit()`信号，而不是放在应用程序的`main()`函数中。这是因为在某些平台上，QApplication：：exec() 调用可能不会返回。例如，在 Windows 平台上，当用户登出时，系统会在 Qt 关闭所有顶层窗口后终止进程。因此，应用程序无法保证在 QApplication：：exec() 调用后，`main()`函数结束时有时间退出事件循环并执行代码。

### `[signal] void QApplication::focusChanged(QWidget *old, QWidget *now)`

**作用与语义：**

当键盘焦点从`old`变成`now`时，即用户按下Tab键、点击小部件或更改活动窗口时，会发出该信号。`old`和`now`都可以`nullptr`。
信号是在两个小部件都通过`QFocusEvent`收到变更通知后发出的。

### `[static] QWidget *QApplication::focusWidget()`

**作用与语义：**

返回带有键盘输入焦点的应用程序控件;如果该应用程序中没有控件，则返回`nullptr`。

### `[static] QFont QApplication::font()`

**作用与语义：**

返回默认的应用字体。

### `[static] QFont QApplication::font(const QWidget *widget)`

**作用与语义：**

返回该`widget`的默认字体。如果默认字体未为`widget`类注册，则返回其最近注册超类的默认字体。

### `[static] QFont QApplication::font(const char *className)`

**作用与语义：**

返回给定`className`小部件的字体。

### `[static] bool QApplication::isEffectEnabled(Qt::UIEffect effect)`

**作用与语义：**

如果启用了`effect`，则返回`true`；否则返回`false`。
默认情况下，Qt将尝试使用桌面设置。要防止这种情况，请调用setDesktopSettingsAware(false)。
注意：在色深低于16位的屏幕上，所有效果都被禁用。

### `[static] Qt::NavigationMode QApplication::navigationMode()`

**作用与语义：**

返回Qt使用的焦点导航类型。
此功能仅在 Qt for Embedded Linux 中提供。

### `[override virtual] bool QApplication::notify(QObject *receiver, QEvent *e)`

**作用与语义：**

重实现自：`QGuiApplication::notify`（QObject *对象，QEvent *事件）。

### `[static] QPalette QApplication::palette(const QWidget *widget)`

**作用与语义：**

如果传递`widget`，则返回该控件类的默认调色板。这可能是应用调色板，也可能不是。大多数情况下，某些类型的控件没有专门的调色板，但一个显著的例外是Windows下弹出菜单，如果用户在显示设置中为菜单定义了特殊背景色。

### `[static] QPalette QApplication::palette(const char *className)`

**作用与语义：**

返回给定`className`小部件的调色板。

### `[static] void QApplication::setEffectEnabled(Qt::UIEffect effect, bool enable = true)`

**作用与语义：**

如果`enable`为真，`effect`启用UI效果，否则该效果不会被使用。
注意：在色深低于16位的屏幕上，所有特效均被禁用。

### `[static] void QApplication::setFont(const QFont &font, const char *className = nullptr)`

**作用与语义：**

将默认应用字体更改为`font`。如果`className`通过，该更改仅适用于继承`className`的类（如`QObject::inherits()`报告）。
应用程序启动时，默认字体取决于窗口系统。它可能因窗口系统版本和区域不同而变化。该功能允许您覆盖默认字体;但覆盖可能是个坏主意，因为例如，某些区域需要超大字体来支持其特殊字符。
警告：请勿将此功能与 Qt 样式表一起使用。应用程序的字体可以通过“font”样式表属性进行自定义。要为所有 QPushButtons 设置加粗字体，请将应用 `styleSheet()` 设置为“`QPushButton` { font： bold }”。

### `[static] void QApplication::setNavigationMode(Qt::NavigationMode mode)`

**作用与语义：**

设定Qt应该用来`mode`的焦点导航方式。
此功能仅在 Qt for Embedded Linux 中提供。

### `[static] void QApplication::setPalette(const QPalette &palette, const char *className = nullptr)`

**作用与语义：**

将应用调色板改为`palette`。
如果通过`className`，变更仅适用于继承`className`的控件（如`QObject::inherits()`报告）。如果`className`保持为0，则该更改影响所有控件，从而覆盖之前设置的类别特定调色板。
调色板可根据当前的图形界面样式在`QStyle::polish()`进行更改。
警告：请勿将此功能与 Qt 样式表结合使用。使用样式表时，控件的调色板可以通过“color”、“background-color”、“selection-color”、“selection-background-color”和“alternate-background-color”来自定义。
注意：有些样式并非所有绘图都使用调色板，例如，如果它们使用了原生主题引擎。这适用于Windows Vista和macOS样式。

### `[static] void QApplication::setStyle(QStyle *style)`

**作用与语义：**

将应用程序的图形界面样式设置为`style`。样式对象的所有权转移给`QApplication`，因此`QApplication`在应用结束或设置新样式且旧样式仍为应用对象父样式时删除样式对象。
用例：
切换应用样式时，调色板会被设置回初始颜色，或者系统默认。这是必要的，因为某些样式必须调整调色板以完全符合样式指南。
在调色板尚未设置之前设置样式，即在创建`QApplication`之前，应用程序会为调色板使用`QStyle::standardPalette()`。
警告：Qt 样式表目前不支持 custom `QStyle` 子类。我们计划在未来的某个版本中解决这个问题。

**官方示例：**

```cpp
 QApplication::setStyle(QStyleFactory::create("Fusion"));
```

### `[static] QStyle *QApplication::setStyle(const QString &style)`

**作用与语义：**

请求`QStyleFactory`的`QStyle`对象进行`style`。
字符串必须是`QStyleFactory::keys()`之一，通常是“windows”、“windowsvista”、“fusion”或“macos”之一。样式名称不区分大小写。
如果传递未知`style`，返回`nullptr`，否则返回的`QStyle`对象将设置为应用程序的GUI样式。
警告：为了确保应用程序的样式正确设置，最好在`QApplication`构造函数之前调用该函数。

### `[static] QStyle *QApplication::style()`

**作用与语义：**

返回应用的样式对象。

### `[static] QWidget *QApplication::topLevelAt(const QPoint &point)`

**作用与语义：**

返回给定`point`的顶层控件;如果没有此类控件，返回`nullptr`。

### `[static] QWidget *QApplication::topLevelAt(int x, int y)`

**作用与语义：**

返回点（`x`， `y`）的顶层小部件;如果没有该小部件，则返回0。

### `[static] QWidgetList QApplication::topLevelWidgets()`

**作用与语义：**

返回应用程序中顶层控件（窗口）的列表。
注意：一些顶层小部件可能被隐藏，例如如果当前没有提示，则会显示提示。

**官方示例：**

```cpp
 void showAllHiddenTopLevelWidgets()
 {
     const QWidgetList topLevelWidgets = QApplication::topLevelWidgets();
     for (QWidget *widget : topLevelWidgets) {
         if (widget->isHidden())
             widget->show();
     }
 }
```

### `[static] QWidget *QApplication::widgetAt(const QPoint &point)`

**作用与语义：**

返回全局屏幕位置`point`的控件，或者如果那里没有Qt控件，则返回`nullptr`。
这个功能可能很慢。

### `[static] QWidget *QApplication::widgetAt(int x, int y)`

**作用与语义：**

返回全局屏幕位置（`x`、`y`），如果没有Qt小部件则返回`nullptr`。

### `qApp`

**作用与语义：**

指代唯一应用对象的全局指针。它等价于`QCoreApplication::instance()`，但被映射为`QApplication`指针，因此仅在唯一应用对象是`QApplication`时才有效。

### `bool autoSipEnabled() const`

**作用与语义：**

切换自动SIP（软件输入面板）可视化。
将该属性设置为`true`，以便在输入接受键盘输入的小部件时自动显示SIP。该属性仅影响设置WA_InputMethodEnabled属性的小部件，通常用于在键数极少或没有键的设备上启动虚拟键盘。
该特性仅对使用软件输入面板的平台产生影响。
默认是平台相关。

**如何使用：** 调用 `autoSipEnabled()` 读取当前值；它不会修改应用状态。

### `QString styleSheet() const`

**作用与语义：**

该属性包含应用样式表。
默认情况下，除非用户在运行应用时在命令行中指定`-stylesheet`选项，否则该属性会返回空字符串。

**如何使用：** 调用 `styleSheet()` 读取当前值；它不会修改应用状态。

### `void setAutoSipEnabled(const bool enabled)`

**作用与语义：**

切换自动SIP（软件输入面板）可视化。
将该属性设置为`true`，以便在输入接受键盘输入的小部件时自动显示SIP。该属性仅影响设置WA_InputMethodEnabled属性的小部件，通常用于在键数极少或没有键的设备上启动虚拟键盘。
该特性仅对使用软件输入面板的平台产生影响。
默认是平台相关。

**如何使用：** 调用 `setAutoSipEnabled(...)` 修改 `autoSipEnabled`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setStyleSheet(const QString &sheet)`

**作用与语义：**

该属性包含应用样式表。
默认情况下，除非用户在运行应用时在命令行中指定`-stylesheet`选项，否则该属性会返回空字符串。

**如何使用：** 调用 `setStyleSheet(...)` 修改 `styleSheet`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `int cursorFlashTime()`

**作用与语义：**

该特性将文本光标的闪烁时间以毫秒计定。
闪光时间是显示、反转和恢复插入图显示所需的时间。通常文本光标显示时间为光标闪光时间的一半，然后隐藏同样时间，但时间可能有所不同。
X11 的默认值是 1000 毫秒。在 Windows 上，使用控制面板值，设置该属性会设置所有应用程序的光标闪烁时间。
我们建议小部件不要缓存该值，因为如果用户更改全局桌面设置，该值随时可能发生变化。
注意：该属性可能为负值，例如禁用光标闪烁。

**如何使用：** 调用 `cursorFlashTime()` 读取当前值；它不会修改应用状态。

### `int doubleClickInterval()`

**作用与语义：**

该特性具有以毫秒为单位的时间限制，将双击点击与连续两次鼠标点击区分开来。
X11 的默认值是 400 毫秒。在 Windows 和 Mac OS 上，使用操作系统的值。

**如何使用：** 调用 `doubleClickInterval()` 读取当前值；它不会修改应用状态。

### `int keyboardInputInterval()`

**作用与语义：**

该特性具有以毫秒为单位的时间限制，用以区分按键与连续两次按键。
X11 的默认值是 400 毫秒。在 Windows 和 Mac OS 上，使用操作系统的值。

**如何使用：** 调用 `keyboardInputInterval()` 读取当前值；它不会修改应用状态。

### `void setCursorFlashTime(int)`

**作用与语义：**

该特性将文本光标的闪烁时间以毫秒计定。
闪光时间是显示、反转和恢复插入图显示所需的时间。通常文本光标显示时间为光标闪光时间的一半，然后隐藏同样时间，但时间可能有所不同。
X11 的默认值是 1000 毫秒。在 Windows 上，使用控制面板值，设置该属性会设置所有应用程序的光标闪烁时间。
我们建议小部件不要缓存该值，因为如果用户更改全局桌面设置，该值随时可能发生变化。
注意：该属性可能为负值，例如禁用光标闪烁。

**如何使用：** 调用 `setCursorFlashTime(...)` 修改 `cursorFlashTime`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setDoubleClickInterval(int)`

**作用与语义：**

该特性具有以毫秒为单位的时间限制，将双击点击与连续两次鼠标点击区分开来。
X11 的默认值是 400 毫秒。在 Windows 和 Mac OS 上，使用操作系统的值。

**如何使用：** 调用 `setDoubleClickInterval(...)` 修改 `doubleClickInterval`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setKeyboardInputInterval(int)`

**作用与语义：**

该特性具有以毫秒为单位的时间限制，用以区分按键与连续两次按键。
X11 的默认值是 400 毫秒。在 Windows 和 Mac OS 上，使用操作系统的值。

**如何使用：** 调用 `setKeyboardInputInterval(...)` 修改 `keyboardInputInterval`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setStartDragDistance(int l)`

**作用与语义：**

该属性表示拖拽操作启动所需的最小距离。
如果你在应用中支持拖放，并且想在用户按住按钮移动光标一定距离后启动拖放操作，你应该用该属性的值作为所需的最小距离。
例如，如果点击的鼠标位置存储在`startPos`，当前位置（例如鼠标移动事件中）是`currentPos`，你可以通过以下代码判断是否应该开始拖动：
Qt在内部使用该值，例如`QFileDialog`。
默认值（如果平台没有提供不同的默认值）是10像素。

**如何使用：** 调用 `setStartDragDistance(...)` 修改 `startDragDistance`；传入的新值会成为后续查询和相关界面行为所使用的值。

**官方示例：**

```cpp
 if ((startPos - currentPos).manhattanLength() >=
         QApplication::startDragDistance())
     startTheDrag();
```

### `void setStartDragTime(int ms)`

**作用与语义：**

该特性表示按住鼠标按键的时间（毫秒）才会开始拖放操作。
如果你的应用程序支持拖放，并且想在用户按住鼠标按键一定时间后启动拖放操作，你应该用该属性的值作为延迟。
Qt也在内部使用这种延迟，例如在`QTextEdit`和`QLineEdit`中，用于启动拖拽。
默认值是500毫秒。

**如何使用：** 调用 `setStartDragTime(...)` 修改 `startDragTime`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setWheelScrollLines(int)`

**作用与语义：**

该属性包含旋转鼠标滚轮时，用于滚动控件的行数。
如果该值超过了控件可见的行数，控件应将滚动操作解释为单页向上或向下。如果控件是物品视图类，那么滚动一行的结果取决于控件滚动模式的设置。滚动一行可以表示滚动一个项目或滚动一个像素。
默认情况下，该属性的值为3。

**如何使用：** 调用 `setWheelScrollLines(...)` 修改 `wheelScrollLines`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `int startDragDistance()`

**作用与语义：**

该属性表示拖拽操作启动所需的最小距离。
如果你在应用中支持拖放，并且想在用户按住按钮移动光标一定距离后启动拖放操作，你应该用该属性的值作为所需的最小距离。
例如，如果点击的鼠标位置存储在`startPos`，当前位置（例如鼠标移动事件中）是`currentPos`，你可以通过以下代码判断是否应该开始拖动：
Qt在内部使用该值，例如`QFileDialog`。
默认值（如果平台没有提供不同的默认值）是10像素。

**如何使用：** 调用 `startDragDistance()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 if ((startPos - currentPos).manhattanLength() >=
         QApplication::startDragDistance())
     startTheDrag();
```

### `int startDragTime()`

**作用与语义：**

该特性表示按住鼠标按键的时间（毫秒）才会开始拖放操作。
如果你的应用程序支持拖放，并且想在用户按住鼠标按键一定时间后启动拖放操作，你应该用该属性的值作为延迟。
Qt也在内部使用这种延迟，例如在`QTextEdit`和`QLineEdit`中，用于启动拖拽。
默认值是500毫秒。

**如何使用：** 调用 `startDragTime()` 读取当前值；它不会修改应用状态。

### `int wheelScrollLines()`

**作用与语义：**

该属性包含旋转鼠标滚轮时，用于滚动控件的行数。
如果该值超过了控件可见的行数，控件应将滚动操作解释为单页向上或向下。如果控件是物品视图类，那么滚动一行的结果取决于控件滚动模式的设置。滚动一行可以表示滚动一个项目或滚动一个像素。
默认情况下，该属性的值为3。

**如何使用：** 调用 `wheelScrollLines()` 读取当前值；它不会修改应用状态。

## 6. 深入实践与常见坑

### 生命周期和资源边界

控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

### 状态和错误边界

控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

### 线程边界

所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

### 最容易出现的错误

不要在 QApplication 前创建 QWidget；不要在 GUI 线程执行耗时循环；高 DPI、平台风格和命令行参数应在构造或显示窗口前配置。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QApplication` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
