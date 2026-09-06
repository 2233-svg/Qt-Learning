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

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QQuickItem::Flagflags QQuickItem::Flags`

**作用与语义：**

该枚举类型用于指定各种项目属性。
- `QQuickItem::ItemClipsChildrenToShape`：`0x01`;表示该项目应视觉上裁剪其子节点，使其仅在本项目边界内渲染。
- `QQuickItem::ItemAcceptsInputMethod`：`0x02`;表示该项目支持文本输入法。
- `QQuickItem::ItemIsFocusScope`：`0x04`;表示该物品是对焦示波器。更多信息请参见Qt Quick中的键盘聚焦。
- `QQuickItem::ItemHasContents`：`0x08`;表示该物品具有视觉内容，应由场景图渲染。
- `QQuickItem::ItemAcceptsDrops`：`0x10`;表示该物品接受拖放事件。
- `QQuickItem::ItemIsViewport`：`0x20`;表示该项为其子节点定义了一个视口。
- `QQuickItem::ItemObservesViewport`：`0x40`;表示当任何祖先设置了ItemIsViewport标志时，该项希望知道视口边界。
Flags 类型是 QFlags 的 typedef<Flag>。它存储 Flag 值的 OR 组合。

### `enum QQuickItem::ItemChange`

**作用与语义：**

与`QQuickItem::itemChange()`配合使用，用于通知该项目某些类型的变更。
- `QQuickItem::ItemChildAddedChange`：`0`;添加了一个子节点。`ItemChangeData::item` 包含了新增的子节点。
- `QQuickItem::ItemChildRemovedChange`：`1`;一个孩子被移除。`ItemChangeData::item`包含被移除的孩子。
- `QQuickItem::ItemSceneChange`：`2`;该物品被添加到或移除场景中。渲染场景的`QQuickWindow`在使用 `ItemChangeData::window` 中指定。当物品从场景中移除时，窗口参数为空。
- `QQuickItem::ItemVisibleHasChanged`：`3`;该物品的可见性发生变化。`ItemChangeData::boolValue` 包含新的可见性。
- `QQuickItem::ItemParentHasChanged`：`4`;该项的父项发生了变化。`ItemChangeData::item` 包含新的父项。
- `QQuickItem::ItemOpacityHasChanged`：`5`;该物品的不透明度发生了变化。`ItemChangeData::realValue` 包含新的不透明度。
- `QQuickItem::ItemActiveFocusHasChanged`：`6`;物品的焦点发生变化。`ItemChangeData::boolValue` 显示物品是否具有焦点。
- `QQuickItem::ItemRotationHasChanged`：`7`;该物品的旋转发生了变化。`ItemChangeData::realValue`包含新的旋转。
- `QQuickItem::ItemDevicePixelRatioHasChanged`：`9`;该项目所在屏幕的设备像素比发生了变化。ItemChangedData：：realValue 包含新的设备像素比。
- `QQuickItem::ItemAntialiasingHasChanged`：`8`;抗锯齿发生了变化。当前（布尔值）可在`QQuickItem::antialiasing`中找到。
- `QQuickItem::ItemEnabledHasChanged`：`10`;项的启用状态发生变化。`ItemChangeData::boolValue` 包含新的启用状态。（自第5.10个Qt起）
- `QQuickItem::ItemScaleHasChanged`：`11`;该项的刻度发生了变化。`ItemChangeData::realValue` 包含刻度。（自第6.9卷起）
- `QQuickItem::ItemTransformHasChanged`：`12`;该项的变换发生了变化。当项的位置、大小、旋转、缩放`transformOrigin`或附加变换发生变化时，就会发生变化。`ItemChangeData::item` 包含导致变更的项。（自第6.9卷起）

### `enum QQuickItem::TransformOrigin`

**作用与语义：**

控制哪些简单的变换，比如尺度，可以应用。
- `QQuickItem::TopLeft`：`0`;物品的左上角。
- `QQuickItem::Top`：`1`;物品顶部的中心点。
- `QQuickItem::TopRight`：`2`;物品右上角。
- `QQuickItem::Left`：`3`;垂直中点的最左端。
- `QQuickItem::Center`：`4`;物品的中心。
- `QQuickItem::Right`：`5`;垂直中点的最右端。
- `QQuickItem::BottomLeft`：`6`;物品的左下角。
- `QQuickItem::Bottom`：`7`;物品底部的中心点。
- `QQuickItem::BottomRight`：`8`;物品的右下角。

### `[read-only] activeFocus : bool`

**作用与语义：**

该只读特性表示该项是否具有主动焦点。
如果 activeFocus 为真，则该项要么是当前接收键盘输入的项，要么是当前接收键盘输入项的`FocusScope`祖先。
通常，activeFocus 通过在物品及其包围的`FocusScope`对象上设置 `focus` 来实现。在以下示例中，`input` 和 `focusScope` 对象将有主动焦点，而根矩形对象则没有。

**如何使用：** 调用 `activeFocus()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 import QtQuick 2.0

 Rectangle {
     width: 100; height: 100

     FocusScope {
         focus: true

         TextInput {
             id: input
             focus: true
         }
     }
 }
```

### `activeFocusOnTab : bool`

**作用与语义：**

该属性决定项是否希望处于标签焦点链中。默认情况下，该项设置为`false`。
注意：`tabFocusBehavior`还可以进一步限制只关注特定类型的控件，比如仅限文本或列表控件。macOS 上就是这样，根据系统设置，可能会限制对特定控件的关注。

**如何使用：** 调用 `activeFocusOnTab()` 读取当前值；它不会修改应用状态。

### `antialiasing : bool`

**作用与语义：**

指定该项目是否进行了抗锯齿处理。
视觉元素用于决定物品是否应使用抗锯齿。在某些情况下，带有抗锯齿的物品需要更多内存，渲染速度也可能更慢（详见抗锯齿部分）。
默认为假，但可被派生元素覆盖。

**如何使用：** 调用 `antialiasing()` 读取当前值；它不会修改应用状态。

### `baselineOffset : qreal`

**作用与语义：**

指定该物品基线在本地坐标中的位置。
`Text`项的基线是文本所处的虚数线。包含文本的控件通常将其基线设置为文本的基线。
对于非文本项目，默认基线偏移量为0。

**如何使用：** 调用 `baselineOffset()` 读取当前值；它不会修改应用状态。

### `[read-only] childrenRect : QRectF`

**作用与语义：**

该属性包含该物品子的集体位置和大小。
如果你需要访问某个物品子节点的集体几何体以正确调整该项目的大小，这个属性非常有用。
返回的几何体是该项目的局部。例如：

**如何使用：** 调用 `childrenRect()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 Item {
     x: 50
     y: 100

     // prints: QRectF(-10, -20, 30, 40)
     Component.onCompleted: print(childrenRect)

     Item {
         x: -10
         y: -20
         width: 30
         height: 40
     }
 }
```

### `clip : bool`

**作用与语义：**

该属性适用于是否启用裁剪。默认裁剪值为 `false`。
如果启用裁剪，项将裁剪自身绘制内容以及其子项的绘制内容到其边界矩形。如果在项的绘制操作中设置了裁剪，请记得重新设置，以防裁剪场景的其他部分。
注意：裁剪可能影响渲染性能。有关更多信息，请参见裁剪。
注意：为了 QML，如果将 clip 设置为 `true`，也会设置 `ItemIsViewport` 标志，这有时作为一种优化：具有 `ItemObservesViewport` 标志的子项可以省略创建视口外的场景图节点。但 `ItemIsViewport` 标志也可以独立设置。

**如何使用：** 调用 `clip()` 读取当前值；它不会修改应用状态。

### `containmentMask : QObject*`

**作用与语义：**

该属性包含一个可选遮罩，用于`contains()`方法，主要用于每个`QPointerEvent`的命中测试。
默认情况下，`contains()` 会返回物品边界框内任意点的 `true`。但任何实现函数 的`QQuickItem`或任何实现 函数的`QObject`。
可以用作掩体，将测试推迟到该对象。
注意：`contains()` 在事件传递过程中经常被调用。将击中测试推迟到另一个对象会在一定程度上减慢速度。如果该对象的 `contains()` 方法效率不高，containmentMask() 可能会引发性能问题。如果你实现了自定义的 `QQuickItem` 子类，也可以选择覆盖`contains()`。

**如何使用：** 调用 `containmentMask()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 Q_INVOKABLE bool contains(const QPointF &point) const;
```

### `enabled : bool`

**作用与语义：**

该属性决定项目是否接收鼠标和键盘事件。默认情况下，这为真。
设置该属性直接影响子项的`enabled`值。当设置为`false`时，所有子项的`enabled`值也会变为`false`。当设置为`true`时，子项的`enabled`值会返回`true`，除非它们被明确设置为`false`。
将该属性设置为`false`会自动使`activeFocus`被设置为`false`，该项将不再接收键盘事件。
注意：悬停事件由`setAcceptHoverEvents()`单独启用。因此，禁用的物品即使该属性被`false`，仍可继续接收悬停事件。这使得即使关闭交互项，仍能显示信息反馈（如`ToolTip`）。任何作为物品子节点添加的`HoverHandlers`同样适用。然而，`HoverHandler`可以显式`disabled`，或者例如绑定到物品的 `enabled` 状态。

**如何使用：** 调用 `enabled()` 读取当前值；它不会修改应用状态。

### `focus : bool`

**作用与语义：**

该只读特性表示该项是否具有主动焦点。
如果 activeFocus 为真，则该项要么是当前接收键盘输入的项，要么是当前接收键盘输入项的`FocusScope`祖先。
通常，activeFocus 通过在物品及其包围的`FocusScope`对象上设置 `focus` 来实现。在以下示例中，`input` 和 `focusScope` 对象将有主动焦点，而根矩形对象则没有。

**如何使用：** 调用 `focus()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 import QtQuick 2.0

 Rectangle {
     width: 100; height: 100

     FocusScope {
         focus: true

         TextInput {
             id: input
             focus: true
         }
     }
 }
```

### `[since 6.7] focusPolicy : Qt::FocusPolicy`

**作用与语义：**

该属性决定了物品接受聚焦的方式。

**如何使用：** 调用 `focusPolicy()` 读取当前值；它不会修改应用状态。

### `[bindable] height : qreal`

**作用与语义：**

该只读特性表示该项是否具有主动焦点。
如果 activeFocus 为真，则该项要么是当前接收键盘输入的项，要么是当前接收键盘输入项的`FocusScope`祖先。
通常，activeFocus 通过在物品及其包围的`FocusScope`对象上设置 `focus` 来实现。在以下示例中，`input` 和 `focusScope` 对象将有主动焦点，而根矩形对象则没有。

**如何使用：** 调用 `height()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 import QtQuick 2.0

 Rectangle {
     width: 100; height: 100

     FocusScope {
         focus: true

         TextInput {
             id: input
             focus: true
         }
     }
 }
```

### `implicitWidth : qreal`

**作用与语义：**

定义物品的首选宽度或高度。
如果未指定`width`或`height`，则物品的有效尺寸将由其`implicitWidth`或`implicitHeight`确定。
然而，如果某个项目是布局的子节点，布局会通过其隐式大小决定该项目的首选大小。在这种情况下，显式的`width`或`height`将被忽略。
大多数项目默认隐式大小为0x0，但某些项固有隐式大小无法覆盖，例如`Image`和`Text`。
设置隐式大小对于定义基于内容具有优先大小的组件非常有用，例如：
注意：使用`Text`或`TextEdit` `implicitWidth`并明确设置宽度会带来性能惩罚，因为文本必须排版两次。

**如何使用：** 调用 `implicitWidth()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 // Label.qml
 import QtQuick 2.0

 Item {
     property alias icon: image.source
     property alias label: text.text
     implicitWidth: text.implicitWidth + image.implicitWidth
     implicitHeight: Math.max(text.implicitHeight, image.implicitHeight)
     Image { id: image }
     Text {
         id: text
         wrapMode: Text.Wrap
         anchors.left: image.right; anchors.right: parent.right
         anchors.verticalCenter: parent.verticalCenter
     }
 }
```

### `opacity : qreal`

**作用与语义：**

该属性包含该项的不透明度。不透明度指定为0.0（完全透明）到1.0（完全不透明）之间的数值。默认值为1.0。
当该属性被设置时，指定的不透明度也会单独应用到子项上。在某些情况下，这可能会产生意想不到的影响。例如，在下面的第二组矩形中，红色矩形指定了0.5的不透明度，这影响了其蓝色子矩形的不透明度，尽管该子矩形并未指定不透明度。
0到1范围之外的数值会被夹紧。
- '`: `Item' {
`Rectangle` {。
颜色：“红色”。
宽度：100;高度：100。
`Rectangle` {。
颜色：“蓝色”。
x：50;y：50;宽度：100;高度：100。
}。
}。
}。
- '`: `Item' {
`Rectangle` {。
不透明度：0.5。
颜色：“红色”。
宽度：100;高度：100。
`Rectangle` {。
颜色：“蓝色”。
x：50;y：50;宽度：100;高度：100。
}。
}。
}。
更改物品的透明度不会影响该物品是否接收用户输入事件。（相比之下，将`visible`属性设置为`false`会停止鼠标事件，将`enabled`属性设置为`false`则停止鼠标和键盘事件，同时移除对该物品的主动关注。）。

**如何使用：** 调用 `opacity()` 读取当前值；它不会修改应用状态。

### `parent : QQuickItem*`

**作用与语义：**

定义物品的首选宽度或高度。
如果未指定`width`或`height`，则物品的有效尺寸将由其`implicitWidth`或`implicitHeight`确定。
然而，如果某个项目是布局的子节点，布局会通过其隐式大小决定该项目的首选大小。在这种情况下，显式的`width`或`height`将被忽略。
大多数项目默认隐式大小为0x0，但某些项固有隐式大小无法覆盖，例如`Image`和`Text`。
设置隐式大小对于定义基于内容具有优先大小的组件非常有用，例如：
注意：使用`Text`或`TextEdit` `implicitWidth`并明确设置宽度会带来性能惩罚，因为文本必须排版两次。

**如何使用：** 调用 `parent()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 // Label.qml
 import QtQuick 2.0

 Item {
     property alias icon: image.source
     property alias label: text.text
     implicitWidth: text.implicitWidth + image.implicitWidth
     implicitHeight: Math.max(text.implicitHeight, image.implicitHeight)
     Image { id: image }
     Text {
         id: text
         wrapMode: Text.Wrap
         anchors.left: image.right; anchors.right: parent.right
         anchors.verticalCenter: parent.verticalCenter
     }
 }
