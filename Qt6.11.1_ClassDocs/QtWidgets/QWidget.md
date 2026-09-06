# QWidget

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QWidget` 是 Qt Widgets 控件和窗口的共同基类，负责可见性、几何位置、绘制、输入事件和父子控件关系。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QWidget` 是 Qt Widgets 控件和窗口的共同基类，负责可见性、几何位置、绘制、输入事件和父子控件关系。

**内部模型：** 一个 QWidget 既可以是顶层窗口，也可以是另一个控件的子控件。它显示什么取决于 parent、window flags、layout、paintEvent 和样式，而不是只有一个“控件类型”概念。

**适用场景：** 自定义桌面控件、简单窗口、复合控件容器和需要直接处理鼠标/键盘/绘制的界面使用。标准交互优先复用 QPushButton、QLineEdit 等现成子类。

**典型调用链：** 构造并设置 parent -> 设置 layout/properties -> show/hide -> 通过事件函数响应输入和绘制 -> close/delete 结束生命周期。

**先记住的坑：** 布局管理的控件不要手动反复 setGeometry；paintEvent 中使用 QPainter；GUI 对象只能在 GUI 线程操作；顶层窗口关闭不等同于应用一定退出。

## 2. 依赖与对象关系

- 头文件：`#include <QWidget>`
- 继承自：QObject、QPaintDevice
- 直接派生类：QAbstractButton、QAbstractSlider、QAbstractSpinBox、QCalendarWidget、QComboBox、QDesignerActionEditorInterface、QDesignerFormWindowInterface、QDesignerObjectInspectorInterface、QDesignerPropertyEditorInterface、QDesignerWidgetBoxInterface、QDialog、QDialogButtonBox、QDockWidget、QFocusFrame、QFrame、QGroupBox、QHelpFilterSettingsWidget、QHelpSearchQueryWidget、QHelpSearchResultWidget、QKeySequenceEdit、QLineEdit、QMainWindow、QMdiSubWindow、QMenu、QMenuBar、QOpenGLWidget、QProgressBar、QQuickWidget、QRhiWidget、QRubberBand、QSizeGrip、QSplashScreen、QSplitterHandle、QStatusBar、QSvgWidget、QTabBar、QTabWidget、QToolBar,、QWizardPage

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

一个 QWidget 既可以是顶层窗口，也可以是另一个控件的子控件。它显示什么取决于 parent、window flags、layout、paintEvent 和样式，而不是只有一个“控件类型”概念。

### 状态、生命周期和线程

**生命周期：** 控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

**状态与结果：** 控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

**线程与事件循环：** 所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

## 3. 直接使用

自定义桌面控件、简单窗口、复合控件容器和需要直接处理鼠标/键盘/绘制的界面使用。标准交互优先复用 QPushButton、QLineEdit 等现成子类。 使用时通常按这个过程组织：构造并设置 parent -> 设置 layout/properties -> show/hide -> 通过事件函数响应输入和绘制 -> close/delete 结束生命周期。

```cpp
#include <QApplication>
#include <QWidget>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    QWidget window;
    window.resize(800, 600);
    window.show();
    return app.exec();
}
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum RenderFlag { DrawWindowBackground, DrawChildren, IgnoreMask }`
- `flags RenderFlags`

### 属性

- `acceptDrops : bool`
- `accessibleDescription : QString`
- `(since 6.9) accessibleIdentifier : QString`
- `accessibleName : QString`
- `autoFillBackground : bool`
- `baseSize : QSize`
- `childrenRect : QRect`
- `childrenRegion : QRegion`
- `contextMenuPolicy : Qt::ContextMenuPolicy`
- `cursor : QCursor`
- `enabled : bool`
- `focus : bool`
- `focusPolicy : Qt::FocusPolicy`
- `font : QFont`
- `frameGeometry : QRect`
- `frameSize : QSize`
- `fullScreen : bool`
- `geometry : QRect`
- `height : int`
- `inputMethodHints : Qt::InputMethodHints`
- `isActiveWindow : bool`
- `layoutDirection : Qt::LayoutDirection`
- `locale : QLocale`
- `maximized : bool`
- `maximumHeight : int`
- `maximumSize : QSize`
- `maximumWidth : int`
- `minimized : bool`
- `minimumHeight : int`
- `minimumSize : QSize`
- `minimumSizeHint : QSize`
- `minimumWidth : int`
- `modal : bool`
- `mouseTracking : bool`
- `normalGeometry : QRect`
- `palette : QPalette`
- `pos : QPoint`
- `rect : QRect`
- `size : QSize`
- `sizeHint : QSize`
- `sizeIncrement : QSize`
- `sizePolicy : QSizePolicy`
- `statusTip : QString`
- `styleSheet : QString`
- `tabletTracking : bool`
- `toolTip : QString`
- `toolTipDuration : int`
- `updatesEnabled : bool`
- `visible : bool`
- `whatsThis : QString`
- `width : int`
- `windowFilePath : QString`
- `windowFlags : Qt::WindowFlags`
- `windowIcon : QIcon`
- `windowModality : Qt::WindowModality`
- `windowModified : bool`
- `windowOpacity : double`
- `windowTitle : QString`
- `x : int`
- `y : int`

### 公有函数

- `QWidget(QWidget *parent = nullptr, Qt::WindowFlags f = Qt::WindowFlags())`
- `virtual ~QWidget()`
- `bool acceptDrops() const`
- `QString accessibleDescription() const`
- `QString accessibleIdentifier() const`
- `QString accessibleName() const`
- `QList<QAction *> actions() const`
- `void activateWindow()`
- `void addAction(QAction *action)`
- `(since 6.3) QAction * addAction(const QString &text)`
- `(since 6.3) QAction * addAction(const QIcon &icon, const QString &text)`
- `(since 6.3) QAction * addAction(const QString &text, const QKeySequence &shortcut)`
- `(since 6.3) QAction * addAction(const QIcon &icon, const QString &text, const QKeySequence &shortcut)`
- `(since 6.3) QAction * addAction(const QString &text, Args &&... args)`
- `(since 6.3) QAction * addAction(const QIcon &icon, const QString &text, Args &&... args)`
- `(since 6.3) QAction * addAction(const QString &text, const QKeySequence &shortcut, Args &&... args)`
- `(since 6.3) QAction * addAction(const QIcon &icon, const QString &text, const QKeySequence &shortcut, Args &&... args)`
- `(since 6.3) QAction * addAction(const QString &text, const QObject *receiver, const char *member, Qt::ConnectionType type = Qt::AutoConnection)`
- `(since 6.3) QAction * addAction(const QIcon &icon, const QString &text, const QObject *receiver, const char *member, Qt::ConnectionType type = Qt::AutoConnection)`
- `(since 6.3) QAction * addAction(const QString &text, const QKeySequence &shortcut, const QObject *receiver, const char *member, Qt::ConnectionType type = Qt::AutoConnection)`
- `(since 6.3) QAction * addAction(const QIcon &icon, const QString &text, const QKeySequence &shortcut, const QObject *receiver, const char *member, Qt::ConnectionType type = Qt::AutoConnection)`
- `void addActions(const QList<QAction *> &actions)`
- `void adjustSize()`
- `bool autoFillBackground() const`
- `QPalette::ColorRole backgroundRole() const`
- `QBackingStore * backingStore() const`
- `QSize baseSize() const`
- `QWidget * childAt(int x, int y) const`
- `QWidget * childAt(const QPoint &p) const`
- `(since 6.8) QWidget * childAt(const QPointF &p) const`
- `QRect childrenRect() const`
- `QRegion childrenRegion() const`
- `void clearFocus()`
- `void clearMask()`
- `QMargins contentsMargins() const`
- `QRect contentsRect() const`
- `Qt::ContextMenuPolicy contextMenuPolicy() const`
- `QCursor cursor() const`
- `WId effectiveWinId() const`
- `void ensurePolished() const`
- `Qt::FocusPolicy focusPolicy() const`
- `QWidget * focusProxy() const`
- `QWidget * focusWidget() const`
- `const QFont & font() const`
- `QFontInfo fontInfo() const`
- `QFontMetrics fontMetrics() const`
- `QPalette::ColorRole foregroundRole() const`
- `QRect frameGeometry() const`
- `QSize frameSize() const`
- `const QRect & geometry() const`
- `QPixmap grab(const QRect &rectangle = QRect(QPoint(0, 0), QSize(-1, -1)))`
- `void grabGesture(Qt::GestureType gesture, Qt::GestureFlags flags = Qt::GestureFlags())`
- `void grabKeyboard()`
- `void grabMouse()`
- `void grabMouse(const QCursor &cursor)`
- `int grabShortcut(const QKeySequence &key, Qt::ShortcutContext context = Qt::WindowShortcut)`
- `QGraphicsEffect * graphicsEffect() const`
- `QGraphicsProxyWidget * graphicsProxyWidget() const`
- `bool hasEditFocus() const`
- `bool hasFocus() const`
- `virtual bool hasHeightForWidth() const`
- `bool hasMouseTracking() const`
- `bool hasTabletTracking() const`
- `int height() const`
- `virtual int heightForWidth(int w) const`
- `Qt::InputMethodHints inputMethodHints() const`
- `virtual QVariant inputMethodQuery(Qt::InputMethodQuery query) const`
- `void insertAction(QAction *before, QAction *action)`
- `void insertActions(QAction *before, const QList<QAction *> &actions)`
- `bool isActiveWindow() const`
- `bool isAncestorOf(const QWidget *child) const`
- `bool isEnabled() const`
- `bool isEnabledTo(const QWidget *ancestor) const`
- `bool isFullScreen() const`
- `bool isHidden() const`
- `bool isMaximized() const`
- `bool isMinimized() const`
- `bool isModal() const`
- `bool isVisible() const`
- `bool isVisibleTo(const QWidget *ancestor) const`
- `bool isWindow() const`
- `bool isWindowModified() const`
- `QLayout * layout() const`
- `Qt::LayoutDirection layoutDirection() const`
- `QLocale locale() const`
- `(since 6.0) QPointF mapFrom(const QWidget *parent, const QPointF &pos) const`
- `QPoint mapFrom(const QWidget *parent, const QPoint &pos) const`
- `(since 6.0) QPointF mapFromGlobal(const QPointF &pos) const`
- `QPoint mapFromGlobal(const QPoint &pos) const`
- `(since 6.0) QPointF mapFromParent(const QPointF &pos) const`
- `QPoint mapFromParent(const QPoint &pos) const`
- `(since 6.0) QPointF mapTo(const QWidget *parent, const QPointF &pos) const`
- `QPoint mapTo(const QWidget *parent, const QPoint &pos) const`
- `(since 6.0) QPointF mapToGlobal(const QPointF &pos) const`
- `QPoint mapToGlobal(const QPoint &pos) const`
- `(since 6.0) QPointF mapToParent(const QPointF &pos) const`
- `QPoint mapToParent(const QPoint &pos) const`
- `QRegion mask() const`
- `int maximumHeight() const`
- `QSize maximumSize() const`
- `int maximumWidth() const`
- `int minimumHeight() const`
- `QSize minimumSize() const`
- `virtual QSize minimumSizeHint() const`
- `int minimumWidth() const`
- `void move(int x, int y)`
- `void move(const QPoint &)`
- `QWidget * nativeParentWidget() const`
- `QWidget * nextInFocusChain() const`
- `QRect normalGeometry() const`
- `void overrideWindowFlags(Qt::WindowFlags flags)`
- `const QPalette & palette() const`
- `QWidget * parentWidget() const`
- `QPoint pos() const`
- `QWidget * previousInFocusChain() const`
- `QRect rect() const`
- `void releaseKeyboard()`
- `void releaseMouse()`
- `void releaseShortcut(int id)`
- `void removeAction(QAction *action)`
- `void render(QPaintDevice *target, const QPoint &targetOffset = QPoint(), const QRegion &sourceRegion = QRegion(), QWidget::RenderFlags renderFlags = RenderFlags(DrawWindowBackground | DrawChildren))`
- `void render(QPainter *painter, const QPoint &targetOffset = QPoint(), const QRegion &sourceRegion = QRegion(), QWidget::RenderFlags renderFlags = RenderFlags(DrawWindowBackground | DrawChildren))`
- `void repaint(const QRect &rect)`
- `void repaint(const QRegion &rgn)`
- `void repaint(int x, int y, int w, int h)`
- `void resize(int w, int h)`
- `void resize(const QSize &)`
- `bool restoreGeometry(const QByteArray &geometry)`
- `QByteArray saveGeometry() const`
- `QScreen * screen() const`
- `void scroll(int dx, int dy)`
- `void scroll(int dx, int dy, const QRect &r)`
- `void setAcceptDrops(bool on)`
- `void setAccessibleDescription(const QString &description)`
- `void setAccessibleIdentifier(const QString &identifier)`
- `void setAccessibleName(const QString &name)`
- `void setAttribute(Qt::WidgetAttribute attribute, bool on = true)`
- `void setAutoFillBackground(bool enabled)`
- `void setBackgroundRole(QPalette::ColorRole role)`
- `void setBaseSize(const QSize &)`
- `void setBaseSize(int basew, int baseh)`
- `void setContentsMargins(int left, int top, int right, int bottom)`
- `void setContentsMargins(const QMargins &margins)`
- `void setContextMenuPolicy(Qt::ContextMenuPolicy policy)`
- `void setCursor(const QCursor &)`
- `void setEditFocus(bool enable)`
- `void setFixedHeight(int h)`
- `void setFixedSize(const QSize &s)`
- `void setFixedSize(int w, int h)`
- `void setFixedWidth(int w)`
- `void setFocus(Qt::FocusReason reason)`
- `void setFocusPolicy(Qt::FocusPolicy policy)`
- `void setFocusProxy(QWidget *w)`
- `void setFont(const QFont &)`
- `void setForegroundRole(QPalette::ColorRole role)`
- `void setGeometry(int x, int y, int w, int h)`
- `void setGeometry(const QRect &)`
- `void setGraphicsEffect(QGraphicsEffect *effect)`
- `void setInputMethodHints(Qt::InputMethodHints hints)`
- `void setLayout(QLayout *layout)`
- `void setLayoutDirection(Qt::LayoutDirection direction)`
- `void setLocale(const QLocale &locale)`
- `void setMask(const QBitmap &bitmap)`
- `void setMask(const QRegion &region)`
- `void setMaximumHeight(int maxh)`
- `void setMaximumSize(const QSize &)`
- `void setMaximumSize(int maxw, int maxh)`
- `void setMaximumWidth(int maxw)`
- `void setMinimumHeight(int minh)`
- `void setMinimumSize(const QSize &)`
- `void setMinimumSize(int minw, int minh)`
- `void setMinimumWidth(int minw)`
- `void setMouseTracking(bool enable)`
- `void setPalette(const QPalette &)`
- `void setParent(QWidget *parent)`
- `void setParent(QWidget *parent, Qt::WindowFlags f)`
- `void setScreen(QScreen *screen)`
- `void setShortcutAutoRepeat(int id, bool enable = true)`
- `void setShortcutEnabled(int id, bool enable = true)`
- `void setSizeIncrement(const QSize &)`
- `void setSizeIncrement(int w, int h)`
- `void setSizePolicy(QSizePolicy)`
- `void setSizePolicy(QSizePolicy::Policy horizontal, QSizePolicy::Policy vertical)`
- `void setStatusTip(const QString &)`
- `void setStyle(QStyle *style)`
- `void setTabletTracking(bool enable)`
- `void setToolTip(const QString &)`
- `void setToolTipDuration(int msec)`
- `void setUpdatesEnabled(bool enable)`
- `void setWhatsThis(const QString &)`
- `void setWindowFilePath(const QString &filePath)`
- `void setWindowFlag(Qt::WindowType flag, bool on = true)`
- `void setWindowFlags(Qt::WindowFlags type)`
- `void setWindowIcon(const QIcon &icon)`
- `void setWindowModality(Qt::WindowModality windowModality)`
- `void setWindowOpacity(qreal level)`
- `void setWindowRole(const QString &role)`
- `void setWindowState(Qt::WindowStates windowState)`
- `void setupUi(QWidget *widget)`
- `QSize size() const`
- `virtual QSize sizeHint() const`
- `QSize sizeIncrement() const`
- `QSizePolicy sizePolicy() const`
- `void stackUnder(QWidget *w)`
- `QString statusTip() const`
- `QStyle * style() const`
- `QString styleSheet() const`
- `bool testAttribute(Qt::WidgetAttribute attribute) const`
- `QString toolTip() const`
- `int toolTipDuration() const`
- `bool underMouse() const`
- `void ungrabGesture(Qt::GestureType gesture)`
- `void unsetCursor()`
- `void unsetLayoutDirection()`
- `void unsetLocale()`
- `void update(const QRect &rect)`
- `void update(const QRegion &rgn)`
- `void update(int x, int y, int w, int h)`
- `void updateGeometry()`
- `bool updatesEnabled() const`
- `QRegion visibleRegion() const`
- `QString whatsThis() const`
- `int width() const`
- `WId winId() const`
- `QWidget * window() const`
- `QString windowFilePath() const`
- `Qt::WindowFlags windowFlags() const`
- `QWindow * windowHandle() const`
- `QIcon windowIcon() const`
- `Qt::WindowModality windowModality() const`
- `qreal windowOpacity() const`
- `QString windowRole() const`
- `Qt::WindowStates windowState() const`
- `QString windowTitle() const`
- `Qt::WindowType windowType() const`
- `int x() const`
- `int y() const`

### 重实现的公有函数

- `virtual QPaintEngine * paintEngine() const override`

### 公有槽函数

- `bool close()`
- `void hide()`
- `void lower()`
- `void raise()`
- `void repaint()`
- `void setDisabled(bool disable)`
- `void setEnabled(bool)`
- `void setFocus()`
- `void setHidden(bool hidden)`
- `void setStyleSheet(const QString &styleSheet)`
- `virtual void setVisible(bool visible)`
- `void setWindowModified(bool)`
- `void setWindowTitle(const QString &)`
- `void show()`
- `void showFullScreen()`
- `void showMaximized()`
- `void showMinimized()`
- `void showNormal()`
- `void update()`

### 信号

- `void customContextMenuRequested(const QPoint &pos)`
- `void windowIconChanged(const QIcon &icon)`
- `void windowTitleChanged(const QString &title)`

### 静态公有成员

- `QWidget * createWindowContainer(QWindow *window, QWidget *parent = nullptr, Qt::WindowFlags flags = Qt::WindowFlags())`
- `QWidget * find(WId id)`
- `QWidget * keyboardGrabber()`
- `QWidget * mouseGrabber()`
- `void setTabOrder(QWidget *first, QWidget *second)`
- `(since 6.6) void setTabOrder(std::initializer_list<QWidget *> widgets)`

### 保护函数

- `virtual void actionEvent(QActionEvent *event)`
- `virtual void changeEvent(QEvent *event)`
- `virtual void closeEvent(QCloseEvent *event)`
- `virtual void contextMenuEvent(QContextMenuEvent *event)`
- `void create(WId window = 0, bool initializeWindow = true, bool destroyOldWindow = true)`
- `void destroy(bool destroyWindow = true, bool destroySubWindows = true)`
- `virtual void dragEnterEvent(QDragEnterEvent *event)`
- `virtual void dragLeaveEvent(QDragLeaveEvent *event)`
- `virtual void dragMoveEvent(QDragMoveEvent *event)`
- `virtual void dropEvent(QDropEvent *event)`
- `virtual void enterEvent(QEnterEvent *event)`
- `virtual void focusInEvent(QFocusEvent *event)`
- `bool focusNextChild()`
- `virtual bool focusNextPrevChild(bool next)`
- `virtual void focusOutEvent(QFocusEvent *event)`
- `bool focusPreviousChild()`
- `virtual void hideEvent(QHideEvent *event)`
- `virtual void inputMethodEvent(QInputMethodEvent *event)`
- `virtual void keyPressEvent(QKeyEvent *event)`
- `virtual void keyReleaseEvent(QKeyEvent *event)`
- `virtual void leaveEvent(QEvent *event)`
- `virtual void mouseDoubleClickEvent(QMouseEvent *event)`
- `virtual void mouseMoveEvent(QMouseEvent *event)`
- `virtual void mousePressEvent(QMouseEvent *event)`
- `virtual void mouseReleaseEvent(QMouseEvent *event)`
- `virtual void moveEvent(QMoveEvent *event)`
- `virtual bool nativeEvent(const QByteArray &eventType, void *message, qintptr *result)`
- `virtual void paintEvent(QPaintEvent *event)`
- `virtual void resizeEvent(QResizeEvent *event)`
- `virtual void showEvent(QShowEvent *event)`
- `virtual void tabletEvent(QTabletEvent *event)`
- `virtual void wheelEvent(QWheelEvent *event)`

### 重实现的保护函数

- `virtual bool event(QEvent *event) override`
- `virtual void initPainter(QPainter *painter) const override`
- `virtual int metric(QPaintDevice::PaintDeviceMetric m) const override`

### 公开宏

