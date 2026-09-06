# QKeyCombination

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“键Combination”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QKeyCombination` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QKeyCombination>`
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

- `QKeyCombination(Qt::Key key = Qt::Key_unknown)`
- `QKeyCombination(Qt::KeyboardModifiers modifiers, Qt::Key key = Qt::Key_unknown)`
- `QKeyCombination(Qt::Modifiers modifiers, Qt::Key key = Qt::Key_unknown)`
- `Qt::Key key() const`
- `Qt::KeyboardModifiers keyboardModifiers() const`
- `int toCombined() const`

### 静态公有成员

- `QKeyCombination fromCombined(int combined)`

### 相关非成员函数

- `size_t qHash(QKeyCombination key, size_t seed = 0)`
- `bool operator!=(const QKeyCombination &lhs, const QKeyCombination &rhs)`
- `QDataStream & operator<<(QDataStream &out, QKeyCombination combination)`
- `QDebug operator<<(QDebug debug, QKeyCombination combination)`
- `bool operator==(const QKeyCombination &lhs, const QKeyCombination &rhs)`
- `QDataStream & operator>>(QDataStream &in, QKeyCombination &combination)`
- `QKeyCombination operator|(Qt::Key key, Qt::KeyboardModifier modifier)`
- `QKeyCombination operator|(Qt::Key key, Qt::KeyboardModifiers modifiers)`
- `QKeyCombination operator|(Qt::Key key, Qt::Modifier modifier)`
- `QKeyCombination operator|(Qt::Key key, Qt::Modifiers modifiers)`
- `QKeyCombination operator|(Qt::KeyboardModifier modifier, Qt::Key key)`
- `QKeyCombination operator|(Qt::KeyboardModifiers modifiers, Qt::Key key)`
- `QKeyCombination operator|(Qt::Modifier modifier, Qt::Key key)`
- `QKeyCombination operator|(Qt::Modifiers modifiers, Qt::Key key)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[constexpr noexcept] QKeyCombination::QKeyCombination(Qt::Key key = Qt::Key_unknown)`

**作用与语义：**

构建一个表示密钥`key`且无修饰符的QKeyCombination对象。

### `[explicit constexpr noexcept] QKeyCombination::QKeyCombination(Qt::KeyboardModifiers modifiers, Qt::Key key = Qt::Key_unknown)`

**作用与语义：**

构造一个QKeyCombination对象，表示`key`与修饰符`modifiers`的组合。

### `[explicit constexpr noexcept] QKeyCombination::QKeyCombination(Qt::Modifiers modifiers, Qt::Key key = Qt::Key_unknown)`

**作用与语义：**

构造一个QKeyCombination对象，表示`key`与修饰符`modifiers`的组合。

### `[static constexpr] QKeyCombination QKeyCombination::fromCombined(int combined)`

**作用与语义：**

通过从`combined`中提取密钥和修饰符来构造`QKeyCombination`对象，该必须是类型`Qt::Key`与类型`Qt::KeyboardModifiers`之间的位或结果。`toCombined()`可以用来生成`combined`的有效值。

### `[constexpr noexcept] Qt::Key QKeyCombination::key() const`

**作用与语义：**

返回由该`QKeyCombination`对象表示的密钥。

### `[constexpr noexcept] Qt::KeyboardModifiers QKeyCombination::keyboardModifiers() const`

**作用与语义：**

返回由该`QKeyCombination`对象表示的键盘修改器。

### `[constexpr noexcept] int QKeyCombination::toCombined() const`

**作用与语义：**

返回一个整数值，通过在`key()`和`keyboardModifiers()`的值之间应用逐位或值得到的。通过使用该`fromCombined()`可以从返回的整数值创建`QKeyCombination`对象。

### `[constexpr noexcept] size_t qHash(QKeyCombination key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种。

### `[constexpr noexcept] bool operator!=(const QKeyCombination &lhs, const QKeyCombination &rhs)`

**作用与语义：**

如果 `lhs` 和 `rhs` 的键和修饰符组合不同，则返回 `true`，否则返回 `false`。

### `QDataStream &operator<<(QDataStream &out, QKeyCombination combination)`

**作用与语义：**

将组合 `combination` 写入流 `out`。返回 `out`。

### `QDebug operator<<(QDebug debug, QKeyCombination combination)`

**作用与语义：**

将组合 `combination` 写入调试对象 `debug` 以用于调试目的。

### `[constexpr noexcept] bool operator==(const QKeyCombination &lhs, const QKeyCombination &rhs)`

**作用与语义：**

如果`lhs`和`rhs`键和修饰符组合相同，返回`true`，否则`false`。

### `QDataStream &operator>>(QDataStream &in, QKeyCombination &combination)`

**作用与语义：**

读取流`in`的组合 `combination`。返回`in`。

### `[constexpr noexcept] QKeyCombination operator|(Qt::Key key, Qt::KeyboardModifier modifier)`

**作用与语义：**

返回一个`QKeyCombination`对象，表示`key`与修饰符`modifier`的组合。

### `[constexpr noexcept] QKeyCombination operator|(Qt::Key key, Qt::KeyboardModifiers modifiers)`

**作用与语义：**

返回一个`QKeyCombination`对象，表示`key`与修饰符`modifier`的组合。

### `QKeyCombination operator|(Qt::Key key, Qt::Modifier modifier)`

**作用与语义：**

返回一个`QKeyCombination`对象，表示`key`与修饰符`modifier`的组合。

### `QKeyCombination operator|(Qt::Key key, Qt::Modifiers modifiers)`

**作用与语义：**

返回一个`QKeyCombination`对象，表示`key`与修饰符`modifier`的组合。

### `QKeyCombination operator|(Qt::KeyboardModifier modifier, Qt::Key key)`

**作用与语义：**

返回一个`QKeyCombination`对象，表示`key`与修饰符`modifiers`的组合。

### `QKeyCombination operator|(Qt::KeyboardModifiers modifiers, Qt::Key key)`

**作用与语义：**

返回一个`QKeyCombination`对象，表示`key`与修饰符`modifiers`的组合。

### `QKeyCombination operator|(Qt::Modifier modifier, Qt::Key key)`

**作用与语义：**

返回一个`QKeyCombination`对象，表示`key`与修饰符`modifiers`的组合。

### `QKeyCombination operator|(Qt::Modifiers modifiers, Qt::Key key)`

**作用与语义：**

返回一个`QKeyCombination`对象，表示`key`与修饰符`modifiers`的组合。

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

`QKeyCombination` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
