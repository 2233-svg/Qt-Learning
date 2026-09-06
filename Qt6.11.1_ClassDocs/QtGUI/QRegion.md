# QRegion

> Qt 6.11.1 · Qt GUI

## 1. 先建立直觉

**一句话定位：** 这是 GUI 基础类型，常用于绘制、输入、图像、字体或窗口系统集成。

**模块背景：** Qt GUI 负责窗口系统集成、绘制、颜色、字体、图像、输入事件和底层 GUI 资源。

### 这是什么

`QRegion` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QRegion>`
- 继承自：未在类页中列出
- 直接派生类：未在类页中列出

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Gui)
target_link_libraries(mytarget PRIVATE Qt6::Gui)
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

- `enum RegionType { Rectangle, Ellipse }`
- `const_iterator`
- `const_reverse_iterator`

### 公有函数

- `QRegion()`
- `QRegion(const QBitmap &bm)`
- `QRegion(const QPolygon &a, Qt::FillRule fillRule = Qt::OddEvenFill)`
- `QRegion(int x, int y, int w, int h, QRegion::RegionType t = Rectangle)`
- `QRegion(const QRect &r, QRegion::RegionType t = Rectangle)`
- `QRegion(const QRegion &r)`
- `QRegion(QRegion &&other)`
- `QRegion::const_iterator begin() const`
- `QRect boundingRect() const`
- `QRegion::const_iterator cbegin() const`
- `QRegion::const_iterator cend() const`
- `bool contains(const QPoint &p) const`
- `bool contains(const QRect &r) const`
- `QRegion::const_reverse_iterator crbegin() const`
- `QRegion::const_reverse_iterator crend() const`
- `QRegion::const_iterator end() const`
- `QRegion intersected(const QRect &rect) const`
- `QRegion intersected(const QRegion &r) const`
- `bool intersects(const QRect &rect) const`
- `bool intersects(const QRegion &region) const`
- `bool isEmpty() const`
- `bool isNull() const`
- `QRegion::const_reverse_iterator rbegin() const`
- `int rectCount() const`
- `(since 6.8) QSpan<const QRect> rects() const`
- `QRegion::const_reverse_iterator rend() const`
- `(since 6.8) void setRects(QSpan<const QRect> rects)`
- `QRegion subtracted(const QRegion &r) const`
- `void swap(QRegion &other)`
- `(since 6.0) HRGN toHRGN() const`
- `void translate(int dx, int dy)`
- `void translate(const QPoint &point)`
- `QRegion translated(int dx, int dy) const`
- `QRegion translated(const QPoint &p) const`
- `QRegion united(const QRect &rect) const`
- `QRegion united(const QRegion &r) const`
- `QRegion xored(const QRegion &r) const`
- `operator QVariant() const`
- `bool operator!=(const QRegion &other) const`
- `QRegion operator&(const QRegion &r) const`
- `QRegion operator&(const QRect &r) const`
- `QRegion & operator&=(const QRegion &r)`
- `QRegion & operator&=(const QRect &r)`
- `QRegion operator+(const QRegion &r) const`
- `QRegion operator+(const QRect &r) const`
- `QRegion & operator+=(const QRect &rect)`
- `QRegion & operator+=(const QRegion &r)`
- `QRegion operator-(const QRegion &r) const`
- `QRegion & operator-=(const QRegion &r)`
- `QRegion & operator=(QRegion &&other)`
- `QRegion & operator=(const QRegion &r)`
- `bool operator==(const QRegion &r) const`
- `QRegion operator^(const QRegion &r) const`
- `QRegion & operator^=(const QRegion &r)`
- `QRegion operator|(const QRegion &r) const`
- `QRegion & operator|=(const QRegion &r)`

### 静态公有成员

- `(since 6.0) QRegion fromHRGN(HRGN hrgn)`

### 相关非成员函数

- `QDataStream & operator<<(QDataStream &s, const QRegion &r)`
- `QDataStream & operator>>(QDataStream &s, QRegion &r)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QRegion::RegionType`

**作用与语义：**

指定要创建区域的形状。
- `QRegion::Rectangle`：`0`;该区域覆盖整个矩形。
- `QRegion::Ellipse`：`1`;该区域是矩形内的一个椭圆。

### `QRegion::const_iterator`

**作用与语义：**

一个迭代器，覆盖构成该区域的非重叠矩形。
所有矩形的并集等于原始区域。
`QRegion`不提供可变迭代器。

### `QRegion::const_reverse_iterator`

**作用与语义：**

对组成该区域的非重叠矩形进行反迭代。
所有矩形的并集等于原始区域。
`QRegion`不提供可变迭代器。

### `QRegion::QRegion()`

**作用与语义：**

构建一个空域。

### `QRegion::QRegion(const QBitmap &bm)`

**作用与语义：**

从位图构建区域`bm`。
最终的区域由位图`bm`中`Qt::color1`的像素组成，就像每个像素是一个1×1的矩形。
该构造器可能会创建复杂的区域，使用时会减缓绘画速度。请注意，使用`QPixmap::setMask()`可以更快地绘制蒙版像素图。

### `QRegion::QRegion(const QPolygon &a, Qt::FillRule fillRule = Qt::OddEvenFill)`

**作用与语义：**

根据`fillRule`指定的填充规则，从点阵列`a`构造一个多边形区域。
如果`fillRule` `Qt::WindingFill`，则使用绕线算法定义多边形区域;如果`Qt::OddEvenFill`，则使用奇偶填充算法。
警告：此构造器可用于创建复杂区域，使用时会减缓绘画速度。

### `QRegion::QRegion(int x, int y, int w, int h, QRegion::RegionType t = Rectangle)`

**作用与语义：**

构造一个矩形或椭圆区域。
如果`t`是`Rectangle`，则该区域是填充矩形（`x`、`y`、`w`、`h`）。如果`t`为`Ellipse`，则该区域是中心为（`x` `w` / 2， `y` `h` / 2）、大小为`w`，`h`的填充椭圆。

### `QRegion::QRegion(const QRect &r, QRegion::RegionType t = Rectangle)`

**作用与语义：**

基于矩形`r`创建一个区域类型`t`的区域。
如果矩形无效，将创建一个空区域。

### `QRegion::QRegion(const QRegion &r)`

**作用与语义：**

构造一个等于区域`r`的新区域。

### `[noexcept] QRegion::QRegion(QRegion &&other)`

**作用与语义：**

从区域`other`移动构建一个新区域。调用后，`other`为空。

### `[noexcept] QRegion::const_iterator QRegion::begin() const`

**作用与语义：**

返回一个指向构成该区域的非重叠矩形范围起点的`const_iterator`。
所有矩形的并集等于原始区域。

### `[noexcept] QRect QRegion::boundingRect() const`

**作用与语义：**

返回该区域的边界矩形。空区域得到一个`QRect::isNull()`矩形。

### `[noexcept] QRegion::const_iterator QRegion::cbegin() const`

**作用与语义：**

和`begin()`一样。

### `[noexcept] QRegion::const_iterator QRegion::cend() const`

**作用与语义：**

和`end()`一样。

### `bool QRegion::contains(const QPoint &p) const`

**作用与语义：**

如果区域包含点`p`，则返回`true`;否则返回`false`。

### `bool QRegion::contains(const QRect &r) const`

**作用与语义：**

如果区域与矩形`r`重叠，返回`true`;否则返回`false`。

### `[noexcept] QRegion::const_reverse_iterator QRegion::crbegin() const`

**作用与语义：**

和`rbegin()`一样。

### `[noexcept] QRegion::const_reverse_iterator QRegion::crend() const`

**作用与语义：**

和`rend()`一样。

### `[noexcept] QRegion::const_iterator QRegion::end() const`

**作用与语义：**

返回一个指向组成该区域的非重叠矩形末端的`const_iterator`。
所有矩形的并集等于原始区域。

### `[static, since 6.0] QRegion QRegion::fromHRGN(HRGN hrgn)`

**作用与语义：**

返回一个等价于给定`hrgn`的`QRegion`。

### `QRegion QRegion::intersected(const QRect &rect) const`

**作用与语义：**

返回一个区域，该区域与给定`rect`的交点。

### `QRegion QRegion::intersected(const QRegion &r) const`

**作用与语义：**

返回一个区域，该区域与`r`的交点。
图中展示了两个椭圆区域的交点。

### `bool QRegion::intersects(const QRect &rect) const`

**作用与语义：**

如果该区域与`rect`相交，返回`true`，否则返回`false`。

### `bool QRegion::intersects(const QRegion &region) const`

**作用与语义：**

如果该区域与`region`相交，返回`true`，否则返回`false`。

### `bool QRegion::isEmpty() const`

**作用与语义：**

如果区域为空，返回`true`;否则返回`false`。空区域是指没有点的区域。

**官方示例：**

```cpp
 QRegion r1(10, 10, 20, 20);
 r1.isEmpty();               // false

 QRegion r3;
 r3.isEmpty();               // true

 QRegion r2(40, 40, 20, 20);
 r3 = r1.intersected(r2);    // r3: intersection of r1 and r2
 r3.isEmpty();               // true

 r3 = r1.united(r2);         // r3: union of r1 and r2
 r3.isEmpty();               // false
