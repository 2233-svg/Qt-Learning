# QPainterPath

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QPainterPath` 是 Qt GUI 绘制体系中的类型，负责画笔、画刷、字体、图像、绘制设备或绘制状态。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QPainterPath` 是 二维绘制状态机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 绘制对象维护一组状态：画笔、画刷、字体、变换、裁剪、合成模式和渲染提示。每次 draw 调用都会使用当前状态；坐标通常经过当前 transform 映射到目标设备。

**适用场景：** 开始绘制后配置必要状态，使用 save/restore 包围局部变换，按设备坐标绘制，结束时让上下文析构或调用 end。绘制文本和图片时同时考虑字体度量、devicePixelRatio、裁剪和性能。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要直接调用 paintEvent；不要在绘制函数里修改会再次触发绘制的状态；不要假定所有图像都是四字节像素；不要忘记 transform 会影响坐标和 boundingRect。

## 2. 依赖与对象关系

- 头文件：`#include <QPainterPath>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

绘制对象维护一组状态：画笔、画刷、字体、变换、裁剪、合成模式和渲染提示。每次 draw 调用都会使用当前状态；坐标通常经过当前 transform 映射到目标设备。

### 状态、生命周期和线程

**生命周期：** 绘制上下文必须绑定有效的 paint device，并在合法的绘制阶段使用。QWidget 上通常只在 `paintEvent()` 内创建 painter；离屏图像、打印设备和 pixmap 则有各自的设备生命周期。

**状态与结果：** `save()`/`restore()` 用于隔离局部状态；改变坐标系、画笔或合成模式后要么恢复，要么明确后续绘制也需要该状态。重绘请求和真正绘制是两个阶段，业务状态变化应调用 `update()`。

**线程与事件循环：** 同一个 GUI 控件的绘制在 GUI 线程完成；离屏 QImage 可以按数据所有权在后台处理，但不要让后台线程直接绘制或访问正在显示的 QWidget/QPixmap 资源。

## 3. 直接使用

开始绘制后配置必要状态，使用 save/restore 包围局部变换，按设备坐标绘制，结束时让上下文析构或调用 end。绘制文本和图片时同时考虑字体度量、devicePixelRatio、裁剪和性能。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

```cpp
void Widget::paintEvent(QPaintEvent *)
{
    QPainter painter(this);
    painter.save();
    // 设置画笔、画刷、字体或变换后进行绘制
    painter.restore();
}
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `class Element`
- `enum ElementType { MoveToElement, LineToElement, CurveToElement, CurveToDataElement }`

### 公有函数

