# QScatterSeries

> Qt 6.11.1 · Qt Charts

## 1. 先建立直觉

**一句话定位：** 这是 Qt Charts 中围绕“ScatterSeries”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Charts 提供折线、柱状、饼图、散点图和坐标轴等数据可视化组件。

### 这是什么

`QScatterSeries` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QScatterSeries>`
- 继承自：QXYSeries
- 直接派生类：未在类页中列出

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

### 状态、生命周期和线程

**生命周期：** 先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

**状态与结果：** 把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

**线程与事件循环：** 如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

## 3. 直接使用

围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum MarkerShape { MarkerShapeCircle, MarkerShapeRectangle, MarkerShapeRotatedRectangle, MarkerShapeTriangle, MarkerShapeStar, MarkerShapePentagon }`

### 属性

- `borderColor : QColor`
- `brush : QBrush`
- `color : QColor`
- `markerShape : MarkerShape`
- `markerSize : qreal`

### 公有函数

- `QScatterSeries(QObject *parent = nullptr)`
- `virtual ~QScatterSeries()`
- `QColor borderColor() const`
- `QBrush brush() const`
- `virtual QColor color() const override`
- `QScatterSeries::MarkerShape markerShape() const`
- `qreal markerSize() const`
- `void setBorderColor(const QColor &color)`
- `virtual void setColor(const QColor &color) override`
- `void setMarkerShape(QScatterSeries::MarkerShape shape)`
- `void setMarkerSize(qreal size)`

### 重实现的公有函数

- `virtual void setBrush(const QBrush &brush) override`
- `virtual void setPen(const QPen &pen) override`
- `virtual QAbstractSeries::SeriesType type() const override`

### 信号

- `void borderColorChanged(QColor color)`
- `void colorChanged(QColor color)`
- `void markerShapeChanged(QScatterSeries::MarkerShape shape)`
- `void markerSizeChanged(qreal size)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QScatterSeries::MarkerShape`

**作用与语义：**

该枚举值描述了在渲染标记项时所使用的形状。
- `QScatterSeries::MarkerShapeCircle`：`0`;标记是一个圆圈。这是默认值。
- `QScatterSeries::MarkerShapeRectangle`：`1`;标记为矩形。
- `QScatterSeries::MarkerShapeRotatedRectangle`：`2`;标记是一个旋转的矩形。
- `QScatterSeries::MarkerShapeTriangle`：`3`;标记是一个三角形。
- `QScatterSeries::MarkerShapeStar`：`4`;标记是一颗星星。
- `QScatterSeries::MarkerShapePentagon`：`5`;标记是一个五边形。

### `borderColor : QColor`

**作用与语义：**

该属性保留用于绘制标记边界的颜色。
这是修改笔颜色的一个便利属性。

**如何使用：** 调用 `borderColor()` 读取当前值；它不会修改应用状态。

### `brush : QBrush`

**作用与语义：**

该属性包含用于绘制散射系列标记的画刷。
画笔可以是可以用`QPainterPath`创建的图像。

**如何使用：** 调用 `brush()` 读取当前值；它不会修改应用状态。

### `color : QColor`

**作用与语义：**

该属性决定了用于填充系列标记的颜色。
这是一个方便属性，用于修改画笔颜色。

**如何使用：** 调用 `color()` 读取当前值；它不会修改应用状态。

### `markerShape : MarkerShape`

**作用与语义：**

该属性表示了用于渲染系列点的标记形状。
默认形状是`MarkerShapeCircle`。

**如何使用：** 调用 `markerShape()` 读取当前值；它不会修改应用状态。

### `markerSize : qreal`

**作用与语义：**

该属性决定了用于渲染系列点的标记大小。

**如何使用：** 调用 `markerSize()` 读取当前值；它不会修改应用状态。

### `[explicit] QScatterSeries::QScatterSeries(QObject *parent = nullptr)`

**作用与语义：**

构造一个是`parent`子的系列对象。

### `[virtual noexcept] QScatterSeries::~QScatterSeries()`

**作用与语义：**

删除散点系列。
注意：将系列添加到`QChart`会将所有权转移到图表上。

### `[signal] void QScatterSeries::borderColorChanged(QColor color)`

**作用与语义：**

