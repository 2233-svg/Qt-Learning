# QGraphicsScene

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QGraphicsScene` 是 图形场景与项目机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QGraphicsScene` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QGraphicsScene>`
- 继承自：QObject
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

- `enum ItemIndexMethod { BspTreeIndex, NoIndex }`
- `enum SceneLayer { ItemLayer, BackgroundLayer, ForegroundLayer, AllLayers }`
- `flags SceneLayers`

### 属性

- `backgroundBrush : QBrush`
- `bspTreeDepth : int`
- `focusOnTouch : bool`
- `font : QFont`
- `foregroundBrush : QBrush`
- `itemIndexMethod : ItemIndexMethod`
- `minimumRenderSize : qreal`
- `palette : QPalette`
- `sceneRect : QRectF`
- `stickyFocus : bool`

### 公有函数

- `QGraphicsScene(QObject *parent = nullptr)`
- `QGraphicsScene(const QRectF &sceneRect, QObject *parent = nullptr)`
- `QGraphicsScene(qreal x, qreal y, qreal width, qreal height, QObject *parent = nullptr)`
- `virtual ~QGraphicsScene()`
- `QGraphicsItem * activePanel() const`
- `QGraphicsWidget * activeWindow() const`
- `QGraphicsEllipseItem * addEllipse(const QRectF &rect, const QPen &pen = QPen(), const QBrush &brush = QBrush())`
- `QGraphicsEllipseItem * addEllipse(qreal x, qreal y, qreal w, qreal h, const QPen &pen = QPen(), const QBrush &brush = QBrush())`
- `void addItem(QGraphicsItem *item)`
- `QGraphicsLineItem * addLine(const QLineF &line, const QPen &pen = QPen())`
- `QGraphicsLineItem * addLine(qreal x1, qreal y1, qreal x2, qreal y2, const QPen &pen = QPen())`
- `QGraphicsPathItem * addPath(const QPainterPath &path, const QPen &pen = QPen(), const QBrush &brush = QBrush())`
- `QGraphicsPixmapItem * addPixmap(const QPixmap &pixmap)`
- `QGraphicsPolygonItem * addPolygon(const QPolygonF &polygon, const QPen &pen = QPen(), const QBrush &brush = QBrush())`
- `QGraphicsRectItem * addRect(const QRectF &rect, const QPen &pen = QPen(), const QBrush &brush = QBrush())`
- `QGraphicsRectItem * addRect(qreal x, qreal y, qreal w, qreal h, const QPen &pen = QPen(), const QBrush &brush = QBrush())`
- `QGraphicsSimpleTextItem * addSimpleText(const QString &text, const QFont &font = QFont())`
- `QGraphicsTextItem * addText(const QString &text, const QFont &font = QFont())`
- `QGraphicsProxyWidget * addWidget(QWidget *widget, Qt::WindowFlags wFlags = Qt::WindowFlags())`
- `QBrush backgroundBrush() const`
- `int bspTreeDepth() const`
- `void clearFocus()`
- `QList<QGraphicsItem *> collidingItems(const QGraphicsItem *item, Qt::ItemSelectionMode mode = Qt::IntersectsItemShape) const`
- `QGraphicsItemGroup * createItemGroup(const QList<QGraphicsItem *> &items)`
- `void destroyItemGroup(QGraphicsItemGroup *group)`
- `QGraphicsItem * focusItem() const`
- `bool focusOnTouch() const`
- `QFont font() const`
- `QBrush foregroundBrush() const`
- `bool hasFocus() const`
- `qreal height() const`
- `virtual QVariant inputMethodQuery(Qt::InputMethodQuery query) const`
- `void invalidate(qreal x, qreal y, qreal w, qreal h, QGraphicsScene::SceneLayers layers = AllLayers)`
- `bool isActive() const`
- `QGraphicsItem * itemAt(const QPointF &position, const QTransform &deviceTransform) const`
- `QGraphicsItem * itemAt(qreal x, qreal y, const QTransform &deviceTransform) const`
- `QGraphicsScene::ItemIndexMethod itemIndexMethod() const`
- `QList<QGraphicsItem *> items(Qt::SortOrder order = Qt::DescendingOrder) const`
- `QList<QGraphicsItem *> items(const QPointF &pos, Qt::ItemSelectionMode mode = Qt::IntersectsItemShape, Qt::SortOrder order = Qt::DescendingOrder, const QTransform &deviceTransform = QTransform()) const`
- `QList<QGraphicsItem *> items(const QPainterPath &path, Qt::ItemSelectionMode mode = Qt::IntersectsItemShape, Qt::SortOrder order = Qt::DescendingOrder, const QTransform &deviceTransform = QTransform()) const`
- `QList<QGraphicsItem *> items(const QPolygonF &polygon, Qt::ItemSelectionMode mode = Qt::IntersectsItemShape, Qt::SortOrder order = Qt::DescendingOrder, const QTransform &deviceTransform = QTransform()) const`
- `QList<QGraphicsItem *> items(const QRectF &rect, Qt::ItemSelectionMode mode = Qt::IntersectsItemShape, Qt::SortOrder order = Qt::DescendingOrder, const QTransform &deviceTransform = QTransform()) const`
- `QList<QGraphicsItem *> items(qreal x, qreal y, qreal w, qreal h, Qt::ItemSelectionMode mode, Qt::SortOrder order, const QTransform &deviceTransform = QTransform()) const`
- `QRectF itemsBoundingRect() const`
- `qreal minimumRenderSize() const`
- `QGraphicsItem * mouseGrabberItem() const`
- `QPalette palette() const`
- `void removeItem(QGraphicsItem *item)`
- `void render(QPainter *painter, const QRectF &target = QRectF(), const QRectF &source = QRectF(), Qt::AspectRatioMode aspectRatioMode = Qt::KeepAspectRatio)`
- `QRectF sceneRect() const`
- `QList<QGraphicsItem *> selectedItems() const`
- `QPainterPath selectionArea() const`
- `bool sendEvent(QGraphicsItem *item, QEvent *event)`
- `void setActivePanel(QGraphicsItem *item)`
- `void setActiveWindow(QGraphicsWidget *widget)`
- `void setBackgroundBrush(const QBrush &brush)`
- `void setBspTreeDepth(int depth)`
- `void setFocus(Qt::FocusReason focusReason = Qt::OtherFocusReason)`
- `void setFocusItem(QGraphicsItem *item, Qt::FocusReason focusReason = Qt::OtherFocusReason)`
- `void setFocusOnTouch(bool enabled)`
- `void setFont(const QFont &font)`
- `void setForegroundBrush(const QBrush &brush)`
- `void setItemIndexMethod(QGraphicsScene::ItemIndexMethod method)`
- `void setMinimumRenderSize(qreal minSize)`
- `void setPalette(const QPalette &palette)`
- `void setSceneRect(const QRectF &rect)`
- `void setSceneRect(qreal x, qreal y, qreal w, qreal h)`
- `void setSelectionArea(const QPainterPath &path, const QTransform &deviceTransform)`
- `void setSelectionArea(const QPainterPath &path, Qt::ItemSelectionOperation selectionOperation = Qt::ReplaceSelection, Qt::ItemSelectionMode mode = Qt::IntersectsItemShape, const QTransform &deviceTransform = QTransform())`
- `void setStickyFocus(bool enabled)`
- `void setStyle(QStyle *style)`
- `bool stickyFocus() const`
- `QStyle * style() const`
- `void update(qreal x, qreal y, qreal w, qreal h)`
- `QList<QGraphicsView *> views() const`
- `qreal width() const`

### 公有槽函数

- `void advance()`
- `void clear()`
- `void clearSelection()`
- `void invalidate(const QRectF &rect = QRectF(), QGraphicsScene::SceneLayers layers = AllLayers)`
- `void update(const QRectF &rect = QRectF())`

### 信号

- `void changed(const QList<QRectF> &region)`
- `void focusItemChanged(QGraphicsItem *newFocusItem, QGraphicsItem *oldFocusItem, Qt::FocusReason reason)`
- `void sceneRectChanged(const QRectF &rect)`
- `void selectionChanged()`

### 保护函数

- `virtual void contextMenuEvent(QGraphicsSceneContextMenuEvent *contextMenuEvent)`
- `virtual void dragEnterEvent(QGraphicsSceneDragDropEvent *event)`
- `virtual void dragLeaveEvent(QGraphicsSceneDragDropEvent *event)`
- `virtual void dragMoveEvent(QGraphicsSceneDragDropEvent *event)`
- `virtual void drawBackground(QPainter *painter, const QRectF &rect)`
- `virtual void drawForeground(QPainter *painter, const QRectF &rect)`
- `virtual void dropEvent(QGraphicsSceneDragDropEvent *event)`
- `virtual void focusInEvent(QFocusEvent *focusEvent)`
- `virtual void focusOutEvent(QFocusEvent *focusEvent)`
- `virtual void helpEvent(QGraphicsSceneHelpEvent *helpEvent)`
- `virtual void inputMethodEvent(QInputMethodEvent *event)`
- `virtual void keyPressEvent(QKeyEvent *keyEvent)`
- `virtual void keyReleaseEvent(QKeyEvent *keyEvent)`
- `virtual void mouseDoubleClickEvent(QGraphicsSceneMouseEvent *mouseEvent)`
- `virtual void mouseMoveEvent(QGraphicsSceneMouseEvent *mouseEvent)`
- `virtual void mousePressEvent(QGraphicsSceneMouseEvent *mouseEvent)`
- `virtual void mouseReleaseEvent(QGraphicsSceneMouseEvent *mouseEvent)`
- `virtual void wheelEvent(QGraphicsSceneWheelEvent *wheelEvent)`

### 重实现的保护函数

- `virtual bool event(QEvent *event) override`
- `virtual bool eventFilter(QObject *watched, QEvent *event) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QGraphicsScene::ItemIndexMethod`

**作用与语义：**

本枚举描述了索引算法`QGraphicsScene`用于管理场景中物品的位置信息。
- `QGraphicsScene::BspTreeIndex`：`0`;应用了二元空间划分树。所有`QGraphicsScene`的物品定位算法通过二分搜索，复杂度接近对数级。添加、移动和移除物品是对数级的。这种方法最适合静态场景（即大多数物品不移动的场景）。
- `QGraphicsScene::NoIndex`：`-1`;不应用索引。物品位置具有线性复杂度，因为场景中的所有物品都会被搜索。然而，添加、移动和移除物品则是恒定时间完成的。这种方法非常适合动态场景，因为许多物品会连续添加、移动或移除。

### `enum QGraphicsScene::SceneLayerflags QGraphicsScene::SceneLayers`

**作用与语义：**

这个枚举描述了`QGraphicsScene`中的渲染层。当`QGraphicsScene`绘制场景内容时，会按顺序分别渲染每一层。
每层代表一个标志，在调用 `invalidate()` 或 `QGraphicsView::invalidateScene()` 等函数时可以合并进行 OR 映射。
- `QGraphicsScene::ItemLayer`：`0x1`;物品图层。`QGraphicsScene`通过调用虚拟函数 drawItems() 来渲染所有位于该图层中的物品。物品图层绘制在背景图层之后，但前景图层之前。
- `QGraphicsScene::BackgroundLayer`：`0x2`;背景图层。`QGraphicsScene` 通过调用虚拟函数 `drawBackground()` 来渲染该图层的场景背景。背景图层是所有图层中第一个绘制的。
- `QGraphicsScene::ForegroundLayer`：`0x4`;前景图层。`QGraphicsScene` 通过调用虚拟函数 `drawForeground()` 来渲染该图层的场景前景。前景图层是所有图层中最后绘制的。
- `QGraphicsScene::AllLayers`：`0xffff`;所有层;该值代表三层的组合。
SceneLayers 类型是 QFlags 的 typedef<SceneLayer>。它存储 SceneLayer 值的 OR 组合。

### `backgroundBrush : QBrush`

**作用与语义：**

该属性保留场景的背景画笔。
将此属性设置为将场景背景更换为不同的颜色、渐变或纹理。默认的背景刷是`Qt::NoBrush`。背景是在物品之前（后方）绘制的。
`QGraphicsScene::render()`调用`drawBackground()`来绘制场景背景。为了更详细地控制背景绘制方式，可以在`QGraphicsScene`子类中重新实现`drawBackground()`。

**如何使用：** 调用 `backgroundBrush()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 QGraphicsScene scene;
 QGraphicsView view(&scene);
 view.show();

 // a blue background
 scene.setBackgroundBrush(Qt::blue);

 // a gradient background
 QRadialGradient gradient(0, 0, 10);
 gradient.setSpread(QGradient::RepeatSpread);
 scene.setBackgroundBrush(gradient);
