# QRandomGenerator

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“RandomGenerator”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QRandomGenerator` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QRandomGenerator>`
- 继承自：未在类页中列出
- 直接派生类：QRandomGenerator64

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

- `result_type`

### 公有函数

- `QRandomGenerator(quint32 seedValue = 1)`
- `QRandomGenerator(const quint32 (&)[N] seedBuffer)`
- `QRandomGenerator(std::seed_seq &sseq)`
- `QRandomGenerator(const quint32 *begin, const quint32 *end)`
- `QRandomGenerator(const quint32 *seedBuffer, qsizetype len)`
- `QRandomGenerator(const QRandomGenerator &other)`
- `double bounded(double highest)`
- `int bounded(int highest)`
- `qint64 bounded(qint64 highest)`
- `quint32 bounded(quint32 highest)`
- `quint64 bounded(quint64 highest)`
- `int bounded(int lowest, int highest)`
- `qint64 bounded(int lowest, qint64 highest)`
- `qint64 bounded(qint64 lowest, int highest)`
- `qint64 bounded(qint64 lowest, qint64 highest)`
- `quint32 bounded(quint32 lowest, quint32 highest)`
- `quint64 bounded(quint64 lowest, quint64 highest)`
- `quint64 bounded(quint64 lowest, unsigned int highest)`
- `quint64 bounded(unsigned int lowest, quint64 highest)`
- `void discard(unsigned long long z)`
- `void fillRange(UInt (&)[N] buffer)`
- `void fillRange(UInt *buffer, qsizetype count)`
- `quint64 generate64()`
- `quint32 generate()`
- `void generate(ForwardIterator begin, ForwardIterator end)`
- `double generateDouble()`
- `void seed(quint32 seed = 1)`
- `void seed(std::seed_seq &seed)`
- `QRandomGenerator::result_type operator()()`

### 静态公有成员

- `QRandomGenerator * global()`
- `QRandomGenerator::result_type max()`
- `QRandomGenerator::result_type min()`
- `QRandomGenerator securelySeeded()`
- `QRandomGenerator * system()`

### 相关非成员函数

- `bool operator!=(const QRandomGenerator &rng1, const QRandomGenerator &rng2)`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 37 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `QRandomGenerator::result_type`

**API 类别：** 成员类型说明

**中文解读：** 这是 `QRandomGenerator` 的配置属性。初始化或状态切换时通过 `setResult_type(...)` 设置，之后用 `result_type()` 验证实际值；如果类提供变化信号，应让界面或业务逻辑连接信号，而不是反复轮询。

**签名拆解：**

- 属性类型：`:result_type`。
- 属性名：`QRandomGenerator`；读取和写入权限以签名前缀和对应访问函数为准。
- 使用时：写入属性可能触发布局、重绘、绑定或状态通知；读取结果只代表当前状态。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRandomGenerator::QRandomGenerator(quint32 seedValue = 1)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QRandomGenerator` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `seedValue`：类型为 `quint32`。默认值为 `1`。传入 `quint32` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <qsizetype N> QRandomGenerator::QRandomGenerator(const quint32 (&)[N] seedBuffer)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QRandomGenerator` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `seedBuffer`：类型为 `const quint32 (&)[N]`。没有默认值，调用时必须提供。传入 `const quint32 (&)[N]` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QRandomGenerator::QRandomGenerator(std::seed_seq &sseq)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QRandomGenerator` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `sseq`：类型为 `std::seed_seq &`。没有默认值，调用时必须提供。传入 `std::seed_seq &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRandomGenerator::QRandomGenerator(const quint32 *begin, const quint32 *end)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QRandomGenerator` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `begin`：类型为 `const quint32 *`。没有默认值，调用时必须提供。传入 `const quint32 *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `end`：类型为 `const quint32 *`。没有默认值，调用时必须提供。传入 `const quint32 *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRandomGenerator::QRandomGenerator(const quint32 *seedBuffer, qsizetype len)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QRandomGenerator` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `seedBuffer`：类型为 `const quint32 *`。没有默认值，调用时必须提供。传入 `const quint32 *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `len`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRandomGenerator::QRandomGenerator(const QRandomGenerator &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QRandomGenerator` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `const QRandomGenerator &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `double QRandomGenerator::bounded(double highest)`

**API 类别：** 成员函数说明

**中文解读：** `QRandomGenerator::bounded` 用于计算、查询或取得与“bounded”相关的操作。调用时要先确认当前状态和 `highest` 的有效范围；返回类型是 `double`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`double`。
- 参数 `highest`：类型为 `double`。没有默认值，调用时必须提供。传入 `double` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QRandomGenerator::bounded(int highest)`

**API 类别：** 成员函数说明

**中文解读：** `QRandomGenerator::bounded` 用于计算、查询或取得与“bounded”相关的操作。调用时要先确认当前状态和 `highest` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `highest`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qint64 QRandomGenerator::bounded(qint64 highest)`

**API 类别：** 成员函数说明

**中文解读：** `QRandomGenerator::bounded` 用于计算、查询或取得与“bounded”相关的操作。调用时要先确认当前状态和 `highest` 的有效范围；返回类型是 `qint64`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qint64`。
- 参数 `highest`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `quint32 QRandomGenerator::bounded(quint32 highest)`

