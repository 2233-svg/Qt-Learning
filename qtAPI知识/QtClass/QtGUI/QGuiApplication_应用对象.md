# QGuiApplication：GUI 进程的全局运行时

> Qt 版本：6.11.1  
> 模块：`Qt6::Gui`  
> 头文件：`#include <QGuiApplication>`  
> 继承：`QCoreApplication`

## 它解决什么问题

一个 GUI 进程需要统一初始化窗口系统、加载 QPA 平台插件、接收操作系统事件、维护屏幕和焦点状态，并提供剪贴板、输入法、系统字体等进程级服务。`QGuiApplication` 就是这些能力的唯一入口，同时继承 `QCoreApplication` 的事件循环、应用元数据、翻译器和退出控制。

每个 GUI 进程应精确创建一个应用对象：

- 纯命令行程序使用 `QCoreApplication`；
- `QWindow`、Qt Quick 或其他非 Widgets GUI 程序使用 `QGuiApplication`；
- 创建 `QWidget` 的程序必须使用其派生类 `QApplication`。

`QGuiApplication` 不是普通业务对象。它通常在 `main()` 的栈上最先构造、最后析构，并限定了绝大多数 GUI 操作的主线程边界。

## 最小程序与构造顺序

```cpp
#include <QGuiApplication>
#include <QWindow>

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);

    QWindow window;
    window.setTitle(QGuiApplication::applicationDisplayName());
    window.resize(800, 500);
    window.show();

    return app.exec();
}
```

必须先构造应用对象，才能创建窗口、`QPixmap`、`QBitmap` 等依赖 GUI 子系统的对象。`argc` 和 `argv` 指向的数据必须在应用对象的整个生命周期中有效；Qt 会识别并移除自己的命令行参数，所以构造后两者可能已被修改。

平台插件、桌面设置策略和高 DPI 舍入策略都涉及初始化阶段。需要设置这些策略时，应在构造应用对象之前调用对应静态函数。

## 应用对象与线程

应用对象以及窗口系统事件循环应位于 GUI 主线程。`QWindow`、绘制设备、剪贴板、输入法和屏幕对象等 GUI 资源也应在该线程访问。工作线程把结果通过 queued signal/slot 或 `QMetaObject::invokeMethod()` 送回 GUI 线程，不应直接修改窗口或调用依赖平台状态的全局接口。

`exec()` 启动主事件循环。窗口输入、重绘、计时器和 queued 信号通常都依赖它。清理工作优先连接 `QCoreApplication::aboutToQuit()`，因为某些平台上 `exec()` 不保证像普通函数那样返回到 `main()` 后继续执行。

## 窗口、焦点与退出

`allWindows()` 包含应用拥有的全部 `QWindow`，包括非顶层窗口；`topLevelWindows()` 只返回顶层窗口。`topLevelAt()` 使用全局屏幕坐标查找指定位置的顶层窗口，找不到时返回 `nullptr`。

`focusWindow()` 是当前接收键盘焦点的窗口，`focusObject()` 是焦点事件的最终接收对象，两者都可能为 `nullptr`，而且在激活切换时会动态变化。`modalWindow()` 返回当前模态窗口，不能用它代替完整的模态栈管理。

`quitOnLastWindowClosed` 默认为 `true`。最后一个可见的主要窗口，也就是没有 transient parent 的顶层窗口关闭时，Qt 会尝试退出并发出 `lastWindowClosed()`。这只是“尝试”：

- `QEventLoopLocker` 仍可阻止退出；
- `QEvent::Quit` 可被忽略；
- 工具窗口或有 transient parent 的次要窗口不按主要窗口计算；
- 托盘应用通常应设为 `false`，再由明确的“退出”命令结束进程。

## 屏幕是动态资源

`screens()`、`primaryScreen()` 和 `screenAt()` 返回的 `QScreen *` 由 Qt 平台层管理，调用方不能删除。显示器可热插拔，主屏幕也会变化，不要把裸指针当成进程永久有效资源。