- `QPainterPath()`
- `QPainterPath(const QPointF &startPoint)`
- `QPainterPath(const QPainterPath &path)`
- `(since 6.10) QPainterPath(QPainterPath &&other)`
- `~QPainterPath()`
- `void addEllipse(const QRectF &boundingRectangle)`
- `void addEllipse(const QPointF &center, qreal rx, qreal ry)`
- `void addEllipse(qreal x, qreal y, qreal width, qreal height)`
- `void addPath(const QPainterPath &path)`
- `void addPolygon(const QPolygonF &polygon)`
- `void addRect(const QRectF &rectangle)`
- `void addRect(qreal x, qreal y, qreal width, qreal height)`
- `void addRegion(const QRegion &region)`
- `void addRoundedRect(const QRectF &rect, qreal xRadius, qreal yRadius, Qt::SizeMode mode = Qt::AbsoluteSize)`
- `void addRoundedRect(qreal x, qreal y, qreal w, qreal h, qreal xRadius, qreal yRadius, Qt::SizeMode mode = Qt::AbsoluteSize)`
- `void addText(const QPointF &point, const QFont &font, const QString &text)`
- `void addText(qreal x, qreal y, const QFont &font, const QString &text)`
- `qreal angleAtPercent(qreal t) const`
- `void arcMoveTo(const QRectF &rectangle, qreal angle)`
- `void arcMoveTo(qreal x, qreal y, qreal width, qreal height, qreal angle)`
- `void arcTo(const QRectF &rectangle, qreal startAngle, qreal sweepLength)`
- `void arcTo(qreal x, qreal y, qreal width, qreal height, qreal startAngle, qreal sweepLength)`
- `QRectF boundingRect() const`
- `int capacity() const`
- `void clear()`
- `void closeSubpath()`
- `void connectPath(const QPainterPath &path)`
- `bool contains(const QPainterPath &p) const`
- `bool contains(const QPointF &point) const`
- `bool contains(const QRectF &rectangle) const`
- `QRectF controlPointRect() const`
- `void cubicTo(const QPointF &c1, const QPointF &c2, const QPointF &endPoint)`
- `void cubicTo(qreal c1X, qreal c1Y, qreal c2X, qreal c2Y, qreal endPointX, qreal endPointY)`
- `QPointF currentPosition() const`
- `QPainterPath::Element elementAt(int index) const`
- `int elementCount() const`
- `Qt::FillRule fillRule() const`
- `QPainterPath intersected(const QPainterPath &p) const`
- `bool intersects(const QPainterPath &p) const`
- `bool intersects(const QRectF &rectangle) const`
- `(since 6.10) bool isCachingEnabled() const`
- `bool isEmpty() const`
- `qreal length() const`
- `void lineTo(const QPointF &endPoint)`
- `void lineTo(qreal x, qreal y)`
- `void moveTo(const QPointF &point)`
- `void moveTo(qreal x, qreal y)`
- `qreal percentAtLength(qreal len) const`
- `QPointF pointAtPercent(qreal t) const`
- `void quadTo(const QPointF &c, const QPointF &endPoint)`
- `void quadTo(qreal cx, qreal cy, qreal endPointX, qreal endPointY)`
- `void reserve(int size)`
- `(since 6.10) void setCachingEnabled(bool enabled)`
- `void setElementPositionAt(int index, qreal x, qreal y)`
- `void setFillRule(Qt::FillRule fillRule)`
- `QPainterPath simplified() const`
- `qreal slopeAtPercent(qreal t) const`
- `QPainterPath subtracted(const QPainterPath &p) const`
- `void swap(QPainterPath &other)`
- `QPolygonF toFillPolygon(const QTransform &matrix = QTransform()) const`
- `QList<QPolygonF> toFillPolygons(const QTransform &matrix = QTransform()) const`
- `QPainterPath toReversed() const`
- `QList<QPolygonF> toSubpathPolygons(const QTransform &matrix = QTransform()) const`
- `void translate(qreal dx, qreal dy)`
- `void translate(const QPointF &offset)`
- `QPainterPath translated(qreal dx, qreal dy) const`
- `QPainterPath translated(const QPointF &offset) const`
- `(since 6.10) QPainterPath trimmed(qreal fromFraction, qreal toFraction, qreal offset = 0) const`
- `QPainterPath united(const QPainterPath &p) const`
- `bool operator!=(const QPainterPath &path) const`
- `QPainterPath operator&(const QPainterPath &other) const`
- `QPainterPath & operator&=(const QPainterPath &other)`
- `QPainterPath operator+(const QPainterPath &other) const`
- `QPainterPath & operator+=(const QPainterPath &other)`
- `QPainterPath operator-(const QPainterPath &other) const`
- `QPainterPath & operator-=(const QPainterPath &other)`
- `QPainterPath & operator=(QPainterPath &&other)`
- `QPainterPath & operator=(const QPainterPath &path)`
- `bool operator==(const QPainterPath &path) const`
- `QPainterPath operator|(const QPainterPath &other) const`
- `QPainterPath & operator|=(const QPainterPath &other)`

### 相关非成员函数

- `QDataStream & operator<<(QDataStream &stream, const QPainterPath &path)`
- `QDataStream & operator>>(QDataStream &stream, QPainterPath &path)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QPainterPath::ElementType`

**作用与语义：**

