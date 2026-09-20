# QApplication

> Qt 6.11.1 · Qt Widgets · 来自 `QApplication`

## 1. 先建立直觉

**一句话定位：** `QApplication` 是所有 Qt Widgets 程序的应用级入口，负责初始化 GUI 平台、Widgets 样式系统、全局输入状态、窗口集合和主事件循环。

### 这是什么

`QApplication` 继承自 `QGuiApplication`，但它不是“多一个名字”的入口类。它额外初始化了 QWidget 体系需要的内容：`QStyle`、Widgets 调色板/字体传播、焦点控件、弹出控件、顶层控件集合、控件样式表、拖拽阈值、双击间隔等桌面交互参数。

只要程序里出现 `QWidget`、`QMainWindow`、`QDialog`、`QPushButton`、`QTableView` 这类 Widgets 对象，入口就应该是 `QApplication`，而不是 `QGuiApplication`。

### 适合使用的场景

- 传统桌面应用：主窗口、菜单栏、工具栏、对话框、表格、树、表单。
- 需要 `QStyle`、应用级样式表、Widgets 调色板和字体策略。
- 需要查询当前焦点控件、活动窗口、活动模态窗口、弹出窗口。
- 需要统一处理拖拽启动距离、双击间隔、滚轮行数等桌面交互习惯。

### 不适合的场景

- 纯控制台或服务：用 `QCoreApplication`。
- 纯 Qt Quick/QML 且不创建 QWidget：通常用 `QGuiApplication`。
- 想用它保存业务状态：应用对象应只做应用级环境和事件循环，业务状态放在自己的 model/service/controller 中。

### 最小示例

```cpp
#include <QApplication>
#include <QMainWindow>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    QMainWindow window;
    window.resize(960, 640);
    window.show();

    return QApplication::exec();
}
```

**先记住的坑：** 所有 QWidget 都必须在 `QApplication` 创建之后使用；GUI 操作应在 GUI 线程；应用级样式表会影响整个 Widgets 树，方便但也容易造成性能和样式排查困难；不要在 GUI 线程里执行长循环或同步等待。

## 2. 依赖与对象关系

- 头文件：`#include <QApplication>`
- CMake：`find_package(Qt6 REQUIRED COMPONENTS Widgets)`，并链接 `Qt6::Widgets`
- 继承自：`QGuiApplication`
- 常用全局宏：`qApp`

### 生命周期

`QApplication` 通常是 `main()` 中最早创建、最后销毁的栈对象。它析构后 QWidget、样式对象、剪贴板、输入法和窗口系统资源都不应继续使用。顶层窗口可以放在栈上，也可以由对象树或智能指针管理；普通子控件通常交给 parent 销毁。

### 事件循环

`exec()` 启动主事件循环，鼠标、键盘、绘制、定时器、网络回调、queued signal 都靠事件循环推进。长耗时任务应放到工作线程或异步 API，完成后通过信号回到 GUI 线程更新控件。

### 与 QGuiApplication 的区别

`QGuiApplication` 只管理 GUI 基础能力；`QApplication` 还管理 Widgets 层的样式、控件集合、焦点控件和桌面交互参数。用 Widgets 时不要为了“更轻量”选择 `QGuiApplication`，否则创建 QWidget 会失败或行为不完整。

## 3. API 速查

