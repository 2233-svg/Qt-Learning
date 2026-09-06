# QQuickItem

> Qt 6.11.1 · Qt Quick

## 1. 先建立直觉

**一句话定位：** `QQuickItem` 是 QML 属性绑定与场景图机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Quick 面向 QML/场景图界面，提供可视项、动画、输入和高性能界面基础设施。

### 这是什么

`QQuickItem` 是 Qt Quick/QML 体系中的公开类型，连接 C++ 对象、QML 属性绑定和场景图渲染。

**内部模型：** QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

**适用场景：** 需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。

**典型调用链：** 注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

**先记住的坑：** 不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

## 2. 依赖与对象关系

- 头文件：`#include <QQuickItem>`
- 继承自：QObject、QQmlParserStatus
- 直接派生类：QQuickFramebufferObject、QQuickPaintedItem,、QQuickRhiItem

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Quick)
target_link_libraries(mytarget PRIVATE Qt6::Quick)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

QML 属性绑定是声明式依赖关系，C++ 侧的属性、信号和对象生命周期会直接影响绑定是否更新。涉及渲染线程的类型不能随意在 GUI 线程之外操作。

### 状态、生命周期和线程

**生命周期：** QML 引擎、上下文和对象所有权必须明确。由 QML 创建的对象通常由引擎管理；通过 context property 或 C++ 暴露的对象要决定由 C++ 持有还是转移给 QML，不能让绑定指向悬空对象。

**状态与结果：** 属性绑定和直接赋值不是一回事：直接给被绑定属性赋值通常会打破原有绑定。C++ 属性要有正确的 notify signal，QML 才能在数据变化时更新；信号参数和属性当前值要保持一致。

**线程与事件循环：** 大多数 QML 对象和 GUI 操作在 GUI 线程，场景图渲染还可能在 render thread。不要在渲染阶段调用 GUI 对象 API；后台数据通过线程安全的信号/槽边界送入 QML。

## 3. 直接使用

需要 QML 界面、动画、场景图或把 C++ 数据暴露给 QML 时使用。 使用时通常按这个过程组织：注册/创建类型 -> 暴露 properties/signals/invokables -> QML 创建和绑定 -> 在 C++ 中通过信号更新状态 -> 按线程规则处理渲染资源。

