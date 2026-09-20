# Qt QWidget 深入笔记

> 适用版本：Qt 6.11.1
> 头文件：`#include <QWidget>`
> 所属模块：`Qt6::Widgets`
> 继承：`QObject`、`QPaintDevice`

## 它解决什么问题

`QWidget` 是 Qt Widgets 体系的可视对象基类。一个 widget 可以是顶层窗口，也可以是另一个 widget 的子控件；它能拥有几何尺寸、父子关系、布局、样式、字体、调色板、事件处理、绘制表面、焦点、鼠标键盘输入、拖放、快捷键和窗口系统句柄。

它同时站在两条体系上：

- `QObject`：对象树、属性、事件、信号槽、生命周期。
- `QPaintDevice`：可以被 `QPainter` 绘制。

`QWidget` 解决的是“让一个 C++ 对象进入桌面窗口系统并成为可见、可布局、可交互的界面元素”。它不是普通数据容器，也不是线程无关对象。所有 QWidget 都应在 GUI 线程创建和访问。

## 实际使用场景

- 作为主窗口或普通面板的根容器。
- 作为自定义控件的基类，重写 `paintEvent()` 和输入事件。
- 组合多个子控件并交给 `QLayout` 管理。
- 接收鼠标、键盘、拖放、触控、输入法、上下文菜单等事件。
- 提供窗口标题、图标、模态、透明度、全屏/最大化等顶层窗口行为。

如果界面是 Qt Quick 场景，不应把 QWidget 当作 QML Item 使用；如果只是存业务状态，也不该为了“方便发信号”继承 QWidget，继承 `QObject` 更合适。

## 对象模型与所有权

传入 parent 的 widget 会成为父控件的子对象。父控件销毁时，子控件会自动销毁。作为子控件时，它默认显示在父控件内部；没有 parent 且设置为窗口类型时，它是顶层窗口。

不要重复 delete 子控件；也不要在非 GUI 线程直接改 UI。跨线程更新界面应通过 queued signal、`QMetaObject::invokeMethod()` 或事件投递回 GUI 线程。

## 几何、布局和坐标

`geometry()` 是相对父控件的外部矩形；`rect()` 是自身局部坐标系矩形，通常从 `(0, 0)` 到 `width/height`；`frameGeometry()` 包含顶层窗口装饰。绘制和鼠标事件大多使用 widget 局部坐标。

手动 `move()`、`resize()`、`setGeometry()` 可用于简单或绝对定位场景，但业务界面应优先使用 `QLayout`。字体、翻译文本、平台样式、DPI 和用户缩放都会改变控件自然尺寸。自定义控件应实现 `sizeHint()`、必要时实现 `minimumSizeHint()`，并配置 `QSizePolicy`。

坐标转换用 `mapToGlobal()`、`mapFromGlobal()`、`mapToParent()`、`mapFromParent()`、`mapTo()`、`mapFrom()`。弹出菜单、tooltip、拖放反馈这类跨窗口 UI 要特别注意全局坐标和高 DPI。

## 绘制和刷新

自定义控件通常重写 `paintEvent(QPaintEvent *)`，在其中创建 `QPainter painter(this)` 绘制。不要在任意函数里直接长时间持有 painter，也不要在 `paintEvent()` 外随意向 widget 绘制；刷新应调用 `update()`，让 Qt 合并重绘请求并在事件循环中绘制。

`repaint()` 会更急迫地触发重绘，容易造成递归绘制或性能问题，除非确实需要同步刷新。`autoFillBackground`、`palette`、`styleSheet`、`QStyle`、`WA_OpaquePaintEvent` 等都会影响背景绘制和重绘成本。

`render()` 和 `grab()` 用于把 widget 画到另一个 paint device 或 pixmap，适合截图、打印预览、缓存或测试，但它们不是常规 UI 刷新路径。

## 事件与输入

大多数交互通过虚函数事件处理：`mousePressEvent()`、`mouseMoveEvent()`、`keyPressEvent()`、`focusInEvent()`、`dragEnterEvent()`、`inputMethodEvent()` 等。更底层或统一处理可重写 `event()`，但要谨慎保留基类行为。

焦点由 `focusPolicy`、`setFocus()`、`clearFocus()`、`setTabOrder()`、`focusProxy()` 共同决定。想收到键盘事件，控件必须能获得焦点。

