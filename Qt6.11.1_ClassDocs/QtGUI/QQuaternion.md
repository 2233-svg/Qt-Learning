# QQuaternion

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QQuaternion` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QQuaternion>`
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

- `(since 6.11) struct Axes`
- `(since 6.11) struct Axis`
- `(since 6.11) struct EulerAngles`

### 公有函数

- `QQuaternion()`
- `QQuaternion(const QVector4D &vector)`
- `QQuaternion(float scalar, const QVector3D &vector)`
- `QQuaternion(float scalar, float xpos, float ypos, float zpos)`
- `QQuaternion conjugated() const`
- `(since 6.11) QQuaternion::EulerAngles<float> eulerAngles() const`
- `void getAxisAndAngle(float *x, float *y, float *z, float *angle) const`
- `void getAxisAndAngle(QVector3D *axis, float *angle) const`
- `QQuaternion inverted() const`
- `bool isIdentity() const`
- `bool isNull() const`
- `float length() const`
- `float lengthSquared() const`
- `void normalize()`
- `QQuaternion normalized() const`
- `QVector3D rotatedVector(const QVector3D &vector) const`
- `float scalar() const`
- `void setScalar(float scalar)`
- `void setVector(const QVector3D &vector)`
- `void setVector(float x, float y, float z)`
- `void setX(float x)`
- `void setY(float y)`
- `void setZ(float z)`
- `(since 6.11) QQuaternion::Axes toAxes() const`
- `QVector3D toEulerAngles() const`
- `QMatrix3x3 toRotationMatrix() const`
- `QVector4D toVector4D() const`
- `QVector3D vector() const`
- `float x() const`
- `float y() const`
- `float z() const`
- `operator QVariant() const`
- `QQuaternion & operator*=(const QQuaternion &quaternion)`
- `QQuaternion & operator*=(float factor)`
- `QQuaternion & operator+=(const QQuaternion &quaternion)`
- `QQuaternion & operator-=(const QQuaternion &quaternion)`
- `QQuaternion & operator/=(float divisor)`

### 静态公有成员

- `float dotProduct(const QQuaternion &q1, const QQuaternion &q2)`
- `(since 6.11) QQuaternion fromAxes(QQuaternion::Axes axes)`
- `QQuaternion fromAxes(const QVector3D &xAxis, const QVector3D &yAxis, const QVector3D &zAxis)`
- `QQuaternion fromAxisAndAngle(const QVector3D &axis, float angle)`
- `QQuaternion fromAxisAndAngle(float x, float y, float z, float angle)`
- `QQuaternion fromDirection(const QVector3D &direction, const QVector3D &up)`
- `QQuaternion fromEulerAngles(float pitch, float yaw, float roll)`
- `(since 6.11) QQuaternion fromEulerAngles(QQuaternion::EulerAngles<float> angles)`
- `QQuaternion fromEulerAngles(const QVector3D &angles)`
- `QQuaternion fromRotationMatrix(const QMatrix3x3 &rot3x3)`
- `QQuaternion nlerp(const QQuaternion &q1, const QQuaternion &q2, float t)`
- `QQuaternion rotationTo(const QVector3D &from, const QVector3D &to)`
- `QQuaternion slerp(const QQuaternion &q1, const QQuaternion &q2, float t)`

### 相关非成员函数

- `bool qFuzzyCompare(const QQuaternion &q1, const QQuaternion &q2)`
- `bool operator!=(const QQuaternion &q1, const QQuaternion &q2)`
- `QQuaternion operator*(const QQuaternion &q1, const QQuaternion &q2)`
- `QVector3D operator*(const QQuaternion &quaternion, const QVector3D &vec)`
- `QQuaternion operator*(const QQuaternion &quaternion, float factor)`
- `QQuaternion operator*(float factor, const QQuaternion &quaternion)`
- `QQuaternion operator+(const QQuaternion &q1, const QQuaternion &q2)`
- `QQuaternion operator-(const QQuaternion &quaternion)`
- `QQuaternion operator-(const QQuaternion &q1, const QQuaternion &q2)`
- `QQuaternion operator/(const QQuaternion &quaternion, float divisor)`
- `QDataStream & operator<<(QDataStream &stream, const QQuaternion &quaternion)`
- `bool operator==(const QQuaternion &q1, const QQuaternion &q2)`
- `QDataStream & operator>>(QDataStream &stream, QQuaternion &quaternion)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[constexpr noexcept] QQuaternion::QQuaternion()`

**作用与语义：**

构造一个恒等四元数（1， 0， 0， 0），即向量为（0， 0， 0）和标量1。

### `[explicit constexpr noexcept] QQuaternion::QQuaternion(const QVector4D &vector)`

**作用与语义：**

由`vector`的分量构造一个四元数。

