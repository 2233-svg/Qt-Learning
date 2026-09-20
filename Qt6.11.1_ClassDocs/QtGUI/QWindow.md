# QWindow

> Qt 6.11.1 · Qt GUI · 来自 `QWindow`

## 1. 先建立直觉

**一句话定位：** `QWindow` 是 Qt GUI 层的底层窗口对象，直接面对平台窗口系统，负责窗口表面、屏幕归属、可见性、几何、输入事件和原生窗口句柄。

### 这是什么

`QWindow` 不是 QWidget。它没有布局、子控件绘制、样式表和 `QStyle`；它是更靠近平台窗口系统的一层。Qt Quick 的 `QQuickWindow`、Vulkan 窗口、低层 OpenGL/RHI 窗口、自定义渲染窗口都建立在这条线上。

可以把 `QWindow` 理解成“平台窗口和渲染表面的 C++ 包装”。它知道自己在哪块屏幕、窗口边框在哪里、客户区多大、是否暴露、是否激活、何时收到鼠标键盘触摸事件，但它不会替你排布按钮或画控件。

### 适合使用的场景

- Qt Quick、自绘渲染、OpenGL/Vulkan/RHI、视频输出等需要直接窗口表面的场景。
- 需要操作平台窗口状态：全屏、最大化、最小化、模态、临时父窗口、系统移动/缩放。
- 需要精确处理屏幕、DPI、safe area、frame geometry 和窗口客户区坐标。
- 需要从原生窗口 ID 包装窗口，或把 Qt 窗口嵌入更底层的系统窗口集成。

### 不适合的场景

- 普通桌面表单、按钮、菜单、表格界面：使用 QWidget/QMainWindow。
- 想用布局系统自动排版：`QWindow` 没有 QWidget 布局能力。
- 想在 `paintEvent()` 里用 `QPainter` 直接画窗口：通常应使用 `QPaintDeviceWindow`、`QRasterWindow`、`QOpenGLWindow` 或 Qt Quick。

### 典型调用链

```cpp
#include <QGuiApplication>
#include <QWindow>

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);

    QWindow window;
    window.setTitle(QStringLiteral("Raw window"));
    window.resize(960, 540);
    window.show();

    return QGuiApplication::exec();
}
```

**先记住的坑：** `QWindow` 的 `geometry()` 是客户区，`frameGeometry()` 才包含平台窗口边框；窗口可见不等于可以渲染，渲染前常要看 `isExposed()`；很多状态改变是对窗口系统的请求，不是同步保证；`winId()` 会创建原生资源，别把它当成无成本查询。

## 2. 依赖与对象关系

- 头文件：`#include <QWindow>`
- CMake：`find_package(Qt6 REQUIRED COMPONENTS Gui)`，并链接 `Qt6::Gui`
- 继承自：`QObject`、`QSurface`
- 常见派生类：`QPaintDeviceWindow`、`QQuickWindow`、`QVulkanWindow`

### 生命周期和平台资源

`QWindow` 对象本身是 QObject；真正的平台窗口资源可能延迟到 `create()`、`show()` 或某些需要原生句柄的调用时创建。`destroy()` 销毁平台资源，但 C++ 对象仍存在；析构会释放相关资源。需要精确控制原生窗口生命周期时，才直接调用 `create()`/`destroy()`。

### 屏幕、几何和坐标

`position()`、`geometry()`、`size()` 描述客户区；`framePosition()`、`frameGeometry()`、`frameMargins()` 包含标题栏和边框。多屏和高 DPI 下，坐标是 Qt 的设备无关坐标；渲染资源大小还要结合 `devicePixelRatio()`。

### 事件和渲染

`QWindow` 通过虚函数接收事件：expose、resize、mouse、key、touch、wheel、native 等。低层渲染通常在暴露后、尺寸有效时进行。`requestUpdate()` 用于请求一次更新事件，适合动画或按需渲染循环。

