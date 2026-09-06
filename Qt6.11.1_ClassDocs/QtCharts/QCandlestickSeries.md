# QCandlestickSeries

> Qt 6.11.1 · Qt Charts

## 1. 先建立直觉

**一句话定位：** `QCandlestickSeries` 是 Qt 对象机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Charts 提供折线、柱状、饼图、散点图和坐标轴等数据可视化组件。

### 这是什么

`QCandlestickSeries` 是 Qt 对象机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

**适用场景：** 使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

## 2. 依赖与对象关系

- 头文件：`#include <QCandlestickSeries>`
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

- `bodyOutlineVisible : bool`
- `bodyWidth : qreal`
- `brush : QBrush`
- `capsVisible : bool`
- `capsWidth : qreal`
- `count : int`
- `decreasingColor : QColor`
- `increasingColor : QColor`
- `maximumColumnWidth : qreal`
- `minimumColumnWidth : qreal`
- `pen : QPen`

### 公有函数

- `QCandlestickSeries(QObject *parent = nullptr)`
- `virtual ~QCandlestickSeries()`
- `bool append(QCandlestickSet *set)`
- `bool append(const QList<QCandlestickSet *> &sets)`
- `bool bodyOutlineVisible() const`
- `qreal bodyWidth() const`
- `QBrush brush() const`
- `bool capsVisible() const`
- `qreal capsWidth() const`
- `void clear()`
- `int count() const`
- `QColor decreasingColor() const`
- `QColor increasingColor() const`
- `bool insert(int index, QCandlestickSet *set)`
- `qreal maximumColumnWidth() const`
- `qreal minimumColumnWidth() const`
- `QPen pen() const`
- `bool remove(QCandlestickSet *set)`
- `bool remove(const QList<QCandlestickSet *> &sets)`
- `void setBodyOutlineVisible(bool bodyOutlineVisible)`
- `void setBodyWidth(qreal bodyWidth)`
- `void setBrush(const QBrush &brush)`
- `void setCapsVisible(bool capsVisible)`
- `void setCapsWidth(qreal capsWidth)`
- `void setDecreasingColor(const QColor &decreasingColor)`
- `void setIncreasingColor(const QColor &increasingColor)`
- `void setMaximumColumnWidth(qreal maximumColumnWidth)`
- `void setMinimumColumnWidth(qreal minimumColumnWidth)`
- `void setPen(const QPen &pen)`
- `QList<QCandlestickSet *> sets() const`
- `bool take(QCandlestickSet *set)`

### 重实现的公有函数

- `virtual QAbstractSeries::SeriesType type() const override`

### 信号

