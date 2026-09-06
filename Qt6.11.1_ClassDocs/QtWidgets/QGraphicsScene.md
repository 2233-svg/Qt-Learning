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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 120 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QGraphicsScene::ItemIndexMethod`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QGraphicsScene` 暴露的类型声明 `项目访问、索引、Method`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:ItemIndexMethod`。
- 属性名：`QGraphicsScene`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QGraphicsScene::SceneLayerflags QGraphicsScene::SceneLayers`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QGraphicsScene` 暴露的类型声明 `Scene、Layerflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:SceneLayerflags QGraphicsScene::SceneLayers`。
- 属性名：`QGraphicsScene`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `backgroundBrush : QBrush`

**API 类别：** 属性说明

**中文解读：** 这是 `QGraphicsScene` 的配置属性。初始化或状态切换时通过 `setBackgroundBrush(...)` 设置，之后用 `backgroundBrush()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QBrush`。
- 属性名：`backgroundBrush`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bspTreeDepth : int`

**API 类别：** 属性说明

**中文解读：** 这是 `QGraphicsScene` 的配置属性。初始化或状态切换时通过 `setBspTreeDepth(...)` 设置，之后用 `bspTreeDepth()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`int`。
- 属性名：`bspTreeDepth`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `focusOnTouch : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QGraphicsScene` 的配置属性。初始化或状态切换时通过 `setFocusOnTouch(...)` 设置，之后用 `focusOnTouch()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`focusOnTouch`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `font : QFont`

**API 类别：** 属性说明

**中文解读：** 这是 `QGraphicsScene` 的配置属性。初始化或状态切换时通过 `setFont(...)` 设置，之后用 `font()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QFont`。
- 属性名：`font`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `foregroundBrush : QBrush`

**API 类别：** 属性说明

**中文解读：** 这是 `QGraphicsScene` 的配置属性。初始化或状态切换时通过 `setForegroundBrush(...)` 设置，之后用 `foregroundBrush()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QBrush`。
- 属性名：`foregroundBrush`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `itemIndexMethod : ItemIndexMethod`

**API 类别：** 属性说明

**中文解读：** 这是 `QGraphicsScene` 的配置属性。初始化或状态切换时通过 `setItemIndexMethod(...)` 设置，之后用 `itemIndexMethod()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`ItemIndexMethod`。
- 属性名：`itemIndexMethod`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `minimumRenderSize : qreal`

**API 类别：** 属性说明

**中文解读：** 这是 `QGraphicsScene` 的配置属性。初始化或状态切换时通过 `setMinimumRenderSize(...)` 设置，之后用 `minimumRenderSize()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`qreal`。
- 属性名：`minimumRenderSize`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `palette : QPalette`

**API 类别：** 属性说明

**中文解读：** 这是 `QGraphicsScene` 的配置属性。初始化或状态切换时通过 `setPalette(...)` 设置，之后用 `palette()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QPalette`。
- 属性名：`palette`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `sceneRect : QRectF`

**API 类别：** 属性说明

