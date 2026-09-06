# QGraphicsWidget

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QGraphicsWidget` 是 图形场景与项目机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QGraphicsWidget` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QGraphicsWidget>`
- 继承自：QGraphicsObject、QGraphicsLayoutItem
- 直接派生类：QGraphicsProxyWidget

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

### 状态、生命周期和线程

**生命周期：** 场景或父项目通常管理子项目，但视图只是观察者，不一定拥有场景。删除项目、改变父项目或切换场景时要确认索引、指针、选中状态和布局关系是否仍有效。

**状态与结果：** 区分局部坐标、场景坐标、视图/窗口坐标，区分选中、悬停、焦点、可见和碰撞状态。改变几何、变换或数据后通常请求更新，而不是手动强制调用绘制函数。

**线程与事件循环：** 图形对象通常只能在其所属 GUI/场景线程操作；后台线程负责数据准备，结果通过信号投递后再更新场景对象。

## 3. 直接使用

需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。 使用时通常按这个过程组织：创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum { Type }`

### 属性

- `autoFillBackground : bool`
- `focusPolicy : Qt::FocusPolicy`
- `font : QFont`
- `geometry : QRectF`
- `layout : QGraphicsLayout*`
- `layoutDirection : Qt::LayoutDirection`
- `maximumSize : QSizeF`
- `minimumSize : QSizeF`
- `palette : QPalette`
- `preferredSize : QSizeF`
- `size : QSizeF`
- `sizePolicy : QSizePolicy`
- `windowFlags : Qt::WindowFlags`
- `windowTitle : QString`

### 公有函数

- `QGraphicsWidget(QGraphicsItem *parent = nullptr, Qt::WindowFlags wFlags = Qt::WindowFlags())`
- `virtual ~QGraphicsWidget()`
- `QList<QAction *> actions() const`
- `void addAction(QAction *action)`
- `void addActions(const QList<QAction *> &actions)`
- `void adjustSize()`
- `bool autoFillBackground() const`
- `Qt::FocusPolicy focusPolicy() const`
- `QGraphicsWidget * focusWidget() const`
- `QFont font() const`
- `void getWindowFrameMargins(qreal *left, qreal *top, qreal *right, qreal *bottom) const`
- `int grabShortcut(const QKeySequence &sequence, Qt::ShortcutContext context = Qt::WindowShortcut)`
- `void insertAction(QAction *before, QAction *action)`
- `void insertActions(QAction *before, const QList<QAction *> &actions)`
- `bool isActiveWindow() const`
- `QGraphicsLayout * layout() const`
- `Qt::LayoutDirection layoutDirection() const`
- `virtual void paintWindowFrame(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget = nullptr)`
- `QPalette palette() const`
- `QRectF rect() const`
- `void releaseShortcut(int id)`
- `void removeAction(QAction *action)`
- `void resize(const QSizeF &size)`
- `void resize(qreal w, qreal h)`
- `void setAttribute(Qt::WidgetAttribute attribute, bool on = true)`
- `void setAutoFillBackground(bool enabled)`
- `void setContentsMargins(QMarginsF margins)`
- `void setContentsMargins(qreal left, qreal top, qreal right, qreal bottom)`
- `void setFocusPolicy(Qt::FocusPolicy policy)`
- `void setFont(const QFont &font)`
- `virtual void setGeometry(const QRectF &rect) override`
- `void setGeometry(qreal x, qreal y, qreal w, qreal h)`
- `void setLayout(QGraphicsLayout *layout)`
- `void setLayoutDirection(Qt::LayoutDirection direction)`
- `void setPalette(const QPalette &palette)`
- `void setShortcutAutoRepeat(int id, bool enabled = true)`
- `void setShortcutEnabled(int id, bool enabled = true)`
- `void setStyle(QStyle *style)`
- `void setWindowFlags(Qt::WindowFlags wFlags)`
- `void setWindowFrameMargins(QMarginsF margins)`
- `void setWindowFrameMargins(qreal left, qreal top, qreal right, qreal bottom)`
- `void setWindowTitle(const QString &title)`
- `QSizeF size() const`
- `QStyle * style() const`
- `bool testAttribute(Qt::WidgetAttribute attribute) const`
- `void unsetLayoutDirection()`
- `void unsetWindowFrameMargins()`
- `Qt::WindowFlags windowFlags() const`
- `QRectF windowFrameGeometry() const`
- `QRectF windowFrameRect() const`
- `QString windowTitle() const`
- `Qt::WindowType windowType() const`

### 重实现的公有函数

- `virtual QRectF boundingRect() const override`
- `virtual void getContentsMargins(qreal *left, qreal *top, qreal *right, qreal *bottom) const override`
- `virtual void paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget = nullptr) override`
- `virtual QPainterPath shape() const override`
- `virtual int type() const override`

### 公有槽函数

- `bool close()`

### 信号

- `void geometryChanged()`
- `void layoutChanged()`

### 静态公有成员

- `void setTabOrder(QGraphicsWidget *first, QGraphicsWidget *second)`

### 保护函数

- `virtual void changeEvent(QEvent *event)`
- `virtual void closeEvent(QCloseEvent *event)`
- `virtual bool focusNextPrevChild(bool next)`
- `virtual void grabKeyboardEvent(QEvent *event)`
- `virtual void grabMouseEvent(QEvent *event)`
- `virtual void hideEvent(QHideEvent *event)`
- `virtual void initStyleOption(QStyleOption *option) const`
- `virtual void moveEvent(QGraphicsSceneMoveEvent *event)`
- `virtual void polishEvent()`
- `virtual void resizeEvent(QGraphicsSceneResizeEvent *event)`
- `virtual void showEvent(QShowEvent *event)`
- `virtual void ungrabKeyboardEvent(QEvent *event)`
- `virtual void ungrabMouseEvent(QEvent *event)`
- `virtual bool windowFrameEvent(QEvent *event)`
- `virtual Qt::WindowFrameSection windowFrameSectionAt(const QPointF &pos) const`

### 重实现的保护函数

- `virtual bool event(QEvent *event) override`
- `virtual void focusInEvent(QFocusEvent *event) override`
- `virtual void focusOutEvent(QFocusEvent *event) override`
- `virtual void hoverLeaveEvent(QGraphicsSceneHoverEvent *event) override`
- `virtual void hoverMoveEvent(QGraphicsSceneHoverEvent *event) override`
- `virtual QVariant itemChange(QGraphicsItem::GraphicsItemChange change, const QVariant &value) override`
- `virtual bool sceneEvent(QEvent *event) override`
- `virtual QSizeF sizeHint(Qt::SizeHint which, const QSizeF &constraint = QSizeF()) const override`
- `virtual void updateGeometry() override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[anonymous] enum`

**作用与语义：**

虚拟 `type()` 函数返回的值。
- `QGraphicsWidget::Type`: `11`；一个图形控件项

### `autoFillBackground : bool`

**作用与语义：**

该属性决定了小部件背景是否自动填充。
如果启用该属性，Qt 会在调用 `paint()` 方法前填充控件的背景。所用颜色由控件`palette`的 `QPalette::Window` 颜色角色定义。
此外，除非设置了WA_OpaquePaintEvent或 WA_NoSystemBackground 属性，否则 Windows 总是充满 `QPalette::Window`。
默认情况下，该属性为`false`。

**如何使用：** 调用 `autoFillBackground()` 读取当前值；它不会修改应用状态。

### `focusPolicy : Qt::FocusPolicy`

**作用与语义：**