该属性保留用于绘制标记边界的颜色。
这是修改笔颜色的一个便利属性。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `borderColor` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QScatterSeries::colorChanged(QColor color)`

**作用与语义：**

该属性决定了用于填充系列标记的颜色。
这是一个方便属性，用于修改画笔颜色。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `color` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QScatterSeries::markerShapeChanged(QScatterSeries::MarkerShape shape)`

**作用与语义：**

该属性表示了用于渲染系列点的标记形状。
默认形状是`MarkerShapeCircle`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `markerShape` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QScatterSeries::markerSizeChanged(qreal size)`

**作用与语义：**

该属性决定了用于渲染系列点的标记大小。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `markerSize` 的变化，不要把它当作普通函数主动调用。

### `[override virtual] void QScatterSeries::setBrush(const QBrush &brush)`

**作用与语义：**

该属性包含用于绘制散射系列标记的画刷。
画笔可以是可以用`QPainterPath`创建的图像。

**如何使用：** 调用 `setBrush(...)` 修改 `brush`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `[override virtual] void QScatterSeries::setPen(const QPen &pen)`

**作用与语义：**

重装：`QXYSeries::setPen`（const QPen & pen）。
将用于绘制图表点的笔设置为`pen`。如果笔未定义，则使用图表主题中的笔。

### `[override virtual] QAbstractSeries::SeriesType QScatterSeries::type() const`

**作用与语义：**

重新实现了属性的访问函数：`QAbstractSeries::type`。

### `QColor borderColor() const`

**作用与语义：**

该属性保留用于绘制标记边界的颜色。
这是修改笔颜色的一个便利属性。

**如何使用：** 调用 `borderColor()` 读取当前值；它不会修改应用状态。

### `QBrush brush() const`

**作用与语义：**

该属性包含用于绘制散射系列标记的画刷。
画笔可以是可以用`QPainterPath`创建的图像。

**如何使用：** 调用 `brush()` 读取当前值；它不会修改应用状态。

### `virtual QColor color() const override`

**作用与语义：**

该属性决定了用于填充系列标记的颜色。
这是一个方便属性，用于修改画笔颜色。

**如何使用：** 调用 `color()` 读取当前值；它不会修改应用状态。

### `QScatterSeries::MarkerShape markerShape() const`

**作用与语义：**

该属性表示了用于渲染系列点的标记形状。
默认形状是`MarkerShapeCircle`。

**如何使用：** 调用 `markerShape()` 读取当前值；它不会修改应用状态。

### `qreal markerSize() const`

**作用与语义：**

该属性决定了用于渲染系列点的标记大小。

**如何使用：** 调用 `markerSize()` 读取当前值；它不会修改应用状态。

### `void setBorderColor(const QColor &color)`

**作用与语义：**

该属性保留用于绘制标记边界的颜色。
这是修改笔颜色的一个便利属性。

**如何使用：** 调用 `setBorderColor(...)` 修改 `borderColor`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `virtual void setColor(const QColor &color) override`

**作用与语义：**

该属性决定了用于填充系列标记的颜色。
这是一个方便属性，用于修改画笔颜色。

**如何使用：** 调用 `setColor(...)` 修改 `color`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMarkerShape(QScatterSeries::MarkerShape shape)`

**作用与语义：**

该属性表示了用于渲染系列点的标记形状。
默认形状是`MarkerShapeCircle`。

**如何使用：** 调用 `setMarkerShape(...)` 修改 `markerShape`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMarkerSize(qreal size)`

**作用与语义：**

该属性决定了用于渲染系列点的标记大小。

**如何使用：** 调用 `setMarkerSize(...)` 修改 `markerSize`；传入的新值会成为后续查询和相关界面行为所使用的值。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确认对象是值类型还是 QObject 派生对象，再确定所有权、有效期、拷贝成本和销毁方式。返回的句柄、索引、reply、设备或迭代器可能有独立的有效期，不能只看 C++ 指针是否非空。

### 状态和错误边界

把返回值、状态查询、错误信息和通知信号分开判断。调用成功可能只表示请求被接受，真正完成还要等待状态变化或完成信号；读取数据前先检查对象和结果是否有效。

### 线程边界

如果类型直接或间接参与 QObject、GUI、设备或异步框架，就必须确认线程归属和事件循环；值类型虽然可以复制，也要注意内部指针、共享数据和并发写入。

### 最容易出现的错误

不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QScatterSeries` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
