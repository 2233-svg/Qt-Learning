# QGraphicsItem

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QGraphicsItem` 是 图形场景与项目机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QGraphicsItem` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QGraphicsItem>`
- 继承自：未在类页中列出
- 直接派生类：QAbstractGraphicsShapeItem、QGraphicsItemGroup、QGraphicsLineItem、QGraphicsObject,、QGraphicsPixmapItem

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

- `enum CacheMode { NoCache, ItemCoordinateCache, DeviceCoordinateCache }`
- `enum GraphicsItemChange { ItemEnabledChange, ItemEnabledHasChanged, ItemPositionChange, ItemPositionHasChanged, ItemTransformChange, …, ItemScenePositionHasChanged }`
- `enum GraphicsItemFlag { ItemIsMovable, ItemIsSelectable, ItemIsFocusable, ItemClipsToShape, ItemClipsChildrenToShape, …, ItemContainsChildrenInShape }`
- `flags GraphicsItemFlags`
- `enum PanelModality { NonModal, PanelModal, SceneModal }`
- `enum { Type, UserType }`

### 公有函数

- `QGraphicsItem(QGraphicsItem *parent = nullptr)`
- `virtual ~QGraphicsItem()`
- `bool acceptDrops() const`
- `bool acceptHoverEvents() const`
- `bool acceptTouchEvents() const`
- `Qt::MouseButtons acceptedMouseButtons() const`
- `virtual void advance(int phase)`
- `virtual QRectF boundingRect() const = 0`
- `QRegion boundingRegion(const QTransform &itemToDeviceTransform) const`
- `qreal boundingRegionGranularity() const`
- `QGraphicsItem::CacheMode cacheMode() const`
- `QList<QGraphicsItem *> childItems() const`
- `QRectF childrenBoundingRect() const`
- `void clearFocus()`
- `QPainterPath clipPath() const`
- `virtual bool collidesWithItem(const QGraphicsItem *other, Qt::ItemSelectionMode mode = Qt::IntersectsItemShape) const`
- `virtual bool collidesWithPath(const QPainterPath &path, Qt::ItemSelectionMode mode = Qt::IntersectsItemShape) const`
- `QList<QGraphicsItem *> collidingItems(Qt::ItemSelectionMode mode = Qt::IntersectsItemShape) const`
- `QGraphicsItem * commonAncestorItem(const QGraphicsItem *other) const`
- `virtual bool contains(const QPointF &point) const`
- `QCursor cursor() const`
- `QVariant data(int key) const`
- `QTransform deviceTransform(const QTransform &viewportTransform) const`
- `qreal effectiveOpacity() const`
- `void ensureVisible(const QRectF &rect = QRectF(), int xmargin = 50, int ymargin = 50)`
- `void ensureVisible(qreal x, qreal y, qreal w, qreal h, int xmargin = 50, int ymargin = 50)`
- `bool filtersChildEvents() const`
- `QGraphicsItem::GraphicsItemFlags flags() const`
- `QGraphicsItem * focusItem() const`
- `QGraphicsItem * focusProxy() const`
- `void grabKeyboard()`
- `void grabMouse()`
- `QGraphicsEffect * graphicsEffect() const`
- `QGraphicsItemGroup * group() const`
- `bool hasCursor() const`
- `bool hasFocus() const`
- `void hide()`
- `Qt::InputMethodHints inputMethodHints() const`
- `void installSceneEventFilter(QGraphicsItem *filterItem)`
- `bool isActive() const`
- `bool isAncestorOf(const QGraphicsItem *child) const`
- `bool isBlockedByModalPanel(QGraphicsItem **blockingPanel = nullptr) const`
- `bool isClipped() const`
- `bool isEnabled() const`
- `bool isObscured(const QRectF &rect = QRectF()) const`
- `bool isObscured(qreal x, qreal y, qreal w, qreal h) const`
- `virtual bool isObscuredBy(const QGraphicsItem *item) const`
- `bool isPanel() const`
- `bool isSelected() const`
- `bool isUnderMouse() const`
- `bool isVisible() const`
- `bool isVisibleTo(const QGraphicsItem *parent) const`
- `bool isWidget() const`
- `bool isWindow() const`
- `QTransform itemTransform(const QGraphicsItem *other, bool *ok = nullptr) const`
- `QPainterPath mapFromItem(const QGraphicsItem *item, const QPainterPath &path) const`
- `QPointF mapFromItem(const QGraphicsItem *item, const QPointF &point) const`
- `QPolygonF mapFromItem(const QGraphicsItem *item, const QPolygonF &polygon) const`
- `QPolygonF mapFromItem(const QGraphicsItem *item, const QRectF &rect) const`
- `QPolygonF mapFromItem(const QGraphicsItem *item, qreal x, qreal y, qreal w, qreal h) const`
- `QPointF mapFromItem(const QGraphicsItem *item, qreal x, qreal y) const`
- `QPainterPath mapFromParent(const QPainterPath &path) const`
- `QPointF mapFromParent(const QPointF &point) const`
- `QPolygonF mapFromParent(const QPolygonF &polygon) const`
- `QPolygonF mapFromParent(const QRectF &rect) const`
- `QPolygonF mapFromParent(qreal x, qreal y, qreal w, qreal h) const`
- `QPointF mapFromParent(qreal x, qreal y) const`
- `QPainterPath mapFromScene(const QPainterPath &path) const`
- `QPointF mapFromScene(const QPointF &point) const`
- `QPolygonF mapFromScene(const QPolygonF &polygon) const`
- `QPolygonF mapFromScene(const QRectF &rect) const`
- `QPolygonF mapFromScene(qreal x, qreal y, qreal w, qreal h) const`
- `QPointF mapFromScene(qreal x, qreal y) const`
- `QRectF mapRectFromItem(const QGraphicsItem *item, const QRectF &rect) const`
- `QRectF mapRectFromItem(const QGraphicsItem *item, qreal x, qreal y, qreal w, qreal h) const`
- `QRectF mapRectFromParent(const QRectF &rect) const`
- `QRectF mapRectFromParent(qreal x, qreal y, qreal w, qreal h) const`
- `QRectF mapRectFromScene(const QRectF &rect) const`
- `QRectF mapRectFromScene(qreal x, qreal y, qreal w, qreal h) const`
- `QRectF mapRectToItem(const QGraphicsItem *item, const QRectF &rect) const`
- `QRectF mapRectToItem(const QGraphicsItem *item, qreal x, qreal y, qreal w, qreal h) const`
- `QRectF mapRectToParent(const QRectF &rect) const`
- `QRectF mapRectToParent(qreal x, qreal y, qreal w, qreal h) const`
- `QRectF mapRectToScene(const QRectF &rect) const`
- `QRectF mapRectToScene(qreal x, qreal y, qreal w, qreal h) const`
- `QPainterPath mapToItem(const QGraphicsItem *item, const QPainterPath &path) const`
- `QPointF mapToItem(const QGraphicsItem *item, const QPointF &point) const`
- `QPolygonF mapToItem(const QGraphicsItem *item, const QPolygonF &polygon) const`
- `QPolygonF mapToItem(const QGraphicsItem *item, const QRectF &rect) const`
- `QPolygonF mapToItem(const QGraphicsItem *item, qreal x, qreal y, qreal w, qreal h) const`
- `QPointF mapToItem(const QGraphicsItem *item, qreal x, qreal y) const`
- `QPainterPath mapToParent(const QPainterPath &path) const`
- `QPointF mapToParent(const QPointF &point) const`
- `QPolygonF mapToParent(const QPolygonF &polygon) const`
- `QPolygonF mapToParent(const QRectF &rect) const`
- `QPolygonF mapToParent(qreal x, qreal y, qreal w, qreal h) const`
- `QPointF mapToParent(qreal x, qreal y) const`
- `QPainterPath mapToScene(const QPainterPath &path) const`
- `QPointF mapToScene(const QPointF &point) const`
- `QPolygonF mapToScene(const QPolygonF &polygon) const`
- `QPolygonF mapToScene(const QRectF &rect) const`
- `QPolygonF mapToScene(qreal x, qreal y, qreal w, qreal h) const`
- `QPointF mapToScene(qreal x, qreal y) const`
- `void moveBy(qreal dx, qreal dy)`
- `qreal opacity() const`
- `virtual QPainterPath opaqueArea() const`
- `virtual void paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget = nullptr) = 0`
- `QGraphicsItem * panel() const`
- `QGraphicsItem::PanelModality panelModality() const`
- `QGraphicsItem * parentItem() const`
- `QGraphicsObject * parentObject() const`
- `QGraphicsWidget * parentWidget() const`
- `QPointF pos() const`
- `void removeSceneEventFilter(QGraphicsItem *filterItem)`
- `void resetTransform()`
- `qreal rotation() const`
- `qreal scale() const`
- `QGraphicsScene * scene() const`
- `QRectF sceneBoundingRect() const`
- `QPointF scenePos() const`
- `QTransform sceneTransform() const`
- `void scroll(qreal dx, qreal dy, const QRectF &rect = QRectF())`
- `void setAcceptDrops(bool on)`
- `void setAcceptHoverEvents(bool enabled)`
- `void setAcceptTouchEvents(bool enabled)`
- `void setAcceptedMouseButtons(Qt::MouseButtons buttons)`
- `void setActive(bool active)`
- `void setBoundingRegionGranularity(qreal granularity)`
- `void setCacheMode(QGraphicsItem::CacheMode mode, const QSize &logicalCacheSize = QSize())`
- `void setCursor(const QCursor &cursor)`
- `void setData(int key, const QVariant &value)`
- `void setEnabled(bool enabled)`
- `void setFiltersChildEvents(bool enabled)`
- `void setFlag(QGraphicsItem::GraphicsItemFlag flag, bool enabled = true)`
- `void setFlags(QGraphicsItem::GraphicsItemFlags flags)`
- `void setFocus(Qt::FocusReason focusReason = Qt::OtherFocusReason)`
- `void setFocusProxy(QGraphicsItem *item)`
- `void setGraphicsEffect(QGraphicsEffect *effect)`
- `void setGroup(QGraphicsItemGroup *group)`
- `void setInputMethodHints(Qt::InputMethodHints hints)`
- `void setOpacity(qreal opacity)`
- `void setPanelModality(QGraphicsItem::PanelModality panelModality)`
- `void setParentItem(QGraphicsItem *newParent)`
- `void setPos(const QPointF &pos)`
- `void setPos(qreal x, qreal y)`
- `void setRotation(qreal angle)`
- `void setScale(qreal factor)`
- `void setSelected(bool selected)`
- `void setToolTip(const QString &toolTip)`
- `void setTransform(const QTransform &matrix, bool combine = false)`
- `void setTransformOriginPoint(const QPointF &origin)`
- `void setTransformOriginPoint(qreal x, qreal y)`
- `void setTransformations(const QList<QGraphicsTransform *> &transformations)`
- `void setVisible(bool visible)`
- `void setX(qreal x)`
- `void setY(qreal y)`
- `void setZValue(qreal z)`
- `virtual QPainterPath shape() const`
- `void show()`
- `void stackBefore(const QGraphicsItem *sibling)`
- `QGraphicsObject * toGraphicsObject()`
- `const QGraphicsObject * toGraphicsObject() const`
- `QString toolTip() const`
- `QGraphicsItem * topLevelItem() const`
- `QGraphicsWidget * topLevelWidget() const`
- `QTransform transform() const`
- `QPointF transformOriginPoint() const`
- `QList<QGraphicsTransform *> transformations() const`
- `virtual int type() const`
- `void ungrabKeyboard()`
- `void ungrabMouse()`
- `void unsetCursor()`
- `void update(const QRectF &rect = QRectF())`
- `void update(qreal x, qreal y, qreal width, qreal height)`
- `QGraphicsWidget * window() const`
- `qreal x() const`
- `qreal y() const`
- `qreal zValue() const`

### 保护函数

- `virtual void contextMenuEvent(QGraphicsSceneContextMenuEvent *event)`
- `virtual void dragEnterEvent(QGraphicsSceneDragDropEvent *event)`
- `virtual void dragLeaveEvent(QGraphicsSceneDragDropEvent *event)`
- `virtual void dragMoveEvent(QGraphicsSceneDragDropEvent *event)`
- `virtual void dropEvent(QGraphicsSceneDragDropEvent *event)`
- `virtual void focusInEvent(QFocusEvent *event)`
- `virtual void focusOutEvent(QFocusEvent *event)`
- `virtual void hoverEnterEvent(QGraphicsSceneHoverEvent *event)`
- `virtual void hoverLeaveEvent(QGraphicsSceneHoverEvent *event)`
- `virtual void hoverMoveEvent(QGraphicsSceneHoverEvent *event)`
- `virtual void inputMethodEvent(QInputMethodEvent *event)`
- `virtual QVariant inputMethodQuery(Qt::InputMethodQuery query) const`
- `virtual QVariant itemChange(QGraphicsItem::GraphicsItemChange change, const QVariant &value)`
- `virtual void keyPressEvent(QKeyEvent *event)`
- `virtual void keyReleaseEvent(QKeyEvent *event)`
- `virtual void mouseDoubleClickEvent(QGraphicsSceneMouseEvent *event)`
- `virtual void mouseMoveEvent(QGraphicsSceneMouseEvent *event)`
- `virtual void mousePressEvent(QGraphicsSceneMouseEvent *event)`
- `virtual void mouseReleaseEvent(QGraphicsSceneMouseEvent *event)`
- `void prepareGeometryChange()`
- `virtual bool sceneEvent(QEvent *event)`
- `virtual bool sceneEventFilter(QGraphicsItem *watched, QEvent *event)`
- `void updateMicroFocus()`
- `virtual void wheelEvent(QGraphicsSceneWheelEvent *event)`

### 相关非成员函数

- `T qgraphicsitem_cast(QGraphicsItem *item)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QGraphicsItem::CacheMode`

**作用与语义：**

本枚举描述了`QGraphicsItem`的缓存模式。缓存通过分配并渲染到屏幕外的像素缓冲区来加快渲染速度，当物品需要重新绘制时可以重复使用。对于某些绘图设备，缓存直接存储在图形内存中，这使得渲染非常快速。
- `QGraphicsItem::NoCache`：`0`;默认;所有项目缓存都被禁用。每次需要重新绘制时都会调用`QGraphicsItem::paint()`。
- `QGraphicsItem::ItemCoordinateCache`：`1`;为物品的逻辑（局部）坐标系启用缓存。`QGraphicsItem`创建一个可配置大小/分辨率的屏幕外像素缓冲区，您可以传递给`QGraphicsItem::setCacheMode()`。渲染质量通常会下降，取决于缓存的分辨率和物品转换。物品第一次重新绘制时，它会将自己渲染到缓存中，随后缓存会在每次后续曝光中被重新使用。随着物品的转换，缓存也会被重复使用。要调整缓存的分辨率，可以再次调用`setCacheMode()`。
- `QGraphicsItem::DeviceCoordinateCache`：`2`;缓存在绘画设备级别的设备坐标中启用。该模式适用于可移动但不旋转、缩放或剪切的物品。如果物品被直接或间接变换，缓存将自动重新生成。与ItemCoordinateCacheMode不同，DeviceCoordinateCache始终以最高质量渲染。

### `enum QGraphicsItem::GraphicsItemChange`

**作用与语义：**

该枚举描述了`QGraphicsItem::itemChange()`通知的状态变更。通知会随着状态变化发送，在某些情况下可以进行调整（详见每个变更的文档）。
注意：在`itemChange()`中调用`QGraphicsItem`本身的函数时要小心，因为某些函数调用可能导致不必要的递归。例如，你不能在 ItemPositionChange 通知中调用 `itemChange()` `setPos()`，因为 `setPos()` 函数会再次调用 `itemChange`（ItemPositionChange）。相反，你可以返回 `itemChange()` 中调整后的新位置。
- `QGraphicsItem::ItemEnabledChange`：`3`;项项的启用状态发生变化。如果项当前启用，则变为禁用，反之亦然。值参数是新的启用状态（即真或假）。在发送此通知时，不要在`itemChange()`调用`setEnabled()`。相反，你可以从`itemChange()`返回新状态。
- `QGraphicsItem::ItemEnabledHasChanged`：`13`;项项的启用状态发生变化。值参数是新的启用状态（即真或假）。在发送此通知时，不要调用`setEnabled()` `itemChange()`。返回值被忽略。
- `QGraphicsItem::ItemPositionChange`：`0`;项的位置发生变化。如果启用`ItemSendsGeometryChanges`标志，且项的本地位置相对于其父项发生变化（即调用`setPos()`或`moveBy()`，则会发送此通知）。值参数即为新位置（即`QPointF`）。你可以调用`pos()`以获取原始位置。在发送此通知时，不要在 `itemChange()` 中调用 `setPos()` 或 `moveBy()`;相反，你可以从`itemChange()`返回新的调整位置。收到通知后，如果位置发生变化，`QGraphicsItem` 会立即发送 ItemPositionHasChanged 通知。
- `QGraphicsItem::ItemPositionHasChanged`：`9`;该项的位置发生了变化。如果启用`ItemSendsGeometryChanges`标志，且该项相对于父项的本地位置发生变化后，会发送此通知。值参数是新位置（与`pos()`相同），`QGraphicsItem`忽略该通知的返回值（即只读通知）。
- `QGraphicsItem::ItemTransformChange`：`8`;项的变换矩阵发生变化。如果启用`ItemSendsGeometryChanges`标志，且当项的局部变换矩阵发生变化（即调用`setTransform()`后，会发送此通知。值参数是新的矩阵（即`QTransform`）;要获取旧矩阵，请调用`transform()`。在发送此通知时，不要调用`setTransform()`或设置`itemChange()`中的任何变换属性;相反，你可以从`itemChange()`返回新的矩阵。如果你更改变换属性，这个通知不会发送。
- `QGraphicsItem::ItemTransformHasChanged`：`10`;项的变换矩阵发生变化，可能是因为调用了`setTransform`，或者变换属性被更改。如果启用`ItemSendsGeometryChanges`标志，且项的本地变换矩阵发生变化，则会发送该通知。值参数是新的矩阵（与`transform()`相同），`QGraphicsItem`忽略该通知的返回值（即只读通知）。
- `QGraphicsItem::ItemRotationChange`：`28`;项的旋转属性发生变化。如果启用`ItemSendsGeometryChanges`标志，且项旋转属性发生变化（即调用`setRotation()`，则会发送此通知）。值参数是新的旋转（即双重）;要获取旧的旋转，请调用`rotation()`。在`itemChange()`中不要调用`setRotation()`，因为该通知正在传递;相反，你可以从`itemChange()`返回新的旋转。
- `QGraphicsItem::ItemRotationHasChanged`：`29`;该项的旋转属性发生了变化。如果启用`ItemSendsGeometryChanges`标志，且在该项的旋转属性发生变化后，会发送此通知。value 参数是新的旋转（即双重），`QGraphicsItem`忽略该通知的返回值（即只读通知）。在发送该通知时，不要在`itemChange()`调用`setRotation()`。
- `QGraphicsItem::ItemScaleChange`：`30`;该项的刻度属性发生变化。如果启用`ItemSendsGeometryChanges`标志，且当项的刻度属性发生变化（即调用`setScale()`后发生变化），该通知会发送。值参数是新的刻度（即双重）;要获取旧的刻度，请调用`scale()`。在发送此通知时，不要在 `itemChange()` 中调用`setScale()`;相反，你可以从`itemChange()`返回新的。
- `QGraphicsItem::ItemScaleHasChanged`：`31`;项的尺度属性发生了变化。如果启用`ItemSendsGeometryChanges`标志，且项的缩放属性发生变化后，会发送此通知。值参数是新的尺度（即重叠），`QGraphicsItem`忽略该通知的返回值（即只读通知）。在发送该通知时，不要在 `itemChange()` 调用 `setScale()`。
- `QGraphicsItem::ItemTransformOriginPointChange`：`32`;项的变换起点属性发生变化。当`ItemSendsGeometryChanges`标志启用，且项变换起点属性发生变化（即调用`setTransformOriginPoint()`时），会发送此通知。值参数是新的原点（即`QPointF`）;要获取旧起点，调用`transformOriginPoint()`。在发送此通知时，不要在 `itemChange()` 调用 `setTransformOriginPoint()`;相反，你可以返回`itemChange()`新的变换起点。
- `QGraphicsItem::ItemTransformOriginPointHasChanged`：`33`;该项的变换起点属性发生了变化。如果启用了`ItemSendsGeometryChanges`标志，并且在变换起点属性发生变化后，会发送该通知。值参数是新的起点（即`QPointF`），`QGraphicsItem`忽略了该通知的返回值（即只读通知）。在发送该通知时，不要在 `itemChange()` 中调用 `setTransformOriginPoint()`。
- `QGraphicsItem::ItemSelectedChange`：`4`;该项的选中状态会发生变化。如果该项当前被选中，则会变为未被选中，反之亦然。值参数是新的选中状态（即真或假）。在发送此通知时，不要在`itemChange()`调用`setSelected()`;相反，你可以从`itemChange()`返回新的选中状态。
- `QGraphicsItem::ItemSelectedHasChanged`：`14`;该项的选择状态发生了变化。值参数是新的选择状态（即真或假）。在此通知传递时，不要调用`setSelected()` in `itemChange()`。返回值被忽略。
- `QGraphicsItem::ItemVisibleChange`：`2`;该项的可见状态会发生变化。如果该项当前可见，则它将变为不可见，反之亦然。值参数即为新的可见状态（即真或假）。在发送此通知时，不要调用`itemChange()`中的`setVisible()`;相反，你可以从`itemChange()`返回新的可见状态。
- `QGraphicsItem::ItemVisibleHasChanged`：`12`;该项的可见状态发生了变化。value 参数是新的可见状态（即真或假）。在发送此通知时，不要调用`setVisible()` in `itemChange()`。返回值被忽略。
- `QGraphicsItem::ItemParentChange`：`5`;该项的父项发生变化。值参数是新的父项（即`QGraphicsItem`指针）。在发送此通知时，不要在 `itemChange()` 调用`setParentItem()`;相反，你可以从`itemChange()`返回新的父项。
- `QGraphicsItem::ItemParentHasChanged`：`15`;该项的父节点发生了变化。值参数是新的父节点（即指向`QGraphicsItem`的指针）。在发送此通知时，不要调用`setParentItem()` in `itemChange()`。返回值被忽略。
- `QGraphicsItem::ItemChildAddedChange`：`6`;该项被添加一个子项。值参数是新的子项（即`QGraphicsItem`指针）。在发送此通知时，不要将该项传递给任何`setParentItem()`函数。返回值未被使用;你不能在通知中调整任何内容。注意，发送此通知时新子节点可能尚未完全构建;调用子节点上的纯虚拟函数可能导致崩溃。
- `QGraphicsItem::ItemChildRemovedChange`：`7`;该项中移除了一个子项。值参数是即将被移除的子项（即`QGraphicsItem`指针）。返回值未被使用;你无法在该通知中调整任何内容。
- `QGraphicsItem::ItemSceneChange`：`11`;该项目被移动到新场景。该通知在添加到初始场景和移除场景时也会发送。该物品的`scene()`是旧场景，如果该物品尚未添加到场景，则为`nullptr`。值参数是新场景（即`QGraphicsScene`指针），如果物品从场景中移除，则为`nullptr`。在发送该通知时，不要通过将该项目传给`QGraphicsScene::addItem()`来覆盖该更改;相反，你可以从`itemChange()`返回新场景。使用此功能时请谨慎;反对场景变更可能导致不必要的递归。
- `QGraphicsItem::ItemSceneHasChanged`：`16`;该项目的场景发生了变化。该项目的`scene()`是新的场景。当该项目被添加到初始场景时和移除时，也会发送该通知。值参数是新场景（即指向`QGraphicsScene`的指针）。在发送此通知时，不要在`itemChange()`中调用 setScene()。返回值被忽略。
- `QGraphicsItem::ItemCursorChange`: `17`；该项目的光标发生变化。value 参数是新的光标（即 `QCursor`）。在发送此通知时不要在 `itemChange()` 中调用 `setCursor()`。相反，你可以从 `itemChange()` 返回一个新光标。
- `QGraphicsItem::ItemCursorHasChanged`: `18`；该项目的光标已更改。value 参数是新的光标（即 `QCursor`）。在发送此通知时不要调用 `setCursor()`。返回值将被忽略。
- `QGraphicsItem::ItemToolTipChange`: `19`；该项目的工具提示发生变化。value 参数是新的工具提示（即 `QToolTip`）。在发送此通知时不要在 `itemChange()` 中调用 `setToolTip()`。相反，你可以从 `itemChange()` 返回一个新的工具提示。
- `QGraphicsItem::ItemToolTipHasChanged`: `20`；该项目的工具提示已更改。value 参数是新的工具提示（即 `QToolTip`）。在发送此通知时不要调用 `setToolTip()`。返回值将被忽略。
- `QGraphicsItem::ItemFlagsChange`: `21`；该项目的标志发生变化。value 参数是新的标志（即 quint32）。在发送此通知时不要在 `itemChange()` 中调用 `setFlags()`。相反，你可以从 `itemChange()` 返回新的标志。
- `QGraphicsItem::ItemFlagsHaveChanged`: `22`；该项目的标志已更改。value 参数是新的标志（即 quint32）。在发送此通知时不要在 `itemChange()` 中调用 `setFlags()`。返回值将被忽略。
- `QGraphicsItem::ItemZValueChange`: `23`；该项目的 Z 值发生变化。value 参数是新的 Z 值（即 double）。在发送此通知时不要在 `itemChange()` 中调用 `setZValue()`。相反，你可以从 `itemChange()` 返回新的 Z 值。
- `QGraphicsItem::ItemZValueHasChanged`: `24`；该项目的 Z 值已更改。value 参数是新的 Z 值（即 double）。在发送此通知时不要调用 `setZValue()`。返回值将被忽略。
- `QGraphicsItem::ItemOpacityChange`: `25`；该项目的不透明度发生变化。value 参数是新的不透明度（即 double）。在发送此通知时不要在 `itemChange()` 中调用 `setOpacity()`。相反，你可以从 `itemChange()` 返回新的不透明度。
- `QGraphicsItem::ItemOpacityHasChanged`: `26`；该项目的不透明度已更改。value 参数是新的不透明度（即 double）。在发送此通知时不要调用 `setOpacity()`。返回值将被忽略。
- `QGraphicsItem::ItemScenePositionHasChanged`: `27`；该项目的场景位置已更改。如果启用了 `ItemSendsScenePositionChanges` 标志，并且在该项目的场景位置发生变化后（即项目自身的位置或变换变化，或任何祖先的位置或变换变化），则会发送此通知。value 参数是新的场景位置（与 `scenePos()` 相同），而 `QGraphicsItem` 会忽略此通知的返回值（即只读通知）。

### `enum QGraphicsItem::GraphicsItemFlagflags QGraphicsItem::GraphicsItemFlags`

**作用与语义：**

这个枚举描述了你可以在物品上设置的不同标志，以切换物品行为中的不同功能。
所有标志默认都是被禁用的。
- `QGraphicsItem::ItemIsMovable`：`0x1`;该项目支持使用鼠标进行交互移动。点击该项目并拖动，该物品会与鼠标光标一起移动。如果该项目有子节点，所有子节点也会被移动。如果该项目是选择的一部分，所有被选中的项目也会被移动。此功能通过`QGraphicsItem`鼠标事件处理程序的基础实现提供了便利性。
- `QGraphicsItem::ItemIsSelectable`：`0x2`;该物品支持选择。启用此功能后，`setSelected()`可以切换该物品的选择。它还可以通过调用`QGraphicsScene::setSelectionArea()`、点击物品或在`QGraphicsView`中使用橡皮筋选择自动选择该物品。
- `QGraphicsItem::ItemIsFocusable`：`0x4`;该项目支持键盘输入焦点（即输入项目）。启用该标志后，项目可以接受焦点，从而再次将按键事件传递到`QGraphicsItem::keyPressEvent()`和`QGraphicsItem::keyReleaseEvent()`。
- `QGraphicsItem::ItemClipsToShape`：`0x8`;物品会剪辑到自身形状。物品不能绘制或接收鼠标、平板、拖拽或悬停事件。默认情况下禁用该功能。此行为由QGraphicsView：:d rawItems()或QGraphicsScene：:d rawItems()强制执行。该标志于Qt 4.3引入。
- `QGraphicsItem::ItemClipsChildrenToShape`：`0x10`;该物品将所有后代的绘制剪辑为自身形状。该物品的直接或间接子节点不得绘制超出该物品形状的物体。默认情况下，该标志被禁用;子节点可以随处绘制。此行为由QGraphicsView：:d rawItems()或QGraphicsScene：:d rawItems()强制执行。该标志于Qt 4.3引入。
注意：该标志类似于ItemContainsChildrenInShape，但通过裁剪子节点来强制限制。
- `QGraphicsItem::ItemIgnoresTransformations`：`0x20`;该项目忽略继承的变换（即其位置仍锚定于父变换，但忽略父或视角的旋转、缩放或剪切变换）。该标志有助于保持文本标签项水平且未缩放，因此即使视角变换，仍可读取。设置后，视角几何体和场景几何体将分别维护。您必须调用`deviceTransform()`来映射坐标并检测视图中的碰撞。默认情况下，该标志是禁用的。该标志在Qt 4.3中引入。
注意：有了这个标志，你仍然可以调整物品本身，而这个比例转换会影响物品的子节点。
- `QGraphicsItem::ItemIgnoresParentOpacity`：`0x40`;该项忽略其父项的不透明度。该项的有效不透明度与自身相同;它不会与父项的不透明度结合。该标志允许即使父项半透明，也保持绝对不透明度。该标志引入于Qt 4.5。
- `QGraphicsItem::ItemDoesntPropagateOpacityToChildren`：`0x80`;该项不会将其不透明度传播到子节点。该标志允许你创建一个半透明的项目，不影响其子节点的透明度。该标志在Qt 4.5引入。
- `QGraphicsItem::ItemStacksBehindParent`：`0x100`;该物品被叠放在父物品之后。默认情况下，子物品会叠放在父物品之上。但设置该标志时，子节点会被叠放在它后面。该标志适用于投影效果和装饰对象，这些对象遵循父物品的几何体而不在其上方绘制。该标志在Qt 4.5中引入。
- `QGraphicsItem::ItemUsesExtendedStyleOption`：`0x200`;该项在`QStyleOptionGraphicsItem`中使用任一`exposedRect`。默认情况下，`exposedRect`初始化为该项的 `boundingRect()`。你可以启用此标志，以便样式选项设置更细粒度的值。如果需要更高的值，可以使用 `QStyleOptionGraphicsItem::levelOfDetailFromTransform()`。该标志于 Qt 4.6 引入。
- `QGraphicsItem::ItemHasNoContents`：`0x400`;该物品不绘制任何东西（即调用`paint()`无效）。你应在不需要绘制的物品上设置此标志，以确保图形视图避免不必要的绘制准备。该标志于Qt 4.6引入。
- `QGraphicsItem::ItemSendsGeometryChanges`：`0x800`;该项目启用`itemChange()`通知，涵盖`ItemPositionChange`、`ItemPositionHasChanged`、`ItemTransformChange`、`ItemTransformHasChanged`、`ItemRotationChange`、`ItemRotationHasChanged`、`ItemScaleChange`、`ItemScaleHasChanged`、`ItemTransformOriginPointChange`和`ItemTransformOriginPointHasChanged`。出于性能原因，这些通知默认被禁用。您必须启用此标志才能接收位置和变换的通知。该标志于 Qt 4.6 引入。
- `QGraphicsItem::ItemAcceptsInputMethod`：`0x1000`;该项支持通常用于亚洲语言的输入法。该标志于Qt 4.6引入。
- `QGraphicsItem::ItemNegativeZStacksBehindParent`：`0x2000`;如果物品的z值为负，则该物品会自动堆叠到父节点之后。该标志使`setZValue()`能够切换ItemStacksBehindParent。该标志于Qt 4.6引入。
- `QGraphicsItem::ItemIsPanel`：`0x4000`;该物品是一个面板。面板提供激活和受控焦点处理。一次只能激活一个面板（参见 `QGraphicsItem::isActive()`）。当没有面板处于激活状态时，`QGraphicsScene`激活所有非面板物品。窗口物品（即`QGraphicsItem::isWindow()`返回`true`）是面板。该标志于第4.6个Qt引入。
- `QGraphicsItem::ItemSendsScenePositionChanges`：`0x10000`;该项目启用`itemChange()` `ItemScenePositionHasChanged`通知。出于性能原因，这些通知默认被禁用。您必须启用此标志才能接收场景位置变化的通知。该标志于Qt 4.6引入。
- `QGraphicsItem::ItemContainsChildrenInShape`：`0x80000`;该标志表示所有直接或间接子节点只在物品形状内绘制。与ItemClipsChildrenToShape不同，该限制不被强制执行。当你手动确保绘图绑定到物品形状并想避免强制剪辑产生的成本时，请设置ItemContainsChildrenInShape。设置该标志可以实现更高效的绘图和碰撞检测。该标志默认被禁用。
注意：如果同时设置了该标志和 ItemClipsChildrenToShape，剪辑将被强制执行。这相当于仅仅设置 ItemClipsChildrenToShape。
该标志于第5.4期引入。
GraphicsItemFlags 类型是 QFlags<GraphicsItemFlag> 的 typedef。它存储 GraphicsItemFlag 值的按位或组合。

### `enum QGraphicsItem::PanelModality`

**作用与语义：**

该枚举指定了模态面板的行为。模态面板是阻止其他面板输入的面板。注意，模态面板的子项不会被阻塞。
这些数值如下：
- `QGraphicsItem::NonModal`：`0`;该面板不是模态的，不会阻挡输入到其他面板。这是面板的默认值。
- `QGraphicsItem::PanelModal`：`1`;该面板对单一项目层级为模态，阻挡其父面板、所有祖父面板以及其父面板的所有兄弟面板的输入。
- `QGraphicsItem::SceneModal`：`2`;窗口对整个场景是模态的，并屏蔽所有面板的输入。

### `[anonymous] enum`

**作用与语义：**

虚拟`type()`函数在标准图形项类中返回的值。所有此类标准图形项类在 Qt 中都关联到一个唯一的类型值，例如`QGraphicsPathItem::type()`返回的值为 2。
- `QGraphicsItem::Type`：`1`;`QGraphicsPathItem`级：公`QAbstractGraphicsShapeItem`
{。
公众：
enum { 类型 = 2 };
int type() const override（return Type; }。
...
};
- `QGraphicsItem::UserType`：`65536`;虚拟`type()`函数对`QGraphicsItem`自定义子类返回的最低值。
类别自定义物品：公开`QGraphicsItem`。
{。
公众：
enum { 类型 = 用户类型 1 };

int type() const 覆盖。
{。
启用该物品的qgraphicsitem_cast。
返回类型;
}。
...
};

### `[explicit] QGraphicsItem::QGraphicsItem(QGraphicsItem *parent = nullptr)`

**作用与语义：**

构造包含给定`parent`项的QGraphicsItem。它不会修改`QObject::parent()`返回的父对象。
如果`parent` `nullptr`，你可以通过调用`QGraphicsScene::addItem()`将该物品添加到场景中。该物品随后会成为顶级物品。

### `[virtual noexcept] QGraphicsItem::~QGraphicsItem()`

**作用与语义：**

销毁`QGraphicsItem`及其所有子节点。如果该物品当前与场景关联，该物品会在被删除前从场景中移除。
注意：最好先将物品从`QGraphicsScene`中移除再销毁。

### `bool QGraphicsItem::acceptDrops() const`

**作用与语义：**

如果该项目能接受拖放事件，返回 `true`;否则返回 `false`。默认情况下，物品不接受拖放事件;物品对拖放是透明的。

### `bool QGraphicsItem::acceptHoverEvents() const`

**作用与语义：**

如果物品接受悬停事件（`QGraphicsSceneHoverEvent`），返回`true`;否则返回 `false`。默认情况下，物品不接受悬停事件。

### `bool QGraphicsItem::acceptTouchEvents() const`

**作用与语义：**

如果项目接受触摸事件，返回`true`;否则返回`false`。默认情况下，物品不接受触摸事件。

### `Qt::MouseButtons QGraphicsItem::acceptedMouseButtons() const`

**作用与语义：**

返回该项目接受鼠标事件的鼠标按钮。默认情况下，所有鼠标按钮都被接受。
如果物品接受鼠标按钮，当该鼠标按钮触发鼠标按键事件时，它将成为鼠标抓取物品。但如果物品不接受按钮，`QGraphicsScene`会将鼠标事件转发给其下方第一个接受该按钮的物品。

### `[virtual] void QGraphicsItem::advance(int phase)`

**作用与语义：**

该虚拟函数通过`QGraphicsScene::advance()`槽调用所有物品两次。第一阶段，所有物品调用时为 `phase` == 0，表示场景中的物品即将推进，然后所有物品以 `phase` == 1 调用。如果你需要简单的场景控制动画，可以重新实现该函数来更新物品。
默认实现什么都不做。
该函数专为动画设计。另一种方法是从`QObject`和`QGraphicsItem`多重继承，并使用动画框架。

### `[pure virtual] QRectF QGraphicsItem::boundingRect() const`

**作用与语义：**

这个纯虚拟函数将物品的外边界定义为矩形;所有绘画必须限制在物品的边界矩形内。`QGraphicsView`利用这一点判断物品是否需要重新绘制。
虽然物品的形状可以任意，但边界矩形始终是矩形，且不受物品变换的影响。
如果你想更改物品的边界矩形，必须先调用`prepareGeometryChange()`。这会通知场景即将发生的变化，以便更新其物品几何索引;否则，场景将无法感知物品的新几何体，结果也未定义（通常渲染的伪影会留在视图中）。
重新实现这个函数，让`QGraphicsView`判断小部件的哪些部分需要重新绘制。
注意：对于绘制轮廓/笔画的形状，在包围矩形中包含一半的笔宽非常重要。不过，这并不需要补偿抗锯齿。

**官方示例：**

```cpp
 QRectF CircleItem::boundingRect() const
 {
     qreal penWidth = 1;
     return QRectF(-radius - penWidth / 2, -radius - penWidth / 2,
                   diameter + penWidth, diameter + penWidth);
 }