- `QWIDGETSIZE_MAX`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QWidget::RenderFlagflags QWidget::RenderFlags`

**作用与语义：**

这个枚举描述了调用`QWidget::render()`时如何渲染该控件。
- `QWidget::DrawWindowBackground`：`0x1`;如果你启用此选项，即使未设置`autoFillBackground`，小部件的背景也会被渲染到目标中。默认情况下，该选项是启用的。
- `QWidget::DrawChildren`：`0x2`;如果你启用此选项，小部件的子节点会递归地被渲染到目标中。默认情况下，该选项是启用的。
- `QWidget::IgnoreMask`：`0x4`;如果你启用此选项，渲染到目标时小部件的 `QWidget::mask()` 会被忽略。默认情况下，该选项被禁用。
RenderFlags 类型是 QFlags 的 typedef<RenderFlag>。它存储 RenderFlag 值的 OR 组合。

### `acceptDrops : bool`

**作用与语义：**

该属性决定该控件是否启用掉落事件。
将该属性设置为 true，会向系统宣布该控件可能能够接受丢弃事件。
警告：请勿在拖放事件处理程序中修改该属性。
默认情况下，该属性为`false`。

**如何使用：** 调用 `acceptDrops()` 读取当前值；它不会修改应用状态。

### `accessibleDescription : QString`

**作用与语义：**

该属性包含辅助技术中控件的描述。
控件的可访问描述应传达控件的功能。虽然`accessibleName`应是简短且简洁的字符串（例如保存），但描述应提供更多上下文，比如保存当前文档。
这个属性必须是本地化的。
默认情况下，该属性包含空字符串，Qt 会回退到使用工具提示来提供这些信息。

**如何使用：** 调用 `accessibleDescription()` 读取当前值；它不会修改应用状态。

### `[since 6.9] accessibleIdentifier : QString`

**作用与语义：**

此属性保存辅助技术中看到的小部件标识符。
如果设置，辅助技术可以使用小部件的可访问标识符来识别特定的小部件，例如在自动化测试中。

**如何使用：** 调用 `accessibleIdentifier()` 读取当前值；它不会修改应用状态。

### `accessibleName : QString`

**作用与语义：**

此属性保存辅助技术中看到的小部件名称。
这是辅助技术（如屏幕阅读器）宣布此小部件的主要名称。对于大多数小部件，不需要设置此属性。例如，对于 `QPushButton`，按钮的文本将被使用。
当小部件不提供任何文本时，设置此属性很重要。例如，仅包含图标的按钮需要设置此属性以配合屏幕阅读器使用。名称应简短，并与小部件传递的视觉信息相当。
此属性必须本地化。
默认情况下，此属性包含空字符串。

**如何使用：** 调用 `accessibleName()` 读取当前值；它不会修改应用状态。

### `autoFillBackground : bool`

**作用与语义：**

该属性决定了小部件背景是否自动填充。
如果启用该属性，Qt 会在调用绘画事件前填充小部件的背景。颜色由小部件`palette`的`QPalette::Window`颜色角色定义。
此外，除非设置了WA_OpaquePaintEvent或WA_NoSystemBackground属性，否则Windows总是充满`QPalette::Window`。
如果小部件的父背景是静态渐变，则该属性无法关闭（即设置为 false）。
警告：请谨慎使用该属性与 Qt 样式表一起使用。当小部件拥有有效背景或边框图片的样式表时，该属性会自动被禁用。
默认情况下，该属性是`false`。

**如何使用：** 调用 `autoFillBackground()` 读取当前值；它不会修改应用状态。

### `baseSize : QSize`

**作用与语义：**

该属性包含控件的基准大小。
如果控件定义了`sizeIncrement()`，则使用基准大小来计算合适的控件大小。
默认情况下，对于新创建的控件，该属性包含宽度和高度为零的大小。

**如何使用：** 调用 `baseSize()` 读取当前值；它不会修改应用状态。

### `[read-only] childrenRect : QRect`

**作用与语义：**

该属性表示了小部件子节点的边界矩形。
隐藏的儿童被排除在外。
默认情况下，对于没有子节点的控件，该属性包含一个宽度和高度均为零的矩形，位于原点。

**如何使用：** 调用 `childrenRect()` 读取当前值；它不会修改应用状态。

### `[read-only] childrenRegion : QRegion`

**作用与语义：**

该属性保存控件子项所占据的组合区域，。
隐藏的子项不包括在内。
默认情况下，对于没有子项的控件，此属性包含一个空区域。

**如何使用：** 调用 `childrenRegion()` 读取当前值；它不会修改应用状态。

### `contextMenuPolicy : Qt::ContextMenuPolicy`

**作用与语义：**

小部件如何显示上下文菜单。
该属性的默认值为`Qt::DefaultContextMenu`，意味着调用`contextMenuEvent()`处理程序。其他值有`Qt::NoContextMenu`、`Qt::PreventContextMenu`、`Qt::ActionsContextMenu`和`Qt::CustomContextMenu`。使用`Qt::CustomContextMenu`时，信号`customContextMenuRequested()`被发射。

**如何使用：** 调用 `contextMenuPolicy()` 读取当前值；它不会修改应用状态。

### `cursor : QCursor`

**作用与语义：**

该属性包含该控件的光标形状。
鼠标光标在该控件上方时会呈现该形状。请参阅预定义光标对象列表，了解一系列有用的形状。
编辑器小部件可能会使用工字束光标：
如果没有设置光标，或者在调用 unsetCursor() 后，则使用父游标。
默认情况下，该属性包含一个具有`Qt::ArrowCursor`形状的光标。
有些底层窗口实现如果光标离开了小部件，即使鼠标被抓取，光标也会重置。如果你想为所有小部件设置光标，即使你在窗口外，也可以考虑用`QGuiApplication::setOverrideCursor()`。

**如何使用：** 调用 `cursor()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 setCursor(Qt::IBeamCursor);
```

### `enabled : bool`

**作用与语义：**

该属性决定小部件是否被启用。
通常，启用的小部件处理键盘和鼠标事件;禁用小部件则不处理。`QAbstractButton` 有例外。
有些小部件在禁用时会以不同的方式显示自己。例如，某个按钮可能会把标签画成灰色。如果你的小部件需要知道自己何时被启用或禁用，可以使用类型为`QEvent::EnabledChange`的`changeEvent()`。
禁用一个小部件会隐式禁用其所有子组件。分别启用则使所有子小部件都被启用，除非它们已被显式禁用。在父小部件仍然被禁用时，不可能显式启用非窗口的子小部件。
默认情况下，该属性为`true`。

**如何使用：** 调用 `enabled()` 读取当前值；它不会修改应用状态。

### `[read-only] focus : bool`

**作用与语义：**

该属性在该控件（或其焦点代理）拥有键盘输入焦点时都成立。
默认情况下，该属性为`false`。
注意：获取该属性的值实际上等同于检查`QApplication::focusWidget()`是否指该控件。

**如何使用：** 调用 `focus()` 读取当前值；它不会修改应用状态。

### `focusPolicy : Qt::FocusPolicy`

**作用与语义：**

该属性表示了小部件接受键盘焦点的方式。
如果控件通过 Tab 键接受键盘聚焦，`Qt::ClickFocus`如果控件通过点击接受焦点，`Qt::StrongFocus`如果两者都接受， `Qt::NoFocus`（默认）则不接受焦点，该策略是 `Qt::TabFocus`。
如果控件处理键盘事件，您必须启用键盘焦点。这通常由控件的构造函数完成。例如，`QLineEdit`构造函数调用 setFocusPolicy（`Qt::StrongFocus`）。
如果小部件有焦点代理，那么焦点策略会传播到它。

**如何使用：** 调用 `focusPolicy()` 读取当前值；它不会修改应用状态。

### `font : QFont`

**作用与语义：**

该属性保留当前为控件设置的字体。
该属性描述了小部件所请求的字体。该字体被小部件的样式用于渲染标准组件，并作为确保自定义小部件能够与原生平台外观和感觉保持一致的手段。不同平台或不同样式通常会为应用程序定义不同的字体。
当你为小部件分配新字体时，该字体的属性会与小部件的默认字体结合，形成小部件的最终字体。你可以调用`fontInfo()`获取小部件最终字体的副本。最终字体也用于初始化`QPainter`字体。
默认字体取决于系统环境。`QApplication`维护一个系统/主题字体，作为所有控件的默认字体。某些类型的控件可能还有特殊的字体默认值。你也可以自己定义控件的默认字体，通过传递自定义字体和控件名称给`QApplication::setFont()`。最后，字体会与Qt的字体数据库匹配，以找到最佳匹配字体。
`QWidget` 会将显式字体属性从父字母传播到子节点。如果你更改字体上的某个属性并将该字体分配给控件，该属性会传播到该控件的所有子节点，覆盖该属性的系统默认设置。注意，除非启用了 `Qt::WA_WindowPropagation` 属性，否则字体默认不会传播到窗口（见 `isWindow()`）。
`QWidget` 的字体传播方式与调色板传播相似。
当前样式用于渲染所有标准 Qt 控件的内容，可以自由选择使用控件字体，或在某些情况下部分或完全忽略它。特别是某些样式如 GTK 样式、Mac 样式和 Windows Vista 样式，会对控件字体进行特殊修改，以匹配平台的原生外观和感觉。因此，给控件的字体赋予属性并不保证会改变控件的外观。相反，你可以选择应用样式表。
注意：如果 Qt 样式表与 setFont（ 相同小部件使用），则样式表优先，且设置冲突。

**如何使用：** 调用 `font()` 读取当前值；它不会修改应用状态。

### `[read-only] frameGeometry : QRect`

**作用与语义：**

小部件相对于其父节点的几何体，包括任何窗口框架。
关于窗口几何问题的概述，请参见 Window Geometry 文档。
默认情况下，该属性包含一个取决于用户平台和屏幕几何形状的值。

**如何使用：** 调用 `frameGeometry()` 读取当前值；它不会修改应用状态。

### `[read-only] frameSize : QSize`

**作用与语义：**

该属性包含了包括任何窗口框在内的小部件大小。
默认情况下，该属性包含一个取决于用户平台和屏幕几何形状的值。

**如何使用：** 调用 `frameSize()` 读取当前值；它不会修改应用状态。

### `[read-only] fullScreen : bool`

**作用与语义：**

该属性是否显示该小部件以全屏模式显示时依然适用。
全屏模式下的小部件占据整个屏幕区域，不会显示窗口装饰，如标题栏。
默认情况下，该属性为`false`。

**如何使用：** 调用 `fullScreen()` 读取当前值；它不会修改应用状态。

### `geometry : QRect`

**作用与语义：**

该属性表示了小部件相对于其父节点的几何形状，排除窗口框架。
更改几何体时，如果控件可见，会立即接收移动事件（`moveEvent()`）和/或调整大小事件（`resizeEvent()`）。如果控件当前不可见，保证在展示前收到相应事件。
如果尺寸分量超出`minimumSize()`和`maximumSize()`定义范围，则会进行调整。
警告：在`resizeEvent()`或`moveEvent()`中调用 setGeometry() 可能导致无限递归。
关于窗口几何问题的概述，请参见 Window Geometry 文档。
默认情况下，该属性包含一个取决于用户平台和屏幕几何形状的值。

**如何使用：** 调用 `geometry()` 读取当前值；它不会修改应用状态。

### `[read-only] height : int`

**作用与语义：**

该属性表示小部件的高度，但不包括任何窗框。
关于窗口几何问题的概述，请参见 Window Geometry 文档。
默认情况下，该属性包含一个取决于用户平台和屏幕几何形状的值。

**如何使用：** 调用 `height()` 读取当前值；它不会修改应用状态。

### `inputMethodHints : Qt::InputMethodHints`

**作用与语义：**

具体输入法提示是什么？
这仅适用于输入小部件。输入法用它来获取输入法应如何操作的提示。例如，如果设置了`Qt::ImhFormattedNumbersOnly`标志，输入法可能会改变其视觉成分，以反映只能输入数字。
警告：有些小部件需要某些标志才能正常工作。要设置标志，请用`w->setInputMethodHints(w->inputMethodHints()|f)`代替`w->setInputMethodHints(f)`。
注意：这些标志只是提示，因此特定的输入法实现可以忽略它们。如果你想确保输入某种类型的字符，也应该在小部件上设置一个`QValidator`。
默认值是`Qt::ImhNone`。

**如何使用：** 调用 `inputMethodHints()` 读取当前值；它不会修改应用状态。

### `[read-only] isActiveWindow : bool`

**作用与语义：**

该属性决定该控件的窗口是否为活跃窗口。
活动窗口是包含带有键盘焦点的控件的窗口（如果窗口没有控件或其控件中没有控件，则可能仍有焦点）。
当弹窗可见时，该属性对激活窗口和弹窗都`true`。
默认情况下，该属性为`false`。

**如何使用：** 调用 `isActiveWindow()` 读取当前值；它不会修改应用状态。

### `layoutDirection : Qt::LayoutDirection`

**作用与语义：**

此属性保存该控件的布局方向。
注意：此方法自 Qt 4.7 后不再影响文本布局方向。
默认情况下，该属性设置为 `Qt::LeftToRight`。
当在控件上设置布局方向时，它会传播到控件的子控件，但不会传播到作为窗口的子控件，也不会传播给已明确调用 setLayoutDirection() 的子控件。此外，在父控件调用 setLayoutDirection() 后添加的子控件不会继承父控件的布局方向。

**如何使用：** 调用 `layoutDirection()` 读取当前值；它不会修改应用状态。

### `locale : QLocale`

**作用与语义：**

此属性保存小部件的区域设置。
只要未设置特殊区域设置，此属性为父组件的区域设置，或者如果该小部件是顶层小部件，则为默认区域设置。
如果小部件显示日期或数字，应使用小部件的区域设置进行格式化。

**如何使用：** 调用 `locale()` 读取当前值；它不会修改应用状态。

### `[read-only] maximized : bool`

**作用与语义：**

该属性在该小部件是否被最大化时成立。
这个属性只适用于窗户。
注意：由于某些窗口系统的限制，这并不总是报告预期结果（例如，如果用户在X11上通过窗口管理器最大化窗口，Qt无法将此与其他调整大小区分开来）。随着窗口管理器协议的发展，这种情况预计会有所改善。
默认情况下，该属性为`false`。

**如何使用：** 调用 `maximized()` 读取当前值；它不会修改应用状态。

### `maximumHeight : int`

**作用与语义：**

此属性保存小部件的最大高度（像素）。
此属性对应 `maximumSize` 属性保存的高度。
默认情况下，此属性的值为 16777215。
注意：`QWIDGETSIZE_MAX` 宏的定义限制了小部件的最大尺寸。

**如何使用：** 调用 `maximumHeight()` 读取当前值；它不会修改应用状态。

### `maximumSize : QSize`

**作用与语义：**

此属性保存小部件的最大尺寸（像素）。
小部件不能调整为超过最大小部件尺寸的大小。
默认情况下，此属性的尺寸的宽度和高度均为 16777215。
注意：`QWIDGETSIZE_MAX` 宏的定义限制了小部件的最大尺寸。

**如何使用：** 调用 `maximumSize()` 读取当前值；它不会修改应用状态。

### `maximumWidth : int`

**作用与语义：**

此属性保存小部件的最大宽度（像素）。
此属性对应 `maximumSize` 属性保存的宽度。
默认情况下，此属性的值为 16777215。
注意：`QWIDGETSIZE_MAX` 宏的定义限制了小部件的最大尺寸。

**如何使用：** 调用 `maximumWidth()` 读取当前值；它不会修改应用状态。

### `[read-only] minimized : bool`

**作用与语义：**

该属性决定该小部件是否被最小化（图标化）。
这个属性只适用于窗户。
默认情况下，该属性为`false`。

**如何使用：** 调用 `minimized()` 读取当前值；它不会修改应用状态。

### `minimumHeight : int`

**作用与语义：**

此属性保存小部件的最小高度（像素）。
此属性对应 `minimumSize` 属性保存的高度。
默认情况下，此属性的值为 0。

**如何使用：** 调用 `minimumHeight()` 读取当前值；它不会修改应用状态。

### `minimumSize : QSize`

**作用与语义：**

此属性保存小部件的最小尺寸。
小部件不能调整为小于最小小部件尺寸的大小。如果当前尺寸较小，小部件的尺寸将被强制为最小尺寸。
此函数设置的最小尺寸将覆盖 `QLayout` 定义的最小尺寸。要取消设置最小尺寸，请使用 `QSize(0, 0)` 的值。
默认情况下，此属性包含宽度和高度均为零的尺寸。

**如何使用：** 调用 `minimumSize()` 读取当前值；它不会修改应用状态。

### `[read-only] minimumSizeHint : QSize`

**作用与语义：**

该属性表示该小部件的推荐最小尺寸。
如果该属性的值是无效的大小，则不建议设定最小大小。
默认实现的 minimumSizeHint() 如果该控件没有布局，则返回无效大小，否则返回布局的最小大小。大多数内置控件会重现 minimumSizeHint()。
除非设置了`minimumSize()`或将大小策略设置为QSizePolicy：：Ignore，否则`QLayout`永远不会将小于最小大小提示的大小。如果`minimumSize()`设置，最小大小提示将被忽略。

**如何使用：** 调用 `minimumSizeHint()` 读取当前值；它不会修改应用状态。

### `minimumWidth : int`

**作用与语义：**

此属性保存小部件的最小宽度（像素）。
此属性对应 `minimumSize` 属性保存的宽度。
默认情况下，此属性的值为 0。

**如何使用：** 调用 `minimumWidth()` 读取当前值；它不会修改应用状态。

### `[read-only] modal : bool`

**作用与语义：**

该属性决定了该控件是否为模态控件。
这个属性只适用于窗口。模态小部件阻止其他窗口中的小部件接收任何输入。
默认情况下，该属性是`false`。

**如何使用：** 调用 `modal()` 读取当前值；它不会修改应用状态。

### `mouseTracking : bool`

**作用与语义：**

该属性决定了小部件是否启用了鼠标追踪功能。
如果关闭了鼠标追踪（默认），小部件只有在移动鼠标时至少按下一个鼠标按钮时才会收到鼠标移动事件。
如果启用了鼠标追踪，即使没有按键，小部件也会接收鼠标移动事件。

**如何使用：** 调用 `mouseTracking()` 读取当前值；它不会修改应用状态。

### `[read-only] normalGeometry : QRect`

**作用与语义：**

该属性保留了该小部件在以正常（非最大化或全屏）顶层小部件显示时的几何形状。
如果小部件已经处于该状态，法线几何体将反映小部件当前的 `geometry()`。
对于子控件，该属性总是包含一个空矩形。
默认情况下，该属性包含一个空矩形。

**如何使用：** 调用 `normalGeometry()` 读取当前值；它不会修改应用状态。

### `palette : QPalette`

**作用与语义：**

该属性包含了小部件的调色板。
该属性描述了小部件的调色板。调色板被控件的样式用于渲染标准组件，并作为确保自定义小部件能够保持与原生平台外观和感觉一致的手段。不同平台或不同样式通常会有不同的调色板。
当你为小部件分配新调色板时，该调色板中的颜色角色会与小部件的默认调色板合并，形成小部件的最终调色板。小部件背景角色的调色板条目用于填充小部件的背景（见 `QWidget::autoFillBackground`），前景角色初始化`QPainter`的笔。
默认选项取决于系统环境。`QApplication`维护一个系统/主题调色板，作为所有控件的默认选项。某些类型的控件可能还有特殊的调色板默认值（例如，在 Windows Vista 上，所有源自 `QMenuBar` 的类都有特殊的默认调色板）。你也可以通过传递自定义调色板和控件名称给 `QApplication::setPalette()`，自己定义控件的默认调色板。最后，样式始终有选项，可以根据分配来润色调色板（参见 `QStyle::polish()`）。
`QWidget` 会将显式调色板角色从父节点传播到子节点。如果你为调色板上的特定角色分配画笔或颜色，并将该调色板分配给小部件，该角色会传播到该小部件的所有子节点，覆盖该角色的任何系统默认设置。注意，调色板默认不会传播到窗口（参见`isWindow()`），除非启用了`Qt::WA_WindowPropagation`属性。
`QWidget` 的调色板传播与字体传播相似。
当前样式用于渲染所有标准Qt控件的内容，可以自由选择组件调色板中的颜色和笔刷，或者在某些情况下（部分或完全）忽略调色板。特别是，像GTK样式、Mac样式和Windows Vista样式等样式依赖第三方API来渲染控件内容，而这些样式通常不遵循调色板。因此，给控件调色板分配角色并不保证改变控件的外观。相反，你可以选择应用样式表。
警告：请勿将此功能与 Qt 样式表结合使用。使用样式表时，控件的调色板可以通过“color”、“background-color”、“selection-color”、“selection-background-color”和“alternate-background-color”来自定义。

**如何使用：** 调用 `palette()` 读取当前值；它不会修改应用状态。

### `pos : QPoint`

**作用与语义：**

该属性表示该控件在其父控件中的位置。
如果小部件是窗口，则该小部件在桌面上的位置，包括其框架。
当调整位置时，如果控件可见，会立即接收移动事件（`moveEvent()`）。如果控件当前不可见，则保证在显示前收到事件。
默认情况下，该属性包含指向原点的位置。
警告：在 `moveEvent()` 内调用 move() 或 `setGeometry()` 可能导致无限递归。
关于窗口几何问题的概述，请参见 Window Geometry 文档。
注意：并非所有窗口系统都支持设置或查询顶层窗口位置。在此类系统中，程序移动窗口可能无效，且当前位置（如`QPoint(0, 0)`）可能会返回人工值。

**如何使用：** 调用 `pos()` 读取当前值；它不会修改应用状态。

### `[read-only] rect : QRect`

**作用与语义：**

该属性包含了不包含任何窗框的组件内部几何形状。
rect属性等于`QRect`（0， 0， `width()`， `height()`）。
关于窗口几何问题的概述，请参见 Window Geometry 文档。
默认情况下，该属性包含一个取决于用户平台和屏幕几何形状的值。

**如何使用：** 调用 `rect()` 读取当前值；它不会修改应用状态。

### `size : QSize`

**作用与语义：**

该属性表示了小部件的大小，但不包括任何窗口框。
如果控件在调整大小时可见，则会立即收到一个调整大小事件（`resizeEvent()`）。如果控件当前不可见，则保证在显示前收到事件。
如果尺寸超出`minimumSize()`和`maximumSize()`定义范围，则调整。
默认情况下，该属性包含一个取决于用户平台和屏幕几何形状的值。
警告：在 `resizeEvent()` 内调用 resize() 或 `setGeometry()` 可能导致无限递归。
注意：将大小设置为`QSize(0, 0)`会导致小部件不会出现在屏幕上。这同样适用于Windows。

**如何使用：** 调用 `size()` 读取当前值；它不会修改应用状态。

### `[read-only] sizeHint : QSize`

**作用与语义：**

该属性包含该小部件的推荐大小。
如果该属性的值为无效大小，则不建议使用大小。
如果该控件没有布局，默认实现的 sizeHint() 会返回无效大小，否则返回布局的首选大小。

**如何使用：** 调用 `sizeHint()` 读取当前值；它不会修改应用状态。

### `sizeIncrement : QSize`

**作用与语义：**

该属性包含小部件的大小增量。
当用户调整窗口大小时，尺寸将以 sizeIncrement() 为步骤移动。`width()` 像素水平，sizeIncrement.`height()` 像素垂直，`baseSize()` 作为基底。首选控件大小为非负整数 i 和 j：
注意，虽然你可以为所有小部件设置大小增量，但这只影响窗口。
默认情况下，该属性包含宽度和高度均为零的大小。
警告：在 Windows 下，大小递增无效，X11 上的窗口管理器可能会忽略它。

**如何使用：** 调用 `sizeIncrement()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 width = baseSize().width() + i * sizeIncrement().width();
 height = baseSize().height() + j * sizeIncrement().height();
```

### `sizePolicy : QSizePolicy`

**作用与语义：**

该属性保留了小部件的默认布局行为。
如果存在管理该控件子节点的 `QLayout`，则使用该布局指定的大小策略。如果没有这样的`QLayout`，则使用该函数的结果。
默认策略为“Preferred/Preferred”，这意味着小部件可以自由调整大小，但优先选择返回的大小`sizeHint()`。类似按钮的小部件设置大小策略，指定它们可以横向拉伸，但垂直方向是固定的。同样适用于行编辑控件（如`QLineEdit`、`QSpinBox`或可编辑`QComboBox`）以及其他横向控件（如`QProgressBar`）。`QToolButton`通常是方形的，因此允许双向扩展。支持不同方向的小部件（如`QSlider`、`QScrollBar`或QHeader）只指定相应方向的拉伸。能够提供滚动条的小部件（通常是`QScrollArea`子类）通常会指定它们可以使用额外空间，并且能用少于`sizeHint()`的空间。

**如何使用：** 调用 `sizePolicy()` 读取当前值；它不会修改应用状态。

### `statusTip : QString`

**作用与语义：**

该属性包含小部件的状态提示。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `statusTip()` 读取当前值；它不会修改应用状态。

### `styleSheet : QString`

**作用与语义：**

该属性包含小部件的样式表。
样式表包含了对小部件样式的自定义描述，详见 Qt 样式表文档。
自 Qt 4.5 起，Qt 样式表已完全支持 macOS。
警告：Qt 样式表目前不支持 custom `QStyle` 子类。我们计划在未来某个版本中解决这个问题。

**如何使用：** 调用 `styleSheet()` 读取当前值；它不会修改应用状态。

### `tabletTracking : bool`

**作用与语义：**

该属性决定了小部件是否启用平板追踪。
如果启用了平板追踪（默认设置），小部件只有在触控笔与绘图板接触时，或至少在触控笔移动时按下一个触控笔按钮时，才会收到平板移动事件。
如果启用了平板追踪，小部件即使在靠近时也会接收平板移动事件。这对于监控位置以及旋转和倾斜等辅助属性以及在界面中提供反馈非常有用。

**如何使用：** 调用 `tabletTracking()` 读取当前值；它不会修改应用状态。

### `toolTip : QString`

**作用与语义：**

该属性包含小部件的工具提示。
请注意，默认情况下，工具提示只显示在活动窗口子组件上。你可以通过在窗口设置属性`Qt::WA_AlwaysShowToolTips`来改变这种行为，而不是在带有提示的小部件上。
如果你想控制提示的行为，可以拦截`event()`函数并捕捉`QEvent::ToolTip`事件（例如，如果你想自定义提示应显示的区域）。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `toolTip()` 读取当前值；它不会修改应用状态。

### `toolTipDuration : int`

**作用与语义：**

该属性包含了小部件在提示中的持续时间。
指定提示显示的时间长度，单位为毫秒。如果值为 -1（默认），则持续时间根据提示长度计算。

**如何使用：** 调用 `toolTipDuration()` 读取当前值；它不会修改应用状态。

### `updatesEnabled : bool`

**作用与语义：**

该属性决定是否启用更新。
启用更新的小部件会接收绘图事件并有系统背景;禁用的小部件则不会。这也意味着如果更新被禁用，调用`update()`和`repaint()`不会有影响。
默认情况下，该属性为`true`。
setUpdatesEnabled() 通常用于短时间禁用更新，例如避免大变更时的屏幕闪烁。在 Qt 中，控件通常不会产生屏幕闪烁，但在 X11 上，当控件隐藏时，服务器可能会在被其他控件替换前清除屏幕上的区域。禁用更新可以解决这个问题。
禁用小部件会隐式禁用其所有子组件。启用小部件会启用除顶层小部件或已明确禁用的子小部件外的所有子小部件。重新启用更新隐式调用该小部件的`update()`。

**如何使用：** 调用 `updatesEnabled()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 setUpdatesEnabled(false);
 bigVisualChanges();
 setUpdatesEnabled(true);