```

### `rotation : qreal`

**作用与语义：**

该属性表示物品围绕其`transformOrigin`顺时针旋转的度数。
默认值为0度（即不旋转）。
- '`: `Rectangle' {
颜色：“蓝色”。
宽度：100;高度：100。
`Rectangle` {。
颜色：“红色”。
x：25;y：25;宽度：50;高度：50。
轮换：30。
}。
}。

**如何使用：** 调用 `rotation()` 读取当前值；它不会修改应用状态。

### `scale : qreal`

**作用与语义：**

该属性表示该项的比例因子。
比例小于1.0时，物品的渲染尺寸变小;比例大于1.0时，物品的尺寸会变大。负比例则表示物品在渲染时被镜像化。
默认值是1.0。
缩放是从`transformOrigin`开始的。
- ''： import QtQuick 2.0

`Rectangle` {。
颜色：“蓝色”。
宽度：100;高度：100。

`Rectangle` {。
颜色：“绿色”。
宽度：25;高度：25。
}。

`Rectangle` {。
颜色：“红色”。
x：25;y：25;宽度：50;高度：50。
比例：1.4。
}。
}。

**如何使用：** 调用 `scale()` 读取当前值；它不会修改应用状态。

### `smooth : bool`

**作用与语义：**

指定该项目是否被平滑处理。
主要用于基于图像的项目，以决定该项目是否应使用平滑采样。平滑采样通过线性插值实现，而非平滑采样则使用最近邻进行。
在 Qt Quick 2.0 中，这一特性对性能的影响很小。
默认情况下，该属性被设置为`true`。

**如何使用：** 调用 `smooth()` 读取当前值；它不会修改应用状态。

### `state : QString`

**作用与语义：**

该属性保存项目当前状态的名称。
如果项目处于默认状态，即未设置任何显式状态，则该属性保存为空字符串。同样，可以通过将此属性设置为空字符串将项目恢复到默认状态。

**如何使用：** 调用 `state()` 读取当前值；它不会修改应用状态。

### `transformOrigin : TransformOrigin`

**作用与语义：**

此属性保存缩放和旋转变换的原点。
提供九个变换原点，如下图所示。默认的变换原点是 `Item.Center`。

**如何使用：** 调用 `transformOrigin()` 读取当前值；它不会修改应用状态。

### `visible : bool`

**作用与语义：**

该属性在物品可见时成立。默认情况下，这点成立。
设置该属性直接影响子项的`visible`值。当设置为`false`时，所有子项的`visible`值也会变为`false`。当设置为`true`时，子项的`visible`值会返回`true`，除非它们明确设置为`false`。
（由于这种连贯行为，如果属性绑定只对显式属性变化做出响应，使用`visible`属性可能无法达到预期效果。在这种情况下，使用`opacity`属性可能更好。）。
如果该属性设置为`false`，物品将不再接收鼠标事件，但会继续接收按键事件，并且如果已设置，键盘`focus`会保留。（相反，将`enabled`属性设置为`false`会停止鼠标和键盘事件，同时移除对物品的关注。）。
注意：该属性的价值仅会因该属性或父`visible`属性的变化而受到影响。例如，如果该物品移出屏幕，或者`opacity`变为0，属性不会改变。但出于历史原因，该属性在物品构建后依然成立，即使该物品尚未添加到场景中。更改或读取尚未添加到场景中的物品的属性可能无法达到预期效果。
注意：该属性的通知信号在视觉父节点销毁时发出。C 信号处理者不能假设视觉父层级中的项目仍然完整构建。使用`qobject_cast`验证父层级中的项目是否可以安全地作为预期类型使用。

**如何使用：** 调用 `visible()` 读取当前值；它不会修改应用状态。

### `[bindable] width : qreal`

**作用与语义：**

该只读特性表示该项是否具有主动焦点。
如果 activeFocus 为真，则该项要么是当前接收键盘输入的项，要么是当前接收键盘输入项的`FocusScope`祖先。
通常，activeFocus 通过在物品及其包围的`FocusScope`对象上设置 `focus` 来实现。在以下示例中，`input` 和 `focusScope` 对象将有主动焦点，而根矩形对象则没有。

**如何使用：** 调用 `width()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 import QtQuick 2.0

 Rectangle {
     width: 100; height: 100

     FocusScope {
         focus: true

         TextInput {
             id: input
             focus: true
         }
     }
 }
```

### `[bindable] x : qreal`

**作用与语义：**

该属性包含该物品子的集体位置和大小。
如果你需要访问某个物品子节点的集体几何体以正确调整该项目的大小，这个属性非常有用。
返回的几何体是该项目的局部。例如：

**如何使用：** 调用 `x()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 Item {
     x: 50
     y: 100

     // prints: QRectF(-10, -20, 30, 40)
     Component.onCompleted: print(childrenRect)

     Item {
         x: -10
         y: -20
         width: 30
         height: 40
     }
 }
```

### `[bindable] y : qreal`

**作用与语义：**

该属性包含该物品子的集体位置和大小。
如果你需要访问某个物品子节点的集体几何体以正确调整该项目的大小，这个属性非常有用。
返回的几何体是该项目的局部。例如：

**如何使用：** 调用 `y()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 Item {
     x: 50
     y: 100

     // prints: QRectF(-10, -20, 30, 40)
     Component.onCompleted: print(childrenRect)

     Item {
         x: -10
         y: -20
         width: 30
         height: 40
     }
 }
```

### `z : qreal`

**作用与语义：**

设置兄弟项目的叠加顺序。默认堆叠顺序为0。
叠加值较高的物品会被绘制在叠加顺序较低的兄弟姐妹上。叠加值相同的物品按出现顺序从下而上绘制。叠加值为负的物品则会被绘制在其父内容下方。
以下示例展示了堆叠顺序的各种影响。
- '`: Same `z' - 较早子节点之上后期子节点：
`Item` {。
`Rectangle` {。
颜色：“红色”。
宽度：100;高度：100。
}。
`Rectangle` {。
颜色：“蓝色”。
x：50;y：50;宽度：100;高度：100。
}。
}。
- 顶部的“`: Higher `z”：
`Item` {。
`Rectangle` {。
Z：1。
颜色：“红色”。
宽度：100;高度：100。
}。
`Rectangle` {。
颜色：“蓝色”。
x：50;y：50;宽度：100;高度：100。
}。
}。
- '`: Same `z' - 父之上的子节点：
`Item` {。
`Rectangle` {。
颜色：“红色”。
宽度：100;高度：100。
`Rectangle` {。
颜色：“蓝色”。
x：50;y：50;宽度：100;高度：100。
}。
}。
}。
- “`: Lower `z”如下：
`Item` {。
`Rectangle` {。
颜色：“红色”。
宽度：100;高度：100。
`Rectangle` {。
Z：-1。
颜色：“蓝色”。
x：50;y：50;宽度：100;高度：100。
}。
}。
}。

**如何使用：** 调用 `z()` 读取当前值；它不会修改应用状态。

### `[explicit] QQuickItem::QQuickItem(QQuickItem *parent = nullptr)`

**作用与语义：**

构造一个带有给定`parent`的QQuickItem。
`parent`将同时作为视觉父体和`QObject`父体使用。

### `[override virtual noexcept] QQuickItem::~QQuickItem()`

**作用与语义：**

摧毁了`QQuickItem`。

### `bool QQuickItem::acceptHoverEvents() const`

**作用与语义：**

返回该项目是否接受悬停事件。
默认值为假。
如果为假，则该物品不会通过`hoverEnterEvent()`、`hoverMoveEvent()`和`hoverLeaveEvent()`函数接收任何悬停事件。

### `bool QQuickItem::acceptTouchEvents() const`

**作用与语义：**

返回该项目是否接受触摸事件。
默认值是`false`。
如果`false`，则该物品不会通过`touchEvent()`函数接收任何触摸事件。

### `Qt::MouseButtons QQuickItem::acceptedMouseButtons() const`

**作用与语义：**

返回该物品接受的鼠标按键。
默认值为`Qt::NoButton`;即不接受鼠标按键。
如果某个物品不接受某个鼠标事件的鼠标按钮，鼠标事件不会被送达到该物品上，而是会被送到物品层级中的下一个物品上。

### `[virtual] QRectF QQuickItem::boundingRect() const`

**作用与语义：**

返回该项自身坐标系的范围：从`0, 0`到`width()`和`height()`的矩形。

### `[invokable] QQuickItem *QQuickItem::childAt(qreal x, qreal y) const`

**作用与语义：**

返回该项坐标系中在点（`x`， `y`）找到的第一个可见子项。
如果没有此类物品，退货`nullptr`。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `QList<QQuickItem *> QQuickItem::childItems() const`

**作用与语义：**

还给该物品的子嗣。

### `[virtual protected] bool QQuickItem::childMouseEventFilter(QQuickItem *item, QEvent *event)`

**作用与语义：**

重新实现该方法以过滤该项子节点接收到的指针事件。
只有当`filtersChildMouseEvents()` `true`时才调用此方法。
如果指定`event`不应传递给指定的子 `item`，则返回 `true`，否则`false`。如果返回 `true`，还应`accept`或`ignore` `event`，以提示事件传播应停止还是继续。然而，`event`始终会发送给父链上的所有 childMouseEventFilters。
注意：尽管名称如此，该函数在向所有子类（通常是鼠标、触摸和平板事件）传递过程中过滤所有 `QPointerEvent` 实例。在子类中覆盖该函数时，建议仅使用`QPointerEvent`中的访问器编写通用事件处理代码。或者，您也可以开启 `event->type()` 和/或 `event->device()->type()`，以不同方式处理不同事件类型。
注意：过滤只是在手势模糊时分担责任的一种方式（例如在按压时，你不知道用户是点击还是拖动）。另一种方法是在按时调用`QPointerEvent::addPassiveGrabber()`，以便非独占地监控`QEventPoint`的进度。无论哪种情况，监控的项目或指针处理器都可以在后来发现手势符合预期模式时窃取独占抓取。

### `[override virtual protected] void QQuickItem::classBegin()`

**作用与语义：**

重装：`QQmlParserStatus::classBegin()`。
派生类应在添加自己在 classBegin 执行的动作之前调用基类方法。

### `[virtual] QRectF QQuickItem::clipRect() const`

**作用与语义：**

如果有视口且`ItemObservesViewport`标志已设置，返回该项内当前在`viewportItem()`中可见的矩形区域;否则，返回该项在其自身坐标系中的范围：从`0, 0`到`width()`和`height()`的矩形。这是在`true`时应保持可见的区域`clip`。它也可以用于`updatePaintNode()`限制添加到场景图的图形。
例如，一个大型绘图或大型文本文档可能显示在仅占应用窗口部分的 Flickable 中：此时，Flickable 是视口项目，自定义内容渲染项目可能会选择省略落在当前可见区域之外的场景图节点。如果设置了 `ItemObservesViewport` 标志，每次用户滚动 Flickable 内容时，该区域都会变化。
对于嵌套视口项目，clipRect() 是所有具有 `ItemIsViewport` 标志集的祖先的 `boundingRect` 的交集，映射到该元素的坐标系。

### `[override virtual protected] void QQuickItem::componentComplete()`

**作用与语义：**

重装：`QQmlParserStatus::componentComplete()`。
派生类应在添加自己在componentComplete执行的操作前调用基类方法。

### `[virtual invokable] bool QQuickItem::contains(const QPointF &point) const`

**作用与语义：**

如果该项包含`point`，且位于本地坐标内，则返回`true`;否则返回`false`。
该函数可以被覆盖，以处理带有自定义形状的物品中的点碰撞。默认实现检查点是否在`containmentMask()`内（如果设定）或是否在边界框内。
注意：该方法用于事件交付期间的每个`QEventPoint`的命中测试，因此实现应尽可能轻量化。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `QCursor QQuickItem::cursor() const`

**作用与语义：**

返回该物品的光标形状。
当鼠标光标位于该项上时，将呈现该形状，除非设置覆盖光标。请参阅预定义光标对象列表，了解一系列有用的形状。
如果没有设置光标形状，则返回一个`Qt::ArrowCursor`形状的光标，但如果重叠的项目有有效的光标，可能会显示另一个光标形状。

### `[virtual protected] void QQuickItem::dragEnterEvent(QDragEnterEvent *event)`

**作用与语义：**

该事件处理程序可以在子类中重新实现，以接收物品的拖入事件。事件信息由`event`参数提供。
拖放事件只有在该物品已设置`ItemAcceptsDrops`标志时才会提供。
该事件默认被接受，因此如果你重新实现该函数，无需显式接受该事件。如果你不接受该事件，则调用`event->ignore()`。

### `[virtual protected] void QQuickItem::dragLeaveEvent(QDragLeaveEvent *event)`

**作用与语义：**

该事件处理程序可以在子类中重新实现，以接收项目的拖放事件。事件信息由`event`参数提供。
拖放事件仅在该物品已设置`ItemAcceptsDrops`标志时提供。
该事件默认被接受，因此如果你重新实现该函数，无需显式接受该事件。如果你不接受该事件，请调用`event->ignore()`。

### `[virtual protected] void QQuickItem::dragMoveEvent(QDragMoveEvent *event)`

**作用与语义：**

该事件处理程序可以在子类中重新实现，以接收某项的拖动移动事件。事件信息由`event`参数提供。
拖放事件只有在该物品已设置`ItemAcceptsDrops`标志时才会被触发。
该事件默认被接受，因此如果你重新实现该函数，无需显式接受该事件。如果你不接受该事件，请调用`event->ignore()`。

### `[virtual protected] void QQuickItem::dropEvent(QDropEvent *event)`

**作用与语义：**

该事件处理程序可以在子类中重新实现，以接收物品的丢弃事件。事件信息由 `event` 参数提供。
拖放事件仅在该物品设置了`ItemAcceptsDrops`标志时才会提供。
该事件默认被接受，因此如果你重新实现该函数，无需显式接受该事件。如果你不接受该事件，则调用`event->ignore()`。

### `[invokable, since 6.3] void QQuickItem::dumpItemTree() const`

**作用与语义：**

递归地倾倒了从该物品开始的视觉树的细节。
注意：`QObject::dumpObjectTree()`导出了类似的树;但正如Qt Quick中的概念-视觉父文中解释的，物品的 `QObject::parent()` 有时会与其 `QQuickItem::parentItem()` 不同。你可以同时导出两棵树以查看区别。
注意：具体的输出格式在未来版本的Qt中可能会有所更改。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[invokable, since 6.3] void QQuickItem::ensurePolished()`

