# QWeakPointer

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“WeakPointer”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QWeakPointer` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QWeakPointer>`
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

- `QWeakPointer()`
- `QWeakPointer(const QSharedPointer<T> &other)`
- `QWeakPointer(const QWeakPointer<T> &other)`
- `~QWeakPointer()`
- `void clear()`
- `bool isNull() const`
- `QSharedPointer<T> lock() const`
- `(since 6.7) bool owner_before(const QSharedPointer<X> &other) const`
- `(since 6.7) bool owner_before(const QWeakPointer<X> &other) const`
- `(since 6.7) bool owner_equal(const QSharedPointer<X> &other) const`
- `(since 6.7) bool owner_equal(const QWeakPointer<X> &other) const`
- `(since 6.7) size_t owner_hash() const`
- `void swap(QWeakPointer<T> &other)`
- `QSharedPointer<T> toStrongRef() const`
- `operator bool() const`
- `bool operator!() const`
- `QWeakPointer<T> & operator=(const QSharedPointer<T> &other)`
- `QWeakPointer<T> & operator=(const QWeakPointer<T> &other)`

### 相关非成员函数

- `QWeakPointer<X> qWeakPointerCast(const QWeakPointer<T> &src)`
- `bool operator!=(const QSharedPointer<T> &ptr1, const QWeakPointer<X> &ptr2)`
- `bool operator!=(const QWeakPointer<T> &ptr1, const QSharedPointer<X> &ptr2)`
- `bool operator!=(const QWeakPointer<T> &lhs, std::nullptr_t)`
- `bool operator!=(std::nullptr_t, const QWeakPointer<T> &rhs)`
- `bool operator==(const QSharedPointer<T> &ptr1, const QWeakPointer<X> &ptr2)`
- `bool operator==(const QWeakPointer<T> &ptr1, const QSharedPointer<X> &ptr2)`
- `bool operator==(const QWeakPointer<T> &lhs, std::nullptr_t)`
- `bool operator==(std::nullptr_t, const QWeakPointer<T> &rhs)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QWeakPointer::QWeakPointer()`

**作用与语义：**

创建一个指向无物的QWeakPointer。

### `QWeakPointer::QWeakPointer(const QSharedPointer<T> &other)`

**作用与语义：**

创建一个QWeakPointer，保留对`other`所引用指针的弱引用。
如果`T`是该类模板参数的派生类型，QWeakPointer会自动执行cast。否则，你会遇到编译器错误。

### `[noexcept] QWeakPointer::QWeakPointer(const QWeakPointer<T> &other)`

**作用与语义：**

创建一个QWeakPointer，保留对`other`所引用指针的弱引用。
如果`T`是该类模板参数的派生类型，QWeakPointer会自动执行cast。否则，你会遇到编译器错误。

### `QWeakPointer::~QWeakPointer()`

**作用与语义：**

销毁该`QWeakPointer`对象。该对象引用的指针不会被删除。

### `void QWeakPointer::clear()`

**作用与语义：**

清除该`QWeakPointer`对象，丢弃它可能指向指针的引用。

### `bool QWeakPointer::isNull() const`

**作用与语义：**

如果该对象指向`nullptr`，返回`true`。
注意，由于弱引用的特性，`QWeakPointer`引用的指针随时可能变`nullptr`，因此该函数返回的值可以从假变真，从一个调用到另一个调用。

### `QSharedPointer<T> QWeakPointer::lock() const`

**作用与语义：**

和`toStrongRef()`一样。
该功能是为了与 std：：weak_ptr 的 API 兼容性而提供。

### `[noexcept, since 6.7] template <typename X> bool QWeakPointer::owner_before(const QWeakPointer<X> &other) const`

**作用与语义：**

返回 `true`当且仅当该智能指针在实现定义的基于所有者的排序中先于`other`。该排序使得两个智能指针如果都是空的，或者它们都拥有同一对象（即使它们的表观类型和指针不同），则视为等价的。

### `[noexcept, since 6.7] template <typename X> bool QWeakPointer::owner_equal(const QWeakPointer<X> &other) const`

**作用与语义：**

回报`true`当且仅当该智能指针和`other`持股时才会有回报。

### `[noexcept, since 6.7] size_t QWeakPointer::owner_hash() const`

**作用与语义：**

返回基于所有者的该智能指针对象的哈希值。比较相等（如`owner_equal`）的智能指针将拥有相同的基于所有者的哈希值。

### `[noexcept] void QWeakPointer::swap(QWeakPointer<T> &other)`

**作用与语义：**

将这个弱指针实例与`other`交换。该操作非常快且从未失败。

### `QSharedPointer<T> QWeakPointer::toStrongRef() const`

**作用与语义：**

将这个弱引用提升为强引用，并返回一个包含该引用的`QSharedPointer`对象。当升`QSharedPointer`时，该函数会验证该对象是否已经被删除。如果还没有，这个函数会增加对共享对象的引用数量，从而确保它不会被删除。
由于该函数可能无法获得对共享对象的有效强引用，你应始终通过调用返回对象的`QSharedPointer::isNull()`来验证转换是否成功。
例如，以下代码将被强引用的`QWeakPointer`提升，如果成功，则打印该索引的整数值：

**官方示例：**

```cpp
 QWeakPointer<int> weakref;

 // ...

 QSharedPointer<int> strong = weakref.toStrongRef();
 if (strong)
     qDebug() << "The value is:" << *strong;
 else
     qDebug() << "The value has already been deleted";
```