```

### `bspTreeDepth : int`

**作用与语义：**

此属性保存 `QGraphicsScene` 的 BSP 索引树的深度。
当使用 `NoIndex` 时，此属性无效。
该值决定 `QGraphicsScene` 的 BSP 树深度。树深度直接影响 `QGraphicsScene` 的性能和内存使用；内存使用随着树的深度呈指数增加。树深度优化后，`QGraphicsScene` 可以瞬间确定项目的局部性，即使场景中有成千上万或数百万的项目，也会大大提高渲染性能。
默认值为 0，此时 Qt 将根据场景中项目的大小、位置和数量自动推测合理的默认深度。然而，如果这些参数频繁变化，`QGraphicsScene` 在内部重新调整深度时，可能会导致性能下降。通过设置此属性固定树深度可以避免潜在的性能下降。
树的深度和场景矩形的大小决定场景分割的颗粒度。每个场景段的大小由以下算法决定：
当每个段包含 0 到 10 个项目时，BSP 树大小为最优。

**如何使用：** 调用 `bspTreeDepth()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 QSizeF segmentSize = sceneRect().size() / pow(2, depth - 1);
```

### `focusOnTouch : bool`

**作用与语义：**

该特性决定物品在获得触控启动事件时是否获得焦点。
通常的行为是只有在点击某个项目时才转移焦点。操作系统通常将触摸板上的轻触等同于鼠标点击，生成合成点击事件作为响应。不过，至少在macOS上你可以配置这种行为。
默认情况下，`QGraphicsScene`在触控板等触控板上操作时也会转移焦点。如果操作系统配置为点击触控板时不生成合成鼠标点击，这就令人惊讶了。如果操作系统在点击触控板时会产生合成鼠标点击，启动触控手势时的焦点转移就没必要了。
关闭 focusOnTouch 后，`QGraphicsScene` 的表现与 macOS 上正常。
默认值为`true`，确保默认行为与5.12之前的Qt版本相同。设置为`false`以防止触摸事件触发焦点变化。

**如何使用：** 调用 `focusOnTouch()` 读取当前值；它不会修改应用状态。

### `font : QFont`

**作用与语义：**

该属性保留场景的默认字体。
该属性提供场景的字体。场景字体默认为 ，并解析所有来自 的条目 `QApplication::font`。
如果场景的字体发生变化，无论是直接通过 setFont() 还是在应用程序字体变化时间接发生，`QGraphicsScene` 首先向自己发送一个 `FontChange` 事件，然后向场景中所有顶层控件发送`FontChange`事件。这些元素通过向场景解析自己的字体来响应，然后通知其子节点，子节点再次通知子节点，如此循环，直到所有控件元素都更新了字体。
更改场景字体（无论是直接还是间接通过`QApplication::setFont()`）会自动安排整个场景的重新绘制。

**如何使用：** 调用 `font()` 读取当前值；它不会修改应用状态。

### `foregroundBrush : QBrush`

**作用与语义：**

该属性保留了场景的前景画笔。
更改此属性，将场景前景设置为不同的颜色、渐变或纹理。
前景是在物品之后（上方）绘制的。默认的前景画笔是`Qt::NoBrush`（即不绘制前景）。
`QGraphicsScene::render()`调用`drawForeground()`来绘制场景前景。如果想更详细地控制前景绘制方式，可以在`QGraphicsScene`子类中重新实现`drawForeground()`函数。

**如何使用：** 调用 `foregroundBrush()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 QGraphicsScene scene;
 QGraphicsView view(&scene);
 view.show();

 // a white semi-transparent foreground
 scene.setForegroundBrush(QColor(255, 255, 255, 127));

 // a grid foreground
 scene.setForegroundBrush(QBrush(Qt::lightGray, Qt::CrossPattern));
