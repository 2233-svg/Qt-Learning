# QBoxSet

> Qt 6.11.1 · Qt Charts

## 1. 先建立直觉

**一句话定位：** `QBoxSet` 是 Qt 对象机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Charts 提供折线、柱状、饼图、散点图和坐标轴等数据可视化组件。

### 这是什么

`QBoxSet` 是 Qt 对象机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

**适用场景：** 使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

## 2. 依赖与对象关系

- 头文件：`#include <QBoxSet>`
- 继承自：QObject
- 直接派生类：未在类页中列出

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

### 状态、生命周期和线程

**生命周期：** 先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

**状态与结果：** QObject 派生对象的状态通常通过属性、状态查询函数和信号变化共同表达。信号是通知，不是返回值；收到通知后应读取当前状态并处理异常路径，不能假设每个信号只会出现一次。

**线程与事件循环：** QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

## 3. 直接使用

使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。 使用时通常按这个过程组织：准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum ValuePositions { LowerExtreme, LowerQuartile, Median, UpperQuartile, UpperExtreme }`

### 属性

- `brush : QBrush`
- `pen : QPen`

### 公有函数

- `QBoxSet(const QString label = QString(), QObject *parent = nullptr)`
- `QBoxSet(const qreal le, const qreal lq, const qreal m, const qreal uq, const qreal ue, const QString label = QString(), QObject *parent = nullptr)`
- `virtual ~QBoxSet()`
- `void append(const QList<qreal> &values)`
- `void append(const qreal value)`
- `qreal at(const int index) const`
- `QBrush brush() const`
- `void clear()`
- `int count() const`
- `QString label() const`
- `QPen pen() const`
- `void setBrush(const QBrush &brush)`
- `void setLabel(const QString label)`
- `void setPen(const QPen &pen)`
- `void setValue(const int index, const qreal value)`
- `QBoxSet & operator<<(const qreal &value)`
- `qreal operator[](const int index) const`

### 信号

- `void brushChanged()`
- `void cleared()`
- `void clicked()`
- `void doubleClicked()`
- `void hovered(bool status)`
- `void penChanged()`
- `void pressed()`
- `void released()`
- `void valueChanged(int index)`
- `void valuesChanged()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QBoxSet::ValuePositions`

**作用与语义：**

该枚举类型定义了框须项的值：
- `QBoxSet::LowerExtreme`：`0`;盒子和胡须物品的最小值。
- `QBoxSet::LowerQuartile`：`1`;方框和胡须物品下半部分的中位数值。
- `QBoxSet::Median`：`2`;方框和胡须物品的中位数值。
- `QBoxSet::UpperQuartile`：`3`;方框胡须条目的上半部分的中位数值。
- `QBoxSet::UpperExtreme`：`4`;箱子和胡须物品的最大值。

### `brush : QBrush`

**作用与语义：**

该属性使所用画刷填满盒子和胡须物品的盒子。

**如何使用：** 调用 `brush()` 读取当前值；它不会修改应用状态。

### `pen : QPen`

**作用与语义：**

该属性包含用于绘制方框与胡须物品线条的笔。

**如何使用：** 调用 `pen()` 读取当前值；它不会修改应用状态。

### `[explicit] QBoxSet::QBoxSet(const QString label = QString(), QObject *parent = nullptr)`

**作用与语义：**

构造一个带有可选标签`label`和父`parent`的方框和胡须条目。

### `[explicit] QBoxSet::QBoxSet(const qreal le, const qreal lq, const qreal m, const qreal uq, const qreal ue, const QString label = QString(), QObject *parent = nullptr)`

**作用与语义：**

构造一个框状和胡须项，具有以下有序值：`le`指定下极值，`lq`下四分位数，`m`中位数，`uq`上四分位数，`ue`上四分位数。可选地，可以指定`label`和`parent`。

### `[virtual noexcept] QBoxSet::~QBoxSet()`

**作用与语义：**

摧毁了那个盒子和胡须的物品。

### `void QBoxSet::append(const QList<qreal> &values)`

**作用与语义：**

在方框和胡须条目末尾附加由`values`指定的实数值列表。

### `void QBoxSet::append(const qreal value)`

**作用与语义：**

将`value`指定的新值附加到方框和胡须条目的末尾。

### `qreal QBoxSet::at(const int index) const`

**作用与语义：**

返回由 `index` 指定的方框和胡须项的值。索引可以通过`ValuePositions`枚举值来指定。如果索引超出界限，返回 0.0。

### `QBrush QBoxSet::brush() const`

**作用与语义：**

归还用来填满箱子和胡须物品的画刷。
注意：属性画刷的获取函数。

### `[signal] void QBoxSet::brushChanged()`

**作用与语义：**

该属性使所用画刷填满盒子和胡须物品的盒子。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `brush` 的变化，不要把它当作普通函数主动调用。

### `void QBoxSet::clear()`

**作用与语义：**

将所有框须条目值设为0。

### `[signal] void QBoxSet::cleared()`

**作用与语义：**

当所有方框和胡须物品的值都设为0时，该信号会发出。

### `[signal] void QBoxSet::clicked()`

**作用与语义：**

当用户点击图表中的方框和胡须条目时，会发出该信号。

### `int QBoxSet::count() const`

**作用与语义：**

返回附加在方框和胡须条目上的数值。

### `[signal] void QBoxSet::doubleClicked()`

**作用与语义：**

当用户双击框框和胡须物品时，会发出该信号。

### `[signal] void QBoxSet::hovered(bool status)`

**作用与语义：**

当鼠标悬停在图表中的方须条纹上时，该信号会发出。当鼠标移动到该项上时，`status`转为`true`;当鼠标再次移开时，`false`转。

### `QString QBoxSet::label() const`

**作用与语义：**

返回盒子和胡须物品类别的标签。

### `QPen QBoxSet::pen() const`

**作用与语义：**

归还用于绘制盒状胡须物品的笔。
注意：属性笔的获取函数。

### `[signal] void QBoxSet::penChanged()`

**作用与语义：**

该属性包含用于绘制方框与胡须物品线条的笔。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `pen` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QBoxSet::pressed()`

