# QAreaSeries

> Qt 6.11.1 · Qt Charts

## 1. 先建立直觉

**一句话定位：** `QAreaSeries` 是 Qt 对象机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Charts 提供折线、柱状、饼图、散点图和坐标轴等数据可视化组件。

### 这是什么

`QAreaSeries` 是 Qt 对象机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

**适用场景：** 使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

## 2. 依赖与对象关系

- 头文件：`#include <QAreaSeries>`
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

- `borderColor : QColor`
- `color : QColor`
- `lowerSeries : QLineSeries*`
- `pointLabelsClipping : bool`
- `pointLabelsColor : QColor`
- `pointLabelsFont : QFont`
- `pointLabelsFormat : QString`
- `pointLabelsVisible : bool`
- `upperSeries : QLineSeries*`

### 公有函数

- `QAreaSeries(QObject *parent = nullptr)`
- `QAreaSeries(QLineSeries *upperSeries, QLineSeries *lowerSeries = nullptr)`
- `virtual ~QAreaSeries()`
- `QColor borderColor() const`
- `QBrush brush() const`
- `QColor color() const`
- `QLineSeries * lowerSeries() const`
- `QPen pen() const`
- `bool pointLabelsClipping() const`
- `QColor pointLabelsColor() const`
- `QFont pointLabelsFont() const`
- `QString pointLabelsFormat() const`
- `bool pointLabelsVisible() const`
- `bool pointsVisible() const`
- `void setBorderColor(const QColor &color)`
- `void setBrush(const QBrush &brush)`
- `void setColor(const QColor &color)`
- `void setLowerSeries(QLineSeries *series)`
- `void setPen(const QPen &pen)`
- `void setPointLabelsClipping(bool enabled = true)`
- `void setPointLabelsColor(const QColor &color)`
- `void setPointLabelsFont(const QFont &font)`
- `void setPointLabelsFormat(const QString &format)`
- `void setPointLabelsVisible(bool visible = true)`
- `void setPointsVisible(bool visible = true)`
- `void setUpperSeries(QLineSeries *series)`
- `QLineSeries * upperSeries() const`

### 重实现的公有函数

- `virtual QAbstractSeries::SeriesType type() const override`

### 信号

