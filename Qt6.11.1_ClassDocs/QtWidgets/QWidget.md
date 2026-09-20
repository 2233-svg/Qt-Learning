# QWidget

> Qt 6.11.1 · Qt Widgets · 来自 `QWidget`

## 1. 先建立直觉

**一句话定位：** `QWidget` 是 Qt Widgets 世界的基本可视对象，既可以作为顶层窗口，也可以作为子控件，负责几何、可见性、绘制、输入事件、焦点、父子关系和窗口属性。

### 这是什么

所有传统 Widgets 控件最终都站在 `QWidget` 这条线上：按钮、输入框、表格、主窗口、对话框都是 QWidget 的子类。它同时承担两种角色：有 parent 时是父控件内部的一块区域；没有 parent 或设置了窗口标志时就是一个顶层窗口。

理解 QWidget 的关键不是“它能不能显示”，而是这几个系统如何叠加：QObject 对象树决定生命周期，布局系统决定子控件几何，QStyle/调色板/字体决定默认外观，事件系统决定输入和绘制，窗口标志决定它是否成为平台窗口。

### 适合使用的场景

- 做一个简单顶层窗口或容器。
- 写自定义控件，重写 `paintEvent()`、鼠标/键盘事件、`sizeHint()`。
- 组合多个子控件形成业务面板。
- 处理焦点、拖放、工具提示、上下文菜单、窗口状态、保存恢复窗口几何。

### 不适合的场景

- 标准按钮、输入框、列表、表格等已有控件能满足需求时，不要从 QWidget 从零造。
- 高性能 3D/场景图界面优先考虑 Qt Quick、QWindow 或专用渲染窗口。
- 复杂主窗口框架优先用 `QMainWindow`，不要手写菜单栏、工具栏和 Dock 管理。

### 典型调用链

```cpp
#include <QApplication>
#include <QPainter>
#include <QWidget>

class ColorPanel : public QWidget
{
public:
    using QWidget::QWidget;
    QSize sizeHint() const override { return {320, 180}; }

protected:
    void paintEvent(QPaintEvent *) override
    {
        QPainter painter(this);
        painter.fillRect(rect(), palette().window());
        painter.drawText(rect(), Qt::AlignCenter, tr("Custom QWidget"));
    }
};

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    ColorPanel panel;
    panel.show();
    return QApplication::exec();
}
```

**先记住的坑：** QWidget 必须在 `QApplication` 之后创建；加入布局的控件不要反复手动 `setGeometry()`；绘制只在 `paintEvent()` 中用 `QPainter`；跨线程不要直接操作控件；隐藏、关闭、删除和应用退出是四件不同的事。

## 2. 依赖与对象关系

- 头文件：`#include <QWidget>`
- CMake：`find_package(Qt6 REQUIRED COMPONENTS Widgets)`，并链接 `Qt6::Widgets`
- 继承自：`QObject`、`QPaintDevice`
- 常见派生类：`QFrame`、`QDialog`、`QMainWindow`、`QAbstractButton`、`QLineEdit`、`QComboBox`、`QTabWidget`、`QTableView`

### 生命周期和 parent

有 parent 的 QWidget 会随父对象销毁；顶层 QWidget 没有父控件，生命周期要由栈对象、智能指针或业务对象明确管理。`setParent()` 会改变控件层级，也会隐藏控件，需要重新 `show()`。`WA_DeleteOnClose` 可以让顶层窗口关闭后自动删除，但要小心外部悬空指针。

### 几何和布局

`geometry()` 是控件在父坐标系中的矩形，`rect()` 是控件自身坐标系中的客户区。布局会根据 `sizeHint()`、`minimumSizeHint()`、`sizePolicy()`、最小/最大尺寸、stretch、margins 和 spacing 计算几何。手动几何和布局系统混用是大多数界面错位的根源。

### 绘制和更新

调用 `update()` 请求稍后重绘，Qt 会合并多个重绘请求；`repaint()` 立即重绘，容易造成卡顿和递归绘制。自定义绘制放在 `paintEvent()`，不要在里面改布局、发起耗时操作或调用 `update()` 形成循环。

### 线程

