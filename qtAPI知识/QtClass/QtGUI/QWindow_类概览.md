# QWindow：原生窗口与渲染表面边界

> 适用版本：Qt 6.11.1
> 头文件：`#include <QWindow>`
> 所属模块：`Qt6::Gui`
> 继承：`QObject`、`QSurface`

## 它解决什么问题

`QWindow` 是 Qt 对平台顶层窗口、子窗口和可渲染 surface 的低层抽象。它负责窗口句柄、几何位置、可见性、窗口状态、屏幕归属、输入事件、焦点、窗口格式以及与原生窗口系统的连接。

它与 `QWidget` 的分工不同：`QWindow` 不提供 QWidget 的子控件布局、样式体系和 backing store 管理。需要 OpenGL、Vulkan、QRhi 或原生绘制时，`QWindow` 是更直接的窗口边界；需要传统桌面控件时，通常在 `QWidget` 体系中工作，必要时再用 `QWidget::createWindowContainer()` 嵌入一个 `QWindow`。

## 实际使用场景

- 创建 OpenGL、Vulkan、QRhi 或自定义原生绘制窗口。
- 作为 `QQuickWindow`、`QVulkanWindow` 等高层窗口类的基础。
- 处理顶层窗口、工具窗口、无边框窗口和模态窗口状态。
- 获取屏幕、高 DPI、safe area 和窗口状态变化。
- 通过 `nativeEvent()` 或 native interface 与平台窗口系统交互。
- 用 `fromWinId()` 包装已有原生窗口，或使用 `createWindowContainer()` 嵌入外部渲染区域。

## 创建、显示与平台资源

构造 `QWindow` 只创建 C++/QObject 对象，窗口默认不可见，平台窗口资源也可能尚未创建。`show()`、`setVisible(true)`、`create()`、`winId()` 以及部分需要原生句柄的操作会触发平台资源创建。不要把“对象存在”理解为“已经有可用的原生窗口”。

`create()` 明确要求创建平台资源；`destroy()` 释放平台窗口资源，但不会销毁 `QWindow` 对象本身，也不会自动删除子对象。资源释放后再次显示或显式 `create()` 可以重新建立平台资源。

窗口的 `visible` 表示应用希望窗口可见；`isExposed()` 表示窗口当前是否有机会被平台显示和渲染。最小化、切换虚拟桌面、屏幕遮挡或平台合成状态都可能让两者不同。动画和持续渲染通常应以 `isExposed()` 为启动条件，并监听 `exposeEvent()`。

`exposeEvent()` 只反映暴露状态变化，不是绘制回调。真正的绘制应放在 `paintEvent()`，或在使用 OpenGL/Vulkan/QRhi 时响应 `UpdateRequest` 并安排自己的渲染循环。

## Surface 格式与生命周期

`setSurfaceType()` 和 `setFormat()` 应在平台 surface 创建前设置。窗口一旦创建了原生资源，再修改这些属性可能不生效；需要改变底层 surface 类型或关键格式时，通常应先 `destroy()`，设置新值，再 `create()`，并重新检查实际 `format()`。

`requestedFormat()` 表示应用请求的格式，`format()` 表示平台最终实际采用的格式。深度缓冲、样本数、颜色空间等属性可能被平台调整，不能只读取请求值来配置渲染器。

## 几何、屏幕与高 DPI

`setGeometry(x, y, w, h)` 同时设置位置和大小；只想改变大小时用 `resize()`，避免意外移动窗口。`geometry()` 通常是客户区几何，`frameGeometry()` 包含窗口装饰，`frameMargins()` 描述两者差异。窗口尚未创建或平台尚未返回装饰尺寸时，frame 信息可能暂时不完整。

`devicePixelRatio()` 可能随着窗口跨屏移动而改变。逻辑尺寸、物理像素尺寸和渲染 attachment 尺寸不能混用；收到 `DevicePixelRatioChange`、`screenChanged` 或 resize 后，应重新计算依赖像素比例的资源。