## 3. API 速查

| API | 用途速查 |
|---|---|
| `enum AncestorMode` | 查询父子/临时父窗口关系时是否把 transient parent 算入祖先链。 |
| `enum Visibility` | 描述窗口可见状态：普通、最小化、最大化、全屏、自动、隐藏。 |
| `active` / `isActive()` / `activeChanged()` | 判断窗口是否为活动窗口。 |
| `contentOrientation` / `reportContentOrientationChange()` | 描述内容方向，用于移动设备和旋转场景。 |
| `flags` / `setFlags()` / `setFlag()` / `type()` | 配置窗口类型、装饰、工具窗口等窗口系统标志。 |
| `x` `y` `width` `height` / `position()` / `size()` | 查询客户区位置和尺寸。 |
| `geometry()` / `setGeometry()` | 一次设置或查询客户区矩形。 |
| `frameGeometry()` / `framePosition()` / `frameMargins()` | 查询或设置包含窗口装饰的外框几何。 |
| `minimumSize()` / `maximumSize()` / 相关宽高属性 | 限制用户和窗口系统可调整的尺寸范围。 |
| `baseSize()` / `sizeIncrement()` | 给窗口管理器提供尺寸递增提示，主要用于终端等网格化窗口。 |
| `modality` / `setModality()` / `isModal()` | 设置窗口模态策略。 |
| `opacity` / `setOpacity()` | 设置窗口整体透明度。 |
| `title` / `setTitle()` / `windowTitleChanged()` | 设置标题栏文本。 |
| `visible` / `visibility` / `show*()` / `hide()` | 控制窗口显示、隐藏、全屏、最大化、最小化。 |
| `transientParent` / `setTransientParent()` | 设置临时父窗口，例如对话框属于哪个主窗口。 |
| `screen()` / `setScreen()` / `screenChanged()` | 查询或移动窗口到指定屏幕。 |
| `safeAreaMargins()` | 获取刘海屏、圆角屏等不可安全使用区域边距。 |
| `devicePixelRatio()` | 把设备无关尺寸换算到实际渲染像素时使用。 |
| `create()` / `destroy()` | 显式创建或销毁底层平台窗口资源。 |
| `winId()` / `fromWinId()` | 取得或包装原生窗口 ID。 |
| `setFormat()` / `format()` / `requestedFormat()` | 配置和查询窗口表面格式。 |
| `setSurfaceType()` / `surfaceType()` | 指定窗口表面类型，例如 Raster/OpenGL/Vulkan。 |
| `setVulkanInstance()` / `vulkanInstance()` | 绑定 Vulkan 实例。 |
| `mapToGlobal()` / `mapFromGlobal()` | 在窗口坐标和全局屏幕坐标之间转换。 |
| `cursor()` / `setCursor()` / `unsetCursor()` | 设置窗口内光标。 |
| `setMouseGrabEnabled()` / `setKeyboardGrabEnabled()` | 请求独占鼠标或键盘输入。 |
| `setMask()` / `mask()` | 设置窗口输入/可见区域遮罩。 |
| `alert()` | 请求平台提示用户注意该窗口。 |
| `close()` / `closeEvent()` | 请求关闭窗口，并允许事件处理器接受或拒绝。 |
| `requestActivate()` | 请求窗口获得焦点和激活状态。 |
| `requestUpdate()` | 请求一次更新事件，适合渲染循环。 |
| `raise()` / `lower()` | 请求调整窗口堆叠顺序。 |
| `startSystemMove()` / `startSystemResize()` | 交给窗口管理器执行系统级移动或缩放。 |
| `event()` 及各类 `*Event()` | 自定义处理平台事件、输入事件、暴露和尺寸变化。 |

## 4. API 逐项说明

### `enum QWindow::AncestorMode`