```

### `visible : bool`

**作用与语义：**

该属性决定小部件是否可见。
调用 setVisible（true） 或 `show()` 会将控件设置为可见状态，前提是其所有父控件直到窗口都可见。如果祖先未被看见，控件在所有祖先显示完毕后才会显现。如果控件的大小或位置发生变化，Qt 保证控件在显示前会触发移动和调整大小事件。如果控件尚未调整大小，Qt 会用 `adjustSize()` 调整控件大小为有用的默认值。
调用 setVisible（false） 或 `hide()` 会显式隐藏一个控件。显式隐藏控件永远不会变得可见，即使它的所有祖先都变得可见，除非你展示它。
当控件的可见性状态发生变化时，小部件会接收显示和隐藏事件。在隐藏和显示事件之间，无需浪费CPU周期来准备或显示信息给用户。例如，视频应用可能只是停止生成新帧。
被屏幕上其他窗口遮挡的控件被视为可见。同样适用于图标窗口以及存在于另一个虚拟桌面上的窗口（支持该概念的平台）。当窗口系统改变控件的映射状态时，控件会接收自发的显示和隐藏事件，例如用户最小化窗口时会触发自发隐藏事件，窗口恢复时则会触发自发显示事件。
你很少需要重新实现 setVisible() 函数。如果你需要在显示小部件前更改某些设置，可以用 `showEvent()`。如果需要延迟初始化，可以使用传递给 `event()` 函数的波兰事件。

**如何使用：** 调用 `visible()` 读取当前值；它不会修改应用状态。

### `whatsThis : QString`

**作用与语义：**

该属性包含小部件的“What's This 帮助文本。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `whatsThis()` 读取当前值；它不会修改应用状态。

### `[read-only] width : int`

**作用与语义：**

该属性表示了小部件的宽度，不包括任何窗框。
关于窗口几何问题的概述，请参见 Window Geometry 文档。
注意：请勿使用此功能在多屏桌面上查找屏幕宽度。详情请参见 `QScreen`。
默认情况下，该属性包含一个取决于用户平台和屏幕几何形状的值。

**如何使用：** 调用 `width()` 读取当前值；它不会修改应用状态。

### `windowFilePath : QString`

**作用与语义：**

该属性包含与控件相关的文件路径。
这个属性只对 Windows 有意义。它将文件路径与窗口关联起来。如果你设置了文件路径但没有设置窗口标题，Qt 会将窗口标题设置为指定路径的文件名，该路径是通过 `QFileInfo::fileName()` 获得的。
如果窗口标题在任意点被设置，那么窗口标题优先，会显示它而不是文件路径字符串。
此外，在macOS上，这还有一个额外好处，就是假设文件路径存在，它会设置窗口的代理图标。
如果没有设置文件路径，该属性包含一个空字符串。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `windowFilePath()` 读取当前值；它不会修改应用状态。

### `windowFlags : Qt::WindowFlags`

**作用与语义：**

窗口标志是类型（例如`Qt::Dialog`）和零个或多个窗口系统的提示（例如`Qt::FramelessWindowHint`）的组合。
如果小部件类型为`Qt::Widget`或`Qt::SubWindow`，并且变成了窗口（`Qt::Window`、`Qt::Dialog`等），则它会被放在桌面上的位置（0， 0）。如果小部件是窗口，并且变成`Qt::Widget`或`Qt::SubWindow`，则它相对于父小部件的位置（0， 0）。
注意：该函数在更改窗口标志时调用`setParent()`，导致控件被隐藏。您必须调用`show()`才能让控件再次可见。

**如何使用：** 调用 `windowFlags()` 读取当前值；它不会修改应用状态。

### `windowIcon : QIcon`

**作用与语义：**

此属性保存小部件的图标。
此属性仅适用于窗口。如果没有设置图标，windowIcon() 将返回应用程序图标 (`QApplication::windowIcon()`)。
注意：在 macOS 上，窗口图标表示活动文档，除非使用 `setWindowFilePath` 设置了文件路径，否则不会显示。

**如何使用：** 调用 `windowIcon()` 读取当前值；它不会修改应用状态。

### `windowModality : Qt::WindowModality`

**作用与语义：**

该属性决定了模态控件阻挡的窗口。
该属性仅适用于窗口。模态控件防止其他窗口中的控件接收输入。该属性的值控制控件可见时哪些窗口被阻挡。窗口可见时更改该属性无效;你必须先`hide()`控件，然后再`show()`。
默认情况下，该属性是`Qt::NonModal`。

**如何使用：** 调用 `windowModality()` 读取当前值；它不会修改应用状态。

### `windowModified : bool`

**作用与语义：**

该属性决定窗口中显示的文档是否存在未保存的更改。
修改后的窗口是指内容发生变化但尚未保存到磁盘的窗口。该标志会因平台而异，效果各异。在macOS上，关闭按钮会有修改后的外观;在其他平台上，窗口标题会带有“*”（星号）。
窗口标题必须包含“[*]”占位符，指示“*”应出现在位置。通常，*应紧随文件名后面出现（例如，“document1.txt[*] - 文本编辑器”）。如果窗口未被修改，占位符会被直接移除。
注意，如果一个小部件被设置为修改，它的所有祖先也会被设置为被修改。然而，如果你调用`setWindowModified(false)`，这个功能不会传播到它的父节点，因为父节点的其他子节点可能也被修改过。

**如何使用：** 调用 `windowModified()` 读取当前值；它不会修改应用状态。

### `windowOpacity : double`

**作用与语义：**

该属性表示了窗口的不透明度水平。
有效不透明度范围为1.0（完全不透明）到0.0（完全透明）。
默认情况下，该属性的价值为1.0。
该功能可在支持复合扩展的嵌入式Linux、macOS、Windows和X11平台上使用。
注意：在 X11 上你需要运行复合管理器，并且你使用的窗口管理器必须支持 X11 专用的 _NET_WM_WINDOW_OPACITY Atom。
警告：将此属性从不透明改为透明可能会触发绘画事件，需要在窗口正确显示前处理。这主要影响`QScreen::grabWindow()`的使用。还要注意，半透明窗口的更新和调整速度明显慢于不透明窗口。

**如何使用：** 调用 `windowOpacity()` 读取当前值；它不会修改应用状态。

### `windowTitle : QString`

**作用与语义：**

该物业拥有窗户标题（说明）。
该属性仅适用于顶层控件，如窗口和对话框。如果未设置说明文字，标题基于`windowFilePath`。若未设置，标题为空字符串。
如果你使用`windowModified`机制，窗口标题必须包含“[*]”占位符，指示“*”应出现在位置。通常，它应紧随文件名之后（例如，“document1.txt[*] - 文本编辑器”）。如果`windowModified`属性被`false`（默认），占位符会被直接移除。
在某些桌面平台（包括 Windows 和 Unix）上，如果设置了，应用程序名称（来自 `QGuiApplication::applicationDisplayName`）会被添加到窗口标题末尾。这是通过 QPA 插件实现的，因此它会显示给用户，但不包含在 windowTitle 字符串中。

**如何使用：** 调用 `windowTitle()` 读取当前值；它不会修改应用状态。

### `[read-only] x : int`

**作用与语义：**

该属性表示了小部件相对于其父节点的 x 坐标，包括任何窗口框架。
关于窗口几何问题的概述，请参见 Window Geometry 文档。
默认情况下，该属性的值为0。

**如何使用：** 调用 `x()` 读取当前值；它不会修改应用状态。

### `[read-only] y : int`

**作用与语义：**

该属性表示小部件相对于其父节点的 y 坐标，包括任意窗口框架。
关于窗口几何问题的概述，请参见 Window Geometry 文档。
默认情况下，该属性的值为0。

**如何使用：** 调用 `y()` 读取当前值；它不会修改应用状态。

### `[explicit] QWidget::QWidget(QWidget *parent = nullptr, Qt::WindowFlags f = Qt::WindowFlags())`

**作用与语义：**

构建一个小部件，该小部件是`parent`的子节点，小部件标志设置为`f`。
如果`parent` `nullptr`，新小部件就变成窗口。如果`parent`是另一个小部件，则该小部件会成为`parent`中的子窗口。当新小部件`parent`被删除时，该小部件也被删除。
控件标志参数`f`通常为0，但可以设置为自定义窗口框架（即必须`parent` `nullptr`）。要自定义框架，使用任意窗口标志的逐位或值组成。
如果你在已经可见的控件上添加子组件，必须明确显示该子组件以使其可见。
注意，X11 版本的 Qt 可能无法在所有系统上提供所有样式标志的组合。这是因为在 X11 上，Qt 只能请求窗口管理器，窗口管理器可以覆盖应用程序的设置。在 Windows 上，Qt 可以设置你想要的任何标志。

### `[virtual noexcept] QWidget::~QWidget()`

**作用与语义：**

毁坏了小部件。
该小部件的所有子节点首先被删除。如果该小部件是主小部件，应用将退出。

### `[virtual protected] void QWidget::actionEvent(QActionEvent *event)`

**作用与语义：**

每当控件的动作发生变化时，该事件处理程序都会被调用给定的`event`。

### `QList<QAction *> QWidget::actions() const`

**作用与语义：**

返回该控件的（可能是空的）动作列表。

### `void QWidget::activateWindow()`

**作用与语义：**

将包含该控件的顶层控件设置为活动窗口。
活动窗口是一个可见的顶层窗口，用于键盘输入焦点。
该函数执行的操作与点击顶层窗口标题栏的鼠标相同。在 X11 上，结果取决于窗口管理器。如果你想确保窗口也叠放在顶部，也应调用 `raise()`。注意窗口必须可见，否则 activateWindow() 无效。
在 Windows 上，如果你调用时应用程序不是当前的激活窗口，那么它不会让它成为激活窗口。它会改变任务栏条目的颜色，表示窗口以某种方式发生了变化。这是因为 Microsoft 不允许应用程序中断用户当前在另一个应用中的操作。

### `void QWidget::addAction(QAction *action)`

**作用与语义：**

将动作`action`附加到该小部件的动作列表中。
所有 QWidgets 都有 `QAction` 的列表。然而，它们可以通过多种不同的图形方式表示。`QAction`列表（由 `actions()` 返回）的默认用途是创建上下文 `QMenu`。
一个`QWidget`应该只有每个动作的一个，添加它已有的动作不会导致同一个动作在小部件中出现两次。
`action`的所有权不会转移给该`QWidget`。

### `[since 6.3] QAction *QWidget::addAction(const QIcon &icon, const QString &text, const QKeySequence &shortcut)`

**作用与语义：**

这些便利功能会创建新的动作，包含文本`text`、图标`icon`和快捷方式，`shortcut`（如果有的话）。
函数会将新创建的动作添加到控件的动作列表中，并返回它。
`QWidget`接管了归还的这`QAction`。

### `[since 6.3] template <typename... Args, typename = QWidget::compatible_action_slot_args<Args...>> QAction *QWidget::addAction(const QIcon &icon, const QString &text, const QKeySequence &shortcut, Args &&... args)`

**作用与语义：**

这些便利功能会创建新的动作，包含文本`text`、图标`icon`和快捷方式，`shortcut`（如果有的话）。
函数会将新创建的动作添加到控件的动作列表中，并返回它。
`QWidget`接管了归还的这`QAction`。

### `[since 6.3] QAction *QWidget::addAction(const QIcon &icon, const QString &text, const QKeySequence &shortcut, const QObject *receiver, const char *member, Qt::ConnectionType type = Qt::AutoConnection)`

**作用与语义：**

这些便利功能会创建新的动作，包含文本`text`、图标`icon`和快捷方式，`shortcut`（如果有的话）。
函数会将新创建的动作添加到控件的动作列表中，并返回它。
`QWidget`接管了归还的这`QAction`。

### `void QWidget::addActions(const QList<QAction *> &actions)`

**作用与语义：**

将`actions`动作附加到该小部件的动作列表中。

### `void QWidget::adjustSize()`

**作用与语义：**

调整小部件大小以适应其内容。
该函数使用 `sizeHint()` 当它有效时，即大小提示的宽度和高度均为 >= 0。否则，它将大小设置为覆盖所有子控件的子矩形（所有子控件矩形的并集）。
对于窗口，屏幕尺寸也会被考虑在内。如果`sizeHint()`小于（200， 100），且尺寸策略为`expanding`，窗口至少会是（200， 100）。窗口的最大尺寸是屏幕宽度和高度的三分之二。

### `QPalette::ColorRole QWidget::backgroundRole() const`

**作用与语义：**

返回小部件的背景角色。
背景角色定义了用于渲染背景的控件中小部件的画笔，`palette`。
如果没有设置显式的后台角色，小部件将继承其父小部件的后台角色。

### `QBackingStore *QWidget::backingStore() const`

**作用与语义：**

返回该控件将被绘制的`QBackingStore`。

### `[virtual protected] void QWidget::changeEvent(QEvent *event)`

**作用与语义：**

该事件处理程序可以重新实现以处理状态变化。
该事件中被更改的状态可以通过提供的`event`检索。
变更事件包括：`QEvent::ToolBarChange`、`QEvent::ActivationChange`、`QEvent::EnabledChange`、`QEvent::FontChange`、`QEvent::StyleChange`、`QEvent::PaletteChange`、`QEvent::WindowTitleChange`、`QEvent::IconTextChange`、`QEvent::ModifiedChange`、`QEvent::MouseTrackingChange`、`QEvent::ParentChange`、`QEvent::WindowStateChange`、`QEvent::LanguageChange`、`QEvent::LocaleChange`、`QEvent::LayoutDirectionChange`、`QEvent::ReadOnlyChange`。

### `QWidget *QWidget::childAt(int x, int y) const`

**作用与语义：**

返回该控件坐标系中位置（`x`， `y`）的可见子组件。如果指定位置没有可见子控件，函数返回`nullptr`。

### `QWidget *QWidget::childAt(const QPoint &p) const`

**作用与语义：**

返回该控件自身坐标系中`p`点的可见子组件。

### `[since 6.8] QWidget *QWidget::childAt(const QPointF &p) const`

**作用与语义：**

返回该控件自身坐标系中`p`点的可见子组件。

### `void QWidget::clearFocus()`

**作用与语义：**

它会从小部件中提取键盘输入的焦点。
如果小部件有活跃焦点，会发送一个焦点输出事件，告诉它失去焦点。
该小部件必须启用焦点设置，才能让键盘输入对焦;也就是说，它必须调用`setFocusPolicy()`。

### `void QWidget::clearMask()`

**作用与语义：**

移除`setMask()`设置的任何遮罩。

### `[slot] bool QWidget::close()`

**作用与语义：**

关闭该控件。如果控件已关闭，返回`true`;否则返回`false`。
首先，它会向小部件发送一个`QCloseEvent`。小部件`accepts`成交事件时`hidden`。如果它`ignores`事件，则不会发生任何事。`QWidget::closeEvent()`的默认实现接受了关闭事件。
如果小部件带有`Qt::WA_DeleteOnClose`标志，小部件也会被删除。无论小部件是否可见，都会向小部件发送关闭事件。
当最后一个可见的主窗口（即没有父窗口）关闭且设置`Qt::WA_QuitOnClose`属性时，`QGuiApplication::lastWindowClosed()`信号会发出。默认情况下，该属性对除瞬时窗口（如启动画面、工具窗口和弹出菜单）外的所有控件都设置为。

### `[virtual protected] void QWidget::closeEvent(QCloseEvent *event)`

**作用与语义：**

当Qt收到来自窗口系统的顶层控件关闭请求时，该事件处理程序会以该`event`调用。
默认情况下，事件被接受，小部件关闭。你可以重新实现这个函数，改变小部件对窗口关闭请求的响应方式。例如，你可以通过调用所有事件中的`ignore()`来阻止窗口关闭。
主窗口应用程序通常会重新实现该函数，以检查用户的工作是否已被保存，并在关闭前请求许可。

### `QMargins QWidget::contentsMargins() const`

**作用与语义：**

contentsMargins 函数返回了小部件的内容边距。

### `QRect QWidget::contentsRect() const`

**作用与语义：**

返回小部件边缘内的区域。

### `[virtual protected] void QWidget::contextMenuEvent(QContextMenuEvent *event)`

**作用与语义：**

该事件处理程序用于事件`event`，可以在子类中重新实现，以接收控件上下文菜单事件。
当控件的 `contextMenuPolicy` `Qt::DefaultContextMenu`时调用处理器。
默认实现忽略上下文事件。详见`QContextMenuEvent`文档。

### `[protected] void QWidget::create(WId window = 0, bool initializeWindow = true, bool destroyOldWindow = true)`

**作用与语义：**

创建一个新的控件窗口。
在Qt 5中，参数`window`、`initializeWindow`和`destroyOldWindow`被忽略。请使用`QWindow::fromWinId()`创建一个`QWindow`包裹外窗口，并转交给`QWidget::createWindowContainer()`。

### `[static] QWidget *QWidget::createWindowContainer(QWindow *window, QWidget *parent = nullptr, Qt::WindowFlags flags = Qt::WindowFlags())`

**作用与语义：**

创建一个`QWidget`，使得将`window`嵌入基于`QWidget`的应用程序成为可能。
窗口容器作为`parent`的子节点创建，并带有窗口旗标`flags`。
一旦窗口嵌入容器中，容器将控制窗口的几何形状和可见性。不建议在嵌入窗口上显式调用`QWindow::setGeometry()`、`QWindow::show()`或`QWindow::hide()`。
容器接管`window`的所有权。窗口可以通过调用`QWindow::setParent()`从窗口容器中移除。
窗口容器作为原生子窗口附加到其子窗口顶层。当窗口容器作为`QAbstractScrollArea`或`QMdiArea`的子窗口使用时，它会为其父链中的每个小部件创建原生窗口，以支持该用例中的正确堆叠和裁剪。为窗口容器创建原生窗口也允许正确的堆叠和裁剪。这必须在展示窗口容器之前完成。拥有许多原生子窗口的应用程序可能会遇到性能问题。
窗户容器存在若干已知的限制：
- 堆叠顺序;嵌入窗口会叠加在控件层级之上，作为一个不透明的盒子。多个重叠窗口容器实例的叠加顺序未定义。
- 渲染集成;窗口容器不与`QGraphicsProxyWidget`、`QWidget::render()`或类似功能互操作。
- 焦点处理;可以让窗口容器实例拥有任意焦点策略，并通过调用`QWindow::requestActivate()`将焦点委托给窗口。然而，从`QWindow`实例返回正常焦点链则取决于`QWindow`实例本身的实现。此外，`QWindow::requestActivate()`是否实际赋予窗口焦点取决于平台。自6.8版本起，如果嵌入基于Qt Quick的窗口，按键操作会在嵌入的QML窗口中切换，允许焦点转移到窗口容器链中下一个或上一个可聚焦对象。
- 在基于`QWidget`的应用中使用大量窗口容器实例会极大影响应用的整体性能。
- 自6.7版本起，如果`window`属于某个控件（即通过调用`windowHandle()`接收到的`window`），则不会创建容器。相反，该函数会在被重新父级化为`parent`后返回控件本身。由于不会创建容器，`flags`将被忽略。换句话说，如果`window`属于控件，考虑直接将该控件重新父级为`parent`，而不是使用该函数。

### `[signal] void QWidget::customContextMenuRequested(const QPoint &pos)`

**作用与语义：**

当小部件的`contextMenuPolicy` `Qt::CustomContextMenu`，且用户请求在小部件上设置右键菜单时，该信号会发出。位置`pos`是小部件接收到的右键菜单事件的位置。通常该事件以小部件坐标为单位。该规则的例外是`QAbstractScrollArea`及其子类，这些子类将右键菜单事件映射到`viewport()`的坐标。

### `[protected] void QWidget::destroy(bool destroyWindow = true, bool destroySubWindows = true)`

**作用与语义：**

释放窗口系统资源。如果`destroyWindow`成立，则销毁小部件窗口。
destroy() 递归调用所有子控件，传递 `destroyWindow` 参数 `destroySubWindows`。为了更好地控制子控件的销毁，先选择性地销毁子控件。
该函数通常由`QWidget`解散器调用。

### `[virtual protected] void QWidget::dragEnterEvent(QDragEnterEvent *event)`

**作用与语义：**

当拖拽进行中且鼠标进入该控件时，调用该事件处理程序。事件通过`event`参数传递。
如果事件被忽略，小部件将不会接收任何拖动动作事件。
请参阅拖放文档，了解如何在申请中提供拖放功能的概览。

### `[virtual protected] void QWidget::dragLeaveEvent(QDragLeaveEvent *event)`

**作用与语义：**

当拖拽进行中且鼠标离开该控件时，调用该事件处理程序。事件通过`event`参数传递。
请参阅拖放文档，了解如何在申请中提供拖放功能的概览。

### `[virtual protected] void QWidget::dragMoveEvent(QDragMoveEvent *event)`

**作用与语义：**

当拖动正在进行中，且发生以下任一条件时，会调用该事件处理程序：光标进入该控件、光标在控件内移动，或在控件拥有焦点时按下键盘上的修饰键。事件通过`event`参数传递。
请参阅拖放文档，了解如何在申请中提供拖放功能的概览。

### `[virtual protected] void QWidget::dropEvent(QDropEvent *event)`

**作用与语义：**

当拖拽该控件时调用该事件处理程序。事件通过 `event` 参数传递。
请参阅拖放文档，了解如何在申请中提供拖放功能的概览。

### `WId QWidget::effectiveWinId() const`

**作用与语义：**

返回该控件的有效窗口系统标识符，即本地父节点的窗口系统标识符。
如果小部件是原生的，该函数返回本地小部件 ID。否则，返回第一个原生父小部件的窗口 ID，即包含该小部件的顶层小部件。
注意：我们建议您不要存储此值，因为它很可能会在运行时发生变化。

### `void QWidget::ensurePolished() const`

**作用与语义：**

确保小部件及其子部件已由 `QStyle` 美化（即具有适当的字体和调色板）。
`QWidget` 会在小部件完全构造后但首次显示前调用此函数。如果你想在进行某个操作之前确保小部件已美化，可以调用此函数，例如，在小部件的 `sizeHint()` 重实现中可能需要正确的字体大小。请注意，此函数在 `sizeHint()` 的默认实现中被调用。
美化对于必须在所有构造函数（包括基类和子类的构造函数）调用之后进行的最终初始化非常有用。
如果你需要在小部件被美化时更改某些设置，请重新实现 `event()` 并处理 `QEvent::Polish` 事件类型。
注意：该函数被声明为 const，因此可以从其他 const 函数中调用（例如 `sizeHint()`）。

### `[virtual protected] void QWidget::enterEvent(QEnterEvent *event)`

**作用与语义：**

该事件处理程序可以在子类中重新实现，以接收通过 `event` 参数传递的控件进入事件。
当鼠标光标进入控件时，会发送一个事件到控件。

### `[override virtual protected] bool QWidget::event(QEvent *event)`

**作用与语义：**

重实现自：`QObject::event`（QEvent *e）。
这是主事件处理程序;它处理事件`event`。你可以在子类中重新实现这个函数，但我们建议使用专门的事件处理程序。
按键按下和释放事件与其他事件有不同的处理方式。event() 检查 Tab 和 Shift Tab，并尝试正确移动焦点。如果没有控件可移动焦点（或按键不是 Tab 或 Shift Tab），event() 会调用 `keyPressEvent()`。
鼠标和平板事件处理也稍有特殊：只有当小部件`enabled`时，event() 才会调用专用处理程序，如 `mousePressEvent()`;否则会丢弃事件。
如果事件被识别，该函数返回`true`，否则返回`false`。如果识别事件被接受（见 `QEvent::accepted`），任何后续处理，如向父控件的事件传播，都会停止。

### `[static] QWidget *QWidget::find(WId id)`

**作用与语义：**

返回一个指向控件的指针，带有窗口标识符/句柄`id`。
窗口标识符类型取决于底层窗口系统，具体定义请参见 `qwindowdefs.h`。如果没有带有该标识符的小部件，则返回`nullptr`。

### `[virtual protected] void QWidget::focusInEvent(QFocusEvent *event)`

**作用与语义：**

此事件处理程序可以在子类中重新实现，以接收部件的键盘焦点事件（获得焦点）。事件通过 `event` 参数传入。
部件通常必须 `setFocusPolicy()` 到除 `Qt::NoFocus` 以外的内容才能接收焦点事件。（注意，应用程序程序员可以在任何部件上调用 `setFocus()`，即使这些部件通常不接受焦点。）。
默认实现会更新部件（不包括未指定 `focusPolicy()` 的窗口）。

### `[protected] bool QWidget::focusNextChild()`

**作用与语义：**

根据 Tab 的需要，找到一个新的控件来给键盘置重点，如果能找到新控件就返回 `true`，找不到则返回 false。

### `[virtual protected] bool QWidget::focusNextPrevChild(bool next)`

**作用与语义：**

根据 Tab 和 Shift Tab 的需要，找到一个新的控件来给键盘置换焦点，如果能找到新控件，则返回 `true`，找不到则返回 false。
如果`next`为真，该函数向前搜索;如果`next`为假，则向后搜索。
有时，你会想重新实现这个函数。例如，浏览器可能会重新实现它，将“当前活跃链接”向前或向后移动，只有当它到达“页面”的最后或第一个链接时才调用 focusNextPrevChild()。
子控件调用其父控件的 focusNextPrevChild()，但只有包含子控件的窗口决定将焦点重定向到哪里。通过重新实现该函数，你就能控制所有子控件的焦点遍历。

### `[virtual protected] void QWidget::focusOutEvent(QFocusEvent *event)`

**作用与语义：**

该事件处理程序可以在子类中重新实现，以接收控件的键盘焦点事件（焦点丢失）。事件通过`event`参数传递。
小部件通常必须`setFocusPolicy()`到非`Qt::NoFocus`的对象才能接收焦点事件。（注意，应用程序员可以调用任何小部件的 `setFocus()`，即使是那些通常不接受焦点的控件。）。
默认实现会更新小部件（除非是没有指定`focusPolicy()`的窗口）。

### `[protected] bool QWidget::focusPreviousChild()`

**作用与语义：**

根据 Shift Tab 的需要，找到一个新的控件来赋予键盘焦点，如果能找到新控件，则返回 `true`;找不到则返回 false。

### `QWidget *QWidget::focusProxy() const`

**作用与语义：**

返回焦点代理，或者如果没有焦点代理则返回`nullptr`。

### `QWidget *QWidget::focusWidget() const`

**作用与语义：**

返回该控件的最后一个子节点，`setFocus`被调用。对于顶级控件，如果该窗口被激活，该控件将被聚焦。
这与`QApplication::focusWidget()`不同，后者会返回当前激活窗口中的焦点控件。

### `QFontInfo QWidget::fontInfo() const`

**作用与语义：**

返回小部件当前字体的字体信息。相当于`QFontInfo(widget->font())`。

### `QFontMetrics QWidget::fontMetrics() const`

**作用与语义：**

返回小部件当前字体的字体度量。相当于`QFontMetrics(widget->font())`。

### `QPalette::ColorRole QWidget::foregroundRole() const`

**作用与语义：**

回归前景角色。
前景角色定义了用于绘制前景的控件的颜色`palette`。
如果没有明确设置前景角色，函数返回的角色与背景角色对比。

### `[invokable] QPixmap QWidget::grab(const QRect &rectangle = QRect(QPoint(0, 0), QSize(-1, -1)))`

**作用与语义：**

将小部件渲染成受限于特定`rectangle`的像素贴图。如果小部件有子节点，则它们也会被绘制在相应位置。
如果指定了一个大小为无效的矩形（默认），则整个控件都会被涂装。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `void QWidget::grabGesture(Qt::GestureType gesture, Qt::GestureFlags flags = Qt::GestureFlags())`

**作用与语义：**

订阅该小部件到特定有特定`flags`的`gesture`。

### `void QWidget::grabKeyboard()`

**作用与语义：**

接键盘输入。
该控件接收所有键盘事件，直到`releaseKeyboard()`被调用;其他控件则完全没有键盘事件。鼠标事件不受影响。如果你想抓取，可以用`grabMouse()`。
焦点控件不受影响，但不会接收任何键盘事件。`setFocus()` 按常规移动焦点，但新的焦点控件只有在调用 `releaseKeyboard()` 后才接收键盘事件。
如果当前有不同的小部件抓取键盘输入，该小部件的抓取会优先释放。

### `void QWidget::grabMouse()`

**作用与语义：**

抓取鼠标输入。
这个小部件会接收所有鼠标事件，直到`releaseMouse()`被调用;其他小部件则完全没有鼠标事件。键盘事件不受影响。如果你想抓取，可以用`grabKeyboard()`。
警告：抓取鼠标应用中的漏洞经常导致终端卡死。使用此功能时务必谨慎，调试时考虑使用`-nograb`命令行选项。
使用 Qt 时很少需要抓握鼠标，因为 Qt 会合理地抓取和释放鼠标。特别是，Qt 在按下鼠标按钮时抓住鼠标，并一直保持直到最后一个按钮松开。
注意：只有可见的小部件可以抓取鼠标输入。如果`isVisible()`返回`false`，该小部件无法调用 grabMouse()。
注意：在 Windows 上，grabMouse() 只有在鼠标处于进程拥有的窗口内时才有效。在 macOS 上，grabMouse() 只有在鼠标处于该控件框架内时才有效。

### `void QWidget::grabMouse(const QCursor &cursor)`

**作用与语义：**

抓取鼠标输入并改变光标形状。
光标会保持形状 `cursor`（只要鼠标焦点被抓取），该小部件将是唯一接收鼠标事件的部件，直到调用`releaseMouse()`()。
警告：抓鼠标可能会锁死终端。
注意：请参见`QWidget::grabMouse()`注释。
注意：该功能会超载`QWidget::grabMouse()`。

### `int QWidget::grabShortcut(const QKeySequence &key, Qt::ShortcutContext context = Qt::WindowShortcut)`

**作用与语义：**

为Qt的快捷方式系统添加一个快捷方式，用于监控给定`context`中的给定`key`序列。如果`context`是`Qt::ApplicationShortcut`，捷径则适用于整个应用程序。否则，捷径要么是本地于该控件，`Qt::WidgetShortcut`，要么本地于窗口，`Qt::WindowShortcut`。
如果同一个`key`序列被多个控件抓取，当`key`序列出现时，会以非确定性顺序向所有适用该控件发送`QEvent::Shortcut`事件，但“模糊”标志设置为true。
警告：通常你不需要使用这个函数;如果你还想要相应的菜单选项和工具栏按钮，可以创建带有快捷键序列的`QAction`，或者如果你只需要按键序列，可以创建`QShortcut`。`QAction`和`QShortcut`都能帮你处理所有事件过滤，并提供当用户触发按键序列时触发的信号，因此比这个低层函数更容易使用。

### `QGraphicsEffect *QWidget::graphicsEffect() const`

**作用与语义：**

graphicsEffect 函数返回了指向小部件图形效果的指针。
如果小部件没有图形效果，`nullptr`会返回。

### `QGraphicsProxyWidget *QWidget::graphicsProxyWidget() const`

**作用与语义：**

返回图形视图中对应嵌入控件的代理控件;否则返回`nullptr`。

### `bool QWidget::hasEditFocus() const`

**作用与语义：**

如果该小部件当前有编辑焦点，返回`true`;否则为假。
该功能仅在 Qt for Embedded Linux 中提供。

### `[virtual] bool QWidget::hasHeightForWidth() const`

**作用与语义：**

如果小部件的首选高度取决于宽度，则返回`true`;否则返回`false`。

### `[virtual] int QWidget::heightForWidth(int w) const`

**作用与语义：**

返回该小部件的首选高度，基于宽度`w`。
如果该控件有布局，默认实现返回该布局的首选高度。如果没有布局，默认实现返回 -1，表示首选高度不依赖于宽度。

### `[slot] void QWidget::hide()`

**作用与语义：**

隐藏小部件。该函数等价于`setVisible`（false）。
注意：如果你正在使用`QDialog`或其子类，并且在该函数后调用`show()`函数，对话框将显示在原始位置。

### `[virtual protected] void QWidget::hideEvent(QHideEvent *event)`

**作用与语义：**

该事件处理程序可以被子类重新实现，以接收控件隐藏事件。事件通过`event`参数传递。
隐藏事件会在小部件被隐藏后立即发送。
注意：当窗口系统改变小部件的映射状态时，会接收自发显示和隐藏事件，例如用户最小化窗口时自发隐藏事件，窗口恢复时自发显示事件。收到自发隐藏事件后，小部件仍被视为可见，意义`isVisible()`。

### `[override virtual protected] void QWidget::initPainter(QPainter *painter) const`

**作用与语义：**

将`painter`笔、背景和字体初始化为与给定控件相同的格式。当画家在`QWidget`上打开时，该函数会自动调用。

### `[virtual protected] void QWidget::inputMethodEvent(QInputMethodEvent *event)`

**作用与语义：**

该事件处理程序对于事件`event`，可以在子类中重新实现以接收输入法组合事件。当输入方法状态发生变化时，调用该处理程序。
注意，在创建自定义文本编辑小部件时，必须明确设置`Qt::WA_InputMethodEnabled`窗口属性（使用`setAttribute()`函数）才能接收输入法事件。
默认实现调用 event->ignore()，该事件拒绝输入法事件。详情请参见 `QInputMethodEvent` 文档。

### `[virtual] QVariant QWidget::inputMethodQuery(Qt::InputMethodQuery query) const`

**作用与语义：**

该方法仅适用于输入控件。输入方法用于查询控件的一组属性，以支持复杂的输入法操作，以支持周围文本和重新转换。
`query` 指定查询的属性。

### `void QWidget::insertAction(QAction *before, QAction *action)`

**作用与语义：**

在该动作`before`之前，将动作`action`插入该控件的动作列表。如果`before`是`nullptr`或`before`不是该控件的有效动作，则会附加该动作。
一个`QWidget`应该每种动作都只有一个。

### `void QWidget::insertActions(QAction *before, const QList<QAction *> &actions)`

**作用与语义：**

在该控件的动作`before`之前，将`actions`动作插入该控件的动作列表。如果`before`是`nullptr`或`before`不是该控件的有效动作，则会附加该动作。
一个`QWidget`最多只能有每种动作的一次。

### `bool QWidget::isAncestorOf(const QWidget *child) const`

**作用与语义：**

如果该小部件是给定`child`的父组件（或祖父级等），且两个小部件在同一窗口内，则返回`true`;否则返回`false`。

### `bool QWidget::isEnabledTo(const QWidget *ancestor) const`

**作用与语义：**

返回`true`如果启用`ancestor`该小部件是否会被启用;否则返回`false`。
如果小部件本身和除除 `ancestor` 以外的所有父节点都没有被明确禁用，那就是这种情况。
如果该控件或其祖先被明确禁用，isEnabledTo（0） 返回 false。
这里的“祖先”指的是同一窗口中的父控件。
因此，isEnabledTo（0） 停止在该控件的窗口，而 `isEnabled()` 则考虑父窗口。

### `bool QWidget::isHidden() const`

**作用与语义：**

如果控件被隐藏，返回`true`，否则返回`false`。
隐藏小部件只有在调用`show()`时才会被看到。当父控件被显示时，它不会自动显示。
要检查可见性，请使用！`isVisible()`（注意感叹号）。
isHidden() 意味着 ！`isVisible()`，但一个小部件可以同时不可见且不隐藏。这适用于那些不可见小部件的子组件。
小部件在以下情况下被隐藏：
- 它们被创建为独立的窗户，
- 它们是由可见控件创建的子体，
- `hide()`或`setVisible`（假）被判定。

### `bool QWidget::isVisibleTo(const QWidget *ancestor) const`

**作用与语义：**

返回`true`该控件在显示`ancestor`时是否可见;否则返回`false`。
真正的情况是，如果小部件本身或除排除`ancestor`之外的任何父节点都没有被明确隐藏。
如果控件被屏幕其他窗口遮挡，该函数仍会返回true，但如果要移动它或它们，它可能会在物理上可见。
isVisibleTo（0） 与 `isVisible()` 相同。

### `bool QWidget::isWindow() const`

**作用与语义：**

如果小部件是独立窗口，返回`true`，否则返回`false`。
窗口是一个小部件，视觉上不是其他小部件的子，通常带有框架和窗口标题。
窗口可以有一个父控件。然后它会与父节点分组，当父节点被删除时删除，最小化父节点时也被最小化，等等。如果窗口管理器支持，它还会与父节点有共同的任务栏条目。
`QDialog`和`QMainWindow`小部件默认都是窗口，即使构造函数中指定了父小部件。这种行为由`Qt::Window`标志指定。

### `[virtual protected] void QWidget::keyPressEvent(QKeyEvent *event)`

**作用与语义：**

该事件处理程序用于事件`event`，可以在子类中重新实现，以接收该控件的按键事件。
小部件必须先调用`setFocusPolicy()`接受焦点，并且拥有焦点才能接收按键事件。
如果你重新实现这个处理器，如果你不对密钥进行操作，务必调用基类实现。
默认实现会关闭弹出式小部件，如果用户按下`QKeySequence::Cancel`的按键序列（通常是Escape键）。否则该事件会被忽略，以便小部件的父节点能够解释。
注意`QKeyEvent`以isAccepted() == true开头，所以你不需要调用`QKeyEvent::accept()`——只要你对该密钥执行时不要调用基类实现即可。

### `[virtual protected] void QWidget::keyReleaseEvent(QKeyEvent *event)`

**作用与语义：**

该事件处理程序用于事件`event`，可以在子类中重新实现，以接收该小部件的密钥释放事件。
小部件必须先接受焦点并拥有焦点，才能接收密钥释放事件。
如果你重新实现这个处理器，如果你不对密钥进行操作，务必调用基类实现。
默认实现忽略事件，以便小部件的父节点能够解释事件。
注意`QKeyEvent`以 isAccepted() == true 开头，所以你不需要调用 `QKeyEvent::accept()`——只要你对密钥执行时不要调用基类实现即可。

### `[static] QWidget *QWidget::keyboardGrabber()`

**作用与语义：**

返回当前抓取键盘输入的小部件。
如果该应用中没有小部件正在抓键盘，`nullptr`返回。

### `QLayout *QWidget::layout() const`

**作用与语义：**

返回安装在该小部件上的布局管理器，或者如果未安装布局管理器，则返回`nullptr`。
布局管理器会设置已添加到布局中的小部件子节点的几何体。

### `[virtual protected] void QWidget::leaveEvent(QEvent *event)`

**作用与语义：**

该事件处理程序可以在子类中重新实现，以接收通过 `event` 参数传递的控件离开事件。
当鼠标光标离开控件时，会向控件发送一个离开事件。

### `[slot] void QWidget::lower()`

**作用与语义：**

将小部件降到父小部件栈的底部。
调用后，控件将视觉上落后于任何重叠的兄弟控件，因此被遮挡。

### `[since 6.0] QPointF QWidget::mapFrom(const QWidget *parent, const QPointF &pos) const`

**作用与语义：**

将控件坐标`pos`从`parent`的坐标系转换为该控件的坐标系。`parent`不能`nullptr`，且必须是调用控件的父节点。

### `QPoint QWidget::mapFrom(const QWidget *parent, const QPoint &pos) const`

**作用与语义：**

将控件坐标`pos`从`parent`的坐标系转换为该控件的坐标系。`parent`不能`nullptr`，且必须是调用控件的父节点。

### `[since 6.0] QPointF QWidget::mapFromGlobal(const QPointF &pos) const`

**作用与语义：**

将全局屏幕坐标`pos`转换为控件坐标。

### `QPoint QWidget::mapFromGlobal(const QPoint &pos) const`

**作用与语义：**

将全局屏幕坐标`pos`转换为控件坐标。

### `[since 6.0] QPointF QWidget::mapFromParent(const QPointF &pos) const`

**作用与语义：**

将父控件坐标`pos`转换为控件坐标。
如果小部件没有父组件`mapFromGlobal()`也是一样。

### `QPoint QWidget::mapFromParent(const QPoint &pos) const`

**作用与语义：**

将父控件坐标`pos`转换为控件坐标。
如果小部件没有父组件`mapFromGlobal()`也是一样。

### `[since 6.0] QPointF QWidget::mapTo(const QWidget *parent, const QPointF &pos) const`

**作用与语义：**

将控件坐标`pos`转换为`parent`的坐标系。`parent`不能是`nullptr`的，且必须是调用控件的父节点。

### `QPoint QWidget::mapTo(const QWidget *parent, const QPoint &pos) const`

**作用与语义：**

将控件坐标`pos`转换为`parent`的坐标系。`parent`不能是`nullptr`的，且必须是调用控件的父节点。

### `[since 6.0] QPointF QWidget::mapToGlobal(const QPointF &pos) const`

**作用与语义：**

将小部件坐标`pos`转换为全局屏幕坐标。例如，`mapToGlobal(QPointF(0,0))`给出小部件左上角像素的全局坐标。

### `QPoint QWidget::mapToGlobal(const QPoint &pos) const`

**作用与语义：**

将小部件坐标`pos`转换为全局屏幕坐标。例如，`mapToGlobal(QPointF(0,0))`给出小部件左上角像素的全局坐标。

### `[since 6.0] QPointF QWidget::mapToParent(const QPointF &pos) const`

**作用与语义：**

将控件坐标`pos`转换为父控件中的坐标。
如果小部件没有父组件，`mapToGlobal()`也是一样。

### `QPoint QWidget::mapToParent(const QPoint &pos) const`

**作用与语义：**

将控件坐标`pos`转换为父控件中的坐标。
如果小部件没有父组件，`mapToGlobal()`也是一样。

### `QRegion QWidget::mask() const`

**作用与语义：**

返回当前在控件上设置的遮罩。如果没有设置遮罩，返回值将是空区域。

### `[override virtual protected] int QWidget::metric(QPaintDevice::PaintDeviceMetric m) const`

**作用与语义：**

重实现自：`QPaintDevice::metric`（QPaintDevice：:P aintDeviceMetric metric） const.
虚拟`QPaintDevice::metric()`功能的内部实现。
`m`是必须获得的指标。

### `[virtual protected] void QWidget::mouseDoubleClickEvent(QMouseEvent *event)`

**作用与语义：**

该事件处理程序用于事件`event`，可以重新实现为子类，以接收小部件的鼠标双击事件。
默认实现调用`mousePressEvent()`。
注意：该小部件除了双击事件外，还会接收鼠标按键和鼠标释放事件。如果与该小部件重叠的其他小部件在新闻发布事件后消失，则该小部件只会接收双击事件。开发者有责任确保应用程序正确解读这些事件。

### `[static] QWidget *QWidget::mouseGrabber()`

**作用与语义：**

返回当前抓取鼠标输入的小部件。
如果该应用中没有小部件抓取鼠标，`nullptr`返回。

### `[virtual protected] void QWidget::mouseMoveEvent(QMouseEvent *event)`

**作用与语义：**

该事件处理程序用于事件`event`，可以在子类中重新实现，以接收该控件的鼠标移动事件。
如果关闭鼠标追踪，只有在鼠标移动过程中按下鼠标按钮时才会发生鼠标移动事件。如果开启鼠标追踪，即使未按键，鼠标移动事件也会发生。
`QMouseEvent::position()`报告鼠标光标相对于该控件的位置。对于按下和释放事件，位置通常与最后一次鼠标移动事件的位置相同，但如果用户手抖动，可能会有所不同。这是底层窗口系统的功能，而非Qt。
如果你想在鼠标移动时立即显示提示（例如，获取鼠标坐标与`QMouseEvent::position()`并显示为提示），你必须先启用上述的鼠标追踪功能。然后，为了确保提示立即更新，你必须在鼠标MoveEvent()实现中调用`QToolTip::showText()`而不是`setToolTip()`。

### `[virtual protected] void QWidget::mousePressEvent(QMouseEvent *event)`

**作用与语义：**

该事件处理程序用于事件`event`，可以重新实现为子类，以接收该小部件的鼠标按键事件。
如果你在 mousePressEvent() 创建新控件，`mouseReleaseEvent()`可能不会到达你预期的位置，这取决于底层窗口系统（或 X11 窗口管理器）、控件的位置，甚至可能还有其他因素。
默认实现实现了当你点击窗口外时关闭弹出小部件的功能。对于其他小部件类型，它没有任何作用。

### `[virtual protected] void QWidget::mouseReleaseEvent(QMouseEvent *event)`

**作用与语义：**

该事件处理程序用于事件`event`，可以重新实现为子类，以接收小部件的鼠标释放事件。

### `void QWidget::move(int x, int y)`

**作用与语义：**

该属性表示该控件在其父控件中的位置。
如果小部件是窗口，则该小部件在桌面上的位置，包括其框架。
当调整位置时，如果控件可见，会立即接收移动事件（`moveEvent()`）。如果控件当前不可见，则保证在显示前收到事件。
默认情况下，该属性包含指向原点的位置。
警告：在 `moveEvent()` 内调用 move() 或 `setGeometry()` 可能导致无限递归。
关于窗口几何问题的概述，请参见 Window Geometry 文档。
注意：并非所有窗口系统都支持设置或查询顶层窗口位置。在此类系统中，程序移动窗口可能无效，且当前位置（如`QPoint(0, 0)`）可能会返回人工值。

**如何使用：** 调用 `move()` 读取当前值；它不会修改应用状态。

### `[virtual protected] void QWidget::moveEvent(QMoveEvent *event)`

**作用与语义：**

该事件处理程序可以在子类中重新实现，以接收通过 `event` 参数传递的小部件移动事件。当小部件接收到该事件时，它已经处于新位置。
旧位置可通过`QMoveEvent::oldPos()`进入。

### `[virtual protected] bool QWidget::nativeEvent(const QByteArray &eventType, void *message, qintptr *result)`

**作用与语义：**

该特殊事件处理程序可在子类中重新实现，以接收由`eventType`识别的本地平台事件，这些事件通过`message`参数传递。
在你重新实现该函数时，如果你想停止事件被 Qt 处理，返回 true 并设为 `result`。`result` 参数仅在 Windows 上有意义。如果你返回 false，这个原生事件会传回给 Qt，Qt 将事件转换成 Qt 事件并发送给控件。
注意：只有当该控件具有本地窗口句柄时，事件才会传递到该事件处理程序。
注意：该函数对Qt 4的事件过滤函数x11Event()、winEvent()和macEvent()进行了超种。
- `Platform`：事件类型标识符;消息类型;结果类型
- `Windows`：“windows_generic_MSG”;MSG *;LRESULT
- `macOS`：“NSEvent”;NSEvent *
- `XCB`：“xcb_generic_event_t”;xcb_generic_event_t *

### `QWidget *QWidget::nativeParentWidget() const`

**作用与语义：**

返回该控件的原生父节点，即下一个带有系统标识符的祖先控件;如果没有任何本地父节点，则返回`nullptr`。

### `QWidget *QWidget::nextInFocusChain() const`

**作用与语义：**

返回该控件焦点链中的下一个控件。

### `void QWidget::overrideWindowFlags(Qt::WindowFlags flags)`

**作用与语义：**

将小部件的窗口标志设置为`flags`，但不告诉窗口系统。
警告：除非你非常了解自己在做什么，否则不要调用这个函数。

### `[override virtual] QPaintEngine *QWidget::paintEngine() const`

**作用与语义：**

重实现自：`QPaintDevice::paintEngine()` const.
返回控件的绘图引擎。
注意，用户不应明确调用该函数，因为它仅用于重构目的。该函数由 Qt 内部调用，默认实现不一定总是返回有效指针。

### `[virtual protected] void QWidget::paintEvent(QPaintEvent *event)`

**作用与语义：**

该事件处理程序可以在子类中重新实现，以接收 `event` 传递的绘画事件。
绘图事件是请求重新绘制一个小部件的全部或部分。它可能由以下原因之一发生：
- `repaint()`或`update()`被援引，
- 小部件被遮挡，现已被发现，或
- 还有很多其他原因。
许多控件可以在被要求时重新绘制整个表面，但有些慢速控件需要通过只绘制请求的区域来优化：`QPaintEvent::region()`。这种速度优化不会改变结果，因为在事件处理过程中绘制会被裁剪到该区域。例如，`QListView`和`QTableView`就是这样做的。
Qt 还试图通过将多个绘画事件合并为一个来加快绘画速度。当 `update()` 被多次调用或窗口系统发送多个绘画事件时，Qt 会将这些事件合并为一个区域更大的事件（参见 `QRegion::united()`）。`repaint()`函数不支持这种优化，因此我们建议尽可能使用 `update()`。
当绘制事件发生时，更新区域通常已经被擦除，所以你是在小部件的背景上作画。
背景可以用`setBackgroundRole()`和`setPalette()`设置。
自 Qt 4.0 起，`QWidget` 会自动双缓冲绘制，因此无需在 paintEvent() 中编写双缓冲代码以避免闪烁。
注意：通常，你应避免在 paintEvent() 中调用 `update()` 或 `repaint()`。例如，在 paintEvent() 中调用 `update()` 或 `repaint()` 会导致行为不明确;孩子可能会也可能不会获得绘画事件。
警告：如果你使用没有 Qt 的 backingstore 的自定义 paint 引擎，`Qt::WA_PaintOnScreen` 必须设置。否则，`QWidget::paintEngine()` 永远不会被调用;将会被使用 backingstore 来替代。

### `QWidget *QWidget::parentWidget() const`

**作用与语义：**

返回该小部件的父部件，如果没有子部件则返回`nullptr`。

### `QWidget *QWidget::previousInFocusChain() const`

**作用与语义：**

前述InFocusChain函数返回该控件焦点链中的前一个控件。

### `[slot] void QWidget::raise()`

**作用与语义：**

将该小部件提升到父小部件栈的顶端。
调用后，控件会在视觉上出现在所有重叠的兄弟控件前面。
注意：使用`activateWindow()`时，你可以调用该函数以确保窗口叠加在顶部。

### `void QWidget::releaseKeyboard()`

**作用与语义：**

松开抓键盘。

### `void QWidget::releaseMouse()`

**作用与语义：**

松开鼠标抓取。

### `void QWidget::releaseShortcut(int id)`

**作用与语义：**

从 Qt 的快捷方式系统中移除该快捷方式的该`id`。小部件将不再接收快捷方式按键序列的 `QEvent::Shortcut` 事件（除非它有其他具有相同按键序列的快捷方式）。
警告：通常不需要使用该函数，因为 Qt 的快捷方式系统在父控件被破坏时会自动移除快捷方式。最好使用`QAction`或`QShortcut`来处理快捷方式，因为它们比这个底层函数更易使用。另外请注意，这是一个昂贵的操作。

### `void QWidget::removeAction(QAction *action)`

**作用与语义：**

将该动作`action`从该小部件的操作列表中移除。

### `void QWidget::render(QPaintDevice *target, const QPoint &targetOffset = QPoint(), const QRegion &sourceRegion = QRegion(), QWidget::RenderFlags renderFlags = RenderFlags(DrawWindowBackground | DrawChildren))`

**作用与语义：**

用`renderFlags`来确定如何渲染，将该小部件的`sourceRegion`渲染到`target`中。渲染从`target`的`targetOffset`开始。例如：
如果`sourceRegion`是空区域，该函数将使用`QWidget::rect()`作为区域，即整个小部件。
渲染前务必调用`QPainter::end()` `target`设备的激活绘图器（如果有的话）。例如：
注意：要获取`QOpenGLWidget`内容，请使用`QOpenGLWidget::grabFramebuffer()`。

**官方示例：**

```cpp
 QPixmap pixmap(widget->size());
 widget->render(&pixmap);
