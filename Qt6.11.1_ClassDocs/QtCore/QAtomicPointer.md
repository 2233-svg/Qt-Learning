# QAtomicPointer

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“AtomicPointer”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QAtomicPointer` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QAtomicPointer>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

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

- `QAtomicPointer(T *value = nullptr)`
- `QAtomicPointer(const QAtomicPointer<T> &other)`
- `T * fetchAndAddAcquire(qptrdiff valueToAdd)`
- `T * fetchAndAddOrdered(qptrdiff valueToAdd)`
- `T * fetchAndAddRelaxed(qptrdiff valueToAdd)`
- `T * fetchAndAddRelease(qptrdiff valueToAdd)`
- `T * fetchAndStoreAcquire(T *newValue)`
- `T * fetchAndStoreOrdered(T *newValue)`
- `T * fetchAndStoreRelaxed(T *newValue)`
- `T * fetchAndStoreRelease(T *newValue)`
- `T * loadAcquire() const`
- `T * loadRelaxed() const`
- `void storeRelaxed(T *newValue)`
- `void storeRelease(T *newValue)`
- `bool testAndSetAcquire(T *expectedValue, T *newValue)`
- `bool testAndSetAcquire(T *expectedValue, T *newValue, T *&currentValue)`
- `bool testAndSetOrdered(T *expectedValue, T *newValue)`
- `bool testAndSetOrdered(T *expectedValue, T *newValue, T *&currentValue)`
- `bool testAndSetRelaxed(T *expectedValue, T *newValue)`
- `bool testAndSetRelaxed(T *expectedValue, T *newValue, T *&currentValue)`
- `bool testAndSetRelease(T *expectedValue, T *newValue)`
- `bool testAndSetRelease(T *expectedValue, T *newValue, T *&currentValue)`
- `QAtomicPointer<T> & operator=(const QAtomicPointer<T> &other)`

### 静态公有成员

- `bool isFetchAndAddNative()`
- `bool isFetchAndAddWaitFree()`
- `bool isFetchAndStoreNative()`
- `bool isFetchAndStoreWaitFree()`
- `bool isTestAndSetNative()`
- `bool isTestAndSetWaitFree()`

### 公开宏

- `Q_ATOMIC_POINTER_FETCH_AND_ADD_IS_ALWAYS_NATIVE`
- `Q_ATOMIC_POINTER_FETCH_AND_ADD_IS_NOT_NATIVE`
- `Q_ATOMIC_POINTER_FETCH_AND_ADD_IS_SOMETIMES_NATIVE`
- `Q_ATOMIC_POINTER_FETCH_AND_ADD_IS_WAIT_FREE`
- `Q_ATOMIC_POINTER_FETCH_AND_STORE_IS_ALWAYS_NATIVE`
- `Q_ATOMIC_POINTER_FETCH_AND_STORE_IS_NOT_NATIVE`
- `Q_ATOMIC_POINTER_FETCH_AND_STORE_IS_SOMETIMES_NATIVE`
- `Q_ATOMIC_POINTER_FETCH_AND_STORE_IS_WAIT_FREE`
- `Q_ATOMIC_POINTER_TEST_AND_SET_IS_ALWAYS_NATIVE`
- `Q_ATOMIC_POINTER_TEST_AND_SET_IS_NOT_NATIVE`
- `Q_ATOMIC_POINTER_TEST_AND_SET_IS_SOMETIMES_NATIVE`
- `Q_ATOMIC_POINTER_TEST_AND_SET_IS_WAIT_FREE`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[constexpr noexcept] QAtomicPointer::QAtomicPointer(T *value = nullptr)`

**作用与语义：**

构造一个带有给定`value`的QAtomicPointer。

### `[noexcept] QAtomicPointer::QAtomicPointer(const QAtomicPointer<T> &other)`

**作用与语义：**

复制了`other`。

### `T *QAtomicPointer::fetchAndAddAcquire(qptrdiff valueToAdd)`

**作用与语义：**

原子式取球加法。
读取该`QAtomicPointer`当前值，然后将`valueToAdd`加到当前值上，返回原始值。
该函数使用获取内存排序语义，确保原子操作之后（按程序顺序）访问内存不会在原子操作前被重新排序。

