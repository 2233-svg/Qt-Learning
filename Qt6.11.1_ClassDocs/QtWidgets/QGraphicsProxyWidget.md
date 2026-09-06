# QGraphicsProxyWidget

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QGraphicsProxyWidget` 是 图形场景与项目机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QGraphicsProxyWidget` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QGraphicsProxyWidget>`
- 继承自：QGraphicsWidget
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

### 公有函数

- `QGraphicsProxyWidget(QGraphicsItem *parent = nullptr, Qt::WindowFlags wFlags = Qt::WindowFlags())`
- `virtual ~QGraphicsProxyWidget()`
- `QGraphicsProxyWidget * createProxyForChildWidget(QWidget *child)`
- `void setWidget(QWidget *widget)`
- `QRectF subWidgetRect(const QWidget *widget) const`
- `QWidget * widget() const`

### 重实现的公有函数

- `virtual void paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget) override`
- `virtual void setGeometry(const QRectF &rect) override`
- `virtual int type() const override`

### 重实现的保护函数

- `virtual void contextMenuEvent(QGraphicsSceneContextMenuEvent *event) override`
- `virtual void dragEnterEvent(QGraphicsSceneDragDropEvent *event) override`
- `virtual void dragLeaveEvent(QGraphicsSceneDragDropEvent *event) override`
- `virtual void dragMoveEvent(QGraphicsSceneDragDropEvent *event) override`
- `virtual void dropEvent(QGraphicsSceneDragDropEvent *event) override`
- `virtual bool event(QEvent *event) override`
- `virtual bool eventFilter(QObject *object, QEvent *event) override`
- `virtual void focusInEvent(QFocusEvent *event) override`
- `virtual bool focusNextPrevChild(bool next) override`
- `virtual void focusOutEvent(QFocusEvent *event) override`
- `virtual void grabMouseEvent(QEvent *event) override`
- `virtual void hideEvent(QHideEvent *event) override`
- `virtual void hoverEnterEvent(QGraphicsSceneHoverEvent *event) override`
- `virtual void hoverLeaveEvent(QGraphicsSceneHoverEvent *event) override`
- `virtual void hoverMoveEvent(QGraphicsSceneHoverEvent *event) override`
- `virtual void inputMethodEvent(QInputMethodEvent *event) override`
- `virtual QVariant inputMethodQuery(Qt::InputMethodQuery query) const override`
- `virtual QVariant itemChange(QGraphicsItem::GraphicsItemChange change, const QVariant &value) override`
- `virtual void keyPressEvent(QKeyEvent *event) override`
- `virtual void keyReleaseEvent(QKeyEvent *event) override`
- `virtual void mouseDoubleClickEvent(QGraphicsSceneMouseEvent *event) override`
- `virtual void mouseMoveEvent(QGraphicsSceneMouseEvent *event) override`
- `virtual void mousePressEvent(QGraphicsSceneMouseEvent *event) override`
- `virtual void mouseReleaseEvent(QGraphicsSceneMouseEvent *event) override`
- `virtual void resizeEvent(QGraphicsSceneResizeEvent *event) override`
- `virtual void showEvent(QShowEvent *event) override`
- `virtual QSizeF sizeHint(Qt::SizeHint which, const QSizeF &constraint = QSizeF()) const override`
- `virtual void ungrabMouseEvent(QEvent *event) override`
- `virtual void wheelEvent(QGraphicsSceneWheelEvent *event) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[anonymous] enum`

**作用与语义：**

虚拟 `type()` 函数返回的值。
- `QGraphicsProxyWidget::Type`: `12`；一个图形代理控件

### `QGraphicsProxyWidget::QGraphicsProxyWidget(QGraphicsItem *parent = nullptr, Qt::WindowFlags wFlags = Qt::WindowFlags())`

**作用与语义：**

构建一个新的 QGraphicsProxy 控件。`parent` 和 `wFlags` 传递给 `QGraphicsItem` 的构造器。

### `[virtual noexcept] QGraphicsProxyWidget::~QGraphicsProxyWidget()`

**作用与语义：**

它会销毁代理小部件和任何嵌入的小部件。

### `[override virtual protected] void QGraphicsProxyWidget::contextMenuEvent(QGraphicsSceneContextMenuEvent *event)`

**作用与语义：**

重实现自：`QGraphicsItem::contextMenuEvent`（QGraphicsSceneContextMenuEvent *event）。
该事件处理程序可以被重新实现为子类以处理上下文菜单事件。`event`参数包含待处理事件的详细信息。
如果你忽略该事件（即调用`QEvent::ignore()`），`event`会传播到该事件下方的任何项目。如果没有项目接受该事件，场景会忽略它并传播到视图。
收到上下文菜单事件后，通常会打开`QMenu`。示例：
默认实现会忽略该事件。

### `QGraphicsProxyWidget *QGraphicsProxyWidget::createProxyForChildWidget(QWidget *child)`

**作用与语义：**

为该代理中包含的该控件的指定 `child`创建代理小部件。
该函数使得非顶级控件能够获得代理。例如，你可以嵌入一个对话框，然后只转换其中一个控件。
如果小部件已经嵌入，返回现有的代理小部件。

### `[override virtual protected] void QGraphicsProxyWidget::dragEnterEvent(QGraphicsSceneDragDropEvent *event)`

**作用与语义：**

重实现自：`QGraphicsItem::dragEnterEvent`（QGraphicsSceneDragDropEvent *event）。
该事件处理程序对于事件`event`，可以重新实现以接收该项目的拖入事件。拖入事件是在光标进入该物品区域时生成的。
通过接受事件（即调用`QEvent::accept()`），物品将接受掉落事件，同时接收拖动移动和拖离事件。否则，事件将被忽略并传播到下面的物品。如果事件被接受，物品将接收拖动移动事件，然后控制权返回事件循环。
dragEnterEvent 的一个常见实现会根据 `event` 中关联的 mime 数据接受或忽略`event`。示例：
物品默认不会接收拖放事件;要启用此功能，请调用`setAcceptDrops(true)`。
默认实现什么都不做。

### `[override virtual protected] void QGraphicsProxyWidget::dragLeaveEvent(QGraphicsSceneDragDropEvent *event)`

**作用与语义：**

重实现自：`QGraphicsItem::dragLeaveEvent`（QGraphicsSceneDragDropEvent *event）。
该事件处理程序（事件`event`）可以重新实现，以接收该物品的拖曳离开事件。拖曳离开事件是在光标离开物品区域时生成的。大多数情况下你不需要重新实现这个函数，但它对重置物品状态（例如高亮）非常有用。
`event`打电话给`QEvent::ignore()`或`QEvent::accept()`没有任何影响。
项目默认不会接收拖放事件;要启用此功能，请调用`setAcceptDrops(true)`。
默认实现什么都不做。

### `[override virtual protected] void QGraphicsProxyWidget::dragMoveEvent(QGraphicsSceneDragDropEvent *event)`

**作用与语义：**

重实现自：`QGraphicsItem::dragMoveEvent`（QGraphicsSceneDragDropEvent *event）。
对于事件`event`，这个事件处理程序可以重新实现，以接收该物品的拖动移动事件。拖动移动事件是在光标在物品区域内移动时生成的。大多数情况下你不需要重新实现这个函数;它用来表示只有物品的部分可以接受掉落。
在`event`上调用`QEvent::ignore()`或`QEvent::accept()`，可以切换该物品是否接受该事件位置的掉落。默认情况下，`event`被接受，表示该物品允许在指定位置掉落。
物品默认不会接收拖放事件;要启用此功能，请调用`setAcceptDrops(true)`。
默认实现什么都不做。

### `[override virtual protected] void QGraphicsProxyWidget::dropEvent(QGraphicsSceneDragDropEvent *event)`

**作用与语义：**

重实现自：`QGraphicsItem::dropEvent`（QGraphicsSceneDragDropEvent *event）。
该事件处理程序用于事件`event`，可以重新实现以接收该物品的掉落事件。只有当最后一次拖动移动事件被接受时，物品才能接收掉落事件。
打电话给`QEvent::ignore()`或`QEvent::accept()` `event`没有效果。
物品默认不会接收拖放事件;要启用此功能，请调用`setAcceptDrops(true)`。
默认实现什么都不做。

### `[override virtual protected] bool QGraphicsProxyWidget::event(QEvent *event)`

**作用与语义：**

重实现自：`QGraphicsWidget::event`（QEvent *事件）。

### `[override virtual protected] bool QGraphicsProxyWidget::eventFilter(QObject *object, QEvent *event)`

**作用与语义：**

重装：`QObject::eventFilter`（QObject *已观看，QEvent *事件）。

### `[override virtual protected] void QGraphicsProxyWidget::focusInEvent(QFocusEvent *event)`

**作用与语义：**

重实现自：`QGraphicsWidget::focusInEvent`（QFocusEvent *event）。

### `[override virtual protected] bool QGraphicsProxyWidget::focusNextPrevChild(bool next)`

**作用与语义：**

重实现自：`QGraphicsWidget::focusNextPrevChild`（下一个布尔）。
根据 Tab 和 Shift Tab 的需要，找到新的控件以赋予键盘焦点，若能找到新控件则返回 `true`;否则返回`false`。如果 `next` 为真，该函数向前搜索;如果 `next` 为假，则向后搜索。
有时，你会想重新实现这个函数，为你的小部件及其子小部件提供特殊的焦点处理。例如，浏览器可能会重新实现它，将当前活跃链接向前或向后移动，只有在到达页面最后或第一个链接时调用基础实现。
子控件在其父控件上调用 focusNextPrevChild()，但只有包含子控件的窗口决定将焦点重定向到哪里。通过为对象重新实现该函数，你可以控制所有子控件的焦点遍历。

### `[override virtual protected] void QGraphicsProxyWidget::focusOutEvent(QFocusEvent *event)`

**作用与语义：**

重实现自：`QGraphicsWidget::focusOutEvent`（QFocusEvent *event）。

### `[override virtual protected] void QGraphicsProxyWidget::grabMouseEvent(QEvent *event)`

**作用与语义：**

重实现自：`QGraphicsWidget::grabMouseEvent`（QEvent *事件）。
`event`，这个事件处理程序可以在子类中重新实现，以接收 `QEvent::GrabMouse` 事件的通知。

### `[override virtual protected] void QGraphicsProxyWidget::hideEvent(QHideEvent *event)`

**作用与语义：**

重实现自：`QGraphicsWidget::hideEvent`（QHideEvent *event）。
对于`Hide`事件，该事件处理程序是在小部件被隐藏后交付的，例如，在小部件之前显示时，已调用该小部件或其前祖之一的 setVisible（false）。
你可以重新实现这个事件处理程序，检测你的小部件是否被隐藏。调用`QEvent::accept()`或`QEvent::ignore()`对`event`没有影响。

### `[override virtual protected] void QGraphicsProxyWidget::hoverEnterEvent(QGraphicsSceneHoverEvent *event)`

**作用与语义：**

重实现自：`QGraphicsItem::hoverEnterEvent`（QGraphicsSceneHoverEvent *event）。
该事件处理程序对于事件`event`，可以重新实现以接收该项的悬停进入事件。默认实现调用`update()`;否则不做任何操作。
打电话给`QEvent::ignore()`或`QEvent::accept()`对`event`没有影响。

### `[override virtual protected] void QGraphicsProxyWidget::hoverLeaveEvent(QGraphicsSceneHoverEvent *event)`

**作用与语义：**

重实现自：`QGraphicsWidget::hoverLeaveEvent`（QGraphicsSceneHoverEvent *event）。

### `[override virtual protected] void QGraphicsProxyWidget::hoverMoveEvent(QGraphicsSceneHoverEvent *event)`

**作用与语义：**

重实现自：`QGraphicsWidget::hoverMoveEvent`（QGraphicsSceneHoverEvent *event）。

### `[override virtual protected] void QGraphicsProxyWidget::inputMethodEvent(QInputMethodEvent *event)`

**作用与语义：**

Reimplements： `QGraphicsItem::inputMethodEvent`（QInputMethodEvent *event）.
该事件处理程序对于事件`event`，可以重新实现以接收该项的输入法事件。默认实现忽略该事件。

### `[override virtual protected] QVariant QGraphicsProxyWidget::inputMethodQuery(Qt::InputMethodQuery query) const`

**作用与语义：**

重实现自：`QGraphicsItem::inputMethodQuery`（Qt：：InputMethodQuery query） const.
该方法仅对输入项相关。输入方法用它来查询项的一组属性，以支持复杂的输入法操作，如支持周围文本和重新转换。`query` 指定查询的属性。

### `[override virtual protected] QVariant QGraphicsProxyWidget::itemChange(QGraphicsItem::GraphicsItemChange change, const QVariant &value)`

**作用与语义：**

重实现自：`QGraphicsWidget::itemChange`（QGraphicsItem：：GraphicsItemChange change， const QVariant & value）。

### `[override virtual protected] void QGraphicsProxyWidget::keyPressEvent(QKeyEvent *event)`

**作用与语义：**

重实现自：`QGraphicsItem::keyPressEvent`（QKeyEvent *event）。
该事件处理程序（针对事件`event`）可以重新实现以接收该项的按键事件。默认实现忽略该事件。如果你重新实现该处理程序，事件默认会被接受。
注意，键事件只会针对设置`ItemIsFocusable`标志且具有键盘输入焦点的物品。

### `[override virtual protected] void QGraphicsProxyWidget::keyReleaseEvent(QKeyEvent *event)`

**作用与语义：**

重实现自：`QGraphicsItem::keyReleaseEvent`（QKeyEvent *event）。
该事件处理程序（针对事件`event`）可以重新实现以接收该项的密钥释放事件。默认实现忽略该事件。如果你重新实现该处理程序，该事件默认会被接受。
注意，键事件只会针对设置`ItemIsFocusable`标志且带有键盘输入焦点的物品。

### `[override virtual protected] void QGraphicsProxyWidget::mouseDoubleClickEvent(QGraphicsSceneMouseEvent *event)`

**作用与语义：**

重实现自：`QGraphicsItem::mouseDoubleClickEvent`（QGraphicsSceneMouseEvent *event）。
该事件处理程序对于事件`event`，可以重新实现以接收该项的鼠标双击事件。
双击物品时，该物品首先会触发鼠标按键事件，接着是释放事件（即点击），再是双击事件，最后是释放事件。
打电话给`QEvent::ignore()`或`QEvent::accept()`打`event`没有效果。
默认实现调用`mousePressEvent()`。如果你想在重新实现这个函数时保留基础实现，可以在你的重实现中调用 QGraphicsItem：：mouseDoubleClickEvent()。
注意，如果物品既非`selectable`也非`movable`，则不会触发双击事件（此时忽略单次鼠标点击，导致双击停止生成）。

### `[override virtual protected] void QGraphicsProxyWidget::mouseMoveEvent(QGraphicsSceneMouseEvent *event)`

**作用与语义：**

重实现自：`QGraphicsItem::mouseMoveEvent`（QGraphicsSceneMouseEvent *event）。
该事件处理程序（事件`event`）可以重新实现，以接收该物品的鼠标移动事件。如果你收到该事件，可以确定该物品也收到了鼠标按键事件，并且该物品是当前的鼠标抓取器。
`event`打电话给`QEvent::ignore()`或`QEvent::accept()`没有任何影响。
默认实现处理基本的项目交互，比如选择和移动。如果你想在重现这个函数时保留基础实现，可以在你的重实现中调用 QGraphicsItem：：mouseMoveEvent()。
请注意，`mousePressEvent()`决定接收鼠标事件的图形项目。详情请参见`mousePressEvent()`描述。

### `[override virtual protected] void QGraphicsProxyWidget::mousePressEvent(QGraphicsSceneMouseEvent *event)`

**作用与语义：**

重实现自：`QGraphicsItem::mousePressEvent`（QGraphicsSceneMouseEvent *event）。
该事件处理程序对于事件`event`，可以重新实现以接收该物品的鼠标按键事件。鼠标按键事件只传递给接受被按下鼠标按钮的物品。默认情况下，物品接受所有鼠标按键，但你可以通过调用`setAcceptedMouseButtons()`来更改。
鼠标按键事件决定哪个物品应成为鼠标抓取器（参见`QGraphicsScene::mouseGrabberItem()`）。如果不重新实现此功能，按键事件将传播到该物品下方的最顶端任何物品，且不会有其他鼠标事件传递到该物品。
如果你重新实现了这个功能，`event`默认会被接受（见`QEvent::accept()`），这个物品就是鼠标抓取器。这允许该物品接收未来的移动、释放和双击事件。如果你在`event`上调用`QEvent::ignore()`，这个物品将失去鼠标抓取功能，`event`会传播到最下面的任何物品。除非收到新的鼠标按键事件，否则不会再传递给该物品。
默认实现处理基本的物品交互，比如选择和移动。如果你想在重现这个函数时保留基础实现，可以在重构中调用 QGraphicsItem：：mousePressEvent()。
对于既非`movable`也非`selectable`的项目，事件为`QEvent::ignore()`d。

### `[override virtual protected] void QGraphicsProxyWidget::mouseReleaseEvent(QGraphicsSceneMouseEvent *event)`

**作用与语义：**

重实现自：`QGraphicsItem::mouseReleaseEvent`（QGraphicsSceneMouseEvent *event）。
该事件处理程序对于事件`event`，可以重新实现以接收该项的鼠标释放事件。
打电话给`QEvent::ignore()`或`QEvent::accept()` `event`没有效果。
默认实现处理基本的物品操作，比如选择和移动。如果你想在重现这个函数时保留基础实现，可以在重写中调用 QGraphicsItem：：mouseReleaseEvent()。
请注意，`mousePressEvent()`决定接收鼠标事件的图形项目。详情请参见`mousePressEvent()`描述。

### `[protected slot] QGraphicsProxyWidget *QGraphicsProxyWidget::newProxyWidget(const QWidget *child)`

**作用与语义：**

为该代理中包含的该控件的指定 `child`创建代理小部件。
你不应该直接调用这个函数;应该用`QGraphicsProxyWidget::createProxyForChildWidget()`。
这个函数是一个假的虚拟槽，你可以在子类中重新实现它，以控制新代理控件的创建方式。默认实现会返回一个用`QGraphicsProxyWidget()`构造函数创建的代理，该代理控件作为父节点。

### `[override virtual] void QGraphicsProxyWidget::paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget)`

**作用与语义：**

由场景调用，把代理所嵌入的 `QWidget` 及其当前样式绘制到图形视图。`option` 提供选择、变换等状态；通常不直接调用，派生类额外绘制后应保持代理控件的几何和缓存一致。

### `[override virtual protected] void QGraphicsProxyWidget::resizeEvent(QGraphicsSceneResizeEvent *event)`

**作用与语义：**

重实现自：`QGraphicsWidget::resizeEvent`（QGraphicsSceneResizeEvent *event）。
对于`GraphicsSceneResize`事件，该事件处理程序是在控件大小调整后交付的（即其局部大小发生变化）。`event`包含旧大小和新大小。
该事件仅在控件本地调整大小时执行;调用控件或其前祖或视图的 `setTransform()` 不会影响控件的本地大小。
你可以重新实现这个事件处理程序，检测你的小部件是否被调整了大小。调用`QEvent::accept()`或`QEvent::ignore()`对`event`没有影响。

### `[override virtual] void QGraphicsProxyWidget::setGeometry(const QRectF &rect)`

**作用与语义：**

重装：`QGraphicsLayoutItem::setGeometry`（const QRectF & rect）。
该虚拟函数将`QGraphicsLayoutItem`的几何体设置为 `rect`，即父坐标（例如，`rect` 的左上角等价于该物品在父坐标中的位置）。
你必须在`QGraphicsLayoutItem`的子类中重新实现该函数以接收几何更新。布局在进行重排时会调用该函数。
如果`rect`超出`minimumSize`和`maximumSize`的范围，则会调整到最接近的尺寸，使其在法律范围内。

### `void QGraphicsProxyWidget::setWidget(QWidget *widget)`

**作用与语义：**

将`widget`嵌入到该代理控件中。嵌入控件必须仅存在于图形视图内部或外部。只要控件同时在UI的其他地方可见，你就无法嵌入它。
`widget`必须是一个顶层控件，其父组件是`nullptr`。
当小部件被嵌入时，其状态（例如可见、启用、几何、大小提示）会复制到代理小部件中。如果嵌入小部件被显式隐藏或禁用，嵌入完成后代理小部件将显式隐藏或禁用。类文档对共享状态有全面的概述。
`QGraphicsProxyWidget` 的窗口标志决定了嵌入后小部件是否会被赋予窗口装饰。
该函数返回后，`QGraphicsProxyWidget`会尽可能保持与`widget`状态同步。
如果调用该函数时该代理已经嵌入了某个小部件，那么该小部件首先会自动去嵌入。传递`widget`参数的`nullptr`只能卸嵌入小部件，当前嵌入小部件的所有权会传递给调用者。所有嵌入的子小部件也会被嵌入，其代理小部件将被销毁。
请注意，带有`Qt::WA_PaintOnScreen`控件属性集的小部件以及包裹外部应用或控制器的小部件不能被嵌入。例如`QOpenGLWidget`和QAxWidget。

### `[override virtual protected] void QGraphicsProxyWidget::showEvent(QShowEvent *event)`

**作用与语义：**

重实现自：`QGraphicsWidget::showEvent`（QShowEvent *event）。
对于`Show`事件，这个事件处理程序在小部件尚未显示之前交付，例如，在小部件之前被隐藏时，已调用了 setVisible（true） 来调用该小部件或其前祖。
你可以重新实现这个事件处理程序，检测你的小部件何时显示。调用`QEvent::accept()`或`QEvent::ignore()`在`event`上没有效果。

### `[override virtual protected] QSizeF QGraphicsProxyWidget::sizeHint(Qt::SizeHint which, const QSizeF &constraint = QSizeF()) const`

**作用与语义：**

重实现自：`QGraphicsWidget::sizeHint`（Qt：：SizeHint which， const QSizeF & constraint） const.

### `QRectF QGraphicsProxyWidget::subWidgetRect(const QWidget *widget) const`

**作用与语义：**

返回`widget`矩形，矩形必须是`widget()`的后代，或者`widget()`该代理项的本地坐标。
如果没有嵌入小部件、`widget` `nullptr`，或者`widget`不是嵌入小部件的后代，该函数返回空`QRectF`。

### `[override virtual] int QGraphicsProxyWidget::type() const`

**作用与语义：**

重实现自：`QGraphicsWidget::type()` const.

### `[override virtual protected] void QGraphicsProxyWidget::ungrabMouseEvent(QEvent *event)`

**作用与语义：**

重实现自：`QGraphicsWidget::ungrabMouseEvent`（QEvent *事件）。
`event`，这个事件处理程序可以重新实现到子类中，以接收`QEvent::UngrabMouse`事件的通知。

### `[override virtual protected] void QGraphicsProxyWidget::wheelEvent(QGraphicsSceneWheelEvent *event)`

**作用与语义：**

重实现自：`QGraphicsItem::wheelEvent`（QGraphicsSceneWheelEvent *event）。
对于事件`event`，这个事件处理程序可以重新实现，以接收该项的轮子事件。如果你重新实现这个函数，`event`将默认被接受。
如果你忽略该事件（即调用`QEvent::ignore()`），它会传播到该事件下方的任何项目。如果没有项目接受该事件，场景会忽略它，并传播到视图（例如视图的垂直滚动条）。
默认实现会忽略该事件。

### `QWidget *QGraphicsProxyWidget::widget() const`

**作用与语义：**

返回指向嵌入控件的指针。

### `enum { Type }`

**作用与语义：**

虚拟 `type()` 函数返回的值。
- `QGraphicsProxyWidget::Type`: `12`；一个图形代理控件

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

`QGraphicsProxyWidget` 所属机制类型：图形场景与项目机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
