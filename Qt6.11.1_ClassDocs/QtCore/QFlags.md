# QFlags

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“Flags”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QFlags` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QFlags>`
- 继承自：QtPrivate::QFlagsStorageHelper
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

- `Int`
- `enum_type`

### 公有函数

- `QFlags()`
- `QFlags(Enum flags)`
- `QFlags(QFlag flag)`
- `QFlags(std::initializer_list<Enum> flags)`
- `(since 6.9) QFlags(std::in_place_t, QFlags<T>::Int flags)`
- `QFlags(const QFlags<T> &other)`
- `QFlags<T> & setFlag(Enum flag, bool on = true)`
- `(since 6.2) bool testAnyFlag(Enum flag) const`
- `(since 6.2) bool testAnyFlags(QFlags<T> flags) const`
- `bool testFlag(Enum flag) const`
- `(since 6.2) bool testFlags(QFlags<T> flags) const`
- `(since 6.2) QFlags<T>::Int toInt() const`
- `operator QFlags<T>::Int() const`
- `bool operator!() const`
- `QFlags<T> operator&(int mask) const`
- `QFlags<T> operator&(Enum mask) const`
- `(since 6.2) QFlags<T> operator&(QFlags<T> mask) const`
- `QFlags<T> operator&(uint mask) const`
- `QFlags<T> & operator&=(int mask)`
- `QFlags<T> & operator&=(Enum mask)`
- `(since 6.2) QFlags<T> & operator&=(QFlags<T> mask)`
- `QFlags<T> & operator&=(uint mask)`
- `int & operator=(const QFlags<T> &other)`
- `QFlags<T> operator^(QFlags<T> other) const`
- `QFlags<T> operator^(Enum other) const`
- `QFlags<T> & operator^=(QFlags<T> other)`
- `QFlags<T> & operator^=(Enum other)`
- `QFlags<T> operator|(QFlags<T> other) const`
- `QFlags<T> operator|(Enum other) const`
- `QFlags<T> & operator|=(QFlags<T> other)`
- `QFlags<T> & operator|=(Enum other)`
- `QFlags<T> operator~() const`

### 静态公有成员

- `(since 6.2) QFlags<T> fromInt(QFlags<T>::Int i)`

### 相关非成员函数

- `(since 6.2) size_t qHash(QFlags<Enum> key, size_t seed = 0)`
- `(since 6.2) bool operator!=(Enum lhs, QFlags<T> rhs)`
- `(since 6.2) bool operator!=(QFlags<T> lhs, Enum rhs)`
- `(since 6.2) bool operator!=(QFlags<T> lhs, QFlags<T> rhs)`
- `(since 6.2) bool operator==(Enum lhs, QFlags<T> rhs)`
- `(since 6.2) bool operator==(QFlags<T> lhs, Enum rhs)`
- `(since 6.2) bool operator==(QFlags<T> lhs, QFlags<T> rhs)`

### 公开宏

- `Q_DECLARE_FLAGS(Flags, Enum)`
- `Q_DECLARE_OPERATORS_FOR_FLAGS(Flags)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[alias] QFlags::Int`

**作用与语义：**

Typedef 用于存储和隐式转换的整数类型。根据枚举底层类型是有符号还是无符号，以及自 Qt 6.9 起的枚举大小，可以选择 `qintXX` 或 `quintXX`。通常，枚举大小为 `qint32`（`int`）或 `quint32`（`unsigned`）。

### `QFlags::enum_type`

**作用与语义：**

Enum 模板类型用 Typedef。

### `[constexpr noexcept] QFlags::QFlags()`

**作用与语义：**

构造一个没有设置标志的QFlags对象。

### `[constexpr noexcept] QFlags::QFlags(Enum flags)`

**作用与语义：**

构建一个QFlags对象来存储`flags`。

### `[constexpr noexcept] QFlags::QFlags(QFlag flag) requires (sizeof(Enum) == sizeof(int))`

**作用与语义：**

构造一个以整数`flag`初始化的QFlags对象。
`QFlag`类型是辅助类型。通过在此使用它而非`int`，我们有效确保任意枚举值无法被转换为QFlags，而未类型枚举值（即`int`值）则可以。
该构造函数仅适用于32位`Enum`类型。为了支持所有枚举大小，请考虑使用`std::in_place_t`构造器。

### `[constexpr noexcept] QFlags::QFlags(std::initializer_list<Enum> flags)`

**作用与语义：**

构建一个QFlags对象，初始化为所有`flags`，使用按位OR操作符组合。

### `[constexpr noexcept, since 6.9] QFlags::QFlags(std::in_place_t, QFlags<T>::Int flags)`

**作用与语义：**

构造一个以整数`flags`初始化的QFlags对象。

### `[default] QFlags::QFlags(const QFlags<T> &other)`

**作用与语义：**

复制了`other`。

### `[static constexpr noexcept, since 6.2] QFlags<T> QFlags::fromInt(QFlags<T>::Int i)`

**作用与语义：**

构造一个`QFlags`对象，表示整数值`i`。

### `[constexpr noexcept] QFlags<T> &QFlags::setFlag(Enum flag, bool on = true)`

