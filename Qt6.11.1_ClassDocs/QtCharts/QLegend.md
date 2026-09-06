# QLegend

> Qt 6.11.1 · Qt Charts

## 1. 先建立直觉

**一句话定位：** 这是 Qt Charts 中围绕“Legend”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Charts 提供折线、柱状、饼图、散点图和坐标轴等数据可视化组件。

### 这是什么

`QLegend` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QLegend>`
- 继承自：QGraphicsWidget
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

- `enum MarkerShape { MarkerShapeDefault, MarkerShapeRectangle, MarkerShapeCircle, MarkerShapeRotatedRectangle, MarkerShapeTriangle, …, MarkerShapeFromSeries }`

### 属性

- `alignment : Qt::Alignment`
- `backgroundVisible : bool`
- `borderColor : QColor`
- `color : QColor`
- `font : QFont`
- `labelColor : QColor`
- `markerShape : MarkerShape`
- `reverseMarkers : bool`
- `showToolTips : bool`

### 公有函数

- `virtual ~QLegend()`
- `Qt::Alignment alignment() const`
- `void attachToChart()`
- `QColor borderColor()`
- `QBrush brush() const`
- `QColor color()`
- `void detachFromChart()`
- `QFont font() const`
- `bool isAttachedToChart()`
- `bool isBackgroundVisible() const`
- `(since 6.2) bool isInteractive() const`
- `QBrush labelBrush() const`
- `QColor labelColor() const`
- `QLegend::MarkerShape markerShape() const`
- `QList<QLegendMarker *> markers(QAbstractSeries *series = nullptr) const`
- `QPen pen() const`
- `bool reverseMarkers()`
- `void setAlignment(Qt::Alignment alignment)`
- `void setBackgroundVisible(bool visible = true)`
- `void setBorderColor(QColor color)`
- `void setBrush(const QBrush &brush)`
- `void setColor(QColor color)`
- `void setFont(const QFont &font)`
- `(since 6.2) void setInteractive(bool interactive)`
- `void setLabelBrush(const QBrush &brush)`
- `void setLabelColor(QColor color)`
- `void setMarkerShape(QLegend::MarkerShape shape)`
- `void setPen(const QPen &pen)`
- `void setReverseMarkers(bool reverseMarkers = true)`
- `void setShowToolTips(bool show)`
- `bool showToolTips() const`

### 信号

- `(since 6.2) void attachedToChartChanged(bool attached)`
- `void backgroundVisibleChanged(bool visible)`
- `void borderColorChanged(QColor color)`
- `void colorChanged(QColor color)`
- `void fontChanged(QFont font)`
- `void labelColorChanged(QColor color)`
- `void markerShapeChanged(QLegend::MarkerShape shape)`
- `void reverseMarkersChanged(bool reverseMarkers)`
- `void showToolTipsChanged(bool showToolTips)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QLegend::MarkerShape`

**作用与语义：**

此枚举描述了渲染图例标记项时使用的形状。
- `QLegend::MarkerShapeDefault`: `0`; 标记使用由`QLegend`确定的默认形状。此值仅支持单个`QLegendMarker`项。
- `QLegend::MarkerShapeRectangle`: `1`; 使用矩形标记。标记大小由字体大小确定。
- `QLegend::MarkerShapeCircle`: `2`; 使用圆形标记。标记大小由字体大小确定。
- `QLegend::MarkerShapeRotatedRectangle`: `4`; 使用旋转矩形形状的标记。标记大小由字体大小确定。
- `QLegend::MarkerShapeTriangle`: `5`; 使用三角形标记。标记大小由字体大小确定。
- `QLegend::MarkerShapeStar`: `6`; 使用星形标记。标记大小由字体大小确定。
- `QLegend::MarkerShapePentagon`: `7`; 使用五边形标记。标记大小由字体大小确定。
- `QLegend::MarkerShapeFromSeries`: `3`; 标记形状由系列决定。在散点序列的情况下，图例标记看起来像散点，并且与点的大小相同。在折线或样条序列的情况下，图例标记看起来像线的小段。对于其他序列类型，显示矩形标记。如果为系列指定了`lightMarker`，则将显示`lightMarker`，其大小由系列标记大小决定。

### `alignment : Qt::Alignment`

**作用与语义：**

图例与图表对齐。
可以是`Qt::AlignTop`、`Qt::AlignBottom`、`Qt::AlignLeft`、`Qt::AlignRight`。如果你设置多个旗标，结果是未定义的。

**如何使用：** 调用 `alignment()` 读取当前值；它不会修改应用状态。

### `backgroundVisible : bool`

**作用与语义：**

该属性决定图例背景是否可见。

**如何使用：** 调用 `backgroundVisible()` 读取当前值；它不会修改应用状态。

### `borderColor : QColor`

**作用与语义：**

该属性保留了图例的线条颜色。

**如何使用：** 调用 `borderColor()` 读取当前值；它不会修改应用状态。

### `color : QColor`

**作用与语义：**

该属性保留图例的背景（画笔）颜色。
如果你改变了图例的颜色，图例画笔的样式会被设置为`Qt::SolidPattern`。

**如何使用：** 调用 `color()` 读取当前值；它不会修改应用状态。

### `font : QFont`

**作用与语义：**

该地产保存了图例所用标记的字体。

**如何使用：** 调用 `font()` 读取当前值；它不会修改应用状态。

### `labelColor : QColor`

**作用与语义：**

该属性决定了用于绘制标签的画笔颜色。

**如何使用：** 调用 `labelColor()` 读取当前值；它不会修改应用状态。

### `markerShape : MarkerShape`

**作用与语义：**

图例标记的默认形状。默认值为 `MarkerShapeRectangle`。

**如何使用：** 调用 `markerShape()` 读取当前值；它不会修改应用状态。

### `reverseMarkers : bool`

**作用与语义：**

该属性决定图例中的标记是否采用逆序。
该属性默认`false`。

**如何使用：** 调用 `reverseMarkers()` 读取当前值；它不会修改应用状态。

### `showToolTips : bool`

**作用与语义：**

该属性在截断文本时是否显示提示时依然适用。
该属性默认`false`。

**如何使用：** 调用 `showToolTips()` 读取当前值；它不会修改应用状态。

### `[virtual noexcept] QLegend::~QLegend()`

**作用与语义：**

销毁图例对象。图例总是由`QChart`拥有，因此应用程序绝不应调用此函数。

### `void QLegend::attachToChart()`

**作用与语义：**

将图例附加到图表上。图表可以调整图例的布局。

### `[signal, since 6.2] void QLegend::attachedToChartChanged(bool attached)`

**作用与语义：**

当图例被`attached`或从图表上分离时，该信号会发出。

### `[signal] void QLegend::backgroundVisibleChanged(bool visible)`

**作用与语义：**

该属性决定图例背景是否可见。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `backgroundVisible` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QLegend::borderColorChanged(QColor color)`