### `[constexpr noexcept] QQuaternion::QQuaternion(float scalar, const QVector3D &vector)`

**作用与语义：**

从指定的`vector`和`scalar`构造一个四元数向量。

### `[constexpr noexcept] QQuaternion::QQuaternion(float scalar, float xpos, float ypos, float zpos)`

**作用与语义：**

构造一个四元数，向量为 （`xpos`， `ypos`， `zpos`） 和 `scalar`。

### `[constexpr noexcept] QQuaternion QQuaternion::conjugated() const`

**作用与语义：**

返回该四元数的共轭，即 （-x， -y， -z， 标量）。

### `[static constexpr noexcept] float QQuaternion::dotProduct(const QQuaternion &q1, const QQuaternion &q2)`

**作用与语义：**

返回`q1`和`q2`的点积。

### `[since 6.11] QQuaternion::EulerAngles<float> QQuaternion::eulerAngles() const`

**作用与语义：**

返回对应该四元数的欧拉角（度数）。

### `[static, since 6.11] QQuaternion QQuaternion::fromAxes(QQuaternion::Axes axes)`

**作用与语义：**

利用包含在`axes`中的轴构造四元数。
注意：这些轴假设为正交归一。

### `[static] QQuaternion QQuaternion::fromAxes(const QVector3D &xAxis, const QVector3D &yAxis, const QVector3D &zAxis)`

**作用与语义：**

利用包含在`axes`中的轴构造四元数。
注意：这些轴假设为正交归一。

### `[static] QQuaternion QQuaternion::fromAxisAndAngle(const QVector3D &axis, float angle)`

**作用与语义：**

创建一个归一化的四元数，对应于围绕指定三维`axis`旋转`angle`度。

### `[static] QQuaternion QQuaternion::fromAxisAndAngle(float x, float y, float z, float angle)`

**作用与语义：**

创建一个归一化的四元数，对应于绕三维轴旋转`angle`度（`x`、`y`、`z`）。

### `[static] QQuaternion QQuaternion::fromDirection(const QVector3D &direction, const QVector3D &up)`

**作用与语义：**

利用指定的前向`direction`和向上方向`up`构造四元数。如果未指定向上方向，或前向和向上向量共线，将生成一个新的正交向上方向。

### `[static] QQuaternion QQuaternion::fromEulerAngles(float pitch, float yaw, float roll)`

**作用与语义：**

生成一个四元数，对应于围绕z轴旋转`roll`度、x轴旋转`pitch`度、y轴旋转`yaw`度（顺序）。

### `[static, since 6.11] QQuaternion QQuaternion::fromEulerAngles(QQuaternion::EulerAngles<float> angles)`

**作用与语义：**

等价于。

**官方示例：**

```cpp
 fromEulerAngles(angles.pitch, angles.yaw, angles.roll);
```

### `[static] QQuaternion QQuaternion::fromEulerAngles(const QVector3D &angles)`

**作用与语义：**

创建一个四元数，对应旋转的 `angles`：角度。`z()` 个 z 轴的度数，角度。`x()` 个 x 轴的度数，以及 角度。`y()` 个绕 y 轴的度数（按此顺序）。

### `[static] QQuaternion QQuaternion::fromRotationMatrix(const QMatrix3x3 &rot3x3)`

**作用与语义：**

生成一个四元数，对应旋转矩阵`rot3x3`。
注意：如果给定的旋转矩阵未被归一化，得到的四元数将包含缩放信息。

### `void QQuaternion::getAxisAndAngle(float *x, float *y, float *z, float *angle) const`

**作用与语义：**

提取一个三维轴（`x`、`y`、`z`）和一个对应于该四元数的旋转角度`angle`（度数）。
所有`x`、`y`、`z`和`angle`都必须是有效的非 Non-`nullptr` 指针，否则行为未定义。

### `void QQuaternion::getAxisAndAngle(QVector3D *axis, float *angle) const`

**作用与语义：**

提取一个三维轴`axis`和一个对应于该四元数的旋转角度`angle`度数。
`axis`和`angle`都必须是有效的非`nullptr`指针，否则行为未定义。

### `[constexpr noexcept] QQuaternion QQuaternion::inverted() const`

**作用与语义：**

返回该四元数的逆函数。如果该四元数为空，则返回一个零四元数。

### `[constexpr noexcept] bool QQuaternion::isIdentity() const`

**作用与语义：**

如果该四元数的x、y和z分量设为0.0，标量分量设为1.0，则返回`true`;否则返回`false`。

### `[constexpr noexcept] bool QQuaternion::isNull() const`

**作用与语义：**

如果该四元数的x、y、z和标量分量设为0.0，返回`true`;否则返回`false`。

### `float QQuaternion::length() const`

**作用与语义：**