`safeAreaMargins()` 表示平台为刘海、圆角、系统手势区域等保留的安全边距，适合移动端和沉浸式窗口布局。它不是窗口装饰边距，也不是内容区自动缩进；应用需主动把它纳入布局。

## 所有权、线程与原生包装

`QWindow` 是 `QObject`，必须在 GUI 线程创建和使用。窗口事件、可见性变化、平台资源创建和销毁都依赖 GUI 线程事件循环；不要把窗口对象搬到工作线程，也不要从工作线程直接调用窗口 API。

`QWindow` 的 QObject 父对象关系与 transient parent、平台父窗口关系不是一回事。`setParent()` 改变 Qt 窗口层级；`setTransientParent()` 表示模态对话框、菜单等临时窗口的逻辑归属。顶层窗口也可以有 transient parent。

`fromWinId()` 返回的是对已有原生窗口的 Qt 包装，能力受平台插件限制，通常适合设置父子关系或嵌入，不等于 Qt 完全接管该窗口的绘制、生命周期和输入。外部窗口销毁后，Qt 包装对象也不能继续使用。

## 常见误区

- 在构造函数中假定 `winId()` 已经存在，导致过早创建平台资源并锁定了错误的格式。
- 用 `isVisible()` 代替 `isExposed()` 驱动持续渲染，窗口最小化后仍消耗资源。
- 把 `exposeEvent()` 当作绘制入口，遗漏 `paintEvent()` 或 `UpdateRequest`。
- 修改 `setFormat()` 后只读取 `requestedFormat()`，没有用实际 `format()` 配置渲染器。
- 用 `QWindow::size()` 直接当物理 framebuffer 大小，忽略 device pixel ratio。
- 只用 `setGeometry()` 调整尺寸，意外改变窗口位置。
- 在非 GUI 线程读写窗口状态、创建 native handle 或响应事件。
- 把 `destroy()` 当作 C++ 删除操作，或把 `fromWinId()` 当作外部窗口所有权转移。

## API 速查表