**API 类别：** 成员函数说明

**中文解读：** `QRandomGenerator::bounded` 用于计算、查询或取得与“bounded”相关的操作。调用时要先确认当前状态和 `highest` 的有效范围；返回类型是 `quint32`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`quint32`。
- 参数 `highest`：类型为 `quint32`。没有默认值，调用时必须提供。传入 `quint32` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `quint64 QRandomGenerator::bounded(quint64 highest)`

**API 类别：** 成员函数说明

**中文解读：** `QRandomGenerator::bounded` 用于计算、查询或取得与“bounded”相关的操作。调用时要先确认当前状态和 `highest` 的有效范围；返回类型是 `quint64`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`quint64`。
- 参数 `highest`：类型为 `quint64`。没有默认值，调用时必须提供。传入 `quint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `int QRandomGenerator::bounded(int lowest, int highest)`

**API 类别：** 成员函数说明

**中文解读：** `QRandomGenerator::bounded` 用于计算、查询或取得与“bounded”相关的操作。调用时要先确认当前状态和 `lowest`、`highest` 的有效范围；返回类型是 `int`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`int`。
- 参数 `lowest`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `highest`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `quint64 QRandomGenerator::bounded(quint64 lowest, unsigned int highest)`

**API 类别：** 成员函数说明

**中文解读：** `QRandomGenerator::bounded` 用于计算、查询或取得与“bounded”相关的操作。调用时要先确认当前状态和 `lowest`、`highest` 的有效范围；返回类型是 `quint64`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`quint64`。
- 参数 `lowest`：类型为 `quint64`。没有默认值，调用时必须提供。传入 `quint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `highest`：类型为 `unsigned int`。没有默认值，调用时必须提供。传入 `unsigned int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qint64 QRandomGenerator::bounded(qint64 lowest, qint64 highest)`

**API 类别：** 成员函数说明

**中文解读：** `QRandomGenerator::bounded` 用于计算、查询或取得与“bounded”相关的操作。调用时要先确认当前状态和 `lowest`、`highest` 的有效范围；返回类型是 `qint64`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qint64`。
- 参数 `lowest`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `highest`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `quint32 QRandomGenerator::bounded(quint32 lowest, quint32 highest)`

**API 类别：** 成员函数说明

**中文解读：** `QRandomGenerator::bounded` 用于计算、查询或取得与“bounded”相关的操作。调用时要先确认当前状态和 `lowest`、`highest` 的有效范围；返回类型是 `quint32`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`quint32`。
- 参数 `lowest`：类型为 `quint32`。没有默认值，调用时必须提供。传入 `quint32` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `highest`：类型为 `quint32`。没有默认值，调用时必须提供。传入 `quint32` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `quint64 QRandomGenerator::bounded(quint64 lowest, quint64 highest)`

**API 类别：** 成员函数说明

**中文解读：** `QRandomGenerator::bounded` 用于计算、查询或取得与“bounded”相关的操作。调用时要先确认当前状态和 `lowest`、`highest` 的有效范围；返回类型是 `quint64`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`quint64`。
- 参数 `lowest`：类型为 `quint64`。没有默认值，调用时必须提供。传入 `quint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `highest`：类型为 `quint64`。没有默认值，调用时必须提供。传入 `quint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRandomGenerator::discard(unsigned long long z)`

**API 类别：** 成员函数说明

**中文解读：** `QRandomGenerator::discard` 用于执行与“discard”相关的操作。调用时要先确认当前状态和 `z` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `z`：类型为 `unsigned long long`。没有默认值，调用时必须提供。传入 `unsigned long long` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template < typename UInt, size_t N, QRandomGenerator::IfValidUInt<UInt> = true > void QRandomGenerator::fillRange(UInt (&)[N] buffer)`

**API 类别：** 成员函数说明

**中文解读：** `QRandomGenerator::fillRange` 用于计算、查询或取得与“fill、Range”相关的操作。调用时要先确认当前状态和 `buffer` 的有效范围；返回类型是 `template < typename UInt, size_t N, QRandomGenerator::IfValidUInt<UInt> = true > void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template < typename UInt, size_t N, QRandomGenerator::IfValidUInt<UInt> = true > void`。
- 参数 `buffer`：类型为 `UInt (&)[N]`。没有默认值，调用时必须提供。传入 `UInt (&)[N]` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename UInt, QRandomGenerator::IfValidUInt<UInt> = true> void QRandomGenerator::fillRange(UInt *buffer, qsizetype count)`

**API 类别：** 成员函数说明