返回四元数的长度。这也称为“范数”。

### `float QQuaternion::lengthSquared() const`

**作用与语义：**

返回四元数的平方长度。
注意：虽然计算成本低，但易发生溢出和下溢，`length()`在许多情况下避免了这种情况。

### `[static] QQuaternion QQuaternion::nlerp(const QQuaternion &q1, const QQuaternion &q2, float t)`

**作用与语义：**

沿旋转位置`q1`和`q2`之间的最短线性路径插值。`t`值应介于0到1之间，表示`q1`到`q2`之间的距离。结果将是`normalized()`。
如果`t`小于或等于0，则返回`q1`。如果`t`大于或等于1，则返回`q2`。
nlerp() 函数通常比 `slerp()` 快，并且能为球面插值提供近似结果，这些结果对于某些应用来说已经足够好。

### `void QQuaternion::normalize()`

**作用与语义：**

在原位对当前四元数进行归一化。如果是零四元数或四元数长度非常接近1，则不会发生任何问题。

### `QQuaternion QQuaternion::normalized() const`

**作用与语义：**

返回该四元数的归一化单位形式。
如果该四元数为零，则返回一个零四元数。如果四元数长度非常接近1，则返回原样。否则返回长度为1的四元数的归一化形式。

### `QVector3D QQuaternion::rotatedVector(const QVector3D &vector) const`

**作用与语义：**

用该四元数旋转`vector`，生成三维空间中的新向量。以下代码：
等价于以下内容：

**官方示例：**

```cpp
 QVector3D result = q.rotatedVector(vector);
```

### `[static] QQuaternion QQuaternion::rotationTo(const QVector3D &from, const QVector3D &to)`

**作用与语义：**

返回从向量`from`描述的方向旋转到向量`to`描述方向的最短弧四元数。

### `[constexpr noexcept] float QQuaternion::scalar() const`

**作用与语义：**

返回该四元数的标量分量。

### `[constexpr noexcept] void QQuaternion::setScalar(float scalar)`

**作用与语义：**

将该四元数的标量分量设为`scalar`。

### `[constexpr noexcept] void QQuaternion::setVector(const QVector3D &vector)`

**作用与语义：**

将该四元数的向量分量设为`vector`。

### `[constexpr noexcept] void QQuaternion::setVector(float x, float y, float z)`

**作用与语义：**

将该四元数的向量分量设为 （`x`， `y`， `z`）。

### `[constexpr noexcept] void QQuaternion::setX(float x)`

**作用与语义：**

将该四元数矢量的x坐标设为给定的`x`坐标。

### `[constexpr noexcept] void QQuaternion::setY(float y)`

**作用与语义：**

将该四元数矢量的 y 坐标设为给定的`y`坐标。

### `[constexpr noexcept] void QQuaternion::setZ(float z)`

**作用与语义：**

将该四元数矢量的 z 坐标设为给定的`z`坐标。

### `[static] QQuaternion QQuaternion::slerp(const QQuaternion &q1, const QQuaternion &q2, float t)`

**作用与语义：**

沿旋转位置`q1`到`q2`之间的最短球面路径进行插值。`t`值应在0到1之间，表示`q1`到`q2`之间的球面距离。
如果`t`小于或等于0，则返回`q1`。如果`t`大于或等于1，则返回`q2`。

### `[since 6.11] QQuaternion::Axes QQuaternion::toAxes() const`

**作用与语义：**

返回定义该四元数的三个正交归一轴。

### `QVector3D QQuaternion::toEulerAngles() const`

**作用与语义：**

计算对应该四元数的滚转、俯仰和偏航欧拉角（度数）。

### `QMatrix3x3 QQuaternion::toRotationMatrix() const`

**作用与语义：**

创建对应该四元数的旋转矩阵。
注意：如果该四元数未归一化，产生的旋转矩阵将包含缩放信息。

### `[constexpr noexcept] QVector4D QQuaternion::toVector4D() const`

**作用与语义：**

将该四元数返回为四维矢量。

### `[constexpr noexcept] QVector3D QQuaternion::vector() const`

**作用与语义：**

返回该四元数的向量分量。

### `[constexpr noexcept] float QQuaternion::x() const`

**作用与语义：**

返回该四元数矢量的x坐标。

### `[constexpr noexcept] float QQuaternion::y() const`

**作用与语义：**

返回该四元数矢量的y坐标。

### `[constexpr noexcept] float QQuaternion::z() const`

**作用与语义：**

返回该四元数矢量的 z 坐标。

### `QQuaternion::operator QVariant() const`

**作用与语义：**

将四元数返回为`QVariant`。

### `[constexpr noexcept] QQuaternion &QQuaternion::operator*=(const QQuaternion &quaternion)`

**作用与语义：**

将该四元数乘以`quaternion`并返回对该四元数的引用。

