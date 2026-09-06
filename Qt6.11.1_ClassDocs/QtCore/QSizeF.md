# QSizeF

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 浮点尺寸类型，用于表示带小数的宽高和几何计算结果。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QSizeF`：浮点尺寸类型，用于表示带小数的宽高和几何计算结果。

**内部模型：** 这类类型通常可以按值传递、复制和返回。许多 Qt 容器、字符串和图像采用隐式共享：复制时共享数据，发生写操作时才 detach。这样便于 API 传值，但获取原始指针或长期持有引用时必须考虑对象修改和生命周期。

**适用场景：** 先确认值的有效性和表示格式，再调用查询、转换或修改 API；处理文本时区分 Unicode 和字节编码，处理图像时确认 format，处理 URL/路径时使用 Qt 的解析 API 而不是手写字符串规则。

**典型调用链：** 构造或取得有效对象 -> 检查初始状态 -> 调用与本类职责对应的 API -> 验证返回值/通知 -> 处理无效值和资源边界。

**先记住的坑：** 不要把空值当成业务成功；不要保存临时对象的内部指针；不要把 QString 当二进制缓冲区；不要假定隐式共享让并发写入自动安全。

## 2. 依赖与对象关系

- 头文件：`#include <QSizeF>`
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

- `QSizeF()`
- `QSizeF(const QSize &size)`
- `QSizeF(qreal width, qreal height)`
- `QSizeF boundedTo(const QSizeF &otherSize) const`
- `QSizeF expandedTo(const QSizeF &otherSize) const`
- `QSizeF grownBy(QMarginsF margins) const`
- `qreal height() const`
- `bool isEmpty() const`
- `bool isNull() const`
- `bool isValid() const`
- `qreal & rheight()`
- `qreal & rwidth()`
- `void scale(qreal width, qreal height, Qt::AspectRatioMode mode)`
- `void scale(const QSizeF &size, Qt::AspectRatioMode mode)`
- `QSizeF scaled(qreal width, qreal height, Qt::AspectRatioMode mode) const`
- `QSizeF scaled(const QSizeF &s, Qt::AspectRatioMode mode) const`
- `void setHeight(qreal height)`
- `void setWidth(qreal width)`
- `QSizeF shrunkBy(QMarginsF margins) const`
- `CGSize toCGSize() const`
- `QSize toSize() const`
- `void transpose()`
- `QSizeF transposed() const`
- `qreal width() const`
- `QSizeF & operator*=(qreal factor)`
- `QSizeF & operator+=(const QSizeF &size)`
- `QSizeF & operator-=(const QSizeF &size)`
- `QSizeF & operator/=(qreal divisor)`

### 静态公有成员

- `QSizeF fromCGSize(CGSize size)`

### 相关非成员函数

- `(since 6.8) bool qFuzzyCompare(const QSizeF &lhs, const QSizeF &rhs)`
- `(since 6.8) bool qFuzzyIsNull(const QSizeF &size)`
- `bool operator!=(const QSizeF &lhs, const QSizeF &rhs)`
- `QSizeF operator*(const QSizeF &size, qreal factor)`
- `QSizeF operator*(qreal factor, const QSizeF &size)`
- `QSizeF operator+(const QSizeF &s1, const QSizeF &s2)`
- `QSizeF operator-(const QSizeF &s1, const QSizeF &s2)`
- `QSizeF operator/(const QSizeF &size, qreal divisor)`
- `QDataStream & operator<<(QDataStream &stream, const QSizeF &size)`
- `bool operator==(const QSizeF &lhs, const QSizeF &rhs)`
- `QDataStream & operator>>(QDataStream &stream, QSizeF &size)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[constexpr noexcept] QSizeF::QSizeF()`

**作用与语义：**

构造一个无效的大小。

### `[constexpr noexcept] QSizeF::QSizeF(const QSize &size)`

**作用与语义：**

根据给定`size`构造出具有浮点精度的大小。

### `[constexpr noexcept] QSizeF::QSizeF(qreal width, qreal height)`

**作用与语义：**

构造出具有有限`width`和`height`的大小。

### `[constexpr noexcept] QSizeF QSizeF::boundedTo(const QSizeF &otherSize) const`

**作用与语义：**