```

### `QRegion QGraphicsItem::boundingRegion(const QTransform &itemToDeviceTransform) const`

**作用与语义：**

返回该项的边界区域。返回区域的坐标空间依赖于`itemToDeviceTransform`。如果你将恒等`QTransform`作为参数传递，该函数将返回一个局部坐标区域。
边界区域描述了物品视觉内容的粗略轮廓。虽然计算成本高，但比`boundingRect()`更精确，有助于避免更新物品时不必要的重新涂色。这对细条目（如线条或简单多边形）尤其高效。你可以通过调用`setBoundingRegionGranularity()`来调整边界区域的粒度。默认粒度为0;即物品的边界区域与其边界矩形相同。
`itemToDeviceTransform` 是从物品坐标到设备坐标的变换。如果你想让这个函数返回场景坐标中的`QRegion`，可以把`sceneTransform()`作为参数传递。

### `qreal QGraphicsItem::boundingRegionGranularity() const`

**作用与语义：**

返回该项的边界区域粒度;介于和之间，包含0和1的值。默认值为0（即最低粒度，其中边界区域对应于物品的边界矩形）。

### `QGraphicsItem::CacheMode QGraphicsItem::cacheMode() const`

**作用与语义：**

返回该项的缓存模式。默认模式为`NoCache`（即缓存被禁用，所有绘画即时完成）。

### `QList<QGraphicsItem *> QGraphicsItem::childItems() const`

**作用与语义：**

返回该物品的子列表。
这些物品按堆叠顺序排序。这会考虑物品的插入顺序和它们的Z值。

### `QRectF QGraphicsItem::childrenBoundingRect() const`

**作用与语义：**

返回该项后代（即其子节点、子节点等）在局部坐标下的边界矩形。矩形将包含所有后代映射到局部坐标后。如果该项没有子节点，该函数返回空的`QRectF`。
这不包括该项自身的边界矩形;它只返回其后代累计的边界矩形。如果你需要包含该项的边界矩格，可以使用 QRectF：：operator| 在 childrenBoundingRect() 中添加`boundingRect()`().
该函数复杂度线性;它通过遍历所有后代确定返回边界矩阵的大小。

### `void QGraphicsItem::clearFocus()`

**作用与语义：**

它会从物品上提取键盘输入的焦点。
如果它有焦点，会向该物品发送一个焦点外事件，告诉它即将失去焦点。
只有设置`ItemIsFocusable`标志的物品，或设置适当焦点策略的小部件，才能接受键盘焦点。

### `QPainterPath QGraphicsItem::clipPath() const`

**作用与语义：**

返回该物品的剪辑路径，如果该物品未被裁剪，则返回空`QPainterPath`。剪辑路径限制该物品的外观和交互（即限制该物品可绘制和接收事件的区域）。
你可以通过设置`ItemClipsToShape`或`ItemClipsChildrenToShape`标志来启用裁剪。该物品的剪辑路径是通过交叉所有裁剪祖先形状计算的。如果该项目设置`ItemClipsToShape`，最终剪辑会与该物品自身的形状相交。
注意：裁剪会对所有涉及的物品产生性能惩罚;如果可以的话，通常应避免使用裁剪（例如，如果你的物品总是在`boundingRect()`或`shape()`边界内绘制，则不需要剪辑）。

### `[virtual] bool QGraphicsItem::collidesWithItem(const QGraphicsItem *other, Qt::ItemSelectionMode mode = Qt::IntersectsItemShape) const`

**作用与语义：**

如果该项与`other`碰撞，返回`true`;否则返回`false`。
`mode`应用到`other`，然后将生成的形状或边界矩形与该物品的形状进行比较。`mode`的默认值为`Qt::IntersectsItemShape`;如果该物体与该物体相交、包含或被该物体的形状包围，`other`与该物体发生碰撞（详情见`Qt::ItemSelectionMode`）。
默认实现基于形状交集，并且在两个项目上调用`shape()`。由于当形状复杂时，任意形状-形状交集的复杂度会随数量级增长，这个操作可能会显得非常耗时。你可以选择在`QGraphicsItem`的子类中重新实现该函数，以提供自定义算法。这允许你利用自己物品形状中的自然约束，以提升碰撞检测的性能。例如，两个未变换的完美圆形物体的碰撞可以通过比较它们的位置和半径非常高效地确定。
请记住，在重新实现该函数并调用`other` `shape()`或`boundingRect()`时，返回的坐标必须先映射到该项的坐标系，才能发生任何交集。

### `[virtual] bool QGraphicsItem::collidesWithPath(const QPainterPath &path, Qt::ItemSelectionMode mode = Qt::IntersectsItemShape) const`

**作用与语义：**

如果该物品与`path`碰撞，返回`true`。
碰撞由`mode`决定。`mode`的默认值为`Qt::IntersectsItemShape`;`path`与该项相交、包含或被该项的形状包围，则与该项发生碰撞。
注意，该函数检查的是物品的形状或边界矩形（取决于`mode`）是否包含在`path`内，而不是 `path` 是否包含在物品形状或边界矩形内。

### `QList<QGraphicsItem *> QGraphicsItem::collidingItems(Qt::ItemSelectionMode mode = Qt::IntersectsItemShape) const`

**作用与语义：**

返回所有与该物品碰撞的物品列表。
碰撞检测方式通过对被比较的物品应用`mode`来确定，即每个物体的形状或边界矩形都与该物体的形状进行对照。`mode`的默认值是`Qt::IntersectsItemShape`。

### `QGraphicsItem *QGraphicsItem::commonAncestorItem(const QGraphicsItem *other) const`

**作用与语义：**

返回该物品和`other`最近的共同祖先物品，或`nullptr`如果`other` `nullptr`或没有共同祖先。

### `[virtual] bool QGraphicsItem::contains(const QPointF &point) const`

**作用与语义：**

如果该项包含`point`，则返回`true`，且该元素位于局部坐标中;否则返回 false。它通常被调用`QGraphicsView`来确定光标下方的物品，因此该函数的实现应尽可能轻量。
默认情况下，这个函数调用`shape()`，但你可以在子类中重新实现，提供（或许更高效的）实现。

### `[virtual protected] void QGraphicsItem::contextMenuEvent(QGraphicsSceneContextMenuEvent *event)`

**作用与语义：**

该事件处理程序可以被重新实现为子类，用于处理上下文菜单事件。`event`参数包含待处理事件的详细信息。
如果你忽略该事件（即调用`QEvent::ignore()`），`event`会传播到该事件下方的任何物品。如果没有物品接受该事件，场景会忽略它并传播到视图。
收到上下文菜单事件后，通常会打开`QMenu`。示例：
默认实现会忽略该事件。

**官方示例：**

```cpp
 void CustomItem::contextMenuEvent(QGraphicsSceneContextMenuEvent *event)
 {
     QMenu menu;
     QAction *removeAction = menu.addAction("Remove");
     QAction *markAction = menu.addAction("Mark");
     QAction *selectedAction = menu.exec(event->screenPos());
     // ...
 }
