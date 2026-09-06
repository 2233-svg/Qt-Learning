# QGraphicsView

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QGraphicsView` 是 图形场景与项目机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QGraphicsView` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QGraphicsView>`
- 继承自：QAbstractScrollArea
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

- `flags CacheMode`
- `enum CacheModeFlag { CacheNone, CacheBackground }`
- `enum DragMode { NoDrag, ScrollHandDrag, RubberBandDrag }`
- `enum OptimizationFlag { DontSavePainterState, DontAdjustForAntialiasing, IndirectPainting }`
- `flags OptimizationFlags`
- `enum ViewportAnchor { NoAnchor, AnchorViewCenter, AnchorUnderMouse }`
- `enum ViewportUpdateMode { FullViewportUpdate, MinimalViewportUpdate, SmartViewportUpdate, BoundingRectViewportUpdate, NoViewportUpdate }`

### 属性

- `alignment : Qt::Alignment`
- `backgroundBrush : QBrush`
- `cacheMode : CacheMode`
- `dragMode : DragMode`
- `foregroundBrush : QBrush`
- `interactive : bool`
- `optimizationFlags : OptimizationFlags`
- `renderHints : QPainter::RenderHints`
- `resizeAnchor : ViewportAnchor`
- `rubberBandSelectionMode : Qt::ItemSelectionMode`
- `sceneRect : QRectF`
- `transformationAnchor : ViewportAnchor`
- `viewportUpdateMode : ViewportUpdateMode`

### 公有函数

- `QGraphicsView(QWidget *parent = nullptr)`
- `QGraphicsView(QGraphicsScene *scene, QWidget *parent = nullptr)`
- `virtual ~QGraphicsView()`
- `Qt::Alignment alignment() const`
- `QBrush backgroundBrush() const`
- `QGraphicsView::CacheMode cacheMode() const`
- `void centerOn(const QPointF &pos)`
- `void centerOn(const QGraphicsItem *item)`
- `void centerOn(qreal x, qreal y)`
- `QGraphicsView::DragMode dragMode() const`
- `void ensureVisible(const QRectF &rect, int xmargin = 50, int ymargin = 50)`
- `void ensureVisible(const QGraphicsItem *item, int xmargin = 50, int ymargin = 50)`
- `void ensureVisible(qreal x, qreal y, qreal w, qreal h, int xmargin = 50, int ymargin = 50)`
- `void fitInView(const QRectF &rect, Qt::AspectRatioMode aspectRatioMode = Qt::IgnoreAspectRatio)`
- `void fitInView(const QGraphicsItem *item, Qt::AspectRatioMode aspectRatioMode = Qt::IgnoreAspectRatio)`
- `void fitInView(qreal x, qreal y, qreal w, qreal h, Qt::AspectRatioMode aspectRatioMode = Qt::IgnoreAspectRatio)`
- `QBrush foregroundBrush() const`
- `bool isInteractive() const`
- `bool isTransformed() const`
- `QGraphicsItem * itemAt(const QPoint &pos) const`
- `QGraphicsItem * itemAt(int x, int y) const`
- `QList<QGraphicsItem *> items() const`
- `QList<QGraphicsItem *> items(const QPoint &pos) const`
- `QList<QGraphicsItem *> items(int x, int y) const`
- `QList<QGraphicsItem *> items(int x, int y, int w, int h, Qt::ItemSelectionMode mode = Qt::IntersectsItemShape) const`
- `QList<QGraphicsItem *> items(const QPainterPath &path, Qt::ItemSelectionMode mode = Qt::IntersectsItemShape) const`
- `QList<QGraphicsItem *> items(const QPolygon &polygon, Qt::ItemSelectionMode mode = Qt::IntersectsItemShape) const`
- `QList<QGraphicsItem *> items(const QRect &rect, Qt::ItemSelectionMode mode = Qt::IntersectsItemShape) const`
- `QPainterPath mapFromScene(const QPainterPath &path) const`
- `QPoint mapFromScene(const QPointF &point) const`
- `QPolygon mapFromScene(const QPolygonF &polygon) const`
- `QPolygon mapFromScene(const QRectF &rect) const`
- `QPoint mapFromScene(qreal x, qreal y) const`
- `QPolygon mapFromScene(qreal x, qreal y, qreal w, qreal h) const`
- `QPainterPath mapToScene(const QPainterPath &path) const`
- `QPointF mapToScene(const QPoint &point) const`
- `QPolygonF mapToScene(const QPolygon &polygon) const`
- `QPolygonF mapToScene(const QRect &rect) const`
- `QPointF mapToScene(int x, int y) const`
- `QPolygonF mapToScene(int x, int y, int w, int h) const`
- `QGraphicsView::OptimizationFlags optimizationFlags() const`
- `void render(QPainter *painter, const QRectF &target = QRectF(), const QRect &source = QRect(), Qt::AspectRatioMode aspectRatioMode = Qt::KeepAspectRatio)`
- `QPainter::RenderHints renderHints() const`
- `void resetCachedContent()`
- `void resetTransform()`
- `QGraphicsView::ViewportAnchor resizeAnchor() const`
- `void rotate(qreal angle)`
- `QRect rubberBandRect() const`
- `Qt::ItemSelectionMode rubberBandSelectionMode() const`
- `void scale(qreal sx, qreal sy)`
- `QGraphicsScene * scene() const`
- `QRectF sceneRect() const`
- `void setAlignment(Qt::Alignment alignment)`
- `void setBackgroundBrush(const QBrush &brush)`
- `void setCacheMode(QGraphicsView::CacheMode mode)`
- `void setDragMode(QGraphicsView::DragMode mode)`
- `void setForegroundBrush(const QBrush &brush)`
- `void setInteractive(bool allowed)`
- `void setOptimizationFlag(QGraphicsView::OptimizationFlag flag, bool enabled = true)`
- `void setOptimizationFlags(QGraphicsView::OptimizationFlags flags)`
- `void setRenderHint(QPainter::RenderHint hint, bool enabled = true)`
- `void setRenderHints(QPainter::RenderHints hints)`
- `void setResizeAnchor(QGraphicsView::ViewportAnchor anchor)`
- `void setRubberBandSelectionMode(Qt::ItemSelectionMode mode)`
- `void setScene(QGraphicsScene *scene)`
- `void setSceneRect(const QRectF &rect)`
- `void setSceneRect(qreal x, qreal y, qreal w, qreal h)`
- `void setTransform(const QTransform &matrix, bool combine = false)`
- `void setTransformationAnchor(QGraphicsView::ViewportAnchor anchor)`
- `void setViewportUpdateMode(QGraphicsView::ViewportUpdateMode mode)`
- `void shear(qreal sh, qreal sv)`
- `QTransform transform() const`
- `QGraphicsView::ViewportAnchor transformationAnchor() const`
- `void translate(qreal dx, qreal dy)`
- `QTransform viewportTransform() const`
- `QGraphicsView::ViewportUpdateMode viewportUpdateMode() const`

### 重实现的公有函数

- `virtual QVariant inputMethodQuery(Qt::InputMethodQuery query) const override`
- `virtual QSize sizeHint() const override`

### 公有槽函数

- `void invalidateScene(const QRectF &rect = QRectF(), QGraphicsScene::SceneLayers layers = QGraphicsScene::AllLayers)`
- `void updateScene(const QList<QRectF> &rects)`
- `void updateSceneRect(const QRectF &rect)`

### 信号

- `void rubberBandChanged(QRect rubberBandRect, QPointF fromScenePoint, QPointF toScenePoint)`

### 保护函数

- `virtual void drawBackground(QPainter *painter, const QRectF &rect)`
- `virtual void drawForeground(QPainter *painter, const QRectF &rect)`

### 重实现的保护函数

- `virtual void contextMenuEvent(QContextMenuEvent *event) override`
- `virtual void dragEnterEvent(QDragEnterEvent *event) override`
- `virtual void dragLeaveEvent(QDragLeaveEvent *event) override`
- `virtual void dragMoveEvent(QDragMoveEvent *event) override`
- `virtual void dropEvent(QDropEvent *event) override`
- `virtual bool event(QEvent *event) override`
- `virtual void focusInEvent(QFocusEvent *event) override`
- `virtual bool focusNextPrevChild(bool next) override`
- `virtual void focusOutEvent(QFocusEvent *event) override`
- `virtual void inputMethodEvent(QInputMethodEvent *event) override`
- `virtual void keyPressEvent(QKeyEvent *event) override`
- `virtual void keyReleaseEvent(QKeyEvent *event) override`
- `virtual void mouseDoubleClickEvent(QMouseEvent *event) override`
- `virtual void mouseMoveEvent(QMouseEvent *event) override`
- `virtual void mousePressEvent(QMouseEvent *event) override`
- `virtual void mouseReleaseEvent(QMouseEvent *event) override`
- `virtual void paintEvent(QPaintEvent *event) override`
- `virtual void resizeEvent(QResizeEvent *event) override`
- `virtual void scrollContentsBy(int dx, int dy) override`
- `virtual void showEvent(QShowEvent *event) override`
- `virtual bool viewportEvent(QEvent *event) override`
- `virtual void wheelEvent(QWheelEvent *event) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QGraphicsView::CacheModeFlagflags QGraphicsView::CacheMode`

**作用与语义：**

这个枚举描述了你可以为`QGraphicsView`的缓存模式设置的标志。
- `QGraphicsView::CacheNone`：`0x0`;所有绘画均直接在视窗上完成。
- `QGraphicsView::CacheBackground`：`0x1`;背景被缓存。这会影响自定义背景和基于`backgroundBrush`属性的背景。启用该标志后，`QGraphicsView`会分配一个视口完整大小的像素地图。
CacheMode 类型是 QFlags 的 typedef<CacheModeFlag>。它存储 CacheModeFlag 值的 OR 组合。

### `enum QGraphicsView::DragMode`

**作用与语义：**

该枚举描述了当鼠标在视口上按压并拖动时视图的默认动作。
- `QGraphicsView::NoDrag`：`0`;没有发生任何事;鼠标事件被忽略。
- `QGraphicsView::ScrollHandDrag`：`1`;光标变为指向的手指，拖动鼠标会滚动scrolbar。该模式兼容`interactive`和非交互模式。
- `QGraphicsView::RubberBandDrag`：`2`;会出现一根橡皮筋。拖动鼠标可设置橡皮筋几何形状，并选择橡皮筋覆盖的所有物品。非交互式视图禁用此模式。

### `enum QGraphicsView::OptimizationFlagflags QGraphicsView::OptimizationFlags`

**作用与语义：**

这个枚举描述了你可以启用以提升`QGraphicsView`渲染性能的标志。默认情况下，这些标志都没有被设置。注意，设置标志通常会带来副作用，而这种效果会因不同绘图设备和平台而异。
- `QGraphicsView::DontSavePainterState`：`0x1`;渲染时，`QGraphicsView`保护画家状态（见`QPainter::save()`），无论是渲染背景或前景，还是渲染每个物品时。这允许你让画家处于改变状态（即你可以调用`QPainter::setPen()`或`QPainter::setBrush()`，但绘制后无需恢复状态）。但如果物品持续恢复状态，应启用该标志以防止`QGraphicsView`同样恢复。
- `QGraphicsView::DontAdjustForAntialiasing`：`0x2`;禁用`QGraphicsView`对已曝光区域的抗锯齿自动调整功能。在`QGraphicsItem::boundingRect()`边界上渲染抗锯齿线条的物品，可能会渲染线条的部分区域。为防止渲染伪影，`QGraphicsView`会将所有暴露区域向所有方向扩展2像素。启用该标志后，`QGraphicsView`将不再执行这些调整，减少需要重绘的区域，从而提升性能。一个常见副作用是，使用抗锯齿绘制的物品在移动时可能会在场景中留下绘画痕迹。
- `QGraphicsView::IndirectPainting`：`0x4`;自Qt 4.6起，恢复调用QGraphicsView：:d rawItems()和QGraphicsScene：:d rawItems()的旧绘画算法。仅用于兼容旧代码。
OptimizationFlags 类型是 QFlags 的 typedef<OptimizationFlag>。它存储 OptimizationFlag 值的 OR 组合。

### `enum QGraphicsView::ViewportAnchor`

**作用与语义：**

这些枚举描述了当用户调整视图大小或转换视图时`QGraphicsView`可能使用的锚点。
- `QGraphicsView::NoAnchor`：`0`;无锚点，即视角保持场景位置不变。
- `QGraphicsView::AnchorViewCenter`：`1`;视角中心的场景点作为锚点。
- `QGraphicsView::AnchorUnderMouse`：`2`;鼠标下方的点作为锚点。

### `enum QGraphicsView::ViewportUpdateMode`

**作用与语义：**

该枚举描述了当场景内容发生变化或暴露时，`QGraphicsView`如何更新视口。
- `QGraphicsView::FullViewportUpdate`：`0`;当场景中任何可见部分发生变化或重新曝光时，`QGraphicsView`会更新整个视口。当`QGraphicsView`花更多时间思考绘制内容时（例如，许多小项目被反复更新），这种方法最快。这是不支持部分更新的视口（如`QOpenGLWidget`）和需要禁用滚动优化的视口的首选更新模式。
- `QGraphicsView::MinimalViewportUpdate`：`1`;`QGraphicsView`会确定需要重绘的最小视口区域，通过避免重绘未变区域，从而减少绘制时间。这是`QGraphicsView`的默认模式。虽然这种方法总体性能最佳，但如果场景中有许多细微可见的变化，`QGraphicsView`可能会花在寻找最小方法上的时间超过绘制时间。
- `QGraphicsView::SmartViewportUpdate`：`2`;`QGraphicsView` 会通过分析需要重绘的区域来尝试找到最优的更新模式。
- `QGraphicsView::BoundingRectViewportUpdate`：`4`;视口中所有变化的边界矩形将被重新绘制。该模式的优点是`QGraphicsView`只搜索一个区域进行变化，从而减少判断需要重绘区域的时间。缺点是未改变的区域也需要重新绘制。
- `QGraphicsView::NoViewportUpdate`：`3`;场景变化时`QGraphicsView`永远不会更新视口;用户需要控制所有更新。该模式在`QGraphicsView`禁用所有（可能较慢的）物品可见性测试，适用于需要固定帧率或视口外部更新的场景。

### `alignment : Qt::Alignment`

**作用与语义：**

该属性表示了当整个场景可见时，场景在视图中的对齐。
如果整个场景在视图中可见（即没有可见的滚动条），视图的对齐将决定场景在视图中渲染的位置。例如，如果对齐是`Qt::AlignCenter`（默认），场景会置中，如果对齐是（`Qt::AlignLeft` |`Qt::AlignTop`），场景将渲染在视图的左上角。

**如何使用：** 调用 `alignment()` 读取当前值；它不会修改应用状态。

### `backgroundBrush : QBrush`

**作用与语义：**

该属性保留场景的背景画笔。
该属性为该视图中场景设置背景画刷。它用于覆盖场景自身背景，并定义`drawBackground()`的行为。为了为该视图提供自定义背景绘图，你可以重新实现`drawBackground()`。
默认情况下，该属性包含带有`Qt::NoBrush`图案的画刷。

**如何使用：** 调用 `backgroundBrush()` 读取当前值；它不会修改应用状态。

### `cacheMode : CacheMode`

**作用与语义：**

该属性决定了视图中哪些部分被缓存。
`QGraphicsView`可以缓存预渲染内容在`QPixmap`中，然后绘制到视口上。此类缓存的目的是加快渲染慢区域的总渲染时间。例如，纹理、渐变和alpha混合背景渲染速度可能明显较慢;尤其是在变换视图时。`CacheBackground`标志使视图背景能够缓存。例如：
每次视图被转换时，缓存都会被废除。然而，在滚动时，只需部分失效。
默认情况下，没有缓存。

**如何使用：** 调用 `cacheMode()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 QGraphicsView view;
 view.setBackgroundBrush(QImage(":/images/backgroundtile.png"));
 view.setCacheMode(QGraphicsView::CacheBackground);
