# QCollator

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“Collator”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QCollator` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QCollator>`
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

- `QCollator()`
- `QCollator(const QLocale &locale)`
- `QCollator(const QCollator &other)`
- `QCollator(QCollator &&other)`
- `~QCollator()`
- `Qt::CaseSensitivity caseSensitivity() const`
- `int compare(QStringView s1, QStringView s2) const`
- `int compare(const QString &s1, const QString &s2) const`
- `int compare(const QChar *s1, qsizetype len1, const QChar *s2, qsizetype len2) const`
- `bool ignorePunctuation() const`
- `QLocale locale() const`
- `bool numericMode() const`
- `void setCaseSensitivity(Qt::CaseSensitivity cs)`
- `void setIgnorePunctuation(bool on)`
- `void setLocale(const QLocale &locale)`
- `void setNumericMode(bool on)`
- `QCollatorSortKey sortKey(const QString &string) const`
- `void swap(QCollator &other)`
- `bool operator()(QStringView s1, QStringView s2) const`
- `bool operator()(const QString &s1, const QString &s2) const`
- `QCollator & operator=(QCollator &&other)`
- `QCollator & operator=(const QCollator &other)`

### 静态公有成员

- `(since 6.3) int defaultCompare(QStringView s1, QStringView s2)`
- `(since 6.3) QCollatorSortKey defaultSortKey(QStringView key)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QCollator::QCollator()`

**作用与语义：**

利用默认位置的整合位置构建QCollator。
系统局部作为默认局部时，可能拥有自身以外的整合局部（例如在 Unix 上，如果 LC_COLLATE 在环境中与 LANG 不同）。其他所有局部区域都是独立的整合局部。

### `[explicit] QCollator::QCollator(const QLocale &locale)`

**作用与语义：**

利用给定`locale`构建QCollator。

### `QCollator::QCollator(const QCollator &other)`

**作用与语义：**

创建`other`副本。

### `[noexcept] QCollator::QCollator(QCollator &&other)`

**作用与语义：**

移动构造器。从`other`移动到这个整理器。
注意：被移出对象 `other` 处于部分成形状态，唯一有效的操作是销毁和赋值。

### `[noexcept] QCollator::~QCollator()`

**作用与语义：**

毁了这个整理器。

### `Qt::CaseSensitivity QCollator::caseSensitivity() const`

**作用与语义：**

整理者的退货敏感性。
在设置之前，默认为大小写区分。
注意：在C区区，区分大小写时，所有小写字母都排在所有大写字母之后，而大多数地区则将每个小写字母排序在大写字母之前或紧接其后。因此，“Zap”在C区排序在“ape”之前，但在大多数其他地区排在“ape”之后。

### `int QCollator::compare(QStringView s1, QStringView s2) const`

**作用与语义：**

比较`s1`和`s2`。
如果`s1`小于`s2`，返回负整数;大于`s2`则返回正整数;相等则返回零。

### `int QCollator::compare(const QString &s1, const QString &s2) const`

**作用与语义：**

比较`s1`和`s2`。
如果`s1`小于`s2`，返回负整数;大于`s2`则返回正整数;相等则返回零。

### `int QCollator::compare(const QChar *s1, qsizetype len1, const QChar *s2, qsizetype len2) const`

**作用与语义：**

比较`s1`与`s2`。`len1`和`len2`指定`s1`和`s2`指向的`QChar`数组的长度。
如果`s1`小于`s2`，则返回负整数;如果大于`s2`，则返回正整数;相等时返回零。
注意：在6.4之前的Qt版本中，长度参数类型为`int`，而非`qsizetype`。

### `[static, since 6.3] int QCollator::defaultCompare(QStringView s1, QStringView s2)`

**作用与语义：**

比较字符串 `s1` 和 `s2`，返回它们的排序顺序。该函数执行与默认构造`QCollator`对象 `compare()` 相同的操作。

### `[static, since 6.3] QCollatorSortKey QCollator::defaultSortKey(QStringView key)`

**作用与语义：**

返回字符串`key`的排序键。该函数执行与默认构造`QCollator`对象的 `sortKey()` 操作相同。

### `bool QCollator::ignorePunctuation() const`

**作用与语义：**

返回整理时是否忽略标点符号和符号。
`true`时，字符串的比较就像去掉了所有标点和符号一样。

### `QLocale QCollator::locale() const`

**作用与语义：**

返回整理器所在的位置。
除非系统向构造器提供或调用`setLocale()`，否则系统默认的排序位置被使用。

### `bool QCollator::numericMode() const`

**作用与语义：**

如果启用数值排序，返回`true`，否则`false`。
当`true`时，数字被识别为数字并按算术顺序排序;例如，100排序在99之后。当`false`时，数字按词汇顺序排序，使得100排序在99之前（因为1在9之前）。默认情况下，该选项被禁用。

### `void QCollator::setCaseSensitivity(Qt::CaseSensitivity cs)`

**作用与语义：**

将校对者的大小写敏感性设置为`cs`。

### `void QCollator::setIgnorePunctuation(bool on)`

**作用与语义：**

如果标点符号和符号`on` `true`，忽略;如果`false`则注意它们。

### `void QCollator::setLocale(const QLocale &locale)`

**作用与语义：**

将收集器的位置设置为`locale`。

### `void QCollator::setNumericMode(bool on)`

**作用与语义：**

当`on` `true`时，启用数值排序模式。

### `QCollatorSortKey QCollator::sortKey(const QString &string) const`

**作用与语义：**

返回一个`string`的sortKey。
创建排序键通常比直接使用`compare()`方法慢一些。但如果字符串被反复比较（例如排序整个字符串列表时），通常为每个字符串创建排序键然后用键排序会更快。
注意：Darwin的C（又称POSIX）地点不支持。

### `[noexcept] void QCollator::swap(QCollator &other)`

**作用与语义：**

把这个整理器和`other`交换。这个操作非常快，从不失败。

### `bool QCollator::operator()(QStringView s1, QStringView s2) const`

**作用与语义：**

`QCollator`可以用作排序算法的比较函数。如果`s1`先于`s2`排序，则返回`true`，否则返回`false`。

### `bool QCollator::operator()(const QString &s1, const QString &s2) const`

**作用与语义：**

`QCollator`可以用作排序算法的比较函数。如果`s1`先于`s2`排序，则返回`true`，否则返回`false`。

### `[noexcept] QCollator &QCollator::operator=(QCollator &&other)`

**作用与语义：**

Move-assign `other`到该`QCollator`实例。
注意：移出对象`other`处于部分成形状态，唯一有效的操作是销毁和赋予新值。

### `QCollator &QCollator::operator=(const QCollator &other)`

**作用与语义：**

给这个整理器分配`other`。

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

`QCollator` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
