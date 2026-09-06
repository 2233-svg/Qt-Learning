# QRectF

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 浮点矩形类型，用于绘制、变换、碰撞和带小数的几何计算。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QRectF`：浮点矩形类型，用于绘制、变换、碰撞和带小数的几何计算。

**内部模型：** 这类类型通常可以按值传递、复制和返回。许多 Qt 容器、字符串和图像采用隐式共享：复制时共享数据，发生写操作时才 detach。这样便于 API 传值，但获取原始指针或长期持有引用时必须考虑对象修改和生命周期。

**适用场景：** 先确认值的有效性和表示格式，再调用查询、转换或修改 API；处理文本时区分 Unicode 和字节编码，处理图像时确认 format，处理 URL/路径时使用 Qt 的解析 API 而不是手写字符串规则。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要把空值当成业务成功；不要保存临时对象的内部指针；不要把 QString 当二进制缓冲区；不要假定隐式共享让并发写入自动安全。

## 2. 依赖与对象关系

- 头文件：`#include <QRectF>`
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

- `QRectF()`
- `QRectF(const QRect &rectangle)`
- `QRectF(const QPointF &topLeft, const QPointF &bottomRight)`
- `QRectF(const QPointF &topLeft, const QSizeF &size)`
- `QRectF(qreal x, qreal y, qreal width, qreal height)`
- `void adjust(qreal dx1, qreal dy1, qreal dx2, qreal dy2)`
- `QRectF adjusted(qreal dx1, qreal dy1, qreal dx2, qreal dy2) const`
- `qreal bottom() const`
- `QPointF bottomLeft() const`
- `QPointF bottomRight() const`
- `QPointF center() const`
- `bool contains(const QPointF &point) const`
- `bool contains(const QRectF &rectangle) const`
- `bool contains(qreal x, qreal y) const`
- `void getCoords(qreal *x1, qreal *y1, qreal *x2, qreal *y2) const`
- `void getRect(qreal *x, qreal *y, qreal *width, qreal *height) const`
- `qreal height() const`
- `QRectF intersected(const QRectF &rectangle) const`
- `bool intersects(const QRectF &rectangle) const`
- `bool isEmpty() const`
- `bool isNull() const`
- `bool isValid() const`
- `qreal left() const`
- `QRectF marginsAdded(const QMarginsF &margins) const`
- `QRectF marginsRemoved(const QMarginsF &margins) const`
- `void moveBottom(qreal y)`
- `void moveBottomLeft(const QPointF &position)`
- `void moveBottomRight(const QPointF &position)`
- `void moveCenter(const QPointF &position)`
- `void moveLeft(qreal x)`
- `void moveRight(qreal x)`
- `void moveTo(qreal x, qreal y)`
- `void moveTo(const QPointF &position)`
- `void moveTop(qreal y)`
- `void moveTopLeft(const QPointF &position)`
- `void moveTopRight(const QPointF &position)`
- `QRectF normalized() const`
- `qreal right() const`
- `void setBottom(qreal y)`
- `void setBottomLeft(const QPointF &position)`
- `void setBottomRight(const QPointF &position)`
- `void setCoords(qreal x1, qreal y1, qreal x2, qreal y2)`
- `void setHeight(qreal height)`
- `void setLeft(qreal x)`
- `void setRect(qreal x, qreal y, qreal width, qreal height)`
- `void setRight(qreal x)`
- `void setSize(const QSizeF &size)`
- `void setTop(qreal y)`
- `void setTopLeft(const QPointF &position)`
- `void setTopRight(const QPointF &position)`
- `void setWidth(qreal width)`
- `void setX(qreal x)`
- `void setY(qreal y)`
- `QSizeF size() const`
- `QRect toAlignedRect() const`
- `CGRect toCGRect() const`
- `(since 6.5) emscripten::val toDOMRect() const`
- `QRect toRect() const`
- `qreal top() const`
- `QPointF topLeft() const`
- `QPointF topRight() const`
- `void translate(qreal dx, qreal dy)`
- `void translate(const QPointF &offset)`
- `QRectF translated(qreal dx, qreal dy) const`
- `QRectF translated(const QPointF &offset) const`
- `QRectF transposed() const`
- `QRectF united(const QRectF &rectangle) const`
- `qreal width() const`
- `qreal x() const`
- `qreal y() const`
- `QRectF operator&(const QRectF &rectangle) const`
- `QRectF & operator&=(const QRectF &rectangle)`
- `QRectF & operator+=(const QMarginsF &margins)`
- `QRectF & operator-=(const QMarginsF &margins)`
- `QRectF operator|(const QRectF &rectangle) const`
- `QRectF & operator|=(const QRectF &rectangle)`

