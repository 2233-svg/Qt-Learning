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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 74 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `QMatrix4x4::QMatrix4x4()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMatrix4x4` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] template <int N, int M> QMatrix4x4::QMatrix4x4(const QGenericMatrix<N, M, float> &matrix)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMatrix4x4` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `matrix`：类型为 `const QGenericMatrix<N, M, float> &`。没有默认值，调用时必须提供。传入 `const QGenericMatrix<N, M, float> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMatrix4x4::QMatrix4x4(const QTransform &transform)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMatrix4x4` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `transform`：类型为 `const QTransform &`。没有默认值，调用时必须提供。传入 `const QTransform &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QMatrix4x4::QMatrix4x4(const float *values)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMatrix4x4` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `values`：类型为 `const float *`。没有默认值，调用时必须提供。传入 `const float *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMatrix4x4::QMatrix4x4(float m11, float m12, float m13, float m14, float m21, float m22, float m23, float m24, float m31, float m32, float m33, float m34, float m41, float m42, float m43, float m44)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMatrix4x4` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `m11`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `m12`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `m13`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `m14`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `m21`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `m22`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `m23`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `m24`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `m31`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `m32`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `m33`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `m34`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `m41`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `m42`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `m43`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `m44`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVector4D QMatrix4x4::column(int index) const`

**API 类别：** 成员函数说明

**中文解读：** `QMatrix4x4::column` 用于计算、查询或取得与“列”相关的操作。调用时要先确认当前状态和 `index` 的有效范围；返回类型是 `QVector4D`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVector4D`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const float *QMatrix4x4::constData() const`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `constData`，用于取得 `QMatrix4x4` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`const float *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMatrix4x4::copyDataTo(float *values) const`

**API 类别：** 成员函数说明

**中文解读：** `QMatrix4x4::copyDataTo` 用于执行与“copy、数据访问、转换输出”相关的操作。调用时要先确认当前状态和 `values` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `values`：类型为 `float *`。没有默认值，调用时必须提供。传入 `float *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `float *QMatrix4x4::data()`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `data`，用于取得 `QMatrix4x4` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`float *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const float *QMatrix4x4::data() const`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `data`，用于取得 `QMatrix4x4` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`const float *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `double QMatrix4x4::determinant() const`

**API 类别：** 成员函数说明

**中文解读：** `QMatrix4x4::determinant` 用于计算、查询或取得与“determinant”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `double`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`double`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMatrix4x4::fill(float value)`

**API 类别：** 成员函数说明

**中文解读：** `QMatrix4x4::fill` 用于执行与“fill”相关的操作。调用时要先确认当前状态和 `value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `value`：类型为 `float`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMatrix4x4::frustum(float left, float right, float bottom, float top, float nearPlane, float farPlane)`

**API 类别：** 成员函数说明

**中文解读：** `QMatrix4x4::frustum` 用于执行与“frustum”相关的操作。调用时要先确认当前状态和 `left`、`right`、`bottom`、`top`、`nearPlane`、`farPlane` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `left`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `right`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `bottom`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `top`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `nearPlane`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `farPlane`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMatrix4x4 QMatrix4x4::inverted(bool *invertible = nullptr) const`

**API 类别：** 成员函数说明

