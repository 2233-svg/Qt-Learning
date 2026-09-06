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

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 35 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `QGenericMatrix::QGenericMatrix()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QGenericMatrix` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[explicit] QGenericMatrix::QGenericMatrix(const T *values)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QGenericMatrix` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `values`：类型为 `const T *`。没有默认值，调用时必须提供。传入 `const T *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const T *QGenericMatrix::constData() const`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `constData`，用于取得 `QGenericMatrix` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`const T *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QGenericMatrix::copyDataTo(T *values) const`

**API 类别：** 成员函数说明

**中文解读：** `QGenericMatrix::copyDataTo` 用于执行与“copy、数据访问、转换输出”相关的操作。调用时要先确认当前状态和 `values` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `values`：类型为 `T *`。没有默认值，调用时必须提供。传入 `T *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T *QGenericMatrix::data()`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `data`，用于取得 `QGenericMatrix` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`T *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const T *QGenericMatrix::data() const`

**API 类别：** 成员函数说明

**中文解读：** 这是数据访问 API `data`，用于取得 `QGenericMatrix` 当前的元素、字段或底层存储。读取前确认索引/键有效；如果返回引用或指针，不要让它跨越对象修改、容器扩容或临时对象生命周期。

**签名拆解：**

- 返回值：`const T *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QGenericMatrix::fill(T value)`

**API 类别：** 成员函数说明

**中文解读：** `QGenericMatrix::fill` 用于执行与“fill”相关的操作。调用时要先确认当前状态和 `value` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `value`：类型为 `T`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QGenericMatrix::isIdentity() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `isIdentity`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QGenericMatrix::setToIdentity()`

**API 类别：** 成员函数说明

