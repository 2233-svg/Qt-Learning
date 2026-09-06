# QRandomGenerator

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“RandomGenerator”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QRandomGenerator` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QRandomGenerator>`
- 继承自：未在类页中列出
- 直接派生类：QRandomGenerator64

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

- `result_type`

### 公有函数

- `QRandomGenerator(quint32 seedValue = 1)`
- `QRandomGenerator(const quint32 (&)[N] seedBuffer)`
- `QRandomGenerator(std::seed_seq &sseq)`
- `QRandomGenerator(const quint32 *begin, const quint32 *end)`
- `QRandomGenerator(const quint32 *seedBuffer, qsizetype len)`
- `QRandomGenerator(const QRandomGenerator &other)`
- `double bounded(double highest)`
- `int bounded(int highest)`
- `qint64 bounded(qint64 highest)`
- `quint32 bounded(quint32 highest)`
- `quint64 bounded(quint64 highest)`
- `int bounded(int lowest, int highest)`
- `qint64 bounded(int lowest, qint64 highest)`
- `qint64 bounded(qint64 lowest, int highest)`
- `qint64 bounded(qint64 lowest, qint64 highest)`
- `quint32 bounded(quint32 lowest, quint32 highest)`
- `quint64 bounded(quint64 lowest, quint64 highest)`
- `quint64 bounded(quint64 lowest, unsigned int highest)`
- `quint64 bounded(unsigned int lowest, quint64 highest)`
- `void discard(unsigned long long z)`
- `void fillRange(UInt (&)[N] buffer)`
- `void fillRange(UInt *buffer, qsizetype count)`
- `quint64 generate64()`
- `quint32 generate()`
- `void generate(ForwardIterator begin, ForwardIterator end)`
- `double generateDouble()`
- `void seed(quint32 seed = 1)`
- `void seed(std::seed_seq &seed)`
- `QRandomGenerator::result_type operator()()`

### 静态公有成员

- `QRandomGenerator * global()`
- `QRandomGenerator::result_type max()`
- `QRandomGenerator::result_type min()`
- `QRandomGenerator securelySeeded()`
- `QRandomGenerator * system()`

### 相关非成员函数

- `bool operator!=(const QRandomGenerator &rng1, const QRandomGenerator &rng2)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QRandomGenerator::result_type`

**作用与语义：**

一个类型def到`operator()`返回的类型。也就是quint32。

### `QRandomGenerator::QRandomGenerator(quint32 seedValue = 1)`

**作用与语义：**

将该QRandomGenerator对象初始化为`seedValue`作为种子。两个用相同种子值构建或重新种子的对象会产生相同的数字序列。

### `template <qsizetype N> QRandomGenerator::QRandomGenerator(const quint32 (&)[N] seedBuffer)`

**作用与语义：**

用数组`seedBuffer`中的值作为种子初始化该QRandomGenerator对象。两个用相同种子值构建或重新种子的对象会产生相同的数字序列。

### `[noexcept] QRandomGenerator::QRandomGenerator(std::seed_seq &sseq)`

**作用与语义：**

初始化该 QRandomGenerator 对象时，种子序列为 `sseq` 作为种子。两个用相同种子值构建或重新种种的对象会产生相同的数字序列。

### `QRandomGenerator::QRandomGenerator(const quint32 *begin, const quint32 *end)`

**作用与语义：**

初始化该QRandomGenerator对象时，使用`begin`到`end`之间的值作为种子。两个用相同种子值构建或重新种种的对象会产生相同的数字序列。
该构造函数等价于：

**官方示例：**

```cpp
     std::seed_seq sseq(begin, end);
     QRandomGenerator generator(sseq);
```

### `QRandomGenerator::QRandomGenerator(const quint32 *seedBuffer, qsizetype len)`

**作用与语义：**

用数组`seedBuffer`中找到的`len`值初始化该QRandomGenerator对象作为种子。两个用相同种子值构建或重新种种的对象会产生相同的数字序列。
该构造函数等价于：

**官方示例：**

```cpp
     std::seed_seq sseq(seedBuffer, seedBuffer + len);
     QRandomGenerator generator(sseq);
```

### `QRandomGenerator::QRandomGenerator(const QRandomGenerator &other)`