该枚举描述了用于连接子路径顶点的元素类型。
注意，使用`addEllipse()`、`addPath()`、`addPolygon()`、`addRect()`、`addRegion()`和`addText()`便利函数添加为闭子路径的元素，实际上是以`moveTo()`、`lineTo()`和`cubicTo()`函数为独立元素的集合加入路径。
- `QPainterPath::MoveToElement`：`0`;一个新的子路径。另见`moveTo()`。
- `QPainterPath::LineToElement`：`1`;一条线。另见`lineTo()`。
- `QPainterPath::CurveToElement`：`2`;一条曲线。另见`cubicTo()`和`quadTo()`。
- `QPainterPath::CurveToDataElement`：`3`;描述CurveToElement元素中曲线所需的额外数据。

### `[noexcept] QPainterPath::QPainterPath()`

**作用与语义：**

构造一个空的QPainterPath对象。

### `[explicit] QPainterPath::QPainterPath(const QPointF &startPoint)`

**作用与语义：**

创建一个QPainterPath对象，当前位置为给定`startPoint`。

### `QPainterPath::QPainterPath(const QPainterPath &path)`

**作用与语义：**

创建一个QPainterPath对象，它是给定`path`的副本。

### `[noexcept, since 6.10] QPainterPath::QPainterPath(QPainterPath &&other)`

**作用与语义：**

从`other`移动构建新的画家路径。
移除对象`other`置于默认构造状态。

### `[noexcept] QPainterPath::~QPainterPath()`

**作用与语义：**

摧毁了这个`QPainterPath`物体。

### `void QPainterPath::addEllipse(const QRectF &boundingRectangle)`

**作用与语义：**

在指定`boundingRectangle`内创建一个椭圆，并将其作为闭子路径添加到画家路径中。
椭圆由顺时针方向的曲线组成，起点和终点均为零度（即3点钟位置）。
- '`: `QLinearGradient' myGradient;
`QPen`我的笔;
`QRectF` boundingRectangle;

`QPainterPath` 我的路径;
myPath.addEllipse（boundingRectangle）;

`QPainter`画家（此）;
painter.setBrush（myGradient）;
painter.setPen（myPen）;
painter.drawPath（myPath）;

### `void QPainterPath::addEllipse(const QPointF &center, qreal rx, qreal ry)`

**作用与语义：**

创建一个位于`center`、半径为`rx`和`ry`的椭圆，并将其作为闭子路径添加到画家路径中。

### `void QPainterPath::addEllipse(qreal x, qreal y, qreal width, qreal height)`

**作用与语义：**

在由左上角定义的边界矩形中创建一个椭圆，该矩形由左上角`y` `x`定义，`width`和`height`，并将其作为闭子路径加入画家路径。

### `void QPainterPath::addPath(const QPainterPath &path)`

**作用与语义：**

将给定`path`加入该路径，作为闭子路径。

### `void QPainterPath::addPolygon(const QPolygonF &polygon)`

**作用与语义：**

将给定`polygon`添加到路径中，作为一个（未封闭的）子路径。
注意，添加多边形后的当前位置是`polygon`的最后一个点。要画回第一个点的线，可以使用`closeSubpath()`函数。
- “`: `QLinearGradient” myGradient;
`QPen` 我的笔;
`QPolygonF` myPolygon;

`QPainterPath` myPath;
myPath.addPolygon（myPolygon）;

`QPainter`画家（此）;
painter.setBrush（myGradient）;
painter.setPen（myPen）;
painter.drawPath（myPath）;

### `void QPainterPath::addRect(const QRectF &rectangle)`

**作用与语义：**

将给定`rectangle`添加到该路径中，作为闭子路径。
`rectangle`以顺时针线条的形式添加。`rectangle`添加后，画家路径的当前位置位于矩形的左上角。
- '`: `QLinearGradient' myGradient;
`QPen` 我的笔;
`QRectF` myRectangle;

`QPainterPath` myPath;
myPath.addRect（myRect）;

`QPainter`画家（此）;
painter.setBrush（myGradient）;
painter.setPen（myPen）;
painter.drawPath（myPath）;

### `void QPainterPath::addRect(qreal x, qreal y, qreal width, qreal height)`

**作用与语义：**

在位置（`x`， `y`）处添加一个矩形，并以给定的`width`和`height`作为闭子路径。

### `void QPainterPath::addRegion(const QRegion &region)`

**作用与语义：**

通过将区域内的每个矩形添加为单独的闭合子路径，将给定的`region`添加到路径中。

