# QVersionNumber

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QVersionNumber` 是区域、版本或时区值类型，用于规范化表示、比较和转换。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QVersionNumber` 是 Qt 值类型与隐式共享机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类类型通常可以按值传递、复制和返回。许多 Qt 容器、字符串和图像采用隐式共享：复制时共享数据，发生写操作时才 detach。这样便于 API 传值，但获取原始指针或长期持有引用时必须考虑对象修改和生命周期。

**适用场景：** 先确认值的有效性和表示格式，再调用查询、转换或修改 API；处理文本时区分 Unicode 和字节编码，处理图像时确认 format，处理 URL/路径时使用 Qt 的解析 API 而不是手写字符串规则。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要把空值当成业务成功；不要保存临时对象的内部指针；不要把 QString 当二进制缓冲区；不要假定隐式共享让并发写入自动安全。

## 2. 依赖与对象关系

- 头文件：`#include <QVersionNumber>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它是值类型或不直接使用 QObject 对象模型，重点放在数据语义、拷贝/移动成本和参数有效性。

### 工作机制

这类类型通常可以按值传递、复制和返回。许多 Qt 容器、字符串和图像采用隐式共享：复制时共享数据，发生写操作时才 detach。这样便于 API 传值，但获取原始指针或长期持有引用时必须考虑对象修改和生命周期。

### 状态、生命周期和线程

**生命周期：** 值对象由作用域、容器或调用者管理，不使用 parent 和 deleteLater。跨线程传递副本通常比传递 QObject 安全，但共享数据在写入时仍可能发生复制，性能和内存峰值要结合数据规模判断。

**状态与结果：** 重点区分空值、无效值、默认值和已初始化值。例如空字符串、空 URL、null 图像和无效索引不一定表示同一件事；转换函数的失败结果要通过对应的状态查询确认。

**线程与事件循环：** 值类型本身通常可以复制后跨线程传递；不要把 data()/bits()/constData() 得到的指针当成跨线程长期有效的所有权。大对象频繁写入会触发 detach，应避免不必要的复制和格式转换。

## 3. 直接使用

先确认值的有效性和表示格式，再调用查询、转换或修改 API；处理文本时区分 Unicode 和字节编码，处理图像时确认 format，处理 URL/路径时使用 Qt 的解析 API 而不是手写字符串规则。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `(since 6.8) const_iterator`
- `(since 6.8) const_pointer`
- `(since 6.8) const_reference`
- `(since 6.8) const_reverse_iterator`
- `(since 6.8) difference_type`
- `(since 6.8) pointer`
- `(since 6.8) reference`
- `(since 6.8) size_type`
- `(since 6.8) value_type`

### 公有函数

- `QVersionNumber()`
- `QVersionNumber(QList<int> &&seg)`
- `(since 6.8) QVersionNumber(QSpan<const int> args)`
- `QVersionNumber(const QList<int> &seg)`
- `QVersionNumber(int maj)`
- `QVersionNumber(std::initializer_list<int> args)`
- `QVersionNumber(int maj, int min)`
- `QVersionNumber(int maj, int min, int mic)`
- `(since 6.8) QVersionNumber::const_iterator begin() const`
- `(since 6.8) QVersionNumber::const_iterator cbegin() const`
- `(since 6.8) QVersionNumber::const_iterator cend() const`
- `(since 6.8) QVersionNumber::const_iterator constBegin() const`
- `(since 6.8) QVersionNumber::const_iterator constEnd() const`
- `(since 6.8) QVersionNumber::const_reverse_iterator crbegin() const`
- `(since 6.8) QVersionNumber::const_reverse_iterator crend() const`
- `(since 6.8) QVersionNumber::const_iterator end() const`
- `bool isNormalized() const`
- `bool isNull() const`
- `bool isPrefixOf(const QVersionNumber &other) const`
- `int majorVersion() const`
- `int microVersion() const`
- `int minorVersion() const`
- `QVersionNumber normalized() const`
- `(since 6.8) QVersionNumber::const_reverse_iterator rbegin() const`
- `(since 6.8) QVersionNumber::const_reverse_iterator rend() const`
- `int segmentAt(qsizetype index) const`
- `qsizetype segmentCount() const`
- `QList<int> segments() const`
- `QString toString() const`

### 静态公有成员

- `QVersionNumber commonPrefix(const QVersionNumber &v1, const QVersionNumber &v2)`
- `int compare(const QVersionNumber &v1, const QVersionNumber &v2)`
- `(since 6.4) QVersionNumber fromString(QAnyStringView string, qsizetype *suffixIndex = nullptr)`

### 相关非成员函数

- `bool operator!=(const QVersionNumber &lhs, const QVersionNumber &rhs)`
- `bool operator<(const QVersionNumber &lhs, const QVersionNumber &rhs)`
- `QDataStream & operator<<(QDataStream &out, const QVersionNumber &version)`
- `bool operator<=(const QVersionNumber &lhs, const QVersionNumber &rhs)`
- `bool operator==(const QVersionNumber &lhs, const QVersionNumber &rhs)`
- `bool operator>(const QVersionNumber &lhs, const QVersionNumber &rhs)`
- `bool operator>=(const QVersionNumber &lhs, const QVersionNumber &rhs)`
- `QDataStream & operator>>(QDataStream &in, QVersionNumber &version)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[alias, since 6.8] QVersionNumber::const_reverse_iterator`

**作用与语义：**

Typedefs 用于一个不透明类，实现了对`QVersionNumber`段的（反向）随机访问迭代器。
注意：`QVersionNumber` 不支持原地修改段，因此没有可变迭代器。
这些类型防线是在Qt 6.8引入的。

### `[alias, since 6.8] QVersionNumber::value_type`

**作用与语义：**

提供STL兼容性。
注意：`QVersionNumber`不支持原地修改段，因此引用和`const_reference`，以及指针和`const_pointer`都是同一类型。
这些类型防线是在Qt 6.8引入的。

### `[noexcept] QVersionNumber::QVersionNumber()`

**作用与语义：**

生成一个空版本。

### `[explicit] QVersionNumber::QVersionNumber(QList<int> &&seg)`

**作用与语义：**

Move从`seg`中包含的数字列表中构造出一个版本号。

### `[explicit, since 6.8] QVersionNumber::QVersionNumber(QSpan<const int> args)`

**作用与语义：**

根据`args`指定的范围构造版本号。
注意：在 6.8 之前的 Qt 版本中，QVersionNumber 只能由 `QList`、QVarLenthArray 或 std：：initializer_list 构建。

### `[explicit] QVersionNumber::QVersionNumber(const QList<int> &seg)`

**作用与语义：**

从`seg`中包含的数字列表中构建一个版本号。

### `[explicit] QVersionNumber::QVersionNumber(int maj)`

**作用与语义：**

构建一个仅包含主要版本号`maj`的QVersionNumber。

### `QVersionNumber::QVersionNumber(std::initializer_list<int> args)`

**作用与语义：**

根据`args`指定的std：：initializer_list构造版本号。

### `[explicit] QVersionNumber::QVersionNumber(int maj, int min)`

**作用与语义：**

构建一个QVersionNumber，分别由主版本号`maj`和次要版本号`min`组成。

### `[explicit] QVersionNumber::QVersionNumber(int maj, int min, int mic)`

**作用与语义：**

构建一个QVersionNumber，由主版本、次要和微版本编号`maj`、`min`和微版本`mic`组成。

### `[noexcept, since 6.8] QVersionNumber::const_iterator QVersionNumber::constEnd() const`

**作用与语义：**

返回`const_iterator`或`const_reverse_iterator`，分别指向该版本号的第一个或最后一个段之后的段。
注意：`QVersionNumber`不支持原地修改分段，因此没有可变迭代器。

### `[static] QVersionNumber QVersionNumber::commonPrefix(const QVersionNumber &v1, const QVersionNumber &v2)`

**作用与语义：**

`QVersionNumber` QVersionNumber：：commonPrefix（const `QVersionNumber` & v1，cont `QVersionNumber` & v2）。
返回一个版本号，该版本同时是`v1`和`v2`的父版本。

### `[static noexcept] int QVersionNumber::compare(const QVersionNumber &v1, const QVersionNumber &v2)`

**作用与语义：**

比较`v1`与`v2`，返回一个小于、等于或大于零的整数，具体取决于`v1`小于、等于或大于`v2`。
比较通过比较`v1`和`v2`的各个段，从索引0开始，向较长列表的末端进行比较。

**官方示例：**

```cpp
 QVersionNumber v1(1, 2);
 QVersionNumber v2(1, 2, 0);
 int compare = QVersionNumber::compare(v1, v2); // compare == -1