该属性表示了小部件接受键盘焦点的方式。
焦点策略`Qt::TabFocus`，如果控件接受键盘对焦通过 Tab，`Qt::ClickFocus` 控件通过点击接受对焦，`Qt::StrongFocus` 如果两者都接受，`Qt::NoFocus`（默认）则不接受对焦。
如果控件处理键盘事件，你必须启用键盘焦点。这通常由控件的构造函数完成。例如，`QLineEdit`构造函数调用 setFocusPolicy（`Qt::StrongFocus`）。
如果你启用了焦点策略（即非`Qt::NoFocus`），`QGraphicsWidget`会自动启用ItemIsFocusable标志。在小部件上设置`Qt::NoFocus`会清除ItemIsFocusable标志。如果小部件当前有键盘焦点，小部件会自动失去焦点。

**如何使用：** 调用 `focusPolicy()` 读取当前值；它不会修改应用状态。

### `font : QFont`

**作用与语义：**

该属性包含控件的字体。
该属性提供了小部件的字体。
`QFont` 包含已明确定义的字体属性和从控件父节点隐式继承的属性。因此，font() 可能返回的字体与带有 setFont() 的字体不同。该方案允许你在不影响字体继承的条目的情况下定义单个字体条目。
当小部件的字体发生变化时，它会将其条目与父小部件对比。如果小部件没有父小部件，则会对场景进行解析。小部件随后会发送`FontChange`事件，并通知所有后代，以便它们也能解析自己的字体。
默认情况下，该属性包含应用程序的默认字体。

**如何使用：** 调用 `font()` 读取当前值；它不会修改应用状态。

### `geometry : QRectF`

**作用与语义：**

该属性包含了小部件的几何形状。
将物品的几何体设置为`rect`。调用该函数后，物品的位置和大小会被修改。物品先移动，然后调整大小。
调用该函数的一个副作用是，控件会接收移动事件和缩放事件。此外，如果控件被分配了布局，布局也会被激活。

**如何使用：** 调用 `geometry()` 读取当前值；它不会修改应用状态。

### `layout : QGraphicsLayout*`

**作用与语义：**

该属性包含了小部件的布局。
在新布局分配之前，任何现有的布局管理器都会被删除。如果`layout` `nullptr`，小部件将不再拥有布局。现有子小部件的几何形状将不受影响。
`QGraphicsWidget`对`layout`负责。
目前由`layout`或其所有子布局管理的所有控件，都会自动被重新父级到该项。随后该布局被废止，子控件几何体根据该项的 `geometry()` 和 contentsMargins() 进行调整。未被 `layout` 明确管理的子节点在被分配到该控件后布局不受其影响。
如果目前没有布局管理该小部件，layout() 会返回`nullptr`。

**如何使用：** 调用 `layout()` 读取当前值；它不会修改应用状态。

### `layoutDirection : Qt::LayoutDirection`

**作用与语义：**

该属性包含该控件的布局方向。
该属性修改该控件及其所有后代的 Widget `Qt::WA_RightToLeft`属性。它还设置了该控件的 `Qt::WA_SetLayoutDirection` 属性。
控件的布局方向决定了布局管理器水平排列该控件子控件的顺序。默认值取决于应用程序的语言和地区，通常与读写单词的方向相同。使用`Qt::LeftToRight`时，布局开始从该控件的左侧向右放置子控件。`Qt::RightToLeft`则相反——布局会从右边开始向左移动。
子控件继承父控件的布局方向。顶层控件的布局方向继承自 QGraphicsScene：：layoutDirection。如果你通过调用 setLayoutDirection() 更改控件的布局方向，该控件会发送一个`LayoutDirectionChange`事件，然后将新的布局方向传播给所有后代。

**如何使用：** 调用 `layoutDirection()` 读取当前值；它不会修改应用状态。

### `maximumSize : QSizeF`

**作用与语义：**

该属性表示了小部件的最大大小。

**如何使用：** 调用 `maximumSize()` 读取当前值；它不会修改应用状态。

### `minimumSize : QSizeF`

**作用与语义：**

该属性表示了小部件的最小大小。

**如何使用：** 调用 `minimumSize()` 读取当前值；它不会修改应用状态。

### `palette : QPalette`

**作用与语义：**

该属性包含了小部件的调色板。
该属性提供了控件的调色板。调色板为颜色组（例如`QPalette::Button`）和状态（例如`QPalette::Inactive`）提供颜色和笔刷，松散地定义了控件及其子节点的一般外观。
`QPalette` 由已明确定义的颜色组和从控件父项隐式继承的颜色组组成。因此，palette() 可以返回与 setPalette() 设置的不同调色板。该方案允许您在调色板中定义单个条目而不影响调色板继承的条目。
当一个小部件的调色板发生变化时，它会根据父小部件解析其条目，或者如果没有父小部件，则会根据场景进行解析。然后它会发送一个`PaletteChange`事件，并通知所有后代，以便它们也能解析自己的调色板。
默认情况下，该属性包含应用程序的默认调色板。

**如何使用：** 调用 `palette()` 读取当前值；它不会修改应用状态。

### `preferredSize : QSizeF`

**作用与语义：**

该属性表示了小部件的首选大小。

**如何使用：** 调用 `preferredSize()` 读取当前值；它不会修改应用状态。

### `size : QSizeF`

**作用与语义：**

该属性表示小部件的大小。
调用 resize() 会将控件调整为由 `minimumSize()` 和 `maximumSize()` 组成的 `size`。该属性仅影响控件的宽度和高度（例如其左右边缘）;控件的位置和左上角不受影响。
调整小部件大小会触发小部件立即接收包含该小部件旧大小和新大小的`GraphicsSceneResize`事件。如果该小部件在事件到达时已分配了布局，该布局将被激活，并自动更新任何子小部件的几何体。
该属性不影响父控件的任何布局。如果控件本身由父控件管理;例如，它有一个分配了布局的父控件，该布局不会被激活。
默认情况下，该属性包含宽度和高度均为零的大小。

**如何使用：** 调用 `size()` 读取当前值；它不会修改应用状态。

### `sizePolicy : QSizePolicy`

**作用与语义：**

该属性表示了小部件的大小策略。

**如何使用：** 调用 `sizePolicy()` 读取当前值；它不会修改应用状态。

### `windowFlags : Qt::WindowFlags`

**作用与语义：**

该属性保留了小部件的窗口标志。
窗口标志是窗口类型（例如`Qt::Dialog`）和多个为窗口行为提供提示的标志的组合。该行为依赖于平台。
默认情况下，该属性不包含窗口标志。
窗口是面板。如果你设置了`Qt::Window`标志，ItemIsPanel 标志将自动被设置。如果你清除了`Qt::Window`标志，ItemIsPanel 标志也会被清除。注意，ItemIsPanel 标志可以独立于`Qt::Window`设置。

**如何使用：** 调用 `windowFlags()` 读取当前值；它不会修改应用状态。

### `windowTitle : QString`

**作用与语义：**

该物业拥有窗户产权（说明）。
该物业仅用于窗户。
默认情况下，如果没有设置标题，该属性包含空字符串。

**如何使用：** 调用 `windowTitle()` 读取当前值；它不会修改应用状态。

### `QGraphicsWidget::QGraphicsWidget(QGraphicsItem *parent = nullptr, Qt::WindowFlags wFlags = Qt::WindowFlags())`

**作用与语义：**

构建一个QGraphicsWidget实例。可选的`parent`参数传递给`QGraphicsItem`的构造函数。可选的`wFlags`参数指定控件的窗口标志（例如，控件应是窗口、工具、弹窗等等）。

### `[virtual noexcept] QGraphicsWidget::~QGraphicsWidget()`

**作用与语义：**

会摧毁`QGraphicsWidget`实例。

### `QList<QAction *> QGraphicsWidget::actions() const`

