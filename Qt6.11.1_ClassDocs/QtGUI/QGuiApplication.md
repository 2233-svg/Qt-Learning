# QGuiApplication

> Qt 6.11.1 · Qt GUI · 来自 `QGuiApplication`

## 1. 先建立直觉

**一句话定位：** `QGuiApplication` 是非 Widgets GUI 程序的进程级入口，负责初始化窗口系统、管理 GUI 事件循环、屏幕/输入/剪贴板/调色板等全局 GUI 状态。

### 这是什么

`QGuiApplication` 不是窗口，也不是所有窗口的父对象；它是 Qt GUI 层和操作系统窗口系统之间的应用上下文。只要程序使用 `QWindow`、Qt Quick、剪贴板、输入法、屏幕信息、光标覆盖、高 DPI 策略等 GUI 能力，就需要先创建一个 `QGuiApplication` 对象。

它位于 `QCoreApplication` 和 `QApplication` 之间：比 `QCoreApplication` 多了 GUI 平台集成，比 `QApplication` 少了 Widgets 风格系统。Qt Quick 或纯 `QWindow` 程序通常使用它；只要程序创建 `QWidget`，就应该使用 `QApplication`。

### 适合使用的场景

- Qt Quick/QML 应用，例如 `QQmlApplicationEngine` 加载 QML 界面。
- 使用 `QWindow`、`QRasterWindow`、OpenGL/Vulkan/RHI 窗口但不使用 Widgets。
- 需要访问全局 GUI 状态：屏幕列表、主屏幕、剪贴板、输入法、鼠标/键盘修饰键、系统字体和调色板。
- 需要处理平台会话恢复、最后窗口关闭退出、应用状态变化等进程级 GUI 行为。

### 不适合的场景

- 控制台工具或服务进程：用 `QCoreApplication`。
- 任何创建 `QWidget`、`QDialog`、`QMainWindow` 的应用：用 `QApplication`。
- 想把它当作业务单例或窗口管理器：它只提供 Qt GUI 全局状态，业务生命周期应放在自己的对象里。

### 典型调用链

```cpp
#include <QGuiApplication>
#include <QQmlApplicationEngine>

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);
    QGuiApplication::setApplicationDisplayName(QObject::tr("Image Desk"));

    QQmlApplicationEngine engine;
    engine.loadFromModule("ImageDesk", "Main");
    if (engine.rootObjects().isEmpty())
        return -1;

    return QGuiApplication::exec();
}
```

**先记住的坑：** 一个进程只能有一个应用对象；它必须在任何 GUI 对象、`QPixmap`、窗口或 Qt Quick 引擎之前创建；GUI 对象通常属于主线程；`exec()` 进入事件循环后，异步结果靠信号、事件和状态变化返回。

## 2. 依赖与对象关系

- 头文件：`#include <QGuiApplication>`
- CMake：`find_package(Qt6 REQUIRED COMPONENTS Gui)`，并链接 `Qt6::Gui`
- 继承自：`QCoreApplication`
- 直接派生类：`QApplication`
- 全局指针：`qGuiApp` 指向当前 `QGuiApplication` 实例

### 生命周期

`QGuiApplication` 通常是 `main()` 里的栈对象。`argc` 和 `argv` 引用的数据必须在它整个生命周期内有效，因为 Qt 会解析并移除自己识别的命令行参数。析构时平台 GUI 资源会被释放，所以不要让窗口、渲染资源或剪贴板访问跨过应用对象的生命周期。

### 线程和事件循环

它管理主 GUI 事件循环。窗口、输入法、剪贴板、屏幕对象、Qt Quick GUI 对象都应在 GUI 线程使用；后台线程通过 queued signal/slot 把结果送回 GUI 线程。`keyboardModifiers()`、`mouseButtons()` 这类状态查询依赖事件队列中已经处理过的输入事件，实时轮询时要理解这一点。

### 与 QApplication 的边界

`QGuiApplication` 只到 GUI 基础层；`QApplication` 在它之上增加了 QWidget、`QStyle`、Widgets 调色板/字体传播、焦点控件等能力。一个项目如果以后会引入 Widgets，入口应直接用 `QApplication`，不要混用两个应用对象。

## 3. API 速查

