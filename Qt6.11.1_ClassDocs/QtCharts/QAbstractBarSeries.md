# QAbstractBarSeries

> Qt 6.11.1 · Qt Charts

## 1. 先建立直觉

**一句话定位：** `QAbstractBarSeries` 是 Qt 对象机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Charts 提供折线、柱状、饼图、散点图和坐标轴等数据可视化组件。

### 这是什么

`QAbstractBarSeries` 是 Qt Charts 中的抽象协议类型，通常通过具体子类、模型、插件或工厂来使用。

**内部模型：** 抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

**适用场景：** 当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。

**典型调用链：** 选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。

**先记住的坑：** 不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

## 2. 依赖与对象关系

- 头文件：`#include <QAbstractBarSeries>`
- 继承自：QAbstractSeries
- 直接派生类：QBarSeries、QHorizontalBarSeries、QHorizontalPercentBarSeries、QHorizontalStackedBarSeries、QPercentBarSeries,、QStackedBarSeries

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

抽象类的核心不是直接创建对象，而是理解它规定的虚函数、状态和通知协议。阅读时先列出必须实现的纯虚函数，再看框架何时调用它们。

### 状态、生命周期和线程

**生命周期：** 先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

**状态与结果：** QObject 派生对象的状态通常通过属性、状态查询函数和信号变化共同表达。信号是通知，不是返回值；收到通知后应读取当前状态并处理异常路径，不能假设每个信号只会出现一次。

**线程与事件循环：** QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

## 3. 直接使用

当 Qt 的现成子类不能满足需求，需要自定义数据源、渲染器、处理器或插件时继承它。 使用时通常按这个过程组织：选择合适的具体抽象基类 -> 实现纯虚函数和必要通知 -> 交给 Qt 框架注册/绑定 -> 遵守生命周期和线程约束。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `enum LabelsPosition { LabelsCenter, LabelsInsideEnd, LabelsInsideBase, LabelsOutsideEnd }`

### 属性

- `barWidth : qreal`
- `count : int`
- `labelsAngle : qreal`
- `labelsFormat : QString`
- `labelsPosition : LabelsPosition`
- `labelsPrecision : int`
- `labelsVisible : bool`

### 公有函数

- `virtual ~QAbstractBarSeries()`
- `bool append(QBarSet *set)`
- `bool append(const QList<QBarSet *> &sets)`
- `QList<QBarSet *> barSets() const`
- `qreal barWidth() const`
- `void clear()`
- `int count() const`
- `bool insert(int index, QBarSet *set)`
- `bool isLabelsVisible() const`
- `qreal labelsAngle() const`
- `QString labelsFormat() const`
- `QAbstractBarSeries::LabelsPosition labelsPosition() const`
- `int labelsPrecision() const`
- `bool remove(QBarSet *set)`
- `void setBarWidth(qreal width)`
- `void setLabelsAngle(qreal angle)`
- `void setLabelsFormat(const QString &format)`
- `void setLabelsPosition(QAbstractBarSeries::LabelsPosition position)`
- `void setLabelsPrecision(int precision)`
- `void setLabelsVisible(bool visible = true)`
- `bool take(QBarSet *set)`

### 信号

- `void barsetsAdded(const QList<QBarSet *> &sets)`
- `void barsetsRemoved(const QList<QBarSet *> &sets)`
- `void clicked(int index, QBarSet *barset)`
- `void countChanged()`
- `void doubleClicked(int index, QBarSet *barset)`
- `void hovered(bool status, int index, QBarSet *barset)`
- `void labelsAngleChanged(qreal angle)`
- `void labelsFormatChanged(const QString &format)`
- `void labelsPositionChanged(QAbstractBarSeries::LabelsPosition position)`
- `void labelsPrecisionChanged(int precision)`
- `void labelsVisibleChanged()`
- `void pressed(int index, QBarSet *barset)`
- `void released(int index, QBarSet *barset)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QAbstractBarSeries::LabelsPosition`

**作用与语义：**