**作用与语义：**

该属性保留了图例的线条颜色。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `borderColor` 的变化，不要把它当作普通函数主动调用。

### `QBrush QLegend::brush() const`

**作用与语义：**

还给传说用的画笔。

### `[signal] void QLegend::colorChanged(QColor color)`

**作用与语义：**

该属性保留图例的背景（画笔）颜色。
如果你改变了图例的颜色，图例画笔的样式会被设置为`Qt::SolidPattern`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `color` 的变化，不要把它当作普通函数主动调用。

### `void QLegend::detachFromChart()`

**作用与语义：**

将图例从图表中分离。图表将不再调整图例的布局。

### `[signal] void QLegend::fontChanged(QFont font)`

**作用与语义：**

该地产保存了图例所用标记的字体。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `font` 的变化，不要把它当作普通函数主动调用。

### `bool QLegend::isAttachedToChart()`

**作用与语义：**

如果图例附在图表上，返回`true`。

### `bool QLegend::isBackgroundVisible() const`

**作用与语义：**

该属性决定图例背景是否可见。

**如何使用：** 调用 `isBackgroundVisible()` 读取当前值；它不会修改应用状态。

### `[since 6.2] bool QLegend::isInteractive() const`

**作用与语义：**

返回图例是否可以用鼠标拖拽或调整大小，且该图例已分离。

### `QBrush QLegend::labelBrush() const`

**作用与语义：**

还原用于绘制标签的画笔。

### `[signal] void QLegend::labelColorChanged(QColor color)`

**作用与语义：**

该属性决定了用于绘制标签的画笔颜色。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `labelColor` 的变化，不要把它当作普通函数主动调用。

### `QList<QLegendMarker *> QLegend::markers(QAbstractSeries *series = nullptr) const`

**作用与语义：**

返回图例中的标记列表。列表可以通过指定返回标记的`series`来过滤。

### `QPen QLegend::pen() const`

**作用与语义：**

归还传奇所用的笔。

### `[signal] void QLegend::reverseMarkersChanged(bool reverseMarkers)`

**作用与语义：**

该属性决定图例中的标记是否采用逆序。
该属性默认`false`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `reverseMarkers` 的变化，不要把它当作普通函数主动调用。

### `void QLegend::setBackgroundVisible(bool visible = true)`

**作用与语义：**

该属性决定图例背景是否可见。

