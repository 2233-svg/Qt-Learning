# QBitArray

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“Bit数组”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QBitArray` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QBitArray>`
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

- `QBitArray()`
- `QBitArray(qsizetype size, bool value = false)`
- `QBitArray(const QBitArray &other)`
- `QBitArray(QBitArray &&other)`
- `bool at(qsizetype i) const`
- `const char * bits() const`
- `void clear()`
- `void clearBit(qsizetype i)`
- `qsizetype count() const`
- `qsizetype count(bool on) const`
- `bool fill(bool value, qsizetype size = -1)`
- `void fill(bool value, qsizetype begin, qsizetype end)`
- `bool isEmpty() const`
- `bool isNull() const`
- `void resize(qsizetype size)`
- `void setBit(qsizetype i)`
- `void setBit(qsizetype i, bool value)`
- `qsizetype size() const`
- `void swap(QBitArray &other)`
- `bool testBit(qsizetype i) const`
- `(since 6.0) quint32 toUInt32(QSysInfo::Endian endianness, bool *ok = nullptr) const`
- `bool toggleBit(qsizetype i)`
- `void truncate(qsizetype pos)`
- `QBitArray & operator&=(QBitArray &&other)`
- `QBitArray & operator&=(const QBitArray &other)`
- `QBitArray & operator=(QBitArray &&other)`
- `QBitArray & operator=(const QBitArray &other)`
- `QBitRef operator[](qsizetype i)`
- `bool operator[](qsizetype i) const`
- `QBitArray & operator^=(QBitArray &&other)`
- `QBitArray & operator^=(const QBitArray &other)`
- `QBitArray & operator|=(QBitArray &&other)`
- `QBitArray & operator|=(const QBitArray &other)`

### 静态公有成员

- `QBitArray fromBits(const char *data, qsizetype size)`

### 相关非成员函数

- `bool operator!=(const QBitArray &lhs, const QBitArray &rhs)`
- `QBitArray operator&(QBitArray &&a1, QBitArray &&a2)`
- `QBitArray operator&(QBitArray &&a1, const QBitArray &a2)`
- `QBitArray operator&(const QBitArray &a1, QBitArray &&a2)`
- `QBitArray operator&(const QBitArray &a1, const QBitArray &a2)`
- `QDataStream & operator<<(QDataStream &out, const QBitArray &ba)`
- `bool operator==(const QBitArray &lhs, const QBitArray &rhs)`
- `QDataStream & operator>>(QDataStream &in, QBitArray &ba)`
- `QBitArray operator^(QBitArray &&a1, QBitArray &&a2)`
- `QBitArray operator^(QBitArray &&a1, const QBitArray &a2)`
- `QBitArray operator^(const QBitArray &a1, QBitArray &&a2)`
- `QBitArray operator^(const QBitArray &a1, const QBitArray &a2)`
- `QBitArray operator|(QBitArray &&a1, QBitArray &&a2)`
- `QBitArray operator|(QBitArray &&a1, const QBitArray &a2)`
- `QBitArray operator|(const QBitArray &a1, QBitArray &&a2)`
- `QBitArray operator|(const QBitArray &a1, const QBitArray &a2)`
- `QBitArray operator~(QBitArray a)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[noexcept] QBitArray::QBitArray()`

**作用与语义：**

构造一个空位数组。

### `[explicit] QBitArray::QBitArray(qsizetype size, bool value = false)`

**作用与语义：**

构造包含`size`位的比特数组。这些比特初始化为`value`，默认为false（0）。

### `[noexcept] QBitArray::QBitArray(const QBitArray &other)`

**作用与语义：**

构建了一份`other`的复制品。
该操作耗时为常数，因为 QBitArray 是隐式共享的。这使得从函数返回 QBitArray 非常快速。如果共享实例被修改，它将被复制（写时复制），这需要线性时间。

### `[noexcept] QBitArray::QBitArray(QBitArray &&other)`

**作用与语义：**

Move构造一个QBitArray实例，使其指向`other`指向的同一个对象。

### `bool QBitArray::at(qsizetype i) const`

