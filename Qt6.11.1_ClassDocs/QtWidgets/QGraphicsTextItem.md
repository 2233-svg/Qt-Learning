# QGraphicsTextItem

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QGraphicsTextItem` 是 图形场景与项目机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QGraphicsTextItem` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QGraphicsTextItem>`
- 继承自：QGraphicsObject
- 直接派生类：未在类页中列出

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

- `openExternalLinks : bool`
- `textCursor : QTextCursor`

### 公有函数

- `QGraphicsTextItem(QGraphicsItem *parent = nullptr)`
- `QGraphicsTextItem(const QString &text, QGraphicsItem *parent = nullptr)`
- `virtual ~QGraphicsTextItem()`
- `void adjustSize()`
- `QColor defaultTextColor() const`
- `QTextDocument * document() const`
- `QFont font() const`
- `bool openExternalLinks() const`
- `void setDefaultTextColor(const QColor &col)`
- `void setDocument(QTextDocument *document)`
- `void setFont(const QFont &font)`
- `void setHtml(const QString &text)`
- `void setOpenExternalLinks(bool open)`
- `void setPlainText(const QString &text)`
- `void setTabChangesFocus(bool b)`
- `void setTextCursor(const QTextCursor &cursor)`
- `void setTextInteractionFlags(Qt::TextInteractionFlags flags)`
- `void setTextWidth(qreal width)`
- `bool tabChangesFocus() const`
- `QTextCursor textCursor() const`
- `Qt::TextInteractionFlags textInteractionFlags() const`
- `qreal textWidth() const`
- `QString toHtml() const`
- `QString toPlainText() const`

### 重实现的公有函数

- `virtual QRectF boundingRect() const override`
- `virtual bool contains(const QPointF &point) const override`
- `virtual bool isObscuredBy(const QGraphicsItem *item) const override`
- `virtual QPainterPath opaqueArea() const override`
- `virtual void paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget) override`
- `virtual QPainterPath shape() const override`
- `virtual int type() const override`

### 信号

- `void linkActivated(const QString &link)`
- `void linkHovered(const QString &link)`

### 重实现的保护函数

- `virtual void contextMenuEvent(QGraphicsSceneContextMenuEvent *event) override`
- `virtual void dragEnterEvent(QGraphicsSceneDragDropEvent *event) override`
- `virtual void dragLeaveEvent(QGraphicsSceneDragDropEvent *event) override`
- `virtual void dragMoveEvent(QGraphicsSceneDragDropEvent *event) override`
- `virtual void dropEvent(QGraphicsSceneDragDropEvent *event) override`
- `virtual void focusInEvent(QFocusEvent *event) override`
- `virtual void focusOutEvent(QFocusEvent *event) override`
- `virtual void hoverEnterEvent(QGraphicsSceneHoverEvent *event) override`
- `virtual void hoverLeaveEvent(QGraphicsSceneHoverEvent *event) override`
- `virtual void hoverMoveEvent(QGraphicsSceneHoverEvent *event) override`
- `virtual void inputMethodEvent(QInputMethodEvent *event) override`
- `virtual QVariant inputMethodQuery(Qt::InputMethodQuery query) const override`
- `virtual void keyPressEvent(QKeyEvent *event) override`
- `virtual void keyReleaseEvent(QKeyEvent *event) override`
- `virtual void mouseDoubleClickEvent(QGraphicsSceneMouseEvent *event) override`
- `virtual void mouseMoveEvent(QGraphicsSceneMouseEvent *event) override`
- `virtual void mousePressEvent(QGraphicsSceneMouseEvent *event) override`
- `virtual void mouseReleaseEvent(QGraphicsSceneMouseEvent *event) override`
- `virtual bool sceneEvent(QEvent *event) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[anonymous] enum`

**作用与语义：**

虚拟 `type()` 函数返回的值。
- `QGraphicsTextItem::Type`: `8`；一个图形文本项

### `openExternalLinks : bool`

**作用与语义：**

规定是否`QGraphicsTextItem`应使用`QDesktopServices::openUrl()`自动开启链路，而不是发出`linkActivated`信号。
默认值为假。

**如何使用：** 调用 `openExternalLinks()` 读取当前值；它不会修改应用状态。

### `textCursor : QTextCursor`

**作用与语义：**

该属性表示可编辑文本项中的可见文本光标。
默认情况下，如果项目文本未被设置，该属性包含一个空文本光标;否则，它包含放置在项目文档开头的文本光标。

**如何使用：** 调用 `textCursor()` 读取当前值；它不会修改应用状态。

### `[explicit] QGraphicsTextItem::QGraphicsTextItem(QGraphicsItem *parent = nullptr)`

**作用与语义：**

构造一个QGraphicsTextItem。`parent`传递给`QGraphicsItem`的构造器。

### `[explicit] QGraphicsTextItem::QGraphicsTextItem(const QString &text, QGraphicsItem *parent = nullptr)`

**作用与语义：**

构造一个QGraphicsTextItem，`text`作为默认明文。`parent`传递给`QGraphicsItem`的构造器。

### `[virtual noexcept] QGraphicsTextItem::~QGraphicsTextItem()`

**作用与语义：**

摧毁了`QGraphicsTextItem`。

### `void QGraphicsTextItem::adjustSize()`

**作用与语义：**

将文本项调整到合理的大小。

### `[override virtual] QRectF QGraphicsTextItem::boundingRect() const`

**作用与语义：**

重实现自：`QGraphicsItem::boundingRect()` const.
这个纯虚拟函数将物品的外边界定义为矩形;所有绘画必须限制在物品的边界矩形内。`QGraphicsView`用此来判断物品是否需要重新绘制。
虽然物品的形状可以任意，但边界矩形始终是矩形，且不受物品变换的影响。
如果你想更改物品的边界矩形，必须先调用`prepareGeometryChange()`。这会通知场景即将发生的变化，以便更新物品几何索引;否则，场景将无法感知物品的新几何体，结果也未定义（通常渲染伪影会留在视图中）。
重新实现这个函数，让`QGraphicsView`判断小部件哪些部分需要重新绘制。
注意：对于绘制轮廓/笔画的形状，在包围矩形中包含一半的笔宽非常重要。不过，这并不需要补偿抗锯齿。

### `[override virtual] bool QGraphicsTextItem::contains(const QPointF &point) const`

**作用与语义：**

重实现自：`QGraphicsItem::contains`（const QPointF & point） const.
如果该项包含`point`，且位于本地坐标内，则返回`true`;否则返回 false。它通常被调用`QGraphicsView`来确定光标下方的物品，因此该函数的实现应尽可能轻量。
默认情况下，这个函数调用`shape()`，但你可以在子类中重新实现，以提供（或许更高效的）实现。

### `[override virtual protected] void QGraphicsTextItem::contextMenuEvent(QGraphicsSceneContextMenuEvent *event)`

**作用与语义：**

重实现自：`QGraphicsItem::contextMenuEvent`（QGraphicsSceneContextMenuEvent *event）。
该事件处理程序可以被重新实现为子类以处理上下文菜单事件。`event`参数包含待处理事件的详细信息。
如果你忽略该事件（即调用`QEvent::ignore()`），`event`会传播到该事件下方的任何项目。如果没有项目接受该事件，场景会忽略它并传播到视图。
收到上下文菜单事件后，通常会打开`QMenu`。示例：
默认实现会忽略该事件。

### `QColor QGraphicsTextItem::defaultTextColor() const`

**作用与语义：**

返回用于未格式文本的默认文本颜色。

### `QTextDocument *QGraphicsTextItem::document() const`

**作用与语义：**

返回该物品的文本文档。

### `[override virtual protected] void QGraphicsTextItem::dragEnterEvent(QGraphicsSceneDragDropEvent *event)`

**作用与语义：**

重实现自：`QGraphicsItem::dragEnterEvent`（QGraphicsSceneDragDropEvent *event）。
该事件处理程序对于事件`event`，可以重新实现以接收该项目的拖入事件。拖入事件是在光标进入该物品区域时生成的。
通过接受事件（即调用`QEvent::accept()`），物品将接受掉落事件，同时接收拖动移动和拖离事件。否则，事件将被忽略并传播到下面的物品。如果事件被接受，物品将接收拖动移动事件，然后控制权返回事件循环。
dragEnterEvent 的一个常见实现会根据 `event` 中关联的 mime 数据接受或忽略`event`。示例：
物品默认不会接收拖放事件;要启用此功能，请调用`setAcceptDrops(true)`。
默认实现什么都不做。

### `[override virtual protected] void QGraphicsTextItem::dragLeaveEvent(QGraphicsSceneDragDropEvent *event)`

**作用与语义：**

重实现自：`QGraphicsItem::dragLeaveEvent`（QGraphicsSceneDragDropEvent *event）。
该事件处理程序（事件`event`）可以重新实现，以接收该物品的拖曳离开事件。拖曳离开事件是在光标离开物品区域时生成的。大多数情况下你不需要重新实现这个函数，但它对重置物品状态（例如高亮）非常有用。
`event`打电话给`QEvent::ignore()`或`QEvent::accept()`没有任何影响。
项目默认不会接收拖放事件;要启用此功能，请调用`setAcceptDrops(true)`。
默认实现什么都不做。

### `[override virtual protected] void QGraphicsTextItem::dragMoveEvent(QGraphicsSceneDragDropEvent *event)`

**作用与语义：**

重实现自：`QGraphicsItem::dragMoveEvent`（QGraphicsSceneDragDropEvent *event）。
对于事件`event`，这个事件处理程序可以重新实现，以接收该物品的拖动移动事件。拖动移动事件是在光标在物品区域内移动时生成的。大多数情况下你不需要重新实现这个函数;它用来表示只有物品的部分可以接受掉落。
在`event`上调用`QEvent::ignore()`或`QEvent::accept()`，可以切换该物品是否接受该事件位置的掉落。默认情况下，`event`被接受，表示该物品允许在指定位置掉落。
物品默认不会接收拖放事件;要启用此功能，请调用`setAcceptDrops(true)`。
默认实现什么都不做。

### `[override virtual protected] void QGraphicsTextItem::dropEvent(QGraphicsSceneDragDropEvent *event)`

**作用与语义：**

重实现自：`QGraphicsItem::dropEvent`（QGraphicsSceneDragDropEvent *event）。
该事件处理程序用于事件`event`，可以重新实现以接收该物品的掉落事件。只有当最后一次拖动移动事件被接受时，物品才能接收掉落事件。
打电话给`QEvent::ignore()`或`QEvent::accept()` `event`没有效果。
物品默认不会接收拖放事件;要启用此功能，请调用`setAcceptDrops(true)`。
默认实现什么都不做。

### `[override virtual protected] void QGraphicsTextItem::focusInEvent(QFocusEvent *event)`

**作用与语义：**

重实现自：`QGraphicsItem::focusInEvent`（QFocusEvent *event）。
该事件处理程序对于事件`event`，可以重新实现以获得该项事件中的关注。默认实现调用`ensureVisible()`。

### `[override virtual protected] void QGraphicsTextItem::focusOutEvent(QFocusEvent *event)`

**作用与语义：**

重实现自：`QGraphicsItem::focusOutEvent`（QFocusEvent *事件）。
对于事件`event`，这个事件处理程序可以重新实现，以接收该项的焦点输出事件。默认实现不做任何事。

### `QFont QGraphicsTextItem::font() const`

**作用与语义：**

返回该物品的字体，用于渲染文本。

### `[override virtual protected] void QGraphicsTextItem::hoverEnterEvent(QGraphicsSceneHoverEvent *event)`

**作用与语义：**

重实现自：`QGraphicsItem::hoverEnterEvent`（QGraphicsSceneHoverEvent *event）。
该事件处理程序对于事件`event`，可以重新实现以接收该项的悬停进入事件。默认实现调用`update()`;否则不做任何操作。
打电话给`QEvent::ignore()`或`QEvent::accept()`对`event`没有影响。

### `[override virtual protected] void QGraphicsTextItem::hoverLeaveEvent(QGraphicsSceneHoverEvent *event)`

**作用与语义：**

重实现自：`QGraphicsItem::hoverLeaveEvent`（QGraphicsSceneHoverEvent *event）。
对于事件`event`，这个事件处理程序可以重新实现，以接收该项的悬停离开事件。默认实现调用`update()`;否则不做任何事。
在`event`上打电话给`QEvent::ignore()`或`QEvent::accept()`没有任何效果。

### `[override virtual protected] void QGraphicsTextItem::hoverMoveEvent(QGraphicsSceneHoverEvent *event)`

**作用与语义：**

重实现自：`QGraphicsItem::hoverMoveEvent`（QGraphicsSceneHoverEvent *event）。
该事件处理程序对于事件`event`，可以重新实现以接收该项的悬停移动事件。默认实现不做任何事。
打电话给`QEvent::ignore()`或`QEvent::accept()`打`event`没有效果。

### `[override virtual protected] void QGraphicsTextItem::inputMethodEvent(QInputMethodEvent *event)`

**作用与语义：**

Reimplements： `QGraphicsItem::inputMethodEvent`（QInputMethodEvent *event）.
该事件处理程序对于事件`event`，可以重新实现以接收该项的输入法事件。默认实现忽略该事件。

### `[override virtual protected] QVariant QGraphicsTextItem::inputMethodQuery(Qt::InputMethodQuery query) const`

**作用与语义：**

重实现自：`QGraphicsItem::inputMethodQuery`（Qt：：InputMethodQuery query） const.
该方法仅对输入项相关。输入方法用它来查询项的一组属性，以支持复杂的输入法操作，如支持周围文本和重新转换。`query` 指定查询的属性。

### `[override virtual] bool QGraphicsTextItem::isObscuredBy(const QGraphicsItem *item) const`

**作用与语义：**

重实现自：`QGraphicsItem::isObscuredBy`（const QGraphicsItem *item） const.
如果该物品的边界矩形完全被不透明的`item`形状遮挡，返回`true`。
基础实现将`item`的`opaqueArea()`映射到该项目的坐标系，然后检查该项目的`boundingRect()`是否完全包含在映射形状内。
你可以重新实现这个函数，提供一个自定义算法来判断该项是否被`item`遮挡。

### `[override virtual protected] void QGraphicsTextItem::keyPressEvent(QKeyEvent *event)`

**作用与语义：**

重实现自：`QGraphicsItem::keyPressEvent`（QKeyEvent *event）。
该事件处理程序（针对事件`event`）可以重新实现以接收该项的按键事件。默认实现忽略该事件。如果你重新实现该处理程序，事件默认会被接受。
注意，键事件只会针对设置`ItemIsFocusable`标志且具有键盘输入焦点的物品。

### `[override virtual protected] void QGraphicsTextItem::keyReleaseEvent(QKeyEvent *event)`

**作用与语义：**

重实现自：`QGraphicsItem::keyReleaseEvent`（QKeyEvent *event）。
该事件处理程序（针对事件`event`）可以重新实现以接收该项的密钥释放事件。默认实现忽略该事件。如果你重新实现该处理程序，该事件默认会被接受。
注意，键事件只会针对设置`ItemIsFocusable`标志且带有键盘输入焦点的物品。

### `[signal] void QGraphicsTextItem::linkActivated(const QString &link)`

**作用与语义：**

当用户点击文本项上的链接以实现`Qt::LinksAccessibleByMouse`或`Qt::LinksAccessibleByKeyboard`时，会发出该信号。`link`是被点击的链接。

### `[signal] void QGraphicsTextItem::linkHovered(const QString &link)`

**作用与语义：**

当用户将鼠标悬停在启用`Qt::LinksAccessibleByMouse`的文本项上的链接上时，会发出该信号。`link` 就是被悬停在的链接。

### `[override virtual protected] void QGraphicsTextItem::mouseDoubleClickEvent(QGraphicsSceneMouseEvent *event)`

**作用与语义：**

重实现自：`QGraphicsItem::mouseDoubleClickEvent`（QGraphicsSceneMouseEvent *event）。
该事件处理程序对于事件`event`，可以重新实现以接收该项的鼠标双击事件。
双击物品时，该物品首先会触发鼠标按键事件，接着是释放事件（即点击），再是双击事件，最后是释放事件。
打电话给`QEvent::ignore()`或`QEvent::accept()`打`event`没有效果。
默认实现调用`mousePressEvent()`。如果你想在重新实现这个函数时保留基础实现，可以在你的重实现中调用 QGraphicsItem：：mouseDoubleClickEvent()。
注意，如果物品既非`selectable`也非`movable`，则不会触发双击事件（此时忽略单次鼠标点击，导致双击停止生成）。

### `[override virtual protected] void QGraphicsTextItem::mouseMoveEvent(QGraphicsSceneMouseEvent *event)`

**作用与语义：**

重实现自：`QGraphicsItem::mouseMoveEvent`（QGraphicsSceneMouseEvent *event）。
该事件处理程序（事件`event`）可以重新实现，以接收该物品的鼠标移动事件。如果你收到该事件，可以确定该物品也收到了鼠标按键事件，并且该物品是当前的鼠标抓取器。
`event`打电话给`QEvent::ignore()`或`QEvent::accept()`没有任何影响。
默认实现处理基本的项目交互，比如选择和移动。如果你想在重现这个函数时保留基础实现，可以在你的重实现中调用 QGraphicsItem：：mouseMoveEvent()。
请注意，`mousePressEvent()`决定接收鼠标事件的图形项目。详情请参见`mousePressEvent()`描述。

### `[override virtual protected] void QGraphicsTextItem::mousePressEvent(QGraphicsSceneMouseEvent *event)`

**作用与语义：**

重实现自：`QGraphicsItem::mousePressEvent`（QGraphicsSceneMouseEvent *event）。
该事件处理程序对于事件`event`，可以重新实现以接收该物品的鼠标按键事件。鼠标按键事件只传递给接受被按下鼠标按钮的物品。默认情况下，物品接受所有鼠标按键，但你可以通过调用`setAcceptedMouseButtons()`来更改。
鼠标按键事件决定哪个物品应成为鼠标抓取器（参见`QGraphicsScene::mouseGrabberItem()`）。如果不重新实现此功能，按键事件将传播到该物品下方的最顶端任何物品，且不会有其他鼠标事件传递到该物品。
如果你重新实现了这个功能，`event`默认会被接受（见`QEvent::accept()`），这个物品就是鼠标抓取器。这允许该物品接收未来的移动、释放和双击事件。如果你在`event`上调用`QEvent::ignore()`，这个物品将失去鼠标抓取功能，`event`会传播到最下面的任何物品。除非收到新的鼠标按键事件，否则不会再传递给该物品。
默认实现处理基本的物品交互，比如选择和移动。如果你想在重现这个函数时保留基础实现，可以在重构中调用 QGraphicsItem：：mousePressEvent()。
对于既非`movable`也非`selectable`的项目，事件为`QEvent::ignore()`d。

### `[override virtual protected] void QGraphicsTextItem::mouseReleaseEvent(QGraphicsSceneMouseEvent *event)`

**作用与语义：**

重实现自：`QGraphicsItem::mouseReleaseEvent`（QGraphicsSceneMouseEvent *event）。
该事件处理程序对于事件`event`，可以重新实现以接收该项的鼠标释放事件。
打电话给`QEvent::ignore()`或`QEvent::accept()` `event`没有效果。
默认实现处理基本的物品操作，比如选择和移动。如果你想在重现这个函数时保留基础实现，可以在重写中调用 QGraphicsItem：：mouseReleaseEvent()。
请注意，`mousePressEvent()`决定接收鼠标事件的图形项目。详情请参见`mousePressEvent()`描述。

### `[override virtual] QPainterPath QGraphicsTextItem::opaqueArea() const`

**作用与语义：**

重实现自：`QGraphicsItem::opaqueArea()` const.
该虚拟函数返回一个形状，表示该项不透明的区域。如果该区域用不透明的画笔或颜色填充（即不透明），则该区域是不透明的。
该函数由`isObscuredBy()`使用，底层项目调用以确定是否被该项遮挡。
默认实现返回空`QPainterPath`，表明该项完全透明且未遮挡其他项。

### `[override virtual] void QGraphicsTextItem::paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget)`

**作用与语义：**

Reimplements： `QGraphicsItem::paint`（QPainter *painter， const QStyleOptionGraphicsItem *option， QWidget *widget）.
该函数通常由`QGraphicsView`调用，将物品内容绘制为局部坐标。
在`QGraphicsItem`子类中重新实现该函数，使用`painter`来提供该物品的绘画实现。`option`参数为物品提供了样式选项，如状态、暴露区域和细节层级提示。`widget`参数是可选的。如果提供了，它指向正在绘制的控件;否则为0。对于缓存绘制，`widget`总是0。
画家的笔默认为0宽，笔初始化为从画具调色板中的`QPalette::Text`笔。画笔初始化为`QPalette::Window`。
确保所有绘画都限制在`boundingRect()`边界内，以避免渲染伪影（因为`QGraphicsView`不会帮你裁剪画家）。特别是，当`QPainter`用指定`QPen`渲染形状轮廓时，轮廓的一半会在外侧绘制，另一半在你正在渲染的形状内侧（例如，笔宽为2单位时，你必须在`boundingRect()`内绘制1单位的轮廓）。`QGraphicsItem`不支持使用宽度非零的美观笔。
所有涂装均在本地坐标内完成。
注意：除非调用`update()`，否则物品必须始终以完全相同的方式重新绘制自己;否则可能会出现视觉伪影。换句话说，两次后续的paint()调用必须始终产生相同的输出，除非它们之间调用了`update()`。
注意：启用缓存并不保证图形视图框架只调用一次 paint()，即使没有明确调用 `update()`。详情请参见 `setCacheMode()` 文档。

### `[override virtual protected] bool QGraphicsTextItem::sceneEvent(QEvent *event)`

**作用与语义：**

重装：`QGraphicsItem::sceneEvent`（QEvent *事件）。
该虚拟函数接收该项的事件。在事件发送到专用事件处理程序`contextMenuEvent()`、`focusInEvent()`、`focusOutEvent()`、`hoverEnterEvent()`、`hoverMoveEvent()`、`hoverLeaveEvent()`、`keyPressEvent()`、`keyReleaseEvent()`、`mousePressEvent()`、`mouseReleaseEvent()`、`mouseMoveEvent()`和`mouseDoubleClickEvent()`之前，重新实现该函数。
如果事件被识别并处理，返回 `true`;否则（例如，如果事件类型未被识别），返回 false。
`event` 是截获的事件。

### `void QGraphicsTextItem::setDefaultTextColor(const QColor &col)`

**作用与语义：**

将未格式文本的颜色设置为`col`。

### `void QGraphicsTextItem::setDocument(QTextDocument *document)`

**作用与语义：**

将文本文档`document`到该物品上。

### `void QGraphicsTextItem::setFont(const QFont &font)`

**作用与语义：**

将用于渲染文本的字体设置为`font`。

### `void QGraphicsTextItem::setHtml(const QString &text)`

**作用与语义：**

将该物品的文本设置为`text`，前提是文本为HTML格式。如果该物品具有键盘输入焦点，该函数还会调用`ensureVisible()`以确保文本在所有视口中可见。

### `void QGraphicsTextItem::setPlainText(const QString &text)`

**作用与语义：**

将该物品的文本设置为`text`。如果该物品具有键盘输入焦点，该函数还会调用`ensureVisible()`，确保文本在所有视口中可见。

### `void QGraphicsTextItem::setTabChangesFocus(bool b)`

**作用与语义：**

如果`b`为真，Tab 键会使控件改变焦点;否则，Tab 键会在文档中插入一个 Tab。
在某些情况下，文本编辑不应允许用户使用Tab键输入计表器或更改缩进，因为这会破坏焦点链。默认为false。

### `void QGraphicsTextItem::setTextInteractionFlags(Qt::TextInteractionFlags flags)`

**作用与语义：**

设置`flags`标志，指定文本项目应如何响应用户输入。
`QGraphicsTextItem`的默认是`Qt::NoTextInteraction`。该功能还会影响ItemIsFocusable `QGraphicsItem`标志，如果`flags`与`Qt::NoTextInteraction`不同，则清除。
默认情况下，文本是只读的。要将该项目转换为编辑器，请设置`Qt::TextEditable`标志。

### `void QGraphicsTextItem::setTextWidth(qreal width)`

**作用与语义：**

设置该项目文本的首选宽度。如果实际文本宽度超过指定宽度，则会被拆分成多行。
如果`width`设置为-1，文本不会被拆分为多行，除非通过明确的换行或新段落强制执行。
默认值为-1。
注意`QGraphicsTextItem`内部会保留一个`QTextDocument`，用于计算文本宽度。

### `[override virtual] QPainterPath QGraphicsTextItem::shape() const`

**作用与语义：**

重装：`QGraphicsItem::shape()` const.
返回该项的形状，作为本地坐标中的`QPainterPath`。该形状用于多种用途，包括碰撞检测、碰撞测试以及`QGraphicsScene::items()`函数。
默认实现调用 `boundingRect()` 返回一个简单的矩形形状，但子类可以重新实现该函数，以返回非矩形物体更准确的形状。例如，一个圆形项目可能会选择返回椭圆形形状以更好地检测碰撞。例如：
形状的轮廓会根据绘画时笔的宽度和风格而变化。如果你想在物体的形状中包含这个轮廓，可以用`QPainterPathStroker`从笔触中创建形状。
该函数由默认实现的`contains()`和`collidesWithPath()`调用。

### `bool QGraphicsTextItem::tabChangesFocus() const`

**作用与语义：**

如果 Tab 键会导致控件改变焦点，返回 `true`;否则返回 false。
默认情况下，该行为被禁用，该函数将返回 false。

### `Qt::TextInteractionFlags QGraphicsTextItem::textInteractionFlags() const`

**作用与语义：**

返回当前的文本交互标志。

### `qreal QGraphicsTextItem::textWidth() const`

**作用与语义：**

返回文本宽度。
宽度是根据`QGraphicsTextItem`内部保持的`QTextDocument`计算的。

### `QString QGraphicsTextItem::toHtml() const`

**作用与语义：**

返回已转换为HTML的物品文本，若未设置文本则返回空的`QString`。

### `QString QGraphicsTextItem::toPlainText() const`

**作用与语义：**

返回将物品的文本转换为纯文本，或者如果没有设置文本则返回空`QString`。

### `[override virtual] int QGraphicsTextItem::type() const`

**作用与语义：**

重装：`QGraphicsItem::type()` const.
返回一个项目的类型，作为整数。所有标准的 Graphicsitem 类都关联一个唯一的值;参见`QGraphicsItem::Type`。`qgraphicsitem_cast()` 利用这些类型信息来区分类型。
默认实现（`QGraphicsItem`）返回`UserType`。
要启用自定义物品中的 `qgraphicsitem_cast()`，请重新实现该函数并声明一个等于自定义物品类型的 Type enum 值。自定义物品必须返回大于 `UserType`（65536）的值。

### `enum { Type }`

**作用与语义：**

虚拟 `type()` 函数返回的值。
- `QGraphicsTextItem::Type`: `8`；一个图形文本项

### `bool openExternalLinks() const`

**作用与语义：**

规定是否`QGraphicsTextItem`应使用`QDesktopServices::openUrl()`自动开启链路，而不是发出`linkActivated`信号。
默认值为假。

**如何使用：** 调用 `openExternalLinks()` 读取当前值；它不会修改应用状态。

### `void setOpenExternalLinks(bool open)`

**作用与语义：**

规定是否`QGraphicsTextItem`应使用`QDesktopServices::openUrl()`自动开启链路，而不是发出`linkActivated`信号。
默认值为假。

**如何使用：** 调用 `setOpenExternalLinks(...)` 修改 `openExternalLinks`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTextCursor(const QTextCursor &cursor)`

**作用与语义：**

该属性表示可编辑文本项中的可见文本光标。
默认情况下，如果项目文本未被设置，该属性包含一个空文本光标;否则，它包含放置在项目文档开头的文本光标。

**如何使用：** 调用 `setTextCursor(...)` 修改 `textCursor`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QTextCursor textCursor() const`

**作用与语义：**

该属性表示可编辑文本项中的可见文本光标。
默认情况下，如果项目文本未被设置，该属性包含一个空文本光标;否则，它包含放置在项目文档开头的文本光标。

**如何使用：** 调用 `textCursor()` 读取当前值；它不会修改应用状态。

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

`QGraphicsTextItem` 所属机制类型：图形场景与项目机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