| API | 用途速查 |
|---|---|
| `applicationDisplayName : QString` | 用户可见的应用名，常用于窗口系统、任务切换和桌面环境展示。 |
| `desktopFileName : QString` | Linux/freedesktop 桌面文件基本名，用来把窗口和启动器、图标、桌面元数据关联起来。 |
| `layoutDirection : Qt::LayoutDirection` | 应用默认布局方向，影响采用默认方向的窗口和控件。 |
| `platformName : const QString` | 当前 QPA 平台插件名，适合诊断平台后端差异。 |
| `primaryScreen : QScreen*` | 当前主屏幕；多屏环境可能运行时变化。 |
| `quitOnLastWindowClosed : bool` | 最后一个可见主窗口关闭时是否自动退出事件循环。 |
| `windowIcon : QIcon` | 未单独指定图标的窗口使用的默认窗口图标。 |
| `QGuiApplication(int &argc, char **argv)` | 初始化 GUI 平台并解析 Qt 命令行参数。 |
| `~QGuiApplication()` | 释放 GUI 平台资源；通常随 `main()` 栈对象结束。 |
| `devicePixelRatio()` | 取得应用层面的设备像素比，用于高 DPI 兼容判断。 |
| `isSavingSession()` / `isSessionRestored()` | 判断是否正在保存会话、是否由桌面会话恢复启动。 |
| `nativeInterface<T>()` | 访问平台原生接口，适合不得不调用平台 API 的场景。 |
| `sessionId()` / `sessionKey()` | 获取桌面会话管理器分配的标识。 |
| `notify()` / `event()` | 事件分发钩子，只有做全局事件诊断或框架层封装时才重写。 |
| `setBadgeNumber()` | 在支持的平台上设置应用徽标数字。 |
| `applicationStateChanged()` | 监听应用激活、后台、挂起等状态变化。 |
| `focusObjectChanged()` / `focusWindowChanged()` | 监听 GUI 焦点对象或焦点窗口变化。 |
| `screenAdded()` / `screenRemoved()` / `primaryScreenChanged()` | 监听显示器热插拔和主屏幕变化。 |
| `commitDataRequest()` / `saveStateRequest()` | 响应桌面会话保存/注销流程。 |
| `allWindows()` / `topLevelWindows()` / `topLevelAt()` | 查询当前应用创建的窗口。 |
| `clipboard()` | 访问进程共享的 GUI 剪贴板对象。 |
| `exec()` | 进入 GUI 主事件循环。 |
| `font()` / `setFont()` | 读取或设置应用默认字体。 |
| `palette()` / `setPalette()` | 读取或设置应用默认调色板。 |
| `styleHints()` | 读取平台交互参数，例如双击间隔、拖拽距离等。 |
| `setOverrideCursor()` / `changeOverrideCursor()` / `restoreOverrideCursor()` | 管理全局覆盖光标栈。 |
| `keyboardModifiers()` / `queryKeyboardModifiers()` / `mouseButtons()` | 查询键盘修饰键和鼠标按钮状态。 |
| `screens()` / `screenAt()` | 查询屏幕列表或某个全局坐标所在屏幕。 |
| `setDesktopSettingsAware()` | 控制是否跟随桌面字体、调色板等系统设置。 |
| `setHighDpiScaleFactorRoundingPolicy()` | 设置高 DPI 缩放因子的取整策略，应在创建应用对象前配置。 |
| `sync()` | 强制与窗口系统同步；主要用于特殊诊断，不是常规刷新手段。 |
| `qGuiApp` | 当前 `QGuiApplication` 的便捷宏。 |

## 4. 重点 API 说明

### `applicationDisplayName : QString`

设置用户看到的应用名称。它比 `applicationName()` 更偏展示层，适合放本地化名称，例如中文产品名。窗口系统、任务切换器、桌面环境、通知中心可能读取这个名字。未设置时通常回退到 `QCoreApplication::applicationName()`；不要把它当作稳定配置键或文件路径的一部分。

### `desktopFileName : QString`

指定 Linux/freedesktop 桌面项的基本名，不含路径和 `.desktop` 后缀。桌面环境用它把窗口、任务栏图标、启动器和应用元数据匹配起来。比如桌面文件是 `org.example.Editor.desktop`，这里设置 `org.example.Editor`。这是桌面集成信息，不是窗口标题。