QWidget 只能在 GUI 线程创建、访问和销毁。后台线程通过信号把数据交回 GUI 线程，再由控件更新显示。即使某个 getter 看起来只是读取状态，也不要从 worker 线程直接调用。

## 3. API 速查

| API | 用途速查 |
|---|---|
| `RenderFlag` / `RenderFlags` | 控制 `render()` 时是否绘制背景、子控件、忽略遮罩。 |
| `acceptDrops` / `setAcceptDrops()` | 启用拖放进入和放下事件。 |
| `accessibleName` / `accessibleDescription` / `accessibleIdentifier` | 提供无障碍名称、说明和测试标识。 |
| `autoFillBackground` | 控制 Qt 是否在绘制前自动填充背景。 |
| `enabled` / `setEnabled()` / `setDisabled()` | 控制控件和子控件是否可交互。 |
| `visible` / `show()` / `hide()` / `setVisible()` | 控制显示隐藏；隐藏不等于删除。 |
| `geometry` / `frameGeometry` / `rect` / `pos` / `size` | 查询控件几何、窗口外框和本地绘制区域。 |
| `minimumSize` / `maximumSize` / `sizeHint` / `sizePolicy` | 参与布局尺寸协商。 |
| `layout()` / `setLayout()` / `contentsMargins()` / `contentsRect()` | 管理子控件布局和内容区域。 |
| `font` / `palette` / `styleSheet` / `style()` | 控制或查询控件外观基础。 |
| `cursor` / `setCursor()` / `unsetCursor()` | 设置鼠标进入控件时的光标。 |
| `focus` / `focusPolicy` / `setFocus()` / `clearFocus()` / `focusWidget()` | 管理键盘焦点。 |
| `mouseTracking` / `tabletTracking` | 控制无按键移动事件和 tablet move 事件是否持续发送。 |
| `toolTip` / `statusTip` / `whatsThis` | 提供帮助提示、状态栏提示和 What's This 帮助。 |
| `contextMenuPolicy` / `contextMenuEvent()` | 控制右键菜单触发方式。 |
| `addAction()` / `insertAction()` / `removeAction()` / `actions()` | 给控件挂接 QAction，用于菜单、快捷键和上下文动作。 |
| `grab()` / `render()` | 截取或渲染控件内容到图像/绘图设备。 |
| `grabMouse()` / `grabKeyboard()` / release 系列 | 临时独占鼠标或键盘输入。 |
| `grabShortcut()` / `releaseShortcut()` / shortcut 设置 | 注册控件作用域快捷键。 |
| `mapTo*()` / `mapFrom*()` | 在控件、父控件、全局坐标之间转换。 |
| `childAt()` / `childrenRect()` / `childrenRegion()` | 查询子控件命中和子控件占用区域。 |
| `windowTitle` / `windowIcon` / `windowFlags` / `windowModality` | 顶层窗口相关属性。 |
| `showFullScreen()` / `showMaximized()` / `showMinimized()` / `showNormal()` | 顶层窗口显示状态切换。 |
| `saveGeometry()` / `restoreGeometry()` | 保存和恢复顶层窗口几何。 |
| `windowHandle()` / `winId()` / `effectiveWinId()` | 访问底层 QWindow 或原生窗口 ID。 |
| `setAttribute()` / `testAttribute()` | 设置 QWidget 低层行为开关。 |
| `update()` / `repaint()` / `updateGeometry()` | 请求重绘或通知布局重新计算尺寸。 |
| `paintEvent()` / `resizeEvent()` / `mouse*Event()` / `key*Event()` | 自定义绘制和输入行为的主要重写点。 |
| `close()` / `closeEvent()` | 请求关闭控件或顶层窗口，可接受或拒绝。 |
| `setTabOrder()` | 指定键盘 Tab 焦点顺序。 |
| `createWindowContainer()` | 把 `QWindow` 嵌入 QWidget 层级。 |
| `QWIDGETSIZE_MAX` | QWidget 尺寸上限常量。 |

## 4. API 逐项说明

### 构造、析构和窗口身份