**作用与语义：**

返回该控件的（可能是空的）动作列表。

### `void QGraphicsWidget::addAction(QAction *action)`

**作用与语义：**

将动作`action`附加到该控件的操作列表中。
所有 QGraphicsWidgets 都有 `QAction` 的列表，但它们可以用多种不同的图形方式表示。`QAction`列表（由 `actions()` 返回）的默认用途是创建上下文 `QMenu`。
一个`QGraphicsWidget`应该只有每个动作的一个，添加它已有的动作不会导致同一个动作在小部件中出现两次。

### `void QGraphicsWidget::addActions(const QList<QAction *> &actions)`

**作用与语义：**

将`actions`动作附加到该小部件的动作列表中。

### `void QGraphicsWidget::adjustSize()`

**作用与语义：**

调整小部件大小以符合其有效首选大小提示。
当该项首次被展示时，该函数被隐式调用。

### `[override virtual] QRectF QGraphicsWidget::boundingRect() const`

**作用与语义：**

重实现自：`QGraphicsItem::boundingRect()` const.
这个纯虚拟函数将物品的外边界定义为矩形;所有绘画必须限制在物品的边界矩形内。`QGraphicsView`用此来判断物品是否需要重新绘制。
虽然物品的形状可以任意，但边界矩形始终是矩形，且不受物品变换的影响。
如果你想更改物品的边界矩形，必须先调用`prepareGeometryChange()`。这会通知场景即将发生的变化，以便更新物品几何索引;否则，场景将无法感知物品的新几何体，结果也未定义（通常渲染伪影会留在视图中）。
重新实现这个函数，让`QGraphicsView`判断小部件哪些部分需要重新绘制。
注意：对于绘制轮廓/笔画的形状，在包围矩形中包含一半的笔宽非常重要。不过，这并不需要补偿抗锯齿。

### `[virtual protected] void QGraphicsWidget::changeEvent(QEvent *event)`

**作用与语义：**

该事件处理程序可以重新实现以处理状态变化。
该事件中被更改的状态可以通过`event`获取。
变更事件包括：`QEvent::ActivationChange`、`QEvent::EnabledChange`、`QEvent::FontChange`、`QEvent::StyleChange`、`QEvent::PaletteChange`、`QEvent::ParentChange`、`QEvent::LayoutDirectionChange`和`QEvent::ContentsRectChange`。

### `[slot] bool QGraphicsWidget::close()`

**作用与语义：**

调用这个函数来关闭小部件。
如果小部件被关闭，返回`true`;否则返回`false`。该槽会先向小部件发送`QCloseEvent`，小部件可能接受也可能不接受。如果事件被忽略，则不会发生任何事。如果事件被接受，则会`hide()`小部件。
如果小部件设置了`Qt::WA_DeleteOnClose`属性，它将被删除。

### `[virtual protected] void QGraphicsWidget::closeEvent(QCloseEvent *event)`

**作用与语义：**

对于`event`来说，这个事件处理程序可以在子类中重新实现，以接收小部件关闭事件。默认实现接受该事件。

### `[override virtual protected] bool QGraphicsWidget::event(QEvent *event)`

**作用与语义：**

重装：`QGraphicsObject::event`（QEvent *ev）。
负责`event`。`QGraphicsWidget`处理以下事件：
- `Event`：使用情况
- `Polish`：在展示后不久交付给小部件。
- `GraphicsSceneMove`：在小部件本地位置发生变化后交付。
- `GraphicsSceneResize`：在控件大小变化后交付。
- `Show`：在小部件展示前交付。
- `Hide`：隐藏后交付给小部件。
- `PaletteChange`：在控件调色板更改后交付。
- `FontChange`：在小部件字体更改后交付。
- `EnabledChange`：在控件启用状态发生变化后交付。
- `StyleChange`：在控件样式变更后交付。
- `LayoutDirectionChange`：在控件布局方向改变后交付。
- `ContentsRectChange`：在控件内容边距/目录rect发生变化后交付。

### `[override virtual protected] void QGraphicsWidget::focusInEvent(QFocusEvent *event)`

**作用与语义：**

重实现自：`QGraphicsItem::focusInEvent`（QFocusEvent *event）。
该事件处理程序对于事件`event`，可以重新实现以获得该项事件中的关注。默认实现调用`ensureVisible()`。

### `[virtual protected] bool QGraphicsWidget::focusNextPrevChild(bool next)`

**作用与语义：**

找到一个新的控件以赋予键盘焦点，适用于 Tab 和 Shift Tab，如果能找到新控件则返回 `true`;否则返回`false`。如果 `next` 为真，该函数向前搜索;如果 `next` 为假，则向后搜索。
有时，你会想重新实现这个函数，为你的小部件及其子小部件提供特殊的焦点处理。例如，浏览器可能会重新实现它，将当前活跃链接向前或向后移动，只有在到达页面最后或第一个链接时调用基础实现。
子控件在其父控件上调用 focusNextPrevChild()，但只有包含子控件的窗口决定将焦点重定向到哪里。通过为对象重新实现该函数，你可以控制所有子控件的焦点遍历。

### `[override virtual protected] void QGraphicsWidget::focusOutEvent(QFocusEvent *event)`

**作用与语义：**

重实现自：`QGraphicsItem::focusOutEvent`（QFocusEvent *事件）。
对于事件`event`，这个事件处理程序可以重新实现，以接收该项的焦点输出事件。默认实现不做任何事。

### `QGraphicsWidget *QGraphicsWidget::focusWidget() const`

**作用与语义：**

如果该控件、其子节点或后代当前拥有输入焦点，该函数将返回指向该控件的指针。如果没有后代控件具有输入焦点，则返回`nullptr`。

### `[signal] void QGraphicsWidget::geometryChanged()`

**作用与语义：**

该属性包含了小部件的几何形状。
将物品的几何体设置为`rect`。调用该函数后，物品的位置和大小会被修改。物品先移动，然后调整大小。
调用该函数的一个副作用是，控件会接收移动事件和缩放事件。此外，如果控件被分配了布局，布局也会被激活。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `geometry` 的变化，不要把它当作普通函数主动调用。

### `[override virtual] void QGraphicsWidget::getContentsMargins(qreal *left, qreal *top, qreal *right, qreal *bottom) const`

**作用与语义：**

重实现自：`QGraphicsLayoutItem::getContentsMargins`（qreal *左，qreal *top，qreal *right，qreal *bottom）const.
获取小部件的内容边距。边距存储在`left`、`top`、`right`和`bottom`，作为指向qreal的指针。每个参数都可以通过传递`nullptr`来省略。
该虚拟函数为该`QGraphicsLayoutItem`提供`left`、`top`、`right`和`bottom`的内容余距。默认实现假设所有内容边距均为0。参数指向存储在qreal中的值。如果任何指针被`nullptr`，该值不会被更新。

### `void QGraphicsWidget::getWindowFrameMargins(qreal *left, qreal *top, qreal *right, qreal *bottom) const`

**作用与语义：**

获取小部件的窗口框架边距。边距存储在`left`、`top`、`right`和`bottom`中，作为指向qreal的指针。每个参数可以通过传递`nullptr`省略。

### `[virtual protected] void QGraphicsWidget::grabKeyboardEvent(QEvent *event)`

**作用与语义：**

`event`，这个事件处理程序可以在子类中重新实现，以接收 `QEvent::GrabKeyboard` 事件的通知。

### `[virtual protected] void QGraphicsWidget::grabMouseEvent(QEvent *event)`

**作用与语义：**

`event`，这个事件处理程序可以重新实现到子类中，以接收`QEvent::GrabMouse`事件的通知。

