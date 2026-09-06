# QSharedDataPointer

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“Shared数据Pointer”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QSharedDataPointer` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QSharedDataPointer>`
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

- `QSharedDataPointer()`
- `QSharedDataPointer(T *data)`
- `(since 6.0) QSharedDataPointer(T *data, QAdoptSharedDataTag)`
- `QSharedDataPointer(const QSharedDataPointer<T> &o)`
- `QSharedDataPointer(QSharedDataPointer<T> &&o)`
- `~QSharedDataPointer()`
- `const T * constData() const`
- `T * data()`
- `const T * data() const`
- `void detach()`
- `(since 6.0) T * get()`
- `(since 6.0) const T * get() const`
- `(since 6.0) void reset(T *ptr = nullptr)`
- `void swap(QSharedDataPointer<T> &other)`
- `(since 6.0) T * take()`
- `operator T *()`
- `operator const T *() const`
- `bool operator!() const`
- `T & operator*()`
- `const T & operator*() const`
- `T * operator->()`
- `const T * operator->() const`
- `QSharedDataPointer<T> & operator=(QSharedDataPointer<T> &&other)`
- `QSharedDataPointer<T> & operator=(T *o)`
- `QSharedDataPointer<T> & operator=(const QSharedDataPointer<T> &o)`

### 保护函数

- `T * clone()`

### 相关非成员函数

- `bool operator!=(T *const &lhs, const QSharedDataPointer<T> &rhs)`
- `bool operator!=(const QSharedDataPointer<T> &lhs, const QSharedDataPointer<T> &rhs)`
- `bool operator==(T *const &lhs, const QSharedDataPointer<T> &rhs)`
- `bool operator==(const QSharedDataPointer<T> &lhs, const QSharedDataPointer<T> &rhs)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QSharedDataPointer::Type`

**作用与语义：**

这是共享数据对象的类型。d 指针指向该类型的对象。

### `[noexcept] QSharedDataPointer::QSharedDataPointer()`

**作用与语义：**

构建一个以 `nullptr` 为 d 指针初始化的 QSharedDataPointer。

### `[explicit noexcept] QSharedDataPointer::QSharedDataPointer(T *data)`

**作用与语义：**

构建一个QSharedDataPointer，d指针设为`data`，并递增`data`的引用计数。

### `[noexcept, since 6.0] QSharedDataPointer::QSharedDataPointer(T *data, QAdoptSharedDataTag)`

**作用与语义：**

构建一个 QSharedDataPointer，d 指针设为 `data`。`data` 的参考计数器不递增;这可用于采用从 `take()` 获得的指针。

### `[noexcept] QSharedDataPointer::QSharedDataPointer(const QSharedDataPointer<T> &o)`

**作用与语义：**

将该数据的 d 指针设置为 `o` 中的 d 指针，并递增共享数据对象的引用计数。

### `[noexcept] QSharedDataPointer::QSharedDataPointer(QSharedDataPointer<T> &&o)`

**作用与语义：**

Move构建一个QSharedDataPointer实例，使其指向`o`所指向的同一对象。

### `QSharedDataPointer::~QSharedDataPointer()`

**作用与语义：**

减少共享数据对象的引用计数。如果引用计数为0，共享数据对象将被删除。随后会被销毁。

### `[protected] T *QSharedDataPointer::clone()`

**作用与语义：**

创建并返回当前数据的深度副本。当引用计数大于1时，`detach()`调用该函数以创建新的副本。该函数使用运算符new，调用类型为T的复制构造器。
提供该函数是为了支持你自己的类型“虚拟复制构造器”。为此，你应为自己的类型声明该函数的模板专用化，如下示例：
在上述示例中，clone() 函数的模板专用调用了 EmployeeData：：clone() 虚拟函数。从 EmployeeData 派生的类可以覆盖该函数并返回正确的多态类型。

**官方示例：**

```cpp
 template<>
 EmployeeData *QSharedDataPointer<EmployeeData>::clone()
 {
     return d->clone();
 }
```

### `[noexcept] const T *QSharedDataPointer::constData() const`

**作用与语义：**

返回一个指向共享数据对象的const指针。该函数不调用`detach()`。

### `T *QSharedDataPointer::data()`

**作用与语义：**

返回一个指向共享数据对象的指针。该函数调用`detach()`。

### `[noexcept] const T *QSharedDataPointer::data() const`

**作用与语义：**

返回一个指向共享数据对象的指针。该函数不调用`detach()`。

### `void QSharedDataPointer::detach()`

**作用与语义：**

如果共享数据对象的引用计数大于1，该函数会创建共享数据对象的深度副本，并将其d指针映射到该副本。
如果需要写时复制，`QSharedDataPointer`的非const成员函数会自动调用这个函数。你不需要自己调用它。

