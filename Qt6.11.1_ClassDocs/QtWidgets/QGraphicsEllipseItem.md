# QGraphicsEllipseItem

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QGraphicsEllipseItem` 是 图形场景与项目机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QGraphicsEllipseItem` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QGraphicsEllipseItem>`
- 继承自：QAbstractGraphicsShapeItem
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

- `QGraphicsEllipseItem(QGraphicsItem *parent = nullptr)`
- `QGraphicsEllipseItem(const QRectF &rect, QGraphicsItem *parent = nullptr)`
- `QGraphicsEllipseItem(qreal x, qreal y, qreal width, qreal height, QGraphicsItem *parent = nullptr)`
- `virtual ~QGraphicsEllipseItem()`
- `QRectF rect() const`
- `void setRect(const QRectF &rect)`
- `void setRect(qreal x, qreal y, qreal width, qreal height)`
- `void setSpanAngle(int angle)`
- `void setStartAngle(int angle)`
- `int spanAngle() const`
- `int startAngle() const`

### 重实现的公有函数

- `virtual QRectF boundingRect() const override`
- `virtual bool contains(const QPointF &point) const override`
- `virtual bool isObscuredBy(const QGraphicsItem *item) const override`
- `virtual QPainterPath opaqueArea() const override`
- `virtual void paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget = nullptr) override`
- `virtual QPainterPath shape() const override`
- `virtual int type() const override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[anonymous] enum`

**作用与语义：**

虚拟`type()`函数返回的值。
- `QGraphicsEllipseItem::Type`：`4`;图形椭圆项

### `[explicit] QGraphicsEllipseItem::QGraphicsEllipseItem(QGraphicsItem *parent = nullptr)`

**作用与语义：**

构造一个QGraphicsEllipseItem。`parent`传递给`QAbstractGraphicsShapeItem`的构造器。

### `[explicit] QGraphicsEllipseItem::QGraphicsEllipseItem(const QRectF &rect, QGraphicsItem *parent = nullptr)`

**作用与语义：**

以 `rect` 作为默认矩形构建 QGraphicsEllipseItem 。`parent` 传递给 `QAbstractGraphicsShapeItem` 的构造器。

### `[explicit] QGraphicsEllipseItem::QGraphicsEllipseItem(qreal x, qreal y, qreal width, qreal height, QGraphicsItem *parent = nullptr)`

**作用与语义：**

利用由（`x`， `y`）定义的矩形以及给定的`width`和`height`作为默认矩形，构建QGraphicsEllipseItem。`parent`传递给`QAbstractGraphicsShapeItem`的构造器。

### `[virtual noexcept] QGraphicsEllipseItem::~QGraphicsEllipseItem()`

**作用与语义：**

摧毁了`QGraphicsEllipseItem`。

### `[override virtual] QRectF QGraphicsEllipseItem::boundingRect() const`

**作用与语义：**

重实现自：`QGraphicsItem::boundingRect()` const.
这个纯虚拟函数将物品的外边界定义为矩形;所有绘画必须限制在物品的边界矩形内。`QGraphicsView`用此来判断物品是否需要重新绘制。
虽然物品的形状可以任意，但边界矩形始终是矩形，且不受物品变换的影响。
如果你想更改物品的边界矩形，必须先调用`prepareGeometryChange()`。这会通知场景即将发生的变化，以便更新物品几何索引;否则，场景将无法感知物品的新几何体，结果也未定义（通常渲染伪影会留在视图中）。
重新实现这个函数，让`QGraphicsView`判断小部件哪些部分需要重新绘制。
注意：对于绘制轮廓/笔画的形状，在包围矩形中包含一半的笔宽非常重要。不过，这并不需要补偿抗锯齿。

### `[override virtual] bool QGraphicsEllipseItem::contains(const QPointF &point) const`

**作用与语义：**

重实现自：`QGraphicsItem::contains`（const QPointF & point） const.
如果该项包含`point`，且位于本地坐标内，则返回`true`;否则返回 false。它通常被调用`QGraphicsView`来确定光标下方的物品，因此该函数的实现应尽可能轻量。
默认情况下，这个函数调用`shape()`，但你可以在子类中重新实现，以提供（或许更高效的）实现。

### `[override virtual] bool QGraphicsEllipseItem::isObscuredBy(const QGraphicsItem *item) const`

**作用与语义：**

重实现自：`QAbstractGraphicsShapeItem::isObscuredBy`（const QGraphicsItem *item） const.

### `[override virtual] QPainterPath QGraphicsEllipseItem::opaqueArea() const`

**作用与语义：**

重装：`QAbstractGraphicsShapeItem::opaqueArea()` const.

### `[override virtual] void QGraphicsEllipseItem::paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget = nullptr)`

**作用与语义：**

Reimplements： `QGraphicsItem::paint`（QPainter *painter， const QStyleOptionGraphicsItem *option， QWidget *widget）.
该函数通常由`QGraphicsView`调用，将物品内容绘制为局部坐标。
在`QGraphicsItem`子类中重新实现该函数，使用`painter`来提供该物品的绘画实现。`option`参数为物品提供了样式选项，如状态、暴露区域和细节层级提示。`widget`参数是可选的。如果提供了，它指向正在绘制的控件;否则为0。对于缓存绘制，`widget`总是0。
画家的笔默认为0宽，笔初始化为从画具调色板中的`QPalette::Text`笔。画笔初始化为`QPalette::Window`。
确保所有绘画都限制在`boundingRect()`边界内，以避免渲染伪影（因为`QGraphicsView`不会帮你裁剪画家）。特别是，当`QPainter`用指定`QPen`渲染形状轮廓时，轮廓的一半会在外侧绘制，另一半在你正在渲染的形状内侧（例如，笔宽为2单位时，你必须在`boundingRect()`内绘制1单位的轮廓）。`QGraphicsItem`不支持使用宽度非零的美观笔。
所有涂装均在本地坐标内完成。
注意：除非调用`update()`，否则物品必须始终以完全相同的方式重新绘制自己;否则可能会出现视觉伪影。换句话说，两次后续的paint()调用必须始终产生相同的输出，除非它们之间调用了`update()`。
注意：启用缓存并不保证图形视图框架只调用一次 paint()，即使没有明确调用 `update()`。详情请参见 `setCacheMode()` 文档。

### `QRectF QGraphicsEllipseItem::rect() const`

**作用与语义：**

返回该物品的椭圆几何形状作为`QRectF`。

### `void QGraphicsEllipseItem::setRect(const QRectF &rect)`

**作用与语义：**

将该物体的椭圆几何设定为`rect`。矩形的左边定义椭圆的左边，矩形的上缘描述椭圆的顶部。矩形的高度和宽度描述椭圆的高度和宽度。

### `void QGraphicsEllipseItem::setRect(qreal x, qreal y, qreal width, qreal height)`

**作用与语义：**

将该项的矩形设置为由（`x`， `y`）定义的矩形，以及给定的`width`和`height`。
这种便利函数等价于调用`setRect(QRectF(x, y, width, height))`。

### `void QGraphicsEllipseItem::setSpanAngle(int angle)`

**作用与语义：**

将椭圆段的张成角设置为`angle`，单位为16分之一度。该角与`startAngle()`一起使用表示椭圆段（一个饼）。默认张成角为5760（360 × 16，一个完整的椭圆）。

### `void QGraphicsEllipseItem::setStartAngle(int angle)`

**作用与语义：**

将椭圆段的起始角设置为`angle`，单位为16分之一度。该角度与`spanAngle()`一起使用表示椭圆段（饼）。默认情况下，起始角为0。

### `[override virtual] QPainterPath QGraphicsEllipseItem::shape() const`

**作用与语义：**

重装：`QGraphicsItem::shape()` const.
返回该项的形状，作为本地坐标中的`QPainterPath`。该形状用于多种用途，包括碰撞检测、碰撞测试以及`QGraphicsScene::items()`函数。
默认实现调用 `boundingRect()` 返回一个简单的矩形形状，但子类可以重新实现该函数，以返回非矩形物体更准确的形状。例如，一个圆形项目可能会选择返回椭圆形形状以更好地检测碰撞。例如：
形状的轮廓会根据绘画时笔的宽度和风格而变化。如果你想在物体的形状中包含这个轮廓，可以用`QPainterPathStroker`从笔触中创建形状。
该函数由默认实现的`contains()`和`collidesWithPath()`调用。

### `int QGraphicsEllipseItem::spanAngle() const`

**作用与语义：**

返回椭圆段的张成角，单位为16度。该角度与`startAngle()`一起使用表示椭圆段（饼）。默认情况下，该函数返回5760（360 × 16，一个完整的椭圆）。

### `int QGraphicsEllipseItem::startAngle() const`

**作用与语义：**

返回椭圆段的起始角度，单位为16分之一度。该角度与`spanAngle()`一起使用表示椭圆段（饼）。默认起始角为0。

### `[override virtual] int QGraphicsEllipseItem::type() const`

**作用与语义：**

重装：`QGraphicsItem::type()` const.
返回一个项目的类型，作为整数。所有标准的 Graphicsitem 类都关联一个唯一的值;参见`QGraphicsItem::Type`。`qgraphicsitem_cast()` 利用这些类型信息来区分类型。
默认实现（`QGraphicsItem`）返回`UserType`。
要启用自定义物品中的 `qgraphicsitem_cast()`，请重新实现该函数并声明一个等于自定义物品类型的 Type enum 值。自定义物品必须返回大于 `UserType`（65536）的值。

### `enum { Type }`

**作用与语义：**

虚拟`type()`函数返回的值。
- `QGraphicsEllipseItem::Type`：`4`;图形椭圆项

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

`QGraphicsEllipseItem` 所属机制类型：图形场景与项目机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