- `void borderColorChanged(QColor color)`
- `void clicked(const QPointF &point)`
- `void colorChanged(QColor color)`
- `void doubleClicked(const QPointF &point)`
- `void hovered(const QPointF &point, bool state)`
- `void pointLabelsClippingChanged(bool clipping)`
- `void pointLabelsColorChanged(const QColor &color)`
- `void pointLabelsFontChanged(const QFont &font)`
- `void pointLabelsFormatChanged(const QString &format)`
- `void pointLabelsVisibilityChanged(bool visible)`
- `void pressed(const QPointF &point)`
- `void released(const QPointF &point)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `borderColor : QColor`

**作用与语义：**

该属性表示了系列的线（笔）颜色。这是一个方便属性，用于修改笔的颜色。

**如何使用：** 调用 `borderColor()` 读取当前值；它不会修改应用状态。

### `color : QColor`

**作用与语义：**

该属性保留了系列的填充（画笔）颜色。这是一个方便属性，用于修改画笔颜色。

**如何使用：** 调用 `color()` 读取当前值；它不会修改应用状态。

### `[read-only] lowerSeries : QLineSeries*`

**作用与语义：**

该属性表示定义面积系列边界的两条线系中的下一条。
注意：如果`QAreaSeries`构造时没有下系列，则该系列为无效。

**如何使用：** 调用 `lowerSeries()` 读取当前值；它不会修改应用状态。

### `pointLabelsClipping : bool`

**作用与语义：**

该属性保留数据点标签的裁剪。默认为真。当开启裁剪时，图区边缘的标签会被裁切。

**如何使用：** 调用 `pointLabelsClipping()` 读取当前值；它不会修改应用状态。

### `pointLabelsColor : QColor`

**作用与语义：**

该属性包含用于数据点标签的颜色。默认情况下，颜色是主题中标签所定义的画笔颜色。

**如何使用：** 调用 `pointLabelsColor()` 读取当前值；它不会修改应用状态。

### `pointLabelsFont : QFont`

**作用与语义：**

该属性包含用于数据点标签的字体。

**如何使用：** 调用 `pointLabelsFont()` 读取当前值；它不会修改应用状态。

### `pointLabelsFormat : QString`

**作用与语义：**

该属性表示了显示带序列点标签的格式。
`QAreaSeries` 支持以下格式标签：
- `@xPoint`：数据点的x值
- `@yPoint`：数据点的y值
例如，以下格式标签的使用方式会产生将数据点（x， y）标注在括号内并用逗号分隔的标签：
默认情况下，标签格式设置为`@xPoint, @yPoint`。标签显示在图区，而图区边缘的标签则被裁切。如果点彼此接近，标签可能会重叠。

**如何使用：** 调用 `pointLabelsFormat()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 series->setPointLabelsFormat("(@xPoint, @yPoint)");
```

### `pointLabelsVisible : bool`

**作用与语义：**

该属性保留了数据点标签的可见性。默认为假。

**如何使用：** 调用 `pointLabelsVisible()` 读取当前值；它不会修改应用状态。

### `[read-only] upperSeries : QLineSeries*`

**作用与语义：**

此属性保存用于定义区域系列边界的两条线系列中的上方一条。

**如何使用：** 调用 `upperSeries()` 读取当前值；它不会修改应用状态。

### `[explicit] QAreaSeries::QAreaSeries(QObject *parent = nullptr)`

**作用与语义：**

构造一个没有上级或下系列的面积系列对象，`parent`对象。

### `[explicit] QAreaSeries::QAreaSeries(QLineSeries *upperSeries, QLineSeries *lowerSeries = nullptr)`

**作用与语义：**

构造一个面积系列对象，该对象将在`upperSeries`线和`lowerSeries`线之间张成。如果没有传递`lowerSeries`给构造器，则使用x轴作为下界。
QAreaSeries 不拥有上系列或下系列，但所有权仍归调用者所有。当系列对象被添加到`QChartView`或`QChart`时，实例所有权转移。

### `[virtual noexcept] QAreaSeries::~QAreaSeries()`

**作用与语义：**

摧毁了该物体。

### `[signal] void QAreaSeries::borderColorChanged(QColor color)`

**作用与语义：**

该属性表示了系列的线（笔）颜色。这是一个方便属性，用于修改笔的颜色。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `borderColor` 的变化，不要把它当作普通函数主动调用。

### `QBrush QAreaSeries::brush() const`

**作用与语义：**

归还用来划定本系列界限的画笔。

### `[signal] void QAreaSeries::clicked(const QPointF &point)`

**作用与语义：**

当用户点击区域图中的`point`触发按键时，会发出该信号。

### `[signal] void QAreaSeries::colorChanged(QColor color)`

**作用与语义：**

该属性保留了系列的填充（画笔）颜色。这是一个方便属性，用于修改画笔颜色。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `color` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QAreaSeries::doubleClicked(const QPointF &point)`

**作用与语义：**

当用户通过双击`point`触发区域图的第一次点击时，会发出该信号。

### `[signal] void QAreaSeries::hovered(const QPointF &point, bool state)`

**作用与语义：**

当用户将鼠标光标悬停在序列上或将其移离序列时，会发出该信号。`point`显示悬停事件的起点（坐标）。当光标悬停在序列上时，`state`为`true`，当光标远离序列时变为虚假。

### `QPen QAreaSeries::pen() const`

**作用与语义：**

归还用于本系列划线的钢笔。

### `[signal] void QAreaSeries::pointLabelsClippingChanged(bool clipping)`

**作用与语义：**