### `layoutDirection : Qt::LayoutDirection`

设置应用默认布局方向。阿拉伯语、希伯来语等从右到左语言需要 `Qt::RightToLeft`；中文、英文通常是 `Qt::LeftToRight`；也可以使用自动方向。它影响采用应用默认方向的窗口和界面对象，已经显式设置方向的对象不会自动被覆盖。

### `[read-only] platformName : const QString`

返回当前加载的 QPA 平台插件名称，例如 `windows`、`xcb`、`wayland`、`cocoa`、`offscreen`。适合诊断部署问题、区分 Wayland/X11、识别无界面测试后端。不建议把平台名写成大量业务分支的核心条件；优先检测具体能力。

### `[read-only] primaryScreen : QScreen*`

返回当前主屏幕对象。常用于决定默认窗口出现在哪块屏幕、读取屏幕 DPI/几何、处理首次窗口定位。多显示器环境会变化，保存 `QScreen *` 前要监听 `primaryScreenChanged()` 和 `screenRemoved()`。

### `quitOnLastWindowClosed : bool`

控制最后一个可见主窗口关闭时是否尝试退出应用。普通桌面应用保持默认 `true`；托盘应用、后台 GUI 服务、无常驻窗口工具通常设为 `false`。这只是退出策略，事件循环锁、被忽略的退出事件或局部事件循环仍可能影响最终退出。

### `windowIcon : QIcon`

设置应用级默认窗口图标。多窗口应用可用它统一任务栏/标题栏图标；具体窗口仍可用 `QWindow::setIcon()` 覆盖。不同平台显示位置、尺寸选择和缓存时机不同，最好在创建或显示窗口前设置。

### `QGuiApplication::QGuiApplication(int &argc, char **argv)`

初始化 GUI 平台、创建唯一应用对象，并解析 Qt 支持的命令行参数。所有 Qt Quick、`QWindow`、绘图设备相关 GUI 程序通常从 `QGuiApplication app(argc, argv);` 开始。

`argc` 必须大于 0，`argv` 至少有一个有效字符串，并且二者引用的数据要活到应用对象析构。Qt 可能会从参数中移除 `-platform`、`-qmljsdebugger`、`-reverse` 等自己识别的选项。应用对象必须早于 `QPixmap`、窗口、QML 引擎等 GUI 资源创建。

### `[virtual noexcept] QGuiApplication::~QGuiApplication()`

关闭 GUI 平台连接并释放应用级 GUI 资源。通常不手动调用，让 `main()` 中的栈对象在退出时自然析构。不要让窗口、剪贴板访问、输入法对象或渲染资源在应用对象析构后继续被访问。

### `[static] QWindowList QGuiApplication::allWindows()`

返回应用创建的所有窗口，包括顶层窗口和子窗口。适合调试窗口泄漏、遍历窗口做统一处理、统计当前 GUI 资源。返回的是调用时的列表快照；遍历时不要假定窗口在后续事件处理中仍然存在。

### `[static] Qt::ApplicationState QGuiApplication::applicationState()`

查询应用当前状态，例如活动、非活动、隐藏、挂起。常用于暂停动画、降低后台刷新频率、应用回到前台时刷新数据。实际项目里更常连接 `applicationStateChanged()`，不要高频轮询。

### `[signal] void QGuiApplication::applicationStateChanged(Qt::ApplicationState state)`

应用激活状态变化时发出。移动端进入后台可以暂停资源占用；桌面端失焦时可以停止不必要的实时更新。信号到来只说明平台状态变化，不等于所有窗口已经完成重绘或隐藏。

### `[static] void QGuiApplication::changeOverrideCursor(const QCursor &cursor)`

修改当前覆盖光标栈顶的光标。已经调用 `setOverrideCursor()` 后，可用它把等待光标改成禁止光标、十字光标等。没有覆盖光标时调用没有实际意义；覆盖光标是栈结构，结束时仍要成对恢复。

### `[static] QClipboard *QGuiApplication::clipboard()`

返回应用的剪贴板对象，用于读写文本、图片、MIME 数据，或监听外部剪贴板变化。返回指针由 Qt 管理，不要删除。剪贴板属于 GUI 平台资源，应在 GUI 线程使用。

