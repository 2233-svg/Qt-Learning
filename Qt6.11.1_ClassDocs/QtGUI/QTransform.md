# QTransform

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QTransform` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QTransform>`
- 继承自：未在类页中列出
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

### 公有类型

- `enum TransformationType { TxNone, TxTranslate, TxScale, TxRotate, TxShear, TxProject }`

### 公有函数

- `QTransform()`
- `QTransform(qreal m11, qreal m12, qreal m21, qreal m22, qreal dx, qreal dy)`
- `QTransform(qreal m11, qreal m12, qreal m13, qreal m21, qreal m22, qreal m23, qreal m31, qreal m32, qreal m33)`
- `qreal m11() const`
- `qreal m12() const`
- `qreal m13() const`
- `qreal m21() const`
- `qreal m22() const`
- `qreal m23() const`
- `qreal m31() const`
- `qreal m32() const`
- `qreal m33() const`
- `QTransform adjoint() const`
- `qreal determinant() const`
- `qreal dx() const`
- `qreal dy() const`
- `QTransform inverted(bool *invertible = nullptr) const`
- `bool isAffine() const`
- `bool isIdentity() const`
- `bool isInvertible() const`
- `bool isRotating() const`
- `bool isScaling() const`
- `bool isTranslating() const`
- `void map(qreal x, qreal y, qreal *tx, qreal *ty) const`
- `QLine map(const QLine &l) const`
- `QLineF map(const QLineF &line) const`
- `QPainterPath map(const QPainterPath &path) const`
- `QPoint map(const QPoint &point) const`
- `QPointF map(const QPointF &p) const`
- `QPolygon map(const QPolygon &polygon) const`
- `QPolygonF map(const QPolygonF &polygon) const`
- `QRegion map(const QRegion &region) const`
- `void map(int x, int y, int *tx, int *ty) const`
- `QRectF mapRect(const QRectF &rectangle) const`
- `QRect mapRect(const QRect &rectangle) const`
- `QPolygon mapToPolygon(const QRect &rectangle) const`
- `void reset()`
- `(since 6.5) QTransform & rotate(qreal a, Qt::Axis axis, qreal distanceToPlane)`
- `QTransform & rotate(qreal a, Qt::Axis axis = Qt::ZAxis)`
- `(since 6.5) QTransform & rotateRadians(qreal a, Qt::Axis axis, qreal distanceToPlane)`
- `QTransform & rotateRadians(qreal a, Qt::Axis axis = Qt::ZAxis)`
- `QTransform & scale(qreal sx, qreal sy)`
- `void setMatrix(qreal m11, qreal m12, qreal m13, qreal m21, qreal m22, qreal m23, qreal m31, qreal m32, qreal m33)`
- `QTransform & shear(qreal sh, qreal sv)`
- `QTransform & translate(qreal dx, qreal dy)`
- `QTransform transposed() const`
- `QTransform::TransformationType type() const`
- `operator QVariant() const`
- `bool operator!=(const QTransform &matrix) const`
- `QTransform operator*(const QTransform &matrix) const`
- `QTransform & operator*=(const QTransform &matrix)`
- `QTransform & operator*=(qreal scalar)`
- `QTransform & operator+=(qreal scalar)`
- `QTransform & operator-=(qreal scalar)`
- `QTransform & operator/=(qreal scalar)`
- `QTransform & operator=(const QTransform &matrix)`
- `bool operator==(const QTransform &matrix) const`

### 静态公有成员

- `QTransform fromScale(qreal sx, qreal sy)`
- `QTransform fromTranslate(qreal dx, qreal dy)`
- `bool quadToQuad(const QPolygonF &one, const QPolygonF &two, QTransform &trans)`
- `bool quadToSquare(const QPolygonF &quad, QTransform &trans)`
- `bool squareToQuad(const QPolygonF &quad, QTransform &trans)`

### 相关非成员函数

