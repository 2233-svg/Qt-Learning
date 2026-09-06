# QBoxPlotSeries

> Qt 6.11.1 · Qt Charts

## 1. 先建立直觉

**一句话定位：** `QBoxPlotSeries` 是 Qt 对象机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Charts 提供折线、柱状、饼图、散点图和坐标轴等数据可视化组件。

### 这是什么

`QBoxPlotSeries` 是 Qt 对象机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

**适用场景：** 使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

## 2. 依赖与对象关系

- 头文件：`#include <QBoxPlotSeries>`
- 继承自：QAbstractSeries
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

### 属性

- `boxOutlineVisible : bool`
- `boxWidth : qreal`
- `brush : QBrush`
- `count : int`
- `pen : QPen`

### 公有函数

- `QBoxPlotSeries(QObject *parent = nullptr)`
- `virtual ~QBoxPlotSeries()`
- `bool append(QBoxSet *set)`
- `bool append(const QList<QBoxSet *> &sets)`
- `bool boxOutlineVisible()`
- `QList<QBoxSet *> boxSets() const`
- `qreal boxWidth()`
- `QBrush brush() const`
- `void clear()`
- `int count() const`
- `bool insert(int index, QBoxSet *set)`
- `QPen pen() const`
- `bool remove(QBoxSet *set)`
- `void setBoxOutlineVisible(bool visible)`
- `void setBoxWidth(qreal width)`
- `void setBrush(const QBrush &brush)`
- `void setPen(const QPen &pen)`
- `bool take(QBoxSet *set)`

### 重实现的公有函数

- `virtual QAbstractSeries::SeriesType type() const override`

### 信号

- `void boxOutlineVisibilityChanged()`
- `void boxWidthChanged()`
- `void boxsetsAdded(const QList<QBoxSet *> &sets)`
- `void boxsetsRemoved(const QList<QBoxSet *> &sets)`
- `void brushChanged()`
- `void clicked(QBoxSet *boxset)`
- `void countChanged()`
- `void doubleClicked(QBoxSet *boxset)`
- `void hovered(bool status, QBoxSet *boxset)`
- `void penChanged()`
- `void pressed(QBoxSet *boxset)`
- `void released(QBoxSet *boxset)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `boxOutlineVisible : bool`

**作用与语义：**

该属性保留了盒子轮廓的可见性。

**如何使用：** 调用 `boxOutlineVisible()` 读取当前值；它不会修改应用状态。

### `boxWidth : qreal`

**作用与语义：**

该属性包含箱子和胡须物品的宽度。该值表示该物品在其类别内的相对宽度。值可以介于0.0到1.0之间。负值被替换为0.0，大于1.0的值被替换为1.0。

**如何使用：** 调用 `boxWidth()` 读取当前值；它不会修改应用状态。

### `brush : QBrush`

**作用与语义：**

该特性用于填充箱子和胡须物品的画刷。

**如何使用：** 调用 `brush()` 读取当前值；它不会修改应用状态。

### `[read-only] count : int`

**作用与语义：**

此属性保存箱形图系列中箱线统计项目的数量。

**如何使用：** 调用 `count()` 读取当前值；它不会修改应用状态。

### `pen : QPen`

**作用与语义：**

该属性包含用于绘制盒子和胡须物品线条的笔。

**如何使用：** 调用 `pen()` 读取当前值；它不会修改应用状态。

### `[explicit] QBoxPlotSeries::QBoxPlotSeries(QObject *parent = nullptr)`

**作用与语义：**

构建了一个空洞的盒子剧情系列，既是`QObject`，也是`parent`的产物。

### `[virtual noexcept] QBoxPlotSeries::~QBoxPlotSeries()`

**作用与语义：**

将该系列从图表中移除。

### `bool QBoxPlotSeries::append(QBoxSet *set)`

**作用与语义：**

将`set`指定的单个方框和胡须条项加入序列并取得其所有权。如果该项为空或已属于该序列，则不会被附加。如果附加成功，返回`true`。

### `bool QBoxPlotSeries::append(const QList<QBoxSet *> &sets)`

**作用与语义：**

将`sets`指定的方框和胡须条目列表添加到系列中并取得它们的所有权。如果列表为空或该项已属于该系列，则不会被添加。如果附加成功，返回 `true`。

### `[signal] void QBoxPlotSeries::boxOutlineVisibilityChanged()`

**作用与语义：**

该属性保留了盒子轮廓的可见性。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `boxOutlineVisible` 的变化，不要把它当作普通函数主动调用。

### `QList<QBoxSet *> QBoxPlotSeries::boxSets() const`

**作用与语义：**

返回箱型图系列中的箱型物品清单。保留物品的所有权。

### `[signal] void QBoxPlotSeries::boxWidthChanged()`

**作用与语义：**

该属性包含箱子和胡须物品的宽度。该值表示该物品在其类别内的相对宽度。值可以介于0.0到1.0之间。负值被替换为0.0，大于1.0的值被替换为1.0。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `boxWidth` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QBoxPlotSeries::boxsetsAdded(const QList<QBoxSet *> &sets)`

**作用与语义：**

当`sets`指定的盒状和胡须条目列表加入系列时，会发出该信号。