**作用与语义：**

返回索引位置`i`位的比特值。
`i` 必须是位数组中的有效索引位置（即 0 <= `i` < `size()`）。

### `const char *QBitArray::bits() const`

**作用与语义：**

返回该`QBitArray`的稠密位数组指针。位数从每个字节的最低有效位向上计数。最后一个字节中相关的位数由 `size() % 8` 给出。

### `void QBitArray::clear()`

**作用与语义：**

清除位数组的内容，使其为空。

### `void QBitArray::clearBit(qsizetype i)`

**作用与语义：**

将索引位置`i`的位设为0。
`i` 必须是位数组中的有效索引位置（即 0 <= `i` < `size()`）。

### `qsizetype QBitArray::count() const`

**作用与语义：**

和`size()`一样。

### `qsizetype QBitArray::count(bool on) const`

**作用与语义：**

如果`on`为真，该函数返回比特数组中存储的1位数;否则返回0比特的数量。

### `bool QBitArray::fill(bool value, qsizetype size = -1)`

**作用与语义：**

将比特数组中的每个比特设置为`value`，成功时返回真;否则返回`false`。如果`size`与默认值-1不同，则比特数组会提前调整为`size`。

**官方示例：**

```cpp
 QBitArray ba(8);
 ba.fill(true);
 // ba: [ 1, 1, 1, 1, 1, 1, 1, 1 ]

 ba.fill(false, 2);
 // ba: [ 0, 0 ]
```

### `void QBitArray::fill(bool value, qsizetype begin, qsizetype end)`

**作用与语义：**

将位置于索引位置`begin`最多（但不包括）`end`到`value`。
`begin` 必须是位数组中的有效索引位置（0 <= `begin` < `size()`）。
`end`必须是有效的索引位置或等于 `size()`，在这种情况下，填充操作一直运行到数组末尾（0 <= `end` <= `size()`）。

**官方示例：**

```cpp
 QBitArray ba(4);
 ba.fill(true, 1, 2);            // ba: [ 0, 1, 0, 0 ]
 ba.fill(true, 1, 3);            // ba: [ 0, 1, 1, 0 ]
 ba.fill(true, 1, 4);            // ba: [ 0, 1, 1, 1 ]
```

### `[static] QBitArray QBitArray::fromBits(const char *data, qsizetype size)`

**作用与语义：**

创建一个`QBitArray`，稠密位数组位于`data`，位数为`size`。位`data`的字节数组必须至少为`size`/8（向上取整）字节。
如果`size`不是8的倍数，该函数将包含`data`中最后一个字节中最低`size`%的8位。

### `bool QBitArray::isEmpty() const`

**作用与语义：**

如果该位数组大小为0，则返回`true`;否则返回假。

### `bool QBitArray::isNull() const`

**作用与语义：**

如果该位数组为空，则返回`true`;否则返回`false`。
Qt 出于历史原因区分空位数组和空位数组。对于大多数应用来说，关键在于位数组是否包含任何数据，这可以通过`isEmpty()`来确定。

**官方示例：**

```cpp
 QBitArray().isNull();           // returns true
 QBitArray(0).isNull();          // returns false
 QBitArray(3).isNull();          // returns false
```

### `void QBitArray::resize(qsizetype size)`

**作用与语义：**

将位数组调整为`size`位。
如果`size`大于当前大小，位数组扩展为`size`位，后者加了额外的位。新比特初始化为false（0）。
如果`size`小于当前大小，则会从端部移除部分位。

### `void QBitArray::setBit(qsizetype i)`

**作用与语义：**

将索引位置`i`的位设为1。
`i` 必须是位数组中的有效索引位置（即 0 <= `i` < `size()`）。

### `void QBitArray::setBit(qsizetype i, bool value)`

**作用与语义：**

将索引位置`i`的位设为`value`。

### `qsizetype QBitArray::size() const`

**作用与语义：**

返回位数组中存储的位数。

### `[noexcept] void QBitArray::swap(QBitArray &other)`

**作用与语义：**