```

### `void QWidget::render(QPainter *painter, const QPoint &targetOffset = QPoint(), const QRegion &sourceRegion = QRegion(), QWidget::RenderFlags renderFlags = RenderFlags(DrawWindowBackground | DrawChildren))`

**作用与语义：**

将小部件渲染到`painter`的 `QPainter::device()`。
渲染时会使用对`painter`施加的变换和设置。
注意：`painter`必须处于激活状态。在macOS中，小部件会被渲染成`QPixmap`，然后由`painter`绘制。

### `[slot] void QWidget::repaint()`

**作用与语义：**

除非禁用更新或隐藏控件，否则会立即调用`paintEvent()`直接重新绘制控件。
我们建议只有在需要立即重新绘制时才使用 repaint()，比如在动画过程中。在大多数情况下，`update()` 更好，因为它允许 Qt 优化速度并减少闪烁。
警告：如果你调用一个函数，而函数本身也可以从`paintEvent()`调用，可能会出现无限递归。`update()`函数从不引发递归。
注意：该槽位已超载。连接该槽位：


使用 qOverload 连接：
connect（sender， &SenderClass：：signal，。
widget， qOverload<>（&QWidget：：repaint））;

或者用lambda作为包装器：
connect（sender， &SenderClass：：signal，。
控件，[接收器 = 控件]() { 接收器>repaint(); }）;


更多示例和方法，请参见连接超载槽位。

### `void QWidget::repaint(const QRect &rect)`

**作用与语义：**

该版本在控件内部重新绘制一个矩形`rect`。

### `void QWidget::repaint(const QRegion &rgn)`

**作用与语义：**

该版本在控件内部重新绘制区域`rgn`。

### `void QWidget::repaint(int x, int y, int w, int h)`

**作用与语义：**

该版本在控件内部重新绘制一个矩形（`x`、`y`、`w`、`h`）。
如果`w`为负，则用`width() - x`替代;如果`h`为负，则以宽度`height() - y`替换。

### `void QWidget::resize(int w, int h)`

**作用与语义：**

该属性表示了小部件的大小，但不包括任何窗口框。
如果控件在调整大小时可见，则会立即收到一个调整大小事件（`resizeEvent()`）。如果控件当前不可见，则保证在显示前收到事件。
如果尺寸超出`minimumSize()`和`maximumSize()`定义范围，则调整。
默认情况下，该属性包含一个取决于用户平台和屏幕几何形状的值。
警告：在 `resizeEvent()` 内调用 resize() 或 `setGeometry()` 可能导致无限递归。
注意：将大小设置为`QSize(0, 0)`会导致小部件不会出现在屏幕上。这同样适用于Windows。

**如何使用：** 调用 `resize()` 读取当前值；它不会修改应用状态。

### `[virtual protected] void QWidget::resizeEvent(QResizeEvent *event)`

**作用与语义：**

该事件处理程序可以被重新实现为子类，以接收通过 `event` 参数传递的控件大小调整事件。当调用 resizeEvent() 时，控件已经拥有新的几何体。旧的大小可以通过 `QResizeEvent::oldSize()` 访问。
控件会被擦除，并在处理调整尺寸事件后立即接收绘图事件。不需要（也不应该）在这个处理程序中进行绘图。

### `bool QWidget::restoreGeometry(const QByteArray &geometry)`

**作用与语义：**

恢复存储在字节数组中的顶层控件的几何体和状态`geometry`。成功时返回`true`;否则返回`false`。
如果恢复后的几何体位于屏幕外，则会修改为在可用的屏幕几何体内。
要恢复使用`QSettings`保存的几何体，可以使用以下代码：
关于窗口几何问题的概述，请参见 Window Geometry 文档。
用`QMainWindow::restoreState()`恢复工具栏和底座小部件的几何体和状态。

**官方示例：**

```cpp
 QSettings settings("MyCompany", "MyApp");
 myWidget->restoreGeometry(settings.value("myWidget/geometry").toByteArray());
