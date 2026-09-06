# QMetaContainer

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“Meta容器”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QMetaContainer` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QMetaContainer>`
- 继承自：未在类页中列出
- 直接派生类：QMetaAssociation、QMetaSequence

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

- `void advanceConstIterator(void *iterator, qsizetype step) const`
- `void advanceIterator(void *iterator, qsizetype step) const`
- `void * begin(void *container) const`
- `bool canClear() const`
- `void clear(void *container) const`
- `bool compareConstIterator(const void *i, const void *j) const`
- `bool compareIterator(const void *i, const void *j) const`
- `void * constBegin(const void *container) const`
- `void * constEnd(const void *container) const`
- `void copyConstIterator(void *target, const void *source) const`
- `void copyIterator(void *target, const void *source) const`
- `void destroyConstIterator(const void *iterator) const`
- `void destroyIterator(const void *iterator) const`
- `qsizetype diffConstIterator(const void *i, const void *j) const`
- `qsizetype diffIterator(const void *i, const void *j) const`
- `void * end(void *container) const`
- `bool hasBidirectionalIterator() const`
- `bool hasConstIterator() const`
- `bool hasForwardIterator() const`
- `bool hasInputIterator() const`
- `bool hasIterator() const`
- `bool hasRandomAccessIterator() const`
- `bool hasSize() const`
- `qsizetype size(const void *container) const`

## 5. API 逐个说明

这里直接说明每个公开成员解决什么问题、参数代表什么、返回什么、会改变什么以及使用时容易出现什么问题。每一个公开签名都会有对应的中文解释。

本类共整理 24 个公开成员条目；没有独立长描述的 API 也会根据签名、类型和所属机制给出使用说明。

### `void QMetaContainer::advanceConstIterator(void *iterator, qsizetype step) const`

**API 类别：** 成员函数说明

**中文解读：** `QMetaContainer::advanceConstIterator` 用于执行与“advance、Const、Iterator”相关的操作。调用时要先确认当前状态和 `iterator`、`step` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `iterator`：类型为 `void *`。没有默认值，调用时必须提供。传入 `void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `step`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMetaContainer::advanceIterator(void *iterator, qsizetype step) const`

**API 类别：** 成员函数说明

**中文解读：** `QMetaContainer::advanceIterator` 用于执行与“advance、Iterator”相关的操作。调用时要先确认当前状态和 `iterator`、`step` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `iterator`：类型为 `void *`。没有默认值，调用时必须提供。传入 `void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `step`：类型为 `qsizetype`。没有默认值，调用时必须提供。传入 `qsizetype` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void *QMetaContainer::begin(void *container) const`

**API 类别：** 成员函数说明

**中文解读：** 这是启动/建立资源的 API `begin`。调用前准备依赖和参数，调用后检查返回值或状态信号；成功后通常需要配套的 stop/close/end/disconnect 或释放操作。

**签名拆解：**

- 返回值：`void *`。
- 参数 `container`：类型为 `void *`。没有默认值，调用时必须提供。传入 `void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QMetaContainer::canClear() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `canClear`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMetaContainer::clear(void *container) const`

**API 类别：** 成员函数说明

**中文解读：** 这是状态清理或重置 API `clear`。调用后原有数据、索引、缓存或绑定可能失效；使用前先确认它影响的是当前对象、子对象还是底层共享资源，之后重新检查状态。

**签名拆解：**

- 返回值：`void`。
- 参数 `container`：类型为 `void *`。没有默认值，调用时必须提供。传入 `void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QMetaContainer::compareConstIterator(const void *i, const void *j) const`

**API 类别：** 成员函数说明

**中文解读：** `QMetaContainer::compareConstIterator` 用于计算、查询或取得与“比较、Const、Iterator”相关的操作。调用时要先确认当前状态和 `i`、`j` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `i`：类型为 `const void *`。没有默认值，调用时必须提供。传入 `const void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `j`：类型为 `const void *`。没有默认值，调用时必须提供。传入 `const void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QMetaContainer::compareIterator(const void *i, const void *j) const`

**API 类别：** 成员函数说明

**中文解读：** `QMetaContainer::compareIterator` 用于计算、查询或取得与“比较、Iterator”相关的操作。调用时要先确认当前状态和 `i`、`j` 的有效范围；返回类型是 `bool`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`bool`。
- 参数 `i`：类型为 `const void *`。没有默认值，调用时必须提供。传入 `const void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `j`：类型为 `const void *`。没有默认值，调用时必须提供。传入 `const void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void *QMetaContainer::constBegin(const void *container) const`

**API 类别：** 成员函数说明

**中文解读：** `QMetaContainer::constBegin` 用于计算、查询或取得与“const、起始位置”相关的操作。调用时要先确认当前状态和 `container` 的有效范围；返回类型是 `void *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void *`。
- 参数 `container`：类型为 `const void *`。没有默认值，调用时必须提供。传入 `const void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void *QMetaContainer::constEnd(const void *container) const`

**API 类别：** 成员函数说明