```cpp
// C++ 侧暴露属性/信号后，在 QML 中建立绑定。
// 变化时发出 notify signal，避免在绑定表达式中直接修改状态。
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `union ItemChangeData`
- `enum Flag { ItemClipsChildrenToShape, ItemAcceptsInputMethod, ItemIsFocusScope, ItemHasContents, ItemAcceptsDrops, …, ItemObservesViewport }`
- `flags Flags`
- `enum ItemChange { ItemChildAddedChange, ItemChildRemovedChange, ItemSceneChange, ItemVisibleHasChanged, ItemParentHasChanged, …, ItemTransformHasChanged }`
- `enum TransformOrigin { TopLeft, Top, TopRight, Left, Center, …, BottomRight }`

### 属性

- `activeFocus : bool`
- `activeFocusOnTab : bool`
- `antialiasing : bool`
- `baselineOffset : qreal`
- `childrenRect : QRectF`
- `clip : bool`
- `containmentMask : QObject*`
- `enabled : bool`
- `focus : bool`
- `(since 6.7) focusPolicy : Qt::FocusPolicy`
- `height : qreal`
- `implicitHeight : qreal`
- `implicitWidth : qreal`
- `opacity : qreal`
- `parent : QQuickItem*`
- `rotation : qreal`
- `scale : qreal`
- `smooth : bool`
- `state : QString`
- `transformOrigin : TransformOrigin`
- `visible : bool`
- `width : qreal`
- `x : qreal`
- `y : qreal`
- `z : qreal`

### 公有函数

- `QQuickItem(QQuickItem *parent = nullptr)`
- `virtual ~QQuickItem() override`
- `bool acceptHoverEvents() const`
- `bool acceptTouchEvents() const`
- `Qt::MouseButtons acceptedMouseButtons() const`
- `bool activeFocusOnTab() const`
- `bool antialiasing() const`
- `qreal baselineOffset() const`
- `QBindable<qreal> bindableHeight()`
- `QBindable<qreal> bindableWidth()`
- `QBindable<qreal> bindableX()`
- `QBindable<qreal> bindableY()`
- `virtual QRectF boundingRect() const`
- `QQuickItem * childAt(qreal x, qreal y) const`
- `QList<QQuickItem *> childItems() const`
- `QRectF childrenRect()`
- `bool clip() const`
- `virtual QRectF clipRect() const`
- `QObject * containmentMask() const`
- `virtual bool contains(const QPointF &point) const`
- `QCursor cursor() const`
- `(since 6.3) void dumpItemTree() const`
- `(since 6.3) void ensurePolished()`
- `bool filtersChildMouseEvents() const`
- `QQuickItem::Flags flags() const`
- `Qt::FocusPolicy focusPolicy() const`
- `void forceActiveFocus()`
- `void forceActiveFocus(Qt::FocusReason reason)`
- `QSharedPointer<QQuickItemGrabResult> grabToImage(const QSize &targetSize = QSize())`
- `bool hasActiveFocus() const`
- `bool hasFocus() const`
- `qreal height() const`
- `qreal implicitHeight() const`
- `qreal implicitWidth() const`
- `virtual QVariant inputMethodQuery(Qt::InputMethodQuery query) const`
- `bool isAncestorOf(const QQuickItem *child) const`
- `bool isEnabled() const`
- `bool isFocusScope() const`
- `virtual bool isTextureProvider() const`
- `bool isVisible() const`
- `bool keepMouseGrab() const`
- `bool keepTouchGrab() const`
- `QPointF mapFromGlobal(const QPointF &point) const`
- `QPointF mapFromItem(const QQuickItem *item, const QPointF &point) const`
- `QPointF mapFromScene(const QPointF &point) const`
- `QRectF mapRectFromItem(const QQuickItem *item, const QRectF &rect) const`
- `QRectF mapRectFromScene(const QRectF &rect) const`
- `QRectF mapRectToItem(const QQuickItem *item, const QRectF &rect) const`
- `QRectF mapRectToScene(const QRectF &rect) const`
- `QPointF mapToGlobal(const QPointF &point) const`
- `QPointF mapToItem(const QQuickItem *item, const QPointF &point) const`
- `QPointF mapToScene(const QPointF &point) const`
- `QQuickItem * nextItemInFocusChain(bool forward = true)`
- `qreal opacity() const`
- `QQuickItem * parentItem() const`
- `void polish()`
- `void resetAntialiasing()`
- `void resetHeight()`
- `void resetWidth()`
- `qreal rotation() const`
- `qreal scale() const`
- `QQuickItem * scopedFocusItem() const`
- `void setAcceptHoverEvents(bool enabled)`
- `void setAcceptTouchEvents(bool enabled)`
- `void setAcceptedMouseButtons(Qt::MouseButtons buttons)`
- `void setActiveFocusOnTab(bool)`
- `void setAntialiasing(bool)`
- `void setBaselineOffset(qreal)`
- `void setClip(bool)`
- `void setContainmentMask(QObject *mask)`
- `void setCursor(const QCursor &cursor)`
- `void setEnabled(bool)`
- `void setFiltersChildMouseEvents(bool filter)`
- `void setFlag(QQuickItem::Flag flag, bool enabled = true)`
- `void setFlags(QQuickItem::Flags flags)`
- `void setFocus(bool)`
- `void setFocus(bool focus, Qt::FocusReason reason)`
- `void setFocusPolicy(Qt::FocusPolicy policy)`
- `void setHeight(qreal)`
- `void setImplicitHeight(qreal)`
- `void setImplicitWidth(qreal)`
- `void setKeepMouseGrab(bool keep)`
- `void setKeepTouchGrab(bool keep)`
- `void setOpacity(qreal)`
- `void setParentItem(QQuickItem *parent)`
- `void setRotation(qreal)`
- `void setScale(qreal)`
- `void setSize(const QSizeF &size)`
- `void setSmooth(bool)`
- `void setState(const QString &)`
- `void setTransformOrigin(QQuickItem::TransformOrigin)`
- `void setVisible(bool)`
- `void setWidth(qreal)`
- `void setX(qreal)`
- `void setY(qreal)`
- `void setZ(qreal)`
- `QSizeF size() const`
- `bool smooth() const`
- `void stackAfter(const QQuickItem *sibling)`
- `void stackBefore(const QQuickItem *sibling)`
- `QString state() const`
- `virtual QSGTextureProvider * textureProvider() const`
- `QQuickItem::TransformOrigin transformOrigin() const`
- `void unsetCursor()`
- `QQuickItem * viewportItem() const`
- `qreal width() const`
- `QQuickWindow * window() const`
- `qreal x() const`
- `qreal y() const`
- `qreal z() const`

### 公有槽函数

- `void update()`

### 信号

- `void activeFocusChanged(bool)`
- `void activeFocusOnTabChanged(bool)`
- `void antialiasingChanged(bool)`
- `void baselineOffsetChanged(qreal)`
- `void childrenRectChanged(const QRectF &)`
- `void clipChanged(bool)`
- `void containmentMaskChanged()`
- `void enabledChanged()`
- `void focusChanged(bool)`
- `void focusPolicyChanged(Qt::FocusPolicy)`
- `void heightChanged()`
- `void implicitHeightChanged()`
- `void implicitWidthChanged()`
- `void opacityChanged()`
- `void parentChanged(QQuickItem *)`
- `void rotationChanged()`
- `void scaleChanged()`
- `void smoothChanged(bool)`
- `void stateChanged(const QString &)`
- `void transformOriginChanged(QQuickItem::TransformOrigin)`
- `void visibleChanged()`
- `void widthChanged()`
- `void windowChanged(QQuickWindow *window)`
- `void xChanged()`
- `void yChanged()`
- `void zChanged()`

### 保护函数

- `virtual bool childMouseEventFilter(QQuickItem *item, QEvent *event)`
- `virtual void dragEnterEvent(QDragEnterEvent *event)`
- `virtual void dragLeaveEvent(QDragLeaveEvent *event)`
- `virtual void dragMoveEvent(QDragMoveEvent *event)`
- `virtual void dropEvent(QDropEvent *event)`
- `virtual void focusInEvent(QFocusEvent *event)`
- `virtual void focusOutEvent(QFocusEvent *event)`
- `(since 6.0) virtual void geometryChange(const QRectF &newGeometry, const QRectF &oldGeometry)`
- `bool heightValid() const`
- `virtual void hoverEnterEvent(QHoverEvent *event)`
- `virtual void hoverLeaveEvent(QHoverEvent *event)`
- `virtual void hoverMoveEvent(QHoverEvent *event)`
- `virtual void inputMethodEvent(QInputMethodEvent *event)`
- `bool isComponentComplete() const`
- `virtual void itemChange(QQuickItem::ItemChange change, const QQuickItem::ItemChangeData &value)`
- `virtual void keyPressEvent(QKeyEvent *event)`
- `virtual void keyReleaseEvent(QKeyEvent *event)`
- `virtual void mouseDoubleClickEvent(QMouseEvent *event)`
- `virtual void mouseMoveEvent(QMouseEvent *event)`
- `virtual void mousePressEvent(QMouseEvent *event)`
- `virtual void mouseReleaseEvent(QMouseEvent *event)`
- `virtual void mouseUngrabEvent()`
- `virtual void releaseResources()`
- `virtual void touchEvent(QTouchEvent *event)`
- `virtual void touchUngrabEvent()`
- `void updateInputMethod(Qt::InputMethodQueries queries = Qt::ImQueryInput)`
- `virtual QSGNode * updatePaintNode(QSGNode *oldNode, QQuickItem::UpdatePaintNodeData *updatePaintNodeData)`
- `virtual void updatePolish()`
- `virtual void wheelEvent(QWheelEvent *event)`
- `bool widthValid() const`

### 重实现的保护函数

- `virtual void classBegin() override`
- `virtual void componentComplete() override`
- `virtual bool event(QEvent *ev) override`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 201 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `enum QQuickItem::Flagflags QQuickItem::Flags`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QQuickItem` 暴露的类型声明 `Flagflags`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:Flagflags QQuickItem::Flags`。
- 属性名：`QQuickItem`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QQuickItem::ItemChange`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QQuickItem` 暴露的类型声明 `项目访问、Change`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:ItemChange`。
- 属性名：`QQuickItem`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum QQuickItem::TransformOrigin`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QQuickItem` 暴露的类型声明 `Transform、Origin`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 属性类型：`:TransformOrigin`。
- 属性名：`QQuickItem`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] activeFocus : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QQuickItem` 的状态/能力属性。通常通过 `activeFocus()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`activeFocus`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `activeFocusOnTab : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QQuickItem` 的配置属性。初始化或状态切换时通过 `setActiveFocusOnTab(...)` 设置，之后用 `activeFocusOnTab()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`activeFocusOnTab`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `antialiasing : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QQuickItem` 的配置属性。初始化或状态切换时通过 `setAntialiasing(...)` 设置，之后用 `antialiasing()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`antialiasing`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `baselineOffset : qreal`

