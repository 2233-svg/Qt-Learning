# QPieSeries

> Qt 6.11.1 · Qt Charts

## 1. 先建立直觉

**一句话定位：** `QPieSeries` 是 Qt 对象机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Charts 提供折线、柱状、饼图、散点图和坐标轴等数据可视化组件。

### 这是什么

`QPieSeries` 是 Qt 对象机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

**适用场景：** 使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

## 2. 依赖与对象关系

- 头文件：`#include <QPieSeries>`
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

- `count : int`
- `endAngle : qreal`
- `holeSize : qreal`
- `horizontalPosition : qreal`
- `size : qreal`
- `startAngle : qreal`
- `sum : qreal`
- `verticalPosition : qreal`

### 公有函数

- `QPieSeries(QObject *parent = nullptr)`
- `virtual ~QPieSeries()`
- `bool append(QPieSlice *slice)`
- `bool append(const QList<QPieSlice *> &slices)`
- `QPieSlice * append(const QString &label, qreal value)`
- `void clear()`
- `int count() const`
- `qreal holeSize() const`
- `qreal horizontalPosition() const`
- `bool insert(int index, QPieSlice *slice)`
- `bool isEmpty() const`
- `qreal pieEndAngle() const`
- `qreal pieSize() const`
- `qreal pieStartAngle() const`
- `bool remove(QPieSlice *slice)`
- `void setHoleSize(qreal holeSize)`
- `void setHorizontalPosition(qreal relativePosition)`
- `void setLabelsPosition(QPieSlice::LabelPosition position)`
- `void setLabelsVisible(bool visible = true)`
- `void setPieEndAngle(qreal angle)`
- `void setPieSize(qreal relativeSize)`
- `void setPieStartAngle(qreal startAngle)`
- `void setVerticalPosition(qreal relativePosition)`
- `QList<QPieSlice *> slices() const`
- `qreal sum() const`
- `bool take(QPieSlice *slice)`
- `qreal verticalPosition() const`
- `QPieSeries & operator<<(QPieSlice *slice)`

### 重实现的公有函数

- `virtual QAbstractSeries::SeriesType type() const override`

### 信号

- `void added(const QList<QPieSlice *> &slices)`
- `void clicked(QPieSlice *slice)`
- `void countChanged()`
- `void doubleClicked(QPieSlice *slice)`
- `void hovered(QPieSlice *slice, bool state)`
- `void pressed(QPieSlice *slice)`
- `void released(QPieSlice *slice)`
- `void removed(const QList<QPieSlice *> &slices)`
- `void sumChanged()`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[read-only] count : int`

**作用与语义：**

该属性表示系列中的切片数。

**如何使用：** 调用 `count()` 读取当前值；它不会修改应用状态。

### `endAngle : qreal`

**作用与语义：**

该属性表示饼的终点角。
一个完整的派是360度，0度是在午夜12点钟方向。
默认数值是360。

**如何使用：** 调用 `endAngle()` 读取当前值；它不会修改应用状态。

### `holeSize : qreal`

**作用与语义：**

该属性具有甜甜圈洞的大小。
该值相对于图表矩形表示，因此：
- 0.0 是最小大小（无孔完整圆饼）。
- 1.0 是能容纳图表的最大尺寸（甜甜圈没有宽度）。
设置该属性时，如有必要会调整`size`属性，以确保孔径不大于饼大小。
默认值为0.0。

**如何使用：** 调用 `holeSize()` 读取当前值；它不会修改应用状态。

### `horizontalPosition : qreal`

**作用与语义：**

该属性表示饼的水平位置。
该值相对于图表矩形表示，因此：
- 0.0 是绝对左。
- 1.0 是绝对右转。
默认数值为0.5（中心）。

**如何使用：** 调用 `horizontalPosition()` 读取当前值；它不会修改应用状态。

### `size : qreal`

**作用与语义：**

该属性表示饼的大小。
该值相对于图表矩形表示，因此：
- 0.0 是最小大小（未绘制的饼）。
- 1.0 是该图表的最大尺寸。
设置该属性时，如有必要会调整`holeSize`属性，以确保孔径不大于饼大小。
默认值是0.7。

**如何使用：** 调用 `size()` 读取当前值；它不会修改应用状态。

### `startAngle : qreal`

**作用与语义：**

该属性表示了饼的起始角度。
一个完整的派是360度，0度是在午夜12点钟方向。
默认值是0。

**如何使用：** 调用 `startAngle()` 读取当前值；它不会修改应用状态。

### `[read-only] sum : qreal`

**作用与语义：**

该属性表示所有切片的和。
该系列记录所有切片的总和。

**如何使用：** 调用 `sum()` 读取当前值；它不会修改应用状态。

### `verticalPosition : qreal`

**作用与语义：**

该属性表示饼的垂直位置。
该值相对于图表矩形表示，因此：
- 0.0 是绝对上限。
- 1.0 是绝对底值。
默认数值为0.5（中心）。

**如何使用：** 调用 `verticalPosition()` 读取当前值；它不会修改应用状态。

### `[explicit] QPieSeries::QPieSeries(QObject *parent = nullptr)`

**作用与语义：**

构造一个是`parent`子的系列对象。

### `[virtual noexcept] QPieSeries::~QPieSeries()`

**作用与语义：**

去除馅饼系列及其切片。

### `[signal] void QPieSeries::added(const QList<QPieSlice *> &slices)`

**作用与语义：**

当`slices`指定的切片加入序列时，该信号会发出。

### `bool QPieSeries::append(QPieSlice *slice)`

**作用与语义：**

将`slice`指定的切片附加到序列中。切片所有权转移给该列。
如果附加成功，返回`true`。

### `bool QPieSeries::append(const QList<QPieSlice *> &slices)`

**作用与语义：**

将`slices`指定的片数组附加到序列中。片的所有权传递给序列。
如果附加成功，返回`true`。

### `QPieSlice *QPieSeries::append(const QString &label, qreal value)`

**作用与语义：**

将单个片附带指定`value`和`label`到序列中。片的所有权传给序列。如果`value`为`NaN`、`Inf`或`-Inf`，则返回空，且对序列不添加任何内容。

### `void QPieSeries::clear()`

**作用与语义：**

清除系列中的所有切片。

### `[signal] void QPieSeries::clicked(QPieSlice *slice)`

**作用与语义：**

当点击`slice`指定的切片时，该信号会发出。

### `int QPieSeries::count() const`

**作用与语义：**

返回该系列中切片的数量。
注意：属性计数的获取函数。

### `[signal] void QPieSeries::countChanged()`

**作用与语义：**

该属性表示系列中的切片数。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `count` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QPieSeries::doubleClicked(QPieSlice *slice)`