### 静态公有成员

- `QRectF fromCGRect(CGRect rect)`
- `(since 6.5) QRectF fromDOMRect(emscripten::val domRect)`

### 相关非成员函数

- `(since 6.8) bool qFuzzyCompare(const QRectF &lhs, const QRectF &rhs)`
- `(since 6.8) bool qFuzzyIsNull(const QRectF &rect)`
- `bool operator!=(const QRectF &lhs, const QRectF &rhs)`
- `QRectF operator+(const QMarginsF &lhs, const QRectF &rhs)`
- `QRectF operator+(const QRectF &lhs, const QMarginsF &rhs)`
- `QRectF operator-(const QRectF &lhs, const QMarginsF &rhs)`
- `QDataStream & operator<<(QDataStream &stream, const QRectF &rectangle)`
- `bool operator==(const QRectF &lhs, const QRectF &rhs)`
- `QDataStream & operator>>(QDataStream &stream, QRectF &rectangle)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[constexpr noexcept] QRectF::QRectF()`

**作用与语义：**

构造一个零矩形。

### `[constexpr noexcept] QRectF::QRectF(const QRect &rectangle)`

**作用与语义：**

从给定`QRect` `rectangle`构造一个QRectF矩形。
注意：该函数与`QRect::toRectF()`一样，保持`rectangle`的`size()`，而非其`bottomRight()`角。

### `[constexpr noexcept] QRectF::QRectF(const QPointF &topLeft, const QPointF &bottomRight)`

**作用与语义：**

构造一个具有给定`topLeft`和`bottomRight`角的矩形。

### `[constexpr noexcept] QRectF::QRectF(const QPointF &topLeft, const QSizeF &size)`

**作用与语义：**

构造一个矩形，`topLeft`角和`size`。

### `[constexpr noexcept] QRectF::QRectF(qreal x, qreal y, qreal width, qreal height)`

**作用与语义：**

构造一个矩形，左上角为（`x`， `y`），给定的`width`和`height`。所有参数必须有限。

### `[constexpr noexcept] void QRectF::adjust(qreal dx1, qreal dy1, qreal dx2, qreal dy2)`

**作用与语义：**

分别向矩形的现有坐标添加`dx1`、`dy1`、`dx2`和`dy2`。所有参数必须有限。

### `[constexpr noexcept] QRectF QRectF::adjusted(qreal dx1, qreal dy1, qreal dx2, qreal dy2) const`

**作用与语义：**

返回一个新的矩形，分别在该矩形的现有坐标上加上`dx1`、`dy1`、`dx2`和`dy2`。所有参数必须是有限的。

### `[constexpr noexcept] qreal QRectF::bottom() const`

**作用与语义：**

返回矩形底部边缘的y坐标。

### `[constexpr noexcept] QPointF QRectF::bottomLeft() const`

**作用与语义：**

返回矩形左下角的位置。

### `[constexpr noexcept] QPointF QRectF::bottomRight() const`

**作用与语义：**

返回矩形右下角的位置。

### `[constexpr noexcept] QPointF QRectF::center() const`

**作用与语义：**

