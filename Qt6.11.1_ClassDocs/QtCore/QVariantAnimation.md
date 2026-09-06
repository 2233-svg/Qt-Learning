# QVariantAnimation

> Qt 6.11.1 · Qt Core

## 1. 先建立直觉

**一句话定位：** `QVariantAnimation` 是 动画时间轴机制 中的类型，负责把这一机制中的数据、状态或资源交给其他 Qt 对象使用。

**模块背景：** Qt Core 提供对象模型、事件循环、容器、字符串、文件、线程、时间和元对象系统等基础能力。

### 这是什么

`QVariantAnimation` 是动画框架中的类型，描述时间、状态、插值或动画组装行为。

**内部模型：** 动画通常由时间轴驱动属性变化；先确认动画对象、目标属性、持续时间和停止后的最终值，再组合 easing、loop 和 group。

**适用场景：** 界面过渡、状态变化和可视反馈需要平滑变化时使用。

**典型调用链：** 创建目标 -> 配置 duration/easing/start/end -> connect state/finished -> start/pause/stop -> 管理动画对象生命周期。

**先记住的坑：** 动画对象销毁会立即停止；重复 start 可能重置进度；不要用动画替代业务状态；跨线程动画通常不是正确方向。

## 2. 依赖与对象关系

- 头文件：`#include <QVariantAnimation>`
- 继承自：QAbstractAnimation
- 直接派生类：QPropertyAnimation

CMake 配置：

```cmake
find_package(Qt6 REQUIRED COMPONENTS Core)
target_link_libraries(mytarget PRIVATE Qt6::Core)
```

**继承带来的规则：** 它属于 QObject 对象模型（直接或间接继承 QObject），因此父对象、信号与槽、事件循环和线程归属是使用主线。

### 工作机制

动画通常由时间轴驱动属性变化；先确认动画对象、目标属性、持续时间和停止后的最终值，再组合 easing、loop 和 group。

### 状态、生命周期和线程

**生命周期：** 动画必须保持目标和动画对象在运行期间有效。父对象、动画组或栈对象的生命周期要覆盖播放过程；删除或替换目标时先停止动画，避免回调访问旧对象。

**状态与结果：** 区分 stopped、running、paused、finished 和 loop 重启。`stop()` 后的当前值和终值取决于具体动画类型及配置，不能把停止当成完成；完成信号才表示时间轴走完。

**线程与事件循环：** 界面动画通常属于 GUI 线程并依赖事件循环；不要用动画对象承担跨线程任务或耗时计算。后台结果应先回到正确线程，再启动属性动画。

## 3. 直接使用

界面过渡、状态变化和可视反馈需要平滑变化时使用。 使用时通常按这个过程组织：创建目标 -> 配置 duration/easing/start/end -> connect state/finished -> start/pause/stop -> 管理动画对象生命周期。
## 4. API 速查

下面列出这个类页面中的公开 API。签名保留 C++ 写法，具体参数含义和使用边界在下一节直接说明。继承而来的常用 API 会在相关类的正文中一并解释。

### 公有类型

- `KeyValue`
- `KeyValues`

### 属性

- `currentValue : QVariant`
- `duration : int`
- `easingCurve : QEasingCurve`
- `endValue : QVariant`
- `startValue : QVariant`

### 公有函数

- `QVariantAnimation(QObject *parent = nullptr)`
- `virtual ~QVariantAnimation()`
- `QBindable<int> bindableDuration()`
- `QBindable<QEasingCurve> bindableEasingCurve()`
- `QVariant currentValue() const`
- `virtual int duration() const override`
- `QEasingCurve easingCurve() const`
- `QVariant endValue() const`
- `QVariant keyValueAt(qreal step) const`
- `QVariantAnimation::KeyValues keyValues() const`
- `void setDuration(int msecs)`
- `void setEasingCurve(const QEasingCurve &easing)`
- `void setEndValue(const QVariant &value)`
- `void setKeyValueAt(qreal step, const QVariant &value)`
- `void setKeyValues(const QVariantAnimation::KeyValues &keyValues)`
- `void setStartValue(const QVariant &value)`
- `QVariant startValue() const`

### 信号

- `void valueChanged(const QVariant &value)`

### 保护函数

- `virtual QVariant interpolated(const QVariant &from, const QVariant &to, qreal progress) const`
- `virtual void updateCurrentValue(const QVariant &value)`

### 重实现的保护函数

- `virtual bool event(QEvent *event) override`
- `virtual void updateCurrentTime(int) override`
- `virtual void updateState(QAbstractAnimation::State newState, QAbstractAnimation::State oldState) override`