**中文解读：** `QMatrix4x4::inverted` 用于计算、查询或取得与“inverted”相关的操作。调用时要先确认当前状态和 `invertible` 的有效范围；返回类型是 `QMatrix4x4`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMatrix4x4`。
- 参数 `invertible`：类型为 `bool *`。默认值为 `nullptr`。传入 `bool *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QMatrix4x4::isAffine() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isAffine`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QMatrix4x4::isIdentity() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isIdentity`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMatrix4x4::lookAt(const QVector3D &eye, const QVector3D &center, const QVector3D &up)`

**API 类别：** 成员函数说明

**中文解读：** `QMatrix4x4::lookAt` 用于执行与“look、按位置访问”相关的操作。调用时要先确认当前状态和 `eye`、`center`、`up` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `eye`：类型为 `const QVector3D &`。没有默认值，调用时必须提供。传入 `const QVector3D &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `center`：类型为 `const QVector3D &`。没有默认值，调用时必须提供。传入 `const QVector3D &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `up`：类型为 `const QVector3D &`。没有默认值，调用时必须提供。传入 `const QVector3D &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPoint QMatrix4x4::map(const QPoint &point) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `map`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QPoint`。
- 参数 `point`：类型为 `const QPoint &`。没有默认值，调用时必须提供。传入 `const QPoint &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPointF QMatrix4x4::map(const QPointF &point) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `map`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QPointF`。
- 参数 `point`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVector3D QMatrix4x4::map(const QVector3D &point) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `map`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QVector3D`。
- 参数 `point`：类型为 `const QVector3D &`。没有默认值，调用时必须提供。传入 `const QVector3D &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVector4D QMatrix4x4::map(const QVector4D &point) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `map`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QVector4D`。
- 参数 `point`：类型为 `const QVector4D &`。没有默认值，调用时必须提供。传入 `const QVector4D &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRect QMatrix4x4::mapRect(const QRect &rect) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `mapRect`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QRect`。
- 参数 `rect`：类型为 `const QRect &`。没有默认值，调用时必须提供。矩形区域；要确认坐标系、是否包含右下边界以及空矩形的语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRectF QMatrix4x4::mapRect(const QRectF &rect) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `mapRect`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QRectF`。
- 参数 `rect`：类型为 `const QRectF &`。没有默认值，调用时必须提供。矩形区域；要确认坐标系、是否包含右下边界以及空矩形的语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVector3D QMatrix4x4::mapVector(const QVector3D &vector) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `mapVector`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QVector3D`。
- 参数 `vector`：类型为 `const QVector3D &`。没有默认值，调用时必须提供。传入 `const QVector3D &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMatrix3x3 QMatrix4x4::normalMatrix() const`

**API 类别：** 成员函数说明

**中文解读：** `QMatrix4x4::normalMatrix` 用于计算、查询或取得与“normal、Matrix”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMatrix3x3`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMatrix3x3`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMatrix4x4::optimize()`

**API 类别：** 成员函数说明

**中文解读：** `QMatrix4x4::optimize` 用于执行与“optimize”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMatrix4x4::ortho(float left, float right, float bottom, float top, float nearPlane, float farPlane)`

**API 类别：** 成员函数说明

**中文解读：** `QMatrix4x4::ortho` 用于执行与“ortho”相关的操作。调用时要先确认当前状态和 `left`、`right`、`bottom`、`top`、`nearPlane`、`farPlane` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `left`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `right`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `bottom`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `top`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `nearPlane`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `farPlane`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMatrix4x4::ortho(const QRect &rect)`

**API 类别：** 成员函数说明

**中文解读：** `QMatrix4x4::ortho` 用于执行与“ortho”相关的操作。调用时要先确认当前状态和 `rect` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `rect`：类型为 `const QRect &`。没有默认值，调用时必须提供。矩形区域；要确认坐标系、是否包含右下边界以及空矩形的语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMatrix4x4::ortho(const QRectF &rect)`

**API 类别：** 成员函数说明

**中文解读：** `QMatrix4x4::ortho` 用于执行与“ortho”相关的操作。调用时要先确认当前状态和 `rect` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `rect`：类型为 `const QRectF &`。没有默认值，调用时必须提供。矩形区域；要确认坐标系、是否包含右下边界以及空矩形的语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMatrix4x4::perspective(float verticalAngle, float aspectRatio, float nearPlane, float farPlane)`

**API 类别：** 成员函数说明

**中文解读：** `QMatrix4x4::perspective` 用于执行与“perspective”相关的操作。调用时要先确认当前状态和 `verticalAngle`、`aspectRatio`、`nearPlane`、`farPlane` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `verticalAngle`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `aspectRatio`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `nearPlane`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `farPlane`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMatrix4x4::rotate(const QQuaternion &quaternion)`

**API 类别：** 成员函数说明