决定 `isAncestorOf()` 和 `parent()` 这类关系查询是否把 `transientParent` 纳入祖先关系。`ExcludeTransients` 只看真实父窗口，`IncludeTransients` 把临时父窗口也算进去。处理弹窗、对话框归属和窗口层级时要选对模式。

### `enum QWindow::Visibility`

描述窗口可见状态。`Windowed` 是普通窗口，`Minimized`、`Maximized`、`FullScreen` 对应窗口管理器状态，`AutomaticVisibility` 让平台决定初次显示方式，`Hidden` 表示隐藏。它比单纯 `visible` 更能表达“怎么显示”。

### `active : bool`

只读属性，表示窗口是否处于活动状态。活动窗口通常接收键盘焦点或被平台标为当前窗口。它适合更新标题栏状态、暂停非活动窗口渲染；不要把它等同于“窗口可见”。

### `contentOrientation : Qt::ScreenOrientation`

描述窗口内容希望呈现的方向。移动设备旋转、全屏视频、游戏画面会用到。它不是直接旋转窗口内容的绘制命令，而是告诉系统内容方向发生变化。

### `flags : Qt::WindowFlags`

窗口标志控制窗口类型和装饰，例如普通窗口、对话框、工具窗口、无边框窗口。应在显示前设置；显示后修改可能导致窗口系统重建或表现不一致。

### `height` / `width` / `x` / `y`

这些属性描述客户区尺寸和位置。它们适合简单绑定或读写单个维度；需要同时改变位置和尺寸时优先用 `setGeometry()`，减少中间状态。

### `minimumHeight` / `minimumWidth` / `maximumHeight` / `maximumWidth`

限制窗口可调整的尺寸范围。窗口管理器通常会遵守这些提示，但平台差异存在。设置范围时要保证最小值不超过最大值。

### `modality : Qt::WindowModality`

设置窗口模态。模态窗口会阻塞某些其他窗口的输入，但它不是业务锁。真正的业务流程仍应在接受/拒绝对话框后显式处理。

### `opacity : qreal`

设置窗口整体透明度，常见范围是 0 到 1。透明窗口是否可点击、是否启用合成、性能如何由平台决定。不要用频繁改变窗口透明度替代内容动画。

### `title : QString`

窗口标题栏文本。文件编辑器通常把文档名和修改状态反映在这里；若需要平台文档代理图标或路径，还要看 `setFilePath()`。

### `transientParent : QWindow*`

临时父窗口用于表达“这个窗口属于那个窗口”，常用于对话框、弹出层、工具窗口。它不同于 QObject parent，不负责内存销毁。

### `visibility` / `visible`

`visible` 只表示显示/隐藏；`visibility` 还能表达最小化、最大化和全屏。窗口可见后仍可能没有暴露区域，渲染代码要检查 `isExposed()`。

### `QWindow(QScreen *targetScreen = nullptr)`

创建一个顶层窗口，可指定目标屏幕。传入 `nullptr` 时由 Qt/平台选择默认屏幕。构造不会必然立刻创建原生窗口资源。

### `QWindow(QWindow *parent)`

创建子窗口。这里的 parent 是窗口层级，不等同于 QWidget 子控件布局。子窗口的支持程度和裁剪行为具有平台差异。

### `~QWindow()`

销毁窗口对象及其平台资源。关闭窗口、隐藏窗口和销毁对象是三件事；不要在关闭事件里假设对象已经被删除。

### `create()` / `destroy()`

`create()` 显式创建底层平台窗口；`destroy()` 销毁平台窗口资源但保留 C++ 对象。通常显示窗口时 Qt 会自动创建资源；只有嵌入、原生句柄、渲染后端初始化需要精确时机时才直接调用。

### `winId()` / `fromWinId(WId id)`

`winId()` 返回原生窗口 ID，可能导致平台窗口被创建。`fromWinId()` 把外部原生窗口包装成 `QWindow`，适合嵌入第三方窗口。包装窗口的能力和生命周期强烈依赖平台，不要假设可以完全控制外部窗口。

