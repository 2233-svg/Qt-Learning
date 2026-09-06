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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 66 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `[constexpr noexcept] QQuaternion::QQuaternion()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QQuaternion` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit constexpr noexcept] QQuaternion::QQuaternion(const QVector4D &vector)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QQuaternion` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `vector`：类型为 `const QVector4D &`。没有默认值，调用时必须提供。传入 `const QVector4D &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] QQuaternion::QQuaternion(float scalar, const QVector3D &vector)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QQuaternion` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `scalar`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `vector`：类型为 `const QVector3D &`。没有默认值，调用时必须提供。传入 `const QVector3D &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] QQuaternion::QQuaternion(float scalar, float xpos, float ypos, float zpos)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QQuaternion` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `scalar`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `xpos`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `ypos`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `zpos`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] QQuaternion QQuaternion::conjugated() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuaternion::conjugated` 用于计算、查询或取得与“conjugated”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QQuaternion`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QQuaternion`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static constexpr noexcept] float QQuaternion::dotProduct(const QQuaternion &q1, const QQuaternion &q2)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `dotProduct`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`float`。
- 参数 `q1`：类型为 `const QQuaternion &`。没有默认值，调用时必须提供。传入 `const QQuaternion &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `q2`：类型为 `const QQuaternion &`。没有默认值，调用时必须提供。传入 `const QQuaternion &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.11] QQuaternion::EulerAngles<float> QQuaternion::eulerAngles() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuaternion::eulerAngles` 用于计算、查询或取得与“euler、Angles”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QQuaternion::EulerAngles<float>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QQuaternion::EulerAngles<float>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.11] QQuaternion QQuaternion::fromAxes(QQuaternion::Axes axes)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromAxes`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QQuaternion`。
- 参数 `axes`：类型为 `QQuaternion::Axes`。没有默认值，调用时必须提供。传入 `QQuaternion::Axes` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QQuaternion QQuaternion::fromAxes(const QVector3D &xAxis, const QVector3D &yAxis, const QVector3D &zAxis)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromAxes`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QQuaternion`。
- 参数 `xAxis`：类型为 `const QVector3D &`。没有默认值，调用时必须提供。传入 `const QVector3D &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `yAxis`：类型为 `const QVector3D &`。没有默认值，调用时必须提供。传入 `const QVector3D &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `zAxis`：类型为 `const QVector3D &`。没有默认值，调用时必须提供。传入 `const QVector3D &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QQuaternion QQuaternion::fromAxisAndAngle(const QVector3D &axis, float angle)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromAxisAndAngle`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QQuaternion`。
- 参数 `axis`：类型为 `const QVector3D &`。没有默认值，调用时必须提供。传入 `const QVector3D &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `angle`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QQuaternion QQuaternion::fromAxisAndAngle(float x, float y, float z, float angle)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromAxisAndAngle`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QQuaternion`。
- 参数 `x`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `z`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `angle`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QQuaternion QQuaternion::fromDirection(const QVector3D &direction, const QVector3D &up)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromDirection`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QQuaternion`。
- 参数 `direction`：类型为 `const QVector3D &`。没有默认值，调用时必须提供。方向枚举，决定排列、遍历或坐标增长方向；要结合该类定义的枚举值判断实际方向。
- 参数 `up`：类型为 `const QVector3D &`。没有默认值，调用时必须提供。传入 `const QVector3D &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QQuaternion QQuaternion::fromEulerAngles(float pitch, float yaw, float roll)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromEulerAngles`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QQuaternion`。
- 参数 `pitch`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `yaw`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `roll`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static, since 6.11] QQuaternion QQuaternion::fromEulerAngles(QQuaternion::EulerAngles<float> angles)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromEulerAngles`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QQuaternion`。
- 参数 `angles`：类型为 `QQuaternion::EulerAngles<float>`。没有默认值，调用时必须提供。传入 `QQuaternion::EulerAngles<float>` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QQuaternion QQuaternion::fromEulerAngles(const QVector3D &angles)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromEulerAngles`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QQuaternion`。
- 参数 `angles`：类型为 `const QVector3D &`。没有默认值，调用时必须提供。传入 `const QVector3D &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QQuaternion QQuaternion::fromRotationMatrix(const QMatrix3x3 &rot3x3)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `fromRotationMatrix`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QQuaternion`。
- 参数 `rot3x3`：类型为 `const QMatrix3x3 &`。没有默认值，调用时必须提供。传入 `const QMatrix3x3 &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QQuaternion::getAxisAndAngle(float *x, float *y, float *z, float *angle) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QQuaternion` 的核心操作 `getAxisAndAngle`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `float *`。没有默认值，调用时必须提供。传入 `float *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `float *`。没有默认值，调用时必须提供。传入 `float *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `z`：类型为 `float *`。没有默认值，调用时必须提供。传入 `float *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `angle`：类型为 `float *`。没有默认值，调用时必须提供。传入 `float *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QQuaternion::getAxisAndAngle(QVector3D *axis, float *angle) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QQuaternion` 的核心操作 `getAxisAndAngle`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`void`。
- 参数 `axis`：类型为 `QVector3D *`。没有默认值，调用时必须提供。传入 `QVector3D *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `angle`：类型为 `float *`。没有默认值，调用时必须提供。传入 `float *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] QQuaternion QQuaternion::inverted() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuaternion::inverted` 用于计算、查询或取得与“inverted”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QQuaternion`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QQuaternion`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] bool QQuaternion::isIdentity() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isIdentity`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] bool QQuaternion::isNull() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isNull`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `float QQuaternion::length() const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `length`，返回 `QQuaternion` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`float`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `float QQuaternion::lengthSquared() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuaternion::lengthSquared` 用于计算、查询或取得与“length、Squared”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `float`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`float`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QQuaternion QQuaternion::nlerp(const QQuaternion &q1, const QQuaternion &q2, float t)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `nlerp`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QQuaternion`。
- 参数 `q1`：类型为 `const QQuaternion &`。没有默认值，调用时必须提供。传入 `const QQuaternion &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `q2`：类型为 `const QQuaternion &`。没有默认值，调用时必须提供。传入 `const QQuaternion &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `t`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QQuaternion::normalize()`

**API 类别：** 成员函数说明

**中文解读：** `QQuaternion::normalize` 用于执行与“normalize”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QQuaternion QQuaternion::normalized() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuaternion::normalized` 用于计算、查询或取得与“normalized”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QQuaternion`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QQuaternion`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVector3D QQuaternion::rotatedVector(const QVector3D &vector) const`

**API 类别：** 成员函数说明

**中文解读：** `QQuaternion::rotatedVector` 用于计算、查询或取得与“rotated、Vector”相关的操作。调用时要先确认当前状态和 `vector` 的有效范围；返回类型是 `QVector3D`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVector3D`。
- 参数 `vector`：类型为 `const QVector3D &`。没有默认值，调用时必须提供。传入 `const QVector3D &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QQuaternion QQuaternion::rotationTo(const QVector3D &from, const QVector3D &to)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `rotationTo`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QQuaternion`。
- 参数 `from`：类型为 `const QVector3D &`。没有默认值，调用时必须提供。传入 `const QVector3D &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `to`：类型为 `const QVector3D &`。没有默认值，调用时必须提供。传入 `const QVector3D &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] float QQuaternion::scalar() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuaternion::scalar` 用于计算、查询或取得与“scalar”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `float`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`float`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] void QQuaternion::setScalar(float scalar)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setScalar`。调用它会改变 `QQuaternion` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `scalar`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] void QQuaternion::setVector(const QVector3D &vector)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setVector`。调用它会改变 `QQuaternion` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `vector`：类型为 `const QVector3D &`。没有默认值，调用时必须提供。传入 `const QVector3D &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] void QQuaternion::setVector(float x, float y, float z)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setVector`。调用它会改变 `QQuaternion` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `y`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `z`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] void QQuaternion::setX(float x)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setX`。调用它会改变 `QQuaternion` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `x`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] void QQuaternion::setY(float y)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setY`。调用它会改变 `QQuaternion` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `y`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] void QQuaternion::setZ(float z)`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setZ`。调用它会改变 `QQuaternion` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数 `z`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QQuaternion QQuaternion::slerp(const QQuaternion &q1, const QQuaternion &q2, float t)`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `slerp`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QQuaternion`。
- 参数 `q1`：类型为 `const QQuaternion &`。没有默认值，调用时必须提供。传入 `const QQuaternion &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `q2`：类型为 `const QQuaternion &`。没有默认值，调用时必须提供。传入 `const QQuaternion &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `t`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[since 6.11] QQuaternion::Axes QQuaternion::toAxes() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toAxes`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QQuaternion::Axes`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVector3D QQuaternion::toEulerAngles() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toEulerAngles`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QVector3D`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMatrix3x3 QQuaternion::toRotationMatrix() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toRotationMatrix`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QMatrix3x3`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] QVector4D QQuaternion::toVector4D() const`