鼠标移动默认只在按键按下时持续发送；要无按键也收到移动，启用 `setMouseTracking(true)`。拖放前要 `setAcceptDrops(true)`，并在 drag enter/move 中接受合适 action。

## 顶层窗口行为

顶层 QWidget 可以设置标题、图标、文件路径、模态、窗口状态、flags、透明度和全屏/最大化/最小化。子控件也有这些属性的一部分，但只有顶层窗口才会真正映射到平台窗口装饰。

调用 `winId()` 会迫使 widget 拥有 native window handle，这可能影响性能、层级和平台行为。只有在需要与原生 API 互操作时才主动获取。

## 样式、字体、调色板和可访问性

`style()` 和 `QStyle` 决定标准控件如何绘制；`styleSheet` 可覆盖部分外观，但过度使用会影响样式一致性和性能。`font`、`palette`、`locale`、`layoutDirection` 具有继承语义，子控件通常会继承父级设置。

`accessibleName`、`accessibleDescription`、`accessibleIdentifier` 帮助屏幕阅读器和自动化工具理解界面。图标按钮、无文本控件、自绘控件尤其要补充可访问信息。

## 常见误区

- 不要在工作线程直接访问 QWidget。
- 不要把 QWidget 当普通 RAII 资源随意复制；它不可拷贝，生命周期由对象树和 GUI 线程约束。
- 不要只重写 `paintEvent()` 而不提供合理 `sizeHint()`。
- 不要在 layout 管理的子控件上频繁手动 `setGeometry()`。
- 不要把 `hide()` 当成销毁；隐藏后对象仍存在，信号槽和资源仍在。
- 不要依赖默认 OpenGL/native window 行为；需要原生句柄时要理解 `winId()` 的副作用。

## API 速查表

