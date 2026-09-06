# QCandlestickSet

> Qt 6.11.1 · Qt Charts

## 1. 先建立直觉

**一句话定位：** `QCandlestickSet` 是 Qt 对象机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Charts 提供折线、柱状、饼图、散点图和坐标轴等数据可视化组件。

### 这是什么

`QCandlestickSet` 是 Qt 对象机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

**适用场景：** 使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

## 2. 依赖与对象关系

- 头文件：`#include <QCandlestickSet>`
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

### 属性

- `brush : QBrush`
- `close : qreal`
- `high : qreal`
- `low : qreal`
- `open : qreal`
- `pen : QPen`
- `timestamp : qreal`

### 公有函数

- `QCandlestickSet(qreal timestamp = 0.0, QObject *parent = nullptr)`
- `QCandlestickSet(qreal open, qreal high, qreal low, qreal close, qreal timestamp = 0.0, QObject *parent = nullptr)`
- `virtual ~QCandlestickSet()`
- `QBrush brush() const`
- `qreal close() const`
- `qreal high() const`
- `qreal low() const`
- `qreal open() const`
- `QPen pen() const`
- `void setBrush(const QBrush &brush)`
- `void setClose(qreal close)`
- `void setHigh(qreal high)`
- `void setLow(qreal low)`
- `void setOpen(qreal open)`
- `void setPen(const QPen &pen)`
- `void setTimestamp(qreal timestamp)`
- `qreal timestamp() const`

### 信号

- `void brushChanged()`
- `void clicked()`
- `void closeChanged()`
- `void doubleClicked()`
- `void highChanged()`
- `void hovered(bool status)`
- `void lowChanged()`
- `void openChanged()`
- `void penChanged()`
- `void pressed()`
- `void released()`
- `void timestampChanged()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `brush : QBrush`

**作用与语义：**

该特性用于填充蜡烛台物品的画刷。

**如何使用：** 调用 `brush()` 读取当前值；它不会修改应用状态。

### `close : qreal`

**作用与语义：**

该属性表示烛台物品的接近值。

**如何使用：** 调用 `close()` 读取当前值；它不会修改应用状态。

### `high : qreal`

**作用与语义：**

该属性具有蜡烛台物品的高价值。

**如何使用：** 调用 `high()` 读取当前值；它不会修改应用状态。

### `low : qreal`

**作用与语义：**

该属性保留烛台物品的低价值。

**如何使用：** 调用 `low()` 读取当前值；它不会修改应用状态。

### `open : qreal`

**作用与语义：**

该属性包含烛台物品的未开值。

**如何使用：** 调用 `open()` 读取当前值；它不会修改应用状态。

### `pen : QPen`

**作用与语义：**

该属性包含用于绘制蜡烛台物品线条的钢笔。

**如何使用：** 调用 `pen()` 读取当前值；它不会修改应用状态。

### `timestamp : qreal`

**作用与语义：**

该属性包含烛台项目的时间戳值。

**如何使用：** 调用 `timestamp()` 读取当前值；它不会修改应用状态。

### `[explicit] QCandlestickSet::QCandlestickSet(qreal timestamp = 0.0, QObject *parent = nullptr)`

**作用与语义：**

构造一个带有可选`timestamp`和一个`parent`的烛台物品。

### `[explicit] QCandlestickSet::QCandlestickSet(qreal open, qreal high, qreal low, qreal close, qreal timestamp = 0.0, QObject *parent = nullptr)`

**作用与语义：**

构造一个具有给定顺序值的蜡烛条目。`open`、`high`、`low`和`close`的数值为必填。`timestamp`和`parent`的数值为可选。

### `[virtual noexcept] QCandlestickSet::~QCandlestickSet()`

**作用与语义：**

摧毁烛台物品。

### `[signal] void QCandlestickSet::brushChanged()`

**作用与语义：**

该特性用于填充蜡烛台物品的画刷。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `brush` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QCandlestickSet::clicked()`

**作用与语义：**

当点击烛台物品时，该信号会发出。