返回一个尺寸，保持该尺寸的最小宽度和高度，以及给定的`otherSize`。

### `[constexpr noexcept] QSizeF QSizeF::expandedTo(const QSizeF &otherSize) const`

**作用与语义：**

返回一个包含该尺寸最大宽度和高度及给定`otherSize`的尺寸。

### `[static noexcept] QSizeF QSizeF::fromCGSize(CGSize size)`

**作用与语义：**

`size`产生`QSizeF`。

### `[constexpr noexcept] QSizeF QSizeF::grownBy(QMarginsF margins) const`

**作用与语义：**

返回因该尺寸增加`margins`而产生的大小。

### `[constexpr noexcept] qreal QSizeF::height() const`

**作用与语义：**

还原高度。

### `[constexpr noexcept] bool QSizeF::isEmpty() const`

**作用与语义：**

如果宽度和高度中任一小于或等于0，返回`true`;否则返回`false`。

### `[noexcept] bool QSizeF::isNull() const`

**作用与语义：**

如果宽度和高度均为0.0（忽略符号），返回`true`;否则返回`false`。

### `[constexpr noexcept] bool QSizeF::isValid() const`

**作用与语义：**

如果宽度和高度都等于或大于0，返回`true`;否则返回`false`。

### `[constexpr noexcept] qreal &QSizeF::rheight()`

**作用与语义：**

返回高度参考。
使用参考可以直接操作高度。例如：

**官方示例：**

```cpp
 QSizeF size(100, 10.2);
 size.rheight() += 5.5;

 // size becomes (100,15.7)
```

### `[constexpr noexcept] qreal &QSizeF::rwidth()`

**作用与语义：**

返回宽度的参考。
使用参考可以直接操作宽度。例如：

**官方示例：**

```cpp
 QSizeF size(100.3, 10);
 size.rwidth() += 20.5;

 // size becomes (120.8,10)
```

### `[noexcept] void QSizeF::scale(qreal width, qreal height, Qt::AspectRatioMode mode)`

**作用与语义：**

根据指定的`mode`，将大小缩放到带有给定`width`和`height`的矩形。
- 如果`mode` `Qt::IgnoreAspectRatio`，则大小设为（`width`， `height`）。
- 如果`mode` `Qt::KeepAspectRatio`，当前尺寸会被缩放到内部尽可能大的矩形（`width`，`height`），保持宽高比。
- 如果`mode` `Qt::KeepAspectRatioByExpanding`，当前尺寸会被缩放到尽可能小的矩形（`width`，`height`），保持宽高比。

**官方示例：**

```cpp
 QSizeF t1(10, 12);
 t1.scale(60, 60, Qt::IgnoreAspectRatio);
 // t1 is (60, 60)

 QSizeF t2(10, 12);
 t2.scale(60, 60, Qt::KeepAspectRatio);
 // t2 is (50, 60)

 QSizeF t3(10, 12);
 t3.scale(60, 60, Qt::KeepAspectRatioByExpanding);
 // t3 is (60, 72)
```

### `[noexcept] void QSizeF::scale(const QSizeF &size, Qt::AspectRatioMode mode)`

**作用与语义：**

根据指定`mode`，将大小缩放到带有给定`size`的矩形。

### `[noexcept] QSizeF QSizeF::scaled(qreal width, qreal height, Qt::AspectRatioMode mode) const`

**作用与语义：**

返回一个大小，按指定`width`和`height`矩形，根据指定的`mode`返回。

### `[noexcept] QSizeF QSizeF::scaled(const QSizeF &s, Qt::AspectRatioMode mode) const`

**作用与语义：**

返回一个缩放为矩形的大小，大小为`s`，符合指定`mode`。

### `[constexpr noexcept] void QSizeF::setHeight(qreal height)`

**作用与语义：**

将高度设定为给定的有限`height`。

### `[constexpr noexcept] void QSizeF::setWidth(qreal width)`

**作用与语义：**

将宽度设定为给定的有限`width`。

### `[constexpr noexcept] QSizeF QSizeF::shrunkBy(QMarginsF margins) const`

**作用与语义：**

返回将该尺寸缩小`margins`后产生的大小。

### `[noexcept] CGSize QSizeF::toCGSize() const`

**作用与语义：**