```

### `bool QRegion::isNull() const`

**作用与语义：**

如果区域为空，返回`true`;否则返回`false`。空区域是指没有点的区域。该函数与`isEmpty`相同。

### `[noexcept] QRegion::const_reverse_iterator QRegion::rbegin() const`

**作用与语义：**

返回一个指向构成该区域的非重叠矩形范围起点的`const_reverse_iterator`。
所有矩形的并集等于原始区域。

### `[noexcept] int QRegion::rectCount() const`

**作用与语义：**

返回该区域由矩形组成的数量。与`end() - begin()`相同。

### `[noexcept, since 6.8] QSpan<const QRect> QRegion::rects() const`

**作用与语义：**

返回组成该区域的非重叠矩形区间。该区间有效直到下一次对该区域使用变异（非恒定）方法。
所有矩形的并集等于原始区域。
注意：这些功能在Qt 5中也存在，但被恢复`QVector`<`QRect`>。

### `[noexcept] QRegion::const_reverse_iterator QRegion::rend() const`

**作用与语义：**

返回一个指向构成该区域的非重叠矩形范围之外的`const_reverse_iterator`。
所有矩形的并集等于原始区域。

### `[since 6.8] void QRegion::setRects(QSpan<const QRect> rects)`

**作用与语义：**

使用`rects`指定的矩形数组设置区域。矩形必须以Y-X最优排序，并遵循以下限制：
- 矩形不得相交。
- 所有具有给定顶坐标的矩形必须具有相同的高度。
- 不能有两个矩形水平相接（在这种情况下，它们应合并成一个更宽的矩形）。
- 矩形必须按升序排序，以Y为主要排序键，X为次序排序键。
注意：出于历史原因，`rects.size()`必须小于`INT_MAX`（见 `rectCount()`）。

### `QRegion QRegion::subtracted(const QRegion &r) const`

**作用与语义：**

返回一个区域，该区域`r`从该区域减去。
图示右侧椭圆从左侧椭圆中减去（`left - right`）后的结果。

### `[noexcept] void QRegion::swap(QRegion &other)`

**作用与语义：**

将该区域与`other`交换。此操作非常快速且从未失败。

### `[since 6.0] HRGN QRegion::toHRGN() const`

**作用与语义：**

返回的HRGN与给定区域相当。

### `void QRegion::translate(int dx, int dy)`

**作用与语义：**

沿X轴平移（移动）区域沿X轴`dx`，沿Y轴`dy`。

### `void QRegion::translate(const QPoint &point)`

**作用与语义：**

相对于当前位置，沿x轴平移区域`point`.x()，沿y轴平移`point`.y()。正值则使区域向右和向下移动。
相当于给定的 `point`。

### `QRegion QRegion::translated(int dx, int dy) const`

**作用与语义：**

返回一个区域副本，该区域相对于当前位置，沿 x 轴`dx`平移，沿 y 轴`dy`。正值则将区域向右移动并向下移动。

### `QRegion QRegion::translated(const QPoint &p) const`

**作用与语义：**

返回一个矩形副本，x轴平移为`p`.x()，y轴为`p`.y()，相对于当前位置。正值则将矩形向右移动并向下移动。

### `QRegion QRegion::united(const QRect &rect) const`

**作用与语义：**

返回一个区域，该区域是该区域与给定`rect`的联合。

### `QRegion QRegion::united(const QRegion &r) const`

**作用与语义：**

返回一个区域，该区域是该区域与`r`的联合。
图中显示了两个椭圆区域的结合。

### `QRegion QRegion::xored(const QRegion &r) const`

**作用与语义：**

返回一个区域，该区域是该区域和`r`的异或（XOR）。
图中显示了两个椭圆区域的排他或。

### `QRegion::operator QVariant() const`

**作用与语义：**

将该地区作为`QVariant`。

### `bool QRegion::operator!=(const QRegion &other) const`

**作用与语义：**

如果该区域与`other`区域不同，返回`true`;否则返回`false`。

### `QRegion QRegion::operator&(const QRegion &r) const`

**作用与语义：**

将`intersected()`函数应用于该区域和`r`。`r1&r2`等价于`r1.intersected(r2)`。

### `QRegion QRegion::operator&(const QRect &r) const`

**作用与语义：**

将`intersected()`函数应用于该区域和`r`。`r1&r2`等价于`r1.intersected(r2)`。

### `QRegion &QRegion::operator&=(const QRegion &r)`

**作用与语义：**

将`intersected()`函数应用于该区域和`r`，并将结果分配到该区域。`r1&=r2`等价于`r1` = r1。Intersected（r²）。

### `QRegion &QRegion::operator&=(const QRect &r)`

**作用与语义：**

将`intersected()`函数应用于该区域和`r`，并将结果分配到该区域。`r1&=r2`等价于`r1` = r1。Intersected（r²）。

### `QRegion QRegion::operator+(const QRegion &r) const`

**作用与语义：**

将`united()`函数应用于该区域和`r`。`r1+r2`等价于`r1.united(r2)`。

### `QRegion QRegion::operator+(const QRect &r) const`

**作用与语义：**

将`united()`函数应用于该区域和`r`。`r1+r2`等价于`r1.united(r2)`。

### `QRegion &QRegion::operator+=(const QRect &rect)`

**作用与语义：**

返回一个区域，该区域与指定`rect`的并集。

### `QRegion &QRegion::operator+=(const QRegion &r)`

**作用与语义：**

将`united()`函数应用于该区域和`r`，并将结果分配到该区域。`r1+=r2`等价于`r1 = r1.united(r2)`。

### `QRegion QRegion::operator-(const QRegion &r) const`

**作用与语义：**

将`subtracted()`函数应用于该区域和`r`。`r1-r2`等价于`r1.subtracted(r2)`。

### `QRegion &QRegion::operator-=(const QRegion &r)`

**作用与语义：**

将`subtracted()`函数应用于该区域和`r`，并将结果分配到该区域。`r1-=r2`等价于`r1 = r1.subtracted(r2)`。

### `[noexcept] QRegion &QRegion::operator=(QRegion &&other)`

**作用与语义：**

Move-assign `other`到该`QRegion`实例。

### `QRegion &QRegion::operator=(const QRegion &r)`

**作用与语义：**

将`r`分配到该区域并返回该区域的引用。

### `bool QRegion::operator==(const QRegion &r) const`

**作用与语义：**

如果区域等于 `r`，则返回 `true`;否则返回 false。

### `QRegion QRegion::operator^(const QRegion &r) const`

**作用与语义：**

将`xored()`函数应用于该区域和`r`。`r1^r2`等价于`r1.xored(r2)`。

### `QRegion &QRegion::operator^=(const QRegion &r)`

**作用与语义：**

将`xored()`函数应用于该区域和`r`，并将结果分配到该区域。`r1^=r2`等价于`r1 = r1.xored(r2)`。

### `QRegion QRegion::operator|(const QRegion &r) const`

**作用与语义：**

将`united()`函数应用于该区域和`r`。`r1|r2`等价于`r1.united(r2)`。

### `QRegion &QRegion::operator|=(const QRegion &r)`

**作用与语义：**

将`united()`函数应用于该区域和`r`，并将结果分配到该区域。`r1|=r2`等价于`r1 = r1.united(r2)`。

### `QDataStream &operator<<(QDataStream &s, const QRegion &r)`

**作用与语义：**

将区域`r`写入流`s`并返回流的引用。

### `QDataStream &operator>>(QDataStream &s, QRegion &r)`

**作用与语义：**

读取流`s`的区域到`r`并返回流的引用。

### `const_iterator`

**作用与语义：**

一个迭代器，覆盖构成该区域的非重叠矩形。
所有矩形的并集等于原始区域。
`QRegion`不提供可变迭代器。

### `const_reverse_iterator`

**作用与语义：**

对组成该区域的非重叠矩形进行反迭代。
所有矩形的并集等于原始区域。
`QRegion`不提供可变迭代器。

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

`QRegion` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