**作用与语义：**

当双击`slice`指定的切片时，会发出该信号。

### `[signal] void QPieSeries::hovered(QPieSlice *slice, bool state)`

**作用与语义：**

当鼠标悬停在`slice`指定的切片上时，会发出该信号。当鼠标移动到切片上时，球`state`转为`true`;当鼠标再次移开时，`false`转。

### `bool QPieSeries::insert(int index, QPieSlice *slice)`

**作用与语义：**

将`slice`指定的切片插入到系列中，然后在`index`指定位置的切片之前。切片所有权传递给系列。
插入成功时返回`true`。

### `bool QPieSeries::isEmpty() const`

**作用与语义：**

如果序列为空，返回`true`。

### `qreal QPieSeries::pieEndAngle() const`

**作用与语义：**

该属性表示饼的终点角。
一个完整的派是360度，0度是在午夜12点钟方向。
默认数值是360。

**如何使用：** 调用 `pieEndAngle()` 读取当前值；它不会修改应用状态。

### `[signal] void QPieSeries::pressed(QPieSlice *slice)`

**作用与语义：**

当用户点击`slice`指定的切片并按住鼠标按钮时，会发出该信号。

### `[signal] void QPieSeries::released(QPieSlice *slice)`

**作用与语义：**

当用户松开鼠标按压`slice`指定的切片时，会发出该信号。

### `bool QPieSeries::remove(QPieSlice *slice)`

**作用与语义：**

从序列中移除`slice`指定的单个片并永久删除。
此调用后无法引用指针。
如果清除成功，还能`true`。

### `[signal] void QPieSeries::removed(const QList<QPieSlice *> &slices)`

**作用与语义：**

当`slices`指定的片片从序列中移除时，会发出该信号。

### `void QPieSeries::setLabelsPosition(QPieSlice::LabelPosition position)`

**作用与语义：**

将所有切片标签的位置设置为`position`。
注意：该功能仅影响序列中的当前切片。如果新增切片，默认标签位置为`QPieSlice::LabelOutside`。

### `void QPieSeries::setLabelsVisible(bool visible = true)`

**作用与语义：**

将所有切片标签的可见性设置为`visible`。
注意：该功能仅影响系列中的当前切片。如果新增切片，默认标签可见性为`false`。

### `void QPieSeries::setPieEndAngle(qreal angle)`

**作用与语义：**

该属性表示饼的终点角。
一个完整的派是360度，0度是在午夜12点钟方向。
默认数值是360。