`QWidget(QWidget *parent, Qt::WindowFlags f)` 创建控件。传入 parent 时成为子控件；没有 parent 时通常是顶层窗口；窗口标志 `f` 决定是否为对话框、工具窗口、无边框等。析构会销毁子控件和相关平台资源。

`isWindow()` 判断控件是否是窗口，`window()` 返回所在顶层窗口，`parentWidget()` 返回父 QWidget，`nativeParentWidget()` 返回原生父窗口相关控件。写复合控件时通常关心 parent；写窗口管理逻辑时才关心 window。

### 可见性和关闭

`show()`、`hide()`、`setVisible()` 控制显示隐藏；`isVisible()` 表示当前可见性，`isHidden()` 表示显式隐藏。`close()` 发送关闭事件，`closeEvent()` 可以拒绝关闭。顶层窗口关闭后默认是隐藏，不一定删除对象，也不一定退出应用。

`showFullScreen()`、`showMaximized()`、`showMinimized()`、`showNormal()` 只对顶层窗口最有意义。窗口管理器可能延迟或调整结果，应通过 `isFullScreen()`、`isMaximized()`、`isMinimized()` 或窗口状态检查最终状态。

### 几何、坐标和布局

`geometry()` 是父坐标系中的矩形；`pos()` 是左上角；`size()`、`width()`、`height()` 是尺寸；`rect()` 是本地坐标矩形，通常从 `(0, 0)` 开始。`frameGeometry()`、`frameSize()` 包含顶层窗口边框和标题栏。

`move()`、`resize()`、`setGeometry()` 用于手动几何。已交给布局管理的子控件不要长期手动设置几何，否则下次布局会覆盖。`adjustSize()` 根据 size hint 调整尺寸；`updateGeometry()` 告诉父布局：我的 size hint 或 size policy 变了，需要重新布局。

`mapToGlobal()`、`mapFromGlobal()`、`mapToParent()`、`mapFromParent()`、`mapTo()`、`mapFrom()` 用于坐标转换。弹出菜单、拖放、工具提示和跨控件命中测试都离不开它们。Qt 6 的 `QPointF` 重载适合高 DPI 小数坐标。

### 尺寸约束和 size hint

`sizeHint()` 是控件建议尺寸，`minimumSizeHint()` 是建议最小尺寸；自定义控件应根据内容、字体、边距计算它们。`sizePolicy()` 告诉布局控件愿不愿意扩展、收缩以及是否按宽度计算高度。

`setMinimumSize()`、`setMaximumSize()`、`setFixedSize()` 直接限制尺寸范围；`setFixedWidth()`、`setFixedHeight()` 是单维固定。不要为了“看起来对齐”滥用 fixed size，响应式布局会变差。

`baseSize()` 和 `sizeIncrement()` 主要给窗口管理器做增量尺寸提示，例如终端按字符网格调整大小。多数普通控件用不到。

### 内容区域和边距

`contentsMargins()`、`setContentsMargins()` 决定内容边距；`contentsRect()` 是排除边距后的可用区域。自定义容器控件布局子元素时应使用 contents rect，而不是直接用 `rect()`。

`childrenRect()` 和 `childrenRegion()` 汇总子控件占用区域，可用于调试布局或自定义滚动/裁剪逻辑。它们不是布局系统的替代品。

### 绘制、刷新和截图

`paintEvent()` 是自定义绘制入口。只在这里创建面向当前控件的 `QPainter`。绘制应尽量只读状态，不做数据库、网络、复杂布局或对象创建。

`update()` 请求稍后重绘，Qt 会合并区域；`repaint()` 立即重绘，除非调试或非常特殊场景，否则优先使用 `update()`。`setUpdatesEnabled(false)` 可以短暂暂停更新，批量改 UI 后再打开；长期关闭会让界面看起来坏掉。

`grab()` 返回控件截图；`render()` 把控件绘制到 `QPaintDevice` 或 `QPainter`。`RenderFlags` 控制是否绘制背景、子控件、是否忽略 mask。

### 外观：字体、调色板、样式、背景

`font()`、`setFont()` 控制控件字体，会影响子控件继承和文本尺寸。改变字体后通常需要重新布局。