### `[signal] void QGuiApplication::commitDataRequest(QSessionManager &manager)`

会话管理器要求应用提交未保存数据时发出，例如桌面注销、关机、会话保存。可在这里保存文档或决定是否允许会话结束。某些平台要求同步、快速完成，不要启动无法结束的交互流程。

### `[static] bool QGuiApplication::desktopSettingsAware()`

查询应用是否跟随桌面系统设置。它影响字体、调色板等平台默认值的采用方式。对应设置应在创建应用对象前配置，否则部分平台资源可能已经初始化。

### `qreal QGuiApplication::devicePixelRatio() const`

返回应用层面可用的设备像素比，主要用于高 DPI 兼容判断。多屏环境下窗口实际像素比应优先查看对应 `QWindow` 或 `QScreen`；不要用一个全局值推断所有窗口。

### `[override virtual protected] bool QGuiApplication::event(QEvent *e)`

处理发给应用对象自身的事件。派生应用类需要捕获应用级事件时才重写。不处理的事件必须交给基类，否则可能破坏 Qt 的会话、文件打开、平台状态等内部事件。

### `[static] int QGuiApplication::exec()`

进入主 GUI 事件循环，直到 `quit()`、最后窗口关闭退出策略或平台退出事件使它结束。`main()` 创建窗口或 QML 引擎后调用，并把返回值作为进程退出码。`exec()` 之后的代码要等事件循环退出才会执行；耗时任务应放到线程或异步流程。

### `[static] QObject *QGuiApplication::focusObject()`

返回当前拥有输入焦点的对象。适合输入法、快捷键路由、调试焦点问题。返回值可能为空，也可能不是窗口本身；保存指针时要关注对象生命周期。

### `[signal] void QGuiApplication::focusObjectChanged(QObject *focusObject)`

焦点对象变化时发出。可根据当前输入目标更新输入法面板、状态栏或快捷键上下文。`focusObject` 可能为空，槽函数里应判空。

### `[static] QWindow *QGuiApplication::focusWindow()`

返回当前拥有焦点的窗口。适合获取活动窗口的屏幕、设置窗口相关行为、诊断焦点切换。没有焦点窗口时返回 `nullptr`。

### `[signal] void QGuiApplication::focusWindowChanged(QWindow *focusWindow)`

焦点窗口变化时发出。多窗口应用可同步工具栏、全局动作或状态栏。切换过程中可能先收到空指针，再收到新窗口。

### `[static] QFont QGuiApplication::font()`

返回应用默认字体。常用于绘制自定义文本、初始化非 QWidget 界面元素字体。桌面字体变化可能让默认字体改变，不要长期缓存后忽略字体数据库变化。

### `[signal] void QGuiApplication::fontDatabaseChanged()`

系统字体数据库变化时发出。字体选择器、文本布局缓存和字体预览界面可在这里刷新。字体文件安装/移除、平台字体回退变化都可能触发。

### `[static] Qt::HighDpiScaleFactorRoundingPolicy QGuiApplication::highDpiScaleFactorRoundingPolicy()`

查询高 DPI 缩放因子取整策略。用于诊断多屏缩放下界面尺寸、图像模糊或像素对齐问题。设置策略要尽早，通常在创建应用对象之前。

### `[static] QInputMethod *QGuiApplication::inputMethod()`

返回应用输入法对象。可控制软键盘、查询输入面板矩形、处理复杂文本输入。指针由 Qt 管理，只有平台和输入控件支持时相关状态才有意义。

### `[static] bool QGuiApplication::isLeftToRight()`

判断当前应用布局方向是否为从左到右。自绘控件或自定义布局需要根据方向翻转几何时使用。如果某个窗口或对象显式设置了方向，应以对象自身方向为准。

### `[static] bool QGuiApplication::isRightToLeft()`

判断当前应用布局方向是否为从右到左。用于国际化界面、自绘箭头和水平布局镜像。不要只靠语言代码判断方向，优先使用 Qt 的方向 API。

### `bool QGuiApplication::isSavingSession() const`

判断应用当前是否处于会话保存流程。可在退出/关机/注销时区分普通关闭和会话保存。只在支持会话管理的平台和流程中有实际意义。

