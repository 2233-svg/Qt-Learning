# QBarCategoryAxis

> Qt 6.11.1 · Qt Charts

## 1. 先建立直觉

**一句话定位：** `QBarCategoryAxis` 是 Qt 对象机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Charts 提供折线、柱状、饼图、散点图和坐标轴等数据可视化组件。

### 这是什么

`QBarCategoryAxis` 是 Qt 对象机制 中的公开类型，作用是把这一机制里的一个职责封装成可组合的 API。

**内部模型：** 这类对象通常参与 Qt 元对象系统。类声明中的 `Q_OBJECT`、信号、槽、属性和可调用函数会被元对象注册；Qt 可以据此完成类型查询、信号槽连接、属性访问和事件分发。对象还带有线程归属，事件和 queued connection 会投递到对象所属线程的事件循环。

**适用场景：** 使用这类对象时，先创建并确定 parent/线程归属，再配置属性和连接信号，最后调用产生异步或状态变化的函数。耗时工作不要塞进 GUI 线程的槽函数；退出时先停止异步操作，再销毁对象。

**典型调用链：** 准备依赖和输入 -> 创建或取得对象 -> 设置必要状态 -> 调用核心 API -> 检查返回值/状态/错误 -> 处理通知或结果 -> 按所有权规则结束和清理。

**先记住的坑：** 不能复制 QObject；不能把属于其他线程的对象当作普通值直接操作；不能在信号回调中阻塞事件循环；`deleteLater()` 依赖事件循环，线程即将退出时要安排好退出和清理顺序。

## 2. 依赖与对象关系

- 头文件：`#include <QBarCategoryAxis>`
- 继承自：QAbstractAxis
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

- `categories : QStringList`
- `count : int`
- `max : QString`
- `min : QString`

### 公有函数

- `QBarCategoryAxis(QObject *parent = nullptr)`
- `virtual ~QBarCategoryAxis()`
- `void append(const QString &category)`
- `void append(const QStringList &categories)`
- `QString at(int index) const`
- `QStringList categories()`
- `void clear()`
- `int count() const`
- `void insert(int index, const QString &category)`
- `QString max() const`
- `QString min() const`
- `void remove(const QString &category)`
- `void replace(const QString &oldCategory, const QString &newCategory)`
- `void setCategories(const QStringList &categories)`
- `void setMax(const QString &max)`
- `void setMin(const QString &min)`
- `void setRange(const QString &minCategory, const QString &maxCategory)`

### 重实现的公有函数

- `virtual QAbstractAxis::AxisType type() const override`

### 信号

