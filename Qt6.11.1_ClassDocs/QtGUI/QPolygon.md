# QPolygon

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QPolygon` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QPolygon>`
- 继承自：QList
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

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

### 公有函数

- `QPolygon()`
- `QPolygon(const QList<QPoint> &points)`
- `QPolygon(const QRect &rectangle, bool closed = false)`
- `QRect boundingRect() const`
- `bool containsPoint(const QPoint &point, Qt::FillRule fillRule) const`
- `QPolygon intersected(const QPolygon &r) const`
- `bool intersects(const QPolygon &p) const`
- `void point(int index, int *x, int *y) const`
- `QPoint point(int index) const`
- `void putPoints(int index, int nPoints, int firstx, int firsty, ...)`
- `void putPoints(int index, int nPoints, const QPolygon &fromPolygon, int fromIndex = 0)`
- `void setPoint(int index, int x, int y)`
- `void setPoint(int index, const QPoint &point)`
- `void setPoints(int nPoints, const int *points)`
- `void setPoints(int nPoints, int firstx, int firsty, ...)`
- `QPolygon subtracted(const QPolygon &r) const`
- `void swap(QPolygon &other)`
- `(since 6.4) QPolygonF toPolygonF() const`
- `void translate(int dx, int dy)`
- `void translate(const QPoint &offset)`
- `QPolygon translated(int dx, int dy) const`
- `QPolygon translated(const QPoint &offset) const`
- `QPolygon united(const QPolygon &r) const`
- `operator QVariant() const`

### 相关非成员函数

- `QDataStream & operator<<(QDataStream &stream, const QPolygon &polygon)`
- `QDataStream & operator>>(QDataStream &stream, QPolygon &polygon)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[constexpr noexcept] QPolygon::QPolygon()`

**作用与语义：**

构造一个无点的多边形。

### `QPolygon::QPolygon(const QList<QPoint> &points)`

**作用与语义：**

构造包含指定`points`的多边形。

### `QPolygon::QPolygon(const QRect &rectangle, bool closed = false)`

**作用与语义：**

从给定的`rectangle`构造一个多边形。如果`closed`为假，则该多边形仅包含矩形顺时针顺序的四个点，否则多边形的第五个点设为`rectangle`。topLeft()。
注意，矩形的右下角位于 （rectangle.x() rectangle.width()， rectangle.y() rectangle.height()）。

### `QRect QPolygon::boundingRect() const`

**作用与语义：**

返回多边形的边界矩形，若多边形为空则返回`QRect`（0， 0， 0， 0）。

### `bool QPolygon::containsPoint(const QPoint &point, Qt::FillRule fillRule) const`

**作用与语义：**

如果给定`point`位于指定`fillRule`内，返回`true`;否则返回`false`。

### `QPolygon QPolygon::intersected(const QPolygon &r) const`

**作用与语义：**

返回一个多边形，该多边形是该多边形与`r`的交点。
对多边形的集合操作将多边形视为面积。非闭合多边形则视为隐式闭多边形。

### `bool QPolygon::intersects(const QPolygon &p) const`

**作用与语义：**

如果当前多边形在给定多边形`p`的任意点相交，返回`true`。如果当前多边形包含或被`p`的任何部分包含，也返回`true`。
对多边形的集合操作将多边形视为面积。非闭合多边形则视为隐式闭多边形。

### `void QPolygon::point(int index, int *x, int *y) const`

**作用与语义：**

提取该点在给定`index`点的坐标，映射到*`x`和*`y`（如果它们是有效的指针）。

### `QPoint QPolygon::point(int index) const`

**作用与语义：**

返回给定`index`点。

### `void QPolygon::putPoints(int index, int nPoints, int firstx, int firsty, ...)`

**作用与语义：**

将变量参数列表中的`nPoints`点复制到给定`index`的多边形中。
点以整数序列形式表示，从`firstx`开始，然后是`firsty`，依此类推。如果多边形`index+nPoints`大于当前大小，则调整大小。
示例代码通过将多边形从1扩展到3个点，创建了一个包含三个点（4,5）、（6,7）和（8,9）的多边形：
以下代码也有相同的结果，但这里putPoints()函数是覆盖而非扩展：

