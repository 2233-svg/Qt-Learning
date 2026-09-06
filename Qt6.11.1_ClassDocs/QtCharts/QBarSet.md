# QBarSet

> Qt 6.11.1 · Qt Charts

## 1. 先建立直觉

**一句话定位：** `QBarSet` 是 Qt 对象机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Charts 提供折线、柱状、饼图、散点图和坐标轴等数据可视化组件。

### 这是什么

`QBarSet` 是 Qt 对象机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

**适用场景：** 使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

## 2. 依赖与对象关系

- 头文件：`#include <QBarSet>`
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

- `borderColor : QColor`
- `brush : QBrush`
- `color : QColor`
- `label : QString`
- `labelBrush : QBrush`
- `labelColor : QColor`
- `labelFont : QFont`
- `pen : QPen`

### 公有函数

- `QBarSet(const QString label, QObject *parent = nullptr)`
- `virtual ~QBarSet()`
- `void append(const QList<qreal> &values)`
- `void append(const qreal value)`
- `qreal at(const int index) const`
- `QColor borderColor()`
- `QBrush brush() const`
- `QColor color()`
- `int count() const`
- `(since 6.2) void deselectAllBars()`
- `(since 6.2) void deselectBar(int index)`
- `(since 6.2) void deselectBars(const QList<int> &indexes)`
- `void insert(const int index, const qreal value)`
- `(since 6.2) bool isBarSelected(int index) const`
- `QString label() const`
- `QBrush labelBrush() const`
- `QColor labelColor()`
- `QFont labelFont() const`
- `QPen pen() const`
- `void remove(const int index, const int count = 1)`
- `void replace(const int index, const qreal value)`
- `(since 6.2) void selectAllBars()`
- `(since 6.2) void selectBar(int index)`
- `(since 6.2) void selectBars(const QList<int> &indexes)`
- `(since 6.2) QList<int> selectedBars() const`
- `(since 6.2) QColor selectedColor() const`
- `(since 6.2) void setBarSelected(int index, bool selected)`
- `void setBorderColor(QColor color)`
- `void setBrush(const QBrush &brush)`
- `void setColor(QColor color)`
- `void setLabel(const QString label)`
- `void setLabelBrush(const QBrush &brush)`
- `void setLabelColor(QColor color)`
- `void setLabelFont(const QFont &font)`
- `void setPen(const QPen &pen)`
- `(since 6.2) void setSelectedColor(const QColor &color)`
- `qreal sum() const`
- `(since 6.2) void toggleSelection(const QList<int> &indexes)`
- `QBarSet & operator<<(const qreal &value)`
- `qreal operator[](const int index) const`

### 信号

- `void borderColorChanged(QColor color)`
- `void brushChanged()`
- `void clicked(int index)`
- `void colorChanged(QColor color)`
- `void doubleClicked(int index)`
- `void hovered(bool status, int index)`
- `void labelBrushChanged()`
- `void labelChanged()`
- `void labelColorChanged(QColor color)`
- `void labelFontChanged()`
- `void penChanged()`
- `void pressed(int index)`
- `void released(int index)`
- `void valueChanged(int index)`
- `void valuesAdded(int index, int count)`
- `void valuesRemoved(int index, int count)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `borderColor : QColor`

**作用与语义：**

该属性表示条形组的线（笔）颜色。

**如何使用：** 调用 `borderColor()` 读取当前值；它不会修改应用状态。

### `brush : QBrush`

**作用与语义：**

该属性包含用于填补条形条的画刷。

**如何使用：** 调用 `brush()` 读取当前值；它不会修改应用状态。

### `color : QColor`

**作用与语义：**

该属性保留了条形集的填充（刷）颜色。

**如何使用：** 调用 `color()` 读取当前值；它不会修改应用状态。

### `label : QString`

**作用与语义：**

该属性表示条形集的标签。

**如何使用：** 调用 `label()` 读取当前值；它不会修改应用状态。

### `labelBrush : QBrush`

**作用与语义：**

该属性包含用于绘制条形组标签的画刷。

**如何使用：** 调用 `labelBrush()` 读取当前值；它不会修改应用状态。

### `labelColor : QColor`

**作用与语义：**

该属性包含条形棒集的文本（标签）颜色。

**如何使用：** 调用 `labelColor()` 读取当前值；它不会修改应用状态。

### `labelFont : QFont`

**作用与语义：**

该属性包含用于绘制条形列标签的字体。

**如何使用：** 调用 `labelFont()` 读取当前值；它不会修改应用状态。

### `pen : QPen`

**作用与语义：**

该属性表明用来绘制条形组中条线的笔。

**如何使用：** 调用 `pen()` 读取当前值；它不会修改应用状态。

### `[explicit] QBarSet::QBarSet(const QString label, QObject *parent = nullptr)`

**作用与语义：**

构造一个条形集，标签为`label`，父节点为`parent`。

### `[virtual noexcept] QBarSet::~QBarSet()`

**作用与语义：**

拆除杆组。

### `void QBarSet::append(const QList<qreal> &values)`

**作用与语义：**

将`values`指定的实值列表附加到条形集合的末尾。

### `void QBarSet::append(const qreal value)`

**作用与语义：**

将`value`指定的新值附加到条形集末尾。

### `qreal QBarSet::at(const int index) const`

**作用与语义：**

返回由`index`从条形集合中指定的值。如果索引超出边界，则返回0.0。

### `QColor QBarSet::borderColor()`

**作用与语义：**

返回条形组的线条颜色。
注意：属性borderColor的Getter函数。

### `[signal] void QBarSet::borderColorChanged(QColor color)`

**作用与语义：**

该属性表示条形组的线（笔）颜色。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `borderColor` 的变化，不要把它当作普通函数主动调用。

### `QBrush QBarSet::brush() const`

**作用与语义：**

退还用于填补杠铃的画刷。
注意：属性画刷的获取函数。

### `[signal] void QBarSet::brushChanged()`

**作用与语义：**

该属性包含用于填补条形条的画刷。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `brush` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QBarSet::clicked(int index)`