```

### `itemIndexMethod : ItemIndexMethod`

**作用与语义：**

该属性包含了项目索引方法。
`QGraphicsScene` 对场景应用索引算法，以加快`items()`和`itemAt()`等物品发现功能。索引在静态场景（即物品不移动）时最为高效。对于动态场景或包含大量动画元素的场景，索引簿记可能超过快速查找速度。
对于常见情况，默认的索引方法`BspTreeIndex`正常工作。如果你的场景使用了很多动画且出现缓慢，可以通过调用`setItemIndexMethod(NoIndex)`来禁用索引。

**如何使用：** 调用 `itemIndexMethod()` 读取当前值；它不会修改应用状态。

### `minimumRenderSize : qreal`

**作用与语义：**

该属性表示了物品必须绘制的最小视图变换尺寸。
当场景被渲染时，任何宽度或高度变换到目标视图后小于 minimumRenderSize() 的物品都不会被渲染。如果某个物品未被渲染且裁剪了其子对象，它们也不会被渲染。设置该值以加快在缩放视图下渲染多物体场景的渲染速度。
默认值是0。如果未设置，或者设置为0或负值，所有项目都会被渲染。
例如，设置该属性在场景由多个视图渲染时尤其有用，其中一个视图作为总览，始终显示所有物品。在拥有多物品的场景中，这种视图会使用较高的缩放因子，以便显示所有物品。由于缩放，较小的物体对最终渲染场景的贡献微乎其微。为了避免绘制这些元素并缩短渲染场景所需时间，你可以调用 setMinimumRenderSize() 并设置非负值。
注意：由于太小未绘制的物品仍会通过`items()`和`itemAt()`等方法返回，并参与碰撞检测和交互。建议将 minimumRenderSize() 设置为小于或等于 1，以避免大型未渲染的可交互物品。

**如何使用：** 调用 `minimumRenderSize()` 读取当前值；它不会修改应用状态。

### `palette : QPalette`

**作用与语义：**

该属性保留了场景的默认调色板。
该属性提供场景调色板。场景调色板默认使用并解析所有元素，`QApplication::palette`。
如果场景调色板发生变化，无论是直接通过 setPalette() 还是在应用调色板变更时间接发生，`QGraphicsScene` 首先向自己发送一个 `PaletteChange` 事件，然后向场景中所有顶层控件发送`PaletteChange`事件。这些控件通过向场景解析自己的调色板来响应，然后通知其子节点，子节点再通知子节点，如此循环，直到所有控件项目更新了调色板。
通过`QApplication::setPalette()`直接或间接更改场景调色板，会自动安排整个场景的重新绘制。

**如何使用：** 调用 `palette()` 读取当前值；它不会修改应用状态。

### `sceneRect : QRectF`

**作用与语义：**

该属性表示场景矩形;场景的边界矩形。
场景矩形定义了场景的范围。它主要用于`QGraphicsView`确定视图默认可滚动区域，`QGraphicsScene`则用于管理物品索引。
如果未设置，或者设置为空`QRectF`，sceneRect() 将返回自场景创建以来场景中所有物品中最大的边界矩形（即当场景中添加或移动物品时会增长但不会缩小的矩形）。

**如何使用：** 调用 `sceneRect()` 读取当前值；它不会修改应用状态。

### `stickyFocus : bool`

**作用与语义：**

该属性适用于点击场景背景时是否清除焦点。
在 stickyFocus 设置为 true 的 `QGraphicsScene` 中，当用户点击场景背景或不接受焦点的项目时，焦点保持不变。否则，焦点将被清除。
默认情况下，该属性为 `false`。
焦点会响应鼠标按下事件变化。可以在 `QGraphicsScene` 的子类中重新实现 `mousePressEvent()`，以根据用户点击位置切换此属性。

**如何使用：** 调用 `stickyFocus()` 读取当前值；它不会修改应用状态。

### `QGraphicsScene::QGraphicsScene(QObject *parent = nullptr)`

**作用与语义：**

构造一个QGraphicsScene对象。`parent`参数传递给`QObject`的构造器。

### `QGraphicsScene::QGraphicsScene(const QRectF &sceneRect, QObject *parent = nullptr)`

**作用与语义：**

构造一个QGraphicsScene对象，使用`sceneRect`作为其场景矩形。`parent`参数传递给`QObject`的构造函数。

### `QGraphicsScene::QGraphicsScene(qreal x, qreal y, qreal width, qreal height, QObject *parent = nullptr)`

**作用与语义：**

构造一个QGraphicsScene对象，使用由（`x`， `y`）指定的矩形，以及其场景矩形的`width`和`height`。`parent`参数传递给`QObject`的构造函数。

### `[virtual noexcept] QGraphicsScene::~QGraphicsScene()`

**作用与语义：**

在销毁场景对象之前，移除并删除场景对象中的所有物品。场景对象从应用程序的全局场景列表中移除，并从所有关联的视图中移除。

### `QGraphicsItem *QGraphicsScene::activePanel() const`

**作用与语义：**

返回当前活跃的面板，或者如果没有当前面板激活，则返回`nullptr`。

### `QGraphicsWidget *QGraphicsScene::activeWindow() const`

**作用与语义：**

返回当前活跃窗口，若无窗口则返回`nullptr`。

### `QGraphicsEllipseItem *QGraphicsScene::addEllipse(const QRectF &rect, const QPen &pen = QPen(), const QBrush &brush = QBrush())`

**作用与语义：**

创建并添加一个椭圆元素到场景，返回元素指针。椭圆的几何体由`rect`定义，其笔和画笔初始化为`pen`和`brush`。
注意，该物品的几何形状以项目坐标表示，其位置初始化为 （0， 0）。
如果该物品可见（即`QGraphicsItem::isVisible()`返回`true`），`QGraphicsScene`在控制返回事件循环时会发出`changed()`。

### `QGraphicsEllipseItem *QGraphicsScene::addEllipse(qreal x, qreal y, qreal w, qreal h, const QPen &pen = QPen(), const QBrush &brush = QBrush())`

**作用与语义：**

这个便捷函数等价于调用 addEllipse(`QRectF`(`x`, `y`, `w`, `h`), `pen`, `brush`) 。

### `void QGraphicsScene::addItem(QGraphicsItem *item)`

**作用与语义：**

将`item`及其所有子场景添加或移动到该场景。该场景拥有`item`的所有权。
如果该物品是可见的（即`QGraphicsItem::isVisible()`返回 true），`QGraphicsScene` 在控制返回事件循环时会发出`changed()`。
如果该物品已经在另一个场景中，它会先从原场景中移除，然后作为顶层添加到该场景。
`QGraphicsScene`会在物品被添加到场景时向`item`发送ItemSceneChange通知。如果物品当前不属于某个场景，则只发送一个通知。如果它已经属于场景（即被移动到该场景），`QGraphicsScene`会在物品从上一个场景移除时发送新增通知。
如果物品是面板，场景处于激活状态，且场景中没有激活面板，那么物品就会被激活。

### `QGraphicsLineItem *QGraphicsScene::addLine(const QLineF &line, const QPen &pen = QPen())`

**作用与语义：**

创建并添加一个行项到场景中，返回条目指针。该行的几何体由`line`定义，其笔初始化为`pen`。
注意，该物品的几何形状以项目坐标表示，其位置初始化为 （0， 0）。
如果物品可见（即`QGraphicsItem::isVisible()`返回`true`），`QGraphicsScene`在控制回到事件循环时会发出`changed()`。

### `QGraphicsLineItem *QGraphicsScene::addLine(qreal x1, qreal y1, qreal x2, qreal y2, const QPen &pen = QPen())`

**作用与语义：**

这个便利函数等同于调用 addLine(`QLineF`(`x1`, `y1`, `x2`, `y2`), `pen`)。

### `QGraphicsPathItem *QGraphicsScene::addPath(const QPainterPath &path, const QPen &pen = QPen(), const QBrush &brush = QBrush())`

**作用与语义：**

创建并添加路径元素到场景，返回物品指针。路径几何由`path`定义，笔和笔刷初始化为`pen`和`brush`。
注意，该物品的几何形状以项目坐标表示，其位置初始化为 （0， 0）。
如果物品可见（即`QGraphicsItem::isVisible()`返回`true`），`QGraphicsScene`在控制返回事件循环时会发出`changed()`。

### `QGraphicsPixmapItem *QGraphicsScene::addPixmap(const QPixmap &pixmap)`

**作用与语义：**

创建并添加一个像素地图元素到场景中，返回物品指针。像素映射由`pixmap`定义。
注意，该物品的几何形状以项目坐标表示，其位置初始化为 （0， 0）。
如果物品可见（即`QGraphicsItem::isVisible()`返回`true`），`QGraphicsScene`在控制返回事件循环时会发出 `changed()`。

### `QGraphicsPolygonItem *QGraphicsScene::addPolygon(const QPolygonF &polygon, const QPen &pen = QPen(), const QBrush &brush = QBrush())`

**作用与语义：**

创建并添加一个多边形元素到场景，返回物品指针。多边形由`polygon`定义，笔和画笔初始化为`pen`和`brush`。
注意，该物品的几何形状以项目坐标表示，其位置初始化为 （0， 0）。
如果该物品可见（即`QGraphicsItem::isVisible()`返回`true`），`QGraphicsScene`在控制返回事件循环时会发出`changed()`。

### `QGraphicsRectItem *QGraphicsScene::addRect(const QRectF &rect, const QPen &pen = QPen(), const QBrush &brush = QBrush())`

**作用与语义：**

创建并添加一个矩形元素到场景，返回物品指针。矩形的几何体由`rect`定义，其笔和画笔初始化为`pen`和`brush`。
注意，该物品的几何形状以物品坐标表示，其位置初始化为 （0， 0）。例如，如果添加一个`QRect`（50， 50， 100， 100），其左上角相对于该物品坐标系的原点将位于 （50， 50）。
如果物品可见（即`QGraphicsItem::isVisible()`返回`true`），`QGraphicsScene`在控制返回事件循环时会发出`changed()`。

### `QGraphicsRectItem *QGraphicsScene::addRect(qreal x, qreal y, qreal w, qreal h, const QPen &pen = QPen(), const QBrush &brush = QBrush())`

**作用与语义：**

这个便捷函数等价于调用 addRect(`QRectF`(`x`, `y`, `w`, `h`), `pen`, `brush`) 。

### `QGraphicsSimpleTextItem *QGraphicsScene::addSimpleText(const QString &text, const QFont &font = QFont())`

**作用与语义：**

创建并添加场景中的`QGraphicsSimpleTextItem`，返回项目指针。文本字符串初始化为`text`，字体初始化为`font`。
该项的位置初始化为（0， 0）。
如果物品可见（即`QGraphicsItem::isVisible()`返回`true`），当控制返回事件循环时，`QGraphicsScene`会发出`changed()`。

### `QGraphicsTextItem *QGraphicsScene::addText(const QString &text, const QFont &font = QFont())`

**作用与语义：**

创建并添加文本项到场景，返回条目指针。文本字符串初始化为`text`，字体初始化为`font`。
该项的位置初始化为（0， 0）。
如果物品可见（即`QGraphicsItem::isVisible()`返回`true`），`QGraphicsScene`在控制返回事件循环时会发出`changed()`。

### `QGraphicsProxyWidget *QGraphicsScene::addWidget(QWidget *widget, Qt::WindowFlags wFlags = Qt::WindowFlags())`

**作用与语义：**

为`widget`创建一个新`QGraphicsProxyWidget`，添加到场景中，并返回代理的指针。`wFlags`为嵌入代理小部件设置默认窗口标志。
该项的位置初始化为（0， 0）。
如果该物品可见（即`QGraphicsItem::isVisible()`返回`true`），`QGraphicsScene`在控制返回事件循环时会发出`changed()`。
请注意，不支持带有`Qt::WA_PaintOnScreen`控件属性的控件以及包裹外部应用程序或控制器的控件。示例包括`QOpenGLWidget`和QAxWidget。

### `[slot] void QGraphicsScene::advance()`

**作用与语义：**

该槽通过调用场景中所有物品的 `QGraphicsItem::advance()`，将场景推进一步。该过程分为两个阶段：第一阶段，所有物品被通知场景即将变化;第二阶段通知所有物品可以移动。第一阶段称为 `QGraphicsItem::advance()` 传递 0 作为参数，第二阶段传递 1。
注意你也可以用动画框架来做动画。

### `[signal] void QGraphicsScene::changed(const QList<QRectF> &region)`

**作用与语义：**

当控制点到达事件环路时，如果场景内容发生变化，`QGraphicsScene`会发出该信号。`region`参数包含一个场景矩形列表，表示已更改的区域。

### `[slot] void QGraphicsScene::clear()`

**作用与语义：**

移除并删除场景中的所有物品，但场景状态保持不变。

### `void QGraphicsScene::clearFocus()`

**作用与语义：**

清除场景中的焦点。如果调用该功能时任何物品有焦点，它会失去焦点，场景恢复聚焦后重新聚焦。
一个没有焦点的场景会忽视按键事件。

### `[slot] void QGraphicsScene::clearSelection()`

**作用与语义：**

清除当前选择。

### `QList<QGraphicsItem *> QGraphicsScene::collidingItems(const QGraphicsItem *item, Qt::ItemSelectionMode mode = Qt::IntersectsItemShape) const`

**作用与语义：**

返回所有与`item`碰撞的物品列表。碰撞通过调用`QGraphicsItem::collidesWithItem()`确定;碰撞检测由`mode`确定。默认情况下，所有形状相交`item`或包含在`item`形状内的物品都会返回。
这些物品按递减顺序返回（即列表中第一个为最上项，最后一项为最底项）。

### `[virtual protected] void QGraphicsScene::contextMenuEvent(QGraphicsSceneContextMenuEvent *contextMenuEvent)`

**作用与语义：**

该事件处理程序可用于事件`contextMenuEvent`，可以在子类中重新实现以接收上下文菜单事件。默认实现会将事件转发到事件位置上最顶的可见项，该项目接受上下文菜单事件。如果该位置没有项目接受上下文菜单事件，则该事件被忽略。
注：关于哪些项目被该函数视为可见，请参见 `items()`。

### `QGraphicsItemGroup *QGraphicsScene::createItemGroup(const QList<QGraphicsItem *> &items)`

**作用与语义：**

将`items`中的所有项分组到新的`QGraphicsItemGroup`，并返回该组的指针。该组以`items`的共同祖先为父，位置为（0， 0）。所有项都被重新父级到组，它们的位置和变换映射到该组。如果`items`为空，该函数将返回空的顶层`QGraphicsItemGroup`。
`QGraphicsScene`拥有该组项目的所有权;你不需要删除它。要拆解（取消组）一个组，请调用`destroyItemGroup()`。

### `void QGraphicsScene::destroyItemGroup(QGraphicsItemGroup *group)`

**作用与语义：**

将`group`中的所有物品重新父级到`group`的父级，然后从场景中移除`group`，最后删除。这些物品的位置和变换会从组映射到组的父单位。

### `[virtual protected] void QGraphicsScene::dragEnterEvent(QGraphicsSceneDragDropEvent *event)`

**作用与语义：**

该事件处理程序用于事件`event`，可以在子类中重新实现，以接收场景的拖拽进入事件。
默认实现接受事件，并准备场景接受拖曳移动事件。

### `[virtual protected] void QGraphicsScene::dragLeaveEvent(QGraphicsSceneDragDropEvent *event)`

**作用与语义：**

该事件处理程序对于事件`event`，可以在子类中重新实现，以接收场景的拖放离开事件。

### `[virtual protected] void QGraphicsScene::dragMoveEvent(QGraphicsSceneDragDropEvent *event)`

**作用与语义：**

该事件处理程序用于事件`event`，可以在子类中重新实现，以接收场景的拖动移动事件。
注意：关于该函数视为可见的项目定义，请参见 `items()`。

### `[virtual protected] void QGraphicsScene::drawBackground(QPainter *painter, const QRectF &rect)`

**作用与语义：**

在绘制任何物品和前景之前，使用`painter`绘制场景背景。重新实现该函数，为场景提供自定义背景。
所有绘画均在场景坐标中完成。`rect`参数是曝光的矩形。
如果你只是想为背景定义颜色、纹理或渐变，可以调用`setBackgroundBrush()`。

### `[virtual protected] void QGraphicsScene::drawForeground(QPainter *painter, const QRectF &rect)`

**作用与语义：**

在绘制完背景和所有物品后，使用 `painter` 绘制场景前景。重新实现该函数，为场景提供自定义前景。
所有绘画都是在场景坐标中完成的。`rect`参数是暴露的矩形。
如果你只是想为前景定义颜色、纹理或渐变，可以调用`setForegroundBrush()`。

### `[virtual protected] void QGraphicsScene::dropEvent(QGraphicsSceneDragDropEvent *event)`

**作用与语义：**

该事件处理程序用于事件`event`，可以在子类中重新实现，以接收场景的丢弃事件。

### `[override virtual protected] bool QGraphicsScene::event(QEvent *event)`

**作用与语义：**

重实现自：`QObject::event`（QEvent *e）。
处理事件`event`，并将其分派到相应的事件处理程序。
除了调用便利事件处理程序外，该函数还负责将鼠标移动事件转换为悬浮事件，以应对没有鼠标抓取物品时的使用。悬浮事件直接传递到物品上;没有方便功能。
与`QWidget`不同，`QGraphicsScene`没有便利函数`enterEvent()`和`leaveEvent()`。用这个函数来获取这些事件。
如果`event`已被识别和处理，返回`true`;否则，返回`false`。

### `[override virtual protected] bool QGraphicsScene::eventFilter(QObject *watched, QEvent *event)`

**作用与语义：**

重实现自：`QObject::eventFilter`（QObject *已观看，QEvent *事件）。
`QGraphicsScene` 会过滤 `QApplication` 事件以检测调色板和字体的变化。

### `[virtual protected] void QGraphicsScene::focusInEvent(QFocusEvent *focusEvent)`

**作用与语义：**

该事件处理程序在事件`focusEvent`中可以重新实现，以获得事件中的关注点。
默认实现会先聚焦场景，然后再聚焦最后一个焦点。

### `QGraphicsItem *QGraphicsScene::focusItem() const`

**作用与语义：**

当场景处于激活状态时，该函数返回场景当前的焦点项目，若无焦点则返回`nullptr`。当场景处于非激活状态时，该函数返回场景激活时将获得输入焦点的物品。
当场景接收到按键事件时，焦点项会接收键盘输入。

### `[signal] void QGraphicsScene::focusItemChanged(QGraphicsItem *newFocusItem, QGraphicsItem *oldFocusItem, Qt::FocusReason reason)`

**作用与语义：**

当场景中焦点发生变化时（例如物品获得或失去输入焦点，或焦点从一个物品转移到另一个物体时），该信号由`QGraphicsScene`发出。如果你需要跟踪其他物品何时获得输入焦点，可以连接到该信号。它对实现虚拟键盘、输入方法和光标物品尤其有用。
`oldFocusItem` 是指向之前有焦点的物品的指针，如果信号发出前没有物品有焦点，则为 0。`newFocusItem` 是指向获得输入焦点的物品的指针，或在焦点丢失时指向`nullptr`。`reason` 是焦点变化的原因（例如，如果场景在输入场有焦点时关闭，`oldFocusItem`会指向输入场的物品，`newFocusItem` 是`nullptr`，`reason` 是`Qt::ActiveWindowFocusReason`）。

### `[virtual protected slot] bool QGraphicsScene::focusNextPrevChild(bool next)`

**作用与语义：**

根据 Tab 和 Shift Tab 的需要，找到新的控件以赋予键盘焦点，若能找到新控件则返回 `true`，找不到则返回 false。如果 `next` 为真，该函数向前搜索;如果 `next` 为假，则向后搜索。
你可以在`QGraphicsScene`的子类中重新实现这个函数，以提供对场景中标签焦点如何通过的细致控制。默认实现基于`QGraphicsWidget::setTabOrder()`定义的标签焦点链。

### `[virtual protected] void QGraphicsScene::focusOutEvent(QFocusEvent *focusEvent)`

**作用与语义：**

该事件处理程序用于事件`focusEvent`，可以在子类中重新实现以接收焦点输出事件。
默认实现会先移除焦点，然后移除场景中的焦点。

### `bool QGraphicsScene::hasFocus() const`

**作用与语义：**

如果场景有焦点，返回`true`;否则返回`false`。如果场景有焦点，它会将按键事件从`QKeyEvent`转发到任何有焦点的项目。

### `qreal QGraphicsScene::height() const`

**作用与语义：**

此便利函数等同于调用 `sceneRect().height()`。

### `[virtual protected] void QGraphicsScene::helpEvent(QGraphicsSceneHelpEvent *helpEvent)`

**作用与语义：**

该事件处理程序用于事件`helpEvent`，可以在子类中重新实现以接收帮助事件。事件类型为`QEvent::ToolTip`，当请求工具提示时创建。
默认实现会在鼠标光标位置显示最顶端可见物品的工具提示，即z值最高的物品。如果没有设置工具提示，这个函数就不会有任何作用。
注：关于哪些项目被该功能视为可见，请参见 `items()` 定义。

### `[virtual protected] void QGraphicsScene::inputMethodEvent(QInputMethodEvent *event)`

**作用与语义：**

该事件处理程序用于事件`event`，可以在子类中重新实现，以接收场景的输入法事件。
默认实现会将事件转发到`focusItem()`。如果当前没有焦点项，或者当前焦点项不接受输入方法，该函数则不起作用。

### `[virtual] QVariant QGraphicsScene::inputMethodQuery(Qt::InputMethodQuery query) const`

**作用与语义：**

输入法使用该方法查询场景的一组属性，以支持复杂的输入法操作，以支持周围文本和重新转换。
`query`参数指定查询的属性。

### `[slot] void QGraphicsScene::invalidate(const QRectF &rect = QRectF(), QGraphicsScene::SceneLayers layers = AllLayers)`

**作用与语义：**

在现场`rect`中`layers`无效并安排重新绘制。`layers`中的任何缓存内容都会无条件失效并重新绘制。
你可以利用这个功能重载来通知`QGraphicsScene`场景背景或前景的变化。这个功能通常用于基于瓦片背景的场景，用来通知`QGraphicsView`启用`CacheBackground`时发生的变化。
注意`QGraphicsView`目前仅支持后台缓存（见`QGraphicsView::CacheBackground`）。该函数等同于如果传递了除`BackgroundLayer`以外的任何层，调用`update()`。
注意：该槽位已超载。连接该槽位：


使用 qOverload 连接：
connect（sender， &SenderClass：：signal，。
graphicsScene， qOverload（&QGraphicsScene：：invalidate））;

或者用lambda作为包装器：
connect（sender， &SenderClass：：signal，。
graphicsScene， [receiver = graphicsScene]（const QRectF &rect， QGraphicsScene：：SceneLayers layers） { receiver->invalidate（rect， layers）; }）;


更多示例和方法，请参见连接超载槽位。

**官方示例：**

```cpp
 QRectF TileScene::rectForTile(int x, int y) const
 {
     // Return the rectangle for the tile at position (x, y).
     return QRectF(x * tileWidth, y * tileHeight, tileWidth, tileHeight);
 }

 void TileScene::setTile(int x, int y, const QPixmap &pixmap)
 {
     // Sets or replaces the tile at position (x, y) with pixmap.
     if (x >= 0 && x < numTilesH && y >= 0 && y < numTilesV) {
         tiles[y][x] = pixmap;
         invalidate(rectForTile(x, y), BackgroundLayer);
     }
 }

 void TileScene::drawBackground(QPainter *painter, const QRectF &exposed)
 {
     // Draws all tiles that intersect the exposed area.
     for (int y = 0; y < numTilesV; ++y) {
         for (int x = 0; x < numTilesH; ++x) {
             QRectF rect = rectForTile(x, y);
             if (exposed.intersects(rect))
                 painter->drawPixmap(rect.topLeft(), tiles[y][x]);
         }
     }
 }
