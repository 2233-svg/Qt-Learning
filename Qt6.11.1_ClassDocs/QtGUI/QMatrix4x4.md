# QMatrix4x4

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QMatrix4x4` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QMatrix4x4>`
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

### 公有函数

- `QMatrix4x4()`
- `QMatrix4x4(const QGenericMatrix<N, M, float> &matrix)`
- `QMatrix4x4(const QTransform &transform)`
- `QMatrix4x4(const float *values)`
- `QMatrix4x4(float m11, float m12, float m13, float m14, float m21, float m22, float m23, float m24, float m31, float m32, float m33, float m34, float m41, float m42, float m43, float m44)`
- `QVector4D column(int index) const`
- `const float * constData() const`
- `void copyDataTo(float *values) const`
- `float * data()`
- `const float * data() const`
- `double determinant() const`
- `void fill(float value)`
- `void frustum(float left, float right, float bottom, float top, float nearPlane, float farPlane)`
- `QMatrix4x4 inverted(bool *invertible = nullptr) const`
- `bool isAffine() const`
- `bool isIdentity() const`
- `void lookAt(const QVector3D &eye, const QVector3D &center, const QVector3D &up)`
- `QPoint map(const QPoint &point) const`
- `QPointF map(const QPointF &point) const`
- `QVector3D map(const QVector3D &point) const`
- `QVector4D map(const QVector4D &point) const`
- `QRect mapRect(const QRect &rect) const`
- `QRectF mapRect(const QRectF &rect) const`
- `QVector3D mapVector(const QVector3D &vector) const`
- `QMatrix3x3 normalMatrix() const`
- `void optimize()`
- `void ortho(float left, float right, float bottom, float top, float nearPlane, float farPlane)`
- `void ortho(const QRect &rect)`
- `void ortho(const QRectF &rect)`
- `void perspective(float verticalAngle, float aspectRatio, float nearPlane, float farPlane)`
- `void rotate(const QQuaternion &quaternion)`
- `void rotate(float angle, const QVector3D &vector)`
- `void rotate(float angle, float x, float y, float z = 0.0f)`
- `QVector4D row(int index) const`
- `void scale(const QVector3D &vector)`
- `void scale(float factor)`
- `void scale(float x, float y)`
- `void scale(float x, float y, float z)`
- `void setColumn(int index, const QVector4D &value)`
- `void setRow(int index, const QVector4D &value)`
- `void setToIdentity()`
- `QGenericMatrix<N, M, float> toGenericMatrix() const`
- `QTransform toTransform() const`
- `QTransform toTransform(float distanceToPlane) const`
- `void translate(const QVector3D &vector)`
- `void translate(float x, float y)`
- `void translate(float x, float y, float z)`
- `QMatrix4x4 transposed() const`
- `void viewport(float left, float bottom, float width, float height, float nearPlane = 0.0f, float farPlane = 1.0f)`
- `void viewport(const QRectF &rect)`
- `operator QVariant() const`
- `bool operator!=(const QMatrix4x4 &other) const`
- `float & operator()(int row, int column)`
- `const float & operator()(int row, int column) const`
- `QMatrix4x4 & operator*=(const QMatrix4x4 &other)`
- `QMatrix4x4 & operator*=(float factor)`
- `QMatrix4x4 & operator+=(const QMatrix4x4 &other)`
- `QMatrix4x4 & operator-=(const QMatrix4x4 &other)`
- `QMatrix4x4 & operator/=(float divisor)`
- `bool operator==(const QMatrix4x4 &other) const`

### 相关非成员函数

- `bool qFuzzyCompare(const QMatrix4x4 &m1, const QMatrix4x4 &m2)`
- `QMatrix4x4 operator*(const QMatrix4x4 &m1, const QMatrix4x4 &m2)`
- `QVector4D operator*(const QMatrix4x4 &matrix, const QVector4D &vector)`
- `QMatrix4x4 operator*(const QMatrix4x4 &matrix, float factor)`
- `QPoint operator*(const QPoint &point, const QMatrix4x4 &matrix)`
- `QPointF operator*(const QPointF &point, const QMatrix4x4 &matrix)`
- `QVector4D operator*(const QVector4D &vector, const QMatrix4x4 &matrix)`
- `QMatrix4x4 operator*(float factor, const QMatrix4x4 &matrix)`
- `QMatrix4x4 operator+(const QMatrix4x4 &m1, const QMatrix4x4 &m2)`
- `QMatrix4x4 operator-(const QMatrix4x4 &matrix)`
- `QMatrix4x4 operator-(const QMatrix4x4 &m1, const QMatrix4x4 &m2)`
- `QMatrix4x4 operator/(const QMatrix4x4 &matrix, float divisor)`
- `QDataStream & operator<<(QDataStream &stream, const QMatrix4x4 &matrix)`
- `QDataStream & operator>>(QDataStream &stream, QMatrix4x4 &matrix)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QMatrix4x4::QMatrix4x4()`