### 相关非成员函数

- `void qRegisterAnimationInterpolator(QVariant (*)(const T &, const T &, qreal) func)`

## 5. API 逐个说明

本节依据 Qt 6.11.1 原始类页逐项整理。每个条目先说明它实际解决的问题，再说明调用方式、返回结果和容易忽略的限制；不再用函数名拆词猜测用途。

### `[alias] QVariantAnimation::KeyValue`

**作用与语义：**

这是针对std：:p air<qreal， `QVariant`>的typedef。

### `QVariantAnimation::KeyValues`

**作用与语义：**

这是`QList`<`KeyValue`>的typedef。

### `[read-only] currentValue : QVariant`

**作用与语义：**

该属性表示动画当前值。
该属性描述当前值;即起始值与结束值之间的插值值，使用当前进度时间。该值本身来自`interpolated()`，动画运行时反复调用。
`QVariantAnimation`在当前值变化时调用虚拟`updateCurrentValue()`函数。这对需要跟踪更新的子类尤其有用。例如，`QPropertyAnimation` 用该函数来动画 Qt 属性。

**如何使用：** 调用 `currentValue()` 读取当前值；它不会修改应用状态。

### `[bindable] duration : int`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性决定了动画的持续时间。
该属性描述了动画的时长（以毫秒为单位）。默认时长为250毫秒。

**如何使用：** 调用 `duration()` 读取当前值；它不会修改应用状态。

### `[bindable] easingCurve : QEasingCurve`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性表示动画的缓和曲线。
该属性定义了动画的缓和曲线。默认情况下，使用线性缓和曲线，从而实现线性插值。例如，还提供了其他曲线，例如`QEasingCurve::InCirc`，它提供了圆形的入口曲线。另一个例子是`QEasingCurve::InOutElastic`，它对插值变体的值产生弹性效应。
`QVariantAnimation`会用`QEasingCurve::valueForProgress()`将动画的“归一化进度”（`currentTime()` / `totalDuration()`）转换为动画实际使用的有效进度。当`interpolated()`被调用时，正是这个有效进度。此外，`keyValues`中的步骤指的是这个有效进度。
缓和曲线与插值器、`interpolated()`虚拟函数以及动画时长一起使用，以控制当前值随着动画进展的变化。

**如何使用：** 调用 `easingCurve()` 读取当前值；它不会修改应用状态。

### `endValue : QVariant`

**作用与语义：**

该属性表示动画的最终价值。
该属性描述了动画的最终价值。

**如何使用：** 调用 `endValue()` 读取当前值；它不会修改应用状态。

### `startValue : QVariant`

**作用与语义：**

该属性包含动画的可选起始值。
该属性描述了动画的可选起始值。如果省略，或者起始值被分配为空`QVariant`，动画将在动画开始时使用结束的当前位置。

**如何使用：** 调用 `startValue()` 读取当前值；它不会修改应用状态。

### `QVariantAnimation::QVariantAnimation(QObject *parent = nullptr)`

**作用与语义：**

构造一个QVariantAnimation对象。`parent`传递给`QAbstractAnimation`的构造器。

### `[virtual noexcept] QVariantAnimation::~QVariantAnimation()`

**作用与语义：**

破坏了动画效果。

### `[override virtual protected] bool QVariantAnimation::event(QEvent *event)`

**作用与语义：**

重装：`QAbstractAnimation::event`（QEvent *事件）。

### `[virtual protected] QVariant QVariantAnimation::interpolated(const QVariant &from, const QVariant &to, qreal progress) const`

**作用与语义：**

该虚拟函数返回变体`from`和`to`之间的线性插值，通常在`progress`处，通常值介于0和1之间。你可以在`QVariantAnimation`的子类中重新实现该函数，提供你自己的插值算法。
注意，为了让插值能处理返回小于0或大于1的`QEasingCurve`（如`QEasingCurve::InBack`），你应确保它可以外推。如果数据类型的语义不允许外推，这个函数应该能优雅地处理。
如果你想让你的类处理 Qt 已经支持的类型，你应该调用该函数的 `QVariantAnimation` 实现（请参见类 `QVariantAnimation` 描述中的支持类型列表）。

### `QVariant QVariantAnimation::keyValueAt(qreal step) const`

**作用与语义：**

返回给定`step`的关键帧值。给定`step`必须在0到1之间。如果没有`step`的`KeyValue`，则返回无效`QVariant`。

### `QVariantAnimation::KeyValues QVariantAnimation::keyValues() const`

**作用与语义：**

返回该动画的关键帧。

### `void QVariantAnimation::setKeyValueAt(qreal step, const QVariant &value)`