```

### `QCursor QGraphicsItem::cursor() const`

**作用与语义：**

返回当前光标形状。鼠标光标在该物体上时会呈现该形状。请参阅预定义光标对象列表，了解一系列有用的形状。
编辑器项目可能想使用工字束光标：
如果没有设置光标，则使用下方物品的光标。

**官方示例：**

```cpp
 item->setCursor(Qt::IBeamCursor);
```

### `QVariant QGraphicsItem::data(int key) const`

**作用与语义：**

返回该项的自定义数据，用于密钥 `key` 作为 `QVariant`。
自定义物品数据对于存储任意物品属性非常有用。示例：
Qt 不使用此功能来存储数据;它仅为用户方便而提供。

**官方示例：**

```cpp
 static const int ObjectName = 0;

 QGraphicsItem *item = scene.itemAt(100, 50);
 if (item->data(ObjectName).toString().isEmpty()) {
     if (qgraphicsitem_cast<ButtonItem *>(item))
         item->setData(ObjectName, "Button");
 }
```

### `QTransform QGraphicsItem::deviceTransform(const QTransform &viewportTransform) const`

**作用与语义：**

返回该项目的设备变换矩阵，使用`viewportTransform`映射场景到设备的坐标。该矩阵可用于将该物体的本地坐标系中的坐标和几何形状映射到视口（或任何设备的）坐标系。要从视口映射坐标，首先必须反转返回的矩阵。
该函数类似于将该物品的场景变换与视角的视口变换结合，但它也理解`ItemIgnoresTransformations`标志。设备变换可用于对不可变换的对象进行精确的坐标映射（及碰撞检测）。

**官方示例：**

```cpp
 QGraphicsRectItem rect;
 rect.setPos(100, 100);

 rect.deviceTransform(view->viewportTransform()).map(QPointF(0, 0));
 // returns the item's (0, 0) point in view's viewport coordinates

 rect.deviceTransform(view->viewportTransform()).inverted().map(QPointF(100, 100));
 // returns view's viewport's (100, 100) coordinate in item coordinates
```

### `[virtual protected] void QGraphicsItem::dragEnterEvent(QGraphicsSceneDragDropEvent *event)`

**作用与语义：**

该事件处理程序对于事件`event`，可以重新实现以接收该项目的拖拽进入事件。拖入事件是在光标进入物品区域时生成的。
通过接受事件（即调用`QEvent::accept()`），该物品将接受掉落事件，同时还会接收拖动移动和拖离。否则，该事件将被忽略并传播到下面的物品。如果事件被接受，该物品会在控制返回事件循环前接收拖动移动事件。
dragEnterEvent 的一个常见实现会根据 `event` 中的 MIME 数据接受或忽略`event`。示例：
物品默认不会接收拖放事件;要启用此功能，请调用`setAcceptDrops(true)`。
默认实现什么都不做。

**官方示例：**

```cpp
 CustomItem::CustomItem()
 {
     setAcceptDrops(true);
     ...
 }

 void CustomItem::dragEnterEvent(QGraphicsSceneDragDropEvent *event)
 {
     event->setAccepted(event->mimeData()->hasFormat("text/plain"));
 }