返回矩形的中心点。

### `[noexcept] bool QRectF::contains(const QPointF &point) const`

**作用与语义：**

如果给定`point`位于矩形的内侧或边缘，返回`true`;否则返回`false`。

### `[noexcept] bool QRectF::contains(const QRectF &rectangle) const`

**作用与语义：**

如果给定`rectangle`在该矩形内，返回`true`;否则返回`false`。

### `[noexcept] bool QRectF::contains(qreal x, qreal y) const`

**作用与语义：**

如果点（`x`，`y`）位于矩形内侧或边缘，返回`true`;否则返回`false`。

### `[static noexcept] QRectF QRectF::fromCGRect(CGRect rect)`

**作用与语义：**

可以从CGRect `rect`创建一个`QRectF`。

### `[static, since 6.5] QRectF QRectF::fromDOMRect(emscripten::val domRect)`

**作用与语义：**

将 DOMRect （https://www.w3.org/TR/geometry-1/） `domRect`转换为 `QRectF`。如果所提供的参数不是 DOMRect，行为是未定义的。

### `[constexpr] void QRectF::getCoords(qreal *x1, qreal *y1, qreal *x2, qreal *y2) const`

**作用与语义：**

提取矩形左上角的位置为*`x1`和*`y1`，右下角为*`x2`和*`y2`。

### `[constexpr] void QRectF::getRect(qreal *x, qreal *y, qreal *width, qreal *height) const`

**作用与语义：**

提取矩形左上角的位置为*`x`和*`y`，其尺寸为*`width`和*`height`。

### `[constexpr noexcept] qreal QRectF::height() const`

**作用与语义：**

返回矩形的高度。

### `[noexcept] QRectF QRectF::intersected(const QRectF &rectangle) const`

**作用与语义：**

返回该矩形与给定`rectangle`的交集。注意`r.intersected(s)`等价于`r & s`。

### `[noexcept] bool QRectF::intersects(const QRectF &rectangle) const`

**作用与语义：**

如果该矩形与给定`rectangle`相交（即存在非空的重叠区域），返回`true`，否则返回`false`。
可以用`intersected()`函数检索该交矩形。

### `[constexpr noexcept] bool QRectF::isEmpty() const`

**作用与语义：**

如果矩形为空，返回`true`，否则返回`false`。
空矩形的 `width()` <= 0 或 `height()` <= 0。空矩形不成立（即 isEmpty() == ！`isValid()`）。
用`normalized()`函数检索一个角互换的矩形。

### `[constexpr noexcept] bool QRectF::isNull() const`

**作用与语义：**

如果矩形是空矩形，返回`true`，否则返回`false`。
零矩形的宽度和高度都设置为0。空矩形也是空的，因此不成立。

### `[constexpr noexcept] bool QRectF::isValid() const`

**作用与语义：**

如果矩形有效，返回`true`，否则返回`false`。
有效的矩形有 `width()` > 0，`height()` > 0。注意，对于无效矩形，不定义像交集这样的非平凡运算。有效的矩形不是空的（即 isValid() == ！`isEmpty()`）。

### `[constexpr noexcept] qreal QRectF::left() const`

**作用与语义：**

返回矩形左边的x坐标。等价于`x()`。

### `[constexpr noexcept] QRectF QRectF::marginsAdded(const QMarginsF &margins) const`

**作用与语义：**

返回由`margins`长大的矩形。

### `[constexpr noexcept] QRectF QRectF::marginsRemoved(const QMarginsF &margins) const`

**作用与语义：**

去除矩形上的 `margins`，使其缩小。

### `[constexpr noexcept] void QRectF::moveBottom(qreal y)`

**作用与语义：**

垂直移动矩形，使矩形的底部边缘保持在给定的有限`y`坐标处。矩形的大小保持不变。

### `[constexpr noexcept] void QRectF::moveBottomLeft(const QPointF &position)`

**作用与语义：**