**作用与语义：**

在`other`对象中创建生成元状态的副本。如果`other` `QRandomGenerator::system()`或其副本，该对象也会读取操作系统的随机生成设施。在这种情况下，两个对象生成的序列将不同。
在其他所有情况下，新的QRandomGenerator对象将从确定性序列中与`other`对象相同的位置开始。从此，两个对象将生成相同的序列。
因此，不建议创建`QRandomGenerator::global()`的副本。如果需要一个排他确定性生成器，可以考虑用`securelySeeded()`获得一个与`QRandomGenerator::global()`无关系的新对象。

### `double QRandomGenerator::bounded(double highest)`

**作用与语义：**

生成一个介于0（含）和`highest`（独占）之间的随机双重。该函数等价于和，实现为：
如果`highest`参数为负，结果也会为负;如果是无限或NaN，结果也会是无限或NaN（即非随机）。

**官方示例：**

```cpp
     return generateDouble() * highest;
```

### `int QRandomGenerator::bounded(int highest)`

**作用与语义：**

生成一个随机的32位量，范围介于0（含）到`highest`（独占）。`highest`必须是正的。
注意，该函数无法获得整数 32 位范围内的值。相反，使用 `generate()` 并 cast 为整数。

### `qint64 QRandomGenerator::bounded(qint64 highest)`

**作用与语义：**

生成一个介于0（含）和`highest`（排斥）之间的随机64位量。`highest`必须是正的。
注意，该函数无法获得`qint64` 64位范围内的值。相反，使用`generate64()`并cast为qint64，或者使用该函数的无符号版本。
注意：该函数以循环形式实现，取决于获得的随机值。长期运行平均应接近2次，但如果随机生成器有缺陷，该函数执行时间可能明显延长。

### `quint32 QRandomGenerator::bounded(quint32 highest)`

**作用与语义：**

生成一个介于0（含）和`highest`（排他）之间的随机32位量。同样的结果也可以通过使用参数为0和`highest - 1`的`std::uniform_int_distribution`获得。该类也可以用于获得大于32位的量;对于64位，也可以使用64位有界()重载。
例如，要得到0到255（含）之间的值，可以写成：
当然，也可以通过只将`generate()`结果掩蔽到较低的8位来实现同样的效果。无论哪种解法，效率都一样。
注意，该函数无法获得quint32完整32位范围的值。相反，使用`generate()`。

**官方示例：**

```cpp
     quint32 v = QRandomGenerator::global()->bounded(256);
```

### `quint64 QRandomGenerator::bounded(quint64 highest)`

**作用与语义：**

生成一个介于0（含）和`highest`（排他）之间的随机64位量。同样的结果也可以通过使用参数为0和`highest - 1`的`std::uniform_int_distribution<quint64>`获得。
注意，该函数无法获得`quint64` 64位范围内的值。相反，请使用`generate64()`。
注意：该函数以循环形式实现，取决于获得的随机值。长期运行平均应接近2次，但如果随机生成器有缺陷，该函数执行时间可能明显延长。

### `int QRandomGenerator::bounded(int lowest, int highest)`

**作用与语义：**

生成一个随机的32位量，介于`lowest`（含）和`highest`（独占）之间，这两个数值都可能是负数，但`highest`必须大于`lowest`。
注意，该函数无法获得整数值的完整32位范围。相反，使用 `generate()` 并转换为整数。

### `quint64 QRandomGenerator::bounded(quint64 lowest, unsigned int highest)`

**作用与语义：**

当参数类型不完全匹配时，该函数的存在是为了帮助超载解析。它们会将较小的类型提升为较大类型，并调用正确的超载。

### `qint64 QRandomGenerator::bounded(qint64 lowest, qint64 highest)`

**作用与语义：**

当参数类型不完全匹配时，该函数的存在是为了帮助超载解析。它们会将较小的类型提升为较大类型，并调用正确的超载。

### `quint32 QRandomGenerator::bounded(quint32 lowest, quint32 highest)`

**作用与语义：**

当参数类型不完全匹配时，该函数的存在是为了帮助超载解析。它们会将较小的类型提升为较大类型，并调用正确的超载。