将该位数组与`other`交换。该操作非常快且从未失败。

### `bool QBitArray::testBit(qsizetype i) const`

**作用与语义：**

如果索引位置`i`位为1，则返回`true`;否则返回`false`。
`i` 必须是位数组中的有效索引位置（即 0 <= `i` < `size()`）。

### `[noexcept, since 6.0] quint32 QBitArray::toUInt32(QSysInfo::Endian endianness, bool *ok = nullptr) const`

**作用与语义：**

返回转换为整数的比特数组。转换基于`endianness`。将数组的前32位转换为`quint32`并返回，遵守`endianness`。如果`ok`不是空指针且数组超过32位，`ok`设为false，该函数返回0;否则为true。

### `bool QBitArray::toggleBit(qsizetype i)`

**作用与语义：**

在索引位置`i`处反转该位的值，返回该位之前的值，如果该位被设置为真，如果未设，则返回为假。
如果之前的值是0，新的值将是1。如果之前的值是1，新的值将是0。
`i` 必须是位数组中的有效索引位置（即 0 <= `i` < `size()`）。

### `void QBitArray::truncate(qsizetype pos)`

**作用与语义：**

在索引位置`pos`截断比特数组。
如果`pos`超出了阵列的尽头，则不会发生任何事。

### `QBitArray &QBitArray::operator&=(QBitArray &&other)`

**作用与语义：**

在该位数组和`other`中的所有位之间执行AND操作。将结果分配到该位数组，并返回对其的引用。
结果的长度为两个比特数组中最长的那一个，如果一个数组比另一个更短，任何缺失的位都取为0。

**官方示例：**

```cpp
 QBitArray a(3);
 QBitArray b(2);
 a[0] = 1; a[1] = 0; a[2] = 1;   // a: [ 1, 0, 1 ]
 b[0] = 1; b[1] = 1;             // b: [ 1, 1 ]
 a &= b;                         // a: [ 1, 0, 0 ]
```

### `[noexcept] QBitArray &QBitArray::operator=(QBitArray &&other)`

**作用与语义：**

`other`移动到该位数组并返回对该位数组的引用。

### `[noexcept] QBitArray &QBitArray::operator=(const QBitArray &other)`

**作用与语义：**

将`other`分配到该位数组，并返回对该位数组的引用。

### `QBitRef QBitArray::operator[](qsizetype i)`

**作用与语义：**

返回索引位置`i`位作为可修改的引用。
`i` 必须是位数组中的有效索引位置（即 0 <= `i` < `size()`）。
返回值类型为 QBitRef，是 `QBitArray` 的辅助类。当你获得类型为 QBitRef 的对象时，可以赋值，赋值会应用到你获得引用的`QBitArray`中位。
`testBit()`、`setBit()`和`clearBit()`功能稍快一些。

**官方示例：**

```cpp
 QBitArray a(3);
 a[0] = false;
 a[1] = true;
 a[2] = a[0] ^ a[1];
```

### `bool QBitArray::operator[](qsizetype i) const`

**作用与语义：**

返回索引位置`i`位作为可修改的引用。
`i` 必须是位数组中的有效索引位置（即 0 <= `i` < `size()`）。
返回值类型为 QBitRef，是 `QBitArray` 的辅助类。当你获得类型为 QBitRef 的对象时，可以赋值，赋值会应用到你获得引用的`QBitArray`中位。
`testBit()`、`setBit()`和`clearBit()`功能稍快一些。

**官方示例：**

```cpp
 QBitArray a(3);
 a[0] = false;
 a[1] = true;
 a[2] = a[0] ^ a[1];
```

### `QBitArray &QBitArray::operator^=(QBitArray &&other)`

**作用与语义：**

在该比特数组和`other`中的所有比特之间执行异或操作。将结果分配给该比特数组，并返回对其的引用。
结果的长度为两个比特数组中最长的那一个，如果一个数组比另一个更短，任何缺失的位都取为0。

**官方示例：**

