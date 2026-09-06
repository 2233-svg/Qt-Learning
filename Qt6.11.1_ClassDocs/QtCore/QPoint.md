# QPoint

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 整数二维点类型，用于表示位置、偏移量和坐标计算。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QPoint`：整数二维点类型，用于表示位置、偏移量和坐标计算。

**内部模型：** 这类类型通常可以按值传递、复制和返回。许多 Qt 容器、字符串和图像采用隐式共享：复制时共享数据，发生写操作时才 detach。这样便于 API 传值，但获取原始指针或长期持有引用时必须考虑对象修改和生命周期。

**适用场景：** 先确认值的有效性和表示格式，再调用查询、转换或修改 API；处理文本时区分 Unicode 和字节编码，处理图像时确认 format，处理 URL/路径时使用 Qt 的解析 API 而不是手写字符串规则。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要把空值当成业务成功；不要保存临时对象的内部指针；不要把 QString 当二进制缓冲区；不要假定隐式共享让并发写入自动安全。

## 2. 依赖与对象关系

- 头文件：`#include <QPoint>`
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

- `QPoint()`
- `QPoint(int xpos, int ypos)`
- `bool isNull() const`
- `int manhattanLength() const`
- `int & rx()`
- `int & ry()`
- `void setX(int x)`
- `void setY(int y)`
- `CGPoint toCGPoint() const`
- `(since 6.4) QPointF toPointF() const`
- `QPoint transposed() const`
- `int x() const`
- `int y() const`
- `QPoint & operator*=(double factor)`
- `QPoint & operator*=(float factor)`
- `QPoint & operator*=(int factor)`
- `QPoint & operator+=(const QPoint &point)`
- `QPoint & operator-=(const QPoint &point)`
- `QPoint & operator/=(qreal divisor)`

### 静态公有成员

- `int dotProduct(const QPoint &p1, const QPoint &p2)`

### 相关非成员函数

- `bool operator!=(const QPoint &lhs, const QPoint &rhs)`
- `QPoint operator*(const QPoint &point, double factor)`
- `QPoint operator*(const QPoint &point, float factor)`
- `QPoint operator*(const QPoint &point, int factor)`
- `QPoint operator*(double factor, const QPoint &point)`
- `QPoint operator*(float factor, const QPoint &point)`
- `QPoint operator*(int factor, const QPoint &point)`
- `QPoint operator+(const QPoint &point)`
- `QPoint operator+(const QPoint &p1, const QPoint &p2)`
- `QPoint operator-(const QPoint &p1, const QPoint &p2)`
- `QPoint operator-(const QPoint &point)`
- `QPoint operator/(const QPoint &point, qreal divisor)`
- `QDataStream & operator<<(QDataStream &stream, const QPoint &point)`
- `bool operator==(const QPoint &lhs, const QPoint &rhs)`
- `QDataStream & operator>>(QDataStream &stream, QPoint &point)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[constexpr noexcept] QPoint::QPoint()`

**作用与语义：**

构造一个零点，即坐标为 （0， 0）。

### `[constexpr noexcept] QPoint::QPoint(int xpos, int ypos)`

**作用与语义：**

构造一个点，坐标为给定的坐标（`xpos`， `ypos`）。

### `[static constexpr] int QPoint::dotProduct(const QPoint &p1, const QPoint &p2)`

**作用与语义：**

返回`p1`和`p2`的点积。

**官方示例：**

```cpp
 QPoint p( 3, 7);
 QPoint q(-1, 4);
 int dotProduct = QPoint::dotProduct(p, q);   // dotProduct becomes 25
```

### `[constexpr noexcept] bool QPoint::isNull() const`

**作用与语义：**

如果x和y坐标都设为0，返回`true`，否则返回`false`。

### `[constexpr] int QPoint::manhattanLength() const`

**作用与语义：**

返回`x()`和`y()`的绝对值之和，传统上称为从原点到点的向量“曼哈顿长度”。例如：
这是一个实用且易于快速计算的真实长度近似：
“曼哈顿长度”这一传统源自于这些距离适用于只能在矩形网格上行进的旅行者，比如曼哈顿的街道。

**官方示例：**

```cpp
 QPoint oldPosition;

 void MyWidget::mouseMoveEvent(QMouseEvent *event)
 {
     QPoint point = event->pos() - oldPosition;
     if (point.manhattanLength() > 3){
         // the mouse has moved more than 3 pixels since the oldPosition
     }
 }
```

### `[constexpr noexcept] int &QPoint::rx()`

**作用与语义：**

返回该点的x坐标的引用。
使用引用可以直接操作 x。例如：

**官方示例：**

```cpp
 QPoint p(1, 2);
 p.rx()--;   // p becomes (0, 2)
```

### `[constexpr noexcept] int &QPoint::ry()`

**作用与语义：**

返回该点的y坐标参考。
使用引用可以直接操作 y 。例如：

**官方示例：**

```cpp
 QPoint p(1, 2);
 p.ry()++;   // p becomes (1, 3)
```

### `[constexpr noexcept] void QPoint::setX(int x)`

**作用与语义：**

将该点的x坐标设为给定的`x`坐标。

### `[constexpr noexcept] void QPoint::setY(int y)`

**作用与语义：**

将该点的y坐标设为给定的`y`坐标。

### `[noexcept] CGPoint QPoint::toCGPoint() const`

**作用与语义：**

从`QPoint`生成CGPoint。

### `[constexpr noexcept, since 6.4] QPointF QPoint::toPointF() const`

**作用与语义：**

将该点返回为浮点精度的点。

