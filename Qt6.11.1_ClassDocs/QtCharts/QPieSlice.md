# QPieSlice

> Qt 6.11.1 · Qt Charts

## 1. 先建立直觉

**一句话定位：** `QPieSlice` 是 Qt 对象机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Charts 提供折线、柱状、饼图、散点图和坐标轴等数据可视化组件。

### 这是什么

`QPieSlice` 是 Qt 对象机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

**适用场景：** 使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

## 2. 依赖与对象关系

- 头文件：`#include <QPieSlice>`
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

- `enum LabelPosition { LabelOutside, LabelInsideHorizontal, LabelInsideTangential, LabelInsideNormal }`

### 属性

- `angleSpan : qreal`
- `borderColor : QColor`
- `borderWidth : int`
- `brush : QBrush`
- `color : QColor`
- `explodeDistanceFactor : qreal`
- `exploded : bool`
- `label : QString`
- `labelArmLengthFactor : qreal`
- `labelBrush : QBrush`
- `labelColor : QColor`
- `labelFont : QFont`
- `labelPosition : LabelPosition`
- `labelVisible : bool`
- `pen : QPen`
- `percentage : qreal`
- `startAngle : qreal`
- `value : qreal`

### 公有函数

- `QPieSlice(QObject *parent = nullptr)`
- `QPieSlice(QString label, qreal value, QObject *parent = nullptr)`
- `virtual ~QPieSlice()`
- `qreal angleSpan() const`
- `QColor borderColor()`
- `int borderWidth()`
- `QBrush brush() const`
- `QColor color()`
- `qreal explodeDistanceFactor() const`
- `bool isExploded() const`
- `bool isLabelVisible() const`
- `QString label() const`
- `qreal labelArmLengthFactor() const`
- `QBrush labelBrush() const`
- `QColor labelColor()`
- `QFont labelFont() const`
- `QPieSlice::LabelPosition labelPosition()`
- `QPen pen() const`
- `qreal percentage() const`
- `QPieSeries * series() const`
- `void setBorderColor(QColor color)`
- `void setBorderWidth(int width)`
- `void setBrush(const QBrush &brush)`
- `void setColor(QColor color)`
- `void setExplodeDistanceFactor(qreal factor)`
- `void setExploded(bool exploded = true)`
- `void setLabel(QString label)`
- `void setLabelArmLengthFactor(qreal factor)`
- `void setLabelBrush(const QBrush &brush)`
- `void setLabelColor(QColor color)`
- `void setLabelFont(const QFont &font)`
- `void setLabelPosition(QPieSlice::LabelPosition position)`
- `void setLabelVisible(bool visible = true)`
- `void setPen(const QPen &pen)`
- `void setValue(qreal value)`
- `qreal startAngle() const`
- `qreal value() const`

### 信号