### `quint64 QRandomGenerator::bounded(quint64 lowest, quint64 highest)`

**作用与语义：**

当参数类型不完全匹配时，该函数的存在是为了帮助超载解析。它们会将较小的类型提升为较大类型，并调用正确的超载。

### `void QRandomGenerator::discard(unsigned long long z)`

**作用与语义：**

丢弃序列中的接下来的`z`条。该方法等同于调用`generate()` `z`次并丢弃结果，具体如下：

**官方示例：**

```cpp
     while (z--)
         generator.generate();
```

### `template < typename UInt, size_t N, QRandomGenerator::IfValidUInt<UInt> = true > void QRandomGenerator::fillRange(UInt (&)[N] buffer)`

**作用与语义：**

生成`N` 32位或64位的数量（取决于类型`UInt`），并将其存储在`buffer`数组中。这是一次获得多个数量的最高效方法，因为它减少了随机数生成器源的调用次数。
例如，为了生成两个32位量，可以写成：
也可以调用一次`generate64()`，然后将64位值的两半拆分。

**官方示例：**

```cpp
     quint32 array[2];
     QRandomGenerator::global()->fillRange(array);
```

### `template <typename UInt, QRandomGenerator::IfValidUInt<UInt> = true> void QRandomGenerator::fillRange(UInt *buffer, qsizetype count)`

**作用与语义：**

生成`count` 32位或64位的数量（取决于类型`UInt`），并将其存储在指向`buffer`的缓冲区中。这是一次获得多个数量的最高效方法，因为它减少了随机数生成器源的调用次数。
例如，为了用随机值填充一个包含16个条目的列表，可以写成：

**官方示例：**

```cpp
     QList<quint32> list;
     list.resize(16);
     QRandomGenerator::global()->fillRange(list.data(), list.size());
```

### `quint64 QRandomGenerator::generate64()`

**作用与语义：**

生成一个64位随机量并返回。

### `quint32 QRandomGenerator::generate()`

**作用与语义：**

生成一个32位随机量并返回。

### `template <typename ForwardIterator> void QRandomGenerator::generate(ForwardIterator begin, ForwardIterator end)`

**作用与语义：**

生成32位量，并存储在`begin`到`end`之间的范围内。该函数等价于（并实现为）：
该函数符合函数`std::seed_seq::generate`的要求，该函数要求无符号的32位整数值。
注意，如果[开始，结束]范围指的是每个元素可存储超过32位的区域，元素初始化时仍仅包含32位数据。其他位为零。为了填满64位量，可以写成：
如果区间指的是连续内存（如数组或`QList`数据），也可以使用`fillRange()`函数。

**官方示例：**

```cpp
     std::generate(begin, end, [this]() { return generate(); });
```

### `double QRandomGenerator::generateDouble()`

**作用与语义：**

生成一个典型值域[0， 1]的随机qreal（即包含零且排斥1）。
该函数等价于：
同样的方法也可以通过参数为0和1的`std::uniform_real_distribution`得到。

**官方示例：**

```cpp
     QRandomGenerator64 rd;
     return std::generate_canonical<qreal, std::numeric_limits<qreal>::digits>(rd);
```

### `[static] QRandomGenerator *QRandomGenerator::global()`

**作用与语义：**

返回一个指向通过`securelySeeded()`做种的共享`QRandomGenerator`的指针。该函数应用于创建随机数据，而无需为特定用途创建高昂的安全种子`QRandomGenerator`或存储较大的`QRandomGenerator`对象。
例如，以下方法生成随机的RGB颜色：
对该对象的访问是线程安全的，因此可以在任何无锁线程中使用。该对象也可以被复制，复制产生的序列将与共享对象生成的序列相同。但请注意，如果有其他线程访问全局对象，这些线程可能会在不可预测的间隔中获得样本。
注意：该功能是线程安全的。

**官方示例：**

```cpp
     return QColor::fromRgb(QRandomGenerator::global()->generate());
```

### `[static constexpr] QRandomGenerator::result_type QRandomGenerator::max()`

**作用与语义：**

返回`QRandomGenerator`可能产生的最大值。也就是说，`std::numeric_limits<result_type>::max()`。

### `[static constexpr] QRandomGenerator::result_type QRandomGenerator::min()`