```cpp
 QBitArray a(3);
 QBitArray b(2);
 a[0] = 1; a[1] = 0; a[2] = 1;   // a: [ 1, 0, 1 ]
 b[0] = 1; b[1] = 1;             // b: [ 1, 1 ]
 a ^= b;                         // a: [ 0, 1, 1 ]
```

### `QBitArray &QBitArray::operator|=(QBitArray &&other)`

**作用与语义：**

在该位数组中的所有位之间执行 OR 操作，并返回 `other`。将结果分配给该位数组，并返回对其的引用。
结果的长度为两个比特数组中最长的那一个，如果一个数组比另一个更短，任何缺失的位都取为0。

**官方示例：**

```cpp
 QBitArray a(3);
 QBitArray b(2);
 a[0] = 1; a[1] = 0; a[2] = 1;   // a: [ 1, 0, 1 ]
 b[0] = 1; b[1] = 1;             // b: [ 1, 1 ]
 a |= b;                         // a: [ 1, 1, 1 ]
```

### `[noexcept] bool operator!=(const QBitArray &lhs, const QBitArray &rhs)`

**作用与语义：**

如果 `lhs` 不等于 `rhs` 位数组，则返回 `true`；否则返回 `false`。

### `QBitArray operator&(QBitArray &&a1, QBitArray &&a2)`

**作用与语义：**

返回一个位数组，该数组是位数组 `a1` 和 `a2` 的 AND。
结果的长度为两个比特数组中最长的那一个，如果一个数组比另一个更短，任何缺失的位都取为0。

**官方示例：**

```cpp
 QBitArray a(3);
 QBitArray b(2);
 QBitArray c;
 a[0] = 1; a[1] = 0; a[2] = 1;   // a: [ 1, 0, 1 ]
 b[0] = 1; b[1] = 1;             // b: [ 1, 1 ]
 c = a & b;                      // c: [ 1, 0, 0 ]
```

### `QDataStream &operator<<(QDataStream &out, const QBitArray &ba)`

**作用与语义：**

将位数组`ba`写入流`out`。

### `[noexcept] bool operator==(const QBitArray &lhs, const QBitArray &rhs)`

**作用与语义：**

如果 `lhs` 等于 `rhs` 位数组，则返回 `true`；否则返回 `false`。

### `QDataStream &operator>>(QDataStream &in, QBitArray &ba)`

**作用与语义：**

从流`in`读取比特数组到`ba`。

### `QBitArray operator^(QBitArray &&a1, QBitArray &&a2)`

**作用与语义：**

返回一个位数组，它是`a1`和`a2`位数组的异或值。
结果的长度为两个比特数组中最长的那一个，如果一个数组比另一个更短，任何缺失的位都取为0。

**官方示例：**

```cpp
 QBitArray a(3);
 QBitArray b(2);
 QBitArray c;
 a[0] = 1; a[1] = 0; a[2] = 1;   // a: [ 1, 0, 1 ]
 b[0] = 1; b[1] = 1;             // b: [ 1, 1 ]
 c = a ^ b;                      // c: [ 0, 1, 1 ]
```

### `QBitArray operator|(QBitArray &&a1, QBitArray &&a2)`

**作用与语义：**

返回一个位数组，它是位数组 `a1` 和 `a2` 的 OR 值。
结果的长度为两个比特数组中最长的那一个，如果一个数组比另一个更短，任何缺失的位都取为0。

**官方示例：**

```cpp
 QBitArray a(3);
 QBitArray b(2);
 QBitArray c;
 a[0] = 1; a[1] = 0; a[2] = 1;   // a: [ 1, 0, 1 ]
 b[0] = 1; b[1] = 1;             // b: [ 1, 1 ]
 c = a | b;                      // c: [ 1, 1, 1 ]
```

### `QBitArray operator~(QBitArray a)`

**作用与语义：**

返回包含位数组倒置位的位数组`a`。

**官方示例：**

```cpp
 QBitArray a(3);
 QBitArray b;
 a[0] = 1; a[1] = 0; a[2] = 1;   // a: [ 1, 0, 1 ]
 b = ~a;                         // b: [ 0, 1, 0 ]
```

