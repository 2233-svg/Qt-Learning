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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 366 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QWidget::RenderFlagflags QWidget::RenderFlags`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QWidget` 暴露的类型声明 `渲染、Flagflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:RenderFlagflags QWidget::RenderFlags`。
- 属性名：`QWidget`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `acceptDrops : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的配置属性。初始化或状态切换时通过 `setAcceptDrops(...)` 设置，之后用 `acceptDrops()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`acceptDrops`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `accessibleDescription : QString`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的配置属性。初始化或状态切换时通过 `setAccessibleDescription(...)` 设置，之后用 `accessibleDescription()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QString`。
- 属性名：`accessibleDescription`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.9] accessibleIdentifier : QString`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的配置属性。初始化或状态切换时通过 `setAccessibleIdentifier(...)` 设置，之后用 `accessibleIdentifier()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QString`。
- 属性名：`accessibleIdentifier`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `accessibleName : QString`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的配置属性。初始化或状态切换时通过 `setAccessibleName(...)` 设置，之后用 `accessibleName()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QString`。
- 属性名：`accessibleName`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `autoFillBackground : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的配置属性。初始化或状态切换时通过 `setAutoFillBackground(...)` 设置，之后用 `autoFillBackground()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`autoFillBackground`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `baseSize : QSize`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的配置属性。初始化或状态切换时通过 `setBaseSize(...)` 设置，之后用 `baseSize()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QSize`。
- 属性名：`baseSize`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] childrenRect : QRect`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的状态/能力属性。通常通过 `childrenRect()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`QRect`。
- 属性名：`childrenRect`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] childrenRegion : QRegion`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的状态/能力属性。通常通过 `childrenRegion()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`QRegion`。
- 属性名：`childrenRegion`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `contextMenuPolicy : Qt::ContextMenuPolicy`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的配置属性。初始化或状态切换时通过 `setContextMenuPolicy(...)` 设置，之后用 `ContextMenuPolicy()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`Qt::ContextMenuPolicy`。
- 属性名：`contextMenuPolicy`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `cursor : QCursor`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的配置属性。初始化或状态切换时通过 `setCursor(...)` 设置，之后用 `cursor()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QCursor`。
- 属性名：`cursor`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enabled : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的配置属性。初始化或状态切换时通过 `setEnabled(...)` 设置，之后用 `enabled()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`enabled`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] focus : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的状态/能力属性。通常通过 `focus()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`focus`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `focusPolicy : Qt::FocusPolicy`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的配置属性。初始化或状态切换时通过 `setFocusPolicy(...)` 设置，之后用 `FocusPolicy()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`Qt::FocusPolicy`。
- 属性名：`focusPolicy`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `font : QFont`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的配置属性。初始化或状态切换时通过 `setFont(...)` 设置，之后用 `font()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QFont`。
- 属性名：`font`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] frameGeometry : QRect`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的状态/能力属性。通常通过 `frameGeometry()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`QRect`。
- 属性名：`frameGeometry`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] frameSize : QSize`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的状态/能力属性。通常通过 `frameSize()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`QSize`。
- 属性名：`frameSize`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] fullScreen : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的状态/能力属性。通常通过 `fullScreen()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`fullScreen`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `geometry : QRect`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的配置属性。初始化或状态切换时通过 `setGeometry(...)` 设置，之后用 `geometry()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QRect`。
- 属性名：`geometry`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] height : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的状态/能力属性。通常通过 `height()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`height`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `inputMethodHints : Qt::InputMethodHints`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的配置属性。初始化或状态切换时通过 `setInputMethodHints(...)` 设置，之后用 `InputMethodHints()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`Qt::InputMethodHints`。
- 属性名：`inputMethodHints`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] isActiveWindow : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的状态/能力属性。通常通过 `isActiveWindow()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`isActiveWindow`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `layoutDirection : Qt::LayoutDirection`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的配置属性。初始化或状态切换时通过 `setLayoutDirection(...)` 设置，之后用 `LayoutDirection()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`Qt::LayoutDirection`。
- 属性名：`layoutDirection`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `locale : QLocale`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的配置属性。初始化或状态切换时通过 `setLocale(...)` 设置，之后用 `locale()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QLocale`。
- 属性名：`locale`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] maximized : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的状态/能力属性。通常通过 `maximized()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`maximized`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `maximumHeight : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的配置属性。初始化或状态切换时通过 `setMaximumHeight(...)` 设置，之后用 `maximumHeight()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`maximumHeight`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `maximumSize : QSize`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的配置属性。初始化或状态切换时通过 `setMaximumSize(...)` 设置，之后用 `maximumSize()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QSize`。
- 属性名：`maximumSize`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `maximumWidth : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的配置属性。初始化或状态切换时通过 `setMaximumWidth(...)` 设置，之后用 `maximumWidth()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`maximumWidth`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] minimized : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的状态/能力属性。通常通过 `minimized()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`minimized`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `minimumHeight : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的配置属性。初始化或状态切换时通过 `setMinimumHeight(...)` 设置，之后用 `minimumHeight()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`minimumHeight`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `minimumSize : QSize`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的配置属性。初始化或状态切换时通过 `setMinimumSize(...)` 设置，之后用 `minimumSize()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QSize`。
- 属性名：`minimumSize`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] minimumSizeHint : QSize`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的状态/能力属性。通常通过 `minimumSizeHint()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`QSize`。
- 属性名：`minimumSizeHint`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `minimumWidth : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的配置属性。初始化或状态切换时通过 `setMinimumWidth(...)` 设置，之后用 `minimumWidth()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`minimumWidth`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] modal : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的状态/能力属性。通常通过 `modal()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`modal`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `mouseTracking : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的配置属性。初始化或状态切换时通过 `setMouseTracking(...)` 设置，之后用 `mouseTracking()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`mouseTracking`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] normalGeometry : QRect`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的状态/能力属性。通常通过 `normalGeometry()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`QRect`。
- 属性名：`normalGeometry`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `palette : QPalette`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的配置属性。初始化或状态切换时通过 `setPalette(...)` 设置，之后用 `palette()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QPalette`。
- 属性名：`palette`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `pos : QPoint`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的配置属性。初始化或状态切换时通过 `setPos(...)` 设置，之后用 `pos()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QPoint`。
- 属性名：`pos`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] rect : QRect`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的状态/能力属性。通常通过 `rect()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`QRect`。
- 属性名：`rect`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `size : QSize`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的配置属性。初始化或状态切换时通过 `setSize(...)` 设置，之后用 `size()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QSize`。
- 属性名：`size`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] sizeHint : QSize`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的状态/能力属性。通常通过 `sizeHint()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`QSize`。
- 属性名：`sizeHint`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `sizeIncrement : QSize`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的配置属性。初始化或状态切换时通过 `setSizeIncrement(...)` 设置，之后用 `sizeIncrement()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QSize`。
- 属性名：`sizeIncrement`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `sizePolicy : QSizePolicy`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的配置属性。初始化或状态切换时通过 `setSizePolicy(...)` 设置，之后用 `sizePolicy()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QSizePolicy`。
- 属性名：`sizePolicy`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `statusTip : QString`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的配置属性。初始化或状态切换时通过 `setStatusTip(...)` 设置，之后用 `statusTip()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QString`。
- 属性名：`statusTip`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `styleSheet : QString`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的配置属性。初始化或状态切换时通过 `setStyleSheet(...)` 设置，之后用 `styleSheet()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QString`。
- 属性名：`styleSheet`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `tabletTracking : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的配置属性。初始化或状态切换时通过 `setTabletTracking(...)` 设置，之后用 `tabletTracking()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`tabletTracking`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `toolTip : QString`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的配置属性。初始化或状态切换时通过 `setToolTip(...)` 设置，之后用 `toolTip()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QString`。
- 属性名：`toolTip`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `toolTipDuration : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的配置属性。初始化或状态切换时通过 `setToolTipDuration(...)` 设置，之后用 `toolTipDuration()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`toolTipDuration`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `updatesEnabled : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的配置属性。初始化或状态切换时通过 `setUpdatesEnabled(...)` 设置，之后用 `updatesEnabled()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`updatesEnabled`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 通常在数据变化后调用，让 Qt 合并重绘请求；不要直接调用 `paintEvent()`。

### `visible : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的配置属性。初始化或状态切换时通过 `setVisible(...)` 设置，之后用 `visible()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`visible`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `whatsThis : QString`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的配置属性。初始化或状态切换时通过 `setWhatsThis(...)` 设置，之后用 `whatsThis()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QString`。
- 属性名：`whatsThis`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] width : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的状态/能力属性。通常通过 `width()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`width`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `windowFilePath : QString`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的配置属性。初始化或状态切换时通过 `setWindowFilePath(...)` 设置，之后用 `windowFilePath()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QString`。
- 属性名：`windowFilePath`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `windowFlags : Qt::WindowFlags`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的配置属性。初始化或状态切换时通过 `setWindowFlags(...)` 设置，之后用 `WindowFlags()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`Qt::WindowFlags`。
- 属性名：`windowFlags`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `windowIcon : QIcon`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的配置属性。初始化或状态切换时通过 `setWindowIcon(...)` 设置，之后用 `windowIcon()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QIcon`。
- 属性名：`windowIcon`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `windowModality : Qt::WindowModality`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的配置属性。初始化或状态切换时通过 `setWindowModality(...)` 设置，之后用 `WindowModality()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`Qt::WindowModality`。
- 属性名：`windowModality`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `windowModified : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的配置属性。初始化或状态切换时通过 `setWindowModified(...)` 设置，之后用 `windowModified()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`windowModified`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `windowOpacity : double`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的配置属性。初始化或状态切换时通过 `setWindowOpacity(...)` 设置，之后用 `windowOpacity()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`double`。
- 属性名：`windowOpacity`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `windowTitle : QString`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的配置属性。初始化或状态切换时通过 `setWindowTitle(...)` 设置，之后用 `windowTitle()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QString`。
- 属性名：`windowTitle`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] x : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的状态/能力属性。通常通过 `x()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`x`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] y : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QWidget` 的状态/能力属性。通常通过 `y()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`y`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QWidget::QWidget(QWidget *parent = nullptr, Qt::WindowFlags f = Qt::WindowFlags())`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QWidget` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `parent`：类型为 `QWidget *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。
- 参数 `f`：类型为 `Qt::WindowFlags`。默认值为 `Qt::WindowFlags()`。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QWidget::~QWidget()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QWidget` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QWidget::actionEvent(QActionEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::actionEvent` 用于执行与“action、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QActionEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QAction *> QWidget::actions() const`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::actions` 用于计算、查询或取得与“actions”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<QAction *>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QAction *>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::activateWindow()`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::activateWindow` 用于执行与“activate、Window”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::addAction(QAction *action)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QWidget` 添加依赖、数据或子对象的 API `addAction`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `action`：类型为 `QAction *`。没有默认值，调用时必须提供。传入 `QAction *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.3] QAction *QWidget::addAction(const QIcon &icon, const QString &text, const QKeySequence &shortcut)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QWidget` 添加依赖、数据或子对象的 API `addAction`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QAction *`。
- 参数 `icon`：类型为 `const QIcon &`。没有默认值，调用时必须提供。传入 `const QIcon &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。
- 参数 `shortcut`：类型为 `const QKeySequence &`。没有默认值，调用时必须提供。传入 `const QKeySequence &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.3] template <typename... Args, typename = QWidget::compatible_action_slot_args<Args...>> QAction *QWidget::addAction(const QIcon &icon, const QString &text, const QKeySequence &shortcut, Args &&... args)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QWidget` 添加依赖、数据或子对象的 API `addAction`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`template <typename... Args, typename = QWidget::compatible_action_slot_args<Args...>> QAction *`。
- 参数 `icon`：类型为 `const QIcon &`。没有默认值，调用时必须提供。传入 `const QIcon &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。
- 参数 `shortcut`：类型为 `const QKeySequence &`。没有默认值，调用时必须提供。传入 `const QKeySequence &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `args`：类型为 `Args &&...`。没有默认值，调用时必须提供。传入 `Args &&...` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.3] QAction *QWidget::addAction(const QIcon &icon, const QString &text, const QKeySequence &shortcut, const QObject *receiver, const char *member, Qt::ConnectionType type = Qt::AutoConnection)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QWidget` 添加依赖、数据或子对象的 API `addAction`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QAction *`。
- 参数 `icon`：类型为 `const QIcon &`。没有默认值，调用时必须提供。传入 `const QIcon &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。
- 参数 `shortcut`：类型为 `const QKeySequence &`。没有默认值，调用时必须提供。传入 `const QKeySequence &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `receiver`：类型为 `const QObject *`。没有默认值，调用时必须提供。接收者对象。它决定槽函数所属线程和连接生命周期，必须在回调使用期间有效。
- 参数 `member`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `type`：类型为 `Qt::ConnectionType`。默认值为 `Qt::AutoConnection`。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::addActions(const QList<QAction *> &actions)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QWidget` 添加依赖、数据或子对象的 API `addActions`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `actions`：类型为 `const QList<QAction *> &`。没有默认值，调用时必须提供。传入 `const QList<QAction *> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::adjustSize()`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::adjustSize` 用于执行与“adjust、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPalette::ColorRole QWidget::backgroundRole() const`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::backgroundRole` 用于计算、查询或取得与“background、角色”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPalette::ColorRole`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPalette::ColorRole`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QBackingStore *QWidget::backingStore() const`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::backingStore` 用于计算、查询或取得与“backing、Store”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QBackingStore *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QBackingStore *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QWidget::changeEvent(QEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::changeEvent` 用于执行与“change、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QWidget *QWidget::childAt(int x, int y) const`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::childAt` 用于计算、查询或取得与“child、按位置访问”相关的操作。调用时要先确认当前状态和 `x`、`y` 的有效范围；返回类型是 `QWidget *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QWidget *`。
- 参数 `x`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QWidget *QWidget::childAt(const QPoint &p) const`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::childAt` 用于计算、查询或取得与“child、按位置访问”相关的操作。调用时要先确认当前状态和 `p` 的有效范围；返回类型是 `QWidget *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QWidget *`。
- 参数 `p`：类型为 `const QPoint &`。没有默认值，调用时必须提供。传入 `const QPoint &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.8] QWidget *QWidget::childAt(const QPointF &p) const`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::childAt` 用于计算、查询或取得与“child、按位置访问”相关的操作。调用时要先确认当前状态和 `p` 的有效范围；返回类型是 `QWidget *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QWidget *`。
- 参数 `p`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::clearFocus()`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::clearFocus` 用于执行与“清空、Focus”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::clearMask()`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::clearMask` 用于执行与“清空、Mask”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] bool QWidget::close()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `close`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QWidget::closeEvent(QCloseEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `closeEvent`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QCloseEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMargins QWidget::contentsMargins() const`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::contentsMargins` 用于计算、查询或取得与“contents、Margins”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMargins`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMargins`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRect QWidget::contentsRect() const`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::contentsRect` 用于计算、查询或取得与“contents、Rect”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRect`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRect`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QWidget::contextMenuEvent(QContextMenuEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::contextMenuEvent` 用于执行与“context、Menu、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QContextMenuEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] void QWidget::create(WId window = 0, bool initializeWindow = true, bool destroyOldWindow = true)`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::create` 用于执行与“创建”相关的操作。调用时要先确认当前状态和 `window`、`initializeWindow`、`destroyOldWindow` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `window`：类型为 `WId`。默认值为 `0`。传入 `WId` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `initializeWindow`：类型为 `bool`。默认值为 `true`。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `destroyOldWindow`：类型为 `bool`。默认值为 `true`。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QWidget *QWidget::createWindowContainer(QWindow *window, QWidget *parent = nullptr, Qt::WindowFlags flags = Qt::WindowFlags())`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `createWindowContainer`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QWidget *`。
- 参数 `window`：类型为 `QWindow *`。没有默认值，调用时必须提供。传入 `QWindow *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `parent`：类型为 `QWidget *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。
- 参数 `flags`：类型为 `Qt::WindowFlags`。默认值为 `Qt::WindowFlags()`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QWidget::customContextMenuRequested(const QPoint &pos)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QWidget` 发出的通知信号 `customContextMenuRequested`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `pos`：类型为 `const QPoint &`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] void QWidget::destroy(bool destroyWindow = true, bool destroySubWindows = true)`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::destroy` 用于执行与“destroy”相关的操作。调用时要先确认当前状态和 `destroyWindow`、`destroySubWindows` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `destroyWindow`：类型为 `bool`。默认值为 `true`。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `destroySubWindows`：类型为 `bool`。默认值为 `true`。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QWidget::dragEnterEvent(QDragEnterEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::dragEnterEvent` 用于执行与“drag、Enter、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QDragEnterEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QWidget::dragLeaveEvent(QDragLeaveEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::dragLeaveEvent` 用于执行与“drag、Leave、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QDragLeaveEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QWidget::dragMoveEvent(QDragMoveEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::dragMoveEvent` 用于执行与“drag、移动、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QDragMoveEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QWidget::dropEvent(QDropEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::dropEvent` 用于执行与“drop、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QDropEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `WId QWidget::effectiveWinId() const`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::effectiveWinId` 用于计算、查询或取得与“effective、Win、Id”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `WId`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`WId`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::ensurePolished() const`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::ensurePolished` 用于执行与“ensure、Polished”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QWidget::enterEvent(QEnterEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::enterEvent` 用于执行与“enter、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QEnterEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] bool QWidget::event(QEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::event` 用于计算、查询或取得与“event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `event`：类型为 `QEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QWidget *QWidget::find(WId id)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `find`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QWidget *`。
- 参数 `id`：类型为 `WId`。没有默认值，调用时必须提供。传入 `WId` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QWidget::focusInEvent(QFocusEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::focusInEvent` 用于执行与“focus、In、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QFocusEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] bool QWidget::focusNextChild()`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::focusNextChild` 用于计算、查询或取得与“focus、移动到下一项、Child”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] bool QWidget::focusNextPrevChild(bool next)`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::focusNextPrevChild` 用于计算、查询或取得与“focus、移动到下一项、Prev、Child”相关的操作。调用时要先确认当前状态和 `next` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `next`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QWidget::focusOutEvent(QFocusEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::focusOutEvent` 用于执行与“focus、Out、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QFocusEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] bool QWidget::focusPreviousChild()`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::focusPreviousChild` 用于计算、查询或取得与“focus、Previous、Child”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QWidget *QWidget::focusProxy() const`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::focusProxy` 用于计算、查询或取得与“focus、Proxy”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QWidget *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QWidget *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QWidget *QWidget::focusWidget() const`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::focusWidget` 用于计算、查询或取得与“focus、Widget”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QWidget *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QWidget *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFontInfo QWidget::fontInfo() const`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::fontInfo` 用于计算、查询或取得与“字体、Info”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QFontInfo`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QFontInfo`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFontMetrics QWidget::fontMetrics() const`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::fontMetrics` 用于计算、查询或取得与“字体、Metrics”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QFontMetrics`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QFontMetrics`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPalette::ColorRole QWidget::foregroundRole() const`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::foregroundRole` 用于计算、查询或取得与“foreground、角色”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPalette::ColorRole`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPalette::ColorRole`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[invokable] QPixmap QWidget::grab(const QRect &rectangle = QRect(QPoint(0, 0), QSize(-1, -1)))`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::grab` 用于计算、查询或取得与“抓取”相关的操作。调用时要先确认当前状态和 `rectangle` 的有效范围；返回类型是 `QPixmap`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPixmap`。
- 参数 `rectangle`：类型为 `const QRect &`。默认值为 `QRect(QPoint(0, 0), QSize(-1, -1))`。传入 `const QRect &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::grabGesture(Qt::GestureType gesture, Qt::GestureFlags flags = Qt::GestureFlags())`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::grabGesture` 用于执行与“抓取、Gesture”相关的操作。调用时要先确认当前状态和 `gesture`、`flags` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `gesture`：类型为 `Qt::GestureType`。没有默认值，调用时必须提供。传入 `Qt::GestureType` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `flags`：类型为 `Qt::GestureFlags`。默认值为 `Qt::GestureFlags()`。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::grabKeyboard()`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::grabKeyboard` 用于执行与“抓取、Keyboard”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::grabMouse()`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::grabMouse` 用于执行与“抓取、Mouse”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::grabMouse(const QCursor &cursor)`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::grabMouse` 用于执行与“抓取、Mouse”相关的操作。调用时要先确认当前状态和 `cursor` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `cursor`：类型为 `const QCursor &`。没有默认值，调用时必须提供。传入 `const QCursor &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QWidget::grabShortcut(const QKeySequence &key, Qt::ShortcutContext context = Qt::WindowShortcut)`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::grabShortcut` 用于计算、查询或取得与“抓取、Shortcut”相关的操作。调用时要先确认当前状态和 `key`、`context` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `key`：类型为 `const QKeySequence &`。没有默认值，调用时必须提供。键、字段名或索引键；应确认编码、大小写规则和键不存在时的返回值。
- 参数 `context`：类型为 `Qt::ShortcutContext`。默认值为 `Qt::WindowShortcut`。上下文对象，用于限定回调连接的生命周期或解析/执行环境。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QGraphicsEffect *QWidget::graphicsEffect() const`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::graphicsEffect` 用于计算、查询或取得与“graphics、Effect”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QGraphicsEffect *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QGraphicsEffect *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QGraphicsProxyWidget *QWidget::graphicsProxyWidget() const`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::graphicsProxyWidget` 用于计算、查询或取得与“graphics、Proxy、Widget”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QGraphicsProxyWidget *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QGraphicsProxyWidget *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QWidget::hasEditFocus() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `hasEditFocus`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] bool QWidget::hasHeightForWidth() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `hasHeightForWidth`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] int QWidget::heightForWidth(int w) const`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::heightForWidth` 用于计算、查询或取得与“高度、For、宽度”相关的操作。调用时要先确认当前状态和 `w` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `w`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QWidget::hide()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `hide`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QWidget::hideEvent(QHideEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::hideEvent` 用于执行与“隐藏、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QHideEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QWidget::initPainter(QPainter *painter) const`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::initPainter` 用于执行与“init、Painter”相关的操作。调用时要先确认当前状态和 `painter` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `painter`：类型为 `QPainter *`。没有默认值，调用时必须提供。绘制上下文。要确认它已经绑定有效绘制设备，并处于允许绘制的阶段。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QWidget::inputMethodEvent(QInputMethodEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::inputMethodEvent` 用于执行与“input、Method、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QInputMethodEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] QVariant QWidget::inputMethodQuery(Qt::InputMethodQuery query) const`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::inputMethodQuery` 用于计算、查询或取得与“input、Method、查询”相关的操作。调用时要先确认当前状态和 `query` 的有效范围；返回类型是 `QVariant`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVariant`。
- 参数 `query`：类型为 `Qt::InputMethodQuery`。没有默认值，调用时必须提供。传入 `Qt::InputMethodQuery` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::insertAction(QAction *before, QAction *action)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QWidget` 添加依赖、数据或子对象的 API `insertAction`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `before`：类型为 `QAction *`。没有默认值，调用时必须提供。传入 `QAction *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `action`：类型为 `QAction *`。没有默认值，调用时必须提供。传入 `QAction *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::insertActions(QAction *before, const QList<QAction *> &actions)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QWidget` 添加依赖、数据或子对象的 API `insertActions`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `before`：类型为 `QAction *`。没有默认值，调用时必须提供。传入 `QAction *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `actions`：类型为 `const QList<QAction *> &`。没有默认值，调用时必须提供。传入 `const QList<QAction *> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QWidget::isAncestorOf(const QWidget *child) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isAncestorOf`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `child`：类型为 `const QWidget *`。没有默认值，调用时必须提供。子对象或子节点；要确认它是否由父对象接管，以及调用后原指针是否仍有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QWidget::isEnabledTo(const QWidget *ancestor) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isEnabledTo`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `ancestor`：类型为 `const QWidget *`。没有默认值，调用时必须提供。Qt 对象参数。要确认对象有效、线程归属、所有权和该 API 是否只处理直接子对象。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QWidget::isHidden() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isHidden`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QWidget::isVisibleTo(const QWidget *ancestor) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isVisibleTo`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `ancestor`：类型为 `const QWidget *`。没有默认值，调用时必须提供。Qt 对象参数。要确认对象有效、线程归属、所有权和该 API 是否只处理直接子对象。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QWidget::isWindow() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isWindow`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QWidget::keyPressEvent(QKeyEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::keyPressEvent` 用于执行与“key、Press、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QKeyEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QWidget::keyReleaseEvent(QKeyEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::keyReleaseEvent` 用于执行与“key、释放、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QKeyEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QWidget *QWidget::keyboardGrabber()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `keyboardGrabber`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QWidget *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QLayout *QWidget::layout() const`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::layout` 用于计算、查询或取得与“layout”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QLayout *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QLayout *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QWidget::leaveEvent(QEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::leaveEvent` 用于执行与“leave、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QWidget::lower()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `lower`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] QPointF QWidget::mapFrom(const QWidget *parent, const QPointF &pos) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `mapFrom`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QPointF`。
- 参数 `parent`：类型为 `const QWidget *`。没有默认值，调用时必须提供。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。
- 参数 `pos`：类型为 `const QPointF &`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPoint QWidget::mapFrom(const QWidget *parent, const QPoint &pos) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `mapFrom`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QPoint`。
- 参数 `parent`：类型为 `const QWidget *`。没有默认值，调用时必须提供。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。
- 参数 `pos`：类型为 `const QPoint &`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] QPointF QWidget::mapFromGlobal(const QPointF &pos) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `mapFromGlobal`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QPointF`。
- 参数 `pos`：类型为 `const QPointF &`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPoint QWidget::mapFromGlobal(const QPoint &pos) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `mapFromGlobal`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QPoint`。
- 参数 `pos`：类型为 `const QPoint &`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] QPointF QWidget::mapFromParent(const QPointF &pos) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `mapFromParent`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QPointF`。
- 参数 `pos`：类型为 `const QPointF &`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPoint QWidget::mapFromParent(const QPoint &pos) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `mapFromParent`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QPoint`。
- 参数 `pos`：类型为 `const QPoint &`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] QPointF QWidget::mapTo(const QWidget *parent, const QPointF &pos) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `mapTo`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QPointF`。
- 参数 `parent`：类型为 `const QWidget *`。没有默认值，调用时必须提供。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。
- 参数 `pos`：类型为 `const QPointF &`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPoint QWidget::mapTo(const QWidget *parent, const QPoint &pos) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `mapTo`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QPoint`。
- 参数 `parent`：类型为 `const QWidget *`。没有默认值，调用时必须提供。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。
- 参数 `pos`：类型为 `const QPoint &`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] QPointF QWidget::mapToGlobal(const QPointF &pos) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `mapToGlobal`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QPointF`。
- 参数 `pos`：类型为 `const QPointF &`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPoint QWidget::mapToGlobal(const QPoint &pos) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `mapToGlobal`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QPoint`。
- 参数 `pos`：类型为 `const QPoint &`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.0] QPointF QWidget::mapToParent(const QPointF &pos) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `mapToParent`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QPointF`。
- 参数 `pos`：类型为 `const QPointF &`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPoint QWidget::mapToParent(const QPoint &pos) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `mapToParent`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QPoint`。
- 参数 `pos`：类型为 `const QPoint &`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRegion QWidget::mask() const`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::mask` 用于计算、查询或取得与“mask”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRegion`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRegion`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] int QWidget::metric(QPaintDevice::PaintDeviceMetric m) const`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::metric` 用于计算、查询或取得与“metric”相关的操作。调用时要先确认当前状态和 `m` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `m`：类型为 `QPaintDevice::PaintDeviceMetric`。没有默认值，调用时必须提供。传入 `QPaintDevice::PaintDeviceMetric` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QWidget::mouseDoubleClickEvent(QMouseEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::mouseDoubleClickEvent` 用于执行与“mouse、Double、Click、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QMouseEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QWidget *QWidget::mouseGrabber()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `mouseGrabber`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QWidget *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QWidget::mouseMoveEvent(QMouseEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::mouseMoveEvent` 用于执行与“mouse、移动、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QMouseEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QWidget::mousePressEvent(QMouseEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::mousePressEvent` 用于执行与“mouse、Press、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QMouseEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QWidget::mouseReleaseEvent(QMouseEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::mouseReleaseEvent` 用于执行与“mouse、释放、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QMouseEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::move(int x, int y)`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::move` 用于执行与“移动”相关的操作。调用时要先确认当前状态和 `x`、`y` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QWidget::moveEvent(QMoveEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::moveEvent` 用于执行与“移动、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QMoveEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] bool QWidget::nativeEvent(const QByteArray &eventType, void *message, qintptr *result)`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::nativeEvent` 用于计算、查询或取得与“native、Event”相关的操作。调用时要先确认当前状态和 `eventType`、`message`、`result` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `eventType`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。
- 参数 `message`：类型为 `void *`。没有默认值，调用时必须提供。传入 `void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `result`：类型为 `qintptr *`。没有默认值，调用时必须提供。传入 `qintptr *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QWidget *QWidget::nativeParentWidget() const`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::nativeParentWidget` 用于计算、查询或取得与“native、父对象、Widget”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QWidget *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QWidget *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QWidget *QWidget::nextInFocusChain() const`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::nextInFocusChain` 用于计算、查询或取得与“移动到下一项、In、Focus、Chain”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QWidget *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QWidget *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::overrideWindowFlags(Qt::WindowFlags flags)`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::overrideWindowFlags` 用于执行与“override、Window、标志”相关的操作。调用时要先确认当前状态和 `flags` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `flags`：类型为 `Qt::WindowFlags`。没有默认值，调用时必须提供。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual] QPaintEngine *QWidget::paintEngine() const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QWidget` 的核心操作 `paintEngine`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`QPaintEngine *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QWidget::paintEvent(QPaintEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QWidget` 的核心操作 `paintEvent`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QPaintEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QWidget *QWidget::parentWidget() const`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::parentWidget` 用于计算、查询或取得与“父对象、Widget”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QWidget *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QWidget *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QWidget *QWidget::previousInFocusChain() const`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::previousInFocusChain` 用于计算、查询或取得与“previous、In、Focus、Chain”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QWidget *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QWidget *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QWidget::raise()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `raise`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::releaseKeyboard()`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::releaseKeyboard` 用于执行与“释放、Keyboard”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::releaseMouse()`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::releaseMouse` 用于执行与“释放、Mouse”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::releaseShortcut(int id)`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::releaseShortcut` 用于执行与“释放、Shortcut”相关的操作。调用时要先确认当前状态和 `id` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `id`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::removeAction(QAction *action)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeAction`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数 `action`：类型为 `QAction *`。没有默认值，调用时必须提供。传入 `QAction *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::render(QPaintDevice *target, const QPoint &targetOffset = QPoint(), const QRegion &sourceRegion = QRegion(), QWidget::RenderFlags renderFlags = RenderFlags(DrawWindowBackground | DrawChildren))`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QWidget` 的核心操作 `render`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `QPaintDevice *`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `targetOffset`：类型为 `const QPoint &`。默认值为 `QPoint()`。传入 `const QPoint &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sourceRegion`：类型为 `const QRegion &`。默认值为 `QRegion()`。传入 `const QRegion &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `renderFlags`：类型为 `QWidget::RenderFlags`。默认值为 `RenderFlags(DrawWindowBackground | DrawChildren)`。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::render(QPainter *painter, const QPoint &targetOffset = QPoint(), const QRegion &sourceRegion = QRegion(), QWidget::RenderFlags renderFlags = RenderFlags(DrawWindowBackground | DrawChildren))`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QWidget` 的核心操作 `render`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `painter`：类型为 `QPainter *`。没有默认值，调用时必须提供。绘制上下文。要确认它已经绑定有效绘制设备，并处于允许绘制的阶段。
- 参数 `targetOffset`：类型为 `const QPoint &`。默认值为 `QPoint()`。传入 `const QPoint &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `sourceRegion`：类型为 `const QRegion &`。默认值为 `QRegion()`。传入 `const QRegion &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `renderFlags`：类型为 `QWidget::RenderFlags`。默认值为 `RenderFlags(DrawWindowBackground | DrawChildren)`。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QWidget::repaint()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `repaint`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::repaint(const QRect &rect)`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::repaint` 用于执行与“repaint”相关的操作。调用时要先确认当前状态和 `rect` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `rect`：类型为 `const QRect &`。没有默认值，调用时必须提供。矩形区域；要确认坐标系、是否包含右下边界以及空矩形的语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::repaint(const QRegion &rgn)`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::repaint` 用于执行与“repaint”相关的操作。调用时要先确认当前状态和 `rgn` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `rgn`：类型为 `const QRegion &`。没有默认值，调用时必须提供。传入 `const QRegion &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::repaint(int x, int y, int w, int h)`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::repaint` 用于执行与“repaint”相关的操作。调用时要先确认当前状态和 `x`、`y`、`w`、`h` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `w`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `h`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::resize(int w, int h)`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::resize` 用于执行与“调整尺寸”相关的操作。调用时要先确认当前状态和 `w`、`h` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `w`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `h`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QWidget::resizeEvent(QResizeEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::resizeEvent` 用于执行与“调整尺寸、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QResizeEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QWidget::restoreGeometry(const QByteArray &geometry)`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::restoreGeometry` 用于计算、查询或取得与“恢复、几何区域”相关的操作。调用时要先确认当前状态和 `geometry` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `geometry`：类型为 `const QByteArray &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QByteArray QWidget::saveGeometry() const`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::saveGeometry` 用于计算、查询或取得与“保存、几何区域”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QByteArray`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QByteArray`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QScreen *QWidget::screen() const`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::screen` 用于计算、查询或取得与“screen”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QScreen *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QScreen *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::scroll(int dx, int dy)`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::scroll` 用于执行与“scroll”相关的操作。调用时要先确认当前状态和 `dx`、`dy` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `dx`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `dy`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::scroll(int dx, int dy, const QRect &r)`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::scroll` 用于执行与“scroll”相关的操作。调用时要先确认当前状态和 `dx`、`dy`、`r` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `dx`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `dy`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `r`：类型为 `const QRect &`。没有默认值，调用时必须提供。传入 `const QRect &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::setAttribute(Qt::WidgetAttribute attribute, bool on = true)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setAttribute`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `attribute`：类型为 `Qt::WidgetAttribute`。没有默认值，调用时必须提供。传入 `Qt::WidgetAttribute` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `on`：类型为 `bool`。默认值为 `true`。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::setBackgroundRole(QPalette::ColorRole role)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setBackgroundRole`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `role`：类型为 `QPalette::ColorRole`。没有默认值，调用时必须提供。数据角色，决定模型返回的是显示文本、编辑值、装饰、用户数据还是其他语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::setBaseSize(int basew, int baseh)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setBaseSize`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `basew`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `baseh`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::setContentsMargins(int left, int top, int right, int bottom)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setContentsMargins`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `left`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `top`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `right`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `bottom`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::setContentsMargins(const QMargins &margins)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setContentsMargins`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `margins`：类型为 `const QMargins &`。没有默认值，调用时必须提供。传入 `const QMargins &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QWidget::setDisabled(bool disable)`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `setDisabled`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `disable`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::setEditFocus(bool enable)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setEditFocus`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enable`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::setFixedHeight(int h)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFixedHeight`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `h`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::setFixedSize(const QSize &s)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFixedSize`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `s`：类型为 `const QSize &`。没有默认值，调用时必须提供。传入 `const QSize &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::setFixedSize(int w, int h)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFixedSize`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `w`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `h`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::setFixedWidth(int w)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFixedWidth`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `w`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::setFocus(Qt::FocusReason reason)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFocus`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `reason`：类型为 `Qt::FocusReason`。没有默认值，调用时必须提供。传入 `Qt::FocusReason` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QWidget::setFocus()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `setFocus`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::setFocusProxy(QWidget *w)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFocusProxy`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `w`：类型为 `QWidget *`。没有默认值，调用时必须提供。Qt 对象参数。要确认对象有效、线程归属、所有权和该 API 是否只处理直接子对象。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::setForegroundRole(QPalette::ColorRole role)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setForegroundRole`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `role`：类型为 `QPalette::ColorRole`。没有默认值，调用时必须提供。数据角色，决定模型返回的是显示文本、编辑值、装饰、用户数据还是其他语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::setGeometry(int x, int y, int w, int h)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setGeometry`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `w`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `h`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 如果控件已交给 layout，通常不应和布局同时手动设置几何，否则会出现 resize 后位置跳回或相互覆盖。

### `void QWidget::setGraphicsEffect(QGraphicsEffect *effect)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setGraphicsEffect`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `effect`：类型为 `QGraphicsEffect *`。没有默认值，调用时必须提供。传入 `QGraphicsEffect *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QWidget::setHidden(bool hidden)`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `setHidden`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `hidden`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::setLayout(QLayout *layout)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setLayout`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `layout`：类型为 `QLayout *`。没有默认值，调用时必须提供。参与操作的布局对象。通常表示整个子布局的几何区域和所有权，不等于子布局里的某一个控件。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::setMask(const QBitmap &bitmap)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setMask`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `bitmap`：类型为 `const QBitmap &`。没有默认值，调用时必须提供。传入 `const QBitmap &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::setMask(const QRegion &region)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setMask`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `region`：类型为 `const QRegion &`。没有默认值，调用时必须提供。传入 `const QRegion &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::setMaximumSize(int maxw, int maxh)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setMaximumSize`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `maxw`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `maxh`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::setMinimumSize(int minw, int minh)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setMinimumSize`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `minw`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `minh`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::setParent(QWidget *parent)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setParent`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `parent`：类型为 `QWidget *`。没有默认值，调用时必须提供。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::setParent(QWidget *parent, Qt::WindowFlags f)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setParent`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `parent`：类型为 `QWidget *`。没有默认值，调用时必须提供。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。
- 参数 `f`：类型为 `Qt::WindowFlags`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::setScreen(QScreen *screen)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setScreen`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `screen`：类型为 `QScreen *`。没有默认值，调用时必须提供。传入 `QScreen *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::setShortcutAutoRepeat(int id, bool enable = true)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setShortcutAutoRepeat`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `id`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `enable`：类型为 `bool`。默认值为 `true`。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::setShortcutEnabled(int id, bool enable = true)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setShortcutEnabled`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `id`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `enable`：类型为 `bool`。默认值为 `true`。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::setSizeIncrement(int w, int h)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSizeIncrement`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `w`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `h`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::setSizePolicy(QSizePolicy::Policy horizontal, QSizePolicy::Policy vertical)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSizePolicy`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `horizontal`：类型为 `QSizePolicy::Policy`。没有默认值，调用时必须提供。传入 `QSizePolicy::Policy` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `vertical`：类型为 `QSizePolicy::Policy`。没有默认值，调用时必须提供。传入 `QSizePolicy::Policy` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::setStyle(QStyle *style)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setStyle`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `style`：类型为 `QStyle *`。没有默认值，调用时必须提供。传入 `QStyle *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] void QWidget::setTabOrder(QWidget *first, QWidget *second)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `setTabOrder`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `first`：类型为 `QWidget *`。没有默认值，调用时必须提供。Qt 对象参数。要确认对象有效、线程归属、所有权和该 API 是否只处理直接子对象。
- 参数 `second`：类型为 `QWidget *`。没有默认值，调用时必须提供。Qt 对象参数。要确认对象有效、线程归属、所有权和该 API 是否只处理直接子对象。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.6] void QWidget::setTabOrder(std::initializer_list<QWidget *> widgets)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `setTabOrder`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`void`。
- 参数 `widgets`：类型为 `std::initializer_list<QWidget *>`。没有默认值，调用时必须提供。Qt 对象参数。要确认对象有效、线程归属、所有权和该 API 是否只处理直接子对象。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::setWindowFlag(Qt::WindowType flag, bool on = true)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setWindowFlag`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `flag`：类型为 `Qt::WindowType`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `on`：类型为 `bool`。默认值为 `true`。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::setWindowRole(const QString &role)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setWindowRole`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `role`：类型为 `const QString &`。没有默认值，调用时必须提供。数据角色，决定模型返回的是显示文本、编辑值、装饰、用户数据还是其他语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::setWindowState(Qt::WindowStates windowState)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setWindowState`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `windowState`：类型为 `Qt::WindowStates`。没有默认值，调用时必须提供。传入 `Qt::WindowStates` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::setupUi(QWidget *widget)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setupUi`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `widget`：类型为 `QWidget *`。没有默认值，调用时必须提供。参与操作的 QWidget。要确认它是否为空、是否已被其他布局/容器管理，以及函数是否只查找直接子项。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QWidget::show()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `show`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 通常在控件完成 parent、layout、属性和信号连接后调用；顶层窗口显示后由事件循环处理绘制和输入。

### `[virtual protected] void QWidget::showEvent(QShowEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::showEvent` 用于执行与“显示、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QShowEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 通常在控件完成 parent、layout、属性和信号连接后调用；顶层窗口显示后由事件循环处理绘制和输入。

### `[slot] void QWidget::showFullScreen()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `showFullScreen`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 通常在控件完成 parent、layout、属性和信号连接后调用；顶层窗口显示后由事件循环处理绘制和输入。

### `[slot] void QWidget::showMaximized()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `showMaximized`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 通常在控件完成 parent、layout、属性和信号连接后调用；顶层窗口显示后由事件循环处理绘制和输入。

### `[slot] void QWidget::showMinimized()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `showMinimized`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 通常在控件完成 parent、layout、属性和信号连接后调用；顶层窗口显示后由事件循环处理绘制和输入。

### `[slot] void QWidget::showNormal()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `showNormal`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 通常在控件完成 parent、layout、属性和信号连接后调用；顶层窗口显示后由事件循环处理绘制和输入。

### `void QWidget::stackUnder(QWidget *w)`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::stackUnder` 用于执行与“stack、Under”相关的操作。调用时要先确认当前状态和 `w` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `w`：类型为 `QWidget *`。没有默认值，调用时必须提供。Qt 对象参数。要确认对象有效、线程归属、所有权和该 API 是否只处理直接子对象。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStyle *QWidget::style() const`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::style` 用于计算、查询或取得与“style”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QStyle *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStyle *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QWidget::tabletEvent(QTabletEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::tabletEvent` 用于执行与“tablet、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QTabletEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QWidget::testAttribute(Qt::WidgetAttribute attribute) const`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::testAttribute` 用于计算、查询或取得与“test、Attribute”相关的操作。调用时要先确认当前状态和 `attribute` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `attribute`：类型为 `Qt::WidgetAttribute`。没有默认值，调用时必须提供。传入 `Qt::WidgetAttribute` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QWidget::underMouse() const`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::underMouse` 用于计算、查询或取得与“under、Mouse”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QWidget::ungrabGesture(Qt::GestureType gesture)`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::ungrabGesture` 用于执行与“ungrab、Gesture”相关的操作。调用时要先确认当前状态和 `gesture` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `gesture`：类型为 `Qt::GestureType`。没有默认值，调用时必须提供。传入 `Qt::GestureType` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QWidget::update()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `update`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 通常在数据变化后调用，让 Qt 合并重绘请求；不要直接调用 `paintEvent()`。

### `void QWidget::update(const QRect &rect)`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::update` 用于执行与“更新”相关的操作。调用时要先确认当前状态和 `rect` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `rect`：类型为 `const QRect &`。没有默认值，调用时必须提供。矩形区域；要确认坐标系、是否包含右下边界以及空矩形的语义。

**正确调用组合：** 通常在数据变化后调用，让 Qt 合并重绘请求；不要直接调用 `paintEvent()`。

### `void QWidget::update(const QRegion &rgn)`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::update` 用于执行与“更新”相关的操作。调用时要先确认当前状态和 `rgn` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `rgn`：类型为 `const QRegion &`。没有默认值，调用时必须提供。传入 `const QRegion &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 通常在数据变化后调用，让 Qt 合并重绘请求；不要直接调用 `paintEvent()`。

### `void QWidget::update(int x, int y, int w, int h)`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::update` 用于执行与“更新”相关的操作。调用时要先确认当前状态和 `x`、`y`、`w`、`h` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `w`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `h`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 通常在数据变化后调用，让 Qt 合并重绘请求；不要直接调用 `paintEvent()`。

### `void QWidget::updateGeometry()`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::updateGeometry` 用于执行与“更新、几何区域”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 通常在数据变化后调用，让 Qt 合并重绘请求；不要直接调用 `paintEvent()`。

### `[protected slot] void QWidget::updateMicroFocus(Qt::InputMethodQuery query = Qt::ImQueryAll)`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::updateMicroFocus` 用于执行与“更新、Micro、Focus”相关的操作。调用时要先确认当前状态和 `query` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `query`：类型为 `Qt::InputMethodQuery`。默认值为 `Qt::ImQueryAll`。传入 `Qt::InputMethodQuery` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 通常在数据变化后调用，让 Qt 合并重绘请求；不要直接调用 `paintEvent()`。

### `QRegion QWidget::visibleRegion() const`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::visibleRegion` 用于计算、查询或取得与“可见状态、Region”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRegion`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRegion`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QWidget::wheelEvent(QWheelEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::wheelEvent` 用于执行与“wheel、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QWheelEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `WId QWidget::winId() const`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::winId` 用于计算、查询或取得与“win、Id”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `WId`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`WId`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QWidget *QWidget::window() const`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::window` 用于计算、查询或取得与“window”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QWidget *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QWidget *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QWindow *QWidget::windowHandle() const`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::windowHandle` 用于计算、查询或取得与“window、Handle”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QWindow *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QWindow *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QWidget::windowIconChanged(const QIcon &icon)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QWidget` 发出的通知信号 `windowIconChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `icon`：类型为 `const QIcon &`。没有默认值，调用时必须提供。传入 `const QIcon &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString QWidget::windowRole() const`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::windowRole` 用于计算、查询或取得与“window、角色”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Qt::WindowStates QWidget::windowState() const`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::windowState` 用于计算、查询或取得与“window、State”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `Qt::WindowStates`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::WindowStates`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QWidget::windowTitleChanged(const QString &title)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QWidget` 发出的通知信号 `windowTitleChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `title`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Qt::WindowType QWidget::windowType() const`

**API 类别：** 成员函数说明

**中文解读：** `QWidget::windowType` 用于计算、查询或取得与“window、类型”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `Qt::WindowType`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::WindowType`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QWIDGETSIZE_MAX`

**API 类别：** 宏说明

**中文解读：** 这是 `QWidget` 的 `MAX` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum RenderFlag { DrawWindowBackground, DrawChildren, IgnoreMask }`

**API 类别：** 公有类型

**中文解读：** 这是 `QWidget` 暴露的类型声明 `渲染、Flag`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags RenderFlags`

**API 类别：** 公有类型

**中文解读：** 这是 `QWidget` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool acceptDrops() const`

**API 类别：** 公有函数

**中文解读：** `QWidget::acceptDrops` 用于计算、查询或取得与“接受、Drops”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString accessibleDescription() const`

**API 类别：** 公有函数

**中文解读：** `QWidget::accessibleDescription` 用于计算、查询或取得与“accessible、Description”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString accessibleIdentifier() const`

**API 类别：** 公有函数

**中文解读：** `QWidget::accessibleIdentifier` 用于计算、查询或取得与“accessible、Identifier”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString accessibleName() const`

**API 类别：** 公有函数

**中文解读：** `QWidget::accessibleName` 用于计算、查询或取得与“accessible、名称”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.3) QAction * addAction(const QString &text)`

**API 类别：** 公有函数

**中文解读：** 这是向 `QWidget` 添加依赖、数据或子对象的 API `addAction`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QAction *`。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.3) QAction * addAction(const QIcon &icon, const QString &text)`

**API 类别：** 公有函数

**中文解读：** 这是向 `QWidget` 添加依赖、数据或子对象的 API `addAction`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QAction *`。
- 参数 `icon`：类型为 `const QIcon &`。没有默认值，调用时必须提供。传入 `const QIcon &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.3) QAction * addAction(const QString &text, const QKeySequence &shortcut)`