### `bool QGuiApplication::isSessionRestored() const`

判断应用是否由先前桌面会话恢复启动。可据此恢复窗口布局、最近文档、未完成工作状态。它不是应用自己的崩溃恢复机制，仍需要业务层保存状态。

### `[static] Qt::KeyboardModifiers QGuiApplication::keyboardModifiers()`

返回事件队列中最后处理过的键盘修饰键状态。适合在事件处理器内部判断 Shift/Ctrl/Alt 状态。需要即时硬件状态时用 `queryKeyboardModifiers()`。

### `[signal] void QGuiApplication::lastWindowClosed()`

最后一个可见主窗口关闭时发出。适合保存状态、清理临时资源、托盘应用决定是否继续驻留。是否随后退出取决于 `quitOnLastWindowClosed` 和事件是否被接受。

### `[static] QWindow *QGuiApplication::modalWindow()`

返回当前活动的模态窗口。可用于判断输入为什么被阻塞，或把提示定位到当前模态上下文。没有模态窗口时返回 `nullptr`；不要绕过模态窗口直接操作被阻塞窗口。

### `[static] Qt::MouseButtons QGuiApplication::mouseButtons()`

返回事件队列中最后处理过的鼠标按钮状态。鼠标事件处理期间判断是否仍有按钮按下时很方便。它不是强制轮询硬件的接口。

### `template <typename QNativeInterface> QNativeInterface *QGuiApplication::nativeInterface() const`

返回平台原生接口对象。只有在 Qt 跨平台 API 覆盖不了需求时才使用，例如访问 Windows、macOS、X11、Wayland 的平台特有能力。调用前要用编译条件和空指针检查保护，不要让跨平台代码无条件依赖某个原生接口。

### `[override virtual] bool QGuiApplication::notify(QObject *object, QEvent *event)`

Qt 事件分发的中心入口之一，把事件投递给目标对象。全局事件监控、异常边界、埋点框架可能重写它。这是高风险钩子：通常必须调用基类，并避免抛异常、阻塞或吞掉未知事件。

### `[static] QCursor *QGuiApplication::overrideCursor()`

返回当前覆盖光标栈顶。可判断是否正处于等待光标、拖拽光标等全局覆盖状态。没有覆盖光标时返回 `nullptr`；不要删除返回指针。

### `[static] QPalette QGuiApplication::palette()`

返回应用默认调色板。自绘界面、Qt Quick/C++ 混合界面需要跟随系统颜色时会用到。调色板不是完整主题系统；深色模式、平台样式和 QML 控件主题还可能有其他规则。

### `[static] Qt::KeyboardModifiers QGuiApplication::queryKeyboardModifiers()`

查询当前硬件键盘修饰键状态。不在键盘事件内、但需要立即知道 Shift/Ctrl/Alt 状态时使用。它可能触发平台查询，语义不同于 `keyboardModifiers()` 的事件状态快照。

### `[static] void QGuiApplication::restoreOverrideCursor()`

弹出一层覆盖光标，恢复到上一层或系统光标。它必须与 `setOverrideCursor()` 成对出现。多次设置就要多次恢复；异常路径、提前返回和异步取消都要保证恢复。

### `[signal] void QGuiApplication::saveStateRequest(QSessionManager &manager)`

会话管理器要求保存可恢复状态时发出。适合保存窗口位置、打开文档列表、工作区状态，供下次会话恢复。它偏保存状态，不一定要求立刻提交所有业务数据。

### `[signal] void QGuiApplication::screenAdded(QScreen *screen)`

新屏幕加入时发出。用于更新屏幕选择器、重算窗口布局、迁移全屏窗口。新屏幕的几何和 DPI 应从 `screen` 或 `screens()` 重新读取。

### `[static] QScreen *QGuiApplication::screenAt(const QPoint &point)`

返回包含全局坐标 `point` 的屏幕。可用于在鼠标位置创建窗口、把弹出层放到正确显示器、处理多屏坐标。点不在任何屏幕上时返回 `nullptr`。

### `[signal] void QGuiApplication::screenRemoved(QScreen *screen)`

屏幕从应用可见屏幕集合中移除时发出。常见处理是把位于被移除屏幕上的窗口迁移回可用屏幕。不要在之后继续把这个 `screen` 当作可用显示器使用。

