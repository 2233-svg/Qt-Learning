# QTextBoundaryFinder

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“文本BoundaryFinder”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QTextBoundaryFinder` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QTextBoundaryFinder>`
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

### 公有类型

- `enum BoundaryReason { NotAtBoundary, BreakOpportunity, StartOfItem, EndOfItem, MandatoryBreak, SoftHyphen }`
- `flags BoundaryReasons`
- `enum BoundaryType { Grapheme, Word, Line, Sentence }`

### 公有函数

- `QTextBoundaryFinder()`
- `QTextBoundaryFinder(QTextBoundaryFinder::BoundaryType type, const QString &string)`
- `(since 6.0) QTextBoundaryFinder(QTextBoundaryFinder::BoundaryType type, QStringView string, unsigned char *buffer = nullptr, qsizetype bufferSize = 0)`
- `QTextBoundaryFinder(QTextBoundaryFinder::BoundaryType type, const QChar *chars, qsizetype length, unsigned char *buffer = nullptr, qsizetype bufferSize = 0)`
- `QTextBoundaryFinder(const QTextBoundaryFinder &other)`
- `(since 6.11) QTextBoundaryFinder(QTextBoundaryFinder &&other)`
- `~QTextBoundaryFinder()`
- `QTextBoundaryFinder::BoundaryReasons boundaryReasons() const`
- `bool isAtBoundary() const`
- `bool isValid() const`
- `qsizetype position() const`
- `void setPosition(qsizetype position)`
- `QString string() const`
- `(since 6.11) void swap(QTextBoundaryFinder &other)`
- `void toEnd()`
- `qsizetype toNextBoundary()`
- `qsizetype toPreviousBoundary()`
- `void toStart()`
- `QTextBoundaryFinder::BoundaryType type() const`
- `(since 6.11) QTextBoundaryFinder & operator=(QTextBoundaryFinder &&other)`
- `QTextBoundaryFinder & operator=(const QTextBoundaryFinder &other)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QTextBoundaryFinder::BoundaryReasonflags QTextBoundaryFinder::BoundaryReasons`

**作用与语义：**

- `QTextBoundaryFinder::NotAtBoundary`: `0`; 边界查找器不在边界位置。
- `QTextBoundaryFinder::BreakOpportunity`: `0x1f`; 边界查找器位于换行机会位置。这样的换行机会也可能是一个项目边界（StartOfItem、EndOfItem或两者组合）、强制换行符或软连字符。
- `QTextBoundaryFinder::StartOfItem (since Qt 5.0)`: `0x20`; 边界查找器位于字形、单词、句子或行的开始位置。
- `QTextBoundaryFinder::EndOfItem (since Qt 5.0)`: `0x40`; 边界查找器位于字形、单词、句子或行的结束位置。
- `QTextBoundaryFinder::MandatoryBreak (since Qt 5.0)`: `0x80`; 边界查找器位于行尾（仅适用于行边界类型）。
- `QTextBoundaryFinder::SoftHyphen`: `0x100`; 边界查找器位于软连字符（仅适用于行边界类型）。
BoundaryReasons 类型是 QFlags<BoundaryReason> 的 typedef。它存储 BoundaryReason 值的或组合。

### `QTextBoundaryFinder::QTextBoundaryFinder()`

**作用与语义：**

构造一个无效的 QTextBoundaryFinder 对象。

### `QTextBoundaryFinder::QTextBoundaryFinder(QTextBoundaryFinder::BoundaryType type, const QString &string)`

**作用与语义：**

创建一个 QTextBoundaryFinder 对象，`type` 操作于 `string`。

### `[since 6.0] QTextBoundaryFinder::QTextBoundaryFinder(QTextBoundaryFinder::BoundaryType type, QStringView string, unsigned char *buffer = nullptr, qsizetype bufferSize = 0)`

**作用与语义：**

创建一个 QTextBoundaryFinder 对象，操作于 `string` `type`。
`buffer`是一个可选的工作缓冲区，大小为`bufferSize`你可以传递给QTextBoundaryFinder。如果缓冲区足够大以容纳所需的工作数据（bufferSize >= 长度1），它会使用它，而不是分配自己的缓冲区。
警告：QTextBoundaryFinder 不会创建 `string` 的副本。只要 QTextBoundaryFinder 对象仍然存在，程序员有责任确保数组被分配。同样适用于 `buffer`。

### `QTextBoundaryFinder::QTextBoundaryFinder(QTextBoundaryFinder::BoundaryType type, const QChar *chars, qsizetype length, unsigned char *buffer = nullptr, qsizetype bufferSize = 0)`

**作用与语义：**

与 QTextBoundaryFinder（类型、`QStringView`（字符、长度）、缓冲区、缓冲区大小）相同。

### `QTextBoundaryFinder::QTextBoundaryFinder(const QTextBoundaryFinder &other)`

**作用与语义：**

复制QTextBoundaryFinder对象，`other`。

### `[noexcept, since 6.11] QTextBoundaryFinder::QTextBoundaryFinder(QTextBoundaryFinder &&other)`

**作用与语义：**

从`other`中移动构建了一个新的QTextBoundaryFinder。
注意：被移出的对象他处于部分形成状态，唯一有效的操作是销毁和赋予新值。

### `[noexcept] QTextBoundaryFinder::~QTextBoundaryFinder()`

**作用与语义：**

摧毁`QTextBoundaryFinder`物体。

### `QTextBoundaryFinder::BoundaryReasons QTextBoundaryFinder::boundaryReasons() const`

**作用与语义：**

返回边界查找器选择当前位置作为边界的原因。