**中文解读：** 这是 `QGraphicsScene` 的配置属性。初始化或状态切换时通过 `setSceneRect(...)` 设置，之后用 `sceneRect()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QRectF`。
- 属性名：`sceneRect`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `stickyFocus : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QGraphicsScene` 的配置属性。初始化或状态切换时通过 `setStickyFocus(...)` 设置，之后用 `stickyFocus()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`stickyFocus`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QGraphicsScene::QGraphicsScene(QObject *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QGraphicsScene` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `parent`：类型为 `QObject *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QGraphicsScene::QGraphicsScene(const QRectF &sceneRect, QObject *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QGraphicsScene` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `sceneRect`：类型为 `const QRectF &`。没有默认值，调用时必须提供。传入 `const QRectF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `parent`：类型为 `QObject *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QGraphicsScene::QGraphicsScene(qreal x, qreal y, qreal width, qreal height, QObject *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QGraphicsScene` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `x`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `width`：类型为 `qreal`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `qreal`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `parent`：类型为 `QObject *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual noexcept] QGraphicsScene::~QGraphicsScene()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QGraphicsScene` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QGraphicsItem *QGraphicsScene::activePanel() const`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsScene::activePanel` 用于计算、查询或取得与“活动状态、Panel”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QGraphicsItem *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QGraphicsItem *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QGraphicsWidget *QGraphicsScene::activeWindow() const`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsScene::activeWindow` 用于计算、查询或取得与“活动状态、Window”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QGraphicsWidget *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QGraphicsWidget *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QGraphicsEllipseItem *QGraphicsScene::addEllipse(const QRectF &rect, const QPen &pen = QPen(), const QBrush &brush = QBrush())`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QGraphicsScene` 添加依赖、数据或子对象的 API `addEllipse`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QGraphicsEllipseItem *`。
- 参数 `rect`：类型为 `const QRectF &`。没有默认值，调用时必须提供。矩形区域；要确认坐标系、是否包含右下边界以及空矩形的语义。
- 参数 `pen`：类型为 `const QPen &`。默认值为 `QPen()`。传入 `const QPen &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `brush`：类型为 `const QBrush &`。默认值为 `QBrush()`。传入 `const QBrush &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QGraphicsEllipseItem *QGraphicsScene::addEllipse(qreal x, qreal y, qreal w, qreal h, const QPen &pen = QPen(), const QBrush &brush = QBrush())`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QGraphicsScene` 添加依赖、数据或子对象的 API `addEllipse`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QGraphicsEllipseItem *`。
- 参数 `x`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `w`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `h`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pen`：类型为 `const QPen &`。默认值为 `QPen()`。传入 `const QPen &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `brush`：类型为 `const QBrush &`。默认值为 `QBrush()`。传入 `const QBrush &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QGraphicsScene::addItem(QGraphicsItem *item)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QGraphicsScene` 添加依赖、数据或子对象的 API `addItem`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`void`。
- 参数 `item`：类型为 `QGraphicsItem *`。没有默认值，调用时必须提供。容器、布局或模型中的一个项目；要确认加入后所有权是否转移以及项目是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QGraphicsLineItem *QGraphicsScene::addLine(const QLineF &line, const QPen &pen = QPen())`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QGraphicsScene` 添加依赖、数据或子对象的 API `addLine`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QGraphicsLineItem *`。
- 参数 `line`：类型为 `const QLineF &`。没有默认值，调用时必须提供。传入 `const QLineF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pen`：类型为 `const QPen &`。默认值为 `QPen()`。传入 `const QPen &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QGraphicsLineItem *QGraphicsScene::addLine(qreal x1, qreal y1, qreal x2, qreal y2, const QPen &pen = QPen())`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QGraphicsScene` 添加依赖、数据或子对象的 API `addLine`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QGraphicsLineItem *`。
- 参数 `x1`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y1`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `x2`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y2`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pen`：类型为 `const QPen &`。默认值为 `QPen()`。传入 `const QPen &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QGraphicsPathItem *QGraphicsScene::addPath(const QPainterPath &path, const QPen &pen = QPen(), const QBrush &brush = QBrush())`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QGraphicsScene` 添加依赖、数据或子对象的 API `addPath`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QGraphicsPathItem *`。
- 参数 `path`：类型为 `const QPainterPath &`。没有默认值，调用时必须提供。路径字符串。要确认是相对路径还是绝对路径，以及它相对于哪个工作目录。
- 参数 `pen`：类型为 `const QPen &`。默认值为 `QPen()`。传入 `const QPen &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `brush`：类型为 `const QBrush &`。默认值为 `QBrush()`。传入 `const QBrush &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QGraphicsPixmapItem *QGraphicsScene::addPixmap(const QPixmap &pixmap)`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QGraphicsScene` 添加依赖、数据或子对象的 API `addPixmap`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QGraphicsPixmapItem *`。
- 参数 `pixmap`：类型为 `const QPixmap &`。没有默认值，调用时必须提供。传入 `const QPixmap &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QGraphicsPolygonItem *QGraphicsScene::addPolygon(const QPolygonF &polygon, const QPen &pen = QPen(), const QBrush &brush = QBrush())`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QGraphicsScene` 添加依赖、数据或子对象的 API `addPolygon`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QGraphicsPolygonItem *`。
- 参数 `polygon`：类型为 `const QPolygonF &`。没有默认值，调用时必须提供。传入 `const QPolygonF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pen`：类型为 `const QPen &`。默认值为 `QPen()`。传入 `const QPen &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `brush`：类型为 `const QBrush &`。默认值为 `QBrush()`。传入 `const QBrush &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QGraphicsRectItem *QGraphicsScene::addRect(const QRectF &rect, const QPen &pen = QPen(), const QBrush &brush = QBrush())`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QGraphicsScene` 添加依赖、数据或子对象的 API `addRect`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QGraphicsRectItem *`。
- 参数 `rect`：类型为 `const QRectF &`。没有默认值，调用时必须提供。矩形区域；要确认坐标系、是否包含右下边界以及空矩形的语义。
- 参数 `pen`：类型为 `const QPen &`。默认值为 `QPen()`。传入 `const QPen &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `brush`：类型为 `const QBrush &`。默认值为 `QBrush()`。传入 `const QBrush &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QGraphicsRectItem *QGraphicsScene::addRect(qreal x, qreal y, qreal w, qreal h, const QPen &pen = QPen(), const QBrush &brush = QBrush())`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QGraphicsScene` 添加依赖、数据或子对象的 API `addRect`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QGraphicsRectItem *`。
- 参数 `x`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `w`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `h`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `pen`：类型为 `const QPen &`。默认值为 `QPen()`。传入 `const QPen &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `brush`：类型为 `const QBrush &`。默认值为 `QBrush()`。传入 `const QBrush &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QGraphicsSimpleTextItem *QGraphicsScene::addSimpleText(const QString &text, const QFont &font = QFont())`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QGraphicsScene` 添加依赖、数据或子对象的 API `addSimpleText`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QGraphicsSimpleTextItem *`。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。
- 参数 `font`：类型为 `const QFont &`。默认值为 `QFont()`。传入 `const QFont &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QGraphicsTextItem *QGraphicsScene::addText(const QString &text, const QFont &font = QFont())`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QGraphicsScene` 添加依赖、数据或子对象的 API `addText`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QGraphicsTextItem *`。
- 参数 `text`：类型为 `const QString &`。没有默认值，调用时必须提供。文本内容。要区分 Unicode 字符串和 UTF-8/本地编码字节，必要时明确转换。
- 参数 `font`：类型为 `const QFont &`。默认值为 `QFont()`。传入 `const QFont &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QGraphicsProxyWidget *QGraphicsScene::addWidget(QWidget *widget, Qt::WindowFlags wFlags = Qt::WindowFlags())`

**API 类别：** 成员函数说明

**中文解读：** 这是向 `QGraphicsScene` 添加依赖、数据或子对象的 API `addWidget`。注意对象所有权、重复添加和添加后的通知；如果对应有 remove/take 接口，要明确谁负责移除后的生命周期。

**签名拆解：**

- 返回值：`QGraphicsProxyWidget *`。
- 参数 `widget`：类型为 `QWidget *`。没有默认值，调用时必须提供。参与操作的 QWidget。要确认它是否为空、是否已被其他布局/容器管理，以及函数是否只查找直接子项。
- 参数 `wFlags`：类型为 `Qt::WindowFlags`。默认值为 `Qt::WindowFlags()`。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QGraphicsScene::advance()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `advance`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QGraphicsScene::changed(const QList<QRectF> &region)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QGraphicsScene` 发出的通知信号 `changed`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `region`：类型为 `const QList<QRectF> &`。没有默认值，调用时必须提供。传入 `const QList<QRectF> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QGraphicsScene::clear()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `clear`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QGraphicsScene::clearFocus()`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsScene::clearFocus` 用于执行与“清空、Focus”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QGraphicsScene::clearSelection()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `clearSelection`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QGraphicsItem *> QGraphicsScene::collidingItems(const QGraphicsItem *item, Qt::ItemSelectionMode mode = Qt::IntersectsItemShape) const`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsScene::collidingItems` 用于计算、查询或取得与“colliding、Items”相关的操作。调用时要先确认当前状态和 `item`、`mode` 的有效范围；返回类型是 `QList<QGraphicsItem *>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QGraphicsItem *>`。
- 参数 `item`：类型为 `const QGraphicsItem *`。没有默认值，调用时必须提供。容器、布局或模型中的一个项目；要确认加入后所有权是否转移以及项目是否允许为空。
- 参数 `mode`：类型为 `Qt::ItemSelectionMode`。默认值为 `Qt::IntersectsItemShape`。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QGraphicsScene::contextMenuEvent(QGraphicsSceneContextMenuEvent *contextMenuEvent)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsScene::contextMenuEvent` 用于执行与“context、Menu、Event”相关的操作。调用时要先确认当前状态和 `contextMenuEvent` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `contextMenuEvent`：类型为 `QGraphicsSceneContextMenuEvent *`。没有默认值，调用时必须提供。传入 `QGraphicsSceneContextMenuEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QGraphicsItemGroup *QGraphicsScene::createItemGroup(const QList<QGraphicsItem *> &items)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsScene::createItemGroup` 用于计算、查询或取得与“创建、项目访问、Group”相关的操作。调用时要先确认当前状态和 `items` 的有效范围；返回类型是 `QGraphicsItemGroup *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QGraphicsItemGroup *`。
- 参数 `items`：类型为 `const QList<QGraphicsItem *> &`。没有默认值，调用时必须提供。传入 `const QList<QGraphicsItem *> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QGraphicsScene::destroyItemGroup(QGraphicsItemGroup *group)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsScene::destroyItemGroup` 用于执行与“destroy、项目访问、Group”相关的操作。调用时要先确认当前状态和 `group` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `group`：类型为 `QGraphicsItemGroup *`。没有默认值，调用时必须提供。传入 `QGraphicsItemGroup *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QGraphicsScene::dragEnterEvent(QGraphicsSceneDragDropEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsScene::dragEnterEvent` 用于执行与“drag、Enter、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QGraphicsSceneDragDropEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QGraphicsScene::dragLeaveEvent(QGraphicsSceneDragDropEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsScene::dragLeaveEvent` 用于执行与“drag、Leave、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QGraphicsSceneDragDropEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QGraphicsScene::dragMoveEvent(QGraphicsSceneDragDropEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsScene::dragMoveEvent` 用于执行与“drag、移动、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QGraphicsSceneDragDropEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QGraphicsScene::drawBackground(QPainter *painter, const QRectF &rect)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QGraphicsScene` 的核心操作 `drawBackground`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `painter`：类型为 `QPainter *`。没有默认值，调用时必须提供。绘制上下文。要确认它已经绑定有效绘制设备，并处于允许绘制的阶段。
- 参数 `rect`：类型为 `const QRectF &`。没有默认值，调用时必须提供。矩形区域；要确认坐标系、是否包含右下边界以及空矩形的语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QGraphicsScene::drawForeground(QPainter *painter, const QRectF &rect)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QGraphicsScene` 的核心操作 `drawForeground`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `painter`：类型为 `QPainter *`。没有默认值，调用时必须提供。绘制上下文。要确认它已经绑定有效绘制设备，并处于允许绘制的阶段。
- 参数 `rect`：类型为 `const QRectF &`。没有默认值，调用时必须提供。矩形区域；要确认坐标系、是否包含右下边界以及空矩形的语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QGraphicsScene::dropEvent(QGraphicsSceneDragDropEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsScene::dropEvent` 用于执行与“drop、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QGraphicsSceneDragDropEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] bool QGraphicsScene::event(QEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsScene::event` 用于计算、查询或取得与“event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `event`：类型为 `QEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] bool QGraphicsScene::eventFilter(QObject *watched, QEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsScene::eventFilter` 用于计算、查询或取得与“event、Filter”相关的操作。调用时要先确认当前状态和 `watched`、`event` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `watched`：类型为 `QObject *`。没有默认值，调用时必须提供。Qt 对象参数。要确认对象有效、线程归属、所有权和该 API 是否只处理直接子对象。
- 参数 `event`：类型为 `QEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QGraphicsScene::focusInEvent(QFocusEvent *focusEvent)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsScene::focusInEvent` 用于执行与“focus、In、Event”相关的操作。调用时要先确认当前状态和 `focusEvent` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `focusEvent`：类型为 `QFocusEvent *`。没有默认值，调用时必须提供。传入 `QFocusEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QGraphicsItem *QGraphicsScene::focusItem() const`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsScene::focusItem` 用于计算、查询或取得与“focus、项目访问”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QGraphicsItem *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QGraphicsItem *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QGraphicsScene::focusItemChanged(QGraphicsItem *newFocusItem, QGraphicsItem *oldFocusItem, Qt::FocusReason reason)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QGraphicsScene` 发出的通知信号 `focusItemChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `newFocusItem`：类型为 `QGraphicsItem *`。没有默认值，调用时必须提供。传入 `QGraphicsItem *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `oldFocusItem`：类型为 `QGraphicsItem *`。没有默认值，调用时必须提供。传入 `QGraphicsItem *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `reason`：类型为 `Qt::FocusReason`。没有默认值，调用时必须提供。传入 `Qt::FocusReason` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected slot] bool QGraphicsScene::focusNextPrevChild(bool next)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsScene::focusNextPrevChild` 用于计算、查询或取得与“focus、移动到下一项、Prev、Child”相关的操作。调用时要先确认当前状态和 `next` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `next`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QGraphicsScene::focusOutEvent(QFocusEvent *focusEvent)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsScene::focusOutEvent` 用于执行与“focus、Out、Event”相关的操作。调用时要先确认当前状态和 `focusEvent` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `focusEvent`：类型为 `QFocusEvent *`。没有默认值，调用时必须提供。传入 `QFocusEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QGraphicsScene::hasFocus() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `hasFocus`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal QGraphicsScene::height() const`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsScene::height` 用于计算、查询或取得与“高度”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QGraphicsScene::helpEvent(QGraphicsSceneHelpEvent *helpEvent)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsScene::helpEvent` 用于执行与“help、Event”相关的操作。调用时要先确认当前状态和 `helpEvent` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `helpEvent`：类型为 `QGraphicsSceneHelpEvent *`。没有默认值，调用时必须提供。传入 `QGraphicsSceneHelpEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QGraphicsScene::inputMethodEvent(QInputMethodEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsScene::inputMethodEvent` 用于执行与“input、Method、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QInputMethodEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] QVariant QGraphicsScene::inputMethodQuery(Qt::InputMethodQuery query) const`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsScene::inputMethodQuery` 用于计算、查询或取得与“input、Method、查询”相关的操作。调用时要先确认当前状态和 `query` 的有效范围；返回类型是 `QVariant`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVariant`。
- 参数 `query`：类型为 `Qt::InputMethodQuery`。没有默认值，调用时必须提供。传入 `Qt::InputMethodQuery` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QGraphicsScene::invalidate(const QRectF &rect = QRectF(), QGraphicsScene::SceneLayers layers = AllLayers)`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `invalidate`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `rect`：类型为 `const QRectF &`。默认值为 `QRectF()`。矩形区域；要确认坐标系、是否包含右下边界以及空矩形的语义。
- 参数 `layers`：类型为 `QGraphicsScene::SceneLayers`。默认值为 `AllLayers`。传入 `QGraphicsScene::SceneLayers` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QGraphicsScene::invalidate(qreal x, qreal y, qreal w, qreal h, QGraphicsScene::SceneLayers layers = AllLayers)`

**API 类别：** 成员函数说明

**中文解读：** 这是状态清理或重置 API `invalidate`。调用后原有数据、索引、缓存或绑定可能失效；使用前先确认它影响的是当前对象、子对象还是底层共享资源，之后重新检查状态。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `w`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `h`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `layers`：类型为 `QGraphicsScene::SceneLayers`。默认值为 `AllLayers`。传入 `QGraphicsScene::SceneLayers` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QGraphicsScene::isActive() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isActive`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QGraphicsItem *QGraphicsScene::itemAt(const QPointF &position, const QTransform &deviceTransform) const`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `itemAt`，用于取得 `QGraphicsScene` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`QGraphicsItem *`。
- 参数 `position`：类型为 `const QPointF &`。没有默认值，调用时必须提供。位置或偏移量，通常从 0 开始；要结合单位、坐标系以及是否允许边界值判断。
- 参数 `deviceTransform`：类型为 `const QTransform &`。没有默认值，调用时必须提供。传入 `const QTransform &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QGraphicsItem *QGraphicsScene::itemAt(qreal x, qreal y, const QTransform &deviceTransform) const`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `itemAt`，用于取得 `QGraphicsScene` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`QGraphicsItem *`。
- 参数 `x`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `deviceTransform`：类型为 `const QTransform &`。没有默认值，调用时必须提供。传入 `const QTransform &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QGraphicsItem *> QGraphicsScene::items(Qt::SortOrder order = Qt::DescendingOrder) const`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsScene::items` 用于计算、查询或取得与“items”相关的操作。调用时要先确认当前状态和 `order` 的有效范围；返回类型是 `QList<QGraphicsItem *>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QGraphicsItem *>`。
- 参数 `order`：类型为 `Qt::SortOrder`。默认值为 `Qt::DescendingOrder`。传入 `Qt::SortOrder` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QGraphicsItem *> QGraphicsScene::items(const QPointF &pos, Qt::ItemSelectionMode mode = Qt::IntersectsItemShape, Qt::SortOrder order = Qt::DescendingOrder, const QTransform &deviceTransform = QTransform()) const`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsScene::items` 用于计算、查询或取得与“items”相关的操作。调用时要先确认当前状态和 `pos`、`mode`、`order`、`deviceTransform` 的有效范围；返回类型是 `QList<QGraphicsItem *>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QGraphicsItem *>`。
- 参数 `pos`：类型为 `const QPointF &`。没有默认值，调用时必须提供。位置或坐标值；要确认它属于局部坐标、场景坐标、视图坐标还是文件/流偏移。
- 参数 `mode`：类型为 `Qt::ItemSelectionMode`。默认值为 `Qt::IntersectsItemShape`。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。
- 参数 `order`：类型为 `Qt::SortOrder`。默认值为 `Qt::DescendingOrder`。传入 `Qt::SortOrder` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `deviceTransform`：类型为 `const QTransform &`。默认值为 `QTransform()`。传入 `const QTransform &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QGraphicsItem *> QGraphicsScene::items(const QPainterPath &path, Qt::ItemSelectionMode mode = Qt::IntersectsItemShape, Qt::SortOrder order = Qt::DescendingOrder, const QTransform &deviceTransform = QTransform()) const`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsScene::items` 用于计算、查询或取得与“items”相关的操作。调用时要先确认当前状态和 `path`、`mode`、`order`、`deviceTransform` 的有效范围；返回类型是 `QList<QGraphicsItem *>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QGraphicsItem *>`。
- 参数 `path`：类型为 `const QPainterPath &`。没有默认值，调用时必须提供。路径字符串。要确认是相对路径还是绝对路径，以及它相对于哪个工作目录。
- 参数 `mode`：类型为 `Qt::ItemSelectionMode`。默认值为 `Qt::IntersectsItemShape`。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。
- 参数 `order`：类型为 `Qt::SortOrder`。默认值为 `Qt::DescendingOrder`。传入 `Qt::SortOrder` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `deviceTransform`：类型为 `const QTransform &`。默认值为 `QTransform()`。传入 `const QTransform &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QGraphicsItem *> QGraphicsScene::items(const QPolygonF &polygon, Qt::ItemSelectionMode mode = Qt::IntersectsItemShape, Qt::SortOrder order = Qt::DescendingOrder, const QTransform &deviceTransform = QTransform()) const`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsScene::items` 用于计算、查询或取得与“items”相关的操作。调用时要先确认当前状态和 `polygon`、`mode`、`order`、`deviceTransform` 的有效范围；返回类型是 `QList<QGraphicsItem *>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QGraphicsItem *>`。
- 参数 `polygon`：类型为 `const QPolygonF &`。没有默认值，调用时必须提供。传入 `const QPolygonF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `mode`：类型为 `Qt::ItemSelectionMode`。默认值为 `Qt::IntersectsItemShape`。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。
- 参数 `order`：类型为 `Qt::SortOrder`。默认值为 `Qt::DescendingOrder`。传入 `Qt::SortOrder` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `deviceTransform`：类型为 `const QTransform &`。默认值为 `QTransform()`。传入 `const QTransform &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QGraphicsItem *> QGraphicsScene::items(const QRectF &rect, Qt::ItemSelectionMode mode = Qt::IntersectsItemShape, Qt::SortOrder order = Qt::DescendingOrder, const QTransform &deviceTransform = QTransform()) const`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsScene::items` 用于计算、查询或取得与“items”相关的操作。调用时要先确认当前状态和 `rect`、`mode`、`order`、`deviceTransform` 的有效范围；返回类型是 `QList<QGraphicsItem *>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QGraphicsItem *>`。
- 参数 `rect`：类型为 `const QRectF &`。没有默认值，调用时必须提供。矩形区域；要确认坐标系、是否包含右下边界以及空矩形的语义。
- 参数 `mode`：类型为 `Qt::ItemSelectionMode`。默认值为 `Qt::IntersectsItemShape`。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。
- 参数 `order`：类型为 `Qt::SortOrder`。默认值为 `Qt::DescendingOrder`。传入 `Qt::SortOrder` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `deviceTransform`：类型为 `const QTransform &`。默认值为 `QTransform()`。传入 `const QTransform &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QGraphicsItem *> QGraphicsScene::items(qreal x, qreal y, qreal w, qreal h, Qt::ItemSelectionMode mode, Qt::SortOrder order, const QTransform &deviceTransform = QTransform()) const`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsScene::items` 用于计算、查询或取得与“items”相关的操作。调用时要先确认当前状态和 `x`、`y`、`w`、`h`、`mode`、`order`、`deviceTransform` 的有效范围；返回类型是 `QList<QGraphicsItem *>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QGraphicsItem *>`。
- 参数 `x`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `w`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `h`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `mode`：类型为 `Qt::ItemSelectionMode`。没有默认值，调用时必须提供。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。
- 参数 `order`：类型为 `Qt::SortOrder`。没有默认值，调用时必须提供。传入 `Qt::SortOrder` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `deviceTransform`：类型为 `const QTransform &`。默认值为 `QTransform()`。传入 `const QTransform &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRectF QGraphicsScene::itemsBoundingRect() const`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsScene::itemsBoundingRect` 用于计算、查询或取得与“items、Bounding、Rect”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRectF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRectF`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QGraphicsScene::keyPressEvent(QKeyEvent *keyEvent)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsScene::keyPressEvent` 用于执行与“key、Press、Event”相关的操作。调用时要先确认当前状态和 `keyEvent` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `keyEvent`：类型为 `QKeyEvent *`。没有默认值，调用时必须提供。传入 `QKeyEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QGraphicsScene::keyReleaseEvent(QKeyEvent *keyEvent)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsScene::keyReleaseEvent` 用于执行与“key、释放、Event”相关的操作。调用时要先确认当前状态和 `keyEvent` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `keyEvent`：类型为 `QKeyEvent *`。没有默认值，调用时必须提供。传入 `QKeyEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QGraphicsScene::mouseDoubleClickEvent(QGraphicsSceneMouseEvent *mouseEvent)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsScene::mouseDoubleClickEvent` 用于执行与“mouse、Double、Click、Event”相关的操作。调用时要先确认当前状态和 `mouseEvent` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `mouseEvent`：类型为 `QGraphicsSceneMouseEvent *`。没有默认值，调用时必须提供。传入 `QGraphicsSceneMouseEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QGraphicsItem *QGraphicsScene::mouseGrabberItem() const`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsScene::mouseGrabberItem` 用于计算、查询或取得与“mouse、Grabber、项目访问”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QGraphicsItem *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QGraphicsItem *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QGraphicsScene::mouseMoveEvent(QGraphicsSceneMouseEvent *mouseEvent)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsScene::mouseMoveEvent` 用于执行与“mouse、移动、Event”相关的操作。调用时要先确认当前状态和 `mouseEvent` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `mouseEvent`：类型为 `QGraphicsSceneMouseEvent *`。没有默认值，调用时必须提供。传入 `QGraphicsSceneMouseEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QGraphicsScene::mousePressEvent(QGraphicsSceneMouseEvent *mouseEvent)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsScene::mousePressEvent` 用于执行与“mouse、Press、Event”相关的操作。调用时要先确认当前状态和 `mouseEvent` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `mouseEvent`：类型为 `QGraphicsSceneMouseEvent *`。没有默认值，调用时必须提供。传入 `QGraphicsSceneMouseEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QGraphicsScene::mouseReleaseEvent(QGraphicsSceneMouseEvent *mouseEvent)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsScene::mouseReleaseEvent` 用于执行与“mouse、释放、Event”相关的操作。调用时要先确认当前状态和 `mouseEvent` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `mouseEvent`：类型为 `QGraphicsSceneMouseEvent *`。没有默认值，调用时必须提供。传入 `QGraphicsSceneMouseEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QGraphicsScene::removeItem(QGraphicsItem *item)`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `removeItem`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void`。
- 参数 `item`：类型为 `QGraphicsItem *`。没有默认值，调用时必须提供。容器、布局或模型中的一个项目；要确认加入后所有权是否转移以及项目是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QGraphicsScene::render(QPainter *painter, const QRectF &target = QRectF(), const QRectF &source = QRectF(), Qt::AspectRatioMode aspectRatioMode = Qt::KeepAspectRatio)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QGraphicsScene` 的核心操作 `render`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `painter`：类型为 `QPainter *`。没有默认值，调用时必须提供。绘制上下文。要确认它已经绑定有效绘制设备，并处于允许绘制的阶段。
- 参数 `target`：类型为 `const QRectF &`。默认值为 `QRectF()`。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `source`：类型为 `const QRectF &`。默认值为 `QRectF()`。源对象、源索引或源数据；它通常决定操作的输入，转换后要确认源的生命周期和线程归属。
- 参数 `aspectRatioMode`：类型为 `Qt::AspectRatioMode`。默认值为 `Qt::KeepAspectRatio`。传入 `Qt::AspectRatioMode` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QGraphicsScene::sceneRectChanged(const QRectF &rect)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QGraphicsScene` 发出的通知信号 `sceneRectChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `rect`：类型为 `const QRectF &`。没有默认值，调用时必须提供。矩形区域；要确认坐标系、是否包含右下边界以及空矩形的语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QGraphicsItem *> QGraphicsScene::selectedItems() const`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsScene::selectedItems` 用于计算、查询或取得与“selected、Items”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<QGraphicsItem *>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QGraphicsItem *>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPainterPath QGraphicsScene::selectionArea() const`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsScene::selectionArea` 用于计算、查询或取得与“selection、Area”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPainterPath`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPainterPath`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QGraphicsScene::selectionChanged()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QGraphicsScene` 发出的通知信号 `selectionChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QGraphicsScene::sendEvent(QGraphicsItem *item, QEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QGraphicsScene` 的核心操作 `sendEvent`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`bool`。
- 参数 `item`：类型为 `QGraphicsItem *`。没有默认值，调用时必须提供。容器、布局或模型中的一个项目；要确认加入后所有权是否转移以及项目是否允许为空。
- 参数 `event`：类型为 `QEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QGraphicsScene::setActivePanel(QGraphicsItem *item)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setActivePanel`。调用它会改变 `QGraphicsScene` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `item`：类型为 `QGraphicsItem *`。没有默认值，调用时必须提供。容器、布局或模型中的一个项目；要确认加入后所有权是否转移以及项目是否允许为空。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QGraphicsScene::setActiveWindow(QGraphicsWidget *widget)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setActiveWindow`。调用它会改变 `QGraphicsScene` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `widget`：类型为 `QGraphicsWidget *`。没有默认值，调用时必须提供。参与操作的 QWidget。要确认它是否为空、是否已被其他布局/容器管理，以及函数是否只查找直接子项。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QGraphicsScene::setFocus(Qt::FocusReason focusReason = Qt::OtherFocusReason)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFocus`。调用它会改变 `QGraphicsScene` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `focusReason`：类型为 `Qt::FocusReason`。默认值为 `Qt::OtherFocusReason`。传入 `Qt::FocusReason` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QGraphicsScene::setFocusItem(QGraphicsItem *item, Qt::FocusReason focusReason = Qt::OtherFocusReason)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFocusItem`。调用它会改变 `QGraphicsScene` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `item`：类型为 `QGraphicsItem *`。没有默认值，调用时必须提供。容器、布局或模型中的一个项目；要确认加入后所有权是否转移以及项目是否允许为空。
- 参数 `focusReason`：类型为 `Qt::FocusReason`。默认值为 `Qt::OtherFocusReason`。传入 `Qt::FocusReason` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QGraphicsScene::setSelectionArea(const QPainterPath &path, const QTransform &deviceTransform)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSelectionArea`。调用它会改变 `QGraphicsScene` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `path`：类型为 `const QPainterPath &`。没有默认值，调用时必须提供。路径字符串。要确认是相对路径还是绝对路径，以及它相对于哪个工作目录。
- 参数 `deviceTransform`：类型为 `const QTransform &`。没有默认值，调用时必须提供。传入 `const QTransform &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QGraphicsScene::setSelectionArea(const QPainterPath &path, Qt::ItemSelectionOperation selectionOperation = Qt::ReplaceSelection, Qt::ItemSelectionMode mode = Qt::IntersectsItemShape, const QTransform &deviceTransform = QTransform())`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSelectionArea`。调用它会改变 `QGraphicsScene` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `path`：类型为 `const QPainterPath &`。没有默认值，调用时必须提供。路径字符串。要确认是相对路径还是绝对路径，以及它相对于哪个工作目录。
- 参数 `selectionOperation`：类型为 `Qt::ItemSelectionOperation`。默认值为 `Qt::ReplaceSelection`。传入 `Qt::ItemSelectionOperation` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `mode`：类型为 `Qt::ItemSelectionMode`。默认值为 `Qt::IntersectsItemShape`。模式枚举或位标志。它通常决定对象后续允许的操作和状态转换。
- 参数 `deviceTransform`：类型为 `const QTransform &`。默认值为 `QTransform()`。传入 `const QTransform &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QGraphicsScene::setStyle(QStyle *style)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setStyle`。调用它会改变 `QGraphicsScene` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `style`：类型为 `QStyle *`。没有默认值，调用时必须提供。传入 `QStyle *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QStyle *QGraphicsScene::style() const`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsScene::style` 用于计算、查询或取得与“style”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QStyle *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QStyle *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QGraphicsScene::update(const QRectF &rect = QRectF())`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `update`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数 `rect`：类型为 `const QRectF &`。默认值为 `QRectF()`。矩形区域；要确认坐标系、是否包含右下边界以及空矩形的语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QGraphicsScene::update(qreal x, qreal y, qreal w, qreal h)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsScene::update` 用于执行与“更新”相关的操作。调用时要先确认当前状态和 `x`、`y`、`w`、`h` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `w`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `h`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QGraphicsView *> QGraphicsScene::views() const`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsScene::views` 用于计算、查询或取得与“views”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<QGraphicsView *>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QGraphicsView *>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QGraphicsScene::wheelEvent(QGraphicsSceneWheelEvent *wheelEvent)`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsScene::wheelEvent` 用于执行与“wheel、Event”相关的操作。调用时要先确认当前状态和 `wheelEvent` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `wheelEvent`：类型为 `QGraphicsSceneWheelEvent *`。没有默认值，调用时必须提供。传入 `QGraphicsSceneWheelEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal QGraphicsScene::width() const`

**API 类别：** 成员函数说明

**中文解读：** `QGraphicsScene::width` 用于计算、查询或取得与“宽度”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum SceneLayer { ItemLayer, BackgroundLayer, ForegroundLayer, AllLayers }`

**API 类别：** 公有类型

**中文解读：** 这是 `QGraphicsScene` 暴露的类型声明 `Scene、Layer`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags SceneLayers`

**API 类别：** 公有类型

**中文解读：** 这是 `QGraphicsScene` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QBrush backgroundBrush() const`

**API 类别：** 公有函数

**中文解读：** `QGraphicsScene::backgroundBrush` 用于计算、查询或取得与“background、Brush”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QBrush`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QBrush`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int bspTreeDepth() const`

**API 类别：** 公有函数

**中文解读：** `QGraphicsScene::bspTreeDepth` 用于计算、查询或取得与“bsp、Tree、Depth”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool focusOnTouch() const`

**API 类别：** 公有函数

**中文解读：** `QGraphicsScene::focusOnTouch` 用于计算、查询或取得与“focus、On、Touch”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QFont font() const`

**API 类别：** 公有函数

**中文解读：** `QGraphicsScene::font` 用于计算、查询或取得与“字体”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QFont`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QFont`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QBrush foregroundBrush() const`

**API 类别：** 公有函数

**中文解读：** `QGraphicsScene::foregroundBrush` 用于计算、查询或取得与“foreground、Brush”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QBrush`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QBrush`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QGraphicsScene::ItemIndexMethod itemIndexMethod() const`

**API 类别：** 公有函数

**中文解读：** `QGraphicsScene::itemIndexMethod` 用于计算、查询或取得与“项目访问、索引、Method”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QGraphicsScene::ItemIndexMethod`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QGraphicsScene::ItemIndexMethod`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal minimumRenderSize() const`

**API 类别：** 公有函数

**中文解读：** `QGraphicsScene::minimumRenderSize` 用于计算、查询或取得与“最小值、渲染、尺寸或数量”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPalette palette() const`

**API 类别：** 公有函数

**中文解读：** `QGraphicsScene::palette` 用于计算、查询或取得与“palette”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QPalette`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QPalette`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRectF sceneRect() const`

**API 类别：** 公有函数

**中文解读：** `QGraphicsScene::sceneRect` 用于计算、查询或取得与“scene、Rect”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRectF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRectF`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setBackgroundBrush(const QBrush &brush)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setBackgroundBrush`。调用它会改变 `QGraphicsScene` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `brush`：类型为 `const QBrush &`。没有默认值，调用时必须提供。传入 `const QBrush &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setBspTreeDepth(int depth)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setBspTreeDepth`。调用它会改变 `QGraphicsScene` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `depth`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setFocusOnTouch(bool enabled)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setFocusOnTouch`。调用它会改变 `QGraphicsScene` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enabled`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setFont(const QFont &font)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setFont`。调用它会改变 `QGraphicsScene` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `font`：类型为 `const QFont &`。没有默认值，调用时必须提供。传入 `const QFont &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setForegroundBrush(const QBrush &brush)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setForegroundBrush`。调用它会改变 `QGraphicsScene` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `brush`：类型为 `const QBrush &`。没有默认值，调用时必须提供。传入 `const QBrush &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setItemIndexMethod(QGraphicsScene::ItemIndexMethod method)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setItemIndexMethod`。调用它会改变 `QGraphicsScene` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `method`：类型为 `QGraphicsScene::ItemIndexMethod`。没有默认值，调用时必须提供。传入 `QGraphicsScene::ItemIndexMethod` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setMinimumRenderSize(qreal minSize)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setMinimumRenderSize`。调用它会改变 `QGraphicsScene` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `minSize`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setPalette(const QPalette &palette)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setPalette`。调用它会改变 `QGraphicsScene` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `palette`：类型为 `const QPalette &`。没有默认值，调用时必须提供。传入 `const QPalette &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setSceneRect(const QRectF &rect)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setSceneRect`。调用它会改变 `QGraphicsScene` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `rect`：类型为 `const QRectF &`。没有默认值，调用时必须提供。矩形区域；要确认坐标系、是否包含右下边界以及空矩形的语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setSceneRect(qreal x, qreal y, qreal w, qreal h)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setSceneRect`。调用它会改变 `QGraphicsScene` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `w`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `h`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setStickyFocus(bool enabled)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setStickyFocus`。调用它会改变 `QGraphicsScene` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enabled`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool stickyFocus() const`

**API 类别：** 公有函数

**中文解读：** `QGraphicsScene::stickyFocus` 用于计算、查询或取得与“sticky、Focus”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

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