**作用与语义：**

调用`updatePolish()`。
这对像布局（或定位器）等会延迟计算其`implicitWidth`和`implicitHeight`直到收到PolishEvent的物品非常有用。
通常，例如，如果向布局添加或移除子项，隐式大小不会立即计算（这是一种优化）。在某些情况下，可能需要在子项添加后立即查询布局的隐式大小。如果是这样，请在查询隐式大小之前使用该函数。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[override virtual protected] bool QQuickItem::event(QEvent *ev)`

**作用与语义：**

重实现自：`QObject::event`（QEvent *e）。

### `bool QQuickItem::filtersChildMouseEvents() const`

**作用与语义：**

返回是否应通过该项过滤该项的指针事件。
如果该项和子项都`acceptTouchEvents()` `true`，那么当发生触控交互时，该项会过滤触摸事件。但如果该项或子节点无法处理触摸事件，`childMouseEventFilter()`会被调用合成鼠标事件。

### `QQuickItem::Flags QQuickItem::flags() const`

**作用与语义：**

返回该物品的标记。

### `[virtual protected] void QQuickItem::focusInEvent(QFocusEvent *event)`

**作用与语义：**

该事件处理程序可以在子类中重新实现，以接收某项的焦点事件。事件信息由 `event` 参数提供。
该事件默认被接受，因此如果你重新实现该函数，无需显式接受该事件。如果你不接受该事件，就调用`event->ignore()`。
如果你真的要重写这个函数，你应该调用基础类实现。

### `[virtual protected] void QQuickItem::focusOutEvent(QFocusEvent *event)`

**作用与语义：**

该事件处理程序可以在子类中重新实现，以接收某个项目的焦点输出事件。事件信息由`event`参数提供。
该事件默认被接受，因此如果你重新实现该函数，无需显式接受该事件。如果你不接受该事件，请调用`event->ignore()`。

### `[invokable] void QQuickItem::forceActiveFocus()`

**作用与语义：**

强制主动聚焦于该物品。
该方法聚焦于该项目，并确保对象层级中所有祖先`FocusScope`对象也被赋予`focus`。
焦点变化的原因将`Qt::OtherFocusReason`。使用重载方法指定焦点原因，以便更好地处理焦点变化。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[invokable] void QQuickItem::forceActiveFocus(Qt::FocusReason reason)`

**作用与语义：**

强制对应`reason`的物品进行主动聚焦。
该方法聚焦于该项，并确保对象层级中的所有祖先`FocusScope`对象也被赋予`focus`。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[virtual protected, since 6.0] void QQuickItem::geometryChange(const QRectF &newGeometry, const QRectF &oldGeometry)`

**作用与语义：**

调用该函数来处理该项几何体从`oldGeometry`到`newGeometry`的变化。如果两个几何体相同，则不做任何操作。
派生类必须在其实现中调用基类方法。

### `QSharedPointer<QQuickItemGrabResult> QQuickItem::grabToImage(const QSize &targetSize = QSize())`

**作用与语义：**

将该项目抓取到内存中的映像。
抓取是异步进行的，抓取完成后`QQuickItemGrabResult::ready()`信号会发出。
使用`targetSize`来指定目标图像的大小。默认情况下，结果的大小与项目相同。
如果抓取无法启动，函数返回`null`。
注意：该功能会将物品渲染到屏幕外的表面，并将该表面从GPU内存复制到CPU内存，这可能成本较高。对于“实时”预览，请使用`layers`或`ShaderEffectSource`。

### `[protected] bool QQuickItem::heightValid() const`

**作用与语义：**

返回高度属性是否被明确设置。

### `[virtual protected] void QQuickItem::hoverEnterEvent(QHoverEvent *event)`

**作用与语义：**

该事件处理程序可以在子类中重新实现，以接收某项的滑鼠进入事件。事件信息由`event`参数提供。
只有当`acceptHoverEvents()`为真时才会提供悬停事件。
该事件默认被接受，因此如果你重新实现该函数，无需显式接受该事件。如果你不接受该事件，就调用`event->ignore()`。

### `[virtual protected] void QQuickItem::hoverLeaveEvent(QHoverEvent *event)`

**作用与语义：**

该事件处理程序可以在子类中重新实现，以接收某个项的悬停-离开事件。事件信息由`event`参数提供。
只有当`acceptHoverEvents()`成立时才会提供悬停事件。
该事件默认被接受，因此如果你重新实现该函数，无需显式接受该事件。如果你不接受该事件，调用`event->ignore()`。

### `[virtual protected] void QQuickItem::hoverMoveEvent(QHoverEvent *event)`

**作用与语义：**

该事件处理程序可以在子类中重新实现，以接收某项的悬停移动事件。事件信息由`event`参数提供。
只有当`acceptHoverEvents()`为真时才会提供悬停事件。
该事件默认被接受，因此如果你重新实现该函数，无需显式接受该事件。如果你不接受该事件，就调用`event->ignore()`。

### `qreal QQuickItem::implicitWidth() const`

**作用与语义：**

定义物品的首选宽度或高度。
如果未指定`width`或`height`，则物品的有效尺寸将由其`implicitWidth`或`implicitHeight`确定。
然而，如果某个项目是布局的子节点，布局会通过其隐式大小决定该项目的首选大小。在这种情况下，显式的`width`或`height`将被忽略。
大多数项目默认隐式大小为0x0，但某些项固有隐式大小无法覆盖，例如`Image`和`Text`。
设置隐式大小对于定义基于内容具有优先大小的组件非常有用，例如：
注意：使用`Text`或`TextEdit` `implicitWidth`并明确设置宽度会带来性能惩罚，因为文本必须排版两次。

**如何使用：** 调用 `implicitWidth()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 // Label.qml
 import QtQuick 2.0

 Item {
     property alias icon: image.source
     property alias label: text.text
     implicitWidth: text.implicitWidth + image.implicitWidth
     implicitHeight: Math.max(text.implicitHeight, image.implicitHeight)
     Image { id: image }
     Text {
         id: text
         wrapMode: Text.Wrap
         anchors.left: image.right; anchors.right: parent.right
         anchors.verticalCenter: parent.verticalCenter
     }
 }
```

### `[virtual protected] void QQuickItem::inputMethodEvent(QInputMethodEvent *event)`

**作用与语义：**

该事件处理程序可以在子类中重新实现，以接收某项的输入法事件。事件信息由`event`参数提供。
该事件默认被接受，因此如果你重新实现该函数，无需显式接受该事件。如果你不接受该事件，调用`event->ignore()`。

### `[virtual] QVariant QQuickItem::inputMethodQuery(Qt::InputMethodQuery query) const`

**作用与语义：**

该方法仅适用于输入项。
如果该项是输入项，则应重新实现该方法，返回给定`query`相关的输入法标志。

### `bool QQuickItem::isAncestorOf(const QQuickItem *child) const`

**作用与语义：**

如果该物品是`child`的祖先（即该物品是`child`的父项，还是`child`的父项之一），返回`true`。

### `[protected] bool QQuickItem::isComponentComplete() const`

**作用与语义：**

如果 QML 组件的构造完成，则返回 true;否则返回 false。
通常建议延迟部分处理直到组件完成。

### `bool QQuickItem::isFocusScope() const`

**作用与语义：**

如果该物品是焦点范围，则返回真，否则返回假。

### `[virtual] bool QQuickItem::isTextureProvider() const`

**作用与语义：**

如果该项是纹理提供者，则返回 true。默认实现返回 false。
该函数可以从任何线程调用。

### `[virtual protected] void QQuickItem::itemChange(QQuickItem::ItemChange change, const QQuickItem::ItemChangeData &value)`

**作用与语义：**

当 `change` 发生在此项上时调用。 `value` 在适用时包含与更改相关的额外信息。 如果在子类中重新实现此方法，确保在实现的最后调用，以确保 `windowChanged()` 信号将被发射。

**官方示例：**

```cpp
 QQuickItem::itemChange(change, value);