```

### `QByteArray QWidget::saveGeometry() const`

**作用与语义：**

保存顶级控件当前的几何体和状态。
为了在窗口关闭时保存几何体，你可以实现类似这样的关闭事件：
关于窗口几何问题的概述，请参见 Window Geometry 文档。
用`QMainWindow::saveState()`保存工具栏和底座小部件的几何体和状态。

**官方示例：**

```cpp
 void MyWidget::closeEvent(QCloseEvent *event)
 {
     QSettings settings("MyCompany", "MyApp");
     settings.setValue("geometry", saveGeometry());
     QWidget::closeEvent(event);
 }
```

### `QScreen *QWidget::screen() const`

**作用与语义：**

返回小部件所在的屏幕。

### `void QWidget::scroll(int dx, int dy)`

**作用与语义：**

向右滚动小部件及其子节点，向右`dx`向下`dy`像素。`dx`和`dy`都可能是负数。
滚动后，控件会接收需要重新绘制区域的绘画事件。对于Qt已知不透明的小部件，这仅是新曝光的部分。例如，如果一个不透明的小部件向左滚动8像素，只需更新右侧8像素宽的条纹。
由于控件默认传播父节点的内容，你需要设置`autoFillBackground`属性，或者用`setAttribute()`设置`Qt::WA_OpaquePaintEvent`属性，才能使控件变得不透明。
对于使用内容传播的小工具，滚动会导致整个滚动区域的更新。

### `void QWidget::scroll(int dx, int dy, const QRect &r)`

**作用与语义：**

该版本仅滚动`r`，不移动小部件的子节点。
如果`r`空或无效，则结果未定义。

### `void QWidget::setAttribute(Qt::WidgetAttribute attribute, bool on = true)`

**作用与语义：**

如果该控件为真，则设置该控件上的属性`attribute` `on`;否则清除该属性。

### `void QWidget::setBackgroundRole(QPalette::ColorRole role)`

**作用与语义：**

将小部件的背景角色设置为`role`。
背景角色定义了小部件`palette`中的画笔，用于渲染背景。
如果`role` `QPalette::NoRole`，则小部件继承父节点的背景角色。
请注意，样式可以自由选择调色板中的任何颜色。如果用 setBackgroundRole() 达不到想要的结果，可以修改调色板或设置样式表。

### `void QWidget::setBaseSize(int basew, int baseh)`

**作用与语义：**

该属性包含控件的基准大小。
如果控件定义了`sizeIncrement()`，则使用基准大小来计算合适的控件大小。
默认情况下，对于新创建的控件，该属性包含宽度和高度为零的大小。

**如何使用：** 调用 `setBaseSize(...)` 修改 `baseSize`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QWidget::setContentsMargins(int left, int top, int right, int bottom)`

**作用与语义：**

将控件内容周围的边距设置为`left`、`top`、`right`和`bottom`。边距用于布局系统，子类也可用来指定绘制区域（例如排除框架）。
改变边际会触发`resizeEvent()`。

### `void QWidget::setContentsMargins(const QMargins &margins)`

**作用与语义：**

setContentsMargins 函数设置了控件内容周围的边距。
设置控件内容周围的边距，其大小由`margins`决定。边距用于布局系统，子类也可用来指定绘制区域（例如排除画框）。
改变边际会触发`resizeEvent()`。

### `[slot] void QWidget::setDisabled(bool disable)`

**作用与语义：**

如果`disable`为真，则禁用控件的输入事件;否则启用输入事件。
更多信息请参见`enabled`文档。

### `void QWidget::setEditFocus(bool enable)`

**作用与语义：**

如果`enable`成立，则使该小部件具有编辑焦点，这样`Qt::Key_Up`和`Qt::Key_Down`将正常传递到小部件;否则，`Qt::Key_Up`和`Qt::Key_Down`用于切换焦点。
该功能仅在 Qt for Embedded Linux 中提供。

### `void QWidget::setFixedHeight(int h)`

**作用与语义：**

设置小部件的最小和最大高度为`h`，但不更改宽度。为方便而提供。

### `void QWidget::setFixedSize(const QSize &s)`

**作用与语义：**

将小部件的最小和最大大小都设置为`s`，从而防止其不断增长或缩小。
这将覆盖`QLayout`设定的默认大小约束。
要移除约束，将大小设为`QWIDGETSIZE_MAX`。
或者，如果你希望小部件根据其内容有固定大小，可以调用 `QLayout::setSizeConstraint`（`QLayout::SetFixedSize`）;

### `void QWidget::setFixedSize(int w, int h)`

**作用与语义：**

将小部件的宽度设置为`w`，高度设置为`h`。

### `void QWidget::setFixedWidth(int w)`

**作用与语义：**

将小部件的最小和最大宽度设置为`w`，且不更改高度。为方便而提供。

### `void QWidget::setFocus(Qt::FocusReason reason)`

**作用与语义：**

如果该控件或其父窗口是活跃窗口，则将键盘输入焦点传递到该控件（或其焦点代理）。`reason`参数将传递到该函数发送的任何焦点事件中，用于解释导致控件获得焦点的原因。如果窗口未激活，窗口激活时控件将获得焦点。
首先，将即将更换焦点的事件发送给焦点组件（如有），告知它即将失去焦点。然后切换焦点，向上一个焦点项目发送焦点出任务，向新物品发送焦点事件，告知新物品刚刚收到焦点。（如果焦点输入和焦点出场控件相同，则不会发生任何事。）。
注意：在嵌入式平台上，setFocus() 不会让输入法打开输入面板。如果你想实现这种情况，必须自己向小部件发送一个`QEvent::RequestSoftwareInputPanel`事件。
setFocus() 无论控件的焦点策略如何，都能为控件提供焦点，但不会清除任何键盘抓取（见 `grabKeyboard()`）。
注意，如果小部件被隐藏，它不会接受焦点，直到显示出来。
警告：如果你在一个函数中调用 setFocus()，而函数本身可能由 `focusOutEvent()` 或 `focusInEvent()` 调用，你可能会得到无限递归。

### `[slot] void QWidget::setFocus()`

**作用与语义：**

如果该控件或其父窗口是活动窗口，则将键盘输入焦点分配给该控件（或其焦点代理）。
注意：该槽位已超载。连接该槽位：


使用 qOverload 连接：
connect（sender， &SenderClass：：signal，。
widget， qOverload<>（&QWidget：：setFocus））;

或者用lambda作为包装器：
connect（sender， &SenderClass：：signal，。
控件，[接收器 = 控件]() { 接收器->setFocus(); }）;


更多示例和方法，请参见连接超载槽位。

### `void QWidget::setFocusProxy(QWidget *w)`

**作用与语义：**

将小部件的焦点代理设置为小部件`w`。如果`w` `nullptr`，函数会重置该小部件为无焦点代理。
有些小部件可以“拥有焦点”，但会创建子小部件，比如`QLineEdit`，来实际处理焦点。在这种情况下，小部件可以将行编辑设置为其焦点代理。
setFocusProxy() 设置了当“该控件”获得焦点时，该控件实际上会被聚焦。如果存在焦点代理，`setFocus()` 和 `hasFocus()` 对焦点代理进行操作。如果“这个控件”是焦点控件，那么 setFocusProxy() 将焦点移动到新的焦点代理。

### `void QWidget::setForegroundRole(QPalette::ColorRole role)`

**作用与语义：**

将小部件的前景定位为`role`。
前景角色定义了用于绘制前景的控件`palette`颜色。
如果`role` `QPalette::NoRole`，则该小部件使用与背景角色对比的前景角色。
请注意，样式可以自由选择调色板中的任何颜色。如果用 setForegroundRole() 无法达到想要的结果，可以修改调色板或设置样式表。

### `void QWidget::setGeometry(int x, int y, int w, int h)`

**作用与语义：**

该属性表示了小部件相对于其父节点的几何形状，排除窗口框架。
更改几何体时，如果控件可见，会立即接收移动事件（`moveEvent()`）和/或调整大小事件（`resizeEvent()`）。如果控件当前不可见，保证在展示前收到相应事件。
如果尺寸分量超出`minimumSize()`和`maximumSize()`定义范围，则会进行调整。
警告：在`resizeEvent()`或`moveEvent()`中调用 setGeometry() 可能导致无限递归。
关于窗口几何问题的概述，请参见 Window Geometry 文档。
默认情况下，该属性包含一个取决于用户平台和屏幕几何形状的值。

**如何使用：** 调用 `setGeometry(...)` 修改 `geometry`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QWidget::setGraphicsEffect(QGraphicsEffect *effect)`

**作用与语义：**

setGraphicsEffect 函数用于设置小部件的图形效果。
将`effect`设置为该小部件的效果。如果该小部件上已经安装了某个效果，`QWidget`会在安装新`effect`前删除现有的效果。
如果`effect`是安装在不同控件上的效果，setGraphicsEffect() 会从控件中移除该效果并安装到该控件上。
`QWidget`对`effect`负责任。
注意：该函数将对自身及其所有子功能施加效果。
注意：基于OpenGL的小部件（如QGLWidget、`QOpenGLWidget`和`QQuickWidget`）不支持图形特效。

### `[slot] void QWidget::setHidden(bool hidden)`

**作用与语义：**

便利功能，相当于`setVisible`（！`hidden`）。

### `void QWidget::setLayout(QLayout *layout)`

**作用与语义：**

将该小部件的布局管理器设置为`layout`。
如果该小部件上已经安装了布局管理器，`QWidget`不会让你安装另一个。你必须先删除现有的布局管理器（由`layout()`返回），才能用新布局调用setLayout()。
如果`layout`是另一个控件的布局管理器，setLayout() 会重新父级该布局，使其成为该控件的布局管理器。
调用该函数的另一种方法是将该控件传递给布局的构造函数。
`QWidget`将接管`layout`。

**官方示例：**

```cpp
 QVBoxLayout *layout = new QVBoxLayout;
 layout->addWidget(formWidget);
 formWidget->setLayout(layout);
```

### `void QWidget::setMask(const QBitmap &bitmap)`

**作用与语义：**

只显示控件中`bitmap`对应1位的像素。如果该区域包含控件`rect()`外的像素，窗口系统控件在该区域可能可见也可能不可见，取决于平台。
注意，如果区域特别复杂，这种效应可能会很慢。
以下代码展示了如何利用带有alpha通道的图像生成小部件的遮罩：
该代码显示的标签被其所包含的图像遮蔽，给人一种不规则形状的图像直接绘制在屏幕上的视觉效果。
蒙面小部件只在其可见部分接收鼠标事件。

**官方示例：**

```cpp
 QLabel topLevelLabel;
 QPixmap pixmap(":/images/tux.png");
 topLevelLabel.setPixmap(pixmap);
 topLevelLabel.setMask(pixmap.mask());
```

### `void QWidget::setMask(const QRegion &region)`

**作用与语义：**

只会让小部件中重叠的部分`region`可见。如果该区域包含了小部件`rect()`外的像素，该区域的窗口系统控件可能会被看到，也可能看不到，具体取决于平台。
由于`QRegion`允许创建任意复杂的区域，widget mask 可以设计成适合最非常规形状窗口的样式，甚至允许显示带有孔洞的小部件。注意，如果区域特别复杂，这种效果可能会比较慢。
控件遮罩用于向窗口系统提示应用不希望遮罩外区域出现鼠标事件。在大多数系统中，它们还会导致粗糙的视觉裁剪。为了获得平滑的窗口边缘，可以使用半透明背景和抗锯齿绘画，如半透明背景示例所示。

### `void QWidget::setMaximumSize(int maxw, int maxh)`

**作用与语义：**

此属性保存小部件的最大尺寸（像素）。
小部件不能调整为超过最大小部件尺寸的大小。
默认情况下，此属性的尺寸的宽度和高度均为 16777215。
注意：`QWIDGETSIZE_MAX` 宏的定义限制了小部件的最大尺寸。

**如何使用：** 调用 `setMaximumSize(...)` 修改 `maximumSize`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QWidget::setMinimumSize(int minw, int minh)`

**作用与语义：**

此属性保存小部件的最小尺寸。
小部件不能调整为小于最小小部件尺寸的大小。如果当前尺寸较小，小部件的尺寸将被强制为最小尺寸。
此函数设置的最小尺寸将覆盖 `QLayout` 定义的最小尺寸。要取消设置最小尺寸，请使用 `QSize(0, 0)` 的值。
默认情况下，此属性包含宽度和高度均为零的尺寸。

**如何使用：** 调用 `setMinimumSize(...)` 修改 `minimumSize`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QWidget::setParent(QWidget *parent)`

**作用与语义：**

将小部件的父节点设置为`parent`，并重置窗口标志。小部件被移动到其新父节点的位置（0， 0）。
如果新父控件位于不同窗口，重新父级控件及其子组件会按之前的内部顺序附加到新父控件的制表链末尾。如果移动的控件中有键盘焦点，setParent() 调用该控件的 `clearFocus()`。
如果新父小部件和旧父小部件在同一个窗口里，设置父小部件不会改变制表顺序或键盘焦点。
如果“新”父控件是旧的父控件，这个函数就不做任何事。
注意：控件在更改父节点时会变得不可见，即使之前是可见的。您必须调用`show()`才能使控件再次可见。
警告：你很可能永远用不到这个功能。如果你有一个能动态更改内容的小工具，使用起来会容易很多`QStackedWidget`。

### `void QWidget::setParent(QWidget *parent, Qt::WindowFlags f)`

**作用与语义：**

该函数还会接收控件标志，`f`作为参数。

### `void QWidget::setScreen(QScreen *screen)`

**作用与语义：**

将小部件应显示的屏幕设置`screen`。
设置屏幕只对窗口有意义。如果有必要，小部件的窗口会在`screen`上重新创建。
注意：如果屏幕是多个屏幕组成的虚拟桌面的一部分，窗口不会自动移动到`screen`。要将窗口相对于屏幕放置，请使用屏幕的左上（TopLeft）位置。

### `void QWidget::setShortcutAutoRepeat(int id, bool enable = true)`

**作用与语义：**

如果`enable`为真，则启用了用该`id`自动重复快捷方式;否则该功能被禁用。

### `void QWidget::setShortcutEnabled(int id, bool enable = true)`

**作用与语义：**

如果`enable`为真，则启用了该快捷方式`id`;否则快捷方式被禁用。
警告：通常不需要使用这个功能，因为Qt的快捷方式系统会在控件变得隐藏/可见并获得或失去焦点时自动启用或禁用快捷方式。最好使用`QAction`或`QShortcut`来处理快捷方式，因为它们比这个低阶函数更易于使用。

### `void QWidget::setSizeIncrement(int w, int h)`

**作用与语义：**

该属性包含小部件的大小增量。
当用户调整窗口大小时，尺寸将以 sizeIncrement() 为步骤移动。`width()` 像素水平，sizeIncrement.`height()` 像素垂直，`baseSize()` 作为基底。首选控件大小为非负整数 i 和 j：
注意，虽然你可以为所有小部件设置大小增量，但这只影响窗口。
默认情况下，该属性包含宽度和高度均为零的大小。
警告：在 Windows 下，大小递增无效，X11 上的窗口管理器可能会忽略它。

**如何使用：** 调用 `setSizeIncrement(...)` 修改 `sizeIncrement`；传入的新值会成为后续查询和相关界面行为所使用的值。

**官方示例：**

```cpp
 width = baseSize().width() + i * sizeIncrement().width();
 height = baseSize().height() + j * sizeIncrement().height();
```

### `void QWidget::setSizePolicy(QSizePolicy::Policy horizontal, QSizePolicy::Policy vertical)`

**作用与语义：**

该属性保留了小部件的默认布局行为。
如果存在管理该控件子节点的 `QLayout`，则使用该布局指定的大小策略。如果没有这样的`QLayout`，则使用该函数的结果。
默认策略为“Preferred/Preferred”，这意味着小部件可以自由调整大小，但优先选择返回的大小`sizeHint()`。类似按钮的小部件设置大小策略，指定它们可以横向拉伸，但垂直方向是固定的。同样适用于行编辑控件（如`QLineEdit`、`QSpinBox`或可编辑`QComboBox`）以及其他横向控件（如`QProgressBar`）。`QToolButton`通常是方形的，因此允许双向扩展。支持不同方向的小部件（如`QSlider`、`QScrollBar`或QHeader）只指定相应方向的拉伸。能够提供滚动条的小部件（通常是`QScrollArea`子类）通常会指定它们可以使用额外空间，并且能用少于`sizeHint()`的空间。

**如何使用：** 调用 `setSizePolicy(...)` 修改 `sizePolicy`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QWidget::setStyle(QStyle *style)`

**作用与语义：**

将小部件的 GUI 样式设置为`style`。样式对象的所有权不会转移。
如果没有设置样式，小部件会使用应用程序的样式，`QApplication::style()`。
设置小部件样式不会影响现有或未来的子小部件。
警告：该功能特别适合演示，比如展示 Qt 的样式功能。实际应用应避免使用，使用统一的 GUI 样式。
警告：目前自定义`QStyle`子类不支持 Qt 样式表。我们计划在未来某个版本中解决这个问题。

### `[static] void QWidget::setTabOrder(QWidget *first, QWidget *second)`

**作用与语义：**

在焦点顺序中，将`second`小部件放在`first`小部件之后。
它实际上是将`second`小部件从焦点链中移除，并将其插入`first`小部件之后。
注意，由于`second`小部件的制表顺序发生了变化，你应该按照链条顺序排列如下：
不是这样：
如果`first`或`second`有焦点代理，setTabOrder() 会正确替换该代理。
注意：自Qt 5.10起：带有子节点作为焦点代理的小部件被理解为复合控件。当在一个或两个复合控件之间设置制表顺序时，每个内部的本地制表顺序将被保留。这意味着如果两个控件都是复合控件，生成的标签顺序将从`first`内的最后一个子节点到`second`中的第一个子节点。

**官方示例：**

```cpp
 setTabOrder(a, b); // a to b
 setTabOrder(b, c); // a to b to c
 setTabOrder(c, d); // a to b to c to d
```

### `[static, since 6.6] void QWidget::setTabOrder(std::initializer_list<QWidget *> widgets)`

**作用与语义：**

通过调用`QWidget::setTabOrder`（QWidget *， QWidget *）来设置`widgets`列表中控件的表表顺序，针对每对相邻的控件。
而不是像这样手动设置每对：
您可以调用：
调用不会创建闭合的标签焦点循环。如果有更多带有`Qt::TabFocus`焦点策略的小部件，在`d`上用标签键控制会把焦点移到这些小部件之一，而不是回到`a`。

**官方示例：**

```cpp
 setTabOrder(a, b); // a to b
 setTabOrder(b, c); // a to b to c
 setTabOrder(c, d); // a to b to c to d
```

### `void QWidget::setWindowFlag(Qt::WindowType flag, bool on = true)`

**作用与语义：**

如果该控件为真，则将窗口标志设为`flag` `on`;否则清除该标志。
注意：该函数在更改窗口标志时调用`setParent()`，导致控件被隐藏。您必须调用`show()`才能使控件再次可见。

### `void QWidget::setWindowRole(const QString &role)`

**作用与语义：**

把窗口的角色设置为`role`。这只适用于X11上的Windows。

### `void QWidget::setWindowState(Qt::WindowStates windowState)`

**作用与语义：**

将窗口状态设置为`windowState`。窗口状态是`Qt::WindowState`的OR组合：`Qt::WindowMinimized`、`Qt::WindowMaximized`、`Qt::WindowFullScreen`和`Qt::WindowActive`。
如果窗口不可见（即`isVisible()`返回`false`），当调用`show()`时窗口状态生效。对于可见窗口，变化是即时发生的。例如，要在全屏和普通模式之间切换，请使用以下代码：
要恢复和激活最小化窗口（同时保持其最大化和/或全屏状态），请使用以下工具：
调用该函数会隐藏小部件。您必须调用`show()`才能让小部件再次可见。
注意：在某些窗户系统中`Qt::WindowActive`不是即时的，在某些情况下可能会被忽略。
当窗口状态变化时，小部件会收到类型为`QEvent::WindowStateChange`的`changeEvent()`。

**官方示例：**

```cpp
 w->setWindowState(w->windowState() ^ Qt::WindowFullScreen);
```

### `void QWidget::setupUi(QWidget *widget)`

**作用与语义：**

为指定`widget`设置用户界面。
注意：该功能适用于基于 uic 创建的用户界面描述的小部件。

### `[slot] void QWidget::show()`

**作用与语义：**

显示小部件及其子小部件。
对于子窗口，这等同于调用 `setVisible`（true）。否则，则等同于调用 `showFullScreen()`、`showMaximized()` 或 `setVisible`（true），具体取决于平台对窗口标志的默认行为。

### `[virtual protected] void QWidget::showEvent(QShowEvent *event)`

**作用与语义：**

该事件处理程序可以在子类中重新实现，以接收通过 `event` 参数传递的控件 show 事件。
非自发的展示事件会在展示前立即发送到小部件。窗口的自发展示事件则在展示之后交付。
注意：当窗口系统改变控件的映射状态时，控件会接收自发显示和隐藏事件，例如用户最小化窗口时触发自发隐藏事件，窗口恢复时则触发自发显示事件。收到自发隐藏事件后，控件仍被视为`isVisible()`可见。

### `[slot] void QWidget::showFullScreen()`

**作用与语义：**

显示小部件全屏模式。
调用该函数只影响`windows`。
要从全屏模式返回，请调用`showNormal()`或 `close()`。
注意：全屏模式在 Windows 下运行良好，但在 X 下存在某些问题。这些问题源于 ICCCM 协议的限制，该协议规定了 X11 客户端与窗口管理器之间的通信。ICCCM 根本不理解非装饰全屏窗口的概念。因此，你能做的最好方法是请求无边框窗口，并放置并调整大小以填满整个屏幕。这取决于窗口管理器，这可能有效也可能无效。无边框窗口是通过 MOTIF 提示请求的，而 MOTIF 提示几乎所有现代窗口管理器至少部分支持该提示。
另一种选择是完全绕过窗口管理器，创建一个带有`Qt::X11BypassWindowManagerHint`标志的窗口。不过这还有其他严重问题，比如键盘焦点损坏，以及桌面切换或用户打开其他窗口时出现非常奇怪的效果。
遵循现代后ICCCM规范的X11窗口管理器支持全屏模式。
在macOS上，显示窗口全屏会让整个应用程序进入全屏模式，从而为它提供专用桌面。在应用程序全屏运行时显示另一个窗口，可能自动使该窗口也变成全屏。为防止这种情况，请在显示另一个窗口前，先调用`showNormal()`或`close()`全屏窗口退出全屏模式。

### `[slot] void QWidget::showMaximized()`

**作用与语义：**

显示小部件已最大化。
调用该函数只影响`windows`。
在 X11 上，这个功能可能无法在某些窗口管理器中正常工作。请参见 Window Geometry 文档来了解相关说明。

### `[slot] void QWidget::showMinimized()`

**作用与语义：**

以图标形式显示小部件最小化。
调用该函数只影响`windows`。

### `[slot] void QWidget::showNormal()`

**作用与语义：**

在小部件被最大化或最小化后恢复。
调用该函数只影响`windows`。

### `void QWidget::stackUnder(QWidget *w)`

**作用与语义：**

将小部件放在父小部件栈的 `w` 下。
要实现这一点，小部件本身和`w`必须是兄弟姐妹。

### `QStyle *QWidget::style() const`

**作用与语义：**

返回当前实际用于绘制该控件的 `QStyle`。控件未通过 `setStyle()` 单独指定时，结果来自父控件或应用样式；可用它查询像素指标、标准图标或绘制控件，但返回对象由 Qt 管理，不要删除或长期缓存。

### `[virtual protected] void QWidget::tabletEvent(QTabletEvent *event)`

**作用与语义：**

该事件处理程序用于事件`event`，可以在子类中重新实现，以接收该小部件的平板事件。
如果你重新实现了这个处理程序，非常重要的是，如果你不处理该事件，`ignore()`事件，这样小部件的父节点才能解释它。
默认实现会忽略该事件。
如果关闭了绘图板追踪，只有在触控笔与绘图板接触，或至少按下一个触控笔按钮时，才会触发平板移动事件。如果开启绘图板追踪，即使触控笔悬停在平板附近，且未按任何按钮，平板移动事件也会发生。

### `bool QWidget::testAttribute(Qt::WidgetAttribute attribute) const`

**作用与语义：**

如果该控件设置了属性`attribute`，返回`true`;否则返回`false`。