**作用与语义：**

构造一个恒等矩阵。

### `[explicit] template <int N, int M> QMatrix4x4::QMatrix4x4(const QGenericMatrix<N, M, float> &matrix)`

**作用与语义：**

从`matrix`的最左4列和最顶4行构造一个4x4矩阵。如果`matrix`列或行少于4列，剩余元素填充单位矩阵中的元素。

### `QMatrix4x4::QMatrix4x4(const QTransform &transform)`

**作用与语义：**

`transform` 从传统的量子二维变换矩阵构造一个 4x4 矩阵。
如果`transform`有特殊类型（身份、平移、尺度等），程序员应按照该构造函数调用`optimize()`，以便QMatrix4x4优化进一步调用`translate()`、`scale()`等。

### `[explicit] QMatrix4x4::QMatrix4x4(const float *values)`

**作用与语义：**

从给定的16个浮点`values`构造矩阵。假定数组内容按行-主要顺序排列`values`。
如果矩阵有特殊类型（恒等、平移、尺度等），程序员应按照该构造函数调用`optimize()`，以便QMatrix4x4优化进一步调用`translate()`、`scale()`等。

### `QMatrix4x4::QMatrix4x4(float m11, float m12, float m13, float m14, float m21, float m22, float m23, float m24, float m31, float m32, float m33, float m34, float m41, float m42, float m43, float m44)`

**作用与语义：**

由16个元素构造矩阵`m11`、`m12`、`m13`、`m14`、`m21`、`m22`、`m23`、`m24`、`m31`、`m32`、`m33`、`m34`、`m41`、`m42`、`m43`和`m44`。元素按行大序排列。
如果矩阵有特殊类型（恒等、平移、尺度等），程序员应按照该构造函数调用`optimize()`，以便QMatrix4x4优化进一步调用`translate()`、`scale()`等。

### `QVector4D QMatrix4x4::column(int index) const`

**作用与语义：**

返回列`index`的元素，作为四维向量。

### `const float *QMatrix4x4::constData() const`

**作用与语义：**

返回该矩阵原始数据的常量指针。这些原始数据以列大调格式存储。

### `void QMatrix4x4::copyDataTo(float *values) const`

**作用与语义：**

检索该矩阵中的16项，并按行大序复制到`values`。

### `float *QMatrix4x4::data()`

**作用与语义：**

返回指向该矩阵原始数据的指针。

### `const float *QMatrix4x4::data() const`

**作用与语义：**

返回该矩阵原始数据的常量指针。这些原始数据以列大调格式存储。

### `double QMatrix4x4::determinant() const`

**作用与语义：**

返回该矩阵的行列式。

### `void QMatrix4x4::fill(float value)`

**作用与语义：**

用`value`填充该矩阵的所有元素。

### `void QMatrix4x4::frustum(float left, float right, float bottom, float top, float nearPlane, float farPlane)`

**作用与语义：**

将该矩阵乘以另一个矩阵，该矩阵对具有左下角（`left`、`bottom`）、右上角（`right`、`top`）以及指定的`nearPlane`和`farPlane`裁切平面的窗口应用透视截锥投影。

### `QMatrix4x4 QMatrix4x4::inverted(bool *invertible = nullptr) const`

**作用与语义：**

返回该矩阵的逆矩阵。如果该矩阵无法被反转，返回恒等式;即`determinant()`为零。如果`invertible`不是空，则如果矩阵可以反转，则写为真;否则为假。
如果该矩阵被识别为单位矩阵或正交归一矩阵，该函数将通过优化的例程快速反演矩阵。

### `bool QMatrix4x4::isAffine() const`

**作用与语义：**

如果该矩阵是仿射矩阵，则返回`true`;否则为假。
仿射矩阵是一个4x4矩阵，第3行等于（0， 0， 0， 1），例如没有射影系数。

### `bool QMatrix4x4::isIdentity() const`

**作用与语义：**