### `T *QAtomicPointer::fetchAndAddOrdered(qptrdiff valueToAdd)`

**作用与语义：**

原子式取球加法。
读取该`QAtomicPointer`当前值，然后将`valueToAdd`加到当前值上，返回原始值。
该函数使用有序内存排序语义，确保原子操作前后（按程序顺序）访问的内存访问不会被重新排序。

### `T *QAtomicPointer::fetchAndAddRelaxed(qptrdiff valueToAdd)`

**作用与语义：**

原子式取球加法。
读取该`QAtomicPointer`当前值，然后将`valueToAdd`加到当前值上，返回原始值。
该函数使用宽松的内存排序语义，使编译器和处理器可以自由重排内存访问。

### `T *QAtomicPointer::fetchAndAddRelease(qptrdiff valueToAdd)`

**作用与语义：**

原子式取球加法。
读取该`QAtomicPointer`当前值，然后将`valueToAdd`加到当前值上，返回原始值。
该函数使用释放内存排序语义，确保原子操作前的内存访问（按程序顺序）不会在原子操作后重新排序。

### `T *QAtomicPointer::fetchAndStoreAcquire(T *newValue)`

**作用与语义：**

原子级取物存储。
读取该`QAtomicPointer`当前值，然后赋予其`newValue`，返回原始值。
该函数使用获取内存排序语义，确保原子操作之后（按程序顺序）访问内存不会在原子操作前被重新排序。

### `T *QAtomicPointer::fetchAndStoreOrdered(T *newValue)`

**作用与语义：**

原子级取物存储。
读取该`QAtomicPointer`的当前值，然后赋予其`newValue`，返回原始值。
该函数使用有序内存排序语义，确保原子操作前后（按程序顺序）访问的内存访问不会被重新排序。

### `T *QAtomicPointer::fetchAndStoreRelaxed(T *newValue)`

**作用与语义：**

原子级取物存储。
读取该`QAtomicPointer`当前值，然后赋予其`newValue`，返回原始值。
该函数使用宽松的内存排序语义，使编译器和处理器可以自由重排内存访问。

### `T *QAtomicPointer::fetchAndStoreRelease(T *newValue)`

**作用与语义：**

原子级取物存储。
读取该`QAtomicPointer`当前值，然后赋予其`newValue`，返回原始值。
该函数使用释放内存排序语义，确保原子操作前的内存访问（按程序顺序）不会在原子操作后重新排序。

### `[static constexpr] bool QAtomicPointer::isFetchAndAddNative()`

**作用与语义：**

如果用原子处理器指令实现取加，返回`true`，否则为假。

### `[static constexpr] bool QAtomicPointer::isFetchAndAddWaitFree()`

**作用与语义：**

如果原子取取加法无等待，返回 `true`，否则返回 false。

### `[static constexpr] bool QAtomicPointer::isFetchAndStoreNative()`

**作用与语义：**

如果用原子处理器指令实现取物与存储，返回`true`，否则返回为假。

### `[static constexpr] bool QAtomicPointer::isFetchAndStoreWaitFree()`

**作用与语义：**

如果原子取源存储无等待，返回`true`;否则为false。

### `[static constexpr] bool QAtomicPointer::isTestAndSetNative()`

**作用与语义：**

如果测试和设置使用原子处理器指令实现，返回`true`，否则返回为假。

### `[static constexpr] bool QAtomicPointer::isTestAndSetWaitFree()`

**作用与语义：**

如果原子测试与设置无等待，返回`true`;否则返回，否则为假。

### `T *QAtomicPointer::loadAcquire() const`

**作用与语义：**

原子加载该`QAtomicPointer`的值时使用“获取”内存排序。该值不会被修改，但请注意，不能保证保持。

### `T *QAtomicPointer::loadRelaxed() const`

**作用与语义：**

原子加载该`QAtomicPointer`值时使用宽松的内存排序。该值不会被任何方式修改，但请注意，不能保证它会保持原值。

### `void QAtomicPointer::storeRelaxed(T *newValue)`

**作用与语义：**

原子层次将`newValue`值存储到这种原子类型中，采用宽松的内存排序。

