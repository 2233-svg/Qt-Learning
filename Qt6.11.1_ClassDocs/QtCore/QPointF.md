# QPointF

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 浮点二维点类型，用于表示带小数的几何位置和变换结果。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QPointF`：浮点二维点类型，用于表示带小数的几何位置和变换结果。

**内部模型：** 这类类型通常可以按值传递、复制和返回。许多 Qt 容器、字符串和图像采用隐式共享：复制时共享数据，发生写操作时才 detach。这样便于 API 传值，但获取原始指针或长期持有引用时必须考虑对象修改和生命周期。

**适用场景：** 先确认值的有效性和表示格式，再调用查询、转换或修改 API；处理文本时区分 Unicode 和字节编码，处理图像时确认 format，处理 URL/路径时使用 Qt 的解析 API 而不是手写字符串规则。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要把空值当成业务成功；不要保存临时对象的内部指针；不要把 QString 当二进制缓冲区；不要假定隐式共享让并发写入自动安全。

## 2. 依赖与对象关系

- 头文件：`#include <QPointF>`
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

- `QPointF()`
- `QPointF(const QPoint &point)`
- `QPointF(qreal xpos, qreal ypos)`
- `bool isNull() const`
- `qreal manhattanLength() const`
- `qreal & rx()`
- `qreal & ry()`
- `void setX(qreal x)`
- `void setY(qreal y)`
- `CGPoint toCGPoint() const`
- `QPoint toPoint() const`
- `QPointF transposed() const`
- `qreal x() const`
- `qreal y() const`
- `QPointF & operator*=(qreal factor)`
- `QPointF & operator+=(const QPointF &point)`
- `QPointF & operator-=(const QPointF &point)`
- `QPointF & operator/=(qreal divisor)`

### 静态公有成员

- `qreal dotProduct(const QPointF &p1, const QPointF &p2)`
- `QPointF fromCGPoint(CGPoint point)`

### 相关非成员函数

- `(since 6.8) bool qFuzzyCompare(const QPointF &p1, const QPointF &p2)`
- `(since 6.8) bool qFuzzyIsNull(const QPointF &point)`
- `bool operator!=(const QPointF &lhs, const QPointF &rhs)`
- `QPointF operator*(const QPointF &point, qreal factor)`
- `QPointF operator*(qreal factor, const QPointF &point)`
- `QPointF operator+(const QPointF &point)`
- `QPointF operator+(const QPointF &p1, const QPointF &p2)`
- `QPointF operator-(const QPointF &p1, const QPointF &p2)`
- `QPointF operator-(const QPointF &point)`
- `QPointF operator/(const QPointF &point, qreal divisor)`
- `QDataStream & operator<<(QDataStream &stream, const QPointF &point)`
- `bool operator==(const QPointF &lhs, const QPointF &rhs)`
- `QDataStream & operator>>(QDataStream &stream, QPointF &point)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[constexpr noexcept] QPointF::QPointF()`

**作用与语义：**

构造一个空点，即坐标为 （0.0， 0.0）。

### `[constexpr noexcept] QPointF::QPointF(const QPoint &point)`

**作用与语义：**

构建给定`point`的副本。

### `[constexpr noexcept] QPointF::QPointF(qreal xpos, qreal ypos)`

**作用与语义：**

构造一个点，坐标为给定的坐标（`xpos`， `ypos`）。

### `[static constexpr] qreal QPointF::dotProduct(const QPointF &p1, const QPointF &p2)`

**作用与语义：**

返回`p1`和`p2`的点积。

**官方示例：**

```cpp
 QPointF p( 3.1, 7.1);
 QPointF q(-1.0, 4.1);
 qreal dotProduct = QPointF::dotProduct(p, q);   // dotProduct becomes 26.01
```

### `[static noexcept] QPointF QPointF::fromCGPoint(CGPoint point)`

**作用与语义：**

从CGPoint `point`创建`QRectF`。

### `[noexcept] bool QPointF::isNull() const`

**作用与语义：**

如果x和y坐标都设为0.0（忽略符号），返回`true`;否则返回`false`。

### `[constexpr] qreal QPointF::manhattanLength() const`

**作用与语义：**

返回`x()`和`y()`的绝对值之和，传统上称为从原点到点的“曼哈顿长度”。

### `[constexpr noexcept] qreal &QPointF::rx()`

**作用与语义：**

返回该点的x坐标的引用。
使用引用可以直接操作 x。例如：

**官方示例：**

```cpp
 QPointF p(1.1, 2.5);
 p.rx()--;   // p becomes (0.1, 2.5)
```

### `[constexpr noexcept] qreal &QPointF::ry()`

**作用与语义：**

返回该点的y坐标参考。
使用引用可以直接操作 y 。例如：

**官方示例：**

```cpp
 QPointF p(1.1, 2.5);
 p.ry()++;   // p becomes (1.1, 3.5)
```

### `[constexpr noexcept] void QPointF::setX(qreal x)`

**作用与语义：**

将该点的x坐标设为给定的有限`x`坐标。

### `[constexpr noexcept] void QPointF::setY(qreal y)`