| API | 用途速查 |
|---|---|
| `autoSipEnabled : bool` | 控制输入控件获得焦点时是否自动显示软件输入面板。 |
| `cursorFlashTime : int` | 文本插入光标闪烁周期，遵循或覆盖系统设置。 |
| `doubleClickInterval : int` | 区分双击与两次单击的最大时间间隔。 |
| `keyboardInputInterval : int` | 区分连续按键输入的时间阈值。 |
| `startDragDistance : int` | 鼠标按下后移动多少像素才认为开始拖拽。 |
| `startDragTime : int` | 鼠标按住多久后可认为开始拖拽。 |
| `styleSheet : QString` | 应用级 Qt Style Sheet，影响整个 Widgets 树。 |
| `wheelScrollLines : int` | 单次滚轮滚动建议滚动的文本行数。 |
| `QApplication(int &argc, char **argv)` | 初始化 Widgets 应用对象和 GUI 平台。 |
| `~QApplication()` | 释放 Widgets 和 GUI 平台资源。 |
| `notify()` / `event()` | 全局事件分发和应用对象事件处理钩子。 |
| `aboutQt()` | 显示 Qt 内置关于对话框。 |
| `closeAllWindows()` | 尝试关闭所有顶层窗口。 |
| `focusChanged()` | 当前焦点 QWidget 改变时发出。 |
| `activeWindow()` / `focusWidget()` | 查询当前活动窗口或焦点控件。 |
| `activeModalWidget()` / `activePopupWidget()` | 查询当前模态控件或弹出控件。 |
| `allWidgets()` / `topLevelWidgets()` | 枚举当前应用中的 QWidget。 |
| `alert()` / `beep()` | 请求平台吸引用户注意或播放提示音。 |
| `font()` / `setFont()` | 读取或设置 Widgets 默认字体，可按类名限定。 |
| `palette()` / `setPalette()` | 读取或设置 Widgets 默认调色板，可按类名限定。 |
| `style()` / `setStyle()` | 读取或更换当前 `QStyle`。 |
| `setStyleSheet()` | 设置全局样式表，适合少量统一规则，不适合替代完整样式系统。 |
| `widgetAt()` / `topLevelAt()` | 按全局坐标查找命中的控件或顶层控件。 |
| `isEffectEnabled()` / `setEffectEnabled()` | 查询或设置 UI 动效开关。 |
| `navigationMode()` / `setNavigationMode()` | 查询或设置键盘/方向键导航模式。 |
| `qApp` | 当前 `QApplication` 的便捷宏。 |

## 4. 重点 API 说明

### `autoSipEnabled : bool`

控制软件输入面板是否在输入控件获得焦点时自动出现。它主要影响触屏、移动设备或没有实体键盘的平台，并且只对启用了输入法属性的控件有意义。桌面平台上它可能没有可见效果；不要把它当作强制弹出软键盘的跨平台保证。

### `cursorFlashTime : int`

设置文本插入光标闪烁时间，单位毫秒。文本编辑控件会用它决定光标显示/隐藏节奏。系统可能提供默认值；Windows 上设置它可能影响系统级行为。控件不应长期缓存这个值，因为用户可以在系统设置里修改。

### `doubleClickInterval : int`

设置两次鼠标点击被识别为双击的最大间隔。自定义鼠标交互、图形编辑器、文件列表重命名逻辑会参考它。不要硬编码 250ms/400ms 之类常量，遵循平台习惯能让应用更自然。

### `keyboardInputInterval : int`

设置连续按键输入的时间阈值。它用于区分单独按键和一组连续输入，对自定义键盘导航、快捷键序列判断有参考价值。普通控件通常不需要直接改它。

### `startDragDistance : int`

设置拖拽开始所需的最小移动距离。实现自定义拖放时，先记录鼠标按下位置，再用当前位置的曼哈顿距离和此值比较。它能避免用户轻微手抖就触发拖拽。

### `startDragTime : int`

设置拖拽开始前的最短按住时间。它常与 `startDragDistance()` 一起使用：距离足够且按住时间满足时才启动拖放。不同平台习惯不同，优先使用系统值。

### `styleSheet : QString`

应用级样式表，语法是 Qt Style Sheets。适合统一小范围视觉规则，比如按钮颜色、输入框边框。它会影响整个 Widgets 树，复杂规则可能让样式排查和绘制性能变差；大型应用更适合用局部样式表、自定义 `QStyle` 或设计系统封装。

### `wheelScrollLines : int`

单次滚轮事件建议滚动的文本行数。文本编辑器、列表和自定义滚动控件可参考它。触控板像素滚动和高精度滚轮可能不完全按“行”表达，处理滚动事件时还要看事件提供的 pixel delta。

### `QApplication::QApplication(int &argc, char **argv)`