### `int QGraphicsWidget::grabShortcut(const QKeySequence &sequence, Qt::ShortcutContext context = Qt::WindowShortcut)`

**作用与语义：**

为Qt的快捷方式系统添加一个快捷方式，监控给定`context`中的密钥`sequence`。如果`context` `Qt::ApplicationShortcut`，则该快捷方式适用于整个应用程序。否则，快捷方式要么是该控件本地的，`Qt::WidgetShortcut`，要么是窗口本身的，`Qt::WindowShortcut`。对于不属于窗口的控件（即顶层控件及其子控件），`Qt::WindowShortcut`快捷方式适用于场景。
如果同一个密钥`sequence`被多个控件抓取，当密钥`sequence`发生时，会以非确定性顺序向所有适用该控件发送`QEvent::Shortcut`事件，但“模糊”标志设置为true。
警告：通常不需要使用这个函数;如果你也想要相应的菜单选项和工具栏按钮，可以创建带有快捷键序列的`QAction`，或者如果只需要按键序列，可以创建`QShortcut`。`QAction`和`QShortcut`都帮你处理所有事件过滤，并提供当用户触发按键序列时触发的信号，因此比这个低层函数更易于使用。

### `[virtual protected] void QGraphicsWidget::hideEvent(QHideEvent *event)`

**作用与语义：**

对于`Hide`事件，这个事件处理程序是在小部件被隐藏后交付的，例如，当小部件之前显示时，已调用该小部件或其前祖之一的setVisible（false）。
你可以重新实现这个事件处理程序，检测你的小部件是否被隐藏。调用`QEvent::accept()`或`QEvent::ignore()`对`event`没有任何影响。

### `[override virtual protected] void QGraphicsWidget::hoverLeaveEvent(QGraphicsSceneHoverEvent *event)`

**作用与语义：**

重实现自：`QGraphicsItem::hoverLeaveEvent`（QGraphicsSceneHoverEvent *event）。
对于事件`event`，这个事件处理程序可以重新实现，以接收该项的悬停离开事件。默认实现调用`update()`;否则不做任何事。
在`event`上打电话给`QEvent::ignore()`或`QEvent::accept()`没有任何效果。

### `[override virtual protected] void QGraphicsWidget::hoverMoveEvent(QGraphicsSceneHoverEvent *event)`

**作用与语义：**

重实现自：`QGraphicsItem::hoverMoveEvent`（QGraphicsSceneHoverEvent *event）。
该事件处理程序对于事件`event`，可以重新实现以接收该项的悬停移动事件。默认实现不做任何事。
打电话给`QEvent::ignore()`或`QEvent::accept()`打`event`没有效果。

### `[virtual protected] void QGraphicsWidget::initStyleOption(QStyleOption *option) const`

**作用与语义：**

根据该控件当前状态填充样式选项对象，并将输出存储在`option`中。默认实现会为`option`填充以下属性。
- `Style Option Property`：价值
- `state & `QStyle：：State_Enabled`: Corresponds to `QGraphicsItem：：isEnabled()'。
- `state & `QStyle：：State_HasFocus`: Corresponds to `QGraphicsItem：：hasFocus()'。
- `state & `QStyle：：State_MouseOver`: Corresponds to `QGraphicsItem：：isUnderMouse()'。
- `direction`：对应`QGraphicsWidget::layoutDirection()`。
- `rect`：对应于`QGraphicsWidget::rect()`.toRect()。
- `palette`：对应`QGraphicsWidget::palette()`。
- `fontMetrics`：对应于`QFontMetrics`（`QGraphicsWidget::font()`）。
`QGraphicsWidget`的子类应调用基础实现，然后用 `qstyleoption_cast`<>() 或测试 `QStyleOption::Type` 测试 `option`类型，再存储特定控件选项。

**官方示例：**

```cpp
 void MyGroupBoxWidget::initStyleOption(QStyleOption *option) const
 {
     QGraphicsWidget::initStyleOption(option);
     if (QStyleOptionGroupBox *box = qstyleoption_cast<QStyleOptionGroupBox *>(option)) {
         // Add group box specific state.
         box->flat = isFlat();
         ...
     }
 }
```

### `void QGraphicsWidget::insertAction(QAction *before, QAction *action)`

**作用与语义：**

在该控件`before`动作之前，将动作`action`插入到该控件的动作列表中。如果`before`是`nullptr`或`before`不是该控件的有效动作，则会附加该动作。
一个`QGraphicsWidget`应该每种动作都只有一个。

### `void QGraphicsWidget::insertActions(QAction *before, const QList<QAction *> &actions)`

**作用与语义：**

在动作 `before` 前，将`actions`动作插入该控件的动作列表。如果`before`是`nullptr`或`before`不是该控件的有效动作，则会附加该动作。
一个`QGraphicsWidget`最多只能有每种动作的一次。

### `bool QGraphicsWidget::isActiveWindow() const`

**作用与语义：**

返回`true`该小部件的窗口是否在活动窗口中，或者该小部件没有窗口但处于当前有焦点的场景中。
活动窗口是包含当前具有输入焦点的子控件，或本身具有输入焦点的窗口。

### `[override virtual protected] QVariant QGraphicsWidget::itemChange(QGraphicsItem::GraphicsItemChange change, const QVariant &value)`

**作用与语义：**

重实现自：`QGraphicsItem::itemChange`（QGraphicsItem：：GraphicsItemChange change， const QVariant &value）。
`QGraphicsWidget` 使用该函数的基础实现来捕捉并传递与项目状态变化相关的事件。因此，子类调用基础实现非常重要。
`change` 指定变更类型，`value` 是新的值。
例如，`QGraphicsWidget` 使用 ItemVisibleChange 传递`Show`和`Hide`事件，ItemPositionHasChanged 传递`Move`事件，ItemParentChange 既用于传递`ParentChange`事件，也用于管理焦点链。
`QGraphicsWidget`默认启用了ItemSendsGeometryChanges标志以跟踪位置变化。
`QGraphicsItem`调用该虚拟函数，以通知自定义项目的某部分状态发生变化。通过重新实现该函数，你可以对变化做出反应，在某些情况下（取决于`change`）还可以进行调整。
`change` 是正在变化的项的参数。`value` 是新值;值的类型取决于`change`。
默认实现不做任何操作，返回`value`。
注意：某些`QGraphicsItem`函数无法在该函数的重实现中调用;详情请参见`GraphicsItemChange`文档。

### `QGraphicsLayout *QGraphicsWidget::layout() const`

**作用与语义：**

返回该控件的布局，若当前无布局管理该控件则返回`nullptr`。
注意：用于物业布局的获取函数。

### `[virtual protected] void QGraphicsWidget::moveEvent(QGraphicsSceneMoveEvent *event)`

**作用与语义：**

对于`GraphicsSceneMove`事件，该事件处理程序是在小部件移动后交付的（例如其本地位置发生变化）。
该事件仅在物品本地移动时执行。调用`setTransform()`或移动物品的祖先不会影响物品的本地位置。
你可以重新实现这个事件处理程序，检测你的小部件是否移动了。调用`QEvent::accept()`或`QEvent::ignore()`对`event`没有影响。

### `[override virtual] void QGraphicsWidget::paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget = nullptr)`

**作用与语义：**