```

### `[static, since 6.4] QVersionNumber QVersionNumber::fromString(QAnyStringView string, qsizetype *suffixIndex = nullptr)`

**作用与语义：**

从一个特殊格式化的非负十进制数`string`构造一个`QVersionNumber`，这些数字以句号（`.`）为界隔。
当数值段被解析完毕后，字符串的其余部分被视为后缀字符串。如果该字符串的起始索引不是空的，则会存储在`suffixIndex`中。
注意：在Qt 6.4之前的版本中，该功能被`QString`、`QLatin1StringView`和`QStringView`重载，`suffixIndex`成为`int*`。

**官方示例：**

```cpp
 QLatin1StringView string("5.4.0-alpha");
 qsizetype suffixIndex;
 auto version = QVersionNumber::fromString(string, &suffixIndex);
 // version is 5.4.0
 // suffixIndex is 5
```

### `[noexcept] bool QVersionNumber::isNormalized() const`

**作用与语义：**

如果版本号没有尾部零，返回`true`;否则返回`false`。

### `[noexcept] bool QVersionNumber::isNull() const`

**作用与语义：**

如果没有数值段，返回`true`，否则返回`false`。

### `[noexcept] bool QVersionNumber::isPrefixOf(const QVersionNumber &other) const`

**作用与语义：**

如果当前版本号包含在`other`版本号中，返回`true`;否则返回`false`。

**官方示例：**

```cpp
 QVersionNumber v1(5, 3);
 QVersionNumber v2(5, 3, 1);
 bool value = v1.isPrefixOf(v2); // true