**作用与语义：**

如果`on` `true`，则将旗标设为`flag`;如果`on`为`false`，则撤销。返回对该对象的引用。

### `[constexpr noexcept, since 6.2] bool QFlags::testAnyFlag(Enum flag) const`

**作用与语义：**

如果`flag`中设置的任何标志也被设置在该标志对象中，返回`true`，否则`false`。如果`flag`没有设置标志，返回总是`false`。

### `[constexpr noexcept, since 6.2] bool QFlags::testAnyFlags(QFlags<T> flags) const`

**作用与语义：**

如果`flags`中设置的任何标志也被设置在该标志对象中，返回`true`，否则返回`false`。如果`flags`没有设置标志，返回总是`false`。

### `[constexpr noexcept] bool QFlags::testFlag(Enum flag) const`

**作用与语义：**

如果`flag`设置了标志，返回`true`，否则`false`。
注意：如果`flag`包含多个位为1的位（例如，如果它是一个枚举器，其位数与其他枚举器的位数或值相等），那么该函数只有当且仅当该标志对象的所有位都被设置为1时，该函数才返回`true`。另一方面，如果`flag`没有位设为1（即其整数值为0），那么该函数返回`true`当且仅当该标志对象也没有位设为1时。

### `[constexpr noexcept, since 6.2] bool QFlags::testFlags(QFlags<T> flags) const`

**作用与语义：**

如果该标志对象与给定`flags`匹配，返回`true`。
如果`flags`设置了任何标志，则该标志对象恰好匹配，前提是`flags`中所有设置的标志也都设置在该对象中。否则，当`flags`没有设置标志时，该标志对象只有在也没有设置标志时才匹配。

### `[constexpr noexcept, since 6.2] QFlags<T>::Int QFlags::toInt() const`

**作用与语义：**

返回`QFlags`对象中存储的值为整数。注意，返回的整数可能是有符号或无符号的，取决于枚举的底层类型是有符号还是无符号。

### `[constexpr noexcept] QFlags::operator QFlags<T>::Int() const`

**作用与语义：**

返回存储在`QFlags`对象中的整数值。

### `[constexpr noexcept] bool QFlags::operator!() const`

**作用与语义：**

如果没有设置标志（即`QFlags`对象存储的值为0），返回`true`;否则返回`false`。

### `[constexpr noexcept] QFlags<T> QFlags::operator&(int mask) const`

**作用与语义：**

返回一个`QFlags`对象，包含该对象和`mask`的位与操作结果。
如果定义了`QT_TYPESAFE_FLAGS`宏，该操作符将被禁用。注意，对于64位`QFlags`也未扩展到64位：支持64位时，使用类型安全重载。

### `[constexpr noexcept] QFlags<T> QFlags::operator&(Enum mask) const`

**作用与语义：**

返回一个`QFlags`对象，包含该对象和`mask`的位与操作结果。
如果定义了`QT_TYPESAFE_FLAGS`宏，该操作符将被禁用。注意，对于64位`QFlags`也未扩展到64位：支持64位时，使用类型安全重载。

### `[constexpr noexcept, since 6.2] QFlags<T> QFlags::operator&(QFlags<T> mask) const`

**作用与语义：**

返回一个`QFlags`对象，包含该对象和`mask`的位与操作结果。
如果定义了`QT_TYPESAFE_FLAGS`宏，该操作符将被禁用。注意，对于64位`QFlags`也未扩展到64位：支持64位时，使用类型安全重载。

### `[constexpr noexcept] QFlags<T> QFlags::operator&(uint mask) const`

**作用与语义：**

如果定义了 `QT_TYPESAFE_FLAGS` 宏，则此运算符被禁用。请注意，它也未扩展到 64 位 `QFlags` 的 64 位：对于 64 位支持，请使用类型安全的重载。

### `[constexpr noexcept] QFlags<T> &QFlags::operator&=(int mask)`

**作用与语义：**

对 `mask` 执行逐位 AND 操作，并将结果存储在这个`QFlags`对象中。返回对该对象的引用。
如果定义了`QT_TYPESAFE_FLAGS`宏，该操作符将被禁用。注意，对于64位`QFlags`也未扩展到64位：支持64位时，使用类型安全重载。

### `[constexpr noexcept] QFlags<T> &QFlags::operator&=(Enum mask)`

**作用与语义：**

对 `mask` 执行逐位 AND 操作，并将结果存储在这个`QFlags`对象中。返回对该对象的引用。
如果定义了`QT_TYPESAFE_FLAGS`宏，该操作符将被禁用。注意，对于64位`QFlags`也未扩展到64位：支持64位时，使用类型安全重载。

### `[constexpr noexcept, since 6.2] QFlags<T> &QFlags::operator&=(QFlags<T> mask)`

**作用与语义：**

对 `mask` 执行逐位 AND 操作，并将结果存储在这个`QFlags`对象中。返回对该对象的引用。
如果定义了`QT_TYPESAFE_FLAGS`宏，该操作符将被禁用。注意，对于64位`QFlags`也未扩展到64位：支持64位时，使用类型安全重载。