```

### `[virtual protected] void QGraphicsItem::dragLeaveEvent(QGraphicsSceneDragDropEvent *event)`

**作用与语义：**

该事件处理程序用于事件`event`，可以重新实现以接收该物品的拖曳离开事件。拖曳离开事件是在光标离开物品区域时生成的。大多数情况下你不需要重新实现这个函数，但它对于重置物品状态（例如高亮）非常有用。
打电话给`QEvent::ignore()`或`QEvent::accept()`打`event`没有任何效果。
物品默认不会接收拖拽事件;要启用此功能，请调用`setAcceptDrops(true)`。
默认实现什么都不做。

### `[virtual protected] void QGraphicsItem::dragMoveEvent(QGraphicsSceneDragDropEvent *event)`

**作用与语义：**

该事件处理程序用于事件`event`，可以重新实现以接收该物品的拖动移动事件。拖动移动事件是在光标在物品区域内移动时生成的。大多数情况下你不需要重新实现这个功能;它用于表示只有物品的部分可以接受掉落。
在`event`时调用`QEvent::ignore()`或`QEvent::accept()`，可以切换该物品是否接受该事件位置的掉落。默认情况下，`event`被接受，表示该物品允许在指定位置掉落。
物品默认不会接收拖拽事件;要启用此功能，请调用`setAcceptDrops(true)`。
默认实现什么都不做。

### `[virtual protected] void QGraphicsItem::dropEvent(QGraphicsSceneDragDropEvent *event)`

**作用与语义：**

该事件处理程序对于事件`event`，可以重新实现以接收该物品的掉落事件。只有当最后一个拖动移动事件被接受时，物品才能接收掉落事件。
打电话给`QEvent::ignore()`或`QEvent::accept()`打`event`没有效果。
物品默认不会接收拖拽事件;要启用此功能，请调用`setAcceptDrops(true)`。
默认实现什么都不做。

### `qreal QGraphicsItem::effectiveOpacity() const`

**作用与语义：**

返回该项的有效不透明度，介于0.0（透明）和1.0（不透明）之间。该值是该项局部不透明度与其父项和祖先不透明度的组合。有效不透明度决定了该项的渲染方式。

### `void QGraphicsItem::ensureVisible(const QRectF &rect = QRectF(), int xmargin = 50, int ymargin = 50)`

**作用与语义：**

如果该项是`QGraphicsView`可观看场景的一部分，这个便利功能会尝试滚动视图，确保`rect`在视图的视口内可见。如果`rect`是空矩形块（默认），`QGraphicsItem`将默认使用该项的边界矩形块。`xmargin`和`ymargin`是视图应用作边距的像素数。
如果无法到达指定的rect，内容会被滚动到最近的有效位置。
如果该项没有被`QGraphicsView`查看，这个函数就不会有任何作用。

### `void QGraphicsItem::ensureVisible(qreal x, qreal y, qreal w, qreal h, int xmargin = 50, int ymargin = 50)`

**作用与语义：**

这个便捷函数等价于调用 ensureVisible(`QRectF`(`x`, `y`, `w`, `h`), `xmargin`, `ymargin`) 。

### `bool QGraphicsItem::filtersChildEvents() const`

**作用与语义：**

如果该项过滤子事件（即所有原本用于其子节点的事件都被发送到该项），则返回`true`;否则返回 false。
默认值为 false;子事件不会被过滤。

### `QGraphicsItem::GraphicsItemFlags QGraphicsItem::flags() const`

**作用与语义：**

返回该项的标志。这些标志描述了该项哪些可配置特征被启用或未启用。例如，如果标志包含`ItemIsFocusable`，则该项可以接受输入焦点。
默认情况下，不会启用任何标志。

### `[virtual protected] void QGraphicsItem::focusInEvent(QFocusEvent *event)`

**作用与语义：**

该事件处理程序对于事件`event`，可以重新实现以获得该项事件中的焦点。默认实现调用`ensureVisible()`。

### `QGraphicsItem *QGraphicsItem::focusItem() const`

**作用与语义：**

如果该项、其子项或后代当前有输入焦点，该函数将返回指向该项的指针。如果没有后代有输入焦点，则返回`nullptr`。

### `[virtual protected] void QGraphicsItem::focusOutEvent(QFocusEvent *event)`

**作用与语义：**

该事件处理程序（针对事件`event`）可以重新实现，以接收该项的焦点出事件。默认实现不做任何事。

### `QGraphicsItem *QGraphicsItem::focusProxy() const`

**作用与语义：**

返回该物品的焦点代理，或者如果没有焦点代理则返回`nullptr`。

### `void QGraphicsItem::grabKeyboard()`

**作用与语义：**

接键盘输入。
该物品将接收所有键盘输入场景，直到以下事件之一发生：
- 物品变得隐形
- 该物品从现场移除
- 该项目被删除
- 该物品调用`ungrabKeyboard()`
- 另一个项目调用 grabKeyboard();当另一个项目调用 `ungrabKeyboard()` 时，该物品将重新获得键盘抓取。
当物品获得键盘抓取时，会触发`QEvent::GrabKeyboard`事件。失去抓键盘时，会触发`QEvent::UngrabKeyboard`事件。这些事件可以用来检测你的物品是否通过获得输入焦点以外的方式获得或失去。
在Qt中几乎不需要明确抓键盘，因为Qt会理智地抓握并放开键盘。特别是，当你的物品获得输入焦点时，Qt会抓住键盘，当物品失去输入焦点或物品被隐藏时，Qt会松开键盘。
注意，只有可见的物品才能抓取键盘输入。调用 grabKeyboard() 对不可见的物品没有影响。
键盘事件不受影响。

### `void QGraphicsItem::grabMouse()`

**作用与语义：**

抓取鼠标输入。
该物品将接收该场景中所有鼠标事件，直到以下任一事件发生：
- 物品变得隐形
- 该物品从现场移除
- 该项目被删除
- 项目调用`ungrabMouse()`
- 另一个物品调用 grabMouse();当另一个物品调用 `ungrabMouse()` 时，该物品将重新获得鼠标抓取。
当物品获得鼠标抓取时，会收到`QEvent::GrabMouse`事件。失去抓鼠时，会收到`QEvent::UngrabMouse`事件。这些事件可以用来检测你的物品是否获得或失去抓鼠，除了接收鼠标按钮事件之外。
在 Qt 中几乎不需要明确抓取鼠标，因为 Qt 会合理地抓取和放开鼠标。特别是，当你按下鼠标按钮时，Qt 会抓住鼠标，直到你松开最后一个鼠标按钮。此外，`Qt::Popup`小部件在显示时隐式调用 grabMouse()，隐藏时调用 `ungrabMouse()`。
注意，只有可见的物品可以抓取鼠标输入。调用 grabMouse() 对不可见的物品没有影响。
键盘事件不受影响。

### `QGraphicsEffect *QGraphicsItem::graphicsEffect() const`

**作用与语义：**

如果该物品有效果，则返回指向该物品的指针;否则`nullptr`。

### `QGraphicsItemGroup *QGraphicsItem::group() const`

**作用与语义：**

返回指向该项的项组指针，若该项不属于组则返回`nullptr`。

### `bool QGraphicsItem::hasCursor() const`

**作用与语义：**

如果该项有光标集，返回`true`;否则返回 false。
默认情况下，物品没有设置任何光标。`cursor()`会返回一个标准的指向箭头光标。

### `bool QGraphicsItem::hasFocus() const`

**作用与语义：**

如果该项处于激活状态，且该项或其焦点代理具有键盘输入焦点，返回`true`;否则返回`false`。

### `void QGraphicsItem::hide()`

**作用与语义：**

隐藏物品（物品默认可见）。
这个便利函数等同于调用`setVisible(false)`。

### `[virtual protected] void QGraphicsItem::hoverEnterEvent(QGraphicsSceneHoverEvent *event)`

**作用与语义：**

对于事件`event`，这个事件处理程序可以重新实现，以接收该项的悬停进入事件。默认实现调用`update()`;否则不做任何事。
打电话给`QEvent::ignore()`或`QEvent::accept()` `event`没有效果。

### `[virtual protected] void QGraphicsItem::hoverLeaveEvent(QGraphicsSceneHoverEvent *event)`

**作用与语义：**

该事件处理程序对于事件`event`，可以重新实现以接收该项的悬停离开事件。默认实现调用`update()`;否则不做任何事。
打电话给`QEvent::ignore()`或`QEvent::accept()` `event`没有任何效果。

### `[virtual protected] void QGraphicsItem::hoverMoveEvent(QGraphicsSceneHoverEvent *event)`

**作用与语义：**

该事件处理程序（事件`event`）可以重新实现以接收该项的悬停移动事件。默认实现不做任何操作。
`event`打电话给`QEvent::ignore()`或`QEvent::accept()`没有任何效果。

### `[virtual protected] void QGraphicsItem::inputMethodEvent(QInputMethodEvent *event)`

**作用与语义：**

该事件处理程序对于事件`event`，可以重新实现以接收该项的输入法事件。默认实现忽略该事件。

### `Qt::InputMethodHints QGraphicsItem::inputMethodHints() const`

**作用与语义：**

返回该项当前输入法的提示。
输入法提示仅对输入项相关。输入法用提示指示其应如何操作。例如，如果设置了 Qt：：ImhNumbersOnly 标志，输入法可能会改变其视觉成分，反映只能输入数字。
不同输入法实现的效果可能有所不同。

### `[virtual protected] QVariant QGraphicsItem::inputMethodQuery(Qt::InputMethodQuery query) const`

**作用与语义：**

该方法仅适用于输入项。输入方法用它来查询一组项的属性，以支持复杂的输入法操作，如支持周围文本和重新转换。`query` 指定查询的属性。

### `void QGraphicsItem::installSceneEventFilter(QGraphicsItem *filterItem)`

**作用与语义：**

在`filterItem`上安装该项的事件过滤器，使所有该项的事件先通过`filterItem`的`sceneEventFilter()`函数。
要筛选另一个项目的事件，可以将该项目安装为另一个项目的事件过滤器。示例：
一个物品只能过滤同一场景中其他物品的事件。此外，物品不能过滤自己的事件;相反，你可以直接重新实现`sceneEvent()`。
物品必须属于场景，才能安装和使用场景事件过滤器。

**官方示例：**

```cpp
 QGraphicsScene scene;
 QGraphicsEllipseItem *ellipse = scene.addEllipse(QRectF(-10, -10, 20, 20));
 QGraphicsLineItem *line = scene.addLine(QLineF(-10, -10, 20, 20));

 line->installSceneEventFilter(ellipse);
 // line's events are filtered by ellipse's sceneEventFilter() function.

 ellipse->installSceneEventFilter(line);
 // ellipse's events are filtered by line's sceneEventFilter() function.
```

### `bool QGraphicsItem::isActive() const`

**作用与语义：**

如果该项目处于激活状态，返回`true`;否则返回`false`。
一个物品只有在场景处于激活状态时才会处于激活状态。一个物品如果是活跃面板，或者它是活跃面板的后代，则该物品是激活的。非活跃面板中的物品则不是激活的。
当场景没有激活面板时，不属于面板的物品会在场景激活后继续。
只有主动物品才能获得输入焦点。

### `bool QGraphicsItem::isAncestorOf(const QGraphicsItem *child) const`

**作用与语义：**

如果该物品是`child`的祖先（即该物品是`child`的父项，还是`child`的父项之一），返回`true`。

### `bool QGraphicsItem::isBlockedByModalPanel(QGraphicsItem **blockingPanel = nullptr) const`

**作用与语义：**

如果该项被模态面板阻塞，返回`true`，否则返回false。如果`blockingPanel`非零，`blockingPanel`将设置为阻挡该项的模态面板。如果该项未被阻塞，`blockingPanel`不会被该函数设置。
对于场景中不存在的物品，这个函数总是返回`false`。

### `bool QGraphicsItem::isClipped() const`

**作用与语义：**

如果该项目被裁剪，返回`true`。如果该项目设置了`ItemClipsToShape`标志，或者其任何前祖设置了`ItemClipsChildrenToShape`标志，则该项目被裁剪。
裁剪会影响物品的外观（即涂装），以及鼠标和悬停事件的传递。

### `bool QGraphicsItem::isEnabled() const`

**作用与语义：**

如果该项被启用，返回`true`;否则返回 false。

### `bool QGraphicsItem::isObscured(const QRectF &rect = QRectF()) const`

**作用与语义：**

如果 `rect` 被其上方任何碰撞物体的完全不透明形状完全遮挡（即其 Z 值高于此物体），则返回 `true`。

### `bool QGraphicsItem::isObscured(qreal x, qreal y, qreal w, qreal h) const`

**作用与语义：**

这个便捷函数等同于调用 isObscured(`QRectF`(`x`, `y`, `w`, `h`))。

### `[virtual] bool QGraphicsItem::isObscuredBy(const QGraphicsItem *item) const`

**作用与语义：**

如果该物品的边界矩形完全被不透明的`item`形状遮挡，返回`true`。
基础实现将`item`的`opaqueArea()`映射到该项目的坐标系，然后检查该项目的 `boundingRect()` 是否完全包含在映射形状内。
你可以重新实现这个函数，提供一个自定义算法来判断该项目是否被`item`遮挡。

### `bool QGraphicsItem::isPanel() const`

**作用与语义：**

如果物品是面板，返回`true`;否则返回`false`。

### `bool QGraphicsItem::isSelected() const`

**作用与语义：**

如果选择该项，返回`true`;否则返回 false。
属于某一组的项目继承该组所选状态。
物品默认不会被选中。

### `bool QGraphicsItem::isUnderMouse() const`

**作用与语义：**

如果该项当前处于某个视图的鼠标光标下方，则返回`true`;否则返回 false。

### `bool QGraphicsItem::isVisible() const`

**作用与语义：**

如果该项目可见，返回`true`;否则返回false。
注意，物品的整体可见性与`QGraphicsView`是否实际可见无关。

### `bool QGraphicsItem::isVisibleTo(const QGraphicsItem *parent) const`

**作用与语义：**

如果`parent`可见，返回`true`;否则返回false。`parent`可以`nullptr`，此时该函数无论该物品是否被场景可见，都会返回。
即使 `isVisible()` 为真，某个项也可能对其祖先不可见。即使 为假，`isVisible()`也可能对其祖先显示。如果任何祖先被隐藏，该项本身也会被隐式隐藏，此时该函数将返回 false。

### `bool QGraphicsItem::isWidget() const`

**作用与语义：**

如果该项是小部件（即`QGraphicsWidget`），返回 `true`;否则返回 `false`。

### `bool QGraphicsItem::isWindow() const`

**作用与语义：**

如果该项是`QGraphicsWidget`窗口，返回`true`，否则返回false。

### `[virtual protected] QVariant QGraphicsItem::itemChange(QGraphicsItem::GraphicsItemChange change, const QVariant &value)`

**作用与语义：**

`QGraphicsItem`调用这个虚拟函数，用来通知自定义项目的某个部分状态发生变化。通过重新实现该函数，你可以对变化做出反应，在某些情况下（取决于`change`）还可以进行调整。
`change` 是正在变化的项目参数。`value` 是新的值;值的类型取决于`change`。
默认实现不做任何操作，返回`value`。
注意：某些`QGraphicsItem`函数无法在该函数的重实现中调用;详情请参见`GraphicsItemChange`文档。

**官方示例：**

```cpp
 QVariant Component::itemChange(GraphicsItemChange change, const QVariant &value)
 {
     if (change == ItemPositionChange && scene()) {
         // value is the new position.
         QPointF newPos = value.toPointF();
         QRectF rect = scene()->sceneRect();
         if (!rect.contains(newPos)) {
             // Keep the item inside the scene rect.
             newPos.setX(qMin(rect.right(), qMax(newPos.x(), rect.left())));
             newPos.setY(qMin(rect.bottom(), qMax(newPos.y(), rect.top())));
             return newPos;
         }
     }
     return QGraphicsItem::itemChange(change, value);
 }