**作用与语义：**

当用户点击`index`条指定条时，会发出该信号。

### `QColor QBarSet::color()`

**作用与语义：**

返回条形组的填充颜色。
注意：属性颜色的获取函数。

### `[signal] void QBarSet::colorChanged(QColor color)`

**作用与语义：**

该属性保留了条形集的填充（刷）颜色。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `color` 的变化，不要把它当作普通函数主动调用。

### `int QBarSet::count() const`

**作用与语义：**

返回条形组中的数值。

### `[since 6.2] void QBarSet::deselectAllBars()`

**作用与语义：**

取消了系列中的所有条。
注意：发出`QBarSet::selectedBarsChanged`。

### `[since 6.2] void QBarSet::deselectBar(int index)`

**作用与语义：**

取消`index`条。
注意：发出`QBarSet::selectedBarsChanged`。

### `[since 6.2] void QBarSet::deselectBars(const QList<int> &indexes)`

**作用与语义：**

在`indexes`列表中标记多个被通过的条为取消选中。
注意：会发出`QBarSet::selectedBarsChanged`。

### `[signal] void QBarSet::doubleClicked(int index)`

**作用与语义：**

当用户双击`index`条中指定的条形时，会发出该信号。

### `[signal] void QBarSet::hovered(bool status, int index)`

**作用与语义：**

当鼠标悬停在`index`指定的条形条上时，会发出该信号。当鼠标越过条时，`status`转`true`;当鼠标再次移开时，转为`false`。

### `void QBarSet::insert(const int index, const qreal value)`

**作用与语义：**

插入`value`在`index`指定的位置。插入值之后的值向上移动一个位置。

### `[since 6.2] bool QBarSet::isBarSelected(int index) const`

**作用与语义：**

如果该`index`的条位于所选条形中，则返回`true`，否则`false`。
注意：如果选中的条纹是用`QBarSet::setSelectedColor`指定颜色绘制的。

### `QString QBarSet::label() const`

**作用与语义：**

返回条形组的标签。
注意：属性标签的获取函数。

### `QBrush QBarSet::labelBrush() const`

**作用与语义：**

返回用于在该条形组顶部绘制数值的画笔。
注意：propertylabelBrush 的获取函数。

### `[signal] void QBarSet::labelBrushChanged()`

**作用与语义：**

该属性包含用于绘制条形组标签的画刷。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `labelBrush` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QBarSet::labelChanged()`

**作用与语义：**

该属性表示条形集的标签。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `label` 的变化，不要把它当作普通函数主动调用。

### `QColor QBarSet::labelColor()`

**作用与语义：**

返回条形组的文本颜色。
注意：属性labelColor的Getter函数。

### `[signal] void QBarSet::labelColorChanged(QColor color)`

**作用与语义：**

该属性包含条形棒集的文本（标签）颜色。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `labelColor` 的变化，不要把它当作普通函数主动调用。

### `QFont QBarSet::labelFont() const`

**作用与语义：**

返回用于绘制该条形图集顶部数值的笔。
注意：propertylabelFont 的获取函数。

### `[signal] void QBarSet::labelFontChanged()`

**作用与语义：**

该属性包含用于绘制条形列标签的字体。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `labelFont` 的变化，不要把它当作普通函数主动调用。

### `QPen QBarSet::pen() const`

**作用与语义：**

返回用于在条形组中绘制线条的钢笔。
注意：属性笔的获取函数。

### `[signal] void QBarSet::penChanged()`

**作用与语义：**

该属性表明用来绘制条形组中条线的笔。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `pen` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QBarSet::pressed(int index)`