该属性保留数据点标签的裁剪。默认为真。当开启裁剪时，图区边缘的标签会被裁切。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `pointLabelsClipping` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QAreaSeries::pointLabelsColorChanged(const QColor &color)`

**作用与语义：**

该属性包含用于数据点标签的颜色。默认情况下，颜色是主题中标签所定义的画笔颜色。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `pointLabelsColor` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QAreaSeries::pointLabelsFontChanged(const QFont &font)`

**作用与语义：**

该属性包含用于数据点标签的字体。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `pointLabelsFont` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QAreaSeries::pointLabelsFormatChanged(const QString &format)`

**作用与语义：**

该属性表示了显示带序列点标签的格式。
`QAreaSeries` 支持以下格式标签：
- `@xPoint`：数据点的x值
- `@yPoint`：数据点的y值
例如，以下格式标签的使用方式会产生将数据点（x， y）标注在括号内并用逗号分隔的标签：
默认情况下，标签格式设置为`@xPoint, @yPoint`。标签显示在图区，而图区边缘的标签则被裁切。如果点彼此接近，标签可能会重叠。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `pointLabelsFormat` 的变化，不要把它当作普通函数主动调用。

**官方示例：**

```cpp
 series->setPointLabelsFormat("(@xPoint, @yPoint)");
```

### `[signal] void QAreaSeries::pointLabelsVisibilityChanged(bool visible)`

**作用与语义：**

该属性保留了数据点标签的可见性。默认为假。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `pointLabelsVisible` 的变化，不要把它当作普通函数主动调用。

### `bool QAreaSeries::pointsVisible() const`

**作用与语义：**

是否抽到本系列积分。

### `[signal] void QAreaSeries::pressed(const QPointF &point)`

**作用与语义：**

当用户按下面积图中`point`指定的点时，会发出该信号。

### `[signal] void QAreaSeries::released(const QPointF &point)`

**作用与语义：**

当用户松开在区域图`point`触发的按压时，会发出该信号。

### `void QAreaSeries::setBrush(const QBrush &brush)`

**作用与语义：**

设定用于填充该区域的`brush`。

### `void QAreaSeries::setLowerSeries(QLineSeries *series)`

**作用与语义：**

设定将用作面积图下系列的`series`。

### `void QAreaSeries::setPen(const QPen &pen)`

**作用与语义：**

设置用于绘制区域轮廓的 `pen`。

### `void QAreaSeries::setPointsVisible(bool visible = true)`

**作用与语义：**

确定数据点是否`visible`并应在线上绘制。

### `void QAreaSeries::setUpperSeries(QLineSeries *series)`

**作用与语义：**

确定用作面积图上系列列的`series`。如果上方系列为零，即使面积图有下级系列，也不会绘制。

### `[override virtual] QAbstractSeries::SeriesType QAreaSeries::type() const`

**作用与语义：**

重新实现了属性的访问函数：`QAbstractSeries::type`。
`QAbstractSeries::SeriesTypeArea`回归。

### `QColor borderColor() const`

**作用与语义：**

该属性表示了系列的线（笔）颜色。这是一个方便属性，用于修改笔的颜色。

**如何使用：** 调用 `borderColor()` 读取当前值；它不会修改应用状态。

### `QColor color() const`

**作用与语义：**

该属性保留了系列的填充（画笔）颜色。这是一个方便属性，用于修改画笔颜色。

**如何使用：** 调用 `color()` 读取当前值；它不会修改应用状态。

### `QLineSeries * lowerSeries() const`

**作用与语义：**

该属性表示定义面积系列边界的两条线系中的下一条。
注意：如果`QAreaSeries`构造时没有下系列，则该系列为无效。

**如何使用：** 调用 `lowerSeries()` 读取当前值；它不会修改应用状态。

### `bool pointLabelsClipping() const`

**作用与语义：**

该属性保留数据点标签的裁剪。默认为真。当开启裁剪时，图区边缘的标签会被裁切。

**如何使用：** 调用 `pointLabelsClipping()` 读取当前值；它不会修改应用状态。

### `QColor pointLabelsColor() const`

**作用与语义：**

该属性包含用于数据点标签的颜色。默认情况下，颜色是主题中标签所定义的画笔颜色。

**如何使用：** 调用 `pointLabelsColor()` 读取当前值；它不会修改应用状态。

### `QFont pointLabelsFont() const`

**作用与语义：**

该属性包含用于数据点标签的字体。

**如何使用：** 调用 `pointLabelsFont()` 读取当前值；它不会修改应用状态。

### `QString pointLabelsFormat() const`

**作用与语义：**

该属性表示了显示带序列点标签的格式。
`QAreaSeries` 支持以下格式标签：
- `@xPoint`：数据点的x值
- `@yPoint`：数据点的y值
例如，以下格式标签的使用方式会产生将数据点（x， y）标注在括号内并用逗号分隔的标签：
默认情况下，标签格式设置为`@xPoint, @yPoint`。标签显示在图区，而图区边缘的标签则被裁切。如果点彼此接近，标签可能会重叠。

**如何使用：** 调用 `pointLabelsFormat()` 读取当前值；它不会修改应用状态。

**官方示例：**

```cpp
 series->setPointLabelsFormat("(@xPoint, @yPoint)");