### `QBitArray & operator&=(const QBitArray &other)`

**作用与语义：**

在该位数组和`other`中的所有位之间执行AND操作。将结果分配到该位数组，并返回对其的引用。
结果的长度为两个比特数组中最长的那一个，如果一个数组比另一个更短，任何缺失的位都取为0。

**官方示例：**

```cpp
 QBitArray a(3);
 QBitArray b(2);
 a[0] = 1; a[1] = 0; a[2] = 1;   // a: [ 1, 0, 1 ]
 b[0] = 1; b[1] = 1;             // b: [ 1, 1 ]
 a &= b;                         // a: [ 1, 0, 0 ]
```

### `QBitArray & operator^=(const QBitArray &other)`

**作用与语义：**

在该比特数组和`other`中的所有比特之间执行异或操作。将结果分配给该比特数组，并返回对其的引用。
结果的长度为两个比特数组中最长的那一个，如果一个数组比另一个更短，任何缺失的位都取为0。

**官方示例：**

```cpp
 QBitArray a(3);
 QBitArray b(2);
 a[0] = 1; a[1] = 0; a[2] = 1;   // a: [ 1, 0, 1 ]
 b[0] = 1; b[1] = 1;             // b: [ 1, 1 ]
 a ^= b;                         // a: [ 0, 1, 1 ]
```

### `QBitArray & operator|=(const QBitArray &other)`

**作用与语义：**

在该位数组中的所有位之间执行 OR 操作，并返回 `other`。将结果分配给该位数组，并返回对其的引用。
结果的长度为两个比特数组中最长的那一个，如果一个数组比另一个更短，任何缺失的位都取为0。

**官方示例：**

```cpp
 QBitArray a(3);
 QBitArray b(2);
 a[0] = 1; a[1] = 0; a[2] = 1;   // a: [ 1, 0, 1 ]
 b[0] = 1; b[1] = 1;             // b: [ 1, 1 ]
 a |= b;                         // a: [ 1, 1, 1 ]
```

### `QBitArray operator&(QBitArray &&a1, const QBitArray &a2)`

**作用与语义：**

返回一个位数组，该数组是位数组 `a1` 和 `a2` 的 AND。
结果的长度为两个比特数组中最长的那一个，如果一个数组比另一个更短，任何缺失的位都取为0。

**官方示例：**

```cpp
 QBitArray a(3);
 QBitArray b(2);
 QBitArray c;
 a[0] = 1; a[1] = 0; a[2] = 1;   // a: [ 1, 0, 1 ]
 b[0] = 1; b[1] = 1;             // b: [ 1, 1 ]
 c = a & b;                      // c: [ 1, 0, 0 ]
```

### `QBitArray operator&(const QBitArray &a1, QBitArray &&a2)`

**作用与语义：**

返回一个位数组，该数组是位数组 `a1` 和 `a2` 的 AND。
结果的长度为两个比特数组中最长的那一个，如果一个数组比另一个更短，任何缺失的位都取为0。

**官方示例：**

```cpp
 QBitArray a(3);
 QBitArray b(2);
 QBitArray c;
 a[0] = 1; a[1] = 0; a[2] = 1;   // a: [ 1, 0, 1 ]
 b[0] = 1; b[1] = 1;             // b: [ 1, 1 ]
 c = a & b;                      // c: [ 1, 0, 0 ]
```

### `QBitArray operator&(const QBitArray &a1, const QBitArray &a2)`

**作用与语义：**

返回一个位数组，该数组是位数组 `a1` 和 `a2` 的 AND。
结果的长度为两个比特数组中最长的那一个，如果一个数组比另一个更短，任何缺失的位都取为0。

**官方示例：**

```cpp
 QBitArray a(3);
 QBitArray b(2);
 QBitArray c;
 a[0] = 1; a[1] = 0; a[2] = 1;   // a: [ 1, 0, 1 ]
 b[0] = 1; b[1] = 1;             // b: [ 1, 1 ]
 c = a & b;                      // c: [ 1, 0, 0 ]
```