### `void QAtomicPointer::storeRelease(T *newValue)`

**作用与语义：**

Atomic将`newValue`值存储到该原子类型中，使用“Release”内存排序。

### `bool QAtomicPointer::testAndSetAcquire(T *expectedValue, T *newValue)`

**作用与语义：**

原子测试与设定。
注意：如果你在循环中使用该函数，建议使用带有额外`T *¤tValue`参数的超载，这样可以避免故障时额外的负载()。
如果该`QAtomicPointer`当前值为`expectedValue`，测试与集合函数将`newValue`赋值为该`QAtomicPointer`并返回真值。如果值不相同，该函数不做任何操作，返回`false`。
该函数使用获取内存排序语义，确保原子操作之后（按程序顺序）访问内存不会在原子操作前被重新排序。

### `bool QAtomicPointer::testAndSetAcquire(T *expectedValue, T *newValue, T *&currentValue)`

**作用与语义：**

原子测试与设定。
如果该`QAtomicPointer`当前值为`expectedValue`，测试与集合函数将`newValue`分配到该`QAtomicPointer`并返回`true`。如果值不相同，函数将该`QAtomicPointer`当前值加载到`currentValue`并返回`false`。
该函数使用获取内存排序语义，确保原子操作之后（按程序顺序）访问内存不会在原子操作前重新排序。如果测试与集合失败，`currentValue`将加载获取内存排序语义。

### `bool QAtomicPointer::testAndSetOrdered(T *expectedValue, T *newValue)`

**作用与语义：**

原子测试与设定。
注意：如果你在循环中使用该函数，建议使用带有额外`T *¤tValue`参数的超载，这样可以避免故障时的额外负载()。
如果该`QAtomicPointer`当前值为`expectedValue`，测试与集合函数将`newValue`赋值为该`QAtomicPointer`并返回真值。如果值不相同，该函数不做任何事，返回`false`。
该函数使用有序内存排序语义，确保原子操作前后（按程序顺序）访问的内存访问不会被重新排序。

### `bool QAtomicPointer::testAndSetOrdered(T *expectedValue, T *newValue, T *&currentValue)`

**作用与语义：**

原子测试与设定。
如果该`QAtomicPointer`当前值为`expectedValue`，测试与集合函数将`newValue`分配给该`QAtomicPointer`并返回`true`。如果值不相同，函数将该`QAtomicPointer`的当前值加载到`currentValue`并返回`false`。
该函数使用有序内存排序语义，确保原子操作前后（按程序顺序）访问的内存访问不会被重新排序。如果测试与集合失败，`currentValue`将加载获取内存排序语义。

### `bool QAtomicPointer::testAndSetRelaxed(T *expectedValue, T *newValue)`

**作用与语义：**

原子测试与设定。
注意：如果你在循环中使用该函数，建议使用带有额外 `T *¤tValue` 参数的超载，这样可以避免故障时额外的 load()。
如果该`QAtomicPointer`当前值为`expectedValue`，测试与集合函数将`newValue`赋值为该`QAtomicPointer`并返回真。如果值不相同，该函数不做任何操作，返回`false`。
该函数使用宽松的内存排序语义，使编译器和处理器可以自由重排内存访问。

### `bool QAtomicPointer::testAndSetRelaxed(T *expectedValue, T *newValue, T *&currentValue)`

**作用与语义：**

原子测试与设定。
如果该`QAtomicPointer`当前值为`expectedValue`，测试与集合函数将`newValue`分配到该`QAtomicPointer`并返回`true`。如果值不相同，函数将该`QAtomicPointer`当前值加载到`currentValue`并返回`false`。
该函数使用宽松的内存排序语义，使编译器和处理器可以自由重排内存访问。如果测试与集合失败，则`currentValue`加载宽松的内存排序语义。

### `bool QAtomicPointer::testAndSetRelease(T *expectedValue, T *newValue)`

**作用与语义：**

原子测试与设定。
注意：如果你在循环中使用该函数，建议使用带有额外`T *¤tValue`参数的超载，这样可以避免故障时额外的 load()。
如果该`QAtomicPointer`当前值为`expectedValue`，测试与集合函数将`newValue`赋值为该`QAtomicPointer`并返回真。如果值不相同，该函数不做任何操作，返回`false`。
该函数使用释放内存排序语义，确保原子操作前的内存访问（按程序顺序）不会在原子操作后重新排序。