需要长期跟踪屏幕时，应连接：

- `screenAdded(QScreen *)`；
- `screenRemoved(QScreen *)`；
- `primaryScreenChanged(QScreen *)`；
- 必要时再连接 `QScreen` 自身的 geometry、DPI 和 orientation 变化信号。

`screenRemoved()` 发出时，应用可先处理位于该屏幕上的窗口，随后 Qt 可能把它们迁移到主屏幕。

`devicePixelRatio()` 返回系统所有屏幕中最高的 DPR，只适合不知道目标窗口时作保守查询。已经知道目标窗口或屏幕时，应优先使用 `QWindow::devicePixelRatio()` 或 `QScreen::devicePixelRatio()`。

## 全局外观与平台设置

`font()`、`palette()` 和 `styleHints()` 提供应用级默认外观。平台主题仍会参与最终结果，尤其 `setPalette()` 提供的颜色角色会与系统平台主题组合。对某个窗口或组件有独立要求时，应设置局部值，不要轻易把整个应用的默认值当作每个对象的最终值。

`setDesktopSettingsAware(false)` 禁止采用系统标准颜色、字体等设置，且必须在构造应用对象前调用。默认是 `true`。

`setHighDpiScaleFactorRoundingPolicy()` 决定如何处理 150% 等非整数缩放，默认是 `PassThrough`。它同样必须在应用对象构造前调用。改变策略可能影响尺寸取整和风格绘制，应在目标平台及混合 DPI 多屏环境中测试。

## 应用标识

- `applicationDisplayName` 是面向用户、可翻译的名称；未设置时退回 `applicationName`。
- `desktopFileName` 是 freedesktop 桌面条目的基本文件名，不含路径和 `.desktop` 后缀，主要影响 Linux 桌面集成。
- `windowIcon` 是窗口未设置自身图标时使用的应用级默认图标。
- `platformName` 是实际 QPA 平台插件名，例如 `windows`、`cocoa`、`wayland`、`xcb` 或 `offscreen`。

构造函数会处理 `-platform`、`-platformpluginpath` 等 Qt 参数。也可通过 `QT_QPA_PLATFORM` 等环境变量选择平台插件。平台名是部署环境的一部分，不宜用作业务逻辑的唯一能力判断；优先检测具体能力或原生接口是否存在。

## 输入状态、光标、剪贴板与输入法

`keyboardModifiers()` 和 `mouseButtons()` 返回 Qt 已处理事件所维护的状态，适合事件处理期间使用。`queryKeyboardModifiers()` 直接向输入设备查询当前修饰键，窗口移动等没有收到按键事件的场景可使用，但多数情况下前者更快，也更符合当前事件发生时的状态。

应用覆盖光标使用栈语义：

```cpp
QGuiApplication::setOverrideCursor(Qt::WaitCursor);
performOperation();
QGuiApplication::restoreOverrideCursor();
```

每次 `setOverrideCursor()` 都必须与一次 `restoreOverrideCursor()` 配对。嵌套调用会逐层压栈；`changeOverrideCursor()` 只替换栈顶，没有覆盖光标时不起作用。生产代码通常用局部 RAII 守卫保证异常或提前返回时也能恢复。

`clipboard()` 和 `inputMethod()` 返回应用管理的单例式对象，调用方不拥有它们。剪贴板在部分平台上采用延迟或事件驱动的数据交换，不能脱离 GUI 事件循环假定数据永远同步可用。

## 应用状态与后台行为

`applicationState()` 反映应用处于 active、inactive、hidden 或 suspended 等状态。连接 `applicationStateChanged()` 后，可在进入后台时暂停动画、降低刷新率、保存进度，在恢复前台时重新加载资源。

状态含义和切换时机由平台决定。它不是安全认证或用户在线状态，也不保证暂停后一定有充分时间执行长任务。

## 会话管理