- `bool qFuzzyCompare(const QTransform &t1, const QTransform &t2)`
- `size_t qHash(const QTransform &key, size_t seed = 0)`
- `QLine operator*(const QLine &line, const QTransform &matrix)`
- `QLineF operator*(const QLineF &line, const QTransform &matrix)`
- `QPainterPath operator*(const QPainterPath &path, const QTransform &matrix)`
- `QPoint operator*(const QPoint &point, const QTransform &matrix)`
- `QPointF operator*(const QPointF &point, const QTransform &matrix)`
- `QPolygon operator*(const QPolygon &polygon, const QTransform &matrix)`
- `QPolygonF operator*(const QPolygonF &polygon, const QTransform &matrix)`
- `QRegion operator*(const QRegion &region, const QTransform &matrix)`
- `QDataStream & operator<<(QDataStream &stream, const QTransform &matrix)`
- `QDataStream & operator>>(QDataStream &stream, QTransform &matrix)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QTransform::QTransform()`

**作用与语义：**

构造一个恒等矩阵。
除了`m11`和`m22`（指定刻度）和`m33`外，所有元素都设为零。

### `QTransform::QTransform(qreal m11, qreal m12, qreal m21, qreal m22, qreal dx, qreal dy)`

**作用与语义：**

构造包含元素`m11`、`m12`、`m21`、`m22`、`dx`和`dy`的矩阵。

### `QTransform::QTransform(qreal m11, qreal m12, qreal m13, qreal m21, qreal m22, qreal m23, qreal m31, qreal m32, qreal m33)`

**作用与语义：**

构造包含元素 `m11`、`m12`、`m13`、`m21`、`m22`、`m23`、`m31`、`m32`、`m33` 的矩阵。

### `qreal QTransform::m11() const`

**作用与语义：**

返回水平缩放因子。

### `qreal QTransform::m12() const`

**作用与语义：**

返回垂直剪切因子。

### `qreal QTransform::m13() const`

**作用与语义：**

返回水平投影因子。

### `qreal QTransform::m21() const`

**作用与语义：**

恢复水平剪切因子。

### `qreal QTransform::m22() const`

**作用与语义：**

返回垂直缩放因子。

### `qreal QTransform::m23() const`

**作用与语义：**

返回垂直投影因子。

### `qreal QTransform::m31() const`

**作用与语义：**

返回水平平移因子。

### `qreal QTransform::m32() const`

**作用与语义：**

返回垂直平移因子。

### `qreal QTransform::m33() const`

**作用与语义：**

返回除法因子。

### `QTransform QTransform::adjoint() const`

**作用与语义：**

返回该矩阵的伴随。

### `qreal QTransform::determinant() const`

**作用与语义：**

返回矩阵的行列式。

### `qreal QTransform::dx() const`

**作用与语义：**

返回水平平移因子。

### `qreal QTransform::dy() const`

**作用与语义：**

返回垂直平移因子。

### `[static] QTransform QTransform::fromScale(qreal sx, qreal sy)`

**作用与语义：**

创建一个矩阵，对应于水平和`sy`的`sx`水平缩放。这与`QTransform()`.scale（sx， sy）相同，但速度稍快。

### `[static] QTransform QTransform::fromTranslate(qreal dx, qreal dy)`

**作用与语义：**

生成一个矩阵，对应于沿 x 轴的 `dx` 平移，y 轴上的 `dy`。这与 `QTransform()`.translate（dx， dy） 相同，但速度稍快。

### `QTransform QTransform::inverted(bool *invertible = nullptr) const`

**作用与语义：**

返回该矩阵的倒置副本。
如果矩阵是奇异的（不可逆的），返回的矩阵就是单位矩阵。如果`invertible`有效（即不是0），则其值设为真（如果矩阵可逆），否则设为假。

### `bool QTransform::isAffine() const`

**作用与语义：**

如果矩阵代表仿射变换，则返回`true`，否则返回`false`。

### `bool QTransform::isIdentity() const`

**作用与语义：**

如果矩阵是单位矩阵，则返回`true`，否则返回`false`。

### `bool QTransform::isInvertible() const`

**作用与语义：**

如果矩阵可逆，返回`true`，否则返回`false`。

### `bool QTransform::isRotating() const`

**作用与语义：**

如果矩阵代表某种旋转变换，返回`true`，否则返回`false`。
注意：180度和/或360度的旋转变换被视为缩放变换。

### `bool QTransform::isScaling() const`

**作用与语义：**

如果矩阵代表缩放变换，返回`true`;否则返回`false`。

### `bool QTransform::isTranslating() const`

**作用与语义：**

如果矩阵代表平移变换，返回`true`;否则返回`false`。

### `void QTransform::map(qreal x, qreal y, qreal *tx, qreal *ty) const`

**作用与语义：**