**API 类别：** 属性说明

**中文解读：** 这是 `QQuickItem` 的配置属性。初始化或状态切换时通过 `setBaselineOffset(...)` 设置，之后用 `baselineOffset()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`qreal`。
- 属性名：`baselineOffset`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[read-only] childrenRect : QRectF`

**API 类别：** 属性说明

**中文解读：** 这是 `QQuickItem` 的状态/能力属性。通常通过 `childrenRect()` 查询；它主要用于决定后续操作是否可执行，不能把查询结果当成永久事实，状态变化要结合对应的 `...Changed` 信号或文档说明。

**签名拆解：**

- 属性类型：`QRectF`。
- 属性名：`childrenRect`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `clip : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QQuickItem` 的配置属性。初始化或状态切换时通过 `setClip(...)` 设置，之后用 `clip()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`clip`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `containmentMask : QObject*`

**API 类别：** 属性说明

**中文解读：** 这是 `QQuickItem` 的配置属性。初始化或状态切换时通过 `setContainmentMask(...)` 设置，之后用 `containmentMask()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QObject*`。
- 属性名：`containmentMask`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enabled : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QQuickItem` 的配置属性。初始化或状态切换时通过 `setEnabled(...)` 设置，之后用 `enabled()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`enabled`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `focus : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QQuickItem` 的配置属性。初始化或状态切换时通过 `setFocus(...)` 设置，之后用 `focus()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`focus`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.7] focusPolicy : Qt::FocusPolicy`

**API 类别：** 属性说明

**中文解读：** 这是 `QQuickItem` 的配置属性。初始化或状态切换时通过 `setFocusPolicy(...)` 设置，之后用 `FocusPolicy()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`Qt::FocusPolicy`。
- 属性名：`focusPolicy`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[bindable] height : qreal`

**API 类别：** 属性说明

**中文解读：** 这是 `QQuickItem` 的配置属性。初始化或状态切换时通过 `setHeight(...)` 设置，之后用 `height()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`qreal`。
- 属性名：`height`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `implicitWidth : qreal`

**API 类别：** 属性说明

**中文解读：** 这是 `QQuickItem` 的配置属性。初始化或状态切换时通过 `setImplicitWidth(...)` 设置，之后用 `implicitWidth()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`qreal`。
- 属性名：`implicitWidth`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `opacity : qreal`

**API 类别：** 属性说明

**中文解读：** 这是 `QQuickItem` 的配置属性。初始化或状态切换时通过 `setOpacity(...)` 设置，之后用 `opacity()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`qreal`。
- 属性名：`opacity`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `parent : QQuickItem*`

**API 类别：** 属性说明

**中文解读：** 这是 `QQuickItem` 的配置属性。初始化或状态切换时通过 `setParent(...)` 设置，之后用 `parent()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QQuickItem*`。
- 属性名：`parent`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `rotation : qreal`

**API 类别：** 属性说明

**中文解读：** 这是 `QQuickItem` 的配置属性。初始化或状态切换时通过 `setRotation(...)` 设置，之后用 `rotation()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`qreal`。
- 属性名：`rotation`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `scale : qreal`

**API 类别：** 属性说明

**中文解读：** 这是 `QQuickItem` 的配置属性。初始化或状态切换时通过 `setScale(...)` 设置，之后用 `scale()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`qreal`。
- 属性名：`scale`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `smooth : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QQuickItem` 的配置属性。初始化或状态切换时通过 `setSmooth(...)` 设置，之后用 `smooth()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`smooth`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `state : QString`

**API 类别：** 属性说明

**中文解读：** 这是 `QQuickItem` 的配置属性。初始化或状态切换时通过 `setState(...)` 设置，之后用 `state()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`QString`。
- 属性名：`state`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `transformOrigin : TransformOrigin`

**API 类别：** 属性说明

**中文解读：** 这是 `QQuickItem` 的配置属性。初始化或状态切换时通过 `setTransformOrigin(...)` 设置，之后用 `transformOrigin()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`TransformOrigin`。
- 属性名：`transformOrigin`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `visible : bool`

**API 类别：** 属性说明

**中文解读：** 这是 `QQuickItem` 的配置属性。初始化或状态切换时通过 `setVisible(...)` 设置，之后用 `visible()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`bool`。
- 属性名：`visible`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[bindable] width : qreal`

**API 类别：** 属性说明

**中文解读：** 这是 `QQuickItem` 的配置属性。初始化或状态切换时通过 `setWidth(...)` 设置，之后用 `width()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`qreal`。
- 属性名：`width`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[bindable] x : qreal`

**API 类别：** 属性说明

**中文解读：** 这是 `QQuickItem` 的配置属性。初始化或状态切换时通过 `setX(...)` 设置，之后用 `x()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`qreal`。
- 属性名：`x`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[bindable] y : qreal`

**API 类别：** 属性说明

**中文解读：** 这是 `QQuickItem` 的配置属性。初始化或状态切换时通过 `setY(...)` 设置，之后用 `y()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`qreal`。
- 属性名：`y`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `z : qreal`

**API 类别：** 属性说明