### `bool QWidget::underMouse() const`

**作用与语义：**

如果小部件位于鼠标光标下方，返回`true`;否则返回`false`。
在拖拽操作期间，这个值没有被正确更新。

### `void QWidget::ungrabGesture(Qt::GestureType gesture)`

**作用与语义：**

取消订阅给定的`gesture`类型。

### `[slot] void QWidget::update()`

**作用与语义：**

除非被禁用更新或控件被隐藏，否则会更新小部件。
该函数不会立即重新绘制;相反，当 Qt 返回主事件循环时，它会安排一个绘制事件进行处理。这使得 Qt 能够比调用 `repaint()` 优化更快的速度和更少的闪烁。
多次调用 update() 通常只会有一次 `paintEvent()` 通话。
Qt 通常在`paintEvent()`调用前擦除小部件的区域。如果设置了`Qt::WA_OpaquePaintEvent`小部件属性，小部件负责将所有像素涂成不透明颜色。
注意：该槽位已超载。连接该槽位：


使用 qOverload 连接：
connect（sender， &SenderClass：：signal，。
widget， qOverload<>（&QWidget：：update））;

或者用lambda作为包装器：
connect（sender， &SenderClass：：signal，。
控件，[接收器 = 控件]() { 接收器->update(); }）;


更多示例和方法，请参见连接超载槽位。

### `void QWidget::update(const QRect &rect)`

**作用与语义：**

该版本更新了小部件内部的一个矩形`rect`。

### `void QWidget::update(const QRegion &rgn)`

**作用与语义：**

该版本在控件内部重新绘制区域`rgn`。

### `void QWidget::update(int x, int y, int w, int h)`

**作用与语义：**

该版本更新了小部件内部的一个矩形（`x`、`y`、`w`、`h`）。

### `void QWidget::updateGeometry()`

**作用与语义：**

通知布局系统该小部件已更改，可能需要更改几何结构。
如果`sizeHint()`或`sizePolicy()`发生变化，就调用这个函数。
对于显式隐藏的小部件，updateGeometry() 是禁用操作。一旦小部件显示，布局系统会立即收到通知。

### `[protected slot] void QWidget::updateMicroFocus(Qt::InputMethodQuery query = Qt::ImQueryAll)`

**作用与语义：**

更新控件的微焦点，并通知输入方法`query`指定的状态发生了变化。

### `QRegion QWidget::visibleRegion() const`

**作用与语义：**

返回可发生绘画事件的未遮挡区域。
对于可见控件，这是对其他控件未覆盖区域的近似值;否则，该区域为空区域。
`repaint()`函数如果需要调用这个函数，所以一般来说你不需要调用它。

### `[virtual protected] void QWidget::wheelEvent(QWheelEvent *event)`

**作用与语义：**

该事件处理程序用于事件`event`，可以在子类中重新实现，以接收该控件的轮事件。
如果你重新实现这个处理程序，非常重要的是，如果你不处理事件，必须`ignore()`事件，这样小部件的父节点才能解释它。
默认实现会忽略该事件。

### `WId QWidget::winId() const`

**作用与语义：**

返回小部件的窗口系统标识符。
原则上是便携式，但如果你用它，可能会做出非便携性的东西。要小心。
如果某个小部件是非原生的（外来的），并且调用了 winId()，该小部件将获得一个原生句柄。
该值在运行时可能会发生变化。窗口系统标识符发生变化后，类型为 `QEvent::WinIdChange` 的事件会发送到小部件。

### `QWidget *QWidget::window() const`

**作用与语义：**

返回该控件的窗口，即下一个具有（或可能有）窗口系统框架的祖先控件。
如果小部件是窗口，则返回小部件本身。
典型用法是更改窗口标题：

**官方示例：**

```cpp
 aWidget->window()->setWindowTitle("New Window Title");
```

### `QWindow *QWidget::windowHandle() const`

**作用与语义：**

如果这是原生小部件，返回关联的`QWindow`。否则返回空。
原生小部件包括顶层小部件、QGLWidget 以及调用 `winId()` 的子小部件。

### `[signal] void QWidget::windowIconChanged(const QIcon &icon)`

**作用与语义：**

此属性保存小部件的图标。
此属性仅适用于窗口。如果没有设置图标，windowIcon() 将返回应用程序图标 (`QApplication::windowIcon()`)。
注意：在 macOS 上，窗口图标表示活动文档，除非使用 `setWindowFilePath` 设置了文件路径，否则不会显示。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `windowIcon` 的变化，不要把它当作普通函数主动调用。

### `QString QWidget::windowRole() const`

**作用与语义：**

返回窗口的角色，或返回空字符串。

### `Qt::WindowStates QWidget::windowState() const`

**作用与语义：**

返回当前窗口状态。窗口状态是`Qt::WindowState`的OR组合：`Qt::WindowMinimized`、`Qt::WindowMaximized`、`Qt::WindowFullScreen`和`Qt::WindowActive`。

### `[signal] void QWidget::windowTitleChanged(const QString &title)`

**作用与语义：**

该物业拥有窗户标题（说明）。
该属性仅适用于顶层控件，如窗口和对话框。如果未设置说明文字，标题基于`windowFilePath`。若未设置，标题为空字符串。
如果你使用`windowModified`机制，窗口标题必须包含“[*]”占位符，指示“*”应出现在位置。通常，它应紧随文件名之后（例如，“document1.txt[*] - 文本编辑器”）。如果`windowModified`属性被`false`（默认），占位符会被直接移除。
在某些桌面平台（包括 Windows 和 Unix）上，如果设置了，应用程序名称（来自 `QGuiApplication::applicationDisplayName`）会被添加到窗口标题末尾。这是通过 QPA 插件实现的，因此它会显示给用户，但不包含在 windowTitle 字符串中。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `windowTitle` 的变化，不要把它当作普通函数主动调用。

### `Qt::WindowType QWidget::windowType() const`

**作用与语义：**

返回该控件的窗口类型。这与`windowFlags()`和`Qt::WindowType_Mask`相同。

### `QWIDGETSIZE_MAX`

**作用与语义：**

定义`QWidget`对象的最大尺寸。
小部件允许的最大尺寸是`QSize`（QWIDGETSIZE_MAX， QWIDGETSIZE_MAX），即`QSize`（16777215,16777215）。

### `enum RenderFlag { DrawWindowBackground, DrawChildren, IgnoreMask }`

**作用与语义：**

这个枚举描述了调用`QWidget::render()`时如何渲染该控件。
- `QWidget::DrawWindowBackground`：`0x1`;如果你启用此选项，即使未设置`autoFillBackground`，小部件的背景也会被渲染到目标中。默认情况下，该选项是启用的。
- `QWidget::DrawChildren`：`0x2`;如果你启用此选项，小部件的子节点会递归地被渲染到目标中。默认情况下，该选项是启用的。
- `QWidget::IgnoreMask`：`0x4`;如果你启用此选项，渲染到目标时小部件的 `QWidget::mask()` 会被忽略。默认情况下，该选项被禁用。
RenderFlags 类型是 QFlags 的 typedef<RenderFlag>。它存储 RenderFlag 值的 OR 组合。

### `flags RenderFlags`

**作用与语义：**

这个枚举描述了调用`QWidget::render()`时如何渲染该控件。
- `QWidget::DrawWindowBackground`：`0x1`;如果你启用此选项，即使未设置`autoFillBackground`，小部件的背景也会被渲染到目标中。默认情况下，该选项是启用的。
- `QWidget::DrawChildren`：`0x2`;如果你启用此选项，小部件的子节点会递归地被渲染到目标中。默认情况下，该选项是启用的。
- `QWidget::IgnoreMask`：`0x4`;如果你启用此选项，渲染到目标时小部件的 `QWidget::mask()` 会被忽略。默认情况下，该选项被禁用。
RenderFlags 类型是 QFlags 的 typedef<RenderFlag>。它存储 RenderFlag 值的 OR 组合。

### `bool acceptDrops() const`

**作用与语义：**

该属性决定该控件是否启用掉落事件。
将该属性设置为 true，会向系统宣布该控件可能能够接受丢弃事件。
警告：请勿在拖放事件处理程序中修改该属性。
默认情况下，该属性为`false`。

**如何使用：** 调用 `acceptDrops()` 读取当前值；它不会修改应用状态。

### `QString accessibleDescription() const`

**作用与语义：**

该属性包含辅助技术中控件的描述。
控件的可访问描述应传达控件的功能。虽然`accessibleName`应是简短且简洁的字符串（例如保存），但描述应提供更多上下文，比如保存当前文档。
这个属性必须是本地化的。
默认情况下，该属性包含空字符串，Qt 会回退到使用工具提示来提供这些信息。

**如何使用：** 调用 `accessibleDescription()` 读取当前值；它不会修改应用状态。

### `QString accessibleIdentifier() const`

**作用与语义：**

此属性保存辅助技术中看到的小部件标识符。
如果设置，辅助技术可以使用小部件的可访问标识符来识别特定的小部件，例如在自动化测试中。

**如何使用：** 调用 `accessibleIdentifier()` 读取当前值；它不会修改应用状态。

### `QString accessibleName() const`

**作用与语义：**

此属性保存辅助技术中看到的小部件名称。
这是辅助技术（如屏幕阅读器）宣布此小部件的主要名称。对于大多数小部件，不需要设置此属性。例如，对于 `QPushButton`，按钮的文本将被使用。
当小部件不提供任何文本时，设置此属性很重要。例如，仅包含图标的按钮需要设置此属性以配合屏幕阅读器使用。名称应简短，并与小部件传递的视觉信息相当。
此属性必须本地化。
默认情况下，此属性包含空字符串。

**如何使用：** 调用 `accessibleName()` 读取当前值；它不会修改应用状态。

### `(since 6.3) QAction * addAction(const QString &text)`

**作用与语义：**

这些便利功能会创建新的动作，包含文本`text`、图标`icon`和快捷方式，`shortcut`（如果有的话）。
函数会将新创建的动作添加到控件的动作列表中，并返回它。
`QWidget`接管了归还的这`QAction`。

### `(since 6.3) QAction * addAction(const QIcon &icon, const QString &text)`

**作用与语义：**

这些便利功能会创建新的动作，包含文本`text`、图标`icon`和快捷方式`shortcut`（如果有的话）。
动作的`triggered()`信号通过调用调用`QObject::connect`（动作，&`QAction::triggered`，args...）连接，完美转发`args`，包括可能的`Qt::ConnectionType`。
该函数会将新创建的动作添加到小部件的动作列表中并返回。
`QWidget`接管了归还的这`QAction`。

### `(since 6.3) QAction * addAction(const QString &text, const QKeySequence &shortcut)`

**作用与语义：**

这些便利功能会创建新的动作，包含文本`text`、图标`icon`和快捷方式`shortcut`（如果有的话）。
动作的`triggered()`信号通过调用调用`QObject::connect`（动作，&`QAction::triggered`，args...）连接，完美转发`args`，包括可能的`Qt::ConnectionType`。
该函数会将新创建的动作添加到小部件的动作列表中并返回。
`QWidget`接管了归还的这`QAction`。

### `(since 6.3) QAction * addAction(const QString &text, Args &&... args)`

**作用与语义：**

这些便利功能会创建新的动作，包含文本`text`、图标`icon`和快捷方式`shortcut`（如果有的话）。
动作的`triggered()`信号通过调用调用`QObject::connect`（动作，&`QAction::triggered`，args...）连接，完美转发`args`，包括可能的`Qt::ConnectionType`。
该函数会将新创建的动作添加到小部件的动作列表中并返回。
`QWidget`接管了归还的这`QAction`。

### `(since 6.3) QAction * addAction(const QIcon &icon, const QString &text, Args &&... args)`

**作用与语义：**

这些便利功能会创建新的动作，包含文本`text`、图标`icon`和快捷方式`shortcut`（如果有的话）。
动作的`triggered()`信号通过调用调用`QObject::connect`（动作，&`QAction::triggered`，args...）连接，完美转发`args`，包括可能的`Qt::ConnectionType`。
该函数会将新创建的动作添加到小部件的动作列表中并返回。
`QWidget`接管了归还的这`QAction`。

### `(since 6.3) QAction * addAction(const QString &text, const QKeySequence &shortcut, Args &&... args)`

**作用与语义：**

这个便利功能会创建一个新的动作，包含文本`text`、图标`icon`和快捷方式`shortcut`（如果有的话）。
动作的`triggered()`信号连接到`receiver`的`member`槽。函数将新创建的动作添加到控件的动作列表中并返回。
`QWidget`接管了归还的`QAction`。

### `(since 6.3) QAction * addAction(const QString &text, const QObject *receiver, const char *member, Qt::ConnectionType type = Qt::AutoConnection)`

**作用与语义：**

这个便利功能会创建一个新的动作，包含文本`text`、图标`icon`和快捷方式`shortcut`（如果有的话）。
动作的`triggered()`信号连接到`receiver`的`member`槽。函数将新创建的动作添加到控件的动作列表中并返回。
`QWidget`接管了归还的`QAction`。

### `(since 6.3) QAction * addAction(const QIcon &icon, const QString &text, const QObject *receiver, const char *member, Qt::ConnectionType type = Qt::AutoConnection)`

**作用与语义：**

这个便利功能会创建一个新的动作，包含文本`text`、图标`icon`和快捷方式`shortcut`（如果有的话）。
动作的`triggered()`信号连接到`receiver`的`member`槽。函数将新创建的动作添加到控件的动作列表中并返回。
`QWidget`接管了归还的`QAction`。

### `(since 6.3) QAction * addAction(const QString &text, const QKeySequence &shortcut, const QObject *receiver, const char *member, Qt::ConnectionType type = Qt::AutoConnection)`

**作用与语义：**

这个便利功能会创建一个新的动作，包含文本`text`、图标`icon`和快捷方式`shortcut`（如果有的话）。
动作的`triggered()`信号连接到`receiver`的`member`槽。函数将新创建的动作添加到控件的动作列表中并返回。
`QWidget`接管了归还的`QAction`。

### `bool autoFillBackground() const`

**作用与语义：**

该属性决定了小部件背景是否自动填充。
如果启用该属性，Qt 会在调用绘画事件前填充小部件的背景。颜色由小部件`palette`的`QPalette::Window`颜色角色定义。
此外，除非设置了WA_OpaquePaintEvent或WA_NoSystemBackground属性，否则Windows总是充满`QPalette::Window`。
如果小部件的父背景是静态渐变，则该属性无法关闭（即设置为 false）。
警告：请谨慎使用该属性与 Qt 样式表一起使用。当小部件拥有有效背景或边框图片的样式表时，该属性会自动被禁用。
默认情况下，该属性是`false`。

**如何使用：** 调用 `autoFillBackground()` 读取当前值；它不会修改应用状态。

### `QSize baseSize() const`

**作用与语义：**

该属性包含控件的基准大小。
如果控件定义了`sizeIncrement()`，则使用基准大小来计算合适的控件大小。
默认情况下，对于新创建的控件，该属性包含宽度和高度为零的大小。

**如何使用：** 调用 `baseSize()` 读取当前值；它不会修改应用状态。

### `QRect childrenRect() const`

**作用与语义：**

该属性表示了小部件子节点的边界矩形。
隐藏的儿童被排除在外。
默认情况下，对于没有子节点的控件，该属性包含一个宽度和高度均为零的矩形，位于原点。

**如何使用：** 调用 `childrenRect()` 读取当前值；它不会修改应用状态。

### `QRegion childrenRegion() const`

**作用与语义：**

该属性保存控件子项所占据的组合区域，。
隐藏的子项不包括在内。
默认情况下，对于没有子项的控件，此属性包含一个空区域。

**如何使用：** 调用 `childrenRegion()` 读取当前值；它不会修改应用状态。

### `Qt::ContextMenuPolicy contextMenuPolicy() const`

**作用与语义：**

小部件如何显示上下文菜单。
该属性的默认值为`Qt::DefaultContextMenu`，意味着调用`contextMenuEvent()`处理程序。其他值有`Qt::NoContextMenu`、`Qt::PreventContextMenu`、`Qt::ActionsContextMenu`和`Qt::CustomContextMenu`。使用`Qt::CustomContextMenu`时，信号`customContextMenuRequested()`被发射。

**如何使用：** 调用 `contextMenuPolicy()` 读取当前值；它不会修改应用状态。

### `QCursor cursor() const`

**作用与语义：**

该属性包含该控件的光标形状。
鼠标光标在该控件上方时会呈现该形状。请参阅预定义光标对象列表，了解一系列有用的形状。
编辑器小部件可能会使用工字束光标：
如果没有设置光标，或者在调用 unsetCursor() 后，则使用父游标。
默认情况下，该属性包含一个具有`Qt::ArrowCursor`形状的光标。
有些底层窗口实现如果光标离开了小部件，即使鼠标被抓取，光标也会重置。如果你想为所有小部件设置光标，即使你在窗口外，也可以考虑用`QGuiApplication::setOverrideCursor()`。

**如何使用：** 调用 `cursor()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 setCursor(Qt::IBeamCursor);
```

### `Qt::FocusPolicy focusPolicy() const`

**作用与语义：**

该属性表示了小部件接受键盘焦点的方式。
如果控件通过 Tab 键接受键盘聚焦，`Qt::ClickFocus`如果控件通过点击接受焦点，`Qt::StrongFocus`如果两者都接受， `Qt::NoFocus`（默认）则不接受焦点，该策略是 `Qt::TabFocus`。
如果控件处理键盘事件，您必须启用键盘焦点。这通常由控件的构造函数完成。例如，`QLineEdit`构造函数调用 setFocusPolicy（`Qt::StrongFocus`）。
如果小部件有焦点代理，那么焦点策略会传播到它。

**如何使用：** 调用 `focusPolicy()` 读取当前值；它不会修改应用状态。

### `const QFont & font() const`

**作用与语义：**

该属性保留当前为控件设置的字体。
该属性描述了小部件所请求的字体。该字体被小部件的样式用于渲染标准组件，并作为确保自定义小部件能够与原生平台外观和感觉保持一致的手段。不同平台或不同样式通常会为应用程序定义不同的字体。
当你为小部件分配新字体时，该字体的属性会与小部件的默认字体结合，形成小部件的最终字体。你可以调用`fontInfo()`获取小部件最终字体的副本。最终字体也用于初始化`QPainter`字体。
默认字体取决于系统环境。`QApplication`维护一个系统/主题字体，作为所有控件的默认字体。某些类型的控件可能还有特殊的字体默认值。你也可以自己定义控件的默认字体，通过传递自定义字体和控件名称给`QApplication::setFont()`。最后，字体会与Qt的字体数据库匹配，以找到最佳匹配字体。
`QWidget` 会将显式字体属性从父字母传播到子节点。如果你更改字体上的某个属性并将该字体分配给控件，该属性会传播到该控件的所有子节点，覆盖该属性的系统默认设置。注意，除非启用了 `Qt::WA_WindowPropagation` 属性，否则字体默认不会传播到窗口（见 `isWindow()`）。
`QWidget` 的字体传播方式与调色板传播相似。
当前样式用于渲染所有标准 Qt 控件的内容，可以自由选择使用控件字体，或在某些情况下部分或完全忽略它。特别是某些样式如 GTK 样式、Mac 样式和 Windows Vista 样式，会对控件字体进行特殊修改，以匹配平台的原生外观和感觉。因此，给控件的字体赋予属性并不保证会改变控件的外观。相反，你可以选择应用样式表。
注意：如果 Qt 样式表与 setFont（ 相同小部件使用），则样式表优先，且设置冲突。

**如何使用：** 调用 `font()` 读取当前值；它不会修改应用状态。

### `QRect frameGeometry() const`

**作用与语义：**

小部件相对于其父节点的几何体，包括任何窗口框架。
关于窗口几何问题的概述，请参见 Window Geometry 文档。
默认情况下，该属性包含一个取决于用户平台和屏幕几何形状的值。

**如何使用：** 调用 `frameGeometry()` 读取当前值；它不会修改应用状态。

### `QSize frameSize() const`

**作用与语义：**

该属性包含了包括任何窗口框在内的小部件大小。
默认情况下，该属性包含一个取决于用户平台和屏幕几何形状的值。

**如何使用：** 调用 `frameSize()` 读取当前值；它不会修改应用状态。

### `const QRect & geometry() const`

**作用与语义：**

该属性表示了小部件相对于其父节点的几何形状，排除窗口框架。
更改几何体时，如果控件可见，会立即接收移动事件（`moveEvent()`）和/或调整大小事件（`resizeEvent()`）。如果控件当前不可见，保证在展示前收到相应事件。
如果尺寸分量超出`minimumSize()`和`maximumSize()`定义范围，则会进行调整。
警告：在`resizeEvent()`或`moveEvent()`中调用 setGeometry() 可能导致无限递归。
关于窗口几何问题的概述，请参见 Window Geometry 文档。
默认情况下，该属性包含一个取决于用户平台和屏幕几何形状的值。

**如何使用：** 调用 `geometry()` 读取当前值；它不会修改应用状态。

### `bool hasFocus() const`

**作用与语义：**

该属性在该控件（或其焦点代理）拥有键盘输入焦点时都成立。
默认情况下，该属性为`false`。
注意：获取该属性的值实际上等同于检查`QApplication::focusWidget()`是否指该控件。

**如何使用：** 调用 `hasFocus()` 读取当前值；它不会修改应用状态。

### `bool hasMouseTracking() const`

**作用与语义：**

该属性决定了小部件是否启用了鼠标追踪功能。
如果关闭了鼠标追踪（默认），小部件只有在移动鼠标时至少按下一个鼠标按钮时才会收到鼠标移动事件。
如果启用了鼠标追踪，即使没有按键，小部件也会接收鼠标移动事件。

**如何使用：** 调用 `hasMouseTracking()` 读取当前值；它不会修改应用状态。

### `bool hasTabletTracking() const`

**作用与语义：**

该属性决定了小部件是否启用平板追踪。
如果启用了平板追踪（默认设置），小部件只有在触控笔与绘图板接触时，或至少在触控笔移动时按下一个触控笔按钮时，才会收到平板移动事件。
如果启用了平板追踪，小部件即使在靠近时也会接收平板移动事件。这对于监控位置以及旋转和倾斜等辅助属性以及在界面中提供反馈非常有用。

**如何使用：** 调用 `hasTabletTracking()` 读取当前值；它不会修改应用状态。

### `int height() const`

**作用与语义：**

该属性表示小部件的高度，但不包括任何窗框。
关于窗口几何问题的概述，请参见 Window Geometry 文档。
默认情况下，该属性包含一个取决于用户平台和屏幕几何形状的值。

**如何使用：** 调用 `height()` 读取当前值；它不会修改应用状态。

### `Qt::InputMethodHints inputMethodHints() const`

**作用与语义：**

具体输入法提示是什么？
这仅适用于输入小部件。输入法用它来获取输入法应如何操作的提示。例如，如果设置了`Qt::ImhFormattedNumbersOnly`标志，输入法可能会改变其视觉成分，以反映只能输入数字。
警告：有些小部件需要某些标志才能正常工作。要设置标志，请用`w->setInputMethodHints(w->inputMethodHints()|f)`代替`w->setInputMethodHints(f)`。
注意：这些标志只是提示，因此特定的输入法实现可以忽略它们。如果你想确保输入某种类型的字符，也应该在小部件上设置一个`QValidator`。
默认值是`Qt::ImhNone`。

**如何使用：** 调用 `inputMethodHints()` 读取当前值；它不会修改应用状态。

### `bool isActiveWindow() const`

**作用与语义：**

该属性决定该控件的窗口是否为活跃窗口。
活动窗口是包含带有键盘焦点的控件的窗口（如果窗口没有控件或其控件中没有控件，则可能仍有焦点）。
当弹窗可见时，该属性对激活窗口和弹窗都`true`。
默认情况下，该属性为`false`。

**如何使用：** 调用 `isActiveWindow()` 读取当前值；它不会修改应用状态。

### `bool isEnabled() const`

**作用与语义：**

该属性决定小部件是否被启用。
通常，启用的小部件处理键盘和鼠标事件;禁用小部件则不处理。`QAbstractButton` 有例外。
有些小部件在禁用时会以不同的方式显示自己。例如，某个按钮可能会把标签画成灰色。如果你的小部件需要知道自己何时被启用或禁用，可以使用类型为`QEvent::EnabledChange`的`changeEvent()`。
禁用一个小部件会隐式禁用其所有子组件。分别启用则使所有子小部件都被启用，除非它们已被显式禁用。在父小部件仍然被禁用时，不可能显式启用非窗口的子小部件。
默认情况下，该属性为`true`。

**如何使用：** 调用 `isEnabled()` 读取当前值；它不会修改应用状态。

### `bool isFullScreen() const`

**作用与语义：**

该属性是否显示该小部件以全屏模式显示时依然适用。
全屏模式下的小部件占据整个屏幕区域，不会显示窗口装饰，如标题栏。
默认情况下，该属性为`false`。

**如何使用：** 调用 `isFullScreen()` 读取当前值；它不会修改应用状态。

### `bool isMaximized() const`

**作用与语义：**

该属性在该小部件是否被最大化时成立。
这个属性只适用于窗户。
注意：由于某些窗口系统的限制，这并不总是报告预期结果（例如，如果用户在X11上通过窗口管理器最大化窗口，Qt无法将此与其他调整大小区分开来）。随着窗口管理器协议的发展，这种情况预计会有所改善。
默认情况下，该属性为`false`。

**如何使用：** 调用 `isMaximized()` 读取当前值；它不会修改应用状态。

### `bool isMinimized() const`

**作用与语义：**

该属性决定该小部件是否被最小化（图标化）。
这个属性只适用于窗户。
默认情况下，该属性为`false`。

