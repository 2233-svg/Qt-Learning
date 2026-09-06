# QMargins

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 整数边距类型，用于表示布局或矩形四条边的外边距。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QMargins`：整数边距类型，用于表示布局或矩形四条边的外边距。

**内部模型：** 这类类型通常可以按值传递、复制和返回。许多 Qt 容器、字符串和图像采用隐式共享：复制时共享数据，发生写操作时才 detach。这样便于 API 传值，但获取原始指针或长期持有引用时必须考虑对象修改和生命周期。

**适用场景：** 先确认值的有效性和表示格式，再调用查询、转换或修改 API；处理文本时区分 Unicode 和字节编码，处理图像时确认 format，处理 URL/路径时使用 Qt 的解析 API 而不是手写字符串规则。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要把空值当成业务成功；不要保存临时对象的内部指针；不要把 QString 当二进制缓冲区；不要假定隐式共享让并发写入自动安全。

## 2. 依赖与对象关系

- 头文件：`#include <QMargins>`
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

先确认值的有效性和表示格式，再调用查询、转换或修改 API；处理文本时区分 Unicode 和字节编码，处理图像时确认 format，处理 URL/路径时使用 Qt 的解析 API 而不是手写字符串规则。 使用时通常按这个过程组织：构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有函数

- `QMargins()`
- `QMargins(int left, int top, int right, int bottom)`
- `int bottom() const`
- `bool isNull() const`
- `int left() const`
- `int right() const`
- `void setBottom(int bottom)`
- `void setLeft(int left)`
- `void setRight(int right)`
- `void setTop(int Top)`
- `(since 6.4) QMarginsF toMarginsF() const`
- `int top() const`
- `QMargins & operator*=(int factor)`
- `QMargins & operator*=(qreal factor)`
- `QMargins & operator+=(const QMargins &margins)`
- `QMargins & operator+=(int addend)`
- `QMargins & operator-=(const QMargins &margins)`
- `QMargins & operator-=(int subtrahend)`
- `QMargins & operator/=(int divisor)`
- `QMargins & operator/=(qreal divisor)`

### 相关非成员函数

- `bool operator!=(const QMargins &lhs, const QMargins &rhs)`
- `QMargins operator*(const QMargins &margins, int factor)`
- `QMargins operator*(const QMargins &margins, qreal factor)`
- `QMargins operator*(int factor, const QMargins &margins)`
- `QMargins operator*(qreal factor, const QMargins &margins)`
- `QMargins operator+(const QMargins &margins)`
- `QMargins operator+(const QMargins &m1, const QMargins &m2)`
- `QMargins operator+(const QMargins &lhs, int rhs)`
- `QMargins operator+(int lhs, const QMargins &rhs)`
- `QMargins operator-(const QMargins &margins)`
- `QMargins operator-(const QMargins &m1, const QMargins &m2)`
- `QMargins operator-(const QMargins &lhs, int rhs)`
- `QMargins operator/(const QMargins &margins, int divisor)`
- `QMargins operator/(const QMargins &margins, qreal divisor)`
- `QDataStream & operator<<(QDataStream &stream, const QMargins &m)`
- `bool operator==(const QMargins &lhs, const QMargins &rhs)`
- `QDataStream & operator>>(QDataStream &stream, QMargins &m)`
- `(since 6.0) QMargins operator|(const QMargins &m1, const QMargins &m2)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[constexpr noexcept] QMargins::QMargins()`

**作用与语义：**

构造一个所有边距为0的边距对象。

### `[constexpr noexcept] QMargins::QMargins(int left, int top, int right, int bottom)`

**作用与语义：**

构造给定`left`、`top`、`right`和`bottom`的边际。

### `[constexpr noexcept] int QMargins::bottom() const`

**作用与语义：**

返回底部边距。

### `[constexpr noexcept] bool QMargins::isNull() const`

**作用与语义：**

如果所有边距均为0，则返回`true`;否则返回为假。

### `[constexpr noexcept] int QMargins::left() const`

**作用与语义：**

返回左边距。

### `[constexpr noexcept] int QMargins::right() const`

**作用与语义：**

返回右边距。

### `[constexpr noexcept] void QMargins::setBottom(int bottom)`

**作用与语义：**

将底边距设为`bottom`。

### `[constexpr noexcept] void QMargins::setLeft(int left)`

**作用与语义：**

将左边距设为`left`。

### `[constexpr noexcept] void QMargins::setRight(int right)`

**作用与语义：**

将右边距设为`right`。

### `[constexpr noexcept] void QMargins::setTop(int Top)`

**作用与语义：**

将顶部边距设为`Top`。

### `[constexpr noexcept, since 6.4] QMarginsF QMargins::toMarginsF() const`

**作用与语义：**

将这些边际返回为浮点精度的边际。

### `[constexpr noexcept] int QMargins::top() const`

**作用与语义：**

返回最高边际。

### `[constexpr noexcept] QMargins &QMargins::operator*=(int factor)`

**作用与语义：**