如果该矩阵是单位元，则返回`true`;否则为假。

### `void QMatrix4x4::lookAt(const QVector3D &eye, const QVector3D &center, const QVector3D &up)`

**作用与语义：**

将该矩阵乘以从视点推导的观察矩阵。`center`值表示`eye`所注视视角的中心。`up`值表示相对于`eye`应考虑向上的方向。
注意：`up`矢量不得与从`eye`到`center`的视线平行。

### `QPoint QMatrix4x4::map(const QPoint &point) const`

**作用与语义：**

映射`point`通过将该矩阵乘以`point`。矩阵在点前应用。

### `QPointF QMatrix4x4::map(const QPointF &point) const`

**作用与语义：**

映射通过后乘以`point`来`point`。矩阵在点前应用。

### `QVector3D QMatrix4x4::map(const QVector3D &point) const`

**作用与语义：**

通过将该矩阵乘以`point`来实现的映射`point`假设w坐标为1.0，扩展为四维矢量。矩阵在点前应用。
注意：该函数与`mapVector()`不同。对于点，始终使用map()。`mapVector()`仅适用于向量（方向）。

### `QVector4D QMatrix4x4::map(const QVector4D &point) const`

**作用与语义：**

映射`point`通过将该矩阵乘以`point`。矩阵在点前应用。

### `QRect QMatrix4x4::mapRect(const QRect &rect) const`

**作用与语义：**

映射`rect`方法是将该矩阵乘以`rect`的角，然后从结果中形成一个新的矩形。返回的矩形将是一个普通的二维矩形，边与水平和垂直轴平行。

### `QRectF QMatrix4x4::mapRect(const QRectF &rect) const`

**作用与语义：**

映射`rect`方法是将该矩阵乘以`rect`的角，然后从结果中形成一个新的矩形。返回的矩形将是一个普通的二维矩形，边与水平和垂直轴平行。

### `QVector3D QMatrix4x4::mapVector(const QVector3D &vector) const`

**作用与语义：**

映射`vector`通过将该矩阵顶部3x3部分乘以`vector`。忽略该矩阵的平移和投影分量。矩阵在向量前应用。

### `QMatrix3x3 QMatrix4x4::normalMatrix() const`

**作用与语义：**

返回对应该4x4变换的法向矩阵。法向矩阵是该4x4矩阵左上方3x3部分逆矩阵的转置。如果3x3子矩阵不可逆，该函数返回恒等矩阵。

### `void QMatrix4x4::optimize()`

**作用与语义：**

优化该矩阵当前元素的使用。
某些操作，例如 `translate()`、`scale()` 和 `rotate()`，如果被修改的矩阵已知为单位矩阵、之前的 `translate()`、之前的 `scale()` 等，可以更高效地执行。
通常情况下，`QMatrix4x4` 类在执行操作时会在内部跟踪这种特殊类型。然而，如果矩阵通过 `operator()`(int, int) 或 `data()` 直接修改，则 `QMatrix4x4` 将失去对特殊类型的跟踪，并会恢复为最安全但效率最低的操作。
通过在直接修改矩阵后调用 optimize()，程序员可以强制 `QMatrix4x4` 恢复特殊类型，如果元素符合已知优化类型之一。

### `void QMatrix4x4::ortho(float left, float right, float bottom, float top, float nearPlane, float farPlane)`

**作用与语义：**

将该矩阵乘以另一个矩阵，该矩阵对具有左下角（`left`、`bottom`）、右上角（`right`、`top`）以及指定的`nearPlane`和`farPlane`裁剪平面的窗口应用正交投影。

### `void QMatrix4x4::ortho(const QRect &rect)`

**作用与语义：**

将该矩阵乘以另一个对边界由`rect`指定的窗口应用正交投影的矩阵。近截断平面和远截断平面分别为-1和1。

### `void QMatrix4x4::ortho(const QRectF &rect)`

**作用与语义：**

将该矩阵乘以另一个对边界由`rect`指定的窗口应用正交投影的矩阵。近截断平面和远截断平面分别为-1和1。

### `void QMatrix4x4::perspective(float verticalAngle, float aspectRatio, float nearPlane, float farPlane)`

**作用与语义：**

将该矩阵乘以另一个应用透视投影的矩阵。垂直视场在一个窗户内为`verticalAngle`度，窗户中有决定水平视野的给定`aspectRatio`。投影具有指定的`nearPlane`和`farPlane`剪裁平面，即观察者到相应平面的距离。