**作用与语义：**

在给定`step`创建关键帧，并以给定`value`。给定`step`必须在0到1之间。

### `void QVariantAnimation::setKeyValues(const QVariantAnimation::KeyValues &keyValues)`

**作用与语义：**

用给定的`keyValues`替换当前的关键帧集合。关键帧的步长必须在0到1之间。

### `[override virtual protected] void QVariantAnimation::updateCurrentTime(int)`

**作用与语义：**

重实现自：`QAbstractAnimation::updateCurrentTime`（int currentTime）。
每次动画`currentTime`变化时都会调用这个纯虚拟函数。

### `[virtual protected] void QVariantAnimation::updateCurrentValue(const QVariant &value)`

**作用与语义：**

每次动画当前值变化时都会调用这个虚拟函数。`value`参数是新的当前值。
基础类实现什么都不做。

### `[override virtual protected] void QVariantAnimation::updateState(QAbstractAnimation::State newState, QAbstractAnimation::State oldState)`

**作用与语义：**

重实现自：`QAbstractAnimation::updateState`（QAbstractAnimation：：State newState， QAbstractAnimation：：State oldState）。
当动画状态从`oldState`变为`newState`时，`QAbstractAnimation`调用了这个虚拟函数。

### `[signal] void QVariantAnimation::valueChanged(const QVariant &value)`

**作用与语义：**

该属性表示动画当前值。
该属性描述当前值;即起始值与结束值之间的插值值，使用当前进度时间。该值本身来自`interpolated()`，动画运行时反复调用。
`QVariantAnimation`在当前值变化时调用虚拟`updateCurrentValue()`函数。这对需要跟踪更新的子类尤其有用。例如，`QPropertyAnimation` 用该函数来动画 Qt 属性。

**如何使用：** 这是变化通知信号。用 `connect()` 监听 `currentValue` 的变化，不要把它当作普通函数主动调用。

### `template <typename T> void qRegisterAnimationInterpolator(QVariant (*)(const T &, const T &, qreal) func)`

**作用与语义：**

注册模板类型`T`的自定义插值器`func`。在构建动画之前，必须先注册该插值器。要取消注册（并使用默认插值器），请将`func`设置为`nullptr`。
注意：该功能是线程安全的。

### `KeyValue`

**作用与语义：**

这是针对std：:p air<qreal， `QVariant`>的typedef。

### `KeyValues`

**作用与语义：**

这是`QList`<`KeyValue`>的typedef。

### `QBindable<int> bindableDuration()`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性决定了动画的持续时间。
该属性描述了动画的时长（以毫秒为单位）。默认时长为250毫秒。

**如何使用：** 调用 `bindableDuration()` 取得 `duration` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `QBindable<QEasingCurve> bindableEasingCurve()`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性表示动画的缓和曲线。
该属性定义了动画的缓和曲线。默认情况下，使用线性缓和曲线，从而实现线性插值。例如，还提供了其他曲线，例如`QEasingCurve::InCirc`，它提供了圆形的入口曲线。另一个例子是`QEasingCurve::InOutElastic`，它对插值变体的值产生弹性效应。
`QVariantAnimation`会用`QEasingCurve::valueForProgress()`将动画的“归一化进度”（`currentTime()` / `totalDuration()`）转换为动画实际使用的有效进度。当`interpolated()`被调用时，正是这个有效进度。此外，`keyValues`中的步骤指的是这个有效进度。
缓和曲线与插值器、`interpolated()`虚拟函数以及动画时长一起使用，以控制当前值随着动画进展的变化。

**如何使用：** 调用 `bindableEasingCurve()` 取得 `easingCurve` 的 `QBindable`，用于建立属性绑定；只读取当前值时直接使用普通 getter。

### `QVariant currentValue() const`

**作用与语义：**

该属性表示动画当前值。
该属性描述当前值;即起始值与结束值之间的插值值，使用当前进度时间。该值本身来自`interpolated()`，动画运行时反复调用。
`QVariantAnimation`在当前值变化时调用虚拟`updateCurrentValue()`函数。这对需要跟踪更新的子类尤其有用。例如，`QPropertyAnimation` 用该函数来动画 Qt 属性。

**如何使用：** 调用 `currentValue()` 读取当前值；它不会修改应用状态。

### `virtual int duration() const override`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性决定了动画的持续时间。
该属性描述了动画的时长（以毫秒为单位）。默认时长为250毫秒。

**如何使用：** 调用 `duration()` 读取当前值；它不会修改应用状态。

