# QVector4D

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** `QVector4D` 是 Qt 容器类型，负责保存一组元素，并提供插入、删除、查找、遍历和容量管理。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QVector4D` 是 Qt 容器与隐式共享机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** Qt 容器负责元素的存储、访问、遍历和修改。部分容器使用隐式共享，复制容器时可能共享数据，写操作时发生 detach；这会降低按值传递成本，但也会影响迭代器、引用、指针和修改时的性能。

**适用场景：** 先选择连续序列、关联映射、哈希表还是队列，再决定按索引、迭代器或范围遍历；批量修改时预留容量并注意 detach，跨 API 传值时确认元素类型和所有权。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要在容器修改后继续使用旧迭代器；不要在范围 for 中改变会导致迭代器失效的容器；不要误以为隐式共享等于线程安全；不要忽略 QHash/QMap/QList 的顺序和复杂度差异。

## 2. 依赖与对象关系

- 头文件：`#include <QVector4D>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

Qt 容器负责元素的存储、访问、遍历和修改。部分容器使用隐式共享，复制容器时可能共享数据，写操作时发生 detach；这会降低按值传递成本，但也会影响迭代器、引用、指针和修改时的性能。

### 状态、生命周期和线程

**生命周期：** 容器自己管理元素存储，容器销毁后由它提供的迭代器、引用和 data 指针通常失效。修改容器可能重新分配或 detach，不能把元素地址和迭代器当成长期句柄。

**状态与结果：** 要区分空容器、容量、元素数量、查找失败和默认构造值。插入/删除可能改变索引和迭代器；关联容器还要考虑键唯一性、排序和查找复杂度。

**线程与事件循环：** 不同线程使用各自的容器副本通常安全；同一个容器一边读一边写仍需要同步，即使底层采用隐式共享也不会自动解决数据竞争。

## 3. 直接使用

先选择连续序列、关联映射、哈希表还是队列，再决定按索引、迭代器或范围遍历；批量修改时预留容量并注意 detach，跨 API 传值时确认元素类型和所有权。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