```

### `bool QQuickItem::keepMouseGrab() const`

**作用与语义：**

返回鼠标输入是否应仅保留在该项。

### `bool QQuickItem::keepTouchGrab() const`

**作用与语义：**

返回该物品所抓取的触点是否应独占该物品。

### `[virtual protected] void QQuickItem::keyPressEvent(QKeyEvent *event)`

**作用与语义：**

该事件处理程序可以在子类中重新实现，以接收某个项目的按键事件。事件信息由`event`参数提供。
该事件默认被接受，因此如果你重新实现该函数，无需显式接受该事件。如果不接受该事件，调用`event->ignore()`。

### `[virtual protected] void QQuickItem::keyReleaseEvent(QKeyEvent *event)`

**作用与语义：**

该事件处理程序可以在子类中重新实现，以接收某个项目的密钥释放事件。事件信息由`event`参数提供。
该事件默认被接受，因此如果你重新实现该函数，无需显式接受该事件。如果不接受该事件，调用`event->ignore()`。

### `[invokable] QPointF QQuickItem::mapFromGlobal(const QPointF &point) const`

**作用与语义：**

将全局屏幕坐标系中的给定`point`映射到该项坐标系内的对应点，并返回映射后的坐标。
映射中使用的物品属性包括：`x`、`y`、`scale`、`rotation`、`transformOrigin`和`transform`。
如果这些物品属于不同的场景，映射会包含两个场景的相对位置。
例如，在 Qt Quick 组件中添加弹窗可能会很有帮助。
注意：窗口位置由窗口管理器完成，该值仅作为提示处理。因此，最终的窗口位置可能与预期不同。
注意：如果该物品位于子场景中，例如映射到3D `Model`物体上，UV映射会被纳入该变换中，因此只要`point`实际在该物体的范围内，它实际上是从屏幕坐标映射到该物品的坐标。其他映射函数目前还没有这种方式。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `[invokable] QPointF QQuickItem::mapFromItem(const QQuickItem *item, const QPointF &point) const`

**作用与语义：**

将`item`坐标系中的给定`point`映射到该项坐标系内的等效点，并返回映射后的坐标。
映射中使用的项的属性包括：`x`、`y`、`scale`、`rotation`、`transformOrigin`和`transform`。
如果这些物品属于不同的场景，映射会包含两个场景的相对位置。
如果`item`是`nullptr`，则`point`从场景的坐标系映射。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `QPointF QQuickItem::mapFromScene(const QPointF &point) const`

**作用与语义：**

将场景坐标系中的给定`point`映射到该元素坐标系内的对应点，并返回映射后的坐标。
映射中使用的项的以下属性包括：`x`、`y`、`scale`、`rotation`、`transformOrigin`和`transform`。
如果这些物品属于不同的场景，映射会包含两个场景的相对位置。

### `QRectF QQuickItem::mapRectFromItem(const QQuickItem *item, const QRectF &rect) const`

**作用与语义：**

将`item`坐标系中的给定`rect`映射到该项坐标系内的等效矩形区域，并返回映射后的矩形值。
映射中使用的项的属性包括：`x`、`y`、`scale`、`rotation`、`transformOrigin`和`transform`。
如果这些物品属于不同的场景，映射会包含两个场景的相对位置。
如果`item`是`nullptr`，则`rect`从场景的坐标系映射。

### `QRectF QQuickItem::mapRectFromScene(const QRectF &rect) const`

**作用与语义：**

将场景坐标系中的给定`rect`映射到该项目坐标系内对应的矩形区域，并返回映射后的矩形值。
映射中使用的物品属性包括：`x`、`y`、`scale`、`rotation`、`transformOrigin`和`transform`。
如果这些物品属于不同的场景，映射会包含两个场景的相对位置。

### `QRectF QQuickItem::mapRectToItem(const QQuickItem *item, const QRectF &rect) const`

**作用与语义：**

将该项坐标系中的给定`rect`映射到`item`坐标系内的等效矩形区域，并返回映射后的矩形值。
映射中使用的项的以下属性包括：`x`、`y`、`scale`、`rotation`、`transformOrigin`和`transform`。
如果这些物品属于不同的场景，映射会包含两个场景的相对位置。
如果`item` `nullptr`，则`rect`映射到场景的坐标系。

### `QRectF QQuickItem::mapRectToScene(const QRectF &rect) const`

**作用与语义：**

将该项目坐标系中的给定`rect`映射到场景坐标系内的等效矩形区域，并返回映射后的矩形值。
映射中使用的物品属性包括：`x`、`y`、`scale`、`rotation`、`transformOrigin`和`transform`。
如果这些物品属于不同的场景，映射会包含两个场景的相对位置。

### `[invokable] QPointF QQuickItem::mapToGlobal(const QPointF &point) const`

**作用与语义：**

将该项坐标系中的给定`point`映射到全局屏幕坐标系中的对应点，并返回映射后的坐标。
映射中使用的项的以下属性是：`x`、`y`、`scale`、`rotation`、`transformOrigin`和`transform`。
如果这些物品属于不同的场景，映射会包含两个场景的相对位置。
例如，在 Qt Quick 组件中添加弹窗可能会很有帮助。
注意：窗口位置由窗口管理器完成，该值仅作为提示处理。因此，最终的窗口位置可能与预期不同。
注意：该函数可通过元对象系统和QML调用。参见 `Q_INVOKABLE`。

### `[invokable] QPointF QQuickItem::mapToItem(const QQuickItem *item, const QPointF &point) const`

**作用与语义：**

将该项坐标系中的给定`point`映射到`item`坐标系内的对应点，并返回映射后的坐标。
映射中使用的项的以下属性包括：`x`、`y`、`scale`、`rotation`、`transformOrigin`和`transform`。
如果这些物品属于不同的场景，映射会包含两个场景的相对位置。
如果`item` `nullptr`，则`point`映射到场景的坐标系。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `QPointF QQuickItem::mapToScene(const QPointF &point) const`

**作用与语义：**

将该项目坐标系中的给定`point`映射到场景坐标系内的对应点，并返回映射后的坐标。
映射中使用的项的以下属性包括：`x`、`y`、`scale`、`rotation`、`transformOrigin`和`transform`。
如果这些物品属于不同的场景，映射会包含两个场景的相对位置。

### `[virtual protected] void QQuickItem::mouseDoubleClickEvent(QMouseEvent *event)`

**作用与语义：**

此事件处理程序可以在子类中重新实现，以接收项目的鼠标双击事件。事件信息通过 `event` 参数提供。
事件默认被接受，因此如果你重新实现此函数，则不需要显式接受事件。如果你不接受事件，请调用 `event->ignore()`。

### `[virtual protected] void QQuickItem::mouseMoveEvent(QMouseEvent *event)`

**作用与语义：**

此事件处理程序可以在子类中重新实现，以接收项目的鼠标移动事件。事件信息通过 `event` 参数提供。
为了接收鼠标移动事件，必须接受前一个鼠标按下事件（例如，通过重写 `mousePressEvent()`）并且 `acceptedMouseButtons()` 必须返回相关鼠标按钮。
事件默认被接受，因此如果你重新实现此函数，则不需要显式接受事件。如果你不接受事件，请调用 `event->ignore()`。

### `[virtual protected] void QQuickItem::mousePressEvent(QMouseEvent *event)`

**作用与语义：**

此事件处理程序可以在子类中重新实现，以接收项目的鼠标按下事件。事件信息通过 `event` 参数提供。
为了接收鼠标按下事件，`acceptedMouseButtons()` 必须返回相关鼠标按钮。
事件默认被接受，因此如果你重新实现此函数，则不需要显式接受事件。如果你不接受事件，请调用 `event->ignore()`。

### `[virtual protected] void QQuickItem::mouseReleaseEvent(QMouseEvent *event)`

**作用与语义：**

此事件处理程序可以在子类中重新实现，以接收项目的鼠标释放事件。事件信息通过 `event` 参数提供。
为了接收鼠标释放事件，必须接受前一个鼠标按下事件（例如，通过重写 `mousePressEvent()`）并且 `acceptedMouseButtons()` 必须返回相关鼠标按钮。
事件默认被接受，因此如果你重新实现此函数，则不需要显式接受事件。如果你不接受事件，请调用 `event->ignore()`。

### `[virtual protected] void QQuickItem::mouseUngrabEvent()`

**作用与语义：**

该事件处理程序可以重新实现到子类中，当该项发生鼠标取回事件时会收到通知。

### `[invokable] QQuickItem *QQuickItem::nextItemInFocusChain(bool forward = true)`

**作用与语义：**

返回焦点链中紧邻该物品的物品。如果`forward`是`true`或未供应，则是前向方向的下一个物品。如果`forward` `false`，则是向下方向的下一个物品。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `void QQuickItem::polish()`

**作用与语义：**

为这款产品安排了一场波兰活动。
当场景图处理请求时，会调用该项`updatePolish()`。

### `[virtual protected] void QQuickItem::releaseResources()`

**作用与语义：**

当某个项目需要释放尚未由`QQuickItem::updatePaintNode()`返回节点管理的图形资源时，调用该函数。
这发生在该项即将从之前渲染的窗口中移除时。当调用该函数时，该项保证会有`window`。
该函数在图形界面线程中被调用，渲染线程的状态（使用时）未知。对象不应直接删除，而应通过`QQuickWindow::scheduleRenderJob()`调度清理。

### `QQuickItem *QQuickItem::scopedFocusItem() const`

**作用与语义：**

如果该物品是焦点范围，则返回当前焦点链中当前有焦点的物品。
如果这个物品不是焦点瞄准镜，退货`nullptr`。

### `void QQuickItem::setAcceptHoverEvents(bool enabled)`

**作用与语义：**

如果`enabled`为真，则该项目接受悬停事件;否则，该项目不接受悬停事件。

### `void QQuickItem::setAcceptTouchEvents(bool enabled)`

**作用与语义：**

如果`enabled`为真，则该项接受触碰事件;否则，该项不接受触碰事件。

### `void QQuickItem::setAcceptedMouseButtons(Qt::MouseButtons buttons)`

**作用与语义：**

将该物品接受的鼠标按键设置为`buttons`。
注意：在Qt 5中，调用setAcceptedMouseButtons()隐式地导致项目同时接收触摸事件和鼠标事件;但建议调用`setAcceptTouchEvents()`订阅。在Qt 6中，需要调用`setAcceptTouchEvents()`才能继续接收。

### `void QQuickItem::setCursor(const QCursor &cursor)`

**作用与语义：**

为该物品设定`cursor`形状。

### `void QQuickItem::setFiltersChildMouseEvents(bool filter)`

**作用与语义：**

设置是否应过滤该项子节点的指针事件。
如果`filter`为真，当子项触发指针事件时会调用`childMouseEventFilter()`。

### `void QQuickItem::setFlag(QQuickItem::Flag flag, bool enabled = true)`

**作用与语义：**

如果 `enabled`为真，则启用该项指定的 `flag`;如果 `enabled`为假，则该标志被禁用。
这些提示为该物品提供了各种提示;例如，`ItemClipsChildrenToShape`标志表示该物品的所有子节点都应裁剪以符合物品区域。

### `void QQuickItem::setFlags(QQuickItem::Flags flags)`

**作用与语义：**

启用该物品的指定`flags`。

### `void QQuickItem::setFocusPolicy(Qt::FocusPolicy policy)`

**作用与语义：**

该属性决定了物品接受聚焦的方式。

**如何使用：** 调用 `setFocusPolicy(...)` 修改 `focusPolicy`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QQuickItem::setKeepMouseGrab(bool keep)`

**作用与语义：**

设置鼠标输入是否应仅保留在该项上。
这对于希望按照预定义手势抓取并保持鼠标互动的物品非常有用。例如，一个对水平鼠标移动感兴趣的项目，一旦阈值超过阈值，`keepMouseGrab` 可能会被设置为 true。一旦`keepMouseGrab`设置为 true，过滤项目就不会对鼠标事件做出反应。
如果`keep`为假，过滤项目可能会窃取抓取。例如，`Flickable`检测到用户开始移动视口时，可能会尝试偷取鼠标抓取。

### `void QQuickItem::setKeepTouchGrab(bool keep)`

**作用与语义：**

设置该物品所抓取的触点是否应仅保留在此物品上。
这对于希望按照预定义手势抓取并保留特定触点的物品非常有用。例如，一个对水平触摸点移动感兴趣的物品，一旦阈值超过阈值，可以将 setKeepTouchGrab 设置为 true。一旦 setKeepTouchGrab 设置为 true，过滤物品将不会对相关触摸点做出反应。
如果`keep`为假，过滤项目可能会窃取抓取。例如，如果`Flickable`检测到用户开始移动视窗，可能会尝试偷取触摸点抓取。

### `void QQuickItem::setSize(const QSizeF &size)`

**作用与语义：**

将项目大小设置为`size`。该方法保留了宽度和高度上的现有绑定;因此，任何触发绑定再次执行的更改都会覆盖设置值。

### `QSizeF QQuickItem::size() const`

**作用与语义：**

返回物品的尺寸。

### `void QQuickItem::stackAfter(const QQuickItem *sibling)`

**作用与语义：**

将该项移动到子项列表中指定兄弟项之后的索引。子节点的顺序会影响视觉叠加顺序和制表焦点导航顺序。
假设两个项目的z值相同，这会导致`sibling`被渲染到该项目下方。
如果两个项目都`activeFocusOnTab`设置为`true`，这也会导致制表符焦点顺序发生变化，`sibling`先获得焦点。
给定`sibling`必须是该项目的兄弟姐妹;也就是说，它们必须有相同的直接的 `parent`。

### `void QQuickItem::stackBefore(const QQuickItem *sibling)`

**作用与语义：**

将该项移至子项列表中指定兄弟项之前的索引。子项的顺序影响视觉堆叠顺序和制表焦点导航顺序。
假设两个项目的z值相同，这会导致`sibling`渲染在该项目之上。
如果两个项目都`activeFocusOnTab`设为`true`，这也会导致标签的焦点顺序发生变化，`sibling`在该物品之后获得焦点。
给定`sibling`必须是该项目的兄弟姐妹;也就是说，它们必须有相同的直接的 `parent`。

### `[virtual] QSGTextureProvider *QQuickItem::textureProvider() const`

**作用与语义：**

返回某个物品的纹理提供者。默认实现返回`nullptr`。
该函数只能在渲染线程中调用。

### `[virtual protected] void QQuickItem::touchEvent(QTouchEvent *event)`

**作用与语义：**

该事件处理程序可以在子类中重新实现，以接收某项的触摸事件。事件信息由`event`参数提供。
该事件默认被接受，因此如果你重新实现该函数，无需显式接受该事件。如果你不接受该事件，请调用`event->ignore()`。

### `[virtual protected] void QQuickItem::touchUngrabEvent()`

**作用与语义：**

该事件处理程序可以重新实现到子类中，当该项发生触摸取回事件时会收到通知。

### `void QQuickItem::unsetCursor()`

**作用与语义：**

清除此项目的光标形状。

### `[slot] void QQuickItem::update()`

**作用与语义：**

安排了`updatePaintNode()`电话咨询此项。
只要商品显示在`QQuickWindow`中，调用`QQuickItem::updatePaintNode()`总是会发生。
只有指定`QQuickItem::ItemHasContents`的项才允许调用QQuickItem：：update()。

### `[protected] void QQuickItem::updateInputMethod(Qt::InputMethodQueries queries = Qt::ImQueryInput)`

**作用与语义：**

如有需要，通知输入方法更新后的查询值。`queries`表示已更改的属性。

### `[virtual protected] QSGNode *QQuickItem::updatePaintNode(QSGNode *oldNode, QQuickItem::UpdatePaintNodeData *updatePaintNodeData)`

**作用与语义：**

当需要将项的状态与场景图同步时，在渲染线程上调用此函数。 该函数是作为 `QQuickItem::update()` 的结果调用的，如果用户已在该项上设置了 `QQuickItem::ItemHasContents` 标志。 该函数应返回此项的场景图子树的根。大多数实现将返回一个包含此项可视表示的单个 `QSGGeometryNode`。 `oldNode` 是上次调用该函数时返回的节点。 `updatePaintNodeData` 提供指向与此 `QQuickItem` 关联的 `QSGTransformNode` 的指针。 在执行此函数时主线程将被阻塞，因此从 `QQuickItem` 实例和主线程中的其他对象读取值是安全的。 如果没有调用 QQuickItem::updatePaintNode() 导致实际场景图发生变化，例如 `QSGNode::markDirty()` 或添加和删除节点，则底层实现可能决定不再重新渲染场景，因为视觉结果是相同的。 警告：图形操作和与场景图的交互必须专门在渲染线程上进行，主要是在 QQuickItem::updatePaintNode() 调用期间。 经验法则是在 QQuickItem::updatePaintNode() 函数内只使用带有 "QSG" 前缀的类。 警告：此函数在渲染线程上调用。 这意味着任何创建的 QObject 或线程本地存储将与渲染线程关联，因此在此函数中执行渲染以外的操作时要谨慎。 信号也是如此，它们将在渲染线程上发射，因此通常通过排队连接传递。 注意：所有带 QSG 前缀的类应仅在场景图的渲染线程上使用。 更多信息请参见场景图和渲染。

**官方示例：**

```cpp
 QSGNode *MyItem::updatePaintNode(QSGNode *node, UpdatePaintNodeData *)
 {
     QSGSimpleRectNode *n = static_cast<QSGSimpleRectNode *>(node);
     if (!n) {
         n = new QSGSimpleRectNode();
         n->setColor(Qt::red);
     }
     n->setRect(boundingRect());
     return n;
 }
```

