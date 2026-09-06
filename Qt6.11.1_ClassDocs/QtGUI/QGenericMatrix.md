# QGenericMatrix

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QGenericMatrix` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QGenericMatrix>`
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

- `QGenericMatrix()`
- `QGenericMatrix(const T *values)`
- `const T * constData() const`
- `void copyDataTo(T *values) const`
- `T * data()`
- `const T * data() const`
- `void fill(T value)`
- `bool isIdentity() const`
- `void setToIdentity()`
- `QGenericMatrix<M, N, T> transposed() const`
- `bool operator!=(const QGenericMatrix<N, M, T> &other) const`
- `T & operator()(int row, int column)`
- `const T & operator()(int row, int column) const`
- `QGenericMatrix<N, M, T> & operator*=(T factor)`
- `QGenericMatrix<N, M, T> & operator+=(const QGenericMatrix<N, M, T> &other)`
- `QGenericMatrix<N, M, T> & operator-=(const QGenericMatrix<N, M, T> &other)`
- `QGenericMatrix<N, M, T> & operator/=(T divisor)`
- `bool operator==(const QGenericMatrix<N, M, T> &other) const`

### 相关非成员函数

- `QMatrix2x2`
- `QMatrix2x3`
- `QMatrix2x4`
- `QMatrix3x2`
- `QMatrix3x3`
- `QMatrix3x4`
- `QMatrix4x2`
- `QMatrix4x3`
- `QGenericMatrix<N, M, T> operator*(T factor, const QGenericMatrix<N, M, T> &matrix)`
- `QGenericMatrix<M1, M2, TT> operator*(const QGenericMatrix<NN, M2, TT> &m1, const QGenericMatrix<M1, NN, TT> &m2)`
- `QGenericMatrix<N, M, T> operator*(const QGenericMatrix<N, M, T> &matrix, T factor)`
- `QGenericMatrix<N, M, T> operator+(const QGenericMatrix<N, M, T> &m1, const QGenericMatrix<N, M, T> &m2)`
- `QGenericMatrix<N, M, T> operator-(const QGenericMatrix<N, M, T> &m1, const QGenericMatrix<N, M, T> &m2)`
- `QGenericMatrix<N, M, T> operator-(const QGenericMatrix<N, M, T> &matrix)`
- `QGenericMatrix<N, M, T> operator/(const QGenericMatrix<N, M, T> &matrix, T divisor)`
- `QDataStream & operator<<(QDataStream &stream, const QGenericMatrix<N, M, T> &matrix)`
- `QDataStream & operator>>(QDataStream &stream, QGenericMatrix<N, M, T> &matrix)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QGenericMatrix::QGenericMatrix()`

**作用与语义：**

构造一个NxM恒定矩阵。

### `[explicit] QGenericMatrix::QGenericMatrix(const T *values)`

**作用与语义：**

从给定的N * M浮点`values`构造一个矩阵。数组内容`values`假设按行大序排列。

### `const T *QGenericMatrix::constData() const`

**作用与语义：**

返回该矩阵原始数据的常数指针。

### `void QGenericMatrix::copyDataTo(T *values) const`

**作用与语义：**

检索该矩阵中的N * M项，并按行大序复制到`values`。

### `T *QGenericMatrix::data()`

**作用与语义：**

返回指向该矩阵原始数据的指针。

### `const T *QGenericMatrix::data() const`

**作用与语义：**

返回该矩阵原始数据的常数指针。

### `void QGenericMatrix::fill(T value)`

**作用与语义：**

用`value`填充该矩阵的所有元素。

### `bool QGenericMatrix::isIdentity() const`

**作用与语义：**

如果该矩阵是单位元，则返回`true`;否则为假。

### `void QGenericMatrix::setToIdentity()`

**作用与语义：**

将该矩阵映射为恒等式。

### `QGenericMatrix<M, N, T> QGenericMatrix::transposed() const`

**作用与语义：**

返回该矩阵，并围绕其对角线进行换置。

### `bool QGenericMatrix::operator!=(const QGenericMatrix<N, M, T> &other) const`

**作用与语义：**

如果该矩阵与`other`不相同，返回`true`;否则为假。

### `T &QGenericMatrix::operator()(int row, int column)`

**作用与语义：**

返回该矩阵中位置（`row`， `column`）的元素的引用，以便将该元素分配到。

### `const T &QGenericMatrix::operator()(int row, int column) const`

**作用与语义：**

返回该矩阵中位置（`row`， `column`）元素的常量引用。

### `QGenericMatrix<N, M, T> &QGenericMatrix::operator*=(T factor)`