**作用与语义：**

当用户点击`index`条指定的条并按住鼠标按钮时，会发出该信号。

### `[signal] void QBarSet::released(int index)`

**作用与语义：**

当用户松开鼠标按键时，该信号会在`index`条中指定的条形上释放。

### `void QBarSet::remove(const int index, const int count = 1)`

**作用与语义：**

从`index`指定的值开始的条形集合中移除`count`指定的数值。

### `void QBarSet::replace(const int index, const qreal value)`

**作用与语义：**

将`value`指定的值加到`index`指定位置的条形。

### `[since 6.2] void QBarSet::selectAllBars()`

**作用与语义：**

标记该系列中的所有条为已选中。
注意：会发出`QBarSet::selectedBarsChanged`。

### `[since 6.2] void QBarSet::selectBar(int index)`

**作用与语义：**

标记`index`条为已选中。
注意：发出`QBarSet::selectedBarsChanged`。

### `[since 6.2] void QBarSet::selectBars(const QList<int> &indexes)`

**作用与语义：**

标记`indexes`列表中多个通过的条纹为已选中。
注意：会发出`QBarSet::selectedBarsChanged`。

### `[since 6.2] QList<int> QBarSet::selectedBars() const`

**作用与语义：**

返回标记为已选中的条列列表。

### `[since 6.2] QColor QBarSet::selectedColor() const`

**作用与语义：**

返回所选条的颜色。
这是标记为已选中的条的填充（刷）颜色。如果未指定，默认使用`QBarSet::color`值。

### `[since 6.2] void QBarSet::setBarSelected(int index, bool selected)`

**作用与语义：**

标记`index`条为已选中或取消，依照`selected`规定。
注意：如果指定了颜色，选中的条纹将使用选定颜色绘制。会发出`QBarSet::selectedBarsChanged`。

### `void QBarSet::setBorderColor(QColor color)`

**作用与语义：**

该属性表示条形组的线（笔）颜色。

**如何使用：** 调用 `setBorderColor(...)` 修改 `borderColor`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QBarSet::setBrush(const QBrush &brush)`

**作用与语义：**

该属性包含用于填补条形条的画刷。

**如何使用：** 调用 `setBrush(...)` 修改 `brush`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QBarSet::setColor(QColor color)`

**作用与语义：**

该属性保留了条形集的填充（刷）颜色。

**如何使用：** 调用 `setColor(...)` 修改 `color`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QBarSet::setLabel(const QString label)`

**作用与语义：**

该属性表示条形集的标签。

**如何使用：** 调用 `setLabel(...)` 修改 `label`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QBarSet::setLabelBrush(const QBrush &brush)`

**作用与语义：**

该属性包含用于绘制条形组标签的画刷。

**如何使用：** 调用 `setLabelBrush(...)` 修改 `labelBrush`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QBarSet::setLabelColor(QColor color)`

**作用与语义：**

该属性包含条形棒集的文本（标签）颜色。

**如何使用：** 调用 `setLabelColor(...)` 修改 `labelColor`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QBarSet::setLabelFont(const QFont &font)`

**作用与语义：**

该属性包含用于绘制条形列标签的字体。

**如何使用：** 调用 `setLabelFont(...)` 修改 `labelFont`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QBarSet::setPen(const QPen &pen)`

**作用与语义：**

该属性表明用来绘制条形组中条线的笔。

**如何使用：** 调用 `setPen(...)` 修改 `pen`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `[since 6.2] void QBarSet::setSelectedColor(const QColor &color)`

**作用与语义：**

设置所选小条的 `color`。

### `qreal QBarSet::sum() const`

**作用与语义：**

返回条形集中所有值的和。

### `[since 6.2] void QBarSet::toggleSelection(const QList<int> &indexes)`

**作用与语义：**

将给定`indexes`条的选择状态改为相反状态。
注意：会发出`QBarSet::selectedBarsChanged`。

### `[signal] void QBarSet::valueChanged(int index)`

**作用与语义：**

当`index`指定位置的值被修改时，会发出该信号。

### `[signal] void QBarSet::valuesAdded(int index, int count)`

**作用与语义：**

当向条形组添加新值时，会发出该信号。`index`表示第一个插入值的位置，`count` 表示插入值的数量。

### `[signal] void QBarSet::valuesRemoved(int index, int count)`

**作用与语义：**

当从条形组中移除数值时，该信号会发出。`index`表示第一个被移除值的位置，`count` 表示被移除的数值数量。

### `QBarSet &QBarSet::operator<<(const qreal &value)`

**作用与语义：**

一个方便算子，用于将`value`指定的实值附加到条形集末尾。

### `qreal QBarSet::operator[](const int index) const`

**作用与语义：**

返回由`index`指定的条形集合值。如果索引超出边界，返回0.0。

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

`QBarSet` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