```

### `void QGraphicsScene::invalidate(qreal x, qreal y, qreal w, qreal h, QGraphicsScene::SceneLayers layers = AllLayers)`

**作用与语义：**

这个便捷函数等效于调用 invalidate(`QRectF`(`x`, `y`, `w`, `h`), `layers`);

### `bool QGraphicsScene::isActive() const`

**作用与语义：**

如果场景处于激活状态（例如，至少有一个活跃`QGraphicsView`在观看），返回`true`;否则返回`false`。

### `QGraphicsItem *QGraphicsScene::itemAt(const QPointF &position, const QTransform &deviceTransform) const`

**作用与语义：**

返回指定`position`的最高可见物品，若该位置无物品则返回`nullptr`。
`deviceTransform`是适用于视图的变换，如果场景包含忽略变换的物品，则需要提供。
注意：关于该函数视为可见的项目定义，请参见 `items()`。

### `QGraphicsItem *QGraphicsScene::itemAt(qreal x, qreal y, const QTransform &deviceTransform) const`

**作用与语义：**

返回由（`x`， `y`）指定位置的最顶可见物品，若该位置无物品则返回`nullptr`。
`deviceTransform`是适用于视图的变换，如果场景包含忽略变换的物品，则需要提供。
这种便利函数等同于调用`itemAt(QPointF(x, y), deviceTransform)`。
注意：关于哪些项目被该函数视为可见，请参见 `items()`。

### `QList<QGraphicsItem *> QGraphicsScene::items(Qt::SortOrder order = Qt::DescendingOrder) const`

**作用与语义：**

返回现场所有物品的有序清单。`order`决定堆叠顺序。

### `QList<QGraphicsItem *> QGraphicsScene::items(const QPointF &pos, Qt::ItemSelectionMode mode = Qt::IntersectsItemShape, Qt::SortOrder order = Qt::DescendingOrder, const QTransform &deviceTransform = QTransform()) const`

**作用与语义：**

返回所有根据`mode`不同，在列表中指定`pos`的可见项，这些项用`order`排序。在这种情况下，“visible”定义了以下项：isVisible() 返回 `true`，effectiveOpacity() 返回大于 0.0（完全透明），且父项未裁剪。
`mode`的默认值是`Qt::IntersectsItemShape`;所有与`pos`形状相交的物品都会返回。
`deviceTransform`是适用于视图的变换，如果场景包含忽略变换的物品，则需要提供。

### `QList<QGraphicsItem *> QGraphicsScene::items(const QPainterPath &path, Qt::ItemSelectionMode mode = Qt::IntersectsItemShape, Qt::SortOrder order = Qt::DescendingOrder, const QTransform &deviceTransform = QTransform()) const`

**作用与语义：**

返回所有根据`mode`，在列表中以`order`排序的列表中，这些可见项要么与指定`path`相交。在这种情况下，“visible”定义了以下条件的项：isVisible() 返回 `true`，effectiveOpacity() 返回大于 0.0（完全透明），且父项不会裁剪该项。
`mode`的默认值为`Qt::IntersectsItemShape`;所有与`path`相交或包含的具体形状的项都会返回。
`deviceTransform`是适用于视图的变换，如果场景包含忽略变换的物品，则需要提供。

### `QList<QGraphicsItem *> QGraphicsScene::items(const QPolygonF &polygon, Qt::ItemSelectionMode mode = Qt::IntersectsItemShape, Qt::SortOrder order = Qt::DescendingOrder, const QTransform &deviceTransform = QTransform()) const`

**作用与语义：**

返回所有根据`mode`不同，位于指定`polygon`内或与其相交的可见项，且列表用`order`排序。在这种情况下，“visible”定义了以下条件的项：isVisible() 返回 `true`，effectiveOpacity() 返回大于 0.0（完全透明），且父项不裁剪该项。
`mode`的默认值为`Qt::IntersectsItemShape`;所有与`polygon`相交或包含的具体形状的项都会返回。
`deviceTransform`是适用于视图的变换，如果场景包含忽略变换的物品，则需要提供。

### `QList<QGraphicsItem *> QGraphicsScene::items(const QRectF &rect, Qt::ItemSelectionMode mode = Qt::IntersectsItemShape, Qt::SortOrder order = Qt::DescendingOrder, const QTransform &deviceTransform = QTransform()) const`

**作用与语义：**

返回所有根据`mode`不同，在列表中以`order`排序的列表中，这些可见项要么在指定`rect`内，要么与之相交。在这种情况下，“可见”定义了以下条件的项：isVisible() 返回 `true`，effectiveOpacity() 返回大于 0.0（完全透明），且父项不会裁剪该项。
`mode`的默认值为`Qt::IntersectsItemShape`;所有与`rect`相交或包含的具体形状的项都会返回。
`deviceTransform`是适用于视图的变换，如果场景包含忽略变换的物品，则需要提供。

### `QList<QGraphicsItem *> QGraphicsScene::items(qreal x, qreal y, qreal w, qreal h, Qt::ItemSelectionMode mode, Qt::SortOrder order, const QTransform &deviceTransform = QTransform()) const`

**作用与语义：**

返回所有可见的项，这些项取决于`mode`，要么位于`x`、`y`、`w`和`h`定义的矩形内，要么与其相交，且列表用`order`排序。在这种情况下，“可见”定义了以下项：isVisible() 返回 `true`，effectiveOpacity() 返回大于 0.0（完全透明），且父项不会裁剪该矩形。
`deviceTransform` 是适用于视图的变换，如果场景包含忽略变换的物品，则需要提供。

### `QRectF QGraphicsScene::itemsBoundingRect() const`

**作用与语义：**

计算并返回场景中所有物品的边界矩形。该函数通过遍历所有物品来工作，因此对于大型场景来说可能会比较慢。

### `[virtual protected] void QGraphicsScene::keyPressEvent(QKeyEvent *keyEvent)`

**作用与语义：**

该事件处理程序用于事件`keyEvent`，可以在子类中重新实现以接收按键事件。默认实现会将事件转发到当前焦点项。

### `[virtual protected] void QGraphicsScene::keyReleaseEvent(QKeyEvent *keyEvent)`

**作用与语义：**

该事件处理程序用于事件`keyEvent`，可以在子类中重新实现以接收密钥释放事件。默认实现会将事件转发到当前焦点项。

### `[virtual protected] void QGraphicsScene::mouseDoubleClickEvent(QGraphicsSceneMouseEvent *mouseEvent)`

**作用与语义：**

该事件处理程序用于事件`mouseEvent`，可以重新实现为子类，以接收场景的鼠标双击事件。
如果有人在场景中双击，场景先会收到鼠标新闻事件，接着是发布事件（即点击），再是双击事件，最后是发布事件。如果双击事件传递到与首次新闻发布的物品不同的物品上，则会作为新闻事件发送。但在这种情况下，三击事件不会作为双击事件发送。
默认实现与`mousePressEvent()`类似。
注意：关于该函数视为可见的项目定义，请参见 `items()`。

### `QGraphicsItem *QGraphicsScene::mouseGrabberItem() const`

**作用与语义：**

返回当前的鼠标抓取物品，或者如果没有当前抓取该鼠标的物品，则返回`nullptr`。抓取鼠标的物品是接收所有发送到场景的鼠标事件的物品。
当物品收到并接受鼠标按键事件时，它就成为鼠标抓取器，并且在以下任一事件发生前保持抓鼠状态：
- 如果物品在没有其他按键按下时触发鼠标释放事件，则失去鼠标抓取功能。
- 如果物品变得隐形（即有人喊`item->setVisible(false)`），或者被禁用（即有人喊`item->setEnabled(false)`），则失去抓取鼠标的权利。
- 如果物品从场景中移除，则失去鼠标抓取功能。
如果物品失去鼠标抓取，场景将忽略所有鼠标事件，直到新物品抓取该鼠标（即新物品获得鼠标按键事件）。

### `[virtual protected] void QGraphicsScene::mouseMoveEvent(QGraphicsSceneMouseEvent *mouseEvent)`

**作用与语义：**

该事件处理程序用于事件`mouseEvent`，可以在子类中重新实现，以接收场景中的鼠标移动事件。
默认实现取决于鼠标抓取器的状态。如果有抓取鼠标的物品，事件会发送给抓取者。如果当前位置有任何物品接受悬停事件，该事件会被转换成悬停事件并被接受;否则会被忽略。

### `[virtual protected] void QGraphicsScene::mousePressEvent(QGraphicsSceneMouseEvent *mouseEvent)`

**作用与语义：**

该事件处理程序用于事件`mouseEvent`，可以在子类中重新实现，以接收场景的鼠标按键事件。
默认实现取决于场景的状态。如果存在抓取鼠标的物品，事件会发送给抓取物品。否则，事件会转发到事件中最顶端的可见物品，该物品会立即成为抓取物品。
如果场景中给定位置没有物品，选择区域会重置，任何焦点物品都会失去输入焦点，事件随后被忽略。
注意：关于该函数视为可见的项目定义，请参见 `items()`。

### `[virtual protected] void QGraphicsScene::mouseReleaseEvent(QGraphicsSceneMouseEvent *mouseEvent)`

**作用与语义：**

该事件处理程序用于事件`mouseEvent`，可以在子类中重新实现，以接收场景中的鼠标释放事件。
默认实现取决于鼠标抓取器的状态。如果没有抓取鼠标，该事件将被忽略。否则，如果有抓取物品，事件会发送给抓取鼠标。如果该松开鼠标代表鼠标上最后按下的按钮，抓取物品则失去抓取鼠标。

### `void QGraphicsScene::removeItem(QGraphicsItem *item)`

**作用与语义：**

将`item`物品及其所有子物品从场景中移除。`item`的所有权转移给调用者（即`QGraphicsScene`销毁后不会再删除`item`）。

### `void QGraphicsScene::render(QPainter *painter, const QRectF &target = QRectF(), const QRectF &source = QRectF(), Qt::AspectRatioMode aspectRatioMode = Qt::KeepAspectRatio)`

**作用与语义：**

利用`painter`将场景中的`source`矩形渲染到`target`。此功能用于将场景内容捕获到绘图设备，如`QImage`（例如截图），或用于用QPrinter打印。例如：
如果`source`是空矩形矩形，该函数会用`sceneRect()`来决定渲染什么。如果`target`是空矩形矩形，则使用`painter`的绘画装置的尺寸。
源矩形块内容会根据`aspectRatioMode`进行转换以适应目标矩形块。默认情况下，保持宽高比，`source`会根据`target`进行缩放以适应。

**官方示例：**

```cpp
 QGraphicsScene scene;
 scene.addItem(...
 ...
 QPrinter printer(QPrinter::HighResolution);
 printer.setPaperSize(QPrinter::A4);

 QPainter painter(&printer);
 scene.render(&painter);
```

### `[signal] void QGraphicsScene::sceneRectChanged(const QRectF &rect)`

**作用与语义：**

每当场景矩形发生变化时，`QGraphicsScene`会发出该信号。`rect`参数是新的场景矩形。

### `QList<QGraphicsItem *> QGraphicsScene::selectedItems() const`

**作用与语义：**

返回所有当前已选中的物品列表。物品的返回顺序无特定。

### `QPainterPath QGraphicsScene::selectionArea() const`

**作用与语义：**

返回之前用`setSelectionArea()`设置的选择区域，若未设置则返回空`QPainterPath`。

### `[signal] void QGraphicsScene::selectionChanged()`

**作用与语义：**

每当选择发生变化时，`QGraphicsScene`会发出这个信号。你可以打电话给`selectedItems()`获取新的选中物品清单。
每当选择或取消选中某个物品、设置、清除或以其他方式更改选择区域，或者将预选物品添加到场景中，或从场景中移除选中物品时，选择都会发生变化。
`QGraphicsScene` 在组选择操作中只发出一次该信号。例如，如果你设置了选择区域，选择或取消了`QGraphicsItemGroup`，或者在场景中添加或移除包含多个选中项目的父项，selectionChanged() 只在操作完成后发出一次（而不是每个项目一次）。

### `bool QGraphicsScene::sendEvent(QGraphicsItem *item, QEvent *event)`

**作用与语义：**

通过可能的事件过滤器向物品 `item`发送事件`event`。
只有当该物品被启用时才会发送该事件。
返回`false`事件是否被过滤或该项被禁用。否则返回事件处理器返回的值。

### `void QGraphicsScene::setActivePanel(QGraphicsItem *item)`

**作用与语义：**

激活`item`，这必须是本场景中的物品。你也可以通过0代`item`，此时`QGraphicsScene`会关闭当前激活的任何面板。
如果场景当前处于非激活状态，`item`保持非激活状态，直到场景激活（或`item` `nullptr`时，物品不会被激活）。

### `void QGraphicsScene::setActiveWindow(QGraphicsWidget *widget)`

**作用与语义：**

激活`widget`，这必须是该场景中的一个小部件。你也可以为`widget`传递0，这样`QGraphicsScene`会关闭当前任何正在激活的窗口。

### `void QGraphicsScene::setFocus(Qt::FocusReason focusReason = Qt::OtherFocusReason)`

**作用与语义：**

Set 通过发送`QFocusEvent`到场景，将`focusReason`作为原因来聚焦场景。如果场景在之前失去焦点且物品有焦点后重新获得焦点，最后一个焦点物品将获得焦点，原因为`focusReason`。
如果场景已经有焦点，这个功能就不做任何事。

### `void QGraphicsScene::setFocusItem(QGraphicsItem *item, Qt::FocusReason focusReason = Qt::OtherFocusReason)`

**作用与语义：**

在移除之前可能有焦点的物品后，将场景的焦点物品设置为`item`，焦点理由`focusReason`。
如果`item`是`nullptr`，或者它不接受对焦（即未启用`QGraphicsItem::ItemIsFocusable`标志），或者不可见或未启用，该功能仅会移除之前任何焦点物品的焦点。
如果物品未`nullptr`，且场景当前没有焦点（即返回`hasFocus()`返回`false`），该函数会自动调用`setFocus()`。

### `void QGraphicsScene::setSelectionArea(const QPainterPath &path, const QTransform &deviceTransform)`

**作用与语义：**

将选择区域设置为`path`。该区域内的所有物品会立即被选中，外面的所有物品都未被选中。你可以通过调用`selectedItems()`获取所有被选中的物品列表。
`deviceTransform`是适用于视图的变换，如果场景中包含忽略变换的物品，则需要提供。
要选择某个项目，必须标记为可选（`QGraphicsItem::ItemIsSelectable`）。

### `void QGraphicsScene::setSelectionArea(const QPainterPath &path, Qt::ItemSelectionOperation selectionOperation = Qt::ReplaceSelection, Qt::ItemSelectionMode mode = Qt::IntersectsItemShape, const QTransform &deviceTransform = QTransform())`

**作用与语义：**

通过`mode`来确定项目是否包含在选择区域内，将选择区域设置为`path`。
`deviceTransform` 是适用于视图的变换，如果场景包含忽略变换的物品，则需要提供。
`selectionOperation`决定当前选中的物品如何处理。

### `void QGraphicsScene::setStyle(QStyle *style)`

**作用与语义：**

将场景样式设置为或替换为`style`，并将样式重新父级到该场景。之前分配的任何样式都会被删除。场景的样式默认为`QApplication::style()`，并作为场景中所有`QGraphicsWidget`项的默认。
无论是直接调用该函数，还是间接调用 `QApplication::setStyle()`，都会自动更新场景中所有未被明确分配样式的小部件的样式。
如果`style` `nullptr`，`QGraphicsScene`会恢复为`QApplication::style()`。

### `QStyle *QGraphicsScene::style() const`

**作用与语义：**

返回场景的样式，或者如果场景没有明确分配样式，则返回`QApplication::style()`样式。

### `[slot] void QGraphicsScene::update(const QRectF &rect = QRectF())`

**作用与语义：**

安排现场`rect`区域的重新绘制。
注意：该槽位已超载。连接该槽位：


使用 qOverload 连接：
connect（sender， &SenderClass：：signal，。
graphicsScene， qOverload（&QGraphicsScene：：update））;

或者用lambda作为包装器：
connect（sender， &SenderClass：：signal，。
graphicsScene， [receiver = graphicsScene]（const QRectF &rect） { receiver->update（rect）; }）;


更多示例和方法，请参见连接超载槽位。

### `void QGraphicsScene::update(qreal x, qreal y, qreal w, qreal h)`

**作用与语义：**

该函数等同于调用 update（`QRectF`（`x`， `y`， `w`， `h`））;

### `QList<QGraphicsView *> QGraphicsScene::views() const`

**作用与语义：**

返回显示该场景的所有视图列表。

### `[virtual protected] void QGraphicsScene::wheelEvent(QGraphicsSceneWheelEvent *wheelEvent)`

**作用与语义：**

该事件处理程序用于事件`wheelEvent`，可以在子类中重新实现，以接收场景的鼠标滚轮事件。
默认情况下，事件会传递到光标下方最顶层的可见物品。如果被忽略，事件会传播到下面的物品，反复传播直到事件被接受或事件到达场景。如果没有物品接受该事件，则被忽略。
注：关于哪些项目被该功能视为可见，请参见 `items()` 定义。

### `qreal QGraphicsScene::width() const`

**作用与语义：**

此便利函数等同于调用 `sceneRect()`.width()。

### `enum SceneLayer { ItemLayer, BackgroundLayer, ForegroundLayer, AllLayers }`

**作用与语义：**

这个枚举描述了`QGraphicsScene`中的渲染层。当`QGraphicsScene`绘制场景内容时，会按顺序分别渲染每一层。
每层代表一个标志，在调用 `invalidate()` 或 `QGraphicsView::invalidateScene()` 等函数时可以合并进行 OR 映射。
- `QGraphicsScene::ItemLayer`：`0x1`;物品图层。`QGraphicsScene`通过调用虚拟函数 drawItems() 来渲染所有位于该图层中的物品。物品图层绘制在背景图层之后，但前景图层之前。
- `QGraphicsScene::BackgroundLayer`：`0x2`;背景图层。`QGraphicsScene` 通过调用虚拟函数 `drawBackground()` 来渲染该图层的场景背景。背景图层是所有图层中第一个绘制的。
- `QGraphicsScene::ForegroundLayer`：`0x4`;前景图层。`QGraphicsScene` 通过调用虚拟函数 `drawForeground()` 来渲染该图层的场景前景。前景图层是所有图层中最后绘制的。
- `QGraphicsScene::AllLayers`：`0xffff`;所有层;该值代表三层的组合。
SceneLayers 类型是 QFlags 的 typedef<SceneLayer>。它存储 SceneLayer 值的 OR 组合。

### `flags SceneLayers`

**作用与语义：**

这个枚举描述了`QGraphicsScene`中的渲染层。当`QGraphicsScene`绘制场景内容时，会按顺序分别渲染每一层。
每层代表一个标志，在调用 `invalidate()` 或 `QGraphicsView::invalidateScene()` 等函数时可以合并进行 OR 映射。
- `QGraphicsScene::ItemLayer`：`0x1`;物品图层。`QGraphicsScene`通过调用虚拟函数 drawItems() 来渲染所有位于该图层中的物品。物品图层绘制在背景图层之后，但前景图层之前。
- `QGraphicsScene::BackgroundLayer`：`0x2`;背景图层。`QGraphicsScene` 通过调用虚拟函数 `drawBackground()` 来渲染该图层的场景背景。背景图层是所有图层中第一个绘制的。
- `QGraphicsScene::ForegroundLayer`：`0x4`;前景图层。`QGraphicsScene` 通过调用虚拟函数 `drawForeground()` 来渲染该图层的场景前景。前景图层是所有图层中最后绘制的。
- `QGraphicsScene::AllLayers`：`0xffff`;所有层;该值代表三层的组合。
SceneLayers 类型是 QFlags 的 typedef<SceneLayer>。它存储 SceneLayer 值的 OR 组合。

### `QBrush backgroundBrush() const`

**作用与语义：**

该属性保留场景的背景画笔。
将此属性设置为将场景背景更换为不同的颜色、渐变或纹理。默认的背景刷是`Qt::NoBrush`。背景是在物品之前（后方）绘制的。
`QGraphicsScene::render()`调用`drawBackground()`来绘制场景背景。为了更详细地控制背景绘制方式，可以在`QGraphicsScene`子类中重新实现`drawBackground()`。

**如何使用：** 调用 `backgroundBrush()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 QGraphicsScene scene;
 QGraphicsView view(&scene);
 view.show();

 // a blue background
 scene.setBackgroundBrush(Qt::blue);

 // a gradient background
 QRadialGradient gradient(0, 0, 10);
 gradient.setSpread(QGradient::RepeatSpread);
 scene.setBackgroundBrush(gradient);
```

### `int bspTreeDepth() const`

**作用与语义：**

此属性保存 `QGraphicsScene` 的 BSP 索引树的深度。
当使用 `NoIndex` 时，此属性无效。
该值决定 `QGraphicsScene` 的 BSP 树深度。树深度直接影响 `QGraphicsScene` 的性能和内存使用；内存使用随着树的深度呈指数增加。树深度优化后，`QGraphicsScene` 可以瞬间确定项目的局部性，即使场景中有成千上万或数百万的项目，也会大大提高渲染性能。
默认值为 0，此时 Qt 将根据场景中项目的大小、位置和数量自动推测合理的默认深度。然而，如果这些参数频繁变化，`QGraphicsScene` 在内部重新调整深度时，可能会导致性能下降。通过设置此属性固定树深度可以避免潜在的性能下降。
树的深度和场景矩形的大小决定场景分割的颗粒度。每个场景段的大小由以下算法决定：
当每个段包含 0 到 10 个项目时，BSP 树大小为最优。

**如何使用：** 调用 `bspTreeDepth()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 QSizeF segmentSize = sceneRect().size() / pow(2, depth - 1);
```

### `bool focusOnTouch() const`

**作用与语义：**

该特性决定物品在获得触控启动事件时是否获得焦点。
通常的行为是只有在点击某个项目时才转移焦点。操作系统通常将触摸板上的轻触等同于鼠标点击，生成合成点击事件作为响应。不过，至少在macOS上你可以配置这种行为。
默认情况下，`QGraphicsScene`在触控板等触控板上操作时也会转移焦点。如果操作系统配置为点击触控板时不生成合成鼠标点击，这就令人惊讶了。如果操作系统在点击触控板时会产生合成鼠标点击，启动触控手势时的焦点转移就没必要了。
关闭 focusOnTouch 后，`QGraphicsScene` 的表现与 macOS 上正常。
默认值为`true`，确保默认行为与5.12之前的Qt版本相同。设置为`false`以防止触摸事件触发焦点变化。

**如何使用：** 调用 `focusOnTouch()` 读取当前值；它不会修改应用状态。

### `QFont font() const`

**作用与语义：**

该属性保留场景的默认字体。
该属性提供场景的字体。场景字体默认为 ，并解析所有来自 的条目 `QApplication::font`。
如果场景的字体发生变化，无论是直接通过 setFont() 还是在应用程序字体变化时间接发生，`QGraphicsScene` 首先向自己发送一个 `FontChange` 事件，然后向场景中所有顶层控件发送`FontChange`事件。这些元素通过向场景解析自己的字体来响应，然后通知其子节点，子节点再次通知子节点，如此循环，直到所有控件元素都更新了字体。
更改场景字体（无论是直接还是间接通过`QApplication::setFont()`）会自动安排整个场景的重新绘制。

**如何使用：** 调用 `font()` 读取当前值；它不会修改应用状态。

### `QBrush foregroundBrush() const`

**作用与语义：**

该属性保留了场景的前景画笔。
更改此属性，将场景前景设置为不同的颜色、渐变或纹理。
前景是在物品之后（上方）绘制的。默认的前景画笔是`Qt::NoBrush`（即不绘制前景）。
`QGraphicsScene::render()`调用`drawForeground()`来绘制场景前景。如果想更详细地控制前景绘制方式，可以在`QGraphicsScene`子类中重新实现`drawForeground()`函数。

**如何使用：** 调用 `foregroundBrush()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 QGraphicsScene scene;
 QGraphicsView view(&scene);
 view.show();

 // a white semi-transparent foreground
 scene.setForegroundBrush(QColor(255, 255, 255, 127));

 // a grid foreground
 scene.setForegroundBrush(QBrush(Qt::lightGray, Qt::CrossPattern));
```

### `QGraphicsScene::ItemIndexMethod itemIndexMethod() const`

**作用与语义：**

该属性包含了项目索引方法。
`QGraphicsScene` 对场景应用索引算法，以加快`items()`和`itemAt()`等物品发现功能。索引在静态场景（即物品不移动）时最为高效。对于动态场景或包含大量动画元素的场景，索引簿记可能超过快速查找速度。
对于常见情况，默认的索引方法`BspTreeIndex`正常工作。如果你的场景使用了很多动画且出现缓慢，可以通过调用`setItemIndexMethod(NoIndex)`来禁用索引。

**如何使用：** 调用 `itemIndexMethod()` 读取当前值；它不会修改应用状态。

### `qreal minimumRenderSize() const`

**作用与语义：**

该属性表示了物品必须绘制的最小视图变换尺寸。
当场景被渲染时，任何宽度或高度变换到目标视图后小于 minimumRenderSize() 的物品都不会被渲染。如果某个物品未被渲染且裁剪了其子对象，它们也不会被渲染。设置该值以加快在缩放视图下渲染多物体场景的渲染速度。
默认值是0。如果未设置，或者设置为0或负值，所有项目都会被渲染。
例如，设置该属性在场景由多个视图渲染时尤其有用，其中一个视图作为总览，始终显示所有物品。在拥有多物品的场景中，这种视图会使用较高的缩放因子，以便显示所有物品。由于缩放，较小的物体对最终渲染场景的贡献微乎其微。为了避免绘制这些元素并缩短渲染场景所需时间，你可以调用 setMinimumRenderSize() 并设置非负值。
注意：由于太小未绘制的物品仍会通过`items()`和`itemAt()`等方法返回，并参与碰撞检测和交互。建议将 minimumRenderSize() 设置为小于或等于 1，以避免大型未渲染的可交互物品。

**如何使用：** 调用 `minimumRenderSize()` 读取当前值；它不会修改应用状态。

### `QPalette palette() const`

**作用与语义：**

该属性保留了场景的默认调色板。
该属性提供场景调色板。场景调色板默认使用并解析所有元素，`QApplication::palette`。
如果场景调色板发生变化，无论是直接通过 setPalette() 还是在应用调色板变更时间接发生，`QGraphicsScene` 首先向自己发送一个 `PaletteChange` 事件，然后向场景中所有顶层控件发送`PaletteChange`事件。这些控件通过向场景解析自己的调色板来响应，然后通知其子节点，子节点再通知子节点，如此循环，直到所有控件项目更新了调色板。
通过`QApplication::setPalette()`直接或间接更改场景调色板，会自动安排整个场景的重新绘制。

**如何使用：** 调用 `palette()` 读取当前值；它不会修改应用状态。

### `QRectF sceneRect() const`

**作用与语义：**

该属性表示场景矩形;场景的边界矩形。
场景矩形定义了场景的范围。它主要用于`QGraphicsView`确定视图默认可滚动区域，`QGraphicsScene`则用于管理物品索引。
如果未设置，或者设置为空`QRectF`，sceneRect() 将返回自场景创建以来场景中所有物品中最大的边界矩形（即当场景中添加或移动物品时会增长但不会缩小的矩形）。

**如何使用：** 调用 `sceneRect()` 读取当前值；它不会修改应用状态。

### `void setBackgroundBrush(const QBrush &brush)`

**作用与语义：**

该属性保留场景的背景画笔。
将此属性设置为将场景背景更换为不同的颜色、渐变或纹理。默认的背景刷是`Qt::NoBrush`。背景是在物品之前（后方）绘制的。
`QGraphicsScene::render()`调用`drawBackground()`来绘制场景背景。为了更详细地控制背景绘制方式，可以在`QGraphicsScene`子类中重新实现`drawBackground()`。

**如何使用：** 调用 `setBackgroundBrush(...)` 修改 `backgroundBrush`；传入的新值会成为后续查询和相关界面行为所使用的值。

**官方示例：**

```cpp
 QGraphicsScene scene;
 QGraphicsView view(&scene);
 view.show();

 // a blue background
 scene.setBackgroundBrush(Qt::blue);

 // a gradient background
 QRadialGradient gradient(0, 0, 10);
 gradient.setSpread(QGradient::RepeatSpread);
 scene.setBackgroundBrush(gradient);
```

### `void setBspTreeDepth(int depth)`

**作用与语义：**

此属性保存 `QGraphicsScene` 的 BSP 索引树的深度。
当使用 `NoIndex` 时，此属性无效。
该值决定 `QGraphicsScene` 的 BSP 树深度。树深度直接影响 `QGraphicsScene` 的性能和内存使用；内存使用随着树的深度呈指数增加。树深度优化后，`QGraphicsScene` 可以瞬间确定项目的局部性，即使场景中有成千上万或数百万的项目，也会大大提高渲染性能。
默认值为 0，此时 Qt 将根据场景中项目的大小、位置和数量自动推测合理的默认深度。然而，如果这些参数频繁变化，`QGraphicsScene` 在内部重新调整深度时，可能会导致性能下降。通过设置此属性固定树深度可以避免潜在的性能下降。
树的深度和场景矩形的大小决定场景分割的颗粒度。每个场景段的大小由以下算法决定：
当每个段包含 0 到 10 个项目时，BSP 树大小为最优。

**如何使用：** 调用 `setBspTreeDepth(...)` 修改 `bspTreeDepth`；传入的新值会成为后续查询和相关界面行为所使用的值。

**官方示例：**

```cpp
 QSizeF segmentSize = sceneRect().size() / pow(2, depth - 1);
```

### `void setFocusOnTouch(bool enabled)`

**作用与语义：**

该特性决定物品在获得触控启动事件时是否获得焦点。
通常的行为是只有在点击某个项目时才转移焦点。操作系统通常将触摸板上的轻触等同于鼠标点击，生成合成点击事件作为响应。不过，至少在macOS上你可以配置这种行为。
默认情况下，`QGraphicsScene`在触控板等触控板上操作时也会转移焦点。如果操作系统配置为点击触控板时不生成合成鼠标点击，这就令人惊讶了。如果操作系统在点击触控板时会产生合成鼠标点击，启动触控手势时的焦点转移就没必要了。
关闭 focusOnTouch 后，`QGraphicsScene` 的表现与 macOS 上正常。
默认值为`true`，确保默认行为与5.12之前的Qt版本相同。设置为`false`以防止触摸事件触发焦点变化。

**如何使用：** 调用 `setFocusOnTouch(...)` 修改 `focusOnTouch`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setFont(const QFont &font)`

**作用与语义：**

该属性保留场景的默认字体。
该属性提供场景的字体。场景字体默认为 ，并解析所有来自 的条目 `QApplication::font`。
如果场景的字体发生变化，无论是直接通过 setFont() 还是在应用程序字体变化时间接发生，`QGraphicsScene` 首先向自己发送一个 `FontChange` 事件，然后向场景中所有顶层控件发送`FontChange`事件。这些元素通过向场景解析自己的字体来响应，然后通知其子节点，子节点再次通知子节点，如此循环，直到所有控件元素都更新了字体。
更改场景字体（无论是直接还是间接通过`QApplication::setFont()`）会自动安排整个场景的重新绘制。

**如何使用：** 调用 `setFont(...)` 修改 `font`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setForegroundBrush(const QBrush &brush)`

**作用与语义：**

该属性保留了场景的前景画笔。
更改此属性，将场景前景设置为不同的颜色、渐变或纹理。
前景是在物品之后（上方）绘制的。默认的前景画笔是`Qt::NoBrush`（即不绘制前景）。
`QGraphicsScene::render()`调用`drawForeground()`来绘制场景前景。如果想更详细地控制前景绘制方式，可以在`QGraphicsScene`子类中重新实现`drawForeground()`函数。

**如何使用：** 调用 `setForegroundBrush(...)` 修改 `foregroundBrush`；传入的新值会成为后续查询和相关界面行为所使用的值。

**官方示例：**

```cpp
 QGraphicsScene scene;
 QGraphicsView view(&scene);
 view.show();

 // a white semi-transparent foreground
 scene.setForegroundBrush(QColor(255, 255, 255, 127));

 // a grid foreground
 scene.setForegroundBrush(QBrush(Qt::lightGray, Qt::CrossPattern));
```

### `void setItemIndexMethod(QGraphicsScene::ItemIndexMethod method)`

**作用与语义：**

该属性包含了项目索引方法。
`QGraphicsScene` 对场景应用索引算法，以加快`items()`和`itemAt()`等物品发现功能。索引在静态场景（即物品不移动）时最为高效。对于动态场景或包含大量动画元素的场景，索引簿记可能超过快速查找速度。
对于常见情况，默认的索引方法`BspTreeIndex`正常工作。如果你的场景使用了很多动画且出现缓慢，可以通过调用`setItemIndexMethod(NoIndex)`来禁用索引。

**如何使用：** 调用 `setItemIndexMethod(...)` 修改 `itemIndexMethod`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMinimumRenderSize(qreal minSize)`

**作用与语义：**

该属性表示了物品必须绘制的最小视图变换尺寸。
当场景被渲染时，任何宽度或高度变换到目标视图后小于 minimumRenderSize() 的物品都不会被渲染。如果某个物品未被渲染且裁剪了其子对象，它们也不会被渲染。设置该值以加快在缩放视图下渲染多物体场景的渲染速度。
默认值是0。如果未设置，或者设置为0或负值，所有项目都会被渲染。
例如，设置该属性在场景由多个视图渲染时尤其有用，其中一个视图作为总览，始终显示所有物品。在拥有多物品的场景中，这种视图会使用较高的缩放因子，以便显示所有物品。由于缩放，较小的物体对最终渲染场景的贡献微乎其微。为了避免绘制这些元素并缩短渲染场景所需时间，你可以调用 setMinimumRenderSize() 并设置非负值。
注意：由于太小未绘制的物品仍会通过`items()`和`itemAt()`等方法返回，并参与碰撞检测和交互。建议将 minimumRenderSize() 设置为小于或等于 1，以避免大型未渲染的可交互物品。

**如何使用：** 调用 `setMinimumRenderSize(...)` 修改 `minimumRenderSize`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setPalette(const QPalette &palette)`

**作用与语义：**

该属性保留了场景的默认调色板。
该属性提供场景调色板。场景调色板默认使用并解析所有元素，`QApplication::palette`。
如果场景调色板发生变化，无论是直接通过 setPalette() 还是在应用调色板变更时间接发生，`QGraphicsScene` 首先向自己发送一个 `PaletteChange` 事件，然后向场景中所有顶层控件发送`PaletteChange`事件。这些控件通过向场景解析自己的调色板来响应，然后通知其子节点，子节点再通知子节点，如此循环，直到所有控件项目更新了调色板。
通过`QApplication::setPalette()`直接或间接更改场景调色板，会自动安排整个场景的重新绘制。

**如何使用：** 调用 `setPalette(...)` 修改 `palette`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setSceneRect(const QRectF &rect)`

**作用与语义：**

该属性表示场景矩形;场景的边界矩形。
场景矩形定义了场景的范围。它主要用于`QGraphicsView`确定视图默认可滚动区域，`QGraphicsScene`则用于管理物品索引。
如果未设置，或者设置为空`QRectF`，sceneRect() 将返回自场景创建以来场景中所有物品中最大的边界矩形（即当场景中添加或移动物品时会增长但不会缩小的矩形）。

**如何使用：** 调用 `setSceneRect(...)` 修改 `sceneRect`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setSceneRect(qreal x, qreal y, qreal w, qreal h)`

**作用与语义：**

该属性表示场景矩形;场景的边界矩形。
场景矩形定义了场景的范围。它主要用于`QGraphicsView`确定视图默认可滚动区域，`QGraphicsScene`则用于管理物品索引。
如果未设置，或者设置为空`QRectF`，sceneRect() 将返回自场景创建以来场景中所有物品中最大的边界矩形（即当场景中添加或移动物品时会增长但不会缩小的矩形）。

**如何使用：** 调用 `setSceneRect(...)` 修改 `sceneRect`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setStickyFocus(bool enabled)`

**作用与语义：**

该属性适用于点击场景背景时是否清除焦点。
在 stickyFocus 设置为 true 的 `QGraphicsScene` 中，当用户点击场景背景或不接受焦点的项目时，焦点保持不变。否则，焦点将被清除。
默认情况下，该属性为 `false`。
焦点会响应鼠标按下事件变化。可以在 `QGraphicsScene` 的子类中重新实现 `mousePressEvent()`，以根据用户点击位置切换此属性。

**如何使用：** 调用 `setStickyFocus(...)` 修改 `stickyFocus`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `bool stickyFocus() const`

**作用与语义：**

该属性适用于点击场景背景时是否清除焦点。
在 stickyFocus 设置为 true 的 `QGraphicsScene` 中，当用户点击场景背景或不接受焦点的项目时，焦点保持不变。否则，焦点将被清除。
默认情况下，该属性为 `false`。
焦点会响应鼠标按下事件变化。可以在 `QGraphicsScene` 的子类中重新实现 `mousePressEvent()`，以根据用户点击位置切换此属性。

**如何使用：** 调用 `stickyFocus()` 读取当前值；它不会修改应用状态。

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

`QGraphicsScene` 所属机制类型：图形场景与项目机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
