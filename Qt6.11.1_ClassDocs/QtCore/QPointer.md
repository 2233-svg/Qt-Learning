# QPointer

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“Pointer”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QPointer` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QPointer>`
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

- `QPointer()`
- `(since 6.6) QPointer(QPointer<X> &&other)`
- `QPointer(T *p)`
- `(since 6.6) QPointer(const QPointer<X> &other)`
- `QPointer(std::nullptr_t)`
- `~QPointer()`
- `void clear()`
- `T * data() const`
- `(since 6.0) T * get() const`
- `bool isNull() const`
- `void swap(QPointer<T> &other)`
- `operator T *() const`
- `T & operator*() const`
- `T * operator->() const`
- `(since 6.6.1) QPointer<T> & operator=(QPointer<X> &&other)`
- `QPointer<T> & operator=(T *p)`
- `(since 6.6) QPointer<T> & operator=(const QPointer<X> &other)`

### 相关非成员函数

- `bool operator!=(X *const &lhs, const QPointer<T> &rhs)`
- `bool operator!=(const QPointer<T> &lhs, X *const &rhs)`
- `bool operator!=(const QPointer<T> &lhs, const QPointer<X> &rhs)`
- `bool operator!=(const QPointer<T> &lhs, const std::nullptr_t &rhs)`
- `bool operator!=(const std::nullptr_t &lhs, const QPointer<T> &rhs)`
- `bool operator==(X *const &lhs, const QPointer<T> &rhs)`
- `bool operator==(const QPointer<T> &lhs, X *const &rhs)`
- `bool operator==(const QPointer<T> &lhs, const QPointer<X> &rhs)`
- `bool operator==(const QPointer<T> &lhs, const std::nullptr_t &rhs)`
- `bool operator==(const std::nullptr_t &lhs, const QPointer<T> &rhs)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[constexpr noexcept] QPointer::QPointer(std::nullptr_t)`

**作用与语义：**

构造一个值`nullptr`的守护指针。

### `[noexcept, since 6.6] template <typename X, QPointer<T>::if_convertible<X> = true> QPointer::QPointer(const QPointer<X> &other)`

**作用与语义：**

构造一个值`nullptr`的守护指针。

### `QPointer::QPointer(T *p)`

**作用与语义：**

转换构造器。通过移动或复制从`other`构建新`QPointer`。
移出的`QPointer`会被重置为nullptr。
注意：这些构造函数只有在`X*`可转换为`T*`时才参与超载解析。

### `QPointer::~QPointer()`

**作用与语义：**

摧毁被守护的指针。就像普通指针一样，摧毁被守护指针并不会摧毁被指向的物体。

### `[noexcept] void QPointer::clear()`

**作用与语义：**

清除`QPointer`物体。

### `[noexcept] T *QPointer::data() const`

**作用与语义：**

返回被守护对象的指针。

### `[noexcept, since 6.0] T *QPointer::get() const`

**作用与语义：**

与`data()`相同。此功能旨在与STL兼容。

### `[noexcept] bool QPointer::isNull() const`

**作用与语义：**

如果被引用对象已被销毁或不存在被引用对象，返回`true`;否则返回`false`。

### `[noexcept] void QPointer::swap(QPointer<T> &other)`

**作用与语义：**

将该指针与`other`交换。此操作非常快速且从未失败。

### `[noexcept] QPointer::operator T *() const`

**作用与语义：**

cast 算子;实现指针语义。由于该函数，你可以将`QPointer`<T>传递到需要 T* 的函数。

### `[noexcept] T &QPointer::operator*() const`

**作用与语义：**

Dereference 操作符;实现指针语义。只需像使用普通 C 指针一样使用这个操作符即可。

### `[noexcept] T *QPointer::operator->() const`

**作用与语义：**

超载箭头算子;实现指针语义。只需像使用普通 C 指针一样使用这个算子。

### `[noexcept, since 6.6.1] template <typename X, QPointer<T>::if_convertible<X> = true> QPointer<T> &QPointer::operator=(QPointer<X> &&other)`