`palette()`、`setPalette()` 提供颜色角色；`backgroundRole()`、`foregroundRole()` 决定用哪些角色绘制背景和前景。现代主题和样式表可能覆盖调色板效果。

`style()` 返回当前样式；`setStyle()` 可给单个控件安装样式。`styleSheet()`、`setStyleSheet()` 设置局部样式表。局部样式表比全局样式表更可控，但复杂选择器仍可能影响性能和可维护性。

`autoFillBackground` 让 Qt 在绘制前填充背景。自绘控件如果完全绘制背景，通常不需要它；如果想让 palette window role 自动填充，可以启用。

### 启用状态、焦点和键盘

`setEnabled()`/`setDisabled()` 控制控件是否接受输入；禁用父控件会影响子控件。`isEnabledTo()` 可判断相对某个祖先是否启用。

`focusPolicy()`、`setFocusPolicy()` 决定控件如何获得焦点；`setFocus()` 请求焦点；`clearFocus()` 清除焦点；`hasFocus()` 判断自身是否有焦点；`focusWidget()` 查找子层级当前焦点控件。`setFocusProxy()` 可把复合控件的焦点转交给内部编辑器。

`keyPressEvent()`、`keyReleaseEvent()` 处理键盘事件。未处理的按键应交给基类，否则 Tab、快捷键、输入法或默认按钮行为可能被破坏。

### 鼠标、滚轮、触摸和手势

`mousePressEvent()`、`mouseMoveEvent()`、`mouseReleaseEvent()`、`mouseDoubleClickEvent()` 处理鼠标。未启用 `mouseTracking` 时，鼠标移动通常只有按键按下时才发送；启用后悬停移动也会送达。

`wheelEvent()` 处理滚轮和触控板滚动；要同时考虑 angle delta 和 pixel delta。`tabletEvent()` 处理数位板事件；`grabGesture()`/`ungrabGesture()` 用于接收 Qt 手势事件。

`underMouse()` 判断鼠标是否在控件上。注意拖拽、抓取、弹出窗口和平台窗口可能影响结果。

### 拖放

`acceptDrops`/`setAcceptDrops()` 开启拖放。随后用 `dragEnterEvent()`、`dragMoveEvent()`、`dropEvent()`、`dragLeaveEvent()` 处理拖拽数据。只有在 enter/move 中接受合适的 mime 数据，drop 才会按预期发生。

### 上下文菜单、动作和快捷键

`contextMenuPolicy` 决定右键菜单策略：默认事件、自定义菜单信号、actions 菜单等。重写 `contextMenuEvent()` 时，应根据位置和当前选择生成菜单。

`addAction()`、`insertAction()`、`removeAction()`、`actions()` 把 `QAction` 挂到控件。动作可用于右键菜单、快捷键和命令状态同步。Qt 6.3 起的重载能边创建 action 边连接槽。

`grabShortcut()` 注册快捷键并返回 ID；`setShortcutEnabled()`、`setShortcutAutoRepeat()` 调整行为；`releaseShortcut()` 释放。复杂应用通常优先使用 QAction 管理快捷键。

### 光标、鼠标/键盘抓取和 mask

`setCursor()` 设置鼠标位于控件上时的光标，`unsetCursor()` 恢复。全局等待光标应使用 `QApplication::setOverrideCursor()`，不要给每个控件单独设置。

`grabMouse()`/`releaseMouse()`、`grabKeyboard()`/`releaseKeyboard()` 独占输入。只在拖拽、弹出交互、特殊输入模式中短时间使用，异常路径必须释放。`mouseGrabber()`、`keyboardGrabber()` 可查询当前抓取者。

`setMask()` 限制控件可见/输入区域，常用于非矩形控件。它可能影响性能和平台表现；优先考虑普通矩形控件加透明绘制。

### 无障碍和帮助文本

`accessibleName`、`accessibleDescription`、`accessibleIdentifier` 服务屏幕阅读器、自动化测试和无障碍工具。交互控件应有清晰名称；只有图标的按钮尤其需要设置。

`toolTip` 是鼠标悬停提示，`toolTipDuration` 控制显示时长；`statusTip` 通常给状态栏使用；`whatsThis` 用于 Qt 的 What's This 帮助模式。