### `format()` / `requestedFormat()` / `setFormat()`

`setFormat()` 请求表面格式，例如深度缓冲、模板缓冲、颜色格式；`requestedFormat()` 返回请求值；`format()` 返回实际格式。真实格式可能因平台和图形后端调整。应在窗口创建前设置格式。

### `surfaceType()` / `setSurfaceType()`

设置窗口表面类型，如 Raster、OpenGL、Vulkan。它决定后续渲染后端如何绑定窗口。应在创建平台窗口前设置，显示后再改通常太晚。

### `setVulkanInstance()` / `vulkanInstance()`

为 Vulkan 窗口提供 `QVulkanInstance`。必须在 Vulkan surface 创建前设置，并保证实例生命周期覆盖窗口使用期。

### `screen()` / `setScreen()`

查询或请求窗口移动到某块屏幕。多屏环境下窗口可能因为用户拖动、屏幕拔插而改变屏幕，应监听 `screenChanged()`，不要只在启动时读取一次。

### `safeAreaMargins()`

返回安全区域边距，用来避开刘海、圆角、系统手势区域等。桌面平台通常为 0；移动端、特殊显示设备更重要。Qt 6.9 起可用。

### `devicePixelRatio()`

返回窗口当前设备像素比。渲染纹理、帧缓冲或离屏图像时，要用逻辑尺寸乘以这个比例得到实际像素尺寸。窗口跨屏移动后该值可能变化。

### `geometry()` / `setGeometry()`

客户区几何，不包含窗口标题栏和边框。设置几何是请求窗口系统调整窗口；窗口管理器可能修正位置或尺寸。需要包含边框时使用 frame 系列 API。

### `frameGeometry()` / `framePosition()` / `frameMargins()` / `setFramePosition()`

frame 系列 API 关注外框，即客户区加标题栏和边框。保存/恢复用户看到的窗口位置时，通常比客户区几何更贴近直觉。

### `resize()` / `setPosition()`

分别改变客户区大小和位置。需要原子地改位置和尺寸时用 `setGeometry()`。窗口管理器仍可能因最小/最大尺寸、屏幕可用区域进行调整。

### `mapToGlobal()` / `mapFromGlobal()`

在窗口本地坐标和全局屏幕坐标之间转换。弹出菜单、工具提示、拖拽命中测试需要它。Qt 6 的 `QPointF` 重载适合高 DPI 和小数坐标。

### `show()` / `hide()` / `setVisible()`

显示或隐藏窗口。`show()` 通常按普通窗口显示；`setVisible(false)` 与 `hide()` 类似。显示后是否立刻可以渲染，要等暴露事件并检查 `isExposed()`。

### `showFullScreen()` / `showMaximized()` / `showMinimized()` / `showNormal()`

请求窗口进入全屏、最大化、最小化或普通状态。平台可能拒绝或延迟执行。全屏窗口要考虑多屏、焦点切换和退出快捷键。

### `windowState()` / `windowStates()` / `setWindowState()` / `setWindowStates()`

查询或设置窗口状态。单状态接口更简单，多状态接口可表达组合状态。修改状态是对窗口管理器的请求，不应假设调用返回后立即完成。

### `close()` / `closeEvent()`

`close()` 请求关闭窗口，会发送关闭事件。`closeEvent()` 中可以接受或拒绝，例如文档未保存时弹出确认。关闭被接受后窗口通常隐藏，但是否删除对象取决于对象生命周期策略。

### `alert(int msec)`

请求平台吸引用户注意，例如任务栏闪烁。适合后台任务完成或需要用户处理的窗口。不同平台对持续时间支持不同。

### `raise()` / `lower()` / `requestActivate()`

请求改变堆叠顺序或激活窗口。现代桌面环境可能限制应用抢焦点，因此这些调用不保证成功。更稳的做法是结合平台通知或用户操作触发。