### `[virtual protected] void QQuickItem::updatePolish()`

**作用与语义：**

该功能应执行该项目所需的任何布局。
当调用`polish()`时，场景图会为该项目安排一个抛光事件。当场景图准备好渲染该项目时，它调用 updatePolish() 来执行所需的任何项目布局，然后再渲染下一帧。

### `QQuickItem *QQuickItem::viewportItem() const`

**作用与语义：**

如果`ItemObservesViewport`标志被设置，返回最近的父节点，带有`ItemIsViewport`标志。如果标志未被设置，或找不到其他视口项，则返回窗口的contentItem。
只有当没有视口项目且该项目未显示在窗口时，返回`nullptr`。

### `[virtual protected] void QQuickItem::wheelEvent(QWheelEvent *event)`

**作用与语义：**

该事件处理程序可以在子类中重新实现，以接收某个项目的轮事件。事件信息由 `event` 参数提供。
该事件默认被接受，因此如果你重新实现该函数，无需显式接受该事件。如果你不接受该事件，就调用`event->ignore()`。

### `[protected] bool QQuickItem::widthValid() const`

**作用与语义：**

返回宽度属性是否被明确设置。

### `QQuickWindow *QQuickItem::window() const`

**作用与语义：**

返回该物品渲染的窗口。
物品在被分配到场景中之前没有窗口。`windowChanged()`信号在物品进入场景和从场景中移除时都会提供通知。

### `[signal] void QQuickItem::windowChanged(QQuickWindow *window)`

**作用与语义：**

当物品的 `window` 变化时，会发出该信号。

### `enum Flag { ItemClipsChildrenToShape, ItemAcceptsInputMethod, ItemIsFocusScope, ItemHasContents, ItemAcceptsDrops, …, ItemObservesViewport }`

**作用与语义：**

该枚举类型用于指定各种项目属性。
- `QQuickItem::ItemClipsChildrenToShape`：`0x01`;表示该项目应视觉上裁剪其子节点，使其仅在本项目边界内渲染。
- `QQuickItem::ItemAcceptsInputMethod`：`0x02`;表示该项目支持文本输入法。
- `QQuickItem::ItemIsFocusScope`：`0x04`;表示该物品是对焦示波器。更多信息请参见Qt Quick中的键盘聚焦。
- `QQuickItem::ItemHasContents`：`0x08`;表示该物品具有视觉内容，应由场景图渲染。
- `QQuickItem::ItemAcceptsDrops`：`0x10`;表示该物品接受拖放事件。
- `QQuickItem::ItemIsViewport`：`0x20`;表示该项为其子节点定义了一个视口。
- `QQuickItem::ItemObservesViewport`：`0x40`;表示当任何祖先设置了ItemIsViewport标志时，该项希望知道视口边界。
Flags 类型是 QFlags 的 typedef<Flag>。它存储 Flag 值的 OR 组合。

### `flags Flags`

**作用与语义：**

该枚举类型用于指定各种项目属性。
- `QQuickItem::ItemClipsChildrenToShape`：`0x01`;表示该项目应视觉上裁剪其子节点，使其仅在本项目边界内渲染。
- `QQuickItem::ItemAcceptsInputMethod`：`0x02`;表示该项目支持文本输入法。
- `QQuickItem::ItemIsFocusScope`：`0x04`;表示该物品是对焦示波器。更多信息请参见Qt Quick中的键盘聚焦。
- `QQuickItem::ItemHasContents`：`0x08`;表示该物品具有视觉内容，应由场景图渲染。
- `QQuickItem::ItemAcceptsDrops`：`0x10`;表示该物品接受拖放事件。
- `QQuickItem::ItemIsViewport`：`0x20`;表示该项为其子节点定义了一个视口。
- `QQuickItem::ItemObservesViewport`：`0x40`;表示当任何祖先设置了ItemIsViewport标志时，该项希望知道视口边界。
Flags 类型是 QFlags 的 typedef<Flag>。它存储 Flag 值的 OR 组合。

### `implicitHeight : qreal`

**作用与语义：**

定义物品的首选宽度或高度。
如果未指定`width`或`height`，则物品的有效尺寸将由其`implicitWidth`或`implicitHeight`确定。
然而，如果某个项目是布局的子节点，布局会通过其隐式大小决定该项目的首选大小。在这种情况下，显式的`width`或`height`将被忽略。
大多数项目默认隐式大小为0x0，但某些项固有隐式大小无法覆盖，例如`Image`和`Text`。
设置隐式大小对于定义基于内容具有优先大小的组件非常有用，例如：
注意：使用`Text`或`TextEdit` `implicitWidth`并明确设置宽度会带来性能惩罚，因为文本必须排版两次。

**如何使用：** 调用 `implicitHeight()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 // Label.qml
 import QtQuick 2.0

 Item {
     property alias icon: image.source
     property alias label: text.text
     implicitWidth: text.implicitWidth + image.implicitWidth
     implicitHeight: Math.max(text.implicitHeight, image.implicitHeight)
     Image { id: image }
     Text {
         id: text
         wrapMode: Text.Wrap
         anchors.left: image.right; anchors.right: parent.right
         anchors.verticalCenter: parent.verticalCenter
     }
 }
```

### `bool activeFocusOnTab() const`

**作用与语义：**

该属性决定项是否希望处于标签焦点链中。默认情况下，该项设置为`false`。
注意：`tabFocusBehavior`还可以进一步限制只关注特定类型的控件，比如仅限文本或列表控件。macOS 上就是这样，根据系统设置，可能会限制对特定控件的关注。

**如何使用：** 调用 `activeFocusOnTab()` 读取当前值；它不会修改应用状态。

### `bool antialiasing() const`

**作用与语义：**

指定该项目是否进行了抗锯齿处理。
视觉元素用于决定物品是否应使用抗锯齿。在某些情况下，带有抗锯齿的物品需要更多内存，渲染速度也可能更慢（详见抗锯齿部分）。
默认为假，但可被派生元素覆盖。

**如何使用：** 调用 `antialiasing()` 读取当前值；它不会修改应用状态。

### `qreal baselineOffset() const`

**作用与语义：**

指定该物品基线在本地坐标中的位置。
`Text`项的基线是文本所处的虚数线。包含文本的控件通常将其基线设置为文本的基线。
对于非文本项目，默认基线偏移量为0。

**如何使用：** 调用 `baselineOffset()` 读取当前值；它不会修改应用状态。

### `QBindable<qreal> bindableHeight()`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该地块能承受该物品的高度。

**如何使用：** 调用 `bindableHeight()` 取得 `height` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `QBindable<qreal> bindableWidth()`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性表示该项的宽度。

**如何使用：** 调用 `bindableWidth()` 取得 `width` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `QBindable<qreal> bindableX()`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
定义该项相对于其父节点的x位置。

**如何使用：** 调用 `bindableX()` 取得 `x` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `QBindable<qreal> bindableY()`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
定义了该物品相对于父节点的 y 位置。

**如何使用：** 调用 `bindableY()` 取得 `y` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `QRectF childrenRect()`

**作用与语义：**

该属性包含该物品子的集体位置和大小。
如果你需要访问某个物品子节点的集体几何体以正确调整该项目的大小，这个属性非常有用。
返回的几何体是该项目的局部。例如：

**如何使用：** 调用 `childrenRect()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 Item {
     x: 50
     y: 100

     // prints: QRectF(-10, -20, 30, 40)
     Component.onCompleted: print(childrenRect)

     Item {
         x: -10
         y: -20
         width: 30
         height: 40
     }
 }
```

### `bool clip() const`

**作用与语义：**

该属性适用于是否启用裁剪。默认裁剪值为 `false`。
如果启用裁剪，项将裁剪自身绘制内容以及其子项的绘制内容到其边界矩形。如果在项的绘制操作中设置了裁剪，请记得重新设置，以防裁剪场景的其他部分。
注意：裁剪可能影响渲染性能。有关更多信息，请参见裁剪。
注意：为了 QML，如果将 clip 设置为 `true`，也会设置 `ItemIsViewport` 标志，这有时作为一种优化：具有 `ItemObservesViewport` 标志的子项可以省略创建视口外的场景图节点。但 `ItemIsViewport` 标志也可以独立设置。

**如何使用：** 调用 `clip()` 读取当前值；它不会修改应用状态。

### `QObject * containmentMask() const`

**作用与语义：**

该属性包含一个可选遮罩，用于`contains()`方法，主要用于每个`QPointerEvent`的命中测试。
默认情况下，`contains()` 会返回物品边界框内任意点的 `true`。但任何实现函数 的`QQuickItem`或任何实现 函数的`QObject`。
可以用作掩体，将测试推迟到该对象。
注意：`contains()` 在事件传递过程中经常被调用。将击中测试推迟到另一个对象会在一定程度上减慢速度。如果该对象的 `contains()` 方法效率不高，containmentMask() 可能会引发性能问题。如果你实现了自定义的 `QQuickItem` 子类，也可以选择覆盖`contains()`。

**如何使用：** 调用 `containmentMask()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 Q_INVOKABLE bool contains(const QPointF &point) const;
```

### `Qt::FocusPolicy focusPolicy() const`

**作用与语义：**

该属性决定了物品接受聚焦的方式。

**如何使用：** 调用 `focusPolicy()` 读取当前值；它不会修改应用状态。

### `bool hasActiveFocus() const`

**作用与语义：**

该只读特性表示该项是否具有主动焦点。
如果 activeFocus 为真，则该项要么是当前接收键盘输入的项，要么是当前接收键盘输入项的`FocusScope`祖先。
通常，activeFocus 通过在物品及其包围的`FocusScope`对象上设置 `focus` 来实现。在以下示例中，`input` 和 `focusScope` 对象将有主动焦点，而根矩形对象则没有。

**如何使用：** 调用 `hasActiveFocus()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 import QtQuick 2.0

 Rectangle {
     width: 100; height: 100

     FocusScope {
         focus: true

         TextInput {
             id: input
             focus: true
         }
     }
 }
```

### `bool hasFocus() const`

**作用与语义：**

该特性成立，是否该物品在包围`FocusScope`内具有焦点。如果成立，当包围`FocusScope`获得主动焦点时，该物品将获得主动焦点。
在以下例子中，当`input` `scope`获得主动聚焦时，将获得主动专注：
在此属性中，整个场景被假定为聚焦示波器。在实际操作层面，这意味着后续的量子大力学将在启动时给予`input`主动聚焦。

**如何使用：** 调用 `hasFocus()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 import QtQuick 2.0

 Rectangle {
     width: 100; height: 100

     FocusScope {
         id: scope

         TextInput {
             id: input
             focus: true
         }
     }
 }
```

### `qreal height() const`

**作用与语义：**

该属性包含该物品子的集体位置和大小。
如果你需要访问某个物品子节点的集体几何体以正确调整该项目的大小，这个属性非常有用。
返回的几何体是该项目的局部。例如：

**如何使用：** 调用 `height()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 Item {
     x: 50
     y: 100

     // prints: QRectF(-10, -20, 30, 40)
     Component.onCompleted: print(childrenRect)

     Item {
         x: -10
         y: -20
         width: 30
         height: 40
     }
 }
```

### `qreal implicitHeight() const`

**作用与语义：**

定义物品的首选宽度或高度。
如果未指定`width`或`height`，则物品的有效尺寸将由其`implicitWidth`或`implicitHeight`确定。
然而，如果某个项目是布局的子节点，布局会通过其隐式大小决定该项目的首选大小。在这种情况下，显式的`width`或`height`将被忽略。
大多数项目默认隐式大小为0x0，但某些项固有隐式大小无法覆盖，例如`Image`和`Text`。
设置隐式大小对于定义基于内容具有优先大小的组件非常有用，例如：
注意：使用`Text`或`TextEdit` `implicitWidth`并明确设置宽度会带来性能惩罚，因为文本必须排版两次。

**如何使用：** 调用 `implicitHeight()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 // Label.qml
 import QtQuick 2.0

 Item {
     property alias icon: image.source
     property alias label: text.text
     implicitWidth: text.implicitWidth + image.implicitWidth
     implicitHeight: Math.max(text.implicitHeight, image.implicitHeight)
     Image { id: image }
     Text {
         id: text
         wrapMode: Text.Wrap
         anchors.left: image.right; anchors.right: parent.right
         anchors.verticalCenter: parent.verticalCenter
     }
 }
```

### `bool isEnabled() const`

**作用与语义：**

该属性决定项目是否接收鼠标和键盘事件。默认情况下，这为真。
设置该属性直接影响子项的`enabled`值。当设置为`false`时，所有子项的`enabled`值也会变为`false`。当设置为`true`时，子项的`enabled`值会返回`true`，除非它们被明确设置为`false`。
将该属性设置为`false`会自动使`activeFocus`被设置为`false`，该项将不再接收键盘事件。
注意：悬停事件由`setAcceptHoverEvents()`单独启用。因此，禁用的物品即使该属性被`false`，仍可继续接收悬停事件。这使得即使关闭交互项，仍能显示信息反馈（如`ToolTip`）。任何作为物品子节点添加的`HoverHandlers`同样适用。然而，`HoverHandler`可以显式`disabled`，或者例如绑定到物品的 `enabled` 状态。

**如何使用：** 调用 `isEnabled()` 读取当前值；它不会修改应用状态。

### `bool isVisible() const`

**作用与语义：**