Reimplements： `QGraphicsItem::paint`（QPainter *painter， const QStyleOptionGraphicsItem *option， QWidget *widget）.
该函数通常由`QGraphicsView`调用，将物品内容绘制为局部坐标。
在`QGraphicsItem`子类中重新实现该函数，使用`painter`来提供该物品的绘画实现。`option`参数为物品提供了样式选项，如状态、暴露区域和细节层级提示。`widget`参数是可选的。如果提供了，它指向正在绘制的控件;否则为0。对于缓存绘制，`widget`总是0。
画家的笔默认为0宽，笔初始化为从画具调色板中的`QPalette::Text`笔。画笔初始化为`QPalette::Window`。
确保所有绘画都限制在`boundingRect()`边界内，以避免渲染伪影（因为`QGraphicsView`不会帮你裁剪画家）。特别是，当`QPainter`用指定`QPen`渲染形状轮廓时，轮廓的一半会在外侧绘制，另一半在你正在渲染的形状内侧（例如，笔宽为2单位时，你必须在`boundingRect()`内绘制1单位的轮廓）。`QGraphicsItem`不支持使用宽度非零的美观笔。
所有涂装均在本地坐标内完成。
注意：除非调用`update()`，否则物品必须始终以完全相同的方式重新绘制自己;否则可能会出现视觉伪影。换句话说，两次后续的paint()调用必须始终产生相同的输出，除非它们之间调用了`update()`。
注意：启用缓存并不保证图形视图框架只调用一次 paint()，即使没有明确调用 `update()`。详情请参见 `setCacheMode()` 文档。

### `[virtual] void QGraphicsWidget::paintWindowFrame(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget = nullptr)`

**作用与语义：**

`QGraphicsScene`调用该虚拟函数，在局部坐标中使用`painter`、`option`和`widget`绘制窗口框架。基础实现使用当前样式渲染框架和标题栏。
你可以在`QGraphicsWidget`的子类中重新实现这个函数，以提供小部件窗口框的自定义渲染。

### `[virtual protected] void QGraphicsWidget::polishEvent()`

**作用与语义：**

该事件会在物品构建后、但通过场景显示或访问之前，由场景传递给该物品。你可以使用这个事件处理程序对需要物品完全构建的控件进行最后的初始化。
基础实现什么都没有。

### `QRectF QGraphicsWidget::rect() const`

**作用与语义：**

返回该项的局部rect作为`QRectF`。该函数等价于`QRectF`（QPointF()， `size()`）。

### `void QGraphicsWidget::releaseShortcut(int id)`

**作用与语义：**

从 Qt 的快捷方式系统中移除该快捷方式的该`id`。小部件将不再接收快捷方式按键序列的 `QEvent::Shortcut` 事件（除非它有其他具有相同按键序列的快捷方式）。
警告：通常不需要使用该函数，因为 Qt 的快捷方式系统在父控件被破坏时会自动移除快捷方式。最好使用`QAction`或`QShortcut`来处理快捷方式，因为它们比这个底层函数更易使用。另外请注意，这是一个昂贵的操作。

### `void QGraphicsWidget::removeAction(QAction *action)`

**作用与语义：**

将该动作`action`从该小部件的操作列表中移除。

### `void QGraphicsWidget::resize(qreal w, qreal h)`

**作用与语义：**

该属性表示小部件的大小。
调用 resize() 会将控件调整为由 `minimumSize()` 和 `maximumSize()` 组成的 `size`。该属性仅影响控件的宽度和高度（例如其左右边缘）;控件的位置和左上角不受影响。
调整小部件大小会触发小部件立即接收包含该小部件旧大小和新大小的`GraphicsSceneResize`事件。如果该小部件在事件到达时已分配了布局，该布局将被激活，并自动更新任何子小部件的几何体。
该属性不影响父控件的任何布局。如果控件本身由父控件管理;例如，它有一个分配了布局的父控件，该布局不会被激活。
默认情况下，该属性包含宽度和高度均为零的大小。

**如何使用：** 调用 `resize()` 读取当前值；它不会修改应用状态。

### `[virtual protected] void QGraphicsWidget::resizeEvent(QGraphicsSceneResizeEvent *event)`

**作用与语义：**

对于`GraphicsSceneResize`事件，该事件处理程序是在控件调整大小（即其局部大小改变）后交付的。`event`包含旧大小和新大小。
该事件仅在控件本地调整大小时执行;调用控件或其任何祖先或视图的`setTransform()`不会影响控件的本地大小。
你可以重新实现这个事件处理程序，检测你的小部件是否被调整了大小。调用`QEvent::accept()`或`QEvent::ignore()`在`event`上没有效果。

### `[override virtual protected] bool QGraphicsWidget::sceneEvent(QEvent *event)`

**作用与语义：**

重实现自：`QGraphicsItem::sceneEvent`（QEvent *事件）。
`QGraphicsWidget` 的 sceneEvent() 实现只是把`event`传递给 `QGraphicsWidget::event()`。你可以在 `event()` 或任何便利函数中处理你的小部件的所有事件;你不应该需要在 `QGraphicsWidget` 的子类中重新实现这个函数。
如果`event`已被识别和处理，返回`true`;否则返回`false`。
该虚拟函数接收该项的事件。在事件处理器 `contextMenuEvent()`、`focusInEvent()`、`focusOutEvent()`、`hoverEnterEvent()`、`hoverMoveEvent()`、`hoverLeaveEvent()`、`keyPressEvent()`、`keyReleaseEvent()`、`mousePressEvent()`、`mouseReleaseEvent()`、`mouseMoveEvent()` 和 `mouseDoubleClickEvent()` 之前，重新实现该函数以拦截事件。
如果事件被识别并处理，返回 `true`;否则（例如，如果事件类型未被识别），则返回 false。
`event` 是被截获的事件。

### `void QGraphicsWidget::setAttribute(Qt::WidgetAttribute attribute, bool on = true)`

**作用与语义：**

如果`on`为真，该函数使 `attribute` 成为可能;否则`attribute`被禁用。
请参阅`QGraphicsWidget`类文档，了解支持哪些属性及其用途的完整列表。

### `void QGraphicsWidget::setContentsMargins(QMarginsF margins)`

**作用与语义：**

将小部件的内容边距设置为`margins`。
目录边距用于指定布局，用于定义子控件和布局的位置。边距对于限制子控件仅在其自身几何体部分的控件中尤为有用。例如，带有布局的组框会将子控件放置在框架内，但位于标题下方。
更改小部件的内容边距总是会触发`update()`，任何分配的布局都会自动激活。小部件随后会收到一个`ContentsRectChange`事件。

### `void QGraphicsWidget::setContentsMargins(qreal left, qreal top, qreal right, qreal bottom)`

**作用与语义：**

将小部件的内容边距设置为`left`、`top`、`right`和`bottom`。

### `void QGraphicsWidget::setGeometry(qreal x, qreal y, qreal w, qreal h)`

**作用与语义：**

该属性包含了小部件的几何形状。
将物品的几何体设置为`rect`。调用该函数后，物品的位置和大小会被修改。物品先移动，然后调整大小。
调用该函数的一个副作用是，控件会接收移动事件和缩放事件。此外，如果控件被分配了布局，布局也会被激活。

**如何使用：** 调用 `setGeometry(...)` 修改 `geometry`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QGraphicsWidget::setLayout(QGraphicsLayout *layout)`

**作用与语义：**

该属性包含了小部件的布局。
在新布局分配之前，任何现有的布局管理器都会被删除。如果`layout` `nullptr`，小部件将不再拥有布局。现有子小部件的几何形状将不受影响。
`QGraphicsWidget`对`layout`负责。
目前由`layout`或其所有子布局管理的所有控件，都会自动被重新父级到该项。随后该布局被废止，子控件几何体根据该项的 `geometry()` 和 contentsMargins() 进行调整。未被 `layout` 明确管理的子节点在被分配到该控件后布局不受其影响。
如果目前没有布局管理该小部件，layout() 会返回`nullptr`。

**如何使用：** 调用 `setLayout(...)` 修改 `layout`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QGraphicsWidget::setShortcutAutoRepeat(int id, bool enabled = true)`