**中文解读：** `QMetaContainer::constEnd` 用于计算、查询或取得与“const、结束”相关的操作。调用时要先确认当前状态和 `container` 的有效范围；返回类型是 `void *`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void *`。
- 参数 `container`：类型为 `const void *`。没有默认值，调用时必须提供。传入 `const void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMetaContainer::copyConstIterator(void *target, const void *source) const`

**API 类别：** 成员函数说明

**中文解读：** `QMetaContainer::copyConstIterator` 用于执行与“copy、Const、Iterator”相关的操作。调用时要先确认当前状态和 `target`、`source` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `void *`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `source`：类型为 `const void *`。没有默认值，调用时必须提供。源对象、源索引或源数据；它通常决定操作的输入，转换后要确认源的生命周期和线程归属。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMetaContainer::copyIterator(void *target, const void *source) const`

**API 类别：** 成员函数说明

**中文解读：** `QMetaContainer::copyIterator` 用于执行与“copy、Iterator”相关的操作。调用时要先确认当前状态和 `target`、`source` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `target`：类型为 `void *`。没有默认值，调用时必须提供。目标对象、目标属性或目标资源。要确认它在操作期间仍然有效，并支持所需能力。
- 参数 `source`：类型为 `const void *`。没有默认值，调用时必须提供。源对象、源索引或源数据；它通常决定操作的输入，转换后要确认源的生命周期和线程归属。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMetaContainer::destroyConstIterator(const void *iterator) const`

**API 类别：** 成员函数说明

**中文解读：** `QMetaContainer::destroyConstIterator` 用于执行与“destroy、Const、Iterator”相关的操作。调用时要先确认当前状态和 `iterator` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `iterator`：类型为 `const void *`。没有默认值，调用时必须提供。传入 `const void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void QMetaContainer::destroyIterator(const void *iterator) const`

**API 类别：** 成员函数说明

**中文解读：** `QMetaContainer::destroyIterator` 用于执行与“destroy、Iterator”相关的操作。调用时要先确认当前状态和 `iterator` 的有效范围；返回类型是 `void`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`void`。
- 参数 `iterator`：类型为 `const void *`。没有默认值，调用时必须提供。传入 `const void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qsizetype QMetaContainer::diffConstIterator(const void *i, const void *j) const`

**API 类别：** 成员函数说明

**中文解读：** `QMetaContainer::diffConstIterator` 用于计算、查询或取得与“diff、Const、Iterator”相关的操作。调用时要先确认当前状态和 `i`、`j` 的有效范围；返回类型是 `qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数 `i`：类型为 `const void *`。没有默认值，调用时必须提供。传入 `const void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `j`：类型为 `const void *`。没有默认值，调用时必须提供。传入 `const void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qsizetype QMetaContainer::diffIterator(const void *i, const void *j) const`

**API 类别：** 成员函数说明

**中文解读：** `QMetaContainer::diffIterator` 用于计算、查询或取得与“diff、Iterator”相关的操作。调用时要先确认当前状态和 `i`、`j` 的有效范围；返回类型是 `qsizetype`，应根据返回值、状态查询或错误信号判断结果，不能只根据函数调用没有崩溃就认为操作成功。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数 `i`：类型为 `const void *`。没有默认值，调用时必须提供。传入 `const void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。
- 参数 `j`：类型为 `const void *`。没有默认值，调用时必须提供。传入 `const void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `void *QMetaContainer::end(void *container) const`

**API 类别：** 成员函数说明

**中文解读：** 这是结束/释放/取消 API `end`。它会改变对象状态或资源所有权，调用后不要继续使用已经失效的句柄、reply、索引或设备，并确认异步完成信号是否仍会到达。

**签名拆解：**

- 返回值：`void *`。
- 参数 `container`：类型为 `void *`。没有默认值，调用时必须提供。传入 `void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QMetaContainer::hasBidirectionalIterator() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `hasBidirectionalIterator`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QMetaContainer::hasConstIterator() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `hasConstIterator`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QMetaContainer::hasForwardIterator() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `hasForwardIterator`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QMetaContainer::hasInputIterator() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `hasInputIterator`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QMetaContainer::hasIterator() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `hasIterator`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QMetaContainer::hasRandomAccessIterator() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `hasRandomAccessIterator`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `bool QMetaContainer::hasSize() const`

**API 类别：** 成员函数说明

**中文解读：** 这是查询 API `hasSize`，用于判断当前状态或能力。它通常没有副作用，适合在执行主操作前做保护性判断，但不能替代真正操作的错误处理。

**签名拆解：**

- 返回值：`bool`。
- 参数：无。

**正确调用组合：** 调用后检查返回值、状态查询和错误信息；如果该类通过信号或事件通知变化，还要处理异步完成和对象生命周期。

### `qsizetype QMetaContainer::size(const void *container) const`

**API 类别：** 成员函数说明

**中文解读：** 这是尺寸/数量查询 API `size`，返回 `QMetaContainer` 当前元素数、字节数、容量或可用空间。它是某一时刻的快照，不能替代并发同步或后续操作的边界检查。

**签名拆解：**

- 返回值：`qsizetype`。
- 参数 `container`：类型为 `const void *`。没有默认值，调用时必须提供。传入 `const void *` 类型的值；调用前确认它的有效范围、默认行为和生命周期。

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

`QMetaContainer` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