将该对象的每个组件乘以`factor`并返回对其的引用。

### `[constexpr noexcept] QMargins &QMargins::operator*=(qreal factor)`

**作用与语义：**

将该对象的每个组件乘以`factor`并返回对其的引用。

### `[constexpr noexcept] QMargins &QMargins::operator+=(const QMargins &margins)`

**作用与语义：**

将`margins`的每个组件添加到该对象的相应组件中，并返回对该组件的引用。

### `[constexpr noexcept] QMargins &QMargins::operator+=(int addend)`

**作用与语义：**

将`addend`添加到该对象的每个组件并返回引用。

### `[constexpr noexcept] QMargins &QMargins::operator-=(const QMargins &margins)`

**作用与语义：**

从该对象的相应组件中减去`margins`的每个组件，返回对它的引用。

### `[constexpr noexcept] QMargins &QMargins::operator-=(int subtrahend)`

**作用与语义：**

从该对象的每个组件中减去`subtrahend`，并返回对其的引用。

### `[constexpr] QMargins &QMargins::operator/=(int divisor)`

**作用与语义：**

将该对象的每个组件除以 `divisor`，并返回对其的引用。

### `[constexpr] QMargins &QMargins::operator/=(qreal divisor)`

**作用与语义：**

将该对象的每个组件除以 `divisor`，并返回对其的引用。

### `[constexpr noexcept] bool operator!=(const QMargins &lhs, const QMargins &rhs)`

**作用与语义：**

如果 `lhs` 和 `rhs` 不同，则返回 `true`；否则返回 `false`。

### `[constexpr noexcept] QMargins operator*(const QMargins &margins, int factor)`

**作用与语义：**

返回一个`QMargins`对象，该对象由给定`margins`的每个分量乘以`factor`构成。

### `[constexpr noexcept] QMargins operator*(const QMargins &margins, qreal factor)`

**作用与语义：**

返回一个`QMargins`对象，该对象由给定`margins`的每个分量乘以`factor`构成。

### `[constexpr noexcept] QMargins operator*(int factor, const QMargins &margins)`

**作用与语义：**

返回一个`QMargins`对象，该对象由给定`margins`的每个分量乘以`factor`构成。

### `[constexpr noexcept] QMargins operator*(qreal factor, const QMargins &margins)`

**作用与语义：**

返回一个`QMargins`对象，该对象由给定`margins`的每个分量乘以`factor`构成。

### `[constexpr noexcept] QMargins operator+(const QMargins &margins)`

**作用与语义：**

返回由`margins`的所有分量组成的QMargin对象。

### `[constexpr noexcept] QMargins operator+(const QMargins &m1, const QMargins &m2)`

**作用与语义：**

返回一个`QMargins`对象，该对象是给定边距`m1`和`m2`的总和;每个分量单独添加。

### `[constexpr noexcept] QMargins operator+(const QMargins &lhs, int rhs)`

**作用与语义：**

返回一个通过向`lhs`添加`rhs`而形成的`QMargins`对象。

### `[constexpr noexcept] QMargins operator+(int lhs, const QMargins &rhs)`

**作用与语义：**

返回一个通过向`rhs`添加`lhs`形成的`QMargins`对象。

### `[constexpr noexcept] QMargins operator-(const QMargins &margins)`

**作用与语义：**

返回一个由否定所有分量组成的QMargin对象`margins`。

### `[constexpr noexcept] QMargins operator-(const QMargins &m1, const QMargins &m2)`

**作用与语义：**

返回一个`QMargins`对象，由`m1`中减去`m2`;每个分量单独相减。

### `[constexpr noexcept] QMargins operator-(const QMargins &lhs, int rhs)`

**作用与语义：**

返回一个`QMargins`对象，该对象由`lhs`减去`rhs`而成。

### `[constexpr] QMargins operator/(const QMargins &margins, int divisor)`

**作用与语义：**

返回一个`QMargins`对象，该对象由给定`margins`的分量除以给定的`divisor`形成。

### `[constexpr] QMargins operator/(const QMargins &margins, qreal divisor)`

**作用与语义：**

返回一个`QMargins`对象，该对象由给定`margins`的分量除以给定的`divisor`形成。

### `QDataStream &operator<<(QDataStream &stream, const QMargins &m)`

**作用与语义：**

将边距`m`写入给定`stream`并返回流的引用。

### `[constexpr noexcept] bool operator==(const QMargins &lhs, const QMargins &rhs)`

**作用与语义：**

如果 `lhs` 和 `rhs` 相等，则返回 `true`；否则返回 `false`。

### `QDataStream &operator>>(QDataStream &stream, QMargins &m)`

**作用与语义：**

读取给定`stream`的边距到边距`m`，并返回对该流的引用。

### `[constexpr noexcept, since 6.0] QMargins operator|(const QMargins &m1, const QMargins &m2)`

**作用与语义：**

返回一个`QMargins`对象，由`m2`和`m1`的每个分量的最大值组成。

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

`QMargins` 所属机制类型：Qt 值类型与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
