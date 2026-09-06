# QAtomicInteger

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“AtomicInteger”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QAtomicInteger` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QAtomicInteger>`
- 继承自：未在类页中列出
- 直接派生类：QAtomicInt

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

### 公有函数

- `QAtomicInteger(T value = 0)`
- `QAtomicInteger(const QAtomicInteger<T> &other)`
- `bool deref()`
- `T fetchAndAddAcquire(T valueToAdd)`
- `T fetchAndAddOrdered(T valueToAdd)`
- `T fetchAndAddRelaxed(T valueToAdd)`
- `T fetchAndAddRelease(T valueToAdd)`
- `T fetchAndAndAcquire(T valueToAnd)`
- `T fetchAndAndOrdered(T valueToAnd)`
- `T fetchAndAndRelaxed(T valueToAnd)`
- `T fetchAndAndRelease(T valueToAnd)`
- `T fetchAndOrAcquire(T valueToOr)`
- `T fetchAndOrOrdered(T valueToOr)`
- `T fetchAndOrRelaxed(T valueToOr)`
- `T fetchAndOrRelease(T valueToOr)`
- `T fetchAndStoreAcquire(T newValue)`
- `T fetchAndStoreOrdered(T newValue)`
- `T fetchAndStoreRelaxed(T newValue)`
- `T fetchAndStoreRelease(T newValue)`
- `T fetchAndSubAcquire(T valueToSub)`
- `T fetchAndSubOrdered(T valueToSub)`
- `T fetchAndSubRelaxed(T valueToSub)`
- `T fetchAndSubRelease(T valueToSub)`
- `T fetchAndXorAcquire(T valueToXor)`
- `T fetchAndXorOrdered(T valueToXor)`
- `T fetchAndXorRelaxed(T valueToXor)`
- `T fetchAndXorRelease(T valueToXor)`
- `T loadAcquire() const`
- `T loadRelaxed() const`
- `bool ref()`
- `void storeRelaxed(T newValue)`
- `void storeRelease(T newValue)`
- `bool testAndSetAcquire(T expectedValue, T newValue)`
- `bool testAndSetAcquire(T expectedValue, T newValue, T &currentValue)`
- `bool testAndSetOrdered(T expectedValue, T newValue)`
- `bool testAndSetOrdered(T expectedValue, T newValue, T &currentValue)`
- `bool testAndSetRelaxed(T expectedValue, T newValue)`
- `bool testAndSetRelaxed(T expectedValue, T newValue, T &currentValue)`
- `bool testAndSetRelease(T expectedValue, T newValue)`
- `bool testAndSetRelease(T expectedValue, T newValue, T &currentValue)`
- `operator T() const`
- `T operator&=(T value)`
- `T operator++()`
- `T operator++(int)`
- `T operator+=(T value)`
- `T operator--()`
- `T operator--(int)`
- `T operator-=(T value)`
- `QAtomicInteger<T> & operator=(T)`
- `QAtomicInteger<T> & operator=(const QAtomicInteger<T> &other)`
- `T operator^=(T value)`
- `T operator|=(T value)`

### 静态公有成员

- `bool isFetchAndAddNative()`
- `bool isFetchAndAddWaitFree()`
- `bool isFetchAndStoreNative()`
- `bool isFetchAndStoreWaitFree()`
- `bool isReferenceCountingNative()`
- `bool isReferenceCountingWaitFree()`
- `bool isTestAndSetNative()`
- `bool isTestAndSetWaitFree()`

### 相关非成员函数

- `(since 6.7) void qYieldCpu()`

### 公开宏