### `startSystemMove()` / `startSystemResize(Qt::Edges edges)`

把窗口移动或缩放交给系统窗口管理器，适合自绘标题栏、无边框窗口。必须由合适的用户输入事件触发，很多平台会拒绝非交互场景调用。

### `setCursor()` / `unsetCursor()` / `cursor()`

设置窗口区域内的光标。`unsetCursor()` 恢复继承或默认光标。临时全局等待光标不要用这里，应使用 `QGuiApplication::setOverrideCursor()`。

### `setMouseGrabEnabled()` / `setKeyboardGrabEnabled()`

请求捕获鼠标或键盘输入。通常只在拖拽、游戏、特殊交互中短时间使用。平台和安全策略可能拒绝，必须检查返回值并确保释放。

### `setMask()` / `mask()`

设置窗口遮罩，创建非矩形窗口或限制输入区域。现代合成窗口系统下视觉透明、输入区域和性能表现各不相同；优先用正常矩形窗口，只有确有需求时使用。

### `filePath()` / `setFilePath()`

设置窗口代表的文件路径。macOS 等平台可能用它展示文档代理图标、最近文档或标题信息。它不是打开文件，也不会自动保存文档。

### `icon()` / `setIcon()`

设置窗口图标。未设置时通常采用应用默认图标。任务栏、标题栏和窗口切换器是否显示由平台决定。

### `focusObject()` / `focusObjectChanged()`

返回或通知窗口内部当前焦点对象。Qt Quick 窗口中常用于输入法、焦点可视化和快捷键上下文。返回对象可能为空。

### `isExposed()`

判断窗口是否有可绘制暴露区域。低层渲染代码应在暴露后再绘制；窗口最小化、被遮挡或尚未显示时可能为 false。

### `isTopLevel()` / `isAncestorOf()` / `parent()`

用于判断窗口层级关系。注意 QObject parent、QWindow parent 和 transient parent 是不同概念；不要混淆所有权和窗口归属。

### `nativeEvent()`

接收平台原生事件。只有跨平台 API 无法表达需求时才重写。代码必须按平台分支解析消息，并对未知事件返回 false 交给 Qt。

### `event()` 与各类事件函数

`event()` 是通用入口；`exposeEvent()`、`resizeEvent()`、`mousePressEvent()`、`keyPressEvent()`、`touchEvent()`、`wheelEvent()` 等是更具体的处理点。重写具体事件函数时，只处理自己关心的事件；未处理逻辑要让基类或事件系统继续工作。

### `requestUpdate()`

请求窗口在合适时机收到更新事件。它适合按需渲染循环，比直接忙等或在事件处理里无限绘制更稳。更新频率仍受事件循环和平台调度影响。

## 5. 深入实践与常见坑

### QWindow 与 QWidget

`QWindow` 是窗口表面，`QWidget` 是控件树。可以通过 `QWidget::createWindowContainer()` 把窗口嵌入 Widgets，但这会引入原生子窗口、焦点和堆叠顺序问题，不应随意滥用。

### 可见不等于可画

`isVisible()` 表示窗口被请求显示；`isExposed()` 才更接近“有区域可画”。低层渲染要根据 expose/resize/update 事件组织，而不是 `show()` 后立即假设表面可用。

### 高 DPI

窗口尺寸通常是设备无关像素。创建帧缓冲、交换链、纹理时要乘 `devicePixelRatio()`，并在窗口移动到其他屏幕或屏幕缩放变化时重建相关资源。

### 状态改变是请求

全屏、最大化、激活、raise/lower 很多都交给窗口管理器。平台可能延迟、拒绝或修正结果。可靠代码应监听状态变化信号，而不是只看 setter 调用完成。

### 原生句柄有成本

调用 `winId()` 可能强制创建平台窗口。只有和外部 API 集成时才取原生句柄；普通 Qt 逻辑应尽量停留在 Qt API。