```

### `QTransform QGraphicsItem::itemTransform(const QGraphicsItem *other, bool *ok = nullptr) const`

**作用与语义：**

返回一个`QTransform`，将该项的坐标映射到`other`。如果`ok`不是空，且不存在此类变换，`ok`指向的布尔值将设为假;否则设为真。
该变换提供了`mapToItem()`或`mapFromItem()`函数的替代方案，通过返回相应的变换，使你能够自己映射形状和坐标。它还帮助你在重复映射同一两个元素时编写更高效的代码。
注意：在极少数情况下，没有转换能映射两个物品之间的变换。

### `[virtual protected] void QGraphicsItem::keyPressEvent(QKeyEvent *event)`

**作用与语义：**

对于事件`event`，这个事件处理程序可以重新实现，以接收该项的按键事件。默认实现会忽略该事件。如果你重新实现这个处理程序，事件默认会被接受。
注意，键事件只会针对设置`ItemIsFocusable`标志且具有键盘输入焦点的物品。

### `[virtual protected] void QGraphicsItem::keyReleaseEvent(QKeyEvent *event)`

**作用与语义：**

该事件处理程序（针对事件`event`）可以重新实现，以接收该项的密钥释放事件。默认实现忽略该事件。如果你重新实现该处理程序，事件默认会被接受。
注意，按键事件只会被设置`ItemIsFocusable`标志且带有键盘输入焦点的物品接收。

### `QPainterPath QGraphicsItem::mapFromItem(const QGraphicsItem *item, const QPainterPath &path) const`

**作用与语义：**

将`item`坐标系中的路径`path`映射到该项的坐标系，并返回映射后的路径。
如果`item` 是`nullptr`，该函数返回的效果与 `mapFromScene()` 相同。

### `QPointF QGraphicsItem::mapFromItem(const QGraphicsItem *item, const QPointF &point) const`

**作用与语义：**

将`item`坐标系中的点`point`映射到该项的坐标系，并返回映射后的坐标。
如果`item` `nullptr`，该函数返回的效果与 `mapFromScene()` 相同。

### `QPolygonF QGraphicsItem::mapFromItem(const QGraphicsItem *item, const QPolygonF &polygon) const`

**作用与语义：**

将`item`坐标系中的多边形`polygon`映射到该项的坐标系，并返回映射后的多边形。
如果`item` `nullptr`，该函数返回的效果与 `mapFromScene()` 相同。

### `QPolygonF QGraphicsItem::mapFromItem(const QGraphicsItem *item, const QRectF &rect) const`

**作用与语义：**

将`item`坐标系中的矩形`rect`映射到该项的坐标系，并将映射后的矩形返回为多边形。
如果`item` `nullptr`，该函数返回的效果与 `mapFromScene()` 相同。

### `QPolygonF QGraphicsItem::mapFromItem(const QGraphicsItem *item, qreal x, qreal y, qreal w, qreal h) const`

**作用与语义：**

这个便捷函数等同于调用 mapFromItem(item, `QRectF`(`x`, `y`, `w`, `h`))。

### `QPointF QGraphicsItem::mapFromItem(const QGraphicsItem *item, qreal x, qreal y) const`

**作用与语义：**

这个便捷函数等同于调用 mapFromItem(`item`, `QPointF`(`x`, `y`))。

### `QPainterPath QGraphicsItem::mapFromParent(const QPainterPath &path) const`

**作用与语义：**

将路径`path`（位于该项目父坐标系）映射到该项目的坐标系，并返回映射后的路径。

### `QPointF QGraphicsItem::mapFromParent(const QPointF &point) const`

**作用与语义：**

将该项目父坐标系中的点`point`映射到该项目的坐标系，并返回映射后的坐标。

### `QPolygonF QGraphicsItem::mapFromParent(const QPolygonF &polygon) const`

**作用与语义：**

将该项目父坐标系中的多边形`polygon`映射到该项目的坐标系，并返回映射后的多边形。

### `QPolygonF QGraphicsItem::mapFromParent(const QRectF &rect) const`

**作用与语义：**

将该项父坐标系中的矩形`rect`映射到该项的坐标系，并将映射后的矩形返回为多边形。

### `QPolygonF QGraphicsItem::mapFromParent(qreal x, qreal y, qreal w, qreal h) const`

**作用与语义：**

该便利函数等价于调用 `mapFromItem`（`QRectF`（`x`， `y`， `w`， `h`））。

### `QPointF QGraphicsItem::mapFromParent(qreal x, qreal y) const`

**作用与语义：**

这个便利函数等同于调用 mapFromParent(`QPointF`(`x`, `y`))。

### `QPainterPath QGraphicsItem::mapFromScene(const QPainterPath &path) const`

**作用与语义：**

将该场景坐标系中的路径`path`映射到该项目的坐标系，并返回映射后的路径。

### `QPointF QGraphicsItem::mapFromScene(const QPointF &point) const`

**作用与语义：**

将该物体场景坐标系中的点`point`映射到该物体的坐标系，并返回映射后的坐标。

### `QPolygonF QGraphicsItem::mapFromScene(const QPolygonF &polygon) const`

**作用与语义：**

将该物品场景坐标系中的多边形`polygon`映射到该物品的坐标系，并返回映射后的多边形。

### `QPolygonF QGraphicsItem::mapFromScene(const QRectF &rect) const`

**作用与语义：**

将该元素场景坐标系中的矩形 `rect` 映射到该元素的坐标系，并将映射后的矩形返回为多边形。

### `QPolygonF QGraphicsItem::mapFromScene(qreal x, qreal y, qreal w, qreal h) const`

**作用与语义：**

这个便捷函数等效于调用 mapFromScene(`QRectF`(`x`, `y`, `w`, `h`))。

### `QPointF QGraphicsItem::mapFromScene(qreal x, qreal y) const`

**作用与语义：**

这个便捷函数等同于调用 mapFromScene(`QPointF`(`x`, `y`))。

### `QRectF QGraphicsItem::mapRectFromItem(const QGraphicsItem *item, const QRectF &rect) const`

**作用与语义：**

将`item`坐标系中的矩形`rect`映射到该项的坐标系，并将映射后的矩形返回为新的矩形（即所得多边形的边界矩形）。
如果`item` `nullptr`，该函数返回的效果与 `mapRectFromScene()` 相同。

### `QRectF QGraphicsItem::mapRectFromItem(const QGraphicsItem *item, qreal x, qreal y, qreal w, qreal h) const`

**作用与语义：**

这个便捷函数等同于调用 mapRectFromItem(item, `QRectF`(`x`, `y`, `w`, `h`))。

### `QRectF QGraphicsItem::mapRectFromParent(const QRectF &rect) const`

**作用与语义：**

将该项父坐标系中的矩形 `rect` 映射到该项的坐标系，并将映射后的矩形返回为新的矩形（即所得多边形的边界矩形）。

### `QRectF QGraphicsItem::mapRectFromParent(qreal x, qreal y, qreal w, qreal h) const`

**作用与语义：**

这个便捷函数等同于调用 mapRectFromParent(`QRectF`(`x`, `y`, `w`, `h`))。

### `QRectF QGraphicsItem::mapRectFromScene(const QRectF &rect) const`

**作用与语义：**

将矩形 `rect`（场景坐标）映射到该项的坐标系，并将映射后的矩形返回为新矩形（即所得多边形的边界矩形）。

### `QRectF QGraphicsItem::mapRectFromScene(qreal x, qreal y, qreal w, qreal h) const`

**作用与语义：**

这个便捷函数等同于调用 mapRectFromScene(`QRectF`(`x`, `y`, `w`, `h`))。

### `QRectF QGraphicsItem::mapRectToItem(const QGraphicsItem *item, const QRectF &rect) const`

**作用与语义：**

将该项坐标系中的矩形`rect`映射到`item`的坐标系，并将映射后的矩形返回为新矩形（即所得多边形的边界矩形）。
如果`item` `nullptr`，该函数返回的效果与 `mapRectToScene()` 相同。

### `QRectF QGraphicsItem::mapRectToItem(const QGraphicsItem *item, qreal x, qreal y, qreal w, qreal h) const`

**作用与语义：**

这个便捷函数等同于调用 mapRectToItem(item, `QRectF`(`x`, `y`, `w`, `h`))。

### `QRectF QGraphicsItem::mapRectToParent(const QRectF &rect) const`

**作用与语义：**

将该项坐标系中的矩形`rect`映射到其父坐标系，并将映射后的矩形返回为新矩形（即所得多边形的边界矩形）。

### `QRectF QGraphicsItem::mapRectToParent(qreal x, qreal y, qreal w, qreal h) const`

**作用与语义：**

这个便捷函数等同于调用 mapRectToParent(`QRectF`(`x`, `y`, `w`, `h`))。

### `QRectF QGraphicsItem::mapRectToScene(const QRectF &rect) const`

**作用与语义：**

将该项目坐标系中的矩形 `rect` 映射到场景坐标系，并将映射后的矩形返回为新矩形（即所得多边形的边界矩形）。

### `QRectF QGraphicsItem::mapRectToScene(qreal x, qreal y, qreal w, qreal h) const`

**作用与语义：**

这个便捷函数等同于调用 mapRectToScene(`QRectF`(`x`, `y`, `w`, `h`))。

### `QPainterPath QGraphicsItem::mapToItem(const QGraphicsItem *item, const QPainterPath &path) const`

**作用与语义：**

将该项目坐标系中的路径`path`映射到`item`的坐标系，并返回映射后的路径。
如果`item` `nullptr`，该函数返回的效果与 `mapToScene()` 相同。

### `QPointF QGraphicsItem::mapToItem(const QGraphicsItem *item, const QPointF &point) const`

**作用与语义：**

将该项坐标系中的点`point`映射到`item`的坐标系，并返回映射后的坐标。
如果`item` `nullptr`，该函数返回的效果与 `mapToScene()` 相同。

### `QPolygonF QGraphicsItem::mapToItem(const QGraphicsItem *item, const QPolygonF &polygon) const`

**作用与语义：**

将该项坐标系中的多边形`polygon`映射到`item`的坐标系，并返回映射后的多边形。
如果`item` `nullptr`，该函数返回的效果与 `mapToScene()` 相同。

### `QPolygonF QGraphicsItem::mapToItem(const QGraphicsItem *item, const QRectF &rect) const`

**作用与语义：**

将该项坐标系中的矩形`rect`映射到`item`的坐标系，并将映射后的矩形返回为多边形。
如果`item` `nullptr`，该函数返回的效果与`mapToScene()`相同。

### `QPolygonF QGraphicsItem::mapToItem(const QGraphicsItem *item, qreal x, qreal y, qreal w, qreal h) const`

**作用与语义：**

这个便捷函数等同于调用 mapToItem(item, `QRectF`(`x`, `y`, `w`, `h`))。

### `QPointF QGraphicsItem::mapToItem(const QGraphicsItem *item, qreal x, qreal y) const`

**作用与语义：**

这个便捷函数等同于调用 mapToItem(`item`, `QPointF`(`x`, `y`))。

### `QPainterPath QGraphicsItem::mapToParent(const QPainterPath &path) const`

**作用与语义：**

将该项目坐标系中的路径`path`映射到其父坐标系，并返回映射后的路径。如果该项目没有父节点，`path`将映射到场景的坐标系。

### `QPointF QGraphicsItem::mapToParent(const QPointF &point) const`

**作用与语义：**

将该项目坐标系中的点`point`映射到其父坐标系，并返回映射后的坐标。如果该项目没有父坐标，`point`将映射到场景的坐标系。

### `QPolygonF QGraphicsItem::mapToParent(const QPolygonF &polygon) const`

**作用与语义：**

将该项目坐标系中的多边形`polygon`映射到其父坐标系，并返回映射后的多边形。如果该项目没有父，`polygon`将映射到场景的坐标系。

### `QPolygonF QGraphicsItem::mapToParent(const QRectF &rect) const`

**作用与语义：**

将该元素坐标系中的矩形`rect`映射到其父坐标系，并将映射后的矩形返回为多边形。如果该物体没有父，`rect`将映射到场景的坐标系。

### `QPolygonF QGraphicsItem::mapToParent(qreal x, qreal y, qreal w, qreal h) const`

**作用与语义：**

这个便捷函数等效于调用 mapToParent(`QRectF`(`x`, `y`, `w`, `h`))。

### `QPointF QGraphicsItem::mapToParent(qreal x, qreal y) const`

**作用与语义：**

这个便捷函数等同于调用 mapToParent(`QPointF`(`x`, `y`))。

### `QPainterPath QGraphicsItem::mapToScene(const QPainterPath &path) const`

**作用与语义：**

将该项目坐标系中的路径`path`映射到场景的坐标系，并返回映射后的路径。

### `QPointF QGraphicsItem::mapToScene(const QPointF &point) const`

**作用与语义：**

将该项目坐标系中的点`point`映射到场景坐标系，并返回映射后的坐标。

### `QPolygonF QGraphicsItem::mapToScene(const QPolygonF &polygon) const`

**作用与语义：**

将该项目坐标系中的多边形`polygon`映射到场景坐标系，并返回映射后的多边形。

### `QPolygonF QGraphicsItem::mapToScene(const QRectF &rect) const`

**作用与语义：**

将该元素坐标系中的矩形`rect`映射到场景坐标系，并将映射后的矩形返回为多边形。

### `QPolygonF QGraphicsItem::mapToScene(qreal x, qreal y, qreal w, qreal h) const`

**作用与语义：**

这个便捷函数等效于调用 mapToScene(`QRectF`(`x`, `y`, `w`, `h`))。

### `QPointF QGraphicsItem::mapToScene(qreal x, qreal y) const`

**作用与语义：**

这个便捷函数等同于调用 mapToScene(`QPointF`(`x`, `y`))。

### `[virtual protected] void QGraphicsItem::mouseDoubleClickEvent(QGraphicsSceneMouseEvent *event)`

**作用与语义：**

该事件处理程序对于事件`event`，可以重新实现以接收该项的鼠标双击事件。
双击物品时，该物品首先会触发鼠标按键事件，接着是释放事件（即点击），再是双击事件，最后是释放事件。
打电话给`QEvent::ignore()`或`QEvent::accept()` `event`没有任何效果。
默认实现调用`mousePressEvent()`。如果你想在重现这个函数时保留基础实现，可以在你的重实现中调用QGraphicsItem：：mouseDoubleClickEvent()。
注意，如果物品既非`selectable`也非`movable`，则不会触发双击事件（此时忽略单次鼠标点击，导致双击生成停止）。

### `[virtual protected] void QGraphicsItem::mouseMoveEvent(QGraphicsSceneMouseEvent *event)`

**作用与语义：**

该事件处理程序对于事件`event`，可以重新实现以接收该物品的鼠标移动事件。如果你收到该事件，可以确定该物品也收到了鼠标按键事件，并且该物品是当前的鼠标抓取器。
打电话给`QEvent::ignore()`或`QEvent::accept()` `event`没有效果。
默认实现处理基本的项目交互，比如选择和移动。如果你想在重现这个函数时保留基础实现，可以在你的重实现中调用 QGraphicsItem：：mouseMoveEvent()。
请注意，`mousePressEvent()`决定接收鼠标事件的图形项目。详情请参见`mousePressEvent()`描述。

### `[virtual protected] void QGraphicsItem::mousePressEvent(QGraphicsSceneMouseEvent *event)`

**作用与语义：**

该事件处理程序用于事件`event`，可以重新实现以接收该物品的鼠标按键事件。鼠标按键事件只传递给接受被按下鼠标按钮的物品。默认情况下，物品接受所有鼠标按键，但你可以通过调用`setAcceptedMouseButtons()`来更改。
鼠标按键事件决定哪个物品应成为鼠标抓取器（见`QGraphicsScene::mouseGrabberItem()`）。如果不重新实现此功能，按键事件将传播到该物品下方的最顶端任何物品，且不会有其他鼠标事件传递到该物品。
如果你重新实现了这个功能，`event`默认会被接受（见 `QEvent::accept()`），这个物品就是鼠标抓取器。这允许该物品接收未来的移动、释放和双击事件。如果你在 `event` 调用 `QEvent::ignore()`，这个物品将失去抓取鼠标，`event`会传播到最下面的任何物品。除非收到新的鼠标按键事件，否则不会再给该物品发送鼠标事件。
默认实现处理基本的物品交互，比如选择和移动。如果你想在重现这个函数时保留基础实现，可以在重构中调用 QGraphicsItem：：mousePressEvent()。
对于既非`movable`也非`selectable`的物品，事件为`QEvent::ignore()`d。

### `[virtual protected] void QGraphicsItem::mouseReleaseEvent(QGraphicsSceneMouseEvent *event)`

**作用与语义：**

该事件处理程序对于事件`event`，可以重新实现以接收该项的鼠标释放事件。
`QEvent::ignore()`或`QEvent::accept()`对`event`没有影响。
默认实现处理基本的物品操作，比如选择和移动。如果你想在重现这个函数时保留基础实现，可以在重写中调用 QGraphicsItem：：mouseReleaseEvent()。
请注意，`mousePressEvent()`决定接收鼠标事件的图形项目。详情请参见`mousePressEvent()`描述。

### `void QGraphicsItem::moveBy(qreal dx, qreal dy)`

**作用与语义：**

横向移动`dx`点，垂直移动`dy`点。该函数等同于调用 `setPos`（`pos()` `QPointF`（`dx`， `dy`））。

### `qreal QGraphicsItem::opacity() const`

**作用与语义：**

返回该项的局部不透明度，介于0.0（透明）和1.0（不透明）之间。该值与父值和祖先值合并到`effectiveOpacity()`中。有效不透明度决定了该项的渲染方式，也影响其在被`QGraphicsView::items()`等函数查询时的可见性。
不透明度属性决定了传递给`paint()`函数的绘画器状态。如果该项被缓存，即`ItemCoordinateCache`或`DeviceCoordinateCache`，则在渲染过程中，有效属性将应用到该缓存上。
默认不透明度为1.0;完全不透明。

### `[virtual] QPainterPath QGraphicsItem::opaqueArea() const`

**作用与语义：**

该虚拟函数返回一个形状，表示该项不透明的区域。如果该区域用不透明的画笔或颜色填充（即不透明），则该区域是不透明的。
该函数由 `isObscuredBy()` 使用，底层项目调用以判断其是否被该项遮挡。
默认实现返回空`QPainterPath`，表明该项完全透明且未遮挡其他项。

### `[pure virtual] void QGraphicsItem::paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget = nullptr)`

**作用与语义：**

该函数通常由`QGraphicsView`调用，它将物品的内容绘制在局部坐标中。
在`QGraphicsItem`子类中重新实现该函数，以提供该物品的绘画实现，使用`painter`。`option`参数为物品提供样式选项，如状态、曝光区域和细节层级提示。`widget`参数为可选。如果提供了，它指向正在绘制的控件;否则为0。对于缓存绘制，`widget`总是为0。
画家的钢笔默认为0宽，笔初始化为油漆设备调色板中的`QPalette::Text`刷。画笔初始化为`QPalette::Window`。
确保所有绘画都限制在`boundingRect()`边界内，以避免渲染伪影（因为`QGraphicsView`不会为你裁剪画家）。特别是，当`QPainter`用指定`QPen`渲染形状轮廓时，轮廓的一半会在外侧绘制，另一半在你正在渲染的形状内侧（例如，笔宽为2单位时，你必须在`boundingRect()`内绘制1单位的轮廓）。`QGraphicsItem`不支持使用宽度非零的美观笔。
所有涂装均在本地坐标内完成。
注意：除非调用`update()`，否则物品必须始终以完全相同的方式重新绘制自己;否则可能会出现视觉伪影。换句话说，两次后续的paint()调用必须始终产生相同的输出，除非它们之间调用了`update()`。
注意：启用缓存并不保证图形视图框架只调用一次 paint()，即使没有明确调用 `update()`。详情请参见 `setCacheMode()` 文档。

**官方示例：**

```cpp
 void RoundRectItem::paint(QPainter *painter,
                           const QStyleOptionGraphicsItem *option,
                           QWidget *widget)
 {
     painter->drawRoundedRect(-10, -10, 20, 20, 5, 5);
 }