将给定坐标`x`和`y`映射到该矩阵定义的坐标系中。所得值分别置于*`tx`和*`ty`中。
坐标通过以下公式进行变换：
点（x， y）是原始点，（x'， y'）是变换后的点。

**官方示例：**

```cpp
 x' = m11*x + m21*y + dx
 y' = m22*y + m12*x + dy
 if (!isAffine()) {
     w' = m13*x + m23*y + m33
     x' /= w'
     y' /= w'
 }
```

### `QLine QTransform::map(const QLine &l) const`

**作用与语义：**

创建并返回一个`QLineF`对象，该对象是给定线的复制品，`l`映射到该矩阵定义的坐标系中。

### `QLineF QTransform::map(const QLineF &line) const`

**作用与语义：**

创建并返回一个`QLine`对象，该对象是给定`line`的复制品，映射到该矩阵定义的坐标系中。注意，变换后的坐标已四舍五入至最近的整数。

### `QPainterPath QTransform::map(const QPainterPath &path) const`

**作用与语义：**

创建并返回一个`QPainterPath`对象，该对象是给定`path`的复制品，映射到该矩阵定义的坐标系中。

### `QPoint QTransform::map(const QPoint &point) const`

**作用与语义：**

创建并返回一个`QPoint`对象，该对象是给定`point`的复制品，映射到该矩阵定义的坐标系中。注意，变换后的坐标被四舍五入到最近的整数。

### `QPointF QTransform::map(const QPointF &p) const`

**作用与语义：**

创建并返回一个`QPointF`对象，该对象是给定点`p`的复制品，映射到由该矩阵定义的坐标系中。

### `QPolygon QTransform::map(const QPolygon &polygon) const`

**作用与语义：**

创建并返回一个`QPolygon`对象，该对象是给定`polygon`的复制品，映射到该矩阵定义的坐标系中。注意，变换后的坐标被四舍五入到最接近的整数。

### `QPolygonF QTransform::map(const QPolygonF &polygon) const`

**作用与语义：**

创建并返回一个`QPolygonF`对象，该对象是给定`polygon`的副本，映射到由该矩阵定义的坐标系中。

### `QRegion QTransform::map(const QRegion &region) const`

**作用与语义：**

创建并返回一个`QRegion`对象，该对象是给定`region`的副本，映射到该矩阵定义的坐标系中。
如果采用旋转或剪切，使用这种方法可能会相当昂贵。

### `void QTransform::map(int x, int y, int *tx, int *ty) const`

**作用与语义：**

将给定坐标`x`和`y`映射到该矩阵定义的坐标系中。所得值分别被置于*`tx`和*`ty`中。注意，变换后的坐标已四舍五入至最近的整数。

### `QRectF QTransform::mapRect(const QRectF &rectangle) const`

**作用与语义：**

创建并返回一个`QRectF`对象，该对象是给定`rectangle`的复制品，映射到由该矩阵定义的坐标系中。
矩形的坐标通过以下公式进行变换：
如果指定了旋转或剪切，该函数返回边界矩形。要检索给定`rectangle`映射到的精确区域，请使用`mapToPolygon()`函数。

**官方示例：**

```cpp
 x' = m11*x + m21*y + dx
 y' = m22*y + m12*x + dy
 if (!isAffine()) {
     w' = m13*x + m23*y + m33
     x' /= w'
     y' /= w'
 }
```

### `QRect QTransform::mapRect(const QRect &rectangle) const`

**作用与语义：**

创建并返回一个`QRect`对象，该对象是给定`rectangle`的复制品，映射到由该矩阵定义的坐标系中。注意，变换后的坐标已四舍五入至最近的整数。

### `QPolygon QTransform::mapToPolygon(const QRect &rectangle) const`

**作用与语义：**

创建并返回给定`rectangle`的`QPolygon`表示，映射到由该矩阵定义的坐标系中。
矩形的坐标通过以下公式进行变换：
多边形和矩形在变换时表现略有不同（由于整数四舍五入），所以`matrix.map(QPolygon(rectangle))`不总是和`matrix.mapToPolygon(rectangle)`一样。

**官方示例：**

```cpp
 x' = m11*x + m21*y + dx
 y' = m22*y + m12*x + dy
 if (!isAffine()) {
     w' = m13*x + m23*y + m33
     x' /= w'
     y' /= w'
 }
```