```

### `dragMode : DragMode`

**作用与语义：**

该属性保留了在按下左键时拖动鼠标在场景上的行为。
该属性定义了用户点击场景背景并拖动鼠标时应发生的操作（例如，使用指针光标滚动视口内容，或用橡皮筋选择多个项目）。默认值`NoDrag`不起作用。
这种行为只影响未被任何项目处理的鼠标点击。你可以通过创建`QGraphicsView`子类并重新实现`mouseMoveEvent()`来定义自定义行为。

**如何使用：** 调用 `dragMode()` 读取当前值；它不会修改应用状态。

### `foregroundBrush : QBrush`

**作用与语义：**

该属性保留了场景的前景画笔。
该属性为该视图中场景设置前景画笔。它用于覆盖场景自身的前景，并定义`drawForeground()`的行为。为了为该视图提供自定义前景绘制，你可以重新实现`drawForeground()`。
默认情况下，该属性包含带有`Qt::NoBrush`图案的画刷。

**如何使用：** 调用 `foregroundBrush()` 读取当前值；它不会修改应用状态。

### `interactive : bool`

**作用与语义：**

该属性是否允许场景交互。
启用时，该视图设置为允许场景交互。否则，该视图不允许交互，鼠标或按键事件被忽略（即只读视图）。
默认情况下，该属性为`true`。

**如何使用：** 调用 `interactive()` 读取当前值；它不会修改应用状态。

### `optimizationFlags : OptimizationFlags`

**作用与语义：**

这些标志可以用来调节`QGraphicsView`的性能。
`QGraphicsView` 使用裁剪、额外的边界矩形调整以及其他一些辅助工具，以提升常见图形场景的渲染质量和性能。然而，根据目标平台、场景和所使用的视口，这些操作可能会降低性能。
效果因标志而异;详情请参见`OptimizationFlags`文档。
默认情况下，没有启用任何最佳化标志。

**如何使用：** 调用 `optimizationFlags()` 读取当前值；它不会修改应用状态。

### `renderHints : QPainter::RenderHints`

**作用与语义：**

该属性包含视图的默认渲染提示。
这些提示用于在绘制每个可见物品前初始化`QPainter`。`QPainter` 使用渲染提示切换渲染功能，如抗锯齿和平滑像素映射转换。
`QPainter::TextAntialiasing`默认是启用的。

**如何使用：** 调用 `renderHints()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 QGraphicsScene scene;
 scene.addRect(QRectF(-10, -10, 20, 20));

 QGraphicsView view(&scene);
 view.setRenderHints(QPainter::Antialiasing | QPainter::SmoothPixmapTransform);
 view.show();