```cpp
#include <QList>

QList<int> values{1, 2, 3};
values.append(4);
for (const int value : values) {
    // 使用 value
}
```
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QVector4D()`
- `QVector4D(QPoint point)`
- `QVector4D(QPointF point)`
- `QVector4D(QVector2D vector)`
- `QVector4D(QVector3D vector)`
- `QVector4D(QVector3D vector, float wpos)`
- `QVector4D(QVector2D vector, float zpos, float wpos)`
- `QVector4D(float xpos, float ypos, float zpos, float wpos)`
- `bool isNull() const`
- `float length() const`
- `float lengthSquared() const`
- `void normalize()`
- `QVector4D normalized() const`
- `void setW(float w)`
- `void setX(float x)`
- `void setY(float y)`
- `void setZ(float z)`
- `QPoint toPoint() const`
- `QPointF toPointF() const`
- `QVector2D toVector2D() const`
- `QVector2D toVector2DAffine() const`
- `QVector3D toVector3D() const`
- `QVector3D toVector3DAffine() const`
- `float w() const`
- `float x() const`
- `float y() const`
- `float z() const`
- `operator QVariant() const`
- `QVector4D & operator*=(QVector4D vector)`
- `QVector4D & operator*=(float factor)`
- `QVector4D & operator+=(QVector4D vector)`
- `QVector4D & operator-=(QVector4D vector)`
- `QVector4D & operator/=(QVector4D vector)`
- `QVector4D & operator/=(float divisor)`
- `float & operator[](int i)`
- `float operator[](int i) const`

### 静态公有成员

- `float dotProduct(QVector4D v1, QVector4D v2)`

### 相关非成员函数

- `bool qFuzzyCompare(QVector4D v1, QVector4D v2)`
- `bool operator!=(QVector4D v1, QVector4D v2)`
- `QVector4D operator*(QVector4D v1, QVector4D v2)`
- `QVector4D operator*(QVector4D vector, float factor)`
- `QVector4D operator*(float factor, QVector4D vector)`
- `QVector4D operator+(QVector4D v1, QVector4D v2)`
- `QVector4D operator-(QVector4D v1, QVector4D v2)`
- `QVector4D operator-(QVector4D vector)`
- `QVector4D operator/(QVector4D vector, QVector4D divisor)`
- `QVector4D operator/(QVector4D vector, float divisor)`
- `QDataStream & operator<<(QDataStream &stream, QVector4D vector)`
- `bool operator==(QVector4D v1, QVector4D v2)`
- `QDataStream & operator>>(QDataStream &stream, QVector4D &vector)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[constexpr noexcept] QVector4D::QVector4D()`

**作用与语义：**

构造一个零向量，即坐标为 （0， 0， 0， 0）。

### `[explicit constexpr noexcept] QVector4D::QVector4D(QPoint point)`

**作用与语义：**

从二维`point`构造一个坐标为x和y的向量，z和w坐标为0。

### `[explicit constexpr noexcept] QVector4D::QVector4D(QPointF point)`

**作用与语义：**

从二维`point`构造一个坐标为x和y的向量，z和w坐标为0。

### `[explicit constexpr noexcept] QVector4D::QVector4D(QVector2D vector)`

**作用与语义：**

从指定的二维向量构造一个四维矢量`vector`。z和w坐标设为零。

### `[explicit constexpr noexcept] QVector4D::QVector4D(QVector3D vector)`

**作用与语义：**

从指定的三维`vector`构造一个四维矢量。w 坐标设为零。

### `[constexpr noexcept] QVector4D::QVector4D(QVector3D vector, float wpos)`

**作用与语义：**

从指定的三维向量构造一个四维向量`vector`。w坐标设为`wpos`，必须是有限的。

### `[constexpr noexcept] QVector4D::QVector4D(QVector2D vector, float zpos, float wpos)`

**作用与语义：**

从指定的二维`vector`构造一个四维向量。z和w坐标分别设为`zpos`和`wpos` W，每个坐标都必须是有限的。

### `[constexpr noexcept] QVector4D::QVector4D(float xpos, float ypos, float zpos, float wpos)`

**作用与语义：**

构造一个坐标为（`xpos`、`ypos`、`zpos`、`wpos`）的向量。所有参数必须是有限的。

### `[static constexpr noexcept] float QVector4D::dotProduct(QVector4D v1, QVector4D v2)`

**作用与语义：**

返回`v1`和`v2`的点积。

### `[constexpr noexcept] bool QVector4D::isNull() const`

**作用与语义：**

如果x、y、z和w坐标设为0.0，返回`true`，否则返回`false`。

### `[noexcept] float QVector4D::length() const`

**作用与语义：**

返回向量从原点出发的长度。

### `[constexpr noexcept] float QVector4D::lengthSquared() const`

**作用与语义：**

返回向量从原点到的平方长度。这等价于向量与自身的点积。

### `[noexcept] void QVector4D::normalize()`

**作用与语义：**

在原地对当前向量进行归一化。如果该向量是零向量或向量长度非常接近1，则不会发生任何问题。

### `[noexcept] QVector4D QVector4D::normalized() const`

**作用与语义：**

返回该向量的归一化单位向量形式。
如果该向量为零，则返回一个空向量。如果向量长度非常接近1，则返回原样向量。否则返回长度为1的向量的归一化形式。

### `[constexpr noexcept] void QVector4D::setW(float w)`

**作用与语义：**

将该点的w坐标设为给定的有限`w`坐标。

### `[constexpr noexcept] void QVector4D::setX(float x)`

**作用与语义：**

将该点的x坐标设为给定的有限`x`坐标。

### `[constexpr noexcept] void QVector4D::setY(float y)`

**作用与语义：**

将该点的y坐标设为给定的有限`y`坐标。

### `[constexpr noexcept] void QVector4D::setZ(float z)`

**作用与语义：**

将该点的z坐标设为给定的有限`z`坐标。

### `[constexpr noexcept] QPoint QVector4D::toPoint() const`

**作用与语义：**

返回该四维向量的`QPoint`形式。去掉z和w坐标。x和y坐标被四舍五入为最接近的整数。

### `[constexpr noexcept] QPointF QVector4D::toPointF() const`

**作用与语义：**

返回该四维向量的 `QPointF` 形式。去掉 z 和 w 坐标。

### `[constexpr noexcept] QVector2D QVector4D::toVector2D() const`

**作用与语义：**

返回该四维矢量的二维向量形式，去除z和w坐标。

### `[constexpr noexcept] QVector2D QVector4D::toVector2DAffine() const`

**作用与语义：**

返回该四维向量的二维向量形式，将x和y坐标除以w坐标，去掉z坐标。如果w为零，返回一个零向量。

### `[constexpr noexcept] QVector3D QVector4D::toVector3D() const`

**作用与语义：**

返回该四维向量的三维向量形式，去除w坐标。

### `[constexpr noexcept] QVector3D QVector4D::toVector3DAffine() const`

**作用与语义：**

返回该四维向量的三维向量形式，将x、y和z坐标除以w坐标。如果w为零，返回零向量。

### `[constexpr noexcept] float QVector4D::w() const`

**作用与语义：**

返回该点的 w 坐标。

### `[constexpr noexcept] float QVector4D::x() const`

**作用与语义：**

返回该点的 x 坐标。

### `[constexpr noexcept] float QVector4D::y() const`

**作用与语义：**

返回该点的y坐标。

### `[constexpr noexcept] float QVector4D::z() const`

**作用与语义：**

返回该点的 z 坐标。

### `QVector4D::operator QVariant() const`

**作用与语义：**

返回四维矢量作为`QVariant`。

### `[constexpr noexcept] QVector4D &QVector4D::operator*=(QVector4D vector)`

**作用与语义：**

将该向量的每个分量乘以`vector`对应的分量，返回该向量的引用。

### `[constexpr noexcept] QVector4D &QVector4D::operator*=(float factor)`

**作用与语义：**

将该向量的坐标乘以给定的有限向量`factor`，返回对该向量的引用。

### `[constexpr noexcept] QVector4D &QVector4D::operator+=(QVector4D vector)`

**作用与语义：**

将给定`vector`相加到该向量上，并返回对该向量的引用。

### `[constexpr noexcept] QVector4D &QVector4D::operator-=(QVector4D vector)`

**作用与语义：**

从该向量中减去给定`vector`，返回对该向量的引用。

### `[constexpr] QVector4D &QVector4D::operator/=(QVector4D vector)`

**作用与语义：**

将该向量的每个分量除以`vector`对应的分量，并返回该向量的引用。
`vector`不能有任何分量为零或NaN。

### `[constexpr] QVector4D &QVector4D::operator/=(float divisor)`

**作用与语义：**

将该向量的坐标除以给定`divisor`，并返回该向量的参考。`divisor`不能是零或NaN。

### `[constexpr] float &QVector4D::operator[](int i)`

**作用与语义：**

返回向量在索引位置`i`的分量作为可修改的参考。
`i` 必须是向量中的有效指标位置（即 0 <= `i` < 4）。

### `[constexpr] float QVector4D::operator[](int i) const`

**作用与语义：**

返回向量在指标位置`i`的分量。
`i` 必须是向量中的有效指标位置（即 0 <= `i` < 4）。

### `[noexcept] bool qFuzzyCompare(QVector4D v1, QVector4D v2)`

**作用与语义：**

如果`v1`和`v2`相等，返回`true`，允许浮点比较产生小模糊因子;否则为假。

### `[constexpr noexcept] bool operator!=(QVector4D v1, QVector4D v2)`

**作用与语义：**

如果 `v1` 不等于 `v2`，则返回 `true`;否则返回 `false`。该算符使用精确浮点比较。

### `[constexpr noexcept] QVector4D operator*(QVector4D v1, QVector4D v2)`

**作用与语义：**

返回由 `v1` 中的每个分量乘以对应的分量形成的 `QVector4D` 对象`v2`。
注意：这在任何意义上都不是`v1`和`v2`的叉积。（其分量加起来就是`v1`和`v2`的点积。）。

### `[constexpr noexcept] QVector4D operator*(QVector4D vector, float factor)`

**作用与语义：**

返回给定`vector`的副本，乘以给定`factor`。

### `[constexpr noexcept] QVector4D operator*(float factor, QVector4D vector)`

**作用与语义：**

返回给定`vector`的副本，乘以给定`factor`。

### `[constexpr noexcept] QVector4D operator+(QVector4D v1, QVector4D v2)`

**作用与语义：**

返回一个`QVector4D`对象，该对象是给定向量 `v1` 和 `v2` 的和;每个分量单独相加。

### `[constexpr noexcept] QVector4D operator-(QVector4D v1, QVector4D v2)`

**作用与语义：**

返回一个`QVector4D`对象，由`v1`中减去`v2`;每个分量单独相减。

### `[constexpr noexcept] QVector4D operator-(QVector4D vector)`

**作用与语义：**

返回一个`QVector4D`对象，该对象通过改变给定`vector`的三个分量的符号构成。
相当于`QVector4D(0,0,0,0) - vector`。

### `[constexpr] QVector4D operator/(QVector4D vector, QVector4D divisor)`

**作用与语义：**

返回由给定`vector`的每个分量除以给定`divisor`对应分量所形成的`QVector4D`对象。
`divisor`不能有任何零或NaN的分量。

### `[constexpr] QVector4D operator/(QVector4D vector, float divisor)`

**作用与语义：**

返回由给定`vector`的每个分量除以给定`divisor`所形成的`QVector4D`对象。
`divisor`不能是零，也不能是NaN。

### `QDataStream &operator<<(QDataStream &stream, QVector4D vector)`

**作用与语义：**

将给定的`vector`写入给定的`stream`，并返回对流的引用。

### `[constexpr noexcept] bool operator==(QVector4D v1, QVector4D v2)`

**作用与语义：**

如果`v1`等于`v2`，则返回`true`;否则返回`false`。该算符使用精确浮点比较。

### `QDataStream &operator>>(QDataStream &stream, QVector4D &vector)`

**作用与语义：**

将给定`stream`的四维向量读取到给定的`vector`并返回对流的引用。

## 6. 深入实践与常见坑

### 生命周期和资源边界

容器自己管理元素存储，容器销毁后由它提供的迭代器、引用和 data 指针通常失效。修改容器可能重新分配或 detach，不能把元素地址和迭代器当成长期句柄。

### 状态和错误边界

要区分空容器、容量、元素数量、查找失败和默认构造值。插入/删除可能改变索引和迭代器；关联容器还要考虑键唯一性、排序和查找复杂度。

### 线程边界

不同线程使用各自的容器副本通常安全；同一个容器一边读一边写仍需要同步，即使底层采用隐式共享也不会自动解决数据竞争。

### 最容易出现的错误

不要在容器修改后继续使用旧迭代器；不要在范围 for 中改变会导致迭代器失效的容器；不要误以为隐式共享等于线程安全；不要忽略 QHash/QMap/QList 的顺序和复杂度差异。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QVector4D` 所属机制类型：Qt 容器与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