### `[constexpr noexcept] QQuaternion &QQuaternion::operator*=(float factor)`

**作用与语义：**

将该四元数的分量乘以给定`factor`，返回对该四元数的引用。

### `[constexpr noexcept] QQuaternion &QQuaternion::operator+=(const QQuaternion &quaternion)`

**作用与语义：**

将给定`quaternion`加到该四元数上，并返回对该四元数的引用。

### `[constexpr noexcept] QQuaternion &QQuaternion::operator-=(const QQuaternion &quaternion)`

**作用与语义：**

从该四元数中减去给定`quaternion`，返回对该四元数的引用。

### `[constexpr] QQuaternion &QQuaternion::operator/=(float divisor)`

**作用与语义：**

将该四元数的分量除以给定的`divisor`，并返回对该四元数的引用。

### `[constexpr noexcept] bool qFuzzyCompare(const QQuaternion &q1, const QQuaternion &q2)`

**作用与语义：**

如果 `q1` 和 `q2` 相等（在浮点比较中允许有小的模糊因子），则返回 `true`；否则返回 false。

### `[constexpr noexcept] bool operator!=(const QQuaternion &q1, const QQuaternion &q2)`

**作用与语义：**

如果 `q1` 不等于 `q2`，则返回 `true`；否则返回 `false`。该运算符使用精确的浮点数比较。

### `[constexpr noexcept] QQuaternion operator*(const QQuaternion &q1, const QQuaternion &q2)`

**作用与语义：**

利用四元数乘法乘`q1`和`q2`。结果对应于应用`q1`和`q2`所指定的两个旋转。

### `QVector3D operator*(const QQuaternion &quaternion, const QVector3D &vec)`

**作用与语义：**

旋转一个带有四元数`quaternion`的向量 `vec`，生成一个新的三维空间向量。

### `[constexpr noexcept] QQuaternion operator*(const QQuaternion &quaternion, float factor)`

**作用与语义：**

返回给定`quaternion`的副本，乘以给定`factor`。

### `[constexpr noexcept] QQuaternion operator*(float factor, const QQuaternion &quaternion)`

**作用与语义：**

返回给定`quaternion`的副本，乘以给定`factor`。

### `[constexpr noexcept] QQuaternion operator+(const QQuaternion &q1, const QQuaternion &q2)`

**作用与语义：**

返回一个`QQuaternion`对象，即给定四元数、`q1`和`q2`的和;每个分量单独相加。

### `[constexpr noexcept] QQuaternion operator-(const QQuaternion &quaternion)`

**作用与语义：**

返回一个`QQuaternion`对象，该对象通过改变给定`quaternion`的三个分量的符号构成。
相当于`QQuaternion(0,0,0,0) - quaternion`。

### `[constexpr noexcept] QQuaternion operator-(const QQuaternion &q1, const QQuaternion &q2)`

**作用与语义：**

返回一个`QQuaternion`对象，由`q1`减去`q2`;每个分量单独相减。

### `[constexpr] QQuaternion operator/(const QQuaternion &quaternion, float divisor)`

**作用与语义：**

返回由给定`quaternion`的所有分量除以给定`divisor`所形成的`QQuaternion`对象。

### `QDataStream &operator<<(QDataStream &stream, const QQuaternion &quaternion)`

**作用与语义：**

将给定的`quaternion`写入给定的`stream`，并返回对流的引用。

### `[constexpr noexcept] bool operator==(const QQuaternion &q1, const QQuaternion &q2)`

**作用与语义：**

如果 `q1` 等于 `q2`，则返回 `true`；否则返回 `false`。该运算符使用精确的浮点数比较。

### `QDataStream &operator>>(QDataStream &stream, QQuaternion &quaternion)`

**作用与语义：**

从给定`stream`读取一个四元数到给定的`quaternion`，并返回对流的引用。

### `(since 6.11) struct Axes`

**作用与语义：**

一个包含定义`quaternion`的三个正交归一`axes`的结构体。

### `(since 6.11) struct Axis`

**作用与语义：**

一个表示三维轴的结构，用于定义`quaternions`，通过三个（正交归一）轴。
结构体本身不限制其`x`、`y`和`z`成员的值，尽管使用该类型的`QQuaternion`函数可能会限制。特别是，轴对象无需规范化。
这种类型与`QVector3D`非常相似，可以很容易地转换成和，但关注点更窄。你可以称它为“强类型防御”，适用于`QVector3D`。

### `(since 6.11) struct EulerAngles`

**作用与语义：**

一个包含三个场`pitch`、`yaw`和`roll`的结构体，代表定义`quaternion`的三个欧拉角。
请查阅使用或返回欧拉角对象的函数文档，了解旋转应用的顺序。

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

`QQuaternion` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