### `void QPainterPath::addRoundedRect(const QRectF &rect, qreal xRadius, qreal yRadius, Qt::SizeMode mode = Qt::AbsoluteSize)`

**作用与语义：**

将给定的矩形加`rect`，带有圆角。
`xRadius`和`yRadius`参数指定了定义圆角矩形角的椭圆半径。当`mode`为`Qt::RelativeSize`时，`xRadius`和`yRadius`分别以矩形宽度和高度的一半百分比表示，应在0.0到100.0之间。

### `void QPainterPath::addRoundedRect(qreal x, qreal y, qreal w, qreal h, qreal xRadius, qreal yRadius, Qt::SizeMode mode = Qt::AbsoluteSize)`

**作用与语义：**

将给定矩形`x`、`y`、`w` `h`带圆角的矩形添加到路径上。

### `void QPainterPath::addText(const QPointF &point, const QFont &font, const QString &text)`

**作用与语义：**

将给定`text`添加到该路径中，作为由所提供`font`创建的闭子路径集合。子路径的位置使文本基线的左端位于指定`point`。
部分字体可能产生重叠子路径，因此需要使用`Qt::WindingFill`填充规则才能正确渲染。
- '`: `QLinearGradient' myGradient;
`QPen` 我的笔;
`QFont` myFont;
`QPointF`基线（x， y）;

`QPainterPath` myPath;
myPath.addText（基线，myFont，tr（“Qt”））;

`QPainter`画家（此）;
painter.setBrush（myGradient）;
painter.setPen（myPen）;
painter.drawPath（myPath）;

### `void QPainterPath::addText(qreal x, qreal y, const QFont &font, const QString &text)`

**作用与语义：**

将给定`text`添加到该路径上，作为由所提供的`font`创建的闭子路径集合。子路径的位置使文本基线的左端位于由（`x`， `y`）指定的点。

### `qreal QPainterPath::angleAtPercent(qreal t) const`

**作用与语义：**

返回路径切线在百分比`t`处的角度。参数`t`必须介于0和1之间。
角度的正值表示逆时针方向，负值表示顺时针方向。零度位于3点钟方向。
注意，与其他百分比方法类似，如果路径中存在曲线，百分比测量对长度不是线性的。当存在曲线时，百分比参数映射到贝塞尔方程的t参数。

### `void QPainterPath::arcMoveTo(const QRectF &rectangle, qreal angle)`

**作用与语义：**

创造一个位于`angle` `rectangle`弧线上的移动。
角度以度数表示。顺时针弧线可以用负角度表示。

### `void QPainterPath::arcMoveTo(qreal x, qreal y, qreal width, qreal height, qreal angle)`

**作用与语义：**

生成一个位于`angle` `QRectF`（`x`、`y`、`width`、`height`）弧线上的移动。

### `void QPainterPath::arcTo(const QRectF &rectangle, qreal startAngle, qreal sweepLength)`

**作用与语义：**

形成一个占据指定`rectangle`的弧线，从指定`startAngle`开始，逆时针延伸`sweepLength`度。
角度以度数表示。顺时针弧线可以用负角度表示。
注意，如果弧的起点尚未连接，该函数将弧的起点与当前位置连接起来。弧线加入后，当前位置即为弧线上的最后一点。要画线回第一点，使用`closeSubpath()`函数。
- '`: `QPainterPath' myPath;
myPath.moveTo（中心）;
myPath.arcTo（boundingRect， startAngle，。
sweepLength）;

`QPainter`画家（此）;
painter.setBrush（myGradient）;
painter.setPen（myPen）;
painter.drawPath（myPath）;

### `void QPainterPath::arcTo(qreal x, qreal y, qreal width, qreal height, qreal startAngle, qreal sweepLength)`

**作用与语义：**

形成一个弧线，占据矩形`QRectF`（`x`、`y`、`width`、`height`），从指定`startAngle`开始，逆时针方向延伸`sweepLength`度。

### `QRectF QPainterPath::boundingRect() const`

**作用与语义：**

将该画家路径的边界矩形返回为浮点精度矩形。

### `int QPainterPath::capacity() const`

**作用与语义：**

