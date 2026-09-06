# QGraphicsObject

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QGraphicsObject` 是 图形场景与项目机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QGraphicsObject` 是 Qt Widgets 界面体系中的组件，负责一段可见 UI 或交互行为。

**内部模型：** 先区分它是顶层窗口、容器、输入控件、显示控件还是视图；再理解 parent、layout、model、signals 和事件之间的关系。

**适用场景：** 需要桌面控件、布局、用户输入、选择或模型/视图展示时使用。

**典型调用链：** 创建并设置 parent -> 配置属性和布局 -> connect 用户动作信号 -> show -> 按需处理事件/更新状态。

**先记住的坑：** 优先用 layout 管理几何；控件只能在 GUI 线程访问；自定义绘制放在 paintEvent；不要阻塞信号槽回调。

## 2. 依赖与对象关系

- 头文件：`#include <QGraphicsObject>`
- 继承自：QObject、QGraphicsItem
- 直接派生类：QGraphicsSvgItem、QGraphicsTextItem,、QGraphicsWidget

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

### 属性

- `effect : QGraphicsEffect*`
- `enabled : bool`
- `opacity : qreal`
- `parent : QGraphicsObject*`
- `pos : QPointF`
- `rotation : qreal`
- `scale : qreal`
- `transformOriginPoint : QPointF`
- `visible : bool`
- `x : qreal`
- `y : qreal`
- `z : qreal`

### 公有函数

- `QGraphicsObject(QGraphicsItem *parent = nullptr)`
- `virtual ~QGraphicsObject()`
- `void grabGesture(Qt::GestureType gesture, Qt::GestureFlags flags = Qt::GestureFlags())`
- `void ungrabGesture(Qt::GestureType gesture)`

### 信号

- `void enabledChanged()`
- `void opacityChanged()`
- `void parentChanged()`
- `void rotationChanged()`
- `void scaleChanged()`
- `void visibleChanged()`
- `void xChanged()`
- `void yChanged()`
- `void zChanged()`

### 重实现的保护函数