该枚举值描述了数据值标签的位置：
- `QAbstractBarSeries::LabelsCenter`：`0`;标签位于横杆中央。
- `QAbstractBarSeries::LabelsInsideEnd`：`1`;标签位于栏杆顶部。
- `QAbstractBarSeries::LabelsInsideBase`：`2`;标签位于杠杆底部内侧。
- `QAbstractBarSeries::LabelsOutsideEnd`：`3`;标签位于杆外顶部。

### `barWidth : qreal`

**作用与语义：**

该属性表示系列条的宽度。
宽度的单位是x轴的单位。条的最小宽度为零，负值视为零。将宽度设为零意味着屏幕上条形条的宽度为1像素，无论x轴的比例如何。宽度大于零的条则使用x轴比例进行缩放。
注意：当与`QBarSeries`配合使用时，该值指定的是一组横杆的宽度，而非单根横杆的宽度。

**如何使用：** 调用 `barWidth()` 读取当前值；它不会修改应用状态。

### `[read-only] count : int`

**作用与语义：**

此属性保存条形图系列中的条集合数量。

**如何使用：** 调用 `count()` 读取当前值；它不会修改应用状态。

### `labelsAngle : qreal`

**作用与语义：**

该属性表示值标签的角度（度数）。

**如何使用：** 调用 `labelsAngle()` 读取当前值；它不会修改应用状态。

### `labelsFormat : QString`

**作用与语义：**

该属性保留了条形系列标签显示的格式。
`QAbstractBarSeries`支持以下格式标签：
- `@value`：棒数值
例如，格式标签的以下用法会产生显示值后面跟单位（u）的标签：
默认情况下，标签显示的是条形图的数值。对于百分比条数列，百分比在数值后加。标签显示在图块上，如果条形相近，标签可能会重叠。

**如何使用：** 调用 `labelsFormat()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 series->setLabelsFormat("@value u");
```

### `labelsPosition : LabelsPosition`

**作用与语义：**

这一属性具有价值标签的位置。

**如何使用：** 调用 `labelsPosition()` 读取当前值；它不会修改应用状态。

### `labelsPrecision : int`

**作用与语义：**

该特性包含价值标签中显著数字的最大数量。
默认值是6。

**如何使用：** 调用 `labelsPrecision()` 读取当前值；它不会修改应用状态。

### `labelsVisible : bool`

**作用与语义：**

该属性表示条形列中标签的可见性。

**如何使用：** 调用 `labelsVisible()` 读取当前值；它不会修改应用状态。

### `[virtual noexcept] QAbstractBarSeries::~QAbstractBarSeries()`

**作用与语义：**

移除抽象条数和其拥有的条形组。

### `bool QAbstractBarSeries::append(QBarSet *set)`

**作用与语义：**

将`set`指定的一组横线添加到横线系列中并取得其所有权。如果该集合为空或已属于该系列，则不会被附加。如果附加成功，返回`true`。

### `bool QAbstractBarSeries::append(const QList<QBarSet *> &sets)`

**作用与语义：**

将`sets`指定的条形集合列表添加到条形列中，并取得这些集合的所有权。如果所有集合都成功附加，返回`true`。如果任何集合为空或之前被附加到该系列中，则不添加任何东西，该函数返回`false`。如果列表中任何集合出现多次，则不添加任何集合，该函数返回`false`。

### `QList<QBarSet *> QAbstractBarSeries::barSets() const`

**作用与语义：**

返回酒吧系列中的酒吧套装列表。保留酒吧套装的所有权。

### `qreal QAbstractBarSeries::barWidth() const`

**作用与语义：**

返回该系列条的宽度。
注意：属性barWidth的Getter函数。

### `[signal] void QAbstractBarSeries::barsetsAdded(const QList<QBarSet *> &sets)`

**作用与语义：**

当`sets`指定的条形组加入串列时，该信号会发出。

### `[signal] void QAbstractBarSeries::barsetsRemoved(const QList<QBarSet *> &sets)`

**作用与语义：**

当`sets`指定的条形组从串列中移除时，该信号会发出。

### `void QAbstractBarSeries::clear()`

**作用与语义：**

移除系列中的所有小节组并永久删除。