桌面会话管理器可要求应用提交数据或保存可恢复状态：

- `commitDataRequest(QSessionManager &)`：保存未提交数据，必要时请求许可后与用户交互；
- `saveStateRequest(QSessionManager &)`：保存用于下次会话恢复的状态；
- `isSessionRestored()`：本次启动是否来自旧会话恢复；
- `sessionId()`、`sessionKey()`：标识会话；
- `isSavingSession()`：当前是否处于会话保存阶段。

连接 `commitDataRequest()` 时应使用 `Qt::DirectConnection`。信号处理期间默认不能与用户交互，除非通过 `QSessionManager` 明确取得许可，也不应在该信号内自行退出程序。会话管理能力受平台支持和编译配置限制。

## 原生接口边界

`nativeInterface<T>()` 是访问受支持平台接口的类型化入口，例如 X11 或 Wayland 应用接口；不可用时返回 `nullptr`。使用前必须按平台和 Qt 配置条件编译，并处理接口缺失。

`platformNativeInterface()` 和 `platformFunction()` 更接近 QPA 实现细节，会降低源码与二进制可移植性。业务代码优先使用 Qt 的跨平台 API，只有集成系统级能力且确实没有 Qt 抽象时才进入这一层。

`sync()` 会处理 Qt 事件、同步窗口系统，再次处理事件，开销较大且可能引发重入，官方不建议在常规流程中使用。

## 常见错误

- 同时创建 `QCoreApplication` 和 `QGuiApplication`，或在同一进程创建多个应用对象。
- Widgets 程序使用 `QGuiApplication`，随后创建 `QWidget`。
- 在应用对象之前创建 `QPixmap`、窗口或其他 GUI 资源。
- 让自制的 `argc`、`argv` 缓冲区在应用对象之前失效。
- 从工作线程直接操作窗口、剪贴板、输入法或屏幕对象。
- 长期缓存 `QScreen *`，却不处理屏幕移除。
- 每次显示忙碌光标都压栈，却漏掉对应的恢复调用。
- 在目标窗口明确时使用全局最高 `devicePixelRatio()`，造成过度缩放。
- 在应用对象构造后才设置桌面设置感知或高 DPI 舍入策略。
- 依赖 `lastWindowClosed()` 一定终止进程。
- 频繁调用 `sync()` 试图“强制刷新界面”；重绘应使用正常事件和更新机制。

## API 速查表