**中文解读：** `QMatrix4x4::rotate` 用于执行与“rotate”相关的操作。调用时要先确认当前状态和 `quaternion` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `quaternion`：类型为 `const QQuaternion &`。没有默认值，调用时必须提供。传入 `const QQuaternion &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMatrix4x4::rotate(float angle, const QVector3D &vector)`

**API 类别：** 成员函数说明

**中文解读：** `QMatrix4x4::rotate` 用于执行与“rotate”相关的操作。调用时要先确认当前状态和 `angle`、`vector` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `angle`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `vector`：类型为 `const QVector3D &`。没有默认值，调用时必须提供。传入 `const QVector3D &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMatrix4x4::rotate(float angle, float x, float y, float z = 0.0f)`

**API 类别：** 成员函数说明

**中文解读：** `QMatrix4x4::rotate` 用于执行与“rotate”相关的操作。调用时要先确认当前状态和 `angle`、`x`、`y`、`z` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `angle`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `x`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `z`：类型为 `float`。默认值为 `0.0f`。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVector4D QMatrix4x4::row(int index) const`

**API 类别：** 成员函数说明

**中文解读：** `QMatrix4x4::row` 用于计算、查询或取得与“行”相关的操作。调用时要先确认当前状态和 `index` 的有效范围；返回类型是 `QVector4D`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVector4D`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMatrix4x4::scale(const QVector3D &vector)`

**API 类别：** 成员函数说明

**中文解读：** `QMatrix4x4::scale` 用于执行与“scale”相关的操作。调用时要先确认当前状态和 `vector` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `vector`：类型为 `const QVector3D &`。没有默认值，调用时必须提供。传入 `const QVector3D &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMatrix4x4::scale(float factor)`

**API 类别：** 成员函数说明

**中文解读：** `QMatrix4x4::scale` 用于执行与“scale”相关的操作。调用时要先确认当前状态和 `factor` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `factor`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMatrix4x4::scale(float x, float y)`

**API 类别：** 成员函数说明

**中文解读：** `QMatrix4x4::scale` 用于执行与“scale”相关的操作。调用时要先确认当前状态和 `x`、`y` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMatrix4x4::scale(float x, float y, float z)`

**API 类别：** 成员函数说明

**中文解读：** `QMatrix4x4::scale` 用于执行与“scale”相关的操作。调用时要先确认当前状态和 `x`、`y`、`z` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `z`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMatrix4x4::setColumn(int index, const QVector4D &value)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setColumn`。调用它会改变 `QMatrix4x4` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `value`：类型为 `const QVector4D &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMatrix4x4::setRow(int index, const QVector4D &value)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setRow`。调用它会改变 `QMatrix4x4` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `index`：类型为 `int`。没有默认值，调用时必须提供。项目或数据索引。先确认索引基于 0 还是 1、是否允许越界/负数，以及调用后索引是否仍然有效。
- 参数 `value`：类型为 `const QVector4D &`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMatrix4x4::setToIdentity()`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setToIdentity`。调用它会改变 `QMatrix4x4` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <int N, int M> QGenericMatrix<N, M, float> QMatrix4x4::toGenericMatrix() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toGenericMatrix`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`template <int N, int M> QGenericMatrix<N, M, float>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTransform QMatrix4x4::toTransform() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toTransform`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QTransform`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QTransform QMatrix4x4::toTransform(float distanceToPlane) const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toTransform`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QTransform`。
- 参数 `distanceToPlane`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMatrix4x4::translate(const QVector3D &vector)`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `translate`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`void`。
- 参数 `vector`：类型为 `const QVector3D &`。没有默认值，调用时必须提供。传入 `const QVector3D &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMatrix4x4::translate(float x, float y)`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `translate`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMatrix4x4::translate(float x, float y, float z)`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `translate`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `z`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMatrix4x4 QMatrix4x4::transposed() const`

**API 类别：** 成员函数说明

**中文解读：** `QMatrix4x4::transposed` 用于计算、查询或取得与“transposed”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QMatrix4x4`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QMatrix4x4`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMatrix4x4::viewport(float left, float bottom, float width, float height, float nearPlane = 0.0f, float farPlane = 1.0f)`