### `[constexpr noexcept] QPoint QPoint::transposed() const`

**作用与语义：**

返回一个交换坐标x和y的点：

**官方示例：**

```cpp
 QPoint{1, 2}.transposed() // {2, 1}
```

### `[constexpr noexcept] int QPoint::x() const`

**作用与语义：**

返回该点的 x 坐标。

### `[constexpr noexcept] int QPoint::y() const`

**作用与语义：**

返回该点的y坐标。

### `[constexpr] QPoint &QPoint::operator*=(double factor)`

**作用与语义：**

将该点的坐标乘以给定的`factor`，返回该点的参考。例如：
注意，由于点以整数计入，结果会四舍五入到最接近的整数。使用`QPointF`以实现浮点精度。

**官方示例：**

```cpp
 QPoint p(-1, 4);
 p *= 2.5;    // p becomes (-3, 10)
```

### `[constexpr] QPoint &QPoint::operator*=(float factor)`

**作用与语义：**

将该点坐标乘以给定`factor`，返回该点的参考。
注意，由于点以整数表示，结果会四舍五入到最接近的整数。使用`QPointF`以实现浮点精度。

### `[constexpr] QPoint &QPoint::operator*=(int factor)`

**作用与语义：**

将该点坐标乘以给定`factor`，返回该点的参考。

### `[constexpr] QPoint &QPoint::operator+=(const QPoint &point)`

**作用与语义：**

将给定`point`加到该点，并返回该点的引用。例如：

**官方示例：**

```cpp
 QPoint p( 3, 7);
 QPoint q(-1, 4);
 p += q;    // p becomes (2, 11)
```

### `[constexpr] QPoint &QPoint::operator-=(const QPoint &point)`

**作用与语义：**

从该点减去给定`point`，返回该点的引用。例如：

**官方示例：**

```cpp
 QPoint p( 3, 7);
 QPoint q(-1, 4);
 p -= q;    // p becomes (4, 3)
```

### `[constexpr] QPoint &QPoint::operator/=(qreal divisor)`

**作用与语义：**

将x和y除以给定`divisor`，并返回该点的引用。例如：
注意，由于点被记为整数，结果会四舍五入到最近的整数。使用`QPointF`以实现浮点精度。

**官方示例：**

```cpp
 QPoint p(-3, 10);
 p /= 2.5;           // p becomes (-1, 4)
```

### `[constexpr noexcept] bool operator!=(const QPoint &lhs, const QPoint &rhs)`

**作用与语义：**

如果 `lhs` 和 `rhs` 不相等，则返回 `true`；否则返回 `false`。

### `[constexpr] QPoint operator*(const QPoint &point, double factor)`

**作用与语义：**

返回给定`point`乘以给定`factor`的副本。
注意，由于点被用作整数，结果会四舍五入到最近的整数。使用`QPointF`以实现浮点精度。

### `[constexpr] QPoint operator*(const QPoint &point, float factor)`

**作用与语义：**

返回给定`point`乘以给定`factor`的副本。
注意，由于点被用作整数，结果会四舍五入到最近的整数。使用`QPointF`以实现浮点精度。

### `[constexpr noexcept] QPoint operator*(const QPoint &point, int factor)`

**作用与语义：**

返回给定`point`的副本乘以给定`factor`。

### `[constexpr] QPoint operator*(double factor, const QPoint &point)`

**作用与语义：**

返回给定`point`乘以给定`factor`的副本。
注意，由于点被用作整数，结果会四舍五入到最近的整数。使用`QPointF`以实现浮点精度。

### `[constexpr] QPoint operator*(float factor, const QPoint &point)`

**作用与语义：**

返回给定`point`乘以给定`factor`的副本。
注意，由于点被用作整数，结果会四舍五入到最近的整数。使用`QPointF`以实现浮点精度。

### `[constexpr noexcept] QPoint operator*(int factor, const QPoint &point)`

**作用与语义：**

返回给定`point`的副本乘以给定`factor`。

### `[constexpr noexcept] QPoint operator+(const QPoint &point)`

**作用与语义：**

退货未`point`修改。

### `[constexpr noexcept] QPoint operator+(const QPoint &p1, const QPoint &p2)`

**作用与语义：**

返回一个`QPoint`对象，该对象是给定点、`p1`和`p2`的和;每个分量单独相加。

### `[constexpr noexcept] QPoint operator-(const QPoint &p1, const QPoint &p2)`

**作用与语义：**

返回一个`QPoint`对象，该对象由`p1`中减去`p2`;每个分量单独相减。

### `[constexpr noexcept] QPoint operator-(const QPoint &point)`

**作用与语义：**

返回一个`QPoint`对象，该对象通过改变给定`point`的两个分量的符号构成。
相当于`QPoint(0,0) - point`。

### `[constexpr] QPoint operator/(const QPoint &point, qreal divisor)`

**作用与语义：**

返回将给定`point`的两个分量除以给定`divisor`所形成的`QPoint`。
注意，由于积分为整数，结果会四舍五入到最近的整数。使用`QPointF`以实现浮点精度。

### `QDataStream &operator<<(QDataStream &stream, const QPoint &point)`

**作用与语义：**

将给定的`point`写入给定的`stream`，并返回对流的引用。

### `[constexpr noexcept] bool operator==(const QPoint &lhs, const QPoint &rhs)`

**作用与语义：**

如果 `lhs` 和 `rhs` 相等，则返回 `true`；否则返回 `false`。

### `QDataStream &operator>>(QDataStream &stream, QPoint &point)`

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

`QPoint` 所属机制类型：Qt 值类型与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