### `bool QAtomicPointer::testAndSetRelease(T *expectedValue, T *newValue, T *&currentValue)`

**作用与语义：**

原子测试与设定。
如果该`QAtomicPointer`当前值为`expectedValue`，测试与集合函数将`newValue`分配到该`QAtomicPointer`并返回`true`。如果值不相同，函数将该`QAtomicPointer`当前值加载到`currentValue`并返回`false`。
该函数使用释放内存排序语义，确保原子操作前的内存访问（按程序顺序）在原子操作后不会被重新排序。如果测试与集合失败，则`currentValue`加载了宽松的内存排序语义。

### `[noexcept] QAtomicPointer<T> &QAtomicPointer::operator=(const QAtomicPointer<T> &other)`

**作用与语义：**

为该`QAtomicPointer`分配`other`并返回该`QAtomicPointer`的引用。

### `Q_ATOMIC_POINTER_FETCH_AND_ADD_IS_ALWAYS_NATIVE`

**作用与语义：**

该宏定义为当且仅当你的处理器支持原子取取加指针时。

### `Q_ATOMIC_POINTER_FETCH_AND_ADD_IS_NOT_NATIVE`

**作用与语义：**

当硬件不支持原子取指针加法时，定义了该宏。

### `Q_ATOMIC_POINTER_FETCH_AND_ADD_IS_SOMETIMES_NATIVE`

**作用与语义：**

该宏定义为只有特定处理器世代支持原子取取加指针时。使用`QAtomicPointer::isFetchAndAddNative()`函数检查处理器支持的功能。

### `Q_ATOMIC_POINTER_FETCH_AND_ADD_IS_WAIT_FREE`

**作用与语义：**

该宏与`Q_ATOMIC_POINTER_FETCH_AND_ADD_IS_ALWAYS_NATIVE`一起定义，表示原子取指针加指针无需等待。

### `Q_ATOMIC_POINTER_FETCH_AND_STORE_IS_ALWAYS_NATIVE`

**作用与语义：**

当且仅当你的处理器支持指针上的原子取取存储时，该宏才被定义。

### `Q_ATOMIC_POINTER_FETCH_AND_STORE_IS_NOT_NATIVE`

**作用与语义：**

当硬件不支持指针原子取取存储时，定义了该宏。

### `Q_ATOMIC_POINTER_FETCH_AND_STORE_IS_SOMETIMES_NATIVE`

**作用与语义：**

当处理器的某些世代支持指针原子取用并存储时，定义了这个宏。使用`QAtomicPointer::isFetchAndStoreNative()`函数检查处理器支持的内容。

### `Q_ATOMIC_POINTER_FETCH_AND_STORE_IS_WAIT_FREE`

**作用与语义：**

该宏与`Q_ATOMIC_POINTER_FETCH_AND_STORE_IS_ALWAYS_NATIVE`一起定义，表示指针上的原子取取存储无需等待。

### `Q_ATOMIC_POINTER_TEST_AND_SET_IS_ALWAYS_NATIVE`

**作用与语义：**

当且仅当你的处理器支持指针的原子测试和设置时，这个宏才被定义。

### `Q_ATOMIC_POINTER_TEST_AND_SET_IS_NOT_NATIVE`

**作用与语义：**

当硬件不支持指针的原子测试和设置时，定义了该宏。

### `Q_ATOMIC_POINTER_TEST_AND_SET_IS_SOMETIMES_NATIVE`

**作用与语义：**

该宏定义为只有特定处理器世代支持指针原子测试和设置。使用`QAtomicPointer::isTestAndSetNative()`函数检查处理器支持的内容。

### `Q_ATOMIC_POINTER_TEST_AND_SET_IS_WAIT_FREE`

**作用与语义：**

该宏与`Q_ATOMIC_POINTER_TEST_AND_SET_IS_ALWAYS_NATIVE`一起定义，表示指针上的原子测试和集合是无等待的。

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

`QAtomicPointer` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