返回`QPainterPath`分配的元素数量。

### `void QPainterPath::clear()`

**作用与语义：**

清除存储的路径元素。
这使得路径可以重复使用之前的内存分配。

### `void QPainterPath::closeSubpath()`

**作用与语义：**

通过在子路径起点画一条线来闭合当前子路径，自动启动一条新路径。新路径的当前点为 （0， 0）。
如果子路径不包含任何元素，该函数则不做任何事。

### `void QPainterPath::connectPath(const QPainterPath &path)`

**作用与语义：**

通过将该路径的最后一个元素加上一条线，将给定`path`连接到该路径的第一个元素。

### `bool QPainterPath::contains(const QPainterPath &p) const`

**作用与语义：**

如果给定路径 `p` 包含在当前路径内，返回 `true`。返回 `false` 如果当前路径和 `p` 的边相交。
路径上的集合操作将路径视为区域。非封闭路径则视为隐式闭合。

### `bool QPainterPath::contains(const QPointF &point) const`

**作用与语义：**

如果给定`point`在路径内，返回`true`，否则返回`false`。

### `bool QPainterPath::contains(const QRectF &rectangle) const`

**作用与语义：**

如果给定`rectangle`在路径内，返回`true`，否则返回`false`。

### `QRectF QPainterPath::controlPointRect() const`

**作用与语义：**

返回包含该路径中所有点和控制点的矩形。
该函数的计算速度远快于精确`boundingRect()`，且返回的矩形总是`boundingRect()`返回矩形的超集。

### `void QPainterPath::cubicTo(const QPointF &c1, const QPointF &c2, const QPointF &endPoint)`

**作用与语义：**

利用`c1`和 `c2` 指定的控制点，在当前位置与给定`endPoint`之间添加一条三次贝塞尔曲线。
曲线加入后，当前位置会更新为曲线的终点。
- '`: `QLinearGradient' myGradient;
`QPen` 我的笔;

`QPainterPath` myPath;
myPath.cubicTo（c1， c2， endPoint）;

`QPainter`画家（此）;
painter.setBrush（myGradient）;
painter.setPen（myPen）;
painter.drawPath（myPath）;

### `void QPainterPath::cubicTo(qreal c1X, qreal c1Y, qreal c2X, qreal c2Y, qreal endPointX, qreal endPointY)`

**作用与语义：**

在当前位置与端点（`endPointX`， `endPointY`）之间添加一条三次贝塞尔曲线，控制点由（`c1X`， `c1Y`）和（`c2X`， `c2Y`）指定。

### `QPointF QPainterPath::currentPosition() const`

**作用与语义：**

返回路径的当前位置。

### `QPainterPath::Element QPainterPath::elementAt(int index) const`

**作用与语义：**

返回画家路径中给定`index`的元素。

### `int QPainterPath::elementCount() const`

**作用与语义：**

返回画家路径中的路径元素数量。

### `Qt::FillRule QPainterPath::fillRule() const`

**作用与语义：**

返回画师路径当前设置的填充规则。

### `QPainterPath QPainterPath::intersected(const QPainterPath &p) const`

**作用与语义：**

返回一条路径，该路径的填充面积与`p`填充面积的交点。由于贝塞尔曲线交集的数值不稳定性，贝塞尔曲线可能会被扁平化为线段。

### `bool QPainterPath::intersects(const QPainterPath &p) const`

**作用与语义：**

如果当前路径在给定路径`p`相交，则返回`true`。如果当前路径包含或被`p`的任何部分包含，也返回`true`。
路径上的集合操作将路径视为区域。非封闭路径则视为隐式闭合。

### `bool QPainterPath::intersects(const QRectF &rectangle) const`

**作用与语义：**

如果给定`rectangle`中的任何点与路径相交，返回`true`;否则返回`false`。
如果构成矩形的任何线条穿越路径的一部分，或矩形的任何部分与路径包围的区域重叠，则存在交叉点。该函数尊重当前`fillRule`以确定路径内的范围。

### `[since 6.10] bool QPainterPath::isCachingEnabled() const`

**作用与语义：**

如果启用缓存，则返回 true;否则返回 false。