- `void angleSpanChanged()`
- `void borderColorChanged()`
- `void borderWidthChanged()`
- `void brushChanged()`
- `void clicked()`
- `void colorChanged()`
- `void doubleClicked()`
- `void hovered(bool state)`
- `void labelBrushChanged()`
- `void labelChanged()`
- `void labelColorChanged()`
- `void labelFontChanged()`
- `void labelVisibleChanged()`
- `void penChanged()`
- `void percentageChanged()`
- `void pressed()`
- `void released()`
- `void startAngleChanged()`
- `void valueChanged()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `enum QPieSlice::LabelPosition`

**作用与语义：**

这个枚举描述了切片标签的位置。
- `QPieSlice::LabelOutside`：`0`;标签位于连接它的切片之外，用臂连接。这是默认值。
- `QPieSlice::LabelInsideHorizontal`：`1`;标签位于切片中央并水平排列。
- `QPieSlice::LabelInsideTangential`：`2`;标签置中于切片内，并旋转使其与切片弧线平行。
- `QPieSlice::LabelInsideNormal`：`3`;标签置中于切片内，并旋转至与切片弧线的法线平行。

### `[read-only] angleSpan : qreal`

**作用与语义：**

该属性以度数表示切片的跨度。一个完整的饼是360度，0度位于12点钟方向。切片加入系列后自动更新。

**如何使用：** 调用 `angleSpan()` 读取当前值；它不会修改应用状态。

### `borderColor : QColor`

**作用与语义：**

该属性保留用于绘制切片边界的颜色。这是一个方便属性，用于修改切片笔。

**如何使用：** 调用 `borderColor()` 读取当前值；它不会修改应用状态。

### `borderWidth : int`

**作用与语义：**

该属性表示切片边界的宽度。这是修改切片笔的一个便利属性。

**如何使用：** 调用 `borderWidth()` 读取当前值；它不会修改应用状态。

### `brush : QBrush`

**作用与语义：**

该属性保留用于填充切片的画刷。

**如何使用：** 调用 `brush()` 读取当前值；它不会修改应用状态。

### `color : QColor`

**作用与语义：**

该属性保留了切片的填充（画刷）颜色。这是一个方便属性，用于修改切片画刷。

**如何使用：** 调用 `color()` 读取当前值；它不会修改应用状态。

### `explodeDistanceFactor : qreal`

**作用与语义：**

决定了炸裂的距离。
- 1.0表示距离等于半径。
- 0.5表示距离为半径的一半。
默认情况下，距离是0.15。

**如何使用：** 调用 `explodeDistanceFactor()` 读取当前值；它不会修改应用状态。

### `exploded : bool`

**作用与语义：**

该属性在切片是否与饼分离时成立。

**如何使用：** 调用 `exploded()` 读取当前值；它不会修改应用状态。

### `label : QString`

**作用与语义：**

该属性包含切片的标签。
注意：字符串可以采用HTML格式。

**如何使用：** 调用 `label()` 读取当前值；它不会修改应用状态。

### `labelArmLengthFactor : qreal`

**作用与语义：**

该属性表示标签臂的长度。因子相对于饼半径。例如：
- 1.0 表示长度与半径相同。
- 0.5 表示长度为半径的一半。
默认情况下，臂长为0.15。

**如何使用：** 调用 `labelArmLengthFactor()` 读取当前值；它不会修改应用状态。

### `labelBrush : QBrush`

**作用与语义：**

该属性包含用于绘制切片标签和标签臂的画刷。

**如何使用：** 调用 `labelBrush()` 读取当前值；它不会修改应用状态。

### `labelColor : QColor`

**作用与语义：**

该属性包含用于绘制切片标签的颜色。这是一个方便属性，用于修改切片标签刷。

**如何使用：** 调用 `labelColor()` 读取当前值；它不会修改应用状态。

### `labelFont : QFont`

**作用与语义：**

该属性包含用于绘制标签文本的字体。

**如何使用：** 调用 `labelFont()` 读取当前值；它不会修改应用状态。

### `labelPosition : LabelPosition`

**作用与语义：**

此属性保存切片标签的位置。

**如何使用：** 调用 `labelPosition()` 读取当前值；它不会修改应用状态。

### `labelVisible : bool`

**作用与语义：**

该属性包含切片标签的可见性。默认情况下，标签不可见。

**如何使用：** 调用 `labelVisible()` 读取当前值；它不会修改应用状态。

### `pen : QPen`

**作用与语义：**

该属性包含用于绘制切片边界的笔。

**如何使用：** 调用 `pen()` 读取当前值；它不会修改应用状态。

### `[read-only] percentage : qreal`

**作用与语义：**

该属性表示切片与序列中所有切片总和的百分比。实际值范围为0.0到1.0。切片加入序列后自动更新。

**如何使用：** 调用 `percentage()` 读取当前值；它不会修改应用状态。

### `[read-only] startAngle : qreal`

**作用与语义：**

该属性包含该切片在其所属序列中的起始角度。一个完整的饼是360度，0度位于12点钟方向。一旦将切片加入序列，将该切片自动更新。

**如何使用：** 调用 `startAngle()` 读取当前值；它不会修改应用状态。

### `value : qreal`

**作用与语义：**

该属性表示片的值。
注意：负值会转换为正值。

**如何使用：** 调用 `value()` 读取当前值；它不会修改应用状态。

### `[explicit] QPieSlice::QPieSlice(QObject *parent = nullptr)`

**作用与语义：**

用父 `parent`构造一个空片。

### `QPieSlice::QPieSlice(QString label, qreal value, QObject *parent = nullptr)`

**作用与语义：**

构造一个空片，包含指定的`value`、`label`和`parent`。

### `[virtual noexcept] QPieSlice::~QPieSlice()`

**作用与语义：**

移除该切片。如果切片已被添加到序列中，则不应被移除。

### `[signal] void QPieSlice::angleSpanChanged()`

**作用与语义：**

该属性以度数表示切片的跨度。一个完整的饼是360度，0度位于12点钟方向。切片加入系列后自动更新。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `angleSpan` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QPieSlice::borderColorChanged()`