### `QBitArray operator^(QBitArray &&a1, const QBitArray &a2)`

**作用与语义：**

返回一个位数组，它是`a1`和`a2`位数组的异或值。
结果的长度为两个比特数组中最长的那一个，如果一个数组比另一个更短，任何缺失的位都取为0。

**官方示例：**

```cpp
 QBitArray a(3);
 QBitArray b(2);
 QBitArray c;
 a[0] = 1; a[1] = 0; a[2] = 1;   // a: [ 1, 0, 1 ]
 b[0] = 1; b[1] = 1;             // b: [ 1, 1 ]
 c = a ^ b;                      // c: [ 0, 1, 1 ]
```

### `QBitArray operator^(const QBitArray &a1, QBitArray &&a2)`

**作用与语义：**

返回一个位数组，它是`a1`和`a2`位数组的异或值。
结果的长度为两个比特数组中最长的那一个，如果一个数组比另一个更短，任何缺失的位都取为0。

**官方示例：**

```cpp
 QBitArray a(3);
 QBitArray b(2);
 QBitArray c;
 a[0] = 1; a[1] = 0; a[2] = 1;   // a: [ 1, 0, 1 ]
 b[0] = 1; b[1] = 1;             // b: [ 1, 1 ]
 c = a ^ b;                      // c: [ 0, 1, 1 ]
```

### `QBitArray operator^(const QBitArray &a1, const QBitArray &a2)`

**作用与语义：**

返回一个位数组，它是`a1`和`a2`位数组的异或值。
结果的长度为两个比特数组中最长的那一个，如果一个数组比另一个更短，任何缺失的位都取为0。

**官方示例：**

```cpp
 QBitArray a(3);
 QBitArray b(2);
 QBitArray c;
 a[0] = 1; a[1] = 0; a[2] = 1;   // a: [ 1, 0, 1 ]
 b[0] = 1; b[1] = 1;             // b: [ 1, 1 ]
 c = a ^ b;                      // c: [ 0, 1, 1 ]
```

### `QBitArray operator|(QBitArray &&a1, const QBitArray &a2)`

**作用与语义：**

返回一个位数组，它是位数组 `a1` 和 `a2` 的 OR 值。
结果的长度为两个比特数组中最长的那一个，如果一个数组比另一个更短，任何缺失的位都取为0。

**官方示例：**

```cpp
 QBitArray a(3);
 QBitArray b(2);
 QBitArray c;
 a[0] = 1; a[1] = 0; a[2] = 1;   // a: [ 1, 0, 1 ]
 b[0] = 1; b[1] = 1;             // b: [ 1, 1 ]
 c = a | b;                      // c: [ 1, 1, 1 ]
```

### `QBitArray operator|(const QBitArray &a1, QBitArray &&a2)`

**作用与语义：**

返回一个位数组，它是位数组 `a1` 和 `a2` 的 OR 值。
结果的长度为两个比特数组中最长的那一个，如果一个数组比另一个更短，任何缺失的位都取为0。

**官方示例：**

```cpp
 QBitArray a(3);
 QBitArray b(2);
 QBitArray c;
 a[0] = 1; a[1] = 0; a[2] = 1;   // a: [ 1, 0, 1 ]
 b[0] = 1; b[1] = 1;             // b: [ 1, 1 ]
 c = a | b;                      // c: [ 1, 1, 1 ]
```

### `QBitArray operator|(const QBitArray &a1, const QBitArray &a2)`

**作用与语义：**

返回一个位数组，它是位数组 `a1` 和 `a2` 的 OR 值。
结果的长度为两个比特数组中最长的那一个，如果一个数组比另一个更短，任何缺失的位都取为0。

**官方示例：**

```cpp
 QBitArray a(3);
 QBitArray b(2);
 QBitArray c;
 a[0] = 1; a[1] = 0; a[2] = 1;   // a: [ 1, 0, 1 ]
 b[0] = 1; b[1] = 1;             // b: [ 1, 1 ]
 c = a | b;                      // c: [ 1, 1, 1 ]
```

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

`QBitArray` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