### `[static] bool QTransform::quadToQuad(const QPolygonF &one, const QPolygonF &two, QTransform &trans)`

**作用与语义：**

创建一个变换矩阵`trans`，将一个四边形`one`映射到另一个四边形`two`。如果变换可行，返回`true`;否则返回假。
这是一种结合`quadToSquare()`和`squareToQuad()`方法的便利方法。它允许输入四边形转换为任何其他四边形。

### `[static] bool QTransform::quadToSquare(const QPolygonF &quad, QTransform &trans)`

**作用与语义：**

创建一个变换矩阵 `trans`，将四边形 `quad` 映射到单位正方形。如果该变换是构造的，返回 `true`;如果不存在，则返回 false。

### `void QTransform::reset()`

**作用与语义：**

将矩阵重置为单位矩阵，即所有元素都设为零，除了`m11`和`m22`（指定刻度）和`m33`为1。

### `[since 6.5] QTransform &QTransform::rotate(qreal a, Qt::Axis axis, qreal distanceToPlane)`

**作用与语义：**

在距离屏幕`distanceToPlane`处，将坐标系逆时针旋转，`a`以指定`axis`为中心的角度，并返回矩阵的参考。
注意，如果你对控件坐标中定义的点应用`QTransform`，旋转方向将顺时针，因为y轴指向下方。
角度以度数表示。
如果`distanceToPlane`为零，则忽略。这适用于实现正交投影，其中 z 坐标应被省略而非投影。

### `QTransform &QTransform::rotate(qreal a, Qt::Axis axis = Qt::ZAxis)`

**作用与语义：**

将坐标系逆时针旋转，`a`在距离屏幕1024.0处指定`axis`的角度，并返回矩阵参考。
注意，如果你对控件坐标中定义的点应用`QTransform`，旋转方向将顺时针，因为y轴指向下方。
角度以度数表示。

### `[since 6.5] QTransform &QTransform::rotateRadians(qreal a, Qt::Axis axis, qreal distanceToPlane)`

**作用与语义：**

在距离屏幕`distanceToPlane`处，将坐标系逆时针旋转，`a`以指定`axis`为中心，并返回矩阵的参考。
注意，如果你对控件坐标中定义的点应用`QTransform`，旋转方向将顺时针，因为y轴指向下方。
角度以弧度表示。
如果`distanceToPlane`为零，则忽略。这适用于实现应省略Z坐标而非投影的正交投影。

### `QTransform &QTransform::rotateRadians(qreal a, Qt::Axis axis = Qt::ZAxis)`

**作用与语义：**

将坐标系逆时针旋转，`a`在距离屏幕1024.0处指定`axis`的给定角度，并返回矩阵参考。
注意，如果你对控件坐标中定义的点应用`QTransform`，旋转方向将顺时针，因为y轴指向下方。
角度以弧度表示。

### `QTransform &QTransform::scale(qreal sx, qreal sy)`

**作用与语义：**

通过水平`sx`和垂直`sy`缩放坐标系，并返回矩阵的参考。

### `void QTransform::setMatrix(qreal m11, qreal m12, qreal m13, qreal m21, qreal m22, qreal m23, qreal m31, qreal m32, qreal m33)`

**作用与语义：**

将矩阵元素设置为指定的值，分别是`m11`、`m12`、`m13` `m21`、`m22`、`m23` `m31`、`m32`和`m33`。注意该函数替换了之前的值。`QTransform`提供了`translate()`、`rotate()`、`scale()`和`shear()`便利函数，以基于当前定义的坐标系操作各种矩阵元素。

### `QTransform &QTransform::shear(qreal sh, qreal sv)`

**作用与语义：**

通过水平`sh`和垂直`sv`剪切坐标系，返回矩阵的参考。

### `[static] bool QTransform::squareToQuad(const QPolygonF &quad, QTransform &trans)`

**作用与语义：**

创建一个变换矩阵 `trans`，将单位正方形映射到四边形 `quad`。如果该变换是构造的，返回 `true`;如果不存在这样的变换，则返回 false。

### `QTransform &QTransform::translate(qreal dx, qreal dy)`

**作用与语义：**

沿 x 轴移动坐标系 `dx`，沿 y 轴`dy`移动，返回矩阵的参考。

### `QTransform QTransform::transposed() const`

**作用与语义：**

返回该矩阵的转置。