**API 类别：** 公有函数

**中文解读：** 这是向 `QWidget` 添加依赖、数据或子对象的 API `addAction`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QAction *`。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。
- 参数 `shortcut`：类型为 `const QKeySequence &`。没有默认值，调用时必须提供。传入 `const QKeySequence &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.3) QAction * addAction(const QString &text, Args &&... args)`

**API 类别：** 公有函数

**中文解读：** 这是向 `QWidget` 添加依赖、数据或子对象的 API `addAction`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QAction *`。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。
- 参数 `args`：类型为 `Args &&...`。没有默认值，调用时必须提供。传入 `Args &&...` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.3) QAction * addAction(const QIcon &icon, const QString &text, Args &&... args)`

**API 类别：** 公有函数

**中文解读：** 这是向 `QWidget` 添加依赖、数据或子对象的 API `addAction`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QAction *`。
- 参数 `icon`：类型为 `const QIcon &`。没有默认值，调用时必须提供。传入 `const QIcon &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。
- 参数 `args`：类型为 `Args &&...`。没有默认值，调用时必须提供。传入 `Args &&...` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.3) QAction * addAction(const QString &text, const QKeySequence &shortcut, Args &&... args)`

**API 类别：** 公有函数

**中文解读：** 这是向 `QWidget` 添加依赖、数据或子对象的 API `addAction`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QAction *`。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。
- 参数 `shortcut`：类型为 `const QKeySequence &`。没有默认值，调用时必须提供。传入 `const QKeySequence &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `args`：类型为 `Args &&...`。没有默认值，调用时必须提供。传入 `Args &&...` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.3) QAction * addAction(const QString &text, const QObject *receiver, const char *member, Qt::ConnectionType type = Qt::AutoConnection)`

**API 类别：** 公有函数

**中文解读：** 这是向 `QWidget` 添加依赖、数据或子对象的 API `addAction`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QAction *`。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。
- 参数 `receiver`：类型为 `const QObject *`。没有默认值，调用时必须提供。接收者对象。它决定槽函数所属线程和连接生命周期，必须在回调使用期间有效。
- 参数 `member`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `type`：类型为 `Qt::ConnectionType`。默认值为 `Qt::AutoConnection`。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.3) QAction * addAction(const QIcon &icon, const QString &text, const QObject *receiver, const char *member, Qt::ConnectionType type = Qt::AutoConnection)`

**API 类别：** 公有函数

**中文解读：** 这是向 `QWidget` 添加依赖、数据或子对象的 API `addAction`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QAction *`。
- 参数 `icon`：类型为 `const QIcon &`。没有默认值，调用时必须提供。传入 `const QIcon &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。
- 参数 `receiver`：类型为 `const QObject *`。没有默认值，调用时必须提供。接收者对象。它决定槽函数所属线程和连接生命周期，必须在回调使用期间有效。
- 参数 `member`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `type`：类型为 `Qt::ConnectionType`。默认值为 `Qt::AutoConnection`。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.3) QAction * addAction(const QString &text, const QKeySequence &shortcut, const QObject *receiver, const char *member, Qt::ConnectionType type = Qt::AutoConnection)`