### `[constexpr noexcept] QFlags<T> &QFlags::operator&=(uint mask)`

**作用与语义：**

如果定义了 `QT_TYPESAFE_FLAGS` 宏，则此运算符被禁用。请注意，它也未扩展到 64 位 `QFlags` 的 64 位：对于 64 位支持，请使用类型安全的重载。

### `[default] int &QFlags::operator=(const QFlags<T> &other)`

**作用与语义：**

将`other`分配到该对象，并返回对该对象的引用。

### `[constexpr noexcept] QFlags<T> QFlags::operator^(QFlags<T> other) const`

**作用与语义：**

返回一个`QFlags`对象，包含该对象和`other`的位异或操作结果。

### `[constexpr noexcept] QFlags<T> QFlags::operator^(Enum other) const`

**作用与语义：**

返回一个`QFlags`对象，包含该对象和`other`的位异或操作结果。

### `[constexpr noexcept] QFlags<T> &QFlags::operator^=(QFlags<T> other)`

**作用与语义：**

对 `other` 执行逐位异或操作，并将结果存储在这个`QFlags`对象中。返回对该对象的引用。

### `[constexpr noexcept] QFlags<T> &QFlags::operator^=(Enum other)`

**作用与语义：**

对 `other` 执行逐位异或操作，并将结果存储在这个`QFlags`对象中。返回对该对象的引用。

### `[constexpr noexcept] QFlags<T> QFlags::operator|(QFlags<T> other) const`

**作用与语义：**

返回一个`QFlags`对象，包含对该对象和`other`的位或操作结果。

### `[constexpr noexcept] QFlags<T> QFlags::operator|(Enum other) const`

**作用与语义：**

返回一个`QFlags`对象，包含对该对象和`other`的位或操作结果。

### `[constexpr noexcept] QFlags<T> &QFlags::operator|=(QFlags<T> other)`

**作用与语义：**

对 `other` 执行按位的 OR 操作，并将结果存储在这个`QFlags`对象中。返回对该对象的引用。

### `[constexpr noexcept] QFlags<T> &QFlags::operator|=(Enum other)`

**作用与语义：**

对 `other` 执行按位的 OR 操作，并将结果存储在这个`QFlags`对象中。返回对该对象的引用。

### `[constexpr noexcept] QFlags<T> QFlags::operator~() const`

**作用与语义：**

返回一个包含该对象逐位否定的`QFlags`对象。

### `[constexpr noexcept, since 6.2] template <typename Enum> size_t qHash(QFlags<Enum> key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `[constexpr noexcept, since 6.2] bool operator!=(Enum lhs, QFlags<T> rhs)`

**作用与语义：**

比较`lhs`和`rhs`的不等式;如果两个参数不完全代表相同的值（位掩码），则视为不同。

### `[constexpr noexcept, since 6.2] bool operator==(Enum lhs, QFlags<T> rhs)`

**作用与语义：**

比较`lhs`和`rhs`以求相等;如果两个参数代表完全相同的值（位掩码），则视为相等。

### `Q_DECLARE_FLAGS(Flags, Enum)`

**作用与语义：**

Q_DECLARE_FLAGS()宏展开为。
`Enum` 是现有的枚举类型名称，而 `Flags` 是`QFlags`<Enum>类型定义的名称。
详情请参见`QFlags`文档。

**官方示例：**

```cpp
 typedef QFlags<Enum> Flags;
```

### `Q_DECLARE_OPERATORS_FOR_FLAGS(Flags)`

**作用与语义：**

Q_DECLARE_OPERATORS_FOR_FLAGS()宏声明全局位算子函数 `operator|()`、`operator&()`、`operator^()`、`operator~()`及其赋值形式：&=、|=、^=。对于`Flags`，其类型为`QFlags`<T>。
详情请参见`QFlags`文档。

### `Int`

**作用与语义：**

Typedef 用于存储和隐式转换的整数类型。根据枚举底层类型是有符号还是无符号，以及自 Qt 6.9 起的枚举大小，可以选择 `qintXX` 或 `quintXX`。通常，枚举大小为 `qint32`（`int`）或 `quint32`（`unsigned`）。

### `enum_type`

**作用与语义：**

Enum 模板类型用 Typedef。

### `(since 6.2) bool operator!=(QFlags<T> lhs, Enum rhs)`

**作用与语义：**

比较`lhs`和`rhs`的不等式;如果两个参数不完全代表相同的值（位掩码），则视为不同。

### `(since 6.2) bool operator!=(QFlags<T> lhs, QFlags<T> rhs)`

**作用与语义：**

比较`lhs`和`rhs`的不等式;如果两个参数不完全代表相同的值（位掩码），则视为不同。

### `(since 6.2) bool operator==(QFlags<T> lhs, Enum rhs)`

**作用与语义：**

比较`lhs`和`rhs`以求相等;如果两个参数代表完全相同的值（位掩码），则视为相等。

### `(since 6.2) bool operator==(QFlags<T> lhs, QFlags<T> rhs)`

**作用与语义：**

比较`lhs`和`rhs`以求相等;如果两个参数代表完全相同的值（位掩码），则视为相等。

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

`QFlags` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