**作用与语义：**

如果`enabled`为真，则启用了用该`id`自动重复快捷方式;否则该功能被禁用。

### `void QGraphicsWidget::setShortcutEnabled(int id, bool enabled = true)`

**作用与语义：**

如果`enabled`为真，则启用了该`id`的快捷方式;否则该快捷方式被禁用。
警告：通常不需要使用这个函数，因为Qt的快捷方式系统会在控件变得隐藏/可见时自动启用或禁用快捷方式，并会显示焦点的得失。最好使用`QAction`或`QShortcut`来处理快捷方式，因为它们比这个低阶函数更容易使用。

### `void QGraphicsWidget::setStyle(QStyle *style)`

**作用与语义：**

将小部件的样式设置为`style`。`QGraphicsWidget`不拥有`style`。
如果没有被分配样式，或者`style` `nullptr`，小部件将使用 `QGraphicsScene::style()`（如果已设置的话）。否则小部件将使用 `QApplication::style()`。
如果 `style` 未被`nullptr`，该函数将设置 `Qt::WA_SetStyle` 属性;否则则清除该属性。

### `[static] void QGraphicsWidget::setTabOrder(QGraphicsWidget *first, QGraphicsWidget *second)`

**作用与语义：**

将`second`小部件绕着焦点控件环移动，使得按下Tab键时键盘焦点从`first`控件转移到`second`控件。
注意，由于`second`小部件的制表顺序发生了变化，你应该像这样排序链条：
不是这样：
如果`first` `nullptr`，表示如果场景获得Tab焦点（即用户按Tab使焦点进入场景），`second`应是第一个接收输入焦点的控件。如果`second` `nullptr`，则表示如果场景获得BackTab焦点，`first`应是第一个获得焦点的控件。
默认情况下，制表顺序通过小部件创建顺序隐式定义。

**官方示例：**

```cpp
 setTabOrder(a, b); // a to b
 setTabOrder(b, c); // a to b to c
 setTabOrder(c, d); // a to b to c to d
```

### `void QGraphicsWidget::setWindowFrameMargins(QMarginsF margins)`

**作用与语义：**

将小部件的窗口框边距设置为`margins`。默认的边距由样式提供，且依赖于当前的窗口标志。
如果你想自己画窗户装饰，可以设置自己的框架边距覆盖默认边距。

### `void QGraphicsWidget::setWindowFrameMargins(qreal left, qreal top, qreal right, qreal bottom)`

**作用与语义：**

将小部件的窗口框边距设置为`left`、`top`、`right`和`bottom`。

### `[override virtual] QPainterPath QGraphicsWidget::shape() const`

**作用与语义：**

重装：`QGraphicsItem::shape()` const.
返回该项的形状，作为本地坐标中的`QPainterPath`。该形状用于多种用途，包括碰撞检测、碰撞测试以及`QGraphicsScene::items()`函数。
默认实现调用 `boundingRect()` 返回一个简单的矩形形状，但子类可以重新实现该函数，以返回非矩形物体更准确的形状。例如，一个圆形项目可能会选择返回椭圆形形状以更好地检测碰撞。例如：
形状的轮廓会根据绘画时笔的宽度和风格而变化。如果你想在物体的形状中包含这个轮廓，可以用`QPainterPathStroker`从笔触中创建形状。
该函数由默认实现的`contains()`和`collidesWithPath()`调用。

### `[virtual protected] void QGraphicsWidget::showEvent(QShowEvent *event)`

**作用与语义：**

对于`Show`事件，这个事件处理程序在小部件尚未显示之前就被交付，例如，当小部件之前隐藏时，setVisible（true） 已被调用。
你可以重新实现这个事件处理程序，检测你的小部件是否被显示。调用`QEvent::accept()`或`QEvent::ignore()`在`event`上没有效果。

### `[override virtual protected] QSizeF QGraphicsWidget::sizeHint(Qt::SizeHint which, const QSizeF &constraint = QSizeF()) const`

**作用与语义：**

重实现自：`QGraphicsLayoutItem::sizeHint`（Qt：：SizeHint which， const QSizeF & constraint） const.
该纯虚拟函数返回`QGraphicsLayoutItem` `which`的大小提示，利用`constraint`的宽度或高度来约束输出。
在`QGraphicsLayoutItem`的一个子类中重新实现这个函数，以提供物品所需的尺寸提示。

### `QStyle *QGraphicsWidget::style() const`

**作用与语义：**

返回指向小部件样式的指针。如果该小部件没有显式分配的样式，则返回场景的样式。反之，如果场景没有分配样式，该函数返回`QApplication::style()`。

### `bool QGraphicsWidget::testAttribute(Qt::WidgetAttribute attribute) const`

**作用与语义：**

如果此小部件启用了 `attribute`，则返回 `true`；否则，返回 `false`。

### `[override virtual] int QGraphicsWidget::type() const`

**作用与语义：**

重装：`QGraphicsItem::type()` const.
返回一个项目的类型，作为整数。所有标准的 Graphicsitem 类都关联一个唯一的值;参见`QGraphicsItem::Type`。`qgraphicsitem_cast()` 利用这些类型信息来区分类型。
默认实现（`QGraphicsItem`）返回`UserType`。
要启用自定义物品中的 `qgraphicsitem_cast()`，请重新实现该函数并声明一个等于自定义物品类型的 Type enum 值。自定义物品必须返回大于 `UserType`（65536）的值。

### `[virtual protected] void QGraphicsWidget::ungrabKeyboardEvent(QEvent *event)`

**作用与语义：**

`event`，这个事件处理程序可以重新实现到子类中，以接收`QEvent::UngrabKeyboard`事件的通知。

### `[virtual protected] void QGraphicsWidget::ungrabMouseEvent(QEvent *event)`

**作用与语义：**

`event`，这个事件处理程序可以在子类中重新实现，以接收`QEvent::UngrabMouse`事件的通知。

### `void QGraphicsWidget::unsetWindowFrameMargins()`

**作用与语义：**

将窗框边距重置为样式提供的默认值。

### `[override virtual protected] void QGraphicsWidget::updateGeometry()`

**作用与语义：**

重装：`QGraphicsLayoutItem::updateGeometry()`。
如果该小部件目前由布局管理，该函数会通知布局小部件的大小提示发生变化，布局可能需要相应调整大小和位置。
如果小部件的 `sizeHint()` 发生变化，就调用这个函数。
这个虚拟函数会丢弃任何缓存大小提示信息。如果你更改了`sizeHint()`函数的返回值，你应该总是调用这个函数。子类在重新实现该函数时必须始终调用基础实现。

### `[virtual protected] bool QGraphicsWidget::windowFrameEvent(QEvent *event)`

**作用与语义：**

对于`event`来说，如果该控件是窗口，该事件处理程序会接收窗口框架的事件。其基础实现支持默认窗口框架交互，如移动、调整大小等。
你可以在`QGraphicsWidget`子类中重新实现这个处理程序，提供你自己的自定义窗口框架交互支持。
如果`event`已被识别和处理，返回`true`;否则，返回`false`。

### `QRectF QGraphicsWidget::windowFrameGeometry() const`

**作用与语义：**

返回小部件的几何体，包含父坐标，包括任何窗口框架。

### `QRectF QGraphicsWidget::windowFrameRect() const`

**作用与语义：**

返回小部件的本地rect，包括任何窗口框架。

### `[virtual protected] Qt::WindowFrameSection QGraphicsWidget::windowFrameSectionAt(const QPointF &pos) const`

**作用与语义：**