### `[signal] void QBoxPlotSeries::boxsetsRemoved(const QList<QBoxSet *> &sets)`

**作用与语义：**

当`sets`指定的方框和胡须条目列表从系列中移除时，该信号会发出。

### `[signal] void QBoxPlotSeries::brushChanged()`

**作用与语义：**

该特性用于填充箱子和胡须物品的画刷。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `brush` 的变化，不要把它当作普通函数主动调用。

### `void QBoxPlotSeries::clear()`

**作用与语义：**

移除系列中所有箱子和胡须相关的物品并永久删除。

### `[signal] void QBoxPlotSeries::clicked(QBoxSet *boxset)`

**作用与语义：**

当用户点击图表中`boxset`指定的方框和胡须条目时，会发出该信号。

### `int QBoxPlotSeries::count() const`

**作用与语义：**

返回箱形图系列中的箱子和胡须物品数量。
注意：属性计数的获取函数。

### `[signal] void QBoxPlotSeries::countChanged()`

**作用与语义：**

此属性保存箱形图系列中箱线统计项目的数量。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `count` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QBoxPlotSeries::doubleClicked(QBoxSet *boxset)`

**作用与语义：**

当用户双击图表中`boxset`指定的方框和胡须条目时，会发出该信号。

### `[signal] void QBoxPlotSeries::hovered(bool status, QBoxSet *boxset)`

**作用与语义：**

当鼠标悬停在图表中`boxset`指定的方框和胡须条上时，该信号会发出。当鼠标移动到该项上时，`status`转为`true`;当鼠标再次移开时，`false`转。

### `bool QBoxPlotSeries::insert(int index, QBoxSet *set)`

**作用与语义：**

在`index`指定位置插入由`set`指定的方框和胡须条目到序列中，并取得该条目的所有权。如果该条目为空或已属于该序列，则不会被附加。插入成功时返回`true`。

### `[signal] void QBoxPlotSeries::penChanged()`

**作用与语义：**

该属性包含用于绘制盒子和胡须物品线条的笔。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `pen` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QBoxPlotSeries::pressed(QBoxSet *boxset)`

**作用与语义：**

当用户点击图表中`boxset`指定的方框和胡须条目并按住鼠标按钮时，会发出该信号。

### `[signal] void QBoxPlotSeries::released(QBoxSet *boxset)`

**作用与语义：**

当用户松开鼠标按压图表中`boxset`指定的方须条时，该信号会发出。

### `bool QBoxPlotSeries::remove(QBoxSet *set)`

**作用与语义：**

移除`set`指定的框状物品，若移除成功则永久删除。返回`true`物品被移除。

### `bool QBoxPlotSeries::take(QBoxSet *set)`

**作用与语义：**

取`set`从系列中指定的方框和胡须物品。不删除该物品。
注意：该系列仍然是该物品的父对象。您必须设置父对象获得全部所有权。
如果take操作成功，返回`true`。

### `[override virtual] QAbstractSeries::SeriesType QBoxPlotSeries::type() const`

**作用与语义：**

重新实现属性访问函数：`QAbstractSeries::type`。
回归系列类型。

### `bool boxOutlineVisible()`

**作用与语义：**

该属性保留了盒子轮廓的可见性。

**如何使用：** 调用 `boxOutlineVisible()` 读取当前值；它不会修改应用状态。

### `qreal boxWidth()`

**作用与语义：**

该属性包含箱子和胡须物品的宽度。该值表示该物品在其类别内的相对宽度。值可以介于0.0到1.0之间。负值被替换为0.0，大于1.0的值被替换为1.0。

**如何使用：** 调用 `boxWidth()` 读取当前值；它不会修改应用状态。

### `QBrush brush() const`

**作用与语义：**

该特性用于填充箱子和胡须物品的画刷。

**如何使用：** 调用 `brush()` 读取当前值；它不会修改应用状态。

### `QPen pen() const`

**作用与语义：**

该属性包含用于绘制盒子和胡须物品线条的笔。

**如何使用：** 调用 `pen()` 读取当前值；它不会修改应用状态。

### `void setBoxOutlineVisible(bool visible)`

**作用与语义：**

该属性保留了盒子轮廓的可见性。

**如何使用：** 调用 `setBoxOutlineVisible(...)` 修改 `boxOutlineVisible`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setBoxWidth(qreal width)`

**作用与语义：**

该属性包含箱子和胡须物品的宽度。该值表示该物品在其类别内的相对宽度。值可以介于0.0到1.0之间。负值被替换为0.0，大于1.0的值被替换为1.0。

**如何使用：** 调用 `setBoxWidth(...)` 修改 `boxWidth`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setBrush(const QBrush &brush)`

**作用与语义：**

该特性用于填充箱子和胡须物品的画刷。

**如何使用：** 调用 `setBrush(...)` 修改 `brush`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setPen(const QPen &pen)`

**作用与语义：**

该属性包含用于绘制盒子和胡须物品线条的笔。

**如何使用：** 调用 `setPen(...)` 修改 `pen`；传入的新值会成为后续查询和相关界面行为所使用的值。

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

`QBoxPlotSeries` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