### `[static] QList<QScreen *> QGuiApplication::screens()`

返回当前可用屏幕列表。多屏设置界面、窗口恢复、DPI/几何枚举会用它。列表会随热插拔变化，不要把索引当作稳定屏幕 ID。

### `QString QGuiApplication::sessionId() const`

返回当前桌面会话 ID。可用于会话恢复、日志诊断、区分由会话管理器恢复的运行实例。是否可用取决于平台会话管理能力。

### `QString QGuiApplication::sessionKey() const`

返回当前会话键。通常与 `sessionId()` 一起识别一个可恢复会话实例。不要把它当作长期持久的用户身份或授权信息。

### `[slot, since 6.5] void QGuiApplication::setBadgeNumber(qint64 number)`

设置应用图标上的徽标数字，例如未读消息数、待处理任务数、下载数量。平台支持差异很大；不支持的平台可能无效果。传入 0 通常表示清除或隐藏徽标。

### `[static] void QGuiApplication::setDesktopSettingsAware(bool on)`

控制应用是否感知并采用桌面系统设置。嵌入式、主题完全自绘、测试环境可能想关闭桌面设置影响。应在创建应用对象前调用，太晚调用可能不会重置已经初始化的平台资源。

### `[static] void QGuiApplication::setFont(const QFont &font)`

设置应用默认字体。适合统一非 Widgets GUI 字体，或在 Qt Quick/C++ 自绘混合项目中保持一致。对已经显式指定字体的对象不一定生效；字体改变可能需要重新布局文本。

### `[static] void QGuiApplication::setHighDpiScaleFactorRoundingPolicy(Qt::HighDpiScaleFactorRoundingPolicy policy)`

设置高 DPI 缩放因子的取整策略。多屏缩放、非整数缩放比例下可用它控制尺寸取整和渲染清晰度。要在创建应用对象前调用；运行中改变无法可靠修复已创建窗口的缩放决策。

### `[static] void QGuiApplication::setOverrideCursor(const QCursor &cursor)`

把一个覆盖光标压入全局光标栈。长操作期间显示等待光标、临时绘图模式显示十字光标时常用。必须用 `restoreOverrideCursor()` 恢复；最好封装成 RAII，避免异常或早退遗留覆盖光标。

### `[static] void QGuiApplication::setPalette(const QPalette &pal)`

设置应用默认调色板。适合统一自绘界面颜色，或覆盖平台默认颜色。对 Qt Quick Controls、平台原生控件或自定义主题的影响有限；不要把调色板当作完整换肤系统。

### `[static] QStyleHints *QGuiApplication::styleHints()`

返回平台交互参数集合，例如双击间隔、拖拽阈值、鼠标按住时间等。指针由 Qt 管理，这些值可能随系统设置变化。

### `[static] void QGuiApplication::sync()`

请求 Qt 与底层窗口系统同步，并处理同步过程中产生的事件。主要用于特殊调试、平台插件测试、需要确认窗口系统状态已同步的低层代码。普通业务代码不应把它当作强制刷新 UI 的方法。

### `[static] QWindow *QGuiApplication::topLevelAt(const QPoint &pos)`

返回全局坐标 `pos` 下的顶层窗口。用于调试命中测试、实现全局拾取、决定弹出层归属。返回值只限当前应用窗口；坐标下是其他程序窗口时不会返回那个窗口。

### `[static] QWindowList QGuiApplication::topLevelWindows()`

返回当前应用的顶层窗口列表。可用于保存/恢复窗口状态、统一关闭窗口、查找主窗口。隐藏窗口也可能在列表里；是否可见需要另查窗口状态。

### `qGuiApp`

当前应用对象的便捷宏，等价于把 `qApp` 视为 `QGuiApplication *` 使用。它适合在较深调用栈中临时访问应用级 GUI 状态，但会隐藏依赖；可测试代码里更推荐显式传入需要的服务或对象。

### `void applicationDisplayNameChanged()`

应用显示名变化时发出。关于对话框、窗口标题策略、状态页中的应用名可连接它同步刷新。这是通知信号，不要手动调用。

### `void layoutDirectionChanged(Qt::LayoutDirection direction)`