移动矩形，左下角保持在指定`position`。矩形大小不变。

### `[constexpr noexcept] void QRectF::moveBottomRight(const QPointF &position)`

**作用与语义：**

移动矩形，右下角保持给定`position`。矩形大小保持不变。

### `[constexpr noexcept] void QRectF::moveCenter(const QPointF &position)`

**作用与语义：**

移动矩形，中心点保持在给定`position`。矩形大小不变。

### `[constexpr noexcept] void QRectF::moveLeft(qreal x)`

**作用与语义：**

将矩形水平移动，使矩形的左边保持在给定的有限`x`坐标处。矩形的大小保持不变。

### `[constexpr noexcept] void QRectF::moveRight(qreal x)`

**作用与语义：**

将矩形水平移动，矩形的右边保持在给定的有限`x`坐标处。矩形的大小保持不变。

### `[constexpr noexcept] void QRectF::moveTo(qreal x, qreal y)`

**作用与语义：**

移动矩形，左上角保持给定位置（`x`，`y`）。矩形大小不变。两个参数都必须有限。

### `[constexpr noexcept] void QRectF::moveTo(const QPointF &position)`

**作用与语义：**

移动矩形，左上角停留在给定`position`。

### `[constexpr noexcept] void QRectF::moveTop(qreal y)`

**作用与语义：**

垂直移动矩形，保持矩形顶直线为给定的有限`y`坐标。矩形大小保持不变。

### `[constexpr noexcept] void QRectF::moveTopLeft(const QPointF &position)`

**作用与语义：**

移动矩形，左上角保持给定`position`。矩形大小不变。

### `[constexpr noexcept] void QRectF::moveTopRight(const QPointF &position)`

**作用与语义：**

移动矩形，将右上角留在给定`position`。矩形大小不变。

### `[noexcept] QRectF QRectF::normalized() const`

**作用与语义：**

返回一个归一化的矩形;即宽度和高度均为非负的矩形。
如果`width()` <0，函数会交换左右角，如果`height()` <0，则交换上下角。

### `[constexpr noexcept] qreal QRectF::right() const`

**作用与语义：**

返回矩形右边的x坐标。

### `[constexpr noexcept] void QRectF::setBottom(qreal y)`

**作用与语义：**

将矩形的下边设为给定的有限`y`坐标。可以改变高度，但永远不会改变矩形的上边。

### `[constexpr noexcept] void QRectF::setBottomLeft(const QPointF &position)`

**作用与语义：**

将矩形左下角设置为给定的`position`。可以改变大小，但永远不会改变矩形的右上角。

### `[constexpr noexcept] void QRectF::setBottomRight(const QPointF &position)`

**作用与语义：**

将矩形的右下角设置为给定的`position`。可以改变大小，但永远不会改变矩形的左上角。

### `[constexpr noexcept] void QRectF::setCoords(qreal x1, qreal y1, qreal x2, qreal y2)`

**作用与语义：**

将矩形左上角的坐标设为（`x1`， `y1`），右下角的坐标为（`x2`， `y2`）。所有参数必须有限。

### `[constexpr noexcept] void QRectF::setHeight(qreal height)`

**作用与语义：**

将矩形的高度设置为给定的有限`height`。底部边被更改，但顶部边不会。

### `[constexpr noexcept] void QRectF::setLeft(qreal x)`

**作用与语义：**

将矩形的左边设为给定的有限`x`坐标。可以改变宽度，但永远不会改变矩形的右边。
相当于`setX()`。

### `[constexpr noexcept] void QRectF::setRect(qreal x, qreal y, qreal width, qreal height)`

**作用与语义：**

将矩形左上角的坐标设为（`x`， `y`），其大小为给定的`width`和`height`。所有参数必须有限。

### `[constexpr noexcept] void QRectF::setRight(qreal x)`

**作用与语义：**