### `[signal] void QCandlestickSet::closeChanged()`

**作用与语义：**

该属性表示烛台物品的接近值。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `close` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QCandlestickSet::doubleClicked()`

**作用与语义：**

当用户双击烛台物品时，会发出该信号。

### `[signal] void QCandlestickSet::highChanged()`

**作用与语义：**

该属性具有蜡烛台物品的高价值。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `high` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QCandlestickSet::hovered(bool status)`

**作用与语义：**

当鼠标悬停在烛台物品上时，会发出该信号。
当鼠标移动到物品上时，`status`会转`true`;当鼠标再次移开时，`false`转。

### `[signal] void QCandlestickSet::lowChanged()`

**作用与语义：**

该属性保留烛台物品的低价值。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `low` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QCandlestickSet::openChanged()`

**作用与语义：**

该属性包含烛台物品的未开值。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `open` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QCandlestickSet::penChanged()`

**作用与语义：**

该属性包含用于绘制蜡烛台物品线条的钢笔。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `pen` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QCandlestickSet::pressed()`

**作用与语义：**

当用户点击烛台物品并按住鼠标按钮时，会发出该信号。

### `[signal] void QCandlestickSet::released()`

**作用与语义：**

当用户松开鼠标按压蜡烛台物品时，会发出该信号。

### `[signal] void QCandlestickSet::timestampChanged()`

**作用与语义：**

该属性包含烛台项目的时间戳值。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `timestamp` 的变化，不要把它当作普通函数主动调用。

### `QBrush brush() const`

**作用与语义：**

该特性用于填充蜡烛台物品的画刷。

**如何使用：** 调用 `brush()` 读取当前值；它不会修改应用状态。

### `qreal close() const`

**作用与语义：**

该属性表示烛台物品的接近值。

**如何使用：** 调用 `close()` 读取当前值；它不会修改应用状态。

### `qreal high() const`

**作用与语义：**

该属性具有蜡烛台物品的高价值。

**如何使用：** 调用 `high()` 读取当前值；它不会修改应用状态。

### `qreal low() const`

**作用与语义：**

该属性保留烛台物品的低价值。

**如何使用：** 调用 `low()` 读取当前值；它不会修改应用状态。

### `qreal open() const`

**作用与语义：**

该属性包含烛台物品的未开值。

**如何使用：** 调用 `open()` 读取当前值；它不会修改应用状态。

### `QPen pen() const`

**作用与语义：**

该属性包含用于绘制蜡烛台物品线条的钢笔。

**如何使用：** 调用 `pen()` 读取当前值；它不会修改应用状态。

### `void setBrush(const QBrush &brush)`

**作用与语义：**

该特性用于填充蜡烛台物品的画刷。

**如何使用：** 调用 `setBrush(...)` 修改 `brush`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setClose(qreal close)`

**作用与语义：**

该属性表示烛台物品的接近值。

**如何使用：** 调用 `setClose(...)` 修改 `close`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setHigh(qreal high)`

**作用与语义：**

该属性具有蜡烛台物品的高价值。

**如何使用：** 调用 `setHigh(...)` 修改 `high`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setLow(qreal low)`

**作用与语义：**

该属性保留烛台物品的低价值。

**如何使用：** 调用 `setLow(...)` 修改 `low`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setOpen(qreal open)`

**作用与语义：**

该属性包含烛台物品的未开值。

**如何使用：** 调用 `setOpen(...)` 修改 `open`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setPen(const QPen &pen)`

**作用与语义：**

该属性包含用于绘制蜡烛台物品线条的钢笔。

**如何使用：** 调用 `setPen(...)` 修改 `pen`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setTimestamp(qreal timestamp)`

**作用与语义：**

该属性包含烛台项目的时间戳值。

**如何使用：** 调用 `setTimestamp(...)` 修改 `timestamp`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `qreal timestamp() const`

**作用与语义：**

该属性包含烛台项目的时间戳值。

**如何使用：** 调用 `timestamp()` 读取当前值；它不会修改应用状态。

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

`QCandlestickSet` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