**API 类别：** 公有函数

**中文解读：** 这是向 `QWidget` 添加依赖、数据或子对象的 API `addAction`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QAction *`。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。
- 参数 `shortcut`：类型为 `const QKeySequence &`。没有默认值，调用时必须提供。传入 `const QKeySequence &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `receiver`：类型为 `const QObject *`。没有默认值，调用时必须提供。接收者对象。它决定槽函数所属线程和连接生命周期，必须在回调使用期间有效。
- 参数 `member`：类型为 `const char *`。没有默认值，调用时必须提供。传入 `const char *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `type`：类型为 `Qt::ConnectionType`。默认值为 `Qt::AutoConnection`。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool autoFillBackground() const`

**API 类别：** 公有函数

**中文解读：** `QWidget::autoFillBackground` 用于计算、查询或取得与“auto、Fill、Background”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSize baseSize() const`

**API 类别：** 公有函数

**中文解读：** `QWidget::baseSize` 用于计算、查询或取得与“base、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSize`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSize`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRect childrenRect() const`

**API 类别：** 公有函数

**中文解读：** `QWidget::childrenRect` 用于计算、查询或取得与“children、Rect”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRect`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRect`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRegion childrenRegion() const`

**API 类别：** 公有函数

**中文解读：** `QWidget::childrenRegion` 用于计算、查询或取得与“children、Region”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRegion`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRegion`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Qt::ContextMenuPolicy contextMenuPolicy() const`