**如何使用：** 调用 `setPieEndAngle(...)` 修改 `endAngle`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QList<QPieSlice *> QPieSeries::slices() const`

**作用与语义：**

返回属于该系列的切片列表。

### `qreal QPieSeries::sum() const`

**作用与语义：**

返回该系列中所有切片值的和。
注意：属性和的得方函数。

### `[signal] void QPieSeries::sumChanged()`

**作用与语义：**

该属性表示所有切片的和。
该系列记录所有切片的总和。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `sum` 的变化，不要把它当作普通函数主动调用。

### `bool QPieSeries::take(QPieSlice *slice)`

**作用与语义：**

从系列中取一个由`slice`指定的切片。不删除切片对象。
注意：该系列仍然是切片的父对象。你必须设置父对象获得全部所有权。
如果收回操作成功，退货`true`。

### `[override virtual] QAbstractSeries::SeriesType QPieSeries::type() const`

**作用与语义：**

重新实现属性访问函数：`QAbstractSeries::type`。
回归系列类型。

### `QPieSeries &QPieSeries::operator<<(QPieSlice *slice)`

**作用与语义：**

将`slice`指定的切片附加到系列中，并返回对该系列的引用。切片所有权转移给该系列。

### `qreal holeSize() const`

**作用与语义：**

该属性具有甜甜圈洞的大小。
该值相对于图表矩形表示，因此：
- 0.0 是最小大小（无孔完整圆饼）。
- 1.0 是能容纳图表的最大尺寸（甜甜圈没有宽度）。
设置该属性时，如有必要会调整`size`属性，以确保孔径不大于饼大小。
默认值为0.0。

**如何使用：** 调用 `holeSize()` 读取当前值；它不会修改应用状态。

### `qreal horizontalPosition() const`

**作用与语义：**

该属性表示饼的水平位置。
该值相对于图表矩形表示，因此：
- 0.0 是绝对左。
- 1.0 是绝对右转。
默认数值为0.5（中心）。

**如何使用：** 调用 `horizontalPosition()` 读取当前值；它不会修改应用状态。

### `qreal pieSize() const`

**作用与语义：**

该属性表示饼的大小。
该值相对于图表矩形表示，因此：
- 0.0 是最小大小（未绘制的饼）。
- 1.0 是该图表的最大尺寸。
设置该属性时，如有必要会调整`holeSize`属性，以确保孔径不大于饼大小。
默认值是0.7。

**如何使用：** 调用 `pieSize()` 读取当前值；它不会修改应用状态。

### `qreal pieStartAngle() const`

**作用与语义：**

该属性表示了饼的起始角度。
一个完整的派是360度，0度是在午夜12点钟方向。
默认值是0。

**如何使用：** 调用 `pieStartAngle()` 读取当前值；它不会修改应用状态。

### `void setHoleSize(qreal holeSize)`

**作用与语义：**

该属性具有甜甜圈洞的大小。
该值相对于图表矩形表示，因此：
- 0.0 是最小大小（无孔完整圆饼）。
- 1.0 是能容纳图表的最大尺寸（甜甜圈没有宽度）。
设置该属性时，如有必要会调整`size`属性，以确保孔径不大于饼大小。
默认值为0.0。

**如何使用：** 调用 `setHoleSize(...)` 修改 `holeSize`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setHorizontalPosition(qreal relativePosition)`

**作用与语义：**

该属性表示饼的水平位置。
该值相对于图表矩形表示，因此：
- 0.0 是绝对左。
- 1.0 是绝对右转。
默认数值为0.5（中心）。

**如何使用：** 调用 `setHorizontalPosition(...)` 修改 `horizontalPosition`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setPieSize(qreal relativeSize)`

**作用与语义：**

该属性表示饼的大小。
该值相对于图表矩形表示，因此：
- 0.0 是最小大小（未绘制的饼）。
- 1.0 是该图表的最大尺寸。
设置该属性时，如有必要会调整`holeSize`属性，以确保孔径不大于饼大小。
默认值是0.7。

**如何使用：** 调用 `setPieSize(...)` 修改 `size`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setPieStartAngle(qreal startAngle)`

**作用与语义：**

该属性表示了饼的起始角度。
一个完整的派是360度，0度是在午夜12点钟方向。
默认值是0。

**如何使用：** 调用 `setPieStartAngle(...)` 修改 `startAngle`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setVerticalPosition(qreal relativePosition)`

**作用与语义：**

该属性表示饼的垂直位置。
该值相对于图表矩形表示，因此：
- 0.0 是绝对上限。
- 1.0 是绝对底值。
默认数值为0.5（中心）。

**如何使用：** 调用 `setVerticalPosition(...)` 修改 `verticalPosition`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `qreal verticalPosition() const`

**作用与语义：**

该属性表示饼的垂直位置。
该值相对于图表矩形表示，因此：
- 0.0 是绝对上限。
- 1.0 是绝对底值。
默认数值为0.5（中心）。

**如何使用：** 调用 `verticalPosition()` 读取当前值；它不会修改应用状态。

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

`QPieSeries` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