**如何使用：** 调用 `setBackgroundVisible(...)` 修改 `backgroundVisible`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QLegend::setBrush(const QBrush &brush)`

**作用与语义：**

设定用于绘制传说背景的 `brush`。

### `[since 6.2] void QLegend::setInteractive(bool interactive)`

**作用与语义：**

当`interactive` `true`且图例被分离时，可以用鼠标像窗口一样移动和调整图例大小。
图例会自动通过拖拽图表边缘来附加到该边。双击附加图例即可将其分离。这是默认`false`。

### `void QLegend::setLabelBrush(const QBrush &brush)`

**作用与语义：**

将用于绘制图例标签的画笔设置为`brush`。

### `void QLegend::setPen(const QPen &pen)`

**作用与语义：**

设置用于绘制图例边框的 `pen`。

### `void QLegend::setShowToolTips(bool show)`

**作用与语义：**

该属性在截断文本时是否显示提示时依然适用。
该属性默认`false`。

**如何使用：** 调用 `setShowToolTips(...)` 修改 `showToolTips`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `bool QLegend::showToolTips() const`

**作用与语义：**

返回在省略图例标签时是否显示工具提示。
注意：地产的获取函数 showToolTips 使用。

### `[signal] void QLegend::showToolTipsChanged(bool showToolTips)`

**作用与语义：**

该属性在截断文本时是否显示提示时依然适用。
该属性默认`false`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `showToolTips` 的变化，不要把它当作普通函数主动调用。

### `Qt::Alignment alignment() const`

**作用与语义：**

图例与图表对齐。
可以是`Qt::AlignTop`、`Qt::AlignBottom`、`Qt::AlignLeft`、`Qt::AlignRight`。如果你设置多个旗标，结果是未定义的。

**如何使用：** 调用 `alignment()` 读取当前值；它不会修改应用状态。

### `QColor borderColor()`

**作用与语义：**

该属性保留了图例的线条颜色。

**如何使用：** 调用 `borderColor()` 读取当前值；它不会修改应用状态。

### `QColor color()`

**作用与语义：**

该属性保留图例的背景（画笔）颜色。
如果你改变了图例的颜色，图例画笔的样式会被设置为`Qt::SolidPattern`。

**如何使用：** 调用 `color()` 读取当前值；它不会修改应用状态。

### `QFont font() const`

**作用与语义：**

该地产保存了图例所用标记的字体。

**如何使用：** 调用 `font()` 读取当前值；它不会修改应用状态。

### `QColor labelColor() const`

**作用与语义：**

该属性决定了用于绘制标签的画笔颜色。

**如何使用：** 调用 `labelColor()` 读取当前值；它不会修改应用状态。

### `QLegend::MarkerShape markerShape() const`

**作用与语义：**

图例标记的默认形状。默认值为 `MarkerShapeRectangle`。

**如何使用：** 调用 `markerShape()` 读取当前值；它不会修改应用状态。

### `bool reverseMarkers()`

**作用与语义：**

该属性决定图例中的标记是否采用逆序。
该属性默认`false`。

**如何使用：** 调用 `reverseMarkers()` 读取当前值；它不会修改应用状态。

### `void setAlignment(Qt::Alignment alignment)`

**作用与语义：**

图例与图表对齐。
可以是`Qt::AlignTop`、`Qt::AlignBottom`、`Qt::AlignLeft`、`Qt::AlignRight`。如果你设置多个旗标，结果是未定义的。

**如何使用：** 调用 `setAlignment(...)` 修改 `alignment`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setBorderColor(QColor color)`

**作用与语义：**

该属性保留了图例的线条颜色。

**如何使用：** 调用 `setBorderColor(...)` 修改 `borderColor`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setColor(QColor color)`

**作用与语义：**

该属性保留图例的背景（画笔）颜色。
如果你改变了图例的颜色，图例画笔的样式会被设置为`Qt::SolidPattern`。

**如何使用：** 调用 `setColor(...)` 修改 `color`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setFont(const QFont &font)`

**作用与语义：**

该地产保存了图例所用标记的字体。

**如何使用：** 调用 `setFont(...)` 修改 `font`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setLabelColor(QColor color)`

**作用与语义：**

该属性决定了用于绘制标签的画笔颜色。

**如何使用：** 调用 `setLabelColor(...)` 修改 `labelColor`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMarkerShape(QLegend::MarkerShape shape)`

**作用与语义：**

图例标记的默认形状。默认值为 `MarkerShapeRectangle`。

**如何使用：** 调用 `setMarkerShape(...)` 修改 `markerShape`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setReverseMarkers(bool reverseMarkers = true)`

**作用与语义：**

该属性决定图例中的标记是否采用逆序。
该属性默认`false`。

**如何使用：** 调用 `setReverseMarkers(...)` 修改 `reverseMarkers`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void markerShapeChanged(QLegend::MarkerShape shape)`

**作用与语义：**

图例标记的默认形状。默认值为 `MarkerShapeRectangle`。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `markerShape` 的变化，不要把它当作普通函数主动调用。

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

`QLegend` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