**API 类别：** 公有函数

**中文解读：** `QWidget::contextMenuPolicy` 用于计算、查询或取得与“context、Menu、Policy”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `Qt::ContextMenuPolicy`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::ContextMenuPolicy`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCursor cursor() const`

**API 类别：** 公有函数

**中文解读：** `QWidget::cursor` 用于计算、查询或取得与“cursor”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QCursor`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCursor`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Qt::FocusPolicy focusPolicy() const`

**API 类别：** 公有函数

**中文解读：** `QWidget::focusPolicy` 用于计算、查询或取得与“focus、Policy”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `Qt::FocusPolicy`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::FocusPolicy`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QFont & font() const`

**API 类别：** 公有函数

**中文解读：** `QWidget::font` 用于计算、查询或取得与“字体”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QFont &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QFont &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRect frameGeometry() const`

**API 类别：** 公有函数

**中文解读：** `QWidget::frameGeometry` 用于计算、查询或取得与“frame、几何区域”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRect`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRect`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSize frameSize() const`

**API 类别：** 公有函数

**中文解读：** `QWidget::frameSize` 用于计算、查询或取得与“frame、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSize`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSize`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QRect & geometry() const`

**API 类别：** 公有函数

**中文解读：** `QWidget::geometry` 用于计算、查询或取得与“几何区域”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QRect &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QRect &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool hasFocus() const`

**API 类别：** 公有函数

**中文解读：** 这是查询 API `hasFocus`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool hasMouseTracking() const`