### `bool QTextBoundaryFinder::isAtBoundary() const`

**作用与语义：**

如果对象的`position()`当前处于有效文本边界，返回`true`。

### `bool QTextBoundaryFinder::isValid() const`

**作用与语义：**

如果文本边界查找器有效，返回`true`;否则返回`false`。默认的`QTextBoundaryFinder`无效。

### `qsizetype QTextBoundaryFinder::position() const`

**作用与语义：**

返回 `QTextBoundaryFinder` 的当前位置。
范围从 0（字符串开头）到字符串长度（包括长度）。

### `void QTextBoundaryFinder::setPosition(qsizetype position)`

**作用与语义：**

将`QTextBoundaryFinder`当前位置设置为`position`。
如果`position`越界，则只绑定于有效位置。在这种情况下，有效位置范围为0到字符串长度（含）。

### `QString QTextBoundaryFinder::string() const`

**作用与语义：**

返回`QTextBoundaryFinder`对象操作的字符串。

### `[noexcept, since 6.11] void QTextBoundaryFinder::swap(QTextBoundaryFinder &other)`

**作用与语义：**

将文本边界查找器与`other`交换。这个操作非常快，从未失败过。

### `void QTextBoundaryFinder::toEnd()`

**作用与语义：**

将寻器移动到弦的末端。这相当于`setPosition`（string.length()）。

### `qsizetype QTextBoundaryFinder::toNextBoundary()`

**作用与语义：**

将`QTextBoundaryFinder`移动到下一个边界位置并返回该位置。
如果没有下一个边界，则返回-1。

### `qsizetype QTextBoundaryFinder::toPreviousBoundary()`

**作用与语义：**

将`QTextBoundaryFinder`移动到上一个边界位置并返回该位置。
如果没有先前边界，则返回-1。

### `void QTextBoundaryFinder::toStart()`

**作用与语义：**

将寻标器移动到弦的起始位置。这等价于`setPosition`（0）。

### `QTextBoundaryFinder::BoundaryType QTextBoundaryFinder::type() const`

**作用与语义：**

返回`QTextBoundaryFinder`类型。

### `[noexcept, since 6.11] QTextBoundaryFinder &QTextBoundaryFinder::operator=(QTextBoundaryFinder &&other)`

**作用与语义：**

Move-assign `other`到该`QTextBoundaryFinder`实例。
注意：被移出的对象他处于部分形成状态，唯一有效的操作是销毁和赋予新值。

### `QTextBoundaryFinder &QTextBoundaryFinder::operator=(const QTextBoundaryFinder &other)`

**作用与语义：**

将对象 `other` 分配给另一个`QTextBoundaryFinder`对象。

### `enum BoundaryReason { NotAtBoundary, BreakOpportunity, StartOfItem, EndOfItem, MandatoryBreak, SoftHyphen }`

**作用与语义：**

- `QTextBoundaryFinder::NotAtBoundary`: `0`; 边界查找器不在边界位置。
- `QTextBoundaryFinder::BreakOpportunity`: `0x1f`; 边界查找器位于换行机会位置。这样的换行机会也可能是一个项目边界（StartOfItem、EndOfItem或两者组合）、强制换行符或软连字符。
- `QTextBoundaryFinder::StartOfItem (since Qt 5.0)`: `0x20`; 边界查找器位于字形、单词、句子或行的开始位置。
- `QTextBoundaryFinder::EndOfItem (since Qt 5.0)`: `0x40`; 边界查找器位于字形、单词、句子或行的结束位置。
- `QTextBoundaryFinder::MandatoryBreak (since Qt 5.0)`: `0x80`; 边界查找器位于行尾（仅适用于行边界类型）。
- `QTextBoundaryFinder::SoftHyphen`: `0x100`; 边界查找器位于软连字符（仅适用于行边界类型）。
BoundaryReasons 类型是 QFlags<BoundaryReason> 的 typedef。它存储 BoundaryReason 值的或组合。

### `flags BoundaryReasons`

**作用与语义：**

- `QTextBoundaryFinder::NotAtBoundary`: `0`; 边界查找器不在边界位置。
- `QTextBoundaryFinder::BreakOpportunity`: `0x1f`; 边界查找器位于换行机会位置。这样的换行机会也可能是一个项目边界（StartOfItem、EndOfItem或两者组合）、强制换行符或软连字符。
- `QTextBoundaryFinder::StartOfItem (since Qt 5.0)`: `0x20`; 边界查找器位于字形、单词、句子或行的开始位置。
- `QTextBoundaryFinder::EndOfItem (since Qt 5.0)`: `0x40`; 边界查找器位于字形、单词、句子或行的结束位置。
- `QTextBoundaryFinder::MandatoryBreak (since Qt 5.0)`: `0x80`; 边界查找器位于行尾（仅适用于行边界类型）。
- `QTextBoundaryFinder::SoftHyphen`: `0x100`; 边界查找器位于软连字符（仅适用于行边界类型）。
BoundaryReasons 类型是 QFlags<BoundaryReason> 的 typedef。它存储 BoundaryReason 值的或组合。

### `enum BoundaryType { Grapheme, Word, Line, Sentence }`

**作用与语义：**

- `QTextBoundaryFinder::Grapheme`: `0`; 查找最小边界的字形。它包括字母、标点符号、数字等。
- `QTextBoundaryFinder::Word`: `1`; 查找一个单词。
- `QTextBoundaryFinder::Line`: `3`; 查找将文本分为多行的可能位置。
- `QTextBoundaryFinder::Sentence`: `2`; 查找句子的边界。这些包括句号、问号等。

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

`QTextBoundaryFinder` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