- `void categoriesChanged()`
- `void countChanged()`
- `void maxChanged(const QString &max)`
- `void minChanged(const QString &min)`
- `void rangeChanged(const QString &min, const QString &max)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `categories : QStringList`

**作用与语义：**

该属性表示轴的范畴。

**如何使用：** 调用 `categories()` 读取当前值；它不会修改应用状态。

### `[read-only] count : int`

**作用与语义：**

此属性保存坐标轴的类别数量。

**如何使用：** 调用 `count()` 读取当前值；它不会修改应用状态。

### `max : QString`

**作用与语义：**

该属性在轴上占最大值。

**如何使用：** 调用 `max()` 读取当前值；它不会修改应用状态。

### `min : QString`

**作用与语义：**

该属性在轴上保持最小值。

**如何使用：** 调用 `min()` 读取当前值；它不会修改应用状态。

### `[explicit] QBarCategoryAxis::QBarCategoryAxis(QObject *parent = nullptr)`

**作用与语义：**

构造一个轴对象，该轴对象是`parent`的子节点。

### `[virtual noexcept] QBarCategoryAxis::~QBarCategoryAxis()`

**作用与语义：**

摧毁轴对象。

### `void QBarCategoryAxis::append(const QString &category)`

**作用与语义：**

附加`category`到一个轴上。轴上的最大值将被调整为与上一个`category`相匹配。如果之前没有定义类别，轴上的最小值也会调整为匹配`category`。
类别必须是有效的`QString`且不能重复。重复的类别不会被附加。

### `void QBarCategoryAxis::append(const QStringList &categories)`

**作用与语义：**

附加`categories`到一个轴上。轴上的最大值将被更改为与`categories`中最后一个类别相匹配。如果之前没有定义过类别，轴上的最小值也会被更改为与`categories`中的第一个类别相匹配。
类别必须是有效的`QString`且不能重复。重复的类别不会被附加。

### `QString QBarCategoryAxis::at(int index) const`

**作用与语义：**

返回`index`的类别。索引必须有效。

### `QStringList QBarCategoryAxis::categories()`

**作用与语义：**

退货类别。
注意：属性类别的获取函数。

### `[signal] void QBarCategoryAxis::categoriesChanged()`

**作用与语义：**

该属性表示轴的范畴。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `categories` 的变化，不要把它当作普通函数主动调用。

### `[invokable] void QBarCategoryAxis::clear()`

**作用与语义：**

移除所有类别。将轴范围的最大值和最小值设置为 QString：：null。
注意：该函数可通过元对象系统和QML调用。参见`Q_INVOKABLE`。

### `int QBarCategoryAxis::count() const`

**作用与语义：**

返回类别数量。
注意：属性计数的获取函数。

### `[signal] void QBarCategoryAxis::countChanged()`

**作用与语义：**

此属性保存坐标轴的类别数量。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `count` 的变化，不要把它当作普通函数主动调用。

### `void QBarCategoryAxis::insert(int index, const QString &category)`

**作用与语义：**

插入`category`到轴线`index`。`category`必须是有效的`QString`，且不能重复。如果`category`在其他类别前加或附加，轴上的最小值和最大值会相应更新。

### `QString QBarCategoryAxis::max() const`

**作用与语义：**

返回最大类别。
注意：属性最大值的获取函数。

### `[signal] void QBarCategoryAxis::maxChanged(const QString &max)`

**作用与语义：**

该属性在轴上占最大值。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `max` 的变化，不要把它当作普通函数主动调用。

### `QString QBarCategoryAxis::min() const`

**作用与语义：**

返回最小类别。
注意：属性最小值的求得函数。

### `[signal] void QBarCategoryAxis::minChanged(const QString &min)`

**作用与语义：**

该属性在轴上保持最小值。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `min` 的变化，不要把它当作普通函数主动调用。

### `[signal] void QBarCategoryAxis::rangeChanged(const QString &min, const QString &max)`

**作用与语义：**

当轴的`min`或`max`值变化时，该信号会发出。

### `void QBarCategoryAxis::remove(const QString &category)`

**作用与语义：**

移除轴上的`category`。移除当前设定轴最大值或最小值的类别会影响轴的范围。

### `void QBarCategoryAxis::replace(const QString &oldCategory, const QString &newCategory)`

**作用与语义：**

用`newCategory`替换`oldCategory`。如果轴上不存在`oldCategory`，则不做任何处理。`newCategory`必须是有效的`QString`，且不能被复制。如果最小或最大类别被替换，轴上的最小值和最大值也会相应更新。

### `void QBarCategoryAxis::setCategories(const QStringList &categories)`

**作用与语义：**

该属性表示轴的范畴。

**如何使用：** 调用 `setCategories(...)` 修改 `categories`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QBarCategoryAxis::setMax(const QString &max)`

**作用与语义：**

该属性在轴上占最大值。

**如何使用：** 调用 `setMax(...)` 修改 `max`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QBarCategoryAxis::setMin(const QString &min)`

**作用与语义：**

该属性在轴上保持最小值。

**如何使用：** 调用 `setMin(...)` 修改 `min`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void QBarCategoryAxis::setRange(const QString &minCategory, const QString &maxCategory)`

**作用与语义：**

轴线范围从`minCategory`到`maxCategory`。

### `[override virtual] QAbstractAxis::AxisType QBarCategoryAxis::type() const`

**作用与语义：**

重装：`QAbstractAxis::type()` const.
返回轴的类型。
返回轴的类型。

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

`QBarCategoryAxis` 所属机制类型：Qt 对象机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