### `void QMatrix4x4::rotate(const QQuaternion &quaternion)`

**作用与语义：**

将该矩阵乘以另一个根据指定`quaternion`旋转坐标的矩阵。假设该`quaternion`已被归一化。

### `void QMatrix4x4::rotate(float angle, const QVector3D &vector)`

**作用与语义：**

将该矩阵乘以另一个将坐标旋转约`angle`度的矩阵，约`vector`度。

### `void QMatrix4x4::rotate(float angle, float x, float y, float z = 0.0f)`

**作用与语义：**

将该矩阵乘以另一个矩阵，使坐标绕向量旋转`angle`度（`x`、`y`、`z`）。

### `QVector4D QMatrix4x4::row(int index) const`

**作用与语义：**

返回第`index`行的元素，作为四维矢量。

### `void QMatrix4x4::scale(const QVector3D &vector)`

**作用与语义：**

将该矩阵乘以另一个坐标乘以`vector`分量的矩阵。

### `void QMatrix4x4::scale(float factor)`

**作用与语义：**

将该矩阵乘以另一个坐标乘以给定`factor`的矩阵。

### `void QMatrix4x4::scale(float x, float y)`

**作用与语义：**

将该矩阵乘以另一个坐标乘以分量`x`的矩阵，`y`。

### `void QMatrix4x4::scale(float x, float y, float z)`

**作用与语义：**

将该矩阵乘以另一个坐标乘以分量`x`、`y`和`z`的矩阵。

### `void QMatrix4x4::setColumn(int index, const QVector4D &value)`

**作用与语义：**

将列`index`的元素映射为`value`的分量。

### `void QMatrix4x4::setRow(int index, const QVector4D &value)`

**作用与语义：**

将第`index`行的元素映射为`value`的分量。

### `void QMatrix4x4::setToIdentity()`

**作用与语义：**

将该矩阵映射为恒等式。

### `template <int N, int M> QGenericMatrix<N, M, float> QMatrix4x4::toGenericMatrix() const`

**作用与语义：**

从该4x4矩阵中最左侧的N列和最顶的M行构造NxM通用矩阵。如果N或M大于4，则其余元素填充单位矩阵中的元素。

### `QTransform QMatrix4x4::toTransform() const`

**作用与语义：**

返回对应该矩阵的常规Qt二维变换矩阵。
返回的`QTransform`是通过简单地去除`QMatrix4x4`的第三行和第三列组成的。这适用于实现正投影，即应去除Z坐标而非投影。

### `QTransform QMatrix4x4::toTransform(float distanceToPlane) const`

**作用与语义：**

返回对应该矩阵的常规Qt二维变换矩阵。
如果`distanceToPlane`非零，则表示一个投影因子用于调整z坐标。10²4的值对应于`QTransform::rotate()`用于x轴和y轴的投影因子。
如果`distanceToPlane`为零，则返回的`QTransform`只需去除`QMatrix4x4`的第三行第三列即可。这适用于实现应省略Z坐标而非投影的正交投影。

### `void QMatrix4x4::translate(const QVector3D &vector)`

**作用与语义：**

将该矩阵乘以另一个将坐标平移为`vector`分量的矩阵。

### `void QMatrix4x4::translate(float x, float y)`

**作用与语义：**

将该矩阵乘以另一个坐标换成分量`x`和`y`。

### `void QMatrix4x4::translate(float x, float y, float z)`

**作用与语义：**

将该矩阵乘以另一个坐标换以分量`x`、`y`和`z`的矩阵。

### `QMatrix4x4 QMatrix4x4::transposed() const`

**作用与语义：**

返回该矩阵，并围绕其对角线进行换置。

### `void QMatrix4x4::viewport(float left, float bottom, float width, float height, float nearPlane = 0.0f, float farPlane = 1.0f)`

**作用与语义：**

将该矩阵乘以另一个矩阵，该矩阵执行OpenGL用于从归一化设备坐标（NDC）到视口（窗口）坐标的比例和偏置变换。也就是说，它将立方体在每个维度中[-1， 1]的点映射到视口的左下角近（`left`， `bottom`， `nearPlane`）和大小（`width`， `height`， `farPlane` - `nearPlane`）。
这与固定函数OpenGL视口变换所使用的变换匹配，该变换由glViewport()和glDepthRange()两个函数控制。

### `void QMatrix4x4::viewport(const QRectF &rect)`

**作用与语义：**