应用默认布局方向变化时发出。自绘对象、缓存布局或非 Qt 布局系统可用它同步 RTL/LTR 变化。参数是新的应用默认方向；个别对象的显式方向仍需单独处理。

### `void primaryScreenChanged(QScreen *screen)`

主屏幕变化时发出。适合更新默认窗口位置、DPI 相关缓存、启动屏幕选择。`screen` 可能为空或随后又变化，稳妥做法是重新读取 `screens()`。

### `QString applicationDisplayName()`

返回应用显示名，常用于关于界面、通知标题和日志。没有显式设置时，结果可能来自 `applicationName()`。

### `QString desktopFileName()`

返回桌面文件基本名。主要用于诊断 Linux 桌面集成是否设置正确。空字符串表示未设置。

### `Qt::LayoutDirection layoutDirection()`

返回应用默认布局方向。自绘或自定义布局计算时使用。对象自身方向可能覆盖应用默认值。

### `QString platformName()`

返回 QPA 平台插件名。主要用于日志和诊断，与只读 `platformName` 属性语义相同。

### `QScreen * primaryScreen()`

返回主屏幕。用于默认窗口定位和 DPI 查询。与 `primaryScreen` 属性语义相同；返回指针不要跨屏幕移除事件长期使用。

### `bool quitOnLastWindowClosed()`

查询最后窗口关闭时是否自动退出。托盘应用或多窗口框架可用它检查退出策略。这只是策略值，不代表当前是否已经可以退出。

### `void setApplicationDisplayName(const QString &name)`

设置应用显示名。通常在应用启动后、显示首个窗口前设置本地化产品名。变化会触发 `applicationDisplayNameChanged()`。

### `void setDesktopFileName(const QString &name)`

设置 Linux 桌面文件基本名。打包为 `.desktop` 应用时可改善桌面环境匹配。只传基本名，不传路径和后缀。

### `void setLayoutDirection(Qt::LayoutDirection direction)`

设置应用默认布局方向。用户切换语言、测试 RTL 界面、强制某个应用方向时使用。变化会触发 `layoutDirectionChanged()`；已经创建的界面是否立即重排取决于对象和布局实现。

### `void setQuitOnLastWindowClosed(bool quit)`

设置最后窗口关闭时是否自动退出。托盘程序通常传 `false`；普通窗口应用保持 `true`。设置为 `false` 后必须提供显式退出入口，例如菜单动作调用 `quit()`。

### `void setWindowIcon(const QIcon &icon)`

设置应用默认窗口图标。一般在创建窗口前调用。某些平台会缓存图标，晚设置可能不能影响已经显示的窗口。

### `QIcon windowIcon()`

返回应用默认窗口图标。可复用到托盘、关于窗口或自定义标题栏。返回的是值对象，可安全保存；但实际显示效果仍由平台决定。

## 5. 深入实践与常见坑

### 初始化顺序

应用对象应尽量在 `main()` 的最前面创建。需要影响平台初始化的设置，例如高 DPI 取整策略和桌面设置感知，应在构造前完成；需要影响窗口展示的设置，例如显示名、默认图标、字体和调色板，应在创建或显示窗口前完成。

### 输入状态

`keyboardModifiers()` 和 `mouseButtons()` 返回的是 Qt 事件系统当前掌握的状态；`queryKeyboardModifiers()` 会向平台查询当前修饰键。事件处理器里通常用前者，非事件上下文里需要即时状态时用后者。

### 多屏和高 DPI

屏幕不是固定资源。用户可能插拔显示器、改变缩放、切换主屏幕。窗口定位、截图、DPI 换算和恢复窗口位置时，应把 `screenRemoved()`、`screenAdded()`、`primaryScreenChanged()` 纳入设计。

### 光标覆盖

覆盖光标是栈，不是单个全局变量。每一次 `setOverrideCursor()` 都应有对应的 `restoreOverrideCursor()`。如果多个模块都设置等待光标，随意恢复可能会把别人的覆盖状态弹掉。

### 平台差异

`setBadgeNumber()`、会话管理、桌面文件名、剪贴板模式、暗色模式、高 DPI 行为都带有平台差异。写跨平台代码时，优先用 Qt 抽象能力；必须使用平台行为时，把分支集中在少量平台适配层中。