### 窗口属性

`windowTitle`、`windowIcon`、`windowFilePath`、`windowModified` 主要对顶层窗口有意义。`[*]` 占位可让标题自动反映修改状态。`windowFilePath` 可帮助平台把窗口和文档关联。

`windowFlags`、`setWindowFlag()`、`setWindowFlags()` 改变窗口类型和装饰。对已经显示的窗口修改 flags 可能导致隐藏/重建，改完通常要重新 show。

`windowModality` 控制模态；`windowOpacity` 控制窗口整体透明度；`windowState()`/`setWindowState()` 查询和设置最小化、最大化、全屏等状态。

### 原生窗口和嵌入

`winId()` 返回原生窗口 ID，可能强制创建原生窗口。`effectiveWinId()` 返回实际用于平台窗口的 ID。普通 Widgets 代码不要为了“拿个句柄看看”调用它。

`windowHandle()` 返回关联的 `QWindow`，顶层控件显示后通常才有意义。`createWindowContainer()` 能把 `QWindow` 放进 QWidget 界面，但会带来原生子窗口、焦点、裁剪和堆叠问题，应谨慎使用。

### 保存和恢复窗口几何

`saveGeometry()` 保存顶层窗口大小、位置和状态，`restoreGeometry()` 恢复。适合配合 `QSettings` 记住主窗口状态。恢复失败时应提供合理默认尺寸，避免窗口跑到不可见屏幕。

### 属性和低层行为

`setAttribute()` / `testAttribute()` 控制低层 QWidget 属性，例如删除策略、透明背景、鼠标穿透、绘制方式等。属性通常影响事件、绘制或平台窗口行为，设置前应理解具体枚举含义。

### 事件总入口

`event()` 是所有事件的通用入口。一般优先重写具体事件函数；只有需要统一拦截多类事件时才重写 `event()`。未处理事件应返回基类结果。

### change/move/resize/show/hide 事件

`changeEvent()` 处理字体、调色板、语言、启用状态等变化；`moveEvent()`、`resizeEvent()` 处理几何变化；`showEvent()`、`hideEvent()` 处理显示隐藏。不要在这些事件里做长耗时工作。

### paint engine 和 metric

`paintEngine()`、`metric()` 来自 `QPaintDevice` 层，Qt 内部和低层绘制代码会用到。普通业务控件很少直接调用或重写。

### setupUi(QWidget *widget)

这是由 uic 生成的 UI 类常见入口，用来把 `.ui` 文件里的控件树安装到传入 widget 上。应用代码通常调用生成类的 `setupUi(this)`，而不是在 QWidget 子类里自己实现同名函数。

### QWIDGETSIZE_MAX

QWidget 支持的最大尺寸常量。设置最大尺寸或做布局计算时可用它表示“实际上不限制”。不要把它当作屏幕尺寸或实际可显示尺寸。

## 5. 深入实践与常见坑

### 顶层窗口和子控件不是一回事

同一个 QWidget 类，没 parent 时可能是窗口，有 parent 时只是父控件的一块区域。窗口 flags、标题、图标、模态、透明度等主要对顶层窗口有意义。

### 布局优先

绝大多数界面应交给布局管理器。手动 `setGeometry()` 适合自定义布局容器、动画或特殊绘图场景，不适合普通表单。控件大小异常时先看 `sizeHint()`、`sizePolicy()`、最小/最大尺寸和父布局参数。

### update 比 repaint 更健康

`update()` 让 Qt 合并重绘区域，能避免重复绘制；`repaint()` 立即同步绘制，容易造成卡顿甚至递归。除非你非常确定需要同步刷新，否则不要用 `repaint()`。

### 不要跨线程碰控件

后台线程只生产数据，不直接改 UI。用信号槽、`QMetaObject::invokeMethod()` 或事件把更新投递到 GUI 线程。

### 样式表不是万能主题系统

Style Sheet 很快能做出效果，但复杂项目里会和 QStyle、palette、自绘控件相互影响。能用局部规则就不要全局规则，能用现成控件属性就不要写过深选择器。