将矩形的右边设为给定的有限`x`坐标。可以改变宽度，但永远不会改变矩形的左边。

### `[constexpr noexcept] void QRectF::setSize(const QSizeF &size)`

**作用与语义：**

将矩形的大小设置为给定的有限`size`。左上角不移动。

### `[constexpr noexcept] void QRectF::setTop(qreal y)`

**作用与语义：**

将矩形的上边设置为给定的有限`y`坐标。可以改变高度，但永远不会改变矩形的下边。
相当于`setY()`。

### `[constexpr noexcept] void QRectF::setTopLeft(const QPointF &position)`

**作用与语义：**

将矩形的左上角设置为给定的`position`。可以改变大小，但永远不会改变矩形的右下角。

### `[constexpr noexcept] void QRectF::setTopRight(const QPointF &position)`

**作用与语义：**

将矩形右上角设置为给定的`position`。可以改变大小，但永远不会改变矩形的左下角。

### `[constexpr noexcept] void QRectF::setWidth(qreal width)`

**作用与语义：**

将矩形的宽度设置为给定的有限`width`。右边变了，但左边不变。

### `[constexpr noexcept] void QRectF::setX(qreal x)`

**作用与语义：**

将矩形的左边设为给定的有限`x`坐标。可以改变宽度，但永远不会改变矩形的右边。
相当于`setLeft()`。

### `[constexpr noexcept] void QRectF::setY(qreal y)`

**作用与语义：**

将矩形的上边设置为给定的有限`y`坐标。可以改变高度，但永远不会改变矩形的下边。
相当于`setTop()`。

### `[constexpr noexcept] QSizeF QRectF::size() const`

**作用与语义：**

返回矩形的大小。

### `[noexcept] QRect QRectF::toAlignedRect() const`

**作用与语义：**

返回基于该矩形值的`QRect`，该矩形是完全包含该矩形的最小整数矩形。

### `[noexcept] CGRect QRectF::toCGRect() const`

**作用与语义：**

从`QRectF`创建一个CGRect。

### `[since 6.5] emscripten::val QRectF::toDOMRect() const`

**作用与语义：**

将该对象转换为 DOMRect（https://www.w3.org/TR/geometry-1/）。

### `[constexpr noexcept] QRect QRectF::toRect() const`

**作用与语义：**

返回基于该矩形值的`QRect`。注意返回矩形中的坐标已四舍五入至最接近的整数。

### `[constexpr noexcept] qreal QRectF::top() const`

**作用与语义：**

返回矩形顶边的y坐标。等价于`y()`。

### `[constexpr noexcept] QPointF QRectF::topLeft() const`

**作用与语义：**

返回矩形左上角的位置。

### `[constexpr noexcept] QPointF QRectF::topRight() const`

**作用与语义：**

返回矩形右上角的位置。

### `[constexpr noexcept] void QRectF::translate(qreal dx, qreal dy)`

**作用与语义：**

相对于当前位置，矩形沿x轴移动`dx`沿y轴`dy`。正值则使矩形向右和向下移动。这两个参数都必须有限。

### `[constexpr noexcept] void QRectF::translate(const QPointF &offset)`

**作用与语义：**

将矩形移动`offset`。`x()`沿x轴移动，`offset`。`y()`沿y轴移动，相对于当前位置。

### `[constexpr noexcept] QRectF QRectF::translated(qreal dx, qreal dy) const`

**作用与语义：**

返回矩形的副本，该矩形相对于当前位置沿x轴`dx`平移，y轴`dy`。正值则将矩形向右和向下移动。这两个参数都必须有限。

### `[constexpr noexcept] QRectF QRectF::translated(const QPointF &offset) const`

**作用与语义：**

返回一个矩形的平移副本，`offset`。`x()`沿 x 轴 和 `offset`。`y()` 沿 y 轴，相对于当前位置。

### `[constexpr noexcept] QRectF QRectF::transposed() const`

**作用与语义：**