### `bool QPainterPath::isEmpty() const`

**作用与语义：**

如果路径中没有元素，或者唯一的元素是`MoveToElement`，返回`true`;否则返回 `false`。

### `qreal QPainterPath::length() const`

**作用与语义：**

返回当前路径的长度。

### `void QPainterPath::lineTo(const QPointF &endPoint)`

**作用与语义：**

从当前位置加上一条直线到给定`endPoint`。线画完成后，当前位置更新为直线的终点。

### `void QPainterPath::lineTo(qreal x, qreal y)`

**作用与语义：**

从当前位置画一条线到点（`x`，`y`）。

### `void QPainterPath::moveTo(const QPointF &point)`

**作用与语义：**

将当前点移动到给定的`point`，隐式启动新的子路径并关闭之前的子路径。

### `void QPainterPath::moveTo(qreal x, qreal y)`

**作用与语义：**

将当前位置移动到（`x`， `y`），并开始新的子路径，隐式关闭之前的路径。

### `qreal QPainterPath::percentAtLength(qreal len) const`

**作用与语义：**

返回在指定长度的路径`len`百分比。
注意，与其他百分比方法类似，如果路径中存在曲线，百分比测量对长度不是线性的。当存在曲线时，百分比参数映射到贝塞尔方程的t参数。

### `QPointF QPainterPath::pointAtPercent(qreal t) const`

**作用与语义：**

返回当前路径`t`百分比的点。参数`t`必须介于0和1之间。
注意，与其他百分比方法类似，如果路径中存在曲线，百分比测量对长度不是线性的。当存在曲线时，百分比参数映射到贝塞尔方程的t参数。

### `void QPainterPath::quadTo(const QPointF &c, const QPointF &endPoint)`

**作用与语义：**

在当前位置与给定`endPoint`之间添加一条二次贝塞尔曲线，控制点由`c`指定。
曲线加入后，当前点会被更新为曲线的终点。

### `void QPainterPath::quadTo(qreal cx, qreal cy, qreal endPointX, qreal endPointY)`

**作用与语义：**

在当前点与端点（`endPointX`， `endPointY`）之间添加一条二次贝塞尔曲线，控制点由（`cx`， `cy`）指定。

### `void QPainterPath::reserve(int size)`

**作用与语义：**

在`QPainterPath`的内部内存中保留一定数量的元素。
尝试为至少`size`个元素分配内存。

### `[since 6.10] void QPainterPath::setCachingEnabled(bool enabled)`

**作用与语义：**

根据`enabled`值启用或禁用长度缓存。
启用缓存可以加快对涉及路径长度和百分比值（如`length()`、`percentAtLength()`、`pointAtPercent()`等）的重复调用，但代价是为存储中间计算而额外占用内存。默认情况下，缓存是被禁用的。
禁用缓存会释放任何已分配的缓存存储。

### `void QPainterPath::setElementPositionAt(int index, qreal x, qreal y)`

**作用与语义：**

将索引`index`元的x和y坐标设置为`x`和`y`。

### `void QPainterPath::setFillRule(Qt::FillRule fillRule)`

**作用与语义：**

将画家路径的填充规则设定为给定的`fillRule`。Qt提供了两种填充路径的方法：
- `Qt::OddEvenFill`（默认）`: `Qt：：WindingFill'
- ``:

### `QPainterPath QPainterPath::simplified() const`

**作用与语义：**

返回该路径的简化版本。这意味着合并所有相交的子路径，返回一条无相交边的路径。连续的平行线也会被合并。简化路径始终使用默认填充规则`Qt::OddEvenFill`。由于贝塞尔曲线交集的数值不稳定性，贝塞尔曲线可能会被扁平化为线段。

### `qreal QPainterPath::slopeAtPercent(qreal t) const`

**作用与语义：**

返回路径在百分比 `t` 处的斜率。参数 `t` 必须介于 0 和 1 之间。
注意，与其他百分比方法类似，如果路径中存在曲线，百分比测量对长度不是线性的。当存在曲线时，百分比参数映射到贝塞尔方程的t参数。

### `QPainterPath QPainterPath::subtracted(const QPainterPath &p) const`