**作用与语义：**

返回`QRandomGenerator`可能产生的最小值。也就是0。

### `[static] QRandomGenerator QRandomGenerator::securelySeeded()`

**作用与语义：**

返回一个已安全种种`QRandomGenerator::system()`的新`QRandomGenerator`对象。该函数将获得`QRandomGenerator`所用算法的理想种子大小，因此是创建新`QRandomGenerator`对象并保留一段时间的推荐方法。
鉴于安全种子确定性引擎所需的数据量，该函数成本较高，不应用于短期使用`QRandomGenerator`（用它生成少于2600字节的随机数据实际上是资源浪费）。如果使用方式不需要那么多数据，考虑使用`QRandomGenerator::global()`而不是存储`QRandomGenerator`对象。

### `void QRandomGenerator::seed(quint32 seed = 1)`

**作用与语义：**

用值 `seed` 作为种子重新种子。

### `[noexcept] void QRandomGenerator::seed(std::seed_seq &seed)`

**作用与语义：**

用种子序列`seed`作为种子重新种种该对象。

### `[static] QRandomGenerator *QRandomGenerator::system()`

**作用与语义：**

返回指向共享`QRandomGenerator`的指针，该始终使用操作系统提供的设施生成随机数。系统设施在至少以下操作系统上被认为是加密学安全的：苹果操作系统（Darwin）、BSD、Linux、Windows。其他操作系统也可能如此。
它们也可能由真正的硬件随机数生成器支持。因此，该函数返回的`QRandomGenerator`不应用于批量数据生成。相反，应用它从头部中播种`QRandomGenerator`或随机引擎<random>。
该函数返回的对象是线程安全的，可以在任何没有锁的线程中使用。它也可以被复制，生成的`QRandomGenerator`也会访问操作系统的设施，但它们不会生成相同的序列。
注意：该功能是线程安全的。

### `QRandomGenerator::result_type QRandomGenerator::operator()()`

**作用与语义：**

生成一个32位随机量并返回。

### `bool operator!=(const QRandomGenerator &rng1, const QRandomGenerator &rng2)`

**作用与语义：**

如果两个引擎`rng1`和`rng2`处于不同状态，或者其中一个引擎读取操作系统功能而另一个没有，返回`true`，否则`false`。

### `result_type`

**作用与语义：**

一个类型def到`operator()`返回的类型。也就是quint32。

### `qint64 bounded(int lowest, qint64 highest)`

**作用与语义：**

生成一个介于`lowest`（含）和`highest`（独占）之间的随机64位量，这两个值都可以为负，但`highest`必须大于`lowest`。
注意，该函数无法获得`qint64` 64位范围内的值。相反，使用 `generate64()` 并转换为 qint64。
注意：该函数以循环形式实现，取决于获得的随机值。长期运行平均应接近2次，但如果随机生成器有缺陷，该函数执行时间可能明显延长。

### `qint64 bounded(qint64 lowest, int highest)`

**作用与语义：**

生成一个随机的32位量，范围介于`lowest`（含）和`highest`（独占）。`highest`参数必须大于`lowest`。
同样的结果也可以通过使用参数为`lowest`和`\a highest - 1`的`std::uniform_int_distribution`获得。该类还可以获得大于32位的数量。
例如，要得到介于1000（含）和2000（不包括）之间的值，可以写成：
注意，该函数无法获得quint32完整32位范围的值。相反，使用`generate()` 49。

**官方示例：**

```cpp
     quint32 v = QRandomGenerator::global()->bounded(1000, 2000);
```

### `quint64 bounded(unsigned int lowest, quint64 highest)`

**作用与语义：**

生成一个介于`lowest`（含）和`highest`（排他）之间的随机64位量。`highest`参数必须大于`lowest`。
同样的结果也可以通过使用参数为`lowest`和`\a highest - 1`的`std::uniform_int_distribution<quint64>`得到。
注意，该函数无法获得`quint64` 64位范围内的值。相反，使用`generate64()`。
注意：该函数以循环形式实现，取决于获得的随机值。长期运行平均应接近2次，但如果随机生成器有缺陷，该函数执行时间可能明显延长。

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

`QRandomGenerator` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