- `Q_ATOMIC_INTnn_FETCH_AND_ADD_IS_ALWAYS_NATIVE`
- `Q_ATOMIC_INTnn_FETCH_AND_ADD_IS_NOT_NATIVE`
- `Q_ATOMIC_INTnn_FETCH_AND_ADD_IS_SOMETIMES_NATIVE`
- `Q_ATOMIC_INTnn_FETCH_AND_ADD_IS_WAIT_FREE`
- `Q_ATOMIC_INTnn_FETCH_AND_STORE_IS_ALWAYS_NATIVE`
- `Q_ATOMIC_INTnn_FETCH_AND_STORE_IS_NOT_NATIVE`
- `Q_ATOMIC_INTnn_FETCH_AND_STORE_IS_SOMETIMES_NATIVE`
- `Q_ATOMIC_INTnn_FETCH_AND_STORE_IS_WAIT_FREE`
- `Q_ATOMIC_INTnn_IS_SUPPORTED`
- `Q_ATOMIC_INTnn_REFERENCE_COUNTING_IS_ALWAYS_NATIVE`
- `Q_ATOMIC_INTnn_REFERENCE_COUNTING_IS_NOT_NATIVE`
- `Q_ATOMIC_INTnn_REFERENCE_COUNTING_IS_SOMETIMES_NATIVE`
- `Q_ATOMIC_INTnn_REFERENCE_COUNTING_IS_WAIT_FREE`
- `Q_ATOMIC_INTnn_TEST_AND_SET_IS_ALWAYS_NATIVE`
- `Q_ATOMIC_INTnn_TEST_AND_SET_IS_NOT_NATIVE`
- `Q_ATOMIC_INTnn_TEST_AND_SET_IS_SOMETIMES_NATIVE`
- `Q_ATOMIC_INTnn_TEST_AND_SET_IS_WAIT_FREE`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 78 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `[constexpr noexcept] QAtomicInteger::QAtomicInteger(T value = 0)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAtomicInteger` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `value`：类型为 `T`。默认值为 `0`。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QAtomicInteger::QAtomicInteger(const QAtomicInteger<T> &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAtomicInteger` 的构造函数。先确认参数代表的依赖、父对象或配置，再决定栈上创建、设置 parent，还是交给 Qt 工厂/容器管理；构造完成后才可以调用其他成员。

**签名拆解：**

- 返回值：构造函数，不返回对象值。
- 参数 `other`：类型为 `const QAtomicInteger<T> &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QAtomicInteger::deref()`

**API 类别：** 成员函数说明

**中文解读：** `QAtomicInteger::deref` 用于计算、查询或取得与“deref”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T QAtomicInteger::fetchAndAddAcquire(T valueToAdd)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAtomicInteger` 的核心操作 `fetchAndAddAcquire`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`T`。
- 参数 `valueToAdd`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T QAtomicInteger::fetchAndAddOrdered(T valueToAdd)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAtomicInteger` 的核心操作 `fetchAndAddOrdered`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`T`。
- 参数 `valueToAdd`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T QAtomicInteger::fetchAndAddRelaxed(T valueToAdd)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAtomicInteger` 的核心操作 `fetchAndAddRelaxed`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`T`。
- 参数 `valueToAdd`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T QAtomicInteger::fetchAndAddRelease(T valueToAdd)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAtomicInteger` 的核心操作 `fetchAndAddRelease`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`T`。
- 参数 `valueToAdd`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T QAtomicInteger::fetchAndAndAcquire(T valueToAnd)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAtomicInteger` 的核心操作 `fetchAndAndAcquire`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`T`。
- 参数 `valueToAnd`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T QAtomicInteger::fetchAndAndOrdered(T valueToAnd)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAtomicInteger` 的核心操作 `fetchAndAndOrdered`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`T`。
- 参数 `valueToAnd`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T QAtomicInteger::fetchAndAndRelaxed(T valueToAnd)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAtomicInteger` 的核心操作 `fetchAndAndRelaxed`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`T`。
- 参数 `valueToAnd`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T QAtomicInteger::fetchAndAndRelease(T valueToAnd)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAtomicInteger` 的核心操作 `fetchAndAndRelease`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`T`。
- 参数 `valueToAnd`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T QAtomicInteger::fetchAndOrAcquire(T valueToOr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAtomicInteger` 的核心操作 `fetchAndOrAcquire`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`T`。
- 参数 `valueToOr`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T QAtomicInteger::fetchAndOrOrdered(T valueToOr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAtomicInteger` 的核心操作 `fetchAndOrOrdered`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`T`。
- 参数 `valueToOr`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T QAtomicInteger::fetchAndOrRelaxed(T valueToOr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAtomicInteger` 的核心操作 `fetchAndOrRelaxed`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`T`。
- 参数 `valueToOr`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T QAtomicInteger::fetchAndOrRelease(T valueToOr)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAtomicInteger` 的核心操作 `fetchAndOrRelease`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`T`。
- 参数 `valueToOr`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T QAtomicInteger::fetchAndStoreAcquire(T newValue)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAtomicInteger` 的核心操作 `fetchAndStoreAcquire`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`T`。
- 参数 `newValue`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T QAtomicInteger::fetchAndStoreOrdered(T newValue)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAtomicInteger` 的核心操作 `fetchAndStoreOrdered`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`T`。
- 参数 `newValue`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T QAtomicInteger::fetchAndStoreRelaxed(T newValue)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAtomicInteger` 的核心操作 `fetchAndStoreRelaxed`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`T`。
- 参数 `newValue`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T QAtomicInteger::fetchAndStoreRelease(T newValue)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAtomicInteger` 的核心操作 `fetchAndStoreRelease`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`T`。
- 参数 `newValue`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T QAtomicInteger::fetchAndSubAcquire(T valueToSub)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAtomicInteger` 的核心操作 `fetchAndSubAcquire`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`T`。
- 参数 `valueToSub`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T QAtomicInteger::fetchAndSubOrdered(T valueToSub)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAtomicInteger` 的核心操作 `fetchAndSubOrdered`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`T`。
- 参数 `valueToSub`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T QAtomicInteger::fetchAndSubRelaxed(T valueToSub)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAtomicInteger` 的核心操作 `fetchAndSubRelaxed`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`T`。
- 参数 `valueToSub`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T QAtomicInteger::fetchAndSubRelease(T valueToSub)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAtomicInteger` 的核心操作 `fetchAndSubRelease`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`T`。
- 参数 `valueToSub`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T QAtomicInteger::fetchAndXorAcquire(T valueToXor)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAtomicInteger` 的核心操作 `fetchAndXorAcquire`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`T`。
- 参数 `valueToXor`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T QAtomicInteger::fetchAndXorOrdered(T valueToXor)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAtomicInteger` 的核心操作 `fetchAndXorOrdered`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`T`。
- 参数 `valueToXor`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T QAtomicInteger::fetchAndXorRelaxed(T valueToXor)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAtomicInteger` 的核心操作 `fetchAndXorRelaxed`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`T`。
- 参数 `valueToXor`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T QAtomicInteger::fetchAndXorRelease(T valueToXor)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAtomicInteger` 的核心操作 `fetchAndXorRelease`。先确认输入类型、当前状态和线程要求，再根据返回值/输出参数读取结果；对文件、网络、数据库和绘制 API 要同时处理失败或部分完成情况。

**签名拆解：**

- 返回值：`T`。
- 参数 `valueToXor`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static constexpr] bool QAtomicInteger::isFetchAndAddNative()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `isFetchAndAddNative`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static constexpr] bool QAtomicInteger::isFetchAndAddWaitFree()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `isFetchAndAddWaitFree`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static constexpr] bool QAtomicInteger::isFetchAndStoreNative()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `isFetchAndStoreNative`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static constexpr] bool QAtomicInteger::isFetchAndStoreWaitFree()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `isFetchAndStoreWaitFree`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static constexpr] bool QAtomicInteger::isReferenceCountingNative()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `isReferenceCountingNative`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static constexpr] bool QAtomicInteger::isReferenceCountingWaitFree()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `isReferenceCountingWaitFree`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static constexpr] bool QAtomicInteger::isTestAndSetNative()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `isTestAndSetNative`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[static constexpr] bool QAtomicInteger::isTestAndSetWaitFree()`

**API 类别：** 成员函数说明

**中文解读：** 这是静态工具 API `isTestAndSetWaitFree`，不依赖某个实例的运行时状态。适合直接完成转换、查找、工厂创建或一次性操作；调用前仍要检查返回值和错误输出。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T QAtomicInteger::loadAcquire() const`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `loadAcquire`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`T`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T QAtomicInteger::loadRelaxed() const`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `loadRelaxed`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`T`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QAtomicInteger::ref()`

**API 类别：** 成员函数说明

**中文解读：** `QAtomicInteger::ref` 用于计算、查询或取得与“ref”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QAtomicInteger::storeRelaxed(T newValue)`

**API 类别：** 成员函数说明

**中文解读：** `QAtomicInteger::storeRelaxed` 用于执行与“store、Relaxed”相关的操作。调用时要先确认当前状态和 `newValue` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `newValue`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QAtomicInteger::storeRelease(T newValue)`

**API 类别：** 成员函数说明

**中文解读：** `QAtomicInteger::storeRelease` 用于执行与“store、释放”相关的操作。调用时要先确认当前状态和 `newValue` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `newValue`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QAtomicInteger::testAndSetAcquire(T expectedValue, T newValue)`

**API 类别：** 成员函数说明

**中文解读：** `QAtomicInteger::testAndSetAcquire` 用于计算、查询或取得与“test、And、设置、Acquire”相关的操作。调用时要先确认当前状态和 `expectedValue`、`newValue` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `expectedValue`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `newValue`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QAtomicInteger::testAndSetAcquire(T expectedValue, T newValue, T &currentValue)`

**API 类别：** 成员函数说明

**中文解读：** `QAtomicInteger::testAndSetAcquire` 用于计算、查询或取得与“test、And、设置、Acquire”相关的操作。调用时要先确认当前状态和 `expectedValue`、`newValue`、`currentValue` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `expectedValue`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `newValue`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `currentValue`：类型为 `T &`。没有默认值，调用时必须提供。传入 `T &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QAtomicInteger::testAndSetOrdered(T expectedValue, T newValue)`

**API 类别：** 成员函数说明

**中文解读：** `QAtomicInteger::testAndSetOrdered` 用于计算、查询或取得与“test、And、设置、Ordered”相关的操作。调用时要先确认当前状态和 `expectedValue`、`newValue` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `expectedValue`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `newValue`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QAtomicInteger::testAndSetOrdered(T expectedValue, T newValue, T &currentValue)`

**API 类别：** 成员函数说明

**中文解读：** `QAtomicInteger::testAndSetOrdered` 用于计算、查询或取得与“test、And、设置、Ordered”相关的操作。调用时要先确认当前状态和 `expectedValue`、`newValue`、`currentValue` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `expectedValue`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `newValue`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `currentValue`：类型为 `T &`。没有默认值，调用时必须提供。传入 `T &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QAtomicInteger::testAndSetRelaxed(T expectedValue, T newValue)`

**API 类别：** 成员函数说明

**中文解读：** `QAtomicInteger::testAndSetRelaxed` 用于计算、查询或取得与“test、And、设置、Relaxed”相关的操作。调用时要先确认当前状态和 `expectedValue`、`newValue` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `expectedValue`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `newValue`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QAtomicInteger::testAndSetRelaxed(T expectedValue, T newValue, T &currentValue)`

**API 类别：** 成员函数说明

**中文解读：** `QAtomicInteger::testAndSetRelaxed` 用于计算、查询或取得与“test、And、设置、Relaxed”相关的操作。调用时要先确认当前状态和 `expectedValue`、`newValue`、`currentValue` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `expectedValue`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `newValue`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `currentValue`：类型为 `T &`。没有默认值，调用时必须提供。传入 `T &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QAtomicInteger::testAndSetRelease(T expectedValue, T newValue)`

**API 类别：** 成员函数说明

**中文解读：** `QAtomicInteger::testAndSetRelease` 用于计算、查询或取得与“test、And、设置、释放”相关的操作。调用时要先确认当前状态和 `expectedValue`、`newValue` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `expectedValue`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `newValue`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QAtomicInteger::testAndSetRelease(T expectedValue, T newValue, T &currentValue)`

**API 类别：** 成员函数说明

**中文解读：** `QAtomicInteger::testAndSetRelease` 用于计算、查询或取得与“test、And、设置、释放”相关的操作。调用时要先确认当前状态和 `expectedValue`、`newValue`、`currentValue` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `expectedValue`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `newValue`：类型为 `T`。没有默认值，调用时必须提供。传入 `T` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `currentValue`：类型为 `T &`。没有默认值，调用时必须提供。传入 `T &` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QAtomicInteger::operator T() const`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAtomicInteger` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`由运算符声明决定`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T QAtomicInteger::operator&=(T value)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAtomicInteger` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`T`。
- 参数 `value`：类型为 `T`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T QAtomicInteger::operator++()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAtomicInteger` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`T`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T QAtomicInteger::operator++(int)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAtomicInteger` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`T`。
- 参数 `int`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T QAtomicInteger::operator+=(T value)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAtomicInteger` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`T`。
- 参数 `value`：类型为 `T`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T QAtomicInteger::operator--()`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAtomicInteger` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`T`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T QAtomicInteger::operator--(int)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAtomicInteger` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`T`。
- 参数 `int`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T QAtomicInteger::operator-=(T value)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAtomicInteger` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`T`。
- 参数 `value`：类型为 `T`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `QAtomicInteger<T> &QAtomicInteger::operator=(T)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAtomicInteger` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QAtomicInteger<T> &`。
- 参数 `T`：类型为 `未标注`。没有默认值，调用时必须提供。传入 `对应类型` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept] QAtomicInteger<T> &QAtomicInteger::operator=(const QAtomicInteger<T> &other)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAtomicInteger` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`QAtomicInteger<T> &`。
- 参数 `other`：类型为 `const QAtomicInteger<T> &`。没有默认值，调用时必须提供。参与比较、合并或交换的另一个对象；要确认它与当前对象属于同一类型或兼容协议。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T QAtomicInteger::operator^=(T value)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAtomicInteger` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`T`。
- 参数 `value`：类型为 `T`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `T QAtomicInteger::operator|=(T value)`

**API 类别：** 成员函数说明

**中文解读：** 这是 `QAtomicInteger` 的运算符重载，用于把对象按值类型语义进行比较、赋值、访问或转换。要确认它返回新对象还是修改当前对象，并注意隐式共享、空值和临时对象生命周期。

**签名拆解：**

- 返回值：`T`。
- 参数 `value`：类型为 `T`。没有默认值，调用时必须提供。要读取或写入的值。要确认类型转换、默认值、所有权以及写入后是否触发通知。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `[noexcept, since 6.7] void qYieldCpu()`

**API 类别：** 相关非成员函数

**中文解读：** `QAtomicInteger::qYieldCpu` 用于执行与“q、Yield、Cpu”相关的操作。调用时要先确认当前状态和 无参数 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Q_ATOMIC_INTnn_FETCH_AND_ADD_IS_ALWAYS_NATIVE`

**API 类别：** 宏说明

**中文解读：** 这是 `QAtomicInteger` 的 `IN、Tnn、NATIVE` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Q_ATOMIC_INTnn_FETCH_AND_ADD_IS_NOT_NATIVE`

**API 类别：** 宏说明

**中文解读：** 这是 `QAtomicInteger` 的 `IN、Tnn、NATIVE` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Q_ATOMIC_INTnn_FETCH_AND_ADD_IS_SOMETIMES_NATIVE`

**API 类别：** 宏说明

**中文解读：** 这是 `QAtomicInteger` 的 `IN、Tnn、NATIVE` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Q_ATOMIC_INTnn_FETCH_AND_ADD_IS_WAIT_FREE`

**API 类别：** 宏说明

**中文解读：** 这是 `QAtomicInteger` 的 `IN、Tnn、FREE` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Q_ATOMIC_INTnn_FETCH_AND_STORE_IS_ALWAYS_NATIVE`

**API 类别：** 宏说明

**中文解读：** 这是 `QAtomicInteger` 的 `IN、Tnn、NATIVE` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Q_ATOMIC_INTnn_FETCH_AND_STORE_IS_NOT_NATIVE`

**API 类别：** 宏说明

**中文解读：** 这是 `QAtomicInteger` 的 `IN、Tnn、NATIVE` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Q_ATOMIC_INTnn_FETCH_AND_STORE_IS_SOMETIMES_NATIVE`

**API 类别：** 宏说明

**中文解读：** 这是 `QAtomicInteger` 的 `IN、Tnn、NATIVE` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Q_ATOMIC_INTnn_FETCH_AND_STORE_IS_WAIT_FREE`

**API 类别：** 宏说明

**中文解读：** 这是 `QAtomicInteger` 的 `IN、Tnn、FREE` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Q_ATOMIC_INTnn_IS_SUPPORTED`

**API 类别：** 宏说明

**中文解读：** 这是 `QAtomicInteger` 的 `IN、Tnn、SUPPORTED` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Q_ATOMIC_INTnn_REFERENCE_COUNTING_IS_ALWAYS_NATIVE`

**API 类别：** 宏说明

**中文解读：** 这是 `QAtomicInteger` 的 `IN、Tnn、NATIVE` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Q_ATOMIC_INTnn_REFERENCE_COUNTING_IS_NOT_NATIVE`

**API 类别：** 宏说明

**中文解读：** 这是 `QAtomicInteger` 的 `IN、Tnn、NATIVE` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Q_ATOMIC_INTnn_REFERENCE_COUNTING_IS_SOMETIMES_NATIVE`

**API 类别：** 宏说明

**中文解读：** 这是 `QAtomicInteger` 的 `IN、Tnn、NATIVE` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Q_ATOMIC_INTnn_REFERENCE_COUNTING_IS_WAIT_FREE`

**API 类别：** 宏说明

**中文解读：** 这是 `QAtomicInteger` 的 `IN、Tnn、FREE` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Q_ATOMIC_INTnn_TEST_AND_SET_IS_ALWAYS_NATIVE`

**API 类别：** 宏说明

**中文解读：** 这是 `QAtomicInteger` 的 `IN、Tnn、NATIVE` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Q_ATOMIC_INTnn_TEST_AND_SET_IS_NOT_NATIVE`

**API 类别：** 宏说明

**中文解读：** 这是 `QAtomicInteger` 的 `IN、Tnn、NATIVE` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Q_ATOMIC_INTnn_TEST_AND_SET_IS_SOMETIMES_NATIVE`

**API 类别：** 宏说明

**中文解读：** 这是 `QAtomicInteger` 的 `IN、Tnn、NATIVE` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

**签名拆解：**

- 这是类型或成员声明，具体可用值和适用范围以该类的类型定义为准。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `Q_ATOMIC_INTnn_TEST_AND_SET_IS_WAIT_FREE`

**API 类别：** 宏说明

**中文解读：** 这是 `QAtomicInteger` 的 `IN、Tnn、FREE` 成员声明。它通常作为其他 API 的类型、常量或配置入口使用；先确认可用值和适用状态，再结合本类的创建、核心操作和清理流程使用。

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

`QAtomicInteger` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
