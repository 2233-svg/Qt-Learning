# QRect

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 整数矩形类型，用于表示位置与尺寸，并支持边缘、交集、并集和坐标计算。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QRect`：整数矩形类型，用于表示位置与尺寸，并支持边缘、交集、并集和坐标计算。

**内部模型：** 这类类型通常可以按值传递、复制和返回。许多 Qt 容器、字符串和图像采用隐式共享：复制时共享数据，发生写操作时才 detach。这样便于 API 传值，但获取原始指针或长期持有引用时必须考虑对象修改和生命周期。

**适用场景：** 先确认值的有效性和表示格式，再调用查询、转换或修改 API；处理文本时区分 Unicode 和字节编码，处理图像时确认 format，处理 URL/路径时使用 Qt 的解析 API 而不是手写字符串规则。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要把空值当成业务成功；不要保存临时对象的内部指针；不要把 QString 当二进制缓冲区；不要假定隐式共享让并发写入自动安全。

## 2. 依赖与对象关系

- 头文件：`#include <QRect>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

这类类型通常可以按值传递、复制和返回。许多 Qt 容器、字符串和图像采用隐式共享：复制时共享数据，发生写操作时才 detach。这样便于 API 传值，但获取原始指针或长期持有引用时必须考虑对象修改和生命周期。

### 状态、生命周期和线程

**生命周期：** 值对象由作用域、容器或调用者管理，不使用 parent 和 deleteLater。跨线程传递副本通常比传递 QObject 安全，但共享数据在写入时仍可能发生复制，性能和内存峰值要结合数据规模判断。

**状态与结果：** 重点区分空值、无效值、默认值和已初始化值。例如空字符串、空 URL、null 图像和无效索引不一定表示同一件事；转换函数的失败结果要通过对应的状态查询确认。

**线程与事件循环：** 值类型本身通常可以复制后跨线程传递；不要把 data()/bits()/constData() 得到的指针当成跨线程长期有效的所有权。大对象频繁写入会触发 detach，应避免不必要的复制和格式转换。

## 3. 直接使用