**作用与语义：**

该属性保留用于绘制切片边界的颜色。这是一个方便属性，用于修改切片笔。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `borderColor` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QPieSlice::borderWidthChanged()`

**作用与语义：**

该属性表示切片边界的宽度。这是修改切片笔的一个便利属性。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `borderWidth` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QPieSlice::brushChanged()`

**作用与语义：**

该属性保留用于填充切片的画刷。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `brush` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QPieSlice::clicked()`

**作用与语义：**

当切片被点击时，该信号会发出。

### `[signal] void QPieSlice::colorChanged()`

**作用与语义：**

该属性保留了切片的填充（画刷）颜色。这是一个方便属性，用于修改切片画刷。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `color` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QPieSlice::doubleClicked()`

**作用与语义：**

当用户双击切片时，会发出该信号。

### `[signal] void QPieSlice::hovered(bool state)`

**作用与语义：**

当鼠标悬停在切片上时，该信号会发出。当鼠标移动到切片上时，`state`转`true`，当鼠标再次移开时，转为`false`。

### `[signal] void QPieSlice::labelBrushChanged()`

**作用与语义：**

该属性包含用于绘制切片标签和标签臂的画刷。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `labelBrush` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QPieSlice::labelChanged()`

**作用与语义：**

该属性包含切片的标签。
注意：字符串可以采用HTML格式。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `label` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QPieSlice::labelColorChanged()`

**作用与语义：**

该属性包含用于绘制切片标签的颜色。这是一个方便属性，用于修改切片标签刷。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `labelColor` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QPieSlice::labelFontChanged()`

**作用与语义：**

该属性包含用于绘制标签文本的字体。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `labelFont` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QPieSlice::labelVisibleChanged()`

**作用与语义：**

该属性包含切片标签的可见性。默认情况下，标签不可见。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `labelVisible` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QPieSlice::penChanged()`

**作用与语义：**

该属性包含用于绘制切片边界的笔。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `pen` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QPieSlice::percentageChanged()`

**作用与语义：**

该属性表示切片与序列中所有切片总和的百分比。实际值范围为0.0到1.0。切片加入序列后自动更新。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `percentage` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QPieSlice::pressed()`

**作用与语义：**

当用户点击切片并按住鼠标按钮时，会发出该信号。

### `[signal] void QPieSlice::released()`

**作用与语义：**

当用户松开鼠标按压切片时，会发出该信号。

### `QPieSeries *QPieSlice::series() const`

**作用与语义：**

返回该切片所属的系列。

### `[signal] void QPieSlice::startAngleChanged()`

**作用与语义：**

该属性包含该切片在其所属序列中的起始角度。一个完整的饼是360度，0度位于12点钟方向。一旦将切片加入序列，将该切片自动更新。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `startAngle` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QPieSlice::valueChanged()`