从`QSizeF`创建CGSize。

### `[constexpr noexcept] QSize QSizeF::toSize() const`

**作用与语义：**

返回一个基于整数的副本，大小相同。
注意，返回大小中的坐标将四舍五入为最近的整数。

### `[noexcept] void QSizeF::transpose()`

**作用与语义：**

交换宽度和高度值。

### `[constexpr noexcept] QSizeF QSizeF::transposed() const`

**作用与语义：**

返回大小，宽度和高度值互换。

### `[constexpr noexcept] qreal QSizeF::width() const`

**作用与语义：**

返回宽度。

### `[constexpr noexcept] QSizeF &QSizeF::operator*=(qreal factor)`

**作用与语义：**

将宽度和高度乘以给定的有限`factor`，返回大小的参考。

### `[constexpr noexcept] QSizeF &QSizeF::operator+=(const QSizeF &size)`

**作用与语义：**

将给定`size`添加到该大小，并返回该大小的引用。例如：

**官方示例：**

```cpp
 QSizeF s( 3, 7);
 QSizeF r(-1, 4);
 s += r;

 // s becomes (2,11)
```

### `[constexpr noexcept] QSizeF &QSizeF::operator-=(const QSizeF &size)`

**作用与语义：**

从该大小中减去给定`size`，返回该大小的引用。例如：

**官方示例：**

```cpp
 QSizeF s( 3, 7);
 QSizeF r(-1, 4);
 s -= r;

 // s becomes (4,3)
```

### `QSizeF &QSizeF::operator/=(qreal divisor)`

**作用与语义：**

将宽度和高度除以给定`divisor`，返回尺寸的参考。`divisor`不能是零或NaN。

### `[constexpr noexcept, since 6.8] bool qFuzzyCompare(const QSizeF &lhs, const QSizeF &rhs)`

**作用与语义：**

如果 的大小 `lhs` 大约等于 `rhs` 的大小，则返回 `true`;否则返回 `false`。
如果宽度和高度大致相等，则视其尺寸大致相等。

### `[constexpr noexcept, since 6.8] bool qFuzzyIsNull(const QSizeF &size)`

**作用与语义：**

如果尺寸`size`的宽度和高度都近似为零，则返回`true`。

### `[constexpr noexcept] bool operator!=(const QSizeF &lhs, const QSizeF &rhs)`

**作用与语义：**

如果 `lhs` 和 `rhs` 差异足够大，则返回 `true`；否则返回 `false`。
警告：此函数不检查严格不等式；相反，它使用模糊比较来比较尺寸的范围。

### `[constexpr noexcept] QSizeF operator*(const QSizeF &size, qreal factor)`

**作用与语义：**

将给定`size`乘以给定的有限`factor`，返回结果。

### `[constexpr noexcept] QSizeF operator*(qreal factor, const QSizeF &size)`

**作用与语义：**

将给定`size`乘以给定的有限`factor`，返回结果。

### `[constexpr noexcept] QSizeF operator+(const QSizeF &s1, const QSizeF &s2)`

**作用与语义：**

返回`s1`和`s2`的和;每个分量单独相加。

### `[constexpr noexcept] QSizeF operator-(const QSizeF &s1, const QSizeF &s2)`

**作用与语义：**

回报`s2`从`s1`中扣除;每个组成部分单独扣除。

### `QSizeF operator/(const QSizeF &size, qreal divisor)`

**作用与语义：**

将给定`size`除以给定的`divisor`并返回结果。`divisor`不能是零，也不能是NaN。

### `QDataStream &operator<<(QDataStream &stream, const QSizeF &size)`

**作用与语义：**

将给定`size`写入给定`stream`，并返回对流的引用。

### `[constexpr noexcept] bool operator==(const QSizeF &lhs, const QSizeF &rhs)`

**作用与语义：**

如果 `lhs` 和 `rhs` 大致相等，则返回 `true`；否则返回 false。警告：此函数不检查严格相等；相反，它使用模糊比较来比较尺寸的范围。

### `QDataStream &operator>>(QDataStream &stream, QSizeF &size)`

**作用与语义：**

将给定`stream`的大小读取到给定`size`，并返回流的引用。

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

`QSizeF` 所属机制类型：Qt 值类型与隐式共享机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