### `QEasingCurve easingCurve() const`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性表示动画的缓和曲线。
该属性定义了动画的缓和曲线。默认情况下，使用线性缓和曲线，从而实现线性插值。例如，还提供了其他曲线，例如`QEasingCurve::InCirc`，它提供了圆形的入口曲线。另一个例子是`QEasingCurve::InOutElastic`，它对插值变体的值产生弹性效应。
`QVariantAnimation`会用`QEasingCurve::valueForProgress()`将动画的“归一化进度”（`currentTime()` / `totalDuration()`）转换为动画实际使用的有效进度。当`interpolated()`被调用时，正是这个有效进度。此外，`keyValues`中的步骤指的是这个有效进度。
缓和曲线与插值器、`interpolated()`虚拟函数以及动画时长一起使用，以控制当前值随着动画进展的变化。

**如何使用：** 调用 `easingCurve()` 读取当前值；它不会修改应用状态。

### `QVariant endValue() const`

**作用与语义：**

该属性表示动画的最终价值。
该属性描述了动画的最终价值。

**如何使用：** 调用 `endValue()` 读取当前值；它不会修改应用状态。

### `void setDuration(int msecs)`

**作用与语义：**

注意：该特性支持`QProperty`绑定。
该属性决定了动画的持续时间。
该属性描述了动画的时长（以毫秒为单位）。默认时长为250毫秒。

**如何使用：** 调用 `setDuration(...)` 修改 `duration`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setEasingCurve(const QEasingCurve &easing)`

**作用与语义：**

注意：此特性支持`QProperty`绑定。
该属性表示动画的缓和曲线。
该属性定义了动画的缓和曲线。默认情况下，使用线性缓和曲线，从而实现线性插值。例如，还提供了其他曲线，例如`QEasingCurve::InCirc`，它提供了圆形的入口曲线。另一个例子是`QEasingCurve::InOutElastic`，它对插值变体的值产生弹性效应。
`QVariantAnimation`会用`QEasingCurve::valueForProgress()`将动画的“归一化进度”（`currentTime()` / `totalDuration()`）转换为动画实际使用的有效进度。当`interpolated()`被调用时，正是这个有效进度。此外，`keyValues`中的步骤指的是这个有效进度。
缓和曲线与插值器、`interpolated()`虚拟函数以及动画时长一起使用，以控制当前值随着动画进展的变化。

**如何使用：** 调用 `setEasingCurve(...)` 修改 `easingCurve`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setEndValue(const QVariant &value)`

**作用与语义：**

该属性表示动画的最终价值。
该属性描述了动画的最终价值。

**如何使用：** 调用 `setEndValue(...)` 修改 `endValue`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `void setStartValue(const QVariant &value)`

**作用与语义：**

该属性包含动画的可选起始值。
该属性描述了动画的可选起始值。如果省略，或者起始值被分配为空`QVariant`，动画将在动画开始时使用结束的当前位置。

**如何使用：** 调用 `setStartValue(...)` 修改 `startValue`；传入的新值会成为后续查询和相关界面行为所使用的值。

### `QVariant startValue() const`

**作用与语义：**

该属性包含动画的可选起始值。
该属性描述了动画的可选起始值。如果省略，或者起始值被分配为空`QVariant`，动画将在动画开始时使用结束的当前位置。

**如何使用：** 调用 `startValue()` 读取当前值；它不会修改应用状态。

## 6. 深入实践与常见坑

### 生命周期和资源边界

动画必须保持目标和动画对象在运行期间有效。父对象、动画组或栈对象的生命周期要覆盖播放过程；删除或替换目标时先停止动画，避免回调访问旧对象。

### 状态和错误边界

区分 stopped、running、paused、finished 和 loop 重启。`stop()` 后的当前值和终值取决于具体动画类型及配置，不能把停止当成完成；完成信号才表示时间轴走完。

### 线程边界

界面动画通常属于 GUI 线程并依赖事件循环；不要用动画对象承担跨线程任务或耗时计算。后台结果应先回到正确线程，再启动属性动画。

### 最容易出现的错误

动画对象销毁会立即停止；重复 start 可能重置进度；不要用动画替代业务状态；跨线程动画通常不是正确方向。

### 版本和平台

本文档以 Qt 6.11.1 为依据。涉及平台后端、编解码器、数据库驱动、窗口风格、编译器特性或标注了版本号的 API 时，要把版本条件当作使用约束，而不是只看函数是否能补全。

## 7. 使用边界

`QVariantAnimation` 所属机制类型：动画时间轴机制。遇到重载时，优先对照参数类型、返回值和对象所有权；遇到布局、事件循环、线程、绘制或模型/视图问题时，要同时考虑本类与协作类之间的协议。