**API 类别：** 成员函数说明

**中文解读：** `QMatrix4x4::viewport` 用于执行与“viewport”相关的操作。调用时要先确认当前状态和 `left`、`bottom`、`width`、`height`、`nearPlane`、`farPlane` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `left`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `bottom`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `width`：类型为 `float`。没有默认值，调用时必须提供。宽度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `height`：类型为 `float`。没有默认值，调用时必须提供。高度，通常以像素、字符数或元素数量表示；要确认是否允许 0、负数和超出最大值。
- 参数 `nearPlane`：类型为 `float`。默认值为 `0.0f`。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `farPlane`：类型为 `float`。默认值为 `1.0f`。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMatrix4x4::viewport(const QRectF &rect)`

**API 类别：** 成员函数说明

**中文解读：** `QMatrix4x4::viewport` 用于执行与“viewport”相关的操作。调用时要先确认当前状态和 `rect` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `rect`：类型为 `const QRectF &`。没有默认值，调用时必须提供。矩形区域；要确认坐标系、是否包含右下边界以及空矩形的语义。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMatrix4x4::operator QVariant() const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMatrix4x4` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`由运算符声明决定`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QMatrix4x4::operator!=(const QMatrix4x4 &other) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMatrix4x4` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `other`：类型为 `const QMatrix4x4 &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `float &QMatrix4x4::operator()(int row, int column)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMatrix4x4` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`float &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const float &QMatrix4x4::operator()(int row, int column) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMatrix4x4` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`const float &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMatrix4x4 &QMatrix4x4::operator*=(const QMatrix4x4 &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMatrix4x4` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QMatrix4x4 &`。
- 参数 `other`：类型为 `const QMatrix4x4 &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMatrix4x4 &QMatrix4x4::operator*=(float factor)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMatrix4x4` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QMatrix4x4 &`。
- 参数 `factor`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMatrix4x4 &QMatrix4x4::operator+=(const QMatrix4x4 &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMatrix4x4` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QMatrix4x4 &`。
- 参数 `other`：类型为 `const QMatrix4x4 &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMatrix4x4 &QMatrix4x4::operator-=(const QMatrix4x4 &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMatrix4x4` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QMatrix4x4 &`。
- 参数 `other`：类型为 `const QMatrix4x4 &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMatrix4x4 &QMatrix4x4::operator/=(float divisor)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMatrix4x4` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QMatrix4x4 &`。
- 参数 `divisor`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QMatrix4x4::operator==(const QMatrix4x4 &other) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QMatrix4x4` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `other`：类型为 `const QMatrix4x4 &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] bool qFuzzyCompare(const QMatrix4x4 &m1, const QMatrix4x4 &m2)`

**API 类别：** 相关非成员函数

**中文解读：** `QMatrix4x4::qFuzzyCompare` 用于计算、查询或取得与“q、Fuzzy、比较”相关的操作。调用时要先确认当前状态和 `m1`、`m2` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `m1`：类型为 `const QMatrix4x4 &`。没有默认值，调用时必须提供。传入 `const QMatrix4x4 &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `m2`：类型为 `const QMatrix4x4 &`。没有默认值，调用时必须提供。传入 `const QMatrix4x4 &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMatrix4x4 operator*(const QMatrix4x4 &m1, const QMatrix4x4 &m2)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QMatrix4x4` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QMatrix4x4`。
- 参数 `m1`：类型为 `const QMatrix4x4 &`。没有默认值，调用时必须提供。传入 `const QMatrix4x4 &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `m2`：类型为 `const QMatrix4x4 &`。没有默认值，调用时必须提供。传入 `const QMatrix4x4 &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVector4D operator*(const QMatrix4x4 &matrix, const QVector4D &vector)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QMatrix4x4` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QVector4D`。
- 参数 `matrix`：类型为 `const QMatrix4x4 &`。没有默认值，调用时必须提供。传入 `const QMatrix4x4 &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `vector`：类型为 `const QVector4D &`。没有默认值，调用时必须提供。传入 `const QVector4D &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMatrix4x4 operator*(const QMatrix4x4 &matrix, float factor)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QMatrix4x4` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QMatrix4x4`。
- 参数 `matrix`：类型为 `const QMatrix4x4 &`。没有默认值，调用时必须提供。传入 `const QMatrix4x4 &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `factor`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPoint operator*(const QPoint &point, const QMatrix4x4 &matrix)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QMatrix4x4` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QPoint`。
- 参数 `point`：类型为 `const QPoint &`。没有默认值，调用时必须提供。传入 `const QPoint &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `matrix`：类型为 `const QMatrix4x4 &`。没有默认值，调用时必须提供。传入 `const QMatrix4x4 &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QPointF operator*(const QPointF &point, const QMatrix4x4 &matrix)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QMatrix4x4` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QPointF`。
- 参数 `point`：类型为 `const QPointF &`。没有默认值，调用时必须提供。传入 `const QPointF &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `matrix`：类型为 `const QMatrix4x4 &`。没有默认值，调用时必须提供。传入 `const QMatrix4x4 &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVector4D operator*(const QVector4D &vector, const QMatrix4x4 &matrix)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QMatrix4x4` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QVector4D`。
- 参数 `vector`：类型为 `const QVector4D &`。没有默认值，调用时必须提供。传入 `const QVector4D &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `matrix`：类型为 `const QMatrix4x4 &`。没有默认值，调用时必须提供。传入 `const QMatrix4x4 &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMatrix4x4 operator*(float factor, const QMatrix4x4 &matrix)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QMatrix4x4` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QMatrix4x4`。
- 参数 `factor`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `matrix`：类型为 `const QMatrix4x4 &`。没有默认值，调用时必须提供。传入 `const QMatrix4x4 &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMatrix4x4 operator+(const QMatrix4x4 &m1, const QMatrix4x4 &m2)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QMatrix4x4` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QMatrix4x4`。
- 参数 `m1`：类型为 `const QMatrix4x4 &`。没有默认值，调用时必须提供。传入 `const QMatrix4x4 &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `m2`：类型为 `const QMatrix4x4 &`。没有默认值，调用时必须提供。传入 `const QMatrix4x4 &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMatrix4x4 operator-(const QMatrix4x4 &matrix)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QMatrix4x4` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QMatrix4x4`。
- 参数 `matrix`：类型为 `const QMatrix4x4 &`。没有默认值，调用时必须提供。传入 `const QMatrix4x4 &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMatrix4x4 operator-(const QMatrix4x4 &m1, const QMatrix4x4 &m2)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QMatrix4x4` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QMatrix4x4`。
- 参数 `m1`：类型为 `const QMatrix4x4 &`。没有默认值，调用时必须提供。传入 `const QMatrix4x4 &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `m2`：类型为 `const QMatrix4x4 &`。没有默认值，调用时必须提供。传入 `const QMatrix4x4 &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMatrix4x4 operator/(const QMatrix4x4 &matrix, float divisor)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QMatrix4x4` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QMatrix4x4`。
- 参数 `matrix`：类型为 `const QMatrix4x4 &`。没有默认值，调用时必须提供。传入 `const QMatrix4x4 &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `divisor`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDataStream &operator<<(QDataStream &stream, const QMatrix4x4 &matrix)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QMatrix4x4` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDataStream &`。
- 参数 `stream`：类型为 `QDataStream &`。没有默认值，调用时必须提供。传入 `QDataStream &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `matrix`：类型为 `const QMatrix4x4 &`。没有默认值，调用时必须提供。传入 `const QMatrix4x4 &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDataStream &operator>>(QDataStream &stream, QMatrix4x4 &matrix)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QMatrix4x4` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDataStream &`。
- 参数 `stream`：类型为 `QDataStream &`。没有默认值，调用时必须提供。传入 `QDataStream &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `matrix`：类型为 `QMatrix4x4 &`。没有默认值，调用时必须提供。传入 `QMatrix4x4 &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

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