**中文解读：** 这是 `QQuickItem` 的配置属性。初始化或状态切换时通过 `setZ(...)` 设置，之后用 `z()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`qreal`。
- 属性名：`z`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QQuickItem::QQuickItem(QQuickItem *parent = nullptr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QQuickItem` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `parent`：类型为 `QQuickItem *`。默认值为 `nullptr`。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual noexcept] QQuickItem::~QQuickItem()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QQuickItem` 的析构函数。对象销毁时资源、子对象和连接会按 Qt 规则释放；异步对象要先停止任务或使用 deleteLater，避免回调访问已经不存在的实例。

**签名拆解：**

- 返回值：析构函数，无返回值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QQuickItem::acceptHoverEvents() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::acceptHoverEvents` 用于计算、查询或取得与“接受、Hover、Events”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QQuickItem::acceptTouchEvents() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::acceptTouchEvents` 用于计算、查询或取得与“接受、Touch、Events”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Qt::MouseButtons QQuickItem::acceptedMouseButtons() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::acceptedMouseButtons` 用于计算、查询或取得与“accepted、Mouse、Buttons”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `Qt::MouseButtons`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::MouseButtons`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] QRectF QQuickItem::boundingRect() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::boundingRect` 用于计算、查询或取得与“bounding、Rect”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRectF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRectF`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[invokable] QQuickItem *QQuickItem::childAt(qreal x, qreal y) const`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::childAt` 用于计算、查询或取得与“child、按位置访问”相关的操作。调用时要先确认当前状态和 `x`、`y` 的有效范围；返回类型是 `QQuickItem *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QQuickItem *`。
- 参数 `x`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `qreal`。没有默认值，调用时必须提供。传入 `qreal` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QList<QQuickItem *> QQuickItem::childItems() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::childItems` 用于计算、查询或取得与“child、Items”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QList<QQuickItem *>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QList<QQuickItem *>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] bool QQuickItem::childMouseEventFilter(QQuickItem *item, QEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::childMouseEventFilter` 用于计算、查询或取得与“child、Mouse、Event、Filter”相关的操作。调用时要先确认当前状态和 `item`、`event` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `item`：类型为 `QQuickItem *`。没有默认值，调用时必须提供。容器、布局或模型中的一个项目；要确认加入后所有权是否转移以及项目是否允许为空。
- 参数 `event`：类型为 `QEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QQuickItem::classBegin()`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::classBegin` 用于执行与“class、起始位置”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] QRectF QQuickItem::clipRect() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::clipRect` 用于计算、查询或取得与“clip、Rect”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRectF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRectF`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] void QQuickItem::componentComplete()`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::componentComplete` 用于执行与“component、Complete”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual invokable] bool QQuickItem::contains(const QPointF &point) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `contains`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `point`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QCursor QQuickItem::cursor() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::cursor` 用于计算、查询或取得与“cursor”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QCursor`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QCursor`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QQuickItem::dragEnterEvent(QDragEnterEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::dragEnterEvent` 用于执行与“drag、Enter、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QDragEnterEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QQuickItem::dragLeaveEvent(QDragLeaveEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::dragLeaveEvent` 用于执行与“drag、Leave、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QDragLeaveEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QQuickItem::dragMoveEvent(QDragMoveEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::dragMoveEvent` 用于执行与“drag、移动、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QDragMoveEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QQuickItem::dropEvent(QDropEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::dropEvent` 用于执行与“drop、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QDropEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[invokable, since 6.3] void QQuickItem::dumpItemTree() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::dumpItemTree` 用于执行与“dump、项目访问、Tree”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[invokable, since 6.3] void QQuickItem::ensurePolished()`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::ensurePolished` 用于执行与“ensure、Polished”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[override virtual protected] bool QQuickItem::event(QEvent *ev)`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::event` 用于计算、查询或取得与“event”相关的操作。调用时要先确认当前状态和 `ev` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `ev`：类型为 `QEvent *`。没有默认值，调用时必须提供。传入 `QEvent *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QQuickItem::filtersChildMouseEvents() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::filtersChildMouseEvents` 用于计算、查询或取得与“filters、Child、Mouse、Events”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QQuickItem::Flags QQuickItem::flags() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::flags` 用于计算、查询或取得与“标志”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QQuickItem::Flags`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QQuickItem::Flags`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QQuickItem::focusInEvent(QFocusEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::focusInEvent` 用于执行与“focus、In、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QFocusEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QQuickItem::focusOutEvent(QFocusEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::focusOutEvent` 用于执行与“focus、Out、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QFocusEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[invokable] void QQuickItem::forceActiveFocus()`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::forceActiveFocus` 用于执行与“force、活动状态、Focus”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[invokable] void QQuickItem::forceActiveFocus(Qt::FocusReason reason)`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::forceActiveFocus` 用于执行与“force、活动状态、Focus”相关的操作。调用时要先确认当前状态和 `reason` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `reason`：类型为 `Qt::FocusReason`。没有默认值，调用时必须提供。传入 `Qt::FocusReason` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected, since 6.0] void QQuickItem::geometryChange(const QRectF &newGeometry, const QRectF &oldGeometry)`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::geometryChange` 用于执行与“几何区域、Change”相关的操作。调用时要先确认当前状态和 `newGeometry`、`oldGeometry` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `newGeometry`：类型为 `const QRectF &`。没有默认值，调用时必须提供。传入 `const QRectF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `oldGeometry`：类型为 `const QRectF &`。没有默认值，调用时必须提供。传入 `const QRectF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSharedPointer<QQuickItemGrabResult> QQuickItem::grabToImage(const QSize &targetSize = QSize())`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::grabToImage` 用于计算、查询或取得与“抓取、转换输出、Image”相关的操作。调用时要先确认当前状态和 `targetSize` 的有效范围；返回类型是 `QSharedPointer<QQuickItemGrabResult>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSharedPointer<QQuickItemGrabResult>`。
- 参数 `targetSize`：类型为 `const QSize &`。默认值为 `QSize()`。传入 `const QSize &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] bool QQuickItem::heightValid() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::heightValid` 用于计算、查询或取得与“高度、有效状态”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QQuickItem::hoverEnterEvent(QHoverEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::hoverEnterEvent` 用于执行与“hover、Enter、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QHoverEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QQuickItem::hoverLeaveEvent(QHoverEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::hoverLeaveEvent` 用于执行与“hover、Leave、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QHoverEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QQuickItem::hoverMoveEvent(QHoverEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::hoverMoveEvent` 用于执行与“hover、移动、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QHoverEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal QQuickItem::implicitWidth() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::implicitWidth` 用于计算、查询或取得与“implicit、宽度”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QQuickItem::inputMethodEvent(QInputMethodEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::inputMethodEvent` 用于执行与“input、Method、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QInputMethodEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] QVariant QQuickItem::inputMethodQuery(Qt::InputMethodQuery query) const`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::inputMethodQuery` 用于计算、查询或取得与“input、Method、查询”相关的操作。调用时要先确认当前状态和 `query` 的有效范围；返回类型是 `QVariant`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVariant`。
- 参数 `query`：类型为 `Qt::InputMethodQuery`。没有默认值，调用时必须提供。传入 `Qt::InputMethodQuery` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QQuickItem::isAncestorOf(const QQuickItem *child) const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isAncestorOf`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数 `child`：类型为 `const QQuickItem *`。没有默认值，调用时必须提供。子对象或子节点；要确认它是否由父对象接管，以及调用后原指针是否仍有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] bool QQuickItem::isComponentComplete() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isComponentComplete`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QQuickItem::isFocusScope() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isFocusScope`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] bool QQuickItem::isTextureProvider() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isTextureProvider`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QQuickItem::itemChange(QQuickItem::ItemChange change, const QQuickItem::ItemChangeData &value)`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::itemChange` 用于执行与“项目访问、Change”相关的操作。调用时要先确认当前状态和 `change`、`value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `change`：类型为 `QQuickItem::ItemChange`。没有默认值，调用时必须提供。传入 `QQuickItem::ItemChange` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `value`：类型为 `const QQuickItem::ItemChangeData &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QQuickItem::keepMouseGrab() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::keepMouseGrab` 用于计算、查询或取得与“keep、Mouse、抓取”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QQuickItem::keepTouchGrab() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::keepTouchGrab` 用于计算、查询或取得与“keep、Touch、抓取”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QQuickItem::keyPressEvent(QKeyEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::keyPressEvent` 用于执行与“key、Press、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QKeyEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QQuickItem::keyReleaseEvent(QKeyEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::keyReleaseEvent` 用于执行与“key、释放、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QKeyEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[invokable] QPointF QQuickItem::mapFromGlobal(const QPointF &point) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `mapFromGlobal`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QPointF`。
- 参数 `point`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[invokable] QPointF QQuickItem::mapFromItem(const QQuickItem *item, const QPointF &point) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `mapFromItem`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QPointF`。
- 参数 `item`：类型为 `const QQuickItem *`。没有默认值，调用时必须提供。容器、布局或模型中的一个项目；要确认加入后所有权是否转移以及项目是否允许为空。
- 参数 `point`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPointF QQuickItem::mapFromScene(const QPointF &point) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `mapFromScene`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QPointF`。
- 参数 `point`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRectF QQuickItem::mapRectFromItem(const QQuickItem *item, const QRectF &rect) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `mapRectFromItem`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QRectF`。
- 参数 `item`：类型为 `const QQuickItem *`。没有默认值，调用时必须提供。容器、布局或模型中的一个项目；要确认加入后所有权是否转移以及项目是否允许为空。
- 参数 `rect`：类型为 `const QRectF &`。没有默认值，调用时必须提供。矩形区域；要确认坐标系、是否包含右下边界以及空矩形的语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRectF QQuickItem::mapRectFromScene(const QRectF &rect) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `mapRectFromScene`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QRectF`。
- 参数 `rect`：类型为 `const QRectF &`。没有默认值，调用时必须提供。矩形区域；要确认坐标系、是否包含右下边界以及空矩形的语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRectF QQuickItem::mapRectToItem(const QQuickItem *item, const QRectF &rect) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `mapRectToItem`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QRectF`。
- 参数 `item`：类型为 `const QQuickItem *`。没有默认值，调用时必须提供。容器、布局或模型中的一个项目；要确认加入后所有权是否转移以及项目是否允许为空。
- 参数 `rect`：类型为 `const QRectF &`。没有默认值，调用时必须提供。矩形区域；要确认坐标系、是否包含右下边界以及空矩形的语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRectF QQuickItem::mapRectToScene(const QRectF &rect) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `mapRectToScene`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QRectF`。
- 参数 `rect`：类型为 `const QRectF &`。没有默认值，调用时必须提供。矩形区域；要确认坐标系、是否包含右下边界以及空矩形的语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[invokable] QPointF QQuickItem::mapToGlobal(const QPointF &point) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `mapToGlobal`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QPointF`。
- 参数 `point`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[invokable] QPointF QQuickItem::mapToItem(const QQuickItem *item, const QPointF &point) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `mapToItem`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QPointF`。
- 参数 `item`：类型为 `const QQuickItem *`。没有默认值，调用时必须提供。容器、布局或模型中的一个项目；要确认加入后所有权是否转移以及项目是否允许为空。
- 参数 `point`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPointF QQuickItem::mapToScene(const QPointF &point) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `mapToScene`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QPointF`。
- 参数 `point`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QQuickItem::mouseDoubleClickEvent(QMouseEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::mouseDoubleClickEvent` 用于执行与“mouse、Double、Click、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QMouseEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QQuickItem::mouseMoveEvent(QMouseEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::mouseMoveEvent` 用于执行与“mouse、移动、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QMouseEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QQuickItem::mousePressEvent(QMouseEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::mousePressEvent` 用于执行与“mouse、Press、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QMouseEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QQuickItem::mouseReleaseEvent(QMouseEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::mouseReleaseEvent` 用于执行与“mouse、释放、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QMouseEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QQuickItem::mouseUngrabEvent()`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::mouseUngrabEvent` 用于执行与“mouse、Ungrab、Event”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[invokable] QQuickItem *QQuickItem::nextItemInFocusChain(bool forward = true)`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::nextItemInFocusChain` 用于计算、查询或取得与“移动到下一项、项目访问、In、Focus、Chain”相关的操作。调用时要先确认当前状态和 `forward` 的有效范围；返回类型是 `QQuickItem *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QQuickItem *`。
- 参数 `forward`：类型为 `bool`。默认值为 `true`。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QQuickItem::polish()`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::polish` 用于执行与“polish”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QQuickItem::releaseResources()`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::releaseResources` 用于执行与“释放、Resources”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QQuickItem *QQuickItem::scopedFocusItem() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::scopedFocusItem` 用于计算、查询或取得与“scoped、Focus、项目访问”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QQuickItem *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QQuickItem *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QQuickItem::setAcceptHoverEvents(bool enabled)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setAcceptHoverEvents`。调用它会改变 `QQuickItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enabled`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QQuickItem::setAcceptTouchEvents(bool enabled)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setAcceptTouchEvents`。调用它会改变 `QQuickItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `enabled`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QQuickItem::setAcceptedMouseButtons(Qt::MouseButtons buttons)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setAcceptedMouseButtons`。调用它会改变 `QQuickItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `buttons`：类型为 `Qt::MouseButtons`。没有默认值，调用时必须提供。传入 `Qt::MouseButtons` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QQuickItem::setCursor(const QCursor &cursor)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setCursor`。调用它会改变 `QQuickItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `cursor`：类型为 `const QCursor &`。没有默认值，调用时必须提供。传入 `const QCursor &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QQuickItem::setFiltersChildMouseEvents(bool filter)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFiltersChildMouseEvents`。调用它会改变 `QQuickItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `filter`：类型为 `bool`。没有默认值，调用时必须提供。过滤条件、匹配器或过滤标志；要确认它作用于显示结果、输入数据还是事件传播。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QQuickItem::setFlag(QQuickItem::Flag flag, bool enabled = true)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFlag`。调用它会改变 `QQuickItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `flag`：类型为 `QQuickItem::Flag`。没有默认值，调用时必须提供。枚举或标志参数。先确认可用枚举值、互斥关系和默认值，必要时用按位或组合标志。
- 参数 `enabled`：类型为 `bool`。默认值为 `true`。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QQuickItem::setFlags(QQuickItem::Flags flags)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFlags`。调用它会改变 `QQuickItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `flags`：类型为 `QQuickItem::Flags`。没有默认值，调用时必须提供。标志位组合。可以用按位或组合，调用前确认哪些标志互斥、哪些标志需要同时出现。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QQuickItem::setFocusPolicy(Qt::FocusPolicy policy)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setFocusPolicy`。调用它会改变 `QQuickItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `policy`：类型为 `Qt::FocusPolicy`。没有默认值，调用时必须提供。传入 `Qt::FocusPolicy` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QQuickItem::setKeepMouseGrab(bool keep)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setKeepMouseGrab`。调用它会改变 `QQuickItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `keep`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QQuickItem::setKeepTouchGrab(bool keep)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setKeepTouchGrab`。调用它会改变 `QQuickItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `keep`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QQuickItem::setSize(const QSizeF &size)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setSize`。调用它会改变 `QQuickItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `size`：类型为 `const QSizeF &`。没有默认值，调用时必须提供。尺寸或长度，单位通常是像素、字节、元素数或时间，必须结合类型和类的上下文确认。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QSizeF QQuickItem::size() const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `size`，返回 `QQuickItem` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`QSizeF`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QQuickItem::stackAfter(const QQuickItem *sibling)`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::stackAfter` 用于执行与“stack、After”相关的操作。调用时要先确认当前状态和 `sibling` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `sibling`：类型为 `const QQuickItem *`。没有默认值，调用时必须提供。传入 `const QQuickItem *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QQuickItem::stackBefore(const QQuickItem *sibling)`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::stackBefore` 用于执行与“stack、Before”相关的操作。调用时要先确认当前状态和 `sibling` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `sibling`：类型为 `const QQuickItem *`。没有默认值，调用时必须提供。传入 `const QQuickItem *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual] QSGTextureProvider *QQuickItem::textureProvider() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::textureProvider` 用于计算、查询或取得与“texture、Provider”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QSGTextureProvider *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSGTextureProvider *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QQuickItem::touchEvent(QTouchEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `touchEvent`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QTouchEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QQuickItem::touchUngrabEvent()`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `touchUngrabEvent`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QQuickItem::unsetCursor()`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::unsetCursor` 用于执行与“unset、Cursor”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[slot] void QQuickItem::update()`

**API 类别：** 成员函数说明

**中文解读：** 这是可被信号连接或元对象调用的槽 `update`。它适合作为一次动作或状态响应的入口；如果调用可能耗时，不要直接阻塞 GUI 事件循环，应把工作拆分或移动到 worker。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] void QQuickItem::updateInputMethod(Qt::InputMethodQueries queries = Qt::ImQueryInput)`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::updateInputMethod` 用于执行与“更新、Input、Method”相关的操作。调用时要先确认当前状态和 `queries` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `queries`：类型为 `Qt::InputMethodQueries`。默认值为 `Qt::ImQueryInput`。传入 `Qt::InputMethodQueries` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] QSGNode *QQuickItem::updatePaintNode(QSGNode *oldNode, QQuickItem::UpdatePaintNodeData *updatePaintNodeData)`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::updatePaintNode` 用于计算、查询或取得与“更新、绘制、Node”相关的操作。调用时要先确认当前状态和 `oldNode`、`updatePaintNodeData` 的有效范围；返回类型是 `QSGNode *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QSGNode *`。
- 参数 `oldNode`：类型为 `QSGNode *`。没有默认值，调用时必须提供。传入 `QSGNode *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `updatePaintNodeData`：类型为 `QQuickItem::UpdatePaintNodeData *`。没有默认值，调用时必须提供。传入 `QQuickItem::UpdatePaintNodeData *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QQuickItem::updatePolish()`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::updatePolish` 用于执行与“更新、Polish”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QQuickItem *QQuickItem::viewportItem() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::viewportItem` 用于计算、查询或取得与“viewport、项目访问”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QQuickItem *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QQuickItem *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[virtual protected] void QQuickItem::wheelEvent(QWheelEvent *event)`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::wheelEvent` 用于执行与“wheel、Event”相关的操作。调用时要先确认当前状态和 `event` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `event`：类型为 `QWheelEvent *`。没有默认值，调用时必须提供。事件对象。通常只在事件处理函数执行期间有效，应读取类型和字段后决定 accept/ignore，不能长期保存指针。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[protected] bool QQuickItem::widthValid() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::widthValid` 用于计算、查询或取得与“宽度、有效状态”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QQuickWindow *QQuickItem::window() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuickItem::window` 用于计算、查询或取得与“window”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QQuickWindow *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QQuickWindow *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[signal] void QQuickItem::windowChanged(QQuickWindow *window)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QQuickItem` 发出的通知信号 `windowChanged`。应用代码通常只连接它，不直接调用它；信号参数描述发生了什么，槽函数中读取相关状态并尽快返回。异步类的完成、错误和状态变化通常都从信号开始处理。

**签名拆解：**

- 返回值：`void`。
- 参数 `window`：类型为 `QQuickWindow *`。没有默认值，调用时必须提供。传入 `QQuickWindow *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `union ItemChangeData`

**API 类别：** 公有类型

**中文解读：** 这是 `QQuickItem` 的 `union` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `enum Flag { ItemClipsChildrenToShape, ItemAcceptsInputMethod, ItemIsFocusScope, ItemHasContents, ItemAcceptsDrops, …, ItemObservesViewport }`

**API 类别：** 公有类型

**中文解读：** 这是 `QQuickItem` 暴露的类型声明 `Flag`。它通常作为其他 API 的参数或返回值使用；先确认每个枚举值/别名的语义、默认值和适用状态，再传给对应函数。

**签名拆解：**

- 这是供该类其他 API 使用的枚举/标志类型；传值前要确认枚举值的语义和适用状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `flags Flags`

**API 类别：** 公有类型

**中文解读：** 这是 `QQuickItem` 的 `标志` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `implicitHeight : qreal`

**API 类别：** 属性

**中文解读：** 这是 `QQuickItem` 的配置属性。初始化或状态切换时通过 `setImplicitHeight(...)` 设置，之后用 `implicitHeight()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`qreal`。
- 属性名：`implicitHeight`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool activeFocusOnTab() const`

**API 类别：** 公有函数

**中文解读：** `QQuickItem::activeFocusOnTab` 用于计算、查询或取得与“活动状态、Focus、On、Tab”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool antialiasing() const`

**API 类别：** 公有函数

**中文解读：** `QQuickItem::antialiasing` 用于计算、查询或取得与“antialiasing”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal baselineOffset() const`

**API 类别：** 公有函数

**中文解读：** `QQuickItem::baselineOffset` 用于计算、查询或取得与“baseline、Offset”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QBindable<qreal> bindableHeight()`

**API 类别：** 公有函数

**中文解读：** 这是启动/建立资源的 API `bindableHeight`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QBindable<qreal>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QBindable<qreal> bindableWidth()`

**API 类别：** 公有函数

**中文解读：** 这是启动/建立资源的 API `bindableWidth`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QBindable<qreal>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QBindable<qreal> bindableX()`

**API 类别：** 公有函数

**中文解读：** 这是启动/建立资源的 API `bindableX`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QBindable<qreal>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QBindable<qreal> bindableY()`

**API 类别：** 公有函数

**中文解读：** 这是启动/建立资源的 API `bindableY`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`QBindable<qreal>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRectF childrenRect()`

**API 类别：** 公有函数

**中文解读：** `QQuickItem::childrenRect` 用于计算、查询或取得与“children、Rect”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QRectF`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QRectF`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool clip() const`

**API 类别：** 公有函数

**中文解读：** `QQuickItem::clip` 用于计算、查询或取得与“clip”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QObject * containmentMask() const`

**API 类别：** 公有函数

**中文解读：** `QQuickItem::containmentMask` 用于计算、查询或取得与“containment、Mask”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QObject *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QObject *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Qt::FocusPolicy focusPolicy() const`

**API 类别：** 公有函数

**中文解读：** `QQuickItem::focusPolicy` 用于计算、查询或取得与“focus、Policy”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `Qt::FocusPolicy`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`Qt::FocusPolicy`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool hasActiveFocus() const`

**API 类别：** 公有函数

**中文解读：** 这是查询 API `hasActiveFocus`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool hasFocus() const`

**API 类别：** 公有函数

**中文解读：** 这是查询 API `hasFocus`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal height() const`

**API 类别：** 公有函数

**中文解读：** `QQuickItem::height` 用于计算、查询或取得与“高度”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal implicitHeight() const`

**API 类别：** 公有函数

**中文解读：** `QQuickItem::implicitHeight` 用于计算、查询或取得与“implicit、高度”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool isEnabled() const`

**API 类别：** 公有函数

**中文解读：** 这是查询 API `isEnabled`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

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

### `qreal opacity() const`

**API 类别：** 公有函数

**中文解读：** `QQuickItem::opacity` 用于计算、查询或取得与“opacity”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QQuickItem * parentItem() const`

**API 类别：** 公有函数

**中文解读：** `QQuickItem::parentItem` 用于计算、查询或取得与“父对象、项目访问”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QQuickItem *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QQuickItem *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void resetAntialiasing()`

**API 类别：** 公有函数

**中文解读：** `QQuickItem::resetAntialiasing` 用于执行与“重置、Antialiasing”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void resetHeight()`

**API 类别：** 公有函数

**中文解读：** `QQuickItem::resetHeight` 用于执行与“重置、高度”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void resetWidth()`

**API 类别：** 公有函数

**中文解读：** `QQuickItem::resetWidth` 用于执行与“重置、宽度”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal rotation() const`

**API 类别：** 公有函数

**中文解读：** `QQuickItem::rotation` 用于计算、查询或取得与“rotation”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal scale() const`

**API 类别：** 公有函数

**中文解读：** `QQuickItem::scale` 用于计算、查询或取得与“scale”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setActiveFocusOnTab(bool)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setActiveFocusOnTab`。调用它会改变 `QQuickItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `bool`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setAntialiasing(bool)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setAntialiasing`。调用它会改变 `QQuickItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `bool`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setBaselineOffset(qreal)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setBaselineOffset`。调用它会改变 `QQuickItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `qreal`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setClip(bool)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setClip`。调用它会改变 `QQuickItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `bool`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setContainmentMask(QObject *mask)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setContainmentMask`。调用它会改变 `QQuickItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `mask`：类型为 `QObject *`。没有默认值，调用时必须提供。Qt 对象参数。要确认对象有效、线程归属、所有权和该 API 是否只处理直接子对象。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setEnabled(bool)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setEnabled`。调用它会改变 `QQuickItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `bool`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setFocus(bool)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setFocus`。调用它会改变 `QQuickItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `bool`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setFocus(bool focus, Qt::FocusReason reason)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setFocus`。调用它会改变 `QQuickItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `focus`：类型为 `bool`。没有默认值，调用时必须提供。传入 `bool` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `reason`：类型为 `Qt::FocusReason`。没有默认值，调用时必须提供。传入 `Qt::FocusReason` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setHeight(qreal)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setHeight`。调用它会改变 `QQuickItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `qreal`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setImplicitHeight(qreal)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setImplicitHeight`。调用它会改变 `QQuickItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `qreal`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setImplicitWidth(qreal)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setImplicitWidth`。调用它会改变 `QQuickItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `qreal`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setOpacity(qreal)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setOpacity`。调用它会改变 `QQuickItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `qreal`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setParentItem(QQuickItem *parent)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setParentItem`。调用它会改变 `QQuickItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `parent`：类型为 `QQuickItem *`。没有默认值，调用时必须提供。父对象。设置后通常由父对象负责销毁子对象；只有在对象确实应挂入这棵对象树时才传入。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setRotation(qreal)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setRotation`。调用它会改变 `QQuickItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `qreal`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setScale(qreal)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setScale`。调用它会改变 `QQuickItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `qreal`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setSmooth(bool)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setSmooth`。调用它会改变 `QQuickItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `bool`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setState(const QString &)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setState`。调用它会改变 `QQuickItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `const QString &`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setTransformOrigin(QQuickItem::TransformOrigin)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setTransformOrigin`。调用它会改变 `QQuickItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `TransformOrigin`：类型为 `QQuickItem::`。没有默认值，调用时必须提供。传入 `QQuickItem::` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setVisible(bool)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setVisible`。调用它会改变 `QQuickItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `bool`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setWidth(qreal)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setWidth`。调用它会改变 `QQuickItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `qreal`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setX(qreal)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setX`。调用它会改变 `QQuickItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `qreal`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setY(qreal)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setY`。调用它会改变 `QQuickItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `qreal`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void setZ(qreal)`

**API 类别：** 公有函数

**中文解读：** 这是配置/写入操作 `setZ`。调用它会改变 `QQuickItem` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `qreal`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool smooth() const`

**API 类别：** 公有函数

**中文解读：** `QQuickItem::smooth` 用于计算、查询或取得与“smooth”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QString state() const`

**API 类别：** 公有函数

**中文解读：** `QQuickItem::state` 用于计算、查询或取得与“state”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QString`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QString`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QQuickItem::TransformOrigin transformOrigin() const`

**API 类别：** 公有函数

**中文解读：** `QQuickItem::transformOrigin` 用于计算、查询或取得与“transform、Origin”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QQuickItem::TransformOrigin`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QQuickItem::TransformOrigin`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal width() const`

**API 类别：** 公有函数

**中文解读：** `QQuickItem::width` 用于计算、查询或取得与“宽度”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal x() const`

**API 类别：** 公有函数

**中文解读：** `QQuickItem::x` 用于计算、查询或取得与“x”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal y() const`

**API 类别：** 公有函数

**中文解读：** `QQuickItem::y` 用于计算、查询或取得与“y”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qreal z() const`

**API 类别：** 公有函数

**中文解读：** `QQuickItem::z` 用于计算、查询或取得与“z”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `qreal`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qreal`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void activeFocusChanged(bool)`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `activeFocusChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `bool`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void activeFocusOnTabChanged(bool)`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `activeFocusOnTabChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `bool`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void antialiasingChanged(bool)`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `antialiasingChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `bool`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void baselineOffsetChanged(qreal)`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `baselineOffsetChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `qreal`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void childrenRectChanged(const QRectF &)`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `childrenRectChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `const QRectF &`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void clipChanged(bool)`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `clipChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `bool`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void containmentMaskChanged()`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `containmentMaskChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void enabledChanged()`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `enabledChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void focusChanged(bool)`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `focusChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `bool`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void focusPolicyChanged(Qt::FocusPolicy)`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `focusPolicyChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `FocusPolicy`：类型为 `Qt::`。没有默认值，调用时必须提供。传入 `Qt::` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void heightChanged()`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `heightChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void implicitHeightChanged()`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `implicitHeightChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void implicitWidthChanged()`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `implicitWidthChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void opacityChanged()`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `opacityChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void parentChanged(QQuickItem *)`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `parentChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `QQuickItem *`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void rotationChanged()`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `rotationChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void scaleChanged()`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `scaleChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void smoothChanged(bool)`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `smoothChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `bool`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void stateChanged(const QString &)`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `stateChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `const QString &`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void transformOriginChanged(QQuickItem::TransformOrigin)`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `transformOriginChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `TransformOrigin`：类型为 `QQuickItem::`。没有默认值，调用时必须提供。传入 `QQuickItem::` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void visibleChanged()`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `visibleChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void widthChanged()`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `widthChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void xChanged()`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `xChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void yChanged()`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `yChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void zChanged()`

**API 类别：** 信号

**中文解读：** 这是状态变化通知 `zChanged`。应用代码通常连接它而不是直接调用它；收到通知后读取当前值并更新依赖对象，不要假设通知一定只发一次或已经代表业务操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

## 6. 深入实践与常见坑

### 生命周期和资源边界

QML 引擎、上下文和对象所有权必须明确。由 QML 创建的对象通常由引擎管理；通过 context property 或 C++ 暴露的对象要决定由 C++ 持有还是转移给 QML，不能让绑定指向悬空对象。

### 状态和错误边界

属性绑定和直接赋值不是一回事：直接给被绑定属性赋值通常会打破原有绑定。C++ 属性要有正确的 notify signal，QML 才能在数据变化时更新；信号参数和属性当前值要保持一致。

### 线程边界

大多数 QML 对象和 GUI 操作在 GUI 线程，场景图渲染还可能在 render thread。不要在渲染阶段调用 GUI 对象 API；后台数据通过线程安全的信号/槽边界送入 QML。

### 最容易出现的错误

不要在 QML 绑定中产生副作用；注意 QObject 所有权；区分 GUI 线程和 render thread；注册类型版本要稳定。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QQuickItem` 所属机制类型：QML 属性绑定与场景图机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