设置视口变换，视口边界为`rect`，近距离和远距离分别设为0和1。

### `QMatrix4x4::operator QVariant() const`

**作用与语义：**

返回矩阵为`QVariant`。

### `bool QMatrix4x4::operator!=(const QMatrix4x4 &other) const`

**作用与语义：**

如果该矩阵与`other`不相同，返回`true`;否则为假。该算符使用精确浮点比较。

### `float &QMatrix4x4::operator()(int row, int column)`

**作用与语义：**

返回该矩阵中位置（`row`， `column`）的元素的引用，以便将该元素分配到。

### `const float &QMatrix4x4::operator()(int row, int column) const`

**作用与语义：**

返回该矩阵中位置（`row`， `column`）元素的常量引用。

### `QMatrix4x4 &QMatrix4x4::operator*=(const QMatrix4x4 &other)`

**作用与语义：**

将`other`的内容乘以该矩阵。

### `QMatrix4x4 &QMatrix4x4::operator*=(float factor)`

**作用与语义：**

将该矩阵的所有元素乘以`factor`。

### `QMatrix4x4 &QMatrix4x4::operator+=(const QMatrix4x4 &other)`

**作用与语义：**

将`other`的内容添加到该矩阵中。

### `QMatrix4x4 &QMatrix4x4::operator-=(const QMatrix4x4 &other)`

**作用与语义：**

从该矩阵中减去`other`的内容。

### `QMatrix4x4 &QMatrix4x4::operator/=(float divisor)`

**作用与语义：**

将该矩阵的所有元素除以`divisor`。

### `bool QMatrix4x4::operator==(const QMatrix4x4 &other) const`

**作用与语义：**

如果该矩阵与`other`相同，返回`true`;否则为假。该算符使用精确浮点比较。

### `[noexcept] bool qFuzzyCompare(const QMatrix4x4 &m1, const QMatrix4x4 &m2)`

**作用与语义：**

如果`m1`和`m2`相等，则返回`true`，允许浮点比较产生小模糊因子;否则为假。

### `QMatrix4x4 operator*(const QMatrix4x4 &m1, const QMatrix4x4 &m2)`

**作用与语义：**

返回`m1`和`m2`的乘积。

### `QVector4D operator*(const QMatrix4x4 &matrix, const QVector4D &vector)`

**作用与语义：**

返回根据 `matrix` 变换 `vector` 的结果，矩阵在向量前应用。

### `QMatrix4x4 operator*(const QMatrix4x4 &matrix, float factor)`

**作用与语义：**

返回将`matrix`的所有元素乘以`factor`的结果。

### `QPoint operator*(const QPoint &point, const QMatrix4x4 &matrix)`

**作用与语义：**

返回根据`matrix`变换`point`的结果，矩阵在点后应用。

### `QPointF operator*(const QPointF &point, const QMatrix4x4 &matrix)`

**作用与语义：**

返回根据`matrix`变换`point`的结果，矩阵在点后应用。

### `QVector4D operator*(const QVector4D &vector, const QMatrix4x4 &matrix)`

**作用与语义：**

返回根据`matrix`对`vector`进行变换的结果，矩阵在矢量后应用。

### `QMatrix4x4 operator*(float factor, const QMatrix4x4 &matrix)`

**作用与语义：**

返回将`matrix`的所有元素乘以`factor`的结果。

### `QMatrix4x4 operator+(const QMatrix4x4 &m1, const QMatrix4x4 &m2)`

**作用与语义：**

返回`m1`和`m2`的总和。

### `QMatrix4x4 operator-(const QMatrix4x4 &matrix)`

**作用与语义：**

返回`matrix`的否定。

### `QMatrix4x4 operator-(const QMatrix4x4 &m1, const QMatrix4x4 &m2)`

**作用与语义：**

返回`m1`和`m2`的差额。

### `QMatrix4x4 operator/(const QMatrix4x4 &matrix, float divisor)`

**作用与语义：**

返回将`matrix`的所有元素除以`divisor`的结果。

### `QDataStream &operator<<(QDataStream &stream, const QMatrix4x4 &matrix)`

**作用与语义：**

将给定`matrix`写入给定`stream`，并返回流的引用。

### `QDataStream &operator>>(QDataStream &stream, QMatrix4x4 &matrix)`

**作用与语义：**

从给定`stream`读取4x4矩阵到给定`matrix`并返回对流的引用。

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

`QMatrix4x4` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
