# qfloat16

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“qfloat16”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`qfloat16` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QFloat16>`
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

- `(since 6.1) qfloat16(Qt::Initialization)`
- `bool isNormal() const`

### 相关非成员函数

- `(since 6.11) qfloat16 copysign(qfloat16 x, qfloat16 sign)`
- `void qFloatFromFloat16(float *out, const qfloat16 *in, qsizetype len)`
- `void qFloatToFloat16(qfloat16 *out, const float *in, qsizetype len)`
- `int qFpClassify(qfloat16 val)`
- `bool qFuzzyCompare(qfloat16 p1, qfloat16 p2)`
- `(since 6.5.3) size_t qHash(qfloat16 key, size_t seed = 0)`
- `bool qIsFinite(qfloat16 f)`
- `bool qIsInf(qfloat16 f)`
- `bool qIsNaN(qfloat16 f)`
- `qint64 qRound64(qfloat16 value)`
- `int qRound(qfloat16 value)`
- `(since 6.11) bool signbit(qfloat16 x)`
- `QDataStream & operator<<(QDataStream &ds, qfloat16 f)`
- `QDataStream & operator>>(QDataStream &ds, qfloat16 &f)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[explicit noexcept, since 6.1] qfloat16::qfloat16(Qt::Initialization)`

**作用与语义：**

构造一个不初始化值的qfloat16。

### `[constexpr noexcept] bool qfloat16::isNormal() const`

**作用与语义：**

如果该`qfloat16`值是有限且为正规形，则返回`true`。

### `[noexcept, since 6.11] qfloat16 copysign(qfloat16 x, qfloat16 sign)`

**作用与语义：**

返回符号为 `sign` 的 qfloat16，其余值取自 `x`。作为 qfloat16 的 std：：copysign() 的等价物。

### `[noexcept] void qFloatFromFloat16(float *out, const qfloat16 *in, qsizetype len)`

**作用与语义：**

将`in`的qfloat16 `len`转换为float并存储在`out`中。`in`和`out`都必须有`len`分配的条目。
该函数比逐个转换值更快，并且可以在x86和x86-64硬件上进行运行时F16C检测。

### `[noexcept] void qFloatToFloat16(qfloat16 *out, const float *in, qsizetype len)`

**作用与语义：**

将浮点数`len`从`in`转换为qfloat16并存储在`out`中。`in`和`out`都必须有`len`分配的条目。
该函数比逐个转换值更快，并且可以在x86和x86-64硬件上进行运行时F16C检测。

### `[noexcept] int qFpClassify(qfloat16 val)`

**作用与语义：**

返回浮点类 `val`。

### `[noexcept] bool qFuzzyCompare(qfloat16 p1, qfloat16 p2)`

**作用与语义：**

比较浮点值`p1`和`p2`，如果它们被视为相等，则返回`true`，否则`false`。
两个数字以相对方式比较，数字越小，精确度越强。

### `[noexcept, since 6.5.3] size_t qHash(qfloat16 key, size_t seed = 0)`

**作用与语义：**

返回`key`的哈希值，使用`seed`来做种计算。
注意：在 6.5 之前的 Qt 版本中，该操作由 qHash（float）重载提供。在 Qt 6.5.0 到 6.5.2 版本中，该功能以多种方式被破坏。在 Qt 6.5.3 和 6.6 版本中，这种重载恢复了 Qt 6.4 的行为。

### `[noexcept] bool qIsFinite(qfloat16 f)`

**作用与语义：**

如果`qfloat16` `f`是有限数，则返回为真。

### `[noexcept] bool qIsInf(qfloat16 f)`

**作用与语义：**

如果`qfloat16` `f`等价于无穷大，则返回为真。

### `[noexcept] bool qIsNaN(qfloat16 f)`

**作用与语义：**

如果`qfloat16` `f`不是数字（NaN），则返回为真。

### `qint64 qRound64(qfloat16 value)`

**作用与语义：**

四舍五入`value`到最近的64位整数。

### `int qRound(qfloat16 value)`

**作用与语义：**

四舍五入`value`到最近的整数。

### `[noexcept, since 6.11] bool signbit(qfloat16 x)`

**作用与语义：**

如果qfloat16 `x`为负，则返回真;否则为假。注意，该函数对负零、负无穷远和负NaN值返回真。

### `QDataStream &operator<<(QDataStream &ds, qfloat16 f)`

**作用与语义：**

使用标准IEEE 754格式，向流`ds`写入浮点数`f`。返回流的引用。
注意：在 6.3 之前的 Qt 版本中，这是 `QDataStream` 上的成员函数。

### `QDataStream &operator>>(QDataStream &ds, qfloat16 &f)`

**作用与语义：**

使用标准IEEE 754格式，将流`ds`中的浮点数读取到`f`。返回流的引用。
注意：在6.3之前的Qt版本中，这是`QDataStream`的成员函数。

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

`qfloat16` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