返回位于位置`pos`的窗框部分，若该位置没有窗框部分则返回`Qt::NoSection`。
该函数用于`QGraphicsWidget`的窗口框架交互基础实现中。
如果你想自定义窗口的交互式移动或调整大小，可以重新实现这个函数。例如，如果你只允许窗口右下角调整大小，可以重新实现该函数，使除`Qt::BottomRightSection`外的所有部分返回`Qt::NoSection`。

### `Qt::WindowType QGraphicsWidget::windowType() const`

**作用与语义：**

返回小部件窗口类型。

### `enum { Type }`

**作用与语义：**

虚拟 `type()` 函数返回的值。
- `QGraphicsWidget::Type`: `11`；一个图形控件项

### `bool autoFillBackground() const`

**作用与语义：**

该属性决定了小部件背景是否自动填充。
如果启用该属性，Qt 会在调用 `paint()` 方法前填充控件的背景。所用颜色由控件`palette`的 `QPalette::Window` 颜色角色定义。
此外，除非设置了WA_OpaquePaintEvent或 WA_NoSystemBackground 属性，否则 Windows 总是充满 `QPalette::Window`。
默认情况下，该属性为`false`。

**如何使用：** 调用 `autoFillBackground()` 读取当前值；它不会修改应用状态。

### `Qt::FocusPolicy focusPolicy() const`

**作用与语义：**

该属性表示了小部件接受键盘焦点的方式。
焦点策略`Qt::TabFocus`，如果控件接受键盘对焦通过 Tab，`Qt::ClickFocus` 控件通过点击接受对焦，`Qt::StrongFocus` 如果两者都接受，`Qt::NoFocus`（默认）则不接受对焦。
如果控件处理键盘事件，你必须启用键盘焦点。这通常由控件的构造函数完成。例如，`QLineEdit`构造函数调用 setFocusPolicy（`Qt::StrongFocus`）。
如果你启用了焦点策略（即非`Qt::NoFocus`），`QGraphicsWidget`会自动启用ItemIsFocusable标志。在小部件上设置`Qt::NoFocus`会清除ItemIsFocusable标志。如果小部件当前有键盘焦点，小部件会自动失去焦点。

**如何使用：** 调用 `focusPolicy()` 读取当前值；它不会修改应用状态。

### `QFont font() const`

**作用与语义：**

该属性包含控件的字体。
该属性提供了小部件的字体。
`QFont` 包含已明确定义的字体属性和从控件父节点隐式继承的属性。因此，font() 可能返回的字体与带有 setFont() 的字体不同。该方案允许你在不影响字体继承的条目的情况下定义单个字体条目。
当小部件的字体发生变化时，它会将其条目与父小部件对比。如果小部件没有父小部件，则会对场景进行解析。小部件随后会发送`FontChange`事件，并通知所有后代，以便它们也能解析自己的字体。
默认情况下，该属性包含应用程序的默认字体。

**如何使用：** 调用 `font()` 读取当前值；它不会修改应用状态。

### `Qt::LayoutDirection layoutDirection() const`

**作用与语义：**

该属性包含该控件的布局方向。
该属性修改该控件及其所有后代的 Widget `Qt::WA_RightToLeft`属性。它还设置了该控件的 `Qt::WA_SetLayoutDirection` 属性。
控件的布局方向决定了布局管理器水平排列该控件子控件的顺序。默认值取决于应用程序的语言和地区，通常与读写单词的方向相同。使用`Qt::LeftToRight`时，布局开始从该控件的左侧向右放置子控件。`Qt::RightToLeft`则相反——布局会从右边开始向左移动。
子控件继承父控件的布局方向。顶层控件的布局方向继承自 QGraphicsScene：：layoutDirection。如果你通过调用 setLayoutDirection() 更改控件的布局方向，该控件会发送一个`LayoutDirectionChange`事件，然后将新的布局方向传播给所有后代。

**如何使用：** 调用 `layoutDirection()` 读取当前值；它不会修改应用状态。

### `QPalette palette() const`

**作用与语义：**

该属性包含了小部件的调色板。
该属性提供了控件的调色板。调色板为颜色组（例如`QPalette::Button`）和状态（例如`QPalette::Inactive`）提供颜色和笔刷，松散地定义了控件及其子节点的一般外观。
`QPalette` 由已明确定义的颜色组和从控件父项隐式继承的颜色组组成。因此，palette() 可以返回与 setPalette() 设置的不同调色板。该方案允许您在调色板中定义单个条目而不影响调色板继承的条目。
当一个小部件的调色板发生变化时，它会根据父小部件解析其条目，或者如果没有父小部件，则会根据场景进行解析。然后它会发送一个`PaletteChange`事件，并通知所有后代，以便它们也能解析自己的调色板。
默认情况下，该属性包含应用程序的默认调色板。

**如何使用：** 调用 `palette()` 读取当前值；它不会修改应用状态。

### `void resize(const QSizeF &size)`

**作用与语义：**

该属性表示小部件的大小。
调用 resize() 会将控件调整为由 `minimumSize()` 和 `maximumSize()` 组成的 `size`。该属性仅影响控件的宽度和高度（例如其左右边缘）;控件的位置和左上角不受影响。
调整小部件大小会触发小部件立即接收包含该小部件旧大小和新大小的`GraphicsSceneResize`事件。如果该小部件在事件到达时已分配了布局，该布局将被激活，并自动更新任何子小部件的几何体。
该属性不影响父控件的任何布局。如果控件本身由父控件管理;例如，它有一个分配了布局的父控件，该布局不会被激活。
默认情况下，该属性包含宽度和高度均为零的大小。

**如何使用：** 调用 `resize()` 读取当前值；它不会修改应用状态。

### `void setAutoFillBackground(bool enabled)`

**作用与语义：**

该属性决定了小部件背景是否自动填充。
如果启用该属性，Qt 会在调用 `paint()` 方法前填充控件的背景。所用颜色由控件`palette`的 `QPalette::Window` 颜色角色定义。
此外，除非设置了WA_OpaquePaintEvent或 WA_NoSystemBackground 属性，否则 Windows 总是充满 `QPalette::Window`。
默认情况下，该属性为`false`。

**如何使用：** 调用 `setAutoFillBackground(...)` 修改 `autoFillBackground`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setFocusPolicy(Qt::FocusPolicy policy)`

**作用与语义：**

该属性表示了小部件接受键盘焦点的方式。
焦点策略`Qt::TabFocus`，如果控件接受键盘对焦通过 Tab，`Qt::ClickFocus` 控件通过点击接受对焦，`Qt::StrongFocus` 如果两者都接受，`Qt::NoFocus`（默认）则不接受对焦。
如果控件处理键盘事件，你必须启用键盘焦点。这通常由控件的构造函数完成。例如，`QLineEdit`构造函数调用 setFocusPolicy（`Qt::StrongFocus`）。
如果你启用了焦点策略（即非`Qt::NoFocus`），`QGraphicsWidget`会自动启用ItemIsFocusable标志。在小部件上设置`Qt::NoFocus`会清除ItemIsFocusable标志。如果小部件当前有键盘焦点，小部件会自动失去焦点。

**如何使用：** 调用 `setFocusPolicy(...)` 修改 `focusPolicy`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setFont(const QFont &font)`

**作用与语义：**

该属性包含控件的字体。
该属性提供了小部件的字体。
`QFont` 包含已明确定义的字体属性和从控件父节点隐式继承的属性。因此，font() 可能返回的字体与带有 setFont() 的字体不同。该方案允许你在不影响字体继承的条目的情况下定义单个字体条目。
当小部件的字体发生变化时，它会将其条目与父小部件对比。如果小部件没有父小部件，则会对场景进行解析。小部件随后会发送`FontChange`事件，并通知所有后代，以便它们也能解析自己的字体。
默认情况下，该属性包含应用程序的默认字体。