**API 类别：** 公有函数

**中文解读：** 这是查询 API `hasMouseTracking`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool hasTabletTracking() const`

**API 类别：** 公有函数

**中文解读：** 这是查询 API `hasTabletTracking`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int height() const`

**API 类别：** 公有函数

**中文解读：** `QWidget::height` 用于计算、查询或取得与“高度”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Qt::InputMethodHints inputMethodHints() const`

**API 类别：** 公有函数

**中文解读：** `QWidget::inputMethodHints` 用于计算、查询或取得与“input、Method、Hints”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `Qt::InputMethodHints`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::InputMethodHints`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool isActiveWindow() const`

**API 类别：** 公有函数

**中文解读：** 这是查询 API `isActiveWindow`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool isEnabled() const`

**API 类别：** 公有函数

**中文解读：** 这是查询 API `isEnabled`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool isFullScreen() const`

**API 类别：** 公有函数

**中文解读：** 这是查询 API `isFullScreen`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool isMaximized() const`

**API 类别：** 公有函数

**中文解读：** 这是查询 API `isMaximized`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool isMinimized() const`

**API 类别：** 公有函数

**中文解读：** 这是查询 API `isMinimized`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool isModal() const`

**API 类别：** 公有函数

**中文解读：** 这是查询 API `isModal`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool isVisible() const`

**API 类别：** 公有函数

**中文解读：** 这是查询 API `isVisible`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool isWindowModified() const`