- `virtual bool event(QEvent *ev) override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `effect : QGraphicsEffect*`

**作用与语义：**

该属性保留该物品所附加的效果。

**如何使用：** 调用 `effect()` 读取当前值；它不会修改应用状态。

### `enabled : bool`

**作用与语义：**

无论该项是否被启用，该属性都成立。
该物业于`QGraphicsItem`年申报。
默认情况下，该属性是`true`的。

**如何使用：** 调用 `enabled()` 读取当前值；它不会修改应用状态。

### `opacity : qreal`

**作用与语义：**

该属性表示了该项的不透明度。

**如何使用：** 调用 `opacity()` 读取当前值；它不会修改应用状态。

### `parent : QGraphicsObject*`

**作用与语义：**

该属性包含该项的父。
注意：该项的父对象与`QObject::parent()`返回的父对象独立设置。

**如何使用：** 调用 `parent()` 读取当前值；它不会修改应用状态。

### `pos : QPointF`

**作用与语义：**

此属性保存项的位置。
描述项的位置。

**如何使用：** 调用 `pos()` 读取当前值；它不会修改应用状态。

### `rotation : qreal`

**作用与语义：**

该属性表示物品的旋转度数。
这说明了围绕其变换原点旋转物品的多少度。默认旋转是0度（即完全不旋转）。

**如何使用：** 调用 `rotation()` 读取当前值；它不会修改应用状态。

### `scale : qreal`

**作用与语义：**

该属性表示物品的比例。
小于1的比例表示该物品会显示比正常小，大小于1的表示显示会大于正常。负的比例表示该物品会被镜像。
默认情况下，物品以1的比例显示（即其正常大小）。
成长来自物品的变形起源。

**如何使用：** 调用 `scale()` 读取当前值；它不会修改应用状态。

### `transformOriginPoint : QPointF`

**作用与语义：**

该属性表示变换原点。
该属性将物品坐标系中的一个特定点设定为缩放和旋转的原点。

**如何使用：** 调用 `transformOriginPoint()` 读取当前值；它不会修改应用状态。

### `visible : bool`

**作用与语义：**

无论该物品是否可见，这一属性都成立。
该地产于`QGraphicsItem`年被宣布。
默认情况下，该属性为`true`。

**如何使用：** 调用 `visible()` 读取当前值；它不会修改应用状态。

### `x : qreal`

**作用与语义：**

该属性表示该项的 x 位置。
描述物品x的位置。

**如何使用：** 调用 `x()` 读取当前值；它不会修改应用状态。

### `y : qreal`

**作用与语义：**

该属性表示该项的 y 位置。
描述物品y的位置。

**如何使用：** 调用 `y()` 读取当前值；它不会修改应用状态。

### `z : qreal`

**作用与语义：**

该属性表示该项的z值。
描述了项目的z值。

**如何使用：** 调用 `z()` 读取当前值；它不会修改应用状态。

### `[explicit] QGraphicsObject::QGraphicsObject(QGraphicsItem *parent = nullptr)`

**作用与语义：**

构造一个带有`parent`的QGraphicsObject。

### `[virtual noexcept] QGraphicsObject::~QGraphicsObject()`

**作用与语义：**

毁灭者。

### `[signal] void QGraphicsObject::enabledChanged()`

**作用与语义：**

无论该项是否被启用，该属性都成立。
该物业于`QGraphicsItem`年申报。
默认情况下，该属性是`true`的。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `enabled` 的变化，不要把它当作普通函数主动调用。

### `[override virtual protected] bool QGraphicsObject::event(QEvent *ev)`

**作用与语义：**

重实现自：`QObject::event`（QEvent *e）。

### `void QGraphicsObject::grabGesture(Qt::GestureType gesture, Qt::GestureFlags flags = Qt::GestureFlags())`

**作用与语义：**

以特定`flags`将图形对象订阅给给定的`gesture`。

### `[signal] void QGraphicsObject::opacityChanged()`

**作用与语义：**

该属性表示了该项的不透明度。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `opacity` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QGraphicsObject::parentChanged()`

**作用与语义：**

该属性包含该项的父。
注意：该项的父对象与`QObject::parent()`返回的父对象独立设置。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `parent` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QGraphicsObject::rotationChanged()`

**作用与语义：**

该属性表示物品的旋转度数。
这说明了围绕其变换原点旋转物品的多少度。默认旋转是0度（即完全不旋转）。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `rotation` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QGraphicsObject::scaleChanged()`

**作用与语义：**

该属性表示物品的比例。
小于1的比例表示该物品会显示比正常小，大小于1的表示显示会大于正常。负的比例表示该物品会被镜像。
默认情况下，物品以1的比例显示（即其正常大小）。
成长来自物品的变形起源。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `scale` 的变化，不要把它当作普通函数主动调用。

### `void QGraphicsObject::ungrabGesture(Qt::GestureType gesture)`

**作用与语义：**

取消订阅给定`gesture`的图形对象。

### `[protected slot] void QGraphicsObject::updateMicroFocus()`

**作用与语义：**

更新物品的微焦点。这是方便的“槽函数”。

### `[signal] void QGraphicsObject::visibleChanged()`

**作用与语义：**

无论该物品是否可见，这一属性都成立。
该地产于`QGraphicsItem`年被宣布。
默认情况下，该属性为`true`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `visible` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QGraphicsObject::xChanged()`

**作用与语义：**

该属性表示该项的 x 位置。
描述物品x的位置。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `x` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QGraphicsObject::yChanged()`

**作用与语义：**

该属性表示该项的 y 位置。
描述物品y的位置。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `y` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QGraphicsObject::zChanged()`

**作用与语义：**

该属性表示该项的z值。
描述了项目的z值。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `z` 的变化，不要把它当作普通函数主动调用。

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

`QGraphicsObject` 所属机制类型：图形场景与项目机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
