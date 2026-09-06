# QExplicitlySharedDataPointer

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“ExplicitlyShared数据Pointer”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QExplicitlySharedDataPointer` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QExplicitlySharedDataPointer>`
- 继承自：QSharedDataPointerBase
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

### 公有类型

- `Type`

### 公有函数

- `QExplicitlySharedDataPointer()`
- `QExplicitlySharedDataPointer(T *data)`
- `QExplicitlySharedDataPointer(const QExplicitlySharedDataPointer<X> &o)`
- `QExplicitlySharedDataPointer(const QExplicitlySharedDataPointer<T> &o)`
- `QExplicitlySharedDataPointer(QExplicitlySharedDataPointer<T> &&o)`
- `~QExplicitlySharedDataPointer()`
- `const T * constData() const`
- `T * data() const`
- `void detach()`
- `(since 6.0) T * get() const`
- `(since 6.0) void reset(T *ptr = nullptr)`
- `void swap(QExplicitlySharedDataPointer<T> &other)`
- `T * take()`
- `operator bool() const`
- `bool operator!() const`
- `T & operator*() const`
- `T * operator->()`
- `T * operator->() const`
- `QExplicitlySharedDataPointer<T> & operator=(QExplicitlySharedDataPointer<T> &&other)`
- `QExplicitlySharedDataPointer<T> & operator=(T *o)`
- `QExplicitlySharedDataPointer<T> & operator=(const QExplicitlySharedDataPointer<T> &o)`

### 保护函数

- `T * clone()`

### 相关非成员函数

- `bool operator!=(const QExplicitlySharedDataPointer<T> &lhs, const QExplicitlySharedDataPointer<T> &rhs)`
- `bool operator!=(const T *const &lhs, const QExplicitlySharedDataPointer<T> &rhs)`
- `bool operator==(const QExplicitlySharedDataPointer<T> &lhs, const QExplicitlySharedDataPointer<T> &rhs)`
- `bool operator==(const T *const &lhs, const QExplicitlySharedDataPointer<T> &rhs)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QExplicitlySharedDataPointer::Type`

**作用与语义：**

这是共享数据对象的类型。d 指针指向该类型的对象。

### `[noexcept] QExplicitlySharedDataPointer::QExplicitlySharedDataPointer()`

**作用与语义：**

构建一个以 `nullptr` 为 d 指针初始化的 QExplicitlySharedDataPointer。

### `[explicit noexcept] QExplicitlySharedDataPointer::QExplicitlySharedDataPointer(T *data)`

**作用与语义：**

构建一个QExplicitlySharedDataPointer，d指针设为`data`并递增`data`的引用计数。

### `[noexcept] template <typename X> QExplicitlySharedDataPointer::QExplicitlySharedDataPointer(const QExplicitlySharedDataPointer<X> &o)`

**作用与语义：**

此复制构造函数的不同之处在于，它允许`o`是不同类型的显式共享数据指针，但其共享数据对象是兼容的。
默认情况下，将`o`（类型为`X *`）的d指针隐式转换为`T *`类型；此转换的结果被设置为此对象的d指针，共享数据对象的引用计数增加。

### `[noexcept] QExplicitlySharedDataPointer::QExplicitlySharedDataPointer(const QExplicitlySharedDataPointer<T> &o)`

**作用与语义：**

该标准复制构造器将该数据的d指针映射到d指针`o`并递增共享数据对象的引用计数。

### `[noexcept] QExplicitlySharedDataPointer::QExplicitlySharedDataPointer(QExplicitlySharedDataPointer<T> &&o)`

**作用与语义：**

Move-构建一个QExplicitlySharedDataPointer实例，使其指向`o`所指向的同一对象。

### `QExplicitlySharedDataPointer::~QExplicitlySharedDataPointer()`

**作用与语义：**

减少共享数据对象的引用计数。如果引用计数为0，共享数据对象将被删除。随后会被销毁。

### `[protected] T *QExplicitlySharedDataPointer::clone()`

**作用与语义：**

创建并返回当前数据的深度副本。当引用计数大于1时，`detach()`调用该函数以创建新副本。该函数使用运算符new，调用类型为T的复制构造器。
关于如何使用，请参见 `QSharedDataPointer`<T>：：clone() 一节。

### `[noexcept] const T *QExplicitlySharedDataPointer::constData() const`

**作用与语义：**

返回一个指向共享数据对象的const指针。

### `[noexcept] T *QExplicitlySharedDataPointer::data() const`

**作用与语义：**

返回指向共享数据对象的指针。