```

### `QGraphicsItem *QGraphicsItem::panel() const`

**作用与语义：**

返回该物品的面板，或者如果该物品没有面板，则返回`nullptr`。如果物品是面板，它会返回自己。否则，它会返回最近的面板祖先。

### `QGraphicsItem::PanelModality QGraphicsItem::panelModality() const`

**作用与语义：**

返回该物品的模态。

### `QGraphicsItem *QGraphicsItem::parentItem() const`

**作用与语义：**

返回指向该项的父项的指针。如果该项没有父项，则返回`nullptr`。

### `QGraphicsObject *QGraphicsItem::parentObject() const`

**作用与语义：**

返回指向该项父项的指针，投射为`QGraphicsObject`。如果父项不是`QGraphicsObject`，则返回`nullptr`。

### `QGraphicsWidget *QGraphicsItem::parentWidget() const`

**作用与语义：**

返回指向该项目父控件的指针。该项目的父控件是最近的控件。

### `QPointF QGraphicsItem::pos() const`

**作用与语义：**

返回该物品在父坐标中的位置。如果该物品没有父坐标，则其位置以场景坐标表示。
该项的位置描述其在父坐标中的原点（局部坐标 （0， 0））;该函数返回的 `mapToParent`（0， 0） 相同。
为了方便起见，你也可以调用 `scenePos()` 来确定该物品在场景坐标中的位置，无论其父坐标为何。

### `[protected] void QGraphicsItem::prepareGeometryChange()`

**作用与语义：**

为几何体变化做准备。在更改物品的边界矩形之前调用此函数，以保持`QGraphicsScene`索引的更新。
如果有必要，prepareGeometryChange() 将调用 `update()`。

**官方示例：**

```cpp
 void CircleItem::setRadius(qreal newRadius)
 {
     if (radius != newRadius) {
         prepareGeometryChange();
         radius = newRadius;
     }
 }
```

### `void QGraphicsItem::removeSceneEventFilter(QGraphicsItem *filterItem)`

**作用与语义：**

移除该物品的事件过滤器`filterItem`。

### `void QGraphicsItem::resetTransform()`

**作用与语义：**

将该项的变换矩阵重置为恒等矩阵或所有变换属性恢复为默认值。这等同于调用`setTransform(QTransform())`。

### `qreal QGraphicsItem::rotation() const`

**作用与语义：**

返回绕Z轴的顺时针旋转（度数）。默认值为0（即物品未旋转）。
旋转与物品的`scale()`、`transform()`和`transformations()`结合，将物品的坐标系映射到父项。

### `qreal QGraphicsItem::scale() const`

**作用与语义：**

返回该物品的比例因子。默认比例因子为1.0（即该物品未被放大）。
该比例与物品的`rotation()`、`transform()`和`transformations()`结合，将物品的坐标系映射到父物品。

### `QGraphicsScene *QGraphicsItem::scene() const`

**作用与语义：**

返回当前场景，如果物品未存储在场景中则返回`nullptr`。
要添加或移动物品到场景，请调用`QGraphicsScene::addItem()`。

### `QRectF QGraphicsItem::sceneBoundingRect() const`

**作用与语义：**

通过将`sceneTransform()`与`boundingRect()`结合，返回该项目在场景坐标中的边界矩。

### `[virtual protected] bool QGraphicsItem::sceneEvent(QEvent *event)`

**作用与语义：**

该虚拟函数接收该项的事件。在事件处理器 `contextMenuEvent()`、`focusInEvent()`、`focusOutEvent()`、`hoverEnterEvent()`、`hoverMoveEvent()`、`hoverLeaveEvent()`、`keyPressEvent()`、`keyReleaseEvent()`、`mousePressEvent()`、`mouseReleaseEvent()`、`mouseMoveEvent()` 和 `mouseDoubleClickEvent()` 之前，重新实现该函数以拦截事件。
如果事件被识别并处理，返回`true`;否则（例如，如果事件类型未被识别），返回为假。
`event` 是截获的事件。

### `[virtual protected] bool QGraphicsItem::sceneEventFilter(QGraphicsItem *watched, QEvent *event)`

**作用与语义：**

筛选项目`watched`事件。`event` 是筛选后的事件。
在子类中重新实现该函数后，该项可以作为其他项目的事件过滤器，拦截所有发送给这些项目的事件，防止它们响应。
重实现必须返回true以防止对某事件的进一步处理，确保事件不会被传递到被关注的项目，或者返回false以表示事件应由事件系统进一步传播。

### `QPointF QGraphicsItem::scenePos() const`

**作用与语义：**

返回该物品在场景坐标中的位置。这相当于调用`mapToScene(0, 0)`。

### `QTransform QGraphicsItem::sceneTransform() const`

**作用与语义：**

返回该项目的场景变换矩阵。该矩阵可用于将坐标和几何形状从该项目的局部坐标系映射到场景的坐标系。要映射场景的坐标，首先必须反转返回的矩阵。
与仅返回项局部变换的 `transform()` 不同，该函数包含项（及任何父项）的位置及所有变换属性。

**官方示例：**

```cpp
 QGraphicsRectItem rect;
 rect.setPos(100, 100);

 rect.sceneTransform().map(QPointF(0, 0));
 // returns QPointF(100, 100);

 rect.sceneTransform().inverted().map(QPointF(100, 100));
 // returns QPointF(0, 0);
```

### `void QGraphicsItem::scroll(qreal dx, qreal dy, const QRectF &rect = QRectF())`

**作用与语义：**

滚动`rect`的内容，`dx`，`dy`。如果`rect`是空矩形块（默认），则该项的边界矩形矩形被滚动。
当物品（或物品的部分）内容被垂直或水平移动时，滚动提供了一种快速的替代方式，而不仅仅是重新绘制。根据当前的变换情况和绘图设备（即视口）的能力，这种操作可能仅仅是用 memmove() 将像素从一个位置移动到另一个位置。在大多数情况下，这比重新渲染整个区域要快。
滚动后，该项目会针对新暴露的区域发送更新。如果不支持滚动（例如，你渲染到一个 OpenGL 视口，而 OpenGL 不享受滚动优化），这个函数相当于调用 update（`rect`）。
注意：只有在启用`QGraphicsItem::ItemCoordinateCache`时才支持滚动;在其他情况下，调用该函数等同于调用 update（`rect`）。如果你确定该项是不透明的，且没有与其他项重叠，你可以将`rect`映射到视口坐标并滚动视口。

**官方示例：**

```cpp
 QTransform xform = item->deviceTransform(view->viewportTransform());
 QRect deviceRect = xform.mapRect(rect).toAlignedRect();
 view->viewport()->scroll(dx, dy, deviceRect);
```

### `void QGraphicsItem::setAcceptDrops(bool on)`

**作用与语义：**

如果`on`为真，该项将接受拖放事件;否则，对拖放事件是透明的。默认情况下，物品不接受拖放事件。

### `void QGraphicsItem::setAcceptHoverEvents(bool enabled)`

**作用与语义：**

如果`enabled`为真，该项目将接受悬停事件;否则，它将忽略悬停事件。默认情况下，物品不接受悬停事件。
当当前没有鼠标抓取物品时，悬浮事件会发送。当鼠标光标进入物品、在物品内部移动时以及光标离开物品时，都会发送悬浮事件。悬浮事件通常用于在物品输入时高亮，以及跟踪鼠标光标悬停在物品上方（相当于`QWidget::mouseTracking`）。
父项目在其子节点之前接收悬停进入事件，子节点后离开事件。但如果光标进入子节点，父项目不会接收悬浮离开事件;父项目保持“悬停”状态，直到光标离开其区域，包括其子节点区域。
如果父项处理子事件，当光标经过子节点时，它会接收滑鼠移动、拖拽移动和放下事件，但不会接收代表子节点的悬停进入和悬停离开，也不会代表其子节点接收拖入和拖拽离开事件。
有窗户装饰的`QGraphicsWidget`无论`acceptHoverEvents()`值多少，都会接受悬停事件。

### `void QGraphicsItem::setAcceptTouchEvents(bool enabled)`

**作用与语义：**

如果`enabled`为真，该项将接受触碰事件;否则，它将忽略触碰事件。默认情况下，项不接受触碰事件。

### `void QGraphicsItem::setAcceptedMouseButtons(Qt::MouseButtons buttons)`

**作用与语义：**

设置该项接受鼠标事件的鼠标`buttons`。
默认情况下，所有鼠标按钮都被接受。如果某个物品接受鼠标按钮，当该按钮发送鼠标按键事件时，它将成为鼠标抓取物品。但如果该物品不接受鼠标按钮，`QGraphicsScene`会将鼠标事件转发到其下方第一个接受的物品。
要禁用某项物品的鼠标事件（即让鼠标事件透明），请调用 setAcceptedMouseButtons（`Qt::NoButton`）。

### `void QGraphicsItem::setActive(bool active)`

**作用与语义：**

如果`active`为真且场景处于激活状态，则该物品的面板将被激活。否则，面板将被关闭。
如果该物品不属于当前场景，`active`将决定场景激活或物品被添加到场景时面板的处理。如果成立，物品面板将在物品被添加到场景或场景激活时激活。否则，物品将保持非激活状态，独立于场景激活状态。

### `void QGraphicsItem::setBoundingRegionGranularity(qreal granularity)`

**作用与语义：**

将边界区域的粒度设置为`granularity`;一个介于和之间，包含0和1的值。默认值为0（即最低粒度，其中边界区域对应于该项的边界矩形）。
`boundingRegion()` 利用该粒度计算物品边界区域的细度。可实现的最高粒度为 1，其中 `boundingRegion()` 将返回相应设备的最细轮廓（例如，对于`QGraphicsView`视口，这会给出像素完美的边界区域）。最低的可能颗粒度为 0。`granularity` 的值描述了设备分辨率与边界区域分辨率的比值（例如，0.25 会给出每个区块对应 4x4 设备单位/像素的区域）。

### `void QGraphicsItem::setCacheMode(QGraphicsItem::CacheMode mode, const QSize &logicalCacheSize = QSize())`

**作用与语义：**

将物品的缓存模式设置为`mode`。
可选的 `logicalCacheSize` 参数仅用于 `ItemCoordinateCache` 模式，描述缓存缓冲区的分辨率;如果 `logicalCacheSize` 为 （100， 100），`QGraphicsItem` 会将该项放入图形内存中的 100x100 像素，无论该项本身的逻辑大小如何。默认情况下，`QGraphicsItem` 使用 `boundingRect()` 的大小。对于所有其他缓存模式，除了 `ItemCoordinateCache` ，`logicalCacheSize` 被忽略。
如果你的物品花大量时间重新绘制自己，缓存可以加快渲染速度。有时缓存也会减缓渲染速度，尤其是当物品重新绘制的时间比`QGraphicsItem`从缓存重新绘制的时间少时。
当缓存启用时，物品的`paint()`函数通常会绘制到屏幕外的像素地图缓存中;对于后续的重新绘制请求，图形视图框架会从缓存中重新绘制。这种方法在QGLWidget中表现尤为出色，它将所有缓存存储为OpenGL纹理。
请注意，`QPixmapCache`的缓存限制可能需要调整以获得最佳性能。
你可以在`CacheMode`文档中了解更多关于不同缓存模式的信息。
注意：启用缓存并不意味着项目的`paint()`函数只会在显式`update()`调用时被调用。例如，在内存压力下，Qt 可能会决定丢弃部分缓存信息;在这种情况下，即使没有`update()`调用（即没有启用缓存）也会调用该项的`paint()`函数。

### `void QGraphicsItem::setCursor(const QCursor &cursor)`

**作用与语义：**

将当前光标形状设置为`cursor`。当鼠标光标位于该物体上时，会呈现该形状。请参阅预定义光标对象列表，了解一系列有用的形状。
编辑器项目可能想使用工字束光标：
如果没有设置光标，则使用下方物品的光标。

**官方示例：**

```cpp
 item->setCursor(Qt::IBeamCursor);