**官方示例：**

```cpp
 QPolygon polygon(1);
 polygon[0] = QPoint(4, 5);
 polygon.putPoints(1, 2, 6,7, 8,9);
```

### `void QPolygon::putPoints(int index, int nPoints, const QPolygon &fromPolygon, int fromIndex = 0)`

**作用与语义：**

从指定`fromIndex`（默认为0 `fromPolygon`）中复制`nPoints`点到该多边形，从指定的`index`开始。例如：

**官方示例：**

```cpp
 QPolygon polygon1;
 polygon1.putPoints(0, 3, 1,2, 0,0, 5,6);
 // polygon1 is now the three-point polygon(1,2, 0,0, 5,6);

 QPolygon polygon2;
 polygon2.putPoints(0, 3, 4,4, 5,5, 6,6);
 // polygon2 is now (4,4, 5,5, 6,6);

 polygon1.putPoints(2, 3, polygon2);
 // polygon1 is now the five-point polygon(1,2, 0,0, 4,4, 5,5, 6,6);
```

### `void QPolygon::setPoint(int index, int x, int y)`

**作用与语义：**

将给定`index`点映射为由（`x`， `y`）指定的点。

### `void QPolygon::setPoint(int index, const QPoint &point)`

**作用与语义：**

将给定`index`点映射到给定`point`。

### `void QPolygon::setPoints(int nPoints, const int *points)`

**作用与语义：**

将多边形调整为`nPoints`，并填充给定的`points`。
示例代码创建了一个包含两个点（10， 20）和 （30， 40） 的多边形：

**官方示例：**

```cpp
 static const int points[] = { 10, 20, 30, 40 };
 QPolygon polygon;
 polygon.setPoints(2, points);
```

### `void QPolygon::setPoints(int nPoints, int firstx, int firsty, ...)`

**作用与语义：**

将多边形调整为`nPoints`，并填充变量参数列表指定的点。点以整数序列的形式给出，从`firstx`开始，然后是`firsty`，依此类推。
示例代码创建了一个包含两个点（10， 20）和 （30， 40） 的多边形：

**官方示例：**

```cpp
 QPolygon polygon;
 polygon.setPoints(2, 10, 20, 30, 40);
```

### `QPolygon QPolygon::subtracted(const QPolygon &r) const`

**作用与语义：**

返回一个多边形，`r`从该多边形中减去。
对多边形的集合操作将多边形视为面积。非闭合多边形则视为隐式闭多边形。

### `[noexcept] void QPolygon::swap(QPolygon &other)`

**作用与语义：**

将这个多边形与`other`交换。这个操作非常快，而且从未失败。

### `[since 6.4] QPolygonF QPolygon::toPolygonF() const`

**作用与语义：**

返回该多边形为具有浮点精度的多边形。

### `void QPolygon::translate(int dx, int dy)`

**作用与语义：**

将多边形中的所有点平移为 （`dx`， `dy`）。

### `void QPolygon::translate(const QPoint &offset)`

**作用与语义：**

对多边形中的所有点平移给定`offset`。

### `QPolygon QPolygon::translated(int dx, int dy) const`

**作用与语义：**

返回一个多边形的副本，平移为 （`dx`， `dy`）。

### `QPolygon QPolygon::translated(const QPoint &offset) const`

**作用与语义：**

返回一个由给定`offset`平移的多边形副本。

### `QPolygon QPolygon::united(const QPolygon &r) const`

**作用与语义：**

返回一个多边形，该多边形是该多边形与`r`的并集。
对多边形进行集合运算，将多边形视为面积，并隐式闭合多边形。

### `QPolygon::operator QVariant() const`

**作用与语义：**

返回多边形作为`QVariant`。

### `QDataStream &operator<<(QDataStream &stream, const QPolygon &polygon)`

**作用与语义：**

将给定`polygon`写入给定`stream`，并返回对流的引用。

### `QDataStream &operator>>(QDataStream &stream, QPolygon &polygon)`

**作用与语义：**

将给定`stream`中的多边形读取到给定`polygon`，并返回对该流的引用。

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

`QPolygon` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