- `void bodyOutlineVisibilityChanged()`
- `void bodyWidthChanged()`
- `void brushChanged()`
- `void candlestickSetsAdded(const QList<QCandlestickSet *> &sets)`
- `void candlestickSetsRemoved(const QList<QCandlestickSet *> &sets)`
- `void capsVisibilityChanged()`
- `void capsWidthChanged()`
- `void clicked(QCandlestickSet *set)`
- `void countChanged()`
- `void decreasingColorChanged()`
- `void doubleClicked(QCandlestickSet *set)`
- `void hovered(bool status, QCandlestickSet *set)`
- `void increasingColorChanged()`
- `void maximumColumnWidthChanged()`
- `void minimumColumnWidthChanged()`
- `void penChanged()`
- `void pressed(QCandlestickSet *set)`
- `void released(QCandlestickSet *set)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `bodyOutlineVisible : bool`

**作用与语义：**

该特性保持烛台主体轮廓的可见性。

**如何使用：** 调用 `bodyOutlineVisible()` 读取当前值；它不会修改应用状态。

### `bodyWidth : qreal`

**作用与语义：**

该属性表示烛台物品在其自身槽内的相对宽度，范围为0.0到1.0。
超出该范围的数值被限制为0.0或1.0。

**如何使用：** 调用 `bodyWidth()` 读取当前值；它不会修改应用状态。

### `brush : QBrush`

**作用与语义：**

该物业存放用于填充烛台物品的画刷。

**如何使用：** 调用 `brush()` 读取当前值；它不会修改应用状态。

### `capsVisible : bool`

**作用与语义：**

该特性保持帽的可见性。

**如何使用：** 调用 `capsVisible()` 读取当前值；它不会修改应用状态。

### `capsWidth : qreal`

**作用与语义：**

该属性决定了烛台内帽的相对宽度，范围为0.0到1.0。
超出该范围的数值被限制为0.0或1.0。

**如何使用：** 调用 `capsWidth()` 读取当前值；它不会修改应用状态。

### `[read-only] count : int`

**作用与语义：**

此属性保存系列中蜡烛图项目的数量。

**如何使用：** 调用 `count()` 读取当前值；它不会修改应用状态。

### `decreasingColor : QColor`

**作用与语义：**

该属性表示递减蜡烛台物品主体的颜色。
当开盘值高于收盘值时，蜡烛尺正在减小。默认情况下，该属性设置为画刷颜色，alpha通道设置为128。当该属性设置为无效色彩值时，也会使用默认颜色。

**如何使用：** 调用 `decreasingColor()` 读取当前值；它不会修改应用状态。

### `increasingColor : QColor`

**作用与语义：**

该属性表示递增的烛台物品主体颜色。
当烛台的收盘值高于开盘值时，它正在递增。默认情况下，该属性设置为画笔颜色。当属性设置为无效颜色值时，也会使用默认颜色。

**如何使用：** 调用 `increasingColor()` 读取当前值；它不会修改应用状态。

### `maximumColumnWidth : qreal`

**作用与语义：**

该属性包含烛台物品的最大宽度（像素单位）。设置负值意味着没有最大宽度。所有负值都转换为-1.0。

**如何使用：** 调用 `maximumColumnWidth()` 读取当前值；它不会修改应用状态。

### `minimumColumnWidth : qreal`

**作用与语义：**

该属性包含烛台物品的最小宽度（像素单位）。设置负值意味着没有最小宽度。所有负值都转换为-1.0。

**如何使用：** 调用 `minimumColumnWidth()` 读取当前值；它不会修改应用状态。

### `pen : QPen`

**作用与语义：**

该属性用于绘制烛台物品线条的笔。

**如何使用：** 调用 `pen()` 读取当前值；它不会修改应用状态。

### `[explicit] QCandlestickSeries::QCandlestickSeries(QObject *parent = nullptr)`

**作用与语义：**

构造一个空的QCandlestickSeries。`parent`为可选。

### `[virtual noexcept] QCandlestickSeries::~QCandlestickSeries()`

**作用与语义：**

销毁了整个系列。将该系列从图表中移除。

### `bool QCandlestickSeries::append(QCandlestickSet *set)`

**作用与语义：**

将`set`指定的单个烛台项目添加到序列中并取得其所有权。如果该物品为空或已在序列中，则不加入。若附加成功，返回`true`，`false`成功。

### `bool QCandlestickSeries::append(const QList<QCandlestickSet *> &sets)`

**作用与语义：**

将`sets`指定的烛台物品列表添加到系列中并取得其所有权。如果任何物品为空、已属于该系列或列表中出现多次，则不添加任何内容。如果所有物品都成功添加，则返回`true`，否则`false`返回。

### `[signal] void QCandlestickSeries::bodyOutlineVisibilityChanged()`

**作用与语义：**

该特性保持烛台主体轮廓的可见性。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `bodyOutlineVisible` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QCandlestickSeries::bodyWidthChanged()`

**作用与语义：**

该属性表示烛台物品在其自身槽内的相对宽度，范围为0.0到1.0。
超出该范围的数值被限制为0.0或1.0。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `bodyWidth` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QCandlestickSeries::brushChanged()`

**作用与语义：**

该物业存放用于填充烛台物品的画刷。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `brush` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QCandlestickSeries::candlestickSetsAdded(const QList<QCandlestickSet *> &sets)`

**作用与语义：**

当`sets`指定的烛台物品加入系列时，该信号会发出。

### `[signal] void QCandlestickSeries::candlestickSetsRemoved(const QList<QCandlestickSet *> &sets)`

**作用与语义：**

当`sets`指定的烛台物品从系列中移除时，该信号会发出。

### `[signal] void QCandlestickSeries::capsVisibilityChanged()`

**作用与语义：**

该特性保持帽的可见性。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `capsVisible` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QCandlestickSeries::capsWidthChanged()`

**作用与语义：**

该属性决定了烛台内帽的相对宽度，范围为0.0到1.0。
超出该范围的数值被限制为0.0或1.0。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `capsWidth` 的变化，不要把它当作普通函数主动调用。

### `void QCandlestickSeries::clear()`

**作用与语义：**

移除系列中所有烛台物品并永久删除。

### `[signal] void QCandlestickSeries::clicked(QCandlestickSet *set)`

**作用与语义：**

当点击图表上`set`指定的蜡烛条目时，会发出该信号。

### `int QCandlestickSeries::count() const`

**作用与语义：**

返回系列中烛台物品的数量。
注意：属性计数的获取函数。

### `[signal] void QCandlestickSeries::countChanged()`

**作用与语义：**

此属性保存系列中蜡烛图项目的数量。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `count` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QCandlestickSeries::decreasingColorChanged()`