**如何使用：** 调用 `isMinimized()` 读取当前值；它不会修改应用状态。

### `bool isModal() const`

**作用与语义：**

该属性决定了该控件是否为模态控件。
这个属性只适用于窗口。模态小部件阻止其他窗口中的小部件接收任何输入。
默认情况下，该属性是`false`。

**如何使用：** 调用 `isModal()` 读取当前值；它不会修改应用状态。

### `bool isVisible() const`

**作用与语义：**

该属性决定小部件是否可见。
调用 setVisible（true） 或 `show()` 会将控件设置为可见状态，前提是其所有父控件直到窗口都可见。如果祖先未被看见，控件在所有祖先显示完毕后才会显现。如果控件的大小或位置发生变化，Qt 保证控件在显示前会触发移动和调整大小事件。如果控件尚未调整大小，Qt 会用 `adjustSize()` 调整控件大小为有用的默认值。
调用 setVisible（false） 或 `hide()` 会显式隐藏一个控件。显式隐藏控件永远不会变得可见，即使它的所有祖先都变得可见，除非你展示它。
当控件的可见性状态发生变化时，小部件会接收显示和隐藏事件。在隐藏和显示事件之间，无需浪费CPU周期来准备或显示信息给用户。例如，视频应用可能只是停止生成新帧。
被屏幕上其他窗口遮挡的控件被视为可见。同样适用于图标窗口以及存在于另一个虚拟桌面上的窗口（支持该概念的平台）。当窗口系统改变控件的映射状态时，控件会接收自发的显示和隐藏事件，例如用户最小化窗口时会触发自发隐藏事件，窗口恢复时则会触发自发显示事件。
你很少需要重新实现 setVisible() 函数。如果你需要在显示小部件前更改某些设置，可以用 `showEvent()`。如果需要延迟初始化，可以使用传递给 `event()` 函数的波兰事件。

**如何使用：** 调用 `isVisible()` 读取当前值；它不会修改应用状态。

### `bool isWindowModified() const`

**作用与语义：**

该属性决定窗口中显示的文档是否存在未保存的更改。
修改后的窗口是指内容发生变化但尚未保存到磁盘的窗口。该标志会因平台而异，效果各异。在macOS上，关闭按钮会有修改后的外观;在其他平台上，窗口标题会带有“*”（星号）。
窗口标题必须包含“[*]”占位符，指示“*”应出现在位置。通常，*应紧随文件名后面出现（例如，“document1.txt[*] - 文本编辑器”）。如果窗口未被修改，占位符会被直接移除。
注意，如果一个小部件被设置为修改，它的所有祖先也会被设置为被修改。然而，如果你调用`setWindowModified(false)`，这个功能不会传播到它的父节点，因为父节点的其他子节点可能也被修改过。

**如何使用：** 调用 `isWindowModified()` 读取当前值；它不会修改应用状态。

### `Qt::LayoutDirection layoutDirection() const`

**作用与语义：**

此属性保存该控件的布局方向。
注意：此方法自 Qt 4.7 后不再影响文本布局方向。
默认情况下，该属性设置为 `Qt::LeftToRight`。
当在控件上设置布局方向时，它会传播到控件的子控件，但不会传播到作为窗口的子控件，也不会传播给已明确调用 setLayoutDirection() 的子控件。此外，在父控件调用 setLayoutDirection() 后添加的子控件不会继承父控件的布局方向。

**如何使用：** 调用 `layoutDirection()` 读取当前值；它不会修改应用状态。

### `QLocale locale() const`

**作用与语义：**

此属性保存小部件的区域设置。
只要未设置特殊区域设置，此属性为父组件的区域设置，或者如果该小部件是顶层小部件，则为默认区域设置。
如果小部件显示日期或数字，应使用小部件的区域设置进行格式化。

**如何使用：** 调用 `locale()` 读取当前值；它不会修改应用状态。

### `int maximumHeight() const`

**作用与语义：**

此属性保存小部件的最大高度（像素）。
此属性对应 `maximumSize` 属性保存的高度。
默认情况下，此属性的值为 16777215。
注意：`QWIDGETSIZE_MAX` 宏的定义限制了小部件的最大尺寸。

**如何使用：** 调用 `maximumHeight()` 读取当前值；它不会修改应用状态。

### `QSize maximumSize() const`

**作用与语义：**

此属性保存小部件的最大尺寸（像素）。
小部件不能调整为超过最大小部件尺寸的大小。
默认情况下，此属性的尺寸的宽度和高度均为 16777215。
注意：`QWIDGETSIZE_MAX` 宏的定义限制了小部件的最大尺寸。

**如何使用：** 调用 `maximumSize()` 读取当前值；它不会修改应用状态。

### `int maximumWidth() const`

**作用与语义：**

此属性保存小部件的最大宽度（像素）。
此属性对应 `maximumSize` 属性保存的宽度。
默认情况下，此属性的值为 16777215。
注意：`QWIDGETSIZE_MAX` 宏的定义限制了小部件的最大尺寸。

**如何使用：** 调用 `maximumWidth()` 读取当前值；它不会修改应用状态。

### `int minimumHeight() const`

**作用与语义：**

此属性保存小部件的最小高度（像素）。
此属性对应 `minimumSize` 属性保存的高度。
默认情况下，此属性的值为 0。

**如何使用：** 调用 `minimumHeight()` 读取当前值；它不会修改应用状态。

### `QSize minimumSize() const`

**作用与语义：**

此属性保存小部件的最小尺寸。
小部件不能调整为小于最小小部件尺寸的大小。如果当前尺寸较小，小部件的尺寸将被强制为最小尺寸。
此函数设置的最小尺寸将覆盖 `QLayout` 定义的最小尺寸。要取消设置最小尺寸，请使用 `QSize(0, 0)` 的值。
默认情况下，此属性包含宽度和高度均为零的尺寸。

**如何使用：** 调用 `minimumSize()` 读取当前值；它不会修改应用状态。

### `virtual QSize minimumSizeHint() const`

**作用与语义：**

该属性表示该小部件的推荐最小尺寸。
如果该属性的值是无效的大小，则不建议设定最小大小。
默认实现的 minimumSizeHint() 如果该控件没有布局，则返回无效大小，否则返回布局的最小大小。大多数内置控件会重现 minimumSizeHint()。
除非设置了`minimumSize()`或将大小策略设置为QSizePolicy：：Ignore，否则`QLayout`永远不会将小于最小大小提示的大小。如果`minimumSize()`设置，最小大小提示将被忽略。

**如何使用：** 调用 `minimumSizeHint()` 读取当前值；它不会修改应用状态。

### `int minimumWidth() const`

**作用与语义：**

此属性保存小部件的最小宽度（像素）。
此属性对应 `minimumSize` 属性保存的宽度。
默认情况下，此属性的值为 0。

**如何使用：** 调用 `minimumWidth()` 读取当前值；它不会修改应用状态。

### `void move(const QPoint &)`

**作用与语义：**

该属性表示该控件在其父控件中的位置。
如果小部件是窗口，则该小部件在桌面上的位置，包括其框架。
当调整位置时，如果控件可见，会立即接收移动事件（`moveEvent()`）。如果控件当前不可见，则保证在显示前收到事件。
默认情况下，该属性包含指向原点的位置。
警告：在 `moveEvent()` 内调用 move() 或 `setGeometry()` 可能导致无限递归。
关于窗口几何问题的概述，请参见 Window Geometry 文档。
注意：并非所有窗口系统都支持设置或查询顶层窗口位置。在此类系统中，程序移动窗口可能无效，且当前位置（如`QPoint(0, 0)`）可能会返回人工值。

**如何使用：** 调用 `move()` 读取当前值；它不会修改应用状态。

### `QRect normalGeometry() const`

**作用与语义：**

该属性保留了该小部件在以正常（非最大化或全屏）顶层小部件显示时的几何形状。
如果小部件已经处于该状态，法线几何体将反映小部件当前的 `geometry()`。
对于子控件，该属性总是包含一个空矩形。
默认情况下，该属性包含一个空矩形。

**如何使用：** 调用 `normalGeometry()` 读取当前值；它不会修改应用状态。

### `const QPalette & palette() const`

**作用与语义：**

该属性包含了小部件的调色板。
该属性描述了小部件的调色板。调色板被控件的样式用于渲染标准组件，并作为确保自定义小部件能够保持与原生平台外观和感觉一致的手段。不同平台或不同样式通常会有不同的调色板。
当你为小部件分配新调色板时，该调色板中的颜色角色会与小部件的默认调色板合并，形成小部件的最终调色板。小部件背景角色的调色板条目用于填充小部件的背景（见 `QWidget::autoFillBackground`），前景角色初始化`QPainter`的笔。
默认选项取决于系统环境。`QApplication`维护一个系统/主题调色板，作为所有控件的默认选项。某些类型的控件可能还有特殊的调色板默认值（例如，在 Windows Vista 上，所有源自 `QMenuBar` 的类都有特殊的默认调色板）。你也可以通过传递自定义调色板和控件名称给 `QApplication::setPalette()`，自己定义控件的默认调色板。最后，样式始终有选项，可以根据分配来润色调色板（参见 `QStyle::polish()`）。
`QWidget` 会将显式调色板角色从父节点传播到子节点。如果你为调色板上的特定角色分配画笔或颜色，并将该调色板分配给小部件，该角色会传播到该小部件的所有子节点，覆盖该角色的任何系统默认设置。注意，调色板默认不会传播到窗口（参见`isWindow()`），除非启用了`Qt::WA_WindowPropagation`属性。
`QWidget` 的调色板传播与字体传播相似。
当前样式用于渲染所有标准Qt控件的内容，可以自由选择组件调色板中的颜色和笔刷，或者在某些情况下（部分或完全）忽略调色板。特别是，像GTK样式、Mac样式和Windows Vista样式等样式依赖第三方API来渲染控件内容，而这些样式通常不遵循调色板。因此，给控件调色板分配角色并不保证改变控件的外观。相反，你可以选择应用样式表。
警告：请勿将此功能与 Qt 样式表结合使用。使用样式表时，控件的调色板可以通过“color”、“background-color”、“selection-color”、“selection-background-color”和“alternate-background-color”来自定义。

**如何使用：** 调用 `palette()` 读取当前值；它不会修改应用状态。

### `QPoint pos() const`

**作用与语义：**

该属性表示该控件在其父控件中的位置。
如果小部件是窗口，则该小部件在桌面上的位置，包括其框架。
当调整位置时，如果控件可见，会立即接收移动事件（`moveEvent()`）。如果控件当前不可见，则保证在显示前收到事件。
默认情况下，该属性包含指向原点的位置。
警告：在 `moveEvent()` 内调用 move() 或 `setGeometry()` 可能导致无限递归。
关于窗口几何问题的概述，请参见 Window Geometry 文档。
注意：并非所有窗口系统都支持设置或查询顶层窗口位置。在此类系统中，程序移动窗口可能无效，且当前位置（如`QPoint(0, 0)`）可能会返回人工值。

**如何使用：** 调用 `pos()` 读取当前值；它不会修改应用状态。

### `QRect rect() const`

**作用与语义：**

该属性包含了不包含任何窗框的组件内部几何形状。
rect属性等于`QRect`（0， 0， `width()`， `height()`）。
关于窗口几何问题的概述，请参见 Window Geometry 文档。
默认情况下，该属性包含一个取决于用户平台和屏幕几何形状的值。

**如何使用：** 调用 `rect()` 读取当前值；它不会修改应用状态。

### `void resize(const QSize &)`

**作用与语义：**

该属性表示了小部件的大小，但不包括任何窗口框。
如果控件在调整大小时可见，则会立即收到一个调整大小事件（`resizeEvent()`）。如果控件当前不可见，则保证在显示前收到事件。
如果尺寸超出`minimumSize()`和`maximumSize()`定义范围，则调整。
默认情况下，该属性包含一个取决于用户平台和屏幕几何形状的值。
警告：在 `resizeEvent()` 内调用 resize() 或 `setGeometry()` 可能导致无限递归。
注意：将大小设置为`QSize(0, 0)`会导致小部件不会出现在屏幕上。这同样适用于Windows。

**如何使用：** 调用 `resize()` 读取当前值；它不会修改应用状态。

### `void setAcceptDrops(bool on)`

**作用与语义：**

该属性决定该控件是否启用掉落事件。
将该属性设置为 true，会向系统宣布该控件可能能够接受丢弃事件。
警告：请勿在拖放事件处理程序中修改该属性。
默认情况下，该属性为`false`。

**如何使用：** 调用 `setAcceptDrops(...)` 修改 `acceptDrops`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setAccessibleDescription(const QString &description)`

**作用与语义：**

该属性包含辅助技术中控件的描述。
控件的可访问描述应传达控件的功能。虽然`accessibleName`应是简短且简洁的字符串（例如保存），但描述应提供更多上下文，比如保存当前文档。
这个属性必须是本地化的。
默认情况下，该属性包含空字符串，Qt 会回退到使用工具提示来提供这些信息。

**如何使用：** 调用 `setAccessibleDescription(...)` 修改 `accessibleDescription`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setAccessibleIdentifier(const QString &identifier)`

**作用与语义：**

此属性保存辅助技术中看到的小部件标识符。
如果设置，辅助技术可以使用小部件的可访问标识符来识别特定的小部件，例如在自动化测试中。

**如何使用：** 调用 `setAccessibleIdentifier(...)` 修改 `accessibleIdentifier`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setAccessibleName(const QString &name)`

**作用与语义：**

此属性保存辅助技术中看到的小部件名称。
这是辅助技术（如屏幕阅读器）宣布此小部件的主要名称。对于大多数小部件，不需要设置此属性。例如，对于 `QPushButton`，按钮的文本将被使用。
当小部件不提供任何文本时，设置此属性很重要。例如，仅包含图标的按钮需要设置此属性以配合屏幕阅读器使用。名称应简短，并与小部件传递的视觉信息相当。
此属性必须本地化。
默认情况下，此属性包含空字符串。

**如何使用：** 调用 `setAccessibleName(...)` 修改 `accessibleName`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setAutoFillBackground(bool enabled)`

**作用与语义：**

该属性决定了小部件背景是否自动填充。
如果启用该属性，Qt 会在调用绘画事件前填充小部件的背景。颜色由小部件`palette`的`QPalette::Window`颜色角色定义。
此外，除非设置了WA_OpaquePaintEvent或WA_NoSystemBackground属性，否则Windows总是充满`QPalette::Window`。
如果小部件的父背景是静态渐变，则该属性无法关闭（即设置为 false）。
警告：请谨慎使用该属性与 Qt 样式表一起使用。当小部件拥有有效背景或边框图片的样式表时，该属性会自动被禁用。
默认情况下，该属性是`false`。

**如何使用：** 调用 `setAutoFillBackground(...)` 修改 `autoFillBackground`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setBaseSize(const QSize &)`

**作用与语义：**

该属性包含控件的基准大小。
如果控件定义了`sizeIncrement()`，则使用基准大小来计算合适的控件大小。
默认情况下，对于新创建的控件，该属性包含宽度和高度为零的大小。

**如何使用：** 调用 `setBaseSize(...)` 修改 `baseSize`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setContextMenuPolicy(Qt::ContextMenuPolicy policy)`

**作用与语义：**

小部件如何显示上下文菜单。
该属性的默认值为`Qt::DefaultContextMenu`，意味着调用`contextMenuEvent()`处理程序。其他值有`Qt::NoContextMenu`、`Qt::PreventContextMenu`、`Qt::ActionsContextMenu`和`Qt::CustomContextMenu`。使用`Qt::CustomContextMenu`时，信号`customContextMenuRequested()`被发射。

**如何使用：** 调用 `setContextMenuPolicy(...)` 修改 `contextMenuPolicy`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setCursor(const QCursor &)`

**作用与语义：**

该属性包含该控件的光标形状。
鼠标光标在该控件上方时会呈现该形状。请参阅预定义光标对象列表，了解一系列有用的形状。
编辑器小部件可能会使用工字束光标：
如果没有设置光标，或者在调用 unsetCursor() 后，则使用父游标。
默认情况下，该属性包含一个具有`Qt::ArrowCursor`形状的光标。
有些底层窗口实现如果光标离开了小部件，即使鼠标被抓取，光标也会重置。如果你想为所有小部件设置光标，即使你在窗口外，也可以考虑用`QGuiApplication::setOverrideCursor()`。

**如何使用：** 调用 `setCursor(...)` 修改 `cursor`；传入的新值会成为后续查询和相关界面行为所使用的值。

**官方示例：**

```cpp
 setCursor(Qt::IBeamCursor);
```

### `void setFocusPolicy(Qt::FocusPolicy policy)`

**作用与语义：**

该属性表示了小部件接受键盘焦点的方式。
如果控件通过 Tab 键接受键盘聚焦，`Qt::ClickFocus`如果控件通过点击接受焦点，`Qt::StrongFocus`如果两者都接受， `Qt::NoFocus`（默认）则不接受焦点，该策略是 `Qt::TabFocus`。
如果控件处理键盘事件，您必须启用键盘焦点。这通常由控件的构造函数完成。例如，`QLineEdit`构造函数调用 setFocusPolicy（`Qt::StrongFocus`）。
如果小部件有焦点代理，那么焦点策略会传播到它。

**如何使用：** 调用 `setFocusPolicy(...)` 修改 `focusPolicy`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setFont(const QFont &)`

**作用与语义：**

该属性保留当前为控件设置的字体。
该属性描述了小部件所请求的字体。该字体被小部件的样式用于渲染标准组件，并作为确保自定义小部件能够与原生平台外观和感觉保持一致的手段。不同平台或不同样式通常会为应用程序定义不同的字体。
当你为小部件分配新字体时，该字体的属性会与小部件的默认字体结合，形成小部件的最终字体。你可以调用`fontInfo()`获取小部件最终字体的副本。最终字体也用于初始化`QPainter`字体。
默认字体取决于系统环境。`QApplication`维护一个系统/主题字体，作为所有控件的默认字体。某些类型的控件可能还有特殊的字体默认值。你也可以自己定义控件的默认字体，通过传递自定义字体和控件名称给`QApplication::setFont()`。最后，字体会与Qt的字体数据库匹配，以找到最佳匹配字体。
`QWidget` 会将显式字体属性从父字母传播到子节点。如果你更改字体上的某个属性并将该字体分配给控件，该属性会传播到该控件的所有子节点，覆盖该属性的系统默认设置。注意，除非启用了 `Qt::WA_WindowPropagation` 属性，否则字体默认不会传播到窗口（见 `isWindow()`）。
`QWidget` 的字体传播方式与调色板传播相似。
当前样式用于渲染所有标准 Qt 控件的内容，可以自由选择使用控件字体，或在某些情况下部分或完全忽略它。特别是某些样式如 GTK 样式、Mac 样式和 Windows Vista 样式，会对控件字体进行特殊修改，以匹配平台的原生外观和感觉。因此，给控件的字体赋予属性并不保证会改变控件的外观。相反，你可以选择应用样式表。
注意：如果 Qt 样式表与 setFont（ 相同小部件使用），则样式表优先，且设置冲突。

**如何使用：** 调用 `setFont(...)` 修改 `font`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setGeometry(const QRect &)`

**作用与语义：**

该属性表示了小部件相对于其父节点的几何形状，排除窗口框架。
更改几何体时，如果控件可见，会立即接收移动事件（`moveEvent()`）和/或调整大小事件（`resizeEvent()`）。如果控件当前不可见，保证在展示前收到相应事件。
如果尺寸分量超出`minimumSize()`和`maximumSize()`定义范围，则会进行调整。
警告：在`resizeEvent()`或`moveEvent()`中调用 setGeometry() 可能导致无限递归。
关于窗口几何问题的概述，请参见 Window Geometry 文档。
默认情况下，该属性包含一个取决于用户平台和屏幕几何形状的值。

**如何使用：** 调用 `setGeometry(...)` 修改 `geometry`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setInputMethodHints(Qt::InputMethodHints hints)`

**作用与语义：**

具体输入法提示是什么？
这仅适用于输入小部件。输入法用它来获取输入法应如何操作的提示。例如，如果设置了`Qt::ImhFormattedNumbersOnly`标志，输入法可能会改变其视觉成分，以反映只能输入数字。
警告：有些小部件需要某些标志才能正常工作。要设置标志，请用`w->setInputMethodHints(w->inputMethodHints()|f)`代替`w->setInputMethodHints(f)`。
注意：这些标志只是提示，因此特定的输入法实现可以忽略它们。如果你想确保输入某种类型的字符，也应该在小部件上设置一个`QValidator`。
默认值是`Qt::ImhNone`。

**如何使用：** 调用 `setInputMethodHints(...)` 修改 `inputMethodHints`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setLayoutDirection(Qt::LayoutDirection direction)`

**作用与语义：**

此属性保存该控件的布局方向。
注意：此方法自 Qt 4.7 后不再影响文本布局方向。
默认情况下，该属性设置为 `Qt::LeftToRight`。
当在控件上设置布局方向时，它会传播到控件的子控件，但不会传播到作为窗口的子控件，也不会传播给已明确调用 setLayoutDirection() 的子控件。此外，在父控件调用 setLayoutDirection() 后添加的子控件不会继承父控件的布局方向。

**如何使用：** 调用 `setLayoutDirection(...)` 修改 `layoutDirection`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setLocale(const QLocale &locale)`

**作用与语义：**

此属性保存小部件的区域设置。
只要未设置特殊区域设置，此属性为父组件的区域设置，或者如果该小部件是顶层小部件，则为默认区域设置。
如果小部件显示日期或数字，应使用小部件的区域设置进行格式化。

**如何使用：** 调用 `setLocale(...)` 修改 `locale`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMaximumHeight(int maxh)`

**作用与语义：**

此属性保存小部件的最大高度（像素）。
此属性对应 `maximumSize` 属性保存的高度。
默认情况下，此属性的值为 16777215。
注意：`QWIDGETSIZE_MAX` 宏的定义限制了小部件的最大尺寸。

**如何使用：** 调用 `setMaximumHeight(...)` 修改 `maximumHeight`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMaximumSize(const QSize &)`

**作用与语义：**

此属性保存小部件的最大尺寸（像素）。
小部件不能调整为超过最大小部件尺寸的大小。
默认情况下，此属性的尺寸的宽度和高度均为 16777215。
注意：`QWIDGETSIZE_MAX` 宏的定义限制了小部件的最大尺寸。

**如何使用：** 调用 `setMaximumSize(...)` 修改 `maximumSize`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMaximumWidth(int maxw)`

**作用与语义：**

此属性保存小部件的最大宽度（像素）。
此属性对应 `maximumSize` 属性保存的宽度。
默认情况下，此属性的值为 16777215。
注意：`QWIDGETSIZE_MAX` 宏的定义限制了小部件的最大尺寸。

**如何使用：** 调用 `setMaximumWidth(...)` 修改 `maximumWidth`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMinimumHeight(int minh)`

**作用与语义：**

此属性保存小部件的最小高度（像素）。
此属性对应 `minimumSize` 属性保存的高度。
默认情况下，此属性的值为 0。

**如何使用：** 调用 `setMinimumHeight(...)` 修改 `minimumHeight`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMinimumSize(const QSize &)`

**作用与语义：**

此属性保存小部件的最小尺寸。
小部件不能调整为小于最小小部件尺寸的大小。如果当前尺寸较小，小部件的尺寸将被强制为最小尺寸。
此函数设置的最小尺寸将覆盖 `QLayout` 定义的最小尺寸。要取消设置最小尺寸，请使用 `QSize(0, 0)` 的值。
默认情况下，此属性包含宽度和高度均为零的尺寸。

**如何使用：** 调用 `setMinimumSize(...)` 修改 `minimumSize`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMinimumWidth(int minw)`

**作用与语义：**

此属性保存小部件的最小宽度（像素）。
此属性对应 `minimumSize` 属性保存的宽度。
默认情况下，此属性的值为 0。

**如何使用：** 调用 `setMinimumWidth(...)` 修改 `minimumWidth`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMouseTracking(bool enable)`

**作用与语义：**

该属性决定了小部件是否启用了鼠标追踪功能。
如果关闭了鼠标追踪（默认），小部件只有在移动鼠标时至少按下一个鼠标按钮时才会收到鼠标移动事件。
如果启用了鼠标追踪，即使没有按键，小部件也会接收鼠标移动事件。

**如何使用：** 调用 `setMouseTracking(...)` 修改 `mouseTracking`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setPalette(const QPalette &)`

**作用与语义：**

该属性包含了小部件的调色板。
该属性描述了小部件的调色板。调色板被控件的样式用于渲染标准组件，并作为确保自定义小部件能够保持与原生平台外观和感觉一致的手段。不同平台或不同样式通常会有不同的调色板。
当你为小部件分配新调色板时，该调色板中的颜色角色会与小部件的默认调色板合并，形成小部件的最终调色板。小部件背景角色的调色板条目用于填充小部件的背景（见 `QWidget::autoFillBackground`），前景角色初始化`QPainter`的笔。
默认选项取决于系统环境。`QApplication`维护一个系统/主题调色板，作为所有控件的默认选项。某些类型的控件可能还有特殊的调色板默认值（例如，在 Windows Vista 上，所有源自 `QMenuBar` 的类都有特殊的默认调色板）。你也可以通过传递自定义调色板和控件名称给 `QApplication::setPalette()`，自己定义控件的默认调色板。最后，样式始终有选项，可以根据分配来润色调色板（参见 `QStyle::polish()`）。
`QWidget` 会将显式调色板角色从父节点传播到子节点。如果你为调色板上的特定角色分配画笔或颜色，并将该调色板分配给小部件，该角色会传播到该小部件的所有子节点，覆盖该角色的任何系统默认设置。注意，调色板默认不会传播到窗口（参见`isWindow()`），除非启用了`Qt::WA_WindowPropagation`属性。
`QWidget` 的调色板传播与字体传播相似。
当前样式用于渲染所有标准Qt控件的内容，可以自由选择组件调色板中的颜色和笔刷，或者在某些情况下（部分或完全）忽略调色板。特别是，像GTK样式、Mac样式和Windows Vista样式等样式依赖第三方API来渲染控件内容，而这些样式通常不遵循调色板。因此，给控件调色板分配角色并不保证改变控件的外观。相反，你可以选择应用样式表。
警告：请勿将此功能与 Qt 样式表结合使用。使用样式表时，控件的调色板可以通过“color”、“background-color”、“selection-color”、“selection-background-color”和“alternate-background-color”来自定义。