### `[signal] void QAbstractBarSeries::clicked(int index, QBarSet *barset)`

**作用与语义：**

当用户点击`barset`指定的条组中`index`指定的条时，会发出该信号。

### `int QAbstractBarSeries::count() const`

**作用与语义：**

返回条形列中的条形组数。
注意：属性计数的获取函数。

### `[signal] void QAbstractBarSeries::countChanged()`

**作用与语义：**

此属性保存条形图系列中的条集合数量。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `count` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QAbstractBarSeries::doubleClicked(int index, QBarSet *barset)`

**作用与语义：**

当用户双击`barset`指定条组中`index`指定的条时，会发出该信号。

### `[signal] void QAbstractBarSeries::hovered(bool status, int index, QBarSet *barset)`

**作用与语义：**

当鼠标悬停在`barset`指定条中`index`指定的条上时，会发出该信号。当鼠标越过条时，`status`转`true`，当鼠标再次移开时，转为`false`。

### `bool QAbstractBarSeries::insert(int index, QBarSet *set)`

**作用与语义：**

将由`set`指定的条形集插入到`index`指定位置的序列中，并取得该集合的所有权。如果该集合为空或已属于该序列，则不会被附加。插入成功时返回`true`。

### `bool QAbstractBarSeries::isLabelsVisible() const`

**作用与语义：**

该属性表示条形列中标签的可见性。

**如何使用：** 调用 `isLabelsVisible()` 读取当前值；它不会修改应用状态。

### `[signal] void QAbstractBarSeries::labelsAngleChanged(qreal angle)`

**作用与语义：**

该属性表示值标签的角度（度数）。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `labelsAngle` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QAbstractBarSeries::labelsFormatChanged(const QString &format)`

**作用与语义：**

该属性保留了条形系列标签显示的格式。
`QAbstractBarSeries`支持以下格式标签：
- `@value`：棒数值
例如，格式标签的以下用法会产生显示值后面跟单位（u）的标签：
默认情况下，标签显示的是条形图的数值。对于百分比条数列，百分比在数值后加。标签显示在图块上，如果条形相近，标签可能会重叠。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `labelsFormat` 的变化，不要把它当作普通函数主动调用。

**官方示例：**

```cpp
 series->setLabelsFormat("@value u");
```

### `[signal] void QAbstractBarSeries::labelsPositionChanged(QAbstractBarSeries::LabelsPosition position)`

**作用与语义：**

这一属性具有价值标签的位置。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `labelsPosition` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QAbstractBarSeries::labelsPrecisionChanged(int precision)`

**作用与语义：**

该特性包含价值标签中显著数字的最大数量。
默认值是6。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `labelsPrecision` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QAbstractBarSeries::labelsVisibleChanged()`

**作用与语义：**

该属性表示条形列中标签的可见性。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `labelsVisible` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QAbstractBarSeries::pressed(int index, QBarSet *barset)`

**作用与语义：**

当用户点击`barset`指定的条中`index`指定的条形条并按住鼠标按钮时，会发出该信号。

### `[signal] void QAbstractBarSeries::released(int index, QBarSet *barset)`

**作用与语义：**

当用户松开鼠标按`barset`指定条形组中`index`指定的条时，会发出该信号。

### `bool QAbstractBarSeries::remove(QBarSet *set)`

**作用与语义：**

从序列中移除`set`指定的条形集合，若移除成功则永久删除。若该集合被移除，返回 `true`。

### `void QAbstractBarSeries::setBarWidth(qreal width)`

**作用与语义：**

该属性表示系列条的宽度。
宽度的单位是x轴的单位。条的最小宽度为零，负值视为零。将宽度设为零意味着屏幕上条形条的宽度为1像素，无论x轴的比例如何。宽度大于零的条则使用x轴比例进行缩放。
注意：当与`QBarSeries`配合使用时，该值指定的是一组横杆的宽度，而非单根横杆的宽度。

**如何使用：** 调用 `setBarWidth(...)` 修改 `barWidth`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QAbstractBarSeries::setLabelsVisible(bool visible = true)`

**作用与语义：**

