# QEasingCurve

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** 这是 Qt Core 中围绕“EasingCurve”职责设计的公开 C++ 类型，先从输入、输出、生命周期和它与相邻类型的协作关系入手。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QEasingCurve` 是 Qt 类型机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这个类的行为由它的继承关系、构造参数、公开状态和成员函数协议共同决定。使用时要把创建、配置、核心操作、结果/通知和清理看成一条闭环，而不是孤立调用某个函数。

**适用场景：** 围绕这个类的核心职责建立最小闭环：准备依赖 -> 创建/取得对象 -> 设置必要配置 -> 调用核心 API -> 检查返回值和状态 -> 处理结果/错误 -> 结束时清理。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不要忽略构造失败、空返回、默认值和版本限制；不要把异步 API 当同步 API；不要在没有确认所有权和线程的情况下保存指针或跨线程调用。

## 2. 依赖与对象关系

- 头文件：`#include <QEasingCurve>`
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

- `EasingFunction`
- `enum Type { Linear, InQuad, OutQuad, InOutQuad, OutInQuad, …, Custom }`

### 公有函数

- `QEasingCurve(QEasingCurve::Type type = Linear)`
- `QEasingCurve(const QEasingCurve &other)`
- `QEasingCurve(QEasingCurve &&other)`
- `~QEasingCurve()`
- `void addCubicBezierSegment(const QPointF &c1, const QPointF &c2, const QPointF &endPoint)`
- `void addTCBSegment(const QPointF &nextPoint, qreal t, qreal c, qreal b)`
- `qreal amplitude() const`
- `QEasingCurve::EasingFunction customType() const`
- `qreal overshoot() const`
- `qreal period() const`
- `void setAmplitude(qreal amplitude)`
- `void setCustomType(QEasingCurve::EasingFunction func)`
- `void setOvershoot(qreal overshoot)`
- `void setPeriod(qreal period)`
- `void setType(QEasingCurve::Type type)`
- `void swap(QEasingCurve &other)`
- `QList<QPointF> toCubicSpline() const`
- `QEasingCurve::Type type() const`
- `qreal valueForProgress(qreal progress) const`
- `QEasingCurve & operator=(QEasingCurve &&other)`
- `QEasingCurve & operator=(const QEasingCurve &other)`

### 相关非成员函数

- `bool operator!=(const QEasingCurve &lhs, const QEasingCurve &rhs)`
- `QDataStream & operator<<(QDataStream &stream, const QEasingCurve &easing)`
- `bool operator==(const QEasingCurve &lhs, const QEasingCurve &rhs)`
- `QDataStream & operator>>(QDataStream &stream, QEasingCurve &easing)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `QEasingCurve::EasingFunction`

**作用与语义：**

这是指向函数签名如下的指针的类型def：

**官方示例：**

```cpp
 qreal myEasingFunction(qreal progress);