**如何使用：** 调用 `setPalette(...)` 修改 `palette`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setSizeIncrement(const QSize &)`

**作用与语义：**

该属性包含小部件的大小增量。
当用户调整窗口大小时，尺寸将以 sizeIncrement() 为步骤移动。`width()` 像素水平，sizeIncrement.`height()` 像素垂直，`baseSize()` 作为基底。首选控件大小为非负整数 i 和 j：
注意，虽然你可以为所有小部件设置大小增量，但这只影响窗口。
默认情况下，该属性包含宽度和高度均为零的大小。
警告：在 Windows 下，大小递增无效，X11 上的窗口管理器可能会忽略它。

**如何使用：** 调用 `setSizeIncrement(...)` 修改 `sizeIncrement`；传入的新值会成为后续查询和相关界面行为所使用的值。

**官方示例：**

```cpp
 width = baseSize().width() + i * sizeIncrement().width();
 height = baseSize().height() + j * sizeIncrement().height();
```

### `void setSizePolicy(QSizePolicy)`

**作用与语义：**

该属性保留了小部件的默认布局行为。
如果存在管理该控件子节点的 `QLayout`，则使用该布局指定的大小策略。如果没有这样的`QLayout`，则使用该函数的结果。
默认策略为“Preferred/Preferred”，这意味着小部件可以自由调整大小，但优先选择返回的大小`sizeHint()`。类似按钮的小部件设置大小策略，指定它们可以横向拉伸，但垂直方向是固定的。同样适用于行编辑控件（如`QLineEdit`、`QSpinBox`或可编辑`QComboBox`）以及其他横向控件（如`QProgressBar`）。`QToolButton`通常是方形的，因此允许双向扩展。支持不同方向的小部件（如`QSlider`、`QScrollBar`或QHeader）只指定相应方向的拉伸。能够提供滚动条的小部件（通常是`QScrollArea`子类）通常会指定它们可以使用额外空间，并且能用少于`sizeHint()`的空间。

**如何使用：** 调用 `setSizePolicy(...)` 修改 `sizePolicy`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setStatusTip(const QString &)`

**作用与语义：**

该属性包含小部件的状态提示。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `setStatusTip(...)` 修改 `statusTip`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTabletTracking(bool enable)`

**作用与语义：**

该属性决定了小部件是否启用平板追踪。
如果启用了平板追踪（默认设置），小部件只有在触控笔与绘图板接触时，或至少在触控笔移动时按下一个触控笔按钮时，才会收到平板移动事件。
如果启用了平板追踪，小部件即使在靠近时也会接收平板移动事件。这对于监控位置以及旋转和倾斜等辅助属性以及在界面中提供反馈非常有用。

**如何使用：** 调用 `setTabletTracking(...)` 修改 `tabletTracking`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setToolTip(const QString &)`

**作用与语义：**

该属性包含小部件的工具提示。
请注意，默认情况下，工具提示只显示在活动窗口子组件上。你可以通过在窗口设置属性`Qt::WA_AlwaysShowToolTips`来改变这种行为，而不是在带有提示的小部件上。
如果你想控制提示的行为，可以拦截`event()`函数并捕捉`QEvent::ToolTip`事件（例如，如果你想自定义提示应显示的区域）。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `setToolTip(...)` 修改 `toolTip`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setToolTipDuration(int msec)`

**作用与语义：**

该属性包含了小部件在提示中的持续时间。
指定提示显示的时间长度，单位为毫秒。如果值为 -1（默认），则持续时间根据提示长度计算。

**如何使用：** 调用 `setToolTipDuration(...)` 修改 `toolTipDuration`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setUpdatesEnabled(bool enable)`

**作用与语义：**

该属性决定是否启用更新。
启用更新的小部件会接收绘图事件并有系统背景;禁用的小部件则不会。这也意味着如果更新被禁用，调用`update()`和`repaint()`不会有影响。
默认情况下，该属性为`true`。
setUpdatesEnabled() 通常用于短时间禁用更新，例如避免大变更时的屏幕闪烁。在 Qt 中，控件通常不会产生屏幕闪烁，但在 X11 上，当控件隐藏时，服务器可能会在被其他控件替换前清除屏幕上的区域。禁用更新可以解决这个问题。
禁用小部件会隐式禁用其所有子组件。启用小部件会启用除顶层小部件或已明确禁用的子小部件外的所有子小部件。重新启用更新隐式调用该小部件的`update()`。

**如何使用：** 调用 `setUpdatesEnabled(...)` 修改 `updatesEnabled`；传入的新值会成为后续查询和相关界面行为所使用的值。

**官方示例：**

```cpp
 setUpdatesEnabled(false);
 bigVisualChanges();
 setUpdatesEnabled(true);
```

### `void setWhatsThis(const QString &)`

**作用与语义：**

该属性包含小部件的“What's This 帮助文本。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `setWhatsThis(...)` 修改 `whatsThis`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setWindowFilePath(const QString &filePath)`

**作用与语义：**

该属性包含与控件相关的文件路径。
这个属性只对 Windows 有意义。它将文件路径与窗口关联起来。如果你设置了文件路径但没有设置窗口标题，Qt 会将窗口标题设置为指定路径的文件名，该路径是通过 `QFileInfo::fileName()` 获得的。
如果窗口标题在任意点被设置，那么窗口标题优先，会显示它而不是文件路径字符串。
此外，在macOS上，这还有一个额外好处，就是假设文件路径存在，它会设置窗口的代理图标。
如果没有设置文件路径，该属性包含一个空字符串。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `setWindowFilePath(...)` 修改 `windowFilePath`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setWindowFlags(Qt::WindowFlags type)`

**作用与语义：**

窗口标志是类型（例如`Qt::Dialog`）和零个或多个窗口系统的提示（例如`Qt::FramelessWindowHint`）的组合。
如果小部件类型为`Qt::Widget`或`Qt::SubWindow`，并且变成了窗口（`Qt::Window`、`Qt::Dialog`等），则它会被放在桌面上的位置（0， 0）。如果小部件是窗口，并且变成`Qt::Widget`或`Qt::SubWindow`，则它相对于父小部件的位置（0， 0）。
注意：该函数在更改窗口标志时调用`setParent()`，导致控件被隐藏。您必须调用`show()`才能让控件再次可见。

**如何使用：** 调用 `setWindowFlags(...)` 修改 `windowFlags`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setWindowIcon(const QIcon &icon)`

**作用与语义：**

此属性保存小部件的图标。
此属性仅适用于窗口。如果没有设置图标，windowIcon() 将返回应用程序图标 (`QApplication::windowIcon()`)。
注意：在 macOS 上，窗口图标表示活动文档，除非使用 `setWindowFilePath` 设置了文件路径，否则不会显示。

**如何使用：** 调用 `setWindowIcon(...)` 修改 `windowIcon`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setWindowModality(Qt::WindowModality windowModality)`

**作用与语义：**

该属性决定了模态控件阻挡的窗口。
该属性仅适用于窗口。模态控件防止其他窗口中的控件接收输入。该属性的值控制控件可见时哪些窗口被阻挡。窗口可见时更改该属性无效;你必须先`hide()`控件，然后再`show()`。
默认情况下，该属性是`Qt::NonModal`。

**如何使用：** 调用 `setWindowModality(...)` 修改 `windowModality`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setWindowOpacity(qreal level)`

**作用与语义：**

该属性表示了窗口的不透明度水平。
有效不透明度范围为1.0（完全不透明）到0.0（完全透明）。
默认情况下，该属性的价值为1.0。
该功能可在支持复合扩展的嵌入式Linux、macOS、Windows和X11平台上使用。
注意：在 X11 上你需要运行复合管理器，并且你使用的窗口管理器必须支持 X11 专用的 _NET_WM_WINDOW_OPACITY Atom。
警告：将此属性从不透明改为透明可能会触发绘画事件，需要在窗口正确显示前处理。这主要影响`QScreen::grabWindow()`的使用。还要注意，半透明窗口的更新和调整速度明显慢于不透明窗口。

**如何使用：** 调用 `setWindowOpacity(...)` 修改 `windowOpacity`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QSize size() const`

**作用与语义：**

该属性表示了小部件的大小，但不包括任何窗口框。
如果控件在调整大小时可见，则会立即收到一个调整大小事件（`resizeEvent()`）。如果控件当前不可见，则保证在显示前收到事件。
如果尺寸超出`minimumSize()`和`maximumSize()`定义范围，则调整。
默认情况下，该属性包含一个取决于用户平台和屏幕几何形状的值。
警告：在 `resizeEvent()` 内调用 resize() 或 `setGeometry()` 可能导致无限递归。
注意：将大小设置为`QSize(0, 0)`会导致小部件不会出现在屏幕上。这同样适用于Windows。

**如何使用：** 调用 `size()` 读取当前值；它不会修改应用状态。

### `virtual QSize sizeHint() const`

**作用与语义：**

该属性包含该小部件的推荐大小。
如果该属性的值为无效大小，则不建议使用大小。
如果该控件没有布局，默认实现的 sizeHint() 会返回无效大小，否则返回布局的首选大小。

**如何使用：** 调用 `sizeHint()` 读取当前值；它不会修改应用状态。

### `QSize sizeIncrement() const`

**作用与语义：**

该属性包含小部件的大小增量。
当用户调整窗口大小时，尺寸将以 sizeIncrement() 为步骤移动。`width()` 像素水平，sizeIncrement.`height()` 像素垂直，`baseSize()` 作为基底。首选控件大小为非负整数 i 和 j：
注意，虽然你可以为所有小部件设置大小增量，但这只影响窗口。
默认情况下，该属性包含宽度和高度均为零的大小。
警告：在 Windows 下，大小递增无效，X11 上的窗口管理器可能会忽略它。

**如何使用：** 调用 `sizeIncrement()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 width = baseSize().width() + i * sizeIncrement().width();
 height = baseSize().height() + j * sizeIncrement().height();
```

### `QSizePolicy sizePolicy() const`

**作用与语义：**

该属性保留了小部件的默认布局行为。
如果存在管理该控件子节点的 `QLayout`，则使用该布局指定的大小策略。如果没有这样的`QLayout`，则使用该函数的结果。
默认策略为“Preferred/Preferred”，这意味着小部件可以自由调整大小，但优先选择返回的大小`sizeHint()`。类似按钮的小部件设置大小策略，指定它们可以横向拉伸，但垂直方向是固定的。同样适用于行编辑控件（如`QLineEdit`、`QSpinBox`或可编辑`QComboBox`）以及其他横向控件（如`QProgressBar`）。`QToolButton`通常是方形的，因此允许双向扩展。支持不同方向的小部件（如`QSlider`、`QScrollBar`或QHeader）只指定相应方向的拉伸。能够提供滚动条的小部件（通常是`QScrollArea`子类）通常会指定它们可以使用额外空间，并且能用少于`sizeHint()`的空间。

**如何使用：** 调用 `sizePolicy()` 读取当前值；它不会修改应用状态。

### `QString statusTip() const`

**作用与语义：**

该属性包含小部件的状态提示。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `statusTip()` 读取当前值；它不会修改应用状态。

### `QString styleSheet() const`

**作用与语义：**

该属性包含小部件的样式表。
样式表包含了对小部件样式的自定义描述，详见 Qt 样式表文档。
自 Qt 4.5 起，Qt 样式表已完全支持 macOS。
警告：Qt 样式表目前不支持 custom `QStyle` 子类。我们计划在未来某个版本中解决这个问题。

**如何使用：** 调用 `styleSheet()` 读取当前值；它不会修改应用状态。

### `QString toolTip() const`

**作用与语义：**

该属性包含小部件的工具提示。
请注意，默认情况下，工具提示只显示在活动窗口子组件上。你可以通过在窗口设置属性`Qt::WA_AlwaysShowToolTips`来改变这种行为，而不是在带有提示的小部件上。
如果你想控制提示的行为，可以拦截`event()`函数并捕捉`QEvent::ToolTip`事件（例如，如果你想自定义提示应显示的区域）。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `toolTip()` 读取当前值；它不会修改应用状态。

### `int toolTipDuration() const`

**作用与语义：**

该属性包含了小部件在提示中的持续时间。
指定提示显示的时间长度，单位为毫秒。如果值为 -1（默认），则持续时间根据提示长度计算。

**如何使用：** 调用 `toolTipDuration()` 读取当前值；它不会修改应用状态。

### `void unsetCursor()`

**作用与语义：**

该属性包含该控件的光标形状。
鼠标光标在该控件上方时会呈现该形状。请参阅预定义光标对象列表，了解一系列有用的形状。
编辑器小部件可能会使用工字束光标：
如果没有设置光标，或者在调用 unsetCursor() 后，则使用父游标。
默认情况下，该属性包含一个具有`Qt::ArrowCursor`形状的光标。
有些底层窗口实现如果光标离开了小部件，即使鼠标被抓取，光标也会重置。如果你想为所有小部件设置光标，即使你在窗口外，也可以考虑用`QGuiApplication::setOverrideCursor()`。

**如何使用：** 调用 `unsetCursor()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 setCursor(Qt::IBeamCursor);
```

### `void unsetLayoutDirection()`

**作用与语义：**

此属性保存该控件的布局方向。
注意：此方法自 Qt 4.7 后不再影响文本布局方向。
默认情况下，该属性设置为 `Qt::LeftToRight`。
当在控件上设置布局方向时，它会传播到控件的子控件，但不会传播到作为窗口的子控件，也不会传播给已明确调用 setLayoutDirection() 的子控件。此外，在父控件调用 setLayoutDirection() 后添加的子控件不会继承父控件的布局方向。

**如何使用：** 调用 `unsetLayoutDirection()` 读取当前值；它不会修改应用状态。

### `void unsetLocale()`

**作用与语义：**

此属性保存小部件的区域设置。
只要未设置特殊区域设置，此属性为父组件的区域设置，或者如果该小部件是顶层小部件，则为默认区域设置。
如果小部件显示日期或数字，应使用小部件的区域设置进行格式化。

**如何使用：** 调用 `unsetLocale()` 读取当前值；它不会修改应用状态。

### `bool updatesEnabled() const`

**作用与语义：**

该属性决定是否启用更新。
启用更新的小部件会接收绘图事件并有系统背景;禁用的小部件则不会。这也意味着如果更新被禁用，调用`update()`和`repaint()`不会有影响。
默认情况下，该属性为`true`。
setUpdatesEnabled() 通常用于短时间禁用更新，例如避免大变更时的屏幕闪烁。在 Qt 中，控件通常不会产生屏幕闪烁，但在 X11 上，当控件隐藏时，服务器可能会在被其他控件替换前清除屏幕上的区域。禁用更新可以解决这个问题。
禁用小部件会隐式禁用其所有子组件。启用小部件会启用除顶层小部件或已明确禁用的子小部件外的所有子小部件。重新启用更新隐式调用该小部件的`update()`。

**如何使用：** 调用 `updatesEnabled()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 setUpdatesEnabled(false);
 bigVisualChanges();
 setUpdatesEnabled(true);
```

### `QString whatsThis() const`

**作用与语义：**

该属性包含小部件的“What's This 帮助文本。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `whatsThis()` 读取当前值；它不会修改应用状态。

### `int width() const`

**作用与语义：**

该属性表示了小部件的宽度，不包括任何窗框。
关于窗口几何问题的概述，请参见 Window Geometry 文档。
注意：请勿使用此功能在多屏桌面上查找屏幕宽度。详情请参见 `QScreen`。
默认情况下，该属性包含一个取决于用户平台和屏幕几何形状的值。

**如何使用：** 调用 `width()` 读取当前值；它不会修改应用状态。

### `QString windowFilePath() const`

**作用与语义：**

该属性包含与控件相关的文件路径。
这个属性只对 Windows 有意义。它将文件路径与窗口关联起来。如果你设置了文件路径但没有设置窗口标题，Qt 会将窗口标题设置为指定路径的文件名，该路径是通过 `QFileInfo::fileName()` 获得的。
如果窗口标题在任意点被设置，那么窗口标题优先，会显示它而不是文件路径字符串。
此外，在macOS上，这还有一个额外好处，就是假设文件路径存在，它会设置窗口的代理图标。
如果没有设置文件路径，该属性包含一个空字符串。
默认情况下，该属性包含空字符串。

**如何使用：** 调用 `windowFilePath()` 读取当前值；它不会修改应用状态。

### `Qt::WindowFlags windowFlags() const`

**作用与语义：**

窗口标志是类型（例如`Qt::Dialog`）和零个或多个窗口系统的提示（例如`Qt::FramelessWindowHint`）的组合。
如果小部件类型为`Qt::Widget`或`Qt::SubWindow`，并且变成了窗口（`Qt::Window`、`Qt::Dialog`等），则它会被放在桌面上的位置（0， 0）。如果小部件是窗口，并且变成`Qt::Widget`或`Qt::SubWindow`，则它相对于父小部件的位置（0， 0）。
注意：该函数在更改窗口标志时调用`setParent()`，导致控件被隐藏。您必须调用`show()`才能让控件再次可见。

**如何使用：** 调用 `windowFlags()` 读取当前值；它不会修改应用状态。

### `QIcon windowIcon() const`

**作用与语义：**

此属性保存小部件的图标。
此属性仅适用于窗口。如果没有设置图标，windowIcon() 将返回应用程序图标 (`QApplication::windowIcon()`)。
注意：在 macOS 上，窗口图标表示活动文档，除非使用 `setWindowFilePath` 设置了文件路径，否则不会显示。

**如何使用：** 调用 `windowIcon()` 读取当前值；它不会修改应用状态。

### `Qt::WindowModality windowModality() const`

**作用与语义：**

该属性决定了模态控件阻挡的窗口。
该属性仅适用于窗口。模态控件防止其他窗口中的控件接收输入。该属性的值控制控件可见时哪些窗口被阻挡。窗口可见时更改该属性无效;你必须先`hide()`控件，然后再`show()`。
默认情况下，该属性是`Qt::NonModal`。

**如何使用：** 调用 `windowModality()` 读取当前值；它不会修改应用状态。

### `qreal windowOpacity() const`

**作用与语义：**

该属性表示了窗口的不透明度水平。
有效不透明度范围为1.0（完全不透明）到0.0（完全透明）。
默认情况下，该属性的价值为1.0。
该功能可在支持复合扩展的嵌入式Linux、macOS、Windows和X11平台上使用。
注意：在 X11 上你需要运行复合管理器，并且你使用的窗口管理器必须支持 X11 专用的 _NET_WM_WINDOW_OPACITY Atom。
警告：将此属性从不透明改为透明可能会触发绘画事件，需要在窗口正确显示前处理。这主要影响`QScreen::grabWindow()`的使用。还要注意，半透明窗口的更新和调整速度明显慢于不透明窗口。

**如何使用：** 调用 `windowOpacity()` 读取当前值；它不会修改应用状态。

### `QString windowTitle() const`

**作用与语义：**

该物业拥有窗户标题（说明）。
该属性仅适用于顶层控件，如窗口和对话框。如果未设置说明文字，标题基于`windowFilePath`。若未设置，标题为空字符串。
如果你使用`windowModified`机制，窗口标题必须包含“[*]”占位符，指示“*”应出现在位置。通常，它应紧随文件名之后（例如，“document1.txt[*] - 文本编辑器”）。如果`windowModified`属性被`false`（默认），占位符会被直接移除。
在某些桌面平台（包括 Windows 和 Unix）上，如果设置了，应用程序名称（来自 `QGuiApplication::applicationDisplayName`）会被添加到窗口标题末尾。这是通过 QPA 插件实现的，因此它会显示给用户，但不包含在 windowTitle 字符串中。

**如何使用：** 调用 `windowTitle()` 读取当前值；它不会修改应用状态。

### `int x() const`

**作用与语义：**

该属性表示了小部件相对于其父节点的 x 坐标，包括任何窗口框架。
关于窗口几何问题的概述，请参见 Window Geometry 文档。
默认情况下，该属性的值为0。

**如何使用：** 调用 `x()` 读取当前值；它不会修改应用状态。

### `int y() const`

**作用与语义：**

该属性表示小部件相对于其父节点的 y 坐标，包括任意窗口框架。
关于窗口几何问题的概述，请参见 Window Geometry 文档。
默认情况下，该属性的值为0。

**如何使用：** 调用 `y()` 读取当前值；它不会修改应用状态。

### `void setEnabled(bool)`

**作用与语义：**

该属性决定小部件是否被启用。
通常，启用的小部件处理键盘和鼠标事件;禁用小部件则不处理。`QAbstractButton` 有例外。
有些小部件在禁用时会以不同的方式显示自己。例如，某个按钮可能会把标签画成灰色。如果你的小部件需要知道自己何时被启用或禁用，可以使用类型为`QEvent::EnabledChange`的`changeEvent()`。
禁用一个小部件会隐式禁用其所有子组件。分别启用则使所有子小部件都被启用，除非它们已被显式禁用。在父小部件仍然被禁用时，不可能显式启用非窗口的子小部件。
默认情况下，该属性为`true`。

**如何使用：** 调用 `setEnabled(...)` 修改 `enabled`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setStyleSheet(const QString &styleSheet)`

**作用与语义：**

该属性包含小部件的样式表。
样式表包含了对小部件样式的自定义描述，详见 Qt 样式表文档。
自 Qt 4.5 起，Qt 样式表已完全支持 macOS。
警告：Qt 样式表目前不支持 custom `QStyle` 子类。我们计划在未来某个版本中解决这个问题。

**如何使用：** 调用 `setStyleSheet(...)` 修改 `styleSheet`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `virtual void setVisible(bool visible)`

**作用与语义：**

该属性决定小部件是否可见。
调用 setVisible（true） 或 `show()` 会将控件设置为可见状态，前提是其所有父控件直到窗口都可见。如果祖先未被看见，控件在所有祖先显示完毕后才会显现。如果控件的大小或位置发生变化，Qt 保证控件在显示前会触发移动和调整大小事件。如果控件尚未调整大小，Qt 会用 `adjustSize()` 调整控件大小为有用的默认值。
调用 setVisible（false） 或 `hide()` 会显式隐藏一个控件。显式隐藏控件永远不会变得可见，即使它的所有祖先都变得可见，除非你展示它。
当控件的可见性状态发生变化时，小部件会接收显示和隐藏事件。在隐藏和显示事件之间，无需浪费CPU周期来准备或显示信息给用户。例如，视频应用可能只是停止生成新帧。
被屏幕上其他窗口遮挡的控件被视为可见。同样适用于图标窗口以及存在于另一个虚拟桌面上的窗口（支持该概念的平台）。当窗口系统改变控件的映射状态时，控件会接收自发的显示和隐藏事件，例如用户最小化窗口时会触发自发隐藏事件，窗口恢复时则会触发自发显示事件。
你很少需要重新实现 setVisible() 函数。如果你需要在显示小部件前更改某些设置，可以用 `showEvent()`。如果需要延迟初始化，可以使用传递给 `event()` 函数的波兰事件。

**如何使用：** 调用 `setVisible(...)` 修改 `visible`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setWindowModified(bool)`

**作用与语义：**

该属性决定窗口中显示的文档是否存在未保存的更改。
修改后的窗口是指内容发生变化但尚未保存到磁盘的窗口。该标志会因平台而异，效果各异。在macOS上，关闭按钮会有修改后的外观;在其他平台上，窗口标题会带有“*”（星号）。
窗口标题必须包含“[*]”占位符，指示“*”应出现在位置。通常，*应紧随文件名后面出现（例如，“document1.txt[*] - 文本编辑器”）。如果窗口未被修改，占位符会被直接移除。
注意，如果一个小部件被设置为修改，它的所有祖先也会被设置为被修改。然而，如果你调用`setWindowModified(false)`，这个功能不会传播到它的父节点，因为父节点的其他子节点可能也被修改过。

**如何使用：** 调用 `setWindowModified(...)` 修改 `windowModified`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setWindowTitle(const QString &)`

**作用与语义：**

该物业拥有窗户标题（说明）。
该属性仅适用于顶层控件，如窗口和对话框。如果未设置说明文字，标题基于`windowFilePath`。若未设置，标题为空字符串。
如果你使用`windowModified`机制，窗口标题必须包含“[*]”占位符，指示“*”应出现在位置。通常，它应紧随文件名之后（例如，“document1.txt[*] - 文本编辑器”）。如果`windowModified`属性被`false`（默认），占位符会被直接移除。
在某些桌面平台（包括 Windows 和 Unix）上，如果设置了，应用程序名称（来自 `QGuiApplication::applicationDisplayName`）会被添加到窗口标题末尾。这是通过 QPA 插件实现的，因此它会显示给用户，但不包含在 windowTitle 字符串中。

**如何使用：** 调用 `setWindowTitle(...)` 修改 `windowTitle`；传入的新值会成为后续查询和相关界面行为所使用的值。

## 6. 深入实践与常见坑

### 生命周期和资源边界

控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

### 状态和错误边界

控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

### 线程边界

所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

### 最容易出现的错误

布局管理的控件不要手动反复 setGeometry；paintEvent 中使用 QPainter；GUI 对象只能在 GUI 线程操作；顶层窗口关闭不等同于应用一定退出。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QWidget` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