该属性在物品可见时成立。默认情况下，这点成立。
设置该属性直接影响子项的`visible`值。当设置为`false`时，所有子项的`visible`值也会变为`false`。当设置为`true`时，子项的`visible`值会返回`true`，除非它们明确设置为`false`。
（由于这种连贯行为，如果属性绑定只对显式属性变化做出响应，使用`visible`属性可能无法达到预期效果。在这种情况下，使用`opacity`属性可能更好。）。
如果该属性设置为`false`，物品将不再接收鼠标事件，但会继续接收按键事件，并且如果已设置，键盘`focus`会保留。（相反，将`enabled`属性设置为`false`会停止鼠标和键盘事件，同时移除对物品的关注。）。
注意：该属性的价值仅会因该属性或父`visible`属性的变化而受到影响。例如，如果该物品移出屏幕，或者`opacity`变为0，属性不会改变。但出于历史原因，该属性在物品构建后依然成立，即使该物品尚未添加到场景中。更改或读取尚未添加到场景中的物品的属性可能无法达到预期效果。
注意：该属性的通知信号在视觉父节点销毁时发出。C 信号处理者不能假设视觉父层级中的项目仍然完整构建。使用`qobject_cast`验证父层级中的项目是否可以安全地作为预期类型使用。

**如何使用：** 调用 `isVisible()` 读取当前值；它不会修改应用状态。

### `qreal opacity() const`

**作用与语义：**

该属性包含该项的不透明度。不透明度指定为0.0（完全透明）到1.0（完全不透明）之间的数值。默认值为1.0。
当该属性被设置时，指定的不透明度也会单独应用到子项上。在某些情况下，这可能会产生意想不到的影响。例如，在下面的第二组矩形中，红色矩形指定了0.5的不透明度，这影响了其蓝色子矩形的不透明度，尽管该子矩形并未指定不透明度。
0到1范围之外的数值会被夹紧。
- '`: `Item' {
`Rectangle` {。
颜色：“红色”。
宽度：100;高度：100。
`Rectangle` {。
颜色：“蓝色”。
x：50;y：50;宽度：100;高度：100。
}。
}。
}。
- '`: `Item' {
`Rectangle` {。
不透明度：0.5。
颜色：“红色”。
宽度：100;高度：100。
`Rectangle` {。
颜色：“蓝色”。
x：50;y：50;宽度：100;高度：100。
}。
}。
}。
更改物品的透明度不会影响该物品是否接收用户输入事件。（相比之下，将`visible`属性设置为`false`会停止鼠标事件，将`enabled`属性设置为`false`则停止鼠标和键盘事件，同时移除对该物品的主动关注。）。

**如何使用：** 调用 `opacity()` 读取当前值；它不会修改应用状态。

### `QQuickItem * parentItem() const`

**作用与语义：**

该属性包含该项的视觉父。
注意：视觉父的概念与`QObject`父的概念不同。一个项目的视觉父节点不一定与其对象父节点相同。更多详情请参见Qt Quick中的概念 - 视觉父。
注意：该属性的通知信号在视觉父节点销毁时发出。C 信号处理者不能假设视觉父层级中的项目仍然完整构建。使用`qobject_cast`验证父层级中的项目是否可以安全地作为预期类型使用。

**如何使用：** 调用 `parentItem()` 读取当前值；它不会修改应用状态。

### `void resetAntialiasing()`

**作用与语义：**

指定该项目是否进行了抗锯齿处理。
视觉元素用于决定物品是否应使用抗锯齿。在某些情况下，带有抗锯齿的物品需要更多内存，渲染速度也可能更慢（详见抗锯齿部分）。
默认为假，但可被派生元素覆盖。

**如何使用：** 调用 `resetAntialiasing()` 撤销对 `antialiasing` 的显式覆盖，让它重新采用继承值或默认值。

### `void resetHeight()`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该地块能承受该物品的高度。

**如何使用：** 调用 `resetHeight()` 撤销对 `height` 的显式覆盖，让它重新采用继承值或默认值。

### `void resetWidth()`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性表示该项的宽度。

**如何使用：** 调用 `resetWidth()` 撤销对 `width` 的显式覆盖，让它重新采用继承值或默认值。

### `qreal rotation() const`

**作用与语义：**

该属性表示物品围绕其`transformOrigin`顺时针旋转的度数。
默认值为0度（即不旋转）。
- '`: `Rectangle' {
颜色：“蓝色”。
宽度：100;高度：100。
`Rectangle` {。
颜色：“红色”。
x：25;y：25;宽度：50;高度：50。
轮换：30。
}。
}。

**如何使用：** 调用 `rotation()` 读取当前值；它不会修改应用状态。

### `qreal scale() const`

**作用与语义：**

该属性表示该项的比例因子。
比例小于1.0时，物品的渲染尺寸变小;比例大于1.0时，物品的尺寸会变大。负比例则表示物品在渲染时被镜像化。
默认值是1.0。
缩放是从`transformOrigin`开始的。
- ''： import QtQuick 2.0

`Rectangle` {。
颜色：“蓝色”。
宽度：100;高度：100。

`Rectangle` {。
颜色：“绿色”。
宽度：25;高度：25。
}。

`Rectangle` {。
颜色：“红色”。
x：25;y：25;宽度：50;高度：50。
比例：1.4。
}。
}。

**如何使用：** 调用 `scale()` 读取当前值；它不会修改应用状态。

### `void setActiveFocusOnTab(bool)`

**作用与语义：**

该属性决定项是否希望处于标签焦点链中。默认情况下，该项设置为`false`。
注意：`tabFocusBehavior`还可以进一步限制只关注特定类型的控件，比如仅限文本或列表控件。macOS 上就是这样，根据系统设置，可能会限制对特定控件的关注。

**如何使用：** 调用 `setActiveFocusOnTab(...)` 修改 `activeFocusOnTab`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setAntialiasing(bool)`

**作用与语义：**

指定该项目是否进行了抗锯齿处理。
视觉元素用于决定物品是否应使用抗锯齿。在某些情况下，带有抗锯齿的物品需要更多内存，渲染速度也可能更慢（详见抗锯齿部分）。
默认为假，但可被派生元素覆盖。

**如何使用：** 调用 `setAntialiasing(...)` 修改 `antialiasing`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setBaselineOffset(qreal)`

**作用与语义：**

指定该物品基线在本地坐标中的位置。
`Text`项的基线是文本所处的虚数线。包含文本的控件通常将其基线设置为文本的基线。
对于非文本项目，默认基线偏移量为0。

**如何使用：** 调用 `setBaselineOffset(...)` 修改 `baselineOffset`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setClip(bool)`

**作用与语义：**

该属性适用于是否启用裁剪。默认裁剪值为 `false`。
如果启用裁剪，项将裁剪自身绘制内容以及其子项的绘制内容到其边界矩形。如果在项的绘制操作中设置了裁剪，请记得重新设置，以防裁剪场景的其他部分。
注意：裁剪可能影响渲染性能。有关更多信息，请参见裁剪。
注意：为了 QML，如果将 clip 设置为 `true`，也会设置 `ItemIsViewport` 标志，这有时作为一种优化：具有 `ItemObservesViewport` 标志的子项可以省略创建视口外的场景图节点。但 `ItemIsViewport` 标志也可以独立设置。

**如何使用：** 调用 `setClip(...)` 修改 `clip`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setContainmentMask(QObject *mask)`

**作用与语义：**

该属性包含一个可选遮罩，用于`contains()`方法，主要用于每个`QPointerEvent`的命中测试。
默认情况下，`contains()` 会返回物品边界框内任意点的 `true`。但任何实现函数 的`QQuickItem`或任何实现 函数的`QObject`。
可以用作掩体，将测试推迟到该对象。
注意：`contains()` 在事件传递过程中经常被调用。将击中测试推迟到另一个对象会在一定程度上减慢速度。如果该对象的 `contains()` 方法效率不高，containmentMask() 可能会引发性能问题。如果你实现了自定义的 `QQuickItem` 子类，也可以选择覆盖`contains()`。

**如何使用：** 调用 `setContainmentMask(...)` 修改 `containmentMask`；传入的新值会成为后续查询和相关界面行为所使用的值。

**官方示例：**

```cpp
 Q_INVOKABLE bool contains(const QPointF &point) const;
```

### `void setEnabled(bool)`

**作用与语义：**

该属性决定项目是否接收鼠标和键盘事件。默认情况下，这为真。
设置该属性直接影响子项的`enabled`值。当设置为`false`时，所有子项的`enabled`值也会变为`false`。当设置为`true`时，子项的`enabled`值会返回`true`，除非它们被明确设置为`false`。
将该属性设置为`false`会自动使`activeFocus`被设置为`false`，该项将不再接收键盘事件。
注意：悬停事件由`setAcceptHoverEvents()`单独启用。因此，禁用的物品即使该属性被`false`，仍可继续接收悬停事件。这使得即使关闭交互项，仍能显示信息反馈（如`ToolTip`）。任何作为物品子节点添加的`HoverHandlers`同样适用。然而，`HoverHandler`可以显式`disabled`，或者例如绑定到物品的 `enabled` 状态。

**如何使用：** 调用 `setEnabled(...)` 修改 `enabled`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setFocus(bool)`

**作用与语义：**

该特性成立，是否该物品在包围`FocusScope`内具有焦点。如果成立，当包围`FocusScope`获得主动焦点时，该物品将获得主动焦点。
在以下例子中，当`input` `scope`获得主动聚焦时，将获得主动专注：
在此属性中，整个场景被假定为聚焦示波器。在实际操作层面，这意味着后续的量子大力学将在启动时给予`input`主动聚焦。

**如何使用：** 调用 `setFocus(...)` 修改 `focus`；传入的新值会成为后续查询和相关界面行为所使用的值。

**官方示例：**

```cpp
 import QtQuick 2.0

 Rectangle {
     width: 100; height: 100

     FocusScope {
         id: scope

         TextInput {
             id: input
             focus: true
         }
     }
 }
```

### `void setFocus(bool focus, Qt::FocusReason reason)`

**作用与语义：**

该特性成立，是否该物品在包围`FocusScope`内具有焦点。如果成立，当包围`FocusScope`获得主动焦点时，该物品将获得主动焦点。
在以下例子中，当`input` `scope`获得主动聚焦时，将获得主动专注：
在此属性中，整个场景被假定为聚焦示波器。在实际操作层面，这意味着后续的量子大力学将在启动时给予`input`主动聚焦。

**如何使用：** 调用 `setFocus(...)` 修改 `focus`；传入的新值会成为后续查询和相关界面行为所使用的值。

**官方示例：**

```cpp
 import QtQuick 2.0

 Rectangle {
     width: 100; height: 100

     FocusScope {
         id: scope

         TextInput {
             id: input
             focus: true
         }
     }
 }
```

### `void setHeight(qreal)`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该地块能承受该物品的高度。

**如何使用：** 调用 `setHeight(...)` 修改 `height`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setImplicitHeight(qreal)`

**作用与语义：**

定义物品的首选宽度或高度。
如果未指定`width`或`height`，则物品的有效尺寸将由其`implicitWidth`或`implicitHeight`确定。
然而，如果某个项目是布局的子节点，布局会通过其隐式大小决定该项目的首选大小。在这种情况下，显式的`width`或`height`将被忽略。
大多数项目默认隐式大小为0x0，但某些项固有隐式大小无法覆盖，例如`Image`和`Text`。
设置隐式大小对于定义基于内容具有优先大小的组件非常有用，例如：
注意：使用`Text`或`TextEdit` `implicitWidth`并明确设置宽度会带来性能惩罚，因为文本必须排版两次。

**如何使用：** 调用 `setImplicitHeight(...)` 修改 `implicitHeight`；传入的新值会成为后续查询和相关界面行为所使用的值。

**官方示例：**

```cpp
 // Label.qml
 import QtQuick 2.0

 Item {
     property alias icon: image.source
     property alias label: text.text
     implicitWidth: text.implicitWidth + image.implicitWidth
     implicitHeight: Math.max(text.implicitHeight, image.implicitHeight)
     Image { id: image }
     Text {
         id: text
         wrapMode: Text.Wrap
         anchors.left: image.right; anchors.right: parent.right
         anchors.verticalCenter: parent.verticalCenter
     }
 }
```

### `void setImplicitWidth(qreal)`

**作用与语义：**

定义物品的首选宽度或高度。
如果未指定`width`或`height`，则物品的有效尺寸将由其`implicitWidth`或`implicitHeight`确定。
然而，如果某个项目是布局的子节点，布局会通过其隐式大小决定该项目的首选大小。在这种情况下，显式的`width`或`height`将被忽略。
大多数项目默认隐式大小为0x0，但某些项固有隐式大小无法覆盖，例如`Image`和`Text`。
设置隐式大小对于定义基于内容具有优先大小的组件非常有用，例如：
注意：使用`Text`或`TextEdit` `implicitWidth`并明确设置宽度会带来性能惩罚，因为文本必须排版两次。

**如何使用：** 调用 `setImplicitWidth(...)` 修改 `implicitWidth`；传入的新值会成为后续查询和相关界面行为所使用的值。

**官方示例：**

```cpp
 // Label.qml
 import QtQuick 2.0

 Item {
     property alias icon: image.source
     property alias label: text.text
     implicitWidth: text.implicitWidth + image.implicitWidth
     implicitHeight: Math.max(text.implicitHeight, image.implicitHeight)
     Image { id: image }
     Text {
         id: text
         wrapMode: Text.Wrap
         anchors.left: image.right; anchors.right: parent.right
         anchors.verticalCenter: parent.verticalCenter
     }
 }
```

### `void setOpacity(qreal)`

**作用与语义：**