**如何使用：** 调用 `setFont(...)` 修改 `font`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `virtual void setGeometry(const QRectF &rect) override`

**作用与语义：**

该属性包含了小部件的几何形状。
将物品的几何体设置为`rect`。调用该函数后，物品的位置和大小会被修改。物品先移动，然后调整大小。
调用该函数的一个副作用是，控件会接收移动事件和缩放事件。此外，如果控件被分配了布局，布局也会被激活。

**如何使用：** 调用 `setGeometry(...)` 修改 `geometry`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setLayoutDirection(Qt::LayoutDirection direction)`

**作用与语义：**

该属性包含该控件的布局方向。
该属性修改该控件及其所有后代的 Widget `Qt::WA_RightToLeft`属性。它还设置了该控件的 `Qt::WA_SetLayoutDirection` 属性。
控件的布局方向决定了布局管理器水平排列该控件子控件的顺序。默认值取决于应用程序的语言和地区，通常与读写单词的方向相同。使用`Qt::LeftToRight`时，布局开始从该控件的左侧向右放置子控件。`Qt::RightToLeft`则相反——布局会从右边开始向左移动。
子控件继承父控件的布局方向。顶层控件的布局方向继承自 QGraphicsScene：：layoutDirection。如果你通过调用 setLayoutDirection() 更改控件的布局方向，该控件会发送一个`LayoutDirectionChange`事件，然后将新的布局方向传播给所有后代。

**如何使用：** 调用 `setLayoutDirection(...)` 修改 `layoutDirection`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setPalette(const QPalette &palette)`

**作用与语义：**

该属性包含了小部件的调色板。
该属性提供了控件的调色板。调色板为颜色组（例如`QPalette::Button`）和状态（例如`QPalette::Inactive`）提供颜色和笔刷，松散地定义了控件及其子节点的一般外观。
`QPalette` 由已明确定义的颜色组和从控件父项隐式继承的颜色组组成。因此，palette() 可以返回与 setPalette() 设置的不同调色板。该方案允许您在调色板中定义单个条目而不影响调色板继承的条目。
当一个小部件的调色板发生变化时，它会根据父小部件解析其条目，或者如果没有父小部件，则会根据场景进行解析。然后它会发送一个`PaletteChange`事件，并通知所有后代，以便它们也能解析自己的调色板。
默认情况下，该属性包含应用程序的默认调色板。

**如何使用：** 调用 `setPalette(...)` 修改 `palette`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setWindowFlags(Qt::WindowFlags wFlags)`

**作用与语义：**

该属性保留了小部件的窗口标志。
窗口标志是窗口类型（例如`Qt::Dialog`）和多个为窗口行为提供提示的标志的组合。该行为依赖于平台。
默认情况下，该属性不包含窗口标志。
窗口是面板。如果你设置了`Qt::Window`标志，ItemIsPanel 标志将自动被设置。如果你清除了`Qt::Window`标志，ItemIsPanel 标志也会被清除。注意，ItemIsPanel 标志可以独立于`Qt::Window`设置。

**如何使用：** 调用 `setWindowFlags(...)` 修改 `windowFlags`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setWindowTitle(const QString &title)`

**作用与语义：**

该物业拥有窗户产权（说明）。
该物业仅用于窗户。
默认情况下，如果没有设置标题，该属性包含空字符串。

**如何使用：** 调用 `setWindowTitle(...)` 修改 `windowTitle`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QSizeF size() const`

**作用与语义：**

该属性表示小部件的大小。
调用 resize() 会将控件调整为由 `minimumSize()` 和 `maximumSize()` 组成的 `size`。该属性仅影响控件的宽度和高度（例如其左右边缘）;控件的位置和左上角不受影响。
调整小部件大小会触发小部件立即接收包含该小部件旧大小和新大小的`GraphicsSceneResize`事件。如果该小部件在事件到达时已分配了布局，该布局将被激活，并自动更新任何子小部件的几何体。
该属性不影响父控件的任何布局。如果控件本身由父控件管理;例如，它有一个分配了布局的父控件，该布局不会被激活。
默认情况下，该属性包含宽度和高度均为零的大小。

**如何使用：** 调用 `size()` 读取当前值；它不会修改应用状态。

### `void unsetLayoutDirection()`

**作用与语义：**

该属性包含该控件的布局方向。
该属性修改该控件及其所有后代的 Widget `Qt::WA_RightToLeft`属性。它还设置了该控件的 `Qt::WA_SetLayoutDirection` 属性。
控件的布局方向决定了布局管理器水平排列该控件子控件的顺序。默认值取决于应用程序的语言和地区，通常与读写单词的方向相同。使用`Qt::LeftToRight`时，布局开始从该控件的左侧向右放置子控件。`Qt::RightToLeft`则相反——布局会从右边开始向左移动。
子控件继承父控件的布局方向。顶层控件的布局方向继承自 QGraphicsScene：：layoutDirection。如果你通过调用 setLayoutDirection() 更改控件的布局方向，该控件会发送一个`LayoutDirectionChange`事件，然后将新的布局方向传播给所有后代。

**如何使用：** 调用 `unsetLayoutDirection()` 读取当前值；它不会修改应用状态。

### `Qt::WindowFlags windowFlags() const`

**作用与语义：**

该属性保留了小部件的窗口标志。
窗口标志是窗口类型（例如`Qt::Dialog`）和多个为窗口行为提供提示的标志的组合。该行为依赖于平台。
默认情况下，该属性不包含窗口标志。
窗口是面板。如果你设置了`Qt::Window`标志，ItemIsPanel 标志将自动被设置。如果你清除了`Qt::Window`标志，ItemIsPanel 标志也会被清除。注意，ItemIsPanel 标志可以独立于`Qt::Window`设置。

**如何使用：** 调用 `windowFlags()` 读取当前值；它不会修改应用状态。

### `QString windowTitle() const`

**作用与语义：**

该物业拥有窗户产权（说明）。
该物业仅用于窗户。
默认情况下，如果没有设置标题，该属性包含空字符串。

**如何使用：** 调用 `windowTitle()` 读取当前值；它不会修改应用状态。

### `void layoutChanged()`

**作用与语义：**

该属性包含了小部件的布局。
在新布局分配之前，任何现有的布局管理器都会被删除。如果`layout` `nullptr`，小部件将不再拥有布局。现有子小部件的几何形状将不受影响。
`QGraphicsWidget`对`layout`负责。
目前由`layout`或其所有子布局管理的所有控件，都会自动被重新父级到该项。随后该布局被废止，子控件几何体根据该项的 `geometry()` 和 contentsMargins() 进行调整。未被 `layout` 明确管理的子节点在被分配到该控件后布局不受其影响。
如果目前没有布局管理该小部件，layout() 会返回`nullptr`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `layout` 的变化，不要把它当作普通函数主动调用。

## 6. 深入实践与常见坑

### 生命周期和资源边界

场景或父项目通常管理子项目，但视图只是观察者，不一定拥有场景。删除项目、改变父项目或切换场景时要确认索引、指针、选中状态和布局关系是否仍有效。

### 状态和错误边界

区分局部坐标、场景坐标、视图/窗口坐标，区分选中、悬停、焦点、可见和碰撞状态。改变几何、变换或数据后通常请求更新，而不是手动强制调用绘制函数。

### 线程边界

图形对象通常只能在其所属 GUI/场景线程操作；后台线程负责数据准备，结果通过信号投递后再更新场景对象。

### 最容易出现的错误

优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QGraphicsWidget` 所属机制类型：图形场景与项目机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