**作用与语义：**

返回一条路径，该路径是`p`的填充面积从该路径的填充面积中减去。
路径上的集合运算将视为路径面积。非闭合路径则视为隐式闭合。由于贝塞尔曲线交集的数值不稳定性，贝塞尔曲线可能会被平整成线段。

### `[noexcept] void QPainterPath::swap(QPainterPath &other)`

**作用与语义：**

将这条痛点路径与`other`互换。这个操作非常快速，从未失败过。

### `QPolygonF QPainterPath::toFillPolygon(const QTransform &matrix = QTransform()) const`

**作用与语义：**

利用`QTransform` `matrix`将路径转换为多边形，返回多边形。
多边形的创建是先将所有子路径转换为多边形，然后使用倒带技术确保可以用正确的填充规则填充重叠的子路径。
注意倒带会在多边形中插入加法线，因此填充多边形的轮廓与路径轮廓不匹配。

### `QList<QPolygonF> QPainterPath::toFillPolygons(const QTransform &matrix = QTransform()) const`

**作用与语义：**

利用`QTransform` `matrix`将路径转换为多边形列表，并返回列表。
该函数与`toFillPolygon()`函数不同之处在于它创建多个多边形。其存在是因为绘制多个小多边形通常比绘制一个大多边形更快，尽管绘制的总点数相同。
toFillPolygons() 函数与 `toSubpathPolygons()` 函数不同，它只为具有重叠边界矩形的子路径创建多边形。
与`toFillPolygon()`函数类似，该函数采用倒带技术确保重叠子路径能使用正确的填充规则填充。注意倒带会在多边形中插入加线，因此填充多边形的轮廓与路径轮廓不匹配。

### `QPainterPath QPainterPath::toReversed() const`

**作用与语义：**

创建并返回路径的反向副本。
元素的顺序被反转：如果一个`QPainterPath`通过指定顺序调用`moveTo()`、`lineTo()`和`cubicTo()`函数组成，则通过调用`cubicTo()`、`lineTo()`和`moveTo()`来组合反向的副本。

### `QList<QPolygonF> QPainterPath::toSubpathPolygons(const QTransform &matrix = QTransform()) const`

**作用与语义：**

利用`QTransform` `matrix`将路径转换为多边形列表，并返回列表。
该函数为每个子路径创建一个多边形，无论子路径是否相交（即重叠的边界矩形）。为了确保这些重叠子路径正确填充，请使用`toFillPolygons()`函数。

### `void QPainterPath::translate(qreal dx, qreal dy)`

**作用与语义：**

将路径中的所有元素平移为 （`dx`， `dy`）。

### `void QPainterPath::translate(const QPointF &offset)`

**作用与语义：**

以给定的 `offset` 平移路径上的所有元素。

### `QPainterPath QPainterPath::translated(qreal dx, qreal dy) const`

**作用与语义：**

返回路径的副本，其翻译为 （`dx`， `dy`）。

### `QPainterPath QPainterPath::translated(const QPointF &offset) const`

**作用与语义：**

返回路径的副本，并由给定的`offset`翻译出来。

### `[since 6.10] QPainterPath QPainterPath::trimmed(qreal fromFraction, qreal toFraction, qreal offset = 0) const`

**作用与语义：**

返回路径中长度分数 `fromFraction` 与 `toFraction` 之间的部分。分数的有效范围从表示路径起点的 0 到 1（表示终点）不等。分数相对于路径长度是线性的，与百分比 t 值相对。
`offset`的值会加到分数值中。如果这导致[0， 1]区间出现溢出或下溢，这些值和路径都会被包裹起来。偏移的有效范围在-1到1之间。
通过{enable caching}{`setCachingEnabled()`}来优化对该函数的反复调用。

### `QPainterPath QPainterPath::united(const QPainterPath &p) const`

**作用与语义：**

返回一条路径，该路径是该路径填充面积与`p`填充面积的并集。
路径上的集合运算将视为路径面积。非闭合路径则视为隐式闭合。由于贝塞尔曲线交集的数值不稳定性，贝塞尔曲线可能会被平整成线段。