创建 Widgets 应用对象，初始化 GUI 平台、Widgets 样式系统并解析 Qt 命令行参数。它必须早于任何 QWidget 创建。`argc`/`argv` 数据必须在应用对象生命周期内有效，Qt 可能移除自己识别的参数。

### `[virtual noexcept] QApplication::~QApplication()`

释放应用级 Widgets/GUI 资源。通常由 `main()` 中的栈对象自然析构。不要在析构后访问任何 QWidget、样式对象或应用级 GUI 服务。

### `bool QApplication::autoSipEnabled() const`

读取自动软件输入面板策略。它只是查询当前应用设置，不会主动显示或隐藏键盘。需要实际控制输入面板时，还要结合输入法相关 API 和平台能力。

### `QString QApplication::styleSheet() const`

返回应用级样式表文本。适合调试当前全局样式规则或在动态追加规则前读取原值。不要用它反推出所有控件最终视觉效果，因为 `QStyle`、控件属性、局部样式表和平台主题都会参与最终绘制。

### `[override virtual] bool QApplication::notify(QObject *receiver, QEvent *e)`

全局事件分发入口，把事件送到目标对象。只有框架层、监控层或需要统一异常边界时才重写。重写时通常要调用基类；吞掉未知事件会导致快捷键、焦点、输入法或绘制异常。

### `[slot] void QApplication::aboutQt()`

显示 Qt 内置关于对话框。适合菜单里的“About Qt”。商业产品通常还会提供自己的关于对话框，两者用途不同。

### `[slot] void QApplication::closeAllWindows()`

尝试关闭所有顶层窗口。每个窗口仍会收到关闭事件，窗口可以拒绝关闭。适合“退出应用”前的统一关闭流程，但真正是否退出要看窗口关闭结果和 `quitOnLastWindowClosed` 策略。

### `[slot] void QApplication::setAutoSipEnabled(const bool enabled)`

设置自动软件输入面板策略。触屏设备或嵌入式界面更常用；桌面平台可能忽略。它不会改变控件是否接受输入法，控件仍需要相关属性支持。

### `[slot] void QApplication::setStyleSheet(const QString &sheet)`

设置应用级样式表。适合启动时统一加载少量样式，也可用于主题切换。注意它会触发大量控件重新 polish/repaint，运行中频繁整表替换会影响性能。

### `[signal] void QApplication::focusChanged(QWidget *old, QWidget *now)`

当前焦点控件变化时发出。表单校验、状态栏提示、输入法上下文、快捷键上下文可连接它。`old` 或 `now` 都可能为空；不要假定焦点变化一定来自鼠标或键盘。

### `[static] QWidget *QApplication::activeModalWidget()`

返回当前活动的模态 QWidget。适合定位对话框层级、诊断为什么其他窗口无法输入。没有模态控件时返回 `nullptr`。

### `[static] QWidget *QApplication::activePopupWidget()`

返回当前活动的弹出控件，例如菜单、下拉框弹层。自定义输入处理或调试焦点/鼠标捕获时有用。普通业务代码不应绕过弹出控件直接操作底层窗口。

### `[static] QWidget *QApplication::activeWindow()`

返回当前活动顶层窗口。适合把新对话框挂到当前窗口、同步全局动作状态。没有活动窗口时返回 `nullptr`。

### `[static] void QApplication::alert(QWidget *widget, int msec = 0)`

请求平台让某个窗口吸引用户注意，例如任务栏闪烁、Dock 弹跳。适合后台任务完成、需要用户确认但窗口不在前台时使用。不同平台表现不同，`msec` 也不一定被严格遵守。

### `[static] QWidgetList QApplication::allWidgets()`

返回应用中所有 QWidget 的列表。调试泄漏、自动化测试、诊断对象树时有用。不要在生产逻辑里频繁遍历所有控件来驱动业务状态。

### `[static] void QApplication::beep()`

请求平台播放默认提示音。适合轻量错误提示或无法显示对话框时提醒用户。是否有声音、声音类型和音量由系统决定。

### `[static] int QApplication::cursorFlashTime()`

返回文本光标闪烁时间。自定义文本编辑控件可用它保持与系统一致。返回值可能表示禁用闪烁，处理时不要只假设正数。