**作用与语义：**

该属性表示片的值。
注意：负值会转换为正值。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `value` 的变化，不要把它当作普通函数主动调用。

### `qreal angleSpan() const`

**作用与语义：**

该属性以度数表示切片的跨度。一个完整的饼是360度，0度位于12点钟方向。切片加入系列后自动更新。

**如何使用：** 调用 `angleSpan()` 读取当前值；它不会修改应用状态。

### `QColor borderColor()`

**作用与语义：**

该属性保留用于绘制切片边界的颜色。这是一个方便属性，用于修改切片笔。

**如何使用：** 调用 `borderColor()` 读取当前值；它不会修改应用状态。

### `int borderWidth()`

**作用与语义：**

该属性表示切片边界的宽度。这是修改切片笔的一个便利属性。

**如何使用：** 调用 `borderWidth()` 读取当前值；它不会修改应用状态。

### `QBrush brush() const`

**作用与语义：**

该属性保留用于填充切片的画刷。

**如何使用：** 调用 `brush()` 读取当前值；它不会修改应用状态。

### `QColor color()`

**作用与语义：**

该属性保留了切片的填充（画刷）颜色。这是一个方便属性，用于修改切片画刷。

**如何使用：** 调用 `color()` 读取当前值；它不会修改应用状态。

### `qreal explodeDistanceFactor() const`

**作用与语义：**

决定了炸裂的距离。
- 1.0表示距离等于半径。
- 0.5表示距离为半径的一半。
默认情况下，距离是0.15。

**如何使用：** 调用 `explodeDistanceFactor()` 读取当前值；它不会修改应用状态。

### `bool isExploded() const`

**作用与语义：**

该属性在切片是否与饼分离时成立。

**如何使用：** 调用 `isExploded()` 读取当前值；它不会修改应用状态。

### `bool isLabelVisible() const`

**作用与语义：**

该属性包含切片标签的可见性。默认情况下，标签不可见。

**如何使用：** 调用 `isLabelVisible()` 读取当前值；它不会修改应用状态。

### `QString label() const`

**作用与语义：**

该属性包含切片的标签。
注意：字符串可以采用HTML格式。

**如何使用：** 调用 `label()` 读取当前值；它不会修改应用状态。

### `qreal labelArmLengthFactor() const`

**作用与语义：**

该属性表示标签臂的长度。因子相对于饼半径。例如：
- 1.0 表示长度与半径相同。
- 0.5 表示长度为半径的一半。
默认情况下，臂长为0.15。

**如何使用：** 调用 `labelArmLengthFactor()` 读取当前值；它不会修改应用状态。

### `QBrush labelBrush() const`

**作用与语义：**

该属性包含用于绘制切片标签和标签臂的画刷。

**如何使用：** 调用 `labelBrush()` 读取当前值；它不会修改应用状态。

### `QColor labelColor()`

**作用与语义：**

该属性包含用于绘制切片标签的颜色。这是一个方便属性，用于修改切片标签刷。

**如何使用：** 调用 `labelColor()` 读取当前值；它不会修改应用状态。

### `QFont labelFont() const`

**作用与语义：**

该属性包含用于绘制标签文本的字体。

**如何使用：** 调用 `labelFont()` 读取当前值；它不会修改应用状态。

### `QPieSlice::LabelPosition labelPosition()`

**作用与语义：**

此属性保存切片标签的位置。

**如何使用：** 调用 `labelPosition()` 读取当前值；它不会修改应用状态。

### `QPen pen() const`

**作用与语义：**

该属性包含用于绘制切片边界的笔。

**如何使用：** 调用 `pen()` 读取当前值；它不会修改应用状态。

### `qreal percentage() const`

**作用与语义：**

该属性表示切片与序列中所有切片总和的百分比。实际值范围为0.0到1.0。切片加入序列后自动更新。

**如何使用：** 调用 `percentage()` 读取当前值；它不会修改应用状态。