```

### `bool pointLabelsVisible() const`

**作用与语义：**

该属性保留了数据点标签的可见性。默认为假。

**如何使用：** 调用 `pointLabelsVisible()` 读取当前值；它不会修改应用状态。

### `void setBorderColor(const QColor &color)`

**作用与语义：**

该属性表示了系列的线（笔）颜色。这是一个方便属性，用于修改笔的颜色。

**如何使用：** 调用 `setBorderColor(...)` 修改 `borderColor`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setColor(const QColor &color)`

**作用与语义：**

该属性保留了系列的填充（画笔）颜色。这是一个方便属性，用于修改画笔颜色。

**如何使用：** 调用 `setColor(...)` 修改 `color`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setPointLabelsClipping(bool enabled = true)`

**作用与语义：**

该属性保留数据点标签的裁剪。默认为真。当开启裁剪时，图区边缘的标签会被裁切。

**如何使用：** 调用 `setPointLabelsClipping(...)` 修改 `pointLabelsClipping`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setPointLabelsColor(const QColor &color)`

**作用与语义：**

该属性包含用于数据点标签的颜色。默认情况下，颜色是主题中标签所定义的画笔颜色。

**如何使用：** 调用 `setPointLabelsColor(...)` 修改 `pointLabelsColor`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setPointLabelsFont(const QFont &font)`

**作用与语义：**

该属性包含用于数据点标签的字体。

**如何使用：** 调用 `setPointLabelsFont(...)` 修改 `pointLabelsFont`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setPointLabelsFormat(const QString &format)`

**作用与语义：**

该属性表示了显示带序列点标签的格式。
`QAreaSeries` 支持以下格式标签：
- `@xPoint`：数据点的x值
- `@yPoint`：数据点的y值
例如，以下格式标签的使用方式会产生将数据点（x， y）标注在括号内并用逗号分隔的标签：
默认情况下，标签格式设置为`@xPoint, @yPoint`。标签显示在图区，而图区边缘的标签则被裁切。如果点彼此接近，标签可能会重叠。

**如何使用：** 调用 `setPointLabelsFormat(...)` 修改 `pointLabelsFormat`；传入的新值会成为后续查询和相关界面行为所使用的值。

**官方示例：**

```cpp
 series->setPointLabelsFormat("(@xPoint, @yPoint)");
```

### `void setPointLabelsVisible(bool visible = true)`

**作用与语义：**

该属性保留了数据点标签的可见性。默认为假。

**如何使用：** 调用 `setPointLabelsVisible(...)` 修改 `pointLabelsVisible`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QLineSeries * upperSeries() const`

**作用与语义：**

此属性保存用于定义区域系列边界的两条线系列中的上方一条。

**如何使用：** 调用 `upperSeries()` 读取当前值；它不会修改应用状态。

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

`QAreaSeries` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