**作用与语义：**

该属性表示递减蜡烛台物品主体的颜色。
当开盘值高于收盘值时，蜡烛尺正在减小。默认情况下，该属性设置为画刷颜色，alpha通道设置为128。当该属性设置为无效色彩值时，也会使用默认颜色。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `decreasingColor` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QCandlestickSeries::doubleClicked(QCandlestickSet *set)`

**作用与语义：**

当双击图表上`set`指定的烛台项目时，会发出该信号。

### `[signal] void QCandlestickSeries::hovered(bool status, QCandlestickSet *set)`

**作用与语义：**

当鼠标悬停在图表中`set`指定的烛台项目上时，会发出该信号。
当鼠标移动到物品上时，`status`会转为`true`;当鼠标再次移开时，`false`转。

### `[signal] void QCandlestickSeries::increasingColorChanged()`

**作用与语义：**

该属性表示递增的烛台物品主体颜色。
当烛台的收盘值高于开盘值时，它正在递增。默认情况下，该属性设置为画笔颜色。当属性设置为无效颜色值时，也会使用默认颜色。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `increasingColor` 的变化，不要把它当作普通函数主动调用。

### `bool QCandlestickSeries::insert(int index, QCandlestickSet *set)`

**作用与语义：**

将`set`指定的烛台项目插入`index`指定位置的系列。取得该物品的所有权。如果该物品为空或已属于该系列，则不插入。插入成功时返回`true`，否则`false`返回。

### `[signal] void QCandlestickSeries::maximumColumnWidthChanged()`

**作用与语义：**

该属性包含烛台物品的最大宽度（像素单位）。设置负值意味着没有最大宽度。所有负值都转换为-1.0。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `maximumColumnWidth` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QCandlestickSeries::minimumColumnWidthChanged()`

**作用与语义：**

该属性包含烛台物品的最小宽度（像素单位）。设置负值意味着没有最小宽度。所有负值都转换为-1.0。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `minimumColumnWidth` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QCandlestickSeries::penChanged()`

**作用与语义：**

该属性用于绘制烛台物品线条的笔。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `pen` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QCandlestickSeries::pressed(QCandlestickSet *set)`

**作用与语义：**

当用户点击`set`指定的烛台物品并按住鼠标按钮时，会发出该信号。

### `[signal] void QCandlestickSeries::released(QCandlestickSet *set)`

**作用与语义：**

当用户松开鼠标按压`set`指定的烛台物品时，会发出该信号。

### `bool QCandlestickSeries::remove(QCandlestickSet *set)`

**作用与语义：**

从序列中移除一个由`set`指定的烛台物品。如果该物品被成功删除，则返回`true`，否则`false`。

### `bool QCandlestickSeries::remove(const QList<QCandlestickSet *> &sets)`

**作用与语义：**

从系列中移除`sets`指定的烛台物品列表。如果任何物品为空、已被移除或列表中出现多次，则不移除任何物品。如果所有物品都成功移除，则返回`true`，否则`false`返回。

### `QList<QCandlestickSet *> QCandlestickSeries::sets() const`

**作用与语义：**

返回系列中的烛台物品列表。物品的所有权不变。

### `bool QCandlestickSeries::take(QCandlestickSet *set)`

**作用与语义：**

从序列中取一个由`set`指定的单一烛台项目。不删除该项。如果取取操作成功，返回`true`，否则`false`返回。
注意：该系列仍然是该物品的父对象。您必须设置父对象获得全部所有权。

### `[override virtual] QAbstractSeries::SeriesType QCandlestickSeries::type() const`

**作用与语义：**

重新实现了属性的访问函数：`QAbstractSeries::type`。
返回系列类型（`QAbstractSeries::SeriesTypeCandlestick`）。

### `bool bodyOutlineVisible() const`

**作用与语义：**

该特性保持烛台主体轮廓的可见性。

**如何使用：** 调用 `bodyOutlineVisible()` 读取当前值；它不会修改应用状态。

### `qreal bodyWidth() const`

**作用与语义：**

该属性表示烛台物品在其自身槽内的相对宽度，范围为0.0到1.0。
超出该范围的数值被限制为0.0或1.0。

**如何使用：** 调用 `bodyWidth()` 读取当前值；它不会修改应用状态。

### `QBrush brush() const`

**作用与语义：**

该物业存放用于填充烛台物品的画刷。

**如何使用：** 调用 `brush()` 读取当前值；它不会修改应用状态。

### `bool capsVisible() const`

**作用与语义：**

该特性保持帽的可见性。

**如何使用：** 调用 `capsVisible()` 读取当前值；它不会修改应用状态。

### `qreal capsWidth() const`