该属性表示条形列中标签的可见性。

**如何使用：** 调用 `setLabelsVisible(...)` 修改 `labelsVisible`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `bool QAbstractBarSeries::take(QBarSet *set)`

**作用与语义：**

从系列中取一个`set`。不会删除条形设置对象。
注意：该系列仍然是条形组的父对象。您必须设置父对象获得全部所有权。
如果take操作成功，返回`true`。

### `qreal labelsAngle() const`

**作用与语义：**

该属性表示值标签的角度（度数）。

**如何使用：** 调用 `labelsAngle()` 读取当前值；它不会修改应用状态。

### `QString labelsFormat() const`

**作用与语义：**

该属性保留了条形系列标签显示的格式。
`QAbstractBarSeries`支持以下格式标签：
- `@value`：棒数值
例如，格式标签的以下用法会产生显示值后面跟单位（u）的标签：
默认情况下，标签显示的是条形图的数值。对于百分比条数列，百分比在数值后加。标签显示在图块上，如果条形相近，标签可能会重叠。

**如何使用：** 调用 `labelsFormat()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 series->setLabelsFormat("@value u");
```

### `QAbstractBarSeries::LabelsPosition labelsPosition() const`

**作用与语义：**

这一属性具有价值标签的位置。

**如何使用：** 调用 `labelsPosition()` 读取当前值；它不会修改应用状态。

### `int labelsPrecision() const`

**作用与语义：**

该特性包含价值标签中显著数字的最大数量。
默认值是6。

**如何使用：** 调用 `labelsPrecision()` 读取当前值；它不会修改应用状态。

### `void setLabelsAngle(qreal angle)`

**作用与语义：**

该属性表示值标签的角度（度数）。

**如何使用：** 调用 `setLabelsAngle(...)` 修改 `labelsAngle`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setLabelsFormat(const QString &format)`

**作用与语义：**

该属性保留了条形系列标签显示的格式。
`QAbstractBarSeries`支持以下格式标签：
- `@value`：棒数值
例如，格式标签的以下用法会产生显示值后面跟单位（u）的标签：
默认情况下，标签显示的是条形图的数值。对于百分比条数列，百分比在数值后加。标签显示在图块上，如果条形相近，标签可能会重叠。

**如何使用：** 调用 `setLabelsFormat(...)` 修改 `labelsFormat`；传入的新值会成为后续查询和相关界面行为所使用的值。

**官方示例：**

```cpp
 series->setLabelsFormat("@value u");
```

### `void setLabelsPosition(QAbstractBarSeries::LabelsPosition position)`

**作用与语义：**

这一属性具有价值标签的位置。

**如何使用：** 调用 `setLabelsPosition(...)` 修改 `labelsPosition`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setLabelsPrecision(int precision)`

**作用与语义：**

该特性包含价值标签中显著数字的最大数量。
默认值是6。

**如何使用：** 调用 `setLabelsPrecision(...)` 修改 `labelsPrecision`；传入的新值会成为后续查询和相关界面行为所使用的值。

## 6. 深入实践与常见坑

### 生命周期和资源边界

先确定对象由谁拥有：设置 parent 后，父对象析构会递归销毁子对象；没有 parent 时可放在栈上或显式使用 `deleteLater()`。跨线程对象不能随意直接删除、移动或调用其依赖线程的成员。异步回调应使用 context 或连接到对象生命周期。

### 状态和错误边界

QObject 派生对象的状态通常通过属性、状态查询函数和信号变化共同表达。信号是通知，不是返回值；收到通知后应读取当前状态并处理异常路径，不能假设每个信号只会出现一次。

### 线程边界

QObject 本身属于一个线程，但它的成员函数不会因为继承 QObject 就自动变成线程安全。直接调用仍在调用者线程执行；跨线程通信应使用 queued connection、信号槽或明确的同步机制。目标线程必须有事件循环，定时器和异步 I/O 才能工作。

### 最容易出现的错误

不要绕过 begin/end 或状态通知；纯虚函数返回值和调用线程要按文档约定；抽象对象通常不能直接实例化。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QAbstractBarSeries` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
