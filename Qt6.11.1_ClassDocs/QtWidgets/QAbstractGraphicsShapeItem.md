# QAbstractGraphicsShapeItem

> Qt 6.11.1 · Qt Widgets

## 1. 先建立直觉

**一句话定位：** `QAbstractGraphicsShapeItem` 是 Qt Widgets 界面机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Widgets 提供传统桌面应用的控件、布局、模型/视图、窗口和交互组件。

### 这是什么

`QAbstractGraphicsShapeItem` 是 Qt Widgets 中的抽象协议类型，通常通过具体子类、模型、插件或工厂来使用。

**内部模型：** 抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

**适用场景：** 当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。

**典型调用链：** 选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。

**先记住的坑：** 不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

## 2. 依赖与对象关系

- 头文件：`#include <QAbstractGraphicsShapeItem>`
- 继承自：QGraphicsItem
- 直接派生类：QGraphicsEllipseItem、QGraphicsPathItem、QGraphicsPolygonItem、QGraphicsRectItem,、QGraphicsSimpleTextItem

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Widgets)
target_link_libraries(mytarget PRIVATE Qt6::Widgets)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

### 状态、生命周期和线程

**生命周期：** 控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

**状态与结果：** 控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

**线程与事件循环：** 所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

## 3. 直接使用

当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。 使用时通常按这个过程组织：选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QAbstractGraphicsShapeItem(QGraphicsItem *parent = nullptr)`
- `virtual ~QAbstractGraphicsShapeItem()`
- `QBrush brush() const`
- `QPen pen() const`
- `void setBrush(const QBrush &brush)`
- `void setPen(const QPen &pen)`

### 重实现的公有函数

- `virtual bool isObscuredBy(const QGraphicsItem *item) const override`
- `virtual QPainterPath opaqueArea() const override`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[explicit] QAbstractGraphicsShapeItem::QAbstractGraphicsShapeItem(QGraphicsItem *parent = nullptr)`

**作用与语义：**

构造一个 QAbstractGraphicsShapeItem。`parent` 传递给 `QGraphicsItem` 的构造器。

### `[virtual noexcept] QAbstractGraphicsShapeItem::~QAbstractGraphicsShapeItem()`

**作用与语义：**

毁掉一个`QAbstractGraphicsShapeItem`。

### `QBrush QAbstractGraphicsShapeItem::brush() const`

**作用与语义：**

返回物品的画刷，或者如果没有画刷设置，则返回空画刷。

### `[override virtual] bool QAbstractGraphicsShapeItem::isObscuredBy(const QGraphicsItem *item) const`

**作用与语义：**

重实现自：`QGraphicsItem::isObscuredBy`（const QGraphicsItem *item） const.
如果该物品的边界矩形完全被不透明的`item`形状遮挡，返回`true`。
基础实现将`item`的`opaqueArea()`映射到该项目的坐标系，然后检查该项目的`boundingRect()`是否完全包含在映射形状内。
你可以重新实现这个函数，提供一个自定义算法来判断该项是否被`item`遮挡。

### `[override virtual] QPainterPath QAbstractGraphicsShapeItem::opaqueArea() const`

**作用与语义：**

重实现自：`QGraphicsItem::opaqueArea()` const.
该虚拟函数返回一个形状，表示该项不透明的区域。如果该区域用不透明的画笔或颜色填充（即不透明），则该区域是不透明的。
该函数由`isObscuredBy()`使用，底层项目调用以确定是否被该项遮挡。
默认实现返回空`QPainterPath`，表明该项完全透明且未遮挡其他项。

### `QPen QAbstractGraphicsShapeItem::pen() const`

**作用与语义：**

返回该物品的笔。如果没有设置笔，该函数返回QPen()，一根默认的黑色实线笔，宽度为1。

### `void QAbstractGraphicsShapeItem::setBrush(const QBrush &brush)`

**作用与语义：**

将物品的画刷设置为`brush`。
物品的画刷用来填充物品。
如果你用画刷和`QGradient`，梯度是相对于物品坐标系的。

### `void QAbstractGraphicsShapeItem::setPen(const QPen &pen)`

**作用与语义：**

将该物品的笔设置为`pen`。
笔用来绘制物品的轮廓。

## 6. 深入实践与常见坑

### 生命周期和资源边界

控件有 parent 时通常由父控件管理销毁；顶层窗口可以放在栈上，也可以由应用对象或业务对象持有。隐藏控件仍然存在，关闭窗口也不一定等于删除对象或退出应用，必须明确 `WA_DeleteOnClose`、parent 和应用退出策略。

### 状态和错误边界

控件状态由属性、焦点、启用/禁用、可见性、选择状态和模型数据共同决定。改变属性可能触发重新布局或重绘；需要刷新界面时通常调用 `update()`，需要重新计算几何时让布局系统处理，不要直接调用 `paintEvent()`。

### 线程边界

所有 QWidget 的创建、访问、布局和绘制都应在 GUI 线程完成。后台线程通过信号把结果投递回来；不要从 worker 线程直接修改控件，也不要在 GUI 线程用 `waitFor...` 或长循环阻塞事件循环。

### 最容易出现的错误

不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QAbstractGraphicsShapeItem` 所属机制类型：Qt Widgets 界面机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