| 类别 | API | 是做什么的 | 使用时重点注意 |
| --- | --- | --- | --- |
| 构造 | `QWidget(QWidget *parent = nullptr, Qt::WindowFlags f = {})` | 创建顶层窗口或子控件。 | 有 parent 时由父对象管理生命周期；无 parent 通常是窗口。 |
| 析构 | `~QWidget()` | 销毁控件及其子对象。 | 父控件会自动删除子控件，避免重复 delete。 |
| 类型 | `bool isWindow() const` | 判断是否顶层窗口。 | Qt 6.1 起替代旧的 `isTopLevel()`。 |
| 原生句柄 | `winId()` / `effectiveWinId()` / `internalWinId()` | 获取平台窗口 ID。 | `winId()` 可能创建 native window，只在原生互操作时使用。 |
| 样式 | `QStyle *style() const` / `setStyle(QStyle *)` | 查询或设置控件 style。 | style 不等于 stylesheet；自定义 style 所有权要看传入方式。 |
| 启用状态 | `isEnabled()` / `setEnabled()` / `setDisabled()` / `isEnabledTo()` | 控制控件是否可交互。 | 父控件禁用会影响子控件实际可用性。 |
| 几何 | `geometry()` / `setGeometry()` | 读写相对父控件的矩形。 | layout 管理下不宜频繁手动设置。 |
| 局部矩形 | `rect()` / `width()` / `height()` / `size()` | 查询自身局部绘制区域和尺寸。 | `rect()` 常用于 `paintEvent()`。 |
| 位置 | `pos()` / `move()` / `x()` / `y()` | 查询或移动控件位置。 | 坐标相对父控件；顶层窗口受窗口管理器影响。 |
| 外框 | `frameGeometry()` / `frameSize()` / `normalGeometry()` | 查询窗口装饰后的几何或正常状态几何。 | 主要用于顶层窗口。 |
| 子区域 | `childrenRect()` / `childrenRegion()` | 查询所有子控件占据范围。 | 可用于自定义容器计算内容区域。 |
| 尺寸约束 | `minimumSize()` / `maximumSize()` / `setMinimumSize()` / `setMaximumSize()` | 控制布局可分配尺寸范围。 | 极限尺寸会参与父布局协商。 |
| 固定尺寸 | `setFixedSize()` / `setFixedWidth()` / `setFixedHeight()` | 把最小和最大尺寸设为同一值。 | 会限制响应式布局，谨慎用于可翻译文本。 |
| 尺寸提示 | `sizeHint()` / `minimumSizeHint()` | 返回控件自然尺寸建议。 | 自定义控件要按内容和字体给出合理值。 |
| 尺寸策略 | `sizePolicy()` / `setSizePolicy()` | 告诉 layout 如何拉伸或收缩控件。 | 与 size hint、min/max size 一起决定布局结果。 |
| 坐标转换 | `mapToGlobal()` / `mapFromGlobal()` | 局部坐标与屏幕坐标互转。 | 弹出菜单、tooltip、拖放位置常用。 |
| 坐标转换 | `mapToParent()` / `mapFromParent()` / `mapTo()` / `mapFrom()` | 与父控件或任意祖先/相关控件互转坐标。 | 目标控件为 null 或跨窗口时要确认语义。 |
| 层级 | `parentWidget()` / `window()` / `nativeParentWidget()` / `topLevelWidget()` | 查询父控件和所属窗口。 | `window()` 返回顶层 QWidget，不等于 `QWindow`。 |
| 屏幕 | `screen()` / `windowHandle()` | 查询关联屏幕或底层 `QWindow`。 | 只有映射到窗口系统后才稳定。 |
| 布局 | `layout()` / `setLayout()` | 查询或安装布局管理器。 | layout 接管子控件几何；不要混用手动定位。 |
| 更新布局 | `updateGeometry()` | 通知父布局 size hint 或策略变了。 | 自定义控件内容尺寸变化后调用。 |
| 调色板 | `palette()` / `setPalette()` / `backgroundRole()` / `foregroundRole()` | 控制颜色角色。 | 受 style 和 stylesheet 影响。 |
| 字体 | `font()` / `setFont()` / `fontMetrics()` / `fontInfo()` | 控制字体和查询字体度量。 | 字体变化会影响 size hint 和布局。 |
| 光标 | `cursor()` / `setCursor()` / `unsetCursor()` | 设置鼠标悬停光标。 | 子控件可继承或覆盖父级光标。 |
| 鼠标跟踪 | `setMouseTracking()` / `hasMouseTracking()` / `underMouse()` | 控制无按键时是否接收 mouse move。 | 默认只有按下鼠标时持续移动事件。 |
| Tablet | `setTabletTracking()` / `hasTabletTracking()` | 控制 tablet move 事件跟踪。 | 绘图板应用常用。 |
| Mask | `setMask()` / `mask()` / `clearMask()` | 设置非矩形可见/命中区域。 | 复杂 mask 可能影响性能和平台行为。 |
| 绘制到设备 | `render(QPaintDevice *, ...)` / `render(QPainter *, ...)` | 把 widget 内容绘制到外部设备或 painter。 | 截图、缓存、打印时使用，不是常规刷新入口。 |
| 截图 | `QPixmap grab(const QRect & = ...)` | 抓取 widget 内容为 pixmap。 | 矩形默认抓整个控件；隐藏或未绘制内容可能不完整。 |
| 图形效果 | `graphicsEffect()` / `setGraphicsEffect()` | 设置阴影、模糊等 `QGraphicsEffect`。 | 效果对象由 widget 接管；可能增加重绘成本。 |
| 手势 | `grabGesture()` / `ungrabGesture()` | 注册或取消 Qt 手势识别。 | 手势事件经 `event()` 或专门逻辑处理。 |
| 窗口标题 | `windowTitle()` / `setWindowTitle()` / `windowTitleChanged` | 设置或监听窗口标题。 | 对子控件通常只是属性，对顶层窗口影响装饰栏。 |
| 窗口图标 | `windowIcon()` / `setWindowIcon()` / `windowIconChanged` | 设置或监听窗口图标。 | 平台任务栏/标题栏展示受系统限制。 |
| 文件路径 | `windowFilePath()` / `setWindowFilePath()` | 关联窗口代表的文件路径。 | macOS 等平台可用于窗口代理图标。 |
| 修改状态 | `isWindowModified()` / `setWindowModified()` | 标记窗口内容是否修改。 | 标题中 `[*]` 占位可显示修改状态。 |
| 透明度 | `windowOpacity()` / `setWindowOpacity()` | 设置顶层窗口透明度。 | 平台支持和性能差异明显。 |
| tooltip | `toolTip()` / `setToolTip()` / `toolTipDuration()` / `setToolTipDuration()` | 设置悬停提示。 | 短提示用 tooltip，长上下文帮助用 What's This。 |
| status tip | `statusTip()` / `setStatusTip()` | 设置状态栏提示文本。 | 通常由 `QStatusBar` 或 action 体系消费。 |
| What's This | `whatsThis()` / `setWhatsThis()` | 设置点击式上下文帮助文本。 | 配合 `QWhatsThis` 使用。 |
| 可访问性 | `accessibleName()` / `setAccessibleName()` | 设置屏幕阅读器名称。 | 图标按钮和自绘控件尤其重要。 |
| 可访问性 | `accessibleDescription()` / `setAccessibleDescription()` | 设置辅助技术描述。 | 描述用途、状态或额外上下文。 |
| 可访问性 | `accessibleIdentifier()` / `setAccessibleIdentifier()` | 设置稳定自动化/可访问标识。 | Qt 6.9 起；适合 UI 自动化定位。 |
| 文本方向 | `layoutDirection()` / `setLayoutDirection()` / `unsetLayoutDirection()` / `isRightToLeft()` / `isLeftToRight()` | 控制左右布局方向。 | 阿拉伯语、希伯来语等 RTL 界面要测试。 |
| 本地化 | `locale()` / `setLocale()` / `unsetLocale()` | 设置控件 locale。 | 影响日期、数字、文本方向等本地化行为。 |
| 焦点 | `setFocus()` / `clearFocus()` / `hasFocus()` / `focusPolicy()` / `setFocusPolicy()` | 控制键盘焦点。 | 想收到键盘事件，必须允许并获得焦点。 |
| Tab 顺序 | `static setTabOrder(...)` | 设置键盘 Tab 焦点顺序。 | 表单和复杂对话框需要显式整理。 |
| 焦点代理 | `setFocusProxy()` / `focusProxy()` | 把焦点转交给内部子控件。 | 复合控件常用。 |
| 上下文菜单 | `contextMenuPolicy()` / `setContextMenuPolicy()` / `customContextMenuRequested` | 控制右键菜单策略。 | `CustomContextMenu` 会发出坐标信号。 |
| 鼠标捕获 | `grabMouse()` / `releaseMouse()` / `mouseGrabber()` | 强制把鼠标事件送到某控件。 | 只在拖动等短时场景使用，异常路径要释放。 |
| 键盘捕获 | `grabKeyboard()` / `releaseKeyboard()` / `keyboardGrabber()` | 强制把键盘事件送到某控件。 | 滥用会破坏用户输入体验。 |
| 快捷键 | `grabShortcut()` / `releaseShortcut()` / `setShortcutEnabled()` / `setShortcutAutoRepeat()` | 注册和控制 widget 级快捷键。 | 更常见做法是使用 `QAction`。 |
| Action | `addAction()` / `addActions()` / `insertAction()` / `removeAction()` / `actions()` | 把 action 附加到控件。 | 菜单、工具栏、快捷键和上下文菜单共享 action 很方便。 |
| 拖放 | `acceptDrops()` / `setAcceptDrops()` | 控制是否接收拖放事件。 | 还要在 drag enter/move 中接受合适 MIME 和 action。 |
| 可见性 | `show()` / `hide()` / `setVisible()` / `isVisible()` / `isHidden()` | 显示或隐藏控件。 | 隐藏不等于销毁。 |
| 显示状态 | `showFullScreen()` / `showMaximized()` / `showMinimized()` / `showNormal()` | 切换顶层窗口显示状态。 | 对子控件无顶层窗口意义。 |
| 窗口状态 | `windowState()` / `setWindowState()` / `isMinimized()` / `isMaximized()` / `isFullScreen()` | 查询或设置窗口状态。 | 不同平台窗口管理器行为不同。 |
| 层叠顺序 | `raise()` / `lower()` / `stackUnder()` | 调整同级控件 Z 顺序。 | 对顶层窗口和子控件语义不同。 |
| 刷新 | `update()` / `repaint()` | 请求异步或同步重绘。 | 优先 `update()`；避免在 paint 中递归 repaint。 |
| 启停刷新 | `updatesEnabled()` / `setUpdatesEnabled()` | 暂停或恢复重绘。 | 批量更新 UI 时可临时关闭，恢复后记得刷新。 |
| 滚动内容 | `scroll()` | 平移控件内容区域并触发暴露区域重绘。 | 自定义大画布优化时有用。 |
| 关闭 | `close()` | 请求关闭窗口或控件。 | 会触发 `closeEvent()`，事件可被忽略。 |
| 输入法 | `inputMethodHints()` / `setInputMethodHints()` / `inputMethodQuery()` / `updateMicroFocus()` | 配置和响应输入法。 | 文本编辑、自定义输入控件需要实现查询。 |
| 属性 | `setAttribute()` / `testAttribute()` | 设置 Qt widget attribute。 | 如透明背景、原生窗口、绘制优化等高级行为。 |
| 窗口 flags | `windowFlags()` / `setWindowFlags()` / `overrideWindowFlags()` / `windowType()` | 控制窗口类型和装饰。 | 改 flags 可能导致窗口重新创建或隐藏后需再 show。 |
| 事件总入口 | `bool event(QEvent *)` | 处理所有事件的分发入口。 | 只有需要统一截获时重写，通常调用基类。 |
| 绘制事件 | `paintEvent(QPaintEvent *)` | 自定义绘制入口。 | 只在这里用 `QPainter(this)` 绘制 widget 内容。 |
| 尺寸事件 | `resizeEvent(QResizeEvent *)` / `moveEvent(QMoveEvent *)` | 响应尺寸或位置变化。 | 用于重建缓存、同步子区域。 |
| 显隐事件 | `showEvent()` / `hideEvent()` | 响应显示或隐藏。 | 可延迟初始化可见时才需要的资源。 |
| 关闭事件 | `closeEvent(QCloseEvent *)` | 响应关闭请求。 | 可保存状态或询问用户，必要时 ignore。 |
| 鼠标事件 | `mousePressEvent()` / `mouseMoveEvent()` / `mouseReleaseEvent()` / `mouseDoubleClickEvent()` / `wheelEvent()` / `enterEvent()` / `leaveEvent()` | 响应鼠标和滚轮。 | 坐标是 widget 局部坐标。 |
| 键盘事件 | `keyPressEvent()` / `keyReleaseEvent()` | 响应键盘。 | 控件需要焦点；快捷键可能先被 action/shortcut 消费。 |
| 焦点事件 | `focusInEvent()` / `focusOutEvent()` | 响应焦点进入或离开。 | 常用于显示光标、选中边框或提交编辑。 |
| 拖放事件 | `dragEnterEvent()` / `dragMoveEvent()` / `dragLeaveEvent()` / `dropEvent()` | 响应拖放生命周期。 | enter/move 中 accept 后才会正常 drop。 |
| 输入法事件 | `inputMethodEvent(QInputMethodEvent *)` | 处理预编辑和提交文本。 | 自定义文本控件必须认真实现。 |
| Tablet 事件 | `tabletEvent(QTabletEvent *)` | 响应压感笔等输入。 | 绘图应用常用。 |
| Action 事件 | `actionEvent(QActionEvent *)` | 响应 action 增删变化。 | 自定义 action 容器时使用。 |
| Change 事件 | `changeEvent(QEvent *)` | 响应字体、语言、style、enabled 等状态变化。 | 翻译或主题切换时常触发。 |
| 上下文菜单事件 | `contextMenuEvent(QContextMenuEvent *)` | 响应右键/菜单键。 | 与 context menu policy 配合。 |
| 原生事件 | `nativeEvent(...)` | 处理平台原生消息。 | 跨平台性差，只在确有原生需求时使用。 |
| 绘制设备 | `paintEngine()` / `devType()` | QPaintDevice 相关底层接口。 | 普通代码很少直接调用。 |
| 宏 | `QWIDGETSIZE_MAX` | QWidget 尺寸上限常量。 | 布局极值和自定义尺寸限制中偶尔出现。 |
| 枚举 | `RenderFlag` / `RenderFlags` | 控制 `render()` 是否画背景、子控件、忽略 mask。 | 截图或离屏渲染时选择。 |

## 一句话总结

`QWidget` 是 Widgets 世界的地基：它把对象树、窗口系统、布局、绘制和输入事件接到一起；写稳 QWidget，关键是尊重 GUI 线程、布局协商、事件驱动和绘制生命周期。