### `QWeakPointer::operator bool() const`

**作用与语义：**

如果包含的指针不`nullptr`，返回`true`。该函数适用于`if-constructs`，例如：
注意，由于弱引用的特性，`QWeakPointer`引用的指针随时可能变`nullptr`，因此该函数返回的值可能从真变假。

**官方示例：**

```cpp
 if (weakref) { /*...*/ }
```

### `bool QWeakPointer::operator!() const`

**作用与语义：**

如果该对象指向`nullptr`，返回`true`。该函数适合用于`if-constructs`，如：
注意，由于弱引用的特性，`QWeakPointer`引用的指针随时可能变`nullptr`，因此该函数返回的值可以从假变真。

**官方示例：**

```cpp
 if (!weakref) { /*...*/ }
```

### `QWeakPointer<T> &QWeakPointer::operator=(const QSharedPointer<T> &other)`

**作用与语义：**

使该对象共享`other`的指针。当前指针引用被丢弃但未被删除。
如果`T`是该类模板参数的派生类型，`QWeakPointer`会执行自动cast。否则，编译器会出错。

### `[noexcept] QWeakPointer<T> &QWeakPointer::operator=(const QWeakPointer<T> &other)`

**作用与语义：**

使该对象共享`other`的指针。当前指针引用被丢弃但未被删除。
如果`T`是该类模板参数的派生类型，`QWeakPointer`会执行自动cast。否则，编译器会出错。

### `template <typename X, typename T> QWeakPointer<X> qWeakPointerCast(const QWeakPointer<T> &src)`

**作用与语义：**

返回一个弱指针指向`src`持有的指针，投射为类型`X`。类型`T`和`X`必须属于一个层级结构，`static_cast`才能成功。
注意`X`必须使用与`T`相同的cv限定符（`const`和`volatile`），否则代码将无法编译。使用`qSharedPointerConstCast`来去除一致性。

### `template <typename T, typename X> bool operator!=(const QSharedPointer<T> &ptr1, const QWeakPointer<X> &ptr2)`

**作用与语义：**

如果 `ptr1` 和 `ptr2` 指向不同的指针，则返回 `true`。
如果 `ptr2` 的模板参数不同于 `ptr1` 的，`QSharedPointer` 将尝试执行自动 `static_cast`，以确保正在比较的指针相等。如果 `ptr2` 的模板参数既不是 `ptr1` 的基类也不是派生类类型，你将得到编译错误。

### `template <typename T, typename X> bool operator!=(const QWeakPointer<T> &ptr1, const QSharedPointer<X> &ptr2)`

**作用与语义：**

如果 `ptr1` 和 `ptr2` 指向不同的指针，则返回 `true`。
如果 `ptr2` 的模板参数不同于 `ptr1` 的，`QSharedPointer` 将尝试执行自动 `static_cast`，以确保正在比较的指针相等。如果 `ptr2` 的模板参数既不是 `ptr1` 的基类也不是派生类类型，你将得到编译错误。

### `template <typename T> bool operator!=(const QWeakPointer<T> &lhs, std::nullptr_t)`

**作用与语义：**

如果`lhs`指的是有效（即非空）指针，返回`true`。

### `template <typename T> bool operator!=(std::nullptr_t, const QWeakPointer<T> &rhs)`

**作用与语义：**

如果 `rhs` 指向一个有效（即非空）指针，则返回 `true`。

### `template <typename T, typename X> bool operator==(const QSharedPointer<T> &ptr1, const QWeakPointer<X> &ptr2)`

**作用与语义：**

如果 `ptr1` 和 `ptr2` 指向相同的指针，则返回 `true`。
如果 `ptr2` 的模板参数与 `ptr1` 的不同，`QSharedPointer` 将尝试执行自动 `static_cast` 以确保被比较的指针相等。如果 `ptr2` 的模板参数既不是 `ptr1` 的基类类型，也不是派生类型，你将得到编译错误。

### `template <typename T, typename X> bool operator==(const QWeakPointer<T> &ptr1, const QSharedPointer<X> &ptr2)`

**作用与语义：**

如果 `ptr1` 和 `ptr2` 指向相同的指针，则返回 `true`。
如果 `ptr2` 的模板参数与 `ptr1` 的不同，`QSharedPointer` 将尝试执行自动 `static_cast` 以确保被比较的指针相等。如果 `ptr2` 的模板参数既不是 `ptr1` 的基类类型，也不是派生类型，你将得到编译错误。

### `template <typename T> bool operator==(const QWeakPointer<T> &lhs, std::nullptr_t)`

**作用与语义：**

如果`lhs`指`nullptr`，返回会`true`。

### `template <typename T> bool operator==(std::nullptr_t, const QWeakPointer<T> &rhs)`

**作用与语义：**

如果 `rhs` 指的是 `nullptr`，则返回 `true`。

### `(since 6.7) bool owner_before(const QSharedPointer<X> &other) const`

**作用与语义：**

返回 `true`当且仅当该智能指针在实现定义的基于所有者的排序中先于`other`。该排序使得两个智能指针如果都是空的，或者它们都拥有同一对象（即使它们的表观类型和指针不同），则视为等价的。

### `(since 6.7) bool owner_equal(const QSharedPointer<X> &other) const`

**作用与语义：**

回报`true`当且仅当该智能指针和`other`持股时才会有回报。

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

`QWeakPointer` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