**API 类别：** 公有函数

**中文解读：** 这是查询 API `isWindowModified`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Qt::LayoutDirection layoutDirection() const`

**API 类别：** 公有函数

**中文解读：** `QWidget::layoutDirection` 用于计算、查询或取得与“layout、Direction”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `Qt::LayoutDirection`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::LayoutDirection`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QLocale locale() const`

**API 类别：** 公有函数

**中文解读：** `QWidget::locale` 用于计算、查询或取得与“locale”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QLocale`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QLocale`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int maximumHeight() const`

**API 类别：** 公有函数

**中文解读：** `QWidget::maximumHeight` 用于计算、查询或取得与“最大值、高度”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSize maximumSize() const`

**API 类别：** 公有函数

**中文解读：** `QWidget::maximumSize` 用于计算、查询或取得与“最大值、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSize`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSize`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int maximumWidth() const`

**API 类别：** 公有函数

**中文解读：** `QWidget::maximumWidth` 用于计算、查询或取得与“最大值、宽度”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int minimumHeight() const`

**API 类别：** 公有函数

**中文解读：** `QWidget::minimumHeight` 用于计算、查询或取得与“最小值、高度”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSize minimumSize() const`

**API 类别：** 公有函数

**中文解读：** `QWidget::minimumSize` 用于计算、查询或取得与“最小值、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSize`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSize`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `virtual QSize minimumSizeHint() const`