**作用与语义：**

当用户点击图表中的方框和胡须条目并按住鼠标按钮时，会发出该信号。

### `[signal] void QBoxSet::released()`

**作用与语义：**

当用户松开鼠标按压在方框和胡须物品上时，会发出该信号。

### `void QBoxSet::setBrush(const QBrush &brush)`

**作用与语义：**

该属性使所用画刷填满盒子和胡须物品的盒子。

**如何使用：** 调用 `setBrush(...)` 修改 `brush`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QBoxSet::setLabel(const QString label)`

**作用与语义：**

设置`label`指定标签，用于箱子和胡须物品的类别。

### `void QBoxSet::setPen(const QPen &pen)`

**作用与语义：**

该属性包含用于绘制方框与胡须物品线条的笔。

**如何使用：** 调用 `setPen(...)` 修改 `pen`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QBoxSet::setValue(const int index, const qreal value)`

**作用与语义：**

在`index`指定的位置上设置`value`指定的值。索引可以通过`ValuePositions`枚举值来指定。

### `[signal] void QBoxSet::valueChanged(int index)`

**作用与语义：**

当`index`指定的方框和胡须物品的价值被修改时，会发出该信号。

### `[signal] void QBoxSet::valuesChanged()`

**作用与语义：**

当箱子和胡须物品的多个值发生变化时，会发出该信号。

### `QBoxSet &QBoxSet::operator<<(const qreal &value)`

**作用与语义：**

一个方便算子，用于将`value`指定的实值附加到框须条目的末尾。

### `qreal QBoxSet::operator[](const int index) const`

**作用与语义：**

返回由 `index` 指定的方框和胡须项的值。索引可以通过`ValuePositions`枚举值来指定。如果索引超出界限，返回 0.0。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

### 状态和错误边界

QObject 派生对象的状态通常通过属性、状态查询函数和信号变化共同表达。信号是通知，不是返回值；收到通知后应读取当前状态并处理异常路径，不能假设每个信号只会出现一次。

### 线程边界

QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

### 最容易出现的错误

不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QBoxSet` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