**作用与语义：**

该属性决定了烛台内帽的相对宽度，范围为0.0到1.0。
超出该范围的数值被限制为0.0或1.0。

**如何使用：** 调用 `capsWidth()` 读取当前值；它不会修改应用状态。

### `QColor decreasingColor() const`

**作用与语义：**

该属性表示递减蜡烛台物品主体的颜色。
当开盘值高于收盘值时，蜡烛尺正在减小。默认情况下，该属性设置为画刷颜色，alpha通道设置为128。当该属性设置为无效色彩值时，也会使用默认颜色。

**如何使用：** 调用 `decreasingColor()` 读取当前值；它不会修改应用状态。

### `QColor increasingColor() const`

**作用与语义：**

该属性表示递增的烛台物品主体颜色。
当烛台的收盘值高于开盘值时，它正在递增。默认情况下，该属性设置为画笔颜色。当属性设置为无效颜色值时，也会使用默认颜色。

**如何使用：** 调用 `increasingColor()` 读取当前值；它不会修改应用状态。

### `qreal maximumColumnWidth() const`

**作用与语义：**

该属性包含烛台物品的最大宽度（像素单位）。设置负值意味着没有最大宽度。所有负值都转换为-1.0。

**如何使用：** 调用 `maximumColumnWidth()` 读取当前值；它不会修改应用状态。

### `qreal minimumColumnWidth() const`

**作用与语义：**

该属性包含烛台物品的最小宽度（像素单位）。设置负值意味着没有最小宽度。所有负值都转换为-1.0。

**如何使用：** 调用 `minimumColumnWidth()` 读取当前值；它不会修改应用状态。

### `QPen pen() const`

**作用与语义：**

该属性用于绘制烛台物品线条的笔。

**如何使用：** 调用 `pen()` 读取当前值；它不会修改应用状态。

### `void setBodyOutlineVisible(bool bodyOutlineVisible)`

**作用与语义：**

该特性保持烛台主体轮廓的可见性。

**如何使用：** 调用 `setBodyOutlineVisible(...)` 修改 `bodyOutlineVisible`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setBodyWidth(qreal bodyWidth)`

**作用与语义：**

该属性表示烛台物品在其自身槽内的相对宽度，范围为0.0到1.0。
超出该范围的数值被限制为0.0或1.0。

**如何使用：** 调用 `setBodyWidth(...)` 修改 `bodyWidth`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setBrush(const QBrush &brush)`

**作用与语义：**

该物业存放用于填充烛台物品的画刷。

**如何使用：** 调用 `setBrush(...)` 修改 `brush`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setCapsVisible(bool capsVisible)`

**作用与语义：**

该特性保持帽的可见性。

**如何使用：** 调用 `setCapsVisible(...)` 修改 `capsVisible`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setCapsWidth(qreal capsWidth)`

**作用与语义：**

该属性决定了烛台内帽的相对宽度，范围为0.0到1.0。
超出该范围的数值被限制为0.0或1.0。

**如何使用：** 调用 `setCapsWidth(...)` 修改 `capsWidth`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setDecreasingColor(const QColor &decreasingColor)`

**作用与语义：**

该属性表示递减蜡烛台物品主体的颜色。
当开盘值高于收盘值时，蜡烛尺正在减小。默认情况下，该属性设置为画刷颜色，alpha通道设置为128。当该属性设置为无效色彩值时，也会使用默认颜色。

**如何使用：** 调用 `setDecreasingColor(...)` 修改 `decreasingColor`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setIncreasingColor(const QColor &increasingColor)`

**作用与语义：**

该属性表示递增的烛台物品主体颜色。
当烛台的收盘值高于开盘值时，它正在递增。默认情况下，该属性设置为画笔颜色。当属性设置为无效颜色值时，也会使用默认颜色。

**如何使用：** 调用 `setIncreasingColor(...)` 修改 `increasingColor`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMaximumColumnWidth(qreal maximumColumnWidth)`

**作用与语义：**

该属性包含烛台物品的最大宽度（像素单位）。设置负值意味着没有最大宽度。所有负值都转换为-1.0。

**如何使用：** 调用 `setMaximumColumnWidth(...)` 修改 `maximumColumnWidth`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setMinimumColumnWidth(qreal minimumColumnWidth)`

**作用与语义：**

该属性包含烛台物品的最小宽度（像素单位）。设置负值意味着没有最小宽度。所有负值都转换为-1.0。

**如何使用：** 调用 `setMinimumColumnWidth(...)` 修改 `minimumColumnWidth`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setPen(const QPen &pen)`

**作用与语义：**

该属性用于绘制烛台物品线条的笔。

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

`QCandlestickSeries` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