```

### `enum QEasingCurve::Type`

**作用与语义：**

缓解曲线的类型。
- `QEasingCurve::Linear`：`0`
线性（t）函数的缓解曲线：速度恒定。
- `QEasingCurve::InQuad`：`1`
二次（t^2）函数的松弛曲线：从零速度加速。
- `QEasingCurve::OutQuad`：`2`
二次函数（t^2）的缓曲线：减速至零速度。
- `QEasingCurve::InOutQuad`：`3`
二次函数（t^2）的缓曲线：先加速到一半，然后减速。
- `QEasingCurve::OutInQuad`：`4`
二次函数（t^2）的缓和曲线：减速至一半，然后加速。
- `QEasingCurve::InCubic`：`5`
三次曲线（t^3）函数的松弛曲线：从零速度加速。
- `QEasingCurve::OutCubic`：`6`
立方（t^3）函数的松动曲线：减速至零速度。
- `QEasingCurve::InOutCubic`：`7`
三次曲线（t^3）函数的缓曲线：加速至一半，然后减速。
- `QEasingCurve::OutInCubic`：`8`
三次（t^3）函数的缓曲线：减速至一半，然后加速。
- `QEasingCurve::InQuart`：`9`
四次函数（t^4）的缓和曲线：从零速度加速。
- `QEasingCurve::OutQuart`：`10`
四次函数（t^4）的缓和曲线：减速至零速度。
- `QEasingCurve::InOutQuart`：`11`
四次函数（t^4）的松弛曲线：加速至一半，然后减速。
- `QEasingCurve::OutInQuart`：`12`
四次函数（t^4）的松弛曲线：减速至一半，然后加速。
- `QEasingCurve::InQuint`：`13`
五次进度（t^5）缓进的松动曲线：从零速度加速。
- `QEasingCurve::OutQuint`：`14`
五次函数（t^5）的缓解曲线：减速至零速度。
- `QEasingCurve::InOutQuint`：`15`
五次函数（t^5）的缓和曲线：加速至一半，然后减速。
- `QEasingCurve::OutInQuint`：`16`
五次函数（t^5）的松曲线：减速至一半，然后加速。
- `QEasingCurve::InSine`：`17`
正弦函数（sin（t））的缓和曲线：从零速度加速。
- `QEasingCurve::OutSine`：`18`
正弦（sin（t））函数的缓曲线：减速至零速度。
- `QEasingCurve::InOutSine`：`19`
正弦（sin（t））函数的缓曲线：加速至一半，然后减速。
- `QEasingCurve::OutInSine`：`20`
正弦函数（sin（t））的缓和曲线：减速至一半，然后加速。
- `QEasingCurve::InExpo`：`21`
指数（2^t）函数的缓和曲线：从零速度加速。
- `QEasingCurve::OutExpo`：`22`
指数函数（2^t）的缓曲线：减速至零速度。
- `QEasingCurve::InOutExpo`：`23`
指数（2^t）函数的缓曲线：加速至一半，然后减速。
- `QEasingCurve::OutInExpo`：`24`
指数（2^t）函数的宽曲线：减速至一半，然后加速度。
- `QEasingCurve::InCirc`：`25`
圆形（sqrt（1-t^2））函数的缓和曲线：从零速度加速。
- `QEasingCurve::OutCirc`：`26`
圆（sqrt（1-t^2））函数的缓曲线：减速至零速度。
- `QEasingCurve::InOutCirc`：`27`
圆（sqrt（1-t^2））函数的缓曲线：先加速至一半，然后减速。
- `QEasingCurve::OutInCirc`：`28`
圆形（sqrt（1-t^2））函数的缓曲线：减速至一半，然后加速。
- `QEasingCurve::InElastic`：`29`
弹性（指数衰减正弦波）函数的缓解曲线：从零速度加速。峰值振幅可以用振幅参数设定，衰减周期用周期参数来设定。
- `QEasingCurve::OutElastic`：`30`
弹性（指数衰减正弦波）函数的缓解曲线：减速至零速度。峰值振幅可以用振幅参数设定，衰减周期用周期参数来设定。
- `QEasingCurve::InOutElastic`：`31`
弹性（指数衰减正弦波）函数的缓曲线：加速至一半，然后减速。
- `QEasingCurve::OutInElastic`：`32`
弹性（指数衰减正弦波）函数的缓解曲线：减速至一半，然后加速。
- `QEasingCurve::InBack`：`33`
后退的缓进曲线（超速三次函数：（s 1）*t^3 - s*t^2）缓进：从零速度加速。
- `QEasingCurve::OutBack`：`34`
后退的缓曲线（超速三次函数：（s 1）*t^3 - s*t^2）缓缓出：减速至零速度。
- `QEasingCurve::InOutBack`：`35`
InOutBack 函数}。
后退的缓进曲线（超速三次函数：（s 1）*t^3 - s*t^2）缓进/出：加速至半程，然后减速。
- `QEasingCurve::OutInBack`：`36`
后退的缓曲线（超速立方缓进：（s 1）*t^3 - s*t^2）缓缓出/入：减速至半程，然后加速。
- `QEasingCurve::InBounce`：`37`
对于一个反弹函数（指数衰减抛物线反弹）的缓曲线：从零速度加速。
- `QEasingCurve::OutBounce`：`38`
反弹（指数衰减抛物线弹跳）函数的缓和曲线：从零速度减速。
- `QEasingCurve::InOutBounce`：`39`
对于反弹（指数衰减抛物线弹跳）函数的缓进/缓出：加速到一半，然后减速。
- `QEasingCurve::OutInBounce`：`40`
对于反弹（指数衰减抛物线反弹）函数的缓进曲线：减速至一半，然后加速。
- `QEasingCurve::BezierSpline`：`45`;允许使用三次贝塞尔样条定义自定义的松弛曲线
- `QEasingCurve::TCBSpline`：`46`;允许使用TCB样条定义自定义的松弛曲线
- `QEasingCurve::Custom`：`47`;如果用户指定了带有`setCustomType()`的自定义曲线类型，则返回此值。注意你不能用此值调用`setType()`，但`type()`可以返回。

### `QEasingCurve::QEasingCurve(QEasingCurve::Type type = Linear)`

**作用与语义：**

构造给定`type`的宽松曲线。

### `QEasingCurve::QEasingCurve(const QEasingCurve &other)`

**作用与语义：**

构建一份`other`的副本。

### `[noexcept] QEasingCurve::QEasingCurve(QEasingCurve &&other)`

**作用与语义：**

Move-构造一个QEasingCurve实例，使其指向`other`指向的同一个对象。

### `[noexcept] QEasingCurve::~QEasingCurve()`

**作用与语义：**

毁灭者。

### `void QEasingCurve::addCubicBezierSegment(const QPointF &c1, const QPointF &c2, const QPointF &endPoint)`

**作用与语义：**

添加一个三次贝塞尔样条的一段以定义自定义的缓解曲线。仅当`type()`为`QEasingCurve::BezierSpline`时才适用。注意，样条线隐式从（0.0， 0.0）开始，必须在（1.0， 1.0）结束，才能成为有效的缓解曲线。`c1`和`c2`是用于绘制曲线的控制点。`endPoint`是曲线的端点。

### `void QEasingCurve::addTCBSegment(const QPointF &nextPoint, qreal t, qreal c, qreal b)`

**作用与语义：**

添加 TCB 贝塞尔样条的一段以定义自定义的缓解曲线。仅在 `type()` `QEasingCurve::TCBSpline`时适用。样条必须明确从（0.0， 0.0）开始，且终止于（1.0， 1.0），才能成为有效的缓解曲线。张力`t`改变切向量的长度。连续性`c`改变切线之间变化的锐利度。偏置`b`改变切向量的方向。`nextPoint` 是样本位置。这三个参数均有效于-1和1之间，并定义了控制点的切线。如果三个参数都是0，则得到的样条是Catmull-Rom样条。起点和终点总是偏向-1和1，因为外切线未定义。

### `qreal QEasingCurve::amplitude() const`

**作用与语义：**

返回振幅。这并不适用于所有曲线类型。它仅适用于反弹和弹性曲线（`type()` `QEasingCurve::InBounce`、`QEasingCurve::OutBounce`、`QEasingCurve::InOutBounce`、`QEasingCurve::OutInBounce`、`QEasingCurve::InElastic`、`QEasingCurve::OutElastic`、`QEasingCurve::InOutElastic`或`QEasingCurve::OutInElastic`曲线）。

### `QEasingCurve::EasingFunction QEasingCurve::customType() const`

**作用与语义：**

返回自定义缓解曲线的函数指针。如果`type()`不返回`QEasingCurve::Custom`，该函数返回0。

### `qreal QEasingCurve::overshoot() const`

**作用与语义：**

返回超冲。这并不适用于所有曲线类型。仅当`type()`为`QEasingCurve::InBack`、`QEasingCurve::OutBack`、`QEasingCurve::InOutBack`或`QEasingCurve::OutInBack`时才适用。

### `qreal QEasingCurve::period() const`

**作用与语义：**

返回周期。这不适用于所有曲线类型。仅在`type()`为`QEasingCurve::InElastic`、`QEasingCurve::OutElastic`、`QEasingCurve::InOutElastic`或`QEasingCurve::OutInElastic`时适用。

### `void QEasingCurve::setAmplitude(qreal amplitude)`

**作用与语义：**

把振幅设为`amplitude`。
这将设定弹跳幅度或弹性“弹簧”效应的幅度。数字越大，幅度越大。

### `void QEasingCurve::setCustomType(QEasingCurve::EasingFunction func)`

**作用与语义：**

设置一个自定义的易度曲线，由用户在函数 `func` 中定义。函数的签名是 qreal myEasingFunction（qreal progress），其中进度和返回值被视为在 0 到 1 之间归一化。（在某些情况下，返回值可能超出该范围）调用该函数后，`type()` 返回 `QEasingCurve::Custom`。`func` 无法`nullptr`。

### `void QEasingCurve::setOvershoot(qreal overshoot)`

**作用与语义：**

将超跃设为`overshoot`。
0不会产生超调，默认值1.70158会产生10%的超调。

### `void QEasingCurve::setPeriod(qreal period)`

**作用与语义：**

将周期设置为`period`。设置小周期值会获得曲线的高频率。较大的周期会得到较小的频率。

### `void QEasingCurve::setType(QEasingCurve::Type type)`

**作用与语义：**

将宽松曲线类型设置为`type`。

### `[noexcept] void QEasingCurve::swap(QEasingCurve &other)`

**作用与语义：**

将该曲线与`other`交换。该操作非常快速且从未失效。

### `QList<QPointF> QEasingCurve::toCubicSpline() const`

**作用与语义：**

返回定义自定义宽松曲线的立方贝塞尔Spline。如果宽松曲线没有自定义贝塞尔宽松曲线，列表为空。

### `QEasingCurve::Type QEasingCurve::type() const`

**作用与语义：**

返回宽松曲线的类型。

### `qreal QEasingCurve::valueForProgress(qreal progress) const`

**作用与语义：**

返回`progress`处缓和曲线的有效进度。虽然 的 变`progress`必须介于 0 和 1 之间，但返回的有效进度可能超出该范围。例如，`QEasingCurve::InBack` 在函数开头会返回负值。

### `[noexcept] QEasingCurve &QEasingCurve::operator=(QEasingCurve &&other)`

**作用与语义：**

Move-assign `other` 到该`QEasingCurve`实例。

### `QEasingCurve &QEasingCurve::operator=(const QEasingCurve &other)`

**作用与语义：**

收到`other`。

### `[noexcept] bool operator!=(const QEasingCurve &lhs, const QEasingCurve &rhs)`

**作用与语义：**

比较宽松曲线`lhs`与`rhs`，如果不相等则返回`true`;否则返回`false`。它还会比较曲线的属性。

### `QDataStream &operator<<(QDataStream &stream, const QEasingCurve &easing)`

**作用与语义：**

将给定的`easing`曲线写入给定的`stream`，并返回对流的引用。
警告：不支持`QEasingCurve::Custom`类型的宽松曲线（即带有自定义宽松函数的曲线）。

### `[noexcept] bool operator==(const QEasingCurve &lhs, const QEasingCurve &rhs)`

**作用与语义：**

比较宽松曲线`lhs`与`rhs`，如果相等`true`回报;否则返回`false`。它还会比较曲线的属性。

### `QDataStream &operator>>(QDataStream &stream, QEasingCurve &easing)`

**作用与语义：**

将给定`stream`的缓曲线读取到给定的`easing`曲线，并返回对该流的引用。

### `EasingFunction`

**作用与语义：**

这是指向函数签名如下的指针的类型def：

**官方示例：**

```cpp
 qreal myEasingFunction(qreal progress);
```

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

`QEasingCurve` 所属机制类型：Qt 类型机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