### `[static] int QApplication::doubleClickInterval()`

返回双击时间阈值。自定义鼠标双击识别应使用它，而不是固定常量。

### `[static] int QApplication::exec()`

进入 Widgets 主事件循环。通常在显示主窗口后调用，并把返回值作为进程退出码。不要在进入事件循环前启动依赖 GUI 事件的异步流程却不显示或不保持对象生命周期。

### `[static] QWidget *QApplication::focusWidget()`

返回当前拥有键盘焦点的 QWidget。表单工具、快捷键路由、状态提示可用它。没有焦点控件时返回 `nullptr`。

### `[static] QFont QApplication::font()`

返回应用默认字体。适合初始化自定义绘制控件。应用字体、平台字体和控件局部字体存在层级关系，最终字体要看控件自己的 `font()`。

### `[static] QFont QApplication::font(const QWidget *widget)`

返回指定控件实际应使用的字体。它会考虑控件类、父子继承和应用默认值。自定义绘制某个控件内部元素时比全局 `font()` 更准确。

### `[static] QFont QApplication::font(const char *className)`

返回某类控件的默认字体。适合为自定义控件模拟某个内置控件的字体策略。类名必须与 Qt 样式/字体数据库可识别的类名匹配。

### `[static] bool QApplication::isEffectEnabled(Qt::UIEffect effect)`

查询某类 UI 动效是否启用，例如菜单淡入、工具提示动画。尊重它可以让应用跟随用户的无障碍或性能偏好。

### `[static] int QApplication::keyboardInputInterval()`

返回键盘输入间隔阈值。自定义按键序列或重复输入逻辑可参考它。

### `[static] Qt::NavigationMode QApplication::navigationMode()`

返回当前导航模式。某些嵌入式、电视或键盘导航界面会依赖它决定焦点移动方式。桌面应用通常较少直接修改。

### `[static] QPalette QApplication::palette(const QWidget *widget)`

返回指定控件适用的调色板。自绘控件应优先用控件自身 palette 或此接口，而不是直接硬编码颜色。

### `[static] QPalette QApplication::palette(const char *className)`

返回指定控件类名的默认调色板。用于按类模拟内置控件色彩。类名不匹配时可能退回应用默认调色板。

### `[static] void QApplication::setCursorFlashTime(int)`

设置文本光标闪烁时间。除非应用有明确的编辑体验要求，否则最好尊重系统设置。过小会造成视觉干扰，负值可能表示禁用闪烁。

### `[static] void QApplication::setDoubleClickInterval(int)`

设置双击识别间隔。通常不建议应用私自覆盖用户系统偏好；更常见是自定义控件读取这个值。

### `[static] void QApplication::setEffectEnabled(Qt::UIEffect effect, bool enable = true)`

启用或禁用指定 UI 动效。可用于低性能设备、远程桌面或无障碍场景。关闭动效不应影响功能本身。

### `[static] void QApplication::setFont(const QFont &font, const char *className = nullptr)`

设置应用默认字体，或指定类名控件的默认字体。适合品牌字体、嵌入式固定字体方案。运行中修改可能导致大量控件重新布局；局部字体优先级可能覆盖它。

### `[static] void QApplication::setKeyboardInputInterval(int)`

设置键盘输入间隔阈值。普通桌面应用很少需要改，除非实现特殊输入设备或 kiosk 场景。

### `[static] void QApplication::setNavigationMode(Qt::NavigationMode mode)`

设置导航模式。适用于方向键、焦点框、无鼠标设备主导的界面。常规鼠标键盘桌面应用通常使用平台默认。

### `[static] void QApplication::setPalette(const QPalette &palette, const char *className = nullptr)`

设置应用默认调色板，或按类名设置某类控件调色板。适合统一色彩基线，但它不是完整主题引擎；样式表、平台样式和控件自绘仍可能覆盖颜色。

### `[static] void QApplication::setStartDragDistance(int l)`

设置拖拽启动距离。自定义拖放体验非常特殊时才改；普通应用应读取系统值，保持平台一致。

### `[static] void QApplication::setStartDragTime(int ms)`