```

### `void QGraphicsItem::setData(int key, const QVariant &value)`

**作用与语义：**

将该物品的密钥 `key` 自定义数据设置为 `value`。
自定义物品数据对于存储任意物品的任意属性非常有用。Qt 不使用此功能来存储数据;它仅为用户方便而提供。

### `void QGraphicsItem::setEnabled(bool enabled)`

**作用与语义：**

如果`enabled`为真，则该物品被启用;否则，该物品被禁用。
禁用物品可见，但不会接收任何事件，也不能被关注或被选择。鼠标事件会被丢弃;除非物品同时隐形，或不接受鼠标事件（见`acceptedMouseButtons()`），否则事件不会传播。禁用物品不能成为鼠标抓取器，因此，如果抓取鼠标时物品被禁用，则失去抓取能力，就像它在禁用时有焦点时失去焦点一样。
残疾物品传统上使用灰色涂色绘制（见 `QPalette::Disabled`）。
如果你禁用父项，它的所有子项也会被禁用。如果你启用父项，所有子项都会被启用，除非它们被明确禁用（例如，如果你调用 setEnabled（false），如果子项被禁用后，它不会重新启用。
物品默认是启用的。
注意：如果你安装了事件过滤器，仍然可以在事件传递到物品之前拦截它们;该机制无视物品的启用状态。

### `void QGraphicsItem::setFiltersChildEvents(bool enabled)`

**作用与语义：**

如果 `enabled` 为真，该项被设置为过滤其所有子节点的所有事件（即所有预定为其子节点的事件都被发送到该项）;否则，如果 `enabled` 为假，该项只处理自身事件。默认值为 false。

### `void QGraphicsItem::setFlag(QGraphicsItem::GraphicsItemFlag flag, bool enabled = true)`

**作用与语义：**

如果`enabled`为真，则物品标志`flag`被启用;否则，该标志被禁用。

### `void QGraphicsItem::setFlags(QGraphicsItem::GraphicsItemFlags flags)`

**作用与语义：**

将物品标志设置为`flags`。`flags`中的所有标志均已启用;所有未在`flags`中的标志均被禁用。
如果该项有焦点且`flags`未启用`ItemIsFocusable`，则该项因调用该函数而失去焦点。同样，如果该项被选中，`flags`未启用`ItemIsSelectable`，则该项自动取消选择。
默认情况下，不启用任何标志。（`QGraphicsWidget`默认启用`ItemSendsGeometryChanges`标志以跟踪位置变化。）。

### `void QGraphicsItem::setFocus(Qt::FocusReason focusReason = Qt::OtherFocusReason)`

**作用与语义：**

赋予该项的键盘输入焦点。`focusReason`参数将传递到该函数生成的任何焦点事件中;它用于解释导致该物品获得焦点的原因。
只有启用并设置`ItemIsFocusable`标志的项目才能接受键盘焦点。
如果该物品不可见、未激活或与场景无关联，则不会立即获得输入焦点。但如果它以后变得可见，它会被注册为其子树的首选焦点物品。
调用该函数后，该项目将获得一个事件焦点，且`focusReason`。如果另一个项目已有焦点，该项目将首先收到焦点出局事件，表示其失去输入焦点。

### `void QGraphicsItem::setFocusProxy(QGraphicsItem *item)`

**作用与语义：**

将物品的焦点代理设置为`item`。
如果物品有焦点代理，当物品获得输入焦点时，焦点代理会接收输入焦点。物品本身仍会有焦点（即返回`hasFocus()`），但只有焦点代理会接收键盘输入。
焦点代理本身可以有焦点代理，依此类推。在这种情况下，键盘输入由最外层焦点代理处理。
焦点代理`item`必须属于与该物品相同的场景。

### `void QGraphicsItem::setGraphicsEffect(QGraphicsEffect *effect)`

**作用与语义：**

将`effect`设置为该物品的效果。如果该物品上已经安装了效果，`QGraphicsItem`会在安装新`effect`前删除已有效果。你可以通过调用 setGraphicsEffect（`nullptr`） 删除已有效果。
如果`effect`是安装在不同物品上的效果，setGraphicsEffect() 会从该物品中移除该效果并安装到该物品上。
`QGraphicsItem`承担`effect`的责任。
注意：该函数将对自身及其所有子功能施加效果。

### `void QGraphicsItem::setGroup(QGraphicsItemGroup *group)`

**作用与语义：**

将该项添加到项目组 `group`。如果 `group` `nullptr`，该项将从当前组中移除，并作为上一个组父组的子组添加。

### `void QGraphicsItem::setInputMethodHints(Qt::InputMethodHints hints)`

**作用与语义：**

将该项当前输入法提示设置为`hints`。

### `void QGraphicsItem::setOpacity(qreal opacity)`

**作用与语义：**

将该项的局部`opacity`设为0.0（透明）和1.0（不透明）。该项的局部不透明度与父不透明度和祖先透明度合并到`effectiveOpacity()`中。
默认情况下，不透明度会从父节点传递到子节点，因此如果父节点的不透明度为0.5，而子节点也是0.5，则子节点的有效透明度为0.25。
不透明度属性决定了传递给 `paint()` 函数的绘画器状态。如果该项被缓存，即`ItemCoordinateCache`或`DeviceCoordinateCache`，则在渲染过程中，有效属性将应用到该项的缓存上。
有两个物品标志会影响物品与父节点的不透明度组合：`ItemIgnoresParentOpacity`和`ItemDoesntPropagateOpacityToChildren`。
注意：根据`isVisible()`，将某个项目的不透明度设置为0并不会使该项目变得不可见，但该项目会被视为不可见。更多信息请参见`setVisible()`文档。

### `void QGraphicsItem::setPanelModality(QGraphicsItem::PanelModality panelModality)`

**作用与语义：**

将该物品的模态设置为`panelModality`。
更改可见物品的模式即刻生效。

### `void QGraphicsItem::setParentItem(QGraphicsItem *newParent)`

**作用与语义：**

将该项的父项设置为`newParent`。如果该项已有父项，首先从前一个父项中移除。如果`newParent`为0，该项将成为顶级项。
注意，这实际上会将该图形项添加到父场景中。你不应自己将该项`add`到场景中。
当调用该函数对 `newParent` 的祖先项时，行为是未定义的。

### `void QGraphicsItem::setPos(const QPointF &pos)`

**作用与语义：**

将物品的位置设置为`pos`，属于父坐标。对于没有父元素的物品，`pos`处于场景坐标中。
该项的位置描述其在父坐标中的原点（局部坐标（0， 0））。

### `void QGraphicsItem::setPos(qreal x, qreal y)`

**作用与语义：**

这个便捷函数等同于调用 setPos(`QPointF`(`x`, `y`))。

### `void QGraphicsItem::setRotation(qreal angle)`

**作用与语义：**

将顺时针旋转`angle`，以度数为单位，绕Z轴。默认值为0（即物品未旋转）。赋值为负值则物品逆时针旋转。通常旋转角度在范围内（-360,360），但也可以分配超出范围的数值（例如，370度旋转与10度旋转相同）。
物品围绕其变换原点旋转，默认为（0， 0）。你可以通过调用`setTransformOriginPoint()`选择不同的变换原点。
旋转与物品的`scale()`、`transform()`和`transformations()`结合，将物品的坐标系映射到父项。

### `void QGraphicsItem::setScale(qreal factor)`

**作用与语义：**

设置物品的比例`factor`。默认比例因子为1.0（即物品未被缩放）。比例因子为0.0时，物品会折叠为一点。如果提供负比例因子，物品会被翻转并镜像（即旋转180度）。
该项围绕其变换原点进行缩放，默认为（0， 0）。你可以通过调用`setTransformOriginPoint()`选择不同的变换原点。
该比例与物品的`rotation()`、`transform()`和`transformations()`结合，将物品的坐标系映射到父物品。

### `void QGraphicsItem::setSelected(bool selected)`

**作用与语义：**

如果`selected`为真且该项可选择，则选择该项;否则，取消选择。
如果该项目属于某个组，则该函数会切换整个组的选择状态。如果选中了该组，组内的所有项目也会被选中;如果未选中组，则组内的项目也不会被选中。
只能选择可见、启用、可选择的项目。如果`selected`为真，且该项目是不可见、禁用或不可选择，这个函数就不做任何事。
默认情况下，物品不能被选中。要启用选择，请设置`ItemIsSelectable`标志。
该功能旨在方便地提供，允许单独切换选中状态。不过，更常见的选择方式是调用`QGraphicsScene::setSelectionArea()`，该功能会调用场景中指定区域内所有可见、启用和可选的物品。

### `void QGraphicsItem::setToolTip(const QString &toolTip)`

**作用与语义：**

将该物品的工具提示设置为`toolTip`。如果`toolTip`空，则该物品的工具提示被清除。

### `void QGraphicsItem::setTransform(const QTransform &matrix, bool combine = false)`

**作用与语义：**

将该物品的电流变换矩阵设置为`matrix`。
如果`combine`为真，则`matrix`与当前矩阵结合;否则，`matrix`替换当前矩阵。`combine`默认为假。
为了简化使用变换视图与物品的交互，`QGraphicsItem` 提供了 mapTo......和 mapFrom......这些函数可以在物品与场景坐标之间转换。例如，你可以调用 `mapToScene()` 将物品坐标映射到场景坐标，或者调用 `mapFromScene()` 将场景坐标映射到物品坐标。
变换矩阵与物品的`rotation()`、`scale()`和`transformations()`结合成一个组合变换，将物品的坐标系映射到其父项。

### `void QGraphicsItem::setTransformOriginPoint(const QPointF &origin)`

**作用与语义：**

设置项坐标变换的 `origin`点。

### `void QGraphicsItem::setTransformOriginPoint(qreal x, qreal y)`

**作用与语义：**

设置变换的原点为项目坐标。这等同于调用 setTransformOriginPoint（`QPointF`（`x`， `y`））。

### `void QGraphicsItem::setTransformations(const QList<QGraphicsTransform *> &transformations)`

**作用与语义：**

列出当前适用于该项目的图形`transformations`（`QGraphicsTransform`）。
如果你只是想旋转或缩放物品，应该调用`setRotation()`或`setScale()`。如果你想对物品设置任意变换，可以调用`setTransform()`。
`QGraphicsTransform`用于对物品应用和控制一系列单独的变换操作。它在动画中特别有用，因为每个变换操作都需要独立插值，或者以不同方式插值。
这些变换与物品的`rotation()`、`scale()`和`transform()`结合，将物品的坐标系映射到父物品。

### `void QGraphicsItem::setVisible(bool visible)`

**作用与语义：**

如果`visible`为真，则该物品会被显示为可见。否则，该物品会被隐藏。隐形物品不会被涂装，也不会接收任何事件。特别是，鼠标事件会直接穿过隐形物品，并被传递到可能在后面的任何物品上。隐形物品同样不可选择，无法获得输入焦点，也不会被`QGraphicsScene`的物品位置函数检测到。
如果物品在抓取鼠标时变得隐形（即在接收鼠标事件时），它会自动失去抓取机会，且通过重新可见该物品也无法恢复抓取;必须重新按一次鼠标才能重新获得抓取。
同样，隐形物品无法获得焦点，因此即使物品在隐形时有焦点，它会失去焦点，且仅仅让物品重新可见无法恢复焦点。
如果你隐藏了父项，它的所有子项也会被隐藏。如果你显示父项，所有子项都会显示，除非它们被明确隐藏（例如，如果你在某个子项上调用 setVisible（false），即使父项被隐藏，它也不会重新显示，然后再次显示）。
条目默认可见;无需在新条目上调用 setVisible() 。
注意：不透明度设置为0的物品仍被视为可见，但会被视为隐形物品：鼠标事件会穿过该项目，不包含在`QGraphicsView::items()`返回的物品中，依此类推。但该物品仍保留焦点。

### `void QGraphicsItem::setX(qreal x)`

**作用与语义：**

集合是该物品位置的`x`坐标。相当于调用`setPos`（x， `y()`）。

### `void QGraphicsItem::setY(qreal y)`

**作用与语义：**

集合是该物品位置的`y`坐标。相当于调用`setPos`（`x()`， y）。

### `void QGraphicsItem::setZValue(qreal z)`

**作用与语义：**

将该物品的Z值设置为`z`。Z值决定了兄弟（邻居）物品的叠加顺序。高Z值的兄弟物品总是会叠加在另一个Z值较低的兄弟物品之上。
如果你恢复了Z值，物品的插入顺序将决定其叠加顺序。
Z值不会影响物品的大小。
默认Z值为0。

### `[virtual] QPainterPath QGraphicsItem::shape() const`

**作用与语义：**

返回该项的形状，作为本地坐标中的`QPainterPath`。该形状用于多种用途，包括碰撞检测、碰撞测试以及`QGraphicsScene::items()`函数。
默认实现调用 `boundingRect()` 返回一个简单的矩形形状，但子类可以重新实现该函数，以更准确地返回非矩形物体的形状。例如，圆形项目可能选择返回椭圆形以更好地检测碰撞。例如：
形状的轮廓会根据笔的宽度和风格而有所不同。如果你想在物体的形状中包含这个轮廓，可以用`QPainterPathStroker`从笔触中创建形状。
该函数由默认实现的`contains()`和 `collidesWithPath()`调用。

**官方示例：**

```cpp
 QPainterPath RoundItem::shape() const
 {
     QPainterPath path;
     path.addEllipse(boundingRect());
     return path;
 }
```

### `void QGraphicsItem::show()`

**作用与语义：**

显示物品（默认可见物品）。
这种便利函数等价于调用`setVisible(true)`。

### `void QGraphicsItem::stackBefore(const QGraphicsItem *sibling)`

**作用与语义：**

在`sibling`之前叠加该物品，这意味着该物品会被抽到兄弟物品后面。换句话说，兄弟物品会视觉上出现在该物品的顶部。
这两个项必须是兄弟项（即它们必须共享相同的父项，或两者都必须是顶层项）。`sibling`必须与该项具有相同的Z值，否则调用该函数无效。
默认情况下，所有兄弟项目按插入顺序堆叠（即你添加的第一个物品会在下一个添加物品之前被抽取）。如果两个物品的Z值不同，则将Z值最高的物品放在最上面。当Z值相同时，插入顺序将决定叠加顺序。

### `QGraphicsObject *QGraphicsItem::toGraphicsObject()`

**作用与语义：**

如果该类实际上是图形对象，则将投射到`QGraphicsObject`的图形项返回，否则返回为0。

### `const QGraphicsObject *QGraphicsItem::toGraphicsObject() const`

**作用与语义：**

如果该类实际上是图形对象，则将投射到`QGraphicsObject`的图形项返回，否则返回为0。

### `QString QGraphicsItem::toolTip() const`

**作用与语义：**

返回该物品的工具提示，或者如果没有设置工具提示，则返回空`QString`。

### `QGraphicsItem *QGraphicsItem::topLevelItem() const`

**作用与语义：**

返回该项的最高级别项。顶层项是该项的最高祖先项，其父项为`nullptr`。如果某个项没有父项，则返回其自身的指针（即顶层项即为自身的顶层项）。

### `QGraphicsWidget *QGraphicsItem::topLevelWidget() const`

**作用与语义：**

返回指向该项目顶层控件的指针（即该项的祖先，其父节点为`nullptr`，或其父节点不是控件），如果该项目没有顶层控件，则返回`nullptr`。如果该项目本身是顶级控件，该函数返回一个指向该项目本身的指针。

### `QTransform QGraphicsItem::transform() const`

**作用与语义：**

返回该物品的变换矩阵。
变形矩阵与物品的`rotation()`、`scale()`和`transformations()`结合，形成该物品的组合变形。
默认变换矩阵是单位矩阵。

### `QPointF QGraphicsItem::transformOriginPoint() const`

**作用与语义：**

返回变换的原点，映射为物品坐标。
默认为`QPointF`（0,0）。

### `QList<QGraphicsTransform *> QGraphicsItem::transformations() const`

**作用与语义：**

返回当前适用于该项的图形变换列表。
`QGraphicsTransform`用于对物品应用和控制一系列单独的变换操作。它在动画中特别有用，因为每个变换操作都需要独立插值，或者以不同方式进行插值。
这些变换与物品的`rotation()`、`scale()`和`transform()`结合，将物品的坐标系映射到父物品。

### `[virtual] int QGraphicsItem::type() const`

**作用与语义：**

返回一个项目的类型，作为一个整数。所有标准的 Graphicsitem 类都关联一个唯一的值;参见 `QGraphicsItem::Type`。`qgraphicsitem_cast()` 利用这些类型信息来区分类型。
默认实现（`QGraphicsItem`）返回`UserType`。
要启用自定义项的 `qgraphicsitem_cast()`，请重新实现该函数并声明一个等于自定义项类型值的 enum。自定义项必须返回大于 `UserType`（65536）的值。

**官方示例：**

```cpp
 class CustomItem : public QGraphicsItem
 {
 public:
    enum { Type = UserType + 1 };

    int type() const override
    {
        // Enable the use of qgraphicsitem_cast with this item.
        return Type;
    }
    ...
 };