### `void setBorderColor(QColor color)`

**作用与语义：**

该属性保留用于绘制切片边界的颜色。这是一个方便属性，用于修改切片笔。

**如何使用：** 调用 `setBorderColor(...)` 修改 `borderColor`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setBorderWidth(int width)`

**作用与语义：**

该属性表示切片边界的宽度。这是修改切片笔的一个便利属性。

**如何使用：** 调用 `setBorderWidth(...)` 修改 `borderWidth`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setBrush(const QBrush &brush)`

**作用与语义：**

该属性保留用于填充切片的画刷。

**如何使用：** 调用 `setBrush(...)` 修改 `brush`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setColor(QColor color)`

**作用与语义：**

该属性保留了切片的填充（画刷）颜色。这是一个方便属性，用于修改切片画刷。

**如何使用：** 调用 `setColor(...)` 修改 `color`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setExplodeDistanceFactor(qreal factor)`

**作用与语义：**

决定了炸裂的距离。
- 1.0表示距离等于半径。
- 0.5表示距离为半径的一半。
默认情况下，距离是0.15。

**如何使用：** 调用 `setExplodeDistanceFactor(...)` 修改 `explodeDistanceFactor`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setExploded(bool exploded = true)`

**作用与语义：**

该属性在切片是否与饼分离时成立。

**如何使用：** 调用 `setExploded(...)` 修改 `exploded`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setLabel(QString label)`

**作用与语义：**

该属性包含切片的标签。
注意：字符串可以采用HTML格式。

**如何使用：** 调用 `setLabel(...)` 修改 `label`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setLabelArmLengthFactor(qreal factor)`

**作用与语义：**

该属性表示标签臂的长度。因子相对于饼半径。例如：
- 1.0 表示长度与半径相同。
- 0.5 表示长度为半径的一半。
默认情况下，臂长为0.15。

**如何使用：** 调用 `setLabelArmLengthFactor(...)` 修改 `labelArmLengthFactor`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setLabelBrush(const QBrush &brush)`

**作用与语义：**

该属性包含用于绘制切片标签和标签臂的画刷。

**如何使用：** 调用 `setLabelBrush(...)` 修改 `labelBrush`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setLabelColor(QColor color)`

**作用与语义：**

该属性包含用于绘制切片标签的颜色。这是一个方便属性，用于修改切片标签刷。

**如何使用：** 调用 `setLabelColor(...)` 修改 `labelColor`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setLabelFont(const QFont &font)`

**作用与语义：**

该属性包含用于绘制标签文本的字体。

**如何使用：** 调用 `setLabelFont(...)` 修改 `labelFont`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setLabelPosition(QPieSlice::LabelPosition position)`

**作用与语义：**

此属性保存切片标签的位置。

**如何使用：** 调用 `setLabelPosition(...)` 修改 `labelPosition`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setLabelVisible(bool visible = true)`

**作用与语义：**

该属性包含切片标签的可见性。默认情况下，标签不可见。

**如何使用：** 调用 `setLabelVisible(...)` 修改 `labelVisible`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setPen(const QPen &pen)`

**作用与语义：**

该属性包含用于绘制切片边界的笔。

**如何使用：** 调用 `setPen(...)` 修改 `pen`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setValue(qreal value)`

**作用与语义：**

该属性表示片的值。
注意：负值会转换为正值。

**如何使用：** 调用 `setValue(...)` 修改 `value`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `qreal startAngle() const`

**作用与语义：**

该属性包含该切片在其所属序列中的起始角度。一个完整的饼是360度，0度位于12点钟方向。一旦将切片加入序列，将该切片自动更新。

**如何使用：** 调用 `startAngle()` 读取当前值；它不会修改应用状态。

### `qreal value() const`

**作用与语义：**

该属性表示片的值。
注意：负值会转换为正值。

**如何使用：** 调用 `value()` 读取当前值；它不会修改应用状态。

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

`QPieSlice` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