### `QTransform::TransformationType QTransform::type() const`

**作用与语义：**

返回该矩阵的变换类型。
变换类型是包含矩阵所有变换的最高枚举值。例如，如果矩阵既是缩放的，也是剪切的，那么该类型将是`TxShear`的，因为`TxShear`的枚举值高于`TxScale`。
知道矩阵的变换类型对优化很有用：你通常能比处理通用情况更优地处理特定类型。

### `QTransform::operator QVariant() const`

**作用与语义：**

将变换返回为`QVariant`。

### `bool QTransform::operator!=(const QTransform &matrix) const`

**作用与语义：**

如果该矩阵不等于给定`matrix`，返回`true`，否则返回`false`。

### `QTransform QTransform::operator*(const QTransform &matrix) const`

**作用与语义：**

返回将该矩阵乘以给定`matrix`的结果。
注意矩阵乘法不是交换的，即 a*b ！= b*a。

### `QTransform &QTransform::operator*=(const QTransform &matrix)`

**作用与语义：**

返回将该矩阵乘以给定`matrix`的结果。

### `QTransform &QTransform::operator*=(qreal scalar)`

**作用与语义：**

返回对该矩阵与给定`scalar`逐元素乘法的结果。

### `QTransform &QTransform::operator+=(qreal scalar)`

**作用与语义：**

返回通过给出给定`scalar`加入该矩阵的每个元素得到的矩阵。

### `QTransform &QTransform::operator-=(qreal scalar)`

**作用与语义：**

返回通过从该矩阵的每个元素减去给定`scalar`所得的矩阵。

### `QTransform &QTransform::operator/=(qreal scalar)`

**作用与语义：**

返回对该矩阵进行元素除以给定`scalar`的结果。

### `[noexcept] QTransform &QTransform::operator=(const QTransform &matrix)`

**作用与语义：**

将给定`matrix`的值分配给该矩阵。

### `bool QTransform::operator==(const QTransform &matrix) const`

**作用与语义：**

如果该矩阵等于给定的`matrix`，则返回`true`，否则返回`false`。

### `[noexcept] bool qFuzzyCompare(const QTransform &t1, const QTransform &t2)`

**作用与语义：**

如果 `t1` 和 `t2` 相等（在浮点比较中允许有小的模糊因子），则返回 `true`；否则返回 false。

### `[noexcept] size_t qHash(const QTransform &key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `QLine operator*(const QLine &line, const QTransform &matrix)`

**作用与语义：**

这和`matrix`.map（`line`）是一样的。

### `QLineF operator*(const QLineF &line, const QTransform &matrix)`

**作用与语义：**

这和`matrix`.map（`line`）是一样的。

### `QPainterPath operator*(const QPainterPath &path, const QTransform &matrix)`

**作用与语义：**

这和`matrix`.map（`path`）是一样的。

### `QPoint operator*(const QPoint &point, const QTransform &matrix)`

**作用与语义：**

这和`matrix`.map（`point`）是一样的。

### `QPointF operator*(const QPointF &point, const QTransform &matrix)`

**作用与语义：**

和`matrix`.map（`point`）一样。

### `QPolygon operator*(const QPolygon &polygon, const QTransform &matrix)`

**作用与语义：**

这和`matrix`.map（`polygon`）是一样的。

### `QPolygonF operator*(const QPolygonF &polygon, const QTransform &matrix)`

**作用与语义：**

这和`matrix`.map（`polygon`）是一样的。

### `QRegion operator*(const QRegion &region, const QTransform &matrix)`

**作用与语义：**

这和`matrix`.map（`region`）是一样的。

### `QDataStream &operator<<(QDataStream &stream, const QTransform &matrix)`

**作用与语义：**

将给定`matrix`写入给定`stream`，并返回流的引用。

### `QDataStream &operator>>(QDataStream &stream, QTransform &matrix)`

**作用与语义：**

从给定`stream`读取给定`matrix`并返回对流的引用。

### `enum TransformationType { TxNone, TxTranslate, TxScale, TxRotate, TxShear, TxProject }`

**作用与语义：**

描述矩阵中最复杂的变换成分，从 `TxNone`、平移、缩放、旋转、错切到 `TxProject` 投影逐级增加。`type()` 返回该分类，绘制和映射代码可据此选择更快路径；它不是让调用者手工设置的状态。

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

`QTransform` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