| API | 作用 | 重点注意 |
| --- | --- | --- |
| `explicit QWindow(QScreen *screen = nullptr)` | 创建顶层窗口对象，可指定初始屏幕。 | 默认不可见；构造本身不保证已有平台窗口。 |
| `explicit QWindow(QWindow *parent)` | 创建 Qt 子窗口。 | parent 关系与 transient parent 的语义不同。 |
| `~QWindow()` | 销毁窗口对象及其平台资源。 | 必须在 GUI 线程生命周期内销毁。 |
| `void create()` | 创建平台窗口资源。 | 会使 surface/format 等创建前配置进入实际生效阶段。 |
| `void destroy()` | 释放平台窗口资源，保留 C++ 对象。 | 资源句柄、native handle 和部分几何信息不能跨越此边界保存。 |
| `WId winId() const` | 返回平台窗口 ID，必要时触发创建。 | 访问前先确认自己确实需要强制创建 native window。 |
| `QPlatformWindow *handle() const` | 返回 Qt 平台窗口内部句柄。 | 主要用于平台集成；不要依赖跨平台实现细节。 |
| `void setSurfaceType(QSurface::SurfaceType)` | 设置 surface 类型。 | 应在平台资源创建前调用。 |
| `QSurface::SurfaceType surfaceType() const` | 查询 surface 类型。 | 不能代表平台最终支持的全部渲染能力。 |
| `void setFormat(const QSurfaceFormat &format)` | 设置请求的 surface 格式。 | 需在创建前设置；实际结果用 `format()` 查询。 |
| `QSurfaceFormat requestedFormat() const` | 返回应用请求的格式。 | 不是平台最终采用值。 |
| `QSurfaceFormat format() const` | 返回实际 surface 格式。 | 平台可能调整 samples、深度、颜色空间等属性。 |
| `bool isVisible() const` | 查询应用可见性状态。 | 不等于当前可渲染；持续渲染应结合 `isExposed()`。 |
| `void setVisible(bool)` | 设置窗口是否可见。 | `true` 可能触发平台资源创建和 show 事件。 |
| `void show()` / `hide()` | 显示或隐藏窗口。 | `show()` 不保证窗口立刻 exposed。 |
| `bool isExposed() const` | 判断窗口当前是否已暴露给屏幕。 | 最小化或被平台隐藏时可能为假。 |
| `void requestUpdate()` | 请求一次 `UpdateRequest` 事件。 | 适合事件驱动渲染；不保证同步立即绘制。 |
| `QRect geometry() const` | 返回客户区位置和大小。 | 坐标通常是逻辑像素；装饰使用 `frameGeometry()`。 |
| `void setGeometry(const QRect &)` / `setGeometry(int,int,int,int)` | 同时设置位置和大小。 | 只改大小请用 `resize()`。 |
| `void resize(const QSize &)` / `resize(int,int)` | 改变窗口客户区大小。 | 可能受 minimum/maximum size 约束。 |
| `QSize size() const` | 返回客户区大小。 | 不一定等于物理渲染尺寸。 |
| `void setPosition(const QPoint &)` | 设置客户区位置。 | 顶层窗口位置可能受窗口管理器修正。 |
| `QPoint position() const` | 返回客户区位置。 | 与 `framePosition()` 不同。 |
| `QRect frameGeometry() const` | 返回含装饰的窗口几何。 | 装饰尺寸依赖平台和窗口状态。 |
| `QMargins frameMargins() const` | 返回客户区到窗口框架的边距。 | 创建前或平台不提供时可能为零或暂不准确。 |
| `QPoint framePosition() const` / `setFramePosition()` | 读取或设置外框位置。 | 受窗口管理器约束，不应作为精确跨平台定位保证。 |
| `QMargins safeAreaMargins() const` | 返回系统安全区域边距。 | 不是 frame margins；需由布局主动使用。 |
| `QScreen *screen() const` / `setScreen(QScreen *)` | 查询或请求窗口所属屏幕。 | 跨屏后 device pixel ratio 和可用区域可能改变。 |
| `qreal devicePixelRatio() const` | 返回窗口当前设备像素比。 | 屏幕变化时可能改变，应重建像素相关资源。 |
| `void setMinimumSize(const QSize &)` / `setMaximumSize()` | 设置客户区尺寸边界。 | 影响 resize 和窗口管理器交互。 |
| `QSize minimumSize() const` / `maximumSize() const` | 查询尺寸限制。 | `minimumWidth()` 等是便捷访问器。 |
| `void setFlags(Qt::WindowFlags)` / `flags() const` | 设置或读取窗口类型和提示。 | 某些 flags 只在创建前或重建平台窗口时可靠。 |
| `void setFlag(Qt::WindowType, bool on = true)` | 增删单个窗口标志。 | 仍需考虑平台是否支持动态修改。 |
| `Qt::WindowType type() const` | 返回主窗口类型。 | 只反映 flags 中的类型部分。 |
| `void setTitle(const QString &)` / `title() const` | 设置或读取窗口标题。 | 标题显示由平台窗口管理器决定。 |
| `void setIcon(const QIcon &)` / `icon() const` | 设置或读取窗口图标。 | 平台可能按多尺寸选择图标。 |
| `void setOpacity(qreal)` / `opacity() const` | 设置或查询窗口透明度。 | 平台合成能力和窗口类型可能限制效果。 |
| `void setWindowState(Qt::WindowState)` | 设置单一窗口状态。 | 状态变化通常异步完成，应监听 `windowStateChanged`。 |
| `void setWindowStates(Qt::WindowStates)` | 设置状态标志集合。 | `WindowStates` 是 QFlags，可包含组合状态。 |
| `Qt::WindowState windowState() const` / `windowStates() const` | 查询当前窗口状态。 | 不要把 flags 集合当成单个枚举比较。 |
| `void showMinimized()` / `showMaximized()` / `showFullScreen()` / `showNormal()` | 以指定状态显示窗口。 | 最终结果受窗口管理器和平台策略影响。 |
| `bool isActive() const` / `requestActivate()` | 查询或请求窗口激活。 | 激活请求可能被操作系统策略拒绝。 |
| `void setModality(Qt::WindowModality)` / `modality() const` | 设置窗口模态级别。 | 需要配合正确的 transient parent 和窗口显示顺序。 |
| `bool isModal() const` | 判断窗口是否处于模态状态。 | 不等于一定阻塞了所有应用窗口。 |
| `void setParent(QWindow *)` / `parent()` | 设置或读取 Qt 窗口父子关系。 | 改变层级时可能影响顶层属性和平台句柄。 |
| `void setTransientParent(QWindow *)` / `transientParent()` | 设置临时窗口的逻辑主窗口。 | 对话框、菜单等窗口管理行为通常依赖它。 |
| `bool isAncestorOf(const QWindow *, AncestorMode)` | 判断窗口是否为另一个窗口的祖先。 | `IncludeTransients` 会把 transient parent 链纳入判断。 |
| `void setMask(const QRegion &)` / `mask() const` | 设置或读取窗口形状遮罩。 | 平台和合成器可能限制非矩形窗口效果。 |
| `QPointF mapToGlobal(const QPointF &) const` / `mapFromGlobal()` | 在窗口局部与全局坐标间转换。 | 坐标是逻辑坐标；跨屏时注意 device pixel ratio。 |
| `bool setMouseGrabEnabled(bool)` / `setKeyboardGrabEnabled(bool)` | 请求独占鼠标或键盘输入。 | 失败是正常可能性；必须有释放和异常路径。 |
| `QWindow *fromWinId(WId)` | 包装已有原生窗口 ID。 | 受平台限制，通常不取得外部窗口完整控制权。 |
| `bool close()` | 请求关闭窗口并派发关闭流程。 | 可能被 `closeEvent()` 忽略，返回值表示是否接受关闭。 |
| `void raise()` / `lower()` | 请求调整窗口 Z 顺序。 | 顶层窗口顺序受窗口管理器控制。 |
| `bool startSystemMove()` / `startSystemResize(Qt::Edges)` | 请求平台执行无边框窗口移动或缩放。 | 必须在合适的用户输入上下文调用，平台可能返回失败。 |
| `void alert(int msec)` | 请求平台对窗口进行提醒。 | 不是跨平台统一的声音或闪烁保证。 |
| `virtual bool event(QEvent *)` | 统一事件入口。 | 重写时应保留未处理事件的基类行为。 |
| `virtual void paintEvent(QPaintEvent *)` | 处理传统 QPainter 绘制请求。 | OpenGL/Vulkan 窗口通常使用各自渲染循环。 |
| `virtual void exposeEvent(QExposeEvent *)` | 处理 exposed 状态变化。 | 用它启停渲染，不把它当绘制事件。 |
| `virtual void resizeEvent(QResizeEvent *)` | 响应逻辑尺寸变化。 | 同时检查物理像素尺寸和 swapchain/framebuffer 重建。 |
| `virtual void keyPressEvent(QKeyEvent *)` / `keyReleaseEvent()` | 处理键盘输入。 | 需要正确处理 auto-repeat 和修饰键。 |
| `virtual void mousePressEvent(QMouseEvent *)` 等 | 处理鼠标按下、释放、双击、移动。 | 未处理时调用基类以维持默认传播行为。 |
| `virtual void wheelEvent(QWheelEvent *)` | 处理滚轮或触控板滚动。 | 优先 `pixelDelta()`，再 fallback 到 `angleDelta()`。 |
| `virtual bool nativeEvent(const QByteArray &, void *, qintptr *)` | 接收平台原生事件。 | 只在平台集成需要时使用，并正确填写 `result` 与返回值。 |

## 一句话总结

`QWindow` 管的是“平台窗口和渲染表面这条边界”：先区分可见与 exposed，再在创建前配置格式，并用实际 `format()`、屏幕和高 DPI 信息驱动渲染。