该属性包含该项的不透明度。不透明度指定为0.0（完全透明）到1.0（完全不透明）之间的数值。默认值为1.0。
当该属性被设置时，指定的不透明度也会单独应用到子项上。在某些情况下，这可能会产生意想不到的影响。例如，在下面的第二组矩形中，红色矩形指定了0.5的不透明度，这影响了其蓝色子矩形的不透明度，尽管该子矩形并未指定不透明度。
0到1范围之外的数值会被夹紧。
- '`: `Item' {
`Rectangle` {。
颜色：“红色”。
宽度：100;高度：100。
`Rectangle` {。
颜色：“蓝色”。
x：50;y：50;宽度：100;高度：100。
}。
}。
}。
- '`: `Item' {
`Rectangle` {。
不透明度：0.5。
颜色：“红色”。
宽度：100;高度：100。
`Rectangle` {。
颜色：“蓝色”。
x：50;y：50;宽度：100;高度：100。
}。
}。
}。
更改物品的透明度不会影响该物品是否接收用户输入事件。（相比之下，将`visible`属性设置为`false`会停止鼠标事件，将`enabled`属性设置为`false`则停止鼠标和键盘事件，同时移除对该物品的主动关注。）。

**如何使用：** 调用 `setOpacity(...)` 修改 `opacity`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setParentItem(QQuickItem *parent)`

**作用与语义：**

该属性包含该项的视觉父。
注意：视觉父的概念与`QObject`父的概念不同。一个项目的视觉父节点不一定与其对象父节点相同。更多详情请参见Qt Quick中的概念 - 视觉父。
注意：该属性的通知信号在视觉父节点销毁时发出。C 信号处理者不能假设视觉父层级中的项目仍然完整构建。使用`qobject_cast`验证父层级中的项目是否可以安全地作为预期类型使用。

**如何使用：** 调用 `setParentItem(...)` 修改 `parent`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setRotation(qreal)`

**作用与语义：**

该属性表示物品围绕其`transformOrigin`顺时针旋转的度数。
默认值为0度（即不旋转）。
- '`: `Rectangle' {
颜色：“蓝色”。
宽度：100;高度：100。
`Rectangle` {。
颜色：“红色”。
x：25;y：25;宽度：50;高度：50。
轮换：30。
}。
}。

**如何使用：** 调用 `setRotation(...)` 修改 `rotation`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setScale(qreal)`

**作用与语义：**

该属性表示该项的比例因子。
比例小于1.0时，物品的渲染尺寸变小;比例大于1.0时，物品的尺寸会变大。负比例则表示物品在渲染时被镜像化。
默认值是1.0。
缩放是从`transformOrigin`开始的。
- ''： import QtQuick 2.0

`Rectangle` {。
颜色：“蓝色”。
宽度：100;高度：100。

`Rectangle` {。
颜色：“绿色”。
宽度：25;高度：25。
}。

`Rectangle` {。
颜色：“红色”。
x：25;y：25;宽度：50;高度：50。
比例：1.4。
}。
}。

**如何使用：** 调用 `setScale(...)` 修改 `scale`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setSmooth(bool)`

**作用与语义：**

指定该项目是否被平滑处理。
主要用于基于图像的项目，以决定该项目是否应使用平滑采样。平滑采样通过线性插值实现，而非平滑采样则使用最近邻进行。
在 Qt Quick 2.0 中，这一特性对性能的影响很小。
默认情况下，该属性被设置为`true`。

**如何使用：** 调用 `setSmooth(...)` 修改 `smooth`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setState(const QString &)`

**作用与语义：**

该属性保存项目当前状态的名称。
如果项目处于默认状态，即未设置任何显式状态，则该属性保存为空字符串。同样，可以通过将此属性设置为空字符串将项目恢复到默认状态。

**如何使用：** 调用 `setState(...)` 修改 `state`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTransformOrigin(QQuickItem::TransformOrigin)`

**作用与语义：**

此属性保存缩放和旋转变换的原点。
提供九个变换原点，如下图所示。默认的变换原点是 `Item.Center`。

**如何使用：** 调用 `setTransformOrigin(...)` 修改 `transformOrigin`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setVisible(bool)`

**作用与语义：**

该属性在物品可见时成立。默认情况下，这点成立。
设置该属性直接影响子项的`visible`值。当设置为`false`时，所有子项的`visible`值也会变为`false`。当设置为`true`时，子项的`visible`值会返回`true`，除非它们明确设置为`false`。
（由于这种连贯行为，如果属性绑定只对显式属性变化做出响应，使用`visible`属性可能无法达到预期效果。在这种情况下，使用`opacity`属性可能更好。）。
如果该属性设置为`false`，物品将不再接收鼠标事件，但会继续接收按键事件，并且如果已设置，键盘`focus`会保留。（相反，将`enabled`属性设置为`false`会停止鼠标和键盘事件，同时移除对物品的关注。）。
注意：该属性的价值仅会因该属性或父`visible`属性的变化而受到影响。例如，如果该物品移出屏幕，或者`opacity`变为0，属性不会改变。但出于历史原因，该属性在物品构建后依然成立，即使该物品尚未添加到场景中。更改或读取尚未添加到场景中的物品的属性可能无法达到预期效果。
注意：该属性的通知信号在视觉父节点销毁时发出。C 信号处理者不能假设视觉父层级中的项目仍然完整构建。使用`qobject_cast`验证父层级中的项目是否可以安全地作为预期类型使用。

**如何使用：** 调用 `setVisible(...)` 修改 `visible`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setWidth(qreal)`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性表示该项的宽度。

**如何使用：** 调用 `setWidth(...)` 修改 `width`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setX(qreal)`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
定义该项相对于其父节点的x位置。

**如何使用：** 调用 `setX(...)` 修改 `x`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setY(qreal)`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
定义了该物品相对于父节点的 y 位置。

**如何使用：** 调用 `setY(...)` 修改 `y`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setZ(qreal)`

**作用与语义：**

设置兄弟项目的叠加顺序。默认堆叠顺序为0。
叠加值较高的物品会被绘制在叠加顺序较低的兄弟姐妹上。叠加值相同的物品按出现顺序从下而上绘制。叠加值为负的物品则会被绘制在其父内容下方。
以下示例展示了堆叠顺序的各种影响。
- '`: Same `z' - 较早子节点之上后期子节点：
`Item` {。
`Rectangle` {。
颜色：“红色”。
宽度：100;高度：100。
}。
`Rectangle` {。
颜色：“蓝色”。
x：50;y：50;宽度：100;高度：100。
}。
}。
- 顶部的“`: Higher `z”：
`Item` {。
`Rectangle` {。
Z：1。
颜色：“红色”。
宽度：100;高度：100。
}。
`Rectangle` {。
颜色：“蓝色”。
x：50;y：50;宽度：100;高度：100。
}。
}。
- '`: Same `z' - 父之上的子节点：
`Item` {。
`Rectangle` {。
颜色：“红色”。
宽度：100;高度：100。
`Rectangle` {。
颜色：“蓝色”。
x：50;y：50;宽度：100;高度：100。
}。
}。
}。
- “`: Lower `z”如下：
`Item` {。
`Rectangle` {。
颜色：“红色”。
宽度：100;高度：100。
`Rectangle` {。
Z：-1。
颜色：“蓝色”。
x：50;y：50;宽度：100;高度：100。
}。
}。
}。

**如何使用：** 调用 `setZ(...)` 修改 `z`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `bool smooth() const`

**作用与语义：**

指定该项目是否被平滑处理。
主要用于基于图像的项目，以决定该项目是否应使用平滑采样。平滑采样通过线性插值实现，而非平滑采样则使用最近邻进行。
在 Qt Quick 2.0 中，这一特性对性能的影响很小。
默认情况下，该属性被设置为`true`。

**如何使用：** 调用 `smooth()` 读取当前值；它不会修改应用状态。

### `QString state() const`

**作用与语义：**

该属性保存项目当前状态的名称。
如果项目处于默认状态，即未设置任何显式状态，则该属性保存为空字符串。同样，可以通过将此属性设置为空字符串将项目恢复到默认状态。

**如何使用：** 调用 `state()` 读取当前值；它不会修改应用状态。

### `QQuickItem::TransformOrigin transformOrigin() const`

**作用与语义：**

此属性保存缩放和旋转变换的原点。
提供九个变换原点，如下图所示。默认的变换原点是 `Item.Center`。

**如何使用：** 调用 `transformOrigin()` 读取当前值；它不会修改应用状态。

### `qreal width() const`

**作用与语义：**

该属性包含该物品子的集体位置和大小。
如果你需要访问某个物品子节点的集体几何体以正确调整该项目的大小，这个属性非常有用。
返回的几何体是该项目的局部。例如：

**如何使用：** 调用 `width()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 Item {
     x: 50
     y: 100

     // prints: QRectF(-10, -20, 30, 40)
     Component.onCompleted: print(childrenRect)

     Item {
         x: -10
         y: -20
         width: 30
         height: 40
     }
 }
```

### `qreal x() const`

**作用与语义：**

该属性包含该物品子的集体位置和大小。
如果你需要访问某个物品子节点的集体几何体以正确调整该项目的大小，这个属性非常有用。
返回的几何体是该项目的局部。例如：

**如何使用：** 调用 `x()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 Item {
     x: 50
     y: 100

     // prints: QRectF(-10, -20, 30, 40)
     Component.onCompleted: print(childrenRect)

     Item {
         x: -10
         y: -20
         width: 30
         height: 40
     }
 }
```

### `qreal y() const`

**作用与语义：**

该属性包含该物品子的集体位置和大小。
如果你需要访问某个物品子节点的集体几何体以正确调整该项目的大小，这个属性非常有用。
返回的几何体是该项目的局部。例如：

**如何使用：** 调用 `y()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 Item {
     x: 50
     y: 100

     // prints: QRectF(-10, -20, 30, 40)
     Component.onCompleted: print(childrenRect)

     Item {
         x: -10
         y: -20
         width: 30
         height: 40
     }
 }
```

### `qreal z() const`

**作用与语义：**

设置兄弟项目的叠加顺序。默认堆叠顺序为0。
叠加值较高的物品会被绘制在叠加顺序较低的兄弟姐妹上。叠加值相同的物品按出现顺序从下而上绘制。叠加值为负的物品则会被绘制在其父内容下方。
以下示例展示了堆叠顺序的各种影响。
- '`: Same `z' - 较早子节点之上后期子节点：
`Item` {。
`Rectangle` {。
颜色：“红色”。
宽度：100;高度：100。
}。
`Rectangle` {。
颜色：“蓝色”。
x：50;y：50;宽度：100;高度：100。
}。
}。
- 顶部的“`: Higher `z”：
`Item` {。
`Rectangle` {。
Z：1。
颜色：“红色”。
宽度：100;高度：100。
}。
`Rectangle` {。
颜色：“蓝色”。
x：50;y：50;宽度：100;高度：100。
}。
}。
- '`: Same `z' - 父之上的子节点：
`Item` {。
`Rectangle` {。
颜色：“红色”。
宽度：100;高度：100。
`Rectangle` {。
颜色：“蓝色”。
x：50;y：50;宽度：100;高度：100。
}。
}。
}。
- “`: Lower `z”如下：
`Item` {。
`Rectangle` {。
颜色：“红色”。
宽度：100;高度：100。
`Rectangle` {。
Z：-1。
颜色：“蓝色”。
x：50;y：50;宽度：100;高度：100。
}。
}。
}。

**如何使用：** 调用 `z()` 读取当前值；它不会修改应用状态。

### `void activeFocusChanged(bool)`

**作用与语义：**

该只读特性表示该项是否具有主动焦点。
如果 activeFocus 为真，则该项要么是当前接收键盘输入的项，要么是当前接收键盘输入项的`FocusScope`祖先。
通常，activeFocus 通过在物品及其包围的`FocusScope`对象上设置 `focus` 来实现。在以下示例中，`input` 和 `focusScope` 对象将有主动焦点，而根矩形对象则没有。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `activeFocus` 的变化，不要把它当作普通函数主动调用。

**官方示例：**

```cpp
 import QtQuick 2.0

 Rectangle {
     width: 100; height: 100

     FocusScope {
         focus: true

         TextInput {
             id: input
             focus: true
         }
     }
 }
```

### `void activeFocusOnTabChanged(bool)`

**作用与语义：**

该属性决定项是否希望处于标签焦点链中。默认情况下，该项设置为`false`。
注意：`tabFocusBehavior`还可以进一步限制只关注特定类型的控件，比如仅限文本或列表控件。macOS 上就是这样，根据系统设置，可能会限制对特定控件的关注。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `activeFocusOnTab` 的变化，不要把它当作普通函数主动调用。

### `void antialiasingChanged(bool)`

**作用与语义：**

指定该项目是否进行了抗锯齿处理。
视觉元素用于决定物品是否应使用抗锯齿。在某些情况下，带有抗锯齿的物品需要更多内存，渲染速度也可能更慢（详见抗锯齿部分）。
默认为假，但可被派生元素覆盖。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `antialiasing` 的变化，不要把它当作普通函数主动调用。

### `void baselineOffsetChanged(qreal)`

**作用与语义：**

指定该物品基线在本地坐标中的位置。
`Text`项的基线是文本所处的虚数线。包含文本的控件通常将其基线设置为文本的基线。
对于非文本项目，默认基线偏移量为0。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `baselineOffset` 的变化，不要把它当作普通函数主动调用。

### `void childrenRectChanged(const QRectF &)`

**作用与语义：**

该属性包含该物品子的集体位置和大小。
如果你需要访问某个物品子节点的集体几何体以正确调整该项目的大小，这个属性非常有用。
返回的几何体是该项目的局部。例如：

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `childrenRect` 的变化，不要把它当作普通函数主动调用。

**官方示例：**

```cpp
 Item {
     x: 50
     y: 100

     // prints: QRectF(-10, -20, 30, 40)
     Component.onCompleted: print(childrenRect)

     Item {
         x: -10
         y: -20
         width: 30
         height: 40
     }
 }