### `void QExplicitlySharedDataPointer::detach()`

**作用与语义：**

如果共享数据对象的引用计数大于1，该函数会创建共享数据对象的深度副本，并将其d指针映射到该副本。
由于`QExplicitlySharedDataPointer`不执行`QSharedDataPointer`成员所做的自动复制写操作，detach() 在该类的成员函数中不会被自动调用。如果你发现代码中处处调用 detach()，可以考虑使用 `QSharedDataPointer`。

### `[noexcept, since 6.0] T *QExplicitlySharedDataPointer::get() const`

**作用与语义：**

与`data()`相同。此功能旨在与STL兼容。

### `[noexcept, since 6.0] void QExplicitlySharedDataPointer::reset(T *ptr = nullptr)`

**作用与语义：**

将该数据的 d 指针设为 `ptr`，如果 `ptr` 未被`nullptr`，则增加`ptr`的引用计数。旧共享数据对象的引用计数减少，如果引用计数为 0，则该对象被删除。

### `[noexcept] void QExplicitlySharedDataPointer::swap(QExplicitlySharedDataPointer<T> &other)`

**作用与语义：**

将这个显式共享的数据指针与`other`交换。该操作非常快且从未失败。

### `[noexcept] T *QExplicitlySharedDataPointer::take()`

**作用与语义：**

返回一个指向共享对象的指针，并将其重置为`nullptr`。（也就是说，该函数将该对象的d指针设为`nullptr`。）。
注意：返回对象的引用计数不会被递减。该函数可以与构造函数一起使用，构造函数通过`QAdoptSharedDataTag`标签对象传输共享数据对象，无需中断原子操作。

### `[noexcept] QExplicitlySharedDataPointer::operator bool() const`

**作用与语义：**

如果 d 指针不是空指针，则返回 `true`。

### `[noexcept] bool QExplicitlySharedDataPointer::operator!() const`

**作用与语义：**

如果 d指针为`nullptr`，则返回 `true`。

### `T &QExplicitlySharedDataPointer::operator*() const`

**作用与语义：**

提供对共享数据对象成员的访问。

### `[noexcept] T *QExplicitlySharedDataPointer::operator->()`

**作用与语义：**

提供对共享数据对象成员的访问。

### `[noexcept] T *QExplicitlySharedDataPointer::operator->() const`

**作用与语义：**

提供对共享数据对象成员的const访问。

### `[noexcept] QExplicitlySharedDataPointer<T> &QExplicitlySharedDataPointer::operator=(QExplicitlySharedDataPointer<T> &&other)`

**作用与语义：**

移动分配`other`到该`QExplicitlySharedDataPointer`实例。

### `[noexcept] QExplicitlySharedDataPointer<T> &QExplicitlySharedDataPointer::operator=(T *o)`

**作用与语义：**

将该数据的 d 指针设为 `o`，并增加`o`的引用计数。旧共享数据对象的引用计数被递减。如果旧共享数据对象的引用计数为 0，则该旧共享数据对象被删除。

### `[noexcept] QExplicitlySharedDataPointer<T> &QExplicitlySharedDataPointer::operator=(const QExplicitlySharedDataPointer<T> &o)`

**作用与语义：**

将该数据对象的d指针设置为`o`的d指针，并递增共享数据对象的引用计数。旧共享数据对象的引用计数递减。如果旧共享数据对象的引用计数为0，则该旧共享数据对象被删除。

### `[noexcept] bool operator!=(const QExplicitlySharedDataPointer<T> &lhs, const QExplicitlySharedDataPointer<T> &rhs)`

**作用与语义：**

如果 `lhs` 和 `rhs` 没有相同的 d 指针，则返回 `true`。

### `[noexcept] bool operator!=(const T *const &lhs, const QExplicitlySharedDataPointer<T> &rhs)`

**作用与语义：**

如果`rhs`的d指针不`lhs`，则返回`true`。

### `[noexcept] bool operator==(const QExplicitlySharedDataPointer<T> &lhs, const QExplicitlySharedDataPointer<T> &rhs)`

**作用与语义：**

如果 `lhs` 和 `rhs` 拥有相同的 d 指针，则返回 `true`。

### `[noexcept] bool operator==(const T *const &lhs, const QExplicitlySharedDataPointer<T> &rhs)`

**作用与语义：**

如果`rhs`的d指针是`lhs`，则返回`true`。

### `Type`

**作用与语义：**

这是共享数据对象的类型。d 指针指向该类型的对象。

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

`QExplicitlySharedDataPointer` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