```

### `resizeAnchor : ViewportAnchor`

**作用与语义：**

视角在调整视角大小时应该如何定位场景。
`QGraphicsView` 利用该属性决定当视口小部件大小变化时，场景在视口中的位置。默认行为`NoAnchor`在调整大小时场景位置保持不变;调整大小时，视图左上角看起来是锚定的。
注意，当场景仅可见部分区域（即有滚动条时），该特性的影响尤为明显。否则，如果整个场景都能放入视图，`QGraphicsScene` 会利用视图对齐来将场景定位于视图中。

**如何使用：** 调用 `resizeAnchor()` 读取当前值；它不会修改应用状态。

### `rubberBandSelectionMode : Qt::ItemSelectionMode`

**作用与语义：**

该属性支持选择带有橡皮筋选择矩形的物品。
该属性定义了使用`RubberBandDrag`拖拽模式时如何选择物品。
默认值为`Qt::IntersectsItemShape`;选择所有形状与橡皮筋相交或被橡皮筋包围的物品。

**如何使用：** 调用 `rubberBandSelectionMode()` 读取当前值；它不会修改应用状态。

### `sceneRect : QRectF`

**作用与语义：**

该属性包含了该视图所显示的场景面积。
场景矩形定义了场景的范围，在视图中，这意味着你可以通过滚动条导航的场景区域。
如果未设置，或者设置了空`QRectF`，该属性与`QGraphicsScene::sceneRect`值相同，且随`QGraphicsScene::sceneRect`变化。否则，视图的场景矩形不受场景影响。
注意，尽管场景支持几乎无限大小，但滚动条的范围永远不会超过整数（INT_MIN、INT_MAX）。当场景大于滚动条值时，你可以选择使用`translate()`来导航场景。
默认情况下，该属性在原点包含一个宽度和高度均为零的矩形。

**如何使用：** 调用 `sceneRect()` 读取当前值；它不会修改应用状态。

### `transformationAnchor : ViewportAnchor`

**作用与语义：**

视角在变换过程中应如何定位场景。
`QGraphicsView`利用该特性决定当变换矩阵变化、视角坐标系变换时，场景在视口中的位置。默认行为`AnchorViewCenter`确保场景中心点在变换过程中保持不变（例如，旋转时场景看起来会围绕视角中心旋转）。
注意，当场景仅可见部分区域（即有滚动条时），该特性的影响尤为明显。否则，如果整个场景都能放入视图，`QGraphicsScene`会利用视图对齐来将场景定位于视图中。

**如何使用：** 调用 `transformationAnchor()` 读取当前值；它不会修改应用状态。

### `viewportUpdateMode : ViewportUpdateMode`

**作用与语义：**

视口应如何更新其内容。
`QGraphicsView` 利用该属性决定如何更新场景中被重新曝光或更改的区域。通常你不需要修改这个属性，但在某些情况下修改可以提升渲染性能。具体细节请参见`ViewportUpdateMode`文档。
默认值是`MinimalViewportUpdate`，当内容变化时，会尽量`QGraphicsView`更新视口的最小区域。

**如何使用：** 调用 `viewportUpdateMode()` 读取当前值；它不会修改应用状态。

### `QGraphicsView::QGraphicsView(QWidget *parent = nullptr)`

**作用与语义：**

构造一个QGraphicsView。`parent`传递给`QWidget`的构造器。

### `QGraphicsView::QGraphicsView(QGraphicsScene *scene, QWidget *parent = nullptr)`

**作用与语义：**

构建一个QGraphicsView，并将可视化场景设置为`scene`。`parent`传递给`QWidget`的构造器。

### `[virtual noexcept] QGraphicsView::~QGraphicsView()`

**作用与语义：**

摧毁`QGraphicsView`物体。

### `void QGraphicsView::centerOn(const QPointF &pos)`

**作用与语义：**

滚动视口内容，确保场景坐标`pos`在视图中居中。
由于`pos`是浮点坐标，而滚动条作用于整数坐标，中心化只是近似值。
注意：如果物品靠近或超出边界，它会在视图中可见，但不会居中。

### `void QGraphicsView::centerOn(const QGraphicsItem *item)`

**作用与语义：**

滚动视口内容，确保`item`在视野中居中。

### `void QGraphicsView::centerOn(qreal x, qreal y)`

**作用与语义：**

该函数是为了方便而提供。它等同于调用 centerOn（`QPointF`（`x`， `y`））。

### `[override virtual protected] void QGraphicsView::contextMenuEvent(QContextMenuEvent *event)`

**作用与语义：**

重实现自：`QAbstractScrollArea::contextMenuEvent`（QContextMenuEvent *e）。

### `[override virtual protected] void QGraphicsView::dragEnterEvent(QDragEnterEvent *event)`

**作用与语义：**

重实现自：`QAbstractScrollArea::dragEnterEvent`（QDragEnterEvent *event）。

### `[override virtual protected] void QGraphicsView::dragLeaveEvent(QDragLeaveEvent *event)`

**作用与语义：**

重实现自：`QAbstractScrollArea::dragLeaveEvent`（QDragLeaveEvent *event）。

### `[override virtual protected] void QGraphicsView::dragMoveEvent(QDragMoveEvent *event)`

**作用与语义：**

重实现自：`QAbstractScrollArea::dragMoveEvent`（QDragMoveEvent *event）。

### `[virtual protected] void QGraphicsView::drawBackground(QPainter *painter, const QRectF &rect)`

**作用与语义：**

在绘制任何物品和前景之前，使用`painter`绘制场景背景。重新实现该函数，为该视图提供自定义背景。
如果你只是想为背景定义颜色、纹理或渐变，可以调用`setBackgroundBrush()`。
所有绘画都是在场景坐标中完成的。`rect`是裸露的矩形。
默认实现会用视图的 `backgroundBrush` 填充`rect`。如果没有定义这样的画刷（默认），则调用场景的 drawBackground() 函数。

### `[virtual protected] void QGraphicsView::drawForeground(QPainter *painter, const QRectF &rect)`

**作用与语义：**

在绘制完背景和所有物品后，使用`painter`绘制场景前景。重新实现该函数，为该视图提供自定义前景。
如果你只是想为前景定义颜色、纹理或渐变，可以调用`setForegroundBrush()`。
所有绘画都是在场景坐标中完成的。`rect`是裸露的矩形。
默认实现会用视图的 `foregroundBrush` 填充`rect`。如果没有定义这样的画刷（默认），则调用场景的 drawForeground() 函数。

### `[override virtual protected] void QGraphicsView::dropEvent(QDropEvent *event)`

**作用与语义：**

重实现自：`QAbstractScrollArea::dropEvent`（QDropEvent *事件）。

### `void QGraphicsView::ensureVisible(const QRectF &rect, int xmargin = 50, int ymargin = 50)`

**作用与语义：**

滚动视口内容，使场景矩形`rect`可见，边距以像素为单位`xmargin`和`ymargin`。如果无法到达指定的矩形，则将内容滚动至最近的有效位置。两个边距的默认值为50像素。

### `void QGraphicsView::ensureVisible(const QGraphicsItem *item, int xmargin = 50, int ymargin = 50)`

**作用与语义：**

滚动视口内容，使物品`item`中心可见，边距以像素为单位`xmargin`和`ymargin`。如果无法到达指定点，内容会滚动到最近的有效位置。两个边距的默认值为50像素。

### `void QGraphicsView::ensureVisible(qreal x, qreal y, qreal w, qreal h, int xmargin = 50, int ymargin = 50)`

**作用与语义：**

该函数仅为方便而提供。它等同于调用 ensureVisible（`QRectF`（`x`， `y`， `w`， `h`）， `xmargin`， `ymargin`）。

### `[override virtual protected] bool QGraphicsView::event(QEvent *event)`

**作用与语义：**

重装：`QAbstractScrollArea::event`（QEvent *事件）。

### `void QGraphicsView::fitInView(const QRectF &rect, Qt::AspectRatioMode aspectRatioMode = Qt::IgnoreAspectRatio)`

**作用与语义：**

缩放视图矩阵并滚动滚动条，确保场景矩形`rect`嵌入视口内。`rect`必须位于场景矩形内部;否则，fitInView() 无法保证整个矩形都可见。
该函数保持视野的旋转、平移或剪切。视角根据`aspectRatioMode`进行缩放。如果视角不紧密，`rect`将置中。
通常会在`resizeEvent()`的重实现中调用 fitInView()，以确保整个场景或场景部分随着视角调整大小自动缩放以适应新的视口大小。不过请注意，如果新变换切换了滚动条的自动状态，从`resizeEvent()`调用 fitInView() 可能会导致不必要的缩放递归。你可以将滚动条策略切换为始终开启或关闭，以防止这种情况（参见`horizontalScrollBarPolicy()`和`verticalScrollBarPolicy()`）。
如果`rect`空，或者视口太小，这个函数就不会有任何作用。

### `void QGraphicsView::fitInView(const QGraphicsItem *item, Qt::AspectRatioMode aspectRatioMode = Qt::IgnoreAspectRatio)`

**作用与语义：**

确保`item`紧密嵌入视图内，并根据视野`aspectRatioMode`比例缩放。

### `void QGraphicsView::fitInView(qreal x, qreal y, qreal w, qreal h, Qt::AspectRatioMode aspectRatioMode = Qt::IgnoreAspectRatio)`

**作用与语义：**

该便利函数等价于调用 fitInView（`QRectF`（`x`， `y`， `w`， `h`）， `aspectRatioMode`）。

### `[override virtual protected] void QGraphicsView::focusInEvent(QFocusEvent *event)`

**作用与语义：**

重实现自：`QWidget::focusInEvent`（QFocusEvent *event）。
该事件处理程序可以在子类中重新实现，以接收控件的键盘焦点事件（焦点接收）。事件通过`event`参数传递。
小部件通常必须`setFocusPolicy()`到非`Qt::NoFocus`的对象才能接收焦点事件。（注意，应用程序员可以调用任何小部件`setFocus()`，即使是那些通常不接受焦点的小部件。）。
默认实现会更新小部件（除非是没有指定`focusPolicy()`的窗口）。

### `[override virtual protected] bool QGraphicsView::focusNextPrevChild(bool next)`

**作用与语义：**

重构：`QWidget::focusNextPrevChild`（下一个布尔）。
根据 Tab 和 Shift Tab 找到一个新的控件来给键盘焦点，如果能找到新控件，则返回 `true`，找不到则返回 false。
如果`next`为真，该函数向前搜索;如果`next`为假，则向后搜索。
有时，你会想重新实现这个函数。例如，浏览器可能会重新实现它，将“当前活跃链接”向前或向后移动，只有当它到达“页面”的最后或第一个链接时才调用 focusNextPrevChild()。
子控件调用其父控件的 focusNextPrevChild()，但只有包含子控件的窗口决定将焦点重定向到哪里。通过重新实现该函数，你就能控制所有子控件的焦点遍历。

### `[override virtual protected] void QGraphicsView::focusOutEvent(QFocusEvent *event)`

**作用与语义：**

重现：`QWidget::focusOutEvent`（QFocusEvent *event）。
该事件处理程序可以在子类中重新实现，以接收控件的键盘焦点事件（焦点丢失）。事件通过`event`参数传递。
小部件通常必须`setFocusPolicy()`到非`Qt::NoFocus`的对象才能接收焦点事件。（注意，应用程序员可以调用任何小部件`setFocus()`，即使是那些通常不接受焦点的小部件。）。
默认实现会更新小部件（除非是没有指定`focusPolicy()`的窗口）。

### `[override virtual protected] void QGraphicsView::inputMethodEvent(QInputMethodEvent *event)`

**作用与语义：**

重实现自：`QWidget::inputMethodEvent`（QInputMethodEvent *event）。
对于事件`event`，该事件处理程序可以被重新实现到子类中以接收输入法组合事件。当输入方法的状态发生变化时，调用该处理程序。
注意，在创建自定义文本编辑小部件时，必须明确设置`Qt::WA_InputMethodEnabled`窗口属性（使用`setAttribute()`函数），才能接收输入法事件。
默认实现调用 event->ignore()，拒绝输入法事件。详情请参见 `QInputMethodEvent` 文档。

### `[override virtual] QVariant QGraphicsView::inputMethodQuery(Qt::InputMethodQuery query) const`

**作用与语义：**

重实现自：`QWidget::inputMethodQuery`（Qt：：InputMethodQuery query） const.
该方法仅适用于输入控件。输入方法用于查询控件的一组属性，以支持复杂的输入法操作，以支持周围文本和重新转换。
`query` 指定查询的属性。

### `[slot] void QGraphicsView::invalidateScene(const QRectF &rect = QRectF(), QGraphicsScene::SceneLayers layers = QGraphicsScene::AllLayers)`

**作用与语义：**

`rect` 内`layers`失效并调度重绘。`rect` 处于场景坐标内。`rect` 内任何缓存内容`layers`都会无条件失效并重新绘制。
你可以调用这个函数来通知`QGraphicsView`场景背景或前景的变化。它通常用于基于瓦片背景的场景，以便在启用背景缓存时通知`QGraphicsView`发生变化。
注意`QGraphicsView`目前仅支持后台缓存（参见 `QGraphicsView::CacheBackground`）。该函数等同于调用 `update()`，如果传递的是除 `QGraphicsScene::BackgroundLayer` 以外的任何层。

### `bool QGraphicsView::isTransformed() const`

**作用与语义：**

如果视图被变换（即被分配了非恒等变换，或滚动条被调整），返回`true`。

### `QGraphicsItem *QGraphicsView::itemAt(const QPoint &pos) const`

**作用与语义：**

返回位于视口坐标中的位置`pos`的物品。如果该位置有多个物品，该函数返回最顶的物品。

**官方示例：**

```cpp
 void CustomView::mousePressEvent(QMouseEvent *event)
 {
     if (QGraphicsItem *item = itemAt(event->pos())) {
         qDebug() << "You clicked on item" << item;
     } else {
         qDebug("You didn't click on an item.");
     }
 }
