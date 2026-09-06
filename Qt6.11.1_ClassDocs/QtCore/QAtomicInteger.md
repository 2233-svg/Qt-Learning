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

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[constexpr noexcept] QAtomicInteger::QAtomicInteger(T value = 0)`

**作用与语义：**

构造一个QAtomic整数，`value`。

### `[noexcept] QAtomicInteger::QAtomicInteger(const QAtomicInteger<T> &other)`

**作用与语义：**

复制了`other`。

### `bool QAtomicInteger::deref()`

**作用与语义：**

原子层递减该`QAtomicInteger`值。如果新值非零，返回`true`，否则为假。
该函数使用有序内存排序语义，确保原子操作前后（按程序顺序）访问的内存访问不会被重新排序。

### `T QAtomicInteger::fetchAndAddAcquire(T valueToAdd)`

**作用与语义：**

原子式取球加法。
读取该`QAtomicInteger`当前值，然后将`valueToAdd`加到当前值上，返回原始值。
该函数使用获取内存排序语义，确保原子操作之后（按程序顺序）访问内存不会在原子操作前被重新排序。

### `T QAtomicInteger::fetchAndAddOrdered(T valueToAdd)`

**作用与语义：**

原子式取球加法。
读取该`QAtomicInteger`的当前值，然后将`valueToAdd`加到当前值上，返回原始值。
该函数使用有序内存排序语义，确保原子操作前后（按程序顺序）访问的内存访问不会被重新排序。

### `T QAtomicInteger::fetchAndAddRelaxed(T valueToAdd)`

**作用与语义：**

原子式取球加法。
读取该`QAtomicInteger`的当前值，然后将`valueToAdd`加到当前值上，返回原始值。
该函数使用宽松的内存排序语义，使编译器和处理器可以自由重排内存访问。

### `T QAtomicInteger::fetchAndAddRelease(T valueToAdd)`

**作用与语义：**

原子式取球加法。
读取该`QAtomicInteger`当前值，然后将`valueToAdd`加到当前值上，返回原始值。
该函数使用释放内存排序语义，确保原子操作前的内存访问（按程序顺序）不会在原子操作后重新排序。

### `T QAtomicInteger::fetchAndAndAcquire(T valueToAnd)`

**作用与语义：**

原子式的接球和再。
读取该`QAtomicInteger`当前值，然后通过位元ANDs返回当前值，返回`valueToAnd`当前值。
该函数使用获取内存排序语义，确保原子操作之后（按程序顺序）访问内存不会在原子操作前被重新排序。

### `T QAtomicInteger::fetchAndAndOrdered(T valueToAnd)`

**作用与语义：**

原子式的接球和再。
读取该`QAtomicInteger`的当前值，然后通过位与 AND `valueToAnd`当前值，返回原始值。
该函数使用有序内存排序语义，确保原子操作前后（按程序顺序）访问的内存访问不会被重新排序。

### `T QAtomicInteger::fetchAndAndRelaxed(T valueToAnd)`

**作用与语义：**

原子式的接球和再。
读取该`QAtomicInteger`的当前值，然后通过位与数字（AND）`valueToAnd`当前值，返回原始值。
该函数使用宽松的内存排序语义，使编译器和处理器可以自由重排内存访问。

### `T QAtomicInteger::fetchAndAndRelease(T valueToAnd)`

**作用与语义：**

原子式的接球和再。
读取该`QAtomicInteger`的当前值，然后通过位与数字（AND）`valueToAnd`当前值，返回原始值。
该函数使用释放内存排序语义，确保原子操作前的内存访问（按程序顺序）不会在原子操作后重新排序。

### `T QAtomicInteger::fetchAndOrAcquire(T valueToOr)`

**作用与语义：**

原子取物与或。
读取该`QAtomicInteger`当前值，然后通过位数 OR `valueToOr`当前值，返回原始值。
该函数使用获取内存排序语义，确保原子操作之后（按程序顺序）访问内存不会在原子操作前被重新排序。

### `T QAtomicInteger::fetchAndOrOrdered(T valueToOr)`

**作用与语义：**

原子取物与或。
读取该`QAtomicInteger`的当前值，然后通过位 OR `valueToOr`当前值，返回原始值。
该函数使用有序内存排序语义，确保原子操作前后（按程序顺序）访问的内存访问不会被重新排序。

### `T QAtomicInteger::fetchAndOrRelaxed(T valueToOr)`

**作用与语义：**

原子取物与或。
读取该`QAtomicInteger`当前值，然后通过位 OR `valueToOr`当前值，返回原始值。
该函数使用宽松的内存排序语义，使编译器和处理器可以自由重排内存访问。

### `T QAtomicInteger::fetchAndOrRelease(T valueToOr)`

**作用与语义：**

原子取物与或。
读取该`QAtomicInteger`的当前值，然后通过位数 OR `valueToOr`当前值，返回原始值。
该函数使用释放内存排序语义，确保原子操作前的内存访问（按程序顺序）不会在原子操作后重新排序。

### `T QAtomicInteger::fetchAndStoreAcquire(T newValue)`

**作用与语义：**

原子级取物存储。
读取该`QAtomicInteger`当前值，然后赋予其`newValue`，返回原始值。
该函数使用获取内存排序语义，确保原子操作之后（按程序顺序）访问内存不会在原子操作前被重新排序。

### `T QAtomicInteger::fetchAndStoreOrdered(T newValue)`

**作用与语义：**

原子级取物存储。
读取该`QAtomicInteger`当前值，然后赋予其`newValue`，返回原始值。
该函数使用有序内存排序语义，确保原子操作前后（按程序顺序）访问的内存访问不会被重新排序。

### `T QAtomicInteger::fetchAndStoreRelaxed(T newValue)`

**作用与语义：**

原子级取物存储。
读取该`QAtomicInteger`当前值，然后赋予其`newValue`，返回原始值。
该函数使用宽松的内存排序语义，使编译器和处理器可以自由重排内存访问。

### `T QAtomicInteger::fetchAndStoreRelease(T newValue)`

**作用与语义：**

原子级取物存储。
读取该`QAtomicInteger`当前值，然后赋予其`newValue`，返回原始值。
该函数使用释放内存排序语义，确保原子操作前的内存访问（按程序顺序）不会在原子操作后重新排序。

### `T QAtomicInteger::fetchAndSubAcquire(T valueToSub)`

**作用与语义：**

原子级取物和潜艇。
读取该`QAtomicInteger`当前值，然后将`valueToSub`减去到当前值，返回原始值。
该函数使用获取内存排序语义，确保原子操作之后（按程序顺序）访问内存不会在原子操作前被重新排序。

### `T QAtomicInteger::fetchAndSubOrdered(T valueToSub)`

**作用与语义：**

原子级取物和潜艇。
读取该`QAtomicInteger`当前值，然后将`valueToSub`减去当前值，返回原始值。
该函数使用有序内存排序语义，确保原子操作前后（按程序顺序）访问的内存访问不会被重新排序。

### `T QAtomicInteger::fetchAndSubRelaxed(T valueToSub)`

**作用与语义：**

原子级取物和潜艇。
读取该`QAtomicInteger`的当前值，然后将`valueToSub`减去为当前值，返回原始值。
该函数使用宽松的内存排序语义，使编译器和处理器可以自由重排内存访问。

### `T QAtomicInteger::fetchAndSubRelease(T valueToSub)`

**作用与语义：**

原子级取物和潜艇。
读取该`QAtomicInteger`当前值，然后将`valueToSub`减去到当前值，返回原始值。
该函数使用释放内存排序语义，确保原子操作前的内存访问（按程序顺序）不会在原子操作后重新排序。

### `T QAtomicInteger::fetchAndXorAcquire(T valueToXor)`

**作用与语义：**

原子取物与异或。
读取该`QAtomicInteger`的当前值，然后通过位XORs返回当前值，返回`valueToXor`当前值。
该函数使用获取内存排序语义，确保原子操作之后（按程序顺序）访问内存不会在原子操作前被重新排序。

### `T QAtomicInteger::fetchAndXorOrdered(T valueToXor)`

**作用与语义：**

原子取物与异或。
读取该`QAtomicInteger`当前值，然后通过位异或`valueToXor`到当前值，返回原始值。
该函数使用有序内存排序语义，确保原子操作前后（按程序顺序）访问的内存访问不会被重新排序。

### `T QAtomicInteger::fetchAndXorRelaxed(T valueToXor)`

**作用与语义：**

原子取物与异或。
读取该`QAtomicInteger`的当前值，然后通过位`valueToXor` XOR 返回当前值，返回原始值。
该函数使用宽松的内存排序语义，使编译器和处理器可以自由重排内存访问。

### `T QAtomicInteger::fetchAndXorRelease(T valueToXor)`

**作用与语义：**

原子取物与异或。
读取该`QAtomicInteger`的当前值，然后通过位分异或`valueToXor`到当前值，返回原始值。
该函数使用释放内存排序语义，确保原子操作前的内存访问（按程序顺序）不会在原子操作后重新排序。

### `[static constexpr] bool QAtomicInteger::isFetchAndAddNative()`

**作用与语义：**

如果用原子处理器指令实现取加，返回`true`，否则为假。

### `[static constexpr] bool QAtomicInteger::isFetchAndAddWaitFree()`

**作用与语义：**

如果原子取取加法无等待，返回 `true`，否则返回 false。

### `[static constexpr] bool QAtomicInteger::isFetchAndStoreNative()`

**作用与语义：**

如果用原子处理器指令实现取物与存储，返回`true`，否则返回为假。

### `[static constexpr] bool QAtomicInteger::isFetchAndStoreWaitFree()`

**作用与语义：**

如果原子取源存储无等待，返回`true`;否则为false。

### `[static constexpr] bool QAtomicInteger::isReferenceCountingNative()`

**作用与语义：**

如果引用计数是用原子处理器指令实现的，返回`true`，否则返回false。

### `[static constexpr] bool QAtomicInteger::isReferenceCountingWaitFree()`

**作用与语义：**

如果原子引用计数无等待，返回`true`，否则返回 false。

### `[static constexpr] bool QAtomicInteger::isTestAndSetNative()`

**作用与语义：**

如果测试和设置使用原子处理器指令实现，返回`true`，否则返回为假。

### `[static constexpr] bool QAtomicInteger::isTestAndSetWaitFree()`

**作用与语义：**

如果原子测试与设置无等待，返回`true`;否则返回，否则为假。

### `T QAtomicInteger::loadAcquire() const`

**作用与语义：**

通过“获取”内存排序原子加载该`QAtomicInteger`值。该值不会被任何方式修改，但请注意，不能保证它会保持原值。

### `T QAtomicInteger::loadRelaxed() const`

**作用与语义：**

原子加载该`QAtomicInteger`值时采用宽松的内存排序。值不会被任何方式修改，但请注意，不能保证它会保持。

### `bool QAtomicInteger::ref()`

**作用与语义：**

原子层递增该`QAtomicInteger`值。如果新值非零，返回`true`，否则为假。
该函数使用有序内存排序语义，确保原子操作前后（按程序顺序）访问的内存访问不会被重新排序。

### `void QAtomicInteger::storeRelaxed(T newValue)`

**作用与语义：**

原子层次将`newValue`值存储到这种原子类型中，采用宽松的内存排序。

### `void QAtomicInteger::storeRelease(T newValue)`

**作用与语义：**

Atomic将`newValue`值存储到该原子类型中，使用“Release”内存排序。

### `bool QAtomicInteger::testAndSetAcquire(T expectedValue, T newValue)`

**作用与语义：**

原子测试与设定。
注意：如果你在循环中使用该函数，建议使用带有额外`T ¤tValue`参数的超载，这样可以避免失败时的额外 `loadAcquire()`。
如果该`QAtomicInteger`当前值为`expectedValue`，测试与集合函数将`newValue`赋值为该`QAtomicInteger`并返回真。如果值不相同，该函数不做任何操作，返回`false`。
该函数使用获取内存排序语义，确保原子操作之后（按程序顺序）访问内存不会在原子操作前被重新排序。

### `bool QAtomicInteger::testAndSetAcquire(T expectedValue, T newValue, T &currentValue)`

**作用与语义：**

原子测试与设定。
如果该`QAtomicInteger`当前值为`expectedValue`，测试与集合函数将`newValue`分配给该`QAtomicInteger`并返回`true`。如果值不相同，函数将该`QAtomicInteger`当前值加载到`currentValue`并返回`false`。
该函数使用获取内存排序语义，确保原子操作之后的内存访问（按程序顺序）不会在原子操作前重新排序。如果测试与集合失败，`currentValue`将加载获取内存排序语义。

### `bool QAtomicInteger::testAndSetOrdered(T expectedValue, T newValue)`

**作用与语义：**

原子测试与设定。
注意：如果你在循环中使用该函数，建议使用带有额外`T ¤tValue`参数的超载，这样可以避免失败时的额外 `loadAcquire()`。
如果该`QAtomicInteger`当前值为`expectedValue`，测试与集合函数将`newValue`分配给该`QAtomicInteger`并返回真值。如果值不相同，该函数不做任何操作，返回`false`。
该函数使用有序内存排序语义，确保原子操作前后（按程序顺序）访问的内存访问不会被重新排序。

### `bool QAtomicInteger::testAndSetOrdered(T expectedValue, T newValue, T &currentValue)`

**作用与语义：**

原子测试与设定。
如果该`QAtomicInteger`当前值为`expectedValue`，测试与集合函数将`newValue`分配到该`QAtomicInteger`并返回`true`。如果值不相同，则将该`QAtomicInteger`当前值加载到`currentValue`并返回`false`。
该函数使用有序内存排序语义，确保原子操作前后（按程序顺序）访问的内存访问不会被重新排序。如果测试与集合失败，`currentValue`将加载获取内存排序语义。

### `bool QAtomicInteger::testAndSetRelaxed(T expectedValue, T newValue)`

**作用与语义：**

原子测试与设定。
注意：如果你在循环中使用该函数，建议使用带有额外`T ¤tValue`参数的超载，这样可以避免失败时的额外 `loadRelaxed()`。
如果该`QAtomicInteger`当前值为`expectedValue`，测试与集合函数将`newValue`赋值给该`QAtomicInteger`并返回真值。如果值不相同，该函数不做任何操作，返回 `false`。
该函数使用宽松的内存排序语义，使编译器和处理器可以自由重排内存访问。

### `bool QAtomicInteger::testAndSetRelaxed(T expectedValue, T newValue, T &currentValue)`

**作用与语义：**

原子测试与设定。
如果该`QAtomicInteger`当前值为`expectedValue`，测试与集合函数将`newValue`分配到该`QAtomicInteger`并返回`true`。如果值不相同，函数将`QAtomicInteger`当前值加载到`currentValue`并返回`false`。
该函数使用宽松的内存排序语义，使编译器和处理器可以自由重排内存访问。如果测试与集合失败，则`currentValue`加载宽松的内存排序语义。

### `bool QAtomicInteger::testAndSetRelease(T expectedValue, T newValue)`

**作用与语义：**

原子测试与设定。
注意：如果你在循环中使用该函数，建议使用带有额外`T ¤tValue`参数的超载，这样可以避免失败时的额外 `loadRelaxed()`。
如果该`QAtomicInteger`当前值为`expectedValue`，测试与集合函数将`newValue`赋值到该`QAtomicInteger`并返回真值。如果值不相同，该函数不做任何操作，返回 `false`。
该函数使用释放内存排序语义，确保原子操作前的内存访问（按程序顺序）不会在原子操作后重新排序。

### `bool QAtomicInteger::testAndSetRelease(T expectedValue, T newValue, T &currentValue)`

**作用与语义：**

原子测试与设定。
如果该`QAtomicInteger`的当前值是`expectedValue`，测试和集合函数将`newValue`分配到该`QAtomicInteger`并返回`true`。如果值不相同，函数会将该`QAtomicInteger`当前值加载到`currentValue`并返回`false`。
该函数使用释放内存排序语义，确保原子操作前的内存访问（按程序顺序）不会在原子操作后重新排序。如果测试与集合失败，则`currentValue`加载宽松的内存排序语义。

### `QAtomicInteger::operator T() const`

**作用与语义：**

如果可能，原子加载该`QAtomicInteger`值时使用顺序一致的内存顺序;如果不行，则采用“获取”顺序。值不会被修改，但请注意，不能保证它会保持。

### `T QAtomicInteger::operator&=(T value)`

**作用与语义：**

原子加法和取球。
读取该`QAtomicInteger`的当前值，然后通过位元ANDs返回当前值，返回新的值`value`。
该函数如果可能，使用顺序一致的内存排序;如果不行，则使用“有序”排序。

### `T QAtomicInteger::operator++()`

**作用与语义：**

原子层预递增该`QAtomicInteger`值。返回该原子的新值。
该函数如果可能，使用顺序一致的内存排序;如果不行，则使用“有序”排序。

### `T QAtomicInteger::operator++(int)`

**作用与语义：**

原子后递增该`QAtomicInteger`值。返回该原子的旧值。
该函数如果可能，使用顺序一致的内存排序;如果不行，则使用“有序”排序。

### `T QAtomicInteger::operator+=(T value)`

**作用与语义：**

原子加法和取球。
读取该`QAtomicInteger`当前值，然后向当前值加上`value`，返回新值。
该函数如果可能，使用顺序一致的内存排序;如果不行，则使用“有序”排序。

### `T QAtomicInteger::operator--()`

**作用与语义：**

原子层预递减该`QAtomicInteger`值。返回该原子的新值。
该函数如果可能，使用顺序一致的内存排序;如果不行，则使用“有序”排序。

### `T QAtomicInteger::operator--(int)`

**作用与语义：**

原子后递减该`QAtomicInteger`的值。返回该原子的旧值。
该函数如果可能，使用顺序一致的内存排序;如果不行，则使用“有序”排序。

### `T QAtomicInteger::operator-=(T value)`

**作用与语义：**

原子潜艇和接球。
读取该`QAtomicInteger`当前值，然后将`value`减去到当前值，返回新值。
该函数如果可能，使用顺序一致的内存排序;如果不行，则使用“有序”排序。

### `QAtomicInteger<T> &QAtomicInteger::operator=(T)`

**作用与语义：**

如果可能，使用顺序一致的内存排序，原子性地将另一个值存储为该原子类型;如果不行，则使用“释放”顺序。该函数返回对该对象的引用。

### `[noexcept] QAtomicInteger<T> &QAtomicInteger::operator=(const QAtomicInteger<T> &other)`

**作用与语义：**

将`other`分配到该`QAtomicInteger`并返回该`QAtomicInteger`的引用。

### `T QAtomicInteger::operator^=(T value)`

**作用与语义：**

原子异或与取物。
读取该`QAtomicInteger`当前值，然后通过比特异或（`value`）返回当前值，返回新值。
该函数如果可能，使用顺序一致的内存排序;如果不行，则使用“有序”排序。

### `T QAtomicInteger::operator|=(T value)`

**作用与语义：**

原子弹或接球。
读取该`QAtomicInteger`的当前值，然后通过位`value`返回当前值，返回新的值。
该函数如果可能，使用顺序一致的内存排序;如果不行，则使用“有序”排序。

### `[noexcept, since 6.7] void qYieldCpu()`

**作用与语义：**

使用硬件指令暂停当前线程的执行，时间不定，且不取消调度该线程。该函数用于高吞吐量循环，代码期望另一个线程修改原子变量。这与`QThread::yieldCurrentThread()`完全不同，后者是操作系统层面操作，可能将整个线程从CPU中移除，允许其他线程（可能属于其他进程）运行。
所以，代替。
应该写。
这适用于同一核心上有硬件多线程时和不支持。对于硬件线程，它防止进一步的推测性执行填满流水线，从而使兄弟线程资源匮乏。在跨核和更高层级分离时，它允许缓存一致性协议将被修改和检查的缓存线分配给该代码预期结果的逻辑处理器。
还建议绕过不修改全局变量的代码，以避免独占获取内存位置的争用。因此，原子修改循环如自旋锁采集应为：
在x86处理器和带有`Zihintpause`扩展的RISC-V处理器上，这会发出`PAUSE`指令，但不支持该指令的处理器会忽略;在ARMv7或更高版本的ARM处理器上，则会发出`YIELD`指令。

**官方示例：**

```cpp
 while (!condition)
     ;