**中文解读：** `QRandomGenerator::fillRange` 用于计算、查询或取得与“fill、Range”相关的操作。调用时要先确认当前状态和 `buffer`、`count` 的有效范围；返回类型是 `template <typename UInt, QRandomGenerator::IfValidUInt<UInt> = true> void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename UInt, QRandomGenerator::IfValidUInt<UInt> = true> void`。
- 参数 `buffer`：类型为 `UInt *`。没有默认值，调用时必须提供。传入 `UInt *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `count`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `quint64 QRandomGenerator::generate64()`

**API 类别：** 成员函数说明

**中文解读：** `QRandomGenerator::generate64` 用于计算、查询或取得与“generate、64”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `quint64`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`quint64`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `quint32 QRandomGenerator::generate()`

**API 类别：** 成员函数说明

**中文解读：** `QRandomGenerator::generate` 用于计算、查询或取得与“generate”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `quint32`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`quint32`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `template <typename ForwardIterator> void QRandomGenerator::generate(ForwardIterator begin, ForwardIterator end)`

**API 类别：** 成员函数说明

**中文解读：** `QRandomGenerator::generate` 用于计算、查询或取得与“generate”相关的操作。调用时要先确认当前状态和 `begin`、`end` 的有效范围；返回类型是 `template <typename ForwardIterator> void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`template <typename ForwardIterator> void`。
- 参数 `begin`：类型为 `ForwardIterator`。没有默认值，调用时必须提供。传入 `ForwardIterator` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `end`：类型为 `ForwardIterator`。没有默认值，调用时必须提供。传入 `ForwardIterator` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `double QRandomGenerator::generateDouble()`

**API 类别：** 成员函数说明

**中文解读：** `QRandomGenerator::generateDouble` 用于计算、查询或取得与“generate、Double”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `double`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`double`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QRandomGenerator *QRandomGenerator::global()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `global`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QRandomGenerator *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static constexpr] QRandomGenerator::result_type QRandomGenerator::max()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `max`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QRandomGenerator::result_type`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static constexpr] QRandomGenerator::result_type QRandomGenerator::min()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `min`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QRandomGenerator::result_type`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QRandomGenerator QRandomGenerator::securelySeeded()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `securelySeeded`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QRandomGenerator`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QRandomGenerator::seed(quint32 seed = 1)`

**API 类别：** 成员函数说明

**中文解读：** `QRandomGenerator::seed` 用于执行与“seed”相关的操作。调用时要先确认当前状态和 `seed` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `seed`：类型为 `quint32`。默认值为 `1`。传入 `quint32` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] void QRandomGenerator::seed(std::seed_seq &seed)`

**API 类别：** 成员函数说明

**中文解读：** `QRandomGenerator::seed` 用于执行与“seed”相关的操作。调用时要先确认当前状态和 `seed` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `seed`：类型为 `std::seed_seq &`。没有默认值，调用时必须提供。传入 `std::seed_seq &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static] QRandomGenerator *QRandomGenerator::system()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `system`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`QRandomGenerator *`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QRandomGenerator::result_type QRandomGenerator::operator()()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QRandomGenerator` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QRandomGenerator::result_type`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool operator!=(const QRandomGenerator &rng1, const QRandomGenerator &rng2)`

**API 类别：** 相关非成员函数

**中文解读：** 这是 `QRandomGenerator` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`bool`。
- 参数 `rng1`：类型为 `const QRandomGenerator &`。没有默认值，调用时必须提供。传入 `const QRandomGenerator &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `rng2`：类型为 `const QRandomGenerator &`。没有默认值，调用时必须提供。传入 `const QRandomGenerator &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `result_type`

**API 类别：** 公有类型

**中文解读：** 这是 `QRandomGenerator` 的 `结果、类型` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qint64 bounded(int lowest, qint64 highest)`

**API 类别：** 公有函数

**中文解读：** `QRandomGenerator::bounded` 用于计算、查询或取得与“bounded”相关的操作。调用时要先确认当前状态和 `lowest`、`highest` 的有效范围；返回类型是 `qint64`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qint64`。
- 参数 `lowest`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `highest`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qint64 bounded(qint64 lowest, int highest)`

**API 类别：** 公有函数

**中文解读：** `QRandomGenerator::bounded` 用于计算、查询或取得与“bounded”相关的操作。调用时要先确认当前状态和 `lowest`、`highest` 的有效范围；返回类型是 `qint64`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qint64`。
- 参数 `lowest`：类型为 `qint64`。没有默认值，调用时必须提供。传入 `qint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `highest`：类型为 `int`。没有默认值，调用时必须提供。传入 `int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `quint64 bounded(unsigned int lowest, quint64 highest)`

**API 类别：** 公有函数

**中文解读：** `QRandomGenerator::bounded` 用于计算、查询或取得与“bounded”相关的操作。调用时要先确认当前状态和 `lowest`、`highest` 的有效范围；返回类型是 `quint64`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`quint64`。
- 参数 `lowest`：类型为 `unsigned int`。没有默认值，调用时必须提供。传入 `unsigned int` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `highest`：类型为 `quint64`。没有默认值，调用时必须提供。传入 `quint64` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

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

`QRandomGenerator` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