**API 类别：** 成员函数说明

**中文解读：** 这是转换/映射 API `toVector4D`。它通常在不同表示、坐标系、编码或 Qt 类型之间建立边界；转换前确认格式和所有权，转换后检查是否丢失精度、编码或上下文。

**签名拆解：**

- 返回值：`QVector4D`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] QVector3D QQuaternion::vector() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuaternion::vector` 用于计算、查询或取得与“vector”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QVector3D`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QVector3D`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] float QQuaternion::x() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuaternion::x` 用于计算、查询或取得与“x”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `float`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`float`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] float QQuaternion::y() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuaternion::y` 用于计算、查询或取得与“y”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `float`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`float`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] float QQuaternion::z() const`

**API 类别：** 成员函数说明

**中文解读：** `QQuaternion::z` 用于计算、查询或取得与“z”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `float`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`float`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QQuaternion::operator QVariant() const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QQuaternion` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`由运算符声明决定`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] QQuaternion &QQuaternion::operator*=(const QQuaternion &quaternion)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QQuaternion` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QQuaternion &`。
- 参数 `quaternion`：类型为 `const QQuaternion &`。没有默认值，调用时必须提供。传入 `const QQuaternion &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] QQuaternion &QQuaternion::operator*=(float factor)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QQuaternion` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QQuaternion &`。
- 参数 `factor`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] QQuaternion &QQuaternion::operator+=(const QQuaternion &quaternion)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QQuaternion` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QQuaternion &`。
- 参数 `quaternion`：类型为 `const QQuaternion &`。没有默认值，调用时必须提供。传入 `const QQuaternion &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] QQuaternion &QQuaternion::operator-=(const QQuaternion &quaternion)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QQuaternion` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QQuaternion &`。
- 参数 `quaternion`：类型为 `const QQuaternion &`。没有默认值，调用时必须提供。传入 `const QQuaternion &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr] QQuaternion &QQuaternion::operator/=(float divisor)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QQuaternion` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QQuaternion &`。
- 参数 `divisor`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] bool qFuzzyCompare(const QQuaternion &q1, const QQuaternion &q2)`

**API 类别：** 相关非成员函数

**中文解读：** `QQuaternion::qFuzzyCompare` 用于计算、查询或取得与“q、Fuzzy、比较”相关的操作。调用时要先确认当前状态和 `q1`、`q2` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `q1`：类型为 `const QQuaternion &`。没有默认值，调用时必须提供。传入 `const QQuaternion &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `q2`：类型为 `const QQuaternion &`。没有默认值，调用时必须提供。传入 `const QQuaternion &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] bool operator!=(const QQuaternion &q1, const QQuaternion &q2)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QQuaternion` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `q1`：类型为 `const QQuaternion &`。没有默认值，调用时必须提供。传入 `const QQuaternion &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `q2`：类型为 `const QQuaternion &`。没有默认值，调用时必须提供。传入 `const QQuaternion &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] QQuaternion operator*(const QQuaternion &q1, const QQuaternion &q2)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QQuaternion` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QQuaternion`。
- 参数 `q1`：类型为 `const QQuaternion &`。没有默认值，调用时必须提供。传入 `const QQuaternion &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `q2`：类型为 `const QQuaternion &`。没有默认值，调用时必须提供。传入 `const QQuaternion &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QVector3D operator*(const QQuaternion &quaternion, const QVector3D &vec)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QQuaternion` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QVector3D`。
- 参数 `quaternion`：类型为 `const QQuaternion &`。没有默认值，调用时必须提供。传入 `const QQuaternion &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `vec`：类型为 `const QVector3D &`。没有默认值，调用时必须提供。传入 `const QVector3D &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] QQuaternion operator*(const QQuaternion &quaternion, float factor)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QQuaternion` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QQuaternion`。
- 参数 `quaternion`：类型为 `const QQuaternion &`。没有默认值，调用时必须提供。传入 `const QQuaternion &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `factor`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] QQuaternion operator*(float factor, const QQuaternion &quaternion)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QQuaternion` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QQuaternion`。
- 参数 `factor`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `quaternion`：类型为 `const QQuaternion &`。没有默认值，调用时必须提供。传入 `const QQuaternion &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] QQuaternion operator+(const QQuaternion &q1, const QQuaternion &q2)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QQuaternion` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QQuaternion`。
- 参数 `q1`：类型为 `const QQuaternion &`。没有默认值，调用时必须提供。传入 `const QQuaternion &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `q2`：类型为 `const QQuaternion &`。没有默认值，调用时必须提供。传入 `const QQuaternion &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] QQuaternion operator-(const QQuaternion &quaternion)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QQuaternion` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QQuaternion`。
- 参数 `quaternion`：类型为 `const QQuaternion &`。没有默认值，调用时必须提供。传入 `const QQuaternion &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] QQuaternion operator-(const QQuaternion &q1, const QQuaternion &q2)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QQuaternion` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QQuaternion`。
- 参数 `q1`：类型为 `const QQuaternion &`。没有默认值，调用时必须提供。传入 `const QQuaternion &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `q2`：类型为 `const QQuaternion &`。没有默认值，调用时必须提供。传入 `const QQuaternion &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr] QQuaternion operator/(const QQuaternion &quaternion, float divisor)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QQuaternion` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QQuaternion`。
- 参数 `quaternion`：类型为 `const QQuaternion &`。没有默认值，调用时必须提供。传入 `const QQuaternion &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `divisor`：类型为 `float`。没有默认值，调用时必须提供。传入 `float` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDataStream &operator<<(QDataStream &stream, const QQuaternion &quaternion)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QQuaternion` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDataStream &`。
- 参数 `stream`：类型为 `QDataStream &`。没有默认值，调用时必须提供。传入 `QDataStream &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `quaternion`：类型为 `const QQuaternion &`。没有默认值，调用时必须提供。传入 `const QQuaternion &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[constexpr noexcept] bool operator==(const QQuaternion &q1, const QQuaternion &q2)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QQuaternion` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `q1`：类型为 `const QQuaternion &`。没有默认值，调用时必须提供。传入 `const QQuaternion &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `q2`：类型为 `const QQuaternion &`。没有默认值，调用时必须提供。传入 `const QQuaternion &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QDataStream &operator>>(QDataStream &stream, QQuaternion &quaternion)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QQuaternion` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QDataStream &`。
- 参数 `stream`：类型为 `QDataStream &`。没有默认值，调用时必须提供。传入 `QDataStream &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `quaternion`：类型为 `QQuaternion &`。没有默认值，调用时必须提供。传入 `QQuaternion &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.11) struct Axes`

**API 类别：** 公有类型

**中文解读：** 这是 `QQuaternion` 的 `Axes` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.11) struct Axis`

**API 类别：** 公有类型

**中文解读：** 这是 `QQuaternion` 的 `Axis` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `(since 6.11) struct EulerAngles`

**API 类别：** 公有类型

**中文解读：** 这是 `QQuaternion` 的 `Euler、Angles` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

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

`QQuaternion` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