先确认值的有效性和表示格式，再调用查询、转换或修改 API；处理文本时区分 Unicode 和字节编码，处理图像时确认 format，处理 URL/路径时使用 Qt 的解析 API 而不是手写字符串规则。 使用时通常按这个过程组织：构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QRect()`
- `QRect(const QPoint &topLeft, const QPoint &bottomRight)`
- `QRect(const QPoint &topLeft, const QSize &size)`
- `QRect(int x, int y, int width, int height)`
- `void adjust(int dx1, int dy1, int dx2, int dy2)`
- `QRect adjusted(int dx1, int dy1, int dx2, int dy2) const`
- `int bottom() const`
- `QPoint bottomLeft() const`
- `QPoint bottomRight() const`
- `QPoint center() const`
- `bool contains(const QPoint &point, bool proper = false) const`
- `bool contains(const QRect &rectangle, bool proper = false) const`
- `bool contains(int x, int y) const`
- `bool contains(int x, int y, bool proper) const`
- `void getCoords(int *x1, int *y1, int *x2, int *y2) const`
- `void getRect(int *x, int *y, int *width, int *height) const`
- `int height() const`
- `QRect intersected(const QRect &rectangle) const`
- `bool intersects(const QRect &rectangle) const`
- `bool isEmpty() const`
- `bool isNull() const`
- `bool isValid() const`
- `int left() const`
- `QRect marginsAdded(const QMargins &margins) const`
- `QRect marginsRemoved(const QMargins &margins) const`
- `void moveBottom(int y)`
- `void moveBottomLeft(const QPoint &position)`
- `void moveBottomRight(const QPoint &position)`
- `void moveCenter(const QPoint &position)`
- `void moveLeft(int x)`
- `void moveRight(int x)`
- `void moveTo(const QPoint &position)`
- `void moveTo(int x, int y)`
- `void moveTop(int y)`
- `void moveTopLeft(const QPoint &position)`
- `void moveTopRight(const QPoint &position)`
- `QRect normalized() const`
- `int right() const`
- `void setBottom(int y)`
- `void setBottomLeft(const QPoint &position)`
- `void setBottomRight(const QPoint &position)`
- `void setCoords(int x1, int y1, int x2, int y2)`
- `void setHeight(int height)`
- `void setLeft(int x)`
- `void setRect(int x, int y, int width, int height)`
- `void setRight(int x)`
- `void setSize(const QSize &size)`
- `void setTop(int y)`
- `void setTopLeft(const QPoint &position)`
- `void setTopRight(const QPoint &position)`
- `void setWidth(int width)`
- `void setX(int x)`
- `void setY(int y)`
- `QSize size() const`
- `CGRect toCGRect() const`
- `(since 6.4) QRectF toRectF() const`
- `int top() const`
- `QPoint topLeft() const`
- `QPoint topRight() const`
- `void translate(int dx, int dy)`
- `void translate(const QPoint &offset)`
- `QRect translated(int dx, int dy) const`
- `QRect translated(const QPoint &offset) const`
- `QRect transposed() const`
- `QRect united(const QRect &rectangle) const`
- `int width() const`
- `int x() const`
- `int y() const`
- `QRect operator&(const QRect &rectangle) const`
- `QRect & operator&=(const QRect &rectangle)`
- `QRect & operator+=(const QMargins &margins)`
- `QRect & operator-=(const QMargins &margins)`
- `QRect operator|(const QRect &rectangle) const`
- `QRect & operator|=(const QRect &rectangle)`

### 静态公有成员

- `(since 6.0) QRect span(const QPoint &p1, const QPoint &p2)`

### 相关非成员函数

- `bool operator!=(const QRect &lhs, const QRect &rhs)`
- `QRect operator+(const QMargins &margins, const QRect &rectangle)`
- `QRect operator+(const QRect &rectangle, const QMargins &margins)`
- `QRect operator-(const QRect &lhs, const QMargins &rhs)`
- `QDataStream & operator<<(QDataStream &stream, const QRect &rectangle)`
- `bool operator==(const QRect &lhs, const QRect &rhs)`
- `QDataStream & operator>>(QDataStream &stream, QRect &rectangle)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[constexpr noexcept] QRect::QRect()`

**作用与语义：**

构造一个零矩形。

### `[constexpr noexcept] QRect::QRect(const QPoint &topLeft, const QPoint &bottomRight)`

**作用与语义：**

构造一个包含给定`topLeft`和`bottomRight`角的矩形，两者都包含在内。
如果`bottomRight`比`topLeft`高且偏左，则定义的矩形不包含角。
注意：为确保无论相对顺序如何都包含两点，请使用`span()`。

### `[constexpr noexcept] QRect::QRect(const QPoint &topLeft, const QSize &size)`

**作用与语义：**

构造一个矩形，`topLeft`角和`size`。

### `[constexpr noexcept] QRect::QRect(int x, int y, int width, int height)`

**作用与语义：**

构造一个矩形，左上角为（`x`， `y`），给定的`width`和`height`。

### `[constexpr noexcept] void QRect::adjust(int dx1, int dy1, int dx2, int dy2)`

**作用与语义：**

分别在矩形的现有坐标上添加`dx1`、`dy1`、`dx2`和`dy2`。

### `[constexpr noexcept] QRect QRect::adjusted(int dx1, int dy1, int dx2, int dy2) const`

**作用与语义：**

返回一个新的矩形，分别在该矩形的现有坐标上添加了`dx1`、`dy1`、`dx2`和`dy2`。

### `[constexpr noexcept] int QRect::bottom() const`

**作用与语义：**

返回矩形底部边缘的y坐标。
注意，出于历史原因，该函数返回`top()` `height()` - 1;使用`y()` `height()`来检索真实的y坐标。

### `[constexpr noexcept] QPoint QRect::bottomLeft() const`

**作用与语义：**

返回矩形左下角的位置。注意，出于历史原因，该函数返回`QPoint`（`left()`， `top()` `height()` - 1）。

### `[constexpr noexcept] QPoint QRect::bottomRight() const`

**作用与语义：**

返回矩形右下角的位置。
注意，出于历史原因，该函数返回 `QPoint`（`left()` `width()` -1， `top()` `height()` - 1）。

### `[constexpr noexcept] QPoint QRect::center() const`

**作用与语义：**

返回矩形的中心点。

### `[noexcept] bool QRect::contains(const QPoint &point, bool proper = false) const`

**作用与语义：**

如果给定`point`在矩形的内侧或边缘，则返回`true`，否则返回`false`。如果`proper`为真，该函数只在给定`point`位于矩形内（即不在边缘）时返回`true`。

### `[noexcept] bool QRect::contains(const QRect &rectangle, bool proper = false) const`

**作用与语义：**

如果给定`rectangle`位于该矩形内，则返回`true`。否则返回`false`。如果`proper`为真，该函数仅在`rectangle`完全位于该矩形内（非边缘）时返回`true`。

### `[noexcept] bool QRect::contains(int x, int y) const`

**作用与语义：**

如果点（`x`， `y`）位于该矩形内，返回`true`，否则返回`false`。

### `[noexcept] bool QRect::contains(int x, int y, bool proper) const`

**作用与语义：**

如果点（`x`，`y`）位于矩形内侧或边缘，返回`true`，否则返回`false`。如果`proper`为真，该函数仅在点完全位于矩形内部（不在边缘）时返回`true`。

### `[constexpr] void QRect::getCoords(int *x1, int *y1, int *x2, int *y2) const`

**作用与语义：**

提取矩形左上角的位置为*`x1`和*`y1`，右下角为*`x2`和*`y2`。

### `[constexpr] void QRect::getRect(int *x, int *y, int *width, int *height) const`

**作用与语义：**

提取矩形左上角的位置为*`x`和*`y`，其尺寸为*`width`和*`height`。

### `[constexpr noexcept] int QRect::height() const`

**作用与语义：**

返回矩形的高度。

### `[noexcept] QRect QRect::intersected(const QRect &rectangle) const`

**作用与语义：**

返回该矩形与给定`rectangle`的交集。注意`r.intersected(s)`等价于`r & s`。

### `[noexcept] bool QRect::intersects(const QRect &rectangle) const`

**作用与语义：**

如果该矩形与给定`rectangle`相交（即至少有一个像素在两个矩形内），返回`true`，否则返回`false`。
交叉矩形可以用`intersected()`函数检索。

### `[constexpr noexcept] bool QRect::isEmpty() const`

**作用与语义：**

如果矩形为空，返回`true`，否则返回`false`。
空矩形有`left()` > `right()`或`top()` > `bottom()`。空矩形不成立（即 isEmpty() == ！`isValid()`）。
使用`normalized()`函数获取一个角互换的矩形。

### `[constexpr noexcept] bool QRect::isNull() const`

**作用与语义：**

如果矩形是空矩形，返回`true`，否则返回`false`。
空矩形的宽度和高度均为0（即`right()` == `left()` - 1 和 `bottom()` == `top()` - 1）。空矩形也是空的，因此不成立。

### `[constexpr noexcept] bool QRect::isValid() const`

**作用与语义：**

如果矩形有效，返回`true`，否则返回`false`。
有效的矩形具有 `left()` <= `right()`，`top()` <= `bottom()`。注意，对于无效矩形，不定义像交集这样的非平凡运算。有效的矩形不是空的（即 isValid() == ！`isEmpty()`）。

### `[constexpr noexcept] int QRect::left() const`

**作用与语义：**

返回矩形左边的x坐标。等价于`x()`。

### `[constexpr noexcept] QRect QRect::marginsAdded(const QMargins &margins) const`

**作用与语义：**

返回由`margins`长大的矩形。

### `[constexpr noexcept] QRect QRect::marginsRemoved(const QMargins &margins) const`

**作用与语义：**

去除矩形上的 `margins`，使其缩小。

### `[constexpr noexcept] void QRect::moveBottom(int y)`

**作用与语义：**

垂直移动矩形，使矩形的底部边缘保持在给定的`y`坐标处。矩形的大小保持不变。

### `[constexpr noexcept] void QRect::moveBottomLeft(const QPoint &position)`

**作用与语义：**

移动矩形，左下角保持在指定`position`。矩形大小不变。

### `[constexpr noexcept] void QRect::moveBottomRight(const QPoint &position)`

**作用与语义：**

移动矩形，右下角保持给定`position`。矩形大小保持不变。

### `[constexpr noexcept] void QRect::moveCenter(const QPoint &position)`

**作用与语义：**

移动矩形，中心点保持在给定`position`。矩形大小不变。

### `[constexpr noexcept] void QRect::moveLeft(int x)`

**作用与语义：**

将矩形水平移动，矩形的左边保持在给定的`x`坐标处。矩形的大小保持不变。

### `[constexpr noexcept] void QRect::moveRight(int x)`

**作用与语义：**

将矩形水平移动，矩形的右边保持在给定的`x`坐标处。矩形的大小保持不变。

### `[constexpr noexcept] void QRect::moveTo(const QPoint &position)`

**作用与语义：**

移动矩形，左上角停留在给定`position`。

### `[constexpr noexcept] void QRect::moveTo(int x, int y)`

**作用与语义：**

移动矩形，左上角保持在指定位置（`x`，`y`）。矩形大小不变。

### `[constexpr noexcept] void QRect::moveTop(int y)`

**作用与语义：**

垂直移动矩形，矩形的顶边保持在给定的`y`坐标处。矩形的大小保持不变。

### `[constexpr noexcept] void QRect::moveTopLeft(const QPoint &position)`

**作用与语义：**

移动矩形，左上角保持给定`position`。矩形大小不变。

### `[constexpr noexcept] void QRect::moveTopRight(const QPoint &position)`

**作用与语义：**

移动矩形，将右上角留在给定`position`。矩形大小不变。

### `[noexcept] QRect QRect::normalized() const`

**作用与语义：**

返回一个归一化的矩形;即宽度和高度均为非负的矩形。
如果`width()` <0，函数交换左角和右角，`height()` <0时交换上下角。角块同时从非包含变为包含。

### `[constexpr noexcept] int QRect::right() const`

**作用与语义：**

返回矩形右边的x坐标。
注意，出于历史原因，该函数返回`left()` `width()` - 1;使用`x()` `width()`来检索真实的x坐标。

### `[constexpr noexcept] void QRect::setBottom(int y)`

**作用与语义：**

将矩形的底边设置为给定的`y`坐标。可以改变高度，但绝不会改变矩形的上边。

### `[constexpr noexcept] void QRect::setBottomLeft(const QPoint &position)`

**作用与语义：**

将矩形左下角设置为给定的`position`。可以改变大小，但永远不会改变矩形的右上角。

### `[constexpr noexcept] void QRect::setBottomRight(const QPoint &position)`

**作用与语义：**

将矩形的右下角设置为给定的`position`。可以改变大小，但永远不会改变矩形的左上角。

### `[constexpr noexcept] void QRect::setCoords(int x1, int y1, int x2, int y2)`

**作用与语义：**

将矩形左上角的坐标设为（`x1`， `y1`），将右下角的坐标设为（`x2`， `y2`）。

### `[constexpr noexcept] void QRect::setHeight(int height)`

**作用与语义：**

将矩形的高度设置为给定的`height`。底部边缘被更改，但顶部边缘不会。

### `[constexpr noexcept] void QRect::setLeft(int x)`

**作用与语义：**

将矩形的左边设为给定的`x`坐标。可以改变宽度，但永远不会改变矩形的右边。
相当于`setX()`。

### `[constexpr noexcept] void QRect::setRect(int x, int y, int width, int height)`

**作用与语义：**

将矩形左上角的坐标设置为（`x`， `y`），其大小为给定的`width`和`height`。

### `[constexpr noexcept] void QRect::setRight(int x)`

**作用与语义：**

将矩形的右边设置为给定的`x`坐标。可以改变宽度，但永远不会改变矩形的左边。

### `[constexpr noexcept] void QRect::setSize(const QSize &size)`

**作用与语义：**

将矩形的大小设置为给定的`size`。左上角不移动。

### `[constexpr noexcept] void QRect::setTop(int y)`

**作用与语义：**

将矩形的上边设置为给定的`y`坐标。可以改变高度，但永远不会改变矩形的下边。
相当于`setY()`。

### `[constexpr noexcept] void QRect::setTopLeft(const QPoint &position)`

**作用与语义：**

将矩形的左上角设置为给定的`position`。可以改变大小，但永远不会改变矩形的右下角。

### `[constexpr noexcept] void QRect::setTopRight(const QPoint &position)`

**作用与语义：**

将矩形右上角设置为给定的`position`。可以改变大小，但永远不会改变矩形的左下角。

### `[constexpr noexcept] void QRect::setWidth(int width)`

**作用与语义：**

将矩形的宽度设置为给定的`width`。右边被更改，但左边没有变化。

### `[constexpr noexcept] void QRect::setX(int x)`

**作用与语义：**

将矩形的左边设置为给定的`x`坐标。可以改变宽度，但永远不会改变矩形的右边。
相当于`setLeft()`。

### `[constexpr noexcept] void QRect::setY(int y)`

**作用与语义：**

将矩形的上边设置为给定的`y`坐标。可以改变高度，但永远不会改变矩形的下边。
相当于`setTop()`。

### `[constexpr noexcept] QSize QRect::size() const`

**作用与语义：**

返回矩形的大小。

### `[static constexpr noexcept, since 6.0] QRect QRect::span(const QPoint &p1, const QPoint &p2)`

**作用与语义：**

返回一个矩形，涵盖`p1`和`p2`两点，包括两点及中间所有点。

### `[noexcept] CGRect QRect::toCGRect() const`

**作用与语义：**

从`QRect`创建一个CGRect。

### `[constexpr noexcept, since 6.4] QRectF QRect::toRectF() const`

**作用与语义：**

将该矩形返回为具有浮点精度的矩形。
注意：该函数与`QRectF`（`QRect`）构造函数一样，保持矩形的`size()`，而非其`bottomRight()`角。

### `[constexpr noexcept] int QRect::top() const`

**作用与语义：**

返回矩形顶边的y坐标。等价于`y()`。

### `[constexpr noexcept] QPoint QRect::topLeft() const`

**作用与语义：**

返回矩形左上角的位置。

### `[constexpr noexcept] QPoint QRect::topRight() const`

**作用与语义：**

返回矩形右上角的位置。
请注意，出于历史原因，该函数返回`QPoint`（`left()` `width()` -1， `top()`）。

### `[constexpr noexcept] void QRect::translate(int dx, int dy)`

**作用与语义：**

相对于当前位置，矩形沿 x 轴移动`dx`并沿 y 轴`dy`。正值则使矩形向右和向下移动。

### `[constexpr noexcept] void QRect::translate(const QPoint &offset)`

**作用与语义：**

将矩形移动`offset`。`x()`沿x轴移动，`offset`。`y()`沿y轴移动，相对于当前位置。

### `[constexpr noexcept] QRect QRect::translated(int dx, int dy) const`

**作用与语义：**

返回矩形的副本，该矩形相对于当前位置沿x轴平移`dx`，y轴`dy`。正值则将矩形向右和向下移动。

### `[constexpr noexcept] QRect QRect::translated(const QPoint &offset) const`

**作用与语义：**

返回一个矩形的平移副本，`offset`。`x()`沿 x 轴 和 `offset`。`y()` 沿 y 轴，相对于当前位置。

### `[constexpr noexcept] QRect QRect::transposed() const`

**作用与语义：**

返回一个矩形的副本，其宽度和高度互换：

**官方示例：**

```cpp
 QRect r = {15, 51, 42, 24};
 r = r.transposed(); // r == {15, 51, 24, 42}