设置拖拽启动时间。改动会影响应用内拖拽手感；设置过短会误触，过长会显得迟钝。

### `[static] void QApplication::setStyle(QStyle *style)`

安装一个 `QStyle` 对象作为应用样式。适合自定义控件绘制策略或统一平台外观。传入样式对象后生命周期由 QApplication 管理；不要再手动删除。

### `[static] QStyle *QApplication::setStyle(const QString &style)`

按样式名称创建并安装样式，例如平台可用的 `Fusion`。返回安装后的样式，失败可能返回 `nullptr`。部署时要确认目标平台有对应样式插件。

### `[static] void QApplication::setWheelScrollLines(int)`

设置滚轮每次滚动建议行数。自定义滚动控件可读取这个值。触控板高精度滚动不一定用行数表达。

### `[static] int QApplication::startDragDistance()`

返回拖拽启动距离。自定义拖放最常用它判断是否从点击转为拖拽。

### `[static] int QApplication::startDragTime()`

返回拖拽启动时间。与距离阈值配合使用，可减少误触发。

### `[static] QStyle *QApplication::style()`

返回当前应用样式对象。自定义绘制、查询像素指标、获取标准图标时常用。返回对象由 QApplication 管理，不要删除。

### `[static] QWidget *QApplication::topLevelAt(const QPoint &point)`

返回全局坐标下的顶层 QWidget。适合调试窗口命中、实现应用内拾取工具。只返回当前应用的窗口。

### `[static] QWidget *QApplication::topLevelAt(int x, int y)`

坐标拆成 `x`、`y` 的重载，语义与 `topLevelAt(QPoint)` 相同。避免在调用点临时构造 `QPoint` 时可读性更高。

### `[static] QWidgetList QApplication::topLevelWidgets()`

返回所有顶层 QWidget。用于统一保存窗口状态、关闭窗口、查找主窗口。隐藏窗口也可能在列表中。

### `[static] int QApplication::wheelScrollLines()`

返回滚轮建议滚动行数。文本、列表、表格控件可用它保持系统一致性。

### `[static] QWidget *QApplication::widgetAt(const QPoint &point)`

返回全局坐标下最具体的 QWidget。适合调试命中测试、上下文帮助、自定义检查工具。透明区域、原生子窗口和平台窗口可能影响结果。

### `[static] QWidget *QApplication::widgetAt(int x, int y)`

坐标拆成 `x`、`y` 的重载，语义与 `widgetAt(QPoint)` 相同。

### `[override virtual protected] bool QApplication::event(QEvent *e)`

处理发给应用对象自身的事件。派生 QApplication 捕获应用级事件时才重写。不处理的事件应交给基类。

### `qApp`

当前应用对象的全局便捷宏，在 Widgets 程序中通常可视为 `QApplication *`。它方便但会隐藏依赖；库代码和可测试代码更适合显式传入需要的对象。

## 5. 深入实践与常见坑

### QApplication 必须比 QWidget 更早

`QWidget` 依赖 QApplication 初始化的样式、字体、平台窗口资源和事件系统。不要在全局静态对象里创建 QWidget，也不要在 `main()` 创建 QApplication 前创建任何控件。

### 样式、调色板、样式表不是同一层

`QStyle` 决定控件如何绘制和计算尺寸；`QPalette` 提供颜色角色；Style Sheet 会覆盖部分样式行为。三者混用时，最终效果不容易从单一 API 推断。大型项目最好约定一套统一策略。

### 全局样式表慎用

`setStyleSheet()` 很方便，但全局选择器会影响所有子控件。复杂选择器可能让控件 polish、重绘和排查变慢。更稳的做法是给特定控件或局部容器设置样式表。

### 焦点和模态

`focusWidget()`、`activeWindow()`、`activeModalWidget()` 回答的是不同问题：键盘输入目标、活动顶层窗口、阻塞其他窗口的模态控件。处理快捷键和对话框时要区分这三者。

### 遵守平台交互参数

拖拽距离、双击间隔、滚轮行数、光标闪烁都来自用户习惯和系统设置。自定义控件优先读取 QApplication 的值，而不是写死。