返回一个矩形的副本，其宽度和高度互换：

**官方示例：**

```cpp
 QRectF r = {1.5, 5.1, 4.2, 2.4};
 r = r.transposed(); // r == {1.5, 5.1, 2.4, 4.2}
```

### `[noexcept] QRectF QRectF::united(const QRectF &rectangle) const`

**作用与语义：**

返回该矩形的边界矩形和给定的`rectangle`。

### `[constexpr noexcept] qreal QRectF::width() const`

**作用与语义：**

返回矩形的宽度。

### `[constexpr noexcept] qreal QRectF::x() const`

**作用与语义：**

返回矩形左边的x坐标。等价于`left()`。

### `[constexpr noexcept] qreal QRectF::y() const`

**作用与语义：**

返回矩形顶边的y坐标。等价于`top()`。

### `[noexcept] QRectF QRectF::operator&(const QRectF &rectangle) const`

**作用与语义：**

返回该矩形与给定`rectangle`的交点。如果没有交集，返回一个空矩形。

### `[noexcept] QRectF &QRectF::operator&=(const QRectF &rectangle)`

**作用与语义：**

与给定`rectangle`相交。

### `[constexpr noexcept] QRectF &QRectF::operator+=(const QMarginsF &margins)`

**作用与语义：**

将`margins`添加到矩形上，使其增长。

### `[constexpr noexcept] QRectF &QRectF::operator-=(const QMarginsF &margins)`

**作用与语义：**

返回一个`margins`缩短的矩形。

### `[noexcept] QRectF QRectF::operator|(const QRectF &rectangle) const`

**作用与语义：**

返回该矩形的边界矩形和给定的`rectangle`。

### `[noexcept] QRectF &QRectF::operator|=(const QRectF &rectangle)`

**作用与语义：**

将该矩形与给定`rectangle`结合。

### `[constexpr noexcept, since 6.8] bool qFuzzyCompare(const QRectF &lhs, const QRectF &rhs)`

**作用与语义：**

如果矩形`lhs`大致等于矩形`rhs`，返回`true`;否则返回`false`。

### `[constexpr noexcept, since 6.8] bool qFuzzyIsNull(const QRectF &rect)`

**作用与语义：**

如果矩形`rect`的宽度和高度都近似为零，返回`true`;否则返回`false`。

### `[constexpr noexcept] bool operator!=(const QRectF &lhs, const QRectF &rhs)`

**作用与语义：**

如果矩形`lhs`和`rhs`相差足够大，返回`true`，否则返回`false`。
警告：该函数不检查严格不等式;相反，它使用模糊比较来比较矩形的坐标。

### `[constexpr noexcept] QRectF operator+(const QMarginsF &lhs, const QRectF &rhs)`

**作用与语义：**

返回`rhs`边距增长的`lhs`矩形。

### `[constexpr noexcept] QRectF operator+(const QRectF &lhs, const QMarginsF &rhs)`

**作用与语义：**

返回`rhs`边距增长的`lhs`矩形。

### `[constexpr noexcept] QRectF operator-(const QRectF &lhs, const QMarginsF &rhs)`

**作用与语义：**

返回`lhs`矩形，缩小了`rhs`边距。

### `QDataStream &operator<<(QDataStream &stream, const QRectF &rectangle)`

**作用与语义：**

将`rectangle`写入`stream`，并返回流的引用。

### `[constexpr noexcept] bool operator==(const QRectF &lhs, const QRectF &rhs)`

**作用与语义：**

如果矩形`lhs`和`rhs`近似相等，则返回`true`，否则返回`false`。
警告：该函数不检查严格等式;而是使用模糊比较来比较矩形的坐标。

### `QDataStream &operator>>(QDataStream &stream, QRectF &rectangle)`

**作用与语义：**

从`stream`读取`rectangle`，并返回对该流的引用。

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

`QRectF` 所属机制类型：Qt 值类型与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