| 类别 | API | 语义与边界 |
| --- | --- | --- |
| 宏 | `qGuiApp` / `qApp` | 指向唯一 `QGuiApplication` 实例；构造前或析构后不可使用。 |
| 构造 | `QGuiApplication(int &argc, char **argv)` | 初始化 GUI 与窗口系统；参数内存须全生命周期有效，Qt 可能修改参数内容。 |
| 析构 | `~QGuiApplication()` | 结束 GUI 应用运行时；应晚于其他 GUI 对象析构。 |
| 事件循环 | `static int exec()` | 启动主事件循环并返回退出码；部分平台不保证返回到 `main()`。 |
| 事件分发 | `bool notify(QObject *receiver, QEvent *event) override` | 向接收者分发事件；重写会影响全局事件路径，必须保留异常与基类契约。 |
| 事件扩展 | `bool event(QEvent *event) override` | 处理应用对象自身事件；未处理事件交给基类。 |
| 事件扩展 | `compressEvent(...) override` | Qt 6.10 起弃用、Qt 7 移除；不要基于它新增事件压缩逻辑。 |
| 名称 | `static setApplicationDisplayName(const QString &name)` | 设置面向用户的可翻译名称。 |
| 名称 | `static applicationDisplayName()` | 返回显示名；未设置时退回应用名。 |
| 名称 | `applicationDisplayNameChanged()` | 显示名变化信号。 |
| 桌面集成 | `static setDesktopFileName(const QString &name)` | 设置桌面条目基本名，不含路径和 `.desktop`。 |
| 桌面集成 | `static desktopFileName()` | 返回桌面条目基本名。 |
| 徽标 | `setBadgeNumber(qint64 number)` | Qt 6.5 起。设置 Dock、任务栏等处的数字徽标；0 清除，范围和显示受平台限制。 |
| 窗口 | `static allWindows()` | 返回全部应用窗口；列表和对象会动态变化。 |
| 窗口 | `static topLevelWindows()` | 只返回顶层窗口。 |
| 窗口 | `static topLevelAt(const QPoint &pos)` | 按全局屏幕坐标查找顶层窗口；可能返回 `nullptr`。 |
| 窗口 | `static modalWindow()` | 返回当前模态窗口；没有时为 `nullptr`。 |
| 窗口 | `static focusWindow()` | 返回当前焦点窗口；应用未激活时可能为空。 |
| 焦点 | `static focusObject()` | 返回焦点事件最终接收对象；可能为空且未必是窗口。 |
| 焦点 | `focusWindowChanged(QWindow *window)` | 焦点窗口改变信号，新值可为 `nullptr`。 |
| 焦点 | `focusObjectChanged(QObject *object)` | 最终焦点接收对象改变信号，新值可为 `nullptr`。 |
| 退出 | `static setQuitOnLastWindowClosed(bool quit)` | 控制最后一个可见主要窗口关闭时是否尝试退出。 |
| 退出 | `static quitOnLastWindowClosed()` | 返回该策略，默认 `true`。 |
| 退出 | `lastWindowClosed()` | 最后一个可见主要窗口关闭时发出；发出不保证进程已退出。 |
| 图标 | `static setWindowIcon(const QIcon &icon)` | 设置应用级默认窗口图标。 |
| 图标 | `static windowIcon()` | 返回应用级默认窗口图标。 |
| 平台 | `static platformName()` | 返回 QPA 插件名；应用构造前查询不反映 `-platform` 或环境变量的最终选择。 |
| 屏幕 | `static primaryScreen()` | 返回主屏幕，所有权属于 Qt；可能随系统变化。 |
| 屏幕 | `static screens()` | 返回当前屏幕列表，不是永久快照。 |
| 屏幕 | `static screenAt(const QPoint &point)` | 按虚拟桌面坐标查找屏幕；点不在任何屏幕时可为空。 |
| 屏幕 | `screenAdded(QScreen *screen)` | 新屏幕加入信号。 |
| 屏幕 | `screenRemoved(QScreen *screen)` | 屏幕移除信号，可在 Qt 回退迁移窗口前处理。 |
| 屏幕 | `primaryScreenChanged(QScreen *screen)` | 主屏幕改变信号。 |
| DPI | `devicePixelRatio() const` | 返回系统最高 DPR；已知目标窗口时改用窗口自己的 DPR。 |
| DPI | `static setHighDpiScaleFactorRoundingPolicy(policy)` | 设置非整数缩放舍入策略；必须在构造应用对象前调用。 |
| DPI | `static highDpiScaleFactorRoundingPolicy()` | 返回当前舍入策略，默认 `PassThrough`，也可能受环境影响。 |
| 光标 | `static setOverrideCursor(const QCursor &cursor)` | 向全局覆盖光标栈压入一项。 |
| 光标 | `static changeOverrideCursor(const QCursor &cursor)` | 替换栈顶覆盖光标；栈空时无效果。 |
| 光标 | `static restoreOverrideCursor()` | 弹出一项；必须与每次 `setOverrideCursor()` 配对。 |
| 光标 | `static overrideCursor()` | 返回当前栈顶指针；没有覆盖光标时为 `nullptr`，不由调用方删除。 |
| 字体 | `static font()` | 返回应用默认字体。 |
| 字体 | `static setFont(const QFont &font)` | 修改应用默认字体。 |
| 字体 | `fontDatabaseChanged()` | 应用字体增删或系统字体变化时发出。 |
| 剪贴板 | `static clipboard()` | 返回应用管理的 `QClipboard *`；需要 GUI 应用和平台支持。 |
| 调色板 | `static palette()` | 返回应用调色板。 |
| 调色板 | `static setPalette(const QPalette &palette)` | 设置应用调色板，颜色角色仍会与平台主题组合。 |
| 调色板 | `paletteChanged(const QPalette &)` | Qt 6.0 已弃用；处理 `QEvent::ApplicationPaletteChange`。 |
| 输入 | `static keyboardModifiers()` | 返回事件队列维护的修饰键状态，适合当前事件语境。 |
| 输入 | `static queryKeyboardModifiers()` | 查询设备此刻的实际修饰键状态；通常不如事件状态合适。 |
| 输入 | `static mouseButtons()` | 返回事件队列维护的鼠标按键状态。 |
| 输入法 | `static inputMethod()` | 返回应用管理的 `QInputMethod *`，不转移所有权。 |
| 布局方向 | `static setLayoutDirection(Qt::LayoutDirection direction)` | 设置全局默认布局方向；`Auto` 随应用语言决定。 |
| 布局方向 | `static layoutDirection()` | 返回全局默认布局方向。 |
| 布局方向 | `static isRightToLeft()` | 是否为 RTL。 |
| 布局方向 | `static isLeftToRight()` | 是否为 LTR。 |
| 布局方向 | `layoutDirectionChanged(Qt::LayoutDirection direction)` | 默认布局方向改变信号。 |
| 桌面设置 | `static setDesktopSettingsAware(bool on)` | 设置是否采用系统字体、颜色等；必须在构造应用对象前调用。 |
| 桌面设置 | `static desktopSettingsAware()` | 返回该策略，默认 `true`。 |
| 平台提示 | `static styleHints()` | 返回平台风格提示对象，如双击间隔；应用所有，不可删除。 |
| 应用状态 | `static applicationState()` | 返回当前前台、后台、隐藏或挂起状态。 |
| 应用状态 | `applicationStateChanged(Qt::ApplicationState state)` | 应用状态改变信号。 |
| 会话 | `isSessionRestored() const` | 是否由早先桌面会话恢复。 |
| 会话 | `sessionId() const` | 返回会话标识。 |
| 会话 | `sessionKey() const` | 返回当前会话键。 |
| 会话 | `isSavingSession() const` | 是否处于会话保存及其后续关闭阶段。 |
| 会话 | `commitDataRequest(QSessionManager &manager)` | 提交未保存数据请求；使用直接连接，交互需先获许可，不要在处理器内退出。 |
| 会话 | `saveStateRequest(QSessionManager &manager)` | 保存下次恢复所需状态的请求。 |
| 原生接口 | `nativeInterface<T>()` | 返回受支持的类型化平台接口；不可用时为 `nullptr`。 |
| 原生接口 | `static platformNativeInterface()` | 旧式 QPA 原生接口入口，可移植性和兼容性较弱。 |
| 原生接口 | `static platformFunction(const QByteArray &name)` | 查询平台函数指针；必须验证空指针和 ABI 契约。 |
| 同步 | `static sync()` | 清空事件、同步窗口系统再处理事件；耗时且可能重入，不建议常规调用。 |
| 信号 | `fontChanged(const QFont &)` | Qt 6.0 已弃用；处理 `QEvent::ApplicationFontChange`。 |

## 相关类

- `QCoreApplication`：非 GUI 的事件循环与进程级服务基类。
- `QApplication`：Widgets 应用必须使用的派生类。
- `QWindow`、`QScreen`：窗口与显示器资源。
- `QClipboard`、`QInputMethod`、`QStyleHints`：应用管理的全局 GUI 服务。
- `QSessionManager`：桌面会话提交和恢复。

`QGuiApplication` 的关键不是“有哪些全局 getter”，而是它定义了 GUI 进程从平台初始化、事件循环到退出清理的完整边界。