**作用与语义：**

将该点的y坐标设为给定的有限`y`坐标。

### `[noexcept] CGPoint QPointF::toCGPoint() const`

**作用与语义：**

从`QPointF`创建CGPoint。

### `[constexpr] QPoint QPointF::toPoint() const`

**作用与语义：**

将该点的坐标四舍五入到最近的整数，返回一个带有四舍五入坐标的`QPoint`对象。

### `[constexpr noexcept] QPointF QPointF::transposed() const`

**作用与语义：**

返回一个交换坐标x和y的点：

**官方示例：**

```cpp
 QPointF{1.0, 2.0}.transposed() // {2.0, 1.0}
```

### `[constexpr noexcept] qreal QPointF::x() const`

**作用与语义：**

返回该点的 x 坐标。

### `[constexpr noexcept] qreal QPointF::y() const`

**作用与语义：**

返回该点的y坐标。

### `[constexpr] QPointF &QPointF::operator*=(qreal factor)`

**作用与语义：**

将该点的坐标乘以给定的有限`factor`，返回该点的参考。例如：

**官方示例：**

```cpp
 QPointF p(-1.1, 4.1);
 p *= 2.5;    // p becomes (-2.75, 10.25)
```

### `[constexpr] QPointF &QPointF::operator+=(const QPointF &point)`

**作用与语义：**

将给定`point`加到该点，并返回该点的引用。例如：

**官方示例：**

```cpp
 QPointF p( 3.1, 7.1);
 QPointF q(-1.0, 4.1);
 p += q;    // p becomes (2.1, 11.2)
```

### `[constexpr] QPointF &QPointF::operator-=(const QPointF &point)`

**作用与语义：**

从该点减去给定`point`，返回该点的引用。例如：

**官方示例：**

```cpp
 QPointF p( 3.1, 7.1);
 QPointF q(-1.0, 4.1);
 p -= q;    // p becomes (4.1, 3.0)
```

### `[constexpr] QPointF &QPointF::operator/=(qreal divisor)`

**作用与语义：**

将x和y除以给定`divisor`，并返回该点的引用。例如：
`divisor`不能是零或NaN。

**官方示例：**

```cpp
 QPointF p(-2.75, 10.25);
 p /= 2.5;           // p becomes (-1.1, 4.1)
```

### `[constexpr noexcept, since 6.8] bool qFuzzyCompare(const QPointF &p1, const QPointF &p2)`

**作用与语义：**

如果 `p1` 大约等于 `p2`，则返回`true`;否则返回`false`。

### `[constexpr noexcept, since 6.8] bool qFuzzyIsNull(const QPointF &point)`

**作用与语义：**

如果 `point` 大致等于点 `(0.0, 0.0)`，则收益`true`。

### `[constexpr noexcept] bool operator!=(const QPointF &lhs, const QPointF &rhs)`

**作用与语义：**

如果 `lhs` 与 `rhs` 足够不同，则返回 `false`；否则返回 `false`。
警告：此函数不检查严格不等式；相反，它使用模糊比较来比较点的坐标。

### `[constexpr] QPointF operator*(const QPointF &point, qreal factor)`

**作用与语义：**

返回给定`point`的副本，乘以给定的有限`factor`。

### `[constexpr] QPointF operator*(qreal factor, const QPointF &point)`

**作用与语义：**

返回给定`point`的副本，乘以给定的有限`factor`。

### `[constexpr] QPointF operator+(const QPointF &point)`

**作用与语义：**

退货未`point`修改。

### `[constexpr] QPointF operator+(const QPointF &p1, const QPointF &p2)`

**作用与语义：**

返回一个`QPointF`对象，该对象是给定点`p1`和`p2`的和;每个分量单独相加。

### `[constexpr] QPointF operator-(const QPointF &p1, const QPointF &p2)`

**作用与语义：**

返回一个`QPointF`对象，由`p1`中减去`p2`;每个分量单独相减。

### `[constexpr] QPointF operator-(const QPointF &point)`

**作用与语义：**

返回一个`QPointF`对象，该对象通过改变给定`point`的每个分量的符号构成。
相当于`QPointF(0,0) - point`。

### `[constexpr] QPointF operator/(const QPointF &point, qreal divisor)`

**作用与语义：**

返回由给定`point`的每个分量除以给定`divisor`所形成的`QPointF`对象。
`divisor`不能是零或NaN。

### `QDataStream &operator<<(QDataStream &stream, const QPointF &point)`

**作用与语义：**

将给定的`point`写入给定的`stream`，并返回对流的引用。

### `[constexpr noexcept] bool operator==(const QPointF &lhs, const QPointF &rhs)`

**作用与语义：**

如果 `lhs` 大致等于 `rhs`，则返回 `true`；否则返回 `false`。
警告：此函数不检查严格相等；相反，它使用模糊比较来比较点的坐标。

### `QDataStream &operator>>(QDataStream &stream, QPointF &point)`

**作用与语义：**

将给定`stream`中的一个点读入给定`point`，并返回对该流的引用。

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

`QPointF` 所属机制类型：Qt 值类型与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