```

### `[noexcept] QRect QRect::united(const QRect &rectangle) const`

**作用与语义：**

返回该矩形的边界矩形和给定的`rectangle`。

### `[constexpr noexcept] int QRect::width() const`

**作用与语义：**

返回矩形的宽度。

### `[constexpr noexcept] int QRect::x() const`

**作用与语义：**

返回矩形左边的x坐标。等价于`left()`。

### `[constexpr noexcept] int QRect::y() const`

**作用与语义：**

返回矩形顶边的y坐标。等价于`top()`。

### `[noexcept] QRect QRect::operator&(const QRect &rectangle) const`

**作用与语义：**

返回该矩形与给定`rectangle`的交点。如果没有交集，返回一个空矩形。

### `[noexcept] QRect &QRect::operator&=(const QRect &rectangle)`

**作用与语义：**

与给定`rectangle`相交。

### `[constexpr noexcept] QRect &QRect::operator+=(const QMargins &margins)`

**作用与语义：**

将`margins`添加到矩形上，使其增长。

### `[constexpr noexcept] QRect &QRect::operator-=(const QMargins &margins)`

**作用与语义：**

返回一个`margins`缩短的矩形。

### `[noexcept] QRect QRect::operator|(const QRect &rectangle) const`

**作用与语义：**

返回该矩形的边界矩形和给定的`rectangle`。

### `[noexcept] QRect &QRect::operator|=(const QRect &rectangle)`

**作用与语义：**

将该矩形与给定`rectangle`结合。

### `[constexpr noexcept] bool operator!=(const QRect &lhs, const QRect &rhs)`

**作用与语义：**

如果矩形`lhs`和`rhs`不同，返回`true`，否则返回`false`。

### `[constexpr noexcept] QRect operator+(const QMargins &margins, const QRect &rectangle)`

**作用与语义：**

归还`margins`种的`rectangle`。

### `[constexpr noexcept] QRect operator+(const QRect &rectangle, const QMargins &margins)`

**作用与语义：**

归还`margins`种的`rectangle`。

### `[constexpr noexcept] QRect operator-(const QRect &lhs, const QMargins &rhs)`

**作用与语义：**

返回`lhs`矩形，缩小了`rhs`边距。

### `QDataStream &operator<<(QDataStream &stream, const QRect &rectangle)`

**作用与语义：**

将给定的`rectangle`写入给定的`stream`，并返回对流的引用。

### `[constexpr noexcept] bool operator==(const QRect &lhs, const QRect &rhs)`

**作用与语义：**

如果矩形`lhs`和`rhs`相等，返回`true`，否则返回`false`。

### `QDataStream &operator>>(QDataStream &stream, QRect &rectangle)`

**作用与语义：**

将给定`stream`的矩形读取到给定`rectangle`，并返回对流的引用。

## 6. 深入实践与常见坑

### 生命周期和资源边界

值对象由作用域、容器或调用者管理，不使用 parent 和 deleteLater。跨线程传递副本通常比传递 QObject 安全，但共享数据在写入时仍可能发生复制，性能和内存峰值要结合数据规模判断。

### 状态和错误边界

重点区分空值、无效值、默认值和已初始化值。例如空字符串、空 URL、null 图像和无效索引不一定表示同一件事；转换函数的失败结果要通过对应的状态查询确认。

### 线程边界

值类型本身通常可以复制后跨线程传递；不要把 data()/bits()/constData() 得到的指针当成跨线程长期有效的所有权。大对象频繁写入会触发 detach，应避免不必要的复制和格式转换。

### 最容易出现的错误

不要把空值当成业务成功；不要保存临时对象的内部指针；不要把 QString 当二进制缓冲区；不要假定隐式共享让并发写入自动安全。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QRect` 所属机制类型：Qt 值类型与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