```

### `[noexcept] int QVersionNumber::majorVersion() const`

**作用与语义：**

返回主要版本号，即第一个段。该函数等价于 `segmentAt`（0）。如果该`QVersionNumber`对象为空，则返回 0。

### `[noexcept] int QVersionNumber::microVersion() const`

**作用与语义：**

返回微观版本号，即第三段。该函数等价于`segmentAt`（2）。如果该`QVersionNumber`对象不含微观数，则返回0。

### `[noexcept] int QVersionNumber::minorVersion() const`

**作用与语义：**

返回次要版本号，即第二个段。该函数等价于`segmentAt`（1）。如果该`QVersionNumber`对象不包含小数，则返回0。

### `QVersionNumber QVersionNumber::normalized() const`

**作用与语义：**

返回一个等效的版本号，但去掉所有尾随的零。
要检查两个数字是否等价，在进行比较前对两个版本号使用归一化()。

**官方示例：**

```cpp
 QVersionNumber v1(5, 4);
 QVersionNumber v2(5, 4, 0);
 bool equivalent = v1.normalized() == v2.normalized();
 bool equal = v1 == v2;
 // equivalent is true
 // equal is false
```

### `[noexcept] int QVersionNumber::segmentAt(qsizetype index) const`

**作用与语义：**

返回`index`的段值。如果索引不存在，返回0。

### `[noexcept] qsizetype QVersionNumber::segmentCount() const`

**作用与语义：**

返回存储在`segments()`中的整数。

### `QList<int> QVersionNumber::segments() const`

**作用与语义：**

返回所有数字段。

### `QString QVersionNumber::toString() const`

**作用与语义：**

返回一个字符串，所有段都用一个周期（`.`）分隔。

### `[noexcept] bool operator!=(const QVersionNumber &lhs, const QVersionNumber &rhs)`

**作用与语义：**

如果 `lhs` 不等于 `rhs`，则返回 `true`；否则返回 `false`。

### `[noexcept] bool operator<(const QVersionNumber &lhs, const QVersionNumber &rhs)`

**作用与语义：**

如果 `lhs` 小于 `rhs`，则返回 `true`；否则返回 `false`。

### `QDataStream &operator<<(QDataStream &out, const QVersionNumber &version)`

**作用与语义：**

写入版本号`version`以进行流`out`。
请注意，这与`QDataStream::version()`无关。

### `[noexcept] bool operator<=(const QVersionNumber &lhs, const QVersionNumber &rhs)`

**作用与语义：**

如果 `lhs` 小于或等于 `rhs`，则返回 `true`；否则返回 `false`。

### `[noexcept] bool operator==(const QVersionNumber &lhs, const QVersionNumber &rhs)`

**作用与语义：**

如果 `lhs` 等于 `rhs`，则返回 `true`；否则返回 `false`。

### `[noexcept] bool operator>(const QVersionNumber &lhs, const QVersionNumber &rhs)`

**作用与语义：**

如果 `lhs` 大于 `rhs`，则返回 `true`；否则返回 `false`。

### `[noexcept] bool operator>=(const QVersionNumber &lhs, const QVersionNumber &rhs)`

**作用与语义：**

如果 `lhs` 大于或等于 `rhs`，则返回 `true`；否则返回 `false`。

### `QDataStream &operator>>(QDataStream &in, QVersionNumber &version)`

**作用与语义：**

读取流`in`的版本号并存储在`version`。
请注意，这与`QDataStream::version()`无关。

### `(since 6.8) const_iterator`

**作用与语义：**

Typedefs 用于一个不透明类，实现了对`QVersionNumber`段的（反向）随机访问迭代器。
注意：`QVersionNumber` 不支持原地修改段，因此没有可变迭代器。
这些类型防线是在Qt 6.8引入的。

### `(since 6.8) const_pointer`

**作用与语义：**

提供STL兼容性。
注意：`QVersionNumber`不支持原地修改段，因此引用和`const_reference`，以及指针和`const_pointer`都是同一类型。
这些类型防线是在Qt 6.8引入的。

### `(since 6.8) const_reference`

**作用与语义：**

提供STL兼容性。
注意：`QVersionNumber`不支持原地修改段，因此引用和`const_reference`，以及指针和`const_pointer`都是同一类型。
这些类型防线是在Qt 6.8引入的。

### `(since 6.8) const_reverse_iterator`

**作用与语义：**

Typedefs 用于一个不透明类，实现了对`QVersionNumber`段的（反向）随机访问迭代器。
注意：`QVersionNumber` 不支持原地修改段，因此没有可变迭代器。
这些类型防线是在Qt 6.8引入的。

### `(since 6.8) difference_type`

**作用与语义：**

提供STL兼容性。
注意：`QVersionNumber`不支持原地修改段，因此引用和`const_reference`，以及指针和`const_pointer`都是同一类型。
这些类型防线是在Qt 6.8引入的。

### `(since 6.8) pointer`

**作用与语义：**

提供STL兼容性。
注意：`QVersionNumber`不支持原地修改段，因此引用和`const_reference`，以及指针和`const_pointer`都是同一类型。
这些类型防线是在Qt 6.8引入的。

### `(since 6.8) reference`

**作用与语义：**

提供STL兼容性。
注意：`QVersionNumber`不支持原地修改段，因此引用和`const_reference`，以及指针和`const_pointer`都是同一类型。
这些类型防线是在Qt 6.8引入的。

### `(since 6.8) size_type`

**作用与语义：**

提供STL兼容性。
注意：`QVersionNumber`不支持原地修改段，因此引用和`const_reference`，以及指针和`const_pointer`都是同一类型。
这些类型防线是在Qt 6.8引入的。

### `(since 6.8) value_type`

**作用与语义：**

提供STL兼容性。
注意：`QVersionNumber`不支持原地修改段，因此引用和`const_reference`，以及指针和`const_pointer`都是同一类型。
这些类型防线是在Qt 6.8引入的。

### `(since 6.8) QVersionNumber::const_iterator begin() const`

**作用与语义：**

返回`const_iterator`或`const_reverse_iterator`，分别指向该版本号的第一个或最后一个段之后的段。
注意：`QVersionNumber`不支持原地修改分段，因此没有可变迭代器。

### `(since 6.8) QVersionNumber::const_iterator cbegin() const`

**作用与语义：**

返回`const_iterator`或`const_reverse_iterator`，分别指向该版本号的第一个或最后一个段之后的段。
注意：`QVersionNumber`不支持原地修改分段，因此没有可变迭代器。

### `(since 6.8) QVersionNumber::const_iterator cend() const`

**作用与语义：**

返回`const_iterator`或`const_reverse_iterator`，分别指向该版本号的第一个或最后一个段之后的段。
注意：`QVersionNumber`不支持原地修改分段，因此没有可变迭代器。

### `(since 6.8) QVersionNumber::const_iterator constBegin() const`

**作用与语义：**

返回`const_iterator`或`const_reverse_iterator`，分别指向该版本号的第一个或最后一个段之后的段。
注意：`QVersionNumber`不支持原地修改分段，因此没有可变迭代器。

### `(since 6.8) QVersionNumber::const_reverse_iterator crbegin() const`

**作用与语义：**

返回`const_iterator`或`const_reverse_iterator`，分别指向该版本号的第一个或最后一个段之后的段。
注意：`QVersionNumber`不支持原地修改分段，因此没有可变迭代器。

### `(since 6.8) QVersionNumber::const_reverse_iterator crend() const`

**作用与语义：**

返回`const_iterator`或`const_reverse_iterator`，分别指向该版本号的第一个或最后一个段之后的段。
注意：`QVersionNumber`不支持原地修改分段，因此没有可变迭代器。

### `(since 6.8) QVersionNumber::const_iterator end() const`

**作用与语义：**

返回`const_iterator`或`const_reverse_iterator`，分别指向该版本号的第一个或最后一个段之后的段。
注意：`QVersionNumber`不支持原地修改分段，因此没有可变迭代器。

### `(since 6.8) QVersionNumber::const_reverse_iterator rbegin() const`

**作用与语义：**

返回`const_iterator`或`const_reverse_iterator`，分别指向该版本号的第一个或最后一个段之后的段。
注意：`QVersionNumber`不支持原地修改分段，因此没有可变迭代器。

### `(since 6.8) QVersionNumber::const_reverse_iterator rend() const`

**作用与语义：**

返回`const_iterator`或`const_reverse_iterator`，分别指向该版本号的第一个或最后一个段之后的段。
注意：`QVersionNumber`不支持原地修改分段，因此没有可变迭代器。

## 6. 深入实践与常见坑

### 生命周期和资源边界

值对象由作用域、容器或调用者管理，不使用 parent 和 deleteLater。跨线程传递副本通常比传递 QObject 安全，但共享数据在写入时仍可能发生复制，性能和内存峰值要结合数据规模判断。

### 状态和错误边界

重点区分空值、无效值、默认值和已初始化值。例如空字符串、空 URL、null 图像和无效索引不一定表示同一件事；转换函数的失败结果要通过对应的状态查询确认。

### 线程边界

值类型本身通常可以复制后跨线程传递；不要把 data()/bits()/constData() 得到的指针当成跨线程长期有效的所有权。大对象频繁写入会触发 detach，应避免不必要的复制和格式转换。

### 最容易出现的错误

不要把空值当成业务成功；不要保存临时对象的内部指针；不要把 QString 当二进制缓冲区；不要假定隐式共享让并发写入自动安全。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QVersionNumber` 所属机制类型：Qt 值类型与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