### `[since 6.0] T *QSharedDataPointer::get()`

**作用与语义：**

与`data()`相同。此功能旨在与STL兼容。

### `[noexcept, since 6.0] const T *QSharedDataPointer::get() const`

**作用与语义：**

与`data()`相同。此功能旨在与STL兼容。

### `[noexcept, since 6.0] void QSharedDataPointer::reset(T *ptr = nullptr)`

**作用与语义：**

将该数据的 d 指针设为 `ptr`，如果 `ptr` 未被`nullptr`，则增加`ptr`的引用计数。旧共享数据对象的引用计数减少，如果引用计数为 0，则该对象被删除。

### `[noexcept] void QSharedDataPointer::swap(QSharedDataPointer<T> &other)`

**作用与语义：**

将共享的数据指针与`other`交换。该操作非常快速且从未失败。

### `[noexcept, since 6.0] T *QSharedDataPointer::take()`

**作用与语义：**

返回一个指向共享对象的指针，并将其重置为`nullptr`。（也就是说，该函数将该对象的d指针设为`nullptr`。）。
注意：返回对象的引用计数不会被递减。该函数可以与构造函数一起使用，构造函数通过`QAdoptSharedDataTag`标签对象传输共享数据对象，无需中断原子操作。

### `QSharedDataPointer::operator T *()`

**作用与语义：**

返回一个指向共享数据对象的指针。该函数调用`detach()`。

### `[noexcept] QSharedDataPointer::operator const T *() const`

**作用与语义：**

返回一个指向共享数据对象的指针。该函数不调用`detach()`。

### `[noexcept] bool QSharedDataPointer::operator!() const`

**作用与语义：**

如果 d指针为`nullptr`，则返回 `true`。

### `T &QSharedDataPointer::operator*()`

**作用与语义：**

提供对共享数据对象成员的访问。该函数调用`detach()`。

### `const T &QSharedDataPointer::operator*() const`

**作用与语义：**

提供对共享数据对象成员的const访问。该函数不调用`detach()`。

### `T *QSharedDataPointer::operator->()`

**作用与语义：**

提供对共享数据对象成员的访问。该函数调用`detach()`。

### `[noexcept] const T *QSharedDataPointer::operator->() const`

**作用与语义：**

提供对共享数据对象成员的const访问。该函数不调用`detach()`。

### `[noexcept] QSharedDataPointer<T> &QSharedDataPointer::operator=(QSharedDataPointer<T> &&other)`

**作用与语义：**

Move-assign `other` 到该`QSharedDataPointer`实例。

### `[noexcept] QSharedDataPointer<T> &QSharedDataPointer::operator=(T *o)`

**作用与语义：**

将 d 指针 og 设为 `o`，并递增`o`的引用计数。旧共享数据对象的引用计数会被递减。如果旧共享数据对象的引用计数为 0，则该旧共享数据对象将被删除。

### `[noexcept] QSharedDataPointer<T> &QSharedDataPointer::operator=(const QSharedDataPointer<T> &o)`

**作用与语义：**

将该数据对象的d指针设置为`o`的d指针，并递增共享数据对象的引用计数。旧共享数据对象的引用计数递减。如果旧共享数据对象的引用计数为0，则该旧共享数据对象被删除。

### `[noexcept] bool operator!=(T *const &lhs, const QSharedDataPointer<T> &rhs)`

**作用与语义：**

如果 `rhs` 的 d 指针不是 `lhs`，则返回 `true`。d 指针。该函数不调用 `detach()`。

### `[noexcept] bool operator!=(const QSharedDataPointer<T> &lhs, const QSharedDataPointer<T> &rhs)`

**作用与语义：**

如果 `lhs` 和 `rhs` 的 d 指针不同，则返回 `true`。此函数不调用 `detach()`。

### `[noexcept] bool operator==(T *const &lhs, const QSharedDataPointer<T> &rhs)`

**作用与语义：**

如果 `rhs` 的 d 指针是 `lhs`，则返回 `true`。该函数不调用 `detach()`。

### `[noexcept] bool operator==(const QSharedDataPointer<T> &lhs, const QSharedDataPointer<T> &rhs)`

**作用与语义：**

如果 `lhs` 和 `rhs` 具有相同的 d 指针，则返回 `true`。此函数不会调用 `detach()`。

### `Type`

**作用与语义：**

这是共享数据对象的类型。d 指针指向该类型的对象。

### `operator T *()`

**作用与语义：**

返回一个指向共享数据对象的指针。该函数调用`detach()`。

### `operator const T *() const`

**作用与语义：**

返回一个指向共享数据对象的指针。该函数不调用`detach()`。

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

`QSharedDataPointer` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