**API 类别：** 公有函数

**中文解读：** `QWidget::minimumSizeHint` 用于计算、查询或取得与“最小值、尺寸或数量、Hint”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSize`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSize`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int minimumWidth() const`

**API 类别：** 公有函数

**中文解读：** `QWidget::minimumWidth` 用于计算、查询或取得与“最小值、宽度”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void move(const QPoint &)`

**API 类别：** 公有函数

**中文解读：** `QWidget::move` 用于执行与“移动”相关的操作。调用时要先确认当前状态和 `const QPoint &` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `const QPoint &`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRect normalGeometry() const`

**API 类别：** 公有函数

**中文解读：** `QWidget::normalGeometry` 用于计算、查询或取得与“normal、几何区域”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRect`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRect`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const QPalette & palette() const`

**API 类别：** 公有函数

**中文解读：** `QWidget::palette` 用于计算、查询或取得与“palette”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `const QPalette &`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`const QPalette &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPoint pos() const`

**API 类别：** 公有函数

**中文解读：** `QWidget::pos` 用于计算、查询或取得与“pos”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPoint`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPoint`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRect rect() const`

**API 类别：** 公有函数

**中文解读：** `QWidget::rect` 用于计算、查询或取得与“rect”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRect`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRect`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void resize(const QSize &)`

**API 类别：** 公有函数