```

### `Q_ATOMIC_INTnn_FETCH_AND_ADD_IS_ALWAYS_NATIVE`

**作用与语义：**

当且仅当你的处理器支持对整数进行原子取加法时，该宏才被定义。
nn 是整数的大小，单位为 8、16、32 或 64。

### `Q_ATOMIC_INTnn_FETCH_AND_ADD_IS_NOT_NATIVE`

**作用与语义：**

当硬件不支持整数的原子取取加时，定义了该宏。
nn 是整数的大小，单位为 8、16、32 或 64。

### `Q_ATOMIC_INTnn_FETCH_AND_ADD_IS_SOMETIMES_NATIVE`

**作用与语义：**

当处理器只有特定世代支持整数原子取加时，该宏定义为。使用`QAtomicInteger::isFetchAndAddNative()`函数检查处理器支持的内容。
nn 是整数的大小，单位为 8、16、32 或 64。

### `Q_ATOMIC_INTnn_FETCH_AND_ADD_IS_WAIT_FREE`

**作用与语义：**

该宏与`Q_ATOMIC_INTnn_FETCH_AND_ADD_IS_ALWAYS_NATIVE`一起定义，表示原子取集加法在整数上是无等待的。
nn 是整数的大小，单位为 8、16、32 或 64。

### `Q_ATOMIC_INTnn_FETCH_AND_STORE_IS_ALWAYS_NATIVE`

**作用与语义：**

当且仅当你的处理器支持整数的原子取物存储时，定义了该宏。
nn 是整数的大小，单位为 8、16、32 或 64。

### `Q_ATOMIC_INTnn_FETCH_AND_STORE_IS_NOT_NATIVE`

**作用与语义：**

当硬件不支持整数的原子取物存储时，定义了该宏。
nn 是整数的大小，单位为 8、16、32 或 64。

### `Q_ATOMIC_INTnn_FETCH_AND_STORE_IS_SOMETIMES_NATIVE`

**作用与语义：**

当处理器只有特定世代支持整数原子取指存储时，该宏定义了。使用`QAtomicInteger::isFetchAndStoreNative()`函数检查处理器支持的内容。
nn 是整数的大小，单位为 8、16、32 或 64。

### `Q_ATOMIC_INTnn_FETCH_AND_STORE_IS_WAIT_FREE`

**作用与语义：**

该宏与`Q_ATOMIC_INTnn_FETCH_AND_STORE_IS_ALWAYS_NATIVE`一起定义，表示整数的原子取物存储是无等待的。
nn 是整数的大小，单位为 8、16、32 或 64。

### `Q_ATOMIC_INTnn_IS_SUPPORTED`

**作用与语义：**

如果该编译器/架构组合支持大小为 nn（位）的原子整数，则定义该宏。
nn 是整数的大小，单位为 8、16、32 或 64。
以下宏始终定义：
- Q_ATOMIC_INT8_IS_SUPPORTED
- Q_ATOMIC_INT16_IS_SUPPORTED
- Q_ATOMIC_INT32_IS_SUPPORTED

### `Q_ATOMIC_INTnn_REFERENCE_COUNTING_IS_ALWAYS_NATIVE`

**作用与语义：**

当且仅当你的处理器所有代都支持原子引用计数时，这个宏才被定义。
nn 是整数的大小，单位为 8、16、32 或 64。

### `Q_ATOMIC_INTnn_REFERENCE_COUNTING_IS_NOT_NATIVE`

**作用与语义：**

当硬件不支持原子引用计数时，该宏被定义。
nn 是整数的大小，单位为 8、16、32 或 64。

### `Q_ATOMIC_INTnn_REFERENCE_COUNTING_IS_SOMETIMES_NATIVE`

**作用与语义：**

当处理器的某些代值支持原子引用计数时，该宏定义了。使用`QAtomicInteger::isReferenceCountingNative()`函数检查处理器支持的内容。
nn 是整数的大小，单位为 8、16、32 或 64。

### `Q_ATOMIC_INTnn_REFERENCE_COUNTING_IS_WAIT_FREE`

**作用与语义：**

该宏与`Q_ATOMIC_INTnn_REFERENCE_COUNTING_IS_ALWAYS_NATIVE`一起定义，表示引用计数是无等待的。
nn 是整数的大小，单位为 8、16、32 或 64。

### `Q_ATOMIC_INTnn_TEST_AND_SET_IS_ALWAYS_NATIVE`

**作用与语义：**

当且仅当你的处理器支持整数的原子测试与集合时，这个宏才被定义。
nn 是整数的大小，单位为 8、16、32 或 64。

### `Q_ATOMIC_INTnn_TEST_AND_SET_IS_NOT_NATIVE`

**作用与语义：**

当硬件不支持整数原子测试和设置时，该宏定义。
nn 是整数的大小，单位为 8、16、32 或 64。

### `Q_ATOMIC_INTnn_TEST_AND_SET_IS_SOMETIMES_NATIVE`

**作用与语义：**

当处理器只有某些世代支持整数原子测试和集合时，该宏定义了。使用`QAtomicInteger::isTestAndSetNative()`函数检查处理器支持的内容。
nn 是整数的大小，单位为 8、16、32 或 64。

### `Q_ATOMIC_INTnn_TEST_AND_SET_IS_WAIT_FREE`

**作用与语义：**

该宏与`Q_ATOMIC_INTnn_TEST_AND_SET_IS_ALWAYS_NATIVE`一起定义，表示整数上的原子测试和集合是无等待的。
nn 是整数的大小，单位为 8、16、32 或 64。

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