**作用与语义：**

转换移动-赋值算符。使该被守护的指针守护`other`守护的同一对象，并将`other`重置为nullptr。
只有当`X*`可转换为`T*`时才参与重载决议。

### `QPointer<T> &QPointer::operator=(T *p)`

**作用与语义：**

赋值算符。这个守护指针现在会指向`p`指向的同一对象。

### `[noexcept, since 6.6] template <typename X, QPointer<T>::if_convertible<X> = true> QPointer<T> &QPointer::operator=(const QPointer<X> &other)`

**作用与语义：**

转换赋值算符。使这个被守卫的指针守卫同一个被`other`守护的物体。
只有当`X*`可转换为`T*`时才参与重载决议。

### `[noexcept] template <typename X> bool operator!=(X *const &lhs, const QPointer<T> &rhs)`

**作用与语义：**

不等式算符。如果`lhs`和守护指针`rhs`不指向同一对象，返回`true`，否则返回`false`。

### `[noexcept] template <typename X> bool operator!=(const QPointer<T> &lhs, X *const &rhs)`

**作用与语义：**

不等式算符。如果`rhs`和守护指针`lhs`指向的对象不相同，则返回`true`，否则返回`false`。

### `[noexcept(...)] template <typename X> bool operator!=(const QPointer<T> &lhs, const QPointer<X> &rhs)`

**作用与语义：**

不等式算符。如果守护指针`lhs`和`rhs`不指向同一对象，返回`true`，否则返回`false`。
注意：该功能仅在`true` `true`时使用。

### `[noexcept] bool operator!=(const QPointer<T> &lhs, const std::nullptr_t &rhs)`

**作用与语义：**

不等式算符。如果`lhs`守护的指针是有效（即非 `nullptr`）指针，返回 `true`，否则返回 `false`。

### `[noexcept] bool operator!=(const std::nullptr_t &lhs, const QPointer<T> &rhs)`

**作用与语义：**

不等式算符。如果`rhs`守护的指针是有效（即非`nullptr`）指针，返回`true`，否则返回`false`。

### `[noexcept] template <typename X> bool operator==(X *const &lhs, const QPointer<T> &rhs)`

**作用与语义：**

等号算符。如果`lhs`和守护指针`rhs`指向同一对象，返回`true`，否则返回`false`。

### `[noexcept] template <typename X> bool operator==(const QPointer<T> &lhs, X *const &rhs)`

**作用与语义：**

等号算符。如果`rhs`和守护指针`lhs`指向同一对象，则返回`true`，否则返回`false`。

### `[noexcept(...)] template <typename X> bool operator==(const QPointer<T> &lhs, const QPointer<X> &rhs)`

**作用与语义：**

等号算符。如果守护指针`lhs`和`rhs`指向同一对象，则返回`true`，否则返回`false`。
注意：该功能仅在`true` `true`时使用。

### `[noexcept] bool operator==(const QPointer<T> &lhs, const std::nullptr_t &rhs)`

**作用与语义：**

等号算符。如果`lhs`守护的指针是`nullptr`，则返回`true`，否则返回`false`。

### `[noexcept] bool operator==(const std::nullptr_t &lhs, const QPointer<T> &rhs)`

**作用与语义：**

等式算符。如果`rhs`守护的指针是`nullptr`，则返回`true`，否则返回`false`。

### `QPointer()`

**作用与语义：**

转换构造器。通过移动或复制从`other`构建新`QPointer`。
移出的`QPointer`会被重置为nullptr。
注意：这些构造函数只有在`X*`可转换为`T*`时才参与超载解析。

### `(since 6.6) QPointer(QPointer<X> &&other)`

**作用与语义：**

构造一个守护指针指向`p`所指向的同一对象。

### `operator T *() const`

**作用与语义：**

cast 算子;实现指针语义。由于该函数，你可以将`QPointer`<T>传递到需要 T* 的函数。

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

`QPointer` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