**中文解读：** 这是配置/写入操作 `setToIdentity`。调用它会改变 `QGenericMatrix` 的状态，必要时触发属性通知、重新布局、重新绘制或后续异步任务；调用顺序要遵守构造和状态前置条件。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QGenericMatrix<M, N, T> QGenericMatrix::transposed() const`

**API 类别：** 成员函数说明

**中文解读：** `QGenericMatrix::transposed` 用于计算、查询或取得与“transposed”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `QGenericMatrix<M, N, T>`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`QGenericMatrix<M, N, T>`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QGenericMatrix::operator!=(const QGenericMatrix<N, M, T> &other) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QGenericMatrix` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `other`：类型为 `const QGenericMatrix<N, M, T> &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T &QGenericMatrix::operator()(int row, int column)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QGenericMatrix` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`T &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `const T &QGenericMatrix::operator()(int row, int column) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QGenericMatrix` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`const T &`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QGenericMatrix<N, M, T> &QGenericMatrix::operator*=(T factor)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QGenericMatrix` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QGenericMatrix<N, M, T> &`。
- 参数 `factor`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QGenericMatrix<N, M, T> &QGenericMatrix::operator+=(const QGenericMatrix<N, M, T> &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QGenericMatrix` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QGenericMatrix<N, M, T> &`。
- 参数 `other`：类型为 `const QGenericMatrix<N, M, T> &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QGenericMatrix<N, M, T> &QGenericMatrix::operator-=(const QGenericMatrix<N, M, T> &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QGenericMatrix` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QGenericMatrix<N, M, T> &`。
- 参数 `other`：类型为 `const QGenericMatrix<N, M, T> &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QGenericMatrix<N, M, T> &QGenericMatrix::operator/=(T divisor)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QGenericMatrix` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QGenericMatrix<N, M, T> &`。
- 参数 `divisor`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QGenericMatrix::operator==(const QGenericMatrix<N, M, T> &other) const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QGenericMatrix` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `other`：类型为 `const QGenericMatrix<N, M, T> &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMatrix2x2`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QGenericMatrix` 的 `Q、Matrix、2、x、2` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMatrix2x3`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QGenericMatrix` 的 `Q、Matrix、2、x、3` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMatrix2x4`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QGenericMatrix` 的 `Q、Matrix、2、x、4` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMatrix3x2`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QGenericMatrix` 的 `Q、Matrix、3、x、2` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMatrix3x3`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QGenericMatrix` 的 `Q、Matrix、3、x、3` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMatrix3x4`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QGenericMatrix` 的 `Q、Matrix、3、x、4` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMatrix4x2`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QGenericMatrix` 的 `Q、Matrix、4、x、2` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QMatrix4x3`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QGenericMatrix` 的 `Q、Matrix、4、x、3` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template < int N, int M, typename T > QGenericMatrix<N, M, T> operator*(T factor, const QGenericMatrix<N, M, T> &matrix)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QGenericMatrix` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`template < int N, int M, typename T > QGenericMatrix<N, M, T>`。
- 参数 `factor`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `matrix`：类型为 `const QGenericMatrix<N, M, T> &`。没有默认值，调用时必须提供。传入 `const QGenericMatrix<N, M, T> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template < int NN, int M1, int M2, typename TT > QGenericMatrix<M1, M2, TT> operator*(const QGenericMatrix<NN, M2, TT> &m1, const QGenericMatrix<M1, NN, TT> &m2)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QGenericMatrix` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`template < int NN, int M1, int M2, typename TT > QGenericMatrix<M1, M2, TT>`。
- 参数 `m1`：类型为 `const QGenericMatrix<NN, M2, TT> &`。没有默认值，调用时必须提供。传入 `const QGenericMatrix<NN, M2, TT> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `m2`：类型为 `const QGenericMatrix<M1, NN, TT> &`。没有默认值，调用时必须提供。传入 `const QGenericMatrix<M1, NN, TT> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template < int N, int M, typename T > QGenericMatrix<N, M, T> operator*(const QGenericMatrix<N, M, T> &matrix, T factor)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QGenericMatrix` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`template < int N, int M, typename T > QGenericMatrix<N, M, T>`。
- 参数 `matrix`：类型为 `const QGenericMatrix<N, M, T> &`。没有默认值，调用时必须提供。传入 `const QGenericMatrix<N, M, T> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `factor`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template < int N, int M, typename T > QGenericMatrix<N, M, T> operator+(const QGenericMatrix<N, M, T> &m1, const QGenericMatrix<N, M, T> &m2)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QGenericMatrix` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`template < int N, int M, typename T > QGenericMatrix<N, M, T>`。
- 参数 `m1`：类型为 `const QGenericMatrix<N, M, T> &`。没有默认值，调用时必须提供。传入 `const QGenericMatrix<N, M, T> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `m2`：类型为 `const QGenericMatrix<N, M, T> &`。没有默认值，调用时必须提供。传入 `const QGenericMatrix<N, M, T> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template < int N, int M, typename T > QGenericMatrix<N, M, T> operator-(const QGenericMatrix<N, M, T> &m1, const QGenericMatrix<N, M, T> &m2)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QGenericMatrix` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`template < int N, int M, typename T > QGenericMatrix<N, M, T>`。
- 参数 `m1`：类型为 `const QGenericMatrix<N, M, T> &`。没有默认值，调用时必须提供。传入 `const QGenericMatrix<N, M, T> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `m2`：类型为 `const QGenericMatrix<N, M, T> &`。没有默认值，调用时必须提供。传入 `const QGenericMatrix<N, M, T> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template < int N, int M, typename T > QGenericMatrix<N, M, T> operator-(const QGenericMatrix<N, M, T> &matrix)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QGenericMatrix` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`template < int N, int M, typename T > QGenericMatrix<N, M, T>`。
- 参数 `matrix`：类型为 `const QGenericMatrix<N, M, T> &`。没有默认值，调用时必须提供。传入 `const QGenericMatrix<N, M, T> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template < int N, int M, typename T > QGenericMatrix<N, M, T> operator/(const QGenericMatrix<N, M, T> &matrix, T divisor)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QGenericMatrix` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`template < int N, int M, typename T > QGenericMatrix<N, M, T>`。
- 参数 `matrix`：类型为 `const QGenericMatrix<N, M, T> &`。没有默认值，调用时必须提供。传入 `const QGenericMatrix<N, M, T> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `divisor`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template < int N, int M, typename T > QDataStream &operator<<(QDataStream &stream, const QGenericMatrix<N, M, T> &matrix)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QGenericMatrix` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`template < int N, int M, typename T > QDataStream &`。
- 参数 `stream`：类型为 `QDataStream &`。没有默认值，调用时必须提供。传入 `QDataStream &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `matrix`：类型为 `const QGenericMatrix<N, M, T> &`。没有默认值，调用时必须提供。传入 `const QGenericMatrix<N, M, T> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template < int N, int M, typename T > QDataStream &operator>>(QDataStream &stream, QGenericMatrix<N, M, T> &matrix)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QGenericMatrix` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`template < int N, int M, typename T > QDataStream &`。
- 参数 `stream`：类型为 `QDataStream &`。没有默认值，调用时必须提供。传入 `QDataStream &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `matrix`：类型为 `QGenericMatrix<N, M, T> &`。没有默认值，调用时必须提供。传入 `QGenericMatrix<N, M, T> &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

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

`QGenericMatrix` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