### `bool QPainterPath::operator!=(const QPainterPath &path) const`

**作用与语义：**

如果这条画家路径与给定的 `path` 不同，返回`true`。
注意，比较路径可能需要每个元素进行比较，这对于复杂路径来说可能较慢。

### `QPainterPath QPainterPath::operator&(const QPainterPath &other) const`

**作用与语义：**

返回该路径与`other`路径的交点。

### `QPainterPath &QPainterPath::operator&=(const QPainterPath &other)`

**作用与语义：**

与 `other` 相交该路径，返回该路径的引用。

### `QPainterPath QPainterPath::operator+(const QPainterPath &other) const`

**作用与语义：**

返回该路径与`other`路径的并集。该函数等价于算符|().

### `QPainterPath &QPainterPath::operator+=(const QPainterPath &other)`

**作用与语义：**

将该路径与`other`合并，并返回对该路径的引用。这等价于算符|=()。

### `QPainterPath QPainterPath::operator-(const QPainterPath &other) const`

**作用与语义：**

从该路径的副本中减去`other`路径，并返回该副本。

### `QPainterPath &QPainterPath::operator-=(const QPainterPath &other)`

**作用与语义：**

从该路径中减去`other`，返回对该路径的引用。

### `[noexcept] QPainterPath &QPainterPath::operator=(QPainterPath &&other)`

**作用与语义：**

移动分配`other`到该`QPainterPath`实例。

### `QPainterPath &QPainterPath::operator=(const QPainterPath &path)`

**作用与语义：**

将给定的`path`分配给这条画家路径。

### `bool QPainterPath::operator==(const QPainterPath &path) const`

**作用与语义：**

如果画家路径等于给定`path`，则返回`true`。
注意，比较路径可能需要每个元素进行比较，这对于复杂路径来说可能较慢。

### `QPainterPath QPainterPath::operator|(const QPainterPath &other) const`

**作用与语义：**

返回这条路径和`other`路径的合集。

### `QPainterPath &QPainterPath::operator|=(const QPainterPath &other)`

**作用与语义：**

将该路径与`other`合并，并返回该路径的引用。

### `QDataStream &operator<<(QDataStream &stream, const QPainterPath &path)`

**作用与语义：**

将给定画家`path`写入给定`stream`，并返回对`stream`的引用。

### `QDataStream &operator>>(QDataStream &stream, QPainterPath &path)`

**作用与语义：**

读取给定`stream`的画家路径进入指定`path`，并返回对`stream`的引用。

### `class Element`

**作用与语义：**

QPainterPath：：Element 类指定子路径的位置和类型。
一旦构建`QPainterPath`对象，可以向路径添加子路径，如线条和曲线（创建`QPainterPath::LineToElement`和`QPainterPath::CurveToElement`组件）。
线条和曲线从`currentPosition()`延伸到参数传递的位置。`QPainterPath`对象的`currentPosition()`总是最后添加子路径的终点位置（或初始起点）。`moveTo()`函数可用于移动`currentPosition()`而不添加线条或曲线，从而创建`QPainterPath::MoveToElement`分量。

## 6. 深入实践与常见坑

### 生命周期和资源边界

绘制上下文必须绑定有效的 paint device，并在合法的绘制阶段使用。QWidget 上通常只在 `paintEvent()` 内创建 painter；离屏图像、打印设备和 pixmap 则有各自的设备生命周期。

### 状态和错误边界

`save()`/`restore()` 用于隔离局部状态；改变坐标系、画笔或合成模式后要么恢复，要么明确后续绘制也需要该状态。重绘请求和真正绘制是两个阶段，业务状态变化应调用 `update()`。

### 线程边界

同一个 GUI 控件的绘制在 GUI 线程完成；离屏 QImage 可以按数据所有权在后台处理，但不要让后台线程直接绘制或访问正在显示的 QWidget/QPixmap 资源。

### 最容易出现的错误

不要直接调用 paintEvent；不要在绘制函数里修改会再次触发绘制的状态；不要假定所有图像都是四字节像素；不要忘记 transform 会影响坐标和 boundingRect。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QPainterPath` 所属机制类型：二维绘制状态机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