```

### `void clipChanged(bool)`

**作用与语义：**

该属性适用于是否启用裁剪。默认裁剪值为 `false`。
如果启用裁剪，项将裁剪自身绘制内容以及其子项的绘制内容到其边界矩形。如果在项的绘制操作中设置了裁剪，请记得重新设置，以防裁剪场景的其他部分。
注意：裁剪可能影响渲染性能。有关更多信息，请参见裁剪。
注意：为了 QML，如果将 clip 设置为 `true`，也会设置 `ItemIsViewport` 标志，这有时作为一种优化：具有 `ItemObservesViewport` 标志的子项可以省略创建视口外的场景图节点。但 `ItemIsViewport` 标志也可以独立设置。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `clip` 的变化，不要把它当作普通函数主动调用。

### `void containmentMaskChanged()`

**作用与语义：**

该属性包含一个可选遮罩，用于`contains()`方法，主要用于每个`QPointerEvent`的命中测试。
默认情况下，`contains()` 会返回物品边界框内任意点的 `true`。但任何实现函数 的`QQuickItem`或任何实现 函数的`QObject`。
可以用作掩体，将测试推迟到该对象。
注意：`contains()` 在事件传递过程中经常被调用。将击中测试推迟到另一个对象会在一定程度上减慢速度。如果该对象的 `contains()` 方法效率不高，containmentMask() 可能会引发性能问题。如果你实现了自定义的 `QQuickItem` 子类，也可以选择覆盖`contains()`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `containmentMask` 的变化，不要把它当作普通函数主动调用。

**官方示例：**

```cpp
 Q_INVOKABLE bool contains(const QPointF &point) const;
```

### `void enabledChanged()`

**作用与语义：**

该属性决定项目是否接收鼠标和键盘事件。默认情况下，这为真。
设置该属性直接影响子项的`enabled`值。当设置为`false`时，所有子项的`enabled`值也会变为`false`。当设置为`true`时，子项的`enabled`值会返回`true`，除非它们被明确设置为`false`。
将该属性设置为`false`会自动使`activeFocus`被设置为`false`，该项将不再接收键盘事件。
注意：悬停事件由`setAcceptHoverEvents()`单独启用。因此，禁用的物品即使该属性被`false`，仍可继续接收悬停事件。这使得即使关闭交互项，仍能显示信息反馈（如`ToolTip`）。任何作为物品子节点添加的`HoverHandlers`同样适用。然而，`HoverHandler`可以显式`disabled`，或者例如绑定到物品的 `enabled` 状态。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `enabled` 的变化，不要把它当作普通函数主动调用。

### `void focusChanged(bool)`

**作用与语义：**

该特性成立，是否该物品在包围`FocusScope`内具有焦点。如果成立，当包围`FocusScope`获得主动焦点时，该物品将获得主动焦点。
在以下例子中，当`input` `scope`获得主动聚焦时，将获得主动专注：
在此属性中，整个场景被假定为聚焦示波器。在实际操作层面，这意味着后续的量子大力学将在启动时给予`input`主动聚焦。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `focus` 的变化，不要把它当作普通函数主动调用。

**官方示例：**

```cpp
 import QtQuick 2.0

 Rectangle {
     width: 100; height: 100

     FocusScope {
         id: scope

         TextInput {
             id: input
             focus: true
         }
     }
 }
```

### `void focusPolicyChanged(Qt::FocusPolicy)`

**作用与语义：**

该属性决定了物品接受聚焦的方式。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `focusPolicy` 的变化，不要把它当作普通函数主动调用。

### `void heightChanged()`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该地块能承受该物品的高度。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `height` 的变化，不要把它当作普通函数主动调用。

### `void implicitHeightChanged()`

**作用与语义：**

定义物品的首选宽度或高度。
如果未指定`width`或`height`，则物品的有效尺寸将由其`implicitWidth`或`implicitHeight`确定。
然而，如果某个项目是布局的子节点，布局会通过其隐式大小决定该项目的首选大小。在这种情况下，显式的`width`或`height`将被忽略。
大多数项目默认隐式大小为0x0，但某些项固有隐式大小无法覆盖，例如`Image`和`Text`。
设置隐式大小对于定义基于内容具有优先大小的组件非常有用，例如：
注意：使用`Text`或`TextEdit` `implicitWidth`并明确设置宽度会带来性能惩罚，因为文本必须排版两次。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `implicitHeight` 的变化，不要把它当作普通函数主动调用。

**官方示例：**

```cpp
 // Label.qml
 import QtQuick 2.0

 Item {
     property alias icon: image.source
     property alias label: text.text
     implicitWidth: text.implicitWidth + image.implicitWidth
     implicitHeight: Math.max(text.implicitHeight, image.implicitHeight)
     Image { id: image }
     Text {
         id: text
         wrapMode: Text.Wrap
         anchors.left: image.right; anchors.right: parent.right
         anchors.verticalCenter: parent.verticalCenter
     }
 }
```

### `void implicitWidthChanged()`

**作用与语义：**

定义物品的首选宽度或高度。
如果未指定`width`或`height`，则物品的有效尺寸将由其`implicitWidth`或`implicitHeight`确定。
然而，如果某个项目是布局的子节点，布局会通过其隐式大小决定该项目的首选大小。在这种情况下，显式的`width`或`height`将被忽略。
大多数项目默认隐式大小为0x0，但某些项固有隐式大小无法覆盖，例如`Image`和`Text`。
设置隐式大小对于定义基于内容具有优先大小的组件非常有用，例如：
注意：使用`Text`或`TextEdit` `implicitWidth`并明确设置宽度会带来性能惩罚，因为文本必须排版两次。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `implicitWidth` 的变化，不要把它当作普通函数主动调用。

**官方示例：**

```cpp
 // Label.qml
 import QtQuick 2.0

 Item {
     property alias icon: image.source
     property alias label: text.text
     implicitWidth: text.implicitWidth + image.implicitWidth
     implicitHeight: Math.max(text.implicitHeight, image.implicitHeight)
     Image { id: image }
     Text {
         id: text
         wrapMode: Text.Wrap
         anchors.left: image.right; anchors.right: parent.right
         anchors.verticalCenter: parent.verticalCenter
     }
 }
```

### `void opacityChanged()`

**作用与语义：**

该属性包含该项的不透明度。不透明度指定为0.0（完全透明）到1.0（完全不透明）之间的数值。默认值为1.0。
当该属性被设置时，指定的不透明度也会单独应用到子项上。在某些情况下，这可能会产生意想不到的影响。例如，在下面的第二组矩形中，红色矩形指定了0.5的不透明度，这影响了其蓝色子矩形的不透明度，尽管该子矩形并未指定不透明度。
0到1范围之外的数值会被夹紧。
- '`: `Item' {
`Rectangle` {。
颜色：“红色”。
宽度：100;高度：100。
`Rectangle` {。
颜色：“蓝色”。
x：50;y：50;宽度：100;高度：100。
}。
}。
}。
- '`: `Item' {
`Rectangle` {。
不透明度：0.5。
颜色：“红色”。
宽度：100;高度：100。
`Rectangle` {。
颜色：“蓝色”。
x：50;y：50;宽度：100;高度：100。
}。
}。
}。
更改物品的透明度不会影响该物品是否接收用户输入事件。（相比之下，将`visible`属性设置为`false`会停止鼠标事件，将`enabled`属性设置为`false`则停止鼠标和键盘事件，同时移除对该物品的主动关注。）。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `opacity` 的变化，不要把它当作普通函数主动调用。

### `void parentChanged(QQuickItem *)`

**作用与语义：**

该属性包含该项的视觉父。
注意：视觉父的概念与`QObject`父的概念不同。一个项目的视觉父节点不一定与其对象父节点相同。更多详情请参见Qt Quick中的概念 - 视觉父。
注意：该属性的通知信号在视觉父节点销毁时发出。C 信号处理者不能假设视觉父层级中的项目仍然完整构建。使用`qobject_cast`验证父层级中的项目是否可以安全地作为预期类型使用。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `parent` 的变化，不要把它当作普通函数主动调用。

### `void rotationChanged()`

**作用与语义：**

该属性表示物品围绕其`transformOrigin`顺时针旋转的度数。
默认值为0度（即不旋转）。
- '`: `Rectangle' {
颜色：“蓝色”。
宽度：100;高度：100。
`Rectangle` {。
颜色：“红色”。
x：25;y：25;宽度：50;高度：50。
轮换：30。
}。
}。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `rotation` 的变化，不要把它当作普通函数主动调用。

### `void scaleChanged()`

**作用与语义：**

该属性表示该项的比例因子。
比例小于1.0时，物品的渲染尺寸变小;比例大于1.0时，物品的尺寸会变大。负比例则表示物品在渲染时被镜像化。
默认值是1.0。
缩放是从`transformOrigin`开始的。
- ''： import QtQuick 2.0

`Rectangle` {。
颜色：“蓝色”。
宽度：100;高度：100。

`Rectangle` {。
颜色：“绿色”。
宽度：25;高度：25。
}。

`Rectangle` {。
颜色：“红色”。
x：25;y：25;宽度：50;高度：50。
比例：1.4。
}。
}。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `scale` 的变化，不要把它当作普通函数主动调用。

### `void smoothChanged(bool)`

**作用与语义：**

指定该项目是否被平滑处理。
主要用于基于图像的项目，以决定该项目是否应使用平滑采样。平滑采样通过线性插值实现，而非平滑采样则使用最近邻进行。
在 Qt Quick 2.0 中，这一特性对性能的影响很小。
默认情况下，该属性被设置为`true`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `smooth` 的变化，不要把它当作普通函数主动调用。

### `void stateChanged(const QString &)`

**作用与语义：**

该属性保存项目当前状态的名称。
如果项目处于默认状态，即未设置任何显式状态，则该属性保存为空字符串。同样，可以通过将此属性设置为空字符串将项目恢复到默认状态。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `state` 的变化，不要把它当作普通函数主动调用。

### `void transformOriginChanged(QQuickItem::TransformOrigin)`

**作用与语义：**

此属性保存缩放和旋转变换的原点。
提供九个变换原点，如下图所示。默认的变换原点是 `Item.Center`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `transformOrigin` 的变化，不要把它当作普通函数主动调用。

### `void visibleChanged()`

**作用与语义：**

该属性在物品可见时成立。默认情况下，这点成立。
设置该属性直接影响子项的`visible`值。当设置为`false`时，所有子项的`visible`值也会变为`false`。当设置为`true`时，子项的`visible`值会返回`true`，除非它们明确设置为`false`。
（由于这种连贯行为，如果属性绑定只对显式属性变化做出响应，使用`visible`属性可能无法达到预期效果。在这种情况下，使用`opacity`属性可能更好。）。
如果该属性设置为`false`，物品将不再接收鼠标事件，但会继续接收按键事件，并且如果已设置，键盘`focus`会保留。（相反，将`enabled`属性设置为`false`会停止鼠标和键盘事件，同时移除对物品的关注。）。
注意：该属性的价值仅会因该属性或父`visible`属性的变化而受到影响。例如，如果该物品移出屏幕，或者`opacity`变为0，属性不会改变。但出于历史原因，该属性在物品构建后依然成立，即使该物品尚未添加到场景中。更改或读取尚未添加到场景中的物品的属性可能无法达到预期效果。
注意：该属性的通知信号在视觉父节点销毁时发出。C 信号处理者不能假设视觉父层级中的项目仍然完整构建。使用`qobject_cast`验证父层级中的项目是否可以安全地作为预期类型使用。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `visible` 的变化，不要把它当作普通函数主动调用。

### `void widthChanged()`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性表示该项的宽度。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `width` 的变化，不要把它当作普通函数主动调用。

### `void xChanged()`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
定义该项相对于其父节点的x位置。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `x` 的变化，不要把它当作普通函数主动调用。

### `void yChanged()`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
定义了该物品相对于父节点的 y 位置。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `y` 的变化，不要把它当作普通函数主动调用。

### `void zChanged()`

**作用与语义：**

设置兄弟项目的叠加顺序。默认堆叠顺序为0。
叠加值较高的物品会被绘制在叠加顺序较低的兄弟姐妹上。叠加值相同的物品按出现顺序从下而上绘制。叠加值为负的物品则会被绘制在其父内容下方。
以下示例展示了堆叠顺序的各种影响。
- '`: Same `z' - 较早子节点之上后期子节点：
`Item` {。
`Rectangle` {。
颜色：“红色”。
宽度：100;高度：100。
}。
`Rectangle` {。
颜色：“蓝色”。
x：50;y：50;宽度：100;高度：100。
}。
}。
- 顶部的“`: Higher `z”：
`Item` {。
`Rectangle` {。
Z：1。
颜色：“红色”。
宽度：100;高度：100。
}。
`Rectangle` {。
颜色：“蓝色”。
x：50;y：50;宽度：100;高度：100。
}。
}。
- '`: Same `z' - 父之上的子节点：
`Item` {。
`Rectangle` {。
颜色：“红色”。
宽度：100;高度：100。
`Rectangle` {。
颜色：“蓝色”。
x：50;y：50;宽度：100;高度：100。
}。
}。
}。
- “`: Lower `z”如下：
`Item` {。
`Rectangle` {。
颜色：“红色”。
宽度：100;高度：100。
`Rectangle` {。
Z：-1。
颜色：“蓝色”。
x：50;y：50;宽度：100;高度：100。
}。
}。
}。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `z` 的变化，不要把它当作普通函数主动调用。

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
