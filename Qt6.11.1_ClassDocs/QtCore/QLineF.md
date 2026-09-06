# QLineF

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“LineF”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QLineF` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QLineF>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
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

### 公有类型

- `enum IntersectionType { NoIntersection, UnboundedIntersection, BoundedIntersection }`

### 公有函数

- `QLineF()`
- `QLineF(const QLine &line)`
- `QLineF(const QPointF &p1, const QPointF &p2)`
- `QLineF(qreal x1, qreal y1, qreal x2, qreal y2)`
- `QPointF p1() const`
- `QPointF p2() const`
- `qreal x1() const`
- `qreal x2() const`
- `qreal y1() const`
- `qreal y2() const`
- `qreal angle() const`
- `qreal angleTo(const QLineF &line) const`
- `QPointF center() const`
- `qreal dx() const`
- `qreal dy() const`
- `QLineF::IntersectionType intersects(const QLineF &line, QPointF *intersectionPoint = nullptr) const`
- `bool isNull() const`
- `qreal length() const`
- `QLineF normalVector() const`
- `QPointF pointAt(qreal t) const`
- `void setP1(const QPointF &p1)`
- `void setP2(const QPointF &p2)`
- `void setAngle(qreal angle)`
- `void setLength(qreal length)`
- `void setLine(qreal x1, qreal y1, qreal x2, qreal y2)`
- `void setPoints(const QPointF &p1, const QPointF &p2)`
- `QLine toLine() const`
- `void translate(const QPointF &offset)`
- `void translate(qreal dx, qreal dy)`
- `QLineF translated(const QPointF &offset) const`
- `QLineF translated(qreal dx, qreal dy) const`
- `QLineF unitVector() const`

### 静态公有成员

- `QLineF fromPolar(qreal length, qreal angle)`

### 相关非成员函数

- `(since 6.8) bool qFuzzyCompare(const QLineF &lhs, const QLineF &rhs)`
- `(since 6.8) bool qFuzzyIsNull(const QLineF &line)`
- `bool operator!=(const QLineF &lhs, const QLineF &rhs)`
- `QDataStream & operator<<(QDataStream &stream, const QLineF &line)`
- `bool operator==(const QLineF &lhs, const QLineF &rhs)`
- `QDataStream & operator>>(QDataStream &stream, QLineF &line)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QLineF::IntersectionType`

**作用与语义：**

描述两条线的交点。
- ``:
- `QLineF::UnboundedIntersection`：QLineF：：有界交点
- `QLineF::NoIntersection`：`0`;表示这些直线不相交;即它们是平行的。
- `QLineF::UnboundedIntersection`：`2`;两条直线相交，但不在它们长度定义的范围内。如果两条直线不平行，则会如此。如果交点仅在其中一条直线的起点和终点内，Intersect() 也会返回该值。
- `QLineF::BoundedIntersection`：`1`;两条线在每条线的起点和终点内相交。

### `[constexpr] QLineF::QLineF()`

**作用与语义：**

构造一条零线。

### `[constexpr] QLineF::QLineF(const QLine &line)`

**作用与语义：**

从给定的整数基`line`构造一个QLineF对象。

### `[constexpr] QLineF::QLineF(const QPointF &p1, const QPointF &p2)`

**作用与语义：**

构造一个表示`p1`与`p2`之间的直线对象。

### `[constexpr] QLineF::QLineF(qreal x1, qreal y1, qreal x2, qreal y2)`

**作用与语义：**

构造一个线对象，表示介于（`x1`， `y1`）与（`x2`， `y2`之间的直线）。

### `[constexpr] QPointF QLineF::p1() const`

**作用与语义：**

返回线路的起点。

### `[constexpr] QPointF QLineF::p2() const`

**作用与语义：**

返回线路的终点。

### `[constexpr] qreal QLineF::x1() const`

**作用与语义：**

返回该直线起点的x坐标。

### `[constexpr] qreal QLineF::x2() const`

**作用与语义：**

返回该直线终点的x坐标。

### `[constexpr] qreal QLineF::y1() const`

**作用与语义：**

返回该直线起点的y坐标。

### `[constexpr] qreal QLineF::y2() const`

**作用与语义：**

返回该直线终点的y坐标。

### `qreal QLineF::angle() const`

**作用与语义：**

返回线的角度（度数）。
返回值范围从0.0到360.0，但不包括360.0。角度从原点右侧的x轴点逆时针测量（x>0）。

### `qreal QLineF::angleTo(const QLineF &line) const`

**作用与语义：**

返回从该直线到给定`line`的角度（度数），考虑了直线的方向。如果直线不`intersect`在其范围内，则延伸直线的交点作为原点（见`QLineF::UnboundedIntersection`）。
返回的值代表你需要对这条线加上多少度，使其与给定`line`的角度相同，逆时针方向。

### `[constexpr] QPointF QLineF::center() const`

**作用与语义：**

返回该直线的中心点。这相当于0.5 * `p1()` 0.5 * `p2()`。

### `[constexpr] qreal QLineF::dx() const`

**作用与语义：**

返回直线矢量的水平分量。

### `[constexpr] qreal QLineF::dy() const`

**作用与语义：**

返回直线矢量的垂直分量。

### `[static] QLineF QLineF::fromPolar(qreal length, qreal angle)`

**作用与语义：**

返回`QLineF`，并返回给定的`length`和`angle`。
直线的第一点将位于原点上。
角度的正值表示逆时针方向，负值表示顺时针方向。零度位于3点钟方向。

### `QLineF::IntersectionType QLineF::intersects(const QLineF &line, QPointF *intersectionPoint = nullptr) const`

**作用与语义：**

返回一个值，表示该直线是否与给定`line`相交。
实际的交点被提取到`intersectionPoint`（如果指针有效）。如果直线平行，则交点未定义。

### `[constexpr] bool QLineF::isNull() const`

**作用与语义：**

如果直线没有明显的起点和终点，返回`true`;否则返回`false`。如果`qFuzzyCompare()`能在至少一个坐标中区分起点和终点，则它们被视为不同的。
注意：由于使用模糊比较，isNull() 可能返回`length()`非零的行的 `true`。

### `qreal QLineF::length() const`

**作用与语义：**

返回该行的长度。

### `[constexpr] QLineF QLineF::normalVector() const`

**作用与语义：**

返回一条垂直于该直线且起点和长度相同的直线。

### `[constexpr] QPointF QLineF::pointAt(qreal t) const`

**作用与语义：**

返回由有限参数`t`指定位置的点。函数返回 t = 0 时返回线的起点，t = 1 时返回终点。

### `void QLineF::setP1(const QPointF &p1)`

**作用与语义：**

将该线的起点设为`p1`。

### `void QLineF::setP2(const QPointF &p2)`

**作用与语义：**

将该行的终点设为`p2`。

### `void QLineF::setAngle(qreal angle)`

**作用与语义：**

将直线的角度设定为给定的`angle`（以度为单位）。这将改变直线第二点的位置，使直线具有给定的角度。
角度的正值表示逆时针方向，负值表示顺时针方向。零度位于3点钟方向。

### `void QLineF::setLength(qreal length)`

**作用与语义：**

将线的长度设置为给定的有限`length`。`QLineF` 会移动线的端点 - `p2()` - 以获得线的新长度，除非之前`length()`为零，此时不尝试缩放。

### `void QLineF::setLine(qreal x1, qreal y1, qreal x2, qreal y2)`

**作用与语义：**

将此行设定为`x1`、`y1`、`x2`、`y2`。

### `void QLineF::setPoints(const QPointF &p1, const QPointF &p2)`

**作用与语义：**

将该直线的起点设为`p1`，终点设为`p2`。

### `[constexpr] QLine QLineF::toLine() const`

**作用与语义：**

返回该行的整数副本。
注意返回的直线的起点和终点已四舍五入到最近的整数。

### `[constexpr] void QLineF::translate(const QPointF &offset)`

**作用与语义：**

按给定`offset`翻译这句话。

### `[constexpr] void QLineF::translate(qreal dx, qreal dy)`

**作用与语义：**

该直线平移为`dx`和`dy`所指定的距离。

### `[constexpr] QLineF QLineF::translated(const QPointF &offset) const`

**作用与语义：**

返回这行经给定`offset`的翻译。

### `[constexpr] QLineF QLineF::translated(qreal dx, qreal dy) const`

**作用与语义：**

返回该行，将`dx`和`dy`所指定的距离平译。

### `QLineF QLineF::unitVector() const`

**作用与语义：**

返回该直线的单位向量，即从该直线起点且长度为1.0的直线，前提是该直线非零。

### `[constexpr noexcept, since 6.8] bool qFuzzyCompare(const QLineF &lhs, const QLineF &rhs)`

**作用与语义：**

如果行`lhs`大致等于行`rhs`，返回`true`;否则返回`false`。
如果线的起点和终点大致相等，则认为它们大致相等。

### `[constexpr noexcept, since 6.8] bool qFuzzyIsNull(const QLineF &line)`

**作用与语义：**

如果`line`行的起点大致等于终点，则返回`true`;否则返回`false`。

### `[constexpr noexcept] bool operator!=(const QLineF &lhs, const QLineF &rhs)`

**作用与语义：**

如果`lhs`行与`rhs`行不相同，返回`true`。
如果一条直线的起点或终点不同，或者点的内部顺序不同，则称其与另一条直线不同。

### `QDataStream &operator<<(QDataStream &stream, const QLineF &line)`

**作用与语义：**

将给定`line`写入给定`stream`并返回流的引用。

### `[constexpr noexcept] bool operator==(const QLineF &lhs, const QLineF &rhs)`

**作用与语义：**

如果`lhs`行与`rhs`行相同，返回`true`。
如果一条直线的起点和终点相同，且点的内部顺序相同，则该直线与另一条直线相同。

### `QDataStream &operator>>(QDataStream &stream, QLineF &line)`

**作用与语义：**

读取给定`stream`的行到给定的`line`，并返回对该流的引用。

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

`QLineF` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