```

### `QGraphicsItem *QGraphicsView::itemAt(int x, int y) const`

**作用与语义：**

该函数为方便而提供。它等价于调用itemAt（`QPoint`（`x`， `y`））。

### `QList<QGraphicsItem *> QGraphicsView::items() const`

**作用与语义：**

返回相关场景中所有物品的列表，按递减堆叠顺序返回（即返回列表中的第一个物品是最上面的物品）。

### `QList<QGraphicsItem *> QGraphicsView::items(const QPoint &pos) const`

**作用与语义：**

返回视图中`pos`位置的所有物品列表。物品按递减排列顺序排列（即列表中第一个为最上项，最后为最底项）。`pos`位于视口坐标内。
该函数最常在`QGraphicsView`子类的鼠标事件处理程序中调用。`pos` 位于未变换的视口坐标中，就像`QMouseEvent::position()`一样。

**官方示例：**

```cpp
 void CustomView::mousePressEvent(QMouseEvent *event)
 {
     qDebug() << "There are" << items(event->pos()).size()
              << "items at position" << mapToScene(event->pos());
 }
```

### `QList<QGraphicsItem *> QGraphicsView::items(int x, int y) const`

**作用与语义：**

该函数是为了方便而提供的。它等同于调用 items（`QPoint`（`x`， `y`））。

### `QList<QGraphicsItem *> QGraphicsView::items(int x, int y, int w, int h, Qt::ItemSelectionMode mode = Qt::IntersectsItemShape) const`

**作用与语义：**

这个便捷函数等同于调用 items(`QRectF`(`x`, `y`, `w`, `h`), `mode`)。

### `QList<QGraphicsItem *> QGraphicsView::items(const QPainterPath &path, Qt::ItemSelectionMode mode = Qt::IntersectsItemShape) const`

**作用与语义：**

返回所有根据`mode`包含或与`path`相交的项目列表。`path`处于视口坐标内。
`mode`的默认值为`Qt::IntersectsItemShape`;所有与`path`相交或包含的具体形状的项都会返回。

### `QList<QGraphicsItem *> QGraphicsView::items(const QPolygon &polygon, Qt::ItemSelectionMode mode = Qt::IntersectsItemShape) const`

**作用与语义：**

返回所有根据`mode`包含或与`polygon`相交的项目列表。`polygon`处于视口坐标内。
`mode`的默认值为`Qt::IntersectsItemShape`;所有与`polygon`相交或包含的具体形状的项都会返回。
这些项按递减堆叠顺序排序（即返回列表中的第一个项是最上面的项）。

### `QList<QGraphicsItem *> QGraphicsView::items(const QRect &rect, Qt::ItemSelectionMode mode = Qt::IntersectsItemShape) const`

**作用与语义：**

返回所有根据`mode`包含或与`rect`相交的项目列表。`rect`位于视口坐标内。
`mode`的默认值为`Qt::IntersectsItemShape`;所有与 相交或被 包含在 `rect` 的精确形状的项都将返回。
这些项目按递减堆叠顺序排序（即返回列表中的第一个项目是最上面的）。

### `[override virtual protected] void QGraphicsView::keyPressEvent(QKeyEvent *event)`

**作用与语义：**

处理按键事件 `event`，默认实现负责场景、焦点图元以及视图自身的导航行为。子类可拦截自定义按键；不处理时必须调用基类实现，否则标准编辑或场景键盘操作会失效。

### `[override virtual protected] void QGraphicsView::keyReleaseEvent(QKeyEvent *event)`

**作用与语义：**

重实现自：`QWidget::keyReleaseEvent`（QKeyEvent *event）。
该事件处理程序用于事件`event`，可以在子类中重新实现，以接收该小部件的密钥释放事件。
小部件必须先接受焦点并拥有焦点，才能接收密钥释放事件。
如果你重新实现这个处理器，如果你不对密钥进行操作，务必调用基类实现。
默认实现忽略事件，以便小部件的父节点能够解释事件。
注意`QKeyEvent`以 isAccepted() == true开头，所以你不需要调用`QKeyEvent::accept()`——只要你对密钥操作时不要调用基类实现即可。

### `QPainterPath QGraphicsView::mapFromScene(const QPainterPath &path) const`

**作用与语义：**

返回场景坐标画家路径`path`到视口坐标画师路径。

### `QPoint QGraphicsView::mapFromScene(const QPointF &point) const`

**作用与语义：**

将场景坐标`point`返回到视口坐标。

### `QPolygon QGraphicsView::mapFromScene(const QPolygonF &polygon) const`

**作用与语义：**

将场景坐标多边形`polygon`返回到视口坐标多边形。

### `QPolygon QGraphicsView::mapFromScene(const QRectF &rect) const`

**作用与语义：**

将场景矩形返回`rect`视口坐标多边形。

### `QPoint QGraphicsView::mapFromScene(qreal x, qreal y) const`

**作用与语义：**

该函数是为了方便而提供。它等同于调用 mapFromScene（`QPointF`（`x`， `y`））。

### `QPolygon QGraphicsView::mapFromScene(qreal x, qreal y, qreal w, qreal h) const`

**作用与语义：**

该函数是为了方便而提供的。它等同于调用 mapFromScene（`QRectF`（`x`， `y`， `w`， `h`））。

### `QPainterPath QGraphicsView::mapToScene(const QPainterPath &path) const`

**作用与语义：**

返回视口绘画路径`path`映射到场景坐标绘画路径。

### `QPointF QGraphicsView::mapToScene(const QPoint &point) const`

**作用与语义：**

返回视口坐标`point`映射到场景坐标。
注意：将像素覆盖的整个矩形映射在`point`处，而不是点本身，这样很有用。为此，你可以调用 mapToScene（`QRect`（`point`， `QSize`（2， 2）））。

### `QPolygonF QGraphicsView::mapToScene(const QPolygon &polygon) const`

**作用与语义：**

返回映射到场景坐标多边形`polygon`视口多边形。

### `QPolygonF QGraphicsView::mapToScene(const QRect &rect) const`

**作用与语义：**

返回视口矩形`rect`映射到场景坐标多边形。

### `QPointF QGraphicsView::mapToScene(int x, int y) const`

**作用与语义：**

该函数是为方便而提供的。它等同于调用 mapToScene（`QPoint`（`x`， `y`））。

### `QPolygonF QGraphicsView::mapToScene(int x, int y, int w, int h) const`

**作用与语义：**

该函数是为了方便而提供。它等同于调用 mapToScene（`QRect`（`x`， `y`， `w`， `h`））。

### `[override virtual protected] void QGraphicsView::mouseDoubleClickEvent(QMouseEvent *event)`

**作用与语义：**

重实现自：`QAbstractScrollArea::mouseDoubleClickEvent`（QMouseEvent *e）。

### `[override virtual protected] void QGraphicsView::mouseMoveEvent(QMouseEvent *event)`

**作用与语义：**

重实现自：`QAbstractScrollArea::mouseMoveEvent`（QMouseEvent *e）。

### `[override virtual protected] void QGraphicsView::mousePressEvent(QMouseEvent *event)`

**作用与语义：**

重实现自：`QAbstractScrollArea::mousePressEvent`（QMouseEvent *e）。

### `[override virtual protected] void QGraphicsView::mouseReleaseEvent(QMouseEvent *event)`

**作用与语义：**

重实现自：`QAbstractScrollArea::mouseReleaseEvent`（QMouseEvent *e）。

### `[override virtual protected] void QGraphicsView::paintEvent(QPaintEvent *event)`

**作用与语义：**

重实现自：`QAbstractScrollArea::paintEvent`（QPaintEvent *event）。

### `void QGraphicsView::render(QPainter *painter, const QRectF &target = QRectF(), const QRect &source = QRect(), Qt::AspectRatioMode aspectRatioMode = Qt::KeepAspectRatio)`

**作用与语义：**

利用`painter`将视图坐标中的`source`矩形矩形渲染到绘图设备坐标中的`target`。该函数用于将视图内容捕获到绘图设备，如`QImage`（例如截图），或打印到QPrinter。例如：
如果`source`是空矩形，该函数会用`viewport()`->`rect()`来决定绘制什么。如果`target`是空矩形矩形，则使用`painter`的绘图设备的完整尺寸（例如，对于QPrinter，页面大小）。
源矩形块内容会根据`aspectRatioMode`进行变换以适应目标矩形块。默认情况下，保持宽高比，`source`会按比例缩放以适应`target`。

**官方示例：**

```cpp
 QGraphicsScene scene;
 scene.addItem(...
 ...

 QGraphicsView view(&scene);
 view.show();
 ...

 QPrinter printer(QPrinter::HighResolution);
 printer.setPageSize(QPrinter::A4);
 QPainter painter(&printer);

 // print, fitting the viewport contents into a full page
 view.render(&painter);

 // print the upper half of the viewport into the lower.
 // half of the page.
 QRect viewport = view.viewport()->rect();
 view.render(&painter,
             QRectF(0, printer.height() / 2,
                    printer.width(), printer.height() / 2),
             viewport.adjusted(0, 0, 0, -viewport.height() / 2));
```

### `void QGraphicsView::resetCachedContent()`

**作用与语义：**

重置所有缓存内容。调用该函数会清除`QGraphicsView`的缓存。如果当前缓存模式为`CacheNone`，该函数不起作用。
当`backgroundBrush`或`QGraphicsScene::backgroundBrush`属性发生变化时，这个函数会自动调用;只有当你重新实现了`QGraphicsScene::drawBackground()`或`QGraphicsView::drawBackground()`来绘制自定义背景，并且需要触发一次完整的重绘时，才需要调用这个函数。

### `void QGraphicsView::resetTransform()`

**作用与语义：**

将视图变换重置为恒来矩阵。

### `[override virtual protected] void QGraphicsView::resizeEvent(QResizeEvent *event)`

**作用与语义：**

重实现自：`QAbstractScrollArea::resizeEvent`（QResizeEvent *event）。

### `void QGraphicsView::rotate(qreal angle)`

**作用与语义：**

顺时针旋转当前视角变换`angle`度。

### `[signal] void QGraphicsView::rubberBandChanged(QRect rubberBandRect, QPointF fromScenePoint, QPointF toScenePoint)`

**作用与语义：**

当更换橡皮筋rect时，该信号会发出。视口Rect由`rubberBandRect`指定。拖动起始位置和拖止位置在场景点中提供`fromScenePoint`和`toScenePoint`。
当橡皮筋选择结束时，该信号将以零值发出。

### `QRect QGraphicsView::rubberBandRect() const`

**作用与语义：**

如果用户当前用橡皮筋进行物品选择，该函数会返回当前橡皮筋区域（视口坐标）。当用户未使用橡皮筋时，该函数返回（空）QRectF()。
注意，这个`QRect`的部分可以位于视觉视口之外。它可以包含例如负值。

### `void QGraphicsView::scale(qreal sx, qreal sy)`

**作用与语义：**

将当前视图变换比例放大为（`sx`，`sy`）。

### `QGraphicsScene *QGraphicsView::scene() const`

**作用与语义：**

返回当前视图中可视化场景的指针。如果当前没有可视化场景，则返回`nullptr`。

### `[override virtual protected] void QGraphicsView::scrollContentsBy(int dx, int dy)`

**作用与语义：**

重实现自：`QAbstractScrollArea::scrollContentsBy`（智力 dx，智力 dy）。
当滚动条被移动`dx`、`dy`时调用，因此视口内容应相应滚动。
默认实现只需调用整个`viewport()`的`update()`，子类可以重新实现该处理程序以优化，或者像`QScrollArea`一样移动内容控件。参数`dx`和`dy`是为了方便，让类知道应该滚动多少（比如像素移动时很有用）。你也可以忽略这些值，直接滚动到滚动条指示的位置。
调用该函数进行程序滚动是错误，建议使用滚动条（例如直接调用`QScrollBar::setValue()`）。

### `void QGraphicsView::setOptimizationFlag(QGraphicsView::OptimizationFlag flag, bool enabled = true)`

**作用与语义：**

如果`enabled`为真，则启用`flag`;否则禁用`flag`。

### `void QGraphicsView::setRenderHint(QPainter::RenderHint hint, bool enabled = true)`

**作用与语义：**

如果`enabled`为真，渲染提示`hint`启用;否则禁用。

### `void QGraphicsView::setScene(QGraphicsScene *scene)`

**作用与语义：**

将当前场景设置为`scene`。如果已经在观看`scene`，这个函数就不做任何事。
当场景设置在一个视图上时，`QGraphicsScene::changed()`信号会自动连接到该视图的`updateScene()`槽，视图的滚动条也会根据场景大小进行调整。
该观点并不拥有`scene`。

### `void QGraphicsView::setTransform(const QTransform &matrix, bool combine = false)`

**作用与语义：**

将视图的电流变换矩阵设置为`matrix`。
如果`combine`为真，则`matrix`与当前矩阵结合;否则，`matrix`替换当前矩阵。`combine`默认为假。
变换矩阵将场景转换为视角坐标。使用由恒等矩阵提供的默认变换，视野中的一个像素代表场景中的一个单元（例如，一个10x10矩形物体使用视图中的10x10像素绘制）。如果应用2x2缩放矩阵，场景将以1：2绘制（例如，10x10矩形物体则使用视图中的20x20像素绘制）。
为了简化使用变换视图与物品的交互，`QGraphicsView` 提供了 mapTo... 和 mapFrom...这些函数可以在场景坐标和视图坐标之间转换。例如，你可以调用 `mapToScene()` 将视角坐标映射到浮点场景坐标，或者调用 `mapFromScene()` 将浮点场景坐标映射到视角坐标。

**官方示例：**

```cpp
 QGraphicsScene scene;
 scene.addText("GraphicsView rotated clockwise");

 QGraphicsView view(&scene);
 view.rotate(90); // the text is rendered with a 90 degree clockwise rotation
 view.show();
```

### `[override virtual protected slot] void QGraphicsView::setupViewport(QWidget *widget)`

**作用与语义：**

重实现自：`QAbstractScrollArea::setupViewport`（QWidget *viewport）。
`QAbstractScrollArea`在调用`setViewport()`后调用该槽位。在`QGraphicsView`的子类中重新实现该函数，以便在使用前初始化新的视口`widget`。
`QAbstractScrollArea`在调用`setViewport`（`viewport`）后调用该槽。在`QAbstractScrollArea`的子类中重构该函数，以在使用前初始化新`viewport`。

### `void QGraphicsView::shear(qreal sh, qreal sv)`

**作用与语义：**

将当前视图变换剪切为（`sh`， `sv`）。

### `[override virtual protected] void QGraphicsView::showEvent(QShowEvent *event)`

**作用与语义：**

重实现自：`QWidget::showEvent`（QShowEvent *event）。
该事件处理程序可以在子类中重新实现，以接收传递给 `event` 参数的控件显示事件。
非自发的展示事件会在展示前立即发送到小部件。窗口的自发展示事件则在展示之后交付。
注意：当窗口系统改变其映射状态时，小部件会接收自发显示和隐藏事件，例如用户最小化窗口时自发隐藏事件，窗口恢复时自发显示事件。收到自发隐藏事件后，小部件仍被视为`isVisible()`可见。

### `[override virtual] QSize QGraphicsView::sizeHint() const`

**作用与语义：**

重装：`QAbstractScrollArea::sizeHint()` const.

### `QTransform QGraphicsView::transform() const`

**作用与语义：**

返回视图的电流变换矩阵。如果未设置电流变换，则返回单位矩阵。

### `void QGraphicsView::translate(qreal dx, qreal dy)`

**作用与语义：**

将当前视图变换换为（`dx`， `dy`）。

### `[slot] void QGraphicsView::updateScene(const QList<QRectF> &rects)`

**作用与语义：**

安排场景矩形的更新 `rects`。

### `[slot] void QGraphicsView::updateSceneRect(const QRectF &rect)`

**作用与语义：**

通知`QGraphicsView`场景的 rect 发生了变化。`rect` 是新的场景 rect。如果视图已经有明确设置的场景 rect，这个函数就不做任何事。

### `[override virtual protected] bool QGraphicsView::viewportEvent(QEvent *event)`

**作用与语义：**

重实现自：`QAbstractScrollArea::viewportEvent`（QEvent *事件）。
滚动区域（`viewport()` 控件）的主事件处理程序。它处理指定的`event`，子类可以调用以提供合理的默认行为。
返回`true`表示事件系统事件已处理，无需进一步处理;否则返回`false`表示事件应继续传播。
你可以在子类中重新实现这个函数，但我们建议使用专门的事件处理程序。
视口事件的专用处理程序有：`paintEvent()`、`mousePressEvent()`、`mouseReleaseEvent()`、`mouseDoubleClickEvent()`、`mouseMoveEvent()`、`wheelEvent()`、`dragEnterEvent()`、`dragMoveEvent()`、`dragLeaveEvent()`、`dropEvent()`、`contextMenuEvent()`和`resizeEvent()`。

### `QTransform QGraphicsView::viewportTransform() const`

**作用与语义：**

返回一个矩阵，将场景坐标映射到视口坐标。

### `[override virtual protected] void QGraphicsView::wheelEvent(QWheelEvent *event)`

**作用与语义：**

重实现自：`QAbstractScrollArea::wheelEvent`（QWheelEvent *e）。

### `flags CacheMode`

**作用与语义：**

这个枚举描述了你可以为`QGraphicsView`的缓存模式设置的标志。
- `QGraphicsView::CacheNone`：`0x0`;所有绘画均直接在视窗上完成。
- `QGraphicsView::CacheBackground`：`0x1`;背景被缓存。这会影响自定义背景和基于`backgroundBrush`属性的背景。启用该标志后，`QGraphicsView`会分配一个视口完整大小的像素地图。
CacheMode 类型是 QFlags 的 typedef<CacheModeFlag>。它存储 CacheModeFlag 值的 OR 组合。

### `enum CacheModeFlag { CacheNone, CacheBackground }`

**作用与语义：**

这个枚举描述了你可以为`QGraphicsView`的缓存模式设置的标志。
- `QGraphicsView::CacheNone`：`0x0`;所有绘画均直接在视窗上完成。
- `QGraphicsView::CacheBackground`：`0x1`;背景被缓存。这会影响自定义背景和基于`backgroundBrush`属性的背景。启用该标志后，`QGraphicsView`会分配一个视口完整大小的像素地图。
CacheMode 类型是 QFlags 的 typedef<CacheModeFlag>。它存储 CacheModeFlag 值的 OR 组合。

### `enum OptimizationFlag { DontSavePainterState, DontAdjustForAntialiasing, IndirectPainting }`

**作用与语义：**

这个枚举描述了你可以启用以提升`QGraphicsView`渲染性能的标志。默认情况下，这些标志都没有被设置。注意，设置标志通常会带来副作用，而这种效果会因不同绘图设备和平台而异。
- `QGraphicsView::DontSavePainterState`：`0x1`;渲染时，`QGraphicsView`保护画家状态（见`QPainter::save()`），无论是渲染背景或前景，还是渲染每个物品时。这允许你让画家处于改变状态（即你可以调用`QPainter::setPen()`或`QPainter::setBrush()`，但绘制后无需恢复状态）。但如果物品持续恢复状态，应启用该标志以防止`QGraphicsView`同样恢复。
- `QGraphicsView::DontAdjustForAntialiasing`：`0x2`;禁用`QGraphicsView`对已曝光区域的抗锯齿自动调整功能。在`QGraphicsItem::boundingRect()`边界上渲染抗锯齿线条的物品，可能会渲染线条的部分区域。为防止渲染伪影，`QGraphicsView`会将所有暴露区域向所有方向扩展2像素。启用该标志后，`QGraphicsView`将不再执行这些调整，减少需要重绘的区域，从而提升性能。一个常见副作用是，使用抗锯齿绘制的物品在移动时可能会在场景中留下绘画痕迹。
- `QGraphicsView::IndirectPainting`：`0x4`;自Qt 4.6起，恢复调用QGraphicsView：:d rawItems()和QGraphicsScene：:d rawItems()的旧绘画算法。仅用于兼容旧代码。
OptimizationFlags 类型是 QFlags 的 typedef<OptimizationFlag>。它存储 OptimizationFlag 值的 OR 组合。

### `flags OptimizationFlags`

**作用与语义：**

这个枚举描述了你可以启用以提升`QGraphicsView`渲染性能的标志。默认情况下，这些标志都没有被设置。注意，设置标志通常会带来副作用，而这种效果会因不同绘图设备和平台而异。
- `QGraphicsView::DontSavePainterState`：`0x1`;渲染时，`QGraphicsView`保护画家状态（见`QPainter::save()`），无论是渲染背景或前景，还是渲染每个物品时。这允许你让画家处于改变状态（即你可以调用`QPainter::setPen()`或`QPainter::setBrush()`，但绘制后无需恢复状态）。但如果物品持续恢复状态，应启用该标志以防止`QGraphicsView`同样恢复。
- `QGraphicsView::DontAdjustForAntialiasing`：`0x2`;禁用`QGraphicsView`对已曝光区域的抗锯齿自动调整功能。在`QGraphicsItem::boundingRect()`边界上渲染抗锯齿线条的物品，可能会渲染线条的部分区域。为防止渲染伪影，`QGraphicsView`会将所有暴露区域向所有方向扩展2像素。启用该标志后，`QGraphicsView`将不再执行这些调整，减少需要重绘的区域，从而提升性能。一个常见副作用是，使用抗锯齿绘制的物品在移动时可能会在场景中留下绘画痕迹。
- `QGraphicsView::IndirectPainting`：`0x4`;自Qt 4.6起，恢复调用QGraphicsView：:d rawItems()和QGraphicsScene：:d rawItems()的旧绘画算法。仅用于兼容旧代码。
OptimizationFlags 类型是 QFlags 的 typedef<OptimizationFlag>。它存储 OptimizationFlag 值的 OR 组合。

### `Qt::Alignment alignment() const`

**作用与语义：**

该属性表示了当整个场景可见时，场景在视图中的对齐。
如果整个场景在视图中可见（即没有可见的滚动条），视图的对齐将决定场景在视图中渲染的位置。例如，如果对齐是`Qt::AlignCenter`（默认），场景会置中，如果对齐是（`Qt::AlignLeft` |`Qt::AlignTop`），场景将渲染在视图的左上角。

**如何使用：** 调用 `alignment()` 读取当前值；它不会修改应用状态。

### `QBrush backgroundBrush() const`

**作用与语义：**

该属性保留场景的背景画笔。
该属性为该视图中场景设置背景画刷。它用于覆盖场景自身背景，并定义`drawBackground()`的行为。为了为该视图提供自定义背景绘图，你可以重新实现`drawBackground()`。
默认情况下，该属性包含带有`Qt::NoBrush`图案的画刷。

**如何使用：** 调用 `backgroundBrush()` 读取当前值；它不会修改应用状态。

### `QGraphicsView::CacheMode cacheMode() const`

**作用与语义：**

该属性决定了视图中哪些部分被缓存。
`QGraphicsView`可以缓存预渲染内容在`QPixmap`中，然后绘制到视口上。此类缓存的目的是加快渲染慢区域的总渲染时间。例如，纹理、渐变和alpha混合背景渲染速度可能明显较慢;尤其是在变换视图时。`CacheBackground`标志使视图背景能够缓存。例如：
每次视图被转换时，缓存都会被废除。然而，在滚动时，只需部分失效。
默认情况下，没有缓存。

**如何使用：** 调用 `cacheMode()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 QGraphicsView view;
 view.setBackgroundBrush(QImage(":/images/backgroundtile.png"));
 view.setCacheMode(QGraphicsView::CacheBackground);
```

### `QGraphicsView::DragMode dragMode() const`

**作用与语义：**

该属性保留了在按下左键时拖动鼠标在场景上的行为。
该属性定义了用户点击场景背景并拖动鼠标时应发生的操作（例如，使用指针光标滚动视口内容，或用橡皮筋选择多个项目）。默认值`NoDrag`不起作用。
这种行为只影响未被任何项目处理的鼠标点击。你可以通过创建`QGraphicsView`子类并重新实现`mouseMoveEvent()`来定义自定义行为。

**如何使用：** 调用 `dragMode()` 读取当前值；它不会修改应用状态。

### `QBrush foregroundBrush() const`

**作用与语义：**

该属性保留了场景的前景画笔。
该属性为该视图中场景设置前景画笔。它用于覆盖场景自身的前景，并定义`drawForeground()`的行为。为了为该视图提供自定义前景绘制，你可以重新实现`drawForeground()`。
默认情况下，该属性包含带有`Qt::NoBrush`图案的画刷。

**如何使用：** 调用 `foregroundBrush()` 读取当前值；它不会修改应用状态。

### `bool isInteractive() const`

**作用与语义：**

该属性是否允许场景交互。
启用时，该视图设置为允许场景交互。否则，该视图不允许交互，鼠标或按键事件被忽略（即只读视图）。
默认情况下，该属性为`true`。

**如何使用：** 调用 `isInteractive()` 读取当前值；它不会修改应用状态。

### `QGraphicsView::OptimizationFlags optimizationFlags() const`

**作用与语义：**

这些标志可以用来调节`QGraphicsView`的性能。
`QGraphicsView` 使用裁剪、额外的边界矩形调整以及其他一些辅助工具，以提升常见图形场景的渲染质量和性能。然而，根据目标平台、场景和所使用的视口，这些操作可能会降低性能。
效果因标志而异;详情请参见`OptimizationFlags`文档。
默认情况下，没有启用任何最佳化标志。

**如何使用：** 调用 `optimizationFlags()` 读取当前值；它不会修改应用状态。

### `QPainter::RenderHints renderHints() const`

**作用与语义：**

该属性包含视图的默认渲染提示。
这些提示用于在绘制每个可见物品前初始化`QPainter`。`QPainter` 使用渲染提示切换渲染功能，如抗锯齿和平滑像素映射转换。
`QPainter::TextAntialiasing`默认是启用的。

**如何使用：** 调用 `renderHints()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 QGraphicsScene scene;
 scene.addRect(QRectF(-10, -10, 20, 20));

 QGraphicsView view(&scene);
 view.setRenderHints(QPainter::Antialiasing | QPainter::SmoothPixmapTransform);
 view.show();
```

### `QGraphicsView::ViewportAnchor resizeAnchor() const`

**作用与语义：**

视角在调整视角大小时应该如何定位场景。
`QGraphicsView` 利用该属性决定当视口小部件大小变化时，场景在视口中的位置。默认行为`NoAnchor`在调整大小时场景位置保持不变;调整大小时，视图左上角看起来是锚定的。
注意，当场景仅可见部分区域（即有滚动条时），该特性的影响尤为明显。否则，如果整个场景都能放入视图，`QGraphicsScene` 会利用视图对齐来将场景定位于视图中。

**如何使用：** 调用 `resizeAnchor()` 读取当前值；它不会修改应用状态。

### `Qt::ItemSelectionMode rubberBandSelectionMode() const`

**作用与语义：**

该属性支持选择带有橡皮筋选择矩形的物品。
该属性定义了使用`RubberBandDrag`拖拽模式时如何选择物品。
默认值为`Qt::IntersectsItemShape`;选择所有形状与橡皮筋相交或被橡皮筋包围的物品。

**如何使用：** 调用 `rubberBandSelectionMode()` 读取当前值；它不会修改应用状态。

### `QRectF sceneRect() const`

**作用与语义：**

该属性包含了该视图所显示的场景面积。
场景矩形定义了场景的范围，在视图中，这意味着你可以通过滚动条导航的场景区域。
如果未设置，或者设置了空`QRectF`，该属性与`QGraphicsScene::sceneRect`值相同，且随`QGraphicsScene::sceneRect`变化。否则，视图的场景矩形不受场景影响。
注意，尽管场景支持几乎无限大小，但滚动条的范围永远不会超过整数（INT_MIN、INT_MAX）。当场景大于滚动条值时，你可以选择使用`translate()`来导航场景。
默认情况下，该属性在原点包含一个宽度和高度均为零的矩形。

**如何使用：** 调用 `sceneRect()` 读取当前值；它不会修改应用状态。

### `void setAlignment(Qt::Alignment alignment)`

**作用与语义：**

该属性表示了当整个场景可见时，场景在视图中的对齐。
如果整个场景在视图中可见（即没有可见的滚动条），视图的对齐将决定场景在视图中渲染的位置。例如，如果对齐是`Qt::AlignCenter`（默认），场景会置中，如果对齐是（`Qt::AlignLeft` |`Qt::AlignTop`），场景将渲染在视图的左上角。

**如何使用：** 调用 `setAlignment(...)` 修改 `alignment`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setBackgroundBrush(const QBrush &brush)`

**作用与语义：**

该属性保留场景的背景画笔。
该属性为该视图中场景设置背景画刷。它用于覆盖场景自身背景，并定义`drawBackground()`的行为。为了为该视图提供自定义背景绘图，你可以重新实现`drawBackground()`。
默认情况下，该属性包含带有`Qt::NoBrush`图案的画刷。

**如何使用：** 调用 `setBackgroundBrush(...)` 修改 `backgroundBrush`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setCacheMode(QGraphicsView::CacheMode mode)`

**作用与语义：**

该属性决定了视图中哪些部分被缓存。
`QGraphicsView`可以缓存预渲染内容在`QPixmap`中，然后绘制到视口上。此类缓存的目的是加快渲染慢区域的总渲染时间。例如，纹理、渐变和alpha混合背景渲染速度可能明显较慢;尤其是在变换视图时。`CacheBackground`标志使视图背景能够缓存。例如：
每次视图被转换时，缓存都会被废除。然而，在滚动时，只需部分失效。
默认情况下，没有缓存。

**如何使用：** 调用 `setCacheMode(...)` 修改 `cacheMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

**官方示例：**

```cpp
 QGraphicsView view;
 view.setBackgroundBrush(QImage(":/images/backgroundtile.png"));
 view.setCacheMode(QGraphicsView::CacheBackground);
```

### `void setDragMode(QGraphicsView::DragMode mode)`

**作用与语义：**

该属性保留了在按下左键时拖动鼠标在场景上的行为。
该属性定义了用户点击场景背景并拖动鼠标时应发生的操作（例如，使用指针光标滚动视口内容，或用橡皮筋选择多个项目）。默认值`NoDrag`不起作用。
这种行为只影响未被任何项目处理的鼠标点击。你可以通过创建`QGraphicsView`子类并重新实现`mouseMoveEvent()`来定义自定义行为。

**如何使用：** 调用 `setDragMode(...)` 修改 `dragMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setForegroundBrush(const QBrush &brush)`

**作用与语义：**

该属性保留了场景的前景画笔。
该属性为该视图中场景设置前景画笔。它用于覆盖场景自身的前景，并定义`drawForeground()`的行为。为了为该视图提供自定义前景绘制，你可以重新实现`drawForeground()`。
默认情况下，该属性包含带有`Qt::NoBrush`图案的画刷。

**如何使用：** 调用 `setForegroundBrush(...)` 修改 `foregroundBrush`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setInteractive(bool allowed)`

**作用与语义：**

该属性是否允许场景交互。
启用时，该视图设置为允许场景交互。否则，该视图不允许交互，鼠标或按键事件被忽略（即只读视图）。
默认情况下，该属性为`true`。

**如何使用：** 调用 `setInteractive(...)` 修改 `interactive`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setOptimizationFlags(QGraphicsView::OptimizationFlags flags)`

**作用与语义：**

这些标志可以用来调节`QGraphicsView`的性能。
`QGraphicsView` 使用裁剪、额外的边界矩形调整以及其他一些辅助工具，以提升常见图形场景的渲染质量和性能。然而，根据目标平台、场景和所使用的视口，这些操作可能会降低性能。
效果因标志而异;详情请参见`OptimizationFlags`文档。
默认情况下，没有启用任何最佳化标志。

**如何使用：** 调用 `setOptimizationFlags(...)` 修改 `optimizationFlags`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setRenderHints(QPainter::RenderHints hints)`

**作用与语义：**

该属性包含视图的默认渲染提示。
这些提示用于在绘制每个可见物品前初始化`QPainter`。`QPainter` 使用渲染提示切换渲染功能，如抗锯齿和平滑像素映射转换。
`QPainter::TextAntialiasing`默认是启用的。

**如何使用：** 调用 `setRenderHints(...)` 修改 `renderHints`；传入的新值会成为后续查询和相关界面行为所使用的值。

**官方示例：**

```cpp
 QGraphicsScene scene;
 scene.addRect(QRectF(-10, -10, 20, 20));

 QGraphicsView view(&scene);
 view.setRenderHints(QPainter::Antialiasing | QPainter::SmoothPixmapTransform);
 view.show();
```

### `void setResizeAnchor(QGraphicsView::ViewportAnchor anchor)`

**作用与语义：**

视角在调整视角大小时应该如何定位场景。
`QGraphicsView` 利用该属性决定当视口小部件大小变化时，场景在视口中的位置。默认行为`NoAnchor`在调整大小时场景位置保持不变;调整大小时，视图左上角看起来是锚定的。
注意，当场景仅可见部分区域（即有滚动条时），该特性的影响尤为明显。否则，如果整个场景都能放入视图，`QGraphicsScene` 会利用视图对齐来将场景定位于视图中。

**如何使用：** 调用 `setResizeAnchor(...)` 修改 `resizeAnchor`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setRubberBandSelectionMode(Qt::ItemSelectionMode mode)`

**作用与语义：**

该属性支持选择带有橡皮筋选择矩形的物品。
该属性定义了使用`RubberBandDrag`拖拽模式时如何选择物品。
默认值为`Qt::IntersectsItemShape`;选择所有形状与橡皮筋相交或被橡皮筋包围的物品。

**如何使用：** 调用 `setRubberBandSelectionMode(...)` 修改 `rubberBandSelectionMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setSceneRect(const QRectF &rect)`

**作用与语义：**

该属性包含了该视图所显示的场景面积。
场景矩形定义了场景的范围，在视图中，这意味着你可以通过滚动条导航的场景区域。
如果未设置，或者设置了空`QRectF`，该属性与`QGraphicsScene::sceneRect`值相同，且随`QGraphicsScene::sceneRect`变化。否则，视图的场景矩形不受场景影响。
注意，尽管场景支持几乎无限大小，但滚动条的范围永远不会超过整数（INT_MIN、INT_MAX）。当场景大于滚动条值时，你可以选择使用`translate()`来导航场景。
默认情况下，该属性在原点包含一个宽度和高度均为零的矩形。

**如何使用：** 调用 `setSceneRect(...)` 修改 `sceneRect`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setSceneRect(qreal x, qreal y, qreal w, qreal h)`

**作用与语义：**

该属性包含了该视图所显示的场景面积。
场景矩形定义了场景的范围，在视图中，这意味着你可以通过滚动条导航的场景区域。
如果未设置，或者设置了空`QRectF`，该属性与`QGraphicsScene::sceneRect`值相同，且随`QGraphicsScene::sceneRect`变化。否则，视图的场景矩形不受场景影响。
注意，尽管场景支持几乎无限大小，但滚动条的范围永远不会超过整数（INT_MIN、INT_MAX）。当场景大于滚动条值时，你可以选择使用`translate()`来导航场景。
默认情况下，该属性在原点包含一个宽度和高度均为零的矩形。

**如何使用：** 调用 `setSceneRect(...)` 修改 `sceneRect`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTransformationAnchor(QGraphicsView::ViewportAnchor anchor)`

**作用与语义：**

视角在变换过程中应如何定位场景。
`QGraphicsView`利用该特性决定当变换矩阵变化、视角坐标系变换时，场景在视口中的位置。默认行为`AnchorViewCenter`确保场景中心点在变换过程中保持不变（例如，旋转时场景看起来会围绕视角中心旋转）。
注意，当场景仅可见部分区域（即有滚动条时），该特性的影响尤为明显。否则，如果整个场景都能放入视图，`QGraphicsScene`会利用视图对齐来将场景定位于视图中。

**如何使用：** 调用 `setTransformationAnchor(...)` 修改 `transformationAnchor`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setViewportUpdateMode(QGraphicsView::ViewportUpdateMode mode)`

**作用与语义：**

视口应如何更新其内容。
`QGraphicsView` 利用该属性决定如何更新场景中被重新曝光或更改的区域。通常你不需要修改这个属性，但在某些情况下修改可以提升渲染性能。具体细节请参见`ViewportUpdateMode`文档。
默认值是`MinimalViewportUpdate`，当内容变化时，会尽量`QGraphicsView`更新视口的最小区域。

**如何使用：** 调用 `setViewportUpdateMode(...)` 修改 `viewportUpdateMode`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QGraphicsView::ViewportAnchor transformationAnchor() const`

**作用与语义：**

视角在变换过程中应如何定位场景。
`QGraphicsView`利用该特性决定当变换矩阵变化、视角坐标系变换时，场景在视口中的位置。默认行为`AnchorViewCenter`确保场景中心点在变换过程中保持不变（例如，旋转时场景看起来会围绕视角中心旋转）。
注意，当场景仅可见部分区域（即有滚动条时），该特性的影响尤为明显。否则，如果整个场景都能放入视图，`QGraphicsScene`会利用视图对齐来将场景定位于视图中。

**如何使用：** 调用 `transformationAnchor()` 读取当前值；它不会修改应用状态。

### `QGraphicsView::ViewportUpdateMode viewportUpdateMode() const`

**作用与语义：**

视口应如何更新其内容。
`QGraphicsView` 利用该属性决定如何更新场景中被重新曝光或更改的区域。通常你不需要修改这个属性，但在某些情况下修改可以提升渲染性能。具体细节请参见`ViewportUpdateMode`文档。
默认值是`MinimalViewportUpdate`，当内容变化时，会尽量`QGraphicsView`更新视口的最小区域。

**如何使用：** 调用 `viewportUpdateMode()` 读取当前值；它不会修改应用状态。

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

`QGraphicsView` 所属机制类型：图形场景与项目机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