**中文解读：** `QWidget::resize` 用于执行与“调整尺寸”相关的操作。调用时要先确认当前状态和 `const QSize &` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `const QSize &`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setAcceptDrops(bool on)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setAcceptDrops`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `on`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setAccessibleDescription(const QString &description)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setAccessibleDescription`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `description`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setAccessibleIdentifier(const QString &identifier)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setAccessibleIdentifier`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `identifier`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setAccessibleName(const QString &name)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setAccessibleName`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `name`：类型为 `const QString &`。没有默认值，调用时必须提供。名称或键。通常是稳定的 API/配置标识，不应随意使用显示文本替代。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setAutoFillBackground(bool enabled)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setAutoFillBackground`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enabled`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setBaseSize(const QSize &)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setBaseSize`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `const QSize &`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setContextMenuPolicy(Qt::ContextMenuPolicy policy)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setContextMenuPolicy`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `policy`：类型为 `Qt::ContextMenuPolicy`。没有默认值，调用时必须提供。传入 `Qt::ContextMenuPolicy` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setCursor(const QCursor &)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setCursor`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `const QCursor &`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setFocusPolicy(Qt::FocusPolicy policy)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setFocusPolicy`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `policy`：类型为 `Qt::FocusPolicy`。没有默认值，调用时必须提供。传入 `Qt::FocusPolicy` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setFont(const QFont &)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setFont`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `const QFont &`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setGeometry(const QRect &)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setGeometry`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `const QRect &`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 如果控件已交给 layout，通常不应和布局同时手动设置几何，否则会出现 resize 后位置跳回或相互覆盖。

### `void setInputMethodHints(Qt::InputMethodHints hints)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setInputMethodHints`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `hints`：类型为 `Qt::InputMethodHints`。没有默认值，调用时必须提供。传入 `Qt::InputMethodHints` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setLayoutDirection(Qt::LayoutDirection direction)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setLayoutDirection`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `direction`：类型为 `Qt::LayoutDirection`。没有默认值，调用时必须提供。方向枚举，决定排列、遍历或坐标增长方向；要结合该类定义的枚举值判断实际方向。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setLocale(const QLocale &locale)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setLocale`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `locale`：类型为 `const QLocale &`。没有默认值，调用时必须提供。传入 `const QLocale &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setMaximumHeight(int maxh)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setMaximumHeight`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `maxh`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setMaximumSize(const QSize &)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setMaximumSize`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `const QSize &`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setMaximumWidth(int maxw)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setMaximumWidth`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `maxw`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setMinimumHeight(int minh)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setMinimumHeight`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `minh`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setMinimumSize(const QSize &)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setMinimumSize`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `const QSize &`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setMinimumWidth(int minw)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setMinimumWidth`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `minw`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setMouseTracking(bool enable)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setMouseTracking`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enable`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setPalette(const QPalette &)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setPalette`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `const QPalette &`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setSizeIncrement(const QSize &)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setSizeIncrement`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `const QSize &`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setSizePolicy(QSizePolicy)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setSizePolicy`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `QSizePolicy`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setStatusTip(const QString &)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setStatusTip`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `const QString &`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setTabletTracking(bool enable)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setTabletTracking`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enable`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setToolTip(const QString &)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setToolTip`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `const QString &`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setToolTipDuration(int msec)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setToolTipDuration`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `msec`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setUpdatesEnabled(bool enable)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setUpdatesEnabled`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enable`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setWhatsThis(const QString &)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setWhatsThis`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `const QString &`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setWindowFilePath(const QString &filePath)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setWindowFilePath`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `filePath`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setWindowFlags(Qt::WindowFlags type)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setWindowFlags`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `type`：类型为 `Qt::WindowFlags`。没有默认值，调用时必须提供。类型、格式或策略枚举。要确认枚举值的适用范围和平台支持情况。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setWindowIcon(const QIcon &icon)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setWindowIcon`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `icon`：类型为 `const QIcon &`。没有默认值，调用时必须提供。传入 `const QIcon &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setWindowModality(Qt::WindowModality windowModality)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setWindowModality`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `windowModality`：类型为 `Qt::WindowModality`。没有默认值，调用时必须提供。传入 `Qt::WindowModality` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setWindowOpacity(qreal level)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setWindowOpacity`。调用它会改变 `QWidget` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `level`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSize size() const`

**API 类别：** 公有函数

**中文解读：** 这是尺寸/数量查询 API `size`，返回 `QWidget` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`QSize`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `virtual QSize sizeHint() const`

**API 类别：** 公有函数

**中文解读：** `QWidget::sizeHint` 用于计算、查询或取得与“尺寸或数量、Hint”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSize`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSize`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSize sizeIncrement() const`

**API 类别：** 公有函数

**中文解读：** `QWidget::sizeIncrement` 用于计算、查询或取得与“尺寸或数量、Increment”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSize`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSize`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSizePolicy sizePolicy() const`

**API 类别：** 公有函数

**中文解读：** `QWidget::sizePolicy` 用于计算、查询或取得与“尺寸或数量、Policy”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSizePolicy`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSizePolicy`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString statusTip() const`

**API 类别：** 公有函数

**中文解读：** `QWidget::statusTip` 用于计算、查询或取得与“状态、Tip”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString styleSheet() const`

**API 类别：** 公有函数

**中文解读：** `QWidget::styleSheet` 用于计算、查询或取得与“style、Sheet”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString toolTip() const`

**API 类别：** 公有函数

**中文解读：** 这是转换/映射 API `toolTip`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int toolTipDuration() const`

**API 类别：** 公有函数

**中文解读：** 这是转换/映射 API `toolTipDuration`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void unsetCursor()`

**API 类别：** 公有函数

**中文解读：** `QWidget::unsetCursor` 用于执行与“unset、Cursor”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void unsetLayoutDirection()`

**API 类别：** 公有函数

**中文解读：** `QWidget::unsetLayoutDirection` 用于执行与“unset、Layout、Direction”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void unsetLocale()`

**API 类别：** 公有函数

**中文解读：** `QWidget::unsetLocale` 用于执行与“unset、Locale”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool updatesEnabled() const`

**API 类别：** 公有函数

**中文解读：** `QWidget::updatesEnabled` 用于计算、查询或取得与“updates、启用状态”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 通常在数据变化后调用，让 Qt 合并重绘请求；不要直接调用 `paintEvent()`。

### `QString whatsThis() const`

**API 类别：** 公有函数

**中文解读：** `QWidget::whatsThis` 用于计算、查询或取得与“whats、This”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int width() const`

**API 类别：** 公有函数

**中文解读：** `QWidget::width` 用于计算、查询或取得与“宽度”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString windowFilePath() const`

**API 类别：** 公有函数

**中文解读：** `QWidget::windowFilePath` 用于计算、查询或取得与“window、File、Path”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Qt::WindowFlags windowFlags() const`

**API 类别：** 公有函数

**中文解读：** `QWidget::windowFlags` 用于计算、查询或取得与“window、标志”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `Qt::WindowFlags`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::WindowFlags`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QIcon windowIcon() const`

**API 类别：** 公有函数

**中文解读：** `QWidget::windowIcon` 用于计算、查询或取得与“window、Icon”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QIcon`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QIcon`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Qt::WindowModality windowModality() const`

**API 类别：** 公有函数

**中文解读：** `QWidget::windowModality` 用于计算、查询或取得与“window、Modality”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `Qt::WindowModality`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::WindowModality`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal windowOpacity() const`

**API 类别：** 公有函数

**中文解读：** `QWidget::windowOpacity` 用于计算、查询或取得与“window、Opacity”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString windowTitle() const`

**API 类别：** 公有函数

**中文解读：** `QWidget::windowTitle` 用于计算、查询或取得与“window、Title”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int x() const`

**API 类别：** 公有函数

**中文解读：** `QWidget::x` 用于计算、查询或取得与“x”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int y() const`

**API 类别：** 公有函数

**中文解读：** `QWidget::y` 用于计算、查询或取得与“y”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setEnabled(bool)`

**API 类别：** 公有槽函数

**中文解读：** 这是可被信号连接或元对象调用的槽 `setEnabled`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `bool`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setStyleSheet(const QString &styleSheet)`

**API 类别：** 公有槽函数

**中文解读：** 这是可被信号连接或元对象调用的槽 `setStyleSheet`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `styleSheet`：类型为 `const QString &`。没有默认值，调用时必须提供。文本/字节参数。要确认编码、空值语义、是否发生拷贝以及调用结束后是否仍需保留数据。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `virtual void setVisible(bool visible)`

**API 类别：** 公有槽函数

**中文解读：** 这是可被信号连接或元对象调用的槽 `setVisible`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `visible`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setWindowModified(bool)`

**API 类别：** 公有槽函数

**中文解读：** 这是可被信号连接或元对象调用的槽 `setWindowModified`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `bool`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setWindowTitle(const QString &)`

**API 类别：** 公有槽函数

**中文解读：** 这是可被信号连接或元对象调用的槽 `setWindowTitle`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `const QString &`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

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
