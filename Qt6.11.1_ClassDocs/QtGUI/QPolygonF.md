# QPolygonF

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QPolygonF` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QPolygonF>`
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

- `QPolygonF()`
- `QPolygonF(const QList<QPointF> &points)`
- `QPolygonF(const QPolygon &polygon)`
- `QPolygonF(const QRectF &rectangle)`
- `QRectF boundingRect() const`
- `bool containsPoint(const QPointF &point, Qt::FillRule fillRule) const`
- `QPolygonF intersected(const QPolygonF &r) const`
- `bool intersects(const QPolygonF &p) const`
- `bool isClosed() const`
- `QPolygonF subtracted(const QPolygonF &r) const`
- `void swap(QPolygonF &other)`
- `QPolygon toPolygon() const`
- `void translate(const QPointF &offset)`
- `void translate(qreal dx, qreal dy)`
- `QPolygonF translated(const QPointF &offset) const`
- `QPolygonF translated(qreal dx, qreal dy) const`
- `QPolygonF united(const QPolygonF &r) const`
- `operator QVariant() const`

### 相关非成员函数

- `QDataStream & operator<<(QDataStream &stream, const QPolygonF &polygon)`
- `QDataStream & operator>>(QDataStream &stream, QPolygonF &polygon)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[constexpr noexcept] QPolygonF::QPolygonF()`

**作用与语义：**

构造一个无点的多边形。

### `QPolygonF::QPolygonF(const QList<QPointF> &points)`

**作用与语义：**

构造包含指定`points`的多边形。

### `QPolygonF::QPolygonF(const QPolygon &polygon)`

**作用与语义：**

从指定的整数基`polygon`构造一个基于浮点的多边形。

### `QPolygonF::QPolygonF(const QRectF &rectangle)`

**作用与语义：**

从指定的`rectangle`构造一个闭多边形。
该多边形包含矩形的四个顶点，顺时针顺序从左上顶点开始到结束。

### `QRectF QPolygonF::boundingRect() const`

**作用与语义：**

返回多边形的边界矩形，若多边形为空，则返回 `QRectF`（0,0,0）。

### `bool QPolygonF::containsPoint(const QPointF &point, Qt::FillRule fillRule) const`

**作用与语义：**

如果给定`point`位于指定`fillRule`内，返回`true`;否则返回`false`。

### `QPolygonF QPolygonF::intersected(const QPolygonF &r) const`

**作用与语义：**

返回一个多边形，该多边形是该多边形与`r`的交点。
对多边形的集合操作将多边形视为面积。非闭合多边形则视为隐式闭多边形。

### `bool QPolygonF::intersects(const QPolygonF &p) const`

**作用与语义：**

如果当前多边形在给定多边形`p`的任意点相交，返回`true`。如果当前多边形包含或被`p`的任何部分包含，也返回`true`。
对多边形的集合操作将多边形视为面积。非闭合多边形则视为隐式闭多边形。

### `bool QPolygonF::isClosed() const`

**作用与语义：**

如果多边形闭合，返回`true`;否则返回`false`。
如果一个多边形的起点和终点相等，则称其为闭边形。

### `QPolygonF QPolygonF::subtracted(const QPolygonF &r) const`

**作用与语义：**

返回一个多边形，`r`从该多边形中减去。
对多边形的集合操作将多边形视为面积。非闭合多边形则视为隐式闭多边形。

### `void QPolygonF::swap(QPolygonF &other)`

**作用与语义：**

将这个多边形与`other`交换。这个操作非常快，而且从未失败。

### `QPolygon QPolygonF::toPolygon() const`

**作用与语义：**

通过将每个`QPointF`转换为`QPoint`来创建并返回`QPolygon`。

### `void QPolygonF::translate(const QPointF &offset)`

**作用与语义：**

将多边形中的所有点平移为给定的`offset`。

### `void QPolygonF::translate(qreal dx, qreal dy)`

**作用与语义：**

将多边形中的所有点平移为 （`dx`， `dy`）。

### `QPolygonF QPolygonF::translated(const QPointF &offset) const`

**作用与语义：**

返回一个由给定`offset`平移的多边形副本。

### `QPolygonF QPolygonF::translated(qreal dx, qreal dy) const`

**作用与语义：**

返回一个多边形的副本，平移为 （`dx`， `dy`）。

### `QPolygonF QPolygonF::united(const QPolygonF &r) const`

**作用与语义：**

返回一个多边形，该多边形是该多边形与`r`的并集。
对多边形的集合操作将多边形视为面积。非闭合多边形则视为隐式闭多边形。

### `QPolygonF::operator QVariant() const`

**作用与语义：**

返回多边形作为`QVariant`。

### `QDataStream &operator<<(QDataStream &stream, const QPolygonF &polygon)`

**作用与语义：**

将给定`polygon`写入给定`stream`，并返回对流的引用。

### `QDataStream &operator>>(QDataStream &stream, QPolygonF &polygon)`

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

`QPolygonF` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