```

### `void QGraphicsItem::ungrabKeyboard()`

**作用与语义：**

松开抓键盘。

### `void QGraphicsItem::ungrabMouse()`

**作用与语义：**

松开鼠标抓取。

### `void QGraphicsItem::unsetCursor()`

**作用与语义：**

清除此项目的光标。

### `void QGraphicsItem::update(const QRectF &rect = QRectF())`

**作用与语义：**

安排该物品中`rect`覆盖区域的重新绘制。每当物品需要重新绘制时，比如外观或大小变化，你可以调用此函数。
该函数不会立即绘制;而是安排绘画请求，在控制到达事件循环后由`QGraphicsView`处理。只有当该物品在任何关联视图中可见时，才会重新绘制。
作为重新涂装的副产品，覆盖`rect`区域的其他物品也可能被重新喷涂。
如果该项是不可见的（即返回`isVisible()`返回`false`），该函数不做任何事。

### `void QGraphicsItem::update(qreal x, qreal y, qreal width, qreal height)`

**作用与语义：**

此便利函数等同于调用 update(`QRectF`(`x`, `y`, `width`, `height`))。

### `[protected] void QGraphicsItem::updateMicroFocus()`

**作用与语义：**

更新物品的微焦点。

### `[virtual protected] void QGraphicsItem::wheelEvent(QGraphicsSceneWheelEvent *event)`

**作用与语义：**

该事件处理程序用于事件`event`，可以重新实现以接收该项的轮子事件。如果您重新实现该函数，默认`event`会被接受。
如果你忽略该事件（即调用`QEvent::ignore()`），它会传播到该事件下方的任何项目。如果没有项目接受该事件，场景会忽略它，并传播到视图（例如视图的垂直滚动条）。
默认实现会忽略该事件。

### `QGraphicsWidget *QGraphicsItem::window() const`

**作用与语义：**

返回该项目的窗口，或者如果该项目没有窗口，则返回`nullptr`。如果该项目是窗口，它会返回自己。否则，它将返回最近的窗口祖先。

### `qreal QGraphicsItem::x() const`

**作用与语义：**

该便利函数等价于调用 `pos()`.x()。

### `qreal QGraphicsItem::y() const`

**作用与语义：**

此便利函数等同于调用 `pos()`.y()。

### `qreal QGraphicsItem::zValue() const`

**作用与语义：**

返回该项的Z值。Z值影响兄弟（邻居）项的叠加顺序。
默认Z值为0。

### `template <typename T> T qgraphicsitem_cast(QGraphicsItem *item)`

**作用与语义：**

如果`item`类型为T，则返回给定的`item`投为类型T;否则返回`nullptr`。
注意：为了让这个函数在自定义物品中正确工作，请为每个自定义`QGraphicsItem`子类重新实现`type()`函数。

### `enum GraphicsItemFlag { ItemIsMovable, ItemIsSelectable, ItemIsFocusable, ItemClipsToShape, ItemClipsChildrenToShape, …, ItemContainsChildrenInShape }`

**作用与语义：**

这个枚举描述了你可以在物品上设置的不同标志，以切换物品行为中的不同功能。
所有标志默认都是被禁用的。
- `QGraphicsItem::ItemIsMovable`：`0x1`;该项目支持使用鼠标进行交互移动。点击该项目并拖动，该物品会与鼠标光标一起移动。如果该项目有子节点，所有子节点也会被移动。如果该项目是选择的一部分，所有被选中的项目也会被移动。此功能通过`QGraphicsItem`鼠标事件处理程序的基础实现提供了便利性。
- `QGraphicsItem::ItemIsSelectable`：`0x2`;该物品支持选择。启用此功能后，`setSelected()`可以切换该物品的选择。它还可以通过调用`QGraphicsScene::setSelectionArea()`、点击物品或在`QGraphicsView`中使用橡皮筋选择自动选择该物品。
- `QGraphicsItem::ItemIsFocusable`：`0x4`;该项目支持键盘输入焦点（即输入项目）。启用该标志后，项目可以接受焦点，从而再次将按键事件传递到`QGraphicsItem::keyPressEvent()`和`QGraphicsItem::keyReleaseEvent()`。
- `QGraphicsItem::ItemClipsToShape`：`0x8`;物品会剪辑到自身形状。物品不能绘制或接收鼠标、平板、拖拽或悬停事件。默认情况下禁用该功能。此行为由QGraphicsView：:d rawItems()或QGraphicsScene：:d rawItems()强制执行。该标志于Qt 4.3引入。
- `QGraphicsItem::ItemClipsChildrenToShape`：`0x10`;该物品将所有后代的绘制剪辑为自身形状。该物品的直接或间接子节点不得绘制超出该物品形状的物体。默认情况下，该标志被禁用;子节点可以随处绘制。此行为由QGraphicsView：:d rawItems()或QGraphicsScene：:d rawItems()强制执行。该标志于Qt 4.3引入。
注意：该标志类似于ItemContainsChildrenInShape，但通过裁剪子节点来强制限制。
- `QGraphicsItem::ItemIgnoresTransformations`：`0x20`;该项目忽略继承的变换（即其位置仍锚定于父变换，但忽略父或视角的旋转、缩放或剪切变换）。该标志有助于保持文本标签项水平且未缩放，因此即使视角变换，仍可读取。设置后，视角几何体和场景几何体将分别维护。您必须调用`deviceTransform()`来映射坐标并检测视图中的碰撞。默认情况下，该标志是禁用的。该标志在Qt 4.3中引入。
注意：有了这个标志，你仍然可以调整物品本身，而这个比例转换会影响物品的子节点。
- `QGraphicsItem::ItemIgnoresParentOpacity`：`0x40`;该项忽略其父项的不透明度。该项的有效不透明度与自身相同;它不会与父项的不透明度结合。该标志允许即使父项半透明，也保持绝对不透明度。该标志引入于Qt 4.5。
- `QGraphicsItem::ItemDoesntPropagateOpacityToChildren`：`0x80`;该项不会将其不透明度传播到子节点。该标志允许你创建一个半透明的项目，不影响其子节点的透明度。该标志在Qt 4.5引入。
- `QGraphicsItem::ItemStacksBehindParent`：`0x100`;该物品被叠放在父物品之后。默认情况下，子物品会叠放在父物品之上。但设置该标志时，子节点会被叠放在它后面。该标志适用于投影效果和装饰对象，这些对象遵循父物品的几何体而不在其上方绘制。该标志在Qt 4.5中引入。
- `QGraphicsItem::ItemUsesExtendedStyleOption`：`0x200`;该项在`QStyleOptionGraphicsItem`中使用任一`exposedRect`。默认情况下，`exposedRect`初始化为该项的 `boundingRect()`。你可以启用此标志，以便样式选项设置更细粒度的值。如果需要更高的值，可以使用 `QStyleOptionGraphicsItem::levelOfDetailFromTransform()`。该标志于 Qt 4.6 引入。
- `QGraphicsItem::ItemHasNoContents`：`0x400`;该物品不绘制任何东西（即调用`paint()`无效）。你应在不需要绘制的物品上设置此标志，以确保图形视图避免不必要的绘制准备。该标志于Qt 4.6引入。
- `QGraphicsItem::ItemSendsGeometryChanges`：`0x800`;该项目启用`itemChange()`通知，涵盖`ItemPositionChange`、`ItemPositionHasChanged`、`ItemTransformChange`、`ItemTransformHasChanged`、`ItemRotationChange`、`ItemRotationHasChanged`、`ItemScaleChange`、`ItemScaleHasChanged`、`ItemTransformOriginPointChange`和`ItemTransformOriginPointHasChanged`。出于性能原因，这些通知默认被禁用。您必须启用此标志才能接收位置和变换的通知。该标志于 Qt 4.6 引入。
- `QGraphicsItem::ItemAcceptsInputMethod`：`0x1000`;该项支持通常用于亚洲语言的输入法。该标志于Qt 4.6引入。
- `QGraphicsItem::ItemNegativeZStacksBehindParent`：`0x2000`;如果物品的z值为负，则该物品会自动堆叠到父节点之后。该标志使`setZValue()`能够切换ItemStacksBehindParent。该标志于Qt 4.6引入。
- `QGraphicsItem::ItemIsPanel`：`0x4000`;该物品是一个面板。面板提供激活和受控焦点处理。一次只能激活一个面板（参见 `QGraphicsItem::isActive()`）。当没有面板处于激活状态时，`QGraphicsScene`激活所有非面板物品。窗口物品（即`QGraphicsItem::isWindow()`返回`true`）是面板。该标志于第4.6个Qt引入。
- `QGraphicsItem::ItemSendsScenePositionChanges`：`0x10000`;该项目启用`itemChange()` `ItemScenePositionHasChanged`通知。出于性能原因，这些通知默认被禁用。您必须启用此标志才能接收场景位置变化的通知。该标志于Qt 4.6引入。
- `QGraphicsItem::ItemContainsChildrenInShape`：`0x80000`;该标志表示所有直接或间接子节点只在物品形状内绘制。与ItemClipsChildrenToShape不同，该限制不被强制执行。当你手动确保绘图绑定到物品形状并想避免强制剪辑产生的成本时，请设置ItemContainsChildrenInShape。设置该标志可以实现更高效的绘图和碰撞检测。该标志默认被禁用。
注意：如果同时设置了该标志和 ItemClipsChildrenToShape，剪辑将被强制执行。这相当于仅仅设置 ItemClipsChildrenToShape。
该标志于第5.4期引入。
GraphicsItemFlags 类型是 QFlags<GraphicsItemFlag> 的 typedef。它存储 GraphicsItemFlag 值的按位或组合。

### `flags GraphicsItemFlags`

**作用与语义：**

这个枚举描述了你可以在物品上设置的不同标志，以切换物品行为中的不同功能。
所有标志默认都是被禁用的。
- `QGraphicsItem::ItemIsMovable`：`0x1`;该项目支持使用鼠标进行交互移动。点击该项目并拖动，该物品会与鼠标光标一起移动。如果该项目有子节点，所有子节点也会被移动。如果该项目是选择的一部分，所有被选中的项目也会被移动。此功能通过`QGraphicsItem`鼠标事件处理程序的基础实现提供了便利性。
- `QGraphicsItem::ItemIsSelectable`：`0x2`;该物品支持选择。启用此功能后，`setSelected()`可以切换该物品的选择。它还可以通过调用`QGraphicsScene::setSelectionArea()`、点击物品或在`QGraphicsView`中使用橡皮筋选择自动选择该物品。
- `QGraphicsItem::ItemIsFocusable`：`0x4`;该项目支持键盘输入焦点（即输入项目）。启用该标志后，项目可以接受焦点，从而再次将按键事件传递到`QGraphicsItem::keyPressEvent()`和`QGraphicsItem::keyReleaseEvent()`。
- `QGraphicsItem::ItemClipsToShape`：`0x8`;物品会剪辑到自身形状。物品不能绘制或接收鼠标、平板、拖拽或悬停事件。默认情况下禁用该功能。此行为由QGraphicsView：:d rawItems()或QGraphicsScene：:d rawItems()强制执行。该标志于Qt 4.3引入。
- `QGraphicsItem::ItemClipsChildrenToShape`：`0x10`;该物品将所有后代的绘制剪辑为自身形状。该物品的直接或间接子节点不得绘制超出该物品形状的物体。默认情况下，该标志被禁用;子节点可以随处绘制。此行为由QGraphicsView：:d rawItems()或QGraphicsScene：:d rawItems()强制执行。该标志于Qt 4.3引入。
注意：该标志类似于ItemContainsChildrenInShape，但通过裁剪子节点来强制限制。
- `QGraphicsItem::ItemIgnoresTransformations`：`0x20`;该项目忽略继承的变换（即其位置仍锚定于父变换，但忽略父或视角的旋转、缩放或剪切变换）。该标志有助于保持文本标签项水平且未缩放，因此即使视角变换，仍可读取。设置后，视角几何体和场景几何体将分别维护。您必须调用`deviceTransform()`来映射坐标并检测视图中的碰撞。默认情况下，该标志是禁用的。该标志在Qt 4.3中引入。
注意：有了这个标志，你仍然可以调整物品本身，而这个比例转换会影响物品的子节点。
- `QGraphicsItem::ItemIgnoresParentOpacity`：`0x40`;该项忽略其父项的不透明度。该项的有效不透明度与自身相同;它不会与父项的不透明度结合。该标志允许即使父项半透明，也保持绝对不透明度。该标志引入于Qt 4.5。
- `QGraphicsItem::ItemDoesntPropagateOpacityToChildren`：`0x80`;该项不会将其不透明度传播到子节点。该标志允许你创建一个半透明的项目，不影响其子节点的透明度。该标志在Qt 4.5引入。
- `QGraphicsItem::ItemStacksBehindParent`：`0x100`;该物品被叠放在父物品之后。默认情况下，子物品会叠放在父物品之上。但设置该标志时，子节点会被叠放在它后面。该标志适用于投影效果和装饰对象，这些对象遵循父物品的几何体而不在其上方绘制。该标志在Qt 4.5中引入。
- `QGraphicsItem::ItemUsesExtendedStyleOption`：`0x200`;该项在`QStyleOptionGraphicsItem`中使用任一`exposedRect`。默认情况下，`exposedRect`初始化为该项的 `boundingRect()`。你可以启用此标志，以便样式选项设置更细粒度的值。如果需要更高的值，可以使用 `QStyleOptionGraphicsItem::levelOfDetailFromTransform()`。该标志于 Qt 4.6 引入。
- `QGraphicsItem::ItemHasNoContents`：`0x400`;该物品不绘制任何东西（即调用`paint()`无效）。你应在不需要绘制的物品上设置此标志，以确保图形视图避免不必要的绘制准备。该标志于Qt 4.6引入。
- `QGraphicsItem::ItemSendsGeometryChanges`：`0x800`;该项目启用`itemChange()`通知，涵盖`ItemPositionChange`、`ItemPositionHasChanged`、`ItemTransformChange`、`ItemTransformHasChanged`、`ItemRotationChange`、`ItemRotationHasChanged`、`ItemScaleChange`、`ItemScaleHasChanged`、`ItemTransformOriginPointChange`和`ItemTransformOriginPointHasChanged`。出于性能原因，这些通知默认被禁用。您必须启用此标志才能接收位置和变换的通知。该标志于 Qt 4.6 引入。
- `QGraphicsItem::ItemAcceptsInputMethod`：`0x1000`;该项支持通常用于亚洲语言的输入法。该标志于Qt 4.6引入。
- `QGraphicsItem::ItemNegativeZStacksBehindParent`：`0x2000`;如果物品的z值为负，则该物品会自动堆叠到父节点之后。该标志使`setZValue()`能够切换ItemStacksBehindParent。该标志于Qt 4.6引入。
- `QGraphicsItem::ItemIsPanel`：`0x4000`;该物品是一个面板。面板提供激活和受控焦点处理。一次只能激活一个面板（参见 `QGraphicsItem::isActive()`）。当没有面板处于激活状态时，`QGraphicsScene`激活所有非面板物品。窗口物品（即`QGraphicsItem::isWindow()`返回`true`）是面板。该标志于第4.6个Qt引入。
- `QGraphicsItem::ItemSendsScenePositionChanges`：`0x10000`;该项目启用`itemChange()` `ItemScenePositionHasChanged`通知。出于性能原因，这些通知默认被禁用。您必须启用此标志才能接收场景位置变化的通知。该标志于Qt 4.6引入。
- `QGraphicsItem::ItemContainsChildrenInShape`：`0x80000`;该标志表示所有直接或间接子节点只在物品形状内绘制。与ItemClipsChildrenToShape不同，该限制不被强制执行。当你手动确保绘图绑定到物品形状并想避免强制剪辑产生的成本时，请设置ItemContainsChildrenInShape。设置该标志可以实现更高效的绘图和碰撞检测。该标志默认被禁用。
注意：如果同时设置了该标志和 ItemClipsChildrenToShape，剪辑将被强制执行。这相当于仅仅设置 ItemClipsChildrenToShape。
该标志于第5.4期引入。
GraphicsItemFlags 类型是 QFlags<GraphicsItemFlag> 的 typedef。它存储 GraphicsItemFlag 值的按位或组合。

### `enum { Type, UserType }`

**作用与语义：**

虚拟`type()`函数在标准图形项类中返回的值。所有此类标准图形项类在 Qt 中都关联到一个唯一的类型值，例如`QGraphicsPathItem::type()`返回的值为 2。
- `QGraphicsItem::Type`：`1`;`QGraphicsPathItem`级：公`QAbstractGraphicsShapeItem`
{。
公众：
enum { 类型 = 2 };
int type() const override（return Type; }。
...
};
- `QGraphicsItem::UserType`：`65536`;虚拟`type()`函数对`QGraphicsItem`自定义子类返回的最低值。
类别自定义物品：公开`QGraphicsItem`。
{。
公众：
enum { 类型 = 用户类型 1 };

int type() const 覆盖。
{。
启用该物品的qgraphicsitem_cast。
返回类型;
}。
...
};

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

`QGraphicsItem` 所属机制类型：图形场景与项目机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