**作用与语义：**

将该矩阵的所有元素乘以`factor`。

### `QGenericMatrix<N, M, T> &QGenericMatrix::operator+=(const QGenericMatrix<N, M, T> &other)`

**作用与语义：**

将`other`的内容添加到该矩阵中。

### `QGenericMatrix<N, M, T> &QGenericMatrix::operator-=(const QGenericMatrix<N, M, T> &other)`

**作用与语义：**

从该矩阵中减去`other`的内容。

### `QGenericMatrix<N, M, T> &QGenericMatrix::operator/=(T divisor)`

**作用与语义：**

将该矩阵的所有元素除以`divisor`。

### `bool QGenericMatrix::operator==(const QGenericMatrix<N, M, T> &other) const`

**作用与语义：**

如果该矩阵与`other`相同，则返回`true`;否则为假。

### `QMatrix2x2`

**作用与语义：**

QMatrix2x2 类型为 2 列、2 行和浮点（float）定义了 `QGenericMatrix` 模板的便捷实例化。

### `QMatrix2x3`

**作用与语义：**

QMatrix2x3类型定义了2列3行的`QGenericMatrix`模板的便捷实例，float作为元素类型。

### `QMatrix2x4`

**作用与语义：**

QMatrix2x4 类型为 2 列、4 行和 float 定义了 `QGenericMatrix` 模板的便捷实例化，作为元素类型。

### `QMatrix3x2`

**作用与语义：**

QMatrix3x2类型定义了3列、2行和float作为元素类型，方便地实现`QGenericMatrix`模板。

### `QMatrix3x3`

**作用与语义：**

QMatrix3x3 类型为 3 列、3 行和 float 定义了 `QGenericMatrix` 模板的便捷实例化。

### `QMatrix3x4`

**作用与语义：**

QMatrix3x4类型为`QGenericMatrix`模板的3列4行和float作为元素类型提供了便捷的实例化。

### `QMatrix4x2`

**作用与语义：**

QMatrix4x2 类型为 4 列、2 行和浮点（float）定义了 `QGenericMatrix` 模板的便捷实例化。

### `QMatrix4x3`

**作用与语义：**

QMatrix4x3 类型为 4 列、3 行和浮点（float）定义了 `QGenericMatrix` 模板的便捷实例化。

### `template < int N, int M, typename T > QGenericMatrix<N, M, T> operator*(T factor, const QGenericMatrix<N, M, T> &matrix)`

**作用与语义：**

返回将`matrix`的所有元素乘以`factor`的结果。

### `template < int NN, int M1, int M2, typename TT > QGenericMatrix<M1, M2, TT> operator*(const QGenericMatrix<NN, M2, TT> &m1, const QGenericMatrix<M1, NN, TT> &m2)`

**作用与语义：**

返回 NNxM2 矩阵的乘积`m1` 与 M1xNN 矩阵的乘积，`m2`生成 M1xM2 矩阵结果。

### `template < int N, int M, typename T > QGenericMatrix<N, M, T> operator*(const QGenericMatrix<N, M, T> &matrix, T factor)`

**作用与语义：**

返回将`matrix`的所有元素乘以`factor`的结果。

### `template < int N, int M, typename T > QGenericMatrix<N, M, T> operator+(const QGenericMatrix<N, M, T> &m1, const QGenericMatrix<N, M, T> &m2)`

**作用与语义：**

返回`m1`和`m2`的总和。

### `template < int N, int M, typename T > QGenericMatrix<N, M, T> operator-(const QGenericMatrix<N, M, T> &m1, const QGenericMatrix<N, M, T> &m2)`

**作用与语义：**

返回`m1`和`m2`的差额。

### `template < int N, int M, typename T > QGenericMatrix<N, M, T> operator-(const QGenericMatrix<N, M, T> &matrix)`

**作用与语义：**

返回`matrix`的否定。

### `template < int N, int M, typename T > QGenericMatrix<N, M, T> operator/(const QGenericMatrix<N, M, T> &matrix, T divisor)`

**作用与语义：**

返回将`matrix`的所有元素除以`divisor`的结果。

### `template < int N, int M, typename T > QDataStream &operator<<(QDataStream &stream, const QGenericMatrix<N, M, T> &matrix)`

**作用与语义：**

将给定`matrix`写入给定`stream`，并返回流的引用。

### `template < int N, int M, typename T > QDataStream &operator>>(QDataStream &stream, QGenericMatrix<N, M, T> &matrix)`

**作用与语义：**

将给定`stream`中的NxM矩阵读取到给定`matrix`，并返回对流的引用。

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

`QGenericMatrix` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
